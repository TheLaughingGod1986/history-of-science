#!/usr/bin/env python3
"""Part 01 v20 — v16 before aisle + reminted walk + ready splice-clean wav.

Picture: v16 0–AISLE_IN, then two-take aisle stitch through hook out.
Audio: locked splice-clean wav (knives s + shadow hook, 75.208 / 76.300 acrossfades).
Keep open card + four early labels (baked on v16). Re-overlay LIVING CLOUD
on the new aisle only. No PASS. STOP for UAT.
"""
from __future__ import annotations

import hashlib
import subprocess
from pathlib import Path

PROJ = Path(__file__).resolve().parents[1]
V16 = PROJ / "09_Final-Export/hos_001_part01_rough_v16.mp4"
V16_SHA = "edb8a35287f968523eb2258f8c023603480ce13b9aa841164727190d9b74ce1d"
WAV = PROJ / "07_Edit-Project/_ready/part01_v20_audio_splices_clean.wav"
WAV_SHA = "dbce69df9d98b74879681ae88e8af3fa2632696160580d2ced5b70f6760f8623"
LABEL = PROJ / "06_Sound-Effects/v15_labels/living_cloud.png"
T1 = PROJ / "04_Generated-Clips/part01/raw/v20_aisle/aisle_walk_t1.mp4"
T2 = PROJ / "04_Generated-Clips/part01/raw/v20_aisle/aisle_walk_t2.mp4"
OUT = PROJ / "09_Final-Export/hos_001_part01_rough_v20.mp4"
ART = Path(
    "/Users/benjaminoats/Library/Application Support/Cursor/"
    "AgentStores/cursor_agent_stores/bc-eb2a62e0-1899-43b0-9cd2-0b96209c2bd0/"
    "files/artifacts"
)
ICLOUD = Path(
    "/Users/benjaminoats/Library/Mobile Documents/com~apple~CloudDocs/HOS UAT"
)

# Measured aisle-in on v16 (instruments→aisle dissolve owns the frame ~67.50).
AISLE_IN = 67.50
TOTAL = 80.140
XFADE_PIC = 0.40
FADE = 14 / 24
LABEL_OUT = 71.22


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
    if sha256(V16) != V16_SHA:
        raise SystemExit("v16 sha mismatch — abort")
    if sha256(WAV) != WAV_SHA:
        raise SystemExit("splice wav sha mismatch — abort")
    for p in (V16, WAV, LABEL, T1, T2):
        if not p.exists():
            raise SystemExit(f"missing {p}")
    wav_dur = probe_dur(WAV)
    if abs(wav_dur - TOTAL) > 0.02:
        raise SystemExit(f"wav duration {wav_dur:.3f} != {TOTAL:.3f}")

    d1 = probe_dur(T1)
    d2 = probe_dur(T2)
    stitched = d1 + d2 - XFADE_PIC
    need = TOTAL - AISLE_IN
    if stitched + 0.05 < need:
        raise SystemExit(
            f"aisle motion short: have {stitched:.3f}s need {need:.3f}s — do not pad"
        )

    label_hold = LABEL_OUT - AISLE_IN
    fade_out = min(FADE, label_hold / 3)
    fc = (
        f"[0:v]trim=0:{AISLE_IN:.4f},setpts=PTS-STARTPTS,fps=24,format=yuv420p[pre];"
        f"[1:v]fps=24,format=yuv420p,setsar=1[t1];"
        f"[2:v]fps=24,format=yuv420p,setsar=1[t2];"
        f"[t1][t2]xfade=transition=fade:duration={XFADE_PIC:.3f}:offset={d1 - XFADE_PIC:.4f}[walk];"
        f"[walk]trim=0:{need:.4f},setpts=PTS-STARTPTS[aisle];"
        f"[pre][aisle]concat=n=2:v=1:a=0[pic];"
        f"[3:v]format=rgba,"
        f"fade=t=in:st=0:d=0.08:alpha=1,"
        f"fade=t=out:st={label_hold - fade_out:.3f}:d={fade_out:.3f}:alpha=1,"
        f"setpts=PTS+{AISLE_IN:.3f}/TB[lab];"
        f"[pic][lab]overlay=0:0:eof_action=pass,format=yuv420p,setsar=1[v];"
        f"[4:a]aformat=sample_fmts=fltp:channel_layouts=stereo,"
        f"atrim=0:{TOTAL:.4f},asetpts=PTS-STARTPTS[a]"
    )

    OUT.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        [
            "ffmpeg", "-y",
            "-i", str(V16),
            "-i", str(T1),
            "-i", str(T2),
            "-loop", "1", "-t", f"{label_hold:.4f}", "-i", str(LABEL),
            "-i", str(WAV),
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
    print(f"AISLE_IN {AISLE_IN:.3f}", flush=True)
    print(f"STITCH {d1:.3f}+{d2:.3f}-xfade {stitched:.3f} used {need:.3f}", flush=True)
    print(f"AUDIO ready_wav {WAV_SHA[:12]}…", flush=True)
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
