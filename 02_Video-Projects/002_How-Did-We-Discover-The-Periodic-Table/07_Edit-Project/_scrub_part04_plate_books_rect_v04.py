#!/usr/bin/env python3
"""Post-scrub book tops with FIXED rectangular leather slabs (v04).

No adaptive / glow-contour expansion (that left house-shaped masks in v03 and
over-matched lamp/flask yellow). Fixed flat rectangles only over known
book-top + upper-shelf house-token zones.
"""
from __future__ import annotations

import random
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageEnhance

# One continuous flat slab covering book tops + shelf house tokens (no gap)
BOXES = [
    (0.68, 0.00, 1.0, 0.56),
]


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


def is_house_glow_right(r: int, g: int, b: int) -> bool:
    """Tight yellow house-token detector (right band only callers)."""
    if r < 220 or g < 185:
        return False
    if b > 120:
        return False
    if (r - b) < 120 or (g - b) < 80:
        return False
    if abs(r - g) > 35:  # pure yellow, not orange flask
        return False
    return True


def paint_rect(im: Image.Image, box_frac, rng: random.Random) -> Image.Image:
    rgb = im.convert("RGB")
    w, h = rgb.size
    x0 = int(w * box_frac[0])
    y0 = int(h * box_frac[1])
    x1 = int(w * box_frac[2])
    y1 = int(h * box_frac[3])

    samples: list[tuple[int, int, int]] = []
    for y in range(min(h - 1, y1 + 2), min(h - 1, y1 + 36)):
        for x in range(max(0, x0 + 6), min(w - 1, x1 - 6), 2):
            r, g, b = rgb.getpixel((x, y))
            if r > 210 and g > 180 and b < 140:
                continue
            if r > 210 and g > 210 and b > 200:
                continue
            samples.append((r, g, b))
    base = (
        tuple(sum(c[i] for c in samples) // len(samples) for i in range(3))
        if samples
        else (108, 70, 48)
    )

    cover = Image.new("RGB", (w, h), base)
    cd = ImageDraw.Draw(cover)
    bw, bh = max(1, x1 - x0), max(1, y1 - y0)
    noise = Image.new("RGB", (bw, bh))
    nd = ImageDraw.Draw(noise)
    for yy in range(0, bh, 2):
        for xx in range(0, bw, 2):
            j = rng.randint(-12, 12)
            col = tuple(max(0, min(255, base[i] + j)) for i in range(3))
            nd.rectangle((xx, yy, xx + 1, yy + 1), fill=col)
    noise = noise.filter(ImageFilter.GaussianBlur(radius=1.0))
    cover.paste(noise, (x0, y0))
    strap = tuple(max(0, c - 16) for c in base)
    hi = tuple(min(255, c + 14) for c in base)
    mid_y = (y0 + y1) // 2
    cd.rectangle((x0 + 8, mid_y - 2, x1 - 8, mid_y + 2), fill=strap)
    cd.rectangle((x0 + 10, y0 + 8, x1 - 10, y0 + 14), fill=hi)
    for k in range(1, 3):
        ey = y0 + int(bh * k / 3)
        cd.line((x0 + 6, ey, x1 - 6, ey), fill=tuple(max(0, c - 8) for c in base), width=1)

    mask = Image.new("L", (w, h), 0)
    ImageDraw.Draw(mask).rectangle((x0, y0, x1, y1), fill=255)  # FLAT — no rounded peaks
    # Hard fill inside; tiny edge soften only (prevents glow bleed under soft mask)
    soft = mask.filter(ImageFilter.GaussianBlur(radius=0.6))
    inset = Image.new("L", (w, h), 0)
    ImageDraw.Draw(inset).rectangle((x0 + 1, y0 + 1, x1 - 1, y1 - 1), fill=255)
    mask = Image.composite(inset, soft, inset)
    return Image.composite(cover, rgb, mask)


def scrub_frame_fixed(im: Image.Image) -> Image.Image:
    out = im.convert("RGB")
    rng = random.Random(42)
    for box in BOXES:
        out = paint_rect(out, box, rng)
    return ImageEnhance.Color(out).enhance(0.99)


def residual_right_glow(im: Image.Image) -> int:
    rgb = im.convert("RGB")
    w, h = rgb.size
    n = 0
    for y in range(0, int(h * 0.60), 2):
        for x in range(int(w * 0.68), w, 2):
            if is_house_glow_right(*rgb.getpixel((x, y))):
                n += 1
    return n


def scrub_mp4(src: Path, dest: Path) -> None:
    if not src.exists():
        raise SystemExit(f"missing {src}")
    dur = probe_dur(src)
    with tempfile.TemporaryDirectory(prefix="hos_p04_books_v04f_") as td:
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
            f"FIXED rect leather scrub {len(paths)} frames {src.name} dur={dur:.2f}",
            flush=True,
        )
        residual_frames = 0
        for i, fp in enumerate(paths):
            out = scrub_frame_fixed(Image.open(fp))
            residual = residual_right_glow(out)
            if residual:
                residual_frames += 1
            out.save(fp)
            if i % 48 == 0:
                print(f"  frame {i}/{len(paths)} residual_right_glow≈{residual}", flush=True)
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
            f"frames_with_residual_glow={residual_frames}/{len(paths)}",
            flush=True,
        )


def main() -> None:
    if len(sys.argv) < 3:
        raise SystemExit(
            "usage: _scrub_part04_plate_books_rect_v04.py <src.mp4> <dest.mp4>"
        )
    scrub_mp4(Path(sys.argv[1]), Path(sys.argv[2]))


if __name__ == "__main__":
    main()
