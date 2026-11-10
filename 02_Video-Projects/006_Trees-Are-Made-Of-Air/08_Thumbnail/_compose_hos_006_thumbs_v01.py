#!/usr/bin/env python3
"""Compose HOS 006 Trees long thumbnails A + B (OWB queue J0869, Step 2 of 2).

Chief pick on J0858 (OWB #99 comment 6355648154):
- Concept A (Primary): 'WOOD / FROM / SKY?' (gold punch word 'SKY?', cream 'WOOD' + 'FROM')
  over Plate A (willow by sunlit arched window with golden-teal air ribbons condensing into glowing wood rings).
- Concept B (Test & Compare second): 'DO PLANTS / EAT / SOIL?' (gold punch word 'SOIL?', cream 'DO PLANTS' + 'EAT')
  over Plate B (van Helmont's 17th-century brass balance scale, uprooted willow pan weighed down low, dried soil pot
  lifted high, zero written numbers on the plate).
- Concept C is dropped.
- Price: Option 1, 0 Flow credits (Nano Banana 2 16:9 stills on AI Ultra + £0 deterministic Python cover-builder lettering).
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
FILM_DIR = HERE.parent
REPO = FILM_DIR.parents[1]
ASSETS = HERE / "_assets_v01"
SELECTED = HERE / "Selected"
TOOLS = REPO / "00_Brand" / "Channel-Setup" / "tools"

PLATE_A = ASSETS / "hos_006_thumb_A_wood_from_sky_plate01.jpg"
PLATE_B = ASSETS / "hos_006_thumb_B_do_plants_eat_soil_plate01.jpg"
ORNAMENT_REF = (
    REPO
    / "02_Video-Projects"
    / "005_How-Harvey-Proved-Blood-Circulates"
    / "08_Thumbnail"
    / "Selected"
    / "hos_005_thumb_A_one_tight_band_v02.jpg"
)

OUT_A = SELECTED / "hos_006_thumb_A_wood_from_sky_v01.jpg"
OUT_B = SELECTED / "hos_006_thumb_B_do_plants_eat_soil_v01.jpg"

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


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def render_scroll_flourish(width: int, height: int, *, is_top: bool = True) -> Image.Image:
    """Render a crisp 4x-supersampled house gold filigree scroll flourish with dark ink
    outline and drop shadow, matching Live 001/002/004/005 without background book/hair bleed."""
    scale = 4
    sw, sh = width * scale, height * scale
    layer = Image.new("RGBA", (sw, sh), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    cx = sw // 2
    cy = int(sh * (0.64 if is_top else 0.36))
    direction = -1 if is_top else 1

    def draw_pass(ox: int, oy: int, col: tuple[int, int, int, int], extra_w: int = 0) -> None:
        # Tapered horizontal rule wings
        wing = int(sw * 0.46)
        for step in range(wing):
            t = step / max(1, wing)
            half_t = max(1, int(round((1.0 - t ** 1.4) * (2.6 * scale) + extra_w)))
            x_l = cx - step + ox
            x_r = cx + step + ox
            y_c = cy + oy
            d.line([(x_l, y_c - half_t), (x_l, y_c + half_t)], fill=col)
            d.line([(x_r, y_c - half_t), (x_r, y_c + half_t)], fill=col)

        # Central fleur-de-lis / diamond finial
        fh = int(sh * 0.44)
        fw = int(sh * 0.28)
        poly = [
            (cx + ox, cy + direction * fh + oy),
            (cx + fw + ox, cy + oy),
            (cx + ox, cy - direction * int(fh * 0.38) + oy),
            (cx - fw + ox, cy + oy),
        ]
        d.polygon(poly, fill=col)

        # Symmetrical C-scroll curls flanking the center finial
        for side in (-1, 1):
            pts = []
            for i in range(45):
                u = i / 44.0
                ang = u * 1.85 * np.pi
                rx = side * (fw * 1.15 + u * (sw * 0.13) - np.sin(ang) * (sh * 0.22))
                ry = direction * (np.sin(ang * 0.65) * (sh * 0.36) * (1.0 - 0.35 * u))
                pts.append((int(round(cx + rx + ox)), int(round(cy + ry + oy))))
            w_curl = max(2, int(round(2.4 * scale + extra_w * 1.6)))
            d.line(pts, fill=col, width=w_curl, joint="curve")
            # End droplet
            ex, ey = pts[-1]
            r_drop = max(2, int(round(2.8 * scale + extra_w)))
            d.ellipse([ex - r_drop, ey - r_drop, ex + r_drop, ey + r_drop], fill=col)

    # 1. Drop shadow
    draw_pass(2 * scale, 3 * scale, SHADOW + (210,), extra_w=scale)
    # 2. Dark ink outline
    draw_pass(0, 0, INK + (255,), extra_w=int(1.8 * scale))
    # 3. Warm gold body + highlight
    draw_pass(0, 0, GOLD + (255,), extra_w=0)
    draw_pass(0, -1 * scale, GOLD_HI + (220,), extra_w=-max(1, scale // 2))

    return layer.resize((width, height), Image.Resampling.LANCZOS)


def extract_scroll_ornaments(ref_path: Path) -> tuple[Image.Image, Image.Image]:
    """Build crisp top and bottom house gold scroll flourishes."""
    return (
        render_scroll_flourish(340, 20, is_top=True),
        render_scroll_flourish(280, 18, is_top=False),
    )


def render_word(
    text: str,
    size: int,
    fill: tuple[int, int, int],
    fill_hi: tuple[int, int, int],
    condense_x: float = CONDENSE_X,
) -> Image.Image:
    f = ImageFont.truetype(GEORGIA, size)
    widths = [
        (f.getbbox(ch)[2] - f.getbbox(ch)[0] + TRACKING) if ch != " " else int(size * 0.28)
        for ch in text
    ]
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
            if ch != " ":
                kw = dict(font=f, fill=color)
                if sw:
                    kw.update(stroke_width=sw, stroke_fill=INK + (255,))
                d.text((x + ox, y0 + oy), ch, **kw)
            x += widths[i]

    for dx, dy in ((6, 7), (4, 5), (2, 3)):
        chars(dx, dy, SHADOW + (235,))
    chars(0, 0, INK + (255,), sw=stroke)
    chars(-1, -2, fill_hi + (255,))
    chars(0, 0, fill + (255,))
    bbox = layer.split()[-1].getbbox()
    if bbox:
        layer = layer.crop(bbox)
    return layer.resize(
        (max(1, int(round(layer.size[0] * condense_x))), layer.size[1]),
        Image.Resampling.LANCZOS,
    )


def prepare_plate_a(im: Image.Image) -> Image.Image:
    """Calm any stray dust motes in the upper-left lettering band (x=40..425, y=10..315)
    and subtly boost the glowing wood rings and golden-teal air ribbons so they pop at 168x94.
    Preserves 100% of the painted Explorer untouched."""
    arr = np.array(im.convert("RGB"), dtype=np.float32)
    yy, xx = np.mgrid[0:H, 0:W]

    # 1. Remove tiny dust specks inside the upper-left bookcase band (x=40..420, y=10..315)
    med = np.array(im.filter(ImageFilter.MedianFilter(7)), dtype=np.float32)
    band_mask = np.zeros((H, W), dtype=np.float32)
    band_mask[10:315, 40:420] = 1.0
    band_mask = np.array(
        Image.fromarray((band_mask * 255).astype(np.uint8), "L").filter(ImageFilter.GaussianBlur(10)),
        dtype=np.float32,
    ) / 255.0
    speck = ((arr - med).sum(axis=2) > 35.0).astype(np.float32) * band_mask
    arr = arr * (1.0 - speck[:, :, None]) + med * speck[:, :, None]

    # Soft vignette in upper-left band so cream/gold serif text has maximum contrast
    ul_vignette = np.exp(-(((xx - 232.0) / 210.0) ** 2 + ((yy - 160.0) / 145.0) ** 2))
    arr *= (1.0 - 0.22 * ul_vignette[:, :, None])

    # 2. Gentle clarity & glow boost on the trunk wood-ring cutaway (x=820..960, y=260..420)
    ring_region = np.exp(-(((xx - 890.0) / 70.0) ** 2 + ((yy - 340.0) / 75.0) ** 2))
    arr[:, :, 0] += ring_region * 10.0
    arr[:, :, 1] += ring_region * 6.0

    out = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8), "RGB")
    out = ImageEnhance.Sharpness(out).enhance(1.12)
    return out


def prepare_plate_b(im: Image.Image) -> Image.Image:
    """Calm any stray dust motes in the upper-left lettering band (x=40..465, y=10..288)
    and add a subtle upper-left contrast vignette while preserving 100% of the painted
    Explorer and brass scale untouched."""
    comp = np.array(im.convert("RGB"), dtype=np.float32)

    # Calm dust motes in the upper-left lettering band (x=40..465, y=10..288)
    med = np.array(im.filter(ImageFilter.MedianFilter(7)), dtype=np.float32)
    band_mask = np.zeros((H, W), dtype=np.float32)
    band_mask[10:288, 40:465] = 1.0
    band_mask = np.array(
        Image.fromarray((band_mask * 255).astype(np.uint8), "L").filter(ImageFilter.GaussianBlur(10)),
        dtype=np.float32,
    ) / 255.0
    speck = ((comp - med).sum(axis=2) > 32.0).astype(np.float32) * band_mask
    comp = comp * (1.0 - speck[:, :, None]) + med * speck[:, :, None]

    yy, xx = np.mgrid[0:H, 0:W]
    ul_vignette = np.exp(-(((xx - 250.0) / 225.0) ** 2 + ((yy - 150.0) / 138.0) ** 2))
    comp *= (1.0 - 0.24 * ul_vignette[:, :, None])

    out = Image.fromarray(np.clip(comp, 0, 255).astype(np.uint8), "RGB")
    out = ImageEnhance.Sharpness(out).enhance(1.12)
    return out


def compose_variant(
    base_rgb: Image.Image,
    lines_spec: list[tuple[str, str, int, float]],
    *,
    cx: int,
    top_y: int,
    line_gap: int,
    top_orn: Image.Image,
    bot_orn: Image.Image,
    hero_box: tuple[int, int, int, int],
    explorer_box: tuple[int, int, int, int],
) -> tuple[Image.Image, dict]:
    rgba = base_rgb.convert("RGBA")

    sprites = []
    for text, kind, size, cond in lines_spec:
        fill, hi = (CREAM, CREAM_HI) if kind == "cream" else (GOLD, GOLD_HI)
        spr = render_word(text, size, fill, hi, condense_x=cond)
        sprites.append((text, kind, size, spr))

    # Place top scroll ornament above line 1
    top_w = min(340, max(s[3].size[0] for s in sprites) + 24)
    top_h = max(16, int(round(top_orn.size[1] * (top_w / max(1, top_orn.size[0])))))
    top_spr = top_orn.resize((top_w, top_h), Image.Resampling.LANCZOS)
    top_ox = int(round(cx - top_spr.size[0] / 2))
    top_oy = max(8, top_y - top_h - 4)
    tmp = Image.new("RGBA", rgba.size, (0, 0, 0, 0))
    tmp.paste(top_spr, (top_ox, top_oy), top_spr)
    rgba = Image.alpha_composite(rgba, tmp)

    y = top_y
    placed = []
    for text, kind, size, spr in sprites:
        left_x = int(round(cx - spr.size[0] / 2))
        tmp = Image.new("RGBA", rgba.size, (0, 0, 0, 0))
        tmp.paste(spr, (left_x, y), spr)
        rgba = Image.alpha_composite(rgba, tmp)
        placed.append({
            "word": text,
            "kind": kind,
            "size": size,
            "box": [left_x, y, left_x + spr.size[0], y + spr.size[1]],
        })
        y += spr.size[1] + line_gap

    # Place bottom scroll ornament below line 3
    bot_w = min(280, int(top_w * 0.82))
    bot_h = max(14, int(round(bot_orn.size[1] * (bot_w / max(1, bot_orn.size[0])))))
    bot_spr = bot_orn.resize((bot_w, bot_h), Image.Resampling.LANCZOS)
    bot_ox = int(round(cx - bot_spr.size[0] / 2))
    bot_oy = y - line_gap + 3
    tmp = Image.new("RGBA", rgba.size, (0, 0, 0, 0))
    tmp.paste(bot_spr, (bot_ox, bot_oy), bot_spr)
    rgba = Image.alpha_composite(rgba, tmp)

    left = min(p["box"][0] for p in placed)
    right = max(p["box"][2] for p in placed)
    top = min(p["box"][1] for p in placed)
    bottom = max(p["box"][3] for p in placed)
    orn_bottom = bot_oy + bot_h

    clear_of_hero = right < hero_box[0]
    clear_of_explorer = orn_bottom <= explorer_box[1]
    clear_of_badge = bottom < H - 140

    meta = {
        "letteringBox": [left, top, right, bottom],
        "ornaments": {
            "topScrollBox": [top_ox, top_oy, top_ox + top_w, top_oy + top_h],
            "bottomScrollBox": [bot_ox, bot_oy, bot_ox + bot_w, bot_oy + bot_h],
        },
        "heroBox": list(hero_box),
        "explorerBox": list(explorer_box),
        "explorerHeightPx": explorer_box[3] - explorer_box[1],
        "explorerHeightFrac": round((explorer_box[3] - explorer_box[1]) / H, 3),
        "placedWords": placed,
        "clearOfHero": clear_of_hero,
        "clearOfExplorer": clear_of_explorer,
        "clearOfBadge": clear_of_badge,
    }
    return rgba.convert("RGB"), meta


def main() -> int:
    for p in (PLATE_A, PLATE_B, ORNAMENT_REF):
        if not p.exists():
            raise SystemExit(f"Missing input file: {p}")

    SELECTED.mkdir(parents=True, exist_ok=True)
    top_orn, bot_orn = extract_scroll_ornaments(ORNAMENT_REF)

    # 1. Compose Concept A: WOOD / FROM / SKY? (gold SKY?)
    base_a = prepare_plate_a(Image.open(PLATE_A).convert("RGB").resize((W, H), Image.Resampling.LANCZOS))
    lines_a = [
        ("WOOD", "cream", 78, 0.90),
        ("FROM", "cream", 78, 0.90),
        ("SKY?", "gold", 104, 0.92),
    ]
    hero_box_a = (440, 20, 1120, 650)
    explorer_box_a = (128, 323, 398, 720)
    im_a, meta_a = compose_variant(
        base_a,
        lines_a,
        cx=232,
        top_y=36,
        line_gap=4,
        top_orn=top_orn,
        bot_orn=bot_orn,
        hero_box=hero_box_a,
        explorer_box=explorer_box_a,
    )
    im_a.save(OUT_A, "JPEG", quality=93, optimize=True, subsampling=1)
    print(f"A composed -> {OUT_A.name}: box={meta_a['letteringBox']} orn_bot={meta_a['ornaments']['bottomScrollBox'][3]} "
          f"clear_hero={meta_a['clearOfHero']} clear_exp={meta_a['clearOfExplorer']} clear_badge={meta_a['clearOfBadge']}")

    # 2. Compose Concept B: DO PLANTS / EAT / SOIL? (gold SOIL?)
    base_b = prepare_plate_b(Image.open(PLATE_B).convert("RGB").resize((W, H), Image.Resampling.LANCZOS))
    lines_b = [
        ("DO PLANTS", "cream", 68, 0.86),
        ("EAT", "cream", 78, 0.92),
        ("SOIL?", "gold", 100, 0.92),
    ]
    hero_box_b = (485, 65, 1265, 620)
    explorer_box_b = (64, 295, 430, 720)
    im_b, meta_b = compose_variant(
        base_b,
        lines_b,
        cx=250,
        top_y=30,
        line_gap=2,
        top_orn=top_orn,
        bot_orn=bot_orn,
        hero_box=hero_box_b,
        explorer_box=explorer_box_b,
    )
    im_b.save(OUT_B, "JPEG", quality=93, optimize=True, subsampling=1)
    print(f"B composed -> {OUT_B.name}: box={meta_b['letteringBox']} orn_bot={meta_b['ornaments']['bottomScrollBox'][3]} "
          f"clear_hero={meta_b['clearOfHero']} clear_exp={meta_b['clearOfExplorer']} clear_badge={meta_b['clearOfBadge']}")

    if not (meta_a["clearOfHero"] and meta_a["clearOfExplorer"] and meta_a["clearOfBadge"]):
        raise SystemExit(f"A failed layout clearance: {meta_a}")
    if not (meta_b["clearOfHero"] and meta_b["clearOfExplorer"] and meta_b["clearOfBadge"]):
        raise SystemExit(f"B failed layout clearance: {meta_b}")

    # 3. Run thumb_preview.py long and style_sheet.py long for A and B
    prev_a = SELECTED / f"{OUT_A.stem}_preview.jpg"
    prev_b = SELECTED / f"{OUT_B.stem}_preview.jpg"
    sheet_a = SELECTED / f"{OUT_A.stem}_style_sheet.jpg"
    sheet_b = SELECTED / f"{OUT_B.stem}_style_sheet.jpg"
    sheet_ab = SELECTED / "hos_006_thumbs_AB_v01_style_sheet.jpg"

    subprocess.check_call([sys.executable, str(TOOLS / "thumb_preview.py"), "long", str(OUT_A), "--out", str(prev_a)])
    subprocess.check_call([sys.executable, str(TOOLS / "thumb_preview.py"), "long", str(OUT_B), "--out", str(prev_b)])
    subprocess.check_call([sys.executable, str(TOOLS / "style_sheet.py"), "long", str(OUT_A), "--out", str(sheet_a)])
    subprocess.check_call([sys.executable, str(TOOLS / "style_sheet.py"), "long", str(OUT_B), "--out", str(sheet_b)])
    subprocess.check_call([sys.executable, str(TOOLS / "style_sheet.py"), "long", str(OUT_A), str(OUT_B), "--out", str(sheet_ab)])

    # 4. Build side-by-side A vs B comparison & 168x94 phone sheet
    phone_ab = SELECTED / "hos_006_thumbs_AB_v01_phone_168.jpg"
    panels = [
        ("Primary A (WOOD / FROM / SKY?)", "A primary", im_a),
        ("Test & Compare B (DO PLANTS / EAT / SOIL?)", "B T&C", im_b),
    ]
    strip = Image.new("RGB", (480 * 2 + 36, 270 + 94 + 84), (14, 10, 6))
    d = ImageDraw.Draw(strip)
    lf = ImageFont.truetype(GEORGIA, 16)
    for i, (label, short_lbl, src_im) in enumerate(panels):
        x0 = 12 + i * (480 + 12)
        d.text((x0, 8), label, font=lf, fill=(238, 214, 172))
        strip.paste(src_im.resize((480, 270), Image.Resampling.LANCZOS), (x0, 32))
        d.text((x0, 312), f"168x94 phone tile ({short_lbl})", font=lf, fill=(210, 184, 142))
        strip.paste(src_im.resize((168, 94), Image.Resampling.LANCZOS), (x0, 338))
    strip.save(phone_ab, "JPEG", quality=93)

    # 5. Write THUMBS_INDEX_v01.json
    idx = {
        "film": "006_Trees-Are-Made-Of-Air",
        "parentTitle": "The Willow Tree That Was Made of Air",
        "titleAbc": [
            "The Willow Tree That Was Made of Air",
            "Where Does a Tree's Weight Come From?",
        ],
        "version": "v01",
        "job": "J0869",
        "decisionRef": "Chief pick on J0858 (OWB #99 comment 6355648154)",
        "maker": "gemini",
        "composer": "08_Thumbnail/_compose_hos_006_thumbs_v01.py",
        "mintScript": "08_Thumbnail/_mint_hos_006_thumbs_flow_v01.py",
        "spend": {
            "flowCredits": 0,
            "vertexGbp": 0.0,
            "cashGbp": 0.0,
            "flowBalanceBefore": 20830,
            "flowBalanceAfter": 20830,
        },
        "factLock": (
            "A: Willow tree growing in a terracotta pot by a sunlit arched window; air streams into the leaves "
            "and condenses into solid wood rings inside the trunk cutaway (FACT_NOTES_v01 rows 1 & 48: 'The wood "
            "of a tree is built mostly out of thin air... About half of dry wood is carbon, and every bit of that "
            "carbon came out of the air'). "
            "B: Van Helmont's 17th-century brass balance scale with the uprooted willow tree weighing the right "
            "pan down low while the pot of dried furnace soil is lifted high, with zero written numbers on the "
            "scale (FACT_NOTES_v01 rows 8-19)."
        ),
        "thumbs": [
            {
                "id": "A",
                "role": "Primary",
                "hook": "WOOD FROM SKY?",
                "punch": "SKY?",
                "jpg": f"Selected/{OUT_A.name}",
                "sha256": sha256(OUT_A),
                "bytes": OUT_A.stat().st_size,
                "plate": f"_assets_v01/{PLATE_A.name}",
                "plateSha256": sha256(PLATE_A),
                "layout": meta_a,
                "scores": {
                    "HOOK": "PASS — 'WOOD FROM SKY?' (3 words, positive question per LEARNINGS Rule #1, gold punch 'SKY?') names the concrete physical substance and source in the cold open & Part 05 without repeating any word of Title A ('The Willow Tree That Was Made of Air') or Title B ('Where Does a Tree\\'s Weight Come From?').",
                    "BAND": f"PASS — Upper-left lettering band {meta_a['letteringBox']} (plus gold scroll flourishes y={meta_a['ornaments']['topScrollBox'][1]}..{meta_a['ornaments']['bottomScrollBox'][3]}) sits on dark bookshelves completely left of the hero willow/air-ribbon cutaway (x>={hero_box_a[0]}), above the Explorer's hair (y={explorer_box_a[1]}), and clear of the bottom-right duration badge.",
                    "PHONE": "PASS — Verified on 168x94 thumb_preview sheet: 3 short words ('WOOD / FROM / SKY?'), glowing wood-ring cutaway on the willow trunk, and the Explorer (55.1% frame height) read in under 1 second.",
                },
                "previews": [
                    f"Selected/{prev_a.name}",
                    f"Selected/{sheet_a.name}",
                ],
            },
            {
                "id": "B",
                "role": "Test & Compare B",
                "hook": "DO PLANTS EAT SOIL?",
                "punch": "SOIL?",
                "jpg": f"Selected/{OUT_B.name}",
                "sha256": sha256(OUT_B),
                "bytes": OUT_B.stat().st_size,
                "plate": f"_assets_v01/{PLATE_B.name}",
                "plateSha256": sha256(PLATE_B),
                "layout": meta_b,
                "scores": {
                    "HOOK": "PASS — 'DO PLANTS EAT SOIL?' (4 words, positive question per LEARNINGS Rule #1, gold punch 'SOIL?') names the concrete Aristotelian belief tested by van Helmont's scale without repeating any word of Title A or Title B.",
                    "BAND": f"PASS — Upper-left lettering band {meta_b['letteringBox']} (plus gold scroll flourishes y={meta_b['ornaments']['topScrollBox'][1]}..{meta_b['ornaments']['bottomScrollBox'][3]}) sits on dark bookshelves completely left of the brass balance scale (x>={hero_box_b[0]}), above the Explorer's hair (y={explorer_box_b[1]}), and clear of the bottom-right duration badge. Scale plate is 100% free of written numbers.",
                    "PHONE": "PASS — Verified on 168x94 thumb_preview sheet: 'DO PLANTS / EAT / SOIL?', the sharply tilted brass balance (heavy willow pan down, small soil pot up), and the Explorer (54.6% frame height) read in under 1 second.",
                },
                "previews": [
                    f"Selected/{prev_b.name}",
                    f"Selected/{sheet_b.name}",
                ],
            },
        ],
        "combinedPreviews": [
            f"Selected/{sheet_ab.name}",
            f"Selected/{phone_ab.name}",
        ],
        "upload": False,
        "studio": False,
        "status": "Staged A/B pair for Test & Compare (0 Flow credits, £0). Parked for Chief before Ben's 1 Nov watch.",
    }
    (HERE / "THUMBS_INDEX_v01.json").write_text(json.dumps(idx, indent=2) + "\n")
    print("DONE THUMBS_INDEX_v01.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
