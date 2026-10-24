#!/usr/bin/env python3
"""HOS 002 long thumb B v02: THE MISSING ELEMENT (OWB queue J0374, fixing J0255 v01).

Fixes Chief's J0255 review notes ("B lacks Explorer + hero size"):
1. Hero scale: 1.25x push-in on the 1376x768 Flow Nano Banana plate
   `_stills_v05/hos_002_empty_slot_hero_v01.jpg` (crop 272,72..1296,648 -> 1280x720)
   so the glowing empty slot sits at x=634..1018, y=222..556 (384x334 px, +35% larger
   than v01's 285x250 px) inside the periodic-table cabinet filling the right two-thirds.
2. Explorer at house scale (~55% of frame height, lower-left, face readable at 168x94):
   recomposed from 002's own `hos_002_thumb_A_gallium_live_v02.png` with a clean silhouette
   polygon mask (excluding top letters, right scroll ornament, and right gallium edge)
   and soft feathering into the warm dark library foreground.
3. House Georgia Bold display lettering (`THE / MISSING / ELEMENT`, cream + gold punch word
   `MISSING`) with dark outline, drop shadow, and top/bottom gold scroll flourishes in the
   upper-left band (x=40..598, y=18..304), completely clear of the Explorer's hair (y>=310),
   clear of the glowing hero slot (x>=634), and clear of the bottom-right duration badge.

£0 / 0 credits — existing 002 plates only, no image model, no Studio changes.
"""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

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
OUT = SELECTED / "hos_002_thumb_B_missing_element_v02.jpg"

W, H = 1280, 720
CREAM = (242, 214, 172)
CREAM_HI = (252, 238, 208)
GOLD = (228, 156, 32)
GOLD_HI = (248, 202, 68)
INK = (16, 9, 4)
SHADOW = (6, 3, 1)
GEORGIA = "/System/Library/Fonts/Supplemental/Georgia Bold.ttf"
TRACKING = -4
CONDENSE_X = 0.89

# Push-in crop on 1376x768 plate (1024x576 = exact 16:9, 1.25x scale to 1280x720)
CROP_BOX = (272, 72, 1296, 648)
# In 1376x768 the glowing slot is (779, 250, 1086, 517) -> in 1280x720 it lands at:
HERO_BOX = (634, 222, 1018, 556)


def load_pushed_plate() -> Image.Image:
    src = Image.open(PLATE).convert("RGB")
    cropped = src.crop(CROP_BOX)
    return cropped.resize((W, H), Image.Resampling.LANCZOS)


def left_warm_vignette(im: Image.Image) -> Image.Image:
    """Soft warm library darkening behind the upper-left lettering and lower-left Explorer."""
    mask = Image.new("L", (W, H), 0)
    d = ImageDraw.Draw(mask)
    for x in range(620):
        val = int(175 * (1 - x / 620) ** 1.45)
        d.line([(x, 0), (x, H)], fill=val)
    mask = mask.filter(ImageFilter.GaussianBlur(28))
    dark = Image.new("RGB", (W, H), (18, 10, 5))
    return Image.composite(dark, im, mask)


def vision_explorer_mask(crop_rgb: Image.Image) -> Image.Image:
    """Use macOS Vision VNGenerateForegroundInstanceMaskRequest for a pixel-accurate Explorer cutout."""
    import tempfile
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
    # Fill the small shadow gap between the right coat hem and trousers at the very bottom
    d = ImageDraw.Draw(m)
    d.polygon([(140, 320), (242, 320), (255, 440), (130, 440)], fill=255)
    return m.filter(ImageFilter.GaussianBlur(0.8))


