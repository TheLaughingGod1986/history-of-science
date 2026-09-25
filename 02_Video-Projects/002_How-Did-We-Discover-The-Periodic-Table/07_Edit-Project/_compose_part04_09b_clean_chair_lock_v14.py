#!/usr/bin/env python3
"""v14 plate 09b: lock chair/bookshelf/lamp to clean start; keep desk card motion.

Flow I2V reintroduces chair-top flame. Scrub paints leave jagged glow.
Composite: clean start (ok_abet DNA, soft panel glow, zero flame) for the
upper scene; motion clip for the desk/cards only, soft-feathered.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
import tempfile
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def build_mask(w: int, h: int) -> Image.Image:
    """255 = use clean (chair/lamp/shelves); 0 = use motion (desk)."""
    mask = Image.new("L", (w, h), 0)
    draw = ImageDraw.Draw(mask)
    # Upper scene locked clean through mid-chair
    y_lock = int(h * 0.50)
    draw.rectangle([0, 0, w, y_lock], fill=255)
    # Soft falloff into desk
    band = int(h * 0.18)
    for i in range(band):
        a = int(255 * (1.0 - (i / max(1, band - 1))))
        draw.rectangle([0, y_lock + i, w, y_lock + i + 1], fill=a)
    return mask.filter(ImageFilter.GaussianBlur(radius=22))


def crown_hot_count(im: Image.Image) -> int:
    w, h = im.size
    pix = im.load()
    hot = 0
    for y in range(int(h * 0.08), int(h * 0.22)):
        for x in range(int(w * 0.34), int(w * 0.66)):
            r, g, b = pix[x, y]
            if r > 200 and g > 110 and b < 100 and (r - b) > 80:
                hot += 1
    return hot


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--clean", type=Path, required=True)
    ap.add_argument("--motion", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--qa-dir", type=Path, required=True)
    args = ap.parse_args()

    clean = Image.open(args.clean).convert("RGB")
    w, h = 1920, 1080
    clean = clean.resize((w, h), Image.Resampling.LANCZOS)
    mask = build_mask(w, h)

    args.qa_dir.mkdir(parents=True, exist_ok=True)
    args.out.parent.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory(prefix="hos_v14_comp_") as td:
        tdir = Path(td)
        frames_in = tdir / "in"
        frames_out = tdir / "out"
        frames_in.mkdir()
        frames_out.mkdir()

        subprocess.check_call(
            [
                "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
                "-i", str(args.motion),
                "-vf", "fps=24,scale=1920:1080:flags=lanczos",
                str(frames_in / "f_%04d.jpg"),
            ]
        )
        frames = sorted(frames_in.glob("f_*.jpg"))
        if not frames:
            raise SystemExit("no frames extracted from motion")

        hot_total = 0
        for i, fp in enumerate(frames):
            motion = Image.open(fp).convert("RGB")
            if motion.size != (w, h):
                motion = motion.resize((w, h), Image.Resampling.LANCZOS)
            # Very light lamp flicker on clean layer only
            if i % 5 == 0:
                base = clean.point(lambda p: min(255, int(p * 1.008)))
            elif i % 5 == 2:
                base = clean.point(lambda p: max(0, int(p * 0.995)))
            else:
                base = clean
            out = Image.composite(base, motion, mask)
            out.save(frames_out / fp.name, quality=95)
            if i % 24 == 0 or i in (0, len(frames) // 2, len(frames) - 1):
                hot_total += crown_hot_count(out)

        tmp_vid = tdir / "comp.mp4"
        subprocess.check_call(
            [
                "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
                "-framerate", "24", "-i", str(frames_out / "f_%04d.jpg"),
                "-i", str(args.motion),
                "-map", "0:v", "-map", "1:a?",
                "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18",
                "-preset", "medium", "-c:a", "aac", "-b:a", "192k",
                "-shortest", str(tmp_vid),
            ]
        )
        shutil.copy2(tmp_vid, args.out)

    # QA stills across clip
    for t in (0.5, 2.0, 4.0, 6.0, 7.5):
        dest = args.qa_dir / f"comp_lock_t{t:.1f}.jpg"
        subprocess.check_call(
            [
                "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
                "-ss", str(t), "-i", str(args.out), "-frames:v", "1",
                str(dest),
            ]
        )

    hot_map = {}
    for p in sorted(args.qa_dir.glob("comp_lock_t*.jpg")):
        hot_map[p.name] = crown_hot_count(Image.open(p).convert("RGB"))

    meta = {
        "out": str(args.out),
        "sha256": sha256(args.out),
        "bytes": args.out.stat().st_size,
        "clean": str(args.clean),
        "motion": str(args.motion),
        "method": "clean-chair-lock composite (upper clean start + desk motion)",
        "crown_hot_qa": hot_map,
        "reject": any(v >= 80 for v in hot_map.values()),
    }
    (args.qa_dir / "comp_lock_meta.json").write_text(json.dumps(meta, indent=2) + "\n")
    print(json.dumps(meta, indent=2), flush=True)
    if meta["reject"]:
        raise SystemExit("FAIL: crown hot pixels remain after composite")


if __name__ == "__main__":
    main()
