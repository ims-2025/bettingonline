#!/usr/bin/env python3
"""Swap the 'Top X Casino sites' sidebar cards on casino sub-pages.

The main builder handled the .book-table pattern (found on /casino/index.html).
Sub-pages use a smaller sidebar card widget with .flex-between rows — this
script targets that specific pattern.
"""
from __future__ import annotations

import html
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CASINO = ROOT / "casino"

# Import brand data
import importlib.util
spec = importlib.util.spec_from_file_location("bcb", ROOT / "scripts" / "build-casino-brands.py")
bcb = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bcb)
BRANDS = bcb.BRANDS


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


# Match the whole sidebar card whose heading includes "Top … Casino" or
# "Best … casinos" AND whose first link references an old casino brand.
CARD_PATTERN = re.compile(
    r'          <div class="card mb-3"[^>]*>\s*\n'
    r'            <h4 class="mt-0">(?:Top|Best)\s+[^<]*(?:[Cc]asino|[Ss]ites)[^<]*</h4>.*?'
    r'</div>\s*\n          </div>',
    re.S,
)


def main() -> None:
    updated = 0
    for path in sorted(CASINO.rglob("index.html")):
        if path == CASINO / "index.html":
            continue  # hub already handled by main builder
        text = path.read_text()
        depth = len(path.relative_to(ROOT).parts) - 1
        new_sidebar = sidebar_html(depth)

        def maybe_replace(m):
            block = m.group(0)
            # Only touch cards whose first ~2 rows include a known old
            # casino brand — leave any sportsbook/poker toplist alone.
            if re.search(
                r'BetMGM Casino|Caesars Palace|DraftKings Casino|FanDuel Casino|'
                r'BetRivers Casino|Golden Nugget|WynnBET|Borgata Casino|888 Casino',
                block,
            ):
                return new_sidebar
            return block

        text2 = CARD_PATTERN.sub(maybe_replace, text)
        if text2 != text:
            path.write_text(text2)
            print(f"  swapped: {path.relative_to(ROOT)}")
            updated += 1
    print(f"Total: {updated} sidebars updated")

    subprocess.run(["git", "-C", str(ROOT), "add", "-A"], check=True)


if __name__ == "__main__":
    main()
