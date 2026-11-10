#!/usr/bin/env python3
"""HOS 001 long thumb B v03 (slot C upgrade): DROP OF WATER (OWB queue J0503).

Builds a post-11-Oct rule-compliant Test & Compare thumbnail variant for HOS 001
('How Did We Discover Germs?', _C92tIJCk8A) from existing 001 plates only
(£0 / 0 credits, no image model, no Studio changes):
- Why 001:
  - 001 (_C92tIJCk8A) is live with no Test & Compare in 05_Analytics/tests/THUMB_LEDGER.json.
  - 003 (frP_YrNShsU) has T001 actively running; 004 (GHZDsiH7L7A) is excluded by brief
    ('never 004's armed test'); 002 (AL_-qlWko_g) and 005 (wwcjcFfC-5M) already have three
    post-11-Oct non-title-repeating variants each (002: 'THE MISSING ELEMENT', 'PREDICTED
    BEFORE FOUND', 'EMPTY ON PURPOSE'; 005: 'ONE TIGHT BAND', 'THE BLOCKED ARTERY',
    'HIDDEN VEIN VALVES').
  - In 001, J0391 ('THE SWAN NECK', v01) and J0457 ('TRAPPED IN GLASS', v02) both feature
    Pasteur's swan-neck flask, while 001's third key-art beat in 08_Thumbnail/README.md
    (Variant C: 'Microscope + droplet', `hos_001_thumb_C_animistry_microscope_v01.jpg`) still
    repeated the full video title ('HOW DID WE DISCOVER GERMS?') with lettering overlapping
    the Explorer's hair and no gold scroll flourishes.
  - Building `hos_001_thumb_B_drop_of_water_v03.jpg` ('DROP / OF / WATER') from 001's existing
    Part 02 pond-water drop master still (`04_Generated-Clips/part02/refs/03_drop_of_water_v01.jpg`)
    and 001's painted key-art plate (`08_Thumbnail/Selected/hos_001_tc_thumb_v02.jpg`) gives 001:
    (1) three complete post-11-Oct non-title-repeating variants ('THE SWAN NECK', 'TRAPPED IN
        GLASS', and 'DROP OF WATER') with zero word overlap with the video title or each other, and
    (2) a distinct Part 02 pond-water droplet hero object alongside the two Part 04 flask variants.
- Base plates:
  - `04_Generated-Clips/part02/refs/03_drop_of_water_v01.jpg` on the NAS (1024x1024 Part 02 master
    plate: giant glowing drop of pond water teeming with faceless rods, spheres, and spirals on an
    illuminated glass microscope slide in the warm golden lab, placed on the right two-thirds at
    x=626..992, y=162..528 with the full slide at x=415..1223, y=475..655).
  - `08_Thumbnail/Selected/hos_001_tc_thumb_v02.jpg` on the NAS (001's painted library key-art
    plate: dark bookcase, teal curtain, lower-left on-model Explorer at x=88..316, y=328..720 =
    54.4% frame height looking up-right at the drop, and original painted top & bottom gold scroll
    flourishes at y=20..60 and y=318..356).
- Hook: 'DROP / OF / WATER' (3 words; gold punch word 'DROP' + cream 'OF / WATER') in house Georgia
  Bold serif display lettering, centered on the ornament column (cx=285), clear of the hero drop
  (x>=626 in the upper half), clear of the Explorer's hair (y>=328) and bottom flourish (y>=318),
  and clear of the bottom-right duration badge.
"""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont

