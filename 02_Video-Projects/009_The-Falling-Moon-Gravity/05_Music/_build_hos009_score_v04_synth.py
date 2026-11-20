#!/usr/bin/env python3
"""J3239 — HOS 009 full-runtime warm score v04, £0 own synthesis.

One continuous D-minor chamber bed from 0.00 to 535.33 s. Deterministic
NumPy only: low-harmonic pads and a soft wooden harp. No samples, no
soundfonts, no Karplus-Strong, no network, no ElevenLabs. Does not touch
04_Audio/tools. Does not claim an ear-review pass or a score acceptance.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess as sp
import sys
import wave
from pathlib import Path

import numpy as np

SR = 48000
TOTAL = 535.33
VO_END = 518.40
REF_END = 526.0
TAIL_SILENCE = 533.0
TEACH_SHA = "4c1f0a17364ad5ba96fdd2d42730b2f857d19017fab52b221701bd4e15d07bb1"

OWB = Path("/Users/benjaminoats/YouTube/orbit-with-ben")
HOS = Path("/Users/benjaminoats/YouTube/History Of Science")
FILM = HOS / "02_Video-Projects/009_The-Falling-Moon-Gravity"
MUSIC = FILM / "05_Music"
REVIEW = MUSIC / "audio_review_v04_synth"
VO = FILM / "02_Voiceover"
NAS = Path(
    "/Volumes/data/studio-live/History Of Science/02_Video-Projects/"
    "009_The-Falling-Moon-Gravity/05_Music"
)
UAT_LOCAL = Path("/Volumes/MiniWork/scratch/j2664/uat_materialized")
AUDIO_EXT = {".mp3", ".wav", ".m4a", ".aac", ".flac"}
BED_NAME = "hos_009_score_v04_synth.wav"

# Chapter cards. Harmony changes every 4 bars in awe and measured explain,
# every 2 bars under the cannon pulse. Basses move; nothing holds one drone.
PARTS = (
    {"part": 1, "title": "The Falling Moon", "slug": "the_falling_moon",
     "start": 0.00, "end": 84.44, "mood": "awe", "bpm": 62, "bars": 4},
    {"part": 2, "title": "An Apple in a Plague Year", "slug": "an_apple_in_a_plague_year",
     "start": 84.44, "end": 176.78, "mood": "awe", "bpm": 62, "bars": 4},
    {"part": 3, "title": "The Cannon on the Mountain", "slug": "the_cannon_on_the_mountain",
     "start": 176.78, "end": 260.16, "mood": "explain", "bpm": 67, "bars": 2},
    {"part": 4, "title": "The Moon Test", "slug": "the_moon_test",
     "start": 260.16, "end": 393.86, "mood": "explain", "bpm": 67, "bars": 4},
    {"part": 5, "title": "Falling Around the World", "slug": "falling_around_the_world",
     "start": 393.86, "end": 535.33, "mood": "awe", "bpm": 62, "bars": 4},
)

# D minor / Dorian / F colour. Distinct from HOS 006 (G/D major) and HOS 007
# (G major / E minor). Every entry is (bass, third-or-colour, fifth, top).
CHORDS = {
    1: [(50, 53, 57, 62), (43, 46, 50, 55), (46, 50, 53, 58),
        (41, 45, 48, 53), (45, 48, 52, 57), (48, 52, 55, 60)],
    2: [(41, 48, 53, 57), (50, 53, 57, 60), (48, 52, 55, 60),
        (46, 50, 53, 58), (43, 46, 50, 55), (45, 52, 57, 60)],
    3: [(50, 53, 57, 62), (45, 52, 57, 60), (46, 50, 53, 58),
        (41, 45, 48, 53), (43, 46, 50, 55), (48, 52, 55, 60),
        (50, 57, 60, 62), (46, 53, 58, 62), (45, 48, 52, 57),
        (41, 48, 53, 57), (43, 50, 55, 58), (48, 55, 60, 62)],
    4: [(50, 53, 57, 62), (45, 48, 52, 57), (43, 46, 50, 55),
        (46, 50, 53, 58), (41, 45, 48, 53), (48, 52, 55, 60),
        (50, 53, 57, 60), (46, 53, 55, 58), (45, 52, 57, 60),
        (43, 50, 55, 58)],
    5: [(50, 53, 57, 62), (41, 45, 48, 53), (46, 50, 53, 58),
        (48, 52, 55, 60), (43, 46, 50, 55), (45, 48, 52, 57),
        (50, 53, 57, 60), (46, 50, 53, 57), (41, 48, 53, 57)],
}
# Slow inner voice, one note a bar. A modal turn, not a borrowed tune.
MELODY = (62, 60, 58, 57, 55, 53, 55, 57, 58, 60, 62, 64, 62, 60, 58, 57)

PROMPT = (
    "Original full-runtime instrumental chamber score for HOS 009 Why Doesn't the Moon "
    "Fall to Earth. Warm D-minor (A4=440) low-harmonic viol pads and a soft wooden harp, "
    "harmony moving every two to four bars, one continuous texture from the first sample "
    "through the last chapter. Calm wonder, a warmer orchard colour, a light rhythmic "
    "explain pulse, then a spacious return and a slow ending. Leave space for British narration.\n"
    "Pace: 60-68 BPM.\n"
    "NOT any earlier HOS or Orbit bed, hos_009_teach_v01, hos_009_wonder_v01, "
    "hos_009_wonder_v02, hos_009_wonder_v03_synth, hos_009_score_joined_v01, "
    "hos_009_score_joined_v02, hos_009_score_joined_v03, trees006_score_bed_v01, "
    "vaccine_score_bed_v01, jupiter-music.mp3, a static bass drone, reed-organ buzz, "
    "metallic chiptune plucks, a synth-to-recording splice, cosmic shimmer, "
    "piano space-documentary music, solo woodwind workshop waltz, borrowed melody, "
    "named-composer imitation, heroic brass, horror, vocals, lyrics, pop drums, EDM "
    "or comedy stings."
)

LOCKS = {
    "hos_009_teach_v01.mp3": TEACH_SHA,
    "hos_009_wonder_v01.mp3": "95dfe11d7c21c9347e9b962ef2f9ecd35116f2fce60df6f123578c11a1debaf0",
    "hos_009_wonder_v02.mp3": "b38ae8922e8d633b9f085a8bb9634c96d889a9293fcab277f7a3a23f4839d148",
    "hos_009_score_joined_v01.wav": "d7f5bf3d7553d7c611a913e93602b8ec83419821059294ddeaee32269a4f9572",
    "hos_009_score_joined_v02.wav": "6fc8628a96b8267eaf5be6c19d7e30d9e473eb86c886ee3106c3219b375b1f68",
    "VO_TAKES_KEEP.json": "530743c507af8d5f9049179d4e9d380b5c1b8aca4f180ada133d0b673f5925e0",
    "VO_RETIME_v01.json": "75a2e7afa1d822b04371511c81a52082e1b80713b0e59711702cfd05fe45a972",
}


def log(msg: str) -> None:
    print(msg, flush=True)


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for blk in iter(lambda: fh.read(1 << 20), b""):
            h.update(blk)
    return h.hexdigest()


def midi_hz(m: float) -> float:
    return 440.0 * (2.0 ** ((float(m) - 69.0) / 12.0))


def unit(i: int, salt: int) -> float:
    """Deterministic value in [-1, 1]. No RNG, so a rerun is the same bed."""
    x = (i * 2246822519 + salt * 3266489917 + 32391120) & 0xFFFFFFFF
    return (x / 0xFFFFFFFF) * 2.0 - 1.0


def write_wav(path: Path, audio: np.ndarray) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    pcm = np.clip(np.asarray(audio, dtype=np.float64), -1.0, 1.0)
    frames = (pcm * 32767.0).astype("<i2")
    with wave.open(str(path), "wb") as w:
        w.setnchannels(2 if frames.ndim == 2 else 1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(np.ascontiguousarray(frames).tobytes())


def load_audio(path: Path, seconds: float | None = None) -> np.ndarray:
    cmd = ["ffmpeg", "-v", "error", "-i", str(path)]
    if seconds is not None:
        cmd += ["-t", f"{seconds:.6f}"]
    cmd += ["-ac", "2", "-ar", str(SR), "-f", "f32le", "-"]
    raw = sp.check_output(cmd)
    if not raw:
        raise RuntimeError(f"no audio decoded from {path}")
    return np.frombuffer(raw, np.float32).reshape(-1, 2).copy()


def probe_duration(path: Path) -> float:
    return float(sp.check_output(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)],
        text=True,
    ).strip())


def integrated_lufs(path: Path) -> float:
    proc = sp.run(
        ["ffmpeg", "-hide_banner", "-i", str(path), "-af", "ebur128", "-f", "null", "-"],
        capture_output=True, text=True,
    )
    found = re.findall(r"I:\s*(-?\d+(?:\.\d+)?)\s*LUFS", proc.stderr)
    if not found:
        raise RuntimeError(f"no EBU R128 reading for {path}\n{proc.stderr[-400:]}")
    return float(found[-1])


def rms(x: np.ndarray) -> float:
    return float(np.sqrt(np.mean(np.square(x.astype(np.float64))) + 1e-20))


def db(x: np.ndarray) -> float:
    return 20.0 * np.log10(rms(x) + 1e-12)


def explain_scalar(t: float) -> float:
    """0 in awe, 1 in explain, 3.0 s cosine ramps centred on the chapter cards."""
    if t < 176.78 - 1.5:
        return 0.0
    if t < 176.78 + 1.5:
        return (t - (176.78 - 1.5)) / 3.0
    if t < 393.86 - 1.5:
        return 1.0
    if t < 393.86 + 1.5:
        return 1.0 - (t - (393.86 - 1.5)) / 3.0
    return 0.0


def warmth_scalar(t: float) -> float:
    """Part 2 orchard warmth. Same register; only the harmonic mix changes."""
    if t < 84.44 - 1.5:
        return 0.0
    if t < 84.44 + 1.5:
        return (t - (84.44 - 1.5)) / 3.0
    if t < 176.78 - 1.5:
        return 1.0
    if t < 176.78 + 1.5:
        return 1.0 - (t - (176.78 - 1.5)) / 3.0
    return 0.0


def box_lowpass(x: np.ndarray, cutoff_hz: float) -> np.ndarray:
    """Moving-average lowpass. -3 dB sits near cutoff_hz. Numpy only."""
    k = max(1, int(round(0.443 * SR / cutoff_hz)))
    if k < 2:
        return x
    y = np.empty_like(x)
    window = np.arange(1, k + 1, dtype=np.float64)
    for c in range(x.shape[1]):
        col = x[:, c].astype(np.float64)
        csum = np.cumsum(col)
        out = np.empty_like(col)
        out[:k] = csum[:k] / window
        out[k:] = (csum[k:] - csum[:-k]) / k
        y[:, c] = out.astype(np.float32)
    return y


def partials(t: np.ndarray, freq: float, h2: np.ndarray | float, h3: np.ndarray | float,
             ceiling: float) -> np.ndarray:
    """sin + bounded 2nd and 3rd. No 4th harmonic. Partials above ceiling dropped."""
    w = 2.0 * np.pi * freq
    tone = np.sin(w * t)
    if 2.0 * freq <= ceiling:
        tone = tone + h2 * np.sin(2.0 * w * t)
    if 3.0 * freq <= ceiling:
        tone = tone + h3 * np.sin(3.0 * w * t)
    return tone.astype(np.float32)


def schedule() -> list[tuple[float, float, int, tuple[int, ...]]]:
    spans = []
    for part in PARTS:
        bar = 4.0 * 60.0 / part["bpm"]
        dur = part["bars"] * bar
        if dur < 2 * bar - 1e-6 or dur > 4 * bar + 1e-6:
            raise SystemExit(f"part {part['part']} chord span is outside 2-4 bars")
        t = part["start"]
        i = 0
        chords = CHORDS[part["part"]]
        while t < part["end"] - 0.05:
            end = min(part["end"], t + dur)
            notes = chords[i % len(chords)]
            spans.append((t, end, part["part"], notes))
            i += 1
            t = end
    basses = [notes[0] for _, _, _, notes in spans]
    for a, b in zip(basses, basses[1:]):
        if a == b:
            raise SystemExit("two chords in a row share a bass; that would sit as a drone")
    return spans


def chord_at(spans, t: float) -> tuple[int, ...]:
    for a, b, _, notes in spans:
        if a <= t < b:
            return notes
    return spans[-1][3]


def synthesize() -> np.ndarray:
    n = int(round(TOTAL * SR))
    pad = np.zeros((n, 2), np.float32)
    harp = np.zeros((n, 2), np.float32)
    spans = schedule()
    log(f"chords {len(spans)}, samples {n}")

    for a, b, _part, notes in spans:
        a0 = a
        b1 = min(TOTAL, b + 3.0)  # 3.0 s overlap, above the 2.5 s floor
        i0 = int(round(a0 * SR))
        i1 = min(n, int(round(b1 * SR)))
        if i1 - i0 < 8:
            continue
        t = np.arange(i1 - i0, dtype=np.float32) / SR
        abs_t = t + a0
        # Opening is already up. Later chords fade in across the 3 s overlap.
        if a0 < 0.05:
            ein = np.ones_like(t)
        else:
            ein = np.clip((abs_t - a0) / 3.0, 0.0, 1.0)
            ein = 0.5 - 0.5 * np.cos(np.pi * ein)
        eout = np.clip((b1 - abs_t) / 3.0, 0.0, 1.0)
        eout = 0.5 - 0.5 * np.cos(np.pi * np.clip(eout, 0.0, 1.0))
        env = (ein * eout).astype(np.float32)
        warm = np.array([warmth_scalar(float(x)) for x in abs_t[::480]], np.float32)
        # Step-wise warmth is enough inside one chord; resample to the window.
        warm_full = np.repeat(warm, 480)[:len(t)]
        if len(warm_full) < len(t):
            warm_full = np.pad(warm_full, (0, len(t) - len(warm_full)), mode="edge")
        h2 = np.clip(0.10 + 0.04 * warm_full, 0.0, 0.14).astype(np.float32)
        h3 = np.clip(0.022 + 0.013 * warm_full, 0.0, 0.035).astype(np.float32)
        for v, midi in enumerate(notes):
            freq = midi_hz(midi)
            tone = partials(t, freq, h2, h3, 1200.0)
            amp = 0.075 / (1.0 + 0.28 * v)
            left = (0.62 + 0.04 * v) * amp
            right = (0.78 - 0.04 * v) * amp
            pad[i0:i1, 0] += tone * env * left
            pad[i0:i1, 1] += tone * env * right

    # One inner note per bar, same low-harmonic pad, never a held bass.
    bar_i = 0
    t_bar = 0.0
    while t_bar < VO_END - 0.2:
        bpm = 62.0 + 5.0 * explain_scalar(t_bar)
        bar = 4.0 * 60.0 / bpm
        midi = MELODY[bar_i % len(MELODY)]
        i0 = int(round(t_bar * SR))
        i1 = min(n, int(round((t_bar + bar + 2.6) * SR)))
        tt = np.arange(i1 - i0, dtype=np.float32) / SR
        ein = np.clip(tt / 2.6, 0.0, 1.0)
        eout = np.clip((bar + 2.6 - tt) / 2.6, 0.0, 1.0)
        env = (0.5 - 0.5 * np.cos(np.pi * ein)) * (0.5 - 0.5 * np.cos(np.pi * np.clip(eout, 0, 1)))
        tone = partials(tt, midi_hz(midi), 0.12, 0.03, 1200.0) * 0.032
        pad[i0:i1, 0] += tone * env * 0.70
        pad[i0:i1, 1] += tone * env * 0.78
        t_bar += bar
        bar_i += 1

    log("pads laid")
    pad = box_lowpass(pad, 1200.0)

    k = 0
    t_beat = 0.0
    while t_beat < VO_END - 0.05:
        e = explain_scalar(t_beat)
        bpm = 62.0 + 5.0 * e
        step = 60.0 / bpm
        spacious = 395.0 <= t_beat < 427.0
        if spacious:
            play = (k % 4 == 0)
        elif e < 0.5:
            play = (k % 4 in (0, 2))
        else:
            play = True
        if play:
            at = t_beat + 0.010 * unit(k, 2)
            if 0.0 <= at < VO_END:
                notes = chord_at(spans, min(t_beat, TOTAL - 0.01))
                midi = notes[(k * 3) % len(notes)]
                if midi < 53:
                    midi += 12  # one octave only, and only to lift a low chord tone
                if midi > 74:
                    midi -= 12
                vel = 0.050 * (0.82 + 0.28 * e) * (1.0 + 0.10 * unit(k, 1))
                decay = 0.72 - 0.22 * e
                i0 = int(round(at * SR))
                length = int(1.05 * SR)
                i1 = min(n, i0 + length)
                if i1 - i0 > 32:
                    tt = np.arange(i1 - i0, dtype=np.float32) / SR
                    att_n = int(0.015 * SR)  # 15 ms, inside the 12-18 ms window
                    att = np.minimum(tt / (att_n / SR), 1.0)
                    att = 0.5 - 0.5 * np.cos(np.pi * att)
                    tail = np.ones_like(tt)
                    fade = int(0.030 * SR)
                    if fade > 1:
                        tail[-fade:] = np.linspace(1.0, 0.0, fade, dtype=np.float32)
                    tone = partials(tt, midi_hz(midi), 0.10, 0.02, 2200.0)
                    tone = tone * att * np.exp(-tt / decay) * tail * vel
                    harp[i0:i1, 0] += tone * 0.62
                    harp[i0:i1, 1] += tone * 0.74
        t_beat += step
        k += 1
    log(f"harp notes scheduled through beat {k}")
    harp = box_lowpass(harp, 2200.0)

    mix = pad + harp
    t = np.arange(n, dtype=np.float64) / SR
    shape = np.ones(n, np.float64)
    # Halley visit: gentle dip across 363-393 s, recovered by the next card.
    dip = (t >= 363.0) & (t <= 393.0)
    phase = (t[dip] - 363.0) / 30.0
    shape[dip] = 1.0 - 0.25 * np.sin(np.pi * phase)
    # Spacious bars keep the pad; the harp is simply quieter by schedule.
    space = (t >= 395.0) & (t <= 427.0)
    shape[space] *= 0.94
    # Stay well above -45 dBFS through 526 s, then leave the room.
    late = (t >= VO_END) & (t < REF_END)
    shape[late] = 1.0 + (0.40 - 1.0) * ((t[late] - VO_END) / (REF_END - VO_END))
    end = (t >= REF_END) & (t < TAIL_SILENCE)
    u = (t[end] - REF_END) / (TAIL_SILENCE - REF_END)
    shape[end] = 0.40 * (0.5 + 0.5 * np.cos(np.pi * u))
    shape[t >= TAIL_SILENCE] = 0.0
    mix *= shape.astype(np.float32)[:, None]
    mix = balance_parts(mix)
    peak = float(np.max(np.abs(mix))) + 1e-9
    if peak > 0.50:
        mix *= np.float32(0.50 / peak)
    return mix.astype(np.float32)


def part_slices(n: int) -> list[tuple[int, int, int]]:
    """RMS windows. Part 5 stops at the VO end so the composed decay is not a hole."""
    spans = []
    for part in PARTS:
        a = part["start"]
        b = VO_END if part["part"] == 5 else part["end"]
        spans.append((part["part"], int(round(a * SR)), min(n, int(round(b * SR)))))
    return spans


def balance_parts(mix: np.ndarray) -> np.ndarray:
    edges = [p["start"] for p in PARTS] + [TOTAL]
    gains = [1.0, 1.0, 1.0, 1.0, 1.0]
    out = mix
    for _pass in range(3):
        dbs = []
        for _part, i0, i1 in part_slices(len(out)):
            dbs.append(db(out[i0:i1]))
        spread = max(dbs) - min(dbs)
        log("part RMS dBFS " + ", ".join(f"p{i+1} {v:.2f}" for i, v in enumerate(dbs))
            + f"  spread {spread:.2f}")
        if spread <= 0.45:
            break
        target = float(np.median(dbs))
        gains = [10 ** ((target - v) / 20.0) for v in dbs]
        env = gain_envelope(len(out), edges, gains)
        out = out * env[:, None]
    dbs = [db(out[i0:i1]) for _p, i0, i1 in part_slices(len(out))]
    spread = max(dbs) - min(dbs)
    if spread > 1.0:
        raise SystemExit(f"part loudness spread {spread:.2f} dB is above 1.0 dB")
    step = dbs[1] - dbs[0]
    if abs(step) > 1.0:
        raise SystemExit(f"part 2 is {step:+.2f} dB against part 1")
    return out


def gain_envelope(n: int, edges: list[float], gains: list[float]) -> np.ndarray:
    t = np.arange(n, dtype=np.float64) / SR
    g = np.empty(n, np.float64)
    g[:] = gains[-1]
    for p in range(5):
        g[(t >= edges[p]) & (t < edges[p + 1])] = gains[p]
    half = 1.5
    for p in range(1, 5):
        c = edges[p]
        m = (t >= c - half) & (t < c + half)
        x = (t[m] - (c - half)) / 3.0
        w = 0.5 - 0.5 * np.cos(np.pi * np.clip(x, 0.0, 1.0))
        g[m] = gains[p - 1] * (1.0 - w) + gains[p] * w
    return g.astype(np.float32)


def silence_spans(path: Path, limit_s: float, hold: str) -> list[dict]:
    proc = sp.run(
        ["ffmpeg", "-hide_banner", "-i", str(path), "-t", f"{limit_s:.3f}",
         "-af", f"silencedetect=noise=-45dB:d={hold}", "-f", "null", "-"],
        capture_output=True, text=True,
    )
    starts = [float(x) for x in re.findall(r"silence_start:\s*([0-9.]+)", proc.stderr)]
    ends = [float(x) for x in re.findall(r"silence_end:\s*([0-9.]+)", proc.stderr)]
    spans = []
    for i, start in enumerate(starts):
        end = ends[i] if i < len(ends) else limit_s
        if end <= 0.02 or start >= limit_s - 0.01:
            continue
        spans.append({"start_s": round(start, 3), "end_s": round(min(end, limit_s), 3), "hold_s": hold})
    return spans


def floor_table(audio: np.ndarray, limit_s: float) -> dict:
    n = int(round(limit_s * SR))
    hop = SR
    mono = audio[:n].mean(axis=1).astype(np.float64)
    rows = []
    worst = 99.0
    below = []
    for i in range(n // hop):
        seg = mono[i * hop:(i + 1) * hop]
        val = 20.0 * np.log10(np.sqrt(np.mean(seg * seg) + 1e-20))
        rows.append({"t_s": i, "rms_dbfs": round(float(val), 2)})
        worst = min(worst, val)
        if val < -45.0:
            below.append(i)
    return {"min_rms_dbfs": round(float(worst), 2), "below_minus_45": below, "one_second_rms": rows}


def render_score() -> np.ndarray:
    mix = synthesize()
    bed = MUSIC / BED_NAME
    write_wav(bed, mix)
    log(f"wrote {bed.name} {probe_duration(bed):.3f}s")
    report = floor_table(mix, REF_END)
    if report["below_minus_45"]:
        raise SystemExit(f"RMS floor under -45 dBFS at seconds {report['below_minus_45'][:12]}")
    sil_025 = silence_spans(bed, REF_END, "0.25")
    sil_050 = silence_spans(bed, REF_END, "0.50")
    if sil_025 or sil_050:
        raise SystemExit(f"silencedetect dropouts 0.25 {sil_025} 0.50 {sil_050}")
    log(f"floor min {report['min_rms_dbfs']} dBFS, silence spans 0")
    stems = []
    for part in PARTS:
        name = f"hos_009_stem_part0{part['part']}_{part['slug']}_v04.wav"
        i0 = int(round(part["start"] * SR))
        i1 = int(round(part["end"] * SR))
        dest = MUSIC / name
        write_wav(dest, mix[i0:i1])
        stems.append(dest)
        log(f"  stem {name} {probe_duration(dest):.3f}s")
    dbs = []
    lufs = []
    for part, dest in zip(PARTS, stems):
        if part["part"] == 5:
            sl = mix[int(round(part["start"] * SR)):int(round(VO_END * SR))]
            tmp = MUSIC / "_part5_body_v04.wav"
            write_wav(tmp, sl)
            measure = tmp
        else:
            sl = mix[int(round(part["start"] * SR)):int(round(part["end"] * SR))]
            measure = dest
        dbs.append(round(db(sl), 3))
        lufs.append(round(integrated_lufs(measure), 3))
        log(f"  part {part['part']} RMS {dbs[-1]} dBFS  LUFS {lufs[-1]}")
    body = MUSIC / "_part5_body_v04.wav"
    if body.exists():
        body.unlink()
    spread = max(dbs) - min(dbs)
    if spread > 1.0:
        raise SystemExit(f"stem RMS spread {spread:.2f} dB")
    continuity = {
        "job": "J3239",
        "bed": BED_NAME,
        "duration_s": probe_duration(bed),
        "silence_noise_db": -45,
        "silence_window_s": [0.0, REF_END],
        "silence_holds_s": [0.25, 0.50],
        "silence_0_25": sil_025,
        "silence_0_50": sil_050,
        "interior_dropouts": 0,
        "min_rms_dbfs": report["min_rms_dbfs"],
        "one_second_rms": report["one_second_rms"],
        "parts": [
            {
                "part": part["part"],
                "title": part["title"],
                "start_s": part["start"],
                "end_s": part["end"],
                "mood": part["mood"],
                "bpm": part["bpm"],
                "bars_per_chord": part["bars"],
                "rms_dbfs": dbs[i],
                "integrated_lufs": lufs[i],
                "rms_window_end_s": VO_END if part["part"] == 5 else part["end"],
            }
            for i, part in enumerate(PARTS)
        ],
        "rms_spread_db": round(spread, 3),
        "part2_minus_part1_db": round(dbs[1] - dbs[0], 3),
        "integrated_lufs": round(integrated_lufs(bed), 3),
    }
    (MUSIC / "CONTINUITY_v04_synth.json").write_text(json.dumps(continuity, indent=2) + "\n")
    plan = {
        "film": "009_The-Falling-Moon-Gravity",
        "job": "J3239",
        "bed": BED_NAME,
        "source": "own synthesis (_build_hos009_score_v04_synth.py), £0, no ElevenLabs, no samples",
        "prompt": PROMPT,
        "duration_s": continuity["duration_s"],
        "bpm_arc": "62 awe / 67 explain",
        "key": "D minor",
        "a4_hz": 440,
        "sha256": sha256_file(bed),
        "integrated_lufs": continuity["integrated_lufs"],
        "chapters": [
            {"part": p["part"], "start_s": p["start"], "end_s": p["end"],
             "mood": p["mood"], "bpm": p["bpm"], "crossfade_s": 3.0}
            for p in PARTS
        ],
    }
    (MUSIC / "hos_009_score_v04_synth_plan.json").write_text(json.dumps(plan, indent=2) + "\n")
    return mix


def build_review(mix: np.ndarray) -> dict:
    REVIEW.mkdir(parents=True, exist_ok=True)
    vo = np.zeros_like(mix)
    placements = [
        (0.0, "hos_009_part01_the_falling_moon_v01.mp3"),
        (86.34, "hos_009_part02_an_apple_in_a_plague_year_v01.mp3"),
        (178.68, "hos_009_part03_the_cannon_on_the_mountain_v01.mp3"),
        (262.06, "hos_009_part04_the_moon_test_v01.mp3"),
        (395.76, "hos_009_part05_falling_around_the_world_v01.mp3"),
    ]
    for start, name in placements:
        part = load_audio(VO / name)
        i = int(round(start * SR))
        n = min(len(part), len(vo) - i)
        vo[i:i + n] += part[:n]
        log(f"  VO {name} at {start:.2f}s ({n / SR:.2f}s)")
    vo_path = REVIEW / "_vo_0_518s40.wav"
    bed_path = REVIEW / "_bed_0_518s40.wav"
    i_end = int(round(VO_END * SR))
    write_wav(vo_path, vo[:i_end])
    write_wav(bed_path, mix[:i_end])
    vo_lufs = integrated_lufs(vo_path)
    bed_lufs = integrated_lufs(bed_path)
    gain_db = (vo_lufs - 12.0) - bed_lufs
    if vo_lufs - (bed_lufs + gain_db) < 10.0:
        gain_db = (vo_lufs - 10.0) - bed_lufs
    gain = float(10 ** (gain_db / 20.0))
    ducked = mix * np.float32(gain)
    write_wav(bed_path, ducked[:i_end])
    ducked_lufs = integrated_lufs(bed_path)
    under = vo_lufs - ducked_lufs
    log(f"VO {vo_lufs:.2f} LUFS, bed {bed_lufs:.2f} then {ducked_lufs:.2f} after {gain_db:.2f} dB, under {under:.2f} LU")
    if under < 10.0 - 1e-6:
        raise SystemExit(f"bed is only {under:.2f} LU under the VO")
    mixed = vo + ducked
    peak = float(np.max(np.abs(mixed))) + 1e-9
    if peak > 0.98:
        mixed *= np.float32(0.98 / peak)
    vo_path.unlink()
    bed_path.unlink()

    def cut(buf: np.ndarray, a: float, b: float | None) -> np.ndarray:
        i = int(round(a * SR))
        j = len(buf) if b is None else int(round(b * SR))
        return buf[i:j]

    files = {
        "transition_078_092_part2_mix": REVIEW / "hos_009_transition_078_092_part2_mix_v04.wav",
        "transition_168_186_bed": REVIEW / "hos_009_transition_168_186_bed_v04.wav",
        "transition_168_186_mix": REVIEW / "hos_009_transition_168_186_mix_v04.wav",
        "transition_386_402_part5_mix": REVIEW / "hos_009_transition_386_402_part5_mix_v04.wav",
        "reference_mix_0_518s40": REVIEW / "hos_009_reference_mix_0_518s40_v04.wav",
        "tail_518s40": REVIEW / "hos_009_tail_518s40_v04.wav",
        "reference_endpoint_526s": REVIEW / "hos_009_reference_endpoint_526s_v04.wav",
    }
    write_wav(files["transition_078_092_part2_mix"], cut(mixed, 78.0, 92.0))
    write_wav(files["transition_168_186_bed"], cut(mix, 168.0, 186.0))
    write_wav(files["transition_168_186_mix"], cut(mixed, 168.0, 186.0))
    write_wav(files["transition_386_402_part5_mix"], cut(mixed, 386.0, 402.0))
    write_wav(files["reference_mix_0_518s40"], cut(mixed, 0.0, VO_END))
    write_wav(files["tail_518s40"], cut(mixed, VO_END, None))
    write_wav(files["reference_endpoint_526s"], cut(mixed, 0.0, REF_END))
    return {
        "bed_gain_db": round(gain_db, 3),
        "vo_lufs_0_518s40": round(vo_lufs, 3),
        "bed_lufs_before_duck": round(bed_lufs, 3),
        "bed_lufs_after_duck": round(ducked_lufs, 3),
        "bed_under_vo_lu": round(under, 3),
        "files": {key: str(path.relative_to(FILM)) for key, path in files.items()},
    }


def is_stub(path: Path) -> bool:
    st = path.stat()
    return st.st_size > 0 and getattr(st, "st_blocks", 1) == 0


def collect_library() -> tuple[list[Path], list[dict]]:
    roots = [
        ("mini-local/History Of Science/02_Video-Projects", HOS / "02_Video-Projects"),
        ("mini-local/orbit-with-ben/02_Video-Projects", OWB / "02_Video-Projects"),
        ("studio-live/History Of Science/02_Video-Projects",
         Path("/Volumes/data/studio-live/History Of Science/02_Video-Projects")),
        ("studio-live/orbit-with-ben/02_Video-Projects",
         Path("/Volumes/data/studio-live/orbit-with-ben/02_Video-Projects")),
        ("mac-mini-archive/YouTube", Path("/Volumes/data/mac-mini-archive/YouTube")),
        ("mac-mini-archive/orbit-with-ben", Path("/Volumes/data/mac-mini-archive/orbit-with-ben")),
        ("mac-mini-archive/youtube-staging", Path("/Volumes/data/mac-mini-archive/youtube-staging")),
        ("mac-mini-archive/History Of Science", Path("/Volumes/data/mac-mini-archive/History Of Science")),
    ]
    patterns = {
        "mac-mini-archive/YouTube": ("*/02_Video-Projects/*/05_Music/*",),
        "mac-mini-archive/orbit-with-ben": ("02_Video-Projects/*/05_Music/*",),
        "mac-mini-archive/youtube-staging": ("*/05_Music/*", "*/*/05_Music/*"),
        "mac-mini-archive/History Of Science": ("02_Video-Projects/*/05_Music/*", "*/05_Music/*"),
    }
    files: list[Path] = []
    report = []
    for label, root in roots:
        if not root.exists():
            report.append({"root": label, "state": "missing", "files": 0})
            continue
        found = []
        globs = patterns.get(label, ("*/05_Music/*", "*/*/05_Music/*"))
        seen = set()
        for pattern in globs:
            for path in root.glob(pattern):
                if not path.is_file() or path.suffix.lower() not in AUDIO_EXT:
                    continue
                if path.name.startswith("._") or "009_The-Falling-Moon-Gravity" in path.parts:
                    continue
                if is_stub(path):
                    continue
                key = str(path)
                if key in seen:
                    continue
                seen.add(key)
                found.append(path)
        files.extend(found)
        report.append({"root": label, "state": "listed", "files": len(found)})
        log(f"library {label}: {len(found)}")
    uat = []
    if UAT_LOCAL.is_dir():
        for path in sorted(UAT_LOCAL.iterdir()):
            if path.is_file() and path.suffix.lower() in AUDIO_EXT and not path.name.startswith("._"):
                if not is_stub(path):
                    uat.append(path)
    files.extend(uat)
    report.append({
        "root": "uat-materialized",
        "state": "listed",
        "files": len(uat),
        "replaces": "icloud HOS UAT + OWB UAT stubs",
    })
    log(f"library uat materialized: {len(uat)}")
    uniq, seen = [], set()
    for path in files:
        key = str(path.resolve())
        if key in seen:
            continue
        seen.add(key)
        uniq.append(path)
    return uniq, report


def run_gate(bed: Path, others: list[Path], out_path: Path, roots: list[dict]) -> dict:
    sys.path.insert(0, str(OWB / "scripts"))
    import music_gate

    scores: list[dict] = []
    real = music_gate.similarity

    def wrapped(a, b, min_overlap=20):
        value = real(a, b, min_overlap)
        scores.append({"similarity": round(float(value), 4)})
        return value

    music_gate.similarity = wrapped
    try:
        result = music_gate.judge(FILM, bed, others=others)
    finally:
        music_gate.similarity = real
    ranked = sorted(scores, key=lambda row: row["similarity"], reverse=True)
    result["comparison_count"] = len(scores)
    result["max_similarity"] = ranked[0]["similarity"] if ranked else 0.0
    result["top_similarities"] = ranked[:8]
    result["unreadable_warn_count"] = sum(1 for w in result.get("warn", []) if "couldn't read" in w)
    result["library_roots"] = roots
    result["music_gate_sha256"] = sha256_file(OWB / "scripts/music_gate.py")
    result["waiver_used"] = bool(result.get("waiver"))
    out_path.write_text(json.dumps(result, indent=2) + "\n")
    log(
        f"music gate {result['verdict']}: comparisons {result['comparison_count']} "
        f"max {result['max_similarity']} unreadable {result['unreadable_warn_count']}"
    )
    if result["verdict"] != "PASS" or result["unreadable_warn_count"] or result["comparison_count"] < 89:
        raise SystemExit(f"music gate did not pass for {bed.name}")
    if result["max_similarity"] >= 0.8 or result["waiver_used"]:
        raise SystemExit("similarity is at the fail line, or a waiver was used")
    if not any(r["root"] == "uat-materialized" and r["files"] >= 15 for r in roots):
        raise SystemExit("materialized UAT library is short of 15 tracks")
    return result


def verify_locks(previous: dict | None = None) -> dict:
    expected = {
        MUSIC / "hos_009_teach_v01.mp3": LOCKS["hos_009_teach_v01.mp3"],
        MUSIC / "hos_009_wonder_v01.mp3": LOCKS["hos_009_wonder_v01.mp3"],
        MUSIC / "hos_009_wonder_v02.mp3": LOCKS["hos_009_wonder_v02.mp3"],
        MUSIC / "hos_009_score_joined_v01.wav": LOCKS["hos_009_score_joined_v01.wav"],
        MUSIC / "hos_009_score_joined_v02.wav": LOCKS["hos_009_score_joined_v02.wav"],
        VO / "VO_TAKES_KEEP.json": LOCKS["VO_TAKES_KEEP.json"],
        FILM / "07_Edit-Project/VO_RETIME_v01.json": LOCKS["VO_RETIME_v01.json"],
    }
    found = {}
    for path, want in expected.items():
        if not path.exists():
            raise SystemExit(f"missing lock {path}")
        got = sha256_file(path)
        if got != want:
            raise SystemExit(f"lock changed {path.name}: {got} != {want}")
        found[path.name] = got
    # v03 stays rejected. Remember its hash and refuse a later rewrite.
    for name in (
        "hos_009_wonder_v03_synth.wav",
        "hos_009_score_joined_v03.wav",
        "_build_hos009_wonder_v03_synth.py",
    ):
        path = MUSIC / name
        if not path.exists():
            continue
        got = sha256_file(path)
        if previous is not None and previous.get(path.name) not in (None, got):
            raise SystemExit(f"rejected v03 file changed: {path.name}")
        found[path.name] = got
    flight = HOS / "04_Audio/tools/hos009_score_flight.py"
    text = flight.read_text()
    if "ACTIVATION_AUTHORIZED = False" not in text:
        raise SystemExit("flight module activation flag is not the closed literal")
    found["hos009_score_flight.py"] = sha256_file(flight)
    for name in (
        "J2631_code_graphic_009_p4_05_minute_second.mp4",
        "J2632_r4_code_graphic_009_p3_01_really_falling_c1.mp4",
    ):
        hits = list(FILM.rglob(name))
        if not hits:
            log(f"diagram lock not in the film folder: {name}")
            continue
        found[name] = sha256_file(hits[0])
    log("preserved locks hashed; flight activation stays closed")
    return found


def mirror_nas(paths: list[Path]) -> dict:
    if not Path("/Volumes/data/studio-live").is_dir():
        raise SystemExit("studio-live is not mounted; NAS parity cannot be checked")
    NAS.mkdir(parents=True, exist_ok=True)
    (NAS / "audio_review_v04_synth").mkdir(parents=True, exist_ok=True)
    parity = []
    for path in paths:
        rel = path.relative_to(MUSIC)
        dest = NAS / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(path.read_bytes())
        a, b = sha256_file(path), sha256_file(dest)
        if a != b:
            raise SystemExit(f"NAS parity failed for {rel}")
        parity.append({"file": str(rel), "sha256": a, "bytes": path.stat().st_size})
        log(f"NAS match {rel}")
    return {"nas": str(NAS), "files": parity}


def deliverable_paths() -> list[Path]:
    paths = [
        MUSIC / "_build_hos009_score_v04_synth.py",
        MUSIC / BED_NAME,
        MUSIC / "hos_009_score_v04_synth_plan.json",
        MUSIC / "CONTINUITY_v04_synth.json",
        MUSIC / "music_gate_v04_synth.json",
        MUSIC / "PROVENANCE_v04_synth.json",
    ]
    for part in PARTS:
        paths.append(MUSIC / f"hos_009_stem_part0{part['part']}_{part['slug']}_v04.wav")
    paths += sorted(REVIEW.glob("hos_009_*_v04.wav"))
    return paths


def write_provenance(locks: dict, nas: dict | None) -> None:
    rows = []
    for path in deliverable_paths():
        if path.name == "PROVENANCE_v04_synth.json" or not path.exists():
            continue
        rows.append({"file": str(path.relative_to(MUSIC)), "sha256": sha256_file(path), "bytes": path.stat().st_size})
    payload = {
        "job": "J3239",
        "scope_job": "J3236",
        "film": "HOS:009",
        "cash_spent_gbp": 0,
        "subscription_credits": 0,
        "account_gets": 0,
        "elevenlabs_posts": 0,
        "method": "deterministic pure Python/NumPy warm low-harmonic pads and soft wooden harp",
        "activation_authorized": False,
        "preserved_locks": locks,
        "teach_unchanged_sha256": sha256_file(MUSIC / "hos_009_teach_v01.mp3"),
        "local_files": rows,
        "ear_review_pass_claimed": False,
        "score_accepted": False,
        "nas_parity": nas,
    }
    (MUSIC / "PROVENANCE_v04_synth.json").write_text(json.dumps(payload, indent=2) + "\n")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--from", dest="start", choices=["synth", "review", "gates", "nas"], default="synth")
    args = parser.parse_args()
    MUSIC.mkdir(parents=True, exist_ok=True)
    locks = verify_locks()
    if args.start == "synth":
        mix = render_score()
        review = build_review(mix)
    else:
        mix = load_audio(MUSIC / BED_NAME)
        review = json.loads((MUSIC / "CONTINUITY_v04_synth.json").read_text()).get("audition")
        if args.start == "review" or review is None:
            review = build_review(mix)
    side = MUSIC / "CONTINUITY_v04_synth.json"
    payload = json.loads(side.read_text())
    payload["audition"] = review
    side.write_text(json.dumps(payload, indent=2) + "\n")
    if args.start in ("synth", "review", "gates"):
        others, roots = collect_library()
        if len(others) < 89:
            raise SystemExit(f"library has {len(others)} readable beds, need at least 89")
        run_gate(MUSIC / BED_NAME, others, MUSIC / "music_gate_v04_synth.json", roots)
    write_provenance(locks, None)
    nas = mirror_nas([p for p in deliverable_paths() if p.exists()])
    write_provenance(locks, nas)
    prov = MUSIC / "PROVENANCE_v04_synth.json"
    nas_prov = NAS / prov.name
    nas_prov.write_bytes(prov.read_bytes())
    if sha256_file(nas_prov) != sha256_file(prov):
        raise SystemExit("provenance NAS parity failed")
    # Locks are hashed again so a mirror cannot have been a rewrite of them.
    verify_locks(locks)
    log("done")
    return 0


if __name__ == "__main__":
    sys.exit(main())
