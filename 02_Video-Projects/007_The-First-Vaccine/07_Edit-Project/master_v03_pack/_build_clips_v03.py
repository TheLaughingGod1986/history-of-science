#!/usr/bin/env python3
"""HOS 007 master v03 (J0887): Build replacement & tail clips at £0 / 0 Flow credits.

1. Cut #21 (P2:01_milking_dawn, 174f = 7.2500s, 100.8333..108.0833s):
   From 01_milking_dawn_v03_aligned.png (both hands gripping udder teats, milk stream straight down into pail)
   with smooth subpixel push-in, warm morning sunbeam motes, and Part 2 overlays p2_ch (0.00-1.55s) + p2_cowpox (2.10-5.50s).
2. Cut #42 (P2:14_explorer_stool, 136f = 5.6667s, 224.7917..230.4583s):
   From 14_explorer_stool_v03.png (wide byre shot, child-sized Explorer at house scale ~1/3 frame height, never dominating frame)
   with smooth subpixel push-in and warm morning sunbeam motes.
3. Cut #97 (P5:12_kite_storm, 168f = 7.0000s, 500.0833..507.0833s):
   Extended from 121f (5.0417s) to 168f (7.0000s) of 12_kite_storm_t1.mp4 so the last VO word at 504.672s breathes for 2.41s.
4. Cut #98 (P5:14_closing_card, 96f = 4.0000s, 507.0833..511.0833s):
   HOS house closing card ('Why Did Franklin Fly a Kite in a Storm?', Thu 19 Nov, 'Subscribe to see it first')
   fading in/out over moving picture (11b_storm_builds_t1.mp4 unused back half 3.80-7.80s).
5. Cuts #99..#102 (4 x 120f = 20.0000s, 511.0833..531.0833s):
   20 s of moving 3D cartoon picture for the YouTube Studio end screen, ending with a 1.5 s fade to black (529.5833..531.0833s).
"""
from __future__ import annotations

import math
import subprocess as sp
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

PACK_DIR = Path(__file__).resolve().parent
EDIT_DIR = PACK_DIR.parent
STILLS_DIR = PACK_DIR / "stills"
CLIPS_DIR = PACK_DIR / "clips"
MEDIA_DIR = Path("/Users/benjaminoats/YouTube/hos-007-vaccine/02_Video-Projects/007_The-First-Vaccine")

sys.path.insert(0, str(EDIT_DIR))
import _assemble_part_roughs_v01 as apr  # noqa: E402

W, H, FPS = 1920, 1080, 24
FONT = "/System/Library/Fonts/Supplemental/Didot.ttc"
BROWN = (61, 41, 28)
CREAM = (245, 232, 210)
GOLD = (242, 208, 122)


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
    zoom_start: float = 1.03,
    zoom_end: float = 1.10,
    dx_start: float = -10.0,
    dx_end: float = 10.0,
    dy_start: float = -3.0,
    dy_end: float = 3.0,
    milk_stream_box: tuple[int, int, int, int] | None = None,
    active_overlays: list[dict] | None = None,
    noise: np.ndarray | None = None,
    part_frame_offset: int = 0,
    seed: int = 42,
) -> Path:
    out_mp4.parent.mkdir(parents=True, exist_ok=True)
    im_src = Image.open(still_path).convert("RGB").resize((W, H), Image.Resampling.LANCZOS)
    src_rgba = im_src.convert("RGBA")

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

    milk_drops = []
    if milk_stream_box:
        sx0, sy0, sx1, sy1 = milk_stream_box
        for _ in range(22):
            up = float(rng.uniform(0.0, 1.0))
            speed = float(rng.uniform(1.8, 2.6))
            jx = float(rng.uniform(-1.5, 1.5))
            rad = float(rng.uniform(1.5, 2.5))
            milk_drops.append((sx0, sy0, sx1, sy1, up, speed, jx, rad))

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

            if milk_drops:
                ov_src = Image.new("RGBA", (W, H), (0, 0, 0, 0))
                ds = ImageDraw.Draw(ov_src)
                for sx0, sy0, sx1, sy1, up, speed, jx, rad in milk_drops:
                    prog_m = (up + t * speed) % 1.0
                    px = sx0 + (sx1 - sx0) * prog_m + jx
                    py = sy0 + (sy1 - sy0) * prog_m
                    fade = math.sin(math.pi * prog_m)
                    alpha = int(190 * fade)
                    if alpha > 10:
                        ds.ellipse(
                            (px - rad, py - rad * 2.2, px + rad, py + rad * 2.2),
                            fill=(252, 249, 242, alpha),
                        )
                comp_src = np.asarray(Image.alpha_composite(src_rgba, ov_src).convert("RGB"), dtype=np.float32)
            else:
                comp_src = np.asarray(im_src, dtype=np.float32)

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


