#!/usr/bin/env python3
"""J2171: Assemble HOS 009 locked Shorts A and B at 936x1664 (2.311x, £0, 0 credits).

- Short A ("What Would Happen If the Moon Stopped Moving?") -> hos_009_short_A_v01.mp4 (25.320 s)
  Uses accepted VO hos_009_short_A_v02 (J0862/J2281 PASS, PR #423) at 1.00x (24.320 s + 1.000 s loop tail).
  Hook ends at 2.800 s <= 2.85 s. Frame 0: P1:01_moon_falling (moving 3D Moon + glowing arc + Newton).
- Short B ("How Did Newton Discover Gravity?") -> hos_009_short_B_v01.mp4 (25.480 s)
  Uses accepted VO hos_009_short_B_v04 (J0862/J2195/J2279/J2281 PASS, PR #423) at 1.00x (24.480 s + 1.000 s loop tail).
  Preserves both "In one minute" and "in one second" comparison intervals and all J1004/J1894 restrictions.
  Hook ends at 2.820 s <= 2.85 s. Frame 0: P4:05_minute_second right-half full-bleed Moon + glowing arc above Earth.
- Uses locked J1237 Tranche 1 + J2033/J2034 Tranche 2 KEEP moving Flow plates (13 distinct plates, 100% SHA-256 verified),
  plus £0 full-bleed 936x1664 portrait house period-paper / moving-plate code graphics derived from locked
  P3:08_km_a_second, P3:06_orbit_teach, P4:03_sixty_earths, and P4:04_dots_square (over moving P4:02_spray_paint_c2),
  leaving all 16:9 Long assets untouched.
- Reuses the J3241 Chief-accepted HOS 009 score (hos_009_score_v04_synth.wav, Part 1 awe for Short A, Part 4 explain
  for Short B) and mixes with the £0 HOS house SFX kit (06_Sound-Effects/kit_v01).
- Runs polish_gate.py, picture_qa.py, music_gate.py, sfx_kit.py level, vo_check_py312.sh, gate_shorts_open.py check,
  and full ffmpeg decode check, then stages durable SHA-256-verified copies to NAS studio-live and HOS UAT.
"""
from __future__ import annotations

import hashlib
import json
import math
import os
import shutil
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
PROJ = HERE.parent
REPO = PROJ.parents[1]
OWB = Path("/Users/benjaminoats/YouTube/orbit-with-ben")
NAS_PROJ = Path("/Volumes/data/studio-live/History Of Science/02_Video-Projects/009_The-Falling-Moon-Gravity")
NAS_ARCH = Path("/Volumes/data/mac-mini-archive/YouTube/History Of Science/02_Video-Projects/009_The-Falling-Moon-Gravity")
LOCAL_MEDIA = Path("/Users/benjaminoats/YouTube/hos-009-gravity/02_Video-Projects/009_The-Falling-Moon-Gravity")
HOS_UAT = Path.home() / "Library/Mobile Documents/com~apple~CloudDocs/HOS UAT/009_The-Falling-Moon-Gravity/10_Shorts"
SCRATCH_ROOT = Path(os.environ.get("STUDIO_SCRATCH", "/Volumes/MiniWork/scratch")) / "J2171-build"

W, H, FPS = 936, 1664, 30
BAND_H = W * 9 // 16          # 526 px
BAND_TOP = (H - BAND_H) // 2  # 569 px
UPSCALE_PLATE = round(H / 720.0, 4)  # 2.3111 <= 2.35

FONT = "/System/Library/Fonts/Supplemental/Didot.ttc"
CREAM = (245, 232, 210, 255)
WHITE = (252, 248, 240, 255)
INK = (24, 20, 18, 255)
YEL = (255, 224, 0, 255)  # #FFE000 per Rule 24

INK_CG = (34, 16, 6)
WASH_CG = (216, 178, 124)
MOON_WASH_CG = (232, 212, 176)

LONG_TITLE = "Why Doesn't the Moon Fall to Earth?"
TITLE_IN, TITLE_OUT = 9.0, 14.0

SCORE_WAV = NAS_PROJ / "05_Music/hos_009_score_v04_synth.wav"
SCORE_SHA = "151ba46acdf7d4395b34e105530bd077c26f6eb92832f9a1f00e1551ca88f58d"

LOCKED_PLATES = {
    "P1:01_moon_falling": (
        LOCAL_MEDIA / "04_Generated-Clips/part01/raw/v01/01_moon_falling_t1.mp4",
        NAS_ARCH / "04_Generated-Clips/part01/raw/v01/01_moon_falling_t1.mp4",
        "3e0774a7dd510b5ee32358c188f5efe4903aaf45aafab8870df662bcc1cd4c1f",
        "J1192/J1237",
    ),
    "P1:02_apple_and_moon": (
        LOCAL_MEDIA / "04_Generated-Clips/part01/raw/v01/02_apple_and_moon_t1.mp4",
        NAS_ARCH / "04_Generated-Clips/part01/raw/v01/02_apple_and_moon_t1.mp4",
        "bc3ad225b09a2fc090c4cbe694eb3aeeb0cf5999cd6c6d6262be81a1adcc90e6",
        "J1192/J1237",
    ),
    "P2:07_orchard_bench": (
        LOCAL_MEDIA / "04_Generated-Clips/part02/raw/v01/07_orchard_bench_t1.mp4",
        NAS_ARCH / "04_Generated-Clips/part02/raw/v01/07_orchard_bench_t1.mp4",
        "028ee06be5e3fb76cbc58265837633993c4834c961735c191c36379c5e7afa02",
        "J1192/J1237",
    ),
    "P2:08_the_apple": (
        LOCAL_MEDIA / "04_Generated-Clips/part02/raw/v01/08_the_apple_t1.mp4",
        NAS_ARCH / "04_Generated-Clips/part02/raw/v01/08_the_apple_t1.mp4",
        "357e8de3e9c771ef212fb01ee0a6052ebfedbc0de0ad9794270f5ff2128a5b44",
        "J1192/J1237",
    ),
    "P3:05_shot_orbit": (
        LOCAL_MEDIA / "04_Generated-Clips/part03/raw/v01/05_shot_orbit_t1.mp4",
        NAS_ARCH / "04_Generated-Clips/part03/raw/v01/05_shot_orbit_t1.mp4",
        "0878c30646fa8b7158044a5e3d52a584a1cf4fda8accc76f6aa747fca8405f1b",
        "J1192/J1237",
    ),
    "P3:07_ball_to_moon": (
        LOCAL_MEDIA / "04_Generated-Clips/part03/raw/v05_tranche2/07_ball_to_moon_t1.mp4",
        NAS_PROJ / "04_Generated-Clips/v05_tranche2_archive/07_ball_to_moon_t1.mp4",
        "fba484bb8b370559",  # full hash verified dynamically against both local and NAS
        "J2033/J2034",
    ),
    "P4:02_spray_paint": (
        LOCAL_MEDIA / "04_Generated-Clips/part04/raw/v01/02_spray_paint_t1.mp4",
        NAS_ARCH / "04_Generated-Clips/part04/raw/v01/02_spray_paint_t1.mp4",
        "8a7b7d907240f959e7db25d3c9108439c5df79ae1b8261cde7079ac23342b092",
        "J1192/J1237",
    ),
    "P4:02_spray_paint_c2": (
        LOCAL_MEDIA / "04_Generated-Clips/part04/raw/v01/02_spray_paint_c2_t1.mp4",
        NAS_ARCH / "04_Generated-Clips/part04/raw/v01/02_spray_paint_c2_t1.mp4",
        "0a6279c069fae36a0df291a33d25cce35d0a3aefd4965ebf21ef3e4281bb0f85",
        "J1192/J1237",
    ),
    "P4:05_minute_second": (
        LOCAL_MEDIA / "04_Generated-Clips/part04/raw/v01/05_minute_second_t1.mp4",
        NAS_ARCH / "04_Generated-Clips/part04/raw/v01/05_minute_second_t1.mp4",
        "7f56f05930cefc854aabde17cd204510771dfbaaa5faa2f6b410facebbd3cd66",
        "J1192/J1237",
    ),
    "P4:06_pretty_nearly": (
        LOCAL_MEDIA / "04_Generated-Clips/part04/raw/v01/06_pretty_nearly_t1.mp4",
        NAS_ARCH / "04_Generated-Clips/part04/raw/v01/06_pretty_nearly_t1.mp4",
        "af487165258059d44e1f3ad9682d80d50c2239882f5495c82d7907a3e98d47ad",
        "J1192/J1237",
    ),
    "P4:06_pretty_nearly_c1": (
        LOCAL_MEDIA / "04_Generated-Clips/part04/raw/v01/06_pretty_nearly_c1_t1.mp4",
        NAS_ARCH / "04_Generated-Clips/part04/raw/v01/06_pretty_nearly_c1_t1.mp4",
        "eb3f5d5030b9b18a545ce0922377771c10f499f14f08d1b64239adca975078cf",
        "J1192/J1237",
    ),
    "P5:01_one_law": (
        LOCAL_MEDIA / "04_Generated-Clips/part05/raw/v01/01_one_law_t1.mp4",
        NAS_ARCH / "04_Generated-Clips/part05/raw/v01/01_one_law_t1.mp4",
        "ed89eb1e5c519f18984284d144ae924616f6d08560179fc6b2e4c3942e6053a0",
        "J1192/J1237",
    ),
    "P5:09_orchard_dusk": (
        LOCAL_MEDIA / "04_Generated-Clips/part05/raw/v01/09_orchard_dusk_t1.mp4",
        NAS_ARCH / "04_Generated-Clips/part05/raw/v01/09_orchard_dusk_t1.mp4",
        "1266d61a73ccb6854051836495df72e9f0d0cbd71dd83698d981d887b9a5a41f",
        "J1192/J1237",
    ),
}

