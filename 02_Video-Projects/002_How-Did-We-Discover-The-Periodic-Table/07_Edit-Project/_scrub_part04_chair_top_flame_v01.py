#!/usr/bin/env python3
"""Surgical chair-top flame scrub for Part 04 Empty Chairs plates.

Keeps soft rectangular backrest PANEL glow; removes orange/yellow fire tongues
on the chair TOP rail and lamp smoke wisps. Used when Flow I2V reintroduces
flame despite a clean start frame.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import tempfile
from pathlib import Path

from PIL import Image, ImageFilter


def scrub_frame(im: Image.Image) -> Image.Image:
    rgb = im.convert("RGB")
    w, h = rgb.size
    pix = rgb.load()
    # Sample plain wood near chair frame for inpaint color
    wood_samples = []
    for y in range(int(h * 0.18), int(h * 0.32), 8):
        for x in (int(w * 0.36), int(w * 0.64)):
            wood_samples.append(pix[x, y])
    if not wood_samples:
        wood_samples = [(90, 60, 35)]
    wr = sum(c[0] for c in wood_samples) // len(wood_samples)
    wg = sum(c[1] for c in wood_samples) // len(wood_samples)
    wb = sum(c[2] for c in wood_samples) // len(wood_samples)

    out = rgb.copy()
    op = out.load()
    # Chair top rail — kill fire tongues only
    for y in range(int(h * 0.10), int(h * 0.30)):
        for x in range(int(w * 0.38), int(w * 0.62)):
            r, g, b = pix[x, y]
            fire = (
                (r >= 195 and g >= 100 and b <= 120 and (r - b) >= 85)
                or (r >= 225 and g >= 165 and b <= 145 and (r - b) >= 70)
            )
            if fire:
                # Prefer nearby cooler pixel
                sx = int(w * 0.35) if x > w // 2 else int(w * 0.65)
                sy = min(h - 1, y + 28)
                rr, gg, bb = pix[sx, sy]
                if rr >= 200 and (rr - bb) >= 80:
                    rr, gg, bb = wr, wg, wb
                op[x, y] = (
                    int(0.15 * r + 0.85 * rr),
                    int(0.15 * g + 0.85 * gg),
                    int(0.10 * b + 0.90 * bb),
                )
    # Soft local blur on scrubbed top rail to avoid speckles
    top = out.crop((int(w * 0.38), int(h * 0.10), int(w * 0.62), int(h * 0.30)))
    top = top.filter(ImageFilter.GaussianBlur(0.8))
    out.paste(top, (int(w * 0.38), int(h * 0.10)))
    return out


def probe_frames(path: Path) -> int:
    # approximate via fps*dur
    dur = float(
        subprocess.check_output(
            [
                "ffprobe", "-v", "error", "-show_entries", "format=duration",
                "-of", "default=nw=1:nk=1", str(path),
            ],
            text=True,
        ).strip()
    )
    return max(1, int(round(dur * 24)))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="src", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--qa-dir", type=Path, required=True)
    args = ap.parse_args()

    args.qa_dir.mkdir(parents=True, exist_ok=True)
    args.out.parent.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory(prefix="hos_v14_scrub_") as td:
        td_path = Path(td)
        frames_dir = td_path / "frames"
        scrub_dir = td_path / "scrub"
        frames_dir.mkdir()
        scrub_dir.mkdir()
        subprocess.run(
            [
                "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
                "-i", str(args.src),
                "-vf", "fps=24",
                str(frames_dir / "f_%05d.png"),
            ],
            check=True,
        )
        frames = sorted(frames_dir.glob("f_*.png"))
        if not frames:
            raise SystemExit("no frames extracted")
        for i, fr in enumerate(frames):
            scrub_frame(Image.open(fr)).save(scrub_dir / fr.name)
            if i in {0, len(frames) // 4, len(frames) // 2, (3 * len(frames)) // 4, len(frames) - 1}:
                Image.open(scrub_dir / fr.name).convert("RGB").save(
                    args.qa_dir / f"scrub_preview_{i:03d}.jpg", quality=92
                )
        subprocess.run(
            [
                "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
                "-framerate", "24",
                "-i", str(scrub_dir / "f_%05d.png"),
                "-i", str(args.src),
                "-map", "0:v:0", "-map", "1:a?",
                "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "16",
                "-c:a", "copy",
                "-shortest",
                str(args.out),
            ],
            check=True,
        )
    meta = {
        "src": str(args.src),
        "out": str(args.out),
        "bytes": args.out.stat().st_size,
        "method": "chair_top_flame_scrub_keep_panel_glow",
    }
    (args.qa_dir / "scrub_meta.json").write_text(json.dumps(meta, indent=2) + "\n")
    print(json.dumps(meta, indent=2))


if __name__ == "__main__":
    main()
