#!/usr/bin/env python3
"""HOS 006 master v05 (J0886): Build replacement clips for Ben's 4 changes on master v04.

1. #02 P1 02_balance_trunk_v05.mp4 (74 frames = 3.083333 s, 0:04.29-0:07.38):
   Whole willow tree (root ball, trunk, weeping canopy) sitting ON the left brass scale pan, visibly weighed down.
2. #17 P2 05_pure_water_v05.mp4 (120 frames = 5.000 s, 1:23.62-1:28.62):
   Willow tree growing directly out of the terracotta pot through the perforated metal lid as van Helmont (full upper body) pours water from a copper watering can.
3. #80 P5 13_water_in_tree_v05.mp4 (122 frames = 5.083333 s, 7:13.83-7:18.92):
   Distinct closer framing of 05_pure_water_v05.png for the Part 5 callback so no shot shows the tree outside the pot.
4. #50 P3 17_notebook_tick_v05.mp4 (101 frames = 4.208333 s, 4:25.29-4:29.50):
   Joseph Priestley (full upper body, shoulders, sleeve and arm naturally connected) holding a quill pen over his open notebook (tick and cross marks only, zero text).
5. #55 P4 04_sunny_window_v05.mp4 (109 frames = 4.541667 s, 4:51.83-4:56.38):
   5 jars on sunny windowsill, n_motes=0, bubbles drawn in source-jar space strictly below the y=555 water meniscus (y=570..800).
6. #59 P4 08_explorer_shade_v05.mp4 (173 frames = 7.208333 s, 5:15.25-5:22.46):
   First 88 frames from 08_explorer_shade_t1.png (corked jar, n_motes=0, underwater bubbles strictly inside [420, 545, 490, 715]) + 8f crossfade into first 93 frames of 08_explorer_shade_t1.mp4 (Explorer carries the corked jar into the shade).
7. #61 P4 10_only_green_v05.mp4 (110 frames = 4.583333 s, 5:25.88-5:30.46):
   From 10_only_green_v05.png (three jars: pale root, red flower, green leaf), n_motes=0, underwater bubbles drawn in source-jar space strictly inside the right jar [1305, 500, 1495, 720] below the y=480 water meniscus, zero bubbles in the air.
"""
from __future__ import annotations

import math
import os
import shutil
import subprocess
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

REPO = Path("/Users/benjaminoats/YouTube/History Of Science")
PROJ = REPO / "02_Video-Projects/006_Trees-Are-Made-Of-Air"
V04_DIR = PROJ / "07_Edit-Project/master_v04"
V05_DIR = PROJ / "07_Edit-Project/master_v05"
STILLS_V04_DIR = V04_DIR / "stills"
STILLS_V05_DIR = V05_DIR / "stills"
CLIPS_V05_DIR = V05_DIR / "clips"

MEDIA = Path(
    os.environ.get(
        "HOS_006_MEDIA",
        "/Volumes/data/mac-mini-archive/hos-worktrees/2026-10-22/hos-006-trees/02_Video-Projects/006_Trees-Are-Made-Of-Air",
    )
)
P4_RAW = MEDIA / "04_Generated-Clips/part04/raw/v01"
P4_FLOW_STILLS = MEDIA / "04_Generated-Clips/part04/refs/v02_flow_stills"

W, H = 1920, 1080
FPS = 24


