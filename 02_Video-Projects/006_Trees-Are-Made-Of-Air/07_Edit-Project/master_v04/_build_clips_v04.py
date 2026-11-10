#!/usr/bin/env python3
"""HOS 006 master v04 (J0882): Build the 12 replacement/updated clips for Ben's 11 changes.

1. #03 P1 03_pot_jar_leaf_v04.mp4 (180 frames = 7.500 s):
   From stills/03_pot_jar_leaf_v04.png (middle mint sprig growing out of soil in terracotta pot under bell jar)
   with smooth sub-pixel push-in + rising underwater bubbles in right jar + golden dust motes.
2. #88 P5 21_three_objects_v04.mp4 (120 frames = 5.000 s):
   From stills/03_pot_jar_leaf_v04.png with distinct closer framing/pan + rising underwater bubbles + motes.
3. #10 P1 10_van_helmont_sack_v04.mp4 (154 frames = 6.416667 s):
   From stills/10_van_helmont_sack_v04.png (heavy soil sack staying solidly on brass scale pan)
   with smooth sub-pixel push-in + warm courtyard sunbeam shimmer + motes.
4. #14 P2 02_balance_200_house_v04.mp4 (140 frames = 5.833333 s):
   02_balance_200_t1.mp4 top-cropped 1920x816 + HOS house DATA counter showing both imperial & metric:
   '0 -> 200 lb (about 91 kg)' / 'of dried soil · starting weight'.
5. #15 P2 03_willow_shoot_scale_v04.mp4 (103 frames = 4.291667 s):
   From stills/03_willow_shoot_scale_v04.png (whole young 5-lb willow tree with washed roots on scale pan)
   with smooth sub-pixel push-in + warm window light shimmer + motes.
6. #16 P2 04_lid_rain_v04.mp4 (153 frames = 6.375 s):
   From stills/04_lid_rain_v04.png (smooth terracotta pot with perforated flat tin-plated iron lid on top)
   with smooth sub-pixel push-in + animated falling silver raindrops onto top lid + golden motes.
7. #35 P3 02_hales_branch_v04.mp4 (156 frames = 6.500 s):
   From stills/02_hales_branch_v04.png (Hales observing upright leafy sprig in hand-blown glass jar of water)
   with smooth sub-pixel push-in + rising underwater bubbles along stem + motes.
8. #36 P3 03_water_level_v04.mp4 (125 frames = 5.208333 s):
   From stills/03_water_level_v04.png (close-up upright leafy sprig in beeswax-sealed glass jar of water)
   with smooth sub-pixel push-in + rising underwater bubbles strictly inside jar + water shimmer.
9. #55 P4 04_sunny_window_v04.mp4 (109 frames = 4.541667 s):
   From stills/04_sunny_window_v04.png (5 glass jars with submerged leaves on sunny windowsill, zero air droplets)
   with smooth sub-pixel push-in + tiny silver bubbles rising strictly inside the jars + motes.
10. #59 P4 08_explorer_shade_v04.mp4 (173 frames = 7.208333 s):
   First 88 clean frames of 08_explorer_shade_t2.mp4 + 8-frame crossfade + first 93 clean frames of
   08_explorer_shade_t1.mp4 (173 frames total; bubbles strictly inside the jar, zero foam outside).
11. #66 P4 15_leaf_turns_sun_v04.mp4 (70 frames = 2.916667 s):
   From 15_leaf_turns_sun_t1.png with smooth sub-pixel push-in toward sunlit green leaves + sunbeam shimmer (zero rotation).
12. #91 P5 24_gold_foil_crop_v04.mp4 (151 frames = 6.291667 s):
   24_gold_foil_t1.mp4 cropped 1664:936:128:144 -> 1920x1080 to remove ceiling 'ATOMOS' sign.
"""
from __future__ import annotations

import math
import os
import shutil
import subprocess
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

REPO = Path("/Users/benjaminoats/YouTube/History Of Science")
PROJ = REPO / "02_Video-Projects/006_Trees-Are-Made-Of-Air"
V04_DIR = PROJ / "07_Edit-Project/master_v04"
STILLS_DIR = V04_DIR / "stills"
CLIPS_DIR = V04_DIR / "clips"
MEDIA = Path(
    os.environ.get(
        "HOS_006_MEDIA",
        "/Volumes/data/mac-mini-archive/hos-worktrees/2026-10-22/hos-006-trees/02_Video-Projects/006_Trees-Are-Made-Of-Air",
    )
)
P2_RAW = MEDIA / "04_Generated-Clips/part02/raw/v01"
P4_RAW = MEDIA / "04_Generated-Clips/part04/raw/v01"
P5_RAW = MEDIA / "04_Generated-Clips/part05/raw/v01"
P4_FLOW_STILLS = MEDIA / "04_Generated-Clips/part04/refs/v02_flow_stills"

