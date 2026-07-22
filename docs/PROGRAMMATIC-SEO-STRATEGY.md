# Programmatic SEO Strategy for BettingOnline.org

**Based on:** "How we generate millions of organic clicks with programmatic SEO in 2026"
**Adapted for:** sports betting / casino / poker affiliate publishing
**Target output:** 50 pages, 2 published per day for 25 days

---

## What the source doc actually says (short version)

The doc argues that instead of writing one 2,000-word blog per keyword, you spot the *repeatable structure* behind a keyword family and build one template that produces every variation. Zapier does this to 800,000 pages, 1.3M keywords, 16.2M monthly organic visitors. It maps out 12 pattern types:

1. **Curation** — best [category], top [tools]
2. **Comparisons** — [x] vs [y]
3. **Use-case** — [product] for [audience]
4. **Integrations** — [tool] + [tool]
5. **Templates** — [type] template, free [type] generator
6. **Converters** — [x] to [y]
7. **Examples** — [type] examples
8. **Directories** — [category] tools
9. **Glossary** — what is [term]
10. **Localization** — translated versions
11. **Locations** — [service] in [location]
12. **Profiles** — [entity] + [attribute]

Then it emphasizes **layering** — combining two patterns compounds them into low-competition, high-intent queries: "notion vs coda for remote teams" beats either single-pattern query.

**The critical warning for 2026:**

> "Template-generated pages with only the variable swapped are getting penalised. QuickSEO's March 2026 analysis found template pages with only the variable swapped are LESS likely to be cited by AI engines than static content. Each programmatic page needs at least ONE genuinely unique data point."

That warning is the whole design constraint. The programmatic play works *only if* each page carries genuinely differentiated data — real pricing, real user counts, real testing results, real cited sources.

---

## How the 12 patterns map to bettingonline.org

Not every pattern makes sense for a betting affiliate. The applicable subset:

| Pattern | Fits us? | Why |
|---|---|---|
| **Curation** (best-of lists) | Strong fit | "Best sportsbook for NFL parlays" is a huge query family |
| **Comparisons** (vs pages) | Strongest fit | Highest commercial intent — "DK vs FanDuel" gets 15K searches/month |
| **Use-case** (best-for personas) | Strong fit | "Best sportsbook for high rollers" — persona-driven, converts |
| **Integrations** | No | Books don't "integrate" the way SaaS tools do |
| **Templates** | Partial fit | Free calculators (already have) |
| **Converters** | Partial fit | Odds converter (already have); can add more |
| **Examples** | No | Not applicable to betting |
| **Directories** | Weak fit | Directory-style pages read as low-trust in gambling |
| **Glossary** | Strong fit | "What is CLV" builds topical authority AND is Google-preferred format |
| **Localization** | Later | US-only makes sense for now |
| **Locations** | Strong fit | State/city pages are core traffic drivers |
| **Profiles** | Weak fit | Operator profile pages exist as reviews already |

**Best patterns for our vertical:** Curation, Comparisons, Use-case, Glossary, Locations (layered).

**Layering strategy applied to us:**

- Locations + Use-case: "Best sportsbook for NFL parlays in New Jersey"
- Comparison + Use-case: "DraftKings vs FanDuel for prop bettors"
- Curation + Locations: "Best crypto sportsbooks accepting Ohio residents"

Each combination narrows the query, reduces competition, and lifts intent quality.

---

## The 50-page architecture

We hit five buckets, weighted toward the highest-converting patterns:

- **12 comparison pages** (30%) — highest commercial intent
- **14 use-case pages** (28%) — persona-targeted, high conversion
- **10 curation pages** (20%) — best-of lists with layered filters
- **7 glossary pages** (14%) — topical authority + AI-engine citation surface
- **7 location+use-case layered pages** (14%) — low-competition, high-intent

Full list is in `data/programmatic-queue.json`.

---

## The anti-penalty guardrail: unique data per page

The doc's warning drives our page-schema design. Every page in the queue carries a `unique_data` payload that the generator injects into the page. Examples:

- **Comparison pages:** side-by-side scorecard with 8+ dimensions where the two operators produce genuinely different numbers (hold rates, cashier speeds, prop menu depth)
- **Use-case pages:** filter-scored ranked table showing which operators score best FOR that specific use case, with the scoring rationale visible
- **Curation pages:** ranked list with each operator's specific score, PLUS a "what changed since last update" freshness signal
- **Glossary pages:** worked math example with real numbers, plus real-world sample of the concept from a specific market
- **Location-layered pages:** state-specific data (tax rate, regulator, licensed operators, retail geography) merged with use-case-specific ranking rationale

