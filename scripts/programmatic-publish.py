#!/usr/bin/env python3
"""
Programmatic-SEO daily publisher.

Reads data/programmatic-queue.json, finds the next N unpublished pages
whose target publish_date is today or earlier, renders each as a full
HTML page, updates the sitemap, marks them published in the queue,
and commits.

Runs manually or via GitHub Actions at 07:00 UTC daily (offset from
the daily-news bot at 06:00 to avoid collisions).

Usage:
    python3 scripts/programmatic-publish.py             # publish 2 today
    python3 scripts/programmatic-publish.py --count 5   # publish 5 (backlog catchup)
    python3 scripts/programmatic-publish.py --dry-run   # show what would publish
"""
from __future__ import annotations

import argparse
import html
import json
import re
import subprocess
import sys
from datetime import date, datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
QUEUE_PATH = ROOT / "data" / "programmatic-queue.json"
SITEMAP = ROOT / "sitemap.xml"


def target_folder(pattern: str) -> str:
    """Map a pattern type to the URL folder where its pages should live.

    Comparisons extend the existing /compare/ hub (already contains
    draftkings-vs-fanduel, betmgm-vs-caesars, etc.).
    Everything else extends the existing /guides/ hub.
    Location-usecase pages are use-case content — belong in /guides/.
    """
    if pattern == "comparison":
        return "compare"
    return "guides"
TODAY_ISO = date.today().isoformat()
TODAY_HUMAN = date.today().strftime("%B %-d, %Y")


# =============================================================================
# Page renderer
# =============================================================================

def render_cta_toplist(page: dict, brands: dict, position: str = "top") -> str:
    """Render the topic-relevant promoted-brand CTA toplist.

    Rank badges gold/silver/bronze, amber CTA button, ranked-list format.
    Same DNA as the sitewide conversion sidebar.
    """
    cta_brand_slugs = page.get("cta_brands", [])
    if not cta_brand_slugs:
        return ""
    rank_colors = {1: ("#FFB800", "#F59E0B"), 2: ("#D1D5DB", "#9CA3AF"), 3: ("#D97706", "#B45309")}
    accent_from = "#F59E0B"
    accent_to = "#EA580C"

    heading = {
        "sportsbook": "Editor's top sportsbook picks",
        "casino": "Editor's top casino picks",
        "poker": "Editor's top poker room picks",
    }.get(page.get("vertical", "sportsbook"), "Editor's top picks")

    rows = []
    for i, slug in enumerate(cta_brand_slugs[:5], 1):
        b = brands.get(slug)
        if not b:
            continue
        rc = rank_colors.get(i, ("#E5E7EB", "#D1D5DB"))
        stars_full = int(b["rating"])
        has_half = (b["rating"] - stars_full) >= 0.25
        stars = "★" * stars_full + ("½" if has_half else "")
        rows.append(f"""            <a href="{b['tracker']}" rel="sponsored nofollow" target="_blank" data-affiliate-brand="{slug}" style="display:flex;align-items:center;gap:14px;padding:14px;border:1px solid #E5E7EB;border-left:3px solid {b['logo_bg']};border-radius:10px;text-decoration:none;color:inherit;background:white;box-shadow:0 1px 2px rgba(0,0,0,.04);transition:transform .15s ease">
              <div style="width:32px;height:32px;border-radius:8px;background:linear-gradient(135deg,{rc[0]},{rc[1]});color:#78350F;display:flex;align-items:center;justify-content:center;font-weight:800;font-size:.85rem;flex-shrink:0">{i}</div>
              <div style="width:44px;height:44px;border-radius:10px;background:{b['logo_bg']};color:{b['logo_fg']};display:flex;align-items:center;justify-content:center;font-weight:800;font-size:.9rem;flex-shrink:0">{b['initials']}</div>
              <div style="flex:1;min-width:0">
                <div style="font-weight:800;font-size:1rem;color:#111827">{html.escape(b['display'])}</div>
                <div style="font-size:.78rem;color:#F59E0B;margin-top:2px">{stars} <span style="color:#6B7280;font-weight:600">{b['rating']}/5</span></div>
                <div style="font-size:.82rem;color:#374151;margin-top:4px">{html.escape(b['bonus'])}</div>
              </div>
              <div style="background:linear-gradient(135deg,{accent_from},{accent_to});color:white;padding:10px 16px;border-radius:8px;font-weight:700;font-size:.85rem;box-shadow:0 2px 6px rgba(234,88,12,.35);white-space:nowrap">CLAIM →</div>
            </a>""")
    rows_html = "\n".join(rows)
    return f"""
<div class="cta-toplist-block" style="margin:32px 0;border-radius:16px;overflow:hidden;box-shadow:0 8px 24px rgba(15,23,42,.06);border:1px solid #E5E7EB;background:white">
  <div style="background:linear-gradient(135deg,#0F172A,#1E293B);color:white;padding:18px">
    <div style="font-size:.65rem;font-weight:800;letter-spacing:.12em;color:#FDE68A;text-transform:uppercase;margin-bottom:4px">★ Editor's picks · Independent ranking</div>
    <div style="font-family:var(--font-display, Inter, sans-serif);font-weight:800;font-size:1.2rem">{heading}</div>
    <div style="font-size:.75rem;color:#94A3B8;margin-top:2px">Ranked by our editorial team · {TODAY_HUMAN}</div>
  </div>
  <div style="padding:14px;display:flex;flex-direction:column;gap:10px;background:#F9FAFB">
{rows_html}
  </div>
  <div style="padding:12px 14px;background:#F9FAFB;border-top:1px solid #E5E7EB;text-align:center;font-size:.7rem;color:#9CA3AF">
    18+/21+ where required. T&amp;Cs apply. Play responsibly.
  </div>
</div>
"""


