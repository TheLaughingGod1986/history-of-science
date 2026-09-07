#!/usr/bin/env python3
"""Post-scrub book tops with HARD rectangular leather only (v04).

Never adaptive / house-contour fills — that left peaked-roof masks in v03.
Use only if Veo remint still shows house tokens; prefer real Veo first.
"""
from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter

BOOK_BOX = (0.62, 0.18, 0.98, 0.58)


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


def scrub_frame(im: Image.Image, box_frac=BOOK_BOX) -> Image.Image:
    rgb = im.convert("RGB")
    w, h = rgb.size
    x0 = int(w * box_frac[0])
    y0 = int(h * box_frac[1])
    x1 = int(w * box_frac[2])
    y1 = int(h * box_frac[3])

    samples: list[tuple[int, int, int]] = []
    for y in range(min(h - 1, y1 + 2), min(h - 1, y1 + 36)):
        for x in range(x0 + 10, x1 - 10, 2):
            r, g, b = rgb.getpixel((x, y))
            if r > 200 and g > 170 and b < 140:
                continue
            if r > 210 and g > 210 and b > 200:
                continue
            samples.append((r, g, b))
    fill = (
        tuple(sum(c[i] for c in samples) // len(samples) for i in range(3))
        if samples
        else (96, 62, 42)
    )

    cover = Image.new("RGB", (w, h), fill)
    cd = ImageDraw.Draw(cover)
    mid_y = (y0 + y1) // 2
    strap = tuple(max(0, c - 16) for c in fill)
    hi = tuple(min(255, c + 18) for c in fill)
    cd.rectangle((x0 + 8, mid_y - 3, x1 - 8, mid_y + 3), fill=strap)
    cd.rectangle((x0 + 10, y0 + 8, x1 - 10, y0 + 16), fill=hi)

    mask = Image.new("L", (w, h), 0)
    ImageDraw.Draw(mask).rounded_rectangle((x0, y0, x1, y1), radius=12, fill=255)
    soft = mask.filter(ImageFilter.GaussianBlur(radius=1.6))
    return Image.composite(cover, rgb, soft)


def scrub_mp4(src: Path, dest: Path) -> None:
    if not src.exists():
        raise SystemExit(f"missing {src}")
    dur = probe_dur(src)
    with tempfile.TemporaryDirectory(prefix="hos_p04_books_v04_") as td:
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
            f"RECT leather book scrub {len(paths)} frames {src.name} dur={dur:.2f}",
            flush=True,
        )
        for i, fp in enumerate(paths):
            scrub_frame(Image.open(fp)).save(fp)
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
        raise SystemExit(
            "usage: _scrub_part04_plate_books_rect_v04.py <src.mp4> <dest.mp4>"
        )
    scrub_mp4(Path(sys.argv[1]), Path(sys.argv[2]))


if __name__ == "__main__":
    main()