Two pages sharing the same operator (say, BetOnline features in 15+ pages) will present genuinely different data on each. On a comparison page it's the head-to-head scorecard; on a use-case page it's a scoring rationale; on a curation page it's the ranking position and gap to #2; on a location page it's the local availability and terms.

---

## The lead-funnel design

Every page includes a topic-appropriate CTA block near the top and again after the main content. The CTA block is not the same on every page — it's picked by topic:

- **Sportsbook comparison / use-case pages:** promote BetOnline, Sportsbetting.ag, BetUS (our 3 promoted sportsbook brands)
- **Casino pages:** promote BetOnline Casino, Sportsbetting.ag Casino, BetUS Casino
- **Poker pages:** promote all 7 poker brands (Black Chip, ACR, Ya Poker, True Poker, BetOnline Poker, TigerGaming, Sportsbetting.ag Poker)
- **Mixed / glossary pages:** promote the brand most relevant to the concept discussed (e.g., a CLV article gets a sportsbook CTA)

All CTAs carry `rel="sponsored nofollow"`, `target="_blank"`, and `data-affiliate-brand="[slug]"` — same infrastructure as the sitewide toplists.

The funnel intent: page ranks for its target query → visitor reads the unique data → CTA is contextually the right offer → click through to tracked affiliate URL.

---

## The publication rhythm

Two pages per day, alternating pattern types where possible so we don't publish 12 comparison pages in a row and trigger a topic-cluster smell. GitHub Actions handles publication at 07:00 UTC daily (offset from the existing news bot at 06:00 to avoid collisions).

Full 50-page publication runs 25 days:
- Days 1-6: mix of comparisons + use-case + glossary
- Days 7-14: curation + comparisons + layered locations
- Days 15-25: remaining variety with new-page freshness ramping into the September NFL kickoff window

Each publication commit deploys via Vercel automatically. Each new page is added to `sitemap.xml` with fresh `lastmod`. Internal links from existing pillars are added on each publish so the new page is discoverable within the site graph immediately.

---

## Expected performance (calibrated realistic)

Zapier's numbers are the ceiling, not the floor. What's realistic for a site with DR 32, a recent algorithmic downgrade, and 25 days of publishing:

- **First 30 days after publishing:** 20-30% of pages indexed, average position 60-80 (typical new-page GSC treatment)
- **Days 30-60:** pages that survive Google's quality filter climb into position 30-50 range. First clicks arrive on longtail queries.
- **Days 60-90:** best-performing pages (comparison + use-case with strong unique data) reach positions 15-25 range. Meaningful clicks arrive.
- **90+ days:** the 10-15 best pages hit page 1 for their target queries. Cumulative impressions from the 50-page set easily 3-5x current sitewide impressions.

The key metric to watch is not per-page traffic but **cumulative impression growth**. Programmatic pages win by stacking — no single page needs to be a top-5 hit; the 50-page set collectively lifts the site's total surface area substantially.

---

## The risks (and how the guardrails address them)

**Risk 1: Templated content penalty.** The doc's own warning. **Guardrail:** unique data payload per page, real specific numbers, no lorem-ipsum-y filler.

**Risk 2: Over-optimization for CTAs.** Google demotes pages with CTA density above content density. **Guardrail:** CTA blocks are compact (one at top, one at bottom), the middle 1,500 words are educational content.

**Risk 3: Publishing during algorithmic recovery.** We're in the middle of a recovery from a Helpful Content Update hit. Publishing 50 more pages during that could re-trigger the signal. **Guardrail:** slow cadence (2/day, not 10/day), unique data per page, all promotional CTAs are earned by content depth.

**Risk 4: The offshore-only affiliate promotion.** We already know Google is stricter on unregulated gambling promotion. **Guardrail:** every page includes regulated-US-market context (DK/FD/BetMGM as informational reference where relevant), CTAs promote only what's contextually correct, no bait-and-switch.

---

## Success measurement

At day 30, we'll pull GSC data on:
- Percent of 50 pages indexed
- Average position on target queries
- Impressions from programmatic pages vs sitewide baseline

At day 60 and day 90, same measurements. The programmatic play is validated if:
- **80%+ of pages indexed** by day 30 (means the unique-data guardrail worked)
- **Average position <50** by day 60 (means Google views them as legitimate content)
- **Cumulative impressions from set >20K/month** by day 90 (means query capture is real)

If any of those benchmarks miss badly, we pause new publishing and diagnose which pages Google is rejecting.
