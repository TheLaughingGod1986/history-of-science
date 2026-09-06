#!/usr/bin/env python3
"""Assemble HOS 002 Part 01 rough v13 — real Veo + Animistry side labels."""
from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

PROJ = Path(__file__).resolve().parents[1]
PLATES_JSON = PROJ / "07_Edit-Project/parts/part-01_plates_v01.json"
RAW = PROJ / "04_Generated-Clips/part01/raw/v01_fast"
LABEL_DIR = PROJ / "04_Generated-Clips/part01/refs/v12_side_labels"
VO = PROJ / "02_Voiceover/part01_zoo_of_stuff_v02.wav"
BED = PROJ / "05_Music/hos_002_part01_curious_workshop_v02_norm.wav"
OUT = PROJ / "09_Final-Export/hos_002_part01_rough_v13.mp4"
ICLOUD = Path.home() / "Library/Mobile Documents/com~apple~CloudDocs/HOS UAT"
CLIP_USE = 8.0
XFADE = 0.35
BED_VOL = 0.38

SIDE_LABELS = [
    (2.4, 6.2, "SEATING PLAN"),
    (33.2, 39.2, "IRON · SALT · FLAME"),
    (44.8, 49.0, "EARTH AIR FIRE WATER"),
    (53.8, 59.8, "ROCK · GAS · MASS"),
    (65.8, 72.0, "ALCHEMISTS · CHEMISTS"),
    (76.8, 80.2, "A LABELLED ZOO"),
    (82.6, 85.5, "SEATING PLAN"),
]


def probe(path: Path) -> float:
    return float(
        subprocess.check_output(
            [
                "ffprobe", "-v", "error", "-show_entries", "format=duration",
                "-of", "default=nw=1:nk=1", str(path),
            ],
            text=True,
        ).strip()
    )


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
    d.rounded_rectangle(
        (8, 8, w - 8, h - 8), radius=18, outline=(232, 214, 180, 230), width=3
    )
    try:
        font = ImageFont.truetype(
            "/System/Library/Fonts/Supplemental/Georgia Bold.ttf", 34
        )
    except OSError:
        font = ImageFont.load_default()
    bb = d.textbbox((0, 0), text, font=font)
    tw, th = bb[2] - bb[0], bb[3] - bb[1]
    d.text(((w - tw) / 2, (h - th) / 2 - 4), text, fill=(245, 232, 205, 255), font=font)
    im.save(dest)


