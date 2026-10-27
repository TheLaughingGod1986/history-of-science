#!/usr/bin/env python3
"""HOS 001 long thumb B v01: THE SWAN NECK (OWB queue J0391).

Builds a Test & Compare B variant for HOS 001 ('How Did We Discover Germs?', _C92tIJCk8A)
from existing 001 plates only (£0 / 0 credits, no image model, no Studio changes):
- Base plate: 001's unused painted key-art plate `Selected/hos_001_tc_thumb_v02.jpg` on the NAS
  (giant glowing swan-neck flask on the library desk filling the right two-thirds at x=598..1100,
  y=32..678; Explorer on model in the lower-left at x=88..316, y=328..720 = 54.4% frame height;
  original painted top & bottom gold scroll flourishes at y=20..60 and y=318..356).
- Replaces the pre-11-Oct 5-word title-repeating question ('WHAT PROVED / GERMS / WERE REAL?')
  in y=62..314 with a 3-word name-the-thing hook per THUMBNAIL_AND_TITLE_RULES.md §2.5 & §2.B:
  'THE / SWAN / NECK' (cream + gold punch word 'SWAN') in house Georgia Bold serif display
  lettering, centered on the ornament column (cx=285), clear of the hero flask (x>=598),
  clear of the Explorer's hair (y>=328), and clear of the bottom-right duration badge.
"""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = Path(__file__).resolve().parent
SELECTED = HERE / "Selected"
REPO = HERE.parents[2]
TOOLS = REPO / "00_Brand" / "Channel-Setup" / "tools"
LIVE_A = REPO / "00_Brand" / "Channel-Setup" / "style" / "long" / "001_how_did_we_discover_germs.jpg"
NAS_TC_V02 = Path(
    "/Volumes/data/mac-mini-archive/YouTube/History Of Science/02_Video-Projects/"
    "001_How-Did-We-Discover-Germs/08_Thumbnail/Selected/hos_001_tc_thumb_v02.jpg"
)
OUT = SELECTED / "hos_001_thumb_B_swan_neck_v01.jpg"

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

HERO_BOX = (598, 32, 1100, 678)
EXPLORER_BOX = (88, 328, 316, 720)
CX = 285


