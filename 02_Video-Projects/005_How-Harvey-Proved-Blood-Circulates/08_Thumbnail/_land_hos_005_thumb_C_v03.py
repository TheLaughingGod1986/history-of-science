#!/usr/bin/env python3
"""Land HOS 005 long Thumb C v03 — Claude KEEP fix (PR #180 #5974119758).

Fixes vs v02:
  1. Scale lettering ~+25% so TIGHT is as wide as A's BAND (phone parity).
  2. Drop new gold rules — keep A's own top/bottom brown scroll ornaments.
  3. Words stay TIE IT TIGHT (cream / cream / gold punch), house Georgia Bold.
  £0 — no image model / no Vertex / no paid generation.
"""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = Path(__file__).resolve().parent
SELECTED = HERE / "Selected"
WORK = HERE / "_work_thumb_c_v03"
TOOLS_MAIN = Path.home() / "YouTube/History Of Science/00_Brand/Channel-Setup/tools"

W, H = 1280, 720
# Letter wipe panel — stop above Explorer hair; ornaments live at top/bottom edges
PANEL = (40, 0, 540, 378)

CREAM = (238, 200, 155)
CREAM_HI = (250, 232, 198)
GOLD = (224, 150, 28)
GOLD_HI = (245, 195, 60)
INK = (14, 8, 4)
SHADOW = (4, 2, 1)

GEORGIA = "/System/Library/Fonts/Supplemental/Georgia Bold.ttf"

# Target: TIGHT width == A's BAND width (~351 core). Start ~+25% over v02 sizes.
# v02 was size 80/80/92 — v03 starts 100/100/115 and auto-fits TIGHT to BAND.
LINES_BASE = [
    ("TIE", "cream", 100, 98),
    ("IT", "cream", 100, 168),
    ("TIGHT", "gold", 115, 248),
]
TRACKING = -5
CONDENSE_X = 0.88
CX = 290  # same column centre as A / v02 — keeps left margin when width matches BAND

# Protect A's ornament bands (panel-relative y inside PANEL crop)
ORN_TOP_Y1 = 68      # don't wipe above this (top brown scroll)
ORN_BOT_Y0 = 292     # don't wipe below this (bottom brown scroll above Explorer)


def tools_dir() -> Path:
    return TOOLS_MAIN


