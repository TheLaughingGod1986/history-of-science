#!/usr/bin/env python3
"""HOS 008 master v02 (J1287, Chief h29). Bed seam only. No ElevenLabs call.

Picture is the locked rough v12 stream, copied. The bed is
lightning008_score_bed_v01_take.mp3 only: film 0.0 plays the take from 50.70 s,
one 15-bar mid-body repeat (54.0 s at 66.7 BPM) joins on a 3.0 s equal-power
crossfade, and the take's fade-out sits at the film end. The last ~0.7 s of the
take file is silence, so the musical ending is kept.
"""
from __future__ import annotations

import hashlib
import json
import re
import shutil
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
DESK = Path("/Volumes/data/mac-mini-archive/YouTube/History Of Science/02_Video-Projects/008_Lightning-Franklin/07_Edit-Project/_desk/008/master_v02")
PACK = FILM / "07_Edit-Project/master_v02"
PRE = FILM / "07_Edit-Project/_precheck/master_v02"
TAKE = NAS / "stem_bed_raw.wav"  # decoded v01 take, already on the scratch disk
VO = NAS / "stem_vo_v12.wav"
SFX_IN = NAS / "stem_sfx_v01.wav"
WHOOSH = FILM / "06_Sound-Effects/kit_v01/sfx_hos_whoosh_soft_v01.wav"
SR = 48000
TAKE_START = 50.70
BAR = 3.6          # 4 beats at 60/66.666... s = 0.9 s, the grid music_gate calls 66.7 BPM
LOOP = 15 * BAR    # 54.0 s, the shortest bar-multiple whose crossfade fits 1.5–3 s
XFADE = 3.0
S0 = int(round(TAKE_START * SR))
LOOP_N = int(round(LOOP * SR))
XF_N = int(round(XFADE * SR))
BAR_N = int(round(BAR * SR))
CARDS = (100.25, 187.95, 319.00, 408.96)  # locked part starts, hold 1.5 s
CARD_HOLD = 1.5
# Chapter whooshes. Body must end at least 0.10 s before the named word.
WHOOSH_MOVES = (
    {"name": "ch2", "old": 100.05, "word": 100.46, "clear": 0.10},
    {"name": "ch3", "old": 187.75, "word": 188.54, "clear": 0.10},
)


def read_wav(p: Path) -> np.ndarray:
    with wave.open(str(p)) as w:
        if w.getframerate() != SR:
            raise SystemExit(f"{p} is {w.getframerate()} Hz, want {SR}")
        x = np.frombuffer(w.readframes(w.getnframes()), dtype="<i2").astype(np.float32)
        x = x.reshape(-1, w.getnchannels()) / 32768.0
        if x.shape[1] == 1:
            x = np.repeat(x, 2, axis=1)
        return x


def write_wav(p: Path, x: np.ndarray) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    pcm = np.clip(x, -1, 1)
    with wave.open(str(p), "w") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes((pcm * 32767.0).astype("<i2").tobytes())