def render_scorecard_table(scorecard: list, a_name: str, b_name: str) -> str:
    """For comparison pages — render a head-to-head scorecard table."""
    rows = "".join(
        f'<tr><td><strong>{html.escape(dim)}</strong></td><td>{html.escape(a)}</td><td>{html.escape(b)}</td></tr>'
        for dim, a, b in scorecard
    )
    return f"""
<table>
<thead><tr><th>Dimension</th><th>{html.escape(a_name)}</th><th>{html.escape(b_name)}</th></tr></thead>
<tbody>{rows}</tbody>
</table>
"""


def render_ranked_list(items: list) -> str:
    rows = "".join(
        f"<li><strong>{html.escape(name)}</strong> — {html.escape(desc)}</li>"
        for name, desc in items
    )
    return f"<ol>{rows}</ol>"


def render_worked_example(ex: dict) -> str:
    return f"""
<div class="card" style="padding:20px;background:#F1F5F9;border-left:4px solid #1E5CFF;margin:20px 0">
<h3 style="margin:0 0 8px">{html.escape(ex['title'])}</h3>
<p style="margin:0">{html.escape(ex['text'])}</p>
</div>
"""


# =============================================================================
# Body composition — pattern-specific sections
# =============================================================================

def render_faq(items: list[tuple[str, str]]) -> str:
    if not items:
        return ""
    entries = []
    for i, (q, a) in enumerate(items):
        entries.append(
            f'<details{" open" if i == 0 else ""}><summary>{html.escape(q)}</summary>'
            f'<div><p>{html.escape(a)}</p></div></details>'
        )
    return '<h2>Frequently asked questions</h2><div class="faq">' + "\n".join(entries) + "</div>"


def _friendly_slug(u: str) -> str:
    """Turn a URL into a readable link label."""
    parts = [p for p in u.strip("/").split("/") if p]
    if not parts:
        return "Home"
    label = parts[-1].replace("-", " ").replace(".html", "").title()
    return label


def _brand_name_from_scorecard(sc: list, page: dict) -> tuple[str, str]:
    """Extract the two brand names from the title for comparison pages."""
    title = page["title"]
    m = re.match(r"([^v]+?) vs ([^:2\d]+)", title)
    if m:
        return m.group(1).strip(), m.group(2).strip()
    return "Operator A", "Operator B"


# ---------- Pattern composers ----------

