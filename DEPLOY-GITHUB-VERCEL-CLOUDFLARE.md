# Deploy BettingOnline.org via GitHub → Vercel → Cloudflare

This guide walks through deploying the site using GitHub for source control, Vercel for hosting + auto-deploys, and Cloudflare for DNS. **Total active time: ~45–60 minutes**, plus DNS propagation (5 minutes to 24 hours).

---

## Architecture

```
You edit files locally
        ↓
   git push
        ↓
   GitHub repo
        ↓ (webhook)
   Vercel auto-deploys
        ↓
   www.bettingonline.org
        ↑
 Cloudflare DNS
        ↑
 Domain registrar nameservers
```

You'll set this up once, then every `git push` deploys automatically in ~30 seconds.

---

## Part 1 — GitHub setup (10 min)

### 1.1 Install Git (skip if you already have it)

Open Terminal:

```bash
git --version
```

If it says "command not found", install Git from https://git-scm.com/download/mac (Mac) or use Homebrew: `brew install git`.

### 1.2 Create a GitHub account & repo

1. Sign up at https://github.com (free).
2. Click the **+** icon top-right → **New repository**.
3. Repository name: `bettingonline-site` (or anything you like).
4. Visibility: **Private** is recommended. Public is fine if you don't mind the source being visible.
5. **Do NOT** check "Add a README", "Add .gitignore", or "Choose a license" — your local folder already has the right files.
6. Click **Create repository**.
7. GitHub shows a "quick setup" page with your repo URL. Copy the URL (looks like `https://github.com/YOUR-USERNAME/bettingonline-site.git`).

### 1.3 Push your local folder to GitHub

In Terminal, navigate to your project folder:

```bash
cd "/Users/cg/Documents/Claude/Projects/Dev BettingOnline"
```

Initialize the repo and push:

```bash
git init
git add .
git commit -m "Initial commit — full site v1"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/bettingonline-site.git
git push -u origin main
```

If asked for credentials, GitHub now requires a **personal access token** instead of your password:
1. Go to https://github.com/settings/tokens → **Generate new token (classic)**.
2. Name it "BettingOnline deploy", scope: `repo` (full control of private repos).
3. Copy the token. Use it as your password when `git push` prompts.

After push completes, refresh your GitHub repo page — you should see all the files.

---

## Part 2 — Vercel setup (10 min)

### 2.1 Create Vercel account

