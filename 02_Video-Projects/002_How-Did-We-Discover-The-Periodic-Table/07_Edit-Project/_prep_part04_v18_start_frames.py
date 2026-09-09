#!/usr/bin/env python3
"""Prep Part 04 v18 start frames — Ben OVERRIDE FAIL remint (single-exposure).

Parent FAIL: hos_002_part04_rough_v17.mp4
  sha256 e4cc41d8cf050f6726e6b3d5cbbbff10285656c588f3a758b4a29e1ec1f998fd

Remint: 06_explorer_leaves_gap · 10_family_before_weight · 11_publish_gaps · 11b_wait_and_hunt
KEEP: written cards ~40 · CLEAN LIGHT 09/09b if still clean

HARD:
- ZERO horizontal ghost doubles (no nested glow edges, no oversharpen ringing)
- Explorer: finished wavy crown, NO face-cloud blot, NO black-hole dots, gold glasses
- Clean warm lamp — no lava / blown jagged white
- Soft Empty Chairs = ONE soft rectangle only
"""
from __future__ import annotations

import json
import math
import random
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont

PROJ = Path(__file__).resolve().parents[1]
REPO = PROJ.parents[1]
OUT = PROJ / "04_Generated-Clips/part04/refs/v18_start_frames"
QA = PROJ / "07_Edit-Project/_qa_part04_v18_prep"
META = OUT / "compose_meta.json"
SHEET = REPO / "01_Character/01_Master-References/hos-explorer-character-sheet-v01.jpg"
W, H = 1920, 1080
PARENT_V17_SHA = "e4cc41d8cf050f6726e6b3d5cbbbff10285656c588f3a758b4a29e1ec1f998fd"


def _font(size: int):
    for path in (
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
        "/System/Library/Fonts/Supplemental/Georgia Bold.ttf",
        "/Library/Fonts/Arial Bold.ttf",
    ):
        try:
            return ImageFont.truetype(path, size)
        except OSError:
            continue
    return ImageFont.load_default()


def paint_bookshelf(canvas: Image.Image, *, x0: int, y0: int, x1: int, y1: int) -> None:
    d = ImageDraw.Draw(canvas)
    d.rectangle((x0, y0, x1, y1), fill=(55, 38, 26, 255))
    colors = [
        (92, 62, 38), (110, 75, 45), (78, 52, 32), (130, 90, 55),
        (70, 48, 30), (100, 68, 42), (120, 82, 50), (85, 58, 35),
        (95, 70, 48), (60, 42, 28),
    ]
    x = x0 + 8
    ci = 0
    while x < x1 - 10:
        bw = 14 + (ci % 6)
        d.rectangle((x, y0 + 6, min(x1 - 6, x + bw), y1 - 6), fill=(*colors[ci % len(colors)], 255))
        x += bw + 2
        ci += 1
    for sy in range(y0 + 90, y1 - 20, 95):
        d.line((x0 + 4, sy, x1 - 4, sy), fill=(40, 28, 18, 255), width=5)


def paint_night_window(canvas: Image.Image) -> None:
    d = ImageDraw.Draw(canvas)
    wx0, wy0, wx1, wy1 = int(W * 0.34), int(H * 0.02), int(W * 0.66), int(H * 0.36)
    d.rectangle((wx0, wy0, wx1, wy1), fill=(25, 40, 70, 255), outline=(70, 50, 35, 255), width=8)
    mx, my = (wx0 + wx1) // 2, (wy0 + wy1) // 2
    d.line((mx, wy0, mx, wy1), fill=(70, 50, 35, 255), width=6)
    d.line((wx0, my, wx1, my), fill=(70, 50, 35, 255), width=6)
    mcx, mcy, r = int(W * 0.55), int(H * 0.14), 46
    d.ellipse((mcx - r, mcy - r, mcx + r, mcy + r), fill=(240, 235, 210, 255))


def soft_empty_chairs_once(canvas: Image.Image) -> Image.Image:
    """ONE soft rectangle — blur-only glow (no hard nested edge Ben read as double)."""
    mask = Image.new("L", (W, H), 0)
    d = ImageDraw.Draw(mask)
    x0, y0, x1, y1 = int(W * 0.42), int(H * 0.24), int(W * 0.58), int(H * 0.40)
    d.rounded_rectangle((x0, y0, x1, y1), radius=18, fill=255)
    # heavier blur so edge is one soft falloff, never a parallel hard line
    mask = mask.filter(ImageFilter.GaussianBlur(28))
    glow = Image.new("RGBA", (W, H), (255, 236, 190, 0))
    a = mask.point(lambda v: int(v * 0.22))
    glow.putalpha(a)
    return Image.alpha_composite(canvas, glow)


