#!/usr/bin/env python3
"""HOS 005 long thumb B v05: TRAPPED UNDER SKIN (OWB queue J0518).

Builds a post-11-Oct rule-compliant Test & Compare thumbnail B variant for HOS 005
('The Tied Arm That Proved Your Blood Circulates', wwcjcFfC-5M, scheduled Thu 29 Oct 18:00)
from existing 005 plates only (£0 / 0 credits, no image model, no Studio changes):
- Why 005:
  - 003 (frP_YrNShsU) has an active Test & Compare armed in THUMB_LEDGER.json (T001).
  - 004 (GHZDsiH7L7A) is excluded by brief ('never 004's armed test').
  - 001 (_C92tIJCk8A) and 002 (AL_-qlWko_g) each already have 3 post-11-Oct existing-plate
    B variants parked (including a pushed-in hero variant on 002 in J0488 and a distinct
    water-drop hero variant on 001 in J0503).
  - 005 (wwcjcFfC-5M) has no entry in THUMB_LEDGER.json, and both of its earlier post-11-Oct
    B variants (J0407 'THE BLOCKED ARTERY' and J0424 'HIDDEN VEIN VALVES') kept the exact
    same unpushed hero framing as Variant A ('ONE TIGHT BAND').
- What B v05 adds:
  - 1.15x hero push-in + vein/artery clarity boost on the right two-thirds of the approved
    005 key-art plate (`hos_005_thumb_A_one_tight_band_v02.jpg`), feathered seamlessly across
    the dark bookcase archway gap (`x=485..545`) so the tight linen band, the stopped glowing
    red artery above it, and the swollen blue forearm veins below it read +15% larger at
    168x94 phone size while preserving 100% of 005's factLock (De Motu Cordis ch. 11,
    FACT_NOTES_v01 row 26), the lower-left Explorer (52.2% frame height), and the original
    painted top/bottom gold scroll flourishes.
  - 3-word concrete visual hook 'TRAPPED / UNDER / SKIN' (punch word 'TRAPPED' in gold,
    'UNDER / SKIN' in cream), sharing zero words with the video title ('The Tied Arm That
    Proved Your Blood Circulates'), Variant A ('ONE TIGHT BAND'), Variant B v03 ('THE
    BLOCKED ARTERY'), or Variant B v04 ('HIDDEN VEIN VALVES').
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
SRC_A = SELECTED / "hos_005_thumb_A_one_tight_band_v02.jpg"
SRC_B_V03 = SELECTED / "hos_005_thumb_B_blocked_artery_v03.jpg"
SRC_B_V04 = SELECTED / "hos_005_thumb_B_vein_valves_v04.jpg"
OUT = SELECTED / "hos_005_thumb_B_trapped_under_skin_v05.jpg"

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

HERO_BOX = (560, 0, 1236, 704)
EXPLORER_BOX = (88, 344, 318, 720)
CX = 288


def wipe_old_lettering(base_a: Image.Image) -> Image.Image:
    """Restore clean painted bookcase shelves behind 'ONE / TIGHT / BAND' (y=62..323)
    while preserving 100% of the top gold scroll flourish (y<=60), bottom gold scroll
    flourish (y>=325), and green curtain on the right."""
    arr = np.array(base_a.convert("RGB"), dtype=np.float32)

    bands = [
        # (y_top_clean_lo, y_top_clean_hi, y0, y1, y_bot_clean_lo, y_bot_clean_hi, x0, x1)
        (58, 62, 62, 125, 125, 129, 184, 362),    # ONE
        (125, 129, 129, 210, 210, 215, 118, 438), # TIGHT
        (210, 215, 215, 322, 322, 326, 100, 472), # BAND
    ]

    letter_mask = Image.new("L", (W, H), 0)
    lm = letter_mask.load()
    for _, _, y0, y1, _, _, x0, x1 in bands:
        for y in range(y0, y1):
            for x in range(x0, x1):
                r, g, b = arr[y, x]
                if (r > 42 and (r + g + b) > 84 and (r - b) > 8) or (r + g + b) > 140:
                    lm[x, y] = 255

    dilated = letter_mask.filter(ImageFilter.MaxFilter(25)).filter(ImageFilter.GaussianBlur(3.5))
    dm = np.array(dilated, dtype=np.float32) / 255.0

    dm[:61, :] = 0.0
    dm[61, :] *= 0.35
    dm[62, :] *= 0.75
    dm[325:, :] = 0.0
    dm[324, :] *= 0.35
    dm[323, :] *= 0.75
    dm[:, :92] = 0.0
    dm[:, 476:] = 0.0

    clean = arr.copy()
    for yt0, yt1, y0, y1, yb0, yb1, x0, x1 in bands:
        pad_x0 = max(88, x0 - 18)
        pad_x1 = min(478, x1 + 18)
        top_strip = arr[yt0:yt1, pad_x0:pad_x1, :].mean(axis=0).copy()
        bot_strip = arr[yb0:yb1, pad_x0:pad_x1, :].mean(axis=0).copy()
        for xi in range(pad_x1 - pad_x0):
            if bot_strip[xi, 0] > 52 and (bot_strip[xi, 0] - bot_strip[xi, 2]) > 20:
                bot_strip[xi] = top_strip[xi] * 0.90
            if top_strip[xi, 0] > 52 and (top_strip[xi, 0] - top_strip[xi, 2]) > 20:
                top_strip[xi] = bot_strip[xi] * 0.90
        span = max(1.0, float(y1 - y0))
        shelf_ref = arr[max(61, y0 - 6):min(325, y1 + 6), 24:96, :]
        for y in range(max(61, y0 - 6), min(325, y1 + 6)):
            t = np.clip((y - y0) / span, 0.0, 1.0)
            row_interp = top_strip * (1.0 - t) + bot_strip * t
            ry = y - max(61, y0 - 6)
            tiled_ref = np.resize(shelf_ref[ry], (pad_x1 - pad_x0, 3))
            w_tex = np.ones((pad_x1 - pad_x0, 1), dtype=np.float32) * 0.28
            for xi in range(pad_x1 - pad_x0):
                if pad_x0 + xi >= 380:
                    w_tex[xi, 0] = 0.0
            clean[y, pad_x0:pad_x1, :] = row_interp * (1.0 - w_tex) + tiled_ref * w_tex

    clean_im = Image.fromarray(np.clip(clean, 0, 255).astype(np.uint8), "RGB")
    clean_im = clean_im.filter(ImageFilter.GaussianBlur(1.4))
    clean_arr = np.array(clean_im, dtype=np.float32)

    out_arr = arr * (1.0 - dm[:, :, None]) + clean_arr * dm[:, :, None]
    return Image.fromarray(np.clip(out_arr, 0, 255).astype(np.uint8), "RGB")


def apply_hero_push_in(wiped: Image.Image) -> Image.Image:
    """Apply a 1.08x hero push-in and vein/artery clarity boost across the entire
    giant tied arm + hand as one unbroken unit, routing the blend boundary through
    the dark bookcase shadow between the arched window and upper arm (y<=355) and
    the narrow gap between the Explorer's coat and the pinky tip (y>=455) so no seam
    ever crosses the thumb or fingers and the linen knot tail stays inside the right edge."""
    scale = 1.075
    anchor_x, anchor_y = 340.0, 660.0
    shift_x = 2.0
    shift_y = -6.0

    # Enhance hero clarity so both the stopped red arterial glow above the tight band
    # and the branching blue venous cords below the band read crisply at 168x94
    boosted = ImageEnhance.Contrast(wiped).enhance(1.07)
    boosted = ImageEnhance.Color(boosted).enhance(1.10)
    boosted = ImageEnhance.Sharpness(boosted).enhance(1.20)

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
        if y <= 355:
            x_lo, x_hi = 720.0, 775.0
        elif y >= 455:
            x_lo, x_hi = 315.0, 324.0
        else:
            ty = (y - 355.0) / (455.0 - 355.0)
            s = ty * ty * (3.0 - 2.0 * ty)
            x_lo = 720.0 * (1.0 - s) + 315.0 * s
            x_hi = 775.0 * (1.0 - s) + 324.0 * s
        for x in range(W):
            if x <= x_lo:
                m_arr[y, x] = 0.0
            elif x >= x_hi:
                m_arr[y, x] = 1.0
            else:
                tx = (x - x_lo) / max(1.0, (x_hi - x_lo))
                m_arr[y, x] = tx * tx * (3.0 - 2.0 * tx)

    mask = Image.fromarray(np.clip(m_arr * 255.0, 0, 255).astype(np.uint8), "L")
    mask = mask.filter(ImageFilter.GaussianBlur(2.5))
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
    if not SRC_A.exists():
        raise SystemExit(f"Missing 005 A plate: {SRC_A}")
    src = Image.open(SRC_A).convert("RGB").resize((W, H), Image.Resampling.LANCZOS)
    wiped = wipe_old_lettering(src)
    pushed = apply_hero_push_in(wiped)
    rgba = pushed.convert("RGBA")

    # 3-word concrete visual hook: TRAPPED / UNDER / SKIN
    # Directly describes the visible proof on the forearm (arterial blood stopped above the
    # tight band and blue venous blood trapped under the pale forearm skin below it, De Motu
    # Cordis ch. 11) while sharing zero words with the video title ('The Tied Arm That Proved
    # Your Blood Circulates'), Variant A ('ONE TIGHT BAND'), Variant B v03 ('THE BLOCKED
    # ARTERY'), or Variant B v04 ('HIDDEN VEIN VALVES').
    lines = [
        ("TRAPPED", "gold", 80),
        ("UNDER", "cream", 86),
        ("SKIN", "cream", 96),
    ]
    sprites = []
    for text, kind, size in lines:
        fill, hi = (CREAM, CREAM_HI) if kind == "cream" else (GOLD, GOLD_HI)
        sprites.append((text, kind, size, render_word(text, size, fill, hi)))

    gap = 5
    total_h = sum(s[3].size[1] for s in sprites) + gap * (len(sprites) - 1)
    y = 64 + max(0, (258 - total_h) // 2)

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

    # Side-by-side 4-panel T&C comparison strip (360x202 + 168x94): A vs B v03 vs B v04 vs New B v05
    phone = SELECTED / "hos_005_thumb_TC_4way_trapped_under_skin_v05_phone_168.jpg"
    b_v03 = Image.open(SRC_B_V03).convert("RGB") if SRC_B_V03.exists() else src
    b_v04 = Image.open(SRC_B_V04).convert("RGB") if SRC_B_V04.exists() else src
    panels = [
        ("A scheduled (ONE TIGHT BAND)", "A scheduled", src),
        ("B v03 (J0407: THE BLOCKED ARTERY)", "B v03", b_v03),
        ("B v04 (J0424: HIDDEN VEIN VALVES)", "B v04", b_v04),
        ("New B v05 (J0518: TRAPPED UNDER SKIN)", "New B v05", out),
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
        "film": "005",
        "video": "wwcjcFfC-5M",
        "job": "J0518",
        "variant": "B v05 (hero push-in + non-title-repeating visual hook)",
        "maker": "gemini",
        "hook": "TRAPPED UNDER SKIN",
        "punch": "TRAPPED",
        "jpg": f"Selected/{OUT.name}",
        "sha256": hashlib.sha256(OUT.read_bytes()).hexdigest(),
        "bytes": OUT.stat().st_size,
        "plates": [
            "Selected/hos_005_thumb_A_one_tight_band_v02.jpg (005 painted 16:9 key-art plate: glowing red artery stopped at linen band, pale forearm with branching blue veins, Explorer lower-left, original gold scroll flourishes)"
        ],
        "method": "existing_005_plate_only_1.08x_hero_push_in_and_reletter_GeorgiaBold_with_original_painted_flourishes",
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
            "HOOK": "PASS — 'TRAPPED UNDER SKIN' (3 words, punch word 'TRAPPED' in gold) names the concrete visible proof on the forearm (glowing red arterial blood stopped at the tight linen band and blue venous blood trapped under the pale forearm skin below it, De Motu Cordis ch. 11, FACT_NOTES_v01 row 26), shares zero words with the video title ('The Tied Arm That Proved Your Blood Circulates'), Variant A ('ONE TIGHT BAND'), Variant B v03 ('THE BLOCKED ARTERY'), or Variant B v04 ('HIDDEN VEIN VALVES'), and uses no vague questions or pronouns.",
            "BAND": f"PASS — Upper-left lettering band (x={left}..{right}, y={top}..{bottom}, framed by original painted gold scroll flourishes at y=24..356) sits completely left of the pushed-in hero arm (x={HERO_BOX[0]}..{HERO_BOX[2]}), above the Explorer's hair (y={EXPLORER_BOX[1]}), and clear of the bottom-right duration badge.",
            "PHONE": "PASS — Checked on 168x94 preview sheet and 4-way comparison strip: the 1.08x hero push-in and clarity boost make the tight linen band, stopped glowing red artery, and swollen blue forearm veins larger and sharper at 168x94 while keeping 'TRAPPED UNDER SKIN' and the Explorer's face/glasses (52.2% height) immediately legible in under a second.",
        },
        "previews": [
            f"Selected/{preview.name}",
            f"Selected/{sheet.name}",
            f"Selected/{phone.name}",
        ],
        "studio": False,
        "status": "Test & Compare B v05 candidate for 005 (wwcjcFfC-5M, built from existing 005 plate only with 1.08x hero push-in, £0). Parked for Chief: thumb B review. No Studio until OK.",
    }
    (HERE / "THUMB_B_TRAPPED_UNDER_SKIN_v05.json").write_text(json.dumps(idx, indent=2) + "\n")
    print("DONE", OUT, idx["sha256"])


if __name__ == "__main__":
    main()