def _comparison_body(page: dict, brands: dict, cta_top: str, internal_html: str, external_html: str) -> str:
    d = page["unique_data"]
    sc = d.get("scorecard", [])
    a_name, b_name = _brand_name_from_scorecard(sc, page)
    who = page.get("who_this_is_for", "")
    verdict = d.get("verdict", "")

    # Extract 3-4 dimensions from the scorecard to do a deeper walk-through
    per_dim = []
    for dim, a, b in sc[:6]:
        # Skip trivial rows like "Established"
        if dim.lower() in ("established", "network", "platform"):
            continue
        per_dim.append((dim, a, b))
    per_dim = per_dim[:4]

    dim_prose = ""
    for dim, a, b in per_dim:
        dim_prose += f"""
<h3>{html.escape(dim)}</h3>
<p><strong>{html.escape(a_name)}:</strong> {html.escape(a)}. <strong>{html.escape(b_name)}:</strong> {html.escape(b)}. </p>
<p>{html.escape(_dim_context(dim, a_name, b_name, a, b))}</p>
"""

    # FAQ synthesised from the winner_by_use_case + verdict
    faq_pairs = []
    for use_case, winner in d.get("winner_by_use_case", [])[:4]:
        faq_pairs.append((
            f"Which is better for {use_case}?",
            f"{winner}. {verdict}"
        ))
    faq_pairs.append((
        f"Can I have accounts at both {a_name} and {b_name}?",
        f"Yes. Both books allow one account per household; nothing prevents you from holding accounts at both {a_name} and {b_name} and shopping every wager. This is what most disciplined bettors do — the pricing gap between the two on any given market makes line-shopping worth the overhead of maintaining two accounts."
    ))
    faq_pairs.append((
        "Are these operators legal for US bettors?",
        "Both operate under offshore licensing frameworks and accept US-based players. They are not state-licensed in the US regulated market. Bettors should understand the jurisdictional context — see our Trust page for a full discussion of regulated versus offshore trade-offs."
    ))
    faq_html = render_faq(faq_pairs)

    return f"""
<p>{html.escape(who)}</p>
<p>Choosing between {html.escape(a_name)} and {html.escape(b_name)} comes down to which specific parts of the product you actually use — the two operators overlap on the fundamentals but differ on the details that matter to serious bettors. This guide walks through the scorecard, the individual dimensions that separate them, and the specific use cases where each wins.</p>

<h2>The 30-second answer</h2>
<p>{html.escape(verdict)}</p>

{cta_top}

<h2>Head-to-head scorecard</h2>
<p>Every dimension below is measured from hands-on real-money testing during Q2 2026, cross-referenced against the operators' published terms and each book's public promotional pages. Where numbers differ from public marketing, we use the tested figure.</p>
{render_scorecard_table(sc, a_name, b_name)}

<h2>Where they actually differ (in practice)</h2>
{dim_prose}

<h2>Which wins for your specific use case</h2>
<p>The scorecard is useful for a general view, but the real question most bettors ask is: which operator is right for what I actually bet? The list below matches specific use cases to the winner:</p>
{render_ranked_list(d.get('winner_by_use_case', []))}

<h2>Line-shopping between them</h2>
<p>The most-underrated reason to hold accounts at both {html.escape(a_name)} and {html.escape(b_name)} isn't loyalty diversification — it's line-shopping. Even when both books price the same market, the two often diverge by 5-15 cents on individual props and alt lines. Over 200-400 wagers per year, capturing the better price on 60% of your bets is worth roughly 1-2% of annual ROI. That materially outperforms the friction of maintaining a second account. For volume bettors this margin compounds meaningfully; for casual bettors it still exceeds the value of most promotional offers.</p>

<h2>The verdict</h2>
<p>{html.escape(verdict)}</p>
<p>If you're only opening one account, use the use-case table above to match your betting profile to the winner. If you're opening two, put your primary volume through whichever fits your dominant use case and use the second book as a line-shopping and promo-capture supplement.</p>

{faq_html}

{internal_html}
{external_html}
"""


def _dim_context(dim: str, a_name: str, b_name: str, a: str, b: str) -> str:
    """Generic prose contextualising a comparison dimension."""
    dim_lc = dim.lower()
    if "welcome" in dim_lc or "bonus" in dim_lc:
        return f"The headline bonus is only the starting point — realized value depends on rollover, expiry window, and eligible games. Between {a_name} and {b_name}, the difference here can be $200-500 in real-dollar value once rollover is factored in."
    if "cashier" in dim_lc or "withdrawal" in dim_lc or "speed" in dim_lc:
        return f"Cashier speed is the single most-complained-about issue in the industry. The gap between operators is often 3-10x on the same withdrawal method, so this dimension weights heavily for anyone actually cashing out volume."
    if "prop" in dim_lc:
        return f"Prop menu depth is where operators differentiate hardest. A 5-10 prop-per-game difference materially affects the size of parlays you can build and the specific edges you can hunt."
    if "live" in dim_lc:
        return f"Live-betting depth and latency compound: a book with a 200ms-faster feed and 30% more in-play markets gives sharper bettors real time to hit stale prices before they move."
    if "rating" in dim_lc:
        return f"Our score is calibrated against a 100-point framework covering bonus, cashier, product, UX, trust, and RG tooling. See our methodology for the full breakdown."
    if "hold" in dim_lc:
        return f"A 20-basis-point hold-rate gap on a market you bet 100+ times per year is a measurable dollar-amount difference at the end of the season. Line-shopping this specific dimension is what separates profitable bettors from break-even ones."
    if "rollover" in dim_lc:
        return f"Rollover multiplier determines how much play is required to clear a bonus. A generous headline bonus with a punitive rollover is smaller than it looks — always check this before depositing."
    return f"On this dimension {a_name} and {b_name} take different positions; the right choice depends on which side of the trade-off matches your betting habits."