def draw_closing_card(base: Image.Image, t: float, dur: float) -> Image.Image:
    im = base.convert("RGBA")
    a = apr.card_alpha(t, 0.0, dur, fade=0.40)
    if a <= 0.01:
        return base
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    slide = int((1.0 - apr.prog(t, 0.0, 0.48)) * 22)

    bw, bh = 1480, 500
    bx0 = (W - bw) // 2
    by0 = (H - bh) // 2 + slide
    bx1 = bx0 + bw
    by1 = by0 + bh

    bg_a = int(226 * a)
    fg_a = int(255 * a)
    d.rounded_rectangle(
        [bx0, by0, bx1, by1],
        radius=18,
        fill=(BROWN[0], BROWN[1], BROWN[2], bg_a),
        outline=(GOLD[0], GOLD[1], GOLD[2], int(215 * a)),
        width=3,
    )
    d.rounded_rectangle(
        [bx0 + 16, by0 + 16, bx1 - 16, by1 - 16],
        radius=12,
        outline=(CREAM[0], CREAM[1], CREAM[2], int(150 * a)),
        width=2,
    )
    f_hdr = apr.font(30, italic=False)
    f_sub = apr.font(38, italic=True)
    f_ttl = apr.fit_font("Why Did Franklin Fly a Kite in a Storm?", 1360, 66, 44, italic=True)
    f_ftr = apr.font(36, italic=True)

    d.text(
        (W / 2, by0 + 62),
        "HISTORY OF SCIENCE  ·  DISCOVERY. WONDER. PROOF.",
        font=f_hdr,
        fill=(GOLD[0], GOLD[1], GOLD[2], fg_a),
        anchor="mt",
    )
    span = int(460 * apr.prog(t, 0.18, 0.75))
    d.line((W / 2 - span, by0 + 118, W / 2 + span, by0 + 118), fill=(GOLD[0], GOLD[1], GOLD[2], int(190 * a)), width=2)

    d.text(
        (W / 2, by0 + 150),
        "Next film  ·  Thursday 19 November",
        font=f_sub,
        fill=(232, 216, 188, fg_a),
        anchor="mt",
    )
    d.text(
        (W / 2, by0 + 236),
        "Why Did Franklin Fly a Kite in a Storm?",
        font=f_ttl,
        fill=(CREAM[0], CREAM[1], CREAM[2], fg_a),
        anchor="mt",
    )
    d.line((W / 2 - span, by0 + 360, W / 2 + span, by0 + 360), fill=(GOLD[0], GOLD[1], GOLD[2], int(160 * a)), width=2)
    d.text(
        (W / 2, by0 + 398),
        "Subscribe to see it first  ·  @HistoryOfScienceYT",
        font=f_ftr,
        fill=(GOLD[0], GOLD[1], GOLD[2], fg_a),
        anchor="mt",
    )
    return Image.alpha_composite(im, ov).convert("RGB")


def render_closing_card_clip(src_mp4: Path, start_s: float, n_frames: int, out_mp4: Path) -> Path:
    out_mp4.parent.mkdir(parents=True, exist_ok=True)
    dur = n_frames / FPS
    dec = sp.Popen(
        [
            "ffmpeg", "-v", "error", "-ss", f"{start_s:.3f}", "-i", str(src_mp4),
            "-frames:v", str(n_frames), "-vf", f"fps={FPS},scale={W}:{H}:flags=lanczos",
            "-f", "rawvideo", "-pix_fmt", "rgb24", "-",
        ],
        stdout=sp.PIPE,
    )
    enc = sp.Popen(
        [
            "ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pixel_format", "rgb24",
            "-video_size", f"{W}x{H}", "-framerate", str(FPS), "-i", "-", "-an",
            "-c:v", "libx264", "-preset", "fast", "-crf", "17", "-pix_fmt", "yuv420p", "-r", str(FPS),
            str(out_mp4),
        ],
        stdin=sp.PIPE,
    )
    last_im = Image.new("RGB", (W, H), BROWN)
    for k in range(n_frames):
        buf = dec.stdout.read(W * H * 3) if dec.stdout else b""
        if len(buf) == W * H * 3:
            last_im = Image.frombytes("RGB", (W, H), buf)
        t = k / FPS
        frame = draw_closing_card(last_im, t, dur)
        assert enc.stdin is not None
        enc.stdin.write(frame.tobytes())
    if dec.stdout:
        dec.stdout.close()
    dec.wait()
    if enc.stdin:
        enc.stdin.close()
    if enc.wait() != 0:
        raise RuntimeError(f"Failed encoding {out_mp4}")
    return out_mp4


