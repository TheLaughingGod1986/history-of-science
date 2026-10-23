#!/usr/bin/env python3
"""£0 deterministic HOS compilation cover builder (J0878).

Reuses the approved 001 library key-art plate (`hos_001_thumb_B_swan_neck_v01.jpg`,
sterile golden broth in Pasteur's swan-neck flask on the right two-thirds, canonical
Explorer lower-left at 54.4% height, and original painted gold scroll flourishes),
restoring the clean bookcase and green curtain behind the upper-left lettering band
and rendering 'FLASK / PROOF' (cream 'FLASK', gold punch word 'PROOF') in house
3D Georgia Bold serif with dark ink outline and drop shadow.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[2]
MAIN_REPO = Path("/Users/benjaminoats/YouTube/History Of Science")
TOOLS = ROOT / "00_Brand" / "Channel-Setup" / "tools"
SRC_PLATE = (
    MAIN_REPO
    / "02_Video-Projects"
    / "001_How-Did-We-Discover-Germs"
    / "08_Thumbnail"
    / "Selected"
    / "hos_001_thumb_B_swan_neck_v01.jpg"
)

W, H = 1280, 720
CREAM = (242, 214, 172)
CREAM_HI = (252, 238, 208)
GOLD = (228, 156, 32)
GOLD_HI = (248, 202, 68)
INK = (16, 9, 4)
SHADOW = (6, 3, 1)
GEORGIA = "/System/Library/Fonts/Supplemental/Georgia Bold.ttf"
TRACKING = -2
CONDENSE_X = 0.94
CX = 285
HERO_BOX = (580, 10, 1138, 696)
EXPLORER_BOX = (88, 328, 316, 720)


def wipe_old_lettering(base: Image.Image) -> Image.Image:
    """Restore painted bookcase texture (x<440) and diagonal green curtain folds (x>=440)
    behind the upper-left lettering band (y=60..318, x=56..518) while preserving 100% of
    the top scroll flourish (y<=59), bottom scroll flourish (y>=318), and Explorer (y>=328)."""
    arr = np.array(base.convert("RGB"), dtype=np.float32)

    letter_mask = Image.new("L", (W, H), 0)
    lm = letter_mask.load()
    for y in range(60, 318):
        for x in range(56, 518):
            r, g, b = arr[y, x]
            if r > 32 and (r + g + b) > 68 and (r - b) > 8:
                lm[x, y] = 255

    dilated = letter_mask.filter(ImageFilter.MaxFilter(23)).filter(ImageFilter.GaussianBlur(3.5))
    dm = np.array(dilated, dtype=np.float32) / 255.0
    dm[:60, :] = 0.0
    dm[60, :] *= 0.4
    dm[61, :] *= 0.8
    for y in range(318, 330):
        for x in range(W):
            if 275 <= x <= 315 and y >= 318:
                dm[y, x] = 0.0
            elif 140 <= x <= 445 and y >= 324:
                dm[y, x] = 0.0
            elif y >= 325:
                dm[y, x] *= max(0.0, (329 - y) / 5.0)
    dm[330:, :] = 0.0
    dm[:, :52] = 0.0
    dm[:, 522:] = 0.0

    clean = arr.copy()
    slope = -0.19
    spine_top = arr[2:20, :460, :].mean(axis=0) * 0.50

    for y in range(58, 330):
        x_curt = int(round(492.0 + slope * (y - 60)))
        for x in range(50, 524):
            if x >= x_curt - 12:
                t = (y - 58.0) / (328.0 - 58.0)
                x_top = int(round(np.clip(x - slope * (y - 14), 445, 548)))
                x_bot = int(round(np.clip(x + slope * (336 - y), 425, 535)))
                c_top = arr[10:18, x_top, :].mean(axis=0)
                c_bot = arr[332:342, x_bot, :].mean(axis=0)
                if c_top[0] > 45 and (c_top[0] - c_top[2]) > 20:
                    c_top = c_bot * 0.85
                if c_bot[0] > 45 and (c_bot[0] - c_bot[2]) > 20:
                    c_bot = c_top
                clean[y, x] = c_top * (1.0 - t) + c_bot * t
            else:
                base_col = spine_top[min(459, x)]
                shelf_mod = 0.72 if (120 <= y <= 128 or 246 <= y <= 254) else 1.0
                bay_pos = ((y - 60) % 126) / 126.0
                bay_shade = 0.65 + 0.35 * (bay_pos ** 1.4)
                clean[y, x] = base_col * shelf_mod * bay_shade

    clean_im = Image.fromarray(np.clip(clean, 0, 255).astype(np.uint8), "RGB")
    clean_blur = clean_im.filter(ImageFilter.GaussianBlur(4.0))
    cb = np.array(clean_blur, dtype=np.float32)

    rng = np.random.default_rng(108)
    grain = rng.normal(0.0, 1.2, size=arr.shape).astype(np.float32)
    out = arr * (1.0 - dm[:, :, None]) + (cb + grain) * dm[:, :, None]
    return Image.fromarray(np.clip(out, 0, 255).astype(np.uint8), "RGB")


def render_word(text: str, size: int, fill: tuple[int, int, int], fill_hi: tuple[int, int, int]) -> Image.Image:
    f = ImageFont.truetype(GEORGIA, size)
    widths = [f.getbbox(ch)[2] - f.getbbox(ch)[0] + TRACKING for ch in text]
    total = max(1, sum(widths) - TRACKING)
    bb = f.getbbox(text)
    pad = 24
    layer = Image.new("RGBA", (total + pad * 2, bb[3] - bb[1] + pad * 2), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    y0 = pad - bb[1]
    stroke = max(7, size // 11)

    def chars(ox: int, oy: int, color: tuple[int, ...], sw: int = 0) -> None:
        x = pad
        for i, ch in enumerate(text):
            kw = dict(font=f, fill=color)
            if sw:
                kw.update(stroke_width=sw, stroke_fill=INK + (255,))
            d.text((x + ox, y0 + oy), ch, **kw)
            x += widths[i]

    for dx, dy in ((6, 7), (4, 5), (2, 3)):
        chars(dx, dy, SHADOW + (230,))
    chars(0, 0, INK + (255,), sw=stroke)
    chars(-1, -2, fill_hi + (255,))
    chars(0, 0, fill + (255,))
    layer = layer.crop(layer.split()[-1].getbbox())
    return layer.resize(
        (max(1, int(layer.size[0] * CONDENSE_X)), layer.size[1]),
        Image.Resampling.LANCZOS,
    )


def main() -> None:
    if not SRC_PLATE.exists():
        raise SystemExit(f"Missing source plate: {SRC_PLATE}")
    raw = Image.open(SRC_PLATE).convert("RGB").resize((W, H), Image.Resampling.LANCZOS)
    wiped = wipe_old_lettering(raw)
    wiped = ImageEnhance.Sharpness(wiped).enhance(1.12)
    rgba = wiped.convert("RGBA")

    lines = [
        ("FLASK", "cream", 104),
        ("PROOF", "gold", 108),
    ]
    sprites = []
    for text, kind, size in lines:
        fill, hi = (CREAM, CREAM_HI) if kind == "cream" else (GOLD, GOLD_HI)
        sprites.append((text, kind, size, render_word(text, size, fill, hi)))

    gap = 10
    total_h = sum(s[3].size[1] for s in sprites) + gap * (len(sprites) - 1)
    y = 63 + max(0, (250 - total_h) // 2)

    placed = []
    for idx_line, (text, kind, size, spr) in enumerate(sprites):
        left_x = int(round(CX - spr.size[0] / 2))
        tmp = Image.new("RGBA", rgba.size, (0, 0, 0, 0))
        tmp.paste(spr, (left_x, y), spr)
        rgba = Image.alpha_composite(rgba, tmp)
        placed.append({
            "word": text,
            "kind": kind,
            "size": size,
            "box": [left_x, y, left_x + spr.size[0], y + spr.size[1]],
        })
        if idx_line < len(sprites) - 1:
            y += spr.size[1] + gap

    left = min(p["box"][0] for p in placed)
    right = max(p["box"][2] for p in placed)
    top = min(p["box"][1] for p in placed)
    bottom = max(p["box"][3] for p in placed)
    assert right < HERO_BOX[0], f"Lettering {right} overlaps hero {HERO_BOX[0]}"
    assert bottom < EXPLORER_BOX[1], f"Lettering {bottom} overlaps Explorer {EXPLORER_BOX[1]}"

    thumb = OUT / "compilation_thumb_v01.jpg"
    phone = OUT / "PHONE_v01.jpg"
    style = OUT / "STYLE_v01.jpg"
    rgba.convert("RGB").save(thumb, "JPEG", quality=93, optimize=True, subsampling=1)

    subprocess.check_call([sys.executable, str(TOOLS / "thumb_preview.py"), "long", str(thumb), "--out", str(phone)])
    subprocess.check_call([sys.executable, str(TOOLS / "style_sheet.py"), "long", str(thumb), "--out", str(style)])
    print(f"SAVED {thumb} box=[{left}, {top}, {right}, {bottom}]")


if __name__ == "__main__":
    main()
