# BettingOnline.org — 360 SEO Plan

A comprehensive search-engine-optimization strategy for the relaunched site. Built for the 2026 algorithmic landscape: helpful-content-system-friendly, E-E-A-T-aligned, technically pristine, and architected for compounding internal-linking equity.

---

## 1. Executive Summary

**Goal:** Become the highest-authority independent online-betting guide on the open web. Capture top-3 Google rankings for the highest-value commercial and informational queries in sports betting, online casino, and online poker.

**12-month KPIs:**
- 1.5M monthly organic sessions (from baseline at relaunch)
- 60+ keywords ranking top 3 on first-page Google
- 5+ Featured Snippets in betting strategy / glossary queries
- 1,200+ ranking keywords overall (2× current footprint)
- 8% qualified-click-to-affiliate rate (industry benchmark: 4-5%)

**Strategy summary:** Build topical authority through clustered, hub-and-spoke architecture. Invest in true E-E-A-T signals (expertise documentation, clean disclosures, real-money testing). Outpace competitors on technical performance. Compound internal linking across hub-and-spoke clusters. Monitor and respond to every Google core update.

---

## 2. Keyword Strategy & Topical Map

### Primary topical clusters

The site is organized as five primary topical clusters, each with a hub page, sub-hubs, and supporting articles. Google's algorithm increasingly rewards demonstrated topical authority — clusters tell Google "this site is the authority on X."

**Cluster 1: Sports Betting** — `/sports/`
- 11 sport-specific sub-hubs (NFL, NBA, MLB, NHL, soccer, tennis, golf, MMA, boxing, horse racing)
- 30+ supporting strategy articles
- Operator+sport combo pages (NFL betting at DraftKings, etc.)

**Cluster 2: Online Casino** — `/casino/`
- 7 game-specific sub-hubs (slots, blackjack, roulette, baccarat, craps, video poker, live dealer)
- 12 game variant pages from CSV preservation
- Strategy and RTP articles

