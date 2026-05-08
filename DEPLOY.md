# BettingOnline.org — Go-Live Deployment Guide

The site is fully built, polished, and ready to deploy. This guide covers hosting, DNS, security headers, search-console submission, analytics, redirects, and post-deploy verification.

## What's in the package

```
Dev BettingOnline/
├── index.html                  # Homepage (528 lines, full hero + sections)
├── 404.html                    # Polished 404 page (noindex)
├── sitemap.html                # HTML sitemap (740+ pages indexed by category)
├── sitemap.xml                 # XML sitemap for Google/Bing
├── robots.txt                  # Crawl directives
├── manifest.json               # PWA manifest
├── favicon.ico                 # Legacy ICO favicon (16px + 32px)
├── DEPLOY.md                   # this file
├── SEO-PLAN.md                 # 360 SEO strategy doc
├── assets/
│   ├── css/
│   │   ├── main.css            # Source CSS
│   │   └── main.min.css        # Minified production CSS (16% smaller)
│   ├── js/
│   │   ├── main.js             # JS — header/footer/search/cookie/calc
│   │   └── search-index.json   # Client-side search index
│   └── img/
│       ├── logo.svg            # Brand wordmark
│       ├── favicon.svg         # Square mark
│       ├── apple-touch-icon.svg
│       └── og-{default,sports,casino,poker,news,guides,reports}.svg
├── about/, methodology/, editorial-standards/, how-we-rate/  # E-E-A-T
├── reviews/                    # Operator reviews + AggregateRating schema
├── us/                         # 39 state pages
├── sports/, casino/, poker/    # Vertical hubs
├── strategy/, guides/          # Strategy library (27 guides)
├── reference/                  # Glossary, cheat sheet, conversion table, etc
├── tools/                      # 6 betting calculators (HowTo schema)
├── bonuses/                    # Bonus finder + 4 T&C deep dives
├── news/                       # 14 articles + rss.xml + feed.json
├── reports/                    # 2026 State of the Industry annual report
├── authors/                    # 5 author profiles + Person schema
├── legal/                      # Privacy, Terms, Disclosure, Responsible Gambling
└── (various legacy URL paths preserved for SEO continuity)
```

## Pre-launch checklist

Replace these placeholder tokens before going live:
- [ ] `REPLACE_WITH_GSC_TOKEN` (in `index.html` `<meta name="google-site-verification">`)
- [ ] `REPLACE_WITH_BING_TOKEN` (in `index.html` `<meta name="msvalidate.01">`)
- [ ] `REPLACE_WITH_YANDEX_TOKEN` (optional)
- [ ] Verify all `mailto:` and `tel:` links match your real contact info
- [ ] Decide on analytics (Plausible, Fathom, Cloudflare Analytics, or none)
- [ ] Confirm welcome-offer copy in `bonuses/` and `reviews/` matches what your affiliate program currently pays

## Hosting recommendations

### Option A: Cloudflare Pages (recommended)
Best for static sites. Global CDN, automatic SSL, free tier handles serious traffic.

```
# In Cloudflare Pages dashboard, after connecting your repo:
# Build command: (none — static)
# Build output directory: /
```

Advantages: free SSL, free CDN, free analytics, custom redirects via `_redirects`, custom headers via `_headers`.

### Option B: Netlify
Same model as Cloudflare Pages. `_redirects` and `_headers` files work identically.

### Option C: Vercel
Set up `vercel.json` with rewrites/redirects. CDN comparable to Cloudflare.

### Option D: Traditional cPanel / Apache
Upload via FTP/SFTP. Configure `.htaccess` for redirects/headers (see below).

## DNS setup

- **A record:** `@` → host's IP (per host docs)
- **CNAME:** `www` → host's apex domain
- **Canonical host:** `www.bettingonline.org` (already reflected in canonical URLs throughout the site).

## SSL/TLS

Cloudflare Pages, Netlify, Vercel auto-issue Let's Encrypt certs. cPanel hosts: enable AutoSSL or upload certificate. Enable HSTS once SSL is stable.

## Security headers

### Cloudflare Pages / Netlify (`_headers` file at site root)

```
/*
  X-Frame-Options: SAMEORIGIN
  X-Content-Type-Options: nosniff
  Referrer-Policy: strict-origin-when-cross-origin
  Permissions-Policy: geolocation=(), microphone=(), camera=(), payment=()
  Strict-Transport-Security: max-age=31536000; includeSubDomains
  Content-Security-Policy: default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; font-src 'self' https://fonts.gstatic.com; img-src 'self' data: https:; connect-src 'self'; frame-ancestors 'self'

/assets/*
  Cache-Control: public, max-age=31536000, immutable

/*.html
  Cache-Control: public, max-age=300, must-revalidate
```

### Apache `.htaccess`

```apache
Header set X-Frame-Options "SAMEORIGIN"
Header set X-Content-Type-Options "nosniff"
Header set Referrer-Policy "strict-origin-when-cross-origin"
Header set Permissions-Policy "geolocation=(), microphone=(), camera=(), payment=()"
Header set Strict-Transport-Security "max-age=31536000; includeSubDomains"
Header set Content-Security-Policy "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; font-src 'self' https://fonts.gstatic.com; img-src 'self' data: https:;"

<FilesMatch "\.(svg|css|js|woff2|png|jpg)$">
    Header set Cache-Control "public, max-age=31536000, immutable"
</FilesMatch>

<FilesMatch "\.html$">
    Header set Cache-Control "public, max-age=300, must-revalidate"
</FilesMatch>
```

