#!/usr/bin/env python3
"""Land HOS 002 thumbs restyled to the LIVE 001 listing grammar.

Live long `_C92tIJCk8A` is 001 Thumb A flask: object is hero (~right 2/3),
Explorer is small lower-left garnish, title painted in on the left.
Do not use 001 README-recommended B (Explorer peek) as the listing lock.

Sources are generated PNGs under the worker artifacts folder. Outputs:
  1280x720 JPEG long ABC  (Studio, <2 MB)
  1080x1920 JPEG Shorts covers
v01 character-hero / film-frame covers stay on disk as trail.
"""
from __future__ import annotations

from pathlib import Path

from PIL import Image

HERE = Path(__file__).resolve().parent
SELECTED = HERE / "Selected"
SHORTS = HERE / "Shorts"
ASSETS = Path("/Users/benjaminoats/.local/share/cursor-mac-mini-hos-worker/artifacts/assets")

LONG = [
    ("hos_002_thumb_A_gallium_live_v02b.png", "hos_002_thumb_A_gallium_live_v02", (1280, 720)),
    ("hos_002_thumb_B_empty_seats_live_v02.png", "hos_002_thumb_B_empty_seats_live_v02", (1280, 720)),
    ("hos_002_thumb_C_empty_slot_live_v02b.png", "hos_002_thumb_C_empty_slot_live_v02", (1280, 720)),
]
SHORT = [
    ("hos_002_s01_empty_chairs_cover_live_v02.png", "hos_002_s01_empty_chairs_cover_live_v02", (1080, 1920)),
    ("hos_002_s02_predict_metal_cover_live_v02.png", "hos_002_s02_predict_metal_cover_live_v02", (1080, 1920)),
    ("hos_002_s03_gallium_cover_live_v02.png", "hos_002_s03_gallium_cover_live_v02", (1080, 1920)),
    ("hos_002_s04_tellurium_cover_live_v02.png", "hos_002_s04_tellurium_cover_live_v02", (1080, 1920)),
    ("hos_002_s05_other_table_cover_live_v02b.png", "hos_002_s05_other_table_cover_live_v02", (1080, 1920)),
]


def land(src_name: str, stem: str, size: tuple[int, int], dest_dir: Path) -> None:
    src = ASSETS / src_name
    if not src.exists():
        raise SystemExit(f"missing {src}")
    im = Image.open(src).convert("RGB")
    im = im.resize(size, Image.Resampling.LANCZOS)
    dest_dir.mkdir(parents=True, exist_ok=True)
    png = dest_dir / f"{stem}.png"
    jpg = dest_dir / f"{stem}.jpg"
    im.save(png, "PNG")
    q = 88
    im.save(jpg, "JPEG", quality=q, optimize=True)
    while jpg.stat().st_size > 1_900_000 and q > 70:
        q -= 4
        im.save(jpg, "JPEG", quality=q, optimize=True)
    print(f"  {jpg.name}  {jpg.stat().st_size}  {im.size}  q={q}", flush=True)


def main() -> None:
    print("LONG", flush=True)
    for src, stem, size in LONG:
        land(src, stem, size, SELECTED)
    print("SHORTS", flush=True)
    for src, stem, size in SHORT:
        land(src, stem, size, SHORTS)
    print("DONE", flush=True)


if __name__ == "__main__":
    main()