def main() -> None:
    plates = json.loads(PLATES_JSON.read_text())["plates"]
    clips: list[Path] = []
    for plate in plates:
        pid = plate["id"]
        clip = RAW / f"{pid}_v01.mp4"
        if not clip.exists() or clip.stat().st_size < 400_000:
            raise SystemExit(f"missing real-motion plate {clip}")
        d = probe(clip)
        if d < 5.5:
            raise SystemExit(f"short plate {clip} d={d}")
        clips.append(clip)
        print(f"  {pid}: {d:.2f}s", flush=True)

    if plates[9]["id"] != "10_rock_not_fire":
        raise SystemExit(f"plate 10 must be 10_rock_not_fire, got {plates[9]['id']}")

    if not VO.exists():
        raise SystemExit(f"missing VO {VO}")
    if not BED.exists():
        raise SystemExit(f"missing bed {BED}")
    vo_dur = probe(VO)
    pic_dur = len(clips) * CLIP_USE - (len(clips) - 1) * XFADE
    print(f"picture≈{pic_dur:.2f}s VO={vo_dur:.2f}s", flush=True)
    if pic_dur + 0.05 < vo_dur:
        raise SystemExit(f"picture {pic_dur:.2f} < VO {vo_dur:.2f}")

    LABEL_DIR.mkdir(parents=True, exist_ok=True)
    label_pngs: list[tuple[float, float, Path]] = []
    for i, (a, b, text) in enumerate(SIDE_LABELS):
        png = LABEL_DIR / f"label_{i:02d}.png"
        render_side_label(text, png)
        label_pngs.append((a, min(b, vo_dur), png))

    OUT.parent.mkdir(parents=True, exist_ok=True)
    n = len(clips)
    inputs: list[str] = []
    for c in clips:
        inputs += ["-i", str(c)]
    inputs += ["-i", str(VO), "-i", str(BED)]
    label_input_start = n + 2
    for _, _, png in label_pngs:
        inputs += ["-loop", "1", "-t", "1", "-i", str(png)]

    parts: list[str] = []
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
        parts.append(
            f"{vlabel}[v{i}]xfade=transition=fade:duration={XFADE}:offset={offset:.3f}{out}"
        )
        vlabel = out

    cur = vlabel
    for li, (a, b, _png) in enumerate(label_pngs):
        idx = label_input_start + li
        nxt = f"[vl{li}]"
        parts.append(
            f"[{idx}:v]format=rgba,scale=640:-1[lg{li}];"
            f"{cur}[lg{li}]overlay=x=1920-660:y=48:enable='between(t,{a:.3f},{b:.3f})'{nxt}"
        )
        cur = nxt

    parts.append(
        f"[{n}:a]aformat=sample_rates=48000:channel_layouts=stereo,"
        f"atrim=0:{vo_dur:.3f},asetpts=PTS-STARTPTS[vo]"
    )
    parts.append(
        f"[{n+1}:a]aformat=sample_rates=48000:channel_layouts=stereo,"
        f"atrim=0:{vo_dur:.3f},volume={BED_VOL}[bed]"
    )
    parts.append("[vo][bed]amix=inputs=2:duration=first:dropout_transition=0[a]")
    fc = ";".join(parts)

    subprocess.run(
        [
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            *inputs,
            "-filter_complex", fc,
            "-map", cur, "-map", "[a]",
            "-c:v", "libx264", "-preset", "medium", "-crf", "18",
            "-c:a", "aac", "-b:a", "192k",
            "-movflags", "+faststart", "-t", f"{vo_dur:.3f}",
            str(OUT),
        ],
        check=True,
    )
    digest = file_sha256(OUT)
    print(
        f"SAVED {OUT} bytes={OUT.stat().st_size} dur≈{probe(OUT):.2f}s sha256={digest}",
        flush=True,
    )

    ICLOUD.mkdir(parents=True, exist_ok=True)
    for old in list(ICLOUD.glob("hos_002_part01_rough_v*.mp4")):
        if old.name == OUT.name:
            continue
        superseded = ICLOUD / f"_SUPERSEDED_do_not_watch_{old.name}"
        if not superseded.exists():
            old.rename(superseded)
            print(f"superseded {old.name}", flush=True)
    dest = ICLOUD / OUT.name
    subprocess.run(["cp", "-f", str(OUT), str(dest)], check=True)
    watch = ICLOUD / "WATCH_part01_v13.txt"
    watch.write_text(
        "WATCH THIS FILE ONLY (Part 01 remint rough v13):\n"
        f"  {OUT.name}\n\n"
        "Ben unlocked motion remint 5 Sep. Gate:\n"
        "- Real Veo every beat (no Ken Burns hero)\n"
        "- Animistry side labels (upper-right, not center stamps)\n"
        "- Continuity: no still↔motion style flips\n"
        "- Plate 10 remint: colourless shimmer under grate (NO orange/fire/embers)\n- KEEP: ore IN brass pan · Animistry side labels · no flask beside scale\n"
        "- Explorer once · British VO · 3D cartoon\n\n"
        "Do not ping Ben. Reject with stills from THIS file only.\n"
        f"sha256={digest}\n"
    )
    (ICLOUD / "ZZ_OPEN_PART01_V13.txt").write_text(
        "Part 01 current remint cut = hos_002_part01_rough_v13.mp4\n"
        "Prior v12 superseded in this folder.\n"
    )
    print(f"ICLOUD {dest}", flush=True)
    print(f"WATCH {watch}", flush=True)
    print(f"HANDOFF path={OUT}", flush=True)
    print(f"HANDOFF bytes={OUT.stat().st_size}", flush=True)
    print(f"HANDOFF sha256={digest}", flush=True)
    print(f"HANDOFF duration_s={probe(OUT):.3f}", flush=True)


if __name__ == "__main__":
    main()
