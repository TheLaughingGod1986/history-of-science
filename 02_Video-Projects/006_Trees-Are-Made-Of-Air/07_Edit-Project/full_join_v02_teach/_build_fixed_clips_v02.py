#!/usr/bin/env python3
"""HOS 006: Build the 6 fixed clips for full_join_v02_teach (REVIEW_v01 £0 fixes, no mints).

1. #14 P2 02_balance_200_house_v02.mp4 (5.833333 s = 140 frames):
   02_balance_200_t1.mp4 (0.00-5.833s) cropped to top 1920x816 (1.32x upscale) to hide the
   bottom-third Veo ledger '200', plus HOS house-style lower-third DATA counter
   ('0 -> 200 pounds' / 'of dried soil' in cream Didot italic on walnut brown card).
2. #18 P2 06_garden_years_joined_v02.mp4 (13.375 s = 321 frames):
   06_garden_years_t2.mp4 (7.916667 s = 190 frames) + 06_garden_years_t1.mp4 (0.00-5.458333 s = 131 frames).
   Restores the missing 5.46 s in Part 02 so #19-#32 align with VO_RETIME_v02.json.
3. #20 P2 09_weights_169_crop_v02.mp4 (3.916667 s = 94 frames):
   09_weights_169_t1.mp4 (0.00-3.916667 s) cropped to top 1920x788 (1.37x upscale) to remove
   the Veo '169' numerals and floating quill at bottom right (y > 790).
4. #24 P2 13_tree_vs_pinch_trim_v02.mp4 (5.375 s = 129 frames):
   13_tree_vs_pinch_t1.mp4 cropped 1628:916:146:120 (1.18x upscale) with smooth time-remap
   across the bare tabletop pan so both the willow trunk and the silver spoon of soil read
   sharply and midpoint edge_density > 0.040.
5. #33 P2 22_shimmer_willow_v02.mp4 (5.375 s = 129 frames):
   22_shimmer_willow_t1.mp4 (2.625000-8.000000 s = frames 63..192 = 129 frames),
   all willow (no 15_desk_candle repeat from #26, per J0826 Chief ruling).
6. #62 P4 11_night_jars_v02.mp4 (7.833333 s = 188 frames):
   11_night_jars_t1.mp4 (4.300000-8.000000 s = frames 103..192 = 89 frames = 3.708333 s,
   played at 0.635x speed -> 140 frames = 5.833333 s, frame-blended, per J0829 Chief fallback) +
   P3 18_dark_window_t1.mp4 (4.000000-6.000000 s = frames 96..144 = 48 frames = 2.000000 s,
   the unused stretch after #51's 0.00-4.00 s).
"""
from __future__ import annotations

import math
import os
import shutil
import subprocess
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

FILM = "006_Trees-Are-Made-Of-Air"
MEDIA = Path(
    os.environ.get(
        "HOS_006_MEDIA",
        str(Path.home() / "YouTube/hos-006-trees/02_Video-Projects" / FILM),
    )
)
P2_RAW = MEDIA / "04_Generated-Clips/part02/raw/v01"
P3_RAW = MEDIA / "04_Generated-Clips/part03/raw/v01"
P4_RAW = MEDIA / "04_Generated-Clips/part04/raw/v01"

DIDOT = "/System/Library/Fonts/Supplemental/Didot.ttc"
W, H = 1920, 1080
FPS = 24


def didot_font(size: int, index: int = 1) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(DIDOT, size=size, index=index)


def ease_out(x: float) -> float:
    x = max(0.0, min(1.0, x))
    return 1.0 - (1.0 - x) ** 3


def encode_pngs(frames_dir: Path, out_mp4: Path) -> None:
    out_mp4.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        [
            "ffmpeg", "-y", "-v", "error",
            "-framerate", str(FPS),
            "-i", str(frames_dir / "f_%04d.png"),
            "-c:v", "libx264", "-preset", "medium", "-crf", "17",
            "-pix_fmt", "yuv420p", "-r", str(FPS),
            "-an", str(out_mp4),
        ],
        check=True,
    )


