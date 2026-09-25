#!/usr/bin/env python3
"""Local Part 02 scenery — period desks, opaque jars, ZERO fire. Ken Burns 8s."""
from __future__ import annotations

import random
import subprocess
import time
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter

PROJ = Path(__file__).resolve().parents[1]
EDIT = Path(__file__).resolve().parent
OUT_RAW = PROJ / "04_Generated-Clips/part02/raw/v01_fast"
STILLS = EDIT / "_qa_part02_v03/scenery_stills"
REJECT = PROJ / "04_Generated-Clips/part02/raw/_rejected_v03_flow_fire"
W, H = 1280, 720
FPS = 24
DUR_S = 8.0

# Match disk / assemble plate ids. Cards 01 + 04 stay elsewhere.
SCENES = [
    "02_lavoisier_list",
    "03_not_a_map",
    "05_explorer_triad_break",
    "06_rhymes_run_out",
    "07_newlands_octave",
    "08_piano_gag_fail",
    "09_almost_right",
    "10_ruler_crooked",
    "11_shared_stick",
]


def wood_desk(seed: int) -> Image.Image:
    rnd = random.Random(seed)
    img = Image.new("RGB", (W, H), (48, 32, 22))
    px = img.load()
    desk_line = int(H * 0.42)
    for y in range(H):
        for x in range(W):
            if y > desk_line:
                band = (y // 28) % 2
                base = 62 + band * 10 + (x // 90) % 3
                n = rnd.randint(-8, 8)
                r = max(0, min(255, base + 18 + n))
                g = max(0, min(255, base + 2 + n // 2))
                b = max(0, min(255, base - 10 + n // 3))
            else:
                band = (y // 36) % 2
                base = 36 + band * 6
                n = rnd.randint(-5, 5)
                r = max(0, min(255, base + 8 + n))
                g = max(0, min(255, base - 2 + n // 2))
                b = max(0, min(255, base - 10 + n // 3))
            px[x, y] = (r, g, b)
    light = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ld = ImageDraw.Draw(light)
    for i in range(18):
        a = max(0, 10 - i // 2)
        ld.polygon(
            [(0, 40 + i * 8), (420 - i * 10, 0), (520 - i * 8, 0), (0, 220 + i * 12)],
            fill=(255, 220, 160, a),
        )
    return Image.alpha_composite(img.convert("RGBA"), light).convert("RGB")


def draw_jar(draw, x, y, w, h, color):
    draw.rounded_rectangle(
        [x, y, x + w, y + h],
        radius=max(4, w // 8),
        fill=color,
        outline=(40, 28, 18),
        width=2,
    )
    lid = (max(0, color[0] - 15), max(0, color[1] - 12), max(0, color[2] - 10))
    draw.ellipse([x + 2, y - 8, x + w - 2, y + 10], fill=lid, outline=(40, 28, 18))


def draw_card(draw, x, y, w, h, tilt=0):
    pts = [(x, y), (x + w, y + tilt), (x + w, y + h + tilt), (x, y + h)]
    draw.polygon(pts, fill=(236, 220, 185), outline=(90, 60, 35))
    inset = 6
    draw.polygon(
        [
            (x + inset, y + inset),
            (x + w - inset, y + inset + tilt),
            (x + w - inset, y + h - inset + tilt),
            (x + inset, y + h - inset),
        ],
        outline=(120, 85, 50),
    )


def draw_ruler(draw, x, y, length, crooked=False):
    hh = 18
    fill = (190, 150, 90)
    outline = (70, 45, 25)
    if crooked:
        mid = length // 2
        draw.polygon(
            [(x, y), (x + mid, y - 10), (x + mid, y - 10 + hh), (x, y + hh)],
            fill=fill,
            outline=outline,
        )
        draw.polygon(
            [
                (x + mid, y - 10),
                (x + length, y + 8),
                (x + length, y + 8 + hh),
                (x + mid, y - 10 + hh),
            ],
            fill=fill,
            outline=outline,
        )
    else:
        draw.rounded_rectangle(
            [x, y, x + length, y + hh], radius=3, fill=fill, outline=outline
        )



def draw_candle(draw, x, y, lit=True):
    # stick + optional small wick flame (jars never lit)
    draw.rectangle([x, y - 70, x + 14, y], fill=(150, 110, 60), outline=(60, 40, 20))
    draw.ellipse([x - 10, y - 78, x + 24, y - 64], fill=(150, 110, 60), outline=(60, 40, 20))
    if lit:
        draw.ellipse([x + 1, y - 100, x + 13, y - 78], fill=(255, 200, 80))
        draw.ellipse([x + 4, y - 96, x + 10, y - 82], fill=(255, 245, 200))

def draw_piano(draw, x, y, n=8):
    for i in range(n):
        kx = x + i * 22
        draw.rectangle([kx, y, kx + 20, y + 70], fill=(245, 240, 230), outline=(50, 40, 30))
        if i % 2 == 1 and i < n - 1:
            draw.rectangle([kx + 14, y, kx + 26, y + 42], fill=(30, 24, 20))


def render_scene(pid: str, seed: int) -> Image.Image:
    rnd = random.Random(seed)
    img = wood_desk(seed)
    draw = ImageDraw.Draw(img)
    desk_y = int(H * 0.55)

    if pid == "02_lavoisier_list":
        for i in range(6):
            draw_card(draw, 90 + i * 70, desk_y - 20, 55, 80, tilt=rnd.randint(-2, 2))
        colors = [(210, 185, 150), (180, 160, 140), (200, 175, 145), (160, 140, 125)]
        for i, c in enumerate(colors):
            draw_jar(draw, 520 + i * 95, desk_y - 110 - (i % 2) * 20, 70, 130 + (i % 3) * 10, c)
        draw_candle(draw, 1100, desk_y, lit=True)

    elif pid == "03_not_a_map":
        for x, y, t in [
            (180, desk_y - 10, 8),
            (250, desk_y - 40, -6),
            (320, desk_y + 5, 12),
            (400, desk_y - 25, -10),
            (470, desk_y - 5, 4),
            (540, desk_y - 50, 15),
            (610, desk_y - 15, -8),
            (700, desk_y - 35, 6),
        ]:
            draw_card(draw, x, y, 60, 85, tilt=t)
        draw_jar(draw, 980, desk_y - 140, 80, 150, (195, 170, 140))
        draw_jar(draw, 1080, desk_y - 120, 70, 130, (170, 150, 130))
        draw_candle(draw, 80, desk_y, lit=True)

    elif pid == "05_explorer_triad_break":
        for i in range(3):
            draw_card(draw, 340 + i * 120, desk_y - 30, 90, 120, tilt=0)
        draw_card(draw, 720, desk_y - 70, 90, 120, tilt=18)
        draw_jar(draw, 120, desk_y - 130, 75, 140, (185, 165, 140))

    elif pid == "06_rhymes_run_out":
        for row, yy in enumerate([120, 260, 400]):
            for i in range(8):
                c = (170 + (i * 11) % 40, 150 + (row * 8), 125 + i * 3)
                draw_jar(draw, 80 + i * 140, yy, 70 + (i % 3) * 8, 100 + (row % 2) * 20, c)
        for i in range(10):
            draw_card(draw, 100 + i * 100, desk_y - 10 + (i % 3) * 8, 50, 70, tilt=rnd.randint(-8, 8))

    elif pid == "07_newlands_octave":
        for i in range(10):
            draw_card(draw, 60 + i * 85, desk_y - 25, 55, 80, tilt=0)
        draw_piano(draw, 980, desk_y - 80, n=7)
        draw_jar(draw, 880, desk_y - 130, 65, 120, (175, 155, 135))

    elif pid == "08_piano_gag_fail":
        draw_piano(draw, 200, desk_y - 40, n=9)
        for i in range(6):
            draw_card(
                draw,
                450 + i * 90,
                desk_y - 5 + rnd.randint(0, 30),
                55,
                75,
                tilt=rnd.randint(-20, 20),
            )
        draw_jar(draw, 1050, desk_y - 125, 70, 130, (190, 170, 145))

    elif pid == "09_almost_right":
        for i in range(7):
            gap = 30 if i == 4 else 0
            draw_card(draw, 160 + i * 110 + gap, desk_y - 30, 70, 100, tilt=rnd.randint(-1, 1))
        draw_jar(draw, 1080, desk_y - 135, 75, 140, (180, 160, 140))

    elif pid == "10_ruler_crooked":
        draw_ruler(draw, 220, desk_y - 10, 700, crooked=True)
        for i in range(5):
            draw_card(draw, 200 + i * 140, desk_y - 90, 60, 85, tilt=rnd.randint(-5, 5))
        draw_jar(draw, 1000, desk_y - 130, 80, 140, (195, 175, 150))

    elif pid == "11_shared_stick":
        for i in range(5):
            draw_ruler(draw, 180 + i * 30, desk_y - 40 + i * 18, 520, crooked=False)
        draw_jar(draw, 90, desk_y - 120, 70, 130, (175, 155, 135))
        draw_jar(draw, 1100, desk_y - 120, 70, 130, (175, 155, 135))

    return img.filter(ImageFilter.SMOOTH_MORE)


def still_to_mp4(still: Path, dest: Path, seed: int) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    frames = int(DUR_S * FPS)
    dx = 40 if seed % 2 == 0 else -30
    dy = 20 if seed % 3 else -15
    vf = (
        f"scale={W * 12 // 10}:{H * 12 // 10},"
        f"zoompan=z='min(1.08,1+0.08*on/{frames})':"
        f"x='iw/2-(iw/zoom/2)+{dx}*on/{frames}':"
        f"y='ih/2-(ih/zoom/2)+{dy}*on/{frames}':"
        f"d={frames}:s={W}x{H}:fps={FPS},"
        f"eq=brightness='0.008*sin(2*PI*t/5)':saturation=1.04"
    )
    subprocess.run(
        [
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            "-loop", "1", "-i", str(still),
            "-vf", vf, "-t", f"{DUR_S}", "-r", str(FPS),
            "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18", "-preset", "medium",
            "-an", str(dest),
        ],
        check=True,
    )


def main() -> None:
    STILLS.mkdir(parents=True, exist_ok=True)
    OUT_RAW.mkdir(parents=True, exist_ok=True)
    REJECT.mkdir(parents=True, exist_ok=True)
    for i, pid in enumerate(SCENES):
        still = STILLS / f"{pid}.png"
        dest = OUT_RAW / f"{pid}_v01.mp4"
        if dest.exists() and dest.stat().st_size > 200_000:
            ts = time.strftime("%Y%m%d_%H%M%S")
            dest.rename(REJECT / f"{pid}_v01_pre_local_{ts}.mp4")
            print(f"archived old {pid}", flush=True)
        img = render_scene(pid, seed=20 + i)
        img.save(still)
        print(f"still {still.name}", flush=True)
        still_to_mp4(still, dest, seed=20 + i)
        dur = float(
            subprocess.check_output(
                [
                    "ffprobe", "-v", "error", "-show_entries", "format=duration",
                    "-of", "default=nw=1:nk=1", str(dest),
                ],
                text=True,
            ).strip()
        )
        size = dest.stat().st_size
        assert size >= 150_000 and 7.5 <= dur <= 8.5, (pid, size, dur)
        print(f"OK {dest.name} size={size} dur={dur:.2f}", flush=True)
    print("DONE local no-fire scenery", flush=True)


if __name__ == "__main__":
    main()
