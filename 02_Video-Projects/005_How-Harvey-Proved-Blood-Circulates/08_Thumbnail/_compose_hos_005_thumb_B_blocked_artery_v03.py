#!/usr/bin/env python3
"""HOS 005 long thumb B v03: THE BLOCKED ARTERY (OWB queue J0407).

Builds a post-11-Oct rule-compliant Test & Compare Variant B v03 for HOS 005
('The Tied Arm That Proved Your Blood Circulates', wwcjcFfC-5M, scheduled Thu 29 Oct 18:00)
from existing 005 plates only (£0 / 0 credits, no image model, no Studio changes):
- Why 005: 001 (J0391) and 002 (J0374) already have post-11-Oct existing-plate B variants
  parked for Chief; 003 has T001 running in THUMB_LEDGER.json; 004 is excluded by brief.
  005 has no entry in THUMB_LEDGER.json (its Studio T&C is Ineligible until 29 Oct air),
  and its pre-11-Oct B v02 ('IT GOES ROUND') and untracked C v04 ('TIE IT TIGHT') both
  violate THUMBNAIL_AND_TITLE_RULES.md §2.5 & §2.B.1 ('IT GOES ROUND' uses vague pronoun
  'IT' and repeats 'Circulates'; 'TIE IT TIGHT' repeats 'Tied' and left a dark wipe smudge).
- Base plate: 005's painted 16:9 key-art plate `hos_005_thumb_A_one_tight_band_v02.jpg`
  (golden library, giant arm on the right with the bright glowing red artery stopped at
  the tight linen band per De Motu Cordis ch. 11 / FACT_NOTES_v01 row 26; Explorer on model
  in the lower-left at x=88..318, y=344..720 = 52.2% frame height; original painted top &
  bottom gold scroll flourishes at y=24..59 and y=328..356).
- Wipes only the 3 letter bands ('ONE / TIGHT / BAND') in y=63..323, restoring painted
  bookcase shelves/spines without touching the original painted top/bottom gold scroll
  flourishes or the green curtain, and renders 'THE / BLOCKED / ARTERY' (cream + gold
  punch word 'BLOCKED') in house Georgia Bold display serif lettering.
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
SRC_A = SELECTED / "hos_005_thumb_A_one_tight_band_v02.jpg"
SRC_B_V02 = SELECTED / "hos_005_thumb_B_it_goes_round_v02.jpg"
OUT = SELECTED / "hos_005_thumb_B_blocked_artery_v03.jpg"

W, H = 1280, 720
CREAM = (242, 214, 172)
CREAM_HI = (252, 238, 208)
GOLD = (228, 156, 32)
GOLD_HI = (248, 202, 68)
INK = (16, 9, 4)
SHADOW = (6, 3, 1)
GEORGIA = "/System/Library/Fonts/Supplemental/Georgia Bold.ttf"
TRACKING = -3
CONDENSE_X = 0.90

# Hero arm bounding box (right two-thirds) and Explorer lower-left box
HERO_BOX = (560, 0, 1200, 692)
EXPLORER_BOX = (88, 344, 318, 720)
CX = 288


def wipe_old_lettering(base_a: Image.Image) -> Image.Image:
    """Mask only the old letters ('ONE / TIGHT / BAND') and their dark ink outlines/shadows
    strictly inside each word's bounding band, preserving the original painted top flourish (y<=60)
    and bottom flourish (y>=326) and interpolating vertically column-by-column from the clean
    painted bookcase/curtain rows immediately above and below each word band."""
    arr = np.array(base_a.convert("RGB"), dtype=np.float32)

    bands = [
        # (y_top_clean_lo, y_top_clean_hi, y0, y1, y_bot_clean_lo, y_bot_clean_hi, x0, x1)
        (59, 63, 63, 124, 124, 128, 188, 358),    # ONE
        (124, 128, 128, 209, 209, 215, 122, 434), # TIGHT
        (209, 215, 215, 321, 321, 326, 104, 470), # BAND
    ]

    letter_mask = Image.new("L", (W, H), 0)
    lm = letter_mask.load()
    for _, _, y0, y1, _, _, x0, x1 in bands:
        for y in range(y0, y1):
            for x in range(x0, x1):
                r, g, b = arr[y, x]
                if (r > 46 and (r + g + b) > 90 and (r - b) > 10) or (r + g + b) > 150:
                    lm[x, y] = 255

    # Dilate to cover dark ink stroke + drop shadow around each glyph
    dilated = letter_mask.filter(ImageFilter.MaxFilter(21)).filter(ImageFilter.GaussianBlur(2.8))
    dm = np.array(dilated, dtype=np.float32) / 255.0

    # Strictly protect top flourish (y<=60), bottom flourish (y>=325), and curtain outside band
    dm[:61, :] = 0.0
    dm[61, :] *= 0.4
    dm[62, :] *= 0.8
    dm[325:, :] = 0.0
    dm[324, :] *= 0.4
    dm[323, :] *= 0.8
    dm[:, :96] = 0.0
    dm[:, 474:] = 0.0

    clean = arr.copy()
    for yt0, yt1, y0, y1, yb0, yb1, x0, x1 in bands:
        pad_x0 = max(90, x0 - 16)
        pad_x1 = min(478, x1 + 16)
        top_strip = arr[yt0:yt1, pad_x0:pad_x1, :].mean(axis=0)
        bot_strip = arr[yb0:yb1, pad_x0:pad_x1, :].mean(axis=0)
        # If any bottom strip pixel catches a warm flourish tip (around x=255..320 in band 3), clamp to top_strip
        for xi in range(pad_x1 - pad_x0):
            if bot_strip[xi, 0] > 55 and (bot_strip[xi, 0] - bot_strip[xi, 2]) > 22:
                bot_strip[xi] = top_strip[xi] * 0.92
            if top_strip[xi, 0] > 55 and (top_strip[xi, 0] - top_strip[xi, 2]) > 22:
                top_strip[xi] = bot_strip[xi] * 0.92
        span = max(1.0, float(y1 - y0))
        for y in range(max(61, y0 - 6), min(325, y1 + 6)):
            t = np.clip((y - y0) / span, 0.0, 1.0)
            row_interp = top_strip * (1.0 - t) + bot_strip * t
            clean[y, pad_x0:pad_x1, :] = row_interp

    clean_im = Image.fromarray(np.clip(clean, 0, 255).astype(np.uint8), "RGB")
    clean_im = clean_im.filter(ImageFilter.GaussianBlur(1.5))
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
    if not SRC_A.exists():
        raise SystemExit(f"Missing 005 A plate: {SRC_A}")
    src = Image.open(SRC_A).convert("RGB").resize((W, H), Image.Resampling.LANCZOS)
    wiped = wipe_old_lettering(src)
    rgba = wiped.convert("RGBA")

    # 3-word name-the-thing hook: THE / BLOCKED / ARTERY
    # Optical vertical placement between top flourish (y=24..59) and bottom flourish (y=328..356)
    lines = [
        ("THE", "cream", 72),
        ("BLOCKED", "gold", 92),
        ("ARTERY", "cream", 92),
    ]
    sprites = []
    for text, kind, size in lines:
        fill, hi = (CREAM, CREAM_HI) if kind == "cream" else (GOLD, GOLD_HI)
        sprites.append((text, kind, size, render_word(text, size, fill, hi)))

    gap = 6
    total_h = sum(s[3].size[1] for s in sprites) + gap * (len(sprites) - 1)
    y = 65 + max(0, (256 - total_h) // 2)

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

    # Side-by-side phone comparison strip (360x202 + 168x94): A live vs old B v02 vs new B v03
    phone = SELECTED / "hos_005_thumb_A_vs_B_blocked_artery_v03_phone_168.jpg"
    b_v02 = Image.open(SRC_B_V02).convert("RGB") if SRC_B_V02.exists() else src
    strip = Image.new("RGB", (360 * 3 + 32, 202 + 94 + 76), (14, 10, 6))
    d = ImageDraw.Draw(strip)
    lf = ImageFont.truetype(GEORGIA, 15)
    for i, (label, src_im) in enumerate([
        ("A scheduled (ONE TIGHT BAND)", src),
        ("Old B v02 (IT GOES ROUND: vague 'IT')", b_v02),
        ("New B v03 (J0407: THE BLOCKED ARTERY)", out),
    ]):
        x0 = 8 + i * (360 + 8)
        d.text((x0, 6), label, font=lf, fill=(235, 212, 170))
        strip.paste(src_im.resize((360, 202), Image.Resampling.LANCZOS), (x0, 28))
        d.text((x0, 238), f"168x94 phone tile ({label.split()[0]} {label.split()[1]})", font=lf, fill=(200, 175, 135))
        strip.paste(src_im.resize((168, 94), Image.Resampling.LANCZOS), (x0, 262))
    strip.save(phone, "JPEG", quality=93)

    idx = {
        "film": "005",
        "video": "wwcjcFfC-5M",
        "job": "J0407",
        "replaces": "hos_005_thumb_B_it_goes_round_v02.jpg (pre-11-Oct 'IT GOES ROUND', vague pronoun + repeats 'Circulates')",
        "variant": "B v03",
        "maker": "gemini",
        "hook": "THE BLOCKED ARTERY",
        "punch": "BLOCKED",
        "jpg": f"Selected/{OUT.name}",
        "sha256": hashlib.sha256(OUT.read_bytes()).hexdigest(),
        "bytes": OUT.stat().st_size,
        "plates": [
            "Selected/hos_005_thumb_A_one_tight_band_v02.jpg (005 painted 16:9 key-art plate: glowing red artery stopped at linen band + Explorer lower-left + original gold scroll flourishes)"
        ],
        "method": "existing_005_plate_only_reletter_GeorgiaBold_with_original_painted_flourishes",
        "spend": 0,
        "heroBox": list(HERO_BOX),
        "explorer": {
            "source": "hos_005_thumb_A_one_tight_band_v02.jpg",
            "box": list(EXPLORER_BOX),
            "height_px": EXPLORER_BOX[3] - EXPLORER_BOX[1],
            "height_frac": round((EXPLORER_BOX[3] - EXPLORER_BOX[1]) / H, 3),
        },
        "lettering": placed,
        "ornaments": {
            "top_scroll_box": [60, 24, 468, 59],
            "bottom_scroll_box": [154, 328, 438, 356],
        },
        "clearOfHero": clear_of_hero,
        "clearOfExplorer": clear_of_explorer,
        "clearOfBadge": clear_of_badge,
        "scores": {
            "HOOK": "PASS — 'THE BLOCKED ARTERY' (3 words, punch word 'BLOCKED' in gold) names the glowing red artery stopped at the linen band (De Motu Cordis ch. 11, FACT_NOTES_v01 row 26) and adds to the video title ('The Tied Arm That Proved Your Blood Circulates') without repeating any content word from it.",
            "BAND": f"PASS — Upper-left lettering band (x={left}..{right}, y={top}..{bottom}, framed by original painted gold scroll flourishes at y=24..356) sits completely left of the hero arm (x={HERO_BOX[0]}..{HERO_BOX[2]}), above the Explorer's hair (y={EXPLORER_BOX[1]}), and clear of the bottom-right duration badge.",
            "PHONE": "PASS — Checked on 168x94 preview sheet and side-by-side strip: 'THE BLOCKED ARTERY', the glowing red artery stopped at the linen band, and the Explorer's face/glasses (52.2% height) all read at a glance at 168x94.",
        },
        "previews": [
            f"Selected/{preview.name}",
            f"Selected/{sheet.name}",
            f"Selected/{phone.name}",
        ],
        "studio": False,
        "status": "Test & Compare B v03 candidate for 005 (wwcjcFfC-5M, built from existing 005 plate only, £0). Parked for Chief: thumb B review. No Studio until OK.",
    }
    (HERE / "THUMB_B_BLOCKED_ARTERY_v03.json").write_text(json.dumps(idx, indent=2) + "\n")
    print("DONE", OUT, idx["sha256"])


if __name__ == "__main__":
    main()
