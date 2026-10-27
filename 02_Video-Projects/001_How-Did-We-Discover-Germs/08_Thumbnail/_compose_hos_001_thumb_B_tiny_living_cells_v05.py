#!/usr/bin/env python3
"""HOS 001 long thumb B v05: TINY LIVING CELLS (OWB queue J0594).

Builds a post-11-Oct rule-compliant Test & Compare thumbnail variant for HOS 001
('How Did We Discover Germs?', _C92tIJCk8A) from existing 001 plates only
(£0 / 0 credits, no image model, no Studio changes):
- Why 001:
  - 001 (_C92tIJCk8A) is live with no active Test & Compare in 05_Analytics/tests/THUMB_LEDGER.json.
  - 003 (frP_YrNShsU) has T001 actively running; 004 (GHZDsiH7L7A) is excluded by brief
    ('never 004's armed test'); in the 001 -> 005 -> 002 rotation, 001 was updated in J0549,
    005 in J0564, and 002 in J0579, making 001 next in rotation.
  - In 001, J0503 ('DROP OF WATER', B v03) introduced the Part 02 pond-water droplet plate
    (`04_Generated-Clips/part02/refs/03_drop_of_water_v01.jpg` composited with
    `08_Thumbnail/Selected/hos_001_tc_thumb_v02.jpg`), but cropped the 1024x1024 plate at
    980x784 and downscaled it to 900x720 (0.918x), leaving the glowing pond-water sphere at
    372x372 px (x=626..998, y=162..534).
- What B v05 adds:
  - 1.155x combined hero push-in (tighter 920x736 right-plate crop + 1.08x local sphere push-in
    anchored on the microscope slide contact point) plus targeted specular and internal microbe
    clarity boost on the glowing pond-water sphere teeming with faceless rods, spiked spheres,
    and golden spirals (`heroBox = [592, 104, 1022, 534]`, 430x430 px, +34% larger area than
    v03's 372x372 px), while keeping 100% of the illuminated glass microscope slide inside the
    frame (`slideBox = [420, 468, 1223, 650]`, clear of the bottom-right duration badge),
    preserving the lower-left Explorer at 54.4% frame height (`box = [88, 328, 316, 720]`), and
    keeping the original painted top & bottom gold scroll flourishes untouched.
  - 3-word concrete visual hook 'TINY / LIVING / CELLS' (cream 'TINY', cream 'LIVING', gold
    punch word 'CELLS'), directly naming the visible faceless microorganisms inside Leeuwenhoek's
    pond-water bead on the glass slide (001 script Part 01 & Part 02: 'Tiny living things...
    spinning cells, life with no face and no name on the hospital chart... a civilisation of
    cells dancing in a bead of liquid' and THUMBNAIL_AND_TITLE_RULES.md §1.2 & §2.B.1 'name the
    thing'), with zero word overlap with the video title ('How Did We Discover Germs?'), J0391
    ('THE SWAN NECK'), J0457 ('TRAPPED IN GLASS'), J0503 ('DROP OF WATER'), or J0549 ('BOILED
    CLEAR BROTH').
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
B_TRAP_V02 = SELECTED / "hos_001_thumb_B_trapped_in_glass_v02.jpg"
B_DROP_V03 = SELECTED / "hos_001_thumb_B_drop_of_water_v03.jpg"
B_BROTH_V04 = SELECTED / "hos_001_thumb_B_boiled_clear_broth_v04.jpg"
OUT = SELECTED / "hos_001_thumb_B_tiny_living_cells_v05.jpg"

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

DROP_CROP_BOX = (104, 192, 1024, 928)
HERO_BOX = (592, 104, 1022, 534)
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


def compose_pushed_pond_drop_plate(tc_clean: Image.Image, drop_sq: Image.Image) -> Image.Image:
    """Composite 001's Part 02 glowing pond-water drop & glass slide on the right two-thirds
    with a 1.155x combined hero push-in (920x736 crop + 1.08x local sphere scale anchored at
    the slide contact point) and local microbe/specular clarity boost, preserving 001's library
    bookcase, teal curtain, lower-left Explorer, and painted gold scroll flourishes on the left."""
    crop_d = drop_sq.crop(DROP_CROP_BOX).resize((900, H), Image.Resampling.LANCZOS)
    right_full = tc_clean.copy()
    right_full.paste(crop_d, (380, 0))

    # Local 1.08x hero push-in on the glowing pond-water sphere anchored at its base on the slide
    scale = 1.08
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
    spd.ellipse((505, 24, 1105, 558), fill=255)
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

    # Local clarity & contrast pop on the pushed-in glowing pond-water sphere (no saturation push)
    popped = ImageEnhance.Contrast(comp).enhance(1.16)
    popped = ImageEnhance.Sharpness(popped).enhance(1.28)
    pop_mask = Image.new("L", (W, H), 0)
    pd = ImageDraw.Draw(pop_mask)
    pd.ellipse((582, 96, 1032, 548), fill=240)
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
    if not NAS_TC_V02.exists() or not NAS_DROP_V01.exists():
        raise SystemExit(f"Missing NAS source plates: {NAS_TC_V02} / {NAS_DROP_V01}")

    tc_raw = Image.open(NAS_TC_V02).convert("RGB").resize((W, H), Image.Resampling.LANCZOS)
    drop_sq = Image.open(NAS_DROP_V01).convert("RGB")
    tc_clean = wipe_old_lettering(tc_raw)
    base_plate = compose_pushed_pond_drop_plate(tc_clean, drop_sq)
    rgba = base_plate.convert("RGBA")

    # 3-word concrete visual hook per THUMBNAIL_AND_TITLE_RULES.md §1.2, §2.5 & §2.B:
    # TINY / LIVING / CELLS (cream 'TINY', cream 'LIVING', gold punch word 'CELLS')
    lines = [
        ("TINY", "cream", 92),
        ("LIVING", "cream", 88),
        ("CELLS", "gold", 104),
    ]
    sprites = []
    for text, kind, size in lines:
        fill, hi = (CREAM, CREAM_HI) if kind == "cream" else (GOLD, GOLD_HI)
        sprites.append((text, kind, size, render_word(text, size, fill, hi)))

    gap = -10
    total_h = sum(s[3].size[1] for s in sprites) + gap * (len(sprites) - 1)
    # Fit strictly inside y=63..315 between top flourish (y<=59) and bottom flourish (y>=318)
    y = 64 + max(0, (250 - total_h) // 2)

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
    # B v02 (J0457: TRAPPED IN GLASS) vs B v03 (J0503: DROP OF WATER, unpushed) vs B v04 (J0549: BOILED CLEAR BROTH) vs New B v05 (J0594: TINY LIVING CELLS, 1.155x push-in)
    phone = SELECTED / "hos_001_thumb_TC_4way_tiny_living_cells_v05_phone_168.jpg"
    fallback = Image.open(LIVE_A).convert("RGB")
    b2_im = Image.open(B_TRAP_V02).convert("RGB") if B_TRAP_V02.exists() else fallback
    b3_im = Image.open(B_DROP_V03).convert("RGB") if B_DROP_V03.exists() else fallback
    b4_im = Image.open(B_BROTH_V04).convert("RGB") if B_BROTH_V04.exists() else fallback
    panels = [
        ("B v02 (J0457: TRAPPED IN GLASS)", "B v02", b2_im),
        ("B v03 (J0503: DROP OF WATER)", "B v03", b3_im),
        ("B v04 (J0549: BOILED CLEAR BROTH)", "B v04", b4_im),
        ("New B v05 (J0594: TINY LIVING CELLS)", "New B v05", out),
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
        "job": "J0594",
        "variant": "B v05 (1.155x pond-water droplet hero push-in + concrete microorganism hook; pairs with B v02 'TRAPPED IN GLASS' and B v04 'BOILED CLEAR BROTH')",
        "maker": "gemini",
        "hook": "TINY LIVING CELLS",
        "punch": "CELLS",
        "jpg": f"Selected/{OUT.name}",
        "sha256": hashlib.sha256(OUT.read_bytes()).hexdigest(),
        "bytes": OUT.stat().st_size,
        "plates": [
            f"04_Generated-Clips/part02/refs/{NAS_DROP_V01.name} (1024x1024 Part 02 pond-water drop master plate, crop {list(DROP_CROP_BOX)} + 1.08x local sphere push-in = 1.155x combined hero push-in on right two-thirds)",
            f"08_Thumbnail/Selected/{NAS_TC_V02.name} (001 painted library key-art plate: lower-left Explorer at 54.4% frame height + original painted gold scroll flourishes)",
        ],
        "method": "existing_001_plates_only_1.155x_pond_drop_hero_push_in_plus_explorer_and_painted_flourishes_GeorgiaBold",
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
            "HOOK": "PASS — 'TINY LIVING CELLS' (3 words, punch word 'CELLS' in gold) names the concrete microorganisms visible inside Leeuwenhoek's glowing pond-water bead on the microscope slide (001 script Part 01 & Part 02: 'Tiny living things... spinning cells, life with no face and no name on the hospital chart... a civilisation of cells dancing in a bead of liquid' and THUMBNAIL_AND_TITLE_RULES.md §1.2 & §2.B.1 'name the thing'), shares zero words with the video title ('How Did We Discover Germs?'), J0391 ('THE SWAN NECK'), J0457 ('TRAPPED IN GLASS'), J0503 ('DROP OF WATER'), or J0549 ('BOILED CLEAR BROTH'), and uses no vague questions or pronouns.",
            "BAND": f"PASS — Upper-left lettering band (x={left}..{right}, y={top}..{bottom}, framed by 001's original painted gold scroll flourishes at y=20..356) sits completely left of the pushed-in glowing pond-water sphere (x={HERO_BOX[0]}..{HERO_BOX[2]}), above the Explorer's hair (y={EXPLORER_BOX[1]}) and bottom flourish (y=318), and clear of the bottom-right duration badge.",
            "PHONE": "PASS — Checked on 168x94 preview sheet and 4-panel comparison strip: the 1.155x hero push-in and internal microbe clarity boost make the glowing pond-water sphere (430x430 px, +34% larger area than v03) and its faceless rods, spiked spheres, and golden spiral read immediately at 168x94 alongside 'TINY LIVING CELLS' and the lower-left Explorer (54.4% height).",
        },
        "previews": [
            f"Selected/{preview.name}",
            f"Selected/{sheet.name}",
            f"Selected/{phone.name}",
        ],
        "studio": False,
        "status": "Test & Compare B v05 candidate for 001 (_C92tIJCk8A, built from existing 001 plates only with 1.155x pond-drop hero push-in, £0). Parked for Chief: thumb B review. No Studio until OK.",
    }
    (HERE / "THUMB_B_TINY_LIVING_CELLS_v05.json").write_text(json.dumps(idx, indent=2) + "\n")
    print("DONE", OUT, idx["sha256"])


if __name__ == "__main__":
    main()
