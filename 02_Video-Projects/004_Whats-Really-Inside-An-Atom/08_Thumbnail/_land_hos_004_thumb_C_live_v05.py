#!/usr/bin/env python3
"""HOS 004 thumb C v05 — scale both tiles left, paint 52 / 53.

Ben PASS on A and B v04. C only:
- Scale the two element tiles down and move them left so both sit fully
  in frame, clear of the bottom-right duration badge.
- Paint 52 and 53 inside the tiles, top-left (periodic-table position),
  in the same painted serif treatment as the title. Digits are lining
  figures (Times New Roman Bold) so "52" does not read as 5². Symbols
  stay Georgia Bold, matching THE HIDDEN NUMBER.
- Picture, title treatment, and colours stay.

Nothing to Studio. No upload.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = Path(__file__).resolve().parent
ASSETS = HERE / "_assets_v04"
SELECTED = HERE / "Selected"
PREVIEWS = HERE / "Previews"
PREVIEW_TOOL = (
    Path(__file__).resolve().parents[3]
    / "00_Brand/Channel-Setup/tools/thumb_preview.py"
)

W, H = 1280, 720
CREAM = (245, 232, 200)
GOLD = (232, 178, 48)
INK = (28, 18, 10)
SHADOW = (12, 8, 4)
GEORGIA = "/System/Library/Fonts/Supplemental/Georgia Bold.ttf"
# Lining figures. Georgia Bold's oldstyle "2" is short and read as 5².
TIMES = "/System/Library/Fonts/Supplemental/Times New Roman Bold.ttf"

BLANK = ASSETS / "hos_004_thumb_C_hidden_number_live_v04.png"
STEM = "hos_004_thumb_C_hidden_number_live_v05"

# Outer wooden tiles on the blank plate (measured edges, 29 Sep 2026).
TE_BOX = (528, 92, 848, 655)
I_BOX = (832, 148, 1278, 708)
TE_FACE = (552, 216, 798, 556)
I_FACE = (872, 196, 1184, 588)

# Pair sits just right of the title and above the duration badge.
DEST = (524, 88)
ORIGIN = (TE_BOX[0], TE_BOX[1])
SCALE = 0.72


def xf(x: int, y: int) -> tuple[int, int]:
    return (
        int(round(DEST[0] + (x - ORIGIN[0]) * SCALE)),
        int(round(DEST[1] + (y - ORIGIN[1]) * SCALE)),
    )


def is_title(rgb: tuple[int, int, int]) -> bool:
    r, g, b = rgb
    return r > 190 and g > 120 and r > b + 40


def cover_holes(im: Image.Image) -> Image.Image:
    """Replace the original tiles with a blend of the wood beside them."""
    out = im.copy()
    op = out.load()
    src = im.load()
    hole = Image.new("L", (W, H), 0)
    hd = ImageDraw.Draw(hole)
    for box in (TE_BOX, I_BOX):
        x0, y0, x1, y1 = box
        hd.rectangle((x0 - 4, y0 - 4, x1 + 6, y1 + 8), fill=255)
    hp = hole.load()
    for y in range(H):
        for x in range(560):
            if is_title(src[x, y]):
                hp[x, y] = 0
    for y in range(H):
        x = 0
        while x < W:
            if hp[x, y] == 0:
                x += 1
                continue
            x0 = x
            while x < W and hp[x, y]:
                x += 1
            x1 = x
            left = op[x0 - 1, y] if x0 > 0 else (36, 20, 8)
            right = op[x1, y] if x1 < W else left
            span = max(1, x1 - x0)
            for i, xx in enumerate(range(x0, x1)):
                t = i / span
                op[xx, y] = tuple(int(left[c] * (1 - t) + right[c] * t) for c in range(3))
    soft = out.filter(ImageFilter.GaussianBlur(5))
    out = Image.composite(soft, out, hole.filter(ImageFilter.GaussianBlur(3)))
    bp = im.load()
    op = out.load()
    for y in range(H):
        for x in range(560):
            if is_title(bp[x, y]):
                op[x, y] = bp[x, y]
    return out


def sprite(im: Image.Image, box: tuple[int, int, int, int]) -> tuple[Image.Image, Image.Image]:
    x0, y0, x1, y1 = box
    crop = im.crop(box)
    alpha = Image.new("L", crop.size, 0)
    ap = alpha.load()
    cp = crop.load()
    cw, ch = crop.size
    for y in range(ch):
        for x in range(cw):
            r, g, b = cp[x, y]
            if (r + g + b) // 3 >= 26 or (r > 70 and r > b + 20):
                ap[x, y] = 255
    alpha = alpha.filter(ImageFilter.GaussianBlur(0.6))
    nw = max(1, int(round(cw * SCALE)))
    nh = max(1, int(round(ch * SCALE)))
    return (
        crop.resize((nw, nh), Image.Resampling.LANCZOS),
        alpha.resize((nw, nh), Image.Resampling.LANCZOS),
    )


def paint(
    draw: ImageDraw.ImageDraw,
    text: str,
    x: int,
    y: int,
    size: int,
    fill: tuple[int, int, int],
    path: str,
) -> tuple[int, int, int, int]:
    font = ImageFont.truetype(path, size)
    stroke = max(3, size // 14)
    draw.text((x + 3, y + 4), text, font=font, fill=SHADOW, anchor="lt")
    draw.text((x, y), text, font=font, fill=INK, stroke_width=stroke + 1, stroke_fill=INK, anchor="lt")
    draw.text((x, y), text, font=font, fill=fill, stroke_width=max(2, stroke - 1), stroke_fill=INK, anchor="lt")
    return draw.textbbox((x, y), text, font=font, anchor="lt")


def face_is_light(px, x: int, y: int) -> bool:
    r, g, b = px[x, y]
    return r > 160 and g > 110 and (r + g + b) > 400


def build() -> Image.Image:
    if not BLANK.exists():
        raise SystemExit(f"missing blank plate {BLANK}")
    src = Image.open(BLANK).convert("RGB")
    if src.size != (W, H):
        raise SystemExit(f"blank is {src.size}, expected {(W, H)}")
    base = cover_holes(src)
    for box in (TE_BOX, I_BOX):
        crop, alpha = sprite(src, box)
        pos = xf(box[0], box[1])
        base.paste(crop, pos, alpha)
        print(f"  tile {box} -> {pos} {crop.size} end ({pos[0]+crop.size[0]}, {pos[1]+crop.size[1]})", flush=True)

    draw = ImageDraw.Draw(base)
    px = base.load()
    for sym, num, face, col in (
        ("Te", "52", TE_FACE, CREAM),
        ("I", "53", I_FACE, GOLD),
    ):
        x0, y0, x1, y1 = face
        dx0, dy0 = xf(x0, y0)
        dx1, dy1 = xf(x1, y1)
        fw, fh = dx1 - dx0, dy1 - dy0
        pad = max(8, int(fw * 0.07))
        nx, ny = dx0 + pad, dy0 + pad
        # Nudge onto the parchment if the top-left is still wooden frame.
        for _ in range(12):
            if face_is_light(px, min(W - 1, nx + 8), min(H - 1, ny + 8)):
                break
            ny += 4
        n_size = max(48, int(fh * 0.28))
        paint(draw, num, nx, ny, n_size, col, TIMES)
        s_size = max(64, int(fh * 0.42))
        sf = ImageFont.truetype(GEORGIA, s_size)
        sw = sf.getlength(sym)
        sx = int(dx0 + (fw - sw) / 2)
        sy = int(dy0 + fh * 0.48)
        paint(draw, sym, sx, sy, s_size, col, GEORGIA)
        print(f"  {sym} {num} face ({dx0},{dy0})-({dx1},{dy1}) num@({nx},{ny})", flush=True)

    # Guards: parchment/gold faces end clear of the duration corner.
    # Brown table grain is not a face (it fails g>175 and b>110 together).
    def is_face(rgb: tuple[int, int, int]) -> bool:
        r, g, b = rgb
        return r > 215 and g > 175 and b > 110 and (r - b) > 25

    px = base.load()
    # Old iodine face lived past x=1100. Those pixels must be gone.
    leftovers = []
    for pt in ((1100, 280), (1100, 400), (1180, 360), (1220, 480)):
        if is_face(px[pt]):
            leftovers.append((pt, px[pt]))
    corner_face = sum(
        1
        for y in range(600, H)
        for x in range(1100, W)
        if is_face(px[x, y])
    )
    if leftovers or corner_face:
        raise SystemExit(f"old tile still showing {leftovers} corner={corner_face}")
    print("  GUARD old tile cleared, badge corner empty", flush=True)
    return base


def main() -> None:
    im = build()
    SELECTED.mkdir(parents=True, exist_ok=True)
    PREVIEWS.mkdir(parents=True, exist_ok=True)
    png = SELECTED / f"{STEM}.png"
    jpg = SELECTED / f"{STEM}.jpg"
    im.save(png, "PNG")
    im.save(jpg, "JPEG", quality=90, optimize=True, subsampling=1)
    print(f"  {jpg.name} {jpg.stat().st_size} B", flush=True)
    preview = SELECTED / f"{STEM}_preview.jpg"
    subprocess.check_call(
        [sys.executable, str(PREVIEW_TOOL), "long", str(jpg), "--out", str(preview)]
    )
    (PREVIEWS / "hos_004_thumb_C_hidden_number_preview_v05.jpg").write_bytes(preview.read_bytes())
    print(f"  preview {preview.name}", flush=True)


if __name__ == "__main__":
    main()