def subpixel_crop_resize(img_arr: np.ndarray, zoom: float, dx_px: float, dy_px: float) -> np.ndarray:
    """Smooth sub-pixel bilinear crop-and-scale from (H_src, W_src, 3) float32 array to (1080, 1920, 3)."""
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
    zoom_start: float = 1.04,
    zoom_end: float = 1.12,
    dx_start: float = -12.0,
    dx_end: float = 12.0,
    dy_start: float = -4.0,
    dy_end: float = 4.0,
    bubble_boxes: list[tuple[int, int, int, int]] | None = None,
    water_stream_box: tuple[int, int, int, int] | None = None,
    n_motes: int = 36,
    tilt_deg: float = 0.0,
    seed: int = 42,
) -> Path:
    """Render a smooth 24fps clip from a 16:9 still with continuous camera move.
    Underwater bubbles are composited in 1920x1080 source space BEFORE camera crop/zoom
    so they stay 100% locked inside the jar's water below the meniscus.
    """
    out_mp4.parent.mkdir(parents=True, exist_ok=True)
    im_src = Image.open(still_path).convert("RGB").resize((W, H), Image.Resampling.LANCZOS)
    if abs(tilt_deg) > 1e-4:
        im_src = im_src.rotate(tilt_deg, resample=Image.Resampling.BICUBIC)
    src_rgba = im_src.convert("RGBA")

    rng = np.random.default_rng(seed)
    motes = []
    for _ in range(n_motes):
        mx = float(rng.uniform(80, W - 80))
        my = float(rng.uniform(60, H - 120))
        vx = float(rng.uniform(-14.0, 18.0))
        vy = float(rng.uniform(-10.0, 12.0))
        r = float(rng.uniform(1.6, 3.0))
        phase = float(rng.uniform(0, 2 * math.pi))
        motes.append((mx, my, vx, vy, r, phase))

    bubbles = []
    if bubble_boxes:
        for bx0, by0, bx1, by1 in bubble_boxes:
            n_b = max(14, int((bx1 - bx0) * (by1 - by0) / 2800))
            for _ in range(n_b):
                bx = float(rng.uniform(bx0 + 8, bx1 - 8))
                by = float(rng.uniform(by0 + 8, by1 - 8))
                vy = float(rng.uniform(20.0, 42.0))
                wobble_amp = float(rng.uniform(1.2, 3.2))
                wobble_freq = float(rng.uniform(1.5, 3.0))
                rad = float(rng.uniform(1.8, 3.4))
                phase = float(rng.uniform(0, 2 * math.pi))
                bubbles.append((bx0, by0, bx1, by1, bx, by, vy, wobble_amp, wobble_freq, rad, phase))

    stream_drops = []
    if water_stream_box:
        sx0, sy0, sx1, sy1 = water_stream_box
        for _ in range(28):
            up = float(rng.uniform(0.0, 1.0))
            speed = float(rng.uniform(1.6, 2.4))
            jitter_x = float(rng.uniform(-4.0, 4.0))
            jitter_y = float(rng.uniform(-3.0, 3.0))
            rad = float(rng.uniform(1.6, 2.8))
            stream_drops.append((sx0, sy0, sx1, sy1, up, speed, jitter_x, jitter_y, rad))

    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    sun_mask = np.clip(
        1.0 - ((xx - W * 0.48) ** 2 / (W * 0.55) ** 2 + (yy - H * 0.28) ** 2 / (H * 0.65) ** 2),
        0.0,
        1.0,
    )

    enc = subprocess.Popen(
        [
            "ffmpeg", "-y", "-v", "error",
            "-f", "rawvideo", "-pixel_format", "rgb24",
            "-video_size", f"{W}x{H}", "-framerate", str(FPS),
            "-i", "-", "-an",
            "-c:v", "libx264", "-preset", "medium", "-crf", "17",
            "-pix_fmt", "yuv420p", "-r", str(FPS),
            str(out_mp4),
        ],
        stdin=subprocess.PIPE,
    )
    try:
        for k in range(n_frames):
            u = k / max(1, n_frames - 1)
            t = k / FPS
            zoom = zoom_start + (zoom_end - zoom_start) * u
            dx = dx_start + (dx_end - dx_start) * u
            dy = dy_start + (dy_end - dy_start) * u

            # 1. Draw locked scene elements (underwater bubbles / water stream) in source space
            if bubbles or stream_drops:
                ov_src = Image.new("RGBA", (W, H), (0, 0, 0, 0))
                ds = ImageDraw.Draw(ov_src)

                for bx0, by0, bx1, by1, bx, by, vy, w_amp, w_freq, rad, phase in bubbles:
                    span_h = max(12.0, float(by1 - by0 - 12))
                    py = by1 - 6.0 - ((by1 - by - vy * t) % span_h)
                    px = bx + w_amp * math.sin(t * w_freq + phase)
                    px = max(bx0 + 6.0, min(bx1 - 6.0, px))
                    py = max(by0 + 6.0, min(by1 - 6.0, py))
                    # Smooth fade out before reaching the top meniscus of the water box
                    edge_fade = min((py - by0) / 16.0, (by1 - py) / 14.0, 1.0)
                    edge_fade = max(0.0, edge_fade)
                    alpha = int(165 * edge_fade)
                    if alpha > 8:
                        ds.ellipse(
                            (px - rad, py - rad, px + rad, py + rad),
                            fill=(235, 248, 255, int(alpha * 0.55)),
                            outline=(255, 255, 255, alpha),
                            width=1,
                        )

                for sx0, sy0, sx1, sy1, up, speed, jx, jy, rad in stream_drops:
                    prog = (up + t * speed) % 1.0
                    px = sx0 + (sx1 - sx0) * prog + jx
                    py = sy0 + (sy1 - sy0) * prog + jy + 10.0 * prog * prog
                    fade = math.sin(math.pi * prog)
                    alpha = int(130 * fade)
                    if alpha > 10:
                        ds.ellipse(
                            (px - rad, py - rad, px + rad, py + rad),
                            fill=(240, 248, 255, alpha),
                        )

                comp_src = Image.alpha_composite(src_rgba, ov_src).convert("RGB")
                src_arr = np.asarray(comp_src, dtype=np.float32)
            else:
                src_arr = np.asarray(im_src, dtype=np.float32)

            # 2. Apply smooth sub-pixel camera move + warm sunlight breathing
            frame_arr = subpixel_crop_resize(src_arr, zoom, dx, dy)
            shimmer = 1.0 + 0.018 * math.sin(2.0 * math.pi * t / 3.2) * sun_mask[:, :, None]
            frame_arr = np.clip(frame_arr * shimmer, 0.0, 255.0)

            if motes:
                im = Image.fromarray(frame_arr.astype(np.uint8), "RGB").convert("RGBA")
                ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
                d = ImageDraw.Draw(ov)
                for mx, my, vx, vy, r, phase in motes:
                    px = (mx + vx * t + 6.0 * math.sin(t * 1.4 + phase)) % W
                    py = (my + vy * t + 4.0 * math.cos(t * 1.1 + phase)) % H
                    alpha = int(55 + 45 * (0.5 + 0.5 * math.sin(t * 2.2 + phase)))
                    d.ellipse((px - r, py - r, px + r, py + r), fill=(255, 240, 200, alpha))
                out_im = Image.alpha_composite(im, ov).convert("RGB")
            else:
                out_im = Image.fromarray(frame_arr.astype(np.uint8), "RGB")

            enc.stdin.write(out_im.tobytes())
    finally:
        if enc.stdin:
            enc.stdin.close()
        if enc.wait() != 0:
            raise RuntimeError(f"ffmpeg failed encoding {out_mp4}")

    return out_mp4


