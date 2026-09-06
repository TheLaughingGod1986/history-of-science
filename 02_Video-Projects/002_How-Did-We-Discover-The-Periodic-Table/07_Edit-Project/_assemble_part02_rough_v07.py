#!/usr/bin/env python3
"""Assemble HOS 002 Part 02 rough v07 — all real Veo + Animistry side labels. No Ken Burns."""
from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

PROJ = Path(__file__).resolve().parents[1]
PLATES_JSON = PROJ / "07_Edit-Project/parts/part-02_plates_v04.json"
RAW = PROJ / "04_Generated-Clips/part02/raw/v07_fast"
LABEL_DIR = PROJ / "04_Generated-Clips/part02/refs/v07_side_labels"
VO = PROJ / "02_Voiceover/part02_first_patterns_v01.wav"
BED = PROJ / "05_Music/hos_002_part01_curious_workshop_v02_norm.wav"
OUT = PROJ / "09_Final-Export/hos_002_part02_rough_v07.mp4"
ICLOUD = Path.home() / "Library/Mobile Documents/com~apple~CloudDocs/HOS UAT"
CLIP_USE = 8.0
XFADE = 0.35
BED_VOL = 0.38

SIDE_LABELS = [
    (0.0, 3.5, "FIRST PATTERNS"),
    (8.0, 16.0, "SIMPLE SUBSTANCES"),
    (18.0, 28.0, "TRIADS"),
    (30.0, 40.0, "COUSIN RHYMES"),
    (42.0, 52.0, "OCTAVES"),
    (54.0, 64.0, "NOT A PIANO"),
    (66.0, 74.0, "ALMOST RIGHT"),
    (76.0, 84.0, "A SHARED STICK"),
]


def probe(path: Path) -> float:
    return float(subprocess.check_output([
        "ffprobe","-v","error","-show_entries","format=duration","-of","default=nw=1:nk=1",str(path)
    ], text=True).strip())


def file_sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def render_side_label(text: str, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    w, h = 640, 120
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((8, 8, w - 8, h - 8), radius=18, fill=(48, 30, 16, 210))
    d.rounded_rectangle((8, 8, w - 8, h - 8), radius=18, outline=(232, 214, 180, 230), width=3)
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Georgia Bold.ttf", 34)
    except OSError:
        font = ImageFont.load_default()
    bb = d.textbbox((0, 0), text, font=font)
    tw, th = bb[2] - bb[0], bb[3] - bb[1]
    d.text(((w - tw) / 2, (h - th) / 2 - 4), text, fill=(245, 232, 205, 255), font=font)
    im.save(dest)


def main() -> None:
    plates = json.loads(PLATES_JSON.read_text())["plates"]
    clips = []
    for plate in plates:
        pid = plate["id"]
        clip = RAW / f"{pid}_v07.mp4"
        if not clip.exists() or clip.stat().st_size < 400_000:
            raise SystemExit(f"missing real-motion plate {clip} — run _mint_part02_flow_remint_v07.py first")
        d = probe(clip)
        if d < 5.5:
            raise SystemExit(f"short plate {clip} d={d}")
        clips.append(clip)
        print(f"  {pid}: {d:.2f}s", flush=True)

    vo_dur = probe(VO)
    pic_dur = len(clips) * CLIP_USE - (len(clips) - 1) * XFADE
    if pic_dur + 0.05 < vo_dur:
        raise SystemExit(f"picture {pic_dur:.2f} < VO {vo_dur:.2f}")

    LABEL_DIR.mkdir(parents=True, exist_ok=True)
    label_pngs = []
    for i, (a, b, text) in enumerate(SIDE_LABELS):
        png = LABEL_DIR / f"label_{i:02d}.png"
        render_side_label(text, png)
        label_pngs.append((a, min(b, vo_dur), png))

    OUT.parent.mkdir(parents=True, exist_ok=True)
    n = len(clips)
    inputs = []
    for c in clips:
        inputs += ["-i", str(c)]
    inputs += ["-i", str(VO), "-i", str(BED)]
    label_input_start = n + 2
    for _, _, png in label_pngs:
        inputs += ["-loop", "1", "-t", "1", "-i", str(png)]

    parts = []
    for i in range(n):
        parts.append(
            f"[{i}:v]trim=0:{CLIP_USE},setpts=PTS-STARTPTS,"
            f"scale=1920:1080:force_original_aspect_ratio=decrease,"
            f"pad=1920:1080:(ow-iw)/2:(oh-ih)/2,fps=24,format=yuv420p[v{i}]"
        )
    vlabel = "[v0]"
    for i in range(1, n):
        out = f"[vx{i}]"
        offset = (CLIP_USE - XFADE) * i
        parts.append(f"{vlabel}[v{i}]xfade=transition=fade:duration={XFADE}:offset={offset:.3f}{out}")
        vlabel = out
    cur = vlabel
    for li, (a, b, _) in enumerate(label_pngs):
        idx = label_input_start + li
        nxt = f"[vl{li}]"
        parts.append(
            f"[{idx}:v]format=rgba,scale=640:-1[lg{li}];"
            f"{cur}[lg{li}]overlay=x=1920-660:y=48:enable='between(t,{a:.3f},{b:.3f})'{nxt}"
        )
        cur = nxt
    parts.append(f"[{n}:a]aformat=sample_rates=48000:channel_layouts=stereo,atrim=0:{vo_dur:.3f},asetpts=PTS-STARTPTS[vo]")
    parts.append(f"[{n+1}:a]aformat=sample_rates=48000:channel_layouts=stereo,atrim=0:{vo_dur:.3f},volume={BED_VOL}[bed]")
    parts.append("[vo][bed]amix=inputs=2:duration=first:dropout_transition=0[a]")

    subprocess.run([
        "ffmpeg","-y","-hide_banner","-loglevel","error", *inputs,
        "-filter_complex", ";".join(parts),
        "-map", cur, "-map", "[a]",
        "-c:v","libx264","-preset","medium","-crf","18",
        "-c:a","aac","-b:a","192k","-movflags","+faststart","-t", f"{vo_dur:.3f}",
        str(OUT),
    ], check=True)
    digest = file_sha256(OUT)
    print(f"SAVED {OUT} sha256={digest}", flush=True)
    ICLOUD.mkdir(parents=True, exist_ok=True)
    for old in list(ICLOUD.glob("hos_002_part02_rough_v*.mp4")):
        if old.name == OUT.name:
            continue
        superseded = ICLOUD / f"_SUPERSEDED_do_not_watch_{old.name}"
        if not superseded.exists():
            old.rename(superseded)
    dest = ICLOUD / OUT.name
    subprocess.run(["cp","-f",str(OUT),str(dest)], check=True)
    (ICLOUD / "WATCH_part02_v07.txt").write_text(
        f"WATCH THIS FILE ONLY (Part 02 remint rough v07):\n  {OUT.name}\n\n"
        "Real Veo every beat. Animistry side labels. No Ken Burns. No center stamps.\n"
        f"sha256={digest}\n"
    )
    print(f"ICLOUD {dest}", flush=True)


if __name__ == "__main__":
    main()
