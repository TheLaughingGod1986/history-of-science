#!/usr/bin/env python3
"""Offline splice cleans for v20 audio — NOT a v20 export.

Cleans the two v19 scratches:
  75.208  v16 mix → v09 knives tail (acrossfade, full s)
  76.300  knives-out → breath + locked shadow hook (acrossfade)

No picture. No tpad. No Flow. Do not ship this as v20.
"""
from __future__ import annotations

import hashlib
import subprocess
from pathlib import Path

PROJ = Path(__file__).resolve().parents[1]
V16 = PROJ / "09_Final-Export/hos_001_part01_rough_v16.mp4"
V16_SHA = "edb8a35287f968523eb2258f8c023603480ce13b9aa841164727190d9b74ce1d"
V09 = PROJ / "09_Final-Export/hos_001_part01_rough_v09.mp4"
HOOK = PROJ / "02_Voiceover/part01_shadow_hook_v01.wav"
BED = PROJ / "05_Music/hos_001_part01_ominous_ward_v14_norm.wav"
OUT = PROJ / "07_Edit-Project/_ready/part01_v20_audio_splices_clean.wav"

V16_OUT = 75.208
KNIVES_OUT = 76.300
XF_KNIVES = 0.080
XF_HOOK = 0.060
BREATH = 0.20
HOOK_DUR = 3.44
AFTER = 0.20


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
    for p in (V16, V09, HOOK, BED):
        if not p.exists():
            raise SystemExit(f"missing {p}")

    hook_in = KNIVES_OUT + BREATH
    hook_out = hook_in + HOOK_DUR
    total = hook_out + AFTER
    knives_start = V16_OUT - XF_KNIVES
    hook_delay_ms = int(round(hook_in * 1000))
    bed_from = KNIVES_OUT - XF_HOOK
    bed_len = total - bed_from
    bed_fade = 0.18

    fc = (
        f"[0:a]atrim=0:{V16_OUT:.4f},asetpts=PTS-STARTPTS,"
        f"aformat=sample_fmts=fltp:channel_layouts=stereo[v16];"
        f"[1:a]atrim=start={knives_start:.4f}:end={KNIVES_OUT:.4f},asetpts=PTS-STARTPTS,"
        f"aformat=sample_fmts=fltp:channel_layouts=stereo[kn];"
        f"[v16][kn]acrossfade=d={XF_KNIVES:.3f}:c1=tri:c2=tri[to_knives];"
        f"[2:a]aformat=sample_fmts=fltp:channel_layouts=stereo,"
        f"adelay={hook_delay_ms}|{hook_delay_ms}[hook];"
        f"[3:a]atrim=start={bed_from:.3f}:end={total:.3f},asetpts=PTS-STARTPTS,"
        f"volume=0.14,afade=t=in:st=0:d={XF_HOOK:.3f},"
        f"afade=t=out:st={bed_len - bed_fade:.3f}:d={bed_fade:.3f}[bed];"
        f"[hook][bed]amix=inputs=2:duration=longest:dropout_transition=0:normalize=0,"
        f"atrim=0:{total:.4f},asetpts=PTS-STARTPTS,"
        f"aformat=sample_fmts=fltp:channel_layouts=stereo[tail];"
        f"[to_knives][tail]acrossfade=d={XF_HOOK:.3f}:c1=tri:c2=tri,"
        f"atrim=0:{total:.4f},asetpts=PTS-STARTPTS[a]"
    )
    OUT.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        [
            "ffmpeg", "-y",
            "-i", str(V16),
            "-i", str(V09),
            "-i", str(HOOK),
            "-i", str(BED),
            "-filter_complex", fc,
            "-map", "[a]",
            "-c:a", "pcm_s24le", "-ar", "48000", "-ac", "2",
            str(OUT),
        ],
        check=True,
    )
    print(f"READY {OUT}", flush=True)
    print(f"SIZE {OUT.stat().st_size}", flush=True)
    print(f"SHA256 {sha256(OUT)}", flush=True)
    print(f"DUR {probe_dur(OUT):.3f}", flush=True)
    print(f"KNIVES_XF {knives_start:.3f}-{KNIVES_OUT:.3f} d={XF_KNIVES:.3f}", flush=True)
    print(f"HOOK_IN {hook_in:.3f} HOOK_OUT {hook_out:.3f} XF={XF_HOOK:.3f}", flush=True)
    print("NOT v20. Audio stem only.", flush=True)


if __name__ == "__main__":
    main()
