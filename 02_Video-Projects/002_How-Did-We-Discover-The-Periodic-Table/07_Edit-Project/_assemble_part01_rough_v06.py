#!/usr/bin/env python3
"""Assemble HOS 002 Part 01 v06 — plates + VO + curious workshop bed + iCloud."""
from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path

PROJ = Path(__file__).resolve().parents[1]
GERMS_MUSIC = PROJ.parent / "001_How-Did-We-Discover-Germs" / "05_Music"
PLATES_JSON = PROJ / "07_Edit-Project/parts/part-01_plates_v01.json"
RAW = PROJ / "04_Generated-Clips/part01/raw/v01_fast"
VO = PROJ / "02_Voiceover/part01_zoo_of_stuff_v02.wav"
MID = PROJ / "05_Music/hos_002_part01_curious_workshop_v01.mid"
SF2 = GERMS_MUSIC / "TimGM6mb.sf2"
BED_RAW = PROJ / "05_Music/hos_002_part01_curious_workshop_v01.wav"
BED = PROJ / "05_Music/hos_002_part01_curious_workshop_v01_norm.wav"
OUT = PROJ / "09_Final-Export/hos_002_part01_rough_v07.mp4"
# HOS only — never Orbit With Ben (OWB UAT).
ICLOUD = Path("/Users/benjaminoats/Library/Mobile Documents/com~apple~CloudDocs/HOS UAT")
ICLOUD_HOS = ICLOUD
CLIP_USE = 8.0
XFADE = 0.4
BED_VOL = 0.14


def probe_dur(path: Path) -> float:
    out = subprocess.check_output(
        [
            "ffprobe", "-v", "error", "-show_entries", "format=duration",
            "-of", "default=nw=1:nk=1", str(path),
        ],
        text=True,
    ).strip()
    return float(out)


def sha256(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def render_bed(vo_dur: float) -> None:
    if not MID.exists() or not SF2.exists():
        raise SystemExit(f"STOP: missing MIDI or sf2 ({MID} / {SF2})")
    BED_RAW.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        ["fluidsynth", "-ni", "-l", "-r", "48000", "-g", "0.7", "-F", str(BED_RAW), str(SF2), str(MID)],
        check=True,
        capture_output=True,
    )
    fade_out_start = max(vo_dur - 2.2, 1.0)
    subprocess.run(
        [
            "ffmpeg", "-y", "-i", str(BED_RAW),
            "-af", f"loudnorm=I=-22:LRA=8:TP=-3,afade=t=in:d=1.4,afade=t=out:st={fade_out_start:.2f}:d=2.0",
            "-ar", "48000", "-ac", "2", str(BED),
        ],
        check=True,
        capture_output=True,
    )
    print(f"BED {BED} dur≈{probe_dur(BED):.2f}s", flush=True)


def main() -> None:
    plates = json.loads(PLATES_JSON.read_text())["plates"]
    clips: list[Path] = []
    for plate in plates:
        mp4 = RAW / f"{plate['id']}_v01.mp4"
        if not mp4.exists() or mp4.stat().st_size < 400_000:
            raise SystemExit(f"missing/small plate: {mp4}")
        clips.append(mp4)
    if not VO.exists():
        raise SystemExit(f"missing VO {VO}")
    vo_dur = probe_dur(VO)
    pic_dur = len(clips) * CLIP_USE - (len(clips) - 1) * XFADE
    if pic_dur + 0.05 < vo_dur:
        raise SystemExit(f"STOP: picture {pic_dur:.2f}s < VO {vo_dur:.2f}s")
    render_bed(vo_dur)
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
    vprev = "v0"
    offset = CLIP_USE - XFADE
    for i in range(1, n):
        out = f"vx{i}"
        parts.append(
            f"[{vprev}][v{i}]xfade=transition=fade:duration={XFADE}:offset={offset:.3f}[{out}]"
        )
        vprev = out
        offset += CLIP_USE - XFADE
    parts.append(f"[{vprev}]trim=0:{vo_dur:.3f},setpts=PTS-STARTPTS[vout]")
    parts.append(
        f"[{n}:a]aresample=48000,aformat=sample_fmts=fltp:channel_layouts=stereo,"
        f"atrim=0:{vo_dur:.3f},apad=whole_dur={vo_dur:.3f}[vo]"
    )
    parts.append(
        f"[{n+1}:a]aresample=48000,aformat=sample_fmts=fltp:channel_layouts=stereo,"
        f"atrim=0:{vo_dur:.3f},volume={BED_VOL}[bed]"
    )
    parts.append("[vo][bed]amix=inputs=2:duration=first:normalize=0[a]")
    filt = ";".join(parts)
    cmd = [
        "ffmpeg", "-y", *inputs, "-filter_complex", filt,
        "-map", "[vout]", "-map", "[a]",
        "-c:v", "libx264", "-preset", "fast", "-crf", "18",
        "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart",
        str(OUT),
    ]
    print(f"assemble v07 → {OUT.name} vo={vo_dur:.2f}s bed_vol={BED_VOL}", flush=True)
    subprocess.run(cmd, check=True)
    digest = sha256(OUT)
    print(f"SAVED {OUT} bytes={OUT.stat().st_size} dur≈{probe_dur(OUT):.2f}s sha256={digest}", flush=True)
    ICLOUD.mkdir(parents=True, exist_ok=True)
    dest = ICLOUD / OUT.name
    subprocess.run(["cp", "-f", str(OUT), str(dest)], check=True)
    print(f"ICLOUD {dest} sha256={sha256(dest)}", flush=True)
    owb = Path("/Users/benjaminoats/Library/Mobile Documents/com~apple~CloudDocs/OWB UAT")
    if owb.exists():
        for stale in owb.glob("hos_*.mp4"):
            stale.unlink()
            print(f"removed from OWB UAT: {stale.name}", flush=True)


if __name__ == "__main__":
    main()
