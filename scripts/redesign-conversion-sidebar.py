#!/usr/bin/env python3
"""Redesign the inner-page conversion sidebar sitewide.

The old sidebar was low-contrast (blue on white, flat cards, a Play "tag"
that read as a label rather than a button). This script generates a new
sidebar with:

- Dark gradient header block ("Editor's Picks" + product-line title)
- Ranked cards with gold/silver/bronze badges
- Brand-color left border stripe on each card
- Compact brand info: logo initials + name + bonus + star rating
- High-contrast amber/orange gradient CTA button (contrasts with site's blue)
- Subtle shadow and hover lift baked into inline styles

Then it walks poker/, casino/, and sports/ (poker + casino subpages carry
sidebars; sportsbook sidebars live on poker pages already updated by
earlier scripts) and replaces every existing sidebar card in place.
"""
from __future__ import annotations

import html
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Import brand data from each builder
import importlib.util


def _load(mod_name: str, filename: str):
    spec = importlib.util.spec_from_file_location(mod_name, ROOT / "scripts" / filename)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


CASINO = _load("bcb", "build-casino-brands.py")
SPORTSBOOK = _load("bsb", "build-sportsbook-brands.py")
POKER = _load("bpb", "build-poker-brands.py")


# ---------------------------------------------------------------------------
# New sidebar renderer
# ---------------------------------------------------------------------------
RANK_COLORS = {
    1: ("#FFB800", "#F59E0B", "#78350F"),   # gold: bg-from, bg-to, text
    2: ("#D1D5DB", "#9CA3AF", "#1F2937"),   # silver
    3: ("#D97706", "#B45309", "#FFFFFF"),   # bronze
}


def render_sidebar(brands: list[dict], product_title: str, product_slug: str, depth: int) -> str:
    """Return the full replacement HTML for a sidebar card.

    depth = number of ../ from the current page up to site root
    (used to build the "All reviews" link).
    """
    up = "../" * depth
    accent_from = "#F59E0B"   # amber-500
    accent_to = "#EA580C"     # orange-600

    rows = []
    for i, b in enumerate(brands, 1):
        # Rank badge colors
        rc_from, rc_to, rc_fg = RANK_COLORS.get(i, ("#E5E7EB", "#D1D5DB", "#374151"))
        rank_badge = (
            f'<div style="width:28px;height:28px;border-radius:8px;'
            f'background:linear-gradient(135deg,{rc_from},{rc_to});color:{rc_fg};'
            f'display:flex;align-items:center;justify-content:center;'
            f'font-weight:800;font-size:.85rem;flex-shrink:0;'
            f'box-shadow:0 2px 4px rgba(0,0,0,.15)">{i}</div>'
        )

        # Brand logo
        logo = (
            f'<div style="width:36px;height:36px;border-radius:8px;'
            f'background:{b["logo_bg"]};color:{b["logo_fg"]};'
            f'display:flex;align-items:center;justify-content:center;'
            f'font-weight:800;font-size:.85rem;flex-shrink:0;'
            f'font-family:var(--font-display, Inter, sans-serif)">{b["initials"]}</div>'
        )

        # Star rating (converts rating to filled/empty stars)
        rating = b.get("rating", 4.5)
        stars_full = int(rating)
        has_half = (rating - stars_full) >= 0.25
        stars_str = "★" * stars_full + ("½" if has_half else "")

        # Get the appropriate display name / bonus_short
        name = b.get("display_name") or b.get("name")
        bonus_short = b.get("bonus_short") or b.get("bonus", "")
        # Truncate bonus to keep the row compact
        if len(bonus_short) > 44:
            bonus_short = bonus_short[:42] + "…"

        # "Ranked #1" ribbon on top pick
        ribbon = ""
        if i == 1:
            ribbon = (
                '<div style="position:absolute;top:-8px;right:12px;'
                'background:linear-gradient(135deg,#FFB800,#F59E0B);'
                'color:#78350F;font-size:.62rem;font-weight:800;'
                'padding:3px 8px;border-radius:6px;letter-spacing:.05em;'
                'text-transform:uppercase;box-shadow:0 2px 4px rgba(0,0,0,.15)">'
                '★ Editor\'s pick</div>'
            )

        rows.append(f'''            <a href="{b["tracker"]}" rel="sponsored nofollow" target="_blank" data-affiliate-brand="{b["slug"]}" style="display:block;position:relative;background:white;border:1px solid #E5E7EB;border-left:3px solid {b["logo_bg"]};border-radius:10px;padding:12px;text-decoration:none;color:inherit;box-shadow:0 1px 2px rgba(0,0,0,.04);transition:transform .15s ease, box-shadow .15s ease" onmouseover="this.style.transform=\'translateY(-2px)\';this.style.boxShadow=\'0 4px 12px rgba(0,0,0,.08)\'" onmouseout="this.style.transform=\'\';this.style.boxShadow=\'0 1px 2px rgba(0,0,0,.04)\'">{ribbon}
              <div style="display:flex;gap:10px;align-items:center;margin-bottom:8px">
                {rank_badge}
                {logo}
                <div style="flex:1;min-width:0">
                  <div style="font-weight:700;font-size:.92rem;color:#111827;white-space:nowrap;overflow:hidden;text-overflow:ellipsis">{html.escape(name)}</div>
                  <div style="font-size:.7rem;color:#F59E0B;letter-spacing:.02em">{stars_str} <span style="color:#6B7280;font-weight:600">{rating}/5</span></div>
                </div>
              </div>
              <div style="font-size:.78rem;color:#374151;margin:6px 0 10px;line-height:1.35">{html.escape(bonus_short)}</div>
              <div style="display:block;background:linear-gradient(135deg,{accent_from},{accent_to});color:white;text-align:center;padding:9px 12px;border-radius:8px;font-weight:700;font-size:.85rem;letter-spacing:.02em;box-shadow:0 2px 6px rgba(234,88,12,.35)">CLAIM BONUS →</div>
            </a>''')

    rows_html = "\n".join(rows)

    return f'''          <div class="conversion-sidebar" style="position:sticky;top:88px;border-radius:16px;overflow:hidden;box-shadow:0 8px 24px rgba(15,23,42,.08);border:1px solid #E5E7EB;background:white;margin-bottom:24px">
            <div style="background:linear-gradient(135deg,#0F172A,#1E293B);color:white;padding:16px 16px 14px">
              <div style="display:flex;align-items:center;gap:6px;margin-bottom:4px">
                <span style="font-size:.62rem;font-weight:800;letter-spacing:.12em;color:#FDE68A;text-transform:uppercase">★ Editor's picks</span>
                <span style="display:inline-block;width:6px;height:6px;border-radius:50%;background:#22C55E;box-shadow:0 0 0 3px rgba(34,197,94,.25);margin-left:auto"></span>
                <span style="font-size:.62rem;font-weight:700;color:#22C55E;letter-spacing:.05em">LIVE</span>
              </div>
              <div style="font-family:var(--font-display, Inter, sans-serif);font-weight:800;font-size:1.15rem;line-height:1.15">{product_title}</div>
              <div style="font-size:.72rem;color:#94A3B8;margin-top:2px">Ranked by our editorial team · Updated monthly</div>
            </div>
            <div style="padding:14px;display:flex;flex-direction:column;gap:10px;background:#F9FAFB">
{rows_html}
            </div>
            <div style="padding:12px 14px 14px;background:#F9FAFB;border-top:1px solid #E5E7EB">
              <a href="{up}reviews/" style="display:block;text-align:center;padding:9px 12px;border:1.5px solid #1E5CFF;color:#1E5CFF;background:white;border-radius:8px;font-weight:700;font-size:.82rem;text-decoration:none;letter-spacing:.02em">Compare all {product_slug} reviews →</a>
              <div style="text-align:center;font-size:.66rem;color:#9CA3AF;margin-top:8px;line-height:1.4">18+/21+ where required. T&amp;Cs apply. Play responsibly.</div>
            </div>
          </div>'''


