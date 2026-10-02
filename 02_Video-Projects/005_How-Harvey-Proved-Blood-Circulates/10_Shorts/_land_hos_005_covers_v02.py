#!/usr/bin/env python3
"""Land HOS 005 Shorts covers v02 (desk task from Claude, PR #180 comment 5949489005).

v02 matches the live covers (GALLIUM IN THE GAP, THE CARBOLIC SPRAY): the lettering stack across
the top, centred, the widest line about 88% of the width. Claude's call: the live set wins over
§4.2's centre band until the docs PR. Same scenes and lettering assets as v01 (covers_v01/_assets).

Then thumb_preview.py short and style_sheet.py short. Nothing to Studio.
"""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageFilter

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
ASSETS = HERE / "covers_v01" / "_assets"
OUT = HERE / "covers_v02"
TOOLS = ROOT / "00_Brand" / "Channel-Setup" / "tools"

W, H = 1080, 1920
WIDTH = 0.86                 # widest line, fraction of W (live covers: 85–90%)
STRETCH = 1.06               # horizontal stretch, so the tall lettering reaches WIDTH inside STACK_MAX_H
TOP = 0.045                  # stack top, fraction of H (live covers start 4–5% down)
STACK_MAX_H = 0.41 * H       # live stacks end by about 40–45% of the height
GAP = 10

# rel: each line's width relative to the widest (top cream, middle teal, bottom gold).
COVERS = {
    "s01_the_sum": {
        "scene": "hos_005_s01_scene_v01h.jpg",
        "letters": "hos_005_s01_letters_v01.jpg",
        "title": "Your Heart Pumps More Blood Than You Have",
        "words": ["MORE", "THAN YOU", "HAVE"],
        "rel": (0.72, 0.50, 1.0),
        "cx": 0.56,
    },
    "s02_the_tied_arm": {
        "scene": "hos_005_s02_scene_v01b.jpg",
        "letters": "hos_005_s02_letters_v01.jpg",
        "title": "One Tight Band Proved Your Blood Goes Round",
        "words": ["ONE", "TIGHT", "BAND"],
        "rel": (0.62, 0.50, 1.0),
        "cx": 0.60,
    },
    "s03_never_saw": {
        "scene": "hos_005_s03_scene_v01a.jpg",
        "letters": "hos_005_s03_letters_v01.jpg",
        "title": "The Blood Vessels Finer Than a Hair",
        "words": ["FINER", "THAN A", "HAIR"],
        "rel": (1.0, 0.55, 0.74),
        "cx": 0.60,
    },
}


