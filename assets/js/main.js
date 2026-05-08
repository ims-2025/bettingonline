/* =============================================================
   BettingOnline.org — Shared JavaScript
   Builds header/footer, dark mode, search, mobile nav, year stamp.
   Path-aware: works from any depth via data-base or auto-detect.
   ============================================================= */

(function () {
  'use strict';

  // ============================================================
  // INTEGRATION KEYS — replace before going live
  // ============================================================
  // The Odds API: get a free key at https://the-odds-api.com (500 requests/mo on free tier)
  window.BO_ODDS_API_KEY = window.BO_ODDS_API_KEY || 'YOUR_API_KEY_HERE';

  // ---- Path resolution: figure out how to reach site root from current page ----
  // Strategy: use the main.css <link> as the source of truth. Its href is statically
  // generated with the correct relative path from the page back to the site root,
  // so it works regardless of URL scheme (file://, http://, https://) and regardless
  // of how deep the filesystem path is.
  function resolveBase() {
    var meta = document.querySelector('meta[name="site-base"]');
    if (meta && meta.content) return meta.content;
    // Look for the main.css (or main.min.css) stylesheet link
    var links = document.querySelectorAll('link[rel="stylesheet"]');
    for (var i = 0; i < links.length; i++) {
      var href = links[i].getAttribute('href') || '';
      // Match either "assets/css/main.css" or "assets/css/main.min.css"
      var marker = 'assets/css/main';
      var idx = href.indexOf(marker);
      if (idx < 0) continue;
      // Verify the next characters are .css or .min.css (not some other file)
      var rest = href.substring(idx + marker.length);
      if (rest !== '.css' && rest !== '.min.css') continue;
      var prefix = href.substring(0, idx);
      // Handle absolute paths (e.g. "/assets/css/main.css") by returning '/' as base
      if (prefix === '/' || prefix.charAt(0) === '/') return prefix;
      // Handle empty prefix (page at site root)
      if (prefix === '') return './';
      return prefix;
    }
    // Fallback to URL-based computation (works on web servers)
    var path = window.location.pathname;
    var parts = path.replace(/\/$/, '').split('/').filter(Boolean);
    var depth = /\.html?$/i.test(path) ? parts.length - 1 : parts.length;
    if (depth <= 0) return './';
    return new Array(depth + 1).join('../');
  }
  var BASE = resolveBase();
  window.__BO_BASE__ = BASE;

  // Build a link target. Production servers (Vercel) auto-serve index.html for
  // directory paths, so we leave directory paths trailing-slash and skip the
  // explicit index.html. The redirect rule in vercel.json handles legacy
  // /index.html URLs.
  function url(p) {
    p = p.replace(/^\//, '');
    var full = BASE + p;
    // Empty path resolves to BASE (homepage). Trailing slash directory
    // paths are served by Vercel's auto-index.
    if (full === '' || full === BASE) {
      full = BASE; // homepage
    }
    return full;
  }

  // ---- Theme (dark/light) ----
  var THEME_KEY = 'bo-theme';
  function applyTheme(t) {
    document.documentElement.setAttribute('data-theme', t);
    try { localStorage.setItem(THEME_KEY, t); } catch (e) {}
    var btns = document.querySelectorAll('[data-theme-toggle]');
    btns.forEach(function (b) { b.setAttribute('aria-pressed', t === 'dark' ? 'true' : 'false'); });
  }
  function initTheme() {
    var saved;
    try { saved = localStorage.getItem(THEME_KEY); } catch (e) {}
    if (!saved) {
      saved = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
    }
    applyTheme(saved);
  }
  initTheme();

  // ---- Build header ----
  var NAV = {
    sports: {
      label: 'Sports',
      href: 'sports/',
      sections: [
        { title: 'Top Sports', links: [
          ['NFL Football', 'sports/football/'],
          ['NBA Basketball', 'sports/basketball/'],
          ['MLB Baseball', 'sports/baseball/'],
          ['NHL Hockey', 'sports/hockey/'],
          ['Soccer', 'sports/soccer/'],
          ['Tennis', 'sports/tennis/'],
          ['Golf', 'sports/golf/']
        ]},
        { title: 'Combat', links: [
          ['MMA / UFC', 'sports/mma/'],
          ['Boxing', 'sports/boxing/'],
          ['All Combat Sports', 'sports/combat/']
        ]},
        { title: 'Racing & Niche', links: [
          ['Horse Racing', 'sports/horse-racing/'],
          ['Auto Racing', 'sports/auto-racing/'],
          ['eSports', 'sports/esports/'],
          ['Cricket / Rugby', 'sports/cricket-rugby/']
        ]}
      ],
      feature: { title: 'Sportsbook of the Month', text: 'DraftKings — $150 in bonus bets', cta: 'See review', href: 'reviews/draftkings/' }
    },
    casino: {
      label: 'Casino',
      href: 'casino/',
      sections: [
        { title: 'Top Games', links: [
          ['Online Slots', 'casino/slots/'],
          ['Blackjack', 'casino/blackjack/'],
          ['Roulette', 'casino/roulette/'],
          ['Baccarat', 'casino/baccarat/'],
          ['Craps', 'casino/craps/'],
          ['Video Poker', 'casino/video-poker/']
        ]},
        { title: 'Live & Specials', links: [
          ['Live Dealer', 'casino/live-dealer/'],
          ['Game Shows', 'casino/game-shows/'],
          ['Progressive Jackpots', 'casino/progressive-jackpots/']
        ]},
        { title: 'Casinos', links: [
          ['Best Casino Sites', 'casino/best/'],
          ['Casino Bonuses', 'casino/bonuses/'],
          ['Crypto Casinos', 'casino/crypto/'],
          ['Casino Reviews', 'reviews/']
        ]}
      ],
      feature: { title: 'Top Casino Bonus', text: 'Up to $1,000 deposit match + 100 free spins', cta: 'View bonuses', href: 'bonuses/' }
    },
    poker: {
      label: 'Poker',
      href: 'poker/',
      sections: [
        { title: 'Variants', links: [
          ['Texas Hold\'em', 'poker/holdem/'],
          ['Omaha', 'poker/omaha/'],
          ['Stud Poker', 'poker/stud/'],
          ['HORSE / Mixed', 'poker/horse-mixed/']
        ]},
        { title: 'Formats', links: [
          ['Cash Games', 'poker/cash-games/'],
          ['Tournaments', 'poker/tournaments/'],
          ['Sit & Go', 'poker/sit-n-go/'],
          ['Heads-Up', 'poker/heads-up/']
        ]},
        { title: 'Sites & Bonuses', links: [
          ['Best Poker Sites', 'poker/best/'],
          ['Poker Bonuses', 'poker/bonuses/'],
          ['Poker Strategy', 'poker/strategy/']
        ]}
      ],
      feature: { title: 'Top Poker Welcome', text: '100% match up to $1,000 + tournament tickets', cta: 'View offers', href: 'bonuses/' }
    }
  };

  function megaHTML(key, data) {
    var sections = data.sections.map(function (s) {
      return '<div><h5>' + s.title + '</h5>' + s.links.map(function (l) {
        return '<a href="' + url(l[1]) + '">' + l[0] + '</a>';
      }).join('') + '</div>';
    }).join('');
    var feat = data.feature ? (
      '<div class="mega-feature">'
      + '<div><strong>' + data.feature.title + '</strong>'
      + '<div class="muted" style="font-size:.9rem">' + data.feature.text + '</div></div>'
      + '<a class="btn btn-primary btn-sm" href="' + url(data.feature.href) + '">' + data.feature.cta + '</a>'
      + '</div>'
    ) : '';
    return '<div class="mega-grid">' + sections + feat + '</div>';
  }

  function buildHeader() {
    var host = document.querySelector('[data-site-header]');
    if (!host) return;
    var h = ''
      + '<header class="site-header" role="banner">'
      +   '<div class="container">'
      +     '<div class="nav-wrap">'
      +       '<a href="' + url('') + '" class="brand"><span class="brand-mark"></span> BettingOnline.org</a>'
      +       '<nav class="primary-nav" aria-label="Primary">'
      +         '<div class="has-mega"><a class="nav-link" href="' + url(NAV.sports.href) + '">Sports</a><div class="mega">' + megaHTML('sports', NAV.sports) + '</div></div>'
      +         '<div class="has-mega"><a class="nav-link" href="' + url(NAV.casino.href) + '">Casino</a><div class="mega">' + megaHTML('casino', NAV.casino) + '</div></div>'
      +         '<div class="has-mega"><a class="nav-link" href="' + url(NAV.poker.href) + '">Poker</a><div class="mega">' + megaHTML('poker', NAV.poker) + '</div></div>'
      +         '<a href="' + url('reviews/') + '">Reviews</a>'
      +         '<a href="' + url('compare/dk-fd-mgm-3way/') + '">Compare</a>'
      +         '<a href="' + url('bonuses/') + '">Bonuses</a>'
      +         '<a href="' + url('tools/') + '">Tools</a>'
      +         '<a href="' + url('guides/') + '">Guides</a>'
      +       '</nav>'
      +       '<div class="nav-actions">'
      +         '<button class="icon-btn" data-search-open aria-label="Search">' + iconSearch() + '</button>'
      +         '<button class="icon-btn" data-theme-toggle aria-label="Toggle theme" aria-pressed="false">' + iconTheme() + '</button>'
      +         '<a href="' + url('reviews/') + '" class="btn btn-primary btn-sm" style="margin-left:6px">Compare books</a>'
      +         '<button class="icon-btn nav-toggle" data-mobile-open aria-label="Open menu">' + iconMenu() + '</button>'
      +       '</div>'
      +     '</div>'
      +   '</div>'
      + '</header>';
    host.outerHTML = h;
  }

  function iconSearch() { return '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="7"/><path d="M21 21l-4.3-4.3"/></svg>'; }
  function iconTheme() { return '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8z"/></svg>'; }
  function iconMenu() { return '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"><path d="M4 7h16M4 12h16M4 17h16"/></svg>'; }
  function iconClose() { return '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"><path d="M6 6l12 12M18 6L6 18"/></svg>'; }

  // ---- Footer ----
  function buildFooter() {
    var host = document.querySelector('[data-site-footer]');
    if (!host) return;
    var year = new Date().getFullYear();
    var h = ''
      + '<footer class="site-footer" role="contentinfo">'
      +   '<div class="container">'
      +     '<div class="footer-grid">'
      +       '<div class="footer-brand">'
      +         '<a href="' + url('') + '" class="brand" style="color:white"><span class="brand-mark"></span> BettingOnline.org</a>'
      +         '<p>The trusted global guide to online sports betting, casino, and poker since 2003. Independent reviews, comparison tools, and expert strategy.</p>'
      +         '<form class="newsletter" data-nl onsubmit="event.preventDefault();this.querySelector(\'.nl-msg\').textContent=\'Thanks — you\\\'re on the list.\';this.querySelector(\'input\').value=\'\';">'
      +           '<label for="nl-email" style="display:block;color:white;font-weight:600;font-size:.9rem;margin:14px 0 6px">Weekly newsletter</label>'
      +           '<div style="display:flex;gap:6px">'
      +             '<input id="nl-email" type="email" placeholder="you@example.com" required style="flex:1;padding:10px 12px;border-radius:8px;border:none;font-family:inherit;font-size:.92rem">'
      +             '<button class="btn btn-primary" type="submit" style="padding:10px 14px">Subscribe</button>'
      +           '</div>'
      +           '<div class="nl-msg" style="color:rgba(255,255,255,.7);font-size:.78rem;margin-top:6px">No spam. Unsubscribe anytime.</div>'
      +         '</form>'
      +       '</div>'
      +       '<div><h5>Sports</h5>'
      +         '<a href="' + url('sports/football/') + '">NFL</a>'
      +         '<a href="' + url('sports/basketball/') + '">NBA</a>'
      +         '<a href="' + url('sports/baseball/') + '">MLB</a>'
      +         '<a href="' + url('sports/hockey/') + '">NHL</a>'
      +         '<a href="' + url('sports/soccer/') + '">Soccer</a>'
      +         '<a href="' + url('sports/mma/') + '">MMA</a>'
      +       '</div>'
      +       '<div><h5>Casino & Poker</h5>'
      +         '<a href="' + url('casino/slots/') + '">Slots</a>'
      +         '<a href="' + url('casino/blackjack/') + '">Blackjack</a>'
      +         '<a href="' + url('casino/roulette/') + '">Roulette</a>'
      +         '<a href="' + url('poker/holdem/') + '">Texas Hold\'em</a>'
      +         '<a href="' + url('poker/tournaments/') + '">Tournaments</a>'
      +       '</div>'
      +       '<div><h5>Tools</h5>'
      +         '<a href="' + url('tools/parlay/') + '">Parlay calculator</a>'
      +         '<a href="' + url('tools/odds-converter/') + '">Odds converter</a>'
      +         '<a href="' + url('tools/hedge/') + '">Hedge calculator</a>'
      +         '<a href="' + url('tools/ev/') + '">Expected value</a>'
      +         '<a href="' + url('tools/kelly/') + '">Kelly criterion</a>'
      +         '<a href="' + url('tools/arbitrage/') + '">Arbitrage</a>'
      +       '</div>'
      +       '<div><h5>Company</h5>'
      +         '<a href="' + url('about/') + '">About</a>'
      +         '<a href="' + url('methodology/') + '">Methodology</a>'
      +         '<a href="' + url('editorial-standards/') + '">Editorial standards</a>'
      +         '<a href="' + url('how-we-rate/') + '">How we rate</a>'
      +         '<a href="' + url('about/contact.html') + '">Contact</a>'
      +         '<a href="' + url('sitemap.html') + '">Sitemap</a>'
      +       '</div>'
      +       '<div><h5>Legal</h5>'
      +         '<a href="' + url('legal/responsible-gambling.html') + '">Responsible gambling</a>'
      +         '<a href="' + url('legal/privacy.html') + '">Privacy policy</a>'
      +         '<a href="' + url('legal/terms.html') + '">Terms of use</a>'
      +         '<a href="' + url('legal/disclosure.html') + '">Affiliate disclosure</a>'
      +       '</div>'
      +     '</div>'
      +     '<div class="responsible-block">'
      +       '<div><strong style="color:white">Bet responsibly. 21+ where legal.</strong>'
      +       '<div style="color:rgba(255,255,255,.6); font-size:.88rem; margin-top:4px">If you or someone you know has a gambling problem, call <a style="color:white;display:inline" href="tel:1-800-522-4700">1-800-GAMBLER</a> or visit <a style="color:white;display:inline" href="https://www.ncpgambling.org" target="_blank" rel="noopener">ncpgambling.org</a>.</div></div>'
      +       '<div class="badges"><span class="badge">21+</span><span class="badge">RG VERIFIED</span><span class="badge">SSL SECURED</span></div>'
      +     '</div>'
      +     '<div class="footer-bar">'
      +       '<div>© ' + year + ' BettingOnline.org. All rights reserved.</div>'
      +       '<div>Independent betting guide — not affiliated with any operator. Operators referenced for review purposes only.</div>'
      +     '</div>'
      +   '</div>'
      + '</footer>';
    host.outerHTML = h;
  }

  // ---- Mobile drawer ----
  function buildMobileDrawer() {
    if (document.querySelector('.mobile-drawer')) return;
    function items(d) { return d.sections.map(function (s) { return '<details><summary>' + s.title + '</summary>' + s.links.map(function (l) { return '<a href="' + url(l[1]) + '">' + l[0] + '</a>'; }).join('') + '</details>'; }).join(''); }
    var html = ''
      + '<div class="mobile-drawer" data-mobile-drawer>'
      +   '<div class="mobile-panel">'
      +     '<div class="flex-between" style="margin-bottom:8px"><strong>Menu</strong><button class="icon-btn" data-mobile-close aria-label="Close menu">' + iconClose() + '</button></div>'
      +     '<details><summary>Sports</summary><a href="' + url('sports/') + '" style="font-weight:700">All Sports →</a>' + items(NAV.sports) + '</details>'
      +     '<details><summary>Casino</summary><a href="' + url('casino/') + '" style="font-weight:700">All Casino →</a>' + items(NAV.casino) + '</details>'
      +     '<details><summary>Poker</summary><a href="' + url('poker/') + '" style="font-weight:700">All Poker →</a>' + items(NAV.poker) + '</details>'
      +     '<a href="' + url('reviews/') + '">Reviews</a>'
      +     '<a href="' + url('bonuses/') + '">Bonuses</a>'
      +     '<a href="' + url('tools/') + '">Calculators</a>'
      +     '<a href="' + url('guides/') + '">Guides</a>'
      +     '<a href="' + url('news/') + '">News</a>'
      +     '<a href="' + url('about/') + '">About</a>'
      +     '<a class="btn btn-primary mt-2" href="' + url('reviews/') + '">Compare sportsbooks</a>'
      +   '</div>'
      + '</div>';
    document.body.insertAdjacentHTML('beforeend', html);
  }

  // ---- Search popover ----
  var SEARCH_INDEX = null;
  function loadSearchIndex(cb) {
    if (SEARCH_INDEX) return cb(SEARCH_INDEX);
    var x = new XMLHttpRequest();
    x.open('GET', url('assets/js/search-index.json'));
    x.onload = function () {
      try { SEARCH_INDEX = JSON.parse(x.responseText); } catch (e) { SEARCH_INDEX = []; }
      cb(SEARCH_INDEX);
    };
    x.onerror = function () { SEARCH_INDEX = []; cb(SEARCH_INDEX); };
    x.send();
  }
  function buildSearchPopover() {
    if (document.querySelector('.search-popover')) return;
    var html = ''
      + '<div class="search-popover" data-search-popover>'
      +   '<div class="search-box">'
      +     '<div class="search-input-wrap">' + iconSearch()
      +       '<input class="search-input" type="text" placeholder="Search guides, reviews, sports, calculators..." autocomplete="off" data-search-input>'
      +       '<span class="search-kbd">ESC</span>'
      +     '</div>'
      +     '<div class="search-results" data-search-results>'
      +       '<div class="empty">Type to search across the site.</div>'
      +     '</div>'
      +   '</div>'
      + '</div>';
    document.body.insertAdjacentHTML('beforeend', html);
  }
  function runSearch(q, container) {
    q = (q || '').trim().toLowerCase();
    if (!q) { container.innerHTML = '<div class="empty">Type to search across the site.</div>'; return; }
    loadSearchIndex(function (idx) {
      var matches = idx.filter(function (it) {
        var hay = (it.title + ' ' + (it.desc || '') + ' ' + (it.tags || []).join(' ')).toLowerCase();
        return q.split(/\s+/).every(function (term) { return hay.indexOf(term) !== -1; });
      }).slice(0, 12);
      if (!matches.length) { container.innerHTML = '<div class="empty">No matches for "' + escapeHtml(q) + '".</div>'; return; }
      container.innerHTML = matches.map(function (m, i) {
        return '<a class="result' + (i === 0 ? ' active' : '') + '" href="' + url(m.url) + '">'
          + '<div class="result-title">' + escapeHtml(m.title) + '</div>'
          + '<div class="result-desc">' + escapeHtml(m.desc || '') + '</div>'
          + '</a>';
      }).join('');
    });
  }
  function escapeHtml(s) { return String(s).replace(/[&<>"']/g, function (c) { return ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[c]; }); }

  // ---- Wire up after DOM loaded ----
  function ready(fn) { if (document.readyState !== 'loading') fn(); else document.addEventListener('DOMContentLoaded', fn); }
  ready(function () {
    buildHeader();
    buildFooter();
    buildMobileDrawer();
    buildSearchPopover();

    document.body.addEventListener('click', function (e) {
      var t = e.target.closest('[data-theme-toggle]');
      if (t) {
        var cur = document.documentElement.getAttribute('data-theme') || 'light';
        applyTheme(cur === 'dark' ? 'light' : 'dark');
      }
      var mo = e.target.closest('[data-mobile-open]');
      if (mo) document.querySelector('[data-mobile-drawer]').classList.add('open');
      var mc = e.target.closest('[data-mobile-close], [data-mobile-drawer]');
      if (mc && (mc.matches('[data-mobile-close]') || mc.matches('[data-mobile-drawer]') && e.target === mc)) {
        document.querySelector('[data-mobile-drawer]').classList.remove('open');
      }
      var so = e.target.closest('[data-search-open]');
      if (so) { var p = document.querySelector('[data-search-popover]'); p.classList.add('open'); var i = p.querySelector('[data-search-input]'); setTimeout(function(){ i.focus(); }, 30); }
      var sp = e.target.closest('[data-search-popover]');
      if (sp && e.target === sp) sp.classList.remove('open');
    });

    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') {
        var p = document.querySelector('[data-search-popover]'); if (p) p.classList.remove('open');
        var d = document.querySelector('[data-mobile-drawer]'); if (d) d.classList.remove('open');
      }
      if ((e.key === 'k' || e.key === 'K') && (e.metaKey || e.ctrlKey)) {
        e.preventDefault();
        var pp = document.querySelector('[data-search-popover]');
        pp.classList.add('open');
        var ii = pp.querySelector('[data-search-input]');
        setTimeout(function(){ ii.focus(); }, 30);
      }
    });

    var input = document.querySelector('[data-search-input]');
    if (input) {
      var t;
      input.addEventListener('input', function () {
        clearTimeout(t);
        var v = input.value;
        var c = document.querySelector('[data-search-results]');
        t = setTimeout(function () { runSearch(v, c); }, 80);
      });
      input.addEventListener('keydown', function (e) {
        if (e.key === 'Enter') {
          var r = document.querySelector('[data-search-results] .result.active') || document.querySelector('[data-search-results] .result');
          if (r) window.location.href = r.href;
        }
        if (e.key === 'ArrowDown' || e.key === 'ArrowUp') {
          e.preventDefault();
          var rs = Array.prototype.slice.call(document.querySelectorAll('[data-search-results] .result'));
          if (!rs.length) return;
          var idx = rs.findIndex(function (r) { return r.classList.contains('active'); });
          rs.forEach(function (r) { r.classList.remove('active'); });
          idx = e.key === 'ArrowDown' ? Math.min(rs.length - 1, idx + 1) : Math.max(0, idx - 1);
          if (idx < 0) idx = 0;
          rs[idx].classList.add('active');
          rs[idx].scrollIntoView({ block: 'nearest' });
        }
      });
    }

    // Hide auto-active state when user navigates
    document.querySelectorAll('.primary-nav > a').forEach(function (a) {
      try {
        var href = new URL(a.getAttribute('href'), window.location.href).pathname;
        if (window.location.pathname.indexOf(href) === 0 && href.length > 1) a.classList.add('active');
      } catch (e) {}
    });
  });
})();

/* ============================================================
   CALCULATORS — small pure-JS utilities, called by tool pages.
   ============================================================ */
window.BO_CALC = (function () {
  'use strict';

  // American → decimal
  function americanToDecimal(a) {
    a = parseFloat(a);
    if (!isFinite(a) || a === 0) return NaN;
    return a > 0 ? 1 + a / 100 : 1 + 100 / Math.abs(a);
  }
  function decimalToAmerican(d) {
    d = parseFloat(d);
    if (!isFinite(d) || d <= 1) return NaN;
    return d >= 2 ? Math.round((d - 1) * 100) : -Math.round(100 / (d - 1));
  }
  function fractionalToDecimal(f) {
    if (!f) return NaN;
    var m = String(f).split('/');
    if (m.length !== 2) return NaN;
    var n = parseFloat(m[0]), de = parseFloat(m[1]);
    if (!isFinite(n) || !isFinite(de) || de === 0) return NaN;
    return 1 + n / de;
  }
  function decimalToFractional(d) {
    d = parseFloat(d);
    if (!isFinite(d) || d <= 1) return '—';
    var num = d - 1;
    // approximate to nice fraction
    var den = 1;
    while ((num * den) % 1 > 0.0001 && den < 1000) den++;
    var n = Math.round(num * den);
    var g = gcd(n, den);
    return (n / g) + '/' + (den / g);
  }
  function gcd(a, b) { return b ? gcd(b, a % b) : a; }
  function impliedProb(d) {
    d = parseFloat(d);
    if (!isFinite(d) || d <= 0) return NaN;
    return 1 / d;
  }

  // Parlay payout from list of {odds: american, stake?}
  function parlay(legs, stake) {
    var combined = 1;
    for (var i = 0; i < legs.length; i++) {
      var d = americanToDecimal(legs[i]);
      if (!isFinite(d)) return null;
      combined *= d;
    }
    var payout = stake * combined;
    return { decimal: combined, payout: payout, profit: payout - stake, american: decimalToAmerican(combined) };
  }

  // Hedge: original bet at stake, original odds (American). Opposite side at hedgeOdds (American).
  // Returns hedge stake to equalize payout, plus guaranteed profit.
  function hedge(originalStake, originalOdds, hedgeOdds) {
    var od = americanToDecimal(originalOdds);
    var hd = americanToDecimal(hedgeOdds);
    if (!isFinite(od) || !isFinite(hd)) return null;
    var origPayout = originalStake * od; // includes stake
    var hedgeStake = origPayout / hd;
    var totalRisk = originalStake + hedgeStake;
    var guaranteed = origPayout - totalRisk;
    return { hedgeStake: hedgeStake, guaranteedProfit: guaranteed, totalRisk: totalRisk, origPayoutIfWin: origPayout, hedgePayoutIfWin: hedgeStake * hd };
  }

  // Expected value
  // winProbability (0-1), odds (American), stake
  // EV = (p * profitIfWin) - ((1-p) * stake)
  function ev(prob, odds, stake) {
    var d = americanToDecimal(odds);
    if (!isFinite(d) || prob < 0 || prob > 1) return null;
    var profit = stake * (d - 1);
    return { ev: prob * profit - (1 - prob) * stake, profitIfWin: profit, breakEvenProb: 1 / d };
  }

  // Kelly criterion
  // f* = (bp - q) / b, where b = decimalOdds - 1, p = win prob, q = 1-p
  function kelly(prob, odds, bankroll, fraction) {
    var d = americanToDecimal(odds);
    if (!isFinite(d) || prob < 0 || prob > 1) return null;
    var b = d - 1;
    var k = (b * prob - (1 - prob)) / b;
    var clamped = Math.max(0, k);
    var f = (typeof fraction === 'number' && fraction > 0) ? fraction : 1;
    return {
      fullKelly: clamped,
      fractionalKelly: clamped * f,
      betAmount: bankroll * clamped * f,
      edge: prob * d - 1
    };
  }

  // Arbitrage: two opposing odds (American). Returns whether arb exists, stakes for $X total bankroll, profit %.
  function arbitrage(oddsA, oddsB, total) {
    var a = americanToDecimal(oddsA);
    var b = americanToDecimal(oddsB);
    if (!isFinite(a) || !isFinite(b)) return null;
    var inv = 1/a + 1/b;
    var stakeA = total * (1/a) / inv;
    var stakeB = total * (1/b) / inv;
    var payout = stakeA * a; // equals stakeB * b
    return {
      arb: inv < 1,
      arbPercent: (1 - inv) * 100,
      stakeA: stakeA, stakeB: stakeB,
      guaranteedPayout: payout,
      profit: payout - total
    };
  }

  return {
    americanToDecimal: americanToDecimal,
    decimalToAmerican: decimalToAmerican,
    fractionalToDecimal: fractionalToDecimal,
    decimalToFractional: decimalToFractional,
    impliedProb: impliedProb,
    parlay: parlay,
    hedge: hedge,
    ev: ev,
    kelly: kelly,
    arbitrage: arbitrage
  };
})();


// Cookie consent banner — uses localStorage primarily (works on file:// and https://),
// falls back to cookies for cross-subdomain scenarios on real deploys.
(function(){
  if (typeof window === 'undefined') return;

  var KEY = 'bo_cookie_consent';

  function getConsent(){
    try {
      var ls = window.localStorage && window.localStorage.getItem(KEY);
      if (ls) return ls;
    } catch(e){}
    try {
      var match = document.cookie.split(';').find(function(c){ return c.trim().indexOf(KEY+'=') === 0; });
      if (match) return match.split('=')[1];
    } catch(e){}
    return null;
  }

  function saveConsent(value){
    try { window.localStorage && window.localStorage.setItem(KEY, value); } catch(e){}
    try {
      var d = new Date();
      d.setTime(d.getTime() + 365 * 24 * 60 * 60 * 1000);
      document.cookie = KEY + '=' + value + ';expires=' + d.toUTCString() + ';path=/;SameSite=Lax';
    } catch(e){}
  }

  // Expose a reset utility for users / debugging — call window.__BO_resetConsent__()
  window.__BO_resetConsent__ = function(){
    try { window.localStorage && window.localStorage.removeItem(KEY); } catch(e){}
    try { document.cookie = KEY + '=;expires=Thu, 01 Jan 1970 00:00:00 GMT;path=/'; } catch(e){}
    location.reload();
  };

  // URL-based override for testing: append ?reset-consent=1 to any URL to clear stored consent
  try {
    if (location.search.indexOf('reset-consent') !== -1) {
      try { window.localStorage && window.localStorage.removeItem(KEY); } catch(e){}
      try { document.cookie = KEY + '=;expires=Thu, 01 Jan 1970 00:00:00 GMT;path=/'; } catch(e){}
    }
  } catch(e){}

  if (getConsent()) return;

  function build(){
    if (!document.body) { setTimeout(build, 50); return; }
    if (document.querySelector('.cookie-banner')) return;
    var banner = document.createElement('div');
    banner.className = 'cookie-banner show';
    banner.setAttribute('role', 'dialog');
    banner.setAttribute('aria-label', 'Cookie consent');
    banner.innerHTML =
      '<p>We use minimal first-party cookies for theme preference and affiliate attribution. No third-party tracking. <a href="' + url('legal/privacy.html') + '">Privacy policy</a>.</p>' +
      '<div class="cookie-actions">' +
        '<button type="button" class="cookie-btn cookie-btn-secondary" data-cookie-action="reject">Reject</button>' +
        '<button type="button" class="cookie-btn cookie-btn-primary" data-cookie-action="accept">Accept</button>' +
      '</div>';
    document.body.appendChild(banner);

    function dismiss(value){
      saveConsent(value);
      banner.classList.remove('show');
      setTimeout(function(){ try { banner.parentNode && banner.parentNode.removeChild(banner); } catch(e){} }, 200);
    }
    banner.querySelector('[data-cookie-action="accept"]').addEventListener('click', function(){ dismiss('accepted'); });
    banner.querySelector('[data-cookie-action="reject"]').addEventListener('click', function(){ dismiss('rejected'); });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', build);
  } else {
    build();
  }
})();
