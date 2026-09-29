#!/usr/bin/env python3
"""Rebuild S02 punch from part02 rough v06 — moving piano open for gate motion."""
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

VENV_PY = Path(
    "/Users/benjaminoats/YouTube/History Of Science/"
    "02_Video-Projects/001_How-Did-We-Discover-Germs/10_Shorts/_venv/bin/python"
)
if VENV_PY.exists() and Path(sys.executable) != VENV_PY:
    os.execv(str(VENV_PY), [str(VENV_PY), str(Path(__file__).resolve())])

from PIL import Image, ImageDraw, ImageFont  # noqa: E402

REPO = Path("/Users/benjaminoats/YouTube/History Of Science")
SHORTS = REPO / "02_Video-Projects/004_Whats-Really-Inside-An-Atom/10_Shorts"
ROUGH = (
    REPO
    / "02_Video-Projects/002_How-Did-We-Discover-The-Periodic-Table"
    / "09_Final-Export/hos_002_part02_rough_v06.mp4"
)
VO = SHORTS / "vo_v03/hos_004_s02_every_eighth_vo_v03.wav"
ICLOUD = Path.home() / (
    "Library/Mobile Documents/com~apple~CloudDocs/HOS UAT/"
    "004_Whats-Really-Inside-An-Atom/10_Shorts"
)
WORK = SHORTS / "_work_v03/s02_every_eighth_r2"
WORK.mkdir(parents=True, exist_ok=True)
OUT = SHORTS / "hos_004_s02_every_eighth_punch_v03.mp4"

W, H = 1080, 1920
FONT = "/System/Library/Fonts/Supplemental/Didot.ttc"
CTA = "/System/Library/Fonts/Supplemental/Times New Roman.ttf"
CREAM = (245, 232, 210, 255)
INK = (28, 26, 28, 255)
YEL = (255, 214, 70, 255)
VF = "scale=1920:1080,crop=608:1080:656:0,scale=1080:1920:flags=lanczos,setsar=1"


def probe(p: Path) -> float:
    return float(
        subprocess.check_output(
            [
                "ffprobe",
                "-v",
                "error",
                "-show_entries",
                "format=duration",
                "-of",
                "default=noprint_wrappers=1:nokey=1",
                str(p),
            ],
            text=True,
        ).strip()
    )


def ff(*a: str) -> None:
    subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", *a], check=True)


def wrap(text: str, font: ImageFont.FreeTypeFont, max_w: int) -> list[str]:
    words = text.split()
    lines: list[str] = []
    cur = ""
    for w in words:
        trial = (cur + " " + w).strip()
        if font.getlength(trial) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines or [text]


def render(path: Path, text: str, size: int, anchor: str, y: int, font_path=FONT, fill=CREAM) -> None:
    font = ImageFont.truetype(font_path, size)
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    lines = wrap(text, font, W - 96)
    heights = [font.getbbox(l)[3] - font.getbbox(l)[1] for l in lines]
    gap = int(size * 0.28)
    block = sum(heights) + gap * (len(lines) - 1)
    top = H - y - block if anchor == "bottom" else y
    cy = top
    stroke = 3
    for line, lh in zip(lines, heights):
        tw = font.getlength(line)
        x = (W - tw) / 2
        for dx in range(-stroke, stroke + 1):
            for dy in range(-stroke, stroke + 1):
                if dx or dy:
                    draw.text((x + dx, cy + dy), line, font=font, fill=INK)
        draw.text((x, cy), line, font=font, fill=fill)
        cy += lh + gap
    img.save(path)