def key_magenta(im: Image.Image) -> Image.Image:
    im = im.convert("RGB")
    w, h = im.size
    border = [im.getpixel((x, y)) for x in range(0, w, 8) for y in (2, h - 3)]
    border += [im.getpixel((x, y)) for y in range(0, h, 8) for x in (2, w - 3)]
    k = tuple(sorted(c[i] for c in border)[len(border) // 2] for i in range(3))
    out = Image.new("RGBA", im.size)
    src, dst = im.load(), out.load()
    lo, hi = 45.0, 120.0
    for y in range(h):
        for x in range(w):
            r, g, b = src[x, y]
            d = ((r - k[0]) ** 2 + (g - k[1]) ** 2 + (b - k[2]) ** 2) ** 0.5
            a = 0.0 if d <= lo else 1.0 if d >= hi else (d - lo) / (hi - lo)
            # The model's soft shadow on the key is a darker crimson (green near zero);
            # the letters' brown outline keeps g/r ≈ 0.45 or more.
            if r > 40:
                f = min(1.0, max(0.0, (0.40 - g / r) / 0.22))
                if f > 0:
                    a *= 1.0 - f
                    r, g, b = (int(c * (1 - f) + t * f) for c, t in zip((r, g, b), (40, 22, 8)))
            dst[x, y] = (r, g, b, int(a * 255))
    return out


def split_lines(rgba: Image.Image) -> list[Image.Image]:
    """Cut the stack into its three lines by face colour (cream / teal / gold); the
    extrudes of neighbouring lines can touch, so empty rows are not enough."""
    w, h = rgba.size
    px = rgba.load()
    kinds = {
        "cream": lambda r, g, b: r > 200 and g > 180 and b > 120,
        "teal": lambda r, g, b: g > 100 and b > 100 and r < 110,
        "gold": lambda r, g, b: r > 180 and 100 < g < 200 and b < 100,
    }
    rows = {k: [] for k in kinds}
    profile = []
    for y in range(h):
        n = {k: 0 for k in kinds}
        alpha = 0
        for x in range(0, w, 2):
            r, g, b, a = px[x, y]
            if a < 200:
                continue
            alpha += 1
            for k, f in kinds.items():
                if f(r, g, b):
                    n[k] += 1
        profile.append(alpha)
        for k in kinds:
            if n[k] > 10:
                rows[k].append(y)
    if not all(rows.values()):
        raise SystemExit(f"lettering colours not found: { {k: len(v) for k, v in rows.items()} }")

    def mid(k: str) -> int:
        return sorted(rows[k])[len(rows[k]) // 2]

    def cut(a: int, b: int) -> int:
        return min(range(a, b + 1), key=lambda y: profile[y])

    m_cream, m_teal, m_gold = mid("cream"), mid("teal"), mid("gold")
    if not m_cream < m_teal < m_gold:
        raise SystemExit(f"line order not cream/teal/gold: {m_cream} {m_teal} {m_gold}")
    c1 = cut(m_cream, m_teal)
    c2 = cut(m_teal, m_gold)
    top = next(y for y in range(h) if profile[y] > 3)
    bot = max(y for y in range(h) if profile[y] > 3) + 1
    segs = [(top, c1), (c1, c2), (c2, bot)]
    lines = []
    for y0, y1 in segs:
        crop = rgba.crop((0, y0, w, y1))
        lines.append(crop.crop(crop.getchannel("A").point(lambda v: 255 if v > 24 else 0).getbbox()))
    return lines


def stack(lines: list[Image.Image], rel_w: tuple[float, float, float]) -> tuple[Image.Image, dict]:
    ratios = [ln.height / ln.width for ln in lines]
    width = WIDTH * W
    height = sum(width * rel * r / STRETCH for rel, r in zip(rel_w, ratios)) + 2 * GAP
    if height > STACK_MAX_H:
        width *= (STACK_MAX_H - 2 * GAP) / (height - 2 * GAP)
    scaled = []
    for rel, ln in zip(rel_w, lines):
        lw = int(round(width * rel))
        lh = int(round(lw * ln.height / ln.width / STRETCH))
        scaled.append(ln.resize((lw, lh), Image.LANCZOS))
    sw = max(l.width for l in scaled)
    sh = sum(l.height for l in scaled) + 2 * GAP
    canvas = Image.new("RGBA", (sw, sh), (0, 0, 0, 0))
    y = 0
    for l in scaled:
        canvas.alpha_composite(l, ((sw - l.width) // 2, y))
        y += l.height + GAP
    return canvas, {}


def build(cid: str, spec: dict) -> dict:
    scene = Image.open(ASSETS / spec["scene"]).convert("RGB").resize((W, H), Image.LANCZOS)
    scene = scene.filter(ImageFilter.UnsharpMask(radius=1.6, percent=60, threshold=2))
    letters = key_magenta(Image.open(ASSETS / spec["letters"]))
    st, _ = stack(split_lines(letters), spec["rel"])
    x = (W - st.width) // 2
    y = int(round(TOP * H))
    shadow = Image.new("RGBA", st.size, (12, 6, 2, 0))
    shadow.putalpha(st.getchannel("A").point(lambda v: int(v * 0.6)).filter(ImageFilter.GaussianBlur(14)))
    base = scene.convert("RGBA")
    base.alpha_composite(shadow, (x + 6, y + 14))
    base.alpha_composite(st, (x, y))
    name = f"hos_005_{cid}_cover_v02.jpg"
    path = OUT / name
    base.convert("RGB").save(path, quality=92, subsampling=0)
    top, bot = y / H, (y + st.height) / H
    m = {
        "file": str(path.relative_to(ROOT)),
        "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        "title": spec["title"],
        "words": spec["words"],
        "scene": spec["scene"],
        "letters": spec["letters"],
        "stack_width_pct": round(100 * st.width / W, 1),
        "stack_x_pct": [round(100 * x / W, 1), round(100 * (x + st.width) / W, 1)],
        "stack_y_pct": [round(100 * top, 1), round(100 * bot, 1)],
    }
    print(f"  {name}  width {m['stack_width_pct']}%  x {m['stack_x_pct']}  y {m['stack_y_pct']}")
    return m


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    index = {"version": "covers_v02", "task": "PR #180 comment 5949489005", "covers": {}}
    for cid, spec in COVERS.items():
        index["covers"][cid] = build(cid, spec)
    files = [ROOT / c["file"] for c in index["covers"].values()]
    for f in files:
        prev = f.with_name(f.stem + "_preview.jpg")
        subprocess.run([sys.executable, str(TOOLS / "thumb_preview.py"), "short", str(f), "--out", str(prev)], check=True)
        index["covers"][f.stem.replace("hos_005_", "").replace("_cover_v02", "")]["preview"] = str(prev.relative_to(ROOT))
    sheet = OUT / "hos_005_shorts_covers_v02_style_sheet.jpg"
    subprocess.run([sys.executable, str(TOOLS / "style_sheet.py"), "short", *map(str, files), "--out", str(sheet)], check=True)
    index["style_sheet"] = str(sheet.relative_to(ROOT))
    (OUT / "COVERS_INDEX_v02.json").write_text(json.dumps(index, indent=2) + "\n")
    print("  INDEX", (OUT / "COVERS_INDEX_v02.json").relative_to(ROOT))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
