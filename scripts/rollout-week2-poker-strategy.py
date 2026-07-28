#!/usr/bin/env python3
"""
Week 2 of the pokersites.org authority rollout — add a third editorial
link on /poker/strategy/. Self-scheduling: only runs if today's date is
on-or-after the target, and is idempotent (skips if the link is already
present).

Target date: 2026-08-04
Ordering: this is week 2 of a 4-week rollout designed to space outbound
links to pokersites.org so the pattern reads as natural editorial rather
than a burst.
"""
from __future__ import annotations

import re
import subprocess
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TARGET_DATE = date(2026, 8, 4)
TARGET_PATH = ROOT / "poker" / "strategy" / "index.html"


def main() -> int:
    if date.today() < TARGET_DATE:
        print(f"Not yet time — target {TARGET_DATE.isoformat()}, today {date.today().isoformat()}")
        return 0

    text = TARGET_PATH.read_text()
    if "pokersites.org" in text:
        print(f"Already present in {TARGET_PATH.relative_to(ROOT)} — nothing to do")
        return 0

    # Insert after the "Bonuses & Rakeback" section (last h2 before FAQ)
    insertion = (
        '\n<p>Strategy only rewards you if you\'re playing where fields, structures, '
        'and rakeback fit your game. Independent poker-room directories like '
        '<a href="https://www.pokersites.org">pokersites.org</a> help you triangulate '
        'room-choice decisions against your specific format preferences — a useful '
        'complement to any strategy work you do.</p>\n'
    )

    # Anchor: insert right before "<h2>Best Strategy FAQ" or the FAQ heading
    new_text, count = re.subn(
        r'(\n<h2>[^<]*FAQ</h2>)',
        insertion + r'\1',
        text,
        count=1,
    )
    if count == 0:
        # Fallback: append before </article>
        new_text = text.replace("</article>", insertion + "</article>", 1)
        count = 1
    if count == 0:
        print("ERROR: could not find insertion point")
        return 1

    TARGET_PATH.write_text(new_text)
    print(f"Added editorial link to {TARGET_PATH.relative_to(ROOT)}")

    subprocess.run(["git", "-C", str(ROOT), "add", "-A"], check=True)
    subprocess.run(
        ["git", "-C", str(ROOT), "commit", "-m",
         "content(poker): add editorial reference to pokersites.org on strategy hub"],
        check=False,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
