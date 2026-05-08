# BettingOnline.org — Launch Day Runbook

A step-by-step deploy day checklist with timing, verification steps, and rollback procedures. Estimated total time: **3–5 hours of active work**, plus ~24 hours for DNS propagation and search-console processing.

---

## T-7 days: Pre-launch prep (do these the week before)

### Accounts & access (each ~10 min)
- [ ] **Google Search Console** — sign up, create property `https://www.bettingonline.org/`, copy the meta-tag verification token.
- [ ] **Bing Webmaster Tools** — sign up, create site, copy the meta-tag token.
- [ ] **Yandex Webmaster** — optional. Skip if you don't care about Russian traffic.
- [ ] **Plausible Analytics** — sign up at plausible.io (or pick your preferred analytics — Cloudflare Web Analytics is also free).
- [ ] **The Odds API** — sign up at the-odds-api.com, copy the API key (free tier: 500 requests/mo).
- [ ] **Affiliate programs** — apply to DraftKings, FanDuel, BetMGM, Caesars, bet365, BetRivers affiliate networks. Approval typically takes 3–7 days. Save the affiliate URLs.
- [ ] **Newsletter ESP** — sign up at Mailchimp, ConvertKit, or Buttondown. Get the form embed code.

### Hosting (~15 min)
- [ ] **Cloudflare account** — sign up at cloudflare.com (free).
- [ ] **GitHub repo** — push the `Dev BettingOnline` folder to a new GitHub repo named `bettingonline-site` (private is fine).
- [ ] **Cloudflare Pages** — connect the GitHub repo, set build output to `/` (no build step required), deploy to a staging URL like `bettingonline.pages.dev`.

### Domain (~10 min)
- [ ] **Domain registrar** — log in to where bettingonline.org is registered.
- [ ] **DNS records** — note current A/CNAME records so you can roll back if needed.

---

## T-3 days: Replace placeholders & test on staging

### Update tokens in `index.html`
- [ ] Replace `REPLACE_WITH_GSC_TOKEN` with your Google Search Console token.
- [ ] Replace `REPLACE_WITH_BING_TOKEN` with your Bing Webmaster token.
- [ ] Replace `REPLACE_WITH_YANDEX_TOKEN` with your Yandex token (or remove the meta tag).

### Update API keys in `assets/js/main.js`
- [ ] Replace `YOUR_API_KEY_HERE` (search for `BO_ODDS_API_KEY`) with your The Odds API key.

### Wire newsletter to ESP
- [ ] In `assets/js/main.js`, find the `<form class="newsletter">` block (search for `data-nl`).
- [ ] Replace the `onsubmit` handler with the embed code from your ESP. Common pattern: change the `<form>` `action` to your ESP's POST URL and add a hidden field with your list ID.

### Replace internal review links with affiliate URLs
- [ ] If you want operator links to track to your affiliate accounts, run a find-and-replace across the codebase. The current links go to internal review pages — leave those internal links for SEO, but add affiliate buttons on each review page itself with your tracking URL.

### Add analytics
- [ ] In `assets/js/main.js`, add your Plausible (or GA4) script before the closing `</body>` tag is rendered. For Plausible, the simplest is to add a `<script defer data-domain="bettingonline.org" src="https://plausible.io/js/script.js"></script>` to every HTML head. You can do this with a one-line find-replace across all .html files.

