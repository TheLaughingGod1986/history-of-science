#!/usr/bin/env python3
"""HOS 001 Short s11 v06 (J0939, £0 local re-cut of 1-BZaFIMwYU).

Audio and captions only. v05's picture plan, plates, in-points, bed, hook,
Pasteur card, promo title and sentence order stay. v06 plays each of the 11
pieces as one unbroken source run (v05's cuts and ends), puts the sentence
gaps back to 0.12-0.18 s, and restores every spoken word on screen.
No new TTS, Veo, Flow or Vertex.

    python3 _build_short_s11_curved_flask_v06.py
    python3 _build_short_s11_curved_flask_v06.py --vo-only
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

VENV_PY = Path("/Users/benjaminoats/YouTube/History Of Science/"
               "02_Video-Projects/001_How-Did-We-Discover-Germs/10_Shorts/_venv/bin/python")
if VENV_PY.exists() and Path(sys.executable) != VENV_PY:
    os.execv(str(VENV_PY), [str(VENV_PY), str(Path(__file__).resolve()), *sys.argv[1:]])

import argparse  # noqa: E402
import array  # noqa: E402
import hashlib  # noqa: E402
import json  # noqa: E402
import math  # noqa: E402
import re  # noqa: E402
import shutil  # noqa: E402
import struct  # noqa: E402
import subprocess  # noqa: E402
import wave  # noqa: E402

from PIL import Image, ImageDraw, ImageFont, ImageFilter  # noqa: E402

HERE = Path(__file__).resolve().parent
PROJ = HERE.parent
REPO = PROJ.parents[1]
NAS_PROJ = Path("/Volumes/data/mac-mini-archive/YouTube/History Of Science/"
                "02_Video-Projects/001_How-Did-We-Discover-Germs")
OWB = Path("/Users/benjaminoats/YouTube/orbit-with-ben")
SID, VER, JOB = "s11_curved_flask", "v06", "J0939"
AIR = "2026-10-27"
YT_ID = "1-BZaFIMwYU"
WORK = Path("/private/tmp/j0939-flask-v06")
QA = HERE / f"qa_{SID}_{VER}"
W, H, FPS = 1080, 1920, 30
LOOP_S = 1.0
XFADE = 0.025
# 30 ms is past the 20 ms onset rule and lets the 25 ms fade finish before speech.
LEAD = 0.030
TAIL = 0.030
DB60 = -60.0
HOOK = "FLASK **STAYS**"
CARD = ("LOUIS PASTEUR", "Swan-neck flask, 1860s")
CARD_IN, CARD_OUT, CARD_FADE = 2.20, 5.90, 0.35
TITLE = "How Did We Discover Germs?"
TITLE_IN, TITLE_OUT = 9.0, 14.0
FONT = "/System/Library/Fonts/Supplemental/Didot.ttc"
CTA_FONT = "/System/Library/Fonts/Supplemental/Times New Roman.ttf"
CREAM, INK, YEL = (245, 232, 210, 255), (28, 26, 28, 255), (255, 214, 70, 255)
BAND_TOP, BAND_H = (H - 608) // 2, 608
# In 1.80 s, crop x=720: the centre band of this plate moves enough to clear the
# stayed gate (crop 640 at 1.60 s measured 1.48, under the 1.50 floor). Black ~19%.
FLASK_IN = 1.80
FLASK_CROP = 720
# v05's measured cut and end, played as one unbroken run. The third field is the
# heard gap after the piece (sentence 0.17 inside 0.12-0.18; joins 0.18, <=0.20).
PIECES = [
    (4.12, 4.75, 0.19, "word", ["a", "flask"]),
    (16.22, 17.15, 0.17, "sentence", ["stays", "clear"]),
    (7.32, 8.13, 0.17, "sentence", ["boil", "broth"]),
    (11.06, 12.02, 0.19, "comma", ["air", "can", "drift"]),
    (12.45, 15.12, 0.17, "sentence", ["but", "dust", "and", "microbes", "settle", "in", "the", "curve"]),
    (38.01, 40.98, 0.19, "comma", ["if", "life", "arrives", "as", "passengers", "from", "the", "outside"]),
    (41.39, 43.54, 0.17, "sentence", ["then", "disease", "can", "be", "a", "passenger", "too"]),
    (17.89, 18.62, 0.19, "comma", ["break", "the", "neck"]),
    (19.04, 20.01, 0.19, "comma", ["or", "tip", "the", "trap"]),
    (20.48, 22.70, 0.15, "sentence", ["and", "life", "blooms", "into", "cloudiness"]),
    (8.83, 10.36, 0.0, "end", ["keep", "the", "swan", "neck", "intact"]),
]
PLATE = "04_Generated-Clips/part04/raw/v01_fast_probe"


def resolve_media(rel: str) -> Path:
    local = PROJ / rel
    if local.exists() and local.stat().st_size > 1000:
        return local
    alt = NAS_PROJ / rel
    if alt.exists():
        return alt
    return local


RAW_VO = resolve_media("02_Voiceover/part04_proof_in_a_flask_v01.wav")
ALIGN = resolve_media("02_Voiceover/part04_proof_in_a_flask_v01_align.json")


def ff(*a: str, cwd: Path | None = None) -> None:
    subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", *a], check=True, cwd=cwd)


def probe(p: Path) -> float:
    return float(subprocess.check_output(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)], text=True))


def sha256(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def mean_db(p: Path) -> float:
    err = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(p), "-af", "volumedetect", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    return float(re.search(r"mean_volume: (-?[\d.]+)", err).group(1))


def _ebu_summary(p: Path) -> str:
    err = subprocess.run(["ffmpeg", "-nostats", "-hide_banner", "-i", str(p), "-af", "ebur128=peak=true", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    return err.split("Summary:")[-1]


def integrated_lufs(p: Path) -> float:
    m = re.search(r"I:\s+(-?[\d.]+) LUFS", _ebu_summary(p))
    if not m:
        raise SystemExit(f"no LUFS for {p.name}")
    return float(m.group(1))


def true_peak(p: Path) -> float:
    m = re.search(r"Peak:\s+(-?[\d.]+) dBFS", _ebu_summary(p))
    return float(m.group(1)) if m else 0.0


def words_in_align() -> list[tuple[str, float, float]]:
    d = json.loads(ALIGN.read_text())
    words, cur, t0, t1 = [], "", 0.0, 0.0
    for ch, a, b in zip(d["characters"], d["character_start_times_seconds"], d["character_end_times_seconds"]):
        if ch.isspace():
            if cur:
                words.append((cur, t0, t1))
            cur = ""
        else:
            if not cur:
                t0 = a
            cur += ch
            if ch not in ".,;:?!”\"'":
                t1 = b
    if cur:
        words.append((cur, t0, t1))
    return [(w, a, b) for w, a, b in words if w.strip("—–-.,")]


def load_wav(path: Path) -> tuple[array.array, array.array, int]:
    """Stereo int16 plus a mono float envelope at 10 ms, and the sample rate."""
    import array as _array
    w = wave.open(str(path))
    sr, nch = w.getframerate(), w.getnchannels()
    if w.getsampwidth() != 2:
        raise SystemExit(f"{path.name} is not 16-bit")
    stereo = _array.array("h")
    stereo.frombytes(w.readframes(w.getnframes()))
    if nch == 1:
        stereo = _array.array("h", (s for s in stereo for _ in range(2)))
    hop = sr // 100
    env = _array.array("d")
    frames = len(stereo) // 2
    for i in range(0, frames - hop, hop):
        acc = 0.0
        base = i * 2
        for j in range(hop):
            v = (stereo[base + j * 2] + stereo[base + j * 2 + 1]) / 65536.0
            acc += v * v
        env.append(math.sqrt(acc / hop))
    return stereo, env, sr


STEREO, ENV, SR = load_wav(RAW_VO)


def slice_stereo(a: float, b: float) -> array.array:
    i0 = max(0, int(a * SR))
    i1 = min(len(STEREO) // 2, int(b * SR))
    return array.array("h", STEREO[i0 * 2:i1 * 2])


def apply_gain(samples: array.array, db: float) -> array.array:
    g = 10 ** (db / 20.0)
    out = array.array("h")
    for s in samples:
        out.append(max(-32767, min(32767, int(s * g))))
    return out


def xfade(a: array.array, b: array.array, nframes: int) -> array.array:
    ns = nframes * 2
    if nframes <= 0 or len(a) < ns or len(b) < ns:
        out = array.array("h", a)
        out.extend(b)
        return out
    out = array.array("h", a[:-ns])
    for i in range(nframes):
        g = i / nframes
        for c in range(2):
            v = int(a[-ns + i * 2 + c] * (1 - g) + b[i * 2 + c] * g)
            out.append(max(-32767, min(32767, v)))
    out.extend(b[ns:])
    return out


def speech_rms_db(samples: array.array, thr: float = 0.012) -> float:
    hop = SR // 100
    frames = len(samples) // 2
    acc = n = 0.0
    for i in range(0, frames - hop, hop):
        e = 0.0
        base = i * 2
        for j in range(hop):
            v = (samples[base + j * 2] + samples[base + j * 2 + 1]) / 65536.0
            e += v * v
        r = math.sqrt(e / hop)
        if r >= thr:
            acc += r * r
            n += 1
    if n < 1:
        return -60.0
    return 20 * math.log10(math.sqrt(acc / n))


def room_tone(nframes: int) -> array.array:
    """A quiet slice of the take (between 'mark.' and 'Boil'), tiled. Not digital zero."""
    i0, i1 = int(6.50 * SR), int(6.90 * SR)
    room = array.array("h", STEREO[i0 * 2:i1 * 2])
    if len(room) < 4:
        raise SystemExit("no room tone")
    out = array.array("h")
    need = nframes * 2
    while len(out) < need:
        out.extend(room)
    return array.array("h", out[:need])


def env_at(t: float) -> float:
    i = int(t * 100)
    if i < 0 or i >= len(ENV):
        return 0.0
    return ENV[i]


def measure_bounds(a: float, b: float) -> tuple[float, float]:
    """First and last 10 ms bin inside [a, b] that is speech."""
    i0, i1 = int(a * 100), min(len(ENV) - 1, int(b * 100))
    onset = offset = None
    for i in range(max(0, i0), max(0, i1) + 1):
        if ENV[i] >= 0.012:
            onset = i / 100.0
            break
    for i in range(max(0, i1), max(0, i0) - 1, -1):
        if ENV[i] >= 0.012:
            offset = (i + 1) / 100.0
            break
    if onset is None:
        onset = a
    if offset is None or offset <= onset:
        offset = b
    return onset, offset


def rms_db(t: float) -> float:
    """10 ms RMS in dBFS, left channel, full scale 32768."""
    i0 = int(t * SR)
    hop = SR // 100
    i1 = i0 + hop
    if i0 < 0 or i1 * 2 > len(STEREO) or hop < 1:
        return -99.0
    acc = 0.0
    for i in range(i0, i1):
        v = STEREO[i * 2] / 32768.0
        acc += v * v
    rms = math.sqrt(acc / hop)
    return -99.0 if rms <= 1e-9 else 20 * math.log10(rms)


def attack_in(a: float, b: float) -> tuple[float | None, float | None]:
    """First and last 10 ms frame inside [a, b) above -60 dBFS."""
    onset = offset = None
    t = round(a, 3)
    end = round(b, 3)
    while t < end - 0.009:
        if rms_db(t) > DB60:
            if onset is None:
                onset = t
            offset = round(t + 0.01, 3)
        t = round(t + 0.01, 3)
    return onset, offset


def release_end(a: float, b: float) -> float | None:
    """End of the last -60 dB frame that still belongs to the word.

    A frame above -60 counts for 80 ms after a frame louder than -42 dB.
    The take's -50 dB noise floor is not the word, and counting it as the
    offset pushes the heard gap past 0.20 s.
    """
    last_loud = None
    last = None
    t = round(max(0.0, a), 3)
    end = round(b, 3)
    while t < end - 0.009:
        db = rms_db(t)
        if db > -42:
            last_loud = t
            last = round(t + 0.01, 3)
        elif db > DB60 and last_loud is not None and (t - last_loud) <= 0.08:
            last = round(t + 0.01, 3)
        t = round(t + 0.01, 3)
    return last


def quiet_edge(pa: float, pb: float, from_end: bool) -> float:
    """How many seconds at this edge sit at or under -38 dBFS (the gap meter's floor)."""
    t = round(pb - 0.01, 3) if from_end else round(pa, 3)
    n = 0.0
    while (t > pa + 0.005) if from_end else (t < pb - 0.005):
        if rms_db(t) > -38:
            break
        n += 0.01
        t = round(t + (-0.01 if from_end else 0.01), 3)
    return round(n, 3)


def write_wav(path: Path, samples: array.array) -> None:
    with wave.open(str(path), "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(samples.tobytes())


def max_gaps(samples: array.array) -> list[dict]:
    hop = SR // 100
    frames = len(samples) // 2
    gaps = []
    run = 0
    start = 0
    for i in range(0, frames - hop, hop):
        e = 0.0
        base = i * 2
        for j in range(0, hop * 2, 2):
            v = samples[base + j] / 32768.0
            e += v * v
        r = math.sqrt(e / max(1, hop))
        if r < 0.012:
            if run == 0:
                start = i
            run += hop
        else:
            if run / SR > 0.08:
                gaps.append({"t": round(start / SR, 3), "dur": round(run / SR, 3)})
            run = 0
    if run / SR > 0.08:
        gaps.append({"t": round(start / SR, 3), "dur": round(run / SR, 3)})
    return gaps


def tighten_span(a: float, b: float, max_silence: float = 0.15) -> list[tuple[float, float]]:
    """Subspans of [a, b] with leading, trailing and internal silence over max_silence removed."""
    onset, offset = measure_bounds(a, b)
    i = int(onset * 100)
    end = min(len(ENV) - 1, int(offset * 100))
    limit = int(max_silence * 100)
    spans = []
    while i <= end:
        while i <= end and ENV[i] < 0.012:
            i += 1
        if i > end:
            break
        j = i
        sil = 0
        closed = False
        while j <= end:
            if ENV[j] < 0.010:
                sil += 1
                if sil >= limit:
                    cut = j - sil
                    if cut > i + 1:
                        spans.append((round(i / 100.0, 3), round((cut + 1) / 100.0, 3)))
                    i = j
                    closed = True
                    break
            else:
                sil = 0
            j += 1
        if not closed:
            spans.append((round(i / 100.0, 3), round(offset, 3)))
            break
    return spans or [(round(onset, 3), round(offset, 3))]


def map_src(subs: list[tuple], t: float) -> float:
    """Map a source time onto the stem. Times inside a cut silence clamp to the next subspan."""
    for src_a, src_b, out_t, _gain in subs:
        if src_a - 0.02 <= t <= src_b + 0.02:
            return out_t + min(max(t, src_a), src_b) - src_a
    later = [s for s in subs if s[0] >= t]
    if later:
        return later[0][2]
    return subs[-1][2] + (subs[-1][1] - subs[-1][0])


def lifted_vo(work: Path) -> tuple[Path, list[tuple[str, float, float]], list[dict], dict]:
    """Each piece is one unbroken source run. Room tone sits only between pieces.

    Sentence gaps land at 0.15 s (band 0.12-0.18). Joins land at 0.10 s and
    stay at or under 0.20 s. Word times are the speech energy on the stem.
    """
    src_words = words_in_align()
    used = [False] * len(src_words)
    expanded = []
    piece_log = []
    for pi, (a, b, target, kind, tokens) in enumerate(PIECES):
        onset, _noise = attack_in(a, b)
        rel = release_end(a, b)
        expanded.append((a, b, target, kind, tokens, onset, rel))
        hit_ceil = rel is not None and rel + TAIL > b + 0.005
        lead_ms = None if onset is None else round((onset - a) * 1000, 1)
        tail_ms = None if rel is None else round((b - rel) * 1000, 1)
        fade_done = round(a if pi == 0 else a + XFADE, 3)
        piece_log.append({
            "i": pi, "tokens": tokens, "window": [a, b],
            "onset_s": onset, "offset_s": rel, "cut_s": a, "end_s": b,
            "lead_ms": lead_ms, "tail_ms": tail_ms,
            "fade_done_s": fade_done,
            "fade_before_onset": None if onset is None else fade_done <= onset + 1e-3,
            "opens_in_speech": bool(rms_db(a) > DB60),
            "silence_after": not hit_ceil,
            "src_edge_rms_db": [round(rms_db(a), 1), round(rms_db(max(a, b - 0.01)), 1)],
            "unbroken": True,
        })
    by_span: dict[int, list] = {}
    for pi, (a, b, _target, _kind, tokens, _on, _off) in enumerate(expanded):
        for tok in tokens:
            hit = None
            for k, (w, s, e) in enumerate(src_words):
                if used[k]:
                    continue
                if w.lower().strip(".,;:").startswith(tok) and a - 0.40 <= (s + e) / 2 <= b + 0.30:
                    hit = k
                    break
            if hit is None:
                raise SystemExit(f"missing word {tok!r} in {a:.2f}-{b:.2f}")
            used[hit] = True
            by_span.setdefault(pi, []).append(src_words[hit])

    def insert_for(i: int, pa: float, pb: float, target: float) -> float:
        if target <= 0 or i + 1 >= len(expanded):
            return 0.0
        npa, npb = expanded[i + 1][0], expanded[i + 1][1]
        tail = quiet_edge(pa, pb, True)
        lead = quiet_edge(npa, npb, False)
        return round(max(0.0, target - tail - lead + XFADE), 3)

    inserts = [insert_for(i, pa, pb, target) for i, (pa, pb, target, *_rest) in enumerate(expanded)]
    boil_i = next(i for i, (pa, pb, *_) in enumerate(expanded) if 7.0 <= pa <= 7.45 and pb <= 8.6)
    opener = slice_stereo(expanded[0][0], expanded[0][1])
    opener.extend(slice_stereo(expanded[1][0], expanded[1][1]))
    boil = slice_stereo(expanded[boil_i][0], expanded[boil_i][1])
    opener_gain = max(-6.0, min(8.0, speech_rms_db(boil) - speech_rms_db(opener)))

    nxf = int(XFADE * SR)
    out = array.array("h")
    subs: list[tuple] = []
    span_meta: list[dict] = []

    def assemble(gain: float, gaps: list[float]) -> tuple[array.array, list, list]:
        buf = array.array("h")
        built_subs = []
        built_meta = []
        for i, (pa, pb, target, kind, _tok, onset, rel) in enumerate(expanded):
            piece = slice_stereo(pa, pb)
            gain_db = 0.0
            if (4.0 <= pa <= 5.0) or (16.0 <= pa <= 17.2):
                piece = apply_gain(piece, gain)
                gain_db = gain
            if i == 0:
                buf.extend(piece)
                out_t = 0.0
            else:
                out_t = len(buf) / 2 / SR - XFADE
                buf = xfade(buf, piece, nxf)
            words_here = " ".join(w for w, _, _ in by_span.get(i, []))
            if not words_here.strip():
                raise SystemExit(f"span {i} has no words")
            built_subs.append((pa, pb, out_t, gain_db, onset, rel))
            built_meta.append({
                "i": i, "src": [pa, pb], "out": round(out_t, 3),
                "dur": round(pb - pa, 3), "gap_after": gaps[i], "gap_kind": kind,
                "gain_db": round(gain_db, 2), "words": words_here,
                "src_edge_rms_db": piece_log[i]["src_edge_rms_db"],
                "measured": "one unbroken source run; word times are stem energy",
            })
            if gaps[i] > 0:
                room = room_tone(int((gaps[i] + XFADE) * SR))
                buf = xfade(buf, room, nxf)
        return buf, built_subs, built_meta

    def speech_edges(buf: array.array, built_subs: list) -> list[tuple[float, float]]:
        edges = []
        for pa, pb, out_t, _g, onset, rel in built_subs:
            start = out_t + ((onset if onset is not None else pa) - pa)
            stop = out_t + ((rel if rel is not None else pb) - pa)
            # Re-measure on the stem so a clipped alignment end cannot win.
            t0, t1 = out_t, out_t + (pb - pa)
            on = off = None
            t = round(t0, 3)
            while t < t1 - 0.009:
                # Same floor as max_gaps (0.012 linear, about -38.4 dB).
                if stem_db(buf, t) > -38.4:
                    if on is None:
                        on = t
                    off = round(t + 0.01, 3)
                t = round(t + 0.01, 3)
            edges.append((on if on is not None else start, off if off is not None else stop))
        return edges

    heard = []
    for _attempt in range(6):
        out, subs, span_meta = assemble(opener_gain, inserts)
        edges = speech_edges(out, subs)
        boil_out = subs[boil_i][2]
        boil_end = boil_out + (expanded[boil_i][1] - expanded[boil_i][0])
        hook_db2 = speech_rms_db(slice_stereo_from(out, 0.0, 1.45))
        boil_db2 = speech_rms_db(slice_stereo_from(out, boil_out, min(boil_end, boil_out + 1.2)))
        diff = hook_db2 - boil_db2
        if abs(diff) > 0.35:
            opener_gain = max(-6.0, min(8.0, round(opener_gain - diff, 2)))
        heard = []
        ok_gaps = True
        for i in range(len(edges) - 1):
            gap = round(edges[i + 1][0] - edges[i][1], 3)
            kind = expanded[i][3]
            target = expanded[i][2]
            heard.append({"after": " ".join(by_span[i][-1][0:1]), "before": by_span[i + 1][0][0],
                          "gap_s": gap, "kind": kind, "target": target})
            if target <= 0:
                continue
            err = target - gap
            if abs(err) > 0.012 and not (err < 0 and inserts[i] <= 0.0):
                ok_gaps = False
                inserts[i] = round(max(0.0, inserts[i] + err), 3)
        if ok_gaps and abs(diff) <= 0.35:
            break

    mapped = []
    edges = speech_edges(out, subs)
    for i, items in by_span.items():
        pa, pb, out_t = subs[i][0], subs[i][1], subs[i][2]

        def mmap(src: float, _out=out_t, _pa=pa, _pb=pb) -> float:
            return _out + (min(max(src, _pa), _pb) - _pa)

        on, off = edges[i]
        starts = [mmap(s) for _w, s, _e in items]
        ends = [mmap(e) for _w, _s, e in items]
        # First word opens on the speech, last word keeps the tail alignment cuts off.
        starts[0] = on
        if ends[-1] < off:
            ends[-1] = off
        for n in range(len(items)):
            if n:
                starts[n] = max(starts[n], ends[n - 1])
            if ends[n] < starts[n] + 0.04:
                ends[n] = starts[n] + 0.04
            if n + 1 < len(items) and ends[n] > starts[n + 1]:
                ends[n] = starts[n + 1]
        for n, (w, _s, _e) in enumerate(items):
            mapped.append((w, round(starts[n], 3), round(ends[n], 3)))
    mapped.sort(key=lambda r: (r[1], r[2]))

    speech = work / f"hos_001_{SID}_vo_{VER}.wav"
    write_wav(speech, out)
    boil_out = subs[boil_i][2]
    boil_end = boil_out + (expanded[boil_i][1] - expanded[boil_i][0])
    hook_db2 = speech_rms_db(slice_stereo_from(out, 0.0, 1.45))
    boil_db2 = speech_rms_db(slice_stereo_from(out, boil_out, min(boil_end, boil_out + 1.2)))
    gaps = max_gaps(out)
    worst = max((g["dur"] for g in gaps), default=0.0)
    info = {
        "opener_gain_db": round(opener_gain, 2),
        "hook_speech_db": round(hook_db2, 2),
        "boil_speech_db": round(boil_db2, 2),
        "hook_minus_boil_db": round(hook_db2 - boil_db2, 2),
        "gaps": gaps,
        "max_gap_s": round(worst, 3),
        "heard_gaps": heard,
        "inserts": inserts,
        "subs": len(subs),
        "pieces": piece_log,
    }
    return speech, mapped, span_meta, info


def stem_db(samples: array.array, t: float) -> float:
    """10 ms RMS of a built stem, dBFS."""
    i0 = int(t * SR)
    hop = SR // 100
    frames = len(samples) // 2
    if i0 < 0 or i0 + hop > frames:
        return -99.0
    acc = 0.0
    base = i0 * 2
    for j in range(hop):
        v = samples[base + j * 2] / 32768.0
        acc += v * v
    rms = math.sqrt(acc / hop)
    return -99.0 if rms <= 1e-9 else 20 * math.log10(rms)


def slice_stereo_from(samples: array.array, a: float, b: float) -> array.array:
    i0 = max(0, int(a * SR))
    i1 = min(len(samples) // 2, int(b * SR))
    return array.array("h", samples[i0 * 2:i1 * 2])


def chunk_words(words: list[tuple[str, float, float]]) -> list[dict]:
    chunks, i, n = [], 0, len(words)
    while i < n:
        t0 = words[i][1]
        parts, t_end, j = [words[i][0]], words[i][2], i + 1
        while j < n:
            wj, sj, ej = words[j]
            if parts[-1][-1:] in ".?!":
                break
            if ej - t0 >= 1.55 and len(parts) >= 2:
                break
            if len(parts) >= 5 and sj - t0 >= 0.45:
                break
            parts.append(wj)
            t_end = ej
            j += 1
        t1 = words[j][1] if j < n else t_end + 0.12
        chunks.append({"text": " ".join(parts), "t0": round(t0, 3), "t1": round(min(t1, t_end + 0.12), 3)})
        i = j
    # Exclusive handovers: each chunk ends where the next starts.
    for k in range(len(chunks) - 1):
        chunks[k]["t1"] = chunks[k + 1]["t0"]
    return chunks


def caption_chunks(words: list[tuple[str, float, float]]) -> list[dict]:
    """One card per group, in spoken order. v05 dropped Boil broth and If life arrives as."""
    groups = [
        ["a", "flask", "stays", "clear"],
        ["boil", "broth"],
        ["air", "can", "drift"],
        ["but", "dust", "and", "microbes"],
        ["settle", "in", "the", "curve"],
        ["if", "life", "arrives", "as"],
        ["passengers", "from", "the", "outside"],
        ["then", "disease", "can", "be", "a", "passenger", "too"],
        ["break", "the", "neck"],
        ["or", "tip", "the", "trap"],
        ["and", "life", "blooms", "into", "cloudiness"],
        ["keep", "the", "swan", "neck", "intact"],
    ]
    idx = 0
    chunks = []
    for g in groups:
        got = words[idx:idx + len(g)]
        if len(got) != len(g):
            raise SystemExit(f"caption ran out at {g[0]!r}")
        for tok, (w, _s, _e) in zip(g, got):
            if not w.lower().strip(".,;:").startswith(tok):
                raise SystemExit(f"caption wanted {tok!r}, heard {w!r}")
        text = " ".join(w for w, _, _ in got)
        if g[0] == "air" and not text.rstrip().endswith(","):
            text += ","
        nxt = idx + len(g)
        t0 = got[0][1]
        t1 = words[nxt][1] if nxt < len(words) else got[-1][2] + 0.12
        chunks.append({"text": text, "t0": round(t0, 3), "t1": round(t1, 3)})
        idx = nxt
    if idx != len(words):
        raise SystemExit(f"captions covered {idx} of {len(words)} words")
    joined = norm_tokens(" ".join(c["text"] for c in chunks))
    spoken = norm_tokens(" ".join(w for w, _, _ in words))
    if joined != spoken:
        raise SystemExit(f"captions != spoken\n{joined}\n{spoken}")
    need = ("boil broth", "if life arrives as", "air can drift", "but dust and microbes", "settle in the curve")
    flat = " ".join(joined)
    for phrase in need:
        if phrase not in flat:
            raise SystemExit(f"caption missing {phrase}")
    return chunks


def render_text(path: Path, text: str, size: int, y: int, *, anchor: str = "top", font_path: str = FONT,
                index: int = 0, stroke: int = 3) -> None:
    font = ImageFont.truetype(font_path, size, index=index)
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    tokens = [(w.strip("*"), w.startswith("**")) for w in text.split()]
    lines, cur = [], []
    for tok in tokens:
        trial = " ".join(t for t, _ in cur + [tok])
        if cur and font.getlength(trial) > W - 96:
            lines.append(cur)
            cur = [tok]
        else:
            cur.append(tok)
    lines.append(cur)
    asc, desc = font.getmetrics()
    lh, gap = asc + desc, int(size * 0.12)
    block = lh * len(lines) + gap * (len(lines) - 1)
    cy = H - y - block if anchor == "bottom" else y
    space = font.getlength(" ")
    for line in lines:
        x = (W - font.getlength(" ".join(t for t, _ in line))) / 2
        for t, hot in line:
            draw.text((x, cy), t, font=font, fill=YEL if hot else CREAM, stroke_width=stroke, stroke_fill=INK)
            x += font.getlength(t) + space
        cy += lh + gap
    img.save(path)


def render_hook(path: Path) -> dict:
    tokens = [(w.strip("*"), w.startswith("**")) for w in HOOK.split()]
    size = 60
    while True:
        font = ImageFont.truetype(FONT, size, index=2)
        cap = -font.getbbox("H", anchor="ls")[1]
        if cap >= 0.086 * H:
            break
        size += 1
    widest = max(font.getlength(t) for t, _ in tokens)
    if widest > W - 80:
        raise SystemExit(f"hook too wide ({widest:.0f}px)")
    pitch = round(cap * 1.28)
    block = pitch * (len(tokens) - 1) + cap
    # Above the stayed-gate centre band (y < 0.28 H), so the hook does not freeze that band.
    top = int(0.025 * H)
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    for k, (t, hot) in enumerate(tokens):
        base = top + cap + k * pitch
        draw.text((W / 2, base), t, font=font, anchor="ms", fill=YEL if hot else CREAM,
                  stroke_width=6, stroke_fill=INK)
    img.save(path)
    if top + block > 0.27 * H:
        raise SystemExit(f"hook ends at {(top + block) / H:.1%}, inside the stayed-gate centre band")
    return {"font_size": size, "cap_pct": round(100 * cap / H, 2),
            "block_pct": [round(100 * top / H, 1), round(100 * (top + block) / H, 1)]}


def render_card(path: Path) -> None:
    size1 = int(BAND_H * 0.11)
    size2 = int(BAND_H * 0.075)
    f1 = ImageFont.truetype(FONT, size1, index=2)
    f2 = ImageFont.truetype(CTA_FONT, size2)
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    x = 70
    y2 = BAND_TOP + BAND_H - 40
    y1 = y2 - size2 - 18
    shade = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shade)
    top, bot = y1 - size1 - 30, BAND_TOP + BAND_H + 80
    for yy in range(top, bot):
        ramp = min(1.0, (yy - top) / 120, (bot - yy) / 120)
        a = int(140 * 0.5 * (1 - math.cos(math.pi * ramp)))
        sd.line([(0, yy), (W, yy)], fill=(0, 0, 0, a))
    img = Image.alpha_composite(img, shade)
    d = ImageDraw.Draw(img)
    d.text((x, y1), CARD[0], font=f1, anchor="ls", fill=YEL, stroke_width=4, stroke_fill=INK)
    d.text((x, y2), CARD[1], font=f2, anchor="ls", fill=CREAM, stroke_width=3, stroke_fill=INK)
    img.save(path)


def plate(name: str) -> Path:
    p = resolve_media(f"{PLATE}/{name}.mp4")
    if not p.exists():
        raise SystemExit(f"missing plate {p}")
    return p


def seg(src: Path, dst: Path, start: float, nframes: int, x: int) -> None:
    """Exactly nframes, starting at `start`. The fps filter must not invent an extra frame."""
    if start < 0:
        raise SystemExit(f"{src.name}: negative in-point {start}")
    dur = nframes / FPS
    if start + dur > probe(src) + 1 / FPS:
        raise SystemExit(f"{src.name}: in {start} + {dur:.3f} runs past the plate ({probe(src):.2f})")
    vf = (f"trim=start={start:.6f}:duration={dur:.6f},setpts=PTS-STARTPTS,"
          f"scale=1920:1080,crop=608:1080:{x}:0,scale={W}:{H}:flags=lanczos,fps={FPS},setsar=1")
    ff("-i", str(src), "-filter_complex", vf, "-an", "-c:v", "libx264", "-pix_fmt", "yuv420p",
       "-preset", "fast", "-crf", "16", "-r", str(FPS), "-frames:v", str(nframes), str(dst))


def word_start(words: list[tuple[str, float, float]], token: str, after: float = -1.0) -> float:
    hits = [s for w, s, e in words if w.lower().strip(".,;:").startswith(token) and s >= after]
    if not hits:
        raise SystemExit(f"no word {token!r} after {after}")
    return hits[0]


def body_cuts(words: list[tuple[str, float, float]], vo_s: float, loop_s: float) -> list[tuple]:
    """Picture follows the words. Every hold is at most 3.0 s. Loop returns to frame 0's plate."""
    flask = plate("01_question_mark_flask_v17")
    boil_t = word_start(words, "boil")
    air_t = word_start(words, "air")
    dust_t = word_start(words, "dust")
    if_t = word_start(words, "if")
    then_t = word_start(words, "then")
    break_t = word_start(words, "break")
    lives = [s for w, s, e in words if w.lower().startswith("life")]
    life_t = lives[-1]
    and_t = max(s for w, s, e in words if w.lower().startswith("and") and s < life_t)
    keep_t = word_start(words, "keep")
    pass_end = min(then_t, if_t + 2.95)
    rows = [
        (0.0, boil_t, flask, FLASK_IN, FLASK_CROP, "flask"),
        (boil_t, air_t, plate("02_boil_broth_v04"), 0.45, 480, "boil"),
        (air_t, dust_t, plate("03_dust_in_the_curve_v23"), 0.40, 640, "dust"),
        (dust_t, if_t, plate("03_dust_in_the_curve_v23"), 3.40, 560, "dust2"),
        (if_t, pass_end, plate("08_passengers_v20"), 0.35, 380, "passengers"),
        (pass_end, break_t, plate("04_still_clear_v21"), 0.50, 640, "clear"),
        (break_t, and_t, plate("05_tip_the_trap_v20"), 0.40, 520, "tip"),
        (and_t, keep_t, plate("07_bloom_cloud_v02"), 2.20, 500, "bloom"),
        (keep_t, vo_s, plate("11_result_returns_v01"), 0.50, 560, "result"),
    ]
    out = []
    for t0, t1, src, ins, x, label in rows:
        d = t1 - t0
        if d <= 0.05:
            raise SystemExit(f"{label} hold {d:.3f}s")
        if d <= 3.0:
            out.append((round(t0, 3), round(t1, 3), src, ins, x, label))
            continue
        # A row over 3.0 s is split on the same plate, in-point moving forward.
        cursor, inn, n = t0, ins, 0
        while t1 - cursor > 3.0 + 1e-3:
            step = 2.9
            if t1 - (cursor + step) < 0.45:
                step = (t1 - cursor) / 2
            out.append((round(cursor, 3), round(cursor + step, 3), src, round(inn, 4), x, f"{label}_{n}"))
            cursor += step
            inn += step
            n += 1
        out.append((round(cursor, 3), round(t1, 3), src, round(inn, 4), x, f"{label}_{n}"))
    # Last frame is the plate frame one output frame before frame 0's in-point (1.80 s).
    # Ending ON 1.80, then pasting frame 0, is the v04 one-frame flick.
    n_loop = max(2, int(round(loop_s * FPS)))
    loop_dur = n_loop / FPS
    loop_in = round(FLASK_IN - loop_dur, 4)
    if loop_in < 0:
        raise SystemExit(f"loop in-point {loop_in}")
    out.append((round(vo_s, 3), round(vo_s + loop_dur, 3), flask, loop_in, FLASK_CROP, "loop"))
    if out[1][0] > 2.60:
        raise SystemExit(f"first cut {out[1][0]}")
    return out


def synth_bed(path: Path, dur: float, sr: int = 48000) -> None:
    """Own pad, A-leaning partials, 76 BPM. Not the v02 F-major bed or the v03 D pad."""
    n = int(sr * dur)
    freqs = [110.0, 164.81, 220.0, 277.18, 329.63]
    amps = [0.28, 0.22, 0.16, 0.11, 0.07]
    frames = bytearray()
    for i in range(n):
        t = i / sr
        pulse = 0.78 + 0.22 * math.sin(2 * math.pi * (76 / 60) * t)
        env = min(1.0, t / 0.35) * min(1.0, max(0.0, (dur - t) / 0.30))
        l = r = 0.0
        for k, (f, a) in enumerate(zip(freqs, amps)):
            l += math.sin(2 * math.pi * f * t + 0.4 * k) * a
            r += math.sin(2 * math.pi * (f * 1.0015) * t + 0.7 * k) * a
        g = env * pulse * 0.22
        frames += struct.pack("<hh", int(max(-1, min(1, l * g)) * 32767), int(max(-1, min(1, r * g)) * 32767))
    with wave.open(str(path), "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(sr)
        w.writeframes(bytes(frames))


def place_sfx(work: Path, total: float) -> Path:
    kit = PROJ / "06_Sound-Effects" / "kit_v01"
    if not (kit / "sfx_hos_whoosh_soft_v01.wav").exists():
        subprocess.run([sys.executable, str(OWB / "scripts/sfx_kit.py"), "make", "--out-dir", str(kit),
                        "--house", "hos"], check=True)
    whoosh = kit / "sfx_hos_whoosh_soft_v01.wav"
    tick = kit / "sfx_hos_tick_ink_v01.wav"
    dst = work / "sfx_stem.wav"
    # Whoosh at frame 0, one ink tick as the Pasteur card arrives. Quiet; the level gate sets the gain.
    ff("-f", "lavfi", "-t", f"{total:.3f}", "-i", "anullsrc=channel_layout=stereo:sample_rate=48000",
       "-i", str(whoosh), "-i", str(tick),
       "-filter_complex",
       "[1:a]volume=-16dB,afade=t=out:st=0.75:d=0.2[w];"
       "[2:a]volume=-10dB,adelay=2200|2200[t];"
       "[0:a][w][t]amix=inputs=3:normalize=0:duration=first,alimiter=limit=0.5[a]",
       "-map", "[a]", "-c:a", "pcm_s16le", str(dst))
    return dst


def mix(vo: Path, bed: Path, sfx: Path, total: float, dst: Path, bed_db: float, sfx_db: float) -> None:
    ff("-i", str(vo), "-i", str(bed), "-i", str(sfx), "-filter_complex",
       f"[0:a]aformat=sample_rates=48000:channel_layouts=stereo,apad=whole_dur={total:.3f}[v];"
       f"[1:a]aformat=sample_rates=48000:channel_layouts=stereo,atrim=0:{total:.3f},volume={bed_db:.2f}dB[b];"
       f"[2:a]aformat=sample_rates=48000:channel_layouts=stereo,atrim=0:{total:.3f},volume={sfx_db:.2f}dB[s];"
       f"[v][b][s]amix=inputs=3:normalize=0:duration=first,alimiter=limit=0.9[a]",
       "-map", "[a]", "-t", f"{total:.3f}", "-c:a", "pcm_s16le", str(dst))


def pin_loop_predecessor(pic: Path, n_frames: int) -> None:
    """Last frame is the plate frame one output frame before frame 0's in-point.

    v04 copied frame 0 onto the end, so the file stepped back on the next frame.
    This writes the predecessor plate only. It is not a copy of frame 0.
    """
    pred = WORK / "loop_pred.png"
    src = plate("01_question_mark_flask_v17")
    start = FLASK_IN - (1 / FPS)
    vf = (f"trim=start={start:.4f}:duration={1 / FPS:.4f},setpts=PTS-STARTPTS,"
          f"scale=1920:1080,crop=608:1080:{FLASK_CROP}:0,scale={W}:{H}:flags=lanczos,fps={FPS},setsar=1")
    ff("-i", str(src), "-filter_complex", vf, "-frames:v", "1", str(pred))
    tmp = WORK / "picture_loop.mp4"
    ff("-i", str(pic), "-i", str(pred), "-filter_complex",
       f"[1:v]scale={W}:{H},fps={FPS},format=yuv420p[f];"
       f"[0:v][f]overlay=enable='eq(n,{n_frames - 1})'[v]",
       "-map", "[v]", "-an", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "fast", "-crf", "16",
       "-r", str(FPS), "-frames:v", str(n_frames), str(tmp))
    tmp.replace(pic)


def force_last_frame(pic: Path, total: float) -> None:
    """Last picture frame becomes the frame-0 picture, so the loop seam matches."""
    frame0 = WORK / "frame0_pic.png"
    ff("-i", str(pic), "-frames:v", "1", str(frame0))
    n = int(round(total * FPS))
    tmp = WORK / "picture_matched.mp4"
    ff("-i", str(pic), "-i", str(frame0), "-filter_complex",
       f"[1:v]scale={W}:{H},fps={FPS},format=yuv420p[f];"
       f"[0:v][f]overlay=enable='eq(n,{n - 1})'[v]",
       "-map", "[v]", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "fast", "-crf", "16",
       "-r", str(FPS), "-t", f"{total:.3f}", str(tmp))
    tmp.replace(pic)


def loop_diff(mp4: Path) -> float:
    """Mean abs luma diff, last frame vs frame 0, with hook/caption/card text masked."""
    a = WORK / "diff_a.png"
    b = WORK / "diff_b.png"
    ff("-i", str(mp4), "-frames:v", "1", str(a))
    ff("-sseof", "-0.05", "-i", str(mp4), "-frames:v", "1", str(b))
    im_a = Image.open(a).convert("RGB")
    im_b = Image.open(b).convert("RGB").resize(im_a.size)
    im_b.save(b)
    # Text mask: pixels on frame 0 that are cream or yellow and differ from the last frame.
    pa, pb = im_a.load(), im_b.load()
    w, h = im_a.size
    mask = Image.new("L", (w, h), 0)
    mpix = mask.load()
    for y in range(h):
        for x in range(w):
            r, g, bl = pa[x, y]
            r2, g2, b2 = pb[x, y]
            cream = r > 200 and g > 185 and bl > 150 and abs(r - g) < 50
            ink = r < 40 and g < 40 and bl < 40
            # Hook word is yellow (255, 214, 70). Cream's blue floor misses it,
            # and that word alone held the masked seam at 6.3.
            yellow = r > 200 and g > 160 and bl < 140 and g > bl + 80
            differ = abs(r - r2) + abs(g - g2) + abs(bl - b2) > 80
            if differ and (cream or ink or yellow):
                mpix[x, y] = 255
    mask = mask.filter(ImageFilter.MaxFilter(5))
    mpix = mask.load()
    acc = n = whole = nw = 0
    for y in range(0, h, 2):
        for x in range(0, w, 2):
            r, g, bl = pa[x, y]
            r2, g2, b2 = pb[x, y]
            la = 0.2126 * r + 0.7152 * g + 0.0722 * bl
            lb = 0.2126 * r2 + 0.7152 * g2 + 0.0722 * b2
            d = abs(la - lb)
            whole += d
            nw += 1
            if mpix[x, y]:
                continue
            acc += d
            n += 1
    return round(acc / max(1, n), 2), round(whole / max(1, nw), 2)


def loudnorm_to(src: Path, dst: Path) -> None:
    """Land on -14 LUFS with true peak at or under -1.5 dBTP.

    alimiter's default level=true boosts up to the ceiling, which is how a
    -1 dB trim came back out at 0 dBTP. level=disabled keeps the cut.
    """
    ff("-i", str(src), "-af", "loudnorm=I=-14.2:TP=-1.8:LRA=11,alimiter=limit=0.841:level=disabled",
       "-c:a", "pcm_s16le", str(dst))
    for _ in range(3):
        got = integrated_lufs(dst)
        peak = true_peak(dst)
        if -14.45 <= got <= -13.55 and peak <= -1.05:
            return
        delta = -14.15 - got
        tmp = dst.with_name(dst.stem + "_trim.wav")
        ff("-i", str(dst), "-af", f"volume={delta:.2f}dB,alimiter=limit=0.841:level=disabled",
           "-c:a", "pcm_s16le", str(tmp))
        tmp.replace(dst)


def black_frac(mp4: Path, t: float) -> float:
    raw = subprocess.check_output(["ffmpeg", "-v", "error", "-ss", f"{t:.3f}", "-i", str(mp4),
                                   "-frames:v", "1", "-vf", "scale=160:284", "-f", "rawvideo", "-pix_fmt", "gray", "-"])
    dark = sum(1 for p in raw if p < 18)
    return round(dark / max(1, len(raw)), 3)


def synth_and_gates(vo: Path, total: float) -> dict:
    bed = PROJ / "05_Music" / f"hos_001_{SID}_{VER}_bed.wav"
    bed.parent.mkdir(parents=True, exist_ok=True)
    synth_bed(bed, total + 0.2)
    plan = {
        "prompt": ("Quiet laboratory pad under a spoken demonstration, slow and even, no chase. "
                   "Pace: 68-78 BPM. NOT a trailer sting, NOT a piano solo, NOT the F-major flask pad "
                   "from s11 v02, NOT the D-leaning 72 BPM pad from s11 v03, NOT any Orbit With Ben bed, "
                   "NOT a drum loop."),
        "film": "001",
        "short": f"{SID}_{VER}",
        "job": JOB,
        "source": "own synthesis in _build_short_s11_curved_flask_v06.py, same pad as v05, 0 credits",
    }
    bed.with_name(bed.stem + "_plan.json").write_text(json.dumps(plan, indent=2) + "\n")
    sfx = place_sfx(WORK, total)
    vo_i = integrated_lufs(vo)
    # Start well under the VO. The level gate reads these stems, not the loudnormed mix.
    bed_db, sfx_db = -8.0, -8.0
    audio = WORK / "audio.wav"
    level = {}
    for _ in range(4):
        mix(vo, bed, sfx, total, audio, bed_db, sfx_db)
        # Stems at the same gain the mix uses, padded to the cut, so the gate's clocks line up.
        vo_stem = WORK / "stem_vo.wav"
        bed_stem = WORK / "stem_bed.wav"
        sfx_stem = WORK / "stem_sfx.wav"
        ff("-i", str(vo), "-af", f"apad=whole_dur={total:.3f}", "-t", f"{total:.3f}", "-c:a", "pcm_s16le", str(vo_stem))
        ff("-i", str(bed), "-af", f"volume={bed_db:.2f}dB,atrim=0:{total:.3f}", "-c:a", "pcm_s16le", str(bed_stem))
        ff("-i", str(sfx), "-af", f"volume={sfx_db:.2f}dB,atrim=0:{total:.3f}", "-c:a", "pcm_s16le", str(sfx_stem))
        r = subprocess.run([sys.executable, str(OWB / "scripts/sfx_kit.py"), "level",
                            "--vo", str(vo_stem), "--sfx", str(sfx_stem), "--bed", str(bed_stem),
                            "--minutes", f"{total / 60:.3f}", "--out", str(QA / "sfx_level.json")],
                           capture_output=True, text=True)
        level = {"exit": r.returncode, "output": (r.stdout + r.stderr).strip(), "bed_db": bed_db, "sfx_db": sfx_db}
        if r.returncode == 0:
            break
        bed_db -= 3.0
        sfx_db -= 3.0
    return {"audio": audio, "bed": bed, "level": level, "vo_i": vo_i}


def run_qa(mp4: Path, plan: list[dict]) -> dict:
    QA.mkdir(parents=True, exist_ok=True)
    cuts, pool, seen = [], [], set()
    for k, row in enumerate(plan, 1):
        base = Path(row["plate"]).name
        src_id = f"loop_end_{base}" if row["label"] == "loop" else base
        cuts.append({"row": f"s{k:02d}_{row['label']}", "timeline_in": row["t0"], "timeline_out": row["t1"],
                     "source": src_id, "upscale": round(1080 / 608, 3), "video": True,
                     "framing": {"offset": row["in_s"]}})
        if src_id not in seen:
            seen.add(src_id)
            pool.append({"file_id": src_id, "title": f"Flow Veo plate {base}"})
    cuts_f = QA / f"cuts_{SID}_{VER}.json"
    pool_f = QA / f"pool_{SID}_{VER}.json"
    cuts_f.write_text(json.dumps(cuts, indent=2) + "\n")
    pool_f.write_text(json.dumps(pool, indent=2) + "\n")
    rel = lambda p: str(p.relative_to(REPO))  # noqa: E731
    r_pg = subprocess.run([sys.executable, str(OWB / "scripts/polish_gate.py"), rel(mp4),
                           "--cuts", rel(cuts_f), "--out", rel(QA / f"polish_gate_{SID}_{VER}.json")],
                          cwd=REPO, capture_output=True, text=True)
    (QA / f"polish_gate_{SID}_{VER}.txt").write_text((r_pg.stdout + r_pg.stderr).strip() + "\n")
    r_pq = subprocess.run([sys.executable, str(OWB / "scripts/picture_qa.py"), rel(mp4),
                           "--cuts", rel(cuts_f), "--pool", rel(pool_f),
                           "--out-dir", rel(QA / f"picture_qa_{SID}_{VER}")],
                          cwd=REPO, capture_output=True, text=True)
    (QA / f"picture_qa_{SID}_{VER}.txt").write_text((r_pq.stdout + r_pq.stderr).strip() + "\n")
    return {"polish_gate": {"exit": r_pg.returncode, "tail": (r_pg.stdout + r_pg.stderr).strip().splitlines()[-3:]},
            "picture_qa": {"exit": r_pq.returncode, "tail": (r_pq.stdout + r_pq.stderr).strip().splitlines()[-5:]}}


def sheet_2fps(mp4: Path) -> Path:
    out = QA / f"{mp4.stem}_2fps_sheet.jpg"
    ff("-i", str(mp4), "-vf", "fps=2,scale=180:-2,tile=8x6", "-q:v", "4", str(out))
    return out


def copy_out(mp4: Path, phone: Path, sheet: Path) -> dict:
    uat = Path.home() / "Library/Mobile Documents/com~apple~CloudDocs/HOS UAT/001_How-Did-We-Discover-Germs/10_Shorts"
    nas = NAS_PROJ / "10_Shorts" / f"{SID}_{VER}"
    copied = []
    for folder in (uat, nas):
        if not folder.parent.exists() and folder == nas:
            continue
        folder.mkdir(parents=True, exist_ok=True)
        for src in (mp4, phone, sheet):
            shutil.copy2(src, folder / src.name)
            copied.append(str(folder / src.name))
    return {"copied": copied}


def check_pieces(pieces: list[dict]) -> None:
    bad = []
    if len(pieces) != 11:
        bad.append(f"{len(pieces)} pieces, want 11")
    for p in pieces:
        tok = p["tokens"][0]
        if tok == "a":
            if abs(p["cut_s"] - 4.12) > 0.006:
                bad.append(f"opener cut {p['cut_s']}")
            continue
        if tok == "boil":
            if p["cut_s"] > 7.331:
                bad.append(f"boil cut {p['cut_s']}")
            if p["fade_done_s"] >= 7.349:
                bad.append(f"boil fade {p['fade_done_s']}")
        if p["onset_s"] is None:
            bad.append(f"{tok} no onset")
            continue
        if not p["opens_in_speech"]:
            if p["lead_ms"] is None or p["lead_ms"] < 19.5:
                bad.append(f"{tok} lead {p['lead_ms']}ms")
            if p["fade_before_onset"] is False:
                bad.append(f"{tok} fade {p['fade_done_s']} after onset {p['onset_s']}")
        if p["silence_after"] and (p["tail_ms"] is None or p["tail_ms"] < 29):
            bad.append(f"{tok} tail {p['tail_ms']}ms")
        if p["offset_s"] is not None and p["end_s"] + 0.005 < p["offset_s"]:
            bad.append(f"{tok} ends {p['end_s']} before offset {p['offset_s']}")
    if bad:
        raise SystemExit("onset rule: " + "; ".join(bad))


def norm_tokens(text: str) -> list[str]:
    return re.findall(r"[a-z']+", text.lower().replace("’", "'"))


def whisper_words(wav: Path) -> dict:
    py = Path.home() / ".venvs/hos-vo/bin/python"
    if not py.exists():
        raise SystemExit(f"no faster-whisper venv at {py}")
    code = (
        "import json,sys\n"
        "from faster_whisper import WhisperModel\n"
        "m=WhisperModel('small.en', device='cpu', compute_type='int8')\n"
        "segs,_=m.transcribe(sys.argv[1], language='en', word_timestamps=True, vad_filter=False)\n"
        "words=[]\n"
        "for s in segs:\n"
        "    for w in (s.words or []):\n"
        "        words.append({'word':w.word.strip(),'start':round(w.start,3),'end':round(w.end,3)})\n"
        "text=' '.join(w['word'] for w in words)\n"
        "print(json.dumps({'text':text,'words':words}))\n"
    )
    r = subprocess.run([str(py), "-c", code, str(wav)], capture_output=True, text=True)
    if r.returncode != 0:
        raise SystemExit(f"whisper failed: {r.stderr[-800:]}")
    return json.loads(r.stdout)


def _pad_span(src: Path, a: float, b: float, dst: Path) -> None:
    a = max(0.0, a)
    ff("-i", str(src), "-af",
       f"atrim=start={a:.3f}:end={b:.3f},asetpts=PTS-STARTPTS,adelay=500|500,apad=pad_dur=0.5",
       "-c:a", "pcm_s16le", str(dst))


def _fold_asr(got: list[str], want: list[str]) -> list[str]:
    folded = list(got)
    for i, tok in enumerate(folded):
        if i < len(want) and want[i] == "a" and tok == "the":
            folded[i] = "a"
        if i < len(want) and want[i] == "too" and tok == "to":
            folded[i] = "too"
    return folded


def fragment_asr(vo: Path, span_meta: list[dict], words: list[tuple[str, float, float]]) -> dict:
    """small.en on each played span and on each join. One model load."""
    py = Path.home() / ".venvs/hos-vo/bin/python"
    jobs = []
    for sp in span_meta:
        dst = WORK / f"frag_span_{sp['i']:02d}.wav"
        _pad_span(vo, sp["out"], sp["out"] + sp["dur"], dst)
        jobs.append({"kind": "span", "i": sp["i"], "wav": str(dst), "want": sp["words"]})
    for i in range(len(span_meta) - 1):
        boundary = span_meta[i + 1]["out"]
        # Whole words around the join, wide enough that small.en is not handed a chopped syllable.
        win_a, win_b = boundary - 0.7, boundary + 0.7
        overlap = [(w, s, e) for w, s, e in words if e >= win_a and s <= win_b]
        if not overlap:
            overlap = [min(words, key=lambda r: abs((r[1] + r[2]) / 2 - boundary))]
        dst = WORK / f"frag_join_{i:02d}.wav"
        _pad_span(vo, max(0.0, overlap[0][1] - 0.06), overlap[-1][2] + 0.06, dst)
        jobs.append({"kind": "join", "i": i, "wav": str(dst),
                     "want": " ".join(w for w, _, _ in overlap), "t": round(boundary, 3)})
    manifest = WORK / "frag_jobs.json"
    manifest.write_text(json.dumps(jobs))
    code = r'''
import json, sys
from faster_whisper import WhisperModel
m = WhisperModel("small.en", device="cpu", compute_type="int8")
jobs = json.load(open(sys.argv[1]))
out = []
for job in jobs:
    segs, _ = m.transcribe(job["wav"], language="en", word_timestamps=True, vad_filter=False)
    words = []
    for s in segs:
        for w in (s.words or []):
            words.append(w.word.strip())
    out.append({"kind": job["kind"], "i": job["i"], "text": " ".join(words), "want": job["want"]})
print(json.dumps(out))
'''
    r = subprocess.run([str(py), "-c", code, str(manifest)], capture_output=True, text=True)
    if r.returncode != 0:
        raise SystemExit(f"fragment whisper failed: {r.stderr[-800:]}")
    rows = json.loads(r.stdout)
    notes = []
    table = []
    spoken_toks = set(norm_tokens(" ".join(w for w, _, _ in words)))
    for row in rows:
        want = norm_tokens(row["want"])
        got = _fold_asr(norm_tokens(row["text"]), want)
        partial = [g for g in got if g not in spoken_toks and any(
            w.startswith(g) and g != w and len(g) >= 3 for w in want)]
        if row["kind"] == "span":
            ok = (not partial) and _contains(got, want)
        else:
            # The join window must contain its words, in order, and no chopped token.
            ok = (not partial) and _contains(got, want)
        if not ok:
            notes.append(f"{row['kind']} {row['i']}: {row['text']!r} want {row['want']!r}")
        table.append({**row, "ok": ok})
    return {"ok": not notes, "notes": notes, "table": table}


def _contains(got: list[str], want: list[str]) -> bool:
    if not want:
        return True
    n = len(want)
    folded_sets = []
    # a/the and too/to already folded against a same-length want; joins can be longer.
    for i in range(len(got) - n + 1):
        window = got[i:i + n]
        if window == want:
            return True
        alt = []
        for g, w in zip(window, want):
            if g == "the" and w == "a":
                alt.append("a")
            elif g in ("to", "2", "two") and w == "too":
                alt.append("too")
            else:
                alt.append(g)
        if alt == want:
            return True
    return False


def tail_steps(mp4: Path, n: int = 11) -> dict:
    """Masked luma step between the last n frames. A pasted frame jumps; a plate step does not."""
    start = max(0.0, probe(mp4) - (n + 0.2) / FPS)
    folder = WORK / "tail_frames"
    if folder.exists():
        shutil.rmtree(folder)
    folder.mkdir()
    ff("-ss", f"{start:.3f}", "-i", str(mp4), "-frames:v", str(n), str(folder / "f%02d.png"))
    frames = sorted(folder.glob("f*.png"))
    if len(frames) < 2:
        return {"max_step": 99.0, "steps": [], "n": len(frames)}
    steps = []
    full_steps = []
    y0, y1 = BAND_TOP, BAND_TOP + BAND_H
    for a, b in zip(frames, frames[1:]):
        im_a = Image.open(a).convert("RGB")
        im_b = Image.open(b).convert("RGB")
        pa, pb = im_a.load(), im_b.load()
        w, h = im_a.size

        def mean_step(y_start: int, y_end: int) -> float:
            acc = count = 0.0
            for y in range(y_start, y_end, 2):
                for x in range(0, w, 2):
                    r, g, bl = pa[x, y]
                    r2, g2, b2 = pb[x, y]
                    cream = r > 200 and g > 185 and bl > 150
                    yellow = r > 200 and g > 160 and bl < 140 and g > bl + 80
                    ink = r < 40 and g < 40 and bl < 40
                    if cream or yellow or ink:
                        continue
                    la = 0.2126 * r + 0.7152 * g + 0.0722 * bl
                    lb = 0.2126 * r2 + 0.7152 * g2 + 0.0722 * b2
                    acc += abs(la - lb)
                    count += 1
            return round(acc / max(1, count), 2)

        steps.append(mean_step(y0, y1))
        full_steps.append(mean_step(0, h))
    return {"max_step": max(steps) if steps else 99.0, "steps": steps,
            "full_max": max(full_steps) if full_steps else 99.0, "full_steps": full_steps,
            "n": len(frames)}


def asr_check(spoken: str, vo: Path, mix: Path) -> dict:
    """small.en on the VO stem and the first 3 s of the mix. Word for word, or not OK."""
    stem = whisper_words(vo)
    head = WORK / "mix_first3.wav"
    ff("-i", str(mix), "-t", "3", "-c:a", "pcm_s16le", str(head))
    opening = whisper_words(head)
    want = norm_tokens(spoken)
    got = norm_tokens(stem["text"])
    notes = []
    # small.en hears the clipped "a" as "the". The ruling allows a/the, and not "with a".
    # "too" comes back as "to". Same sound, not a cut error.
    folded = list(got)
    if want and folded and want[0] == "a" and folded[0] == "the":
        folded[0] = "a"
    for i, tok in enumerate(folded):
        if tok == "to" and i < len(want) and want[i] == "too":
            folded[i] = "too"
    if folded != want:
        notes.append(f"stem {stem['text']!r}")
    open_got = norm_tokens(opening["text"])
    # The first 3 s must carry the hook and Boil, and must not be "with a" or "oil".
    if open_got[:1] == ["with"] or "with" in open_got[:3]:
        notes.append(f"opening hears with: {opening['text']!r}")
    if "oil" in open_got and "boil" not in open_got:
        notes.append(f"opening hears oil: {opening['text']!r}")
    if "boil" not in open_got:
        notes.append(f"opening missed boil: {opening['text']!r}")
    if open_got[:1] not in (["a"], ["the"]):
        notes.append(f"opening is not a/the flask: {opening['text']!r}")
    joined = " ".join(got)
    if "drift but dust" not in joined:
        notes.append("stem missed drift but dust")
    QA.mkdir(parents=True, exist_ok=True)
    payload = {"model": "small.en", "spoken": spoken, "stem": stem, "mix_first_3s": opening,
               "ok": not notes, "notes": notes}
    (QA / f"asr_{SID}_{VER}.json").write_text(json.dumps(payload, indent=2) + "\n")
    (QA / f"asr_{SID}_{VER}.txt").write_text(
        f"spoken: {spoken}\nstem: {stem['text']}\nmix_first_3s: {opening['text']}\n"
        + ("\n".join(notes) if notes else "OK\n"))
    return payload


def build(vo_only: bool = False) -> dict:
    if WORK.exists():
        shutil.rmtree(WORK)
    WORK.mkdir(parents=True)
    QA.mkdir(parents=True, exist_ok=True)
    vo, words, span_meta, vo_info = lifted_vo(WORK)
    spoken = " ".join(w for w, _, _ in words)
    (WORK / "spoken.txt").write_text(spoken + "\n")
    vo_s = probe(vo)
    last_end_preview = words[-1][2]
    pad = max(0.0, vo_s - last_end_preview)
    # Audio tail from the last word to EOF stays at or under 1.0 s, on a frame boundary.
    room = 1.0 - pad
    if room < 0.40:
        raise SystemExit(f"no room for the loop, pad {pad:.3f}")
    max_total = last_end_preview + 1.0
    n_frames = int(math.floor(max_total * FPS + 1e-4))
    total = round(n_frames / FPS, 3)
    if total + 1e-3 < vo_s:
        raise SystemExit(f"tail snap {total} shorter than vo {vo_s}")
    loop_s = round(total - vo_s, 3)
    if total - last_end_preview > 1.0 + 1e-3:
        raise SystemExit(f"tail {total - last_end_preview:.3f}s over 1.0")
    if not 18.0 <= total <= 24.05:
        raise SystemExit(f"duration {total}s outside 18–24 s (vo {vo_s:.2f}) info={vo_info}")
    flask_t = next(s for w, s, e in words if w.lower().startswith("flask"))
    clear_t = next(s for w, s, e in words if w.lower().startswith("clear"))
    stays_t = next(s for w, s, e in words if w.lower().startswith("stays"))
    if flask_t > 1.50 or clear_t > 1.50:
        raise SystemExit(f"claim late: flask {flask_t} clear {clear_t}")
    if words[0][1] > 0.15:
        raise SystemExit(f"first word at {words[0][1]}")
    if vo_info["max_gap_s"] > 0.205:
        print("PIECES", json.dumps(vo_info["pieces"], indent=2))
        print("WORDS", [(w, round(s, 3), round(e, 3)) for w, s, e in words])
        raise SystemExit(f"gap {vo_info['max_gap_s']}s > 0.20: {vo_info['gaps']}")
    if abs(vo_info["hook_minus_boil_db"]) > 1.0:
        raise SystemExit(f"hook level {vo_info}")
    if " but " not in f" {spoken} ":
        raise SystemExit(f"spoken dropped but: {spoken}")
    check_pieces(vo_info["pieces"])
    life_t = [s for w, s, e in words if w.lower().startswith("life")][-1]
    if life_t / total < 0.70:
        raise SystemExit(f"payoff {life_t / total:.3f} under 70% (life {life_t:.2f}, total {total})")
    for h in vo_info.get("heard_gaps") or []:
        if h["kind"] == "sentence" and not (0.119 <= h["gap_s"] <= 0.181):
            raise SystemExit(f"sentence gap {h}")
        if h["gap_s"] > 0.201:
            raise SystemExit(f"join gap {h}")
    print(json.dumps({"vo_s": round(vo_s, 3), "loop_s": loop_s, "total": total, "life_s": life_t,
                      "payoff": round(life_t / total, 3), "spoken": spoken, **vo_info,
                      "words": [{"w": w, "s": s, "e": e} for w, s, e in words]}, indent=2))
    if vo_only:
        return {"vo_only": True, "duration_s": total, "brief": {"payoff_frac": life_t / total, "loop_diff": 0}}

    cuts = body_cuts(words, vo_s, loop_s)
    # Frame counts have to add up. A short concat plus -frames:v clones the last
    # frame, which is the v05 one-frame flick in another shape.
    counted = []
    for t0, t1, src, ins, x, label in cuts:
        n = max(1, int(round(t1 * FPS)) - int(round(t0 * FPS)))
        counted.append([t0, t1, src, ins, x, label, n])
    target_n = int(round(total * FPS))
    delta = target_n - sum(row[6] for row in counted)
    counted[-1][6] += delta
    if counted[-1][6] < 2:
        raise SystemExit(f"loop frames {counted[-1][6]}")
    loop_n = counted[-1][6]
    # trim+fps lands one frame early, so start one frame later. The last frame
    # is then the plate frame before 1.80 s, not a copy of frame 0.
    counted[-1][3] = round(FLASK_IN - loop_n / FPS + (1 / FPS), 6)
    n_frames = sum(row[6] for row in counted)
    total = round(n_frames / FPS, 3)
    if not 18.0 <= total <= 24.05:
        raise SystemExit(f"snapped duration {total}")
    segs = []
    plan = []
    cursor = 0
    for t0, t1, src, ins, x, label, n in counted:
        out = WORK / f"seg_{len(segs):02d}.mp4"
        seg(src, out, ins, n, x)
        segs.append(out)
        t_out0 = cursor / FPS
        cursor += n
        plan.append({"t0": round(t_out0, 3), "t1": round(cursor / FPS, 3), "plate": str(src),
                     "in_s": round(ins, 4), "crop_x": x, "label": label, "hold_s": round(n / FPS, 3)})
    if cursor != n_frames:
        raise SystemExit(f"frame count {cursor} != {n_frames}")
    (WORK / "pic.txt").write_text("".join(f"file '{s.name}'\n" for s in segs))
    pic = WORK / "picture.mp4"
    ff("-f", "concat", "-safe", "0", "-i", "pic.txt", "-c:v", "libx264", "-pix_fmt", "yuv420p",
       "-preset", "fast", "-crf", "16", "-r", str(FPS), "-frames:v", str(n_frames), str(pic), cwd=WORK)
    # The loop span itself runs up to the frame before 1.80 s. No pasted last frame.

    sound = synth_and_gates(vo, total)
    audio = sound["audio"]
    norm = WORK / "audio_norm.wav"
    loudnorm_to(audio, norm)
    asr = asr_check(spoken, vo, norm)
    fragments = fragment_asr(vo, span_meta, words)
    asr["fragments"] = {"ok": fragments["ok"], "notes": fragments["notes"]}
    (QA / f"asr_{SID}_{VER}_fragments.json").write_text(json.dumps(fragments, indent=2) + "\n")
    (QA / f"asr_{SID}_{VER}_fragments.txt").write_text(
        "\n".join(
            f"{'OK' if row['ok'] else 'FAIL'} {row['kind']} {row['i']}: {row['text']}  ||  {row['want']}"
            for row in fragments["table"]
        ) + ("\n" + "\n".join(fragments["notes"]) if fragments["notes"] else "\n")
    )

    chunks = caption_chunks(words)
    overlays = []
    hook_png = WORK / "cap_hook.png"
    hook_meta = render_hook(hook_png)
    overlays.append((hook_png, 0.0, 2.0))
    for i, c in enumerate(chunks):
        png = WORK / f"cap_{i:03d}.png"
        render_text(png, c["text"], 52, 330, anchor="bottom")
        overlays.append((png, c["t0"], min(c["t1"], total - 0.05)))
    title_png = WORK / "cap_title.png"
    render_text(title_png, TITLE, 58, 250, index=2, stroke=4)
    shade = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    for yy in range(560):
        a = int(140 * 0.5 * (1 + math.cos(math.pi * yy / 560)))
        ImageDraw.Draw(shade).line([(0, yy), (W, yy)], fill=(0, 0, 0, a))
    Image.alpha_composite(shade, Image.open(title_png)).save(title_png)
    title_out = min(14.0, round(life_t - 0.12, 3))
    overlays.append((title_png, TITLE_IN, min(title_out, total - 0.2)))
    card_png = WORK / "card_who.png"
    render_card(card_png)

    inputs = ["-i", str(pic), "-i", str(norm)]
    for png, *_ in overlays:
        inputs += ["-loop", "1", "-i", str(png)]
    ci = 2 + len(overlays)
    inputs += ["-loop", "1", "-t", f"{total:.3f}", "-i", str(card_png)]
    fc = [f"[{ci}:v]format=rgba,fade=t=in:st={CARD_IN}:d={CARD_FADE}:alpha=1,"
          f"fade=t=out:st={CARD_OUT - CARD_FADE}:d={CARD_FADE}:alpha=1[card]",
          f"[0:v][card]overlay=0:0:enable='gte(t,{CARD_IN:.3f})*lt(t,{CARD_OUT:.3f})'[vc]"]
    last = "[vc]"
    for i, (_, t0, t1) in enumerate(overlays, 2):
        fc.append(f"{last}[{i}:v]overlay=0:0:enable='gte(t,{t0:.3f})*lt(t,{t1:.3f})'[v{i}]")
        last = f"[v{i}]"
    mp4 = HERE / f"hos_001_{SID}_{VER}.mp4"
    ff(*inputs, "-filter_complex", ";".join(fc), "-map", last, "-map", "1:a",
       "-c:v", "libx264", "-pix_fmt", "yuv420p", "-profile:v", "high", "-preset", "medium", "-crf", "18",
       "-r", str(FPS), "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2",
       "-frames:v", str(n_frames), "-t", f"{total:.3f}", "-movflags", "+faststart", str(mp4))

    lufs = integrated_lufs(mp4)
    peak = true_peak(mp4)
    diff, diff_whole = loop_diff(mp4)
    steps = tail_steps(mp4)
    holds = [r["hold_s"] for r in plan if r["label"] != "loop"]
    payoff = life_t
    last_end = words[-1][2]
    tail_gap = round(total - last_end, 3)
    brief = {
        "frame0_source": f"{PLATE}/01_question_mark_flask_v17.mp4",
        "frame0_zoom": "none — moving plate, in 1.80s, crop x=720, no Ken Burns",
        "first_word_s": words[0][1],
        "surprise_s": {"flask": flask_t, "stays": stays_t, "clear": clear_t},
        "first_cut_s": plan[1]["t0"],
        "last_word_to_loop_s": tail_gap,
        "meta_promise": False,
        "runtime_s": round(probe(mp4), 3),
        "longest_hold_s": max(holds),
        "payoff_phrase": "life blooms into cloudiness",
        "payoff_s": payoff,
        "payoff_frac": round(payoff / total, 3),
        "payoff_vs_70pct": round(payoff / total - 0.70, 3),
        "loop_sentence": "Keep the swan neck intact. A flask stays clear.",
        "loop_diff": diff,
        "loop_diff_masked": diff,
        "loop_diff_whole": diff_whole,
        "tail_step": steps["max_step"],
        "tail_steps": steps["steps"],
        "lufs": lufs,
        "measured_lufs": lufs,
        "true_peak_dbfs": peak,
        "frame0_black": black_frac(mp4, 0.2),
        "max_inter_sentence_gap_s": vo_info["max_gap_s"],
        "hook_level": vo_info,
        "title_out_s": title_out,
        "loop_s": loop_s,
    }
    meta = {
        "id": SID, "version": VER, "job": JOB, "youtube_id": YT_ID,
        "title": "What Is the Pasteur Swan Neck Flask Experiment?",
        "air_date": AIR, "spoken": spoken, "script": spoken,
        "words": [{"word": w, "start": s, "end": e} for w, s, e in words],
        "word_count": len(words), "vo_s": round(vo_s, 3), "last_word_end_s": last_end,
        "pieces": vo_info["pieces"], "captions": chunks,
        "asr": {"ok": asr["ok"], "notes": asr["notes"], "stem": asr["stem"]["text"],
                "mix_first_3s": asr["mix_first_3s"]["text"],
                "fragments_ok": fragments["ok"], "fragment_notes": fragments["notes"]},
        "spans": span_meta, "plan": [{**r, "plate": Path(r["plate"]).name} for r in plan],
        "hook": HOOK.replace("**", ""), "hook_layer": hook_meta,
        "who_card": {"name": CARD[0], "line2": CARD[1], "in_s": CARD_IN, "out_s": CARD_OUT},
        "title_on_screen": TITLE, "no_cta": True, "no_new_spend": True,
        "bed": sound["bed"].name, "sfx_level": sound["level"],
        **brief,
    }
    meta_path = HERE / f"hos_001_{SID}_{VER}_meta.json"
    meta_path.write_text(json.dumps(meta, indent=2) + "\n")
    (HERE / f"SHORT_{SID}_{VER}.json").write_text(json.dumps(meta, indent=2) + "\n")

    gate = subprocess.run([sys.executable, str(REPO / "00_Brand/Channel-Setup/tools/gate_shorts_open.py"),
                           "check", str(mp4), "--air-date", AIR, "--id", YT_ID,
                           "--script", str(WORK / "spoken.txt"), "--vo", str(vo),
                           "--meta", str(meta_path), "--json"],
                          capture_output=True, text=True)
    (QA / f"gate_{SID}_{VER}.txt").write_text((gate.stdout + gate.stderr).strip() + "\n")
    try:
        gate_json = json.loads(gate.stdout)
        if isinstance(gate_json, list):
            gate_json = gate_json[0]
    except json.JSONDecodeError:
        gate_json = {"verdict": "FAIL", "raw": gate.stdout[-1500:], "err": gate.stderr[-800:]}
    (QA / f"gate_{SID}_{VER}.json").write_text(json.dumps(gate_json, indent=2) + "\n")
    j0918 = (
        "J0918 HOS ship gate (Chief, 24 Oct 2026). Text from gate_shorts_open.py, "
        "missing on the v04 and v05 packs:\n"
        "(a) FAIL a pushed still at frame 0 when the 0-1.5 s centre-band frame diff is under 1.50.\n"
        "(b) FAIL when the first cut comes after 3.0 s.\n"
        "(c) WARN when the first VO word starts after 0.15 s.\n"
        "(d) WARN when the gap from the last word to the end of the file is over 1.5 s.\n"
        "(e) FAIL if the script or the spoken line contains a meta-promise "
        "(stay and I'll show you, did you know, wait for it).\n"
        f"measured frame0_diff_0_1_5s={gate_json.get('frame0_diff_0_1_5s')} "
        f"first_cut_s={gate_json.get('first_cut_s')} "
        f"vo_onset_s={gate_json.get('vo_onset_s')} "
        f"tail_gap_s={gate_json.get('tail_gap_s')} "
        f"stayed_fails={gate_json.get('stayed_fails')}\n"
    )
    (QA / f"j0918_ship_gate_{SID}_{VER}.txt").write_text(j0918)

    qa = run_qa(mp4, plan)
    music = subprocess.run([sys.executable, str(OWB / "scripts/music_gate.py"), str(PROJ),
                            "--bed", str(sound["bed"]), "--video", str(mp4),
                            "--out", str(QA / f"music_gate_{SID}_{VER}.json")],
                           capture_output=True, text=True)
    (QA / f"music_gate_{SID}_{VER}.txt").write_text((music.stdout + music.stderr).strip() + "\n")

    phone = HERE / f"hos_001_{SID}_{VER}_PHONE.mp4"
    ff("-i", str(mp4), "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "fast", "-crf", "26",
       "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart", str(phone))
    sheet = sheet_2fps(mp4)
    copies = copy_out(mp4, phone, sheet)

    summary = {
        "file": mp4.name, "sha256": sha256(mp4), "duration_s": brief["runtime_s"],
        "spoken": spoken, "brief": brief, "gate_exit": gate.returncode,
        "gate_verdict": gate_json.get("verdict"), "gate_fails": gate_json.get("fails"),
        "gate_warns": gate_json.get("warns"), "qa": qa,
        "music_exit": music.returncode, "music_tail": (music.stdout + music.stderr).strip().splitlines()[-4:],
        "sfx": sound["level"], "copies": copies, "phone": phone.name,
        "asr_ok": asr["ok"] and fragments["ok"], "asr_notes": asr["notes"] + fragments["notes"],
    }
    (QA / f"build_{SID}_{VER}.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps({k: summary[k] for k in ("file", "duration_s", "gate_verdict", "gate_fails", "gate_warns",
                                              "qa", "music_exit", "music_tail", "sfx", "brief")}, indent=2))
    return summary


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--vo-only", action="store_true")
    args = ap.parse_args()
    rec = build(vo_only=args.vo_only)
    if args.vo_only:
        return
    bad = []
    if rec["gate_verdict"] != "PASS":
        bad.append("gate")
    if rec["qa"]["polish_gate"]["exit"] != 0:
        bad.append("polish")
    if rec["qa"]["picture_qa"]["exit"] != 0:
        bad.append("picture")
    if rec["music_exit"] != 0:
        bad.append("music")
    if rec["sfx"]["exit"] != 0:
        bad.append("sfx")
    if rec["brief"]["loop_diff"] > 5:
        bad.append(f"loop_diff {rec['brief']['loop_diff']}")
    if rec["brief"]["loop_diff"] < 0.3:
        bad.append(f"loop looks like a frame-0 copy ({rec['brief']['loop_diff']})")
    if rec["brief"].get("tail_step", 99) > 3:
        bad.append(f"tail step {rec['brief'].get('tail_step')}")
    if rec["brief"].get("longest_hold_s", 99) > 3.0:
        bad.append(f"hold {rec['brief'].get('longest_hold_s')}")
    if not rec.get("asr_ok"):
        bad.append("asr " + "; ".join(rec.get("asr_notes") or ["missing"]))
    if rec["brief"]["payoff_frac"] < 0.70:
        bad.append(f"payoff {rec['brief']['payoff_frac']}")
    if not -14.5 <= rec["brief"]["lufs"] <= -13.5:
        bad.append(f"lufs {rec['brief']['lufs']}")
    if rec["brief"]["true_peak_dbfs"] > -1.0:
        bad.append(f"tp {rec['brief']['true_peak_dbfs']}")
    if bad:
        raise SystemExit("NOT PASS: " + ", ".join(bad))
    print("PASS", rec["file"], rec["duration_s"], "s")


if __name__ == "__main__":
    main()
