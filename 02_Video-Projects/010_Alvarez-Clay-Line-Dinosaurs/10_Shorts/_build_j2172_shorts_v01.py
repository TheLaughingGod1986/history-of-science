#!/usr/bin/env python3
"""J2172: Assemble HOS 010 Shorts A and C at 936x1664 (2.311x, £0, 0 credits).

- Short A ("What Killed the Dinosaurs?") -> hos_010_short_A_v01.mp4 (23.289 s)
  Uses accepted VO hos_010_short_A_v02 with approved J1004 Option A1
  (6 word-preserving silence trims = -0.260 s + 1.06x on S1 -> hook ends 2.849 s,
  body at 1.00x -> VO 22.289 s + 1.000 s loop tail = 23.289 s).
- Short C ("Are Birds Really Dinosaurs?") -> hos_010_short_C_v01.mp4 (23.560 s)
  Uses accepted VO hos_010_short_C_v02 at 1.00x (hook ends 1.780 s, S01 cuts 1.880 s,
  VO 22.560 s + 1.000 s loop tail = 23.560 s).
- Uses the 12/12 KEEP moving Flow plates locked in J2915_R1_R6_REVIEW_v01.json (PR #605),
  plus two £0 full-bleed 936x1664 portrait house period-notebook teach graphics derived
  from locked P4:01_iridium_spike and P5:11_why_survive (leaving all 16:9 Long assets untouched).
- Synthesises two distinct £0 HOS period chamber score beds and mixes with the £0 HOS house SFX kit.
- Runs polish_gate.py, picture_qa.py, music_gate.py, sfx_kit.py level, vo_check_py312.sh,
  and gate_shorts_open.py check, then stages durable SHA-256-verified copies to studio-live on the NAS.
"""
from __future__ import annotations

import hashlib
import json
import math
import os
import shutil
import struct
import subprocess
import sys
import wave
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
PROJ = HERE.parent
REPO = PROJ.parents[1]
OWB = Path("/Users/benjaminoats/YouTube/orbit-with-ben")
NAS_PROJ = Path("/Volumes/data/studio-live/History Of Science/02_Video-Projects/010_Alvarez-Clay-Line-Dinosaurs")
SCRATCH_ROOT = Path(os.environ.get("STUDIO_SCRATCH", "/private/tmp")) / "J2172-build"

W, H, FPS = 936, 1664, 30
BAND_H = W * 9 // 16          # 526 px
BAND_TOP = (H - BAND_H) // 2  # 569 px
UPSCALE_PLATE = round(H / 720.0, 4)  # 2.3111 <= 2.35

FONT = "/System/Library/Fonts/Supplemental/Didot.ttc"
CREAM = (245, 232, 210, 255)
WHITE = (252, 248, 240, 255)
INK = (24, 20, 18, 255)
YEL = (255, 224, 0, 255)  # #FFE000 per Rule 24

LONG_TITLE = "What Killed the Dinosaurs Was Hidden in a Line of Clay"
TITLE_IN, TITLE_OUT = 9.0, 14.0

LOCKED_PLATES = {
    "P1:01_clay_line": ("archive_v01_twelve_plates", "P01_01_clay_line_t1.mp4", "927e826b3fe8f83c66a879b2e9a932b683d711d91c075fc235a6a4012dd0338b", "codex"),
    "P2:01_walter_hammer": ("archive_v01_twelve_plates", "P02_01_walter_hammer_t1.mp4", "db506d28c3abd7ee5c441e22e0bdb55494b715e4811163885b7cfd2d5ade60f6", "codex"),
    "P2:03_tiny_shells": ("archive_v01_twelve_plates", "P02_03_tiny_shells_t1.mp4", "1c32a8521956d95ccc6922e6220a84b568ae02ddcb43662c7ee41c810beca205", "codex"),
    "P3:08_asaro_michel": ("archive_v01_twelve_plates", "P03_08_asaro_michel_t1.mp4", "2c512d8bc8bf29b4bfbac37aa9eae1bdebdd4bb14fbfe64256cc2ac1ab0d5d18", "codex"),
    "P5:09a_pigeon_pavement": ("archive_v01_twelve_plates", "P05_09a_pigeon_pavement_t1.mp4", "0a9797df0ac726b20aab4c358e498f7fdf62aa96f85f0a7238193c2db5e3b59a", "gemini"),
    "P5:13a_gull_seaside": ("archive_v01_twelve_plates", "P05_13a_gull_seaside_t1.mp4", "893b17b8d5f3f0b9b5e245688d17145dfa3933f09e027f124acd8593de74b74a", "gemini"),
    "P2:05_almost_none": ("archive_v02_r1_r6_plates", "P02_05_almost_none_t2.mp4", "eda112847953e75d97f970add475552c5fb527f3b7c04abae8f0cda035eca330", "gemini"),
    "P4:06_dust_veil": ("archive_v02_r1_r6_plates", "P04_06_dust_veil_t2.mp4", "1898afb6b8d89d57a818dd340b6e327733b67717b81e9581ca43ae539562e082", "gemini"),
    "P5:08_all_at_once": ("archive_v02_r1_r6_plates", "P05_08_all_at_once_t2.mp4", "ab9d8eb7690fbb0542db508b5f1cf41a39f5c45210e40d7c574c2224ee27b7aa", "gemini"),
    "P5:12_clay_callback": ("archive_v02_r1_r6_plates", "P05_12_clay_callback_t2.mp4", "37cf7962a646ff073af3e7f5db74d7c565f2dd613b5cdaea33c7cd63ce2034dc", "gemini"),
    "P5:10_explorer_robin": ("archive_v02_r1_r6_plates", "P05_10_explorer_robin_t2.mp4", "fc1485661a50a4d072257f3e3b422221a2674a1ec23e9018361dfd283f666969", "gemini"),
    "P5:09_robin": ("archive_v02_r1_r6_plates", "P05_09_robin_t2.mp4", "172a0a9561a1c25191caf84188b3e492493b31ffd46e1fbfdffb216d911da824", "gemini"),
}

PARENT_CODE_GRAPHICS = {
    "P4:01_iridium_spike": ("code_graphic_010_p4_01_iridium_spike.mp4", "f9b504cf26e927d988a55aea58b4b2173660c2188b0ca94561e2c85479c2fd84"),
    "P5:11_why_survive": ("code_graphic_010_p5_11_why_survive.mp4", "0e71b03e41d0b16bb92afeb318798f796c06ae9cb78bdb776eba0e4f99940acd"),
}


def ff(*args: str, cwd: Path | None = None) -> None:
    subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", *args], check=True, cwd=cwd)


def probe(path: Path) -> float:
    return float(
        subprocess.check_output(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)],
            text=True,
        ).strip()
    )


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def ease(x: float) -> float:
    x = max(0.0, min(1.0, x))
    return x * x * (3.0 - 2.0 * x)


def prog(t: float, a: float, b: float) -> float:
    return ease((t - a) / (b - a)) if b > a else 1.0


def col(rgb: tuple[int, int, int], a: float = 1.0) -> tuple[int, int, int, int]:
    return (rgb[0], rgb[1], rgb[2], int(max(0, min(255, round(255 * a)))))


# ---------------------------------------------------------------------------
# £0 Full-bleed 936x1664 portrait house period-notebook code graphics
# ---------------------------------------------------------------------------