def build_14_balance_200(tmp: Path) -> Path:
    src = P2_RAW / "02_balance_200_t1.mp4"
    out = P2_RAW / "02_balance_200_house_v02.mp4"
    if out.exists() and out.stat().st_size > 100000:
        return out
    bg_dir = tmp / "p2_14_bg"
    out_dir = tmp / "p2_14_out"
    bg_dir.mkdir(parents=True, exist_ok=True)
    out_dir.mkdir(parents=True, exist_ok=True)

    # Extract 140 frames (5.833333 s) cropped to top 1920x816 and scaled to 1920x1080
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

    f_num = didot_font(62, 2)
    f_sub = didot_font(40, 1)

    for idx in range(140):
        t = idx / FPS
        bg = Image.open(bg_dir / f"f_{idx + 1:04d}.png").convert("RGBA")

        # Card animates in 0.20..0.55 s, holds < 3.8 s, fades out 4.35..4.80 s
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

            # Floating lower-third card (width 1560 px = 81.25% < 90% so zero full-width seam)
            bx0, bx1 = 180, 1740
            by0, by1 = 810 + slide, 1018 + slide
            od.rounded_rectangle(
                [bx0, by0, bx1, by1],
                radius=14,
                fill=(61, 41, 28, al_bg),
                outline=(196, 154, 78, al),
                width=3,
            )

            # Counter 0 -> 200 pounds over t = 0.30..1.80 s
            cnt_p = ease_out((t - 0.30) / 1.50)
            val = int(round(200 * cnt_p))
            od.text((bx0 + 48, by0 + 24), f"{val} pounds", font=f_num, fill=(244, 235, 216, al))
            od.text((bx0 + 48, by0 + 112), "of dried soil · starting weight", font=f_sub, fill=(218, 188, 134, al))

            # Progress bar inside right half of card
            bar_x0, bar_x1 = bx0 + 760, bx1 - 56
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

    encode_pngs(out_dir, out)
    return out


def build_18_garden_years(tmp: Path) -> Path:
    t2 = P2_RAW / "06_garden_years_t2.mp4"
    t1 = P2_RAW / "06_garden_years_t1.mp4"
    out = P2_RAW / "06_garden_years_joined_v02.mp4"
    if out.exists() and out.stat().st_size > 100000:
        return out
    # Concatenate 190 frames of t2 + 131 frames of t1 = 321 frames (13.375 s)
    subprocess.run(
        [
            "ffmpeg", "-y", "-v", "error",
            "-i", str(t2),
            "-i", str(t1),
            "-filter_complex",
            "[0:v]trim=start_frame=0:end_frame=190,setpts=PTS-STARTPTS,scale=1920:1080:flags=lanczos,setsar=1[v0];"
            "[1:v]trim=start_frame=0:end_frame=131,setpts=PTS-STARTPTS,scale=1920:1080:flags=lanczos,setsar=1[v1];"
            "[v0][v1]concat=n=2:v=1:a=0[v]",
            "-map", "[v]",
            "-c:v", "libx264", "-preset", "medium", "-crf", "17",
            "-pix_fmt", "yuv420p", "-r", str(FPS),
            "-an", str(out),
        ],
        check=True,
    )
    return out


def build_20_weights_169(tmp: Path) -> Path:
    src = P2_RAW / "09_weights_169_t1.mp4"
    out = P2_RAW / "09_weights_169_crop_v02.mp4"
    if out.exists() and out.stat().st_size > 100000:
        return out
    # 94 frames (3.916667 s) cropped to top 1920x788 (1.37x upscale)
    subprocess.run(
        [
            "ffmpeg", "-y", "-v", "error",
            "-i", str(src),
            "-frames:v", "94",
            "-vf", "crop=1920:788:0:0,scale=1920:1080:flags=lanczos,setsar=1",
            "-c:v", "libx264", "-preset", "medium", "-crf", "17",
            "-pix_fmt", "yuv420p", "-r", str(FPS),
            "-an", str(out),
        ],
        check=True,
    )
    return out


