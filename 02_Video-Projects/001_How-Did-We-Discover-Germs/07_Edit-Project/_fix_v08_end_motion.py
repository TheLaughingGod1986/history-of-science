#!/usr/bin/env python3
"""Replace still-zoom end plates with real motion beds + drifting FACELESS microbes."""
from __future__ import annotations

import math
import subprocess
from pathlib import Path

from PIL import Image, ImageEnhance, ImageFilter

PROJ = Path(__file__).resolve().parents[1]
RAW = PROJ / "04_Generated-Clips" / "part01" / "raw" / "v08_faceless"
ASSETS = PROJ / "04_Generated-Clips" / "part01" / "refs" / "v08_micro_assets"
TMP = PROJ / "07_Edit-Project" / "_tmp_v08" / "end_motion"
FPS = 24
DUR = 8.0
NFRAMES = int(DUR * FPS)


def load_micro_rgba(path: Path) -> Image.Image:
    im = Image.open(path).convert("RGBA")
    px = im.load()
    w, h = im.size
    for y in range(h):
        for x in range(w):
            r, g, b, a = px[x, y]
            if r < 28 and g < 28 and b < 28:
                px[x, y] = (r, g, b, 0)
            elif r < 45 and g < 45 and b < 45:
                px[x, y] = (r, g, b, int(a * 0.35))
    bbox = im.getbbox()
    return im.crop(bbox) if bbox else im