PARENT_CODE_GRAPHICS = {
    "P3:08_km_a_second": ("code_graphic_009_p3_08_km_a_second.mp4", "b18c90bc720791f3b4e084db41ca2df4e573d791db74191032366ae9d42a6f58"),
    "P3:06_orbit_teach": ("code_graphic_009_p3_06_orbit_teach.mp4", "840706a32f1717c789317f13c0a4481e334c34f8a39c9393f78a660ea9d9a178"),
    "P4:03_sixty_earths": ("code_graphic_009_p4_03_sixty_earths.mp4", "4de87bc274d984971dabea10403c42ccb45ef654279414d36c19f3c3fce1ac10"),
    "P4:04_dots_square": ("code_graphic_009_p4_04_dots_square.mp4", "7c393d99592073b975adb3faf4196f1253c5c193fd9316b839bc367e32cad072"),
}

UK_SPELLING = {
    "kilometer": "kilometre",
    "kilometer,": "kilometre,",
    "meters.": "metres.",
    "meters": "metres",
    "center": "centre",
    "moon": "Moon",
    "moons": "Moons.",
    "moons.": "Moons.",
    "forever": "for ever.",
    "forever.": "for ever.",
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
# £0 Full-bleed 936x1664 portrait house period-paper & moving-plate code graphics
# ---------------------------------------------------------------------------

def make_parchment_bg(seed: int) -> Image.Image:
    """Warm textured period paper with organic multi-scale fibers (full-bleed 936x1664)."""
    rng = np.random.default_rng(seed)
    y, x = np.mgrid[:H, :W].astype(np.float32)
    nx = (x - W / 2.0) / (W / 2.0)
    ny = (y - H / 2.0) / (H / 2.0)
    vig = np.clip(0.55 * nx * nx + 0.50 * ny * ny, 0.0, 1.2)
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

    base = np.array([224.0, 200.0, 162.0], np.float32)
    dark = np.array([60.0, 48.0, 36.0], np.float32)
    out = np.zeros((H, W, 3), np.float32)
    tex = 0.35 * coarse_img + 0.35 * med_img + fine
    for c in range(3):
        out[:, :, c] = base[c] - dark[c] * vig * 0.55 + tex * (1.0, 0.90, 0.78)[c]
    return Image.fromarray(np.uint8(np.clip(out, 0, 255)), "RGB")


def _draw_notebook_compass_lines(d: ImageDraw.ImageDraw, t: float, seed_off: float = 0.0) -> None:
    """Organic period astronomy notebook compass arcs top & bottom (adds crisp fine detail, no straight bars)."""
    sepia = (72, 52, 36)
    for k, cy in enumerate((130, 250, 370, 1300, 1430, 1550)):
        pts = [
            (xx, cy + 20.0 * math.sin(xx * 0.009 + k * 0.9 + seed_off) + 7.0 * math.cos(xx * 0.021 + t * 0.4))
            for xx in range(36, W - 32, 24)
        ]
        d.line(pts, fill=col(sepia, 0.36), width=3)
    # Subtle engraved brass compass arcs in corners
    d.arc((-140, -140, 340, 340), start=5, end=85, fill=col(sepia, 0.42), width=3)
    d.arc((W - 340, -140, W + 140, 340), start=95, end=175, fill=col(sepia, 0.42), width=3)
    d.arc((-140, H - 340, 340, H + 140), start=275, end=355, fill=col(sepia, 0.42), width=3)
    d.arc((W - 340, H - 340, W + 140, H + 140), start=185, end=265, fill=col(sepia, 0.42), width=3)


def _draw_earth(d: ImageDraw.ImageDraw, cx: float, cy: float, r: float, a: float = 1.0) -> None:
    if a <= 0.01:
        return
    w = max(3, int(r / 14))
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=col(WASH_CG, 0.92 * a), outline=col(INK_CG, a), width=w)
    if r >= 18:
        d.ellipse((cx - r * 0.84, cy - r * 0.84, cx + r * 0.84, cy + r * 0.84), outline=col(INK_CG, 0.45 * a), width=max(2, w - 2))
        d.arc((cx - r * 0.35, cy - r * 0.72, cx + r * 0.55, cy + r * 0.15), 210, 30, fill=col(INK_CG, a), width=max(2, w - 1))
        d.arc((cx - r * 0.62, cy - r * 0.05, cx + r * 0.15, cy + r * 0.72), 20, 200, fill=col(INK_CG, a), width=max(2, w - 1))


def _draw_moon(d: ImageDraw.ImageDraw, cx: float, cy: float, r: float, a: float = 1.0) -> None:
    if a <= 0.01:
        return
    w = max(3, int(r / 10))
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=col(MOON_WASH_CG, 0.95 * a), outline=col(INK_CG, a), width=w)
    d.ellipse((cx - r * 0.25, cy - r * 0.15, cx + r * 0.05, cy + r * 0.20), outline=col(INK_CG, a), width=max(2, w - 1))
    d.ellipse((cx + r * 0.10, cy + r * 0.15, cx + r * 0.38, cy + r * 0.42), outline=col(INK_CG, a), width=max(2, w - 1))


def _draw_arrow(d: ImageDraw.ImageDraw, x0: float, y0: float, x1: float, y1: float, p: float, a: float = 1.0, width: int = 7, head: int = 20) -> None:
    if p <= 0.02 or a <= 0.01:
        return
    p = min(1.0, p)
    x = x0 + (x1 - x0) * p
    y = y0 + (y1 - y0) * p
    fill = col(INK_CG, a)
    d.line((x0, y0, x, y), fill=fill, width=width)
    if p > 0.65:
        ang = math.atan2(y1 - y0, x1 - x0)
        hp = ease((p - 0.65) / 0.35)
        for s in (2.55, -2.55):
            d.line(
                (x, y, x - head * hp * math.cos(ang - s), y - head * hp * math.sin(ang - s)),
                fill=fill,
                width=width,
            )


