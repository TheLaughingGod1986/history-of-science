#!/usr/bin/env python3
"""HOS 006 VO v02 finish (same v01 raw takes, adds the Part 02 "Picture yourself" fix): splice regenerated sentences, trim pauses, set peak, build the listen file.

STUDIO_PLAYBOOK.md §4: a fix replaces one whole sentence (same words, new take); pauses over
0.6 s inside a part are trimmed to 0.6 s; part joins are added after trimming; no atempo here.
Needs numpy (run with the vo_check venv). Never overwrites a finished take.

  python3 _finish_vo_v02.py            # all parts + listen file
"""
from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
SR = 44100
FRAME = 441  # 10 ms
SILENT_DB = -45.0
MAX_PAUSE = 0.6
PEAK_DB = -2.0
JOIN_S = 1.0
SLUGS = {1: "plants_eat_soil", 2: "five_years_and_two_ounces", 3: "the_air_that_mint_repaired",
         4: "bubbles_in_the_sunlight", 5: "carbon_from_the_sky"}
FIXES = {2: [("Picture yourself in that garden.", "_qa_picture_yourself_v01c.mp3"),
             ("So, he wrote, the wood, the bark and the roots had come from water alone.", "_qa_had_come_v01b.mp3")],
         3: [("Then he tried air that mice had made stale with their breathing.", "_qa_mice_had_made_v01d.mp3")]}


def load(path: Path) -> np.ndarray:
    raw = subprocess.check_output(["ffmpeg", "-v", "error", "-i", str(path), "-ac", "1", "-ar", str(SR),
                                   "-f", "f32le", "-"])
    return np.frombuffer(raw, dtype=np.float32).copy()


def save(x: np.ndarray, mp3: Path) -> None:
    for out, args in ((mp3, ["-c:a", "libmp3lame", "-b:a", "192k"]),
                      (mp3.with_suffix(".wav"), ["-c:a", "pcm_s16le", "-ar", "48000", "-ac", "2"])):
        if out.exists():
            raise SystemExit(f"STOP: {out.name} exists; versions only go up")
        subprocess.run(["ffmpeg", "-v", "error", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-", *args,
                        str(out)], input=x.astype(np.float32).tobytes(), check=True)


def frame_db(x: np.ndarray) -> np.ndarray:
    n = len(x) // FRAME
    rms = np.sqrt(np.mean(x[: n * FRAME].reshape(n, FRAME) ** 2, axis=1) + 1e-12)
    return 20 * np.log10(rms)


def speech_rms(x: np.ndarray) -> float:
    db = frame_db(x)
    n = len(db)
    fr = x[: n * FRAME].reshape(n, FRAME)[db > SILENT_DB]
    return float(np.sqrt(np.mean(fr ** 2))) if len(fr) else 1e-6


def trim_edges(x: np.ndarray) -> np.ndarray:
    loud = np.where(frame_db(x) > SILENT_DB)[0]
    return x[max(loud[0] - 2, 0) * FRAME: (loud[-1] + 3) * FRAME]


def splice(x: np.ndarray, align: dict, text: str, sentence: str, new: np.ndarray) -> np.ndarray:
    chars = "".join(align["characters"])
    st, en = align["character_start_times_seconds"], align["character_end_times_seconds"]
    i = chars.index(sentence)
    j = i + len(sentence) - 1
    p = i - 1
    while p >= 0 and chars[p].isspace():
        p -= 1
    q = j + 1
    while q < len(chars) and chars[q].isspace():
        q += 1
    a = 0.0 if p < 0 else (en[p] + st[i]) / 2
    b = len(x) / SR if q >= len(chars) else (en[j] + st[q]) / 2
    a_i, b_i = int(a * SR), int(b * SR)
    old = x[a_i:b_i]
    new = trim_edges(new) * (speech_rms(old) / speech_rms(new))
    lead = np.zeros(int(max(st[i] - a, 0.05) * SR), dtype=np.float32) if p >= 0 else np.zeros(int(0.1 * SR), np.float32)
    tail = np.zeros(int(max(b - en[j], 0.15) * SR), dtype=np.float32)
    print(f"   splice '{sentence[:40]}' {a:.2f}–{b:.2f}s → new {len(new) / SR:.2f}s", flush=True)
    return np.concatenate([x[:a_i], lead, new.astype(np.float32), tail, x[b_i:]])


def trim_pauses(x: np.ndarray) -> tuple[np.ndarray, float]:
    db = frame_db(x)
    silent = db <= SILENT_DB
    keep = np.ones(len(x), dtype=bool)
    half = int(MAX_PAUSE / 2 * SR / FRAME)
    k = 0
    while k < len(silent):
        if silent[k]:
            e = k
            while e < len(silent) and silent[e]:
                e += 1
            if (e - k) * FRAME / SR > MAX_PAUSE:
                keep[(k + half) * FRAME:(e - half) * FRAME] = False
            k = e
        else:
            k += 1
    return x[keep], (len(x) - keep.sum()) / SR


def set_peak(x: np.ndarray) -> np.ndarray:
    peak = 20 * np.log10(np.max(np.abs(x)) + 1e-12)
    return x * (10 ** ((PEAK_DB - peak) / 20)) if peak > PEAK_DB else x


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    parts, recs, t = [], [], 0.0
    for n, slug in SLUGS.items():
        final = HERE / f"part{n:02d}_{slug}_v02.mp3"
        raw = HERE / f"part{n:02d}_{slug}_v01_raw.mp3"
        if not raw.exists():
            final.rename(raw)
            final.with_name(final.stem + "_align.json").rename(raw.with_name(raw.stem + "_align.json"))
        x = load(raw)
        align = json.loads(raw.with_name(raw.stem + "_align.json").read_text())
        text = (HERE / f"part{n:02d}_{slug}_v01.txt").read_text(encoding="utf-8").strip()
        print(f"part {n:02d}: raw {len(x) / SR:.2f}s", flush=True)
        for sentence, qa in sorted(FIXES.get(n, []), key=lambda f: -text.index(f[0])):
            x = splice(x, align, text, sentence, load(HERE / qa))
        x, cut = trim_pauses(x)
        x = set_peak(x)
        save(x, final)
        dur = len(x) / SR
        recs.append({"part": n, "file": final.name, "raw": raw.name, "raw_sha256": sha256(raw),
                     "fixes": [qa for _, qa in FIXES.get(n, [])], "pause_trim_s": round(cut, 2),
                     "start_s": round(t, 2), "duration_s": round(dur, 2), "sha256": sha256(final)})
        print(f"   trimmed {cut:.2f}s of pauses → {dur:.2f}s, starts {t:.2f}s in the listen file", flush=True)
        parts.append(x)
        t += dur + JOIN_S
    gap = np.zeros(int(JOIN_S * SR), dtype=np.float32)
    full = np.concatenate([seg for x in parts for seg in (x, gap)][:-1])
    listen = HERE / "hos_006_vo_all_parts_listen_v02.mp3"
    save(full, listen)
    out = {"listen": listen.name, "listen_sha256": sha256(listen), "duration_s": round(len(full) / SR, 2),
           "join_s": JOIN_S, "max_pause_s": MAX_PAUSE, "peak_db": PEAK_DB, "atempo": None, "parts": recs}
    (HERE / "VO_FINISH_v02.json").write_text(json.dumps(out, indent=2) + "\n")
    m, s = divmod(len(full) / SR, 60)
    print(f"LISTEN {listen.name} {int(m)}:{s:05.2f} sha256 {out['listen_sha256']}", flush=True)


if __name__ == "__main__":
    main()