def src_a() -> Image.Image:
    for p in (
        SELECTED / "hos_005_thumb_A_one_tight_band_v02.jpg",
        SELECTED / "hos_005_thumb_A_one_tight_band_v01.jpg",
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


def extract_ornaments(a: Image.Image) -> list[tuple[Image.Image, tuple[int, int]]]:
    """Pull A's top/bottom scroll ornaments as RGBA sprites (gold+bronze filigree, not letter stems)."""
    out: list[tuple[Image.Image, tuple[int, int]]] = []
    for box, max_run in (
        ((120, 28, 460, 78), 14),
        ((110, 285, 470, 330), 16),
    ):
        x0, y0, x1, y1 = box
        crop = a.crop(box)
        cw, ch = crop.size
        cp = crop.load()
        gold = [[False] * cw for _ in range(ch)]
        for y in range(ch):
            for x in range(cw):
                r, g, b = cp[x, y]
                # gold / bronze / dark-brown filigree (A's scrolls are often very dark)
                bright = r + g + b
                warm = (r - b) > 8 and r >= g - 20 and r > 8
                not_cream = not (r > 200 and g > 170 and b > 120)
                if warm and not_cream and bright > 12:
                    gold[y][x] = True
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
        alpha = alpha.filter(ImageFilter.GaussianBlur(0.6))
        rgba = Image.new("RGBA", (cw, ch), (0, 0, 0, 0))
        op = rgba.load()
        ap = alpha.load()
        for y in range(ch):
            for x in range(cw):
                achan = ap[x, y]
                if achan > 35:
                    r, g, b = cp[x, y]
                    op[x, y] = (r, g, b, achan)
        out.append((rgba, (x0, y0)))
        print(f"  ORN extracted box={box} nonzero={sum(1 for y in range(ch) for x in range(cw) if keep[y][x])}", flush=True)
    return out


def cover_lettering_only(base: Image.Image) -> Image.Image:
    """Aggressively wipe A lettering (faces + dark outlines/shadows). Ornaments restored later."""
    out = base.copy()
    x0, y0, x1, y1 = PANEL
    region = out.crop((x0, y0, x1, y1))
    src = region.copy()
    sp = src.load()
    w, h = region.size

    mask = Image.new("L", (w, h), 0)
    mp = mask.load()
    # Letter wipe band — stop above Explorer; ornaments will be pasted back
    for y in range(20, min(h - 50, 310)):
        for x in range(30, w - 8):
            r, g, b = sp[x, y]
            bright = r + g + b
            letter_face = (
                bright > 160
                or (r > 125 and g > 55 and (r - b) > 22 and r > b)
                or (r > 150 and g > 90 and b < 140 and (r - b) > 35)
            )
            if letter_face:
                for dy in range(-8, 9):
                    for dx in range(-8, 9):
                        xx, yy = x + dx, y + dy
                        if 0 <= xx < w and 20 <= yy < min(h - 45, 315):
                            mp[xx, yy] = 255

    # Also catch dark outline/shadow blobs inside the letter column (near faces)
    # Expand first so outlines adjacent to faces are included
    mask = mask.filter(ImageFilter.MaxFilter(9))
    mp = mask.load()
    for y in range(25, min(h - 55, 305)):
        for x in range(40, w - 15):
            if mp[x, y] < 200:
                continue
            # already marked — ok
            pass
    # Dark ink near marked areas: flood a bit more for drop shadows
    for y in range(25, min(h - 55, 305)):
        for x in range(40, w - 15):
            r, g, b = sp[x, y]
            bright = r + g + b
            if bright < 55 and r <= 40:
                # near a marked letter?
                near = False
                for dy in range(-6, 7):
                    for dx in range(-6, 7):
                        xx, yy = x + dx, y + dy
                        if 0 <= xx < w and 0 <= yy < h and mp[xx, yy] > 180:
                            near = True
                            break
                    if near:
                        break
                if near:
                    mp[x, y] = 255

    mask = mask.filter(ImageFilter.MaxFilter(5))
    mask = mask.filter(ImageFilter.GaussianBlur(2.8))
    mp = mask.load()

    filled = region.copy()
    fp = filled.load()
    for y in range(h):
        clear_xs = [x for x in range(w) if mp[x, y] < 40]
        if not clear_xs:
            # fully masked row — sample from nearby clear rows
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
                a = mp[xx, y] / 255.0
                blended = tuple(int(left[c] * (1 - t) + right[c] * t) for c in range(3))
                orig = sp[xx, y]
                fp[xx, y] = tuple(int(orig[c] * (1 - a) + blended[c] * a) for c in range(3))

    soft = filled.filter(ImageFilter.GaussianBlur(3.5))
    covered = Image.composite(soft, filled, mask.filter(ImageFilter.GaussianBlur(2)))
    fade = Image.new("L", (w, h), 255)
    fd = ImageDraw.Draw(fade)
    for i in range(55):
        fd.rectangle([0, h - 55 + i, w, h], fill=int(255 * (1 - i / 55)))
    covered = Image.composite(covered, region, fade)
    out.paste(covered, (x0, y0))
    return out


def paint_word_layer(
    text: str,
    *,
    size: int,
    fill: tuple[int, int, int],
    fill_hi: tuple[int, int, int],
) -> Image.Image:
    f = ImageFont.truetype(GEORGIA, size)
    widths: list[int] = []
    for ch in text:
        bb = f.getbbox(ch)
        widths.append(bb[2] - bb[0] + TRACKING)
    total = max(1, sum(widths) - TRACKING)
    bb_all = f.getbbox(text)
    th = bb_all[3] - bb_all[1]
    pad = 28
    layer = Image.new("RGBA", (total + pad * 2, th + pad * 2), (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer)
    x0 = pad
    y0 = pad - bb_all[1]
    stroke = max(7, size // 11)

    def draw_chars(ox: int, oy: int, color, stroke_w: int = 0):
        xp = x0
        for i, ch in enumerate(text):
            kw: dict = dict(font=f, fill=color)
            if stroke_w:
                kw.update(stroke_width=stroke_w, stroke_fill=INK)
            draw.text((xp + ox, y0 + oy), ch, **kw)
            xp += widths[i]

    for dx, dy in ((7, 8), (5, 6), (3, 4)):
        draw_chars(dx, dy, SHADOW + (230,))
    for dx, dy in ((0, 0), (1, 0), (0, 1), (1, 1), (-1, 0), (0, -1), (2, 0), (0, 2)):
        draw_chars(dx, dy, INK + (255,), stroke_w=stroke)
    draw_chars(-1, -2, fill_hi + (255,))
    draw_chars(0, 0, fill + (255,))

    bbox = layer.split()[-1].getbbox()
    if not bbox:
        return layer
    cropped = layer.crop(bbox)
    nw = max(1, int(cropped.size[0] * CONDENSE_X))
    return cropped.resize((nw, cropped.size[1]), Image.Resampling.LANCZOS)


def core_word_width(path_or_im, y_lo: int, y_hi: int) -> int:
    im = path_or_im if isinstance(path_or_im, Image.Image) else Image.open(path_or_im).convert("RGB")
    crop = im.crop((40, y_lo, 540, y_hi))
    px = crop.load()
    w, h = crop.size
    cols_hit = [0] * w
    for y in range(h):
        for x in range(w):
            r, g, b = px[x, y]
            if r + g + b > 200 or (r > 180 and g > 100 and (r - b) > 40):
                cols_hit[x] += 1
    thr = max(2, h // 8)
    xs = [x for x, c in enumerate(cols_hit) if c >= thr]
    if not xs:
        return 0
    return xs[-1] - xs[0] + 1


def tight_core_width(size: int) -> tuple[int, int, int]:
    """Return (core_w, left_x, right_x) for TIGHT at given size on a blank canvas."""
    sprite = paint_word_layer("TIGHT", size=size, fill=GOLD, fill_hi=GOLD_HI)
    canvas = Image.new("RGB", (W, H), (0, 0, 0)).convert("RGBA")
    px = int(CX - sprite.size[0] / 2)
    py = 180
    tmp = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    tmp.paste(sprite, (px, py), sprite)
    rgb = Image.alpha_composite(canvas, tmp).convert("RGB")
    crop = rgb.crop((40, py, 540, py + sprite.size[1]))
    pix = crop.load()
    w, h = crop.size
    cols = [0] * w
    for y in range(h):
        for x in range(w):
            r, g, b = pix[x, y]
            if r + g + b > 200 or (r > 180 and g > 100 and (r - b) > 40):
                cols[x] += 1
    thr = max(2, h // 8)
    xs = [x for x, c in enumerate(cols) if c >= thr]
    if not xs:
        return 0, 0, 0
    return xs[-1] - xs[0] + 1, 40 + xs[0], 40 + xs[-1]


def fit_tight_size(target_band_w: int) -> int:
    """Binary-search Georgia size so TIGHT CORE width ≈ A's BAND (±2%)."""
    lo, hi = 100, 140
    best = 118
    best_err = 9999
    for _ in range(16):
        mid = (lo + hi) // 2
        cw, left, right = tight_core_width(mid)
        err = abs(cw - target_band_w)
        print(f"  fit TIGHT size={mid} core_w={cw} left={left} target={target_band_w} err={err}", flush=True)
        if err < best_err:
            best_err = err
            best = mid
        if cw < target_band_w * 0.985:
            lo = mid + 1
        elif cw > target_band_w * 1.015:
            hi = mid - 1
        else:
            return mid
        if lo > hi:
            break
    return best


def paint_c(cleared: Image.Image, lines: list, ornaments: list | None = None) -> Image.Image:
    """Restore A's ornaments first, then composite TIE IT TIGHT (no new gold rules)."""
    rgba = cleared.convert("RGBA")
    # Ornaments under letters — letters sit above bottom scroll like A
    if ornaments:
        for spr, (ox, oy) in ornaments:
            tmp = Image.new("RGBA", rgba.size, (0, 0, 0, 0))
            tmp.paste(spr, (ox, oy), spr)
            rgba = Image.alpha_composite(rgba, tmp)
            print(f"  ORN pasted at ({ox},{oy}) size={spr.size}", flush=True)
    for text, kind, size, cy in lines:
        fill, fill_hi = (CREAM, CREAM_HI) if kind == "cream" else (GOLD, GOLD_HI)
        sprite = paint_word_layer(text, size=size, fill=fill, fill_hi=fill_hi)
        px = int(CX - sprite.size[0] / 2)
        py = int(cy - sprite.size[1] / 2)
        # Keep TIGHT bottom above bottom ornament (starts ~278)
        if text == "TIGHT":
            max_bottom = 276
            if py + sprite.size[1] > max_bottom:
                py = max_bottom - sprite.size[1]
        # Keep TIE top below top ornament (ends ~78)
        if text == "TIE":
            min_top = 78
            if py < min_top:
                py = min_top
        tmp = Image.new("RGBA", rgba.size, (0, 0, 0, 0))
        tmp.paste(sprite, (px, py), sprite)
        rgba = Image.alpha_composite(rgba, tmp)
        print(f"  word {text} size={size} cy={cy} sprite={sprite.size} at=({px},{py})", flush=True)
    return rgba.convert("RGB")


def check(kind: str, tool: str, jpg: Path, out: Path) -> None:
    cmd = [sys.executable, str(tools_dir() / tool), kind, str(jpg), "--out", str(out)]
    print("$", " ".join(cmd[1:]), flush=True)
    subprocess.check_call(cmd)


def make_phone_sheet(a_jpg: Path, c_jpg: Path, out: Path, label_c: str = "C v03") -> Path:
    cell_a = Image.open(a_jpg).convert("RGB").resize((168, 94), Image.Resampling.LANCZOS)
    cell_c = Image.open(c_jpg).convert("RGB").resize((168, 94), Image.Resampling.LANCZOS)
    strip = Image.new("RGB", (168 * 2 + 8, 94 + 22), (12, 8, 4))
    d = ImageDraw.Draw(strip)
    try:
        fnt = ImageFont.truetype(GEORGIA, 14)
    except OSError:
        fnt = ImageFont.load_default()
    d.text((4, 2), "A", font=fnt, fill=(220, 200, 160))
    d.text((168 + 12, 2), label_c, font=fnt, fill=(220, 200, 160))
    strip.paste(cell_a, (0, 18))
    strip.paste(cell_c, (168 + 8, 18))
    out.parent.mkdir(parents=True, exist_ok=True)
    strip.save(out, "JPEG", quality=92)
    x3 = out.with_name(out.stem + "_x3.jpg")
    strip.resize((strip.size[0] * 3, strip.size[1] * 3), Image.Resampling.NEAREST).save(
        x3, "JPEG", quality=95
    )
    print(f"  PHONE {out}", flush=True)
    print(f"  PHONE_X3 {x3}", flush=True)
    return out


def main() -> None:
    WORK.mkdir(parents=True, exist_ok=True)
    SELECTED.mkdir(parents=True, exist_ok=True)

    a = src_a()
    band_w = core_word_width(a, 220, 285)
    print(f"  A BAND core width = {band_w}px", flush=True)
    if band_w < 200:
        band_w = 351  # fallback from prior measure
        print(f"  fallback BAND target = {band_w}", flush=True)

    ornaments = extract_ornaments(a)
    cleared = cover_lettering_only(a)
    save_jpg(cleared, WORK / "cleared_panel_v03.jpg")

    tight_size = fit_tight_size(band_w)
    # Scale cream lines proportionally to v02 ratio (80/92) → keep ~same proportion
    cream_size = max(88, int(round(tight_size * (80 / 92))))
    # Vertical centres: match A's stack height (ONE~94, cream TIGHT~168, BAND~245)
    # With larger glyphs, nudge slightly so stack fills same vertical as A between ornaments
    lines = [
        ("TIE", "cream", cream_size, 112),
        ("IT", "cream", cream_size, 168),
        ("TIGHT", "gold", tight_size, 224),
    ]
    print(f"  LINES {lines}", flush=True)

    c_im = paint_c(cleared, lines, ornaments)
    c_jpg = save_jpg(c_im, SELECTED / "hos_005_thumb_C_tie_it_tight_v03.jpg")

    # Measure TIGHT in its actual y band (fitted glyph sits above bottom ornament)
    tight_w = core_word_width(c_jpg, 175, 275)
    ratio = tight_w / band_w if band_w else 0
    print(f"  MEASURE full: BAND={band_w} TIGHT={tight_w} ratio={ratio:.3f}", flush=True)

    def left_edge(path, y_lo, y_hi):
        im = Image.open(path).convert("RGB")
        crop = im.crop((40, y_lo, 540, y_hi))
        px = crop.load(); w, h = crop.size
        for x in range(w):
            for y in range(h):
                r, g, b = px[x, y]
                if r + g + b > 200 or (r > 180 and g > 100 and (r - b) > 40):
                    return 40 + x
        return None

    a_ref = SELECTED / "hos_005_thumb_A_one_tight_band_v02.jpg"
    print(
        f"  LEFT BAND={left_edge(a_ref, 220, 285)} TIGHT={left_edge(c_jpg, 175, 275)}",
        flush=True,
    )

    preview = SELECTED / f"{c_jpg.stem}_preview.jpg"
    try:
        check("long", "thumb_preview.py", c_jpg, preview)
    except Exception as e:
        print(f"  preview skip: {e}", flush=True)

    a_jpg = SELECTED / "hos_005_thumb_A_one_tight_band_v02.jpg"
    b_jpg = SELECTED / "hos_005_thumb_B_it_goes_round_v02.jpg"

    phone = WORK / "hos_005_thumb_A_vs_C_v03_phone_168.jpg"
    make_phone_sheet(a_jpg, c_jpg, phone)
    # also copy phone sheet next to Selected for convenience
    (SELECTED / phone.name).write_bytes(phone.read_bytes())
    x3 = phone.with_name(phone.stem + "_x3.jpg")
    if x3.exists():
        (SELECTED / x3.name).write_bytes(x3.read_bytes())

    # Phone-scale widths
    def phone_core(path, y_lo_full, y_hi_full):
        im = Image.open(path).convert("RGB").resize((168, 94), Image.Resampling.LANCZOS)
        sy = 94 / 720
        return core_word_width(im, int(y_lo_full * sy), int(y_hi_full * sy))

    # core_word_width assumes full-res panel x 40-540; for phone need different helper
    def phone_punch_w(path, y_lo_full, y_hi_full):
        im = Image.open(path).convert("RGB").resize((168, 94), Image.Resampling.LANCZOS)
        sx, sy = 168 / 1280, 94 / 720
        x0, x1 = int(40 * sx), int(540 * sx)
        y0, y1 = int(y_lo_full * sy), int(y_hi_full * sy)
        crop = im.crop((x0, y0, x1, y1))
        px = crop.load()
        w, h = crop.size
        cols_hit = [0] * w
        for y in range(h):
            for x in range(w):
                r, g, b = px[x, y]
                if r + g + b > 200 or (r > 180 and g > 100 and (r - b) > 40):
                    cols_hit[x] += 1
        thr = max(1, h // 6)
        xs = [x for x, c in enumerate(cols_hit) if c >= thr]
        if not xs:
            return 0
        return xs[-1] - xs[0] + 1

    band_phone = phone_punch_w(a_jpg, 220, 285)
    tight_phone = phone_punch_w(c_jpg, 175, 275)
    print(f"  MEASURE phone168: BAND={band_phone} TIGHT={tight_phone}", flush=True)

    sheet_out = SELECTED / "hos_005_thumbs_v05_style_sheet.jpg"
    try:
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
        print(f"  STYLE {sheet_out.name}", flush=True)
    except Exception as e:
        print(f"  style_sheet skip: {e}", flush=True)

    pa = Image.open(a_jpg).crop((40, 0, 540, 378))
    pc = Image.open(c_jpg).crop((40, 0, 540, 378))
    ss = Image.new("RGB", (pa.size[0] * 2 + 20, pa.size[1] + 28), (8, 4, 2))
    dd = ImageDraw.Draw(ss)
    dd.text((8, 4), "A", fill=(230, 210, 170))
    dd.text((pa.size[0] + 28, 4), "C v03", fill=(230, 210, 170))
    ss.paste(pa, (0, 24))
    ss.paste(pc, (pa.size[0] + 20, 24))
    ss.save(WORK / "compare_panel_A_C_v03.jpg", quality=92)

    sha_a = hashlib.sha256(a_jpg.read_bytes()).hexdigest()
    sha_b = hashlib.sha256(b_jpg.read_bytes()).hexdigest()
    sha_c = hashlib.sha256(c_jpg.read_bytes()).hexdigest()

    idx = {
        "parentTitle": "The Tied Arm That Proved Your Blood Circulates",
        "version": "v05",
        "status": "Thumb C v03 Claude KEEP fix: TIGHT≈BAND width, A's ornaments only, no new gold rules. Ready for Studio T&C on wwcjcFfC-5M.",
        "composer": "08_Thumbnail/_land_hos_005_thumb_C_v03.py",
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
                "method": "reletter_A_painting_GeorgiaBold_no_image_model_v03_keep_A_ornaments",
                "note": "v02 had doubled gold rules + undersized TIGHT. v03 scales stack so TIGHT≈BAND, drops new gold, keeps A's brown scrolls. Studio-candidate sha is this Selected jpg.",
                "measures": {
                    "band_full_px": band_w,
                    "tight_full_px": tight_w,
                    "band_phone168_px": band_phone,
                    "tight_phone168_px": tight_phone,
                    "ratio_full": round(ratio, 4),
                },
            },
        ],
        "sources": ["hos_005_thumb_A_one_tight_band_v02.jpg"],
        "upload": False,
        "studio": False,
        "studioTestAndCompare": False,
        "studioTestAndCompareVideoId": "wwcjcFfC-5M",
    }
    for path in (HERE / "THUMBS_INDEX_v05.json", HERE / "THUMBS_INDEX_v03.json"):
        path.write_text(json.dumps(idx, indent=2) + "\n")
    print("  INDEX updated", flush=True)
    print("  C sha256 (Studio candidate)", sha_c, flush=True)

    manifest = HERE.parent / "11_Upload-Package" / "PACKAGE_MANIFEST.json"
    if manifest.exists():
        data = json.loads(manifest.read_text())
        data["thumbnailAbc"] = [
            "../08_Thumbnail/Selected/hos_005_thumb_A_one_tight_band_v02.jpg",
            "../08_Thumbnail/Selected/hos_005_thumb_B_it_goes_round_v02.jpg",
            "../08_Thumbnail/Selected/hos_005_thumb_C_tie_it_tight_v03.jpg",
        ]
        note = data.get("note") or ""
        tag = "Thumb C v03 proposed (TIE IT TIGHT, KEEP-scale, A's ornaments) — Studio T&C ready on wwcjcFfC-5M after Claude KEEP."
        # strip old v02 tag if present
        if "Thumb C v02" in note:
            parts = [p.strip() for p in note.split("|")]
            parts = [p for p in parts if "Thumb C v02" not in p]
            note = " | ".join(parts)
        if tag not in note:
            data["note"] = (note + " | " + tag).strip(" |")
        manifest.write_text(json.dumps(data, indent=2) + "\n")
        print("  MANIFEST thumbnailAbc updated (thumbnail still A)", flush=True)

    print("DONE", flush=True)


if __name__ == "__main__":
    main()
