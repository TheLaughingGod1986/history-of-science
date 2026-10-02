#!/usr/bin/env python3
"""Land the back-catalogue Shorts covers (Sun 1 Nov → 004, Tue 3 Nov → 002), desk PR #180 comment 5950150517.

The live layout, as 005 covers v02 (`005_…/10_Shorts/_land_hos_005_covers_v02.py`): the lettering stack
centred across the top, starting about 4.5% down, widest line 86% of the width. Each cover is a painted
scene with no text plus a lettering stack on flat magenta (both from the image model, in each film's
`10_Shorts/covers_backcat_v01/_assets/`); the magenta is keyed out and the lines stacked here.
`rel`: each line's width relative to the widest (top cream, middle teal, bottom gold), as 005. Then thumb_preview.py short and style_sheet.py short.
Nothing to Studio.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageFilter

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
TOOLS = ROOT / "00_Brand" / "Channel-Setup" / "tools"
F005 = Path("/Users/benjaminoats/YouTube/hos-005-blood/02_Video-Projects/005_How-Harvey-Proved-Blood-Circulates/"
            "10_Shorts/_land_hos_005_covers_v02.py")

W, H = 1080, 1920
WIDTH = 0.86
STRETCH = 1.06
TOP = 0.045
STACK_MAX_H = 0.41 * H
GAP = 10

COVERS = {
    "004_gold_foil": {
        "dir": ROOT / "02_Video-Projects/004_Whats-Really-Inside-An-Atom/10_Shorts/covers_backcat_v01",
        "name": "hos_004_backcat_gold_foil_cover_v01.jpg",
        "scene": "hos_004_backcat_scene_v01.jpg", "letters": "hos_004_backcat_letters_v01.jpg",
        "title": "Why Gold Foil Bounced Rutherford's Particles Back", "words": ["GOLD", "THREW IT", "BACK"],
        "rel": (0.74, 0.62, 1.0),
    },
    "002_four_elements": {
        "dir": ROOT / "02_Video-Projects/002_How-Did-We-Discover-The-Periodic-Table/10_Shorts/covers_backcat_v01",
        "name": "hos_002_backcat_four_elements_cover_v01.jpg",
        "scene": "hos_002_backcat_scene_v01.jpg", "letters": "hos_002_backcat_letters_v01.jpg",
        "title": "The Four Elements Were Wrong", "words": ["FOUR", "ELEMENTS WERE", "WRONG"],
        "rel": (0.78, 0.86, 1.0),
    },
}


def load_005():
    spec = importlib.util.spec_from_file_location("c005", F005)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def stack(lines: list[Image.Image], rel_w: tuple[float, float, float]) -> Image.Image:
    width = WIDTH * W
    height = sum(width * rel * ln.height / ln.width / STRETCH for rel, ln in zip(rel_w, lines)) + 2 * GAP
    if height > STACK_MAX_H:
        width *= (STACK_MAX_H - 2 * GAP) / (height - 2 * GAP)
    scaled = []
    for rel, ln in zip(rel_w, lines):
        lw = int(round(width * rel))
        scaled.append(ln.resize((lw, int(round(lw * ln.height / ln.width / STRETCH))), Image.LANCZOS))
    canvas = Image.new("RGBA", (max(l.width for l in scaled), sum(l.height for l in scaled) + 2 * GAP), (0, 0, 0, 0))
    y = 0
    for l in scaled:
        canvas.alpha_composite(l, ((canvas.width - l.width) // 2, y))
        y += l.height + GAP
    return canvas


def build(c005, cid: str, spec: dict) -> dict:
    assets = spec["dir"] / "_assets"
    scene = Image.open(assets / spec["scene"]).convert("RGB").resize((W, H), Image.LANCZOS)
    scene = scene.filter(ImageFilter.UnsharpMask(radius=1.6, percent=60, threshold=2))
    st = stack(c005.split_lines(c005.key_magenta(Image.open(assets / spec["letters"]))), spec["rel"])
    x, y = (W - st.width) // 2, int(round(TOP * H))
    shadow = Image.new("RGBA", st.size, (12, 6, 2, 0))
    shadow.putalpha(st.getchannel("A").point(lambda v: int(v * 0.6)).filter(ImageFilter.GaussianBlur(14)))
    base = scene.convert("RGBA")
    base.alpha_composite(shadow, (x + 6, y + 14))
    base.alpha_composite(st, (x, y))
    path = spec["dir"] / spec["name"]
    base.convert("RGB").save(path, quality=92, subsampling=0)
    m = {"file": str(path.relative_to(ROOT)), "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
         "title": spec["title"], "words": spec["words"], "scene": spec["scene"], "letters": spec["letters"],
         "stack_width_pct": round(100 * st.width / W, 1),
         "stack_x_pct": [round(100 * x / W, 1), round(100 * (x + st.width) / W, 1)],
         "stack_y_pct": [round(100 * y / H, 1), round(100 * (y + st.height) / H, 1)]}
    print(f"  {spec['name']}  width {m['stack_width_pct']}%  x {m['stack_x_pct']}  y {m['stack_y_pct']}")
    prev = path.with_name(path.stem + "_preview.jpg")
    subprocess.run([sys.executable, str(TOOLS / "thumb_preview.py"), "short", str(path), "--out", str(prev)], check=True)
    m["preview"] = str(prev.relative_to(ROOT))
    return m


def main() -> int:
    c005 = load_005()
    index = {"version": "covers_backcat_v01", "task": "PR #180 comment 5950150517", "covers": {}}
    for cid, spec in COVERS.items():
        spec["dir"].mkdir(parents=True, exist_ok=True)
        index["covers"][cid] = build(c005, cid, spec)
    files = [ROOT / c["file"] for c in index["covers"].values()]
    sheet = COVERS["004_gold_foil"]["dir"] / "hos_backcat_nov_covers_v01_style_sheet.jpg"
    subprocess.run([sys.executable, str(TOOLS / "style_sheet.py"), "short", *map(str, files), "--out", str(sheet)],
                   check=True)
    index["style_sheet"] = str(sheet.relative_to(ROOT))
    for spec in COVERS.values():
        (spec["dir"] / "COVERS_INDEX_BACKCAT_v01.json").write_text(json.dumps(index, indent=2) + "\n")
    print("  style sheet", index["style_sheet"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
