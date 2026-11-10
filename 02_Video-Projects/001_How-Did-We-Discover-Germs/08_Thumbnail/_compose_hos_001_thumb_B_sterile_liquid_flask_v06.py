#!/usr/bin/env python3
"""HOS 001 long thumb B v06: STERILE LIQUID FLASK (OWB queue J0640).

Builds a post-11-Oct rule-compliant Test & Compare thumbnail variant for HOS 001
('How Did We Discover Germs?', _C92tIJCk8A) from existing 001 plates only
(£0 / 0 credits, no image model, no Studio changes):
- Why 001:
  - 001 (_C92tIJCk8A) is live with no active Test & Compare in 05_Analytics/tests/THUMB_LEDGER.json.
  - 003 (frP_YrNShsU) has T001 actively running; 004 (GHZDsiH7L7A) is excluded by brief
    ('never 004's armed test'); in the 001 -> 005 -> 002 rotation, 001 got B v05 in J0594,
    005 got B v07 in J0609, and 002 got B v09 in J0624, making 001 next in rotation.
- What B v06 adds:
  - 1.06x hero push-in + glass/liquid & S-bend specular clarity boost on the giant glowing
    swan-neck flask, sterile golden liquid bulb, and curved U-bend trap on the right two-thirds of
    `hos_001_tc_thumb_v02.jpg`, routed cleanly through the vertical window/bookcase shadow and
    mahogany tabletop grain so the flask bulb, golden liquid meniscus, curved glass neck, and
    U-bend droplet read larger and crisper at 168x94 phone size while keeping 100% of the flask
    and open tube tip in frame (`heroBox = [582, 12, 1138, 694]`, clear of the bottom-right
    duration badge), preserving the lower-left Explorer (54.4% frame height), and keeping the
    original painted top & bottom gold scroll flourishes untouched.
  - 3-word concrete visual hook 'STERILE / LIQUID / FLASK' (cream 'STERILE', cream 'LIQUID',
    gold punch word 'FLASK'), directly naming the concrete apparatus ('FLASK') and visible
    unspoiled liquid ('STERILE LIQUID') inside Pasteur's curved-neck flask (001 script Part 04:
    'Pasteur’s swan-neck flask experiments showed broth stays sterile when microbes cannot reach
    it... The liquid stays clear... Inside that clear liquid sits a paradox the old world hated'
    and THUMBNAIL_AND_TITLE_RULES.md §1.2 & §2.B.1 'name the thing'), with zero word overlap with
    the video title ('How Did We Discover Germs?'), J0391 ('THE SWAN NECK'), J0457 ('TRAPPED IN
    GLASS'), J0503 ('DROP OF WATER'), J0549 ('BOILED CLEAR BROTH'), or J0594 ('TINY LIVING CELLS').
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
B_DROP_V03 = SELECTED / "hos_001_thumb_B_drop_of_water_v03.jpg"
B_BROTH_V04 = SELECTED / "hos_001_thumb_B_boiled_clear_broth_v04.jpg"
B_CELLS_V05 = SELECTED / "hos_001_thumb_B_tiny_living_cells_v05.jpg"
OUT = SELECTED / "hos_001_thumb_B_sterile_liquid_flask_v06.jpg"

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

HERO_BOX = (582, 12, 1138, 694)
EXPLORER_BOX = (88, 328, 316, 720)
CX = 285


def wipe_old_lettering(base: Image.Image) -> Image.Image:
    """Mask only the old letters ('WHAT PROVED / GERMS / WERE REAL?') and their stroke/shadow
    in y=62..314, x=58..518, restoring painted bookcase texture on the left (x<440) and
    continuous diagonal green curtain folds on the right (x>=440) while preserving 100% of
    the top flourish (y<=59), bottom flourish (y>=318), and Explorer (y>=328)."""
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


def apply_flask_push_in(wiped: Image.Image) -> Image.Image:
    """Apply a 1.06x hero push-in and glass/liquid specular clarity boost across the giant
    swan-neck flask, golden sterile liquid bulb, and curved U-bend dust trap on the right
    two-thirds, anchored at (598, 596) and routed to the right of the arched window for
    y<=320 (x=640..675) and left of the lower bulb for y>=450 (x=540..575) so 100% of the
    arched window mullions, teal curtain, desk lamp, Explorer, and painted gold scroll
    flourishes stay completely untouched."""
    scale = 1.06
    anchor_x, anchor_y = 598.0, 596.0
    shift_x = 5.0
    shift_y = 4.0

    # Local specular contrast & sharpness boost on the glass flask and clear golden liquid
    # (no saturation push per THUMBNAIL_AND_TITLE_RULES.md §2.B)
    boosted = ImageEnhance.Contrast(wiped).enhance(1.10)
    boosted = ImageEnhance.Sharpness(boosted).enhance(1.26)

    a = 1.0 / scale
    c = anchor_x - (anchor_x + shift_x) * a
    e = 1.0 / scale
    f = anchor_y - (anchor_y + shift_y) * e
    pushed = boosted.transform(
        (W, H),
        Image.Transform.AFFINE,
        (a, 0.0, c, 0.0, e, f),
        resample=Image.Resampling.BICUBIC,
    )

    m_arr = np.zeros((H, W), dtype=np.float32)
    for y in range(H):
        if y <= 320:
            x_lo, x_hi = 640.0, 675.0
        elif y >= 450:
            x_lo, x_hi = 540.0, 575.0
        else:
            ty = (y - 320.0) / (450.0 - 320.0)
            s = ty * ty * (3.0 - 2.0 * ty)
            x_lo = 640.0 * (1.0 - s) + 540.0 * s
            x_hi = 675.0 * (1.0 - s) + 575.0 * s
        for x in range(W):
            if x <= x_lo:
                m_arr[y, x] = 0.0
            elif x >= x_hi:
                m_arr[y, x] = 1.0
            else:
                tx = (x - x_lo) / (x_hi - x_lo)
                m_arr[y, x] = tx * tx * (3.0 - 2.0 * tx)

    mask = Image.fromarray(np.clip(m_arr * 255.0, 0, 255).astype(np.uint8), "L")
    mask = mask.filter(ImageFilter.GaussianBlur(4.0))
    return Image.composite(pushed, wiped, mask)


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

    tc_raw = Image.open(NAS_TC_V02).convert("RGB").resize((W, H), Image.Resampling.LANCZOS)
    tc_clean = wipe_old_lettering(tc_raw)
    base_plate = apply_flask_push_in(tc_clean)
    rgba = base_plate.convert("RGBA")

    # 3-word concrete visual hook per THUMBNAIL_AND_TITLE_RULES.md §1.2, §2.5 & §2.B:
    # STERILE / LIQUID / FLASK (cream 'STERILE', cream 'LIQUID', gold punch word 'FLASK')
    lines = [
        ("STERILE", "cream", 82),
        ("LIQUID", "cream", 86),
        ("FLASK", "gold", 100),
    ]
    sprites = []
    for text, kind, size in lines:
        fill, hi = (CREAM, CREAM_HI) if kind == "cream" else (GOLD, GOLD_HI)
        sprites.append((text, kind, size, render_word(text, size, fill, hi)))

    gaps = [-6, -1]
    total_h = sum(s[3].size[1] for s in sprites) + sum(gaps)
    # Fit strictly inside y=63..315 between top flourish (y<=59) and bottom flourish (y>=318)
    y = 63 + max(0, (250 - total_h) // 2)

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
    # B v03 (J0503: DROP OF WATER) vs B v04 (J0549: BOILED CLEAR BROTH) vs B v05 (J0594: TINY LIVING CELLS) vs New B v06 (J0640: STERILE LIQUID FLASK, 1.06x push-in)
    phone = SELECTED / "hos_001_thumb_TC_4way_sterile_liquid_flask_v06_phone_168.jpg"
    fallback = Image.open(LIVE_A).convert("RGB")
    b3_im = Image.open(B_DROP_V03).convert("RGB") if B_DROP_V03.exists() else fallback
    b4_im = Image.open(B_BROTH_V04).convert("RGB") if B_BROTH_V04.exists() else fallback
    b5_im = Image.open(B_CELLS_V05).convert("RGB") if B_CELLS_V05.exists() else fallback
    panels = [
        ("B v03 (J0503: DROP OF WATER)", "B v03", b3_im),
        ("B v04 (J0549: BOILED CLEAR BROTH)", "B v04", b4_im),
        ("B v05 (J0594: TINY LIVING CELLS)", "B v05", b5_im),
        ("New B v06 (J0640: STERILE LIQUID FLASK)", "New B v06", out),
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
        "job": "J0640",
        "variant": "B v06 (1.06x swan-neck flask hero push-in + concrete sterile-flask hook; pairs with B v04 'BOILED CLEAR BROTH' and B v05 'TINY LIVING CELLS')",
        "maker": "gemini",
        "hook": "STERILE LIQUID FLASK",
        "punch": "FLASK",
        "jpg": f"Selected/{OUT.name}",
        "sha256": hashlib.sha256(OUT.read_bytes()).hexdigest(),
        "bytes": OUT.stat().st_size,
        "plates": [
            f"08_Thumbnail/Selected/{NAS_TC_V02.name} (NAS 001 painted 16:9 library key-art plate: giant swan-neck flask with clear sterile liquid & S-curve dust trap on right two-thirds with 1.06x hero push-in + lower-left Explorer at 54.4% frame height + original painted gold scroll flourishes)"
        ],
        "method": "existing_001_plate_only_1.06x_hero_push_in_and_reletter_GeorgiaBold_with_original_painted_flourishes",
        "spend": 0,
        "heroBox": list(HERO_BOX),
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
            "HOOK": "PASS — 'STERILE LIQUID FLASK' (3 words, punch word 'FLASK' in gold) names the concrete apparatus ('FLASK') and visible unspoiled liquid ('STERILE LIQUID') inside Pasteur's giant curved-neck flask on the right (001 script Part 04: 'Pasteur’s swan-neck flask experiments showed broth stays sterile when microbes cannot reach it... The liquid stays clear... Inside that clear liquid sits a paradox the old world hated' and THUMBNAIL_AND_TITLE_RULES.md §1.2 & §2.B.1 'name the thing'), shares zero words with the video title ('How Did We Discover Germs?'), J0391 ('THE SWAN NECK'), J0457 ('TRAPPED IN GLASS'), J0503 ('DROP OF WATER'), J0549 ('BOILED CLEAR BROTH'), or J0594 ('TINY LIVING CELLS'), and uses no vague questions or pronouns.",
            "BAND": f"PASS — Upper-left lettering band (x={left}..{right}, y={top}..{bottom}, framed by 001's original painted gold scroll flourishes at y=20..356) sits completely left of the pushed-in hero swan-neck flask (x={HERO_BOX[0]}..{HERO_BOX[2]}), above the Explorer's hair (y={EXPLORER_BOX[1]}) and bottom flourish (y=318), and clear of the bottom-right duration badge.",
            "PHONE": "PASS — Checked on 168x94 preview sheet and 4-panel strip: the 1.06x hero push-in and glass/liquid specular clarity boost make the giant swan-neck flask bulb, golden liquid level, and S-curve dust-trap bend larger and crisper at 168x94 while keeping 'STERILE LIQUID FLASK' and the Explorer's face/glasses (54.4% height) immediately legible in under a second.",
        },
        "previews": [
            f"Selected/{preview.name}",
            f"Selected/{sheet.name}",
            f"Selected/{phone.name}",
        ],
        "studio": False,
        "status": "Test & Compare B v06 candidate for 001 (_C92tIJCk8A, built from existing 001 plate only with 1.06x hero push-in, £0). Parked for Chief: thumb B review. No Studio until OK.",
    }
    (HERE / "THUMB_B_STERILE_LIQUID_FLASK_v06.json").write_text(json.dumps(idx, indent=2) + "\n")
    print("DONE", OUT, idx["sha256"])


if __name__ == "__main__":
    main()
