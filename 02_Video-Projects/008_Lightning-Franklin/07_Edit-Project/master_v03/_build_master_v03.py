#!/usr/bin/env python3
"""HOS 008 master v03 (J1287, Chief h33). VO sync and chapter-3 whoosh only.

No ElevenLabs call. Picture is the locked rough v12 stream, copied.
The arranged bed is stem_bed_v02_arranged.wav unchanged (sha 142b7d41).
The VO is stem_vo_v12.wav from sample 0, cut to 25,902,071 samples.
Chapter 3's whoosh moves from 187.75 s to 187.65 s. Chapter 2 stays at 99.67 s.
"""
from __future__ import annotations

import hashlib
import importlib.util
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
LOCAL = Path("/private/tmp/j1287-v03")
DESK = Path("/Volumes/data/mac-mini-archive/YouTube/History Of Science/02_Video-Projects/008_Lightning-Franklin/07_Edit-Project/_desk/008/master_v03")
PACK = FILM / "07_Edit-Project/master_v03"
PRE = FILM / "07_Edit-Project/_precheck/master_v03"
ARRANGED = LOCAL / "stem_bed_v02_arranged.wav"
VO_SRC = LOCAL / "stem_vo_v12.wav"
SFX_V02 = LOCAL / "stem_sfx_v02.wav"
ARRANGED_SHA = "142b7d41bb5aaf3403ec0c09f73af875c40b3f3f9953bde3361d18cd91c17355"
VIDEO_MD5 = "1ab08ec6b7bb7dbb7b44d272710474dd"
SR = 48000
FILM_N = 25902071  # round(539.626479 * 48000)
# Same seam the v02 arranger wrote into the arranged wav.
S0 = int(round(50.70 * SR))
LOOP_N = int(round(54.0 * SR))
XF_N = int(round(3.0 * SR))
SEAM_B = int(round(370.45 * SR))
CH2_START = 99.67
CH3_OLD = 187.75
CH3_NEW = 187.65
WHOOSH_N = SR  # kit whoosh is 1.00 s
POINTS = (5.0, 100.0, 300.0, 500.0)


