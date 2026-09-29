#!/usr/bin/env python3
"""HOS 004 thumb C v06 — painted title lettering + bigger Te / I.

Ben back 29 Sep 2026:
- Numbers 52 / 53 in the SAME painted lettering as THE HIDDEN NUMBER (Georgia Bold
  cream/gold bevel), top-left inside each tile.
- Te and I much bigger — fill the tile.
- Everything else stays (scaled-left tiles, clear bottom-right).

Nothing to Studio. No KEEP/LOCKED. No upload.
"""
from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = Path(__file__).resolve().parent
ASSETS_V04 = HERE / "_assets_v04"
ASSETS = HERE / "_assets_v06"
SELECTED = HERE / "Selected"
PREVIEWS = HERE / "Previews"
PREVIEW_TOOL = (
    Path(__file__).resolve().parents[3]
    / "00_Brand/Channel-Setup/tools/thumb_preview.py"
)
ICLOUD = (
    Path.home()
    / "Library/Mobile Documents/com~apple~CloudDocs/HOS UAT"
    / "004_Whats-Really-Inside-An-Atom/08_Thumbnail/Selected"
)
WALK = Path(
    "/Users/benjaminoats/Library/Application Support/Cursor/AgentStores/"
    "cursor_agent_stores/bc-958ae0f3-be07-568f-a2ab-eb7f422d8839/files/artifacts"
)

W, H = 1280, 720
CREAM = (245, 232, 200)
GOLD = (232, 178, 48)
INK = (28, 18, 10)
SHADOW = (12, 8, 4)
GEORGIA = "/System/Library/Fonts/Supplemental/Georgia Bold.ttf"

BLANK = ASSETS_V04 / "hos_004_thumb_C_hidden_number_live_v04.png"
STEM = "hos_004_thumb_C_hidden_number_live_v06"

TE_BOX = (528, 92, 848, 655)
I_BOX = (832, 148, 1278, 708)
TE_FACE = (552, 216, 798, 556)
I_FACE = (872, 196, 1184, 588)

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


def paint_word(
    draw: ImageDraw.ImageDraw,
    text: str,
    *,
    cx: int,
    cy: int,
    size: int,
    fill: tuple[int, int, int],
) -> None:
    """Same cream/gold painted bevel as THE HIDDEN NUMBER / live 001/002."""
    f = ImageFont.truetype(GEORGIA, size)
    tw = f.getlength(text)
    x = int(cx - tw / 2)
    y = int(cy - size / 2)
    for dx, dy in ((4, 5), (2, 3)):
        draw.text((x + dx, y + dy), text, font=f, fill=SHADOW)
    draw.text((x, y), text, font=f, fill=INK, stroke_width=max(3, size // 18), stroke_fill=INK)
    draw.text((x, y), text, font=f, fill=fill)


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
        # Top-left number, same painted Georgia as the title.
        pad = max(6, int(fw * 0.06))
        nx = dx0 + pad + int(fw * 0.18)
        ny = dy0 + pad + int(fh * 0.12)
        for _ in range(12):
            if face_is_light(px, min(W - 1, nx), min(H - 1, ny)):
                break
            ny += 4
        n_size = max(36, int(fh * 0.18))
        paint_word(draw, num, cx=nx, cy=ny, size=n_size, fill=col)
        # Symbol fills the tile.
        s_size = max(120, int(min(fw * 0.72, fh * 0.62)))
        sx = dx0 + fw // 2
        sy = dy0 + int(fh * 0.58)
        paint_word(draw, sym, cx=sx, cy=sy, size=s_size, fill=col)
        print(
            f"  {sym} {num} face ({dx0},{dy0})-({dx1},{dy1}) "
            f"num@({nx},{ny}) s={s_size}",
            flush=True,
        )

    def is_face(rgb: tuple[int, int, int]) -> bool:
        r, g, b = rgb
        return r > 215 and g > 175 and b > 110 and (r - b) > 25

    px = base.load()
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
    print(f"  leftovers_far_right={leftovers} corner_face_px={corner_face}", flush=True)
    if leftovers or corner_face > 40:
        raise SystemExit("C v06 still occupies bottom-right / far-right — abort")
    return base


def save(im: Image.Image) -> None:
    ASSETS.mkdir(parents=True, exist_ok=True)
    SELECTED.mkdir(parents=True, exist_ok=True)
    PREVIEWS.mkdir(parents=True, exist_ok=True)
    png = SELECTED / f"{STEM}.png"
    jpg = SELECTED / f"{STEM}.jpg"
    im.save(png)
    im.convert("RGB").save(jpg, quality=92, optimize=True)
    (ASSETS / f"{STEM}_blank.png").write_bytes(png.read_bytes())
    preview = SELECTED / f"{STEM}_preview.jpg"
    subprocess.run(
        [sys.executable, str(PREVIEW_TOOL), "long", str(jpg), "--out", str(preview)],
        check=True,
    )
    sheet = PREVIEWS / "hos_004_thumb_C_hidden_number_preview_v06.jpg"
    shutil.copy2(preview, sheet)
    ICLOUD.mkdir(parents=True, exist_ok=True)
    for src in (jpg, preview):
        try:
            shutil.copy2(src, ICLOUD / src.name)
        except OSError as e:
            print(f"  iCloud warn {src.name}: {e}", flush=True)
    WALK.mkdir(parents=True, exist_ok=True)
    shutil.copy2(jpg, WALK / jpg.name)
    shutil.copy2(preview, WALK / preview.name)
    print(f"SAVED {jpg}", flush=True)
    print(f"PREVIEW {preview}", flush=True)


def main() -> None:
    print("C v06 — bigger Te/I + painted Georgia 52/53", flush=True)
    save(build())


if __name__ == "__main__":
    main()
