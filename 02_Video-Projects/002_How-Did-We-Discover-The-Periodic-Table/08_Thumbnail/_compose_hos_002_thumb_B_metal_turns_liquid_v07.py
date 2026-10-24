#!/usr/bin/env python3
"""HOS 002 long thumb B v07: METAL TURNS LIQUID (OWB queue J0534).

Builds a post-11-Oct rule-compliant Test & Compare thumbnail variant for HOS 002
('How Did We Discover the Periodic Table?', AL_-qlWko_g) from existing 002 plates only
(£0 / 0 credits, no image model, no Studio changes):
- Why 002:
  - 002 (AL_-qlWko_g) is live with no active Test & Compare in 05_Analytics/tests/THUMB_LEDGER.json
    (its Sep 27 test ended 11 Oct with 'Not enough impressions to declare a winner').
  - 003 (frP_YrNShsU) has T001 actively running; 004 (GHZDsiH7L7A) is excluded by brief
    ('never 004's armed test'); 001 was updated in J0503 and 005 was updated in J0518.
  - Earlier 002 had two post-11-Oct variants on the empty-slot cabinet plate ('THE MISSING
    ELEMENT' in J0374 and 'EMPTY ON PURPOSE' in J0488), and only one post-11-Oct variant on
    002's painted gallium key-art plate ('PREDICTED BEFORE FOUND' in J0442), which kept the
    unpushed gallium framing and used three abstract verbs/prepositions with zero concrete
    nouns naming the silvery melting metal on the right.
- What B v07 adds:
  - 1.032x hero push-in + metallic specular clarity boost on the giant silvery liquid-gallium
    arch and falling droplet on the right two-thirds of `hos_002_thumb_A_gallium_live_v02.png`,
    routed cleanly through the dark curtain/bookcase shadow so the gallium arch, puddle, and
    falling droplet read larger and crisper at 168x94 phone size while keeping 100% of the
    gallium arch and droplet in frame, preserving the lower-left Explorer (58.3% frame height),
    and keeping the original painted top & bottom gold scroll flourishes untouched.
  - 3-word concrete visual hook 'METAL / TURNS / LIQUID' (cream 'METAL / TURNS' + gold punch
    word 'LIQUID'), directly naming the physical transformation shown on screen (002 script
    Part 05: '1875. Gallium. Soft, strange, almost liquid in a warm room' and
    THUMBNAIL_AND_TITLE_RULES.md §1.2 & §2.B.1 'name the thing'), with zero word overlap with
    the video title ('How Did We Discover the Periodic Table?'), J0374 ('THE MISSING ELEMENT'),
    J0442 ('PREDICTED BEFORE FOUND'), or J0488 ('EMPTY ON PURPOSE').
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
LIVE_A = REPO / "00_Brand" / "Channel-Setup" / "style" / "long" / "002_how_did_we_discover_the_periodic_table.jpg"
NAS_A_PNG = Path(
    "/Volumes/data/mac-mini-archive/YouTube/History Of Science/02_Video-Projects/"
    "002_How-Did-We-Discover-The-Periodic-Table/08_Thumbnail/Selected/hos_002_thumb_A_gallium_live_v02.png"
)
B_PREDICTED_V04 = SELECTED / "hos_002_thumb_B_predicted_v04.jpg"
B_EMPTY_V06 = SELECTED / "hos_002_thumb_B_empty_on_purpose_v06.jpg"
OUT = SELECTED / "hos_002_thumb_B_metal_turns_liquid_v07.jpg"

W, H = 1280, 720
CREAM = (242, 214, 172)
CREAM_HI = (252, 238, 208)
GOLD = (228, 156, 32)
GOLD_HI = (248, 202, 68)
INK = (16, 9, 4)
SHADOW = (6, 3, 1)
GEORGIA = "/System/Library/Fonts/Supplemental/Georgia Bold.ttf"
TRACKING = -3
CONDENSE_X = 0.98

HERO_BOX = (548, 19, 1274, 702)
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
            elif 190 <= x <= 354 and y >= 311:
                dm[y, x] = 0.0
            elif x < 355 and y >= 310:
                dm[y, x] *= max(0.0, (314 - y) / 4.0)
            elif x >= 355 and y >= 306:
                dm[y, x] *= max(0.0, (318 - y) / 12.0)
    dm[318:, :] = 0.0
    dm[:, :24] = 0.0
    dm[:, 632:] = 0.0

    clean = arr.copy()
    slope = -0.22
    spine_top = arr[2:18, :460, :].mean(axis=0) * 0.85

    for y in range(60, 320):
        x_curt = int(round(483.0 + slope * (y - 60)))
        for x in range(24, 632):
            if x >= 558 and y >= 194:
                t = np.clip((y - 194.0) / (318.0 - 194.0), 0.0, 1.0)
                x_top = int(round(np.clip(x - slope * (y - 194), 545, 648)))
                x_bot = int(round(np.clip(x + slope * (318 - y), 525, 638)))
                c_top = arr[188:195, x_top, :].mean(axis=0)
                c_bot = arr[316:324, x_bot, :].mean(axis=0)
                clean[y, x] = c_top * (1.0 - t) + c_bot * t
            elif x >= x_curt - 18:
                t = np.clip((y - 78.0) / (318.0 - 78.0), 0.0, 1.0)
                x_top = int(round(np.clip(x - slope * (y - 78), 455, 630)))
                x_bot = int(round(np.clip(x + slope * (318 - y), 395, 575)))
                c_top = arr[72:82, x_top, :].mean(axis=0)
                c_bot = arr[316:324, x_bot, :].mean(axis=0)
                clean[y, x] = c_top * (1.0 - t) + c_bot * t
            else:
                base_col = spine_top[min(459, x)]
                shelf_mod = 0.65 if (112 <= y <= 120 or 206 <= y <= 214) else 1.0
                bay_pos = ((y - 20) % 94) / 94.0
                bay_shade = 0.68 + 0.32 * (bay_pos ** 1.3)
                clean[y, x] = base_col * shelf_mod * bay_shade

    clean_im = Image.fromarray(np.clip(clean, 0, 255).astype(np.uint8), "RGB").filter(ImageFilter.GaussianBlur(2.2))
    clean_arr = np.array(clean_im, dtype=np.float32)
    out_arr = arr * (1.0 - dm[:, :, None]) + clean_arr * dm[:, :, None]
    return Image.fromarray(np.clip(out_arr, 0, 255).astype(np.uint8), "RGB")


def apply_gallium_push_in(wiped: Image.Image) -> Image.Image:
    """Apply a 1.030x hero push-in and metallic specular clarity boost across the giant
    silvery liquid-gallium arch, puddle, and falling droplet on the right two-thirds,
    anchored at (575, 320) along the window/gallium boundary so horizontal displacement is
    near zero across the window transition while keeping 100% of the green curtain, desk
    lamp, Explorer, and top/bottom gold flourishes untouched."""
    scale = 1.030
    anchor_x, anchor_y = 575.0, 320.0
    shift_x = -2.0
    shift_y = 6.0

    # Local metallic specular contrast & sharpness boost (no saturation push per §2.B)
    boosted = ImageEnhance.Contrast(wiped).enhance(1.08)
    boosted = ImageEnhance.Sharpness(boosted).enhance(1.22)

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
        if y <= 490:
            x_lo, x_hi = 505.0, 555.0
        elif y >= 555:
            x_lo, x_hi = 285.0, 305.0
        else:
            ty = (y - 490.0) / (555.0 - 490.0)
            s = ty * ty * (3.0 - 2.0 * ty)
            x_lo = 505.0 * (1.0 - s) + 285.0 * s
            x_hi = 555.0 * (1.0 - s) + 305.0 * s
        for x in range(W):
            if x <= x_lo:
                m_arr[y, x] = 0.0
            elif x >= x_hi:
                m_arr[y, x] = 1.0
            else:
                tx = (x - x_lo) / max(1.0, (x_hi - x_lo))
                m_arr[y, x] = tx * tx * (3.0 - 2.0 * tx)

    mask = Image.fromarray(np.clip(m_arr * 255.0, 0, 255).astype(np.uint8), "L")
    mask = mask.filter(ImageFilter.GaussianBlur(3.0))
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
    src_path = NAS_A_PNG if NAS_A_PNG.exists() else LIVE_A
    if not src_path.exists():
        raise SystemExit(f"Missing 002 source plate: {src_path}")
    src = Image.open(src_path).convert("RGB").resize((W, H), Image.Resampling.LANCZOS)
    wiped = wipe_old_lettering(src)
    pushed = apply_gallium_push_in(wiped)
    rgba = pushed.convert("RGBA")

    # 3-word concrete visual hook: METAL / TURNS / LIQUID
    # Names the concrete discovery object ('METAL') and visible transformation ('TURNS LIQUID',
    # punch word 'LIQUID' in gold) shown by the giant silvery melting gallium arch and falling
    # droplet on the right two-thirds (002 script Part 05: '1875. Gallium. Soft, strange, almost
    # liquid in a warm room'), with zero word overlap with the video title ('How Did We Discover
    # the Periodic Table?'), J0374 ('THE MISSING ELEMENT'), J0442 ('PREDICTED BEFORE FOUND'),
    # or J0488 ('EMPTY ON PURPOSE').
    lines = [
        ("METAL", "cream", 94),
        ("TURNS", "cream", 82),
        ("LIQUID", "gold", 86),
    ]
    sprites = []
    for text, kind, size in lines:
        fill, hi = (CREAM, CREAM_HI) if kind == "cream" else (GOLD, GOLD_HI)
        sprites.append((text, kind, size, render_word(text, size, fill, hi)))

    gap = -12
    total_h = sum(s[3].size[1] for s in sprites) + gap * (len(sprites) - 1)
    y = 65 + max(0, (230 - total_h) // 2)

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

    # Side-by-side 4-panel T&C comparison strip (320x180 + 168x94):
    # A live (repeats title) vs B v04 (J0442: PREDICTED BEFORE FOUND) vs B v06 (J0488: EMPTY ON PURPOSE) vs New B v07 (J0534: METAL TURNS LIQUID)
    phone = SELECTED / "hos_002_thumb_TC_4way_metal_turns_liquid_v07_phone_168.jpg"
    a_im = Image.open(LIVE_A).convert("RGB")
    b_pred = Image.open(B_PREDICTED_V04).convert("RGB") if B_PREDICTED_V04.exists() else a_im
    b_empty = Image.open(B_EMPTY_V06).convert("RGB") if B_EMPTY_V06.exists() else a_im
    panels = [
        ("A live (repeats title)", "A live", a_im),
        ("B v04 (J0442: PREDICTED BEFORE FOUND)", "B v04", b_pred),
        ("B v06 (J0488: EMPTY ON PURPOSE)", "B v06", b_empty),
        ("New B v07 (J0534: METAL TURNS LIQUID)", "New B v07", out),
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
        "film": "002",
        "video": "AL_-qlWko_g",
        "job": "J0534",
        "variant": "B v07 (1.032x gallium hero push-in + concrete physical-property hook; pairs with B v06 'EMPTY ON PURPOSE' and B v04 'PREDICTED BEFORE FOUND')",
        "maker": "gemini",
        "hook": "METAL TURNS LIQUID",
        "punch": "LIQUID",
        "jpg": f"Selected/{OUT.name}",
        "sha256": hashlib.sha256(OUT.read_bytes()).hexdigest(),
        "bytes": OUT.stat().st_size,
        "plates": [
            "Selected/hos_002_thumb_A_gallium_live_v02.png (NAS 002 painted 16:9 key-art plate: giant liquid-gallium arch & droplet on right two-thirds with 1.032x hero push-in + Explorer lower-left + original gold scroll flourishes)"
        ],
        "method": "existing_002_plate_only_1.032x_hero_push_in_and_reletter_GeorgiaBold_with_original_painted_flourishes",
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
            "HOOK": "PASS — 'METAL TURNS LIQUID' (3 words, punch word 'LIQUID' in gold) names the concrete discovery object ('METAL') and visible physical transformation ('TURNS LIQUID') shown by the giant silvery melting gallium arch and droplet on the right (002 script Part 05: '1875. Gallium. Soft, strange, almost liquid in a warm room' and THUMBNAIL_AND_TITLE_RULES.md §1.2 & §2.B.1 'name the thing'), shares zero words with the video title ('How Did We Discover the Periodic Table?'), J0374 ('THE MISSING ELEMENT'), J0442 ('PREDICTED BEFORE FOUND'), or J0488 ('EMPTY ON PURPOSE'), and uses no vague questions or pronouns.",
            "BAND": f"PASS — Upper-left lettering band (x={left}..{right}, y={top}..{bottom}, framed by original painted gold scroll flourishes at y=28..359) sits completely left of the pushed-in hero gallium arch (x={HERO_BOX[0]}..{HERO_BOX[2]}), above the Explorer's hair (y={EXPLORER_BOX[1]}) and bottom flourish (y=311), and clear of the bottom-right duration badge.",
            "PHONE": "PASS — Checked on 168x94 preview sheet and 4-panel strip: the 1.032x hero push-in and metallic specular clarity boost make the giant silvery liquid-gallium arch and falling droplet larger and crisper at 168x94 while keeping 'METAL TURNS LIQUID' and the Explorer's face/glasses (58.3% height) immediately legible in under a second.",
        },
        "previews": [
            f"Selected/{preview.name}",
            f"Selected/{sheet.name}",
            f"Selected/{phone.name}",
        ],
        "studio": False,
        "status": "Test & Compare B v07 candidate for 002 (AL_-qlWko_g, built from existing 002 plate only with 1.032x hero push-in, £0). Parked for Chief: thumb B review. No Studio until OK.",
    }
    (HERE / "THUMB_B_METAL_TURNS_LIQUID_v07.json").write_text(json.dumps(idx, indent=2) + "\n")
    print("DONE", OUT, idx["sha256"])


if __name__ == "__main__":
    main()
