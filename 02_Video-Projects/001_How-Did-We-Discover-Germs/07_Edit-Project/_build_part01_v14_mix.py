#!/usr/bin/env python3
"""Part 01 v14 — rebuild mix from v12 stems. Do not reuse the v13 flatten.

v12 picture (card + 0:08 dissolve). v09 VO. All v12 FX. No metal. No remint.
"""
from __future__ import annotations

import hashlib
import subprocess
from pathlib import Path

PROJ = Path(__file__).resolve().parents[1]
PIC = PROJ / "09_Final-Export/hos_001_part01_rough_v12.mp4"
VO_SRC = PROJ / "09_Final-Export/hos_001_part01_rough_v09.mp4"
OUT = PROJ / "09_Final-Export/hos_001_part01_rough_v14.mp4"
MUSIC = PROJ / "05_Music"
SFX = PROJ / "06_Sound-Effects/v12"
BED_RAW = MUSIC / "hos_001_part01_ominous_ward_v12.wav"
BED = MUSIC / "hos_001_part01_ominous_ward_v14_norm.wav"
WALLA = SFX / "walla_ward_v12.wav"
ROOM = SFX / "room_ward_v12.wav"
COUGH = SFX / "cough_v12.wav"
CLOTH = SFX / "cloth_v12.wav"
WOOD = SFX / "wood_v12.wav"
GLASS = SFX / "glass_lamp_v12.wav"
METAL = PROJ / "06_Sound-Effects/v10/metal_instrument_clink_v10.wav"
ART = Path(
    "/Users/benjaminoats/Library/Application Support/Cursor/"
    "AgentStores/cursor_agent_stores/bc-eb2a62e0-1899-43b0-9cd2-0b96209c2bd0/"
    "files/artifacts"
)
ICLOUD = Path(
    "/Users/benjaminoats/Library/Mobile Documents/com~apple~CloudDocs/HOS UAT"
)
# Pre-speech HF burst on the instruments/tray in-point (v09). Not VO.
CLINK_MUTE = (57.28, 57.56)


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
    needed = [PIC, VO_SRC, BED_RAW, WALLA, ROOM, COUGH, CLOTH, WOOD, GLASS]
    missing = [str(p) for p in needed if not p.exists()]
    if missing:
        raise SystemExit("missing " + ", ".join(missing))
    if METAL.exists():
        METAL.unlink()

    pic_dur = probe_dur(PIC)
    # 12ms click-guard only — not a fade-out ending.
    cut = pic_dur

    subprocess.run(
        [
            "ffmpeg", "-y", "-i", str(BED_RAW),
            "-af", "loudnorm=I=-21:LRA=9:TP=-3,afade=t=in:d=1.5",
            "-ar", "48000", "-ac", "2", str(BED),
        ],
        check=True,
        capture_output=True,
    )
    vo = SFX / "_vo_from_v09_v14.wav"
    subprocess.run(
        [
            "ffmpeg", "-y", "-i", str(VO_SRC),
            "-t", f"{cut:.6f}", "-vn", "-ac", "2", "-ar", "48000", str(vo),
        ],
        check=True,
        capture_output=True,
    )

    a0, a1 = CLINK_MUTE
    fc = (
        f"[0:v]trim=0:{cut:.6f},setpts=PTS-STARTPTS,format=yuv420p,setsar=1[v];"
        f"[1:a]aformat=sample_fmts=fltp:channel_layouts=stereo,"
        f"volume=enable='between(t,{a0:.2f},{a1:.2f})':volume=0,"
        f"asplit=2[vo][sc];"
        f"[2:a]atrim=0:{cut:.6f},asetpts=PTS-STARTPTS,volume=0.14[bed];"
        f"[3:a]atrim=0:{cut:.6f},volume=0.09[walla_raw];"
        f"[walla_raw][sc]sidechaincompress=threshold=0.025:ratio=10:attack=12:"
        f"release=220:makeup=1.4[walla];"
        f"[4:a]atrim=0:{cut:.6f},volume=0.06[room];"
        f"[5:a]asplit=3[cg1][cg2][cg3];"
        f"[cg1]adelay=12800|12800,volume=0.10[c1];"
        f"[cg2]adelay=38550|38550,volume=0.09[c2];"
        f"[cg3]adelay=47150|47150,volume=0.09[c3];"
        f"[6:a]adelay=1050|1050,volume=0.10[grab_cloth];"
        f"[7:a]adelay=6350|6350,volume=0.09[grab_wood];"
        f"[8:a]adelay=2100|2100,volume=0.07[grab_glass];"
        f"[vo][bed][walla][room][c1][c2][c3][grab_cloth][grab_wood][grab_glass]"
        f"amix=inputs=10:duration=first:dropout_transition=0:normalize=0,"
        f"afade=t=out:st={cut - 0.012:.6f}:d=0.012[a]"
    )
    OUT.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        [
            "ffmpeg", "-y",
            "-i", str(PIC),
            "-i", str(vo),
            "-i", str(BED),
            "-i", str(WALLA),
            "-i", str(ROOM),
            "-i", str(COUGH),
            "-i", str(CLOTH),
            "-i", str(WOOD),
            "-i", str(GLASS),
            "-filter_complex", fc,
            "-map", "[v]", "-map", "[a]",
            "-c:v", "libx264", "-pix_fmt", "yuv420p",
            "-profile:v", "baseline", "-level", "3.1", "-bf", "0",
            "-preset", "fast", "-crf", "18",
            "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2",
            "-movflags", "+faststart", "-brand", "mp42",
            str(OUT),
        ],
        check=True,
    )
    print(f"CUT {cut:.6f}", flush=True)
    print(f"SAVED {OUT}", flush=True)
    print(f"SIZE {OUT.stat().st_size}", flush=True)
    print(f"SHA256 {sha256(OUT)}", flush=True)
    print(f"DUR {probe_dur(OUT):.3f}", flush=True)
    ART.mkdir(parents=True, exist_ok=True)
    subprocess.run(["cp", "-f", str(OUT), str(ART / OUT.name)], check=True)
    if ICLOUD.parent.exists():
        ICLOUD.mkdir(parents=True, exist_ok=True)
        subprocess.run(["cp", "-f", str(OUT), str(ICLOUD / OUT.name)], check=False)
    print(f"ART {ART / OUT.name}", flush=True)
    print(f"ICLOUD {ICLOUD / OUT.name}", flush=True)


if __name__ == "__main__":
    main()
