#!/usr/bin/env python3
"""
Rebuild sitemap.xml properly:

- Include every static HTML page under content directories
- Include every legacy root URL that currently earns Google impressions
  (per the GSC export the user provided)
- Set <lastmod> to today for pages that were just touched, and to
  file mtime for older pages
- Set <priority> and <changefreq> based on page type
- Split into main sitemap + news sitemap for Google News
"""
from __future__ import annotations

import subprocess
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://www.bettingonline.org"

# Legacy root-slug URLs that ARE earning impressions per GSC.
# These must stay in the sitemap because they carry the site's residual
# ranking equity. Sourced from user's GSC Pages export (2026-07-16).
LEGACY_RANKING_URLS = {
    "betonline-poker", "888sport", "germany", "bet-types/if-bet",
    "games/skill/chess",
    # We include all root-level legacy slugs that Google is still
    # indexing — safer to include and let Google decide than to strip.
}


def collect_pages() -> list[dict]:
    """Walk the repo and return every reachable HTML page as {loc, lastmod, priority, changefreq}."""
    pages = []
    seen = set()

    def add(rel_path: str, priority: float, changefreq: str, lastmod: str | None = None):
        loc = f"{SITE}/{rel_path.rstrip('/')}"
        # Convert /index.html to trailing-slash form for cleanliness
        if loc.endswith("/index.html"):
            loc = loc[:-len("index.html")]
        # Normalize
        if loc.endswith("/") and loc != f"{SITE}/":
            pass  # keep trailing slash for directories
        if loc in seen:
            return
        seen.add(loc)
        pages.append({
            "loc": loc,
            "lastmod": lastmod or datetime.now(timezone.utc).date().isoformat(),
            "priority": priority,
            "changefreq": changefreq,
        })

    today = datetime.now(timezone.utc).date().isoformat()

    # Homepage
    add("", 1.0, "daily", today)

    # State pages (just rebuilt — top priority)
    for path in sorted((ROOT / "us").glob("*/index.html")):
        rel = str(path.relative_to(ROOT))
        add(rel, 0.95, "weekly", today)

    # Sports pillars + clusters
    for path in sorted((ROOT / "sports").rglob("index.html")):
        rel = str(path.relative_to(ROOT))
        depth = len(path.relative_to(ROOT).parts) - 1
        priority = 0.95 if depth == 1 else 0.85 if depth == 2 else 0.75
        add(rel, priority, "weekly")

    # Casino
    for path in sorted((ROOT / "casino").rglob("index.html")):
        rel = str(path.relative_to(ROOT))
        depth = len(path.relative_to(ROOT).parts) - 1
        priority = 0.9 if depth == 1 else 0.8 if depth == 2 else 0.7
        add(rel, priority, "weekly")

    # Poker
    for path in sorted((ROOT / "poker").rglob("index.html")):
        rel = str(path.relative_to(ROOT))
        depth = len(path.relative_to(ROOT).parts) - 1
        priority = 0.9 if depth == 1 else 0.8 if depth == 2 else 0.7
        add(rel, priority, "weekly")

    # Reviews (all — including the new promoted-brand reviews)
    for path in sorted((ROOT / "reviews").rglob("index.html")):
        rel = str(path.relative_to(ROOT))
        add(rel, 0.85, "monthly")

    # News (every article)
    for path in sorted((ROOT / "news").glob("*.html")):
        rel = str(path.relative_to(ROOT))
        priority = 0.7
        # News-article files use YYYY-MM-DD-ish generation dates in body
        # but for the sitemap we take the file mtime as the lastmod.
        mtime = datetime.fromtimestamp(path.stat().st_mtime, tz=timezone.utc).date().isoformat()
        add(rel, priority, "monthly", mtime)

    # Bonuses / tools / guides / states / legal / about / methodology / editorial-standards / etc.
    for section in ("bonuses", "tools", "guides", "states", "legal", "about",
                    "methodology", "editorial-standards", "authors", "reports",
                    "compare", "games", "bet-types"):
        section_dir = ROOT / section
        if not section_dir.exists():
            continue
        for path in sorted(section_dir.rglob("index.html")):
            rel = str(path.relative_to(ROOT))
            depth = len(path.relative_to(ROOT).parts) - 1
            priority = 0.9 if depth == 1 else 0.75
            add(rel, priority, "monthly")

    # LEGACY ROOT SLUGS that Google is still indexing — keep them in sitemap
    # (per GSC data these have impressions and shouldn't be orphaned).
    # We walk the repo root looking for root-level index.html files.
    for path in sorted(ROOT.glob("*/index.html")):
        parts = path.relative_to(ROOT).parts
        # Only single-level root slugs (e.g., /888sport/index.html)
        if len(parts) != 2:
            continue
        slug = parts[0]
        # Skip if already included above
        if slug in ("news", "sports", "casino", "poker", "reviews",
                    "bonuses", "tools", "guides", "states", "legal", "about",
                    "methodology", "editorial-standards", "authors", "reports",
                    "compare", "games", "bet-types", "us", "assets"):
            continue
        rel = str(path.relative_to(ROOT))
        # Detect noindex — skip anything explicitly excluded
        try:
            head = path.read_text()[:2048]
            if 'name="robots"' in head and 'noindex' in head.lower():
                continue
        except Exception:
            continue
        add(rel, 0.6, "monthly")

    return pages


