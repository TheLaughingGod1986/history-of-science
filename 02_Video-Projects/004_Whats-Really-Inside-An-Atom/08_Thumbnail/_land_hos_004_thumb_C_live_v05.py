#!/usr/bin/env python3
"""HOS 004 thumb C v05 ONLY — fix Te/I number overlays.

Ben: v04 C "52" read as 5² (Georgia oldstyle figures, uneven heights) and
numbers were small/jammed to the top edge. Redo both number overlays with
lining figures, bigger, top-left inside each tile with padding.

A and B v04 untouched. Art / Explorer / THE HIDDEN NUMBER type unchanged.
Nothing to Studio. No KEEP/LOCKED.
"""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
ASSETS = HERE / "_assets_v04"
SELECTED = HERE / "Selected"
PREVIEWS = HERE / "Previews"
DRAFTS = HERE / "Drafts"
WALK = Path(
    "/Users/benjaminoats/Library/Application Support/Cursor/AgentStores/"
    "cursor_agent_stores/bc-958ae0f3-be07-568f-a2ab-eb7f422d8839/files/artifacts"
)
ICLOUD = (
    Path.home()
    / "Library/Mobile Documents/com~apple~CloudDocs/HOS UAT"
    / "004_Whats-Really-Inside-An-Atom/08_Thumbnail/Selected"
)
LIVE_002 = (
    Path(__file__).resolve().parents[2]
    / "002_How-Did-We-Discover-The-Periodic-Table/08_Thumbnail/Selected"
    / "hos_002_thumb_A_gallium_live_v02.jpg"
)
PREVIEW_TOOL = (
    Path(__file__).resolve().parents[3]
    / "00_Brand/Channel-Setup/tools/thumb_preview.py"
)

W, H = 1280, 720
CREAM = (245, 232, 200)
GOLD = (232, 178, 48)
INK = (28, 18, 10)
SHADOW = (12, 8, 4)

# Serif for symbols (painted feel). Modern lining-figure font for Z —
# Georgia Bold oldstyle "2" sat higher/shorter and read as 5².
SYMBOL_FONT = "/System/Library/Fonts/Supplemental/Georgia Bold.ttf"
# Arial Black: clear lining figures, equal digit box heights.
NUMBER_FONT = "/System/Library/Fonts/Supplemental/Arial Black.ttf"
FALLBACK = "/System/Library/Fonts/Supplemental/Impact.ttf"

BLANK_C = "hos_004_thumb_C_hidden_number_live_v04.png"
STEM = "hos_004_thumb_C_hidden_number_live_v05"

# Cream/gold PANEL interiors (inside wood rims) — measured on blank plate
TE_FACE = (600, 175, 810, 490)
I_FACE = (960, 200, 1200, 505)
TE_Z, I_Z = 52, 53
PAD = 52  # clear padding from panel edges (stroke must stay inside)


def load_font(path: str, size: int) -> ImageFont.FreeTypeFont:
    for p in (path, FALLBACK):
        try:
            return ImageFont.truetype(p, size)
        except OSError:
            continue
    return ImageFont.load_default()