### Push to staging and verify (~30 min)
- [ ] Push your changes to GitHub. Cloudflare Pages auto-rebuilds.
- [ ] Visit `bettingonline.pages.dev` (or your staging URL).
- [ ] **Smoke test:** click through main hubs (sports, casino, poker, reviews, tools, bonuses, news), verify pages load.
- [ ] **Calculator test:** open `/tools/parlay/`, `/tools/ev/`, `/tools/kelly/` — input sample values, confirm output.
- [ ] **Search test:** click magnifier icon in header, type "draftkings" — verify results.
- [ ] **Mobile drawer:** resize browser to <720px, confirm hamburger menu opens.
- [ ] **Theme toggle:** click moon/sun icon, confirm dark/light theme switches.
- [ ] **Cookie banner:** clear cookies/localStorage, confirm thin bottom bar appears.
- [ ] **Live odds:** confirm the live odds shell loads real data (or shows illustrative samples if API key not set).
- [ ] **PageSpeed Insights:** run on staging URL — target 90+ on mobile and desktop.
- [ ] **Lighthouse audit:** target 95+ on Accessibility, SEO, Best Practices.
- [ ] **Schema validation:** test 5 critical pages on Google's Rich Results Test (https://search.google.com/test/rich-results):
  - Homepage
  - `/reports/2026-state-of-the-industry/`
  - `/reviews/draftkings/`
  - `/us/new-york/`
  - `/guides/why-retail-bettors-lose.html`
- [ ] **404 page:** visit a non-existent URL, confirm polished 404 page renders.

---

## T-0 (Launch day): Switch DNS

**Best timing:** Tuesday–Thursday, 10am ET. Avoid Friday afternoons and weekends.

### Hour 1: DNS switch
- [ ] **Verify staging is healthy.** Re-run smoke tests above.
- [ ] **In your domain registrar:** update DNS records.
  - `A` record for `@` (apex): point to Cloudflare Pages IP (per their setup docs)
  - `CNAME` for `www`: point to your Cloudflare Pages URL
  - Or, if using Cloudflare for DNS too: just add the domain to Cloudflare and follow the wizard.
- [ ] **In Cloudflare Pages dashboard:** add `bettingonline.org` and `www.bettingonline.org` as custom domains.
- [ ] **Wait for SSL provisioning.** Typically 5–60 minutes. Refresh `https://www.bettingonline.org/` periodically.

### Hour 2: Verify production
- [ ] Confirm `https://www.bettingonline.org/` loads with valid SSL.
- [ ] Confirm `bettingonline.org` redirects to `www.bettingonline.org` (the `_redirects` file handles this on Cloudflare/Netlify).
- [ ] Repeat the staging smoke test on production.
- [ ] **Headers test:** run https://securityheaders.com on your domain. Target A grade. The `_headers` file ships with appropriate security headers.

### Hour 3: Search console setup
- [ ] **Google Search Console** — verify property using the meta tag (already in `index.html`). Submit sitemap: `https://www.bettingonline.org/sitemap.xml`.
- [ ] **Request indexing** for top 10 priority pages: homepage, reports, top operator reviews, top state pages.
- [ ] **Bing Webmaster Tools** — verify, submit sitemap.
- [ ] **Yandex** — verify (if used).

