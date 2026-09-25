#!/usr/bin/env python3
"""Post-scrub glowing house / model-town props from Part 04 plate mp4 (book/shelf).

Detect vivid yellow house-glow tokens per frame on the right desk/shelf band and
paint local leather/wood over a dilated mask. Keeps Veo desk/card motion.
"""
from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter


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


def is_house_glow(r: int, g: int, b: int) -> bool:
    """Vivid yellow house tokens — not warm lamp brown / orange flask liquid."""
    if r < 210 or g < 170:
        return False
    if b > 140:
        return False
    if (r - b) < 100 or (g - b) < 60:
        return False
    if r > g + 55:  # orange flask
        return False
    return True


def scrub_frame(im: Image.Image) -> Image.Image:
    rgb = im.convert("RGB")
    w, h = rgb.size
    # Right desk + shelf band where house props live on 02b
    x0, x1 = int(w * 0.55), w
    y0, y1 = int(h * 0.02), int(h * 0.72)

    mask = Image.new("L", (w, h), 0)
    md = ImageDraw.Draw(mask)

    # HARD rectangular book-top cover — never leave house-shaped leather silhouettes
    book_box = (
        int(w * 0.68),
        int(h * 0.34),
        int(w * 0.93),
        int(h * 0.62),
    )
    md.rounded_rectangle(book_box, radius=14, fill=255)

    # Plus any vivid yellow house-glow tokens elsewhere on right (shelf / sticks)
    glow_pts: list[tuple[int, int]] = []
    for y in range(y0, y1):
        for x in range(x0, x1):
            r, g, b = rgb.getpixel((x, y))
            if is_house_glow(r, g, b):
                glow_pts.append((x, y))
                md.ellipse((x - 4, y - 4, x + 4, y + 4), fill=255)

    soft = mask.filter(ImageFilter.MaxFilter(7)).filter(ImageFilter.GaussianBlur(radius=2.0))

    # Sample leather from book body just below the hard box
    samples: list[tuple[int, int, int]] = []
    bx0, by0, bx1, by1 = book_box
    for y in range(min(h - 1, by1 + 4), min(h - 1, by1 + 28)):
        for x in range(bx0 + 10, bx1 - 10, 2):
            r, g, b = rgb.getpixel((x, y))
            if is_house_glow(r, g, b):
                continue
            samples.append((r, g, b))
    for x, y in glow_pts[:: max(1, len(glow_pts) // 60 or 1)]:
        for dy, dx in ((20, 0), (28, -10), (28, 10)):
            sx, sy = min(w - 1, max(0, x + dx)), min(h - 1, max(0, y + dy))
            if soft.getpixel((sx, sy)) > 40:
                continue
            r, g, b = rgb.getpixel((sx, sy))
            if is_house_glow(r, g, b):
                continue
            samples.append((r, g, b))
    fill = (
        tuple(sum(c[i] for c in samples) // len(samples) for i in range(3))
        if samples
        else (92, 58, 38)
    )

    cover = Image.new("RGB", (w, h), fill)
    cd = ImageDraw.Draw(cover)
    # Flat book-top leather + one strap — rectangular, not house-contour
    strap = tuple(max(0, c - 18) for c in fill)
    hi = tuple(min(255, c + 18) for c in fill)
    mid_y = (by0 + by1) // 2
    cd.rectangle((bx0 + 8, mid_y - 3, bx1 - 8, mid_y + 3), fill=strap)
    cd.rectangle((bx0 + 10, by0 + 8, bx1 - 10, by0 + 16), fill=hi)

    return Image.composite(cover, rgb, soft)


def scrub_mp4(src: Path, dest: Path) -> None:
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
        print(f"adaptive book-prop scrub {len(paths)} frames {src.name} dur={dur:.2f}", flush=True)
        glow_frames = 0
        for i, fp in enumerate(paths):
            out = scrub_frame(Image.open(fp))
            # count residual glow in right band for logging
            w, h = out.size
            residual = 0
            for y in range(int(h * 0.02), int(h * 0.72), 2):
                for x in range(int(w * 0.55), w, 2):
                    if is_house_glow(*out.getpixel((x, y))):
                        residual += 1
            if residual:
                glow_frames += 1
            out.save(fp)
            if i % 48 == 0:
                print(f"  frame {i}/{len(paths)} residual_glow≈{residual}", flush=True)
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
        print(
            f"SAVED {dest} bytes={dest.stat().st_size} dur={probe_dur(dest):.2f} "
            f"frames_with_residual_glow={glow_frames}/{len(paths)}",
            flush=True,
        )


def main() -> None:
    if len(sys.argv) < 3:
        raise SystemExit(
            "usage: _scrub_part04_plate_book_props_v03.py <src.mp4> <dest.mp4>"
        )
    scrub_mp4(Path(sys.argv[1]), Path(sys.argv[2]))


if __name__ == "__main__":
    main()
