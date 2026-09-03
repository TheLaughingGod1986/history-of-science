#!/usr/bin/env python3
"""Part 01 v18 — recut from v16. Complete knives from v09 VO tail, then reused hook.

Do not use v17. Do not remint. Do not re-record if hook wav already has shadow.
"""
from __future__ import annotations

import hashlib
import subprocess
from pathlib import Path

PROJ = Path(__file__).resolve().parents[1]
SRC = PROJ / "09_Final-Export/hos_001_part01_rough_v16.mp4"
SRC_SHA = "edb8a35287f968523eb2258f8c023603480ce13b9aa841164727190d9b74ce1d"
# Same VO take as v16, longer — only used from the v16 cut onward.
VO_TAIL = PROJ / "09_Final-Export/hos_001_part01_rough_v09.mp4"
HOOK = PROJ / "02_Voiceover/part01_shadow_hook_v01.wav"
BED = PROJ / "05_Music/hos_001_part01_ominous_ward_v14_norm.wav"
OUT = PROJ / "09_Final-Export/hos_001_part01_rough_v18.mp4"
ART = Path(
    "/Users/benjaminoats/Library/Application Support/Cursor/"
    "AgentStores/cursor_agent_stores/bc-eb2a62e0-1899-43b0-9cd2-0b96209c2bd0/"
    "files/artifacts"
)
ICLOUD = Path(
    "/Users/benjaminoats/Library/Mobile Documents/com~apple~CloudDocs/HOS UAT"
)

# v16 picture/mix out. Energy is mid-fingers; knives is not on v16.
V16_OUT = 75.208
# Whisper + envelope on v09: "knives." 75.620–75.900, speech dies ~76.04.
KNIVES_OUT = 76.060
BREATH = 0.25
HOOK_DUR = 3.44  # full reused wav; shadow ends 3.040, energy to ~3.22
AFTER = 0.20  # pad after hook file so AAC cannot eat "shadow"


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
    if sha256(SRC) != SRC_SHA:
        raise SystemExit("v16 sha mismatch — abort")
    for p in (SRC, VO_TAIL, HOOK, BED):
        if not p.exists():
            raise SystemExit(f"missing {p}")

    hook_in = KNIVES_OUT + BREATH
    hook_out = hook_in + HOOK_DUR
    total = hook_out + AFTER
    hold = total - V16_OUT
    tail_delay_ms = int(round(V16_OUT * 1000))
    hook_delay_ms = int(round(hook_in * 1000))
    bed_fade = 0.18
    fc = (
        f"[0:v]tpad=stop_mode=clone:stop_duration={hold:.4f},format=yuv420p,setsar=1[v];"
        f"[0:a]atrim=0:{V16_OUT:.4f},asetpts=PTS-STARTPTS,"
        f"aformat=sample_fmts=fltp:channel_layouts=stereo[src];"
        f"[1:a]atrim=start={V16_OUT:.4f}:end={KNIVES_OUT:.4f},asetpts=PTS-STARTPTS,"
        f"aformat=sample_fmts=fltp:channel_layouts=stereo,"
        f"adelay={tail_delay_ms}|{tail_delay_ms}[knives];"
        f"[2:a]aformat=sample_fmts=fltp:channel_layouts=stereo,"
        f"adelay={hook_delay_ms}|{hook_delay_ms}[hook];"
        f"[3:a]atrim=start={V16_OUT:.3f}:end={total:.3f},asetpts=PTS-STARTPTS,"
        f"volume=0.14,afade=t=out:st={hold - bed_fade:.3f}:d={bed_fade:.3f},"
        f"adelay={tail_delay_ms}|{tail_delay_ms}[bed];"
        f"[src][knives][hook][bed]amix=inputs=4:duration=longest:"
        f"dropout_transition=0:normalize=0,"
        f"apad=pad_dur={AFTER:.3f},"
        f"atrim=0:{total:.4f},asetpts=PTS-STARTPTS[a]"
    )
    OUT.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        [
            "ffmpeg", "-y",
            "-i", str(SRC),
            "-i", str(VO_TAIL),
            "-i", str(HOOK),
            "-i", str(BED),
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
    print(f"KNIVES_OUT {KNIVES_OUT:.3f}", flush=True)
    print(f"HOOK_IN {hook_in:.3f} HOOK_OUT {hook_out:.3f}", flush=True)
    print(f"TOTAL {total:.3f} HOLD {hold:.3f}", flush=True)
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