def make_parchment_bg(seed: int) -> Image.Image:
    """Warm textured period naturalist paper with organic multi-scale fibers (full-bleed 936x1664)."""
    rng = np.random.default_rng(seed)
    y, x = np.mgrid[:H, :W].astype(np.float32)
    nx = (x - W / 2.0) / (W / 2.0)
    ny = (y - H / 2.0) / (H / 2.0)
    vig = np.clip(0.55 * nx * nx + 0.50 * ny * ny, 0.0, 1.2)
    # Multi-scale organic mottled paper grain so coarse 8x check and full-bleed sharpness both pass cleanly
    coarse = rng.normal(0.0, 9.5, (H // 16 + 2, W // 16 + 2)).astype(np.float32)
    coarse_img = np.array(
        Image.fromarray(np.uint8(np.clip(128 + coarse * 3, 0, 255)), "L").resize((W, H), Image.BICUBIC),
        dtype=np.float32,
    ) - 128.0
    med = rng.normal(0.0, 6.0, (H // 4 + 2, W // 4 + 2)).astype(np.float32)
    med_img = np.array(
        Image.fromarray(np.uint8(np.clip(128 + med * 3, 0, 255)), "L").resize((W, H), Image.BICUBIC),
        dtype=np.float32,
    ) - 128.0
    fine = rng.normal(0.0, 2.2, (H, W)).astype(np.float32)

    base = np.array([232.0, 213.0, 181.0], np.float32)
    dark = np.array([52.0, 46.0, 38.0], np.float32)
    out = np.zeros((H, W, 3), np.float32)
    tex = 0.35 * coarse_img + 0.35 * med_img + fine
    for c in range(3):
        out[:, :, c] = base[c] - dark[c] * vig * 0.55 + tex * (1.0, 0.92, 0.80)[c]
    return Image.fromarray(np.uint8(np.clip(out, 0, 255)), "RGB")


def render_iridium_spike_9x16(out_mp4: Path, out_jpg: Path, dur: float = 2.900) -> dict:
    """Short A S06 (2.900 s): Gubbio rock column + dark clay seam + animated 30x iridium spike on period paper."""
    bg = make_parchment_bg(10104)
    sepia = (64, 46, 34)
    clay_dark = (54, 40, 32)
    ochre = (182, 118, 28)
    gold_hi = (232, 174, 48)
    limestone = (148, 126, 98)

    # Pre- pick organic fossil shell coordinates below the clay band (y = 940..1590)
    rng = np.random.default_rng(1980)
    shells = [
        (int(rng.uniform(70, W - 70)), int(rng.uniform(950, H - 70)), int(rng.uniform(10, 22)), float(rng.uniform(0, 6.28)))
        for _ in range(68)
    ]
    # Sparse tiny specks in upper Paleogene limestone (y = 70..800) + diagonal notebook margin sketches
    upper_specks = [
        (int(rng.uniform(80, W - 80)), int(rng.uniform(80, 790)), int(rng.uniform(3, 6)))
        for _ in range(18)
    ]

    n_frames = int(round(dur * FPS))
    hero_idx = int(round(2.10 * FPS))
    out_mp4.parent.mkdir(parents=True, exist_ok=True)
    enc = subprocess.Popen(
        [
            "ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pixel_format", "rgb24",
            "-video_size", f"{W}x{H}", "-framerate", str(FPS), "-i", "-", "-an",
            "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p",
            "-movflags", "+faststart", str(out_mp4),
        ],
        stdin=subprocess.PIPE,
    )
    assert enc.stdin is not None
    font_lbl = ImageFont.truetype(FONT, int(BAND_H * 0.115), index=1)  # Didot Italic, ~60 px (11.4% of band)

    for fi in range(n_frames):
        t = fi / FPS
        im = bg.copy().convert("RGBA")
        ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        d = ImageDraw.Draw(ov)

        # Wavy organic limestone bedding lines from top (y=55) to bottom (y=1610) — never straight horizontal seams
        for k, y_base in enumerate(range(65, H - 45, 78)):
            pts = [
                (
                    xx,
                    y_base
                    + 14.0 * math.sin(xx * 0.011 + k * 0.85)
                    + 7.0 * math.cos(xx * 0.023 - k * 0.4 + t * 0.35),
                )
                for xx in range(24, W - 20, 24)
            ]
            d.line(pts, fill=col(limestone, 0.52), width=3)

        # Curved naturalist-notebook frame arcs in corners (adds crisp organic ink detail top & bottom)
        for cy_arc, flip in ((120, 1), (H - 120, -1)):
            arc_pts = [
                (xx, cy_arc + flip * 26.0 * math.sin((xx / W) * math.pi))
                for xx in range(60, W - 56, 20)
            ]
            d.line(arc_pts, fill=col(sepia, 0.42), width=3)

        # Dark 1-cm Gubbio K-Pg clay boundary band (wavy organic stratum around y=880)
        top_clay = [
            (xx, 858 + 11.0 * math.sin(xx * 0.012 + 0.4) + 4.0 * math.sin(xx * 0.029))
            for xx in range(0, W + 24, 24)
        ]
        bot_clay = [
            (xx, 912 + 11.0 * math.sin(xx * 0.012 + 0.4) + 5.0 * math.cos(xx * 0.027))
            for xx in reversed(range(0, W + 24, 24))
        ]
        d.polygon(top_clay + bot_clay, fill=col(clay_dark, 0.84))
        d.line(top_clay, fill=col(sepia, 0.92), width=4)
        d.line(list(reversed(bot_clay)), fill=col(sepia, 0.92), width=4)

        # Tiny inked foraminifera / fossil shells below the clay boundary (Cretaceous)
        for sx, sy, sr, ang in shells:
            wob = 1.5 * math.sin(t * 2.0 + ang)
            d.arc((sx - sr, sy - sr + wob, sx + sr, sy + sr + wob), start=20, end=315, fill=col(sepia, 0.62), width=3)
            d.ellipse((sx - 3, sy - 3 + wob, sx + 3, sy + 3 + wob), fill=col(sepia, 0.52))

        # Almost none above (Paleogene)
        for ux, uy, ur in upper_specks:
            d.ellipse((ux - ur, uy - ur, ux + ur, uy + ur), outline=col(limestone, 0.42), width=2)

        # Animated iridium trace: baseline down rock column, surging 30x horizontally/upward at the clay band!
        # Trace runs from bottom (y=1520) up to top (y=240), with x baseline at 165 surging to x=795 at y=885!
        n_pts = 84
        pts_trace = []
        for i in range(n_pts):
            u = i / (n_pts - 1)
            yy = 1520.0 - u * (1520.0 - 250.0)
            dist = abs(yy - 885.0)
            spike = math.exp(-((dist / 36.0) ** 2))
            xx = 165.0 + 10.0 * math.sin(yy * 0.03) + spike * 630.0
            pts_trace.append((xx, yy))

        draw_n = max(2, int(prog(t, 0.08, 2.15) * (n_pts - 1)))
        d.line(pts_trace[: draw_n + 1], fill=col(sepia, 0.95), width=11)
        d.line(pts_trace[: draw_n + 1], fill=col(ochre, 0.98), width=6)

        # Peak highlight dot once trace crosses y=885 (around u=0.50 -> t ~ 1.15 s)
        peak_idx = min(range(n_pts), key=lambda i: abs(pts_trace[i][1] - 885.0))
        if draw_n >= peak_idx:
            px, py = pts_trace[peak_idx]
            pulse = 14.0 + 4.0 * math.sin(t * 5.0)
            d.ellipse((px - pulse, py - pulse, px + pulse, py + pulse), fill=col(gold_hi, 0.95), outline=col(sepia, 1.0), width=4)

        # Single built-in house label inside 16:9 center band: "ABOUT 30 TIMES" (3 words <= 4 words)
        lbl_a = prog(t, 0.30, 0.68) * (1.0 - prog(t, dur - 0.42, dur - 0.05))
        if lbl_a > 0.02:
            ly = BAND_TOP + 76
            d.text(
                (W * 0.56, ly),
                "ABOUT 30 TIMES",
                font=font_lbl,
                fill=col((250, 240, 215), lbl_a),
                anchor="mm",
                stroke_width=4,
                stroke_fill=col((36, 26, 18), lbl_a),
            )

        frame_rgb = Image.alpha_composite(im, ov).convert("RGB")
        if fi == hero_idx:
            frame_rgb.save(out_jpg, quality=92)
        enc.stdin.write(frame_rgb.tobytes())

    enc.stdin.close()
    if enc.wait() != 0:
        raise SystemExit("ffmpeg encode failed on iridium_spike_9x16")
    return {"file": str(out_mp4), "sha256": sha256(out_mp4), "duration_s": round(probe(out_mp4), 3)}


def _draw_bird_icon(d: ImageDraw.ImageDraw, cx: float, cy: float, a: float, t: float) -> None:
    if a <= 0.01:
        return
    sepia = col((58, 42, 30), a)
    fill_c = col((198, 152, 92), 0.55 * a)
    wing_lift = 6.0 * math.sin(t * 4.2)
    d.ellipse((cx - 102, cy - 102, cx + 102, cy + 102), fill=col((170, 140, 102), 0.28 * a), outline=sepia, width=4)
    # Body + head + beak + tail + feathered wing
    d.ellipse((cx - 42, cy - 14, cx + 28, cy + 28), fill=fill_c, outline=sepia, width=5)
    d.ellipse((cx + 14, cy - 38, cx + 52, cy - 4), fill=fill_c, outline=sepia, width=5)
    d.polygon([(cx + 50, cy - 24), (cx + 74, cy - 18), (cx + 50, cy - 12)], fill=col((204, 134, 42), a), outline=sepia)
    d.line([(cx - 40, cy + 4), (cx - 76, cy - 12)], fill=sepia, width=5)
    d.arc((cx - 32, cy - 46 + wing_lift, cx + 24, cy + 12 + wing_lift), start=190, end=350, fill=sepia, width=5)
    d.line([(cx - 8, cy + 28), (cx - 14, cy + 54), (cx + 10, cy + 28), (cx + 6, cy + 54)], fill=sepia, width=4)


def _draw_seed_icon(d: ImageDraw.ImageDraw, cx: float, cy: float, a: float) -> None:
    if a <= 0.01:
        return
    sepia = col((58, 42, 30), a)
    fill_c = col((196, 156, 94), 0.58 * a)
    d.ellipse((cx - 98, cy - 98, cx + 98, cy + 98), fill=col((170, 140, 102), 0.28 * a), outline=sepia, width=4)
    d.ellipse((cx - 30, cy - 46, cx + 30, cy + 48), fill=fill_c, outline=sepia, width=5)
    for yy in (-22, 0, 22):
        d.arc((cx - 24, cy + yy - 10, cx + 24, cy + yy + 12), start=15, end=165, fill=sepia, width=3)
    d.line([(cx, cy - 46), (cx + 10, cy - 72)], fill=sepia, width=5)


def _draw_burrow_icon(d: ImageDraw.ImageDraw, cx: float, cy: float, a: float) -> None:
    if a <= 0.01:
        return
    sepia = col((58, 42, 30), a)
    fill_c = col((126, 96, 70), 0.62 * a)
    d.ellipse((cx - 98, cy - 98, cx + 98, cy + 98), fill=col((170, 140, 102), 0.28 * a), outline=sepia, width=4)
    d.pieslice((cx - 58, cy - 30, cx + 58, cy + 56), start=180, end=360, fill=fill_c, outline=sepia, width=5)
    d.line([(cx - 72, cy + 14), (cx + 72, cy + 14)], fill=sepia, width=5)
    d.ellipse((cx - 18, cy - 8, cx - 4, cy + 6), fill=col((244, 228, 195), a))
    d.ellipse((cx + 4, cy - 8, cx + 18, cy + 6), fill=col((244, 228, 195), a))


def render_why_survive_9x16(out_mp4: Path, out_jpg: Path, dur: float = 2.720) -> dict:
    """Short C S03 (2.720 s): all 3 survivors (feathered bird, seed, burrow) + protective arch on 936x1664 paper."""
    bg = make_parchment_bg(10511)
    sepia = (64, 46, 34)
    ochre = (186, 124, 34)
    slate_ash = (96, 84, 72)
    earth_line = (128, 102, 76)
    ash_rng = np.random.default_rng(511)
    ash_particles = [
        (float(ash_rng.uniform(55, W - 55)), float(ash_rng.uniform(0, 420)), float(ash_rng.uniform(75.0, 120.0)))
        for _ in range(32)
    ]

    n_frames = int(round(dur * FPS))
    hero_idx = int(round(2.15 * FPS))
    out_mp4.parent.mkdir(parents=True, exist_ok=True)
    enc = subprocess.Popen(
        [
            "ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pixel_format", "rgb24",
            "-video_size", f"{W}x{H}", "-framerate", str(FPS), "-i", "-", "-an",
            "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p",
            "-movflags", "+faststart", str(out_mp4),
        ],
        stdin=subprocess.PIPE,
    )
    assert enc.stdin is not None

    for fi in range(n_frames):
        t = fi / FPS
        im = bg.copy().convert("RGBA")
        ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        d = ImageDraw.Draw(ov)

        # Falling impact-winter ash streaks & swirling dust arcs across upper sky (y = 55..540)
        for k in range(4):
            y_cloud = 110 + k * 95
            pts_c = [
                (xx, y_cloud + 22.0 * math.sin(xx * 0.013 + k + t * 0.9))
                for xx in range(30, W - 26, 24)
            ]
            d.line(pts_c, fill=col(slate_ash, 0.45), width=4)
        for ax, ay0, spd in ash_particles:
            ay = 65.0 + ((ay0 + t * spd) % 425.0)
            d.line((ax, ay, ax - 16, ay + 32), fill=col(slate_ash, 0.58), width=3)

        # Wavy earthen soil & root strata across lower page (y = 1090..1610)
        for k, y_soil in enumerate(range(1100, H - 45, 72)):
            pts_s = [
                (
                    xx,
                    y_soil
                    + 16.0 * math.sin(xx * 0.012 + k * 1.1)
                    + 6.0 * math.cos(xx * 0.025 - t * 0.5),
                )
                for xx in range(24, W - 20, 24)
            ]
            d.line(pts_s, fill=col(earth_line, 0.58), width=4)

        # Protective earthen shelter arch drawing over all three survivors (x = 70..866, y = 510..1080)
        arc_p = prog(t, 0.12, 1.55)
        if arc_p > 0.01:
            end_deg = int(190 + 160 * arc_p)
            d.arc((68, 505, W - 68, 1140), start=190, end=end_deg, fill=col(sepia, 0.92), width=10)
            d.arc((92, 530, W - 92, 1120), start=193, end=max(195, end_deg - 3), fill=col(ochre, 0.90), width=6)

        # All three survival icons inside 936 px width, well above the 81% (1348 px) caption zone!
        _draw_bird_icon(d, 215.0, 855.0, prog(t, 0.08, 0.78), t)
        _draw_seed_icon(d, 468.0, 775.0, prog(t, 0.38, 1.12))
        _draw_burrow_icon(d, 721.0, 865.0, prog(t, 0.68, 1.45))

        frame_rgb = Image.alpha_composite(im, ov).convert("RGB")
        if fi == hero_idx:
            frame_rgb.save(out_jpg, quality=92)
        enc.stdin.write(frame_rgb.tobytes())

    enc.stdin.close()
    if enc.wait() != 0:
        raise SystemExit("ffmpeg encode failed on why_survive_9x16")
    return {"file": str(out_mp4), "sha256": sha256(out_mp4), "duration_s": round(probe(out_mp4), 3)}


# ---------------------------------------------------------------------------
# Audio: Option A1 VO, £0 synthesised distinct HOS score beds, and house SFX
# ---------------------------------------------------------------------------

def build_short_a_vo(src_wav: Path, dst_wav: Path, speech_only_wav: Path, total_dur: float) -> list[tuple[str, float, float]]:
    """Apply exact J1004 Option A1 word-preserving pause trims + 1.06x on S1, 1.00x on body."""
    stt_path = PROJ / "10_Shorts/vo_v02/stt/hos_010_short_A_v02/stt_raw.json"
    raw_words = [
        (w["text"].strip(), float(w["start"]), float(w["end"]))
        for w in json.loads(stt_path.read_text())["words"]
        if (w.get("text") or "").strip()
    ]
    removals = [(0.00, 0.08), (0.64, 0.68), (1.08, 1.10), (1.44, 1.50), (1.98, 2.00), (2.42, 2.46)]
    kept = [(0.08, 0.64), (0.68, 1.08), (1.10, 1.44), (1.50, 1.98), (2.00, 2.42), (2.46, 3.28)]
    hook_atempo = 1.06
    body_shift = -0.431

    fc_parts = []
    labels = []
    for i, (a, b) in enumerate(kept):
        d_seg = round(b - a, 4)
        fc_parts.append(
            f"[0:a]atrim={a:.3f}:{b:.3f},asetpts=PTS-STARTPTS,"
            f"afade=t=in:d=0.004,afade=t=out:st={max(0.005, d_seg - 0.004):.4f}:d=0.004,"
            f"aformat=sample_rates=48000:channel_layouts=stereo[h{i}]"
        )
        labels.append(f"[h{i}]")
    fc_parts.append(
        "".join(labels)
        + f"concat=n={len(labels)}:v=0:a=1,atempo={hook_atempo},atrim=0:2.849,asetpts=PTS-STARTPTS[hook]"
    )
    fc_parts.append(
        "[0:a]atrim=3.280:22.720,asetpts=PTS-STARTPTS,"
        "afade=t=in:d=0.005,aformat=sample_rates=48000:channel_layouts=stereo[body]"
    )
    fc_parts.append("[hook][body]concat=n=2:v=0:a=1[speech]")
    ff("-i", str(src_wav), "-filter_complex", ";".join(fc_parts), "-map", "[speech]", "-c:a", "pcm_s16le", str(speech_only_wav))
    ff(
        "-i", str(speech_only_wav),
        "-af", f"apad=whole_dur={total_dur:.3f}",
        "-t", f"{total_dur:.3f}",
        "-c:a", "pcm_s16le",
        str(dst_wav),
    )

    def map_t(t_raw: float) -> float:
        if t_raw <= 3.28:
            rem = sum(max(0.0, min(t_raw, b) - a) for a, b in removals if a < t_raw)
            return round((t_raw - rem) / hook_atempo, 3)
        return round(t_raw + body_shift, 3)

    return [(w, map_t(s), map_t(e)) for w, s, e in raw_words]


def build_short_c_vo(src_wav: Path, dst_wav: Path, speech_only_wav: Path, total_dur: float) -> list[tuple[str, float, float]]:
    stt_path = PROJ / "10_Shorts/vo_v02/stt/hos_010_short_C_v02/stt_raw.json"
    raw_words = [
        (w["text"].strip(), float(w["start"]), float(w["end"]))
        for w in json.loads(stt_path.read_text())["words"]
        if (w.get("text") or "").strip()
    ]
    ff("-i", str(src_wav), "-ar", "48000", "-ac", "2", "-c:a", "pcm_s16le", str(speech_only_wav))
    ff(
        "-i", str(speech_only_wav),
        "-af", f"apad=whole_dur={total_dur:.3f}",
        "-t", f"{total_dur:.3f}",
        "-c:a", "pcm_s16le",
        str(dst_wav),
    )
    return raw_words


def synth_bed_short_a(path: Path, dur: float, sr: int = 48000) -> None:
    """A-minor / F-major / C-major / E7 chamber harp + warm cello fifths at 72 BPM (£0 own synthesis)."""
    total = dur + 0.5
    n = int(sr * total)
    t = np.arange(n, dtype=np.float64) / sr
    beat = 60.0 / 72.0
    # 8-beat chord cycle (A2-E3-C4, F2-C3-A3, C3-G3-E4, E2-B2-G#3)
    chords = [
        (110.00, 164.81, 261.63, 329.63),
        (87.31, 130.81, 220.00, 349.23),
        (130.81, 196.00, 329.63, 392.00),
        (82.41, 123.47, 207.65, 329.63),
    ]
    beat_idx = (t / beat).astype(np.int64)
    phase = (t / beat) - beat_idx
    chord_idx = (beat_idx // 2) % len(chords)
    arp_step = beat_idx % 4

    sig = np.zeros(n, dtype=np.float64)
    for ci, ch in enumerate(chords):
        mask_c = chord_idx == ci
        if not np.any(mask_c):
            continue
        tt = t[mask_c]
        ph = phase[mask_c]
        st = arp_step[mask_c]
        # Warm sustained cello drone on root + fifth
        drone = 0.28 * np.sin(2 * np.pi * ch[0] * tt) + 0.14 * np.sin(2 * np.pi * ch[1] * tt)
        # Chamber harp pluck on beat
        f_note = np.choose(st, ch)
        env = np.exp(-3.1 * ph) * np.minimum(1.0, ph / 0.015)
        pluck = env * (
            0.48 * np.sin(2 * np.pi * f_note * tt)
            + 0.16 * np.sin(2 * np.pi * f_note * 2.0 * tt)
            + 0.05 * np.sin(2 * np.pi * f_note * 3.0 * tt)
        )
        sig[mask_c] = drone + pluck

    fade = np.minimum(1.0, t / 0.35) * np.minimum(1.0, np.maximum(0.0, (total - t) / 0.40))
    sig = np.clip(sig * fade * 0.22, -0.95, 0.95)
    pcm = np.int16(sig * 32767)
    stereo = np.column_stack([pcm, pcm]).ravel()
    path.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(path), "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(sr)
        w.writeframes(stereo.tobytes())


def synth_bed_short_c(path: Path, dur: float, sr: int = 48000) -> None:
    """G-major / E-minor / C-major / D-major morning celesta + warm woodwind fifths at 76 BPM (£0 own synthesis)."""
    total = dur + 0.5
    n = int(sr * total)
    t = np.arange(n, dtype=np.float64) / sr
    beat = 60.0 / 76.0
    chords = [
        (196.00, 293.66, 392.00, 493.88),
        (164.81, 246.94, 329.63, 392.00),
        (130.81, 196.00, 261.63, 392.00),
        (146.83, 220.00, 293.66, 369.99),
    ]
    beat_idx = (t / beat).astype(np.int64)
    phase = (t / beat) - beat_idx
    chord_idx = (beat_idx // 2) % len(chords)
    arp_step = (beat_idx * 3 + 1) % 4

    sig = np.zeros(n, dtype=np.float64)
    for ci, ch in enumerate(chords):
        mask_c = chord_idx == ci
        if not np.any(mask_c):
            continue
        tt = t[mask_c]
        ph = phase[mask_c]
        st = arp_step[mask_c]
        pad = 0.24 * np.sin(2 * np.pi * ch[0] * tt) + 0.15 * np.sin(2 * np.pi * (ch[1] * 0.5) * tt)
        f_note = np.choose(st, ch)
        env = np.exp(-3.8 * ph) * np.minimum(1.0, ph / 0.012)
        celesta = env * (
            0.44 * np.sin(2 * np.pi * f_note * tt)
            + 0.12 * np.sin(2 * np.pi * f_note * 2.0 * tt)
            + 0.06 * np.sin(2 * np.pi * f_note * 4.0 * tt)
        )
        sig[mask_c] = pad + celesta

    fade = np.minimum(1.0, t / 0.35) * np.minimum(1.0, np.maximum(0.0, (total - t) / 0.40))
    sig = np.clip(sig * fade * 0.22, -0.95, 0.95)
    pcm = np.int16(sig * 32767)
    stereo = np.column_stack([pcm, pcm]).ravel()
    path.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(path), "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(sr)
        w.writeframes(stereo.tobytes())


def place_sfx(kit_dir: Path, dst: Path, total: float, events: list[tuple[str, float, float, float]]) -> Path:
    """events: [(kind 'whoosh'|'tick'|'rumble', start_s, gain_db, max_dur_s)]."""
    files = {
        "whoosh": kit_dir / "sfx_hos_whoosh_soft_v01.wav",
        "tick": kit_dir / "sfx_hos_tick_ink_v01.wav",
        "rumble": kit_dir / "sfx_hos_rumble_low_v01.wav",
    }
    inputs = ["-f", "lavfi", "-t", f"{total:.3f}", "-i", "anullsrc=channel_layout=stereo:sample_rate=48000"]
    fc = []
    mix_labels = ["[0:a]"]
    for idx, (kind, st, gdb, mdur) in enumerate(events, start=1):
        inputs += ["-i", str(files[kind])]
        ms = max(0, int(round(st * 1000)))
        fc.append(
            f"[{idx}:a]atrim=0:{mdur:.3f},asetpts=PTS-STARTPTS,"
            f"afade=t=out:st={max(0.02, mdur - 0.25):.3f}:d=0.22,"
            f"volume={gdb:.1f}dB,adelay={ms}|{ms}[e{idx}]"
        )
        mix_labels.append(f"[e{idx}]")
    fc.append("".join(mix_labels) + f"amix=inputs={len(mix_labels)}:normalize=0:duration=first,alimiter=limit=0.5[a]")
    ff(*inputs, "-filter_complex", ";".join(fc), "-map", "[a]", "-c:a", "pcm_s16le", str(dst))
    return dst


# ---------------------------------------------------------------------------
# Typography & Overlays (936x1664 house Didot)
# ---------------------------------------------------------------------------

def chunk_words(ws: list[tuple[str, float, float]], total: float) -> list[dict]:
    chunks, i, n = [], 0, len(ws)
    while i < n:
        t0 = ws[i][1]
        parts, t_end, j = [ws[i][0]], ws[i][2], i + 1
        while j < n:
            wj, sj, ej = ws[j]
            if parts[-1][-1:] in ".?!":
                break
            if parts[-1][-1:] in ",;:" and sj - t0 >= 0.45 and (len(parts) >= 2 or wj[:1].isupper()):
                break
            if len(parts) >= 5 and sj - t0 >= 0.45:
                break
            if ej - t0 >= 1.55 and len(parts) >= 2:
                break
            parts.append(wj)
            t_end = ej
            j += 1
        t1 = min(ws[j][1], t_end + 0.22) if j < n else t_end + 0.22
        t0_show = max(t0, 2.0)  # 0-2 s is the frame-0 hook caption only
        if t1 > t0_show + 0.12:
            chunks.append({
                "text": " ".join(parts),
                "t0": round(t0_show, 3),
                "t1": round(min(t1, total - 0.05), 3),
            })
        i = j
    return chunks


def render_hook(path: Path, hook_markup: str, *, top_frac: float = 0.145, cap_frac: float = 0.090) -> dict:
    """Render 2-word hook in upper-middle band (8-10% H cap height) clear of the hero subject."""
    size = 104
    while True:
        font = ImageFont.truetype(FONT, size, index=2)
        cap = -font.getbbox("H", anchor="ls")[1]
        if cap >= cap_frac * H:
            break
        size += 2
    tokens = [(w.strip("*"), w.startswith("**")) for w in hook_markup.split()]
    pitch = round(cap * 1.18)
    block = pitch * (len(tokens) - 1) + cap
    top = int(H * top_frac)
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    widest = max(font.getlength(t) for t, _ in tokens)
    for k, (t_str, hot) in enumerate(tokens):
        base = top + cap + k * pitch
        draw.text(
            (W / 2, base),
            t_str,
            font=font,
            anchor="ms",
            fill=YEL if hot else WHITE,
            stroke_width=7,
            stroke_fill=INK,
        )
    img.save(path)
    return {
        "font_size": size,
        "cap_px": cap,
        "cap_pct": round(100 * cap / H, 2),
        "block_pct": [round(100 * top / H, 1), round(100 * (top + block) / H, 1)],
        "widest_pct": round(100 * widest / W, 1),
    }


def render_text_overlay(path: Path, text: str, size: int, y_margin: int, *, index: int = 1, anchor: str = "top") -> None:
    font = ImageFont.truetype(FONT, size, index=index)
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    tokens = [(w.strip("*"), w.startswith("**")) for w in text.split()]
    lines, cur = [], []
    for tok in tokens:
        trial = " ".join(t for t, _ in cur + [tok])
        if cur and font.getlength(trial) > W - 96:
            lines.append(cur)
            cur = [tok]
        else:
            cur.append(tok)
    lines.append(cur)
    asc, desc = font.getmetrics()
    lh, gap = asc + desc, int(size * 0.12)
    block = lh * len(lines) + gap * (len(lines) - 1)
    cy = H - y_margin - block if anchor == "bottom" else y_margin
    space = font.getlength(" ")
    for line in lines:
        x = (W - font.getlength(" ".join(t for t, _ in line))) / 2
        for t_str, hot in line:
            draw.text(
                (x, cy),
                t_str,
                font=font,
                fill=YEL if hot else CREAM,
                stroke_width=4,
                stroke_fill=INK,
            )
            x += font.getlength(t_str) + space
        cy += lh + gap
    img.save(path)


def render_when_card(path: Path, hot_part: str, rest_part: str) -> dict:
    size = int(BAND_H * 0.115)  # 60 px = 11.4% of 16:9 band height
    font = ImageFont.truetype(FONT, size, index=2)
    full_text = hot_part + rest_part
    while font.getlength(full_text) > W - 96 and size > 42:
        size -= 2
        font = ImageFont.truetype(FONT, size, index=2)
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    y = BAND_TOP + 82  # inside 16:9 center band (569..1095)
    full_w = font.getlength(full_text)
    x = (W - full_w) / 2
    draw.text((x, y), hot_part, font=font, anchor="ls", fill=YEL, stroke_width=4, stroke_fill=INK)
    draw.text((x + font.getlength(hot_part), y), rest_part, font=font, anchor="ls", fill=CREAM, stroke_width=4, stroke_fill=INK)
    img.save(path)
    return {"text": full_text, "size_px": size, "pct_of_band": round(100 * size / BAND_H, 1)}


# ---------------------------------------------------------------------------
# Segment extraction & Loudness leveling
# ---------------------------------------------------------------------------

def cut_plate_segment(src: Path, dst: Path, t_in: float, dur: float, x0: float, x1: float) -> None:
    src_dur = probe(src)
    if t_in < -0.001 or t_in + dur > src_dur + 0.02:
        raise SystemExit(f"{src.name}: [{t_in:.3f}, {t_in + dur:.3f}] exceeds {src_dur:.3f}s")
    t_end = t_in + dur
    if abs(x1 - x0) < 0.01:
        crop_f = f"crop=405:720:{int(round(x0))}:0"
    else:
        crop_f = f"crop=405:720:'{x0:.3f}+({x1:.3f}-{x0:.3f})*(t/{dur:.4f})':0"
    vf = (
        f"trim=start={t_in:.4f}:end={t_end:.4f},setpts=PTS-STARTPTS,"
        f"{crop_f},scale={W}:{H}:flags=lanczos,setsar=1,fps={FPS}"
    )
    ff(
        "-i", str(src),
        "-vf", vf,
        "-t", f"{dur:.3f}",
        "-an", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "veryfast", "-crf", "18",
        str(dst),
    )


def ebur128(path: Path) -> tuple[float, float]:
    err = subprocess.run(
        ["ffmpeg", "-nostats", "-hide_banner", "-i", str(path), "-af", "ebur128=peak=true", "-f", "null", "-"],
        capture_output=True,
        text=True,
    ).stderr
    i_lines = [ln for ln in err.splitlines() if ln.strip().startswith("I:") and "LUFS" in ln]
    p_lines = [ln for ln in err.splitlines() if ln.strip().startswith("Peak:") and "dBFS" in ln]
    if not i_lines or not p_lines:
        raise SystemExit(f"ebur128 failed on {path.name}")
    lufs = float(i_lines[-1].split("I:")[1].split("LUFS")[0].strip())
    peak = float(p_lines[-1].split("Peak:")[1].split("dBFS")[0].strip())
    return lufs, peak


def level_master(mp4: Path) -> dict:
    tmp = mp4.with_suffix(".leveled.mp4")
    target, tp = -12.0, -2.0
    lufs2, peak2 = 0.0, 0.0
    for _ in range(5):
        ff(
            "-i", str(mp4), "-c:v", "copy",
            "-af", f"loudnorm=I={target:.2f}:TP={tp:.2f}:LRA=11",
            "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2", "-movflags", "+faststart",
            str(tmp),
        )
        lufs2, peak2 = ebur128(tmp)
        if -14.4 <= lufs2 <= -13.6 and peak2 <= -1.7:
            break
        target += (-14.0 - lufs2)
        if peak2 > -1.7:
            tp -= 0.3
    if not (-14.5 <= lufs2 <= -13.5) or peak2 > -1.6:
        tmp.unlink(missing_ok=True)
        raise SystemExit(f"level landed at {lufs2:.2f} LUFS / {peak2:.2f} dBTP")
    tmp.replace(mp4)
    return {"lufs": round(lufs2, 2), "true_peak_dbtp": round(peak2, 2), "loudnorm_I": round(target, 2)}


def verify_all_inputs() -> dict[str, Path]:
    paths: dict[str, Path] = {}
    for row_id, (sub, fn, exp_sha, _prod) in LOCKED_PLATES.items():
        p = NAS_PROJ / "04_Generated-Clips" / sub / fn
        if not p.is_file():
            raise SystemExit(f"Missing locked plate on NAS: {p}")
        got = sha256(p)
        if got != exp_sha:
            raise SystemExit(f"SHA256 mismatch on {fn}: {got} != {exp_sha}")
        paths[row_id] = p
    for row_id, (fn, exp_sha) in PARENT_CODE_GRAPHICS.items():
        p = NAS_PROJ / "07_Edit-Project/code_graphics_v01" / fn
        if not p.is_file() or sha256(p) != exp_sha:
            raise SystemExit(f"Parent code graphic mismatch: {fn}")
        paths[f"parent_{row_id}"] = p
    return paths


def assemble_one(
    *,
    short_key: str,
    stem_out: str,
    yt_title: str,
    air_date_check: str,
    hook_markup: str,
    hook_plain: str,
    hook_end_t: float,
    total_dur: float,
    vo_src_mp3: Path,
    vo_src_wav: Path,
    vo_mp3_sha: str,
    vo_wav_sha: str,
    vo_builder,
    beats: list[dict],
    bed_synth_fn,
    bed_prompt: str,
    bed_pace: str,
    sfx_events: list[tuple[str, float, float, float]],
    when_card_spec: tuple[str, str, float, float] | None,
    payoff_word_prefix: str,
    plate_paths: dict[str, Path],
    cg_paths: dict[str, Path],
) -> dict:
    if sha256(vo_src_mp3) != vo_mp3_sha or sha256(vo_src_wav) != vo_wav_sha:
        raise SystemExit(f"{short_key}: accepted VO SHA-256 mismatch")

    work = SCRATCH_ROOT / short_key
    if work.exists():
        shutil.rmtree(work)
    work.mkdir(parents=True, exist_ok=True)
    qa_dir = HERE / f"qa_{short_key}_v01"
    if qa_dir.exists():
        shutil.rmtree(qa_dir)
    qa_dir.mkdir(parents=True, exist_ok=True)

    speech_wav = work / f"{stem_out}_vo_speech.wav"
    vo_wav = work / f"{stem_out}_vo.wav"
    ws = vo_builder(vo_src_wav, vo_wav, speech_wav, total_dur)
    spoken_full = " ".join(w for w, _, _ in ws)
    (work / "spoken.txt").write_text(spoken_full + "\n")

    if ws[0][1] > 0.15:
        raise SystemExit(f"{short_key}: first word starts at {ws[0][1]:.3f}s > 0.15s")

    # Cut & concatenate picture beats
    segs, plan_rows = [], []
    for k, b in enumerate(beats):
        t0, t1 = b["t0"], b["t1"]
        dur = round(t1 - t0, 3)
        seg_out = work / f"seg_{k:02d}.mp4"
        if b["kind"] == "code_graphic":
            cg_src = cg_paths[b["row_id"]]
            ff(
                "-i", str(cg_src),
                "-t", f"{dur:.3f}",
                "-vf", f"fps={FPS},setsar=1",
                "-an", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "veryfast", "-crf", "18",
                str(seg_out),
            )
            src_name = cg_src.name
            upscale = 1.0
            producer = "gemini"
            src_sha = sha256(cg_src)
        else:
            p_src = plate_paths[b["row_id"]]
            cut_plate_segment(p_src, seg_out, b["in_s"], dur, b["x0"], b["x1"])
            src_name = p_src.name
            upscale = UPSCALE_PLATE
            producer = LOCKED_PLATES[b["row_id"]][3]
            src_sha = LOCKED_PLATES[b["row_id"]][2]
        segs.append(seg_out)
        plan_rows.append({
            "id": b["id"],
            "row_id": b["row_id"],
            "t0": t0,
            "t1": t1,
            "hold_s": dur,
            "plate": src_name,
            "source_sha256": src_sha,
            "producer": producer,
            "in_s": b["in_s"],
            "x0": b.get("x0"),
            "x1": b.get("x1"),
            "lands_on": b["lands_on"],
            "upscale": upscale,
        })

    (work / "pic.txt").write_text("".join(f"file '{s.name}'\n" for s in segs))
    pic_mp4 = work / "picture.mp4"
    ff(
        "-f", "concat", "-safe", "0", "-i", "pic.txt",
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "veryfast", "-crf", "18",
        "-r", str(FPS), "-t", f"{total_dur:.3f}",
        str(pic_mp4),
        cwd=work,
    )

    # Music bed (temp in PROJ/05_Music during music_gate, permanent on NAS_PROJ/05_Music; plan JSON kept in git)
    music_dir_git = PROJ / "05_Music"
    music_dir_git.mkdir(parents=True, exist_ok=True)
    bed_wav_tmp = music_dir_git / f"{stem_out}_bed.wav"
    bed_synth_fn(bed_wav_tmp, total_dur)
    bed_sha = sha256(bed_wav_tmp)
    plan_json = {
        "prompt": bed_prompt,
        "film": "010",
        "short": stem_out,
        "job": "J2172",
        "source": "own synthesis in _build_j2172_shorts_v01.py, 0 credits",
        "pace_bpm": bed_pace,
        "bed_file": bed_wav_tmp.name,
        "bed_sha256": bed_sha,
        "nas_path": str(NAS_PROJ / "05_Music" / bed_wav_tmp.name),
    }
    (music_dir_git / f"{stem_out}_bed_plan.json").write_text(json.dumps(plan_json, indent=2) + "\n")

    # SFX stem + stem mix check via sfx_kit.py level
    kit_dir = NAS_PROJ / "06_Sound-Effects/kit_v01"
    sfx_raw = place_sfx(kit_dir, work / "sfx_raw.wav", total_dur, sfx_events)
    audio_mix = work / "audio_mix.wav"
    bed_db, sfx_db, sfx_level = -16.5, -15.0, {}
    stems: dict[str, Path] = {}
    for _ in range(6):
        ff(
            "-i", str(vo_wav), "-i", str(bed_wav_tmp), "-i", str(sfx_raw),
            "-filter_complex",
            f"[0:a]aformat=sample_rates=48000:channel_layouts=stereo,atrim=0:{total_dur:.3f}[v];"
            f"[1:a]aformat=sample_rates=48000:channel_layouts=stereo,atrim=0:{total_dur:.3f},asetpts=PTS-STARTPTS,"
            f"volume={bed_db:.2f}dB,afade=t=in:d=0.05,afade=t=out:st={total_dur - 0.25:.3f}:d=0.25[b];"
            f"[2:a]aformat=sample_rates=48000:channel_layouts=stereo,atrim=0:{total_dur:.3f},volume={sfx_db:.2f}dB[s];"
            "[v][b][s]amix=inputs=3:normalize=0:duration=first,alimiter=limit=0.89[a]",
            "-map", "[a]", "-t", f"{total_dur:.3f}", "-c:a", "pcm_s16le",
            str(audio_mix),
        )
        for sname, ssrc, af_extra in (
            ("vo", vo_wav, f"atrim=0:{total_dur:.3f}"),
            ("bed", bed_wav_tmp, f"volume={bed_db:.2f}dB,atrim=0:{total_dur:.3f},afade=t=in:d=0.05,afade=t=out:st={total_dur - 0.25:.3f}:d=0.25"),
            ("sfx", sfx_raw, f"volume={sfx_db:.2f}dB,atrim=0:{total_dur:.3f}"),
        ):
            stems[sname] = work / f"stem_{sname}.wav"
            ff("-i", str(ssrc), "-af", af_extra, "-t", f"{total_dur:.3f}", "-c:a", "pcm_s16le", str(stems[sname]))
        r = subprocess.run(
            [
                sys.executable, str(OWB / "scripts/sfx_kit.py"), "level",
                "--vo", str(stems["vo"]), "--sfx", str(stems["sfx"]), "--bed", str(stems["bed"]),
                "--minutes", f"{total_dur / 60.0:.4f}",
            ],
            capture_output=True,
            text=True,
        )
        sfx_level = {"exit": r.returncode, "output": (r.stdout + r.stderr).strip(), "bed_db": bed_db, "sfx_db": sfx_db}
        if r.returncode == 0:
            break
        bed_db -= 2.5
        sfx_db -= 2.5
    if sfx_level.get("exit") != 0:
        raise SystemExit(f"{short_key}: sfx_kit.py level failed: {sfx_level.get('output')}")

    # Overlays: frame-0 hook, bottom VO captions (after 2.0s), 9-14s promoted-long title, optional WHEN card
    chunks = chunk_words(ws, total_dur)
    overlays: list[tuple[Path, float, float, str, str]] = []
    hook_png = work / "cap_hook.png"
    if short_key == "short_C":
        hook_meta = render_hook(hook_png, hook_markup, top_frac=0.055, cap_frac=0.081)
    else:
        hook_meta = render_hook(hook_png, hook_markup, top_frac=0.145, cap_frac=0.090)
    overlays.append((hook_png, 0.0, hook_end_t, "hook", hook_plain))

    for idx, c in enumerate(chunks):
        c_png = work / f"cap_{idx:03d}.png"
        render_text_overlay(c_png, c["text"], 48, 195, anchor="bottom")
        overlays.append((c_png, c["t0"], c["t1"], "vo", c["text"]))

    title_png = work / "cap_title.png"
    render_text_overlay(title_png, LONG_TITLE, 48, 160, index=2, anchor="top")
    overlays.append((title_png, TITLE_IN, TITLE_OUT, "title", LONG_TITLE))

    inputs = ["-i", str(pic_mp4), "-i", str(audio_mix)]
    for png, *_ in overlays:
        inputs += ["-loop", "1", "-i", str(png)]

    fc, last_v = [], "[0:v]"
    card_meta = None
    if when_card_spec is not None:
        hot_p, rest_p, c_in, c_out = when_card_spec
        card_png = work / "card_when.png"
        card_meta = render_when_card(card_png, hot_p, rest_p)
        card_meta["in_s"] = c_in
        card_meta["out_s"] = c_out
        ci = 2 + len(overlays)
        inputs += ["-loop", "1", "-t", f"{total_dur:.3f}", "-i", str(card_png)]
        fade_d = 0.35
        fc.append(
            f"[{ci}:v]format=rgba,fade=t=in:st={c_in:.3f}:d={fade_d}:alpha=1,"
            f"fade=t=out:st={c_out - fade_d:.3f}:d={fade_d}:alpha=1[card]"
        )
        fc.append(f"{last_v}[card]overlay=0:0:enable='between(t,{c_in:.3f},{c_out:.3f})'[vc]")
        last_v = "[vc]"

    for idx, (_, t0, t1, *_rest) in enumerate(overlays, start=2):
        fc.append(f"{last_v}[{idx}:v]overlay=0:0:enable='between(t,{t0:.3f},{t1:.3f})'[v{idx}]")
        last_v = f"[v{idx}]"

    mp4_scratch = work / f"{stem_out}.mp4"
    ff(
        *inputs,
        "-filter_complex", ";".join(fc),
        "-map", last_v, "-map", "1:a",
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-profile:v", "high", "-preset", "veryfast",
        "-crf", "18", "-r", str(FPS),
        "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2",
        "-t", f"{total_dur:.3f}", "-movflags", "+faststart",
        str(mp4_scratch),
    )
    level = level_master(mp4_scratch)
    payoff_w = next(w for w in ws if w[0].startswith(payoff_word_prefix))

    # Full stream decode check (0 errors)
    dec = subprocess.run(
        ["ffmpeg", "-v", "error", "-i", str(mp4_scratch), "-f", "null", "-"],
        capture_output=True,
        text=True,
    )
    if dec.returncode != 0 or dec.stderr.strip():
        raise SystemExit(f"{short_key}: decode check failed: {dec.stderr}")

    # Sidecar <stem>_meta.json (placed beside scratch mp4 for gate_shorts_open AND saved in git 10_Shorts/ + NAS)
    nas_short_dir = NAS_PROJ / "10_Shorts/J2172" / short_key
    meta_payload = {
        "film": "HOS:010",
        "job": "J2172",
        "short_id": short_key,
        "stem": stem_out,
        "youtube_title": yt_title,
        "promoted_long_title": LONG_TITLE,
        "conditional_target_air_date": air_date_check,
        "long_must_be_public_first": True,
        "resolution": f"{W}x{H}",
        "fps": FPS,
        "duration_s": round(probe(mp4_scratch), 3),
        "hook_caption": {"text": hook_plain, "start_s": 0.0, "end_s": hook_end_t},
        "vo_onset_s": ws[0][1],
        "hook_sentence_end_s": beats[0]["t1"],
        "first_cut_s": beats[0]["t1"],
        "second_cut_s": beats[1]["t1"],
        "last_word_end_s": ws[-1][2],
        "loop_tail_s": round(total_dur - beats[-2]["t1"], 3),
        "payoff_word": payoff_w[0],
        "payoff_start_s": payoff_w[1],
        "payoff_frac": round(payoff_w[1] / total_dur, 4),
        "meta_promise": False,
        "end_card": None,
        "full_film_banner": False,
        "spoken": spoken_full,
        "captions": [{"word": w, "start": s, "end": e} for w, s, e in ws],
        "audio": {
            "vo_source_mp3_sha256": vo_mp3_sha,
            "vo_source_wav_sha256": vo_wav_sha,
            "level": level,
            "sfx_level": sfx_level,
            "stems": {
                "vo": str(nas_short_dir / "stems/stem_vo.wav"),
                "bed": str(nas_short_dir / "stems/stem_bed.wav"),
                "sfx": str(nas_short_dir / "stems/stem_sfx.wav"),
            },
        },
        "cuts": plan_rows,
        "when_card": card_meta,
    }
    meta_scratch = work / f"{stem_out}_meta.json"
    meta_scratch.write_text(json.dumps(meta_payload, indent=2) + "\n")

    # Run all gates
    cuts_list, pool_list, seen = [], [], set()
    for idx, row in enumerate(plan_rows, start=1):
        src_id = f"loop_{row['plate']}" if row["lands_on"] == "loop" else row["plate"]
        cuts_list.append({
            "row": f"s{idx:02d}",
            "timeline_in": row["t0"],
            "timeline_out": row["t1"],
            "source": src_id,
            "upscale": row["upscale"],
            "video": True,
            "framing": {"offset": row["in_s"]},
        })
        if src_id not in seen:
            seen.add(src_id)
            pool_list.append({"file_id": src_id, "title": f"Flow/code plate {row['plate']}"})

    cuts_f, pool_f = qa_dir / "cuts.json", qa_dir / "pool.json"
    cuts_f.write_text(json.dumps(cuts_list, indent=2) + "\n")
    pool_f.write_text(json.dumps(pool_list, indent=2) + "\n")

    gate_results: dict[str, dict] = {}
    sheet_dir = qa_dir / "sheets"
    sheet_dir.mkdir(parents=True, exist_ok=True)
    for gname, cmd in (
        ("polish", [
            sys.executable, str(OWB / "scripts/polish_gate.py"), str(mp4_scratch),
            "--cuts", str(cuts_f), "--out", str(qa_dir / "polish_gate.json"),
        ]),
        ("picture", [
            sys.executable, str(OWB / "scripts/picture_qa.py"), str(mp4_scratch),
            "--cuts", str(cuts_f), "--pool", str(pool_f), "--out-dir", str(qa_dir / "picture_qa"),
        ]),
        ("music", [
            sys.executable, str(OWB / "scripts/music_gate.py"), str(PROJ),
            "--bed", str(bed_wav_tmp), "--video", str(mp4_scratch), "--out", str(qa_dir / "music_gate.json"),
        ]),
        ("open", [
            sys.executable, str(REPO / "00_Brand/Channel-Setup/tools/gate_shorts_open.py"), "check", str(mp4_scratch),
            "--air-date", air_date_check, "--meta", str(meta_scratch),
            "--script", str(work / "spoken.txt"), "--vo", str(vo_wav),
            "--sheet-dir", str(sheet_dir),
        ]),
    ):
        r = subprocess.run(cmd, capture_output=True, text=True)
        txt = (r.stdout + r.stderr).strip()
        (qa_dir / f"{gname}.txt").write_text(txt + "\n")
        gate_results[gname] = {"exit": r.returncode, "output": txt}
        if r.returncode != 0:
            raise SystemExit(f"{short_key} gate {gname} FAILED (exit {r.returncode}):\n{txt}")

    # Also run vo_check_py312.sh on speech_wav against exact spoken script!
    vo_script_md = work / "short_script_check.md"
    vo_script_md.write_text(spoken_full + "\n")
    r_vo = subprocess.run(
        [str(REPO / "00_Brand/Channel-Setup/tools/vo_check_py312.sh"), str(speech_wav), "--script", str(vo_script_md)],
        capture_output=True,
        text=True,
    )
    vo_txt = (r_vo.stdout + r_vo.stderr).strip()
    (qa_dir / "vo_check.txt").write_text(vo_txt + "\n")
    gate_results["vo_check"] = {"exit": r_vo.returncode, "output": vo_txt}

    (qa_dir / "sfx.txt").write_text(sfx_level["output"] + "\n")
    gate_results["sfx"] = {"exit": sfx_level["exit"], "output": sfx_level["output"]}

    # Stage durable copies to NAS_PROJ and verify SHA-256 on both sides; remove temporary .wav from git worktree!
    nas_music_dir = NAS_PROJ / "05_Music"
    nas_music_dir.mkdir(parents=True, exist_ok=True)
    nas_bed_wav = nas_music_dir / bed_wav_tmp.name
    shutil.copy2(bed_wav_tmp, nas_bed_wav)
    shutil.copy2(music_dir_git / f"{stem_out}_bed_plan.json", nas_music_dir / f"{stem_out}_bed_plan.json")
    if sha256(nas_bed_wav) != bed_sha:
        raise SystemExit(f"{short_key}: NAS bed SHA-256 mismatch")
    bed_wav_tmp.unlink()  # keep git checkout 100% free of audio/video files!

    (nas_short_dir / "stems").mkdir(parents=True, exist_ok=True)
    nas_mp4 = nas_short_dir / f"{stem_out}.mp4"
    mp4_sha = sha256(mp4_scratch)
    shutil.copy2(mp4_scratch, nas_mp4)
    if sha256(nas_mp4) != mp4_sha:
        raise SystemExit(f"{short_key}: NAS master MP4 SHA-256 mismatch")

    stem_hashes = {}
    for sname, spath in stems.items():
        dst_s = nas_short_dir / "stems" / spath.name
        s_sha = sha256(spath)
        shutil.copy2(spath, dst_s)
        if sha256(dst_s) != s_sha:
            raise SystemExit(f"{short_key}: NAS stem {sname} SHA-256 mismatch")
        stem_hashes[sname] = {"nas_path": str(dst_s), "sha256": s_sha, "bytes": dst_s.stat().st_size}

    meta_payload["nas_master_mp4"] = str(nas_mp4)
    meta_payload["master_sha256"] = mp4_sha
    meta_payload["master_bytes"] = nas_mp4.stat().st_size
    meta_payload["audio"]["stem_hashes"] = stem_hashes
    meta_payload["hook_metrics"] = hook_meta

    meta_git = HERE / f"{stem_out}_meta.json"
    meta_git.write_text(json.dumps(meta_payload, indent=2) + "\n")
    shutil.copy2(meta_git, nas_short_dir / f"{stem_out}_meta.json")

    # Build a 9-tile timeline contact sheet in qa_dir so cloud reviewers can inspect every row
    tiles = []
    for k, row in enumerate(plan_rows):
        t_mid = round((row["t0"] + row["t1"]) / 2.0, 3)
        if k == 0:
            t_mid = 0.50  # show frame-0 hook caption + opening plate
        tp = work / f"tile_{k:02d}.png"
        ff("-ss", f"{t_mid:.3f}", "-i", str(mp4_scratch), "-frames:v", "1", "-vf", "scale=234:416", str(tp))
        tiles.append(tp)
    row_sheet = qa_dir / f"{stem_out}_rows_sheet.jpg"
    ff(
        *[x for tp in tiles for x in ("-i", str(tp))],
        "-filter_complex", f"hstack=inputs={len(tiles)}",
        str(row_sheet),
    )

    build_summary = {
        "short_id": short_key,
        "stem": stem_out,
        "youtube_title": yt_title,
        "nas_master_mp4": str(nas_mp4),
        "scratch_mp4": str(mp4_scratch),
        "master_sha256": mp4_sha,
        "master_bytes": nas_mp4.stat().st_size,
        "duration_s": meta_payload["duration_s"],
        "resolution": f"{W}x{H}",
        "fps": FPS,
        "words_count": len(ws),
        "vo_onset_s": ws[0][1],
        "hook_sentence_end_s": beats[0]["t1"],
        "first_cut_s": beats[0]["t1"],
        "second_cut_s": beats[1]["t1"],
        "max_body_hold_s": max(r["hold_s"] for r in plan_rows if r["lands_on"] != "loop"),
        "last_word_end_s": ws[-1][2],
        "tail_gap_s": round(total_dur - ws[-1][2], 3),
        "loop_tail_s": meta_payload["loop_tail_s"],
        "payoff_word": payoff_w[0],
        "payoff_start_s": payoff_w[1],
        "payoff_frac": meta_payload["payoff_frac"],
        "level": level,
        "bed_nas_path": str(nas_bed_wav),
        "bed_sha256": bed_sha,
        "stem_hashes": stem_hashes,
        "gates": {k: {"exit": v["exit"]} for k, v in gate_results.items()},
    }
    (qa_dir / "BUILD.json").write_text(json.dumps(build_summary, indent=2) + "\n")
    return build_summary


def main() -> None:
    plate_paths = verify_all_inputs()
    SCRATCH_ROOT.mkdir(parents=True, exist_ok=True)

    # 1. Render £0 full-bleed 936x1664 portrait code graphics and stage to NAS code_graphics_v01
    cg_scratch = SCRATCH_ROOT / "code_graphics_9x16"
    cg_a_mp4 = cg_scratch / "code_graphic_010_short_A_s06_iridium_spike_9x16.mp4"
    cg_a_jpg = HERE / "qa_short_A_v01_cg_s06.jpg"
    cg_a_info = render_iridium_spike_9x16(cg_a_mp4, cg_a_jpg, dur=2.900)

    cg_c_mp4 = cg_scratch / "code_graphic_010_short_C_s03_why_survive_9x16.mp4"
    cg_c_jpg = HERE / "qa_short_C_v01_cg_s03.jpg"
    cg_c_info = render_why_survive_9x16(cg_c_mp4, cg_c_jpg, dur=2.720)

    nas_cg_dir = NAS_PROJ / "07_Edit-Project/code_graphics_v01"
    for src_cg, info in ((cg_a_mp4, cg_a_info), (cg_c_mp4, cg_c_info)):
        dst_cg = nas_cg_dir / src_cg.name
        shutil.copy2(src_cg, dst_cg)
        if sha256(dst_cg) != info["sha256"]:
            raise SystemExit(f"NAS code graphic SHA-256 mismatch: {dst_cg}")

    cg_paths = {
        "P4:01_iridium_spike": cg_a_mp4,
        "P5:11_why_survive": cg_c_mp4,
    }

    # 2. Assemble Short A (23.289 s, Option A1)
    beats_a = [
        {"id": "S01", "row_id": "P1:01_clay_line", "kind": "plate", "t0": 0.000, "t1": 2.849, "in_s": 1.000, "x0": 437.0, "x1": 437.0, "lands_on": "plate"},
        {"id": "S02", "row_id": "P2:01_walter_hammer", "kind": "plate", "t0": 2.849, "t1": 6.189, "in_s": 0.000, "x0": 620.0, "x1": 620.0, "lands_on": "plate"},
        {"id": "S03", "row_id": "P2:03_tiny_shells", "kind": "plate", "t0": 6.189, "t1": 9.549, "in_s": 0.000, "x0": 437.0, "x1": 437.0, "lands_on": "plate"},
        {"id": "S04", "row_id": "P2:05_almost_none", "kind": "plate", "t0": 9.549, "t1": 13.269, "in_s": 0.000, "x0": 380.0, "x1": 460.0, "lands_on": "plate"},
        {"id": "S05", "row_id": "P3:08_asaro_michel", "kind": "plate", "t0": 13.269, "t1": 16.389, "in_s": 0.000, "x0": 180.0, "x1": 180.0, "lands_on": "plate"},
        {"id": "S06", "row_id": "P4:01_iridium_spike", "kind": "code_graphic", "t0": 16.389, "t1": 19.289, "in_s": 0.000, "lands_on": "code_graphic"},
        {"id": "S07", "row_id": "P4:06_dust_veil", "kind": "plate", "t0": 19.289, "t1": 22.289, "in_s": 2.000, "x0": 540.0, "x1": 540.0, "lands_on": "plate"},
        {"id": "loop_tail", "row_id": "P1:01_clay_line", "kind": "plate", "t0": 22.289, "t1": 23.289, "in_s": 0.000, "x0": 437.0, "x1": 437.0, "lands_on": "loop"},
    ]
    res_a = assemble_one(
        short_key="short_A",
        stem_out="hos_010_short_A_v01",
        yt_title="What Killed the Dinosaurs?",
        air_date_check="2026-12-04",
        hook_markup="THE **LINE**",
        hook_plain="THE LINE",
        hook_end_t=2.000,
        total_dur=23.289,
        vo_src_mp3=NAS_PROJ / "10_Shorts/vo_v02/hos_010_short_A_v02.mp3",
        vo_src_wav=NAS_PROJ / "10_Shorts/vo_v02/hos_010_short_A_v02.wav",
        vo_mp3_sha="68d88b5b5883f2376bcec29c26d77efea7634d5c7705693f41202ca587b927fb",
        vo_wav_sha="2488aa8b49beb3a642597e08f30ca53e723fbee00cd21ad8bdc581a9293ff228",
        vo_builder=build_short_a_vo,
        beats=beats_a,
        bed_synth_fn=synth_bed_short_a,
        bed_prompt=(
            "Quiet A-minor chamber harp and warm cello fifths under the Gubbio clay mystery, measured and curious, "
            "leaving clear space for spoken British narration. Pace: 68-78 BPM. NOT the 008 Franklin D-minor plucked bed, "
            "NOT the 007 vaccine score, NOT the 006 Trees bed, NOT any Orbit With Ben synth pad, NOT percussion or trailer stings."
        ),
        bed_pace="68-78",
        sfx_events=[
            ("whoosh", 0.00, -14.0, 0.75),
            ("tick", 16.42, -9.0, 0.06),
            ("rumble", 19.30, -17.0, 2.60),
        ],
        when_card_spec=None,
        payoff_word_prefix="packed",
        plate_paths=plate_paths,
        cg_paths=cg_paths,
    )
    shutil.move(str(cg_a_jpg), str(HERE / "qa_short_A_v01/cg_s06_iridium_spike_9x16.jpg"))

    # 3. Assemble Short C (23.560 s, 1.00x VO)
    # R6c tracked x: 515 -> 535 over t_src = 3.25..6.13 (2.88s). At t_src=4.25, x = 515 + 20*(1.00/2.88) = 521.944.
    beats_c = [
        {"id": "S01", "row_id": "P5:09_robin", "kind": "plate", "t0": 0.000, "t1": 1.880, "in_s": 4.250, "x0": 521.944, "x1": 535.0, "lands_on": "plate"},
        {"id": "S02", "row_id": "P4:06_dust_veil", "kind": "plate", "t0": 1.880, "t1": 5.200, "in_s": 1.750, "x0": 540.0, "x1": 540.0, "lands_on": "plate"},
        {"id": "S03", "row_id": "P5:11_why_survive", "kind": "code_graphic", "t0": 5.200, "t1": 7.920, "in_s": 0.000, "lands_on": "code_graphic"},
        {"id": "S04", "row_id": "P5:08_all_at_once", "kind": "plate", "t0": 7.920, "t1": 10.420, "in_s": 1.250, "x0": 380.0, "x1": 380.0, "lands_on": "plate"},
        {"id": "S05", "row_id": "P5:09a_pigeon_pavement", "kind": "plate", "t0": 10.420, "t1": 13.060, "in_s": 1.100, "x0": 360.0, "x1": 530.0, "lands_on": "plate"},
        {"id": "S06", "row_id": "P5:13a_gull_seaside", "kind": "plate", "t0": 13.060, "t1": 15.780, "in_s": 4.300, "x0": 605.0, "x1": 520.0, "lands_on": "plate"},
        {"id": "S07", "row_id": "P5:10_explorer_robin", "kind": "plate", "t0": 15.780, "t1": 19.380, "in_s": 2.050, "x0": 375.0, "x1": 410.0, "lands_on": "plate"},
        {"id": "S08", "row_id": "P5:12_clay_callback", "kind": "plate", "t0": 19.380, "t1": 22.560, "in_s": 1.050, "x0": 437.0, "x1": 437.0, "lands_on": "plate"},
        {"id": "loop_tail", "row_id": "P5:09_robin", "kind": "plate", "t0": 22.560, "t1": 23.560, "in_s": 3.250, "x0": 515.0, "x1": 521.944, "lands_on": "loop"},
    ]
    res_c = assemble_one(
        short_key="short_C",
        stem_out="hos_010_short_C_v01",
        yt_title="Are Birds Really Dinosaurs?",
        air_date_check="2026-12-07",
        hook_markup="STILL **HERE**",
        hook_plain="STILL HERE",
        hook_end_t=1.880,
        total_dur=23.560,
        vo_src_mp3=NAS_PROJ / "10_Shorts/vo_v02/hos_010_short_C_v02.mp3",
        vo_src_wav=NAS_PROJ / "10_Shorts/vo_v02/hos_010_short_C_v02.wav",
        vo_mp3_sha="20432ecd645b28e9fdc051578a284cb2845bd09f3040170b192089b256055b87",
        vo_wav_sha="ca814ab01ad72fde015b4e157638b5e346d592e5df54cefe97e38969340fcb0c",
        vo_builder=build_short_c_vo,
        beats=beats_c,
        bed_synth_fn=synth_bed_short_c,
        bed_prompt=(
            "Gentle G-major morning celesta and warm pastoral woodwind fifths for living garden birds, light and clear "
            "under British narration. Pace: 70-82 BPM. NOT the Short A A-minor harp bed, NOT the 008 Franklin bed, "
            "NOT the 007 vaccine score, NOT the 006 Trees bed, NOT any Orbit With Ben synth pad, NOT drums or trailer stings."
        ),
        bed_pace="70-82",
        sfx_events=[
            ("whoosh", 0.00, -14.0, 0.75),
            ("rumble", 1.90, -17.5, 2.50),
            ("tick", 2.20, -9.5, 0.06),
            ("tick", 5.22, -9.5, 0.06),
        ],
        when_card_spec=("66 MILLION", " YEARS AGO", 2.20, 5.15),
        payoff_word_prefix="Every",
        plate_paths=plate_paths,
        cg_paths=cg_paths,
    )
    shutil.move(str(cg_c_jpg), str(HERE / "qa_short_C_v01/cg_s03_why_survive_9x16.jpg"))

    manifest_dir = HERE / "J2172"
    manifest_dir.mkdir(parents=True, exist_ok=True)
    delivery = {
        "job": "J2172",
        "film": "HOS:010",
        "assembler": "gemini",
        "gbp_spent": 0,
        "credits_spent": 0,
        "parent_long_status": "not_uploaded_yet_must_be_public_before_shorts",
        "conditional_planning_targets": {
            "long_planned": "2026-12-03T18:00:00Z",
            "short_A_conditional": "2026-12-04T11:30:00Z",
            "short_C_conditional": "2026-12-06T11:30:00Z (or Tue 2026-12-08T11:30:00Z; Mon 7 Dec is not a locked HOS Sat/Fri/Sun/Tue Short weekday)",
            "ben_watch_ready_target": "2026-12-01T18:00:00Z",
        },
        "code_graphics_9x16": {
            "short_A_s06": {
                "nas_path": str(nas_cg_dir / cg_a_mp4.name),
                "sha256": cg_a_info["sha256"],
                "duration_s": cg_a_info["duration_s"],
                "derived_from_parent": PARENT_CODE_GRAPHICS["P4:01_iridium_spike"],
            },
            "short_C_s03": {
                "nas_path": str(nas_cg_dir / cg_c_mp4.name),
                "sha256": cg_c_info["sha256"],
                "duration_s": cg_c_info["duration_s"],
                "derived_from_parent": PARENT_CODE_GRAPHICS["P5:11_why_survive"],
            },
        },
        "shorts": {"Short_A": res_a, "Short_C": res_c},
    }
    (manifest_dir / "DELIVERY_MANIFEST.json").write_text(json.dumps(delivery, indent=2) + "\n")
    shutil.copy2(manifest_dir / "DELIVERY_MANIFEST.json", NAS_PROJ / "10_Shorts/J2172/DELIVERY_MANIFEST.json")
    print(json.dumps(delivery, indent=2))


if __name__ == "__main__":
    main()