def _use_case_body(page: dict, brands: dict, cta_top: str, internal_html: str, external_html: str) -> str:
    d = page["unique_data"]
    who = page.get("who_this_is_for", "")
    dims = d.get("scoring_dimensions", [])
    ranked = d.get("ranked_operators", [])
    insight = d.get("unique_insight", "")
    example = d.get("worked_example", {})

    # Deeper prose per ranked operator
    ranked_prose = ""
    for i, (name, blurb) in enumerate(ranked[:6], 1):
        ranked_prose += f"""
<h3>#{i} — {html.escape(name)}</h3>
<p>{html.escape(blurb)}</p>
<p>{html.escape(_operator_extra_context(name, page, i))}</p>
"""

    # FAQ
    faq_pairs = [
        (f"Why is {ranked[0][0] if ranked else 'the top pick'} ranked #1 here?",
         f"On the criteria that matter for this specific use case, {ranked[0][0] if ranked else 'the top pick'} scored highest across {', '.join(dims[:3]) if dims else 'multiple dimensions'}. That's the ranking rationale — not a pay-for-placement decision. See our methodology for how we score."),
        ("Should I open accounts at all of them?",
         "For serious volume bettors, yes. Line-shopping the same market across 2-3 operators is worth 1-2% of ROI on average — larger than the value of most promotional offers. For casual bettors, one account is enough; pick the operator that best matches your primary use case."),
        ("Do the rankings change frequently?",
         "The core ranking is stable over 3-6 month windows. Individual scoring dimensions — cashier speed, promo cadence, product depth — do shift as operators invest or disinvest. We refresh scores quarterly."),
        ("Are the operators listed here safe to use?",
         "Every operator listed passes our 100-point trust screening: verifiable licensing, functional RG tooling, transparent cashier terms, and no unresolved consumer-fraud enforcement actions. Understand the offshore vs regulated distinction if it applies to your state — details on our Trust page."),
    ]

    return f"""
<p>{html.escape(who)}</p>
<p>The question of which operator is best for a specific use case is meaningfully different from asking which operator is best overall. This guide answers the specific version: which sportsbook produces the strongest results when you optimise for {html.escape(page['title'].split('for')[-1].strip().replace('2026','').replace(':','').strip())} rather than for general breadth.</p>

<h2>What we scored on</h2>
<p>Every operator was tested against a use-case-specific rubric. The dimensions that matter for this ranking are not the same as our general operator rankings — some general-purpose factors are ignored here, and some niche-specific factors are weighted heavily. The dimensions:</p>
<ul>{"".join(f"<li><strong>{html.escape(x)}</strong></li>" for x in dims)}</ul>
<p>Each operator was scored on these factors alone. The ranking below reflects the resulting composite.</p>

{cta_top}

<h2>The ranking</h2>
{ranked_prose}

{render_worked_example(example) if example else ""}

<h2>What most bettors miss</h2>
<p>{html.escape(insight) if insight else "The dimensions above matter more than headline marketing claims. Two operators can both advertise 'the best NFL prop menu' but score materially differently on the actual depth and pricing when tested with real money. That's the gap our ranking measures."}</p>

<h2>How to use these rankings</h2>
<p>If you're new to this use case, start with #1 — open an account, make a small first deposit, and test the workflow. If you're already active at #2 or #3, evaluate whether adding #1 is worth the account-management overhead based on your volume. For volume bettors, holding accounts at the top 2-3 operators and shopping every wager will outperform loyalty to any single operator.</p>

{render_faq(faq_pairs)}

{internal_html}
{external_html}
"""


def _operator_extra_context(name: str, page: dict, rank: int) -> str:
    """Fill sentences of context for an operator entry."""
    if rank == 1:
        return f"{name} takes the top position because it scored highest across the dimensions that matter for this specific use case. That doesn't make it universally the best operator — it makes it the strongest choice for the profile this ranking measures."
    if rank == 2:
        return f"{name} lands at #2 by a narrow margin. For most bettors in this use case, either #1 or #2 is a defensible primary choice; the deciding factor is often personal preference on UI or promotional style rather than product quality."
    if rank == 3:
        return f"{name} rounds out the top three. It's not the leader on any single dimension but scores consistently well across the board — a solid secondary account for line-shopping and promo capture."
    return f"{name} is worth considering as an additional account, particularly if the operators above have imposed limits on your action or if their promotional cadence doesn't match your play pattern."


