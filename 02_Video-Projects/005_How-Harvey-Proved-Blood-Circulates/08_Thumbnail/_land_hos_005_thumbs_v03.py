#!/usr/bin/env python3
"""Land HOS 005 long Thumb C v03 — reletter A painting at £0 (no image model).

Claude desk task (PR #180): Thumb C = TIE IT TIGHT (punch on TIGHT), same tied-arm
painting as A/B. Cover/replace ONLY the left lettering panel; cream + gold house serif.
"""
from __future__ import annotations

import hashlib
import json
import math
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]  # hos-005-blood
ASSETS = HERE / "_assets_v02"
SELECTED = HERE / "Selected"
TOOLS = ROOT / "00_Brand/Channel-Setup/tools"
# Also try History Of Science tools if hos-005-blood tools missing style refs
TOOLS_MAIN = Path.home() / "YouTube/History Of Science/00_Brand/Channel-Setup/tools"

W, H = 1280, 720
SRC_A = ASSETS / "hos_005_thumb_A_one_tight_band_v02c.jpg"
SRC_A_JPG = SELECTED / "hos_005_thumb_A_one_tight_band_v02.jpg"
SRC_B_JPG = SELECTED / "hos_005_thumb_B_it_goes_round_v02.jpg"
PANEL = (40, 0, 540, 378)
FEATHER = 10

CREAM = (242, 210, 165)
GOLD = (220, 150, 35)
INK = (28, 18, 10)
SHADOW = (8, 4, 2)

FONT_CANDIDATES = [
    ("/System/Library/Fonts/Supplemental/Didot.ttc", 2),  # Bold
    ("/System/Library/Fonts/Supplemental/Baskerville.ttc", 1),  # Bold
    ("/System/Library/Fonts/Supplemental/Georgia Bold.ttf", 0),
]


def font(size: int) -> ImageFont.FreeTypeFont:
    for path, index in FONT_CANDIDATES:
        try:
            return ImageFont.truetype(path, size, index=index)
        except OSError:
            try:
                return ImageFont.truetype(path, size)
            except OSError:
                continue
    return ImageFont.load_default()


def tools_dir() -> Path:
    if (TOOLS / "thumb_preview.py").exists():
        return TOOLS
    return TOOLS_MAIN


def save_jpg(im: Image.Image, dest: Path) -> Path:
    dest.parent.mkdir(parents=True, exist_ok=True)
    im.convert("RGB").resize((W, H), Image.Resampling.LANCZOS).save(
        dest, "JPEG", quality=92, optimize=True, subsampling=1
    )
    print(f"  {dest.name}  {dest.stat().st_size} B", flush=True)
    return dest


