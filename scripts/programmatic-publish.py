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
PROG_DIR = ROOT / "programmatic"
SITEMAP = ROOT / "sitemap.xml"
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

def compose_body(page: dict, brands: dict) -> str:
    """Given a page config, produce the full <article> body HTML."""
    pat = page["pattern"]
    d = page["unique_data"]

    intro = f"<p>{html.escape(page.get('who_this_is_for', 'This guide walks through the practical decision framework.'))}</p>"

    # Insert the CTA toplist near the top (after 1st substantive section)
    cta_top = render_cta_toplist(page, brands, "top")

    # Internal links block near the end
    ilinks = page.get("internal_links", [])
    internal_html = ""
    if ilinks:
        items = "".join(f'<li><a href="{u}">{html.escape(u.split("/")[-2] if u.endswith("/") else u.split("/")[-1] or "Home")}</a></li>' for u in ilinks)
        internal_html = f"<h2>Related resources</h2><ul>{items}</ul>"

    # External sources block
    elinks = page.get("external_links", [])
    external_html = ""
    if elinks:
        items = "".join(f'<li><a href="{u}" rel="noopener nofollow" target="_blank">{html.escape(u)}</a></li>' for u in elinks)
        external_html = f"<h2>External references</h2><ul>{items}</ul>"

    # ---- Pattern-specific body ----
    if pat == "comparison":
        sc = d.get("scorecard", [])
        # First 2 rows tell us the two brand names typically
        title = page["title"]
        # Parse title to extract two names
        m = re.match(r"([^v]+?) vs ([^:2\d]+)", title)
        a_name = m.group(1).strip() if m else "Brand A"
        b_name = m.group(2).strip() if m else "Brand B"
        body = f"""
{intro}

<h2>The 30-second answer</h2>
<p>{html.escape(d.get('verdict', ''))}</p>

{cta_top}

<h2>Head-to-head scorecard</h2>
{render_scorecard_table(sc, a_name, b_name)}

<h2>Who wins for your use case</h2>
{render_ranked_list(d.get('winner_by_use_case', []))}

<h2>The verdict</h2>
<p>{html.escape(d.get('verdict', ''))}</p>

{internal_html}
{external_html}
"""

    elif pat == "use-case":
        body = f"""
{intro}

<h2>What we scored on</h2>
<ul>{"".join(f"<li>{html.escape(x)}</li>" for x in d.get('scoring_dimensions', []))}</ul>

{cta_top}

<h2>Ranked operators for this use case</h2>
{render_ranked_list(d.get('ranked_operators', []))}
"""
        if d.get("worked_example"):
            body += render_worked_example(d["worked_example"])
        if d.get("unique_insight"):
            body += f"\n<h2>What most bettors miss</h2>\n<p>{html.escape(d['unique_insight'])}</p>\n"

        body += f"\n{internal_html}\n{external_html}\n"

    elif pat == "curation":
        body = f"""
{intro}

<h2>How we ranked</h2>
<ul>{"".join(f"<li>{html.escape(x)}</li>" for x in d.get('scoring_dimensions', []))}</ul>

{cta_top}

<h2>The ranking</h2>
{render_ranked_list(d.get('ranked_operators', []) or d.get('top_slots', []))}
"""
        if d.get("unique_insight"):
            body += f"\n<h2>What the data shows</h2>\n<p>{html.escape(d['unique_insight'])}</p>\n"
        if d.get("what_changed"):
            body += f"\n<h2>What changed since last update</h2>\n<p>{html.escape(d['what_changed'])}</p>\n"
        body += f"\n{internal_html}\n{external_html}\n"

    elif pat == "glossary":
        body = f"""
{intro}

<h2>Definition</h2>
<p>{html.escape(d.get('definition', ''))}</p>
"""
        if d.get("worked_example"):
            body += render_worked_example(d["worked_example"])

        if d.get("typical_rates"):
            rows = "".join(f"<tr><td><strong>{html.escape(k)}</strong></td><td>{html.escape(v)}</td></tr>" for k, v in d["typical_rates"].items())
            body += f"\n<h2>Typical rates in the wild</h2>\n<table>{rows}</table>\n"

        if d.get("why_it_matters"):
            body += f"\n<h2>Why this matters</h2>\n<p>{html.escape(d['why_it_matters'])}</p>\n"

        for k in ("how_to_actually_use_it", "how_tiers_work", "how_to_maximize",
                  "when_to_use_moneyline", "when_to_use_spreads",
                  "nfl_key_numbers", "why_it_gets_hard_at_scale", "practical_verdict"):
            if d.get(k):
                heading = k.replace("_", " ").capitalize()
                body += f"\n<h2>{html.escape(heading)}</h2>\n<p>{html.escape(d[k])}</p>\n"

        body += f"\n{cta_top}\n{internal_html}\n{external_html}\n"

    elif pat == "location-usecase":
        body = f"""
{intro}

<h2>State context</h2>
<p>{html.escape(d.get('state_context', ''))}</p>

{cta_top}

<h2>Ranked for this use case</h2>
{render_ranked_list(d.get('ranked_for_nfl', []) or d.get('ranked_for_nba', []) or d.get('ranked_for_mlb', []) or d.get('ranked_for_parlays', []) or d.get('ranked_for_cfb', []) or d.get('ranked_for_props', []) or d.get('ranked_for_nj', []))}
"""
        if d.get("offshore_alternative"):
            body += f"\n<h2>Offshore alternative context</h2>\n<p>{html.escape(d['offshore_alternative'])}</p>\n"

        body += f"\n{internal_html}\n{external_html}\n"

    else:
        body = f"{intro}\n{cta_top}\n{internal_html}\n"

    return body


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
  <link rel="stylesheet" href="../assets/css/main.min.css?v=20260509c">
  <link rel="canonical" href="https://www.bettingonline.org/programmatic/{slug}/">
  <meta property="og:type" content="article">
  <meta property="og:site_name" content="BettingOnline.org">
  <meta property="og:title" content="{title_esc}">
  <meta property="og:description" content="{meta_desc_esc}">
  <meta property="og:url" content="https://www.bettingonline.org/programmatic/{slug}/">
  <meta property="og:image" content="https://www.bettingonline.org/assets/img/og-default.png">
  <meta name="twitter:card" content="summary_large_image">
  <script type="application/ld+json">{breadcrumb_json}</script>
  <script type="application/ld+json">{article_json}</script>
  <link rel="icon" type="image/svg+xml" href="../assets/img/favicon.svg">
  <link rel="apple-touch-icon" href="../assets/img/apple-touch-icon.svg">
  <link rel="manifest" href="../manifest.json">
  <meta name="theme-color" content="#1e5cff">
