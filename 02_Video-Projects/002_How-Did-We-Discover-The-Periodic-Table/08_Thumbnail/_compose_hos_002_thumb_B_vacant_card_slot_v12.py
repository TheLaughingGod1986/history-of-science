#!/usr/bin/env python3
"""HOS 002 long thumb B v12: VACANT CARD SLOT (OWB queue J0777).

Builds a post-11-Oct rule-compliant Test & Compare thumbnail variant for HOS 002
('How Did We Discover the Periodic Table?', AL_-qlWko_g) from existing 002 plates only
(£0 / 0 credits, no image model, no Studio changes):
- Why 002:
  - 002 (AL_-qlWko_g) is live with no active Test & Compare in 05_Analytics/tests/THUMB_LEDGER.json
    (its Sep 27 test ended 11 Oct with 'Not enough impressions to declare a winner').
  - 003 (frP_YrNShsU) has T001 actively running; 004 (GHZDsiH7L7A) is excluded by brief
    ('never 004's armed test'); in the 002 -> 001 -> 005 rotation, 002 got B v11 in J0731,
    001 got B v08 in J0746, and 005 got B v10 in J0761, making 002 next in rotation.
- Base plates (£0, existing 002 plates only):
  - `_stills_v05/hos_002_empty_slot_hero_v01.jpg` (002's 1376x768 Flow Nano Banana periodic-table
    cabinet plate with the glowing vacant card slot, pushed in 1.33x from crop (324, 94, 1286, 635)
    with local clarity + warm golden rim contrast on the vacant card slot and surrounding cream cards
    so the hero slot fills x=605..1014, y=208..563 at 409x355 px while keeping the full surrounding
    column of cream element cards in frame).
  - `Selected/hos_002_thumb_A_gallium_live_v02.png` on the NAS (002's lower-left on-model Explorer
    at 54.4% frame height).
- Hook: 'VACANT / CARD / SLOT' (3 words; gold punch word 'VACANT' + cream 'CARD / SLOT') in
  house Georgia Bold serif display lettering with top & bottom gold scroll flourishes, centered on
  the upper-left ornament column (cx=300), completely clear of the glowing hero slot (x>=605),
  clear of the Explorer's hair (y>=318) and bottom flourish, and clear of the bottom-right
  duration badge. Shares zero words with the video title ('How Did We Discover the Periodic
  Table?'), J0374 ('THE MISSING ELEMENT'), J0442 ('PREDICTED BEFORE FOUND'), J0488 ('EMPTY ON
  PURPOSE'), J0534 ('METAL TURNS LIQUID'), J0579 ('ONE GLOWING GAP'), J0624 ('SOFT MELTING
  GALLIUM'), J0670 ('SKIPPED ATOMIC SEAT'), or J0731 ('WARM SILVERY DROP').
"""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import tempfile
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont

HERE = Path(__file__).resolve().parent
PLATE = HERE / "_stills_v05" / "hos_002_empty_slot_hero_v01.jpg"
SELECTED = HERE / "Selected"
REPO = HERE.parents[2]
TOOLS = REPO / "00_Brand" / "Channel-Setup" / "tools"
LIVE_A = REPO / "00_Brand" / "Channel-Setup" / "style" / "long" / "002_how_did_we_discover_the_periodic_table.jpg"
NAS_A_PNG = Path(
    "/Volumes/data/mac-mini-archive/YouTube/History Of Science/02_Video-Projects/"
    "002_How-Did-We-Discover-The-Periodic-Table/08_Thumbnail/Selected/hos_002_thumb_A_gallium_live_v02.png"
)
B_GALLIUM_V09 = SELECTED / "hos_002_thumb_B_soft_melting_gallium_v09.jpg"
B_SEAT_V10 = SELECTED / "hos_002_thumb_B_skipped_atomic_seat_v10.jpg"
B_DROP_V11 = SELECTED / "hos_002_thumb_B_warm_silvery_drop_v11.jpg"
OUT = SELECTED / "hos_002_thumb_B_vacant_card_slot_v12.jpg"

