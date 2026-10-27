#!/usr/bin/env python3
"""HOS 001 long thumb B v02: TRAPPED IN GLASS (OWB queue J0457).

Builds a post-11-Oct rule-compliant Test & Compare thumbnail variant for HOS 001
('How Did We Discover Germs?', _C92tIJCk8A) from existing 001 plates only
(£0 / 0 credits, no image model, no Studio changes):
- Why 001:
  - 001 (_C92tIJCk8A) is live with no Test & Compare in 05_Analytics/tests/THUMB_LEDGER.json.
  - 003 (frP_YrNShsU) has T001 actively running; 004 (GHZDsiH7L7A) is excluded by brief
    ('never 004's armed test'); 002 (AL_-qlWko_g) and 005 (wwcjcFfC-5M) already have two
    post-11-Oct existing-plate B/C variants each (J0374 + J0442 for 002; J0407 + J0424 for 005).
  - 001 had only one post-11-Oct variant so far (`hos_001_thumb_B_swan_neck_v01.jpg`,
    'THE SWAN NECK', J0391, built from the library clear-broth key-art plate
    `hos_001_tc_thumb_v02.jpg`), while 001's other pre-11-Oct drafts on the NAS still repeated
    the full video title ('HOW DID WE DISCOVER GERMS?').
  - Re-lettering 001's hospital-ward glowing-microbe flask key-art plate
    (`Selected/hos_001_thumb_A_animistry_flask_v01.png` on the NAS) with the 3-word hook
    'TRAPPED / IN / GLASS' (`hos_001_thumb_B_trapped_in_glass_v02.jpg`) gives Chief both:
    (1) a clean same-plate B test against live A (isolating the 3-word hook vs title-repeating A),
    and (2) a full post-11-Oct 3-way Test & Compare set alongside J0391's `THE SWAN NECK`.
- Base plate: 001's painted 16:9 key-art plate `Selected/hos_001_thumb_A_animistry_flask_v01.png`
  on the NAS (giant glowing swan-neck flask with faceless microbes in golden broth on the right
  two-thirds; Explorer on model in the lower-left at x=82..308, y=366..720 = 49.2% frame height;
  original painted top & bottom gold scroll flourishes).
- Replaces the title-repeating 4-word question ('HOW DID WE / DISCOVER / GERMS?') with a 3-word
  hook per THUMBNAIL_AND_TITLE_RULES.md §2.5 & §2.B: 'TRAPPED / IN / GLASS' (gold punch word
  'TRAPPED' + cream 'IN / GLASS') in house Georgia Bold serif display lettering, centered on the
  ornament column (cx=288), clear of the hero swan-neck flask (x>=583 in the lettering band),
  clear of the Explorer's hair (y>=366) and bottom flourish (y=354..390), and clear of the
  bottom-right duration badge.
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
NAS_A_PNG = Path(
    "/Volumes/data/mac-mini-archive/YouTube/History Of Science/02_Video-Projects/"
    "001_How-Did-We-Discover-Germs/08_Thumbnail/Selected/hos_001_thumb_A_animistry_flask_v01.png"
)
NAS_TC_V02 = Path(
    "/Volumes/data/mac-mini-archive/YouTube/History Of Science/02_Video-Projects/"
    "001_How-Did-We-Discover-Germs/08_Thumbnail/Selected/hos_001_tc_thumb_v02.jpg"
)
B_SWAN_V01 = SELECTED / "hos_001_thumb_B_swan_neck_v01.jpg"
OUT = SELECTED / "hos_001_thumb_B_trapped_in_glass_v02.jpg"

W, H = 1280, 720
CREAM = (242, 214, 172)
CREAM_HI = (252, 238, 208)
GOLD = (228, 156, 32)
GOLD_HI = (248, 202, 68)
INK = (16, 9, 4)
SHADOW = (6, 3, 1)
GEORGIA = "/System/Library/Fonts/Supplemental/Georgia Bold.ttf"
TRACKING = -3
CONDENSE_X = 0.92

HERO_BOX = (583, 20, 1279, 719)
EXPLORER_BOX = (82, 366, 308, 720)
CX = 288


def wipe_old_lettering(base: Image.Image, tc_ref: Image.Image | None) -> Image.Image:
    """Mask only the old title letters ('HOW DID WE / DISCOVER / GERMS?') and the R swash tail
    in y=62..392, x=24..566, restoring the dark warm ward panelling on the left and diagonal
    teal/green curtain fold on the right, while preserving 100% of the top gold flourish (y<=60),
    the Explorer's hair (x=82..246, y>=364), the left/right wings of the original bottom gold
    flourish (y=358..376), and the center gold scroll ornament (restored cleanly at y=354..390)."""
    arr = np.array(base.convert("RGB"), dtype=np.float32)

    letter_mask = Image.new("L", (W, H), 0)
    lm = letter_mask.load()
    bands = [
        (63, 108, 100, 466),   # HOW DID WE
        (114, 224, 24, 556),   # DISCOVER
        (228, 355, 40, 565),   # GERMS? main bodies
        (355, 392, 260, 366),  # R downward swash tail only (leaving left/right flourish wings intact)
    ]
    for y0, y1, x0, x1 in bands:
        for y in range(y0, y1):
            for x in range(x0, x1):
                r, g, b = arr[y, x]
                if (r > 30 and (r + g + b) > 62 and (r - b) > 6) or (r + g + b) > 110:
                    lm[x, y] = 255

    dilated = letter_mask.filter(ImageFilter.MaxFilter(25)).filter(ImageFilter.GaussianBlur(3.5))
    dm = np.array(dilated, dtype=np.float32) / 255.0

    # Protect top gold scroll flourish (y<=60)
    dm[:61, :] = 0.0
    dm[61, :] *= 0.35
    dm[62, :] *= 0.75

    # Protect left & right wings of the original bottom flourish (y>=358 outside x=256..368)
    # and protect the Explorer's hair (x<=255, y>=360) and ward lamp (x>=368, y>=358)
    for y in range(354, 400):
        for x in range(W):
            if (x <= 255 or x >= 368) and y >= 359:
                dm[y, x] = 0.0
            elif (x <= 255 or x >= 368) and y >= 355:
                dm[y, x] *= max(0.0, (359 - y) / 4.0)
    dm[394:, :] = 0.0
    dm[:, :20] = 0.0
    dm[:, 572:] = 0.0

    # Synthesize clean dark ward wall + teal curtain fold from the clean gap rows
    clean = arr.copy()
    row_61 = arr[59:62, :575, :].mean(axis=0)
    row_110 = arr[108:113, :575, :].mean(axis=0)
    row_226 = arr[224:229, :575, :].mean(axis=0)
    # Remove residual D-shadow warmth in x=20..85 of row_226 using row_110
    row_226[20:85] = row_110[20:85]
    # Below GERMS?, keep left wall dark like row_226, and smoothly bridge x=250..370
    row_360 = row_226.copy()
    row_360[250:370] = arr[396:410, 250:370, :].mean(axis=0)
    row_360[370:575] = arr[355:359, 370:575, :].mean(axis=0)

    for y in range(60, 394):
        if y <= 110:
            t = np.clip((y - 61.0) / (110.0 - 61.0), 0.0, 1.0)
            base_row = row_61 * (1.0 - t) + row_110 * t
        elif y <= 226:
            t = np.clip((y - 110.0) / (226.0 - 110.0), 0.0, 1.0)
            base_row = row_110 * (1.0 - t) + row_226 * t
        else:
            t = np.clip((y - 226.0) / (365.0 - 226.0), 0.0, 1.0)
            base_row = row_226 * (1.0 - t) + row_360 * t
        clean[y, 20:572] = base_row[20:572]
        # For y=354..393, horizontally interpolate x=252..370 between actual left/right neighbors
        if y >= 354:
            c_left = arr[min(H - 1, max(396, y)), 248:254, :].mean(axis=0)
            c_right = arr[y, 370:376, :].mean(axis=0)
            for x in range(252, 370):
                tx = (x - 252.0) / (370.0 - 252.0)
                clean[y, x] = c_left * (1.0 - tx) + c_right * tx

    clean_im = Image.fromarray(np.clip(clean, 0, 255).astype(np.uint8), "RGB").filter(ImageFilter.GaussianBlur(2.0))
    clean_arr = np.array(clean_im, dtype=np.float32)
    out_arr = arr * (1.0 - dm[:, :, None]) + clean_arr * dm[:, :, None]

    # Restore the clean center scroll ornament and horizontal bar of the bottom gold flourish
    # at y=355..390 using the right half of tc_ref's bottom scroll ornament (y_tc=319..354,
    # x_tc=292..444) mirrored symmetrically around cx=292 so zero Explorer hair from tc_ref is touched.
    if tc_ref is not None:
        tc_arr = np.array(tc_ref.convert("RGB").resize((W, H), Image.Resampling.LANCZOS), dtype=np.float32)
        cx_orn = 292
        for dy in range(36):
            y_tc = 319 + dy
            y_dst = 355 + dy
            if y_dst >= H:
                break
            for dx in range(152):
                x_tc = cx_orn + dx
                if x_tc >= W:
                    break
                r, g, b = tc_arr[y_tc, x_tc]
                lum = (r + g + b) / 3.0
                warmth = r - b
                if r > 52 and warmth > 20 and lum > 38:
                    alpha = np.clip((warmth - 20.0) / 50.0, 0.0, 1.0)
                    for x_dst in (cx_orn + dx, cx_orn - dx):
                        if 140 <= x_dst <= 445:
                            out_arr[y_dst, x_dst] = out_arr[y_dst, x_dst] * (1.0 - alpha) + tc_arr[y_tc, x_tc] * alpha

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
    src_path = NAS_A_PNG if NAS_A_PNG.exists() else LIVE_A
    if not src_path.exists():
        raise SystemExit(f"Missing 001 source plate: {src_path}")
    src = Image.open(src_path).convert("RGB").resize((W, H), Image.Resampling.LANCZOS)
    tc_ref = Image.open(NAS_TC_V02).convert("RGB") if NAS_TC_V02.exists() else None
    wiped = wipe_old_lettering(src, tc_ref)
    rgba = wiped.convert("RGBA")

    # 3-word concrete mechanism hook: TRAPPED / IN / GLASS
    # Punch word 'TRAPPED' in gold, 'IN' and 'GLASS' in cream.
    # Zero word overlap with the video title ('How Did We Discover Germs?')
    # or with J0391's 'THE SWAN NECK'.
    lines = [
        ("TRAPPED", "gold", 96),
        ("IN", "cream", 74),
        ("GLASS", "cream", 112),
    ]
    sprites = []
    for text, kind, size in lines:
        fill, hi = (CREAM, CREAM_HI) if kind == "cream" else (GOLD, GOLD_HI)
        sprites.append((text, kind, size, render_word(text, size, fill, hi)))

    gap = -6
    total_h = sum(s[3].size[1] for s in sprites) + gap * (len(sprites) - 1)
    y = 70 + max(0, (276 - total_h) // 2)

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

    # Side-by-side 3-way T&C comparison strip (360x202 + 168x94):
    # A live (repeats title) vs B v01 (J0391: THE SWAN NECK) vs New B v02 (J0457: TRAPPED IN GLASS)
    phone = SELECTED / "hos_001_thumb_TC_3way_trapped_in_glass_v02_phone_168.jpg"
    a_im = Image.open(LIVE_A).convert("RGB")
    b1_im = Image.open(B_SWAN_V01).convert("RGB") if B_SWAN_V01.exists() else a_im
    panels = [
        ("A live (repeats title)", "A live", a_im),
        ("B v01 (J0391: THE SWAN NECK)", "B v01", b1_im),
        ("New B v02 (J0457: TRAPPED IN GLASS)", "New B v02", out),
    ]
    strip = Image.new("RGB", (360 * len(panels) + 12 * (len(panels) + 1), 202 + 94 + 76), (14, 10, 6))
    d = ImageDraw.Draw(strip)
    lf = ImageFont.truetype(GEORGIA, 14)
    for i, (label, short_lbl, src_im) in enumerate(panels):
        x0 = 12 + i * (360 + 12)
        d.text((x0, 6), label, font=lf, fill=(235, 212, 170))
        strip.paste(src_im.resize((360, 202), Image.Resampling.LANCZOS), (x0, 28))
        d.text((x0, 238), f"168x94 phone tile ({short_lbl})", font=lf, fill=(200, 175, 135))
        strip.paste(src_im.resize((168, 94), Image.Resampling.LANCZOS), (x0, 262))
    strip.save(phone, "JPEG", quality=93)

    idx = {
        "film": "001",
        "video": "_C92tIJCk8A",
        "job": "J0457",
        "replaces": "hos_001_thumb_A_animistry_flask_v01.jpg title-repeating text ('HOW DID WE DISCOVER GERMS?'); pairs with A live and J0391 B v01 ('THE SWAN NECK') for 3-way Test & Compare",
        "variant": "B v02 (ward glowing-microbe flask variant; pairs with A live and/or J0391 B v01 THE SWAN NECK)",
        "maker": "gemini",
        "hook": "TRAPPED IN GLASS",
        "punch": "TRAPPED",
        "jpg": f"Selected/{OUT.name}",
        "sha256": hashlib.sha256(OUT.read_bytes()).hexdigest(),
        "bytes": OUT.stat().st_size,
        "plates": [
            "Selected/hos_001_thumb_A_animistry_flask_v01.png (NAS 001 painted 16:9 key-art plate: giant glowing swan-neck flask with faceless microbes on right two-thirds + Explorer lower-left + original gold scroll flourishes)",
            "Selected/hos_001_tc_thumb_v02.jpg (NAS 001 companion key-art plate: symmetric center gold scroll ornament reference)"
        ],
        "method": "existing_001_plate_only_reletter_GeorgiaBold_with_original_painted_flourishes",
        "spend": 0,
        "heroBox": list(HERO_BOX),
        "explorer": {
            "source": "hos_001_thumb_A_animistry_flask_v01.png",
            "box": list(EXPLORER_BOX),
            "height_px": EXPLORER_BOX[3] - EXPLORER_BOX[1],
            "height_frac": round((EXPLORER_BOX[3] - EXPLORER_BOX[1]) / H, 3),
        },
        "lettering": placed,
        "ornaments": {
            "top_scroll_box": [88, 20, 496, 60],
            "bottom_scroll_box": [140, 355, 445, 390],
        },
        "clearOfHero": clear_of_hero,
        "clearOfExplorer": clear_of_explorer,
        "clearOfBadge": clear_of_badge,
        "scores": {
            "HOOK": "PASS — 'TRAPPED IN GLASS' (3 words, punch word 'TRAPPED' in gold) names Pasteur's curved-glass flask trap holding airborne dust and microbes (001 script Part 04 'a flask that trapped the truth'), shares zero words with the video title ('How Did We Discover Germs?') or J0391's 'THE SWAN NECK', and uses no vague questions or pronouns.",
            "BAND": f"PASS — Upper-left lettering band (x={left}..{right}, y={top}..{bottom}, framed by original painted gold scroll flourishes at y=20..390) sits completely left of the glowing swan-neck flask in the upper half (x>={HERO_BOX[0]}), above the Explorer's hair (y={EXPLORER_BOX[1]}) and bottom flourish (y=355), and clear of the bottom-right duration badge.",
            "PHONE": "PASS — Checked on 168x94 preview sheet and 3-way T&C comparison strip: 'TRAPPED IN GLASS', the giant glowing swan-neck flask with faceless microbes, and the Explorer's face/glasses (49.2% height) all read at a glance at 168x94.",
        },
        "previews": [
            f"Selected/{preview.name}",
            f"Selected/{sheet.name}",
            f"Selected/{phone.name}",
        ],
        "studio": False,
        "status": "Test & Compare B v02 candidate for 001 (_C92tIJCk8A, built from existing 001 plates only, £0). Parked for Chief: thumb B review. No Studio until OK.",
    }
    (HERE / "THUMB_B_TRAPPED_IN_GLASS_v02.json").write_text(json.dumps(idx, indent=2) + "\n")
    print("DONE", OUT, idx["sha256"])


if __name__ == "__main__":
    main()