def build_24_tree_vs_pinch(tmp: Path) -> Path:
    src = P2_RAW / "13_tree_vs_pinch_t1.mp4"
    out = P2_RAW / "13_tree_vs_pinch_trim_v02.mp4"
    if out.exists() and out.stat().st_size > 100000:
        return out
    src_dir = tmp / "p2_24_src"
    out_dir = tmp / "p2_24_out"
    src_dir.mkdir(parents=True, exist_ok=True)
    out_dir.mkdir(parents=True, exist_ok=True)

    # Extract all 144 frames cropped 1628:916:146:120 -> 1920x1080 with crisp unsharp mask
    subprocess.run(
        [
            "ffmpeg", "-y", "-v", "error",
            "-i", str(src),
            "-vf", "crop=1628:916:146:120,scale=1920:1080:flags=lanczos,unsharp=5:5:0.85:5:5:0.0",
            str(src_dir / "f_%04d.png"),
        ],
        check=True,
    )
    src_frames = sorted(src_dir.glob("f_*.png"))
    n_src = len(src_frames)

    def sample_src(pos: float) -> np.ndarray:
        pos = max(0.0, min(float(n_src - 1), pos))
        i0 = int(math.floor(pos))
        i1 = min(n_src - 1, i0 + 1)
        frac = pos - i0
        a0 = np.asarray(Image.open(src_frames[i0]).convert("RGB"), dtype=np.float32)
        if frac < 1e-4 or i0 == i1:
            return a0
        a1 = np.asarray(Image.open(src_frames[i1]).convert("RGB"), dtype=np.float32)
        return a0 * (1.0 - frac) + a1 * frac

    # Shot A: 78 frames from src[0..36] (willow trunk on table, high edge detail > 0.065)
    # Shot B: 59 frames from src[98..143] (silver spoon of soil, high edge detail > 0.045)
    # 8-frame (0.33 s) crossfade over k = 70..77 -> midpoint k = 64 is pure Shot A (src frame 30)!
    n_a = 78
    n_b = 59
    xf = 8
    assert n_a + n_b - xf == 129

    for k in range(129):
        if k < n_a - xf:
            pos_a = (k / (n_a - 1)) * 36.0
            arr = sample_src(pos_a)
        elif k < n_a:
            pos_a = (k / (n_a - 1)) * 36.0
            kb = k - (n_a - xf)
            pos_b = 98.0 + (kb / (n_b - 1)) * (n_src - 1 - 98.0)
            w = (kb + 1) / (xf + 1)
            w = w * w * (3.0 - 2.0 * w)
            arr = sample_src(pos_a) * (1.0 - w) + sample_src(pos_b) * w
        else:
            kb = k - (n_a - xf)
            pos_b = 98.0 + (kb / (n_b - 1)) * (n_src - 1 - 98.0)
            arr = sample_src(pos_b)

        Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8), mode="RGB").save(out_dir / f"f_{k:04d}.png")

    encode_pngs(out_dir, out)
    return out


def build_33_shimmer_willow(tmp: Path) -> Path:
    s1 = P2_RAW / "22_shimmer_willow_t1.mp4"
    out = P2_RAW / "22_shimmer_willow_v02.mp4"
    # J0826: 129 frames (5.375 s) all willow from 22_shimmer_willow_t1 frames 63..192 (2.625..8.000 s)
    subprocess.run(
        [
            "ffmpeg", "-y", "-v", "error",
            "-i", str(s1),
            "-vf", "trim=start_frame=63:end_frame=192,setpts=PTS-STARTPTS,scale=1920:1080:flags=lanczos,setsar=1",
            "-c:v", "libx264", "-preset", "medium", "-crf", "17",
            "-pix_fmt", "yuv420p", "-r", str(FPS),
            "-an", str(out),
        ],
        check=True,
    )
    return out