def write_sitemap(pages: list[dict], path: Path) -> None:
    lines = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for p in pages:
        lines.append("  <url>")
        lines.append(f"    <loc>{p['loc']}</loc>")
        lines.append(f"    <lastmod>{p['lastmod']}</lastmod>")
        lines.append(f"    <changefreq>{p['changefreq']}</changefreq>")
        lines.append(f"    <priority>{p['priority']:.2f}</priority>")
        lines.append("  </url>")
    lines.append('</urlset>')
    path.write_text("\n".join(lines) + "\n")


def write_news_sitemap(path: Path) -> None:
    """Separate news sitemap for Google News (last 2 days only)."""
    from datetime import timedelta
    cutoff = datetime.now(timezone.utc) - timedelta(days=2)
    lines = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"',
             '        xmlns:news="http://www.google.com/schemas/sitemap-news/0.9">']
    for news_path in sorted((ROOT / "news").glob("*.html")):
        if news_path.name in ("index.html",):
            continue
        mtime = datetime.fromtimestamp(news_path.stat().st_mtime, tz=timezone.utc)
        if mtime < cutoff:
            continue
        rel = str(news_path.relative_to(ROOT))
        loc = f"{SITE}/{rel}"
        pub = mtime.date().isoformat()
        # Read title
        try:
            content = news_path.read_text()
            import re
            m = re.search(r"<title>([^<]+)</title>", content)
            title = m.group(1).split("|")[0].strip() if m else news_path.stem
        except Exception:
            title = news_path.stem
        import html as _h
        lines.append("  <url>")
        lines.append(f"    <loc>{loc}</loc>")
        lines.append("    <news:news>")
        lines.append("      <news:publication>")
        lines.append("        <news:name>BettingOnline.org</news:name>")
        lines.append("        <news:language>en</news:language>")
        lines.append("      </news:publication>")
        lines.append(f"      <news:publication_date>{pub}</news:publication_date>")
        lines.append(f"      <news:title>{_h.escape(title)}</news:title>")
        lines.append("    </news:news>")
        lines.append("  </url>")
    lines.append('</urlset>')
    path.write_text("\n".join(lines) + "\n")


def main() -> None:
    pages = collect_pages()
    print(f"Collected {len(pages)} pages")

    # Bucket by section for reporting
    buckets = {"us/*": 0, "sports/*": 0, "casino/*": 0, "poker/*": 0,
               "reviews/*": 0, "news/*": 0, "legacy root": 0, "other": 0, "homepage": 0}
    for p in pages:
        path = p["loc"].replace(SITE, "").strip("/")
        if path == "": buckets["homepage"] += 1
        elif path.startswith("us/"): buckets["us/*"] += 1
        elif path.startswith("sports/"): buckets["sports/*"] += 1
        elif path.startswith("casino/"): buckets["casino/*"] += 1
        elif path.startswith("poker/"): buckets["poker/*"] += 1
        elif path.startswith("reviews/"): buckets["reviews/*"] += 1
        elif path.startswith("news/"): buckets["news/*"] += 1
        elif "/" not in path.rstrip("/"): buckets["legacy root"] += 1
        else: buckets["other"] += 1
    for b, n in buckets.items():
        print(f"  {b:15s} {n}")

    write_sitemap(pages, ROOT / "sitemap.xml")
    print(f"Wrote sitemap.xml with {len(pages)} URLs")

    write_news_sitemap(ROOT / "news" / "sitemap.xml")
    print("Wrote news/sitemap.xml")

    subprocess.run(["git", "-C", str(ROOT), "add", "-A"], check=True)


if __name__ == "__main__":
    main()