### Hour 4: Set up monitoring
- [ ] **Cloudflare Analytics** auto-tracks if using Cloudflare Pages.
- [ ] **Uptime monitor** — set up free uptime monitoring (UptimeRobot, BetterStack, or Cloudflare's built-in uptime checks).
- [ ] **Email alerts** — configure email alerts on uptime monitor for downtime.

### Hour 5: Social signals
- [ ] **Twitter/X** announce launch with link to homepage.
- [ ] **LinkedIn** post on company page.
- [ ] **Submit to relevant directories** (DMOZ-style aggregators for gambling sites — though most have closed; consider Reddit's `r/sportsbook`, `r/sportsbookadvice` on launch).

---

## Post-launch: Days 1–7

### Day 1
- [ ] **Hourly checks for the first 4 hours** — verify no SSL issues, no 500 errors in Cloudflare logs.
- [ ] **Test the cookie banner** in a fresh incognito window on multiple browsers (Chrome, Firefox, Safari mobile).
- [ ] **Test the search** with random queries to confirm relevant results.
- [ ] **Submit to Apple News Publisher** (if pursuing Apple News).
- [ ] **Submit RSS feed to Google News Publisher Center.**

### Day 2–3
- [ ] **Monitor Google Search Console** — check for crawl errors, coverage warnings.
- [ ] **Check PageSpeed Insights** on production. Compare to staging benchmark.
- [ ] **Monitor Cloudflare Analytics** for traffic patterns.
- [ ] **Monitor uptime monitor** for any flapping.

### Day 4–7
- [ ] **First content update** — publish a fresh news article to demonstrate cadence.
- [ ] **Verify GSC indexing progress** — by day 7 you should have ~50–100 pages indexed.
- [ ] **Check for backlinks** via Ahrefs free tools or Google Search Console links report.

---

## Rollback procedure (if something breaks)

If the production site is broken:

1. **DNS rollback:** revert DNS changes at your domain registrar to point back to old hosting (if any) — DNS propagation 5–60 min.
2. **Cloudflare Pages rollback:** in Pages dashboard, click "Rollback to previous deployment." Effective immediately.
3. **Specific file fix:** push a fix commit to GitHub. Cloudflare auto-deploys in ~30 sec.

Keep the GitHub repo's first deploy commit tagged so you can always roll back to a known-good state.

---

## Ongoing maintenance schedule (weekly/monthly/quarterly)

### Weekly
- [ ] Review GSC coverage report; fix any newly indexed pages with errors.
- [ ] Check operator welcome offer copy is current (welcome offers change frequently).
- [ ] Publish 1–2 news articles (target 10/month for healthy publishing cadence).

### Monthly
- [ ] Refresh "Last updated" stamps on top traffic pages.
- [ ] Re-rate top 6 operators using the 100-point framework; update review pages if scores changed.
- [ ] Review Core Web Vitals; address regressions.

### Quarterly
- [ ] Full operator re-rate cycle.
- [ ] State page refresh — regulatory changes need to be reflected.
- [ ] Tax-strategy guide update before US tax season (March/April).
- [ ] Performance audit (PageSpeed, Lighthouse).

### Annually
- [ ] Annual industry report update (next: April 2027).
- [ ] Backlink audit + outreach.
- [ ] Editorial standards review.

---

## Critical files reference

| File | Purpose | Edit before launch? |
|------|---------|---------------------|
| `index.html` | Homepage | Yes — replace 3 verification tokens |
| `assets/js/main.js` | Shared JS | Yes — replace `BO_ODDS_API_KEY` |
| `_headers` | Security + cache headers | No (already configured) |
| `_redirects` | URL redirects | No (already configured) |
| `manifest.json` | PWA manifest | No |
| `sitemap.xml` | XML sitemap | No (auto-generated) |
| `robots.txt` | Crawl rules | No (auto-generated) |
| `news/rss.xml` | News RSS feed | No (auto-generated) |
| `DEPLOY.md` | Hosting setup guide | No |
| `LAUNCH-DAY.md` | This file | No |
| `SEO-PLAN.md` | 360 SEO strategy | No (reference doc) |

---

## Support & escalation

- **Hosting issues:** Cloudflare Support (paid Pro plan recommended for priority support: $20/mo)
- **DNS issues:** your domain registrar's support
- **SSL issues:** auto-handled by Cloudflare Pages; rarely needs intervention
- **Content questions:** editorial@bettingonline.org
- **Privacy questions:** privacy@bettingonline.org
- **Legal questions:** legal@bettingonline.org

---

## Final pre-launch confidence check

If all the following are true, you are go for launch:

- [ ] All 3 verification tokens replaced
- [ ] The Odds API key replaced (or live odds shell explicitly disabled)
- [ ] Newsletter form wired to your ESP (or removed)
- [ ] Analytics installed
- [ ] Affiliate URLs updated on review pages
- [ ] Smoke test passing on staging URL
- [ ] PageSpeed 90+ on mobile and desktop
- [ ] Schema validated on top 5 pages
- [ ] DNS records ready to switch
- [ ] Rollback plan understood

Estimated time from "go" to "indexed in Google": 7–14 days for initial indexing, 60–90 days for full SEO ramp.

**Good luck with the launch.**
