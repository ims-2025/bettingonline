# BettingOnline.org — Buyer Handover Package

**Prepared:** August 2026 · **For:** the new owner of bettingonline.org

Welcome. This document walks you through everything you need to get the site running on your own infrastructure — including source, deployment, automation, affiliate accounts, and search-engine ownership.

---

## What's in this package

```
bettingonline-org-handover.zip
├── HANDOVER.md                          ← this document
├── SEO-RECOVERY-PLAN.md                 ← current SEO status + recovery playbook
├── LAUNCH-DAY.md                        ← existing runbook (pre-launch reference)
├── DEPLOY.md                            ← deployment reference
├── docs/                                ← strategy docs, valuation, outreach templates
├── .git/                                ← full commit history (23+ years of asset development)
├── .github/workflows/                   ← 3 GitHub Actions (news, programmatic, pokersites rollout)
├── data/                                ← queues + config for automation
├── scripts/                             ← Python automation (news gen, programmatic pages, etc.)
├── assets/                              ← CSS, JS, images, icons
├── {content directories}                ← all HTML content (sports, casino, poker, reviews, us, etc.)
├── vercel.json                          ← Vercel deployment config with redirects and headers
├── sitemap.xml + news/sitemap.xml       ← current sitemaps
└── manifest.json + robots.txt + favicons
```

Total ~37 MB unpacked. ~3,400 files.

---

## Step 1 — Domain transfer

The seller will initiate transfer of `bettingonline.org` at the registrar. You'll receive an EPP/auth code by email. Typical transfer takes 5-7 days.

While transfer is pending, you can already start hosting setup — DNS will move over when the domain lands with you.

---

## Step 2 — Git + code hosting

The `.git` directory in this package contains the full development history.

**Option A: Push to your own GitHub organization** (recommended)
```bash
unzip bettingonline-org-handover.zip -d bettingonline
cd bettingonline
# Rename remote to your new repo
git remote remove origin
git remote add origin git@github.com:YOUR-ORG/bettingonline.git
git push -u origin main
```

**Option B: Use as-is without git history**
Delete the `.git/` directory. The site will still work — you'll just be starting a fresh git history.

The three GitHub Actions workflows under `.github/workflows/` will run automatically once the repo is on GitHub:

- `daily-news.yml` — publishes 2 news articles every Tuesday + Friday at 06:00 UTC
- `programmatic-daily.yml` — publishes 2 pages/day from `data/programmatic-queue.json` at 07:00 UTC (48 pages remaining in queue)
- `pokersites-rollout.yml` — one-shot editorial link additions (see notes at bottom)

If you don't want these running, delete the workflow files or disable them in GitHub Actions settings.

---

## Step 3 — Hosting (Vercel recommended)

The site is a static-HTML build optimized for Vercel. `vercel.json` in the root contains:
- 34 URL redirects (301s handling legacy WordPress URLs)
- Cache-Control headers for assets, HTML, sitemap
- Security headers (CSP, X-Frame-Options, etc.)

**To deploy on Vercel:**
1. Create a new project at vercel.com
2. Import the GitHub repo
3. Framework preset: "Other" (static)
4. Build command: leave blank (site is pre-built)
5. Output directory: `.` (root)
6. Deploy

Once your custom domain is added and DNS points to Vercel, the site is live.

**Alternative hosts** — the site is plain static HTML with no runtime dependencies. It runs anywhere:
- Netlify: same import flow
- Cloudflare Pages: same
- Any web server (nginx / apache): copy the files to the doc root; the `vercel.json` redirects need to be translated to your webserver's rewrite rules

---

## Step 4 — Google Search Console + Bing

The site has an active Search Console history you'll want ownership of.

**Path A (recommended): DNS verification transfer**
1. Sign in to Search Console at search.google.com/search-console
2. Add property → **Domain** → `bettingonline.org`
3. Google gives you a TXT record; add it to your DNS at the registrar
4. Verify — Google will retain historical data and now show it to you as the verified owner