def extract_frames(video: Path, out_dir: Path) -> list[Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    for p in out_dir.glob("f_*.png"):
        p.unlink()
    subprocess.run(
        [
            "ffmpeg", "-y", "-i", str(video),
            "-vf", f"fps={FPS},scale=1280:720:force_original_aspect_ratio=decrease,"
            f"pad=1280:720:(ow-iw)/2:(oh-ih)/2",
            str(out_dir / "f_%04d.png"),
        ],
        check=True,
        capture_output=True,
    )
    frames = sorted(out_dir.glob("f_*.png"))
    if len(frames) < NFRAMES - 2:
        raise SystemExit(f"too few frames from {video}: {len(frames)}")
    return frames[:NFRAMES]


def render_overlay_clip(
    bed_video: Path,
    dest: Path,
    *,
    placements: list[dict],
    work: Path,
) -> None:
    """placements: name, x0,y0 (0-1), amp_x, amp_y, scale, speed, phase, rot_speed"""
    frames_dir = work / "bed_frames"
    out_dir = work / "comp_frames"
    frames = extract_frames(bed_video, frames_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    for p in out_dir.glob("c_*.png"):
        p.unlink()

    micros = {
        "sphere_teal": load_micro_rgba(ASSETS / "sphere_teal.png"),
        "sphere_amber": load_micro_rgba(ASSETS / "sphere_amber.png"),
        "rod_teal": load_micro_rgba(ASSETS / "rod_teal.png"),
        "spiral": load_micro_rgba(ASSETS / "spiral.png"),
    }

    for i, fp in enumerate(frames):
        t = i / FPS
        base = Image.open(fp).convert("RGBA")
        W, H = base.size
        layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        for p in placements:
            m = micros[p["name"]]
            sc = p["scale"] * (1.0 + 0.04 * math.sin(t * p["speed"] + p["phase"]))
            mw = max(20, int(W * sc))
            mh = int(m.height * (mw / m.width))
            mm = m.resize((mw, mh), Image.Resampling.LANCZOS)
            ang = p.get("rot0", 0) + t * p.get("rot_speed", 0)
            mm = mm.rotate(ang, expand=True, resample=Image.Resampling.BICUBIC)
            alpha = mm.split()[-1]
            alpha = ImageEnhance.Brightness(alpha).enhance(p.get("opacity", 0.85))
            mm.putalpha(alpha)
            x = int(W * (p["x0"] + p["amp_x"] * math.sin(t * p["speed"] + p["phase"])) - mm.width / 2)
            y = int(H * (p["y0"] + p["amp_y"] * math.cos(t * p["speed"] * 0.85 + p["phase"])) - mm.height / 2)
            layer.alpha_composite(mm, (x, y))
        soft = layer.filter(ImageFilter.GaussianBlur(radius=0.5))
        out = Image.alpha_composite(base, soft).convert("RGB")
        out.save(out_dir / f"c_{i+1:04d}.png", quality=95)
        if i % 24 == 0:
            print(f"  frame {i}/{len(frames)} → {dest.name}", flush=True)

    dest.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        [
            "ffmpeg", "-y", "-framerate", str(FPS),
            "-i", str(out_dir / "c_%04d.png"),
            "-c:v", "libx264", "-preset", "fast", "-crf", "17",
            "-pix_fmt", "yuv420p", "-an", str(dest),
        ],
        check=True,
        capture_output=True,
    )
    print(f"SAVED {dest} ({dest.stat().st_size})", flush=True)


def main() -> None:
    TMP.mkdir(parents=True, exist_ok=True)

    # Plate 09 — sparse faceless on real instruments motion
    placements_09 = [
        {"name": "spiral", "x0": 0.22, "y0": 0.35, "amp_x": 0.04, "amp_y": 0.05, "scale": 0.10, "speed": 0.9, "phase": 0.2, "rot_speed": 8, "opacity": 0.88},
        {"name": "sphere_teal", "x0": 0.55, "y0": 0.42, "amp_x": 0.05, "amp_y": 0.04, "scale": 0.07, "speed": 1.1, "phase": 1.4, "rot_speed": -12, "opacity": 0.86},
        {"name": "rod_teal", "x0": 0.72, "y0": 0.62, "amp_x": 0.03, "amp_y": 0.06, "scale": 0.09, "speed": 0.8, "phase": 2.1, "rot_speed": 15, "rot0": 40, "opacity": 0.84},
        {"name": "sphere_amber", "x0": 0.40, "y0": 0.58, "amp_x": 0.04, "amp_y": 0.03, "scale": 0.055, "speed": 1.3, "phase": 0.7, "rot_speed": 10, "opacity": 0.82},
    ]
    render_overlay_clip(
        RAW / "04_instruments_v08.mp4",
        RAW / "09_sparse_faceless_v08b.mp4",
        placements=placements_09,
        work=TMP / "p09",
    )

    # Plate 10 — end hold: real ward camera motion + sparse drifting faceless germs
    placements_10 = [
        {"name": "sphere_teal", "x0": 0.28, "y0": 0.40, "amp_x": 0.06, "amp_y": 0.05, "scale": 0.09, "speed": 0.7, "phase": 0.0, "rot_speed": -10, "opacity": 0.88},
        {"name": "rod_teal", "x0": 0.50, "y0": 0.48, "amp_x": 0.05, "amp_y": 0.07, "scale": 0.11, "speed": 0.85, "phase": 1.1, "rot_speed": 12, "rot0": -20, "opacity": 0.86},
        {"name": "spiral", "x0": 0.62, "y0": 0.32, "amp_x": 0.04, "amp_y": 0.06, "scale": 0.08, "speed": 1.0, "phase": 2.4, "rot_speed": 18, "opacity": 0.87},
        {"name": "sphere_amber", "x0": 0.38, "y0": 0.60, "amp_x": 0.05, "amp_y": 0.04, "scale": 0.07, "speed": 0.95, "phase": 0.5, "rot_speed": 9, "opacity": 0.84},
        {"name": "sphere_teal", "x0": 0.70, "y0": 0.55, "amp_x": 0.04, "amp_y": 0.05, "scale": 0.06, "speed": 1.15, "phase": 1.8, "rot_speed": -14, "opacity": 0.83},
        {"name": "spiral", "x0": 0.45, "y0": 0.28, "amp_x": 0.03, "amp_y": 0.04, "scale": 0.065, "speed": 0.75, "phase": 3.0, "rot_speed": 11, "opacity": 0.82},
    ]
    # Prefer curtains aisle (closer to classic ward end look) as motion bed
    render_overlay_clip(
        RAW / "02_curtains_v08.mp4",
        RAW / "10_end_faceless_v08b.mp4",
        placements=placements_10,
        work=TMP / "p10",
    )


if __name__ == "__main__":
    main()
