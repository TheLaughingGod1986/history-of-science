#!/usr/bin/env python3
"""Part 01 v17 — splice shadow hook onto locked v16. No remint. No new key I/O."""
from __future__ import annotations

import hashlib
import subprocess
from pathlib import Path

PROJ = Path(__file__).resolve().parents[1]
SRC = PROJ / "09_Final-Export/hos_001_part01_rough_v16.mp4"
SRC_SHA = "edb8a35287f968523eb2258f8c023603480ce13b9aa841164727190d9b74ce1d"
HOOK = PROJ / "02_Voiceover/part01_shadow_hook_v01.wav"
BED = PROJ / "05_Music/hos_001_part01_ominous_ward_v14_norm.wav"
OUT = PROJ / "09_Final-Export/hos_001_part01_rough_v17.mp4"
ART = Path(
    "/Users/benjaminoats/Library/Application Support/Cursor/"
    "AgentStores/cursor_agent_stores/bc-eb2a62e0-1899-43b0-9cd2-0b96209c2bd0/"
    "files/artifacts"
)
ICLOUD = Path(
    "/Users/benjaminoats/Library/Mobile Documents/com~apple~CloudDocs/HOS UAT"
)
# v16 tape out. New VO starts immediately after knives / tape end.
SPLICE = 75.208
AIR = 0.08
# Whisper: "shadow?" ends 3.040; silence from 3.254. Trim for hard stop.
HOOK_KEEP = 3.12


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
    if not SRC.exists():
        raise SystemExit(f"missing {SRC}")
    got = sha256(SRC)
    if got != SRC_SHA:
        raise SystemExit(f"v16 sha mismatch: {got}")
    if not HOOK.exists():
        raise SystemExit(f"missing hook {HOOK}")
    if not BED.exists():
        raise SystemExit(f"missing bed {BED}")

    vo_in = SPLICE + AIR
    hold = AIR + HOOK_KEEP
    total = SPLICE + hold
    hook_delay_ms = int(round(vo_in * 1000))
    bed_delay_ms = int(round(SPLICE * 1000))
    fade = 0.12
    fc = (
        f"[0:v]tpad=stop_mode=clone:stop_duration={hold:.4f},format=yuv420p,setsar=1[v];"
        f"[0:a]aformat=sample_fmts=fltp:channel_layouts=stereo[src];"
        f"[1:a]atrim=0:{HOOK_KEEP:.3f},asetpts=PTS-STARTPTS,"
        f"aformat=sample_fmts=fltp:channel_layouts=stereo,"
        f"adelay={hook_delay_ms}|{hook_delay_ms}[hook];"
        f"[2:a]atrim=start={SPLICE:.3f}:end={SPLICE + hold:.3f},asetpts=PTS-STARTPTS,"
        f"volume=0.14,afade=t=out:st={hold - fade:.3f}:d={fade:.3f},"
        f"adelay={bed_delay_ms}|{bed_delay_ms}[bed];"
        f"[src][hook][bed]amix=inputs=3:duration=longest:dropout_transition=0:normalize=0,"
        f"atrim=0:{total:.4f},asetpts=PTS-STARTPTS,"
        f"afade=t=out:st={total - 0.012:.4f}:d=0.012[a]"
    )
    OUT.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        [
            "ffmpeg", "-y",
            "-i", str(SRC),
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
    print(f"SPLICE_IN {vo_in:.3f}", flush=True)
    print(f"HOLD {hold:.3f} TOTAL {total:.3f}", flush=True)
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
