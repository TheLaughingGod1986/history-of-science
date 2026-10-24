#!/usr/bin/env python3
"""£0 deterministic HOS compilation cover builder v02 (J0896).

Implements Chief's ruling on J0878:
- Replaces single-object 'FLASK PROOF' v01 cover with a 3-object painted key-art
  cover in the canonical HOS library house style:
  1) Pasteur's swan-neck flask with sterile golden broth on the left-center table (001)
  2) Glowing gold-foil nuclear atom with orbital rings in center-upper (004)
  3) Harvey's tied arm with stopped red arterial blood above the tight linen band
     and swollen forearm veins on the right (005)
- Hook text: '6 / EXPERIMENTS' (gold punch '6', cream 'EXPERIMENTS') in the upper-left
  ornament column above the canonical Explorer, clear of all three hero objects and
  clear of the bottom-right duration badge.
- Generates compilation_thumb_v02.jpg, PHONE_v02.jpg (thumb_preview.py), and
  STYLE_v02.jpg (style_sheet.py). £0 / 0 credits.
"""
from __future__ import annotations

from collections import deque
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[2]
MAIN_REPO = Path("/Users/benjaminoats/YouTube/History Of Science")
TOOLS = ROOT / "00_Brand" / "Channel-Setup" / "tools"

from build_cover_v01 import (
    CREAM,
    CREAM_HI,
    EXPLORER_BOX,
    GEORGIA,
    GOLD,
    GOLD_HI,
    INK,
    SHADOW,
    TRACKING,
    W,
    H,
    wipe_old_lettering,
)

P_FLASK = (
    MAIN_REPO
    / "02_Video-Projects"
    / "001_How-Did-We-Discover-Germs"
    / "08_Thumbnail"
    / "Selected"
    / "hos_001_thumb_B_swan_neck_v01.jpg"
)
P_ATOM = (
    MAIN_REPO
    / "00_Brand"
    / "Channel-Setup"
    / "style"
    / "long"
    / "004_whats_really_inside_an_atom_A.jpg"
)
P_ARM = (
    MAIN_REPO
    / "02_Video-Projects"
    / "005_How-Harvey-Proved-Blood-Circulates"
    / "08_Thumbnail"
    / "Selected"
    / "hos_005_thumb_A_one_tight_band_v02.jpg"
)


def fill_holes(mask_bool: np.ndarray) -> np.ndarray:
    h, w = mask_bool.shape
    visited = np.zeros((h, w), dtype=bool)
    q: deque[tuple[int, int]] = deque()
    for x in range(w):
        for y in (0, h - 1):
            if not mask_bool[y, x]:
                visited[y, x] = True
                q.append((y, x))
    for y in range(h):
        for x in (0, w - 1):
            if not mask_bool[y, x]:
                visited[y, x] = True
                q.append((y, x))
    while q:
        cy, cx = q.popleft()
        for ny, nx in ((cy - 1, cx), (cy + 1, cx), (cy, cx - 1), (cy, cx + 1)):
            if 0 <= ny < h and 0 <= nx < w and not visited[ny, nx] and not mask_bool[ny, nx]:
                visited[ny, nx] = True
                q.append((ny, nx))
    return ~visited


