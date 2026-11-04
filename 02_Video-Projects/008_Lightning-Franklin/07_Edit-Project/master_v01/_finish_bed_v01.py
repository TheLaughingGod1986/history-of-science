#!/usr/bin/env python3
"""J1287: one gain pass on the shifted bed (same ElevenLabs take), then remux.

stem_bed_v01c is the shifted take, ducked under speech, with flat pauses.
This raises the speech floor toward 16 LU and lifts pauses of 0.8 s or longer.
No ElevenLabs call. Does not replace rough_v12 or the NAS desk copy.
"""
from __future__ import annotations

import json
import re
import subprocess as sp
import sys
import wave
from pathlib import Path

import numpy as np

OWB = Path("/Users/benjaminoats/YouTube/orbit-with-ben")
sys.path.insert(0, str(OWB / "scripts"))
import sfx_kit  # noqa: E402

FILM = Path("/Users/benjaminoats/YouTube/History Of Science/02_Video-Projects/008_Lightning-Franklin")
V12 = Path("/Users/benjaminoats/YouTube/hos-008-lightning/02_Video-Projects/008_Lightning-Franklin/07_Edit-Project/_precheck/rough_v12/hos_008_rough_v12.mp4")
NAS = Path("/Volumes/data/mac-mini-archive/scratch/J1287")
PACK = FILM / "07_Edit-Project/master_v01"
PRE = FILM / "07_Edit-Project/_precheck/master_v01"
VO = NAS / "stem_vo_v12.wav"
SFX = NAS / "stem_sfx_v01.wav"
SRC = NAS / "stem_bed_v01c.wav"
BED = NAS / "stem_bed_v01g.wav"
SR = 48000


def read_wav(p: Path) -> np.ndarray:
    with wave.open(str(p)) as w:
        x = np.frombuffer(w.readframes(w.getnframes()), dtype="<i2").astype(np.float32)
        x = x.reshape(-1, w.getnchannels()) / 32768.0
        if x.shape[1] == 1:
            x = np.repeat(x, 2, axis=1)
        return x


def write_wav(p: Path, x: np.ndarray) -> None:
    pcm = np.clip(x, -1, 1)
    with wave.open(str(p), "w") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes((pcm * 32767.0).astype("<i2").tobytes())


def runs(mask: np.ndarray):
    out, start = [], None
    for i, f in enumerate(list(mask) + [False]):
        if f and start is None:
            start = i
        elif not f and start is not None:
            out.append((start, i - start))
            start = None
    return out


def stats(vm, bm, vo_i, speaking):
    n = min(len(vm), len(bm), len(speaking))
    vm, bm, sp = vm[:n], bm[:n], speaking[:n]
    audible = sp & (bm > sfx_kit.SILENT)
    d = vm[audible] - bm[audible]
    pause = ~sp & (bm > sfx_kit.SILENT)
    long = np.zeros(n, dtype=bool)
    for s, ln in runs(~sp):
        if ln >= 8:
            long[s:s + ln] = True
    lp = long & (bm > sfx_kit.SILENT)
    breach = sp & (bm > sfx_kit.SILENT) & ((vm - bm) < 10)
    worst = cur = count = 0
    for f in breach:
        if f:
            cur += 1
            worst = max(worst, cur)
        else:
            if cur >= 3:
                count += 1
            cur = 0
    if cur >= 3:
        count += 1
    return {
        "speech_mean": round(float(d.mean()), 2),
        "p10": round(float(np.percentile(d, 10)), 2),
        "min": round(float(d.min()), 2),
        "under16": int((d < 16).sum()),
        "pause_under_i": round(float((vo_i - bm[pause]).mean()), 2),
        "long_pause_under_i": round(float((vo_i - bm[lp]).mean()), 2) if lp.any() else None,
        "breach_runs_0.3s": count,
        "worst_breach_frames": worst,
    }


def apply_frame_db(x: np.ndarray, frame_db: np.ndarray) -> np.ndarray:
    grid = np.arange(len(frame_db)) * 0.1
    t = np.arange(len(x)) / SR
    env = np.interp(t, grid, frame_db, left=float(frame_db[0]), right=float(frame_db[-1]))
    # 40 ms smoothing so a frame step does not click.
    win = int(0.04 * SR)
    if win > 1:
        k = np.ones(win) / win
        env = np.convolve(env, k, mode="same")
    return x * (10.0 ** (env / 20.0))[:, None]


