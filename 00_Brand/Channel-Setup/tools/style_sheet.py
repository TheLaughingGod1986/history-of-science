#!/usr/bin/env python3
"""Style check sheet: new thumbnails/covers side by side with the LIVE approved ones.

Rule (THUMBNAIL_AND_TITLE_RULES.md §2 and §4, 30 Sep 2026): no new long thumbnail or Shorts
cover goes to Ben until it has been put next to the live ones of the SAME format and reads as
the same family. This builds that sheet from the reference set in
00_Brand/Channel-Setup/style/{long,shorts}/, so nobody has to assemble it by hand.

  python3 00_Brand/Channel-Setup/tools/style_sheet.py long  new_A.jpg new_B.jpg --out sheet.jpg
  python3 00_Brand/Channel-Setup/tools/style_sheet.py short new_cover.jpg --out sheet.jpg

New images come first with a red frame; the references follow. Tiles are phone-feed size
(long 360×202, short 180×320). Then also run thumb_preview.py for the 168×94 legibility check.

When Ben approves a new thumbnail or cover and it goes live, copy it into style/long or
style/shorts so the reference set stays current.

Needs Pillow.
"""
from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image, ImageDraw, ImageOps

STYLE = Path(__file__).resolve().parent.parent / "style"
TILE = {"long": (360, 202), "short": (180, 320)}
REF_DIR = {"long": STYLE / "long", "short": STYLE / "shorts"}
GAP = 10
PER_ROW = {"long": 4, "short": 8}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("kind", choices=TILE)
    ap.add_argument("new", nargs="+", type=Path)
    ap.add_argument("--out", type=Path, required=True)
    ns = ap.parse_args()

    refs = sorted(p for p in REF_DIR[ns.kind].glob("*") if p.suffix.lower() in {".jpg", ".jpeg", ".png", ".webp"})
    if not refs:
        raise SystemExit(f"No references in {REF_DIR[ns.kind]} — add the live approved {ns.kind} images first.")
    items = [(p, True) for p in ns.new] + [(p, False) for p in refs]
    w, h = TILE[ns.kind]
    cols = min(PER_ROW[ns.kind], len(items))
    rows = (len(items) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * (w + GAP) + GAP, rows * (h + GAP) + GAP), "white")
    draw = ImageDraw.Draw(sheet)
    for i, (p, is_new) in enumerate(items):
        x = GAP + (i % cols) * (w + GAP)
        y = GAP + (i // cols) * (h + GAP)
        sheet.paste(ImageOps.fit(Image.open(p).convert("RGB"), (w, h), Image.LANCZOS), (x, y))
        if is_new:
            draw.rectangle([x - 3, y - 3, x + w + 2, y + h + 2], outline=(220, 30, 30), width=4)
    ns.out.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(ns.out, quality=90)
    print(f"{ns.out}  ({len(ns.new)} new vs {len(refs)} live {ns.kind} references)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