**Path B: Request access from the seller**
The seller can add your Google account as a verified owner without you touching DNS. Ask for that if easier.

**Bing Webmaster Tools** — same principle. Add domain, DNS TXT record, verify.

**Existing GSC configuration to preserve:**
- Two active sitemap submissions: `sitemap.xml` and `news/sitemap.xml`
- 489+ pages indexed as of package date
- Zero manual actions, zero security issues (verified)

---

## Step 5 — Affiliate accounts and click tracking

The site currently promotes 13 brands across sports / casino / poker. Every CTA on the site links to a tracked affiliate URL with `rel="sponsored nofollow"` and `data-affiliate-brand="{slug}"` for analytics.

**You will need to:**
1. Open affiliate accounts under your business at each network
2. Get your own tracking URLs
3. Search and replace in the codebase — every current tracker URL points to the seller's account

**The 13 brand slugs and their networks:**

| Brand slug | Network | Tracker URL to replace |
|---|---|---|
| `betonline-sportsbook` | BetOnline Affiliates | ends `/2/` |
| `sportsbetting-sportsbook` | Sportsbetting Affiliates | ends `/2/` |
| `betus-sportsbook` | Revmasters | ends `/2/` |
| `betonline-casino` | BetOnline Affiliates | ends `/3/` (casino) |
| `sportsbetting-casino` | BetOnline Affiliates | ends `/3/` |
| `betus-casino` | Revmasters | ends `/2/` (casino) |
| `black-chip-poker` | Winning Poker Network | `wpnaffiliates.com` |
| `acr-poker` | Winning Poker Network | `wpnaffiliates.com` |
| `ya-poker` | Winning Poker Network | `wpnaffiliates.com` |
| `true-poker` | Winning Poker Network | `wpnaffiliates.com` |
| `betonline-poker` | BetOnline Affiliates | ends `/3/` (poker) |
| `tigergaming-poker` | BetOnline Affiliates | ends `/3/` |
| `sportsbetting-poker` | BetOnline Affiliates | ends `/3/` |

Quickest replacement approach:
```bash
# From the repo root — first find one tracker URL from any brand, then swap it sitewide
# 1. Discover the existing tracker URL for a brand (grep for the brand slug's data-affiliate-brand attribute):
grep -rE 'data-affiliate-brand="betonline-sportsbook"' . --include="*.html" | head -1
# The href="..." in the same tag is the tracker URL to replace.

# 2. Once you have the existing tracker URL, run a sitewide sed to swap it for yours:
OLD_URL="<paste-the-existing-tracker-url-here>"
NEW_URL="<your-new-tracker-url-here>"
grep -rl "$OLD_URL" . --include="*.html" --include="*.json" --include="*.py" \
  | xargs sed -i.bak "s|$OLD_URL|$NEW_URL|g"
find . -name "*.bak" -delete
```
Repeat once per brand with your new URLs. Commit and redeploy.

Alternatively, the mapping is centralised in `scripts/programmatic-queue-build.py` and in the site's poker/sportsbook/casino builder scripts under `scripts/`. Updating those in one place, then regenerating the pages, is the maintainable long-term approach.

---

## Step 6 — Analytics wiring (optional but recommended)

The `data-affiliate-brand` attribute is on every affiliate CTA — this is the hook to wire clicks into GA4 or GTM.

Sample GA4 event listener (drop into `assets/js/main.js` or fire via GTM):
```javascript
document.addEventListener('click', function(e) {
  var el = e.target.closest('[data-affiliate-brand]');
  if (el) {
    gtag('event', 'affiliate_click', {
      brand: el.getAttribute('data-affiliate-brand'),
      href: el.getAttribute('href'),
      vertical: (el.getAttribute('data-affiliate-brand') || '').split('-').pop()
    });
  }
});
```

---

## Step 7 — Automation (understand what's running)