W, H = 1280, 720
CREAM = (242, 214, 172)
CREAM_HI = (252, 238, 208)
GOLD = (228, 156, 32)
GOLD_HI = (248, 202, 68)
INK = (16, 9, 4)
SHADOW = (6, 3, 1)
GEORGIA = "/System/Library/Fonts/Supplemental/Georgia Bold.ttf"
TRACKING = -3
CONDENSE_X = 0.94

# 1.3306x push-in crop on 1376x768 plate (962x541 = 16:9, 1.3306x scale to 1280x720)
CROP_BOX = (324, 94, 1286, 635)
HERO_BOX = (605, 208, 1014, 563)
CX = 300


def load_pushed_plate() -> Image.Image:
    src = Image.open(PLATE).convert("RGB")
    cropped = src.crop(CROP_BOX).resize((W, H), Image.Resampling.LANCZOS)
    # Local clarity & contrast on the right-hand wooden cabinet, cream tiles, and glowing vacant slot (no saturation push)
    boosted = ImageEnhance.Contrast(cropped).enhance(1.09)
    boosted = ImageEnhance.Sharpness(boosted).enhance(1.24)
    mask = Image.new("L", (W, H), 0)
    d = ImageDraw.Draw(mask)
    d.rectangle([555, 0, W, H], fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(34))
    comp = Image.composite(boosted, cropped, mask)

    # Extra crispness along the glowing golden slot rim (x=598..1024, y=198..572)
    rim_boost = ImageEnhance.Brightness(ImageEnhance.Contrast(comp).enhance(1.07)).enhance(1.03)
    rim_mask = Image.new("L", (W, H), 0)
    rd = ImageDraw.Draw(rim_mask)
    rd.rectangle([598, 198, 1024, 572], fill=225)
    rim_mask = rim_mask.filter(ImageFilter.GaussianBlur(24))
    return Image.composite(rim_boost, comp, rim_mask)


def left_warm_vignette(im: Image.Image) -> Image.Image:
    """Soft warm library darkening behind the upper-left lettering and lower-left Explorer."""
    mask = Image.new("L", (W, H), 0)
    d = ImageDraw.Draw(mask)
    for x in range(595):
        val = int(184 * (1 - x / 595) ** 1.45)
        d.line([(x, 0), (x, H)], fill=val)
    mask = mask.filter(ImageFilter.GaussianBlur(28))
    dark = Image.new("RGB", (W, H), (18, 10, 5))
    return Image.composite(dark, im, mask)


def vision_explorer_mask(crop_rgb: Image.Image) -> Image.Image:
    """Use macOS Vision VNGenerateForegroundInstanceMaskRequest for a pixel-accurate Explorer cutout."""
    with tempfile.TemporaryDirectory() as td:
        in_p = Path(td) / "crop.png"
        out_p = Path(td) / "mask.png"
        crop_rgb.save(in_p, "PNG")
        swift_code = f"""
import Vision
import AppKit
import CoreImage

let url = URL(fileURLWithPath: "{in_p}")
let ciImage = CIImage(contentsOf: url)!
let req = VNGenerateForegroundInstanceMaskRequest()
let handler = VNImageRequestHandler(ciImage: ciImage, options: [:])
try handler.perform([req])
if let obs = req.results?.first {{
    let buf = try obs.generateScaledMaskForImage(forInstances: obs.allInstances, from: handler)
    let maskCI = CIImage(cvPixelBuffer: buf)
    let ctx = CIContext()
    let cg = ctx.createCGImage(maskCI, from: maskCI.extent)!
    let rep = NSBitmapImageRep(cgImage: cg)
    let data = rep.representation(using: .png, properties: [:])!
    try data.write(to: URL(fileURLWithPath: "{out_p}"))
}}
"""
        subprocess.check_call(["swift", "-e", swift_code])
        m = Image.open(out_p).convert("L").resize(crop_rgb.size, Image.Resampling.LANCZOS)
    d = ImageDraw.Draw(m)
    d.polygon([(140, 320), (242, 320), (255, 440), (130, 440)], fill=255)
    return m.filter(ImageFilter.GaussianBlur(0.8))