DIDOT = "/System/Library/Fonts/Supplemental/Didot.ttc"
W, H = 1920, 1080
FPS = 24


def didot_font(size: int, index: int = 1) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(DIDOT, size=size, index=index)


def ease_out(x: float) -> float:
    x = max(0.0, min(1.0, x))
    return 1.0 - (1.0 - x) ** 3


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
    rain_box: tuple[int, int, int, int] | None = None,
    seed: int = 42,
) -> Path:
    """Render a smooth 24fps clip from a 16:9 still with continuous camera move + underwater bubbles / raindrops / motes."""
    out_mp4.parent.mkdir(parents=True, exist_ok=True)
    im_src = Image.open(still_path).convert("RGB").resize((W, H), Image.Resampling.LANCZOS)
    src_arr = np.asarray(im_src, dtype=np.float32)

    rng = np.random.default_rng(seed)
    # Pre-generate warm golden sunbeam dust motes
    n_motes = 42
    motes = []
    for _ in range(n_motes):
        mx = float(rng.uniform(80, W - 80))
        my = float(rng.uniform(60, H - 120))
        vx = float(rng.uniform(-14.0, 18.0))
        vy = float(rng.uniform(-10.0, 12.0))
        r = float(rng.uniform(1.6, 3.2))
        phase = float(rng.uniform(0, 2 * math.pi))
        motes.append((mx, my, vx, vy, r, phase))

    # Pre-generate underwater rising bubbles inside specified water boxes (x0, y0, x1, y1 in 1920x1080 space)
    bubbles = []
    if bubble_boxes:
        for bx0, by0, bx1, by1 in bubble_boxes:
            n_b = max(14, int((bx1 - bx0) * (by1 - by0) / 3200))
            for _ in range(n_b):
                bx = float(rng.uniform(bx0 + 8, bx1 - 8))
                by = float(rng.uniform(by0 + 8, by1 - 8))
                vy = float(rng.uniform(22.0, 48.0))
                wobble_amp = float(rng.uniform(1.5, 4.0))
                wobble_freq = float(rng.uniform(1.5, 3.2))
                rad = float(rng.uniform(1.8, 3.8))
                phase = float(rng.uniform(0, 2 * math.pi))
                bubbles.append((bx0, by0, bx1, by1, bx, by, vy, wobble_amp, wobble_freq, rad, phase))

    # Pre-generate falling raindrops if rain_box is specified
    drops = []
    if rain_box:
        rx0, ry0, rx1, ry1 = rain_box
        for _ in range(55):
            rx = float(rng.uniform(rx0, rx1))
            ry = float(rng.uniform(ry0, ry1))
            vy = float(rng.uniform(420.0, 620.0))
            vx = float(rng.uniform(-18.0, -6.0))
            length = float(rng.uniform(18.0, 34.0))
            drops.append((rx0, ry0, rx1, ry1, rx, ry, vx, vy, length))

    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    sun_mask = np.clip(1.0 - ((xx - W * 0.48) ** 2 / (W * 0.55) ** 2 + (yy - H * 0.28) ** 2 / (H * 0.65) ** 2), 0.0, 1.0)

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

            frame_arr = subpixel_crop_resize(src_arr, zoom, dx, dy)
            # Subtle warm sunlight breathing so luma evolves smoothly frame-to-frame
            shimmer = 1.0 + 0.018 * math.sin(2.0 * math.pi * t / 3.2) * sun_mask[:, :, None]
            frame_arr = np.clip(frame_arr * shimmer, 0.0, 255.0)

            im = Image.fromarray(frame_arr.astype(np.uint8), "RGB").convert("RGBA")
            ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
            d = ImageDraw.Draw(ov)

            # Draw drifting warm dust motes
            for mx, my, vx, vy, r, phase in motes:
                px = (mx + vx * t + 6.0 * math.sin(t * 1.4 + phase)) % W
                py = (my + vy * t + 4.0 * math.cos(t * 1.1 + phase)) % H
                alpha = int(55 + 45 * (0.5 + 0.5 * math.sin(t * 2.2 + phase)))
                d.ellipse((px - r, py - r, px + r, py + r), fill=(255, 240, 200, alpha))

            # Draw rising underwater bubbles strictly inside their water bounding boxes
            for bx0, by0, bx1, by1, bx, by, vy, w_amp, w_freq, rad, phase in bubbles:
                span_h = max(12.0, float(by1 - by0 - 12))
                py = by1 - 6.0 - ((by1 - by - vy * t) % span_h)
                px = bx + w_amp * math.sin(t * w_freq + phase)
                px = max(bx0 + 6.0, min(bx1 - 6.0, px))
                # Fade near bottom and top meniscus of the water box
                edge_fade = min((py - by0) / 14.0, (by1 - py) / 14.0, 1.0)
                edge_fade = max(0.0, edge_fade)
                alpha = int(165 * edge_fade)
                if alpha > 8:
                    d.ellipse(
                        (px - rad, py - rad, px + rad, py + rad),
                        fill=(235, 248, 255, int(alpha * 0.55)),
                        outline=(255, 255, 255, alpha),
                        width=1,
                    )

            # Draw falling silver raindrops onto the top perforated lid
            for rx0, ry0, rx1, ry1, rx, ry, vx, vy, length in drops:
                span_h = float(ry1 - ry0)
                py = ry0 + ((ry - ry0 + vy * t) % span_h)
                px = rx0 + ((rx - rx0 + vx * t) % (rx1 - rx0))
                if py + length <= ry1:
                    d.line(
                        (px, py, px + vx * 0.04, py + length),
                        fill=(230, 242, 255, 135),
                        width=2,
                    )
                else:
                    # Tiny splash ripple right on the perforated metal lid (y ~ ry1)
                    rp = (py + length - ry1) / max(1.0, length)
                    rr = 2.0 + 8.0 * rp
                    ra = int(140 * (1.0 - rp))
                    if ra > 10:
                        d.ellipse((px - rr, ry1 - rr * 0.35, px + rr, ry1 + rr * 0.35), outline=(235, 245, 255, ra), width=1)

            out_im = Image.alpha_composite(im, ov).convert("RGB")
            enc.stdin.write(out_im.tobytes())
    finally:
        if enc.stdin:
            enc.stdin.close()
        if enc.wait() != 0:
            raise RuntimeError(f"ffmpeg failed encoding {out_mp4}")

    return out_mp4


