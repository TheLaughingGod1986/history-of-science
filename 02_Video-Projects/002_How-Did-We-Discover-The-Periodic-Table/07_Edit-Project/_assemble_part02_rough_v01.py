#!/usr/bin/env python3
"""Assemble HOS 002 Part 02 rough v01 — First Patterns, Still Wrong → HOS UAT."""
from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path

PROJ = Path(__file__).resolve().parents[1]
GERMS_MUSIC = PROJ.parent / "001_How-Did-We-Discover-Germs" / "05_Music"
PLATES_JSON = PROJ / "07_Edit-Project/parts/part-02_plates_v01.json"
RAW = PROJ / "04_Generated-Clips/part02/raw/v01_fast"
VO = PROJ / "02_Voiceover/part02_first_patterns_v01.wav"
BED = PROJ / "05_Music/hos_002_part01_curious_workshop_v02_norm.wav"
MID = PROJ / "05_Music/hos_002_part01_curious_workshop_v02.mid"
SF2 = GERMS_MUSIC / "TimGM6mb.sf2"
BED_RAW = PROJ / "05_Music/hos_002_part01_curious_workshop_v02.wav"
OUT = PROJ / "09_Final-Export/hos_002_part02_rough_v02.mp4"
ICLOUD = Path("/Users/benjaminoats/Library/Mobile Documents/com~apple~CloudDocs/HOS UAT")
CLIP_USE = 8.0
XFADE = 0.4
BED_VOL = 0.42


def probe_dur(path: Path) -> float:
    return float(
        subprocess.check_output(
            [
                "ffprobe", "-v", "error", "-show_entries", "format=duration",
                "-of", "default=nw=1:nk=1", str(path),
            ],
            text=True,
        ).strip()
    )


def sha256(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def ensure_bed(vo_dur: float) -> None:
    if BED.exists() and probe_dur(BED) >= vo_dur:
        return
    if not MID.exists() or not SF2.exists():
        raise SystemExit(f"STOP: missing MIDI/sf2 ({MID} / {SF2})")
    BED_RAW.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        ["fluidsynth", "-ni", "-l", "-r", "48000", "-g", "1.0", "-F", str(BED_RAW), str(SF2), str(MID)],
        check=True,
        capture_output=True,
    )
    fade_out_start = max(vo_dur - 2.2, 1.0)
    subprocess.run(
        [
            "ffmpeg", "-y", "-i", str(BED_RAW),
            "-af",
            f"loudnorm=I=-20:LRA=9:TP=-2.5,afade=t=in:d=1.2,afade=t=out:st={fade_out_start:.2f}:d=2.0",
            "-ar", "48000", "-ac", "2", str(BED),
        ],
        check=True,
        capture_output=True,
    )


def main() -> None:
    plates = json.loads(PLATES_JSON.read_text())["plates"]
    clips: list[Path] = []
    for plate in plates:
        mp4 = RAW / f"{plate['id']}_v01.mp4"
        if not mp4.exists() or mp4.stat().st_size < 400_000:
            raise SystemExit(f"missing/small: {mp4}")
        d = probe_dur(mp4)
        if d < 5.5 or d > 12.0:
            raise SystemExit(f"STOP bad duration {mp4.name} d={d}")
        clips.append(mp4)
        print(f"  {plate['id']}: {mp4.stat().st_size}b {d:.2f}s", flush=True)
    if not VO.exists():
        raise SystemExit(f"missing VO {VO}")
    vo_dur = probe_dur(VO)
    pic_dur = len(clips) * CLIP_USE - (len(clips) - 1) * XFADE
    if pic_dur + 0.05 < vo_dur:
        raise SystemExit(f"picture {pic_dur:.2f} < VO {vo_dur:.2f} — need more plates or shorter VO")
    ensure_bed(vo_dur)
    OUT.parent.mkdir(parents=True, exist_ok=True)

    inputs: list[str] = []
    for c in clips:
        inputs += ["-i", str(c)]
    n = len(clips)
    inputs += ["-i", str(VO), "-i", str(BED)]
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
        parts.append(
            f"{vlabel}[v{i}]xfade=transition=fade:duration={XFADE}:offset="
            f"{(CLIP_USE - XFADE) * i:.3f}{out}"
        )
        vlabel = out
    parts.append(
        f"[{n}:a]aformat=sample_rates=48000:channel_layouts=stereo,atrim=0:{vo_dur:.3f},"
        f"asetpts=PTS-STARTPTS[vo]"
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
            "-map", vlabel, "-map", "[a]",
            "-c:v", "libx264", "-preset", "medium", "-crf", "18",
            "-c:a", "aac", "-b:a", "192k",
            "-movflags", "+faststart", "-t", f"{vo_dur:.3f}",
            str(OUT),
        ],
        check=True,
    )
    digest = sha256(OUT)
    print(
        f"SAVED {OUT} bytes={OUT.stat().st_size} dur≈{probe_dur(OUT):.2f}s sha256={digest}",
        flush=True,
    )
    ICLOUD.mkdir(parents=True, exist_ok=True)
    dest = ICLOUD / OUT.name
    subprocess.run(["cp", "-f", str(OUT), str(dest)], check=True)
    watch = ICLOUD / "WATCH_part02_v02.txt"
    watch.write_text(
        "WATCH THIS FILE ONLY:\n"
        f"  {OUT.name}\n\n"
        "Part 02 — First Patterns, Still Wrong (v02 UAT fix).\n"
        "Science cards kept — now exact English + factual.\n"
        "Workshop fire / flaming pots removed (cards 02–11 are local parchment).\n"
        "Plate 01 chapter card kept from prior PASS-style mint.\n"
        "Part 01 is PASS. Reject with stills from THIS file only.\n"
        "Do NOT start Part 03 until Ben PASSes this cut.\n"
    )
    print(f"ICLOUD {dest} sha256={sha256(dest)}", flush=True)


if __name__ == "__main__":
    main()
