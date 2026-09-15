# BettingOnline.org — Buyer Handover Package

**For:** the new owner of bettingonline.org

Welcome. This document walks you through everything you need to get the site running on your own infrastructure — domain transfer, hosting, search-engine ownership, affiliate re-attribution, and analytics.

---

## What's in this package

```
bettingonline-org-handover.zip
├── HANDOVER.md                          ← this document
├── SEO-RECOVERY-PLAN.md                 ← current SEO status + recovery playbook
├── SEO-PLAN.md                          ← earlier SEO planning notes
├── LAUNCH-DAY.md                        ← operational runbook
├── DEPLOY.md                            ← deployment reference
├── DEPLOY-GITHUB-VERCEL-CLOUDFLARE.md   ← hosting-specific setup notes
├── docs/PROGRAMMATIC-SEO-STRATEGY.md    ← content strategy notes
├── data/                                ← content data (queues, feeds, config)
├── assets/                              ← CSS, JS, images, icons
├── {content directories}                ← all HTML content (sports, casino, poker, reviews, us, news, guides, etc.)
├── vercel.json                          ← Vercel deployment config with redirects and headers
├── _headers + _redirects                ← Netlify/Cloudflare Pages headers + redirects
├── sitemap.xml + news/sitemap.xml       ← current sitemaps
└── manifest.json + robots.txt + favicons
```

Total ~19 MB compressed. ~4,470 files. 870 HTML pages published.

---

## Step 1 — Domain transfer

The seller initiates transfer of `bettingonline.org` at the registrar. You'll receive an EPP/auth code by email. Typical transfer takes 5-7 days.

While transfer is pending, you can already prepare hosting — DNS will move over once the domain lands with you.

---

## Step 2 — Git + code hosting

This package ships as source files only (no `.git/` directory). Initialize a fresh git repository and push to your own GitHub organization:

```bash
unzip bettingonline-org-handover.zip
cd "Dev BettingOnline"        # or rename the folder to whatever you prefer
git init
git add .
git commit -m "Initial import from seller handover"
git branch -M main
git remote add origin git@github.com:YOUR-ORG/bettingonline.git
git push -u origin main
```

The site is a static build — no runtime dependencies, no environment variables to migrate, no database to restore. Once the files are in your repo, they're ready to deploy.

---

## Step 3 — Hosting (Vercel recommended)

The site is a static-HTML build. `vercel.json` in the root contains:
- 34 URL redirects (301s handling legacy WordPress URLs)
- Cache-Control headers for assets, HTML, sitemap
- Security headers (CSP, X-Frame-Options, HSTS, etc.)

**To deploy on Vercel:**
1. Create a new project at vercel.com
2. Import the GitHub repo
3. Framework preset: "Other" (static)
4. Build command: leave blank (site is pre-built)
5. Output directory: `.` (root)
6. Deploy

Once your custom domain is added and DNS points to Vercel, the site is live.

**Alternative hosts** — the site is plain static HTML with no runtime dependencies. It runs anywhere:
- **Netlify:** `_headers` and `_redirects` are included in the package for their format
- **Cloudflare Pages:** same import flow as Vercel
- **Any web server (nginx / apache):** copy the files to the doc root; the `vercel.json` redirects need to be translated to your webserver's rewrite rules

See `DEPLOY-GITHUB-VERCEL-CLOUDFLARE.md` for platform-specific notes.

---

## Step 4 — Google Search Console + Bing Webmaster Tools

The site has an active Search Console history you'll want ownership of.

**Path A (recommended): DNS verification transfer**
1. Sign in to Search Console at `search.google.com/search-console`
2. Add property → **Domain** → `bettingonline.org`
3. Google gives you a TXT record; add it to your DNS at the registrar
4. Verify — Google retains historical data and now shows it to you as the verified owner

**Path B: Request access from the seller**
The seller can add your Google account as a verified owner without you touching DNS. Ask for that if easier.

**Bing Webmaster Tools** — same principle. Add domain, DNS TXT record, verify.

**Existing GSC configuration to preserve:**
- Two sitemap submissions: `sitemap.xml` and `news/sitemap.xml`
- ~489 pages indexed as of package date
- Zero manual actions, zero security issues (verified)

---

## Step 5 — Affiliate accounts and click tracking

The site currently promotes 13 brands across sports / casino / poker. Every CTA on the site links to a tracked affiliate URL with `rel="sponsored nofollow"` and `data-affiliate-brand="{slug}"` for analytics.

