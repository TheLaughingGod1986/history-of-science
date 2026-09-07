#!/usr/bin/env python3
"""Post-scrub model-town houses from Part 04 plate mp4 via hard window fill.

Veo remints often regenerate glowing yellow-window houses. This keeps Veo desk
motion and paints an opaque night-sky+moon over a fixed window glass region.
"""
from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter

# plate_id substring → (x0,y0,x1,y1) fractions + moon (mx,my) fractions
# v02: deepen 05 y1 past glowing house leak under PERIODIC TABLE / EMPTY SEATS (~40–45s)
WINDOW_BOXES = {
    "05_columns": ((0.10, 0.00, 0.995, 0.62), (0.55, 0.14)),
    "06_explorer": ((0.32, 0.00, 0.995, 0.62), (0.78, 0.10)),
    "default": ((0.18, 0.00, 0.90, 0.48), (0.55, 0.12)),
}


def probe_dur(path: Path) -> float:
    return float(
        subprocess.check_output(
            [
                "ffprobe", "-v", "error", "-show_entries", "format=duration",
                "-of", "default=nw=1:nk=1", str(path),
            ],
            text=True,
        ).strip()
    )


def pick_box(name: str):
    low = name.lower()
    for key, val in WINDOW_BOXES.items():
        if key in low:
            return val
    return WINDOW_BOXES["default"]


def hard_fill_window(im: Image.Image, box_frac, moon_frac) -> Image.Image:
    rgb = im.convert("RGB")
    w, h = rgb.size
    x0 = int(w * box_frac[0])
    y0 = int(h * box_frac[1])
    x1 = int(w * box_frac[2])
    y1 = int(h * box_frac[3])

    sky = Image.new("RGB", (w, h), (24, 38, 80))
    sd = ImageDraw.Draw(sky)
    mx, my = int(w * moon_frac[0]), int(h * moon_frac[1])
    rad = max(18, int(min(w, h) * 0.032))
    sd.ellipse((mx - rad, my - rad, mx + rad, my + rad), fill=(236, 236, 250))
    for sx, sy in (
        (mx - rad * 2.6, my + 10),
        (mx + rad * 1.9, my - 6),
        (mx + 10, my + rad * 1.7),
        (mx - rad * 0.8, my + rad * 2.1),
    ):
        sd.ellipse((int(sx), int(sy), int(sx) + 2, int(sy) + 2), fill=(220, 225, 240))

    # Hard opaque fill — soft blur at the bottom edge previously leaked yellow windows.
    mask = Image.new("L", (w, h), 0)
    ImageDraw.Draw(mask).rectangle((x0, y0, x1, y1), fill=255)
    soft = mask.filter(ImageFilter.GaussianBlur(radius=1.2))
    inset = Image.new("L", (w, h), 0)
    # Keep bottom edge hard (no soft fade into house glow)
    ImageDraw.Draw(inset).rectangle((x0 + 3, y0 + 3, x1 - 3, y1), fill=255)
    mask = Image.composite(inset, soft, inset)
    return Image.composite(sky, rgb, mask)


def scrub_mp4(src: Path, dest: Path) -> None:
    if not src.exists():
        raise SystemExit(f"missing {src}")
    box_frac, moon_frac = pick_box(src.name + dest.name)
    dur = probe_dur(src)
    with tempfile.TemporaryDirectory(prefix="hos_p04_win_") as td:
        frames = Path(td) / "frames"
        frames.mkdir()
        subprocess.run(
            [
                "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
                "-i", str(src), "-vf", "fps=24",
                str(frames / "f_%05d.png"),
            ],
            check=True,
        )
        paths = sorted(frames.glob("f_*.png"))
        print(
            f"hard-fill window {len(paths)} frames {src.name} "
            f"box={box_frac} dur={dur:.2f}",
            flush=True,
        )
        for i, fp in enumerate(paths):
            hard_fill_window(Image.open(fp), box_frac, moon_frac).save(fp)
            if i % 48 == 0:
                print(f"  frame {i}/{len(paths)}", flush=True)
        tmp = dest.with_suffix(".scrub.tmp.mp4")
        subprocess.run(
            [
                "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
                "-framerate", "24", "-i", str(frames / "f_%05d.png"),
                "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18",
                "-an", str(tmp),
            ],
            check=True,
        )
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.unlink(missing_ok=True)
        shutil.move(str(tmp), str(dest))
        print(f"SAVED {dest} bytes={dest.stat().st_size} dur={probe_dur(dest):.2f}", flush=True)


def main() -> None:
    if len(sys.argv) < 3:
        raise SystemExit("usage: _scrub_part04_plate_window_v02.py <src.mp4> <dest.mp4>")
    scrub_mp4(Path(sys.argv[1]), Path(sys.argv[2]))


if __name__ == "__main__":
    main()