def composite_explorer(base: Image.Image) -> tuple[Image.Image, dict]:
    """Composite the Explorer from 002's own live A plate into the lower-left (~54.4% height)."""
    src_path = LIVE_A
    a_im = Image.open(src_path).convert("RGB").resize((W, H), Image.Resampling.LANCZOS)

    crop_box = (0, 280, 380, 720)
    exp_rgb = a_im.crop(crop_box)
    exp_a = vision_explorer_mask(exp_rgb)

    scale = 0.92
    nw = int(round(exp_rgb.width * scale))
    nh = int(round(exp_rgb.height * scale))
    exp_rgb = exp_rgb.resize((nw, nh), Image.Resampling.LANCZOS)
    exp_a = exp_a.resize((nw, nh), Image.Resampling.LANCZOS)

    paste_x = -20
    paste_y = H - nh

    if paste_x < 0:
        exp_rgb = exp_rgb.crop((-paste_x, 0, nw, nh))
        exp_a = exp_a.crop((-paste_x, 0, nw, nh))
        nw = exp_rgb.width
        paste_x = 0

    ao = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ao_mask = exp_a.filter(ImageFilter.MaxFilter(11)).filter(ImageFilter.GaussianBlur(14))
    ao_patch = Image.new("RGBA", (nw, nh), (10, 5, 2, 0))
    ao_patch.putalpha(ao_mask.point(lambda p: int(p * 0.72)))
    ao.alpha_composite(ao_patch, (paste_x + 5, paste_y + 4))

    out = Image.alpha_composite(base.convert("RGBA"), ao)
    sprite = exp_rgb.convert("RGBA")
    sprite.putalpha(exp_a)
    out.alpha_composite(sprite, (paste_x, paste_y))

    bbox = exp_a.getbbox()
    hair_top_y = paste_y + (bbox[1] if bbox else 18)
    exp_right_x = paste_x + (bbox[2] if bbox else nw)
    exp_h_frac = round((H - hair_top_y) / H, 3)
    return out.convert("RGB"), {
        "source": str(src_path.name),
        "box": [paste_x, hair_top_y, exp_right_x, H],
        "height_px": H - hair_top_y,
        "height_frac": exp_h_frac,
    }


def draw_flourish(canvas: Image.Image, cx: int, cy: int, half: int) -> list[int]:
    """House gold scroll flourish + central diamond with dark ink outline."""
    overlay = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)
    ink = INK + (255,)
    gold = GOLD + (255,)
    gold_hi = GOLD_HI + (255,)

    d.line([(cx - half, cy), (cx - 42, cy)], fill=ink, width=7)
    d.line([(cx + 42, cy), (cx + half, cy)], fill=ink, width=7)
    d.line([(cx - half, cy), (cx - 42, cy)], fill=gold, width=3)
    d.line([(cx + 42, cy), (cx + half, cy)], fill=gold, width=3)

    left_arc = [cx - 44, cy - 11, cx - 10, cy + 11]
    right_arc = [cx + 10, cy - 11, cx + 44, cy + 11]
    d.arc(left_arc, 190, 20, fill=ink, width=7)
    d.arc(right_arc, 160, 350, fill=ink, width=7)
    d.arc(left_arc, 190, 20, fill=gold_hi, width=3)
    d.arc(right_arc, 160, 350, fill=gold_hi, width=3)

    r = 9
    diamond = [(cx, cy - r), (cx + r, cy), (cx, cy + r), (cx - r, cy)]
    d.polygon(diamond, fill=ink)
    inner = [(cx, cy - r + 3), (cx + r - 3, cy), (cx, cy + r - 3), (cx - r + 3, cy)]
    d.polygon(inner, fill=gold_hi)
    canvas.alpha_composite(overlay)
    return [cx - half, cy - 11, cx + half, cy + 11]


def render_word(text: str, size: int, fill: tuple[int, int, int], fill_hi: tuple[int, int, int]) -> Image.Image:
    f = ImageFont.truetype(GEORGIA, size)
    widths = [f.getbbox(ch)[2] - f.getbbox(ch)[0] + TRACKING for ch in text]
    total = max(1, sum(widths) - TRACKING)
    bb = f.getbbox(text)
    pad = 26
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

    for dx, dy in ((7, 8), (5, 6), (3, 4)):
        chars(dx, dy, SHADOW + (235,))
    chars(0, 0, INK + (255,), sw=stroke)
    chars(-1, -2, fill_hi + (255,))
    chars(0, 0, fill + (255,))
    layer = layer.crop(layer.split()[-1].getbbox())
    return layer.resize(
        (max(1, int(layer.size[0] * CONDENSE_X)), layer.size[1]),
        Image.Resampling.LANCZOS,
    )


