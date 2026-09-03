#!/usr/bin/env python3
"""Part 01 v21 — v20 picture locked + v19 audio with splice softens.

Ready wav is missing the shadow hook (acrossfade bug). Do not use it.
v19 audio has knives + the full hook. Soften 75.208 and 76.300 only.
Picture: copy v20 video bitstream. No remint. No new VO.
"""
from __future__ import annotations

import hashlib
import subprocess
from pathlib import Path

PROJ = Path(__file__).resolve().parents[1]
PIC = PROJ / "09_Final-Export/hos_001_part01_rough_v20.mp4"
PIC_SHA = "b89e4d895b5c5ce59919c50c94b609c7453b98a6eacb13c9696dd43d4f04f1cb"
AUD = PROJ / "09_Final-Export/hos_001_part01_rough_v19.mp4"
OUT = PROJ / "09_Final-Export/hos_001_part01_rough_v21.mp4"
ART = Path(
    "/Users/benjaminoats/Library/Application Support/Cursor/"
    "AgentStores/cursor_agent_stores/bc-eb2a62e0-1899-43b0-9cd2-0b96209c2bd0/"
    "files/artifacts"
)
ICLOUD = Path(
    "/Users/benjaminoats/Library/Mobile Documents/com~apple~CloudDocs/HOS UAT"
)

V16_OUT = 75.208
KNIVES_OUT = 76.300
XF_KNIVES = 0.080
XF_HOOK = 0.060
TOTAL = 80.140


def sha256(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def probe_dur(p: Path) -> float:
    r = subprocess.run(
        [
            "ffprobe", "-v", "error", "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1", str(p),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    return float(r.stdout.strip())


def main() -> None:
    if sha256(PIC) != PIC_SHA:
        raise SystemExit("v20 picture sha mismatch — abort")
    if not AUD.exists():
        raise SystemExit(f"missing {AUD}")

    knives_a = V16_OUT - XF_KNIVES  # 75.128
    hook_a = KNIVES_OUT - XF_HOOK  # 76.240
    # Soften the two hard cuts already in v19. asplit — a pad can only be read once.
    # Do not delay the hook.
    fc = (
        f"[1:a]aformat=sample_fmts=fltp:channel_layouts=stereo,asplit=2[s0][s1];"
        f"[s0]atrim=0:{V16_OUT:.4f},asetpts=PTS-STARTPTS[a0];"
        f"[s1]atrim=start={knives_a:.4f}:end={TOTAL:.4f},asetpts=PTS-STARTPTS[a1];"
        f"[a0][a1]acrossfade=d={XF_KNIVES:.3f}:c1=tri:c2=tri[k];"
        f"[k]asplit=2[t0][t1];"
        f"[t0]atrim=0:{KNIVES_OUT:.4f},asetpts=PTS-STARTPTS[k0];"
        f"[t1]atrim=start={hook_a:.4f},asetpts=PTS-STARTPTS[k1];"
        f"[k0][k1]acrossfade=d={XF_HOOK:.3f}:c1=tri:c2=tri,"
        f"atrim=0:{TOTAL:.4f},asetpts=PTS-STARTPTS[a]"
    )
    OUT.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        [
            "ffmpeg", "-y",
            "-i", str(PIC),
            "-i", str(AUD),
            "-filter_complex", fc,
            "-map", "0:v", "-map", "[a]",
            "-c:v", "copy",
            "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2",
            "-movflags", "+faststart", "-brand", "mp42",
            str(OUT),
        ],
        check=True,
    )
    print(f"PIC v20 copy {PIC_SHA}", flush=True)
    print(f"AUD v19 + xf {XF_KNIVES:.3f}/{XF_HOOK:.3f}", flush=True)
    print(f"SAVED {OUT}", flush=True)
    print(f"SIZE {OUT.stat().st_size}", flush=True)
    print(f"SHA256 {sha256(OUT)}", flush=True)
    print(f"DUR {probe_dur(OUT):.3f}", flush=True)
    ART.mkdir(parents=True, exist_ok=True)
    subprocess.run(["cp", "-f", str(OUT), str(ART / OUT.name)], check=True)
    if ICLOUD.parent.exists():
        ICLOUD.mkdir(parents=True, exist_ok=True)
        subprocess.run(["cp", "-f", str(OUT), str(ICLOUD / OUT.name)], check=False)


if __name__ == "__main__":
    main()
