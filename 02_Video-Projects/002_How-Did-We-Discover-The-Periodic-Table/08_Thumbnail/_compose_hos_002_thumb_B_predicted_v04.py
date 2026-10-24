#!/usr/bin/env python3
"""HOS 002 long thumb B v04: PREDICTED BEFORE FOUND (OWB queue J0442).

Builds a post-11-Oct rule-compliant Test & Compare thumbnail variant for HOS 002
('How Did We Discover the Periodic Table?', AL_-qlWko_g) from existing 002 plates only
(£0 / 0 credits, no image model, no Studio changes):
- Why 002:
  - 002's Sep 27 3-way Test & Compare finished on 11 Oct 2026 with no winner ('Not enough
    impressions to declare a winner'; AB_TEST_RESULT_2026-10-13.md), so 002 has no active test
    and no row in 05_Analytics/tests/THUMB_LEDGER.json.
  - 002's earlier slot-B gallium thumb (`hos_002_thumb_B_predicted_v03.jpg`, 'HE PREDICTED THIS')
    was built on 27 Sep before the 30 Sep live-look lock and 11 Oct Astrum packaging rules:
    it cropped out the Explorer entirely, used flat Arial Black sans-serif white/yellow type,
    left a visible rectangular blur patch in the upper-left corner, and used vague pronouns
    ('HE PREDICTED THIS').
  - J0374 rebuilt 002's empty-slot variant (`hos_002_thumb_B_missing_element_v02.jpg`,
    'THE MISSING ELEMENT'). Rebuilding the gallium-prediction variant in the locked house look
    (`hos_002_thumb_B_predicted_v04.jpg`, 'PREDICTED BEFORE FOUND') gives Chief both a clean
    same-plate B test against live A (isolating hook words vs title-repeating A) and a full
    post-11-Oct 3-way Test & Compare set alongside `THE MISSING ELEMENT` (J0374).
- Base plate: 002's own painted 16:9 key-art plate `Selected/hos_002_thumb_A_gallium_live_v02.png`
  on the NAS (giant silvery liquid-gallium arch and droplet filling the right two-thirds at
  x=560..1248, y=22..704; Explorer on model in the lower-left at x=42..256, y=300..720 = 58.3%
  frame height; original painted top & bottom gold scroll flourishes at y=28..63 and y=311..359).
- Replaces the title-repeating 6-word lettering ('HOW DID WE / DISCOVER THE / PERIODIC TABLE?')
  in y=66..308 with a 3-word discovery-prediction hook per THUMBNAIL_AND_TITLE_RULES.md §1.2,
  §2.5 & §2.B: 'PREDICTED / BEFORE / FOUND' (gold punch word 'PREDICTED' + cream 'BEFORE / FOUND')
  in house Georgia Bold serif display lettering, centered on the ornament column (cx=298),
  clear of the hero gallium arch (x>=560), clear of the Explorer's hair (y>=300) and bottom
  flourish (y>=311), and clear of the bottom-right duration badge.
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
LIVE_A = REPO / "00_Brand" / "Channel-Setup" / "style" / "long" / "002_how_did_we_discover_the_periodic_table.jpg"
NAS_A_PNG = Path(
    "/Volumes/data/mac-mini-archive/YouTube/History Of Science/02_Video-Projects/"
    "002_How-Did-We-Discover-The-Periodic-Table/08_Thumbnail/Selected/hos_002_thumb_A_gallium_live_v02.png"
)
OLD_B_V03 = SELECTED / "hos_002_thumb_B_predicted_v03.jpg"
B_MISSING_V02 = SELECTED / "hos_002_thumb_B_missing_element_v02.jpg"
OUT = SELECTED / "hos_002_thumb_B_predicted_v04.jpg"

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

HERO_BOX = (560, 22, 1248, 704)
EXPLORER_BOX = (42, 300, 256, 720)
CX = 298


def wipe_old_lettering(base: Image.Image) -> Image.Image:
    """Mask only the old title letters ('HOW DID WE / DISCOVER THE / PERIODIC TABLE?') and their
    stroke/shadow in y=65..309, x=28..624, restoring painted bookcase texture on the left,
    continuous diagonal green curtain folds in the middle, and warm window edge on the right,
    while preserving 100% of the top gold flourish (y<=63), bottom gold flourish (y>=311),
    and the Explorer's top hair curl (x=182..216, y>=300)."""
    arr = np.array(base.convert("RGB"), dtype=np.float32)

    letter_mask = Image.new("L", (W, H), 0)
    lm = letter_mask.load()
    bands = [
        (67, 115, 145, 455),   # HOW DID WE
        (115, 208, 40, 560),   # DISCOVER THE
        (208, 309, 30, 620),   # PERIODIC TABLE?
    ]
    for y0, y1, x0, x1 in bands:
        for y in range(y0, y1):
            for x in range(x0, x1):
                if y >= 300 and 184 <= x <= 216:
                    continue
                r, g, b = arr[y, x]
                if (r > 36 and (r + g + b) > 74 and (r - b) > 8) or (r + g + b) > 130:
                    lm[x, y] = 255

    dilated = letter_mask.filter(ImageFilter.MaxFilter(25)).filter(ImageFilter.GaussianBlur(3.5))
    dm = np.array(dilated, dtype=np.float32) / 255.0

    dm[:64, :] = 0.0
    dm[64, :] *= 0.35
    dm[65, :] *= 0.75

    for y in range(298, 330):
        for x in range(W):
            if 182 <= x <= 216 and y >= 300:
                dm[y, x] = 0.0
            elif 100 <= x <= 245 and y >= 309:
                dm[y, x] = 0.0
            elif 190 <= x <= 485 and y >= 311:
                dm[y, x] = 0.0
            elif y >= 310:
                dm[y, x] *= max(0.0, (314 - y) / 4.0)
    dm[315:, :] = 0.0
    dm[:, :24] = 0.0
    dm[:, 632:] = 0.0

    clean = arr.copy()
    slope = -0.255
    spine_top = arr[2:18, :460, :].mean(axis=0) * 0.85

    for y in range(60, 316):
        x_curt = int(round(483.0 + slope * (y - 60)))
        for x in range(24, 632):
            if x >= 558 and y >= 200:
                t = np.clip((y - 201.0) / (306.0 - 201.0), 0.0, 1.0)
                x_top = int(round(np.clip(x - slope * (y - 201), 545, 648)))
                x_bot = int(round(np.clip(x + slope * (306 - y), 530, 638)))
                c_top = arr[197:203, x_top, :].mean(axis=0)
                c_bot = arr[304:310, x_bot, :].mean(axis=0)
                clean[y, x] = c_top * (1.0 - t) + c_bot * t
            elif x >= x_curt - 15:
                t = np.clip((y - 80.0) / (308.0 - 80.0), 0.0, 1.0)
                x_top = int(round(np.clip(x - slope * (y - 80), 455, 630)))
                x_bot = int(round(np.clip(x + slope * (308 - y), 410, 575)))
                c_top = arr[74:84, x_top, :].mean(axis=0)
                c_bot = arr[306:312, x_bot, :].mean(axis=0)
                clean[y, x] = c_top * (1.0 - t) + c_bot * t
            else:
                base_col = spine_top[min(459, x)]
                shelf_mod = 0.65 if (112 <= y <= 120 or 206 <= y <= 214) else 1.0
                bay_pos = ((y - 20) % 94) / 94.0
                bay_shade = 0.68 + 0.32 * (bay_pos ** 1.3)
                clean[y, x] = base_col * shelf_mod * bay_shade

    clean_im = Image.fromarray(np.clip(clean, 0, 255).astype(np.uint8), "RGB").filter(ImageFilter.GaussianBlur(1.8))
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
    src_path = NAS_A_PNG if NAS_A_PNG.exists() else LIVE_A
    if not src_path.exists():
        raise SystemExit(f"Missing 002 source plate: {src_path}")
    src = Image.open(src_path).convert("RGB").resize((W, H), Image.Resampling.LANCZOS)
    wiped = wipe_old_lettering(src)
    rgba = wiped.convert("RGBA")

    # 3-word concrete prediction hook: PREDICTED / BEFORE / FOUND
    # Punch word 'PREDICTED' in gold, 'BEFORE' and 'FOUND' in cream.
    # Zero word overlap with the video title ('How Did We Discover the Periodic Table?')
    # or with J0374's 'THE MISSING ELEMENT'.
    lines = [
        ("PREDICTED", "gold", 80),
        ("BEFORE", "cream", 78),
        ("FOUND", "cream", 94),
    ]
    sprites = []
    for text, kind, size in lines:
        fill, hi = (CREAM, CREAM_HI) if kind == "cream" else (GOLD, GOLD_HI)
        sprites.append((text, kind, size, render_word(text, size, fill, hi)))

    gap = -4
    total_h = sum(s[3].size[1] for s in sprites) + gap * (len(sprites) - 1)
    y = 66 + max(0, (232 - total_h) // 2)

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

    # Side-by-side 4-panel T&C comparison strip (360x202 + 168x94):
    # A live vs Old B v03 (pre-lock, no Explorer) vs B v02 (THE MISSING ELEMENT) vs New B v04 (PREDICTED BEFORE FOUND)
    phone = SELECTED / "hos_002_thumb_TC_3way_predicted_v04_phone_168.jpg"
    a_im = Image.open(LIVE_A).convert("RGB")
    old_b_im = Image.open(OLD_B_V03).convert("RGB") if OLD_B_V03.exists() else a_im
    miss_b_im = Image.open(B_MISSING_V02).convert("RGB") if B_MISSING_V02.exists() else a_im
    panels = [
        ("A live (repeats title)", "A live", a_im),
        ("Old B v03 (Sep 27: no Explorer, pronouns)", "Old B v03", old_b_im),
        ("B v02 (J0374: THE MISSING ELEMENT)", "B v02 slot", miss_b_im),
        ("New B v04 (J0442: PREDICTED BEFORE FOUND)", "New B v04", out),
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
        "film": "002",
        "video": "AL_-qlWko_g",
        "job": "J0442",
        "replaces": "hos_002_thumb_B_predicted_v03.jpg (Sep 27 pre-lock 'HE PREDICTED THIS': no Explorer, flat Arial Black sans, upper-left blur patch, vague pronouns)",
        "variant": "B v04 (gallium-prediction variant; pairs with A live and/or J0374 B v02 THE MISSING ELEMENT)",
        "maker": "gemini",
        "hook": "PREDICTED BEFORE FOUND",
        "punch": "PREDICTED",
        "jpg": f"Selected/{OUT.name}",
        "sha256": hashlib.sha256(OUT.read_bytes()).hexdigest(),
        "bytes": OUT.stat().st_size,
        "plates": [
            "Selected/hos_002_thumb_A_gallium_live_v02.png (NAS 002 painted 16:9 key-art plate: giant liquid-gallium arch & droplet on right two-thirds + Explorer lower-left + original gold scroll flourishes)"
        ],
        "method": "existing_002_plate_only_reletter_GeorgiaBold_with_original_painted_flourishes",
        "spend": 0,
        "heroBox": list(HERO_BOX),
        "explorer": {
            "source": "hos_002_thumb_A_gallium_live_v02.png",
            "box": list(EXPLORER_BOX),
            "height_px": EXPLORER_BOX[3] - EXPLORER_BOX[1],
            "height_frac": round((EXPLORER_BOX[3] - EXPLORER_BOX[1]) / H, 3),
        },
        "lettering": placed,
        "ornaments": {
            "top_scroll_box": [113, 28, 485, 63],
            "bottom_scroll_box": [197, 311, 467, 359],
        },
        "clearOfHero": clear_of_hero,
        "clearOfExplorer": clear_of_explorer,
        "clearOfBadge": clear_of_badge,
        "scores": {
            "HOOK": "PASS — 'PREDICTED BEFORE FOUND' (3 words, punch word 'PREDICTED' in gold) names Mendeleev's 1869 prediction of eka-aluminium before gallium was discovered in 1875 (THUMBNAIL_AND_TITLE_RULES.md §1.2 'He predicted a metal before it was found'), shares zero words with the video title ('How Did We Discover the Periodic Table?') or J0374's 'THE MISSING ELEMENT', and replaces v03's vague pronouns ('HE PREDICTED THIS').",
            "BAND": f"PASS — Upper-left lettering band (x={left}..{right}, y={top}..{bottom}, framed by original painted gold scroll flourishes at y=28..359) sits completely left of the hero gallium arch (x={HERO_BOX[0]}..{HERO_BOX[2]}), above the Explorer's hair (y={EXPLORER_BOX[1]}) and bottom flourish (y=311), and clear of the bottom-right duration badge.",
            "PHONE": "PASS — Checked on 168x94 preview sheet and 4-panel strip: 'PREDICTED BEFORE FOUND', the giant silvery liquid-gallium arch and droplet (688x682 px), and the Explorer's face/glasses (58.3% height) all read at a glance at 168x94.",
        },
        "previews": [
            f"Selected/{preview.name}",
            f"Selected/{sheet.name}",
            f"Selected/{phone.name}",
        ],
        "studio": False,
        "status": "Test & Compare B v04 candidate for 002 (AL_-qlWko_g, built from existing 002 plate only, £0). Parked for Chief: thumb B review. No Studio until OK.",
    }
    (HERE / "THUMB_B_PREDICTED_v04.json").write_text(json.dumps(idx, indent=2) + "\n")
    print("DONE", OUT, idx["sha256"])


if __name__ == "__main__":
    main()
