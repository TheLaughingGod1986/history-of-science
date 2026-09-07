#!/usr/bin/env python3
"""Post-scrub glowing house / model-town props from Part 04 plate mp4 (book top).

Veo remints often regenerate glowing yellow house props. Keep Veo desk/card motion
and paint opaque leather over a fixed book-top prop region every frame.
"""
from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter

# Default: 02b glowing props on leather books (measured from v02 fail stills)
BOOK_PROP_BOX = (0.68, 0.38, 0.88, 0.58)


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


def scrub_frame(im: Image.Image, box_frac=BOOK_PROP_BOX) -> Image.Image:
    rgb = im.convert("RGB")
    w, h = rgb.size
    x0 = int(w * box_frac[0])
    y0 = int(h * box_frac[1])
    x1 = int(w * box_frac[2])
    y1 = int(h * box_frac[3])

    samples = []
    sy0 = min(h - 2, y1 + 4)
    sy1 = min(h - 1, y1 + 28)
    sx0 = max(0, x0 + 8)
    sx1 = min(w - 1, x1 - 8)
    for y in range(sy0, sy1):
        for x in range(sx0, sx1, 3):
            r, g, b = rgb.getpixel((x, y))
            if r > 190 and g > 150 and b < 130:
                continue
            samples.append((r, g, b))
    leather = (
        tuple(sum(c[i] for c in samples) // len(samples) for i in range(3))
        if samples
        else (92, 58, 38)
    )

    cover = Image.new("RGB", (w, h), leather)
    cd = ImageDraw.Draw(cover)
    mid_y = (y0 + y1) // 2
    strap = tuple(max(0, c - 18) for c in leather)
    cd.rectangle((x0, mid_y - 3, x1, mid_y + 3), fill=strap)
    highlight = tuple(min(255, c + 22) for c in leather)
    cd.rectangle((x0 + 6, y0 + 4, x1 - 6, y0 + 10), fill=highlight)

    mask = Image.new("L", (w, h), 0)
    ImageDraw.Draw(mask).rounded_rectangle((x0, y0, x1, y1), radius=10, fill=255)
    soft = mask.filter(ImageFilter.GaussianBlur(radius=2.0))
    return Image.composite(cover, rgb, soft)


def scrub_mp4(src: Path, dest: Path, box_frac=BOOK_PROP_BOX) -> None:
    if not src.exists():
        raise SystemExit(f"missing {src}")
    dur = probe_dur(src)
    with tempfile.TemporaryDirectory(prefix="hos_p04_books_") as td:
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
            f"hard-fill book props {len(paths)} frames {src.name} "
            f"box={box_frac} dur={dur:.2f}",
            flush=True,
        )
        for i, fp in enumerate(paths):
            scrub_frame(Image.open(fp), box_frac).save(fp)
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
            "usage: _scrub_part04_plate_book_props_v03.py <src.mp4> <dest.mp4>"
        )
    scrub_mp4(Path(sys.argv[1]), Path(sys.argv[2]))


if __name__ == "__main__":
    main()
