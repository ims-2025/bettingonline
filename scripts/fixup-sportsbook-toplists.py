#!/usr/bin/env python3
"""Fixup pass: patch the homepage hero aside and the NFL/NBA/MLB pillar
Play-Now tables that build-sportsbook-brands.py missed."""
from __future__ import annotations

import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Import brand data from the main builder to stay in sync
import importlib.util
spec = importlib.util.spec_from_file_location("bsb", ROOT / "scripts" / "build-sportsbook-brands.py")
bsb = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bsb)
BRANDS = bsb.BRANDS


# --- Homepage hero aside ------------------------------------------------------
def fix_homepage_hero() -> None:
    path = ROOT / "index.html"
    text = path.read_text()

    # Match all 4 old row-link blocks (DK/FD/BetMGM/Caesars) as one span.
    # Anchor on the "LIVE" span closing and the "See full leaderboard" button.
    old_rows_pattern = re.compile(
        r'(<span class="live-pulse"[^>]*>.*?LIVE</span>\s*</div>\s*\n)'
        r'(?:\s*<a href="go/[^"]+"[^>]*class="row-link"[^>]*>.*?</div>\s*)+'
        r'(\s*<a href="reviews/" class="btn btn-primary btn-block")',
        re.S,
    )

    new_rows = "\n".join(bsb.hero_aside_html().splitlines()) + "\n"

    text2, n = old_rows_pattern.subn(
        lambda m: m.group(1) + new_rows + m.group(2), text, count=1
    )
    if n == 0:
        print("  WARN: hero aside pattern still didn't match")
        return
    path.write_text(text2)
    print(f"  homepage hero aside updated ({n} match)")


# --- Sport pillars (NFL / NBA / MLB) — .ranked-book pattern ------------------
def sport_pillar_ranked_html(sport: str, depth: int) -> str:
    up = "../" * depth
    rows = []
    for i, b in enumerate(BRANDS, 1):
        # ranked-book uses .rank + name/desc + buttons column
        desc = f"{b['tagline']} Current offer: {b['bonus_short']}."
        rows.append(f"""        <div class="ranked-book">
          <div class="rank">{i}</div>
          <div>
            <p class="name">{b['display_name']}</p>
            <p class="desc">{desc}</p>
          </div>
          <div style="display:flex;flex-direction:column;gap:6px;min-width:120px"><a href="{b['tracker']}" rel="sponsored nofollow" target="_blank" data-affiliate-brand="{b['slug']}" class="btn btn-primary btn-sm" style="font-weight:700">Bet Now</a><a href="{up}reviews/{b['slug']}/" class="btn btn-ghost btn-sm">Review →</a></div>
        </div>""")
    intro = f"        <p>Our editorial team's ranked sportsbooks for {sport} betting. Affiliate disclosure: we may earn commission from CTA signups — ranking independent.</p>"
    return intro + "\n\n" + "\n\n".join(rows)


def fix_sport_pillar(pillar_path: Path, sport: str) -> None:
    text = pillar_path.read_text()

    # Match the ranked-book cluster inside the pillar.
    # From the first <div class="ranked-book"> through the closing </div>
    # of the last old ranked-book block.
    pattern = re.compile(
        r'(<h2[^>]*id="books"[^>]*>[^<]*</h2>\s*\n\s*<p>[^<]*(?:line shopping|line-shopping)[^<]*</p>\s*\n)'
        r'(\s*<div class="ranked-book">.*?</div>\s*\n\s*</div>\s*\n\s*)+',
        re.S,
    )
    depth = len(pillar_path.relative_to(ROOT).parts) - 1
    new = "\n\n" + sport_pillar_ranked_html(sport, depth) + "\n"
    text2, n = pattern.subn(
        lambda m: m.group(1).rstrip() + new, text, count=1
    )
    if n == 0:
        # Simpler fallback: match the whole sequence of ranked-book blocks
        pat2 = re.compile(
            r'(\s*<div class="ranked-book">.*?</div>\s*\n\s*</div>\s*\n\s*){2,}',
            re.S,
        )
        text2, n = pat2.subn(new, text, count=1)
    if n == 0:
        print(f"  WARN: {pillar_path.relative_to(ROOT)} ranked-book not matched")
        return
    pillar_path.write_text(text2)
    print(f"  {pillar_path.relative_to(ROOT)} updated ({n} match)")


def main() -> None:
    print("Fixing homepage hero aside...")
    fix_homepage_hero()

    print("Fixing sport pillar Play-Now tables...")
    fix_sport_pillar(ROOT / "sports" / "football" / "index.html", "NFL")
    fix_sport_pillar(ROOT / "sports" / "basketball" / "index.html", "NBA")
    fix_sport_pillar(ROOT / "sports" / "baseball" / "index.html", "MLB")

    subprocess.run(["git", "-C", str(ROOT), "add", "-A"], check=True)


if __name__ == "__main__":
    main()