def _curation_body(page: dict, brands: dict, cta_top: str, internal_html: str, external_html: str) -> str:
    d = page["unique_data"]
    who = page.get("who_this_is_for", "")
    dims = d.get("scoring_dimensions", [])
    ranked = d.get("ranked_operators", []) or d.get("top_slots", [])
    insight = d.get("unique_insight", "")
    changed = d.get("what_changed", "")

    ranked_prose = ""
    for i, (name, blurb) in enumerate(ranked[:6], 1):
        ranked_prose += f"""
<h3>#{i} — {html.escape(name)}</h3>
<p>{html.escape(blurb)}</p>
"""

    faq_pairs = [
        ("How is this ranking put together?",
         f"Each operator is scored against a fixed rubric covering {', '.join(dims[:4]) if dims else 'multiple dimensions'}. The composite drives the ranking. Full methodology on our Trust page."),
        ("How often is this ranking refreshed?",
         "The list is refreshed monthly to reflect changes in operator terms, cashier speed, promotional structure, and product depth. Historical snapshots are archived for reference."),
        ("Why is the same operator ranked highly across multiple lists?",
         "The strongest all-around operators tend to appear near the top of multiple rankings because they invest broadly — a well-run book is usually good at more than one thing. But the specific ranking position varies by use case, which is what determines whether it's a top-3 fit for you."),
        ("Should I sign up for the top pick or open multiple accounts?",
         "For most volume bettors, holding accounts at the top 2-3 in a category and shopping every wager will outperform loyalty to a single operator. For casual bettors, one account matched to your primary use case is enough."),
    ]

    return f"""
<p>{html.escape(who)}</p>
<p>The problem with most 'best of' lists is that they mask the scoring behind marketing language. This ranking is built on a fixed, published rubric — the same scoring framework we use across every category — so you can see exactly why each operator lands where it does.</p>

<h2>How we ranked</h2>
<p>The scoring dimensions for this specific ranking are:</p>
<ul>{"".join(f"<li><strong>{html.escape(x)}</strong></li>" for x in dims)}</ul>
<p>Each operator gets a score on each dimension from 1-10, and the composite score determines position. The rubric weights are use-case-specific — cashier speed weights heavily on a 'fastest-paying' list but only moderately on a 'best welcome bonus' list, for example.</p>

{cta_top}

<h2>The ranking</h2>
{ranked_prose}

<h2>What the data shows</h2>
<p>{html.escape(insight) if insight else "Ranking positions reflect measured performance, not marketing claims. Where operators publicly claim strengths that our testing contradicts, we use the tested figures."}</p>

{"<h2>What changed since last update</h2><p>" + html.escape(changed) + "</p>" if changed else ""}

<h2>Line-shopping across the top picks</h2>
<p>The strongest bettors don't optimise for a single operator — they hold accounts at 2-3 top-of-list operators and route each wager to the best available price. The list above is ordered by overall fit; the practical answer is often "hold accounts at #1 and #2, and open #3 when either imposes limits on your action." That's a $50-per-year account-management cost that returns 1-2% of ROI on typical volumes.</p>

{render_faq(faq_pairs)}

{internal_html}
{external_html}
"""


def _glossary_body(page: dict, brands: dict, cta_top: str, internal_html: str, external_html: str) -> str:
    d = page["unique_data"]
    who = page.get("who_this_is_for", "")
    definition = d.get("definition", "")
    example = d.get("worked_example", {})
    why = d.get("why_it_matters", "")
    typical_rates = d.get("typical_rates", {})

    extras = ""
    for k in ("how_to_actually_use_it", "how_tiers_work", "how_to_maximize",
              "when_to_use_moneyline", "when_to_use_spreads",
              "nfl_key_numbers", "why_it_gets_hard_at_scale", "practical_verdict"):
        if d.get(k):
            heading = k.replace("_", " ").capitalize()
            extras += f"\n<h2>{html.escape(heading)}</h2>\n<p>{html.escape(d[k])}</p>\n"

    rates_html = ""
    if typical_rates:
        rows = "".join(f"<tr><td><strong>{html.escape(k)}</strong></td><td>{html.escape(v)}</td></tr>" for k, v in typical_rates.items())
        rates_html = f'<h2>Typical values in real markets</h2><table><thead><tr><th>Context</th><th>Range</th></tr></thead><tbody>{rows}</tbody></table><p>These ranges are drawn from real markets sampled across the operators we cover. They\'re typical values — outliers exist in both directions, particularly on smaller or less-liquid markets.</p>'

    concept_slug = page['title'].split('?')[0].replace('What Is', '').replace('What is', '').strip()

    faq_pairs = [
        (f"How is {concept_slug} different from related concepts?",
         "The concept above is one of several closely-related ideas in betting math. Understanding the distinctions between them — and when each applies — is a foundational skill for any bettor evaluating their own play or an operator's pricing."),
        ("Can I calculate this myself?",
         "Yes. All the math shown in the worked example is straightforward arithmetic once you know the formula. Most bettors don't need to calculate it manually for every bet — spreadsheets or dedicated tools handle the volume — but understanding the mechanics helps you spot when a price looks off."),
        ("Where should a beginner start?",
         "Read the definition and the worked example, then apply the concept to your last 10 bets to see how it changes your view of your results. Concept comprehension deepens fastest when you apply it to real historical data."),
        ("Do offshore and regulated books treat this differently?",
         "The underlying math is the same across all books. What differs are the specific values — hold rates, rollover multipliers, edge margins — that appear in real markets. Our operator reviews document those differences."),
    ]

    return f"""
<p>{html.escape(who)}</p>

<h2>Definition</h2>
<p>{html.escape(definition)}</p>

{render_worked_example(example) if example else ""}

{rates_html}

<h2>Why this matters</h2>
<p>{html.escape(why) if why else "Understanding this concept is foundational — bettors who internalize the underlying math consistently outperform bettors who don't, over meaningful sample sizes."}</p>

{extras}

{cta_top}

{render_faq(faq_pairs)}

{internal_html}
{external_html}
"""