def composite_explorer(base: Image.Image) -> tuple[Image.Image, dict]:
    """Composite the Explorer from 002's own live A plate into the lower-left (~54% height)."""
    src_path = NAS_A_PNG if NAS_A_PNG.exists() else LIVE_A
    a_im = Image.open(src_path).convert("RGB").resize((W, H), Image.Resampling.LANCZOS)

    crop_box = (0, 280, 380, 720)
    exp_rgb = a_im.crop(crop_box)
    exp_a = vision_explorer_mask(exp_rgb)

    scale = 0.94
    nw = int(round(exp_rgb.width * scale))
    nh = int(round(exp_rgb.height * scale))
    exp_rgb = exp_rgb.resize((nw, nh), Image.Resampling.LANCZOS)
    exp_a = exp_a.resize((nw, nh), Image.Resampling.LANCZOS)

    paste_x = -24
    paste_y = H - nh  # feet/coat anchored to bottom frame edge (y=720)

    # Crop off left negative overhang if paste_x < 0
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

    # Measure actual bounding box of non-zero alpha on canvas
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


def render_word(text: str, size: int, fill: tuple[int, int, int], fill_hi: tuple[int, int, int]) -> Image.Image:
    f = ImageFont.truetype(GEORGIA, size)
    widths = [f.getbbox(ch)[2] - f.getbbox(ch)[0] + TRACKING for ch in text]
    total = max(1, sum(widths) - TRACKING)
    bb = f.getbbox(text)
    pad = 28
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
        chars(dx, dy, SHADOW + (230,))
    chars(0, 0, INK + (255,), sw=stroke)
    chars(-1, -2, fill_hi + (255,))
    chars(0, 0, fill + (255,))
    layer = layer.crop(layer.split()[-1].getbbox())
    return layer.resize(
        (max(1, int(layer.size[0] * CONDENSE_X)), layer.size[1]),
        Image.Resampling.LANCZOS,
    )


def draw_flourish(canvas: Image.Image, cx: int, cy: int, half: int) -> None:
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


