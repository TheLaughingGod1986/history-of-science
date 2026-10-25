#!/usr/bin/env python3
"""HOS 001 Short s11 v04 (J0939, £0 local re-cut of 1-BZaFIMwYU).

v03 left ~5 s of digital silence because the ElevenLabs alignment folds the
pre-word breath into each first word. v04 trims every span to the RMS speech
onset in part04_proof_in_a_flask_v01.wav, keeps sentence gaps at 0.12–0.18 s
and comma pauses at or under 0.20 s, and swaps the glued "emptiness" line for
"then disease can be a passenger too." No new TTS, Veo, Flow or Vertex.

    python3 _build_short_s11_curved_flask_v04.py
    python3 _build_short_s11_curved_flask_v04.py --vo-only
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
SID, VER, JOB = "s11_curved_flask", "v04", "J0939"
AIR = "2026-10-27"
YT_ID = "1-BZaFIMwYU"
WORK = Path("/private/tmp/j0939-flask-v04")
QA = HERE / f"qa_{SID}_{VER}"
W, H, FPS = 1080, 1920, 30
LOOP_S = 1.0
XFADE = 0.025
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
# Source spans trimmed to measured speech (RMS), not the alignment breath.
# gap is room tone inserted after the piece. kind is sentence | comma | word | end.
PIECES = [
    (4.08, 4.68, 0.18, "word", ["a", "flask"]),
    (16.22, 17.10, 0.18, "sentence", ["stays", "clear"]),
    (7.32, 8.08, 0.18, "sentence", ["boil", "broth"]),
    (11.05, 11.98, 0.20, "comma", ["air", "can", "drift"]),
    (12.40, 15.05, 0.18, "sentence", ["dust", "and", "microbes", "settle", "in", "the", "curve"]),
    (37.98, 40.92, 0.20, "comma", ["if", "life", "arrives", "as", "passengers", "from", "the", "outside"]),
    (41.38, 43.52, 0.18, "sentence", ["then", "disease", "can", "be", "a", "passenger", "too"]),
    (17.88, 18.58, 0.20, "comma", ["break", "the", "neck"]),
    (19.02, 19.98, 0.20, "comma", ["or", "tip", "the", "trap"]),
    (20.45, 22.68, 0.18, "sentence", ["and", "life", "blooms", "into", "cloudiness"]),
    (8.85, 10.35, 0.0, "end", ["keep", "the", "swan", "neck", "intact"]),
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
    """Speech-trimmed pieces, room-tone gaps, 25 ms crossfades.

    Internal silences over 0.15 s are cut and replaced with a 0.15 s room gap.
    Sentence gaps are 0.17 s and comma gaps are 0.19 s, both on the room tone.
    Word times are RMS onsets on the source, mapped onto the stem.
    """
    src_words = words_in_align()
    used = [False] * len(src_words)
    # Expand pieces so a long internal pause cannot survive into the stem.
    expanded = []
    for a, b, gap, kind, tokens in PIECES:
        parts = tighten_span(a, b, 0.08)
        for n, (pa, pb) in enumerate(parts):
            if pb - pa < 0.04:
                continue
            if n < len(parts) - 1:
                expanded.append((pa, pb, 0.16, "word", tokens if n == 0 else []))
            else:
                expanded.append((pa, pb, gap, kind, tokens if n == 0 else []))
        if len(parts) > 1:
            # tokens after the first subspan still need a home: the subspan that holds them
            pass
    # Re-home tokens onto the subspan that contains the alignment word.
    housed = [(pa, pb, gap, kind, []) for pa, pb, gap, kind, _tok in expanded]
    token_home = []
    for a, b, _gap, _kind, tokens in PIECES:
        for tok in tokens:
            hit = None
            for k, (w, s, e) in enumerate(src_words):
                if used[k]:
                    continue
                if w.lower().strip(".,;:").startswith(tok) and a - 0.40 <= (s + e) / 2 <= b + 0.30:
                    hit = k
                    break
            if hit is None:
                if tok == "but":
                    continue
                raise SystemExit(f"missing word {tok!r} in {a:.2f}-{b:.2f}")
            used[hit] = True
            w, s, e = src_words[hit]
            mid = (s + e) / 2
            best = min(range(len(expanded)), key=lambda i: 0 if expanded[i][0] <= mid <= expanded[i][1]
                       else min(abs(mid - expanded[i][0]), abs(mid - expanded[i][1])))
            # only consider subspans that came from this piece (source inside [a-0.05, b+0.05])
            cands = [i for i, (pa, pb, *_) in enumerate(expanded) if a - 0.05 <= pa and pb <= b + 0.05]
            if not cands:
                raise SystemExit(f"no subspan for {tok}")
            best = min(cands, key=lambda i: 0 if expanded[i][0] <= mid <= expanded[i][1]
                       else min(abs(mid - expanded[i][0]), abs(mid - expanded[i][1])))
            token_home.append((best, w, s, e))
    by_span = {}
    for idx, w, s, e in token_home:
        by_span.setdefault(idx, []).append((w, s, e))

    opener = slice_stereo(expanded[0][0], expanded[0][1])
    if len(expanded) > 1 and expanded[1][0] < 20:
        opener.extend(slice_stereo(expanded[1][0], expanded[1][1]))
    boil_i = next(i for i, (_a, _b, _g, _k, _t) in enumerate(expanded) if abs(_a - PIECES[2][0]) < 1.5 or (_a >= 7.2 and _a <= 8.2))
    # boil is the piece whose source sits near 7.3
    boil_i = next(i for i, (pa, pb, *_) in enumerate(expanded) if pa >= 7.0 and pb <= 8.3)
    boil = slice_stereo(expanded[boil_i][0], expanded[boil_i][1])
    hook_db = speech_rms_db(opener)
    boil_db = speech_rms_db(boil)
    opener_gain = max(-3.0, min(6.0, boil_db - hook_db + 1.0))

    nxf = int(XFADE * SR)
    out = array.array("h")
    cursor = 0.0
    subs = []
    span_meta = []
    for i, (pa, pb, gap, kind, _tok) in enumerate(expanded):
        piece = slice_stereo(pa, pb)
        gain_db = opener_gain if pa < 18 and pb < 18 and pa < 5 else 0.0
        # opener is the flask piece (source ~4 s) and the stays piece (source ~16 s)
        if (4.0 <= pa <= 5.0) or (16.0 <= pa <= 17.2):
            piece = apply_gain(piece, opener_gain)
            gain_db = opener_gain
        else:
            gain_db = 0.0
        if i == 0:
            out.extend(piece)
            out_t = 0.0
        else:
            out_t = cursor - XFADE
            out = xfade(out, piece, nxf)
        cursor = len(out) / 2 / SR
        subs.append((pa, pb, out_t, gain_db))
        words_here = " ".join(w for w, _, _ in by_span.get(i, []))
        span_meta.append({
            "i": i, "src": [pa, pb], "out": round(out_t, 3),
            "dur": round(pb - pa, 3), "gap_after": gap, "gap_kind": kind,
            "gain_db": round(gain_db, 2), "words": words_here,
            "measured": "rms onset/offset on the source, mapped onto the stem",
        })
        if gap > 0:
            room = room_tone(int((gap + XFADE) * SR))
            out = xfade(out, room, nxf)
            cursor = len(out) / 2 / SR

    mapped = []
    for i, items in by_span.items():
        prev = expanded[i][0]
        for n, (w, s, e) in enumerate(items):
            # next word's alignment start, so this word cannot swallow it
            nxt_s = items[n + 1][1] if n + 1 < len(items) else expanded[i][1]
            search_a = max(expanded[i][0], min(s, prev) - 0.02)
            search_b = min(expanded[i][1], max(e, s) + 0.16, nxt_s + 0.04)
            if search_b <= search_a + 0.03:
                search_b = search_a + 0.06
            onset, offset = measure_bounds(search_a, search_b)
            onset = max(onset, expanded[i][0])
            offset = min(max(offset, onset + 0.04), expanded[i][1])
            if n + 1 < len(items):
                offset = min(offset, nxt_s)
            prev = offset
            mapped.append((w, round(map_src(subs, onset), 3), round(map_src(subs, offset), 3)))
    mapped.sort(key=lambda r: r[1])

    speech = work / f"hos_001_{SID}_vo_{VER}.wav"
    write_wav(speech, out)
    boil_out = subs[boil_i][2]
    boil_end = boil_out + (expanded[boil_i][1] - expanded[boil_i][0])
    hook_s = slice_stereo_from(out, 0.0, 1.45)
    boil_s = slice_stereo_from(out, boil_out, min(boil_end, boil_out + 1.2))
    hook_db2 = speech_rms_db(hook_s)
    boil_db2 = speech_rms_db(boil_s)
    gaps = max_gaps(out)
    worst = max((g["dur"] for g in gaps), default=0.0)
    info = {
        "opener_gain_db": round(opener_gain, 2),
        "hook_speech_db": round(hook_db2, 2),
        "boil_speech_db": round(boil_db2, 2),
        "hook_minus_boil_db": round(hook_db2 - boil_db2, 2),
        "gaps": gaps,
        "max_gap_s": round(worst, 3),
        "subs": len(subs),
    }
    return speech, mapped, span_meta, info


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


def seg(src: Path, dst: Path, start: float, dur: float, x: int) -> None:
    if start < 0:
        raise SystemExit(f"{src.name}: negative in-point {start}")
    if start + dur > probe(src) - 0.04:
        raise SystemExit(f"{src.name}: in {start} + {dur:.2f} runs past the plate ({probe(src):.2f})")
    vf = (f"trim=start={start:.4f}:duration={dur:.4f},setpts=PTS-STARTPTS,"
          f"scale=1920:1080,crop=608:1080:{x}:0,scale={W}:{H}:flags=lanczos,fps={FPS},setsar=1")
    ff("-i", str(src), "-filter_complex", vf, "-an", "-c:v", "libx264", "-pix_fmt", "yuv420p",
       "-preset", "fast", "-crf", "16", "-r", str(FPS), str(dst))


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
        if d > 3.01:
            raise SystemExit(f"{label} hold {d:.2f}s over 3.0s ({t0:.2f}-{t1:.2f})")
        out.append((round(t0, 3), round(t1, 3), src, ins, x, label))
    n_loop = max(2, round(loop_s * FPS))
    loop_in = FLASK_IN - (n_loop - 1) / FPS
    if loop_in < 0:
        raise SystemExit(f"loop in-point {loop_in}")
    out.append((round(vo_s, 3), round(vo_s + loop_s, 3), flask, loop_in, FLASK_CROP, "loop"))
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
            differ = abs(r - r2) + abs(g - g2) + abs(bl - b2) > 80
            if differ and (cream or ink):
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
        "source": "own synthesis in _build_short_s11_curved_flask_v04.py, 0 credits",
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
    loop_s = round(min(1.0, max(0.85, 1.0 - pad)), 3)
    total = round(vo_s + loop_s, 3)
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
        print("WORDS", [(w, s, e) for w, s, e in words])
        raise SystemExit(f"gap {vo_info['max_gap_s']}s > 0.20: {vo_info['gaps']}")
    if abs(vo_info["hook_minus_boil_db"]) > 1.05:
        raise SystemExit(f"hook level {vo_info}")
    life_t = [s for w, s, e in words if w.lower().startswith("life")][-1]
    if life_t / total < 0.70:
        raise SystemExit(f"payoff {life_t / total:.3f} under 70% (life {life_t:.2f}, total {total})")
    print(json.dumps({"vo_s": round(vo_s, 3), "loop_s": loop_s, "total": total, "life_s": life_t,
                      "payoff": round(life_t / total, 3), "spoken": spoken, **vo_info,
                      "words": [{"w": w, "s": s, "e": e} for w, s, e in words]}, indent=2))
    if vo_only:
        return {"vo_only": True, "duration_s": total, "brief": {"payoff_frac": life_t / total, "loop_diff": 0}}

    cuts = body_cuts(words, vo_s, loop_s)
    segs = []
    plan = []
    for k, (t0, t1, src, ins, x, label) in enumerate(cuts):
        d = t1 - t0
        if d > 4.01:
            raise SystemExit(f"{label} hold {d:.2f}s")
        if k == 1 and t0 > 2.60:
            raise SystemExit(f"first cut {t0}")
        out = WORK / f"seg_{k:02d}.mp4"
        seg(src, out, ins, d, x)
        segs.append(out)
        plan.append({"t0": t0, "t1": round(t1, 3), "plate": str(src), "in_s": round(ins, 4),
                     "crop_x": x, "label": label, "hold_s": round(d, 3)})
    (WORK / "pic.txt").write_text("".join(f"file '{s.name}'\n" for s in segs))
    pic = WORK / "picture.mp4"
    ff("-f", "concat", "-safe", "0", "-i", "pic.txt", "-c:v", "libx264", "-pix_fmt", "yuv420p",
       "-preset", "fast", "-crf", "16", "-r", str(FPS), "-t", f"{total:.3f}", str(pic), cwd=WORK)
    force_last_frame(pic, total)

    sound = synth_and_gates(vo, total)
    audio = sound["audio"]
    norm = WORK / "audio_norm.wav"
    loudnorm_to(audio, norm)

    chunks = chunk_words(words)
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
       "-t", f"{total:.3f}", "-movflags", "+faststart", str(mp4))

    lufs = integrated_lufs(mp4)
    peak = true_peak(mp4)
    diff, diff_whole = loop_diff(mp4)
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
    if rec["brief"]["loop_diff"] > 15:
        bad.append(f"loop_diff {rec['brief']['loop_diff']}")
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