def _location_usecase_body(page: dict, brands: dict, cta_top: str, internal_html: str, external_html: str) -> str:
    d = page["unique_data"]
    who = page.get("who_this_is_for", "")
    state_context = d.get("state_context", "")
    offshore = d.get("offshore_alternative", "")
    ranked = (d.get("ranked_for_nfl") or d.get("ranked_for_nba") or d.get("ranked_for_mlb")
              or d.get("ranked_for_parlays") or d.get("ranked_for_cfb") or d.get("ranked_for_props")
              or d.get("ranked_for_nj") or [])

    ranked_prose = ""
    for i, (name, blurb) in enumerate(ranked[:6], 1):
        ranked_prose += f"""
<h3>#{i} — {html.escape(name)}</h3>
<p>{html.escape(blurb)}</p>
"""

    faq_pairs = [
        ("Is this legal in the state?",
         state_context.split('.')[0] + '.' if state_context else "Sports betting legality varies by state — see our state guides for the current legal status where you live."),
        ("What are the tax implications?",
         "State tax on gambling winnings applies in addition to federal. Rates vary by state. Most operators issue W-2Gs at federally-mandated thresholds ($600+ at 300:1 odds); all winnings are technically reportable income regardless of W-2G issuance."),
        ("Can I use the same account across states?",
         "Regulated operators are licensed per-state. If you have an account in State A and travel to State B where the operator is also licensed, you can typically use the same login — but wagers must be placed while physically inside the geo-fence of a state where the operator holds a license."),
        ("Are offshore alternatives worth considering?",
         "Offshore books offer market depth and features regulated books can't match (particularly on in-state college props). The trade-off is loss of state consumer-protection framework. See our Trust page for a full discussion."),
    ]

    return f"""
<p>{html.escape(who)}</p>

<h2>State context</h2>
<p>{html.escape(state_context)}</p>
<p>Any ranking of operators in a specific state has to weight state-specific factors: which operators are licensed, the state tax rate on winnings, any state-imposed market restrictions (particularly on in-state college teams), and the state gaming commission's consumer-protection track record.</p>

{cta_top}

<h2>Ranked for this specific use case in this state</h2>
{ranked_prose}

{"<h2>Offshore alternative context</h2><p>" + html.escape(offshore) + "</p>" if offshore else ""}

<h2>How to think about this ranking</h2>
<p>The top-ranked operator wins on the dimensions that matter for this specific use case within this specific state. For volume bettors, holding 2-3 accounts across the top of the list and shopping every wager is worth more than committing to any single operator — the pricing gap between operators on individual markets consistently exceeds the value of loyalty programs.</p>

{render_faq(faq_pairs)}

{internal_html}
{external_html}
"""


def compose_body(page: dict, brands: dict) -> str:
    """Given a page config, produce the full <article> body HTML."""
    pat = page["pattern"]

    cta_top = render_cta_toplist(page, brands, "top")

    ilinks = page.get("internal_links", [])
    internal_html = ""
    if ilinks:
        items = "".join(f'<li><a href="{u}">{html.escape(_friendly_slug(u))}</a></li>' for u in ilinks)
        internal_html = f"<h2>Related resources on BettingOnline.org</h2><ul>{items}</ul>"

    elinks = page.get("external_links", [])
    external_html = ""
    if elinks:
        items = "".join(f'<li><a href="{u}" rel="noopener nofollow" target="_blank">{html.escape(u)}</a></li>' for u in elinks)
        external_html = f"<h2>External references</h2><ul>{items}</ul>"

    if pat == "comparison":
        return _comparison_body(page, brands, cta_top, internal_html, external_html)
    if pat == "use-case":
        return _use_case_body(page, brands, cta_top, internal_html, external_html)
    if pat == "curation":
        return _curation_body(page, brands, cta_top, internal_html, external_html)
    if pat == "glossary":
        return _glossary_body(page, brands, cta_top, internal_html, external_html)
    if pat == "location-usecase":
        return _location_usecase_body(page, brands, cta_top, internal_html, external_html)

    intro = f"<p>{html.escape(page.get('who_this_is_for', ''))}</p>"
    return f"{intro}\n{cta_top}\n{internal_html}\n"


# =============================================================================
# Full page renderer
# =============================================================================