def cover_lettering(base: Image.Image) -> Image.Image:
    """Fully obscure A lettering in the text column; keep library edges + Explorer hair."""
    import random

    out = base.copy()
    x0, y0, x1, y1 = PANEL
    region = out.crop((x0, y0, x1, y1))
    px = region.load()
    w, h = region.size

    # Dark library samples from left strip (books) — avoid bright lettering
    samples: list[tuple[int, int, int]] = []
    for y in range(h):
        for x in range(0, min(100, w)):
            r, g, b = px[x, y]
            if r + g + b < 160:
                samples.append((r, g, b))
    if not samples:
        samples = [(14, 6, 2)]
    samples.sort(key=lambda c: sum(c))
    mid = samples[len(samples) // 2]
    rnd = random.Random(7)

    # Core text column to wipe hard (leaves side books / curtain)
    wipe_x0, wipe_x1 = 70, w - 30  # relative to panel
    wipe_y0, wipe_y1 = 18, h - 55  # stop above Explorer hair

    plate = region.copy()
    pplate = plate.load()
    for y in range(h):
        for x in range(w):
            in_wipe = wipe_x0 <= x <= wipe_x1 and wipe_y0 <= y <= wipe_y1
            r, g, b = px[x, y]
            bright = r + g + b
            is_letter = bright > 200 or (r > 150 and g > 70 and b < 130 and r > b + 25)
            if in_wipe or is_letter:
                s = samples[rnd.randrange(len(samples))]
                # warm dark average
                pplate[x, y] = (
                    max(0, (s[0] + mid[0]) // 2 - 2),
                    max(0, (s[1] + mid[1]) // 2 - 1),
                    max(0, (s[2] + mid[2]) // 2),
                )
    plate = plate.filter(ImageFilter.GaussianBlur(2.5))

    # Full-opacity wipe mask in the text column; soft edges
    mask = Image.new("L", (w, h), 0)
    md = ImageDraw.Draw(mask)
    md.rectangle([wipe_x0, wipe_y0, wipe_x1, wipe_y1], fill=255)
    # also force cover any remaining bright letter pixels outside wipe
    mpx = mask.load()
    for y in range(h):
        for x in range(w):
            r, g, b = px[x, y]
            bright = r + g + b
            if bright > 220 or (r > 170 and g > 90 and b < 120 and r > b + 30):
                mpx[x, y] = 255
    mask = mask.filter(ImageFilter.GaussianBlur(6))

    covered = Image.composite(plate, region, mask)
    # Feather bottom into Explorer hair / shoulder
    outer = Image.new("L", (w, h), 255)
    od = ImageDraw.Draw(outer)
    for i in range(FEATHER * 4):
        alpha = int(255 * (1 - i / (FEATHER * 4)))
        od.rectangle([0, h - 1 - i, w, h], fill=alpha)
    covered = Image.composite(covered, region, outer)

    out.paste(covered, (x0, y0))
    return out


def paint_word(
    draw: ImageDraw.ImageDraw,
    text: str,
    *,
    cx: int,
    cy: int,
    size: int,
    fill: tuple[int, int, int],
) -> tuple[int, int, int, int]:
    """Cream/gold painted bevel lettering. Returns bbox."""
    f = font(size)
    bbox = draw.textbbox((0, 0), text, font=f)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    x = int(cx - tw / 2)
    y = int(cy - th / 2) - bbox[1]
    stroke = max(4, size // 16)
    for dx, dy in ((5, 6), (3, 4), (1, 2)):
        draw.text((x + dx, y + dy), text, font=f, fill=SHADOW)
    draw.text((x, y), text, font=f, fill=INK, stroke_width=stroke, stroke_fill=INK)
    # slight highlight offset for bevel
    draw.text((x - 1, y - 1), text, font=f, fill=tuple(min(255, c + 25) for c in fill))
    draw.text((x, y), text, font=f, fill=fill)
    return (x, y + bbox[1], x + tw, y + bbox[1] + th)


def draw_flourish(draw: ImageDraw.ImageDraw, cx: int, y: int, half_w: int, *, up: bool) -> None:
    """Thin gold line with diamond tip and small curls (house long-thumb flourish)."""
    color = GOLD
    tip = -10 if up else 10
    # main line
    draw.line([(cx - half_w, y), (cx - 18, y)], fill=color, width=3)
    draw.line([(cx + 18, y), (cx + half_w, y)], fill=color, width=3)
    # diamond tip
    draw.polygon(
        [(cx, y + tip), (cx - 8, y), (cx, y - tip // 3), (cx + 8, y)],
        fill=color,
    )
    # small end curls (simple arcs via short chords)
    for side in (-1, 1):
        ex = cx + side * half_w
        for i in range(6):
            ang = (i / 5) * math.pi * 0.7
            px = ex + side * (6 * math.sin(ang))
            py = y + (1 if up else -1) * (-6 + 6 * math.cos(ang))
            draw.ellipse([px - 1.5, py - 1.5, px + 1.5, py + 1.5], fill=color)


def paint_c_lettering(base: Image.Image) -> Image.Image:
    """TIE / IT / TIGHT — cream, cream, gold punch. Reads at 168×94."""
    im = base.copy()
    draw = ImageDraw.Draw(im)
    # Center of lettering column (PANEL mid-x, mid-upper)
    cx = (PANEL[0] + PANEL[2]) // 2  # 290
    # Three-line stack like A (ONE / TIGHT / BAND)
    lines = [
        ("TIE", CREAM, 92),
        ("IT", CREAM, 92),
        ("TIGHT", GOLD, 108),
    ]
    # Vertical placement: leave room for flourishes + Explorer hair below panel
    top = 48
    gap = 8
    y = top
    boxes = []
    for text, fill, size in lines:
        # advance by approximate line height
        f = font(size)
        bb = draw.textbbox((0, 0), text, font=f)
        th = bb[3] - bb[1]
        cy = y + th // 2
        boxes.append(paint_word(draw, text, cx=cx, cy=cy, size=size, fill=fill))
        y = cy + th // 2 + gap + (14 if text != "TIGHT" else 0)

    # Flourishes above first and below last
    half = 150
    draw_flourish(draw, cx, boxes[0][1] - 18, half, up=True)
    draw_flourish(draw, cx, boxes[-1][3] + 16, half, up=False)
    return im


def check(kind: str, tool: str, jpg: Path, out: Path) -> None:
    tdir = tools_dir()
    cmd = [sys.executable, str(tdir / tool), kind, str(jpg), "--out", str(out)]
    print("$", " ".join(cmd[1:]), flush=True)
    subprocess.check_call(cmd)


def main() -> None:
    if SRC_A.exists():
        a = Image.open(SRC_A).convert("RGB").resize((W, H), Image.Resampling.LANCZOS)
    else:
        a = Image.open(SRC_A_JPG).convert("RGB")

    cleared = cover_lettering(a)
    # debug intermediate
    save_jpg(cleared, HERE / "_work_thumb_c" / "hos_005_thumb_C_cleared_panel_v01.jpg")
    c_im = paint_c_lettering(cleared)
    c_jpg = save_jpg(c_im, SELECTED / "hos_005_thumb_C_tie_it_tight_v01.jpg")

    check("long", "thumb_preview.py", c_jpg, SELECTED / f"{c_jpg.stem}_preview.jpg")

    a_jpg = SRC_A_JPG
    b_jpg = SRC_B_JPG
    sheet_out = SELECTED / "hos_005_thumbs_v03_style_sheet.jpg"
    tdir = tools_dir()
    subprocess.check_call(
        [
            sys.executable,
            str(tdir / "style_sheet.py"),
            "long",
            str(a_jpg),
            str(b_jpg),
            str(c_jpg),
            "--out",
            str(sheet_out),
        ]
    )
    print(f"  STYLE {sheet_out.name}", flush=True)

    sha_a = hashlib.sha256(a_jpg.read_bytes()).hexdigest()
    sha_b = hashlib.sha256(b_jpg.read_bytes()).hexdigest()
    sha_c = hashlib.sha256(c_jpg.read_bytes()).hexdigest()

    idx = {
        "parentTitle": "The Tied Arm That Proved Your Blood Circulates",
        "version": "v03",
        "status": "Thumb C proposed for Claude review. A/B kept. Nothing to Studio T&C yet.",
        "composer": HERE.name + "/" + Path(__file__).name,
        "factLock": "Tight linen band on the upper arm; red (artery) only on the shoulder side, "
        "a wide glowing artery under the skin, stopping at the band; no red below it; "
        "forearm and hand paler below the band (De Motu Cordis ch. 11, FACT_NOTES_v01 row 26).",
        "thumbs": [
            {"id": "A", "hook": "ONE TIGHT BAND", "jpg": f"Selected/{a_jpg.name}", "sha256": sha_a},
            {"id": "B", "hook": "IT GOES ROUND", "jpg": f"Selected/{b_jpg.name}", "sha256": sha_b},
            {
                "id": "C",
                "hook": "TIE IT TIGHT",
                "punch": "TIGHT",
                "jpg": f"Selected/{c_jpg.name}",
                "sha256": sha_c,
                "method": "reletter_A_painting_no_image_model",
            },
        ],
        "sources": ["hos_005_thumb_A_one_tight_band_v02c.jpg", "hos_005_thumb_B_it_goes_round_v01d.jpg"],
        "upload": False,
        "studio": False,
        "studioTestAndCompare": False,
    }
    (HERE / "THUMBS_INDEX_v03.json").write_text(json.dumps(idx, indent=2) + "\n")
    print("  INDEX THUMBS_INDEX_v03.json", flush=True)
    print("  C sha256", sha_c, flush=True)


if __name__ == "__main__":
    main()