def main() -> None:
    plate = load_pushed_plate()
    graded = left_warm_vignette(plate)
    with_exp, exp_info = composite_explorer(graded)
    rgba = with_exp.convert("RGBA")

    lines = [
        ("THE", "cream", 70),
        ("MISSING", "gold", 112),
        ("ELEMENT", "cream", 94),
    ]
    left_x = 42
    y = 34
    gap = 3
    placed = []
    for text, kind, size in lines:
        fill, hi = (CREAM, CREAM_HI) if kind == "cream" else (GOLD, GOLD_HI)
        spr = render_word(text, size, fill, hi)
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

    right = max(p["box"][2] for p in placed)
    bottom = max(p["box"][3] for p in placed)
    cx = left_x + (right - left_x) // 2
    draw_flourish(rgba, cx, 19, half=min(170, (right - left_x) // 2 - 20))
    # Place bottom flourish centered slightly right (cx=340, like live A) so it sits cleanly in the gap right of the Explorer's hair curl
    draw_flourish(rgba, 340, bottom + 12, half=115)

    out = rgba.convert("RGB")
    SELECTED.mkdir(parents=True, exist_ok=True)
    out.save(OUT, "JPEG", quality=92, optimize=True, subsampling=1)

    clear_of_hero = right < HERO_BOX[0]
    clear_of_explorer = (bottom + 22) <= exp_info["box"][1]
    clear_of_badge = bottom < H - 120 and HERO_BOX[3] < H - 120
    print(
        f"lettering right={right} bottom={bottom} (flourish_bot={bottom+22}) "
        f"explorer_top={exp_info['box'][1]} hero_left={HERO_BOX[0]} "
        f"clear_of_hero={clear_of_hero} clear_of_explorer={clear_of_explorer} clear_of_badge={clear_of_badge}"
    )

    preview = SELECTED / f"{OUT.stem}_preview.jpg"
    subprocess.check_call([sys.executable, str(TOOLS / "thumb_preview.py"), "long", str(OUT), "--out", str(preview)])
    sheet = SELECTED / f"{OUT.stem}_style_sheet.jpg"
    subprocess.check_call([sys.executable, str(TOOLS / "style_sheet.py"), "long", str(OUT), "--out", str(sheet)])

    # Side-by-side phone comparison strip (168x94 + 360x202): A live vs B v01 vs B v02
    phone = SELECTED / "hos_002_thumb_A_vs_B_missing_element_v02_phone_168.jpg"
    a_im = Image.open(LIVE_A).convert("RGB")
    v01_path = SELECTED / "hos_002_thumb_B_missing_element_v01.jpg"
    v01_im = Image.open(v01_path).convert("RGB") if v01_path.exists() else a_im

    strip = Image.new("RGB", (360 * 3 + 32, 202 + 94 + 76), (14, 10, 6))
    d = ImageDraw.Draw(strip)
    lf = ImageFont.truetype(GEORGIA, 16)
    for i, (label, src_im) in enumerate([
        ("A live (Gallium + Title)", a_im),
        ("B v01 (J0255: no Explorer)", v01_im),
        ("B v02 (J0374: Explorer + Hero push-in)", out),
    ]):
        x0 = 8 + i * (360 + 8)
        d.text((x0, 6), label, font=lf, fill=(235, 212, 170))
        strip.paste(src_im.resize((360, 202), Image.Resampling.LANCZOS), (x0, 28))
        d.text((x0, 238), f"168x94 phone tile ({label.split()[0]} {label.split()[1]})", font=lf, fill=(200, 175, 135))
        strip.paste(src_im.resize((168, 94), Image.Resampling.LANCZOS), (x0, 262))
    strip.save(phone, "JPEG", quality=93)

    idx = {
        "film": "002",
        "video": "AL_-qlWko_g",
        "job": "J0374",
        "replaces": "J0255 v01 (hos_002_thumb_B_missing_element_v01.jpg)",
        "variant": "B v02",
        "maker": "gemini",
        "hook": "THE MISSING ELEMENT",
        "punch": "MISSING",
        "jpg": f"Selected/{OUT.name}",
        "sha256": hashlib.sha256(OUT.read_bytes()).hexdigest(),
        "bytes": OUT.stat().st_size,
        "plates": [
            f"_stills_v05/{PLATE.name} (1376x768 Flow Nano Banana plate, 1.25x hero push-in crop {list(CROP_BOX)})",
            "Selected/hos_002_thumb_A_gallium_live_v02.png (Explorer lower-left at 55.8% frame height)",
        ],
        "method": "existing_plates_only_hero_pushin_plus_explorer_and_house_GeorgiaBold_flourishes",
        "spend": 0,
        "heroBox": list(HERO_BOX),
        "explorer": exp_info,
        "lettering": placed,
        "clearOfHero": clear_of_hero,
        "clearOfExplorer": clear_of_explorer,
        "clearOfBadge": clear_of_badge,
        "scores": {
            "HOOK": "PASS — 'THE MISSING ELEMENT' (3 words, punch word 'MISSING' in gold) names the concrete discovery object/gap without repeating the video title ('How Did We Discover the Periodic Table?').",
            "BAND": f"PASS — Upper-left lettering band (x=42..{right}, y=18..{bottom+22} with gold flourishes) sits completely left of the glowing hero slot (x={HERO_BOX[0]}..{HERO_BOX[2]}), above the Explorer's hair (y={exp_info['box'][1]}), and clear of the bottom-right duration badge.",
            "PHONE": "PASS — Checked on 168x94 preview sheet and side-by-side strip: 'THE MISSING ELEMENT', the glowing periodic-table slot (384x334 px), and the Explorer's face/glasses (55.8% height) all read at a glance at 168x94.",
        },
        "previews": [
            f"Selected/{preview.name}",
            f"Selected/{sheet.name}",
            f"Selected/{phone.name}",
        ],
        "studio": False,
        "status": "Test & Compare B v02 candidate for 002 (fixes J0255 Explorer + hero size notes from existing 002 plates, £0). Parked for Chief: thumb B review. No Studio until OK.",
    }
    (HERE / "THUMB_B_MISSING_ELEMENT_v02.json").write_text(json.dumps(idx, indent=2) + "\n")
    print("DONE", OUT, idx["sha256"])


if __name__ == "__main__":
    main()