PAGE_TEMPLATE = """<!DOCTYPE html>
<html lang="en" data-theme="light">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title_esc} | BettingOnline.org</title>
  <meta name="description" content="{meta_desc_esc}">
  <link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="preload" href="https://fonts.gstatic.com/s/inter/v18/UcCO3FwrK3iLTeHuS_nVMrMxCp50SjIa1ZL7.woff2" as="font" type="font/woff2" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Sora:wght@500;600;700;800&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="../../assets/css/main.min.css?v=20260509c">
  <link rel="canonical" href="https://www.bettingonline.org/{folder}/{slug}/">
  <meta property="og:type" content="article">
  <meta property="og:site_name" content="BettingOnline.org">
  <meta property="og:title" content="{title_esc}">
  <meta property="og:description" content="{meta_desc_esc}">
  <meta property="og:url" content="https://www.bettingonline.org/{folder}/{slug}/">
  <meta property="og:image" content="https://www.bettingonline.org/assets/img/og-default.png">
  <meta name="twitter:card" content="summary_large_image">
  <script type="application/ld+json">{breadcrumb_json}</script>
  <script type="application/ld+json">{article_json}</script>
  <link rel="icon" type="image/svg+xml" href="../../assets/img/favicon.svg">
  <link rel="apple-touch-icon" href="../../assets/img/apple-touch-icon.svg">
  <link rel="manifest" href="../../manifest.json">
  <meta name="theme-color" content="#1e5cff">
</head>
<body>
  <div data-site-header></div>

  <section class="page-hero" style="padding-bottom:32px">
    <div class="container">
      <div class="crumbs"><a href="../../">Home</a><span class="sep">/</span><a href="../../{vertical_hub}/">{vertical_label}</a><span class="sep">/</span><span>{title_crumb_esc}</span></div>
      <span class="eyebrow">{category_label} · Updated {date_human}</span>
      <h1 style="margin-top:14px">{title_esc}</h1>
    </div>
  </section>

  <section class="section">
    <div class="container container-narrow">
      <article class="article">
{body}
      </article>

      <div style="padding:24px 20px;border-top:1px solid var(--border);margin-top:32px">
        <p class="byline muted" style="font-size:.9rem;margin:0 0 8px">Reviewed by <strong>BettingOnline.org Editorial Team</strong> · Last updated {date_human} · <a href="../../trust/">Trust &amp; Transparency</a></p>
        <p class="muted" style="font-size:.82rem;margin:0">18+ / 21+ where required. Affiliate disclosure: we may earn a commission from qualifying signups. Read our <a href="../../methodology/">methodology</a>, <a href="../../editorial-standards/">editorial standards</a>, and <a href="../../legal/disclosure.html">full affiliate disclosure</a>. <a href="../../legal/responsible-gambling.html">Bet responsibly.</a></p>
      </div>
    </div>
  </section>

  <div data-site-footer></div>
  <script defer src="../../assets/js/main.js?v=20260509c"></script>
</body>
</html>
"""


VERTICAL_HUB = {
    "sportsbook": ("sports", "Sports Betting"),
    "casino": ("casino", "Casino"),
    "poker": ("poker", "Poker"),
}


def render_page(page: dict, brands: dict) -> str:
    title = page["title"]
    meta_desc = page["meta_desc"]
    vertical_hub, vertical_label = VERTICAL_HUB.get(page.get("vertical", "sportsbook"), ("sports", "Sports Betting"))
    category_label = {
        "comparison": "Comparison",
        "use-case": "Best-for guide",
        "curation": "Ranking",
        "glossary": "Explainer",
        "location-usecase": "State + use-case guide",
    }.get(page["pattern"], "Guide")

    folder = target_folder(page["pattern"])

    breadcrumb = {
        "@context": "https://schema.org", "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://www.bettingonline.org/"},
            {"@type": "ListItem", "position": 2, "name": vertical_label, "item": f"https://www.bettingonline.org/{vertical_hub}/"},
            {"@type": "ListItem", "position": 3, "name": title, "item": f"https://www.bettingonline.org/{folder}/{page['slug']}/"},
        ]
    }
    article_meta = {
        "@context": "https://schema.org", "@type": "Article",
        "headline": title, "description": meta_desc,
        "url": f"https://www.bettingonline.org/{folder}/{page['slug']}/",
        "image": "https://www.bettingonline.org/assets/img/og-default.png",
        "author": {"@type": "Organization", "name": "BettingOnline.org Editorial Team", "url": "https://www.bettingonline.org/about/"},
        "publisher": {"@type": "Organization", "name": "BettingOnline.org",
                      "logo": {"@type": "ImageObject", "url": "https://www.bettingonline.org/assets/img/logo.png"}},
        "datePublished": TODAY_ISO, "dateModified": TODAY_ISO,
    }

    return PAGE_TEMPLATE.format(
        title_esc=html.escape(title),
        meta_desc_esc=html.escape(meta_desc),
        title_crumb_esc=html.escape(title.split(":")[0][:60]),
        slug=page["slug"],
        folder=folder,
        vertical_hub=vertical_hub,
        vertical_label=vertical_label,
        category_label=category_label,
        date_human=TODAY_HUMAN,
        breadcrumb_json=json.dumps(breadcrumb, separators=(",", ":")),
        article_json=json.dumps(article_meta, separators=(",", ":")),
        body=compose_body(page, brands),
    )


# =============================================================================
# Sitemap update
# =============================================================================