# ---------------------------------------------------------------------------
# Detect and replace existing sidebars
# ---------------------------------------------------------------------------
# Match the whole existing sidebar card (either style: with or without
# position:sticky). Heading distinguishes the product line.
SIDEBAR_RE = re.compile(
    r'          <div class="card mb-3"[^>]*>\s*\n'
    r'            <h4 class="mt-0">(Top (?:casinos|poker sites|sportsbooks))</h4>'
    r'.*?'
    r'\n          </div>',
    re.S,
)

# Detect the NEW sidebar we've already emitted (skip on re-run)
NEW_SIDEBAR_MARKER = 'class="conversion-sidebar"'

PRODUCT_INFO = {
    "Top casinos":     (CASINO.BRANDS,     "Top Real-Money Casinos", "casino"),
    "Top poker sites": (POKER.BRANDS,      "Top Online Poker Rooms",  "poker"),
    "Top sportsbooks": (SPORTSBOOK.BRANDS, "Top US Sportsbooks",      "sportsbook"),
}


def update_file(path: Path) -> bool:
    text = path.read_text()
    if NEW_SIDEBAR_MARKER in text:
        return False  # already redesigned

    depth = len(path.relative_to(ROOT).parts) - 1

    def replace(m):
        heading = m.group(1)
        info = PRODUCT_INFO.get(heading)
        if not info:
            return m.group(0)
        brands, title, slug = info
        return render_sidebar(brands, title, slug, depth)

    text2 = SIDEBAR_RE.sub(replace, text)
    if text2 != text:
        path.write_text(text2)
        return True
    return False


def main() -> None:
    dirs = [ROOT / "poker", ROOT / "casino"]
    updated = 0
    for d in dirs:
        for path in sorted(d.rglob("index.html")):
            if update_file(path):
                print(f"  {path.relative_to(ROOT)}")
                updated += 1
    print(f"\n{updated} sidebars redesigned")

    subprocess.run(["git", "-C", str(ROOT), "add", "-A"], check=True)


if __name__ == "__main__":
    main()
