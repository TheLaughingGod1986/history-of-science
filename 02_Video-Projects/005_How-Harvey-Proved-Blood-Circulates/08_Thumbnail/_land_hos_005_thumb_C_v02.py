#!/usr/bin/env python3
"""Land HOS 005 long Thumb C v02 — re-letter A painting (Claude PR #180 #5974014892).

£0, no image model. C v01 used thin Didot — WRONG. Match house face of A:
heavy condensed Georgia Bold, cream + gold punch, dark outline, A's gold flourishes.

  Words: TIE / IT / TIGHT  (TIGHT = gold punch, same cap height as BAND on A)
  Art: same tied-arm painting as A/B (Explorer lower left preserved)
  NOT uploaded to Studio Test & Compare until Claude KEEP.
"""
from __future__ import annotations

import hashlib
import json
import random
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
SELECTED = HERE / "Selected"
WORK = HERE / "_work_thumb_c_v02"
TOOLS = ROOT / "00_Brand/Channel-Setup/tools"
TOOLS_MAIN = Path.home() / "YouTube/History Of Science/00_Brand/Channel-Setup/tools"
MAIN_SELECTED = (
    Path.home()
    / "YouTube/History Of Science/02_Video-Projects"
    / "005_How-Harvey-Proved-Blood-Circulates/08_Thumbnail/Selected"
)
MAIN_THUMB = MAIN_SELECTED.parent

W, H = 1280, 720
PANEL = (40, 0, 540, 378)
FEATHER = 12

CREAM = (238, 200, 155)
CREAM_HI = (250, 232, 198)
GOLD = (224, 150, 28)
GOLD_HI = (245, 195, 60)
INK = (14, 8, 4)
SHADOW = (4, 2, 1)

GEORGIA = "/System/Library/Fonts/Supplemental/Georgia Bold.ttf"

# Match A line centres: ONE~94, TIGHT cream~168, BAND~245
LINES = [
    ("TIE", "cream", 80, 100),
    ("IT", "cream", 80, 172),
    ("TIGHT", "gold", 92, 252),
]
TRACKING = -5
CONDENSE_X = 0.88
CX = 290


def tools_dir() -> Path:
    if (TOOLS / "thumb_preview.py").exists():
        return TOOLS
    return TOOLS_MAIN


def src_a() -> Image.Image:
    for p in (
        SELECTED / "hos_005_thumb_A_one_tight_band_v02.jpg",
        MAIN_SELECTED / "hos_005_thumb_A_one_tight_band_v02.jpg",
        Path.home() / "YouTube/hos-005-blood/thumb_work/A_v02.jpg",
        HERE / "_assets_v02" / "hos_005_thumb_A_one_tight_band_v02c.jpg",
    ):
        if p.exists():
            im = Image.open(p).convert("RGB")
            if im.size != (W, H):
                im = im.resize((W, H), Image.Resampling.LANCZOS)
            print(f"  SRC_A {p}", flush=True)
            return im
    raise SystemExit("missing A painting")


def save_jpg(im: Image.Image, dest: Path) -> Path:
    dest.parent.mkdir(parents=True, exist_ok=True)
    im.convert("RGB").resize((W, H), Image.Resampling.LANCZOS).save(
        dest, "JPEG", quality=92, optimize=True, subsampling=1
    )
    print(f"  {dest.name}  {dest.stat().st_size} B", flush=True)
    return dest


def is_letter_pixel(r: int, g: int, b: int) -> bool:
    bright = r + g + b
    if bright > 170:
        return True
    # cream / gold painted faces + bevels
    if r > 130 and g > 60 and (r - b) > 25:
        return True
    # dark outline near letters still "letter territory" if warm-dark
    if bright < 90 and r > g and r > 25:
        return False
    return False