def render_word_custom(
    text: str,
    size: int,
    fill: tuple[int, int, int],
    fill_hi: tuple[int, int, int],
    condense_x: float = 0.94,
) -> Image.Image:
    f = ImageFont.truetype(GEORGIA, size)
    widths = [f.getbbox(ch)[2] - f.getbbox(ch)[0] + TRACKING for ch in text]
    total = max(1, sum(widths) - TRACKING)
    bb = f.getbbox(text)
    pad = 24
    layer = Image.new("RGBA", (total + pad * 2, bb[3] - bb[1] + pad * 2), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    y0 = pad - bb[1]
    stroke = max(7, size // 10)

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
        (max(1, int(layer.size[0] * condense_x)), layer.size[1]),
        Image.Resampling.LANCZOS,
    )


def make_rgba(rgb_arr: np.ndarray, alpha_arr: np.ndarray, box: tuple[int, int, int, int]) -> Image.Image:
    x0, y0, x1, y1 = box
    rgba = np.zeros((y1 - y0, x1 - x0, 4), dtype=np.uint8)
    rgba[:, :, :3] = np.clip(rgb_arr[y0:y1, x0:x1], 0, 255).astype(np.uint8)
    rgba[:, :, 3] = np.clip(alpha_arr[y0:y1, x0:x1] * 255.0, 0, 255).astype(np.uint8)
    return Image.fromarray(rgba, "RGBA")


def main() -> None:
    for p in (P_FLASK, P_ATOM, P_ARM):
        if not p.exists():
            raise SystemExit(f"Missing source plate: {p}")

    im1_raw = Image.open(P_FLASK).convert("RGB").resize((W, H), Image.Resampling.LANCZOS)
    im1 = np.array(wipe_old_lettering(im1_raw), dtype=np.float32)
    im4 = np.array(Image.open(P_ATOM).convert("RGB").resize((W, H), Image.Resampling.LANCZOS), dtype=np.float32)
    im5 = np.array(Image.open(P_ARM).convert("RGB").resize((W, H), Image.Resampling.LANCZOS), dtype=np.float32)

    # 1. Reconstruct clean library background (1280x720)
    bg = im1.copy()
    m_win = Image.new("L", (W, H), 0)
    ImageDraw.Draw(m_win).polygon([(580, 0), (805, 0), (805, 365), (725, 460), (580, 460)], fill=255)
    mw = np.array(m_win.filter(ImageFilter.GaussianBlur(14)), dtype=np.float32) / 255.0
    bg = bg * (1.0 - mw[:, :, None]) + im5 * mw[:, :, None]

    m_shelf = Image.new("L", (W, H), 0)
    ImageDraw.Draw(m_shelf).polygon(
        [
            (785, 0),
            (1105, 0),
            (1105, 425),
            (975, 425),
            (975, 575),
            (585, 575),
            (585, 445),
            (725, 445),
            (785, 365),
        ],
        fill=255,
    )
    ms = np.array(m_shelf.filter(ImageFilter.GaussianBlur(18)), dtype=np.float32) / 255.0
    clean_patch = im1[140:330, 846:908, :]
    tile_y = np.concatenate([clean_patch, clean_patch[::-1, :, :]], axis=0)
    tile_yx = np.concatenate([tile_y, tile_y[:, ::-1, :]], axis=1)
    th, tw = tile_yx.shape[:2]
    shelf_fill = bg.copy()
    for y in range(0, 580):
        sy = y % th
        for x in range(580, 1110):
            sx = (x - 580) % tw
            shade = 0.78 + 0.26 * max(0.0, (x - 750) / 360.0)
            shelf_fill[y, x] = tile_yx[sy, sx] * shade
    shelf_blur = np.array(
        Image.fromarray(np.clip(shelf_fill, 0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(2.5)),
        dtype=np.float32,
    )
    bg = bg * (1.0 - ms[:, :, None]) + shelf_blur * ms[:, :, None]

    m_table = Image.new("L", (W, H), 0)
    ImageDraw.Draw(m_table).rectangle((585, 560, 975, 700), fill=255)
    mt = np.array(m_table.filter(ImageFilter.GaussianBlur(14)), dtype=np.float32) / 255.0
    table_fill = bg.copy()
    for y in range(550, 710):
        left_c = bg[y, 535:575, :].mean(axis=0)
        right_c = bg[y, 985:1035, :].mean(axis=0)
        for x in range(580, 985):
            t = (x - 580.0) / 405.0
            gx = 340 + ((x - 580) % 210)
            detail = im1[y, gx] - im1[y, max(0, gx - 12) : min(W, gx + 12)].mean(axis=0)
            table_fill[y, x] = left_c * (1.0 - t) + right_c * t + detail * 0.5
    bg = bg * (1.0 - mt[:, :, None]) + table_fill * mt[:, :, None]

    # 2. Extract Tied Arm (005)
    arm_poly_im = Image.new("L", (W, H), 0)
    ImageDraw.Draw(arm_poly_im).polygon(
        [
            (865, 0),
            (1160, 0),
            (1150, 220),
            (1238, 395),
            (1205, 515),
            (1125, 500),
            (1055, 565),
            (955, 625),
            (600, 690),
            (400, 688),
            (322, 612),
            (322, 555),
            (410, 450),
            (560, 465),
            (685, 508),
            (775, 445),
            (828, 360),
            (826, 240),
        ],
        fill=255,
    )
    arm_roi = np.array(arm_poly_im) > 128
    r5, g5, b5 = im5[:, :, 0], im5[:, :, 1], im5[:, :, 2]
    arm_raw = arm_roi & (
        ((r5 > 76) & (b5 > 26) & ((r5 + g5 + b5) > 145))
        | ((r5 > 92) & ((r5 - b5) > 38) & (np.arange(H)[:, None] < 565))
    )
    palm_core_im = Image.new("L", (W, H), 0)
    ImageDraw.Draw(palm_core_im).polygon(
        [
            (440, 485),
            (565, 505),
            (695, 520),
            (920, 390),
            (1095, 450),
            (1025, 565),
            (885, 625),
            (620, 678),
            (405, 672),
            (332, 592),
            (390, 585),
            (445, 585),
        ],
        fill=255,
    )
    arm_raw = arm_raw | (np.array(palm_core_im) > 128)
    arm_closed = np.array(Image.fromarray((arm_raw * 255).astype(np.uint8)).filter(ImageFilter.MaxFilter(5))) > 128
    arm_closed[0, 875:1145] = True
    arm_solid = fill_holes(arm_closed) & arm_roi
    arm_alpha = (
        np.array(
            Image.fromarray((arm_solid * 255).astype(np.uint8))
            .filter(ImageFilter.MinFilter(3))
            .filter(ImageFilter.GaussianBlur(2.0)),
            dtype=np.float32,
        )
        / 255.0
    )

    # 3. Extract Swan-Neck Flask (001)
    im1_orig = np.array(im1_raw, dtype=np.float32)
    flask_poly_im = Image.new("L", (W, H), 0)
    ImageDraw.Draw(flask_poly_im).polygon(
        [
            (725, 160),
            (722, 85),
            (755, 30),
            (885, 30),
            (935, 80),
            (958, 220),
            (968, 335),
            (1022, 345),
            (1048, 255),
            (1102, 265),
            (1088, 365),
            (1035, 405),
            (968, 405),
            (925, 355),
            (905, 220),
            (865, 100),
            (805, 95),
            (788, 200),
            (805, 325),
            (895, 435),
            (952, 520),
            (950, 590),
            (908, 650),
            (842, 674),
            (712, 674),
            (645, 648),
            (602, 588),
            (604, 510),
            (655, 420),
            (712, 340),
            (726, 250),
        ],
        fill=255,
    )
    flask_roi = np.array(flask_poly_im) > 128
    r1, g1, b1 = im1_orig[:, :, 0], im1_orig[:, :, 1], im1_orig[:, :, 2]
    flask_rim = flask_roi & ((r1 > 62) & ((r1 - b1) > 22) & ((r1 + g1 + b1) > 115))
    rim_im = Image.fromarray((flask_rim * 255).astype(np.uint8))
    ImageDraw.Draw(rim_im).line([(1050, 262), (1098, 274)], fill=255, width=6)
    ImageDraw.Draw(rim_im).line([(655, 652), (715, 671), (840, 671), (900, 652)], fill=255, width=6)
    rim_closed = np.array(rim_im.filter(ImageFilter.MaxFilter(5))) > 128
    flask_solid = fill_holes(rim_closed) & flask_roi
    flask_outer = (
        np.array(
            Image.fromarray((flask_solid * 255).astype(np.uint8))
            .filter(ImageFilter.MinFilter(3))
            .filter(ImageFilter.GaussianBlur(1.8)),
            dtype=np.float32,
        )
        / 255.0
    )
    bright_glass = np.clip((r1 + g1 - 85.0) / 130.0, 0.0, 1.0)
    broth_mask = np.clip((np.arange(H)[:, None] - 475.0) / 20.0, 0.0, 1.0)
    flask_alpha = flask_outer * np.maximum(0.85, np.maximum(bright_glass, broth_mask))

    # 4. Extract Gold-Foil Atom (004) using fitted 3 ellipses + 5 electron spheres + central nucleus
    r4, g4, b4 = im4[:, :, 0], im4[:, :, 1], im4[:, :, 2]
    yy, xx = np.ogrid[:H, :W]
    nuc_dist = np.sqrt((xx - 848.0) ** 2 + (yy - 344.0) ** 2)
    nuc_mask = np.clip((102.0 - nuc_dist) / 5.0, 0.0, 1.0)

    geom_im = Image.new("L", (W, H), 0)
    gd = ImageDraw.Draw(geom_im)
    t_pts = np.linspace(0, 2 * np.pi, 720, endpoint=True)
    for cx_e, cy_e, a_e, b_e, deg_e in [
        (860.0, 336.0, 318.0, 122.0, 91.5),
        (863.0, 345.0, 316.0, 116.0, 30.0),
        (886.0, 332.0, 336.0, 110.0, -32.5),
    ]:
        th_e = np.deg2rad(deg_e)
        ct_e, st_e = np.cos(th_e), np.sin(th_e)
        pts = [
            (
                float(cx_e + a_e * np.cos(ang) * ct_e - b_e * np.sin(ang) * st_e),
                float(cy_e + a_e * np.cos(ang) * st_e + b_e * np.sin(ang) * ct_e),
            )
            for ang in t_pts
        ]
        gd.line(pts, fill=255, width=24, joint="curve")

    for ex, ey, er in [
        (778, 157, 32),
        (1059, 131, 34),
        (635, 306, 33),
        (643, 514, 31),
        (939, 542, 32),
    ]:
        gd.ellipse((ex - er, ey - er, ex + er, ey + er), fill=255)

    corridor = np.array(geom_im.filter(ImageFilter.MaxFilter(15)).filter(ImageFilter.GaussianBlur(3.0)), dtype=np.float32) / 255.0
    core_tube = np.array(geom_im.filter(ImageFilter.GaussianBlur(2.2)), dtype=np.float32) / 255.0
    gold_edge = np.clip(((r4 - b4) - 25.0) / 35.0, 0.0, 1.0) * np.clip((r4 - 85.0) / 60.0, 0.0, 1.0) * corridor
    tube_alpha = np.maximum(core_tube * 0.92, gold_edge)
    glow_mask = np.clip((155.0 - nuc_dist) / 55.0, 0.0, 1.0) * np.clip((r4 - 75.0) / 90.0, 0.0, 1.0) * 0.65
    atom_alpha = np.maximum(nuc_mask, np.maximum(tube_alpha, glow_mask))

    flask_rgba = make_rgba(im1_orig, flask_alpha, (595, 28, 1104, 678))
    atom_rgb_boost = np.clip(im4 * 1.08, 0, 255)
    atom_rgba = make_rgba(atom_rgb_boost, atom_alpha, (558, 14, 1200, 665))
    arm_rgba = make_rgba(im5, arm_alpha, (322, 0, 1238, 694))

    canvas = Image.fromarray(np.clip(bg, 0, 255).astype(np.uint8), "RGB").convert("RGBA")

    # Place 1: Gold-Foil Atom in center-upper (x=618..973, y=18..373)
    atom_resized = atom_rgba.resize((355, 355), Image.Resampling.LANCZOS)
    tmp = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    tmp.paste(atom_resized, (618, 18), atom_resized)
    canvas = Image.alpha_composite(canvas, tmp)

    # Place 2: Swan-Neck Flask on left-center table (x=330..635, y=268..678)
    flask_resized = flask_rgba.resize((305, 410), Image.Resampling.LANCZOS)
    tmp = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    tmp.paste(flask_resized, (330, 268), flask_resized)
    canvas = Image.alpha_composite(canvas, tmp)

    # Place 3: Tied Arm on right (anchored at y=0, x=595..1275, y=0..632)
    arm_resized = arm_rgba.resize((680, 632), Image.Resampling.LANCZOS)
    tmp = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    tmp.paste(arm_resized, (595, 0), arm_resized)
    canvas = Image.alpha_composite(canvas, tmp)

    # Place 4: Hook Text '6 / EXPERIMENTS' in upper-left ornament column (cx=264, y=62..308)
    lines = [
        ("6", "gold", 142, 0.94),
        ("EXPERIMENTS", "cream", 68, 0.78),
    ]
    sprites = []
    for text, kind, size, cond_x in lines:
        fill, hi = (CREAM, CREAM_HI) if kind == "cream" else (GOLD, GOLD_HI)
        sprites.append((text, kind, size, render_word_custom(text, size, fill, hi, condense_x=cond_x)))

    gap = 8
    total_h = sum(s[3].size[1] for s in sprites) + gap * (len(sprites) - 1)
    y = 62 + max(0, (244 - total_h) // 2)
    cx = 264
    placed = []
    for idx_line, (text, kind, size, spr) in enumerate(sprites):
        left_x = int(round(cx - spr.size[0] / 2))
        tmp = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        tmp.paste(spr, (left_x, y), spr)
        canvas = Image.alpha_composite(canvas, tmp)
        placed.append(
            {
                "word": text,
                "kind": kind,
                "size": size,
                "box": [left_x, y, left_x + spr.size[0], y + spr.size[1]],
            }
        )
        y += spr.size[1] + gap

    left = min(p["box"][0] for p in placed)
    right = max(p["box"][2] for p in placed)
    top = min(p["box"][1] for p in placed)
    bottom = max(p["box"][3] for p in placed)
    assert bottom < EXPLORER_BOX[1], f"Lettering {bottom} overlaps Explorer {EXPLORER_BOX[1]}"

    thumb = OUT / "compilation_thumb_v02.jpg"
    phone = OUT / "PHONE_v02.jpg"
    style = OUT / "STYLE_v02.jpg"
    canvas.convert("RGB").save(thumb, "JPEG", quality=93, optimize=True, subsampling=1)

    subprocess.check_call([sys.executable, str(TOOLS / "thumb_preview.py"), "long", str(thumb), "--out", str(phone)])
    subprocess.check_call([sys.executable, str(TOOLS / "style_sheet.py"), "long", str(thumb), "--out", str(style)])
    print(f"SAVED {thumb} box=[{left}, {top}, {right}, {bottom}]")


if __name__ == "__main__":
    main()