def main() -> int:
    CLIPS_DIR.mkdir(parents=True, exist_ok=True)
    noise = np.random.default_rng(7007).random((H, W)).astype(np.float32)

    # 1. Cut #21: 01_milking_dawn_v03.mp4 (174 frames = 7.2500 s)
    p2_ovs = [ov for ov in apr.PART_OVERLAYS[2] if ov["id"] in ("p2_ch", "p2_cowpox")]
    print("Rendering 01_milking_dawn_v03.mp4 (174 frames)...", flush=True)
    render_animated_still_clip(
        still_path=STILLS_DIR / "01_milking_dawn_v03b.png",
        out_mp4=CLIPS_DIR / "01_milking_dawn_v03.mp4",
        n_frames=174,
        zoom_start=1.02,
        zoom_end=1.10,
        dx_start=-10.0,
        dx_end=10.0,
        dy_start=-3.0,
        dy_end=3.0,
        milk_stream_box=(1014, 712, 1022, 825),
        active_overlays=p2_ovs,
        noise=noise,
        part_frame_offset=0,
        seed=721,
    )

    # 2. Cut #42: 14_explorer_stool_v03.mp4 (136 frames = 5.6667 s)
    print("Rendering 14_explorer_stool_v03.mp4 (136 frames)...", flush=True)
    render_animated_still_clip(
        still_path=STILLS_DIR / "14_explorer_stool_v03.png",
        out_mp4=CLIPS_DIR / "14_explorer_stool_v03.mp4",
        n_frames=136,
        zoom_start=1.02,
        zoom_end=1.09,
        dx_start=-10.0,
        dx_end=10.0,
        dy_start=-3.0,
        dy_end=3.0,
        milk_stream_box=None,
        active_overlays=None,
        noise=None,
        part_frame_offset=0,
        seed=742,
    )

    # 3. Cut #97: 12_kite_storm_v03.mp4 (168 frames = 7.0000 s, extended from 121f so last VO word breathes 2.41s)
    print("Rendering 12_kite_storm_v03.mp4 (168 frames)...", flush=True)
    sp.run(
        [
            "ffmpeg", "-y", "-v", "error",
            "-ss", "0.000",
            "-i", str(MEDIA_DIR / "04_Generated-Clips/part05/raw/v01/12_kite_storm_t1.mp4"),
            "-frames:v", "168",
            "-vf", f"fps={FPS},scale={W}:{H}:flags=lanczos,setsar=1,format=yuv420p",
            "-c:v", "libx264", "-preset", "fast", "-crf", "17", "-r", str(FPS), "-an",
            str(CLIPS_DIR / "12_kite_storm_v03.mp4"),
        ],
        check=True,
    )

    # 4. Cut #98: 14_closing_card_v03.mp4 (96 frames = 4.0000 s over moving storm clouds)
    print("Rendering 14_closing_card_v03.mp4 (96 frames)...", flush=True)
    render_closing_card_clip(
        src_mp4=MEDIA_DIR / "04_Generated-Clips/part05/raw/v01/11b_storm_builds_t1.mp4",
        start_s=3.800,
        n_frames=96,
        out_mp4=CLIPS_DIR / "14_closing_card_v03.mp4",
    )

    # 5. Cuts #99..#102: 20 s (4 x 120 frames = 480 frames) of moving picture for the Studio end screen + 1.5 s fade out
    endscreen_specs = [
        (
            "15_endscreen_01_v03.mp4",
            MEDIA_DIR / "04_Generated-Clips/part05/raw/v01/09_meadow_golden_t1.mp4",
            2.600,
            f"fps={FPS},scale=2074:1166:flags=lanczos,crop={W}:{H}:77:43,setsar=1,format=yuv420p",
        ),
        (
            "16_endscreen_02_v03.mp4",
            MEDIA_DIR / "04_Generated-Clips/part02/raw/v01/08a_berkeley_t1.mp4",
            2.600,
            f"fps={FPS},scale=2074:1166:flags=lanczos,crop={W}:{H}:77:43,setsar=1,format=yuv420p",
        ),
        (
            "17_endscreen_03_v03.mp4",
            MEDIA_DIR / "04_Generated-Clips/part04/raw/v01/10_garden_hut_t1.mp4",
            2.600,
            f"fps={FPS},scale=2074:1166:flags=lanczos,crop={W}:{H}:77:43,setsar=1,format=yuv420p",
        ),
        (
            "18_endscreen_04_v03.mp4",
            MEDIA_DIR / "04_Generated-Clips/part05/raw/v01/10_history_book_t1.mp4",
            2.600,
            f"fps={FPS},scale=2074:1166:flags=lanczos,crop={W}:{H}:77:43,fade=t=out:st=3.50:d=1.50,setsar=1,format=yuv420p",
        ),
    ]
    for fname, src_p, start_s, vf in endscreen_specs:
        print(f"Rendering {fname} (120 frames)...", flush=True)
        sp.run(
            [
                "ffmpeg", "-y", "-v", "error",
                "-ss", f"{start_s:.3f}",
                "-i", str(src_p),
                "-frames:v", "120",
                "-vf", vf,
                "-c:v", "libx264", "-preset", "fast", "-crf", "17", "-r", str(FPS), "-an",
                str(CLIPS_DIR / fname),
            ],
            check=True,
        )

    print("ALL 8 CLIPS RENDERED SUCCESSFULLY", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