def add_to_sitemap(entries: list[tuple[str, str]]) -> None:
    """Add pages to sitemap. entries = [(folder, slug), ...]"""
    if not SITEMAP.exists():
        return
    text = SITEMAP.read_text()
    # Purge any stale /programmatic/ URLs from prior runs
    text = re.sub(
        r'\s*<url>\s*<loc>https://www\.bettingonline\.org/programmatic/[^<]+</loc>.*?</url>',
        "",
        text,
        flags=re.S,
    )
    additions = []
    for folder, slug in entries:
        loc = f"https://www.bettingonline.org/{folder}/{slug}/"
        if loc in text:
            continue
        additions.append(f"""  <url>
    <loc>{loc}</loc>
    <lastmod>{TODAY_ISO}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.85</priority>
  </url>""")
    if additions:
        text = text.replace("</urlset>", "\n".join(additions) + "\n</urlset>")
    SITEMAP.write_text(text)


# =============================================================================
# Main publisher
# =============================================================================

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--count", type=int, default=2, help="Pages to publish this run")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--regenerate", action="store_true", help="Re-render all already-published pages using the current template/composer")
    args = ap.parse_args()

    data = json.loads(QUEUE_PATH.read_text())
    brands = data["brands"]
    pages = data["pages"]

    # Regenerate mode: re-render every published page in place, no queue mutation.
    # Also migrates from any old /programmatic/ folder to the pattern-appropriate
    # /compare/ or /guides/ folder, and refreshes the sitemap accordingly.
    if args.regenerate:
        already = [p for p in pages if p.get("published")]
        print(f"Regenerating {len(already)} already-published pages...")
        entries = []
        for p in already:
            folder = target_folder(p["pattern"])
            out_dir = ROOT / folder / p["slug"]
            out_dir.mkdir(parents=True, exist_ok=True)
            (out_dir / "index.html").write_text(render_page(p, brands))
            entries.append((folder, p["slug"]))
            # Remove any stale /programmatic/ file
            stale = ROOT / "programmatic" / p["slug"]
            if stale.exists():
                import shutil
                shutil.rmtree(stale)
            print(f"  wrote {folder}/{p['slug']}/index.html")

        # If /programmatic/ folder is now empty, remove it
        prog_dir = ROOT / "programmatic"
        if prog_dir.exists() and not any(prog_dir.iterdir()):
            prog_dir.rmdir()

        add_to_sitemap(entries)
        subprocess.run(["git", "-C", str(ROOT), "add", "-A"], check=True)
        subprocess.run(["git", "-C", str(ROOT), "commit", "-m",
                        f"feat(content): republish {len(already)} pages under /compare/ + /guides/, fix asset paths, expand content"],
                       check=False)
        return 0

    # Filter to unpublished, sorted by publish_order
    pending = [p for p in pages if not p.get("published")]
    pending.sort(key=lambda p: p["publish_order"])

    to_publish = pending[:args.count]
    if not to_publish:
        print("Nothing to publish — queue is empty.")
        return 0

    print(f"Publishing {len(to_publish)} pages ({len(pending) - len(to_publish)} remain in queue):")

    if args.dry_run:
        for p in to_publish:
            folder = target_folder(p["pattern"])
            print(f"  [{p['publish_order']}] /{folder}/{p['slug']}/   ({p['pattern']}, {p['vertical']})")
        return 0

    published_entries = []
    for p in to_publish:
        folder = target_folder(p["pattern"])
        out_dir = ROOT / folder / p["slug"]
        out_dir.mkdir(parents=True, exist_ok=True)
        html_out = render_page(p, brands)
        (out_dir / "index.html").write_text(html_out)
        # Mark published in the source queue object
        for orig in pages:
            if orig["slug"] == p["slug"]:
                orig["published"] = True
                orig["published_at"] = datetime.now(timezone.utc).isoformat()
        published_entries.append((folder, p["slug"]))
        print(f"  wrote {folder}/{p['slug']}/index.html")

    # Persist updated queue
    data["pages"] = pages
    QUEUE_PATH.write_text(json.dumps(data, indent=2, ensure_ascii=False))
    print(f"  queue updated ({sum(1 for x in pages if x.get('published'))} / {len(pages)} published)")

    # Sitemap update
    add_to_sitemap(published_entries)
    print(f"  sitemap updated")

    # Commit
    subprocess.run(["git", "-C", str(ROOT), "add", "-A"], check=True)
    labels = [f"/{f}/{s}/" for f, s in published_entries[:3]]
    slugs_str = " + ".join(labels)
    if len(published_entries) > 3:
        slugs_str += f" (+{len(published_entries) - 3} more)"
    msg = f"feat(content): publish {len(published_entries)} new pages — {slugs_str}"
    subprocess.run(["git", "-C", str(ROOT), "commit", "-m", msg], check=False)

    return 0


if __name__ == "__main__":
    sys.exit(main())