def main() -> None:
    if not ROUGH.exists():
        raise SystemExit(f"missing {ROUGH}")
    if not VO.exists():
        raise SystemExit(f"missing {VO}")
    vo_dur = probe(VO)
    loop = 4.0
    story = vo_dur
    total = story + loop
    if total > 27:
        loop = max(3.5, 27 - story)
        total = story + loop

    # Open on piano xfade (motion spike ~60), then octave cards / desk beats
    wins = [(59.5, 7.5), (34.0, 7.0), (66.5, 7.0), (42.0, 6.0)]
    segs: list[Path] = []
    covered = 0.0
    i = 0
    while covered < story - 0.05:
        st, mx = wins[i % len(wins)]
        off = 0.6 * (i // len(wins))
        take = min(mx - off, story - covered)
        if take < 0.4:
            i += 1
            continue
        out = WORK / f"seg_{i:02d}.mp4"
        # First segment: slight speed-up so open motion clears the gate warn
        if i == 0:
            vf = f"{VF},setpts=0.55*PTS"
            # need more source time when speeding up
            src_t = min(take / 0.55 + 0.2, 8.0)
            ff(
                "-ss",
                f"{st:.3f}",
                "-t",
                f"{src_t:.3f}",
                "-i",
                str(ROUGH),
                "-vf",
                vf,
                "-an",
                "-c:v",
                "libx264",
                "-pix_fmt",
                "yuv420p",
                "-preset",
                "fast",
                "-crf",
                "18",
                "-r",
                "24",
                "-t",
                f"{take:.3f}",
                str(out),
            )
        else:
            ff(
                "-ss",
                f"{st + off:.3f}",
                "-t",
                f"{take:.3f}",
                "-i",
                str(ROUGH),
                "-vf",
                VF,
                "-an",
                "-c:v",
                "libx264",
                "-pix_fmt",
                "yuv420p",
                "-preset",
                "fast",
                "-crf",
                "18",
                "-r",
                "24",
                str(out),
            )
        segs.append(out)
        covered += take
        i += 1

    concat = WORK / "pic.txt"
    concat.write_text("".join(f"file '{s.name}'\n" for s in segs))
    pic = WORK / "picture.mp4"
    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-hide_banner",
            "-loglevel",
            "error",
            "-f",
            "concat",
            "-safe",
            "0",
            "-i",
            str(concat),
            "-c",
            "copy",
            str(pic),
        ],
        check=True,
        cwd=WORK,
    )
    pic_t = WORK / "picture_trim.mp4"
    ff(
        "-i",
        str(pic),
        "-t",
        f"{story:.3f}",
        "-c:v",
        "libx264",
        "-pix_fmt",
        "yuv420p",
        "-preset",
        "fast",
        "-crf",
        "18",
        "-r",
        "24",
        "-an",
        str(pic_t),
    )

    vo_fit = WORK / "vo_fit.wav"
    if vo_dur < story:
        ff(
            "-i",
            str(VO),
            "-af",
            f"apad=pad_dur={story - vo_dur:.3f}",
            "-t",
            f"{story:.3f}",
            "-ar",
            "48000",
            "-ac",
            "2",
            str(vo_fit),
        )
    else:
        ff("-i", str(VO), "-t", f"{story:.3f}", "-ar", "48000", "-ac", "2", str(vo_fit))

    story_av = WORK / "story_av.mp4"
    ff(
        "-i",
        str(pic_t),
        "-i",
        str(vo_fit),
        "-map",
        "0:v",
        "-map",
        "1:a",
        "-c:v",
        "copy",
        "-c:a",
        "aac",
        "-b:a",
        "192k",
        "-ar",
        "48000",
        "-ac",
        "2",
        "-shortest",
        str(story_av),
    )

    loop_mp4 = WORK / "loop.mp4"
    ff(
        "-ss",
        "59.5",
        "-t",
        f"{loop:.3f}",
        "-i",
        str(ROUGH),
        "-vf",
        VF,
        "-an",
        "-c:v",
        "libx264",
        "-pix_fmt",
        "yuv420p",
        "-preset",
        "fast",
        "-crf",
        "18",
        "-r",
        "24",
        str(loop_mp4),
    )
    loop_av = WORK / "loop_av.mp4"
    ff(
        "-i",
        str(loop_mp4),
        "-f",
        "lavfi",
        "-i",
        "anullsrc=r=48000:cl=stereo",
        "-shortest",
        "-c:v",
        "copy",
        "-c:a",
        "aac",
        "-b:a",
        "192k",
        str(loop_av),
    )

    raw = WORK / "raw.mp4"
    (WORK / "av.txt").write_text(f"file '{story_av.name}'\nfile '{loop_av.name}'\n")
    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-hide_banner",
            "-loglevel",
            "error",
            "-f",
            "concat",
            "-safe",
            "0",
            "-i",
            str(WORK / "av.txt"),
            "-c",
            "copy",
            str(raw),
        ],
        check=True,
        cwd=WORK,
    )

    hook = WORK / "cap_hook.png"
    line = WORK / "cap_line.png"
    title = WORK / "cap_title.png"
    cta = WORK / "cap_cta.png"
    render(hook, "EVERY EIGHTH?", 64, "top", 160, fill=YEL)
    render(
        line,
        "Before Mendeleev, John Newlands lined the elements up like notes on a piano.",
        44,
        "bottom",
        300,
    )
    render(title, "How Did We Discover the Periodic Table?", 34, "top", 220)
    render(cta, "watch the full film →", 40, "bottom", 240, font_path=CTA)
    cta_in = max(total - 4.0, 14.4)
    overlays = [
        (hook, 0.0, 3.2),
        (line, 0.2, cta_in - 0.1),
        (title, 9.0, 14.0),
        (cta, cta_in, total - 0.12),
    ]
    inputs: list[str] = ["-i", str(raw)]
    for png, _, _ in overlays:
        inputs += ["-loop", "1", "-i", str(png)]
    fc = []
    last = "[0:v]"
    for i, (_, t0, t1) in enumerate(overlays, 1):
        out = f"[v{i}]"
        fc.append(f"{last}[{i}:v]overlay=0:0:enable='between(t,{t0:.3f},{t1:.3f})'{out}")
        last = out
    ff(
        *inputs,
        "-filter_complex",
        ";".join(fc),
        "-map",
        last,
        "-map",
        "0:a",
        "-c:v",
        "libx264",
        "-pix_fmt",
        "yuv420p",
        "-preset",
        "fast",
        "-crf",
        "18",
        "-r",
        "24",
        "-c:a",
        "aac",
        "-b:a",
        "192k",
        "-t",
        f"{total:.3f}",
        "-movflags",
        "+faststart",
        str(OUT),
    )
    print(f"built {OUT} dur={probe(OUT):.2f}s", flush=True)
    ICLOUD.mkdir(parents=True, exist_ok=True)
    (ICLOUD / OUT.name).write_bytes(OUT.read_bytes())


if __name__ == "__main__":
    main()