def _open_encoder(out_mp4: Path) -> subprocess.Popen:
    out_mp4.parent.mkdir(parents=True, exist_ok=True)
    return subprocess.Popen(
        [
            "ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pixel_format", "rgb24",
            "-video_size", f"{W}x{H}", "-framerate", str(FPS), "-i", "-", "-an",
            "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p",
            "-movflags", "+faststart", str(out_mp4),
        ],
        stdin=subprocess.PIPE,
    )


def render_km_a_second_9x16(out_mp4: Path, out_jpg: Path, dur: float = 2.940) -> dict:
    """Short A S02 (2.940 s): Earth + curved Moon arc + sideways & downward arrows + SIDEWAYS AND DOWN."""
    bg = make_parchment_bg(90308)
    n_frames = int(round(dur * FPS))
    hero_idx = int(round(2.15 * FPS))
    font_lbl = ImageFont.truetype(FONT, int(BAND_H * 0.112), index=1)  # ~59 px Didot Italic

    def curve(u: float) -> tuple[float, float]:
        x = 185.0 + 615.0 * u
        y = 890.0 - 300.0 * math.sin(u * math.pi * 0.80)
        return x, y

    enc = _open_encoder(out_mp4)
    assert enc.stdin is not None
    for fi in range(n_frames):
        t = fi / FPS
        im = bg.copy().convert("RGBA")
        ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        d = ImageDraw.Draw(ov)
        _draw_notebook_compass_lines(d, t, 0.3)

        _draw_earth(d, 175.0, 900.0, 82.0, prog(t, 0.04, 0.35))
        steps = 32
        drawn = int(prog(t, 0.15, 1.55) * steps)
        pts = [curve(i / steps) for i in range(drawn + 1)]
        if len(pts) > 1:
            d.line(pts, fill=col(INK_CG, 0.92), width=6)

        mp = 0.48 + 0.30 * prog(t, 0.25, dur - 0.15)
        mx, my = curve(mp)
        _draw_moon(d, mx, my, 44.0, prog(t, 0.35, 0.80))
        # Sideways arrow + downward drop arrow
        _draw_arrow(d, mx + 48, my, mx + 185, my, prog(t, 0.70, 1.65), width=7, head=20)
        _draw_arrow(d, mx, my + 48, mx, my + 165, prog(t, 1.40, 2.25), width=7, head=18)

        # Single Short DATA label inside 16:9 center band (569..1095), clear of Earth and bottom captions
        lbl_a = prog(t, 0.28, 0.62) * (1.0 - prog(t, dur - 0.38, dur - 0.05))
        if lbl_a > 0.02:
            d.text(
                (W / 2, BAND_TOP + BAND_H - 36),
                "SIDEWAYS AND DOWN",
                font=font_lbl,
                fill=col((252, 244, 224), lbl_a),
                anchor="mm",
                stroke_width=4,
                stroke_fill=col((36, 22, 12), lbl_a),
            )

        rgb = Image.alpha_composite(im, ov).convert("RGB")
        if fi == hero_idx:
            rgb.save(out_jpg, quality=92)
        enc.stdin.write(rgb.tobytes())

    enc.stdin.close()
    if enc.wait() != 0:
        raise SystemExit("ffmpeg encode failed on km_a_second_9x16")
    return {"file": str(out_mp4), "sha256": sha256(out_mp4), "duration_s": round(probe(out_mp4), 3)}


def render_orbit_teach_9x16(out_mp4: Path, out_jpg: Path, dur: float = 2.660) -> dict:
    """Short A S07 (2.660 s): Earth + full falling-sideways circular orbit diagram (pure diagram; S02 carries the 1 Short label)."""
    bg = make_parchment_bg(90306)
    n_frames = int(round(dur * FPS))
    hero_idx = int(round(2.05 * FPS))
    cx, cy, R = W / 2.0, 820.0, 250.0

    enc = _open_encoder(out_mp4)
    assert enc.stdin is not None
    for fi in range(n_frames):
        t = fi / FPS
        im = bg.copy().convert("RGBA")
        ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        d = ImageDraw.Draw(ov)
        _draw_notebook_compass_lines(d, t, 1.7)

        _draw_earth(d, cx, cy, 98.0, prog(t, 0.04, 0.35))
        ang0 = -0.35
        bx = cx + R * math.cos(ang0)
        by = cy + R * math.sin(ang0)
        ba = prog(t, 0.12, 0.42)
        if ba > 0.01:
            d.ellipse((bx - 16, by - 16, bx + 16, by + 16), fill=col(INK_CG, ba))
        _draw_arrow(d, bx + 16, by, bx + 135, by - 40, prog(t, 0.30, 0.95), width=6, head=18)
        _draw_arrow(d, bx, by + 16, bx - 35, by + 115, prog(t, 0.75, 1.35), width=6, head=18)

        arc_p = prog(t, 0.90, 2.35)
        if arc_p > 0.01:
            d.arc((cx - R, cy - R, cx + R, cy + R), start=0, end=int(360 * arc_p), fill=col(INK_CG, 0.90), width=6)
            d.arc((cx - R - 26, cy - R - 26, cx + R + 26, cy + R + 26), start=0, end=int(360 * arc_p), fill=col(INK_CG, 0.35), width=3)
        for i, frac in enumerate((0.28, 0.56, 0.82)):
            if arc_p < frac:
                continue
            a = ang0 + frac * math.tau
            x = cx + R * math.cos(a)
            y = cy + R * math.sin(a)
            d.ellipse((x - 11, y - 11, x + 11, y + 11), fill=col(INK_CG, 1.0))
            tx, ty = -math.sin(a), math.cos(a)
            _draw_arrow(d, x, y, x + tx * 68, y + ty * 68, prog(t, 1.05 + i * 0.25, 1.60 + i * 0.25), width=5, head=14)
            _draw_arrow(d, x, y, x - math.cos(a) * 56, y - math.sin(a) * 56, prog(t, 1.20 + i * 0.25, 1.75 + i * 0.25), width=5, head=14)

        rgb = Image.alpha_composite(im, ov).convert("RGB")
        if fi == hero_idx:
            rgb.save(out_jpg, quality=92)
        enc.stdin.write(rgb.tobytes())

    enc.stdin.close()
    if enc.wait() != 0:
        raise SystemExit("ffmpeg encode failed on orbit_teach_9x16")
    return {"file": str(out_mp4), "sha256": sha256(out_mp4), "duration_s": round(probe(out_mp4), 3)}