def cover_lettering(base: Image.Image) -> Image.Image:
    """Wipe A lettering by row-interpolating bookshelf; keep natural library grain."""
    out = base.copy()
    x0, y0, x1, y1 = PANEL
    region = out.crop((x0, y0, x1, y1))
    src = region.copy()
    sp = src.load()
    w, h = region.size

    # Letter / flourish / outline mask in the text column
    mask = Image.new("L", (w, h), 0)
    mp = mask.load()
    for y in range(h - 48):  # stop above Explorer hair
        for x in range(40, w - 10):
            r, g, b = sp[x, y]
            bright = r + g + b
            letter = (
                bright > 165
                or (r > 125 and g > 55 and (r - b) > 22 and r > b)
                or (r > 150 and g > 90 and b < 140 and (r - b) > 35)  # gold
            )
            if letter:
                for dy in range(-4, 5):
                    for dx in range(-4, 5):
                        xx, yy = x + dx, y + dy
                        if 0 <= xx < w and 0 <= yy < h - 40:
                            mp[xx, yy] = 255

    # Expand a soft core so thin leftovers die
    mask = mask.filter(ImageFilter.MaxFilter(5))
    mask = mask.filter(ImageFilter.GaussianBlur(2.5))
    mp = mask.load()

    filled = region.copy()
    fp = filled.load()
    for y in range(h):
        # collect clear samples on this row
        clear_xs = [x for x in range(w) if mp[x, y] < 40]
        if not clear_xs:
            continue
        x = 0
        while x < w:
            if mp[x, y] < 20:
                x += 1
                continue
            x_start = x
            while x < w and mp[x, y] >= 20:
                x += 1
            x_end = x
            # nearest clear left / right
            left = None
            for lx in range(x_start - 1, -1, -1):
                if mp[lx, y] < 40:
                    left = sp[lx, y]
                    break
            right = None
            for rx in range(x_end, w):
                if mp[rx, y] < 40:
                    right = sp[rx, y]
                    break
            if left is None:
                left = right or (18, 8, 4)
            if right is None:
                right = left
            span = max(1, x_end - x_start)
            for i, xx in enumerate(range(x_start, x_end)):
                t = i / span
                # weight by mask strength
                a = mp[xx, y] / 255.0
                blended = tuple(int(left[c] * (1 - t) + right[c] * t) for c in range(3))
                orig = sp[xx, y]
                fp[xx, y] = tuple(int(orig[c] * (1 - a) + blended[c] * a) for c in range(3))

    soft = filled.filter(ImageFilter.GaussianBlur(3.5))
    # Only blur inside mask
    covered = Image.composite(soft, filled, mask.filter(ImageFilter.GaussianBlur(2)))
    # Bottom fade into Explorer
    fade = Image.new("L", (w, h), 255)
    fd = ImageDraw.Draw(fade)
    for i in range(55):
        fd.rectangle([0, h - 55 + i, w, h], fill=int(255 * (1 - i / 55)))
    covered = Image.composite(covered, region, fade)
    out.paste(covered, (x0, y0))
    return out


def ImageEnhance_Brightness(im: Image.Image, factor: int | float) -> Image.Image:
    from PIL import ImageEnhance

    return ImageEnhance.Brightness(im).enhance(factor)


def extract_flourishes(
    a: Image.Image,
) -> tuple[Image.Image, tuple[int, int], Image.Image, tuple[int, int]]:
    def pull(box: tuple[int, int, int, int], *, max_run: int = 14) -> Image.Image:
        """Gold filigree only — skip thick vertical letter stems."""
        x0, y0, x1, y1 = box
        crop = a.crop(box)
        cw, ch = crop.size
        cp = crop.load()
        # mark gold candidates
        gold = [[False] * cw for _ in range(ch)]
        for y in range(ch):
            for x in range(cw):
                r, g, b = cp[x, y]
                if r > 155 and g > 95 and b < 145 and (r - b) > 40 and r >= g - 8:
                    if not (r > 220 and g > 185 and b > 140):  # not cream
                        gold[y][x] = True
        # suppress thick vertical runs (letter stems)
        keep = [[False] * cw for _ in range(ch)]
        for x in range(cw):
            y = 0
            while y < ch:
                if not gold[y][x]:
                    y += 1
                    continue
                y0r = y
                while y < ch and gold[y][x]:
                    y += 1
                run = y - y0r
                if run <= max_run:
                    for yy in range(y0r, y):
                        keep[yy][x] = True
        alpha = Image.new("L", (cw, ch), 0)
        ap = alpha.load()
        for y in range(ch):
            for x in range(cw):
                if keep[y][x]:
                    ap[x, y] = 255
        alpha = alpha.filter(ImageFilter.MaxFilter(3))
        alpha = alpha.filter(ImageFilter.GaussianBlur(0.7))
        out = Image.new("RGBA", (cw, ch), (0, 0, 0, 0))
        op = out.load()
        for y in range(ch):
            for x in range(cw):
                achan = ap[x, y]
                if achan > 40:
                    r, g, b = cp[x, y]
                    op[x, y] = (r, g, b, achan)
        return out

    top_box = (150, 38, 420, 78)
    bot_box = (130, 280, 440, 318)
    return pull(top_box), (top_box[0], top_box[1]), pull(bot_box, max_run=10), (bot_box[0], bot_box[1])


