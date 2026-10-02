#!/usr/bin/env python3
"""HOS 005 Shorts VO finish v01: the long's step 1 only (STUDIO_PLAYBOOK §4).

Lead-in trimmed to 0.05 s, pauses over 0.6 s cut to 0.6 s, tail to 0.25 s, peak set to −2 dB (uniform gain).
No atempo. The ElevenLabs character alignment is remapped through the same cuts.
Writes vo_v01/hos_005_<id>_vo_v01_fin.wav + _fin_align.json and VO_SHORTS_FINISH_v01.json.
"""
from __future__ import annotations

import hashlib
import json
import re
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
VO = HERE / "vo_v01"
TAKES = {"s01_the_sum": "a", "s02_the_tied_arm": "a", "s03_never_saw": "b"}
MAX_PAUSE, LEAD, TAIL, PEAK = 0.6, 0.05, 0.25, -2.0


def silences(wav: Path, dur: float) -> list[tuple[float, float]]:
    err = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(wav), "-af",
                          "silencedetect=n=-45dB:d=0.05", "-f", "null", "-"], capture_output=True, text=True).stderr
    st = [float(x) for x in re.findall(r"silence_start: (-?[\d.]+)", err)]
    en = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", err)]
    if len(en) < len(st):
        en.append(dur)
    return [(max(0.0, a), b) for a, b in zip(st, en)]


def dur(p: Path) -> float:
    return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                          "-of", "csv=p=0", str(p)], text=True))


def peak(p: Path) -> float:
    err = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(p), "-af", "volumedetect", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    return float(re.search(r"max_volume: (-?[\d.]+)", err).group(1))


def finish(sid: str, take: str) -> dict:
    src = VO / f"hos_005_{sid}_vo_v01{take}.wav"
    al = json.loads((VO / f"hos_005_{sid}_vo_v01{take}_align.json").read_text())
    d = dur(src)
    keep: list[tuple[float, float]] = []  # source spans to keep
    cur = 0.0
    for a, b in silences(src, d):
        if a <= 0.01:
            cur = max(0.0, b - LEAD)
            continue
        if b >= d - 0.01:
            keep.append((cur, min(d, a + TAIL)))
            cur = d
            break
        if b - a > MAX_PAUSE:
            keep.append((cur, a + MAX_PAUSE / 2))
            cur = b - MAX_PAUSE / 2
    if cur < d:
        keep.append((cur, d))

    def remap(t: float) -> float:
        out = 0.0
        for a, b in keep:
            if t <= a:
                return out
            if t <= b:
                return out + (t - a)
            out += b - a
        return out

    gain = PEAK - peak(src)
    parts = "".join(f"[0:a]atrim={a:.4f}:{b:.4f},asetpts=PTS-STARTPTS[s{i}];" for i, (a, b) in enumerate(keep))
    fc = parts + "".join(f"[s{i}]" for i in range(len(keep))) + f"concat=n={len(keep)}:v=0:a=1,volume={gain:.3f}dB[a]"
    out = VO / f"hos_005_{sid}_vo_v01_fin.wav"
    subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", str(src), "-filter_complex", fc,
                    "-map", "[a]", "-c:a", "pcm_s16le", "-ar", "48000", "-ac", "2", str(out)], check=True)
    al2 = dict(al)
    al2["character_start_times_seconds"] = [round(remap(t), 4) for t in al["character_start_times_seconds"]]
    al2["character_end_times_seconds"] = [round(remap(t), 4) for t in al["character_end_times_seconds"]]
    (VO / f"hos_005_{sid}_vo_v01_fin_align.json").write_text(json.dumps(al2, indent=1))
    rec = {"id": sid, "take": take, "source": src.name, "source_s": round(d, 3), "finished": out.name,
           "finished_s": round(dur(out), 3), "removed_s": round(d - dur(out), 3), "gain_db": round(gain, 2),
           "peak_db": peak(out), "sha256": hashlib.sha256(out.read_bytes()).hexdigest()}
    print(f"FIN {sid} take {take}: {rec['source_s']} → {rec['finished_s']} s (−{rec['removed_s']}), peak {rec['peak_db']}")
    return rec


if __name__ == "__main__":
    recs = [finish(s, t) for s, t in TAKES.items()]
    (VO / "VO_SHORTS_FINISH_v01.json").write_text(json.dumps(
        {"rule": "pauses > 0.6 s → 0.6 s, lead 0.05 s, tail 0.25 s, peak −2 dB, no atempo", "shorts": recs},
        indent=2) + "\n")