def paint_text(
    draw: ImageDraw.ImageDraw,
    text: str,
    *,
    x: int,
    y: int,
    size: int,
    fill: tuple[int, int, int],
    font_path: str,
) -> tuple[int, int, int, int]:
    f = load_font(font_path, size)
    stroke = max(4, size // 14)
    # Soft shadow below-right only (does not eat top padding)
    draw.text((x + 4, y + 5), text, font=f, fill=SHADOW, anchor="lt")
    draw.text(
        (x, y),
        text,
        font=f,
        fill=INK,
        stroke_width=stroke + 2,
        stroke_fill=INK,
        anchor="lt",
    )
    draw.text((x, y), text, font=f, fill=fill, stroke_width=stroke, stroke_fill=INK, anchor="lt")
    return draw.textbbox((x, y), text, font=f, stroke_width=stroke + 2, anchor="lt")


def paint_lining_number(
    draw: ImageDraw.ImageDraw,
    number: int,
    *,
    x: int,
    y: int,
    size: int,
    fill: tuple[int, int, int],
) -> tuple[int, int, int, int]:
    """Draw Z with lining figures, digit-by-digit on one baseline (no 5²)."""
    f = load_font(NUMBER_FONT, size)
    # Prove equal ink heights before paint
    heights = []
    for ch in str(number):
        b = f.getbbox(ch)
        heights.append(b[3] - b[1])
    if max(heights) - min(heights) > 2:
        raise SystemExit(f"uneven lining figures for {number}: {heights}")
    # Shared top using anchor lt — each digit same em box
    stroke = max(4, size // 14)
    cursor = x
    first_box = None
    last_box = None
    for ch in str(number):
        draw.text((cursor + 4, y + 5), ch, font=f, fill=SHADOW, anchor="lt")
        draw.text(
            (cursor, y),
            ch,
            font=f,
            fill=INK,
            stroke_width=stroke + 2,
            stroke_fill=INK,
            anchor="lt",
        )
        draw.text(
            (cursor, y),
            ch,
            font=f,
            fill=fill,
            stroke_width=stroke,
            stroke_fill=INK,
            anchor="lt",
        )
        box = draw.textbbox((cursor, y), ch, font=f, stroke_width=stroke + 2, anchor="lt")
        if first_box is None:
            first_box = box
        last_box = box
        cursor = box[2] + max(2, size // 40)
    assert first_box and last_box
    return (first_box[0], first_box[1], last_box[2], max(first_box[3], last_box[3]))


def overlay_tile_labels(im: Image.Image) -> Image.Image:
    """Te 52 / I 53 only. Lining figures, bigger, top-left with padding."""
    assert TE_Z == 52 and I_Z == 53
    draw = ImageDraw.Draw(im)
    specs = [
        ("Te", TE_Z, TE_FACE, CREAM, CREAM),
        ("I", I_Z, I_FACE, GOLD, GOLD),
    ]
    for symbol, number, box, scol, ncol in specs:
        x0, y0, x1, y1 = box
        tw, th = x1 - x0, y1 - y0
        # Numbers: top-left inside cream panel, padded — lining, clearly bigger
        n_size = max(88, th // 4)
        nx = x0 + PAD
        ny = y0 + PAD
        nbox = paint_lining_number(draw, number, x=nx, y=ny, size=n_size, fill=ncol)
        # Guard: number stroke must stay inside panel
        if nbox[1] < y0 + 8 or nbox[0] < x0 + 8:
            raise SystemExit(f"{symbol} number clipped into rim: {nbox} vs face {box}")
        # Symbol centred lower on face
        s_size = max(110, th // 3)
        sf = load_font(SYMBOL_FONT, s_size)
        sw = sf.getlength(symbol)
        sx = int(x0 + (tw - sw) / 2)
        sy = int(y0 + th * 0.40)
        paint_text(
            draw,
            symbol,
            x=sx,
            y=sy,
            size=s_size,
            fill=scol,
            font_path=SYMBOL_FONT,
        )
    return im


def save_jpg(im: Image.Image, dest: Path) -> Path:
    dest.parent.mkdir(parents=True, exist_ok=True)
    rgb = im.convert("RGB").resize((W, H), Image.Resampling.LANCZOS)
    q = 90
    rgb.save(dest, "JPEG", quality=q, optimize=True, subsampling=1)
    while dest.stat().st_size > 1_900_000 and q > 70:
        q -= 4
        rgb.save(dest, "JPEG", quality=q, optimize=True, subsampling=1)
    print(f"  {dest.name}  {dest.stat().st_size} B  q={q}", flush=True)
    return dest


def family_sheet() -> Path:
    refs = [
        (LIVE_002, "002 LIVE A"),
        (SELECTED / "hos_004_thumb_A_atom_live_v04.jpg", "004 A v04"),
        (SELECTED / "hos_004_thumb_B_cut_gold_live_v04.jpg", "004 B v04"),
        (SELECTED / f"{STEM}.jpg", "004 C v05"),
    ]
    tw, th = 420, 236
    gap = 16
    label_h = 36
    sheet_w = gap + len(refs) * (tw + gap)
    sheet_h = gap + label_h + th + gap
    sheet = Image.new("RGB", (sheet_w, sheet_h), (18, 14, 10))
    draw = ImageDraw.Draw(sheet)
    f = load_font(SYMBOL_FONT, 22)
    x = gap
    for path, lab in refs:
        if not path.exists():
            raise SystemExit(f"missing family tile {path}")
        tile = Image.open(path).convert("RGB").resize((tw, th), Image.Resampling.LANCZOS)
        draw.text((x, gap + 4), lab, font=f, fill=CREAM)
        sheet.paste(tile, (x, gap + label_h))
        x += tw + gap
    out = SELECTED / "hos_004_thumbs_v05_family_vs_002_live.jpg"
    out.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(out, "JPEG", quality=92, optimize=True)
    print(f"  FAMILY {out.name}  {out.stat().st_size} B  {sheet.size}", flush=True)
    return out


def write_index(c_jpg: Path) -> Path:
    a = SELECTED / "hos_004_thumb_A_atom_live_v04.jpg"
    b = SELECTED / "hos_004_thumb_B_cut_gold_live_v04.jpg"
    pairs = [
        {
            "slot": 1,
            "role": "main",
            "title": "What's Really Inside an Atom?",
            "thumbId": "A",
            "hook": "WHAT'S REALLY INSIDE AN ATOM?",
            "jpg": f"Selected/{a.name}",
            "preview": f"Selected/{a.stem}_preview.jpg",
            "sha256": hashlib.sha256(a.read_bytes()).hexdigest(),
            "bytes": a.stat().st_size,
            "version": "v04",
        },
        {
            "slot": 2,
            "role": "alt",
            "title": "Why Is the Periodic Table in This Order?",
            "thumbId": "C",
            "hook": "THE HIDDEN NUMBER",
            "jpg": f"Selected/{c_jpg.name}",
            "preview": f"Selected/{c_jpg.stem}_preview.jpg",
            "sha256": hashlib.sha256(c_jpg.read_bytes()).hexdigest(),
            "bytes": c_jpg.stat().st_size,
            "version": "v05",
            "note": "lining-figure Te 52 / I 53; bigger; top-left padded",
        },
        {
            "slot": 3,
            "role": "alt",
            "title": "How Small Can You Cut Gold?",
            "thumbId": "B",
            "hook": "CUT GOLD?",
            "jpg": f"Selected/{b.name}",
            "preview": f"Selected/{b.stem}_preview.jpg",
            "sha256": hashlib.sha256(b.read_bytes()).hexdigest(),
            "bytes": b.stat().st_size,
            "version": "v04",
        },
    ]
    idx = {
        "parentTitle": "What's Really Inside an Atom?",
        "version": "v05",
        "status": "STOP for Ben pick. Proposed only. Nothing to Studio. No KEEP/LOCKED.",
        "note": (
            "C v05 ONLY — lining-figure Te 52 / I 53 (fixed 5² read). "
            "A and B remain v04. Live Studio grammar."
        ),
        "composer": "_land_hos_004_thumb_C_live_v05.py",
        "factLock": {
            "Te": 52,
            "I": 53,
            "numberFont": "Arial Black (lining figures, digit-by-digit baseline)",
        },
        "testAndComparePairs": pairs,
        "upload": False,
        "studio": False,
        "icloud": "HOS UAT/004_Whats-Really-Inside-An-Atom/08_Thumbnail/Selected/",
        "familySheet": "Selected/hos_004_thumbs_v05_family_vs_002_live.jpg",
    }
    out = HERE / "THUMBS_INDEX_v05.json"
    out.write_text(json.dumps(idx, indent=2) + "\n")
    print(f"  INDEX {out.name}", flush=True)
    return out


def main() -> None:
    blank = ASSETS / BLANK_C
    if not blank.exists():
        raise SystemExit(f"missing blank C plate {blank}")
    # Prove lining figures are level before paint
    nf = load_font(NUMBER_FONT, 80)
    h5 = nf.getbbox("5")[3] - nf.getbbox("5")[1]
    h2 = nf.getbbox("2")[3] - nf.getbbox("2")[1]
    h3 = nf.getbbox("3")[3] - nf.getbbox("3")[1]
    if abs(h5 - h2) > 2 or abs(h5 - h3) > 2:
        raise SystemExit(f"number font still uneven: 5={h5} 2={h2} 3={h3}")
    print(f"LINING_OK Arial Black digit heights 5={h5} 2={h2} 3={h3}", flush=True)

    im = Image.open(blank).convert("RGB")
    im = overlay_tile_labels(im)
    SELECTED.mkdir(parents=True, exist_ok=True)
    DRAFTS.mkdir(parents=True, exist_ok=True)
    PREVIEWS.mkdir(parents=True, exist_ok=True)
    png = SELECTED / f"{STEM}.png"
    im.save(png, "PNG")
    jpg = save_jpg(im, SELECTED / f"{STEM}.jpg")
    (DRAFTS / jpg.name).write_bytes(jpg.read_bytes())

    preview = SELECTED / f"{STEM}_preview.jpg"
    subprocess.check_call(
        [sys.executable, str(PREVIEW_TOOL), "long", str(jpg), "--out", str(preview)]
    )
    (PREVIEWS / "hos_004_thumb_C_hidden_number_preview_v05.jpg").write_bytes(preview.read_bytes())

    family = family_sheet()
    write_index(jpg)

    WALK.mkdir(parents=True, exist_ok=True)
    for p in (jpg, preview, family):
        (WALK / p.name).write_bytes(p.read_bytes())

    ICLOUD.mkdir(parents=True, exist_ok=True)
    for p in (jpg, preview, family):
        (ICLOUD / p.name).write_bytes(p.read_bytes())
        print(f"  iCloud ← {p.name}", flush=True)

    print("DONE C v05 only · A/B v04 untouched · STOP for Ben · no Studio")


if __name__ == "__main__":
    main()
