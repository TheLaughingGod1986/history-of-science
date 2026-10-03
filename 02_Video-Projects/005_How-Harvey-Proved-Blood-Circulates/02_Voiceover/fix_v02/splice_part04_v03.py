#!/usr/bin/env python3
"""HOS 005 Part 04 VO v03 (= v02 with no whole-file gain): swap ONE sentence (desk 5952762841).
v02 normalised the WHOLE file to -2 dB peak because the new take peaked -0.8 dB, which dropped Part 04 by 1.4 LU.
v03 instead peak-limits only the new sentence (5 ms look-around gain envelope) to the v01 file peak, so
every v01 sample outside the sentence is untouched and loudness matches v01.
Old (v01 13.50-16.24 s): "Below the band, the hand goes pale and cold."
New: "Below the band, the pulse is gone, and slowly the hand grows cool." (take a, voiced in context,
same voice/model/settings_for_part(4)). Everything before stays sample-identical; everything after is
the v01 audio shifted later by DELTA. Pauses kept as in v01 (0.72 s before, 0.58 s after). RMS-matched
to the old sentence; 10 ms fades. Never overwrites."""
import hashlib, json, subprocess
from pathlib import Path
import numpy as np
HERE = Path(__file__).resolve().parent; VO = HERE.parent
SR = 44100
OLD_S, OLD_E, NEXT_S = 13.50, 16.24, 16.82
CUT_A, CUT_B = 13.30, 16.53
TAKE, T_S, T_E = "a", 4.789, 9.306          # speech span of take a (silencedetect -45 dB)
def dec(p):
    return np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", str(p), "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"],
                                        capture_output=True, check=True).stdout, dtype=np.float32).copy()
def srms(x):
    fr = x[: len(x) // 441 * 441].reshape(-1, 441); db = 20 * np.log10(np.sqrt((fr ** 2).mean(1)) + 1e-12)
    s = fr[db > -45]; return float(np.sqrt((s ** 2).mean()))
base = dec(VO / "part04_the_tied_arm_v01.mp3")
take = dec(HERE / f"p04_pulse_ctx_{TAKE}.mp3")
seg = take[int((T_S - 0.02) * SR): int((T_E + 0.03) * SR)].copy()
seg *= srms(base[int(OLD_S * SR): int(OLD_E * SR)]) / srms(seg)
f = int(0.01 * SR); r = np.linspace(0, 1, f); seg[:f] *= r; seg[-f:] *= r[::-1]
pre = np.zeros(int(round((OLD_S - 0.02 - CUT_A) * SR)), np.float32)
post = np.zeros(int(round((CUT_B - OLD_E - 0.03) * SR)), np.float32)
out = np.concatenate([base[: int(CUT_A * SR)], pre, seg, post, base[int(CUT_B * SR):]])
delta = (len(out) - len(base)) / SR
ceil = float(np.abs(base).max())
need = np.minimum(1.0, ceil / np.maximum(np.abs(seg), 1e-9))
w = int(0.005 * SR)
env = np.array([need[max(0, i - w): i + w + 1].min() for i in range(len(need))]) if (need < 1).any() else need
k = np.ones(w) / w; env = np.minimum(env, np.convolve(env, k, mode="same")); seg = seg * env
LIMITED = int((need < 1).sum())
out = np.concatenate([base[: int(CUT_A * SR)], pre, seg, post, base[int(CUT_B * SR):]])
mp3 = VO / "part04_the_tied_arm_v03.mp3"
for o, args in ((mp3, ["-c:a", "libmp3lame", "-b:a", "320k"]), (mp3.with_suffix(".wav"), ["-c:a", "pcm_s16le", "-ar", "48000", "-ac", "2"])):
    if o.exists(): raise SystemExit(f"STOP: {o.name} exists")
    subprocess.run(["ffmpeg", "-v", "error", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-", *args, str(o)],
                   input=out.astype(np.float32).tobytes(), check=True)
txt = (VO / "part04_the_tied_arm_v01.txt").read_text().replace(
    "Below the band, the hand goes pale and cold.", "Below the band, the pulse is gone, and slowly the hand grows cool.")
(VO / "part04_the_tied_arm_v03.txt").write_text(txt)
sha = hashlib.sha256(mp3.read_bytes()).hexdigest()
dur = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(mp3)], text=True))
meta = {"file": mp3.name, "sha256": sha, "duration_s": round(dur, 3), "from": "part04_the_tied_arm_v01.mp3",
        "take": f"fix_v02/p04_pulse_ctx_{TAKE}.mp3", "take_span_s": [T_S, T_E], "new_sentence_part_s": [OLD_S, round(OLD_S + T_E - T_S, 3)],
        "shift_after_s": round(delta, 3), "shift_from_part_s": NEXT_S, "peak_db": round(float(20*np.log10(np.abs(out).max())), 2), "limited_samples": LIMITED, "whole_file_gain_db": 0.0,
        "desk": "PR #180 comments 5952762841 / 5953047660"}
(HERE / "VO_FIX_v03.json").write_text(json.dumps(meta, indent=2) + "\n"); print(json.dumps(meta, indent=1))