### `.github/workflows/daily-news.yml`
Runs Tuesday + Friday at 06:00 UTC. Executes `scripts/generate-daily-news.py` which auto-produces 2 news articles per run, updates `news/index.html` + homepage + RSS + JSON feed, commits, pushes. Vercel auto-deploys.

To disable: delete the workflow file, or set `on:` to only `workflow_dispatch`.

### `.github/workflows/programmatic-daily.yml`
Runs daily at 07:00 UTC. Executes `scripts/programmatic-publish.py` which reads `data/programmatic-queue.json`, publishes the next 2 queued pages under `/compare/` or `/guides/` folders, updates sitemap, commits, pushes. Queue has 48 pages remaining as of package date.

### `.github/workflows/pokersites-rollout.yml`
Runs daily at 06:15 UTC. Self-guards on date — becomes a no-op after both scheduled additions have fired (2026-08-04 and 2026-08-11). You can delete this workflow safely.

---

## Step 8 — Content refresh conventions

The site uses an auto-updating month/year mechanism. Any HTML element with `data-current-month` gets its content replaced with the current month/year on page load — so freshness stamps stay current without manual editing.

Example already in the homepage:
```html
<span data-current-month>July 2026</span>
```
The text `July 2026` is the fallback for no-JS visitors; the JS overwrites it with the current month on every page view.

---

## Step 9 — SEO status (important context)

The site is mid-recovery from Google's March 2024 Site Reputation Abuse / Helpful Content Update. Full history and forward plan is in `SEO-RECOVERY-PLAN.md`. Summary:

- Phases 1-3 (technical fixes, content depth, E-E-A-T, original data content) shipped
- GSC impressions rising +80% quarter-over-quarter as of July 2026
- 489 pages indexed, 549 not indexed — Coverage report in GSC has the detail
- 4-week pokersites.org authority-link rollout scheduled through August 2026

Recommended read-order for the new owner:
1. This file (HANDOVER.md)
2. `SEO-RECOVERY-PLAN.md` — SEO status + roadmap
3. `docs/PROGRAMMATIC-SEO-STRATEGY.md` — content pipeline strategy
4. `docs/BettingOnline-org-Valuation-Sheet.md` — asset breakdown

---

## Step 10 — Support quick-reference

**Domain:** bettingonline.org (registered 2003)
**Vertical:** online gambling affiliate (sports betting, casino, poker)
**Content architecture:** pillar-and-cluster with automation
**Live pages:** ~800
**Backlinks:** 7,500 across 442 referring domains (as of last audit)

**Files worth reading first:**
- `SEO-RECOVERY-PLAN.md` — where the site is in its recovery cycle
- `docs/PROGRAMMATIC-SEO-STRATEGY.md` — content strategy adapted from Zapier's 2026 programmatic playbook
- `LAUNCH-DAY.md` — original launch checklist (still useful as an operational reference)
- `DEPLOY.md` — deployment specifics
- `docs/pokersites-week4-outreach.md` — pending outreach template for the pokersites.org cross-linking work

---

## Post-transfer to-do list (in order)

1. [ ] Complete domain transfer at registrar
2. [ ] Push code to your GitHub org
3. [ ] Deploy on Vercel (or your preferred host)
4. [ ] Point domain to hosting
5. [ ] Verify Search Console + Bing Webmaster with your own accounts
6. [ ] Open affiliate accounts at each of the 13 brands' networks
7. [ ] Replace tracker URLs in codebase, commit, redeploy
8. [ ] Wire GA4 / GTM to `data-affiliate-brand` click events
9. [ ] Decide which GitHub Actions to keep, disable, or delete
10. [ ] Read SEO-RECOVERY-PLAN.md and decide next content investments

---

**Best of luck with the site.** The historical backlink profile and modern rebuild give you a strong foundation; the recovery trajectory documented in GSC is what makes the acquisition thesis work. If you have questions on any specific piece of the codebase, the commit history in `.git/` documents the reasoning behind essentially every architectural decision.
