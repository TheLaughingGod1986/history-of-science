#!/usr/bin/env python3
"""HOS 002 long thumb B v01: THE MISSING ELEMENT (OWB queue J0255, backlog thumb B).

Re-letter of the existing text-free hero plate `_stills_v05/hos_002_empty_slot_hero_v01.jpg`
(glowing empty slot in a wall of blank cream tiles). House lettering: Georgia Bold, cream with
one gold punch word, on the clear left edge, never over the glowing slot. £0, no image model.

Output is a Test & Compare B candidate against the live A only. No Studio until Chief OKs it.
"""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = Path(__file__).resolve().parent
PLATE = HERE / "_stills_v05" / "hos_002_empty_slot_hero_v01.jpg"
SELECTED = HERE / "Selected"
TOOLS = HERE.parents[2] / "00_Brand" / "Channel-Setup" / "tools"
LIVE_A = HERE.parents[2] / "00_Brand" / "Channel-Setup" / "style" / "long" / "002_how_did_we_discover_the_periodic_table.jpg"
OUT = SELECTED / "hos_002_thumb_B_missing_element_v01.jpg"

W, H = 1280, 720
CREAM = (238, 200, 155)
CREAM_HI = (250, 232, 198)
GOLD = (224, 150, 28)
GOLD_HI = (245, 195, 60)
INK = (14, 8, 4)
SHADOW = (4, 2, 1)
GEORGIA = "/System/Library/Fonts/Supplemental/Georgia Bold.ttf"
TRACKING = -4
CONDENSE_X = 0.9

LINES = [
    ("THE", "cream", 92),
    ("MISSING", "gold", 128),
    ("ELEMENT", "cream", 112),
]
LEFT_X = 44
TOP_Y = 92
GAP = 10
HERO_BOX = (725, 235, 1010, 485)  # glowing slot at 1280x720; lettering must stay left of it


def word(text: str, size: int, fill, fill_hi) -> Image.Image:
    f = ImageFont.truetype(GEORGIA, size)
    widths = [f.getbbox(ch)[2] - f.getbbox(ch)[0] + TRACKING for ch in text]
    total = max(1, sum(widths) - TRACKING)
    bb = f.getbbox(text)
    pad = 28
    layer = Image.new("RGBA", (total + pad * 2, bb[3] - bb[1] + pad * 2), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    y0 = pad - bb[1]
    stroke = max(7, size // 11)

    def chars(ox, oy, color, sw=0):
        x = pad
        for i, ch in enumerate(text):
            kw = dict(font=f, fill=color)
            if sw:
                kw.update(stroke_width=sw, stroke_fill=INK)
            d.text((x + ox, y0 + oy), ch, **kw)
            x += widths[i]

    for dx, dy in ((7, 8), (5, 6), (3, 4)):
        chars(dx, dy, SHADOW + (230,))
    chars(0, 0, INK + (255,), sw=stroke)
    chars(-1, -2, fill_hi + (255,))
    chars(0, 0, fill + (255,))
    layer = layer.crop(layer.split()[-1].getbbox())
    return layer.resize((max(1, int(layer.size[0] * CONDENSE_X)), layer.size[1]), Image.Resampling.LANCZOS)


def left_shade(im: Image.Image) -> Image.Image:
    """Soft warm darkening behind the lettering column (a vignette, not a slab)."""
    mask = Image.new("L", (W, H), 0)
    d = ImageDraw.Draw(mask)
    for x in range(620):
        d.line([(x, 0), (x, H)], fill=int(150 * (1 - x / 620) ** 1.6))
    mask = mask.filter(ImageFilter.GaussianBlur(30))
    dark = Image.new("RGB", (W, H), (20, 10, 4))
    return Image.composite(dark, im, mask)


def main() -> None:
    plate = Image.open(PLATE).convert("RGB").resize((W, H), Image.Resampling.LANCZOS)
    rgba = left_shade(plate).convert("RGBA")
    y = TOP_Y
    placed = []
    for text, kind, size in LINES:
        fill, hi = (CREAM, CREAM_HI) if kind == "cream" else (GOLD, GOLD_HI)
        spr = word(text, size, fill, hi)
        tmp = Image.new("RGBA", rgba.size, (0, 0, 0, 0))
        tmp.paste(spr, (LEFT_X, y), spr)
        rgba = Image.alpha_composite(rgba, tmp)
        placed.append({"word": text, "size": size, "box": [LEFT_X, y, LEFT_X + spr.size[0], y + spr.size[1]]})
        y += spr.size[1] + GAP
    out = rgba.convert("RGB")
    SELECTED.mkdir(parents=True, exist_ok=True)
    out.save(OUT, "JPEG", quality=92, optimize=True, subsampling=1)

    right = max(p["box"][2] for p in placed)
    bottom = max(p["box"][3] for p in placed)
    clear_of_hero = right < HERO_BOX[0]
    clear_of_badge = bottom < H - 120 or right < W - 260
    print(f"lettering right={right} bottom={bottom} clear_of_hero={clear_of_hero} clear_of_badge={clear_of_badge}")

    preview = SELECTED / f"{OUT.stem}_preview.jpg"
    subprocess.check_call([sys.executable, str(TOOLS / "thumb_preview.py"), "long", str(OUT), "--out", str(preview)])
    sheet = SELECTED / f"{OUT.stem}_style_sheet.jpg"
    subprocess.check_call([sys.executable, str(TOOLS / "style_sheet.py"), "long", str(OUT), "--out", str(sheet)])

    phone = SELECTED / "hos_002_thumb_A_vs_B_missing_element_v01_phone_168.jpg"
    a = Image.open(LIVE_A).convert("RGB").resize((168, 94), Image.Resampling.LANCZOS)
    b = out.resize((168, 94), Image.Resampling.LANCZOS)
    strip = Image.new("RGB", (168 * 2 + 8, 94 + 22), (12, 8, 4))
    d = ImageDraw.Draw(strip)
    lf = ImageFont.truetype(GEORGIA, 14)
    d.text((4, 2), "A live", font=lf, fill=(220, 200, 160))
    d.text((180, 2), "B v01", font=lf, fill=(220, 200, 160))
    strip.paste(a, (0, 18))
    strip.paste(b, (176, 18))
    strip.resize((strip.size[0] * 3, strip.size[1] * 3), Image.Resampling.NEAREST).save(phone, "JPEG", quality=95)

    idx = {
        "film": "002",
        "video": "AL_-qlWko_g",
        "job": "J0255",
        "variant": "B",
        "maker": "cursor",
        "hook": "THE MISSING ELEMENT",
        "punch": "MISSING",
        "jpg": f"Selected/{OUT.name}",
        "sha256": hashlib.sha256(OUT.read_bytes()).hexdigest(),
        "plate": f"_stills_v05/{PLATE.name}",
        "method": "reletter_existing_plate_GeorgiaBold_no_image_model",
        "spend": 0,
        "lettering": placed,
        "clearOfHero": clear_of_hero,
        "clearOfBadge": clear_of_badge,
        "previews": [f"Selected/{preview.name}", f"Selected/{sheet.name}", f"Selected/{phone.name}"],
        "studio": False,
        "status": "Test & Compare B candidate against live A. Parked for Chief: thumb B review. No Studio until OK.",
    }
    (HERE / "THUMB_B_MISSING_ELEMENT_v01.json").write_text(json.dumps(idx, indent=2) + "\n")
    print("DONE", OUT, idx["sha256"])


if __name__ == "__main__":
    main()
