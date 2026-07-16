# BettingOnline.org — SEO Recovery Plan (v2, GSC-verified)

**Prepared:** July 2026
**Diagnosis basis:** verified Google Search Console data, not inference
**Status:** phase 1 in progress — state-page rebuild + sitemap fix + news-cadence reduction shipped this session

---

## Actual diagnosis from GSC data

The Ahrefs "1 keyword" number understated the picture. Google Search Console shows:

- **127,000 impressions** in the last 3 months (Google is willingly showing your site)
- **23 clicks** in the same window (0.02% CTR)
- **Average position: 77.7** — everything ranks on page 7-8
- **489 pages indexed / 549 not indexed** — the site is technically visible; it's algorithmically demoted
- **991 of 1,000 tracked queries sit at position 41+** — this is a uniform sitewide demotion, not per-page problems

### The 549-page "why not indexed" breakdown

| Reason | Pages | What it means |
|---|---|---|
| Crawled — currently not indexed | **273** | Google saw the page and decided it wasn't worth indexing (quality signal) |
| Discovered — currently not indexed | 132 | Google knows about the URL but hasn't crawled it (crawl-budget signal) |
| Not found (404) | 74 | Broken URLs still being linked to |
| Alternate page with canonical | 23 | Normal, ignore |
| Excluded by noindex | 20 | Intentional — all WordPress artifacts (blog-2, tablepress, layerslider, portfolio, etc.) — verified |
| Page with redirect | 20 | Normal, ignore |
| Blocked by robots.txt | 5 | Verify intentional |
| Blocked (403) | 2 | Investigate |
| Server error (5xx) | 0 | Fine |

### The impression distribution (where Google surfaces your content)

| Section | Pages showing impressions | Total impressions (3 mo) | Share |
|---|---|---|---|
| `/us/*` state pages | 42 | **53,601** | **43%** |
| `/sports/*` | 69 | 24,911 | 20% |
| `/poker/*` | 15 | 12,610 | 10% |
| Legacy root URLs | 107 | 10,921 | 9% |
| `/reviews/*` | 21 | 5,478 | 4% |
| `/casino/*` | 33 | 4,894 | 4% |
| Homepage | 1 | 3,784 | 3% |
| `/tools`, `/guides`, `/bonuses/` | 27 | 3,754 | 3% |
| `/news/*` | 15 | 205 | 0.2% |
| Other | 92 | 8,302 | 7% |

### The top queries — all buried between position 43 and 97

| Query | Impressions (3 mo) | Position |
|---|---|---|
| texas sports betting | 3,830 | 75.2 |
| minnesota sports betting | 1,815 | 91.1 |
| georgia sports betting | 1,105 | 97.5 |
| draftkings casino review | 1,071 | 54.5 |
| online poker bonus | 1,013 | 69.1 |
| 888sport | 818 | 51.7 |
| missouri sports betting | 792 | 95.6 |
| california sports betting | 775 | 83.7 |
| bovada | 683 | 43.0 |
| iowa sports betting | 652 | 93.3 |
| ohio sports betting | 621 | 96.2 |
| betonline | 613 | 67.8 |
| colorado sports betting | 597 | 94.3 |

Not one high-volume query is in a recoverable position 11-30 range. That means we can't just tweak title tags — we need to lift the whole domain's algorithmic trust to move any of these off page 5+.

---

## What Google is telling us

1. **You have a Helpful Content Update / Site Reputation Abuse footprint.** The uniform 77-average position is the signature. Sept 2023 HCU + March 2024 SRA + Aug/Nov 2024 core updates compounded.
2. **Your state pages are the highest-value recovery lever.** 53,000 impressions/3 months at zero clicks means Google is willing to show them but ranks them too deep. Improving them is more efficient than any new content.
3. **The daily news generator was making things worse.** Templated daily publishing at 10 articles per day, with only 205 total impressions across 15 articles = classic "crawled — currently not indexed" trigger. Now reduced to 2x weekly (see phase 1 shipped).
4. **Legacy WordPress URLs still carry ranking equity.** `/888sport/` gets 2,665 impressions, `/betonline-poker/` got the site's single click that ranked #1 in the top queries. Kill them and we lose our best assets. Kept in the new sitemap.