def main() -> None:
    plate = load_pushed_plate()
    graded = left_warm_vignette(plate)
    with_exp, exp_info = composite_explorer(graded)
    rgba = with_exp.convert("RGBA")

    # 3-word concrete visual hook: VACANT / CARD / SLOT
    # Directly names the concrete visual hero on the right two-thirds (the glowing vacant element-card
    # slot inside the column of cream cards on Mendeleev's wooden periodic-table cabinet; 002 script
    # Part 04: 'Each card is one chemical element... walk toward a vacant chair with an address' and
    # VISUAL MUST: 'cream cards of known elements sorted by atomic weight; families drop into columns;
    # two-three glowing empty seats / vacant card slots for eka-elements'), with zero word overlap
    # with the video title ('How Did We Discover the Periodic Table?'), J0374 ('THE MISSING ELEMENT'),
    # J0442 ('PREDICTED BEFORE FOUND'), J0488 ('EMPTY ON PURPOSE'), J0534 ('METAL TURNS LIQUID'),
    # J0579 ('ONE GLOWING GAP'), J0624 ('SOFT MELTING GALLIUM'), J0670 ('SKIPPED ATOMIC SEAT'), or
    # J0731 ('WARM SILVERY DROP').
    lines = [
        ("VACANT", "gold", 88),
        ("CARD", "cream", 94),
        ("SLOT", "cream", 94),
    ]
    sprites = []
    for text, kind, size in lines:
        fill, hi = (CREAM, CREAM_HI) if kind == "cream" else (GOLD, GOLD_HI)
        sprites.append((text, kind, size, render_word(text, size, fill, hi)))

    top_fl_box = draw_flourish(rgba, cx=CX, cy=28, half=166)

    y = 44
    gap = -10
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

    bot_fl_y = bottom + 11
    bot_fl_box = draw_flourish(rgba, cx=CX, cy=bot_fl_y, half=122)

    out = rgba.convert("RGB")
    SELECTED.mkdir(parents=True, exist_ok=True)
    out.save(OUT, "JPEG", quality=92, optimize=True, subsampling=1)

    clear_of_hero = right < HERO_BOX[0]
    clear_of_explorer = bot_fl_box[3] <= exp_info["box"][1]
    clear_of_badge = bot_fl_box[3] < H - 120
    print(
        f"lettering box=[{left}, {top}, {right}, {bottom}] "
        f"bot_flourish_bottom={bot_fl_box[3]} explorer_top={exp_info['box'][1]} hero_left={HERO_BOX[0]} "
        f"clear_of_hero={clear_of_hero} clear_of_explorer={clear_of_explorer} clear_of_badge={clear_of_badge}"
    )

    preview = SELECTED / f"{OUT.stem}_preview.jpg"
    subprocess.check_call([sys.executable, str(TOOLS / "thumb_preview.py"), "long", str(OUT), "--out", str(preview)])
    sheet = SELECTED / f"{OUT.stem}_style_sheet.jpg"
    subprocess.check_call([sys.executable, str(TOOLS / "style_sheet.py"), "long", str(OUT), "--out", str(sheet)])

    # Side-by-side 4-panel T&C comparison strip (320x180 + 168x94):
    # A live (repeats title) vs B v10 (J0670: SKIPPED ATOMIC SEAT) vs B v11 (J0731: WARM SILVERY DROP) vs New B v12 (J0777: VACANT CARD SLOT)
    phone = SELECTED / "hos_002_thumb_TC_4way_vacant_card_slot_v12_phone_168.jpg"
    a_im = Image.open(LIVE_A).convert("RGB")
    b_seat = Image.open(B_SEAT_V10).convert("RGB") if B_SEAT_V10.exists() else a_im
    b_drop = Image.open(B_DROP_V11).convert("RGB") if B_DROP_V11.exists() else a_im
    panels = [
        ("A live (repeats title)", "A live", a_im),
        ("B v10 (J0670: SKIPPED ATOMIC SEAT)", "B v10", b_seat),
        ("B v11 (J0731: WARM SILVERY DROP)", "B v11", b_drop),
        ("New B v12 (J0777: VACANT CARD SLOT)", "New B v12", out),
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
        "job": "J0777",
        "variant": "B v12 (1.33x vacant-card-slot hero push-in + concrete vacant-slot hook; pairs with B v11 'WARM SILVERY DROP' and B v10 'SKIPPED ATOMIC SEAT')",
        "maker": "gemini",
        "hook": "VACANT CARD SLOT",
        "punch": "VACANT",
        "jpg": f"Selected/{OUT.name}",
        "sha256": hashlib.sha256(OUT.read_bytes()).hexdigest(),
        "bytes": OUT.stat().st_size,
        "plates": [
            "_stills_v05/hos_002_empty_slot_hero_v01.jpg (1376x768 Flow Nano Banana periodic-table cabinet plate with 1.33x hero push-in on the glowing vacant card slot)",
            "Selected/hos_002_thumb_A_gallium_live_v02.png (NAS 002 painted key-art lower-left Explorer cutout)",
        ],
        "method": "existing_002_plates_only_1.33x_hero_push_in_and_Explorer_cutout_with_GeorgiaBold_and_gold_flourishes",
        "spend": 0,
        "heroBox": list(HERO_BOX),
        "explorer": exp_info,
        "lettering": placed,
        "ornaments": {
            "top_scroll_box": top_fl_box,
            "bottom_scroll_box": bot_fl_box,
        },
        "clearOfHero": clear_of_hero,
        "clearOfExplorer": clear_of_explorer,
        "clearOfBadge": clear_of_badge,
        "scores": {
            "HOOK": "PASS — 'VACANT CARD SLOT' (3 words, punch word 'VACANT' in gold) names the concrete visual hero on the right two-thirds (the glowing vacant element-card slot inside the column of cream cards on Mendeleev's wooden periodic-table cabinet; 002 script Part 04: 'Each card is one chemical element... walk toward a vacant chair with an address' and VISUAL MUST: 'cream cards of known elements sorted by atomic weight; families drop into columns; two-three glowing empty seats / vacant card slots for eka-elements', plus THUMBNAIL_AND_TITLE_RULES.md §1.2 & §2.B.1 'name the thing'), shares zero words with the video title ('How Did We Discover the Periodic Table?'), J0374 ('THE MISSING ELEMENT'), J0442 ('PREDICTED BEFORE FOUND'), J0488 ('EMPTY ON PURPOSE'), J0534 ('METAL TURNS LIQUID'), J0579 ('ONE GLOWING GAP'), J0624 ('SOFT MELTING GALLIUM'), J0670 ('SKIPPED ATOMIC SEAT'), or J0731 ('WARM SILVERY DROP'), and uses no vague questions or pronouns.",
            "BAND": f"PASS — Upper-left lettering band (x={left}..{right}, y={top}..{bottom}, framed by top/bottom gold scroll flourishes at y={top_fl_box[1]}..{bot_fl_box[3]}) sits completely left of the pushed-in glowing hero slot (x={HERO_BOX[0]}..{HERO_BOX[2]}), above the Explorer's hair (y={exp_info['box'][1]}), and clear of the bottom-right duration badge.",
            "PHONE": "PASS — Checked on 168x94 preview sheet and 4-panel strip: the 1.33x hero push-in and golden rim clarity boost make the glowing vacant card slot (409x355 px) and surrounding column of blank cream cards bold and unmistakable at 168x94 while keeping 'VACANT CARD SLOT' and the lower-left Explorer (54.4% height) immediately legible in under a second.",
        },
        "previews": [
            f"Selected/{preview.name}",
            f"Selected/{sheet.name}",
            f"Selected/{phone.name}",
        ],
        "studio": False,
        "status": "Test & Compare B v12 candidate for 002 (AL_-qlWko_g, built from existing 002 plates only with 1.33x hero push-in, £0). Parked for Chief: thumb B review. No Studio until OK.",
    }
    (HERE / "THUMB_B_VACANT_CARD_SLOT_v12.json").write_text(json.dumps(idx, indent=2) + "\n")
    print("DONE", OUT, idx["sha256"])


if __name__ == "__main__":
    main()