HERE = Path(__file__).resolve().parent
SELECTED = HERE / "Selected"
REPO = HERE.parents[2]
TOOLS = REPO / "00_Brand" / "Channel-Setup" / "tools"
LIVE_A = REPO / "00_Brand" / "Channel-Setup" / "style" / "long" / "001_how_did_we_discover_germs.jpg"
NAS_TC_V02 = Path(
    "/Volumes/data/mac-mini-archive/YouTube/History Of Science/02_Video-Projects/"
    "001_How-Did-We-Discover-Germs/08_Thumbnail/Selected/hos_001_tc_thumb_v02.jpg"
)
NAS_DROP_V01 = Path(
    "/Volumes/data/mac-mini-archive/YouTube/History Of Science/02_Video-Projects/"
    "001_How-Did-We-Discover-Germs/04_Generated-Clips/part02/refs/03_drop_of_water_v01.jpg"
)
NAS_OLD_C = Path(
    "/Volumes/data/mac-mini-archive/YouTube/History Of Science/02_Video-Projects/"
    "001_How-Did-We-Discover-Germs/08_Thumbnail/Selected/hos_001_thumb_C_animistry_microscope_v01.jpg"
)
B_SWAN_V01 = SELECTED / "hos_001_thumb_B_swan_neck_v01.jpg"
B_TRAP_V02 = SELECTED / "hos_001_thumb_B_trapped_in_glass_v02.jpg"
OUT = SELECTED / "hos_001_thumb_B_drop_of_water_v03.jpg"

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

DROP_CROP_BOX = (44, 152, 1024, 936)
HERO_BOX = (626, 162, 998, 534)
SLIDE_BOX = (415, 475, 1223, 655)
EXPLORER_BOX = (88, 328, 316, 720)
CX = 285


def wipe_old_lettering(base: Image.Image) -> Image.Image:
    """Mask only the old letters ('WHAT PROVED / GERMS / WERE REAL?') and their stroke/shadow
    in y=62..314, x=58..518 of hos_001_tc_thumb_v02.jpg, restoring painted bookcase texture on
    the left (x<440) and continuous diagonal green curtain folds on the right (x>=440), while
    preserving 100% of the top flourish (y<=59), bottom flourish (y>=318), and Explorer (y>=328)."""
    arr = np.array(base.convert("RGB"), dtype=np.float32)

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

    clean = arr.copy()
    slope = -0.19
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
    clean_blur = clean_im.filter(ImageFilter.GaussianBlur(4.0))
    cb = np.array(clean_blur, dtype=np.float32)

    rng = np.random.default_rng(101)
    grain = rng.normal(0.0, 1.2, size=arr.shape).astype(np.float32)
    out = arr * (1.0 - dm[:, :, None]) + (cb + grain) * dm[:, :, None]
    return Image.fromarray(np.clip(out, 0, 255).astype(np.uint8), "RGB")