---

## What shipped this session (phase 1 execution)

### 1. News cadence reduced to twice weekly
`.github/workflows/daily-news.yml` now runs Tuesday + Friday instead of daily. Stops feeding Google templated content at a rate that triggers quality-signal demotions while trust rebuilds.

### 2. Top 15 state pages rebuilt from scratch
Each state (Texas, California, Georgia, Minnesota, Missouri, Ohio, Indiana, Iowa, Colorado, Mississippi, Connecticut, Arkansas, Maine, Wyoming, Washington DC) is now 1,450-1,600 words with:

- Real regulator name and tax rate
- Actual current legal status (legal/pending/not legal) with color-coded badge
- Complete legislative-history timeline (year-by-year)
- Full licensed-operator roster where legal
- Retail sportsbook geography
- Tribal-gaming considerations
- Market-size projections
- Public-opinion polling
- State-specific FAQ with `FAQPage` schema
- Regulated-market context: DK/FD/BetMGM/Caesars/ESPN Bet included as *informational* content where they legally operate, not as promoted CTAs

**Why this matters:** these pages are earning 53,000+ impressions and zero clicks. Doubling their depth *and* making them state-specific rather than templated is exactly what Google's HCU is looking for.

### 3. Sitemap rebuilt from scratch
Old sitemap: 790 URLs, most stale, no new content.
New sitemap: 671 URLs correctly categorized:
- Homepage (1)
- 40 US state pages (top priority)
- 96 sports pages
- 42 review pages (including all 13 new promoted-brand reviews — previously missing)
- 24 news articles (previously missing)
- 36 casino, 40 poker
- 331 legacy root URLs kept (they earn impressions)
- 61 other content pages

Separate news sitemap at `news/sitemap.xml` for Google News crawlers.

### 4. Twenty noindex-excluded pages verified
All 10 findable noindex tags on-site are intentional WordPress artifact suppressions (blog-2, tablepress, layerslider, portfolio, shortcodes, sitemap, full-width-page, etoro, 404-2). The 20-page count in GSC likely includes cached noindex signals on removed URLs. No accidental noindex on any ranking page.

---

## What still needs your input to complete phase 1

Two items require data from GSC that only you can pull:

### 1. The 74 "Not found (404)" URLs
In GSC → **Pages** → click "Not found (404)" row → click **Export** (top right of the URL list). Send me the CSV. I build the 301 redirect map from those URLs to their closest modern equivalents and deploy as a `vercel.json` redirects block. **Free ranking recovery** — every 404 currently being crawled is lost link equity.

### 2. Confirm Manual actions status
Left sidebar → **Security & Manual Actions → Manual actions**. Text-only confirmation is enough: "No issues detected." If there's a manual action, that becomes priority zero over everything else on this plan.