def sha256(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def rms_db(x: np.ndarray) -> float:
    return float(20 * np.log10(np.sqrt(np.mean(np.square(x)) + 1e-20)))


def frame_rms_db(mono: np.ndarray, hop: int) -> np.ndarray:
    n = len(mono) // hop
    x = mono[: n * hop].reshape(n, hop)
    return 20 * np.log10(np.sqrt(np.mean(np.square(x), axis=1) + 1e-20))


def chroma(mono: np.ndarray) -> np.ndarray:
    n = 4096
    hop = 2048
    if len(mono) < n:
        mono = np.pad(mono, (0, n - len(mono)))
    window = np.hanning(n).astype(np.float32)
    freqs = np.fft.rfftfreq(n, 1 / SR)
    acc = np.zeros(12, dtype=np.float64)
    for i in range(0, len(mono) - n, hop):
        mag = np.abs(np.fft.rfft(mono[i : i + n] * window))
        for k, f in enumerate(freqs):
            if f < 80 or f > 4000:
                continue
            midi = 69 + 12 * np.log2(f / 440.0)
            acc[int(np.round(midi)) % 12] += mag[k]
    acc /= np.linalg.norm(acc) + 1e-12
    return acc


def lufs_of(x: np.ndarray) -> float:
    tmp = NAS / "_lufs_snip.wav"
    write_wav(tmp, x if x.ndim == 2 else np.repeat(x[:, None], 2, axis=1))
    _m, integ = sfx_kit.ebur128(tmp)
    return float(integ)


def runs_of(mask: np.ndarray):
    out, start = [], None
    for i, flag in enumerate(list(mask) + [False]):
        if flag and start is None:
            start = i
        elif not flag and start is not None:
            out.append((start, i - start))
            start = None
    return out


def gap(a0: float, a1: float, b0: float, b1: float) -> float:
    if a1 <= b0:
        return b0 - a1
    if b1 <= a0:
        return a0 - b1
    return 0.0


def beat_phase(mono: np.ndarray) -> float:
    """Downbeat offset in seconds. Beat period is 0.9 s (music_gate's 66.7 BPM)."""
    hop = SR // 20
    n = len(mono) // hop
    env = np.sqrt(np.mean(mono[: n * hop].reshape(n, hop) ** 2, axis=1) + 1e-12)
    onset = np.maximum(np.diff(np.log1p(env * 100)), 0.0)
    # Musical body only: after the opening hole, before the final fade.
    a, b = int(60 / 0.05), int(500 / 0.05)
    onset = onset[a:b]
    period = 18  # 0.9 s / 0.05 s
    scores = [float(onset[p::period].sum()) for p in range(period)]
    best = int(np.argmax(scores))
    # Bar line is the strongest beat, then every 4 beats.
    return (a + best) * 0.05


def vo_mask(vo_m, vo_i):
    vm = np.array(vo_m, dtype=np.float64)
    speaking = (vm > sfx_kit.SILENT) & (vm >= vo_i - sfx_kit.SPEAKING_WITHIN)
    pauses = []
    for s, ln in runs_of(~speaking):
        if ln >= 8:
            pauses.append((s * 0.1, (s + ln) * 0.1))
    return speaking, pauses


def seam_ok(speaking, pauses, fade0: float, fade1: float) -> str | None:
    """None when the crossfade sits under running VO, else a short reason."""
    i0 = int(np.floor(fade0 / 0.1))
    i1 = int(np.ceil(fade1 / 0.1))
    i0 = max(0, i0)
    i1 = min(len(speaking), i1)
    if i1 <= i0 or not bool(speaking[i0:i1].all()):
        return "not under running VO"
    for p0, p1 in pauses:
        if gap(fade0, fade1, p0, p1) < 2.0:
            return f"within 2 s of a pause {p0:.2f}-{p1:.2f}"
    for card in CARDS:
        if gap(fade0, fade1, card, card + CARD_HOLD) < 2.0:
            return f"within 2 s of chapter card {card:.2f}"
    return None


def stitch(take: np.ndarray, b: int, end: int) -> np.ndarray:
    a = b + LOOP_N
    head = take[S0:a]
    tail = take[b:end]
    n = len(head) + len(tail) - XF_N
    out = np.empty((n, 2), dtype=np.float32)
    out[: len(head) - XF_N] = head[:-XF_N]
    t = np.linspace(0, np.pi / 2, XF_N, endpoint=False, dtype=np.float32)
    out[len(head) - XF_N : len(head)] = head[-XF_N:] * np.cos(t)[:, None] + tail[:XF_N] * np.sin(t)[:, None]
    out[len(head) :] = tail[XF_N:]
    return out


def quiet_stretches(x: np.ndarray, skip_end: float = 25.0) -> list[dict]:
    hop = SR // 10
    mono = x.mean(axis=1) if x.ndim == 2 else x
    db = frame_rms_db(mono, hop)
    n = len(db)
    end = max(0, n - int(skip_end * 10))
    body = db[:end]
    if len(body) < 20:
        return []
    med = float(np.median(body))
    quiet = body < med - 6.0
    found = []
    for s, ln in runs_of(quiet):
        if ln >= 60:
            found.append({"start": round(s * 0.1, 2), "seconds": round(ln * 0.1, 2), "median_db": round(med, 2)})
    return found


def spectral_flux(mono: np.ndarray) -> np.ndarray:
    n = 2048
    hop = 1024
    window = np.hanning(n).astype(np.float32)
    mags = []
    for i in range(0, len(mono) - n, hop):
        mags.append(np.abs(np.fft.rfft(mono[i : i + n] * window)))
    mag = np.stack(mags)
    delta = np.diff(mag, axis=0)
    return np.sqrt(np.sum(np.square(np.maximum(delta, 0)), axis=1))


def seam_report(bed: np.ndarray, b: int, end: int) -> dict:
    a = b + LOOP_N
    fade0 = (a - S0 - XF_N) / SR
    fade1 = (a - S0) / SR
    centre = (fade0 + fade1) / 2
    c = int(round(centre * SR))
    left = bed[c - 2 * SR : c]
    right = bed[c : c + 2 * SR]
    rms_l, rms_r = rms_db(left), rms_db(right)
    lu_l, lu_r = lufs_of(left), lufs_of(right)
    mono = bed.mean(axis=1)
    d2 = np.abs(np.diff(mono, n=2))
    # Body excludes the crossfade and the final ending.
    body = np.ones(len(d2), dtype=bool)
    body[int(fade0 * SR) : int(fade1 * SR)] = False
    body[int((len(mono) / SR - 25) * SR) :] = False
    click_body = float(d2[body].max()) if body.any() else 1.0
    click_seam = float(d2[int(fade0 * SR) : int(fade1 * SR)].max())
    flux = spectral_flux(mono)
    hop = 1024 / SR
    seam_frames = (flux[(np.arange(len(flux)) * hop >= fade0) & (np.arange(len(flux)) * hop <= fade1)])
    body_flux = flux[np.arange(len(flux)) * hop < (len(mono) / SR - 25)]
    # Drop the seam frames from the body percentile.
    body_mask = (np.arange(len(flux)) * hop < fade0 - 1) | (
        (np.arange(len(flux)) * hop > fade1 + 1) & (np.arange(len(flux)) * hop < len(mono) / SR - 25)
    )
    p999 = float(np.percentile(flux[body_mask], 99.9)) if body_mask.any() else 0.0
    flux_seam = float(seam_frames.max()) if len(seam_frames) else 0.0
    holes = quiet_stretches(bed)
    ok = (
        abs(rms_l - rms_r) <= 1.0
        and abs(lu_l - lu_r) <= 1.0
        and click_seam <= click_body + 1e-9
        and flux_seam <= p999 + 1e-6
        and not holes
    )
    return {
        "ok": ok,
        "seam_centre_s": round(centre, 3),
        "fade_s": [round(fade0, 3), round(fade1, 3)],
        "xfade_s": XFADE,
        "source_in_s": round(b / SR, 3),
        "source_out_s": round(a / SR, 3),
        "take_end_s": round(end / SR, 3),
        "rms_db": [round(rms_l, 2), round(rms_r, 2)],
        "rms_delta_db": round(abs(rms_l - rms_r), 3),
        "short_term_lufs": [round(lu_l, 2), round(lu_r, 2)],
        "lufs_delta": round(abs(lu_l - lu_r), 3),
        "click_seam": click_seam,
        "click_body_max": click_body,
        "click_ok": click_seam <= click_body + 1e-9,
        "flux_seam": flux_seam,
        "flux_body_p999": p999,
        "flux_ok": flux_seam <= p999 + 1e-6,
        "quiet_stretches": holes,
    }


def choose_seam(take: np.ndarray, speaking, pauses, end: int) -> tuple[int, list[dict]]:
    mono = take.mean(axis=1)
    phase = beat_phase(mono)
    phase_n = int(round(phase * SR)) % BAR_N
    print(f"bar phase {phase_n / SR:.3f} s", flush=True)
    ranked = []
    b = phase_n
    while b < 110 * SR:
        b += BAR_N
    limit = end - 25 * SR - LOOP_N
    while b <= limit:
        a = b + LOOP_N
        fade0 = (a - S0 - XF_N) / SR
        fade1 = (a - S0) / SR
        why = seam_ok(speaking, pauses, fade0, fade1)
        # Match the two bars that the crossfade blends. The aired seam is
        # measured later, on the crossfade itself.
        left = mono[a - XF_N : a]
        right = mono[b : b + XF_N]
        delta = abs(rms_db(left) - rms_db(right))
        row = {
            "b_s": round(b / SR, 3),
            "fade": [round(fade0, 3), round(fade1, 3)],
            "rms_delta_db": round(delta, 3),
            "rejected": why,
        }
        if why is None and delta <= 2.0:
            cos = float(np.dot(chroma(mono[a - XF_N : a]), chroma(mono[b : b + XF_N])))
            row["chroma"] = round(cos, 4)
            row["score"] = round(delta + 3 * (1 - cos), 4)
            row["b_n"] = int(b)
            ranked.append((row["score"], b, row))
        elif why is None:
            row["rejected"] = f"rms sides differ by {delta:.2f} dB"
        b += BAR_N
    ranked.sort(key=lambda r: r[0])
    print(f"vo-legal level-matched seams: {len(ranked)}", flush=True)
    return (ranked[0][1] if ranked else -1), [r[2] for r in ranked[:8]]


def apply_frame_db(x: np.ndarray, frame_db: np.ndarray) -> np.ndarray:
    grid = np.arange(len(frame_db)) * 0.1
    t = np.arange(len(x)) / SR
    env = np.interp(t, grid, frame_db, left=float(frame_db[0]), right=float(frame_db[-1]))
    win = int(0.04 * SR)
    if win > 1:
        env = np.convolve(env, np.ones(win) / win, mode="same")
    return x * (10.0 ** (env / 20.0))[:, None]


def speech_stats(vm, bm, vo_i, speaking):
    n = min(len(vm), len(bm), len(speaking))
    vm, bm, sp = vm[:n], bm[:n], speaking[:n]
    audible = sp & (bm > sfx_kit.SILENT)
    d = vm[audible] - bm[audible]
    long = np.zeros(n, dtype=bool)
    for s, ln in runs_of(~sp):
        if ln >= 8:
            long[s : s + ln] = True
    lp = long & (bm > sfx_kit.SILENT)
    breach = sp & (bm > sfx_kit.SILENT) & ((vm - bm) < 10)
    worst = cur = count = 0
    for flag in breach:
        if flag:
            cur += 1
            worst = max(worst, cur)
        else:
            if cur >= 3:
                count += 1
            cur = 0
    if cur >= 3:
        count += 1
    pause_under = float((vo_i - bm[lp]).mean()) if lp.any() else None
    return {
        "speech_mean": round(float(d.mean()), 2) if len(d) else None,
        "min": round(float(d.min()), 2) if len(d) else None,
        "long_pause_under_i": round(pause_under, 2) if pause_under is not None else None,
        "breach_runs_0.3s": count,
        "worst_breach_frames": worst,
        "pause_above_speech": round(float(d.mean()) - pause_under, 2) if pause_under is not None and len(d) else None,
    }


def duck_bed(raw: np.ndarray, vo_m, vo_i, speaking) -> tuple[np.ndarray, dict]:
    tmp = NAS / "stem_bed_v02_raw.wav"
    write_wav(tmp, raw)
    bed_m, _bed_i = sfx_kit.ebur128(tmp)
    vm = np.array(vo_m, dtype=np.float64)
    bm = np.array(bed_m[: len(vm)], dtype=np.float64)
    n = min(len(vm), len(bm), len(speaking))
    vm, bm, sp = vm[:n], bm[:n], speaking[:n]
    before = speech_stats(vm, bm, vo_i, sp)
    print("duck before", before, flush=True)
    audible = sp & (bm > sfx_kit.SILENT)
    current = float((vm[audible] - bm[audible]).mean())
    global_db = current - 18.5
    gain = np.full(n, global_db, dtype=np.float64)
    bm2 = bm + global_db
    d = vm - bm2
    # Extra duck where speech would still sit closer than 16.5 LU. Cap 8 dB.
    extra = np.where(sp & (d < 16.5), np.clip(18.5 - d, 0, 8), 0.0)
    gain -= extra
    bm3 = bm + gain
    for s, ln in runs_of(~sp):
        if ln < 8:
            continue
        a, b = s + 2, s + ln - 2
        if b <= a:
            a, b = s, s + ln
        # Pauses land about 13 LU under the VO's integrated level, so they sit
        # at least 2.5 LU louder than speech parked near 18.5.
        want = np.clip((vo_i - 13.0) - bm3[a:b], 0, 12)
        gain[a:b] = np.maximum(gain[a:b], global_db + want)
    print(f"duck gain min {gain.min():.2f} max {gain.max():.2f}", flush=True)
    out = apply_frame_db(raw[: int(n * 0.1 * SR) + SR], gain)
    if len(out) < len(raw):
        pad = np.zeros((len(raw) - len(out), 2), dtype=np.float32)
        out = np.concatenate([out, pad])
    out = out[: len(raw)]
    ducked = NAS / "stem_bed_v02.wav"
    write_wav(ducked, out)
    bed_m, bed_i = sfx_kit.ebur128(ducked)
    bm = np.array(bed_m[:n], dtype=np.float64)
    after = speech_stats(vm, bm, vo_i, sp)
    after["bed_integrated"] = round(float(bed_i), 2)
    after["vo_integrated"] = round(float(vo_i), 2)
    after["before"] = before
    print("duck after", {k: after[k] for k in after if k != "before"}, flush=True)
    return out, after


def whoosh_body_offset() -> float:
    """Seconds from the file start to the end of the loud body (within 6 dB of peak)."""
    x = read_wav(WHOOSH).mean(axis=1)
    db = frame_rms_db(x, SR // 100)
    peak = float(db.max())
    hot = np.where(db >= peak - 6.0)[0]
    if len(hot) == 0:
        raise SystemExit("whoosh has no body")
    return (int(hot[-1]) + 1) / 100.0


def move_whooshes(sfx: np.ndarray) -> tuple[np.ndarray, list[dict]]:
    body = whoosh_body_offset()
    print(f"whoosh body ends at {body:.2f} s into the file", flush=True)
    out = sfx.copy()
    notes = []
    for spec in WHOOSH_MOVES:
        old = int(round(spec["old"] * SR))
        length = SR  # the kit whoosh is 1.00 s
        new_s = (spec["word"] - spec["clear"]) - body
        new = int(round(new_s * SR))
        if new < 0 or new + length > len(out) or old + length > len(out):
            raise SystemExit(f"{spec['name']} whoosh would leave the stem")
        dest_before = out[new:old] if new < old else np.zeros((0, 2))
        if len(dest_before) and float(np.max(np.abs(dest_before))) > 0.002:
            raise SystemExit(f"{spec['name']} destination is not silent ({np.max(np.abs(dest_before)):.4f})")
        seg = out[old : old + length].copy()
        out[old : old + length] = 0
        out[new : new + length] = seg
        notes.append({
            "name": spec["name"],
            "old_start": spec["old"],
            "new_start": round(new / SR, 3),
            "body_end": round(new / SR + body, 3),
            "word": spec["word"],
            "clear_s": round(spec["word"] - (new / SR + body), 3),
        })
        print(f"{spec['name']} whoosh {spec['old']:.2f} -> {new / SR:.3f}, body ends {new / SR + body:.3f}", flush=True)
    return out, notes


def loudnorm_measure(vo, bed, sfx) -> dict:
    fc = "[0:a][1:a][2:a]amix=inputs=3:normalize=0:duration=first,alimiter=limit=0.89:level=false:latency=true"
    r = sp.run(
        ["ffmpeg", "-hide_banner", "-i", str(vo), "-i", str(bed), "-i", str(sfx),
         "-filter_complex", fc + ",loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json[a]",
         "-map", "[a]", "-f", "null", "-"],
        capture_output=True, text=True,
    )
    if r.returncode:
        raise SystemExit(r.stderr[-1500:])
    return json.loads(re.findall(r'\{[^{}]*"input_i"[^{}]*\}', r.stderr, re.S)[-1])


def decode_at(path: Path, ss: float, seconds: float = 8.0) -> np.ndarray:
    raw = sp.check_output(
        ["ffmpeg", "-v", "error", "-ss", str(ss), "-t", str(seconds), "-i", str(path),
         "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"]
    )
    return np.frombuffer(raw, dtype=np.float32)


def lag_ms(ref: np.ndarray, mix: np.ndarray) -> float:
    n = min(len(ref), len(mix))
    a = ref[:n] - ref[:n].mean()
    b = mix[:n] - mix[:n].mean()
    step = 4
    a, b = a[::step], b[::step]
    corr = np.correlate(b, a, mode="full")
    lag = int(np.argmax(corr) - (len(a) - 1))
    return lag * step / SR * 1000.0


def stream_md5(path: Path) -> str:
    r = sp.run(["ffmpeg", "-v", "error", "-i", str(path), "-map", "0:v:0", "-c", "copy", "-f", "md5", "-"],
               capture_output=True, text=True)
    if r.returncode:
        raise SystemExit(r.stderr[-500:])
    return r.stdout.strip().split("=")[-1]


def probe(path: Path) -> dict:
    r = sp.check_output(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-show_entries",
         "stream=codec_type,start_time,duration,nb_frames", "-of", "json", str(path)],
        text=True,
    )
    return json.loads(r)


def align_vo() -> tuple[Path, np.ndarray]:
    """The stored VO wav is the v12 AAC decode with its priming left in.

    Drop that delay so sample 0 matches the locked picture, then cut to the
    v12 duration. 944 samples (19.667 ms) is the delay this take measures.
    """
    film_n = int(round(539.626479 * SR))
    src = read_wav(VO)
    ref = decode_at(V12, 40.0, 5.0)
    window = src.mean(axis=1)[40 * SR : 40 * SR + len(ref) + 4000]
    a = ref - ref.mean()
    b = window[: len(a) + 4000] - window[: len(a) + 4000].mean()
    corr = np.correlate(b[::2], a[::2], mode="full")
    lag = int(np.argmax(corr) - (len(a[::2]) - 1)) * 2
    print(f"VO priming delay {lag} samples ({lag / SR * 1000:.3f} ms)", flush=True)
    if not 0 <= lag <= 4000:
        raise SystemExit(f"unexpected VO delay {lag}")
    vo = src[lag : lag + film_n]
    if len(vo) != film_n:
        raise SystemExit(f"aligned VO is {len(vo)} samples, film is {film_n}")
    path = NAS / "stem_vo_v12_film.wav"
    write_wav(path, vo)
    check = decode_at(path, 40.0, 5.0)
    n = min(len(check), len(ref))
    corr = np.correlate(check[:n] - check[:n].mean(), ref[:n] - ref[:n].mean(), mode="full")
    residual = int(np.argmax(corr) - (n - 1))
    print(f"aligned VO residual {residual} samples", flush=True)
    if abs(residual) > 1:
        raise SystemExit(f"VO still {residual} samples off v12")
    return path, vo


def main() -> int:
    PACK.mkdir(parents=True, exist_ok=True)
    PRE.mkdir(parents=True, exist_ok=True)
    if not TAKE.exists() or not VO.exists() or not SFX_IN.exists():
        raise SystemExit("missing take, VO or SFX stem on the J1287 scratch disk")
    vo_path, vo = align_vo()
    take = read_wav(TAKE)
    vo_n = len(vo)
    end = vo_n - LOOP_N + XF_N + S0
    if end > len(take) or end < S0 + LOOP_N:
        raise SystemExit(f"take end {end} is outside the file ({len(take)})")
    print(f"film samples {vo_n} ({vo_n / SR:.6f} s), take tail used to {end / SR:.6f} s", flush=True)
    tail_db = rms_db(take[end:])
    print(f"unused take tail {len(take) - end} samples, {tail_db:.1f} dBFS", flush=True)
    if tail_db > -60:
        raise SystemExit("refusing to drop a take tail that is still audible")

    print("reading VO loudness", flush=True)
    vo_m, vo_i = sfx_kit.ebur128(vo_path)
    speaking, pauses = vo_mask(vo_m, vo_i)
    print(f"VO {vo_i:.2f} LUFS, long pauses {len(pauses)}", flush=True)
    b, shortlist = choose_seam(take, speaking, pauses, end)
    if b < 0:
        (PACK / "BED_SEAMS.json").write_text(json.dumps({"ok": False, "shortlist": shortlist}, indent=2) + "\n")
        print("NO SEAM", json.dumps(shortlist[:3], indent=2), flush=True)
        return 3

    print(f"building seam at take {b / SR:.3f} s", flush=True)
    raw = stitch(take, b, end)
    if len(raw) != vo_n:
        raise SystemExit(f"bed length {len(raw)} != vo {vo_n}")
    report = seam_report(raw, b, end)
    report["shortlist"] = shortlist
    report["unused_tail_dbfs"] = round(tail_db, 2)
    print("seam", {k: report[k] for k in report if k != "shortlist"}, flush=True)
    if not report["ok"]:
        # Try the next level-matched candidates before giving up.
        tried = [report]
        found = None
        for row in shortlist[1:6]:
            b2 = int(row["b_n"])
            raw2 = stitch(take, b2, end)
            rep2 = seam_report(raw2, b2, end)
            tried.append(rep2)
            print("try", row["b_s"], "ok" if rep2["ok"] else "no", flush=True)
            if rep2["ok"]:
                raw, report, b = raw2, rep2, b2
                found = rep2
                break
        if found is None:
            (PACK / "BED_SEAMS.json").write_text(json.dumps({"ok": False, "tried": tried, "shortlist": shortlist}, indent=2) + "\n")
            print("NO SEAM MET THE BAR", flush=True)
            return 3

    write_wav(NAS / "stem_bed_v02_arranged.wav", raw)
    ducked, duck_stats = duck_bed(raw, vo_m, vo_i, speaking)
    ok_duck = (
        duck_stats["speech_mean"] is not None
        and 16.0 <= duck_stats["speech_mean"] <= 21.5
        and duck_stats["breach_runs_0.3s"] == 0
        and duck_stats["pause_above_speech"] is not None
        and duck_stats["pause_above_speech"] >= 2.5
    )
    if not ok_duck:
        (PACK / "BED_SEAMS.json").write_text(json.dumps({"seam": report, "duck": duck_stats}, indent=2) + "\n")
        raise SystemExit(f"duck window missed: {duck_stats}")
    # The aired bed is the ducked one. Re-check the seam on it.
    aired = seam_report(ducked, b, end)
    aired["arranged"] = {k: report[k] for k in report if k != "shortlist"}
    (PACK / "BED_SEAMS.json").write_text(json.dumps(aired, indent=2) + "\n")
    if not aired["ok"]:
        print("ducked seam missed", aired, flush=True)
        return 3

    sfx = read_wav(SFX_IN)
    if len(sfx) < vo_n:
        sfx = np.pad(sfx, ((0, vo_n - len(sfx)), (0, 0)))
    sfx = sfx[:vo_n]
    before_sfx = sfx.copy()
    sfx, whoosh_notes = move_whooshes(sfx)
    # Every sample outside the two moved whooshes stays identical.
    cover = np.zeros(vo_n, dtype=bool)
    for note in whoosh_notes:
        for start in (note["old_start"], note["new_start"]):
            a = int(round(start * SR))
            cover[a : a + SR] = True
    if float(np.max(np.abs(sfx[~cover] - before_sfx[~cover]))) != 0.0:
        raise SystemExit("a cue other than the two whooshes changed")
    sfx_path = NAS / "stem_sfx_v02.wav"
    bed_path = NAS / "stem_bed_v02.wav"
    write_wav(sfx_path, sfx)
    write_wav(bed_path, ducked)

    level_json = PACK / "sfx_level.json"
    rc = sp.run(
        [sys.executable, str(OWB / "scripts/sfx_kit.py"), "level",
         "--vo", str(vo_path), "--sfx", str(sfx_path), "--bed", str(bed_path),
         "--minutes", f"{vo_n / SR / 60:.2f}", "--out", str(level_json)]
    ).returncode
    print(level_json.read_text(), flush=True)
    if rc:
        raise SystemExit(f"sfx level failed ({rc})")

    print("loudnorm measure", flush=True)
    st = loudnorm_measure(vo_path, bed_path, sfx_path)
    (PACK / "loudnorm_pass1.json").write_text(json.dumps(st, indent=2) + "\n")
    norm = (
        f"loudnorm=I=-14:TP=-1.5:LRA=11:measured_I={st['input_i']}:measured_TP={st['input_tp']}:"
        f"measured_LRA={st['input_lra']}:measured_thresh={st['input_thresh']}:offset={st['target_offset']}:linear=true"
    )
    fc = "[0:a][1:a][2:a]amix=inputs=3:normalize=0:duration=first,alimiter=limit=0.89:level=false:latency=true," + norm
    mix = NAS / "audio_master_v02.wav"
    sp.run(
        ["ffmpeg", "-y", "-v", "error", "-i", str(vo_path), "-i", str(bed_path), "-i", str(sfx_path),
         "-filter_complex", fc + "[a]", "-map", "[a]", "-ar", str(SR), "-c:a", "pcm_s16le", str(mix)],
        check=True,
    )
    lag = lag_ms(decode_at(vo_path, 30), decode_at(mix, 30))
    print(f"mix vs VO lag {lag:.2f} ms", flush=True)
    if abs(lag) > 1.0:
        # Positive lag: the mix is late, so trim the start and pad the end.
        shift = int(round(lag / 1000 * SR))
        audio = read_wav(mix)
        if shift > 0:
            audio = np.concatenate([audio[shift:], np.zeros((shift, 2), dtype=np.float32)])
        else:
            audio = np.concatenate([np.zeros((-shift, 2), dtype=np.float32), audio[:shift]])
        audio = audio[:vo_n]
        write_wav(mix, audio)
        lag2 = lag_ms(decode_at(vo_path, 30), decode_at(mix, 30))
        print(f"lag after trim {lag2:.2f} ms", flush=True)
        lag = lag2

    m4a = NAS / "audio_master_v02.m4a"
    sp.run(["ffmpeg", "-y", "-v", "error", "-i", str(mix), "-c:a", "aac", "-b:a", "256k", str(m4a)], check=True)
    master = PRE / "hos_008_master_v02.mp4"
    sp.run(
        ["ffmpeg", "-y", "-v", "error", "-i", str(V12), "-i", str(m4a),
         "-map", "0:v:0", "-map", "1:a:0", "-c:v", "copy", "-c:a", "copy",
         "-movflags", "+faststart", str(master)],
        check=True,
    )
    v12_md5 = stream_md5(V12)
    out_md5 = stream_md5(master)
    print(f"video md5 v12 {v12_md5} master {out_md5}", flush=True)
    if v12_md5 != out_md5:
        raise SystemExit("video stream changed")
    packets = sp.check_output(
        ["ffprobe", "-v", "error", "-select_streams", "v:0", "-count_packets",
         "-show_entries", "stream=nb_read_packets", "-of", "csv=p=0", str(master)],
        text=True,
    ).strip()
    print("video packets", packets, flush=True)
    lag_master = lag_ms(decode_at(V12, 30), decode_at(master, 30))
    print(f"master vs v12 lag {lag_master:.2f} ms", flush=True)
    loud = sp.run(
        ["ffmpeg", "-nostats", "-hide_banner", "-i", str(master), "-filter_complex", "ebur128=peak=true",
         "-f", "null", "-"],
        capture_output=True, text=True,
    )
    summary = "\n".join(loud.stderr.splitlines()[-12:])
    print(summary, flush=True)
    (PACK / "loudness_v02.txt").write_text(summary + "\n")

    bed_mp3 = FILM / "05_Music/lightning008_score_bed_v02.mp3"
    sp.run(
        ["ffmpeg", "-y", "-v", "error", "-i", str(NAS / "stem_bed_v02_arranged.wav"),
         "-c:a", "libmp3lame", "-b:a", "192k", str(bed_mp3)],
        check=True,
    )
    plan_src = json.loads((FILM / "05_Music/lightning008_score_bed_v01_plan.json").read_text())
    plan = {
        "created_at": "2026-10-31T00:30:00+00:00",
        "project": "lightning008",
        "script": None,
        "music_cues": [],
        "prompt": plan_src["prompt"],
        "length_ms": int(round(vo_n / SR * 1000)),
        "model_id": "arranged-from-take",
        "force_instrumental": True,
        "generate": False,
        "audio_file": bed_mp3.name,
        "status": "arranged from lightning008_score_bed_v01_take.mp3, no second ElevenLabs take",
        "source_take": "lightning008_score_bed_v01_take.mp3",
        "song_id": plan_src.get("song_id"),
        "note": "Same take as v01. Film starts at take 50.70 s. One 15-bar mid-body repeat, 3.0 s equal-power crossfade. No new generate.",
    }
    (FILM / "05_Music/lightning008_score_bed_v02_plan.json").write_text(json.dumps(plan, indent=2) + "\n")

    DESK.mkdir(parents=True, exist_ok=True)
    desk_mp4 = DESK / "hos_008_master_v02.mp4"
    shutil.copy2(master, desk_mp4)
    digest = sha256(master)
    if sha256(desk_mp4) != digest:
        raise SystemExit("NAS desk copy hash does not match")
    provenance = {
        "job": "J1287",
        "ruling": "Chief h29, bed seam only, no ElevenLabs",
        "take": "05_Music/lightning008_score_bed_v01_take.mp3",
        "song_id": plan_src.get("song_id"),
        "credits_new": 0,
        "take_start_s": TAKE_START,
        "loop_bars": 15,
        "loop_s": LOOP,
        "bpm_grid": 66.7,
        "xfade_s": XFADE,
        "source_in_s": round(b / SR, 3),
        "source_out_s": round((b + LOOP_N) / SR, 3),
        "take_end_used_s": round(end / SR, 3),
        "bed_arranged_sha256": sha256(NAS / "stem_bed_v02_arranged.wav"),
        "bed_ducked_sha256": sha256(bed_path),
        "bed_mp3_sha256": sha256(bed_mp3),
        "master_sha256": digest,
        "video_md5": out_md5,
        "video_packets": int(packets),
        "mix_vs_vo_lag_ms": round(lag, 3),
        "master_vs_v12_lag_ms": round(lag_master, 3),
        "duck": {k: duck_stats[k] for k in duck_stats if k != "before"},
        "whoosh": whoosh_notes,
        "paths": {"precheck": str(master), "nas_desk": str(desk_mp4)},
    }
    (PACK / "BED_PROVENANCE.json").write_text(json.dumps(provenance, indent=2) + "\n")
    print("MASTER", digest, flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