def paint_lamp(canvas: Image.Image, cx: int, cy: int, *, scale: float = 1.0) -> None:
    """Solid warm lamp — no blown white lava patches · no stepped concentric rings."""
    lw, lh = int(150 * scale), int(260 * scale)
    lamp = Image.new("RGBA", (lw, lh), (0, 0, 0, 0))
    d = ImageDraw.Draw(lamp)
    # ONE base ellipse only (nested bases read as horizontal doubles under soft light)
    d.ellipse((int(lw * 0.26), int(lh * 0.82), int(lw * 0.74), int(lh * 0.96)), fill=(125, 88, 48, 255))
    d.rectangle((int(lw * 0.46), int(lh * 0.30), int(lw * 0.54), int(lh * 0.84)), fill=(145, 105, 55, 255))
    d.polygon(
        [
            (int(lw * 0.16), int(lh * 0.36)),
            (int(lw * 0.84), int(lh * 0.36)),
            (int(lw * 0.68), int(lh * 0.10)),
            (int(lw * 0.32), int(lh * 0.10)),
        ],
        fill=(175, 135, 70, 255),
    )
    # shade lip as same fill family — no hard outline ring
    d.polygon(
        [
            (int(lw * 0.18), int(lh * 0.34)),
            (int(lw * 0.82), int(lh * 0.34)),
            (int(lw * 0.78), int(lh * 0.36)),
            (int(lw * 0.22), int(lh * 0.36)),
        ],
        fill=(155, 115, 55, 255),
    )
    # warm underside — heavy blur, low alpha so no stepped rings / jagged white
    warm = Image.new("RGBA", (lw, lh), (0, 0, 0, 0))
    ImageDraw.Draw(warm).ellipse(
        (int(lw * 0.22), int(lh * 0.20), int(lw * 0.78), int(lh * 0.52)),
        fill=(255, 205, 130, 55),
    )
    warm = warm.filter(ImageFilter.GaussianBlur(16))
    lamp = Image.alpha_composite(lamp, warm)
    canvas.alpha_composite(lamp, (cx - lw // 2, cy - lh // 2))


def paint_flask(
    canvas: Image.Image,
    cx: int,
    cy: int,
    *,
    liquid: tuple[int, int, int],
    scale: float = 1.0,
    sphere: bool = False,
) -> None:
    """Fully opaque flask — single silhouette (no rim+inner double outline)."""
    fw, fh = int(110 * scale), int(150 * scale)
    flask = Image.new("RGBA", (fw, fh), (0, 0, 0, 0))
    d = ImageDraw.Draw(flask)
    # outer glass body — fill only, no outline stroke (stroke+fill reads as ghost rim)
    d.ellipse((8, int(fh * 0.28), fw - 9, fh - 8), fill=(200, 215, 225, 255))
    ly0 = int(fh * 0.50)
    # liquid inset enough that glass rim is a band, not a second flask
    d.ellipse((18, ly0, fw - 19, fh - 16), fill=(*liquid, 255))
    if sphere:
        # bubbles as lighter liquid tint only — no dark outline rings
        for ox, oy, r in ((0.38, 0.64, 7), (0.55, 0.72, 5), (0.44, 0.78, 4)):
            sx, sy = int(fw * ox), int(fh * oy)
            bubble = tuple(min(255, c + 40) for c in liquid)
            d.ellipse((sx - r, sy - r, sx + r, sy + r), fill=(*bubble, 255))
    nx0, nx1 = int(fw * 0.40), int(fw * 0.60)
    d.rectangle((nx0, 8, nx1, int(fh * 0.36)), fill=(195, 210, 220, 255))
    d.ellipse((nx0 - 1, 4, nx1 + 1, 14), fill=(215, 220, 225, 255))
    # single soft specular — not a second body
    d.ellipse((int(fw * 0.22), int(fh * 0.36), int(fw * 0.34), int(fh * 0.52)), fill=(235, 240, 245, 255))
    canvas.alpha_composite(flask, (cx - fw // 2, cy - fh // 2))


def paint_magnifier(canvas: Image.Image, cx: int, cy: int, *, scale: float = 1.0) -> None:
    """Opaque lens + single ring — no translucent inner that reads as a double."""
    mw, mh = int(220 * scale), int(90 * scale)
    mag = Image.new("RGBA", (mw, mh), (0, 0, 0, 0))
    d = ImageDraw.Draw(mag)
    r = int(38 * scale)
    # filled opaque glass disk first, then ONE ring
    d.ellipse((10, mh // 2 - r + 2, 6 + 2 * r, mh // 2 + r - 2), fill=(175, 200, 210, 255))
    d.ellipse((8, mh // 2 - r, 8 + 2 * r, mh // 2 + r), outline=(140, 105, 50, 255), width=5)
    d.line((8 + 2 * r - 4, mh // 2 + 4, mw - 10, mh // 2 + 18), fill=(90, 60, 35, 255), width=10)
    canvas.alpha_composite(mag, (cx - mw // 2, cy - mh // 2))


def paint_mortar(canvas: Image.Image, cx: int, cy: int, *, scale: float = 1.0, color=(235, 230, 220)) -> None:
    """Single bowl silhouette — no nested ellipse doubles."""
    mw, mh = int(90 * scale), int(70 * scale)
    m = Image.new("RGBA", (mw, mh), (0, 0, 0, 0))
    d = ImageDraw.Draw(m)
    d.ellipse((4, int(mh * 0.22), mw - 5, mh - 4), fill=(*color, 255))
    # pestle as one stroke only
    d.line((int(mw * 0.55), 6, int(mw * 0.78), int(mh * 0.55)), fill=(185, 175, 160, 255), width=7)
    canvas.alpha_composite(m, (cx - mw // 2, cy - mh // 2))


def paint_card_stack(canvas: Image.Image, cx: int, cy: int, *, n: int = 5, scale: float = 1.0) -> None:
    """Stack depth is VERTICAL only — horizontal card offsets read as Ben ghost doubles."""
    cw, ch = int(70 * scale), int(90 * scale)
    for i in range(n):
        card = Image.new("RGBA", (cw, ch), (0, 0, 0, 0))
        d = ImageDraw.Draw(card)
        d.rounded_rectangle((1, 1, cw - 2, ch - 2), radius=6, fill=(248, 242, 228, 255), outline=(55, 45, 35, 255), width=2)
        canvas.alpha_composite(card, (cx - cw // 2, cy - ch // 2 - i * 3))


def paint_element_card(
    canvas: Image.Image,
    pos: tuple[int, int],
    symbol: str,
    weight: str,
    *,
    angle: float = 0.0,
    scale: float = 1.0,
) -> None:
    cw, ch = int(150 * scale), int(190 * scale)
    card = Image.new("RGBA", (cw, ch), (0, 0, 0, 0))
    d = ImageDraw.Draw(card)
    d.rounded_rectangle((2, 2, cw - 3, ch - 3), radius=10, fill=(250, 244, 230, 255), outline=(40, 32, 24, 255), width=3)
    d.text((cw // 2 - 28 * scale, ch * 0.18), symbol, fill=(30, 25, 20, 255), font=_font(int(72 * scale)))
    d.text((cw // 2 - 20 * scale, ch * 0.62), weight, fill=(50, 42, 34, 255), font=_font(int(40 * scale)))
    if abs(angle) > 0.1:
        card = card.rotate(angle, resample=Image.Resampling.BICUBIC, expand=True)
    cx, cy = pos
    canvas.alpha_composite(card, (cx - card.size[0] // 2, cy - card.size[1] // 2))


def paint_grid_sheet(
    canvas: Image.Image,
    x0: int,
    y0: int,
    x1: int,
    y1: int,
    *,
    holes: bool = False,
) -> None:
    sheet = Image.new("RGBA", (x1 - x0, y1 - y0), (0, 0, 0, 0))
    d = ImageDraw.Draw(sheet)
    w, h = sheet.size
    d.rounded_rectangle((2, 2, w - 3, h - 3), radius=8, fill=(245, 236, 215, 255))
    # single thin rim stroke only (width 2)
    d.rounded_rectangle((2, 2, w - 3, h - 3), radius=8, outline=(60, 50, 40, 255), width=2)
    cols, rows = 6, 4
    pad = 18
    cell_w = (w - 2 * pad) / cols
    cell_h = (h - 2 * pad) / rows
    ink = (35, 30, 28, 255)
    for c in range(cols + 1):
        x = int(pad + c * cell_w)
        d.line((x, pad, x, h - pad), fill=ink, width=2)
    for r in range(rows + 1):
        y = int(pad + r * cell_h)
        d.line((pad, y, w - pad, y), fill=ink, width=2)
    gap_cells = {(1, 1), (2, 2), (4, 1), (3, 3), (5, 2)} if holes else {(1, 1), (3, 2), (4, 1)}
    for (cc, rr) in gap_cells:
        cx = int(pad + (cc + 0.5) * cell_w)
        cy = int(pad + (rr + 0.5) * cell_h)
        rad = int(min(cell_w, cell_h) * 0.28)
        if holes:
            d.ellipse((cx - rad, cy - rad, cx + rad, cy + rad), fill=(120, 85, 50, 255))
        else:
            d.ellipse((cx - rad, cy - rad, cx + rad, cy + rad), fill=(55, 45, 35, 255))
    canvas.alpha_composite(sheet, (x0, y0))


def base_room() -> Image.Image:
    """Fully opaque procedural room — never composite onto ghosty KEEP DNA."""
    rgba = Image.new("RGBA", (W, H), (28, 22, 18, 255))
    d0 = ImageDraw.Draw(rgba)
    d0.rectangle((0, 0, W, int(H * 0.42)), fill=(42, 30, 22, 255))
    d0.rectangle((0, 0, int(W * 0.34), int(H * 0.42)), fill=(48, 34, 24, 255))
    for i in range(0, int(H * 0.42), 28):
        d0.line((0, i, int(W * 0.34), i), fill=(58, 40, 28, 255), width=2)
    paint_bookshelf(rgba, x0=int(W * 0.66), y0=0, x1=W, y1=int(H * 0.42))
    paint_night_window(rgba)
    # opaque desk + soft warm pool (drawn into opaque desk, not a second exposure)
    desk = Image.new("RGBA", (W, int(H * 0.68)), (78, 52, 32, 255))
    dd = ImageDraw.Draw(desk)
    for i in range(0, desk.size[1], 5):
        shade = 78 + (i % 12) - 4
        dd.rectangle((0, i, W, i + 4), fill=(shade, int(shade * 0.68), int(shade * 0.42), 255))
    # warm pool — solid soft amber, single layer
    pool = Image.new("RGBA", desk.size, (0, 0, 0, 0))
    ImageDraw.Draw(pool).ellipse(
        (int(W * 0.08), int(desk.size[1] * 0.02), int(W * 0.62), int(desk.size[1] * 0.62)),
        fill=(170, 125, 70, 90),
    )
    pool = pool.filter(ImageFilter.GaussianBlur(28))
    desk = Image.alpha_composite(desk, pool)
    rgba.alpha_composite(desk, (0, int(H * 0.34)))
    return soft_empty_chairs_once(rgba)


def paint_publish_desk(*, holes: bool) -> Image.Image:
    rgba = base_room()
    paint_lamp(rgba, int(W * 0.13), int(H * 0.40), scale=1.10)
    paint_card_stack(rgba, int(W * 0.22), int(H * 0.72), n=6, scale=1.1)
    paint_card_stack(rgba, int(W * 0.86), int(H * 0.68), n=5, scale=1.0)
    if holes:
        paint_grid_sheet(rgba, int(W * 0.28), int(H * 0.52), int(W * 0.78), int(H * 0.92), holes=True)
    else:
        paint_grid_sheet(rgba, int(W * 0.30), int(H * 0.50), int(W * 0.72), int(H * 0.88), holes=False)
    paint_flask(rgba, int(W * 0.38), int(H * 0.42), liquid=(210, 90, 140), scale=0.95)
    paint_flask(rgba, int(W * 0.48), int(H * 0.40), liquid=(70, 150, 210), scale=1.0)
    paint_flask(rgba, int(W * 0.60), int(H * 0.41), liquid=(60, 180, 90), scale=1.08, sphere=holes)
    paint_flask(rgba, int(W * 0.72), int(H * 0.40), liquid=(150, 70, 200), scale=1.12, sphere=holes)
    paint_mortar(rgba, int(W * 0.52), int(H * 0.48), scale=0.95, color=(235, 230, 220))
    paint_mortar(rgba, int(W * 0.58), int(H * 0.50), scale=1.05, color=(170, 170, 165))
    paint_magnifier(rgba, int(W * 0.78), int(H * 0.58), scale=1.05)
    # NO sharpen on publish — even 1.04 rang as ghost edges for Ben
    return rgba.convert("RGB")


def paint_family_desk() -> Image.Image:
    rgba = base_room()
    paint_lamp(rgba, int(W * 0.14), int(H * 0.38), scale=1.05)
    paint_bookshelf(rgba, x0=int(W * 0.70), y0=int(H * 0.35), x1=W, y1=int(H * 0.78))
    paint_element_card(rgba, (int(W * 0.22), int(H * 0.62)), "H", "1", angle=-8, scale=1.05)
    paint_element_card(rgba, (int(W * 0.40), int(H * 0.56)), "C", "12", angle=5, scale=1.08)
    paint_element_card(rgba, (int(W * 0.58), int(H * 0.58)), "N", "14", angle=-4, scale=1.10)
    paint_element_card(rgba, (int(W * 0.76), int(H * 0.64)), "O", "16", angle=8, scale=1.05)
    return rgba.convert("RGB")


def paint_finished_crown(canvas: Image.Image, hx: int, hy: int) -> None:
    """Finished wavy brown crown — solid mass + soft tufts. NO scribbly blot. NO black dots."""
    hair = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    hd = ImageDraw.Draw(hair)
    # solid scalp + crown mass (opaque)
    hd.ellipse((hx - 54, hy - 58, hx + 52, hy + 28), fill=(118, 70, 40, 255))
    hd.ellipse((hx - 48, hy - 70, hx + 46, hy - 10), fill=(128, 78, 46, 255))
    # soft tufts (filled wedges, not stroke noise)
    tufts = [(-34, -78), (-12, -88), (10, -86), (32, -76), (-22, -60), (20, -58)]
    for i, (ox, oy) in enumerate(tufts):
        col = (105 + (i * 7) % 40, 60 + (i * 5) % 25, 32 + (i * 3) % 15)
        hd.ellipse((hx + ox - 16, hy + oy - 14, hx + ox + 16, hy + oy + 18), fill=(*col, 255))
    # gentle highlight waves (light brown only — never black pins)
    for ox, oy, w in ((-20, -40, 22), (0, -48, 24), (18, -38, 20), (-8, -28, 18)):
        hd.arc(
            (hx + ox - w, hy + oy - 8, hx + ox + w, hy + oy + 14),
            200, 340, fill=(150, 98, 58, 255), width=5,
        )
    # soft blur once so crown reads finished, not scribble
    hair = hair.filter(ImageFilter.GaussianBlur(1.2))
    canvas.alpha_composite(hair)


def paint_explorer_scene(sheet: Image.Image) -> Image.Image:
    """Profile/back Explorer — finished crown, gold glasses rim, clean written cards.

    sheet arg kept for API compatibility / future DNA; do NOT paste rectangular face crops
    (that caused Ben face-cloud blot).
    """
    _ = sheet  # identity lock via paint, not face crop
    rgba = base_room()
    paint_bookshelf(rgba, x0=0, y0=0, x1=W, y1=int(H * 0.55))
    d = ImageDraw.Draw(rgba)
    d.rectangle((0, int(H * 0.55), W, H), fill=(88, 58, 36, 255))
    for i in range(int(H * 0.55), H, 6):
        shade = 88 + ((i // 6) % 8) - 3
        d.rectangle((0, i, W, i + 5), fill=(shade, int(shade * 0.66), int(shade * 0.40), 255))
    paint_lamp(rgba, int(W * 0.12), int(H * 0.42), scale=1.0)

    # clean readable cards — spaced, no garbled overlap
    for i, (sym, wt) in enumerate([("H", "1"), ("C", "12"), ("N", "14"), ("O", "16")]):
        paint_element_card(
            rgba,
            (int(W * (0.50 + i * 0.10)), int(H * 0.74)),
            sym,
            wt,
            angle=(-5 + i * 3),
            scale=0.70,
        )
    paint_flask(rgba, int(W * 0.84), int(H * 0.62), liquid=(90, 170, 200), scale=0.85)
    paint_mortar(rgba, int(W * 0.90), int(H * 0.70), scale=0.9)

    body = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    bd = ImageDraw.Draw(body)
    cx, cy = int(W * 0.42), int(H * 0.52)
    # teal coat 3/4 BACK — face mostly hidden
    bd.ellipse((cx - 70, cy - 20, cx + 90, cy + 160), fill=(28, 78, 78, 255))
    bd.rectangle((cx - 55, cy + 20, cx + 75, cy + 210), fill=(28, 78, 78, 255))
    bd.ellipse((cx + 55, cy + 90, cx + 95, cy + 130), fill=(240, 235, 225, 255))
    bd.polygon(
        [(cx + 40, cy + 40), (cx + 150, cy + 110), (cx + 140, cy + 130), (cx + 30, cy + 70)],
        fill=(28, 78, 78, 255),
    )
    bd.ellipse((cx + 135, cy + 105, cx + 165, cy + 135), fill=(220, 185, 150, 255))
    bd.rectangle((cx - 35, cy + 200, cx - 5, cy + 280), fill=(90, 60, 40, 255))
    bd.rectangle((cx + 25, cy + 200, cx + 55, cy + 280), fill=(90, 60, 40, 255))
    bd.ellipse((cx - 45, cy + 270, cx + 5, cy + 300), fill=(70, 45, 30, 255))
    bd.ellipse((cx + 15, cy + 270, cx + 65, cy + 300), fill=(70, 45, 30, 255))
    bd.ellipse((cx - 100, cy + 60, cx - 40, cy + 140), fill=(120, 80, 45, 255), outline=(70, 45, 25, 255), width=2)

    # head from BACK — hair covers most of scalp; tiny skin ear + gold glasses rim only
    hx, hy = cx + 8, cy - 72
    # neck
    bd.rectangle((hx - 18, hy + 30, hx + 22, hy + 70), fill=(220, 185, 150, 255))
    # ear only (profile cue) — no front face / no eye
    bd.ellipse((hx + 38, hy - 8, hx + 60, hy + 28), fill=(210, 170, 140, 255))
    # gold glasses temple + rim peek (readable gold, not a face blot)
    bd.line((hx + 20, hy + 2, hx + 55, hy + 6), fill=(200, 160, 50, 255), width=4)
    bd.arc((hx + 5, hy - 10, hx + 48, hy + 28), start=200, end=330, fill=(200, 160, 50, 255), width=4)
    rgba = Image.alpha_composite(rgba, body)
    paint_finished_crown(rgba, hx, hy)
    return rgba.convert("RGB")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    QA.mkdir(parents=True, exist_ok=True)
    if not SHEET.exists():
        raise SystemExit(f"missing Explorer sheet {SHEET}")
    sheet = Image.open(SHEET).convert("RGB")
    meta: dict = {
        "parent_v17_sha": PARENT_V17_SHA,
        "bible_main": "25bdefd",
        "plates": {},
        "method": (
            "procedural_single_exposure_v18 — opaque props, ONE soft Empty Chairs rect, "
            "no nested glow, no oversharpen ringing, Explorer crown from sheet + stroke hair "
            "(NOT black-dot spray, NOT face-cloud scrub)"
        ),
        "ben_fail": [
            "publish_ghost",
            "explorer_face",
            "family_lamp_panel",
            "family_cards",
        ],
    }

    mapping = {
        "11_publish_gaps": paint_publish_desk(holes=False),
        "11b_wait_and_hunt": paint_publish_desk(holes=True),
        "10_family_before_weight": paint_family_desk(),
        "06_explorer_leaves_gap": paint_explorer_scene(sheet),
    }
    for pid, im in mapping.items():
        out = OUT / f"{pid}_start_v18.jpg"
        im.save(out, quality=95)
        im.save(QA / f"start_{pid}.jpg", quality=92)
        meta["plates"][pid] = str(out)
        print(f"wrote {out.name}", flush=True)

    META.write_text(json.dumps(meta, indent=2) + "\n")
    print(json.dumps(meta, indent=2), flush=True)
    print("PREP OK", flush=True)


if __name__ == "__main__":
    main()
