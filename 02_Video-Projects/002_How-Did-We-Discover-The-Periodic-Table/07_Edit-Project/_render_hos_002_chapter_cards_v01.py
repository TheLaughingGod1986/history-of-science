#!/usr/bin/env python3
"""Render HOS 002 mid-film chapter cards to match Part 02's parchment plate.

Cheap read: PART N + year + short title. No long subtitle.

P01 cold-opens (house lock — no card at 0:00).
P02 already opens on its baked CHAPTER 2 card — do not duplicate.
These stills are inserted before locked Parts 03 / 04 / 05.

Locked stills — no Ken Burns. No Flow. No remint of 01–05.
"""
from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

PROJ = Path(__file__).resolve().parents[1]
OUT_DIR = PROJ / "07_Edit-Project/chapter_cards_v01"

CARDS = [
    {
        "id": "03",
        "part": "PART 03",
        "date": "1860",
        "title": "The ruler",
    },
    {
        "id": "04",
        "part": "PART 04",
        "date": "1869",
        "title": "Empty chairs",
    },
    {
        "id": "05",
        "part": "PART 05",
        "date": "1875",
        "title": "The guests",
    },
]

W, H = 1920, 1080
STRIPE_A = (28, 20, 16)
STRIPE_B = (36, 24, 18)
PLAQUE = (234, 220, 196)
INK = (48, 32, 20)
RULE = (92, 64, 40)
MUTED = (96, 68, 44)


def font(path: str, size: int) -> ImageFont.FreeTypeFont:
    for p in (path, "/System/Library/Fonts/Supplemental/Georgia.ttf"):
        try:
            return ImageFont.truetype(p, size)
        except OSError:
            continue
    return ImageFont.load_default()


def draw_card(card: dict) -> Image.Image:
    im = Image.new("RGB", (W, H), STRIPE_A)
    d = ImageDraw.Draw(im)
    for y in range(0, H, 28):
        if (y // 28) % 2 == 0:
            d.rectangle((0, y, W, y + 14), fill=STRIPE_B)
    x0, y0, x1, y1 = 300, 260, 1620, 820
    d.rounded_rectangle((x0 - 8, y0 - 8, x1 + 8, y1 + 8), radius=6, outline=RULE, width=3)
    d.rounded_rectangle((x0, y0, x1, y1), radius=4, fill=PLAQUE)
    d.rounded_rectangle((x0 + 18, y0 + 18, x1 - 18, y1 - 18), radius=2, outline=INK, width=3)

    f_part = font("/System/Library/Fonts/Supplemental/Georgia.ttf", 32)
    f_date = font("/System/Library/Fonts/Supplemental/Georgia Bold.ttf", 120)
    f_title = font("/System/Library/Fonts/Supplemental/Georgia Italic.ttf", 42)

    def center(text: str, y: int, fnt, fill) -> None:
        bb = d.textbbox((0, 0), text, font=fnt)
        tw = bb[2] - bb[0]
        d.text(((W - tw) / 2, y), text, font=fnt, fill=fill)

    center(card["part"], 340, f_part, MUTED)
    cx, cy = W / 2, 400
    d.line((cx - 180, cy, cx - 14, cy), fill=RULE, width=2)
    d.ellipse((cx - 5, cy - 5, cx + 5, cy + 5), fill=INK)
    d.line((cx + 14, cy, cx + 180, cy), fill=RULE, width=2)
    center(card["date"], 430, f_date, INK)
    center(card["title"], 590, f_title, MUTED)
    return im


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for card in CARDS:
        im = draw_card(card)
        png = OUT_DIR / f"chapter_{card['id']}.png"
        im.save(png, "PNG")
        print(f"SAVED {png}  {card['part']}  {card['date']}  {card['title']}", flush=True)


if __name__ == "__main__":
    main()