1. Go to https://vercel.com/signup.
2. Click **Continue with GitHub**. This authorizes Vercel to read your GitHub repos (read-only — Vercel can't modify your code, only deploy it).
3. Pick the **Hobby** plan (free; allows custom domains).

### 2.2 Import your repo

1. In Vercel dashboard, click **Add New...** → **Project**.
2. Find your `bettingonline-site` repo in the list. Click **Import**.
3. Vercel asks for build configuration:
   - **Framework Preset:** "Other" (this is a static HTML site)
   - **Root Directory:** `./` (default — leave it)
   - **Build and Output Settings:** leave Build Command empty, Output Directory empty
   - **Environment Variables:** none needed
4. Click **Deploy**.

Vercel deploys in ~30 seconds. You'll get a URL like `bettingonline-site-abc123.vercel.app`.

### 2.3 Verify the staging URL

Open `https://bettingonline-site-abc123.vercel.app/` (your actual URL will differ).

**Smoke test:**
- Homepage loads
- Click through Sports / Casino / Poker / Reviews / Bonuses / Tools / Guides
- Open one calculator (e.g. `/tools/parlay/`) — verify it works
- Open the cookie banner — verify the thin bottom bar appears
- Toggle dark mode — verify it switches

If everything works, you're ready for the custom domain.

---

## Part 3 — Cloudflare DNS setup (15 min)

### 3.1 Create Cloudflare account

1. Go to https://dash.cloudflare.com/sign-up (free).
2. Verify your email.

### 3.2 Add your domain to Cloudflare

1. From Cloudflare dashboard, click **Add a site**.
2. Enter `bettingonline.org` (no www, no https).
3. Pick the **Free** plan.
4. Cloudflare scans your existing DNS records. For a fresh domain you may see nothing; that's fine.
5. Cloudflare gives you **2 nameservers** like:
   ```
   alice.ns.cloudflare.com
   ben.ns.cloudflare.com
   ```
   Copy these — you'll add them at your domain registrar.

### 3.3 Update nameservers at your registrar

Go to wherever you bought `bettingonline.org` (GoDaddy, Namecheap, Google Domains, etc.). Find the **Nameservers** or **DNS** section.

1. Change from "Default" or registrar nameservers to **Custom nameservers**.
2. Replace existing nameservers with the 2 Cloudflare nameservers from step 3.2.
3. Save.

**Propagation time:** 5 minutes to 24 hours (usually <2 hours). Cloudflare emails you when nameservers are confirmed.

### 3.4 (Once propagation completes) Configure DNS records

In Cloudflare → your domain → **DNS** → **Records**.

Vercel needs **two DNS records** to serve your domain. Vercel's docs give you the exact values once you add the domain in Vercel (Part 4 below) — typical setup is:

- **A record:** name `@`, value `76.76.21.21` (Vercel's anycast IP), proxy status: **DNS only** (gray cloud, NOT orange).
- **CNAME record:** name `www`, value `cname.vercel-dns.com`, proxy status: **DNS only**.

> **Important:** keep proxy status set to "DNS only" (gray cloud). Vercel handles SSL itself; turning on Cloudflare's orange-cloud proxy creates SSL handshake conflicts. You can experiment with the orange cloud later once everything is stable, but launch with gray cloud.

---

## Part 4 — Add custom domain in Vercel (10 min)

### 4.1 Add domain in Vercel

1. In Vercel dashboard → your project → **Settings** → **Domains**.
2. Type `www.bettingonline.org` and click **Add**.
3. Vercel detects that DNS isn't pointed yet. It tells you exactly what records to add — typically a `CNAME` from `www` → `cname.vercel-dns.com`.
4. Add `bettingonline.org` (the apex / no-www version) too. Vercel will tell you to set the apex `A` record to `76.76.21.21`.

### 4.2 Add the records in Cloudflare

Go back to Cloudflare → DNS → Records and add the records Vercel specified. Make sure both records are **proxy status: DNS only (gray cloud)**.

### 4.3 Wait for SSL provisioning

Vercel automatically issues an SSL certificate via Let's Encrypt. This takes 1–10 minutes.

In Vercel → Settings → Domains, both domains will show status "Valid Configuration" with a green checkmark when ready.

### 4.4 Set the canonical domain

The site is set up for `www.bettingonline.org` as canonical (all canonical URLs in the HTML point to www). In Vercel's domain settings, mark `www.bettingonline.org` as the **production domain** and configure `bettingonline.org` to redirect to `www.bettingonline.org` (Vercel offers a one-click redirect option).

---

## Part 5 — Verify production (15 min)

### 5.1 Open the production URL

Visit `https://www.bettingonline.org/`. You should see your homepage with a valid SSL padlock.

### 5.2 Smoke test on production

Repeat the staging smoke test:
- Click through main hubs
- Open 2–3 calculators
- Test the search box
- Test the cookie banner (clear cookies if needed)
- Toggle dark mode

### 5.3 Test redirects

These should all work:
- `bettingonline.org` → redirects to `www.bettingonline.org` ✓
- `http://www.bettingonline.org` → redirects to `https://` ✓
- `www.bettingonline.org/index.html` → redirects to `www.bettingonline.org/` ✓ (handled by `vercel.json`)

### 5.4 Run external tests

- **Security headers:** https://securityheaders.com/?q=https%3A%2F%2Fwww.bettingonline.org (target A grade — `vercel.json` ships with appropriate headers).
- **PageSpeed Insights:** https://pagespeed.web.dev/?url=https%3A%2F%2Fwww.bettingonline.org (target 90+ on mobile and desktop).
- **Schema rich results test:** https://search.google.com/test/rich-results — paste your homepage URL.

---

## Part 6 — Replace placeholder tokens (10 min)

Before announcing the site, update these placeholders:

### 6.1 Search Console verification tokens

Edit `index.html` locally:

```bash
# Open in your editor
open -a "Sublime Text" "/Users/cg/Documents/Claude/Projects/Dev BettingOnline/index.html"
```

Find and replace:
- `REPLACE_WITH_GSC_TOKEN` → your Google Search Console token
- `REPLACE_WITH_BING_TOKEN` → your Bing Webmaster token
- `REPLACE_WITH_YANDEX_TOKEN` → your Yandex token (or delete that meta tag if not using)

### 6.2 The Odds API key

Edit `assets/js/main.js`:

Find this line near the top:
```js
window.BO_ODDS_API_KEY = window.BO_ODDS_API_KEY || 'YOUR_API_KEY_HERE';
```

Replace `YOUR_API_KEY_HERE` with your actual key from https://the-odds-api.com.

### 6.3 Push the changes

```bash
cd "/Users/cg/Documents/Claude/Projects/Dev BettingOnline"
git add index.html assets/js/main.js
git commit -m "Add production verification tokens and API keys"
git push
```

Vercel auto-deploys in ~30 seconds. Refresh your site to confirm.

---

## Part 7 — Submit to search engines (10 min)

### 7.1 Google Search Console

1. Go to https://search.google.com/search-console.
2. Add property → **URL prefix** → enter `https://www.bettingonline.org/`.
3. Verify ownership using the meta tag (which is now in `index.html`). Click **Verify**.
4. Once verified → **Sitemaps** → add `https://www.bettingonline.org/sitemap.xml` → submit.
5. Open **URL Inspection** → paste your homepage URL → click **Request indexing**. Repeat for top 5–10 priority pages.

### 7.2 Bing Webmaster Tools

1. Go to https://www.bing.com/webmasters.
2. Add site `https://www.bettingonline.org/`.
3. Verify with the meta tag.
4. Submit sitemap.

### 7.3 (Optional) Submit to additional indexers

- **Yandex Webmaster** (Russian search): https://webmaster.yandex.com (only if relevant).
- **Apple News Publisher** (https://www.apple.com/apple-news/) for iOS news distribution.
- **Google News Publisher Center** for inclusion in Google News search.

---

## Future deployment workflow

Once everything is set up, deploying changes is just:

```bash
cd "/Users/cg/Documents/Claude/Projects/Dev BettingOnline"

# Make changes locally — edit any file

git add .
git commit -m "Describe what you changed"
git push
```

Vercel automatically builds and deploys on every push to `main`. Deploy time: ~30 seconds.

You can see deploy history, roll back to previous versions, or preview branch deploys at https://vercel.com/your-username/bettingonline-site/deployments.

---

## Troubleshooting

### "Site not loading after DNS change"
Wait. DNS propagation can take up to 24 hours. Use https://www.whatsmydns.net to check propagation globally. If after 24 hours nothing's working, double-check the DNS records match what Vercel asked for.

### "SSL not provisioning"
In Vercel → Settings → Domains, click **Refresh** next to the domain. Cloudflare proxy status must be "DNS only" (gray cloud) for SSL to work. If still failing, remove the domain from Vercel and re-add it.

### "Cookies/localStorage not persisting on www subdomain"
This is normal behavior — cookies set on `www.bettingonline.org` won't transfer to `bettingonline.org`. Since the apex redirects to www, this isn't a real issue, but if you see it during testing, force-redirect to www.

### "Pages return 404"
Check that the file exists at the expected path. Vercel serves `/some-page/` by looking for `/some-page/index.html`. The site is configured this way correctly.

### "I want to roll back to a previous deploy"
Vercel → your project → **Deployments** → click any previous deploy → **Promote to Production**. Effective immediately.

---

## Cost estimate

| Service | Plan | Cost |
|---------|------|------|
| GitHub | Free (private repos included) | $0 |
| Vercel | Hobby plan | $0 |
| Cloudflare | Free | $0 |
| Domain registration (existing) | Annual | ~$15/year |
| **Total ongoing** | | **~$15/year** |

Vercel Hobby includes generous limits: 100 GB bandwidth/month, unlimited deploys, custom domains, automatic SSL. You'd only need to upgrade if you hit traffic levels in the millions of visits per month.

---

## Quick reference — the 5-minute version

1. **GitHub:** create repo, `git init` + `git push` your project folder.
2. **Vercel:** sign up, import GitHub repo, framework "Other", deploy.
3. **Cloudflare:** add your domain, swap nameservers at your registrar.
4. **DNS records:** add A `@` → `76.76.21.21` and CNAME `www` → `cname.vercel-dns.com`, both gray cloud.
5. **Vercel custom domain:** add www and apex, wait for SSL.
6. **Replace tokens** in `index.html` and `main.js`, `git push`.
7. **Submit to GSC and Bing**, then announce.

Done.