def build_14_balance_200_v04(tmp: Path) -> Path:
    """#14 P2 02_balance_200_house_v04.mp4: 140 frames with imperial + metric animated counter."""
    src = P2_RAW / "02_balance_200_t1.mp4"
    out = CLIPS_DIR / "02_balance_200_house_v04.mp4"
    bg_dir = tmp / "p2_14_bg"
    out_dir = tmp / "p2_14_out"
    bg_dir.mkdir(parents=True, exist_ok=True)
    out_dir.mkdir(parents=True, exist_ok=True)

    subprocess.run(
        [
            "ffmpeg", "-y", "-v", "error",
            "-i", str(src),
            "-frames:v", "140",
            "-vf", "crop=1920:816:0:0,scale=1920:1080:flags=lanczos",
            str(bg_dir / "f_%04d.png"),
        ],
        check=True,
    )

    f_num = didot_font(54, 1)
    f_sub = didot_font(38, 1)

    for idx in range(140):
        t = idx / FPS
        bg = Image.open(bg_dir / f"f_{idx + 1:04d}.png").convert("RGBA")

        if t < 0.20 or t > 4.85:
            a = 0.0
        elif t < 0.55:
            a = ease_out((t - 0.20) / 0.35)
        elif t > 4.35:
            a = ease_out((4.85 - t) / 0.50)
        else:
            a = 1.0

        if a > 0.01:
            ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
            od = ImageDraw.Draw(ov)
            slide = int(round((1.0 - a) * 28))
            al = int(round(255 * a))
            al_bg = int(round(238 * a))

            # Floating lower-third card (width 1440 px = 75.0% < 85% so zero horizontal seam in polish_gate)
            bx0, bx1 = 240, 1680
            by0, by1 = 814 + slide, 1018 + slide
            od.rounded_rectangle(
                [bx0, by0, bx1, by1],
                radius=14,
                fill=(61, 41, 28, al_bg),
                outline=(196, 154, 78, al),
                width=3,
            )

            cnt_p = ease_out((t - 0.30) / 1.50)
            val_lb = int(round(200 * cnt_p))
            val_kg = int(round(91 * cnt_p))
            od.text(
                (bx0 + 44, by0 + 24),
                f"{val_lb} lb (about {val_kg} kg)",
                font=f_num,
                fill=(244, 235, 216, al),
            )
            od.text(
                (bx0 + 44, by0 + 112),
                "of dried soil · starting weight",
                font=f_sub,
                fill=(218, 188, 134, al),
            )

            bar_x0, bar_x1 = bx0 + 820, bx1 - 48
            bar_y0, bar_y1 = by0 + 88, by0 + 122
            od.rounded_rectangle(
                [bar_x0, bar_y0, bar_x1, bar_y1],
                radius=8,
                fill=(42, 28, 18, al),
                outline=(152, 114, 68, al),
                width=2,
            )
            fill_w = int(round((bar_x1 - bar_x0 - 8) * cnt_p))
            if fill_w > 4:
                od.rounded_rectangle(
                    [bar_x0 + 4, bar_y0 + 4, bar_x0 + 4 + fill_w, bar_y1 - 4],
                    radius=6,
                    fill=(196, 154, 78, al),
                )

            bg = Image.alpha_composite(bg, ov)

        bg.convert("RGB").save(out_dir / f"f_{idx:04d}.png")

    subprocess.run(
        [
            "ffmpeg", "-y", "-v", "error",
            "-framerate", str(FPS),
            "-i", str(out_dir / "f_%04d.png"),
            "-c:v", "libx264", "-preset", "medium", "-crf", "17",
            "-pix_fmt", "yuv420p", "-r", str(FPS),
            "-an", str(out),
        ],
        check=True,
    )
    return out


