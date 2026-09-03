#!/usr/bin/env python3
"""Part 01 v10 — join-only at ~0:08, then mix. No mint. No Flow.

Hands (v09 0–7.20, out on forceps pass) dissolve 10 frames into the
surviving aisle plate (v09 from 8.00). Strips the Edison/bed ghost
(fever leak + old-open smash). Then quiet curious pad + sparse on-picture FX.
"""
from __future__ import annotations

import hashlib
import subprocess
from pathlib import Path

PROJ = Path(__file__).resolve().parents[1]
SRC = PROJ / "09_Final-Export/hos_001_part01_rough_v09.mp4"
OUT = PROJ / "09_Final-Export/hos_001_part01_rough_v10.mp4"
WORK = PROJ / "04_Generated-Clips/part01/raw/v10_join"
MUSIC = PROJ / "05_Music"
SFX_DIR = PROJ / "06_Sound-Effects/v10"
ART = Path(
    "/Users/benjaminoats/Library/Application Support/Cursor/"
    "AgentStores/cursor_agent_stores/bc-eb2a62e0-1899-43b0-9cd2-0b96209c2bd0/"
    "files/artifacts"
)
ICLOUD = Path(
    "/Users/benjaminoats/Library/Mobile Documents/com~apple~CloudDocs/HOS UAT"
)

HANDS_OUT = 7.20
AISLE_IN = 8.00
XFADE_FRAMES = 10
FPS = 24
XFADE = XFADE_FRAMES / FPS  # 0.4167s
OFFSET = HANDS_OUT - XFADE


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


def make_bed(dest: Path, seconds: float) -> None:
    """Warm curious pad. ffmpeg lavfi — no drums, no trailer swell."""
    dest.parent.mkdir(parents=True, exist_ok=True)
    d = f"{seconds:.3f}"
    subprocess.run(
        [
            "ffmpeg", "-y",
            "-f", "lavfi", "-i", f"sine=frequency=98:duration={d}",
            "-f", "lavfi", "-i", f"sine=frequency=196:duration={d}",
            "-f", "lavfi", "-i", f"sine=frequency=246.94:duration={d}",
            "-f", "lavfi", "-i", f"sine=frequency=293.66:duration={d}",
            "-f", "lavfi", "-i", f"anoisesrc=color=brown:duration={d}:sample_rate=44100",
            "-filter_complex",
            "[0]volume=0.11,lowpass=f=280[bass];"
            "[1]volume=0.055,tremolo=f=0.12:d=0.32[g];"
            "[2]volume=0.04,tremolo=f=0.10:d=0.28[b];"
            "[3]volume=0.028,tremolo=f=0.11:d=0.22,lowpass=f=1200[d];"
            "[4]volume=0.018,lowpass=f=180,highpass=f=40[air];"
            "[bass][g][b][d][air]amix=inputs=5:duration=longest:normalize=0,"
            "alimiter=limit=0.12,aformat=sample_fmts=fltp:channel_layouts=stereo",
            "-ar", "48000", "-ac", "2",
            str(dest),
        ],
        check=True,
        capture_output=True,
    )


def make_metal(dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        [
            "ffmpeg", "-y",
            "-f", "lavfi",
            "-i",
            "aevalsrc=0.55*sin(2*PI*1640*t)*exp(-18*t)"
            "+0.28*sin(2*PI*2480*t)*exp(-22*t)"
            "+0.12*sin(2*PI*3920*t)*exp(-30*t):d=0.45:s=48000",
            "-ac", "2", str(dest),
        ],
        check=True,
        capture_output=True,
    )


def make_cloth(dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        [
            "ffmpeg", "-y",
            "-f", "lavfi",
            "-i", "anoisesrc=color=brown:duration=0.55:sample_rate=48000",
            "-af",
            "highpass=f=200,lowpass=f=1400,volume=0.35,"
            "afade=t=in:st=0:d=0.04,afade=t=out:st=0.28:d=0.27",
            "-ac", "2", str(dest),
        ],
        check=True,
        capture_output=True,
    )


def main() -> None:
    if not SRC.exists():
        raise SystemExit(f"missing v09 {SRC}")
    WORK.mkdir(parents=True, exist_ok=True)
    src_dur = probe_dur(SRC)
    pic_dur = HANDS_OUT + (src_dur - AISLE_IN) - XFADE
    bed = MUSIC / "hos_001_part01_curious_pad_v10.wav"
    metal = SFX_DIR / "metal_instrument_clink_v10.wav"
    cloth = SFX_DIR / "cloth_curtain_v10.wav"
    make_bed(bed, pic_dur + 1.0)
    make_metal(metal)
    make_cloth(cloth)

    # Picture: hands 0–7.20 xfade 10f into aisle @ 8.00. Audio mix after.
    fc = (
        f"[0:v]trim=0:{HANDS_OUT:.2f},setpts=PTS-STARTPTS,"
        f"fps={FPS},format=yuv420p,setsar=1[hands];"
        f"[0:v]trim=start={AISLE_IN:.2f},setpts=PTS-STARTPTS,"
        f"fps={FPS},format=yuv420p,setsar=1[aisle];"
        f"[hands][aisle]xfade=transition=fade:duration={XFADE:.6f}:offset={OFFSET:.6f}[v];"
        f"[0:a]atrim=0:{pic_dur:.6f},asetpts=PTS-STARTPTS,aformat=sample_fmts=fltp:channel_layouts=stereo[vo];"
        f"[1:a]atrim=0:{pic_dur:.6f},asetpts=PTS-STARTPTS,volume=0.07[bed];"
        f"[2:a]asplit=2[mraw1][mraw2];"
        f"[mraw1]adelay=900|900,volume=0.16[m1];"
        f"[mraw2]adelay=6400|6400,volume=0.14[m2];"
        f"[3:a]adelay=7000|7000,volume=0.10[c1];"
        f"[vo][bed][m1][m2][c1]amix=inputs=5:duration=first:dropout_transition=0:normalize=0[a]"
    )
    OUT.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        [
            "ffmpeg", "-y",
            "-i", str(SRC),
            "-i", str(bed),
            "-i", str(metal),
            "-i", str(cloth),
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
    out_sha = sha256(OUT)
    print(f"JOIN dissolve {XFADE_FRAMES} frames ({XFADE:.4f}s) offset={OFFSET:.4f}", flush=True)
    print(f"HANDS_OUT {HANDS_OUT} AISLE_IN {AISLE_IN}", flush=True)
    print(f"FOLLOWS 02_curtains / clean aisle (v09 from {AISLE_IN}s)", flush=True)
    print(f"SAVED {OUT}", flush=True)
    print(f"SIZE {OUT.stat().st_size}", flush=True)
    print(f"SHA256 {out_sha}", flush=True)
    print(f"DUR {probe_dur(OUT):.3f}", flush=True)
    print(f"BED {bed} ffmpeg lavfi warm pad", flush=True)
    print(f"FX metal@{0.9}s+{6.4}s cloth@{7.0}s", flush=True)
    ART.mkdir(parents=True, exist_ok=True)
    subprocess.run(["cp", "-f", str(OUT), str(ART / OUT.name)], check=True)
    if ICLOUD.parent.exists():
        ICLOUD.mkdir(parents=True, exist_ok=True)
        subprocess.run(["cp", "-f", str(OUT), str(ICLOUD / OUT.name)], check=False)


if __name__ == "__main__":
    main()
