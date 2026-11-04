#!/usr/bin/env python3
"""HOS 007 master v04 (J0925): Build 3 replacement clips for Ben's v03 notes at £0 / 0 Flow credits,
and stage the 8 kept v03 replacement/tail clips from master_v03_J0887.

1. Cut #007 (P1:07b_three_in_ten, 91f = 3.7917s, 35.1667..38.9583s, part_frame_offset=844):
   From 07b_three_in_ten_v04.png (ten intact turned-wood peg dolls on solid oak cottage windowsill:
   7 standing upright, 3 lying on their sides on the solid shelf; nothing passes through solid objects)
   with smooth subpixel push-in, soft window motes, and Part 1 overlay p1_data_3in10.
2. Cut #031 (P2:06b_jesty_hands, 152f = 6.3333s, 155.4167..161.7500s, part_frame_offset=1310):
   From 06b_jesty_hands_v04.png (18th-century folding steel medical lancet held at a flat shallow grazing
   angle scratching the surface of the forearm skin, with no needle going into the arm)
   with smooth subpixel push-in, warm farmhouse daylight motes, and Part 2 overlay p2_when_1774.
3. Cut #048 (P3:04_lancet_touch, 158f = 6.5833s, 255.8333..262.4167s, part_frame_offset=609):
   From 04_lancet_touch_v04.png (Edward Jenner in his sunlit study gently touching a flat folding steel
   lancet at a shallow grazing angle to 8-year-old James Phipps's clean upper arm; zero AI artefact on arm)
   with smooth subpixel push-in, warm study sunbeam motes, and Part 3 overlay p3_who_phipps.
"""
from __future__ import annotations

import math
import shutil
import subprocess as sp
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

PACK_DIR = Path(__file__).resolve().parent
EDIT_DIR = PACK_DIR.parent
NAS_WORK = Path("/Volumes/data/mac-mini-archive/scratch/J0925")
STILLS_DIR = NAS_WORK / "stills"
CLIPS_DIR = NAS_WORK / "clips"
V03_NAS = Path("/Volumes/data/mac-mini-archive/hos-007-vaccine/master_v03_J0887")

sys.path.insert(0, str(EDIT_DIR))
import _assemble_part_roughs_v01 as apr  # noqa: E402

W, H, FPS = 1920, 1080, 24


def subpixel_crop_resize(img_arr: np.ndarray, zoom: float, dx_px: float, dy_px: float) -> np.ndarray:
    sh, sw, _ = img_arr.shape
    cw = sw / zoom
    ch = sh / zoom
    cx = sw * 0.5 + dx_px
    cy = sh * 0.5 + dy_px
    x0 = max(0.0, min(sw - cw, cx - cw * 0.5))
    y0 = max(0.0, min(sh - ch, cy - ch * 0.5))

    xs = x0 + (np.arange(W, dtype=np.float32) + 0.5) * (cw / W) - 0.5
    ys = y0 + (np.arange(H, dtype=np.float32) + 0.5) * (ch / H) - 0.5
    xs = np.clip(xs, 0.0, sw - 1.001)
    ys = np.clip(ys, 0.0, sh - 1.001)

    xi = np.floor(xs).astype(np.int32)
    yi = np.floor(ys).astype(np.int32)
    xf = (xs - xi)[None, :, None]
    yf = (ys - yi)[:, None, None]

    p00 = img_arr[yi[:, None], xi[None, :]]
    p01 = img_arr[yi[:, None], xi[None, :] + 1]
    p10 = img_arr[yi[:, None] + 1, xi[None, :]]
    p11 = img_arr[yi[:, None] + 1, xi[None, :] + 1]

    top = p00 * (1.0 - xf) + p01 * xf
    bot = p10 * (1.0 - xf) + p11 * xf
    return top * (1.0 - yf) + bot * yf


