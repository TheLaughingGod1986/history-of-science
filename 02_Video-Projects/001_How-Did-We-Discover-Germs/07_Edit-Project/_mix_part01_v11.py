#!/usr/bin/env python3
"""Part 01 v11 — mix only. Keep v10 picture. New DLS pad + period-ward FX."""
from __future__ import annotations

import hashlib
import subprocess
from pathlib import Path

PROJ = Path(__file__).resolve().parents[1]
PIC = PROJ / "09_Final-Export/hos_001_part01_rough_v10.mp4"
VO_SRC = PROJ / "09_Final-Export/hos_001_part01_rough_v09.mp4"
OUT = PROJ / "09_Final-Export/hos_001_part01_rough_v11.mp4"
BED_RAW = PROJ / "05_Music/hos_001_part01_warm_dls_pad_v11.wav"
BED = PROJ / "05_Music/hos_001_part01_warm_dls_pad_v11_norm.wav"
SFX = PROJ / "06_Sound-Effects/v11"
SINE = PROJ / "05_Music/hos_001_part01_curious_pad_v10.wav"
METAL = PROJ / "06_Sound-Effects/v10/metal_instrument_clink_v10.wav"
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


def ff(*args: str) -> None:
    subprocess.run(["ffmpeg", "-y", *args], check=True, capture_output=True)


def main() -> None:
    if not PIC.exists():
        raise SystemExit(f"missing v10 picture {PIC}")
    if not VO_SRC.exists():
        raise SystemExit(f"missing v09 VO source {VO_SRC}")
    if not BED_RAW.exists():
        raise SystemExit(f"missing DLS pad {BED_RAW}")
    SFX.mkdir(parents=True, exist_ok=True)
    pic_dur = probe_dur(PIC)

    # Kill sine + metal so they cannot leak into the mix.
    for dead in (SINE, METAL):
        if dead.exists():
            dead.unlink()

    # Bed: real DLS instruments, lift so a phone hears music, still mix under VO.
    ff(
        "-i", str(BED_RAW),
        "-af", "loudnorm=I=-22:LRA=8:TP=-3,afade=t=in:d=1.2,afade=t=out:st=73.5:d=1.7",
        "-ar", "48000", "-ac", "2", str(BED),
    )

    cloth = SFX / "cloth_coat_curtain_v11.wav"
    wood = SFX / "wood_table_v11.wav"
    # Fabric rustle — fluttered brown noise, no metal.
    ff(
        "-f", "lavfi",
        "-i", "anoisesrc=color=brown:duration=0.7:sample_rate=48000",
        "-af",
        "highpass=f=280,lowpass=f=2200,tremolo=f=14:d=0.55,volume=0.45,"
        "afade=t=in:st=0:d=0.05,afade=t=out:st=0.38:d=0.32",
        "-ac", "2", str(cloth),
    )
    # Wood table / bed-frame knock — low, short, not steel.
    ff(
        "-f", "lavfi",
        "-i",
        "aevalsrc=0.7*sin(2*PI*92*t)*exp(-14*t)"
        "+0.25*sin(2*PI*148*t)*exp(-18*t):d=0.4:s=48000",
        "-af", "lowpass=f=420,volume=0.55,afade=t=out:st=0.18:d=0.22",
        "-ac", "2", str(wood),
    )

    vo = SFX / "_vo_from_v09.wav"
    ff(
        "-i", str(VO_SRC),
        "-t", f"{pic_dur:.6f}",
        "-vn", "-ac", "2", "-ar", "48000", str(vo),
    )

    fc = (
        f"[1:a]atrim=0:{pic_dur:.6f},asetpts=PTS-STARTPTS,"
        f"aformat=sample_fmts=fltp:channel_layouts=stereo[vo];"
        f"[2:a]atrim=0:{pic_dur:.6f},asetpts=PTS-STARTPTS,volume=0.13[bed];"
        f"[3:a]asplit=2[craw1][craw2];"
        f"[craw1]adelay=1050|1050,volume=0.11[coat];"
        f"[craw2]adelay=7050|7050,volume=0.10[curtain];"
        f"[4:a]adelay=6350|6350,volume=0.09[wood];"
        f"[vo][bed][coat][curtain][wood]amix=inputs=5:duration=first:"
        f"dropout_transition=0:normalize=0[a]"
    )
    OUT.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        [
            "ffmpeg", "-y",
            "-i", str(PIC),
            "-i", str(vo),
            "-i", str(BED),
            "-i", str(cloth),
            "-i", str(wood),
            "-filter_complex", fc,
            "-map", "0:v", "-map", "[a]",
            "-c:v", "copy",
            "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2",
            "-movflags", "+faststart", "-brand", "mp42",
            str(OUT),
        ],
        check=True,
    )
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