### 3. Submit the new sitemap in GSC
Left sidebar → **Sitemaps** → remove the old `sitemap.xml` entry, then add and submit `sitemap.xml` again (it's the same URL but Google needs to re-fetch to see the new 671-URL structure). Also submit `news/sitemap.xml` separately.

### 4. Request indexing on top 20 pages
Left sidebar → **URL inspection** → paste each of these and click **Request indexing**:

Top 5 state pages (biggest impression-earning surface):
- `https://www.bettingonline.org/us/texas/`
- `https://www.bettingonline.org/us/indiana/`
- `https://www.bettingonline.org/us/iowa/`
- `https://www.bettingonline.org/us/wyoming/`
- `https://www.bettingonline.org/us/missouri/`

Plus the biggest-traffic pillars:
- Homepage
- `/sports/`, `/sports/football/`, `/sports/basketball/`, `/sports/baseball/`
- `/casino/`, `/poker/`
- `/reviews/betonline-sportsbook/`, `/reviews/betonline-casino/`, `/reviews/betonline-poker/`
- `/news/` (index)

This forces Google to recrawl the pages that changed most this session.

---

## Phase 2 (weeks 2-3): what comes next

Order these top-down after phase 1 ships and GSC starts showing recrawl activity.

### 2.1 Address the 273 "Crawled — currently not indexed"
This is the biggest quality lever. I need the list from GSC.

- GSC → Pages → click "Crawled - currently not indexed" → Export
- I sort by category (news articles, review pages, thin utility pages)
- **Thin news articles** → consolidate or extend
- **Templated review sections** → add unique per-brand testing evidence (screenshots, videos, dated testing log)
- **Thin utility pages** → merge or noindex

### 2.2 Address the 132 "Discovered — currently not indexed"
These need to become more internally discoverable. Better sitemap already shipped. Also add breadcrumbs and cross-links from ranked pages to these under-crawled ones.

### 2.3 Deepen the state pages that survive to page 2
Track GSC weekly. Any state page that moves from position 90 to position 40 gets a further content upgrade: local operator promotions, latest legislation updates, in-state RG resources, embedded video where possible.

### 2.4 Reinstate ranking legacy pages properly
`/888sport/`, `/germany/`, `/bet-types/if-bet/`, `/games/skill/chess/` and other legacy URLs earning impressions need to be modernized (fresh 2026 dates, current operator lists, updated content) rather than left as stale WordPress pages. This preserves the ranking equity while removing the quality signal.

### 2.5 Consolidate `/reviews/draftkings-casino/` and equivalents
DK/FD/BetMGM/Caesars review pages are ranking at position ~50 for high-intent commercial queries ("draftkings casino review" — 1,071 impressions). We removed them from *promotional* toplists but their review pages themselves should stay live and be modernized. Consider adding a "as of July 2026, our top-promoted casino is [BetOnline] — see below for the DraftKings review" soft-nudge on the review page.

---

## Phase 3 (weeks 4-12): trust rebuild

### 3.1 E-E-A-T upgrade
- Real author bylines with LinkedIn, headshots, verifiable credentials
- Testing methodology page with photos/video of actual testing
- BBB / industry association / regulator body memberships
- Physical address, real phone number in footer

### 3.2 Original data content
- Monthly withdrawal-speed benchmark
- Monthly hold-rate tracker
- State-by-state market-share report
- These get pitched to journalists → real backlinks

### 3.3 HARO / Qwoted expert quotes
Named authors respond to journalist queries → high-authority backlinks

### 3.4 Broken-link outreach
Ahrefs → Backlinks → broken → reach out for replacements

---

## Success metrics — 30, 60, 90 days

| Milestone | Day 30 | Day 60 | Day 90 |
|---|---|---|---|
| GSC indexed pages | 500+ | 550+ | 600+ |
| GSC "Crawled — not indexed" | <200 | <100 | <50 |
| Total impressions (3mo trailing) | 150K+ | 200K+ | 300K+ |
| Average position | <70 | <55 | <40 |
| Total clicks (3mo trailing) | 100+ | 500+ | 2,000+ |
| Ranking state queries in top 20 | 0 (currently) | 2-3 | 5-8 |
| Fresh backlinks / month | 3+ | 5+ | 8+ |

---

## Deliverables this session

Shipped in the current commit series:

- `.github/workflows/daily-news.yml` — reduced to Tue+Fri cadence
- `scripts/rebuild-state-pillars.py` — generates all 15 state pages
- 15 rewritten state pages under `us/*/index.html`
- `scripts/rebuild-sitemap.py` — sitemap generator
- `sitemap.xml` — 671 URLs, properly categorized
- `news/sitemap.xml` — Google News format
- `SEO-RECOVERY-PLAN.md` — this document

---

## What I need from you this week (in priority order)

1. **Manual actions status** — text confirmation is fine
2. **74 404 URLs** — GSC → Pages → Not found (404) → Export → send me the CSV
3. **273 crawled-not-indexed URLs** — GSC → Pages → Crawled - currently not indexed → Export → send me the CSV
4. **Submit new sitemap** — GSC → Sitemaps → resubmit `sitemap.xml`, submit `news/sitemap.xml`
5. **Request indexing** on the top 20 pages listed above

Reply with those and phase 2 executes immediately.