def load_v02():
    path = FILM / "07_Edit-Project/master_v02/_build_bed_v02.py"
    spec = importlib.util.spec_from_file_location("bedv02", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def sha256(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def read_wav(p: Path) -> np.ndarray:
    with wave.open(str(p)) as w:
        if w.getframerate() != SR or w.getnchannels() != 2:
            raise SystemExit(f"{p} is {w.getframerate()} Hz {w.getnchannels()} ch")
        n = w.getnframes()
        x = np.frombuffer(w.readframes(n), dtype="<i2").astype(np.float32)
    return x.reshape(n, 2) / 32768.0


def write_wav(p: Path, x: np.ndarray) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    pcm = np.clip(np.asarray(x, dtype=np.float32), -1, 1)
    with wave.open(str(p), "w") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes((pcm * 32767.0).astype("<i2").tobytes())


def frame_db(mono: np.ndarray, hop: int) -> np.ndarray:
    n = len(mono) // hop
    x = mono[: n * hop].reshape(n, hop)
    return 20 * np.log10(np.sqrt(np.mean(np.square(x), axis=1) + 1e-20))


def body_end_s(mono: np.ndarray, below_peak: float = 20.0) -> float:
    hop = SR // 100  # 10 ms
    db = frame_db(mono, hop)
    hot = np.where(db >= float(db.max()) - below_peak)[0]
    if len(hot) == 0:
        raise SystemExit("whoosh has no body")
    return (int(hot[-1]) + 1) * hop / SR


def first_onset(mono: np.ndarray, t0: float, t1: float) -> float | None:
    """First 10 ms window above -45 dBFS that follows one at or below -45."""
    hop = SR // 100
    db = frame_db(mono, hop)
    i0 = max(1, int(t0 * 100))
    i1 = min(len(db) - 1, int(t1 * 100))
    for i in range(i0, i1):
        if db[i] > -45.0 and db[i - 1] <= -45.0:
            return i * 0.01
    return None


def duck_v03(bed, raw, vo_m, vo_i, speaking):
    tmp = LOCAL / "stem_bed_v03_preduck.wav"
    write_wav(tmp, raw)
    bed_m, _bed_i = sfx_kit.ebur128(tmp)
    vm = np.array(vo_m, dtype=np.float64)
    bm = np.array(bed_m[: len(vm)], dtype=np.float64)
    n = min(len(vm), len(bm), len(speaking))
    vm, bm, sp = vm[:n], bm[:n], speaking[:n]
    before = bed.speech_stats(vm, bm, vo_i, sp)
    print("duck before", before, flush=True)
    audible = sp & (bm > sfx_kit.SILENT)
    current = float((vm[audible] - bm[audible]).mean())
    global_db = current - 18.5
    gain = np.full(n, global_db, dtype=np.float64)
    bm2 = bm + global_db
    d = vm - bm2
    extra = np.where(sp & (d < 16.5), np.clip(18.5 - d, 0, 8), 0.0)
    gain -= extra
    bm3 = bm + gain
    for s, ln in bed.runs_of(~sp):
        if ln < 8:
            continue
        a, b0 = s + 2, s + ln - 2
        if b0 <= a:
            a, b0 = s, s + ln
        want = np.clip((vo_i - 13.0) - bm3[a:b0], 0, 12)
        gain[a:b0] = np.maximum(gain[a:b0], global_db + want)
    print(f"duck gain min {gain.min():.2f} max {gain.max():.2f}", flush=True)
    out = bed.apply_frame_db(raw[: int(n * 0.1 * SR) + SR], gain)
    if len(out) < len(raw):
        out = np.concatenate([out, np.zeros((len(raw) - len(out), 2), dtype=np.float32)])
    out = out[: len(raw)]
    ducked_path = LOCAL / "stem_bed_v03.wav"
    write_wav(ducked_path, out)
    bed_m2, bed_i = sfx_kit.ebur128(ducked_path)
    bm = np.array(bed_m2[:n], dtype=np.float64)
    after = bed.speech_stats(vm, bm, vo_i, sp)
    after["bed_integrated"] = round(float(bed_i), 2)
    after["vo_integrated"] = round(float(vo_i), 2)
    after["before"] = before
    print("duck after", {k: after[k] for k in after if k != "before"}, flush=True)
    return out, after, ducked_path


def move_ch3(sfx: np.ndarray) -> tuple[np.ndarray, dict]:
    old = int(round(CH3_OLD * SR))
    new = int(round(CH3_NEW * SR))
    if new < 0 or old + WHOOSH_N > len(sfx) or new + WHOOSH_N > len(sfx):
        raise SystemExit("chapter 3 whoosh would leave the stem")
    dest = sfx[new:old]
    if float(np.max(np.abs(dest))) > 0.002:
        raise SystemExit(f"chapter 3 destination is not silent ({np.max(np.abs(dest)):.4f})")
    out = sfx.copy()
    seg = out[old : old + WHOOSH_N].copy()
    out[old : old + WHOOSH_N] = 0
    out[new : new + WHOOSH_N] = seg
    body = body_end_s(seg.mean(axis=1), 20.0)
    note = {
        "name": "ch3",
        "old_start": CH3_OLD,
        "new_start": round(new / SR, 3),
        "body_s": round(body, 3),
        "body_end": round(new / SR + body, 3),
    }
    cover = np.zeros(len(sfx), dtype=bool)
    cover[new : old + WHOOSH_N] = True
    if float(np.max(np.abs(out[~cover] - sfx[~cover]))) != 0.0:
        raise SystemExit("a sample outside the chapter 3 whoosh changed")
    ch2 = int(round(CH2_START * SR))
    if float(np.max(np.abs(out[ch2 : ch2 + WHOOSH_N] - sfx[ch2 : ch2 + WHOOSH_N]))) != 0.0:
        raise SystemExit("chapter 2 whoosh changed")
    print(f"ch3 whoosh {CH3_OLD:.2f} -> {new / SR:.3f}, 20 dB body ends {note['body_end']:.3f}", flush=True)
    return out, note


def wav_data_f32(wav: Path) -> bytes:
    """Read a little-endian 32-bit float mono wav, including format-3 files the wave module rejects."""
    data = wav.read_bytes()
    if data[:4] != b"RIFF" or data[8:12] != b"WAVE":
        raise SystemExit(f"{wav} is not a wav")
    i = 12
    audio_format = channels = rate = bits = None
    audio = None
    while i + 8 <= len(data):
        chunk = data[i : i + 4]
        size = int.from_bytes(data[i + 4 : i + 8], "little")
        body = data[i + 8 : i + 8 + size]
        if chunk == b"fmt " and len(body) >= 16:
            audio_format, channels, rate = int.from_bytes(body[0:2], "little"), int.from_bytes(body[2:4], "little"), int.from_bytes(body[4:8], "little")
            bits = int.from_bytes(body[14:16], "little")
        elif chunk == b"data":
            audio = body
            break
        i += 8 + size + (size & 1)
    if audio is None or audio_format not in (3, 0xFFFE) or channels != 1 or rate != SR or bits != 32:
        raise SystemExit(f"afconvert wav is format {audio_format} {channels} ch {rate} Hz {bits} bit")
    return audio


def decode_raw(src: Path, dest: Path, tool: str) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    if tool == "ffmpeg":
        sp.run(
            ["ffmpeg", "-y", "-v", "error", "-i", str(src), "-vn", "-ac", "1", "-ar", str(SR),
             "-c:a", "pcm_f32le", "-f", "f32le", str(dest)],
            check=True,
        )
        return
    m4a = dest.with_suffix(".m4a")
    wav = dest.with_suffix(".wav")
    sp.run(["ffmpeg", "-y", "-v", "error", "-i", str(src), "-vn", "-c:a", "copy", str(m4a)], check=True)
    sp.run(["afconvert", "-f", "WAVE", "-d", "LEF32@48000", "-c", "1", str(m4a), str(wav)], check=True)
    dest.write_bytes(wav_data_f32(wav))


def lag_ms(ref: np.ndarray, mix: np.ndarray, t: float, win: float = 2.0, search: float = 0.04) -> float:
    i0 = int(round(t * SR))
    n = int(win * SR)
    s = int(search * SR)
    if i0 < s or i0 + n + s > min(len(ref), len(mix)):
        raise SystemExit(f"lag window {t} s does not fit the decode")
    a = ref[i0 : i0 + n].astype(np.float64)
    b = mix[i0 - s : i0 + n + s].astype(np.float64)
    a -= a.mean()
    b -= b.mean()
    corr = np.correlate(b, a, mode="valid")
    k = int(np.argmax(corr))
    if k == 0 or k == len(corr) - 1:
        raise SystemExit(f"lag at {t} s sat on the search edge; the offset is larger than {search * 1000:.0f} ms")
    return (k - s) / SR * 1000.0


def load_f32(path: Path) -> np.ndarray:
    return np.fromfile(path, dtype="<f4")


def lag_table(ref_path: Path, mix_path: Path, tool: str) -> list[dict]:
    ref = load_f32(ref_path)
    mix = load_f32(mix_path)
    rows = []
    for t in POINTS:
        ms = lag_ms(ref, mix, t)
        rows.append({"tool": tool, "t": t, "lag_ms": round(ms, 3)})
        print(f"lag {tool} {t:.0f}s {ms:.3f} ms", flush=True)
    return rows


def stream_md5(path: Path) -> str:
    r = sp.run(
        ["ffmpeg", "-v", "error", "-i", str(path), "-map", "0:v:0", "-c", "copy", "-f", "md5", "-"],
        capture_output=True, text=True,
    )
    if r.returncode:
        raise SystemExit(r.stderr[-500:])
    return r.stdout.strip().split("=")[-1]


def probe(path: Path) -> dict:
    raw = sp.check_output(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-show_entries", "stream=codec_type,start_time,duration,nb_frames", "-of", "json", str(path)],
        text=True,
    )
    return json.loads(raw)


def ebur128_summary(path: Path) -> dict:
    r = sp.run(
        ["ffmpeg", "-nostats", "-hide_banner", "-i", str(path), "-filter_complex", "ebur128=peak=true",
         "-f", "null", "-"],
        capture_output=True, text=True,
    )
    if r.returncode:
        raise SystemExit(r.stderr[-800:])
    text = r.stderr
    summary = text.split("Summary:")[-1]
    i = float(re.search(r"I:\s+([-\d.]+) LUFS", summary).group(1))
    tp = float(re.search(r"Peak:\s+([-\d.]+) dBFS", summary).group(1))
    lra = float(re.search(r"LRA:\s+([-\d.]+) LU", summary).group(1))
    if i < -40:
        raise SystemExit(f"loudness parse looks wrong: I {i}\n{summary[-500:]}")
    return {"I": i, "TP": tp, "LRA": lra, "text": "\n".join(summary.strip().splitlines()[:16])}


def render_mix(vo: Path, bed_path: Path, sfx: Path, gain_db: float, out: Path, limit_db: float) -> None:
    limit = 10 ** (limit_db / 20)
    fc = (
        "[0:a][1:a][2:a]amix=inputs=3:normalize=0:duration=first,"
        f"volume={gain_db:.4f}dB,"
        f"alimiter=limit={limit:.6f}:attack=0.1:level=false:latency=true"
    )
    sp.run(
        ["ffmpeg", "-y", "-v", "error", "-i", str(vo), "-i", str(bed_path), "-i", str(sfx),
         "-filter_complex", fc + "[a]", "-map", "[a]", "-ar", str(SR), "-c:a", "pcm_s16le", str(out)],
        check=True,
    )


def stage_sources() -> None:
    """Copy the locked stems onto the local disk. The NAS is busy and small reads stall."""
    LOCAL.mkdir(parents=True, exist_ok=True)
    mapping = {
        "stem_bed_v02_arranged.wav": ARRANGED_SHA,
        "stem_vo_v12.wav": None,
        "stem_sfx_v02.wav": None,
    }
    for name, expect in mapping.items():
        dest = LOCAL / name
        src = NAS / name
        if not dest.exists() or dest.stat().st_size != src.stat().st_size:
            print(f"copy {name}", flush=True)
            sp.run(["cp", "-c", str(src), str(dest)], check=False)
            if not dest.exists() or dest.stat().st_size != src.stat().st_size:
                sp.run(["cp", str(src), str(dest)], check=True)
        digest = sha256(dest)
        if expect and digest != expect:
            raise SystemExit(f"{name} sha {digest} != {expect}")
        print(f"staged {name} {digest[:12]}", flush=True)


def main() -> int:
    PACK.mkdir(parents=True, exist_ok=True)
    PRE.mkdir(parents=True, exist_ok=True)
    stage_sources()
    if sha256(ARRANGED) != ARRANGED_SHA:
        raise SystemExit("arranged bed sha changed; refusing to mix")
    v02 = load_v02()
    v02.NAS = LOCAL
    vo_full = read_wav(VO_SRC)
    if len(vo_full) < FILM_N:
        raise SystemExit(f"VO wav is {len(vo_full)} samples, need {FILM_N}")
    vo = vo_full[:FILM_N]
    vo_path = LOCAL / "stem_vo_v03_unshifted.wav"
    write_wav(vo_path, vo)
    print(f"unshifted VO {FILM_N} samples ({FILM_N / SR:.6f} s), dropped tail {len(vo_full) - FILM_N}", flush=True)

    print("VO vs v12, ffmpeg full-file, before the mix", flush=True)
    v12_ff = LOCAL / "decode_v12_ffmpeg.f32"
    vo_ff = LOCAL / "decode_vo_v03_ffmpeg.f32"
    decode_raw(V12, v12_ff, "ffmpeg")
    decode_raw(vo_path, vo_ff, "ffmpeg")
    pre = lag_table(v12_ff, vo_ff, "vo-ffmpeg")
    if any(abs(row["lag_ms"]) > 1.0 for row in pre):
        (PACK / "LAG_PRECHECK.json").write_text(json.dumps(pre, indent=2) + "\n")
        raise SystemExit(f"unshifted VO is not within 1 ms of v12: {pre}")

    arranged = read_wav(ARRANGED)
    if len(arranged) != FILM_N:
        raise SystemExit(f"arranged bed is {len(arranged)} samples, film is {FILM_N}")
    if sha256(ARRANGED) != ARRANGED_SHA:
        raise SystemExit("arranged bed changed while reading")
    print("reading VO loudness", flush=True)
    vo_m, vo_i = sfx_kit.ebur128(vo_path)
    speaking, _pauses = v02.vo_mask(vo_m, vo_i)
    ducked, duck_stats, bed_path = duck_v03(v02, arranged, vo_m, vo_i, speaking)
    ok_duck = (
        duck_stats["speech_mean"] is not None
        and 16.0 <= duck_stats["speech_mean"] <= 21.5
        and duck_stats["breach_runs_0.3s"] == 0
        and duck_stats["pause_above_speech"] is not None
        and duck_stats["pause_above_speech"] >= 2.5
    )
    if not ok_duck:
        raise SystemExit(f"duck window missed: {duck_stats}")
    end = FILM_N - LOOP_N + XF_N + S0
    aired = v02.seam_report(ducked, SEAM_B, end)
    (PACK / "BED_SEAMS.json").write_text(json.dumps(aired, indent=2) + "\n")
    print("ducked seam", {k: aired[k] for k in aired if k != "shortlist"}, flush=True)
    if not aired["ok"]:
        raise SystemExit("ducked seam missed the bar")

    sfx_in = read_wav(SFX_V02)
    if len(sfx_in) != FILM_N:
        raise SystemExit(f"sfx v02 is {len(sfx_in)} samples")
    sfx, ch3 = move_ch3(sfx_in)
    vo_mono = vo.mean(axis=1)
    ch2_seg = sfx[int(round(CH2_START * SR)) : int(round(CH2_START * SR)) + WHOOSH_N].mean(axis=1)
    ch2_body_end = CH2_START + body_end_s(ch2_seg, 20.0)
    ch2_onset = first_onset(vo_mono, 100.2, 101.2)
    ch3_onset = first_onset(vo_mono, 188.2, 189.2)
    ch3["onset"] = ch3_onset
    ch3["clear_s"] = None if ch3_onset is None else round(ch3_onset - ch3["body_end"], 3)
    ch2_note = {
        "name": "ch2",
        "start": CH2_START,
        "body_end": round(ch2_body_end, 3),
        "onset": ch2_onset,
        "clear_s": None if ch2_onset is None else round(ch2_onset - ch2_body_end, 3),
    }
    print("whoosh clearance", ch2_note, ch3, flush=True)
    if ch3["clear_s"] is None or ch3["clear_s"] < 0.15:
        raise SystemExit(f"chapter 3 clearance {ch3['clear_s']} is under 0.15 s")
    sfx_path = LOCAL / "stem_sfx_v03.wav"
    write_wav(sfx_path, sfx)

    level_json = PACK / "sfx_level.json"
    rc = sp.run(
        [sys.executable, str(OWB / "scripts/sfx_kit.py"), "level",
         "--vo", str(vo_path), "--sfx", str(sfx_path), "--bed", str(bed_path),
         "--minutes", f"{FILM_N / SR / 60:.2f}", "--out", str(level_json)]
    ).returncode
    print(level_json.read_text(), flush=True)
    if rc:
        raise SystemExit(f"sfx level failed ({rc})")

    dry = LOCAL / "audio_master_v03_dry.wav"
    render_mix(vo_path, bed_path, sfx_path, 0.0, dry, -1.5)
    dry_stats = ebur128_summary(dry)
    gain_db = -14.0 - dry_stats["I"]
    limit_db = -1.5
    print(f"dry I {dry_stats['I']:.3f} TP {dry_stats['TP']:.3f}, first gain {gain_db:.3f} dB", flush=True)
    mix = LOCAL / "audio_master_v03.wav"
    stats = None
    for attempt in range(5):
        render_mix(vo_path, bed_path, sfx_path, gain_db, mix, limit_db)
        stats = ebur128_summary(mix)
        print(f"mix attempt {attempt} gain {gain_db:.3f} limit {limit_db:.2f} I {stats['I']:.3f} TP {stats['TP']:.3f}", flush=True)
        if -14.3 <= stats["I"] <= -13.7 and stats["TP"] <= -1.0:
            break
        if stats["TP"] > -1.0:
            limit_db -= 0.3
        gain_db += -14.0 - stats["I"]
    else:
        raise SystemExit(f"mix missed -14.0±0.3 / -1.0 dBTP: {stats}")
    if not (-14.3 <= stats["I"] <= -13.7 and stats["TP"] <= -1.0):
        raise SystemExit(f"mix missed the loudness bar: {stats}")

    m4a = LOCAL / "audio_master_v03.m4a"
    sp.run(["ffmpeg", "-y", "-v", "error", "-i", str(mix), "-c:a", "aac", "-b:a", "256k", str(m4a)], check=True)
    master = PRE / "hos_008_master_v03.mp4"
    sp.run(
        ["ffmpeg", "-y", "-v", "error", "-i", str(V12), "-i", str(m4a),
         "-map", "0:v:0", "-map", "1:a:0", "-c:v", "copy", "-c:a", "copy",
         "-movflags", "+faststart", str(master)],
        check=True,
    )
    out_md5 = stream_md5(master)
    v12_md5 = stream_md5(V12)
    print(f"video md5 v12 {v12_md5} master {out_md5}", flush=True)
    if out_md5 != VIDEO_MD5 or v12_md5 != VIDEO_MD5:
        raise SystemExit("video stream changed")
    packets = sp.check_output(
        ["ffprobe", "-v", "error", "-select_streams", "v:0", "-count_packets",
         "-show_entries", "stream=nb_read_packets", "-of", "csv=p=0", str(master)],
        text=True,
    ).strip()
    if packets != "12923":
        raise SystemExit(f"video packets {packets}")

    master_ff = LOCAL / "decode_v03_ffmpeg.f32"
    decode_raw(master, master_ff, "ffmpeg")
    rows = lag_table(v12_ff, master_ff, "ffmpeg")
    v12_af = LOCAL / "decode_v12_afconvert.f32"
    master_af = LOCAL / "decode_v03_afconvert.f32"
    decode_raw(V12, v12_af, "afconvert")
    decode_raw(master, master_af, "afconvert")
    rows += lag_table(v12_af, master_af, "afconvert")
    if any(abs(row["lag_ms"]) > 1.0 for row in rows):
        (PACK / "LAG_TABLE.json").write_text(json.dumps(rows, indent=2) + "\n")
        raise SystemExit(f"master VO lag is outside ±1 ms: {rows}")

    loud = ebur128_summary(master)
    (PACK / "loudness_v03.txt").write_text(loud["text"] + "\n")
    print(loud["text"], flush=True)
    if not (-14.3 <= loud["I"] <= -13.7 and loud["TP"] <= -1.0):
        raise SystemExit(f"master loudness missed the bar: {loud}")

    info = probe(master)
    vinfo = probe(V12)
    DESK.mkdir(parents=True, exist_ok=True)
    desk_mp4 = DESK / "hos_008_master_v03.mp4"
    shutil.copy2(master, desk_mp4)
    digest = sha256(master)
    if sha256(desk_mp4) != digest:
        raise SystemExit("NAS desk copy hash does not match")
    if sha256(ARRANGED) != ARRANGED_SHA:
        raise SystemExit("arranged bed sha changed during the mix")

    report = {
        "job": "J1287",
        "ruling": "Chief h33, VO sync and chapter-3 whoosh only, no ElevenLabs",
        "credits_new": 0,
        "normalization_type": "linear",
        "chain": "amix normalize=0, volume static gain, alimiter attack=0.1 latency=true (compensated). No loudnorm.",
        "gain_db": round(gain_db, 4),
        "limiter_db": round(limit_db, 2),
        "wav_I": round(stats["I"], 3),
        "wav_TP": round(stats["TP"], 3),
        "master_I": round(loud["I"], 3),
        "master_TP": round(loud["TP"], 3),
        "master_LRA": round(loud["LRA"], 3),
        "bed_arranged_sha256": ARRANGED_SHA,
        "bed_ducked_sha256": sha256(bed_path),
        "master_sha256": digest,
        "video_md5": out_md5,
        "video_packets": int(packets),
        "film_samples": FILM_N,
        "vo_trim_samples": 0,
        "lag_precheck": pre,
        "lag": rows,
        "duck": {k: duck_stats[k] for k in duck_stats if k != "before"},
        "seam": {k: aired[k] for k in aired if k != "shortlist"},
        "whoosh": [ch2_note, ch3],
        "probe_master": info,
        "probe_v12": vinfo,
        "paths": {"precheck": str(master), "nas_desk": str(desk_mp4)},
    }
    (PACK / "MEASURE_v03.json").write_text(json.dumps(report, indent=2) + "\n")
    print("MASTER", digest, flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