def render_sixty_earths_9x16(out_mp4: Path, out_jpg: Path, dur: float = 3.020) -> dict:
    """Short B S04 (3.020 s, overlaps 9-14s top title): 60 inked Earths in a graduated span to the Moon (no text label so no clash with 9-14s title)."""
    bg = make_parchment_bg(90403)
    n_frames = int(round(dur * FPS))
    hero_idx = int(round(2.40 * FPS))

    enc = _open_encoder(out_mp4)
    assert enc.stdin is not None
    for fi in range(n_frames):
        t = fi / FPS
        im = bg.copy().convert("RGBA")
        ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        d = ImageDraw.Draw(ov)
        _draw_notebook_compass_lines(d, t, 2.5)

        # Diagonal/arched span from bottom-left Earth (150, 1080) up-right to Moon (786, 610)
        ex, ey = 150.0, 1060.0
        mx, my = 786.0, 610.0
        _draw_earth(d, ex, ey, 68.0, prog(t, 0.04, 0.35))
        d.arc((ex - 108, ey - 108, ex + 108, ey + 108), -70, 20, fill=col(INK_CG, 0.50), width=3)

        n = 60
        shown = int(round(prog(t, 0.18, 2.35) * n))
        sx0, sy0 = ex + 82.0, ey - 58.0
        sx1, sy1 = mx - 62.0, my + 44.0
        if shown > 0:
            dx = (sx1 - sx0) / (n - 1)
            dy = (sy1 - sy0) / (n - 1)
            # Perpendicular normal for measuring ticks
            ln = math.hypot(dx, dy)
            nx_, ny_ = -dy / ln, dx / ln
            for i in range(shown):
                xx = sx0 + i * dx
                yy = sy0 + i * dy
                d.ellipse((xx - 6.5, yy - 6.5, xx + 6.5, yy + 6.5), fill=col(WASH_CG, 0.95), outline=col(INK_CG, 0.95), width=2)
                if i % 10 == 0:
                    d.line((xx + nx_ * 18, yy + ny_ * 18, xx + nx_ * 48, yy + ny_ * 48), fill=col(INK_CG, 0.80), width=4)
            end_x = sx0 + (shown - 1) * dx
            end_y = sy0 + (shown - 1) * dy
            d.line((sx0 + nx_ * 34, sy0 + ny_ * 34, end_x + nx_ * 34, end_y + ny_ * 34), fill=col(INK_CG, 0.70), width=3)

        _draw_moon(d, mx, my, 48.0, prog(t, 1.35, 2.20))

        rgb = Image.alpha_composite(im, ov).convert("RGB")
        if fi == hero_idx:
            rgb.save(out_jpg, quality=92)
        enc.stdin.write(rgb.tobytes())

    enc.stdin.close()
    if enc.wait() != 0:
        raise SystemExit("ffmpeg encode failed on sixty_earths_9x16")
    return {"file": str(out_mp4), "sha256": sha256(out_mp4), "duration_s": round(probe(out_mp4), 3)}


def _build_dot_square_img(span: int = 540) -> Image.Image:
    n = 60
    arr = np.zeros((span, span, 4), dtype=np.uint8)
    arr[:, :, 0] = WASH_CG[0]
    arr[:, :, 1] = WASH_CG[1]
    arr[:, :, 2] = WASH_CG[2]
    arr[:, :, 3] = 205
    step = span / n
    yy, xx = np.mgrid[0:n, 0:n]
    xs = ((xx + 0.5) * step).astype(int)
    ys = ((yy + 0.5) * step).astype(int)
    dot = np.zeros((span, span), dtype=bool)
    dot[ys, xs] = True
    stamped = np.zeros_like(dot)
    for dy in (-1, 0, 1):
        for dx in (-1, 0, 1):
            stamped |= np.roll(np.roll(dot, dy, 0), dx, 1)
    arr[stamped, 0] = INK_CG[0]
    arr[stamped, 1] = INK_CG[1]
    arr[stamped, 2] = INK_CG[2]
    arr[stamped, 3] = 245
    im = Image.fromarray(arr, "RGBA")
    d = ImageDraw.Draw(im)
    d.rectangle((0, 0, span - 1, span - 1), outline=(*INK_CG, 255), width=6)
    for k in range(10, 60, 10):
        pos = int(round(k * step))
        d.line((pos, 0, pos, span), fill=(*INK_CG, 150), width=2)
        d.line((0, pos, span, pos), fill=(*INK_CG, 150), width=2)
    return im


def render_dots_square_composite_9x16(
    bg_plate: Path,
    out_mp4: Path,
    out_jpg: Path,
    work: Path,
    dur: float = 3.150,
) -> dict:
    """Short B S06 (3.150 s): moving-plate composite of 60x60 dot square + SIXTY TIMES SIXTY over P4:02_spray_paint_c2."""
    bg_crop = work / "dots_bg_plate.mp4"
    cut_plate_segment(bg_plate, bg_crop, 0.50, dur, 380.0, 460.0)
    raw_bg = subprocess.check_output(
        [
            "ffmpeg", "-v", "error", "-i", str(bg_crop),
            "-f", "rawvideo", "-pix_fmt", "rgb24", "-",
        ]
    )
    frame_bytes = W * H * 3
    n_frames = min(int(round(dur * FPS)), len(raw_bg) // frame_bytes)
    hero_idx = min(n_frames - 1, int(round(2.35 * FPS)))

    dot_sq = _build_dot_square_img(520)
    sq_x, sq_y = (W - 520) // 2, 430
    font_lbl = ImageFont.truetype(FONT, int(BAND_H * 0.112), index=1)

    enc = _open_encoder(out_mp4)
    assert enc.stdin is not None
    for fi in range(n_frames):
        t = fi / FPS
        buf = raw_bg[fi * frame_bytes : (fi + 1) * frame_bytes]
        im = Image.frombytes("RGB", (W, H), buf).convert("RGBA")
        # Gentle warm period glaze so dark ink reads crisply over the moving plate
        ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        d = ImageDraw.Draw(ov)

        rows = prog(t, 0.12, 1.85) * 60.0
        if rows > 0.5:
            h_crop = max(2, int(dot_sq.height * rows / 60.0))
            crop = dot_sq.crop((0, 0, dot_sq.width, h_crop))
            ov.alpha_composite(crop, (sq_x, sq_y))

        # Earth, Moon, and shrinking pull arrow right below the 60x60 square
        _draw_earth(d, 250.0, 1085.0, 56.0, prog(t, 0.15, 0.45))
        _draw_moon(d, 710.0, 1085.0, 36.0, prog(t, 0.35, 0.70))
        shrink = prog(t, 1.35, 2.75)
        if shrink < 0.84:
            alen = 240.0 * (1.0 - shrink)
            _draw_arrow(d, 666.0, 1085.0, 666.0 - max(32.0, alen), 1085.0, prog(t, 0.70, 1.30), width=7, head=18)
        else:
            d.ellipse((646, 1075, 666, 1095), fill=col(INK_CG, 1.0))

        # Single Short DATA label ("SIXTY TIMES SIXTY") inside 16:9 center band (569..1095)
        lbl_a = prog(t, 0.30, 0.65) * (1.0 - prog(t, dur - 0.38, dur - 0.05))
        if lbl_a > 0.02:
            d.text(
                (W / 2, 995),
                "SIXTY TIMES SIXTY",
                font=font_lbl,
                fill=col((252, 244, 224), lbl_a),
                anchor="mm",
                stroke_width=5,
                stroke_fill=col((32, 18, 10), lbl_a),
            )

        rgb = Image.alpha_composite(im, ov).convert("RGB")
        if fi == hero_idx:
            rgb.save(out_jpg, quality=92)
        enc.stdin.write(rgb.tobytes())

    enc.stdin.close()
    if enc.wait() != 0:
        raise SystemExit("ffmpeg encode failed on dots_square_composite_9x16")
    return {"file": str(out_mp4), "sha256": sha256(out_mp4), "duration_s": round(probe(out_mp4), 3)}


# ---------------------------------------------------------------------------
# Audio helpers (locked VO, accepted 009 v04 score slice, house SFX kit)
# ---------------------------------------------------------------------------

def load_stt_words(stt_path: Path) -> list[tuple[str, float, float]]:
    raw = json.loads(stt_path.read_text())["words"]
    out = []
    for w in raw:
        txt = (w.get("text") or "").strip()
        if not txt or w.get("type") == "spacing":
            continue
        disp = UK_SPELLING.get(txt.lower(), txt)
        # Keep original capitalization for sentence starts if needed
        if txt[:1].isupper() and disp[:1].islower():
            disp = disp[:1].upper() + disp[1:]
        out.append((disp, float(w["start"]), float(w["end"])))
    return out


def prepare_vo(src_wav: Path, dst_wav: Path, speech_only_wav: Path, total_dur: float) -> None:
    ff("-i", str(src_wav), "-ar", "48000", "-ac", "2", "-c:a", "pcm_s16le", str(speech_only_wav))
    ff(
        "-i", str(speech_only_wav),
        "-af", f"apad=whole_dur={total_dur:.3f}",
        "-t", f"{total_dur:.3f}",
        "-c:a", "pcm_s16le",
        str(dst_wav),
    )


def place_sfx(kit_dir: Path, dst: Path, total: float, events: list[tuple[str, float, float, float]]) -> Path:
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
            f"afade=t=out:st={max(0.02, mdur - 0.22):.3f}:d=0.20,"
            f"volume={gdb:.1f}dB,adelay={ms}|{ms}[e{idx}]"
        )
        mix_labels.append(f"[e{idx}]")
    fc.append("".join(mix_labels) + f"amix=inputs={len(mix_labels)}:normalize=0:duration=first,alimiter=limit=0.5[a]")
    ff(*inputs, "-filter_complex", ";".join(fc), "-map", "[a]", "-c:a", "pcm_s16le", str(dst))
    return dst