</head>
<body>
  <div data-site-header></div>

  <section class="page-hero" style="padding-bottom:32px">
    <div class="container">
      <div class="crumbs"><a href="../">Home</a><span class="sep">/</span><a href="../{vertical_hub}/">{vertical_label}</a><span class="sep">/</span><span>{title_crumb_esc}</span></div>
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
        <p class="byline muted" style="font-size:.9rem;margin:0 0 8px">Reviewed by <strong>BettingOnline.org Editorial Team</strong> · Last updated {date_human} · <a href="../trust/">Trust &amp; Transparency</a></p>
        <p class="muted" style="font-size:.82rem;margin:0">18+ / 21+ where required. Affiliate disclosure: we may earn a commission from qualifying signups. Read our <a href="../methodology/">methodology</a>, <a href="../editorial-standards/">editorial standards</a>, and <a href="../legal/disclosure.html">full affiliate disclosure</a>. <a href="../legal/responsible-gambling.html">Bet responsibly.</a></p>
      </div>
    </div>
  </section>

  <div data-site-footer></div>
  <script defer src="../assets/js/main.js?v=20260509c"></script>
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

    breadcrumb = {
        "@context": "https://schema.org", "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://www.bettingonline.org/"},
            {"@type": "ListItem", "position": 2, "name": vertical_label, "item": f"https://www.bettingonline.org/{vertical_hub}/"},
            {"@type": "ListItem", "position": 3, "name": title, "item": f"https://www.bettingonline.org/programmatic/{page['slug']}/"},
        ]
    }
    article_meta = {
        "@context": "https://schema.org", "@type": "Article",
        "headline": title, "description": meta_desc,
        "url": f"https://www.bettingonline.org/programmatic/{page['slug']}/",
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

def add_to_sitemap(slugs: list[str]) -> None:
    if not SITEMAP.exists():
        return
    text = SITEMAP.read_text()
    additions = []
    for slug in slugs:
        loc = f"https://www.bettingonline.org/programmatic/{slug}/"
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
    args = ap.parse_args()

    data = json.loads(QUEUE_PATH.read_text())
    brands = data["brands"]
    pages = data["pages"]

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
            print(f"  [{p['publish_order']}] {p['slug']}  ({p['pattern']}, {p['vertical']})")
        return 0

    PROG_DIR.mkdir(exist_ok=True)
    published_slugs = []
    for p in to_publish:
        out_dir = PROG_DIR / p["slug"]
        out_dir.mkdir(exist_ok=True)
        html_out = render_page(p, brands)
        (out_dir / "index.html").write_text(html_out)
        # Mark published in the source queue object
        for orig in pages:
            if orig["slug"] == p["slug"]:
                orig["published"] = True
                orig["published_at"] = datetime.now(timezone.utc).isoformat()
        published_slugs.append(p["slug"])
        print(f"  wrote programmatic/{p['slug']}/index.html")

    # Persist updated queue
    data["pages"] = pages
    QUEUE_PATH.write_text(json.dumps(data, indent=2, ensure_ascii=False))
    print(f"  queue updated ({sum(1 for x in pages if x.get('published'))} / {len(pages)} published)")

    # Sitemap update
    add_to_sitemap(published_slugs)
    print(f"  sitemap updated")

    # Commit
    subprocess.run(["git", "-C", str(ROOT), "add", "-A"], check=True)
    slugs_str = " + ".join(published_slugs[:3])
    if len(published_slugs) > 3:
        slugs_str += f" (+{len(published_slugs) - 3} more)"
    msg = f"feat(programmatic): publish {len(published_slugs)} pages — {slugs_str}"
    subprocess.run(["git", "-C", str(ROOT), "commit", "-m", msg], check=False)

    return 0


if __name__ == "__main__":
    sys.exit(main())
