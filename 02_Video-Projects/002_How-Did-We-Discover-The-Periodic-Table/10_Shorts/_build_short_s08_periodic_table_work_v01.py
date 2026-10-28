#!/usr/bin/env python3
"""HOS 002 Short s08 v01 (test B, search-titled): a stretch lifted from the long's own Part 05 (J0563).

No new VO or picture spend. VO: 02_Voiceover/part05_the_guests_arrive_v01.wav, lift:
"But the table is not finished. It never was, in 1869. Noble gases crash the party,
colourless, almost aloof, a whole family nobody had a column for. The map stretches.
A new street appears. Then a sharper ruler. Atomic number. X-ray fingerprints.
Mass was the first coordinate. The deeper coordinate is how many protons sit in the nucleus.
A photon can read the difference."
(64 words, lifting 42.30–63.65 s and 74.00–83.48 s from Part 05, so there is zero overlap
with S1–S5 (P04 + 42..120 s, P05 + 5.00..26.20 s, P05 + 122.40..143.40 s), s06_atomic_weights (Part 03),
s07_mendeleev_cards (Part 04 0..41 s), Newlands (Part 02), or the Part 01 four-elements Short,
and the Short stays inside 22–27 s and 55–65 words).
Plates: the long's Part 05, Part 01, and Part 03 KEEP takes (01b_empty_seats_waiting_v01_try1,
02_guests_as_work_v01_try3, 10_zoo_became_city_v01_try4, 11b_late_for_dinner_v01_try2,
08b_weight_vs_identity_v01_try1, P1:10_rock_not_fire_v01, P3:08_property_waves_v08).
Bed: own-synthesis warm harmonic pad at −20 dB under VO (0 credits; distinct G-lydian/Em9 voicing).
Hook on frame 0, word captions, one person/date card (DMITRI MENDELEEV · First table, 1869, from the
long's Part 05 VO), the long's exact title at 9–14 s, the last 3.0 s on the opening plate so
it loops. Then caption check, gate_shorts_open, vo_check, freezedetect, polish_gate, picture_qa, stills,
iCloud copy. Never uploads.

    python3 _build_short_s08_periodic_table_work_v01.py [--air-date YYYY-MM-DD] [--no-icloud]
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
import hashlib  # noqa: E402
import json  # noqa: E402
import math  # noqa: E402
import re  # noqa: E402
import shutil  # noqa: E402
import struct  # noqa: E402
import subprocess  # noqa: E402
import wave  # noqa: E402

from PIL import Image, ImageDraw, ImageFont  # noqa: E402

HERE = Path(__file__).resolve().parent
PROJ = HERE.parent
REPO = PROJ.parents[1]
NAS_PROJ = Path("/Volumes/data/mac-mini-archive/YouTube/History Of Science/"
                "02_Video-Projects/002_How-Did-We-Discover-The-Periodic-Table")
OWB_REPO = Path("/Users/benjaminoats/YouTube/orbit-with-ben")
SID = "s08_periodic_table_work"
VER = "v01"
JOB = "J0563"
WORK = HERE / f"_work_{SID}_{VER}"
QA_DIR = HERE / f"qa_{SID}_{VER}"


def resolve_media(rel: str) -> Path:
    local = PROJ / rel
    if local.exists():
        return local
    alt = NAS_PROJ / rel
    if alt.exists():
        return alt
    return local


RAW_VO = resolve_media("02_Voiceover/part05_the_guests_arrive_v01.wav")
# Part 05 word-level timestamps (verified against align.json and faster-whisper) for the 2 lifted windows:
# Win 1 (42.30..63.65): "But the table is not finished. It never was, in 1869. Noble gases crash the party,
#   colourless, almost aloof, a whole family nobody had a column for. The map stretches. A new street appears.
#   Then a sharper ruler. Atomic number. X-ray fingerprints." (42 words)
# Win 2 (74.00..83.48): "Mass was the first coordinate. The deeper coordinate is how many protons sit in the
#   nucleus. A photon can read the difference." (22 words)
SPAN_WINDOWS = [
    (42.30, 63.65),
    (74.00, 83.48),
]
RAW_WORDS: list[tuple[str, float, float]] = [
    ("But", 42.36, 43.20),          # 0
    ("the", 43.22, 43.28),          # 1
    ("table", 43.35, 43.68),        # 2
    ("is", 43.71, 43.76),           # 3
    ("not", 43.80, 43.92),          # 4
    ("finished.", 43.99, 44.96),    # 5
    ("It", 44.99, 45.04),           # 6
    ("never", 45.07, 45.20),        # 7
    ("was,", 45.32, 45.76),         # 8
    ("in", 45.79, 45.84),           # 9
    ("1869.", 45.88, 47.12),        # 10
    ("Noble", 47.32, 47.92),        # 11
    ("gases", 48.01, 48.48),        # 12
    ("crash", 48.53, 48.80),        # 13
    ("the", 48.84, 48.96),          # 14
    ("party,", 49.05, 49.52),       # 15
    ("colourless,", 50.05, 50.72),  # 16
    ("almost", 50.77, 51.04),       # 17
    ("aloof,", 51.12, 52.00),       # 18
    ("a", 52.04, 52.08),            # 19
    ("whole", 52.12, 52.32),        # 20
    ("family", 52.41, 52.96),       # 21
    ("nobody", 53.03, 53.44),       # 22
    ("had", 53.46, 53.52),          # 23
    ("a", 53.56, 53.60),            # 24
    ("column", 53.66, 54.00),       # 25
    ("for.", 54.08, 54.48),         # 26
    ("The", 54.62, 55.04),          # 27
    ("map", 55.14, 55.44),          # 28
    ("stretches.", 55.53, 56.52),   # 29
    ("A", 56.62, 56.72),            # 30
    ("new", 56.80, 57.04),          # 31
    ("street", 57.11, 57.52),       # 32
    ("appears.", 57.61, 58.32),     # 33
    ("Then", 58.53, 59.04),         # 34
    ("a", 59.20, 59.36),            # 35
    ("sharper", 59.43, 59.92),      # 36
    ("ruler.", 59.99, 60.48),       # 37
    ("Atomic", 60.59, 61.28),       # 38
    ("number.", 61.35, 61.92),      # 39
    ("X-ray", 62.16, 62.64),        # 40
    ("fingerprints.", 62.71, 63.60),  # 41
    ("Mass", 74.06, 74.96),         # 42
    ("was", 75.02, 75.20),          # 43
    ("the", 75.22, 75.28),          # 44
    ("first", 75.33, 75.60),        # 45
    ("coordinate.", 75.67, 76.40),  # 46
    ("The", 76.56, 77.04),          # 47
    ("deeper", 77.10, 77.44),       # 48
    ("coordinate", 77.50, 78.08),   # 49
    ("is", 78.16, 78.32),           # 50
    ("how", 78.38, 78.56),          # 51
    ("many", 78.59, 78.72),         # 52
    ("protons", 78.80, 79.52),      # 53
    ("sit", 79.62, 79.92),          # 54
    ("in", 79.97, 80.08),           # 55
    ("the", 80.10, 80.16),          # 56
    ("nucleus.", 80.25, 81.04),     # 57
    ("A", 81.36, 81.68),            # 58
    ("photon", 81.75, 82.16),       # 59
    ("can", 82.20, 82.32),          # 60
    ("read", 82.37, 82.56),         # 61
    ("the", 82.58, 82.64),          # 62
    ("difference.", 82.70, 83.44),  # 63
]
MAX_PAUSE = 0.18
ATEMPO = 1.06
HOOK = "NOBLE **GASES**"
CARD = ("DMITRI MENDELEEV", "First table, 1869")
CARD_IN, CARD_OUT, CARD_FADE = 2.15, 5.75, 0.35
W, H, FPS = 1080, 1920, 30
BAND_TOP, BAND_H = (H - 608) // 2, 608
CREAM, INK, YEL = (245, 232, 210, 255), (28, 26, 28, 255), (255, 214, 70, 255)
FONT = "/System/Library/Fonts/Supplemental/Didot.ttc"
CTA_FONT = "/System/Library/Fonts/Supplemental/Times New Roman.ttf"
TITLE = "How Did We Discover the Periodic Table?"
TITLE_DRAFT = "How Does the Periodic Table Work?"
TAIL_S = 0.42
LOOP_S = 3.0
TITLE_IN, TITLE_OUT = 9.0, 14.0
CHUNK_MAX_S, CHUNK_MAX_WORDS, CHUNK_MIN_S = 1.55, 5, 0.45
HOOK_CAP = 0.088
HOOK_PITCH = 1.32
UI_TOP = 0.75
GATE = Path(os.environ.get("HOS_GATE", REPO / "00_Brand/Channel-Setup/tools/gate_shorts_open.py"))
VO_CHECK = REPO / "00_Brand/Channel-Setup/tools/vo_check.py"
VO_PY = Path.home() / ".venvs/hos-vo/bin/python"
ICLOUD = Path.home() / ("Library/Mobile Documents/com~apple~CloudDocs/HOS UAT/"
                        "002_How-Did-We-Discover-The-Periodic-Table/10_Shorts")
SCRIPT_TXT = WORK / f"{SID}.txt"


def clip(rel: str) -> Path:
    return resolve_media(f"04_Generated-Clips/{rel}.mp4")


# (index of the word the plate lands on, plate, in-point s, crop x on 1920x1080); "loop" = last LOOP_S s.
# All 7 source clips checked (18 Oct 2026): Part 05 and Part 03 KEEP takes, continuous motion, no Explorer, no garbled text.
BEATS = [
    (0, clip("part05/raw/v01_quality/01b_empty_seats_waiting_v01_try1"), 0.60, 656),   # But the table is not finished. It never was, in 1869.
    (11, clip("part05/raw/v01_quality/02_guests_as_work_v01_try3"), 0.60, 656),        # Noble gases crash the party, colourless, almost aloof,
    (19, clip("part05/raw/v01_quality/10_zoo_became_city_v01_try4"), 1.20, 656),       # a whole family nobody had a column for.
    (27, clip("part05/raw/v01_quality/11b_late_for_dinner_v01_try2"), 0.60, 656),      # The map stretches. A new street appears.
    (34, clip("part05/raw/v01_quality/08b_weight_vs_identity_v01_try1"), 1.20, 1200),  # Then a sharper ruler. Atomic number. X-ray fingerprints.
    (42, clip("part01/raw/v01_fast/10_rock_not_fire_v01"), 0.60, 656),                  # Mass was the first coordinate.
    (47, clip("part03/raw/v08_fast/08_property_waves_v08"), 0.60, 656),                # The deeper coordinate is how many protons sit in the nucleus.
    ("loop", clip("part05/raw/v01_quality/01b_empty_seats_waiting_v01_try1"), 0.60, 656),  # A photon can read the difference.
]


def ff(*a: str, cwd: Path | None = None) -> None:
    subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", *a], check=True, cwd=cwd)


def probe(p: Path) -> float:
    return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                          "-of", "csv=p=0", str(p)], text=True))


def sha256(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def mean_db(p: Path) -> float:
    err = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(p), "-af", "volumedetect", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    return float(re.search(r"mean_volume: (-?[\d.]+)", err).group(1))


def synth_warm_bed(path: Path, dur: float, sr: int = 48000) -> Path:
    """Synthesise a gentle, period-fitting warm harmonic pad (own synthesis, 0 credits, G-lydian / Em9 voicing)."""
    n = int(sr * (dur + 1.0))
    freqs = [164.81, 246.94, 293.66, 369.99, 493.88]  # E3, B3, D4, F#4, B4 warm study pad (distinct from s06/s07)
    amps = [0.37, 0.29, 0.21, 0.14, 0.09]
    frames = bytearray()
    for i in range(n):
        t = i / sr
        env = min(1.0, t / 0.4) * min(1.0, max(0.0, (dur + 0.5 - t) / 0.5))
        l_val = 0.0
        r_val = 0.0
        for k, (f, a) in enumerate(zip(freqs, amps)):
            shimmer = 1.0 + 0.07 * math.sin(2.0 * math.pi * (0.11 + 0.03 * k) * t + k * 0.85)
            s_l = math.sin(2.0 * math.pi * f * t + 0.30 * k) * a * shimmer
            s_r = math.sin(2.0 * math.pi * (f * 1.0008) * t + 0.60 * k) * a * shimmer
            l_val += s_l
            r_val += s_r
        l_sample = int(max(-1.0, min(1.0, l_val * env * 0.24)) * 32767)
        r_sample = int(max(-1.0, min(1.0, r_val * env * 0.24)) * 32767)
        frames += struct.pack("<hh", l_sample, r_sample)
    path.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(path), "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(sr)
        w.writeframes(bytes(frames))
    return path


def chunk_words(words: list[tuple[str, float, float]]) -> list[dict]:
    chunks, i, n = [], 0, len(words)
    while i < n:
        t0 = words[i][1]
        parts, t_end, j = [words[i][0]], words[i][2], i + 1
        while j < n:
            wj, sj, ej = words[j]
            if parts[-1][-1:] in ".?!":
                break
            if parts[-1][-1:] in ",;:" and sj - t0 >= CHUNK_MIN_S and (len(parts) >= 2 or wj[:1].isupper()):
                break
            if len(parts) >= CHUNK_MAX_WORDS and sj - t0 >= CHUNK_MIN_S:
                break
            if ej - t0 >= CHUNK_MAX_S and len(parts) >= 2:
                break
            parts.append(wj)
            t_end = ej
            j += 1
        t1 = words[j][1] if j < n else t_end + 0.25
        chunks.append({"text": " ".join(parts), "t0": round(t0, 3), "t1": round(t1, 3), "n_words": len(parts)})
        i = j
    return chunks


def render(path: Path, text: str, size: int, y: int, *, anchor: str = "top", font_path: str = FONT,
           index: int = 0, fill=CREAM, stroke: int = 3) -> None:
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
            draw.text((x, cy), t, font=font, fill=YEL if hot else fill, stroke_width=stroke, stroke_fill=INK)
            x += font.getlength(t) + space
        cy += lh + gap
    img.save(path)


def render_hook(path: Path, text: str) -> dict:
    tokens = [(w.strip("*"), w.startswith("**")) for w in text.split()]
    target = HOOK_CAP
    while target >= 0.080 - 1e-9:
        size = 60
        while True:
            font = ImageFont.truetype(FONT, size, index=2)
            cap = -font.getbbox("H", anchor="ls")[1]
            if cap >= target * H:
                break
            size += 1
        widest = max(font.getlength(t) for t, _ in tokens)
        if widest <= W - 80:
            break
        target -= 0.002
    else:
        raise SystemExit(f"hook word {widest:.0f} px wider than the frame")
    pitch = round(cap * HOOK_PITCH)
    block = pitch * (len(tokens) - 1) + cap
    top = (H - block) // 2
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    for k, (t, hot) in enumerate(tokens):
        base = top + cap + k * pitch
        draw.text((W / 2, base), t, font=font, anchor="ms", fill=YEL if hot else CREAM, stroke_width=6,
                  stroke_fill=INK)
    img.save(path)
    bottom = top + block
    if bottom > UI_TOP * H:
        raise SystemExit(f"hook block ends at {bottom / H:.1%}, inside the bottom UI")
    return {"font_size": size, "cap_px": cap, "cap_pct": round(100 * cap / H, 2), "lines": len(tokens),
            "block_pct": [round(100 * top / H, 1), round(100 * bottom / H, 1)],
            "widest_pct": round(100 * widest / W, 1)}


def seg(src: Path, dst: Path, start: float, dur: float, x: int) -> None:
    if start + dur > probe(src) - 0.05:
        raise SystemExit(f"{src.name}: in {start} + {dur:.2f} s runs past the plate")
    vf = f"scale=1920:1080,crop=608:1080:{x}:0,scale={W}:{H}:flags=lanczos,setsar=1"
    ff("-ss", f"{start:.3f}", "-i", str(src), "-t", f"{dur:.3f}", "-filter_complex", vf, "-an", "-c:v", "libx264",
       "-pix_fmt", "yuv420p", "-preset", "fast", "-crf", "17", "-r", str(FPS), str(dst))


def lifted_vo(work: Path) -> tuple[Path, list[tuple[str, float, float]]]:
    """Cut the 64-word Part 05 noble-gases + atomic-number stretch, cap silences at MAX_PAUSE, apply ATEMPO."""
    err = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(RAW_VO),
                          "-af", "silencedetect=n=-38dB:d=0.08", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    sils = list(zip([float(x) for x in re.findall(r"silence_start: (-?[\d.]+)", err)],
                    [float(x) for x in re.findall(r"silence_end: ([\d.]+)", err)]))

    def segments_in(win_a: float, win_b: float) -> list[tuple[float, float]]:
        keep, cur = [], win_a
        for a, b in sils:
            if b <= win_a or a >= win_b:
                continue
            a = max(win_a, a)
            b = min(win_b, b)
            if b - a > MAX_PAUSE:
                if a + MAX_PAUSE / 2 - cur >= 0.08:
                    keep.append((cur, a + MAX_PAUSE / 2))
                cur = b - MAX_PAUSE / 2
        if win_b - cur >= 0.08:
            keep.append((cur, win_b))
        return keep

    spans: list[tuple[float, float]] = []
    for wa, wb in SPAN_WINDOWS:
        spans.extend(segments_in(wa, wb))

    remap: list[tuple[float, float, float]] = []
    out_t = 0.0
    for s, e in spans:
        remap.append((s, e, out_t))
        out_t += e - s

    def map_time(t: float) -> float:
        for rs, re_, ot in remap:
            if t <= rs:
                return ot / ATEMPO
            if t <= re_:
                return (ot + (t - rs)) / ATEMPO
        return out_t / ATEMPO

    mapped = [(w, round(map_time(s), 3), round(max(map_time(s) + 0.08, map_time(e)), 3))
              for w, s, e in RAW_WORDS]

    n = len(spans)
    ins = "".join(f"[in{k}]" for k in range(n))
    fc = [f"[0:a]asplit={n}{ins}"]
    for k, (s, e) in enumerate(spans):
        fc.append(f"[in{k}]atrim={s:.3f}:{e:.3f},asetpts=PTS-STARTPTS,"
                  f"afade=t=in:d=0.015,afade=t=out:st={max(0.01, e - s - 0.02):.3f}:d=0.02,"
                  f"aformat=sample_rates=48000:channel_layouts=stereo[s{k}]")
    order = "".join(f"[s{k}]" for k in range(n))
    fc.append(f"{order}concat=n={n}:v=0:a=1,atempo={ATEMPO}[a]")
    wav = work / f"hos_002_{SID}_vo_{VER}.wav"
    ff("-i", str(RAW_VO), "-filter_complex", ";".join(fc), "-map", "[a]", "-c:a", "pcm_s16le", str(wav))
    return wav, mapped


def render_card(path: Path) -> dict:
    """Lower third of the 16:9 centre band: name on line one, place and date on line two."""
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
    top = y1 - size1 - 30
    bot = BAND_TOP + BAND_H + 80
    feather_in, feather_out = 120, 120
    for yy in range(top, bot):
        ramp_in = min(1.0, (yy - top) / feather_in)
        ramp_out = min(1.0, (bot - yy) / feather_out)
        w = 0.5 * (1.0 - math.cos(math.pi * min(ramp_in, ramp_out)))
        a = int(140 * w)
        sd.line([(0, yy), (W, yy)], fill=(0, 0, 0, a))
    img = Image.alpha_composite(img, shade)
    d = ImageDraw.Draw(img)
    d.text((x, y1), CARD[0], font=f1, anchor="ls", fill=YEL, stroke_width=4, stroke_fill=INK)
    d.text((x, y2), CARD[1], font=f2, anchor="ls", fill=CREAM, stroke_width=3, stroke_fill=INK)
    img.save(path)
    return {"name": CARD[0], "line2": CARD[1], "line1_px": size1, "line1_pct_of_band": round(100 * size1 / BAND_H, 1),
            "band": [BAND_TOP, BAND_TOP + BAND_H], "in_s": CARD_IN, "out_s": CARD_OUT, "fade_s": CARD_FADE}


def rel_to_proj(p: Path) -> str:
    for base in (PROJ, NAS_PROJ):
        try:
            return p.relative_to(base).as_posix()
        except ValueError:
            pass
    return p.name


def build(air_date: str) -> dict:
    if WORK.exists():
        shutil.rmtree(WORK)
    WORK.mkdir(parents=True)
    vo, words = lifted_vo(WORK)
    SCRIPT_TXT.write_text(" ".join(w for w, _, _ in words) + "\n")
    vo_s = probe(vo)
    total = round(vo_s + TAIL_S, 3)
    if not 22.0 <= total <= 27.0:
        raise SystemExit(f"{SID}: {total} s outside 22–27 s")
    if not 55 <= len(words) <= 65:
        raise SystemExit(f"{SID}: {len(words)} words outside 55–65")

    cuts = []
    for w, src, ins, x in BEATS:
        if w == 0:
            t = 0.0
        elif w == "loop":
            t = total - LOOP_S
        else:
            t = max(0.0, words[w][1] - 0.12)
        cuts.append((round(t, 3), src, ins, x, w))
    plan, segs = [], []
    for k, (t, src, ins, x, w) in enumerate(cuts):
        end = cuts[k + 1][0] if k + 1 < len(cuts) else total
        d = end - t
        if d < 1.2:
            raise SystemExit(f"{SID}: beat {k} only {d:.2f} s")
        out = WORK / f"seg_{k:02d}.mp4"
        seg(src, out, ins, d, x)
        segs.append(out)
        plan.append({"t0": t, "t1": round(end, 3), "plate": rel_to_proj(src), "in_s": ins,
                     "crop_x": x, "lands_on": w if w in (0, "loop") else words[w][0]})
    (WORK / "pic.txt").write_text("".join(f"file '{s.name}'\n" for s in segs))
    pic = WORK / "picture.mp4"
    ff("-f", "concat", "-safe", "0", "-i", "pic.txt", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "fast",
       "-crf", "17", "-r", str(FPS), "-t", f"{total:.3f}", str(pic), cwd=WORK)

    bed = synth_warm_bed(PROJ / "05_Music" / "hos002_s08_synth_pad_v01.wav", total)
    bed.with_name(bed.stem + "_plan.json").write_text(json.dumps({
        "prompt": ("Warm 1875 gallium-discovery harmonic pad in G-lydian / Em9 voicing (E3, B3, D4, F#4, B4) "
                   "under spoken narration, slow and even, no chase. Pace: 60-80 BPM. NOT a trailer sting, "
                   "NOT a piano solo, NOT 002 four-elements bed, NOT s06/s07/s09 pads, NOT any Orbit With Ben bed, "
                   "NOT a drum loop."),
        "film": "002", "short": f"{SID}_{VER}", "job": "J1064", "orig_job": JOB,
        "source": f"own synthesis in _build_short_{SID}_{VER}.py, 0 credits", "pace_bpm": "60-80",
    }, indent=2) + "\n")
    bed_gain = (mean_db(vo) - 20.0) - mean_db(bed)
    audio = WORK / "audio.wav"
    ff("-i", str(vo), "-i", str(bed), "-filter_complex",
       f"[0:a]aformat=sample_rates=48000:channel_layouts=stereo,apad=whole_dur={total:.3f}[v];"
       f"[1:a]aformat=sample_rates=48000:channel_layouts=stereo,atrim=0:{total:.3f},asetpts=PTS-STARTPTS,"
       f"volume={bed_gain:.2f}dB,afade=t=in:d=0.05,afade=t=out:st={total - 0.2:.3f}:d=0.2[b];"
       f"[v][b]amix=inputs=2:normalize=0:duration=first[a]",
       "-map", "[a]", "-t", f"{total:.3f}", "-c:a", "pcm_s16le", str(audio))

    chunks = chunk_words(words)
    overlays = []
    hook_png = WORK / "cap_hook.png"
    hook_meta = render_hook(hook_png, HOOK)
    overlays.append((hook_png, 0.0, 2.0, "hook", HOOK.replace("**", "")))
    for i, c in enumerate(chunks):
        png = WORK / f"cap_{i:03d}.png"
        render(png, c["text"], 52, 330, anchor="bottom")
        overlays.append((png, c["t0"], min(c["t1"], total - 0.05), "vo", c["text"]))
    title_png = WORK / "cap_title.png"
    render(title_png, TITLE, 58, 250, index=2, stroke=4)
    shade = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    for yy in range(620):
        w = 0.5 * (1.0 + math.cos(math.pi * yy / 620))
        a = int(150 * w)
        ImageDraw.Draw(shade).line([(0, yy), (W, yy)], fill=(0, 0, 0, a))
    Image.alpha_composite(shade, Image.open(title_png)).save(title_png)
    overlays.append((title_png, TITLE_IN, TITLE_OUT, "title", TITLE))
    cta = WORK / "cap_cta.png"
    render(cta, "watch the full film →", 44, 250, anchor="bottom", font_path=CTA_FONT)
    overlays.append((cta, total - LOOP_S, total - 0.08, "cta", "watch the full film →"))
    card_png = WORK / "card_who.png"
    card_meta = render_card(card_png)

    inputs = ["-i", str(pic), "-i", str(audio)]
    for png, *_ in overlays:
        inputs += ["-loop", "1", "-i", str(png)]
    ci = 2 + len(overlays)
    inputs += ["-loop", "1", "-t", f"{total:.3f}", "-i", str(card_png)]
    fc, last = [], "[0:v]"
    fc.append(f"[{ci}:v]format=rgba,fade=t=in:st={CARD_IN}:d={CARD_FADE}:alpha=1,"
              f"fade=t=out:st={CARD_OUT - CARD_FADE}:d={CARD_FADE}:alpha=1[card]")
    fc.append(f"{last}[card]overlay=0:0:enable='between(t,{CARD_IN:.3f},{CARD_OUT:.3f})'[vc]")
    last = "[vc]"
    for i, (_, t0, t1, *_r) in enumerate(overlays, 2):
        fc.append(f"{last}[{i}:v]overlay=0:0:enable='between(t,{t0:.3f},{t1:.3f})'[v{i}]")
        last = f"[v{i}]"
    mp4 = HERE / f"hos_002_{SID}_{VER}.mp4"
    ff(*inputs, "-filter_complex", ";".join(fc), "-map", last, "-map", "1:a", "-c:v", "libx264",
       "-pix_fmt", "yuv420p", "-profile:v", "high", "-preset", "medium", "-crf", "18", "-r", str(FPS),
       "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2", "-t", f"{total:.3f}", "-movflags", "+faststart",
       str(mp4))
    timeline = [{"role": r, "text": t, "t0": round(a, 3), "t1": round(c, 3)} for _, a, c, r, t in overlays]
    timeline.append({"role": "who", "text": " · ".join(CARD), "t0": CARD_IN, "t1": CARD_OUT})
    (WORK / "timeline.json").write_text(json.dumps({"plan": plan, "overlays": timeline}, indent=2) + "\n")
    return {"id": SID, "job": JOB, "test": "B (search-titled)", "air_date_draft": air_date,
            "file": mp4.relative_to(PROJ).as_posix(), "sha256": sha256(mp4), "duration_s": round(probe(mp4), 3),
            "vo_source": rel_to_proj(RAW_VO),
            "vo_span_windows_s": [list(w) for w in SPAN_WINDOWS],
            "route": "lift: But the table is not finished. It never was, in 1869. Noble gases crash the party … A photon can read the difference. (42.30–63.65 s, 74.00–83.48 s from Part 05)",
            "vo_s": round(vo_s, 3), "words": len(words), "max_pause_s": MAX_PAUSE, "atempo": ATEMPO,
            "bed": f"05_Music/{bed.name} (own synthesis, 0 credits)", "bed_gain_db": round(bed_gain, 2),
            "hook": HOOK.replace("**", ""), "hook_layer": hook_meta, "who_card": card_meta,
            "title_on_screen": TITLE, "youtube_title_draft": TITLE_DRAFT, "plan": plan,
            "captions": len(chunks), "timeline": timeline}


def caption_check(mp4: Path, timeline: list[dict]) -> dict:
    frames = WORK / "frames"
    frames.mkdir(parents=True, exist_ok=True)
    vo_rows = [r for r in timeline if r["role"] == "vo"]
    prev_text = prev_hash = None
    changes = matched = 0
    t, dur = 0.0, probe(mp4)
    while t < dur - 0.05:
        crop = frames / f"c{t:05.1f}.png"
        ff("-ss", f"{t:.3f}", "-i", str(mp4), "-frames:v", "1", "-vf", "crop=1000:320:40:1250", str(crop))
        text = next((r["text"] for r in vo_rows if r["t0"] <= t < r["t1"]), None)
        h = hashlib.md5(crop.read_bytes()).hexdigest()
        if prev_text is not None and text != prev_text:
            changes += 1
            matched += h != prev_hash
        prev_text, prev_hash = text, h
        t += 0.5
    ratio = matched / changes if changes else 0.0
    return {"ok": changes >= 7 and ratio >= 0.7, "changes": changes, "ratio": round(ratio, 2)}


def freeze(mp4: Path) -> list[str]:
    err = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(mp4), "-vf",
                          "freezedetect=n=0.003:d=0.8", "-map", "0:v", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    return re.findall(r"freeze_start: ([\d.]+)", err)


def run_qa(mp4: Path, plan: list[dict]) -> dict:
    """Run polish_gate and picture_qa into QA_DIR so QA sweep files are present and PASS."""
    QA_DIR.mkdir(parents=True, exist_ok=True)
    cuts_data, pool_data, seen = [], [], set()
    for k, row in enumerate(plan, 1):
        base = Path(row["plate"]).name
        src_id = f"loop_end_{base}" if row["lands_on"] == "loop" else base
        cuts_data.append({
            "row": f"s{k:02d}_{row['lands_on']}",
            "timeline_in": row["t0"],
            "timeline_out": row["t1"],
            "source": src_id,
            "upscale": 1.0,
            "framing": {"offset": row["in_s"]},
            "video": True,
        })
        if src_id not in seen:
            seen.add(src_id)
            title = f"Loop end plate {base}" if row["lands_on"] == "loop" else f"Flow Veo 3.1 plate {base}"
            pool_data.append({"file_id": src_id, "title": title})
    cuts_f = QA_DIR / f"cuts_{SID}_{VER}.json"
    pool_f = QA_DIR / f"pool_{SID}_{VER}.json"
    cuts_f.write_text(json.dumps(cuts_data, indent=2) + "\n")
    pool_f.write_text(json.dumps(pool_data, indent=2) + "\n")

    pg_json = QA_DIR / f"polish_gate_{SID}_{VER}.json"
    pg_txt = QA_DIR / f"polish_gate_{SID}_{VER}.txt"
    r_pg = subprocess.run([sys.executable, str(OWB_REPO / "scripts/polish_gate.py"),
                           str(mp4.relative_to(REPO)), "--cuts", str(cuts_f.relative_to(REPO)),
                           "--out", str(pg_json.relative_to(REPO))],
                          cwd=REPO, capture_output=True, text=True)
    pg_out = (r_pg.stdout + r_pg.stderr).strip()
    pg_txt.write_text(pg_out + "\n")

    pqa_dir = QA_DIR / f"picture_qa_{SID}_{VER}"
    pqa_txt = QA_DIR / f"picture_qa_{SID}_{VER}.txt"
    r_pqa = subprocess.run([sys.executable, str(OWB_REPO / "scripts/picture_qa.py"),
                            str(mp4.relative_to(REPO)), "--cuts", str(cuts_f.relative_to(REPO)),
                            "--pool", str(pool_f.relative_to(REPO)),
                            "--out-dir", str(pqa_dir.relative_to(REPO))],
                           cwd=REPO, capture_output=True, text=True)
    pqa_out = (r_pqa.stdout + r_pqa.stderr).strip()
    pqa_txt.write_text(pqa_out + "\n")

    mg_json = QA_DIR / f"music_gate_{SID}_{VER}.json"
    mg_txt = QA_DIR / f"music_gate_{SID}_{VER}.txt"
    r_mg = subprocess.run([sys.executable, str(OWB_REPO / "scripts/music_gate.py"),
                           str(PROJ), "--bed", str(PROJ / "05_Music" / "hos002_s08_synth_pad_v01.wav"),
                           "--video", str(mp4), "--out", str(mg_json)],
                          cwd=REPO, capture_output=True, text=True)
    mg_out = (r_mg.stdout + r_mg.stderr).strip()
    mg_txt.write_text(mg_out + "\n")
    return {
        "polish_gate": {"exit": r_pg.returncode, "output": pg_out.splitlines()[-1] if pg_out else ""},
        "picture_qa": {"exit": r_pqa.returncode, "output": pqa_out.splitlines()[-1] if pqa_out else ""},
        "music_gate": {"exit": r_mg.returncode, "output": mg_out.splitlines()[-1] if mg_out else ""},
    }


def run(cmd: list[str]) -> tuple[int, str]:
    r = subprocess.run(cmd, capture_output=True, text=True)
    out = "\n".join(line for line in (r.stdout + r.stderr).splitlines() if "Warning" not in line and line.strip())
    return r.returncode, out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--air-date", default="2026-12-28")
    ap.add_argument("--no-icloud", action="store_true")
    ns = ap.parse_args()
    rec = build(ns.air_date)
    mp4 = PROJ / rec["file"]
    rec["caption_check"] = caption_check(mp4, rec.pop("timeline"))
    code, out = run([sys.executable, str(GATE), "check", str(mp4), "--air-date", ns.air_date])
    rec["gate"] = {"exit": code, "output": out}
    code, out = run([str(VO_PY), str(VO_CHECK), str(mp4), "--script", str(SCRIPT_TXT)])
    rec["vo_check"] = {"exit": code, "output": out}
    rec["freezedetect_starts"] = freeze(mp4)
    rec["qa"] = run_qa(mp4, rec["plan"])
    stills = []
    for t in (0.0, 3.8, 11.5, round(rec["duration_s"] - 1.0, 1)):
        st = WORK / f"{mp4.stem}_t{t:05.1f}.jpg"
        ff("-ss", f"{t:.3f}", "-i", str(mp4), "-frames:v", "1", "-q:v", "3", str(st))
        stills.append(st.relative_to(PROJ).as_posix())
    rec["stills"] = stills
    if not ns.no_icloud:
        ICLOUD.mkdir(parents=True, exist_ok=True)
        dst = ICLOUD / mp4.name
        dst.unlink(missing_ok=True)
        shutil.copy2(mp4, dst)
        rec["icloud"] = str(dst)
    rec["autocomplete_check"] = {
        "date": "2026-10-18",
        "source": "suggestqueries client=youtube ds=yt gl=GB signed-out",
        "hits": [
            "how does the periodic table work",
            "how does the periodic table of elements work",
            "how is the periodic table arranged",
            "noble gases periodic table",
            "position of noble gases in periodic table",
            "mendeleev periodic table vs modern",
        ],
        "note": "'how does the periodic table work', 'how is the periodic table arranged', and 'noble gases periodic table' are exact signed-out GB YouTube autocomplete hits. The lifted VO opens on why Mendeleev's 1869 table was not finished — adding a whole new column for the noble gases and replacing atomic mass with atomic number (how many protons sit in the nucleus, read by X-ray photons). Third search-titled Short on HOS 002 (matching 003, 004, 005, and 006 which each have 3). Chief's call.",
    }
    rec["air_date_draft_note"] = "2026-12-28 used for the gate only; slot is Chief's call."
    rec["who_card_note"] = "card is DMITRI MENDELEEV · First table, 1869, on screen 2.15–5.75 s (3.6 s) right after the 0–2 s hook while 'It never was, in 1869' is spoken. Clear of the 0–2 s hook, the 9–14 s title, and the last 3.0 s CTA."
    rec["overlap_note"] = "Zero overlap with 002 S1–S5 (P04 + 42..120 s, P05 + 5.00..26.20 s, P05 + 122.40..143.40 s), s06_atomic_weights (Part 03), s07_mendeleev_cards (Part 04 0..41 s), Newlands octaves (Part 02), or the Oct 2 four-elements Short (Part 01): this lifts 42.30–63.65 s and 74.00–83.48 s of Part 05 (noble gases new column + atomic number / protons in the nucleus), which had never been used in any 002 Short."
    (HERE / f"SHORT_{SID}_{VER}.json").write_text(json.dumps(rec, indent=2) + "\n")
    print(f"BUILT {SID} {rec['duration_s']} s {rec['words']} words sha {rec['sha256'][:12]} "
          f"captions {rec['caption_check']}")
    print(rec["gate"]["output"])
    print(rec["vo_check"]["output"])
    print(rec["qa"]["polish_gate"]["output"])
    print(rec["qa"]["picture_qa"]["output"])
    print(rec["qa"]["music_gate"]["output"])
    print(f"freezedetect: {len(rec['freezedetect_starts'])} events {rec['freezedetect_starts']}")


if __name__ == "__main__":
    main()
