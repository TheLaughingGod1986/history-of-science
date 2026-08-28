#!/usr/bin/env python3
"""Replace only 0:53–1:01 of Part 02 v01 with plate 08 v03 I2V. Keep v01 audio."""
from __future__ import annotations

import hashlib
import subprocess
from pathlib import Path

PROJ = Path(__file__).resolve().parents[1]
SRC_CANDIDATES = [
    Path("/opt/cursor/artifacts/hos_001_part02_rough_v01.mp4"),
    PROJ / "09_Final-Export/hos_001_part02_rough_v01.mp4",
]
PLATE = PROJ / "04_Generated-Clips/part02/raw/v03_flow/08_ward_vs_lens_v03.mp4"
OUT = PROJ / "09_Final-Export/hos_001_part02_rough_v03.mp4"
ART = Path("/opt/cursor/artifacts")
T0, T1 = 53.0, 61.0


def sha256(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> None:
    src = next((p for p in SRC_CANDIDATES if p.exists()), None)
    if src is None:
        raise SystemExit("missing v01 rough")
    if not PLATE.exists():
        raise SystemExit(f"missing plate {PLATE}")
    OUT.parent.mkdir(parents=True, exist_ok=True)
    ART.mkdir(parents=True, exist_ok=True)
    fc = (
        f"[1:v]trim=0:8,setpts=PTS-STARTPTS,"
        f"scale=1280:720:force_original_aspect_ratio=decrease,"
        f"pad=1280:720:(ow-iw)/2:(oh-ih)/2,fps=24,format=yuv420p,setsar=1[new];"
        f"[0:v]trim=0:{T0},setpts=PTS-STARTPTS,fps=24,format=yuv420p,setsar=1[pre];"
        f"[0:v]trim=start={T1},setpts=PTS-STARTPTS,fps=24,format=yuv420p,setsar=1[post];"
        f"[pre][new][post]concat=n=3:v=1:a=0[v]"
    )
    subprocess.run(
        [
            "ffmpeg", "-y", "-i", str(src), "-i", str(PLATE),
            "-filter_complex", fc,
            "-map", "[v]", "-map", "0:a",
            "-c:v", "libx264", "-pix_fmt", "yuv420p",
            "-profile:v", "baseline", "-level", "3.1", "-bf", "0",
            "-preset", "fast", "-crf", "18",
            "-c:a", "copy",
            "-movflags", "+faststart", "-brand", "mp42", str(OUT),
        ],
        check=True,
    )
    dest = ART / OUT.name
    subprocess.run(["cp", "-f", str(OUT), str(dest)], check=True)
    print(f"SAVED {OUT}", flush=True)
    print(f"SAVED {dest}", flush=True)
    print(f"SIZE {OUT.stat().st_size}", flush=True)
    print(f"SHA256 {sha256(OUT)}", flush=True)


if __name__ == "__main__":
    main()