def render_animated_still_clip(
    still_path: Path,
    out_mp4: Path,
    n_frames: int,
    zoom_start: float = 1.02,
    zoom_end: float = 1.10,
    dx_start: float = -10.0,
    dx_end: float = 10.0,
    dy_start: float = -3.0,
    dy_end: float = 3.0,
    active_overlays: list[dict] | None = None,
    noise: np.ndarray | None = None,
    part_frame_offset: int = 0,
    seed: int = 42,
) -> Path:
    out_mp4.parent.mkdir(parents=True, exist_ok=True)
    im_src = Image.open(still_path).convert("RGB").resize((W, H), Image.Resampling.LANCZOS)
    comp_src = np.asarray(im_src, dtype=np.float32)

    rng = np.random.default_rng(seed)
    motes = []
    for _ in range(34):
        mx = float(rng.uniform(80, W - 80))
        my = float(rng.uniform(60, H - 120))
        vx = float(rng.uniform(-12.0, 16.0))
        vy = float(rng.uniform(-8.0, 10.0))
        r = float(rng.uniform(1.6, 2.8))
        phase = float(rng.uniform(0, 2 * math.pi))
        motes.append((mx, my, vx, vy, r, phase))

    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    sun_mask = np.clip(
        1.0 - ((xx - W * 0.35) ** 2 / (W * 0.55) ** 2 + (yy - H * 0.28) ** 2 / (H * 0.65) ** 2),
        0.0,
        1.0,
    )

    enc = sp.Popen(
        [
            "ffmpeg", "-y", "-v", "error",
            "-f", "rawvideo", "-pixel_format", "rgb24",
            "-video_size", f"{W}x{H}", "-framerate", str(FPS),
            "-i", "-", "-an",
            "-c:v", "libx264", "-preset", "fast", "-crf", "17",
            "-pix_fmt", "yuv420p", "-r", str(FPS),
            str(out_mp4),
        ],
        stdin=sp.PIPE,
    )
    try:
        for k in range(n_frames):
            u = k / max(1, n_frames - 1)
            t = k / FPS
            zoom = zoom_start + (zoom_end - zoom_start) * u
            dx = dx_start + (dx_end - dx_start) * u
            dy = dy_start + (dy_end - dy_start) * u

            frame_f = subpixel_crop_resize(comp_src, zoom, dx, dy)
            shimmer = 1.0 + 0.016 * math.sin(t * 1.6) * sun_mask
            frame_f = np.clip(frame_f * shimmer[:, :, None], 0.0, 255.0)
            frame_im = Image.fromarray(frame_f.astype(np.uint8), "RGB").convert("RGBA")

            ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
            d = ImageDraw.Draw(ov)
            for mx, my, vx, vy, r, phase in motes:
                px = (mx + vx * t + 5.0 * math.sin(t * 1.2 + phase)) % W
                py = (my + vy * t + 4.0 * math.cos(t * 1.0 + phase)) % H
                twinkle = 0.5 + 0.5 * math.sin(t * 2.3 + phase)
                alpha = int(32 + 48 * twinkle)
                d.ellipse((px - r, py - r, px + r, py + r), fill=(255, 242, 208, alpha))

            out_im = Image.alpha_composite(frame_im, ov).convert("RGB")
            if active_overlays and noise is not None:
                t_part = (part_frame_offset + k) / FPS
                for ov_spec in active_overlays:
                    if ov_spec["start"] <= t_part <= ov_spec["end"]:
                        out_im = apr.draw_overlay_on_frame(out_im, ov_spec, t_part, noise, part_frame_offset + k)

            assert enc.stdin is not None
            enc.stdin.write(out_im.tobytes())
    finally:
        if enc.stdin:
            enc.stdin.close()
        if enc.wait() != 0:
            raise RuntimeError(f"ffmpeg failed encoding {out_mp4}")

    return out_mp4


def main() -> int:
    CLIPS_DIR.mkdir(parents=True, exist_ok=True)
    STILLS_DIR.mkdir(parents=True, exist_ok=True)

    # Copy kept v03 stills and clips from NAS master_v03_J0887
    for p in (V03_NAS / "stills").glob("*.png"):
        if not p.name.startswith("._"):
            dst = STILLS_DIR / p.name
            if not dst.exists():
                shutil.copy2(p, dst)
    for p in (V03_NAS / "clips").glob("*.mp4"):
        if not p.name.startswith("._"):
            dst = CLIPS_DIR / p.name
            if not dst.exists():
                shutil.copy2(p, dst)

    noise = np.random.default_rng(7007).random((H, W)).astype(np.float32)

    # 1. Cut #007 (0:35.17..0:38.96, 91 frames = 3.7917 s, part_frame_offset=844)
    p1_ovs = [ov for ov in apr.PART_OVERLAYS[1] if ov["id"] == "p1_data_3in10"]
    print("Rendering 07b_three_in_ten_v04.mp4 (91 frames)...", flush=True)
    render_animated_still_clip(
        still_path=STILLS_DIR / "07b_three_in_ten_v04.png",
        out_mp4=CLIPS_DIR / "07b_three_in_ten_v04.mp4",
        n_frames=91,
        zoom_start=1.02,
        zoom_end=1.09,
        dx_start=-8.0,
        dx_end=8.0,
        dy_start=-2.0,
        dy_end=2.0,
        active_overlays=p1_ovs,
        noise=noise,
        part_frame_offset=844,
        seed=707,
    )

    # 2. Cut #031 (2:35.42..2:41.75, 152 frames = 6.3333 s, part_frame_offset=1310)
    p2_ovs = [ov for ov in apr.PART_OVERLAYS[2] if ov["id"] == "p2_when_1774"]
    print("Rendering 06b_jesty_hands_v04.mp4 (152 frames)...", flush=True)
    render_animated_still_clip(
        still_path=STILLS_DIR / "06b_jesty_hands_v04.png",
        out_mp4=CLIPS_DIR / "06b_jesty_hands_v04.mp4",
        n_frames=152,
        zoom_start=1.02,
        zoom_end=1.10,
        dx_start=-10.0,
        dx_end=10.0,
        dy_start=-3.0,
        dy_end=3.0,
        active_overlays=p2_ovs,
        noise=noise,
        part_frame_offset=1310,
        seed=731,
    )

    # 3. Cut #048 (4:15.83..4:22.42, 158 frames = 6.5833 s, part_frame_offset=609)
    p3_ovs = [ov for ov in apr.PART_OVERLAYS[3] if ov["id"] == "p3_who_phipps"]
    print("Rendering 04_lancet_touch_v04.mp4 (158 frames)...", flush=True)
    render_animated_still_clip(
        still_path=STILLS_DIR / "04_lancet_touch_v04.png",
        out_mp4=CLIPS_DIR / "04_lancet_touch_v04.mp4",
        n_frames=158,
        zoom_start=1.02,
        zoom_end=1.10,
        dx_start=-10.0,
        dx_end=10.0,
        dy_start=-3.0,
        dy_end=3.0,
        active_overlays=p3_ovs,
        noise=noise,
        part_frame_offset=609,
        seed=748,
    )

    print("ALL 3 V04 REPLACEMENT CLIPS RENDERED SUCCESSFULLY", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