def paint_word_layer(
    text: str,
    *,
    size: int,
    fill: tuple[int, int, int],
    fill_hi: tuple[int, int, int],
) -> Image.Image:
    """Render one word to a tight RGBA layer (already condensed)."""
    f = ImageFont.truetype(GEORGIA, size)
    widths: list[int] = []
    for ch in text:
        bb = f.getbbox(ch)
        widths.append(bb[2] - bb[0] + TRACKING)
    total = max(1, sum(widths) - TRACKING)
    bb_all = f.getbbox(text)
    th = bb_all[3] - bb_all[1]
    pad = 24
    layer = Image.new("RGBA", (total + pad * 2, th + pad * 2), (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer)
    x0 = pad
    y0 = pad - bb_all[1]
    stroke = max(7, size // 11)

    def draw_chars(ox: int, oy: int, color, stroke_w: int = 0):
        xp = x0
        for i, ch in enumerate(text):
            kw = dict(font=f, fill=color)
            if stroke_w:
                kw.update(stroke_width=stroke_w, stroke_fill=color[:3] if len(color) == 4 else color)
                # stroke_fill must be RGB
                kw["stroke_fill"] = INK
                kw["fill"] = color
            draw.text((xp + ox, y0 + oy), ch, **kw)
            xp += widths[i]

    for dx, dy in ((7, 8), (5, 6), (3, 4)):
        draw_chars(dx, dy, SHADOW + (230,))
    for dx, dy in ((0, 0), (1, 0), (0, 1), (1, 1), (-1, 0), (0, -1), (2, 0), (0, 2)):
        draw_chars(dx, dy, INK + (255,), stroke_w=stroke)
    draw_chars(-1, -2, fill_hi + (255,))
    draw_chars(0, 0, fill + (255,))

    # Condense horizontally
    bbox = layer.split()[-1].getbbox()
    if not bbox:
        return layer
    cropped = layer.crop(bbox)
    nw = max(1, int(cropped.size[0] * CONDENSE_X))
    return cropped.resize((nw, cropped.size[1]), Image.Resampling.LANCZOS)


def paint_c(cleared: Image.Image, a_src: Image.Image) -> Image.Image:
    rgba = cleared.convert("RGBA")
    # Flourishes UNDER letters so they never clip TIE tops
    draw_simple_flourishes(rgba)
    for text, kind, size, cy in LINES:
        fill, fill_hi = (CREAM, CREAM_HI) if kind == "cream" else (GOLD, GOLD_HI)
        sprite = paint_word_layer(text, size=size, fill=fill, fill_hi=fill_hi)
        px = int(CX - sprite.size[0] / 2)
        py = int(cy - sprite.size[1] / 2)
        tmp = Image.new("RGBA", rgba.size, (0, 0, 0, 0))
        tmp.paste(sprite, (px, py), sprite)
        rgba = Image.alpha_composite(rgba, tmp)
    return rgba.convert("RGB")


def draw_simple_flourishes(rgba: Image.Image) -> None:
    """Paint gold filigree matching A's top/bottom ornaments (over extracted if any)."""
    import math

    overlay = Image.new("RGBA", rgba.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)
    gold = GOLD + (255,)
    gold2 = GOLD_HI + (230,)

    def flourish(cx: int, cy: int, half: int, up: bool) -> None:
        tip = -12 if up else 12
        # arms
        d.line([(cx - half, cy), (cx - 22, cy)], fill=gold, width=3)
        d.line([(cx + 22, cy), (cx + half, cy)], fill=gold, width=3)
        # center diamond / fleur
        d.polygon(
            [(cx, cy + tip), (cx - 9, cy), (cx, cy - tip // 4), (cx + 9, cy)],
            fill=gold2,
        )
        d.ellipse([cx - 3, cy - 3, cx + 3, cy + 3], fill=gold)
        # end scrolls
        for side in (-1, 1):
            ex = cx + side * half
            for i in range(8):
                ang = (i / 7) * math.pi * 0.85
                px = ex + side * (7 * math.sin(ang))
                py = cy + (1 if up else -1) * (-7 + 7 * math.cos(ang))
                d.ellipse([px - 1.8, py - 1.8, px + 1.8, py + 1.8], fill=gold)
            # small secondary curl
            for i in range(5):
                ang = (i / 4) * math.pi * 0.6
                px = ex - side * 12 + side * (5 * math.sin(ang))
                py = cy + (1 if up else -1) * (4 * math.cos(ang))
                d.ellipse([px - 1.2, py - 1.2, px + 1.2, py + 1.2], fill=gold2)

    # Place above TIE and below TIGHT (match A positions)
    flourish(CX, 52, 145, up=True)
    flourish(CX, 302, 155, up=False)
    # soft edge
    overlay = overlay.filter(ImageFilter.GaussianBlur(0.4))
    base = Image.alpha_composite(rgba, overlay)
    rgba.paste(base)


def check(kind: str, tool: str, jpg: Path, out: Path) -> None:
    cmd = [sys.executable, str(tools_dir() / tool), kind, str(jpg), "--out", str(out)]
    print("$", " ".join(cmd[1:]), flush=True)
    subprocess.check_call(cmd)


def main() -> None:
    WORK.mkdir(parents=True, exist_ok=True)
    SELECTED.mkdir(parents=True, exist_ok=True)

    a = src_a()
    cleared = cover_lettering(a)
    save_jpg(cleared, WORK / "cleared_panel_v02.jpg")

    c_im = paint_c(cleared, a)
    c_jpg = save_jpg(c_im, SELECTED / "hos_005_thumb_C_tie_it_tight_v02.jpg")

    MAIN_SELECTED.mkdir(parents=True, exist_ok=True)
    main_c = MAIN_SELECTED / c_jpg.name
    main_c.write_bytes(c_jpg.read_bytes())
    print(f"  MIRRORED {main_c}", flush=True)

    preview = SELECTED / f"{c_jpg.stem}_preview.jpg"
    check("long", "thumb_preview.py", c_jpg, preview)
    (MAIN_SELECTED / preview.name).write_bytes(preview.read_bytes())

    a_jpg = MAIN_SELECTED / "hos_005_thumb_A_one_tight_band_v02.jpg"
    if not a_jpg.exists():
        a_jpg = SELECTED / "hos_005_thumb_A_one_tight_band_v02.jpg"
    b_jpg = MAIN_SELECTED / "hos_005_thumb_B_it_goes_round_v02.jpg"
    if not b_jpg.exists():
        b_jpg = SELECTED / "hos_005_thumb_B_it_goes_round_v02.jpg"

    cell_a = Image.open(a_jpg).convert("RGB").resize((168, 94), Image.Resampling.LANCZOS)
    cell_c = Image.open(c_jpg).convert("RGB").resize((168, 94), Image.Resampling.LANCZOS)
    strip = Image.new("RGB", (168 * 2 + 8, 94 + 22), (12, 8, 4))
    d = ImageDraw.Draw(strip)
    try:
        fnt = ImageFont.truetype(GEORGIA, 14)
    except OSError:
        fnt = ImageFont.load_default()
    d.text((4, 2), "A", font=fnt, fill=(220, 200, 160))
    d.text((168 + 12, 2), "C v02", font=fnt, fill=(220, 200, 160))
    strip.paste(cell_a, (0, 18))
    strip.paste(cell_c, (168 + 8, 18))
    phone = WORK / "hos_005_thumb_A_vs_C_v02_phone_168.jpg"
    strip.save(phone, "JPEG", quality=92)
    # also large nearest for thread readability
    phone_x3 = WORK / "hos_005_thumb_A_vs_C_v02_phone_168_x3.jpg"
    strip.resize((strip.size[0] * 3, strip.size[1] * 3), Image.Resampling.NEAREST).save(
        phone_x3, "JPEG", quality=95
    )
    print(f"  PHONE {phone}", flush=True)

    sheet_out = SELECTED / "hos_005_thumbs_v04_style_sheet.jpg"
    subprocess.check_call(
        [
            sys.executable,
            str(tools_dir() / "style_sheet.py"),
            "long",
            str(a_jpg),
            str(b_jpg),
            str(c_jpg),
            "--out",
            str(sheet_out),
        ]
    )
    (MAIN_SELECTED / sheet_out.name).write_bytes(sheet_out.read_bytes())
    print(f"  STYLE {sheet_out.name}", flush=True)

    # panel compare for QA
    pa = Image.open(a_jpg).crop((40, 0, 540, 378))
    pc = Image.open(c_jpg).crop((40, 0, 540, 378))
    ss = Image.new("RGB", (pa.size[0] * 2 + 20, pa.size[1] + 28), (8, 4, 2))
    dd = ImageDraw.Draw(ss)
    dd.text((8, 4), "A", fill=(230, 210, 170))
    dd.text((pa.size[0] + 28, 4), "C v02", fill=(230, 210, 170))
    ss.paste(pa, (0, 24))
    ss.paste(pc, (pa.size[0] + 20, 24))
    ss.save(WORK / "compare_panel_A_C_v02.jpg", quality=92)

    sha_a = hashlib.sha256(a_jpg.read_bytes()).hexdigest()
    sha_b = hashlib.sha256(b_jpg.read_bytes()).hexdigest()
    sha_c = hashlib.sha256(c_jpg.read_bytes()).hexdigest()
    assert sha_c == hashlib.sha256(main_c.read_bytes()).hexdigest()

    idx = {
        "parentTitle": "The Tied Arm That Proved Your Blood Circulates",
        "version": "v04",
        "status": "Thumb C v02 re-letter for Claude KEEP. A/B kept. Nothing to Studio T&C yet.",
        "composer": "08_Thumbnail/_land_hos_005_thumb_C_v02.py",
        "factLock": "Tight linen band on the upper arm; red (artery) only on the shoulder side, "
        "a wide glowing artery under the skin, stopping at the band; no red below it; "
        "forearm and hand paler below the band (De Motu Cordis ch. 11, FACT_NOTES_v01 row 26).",
        "thumbs": [
            {"id": "A", "hook": "ONE TIGHT BAND", "jpg": f"Selected/{a_jpg.name}", "sha256": sha_a},
            {"id": "B", "hook": "IT GOES ROUND", "jpg": f"Selected/{b_jpg.name}", "sha256": sha_b},
            {
                "id": "C",
                "hook": "TIE IT TIGHT",
                "punch": "TIGHT",
                "jpg": f"Selected/{c_jpg.name}",
                "sha256": sha_c,
                "method": "reletter_A_painting_GeorgiaBold_no_image_model_v02",
                "note": "v01 Didot rejected; v02 heavy Georgia + flourishes. Studio-candidate sha is this Selected jpg.",
            },
        ],
        "sources": ["hos_005_thumb_A_one_tight_band_v02.jpg"],
        "upload": False,
        "studio": False,
        "studioTestAndCompare": False,
    }
    for path in (
        HERE / "THUMBS_INDEX_v03.json",
        HERE / "THUMBS_INDEX_v04.json",
        MAIN_THUMB / "THUMBS_INDEX_v03.json",
    ):
        path.write_text(json.dumps(idx, indent=2) + "\n")
    print("  INDEX updated", flush=True)
    print("  C sha256 (Studio candidate)", sha_c, flush=True)

    # Copy composer into main repo too
    main_composer = MAIN_THUMB / "_land_hos_005_thumb_C_v02.py"
    main_composer.write_text(Path(__file__).read_text())
    print(f"  COMPOSER {main_composer}", flush=True)

    manifest = MAIN_THUMB.parent / "11_Upload-Package" / "PACKAGE_MANIFEST.json"
    if manifest.exists():
        data = json.loads(manifest.read_text())
        data["thumbnailAbc"] = [
            "../08_Thumbnail/Selected/hos_005_thumb_A_one_tight_band_v02.jpg",
            "../08_Thumbnail/Selected/hos_005_thumb_B_it_goes_round_v02.jpg",
            "../08_Thumbnail/Selected/hos_005_thumb_C_tie_it_tight_v02.jpg",
        ]
        note = data.get("note") or ""
        tag = "Thumb C v02 proposed (TIE IT TIGHT) — not in Studio T&C until Claude KEEP."
        if tag not in note:
            data["note"] = (note + " | " + tag).strip(" |")
        manifest.write_text(json.dumps(data, indent=2) + "\n")
        print("  MANIFEST thumbnailAbc updated (thumbnail still A)", flush=True)


if __name__ == "__main__":
    main()
