#!/usr/bin/env python3
"""Land the HOS 005 Short s04 cover, 'Is the Heart a Pump?' (OWB queue J0230), in the covers_v02 style.

Same lettering stack as the live 005 covers (`_land_hos_005_covers_v02.py`: across the top, widest line
about 86%, cream/teal/gold), keyed from a lettering stack painted on flat magenta in covers_v02/_assets/.
The scene is the Short's own opening plate (part02 05_heart_stove_t1 at 0.3 s): a 1000 px wide crop
around the heart and stove (upscale 1.08x), set low in the frame so the stack sits over the room, with a
blurred, feathered extension of the plate's own wall above it. Nothing to Studio.

Then thumb_preview.py short and style_sheet.py short, and the s04 entry in COVERS_INDEX_v02.json.
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
OUT = HERE / "covers_v02"
ASSETS = OUT / "_assets"
TOOLS = ROOT / "00_Brand" / "Channel-Setup" / "tools"

spec = importlib.util.spec_from_file_location("c005", HERE / "_land_hos_005_covers_v02.py")
c005 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(c005)
W, H = c005.W, c005.H

CID = "s04_galen_stove"
SPEC = {
    "scene": "hos_005_s04_scene_v02.png",  # ffmpeg -ss 0.3 -i 05_heart_stove_t1.mp4 -frames:v 1
    "scene_source": "04_Generated-Clips/part02/raw/v01/05_heart_stove_t1.mp4 @ 0.3 s",
    "letters": "hos_005_s04_letters_v02.jpg",
    "title": "Is the Heart a Pump?",
    "words": ["IS THE", "HEART A", "PUMP?"],
    "rel": (0.84, 0.74, 1.0),
}
CROP_X0, CROP_W = 280, 1000   # source x range around the heart and stove (source centre ~780)
SEAM = 200                    # feather height between the wall extension and the plate


def scene_canvas(src: Image.Image) -> Image.Image:
    plate = src.crop((CROP_X0, 0, CROP_X0 + CROP_W, src.height))
    ph = round(plate.height * W / plate.width)
    plate = plate.resize((W, ph), Image.LANCZOS)
    top = H - ph
    wall = src.crop((CROP_X0, 0, CROP_X0 + CROP_W, src.height // 3)).resize((W, top + SEAM), Image.LANCZOS)
    wall = wall.filter(ImageFilter.GaussianBlur(18))
    canvas = Image.new("RGB", (W, H))
    canvas.paste(wall, (0, 0))
    mask = Image.new("L", (W, ph), 255)
    grad = Image.linear_gradient("L").resize((W, SEAM))
    mask.paste(grad, (0, 0))
    canvas.paste(plate, (0, top), mask)
    return canvas.filter(ImageFilter.UnsharpMask(radius=1.6, percent=60, threshold=2))


def build() -> dict:
    scene = scene_canvas(Image.open(ASSETS / SPEC["scene"]).convert("RGB"))
    letters = c005.key_magenta(Image.open(ASSETS / SPEC["letters"]))
    st, _ = c005.stack(c005.split_lines(letters), SPEC["rel"])
    x, y = (W - st.width) // 2, int(round(c005.TOP * H))
    shadow = Image.new("RGBA", st.size, (12, 6, 2, 0))
    shadow.putalpha(st.getchannel("A").point(lambda v: int(v * 0.6)).filter(ImageFilter.GaussianBlur(14)))
    base = scene.convert("RGBA")
    base.alpha_composite(shadow, (x + 6, y + 14))
    base.alpha_composite(st, (x, y))
    path = OUT / f"hos_005_{CID}_cover_v02.jpg"
    base.convert("RGB").save(path, quality=92, subsampling=0)
    m = {
        "file": str(path.relative_to(ROOT)),
        "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        "title": SPEC["title"],
        "words": SPEC["words"],
        "scene": SPEC["scene"],
        "scene_source": SPEC["scene_source"],
        "letters": SPEC["letters"],
        "stack_width_pct": round(100 * st.width / W, 1),
        "stack_x_pct": [round(100 * x / W, 1), round(100 * (x + st.width) / W, 1)],
        "stack_y_pct": [round(100 * y / H, 1), round(100 * (y + st.height) / H, 1)],
        "job": "J0230",
    }
    print(f"  {path.name}  width {m['stack_width_pct']}%  x {m['stack_x_pct']}  y {m['stack_y_pct']}")
    return m


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    m = build()
    f = ROOT / m["file"]
    prev = f.with_name(f.stem + "_preview.jpg")
    subprocess.run([sys.executable, str(TOOLS / "thumb_preview.py"), "short", str(f), "--out", str(prev)], check=True)
    m["preview"] = str(prev.relative_to(ROOT))
    covers = sorted(OUT.glob("hos_005_s0*_cover_v02.jpg"))
    sheet = OUT / "hos_005_shorts_covers_v02_s04_style_sheet.jpg"
    subprocess.run([sys.executable, str(TOOLS / "style_sheet.py"), "short", *map(str, covers), "--out", str(sheet)], check=True)
    m["style_sheet"] = str(sheet.relative_to(ROOT))
    idx_path = OUT / "COVERS_INDEX_v02.json"
    index = json.loads(idx_path.read_text())
    index["covers"][CID] = m
    idx_path.write_text(json.dumps(index, indent=2) + "\n")
    print("  INDEX", idx_path.relative_to(ROOT))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
