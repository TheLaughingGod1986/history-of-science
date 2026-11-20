#!/usr/bin/env python3
"""J3234 — HOS 009 wonder opening v03, £0 own synthesis.

Deterministic NumPy Karplus-Strong lute and bowed-viol chamber bed in D minor.
No samples, no soundfonts, no network, no ElevenLabs. Does not touch
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
BPM = 63.0
BEAT = 60.0 / BPM
SEED = 32341120
RAW_S = 180.0
WINDOW_END = 178.28
HANDOFF = (175.28, 178.28)
ORCHARD = 84.44
TEACH_SHA = "4c1f0a17364ad5ba96fdd2d42730b2f857d19017fab52b221701bd4e15d07bb1"
TEACH_S = 360.045688

OWB = Path("/Users/benjaminoats/YouTube/orbit-with-ben")
HOS = Path("/Users/benjaminoats/YouTube/History Of Science")
FILM = HOS / "02_Video-Projects/009_The-Falling-Moon-Gravity"
MUSIC = FILM / "05_Music"
REVIEW = MUSIC / "audio_review_v03_synth"
VO = FILM / "02_Voiceover"
NAS = Path(
    "/Volumes/data/studio-live/History Of Science/02_Video-Projects/"
    "009_The-Falling-Moon-Gravity/05_Music"
)
UAT_LOCAL = Path("/Volumes/MiniWork/scratch/j2664/uat_materialized")
AUDIO_EXT = {".mp3", ".wav", ".m4a", ".aac", ".flac"}

WONDER_PROMPT = (
    "Original instrumental opening underscore exclusively for HOS 009 The Falling Moon. "
    "17th-century D-minor chamber texture (A4=440): Karplus-Strong plucked gut-string lute "
    "arpeggios over warm multi-voice bowed viols, moving modal harmony every two or three bars, "
    "voices overlapping from the first sample with no silent rest. At 84.44 seconds the colour "
    "warms into a Woolsthorpe orchard. From 175.28 to 178.28 a quiet sustained D4/A4 open fifth "
    "hands off into the retained D-minor harpsichord teach cue. Leave space for British narration.\n"
    "Pace: 60-66 BPM.\n"
    "NOT any earlier HOS or Orbit bed, hos_009_wonder_v01, hos_009_wonder_v02, jupiter-music.mp3, "
    "a static bass-drone opening, cosmic shimmer, piano space-documentary music, solo woodwind "
    "workshop waltz, borrowed melody, named-composer imitation, heroic brass, horror, vocals, "
    "lyrics, pop drums, EDM or comedy stings."
)
JOINED_PROMPT = (
    "Original joined instrumental bed v03 for HOS 009 The Falling Moon. Own-synthesis wonder "
    "opening (0-178.28s, D-minor gut-string lute and bowed viols, moving harmony, no silent rest) "
    "equal-power crossfaded into the retained teach_v01 harpsichord and low strings "
    "(175.28-535.33s). Leave generous space for British narration.\n"
    "Pace: 60-72 BPM.\n"
    "NOT any earlier HOS or Orbit bed, hos_009_wonder_v01, hos_009_wonder_v02, jupiter-music.mp3, "
    "a static bass-drone opening, cosmic shimmer, piano space-documentary music, solo woodwind "
    "workshop waltz, borrowed melody, named-composer imitation, heroic brass, horror, vocals, "
    "lyrics, pop drums, EDM or comedy stings.\n"
    "Crossfade: 3 second equal-power (acrossfade=d=3:c1=qsin:c2=qsin) from 175.28 to 178.28, "
    "centred on the cannon card at 176.78. No loop and no silence fill."
)

# Modal D minor. The bass note changes with every span, including the opening span,
# so the low end is a moving pluck and not a held drone.
CHORDS = [
    (50, 57, 65),  # D3 A3 F4
    (43, 50, 58),  # G2 D3 Bb3
    (46, 53, 62),  # Bb2 F3 D4
    (45, 52, 60),  # A2 E3 C4
    (41, 48, 57),  # F2 C3 A3
    (48, 55, 64),  # C3 G3 E4
    (50, 57, 62),  # D3 A3 D4
    (46, 53, 65),  # Bb2 F3 F4
    (43, 50, 62),  # G2 D3 D4
    (45, 52, 64),  # A2 E3 E4
    (50, 57, 65),
    (48, 55, 62),
    (46, 55, 62),
    (45, 57, 64),
    (50, 57, 62),
]


def log(msg: str) -> None:
    print(msg, flush=True)


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for blk in iter(lambda: fh.read(1 << 20), b""):
            h.update(blk)
    return h.hexdigest()


def midi_hz(m: float) -> float:
    return 440.0 * (2.0 ** ((m - 69.0) / 12.0))


def write_wav(path: Path, audio: np.ndarray) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    pcm = np.clip(np.asarray(audio, dtype=np.float64), -1.0, 1.0)
    frames = (pcm * 32767.0).astype("<i2")
    with wave.open(str(path), "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(frames.tobytes())


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
    return float(
        sp.check_output(
            [
                "ffprobe", "-v", "error", "-show_entries", "format=duration",
                "-of", "csv=p=0", str(path),
            ],
            text=True,
        ).strip()
    )


def integrated_lufs(path: Path) -> float:
    proc = sp.run(
        ["ffmpeg", "-hide_banner", "-i", str(path), "-af", "ebur128", "-f", "null", "-"],
        capture_output=True, text=True,
    )
    found = re.findall(r"I:\s*(-?\d+(?:\.\d+)?)\s*LUFS", proc.stderr)
    if not found:
        raise RuntimeError(f"no EBU R128 reading for {path}\n{proc.stderr[-500:]}")
    return float(found[-1])


def fir(cutoff_hz: float, taps: int = 63) -> np.ndarray:
    n = np.arange(taps, dtype=np.float64) - (taps - 1) / 2.0
    fc = cutoff_hz / SR
    h = np.sinc(2.0 * fc * n) * np.hamming(taps)
    h /= h.sum()
    return h.astype(np.float32)


def apply_fir(x: np.ndarray, kernel: np.ndarray) -> np.ndarray:
    if x.ndim == 1:
        return np.convolve(x, kernel, mode="same").astype(np.float32)
    return np.stack([np.convolve(x[:, c], kernel, mode="same") for c in range(x.shape[1])], 1).astype(np.float32)


def comb(x: np.ndarray, delay: int, gain: float) -> np.ndarray:
    y = np.array(x, dtype=np.float32, copy=True)
    pos = delay
    n = len(y)
    while pos < n:
        m = min(delay, n - pos)
        y[pos:pos + m] += gain * y[pos - delay:pos - delay + m]
        pos += delay
    return y


def schedule(total: float = RAW_S) -> list[tuple[float, float, tuple[int, ...]]]:
    spans = []
    t = 0.0
    i = 0
    while t < 170.0 - 1e-6:
        bars = 2 if t < 33.0 else 3
        dur = bars * 4 * BEAT
        end = min(170.0, t + dur)
        spans.append((t, end, CHORDS[i % len(CHORDS)]))
        i += 1
        t = end
    spans.append((170.0, total, (62, 69)))
    return spans


def fade_in_out(n: int, fade: int, rise: bool, fall: bool) -> np.ndarray:
    e = np.ones(n, np.float32)
    f = min(fade, n // 2)
    if f <= 1:
        return e
    ramp = np.linspace(0.0, np.pi / 2.0, f, dtype=np.float32)
    if rise:
        e[:f] = np.sin(ramp)
    if fall:
        e[-f:] = np.cos(ramp)
    return e


def karplus(freq: float, n: int, decay: float, rng: np.random.Generator) -> np.ndarray:
    period = max(2, int(round(SR / freq)))
    burst = rng.standard_normal(period).astype(np.float64)
    burst *= np.hanning(period)
    y = np.zeros(n, np.float64)
    y[:period] = burst
    src = 0
    dst = period
    while dst < n:
        m = min(period, n - dst)
        prev = y[src:src + m]
        low = prev.copy()
        if m > 1:
            low[1:] = 0.5 * (prev[1:] + prev[:-1])
        y[dst:dst + m] = decay * low
        src = dst
        dst += period
    fade = min(int(0.03 * SR), n // 3)
    if fade > 1:
        y[-fade:] *= np.linspace(1.0, 0.0, fade)
    peak = float(np.max(np.abs(y))) + 1e-9
    return (y / peak).astype(np.float32)


def add_mono(bus: np.ndarray, start: int, mono: np.ndarray, pan: tuple[float, float], amp: float) -> None:
    n = min(len(mono), len(bus) - start)
    if n <= 0:
        return
    bus[start:start + n, 0] += mono[:n] * amp * pan[0]
    bus[start:start + n, 1] += mono[:n] * amp * pan[1]


def bowed(midi: int, n: int, amp: float, rng: np.random.Generator, rate: float) -> np.ndarray:
    t = np.arange(n, dtype=np.float64) / SR
    f = midi_hz(midi)
    vib = 1.0 + 0.0035 * np.sin(2.0 * np.pi * rate * t + float(midi))
    phase = 2.0 * np.pi * np.cumsum(f * vib) / SR
    tone = np.sin(phase) + 0.32 * np.sin(2.0 * phase) + 0.10 * np.sin(3.0 * phase) + 0.035 * np.sin(4.0 * phase)
    trem = 1.0 + 0.028 * np.sin(2.0 * np.pi * (rate + 0.37) * t)
    noise = rng.standard_normal(n).astype(np.float64)
    noise = np.convolve(noise, np.ones(24) / 24.0, mode="same")
    y = amp * trem * tone + amp * 0.045 * noise
    return y.astype(np.float32)


def synthesize() -> np.ndarray:
    n = int(round(RAW_S * SR))
    lute = np.zeros((n, 2), np.float32)
    viol = np.zeros((n, 2), np.float32)
    spans = schedule()
    log(f"chord spans: {len(spans)} at {BPM:.0f} BPM")
    fade_n = int(1.15 * SR)
    for idx, (a, b, notes) in enumerate(spans):
        i0 = int(round(a * SR))
        i1 = int(round(b * SR))
        hold = i1 - i0 + fade_n
        hold = min(hold, n - i0)
        last = idx == len(spans) - 1
        env = fade_in_out(hold, fade_n, rise=idx > 0, fall=not last)
        orchard = a >= ORCHARD or b > ORCHARD
        amps = (0.055, 0.040, 0.030) if not orchard else (0.050, 0.038, 0.034)
        for v, midi in enumerate(notes[:3]):
            rng = np.random.default_rng(SEED + 1000 * idx + midi)
            tone = bowed(int(midi), hold, amps[min(v, 2)], rng, 4.6 + 0.17 * v)
            tone *= env
            pan = (0.46 + 0.04 * v, 0.54 - 0.03 * v)
            add_mono(viol, i0, tone, pan, 1.0)
        if orchard and not last:
            rng = np.random.default_rng(SEED + 5000 + idx)
            high = bowed(notes[-1] + 12, hold, 0.018, rng, 5.2)
            high *= env
            add_mono(viol, i0, high, (0.42, 0.58), 1.0)
        log(f"  viol span {idx + 1}/{len(spans)} {a:.2f}-{b:.2f}s {notes}")

    # Lute arpeggio on every half-beat until the handoff is cleared, plus a
    # moving bass pluck on every beat. Both change pitch with the chord.
    half = BEAT / 2.0
    t = 0.0
    k = 0
    pattern = (0, 2, 1, 2)
    while t < 173.6:
        notes = chord_at(spans, t)
        degree = pattern[k % 4]
        midi = notes[min(degree, len(notes) - 1)] + 12
        if t >= ORCHARD:
            midi += 12
        dur = int((1.35 if t < ORCHARD else 1.7) * SR)
        rng = np.random.default_rng(SEED + 17 * k + 3)
        pluck = karplus(midi_hz(midi), dur, 0.988 if t < ORCHARD else 0.991, rng)
        amp = 0.20 if t < ORCHARD else 0.15
        pan = (0.62, 0.38) if k % 2 == 0 else (0.40, 0.60)
        add_mono(lute, int(round(t * SR)), pluck, pan, amp)
        if k % 2 == 0 and t < 168.0:
            root = notes[0]
            fifth = notes[min(1, len(notes) - 1)]
            bass_midi = root if (k // 2) % 2 == 0 else fifth
            if bass_midi > 50:
                bass_midi -= 12
            rng_b = np.random.default_rng(SEED + 9000 + k)
            bass = karplus(midi_hz(bass_midi), int(0.95 * SR), 0.993, rng_b)
            add_mono(lute, int(round(t * SR)), bass, (0.52, 0.48), 0.11)
        t += half
        k += 1
        if k % 40 == 0:
            log(f"  lute plucks through {t:.1f}s ({k})")
    log(f"lute events: {k}")

    dark = fir(900, 63)
    warm = fir(1700, 63)
    body = fir(380, 63)
    cut = int(round(ORCHARD * SR))
    viol[:cut] = apply_fir(viol[:cut], dark)
    rest = apply_fir(viol[cut:], warm)
    rest += 0.28 * apply_fir(rest, body)
    viol[cut:] = rest

    mix = lute + viol
    # Small chamber: a few combs, different on each side, never a long black tail.
    wet = np.zeros_like(mix)
    for channel, delays in ((0, (1483, 2011, 2551)), (1, (1601, 1879, 2341))):
        acc = np.zeros(n, np.float32)
        for delay, gain in zip(delays, (0.62, 0.55, 0.48)):
            acc += comb(mix[:, channel], delay, gain)
        wet[:, channel] = acc / 3.0
    mix = (0.78 * mix + 0.22 * wet).astype(np.float32)

    # 15 ms click-free start. The bed is already at musical level after that.
    atk = int(0.015 * SR)
    mix[:atk] *= np.linspace(0.0, 1.0, atk, dtype=np.float32)[:, None]
    # Keep the handoff sustaining through 178.28, then a short ring to 180.
    tail = int(round(WINDOW_END * SR))
    end = n
    if end > tail + 8:
        mix[tail:] *= np.linspace(1.0, 0.15, end - tail, dtype=np.float32)[:, None]
    return mix


def chord_at(spans, t: float) -> tuple[int, ...]:
    for a, b, notes in spans:
        if a <= t < b:
            return notes
    return spans[-1][2]


def rms(x: np.ndarray) -> float:
    arr = np.asarray(x, dtype=np.float64)
    return float(np.sqrt(np.mean(arr * arr))) + 1e-12


def match_levels(mix: np.ndarray, teach: Path) -> np.ndarray:
    head = load_audio(teach, 3.0)
    a = int(round(HANDOFF[0] * SR))
    b = int(round(HANDOFF[1] * SR))
    target = rms(head)
    have = rms(mix[a:b])
    # Raise only the handoff region if it sits more than 1 dB under the teach opening.
    ratio = target / have
    if ratio > 10 ** (1.0 / 20.0):
        ramp_a = int(round(171.0 * SR))
        ramp = np.ones(len(mix), np.float32)
        ramp[ramp_a:a] = np.linspace(1.0, ratio, a - ramp_a, dtype=np.float32)
        ramp[a:] = ratio
        mix = mix * ramp[:, None]
        log(f"handoff lift {20 * np.log10(ratio):.2f} dB so D4/A4 meets the teach opening")
    peak = float(np.max(np.abs(mix))) + 1e-9
    if peak > 0.89:
        mix = mix * (0.89 / peak)
    return mix.astype(np.float32)


def floor_report(mix: np.ndarray) -> dict:
    a = 0
    b = int(round(WINDOW_END * SR))
    hop = SR
    rows = []
    weak = []
    mono = mix[:b].mean(axis=1)
    for i, start in enumerate(range(0, b - hop + 1, hop)):
        level = 20.0 * np.log10(rms(mono[start:start + hop]))
        rows.append(round(float(level), 2))
        if level < -45.0:
            weak.append({"second": i, "rms_dbfs": round(float(level), 2)})
    return {
        "window_s": [0.0, WINDOW_END],
        "hop_s": 1.0,
        "rms_dbfs": rows,
        "min_rms_dbfs": min(rows) if rows else None,
        "below_minus_45": weak,
    }


def lift_floor(mix: np.ndarray, report: dict) -> np.ndarray:
    if not report["below_minus_45"]:
        return mix
    log(f"floor lift: {len(report['below_minus_45'])} one-second windows under -45 dBFS")
    spans = schedule()
    n = len(mix)
    safety = np.zeros(n, np.float32)
    for a, b, notes in spans:
        i0 = int(round(a * SR))
        i1 = min(n, int(round(b * SR)) + SR)
        hold = i1 - i0
        rng = np.random.default_rng(SEED + int(a * 10) + 77)
        tone = bowed(notes[0] + 12, hold, 0.04, rng, 4.4)
        safety[i0:i1] += tone
    # Bring the weakest second up to about -38 dBFS without swamping the lute.
    mono = mix.mean(axis=1)
    worst = min(report["rms_dbfs"])
    need = -38.0 - worst
    gain = float(10 ** (max(need, 0.0) / 20.0))
    peak = float(np.max(np.abs(safety))) + 1e-9
    safety = safety / peak * 0.08 * min(gain, 4.0)
    return (mix + safety[:, None]).astype(np.float32)


def silence_spans(path: Path, limit_s: float, hold: str) -> list[dict]:
    proc = sp.run(
        [
            "ffmpeg", "-hide_banner", "-i", str(path), "-t", f"{limit_s:.3f}",
            "-af", f"silencedetect=noise=-45dB:d={hold}", "-f", "null", "-",
        ],
        capture_output=True, text=True,
    )
    text = proc.stderr
    starts = [float(x) for x in re.findall(r"silence_start:\s*([0-9.]+)", text)]
    ends = [float(x) for x in re.findall(r"silence_end:\s*([0-9.]+)", text)]
    spans = []
    for i, start in enumerate(starts):
        end = ends[i] if i < len(ends) else limit_s
        if end <= 0.02:
            continue
        if start >= limit_s - 0.01:
            continue
        spans.append({"start_s": round(start, 3), "end_s": round(min(end, limit_s), 3), "hold_s": hold})
    return spans


def apply_lufs_match(path: Path, teach: Path) -> dict:
    teach_lufs = integrated_lufs(teach)
    mine = integrated_lufs(path)
    gain_db = teach_lufs - mine
    log(f"LUFS teach {teach_lufs:.2f} wonder {mine:.2f} gain {gain_db:.2f} dB")
    tmp = path.with_suffix(".match.wav")
    sp.run(
        [
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            "-i", str(path), "-af", f"volume={gain_db:.4f}dB",
            "-c:a", "pcm_s16le", "-ar", str(SR), "-ac", "2", str(tmp),
        ],
        check=True,
    )
    tmp.replace(path)
    after = integrated_lufs(path)
    # The global match can move the handoff off the teach opening. Put that
    # three-second window back, then leave the rest of the cue where it is.
    wonder = load_audio(path)
    head = load_audio(teach, 3.0)
    a = int(round(HANDOFF[0] * SR))
    b = int(round(HANDOFF[1] * SR))
    ratio = rms(head) / rms(wonder[a:b])
    correction_db = float(20.0 * np.log10(ratio))
    if abs(correction_db) > 0.6:
        ramp_a = int(round(172.0 * SR))
        ramp = np.ones(len(wonder), np.float32)
        ramp[ramp_a:a] = np.linspace(1.0, ratio, a - ramp_a, dtype=np.float32)
        ramp[a:b] = ratio
        wonder = wonder * ramp[:, None]
        peak = float(np.max(np.abs(wonder))) + 1e-9
        if peak > 0.98:
            wonder *= 0.98 / peak
        write_wav(path, wonder)
        after = integrated_lufs(path)
        log(f"handoff corrected by {correction_db:+.2f} dB after the loudness match")
        correction_db = 0.0
    return {
        "teach_lufs": teach_lufs,
        "wonder_before_lufs": mine,
        "gain_db": round(gain_db, 3),
        "wonder_after_lufs": after,
        "handoff_remaining_db": round(correction_db, 3),
    }


def render_wonder(teach: Path) -> dict:
    mix = synthesize()
    mix = match_levels(mix, teach)
    report = floor_report(mix)
    if report["below_minus_45"]:
        mix = lift_floor(mix, report)
        report = floor_report(mix)
    out = MUSIC / "hos_009_wonder_v03_synth.wav"
    write_wav(out, mix)
    loud = apply_lufs_match(out, teach)
    # Re-check the floor after the loudness match. Matching teach should only make it hotter.
    matched = load_audio(out, WINDOW_END + 0.05)
    report = floor_report(matched)
    sil_025 = silence_spans(out, WINDOW_END, "0.25")
    sil_050 = silence_spans(out, WINDOW_END, "0.50")
    if report["below_minus_45"] or sil_025 or sil_050:
        raise SystemExit(
            f"continuity fail after render: rms {report['below_minus_45']} "
            f"silence 0.25 {sil_025} silence 0.50 {sil_050}"
        )
    log(f"wonder floor min {report['min_rms_dbfs']} dBFS, silence spans 0")
    return {"loudness": loud, "floor": report, "silence_0_25": sil_025, "silence_0_50": sil_050}


def write_plan(path: Path, bed_name: str, prompt: str, extra: dict) -> None:
    payload = {
        "film": "009_The-Falling-Moon-Gravity",
        "job": "J3234",
        "bed": bed_name,
        "source": "own synthesis (_build_hos009_wonder_v03_synth.py), £0, no ElevenLabs, no samples",
        "prompt": prompt,
    }
    payload.update(extra)
    path.write_text(json.dumps(payload, indent=2) + "\n")


def join_and_stems(teach: Path) -> Path:
    wonder = MUSIC / "hos_009_wonder_v03_synth.wav"
    joined = MUSIC / "hos_009_score_joined_v03.wav"
    log("joining wonder[0:178.28] to teach with a 3.0s equal-power crossfade")
    sp.run(
        [
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            "-i", str(wonder), "-i", str(teach),
            "-filter_complex",
            "[0:a]atrim=end=178.28,asetpts=PTS-STARTPTS,aformat=sample_rates=48000:channel_layouts=stereo[a0];"
            "[1:a]aformat=sample_rates=48000:channel_layouts=stereo[a1];"
            "[a0][a1]acrossfade=d=3:c1=qsin:c2=qsin[out]",
            "-map", "[out]", "-c:a", "pcm_s16le", "-ar", str(SR), "-ac", "2", str(joined),
        ],
        check=True,
    )
    stems = [
        ("hos_009_stem_part01_the_falling_moon_v03.wav", 0.0, 84.44),
        ("hos_009_stem_part02_an_apple_in_a_plague_year_v03.wav", 84.44, 176.78),
        ("hos_009_stem_part03_the_cannon_on_the_mountain_v03.wav", 176.78, 260.16),
        ("hos_009_stem_part04_the_moon_test_v03.wav", 260.16, 393.86),
        ("hos_009_stem_part05_falling_around_the_world_v03.wav", 393.86, 535.28),
    ]
    for name, a, b in stems:
        dest = MUSIC / name
        sp.run(
            [
                "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
                "-i", str(joined),
                "-af", f"atrim=start={a:.2f}:end={b:.2f},asetpts=PTS-STARTPTS",
                "-c:a", "pcm_s16le", "-ar", str(SR), "-ac", "2", str(dest),
            ],
            check=True,
        )
        log(f"  stem {name} {probe_duration(dest):.3f}s")
    return joined


def build_review(joined: Path, loudness: dict) -> dict:
    REVIEW.mkdir(parents=True, exist_ok=True)
    bed = load_audio(joined)
    vo = np.zeros_like(bed)
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
    vo_lufs_proxy = 20.0 * np.log10(rms(vo[: int(518.40 * SR)]) + 1e-12)
    bed_lufs = loudness["wonder_after_lufs"]
    # HOS 009 audition parity used by the v02 listening review was -16 dB.
    # Keep the bed at least 10 LU under the placed narration.
    gain_db = -16.0
    if vo_lufs_proxy - (bed_lufs + gain_db) < 10.0:
        gain_db = (vo_lufs_proxy - 12.0) - bed_lufs
    gain = float(10 ** (gain_db / 20.0))
    mix = vo + bed * gain
    peak = float(np.max(np.abs(mix))) + 1e-9
    if peak > 0.98:
        mix *= 0.98 / peak
    def cut(buf: np.ndarray, a: float, b: float | None) -> np.ndarray:
        i = int(round(a * SR))
        j = len(buf) if b is None else int(round(b * SR))
        return buf[i:j]

    files = {
        "transition_168_186_bed": REVIEW / "hos_009_transition_168_186_bed_v03.wav",
        "transition_168_186_mix": REVIEW / "hos_009_transition_168_186_mix_v03.wav",
        "reference_mix_0_518s40": REVIEW / "hos_009_reference_mix_0_518s40_v03.wav",
        "tail_518s40": REVIEW / "hos_009_tail_518s40_v03.wav",
        "reference_endpoint_526s": REVIEW / "hos_009_reference_endpoint_526s_v03.wav",
    }
    write_wav(files["transition_168_186_bed"], cut(bed, 168.0, 186.0))
    write_wav(files["transition_168_186_mix"], cut(mix, 168.0, 186.0))
    write_wav(files["reference_mix_0_518s40"], cut(mix, 0.0, 518.40))
    write_wav(files["tail_518s40"], cut(mix, 518.40, None))
    write_wav(files["reference_endpoint_526s"], cut(mix, 0.0, 526.0))
    return {
        "bed_gain_db": round(gain_db, 3),
        "vo_placed_rms_dbfs": round(vo_lufs_proxy, 2),
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
    ]
    # One or two levels only. A full **/ walk enters archived render trees and
    # stalls on the NAS. Beds sit directly inside each film's 05_Music.
    patterns = {
        "mac-mini-archive/YouTube": ("*/02_Video-Projects/*/05_Music/*",),
        "mac-mini-archive/orbit-with-ben": ("02_Video-Projects/*/05_Music/*",),
        "mac-mini-archive/youtube-staging": ("*/05_Music/*", "*/*/05_Music/*"),
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
                if path.name.startswith("._"):
                    continue
                if "009_The-Falling-Moon-Gravity" in path.parts:
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
    report.append({"root": "uat-materialized", "state": "listed", "files": len(uat), "replaces": "icloud HOS UAT + OWB UAT stubs"})
    log(f"library uat materialized: {len(uat)}")
    # Stable order, drop duplicate paths.
    uniq = []
    seen = set()
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
        f"music gate {result['verdict']}: {bed.name} comparisons {result['comparison_count']} "
        f"max {result['max_similarity']} unreadable {result['unreadable_warn_count']}"
    )
    if result["verdict"] != "PASS" or result["unreadable_warn_count"] or result["comparison_count"] < 89:
        raise SystemExit(f"music gate did not pass for {bed.name}")
    if result["max_similarity"] >= 0.8:
        raise SystemExit(f"similarity {result['max_similarity']} is at the fail line")
    return result


def verify_locks() -> dict:
    expected = {
        MUSIC / "hos_009_teach_v01.mp3": TEACH_SHA,
        MUSIC / "hos_009_wonder_v01.mp3": "95dfe11d7c21c9347e9b962ef2f9ecd35116f2fce60df6f123578c11a1debaf0",
        MUSIC / "hos_009_wonder_v02.mp3": "b38ae8922e8d633b9f085a8bb9634c96d889a9293fcab277f7a3a23f4839d148",
        MUSIC / "hos_009_score_joined_v01.wav": "d7f5bf3d7553d7c611a913e93602b8ec83419821059294ddeaee32269a4f9572",
        MUSIC / "hos_009_score_joined_v02.wav": "6fc8628a96b8267eaf5be6c19d7e30d9e473eb86c886ee3106c3219b375b1f68",
        VO / "VO_TAKES_KEEP.json": "530743c507af8d5f9049179d4e9d380b5c1b8aca4f180ada133d0b673f5925e0",
        FILM / "07_Edit-Project/VO_RETIME_v01.json": "75a2e7afa1d822b04371511c81a52082e1b80713b0e59711702cfd05fe45a972",
    }
    found = {}
    for path, want in expected.items():
        if not path.exists():
            raise SystemExit(f"missing lock {path}")
        got = sha256_file(path)
        if got != want:
            raise SystemExit(f"lock changed {path.name}: {got} != {want}")
        found[path.name] = got
    for name in (
        "J2631_code_graphic_009_p4_05_minute_second.mp4",
        "J2632_r4_code_graphic_009_p3_01_really_falling_c1.mp4",
    ):
        hits = list(FILM.rglob(name))
        if not hits:
            log(f"diagram lock not in the film folder: {name}")
            continue
        found[name] = sha256_file(hits[0])
    log("preserved locks match the scope hashes")
    return found


def mirror_nas(paths: list[Path]) -> dict:
    if not Path("/Volumes/data/studio-live").is_dir():
        raise SystemExit("studio-live is not mounted; NAS parity cannot be checked")
    NAS.mkdir(parents=True, exist_ok=True)
    (NAS / "audio_review_v03_synth").mkdir(parents=True, exist_ok=True)
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


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--from", dest="start", choices=["synth", "join", "gates", "nas"], default="synth")
    args = parser.parse_args()
    MUSIC.mkdir(parents=True, exist_ok=True)
    locks = verify_locks()
    teach = MUSIC / "hos_009_teach_v01.mp3"
    if probe_duration(teach) < 360.0:
        raise SystemExit("teach cue is shorter than the retained 360s file")

    continuity = {}
    if args.start == "synth":
        continuity = render_wonder(teach)
        (MUSIC / "CONTINUITY_v03_synth.json").write_text(json.dumps({
            "job": "J3234",
            "silence_noise_db": -45,
            "silence_holds_s": [0.25, 0.50],
            "silence_0_25": continuity["silence_0_25"],
            "silence_0_50": continuity["silence_0_50"],
            "one_second_rms": continuity["floor"],
            "loudness": continuity["loudness"],
            "interior_dropouts": 0,
        }, indent=2) + "\n")
        write_plan(
            MUSIC / "hos_009_wonder_v03_synth_plan.json",
            "hos_009_wonder_v03_synth.wav",
            WONDER_PROMPT,
            {
                "duration_s": RAW_S,
                "used_window_s": [0.0, WINDOW_END],
                "bpm": BPM,
                "key": "D minor",
                "a4_hz": 440,
                "sha256": sha256_file(MUSIC / "hos_009_wonder_v03_synth.wav"),
                "integrated_lufs": continuity["loudness"]["wonder_after_lufs"],
            },
        )
    else:
        continuity = json.loads((MUSIC / "CONTINUITY_v03_synth.json").read_text())

    if args.start in ("synth", "join"):
        joined = join_and_stems(teach)
        review = build_review(joined, continuity["loudness"] if "loudness" in continuity else continuity)
        write_plan(
            MUSIC / "hos_009_score_joined_v03_plan.json",
            "hos_009_score_joined_v03.wav",
            JOINED_PROMPT,
            {
                "duration_s": probe_duration(joined),
                "crossfade": {
                    "start_s": 175.28,
                    "end_s": 178.28,
                    "duration_s": 3.0,
                    "ffmpeg": "acrossfade=d=3:c1=qsin:c2=qsin",
                    "chapter_card_s": 176.78,
                },
                "teach_sha256": TEACH_SHA,
                "teach_duration_s": probe_duration(teach),
                "sha256": sha256_file(joined),
                "audition": review,
            },
        )
        side = MUSIC / "CONTINUITY_v03_synth.json"
        payload = json.loads(side.read_text())
        payload["audition"] = review
        payload["joined_duration_s"] = probe_duration(joined)
        payload["joined_lufs"] = integrated_lufs(joined)
        payload["vo_lufs"] = {
            "part01": -20.3,
            "part02": -19.5,
            "part03": -20.4,
            "part04": -20.5,
            "part05": -20.9,
            "source": "VO_TAKES_KEEP.json locked integrated readings",
        }
        side.write_text(json.dumps(payload, indent=2) + "\n")

    if args.start in ("synth", "join", "gates"):
        others, roots = collect_library()
        if len(others) < 89:
            raise SystemExit(f"library has {len(others)} readable beds, need at least 89")
        run_gate(MUSIC / "hos_009_wonder_v03_synth.wav", others, MUSIC / "music_gate_v03_wonder.json", roots)
        run_gate(MUSIC / "hos_009_score_joined_v03.wav", others, MUSIC / "music_gate_v03_joined.json", roots)

    text_and_media = [
        MUSIC / "_build_hos009_wonder_v03_synth.py",
        MUSIC / "hos_009_wonder_v03_synth.wav",
        MUSIC / "hos_009_wonder_v03_synth_plan.json",
        MUSIC / "hos_009_score_joined_v03.wav",
        MUSIC / "hos_009_score_joined_v03_plan.json",
        MUSIC / "hos_009_stem_part01_the_falling_moon_v03.wav",
        MUSIC / "hos_009_stem_part02_an_apple_in_a_plague_year_v03.wav",
        MUSIC / "hos_009_stem_part03_the_cannon_on_the_mountain_v03.wav",
        MUSIC / "hos_009_stem_part04_the_moon_test_v03.wav",
        MUSIC / "hos_009_stem_part05_falling_around_the_world_v03.wav",
        MUSIC / "PROVENANCE_v03_synth.json",
        MUSIC / "music_gate_v03_wonder.json",
        MUSIC / "music_gate_v03_joined.json",
        MUSIC / "CONTINUITY_v03_synth.json",
    ]
    text_and_media += sorted(REVIEW.glob("*.wav"))
    # Provenance is written before the NAS copy, then rewritten with NAS hashes
    # and copied last so both sides match.
    local_rows = []
    for path in text_and_media:
        if path.name == "PROVENANCE_v03_synth.json" or not path.exists():
            continue
        local_rows.append({"file": str(path.relative_to(MUSIC)), "sha256": sha256_file(path), "bytes": path.stat().st_size})
    provenance = {
        "job": "J3234",
        "scope_job": "J3233",
        "film": "HOS:009",
        "cash_spent_gbp": 0,
        "subscription_credits": 0,
        "elevenlabs_posts": 0,
        "method": "deterministic pure Python/NumPy Karplus-Strong lute and bowed viols",
        "activation_authorized": False,
        "preserved_locks": locks,
        "teach_unchanged_sha256": sha256_file(teach),
        "local_files": local_rows,
        "ear_review_pass_claimed": False,
        "score_accepted": False,
    }
    prov_path = MUSIC / "PROVENANCE_v03_synth.json"
    prov_path.write_text(json.dumps(provenance, indent=2) + "\n")
    copy_paths = [p for p in text_and_media if p.exists()]
    if prov_path not in copy_paths:
        copy_paths.append(prov_path)
    nas = mirror_nas(copy_paths)
    provenance["nas_parity"] = nas
    prov_path.write_text(json.dumps(provenance, indent=2) + "\n")
    # The provenance file changed after the first copy. Copy that one file again.
    nas_prov = NAS / prov_path.name
    nas_prov.write_bytes(prov_path.read_bytes())
    if sha256_file(nas_prov) != sha256_file(prov_path):
        raise SystemExit("provenance NAS parity failed")
    log("done")
    return 0


if __name__ == "__main__":
    sys.exit(main())
