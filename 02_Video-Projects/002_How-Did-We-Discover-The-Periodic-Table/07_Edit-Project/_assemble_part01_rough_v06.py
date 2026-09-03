#!/usr/bin/env python3
"""Assemble HOS 002 Part 01 rough v06 — unique Flow plates + locked VO."""
from __future__ import annotations

import json
import subprocess
from pathlib import Path

PROJ = Path(__file__).resolve().parents[1]
PLATES_JSON = PROJ / "07_Edit-Project/parts/part-01_plates_v01.json"
RAW = PROJ / "04_Generated-Clips/part01/raw/v01_fast"
VO = PROJ / "02_Voiceover/part01_zoo_of_stuff_v02.wav"
OUT = PROJ / "09_Final-Export/hos_002_part01_rough_v06.mp4"
CLIP_USE = 8.0
XFADE = 0.4


def probe_dur(path: Path) -> float:
    out = subprocess.check_output(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "default=nw=1:nk=1",
            str(path),
        ],
        text=True,
    ).strip()
    return float(out)


def main() -> None:
    plates = json.loads(PLATES_JSON.read_text())["plates"]
    clips: list[Path] = []
    for plate in plates:
        mp4 = RAW / f"{plate['id']}_v01.mp4"
        if not mp4.exists() or mp4.stat().st_size < 400_000:
            raise SystemExit(f"missing/small plate: {mp4}")
        clips.append(mp4)
    if not VO.exists():
        raise SystemExit(f"missing VO: {VO}")
    vo_dur = probe_dur(VO)
    pic_dur = len(clips) * CLIP_USE - (len(clips) - 1) * XFADE
    if pic_dur + 0.05 < vo_dur:
        raise SystemExit(
            f"STOP: picture {pic_dur:.2f}s < VO {vo_dur:.2f}s — mint more unique plates"
        )
    OUT.parent.mkdir(parents=True, exist_ok=True)
    inputs: list[str] = []
    for c in clips:
        inputs += ["-i", str(c)]
    inputs += ["-i", str(VO)]
    parts: list[str] = []
    for i in range(len(clips)):
        parts.append(
            f"[{i}:v]trim=0:{CLIP_USE},setpts=PTS-STARTPTS,"
            f"scale=1920:1080:force_original_aspect_ratio=decrease,"
            f"pad=1920:1080:(ow-iw)/2:(oh-ih)/2,fps=24,format=yuv420p[v{i}]"
        )
    vprev = "v0"
    offset = CLIP_USE - XFADE
    for i in range(1, len(clips)):
        out = f"vx{i}"
        parts.append(
            f"[{vprev}][v{i}]xfade=transition=fade:duration={XFADE}:offset={offset:.3f}[{out}]"
        )
        vprev = out
        offset += CLIP_USE - XFADE
    n = len(clips)
    parts.append(
        f"[{n}:a]aresample=48000,aformat=sample_fmts=fltp:channel_layouts=stereo,"
        f"atrim=0:{vo_dur:.3f},apad=whole_dur={vo_dur:.3f}[a]"
    )
    parts.append(f"[{vprev}]trim=0:{vo_dur:.3f},setpts=PTS-STARTPTS[vout]")
    filt = ";".join(parts)
    cmd = [
        "ffmpeg",
        "-y",
        *inputs,
        "-filter_complex",
        filt,
        "-map",
        "[vout]",
        "-map",
        "[a]",
        "-c:v",
        "libx264",
        "-preset",
        "fast",
        "-crf",
        "18",
        "-c:a",
        "aac",
        "-b:a",
        "192k",
        "-shortest",
        "-movflags",
        "+faststart",
        str(OUT),
    ]
    print(f"assemble v06 → {OUT.name} vo={vo_dur:.2f}s", flush=True)
    subprocess.run(cmd, check=True)
    print(f"SAVED {OUT} bytes={OUT.stat().st_size} dur≈{probe_dur(OUT):.2f}s", flush=True)


if __name__ == "__main__":
    main()
