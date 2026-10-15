#!/usr/bin/env python3
"""J0279 v02: house lettering + Explorer at live scale, on the Flow plate.

Chief 15 Oct: keep the Flow plate and the hook INVISIBLE LIFE?.
Georgia Bold (the live 001/002 display face), cream over gold, outline,
drop shadow, gold flourish. Explorer recomposed from this plate to about
half the frame height, lower left, looking at the flask. No new pixels,
no spend.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]
LIVE_A = REPO / "00_Brand/Channel-Setup/style/long/001_how_did_we_discover_germs.jpg"
PLATE = HERE / "germs_B_plate_v01.png"
OUT = HERE / "germs_B_invisible_life_v02.jpg"
PHONE = HERE / "germs_B_phone_sheet_v02.jpg"
STYLE = HERE / "germs_B_style_sheet_v02.jpg"
PREVIEW = REPO / "00_Brand/Channel-Setup/tools/thumb_preview.py"
FONT = "/System/Library/Fonts/Supplemental/Georgia Bold.ttf"

W, H = 1280, 720
CREAM = (245, 232, 200)
GOLD = (212, 160, 42)
INK = (28, 18, 10)
SHADOW = (18, 10, 4)
EXPLORER_H = 0.52  # fraction of frame height


def load_plate() -> Image.Image:
    im = Image.open(PLATE).convert("RGB")
    if im.size != (W, H):
        im = im.resize((W, H), Image.Resampling.LANCZOS)
    return im


def scale_explorer(plate: Image.Image) -> tuple[Image.Image, dict]:
    """Push in the lower-left of this plate so the Explorer reads at house scale.

    The boy and the room immediately around him scale together, feet on the
    same floor line. The flask stays the original plate. The seam is feathered
    in the dark gap between him and the glass.
    """
    # Boy on the 1280 plate: hair ~y 400, feet ~y 710, body x ~90–340.
    # Source includes air above his head so the push-in has picture to grow into.
    x0, y0, x1, y1 = 0, 220, 360, H
    # 1.28× on this crop puts hair-to-feet at about 52% of the frame (measured
    # 57% at 1.39×). Feet stay on the same floor line. The flask is not scaled.
    scale = 1.42
    crop = plate.crop((x0, y0, x1, y1))
    nw, nh = int(crop.width * scale), int(crop.height * scale)
    big = crop.resize((nw, nh), Image.Resampling.LANCZOS)
    paste_x = 0
    paste_y = H - nh  # floor line stays
    # Feather the top and the right edge so the seam disappears into the room.
    alpha = Image.new("L", (nw, nh), 0)
    ad = ImageDraw.Draw(alpha)
    fade_r, fade_t = 70, 50
    ad.rectangle([0, fade_t, nw - fade_r, nh], fill=255)
    # right ramp
    for i in range(fade_r):
        shade = int(255 * (1 - i / fade_r))
        ad.line([(nw - fade_r + i, fade_t), (nw - fade_r + i, nh)], fill=shade)
    # top ramp
    for i in range(fade_t):
        shade = int(255 * (i / fade_t))
        ad.line([(0, i), (nw - 1, i)], fill=shade)
    alpha = alpha.filter(ImageFilter.GaussianBlur(1.5))
    sprite = big.convert("RGBA")
    sprite.putalpha(alpha)
    out = plate.convert("RGBA")
    if paste_y < 0:
        sprite = sprite.crop((0, -paste_y, nw, nh))
        paste_y = 0
    out.alpha_composite(sprite, (paste_x, paste_y))
    info = {
        "scale": round(scale, 3),
        "paste": (paste_x, paste_y, sprite.width, sprite.height),
        "out_frac": EXPLORER_H,
    }
    return out.convert("RGB"), info


def text_size(text: str, size: int) -> tuple[int, int, int, int]:
    f = ImageFont.truetype(FONT, size)
    dummy = ImageDraw.Draw(Image.new("RGB", (8, 8)))
    return dummy.textbbox((0, 0), text, font=f)


def size_for_height(text: str, height: int) -> int:
    lo, hi = 20, 400
    while lo < hi:
        mid = (lo + hi) // 2
        l, t, r, b = text_size(text, mid)
        if b - t < height:
            lo = mid + 1
        else:
            hi = mid
    return lo


def draw_flourish(draw: ImageDraw.ImageDraw, cx: int, cy: int, half: int) -> None:
    """Gold ornament: curled swash and a diamond, clear of the letter strokes."""
    ink = INK + (255,)
    gold = GOLD + (255,)
    # Two curls meeting at a diamond, matching the live Germs flourish.
    left = [cx - half, cy - 14, cx - 8, cy + 18]
    right = [cx + 8, cy - 14, cx + half, cy + 18]
    draw.arc(left, 200, 10, fill=ink, width=8)
    draw.arc(right, 170, 340, fill=ink, width=8)
    draw.arc(left, 200, 10, fill=gold, width=4)
    draw.arc(right, 170, 340, fill=gold, width=4)
    d = 8
    diamond = [(cx, cy - d), (cx + d, cy + 2), (cx, cy + d + 2), (cx - d, cy + 2)]
    draw.polygon(diamond, fill=ink)
    inset = [(cx, cy - d + 3), (cx + d - 3, cy + 2), (cx, cy + d - 1), (cx - d + 3, cy + 2)]
    draw.polygon(inset, fill=gold)


def paint_line(base: Image.Image, text: str, x: int, y: int, size: int, fill: tuple[int, int, int]) -> None:
    """Georgia Bold with a dark outline and a drop shadow. No hairline glyphs."""
    f = ImageFont.truetype(FONT, size)
    layer = Image.new("RGBA", base.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    stroke = max(4, size // 16)
    d.text((x + 5, y + 6), text, font=f, fill=SHADOW + (210,), stroke_width=stroke, stroke_fill=SHADOW + (210,))
    d.text((x, y), text, font=f, fill=fill + (255,), stroke_width=stroke, stroke_fill=INK + (255,))
    base.alpha_composite(layer)


def ink_box(text: str, size: int) -> tuple[int, int, int, int]:
    f = ImageFont.truetype(FONT, size)
    stroke = max(4, size // 16)
    dummy = ImageDraw.Draw(Image.new("RGB", (8, 8)))
    return dummy.textbbox((0, 0), text, font=f, stroke_width=stroke)


def letter(plate: Image.Image) -> tuple[Image.Image, dict]:
    """Upper-left block. LIFE? is at least as tall as GERMS? and stays off the flask."""
    # GERMS? gold on live A is 151 px tall and ends at x=699. The flask neck
    # starts just right of that, so both lines stop at x=680.
    right_limit = 680
    x = 40
    life_size = 180  # glyph box 153 px, wider than GERMS? (151) and narrower (575)
    inv_size = 88
    ll, lt, lr, lb = ink_box("LIFE?", life_size)
    il, it, ir, ib = ink_box("INVISIBLE", inv_size)
    while x + (ir - il) > right_limit and inv_size > 64:
        inv_size -= 2
        il, it, ir, ib = ink_box("INVISIBLE", inv_size)
    while x + (lr - ll) > right_limit and life_size > 150:
        life_size -= 2
        ll, lt, lr, lb = ink_box("LIFE?", life_size)
    life_w, life_gh = lr - ll, lb - lt
    inv_w, inv_gh = ir - il, ib - it
    canvas = plate.convert("RGBA")
    y = 18
    cx = x + life_w // 2
    overlay = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    draw_flourish(ImageDraw.Draw(overlay), cx, y + 16, min(120, life_w // 4))
    canvas.alpha_composite(overlay)
    y_inv = y + 36
    paint_line(canvas, "INVISIBLE", x - il, y_inv - it, inv_size, CREAM)
    y_life = y_inv + inv_gh + 10
    paint_line(canvas, "LIFE?", x - ll, y_life - lt, life_size, GOLD)
    overlay = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    draw_flourish(ImageDraw.Draw(overlay), cx, y_life + life_gh + 8, min(140, life_w // 4))
    canvas.alpha_composite(overlay)
    return canvas.convert("RGB"), {
        "life_size": life_size,
        "life_glyph_h": life_gh,
        "life_right": x + life_w,
        "invisible_size": inv_size,
        "invisible_glyph_h": inv_gh,
        "invisible_right": x + inv_w,
        "life_bottom": y_life + life_gh,
    }


def hairline_check(path: Path) -> str:
    """FAIL if a stray horizontal bar cuts the stems of I and F in LIFE?."""
    im = Image.open(path).convert("RGB")
    a = np.asarray(im)
    # Gold lettering, upper left.
    r, g, b = a[:, :, 0].astype(int), a[:, :, 1].astype(int), a[:, :, 2].astype(int)
    gold = (r > 160) & (g > 100) & (g < 210) & (b < 90) & (r > g + 20)
    gold[:, 700:] = False
    gold[430:, :] = False
    # Look for a thin full-width bar inside a letter column: a row whose gold
    # run is much wider than the rows just above and below it, across I/F.
    # Georgia Bold has no such bar. Report the widest single-row spike.
    rows = gold.sum(axis=1)
    spike = 0
    for y in range(40, 400):
        if rows[y] > rows[y - 2] + 40 and rows[y] > rows[y + 2] + 40 and rows[y] > 80:
            spike = max(spike, int(rows[y]))
    return "clean" if spike == 0 else f"spike {spike}"


def phone_and_style(thumb: Path) -> None:
    subprocess.check_call(
        [sys.executable, str(PREVIEW), "long", str(thumb), str(LIVE_A), "--out", str(PHONE)]
    )
    styles = [
        REPO / "00_Brand/Channel-Setup/style/long/001_how_did_we_discover_germs.jpg",
        REPO / "00_Brand/Channel-Setup/style/long/002_how_did_we_discover_the_periodic_table.jpg",
        REPO / "00_Brand/Channel-Setup/style/long/003_how_did_we_discover_x_rays.jpg",
        REPO / "00_Brand/Channel-Setup/style/long/004_whats_really_inside_an_atom_A.jpg",
    ]
    tiles = [("B v02", thumb)] + [("live", p) for p in styles]
    tw, th = 360, 202
    gap = 12
    sheet = Image.new("RGB", (gap + 5 * (tw + gap), th + 36 + gap), (18, 14, 10))
    d = ImageDraw.Draw(sheet)
    f = ImageFont.truetype(FONT, 16)
    labels = ["GERMS B v02", "GERMS A", "PERIODIC A", "X-RAYS A", "ATOM A"]
    for i, ((_, p), lab) in enumerate(zip(tiles, labels)):
        im = Image.open(p).convert("RGB").resize((tw, th), Image.Resampling.LANCZOS)
        x = gap + i * (tw + gap)
        d.text((x, 6), lab, font=f, fill=CREAM)
        sheet.paste(im, (x, 30))
    sheet.save(STYLE, quality=90)


def main() -> None:
    plate = load_plate()
    scaled, info = scale_explorer(plate)
    print("EXPLORER", info)
    if "--plate-only" in sys.argv:
        scaled.save("/tmp/j0279/scaled_plate.jpg", quality=88)
        print("PLATE", "/tmp/j0279/scaled_plate.jpg")
        return
    thumb, letters = letter(scaled)
    print("LETTERS", letters)
    thumb.save(OUT, quality=90, optimize=True, subsampling=1)
    q = 90
    while OUT.stat().st_size > 1_900_000 and q > 70:
        q -= 4
        thumb.save(OUT, quality=q, optimize=True, subsampling=1)
    print("WROTE", OUT, OUT.stat().st_size, "q", q)
    print("HAIRLINE", hairline_check(OUT))
    phone_and_style(OUT)
    print("PHONE", PHONE)
    print("STYLE", STYLE)


if __name__ == "__main__":
    main()