def build_59_explorer_shade_v04(tmp: Path) -> Path:
    """#59 P4 08_explorer_shade_v04.mp4 (173 frames = 7.208333 s):
    Join clean bubble-inside-jar first 88 frames of 08_explorer_shade_t2.mp4 + 8f crossfade +
    clean bubble-inside-jar first 93 frames of 08_explorer_shade_t1.mp4 = 173 frames.
    """
    t2 = P4_RAW / "08_explorer_shade_t2.mp4"
    t1 = P4_RAW / "08_explorer_shade_t1.mp4"
    out = CLIPS_DIR / "08_explorer_shade_v04.mp4"
    d_a = tmp / "p4_59_a"
    d_b = tmp / "p4_59_b"
    d_out = tmp / "p4_59_out"
    for d in (d_a, d_b, d_out):
        d.mkdir(parents=True, exist_ok=True)

    subprocess.run(
        [
            "ffmpeg", "-y", "-v", "error",
            "-i", str(t2), "-frames:v", "88",
            "-vf", "scale=1920:1080:flags=lanczos",
            str(d_a / "f_%04d.png"),
        ],
        check=True,
    )
    subprocess.run(
        [
            "ffmpeg", "-y", "-v", "error",
            "-i", str(t1), "-frames:v", "93",
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


def build_91_gold_foil_crop_v04() -> Path:
    """#91 P5 24_gold_foil_crop_v04.mp4 (156 frames = 6.500 s):
    Crop top 14% (crop=1664:936:128:144,scale=1920:1080) to remove ceiling 'ATOMOS' sign.
    """
    src = REPO / "02_Video-Projects/004_Whats-Really-Inside-An-Atom/04_Generated-Clips/part01/raw/v01/11_gold_foil_bounce_v01.mp4"
    out = CLIPS_DIR / "24_gold_foil_crop_v04.mp4"
    subprocess.run(
        [
            "ffmpeg", "-y", "-v", "error",
            "-i", str(src),
            "-frames:v", "156",
            "-vf", "scale=1920:1080:flags=lanczos,crop=1664:936:128:144,scale=1920:1080:flags=lanczos,setsar=1",
            "-c:v", "libx264", "-preset", "medium", "-crf", "17",
            "-pix_fmt", "yuv420p", "-r", str(FPS),
            "-an", str(out),
        ],
        check=True,
    )
    return out


def main() -> None:
    CLIPS_DIR.mkdir(parents=True, exist_ok=True)
    tmp = Path("/private/tmp/hos006_clips_v04")
    if tmp.exists():
        shutil.rmtree(tmp)
    tmp.mkdir(parents=True, exist_ok=True)

    outputs = [
        (
            "#03 P1 03_pot_jar_leaf",
            render_animated_still_clip(
                STILLS_DIR / "03_pot_jar_leaf_v04.png",
                CLIPS_DIR / "03_pot_jar_leaf_v04.mp4",
                n_frames=180,
                zoom_start=1.10,
                zoom_end=1.17,
                dx_start=-16.0,
                dx_end=16.0,
                dy_start=-42.0,
                dy_end=-36.0,
                bubble_boxes=[(1345, 520, 1565, 830)],
                seed=103,
            ),
        ),
        (
            "#88 P5 21_three_objects",
            render_animated_still_clip(
                STILLS_DIR / "03_pot_jar_leaf_v04.png",
                CLIPS_DIR / "21_three_objects_v04.mp4",
                n_frames=123,
                zoom_start=1.13,
                zoom_end=1.20,
                dx_start=20.0,
                dx_end=-20.0,
                dy_start=-36.0,
                dy_end=-42.0,
                bubble_boxes=[(1345, 520, 1565, 830)],
                seed=588,
            ),
        ),
        (
            "#10 P1 10_van_helmont_sack",
            render_animated_still_clip(
                STILLS_DIR / "10_van_helmont_sack_v04.png",
                CLIPS_DIR / "10_van_helmont_sack_v04.mp4",
                n_frames=154,
                zoom_start=1.03,
                zoom_end=1.11,
                dx_start=-14.0,
                dx_end=14.0,
                dy_start=-4.0,
                dy_end=4.0,
                seed=110,
            ),
        ),
        (
            "#14 P2 02_balance_200",
            build_14_balance_200_v04(tmp),
        ),
        (
            "#15 P2 03_willow_shoot_scale",
            render_animated_still_clip(
                STILLS_DIR / "03_willow_shoot_scale_v04.png",
                CLIPS_DIR / "03_willow_shoot_scale_v04.mp4",
                n_frames=103,
                zoom_start=1.03,
                zoom_end=1.10,
                dx_start=-12.0,
                dx_end=12.0,
                dy_start=-4.0,
                dy_end=4.0,
                seed=215,
            ),
        ),
        (
            "#16 P2 04_lid_rain",
            render_animated_still_clip(
                STILLS_DIR / "04_lid_rain_v04.png",
                CLIPS_DIR / "04_lid_rain_v04.mp4",
                n_frames=153,
                zoom_start=1.03,
                zoom_end=1.11,
                dx_start=14.0,
                dx_end=-14.0,
                dy_start=-4.0,
                dy_end=4.0,
                rain_box=(670, 40, 1250, 520),
                seed=216,
            ),
        ),
        (
            "#35 P3 02_hales_branch",
            render_animated_still_clip(
                STILLS_DIR / "02_hales_branch_v04.png",
                CLIPS_DIR / "02_hales_branch_v04.mp4",
                n_frames=156,
                zoom_start=1.03,
                zoom_end=1.11,
                dx_start=-14.0,
                dx_end=14.0,
                dy_start=-4.0,
                dy_end=4.0,
                bubble_boxes=[(730, 580, 910, 815)],
                seed=335,
            ),
        ),
        (
            "#36 P3 03_water_level",
            render_animated_still_clip(
                STILLS_DIR / "03_water_level_v04.png",
                CLIPS_DIR / "03_water_level_v04.mp4",
                n_frames=125,
                zoom_start=1.04,
                zoom_end=1.12,
                dx_start=12.0,
                dx_end=-12.0,
                dy_start=4.0,
                dy_end=-4.0,
                bubble_boxes=[(815, 360, 1115, 860)],
                seed=336,
            ),
        ),
        (
            "#55 P4 04_sunny_window",
            render_animated_still_clip(
                STILLS_DIR / "04_sunny_window_v04.png",
                CLIPS_DIR / "04_sunny_window_v04.mp4",
                n_frames=109,
                zoom_start=1.03,
                zoom_end=1.10,
                dx_start=-14.0,
                dx_end=14.0,
                dy_start=-3.0,
                dy_end=3.0,
                bubble_boxes=[
                    (210, 540, 410, 825),
                    (545, 540, 735, 825),
                    (865, 540, 1055, 825),
                    (1180, 540, 1370, 825),
                    (1500, 540, 1690, 825),
                ],
                seed=455,
            ),
        ),
        (
            "#59 P4 08_explorer_shade",
            build_59_explorer_shade_v04(tmp),
        ),
        (
            "#66 P4 15_leaf_turns_sun",
            render_animated_still_clip(
                P4_FLOW_STILLS / "15_leaf_turns_sun_t1.png",
                CLIPS_DIR / "15_leaf_turns_sun_v04.mp4",
                n_frames=70,
                zoom_start=1.03,
                zoom_end=1.09,
                dx_start=-10.0,
                dx_end=10.0,
                dy_start=-3.0,
                dy_end=3.0,
                seed=466,
            ),
        ),
        (
            "#91 P5 24_gold_foil_crop",
            build_91_gold_foil_crop_v04(),
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