def build_59_explorer_shade_v05(tmp: Path) -> Path:
    """#59 P4 08_explorer_shade_v05.mp4 (173 frames = 7.208333 s):
    First 88 frames from 08_explorer_shade_t1.png (corked jar on sunny windowsill, n_motes=0,
    bubbles strictly underwater inside [420, 545, 490, 715]) + 8-frame crossfade +
    first 93 frames of 08_explorer_shade_t1.mp4 (Explorer carries the corked jar into the shade).
    """
    t1_still = P4_FLOW_STILLS / "08_explorer_shade_t1.png"
    t1_vid = P4_RAW / "08_explorer_shade_t1.mp4"
    out = CLIPS_V05_DIR / "08_explorer_shade_v05.mp4"

    part_a_mp4 = tmp / "p4_59_a.mp4"
    render_animated_still_clip(
        t1_still,
        part_a_mp4,
        n_frames=88,
        zoom_start=1.05,
        zoom_end=1.01,
        dx_start=-10.0,
        dx_end=0.0,
        dy_start=-3.0,
        dy_end=0.0,
        bubble_boxes=[(420, 545, 490, 715)],
        n_motes=0,
        seed=459,
    )

    d_a = tmp / "p4_59_a_frames"
    d_b = tmp / "p4_59_b_frames"
    d_out = tmp / "p4_59_out"
    for d in (d_a, d_b, d_out):
        d.mkdir(parents=True, exist_ok=True)

    subprocess.run(
        [
            "ffmpeg", "-y", "-v", "error",
            "-i", str(part_a_mp4), "-frames:v", "88",
            "-vf", "scale=1920:1080:flags=lanczos",
            str(d_a / "f_%04d.png"),
        ],
        check=True,
    )
    subprocess.run(
        [
            "ffmpeg", "-y", "-v", "error",
            "-i", str(t1_vid), "-frames:v", "93",
            "-vf", "scale=1920:1080:flags=lanczos",
            str(d_b / "f_%04d.png"),
        ],
        check=True,
    )

    fa = sorted(d_a.glob("f_*.png"))
    fb = sorted(d_b.glob("f_*.png"))
    n_a, n_b, xf = 88, 93, 8
    assert len(fa) == n_a and len(fb) == n_b
    assert n_a + n_b - xf == 173

    for k in range(173):
        if k < n_a - xf:
            shutil.copy2(fa[k], d_out / f"f_{k:04d}.png")
        elif k < n_a:
            kb = k - (n_a - xf)
            w = (kb + 1) / (xf + 1)
            w = w * w * (3.0 - 2.0 * w)
            aa = np.asarray(Image.open(fa[k]).convert("RGB"), dtype=np.float32)
            ab = np.asarray(Image.open(fb[kb]).convert("RGB"), dtype=np.float32)
            arr = aa * (1.0 - w) + ab * w
            Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8), "RGB").save(d_out / f"f_{k:04d}.png")
        else:
            kb = k - (n_a - xf)
            shutil.copy2(fb[kb], d_out / f"f_{k:04d}.png")

    subprocess.run(
        [
            "ffmpeg", "-y", "-v", "error",
            "-framerate", str(FPS),
            "-i", str(d_out / "f_%04d.png"),
            "-c:v", "libx264", "-preset", "medium", "-crf", "17",
            "-pix_fmt", "yuv420p", "-r", str(FPS),
            "-an", str(out),
        ],
        check=True,
    )
    return out