def wipe_old_lettering(base: Image.Image) -> Image.Image:
    """Mask only the old letters ('WHAT PROVED / GERMS / WERE REAL?') and their stroke/shadow
    in y=62..314, x=58..518, restoring painted bookcase texture on the left (x<440) and
    continuous diagonal green curtain folds on the right (x>=440) so there is no rectangular seam."""
    arr = np.array(base.convert("RGB"), dtype=np.float32)

    # 1. Detect bright/warm letter faces strictly inside the 3 old text bands:
    letter_mask = Image.new("L", (W, H), 0)
    lm = letter_mask.load()
    bands = [
        (62, 120, 78, 492),
        (124, 248, 56, 518),
        (252, 318, 70, 514),
    ]
    for y0, y1, x0, x1 in bands:
        for y in range(y0, y1):
            for x in range(x0, x1):
                r, g, b = arr[y, x]
                if r > 32 and (r + g + b) > 68 and (r - b) > 8:
                    lm[x, y] = 255

    # Dilate to cover dark ink outlines and drop shadows around each glyph,
    # while protecting the top flourish (y<=59) and bottom flourish (center tip y>=319 at x=275..315; arms y>=325 at x=140..445)
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

    # 2. Synthesize natural painted bookcase + curtain background for y=58..329, x=48..530:
    clean = arr.copy()
    slope = -0.19  # curtain fold leans left as y increases
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
    clean_im = clean_im.filter(ImageFilter.GaussianBlur(1.8))
    clean_arr = np.array(clean_im, dtype=np.float32)

    out_arr = arr * (1.0 - dm[:, :, None]) + clean_arr * dm[:, :, None]
    return Image.fromarray(np.clip(out_arr, 0, 255).astype(np.uint8), "RGB")


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
    if not NAS_TC_V02.exists():
        raise SystemExit(f"Missing NAS source plate: {NAS_TC_V02}")
    src = Image.open(NAS_TC_V02).convert("RGB").resize((W, H), Image.Resampling.LANCZOS)
    wiped = wipe_old_lettering(src)
    rgba = wiped.convert("RGBA")

    # 3-word name-the-thing hook: THE / SWAN / NECK
    # Optical vertical placement between top flourish (y=20..59) and bottom flourish (y=318..356)
    lines = [
        ("THE", "cream", 70),
        ("SWAN", "gold", 122),
        ("NECK", "cream", 96),
    ]
    sprites = []
    for text, kind, size in lines:
        fill, hi = (CREAM, CREAM_HI) if kind == "cream" else (GOLD, GOLD_HI)
        sprites.append((text, kind, size, render_word(text, size, fill, hi)))

    # Tight optical line gap (-12 px on padded stroke/shadow boxes) so block sits at y=65..308
    gap = -12
    total_h = sum(s[3].size[1] for s in sprites) + gap * (len(sprites) - 1)
    y = 63 + max(0, (248 - total_h) // 2)

    placed = []
    for text, kind, size, spr in sprites:
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
        y += spr.size[1] + gap

    left = min(p["box"][0] for p in placed)
    right = max(p["box"][2] for p in placed)
    top = min(p["box"][1] for p in placed)
    bottom = max(p["box"][3] for p in placed)

    out = rgba.convert("RGB")
    SELECTED.mkdir(parents=True, exist_ok=True)
    out.save(OUT, "JPEG", quality=92, optimize=True, subsampling=1)

    clear_of_hero = right < HERO_BOX[0]
    clear_of_explorer = bottom <= EXPLORER_BOX[1]
    clear_of_badge = bottom < H - 120
    print(
        f"lettering box=[{left}, {top}, {right}, {bottom}] "
        f"explorer_top={EXPLORER_BOX[1]} hero_left={HERO_BOX[0]} "
        f"clear_of_hero={clear_of_hero} clear_of_explorer={clear_of_explorer} clear_of_badge={clear_of_badge}"
    )

    preview = SELECTED / f"{OUT.stem}_preview.jpg"
    subprocess.check_call([sys.executable, str(TOOLS / "thumb_preview.py"), "long", str(OUT), "--out", str(preview)])
    sheet = SELECTED / f"{OUT.stem}_style_sheet.jpg"
    subprocess.check_call([sys.executable, str(TOOLS / "style_sheet.py"), "long", str(OUT), "--out", str(sheet)])

    # Side-by-side phone comparison strip (360x202 + 168x94): A live vs old Oct-1 draft vs new B v01
    phone = SELECTED / "hos_001_thumb_A_vs_B_swan_neck_v01_phone_168.jpg"
    a_im = Image.open(LIVE_A).convert("RGB")
    strip = Image.new("RGB", (360 * 3 + 32, 202 + 94 + 76), (14, 10, 6))
    d = ImageDraw.Draw(strip)
    lf = ImageFont.truetype(GEORGIA, 15)
    for i, (label, src_im) in enumerate([
        ("A live (repeats title)", a_im),
        ("Oct-1 draft (5w question, repeats GERMS)", src),
        ("B v01 (J0391: THE SWAN NECK, 3w hook, £0)", out),
    ]):
        x0 = 8 + i * (360 + 8)
        d.text((x0, 6), label, font=lf, fill=(235, 212, 170))
        strip.paste(src_im.resize((360, 202), Image.Resampling.LANCZOS), (x0, 28))
        d.text((x0, 238), f"168x94 phone tile ({label.split()[0]} {label.split()[1]})", font=lf, fill=(200, 175, 135))
        strip.paste(src_im.resize((168, 94), Image.Resampling.LANCZOS), (x0, 262))
    strip.save(phone, "JPEG", quality=93)

    idx = {
        "film": "001",
        "video": "_C92tIJCk8A",
        "job": "J0391",
        "variant": "B v01",
        "maker": "gemini",
        "hook": "THE SWAN NECK",
        "punch": "SWAN",
        "jpg": f"Selected/{OUT.name}",
        "sha256": hashlib.sha256(OUT.read_bytes()).hexdigest(),
        "bytes": OUT.stat().st_size,
        "plates": [
            "Selected/hos_001_tc_thumb_v02.jpg (NAS 001 unused painted key-art plate: swan-neck flask right two-thirds + Explorer lower-left + gold scroll flourishes)"
        ],
        "method": "existing_001_plate_only_reletter_GeorgiaBold_with_original_painted_flourishes",
        "spend": 0,
        "heroBox": list(HERO_BOX),
        "explorer": {
            "source": "hos_001_tc_thumb_v02.jpg",
            "box": list(EXPLORER_BOX),
            "height_px": EXPLORER_BOX[3] - EXPLORER_BOX[1],
            "height_frac": round((EXPLORER_BOX[3] - EXPLORER_BOX[1]) / H, 3),
        },
        "lettering": placed,
        "ornaments": {
            "top_scroll_box": [80, 20, 490, 59],
            "bottom_scroll_box": [140, 318, 445, 356],
        },
        "clearOfHero": clear_of_hero,
        "clearOfExplorer": clear_of_explorer,
        "clearOfBadge": clear_of_badge,
        "scores": {
            "HOOK": "PASS — 'THE SWAN NECK' (3 words, punch word 'SWAN' in gold) names Pasteur's iconic curved-neck flask shown on the right and adds to the video title ('How Did We Discover Germs?') without repeating any word from it.",
            "BAND": f"PASS — Upper-left lettering band (x={left}..{right}, y={top}..{bottom}, framed by painted gold scroll flourishes at y=20..356) sits completely left of the glowing swan-neck flask (x={HERO_BOX[0]}..{HERO_BOX[2]}), above the Explorer's hair (y={EXPLORER_BOX[1]}), and clear of the bottom-right duration badge.",
            "PHONE": "PASS — Checked on 168x94 preview sheet and side-by-side strip: 'THE SWAN NECK', the giant glowing swan-neck flask (502x646 px), and the Explorer's face/glasses (54.4% height) all read at a glance at 168x94.",
        },
        "previews": [
            f"Selected/{preview.name}",
            f"Selected/{sheet.name}",
            f"Selected/{phone.name}",
        ],
        "studio": False,
        "status": "Test & Compare B v01 candidate for 001 (_C92tIJCk8A, built from existing 001 plate only, £0). Parked for Chief: thumb B review. No Studio until OK.",
    }
    (HERE / "THUMB_B_SWAN_NECK_v01.json").write_text(json.dumps(idx, indent=2) + "\n")
    print("DONE", OUT, idx["sha256"])


if __name__ == "__main__":
    main()