## 301 redirects

The URL structure here preserves all 700+ legacy paths from the old site. No mass redirects required.

If specific URLs change later:

### Cloudflare Pages / Netlify (`_redirects` file)

```
# Force www
https://bettingonline.org/*  https://www.bettingonline.org/:splat  301!

# Specific redirects below as needed
# /old-url  /new-url  301
```

### Apache `.htaccess`

```apache
RewriteEngine On
RewriteCond %{HTTP_HOST} !^www\. [NC]
RewriteRule ^(.*)$ https://www.%{HTTP_HOST}/$1 [L,R=301]
RewriteCond %{HTTPS} off
RewriteRule ^(.*)$ https://%{HTTP_HOST}/$1 [L,R=301]
```

## Analytics

### Plausible (recommended — privacy-respecting)

Add before `</head>` in `index.html`:

```html
<script defer data-domain="bettingonline.org" src="https://plausible.io/js/script.js"></script>
```

### Cloudflare Web Analytics
Enabled via Cloudflare Pages dashboard. No code changes required.

### Google Analytics 4 (if needed)

```html
<script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}gtag('js',new Date());gtag('config','G-XXXXXXXXXX');</script>
```

## Search Console submission

### Google Search Console
1. Add property: `https://www.bettingonline.org/`
2. Verify with the meta tag (replace `REPLACE_WITH_GSC_TOKEN` in `index.html`)
3. Submit sitemap: `https://www.bettingonline.org/sitemap.xml`
4. Request indexing for top-priority pages: homepage, top operator reviews, key state pages
5. Monitor Core Web Vitals + Coverage reports weekly

### Bing Webmaster Tools
1. Add site, verify via meta tag (replace `REPLACE_WITH_BING_TOKEN`)
2. Submit `sitemap.xml`
3. Bing typically indexes faster than Google

### IndexNow (Bing/Yandex/Seznam)
Bing accepts IndexNow pings for instant indexing. Cloudflare auto-supports if enabled.

## RSS feeds

The site publishes:
- `/news/rss.xml` (RSS 2.0 — Google News, Feedly, etc.)
- `/news/feed.json` (JSON Feed 1.1)

Submit to:
- Google News Publisher Center (apply for inclusion)
- Apple News Publisher (optional)

## Post-deploy verification (run within first 24 hours)

- [ ] Visit homepage on mobile + desktop, confirm rendering
- [ ] Tap through main hubs (sports, casino, poker, reviews, tools, bonuses, news)
- [ ] Test 3 calculators (parlay, EV, Kelly) — confirm math works
- [ ] Test search (top-right magnifier) — confirm results render
- [ ] Test mobile drawer — confirm opens, links work
- [ ] Test dark/light theme toggle
- [ ] Test cookie banner — accept + reject paths
- [ ] Submit to Google Search Console + request indexing on homepage
- [ ] Submit RSS to Google News (if pursuing News inclusion)
- [ ] Check Google PageSpeed Insights — target 90+ on mobile + desktop
- [ ] Check Lighthouse a11y, SEO, best practices — target 95+
- [ ] Run schema validator on top 5 pages: homepage, /reports/2026-state-of-the-industry/, /reviews/draftkings/, /us/new-york/, /guides/why-retail-bettors-lose.html
- [ ] Verify favicon renders in browser tab + bookmarks
- [ ] Wire newsletter form to a backend (Mailchimp, ConvertKit, Buttondown) — currently shows confirmation message but does not POST anywhere

## Ongoing maintenance

### Weekly
- [ ] Review GSC for crawl errors, new indexed pages
- [ ] Check operator welcome offers — update bonus copy if changes
- [ ] Publish 1-2 news items (target cadence: 10/month)

### Monthly
- [ ] Re-rate top 6 operators (`/how-we-rate/`); refresh review pages
- [ ] Review Core Web Vitals; address regressions
- [ ] Add 2-3 new strategy guides per quarter (target cadence)
- [ ] Refresh all "Last updated" stamps on key pages

### Quarterly
- [ ] Full operator re-rate cycle
- [ ] State page refresh (regulatory changes)
- [ ] Annual report update (next: April 2027)
- [ ] Backlink audit + outreach

## Final state at deploy time

- **Total HTML pages:** 741 (sitemap.xml: 739, search index: 739)
- **Total site size:** ~8 MB
- **Schema blocks:** 989+ JSON-LD blocks across all pages, 0 invalid
- **Internal links:** 17,500+ checked, 0 broken (2 JS template-literal false positives)
- **Image alt-text coverage:** 100%
- **Canonical URLs:** 100%
- **Breadcrumbs:** 100% on non-root pages
- **Mobile responsive:** Yes (CSS grid + flexbox throughout)
- **Dark mode:** Yes (toggle in header, CSS variables for full theme support)
- **Search:** Client-side (no backend dependency)
- **Cookie banner:** Yes (dismissible, no third-party trackers by default)
- **Accessibility:** Alt-text 100%, ARIA labels on icon buttons, keyboard navigation supported
- **Performance:** CSS minified (16% reduction), font preload, JS deferred, images lazy-loaded

## Support

- Editorial: editorial@bettingonline.org
- Technical: webmaster@bettingonline.org
- Privacy: privacy@bettingonline.org
- Legal: legal@bettingonline.org