def main() -> int:
    print("measure source", flush=True)
    vo_m, vo_i = sfx_kit.ebur128(VO)
    bed_m, _ = sfx_kit.ebur128(SRC)
    vm = np.array(vo_m, dtype=np.float64)
    bm = np.array(bed_m[: len(vm)], dtype=np.float64)
    n = min(len(vm), len(bm))
    vm, bm = vm[:n], bm[:n]
    speaking = (vm > sfx_kit.SILENT) & (vm >= vo_i - sfx_kit.SPEAKING_WITHIN)
    before = stats(vm, bm, vo_i, speaking)
    print("before", before, flush=True)

    gain = np.zeros(n, dtype=np.float64)
    d = vm - bm
    # Speech floor: where the bed sits closer than 16 LU, duck it. Cap 6 dB.
    floor = np.where(speaking & (d < 16), np.clip(16.2 - d, 0, 6), 0.0)
    gain -= floor
    # Long pauses (>=0.8 s): lift the inner 0.6 s so the 400 ms meter can hear it.
    for s, ln in runs(~speaking):
        if ln < 8:
            continue
        a = s + 2
        b = s + ln - 2
        if b <= a:
            a, b = s, s + ln
        # Target about 14 LU under the VO's integrated level, at most +7 dB.
        want = np.clip((vo_i - 14.0) - bm[a:b], 0, 7)
        gain[a:b] = np.maximum(gain[a:b], want)
    print(f"gain speech-duck frames {(gain < -0.2).sum()} pause-lift frames {(gain > 0.2).sum()} max {gain.max():.1f} min {gain.min():.1f}", flush=True)

    audio = read_wav(SRC)
    n_s = min(len(audio), int(n * 0.1 * SR) + SR)
    audio = audio[:n_s]
    write_wav(BED, apply_frame_db(audio, gain))

    bed_m, bed_i = sfx_kit.ebur128(BED)
    bm = np.array(bed_m[:n], dtype=np.float64)
    after = stats(vm, bm, vo_i, speaking)
    after["bed_integrated"] = round(float(bed_i), 2)
    after["vo_integrated"] = round(float(vo_i), 2)
    print("after", after, flush=True)
    (PACK / "bed_vs_vo.json").write_text(json.dumps({"source": "stem_bed_v01c", "out": "stem_bed_v01g", "before": before, "after": after}, indent=2) + "\n")
    ok = (
        16.0 <= after["speech_mean"] <= 21.5
        and after["min"] >= 11.5
        and after["breach_runs_0.3s"] == 0
        and after["long_pause_under_i"] is not None
        and after["long_pause_under_i"] <= after["speech_mean"] - 2.5
    )
    if not ok:
        raise SystemExit(f"bed window missed: {after}")

    level_json = PACK / "sfx_level.json"
    rc = sp.run(
        [sys.executable, str(OWB / "scripts/sfx_kit.py"), "level",
         "--vo", str(VO), "--sfx", str(SFX), "--bed", str(BED),
         "--minutes", "8.99", "--out", str(level_json)]
    ).returncode
    print(level_json.read_text(), flush=True)
    if rc:
        raise SystemExit(f"sfx level failed ({rc})")

    fc = "[0:a][1:a][2:a]amix=inputs=3:normalize=0:duration=first,alimiter=limit=0.89:level=false"
    r = sp.run(
        ["ffmpeg", "-hide_banner", "-i", str(VO), "-i", str(BED), "-i", str(SFX),
         "-filter_complex", fc + ",loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json[a]",
         "-map", "[a]", "-f", "null", "-"],
        capture_output=True, text=True,
    )
    if r.returncode:
        print(r.stderr[-1500:], flush=True)
        raise SystemExit("loudnorm pass 1 failed")
    st = json.loads(re.findall(r'\{[^{}]*"input_i"[^{}]*\}', r.stderr, re.S)[-1])
    (PRE / "loudnorm_v01g.json").write_text(json.dumps(st, indent=2) + "\n")
    norm = (
        f"loudnorm=I=-14:TP=-1.5:LRA=11:measured_I={st['input_i']}:measured_TP={st['input_tp']}:"
        f"measured_LRA={st['input_lra']}:measured_thresh={st['input_thresh']}:offset={st['target_offset']}:linear=true"
    )
    audio_out = NAS / "audio_master_v01g.m4a"
    sp.run(
        ["ffmpeg", "-y", "-v", "error", "-i", str(VO), "-i", str(BED), "-i", str(SFX),
         "-filter_complex", fc + "," + norm + "[a]", "-map", "[a]", "-ar", str(SR),
         "-c:a", "aac", "-b:a", "256k", str(audio_out)],
        check=True,
    )
    out = NAS / "hos_008_master_v01g.mp4"
    sp.run(
        ["ffmpeg", "-y", "-v", "error", "-i", str(V12), "-i", str(audio_out),
         "-map", "0:v:0", "-map", "1:a:0", "-c:v", "copy", "-c:a", "copy",
         "-movflags", "+faststart", str(out)],
        check=True,
    )
    print("master", out, out.stat().st_size, flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
