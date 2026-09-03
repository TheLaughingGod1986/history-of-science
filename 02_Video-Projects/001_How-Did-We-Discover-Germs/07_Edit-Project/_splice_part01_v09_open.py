#!/usr/bin/env python3
"""Part 01 v09 — splice-only open recut.

Replace ONLY 0:00–0:08 of v08 with the already-moving instruments plate
stolen from the same cut (05_doctor_hands_instruments / 04_instruments @ 22.8).
In-point after the Explorer xfade. Keep v08 audio. No mint. No Ken Burns.
"""
from __future__ import annotations

import hashlib
import subprocess
from pathlib import Path

PROJ = Path(__file__).resolve().parents[1]
SRC = PROJ / "09_Final-Export/hos_001_part01_rough_v08.mp4"
OUT = PROJ / "09_Final-Export/hos_001_part01_rough_v09.mp4"
PLATE_DIR = PROJ / "04_Generated-Clips/part01/raw/v09_splice"
PLATE = PLATE_DIR / "05_doctor_hands_instruments_from_v08.mp4"
# Plate 04_instruments starts 22.8; 0.4s xfade still has Explorer. First clean frame.
IN_POINT = 23.20
REPLACE = 8.0
ART = Path(
    "/Users/benjaminoats/Library/Application Support/Cursor/"
    "AgentStores/cursor_agent_stores/bc-eb2a62e0-1899-43b0-9cd2-0b96209c2bd0/"
    "files/artifacts"
)
ICLOUD = Path(
    "/Users/benjaminoats/Library/Mobile Documents/com~apple~CloudDocs/HOS UAT"
)


def sha256(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> None:
    if not SRC.exists():
        raise SystemExit(f"missing v08 {SRC}")
    PLATE_DIR.mkdir(parents=True, exist_ok=True)
    # Steal 8s at 1× from v08. No setpts stretch, no zoompan, no loop.
    subprocess.run(
        [
            "ffmpeg", "-y",
            "-ss", f"{IN_POINT:.2f}", "-i", str(SRC),
            "-t", f"{REPLACE:.1f}",
            "-an",
            "-c:v", "libx264", "-pix_fmt", "yuv420p",
            "-profile:v", "baseline", "-level", "3.1", "-bf", "0",
            "-preset", "fast", "-crf", "18",
            "-movflags", "+faststart",
            str(PLATE),
        ],
        check=True,
    )
    # Picture: stolen plate (0–8) + v08 from 8s. Audio: v08 untouched.
    fc = (
        f"[1:v]fps=24,format=yuv420p,setsar=1,trim=0:{REPLACE:.1f},"
        f"setpts=PTS-STARTPTS[new];"
        f"[0:v]trim=start={REPLACE:.1f},setpts=PTS-STARTPTS,"
        f"fps=24,format=yuv420p,setsar=1[post];"
        f"[new][post]concat=n=2:v=1:a=0[v]"
    )
    OUT.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        [
            "ffmpeg", "-y", "-i", str(SRC), "-i", str(PLATE),
            "-filter_complex", fc,
            "-map", "[v]", "-map", "0:a",
            "-c:v", "libx264", "-pix_fmt", "yuv420p",
            "-profile:v", "baseline", "-level", "3.1", "-bf", "0",
            "-preset", "fast", "-crf", "18",
            "-c:a", "copy",
            "-movflags", "+faststart", "-brand", "mp42",
            str(OUT),
        ],
        check=True,
    )
    plate_sha = sha256(PLATE)
    out_sha = sha256(OUT)
    print(f"PLATE {PLATE}", flush=True)
    print(f"PLATE_SHA256 {plate_sha}", flush=True)
    print(f"IN_POINT {IN_POINT}", flush=True)
    print(f"SAVED {OUT}", flush=True)
    print(f"SIZE {OUT.stat().st_size}", flush=True)
    print(f"SHA256 {out_sha}", flush=True)
    ART.mkdir(parents=True, exist_ok=True)
    subprocess.run(["cp", "-f", str(OUT), str(ART / OUT.name)], check=True)
    subprocess.run(["cp", "-f", str(PLATE), str(ART / PLATE.name)], check=True)
    if ICLOUD.parent.exists():
        ICLOUD.mkdir(parents=True, exist_ok=True)
        subprocess.run(["cp", "-f", str(OUT), str(ICLOUD / OUT.name)], check=False)


if __name__ == "__main__":
    main()
