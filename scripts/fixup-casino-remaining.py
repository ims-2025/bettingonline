#!/usr/bin/env python3
"""Final casino-toplist fixup.

Two remaining categories to handle:

1. Casino pages that carry a sidebar card with old sportsbook brands
   (DraftKings / FanDuel / BetMGM / Caesars) — that's a misplaced sportsbook
   toplist on a casino page. Swap it for the 3-brand casino sidebar.

2. Casino /best/ and /bonuses/ pillar pages — huge editorial ranking
   articles that are themselves toplists. Insert a compact 'Editor's
   promoted casinos' block near the top, above the fold, so the promoted
   brands lead the page even though the deeper US-regulated-market
   analysis below remains as informational reference.
"""
from __future__ import annotations

import html
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CASINO = ROOT / "casino"

import importlib.util
spec = importlib.util.spec_from_file_location("bcb", ROOT / "scripts" / "build-casino-brands.py")
bcb = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bcb)
BRANDS = bcb.BRANDS


# ---------------------------------------------------------------------------
def sidebar_html(depth: int) -> str:
    up = "../" * depth
    items = []
    for b in BRANDS:
        items.append(
            f'              <a href="{b["tracker"]}" rel="sponsored nofollow" target="_blank" '
            f'data-affiliate-brand="{b["slug"]}" class="flex-between" '
            f'style="padding:10px; border-radius:10px; background:var(--surface-2)">'
            f'<div><strong>{b["display_name"]}</strong><br>'
            f'<small class="muted">{html.escape(b["bonus_short"][:44])}</small></div>'
            f'<span class="tag primary">Play →</span></a>'
        )
    items_html = "\n".join(items)
    return f"""          <div class="card mb-3">
            <h4 class="mt-0">Top casinos</h4>
            <div style="display:flex; flex-direction:column; gap:10px">
{items_html}
            </div>
            <a href="{up}reviews/" class="btn btn-primary btn-block mt-2">All casino reviews</a>
          </div>"""


def promoted_hero_block() -> str:
    """Prominent block for the top of /casino/best/ and /casino/bonuses/."""
    rows = []
    for i, b in enumerate(BRANDS, 1):
        rank_class = "gold" if i == 1 else "silver" if i == 2 else "bronze"
        features = "".join(f'<span class="tag">{html.escape(t)}</span>' for t in b["tags"])
        rows.append(f"""
        <div class="book-row">
          <div class="rank-pill {rank_class}">{i}</div>
          <div class="book-name"><div class="book-logo" style="background:{b['logo_bg']}; color:{b['logo_fg']}">{b['initials']}</div><div class="name-text"><strong>{b['display_name']}</strong><span>{html.escape(b['tagline'])}</span></div></div>
          <div class="bonus">{html.escape(b['bonus_short'])}</div>
          <div class="rating"><span class="stars">★★★★★</span> {b['rating']}</div>
          <div class="features">{features}</div>
          <div class="cta"><a class="btn btn-primary btn-sm" href="{b['tracker']}" rel="sponsored nofollow" target="_blank" data-affiliate-brand="{b['slug']}">Play at {b['short']} →</a></div>
        </div>""")
    return f"""
  <section class="section" id="editor-promoted">
    <div class="container">
      <h2>Editor's promoted casinos</h2>
      <p class="muted">Our editorial team's promoted casinos, in ranked order. Affiliate disclosure: we may earn a commission from CTA signups — ranking is independent. Below this section: the broader US-regulated market analysis for reference.</p>
      <div class="book-table">
        <div class="book-row head"><div>#</div><div>Casino</div><div>Welcome offer</div><div>Rating</div><div>Highlights</div><div></div></div>{''.join(rows)}
      </div>
      <p class="muted" style="font-size:.82rem; margin-top:8px">18+ / 21+ where required. Play responsibly.</p>
    </div>
  </section>
"""


# ---------------------------------------------------------------------------
# 1. Swap old-sportsbook-brand sidebars on casino pages
# ---------------------------------------------------------------------------
OLD_BRAND_PATTERN = re.compile(
    r'DraftKings|FanDuel|BetMGM|Caesars|BetRivers|Golden Nugget|WynnBET|Borgata',
)

SIDEBAR_CARD_PATTERN = re.compile(
    r'          <div class="card mb-3"[^>]*>\s*\n'
    r'            <h4 class="mt-0">(?:Top|Best)\s+[^<]*</h4>.*?'
    r'</div>\s*\n          </div>',
    re.S,
)


def swap_misplaced_sidebars() -> int:
    updated = 0
    for path in sorted(CASINO.rglob("index.html")):
        text = path.read_text()
        depth = len(path.relative_to(ROOT).parts) - 1
        new_sidebar = sidebar_html(depth)

        def maybe_replace(m):
            block = m.group(0)
            if OLD_BRAND_PATTERN.search(block):
                return new_sidebar
            return block

        text2 = SIDEBAR_CARD_PATTERN.sub(maybe_replace, text)
        if text2 != text:
            path.write_text(text2)
            print(f"  sidebar swapped: {path.relative_to(ROOT)}")
            updated += 1
    return updated


# ---------------------------------------------------------------------------
# 2. Add editor's promoted block near top of /casino/best/ and /bonuses/
# ---------------------------------------------------------------------------
def add_promoted_block(path: Path) -> None:
    text = path.read_text()
    if 'id="editor-promoted"' in text:
        print(f"  already has editor-promoted block: {path.relative_to(ROOT)}")
        return
    # Insert right after the page-hero <section> closes
    pattern = re.compile(r'(<section class="page-hero"[^>]*>.*?</section>\s*\n)', re.S)
    text2, n = pattern.subn(lambda m: m.group(1) + promoted_hero_block(), text, count=1)
    if n == 0:
        print(f"  WARN: could not locate page-hero on {path.relative_to(ROOT)}")
        return
    path.write_text(text2)
    print(f"  editor-promoted block added: {path.relative_to(ROOT)}")


# ---------------------------------------------------------------------------
def main() -> None:
    print("Phase 1: swap misplaced sportsbook sidebars on casino pages...")
    n = swap_misplaced_sidebars()
    print(f"  {n} pages updated\n")

    print("Phase 2: add Editor's promoted casinos block to pillar pages...")
    add_promoted_block(CASINO / "best" / "index.html")
    add_promoted_block(CASINO / "bonuses" / "index.html")

    subprocess.run(["git", "-C", str(ROOT), "add", "-A"], check=True)


if __name__ == "__main__":
    main()