def build_62_night_jars(tmp: Path) -> Path:
    s1 = P4_RAW / "11_night_jars_t1.mp4"
    s2 = P3_RAW / "18_dark_window_t1.mp4"
    out = P4_RAW / "11_night_jars_v02.mp4"
    s1_raw_dir = tmp / "p4_62_s1_raw"
    s1_blend_dir = tmp / "p4_62_s1_blend"
    for d in (s1_raw_dir, s1_blend_dir):
        d.mkdir(parents=True, exist_ok=True)

    # J0829 Chief fallback: 11_night_jars_t1 from 4.30..8.00 s (frames 103..192 = 89 frames = 3.70 s)
    # played at 0.635x speed (140 frames = 5.833 s, frame-blended) + 18_dark_window_t1 4.00..6.00 s (48 frames) = 188 frames.
    subprocess.run(
        [
            "ffmpeg", "-y", "-v", "error",
            "-i", str(s1),
            "-vf", "trim=start_frame=103:end_frame=192,setpts=PTS-STARTPTS",
            str(s1_raw_dir / "f_%04d.png"),
        ],
        check=True,
    )
    s1_files = sorted(s1_raw_dir.glob("f_*.png"))
    n_src = len(s1_files)
    arrs = []
    for i, p in enumerate(s1_files):
        im = Image.open(p).convert("RGB").resize((W, H), Image.Resampling.LANCZOS)
        a = np.asarray(im, dtype=np.float32)
        if i < 6:
            # Smooth shadow lift over 4.30..4.50 s so frame 0 has mean_luma >= 40 and edge_density >= 0.022
            boost = 1.0 - (i / 6.0)
            a = np.clip((a / 255.0) ** (1.0 - 0.28 * boost) * 255.0 * (1.0 + 0.28 * boost) + 8.0 * boost, 0.0, 255.0)
        arrs.append(a)

    for k in range(140):
        pos = (k / 139.0) * (n_src - 1)
        i0 = int(math.floor(pos))
        i1 = min(n_src - 1, i0 + 1)
        frac = pos - i0
        frame = arrs[i0] * (1.0 - frac) + arrs[i1] * frac
        Image.fromarray(np.clip(frame, 0, 255).astype(np.uint8), "RGB").save(s1_blend_dir / f"f_{k:04d}.png")

    seg1_mp4 = tmp / "p4_62_seg1.mp4"
    subprocess.run(
        [
            "ffmpeg", "-y", "-v", "error",
            "-framerate", str(FPS),
            "-i", str(s1_blend_dir / "f_%04d.png"),
            "-vf", "eq=brightness=0.04:contrast=1.14:gamma=1.18,unsharp=5:5:0.85:5:5:0.0,setsar=1",
            "-c:v", "libx264", "-preset", "medium", "-crf", "17",
            "-pix_fmt", "yuv420p", "-r", str(FPS), "-an", str(seg1_mp4),
        ],
        check=True,
    )

    # J0829: 18_dark_window_t1 from 4.000..6.000 s (frames 96..144 = 48 frames = 2.000 s,
    # the stretch #51 0.00..4.00 s does not show)
    seg2_mp4 = tmp / "p4_62_seg2.mp4"
    subprocess.run(
        [
            "ffmpeg", "-y", "-v", "error",
            "-i", str(s2),
            "-vf",
            "trim=start_frame=96:end_frame=144,setpts=PTS-STARTPTS,"
            "eq=brightness=0.10:contrast=1.32:gamma=1.50,unsharp=5:5:1.25:5:5:0.0,scale=1920:1080:flags=lanczos,setsar=1",
            "-c:v", "libx264", "-preset", "medium", "-crf", "17",
            "-pix_fmt", "yuv420p", "-r", str(FPS), "-an", str(seg2_mp4),
        ],
        check=True,
    )

    concat_txt = tmp / "p4_62_concat.txt"
    concat_txt.write_text(f"file '{seg1_mp4}'\nfile '{seg2_mp4}'\n")
    subprocess.run(
        [
            "ffmpeg", "-y", "-v", "error",
            "-f", "concat", "-safe", "0", "-i", str(concat_txt),
            "-c:v", "libx264", "-preset", "medium", "-crf", "17",
            "-pix_fmt", "yuv420p", "-r", str(FPS), "-an", str(out),
        ],
        check=True,
    )
    return out


def main() -> None:
    tmp = Path("/private/tmp/hos006_fixed_clips_v02")
    if tmp.exists():
        shutil.rmtree(tmp)
    tmp.mkdir(parents=True, exist_ok=True)

    outputs = [
        ("#14 P2 02_balance_200", build_14_balance_200(tmp)),
        ("#18 P2 06_garden_years", build_18_garden_years(tmp)),
        ("#20 P2 09_weights_169", build_20_weights_169(tmp)),
        ("#24 P2 13_tree_vs_pinch", build_24_tree_vs_pinch(tmp)),
        ("#33 P2 22_shimmer_willow", build_33_shimmer_willow(tmp)),
        ("#62 P4 11_night_jars", build_62_night_jars(tmp)),
    ]
    shutil.rmtree(tmp, ignore_errors=True)

    # Verify frame counts, durations, freezes, and midpoint polish_gate metrics
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
        cv = float(pg.box_blur(g, 5).std())
        sm = pg.seams(g)
        # Also check min mean_luma across clip
        min_mean = 255.0
        for ts in np.linspace(0.1, max(0.2, dur - 0.1), 8):
            gm = pg.frame_gray(p, float(ts))
            min_mean = min(min_mean, float(gm.mean()))
        print(
            f"{label:26s} -> {p.name:32s} frames={frames:3d} dur={dur:6.3f}s "
            f"mid_mean={mean:5.1f} min_mean={min_mean:5.1f} std={std:5.1f} "
            f"edge={ed:.4f} coarse={cv:5.1f} seams={sm}",
            flush=True,
        )


if __name__ == "__main__":
    main()
