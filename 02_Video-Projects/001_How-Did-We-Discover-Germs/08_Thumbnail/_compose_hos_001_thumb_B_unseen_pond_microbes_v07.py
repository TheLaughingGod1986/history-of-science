#!/usr/bin/env python3
"""HOS 001 long thumb B v07: UNSEEN POND MICROBES (OWB queue J0685).

Builds a post-11-Oct rule-compliant Test & Compare thumbnail variant for HOS 001
('How Did We Discover Germs?', _C92tIJCk8A) from existing 001 plates only
(£0 / 0 credits, no image model, no Studio changes):
- Why 001:
  - 001 (_C92tIJCk8A) is live with no active Test & Compare in 05_Analytics/tests/THUMB_LEDGER.json.
  - 003 (frP_YrNShsU) has T001 actively running; 004 (GHZDsiH7L7A) is excluded by brief
    ('never 004's armed test'); in the 001 -> 005 -> 002 rotation, 001 got B v06 in J0640,
    005 got B v08 in J0655, and 002 got B v10 in J0670, making 001 next in rotation.
- What B v07 adds:
  - Alternates back from B v06's swan-neck flask plate ('STERILE LIQUID FLASK') to 001's Part 02
    glowing pond-water droplet & microscope slide plate (`03_drop_of_water_v01.jpg` composited with
    `hos_001_tc_thumb_v02.jpg`), stepping up to a 1.175x combined hero push-in (920x736 right-plate
    crop + 1.10x local sphere push-in anchored on the microscope slide contact point) plus targeted
    internal microbe (faceless rods, spiked spheres, golden spirals) and glass-slide rim clarity
    boost (`heroBox = [588, 96, 1026, 534]`, 438x438 px, +39% larger area than v03's 372x372 px;
    `slideBox = [420, 468, 1223, 650]`, clear of the bottom-right duration badge), preserving the
    lower-left Explorer at 54.4% frame height (`box = [88, 328, 316, 720]`) and keeping the
    original painted top & bottom gold scroll flourishes untouched.
  - 3-word concrete visual hook 'UNSEEN / POND / MICROBES' (cream 'UNSEEN', cream 'POND', gold
    punch word 'MICROBES'), directly naming the visible microorganisms inside Leeuwenhoek's
    pond-water bead on the glass slide (001 script Part 01 & Part 02: 'microbes drifting unseen...
    A drop of pond water is not empty. It is a bustling kingdom — darting shapes, spinning cells...
    People could watch microbes dance' and THUMBNAIL_AND_TITLE_RULES.md §1.2 & §2.B.1 'name the
    thing'), with zero word overlap with the video title ('How Did We Discover Germs?'), Live A
    ('WHAT PROVED GERMS WERE REAL?'), J0391 ('THE SWAN NECK'), J0457 ('TRAPPED IN GLASS'), J0503
    ('DROP OF WATER'), J0549 ('BOILED CLEAR BROTH'), J0594 ('TINY LIVING CELLS'), or J0640
    ('STERILE LIQUID FLASK').
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
LOCAL_TC_BASE = SELECTED / "hos_001_thumb_B_sterile_liquid_flask_v06.jpg"
LOCAL_DROP_V01 = HERE.parent / "04_Generated-Clips" / "part02" / "refs" / "03_drop_of_water_v01.jpg"
B_BROTH_V04 = SELECTED / "hos_001_thumb_B_boiled_clear_broth_v04.jpg"
B_CELLS_V05 = SELECTED / "hos_001_thumb_B_tiny_living_cells_v05.jpg"
B_FLASK_V06 = SELECTED / "hos_001_thumb_B_sterile_liquid_flask_v06.jpg"
OUT = SELECTED / "hos_001_thumb_B_unseen_pond_microbes_v07.jpg"

W, H = 1280, 720
CREAM = (242, 214, 172)
CREAM_HI = (252, 238, 208)
GOLD = (228, 156, 32)
GOLD_HI = (248, 202, 68)
INK = (16, 9, 4)
SHADOW = (6, 3, 1)
GEORGIA = "/System/Library/Fonts/Supplemental/Georgia Bold.ttf"
TRACKING = -2
CONDENSE_X = 0.92

DROP_CROP_BOX = (104, 192, 1024, 928)
HERO_BOX = (588, 96, 1026, 534)
SLIDE_BOX = (420, 468, 1223, 650)
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
        (60, 318, 56, 518),
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


def compose_pushed_pond_drop_plate(tc_clean: Image.Image, drop_sq: Image.Image) -> Image.Image:
    """Composite 001's Part 02 glowing pond-water drop & glass slide on the right two-thirds
    with a 1.175x combined hero push-in (920x736 crop + 1.10x local sphere scale anchored at
    the slide contact point) and targeted microbe/slide-rim clarity boost, preserving 001's
    library bookcase, teal curtain, lower-left Explorer, and painted gold scroll flourishes."""
    crop_d = drop_sq.crop(DROP_CROP_BOX).resize((900, H), Image.Resampling.LANCZOS)
    right_full = tc_clean.copy()
    right_full.paste(crop_d, (380, 0))

    # Local 1.10x hero push-in on the glowing pond-water sphere anchored at its base on the slide
    scale = 1.10
    anchor_x, anchor_y = 808.0, 526.0
    a = 1.0 / scale
    c = anchor_x - anchor_x * a
    e = 1.0 / scale
    f = anchor_y - anchor_y * e
    pushed_sphere = right_full.transform(
        (W, H),
        Image.Transform.AFFINE,
        (a, 0.0, c, 0.0, e, f),
        resample=Image.Resampling.BICUBIC,
    )
    sphere_push_mask = Image.new("L", (W, H), 0)
    spd = ImageDraw.Draw(sphere_push_mask)
    spd.ellipse((500, 18, 1110, 560), fill=255)
    sphere_push_mask = sphere_push_mask.filter(ImageFilter.GaussianBlur(26))
    right_pushed = Image.composite(pushed_sphere, right_full, sphere_push_mask)

    mask = Image.new("L", (W, H), 0)
    m = mask.load()
    for y in range(H):
        for x in range(W):
            if y < 160:
                t_top = min(1.0, max(0.0, (160 - y) / 140.0))
                x0 = 565 + 95 * t_top
                x1 = 645 + 85 * t_top
            elif y < 420:
                x0, x1 = 565, 645
            else:
                t_bot = min(1.0, max(0.0, (y - 420) / 85.0))
                x0 = 565 * (1.0 - t_bot) + 415 * t_bot
                x1 = 645 * (1.0 - t_bot) + 520 * t_bot
            w = min(1.0, max(0.0, (x - x0) / max(1.0, (x1 - x0))))
            m[x, y] = int(255 * w)
    mask = mask.filter(ImageFilter.GaussianBlur(20))
    comp = Image.composite(right_pushed, tc_clean, mask)

    # Local clarity & contrast pop on the pushed-in glowing pond-water sphere and glass slide rim
    popped = ImageEnhance.Contrast(comp).enhance(1.18)
    popped = ImageEnhance.Sharpness(popped).enhance(1.32)
    pop_mask = Image.new("L", (W, H), 0)
    pd = ImageDraw.Draw(pop_mask)
    pd.ellipse((578, 88, 1038, 550), fill=245)
    pd.polygon([(430, 500), (810, 468), (1215, 555), (815, 645)], fill=185)
    pop_mask = pop_mask.filter(ImageFilter.GaussianBlur(22))
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
    if not LOCAL_TC_BASE.exists() or not LOCAL_DROP_V01.exists():
        raise SystemExit(f"Missing local source plates: {LOCAL_TC_BASE} / {LOCAL_DROP_V01}")

    tc_raw = Image.open(LOCAL_TC_BASE).convert("RGB").resize((W, H), Image.Resampling.LANCZOS)
    drop_sq = Image.open(LOCAL_DROP_V01).convert("RGB")
    tc_clean = wipe_old_lettering(tc_raw)
    base_plate = compose_pushed_pond_drop_plate(tc_clean, drop_sq)
    rgba = base_plate.convert("RGBA")

    # 3-word concrete visual hook per THUMBNAIL_AND_TITLE_RULES.md §1.2, §2.5 & §2.B:
    # UNSEEN / POND / MICROBES (cream 'UNSEEN', cream 'POND', gold punch word 'MICROBES')
    lines = [
        ("UNSEEN", "cream", 84),
        ("POND", "cream", 96),
        ("MICROBES", "gold", 76),
    ]
    sprites = []
    for text, kind, size in lines:
        fill, hi = (CREAM, CREAM_HI) if kind == "cream" else (GOLD, GOLD_HI)
        sprites.append((text, kind, size, render_word(text, size, fill, hi)))

    gaps = [-8, -6]
    total_h = sum(s[3].size[1] for s in sprites) + sum(gaps)
    # Fit strictly inside y=63..315 between top flourish (y<=59) and bottom flourish (y>=318)
    y = 64 + max(0, (250 - total_h) // 2)

    placed = []
    for idx_line, (text, kind, size, spr) in enumerate(sprites):
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
        if idx_line < len(gaps):
            y += spr.size[1] + gaps[idx_line]

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
    # B v04 (J0549: BOILED CLEAR BROTH) vs B v05 (J0594: TINY LIVING CELLS) vs B v06 (J0640: STERILE LIQUID FLASK) vs New B v07 (J0685: UNSEEN POND MICROBES, 1.175x push-in)
    phone = SELECTED / "hos_001_thumb_TC_4way_unseen_pond_microbes_v07_phone_168.jpg"
    fallback = Image.open(LIVE_A).convert("RGB")
    b4_im = Image.open(B_BROTH_V04).convert("RGB") if B_BROTH_V04.exists() else fallback
    b5_im = Image.open(B_CELLS_V05).convert("RGB") if B_CELLS_V05.exists() else fallback
    b6_im = Image.open(B_FLASK_V06).convert("RGB") if B_FLASK_V06.exists() else fallback
    panels = [
        ("B v04 (J0549: BOILED CLEAR BROTH)", "B v04", b4_im),
        ("B v05 (J0594: TINY LIVING CELLS)", "B v05", b5_im),
        ("B v06 (J0640: STERILE LIQUID FLASK)", "B v06", b6_im),
        ("New B v07 (J0685: UNSEEN POND MICROBES)", "New B v07", out),
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
        "job": "J0685",
        "variant": "B v07 (1.175x pond-water droplet hero push-in + microbe & slide-rim clarity boost + concrete pond-microbes hook; pairs with B v06 'STERILE LIQUID FLASK' and B v05 'TINY LIVING CELLS')",
        "maker": "gemini",
        "hook": "UNSEEN POND MICROBES",
        "punch": "MICROBES",
        "jpg": f"Selected/{OUT.name}",
        "sha256": hashlib.sha256(OUT.read_bytes()).hexdigest(),
        "bytes": OUT.stat().st_size,
        "plates": [
            f"04_Generated-Clips/part02/refs/{LOCAL_DROP_V01.name} (1024x1024 Part 02 pond-water drop master plate, crop {list(DROP_CROP_BOX)} + 1.10x local sphere push-in = 1.175x combined hero push-in on right two-thirds)",
            "08_Thumbnail/Selected/hos_001_tc_thumb_v02.jpg (001 painted library key-art plate: lower-left Explorer at 54.4% frame height + original painted gold scroll flourishes)",
        ],
        "method": "existing_001_plates_only_1.175x_pond_drop_hero_push_in_plus_explorer_and_painted_flourishes_GeorgiaBold",
        "spend": 0,
        "heroBox": list(HERO_BOX),
        "slideBox": list(SLIDE_BOX),
        "explorer": {
            "source": "hos_001_tc_thumb_v02.jpg",
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
            "HOOK": "PASS — 'UNSEEN POND MICROBES' (3 words, punch word 'MICROBES' in gold) names the concrete microorganisms visible inside Leeuwenhoek's glowing pond-water bead on the microscope slide (001 script Part 01 & Part 02: 'microbes drifting unseen... A drop of pond water is not empty. It is a bustling kingdom — darting shapes, spinning cells... People could watch microbes dance' and THUMBNAIL_AND_TITLE_RULES.md §1.2 & §2.B.1 'name the thing'), shares zero words with the video title ('How Did We Discover Germs?'), Live A ('WHAT PROVED GERMS WERE REAL?'), J0391 ('THE SWAN NECK'), J0457 ('TRAPPED IN GLASS'), J0503 ('DROP OF WATER'), J0549 ('BOILED CLEAR BROTH'), J0594 ('TINY LIVING CELLS'), or J0640 ('STERILE LIQUID FLASK'), and uses no vague questions or pronouns.",
            "BAND": f"PASS — Upper-left lettering band (x={left}..{right}, y={top}..{bottom}, framed by 001's original painted gold scroll flourishes at y=20..356) sits completely left of the pushed-in glowing pond-water sphere (x={HERO_BOX[0]}..{HERO_BOX[2]}), above the Explorer's hair (y={EXPLORER_BOX[1]}) and bottom flourish (y=318), and clear of the bottom-right duration badge.",
            "PHONE": "PASS — Checked on 168x94 preview sheet and 4-panel comparison strip: the 1.175x hero push-in and internal microbe + glass-slide rim clarity boost make the glowing pond-water sphere (438x438 px, +39% larger area than v03) and its faceless rods, spiked spheres, and golden spiral read immediately at 168x94 alongside 'UNSEEN POND MICROBES' and the lower-left Explorer (54.4% height).",
        },
        "previews": [
            f"Selected/{preview.name}",
            f"Selected/{sheet.name}",
            f"Selected/{phone.name}",
        ],
        "studio": False,
        "status": "Test & Compare B v07 candidate for 001 (_C92tIJCk8A, built from existing 001 plates only with 1.175x pond-drop hero push-in, £0). Parked for Chief: thumb B review. No Studio until OK.",
    }
    (HERE / "THUMB_B_UNSEEN_POND_MICROBES_v07.json").write_text(json.dumps(idx, indent=2) + "\n")
    print("DONE", OUT, idx["sha256"])


if __name__ == "__main__":
    main()