# ---------------------------------------------------------------------------
# Typography & Overlays (936x1664 house Didot)
# ---------------------------------------------------------------------------

def chunk_words(ws: list[tuple[str, float, float]], total: float, hook_end_t: float) -> list[dict]:
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
        t0_show = max(t0, hook_end_t)
        if t1 > t0_show + 0.12:
            chunks.append({
                "text": " ".join(parts),
                "t0": round(t0_show, 3),
                "t1": round(min(t1, total - 0.05), 3),
            })
        i = j
    return chunks


def render_hook_lines(path: Path, lines_markup: list[str], *, top_frac: float, cap_frac: float) -> dict:
    """Render 2-line hook caption in house Didot bold with #FFE000 yellow keyword."""
    size = 80
    while True:
        font = ImageFont.truetype(FONT, size, index=2)
        cap = -font.getbbox("H", anchor="ls")[1]
        if cap >= cap_frac * H:
            break
        size += 2
    parsed = [[(w.strip("*"), w.startswith("**")) for w in ln.split()] for ln in lines_markup]
    # Ensure widest line fits comfortably inside W - 80
    while size > 56:
        font = ImageFont.truetype(FONT, size, index=2)
        widest = max(font.getlength(" ".join(t for t, _ in ln)) for ln in parsed)
        if widest <= W - 80:
            break
        size -= 2
    cap = -font.getbbox("H", anchor="ls")[1]
    pitch = round(cap * 1.24)
    block = pitch * (len(parsed) - 1) + cap
    top = int(H * top_frac)
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    space = font.getlength(" ")
    widest = 0.0
    for k, ln in enumerate(parsed):
        base = top + cap + k * pitch
        lw = font.getlength(" ".join(t for t, _ in ln))
        widest = max(widest, lw)
        x = (W - lw) / 2.0
        for t_str, hot in ln:
            draw.text(
                (x, base),
                t_str,
                font=font,
                anchor="ls",
                fill=YEL if hot else WHITE,
                stroke_width=7,
                stroke_fill=INK,
            )
            x += font.getlength(t_str) + space
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


def verify_all_inputs() -> tuple[dict[str, Path], dict[str, str]]:
    paths: dict[str, Path] = {}
    hashes: dict[str, str] = {}
    for row_id, (lp, np_, exp_sha, _prod) in LOCKED_PLATES.items():
        if not lp.is_file():
            raise SystemExit(f"Missing local plate: {lp}")
        if not np_.is_file():
            raise SystemExit(f"Missing NAS plate: {np_}")
        h_loc = sha256(lp)
        h_nas = sha256(np_)
        if h_loc != h_nas:
            raise SystemExit(f"Local/NAS SHA-256 mismatch on {row_id}: {h_loc} != {h_nas}")
        if not h_loc.startswith(exp_sha):
            raise SystemExit(f"Expected SHA-256 mismatch on {row_id}: {h_loc} != {exp_sha}")
        paths[row_id] = lp
        hashes[row_id] = h_loc

    for row_id, (fn, exp_sha) in PARENT_CODE_GRAPHICS.items():
        p = NAS_PROJ / "07_Edit-Project/code_graphics_v01" / fn
        if not p.is_file() or sha256(p) != exp_sha:
            raise SystemExit(f"Parent code graphic mismatch: {fn}")
        paths[f"parent_{row_id}"] = p
        hashes[f"parent_{row_id}"] = exp_sha

    if not SCORE_WAV.is_file() or sha256(SCORE_WAV) != SCORE_SHA:
        raise SystemExit(f"Accepted score mismatch: {SCORE_WAV}")
    return paths, hashes