**You will need to:**
1. Open affiliate accounts under your business at each network
2. Get your own tracking URLs
3. Search and replace in the codebase — every current tracker URL points to the seller's account

**The 13 brand slugs and their networks:**

| Brand slug | Network |
|---|---|
| `betonline-sportsbook` | BetOnline Affiliates |
| `sportsbetting-sportsbook` | Sportsbetting Affiliates |
| `betus-sportsbook` | Revmasters |
| `betonline-casino` | BetOnline Affiliates (casino) |
| `sportsbetting-casino` | BetOnline Affiliates (casino) |
| `betus-casino` | Revmasters (casino) |
| `black-chip-poker` | Winning Poker Network (wpnaffiliates.com) |
| `acr-poker` | Winning Poker Network |
| `ya-poker` | Winning Poker Network |
| `true-poker` | Winning Poker Network |
| `betonline-poker` | BetOnline Affiliates (poker) |
| `tigergaming-poker` | BetOnline Affiliates (poker) |
| `sportsbetting-poker` | BetOnline Affiliates (poker) |

**Quickest replacement approach:**

```bash
# 1. Discover the existing tracker URL for a brand:
grep -rE 'data-affiliate-brand="betonline-sportsbook"' . --include="*.html" | head -1
# The href="..." in the same tag is the tracker URL currently in place.

# 2. Once you have the existing tracker URL, run a sitewide sed to swap it for yours:
OLD_URL="<paste-the-existing-tracker-url-here>"
NEW_URL="<your-new-tracker-url-here>"
grep -rl "$OLD_URL" . --include="*.html" --include="*.json" \
  | xargs sed -i.bak "s|$OLD_URL|$NEW_URL|g"
find . -name "*.bak" -delete
```

Repeat once per brand with your new URLs. Commit and redeploy.

---

## Step 6 — Analytics wiring (optional but recommended)

The `data-affiliate-brand` attribute is present on every affiliate CTA on the site. This is the hook to wire clicks into GA4 or GTM.

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

## Step 7 — Content freshness stamps

The site uses an auto-updating month/year mechanism. Any HTML element with `data-current-month` gets its content replaced with the current month/year on page load — so freshness stamps stay current without manual editing.

Example on the homepage:
```html
<span data-current-month>July 2026</span>
```
The text `July 2026` is the fallback for no-JS visitors; the JS overwrites it with the current month on every page view.

---

## Step 8 — SEO status (important context)

The site is mid-recovery from Google's March 2024 Site Reputation Abuse / Helpful Content Update. Full history and forward plan is in `SEO-RECOVERY-PLAN.md`. Summary:

- Phase 1-3 recovery work has shipped (technical fixes, deepened state pages, E-E-A-T infrastructure, original data content)
- GSC impressions were rising quarter-over-quarter as of the last snapshot
- 489 pages indexed, 549 not-indexed — Coverage report in GSC has the specifics
- Zero manual actions

Recommended read-order for the new owner:
1. This file (HANDOVER.md)
2. `SEO-RECOVERY-PLAN.md` — SEO status + roadmap
3. `SEO-PLAN.md` — earlier planning notes
4. `docs/PROGRAMMATIC-SEO-STRATEGY.md` — content strategy notes

---

## Site quick reference

**Domain:** bettingonline.org (registered 2003)
**Vertical:** online gambling affiliate (sports betting, casino, poker)
**Content architecture:** pillar-and-cluster
**Live pages:** ~870 HTML files
**Backlinks:** substantial profile — see Ahrefs / Semrush for current numbers
**Stack:** static HTML, ready to deploy on any modern host

---

## Post-transfer checklist (in order)

1. [ ] Complete domain transfer at registrar
2. [ ] Push code to your GitHub org
3. [ ] Deploy on Vercel (or your preferred host)
4. [ ] Point domain to hosting
5. [ ] Verify Search Console + Bing Webmaster with your own accounts
6. [ ] Open affiliate accounts at each of the 13 brands' networks
7. [ ] Replace tracker URLs in codebase, commit, redeploy
8. [ ] Wire GA4 / GTM to `data-affiliate-brand` click events
9. [ ] Read SEO-RECOVERY-PLAN.md and decide next content investments

---

**Best of luck with the site.** The historical backlink profile and modern rebuild give you a strong foundation. The SEO recovery documentation in this package explains the reasoning behind the current site architecture and what's been prioritized.
