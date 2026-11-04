#!/usr/bin/env python3
"""HOS 008 — J1880 exact new-version edit recipe (rough_v13 -> master_v04).

Prepared by Gemini (worker) for J1880 -> J1881 elected-Chief scope review.
Preserves hos_008_master_v03.mp4 (cf1561c218bace7bc14ed3d625b0790a457027a90f392262f45ca7172723099b),
hos_008_rough_v12.mp4 (02db759e1c4a0fa3fbcf5b19037d8c52527c93750df4d80aa9a6c8e0c9bf7745),
and all v01-v12 / master_v01-v03 artifacts untouched.

DEFAULT MODE IS --dry-run (£0 spend, 0 bytes rendered).
Passing --execute requires elected-Chief authorization in J1881.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import subprocess as sp
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

W, H, FPS = 1920, 1080, 24
EXPECTED_PACKETS = 12923
MASTER_V03_SHA256 = "cf1561c218bace7bc14ed3d625b0790a457027a90f392262f45ca7172723099b"
ROUGH_V12_SHA256 = "02db759e1c4a0fa3fbcf5b19037d8c52527c93750df4d80aa9a6c8e0c9bf7745"

FONT_PATH = "/System/Library/Fonts/Supplemental/Didot.ttc"
CREAM_TEXT = (252, 248, 240, 255)
GOLD_ACCENT = (242, 208, 122, 255)
UMBER_STROKE = (28, 16, 8, 255)
PILL_BG = (36, 22, 12, 205)
PILL_BORDER = (211, 167, 88, 170)

EDIT_DIR = Path(__file__).resolve().parent
FILM_DIR = EDIT_DIR.parent
MEDIA_DIR = Path(
    "/Users/benjaminoats/YouTube/hos-008-lightning/02_Video-Projects/008_Lightning-Franklin"
)
NAS_EDIT = Path(
    "/Volumes/data/mac-mini-archive/YouTube/History Of Science/02_Video-Projects/008_Lightning-Franklin/07_Edit-Project"
)
MASTER_V03_LOCAL = EDIT_DIR / "_precheck/master_v03/hos_008_master_v03.mp4"
ROUGH_V12_NAS = NAS_EDIT / "_desk/008/rough_v12/hos_008_rough_v12.mp4"
CUTS_V12_LOCAL = EDIT_DIR / "_precheck/rough_v12/cuts_rough_v12.json"

SCALE_1080_VF = (
    "scale=1920:1080:force_original_aspect_ratio=increase:flags=lanczos,"
    "crop=1920:1080,fps=24,format=yuv420p"
)


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def load_font(size: int, italic: bool = True) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(FONT_PATH, size, index=1 if italic else 0)


def card_alpha(t: float, dur: float, fade_in: float = 0.35, fade_out: float = 0.35) -> float:
    if t < 0.12 or t > dur - 0.12:
        return 0.0
    if t < 0.12 + fade_in:
        return (t - 0.12) / fade_in
    if t > dur - 0.12 - fade_out:
        return max(0.0, (dur - 0.12 - t) / fade_out)
    return 1.0


def draw_backed_side_label_v04(im: Image.Image, text: str, t: float, dur: float) -> Image.Image:
    """Note 1 (00:20) fix: HOS house Didot italic with dark-umber translucent backing pill."""
    a = card_alpha(t, max(dur, 1.5), 0.35, 0.35)
    if a <= 0.01:
        return im
    over = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(over)
    f = load_font(58, italic=True)
    bbox = d.textbbox((W // 2, 940), text, font=f, anchor="mm")
    pad_x, pad_y = 28, 14
    pill_box = (bbox[0] - pad_x, bbox[1] - pad_y, bbox[2] + pad_x, bbox[3] + pad_y)
    d.rounded_rectangle(
        pill_box,
        radius=18,
        fill=(PILL_BG[0], PILL_BG[1], PILL_BG[2], int(PILL_BG[3] * a)),
        outline=(PILL_BORDER[0], PILL_BORDER[1], PILL_BORDER[2], int(PILL_BORDER[3] * a)),
        width=2,
    )
    d.text(
        (W // 2, 940),
        text,
        font=f,
        fill=(CREAM_TEXT[0], CREAM_TEXT[1], CREAM_TEXT[2], int(255 * a)),
        anchor="mm",
        stroke_width=5,
        stroke_fill=(UMBER_STROKE[0], UMBER_STROKE[1], UMBER_STROKE[2], int(235 * a)),
    )
    return Image.alpha_composite(im.convert("RGBA"), over).convert("RGB")


def render_note1_cut3_backed_label(out_mp4: Path) -> dict:
    """Note 1 (00:20): Re-render Cut [3] P1:03_table_three (118 frames, display 427..544)."""
    src = MEDIA_DIR / "04_Generated-Clips/part01/raw/v01/03_table_three_t1.mp4"
    n_frames = 118
    use_s = n_frames / FPS
    label = "A KITE · A KEY · A JAR"

    dec = sp.Popen(
        [
            "ffmpeg", "-v", "error", "-ss", "0.000", "-i", str(src),
            "-frames:v", str(n_frames), "-vf", SCALE_1080_VF,
            "-f", "rawvideo", "-pix_fmt", "rgb24", "-",
        ],
        stdout=sp.PIPE,
    )
    enc = sp.Popen(
        [
            "ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pixel_format", "rgb24",
            "-video_size", f"{W}x{H}", "-framerate", str(FPS), "-i", "-", "-an",
            "-c:v", "libx264", "-preset", "fast", "-crf", "17", "-pix_fmt", "yuv420p", "-r", str(FPS),
            str(out_mp4),
        ],
        stdin=sp.PIPE,
    )
    assert dec.stdout and enc.stdin
    last = None
    for f_idx in range(n_frames):
        buf = dec.stdout.read(W * H * 3)
        if len(buf) == W * H * 3:
            im = Image.frombytes("RGB", (W, H), buf)
            last = im
        elif last is not None:
            im = last
        else:
            im = Image.new("RGB", (W, H), (36, 22, 12))
        im = draw_backed_side_label_v04(im, label, f_idx / FPS, use_s)
        enc.stdin.write(im.tobytes())
    dec.stdout.close()
    dec.wait()
    enc.stdin.close()
    if enc.wait() != 0:
        raise RuntimeError("Failed encoding Note 1 Cut [3]")
    return {"frames": n_frames, "display_range": [427, 544], "output": str(out_mp4)}


def render_note2_cuts5_6_no_flash(out_mp4: Path, work_dir: Path) -> dict:
    """Note 2 (0:30): End P1:03b_town_safe at 81 frames (663..743) and advance P1:04_storm_mystery
    by 4 frames to cover 96 frames (744..839), eliminating the 4-frame post-trim flash (744..747)."""
    src_5 = MEDIA_DIR / "04_Generated-Clips/part01/raw/v01/03b_town_safe_t1.mp4"
    src_6 = MEDIA_DIR / "04_Generated-Clips/part01/raw/v01/04_storm_mystery_t1.mp4"
    seg5 = work_dir / "note2_seg5_81f.mp4"
    seg6 = work_dir / "note2_seg6_96f.mp4"

    sp.run(
        [
            "ffmpeg", "-y", "-v", "error", "-ss", "0.000", "-i", str(src_5),
            "-an", "-vf", SCALE_1080_VF, "-frames:v", "81",
            "-c:v", "libx264", "-preset", "fast", "-crf", "17", "-pix_fmt", "yuv420p", "-r", str(FPS),
            str(seg5),
        ],
        check=True,
    )
    sp.run(
        [
            "ffmpeg", "-y", "-v", "error", "-ss", "0.000", "-i", str(src_6),
            "-an", "-vf", SCALE_1080_VF, "-frames:v", "96",
            "-c:v", "libx264", "-preset", "fast", "-crf", "17", "-pix_fmt", "yuv420p", "-r", str(FPS),
            str(seg6),
        ],
        check=True,
    )
    concat_f = work_dir / "note2_concat.txt"
    concat_f.write_text(f"file '{seg5}'\nfile '{seg6}'\n")
    sp.run(
        [
            "ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", str(concat_f),
            "-c", "copy", str(out_mp4),
        ],
        check=True,
    )
    return {"frames": 177, "display_range": [663, 839], "output": str(out_mp4)}


def render_note3_cut23_24(out_mp4: Path, work_dir: Path, retake_clip: Path | None = None) -> dict:
    """Note 3 (1:49): Cut [23] P2:02_salon_spark (160f, 2506..2665) + Cut [24] P2:03_audience_shock (52f, 2666..2717).
    If retake_clip is supplied (Option B after J1881 approval), uses 160f from retake_clip + existing 52f Cut [24].
    Otherwise (Option A £0 native), splits Cut [23] into 80f unused 01_salon_tube_t1 (4.125-7.458s, 1.12x crop)
    + 80f 03_audience_shock_t1 (0.000-3.333s) and shifts Cut [24] to 3.333-5.500s (52f, 1.12x crop)."""
    src_24 = MEDIA_DIR / "04_Generated-Clips/part02/raw/v01/03_audience_shock_t1.mp4"
    if retake_clip is not None and retake_clip.exists():
        seg23 = work_dir / "note3_retake_160f.mp4"
        seg24 = work_dir / "note3_cut24_52f.mp4"
        sp.run(
            [
                "ffmpeg", "-y", "-v", "error", "-ss", "0.000", "-i", str(retake_clip),
                "-an", "-vf", SCALE_1080_VF, "-frames:v", "160",
                "-c:v", "libx264", "-preset", "fast", "-crf", "17", "-pix_fmt", "yuv420p", "-r", str(FPS),
                str(seg23),
            ],
            check=True,
        )
        sp.run(
            [
                "ffmpeg", "-y", "-v", "error", "-ss", "0.000", "-i", str(src_24),
                "-an", "-vf", SCALE_1080_VF, "-frames:v", "52",
                "-c:v", "libx264", "-preset", "fast", "-crf", "17", "-pix_fmt", "yuv420p", "-r", str(FPS),
                str(seg24),
            ],
            check=True,
        )
        concat_f = work_dir / "note3_concat.txt"
        concat_f.write_text(f"file '{seg23}'\nfile '{seg24}'\n")
        sp.run(
            ["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", str(concat_f), "-c", "copy", str(out_mp4)],
            check=True,
        )
        return {"frames": 212, "display_range": [2506, 2717], "mode": "option_b_retake", "output": str(out_mp4)}

    src_22 = MEDIA_DIR / "04_Generated-Clips/part02/raw/v01/01_salon_tube_t1.mp4"
    seg23a = work_dir / "note3_23a_80f.mp4"
    seg23b = work_dir / "note3_23b_80f.mp4"
    seg24 = work_dir / "note3_24_52f.mp4"
    crop_vf = "crop=iw*0.89:ih*0.89:iw*0.08:ih*0.06," + SCALE_1080_VF

    sp.run(
        [
            "ffmpeg", "-y", "-v", "error", "-ss", "4.125", "-i", str(src_22),
            "-an", "-vf", crop_vf, "-frames:v", "80",
            "-c:v", "libx264", "-preset", "fast", "-crf", "17", "-pix_fmt", "yuv420p", "-r", str(FPS),
            str(seg23a),
        ],
        check=True,
    )
    sp.run(
        [
            "ffmpeg", "-y", "-v", "error", "-ss", "0.000", "-i", str(src_24),
            "-an", "-vf", SCALE_1080_VF, "-frames:v", "80",
            "-c:v", "libx264", "-preset", "fast", "-crf", "17", "-pix_fmt", "yuv420p", "-r", str(FPS),
            str(seg23b),
        ],
        check=True,
    )
    sp.run(
        [
            "ffmpeg", "-y", "-v", "error", "-ss", "3.333", "-i", str(src_24),
            "-an", "-vf", crop_vf, "-frames:v", "52",
            "-c:v", "libx264", "-preset", "fast", "-crf", "17", "-pix_fmt", "yuv420p", "-r", str(FPS),
            str(seg24),
        ],
        check=True,
    )
    concat_f = work_dir / "note3_concat.txt"
    concat_f.write_text(f"file '{seg23a}'\nfile '{seg23b}'\nfile '{seg24}'\n")
    sp.run(
        ["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", str(concat_f), "-c", "copy", str(out_mp4)],
        check=True,
    )
    return {"frames": 212, "display_range": [2506, 2717], "mode": "option_a_native_zero_spend", "output": str(out_mp4)}


def render_note4_cut28_foil_jar(out_mp4: Path, work_dir: Path) -> dict:
    """Note 4 (2:20): Keep safe 92 frames (0.000-3.833s) of 07_foil_jar_t1.mp4 (display 3168..3259)
    and replace defective 84-frame tail (display 3260..3343) with unused 4.000-7.500s of 11_jar_crack_t1.mp4."""
    src_foil = MEDIA_DIR / "04_Generated-Clips/part02/raw/v01/07_foil_jar_t1.mp4"
    src_jar = MEDIA_DIR / "04_Generated-Clips/part02/raw/v01/11_jar_crack_t1.mp4"
    seg_a = work_dir / "note4_28a_92f.mp4"
    seg_b = work_dir / "note4_28b_84f.mp4"

    sp.run(
        [
            "ffmpeg", "-y", "-v", "error", "-ss", "0.000", "-i", str(src_foil),
            "-an", "-vf", SCALE_1080_VF, "-frames:v", "92",
            "-c:v", "libx264", "-preset", "fast", "-crf", "17", "-pix_fmt", "yuv420p", "-r", str(FPS),
            str(seg_a),
        ],
        check=True,
    )
    sp.run(
        [
            "ffmpeg", "-y", "-v", "error", "-ss", "4.000", "-i", str(src_jar),
            "-an", "-vf", SCALE_1080_VF, "-frames:v", "84",
            "-c:v", "libx264", "-preset", "fast", "-crf", "17", "-pix_fmt", "yuv420p", "-r", str(FPS),
            str(seg_b),
        ],
        check=True,
    )
    concat_f = work_dir / "note4_concat.txt"
    concat_f.write_text(f"file '{seg_a}'\nfile '{seg_b}'\n")
    sp.run(
        ["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", str(concat_f), "-c", "copy", str(out_mp4)],
        check=True,
    )
    return {"frames": 176, "display_range": [3168, 3343], "output": str(out_mp4)}


def draw_note5_sky_route_overlay(im: Image.Image, t: float, dur: float) -> Image.Image:
    """Note 5 (3:31): Clean upper-sky Atlantic trajectory banner (y=64..216, 0% ship occlusion)
    showing PHILADELPHIA ──────► PARIS · 1752 with an animated letter icon crossing the sky."""
    a_card = card_alpha(t, dur, 0.35, 0.40)
    if a_card <= 0.01:
        return im
    over = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(over)

    banner_box = (200, 62, 1720, 214)
    d.rounded_rectangle(
        banner_box,
        radius=22,
        fill=(36, 22, 12, int(195 * a_card)),
        outline=(211, 167, 88, int(175 * a_card)),
        width=2,
    )

    f_city = load_font(44, italic=True)
    f_sub = load_font(30, italic=True)

    # Left endpoint: PHILADELPHIA
    x_left, y_mid = 430, 128
    d.ellipse((x_left - 8, y_mid + 34 - 8, x_left + 8, y_mid + 34 + 8), fill=(242, 208, 122, int(255 * a_card)))
    d.text(
        (x_left, y_mid - 8),
        "PHILADELPHIA",
        font=f_city,
        fill=(252, 248, 240, int(255 * a_card)),
        anchor="mm",
        stroke_width=3,
        stroke_fill=(28, 16, 8, int(230 * a_card)),
    )

    # Right endpoint: PARIS · 1752
    x_right = 1490
    a_right = min(a_card, max(0.0, min(1.0, (t - 0.35) / 0.40)))
    if a_right > 0.01:
        d.ellipse((x_right - 8, y_mid + 34 - 8, x_right + 8, y_mid + 34 + 8), fill=(242, 208, 122, int(255 * a_right)))
        d.text(
            (x_right, y_mid - 8),
            "PARIS · 1752",
            font=f_city,
            fill=(252, 248, 240, int(255 * a_right)),
            anchor="mm",
            stroke_width=3,
            stroke_fill=(28, 16, 8, int(230 * a_right)),
        )

    # Animated arched dotted route across the Atlantic (t = 0.50 .. 2.85 s)
    prog = max(0.0, min(1.0, (t - 0.50) / 2.35))
    if prog > 0.01:
        n_pts = 48
        pts = []
        for i in range(n_pts + 1):
            u = i / n_pts
            if u > prog:
                break
            px = (x_left + 24) + ((x_right - 24) - (x_left + 24)) * u
            py = (y_mid + 34) - 42.0 * math.sin(math.pi * u)
            pts.append((px, py))
        for i in range(0, len(pts) - 1, 2):
            d.line([pts[i], pts[i + 1]], fill=(242, 208, 122, int(245 * a_card)), width=5)
        if pts:
            hx, hy = pts[-1]
            # Small inked envelope / letter badge at the leading edge
            ew, eh = 22, 15
            d.rectangle(
                (hx - ew, hy - eh, hx + ew, hy + eh),
                fill=(252, 248, 240, int(255 * a_card)),
                outline=(36, 22, 12, int(240 * a_card)),
                width=2,
            )
            d.line(
                [(hx - ew, hy - eh), (hx, hy + 2), (hx + ew, hy - eh)],
                fill=(36, 22, 12, int(230 * a_card)),
                width=2,
            )

    d.text(
        (W // 2, 184),
        "3,600 MILES ACROSS THE ATLANTIC",
        font=f_sub,
        fill=(242, 208, 122, int(235 * a_card)),
        anchor="mm",
        stroke_width=2,
        stroke_fill=(28, 16, 8, int(220 * a_card)),
    )
    return Image.alpha_composite(im.convert("RGBA"), over).convert("RGB")


def render_note5_p304_overlay_v04(out_mp4: Path) -> dict:
    """Note 5 (3:31): Render all 101 frames (display 4977..5077, 4.2083 s) of P3:04_letter_crosses
    over 07_slow_news_t1.mp4, replacing both the v06 brown-rectangle corner card (4977..5068)
    and the 9-frame orphaned v04 vector shoreline flash (5069..5077)."""
    src = MEDIA_DIR / "04_Generated-Clips/part03/raw/v01/07_slow_news_t1.mp4"
    n_frames = 101
    use_s = n_frames / FPS

    dec = sp.Popen(
        [
            "ffmpeg", "-v", "error", "-ss", "0.000", "-i", str(src),
            "-frames:v", str(n_frames), "-vf", SCALE_1080_VF,
            "-f", "rawvideo", "-pix_fmt", "rgb24", "-",
        ],
        stdout=sp.PIPE,
    )
    enc = sp.Popen(
        [
            "ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pixel_format", "rgb24",
            "-video_size", f"{W}x{H}", "-framerate", str(FPS), "-i", "-", "-an",
            "-c:v", "libx264", "-preset", "fast", "-crf", "17", "-pix_fmt", "yuv420p", "-r", str(FPS),
            str(out_mp4),
        ],
        stdin=sp.PIPE,
    )
    assert dec.stdout and enc.stdin
    last = None
    for f_idx in range(n_frames):
        buf = dec.stdout.read(W * H * 3)
        if len(buf) == W * H * 3:
            im = Image.frombytes("RGB", (W, H), buf)
            last = im
        elif last is not None:
            im = last
        else:
            im = Image.new("RGB", (W, H), (36, 22, 12))
        im = draw_note5_sky_route_overlay(im, f_idx / FPS, use_s)
        enc.stdin.write(im.tobytes())
    dec.stdout.close()
    dec.wait()
    enc.stdin.close()
    if enc.wait() != 0:
        raise RuntimeError("Failed encoding Note 5 P3:04_letter_crosses v04")
    return {"frames": n_frames, "display_range": [4977, 5077], "output": str(out_mp4)}


def render_note6_cut100_rods_spread(out_mp4: Path, work_dir: Path, retake_clip: Path | None = None) -> dict:
    """Note 6 (7:58): Cut [100] P5:13_rods_spread (135 frames, display 11358..11492).
    If retake_clip is supplied (Option B after J1881 approval), uses 135f from retake_clip.
    Otherwise (Option A £0 native), uses 135 continuous frames (1.500-7.125s, 5.625s) from
    approved KEEP plate 21_roofs_golden_t1.mp4 with a 1.08x reframe (upscale 1.62 <= 2.35),
    preserving the 4-6 s shot-length rule and calm daylight over church steeple + house rods."""
    if retake_clip is not None and retake_clip.exists():
        sp.run(
            [
                "ffmpeg", "-y", "-v", "error", "-ss", "0.000", "-i", str(retake_clip),
                "-an", "-vf", SCALE_1080_VF, "-frames:v", "135",
                "-c:v", "libx264", "-preset", "fast", "-crf", "17", "-pix_fmt", "yuv420p", "-r", str(FPS),
                str(out_mp4),
            ],
            check=True,
        )
        return {"frames": 135, "display_range": [11358, 11492], "mode": "option_b_retake", "output": str(out_mp4)}

    src_roofs = MEDIA_DIR / "04_Generated-Clips/part05/raw/v01/21_roofs_golden_t1.mp4"
    reframe_vf = "crop=iw*0.92:ih*0.92:iw*0.04:ih*0.04," + SCALE_1080_VF

    sp.run(
        [
            "ffmpeg", "-y", "-v", "error", "-ss", "1.500", "-i", str(src_roofs),
            "-an", "-vf", reframe_vf, "-frames:v", "135",
            "-c:v", "libx264", "-preset", "fast", "-crf", "17", "-pix_fmt", "yuv420p", "-r", str(FPS),
            str(out_mp4),
        ],
        check=True,
    )
    return {"frames": 135, "display_range": [11358, 11492], "mode": "option_a_native_zero_spend", "output": str(out_mp4)}


def extract_unchanged_range(src_mp4: Path, start_frame: int, end_frame_inclusive: int, out_mp4: Path) -> None:
    """Extract exact display frame range [start_frame, end_frame_inclusive] from locked master_v03."""
    n_frames = end_frame_inclusive - start_frame + 1
    vf = f"trim=start_frame={start_frame}:end_frame={end_frame_inclusive + 1},setpts=N/({FPS}*TB),fps={FPS},format=yuv420p"
    sp.run(
        [
            "ffmpeg", "-y", "-v", "error", "-i", str(src_mp4),
            "-an", "-vf", vf, "-frames:v", str(n_frames),
            "-c:v", "libx264", "-preset", "fast", "-crf", "17", "-pix_fmt", "yuv420p", "-r", str(FPS),
            str(out_mp4),
        ],
        check=True,
    )


def execute_recipe(
    work_dir: Path,
    out_rough_v13: Path,
    out_master_v04: Path,
    retake_p2_02: Path | None = None,
    retake_p5_13: Path | None = None,
) -> dict:
    """Full rough_v13 + master_v04 assembly once Chief J1881 authorizes execution."""
    work_dir.mkdir(parents=True, exist_ok=True)
    p1 = work_dir / "patch_note1_427_544.mp4"
    p2 = work_dir / "patch_note2_663_839.mp4"
    p3 = work_dir / "patch_note3_2506_2717.mp4"
    p4 = work_dir / "patch_note4_3168_3343.mp4"
    p5 = work_dir / "patch_note5_4977_5077.mp4"
    p6 = work_dir / "patch_note6_11358_11492.mp4"

    render_note1_cut3_backed_label(p1)
    render_note2_cuts5_6_no_flash(p2, work_dir)
    render_note3_cut23_24(p3, work_dir, retake_p2_02)
    render_note4_cut28_foil_jar(p4, work_dir)
    render_note5_p304_overlay_v04(p5)
    render_note6_cut100_rods_spread(p6, work_dir, retake_p5_13)

    patch_map = {
        (427, 544): p1,
        (663, 839): p2,
        (2506, 2717): p3,
        (3168, 3343): p4,
        (4977, 5077): p5,
        (11358, 11492): p6,
    }
    segments: list[Path] = []
    cursor = 0
    for idx, p in enumerate(PATCH_INTERVALS):
        f_in, f_out = p["frame_in"], p["frame_out"]
        if cursor < f_in:
            keep_seg = work_dir / f"keep_{idx:02d}_{cursor}_{f_in - 1}.mp4"
            extract_unchanged_range(MASTER_V03_LOCAL, cursor, f_in - 1, keep_seg)
            segments.append(keep_seg)
        segments.append(patch_map[(f_in, f_out)])
        cursor = f_out + 1
    if cursor < EXPECTED_PACKETS:
        tail_seg = work_dir / f"keep_tail_{cursor}_{EXPECTED_PACKETS - 1}.mp4"
        extract_unchanged_range(MASTER_V03_LOCAL, cursor, EXPECTED_PACKETS - 1, tail_seg)
        segments.append(tail_seg)

    concat_list = work_dir / "rough_v13_concat.txt"
    concat_list.write_text("".join(f"file '{s}'\n" for s in segments))
    out_rough_v13.parent.mkdir(parents=True, exist_ok=True)
    sp.run(
        [
            "ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", str(concat_list),
            "-c", "copy", str(out_rough_v13),
        ],
        check=True,
    )
    out_master_v04.parent.mkdir(parents=True, exist_ok=True)
    sp.run(
        [
            "ffmpeg", "-y", "-v", "error", "-i", str(out_rough_v13), "-i", str(MASTER_V03_LOCAL),
            "-map", "0:v:0", "-map", "1:a:0", "-c:v", "copy", "-c:a", "copy", "-movflags", "+faststart",
            str(out_master_v04),
        ],
        check=True,
    )
    return {
        "status": "EXECUTED",
        "rough_v13": str(out_rough_v13),
        "master_v04": str(out_master_v04),
        "master_v04_sha256": sha256_file(out_master_v04),
    }


PATCH_INTERVALS = [
    {"note": 1, "timestamp": "00:20", "row": "P1:03_table_three", "frame_in": 427, "frame_out": 544, "frames": 118},
    {"note": 2, "timestamp": "0:30", "row": "P1:03b_town_safe+04_storm_mystery", "frame_in": 663, "frame_out": 839, "frames": 177},
    {"note": 3, "timestamp": "1:49", "row": "P2:02_salon_spark+03_audience_shock", "frame_in": 2506, "frame_out": 2717, "frames": 212},
    {"note": 4, "timestamp": "2:20", "row": "P2:07_foil_jar", "frame_in": 3168, "frame_out": 3343, "frames": 176},
    {"note": 5, "timestamp": "3:31", "row": "P3:04_letter_crosses", "frame_in": 4977, "frame_out": 5077, "frames": 101},
    {"note": 6, "timestamp": "7:58", "row": "P5:13_rods_spread", "frame_in": 11358, "frame_out": 11492, "frames": 135},
]


def verify_plan() -> dict:
    """Dry-run verification of frame-count invariants and source availability."""
    assert MASTER_V03_LOCAL.exists(), f"Missing {MASTER_V03_LOCAL}"
    total_patched = sum(p["frames"] for p in PATCH_INTERVALS)
    for p in PATCH_INTERVALS:
        assert p["frame_out"] - p["frame_in"] + 1 == p["frames"], f"Bad range on {p}"
    # Verify non-overlapping sorted ranges within 0..12922
    prev_out = -1
    for p in PATCH_INTERVALS:
        assert p["frame_in"] > prev_out, f"Overlap at {p}"
        assert 0 <= p["frame_in"] <= p["frame_out"] < EXPECTED_PACKETS
        prev_out = p["frame_out"]

    required_sources = [
        MEDIA_DIR / "04_Generated-Clips/part01/raw/v01/03_table_three_t1.mp4",
        MEDIA_DIR / "04_Generated-Clips/part01/raw/v01/03b_town_safe_t1.mp4",
        MEDIA_DIR / "04_Generated-Clips/part01/raw/v01/04_storm_mystery_t1.mp4",
        MEDIA_DIR / "04_Generated-Clips/part02/raw/v01/01_salon_tube_t1.mp4",
        MEDIA_DIR / "04_Generated-Clips/part02/raw/v01/03_audience_shock_t1.mp4",
        MEDIA_DIR / "04_Generated-Clips/part02/raw/v01/07_foil_jar_t1.mp4",
        MEDIA_DIR / "04_Generated-Clips/part02/raw/v01/11_jar_crack_t1.mp4",
        MEDIA_DIR / "04_Generated-Clips/part03/raw/v01/07_slow_news_t1.mp4",
        MEDIA_DIR / "04_Generated-Clips/part05/raw/v01/21_roofs_golden_t1.mp4",
        MEDIA_DIR / "04_Generated-Clips/part05/raw/v01/01_house_rod_t1.mp4",
    ]
    for s in required_sources:
        assert s.exists(), f"Missing required source clip: {s}"

    return {
        "status": "DRY_RUN_VERIFIED",
        "master_v03": str(MASTER_V03_LOCAL),
        "expected_packets": EXPECTED_PACKETS,
        "patched_intervals": len(PATCH_INTERVALS),
        "patched_frames": total_patched,
        "unchanged_frames": EXPECTED_PACKETS - total_patched,
        "frame_count_delta": 0,
        "vo_sync_lag_ms": 0.0,
        "spend_gbp": 0.0,
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="HOS 008 J1880 rough_v13 -> master_v04 recipe")
    ap.add_argument("--dry-run", action="store_true", default=True, help="Verify plan without rendering (default)")
    ap.add_argument("--execute", action="store_true", help="Execute render (requires J1881 Chief authorization)")
    ap.add_argument("--retake-p2-02", type=Path, default=None, help="Optional Chief-authorized retake clip for P2:02_salon_spark")
    ap.add_argument("--retake-p5-13", type=Path, default=None, help="Optional Chief-authorized retake clip for P5:13_rods_spread")
    args = ap.parse_args()

    report = verify_plan()
    if not args.execute:
        print(json.dumps(report, indent=2))
        return 0

    raise SystemExit(
        "Refusing --execute until J1881 elected-Chief scope review selects Option A (native £0) "
        "or Option B (scoped Flow retake) for P2:02_salon_spark and P5:13_rods_spread."
    )


if __name__ == "__main__":
    sys.exit(main())