def compose_pond_drop_plate(tc_clean: Image.Image, drop_sq: Image.Image) -> Image.Image:
    """Composite 001's Part 02 glowing pond-water drop & glass slide on the right two-thirds
    with 001's library bookcase, teal curtain, lower-left Explorer, and painted gold scroll
    flourishes on the left."""
    crop_d = drop_sq.crop(DROP_CROP_BOX).resize((900, H), Image.Resampling.LANCZOS)
    right_full = tc_clean.copy()
    right_full.paste(crop_d, (380, 0))

    mask = Image.new("L", (W, H), 0)
    m = mask.load()
    for y in range(H):
        for x in range(W):
            if y < 160:
                t_top = min(1.0, max(0.0, (160 - y) / 140.0))
                x0 = 590 + 95 * t_top
                x1 = 670 + 85 * t_top
            elif y < 420:
                x0, x1 = 590, 670
            else:
                t_bot = min(1.0, max(0.0, (y - 420) / 85.0))
                x0 = 590 * (1.0 - t_bot) + 415 * t_bot
                x1 = 670 * (1.0 - t_bot) + 520 * t_bot
            w = min(1.0, max(0.0, (x - x0) / max(1.0, (x1 - x0))))
            m[x, y] = int(255 * w)
    mask = mask.filter(ImageFilter.GaussianBlur(20))
    comp = Image.composite(right_full, tc_clean, mask)

    # Local clarity & contrast pop on the glowing pond-water sphere (no saturation push)
    popped = ImageEnhance.Contrast(comp).enhance(1.14)
    popped = ImageEnhance.Sharpness(popped).enhance(1.25)
    pop_mask = Image.new("L", (W, H), 0)
    pd = ImageDraw.Draw(pop_mask)
    pd.ellipse((610, 145, 1005, 555), fill=235)
    pop_mask = pop_mask.filter(ImageFilter.GaussianBlur(24))
    return Image.composite(popped, comp, pop_mask)


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
    if not NAS_TC_V02.exists() or not NAS_DROP_V01.exists():
        raise SystemExit(f"Missing NAS source plates: {NAS_TC_V02} / {NAS_DROP_V01}")

    tc_raw = Image.open(NAS_TC_V02).convert("RGB").resize((W, H), Image.Resampling.LANCZOS)
    drop_sq = Image.open(NAS_DROP_V01).convert("RGB")
    tc_clean = wipe_old_lettering(tc_raw)
    base_plate = compose_pond_drop_plate(tc_clean, drop_sq)
    rgba = base_plate.convert("RGBA")

    # 3-word name-the-thing hook per THUMBNAIL_AND_TITLE_RULES.md §1.1, §2.5 & §2.B:
    # DROP / OF / WATER (gold punch word 'DROP' + cream 'OF' and 'WATER')
    lines = [
        ("DROP", "gold", 110),
        ("OF", "cream", 68),
        ("WATER", "cream", 104),
    ]
    sprites = []
    for text, kind, size in lines:
        fill, hi = (CREAM, CREAM_HI) if kind == "cream" else (GOLD, GOLD_HI)
        sprites.append((text, kind, size, render_word(text, size, fill, hi)))

    gap = -10
    total_h = sum(s[3].size[1] for s in sprites) + gap * (len(sprites) - 1)
    # Fit strictly inside y=63..315 between top flourish (y<=59) and bottom flourish (y>=318)
    y = 65 + max(0, (248 - total_h) // 2)

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
    clear_of_explorer = bottom < EXPLORER_BOX[1]
    clear_of_badge = bottom < H - 120 and HERO_BOX[2] < W - 140
    print(
        f"lettering box=[{left}, {top}, {right}, {bottom}] "
        f"explorer_top={EXPLORER_BOX[1]} hero_left={HERO_BOX[0]} "
        f"clear_of_hero={clear_of_hero} clear_of_explorer={clear_of_explorer} clear_of_badge={clear_of_badge}"
    )

    preview = SELECTED / f"{OUT.stem}_preview.jpg"
    subprocess.check_call([sys.executable, str(TOOLS / "thumb_preview.py"), "long", str(OUT), "--out", str(preview)])
    sheet = SELECTED / f"{OUT.stem}_style_sheet.jpg"
    subprocess.check_call([sys.executable, str(TOOLS / "style_sheet.py"), "long", str(OUT), "--out", str(sheet)])

    # 4-panel comparison strip (320x180 + 168x94):
    # C v01 old (repeats title + overlaps hair) vs B v01 (J0391) vs B v02 (J0457) vs New B v03 (J0503: DROP OF WATER)
    phone = SELECTED / "hos_001_thumb_TC_3way_drop_of_water_v03_phone_168.jpg"
    old_c = Image.open(NAS_OLD_C).convert("RGB") if NAS_OLD_C.exists() else Image.open(LIVE_A).convert("RGB")
    b1_im = Image.open(B_SWAN_V01).convert("RGB") if B_SWAN_V01.exists() else old_c
    b2_im = Image.open(B_TRAP_V02).convert("RGB") if B_TRAP_V02.exists() else old_c
    panels = [
        ("C v01 (2 Sep: repeats title + on hair)", "C v01 old", old_c),
        ("B v01 (J0391: THE SWAN NECK)", "B v01", b1_im),
        ("B v02 (J0457: TRAPPED IN GLASS)", "B v02", b2_im),
        ("New B v03 (J0503: DROP OF WATER)", "New B v03", out),
    ]
    pw, ph = 320, 180
    strip = Image.new("RGB", (pw * len(panels) + 12 * (len(panels) + 1), ph + 94 + 76), (14, 10, 6))
    d = ImageDraw.Draw(strip)
    lf = ImageFont.truetype(GEORGIA, 13)
    for i, (label, short_lbl, src_im) in enumerate(panels):
        x0 = 12 + i * (pw + 12)
        d.text((x0, 6), label, font=lf, fill=(235, 212, 170))
        strip.paste(src_im.resize((pw, ph), Image.Resampling.LANCZOS), (x0, 28))
        d.text((x0, 216), f"168x94 phone tile ({short_lbl})", font=lf, fill=(200, 175, 135))
        strip.paste(src_im.resize((168, 94), Image.Resampling.LANCZOS), (x0, 240))
    strip.save(phone, "JPEG", quality=93)

    idx = {
        "film": "001",
        "video": "_C92tIJCk8A",
        "job": "J0503",
        "replaces": "hos_001_thumb_C_animistry_microscope_v01.jpg (2 Sep droplet variant repeating full title 'HOW DID WE DISCOVER GERMS?' over Explorer's hair, no flourishes)",
        "variant": "B v03 (and T&C slot C upgrade; pairs with J0391 'THE SWAN NECK' and J0457 'TRAPPED IN GLASS' for a full 3-way non-title-repeating Test & Compare)",
        "maker": "gemini",
        "hook": "DROP OF WATER",
        "punch": "DROP",
        "jpg": f"Selected/{OUT.name}",
        "sha256": hashlib.sha256(OUT.read_bytes()).hexdigest(),
        "bytes": OUT.stat().st_size,
        "plates": [
            f"04_Generated-Clips/part02/refs/{NAS_DROP_V01.name} (1024x1024 Part 02 pond-water drop master plate, crop {list(DROP_CROP_BOX)} placed on right two-thirds)",
            f"08_Thumbnail/Selected/{NAS_TC_V02.name} (001 painted library key-art plate: lower-left Explorer at 54.4% frame height + original painted gold scroll flourishes)",
        ],
        "method": "existing_001_plates_only_pond_drop_hero_plus_explorer_and_painted_flourishes_GeorgiaBold",
        "spend": 0,
        "heroBox": list(HERO_BOX),
        "slideBox": list(SLIDE_BOX),
        "explorer": {
            "source": NAS_TC_V02.name,
            "box": list(EXPLORER_BOX),
            "height_px": EXPLORER_BOX[3] - EXPLORER_BOX[1],
            "height_frac": round((EXPLORER_BOX[3] - EXPLORER_BOX[1]) / H, 3),
        },
        "lettering": placed,
        "ornaments": {
            "top_scroll_box": [88, 20, 496, 60],
            "bottom_scroll_box": [140, 318, 445, 356],
        },
        "clearOfHero": clear_of_hero,
        "clearOfExplorer": clear_of_explorer,
        "clearOfBadge": clear_of_badge,
        "scores": {
            "HOOK": "PASS — 'DROP OF WATER' (3 words, punch word 'DROP' in gold) names Leeuwenhoek's pond-water droplet teeming with faceless microbes (001 script Part 02 'A drop of pond water is not empty' and THUMBNAIL_AND_TITLE_RULES.md §1.1 familiar noun 'a drop of water'), shares zero words with the video title ('How Did We Discover Germs?'), J0391 ('THE SWAN NECK'), or J0457 ('TRAPPED IN GLASS'), and uses no vague questions or pronouns.",
            "BAND": f"PASS — Upper-left lettering band (x={left}..{right}, y={top}..{bottom}, framed by 001's original painted gold scroll flourishes at y=20..356) sits completely left of the glowing pond-water drop (x={HERO_BOX[0]}..{HERO_BOX[2]}), above the Explorer's hair (y={EXPLORER_BOX[1]}) and bottom flourish (y=318), and clear of the bottom-right duration badge.",
            "PHONE": "PASS — Checked on 168x94 preview sheet and 4-panel comparison strip: 'DROP OF WATER', the giant glowing pond-water droplet with faceless microbes on the microscope slide, and the Explorer's face/glasses (54.4% height) all read at a glance at 168x94.",
        },
        "previews": [
            f"Selected/{preview.name}",
            f"Selected/{sheet.name}",
            f"Selected/{phone.name}",
        ],
        "studio": False,
        "status": "Test & Compare B v03 (slot C upgrade) candidate for 001 (_C92tIJCk8A, built from existing 001 plates only, £0). Parked for Chief: thumb B review. No Studio until OK.",
    }
    (HERE / "THUMB_B_DROP_OF_WATER_v03.json").write_text(json.dumps(idx, indent=2) + "\n")
    print("DONE", OUT, idx["sha256"])


if __name__ == "__main__":
    main()
