#!/usr/bin/env python3
"""Assemble HOS 002 Part 01 v08 — same picture as v07 + audible continuous workshop bed.

Picture/VO locked PASS. Only the underscore was too quiet/sparse on phone.
Remux video from v07; mix VO + denser bed at Germs-audible level.
"""
from __future__ import annotations

import hashlib
import subprocess
from pathlib import Path

PROJ = Path(__file__).resolve().parents[1]
GERMS_MUSIC = PROJ.parent / "001_How-Did-We-Discover-Germs" / "05_Music"
PIC = PROJ / "09_Final-Export/hos_002_part01_rough_v07.mp4"
VO = PROJ / "02_Voiceover/part01_zoo_of_stuff_v02.wav"
MID = PROJ / "05_Music/hos_002_part01_curious_workshop_v02.mid"
SF2 = GERMS_MUSIC / "TimGM6mb.sf2"
BED_RAW = PROJ / "05_Music/hos_002_part01_curious_workshop_v02.wav"
BED = PROJ / "05_Music/hos_002_part01_curious_workshop_v02_norm.wav"
OUT = PROJ / "09_Final-Export/hos_002_part01_rough_v08.mp4"
ICLOUD = Path("/Users/benjaminoats/Library/Mobile Documents/com~apple~CloudDocs/OWB UAT")
ICLOUD_HOS = Path("/Users/benjaminoats/Library/Mobile Documents/com~apple~CloudDocs/HOS UAT")
# v07 used 0.14 → pauses ~-43 dBFS (inaudible on phone). Target ~-30 like Germs.
BED_VOL = 0.42


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
    print(f"BED {BED} dur≈{probe_dur(BED):.2f}s", flush=True)


def main() -> None:
    if not PIC.exists():
        raise SystemExit(f"STOP: missing locked picture {PIC}")
    if not VO.exists():
        raise SystemExit(f"STOP: missing VO {VO}")
    vo_dur = probe_dur(VO)
    render_bed(vo_dur)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    # Same picture as v07 — only remux audio (VO + continuous workshop bed).
    filt = (
        f"[1:a]aresample=48000,aformat=sample_fmts=fltp:channel_layouts=stereo,"
        f"atrim=0:{vo_dur:.3f},apad=whole_dur={vo_dur:.3f}[vo];"
        f"[2:a]aresample=48000,aformat=sample_fmts=fltp:channel_layouts=stereo,"
        f"atrim=0:{vo_dur:.3f},volume={BED_VOL}[bed];"
        f"[vo][bed]amix=inputs=2:duration=first:normalize=0,"
        f"alimiter=limit=0.95:attack=5:release=50[a]"
    )
    cmd = [
        "ffmpeg", "-y",
        "-i", str(PIC),
        "-i", str(VO),
        "-i", str(BED),
        "-filter_complex", filt,
        "-map", "0:v", "-map", "[a]",
        "-c:v", "copy",
        "-c:a", "aac", "-b:a", "192k",
        "-shortest", "-movflags", "+faststart",
        str(OUT),
    ]
    print(f"assemble v08 (audio remux) → {OUT.name} vo={vo_dur:.2f}s bed_vol={BED_VOL}", flush=True)
    subprocess.run(cmd, check=True)
    digest = sha256(OUT)
    print(f"SAVED {OUT} bytes={OUT.stat().st_size} dur≈{probe_dur(OUT):.2f}s sha256={digest}", flush=True)
    for cloud in (ICLOUD, ICLOUD_HOS):
        if not cloud.parent.exists():
            continue
        cloud.mkdir(parents=True, exist_ok=True)
        dest = cloud / OUT.name
        subprocess.run(["cp", "-f", str(OUT), str(dest)], check=False)
        print(f"ICLOUD {dest} sha256={sha256(dest)}", flush=True)


if __name__ == "__main__":
    main()