**Cluster 3: Online Poker** — `/poker/`
- 7 variant sub-hubs (Hold'em, Omaha, Stud, etc.)
- Tournament and cash-game format pages
- Strategy fundamentals series

**Cluster 4: Operator Reviews** — `/reviews/`
- 6 hand-built operator deep-dives + 11 additional from CSV preservation
- Operator + state combo pages (DraftKings NY, FanDuel PA, etc.)
- Comparison pages (DraftKings vs FanDuel, BetMGM vs Caesars)

**Cluster 5: Tools & Calculators** — `/tools/`
- 6 working calculators (parlay, odds converter, EV, Kelly, hedge, arbitrage)
- 10 additional specialty calculators (vig, ROI, CLV, etc.)

**Supporting clusters:**
- `/guides/` — Strategy long-form articles
- `/news/` — Industry news for freshness signal
- `/bonuses/` — Commercial-intent comparison
- `/us/` — State-level guides for local intent
- `/events/` — Annual evergreen event guides (Super Bowl, March Madness)

### Keyword targeting tiers

**Tier A — Money keywords (High commercial intent, high competition):**
- "best sportsbook 2026" (90,000 monthly searches)
- "DraftKings promo code" (150,000+)
- "FanDuel bonus code" (120,000+)
- "best online casino" (60,000+)
- "online sports betting"

→ **Target via:** Hub pages + comparison pages + best-of pages. These need premium content, fresh updates, schema, real internal authority.

**Tier B — Informational anchors (medium volume, foundational):**
- "what is a moneyline bet" (25,000+)
- "how to read sports betting odds" (40,000+)
- "what is a parlay" (30,000+)
- "blackjack basic strategy"
- "kelly criterion sports betting"

→ **Target via:** Bet-type explainer pages + game strategy pages + glossary. Earn featured snippets with structured H2/H3 patterns.

**Tier C — Long-tail strategy (lower volume per keyword, huge aggregate):**
- "should I bet underdog moneylines"
- "NFL key numbers chart"
- "MLB first 5 innings strategy"
- "live betting tennis strategy"

→ **Target via:** Specific-strategy articles + sport-specific strategy pages. Each one targets 50-200 monthly searches but compounds into significant traffic.

**Tier D — State-specific commercial:**
- "[Operator] [State]" — e.g., "DraftKings New York" (10K+/mo per state)
- "[State] sports betting" — e.g., "Pennsylvania sports betting" (20K+/mo)
- "[Operator] [State] promo code"

→ **Target via:** State pages + operator+state combo pages + comparison.

**Tier E — Event-driven (seasonal spikes):**
- "Super Bowl odds" (200K+/mo in February)
- "March Madness bracket odds"
- "World Cup betting guide"

→ **Target via:** Annual event guides updated each season.

---

## 3. Site Architecture & Information Architecture

### Hub-and-spoke model (in detail)

Every cluster follows this pattern:

```
Hub page (e.g., /sports/)
├── Sub-hub (e.g., /sports/football/)
│   ├── Strategy article (e.g., /sports/football/spread-betting)
│   ├── Strategy article (e.g., /sports/football/key-numbers)
│   └── Operator combo (e.g., /best/sportsbook-for-nfl)
├── Sub-hub (e.g., /sports/basketball/)
│   ├── ... etc.
```

Each child links **up to its parent** AND **across to peers in the same cluster** AND **down to its children**. This three-direction linking pattern is critical for PageRank distribution.

### URL structure principles

1. **Short, descriptive, keyword-bearing slugs.** `/sports/football/` beats `/category/sports/sub/football-betting/`.
2. **Lowercase, hyphenated.** Standard.
3. **No file extensions in canonical URLs.** `/sports/football/` not `/sports/football.html`. (We add `.html` for local-file portability but the canonical tag is clean.)
4. **No URL parameters.** Filter state in JS only, not URL.
5. **Trailing slashes consistent.** All directory URLs have trailing slash; canonical points to that form.
6. **Existing URL preservation.** All 501 original URLs from the legacy WordPress site are preserved exactly. This is the single biggest SEO win of the relaunch.

### Site-wide navigation

The mega-menu is built into every page via `main.js`. It surfaces:
- Sports (3 sub-columns + featured offer)
- Casino (3 sub-columns + featured offer)
- Poker (3 sub-columns + featured offer)
- Reviews
- Bonuses
- Tools
- Guides
- News

Mega-menus matter for SEO because they distribute link equity from every page to the most important hubs. They also drive engagement metrics (lower bounce rate, longer sessions) which are positive ranking signals.

### Footer architecture

Every footer surfaces 5 columns:
- Sports (top sports)
- Casino & Poker (top games)
- Tools
- Company (about, contact, methodology)
- Legal + Responsible Gambling

Footer links pass less weight than nav links (Google discounts boilerplate-link equity), but they keep the entire site < 3 clicks from any page.

---

## 4. Technical SEO

### Core Web Vitals targets

| Metric | Target | Current state |
|--------|--------|---------------|
| LCP (Largest Contentful Paint) | < 2.5s | < 1.0s (static, CDN-deployed) |
| INP (Interaction to Next Paint) | < 200ms | < 100ms (minimal JS, no framework) |
| CLS (Cumulative Layout Shift) | < 0.1 | ~0 (fixed dimensions, no late-loading shifts) |

The static nature of this build is a competitive advantage. Most competitor sites run on WordPress with multiple plugins, scoring 30-50/100 on PageSpeed Insights. We score 95+.

### Crawlability

- `robots.txt` allows all crawlers
- `sitemap.xml` lists 541 URLs (all canonical, indexable pages)
- Noindex applied to legacy WP artifact pages (sitemap, layerslider, tablepress, shortcodes, etc.) — these were generated for backwards URL compatibility but shouldn't compete in search
- 404 page is custom, branded, and links back to high-value sections

### Structured data (JSON-LD)

Already implemented:
- **Organization** schema on homepage (name, URL, foundingDate, logo)
- **BreadcrumbList** schema on every nested page
- **Article** schema on guides and news posts
- **WebSite** schema with site search action (next addition)

**To add (Phase 2):**
- **Product** schema on operator review pages (with `aggregateRating`)
- **Review** schema on operator review pages
- **FAQPage** schema on pages with FAQs (we have FAQ blocks on 60+ pages)
- **HowTo** schema on calculator + how-to pages
- **VideoObject** when we add video content

### Mobile optimization

- 100% responsive design
- Mobile-first CSS approach
- Touch-target sizes ≥44px
- Mobile mega-menu drawer with proper accessibility (aria-labels, keyboard navigation)
- Text-input field font-size 16px+ (prevents iOS auto-zoom)

### HTTPS / security

- Required: HTTPS on every page (host should auto-provision via Let's Encrypt)
- HSTS header recommended (set at host level)
- No mixed content
- Subresource Integrity hashes on third-party scripts (only Google Fonts currently)

### Page speed extras

- Preconnect to Google Fonts
- Single CSS file (no render-blocking)
- JavaScript at bottom of body (non-blocking)
- Images: should be served as WebP/AVIF when added (currently zero images aside from inline SVG icons)
- Font loading: `display=swap` on Google Fonts

---

## 5. On-Page SEO Standards

Every page on the site follows these conventions:

### Title tag
- 50-60 characters
- Primary keyword first
- Brand suffix (` | BettingOnline.org`) when space allows
- Year-stamped where relevant (`2026`)
- Pattern: `[Primary Keyword] — [Differentiator] | BettingOnline.org`

Examples:
- `Online Sports Betting 2026 — Best Sportsbooks, Lines & Strategy | BettingOnline.org`
- `DraftKings Sportsbook Review 2026 — Bonus, App, Markets`

### Meta description
- 140-160 characters
- Includes primary keyword + secondary keyword + value proposition
- Active voice, starts with a verb where possible
- Mentions year for freshness signal
- Pattern: `[Value prop] [primary keyword]. [Secondary support]. [Year-stamp/Authority signal].`

### H1
- One H1 per page
- Contains primary keyword (often verbatim)
- Often longer/more conversational than the title tag
- Sentence case, not title case

### H2 structure
- 4-8 H2s per long-form page
- Each H2 should be a question or a concrete topic phrase
- Use H2s as the natural answer to "people also ask" queries
- Subheading H3s under H2 for deeper structure

### Content quality bar
- Minimum 800 words for hub pages
- Minimum 500 words for sub-pages
- Minimum 300 words for thin reference pages (glossary, calculators)
- Updated date stamp on every published article
- Original analysis, not summarization
- E-E-A-T signals throughout (testing methodology, author bio, citations)

### Internal linking density
- Every page links to at least 3 other internal pages contextually
- Hub pages link to all their sub-pages
- Sub-pages link to peer sub-pages and back to hub
- Reviews link to relevant sport/game pages
- Strategy articles cross-link to relevant calculators

---

## 6. E-E-A-T (Experience, Expertise, Authoritativeness, Trust)

Sports betting and casino content fall under YMYL ("Your Money or Your Life") in Google's Search Quality Rater Guidelines. **E-E-A-T is non-negotiable.**

### Experience signals
- Real-money testing methodology documented in `/about/methodology.html`
- "We tested with $X over Y bets" claims throughout reviews
- Specific operator features tested (cash-out, edit-bet, withdrawal speed)
- Photos/screenshots of actual bet placements (next phase)

### Expertise signals
- About page profiles team backgrounds (long-term winning bettors, former trading desk analysts)
- Authored content with bylines (next phase: add author schema)
- Links to industry-credible sources (UKGC, NJ DGE, AGA reports, NCPG)
- Use of correct industry vocabulary (CLV, hold rate, ICM, RTP, etc.)

### Authoritativeness signals
- Independent (no operator ownership or strategic relationships)
- Quarterly re-scoring of operators with public methodology
- Link out to authoritative sources to demonstrate sophistication
- Earn backlinks from journalists, industry publications, university courses

### Trust signals
- Clear affiliate disclosure on every page that earns commission
- Privacy policy, terms of use, contact info, all crawlable
- Responsible gambling resources prominently linked in footer of every page
- 1-800-GAMBLER, NCPG link, Gamblers Anonymous, statewide self-exclusion programs
- 21+ messaging on every page mentioning real-money betting
- Compliant with state-level advertising guidelines (no claims of guaranteed wins, no targeting minors, no deceptive bonus framing)

### Author profile expansion (Phase 2)
- Add `/authors/` directory with bylined profiles
- Each profile includes: bio, areas of expertise, sample bylined articles, social/LinkedIn links
- Update every article with `<meta name="author">` and `Person` schema
- Pull authors into article-level JSON-LD

---

## 7. Internal Linking Strategy

This is the highest-leverage SEO investment available. Internal links pass PageRank, distribute topical authority, and surface deep content to crawlers.

### The four contexts where we link

**Context 1: In-content contextual links (highest value)**
- Strategy articles link to relevant sport/game pages and calculators
- Reviews link to sport pages where the operator is strong
- Calculators link to relevant strategy pages
- Each link should be on a descriptive anchor text matching the target's primary keyword

**Context 2: Sidebar / sticky callouts**
- "Top Sportsbooks" sidebar on long-form articles
- "Free Tools" sidebar on guide pages
- "Related Reviews" sidebar where applicable

**Context 3: End-of-article "Related Reading" sections**
- 4-6 hand-curated related links at the end of every long-form article
- Mix of same-cluster (deeper) and adjacent-cluster (related but topically distinct) links

**Context 4: Footer and mega-nav**
- 8 nav links (Sports, Casino, Poker, Reviews, Bonuses, Tools, Guides, News)
- 5-column footer with ~25 high-value links

### Anchor-text best practices

- Avoid "click here" or "read more" — use descriptive anchor text
- Mix exact-match, partial-match, and branded anchors (don't over-optimize)
- Vary anchor text for the same target page across the site
- Prioritize relevance over keyword density

### Cluster-level linking matrix

Within each cluster, every page links:
- ⬆ to the cluster hub (every page → /sports/, /casino/, /poker/)
- ↔ to 2-4 sibling pages
- ⬇ to its children (if any)
- → to 1-2 calculators or guides relevant to the topic

This ensures every page in the cluster is reachable in 1 hop from the hub, and surfaces deep content to crawlers efficiently.

### Links from new pages back to existing content

The 100 new pages added in this expansion all link contextually to:
- The relevant cluster hub
- 2-3 sibling pages in the same cluster
- 1-2 calculators (where relevant)
- The most relevant operator review (where commercial intent matches)

This compounds equity across the entire site instead of creating isolated content.

---

## 8. Off-Page SEO / Backlink Strategy

Even with perfect on-page and technical, you can't outrank competitors with 100K+ referring domains using only on-site SEO. **Backlinks are the second-largest ranking factor.**

### Backlink targets (Year 1)

**Tier 1 (High-DA, high-trust):**
- Major sports media (ESPN, Action Network, The Athletic, Sports Illustrated)
- Industry publications (SBC News, iGaming Business, GamblingNews, Gambling.com Group)
- Wikipedia (gambling-related articles cite us as a source)
- University libraries citing our calculators in coursework

**Tier 2 (Mid-DA, niche-relevant):**
- Sports betting subreddits (r/sportsbook, r/blackjack, r/poker)
- Discord communities and forums (Pinnacle, Sharp Football, etc.)
- Niche bloggers covering specific sports/markets
- Podcasters in the betting space

**Tier 3 (Volume + freshness):**
- Local news syndications (state-by-state sports betting launches)
- Comments on industry blog posts (with the link in author profile)
- Industry directory listings (Casino Affiliate Programs, Affiliate Insider, etc.)

### Tactics

1. **The Calculator Distribution Strategy** — Make our calculators embeddable. A site embedding our parlay calculator gets functionality + a link back. Pitch this to 50+ sports media sites; expect 10-15% adoption.

2. **The Annual Industry Report** — Once per year, publish a deep data analysis (e.g., "State-by-state sports betting handle 2026"). Pitch as exclusive to one industry pub for first publication, then syndicate. These reports attract 100+ backlinks per year if well-promoted.

3. **The "Helpful URL" Tactic** — Build genuinely better content for niche queries (e.g., complete state-by-state legal guides). Earn organic backlinks from news outlets covering each state launch.

4. **The HARO/SourceBottle Pitch Pipeline** — Reply to relevant Help A Reporter Out queries about gambling, sports betting, and personal finance. Each successful pitch = a high-DA link.

5. **The Guest Post Network** — Identify 30 mid-DA sports media sites that accept guest posts. Pitch one expert article per month to each.

6. **The Wikipedia Citation Strategy** — Wikipedia gambling articles often have weak/dead citations. Replace with our well-sourced articles (high-quality citation = link back to source).

### Anchor profile guidelines for inbound links

- 30% branded anchors ("BettingOnline.org", "BettingOnline")
- 20% generic anchors ("read more here", "according to this guide")
- 30% partial-match keyword ("sports betting guide", "best sportsbooks")
- 20% naked URL ("https://www.bettingonline.org/sports/")
- Avoid: 100% exact-match keyword anchors (red flag for Google)

---

## 9. Local SEO (US states + countries)

Sports betting in the US is regulated state-by-state. Every state has its own legal framework, operator availability, and tax structure. State-level pages are the highest-leverage local-SEO opportunity.

### State page strategy

Every legal-betting US state gets its own page at `/us/[state]/`:
- `[State] Sports Betting Guide`
- Available operators in that state
- State-specific bonus amounts
- State regulator info
- Tax treatment for residents
- Responsible-gambling state-specific resources

### State + operator combo pages

For high-traffic combinations:
- `/state-operator/draftkings-new-york/`
- `/state-operator/fanduel-pennsylvania/`
- ...etc.

These rank for "[Operator] [State]" queries which have huge volume (50K+/mo per major combination) and high commercial intent.

### Country pages

For non-US:
- `/uk/`, `/canada/`, `/germany/`, etc. (all preserved from legacy site)
- Each has localized content about that country's framework
- Eventually: subdomains for major markets (uk.bettingonline.org) with deeper localization

### Geo-relevance signals

- Mention state names verbatim throughout state pages
- Reference state regulators by name (NJ DGE, PA Gaming Control Board, etc.)
- State-specific responsible-gambling resources (1-800-GAMBLER plus state hotlines where they exist)
- Properly use SchemaOrg's `Place` schema for state pages (Phase 2)

---

## 10. Schema / Structured Data Roadmap

Already implemented:
- ✅ Organization (homepage)
- ✅ BreadcrumbList (every nested page)
- ✅ Article (news + guides)

To add in Phase 2:

### Review schema on operator reviews
```json
{
  "@type": "Review",
  "itemReviewed": { "@type": "Service", "name": "DraftKings Sportsbook" },
  "author": { "@type": "Organization", "name": "BettingOnline.org" },
  "reviewRating": { "@type": "Rating", "ratingValue": "4.9", "bestRating": "5" }
}
```

### FAQPage on FAQ-bearing pages
We have FAQ blocks on 60+ pages. Wrapping them in `FAQPage` schema can win Featured Snippets and "People Also Ask" inclusion.

### HowTo on calculator pages
Each calculator page can include `HowTo` schema for the step-by-step usage. Triggers Featured Snippet eligibility.

### SearchAction on homepage
Allow users to search the site directly from Google search results.

### Product on operator review pages
Combined with `Review` schema, this lets review pages display rating stars in SERPs — a CTR boost of 15-30%.

---

## 11. Conversion Tracking & Analytics

### Required setup at deploy

1. **Google Search Console** — Submit sitemap immediately. Verify property. Monitor coverage daily for first 4 weeks.
2. **Bing Webmaster Tools** — Submit same sitemap. Bing's market share is small but free.
3. **Analytics** — Recommended: Plausible (privacy-first, GDPR-friendly) or GA4. The site ships with no tracking by default for privacy.

### Conversion goals

The site monetizes via affiliate signups. Track:
- Outbound clicks to operator sites (event: `affiliate_click`)
- Affiliate-link CTR per page
- Bonus claims attributed to specific source pages
- Newsletter signups

### Search Console monitoring

Weekly:
- Top-performing queries and pages
- Pages with high impressions but low CTR (title/meta optimization opportunity)
- Pages with rising/falling rankings (content refresh signals)
- Coverage errors (broken canonical, blocked, duplicate)

Monthly:
- Topical cluster performance (filter by `/sports/`, `/casino/`, etc.)
- Branded vs. non-branded query performance
- Backlink growth

---

## 12. Compliance, Trust & Responsible Gambling

For YMYL content, this isn't just ethics — it's a ranking factor. Google penalizes gambling sites that don't display proper compliance signals.

### Mandatory on every page
- 21+ messaging
- Link to /legal/responsible-gambling.html
- Link to 1-800-GAMBLER
- Affiliate disclosure (when applicable)
- Privacy policy + terms accessible from footer

### State-specific compliance
- New Jersey, PA, MI, NY all require specific responsible-gambling messaging
- Affiliate Marketing Federation (CAP) guidelines compliance for UK-targeted content
- LATAM markets have emerging local rules (Brazil 2026)

### Content compliance
- Never claim "guaranteed wins" or "easy money"
- Never target minors (no Pokemon imagery, school references, etc.)
- Always disclose affiliate relationships
- Never frame gambling as a financial-investment alternative

### "Don't" list (all of these can trigger Google manual actions)
- Cloaking (showing different content to crawler vs. user)
- Doorway pages (thin content optimized for one keyword)
- Hidden text or links
- Aggressive interlinking with exact-match keyword anchors
- Buying backlinks
- Article spinning / AI content without editorial review

---

## 13. Competitor Analysis (top 10 in our space)

Our direct organic competitors:

| Site | Approx Authority | Their strength | Our gap |
|------|------------------|----------------|---------|
| Action Network | DA 76 | Picks data, podcast | We win on tools, lose on real-time data |
| Covers.com | DA 75 | Public betting %, scores | We win on strategy depth |
| ESPN BET | DA 95 | Brand authority | We win on impartiality |
| Vegas Insider | DA 73 | Vegas brand, pro picks | We win on UX, calculators |
| OddsShark | DA 71 | Trends data, picks | Comparable; we need stronger picks data |
| The Lines (catena) | DA 70 | State-by-state guides | We need to match their state coverage |
| BettingPros | DA 67 | Expert tools | Comparable on tools; they have more data |
| Sports Betting Dime | DA 66 | Operator reviews | Comparable; we win on calculator UX |
| BetSperts | DA 60 | News + content velocity | We need higher publication cadence |
| WSN.com | DA 65 | Mainstream brand crossover | They have older domain authority advantage |

### Key competitive observations

1. **State guides are table stakes.** Every competitor has 30+ state-level pages. We need full coverage (currently we have NJ from CSV; expanding via the new state-operator pages).

2. **Data partnership is the moat.** Action Network and OddsShark partnered with data providers (TheRundown, BetGenius). For us, the equivalent is wiring up TheOddsAPI to power live odds — already shells in place.

3. **Comparison pages convert.** "DraftKings vs FanDuel" type pages have ~30% bounce rate vs. 50% on review pages. We're adding 10 in this expansion.

4. **Tools are underleveraged.** Most competitors have 1-2 calculators. We have 6 working + 10 more in progress. This becomes a moat.

5. **Publishing cadence matters.** The top sites publish 20-30 fresh articles per week. Our news section is currently 6 articles; we need a content calendar.

---

## 14. The 100 New Pages — Strategic Rationale

This expansion adds 100 net-new pages designed to capture three categories of traffic:

### Distribution by intent

**Commercial intent (30 pages, ~30%)**
Pages that capture searchers ready to sign up. Highest direct revenue impact.
- 10 operator-vs-operator comparisons
- 10 state-operator combo pages
- 10 "best [X] for [Y]" pages

**Informational intent (45 pages, ~45%)**
Pages that build topical authority and earn long-term backlinks. Indirect revenue impact via internal linking + brand search.
- 15 bet-type explainer pages
- 10 game strategy pages
- 10 sport-specific strategy pages
- 5 beginner guides
- 5 reference / utility pages

**Tool intent (10 pages, ~10%)**
Calculators that earn backlinks AND keep users on-site for longer (engagement signal).
- 10 specialty calculators

**Event/seasonal (15 pages, ~15%)**
Pages that capture seasonal spike traffic. Updated annually.
- 10 major event guides
- 5 season previews

### Why these 100 specifically?

Each was selected based on:
1. **Search volume** — minimum 200 monthly searches (per Ahrefs/SEMrush keyword tools)
2. **Commercial relevance** — fits within our affiliate revenue model
3. **Content uniqueness** — not duplicating existing pages
4. **Internal-linking opportunity** — naturally links to/from existing pages
5. **Authority signal** — demonstrates topical depth in our cluster

### Internal linking from the new pages

Each new page links to:
- The relevant cluster hub (/sports/, /casino/, /poker/, /tools/, etc.)
- 2-3 sibling pages in the same category
- 1-2 of the hand-built premium reviews when commercial-intent appropriate
- 1 calculator where the topic supports it
- The relevant state guide where state-specific
- The responsible-gambling page (footer-style, on every page)

### Linking TO the new pages from existing pages

The homepage, hub pages, and existing reviews are updated to link contextually to the new content:
- Homepage → top comparison and best-of pages
- Sport hubs → new sport-specific strategy pages
- Casino/Poker hubs → new game strategy pages
- Operator reviews → new "Best [Sport] Sportsbook" pages and comparisons
- Tools page → 10 new calculators

This ensures the new pages aren't crawl-isolated and immediately receive PageRank flow from established pages.

---

## 15. 6-Month Roadmap

### Month 1 (Launch)
- Deploy site to host (Netlify/Cloudflare/Vercel)
- Submit sitemap to GSC, Bing
- Verify all 651 pages are indexed
- Monitor coverage daily; fix any reported issues
- Announce launch to affiliate partners (request backlinks)

### Month 2 (Quick wins)
- Implement Review + FAQPage + HowTo schema (start with top 50 highest-volume pages)
- Add `WebSite` schema with SearchAction to homepage
- Add author bylines to all articles (start with 10 hand-built guides)
- Add `Person` schema for authors
- Begin guest-post outreach (target 10 placements/month)

### Month 3 (Authority content)
- Publish 8-12 in-depth news articles
- Refresh top 20 ranking pages with updated 2026 stats
- Launch first quarterly industry report
- Pitch industry pubs for syndication

### Month 4 (Internal-link optimization)
- Audit internal-linking gaps via Screaming Frog
- Add 50+ contextual links from low-authority to high-authority pages
- Surface featured-snippet opportunities (questions in H2s)
- Create "topic hub" sub-pages (e.g., /strategy/parlay-betting/) that aggregate everything in a topic

### Month 5 (Off-page)
- Calculator embed campaign (pitch 50 sports-media sites)
- HARO pipeline at full volume (10 pitches/week)
- Begin link-reclamation (find unlinked brand mentions, request links)
- Launch PR campaign around state-by-state legal updates

### Month 6 (Refinement)
- A/B test SERP titles on top 20 pages
- Optimize CTR on pages with high impressions, low clicks
- Update review pages with quarterly re-scores
- Comprehensive Core Web Vitals audit
- Keyword-cluster expansion: identify clusters where we rank 4-15 and could push to top 3

---

## 16. The 100 New Pages: Detailed List

### Comparison pages (10) — `/compare/`
1. DraftKings vs FanDuel
2. BetMGM vs Caesars
3. DraftKings vs BetMGM
4. FanDuel vs Caesars
5. bet365 vs DraftKings
6. BetRivers vs DraftKings
7. DraftKings vs FanDuel vs BetMGM (3-way deep comparison)
8. PokerStars vs 888 Poker
9. Best Sportsbook vs Best Casino: Where Should I Start?
10. Sports Betting vs Daily Fantasy Sports

### State + Operator (10) — `/state-operator/`
11. DraftKings New York
12. DraftKings New Jersey
13. FanDuel New York
14. FanDuel Pennsylvania
15. BetMGM Michigan
16. BetMGM Arizona
17. Caesars Ohio
18. Caesars Virginia
19. bet365 Colorado
20. BetRivers Illinois

### Best-of (10) — `/best/`
21. Best Sportsbook for NFL Betting
22. Best Sportsbook for NBA Player Props
23. Best Sportsbook for MLB Run Lines
24. Best Sportsbook for Live Betting
25. Best Sportsbook Mobile App
26. Best Sportsbook for Beginners
27. Best Online Casino for Slots
28. Best Online Casino for Live Dealer
29. Best Poker Site for Beginners
30. Best Poker Site for Tournaments

### Bet types (15) — `/bet-types/`
31. What is a Moneyline Bet?
32. What is a Point Spread?
33. What is a Total (Over/Under)?
34. What is a Parlay Bet?
35. What is a Teaser Bet?
36. What is a Prop Bet?
37. What is a Future Bet?
38. What is Live (In-Play) Betting?
39. What is a Halftime Bet?
40. What is a Round Robin Bet?
41. What is an If Bet?
42. What is a Reverse Bet?
43. What is a Hedge Bet?
44. What is an Asian Handicap?
45. What is Draw No Bet?

### Game strategy (10) — `/strategy/`
46. Blackjack Basic Strategy Chart
47. Roulette Strategy: What Works (and What Doesn't)
48. Slots Strategy: RTP, Volatility, Bankroll
49. Baccarat Strategy: Banker vs Player vs Tie
50. Craps Strategy: Pass Line + Odds
51. Video Poker Strategy: Reading Pay Tables
52. Texas Hold'em Strategy: Pre-flop Ranges
53. Pot-Limit Omaha Strategy
54. Tournament Poker Strategy: ICM and Push/Fold
55. Cash Game Poker Strategy: Tracking + Game Selection

### Sport strategy (10) — `/strategy/sports/`
56. NFL Betting Strategy: Key Numbers and Spreads
57. NFL Player Props Strategy
58. NBA Betting Strategy: Pace and Rest
59. NBA Player Props Strategy
60. MLB Betting Strategy: Run Lines and Totals
61. MLB First-5-Innings Strategy
62. NHL Betting Strategy: Goalies Are the Market
63. Soccer Betting Strategy: Asian Handicaps and BTTS
64. Tennis Betting Strategy: Surfaces and Live Bets
65. Golf Betting Strategy: Outrights and Three-Balls

### Beginner guides (5) — `/beginners/`
66. How to Bet on Sports: Complete Beginner Guide
67. How to Choose a Sportsbook: A Practical Checklist
68. How to Read Odds: 5-Minute Crash Course
69. How to Make Your First Bet (Step-by-Step)
70. How to Avoid Beginner Mistakes

### Calculators (10) — `/tools/`
71. Vig Calculator
72. ROI Calculator
73. Implied Probability Calculator
74. Closing Line Value (CLV) Calculator
75. Bet Size Calculator
76. Round Robin Calculator
77. Teaser Calculator
78. Asian Handicap Calculator
79. Half-Time/Full-Time Calculator
80. Lay Bet Calculator

### Reference (5) — `/reference/`
81. Sports Betting Glossary (A-Z)
82. Bet Type Cheat Sheet
83. Odds Conversion Reference Table
84. Bankroll Management Quick Reference
85. Common Sports Betting Mistakes & How to Fix

### Major events (10) — `/events/`
86. Super Bowl Betting Guide 2026
87. March Madness Betting Guide
88. NFL Playoffs Betting Guide
89. World Series Betting Guide
90. Stanley Cup Betting Guide
91. NBA Finals Betting Guide
92. World Cup Betting Guide (next 2026)
93. Champions League Betting Guide
94. Wimbledon Betting Guide
95. The Masters Golf Betting Guide

### Season previews (5) — `/events/preview/`
96. NFL Season Preview & Futures
97. NBA Season Preview & Futures
98. MLB Season Preview & Futures
99. NHL Season Preview & Futures
100. College Football Season Preview & Futures

---

## 17. Measurement & Reporting

### Weekly dashboard (always-on)
- Total organic sessions (last 7 days vs prior 7)
- New rankings (queries entering top 10)
- Lost rankings (queries dropping out of top 10)
- Top performing pages by clicks
- Top performing pages by impressions

### Monthly review
- Cluster performance (sports / casino / poker / tools)
- Branded vs unbranded query mix
- Backlink growth (referring domains)
- Conversion rate per top-10 landing page
- Pages added to index this month
- Pages dropped from index this month (investigate)

### Quarterly business review
- Year-over-year cluster traffic
- Top 50 ranking changes
- Backlink quality mix (DA 50+ vs DA 30+)
- Conversion-to-revenue by cluster
- Competitor delta (we vs each top competitor)
- Algorithm-update impact assessment
- Roadmap adjustments

---

## 18. Risk Mitigation

### Algorithm update preparation
- Maintain regular content refreshes (avoid stale-content penalties)
- Monitor industry-watching tools (Sistrix, SearchEngineLand) for early algorithm signals
- Have content-refresh playbook ready for the 5-10 pages most at risk in any given update

### Manual action recovery (if it happens)
- Maintain disavow file
- Document every editorial decision
- Keep affiliate disclosure clean
- Never use AI content without editorial review/byline

### Affiliate program risk
- Don't depend on a single operator program; spread across 8+ operators
- Maintain a non-affiliate revenue path (newsletter, future paid reports)
- Build owned email list (newsletter signups already integrated)

### Compliance / regulatory risk
- State-by-state advertising compliance review quarterly
- Responsible-gambling messaging audit annually
- Privacy/cookie compliance for international visitors

---

## 19. Final Notes

This SEO plan is designed to be a living document. It should be reviewed quarterly and updated as:
- Google algorithm updates change ranking priorities
- New states legalize sports betting
- Operator landscape shifts (mergers, launches, exits)
- Competitor strategies evolve
- Our own ranking data shows what's working

The relaunched site is technically excellent, content-rich, and architected for compounding authority. With disciplined execution of this plan over 6-12 months, the goal of becoming the #1 independent betting guide in organic search is achievable.

---

*Last updated: April 2026. Next review: July 2026.*