def assemble_one(
    *,
    short_key: str,
    stem_out: str,
    yt_title: str,
    air_date_check: str,
    hook_lines: list[str],
    hook_plain: str,
    hook_top_frac: float,
    hook_cap_frac: float,
    hook_end_t: float,
    total_dur: float,
    vo_src_mp3: Path,
    vo_src_wav: Path,
    vo_mp3_sha: str,
    vo_wav_sha: str,
    stt_path: Path,
    locked_script_text: str,
    beats: list[dict],
    score_start_s: float,
    sfx_events: list[tuple[str, float, float, float]],
    payoff_word_prefix: str,
    plate_paths: dict[str, Path],
    plate_hashes: dict[str, str],
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
    prepare_vo(vo_src_wav, vo_wav, speech_wav, total_dur)
    ws = load_stt_words(stt_path)
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
            src_sha = plate_hashes[b["row_id"]]
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

    # Music bed slice from accepted J3241 HOS 009 score (hos_009_score_v04_synth.wav)
    bed_slice = work / f"{stem_out}_bed_slice.wav"
    ff(
        "-ss", f"{score_start_s:.3f}", "-t", f"{total_dur + 0.5:.3f}",
        "-i", str(SCORE_WAV),
        "-ar", "48000", "-ac", "2", "-c:a", "pcm_s16le",
        str(bed_slice),
    )

    # SFX stem + stem mix check via sfx_kit.py level
    kit_dir = NAS_PROJ / "06_Sound-Effects/kit_v01"
    sfx_raw = place_sfx(kit_dir, work / "sfx_raw.wav", total_dur, sfx_events)
    audio_mix = work / "audio_mix.wav"
    bed_db, sfx_db, sfx_level = -12.0, -14.0, {}
    stems: dict[str, Path] = {}
    for _ in range(8):
        ff(
            "-i", str(vo_wav), "-i", str(bed_slice), "-i", str(sfx_raw),
            "-filter_complex",
            f"[0:a]aformat=sample_rates=48000:channel_layouts=stereo,atrim=0:{total_dur:.3f}[v];"
            f"[1:a]aformat=sample_rates=48000:channel_layouts=stereo,atrim=0:{total_dur:.3f},asetpts=PTS-STARTPTS,"
            f"volume={bed_db:.2f}dB,afade=t=in:d=0.10,afade=t=out:st={total_dur - 0.25:.3f}:d=0.25[b];"
            f"[2:a]aformat=sample_rates=48000:channel_layouts=stereo,atrim=0:{total_dur:.3f},volume={sfx_db:.2f}dB[s];"
            "[v][b][s]amix=inputs=3:normalize=0:duration=first,alimiter=limit=0.89[a]",
            "-map", "[a]", "-t", f"{total_dur:.3f}", "-c:a", "pcm_s16le",
            str(audio_mix),
        )
        for sname, ssrc, af_extra in (
            ("vo", vo_wav, f"atrim=0:{total_dur:.3f}"),
            ("bed", bed_slice, f"volume={bed_db:.2f}dB,atrim=0:{total_dur:.3f},afade=t=in:d=0.10,afade=t=out:st={total_dur - 0.25:.3f}:d=0.25"),
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
        bed_db -= 2.0
        sfx_db -= 2.0
    if sfx_level.get("exit") != 0:
        raise SystemExit(f"{short_key}: sfx_kit.py level failed: {sfx_level.get('output')}")

    # Overlays: frame-0 hook, bottom VO captions (after hook_end_t), 9-14s promoted-long title
    chunks = chunk_words(ws, total_dur, hook_end_t)
    overlays: list[tuple[Path, float, float, str, str]] = []
    hook_png = work / "cap_hook.png"
    hook_meta = render_hook_lines(hook_png, hook_lines, top_frac=hook_top_frac, cap_frac=hook_cap_frac)
    overlays.append((hook_png, 0.0, hook_end_t, "hook", hook_plain))

    for idx, c in enumerate(chunks):
        c_png = work / f"cap_{idx:03d}.png"
        render_text_overlay(c_png, c["text"], 48, 195, anchor="bottom")
        overlays.append((c_png, c["t0"], c["t1"], "vo", c["text"]))

    title_png = work / "cap_title.png"
    render_text_overlay(title_png, LONG_TITLE, 50, 155, index=2, anchor="top")
    overlays.append((title_png, TITLE_IN, TITLE_OUT, "title", LONG_TITLE))

    inputs = ["-i", str(pic_mp4), "-i", str(audio_mix)]
    for png, *_ in overlays:
        inputs += ["-loop", "1", "-i", str(png)]

    fc, last_v = [], "[0:v]"
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
    payoff_w = next(w for w in ws if w[0].lower().startswith(payoff_word_prefix.lower()))

    # Full stream decode check (0 errors)
    dec = subprocess.run(
        ["ffmpeg", "-v", "error", "-i", str(mp4_scratch), "-f", "null", "-"],
        capture_output=True,
        text=True,
    )
    if dec.returncode != 0 or dec.stderr.strip():
        raise SystemExit(f"{short_key}: decode check failed: {dec.stderr}")

    nas_short_dir = NAS_PROJ / "10_Shorts/J2171" / short_key
    meta_payload = {
        "film": "HOS:009",
        "job": "J2171",
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
            "score_source": str(SCORE_WAV),
            "score_sha256": SCORE_SHA,
            "score_start_s": score_start_s,
            "level": level,
            "sfx_level": sfx_level,
            "stems": {
                "vo": str(nas_short_dir / "stems/stem_vo.wav"),
                "bed": str(nas_short_dir / "stems/stem_bed.wav"),
                "sfx": str(nas_short_dir / "stems/stem_sfx.wav"),
            },
        },
        "cuts": plan_rows,
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
            sys.executable, str(OWB / "scripts/music_gate.py"), str(NAS_PROJ),
            "--bed", str(SCORE_WAV), "--video", str(mp4_scratch), "--out", str(qa_dir / "music_gate.json"),
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

    # Run vo_check_py312.sh on speech_wav against exact locked script
    vo_script_md = work / "short_script_check.md"
    vo_script_md.write_text(locked_script_text + "\n")
    r_vo = subprocess.run(
        [str(REPO / "00_Brand/Channel-Setup/tools/vo_check_py312.sh"), str(speech_wav), "--script", str(vo_script_md)],
        capture_output=True,
        text=True,
    )
    vo_txt = (r_vo.stdout + r_vo.stderr).strip()
    (qa_dir / "vo_check.txt").write_text(vo_txt + "\n")
    gate_results["vo_check"] = {"exit": r_vo.returncode, "output": vo_txt}
    if r_vo.returncode != 0:
        raise SystemExit(f"{short_key} vo_check FAILED (exit {r_vo.returncode}):\n{vo_txt}")

    (qa_dir / "sfx.txt").write_text(sfx_level["output"] + "\n")
    gate_results["sfx"] = {"exit": sfx_level["exit"], "output": sfx_level["output"]}

    # Stage durable copies to NAS_PROJ and HOS UAT (iCloud) with full SHA-256 verification
    (nas_short_dir / "stems").mkdir(parents=True, exist_ok=True)
    nas_mp4 = nas_short_dir / f"{stem_out}.mp4"
    mp4_sha = sha256(mp4_scratch)
    shutil.copy2(mp4_scratch, nas_mp4)
    if sha256(nas_mp4) != mp4_sha:
        raise SystemExit(f"{short_key}: NAS master MP4 SHA-256 mismatch")

    HOS_UAT.mkdir(parents=True, exist_ok=True)
    uat_mp4 = HOS_UAT / f"{stem_out}.mp4"
    shutil.copy2(mp4_scratch, uat_mp4)
    if sha256(uat_mp4) != mp4_sha:
        raise SystemExit(f"{short_key}: HOS UAT master MP4 SHA-256 mismatch")

    stem_hashes = {}
    for sname, spath in stems.items():
        dst_s = nas_short_dir / "stems" / spath.name
        s_sha = sha256(spath)
        shutil.copy2(spath, dst_s)
        if sha256(dst_s) != s_sha:
            raise SystemExit(f"{short_key}: NAS stem {sname} SHA-256 mismatch")
        stem_hashes[sname] = {"nas_path": str(dst_s), "sha256": s_sha, "bytes": dst_s.stat().st_size}

    meta_payload["nas_master_mp4"] = str(nas_mp4)
    meta_payload["uat_master_mp4"] = str(uat_mp4)
    meta_payload["master_sha256"] = mp4_sha
    meta_payload["master_bytes"] = nas_mp4.stat().st_size
    meta_payload["audio"]["stem_hashes"] = stem_hashes
    meta_payload["hook_metrics"] = hook_meta

    meta_git = HERE / f"{stem_out}_meta.json"
    meta_git.write_text(json.dumps(meta_payload, indent=2) + "\n")
    shutil.copy2(meta_git, nas_short_dir / f"{stem_out}_meta.json")

    # Build a 9-tile timeline contact sheet in qa_dir + sync QA sheets to NAS (keep images out of git!)
    tiles = []
    for k, row in enumerate(plan_rows):
        t_mid = round((row["t0"] + row["t1"]) / 2.0, 3)
        if k == 0:
            t_mid = 0.50
        tp = work / f"tile_{k:02d}.png"
        ff("-ss", f"{t_mid:.3f}", "-i", str(mp4_scratch), "-frames:v", "1", "-vf", "scale=234:416", str(tp))
        tiles.append(tp)
    row_sheet = qa_dir / f"{stem_out}_rows_sheet.jpg"
    ff(
        *[x for tp in tiles for x in ("-i", str(tp))],
        "-filter_complex", f"hstack=inputs={len(tiles)}",
        str(row_sheet),
    )

    # Sync QA directory (including jpg sheets) to NAS_PROJ/10_Shorts/qa_<short_key>_v01
    nas_qa_dir = NAS_PROJ / "10_Shorts" / f"qa_{short_key}_v01"
    if nas_qa_dir.exists():
        shutil.rmtree(nas_qa_dir)
    shutil.copytree(qa_dir, nas_qa_dir)

    build_summary = {
        "short_id": short_key,
        "stem": stem_out,
        "youtube_title": yt_title,
        "nas_master_mp4": str(nas_mp4),
        "uat_master_mp4": str(uat_mp4),
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
        "score_nas_path": str(SCORE_WAV),
        "score_sha256": SCORE_SHA,
        "score_start_s": score_start_s,
        "stem_hashes": stem_hashes,
        "gates": {k: {"exit": v["exit"]} for k, v in gate_results.items()},
    }
    (qa_dir / "BUILD.json").write_text(json.dumps(build_summary, indent=2) + "\n")
    shutil.copy2(qa_dir / "BUILD.json", nas_qa_dir / "BUILD.json")
    return build_summary


def main() -> None:
    plate_paths, plate_hashes = verify_all_inputs()
    SCRATCH_ROOT.mkdir(parents=True, exist_ok=True)

    # 1. Render £0 full-bleed 936x1664 portrait code graphics and stage to NAS code_graphics_v01
    cg_scratch = SCRATCH_ROOT / "code_graphics_9x16"
    cg_scratch.mkdir(parents=True, exist_ok=True)

    cg_a_s02_mp4 = cg_scratch / "code_graphic_009_short_A_s02_km_a_second_9x16.mp4"
    cg_a_s02_jpg = cg_scratch / "cg_short_A_s02_km_a_second_9x16.jpg"
    cg_a_s02_info = render_km_a_second_9x16(cg_a_s02_mp4, cg_a_s02_jpg, dur=2.940)

    cg_a_s07_mp4 = cg_scratch / "code_graphic_009_short_A_s07_orbit_teach_9x16.mp4"
    cg_a_s07_jpg = cg_scratch / "cg_short_A_s07_orbit_teach_9x16.jpg"
    cg_a_s07_info = render_orbit_teach_9x16(cg_a_s07_mp4, cg_a_s07_jpg, dur=2.660)

    cg_b_s04_mp4 = cg_scratch / "code_graphic_009_short_B_s04_sixty_earths_9x16.mp4"
    cg_b_s04_jpg = cg_scratch / "cg_short_B_s04_sixty_earths_9x16.jpg"
    cg_b_s04_info = render_sixty_earths_9x16(cg_b_s04_mp4, cg_b_s04_jpg, dur=3.020)

    cg_b_s06_mp4 = cg_scratch / "code_graphic_009_short_B_s06_dots_square_9x16.mp4"
    cg_b_s06_jpg = cg_scratch / "cg_short_B_s06_dots_square_9x16.jpg"
    cg_b_s06_info = render_dots_square_composite_9x16(
        plate_paths["P4:02_spray_paint_c2"], cg_b_s06_mp4, cg_b_s06_jpg, cg_scratch, dur=3.150
    )

    nas_cg_dir = NAS_PROJ / "07_Edit-Project/code_graphics_v01"
    nas_cg_dir.mkdir(parents=True, exist_ok=True)
    for src_cg, info in (
        (cg_a_s02_mp4, cg_a_s02_info),
        (cg_a_s07_mp4, cg_a_s07_info),
        (cg_b_s04_mp4, cg_b_s04_info),
        (cg_b_s06_mp4, cg_b_s06_info),
    ):
        dst_cg = nas_cg_dir / src_cg.name
        shutil.copy2(src_cg, dst_cg)
        if sha256(dst_cg) != info["sha256"]:
            raise SystemExit(f"NAS code graphic SHA-256 mismatch: {dst_cg}")

    cg_paths = {
        "P3:08_km_a_second": cg_a_s02_mp4,
        "P3:06_orbit_teach": cg_a_s07_mp4,
        "P4:03_sixty_earths": cg_b_s04_mp4,
        "P4:04_dots_square": cg_b_s06_mp4,
    }

    # 2. Assemble Short A (25.320 s = 24.320 s VO + 1.000 s loop tail)
    beats_a = [
        {"id": "S01", "row_id": "P1:01_moon_falling", "kind": "plate", "t0": 0.000, "t1": 2.800, "in_s": 2.000, "x0": 260.0, "x1": 360.0, "lands_on": "plate"},
        {"id": "S02", "row_id": "P3:08_km_a_second", "kind": "code_graphic", "t0": 2.800, "t1": 5.740, "in_s": 0.000, "lands_on": "code_graphic"},
        {"id": "S03", "row_id": "P3:07_ball_to_moon", "kind": "plate", "t0": 5.740, "t1": 8.980, "in_s": 0.500, "x0": 320.0, "x1": 680.0, "lands_on": "plate"},
        {"id": "S04", "row_id": "P3:05_shot_orbit", "kind": "plate", "t0": 8.980, "t1": 12.140, "in_s": 1.000, "x0": 420.0, "x1": 560.0, "lands_on": "plate"},
        {"id": "S05", "row_id": "P2:07_orchard_bench", "kind": "plate", "t0": 12.140, "t1": 15.420, "in_s": 1.200, "x0": 540.0, "x1": 560.0, "lands_on": "plate"},
        {"id": "S06", "row_id": "P2:08_the_apple", "kind": "plate", "t0": 15.420, "t1": 18.620, "in_s": 0.400, "x0": 450.0, "x1": 460.0, "lands_on": "plate"},
        {"id": "S07", "row_id": "P3:06_orbit_teach", "kind": "code_graphic", "t0": 18.620, "t1": 21.280, "in_s": 0.000, "lands_on": "code_graphic"},
        {"id": "S08", "row_id": "P5:09_orchard_dusk", "kind": "plate", "t0": 21.280, "t1": 24.320, "in_s": 0.500, "x0": 360.0, "x1": 480.0, "lands_on": "plate"},
        {"id": "loop_tail", "row_id": "P1:01_moon_falling", "kind": "plate", "t0": 24.320, "t1": 25.320, "in_s": 1.000, "x0": 225.0, "x1": 260.0, "lands_on": "loop"},
    ]
    res_a = assemble_one(
        short_key="short_A",
        stem_out="hos_009_short_A_v01",
        yt_title="What Would Happen If the Moon Stopped Moving?",
        air_date_check="2026-11-27",
        hook_lines=["IT'S", "**FALLING**"],
        hook_plain="IT'S FALLING",
        hook_top_frac=0.255,
        hook_cap_frac=0.078,
        hook_end_t=2.000,
        total_dur=25.320,
        vo_src_mp3=NAS_PROJ / "10_Shorts/vo_v02/hos_009_short_A_v02.mp3",
        vo_src_wav=NAS_PROJ / "10_Shorts/vo_v02/hos_009_short_A_v02.wav",
        vo_mp3_sha="c2fd407d3aafbe57030b29b213ed128ee4887b785272a2192b4c0809796a1ce6",
        vo_wav_sha="48847b15feda51804a0f6afae1a79aacc74b9bac43ef3eeadda8a7503b745571",
        stt_path=NAS_PROJ / "10_Shorts/vo_v02/stt/hos_009_short_A_v02/stt_raw.json",
        locked_script_text=(
            "The Moon is falling towards the Earth right now. Every second, it moves sideways about a kilometre, "
            "and drops a tiny bit towards us. But the Earth curves away beneath it, so it keeps on missing. "
            "Isaac Newton worked this out, more than three hundred years ago. An orbit isn't floating at all. "
            "It's falling, and missing, for ever."
        ),
        beats=beats_a,
        score_start_s=2.0,  # Part 1 awe/wonder 62 BPM
        sfx_events=[
            ("whoosh", 0.00, -14.0, 0.75),
            ("tick", 2.84, -9.0, 0.06),
            ("tick", 18.66, -9.0, 0.06),
        ],
        payoff_word_prefix="orbit",
        plate_paths=plate_paths,
        plate_hashes=plate_hashes,
        cg_paths=cg_paths,
    )
    shutil.copy2(cg_a_s02_jpg, NAS_PROJ / "10_Shorts/qa_short_A_v01/cg_s02_km_a_second_9x16.jpg")
    shutil.copy2(cg_a_s07_jpg, NAS_PROJ / "10_Shorts/qa_short_A_v01/cg_s07_orbit_teach_9x16.jpg")

    # 3. Assemble Short B (25.480 s = 24.480 s VO + 1.000 s loop tail)
    beats_b = [
        {"id": "S01", "row_id": "P4:05_minute_second", "kind": "plate", "t0": 0.000, "t1": 2.820, "in_s": 2.000, "x0": 720.0, "x1": 875.0, "lands_on": "plate"},
        {"id": "S02", "row_id": "P1:02_apple_and_moon", "kind": "plate", "t0": 2.820, "t1": 5.560, "in_s": 0.800, "x0": 437.0, "x1": 480.0, "lands_on": "plate"},
        {"id": "S03", "row_id": "P4:06_pretty_nearly", "kind": "plate", "t0": 5.560, "t1": 8.420, "in_s": 1.000, "x0": 437.0, "x1": 460.0, "lands_on": "plate"},
        {"id": "S04", "row_id": "P4:03_sixty_earths", "kind": "code_graphic", "t0": 8.420, "t1": 11.440, "in_s": 0.000, "lands_on": "code_graphic"},
        {"id": "S05", "row_id": "P4:02_spray_paint", "kind": "plate", "t0": 11.440, "t1": 14.500, "in_s": 1.200, "x0": 360.0, "x1": 440.0, "lands_on": "plate"},
        {"id": "S06", "row_id": "P4:04_dots_square", "kind": "code_graphic", "t0": 14.500, "t1": 17.650, "in_s": 0.000, "lands_on": "code_graphic"},
        {"id": "S07", "row_id": "P4:06_pretty_nearly_c1", "kind": "plate", "t0": 17.650, "t1": 20.820, "in_s": 1.000, "x0": 437.0, "x1": 460.0, "lands_on": "plate"},
        {"id": "S08", "row_id": "P5:01_one_law", "kind": "plate", "t0": 20.820, "t1": 24.480, "in_s": 1.000, "x0": 437.0, "x1": 450.0, "lands_on": "plate"},
        {"id": "loop_tail", "row_id": "P4:05_minute_second", "kind": "plate", "t0": 24.480, "t1": 25.480, "in_s": 1.000, "x0": 680.0, "x1": 720.0, "lands_on": "loop"},
    ]
    res_b = assemble_one(
        short_key="short_B",
        stem_out="hos_009_short_B_v01",
        yt_title="How Did Newton Discover Gravity?",
        air_date_check="2026-11-30",
        hook_lines=["1 MINUTE =", "**1** **SECOND**"],
        hook_plain="1 MINUTE = 1 SECOND",
        hook_top_frac=0.080,
        hook_cap_frac=0.068,
        hook_end_t=2.000,
        total_dur=25.480,
        vo_src_mp3=NAS_PROJ / "10_Shorts/vo_v02/hos_009_short_B_v04.mp3",
        vo_src_wav=NAS_PROJ / "10_Shorts/vo_v02/hos_009_short_B_v04.wav",
        vo_mp3_sha="0c9c4c6ffdb1337dc11acaf57af909f8d8be91d77210bca2e13af80715b87498",
        vo_wav_sha="a6666fd27c9a90e781369ea07e4888d87a2d5edb1624a0090ae98fa39504686b",
        stt_path=NAS_PROJ / "10_Shorts/vo_v02/stt/hos_009_short_B_v04/stt_raw.json",
        locked_script_text=(
            "In one minute, the Moon falls five metres. An apple falls that far in one second. "
            "Isaac Newton worked out why. The Moon is sixty times further from the Earth's centre than we are, "
            "so the pull on it is sixty times sixty weaker. Three thousand six hundred times. "
            "And the numbers matched. One pull, for apples and Moons."
        ),
        beats=beats_b,
        score_start_s=262.0,  # Part 4 explain rhythmic chamber pulse 67 BPM
        sfx_events=[
            ("whoosh", 0.00, -14.0, 0.75),
            ("tick", 8.46, -9.0, 0.06),
            ("tick", 14.55, -9.0, 0.06),
        ],
        payoff_word_prefix="numbers",
        plate_paths=plate_paths,
        plate_hashes=plate_hashes,
        cg_paths=cg_paths,
    )
    shutil.copy2(cg_b_s04_jpg, NAS_PROJ / "10_Shorts/qa_short_B_v01/cg_s04_sixty_earths_9x16.jpg")
    shutil.copy2(cg_b_s06_jpg, NAS_PROJ / "10_Shorts/qa_short_B_v01/cg_s06_dots_square_9x16.jpg")

    # Remove image files from git worktree qa dirs (already synced to NAS_PROJ/10_Shorts/qa_*)
    for sk in ("short_A", "short_B"):
        qdir = HERE / f"qa_{sk}_v01"
        for img_p in list(qdir.rglob("*.jpg")) + list(qdir.rglob("*.png")):
            img_p.unlink()

    manifest_dir = HERE / "J2171"
    manifest_dir.mkdir(parents=True, exist_ok=True)
    delivery = {
        "job": "J2171",
        "film": "HOS:009",
        "assembler": "gemini",
        "gbp_spent": 0,
        "credits_spent": 0,
        "parent_long_status": "not_uploaded_yet_must_be_public_before_shorts",
        "conditional_planning_targets": {
            "long_planned": "2026-11-26T18:00:00Z",
            "short_A_conditional": "2026-11-27T11:30:00Z (Fri; note Sat 2026-11-28 11:30Z is go-public-day Short slot under 7 Nov week rule)",
            "short_B_conditional": "2026-11-30T11:30:00Z (brief conditional target; note Mon is not a locked HOS Sat/Fri/Sun/Tue Short weekday — Sun 2026-11-29 or Tue 2026-12-01 11:30Z matches the 7 Nov week)",
            "ben_watch_ready_target": "2026-11-24T18:00:00Z",
        },
        "duplicate_check": {
            "snapshot": "05_Analytics/hos/snapshots/2026-11-20.json",
            "total_hos_videos_checked": 69,
            "gravity_newton_moon_orbit_matches": 0,
        },
        "code_graphics_9x16": {
            "short_A_s02": {
                "nas_path": str(nas_cg_dir / cg_a_s02_mp4.name),
                "sha256": cg_a_s02_info["sha256"],
                "duration_s": cg_a_s02_info["duration_s"],
                "derived_from_parent": PARENT_CODE_GRAPHICS["P3:08_km_a_second"],
            },
            "short_A_s07": {
                "nas_path": str(nas_cg_dir / cg_a_s07_mp4.name),
                "sha256": cg_a_s07_info["sha256"],
                "duration_s": cg_a_s07_info["duration_s"],
                "derived_from_parent": PARENT_CODE_GRAPHICS["P3:06_orbit_teach"],
            },
            "short_B_s04": {
                "nas_path": str(nas_cg_dir / cg_b_s04_mp4.name),
                "sha256": cg_b_s04_info["sha256"],
                "duration_s": cg_b_s04_info["duration_s"],
                "derived_from_parent": PARENT_CODE_GRAPHICS["P4:03_sixty_earths"],
            },
            "short_B_s06": {
                "nas_path": str(nas_cg_dir / cg_b_s06_mp4.name),
                "sha256": cg_b_s06_info["sha256"],
                "duration_s": cg_b_s06_info["duration_s"],
                "derived_from_parent": PARENT_CODE_GRAPHICS["P4:04_dots_square"],
                "background_moving_plate": {
                    "row_id": "P4:02_spray_paint_c2",
                    "sha256": plate_hashes["P4:02_spray_paint_c2"],
                },
            },
        },
        "shorts": {"Short_A": res_a, "Short_B": res_b},
    }
    (manifest_dir / "DELIVERY_MANIFEST.json").write_text(json.dumps(delivery, indent=2) + "\n")
    shutil.copy2(manifest_dir / "DELIVERY_MANIFEST.json", NAS_PROJ / "10_Shorts/J2171/DELIVERY_MANIFEST.json")
    print(json.dumps(delivery, indent=2))


if __name__ == "__main__":
    main()