def main() -> None:
    CLIPS_V05_DIR.mkdir(parents=True, exist_ok=True)
    tmp = Path("/private/tmp/hos006_clips_v05")
    if tmp.exists():
        shutil.rmtree(tmp)
    tmp.mkdir(parents=True, exist_ok=True)

    outputs = [
        (
            "#02 P1 02_balance_trunk",
            render_animated_still_clip(
                STILLS_V05_DIR / "02_balance_trunk_v05.png",
                CLIPS_V05_DIR / "02_balance_trunk_v05.mp4",
                n_frames=74,
                zoom_start=1.03,
                zoom_end=1.10,
                dx_start=-12.0,
                dx_end=12.0,
                dy_start=-3.0,
                dy_end=3.0,
                n_motes=32,
                seed=102,
            ),
        ),
        (
            "#17 P2 05_pure_water",
            render_animated_still_clip(
                STILLS_V05_DIR / "05_pure_water_v05.png",
                CLIPS_V05_DIR / "05_pure_water_v05.mp4",
                n_frames=120,
                zoom_start=1.03,
                zoom_end=1.11,
                dx_start=-14.0,
                dx_end=14.0,
                dy_start=-4.0,
                dy_end=4.0,
                water_stream_box=(1155, 695, 1065, 790),
                n_motes=30,
                seed=217,
            ),
        ),
        (
            "#80 P5 13_water_in_tree",
            render_animated_still_clip(
                STILLS_V05_DIR / "05_pure_water_v05.png",
                CLIPS_V05_DIR / "13_water_in_tree_v05.mp4",
                n_frames=122,
                zoom_start=1.10,
                zoom_end=1.18,
                dx_start=18.0,
                dx_end=-18.0,
                dy_start=-8.0,
                dy_end=6.0,
                water_stream_box=(1155, 695, 1065, 790),
                n_motes=30,
                seed=580,
            ),
        ),
        (
            "#50 P3 17_notebook_tick",
            render_animated_still_clip(
                STILLS_V05_DIR / "17_notebook_tick_v05.png",
                CLIPS_V05_DIR / "17_notebook_tick_v05.mp4",
                n_frames=101,
                zoom_start=1.03,
                zoom_end=1.10,
                dx_start=-12.0,
                dx_end=12.0,
                dy_start=-3.0,
                dy_end=3.0,
                n_motes=28,
                seed=350,
            ),
        ),
        (
            "#55 P4 04_sunny_window",
            render_animated_still_clip(
                STILLS_V04_DIR / "04_sunny_window_v04.png",
                CLIPS_V05_DIR / "04_sunny_window_v05.mp4",
                n_frames=109,
                zoom_start=1.03,
                zoom_end=1.10,
                dx_start=-14.0,
                dx_end=14.0,
                dy_start=-3.0,
                dy_end=3.0,
                bubble_boxes=[
                    (175, 570, 375, 800),
                    (520, 570, 710, 800),
                    (855, 570, 1045, 800),
                    (1190, 570, 1380, 800),
                    (1530, 570, 1720, 800),
                ],
                n_motes=0,
                seed=455,
            ),
        ),
        (
            "#59 P4 08_explorer_shade",
            build_59_explorer_shade_v05(tmp),
        ),
        (
            "#61 P4 10_only_green",
            render_animated_still_clip(
                STILLS_V05_DIR / "10_only_green_v05.png",
                CLIPS_V05_DIR / "10_only_green_v05.mp4",
                n_frames=110,
                zoom_start=1.05,
                zoom_end=1.12,
                dx_start=-14.0,
                dx_end=14.0,
                dy_start=-3.0,
                dy_end=3.0,
                bubble_boxes=[(1305, 500, 1495, 720)],
                n_motes=0,
                tilt_deg=0.7,
                seed=461,
            ),
        ),
    ]
    shutil.rmtree(tmp, ignore_errors=True)

    import sys
    sys.path.insert(0, "/Users/benjaminoats/YouTube/orbit-with-ben/scripts")
    import polish_gate as pg

    for label, p in outputs:
        nb = subprocess.check_output(
            [
                "ffprobe", "-v", "error", "-count_frames", "-select_streams", "v:0",
                "-show_entries", "stream=nb_read_frames,duration", "-of", "csv=p=0", str(p),
            ],
            text=True,
        ).strip()
        dur = float(nb.split(",")[0])
        frames = int(nb.split(",")[1])
        mid = dur / 2.0
        g = pg.frame_gray(p, mid)
        mean = float(g.mean())
        std = float(g.std())
        ed = pg.edge_density(g)
        sm = pg.seams(g)
        print(
            f"{label:26s} -> {p.name:30s} frames={frames:3d} dur={dur:6.3f}s "
            f"mean={mean:5.1f} std={std:5.1f} edge={ed:.4f} seams={sm}",
            flush=True,
        )


if __name__ == "__main__":
    main()
