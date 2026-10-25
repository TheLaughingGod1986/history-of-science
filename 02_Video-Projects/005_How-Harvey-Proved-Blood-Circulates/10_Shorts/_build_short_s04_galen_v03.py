#!/usr/bin/env python3
"""HOS 005 Short s04 v03 (J0934, £0 re-cut of 5n7xFQRBUvI).

Chief c35: v02 stated Galen's model as fact and its loop_diff was a pasted
frame-0 stamp. This cut keeps "The", moves "For 14 centuries…" to the end
(the payoff, at or after 70%), and trims the 1 s hole between "blood." and
"Your veins" down to room tone. "You eat." is dropped so the cut stays
inside 18–24 s. No new speech, no frame-0 copies.

    python3 _build_short_s04_galen_v03.py
"""
from __future__ import annotations

import hashlib
import json
import math
import os
import re
import shutil
import struct
import subprocess
import sys
import wave
from pathlib import Path

VENV_PY = Path("/Users/benjaminoats/YouTube/History Of Science/"
               "02_Video-Projects/001_How-Did-We-Discover-Germs/10_Shorts/_venv/bin/python")
if VENV_PY.exists() and Path(sys.executable) != VENV_PY:
    os.execv(str(VENV_PY), [str(VENV_PY), str(Path(__file__).resolve()), *sys.argv[1:]])

from PIL import Image, ImageDraw, ImageFilter, ImageFont  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _build_shorts_v03 as b  # noqa: E402

HERE, PROJ, REPO = b.HERE, b.PROJ, b.REPO
SID, VER, JOB = "s04_galen_stove", "v03", "J0934"
AIR, YT = "2026-10-31", "5n7xFQRBUvI"
TAIL_S = 1.00
FIRST_CUT = 2.15
F0_IN = 1.20
NAS = Path("/Volumes/data/mac-mini-archive/hos-worktrees/2026-10-22/hos-005-blood/"
           "02_Video-Projects/005_How-Harvey-Proved-Blood-Circulates")
RAW = NAS / "02_Voiceover/part02_the_liver_that_made_blood_v01_raw.mp3"
ALIGN = NAS / "02_Voiceover/part02_the_liver_that_made_blood_v01_raw_align.json"
CLIPS = NAS / "04_Generated-Clips/part02/raw/v01"
WORK = HERE / f"_work_{SID}_{VER}"
QA = HERE / f"qa_{SID}_{VER}"
OWB = Path("/Users/benjaminoats/YouTube/orbit-with-ben")
W, H, FPS = b.W, b.H, b.FPS
HOOK = "NOT A **PUMP**"
CARD = ("GALEN", "Rome, c. AD 170")
CARD_IN, CARD_OUT, CARD_FADE = 2.30, 5.50, 0.35
BAND_TOP, BAND_H = (H - 608) // 2, 608
# (name, src start, src end). Ends sit 40 ms past the last -60 dB frame.
# "You eat." and "Your food turns into a milky juice," are out so the
# honest tails still fit in 18–24 s. The 1 s hole after "blood." is out.
SLICES = [
    ("pump", 28.200, 30.820),
    ("stove_a", 30.840, 32.720),
    ("stove_b", 33.050, 35.100),
    ("liver", 18.180, 20.760),
    ("veins_a", 21.530, 24.540),
    ("veins_b", 24.930, 27.700),
    ("centuries", 6.500, 11.220),
]
# Room under each join. The first join already has a short breath in the take.
ROOMS = (0.08, 0.05, 0.12, 0.12, 0.06, 0.12)


def ff(*a: str, cwd: Path | None = None) -> None:
    subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", *a], check=True, cwd=cwd)


def plate(name: str) -> Path:
    p = CLIPS / name
    if not p.exists() or p.stat().st_size < 1000:
        raise SystemExit(f"missing plate {p}")
    return p


def slice_wav(src: Path, dst: Path, t0: float, t1: float, fade: float = 0.012) -> None:
    dur = t1 - t0
    ff("-ss", f"{t0:.3f}", "-i", str(src), "-t", f"{dur:.3f}",
       "-af", (f"aformat=sample_rates=48000:channel_layouts=stereo,"
               f"afade=t=in:d={fade:.3f},afade=t=out:st={max(0.0, dur - fade - 0.004):.3f}:d={fade:.3f}"),
       "-c:a", "pcm_s16le", str(dst))


def room_gap(dst: Path, dur: float) -> None:
    """Quiet room after nourishment, before The (27.78–28.08)."""
    ff("-ss", "27.78", "-t", "0.28", "-i", str(RAW),
       "-af", "aformat=sample_rates=48000:channel_layouts=stereo",
       "-c:a", "pcm_s16le", str(WORK / "room.wav"))
    ff("-stream_loop", "-1", "-i", str(WORK / "room.wav"), "-t", f"{dur:.3f}",
       "-af", f"afade=t=in:d=0.008,afade=t=out:st={max(0.0, dur - 0.012):.3f}:d=0.008",
       "-c:a", "pcm_s16le", str(dst))


def hot_bounds(wav: Path, thresh: float = -45.0) -> tuple[float, float, float]:
    """Speech edge. This take's room sits above -60 dB, so -60 marks the room
    as speech. -45 dB is the edge silencedetect uses."""
    with wave.open(str(wav)) as w:
        sr, ch = w.getframerate(), w.getnchannels()
        raw = w.readframes(w.getnframes())
    samples = memoryview(raw).cast("h")
    left = samples[0::2] if ch == 2 else samples
    hop = max(1, sr // 100)
    hot = []
    for i in range(0, len(left) - hop, hop):
        acc = 0.0
        for k in range(i, i + hop):
            v = left[k] / 32768.0
            acc += v * v
        db = -99.0 if acc <= 1e-12 else 20 * math.log10(math.sqrt(acc / hop))
        if db > thresh:
            hot.append(i / sr)
    dur = len(left) / sr
    first = hot[0] if hot else dur
    last = hot[-1] if hot else 0.0
    return dur, first, last


def show_token(word: str) -> str:
    return "14" if word.lower().startswith("fourteen") else word


def build_vo() -> tuple[Path, list[tuple[str, float, float]], list[dict]]:
    raw_words = b.words_from_align(ALIGN)
    parts: list[Path] = []
    placed: list[tuple[str, float, float, float]] = []
    cursor = 0.0
    onsets = []
    for i, (name, a, c) in enumerate(SLICES):
        piece = WORK / f"vo_p{i}.wav"
        slice_wav(RAW, piece, a, c)
        dur, first, last = hot_bounds(piece)
        lead = first
        tail = dur - (last + 0.010)
        onsets.append({
            "piece": name, "src": [a, c], "cut_s": round(cursor, 3),
            "dur_s": round(dur, 3), "first_hot_s": round(first, 4),
            "last_hot_s": round(last, 4), "lead_s": round(lead, 4),
            "tail_s": round(tail, 4), "lead_ok": lead >= 0.020, "tail_ok": tail >= 0.030,
        })
        parts.append(piece)
        placed.append((name, a, c, cursor))
        cursor += c - a
        if i < len(ROOMS):
            gap = WORK / f"vo_g{i}.wav"
            room_gap(gap, ROOMS[i])
            parts.append(gap)
            cursor += ROOMS[i]
    bad = [o for o in onsets if not o["lead_ok"] or not o["tail_ok"]]
    if bad:
        raise SystemExit("onset\n" + json.dumps(bad, indent=2))
    tail = WORK / "vo_tail.wav"
    room_gap(tail, TAIL_S)
    parts.append(tail)
    mapped: list[tuple[str, float, float]] = []
    for w, s, e in raw_words:
        best_i, best_ov = None, 0.015
        for i, (_name, a, c, _cur) in enumerate(placed):
            ov = min(e, c) - max(s, a)
            if ov > best_ov:
                best_i, best_ov = i, ov
        if best_i is None:
            continue
        _name, a, c, cur = placed[best_i]
        ss = cur + (max(s, a) - a)
        ee = cur + (min(e, c) - a)
        if ee - ss < 0.02:
            continue
        mapped.append((show_token(w), round(ss, 3), round(ee, 3)))
    mapped.sort(key=lambda t: (t[1], t[2]))
    lst = WORK / "vo_concat.txt"
    lst.write_text("".join(f"file '{p.name}'\n" for p in parts))
    vo = WORK / f"hos_005_{SID}_vo_{VER}.wav"
    ff("-f", "concat", "-safe", "0", "-i", str(lst), "-c:a", "pcm_s16le", str(vo), cwd=WORK)
    return vo, mapped, onsets


def silence_gaps(wav: Path) -> list[tuple[float, float]]:
    err = subprocess.run(
        ["ffmpeg", "-nostats", "-hide_banner", "-i", str(wav),
         "-af", "silencedetect=noise=-45dB:d=0.22", "-f", "null", "-"],
        capture_output=True, text=True).stderr
    starts = [float(x) for x in re.findall(r"silence_start: ([0-9.]+)", err)]
    ends = [float(x) for x in re.findall(r"silence_end: ([0-9.]+)", err)]
    return list(zip(starts, ends))


def synth_bed(path: Path, dur: float, sr: int = 48000) -> None:
    n = int(sr * dur)
    freqs = [82.41, 123.47, 164.81, 196.00, 246.94]
    amps = [0.34, 0.22, 0.14, 0.09, 0.05]
    frames = bytearray()
    for i in range(n):
        t = i / sr
        pulse = 0.86 + 0.14 * math.sin(2 * math.pi * (68 / 60) * t)
        env = min(1.0, t / 0.50) * min(1.0, max(0.0, (dur - t) / 0.45))
        left = right = 0.0
        for k, (f, a) in enumerate(zip(freqs, amps)):
            left += math.sin(2 * math.pi * f * t + 0.3 * k) * a
            right += math.sin(2 * math.pi * (f * 1.004) * t + 0.15 * k) * a
        g = env * pulse * 0.16
        frames += struct.pack("<hh", int(max(-1, min(1, left * g)) * 32767),
                              int(max(-1, min(1, right * g)) * 32767))
    path.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(path), "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(sr)
        w.writeframes(bytes(frames))


def place_sfx(total: float) -> Path:
    kit = PROJ / "06_Sound-Effects" / "kit_v01"
    whoosh = kit / "sfx_hos_whoosh_soft_v01.wav"
    tick = kit / "sfx_hos_tick_ink_v01.wav"
    if not whoosh.exists():
        subprocess.run([sys.executable, str(OWB / "scripts/sfx_kit.py"), "make",
                        "--out-dir", str(kit), "--house", "hos"], check=True)
    dst = WORK / "sfx_stem.wav"
    delay = int(CARD_IN * 1000)
    ff("-f", "lavfi", "-t", f"{total:.3f}", "-i", "anullsrc=channel_layout=stereo:sample_rate=48000",
       "-i", str(whoosh), "-i", str(tick), "-filter_complex",
       "[1:a]volume=-16dB,afade=t=out:st=0.7:d=0.2[w];"
       f"[2:a]volume=-10dB,adelay={delay}|{delay}[t];"
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


def integrated_lufs(p: Path) -> float:
    err = subprocess.run(["ffmpeg", "-nostats", "-hide_banner", "-i", str(p), "-af", "ebur128", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    lines = [ln for ln in err.splitlines() if "I:" in ln and "LUFS" in ln]
    return float(lines[-1].split("I:")[1].split("LUFS")[0].strip())


def true_peak(p: Path) -> float:
    err = subprocess.run(["ffmpeg", "-nostats", "-hide_banner", "-i", str(p),
                          "-af", "ebur128=peak=true", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    hits = [ln for ln in err.splitlines() if "Peak:" in ln]
    return float(hits[-1].split("Peak:")[1].split("dBFS")[0].strip())


def fit_loudness(src: Path, dst: Path) -> tuple[float, float]:
    """The take is quiet and peaky, so a straight gain stops at the peak and
    the master sits near -17 LUFS. One loudnorm pass raises it to about -14."""
    ff("-i", str(src), "-af", "loudnorm=I=-13.3:TP=-1.6:LRA=11",
       "-c:a", "pcm_s16le", str(dst))
    return integrated_lufs(dst), true_peak(dst)


def sound(vo: Path, total: float) -> dict:
    bed = PROJ / "05_Music" / f"hos_005_{SID}_{VER}_bed.wav"
    synth_bed(bed, total + 0.2)
    plan = {
        "prompt": ("Low warm drone under a spoken history, even and quiet, no chase. "
                   "Pace: 62-78 BPM. NOT the 005 s04 galen v02 pad, "
                   "NOT the 005 s01 heart-sum pad, NOT the 005 Part 02 harpsichord temp bed, "
                   "NOT any Orbit With Ben bed, NOT a drum loop, NOT a trailer sting."),
        "film": "005", "short": f"{SID}_{VER}", "job": JOB,
        "source": "own synthesis in _build_short_s04_galen_v03.py, 0 credits",
        "Pace": "62-78 BPM",
    }
    bed.with_name(bed.stem + "_plan.json").write_text(json.dumps(plan, indent=2) + "\n")
    sfx = place_sfx(total)
    QA.mkdir(parents=True, exist_ok=True)
    bed_db, sfx_db = -10.0, -12.0
    audio = WORK / "audio.wav"
    level: dict = {}
    for _ in range(5):
        mix(vo, bed, sfx, total, audio, bed_db, sfx_db)
        vo_stem, bed_stem, sfx_stem = WORK / "stem_vo.wav", WORK / "stem_bed.wav", WORK / "stem_sfx.wav"
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
    return {"audio": audio, "bed": bed, "level": level}


def loop_diff(mp4: Path) -> float:
    a, c = WORK / "diff_a.png", WORK / "diff_b.png"
    ff("-i", str(mp4), "-frames:v", "1", str(a))
    ff("-sseof", "-0.05", "-i", str(mp4), "-frames:v", "1", str(c))
    im_a = Image.open(a).convert("RGB")
    im_b = Image.open(c).convert("RGB").resize(im_a.size)
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
            yellow = r > 200 and g > 160 and bl < 130
            differ = abs(r - r2) + abs(g - g2) + abs(bl - b2) > 80
            if differ and (cream or ink or yellow):
                mpix[x, y] = 255
    mask = mask.filter(ImageFilter.MaxFilter(7))
    mpix = mask.load()
    acc = n = 0
    for y in range(0, h, 2):
        for x in range(0, w, 2):
            if mpix[x, y]:
                continue
            r, g, bl = pa[x, y]
            r2, g2, b2 = pb[x, y]
            la = 0.2126 * r + 0.7152 * g + 0.0722 * bl
            lb = 0.2126 * r2 + 0.7152 * g2 + 0.0722 * b2
            acc += abs(la - lb)
            n += 1
    return round(acc / max(1, n), 2)


def black_frac(mp4: Path, t: float) -> float:
    raw = subprocess.check_output(["ffmpeg", "-v", "error", "-ss", f"{t:.3f}", "-i", str(mp4),
                                   "-frames:v", "1", "-vf", "scale=160:284", "-f", "rawvideo", "-pix_fmt", "gray", "-"])
    return round(sum(1 for p in raw if p < 18) / max(1, len(raw)), 3)


def render_card(path: Path) -> dict:
    size1 = int(BAND_H * 0.12)
    size2 = int(BAND_H * 0.075)
    f1 = ImageFont.truetype(b.FONT, size1, index=2)
    f2 = ImageFont.truetype(b.CTA_FONT, size2)
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    shade = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shade)
    y2 = BAND_TOP + BAND_H - 80
    y1 = y2 - size2 - 18
    top = y1 - size1 - 40
    band_bottom = BAND_TOP + BAND_H
    for yy in range(top, min(H, band_bottom + 80)):
        rise = min(1.0, (yy - top) / 90)
        fall = 1.0 if yy < band_bottom - 70 else max(0.0, 1 - (yy - (band_bottom - 70)) / 150)
        a = int(100 * rise * fall)
        if a <= 0:
            continue
        sd.line([(0, yy), (W, yy)], fill=(0, 0, 0, a))
    img = Image.alpha_composite(img, shade)
    d = ImageDraw.Draw(img)
    d.text((70, y1), CARD[0], font=f1, anchor="ls", fill=b.YEL, stroke_width=4, stroke_fill=b.INK)
    d.text((70, y2), CARD[1], font=f2, anchor="ls", fill=b.CREAM, stroke_width=3, stroke_fill=b.INK)
    img.save(path)
    return {"name": CARD[0], "line2": CARD[1], "in_s": CARD_IN, "out_s": CARD_OUT,
            "y": [int(top), int(y2)], "band": [BAND_TOP, band_bottom]}


def nframes(p: Path) -> int:
    out = subprocess.check_output(
        ["ffprobe", "-v", "error", "-select_streams", "v:0", "-count_frames",
         "-show_entries", "stream=nb_read_frames", "-of", "csv=p=0", str(p)], text=True).strip()
    return int(out)


def stove_parts(src: Path, open_dur: float, loop_dur: float, open_out: Path, loop_out: Path) -> None:
    span = WORK / "stove_span.mp4"
    start = F0_IN - loop_dur
    n_loop = int(round(loop_dur * FPS))
    n_open = int(round(open_dur * FPS))
    vf = f"scale=1920:1080,crop=608:1080:656:0,scale={W}:{H}:flags=lanczos,setsar=1,fps={FPS}"
    ff("-i", str(src), "-ss", f"{start:.3f}", "-t", f"{(n_loop + n_open) / FPS + 0.08:.3f}",
       "-vf", vf, "-an", "-c:v", "libx264", "-pix_fmt", "yuv420p",
       "-preset", "fast", "-crf", "16", "-r", str(FPS), str(span))
    common = ["-an", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "fast", "-crf", "16", "-r", str(FPS)]
    ff("-i", str(span), "-vf", f"trim=start_frame=0:end_frame={n_loop},setpts=PTS-STARTPTS", *common, str(loop_out))
    ff("-i", str(span), "-vf", f"trim=start_frame={n_loop}:end_frame={n_loop + n_open},setpts=PTS-STARTPTS",
       *common, str(open_out))


def picture(words: list[tuple[str, float, float]], total: float) -> tuple[Path, list[dict]]:
    for_t = next(s for w, s, _e in words if w.lower().rstrip(".,") in {"for", "14"})
    loop_start = round(total - TAIL_S, 3)
    bounds = [0.0, FIRST_CUT]
    span = for_t - FIRST_CUT
    n = max(1, math.ceil(span / 2.85))
    for i in range(1, n):
        bounds.append(round(FIRST_CUT + span * i / n, 3))
    bounds.append(round(for_t, 3))
    bounds.append(round((for_t + loop_start) / 2, 3))
    bounds.append(loop_start)
    bounds.append(total)
    middles = [
        "01_galen_scrolls_t1.mp4",
        "08_vesalius_book_t1.mp4",
        "03_eat_to_liver_t1.mp4",
        "09_vesalius_nothing_t1.mp4",
        "04_veins_soak_t1.mp4",
        "11_padua_explorer_t1.mp4",
        "12_fabricius_t1.mp4",
        "13_little_doors_t1.mp4",
        "14_pool_feet_t1.mp4",
    ]
    cent = ["07_doctors_believe_t1.mp4", "10_why_believe_t1.mp4"]
    stove = plate("05_heart_stove_t1.mp4")
    rows = []
    mi = ci = 0
    for i in range(len(bounds) - 1):
        t0, t1 = bounds[i], bounds[i + 1]
        d = round(t1 - t0, 3)
        if i == 0:
            rows.append((t0, t1, stove, F0_IN, "stove"))
        elif i == len(bounds) - 2:
            rows.append((t0, t1, stove, round(F0_IN - TAIL_S, 3), "loop"))
        elif t0 >= for_t - 0.05:
            name = cent[min(ci, len(cent) - 1)]
            ci += 1
            rows.append((t0, t1, plate(name), 0.40, Path(name).stem))
        else:
            name = middles[mi]
            mi += 1
            rows.append((t0, t1, plate(name), 0.45, Path(name).stem))
        if d > 3.001:
            raise SystemExit(f"hold {rows[-1][4]} {d}")
        if rows[-1][4] != "loop" and d < 1.50:
            raise SystemExit(f"short hold {rows[-1][4]} {d}")
    if rows[1][0] > 2.60:
        raise SystemExit(f"first cut {rows[1][0]}")
    open_out, loop_out = WORK / "seg_stove_open.mp4", WORK / "seg_stove_loop.mp4"
    stove_parts(stove, FIRST_CUT, TAIL_S, open_out, loop_out)
    plan, segs = [], []
    for k, (t0, t1, src, ins, label) in enumerate(rows):
        d = round(t1 - t0, 3)
        out = WORK / f"seg_{k:02d}.mp4"
        if label == "stove":
            shutil.copy2(open_out, out)
        elif label == "loop":
            shutil.copy2(loop_out, out)
        else:
            b.seg(src, out, ins, d, 656)
        segs.append(out)
        plan.append({"t0": t0, "t1": t1, "plate": src.name, "in_s": ins, "crop_x": 656,
                     "label": label, "hold_s": d})
    target = int(round(total * FPS))
    extra = sum(nframes(s) for s in segs) - target
    if extra > 0:
        mid_i = max((i for i, row in enumerate(plan) if row["label"] not in {"stove", "loop"}),
                    key=lambda i: plan[i]["hold_s"])
        keep = nframes(segs[mid_i]) - extra
        if keep < int(1.5 * FPS):
            raise SystemExit(f"{plan[mid_i]['label']} would shrink to {keep} frames")
        trimmed = WORK / "seg_trim.mp4"
        ff("-i", str(segs[mid_i]), "-vf", f"trim=end_frame={keep},setpts=PTS-STARTPTS",
           "-an", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "fast", "-crf", "16",
           "-r", str(FPS), str(trimmed))
        segs[mid_i] = trimmed
        plan[mid_i]["hold_s"] = round(keep / FPS, 3)
        plan[mid_i]["t1"] = round(plan[mid_i]["t0"] + keep / FPS, 3)
        # Pull the later cuts back so the timeline still ends on the loop.
        shift = plan[mid_i]["t1"]
        for row, seg in zip(plan[mid_i + 1:], segs[mid_i + 1:]):
            dur = nframes(seg) / FPS
            row["t0"] = round(shift, 3)
            row["t1"] = round(shift + dur, 3)
            row["hold_s"] = round(dur, 3)
            shift = row["t1"]
    got = sum(nframes(s) for s in segs)
    if got != target:
        raise SystemExit(f"frame count {got} != {target}")
    (WORK / "pic.txt").write_text("".join(f"file '{s.name}'\n" for s in segs))
    pic = WORK / "picture.mp4"
    ff("-f", "concat", "-safe", "0", "-i", "pic.txt", "-c:v", "libx264", "-pix_fmt", "yuv420p",
       "-preset", "fast", "-crf", "16", "-r", str(FPS), str(pic), cwd=WORK)
    return pic, plan


def run_qa(mp4: Path, plan: list[dict]) -> dict:
    cuts, pool, seen = [], [], set()
    for k, row in enumerate(plan, 1):
        base = row["plate"]
        src_id = f"loop_span_{base}" if row["label"] == "loop" else base
        cuts.append({"row": f"s{k:02d}_{row['label']}", "timeline_in": row["t0"], "timeline_out": row["t1"],
                     "source": src_id, "upscale": 1.78, "video": True, "framing": {"offset": row["in_s"]}})
        if src_id not in seen:
            seen.add(src_id)
            pool.append({"file_id": src_id, "title": f"Veo plate {base}"})
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
    return {"polish_gate": {"exit": r_pg.returncode, "tail": (r_pg.stdout + r_pg.stderr).strip().splitlines()[-6:]},
            "picture_qa": {"exit": r_pq.returncode, "tail": (r_pq.stdout + r_pq.stderr).strip().splitlines()[-8:]}}


def norm_tokens(text: str) -> list[str]:
    t = text.lower().replace("'", "'").replace("’", "'")
    return re.findall(r"[a-z0-9']+", t)


def canon(tok: str) -> str:
    if tok in {"14", "fourteen"}:
        return "14"
    return tok


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


def asr_check(spoken: str, vo: Path) -> dict:
    stem = whisper_words(vo)
    want, got = [canon(t) for t in norm_tokens(spoken)], [canon(t) for t in norm_tokens(stem["text"])]
    notes = []
    if norm_tokens(stem["text"]) != norm_tokens(spoken) and want == got:
        notes.append("small.en token differs only by 14/fourteen; spoken line kept")
    if want != got:
        notes.append(f"stem {stem['text']!r}")
    payload = {"model": "small.en", "spoken": spoken, "stem": stem, "ok": want == got, "notes": notes}
    (QA / f"asr_{SID}_{VER}.json").write_text(json.dumps(payload, indent=2) + "\n")
    (QA / f"asr_{SID}_{VER}.txt").write_text(
        f"spoken: {spoken}\nstem: {stem['text']}\n"
        + (("\n".join(notes) + "\n") if notes else "")
        + ("OK\n" if payload["ok"] else "FAIL\n"))
    return payload


def build() -> dict:
    if WORK.exists():
        shutil.rmtree(WORK)
    WORK.mkdir(parents=True)
    QA.mkdir(parents=True, exist_ok=True)
    vo, words, onsets = build_vo()
    spoken = " ".join(w for w, _, _ in words)
    (WORK / "spoken.txt").write_text(spoken + "\n")
    (QA / f"onset_{SID}_{VER}.json").write_text(json.dumps(onsets, indent=2) + "\n")
    print("SPOKEN", spoken)
    if not words or words[0][0].lower().rstrip(".,") != "the":
        raise SystemExit(f"opener is {words[0][0] if words else None!r}, expected The")
    if words[0][1] > 0.15:
        raise SystemExit(f"first word at {words[0][1]}")
    pump_t = next(s for w, s, _e in words if w.lower().startswith("pump"))
    if pump_t > 1.50:
        raise SystemExit(f"pump at {pump_t}")
    banned = {w.lower().rstrip(".,") for w, _, _ in words}
    if banned & {"eat", "taught", "here"}:
        raise SystemExit("dropped or setup line still in: " + spoken)
    if "galen" in spoken.lower():
        raise SystemExit("Galen is on the card only; the take has no 'For Galen'")
    gaps = [round(words[i + 1][1] - words[i][2], 3) for i in range(len(words) - 1)]
    # Alignment gaps overstate the breaths (c35: the v02 "0.20" was the character
    # times). Real holes are the -45 dB detect below. A join past 0.45 s is a missed word.
    if max(gaps) > 0.45:
        pairs = [f"{words[i][0]!r}->{words[i+1][0]!r} {gaps[i]}" for i in range(len(gaps)) if gaps[i] > 0.30]
        raise SystemExit(f"pause {max(gaps):.3f}s {pairs}")
    last_end = words[-1][2]
    total = round(b.probe(vo), 3)
    if not 18.0 <= total <= 24.0:
        raise SystemExit(f"duration {total} spoken_end {last_end}")
    tail_gap = round(total - last_end, 3)
    if not 0.85 <= tail_gap <= 1.50:
        raise SystemExit(f"tail {tail_gap} (last word {last_end}, file {total})")
    holes = []
    for a, c in silence_gaps(vo):
        if a >= last_end - 0.05:
            continue
        span = c - a
        inside = False
        for _w, s, e in words:
            ov = min(c, e) - max(a, s)
            if ov > 0.35 * span:
                inside = True
                break
        if not inside and span > 0.20:
            holes.append((round(a, 3), round(c, 3), round(span, 3)))
    if holes:
        raise SystemExit(f"silencedetect -45 dB gaps {holes}")
    for_t = next(s for w, s, _e in words if w.lower().rstrip(".,") in {"for", "14"})
    if for_t / total < 0.70:
        raise SystemExit(f"payoff {for_t / total:.3f} at {for_t}")
    print(f"VO ok {total:.2f}s pump {pump_t:.2f} payoff {for_t / total:.3f} max_gap {max(gaps):.3f}")

    pic, plan = picture(words, total)
    snd = sound(vo, total)
    if snd["level"]["exit"] != 0:
        raise SystemExit("sfx level\n" + snd["level"]["output"])
    norm = WORK / "audio_norm.wav"
    fit_loudness(snd["audio"], norm)

    chunks = b.chunk_words(words)
    overlays = []
    hook_png = WORK / "cap_hook.png"
    b.render_hook(hook_png, HOOK)
    overlays.append((hook_png, 0.0, 2.0))
    for i, c in enumerate(chunks):
        png = WORK / f"cap_{i:03d}.png"
        b.render(png, c["text"], 52, 330, anchor="bottom")
        overlays.append((png, c["t0"], min(c["t1"], total - 0.05)))
    title_png = WORK / "cap_title.png"
    b.render(title_png, b.TITLE, 62, 250, index=2, stroke=4)
    shade = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    for yy in range(560):
        a = int(150 * (1 - yy / 560) ** 1.5)
        ImageDraw.Draw(shade).line([(0, yy), (W, yy)], fill=(0, 0, 0, a))
    Image.alpha_composite(shade, Image.open(title_png)).save(title_png)
    overlays.append((title_png, b.TITLE_IN, b.TITLE_OUT))
    if not (CARD_OUT <= b.TITLE_IN or CARD_IN >= b.TITLE_OUT):
        raise SystemExit("Galen card overlaps the promo title")
    card_png = WORK / "card_who.png"
    card_meta = render_card(card_png)

    target_frames = int(round(total * FPS))
    inputs = ["-i", str(pic), "-i", str(norm)]
    for png, *_ in overlays:
        inputs += ["-loop", "1", "-i", str(png)]
    ci = 2 + len(overlays)
    inputs += ["-loop", "1", "-t", f"{total:.3f}", "-i", str(card_png)]
    fc, last = [], "[0:v]"
    fc.append(f"[{ci}:v]format=rgba,fade=t=in:st={CARD_IN}:d={CARD_FADE}:alpha=1,"
              f"fade=t=out:st={CARD_OUT - CARD_FADE}:d={CARD_FADE}:alpha=1[card]")
    fc.append(f"{last}[card]overlay=0:0:enable='between(t,{CARD_IN:.3f},{CARD_OUT:.3f})'[vc]")
    last = "[vc]"
    for i, (_, t0, t1) in enumerate(overlays, 2):
        fc.append(f"{last}[{i}:v]overlay=0:0:enable='between(t,{t0:.3f},{t1:.3f})'[v{i}]")
        last = f"[v{i}]"
    mp4 = HERE / f"hos_005_{SID}_{VER}.mp4"
    ff(*inputs, "-filter_complex", ";".join(fc), "-map", last, "-map", "1:a",
       "-c:v", "libx264", "-pix_fmt", "yuv420p", "-profile:v", "high", "-preset", "medium", "-crf", "18",
       "-r", str(FPS), "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2",
       "-frames:v", str(target_frames), "-t", f"{target_frames / FPS:.6f}",
       "-movflags", "+faststart", str(mp4))

    diff = loop_diff(mp4)
    lufs, peak = integrated_lufs(mp4), true_peak(mp4)
    holds = [r["hold_s"] for r in plan]
    sha = hashlib.sha256(mp4.read_bytes()).hexdigest()
    asr = asr_check(spoken, vo)
    brief = {
        "frame0_source": "04_Generated-Clips/part02/raw/v01/05_heart_stove_t1.mp4",
        "frame0_zoom": f"none — moving plate, in {F0_IN}s, crop x=656, no Ken Burns",
        "frame0_in_s": F0_IN,
        "loop_in_s": round(F0_IN - TAIL_S, 3),
        "loop_ends_on": "frame before frame 0 in-point; no frame-0 copy",
        "no_frame0_stamp": True,
        "first_word_s": words[0][1],
        "surprise_s": {"pump": pump_t, "wasnt": next(s for w, s, _e in words if "wasn" in w.lower())},
        "first_cut_s": plan[1]["t0"],
        "last_word_to_loop_s": round(total - last_end, 3),
        "meta_promise": False,
        "runtime_s": round(b.probe(mp4), 3),
        "longest_hold_s": max(holds),
        "payoff_phrase": "For 14 centuries",
        "payoff_s": for_t,
        "payoff_frac": round(for_t / total, 3),
        "payoff_leads": False,
        "loop_sentence": "argue with his books. The heart wasn't a pump at all.",
        "loop_diff": diff,
        "lufs": lufs,
        "true_peak_dbfs": peak,
        "frame0_black": black_frac(mp4, 0.2),
        "max_word_gap_s": max(gaps),
        "no_cta": True,
        "dropped": "You eat. Your food turns into a milky juice. Here is what Galen taught.",
        "who_card": card_meta,
        "onset": onsets,
        "sha256": sha,
    }
    meta = {
        "id": SID, "version": VER, "job": JOB, "youtube_id": YT,
        "title": "Is the Heart a Pump?",
        "air_date": AIR, "spoken": spoken, "script": spoken,
        "words": [{"word": w, "start": s, "end": e} for w, s, e in words],
        "word_count": len(words), "last_word_end_s": last_end,
        "plan": plan, "hook": HOOK.replace("**", ""),
        "title_on_screen": b.TITLE, "no_cta": True, "no_new_spend": True,
        "bed": snd["bed"].name, "sfx_level": snd["level"],
        "asr": {"ok": asr["ok"], "notes": asr["notes"], "stem": asr["stem"]["text"]},
        **brief,
    }
    meta_path = HERE / f"hos_005_{SID}_{VER}_meta.json"
    meta_path.write_text(json.dumps(meta, indent=2) + "\n")
    (HERE / f"SHORT_{SID}_{VER}.json").write_text(json.dumps(meta, indent=2) + "\n")

    gate = subprocess.run([sys.executable, str(REPO / "00_Brand/Channel-Setup/tools/gate_shorts_open.py"),
                           "check", str(mp4), "--air-date", AIR, "--id", YT,
                           "--script", str(WORK / "spoken.txt"),
                           "--vo", str(vo),
                           "--meta", str(meta_path), "--json"],
                          capture_output=True, text=True)
    (QA / f"gate_{SID}_{VER}.txt").write_text((gate.stdout + gate.stderr).strip() + "\n")
    try:
        gate_json = json.loads(gate.stdout)
        if isinstance(gate_json, list):
            gate_json = gate_json[0]
    except json.JSONDecodeError:
        gate_json = {"verdict": "FAIL", "raw": (gate.stdout + gate.stderr)[-2000:]}
    (QA / f"gate_{SID}_{VER}.json").write_text(json.dumps(gate_json, indent=2) + "\n")
    j0918 = (
        "J0918 HOS ship gate (Chief, 24 Oct 2026).\n"
        "(a) FAIL a pushed still at frame 0 when the 0-1.5 s centre-band frame diff is under 1.50.\n"
        "(b) FAIL when the first cut comes after 3.0 s.\n"
        "(c) WARN when the first VO word starts after 0.15 s.\n"
        "(d) WARN when the gap from the last word to the end of the file is over 1.5 s.\n"
        "(e) FAIL if the script or the spoken line contains a meta-promise.\n"
        f"measured frame0_diff_0_1_5s={gate_json.get('frame0_diff_0_1_5s')} "
        f"first_cut_s={gate_json.get('first_cut_s')} "
        f"vo_onset_s={gate_json.get('vo_onset_s')} "
        f"tail_gap_s={gate_json.get('tail_gap_s')} "
        f"stayed_fails={gate_json.get('stayed_fails')}\n"
    )
    (QA / f"j0918_ship_gate_{SID}_{VER}.txt").write_text(j0918)

    qa = run_qa(mp4, plan)
    music = subprocess.run([sys.executable, str(OWB / "scripts/music_gate.py"), str(PROJ),
                            "--bed", str(snd["bed"]), "--video", str(mp4),
                            "--out", str(QA / f"music_gate_{SID}_{VER}.json")],
                           capture_output=True, text=True)
    (QA / f"music_gate_{SID}_{VER}.txt").write_text((music.stdout + music.stderr).strip() + "\n")

    phone = HERE / f"hos_005_{SID}_{VER}_PHONE.mp4"
    ff("-i", str(mp4), "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "fast", "-crf", "26",
       "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart", str(phone))
    sheet = QA / f"hos_005_{SID}_{VER}_2fps_sheet.jpg"
    ff("-i", str(mp4), "-vf", "fps=2,scale=180:-2,tile=8x8", "-q:v", "4", str(sheet))
    uat = Path.home() / "Library/Mobile Documents/com~apple~CloudDocs/HOS UAT/005_How-Harvey-Proved-Blood-Circulates/10_Shorts"
    nas_out = Path("/Volumes/data/mac-mini-archive/YouTube/History Of Science/02_Video-Projects/"
                   "005_How-Harvey-Proved-Blood-Circulates/10_Shorts") / f"{SID}_{VER}"
    copied = []
    for folder in (uat, nas_out):
        folder.mkdir(parents=True, exist_ok=True)
        for src in (mp4, phone, sheet):
            shutil.copy2(src, folder / src.name)
            copied.append(str(folder / src.name))

    summary = {
        "file": mp4.name, "sha256": sha, "duration_s": brief["runtime_s"], "spoken": spoken,
        "brief": brief, "gate_exit": gate.returncode, "gate_verdict": gate_json.get("verdict"),
        "gate_fails": gate_json.get("fails"), "gate_warns": gate_json.get("warns"),
        "qa": qa, "music_exit": music.returncode,
        "music_tail": (music.stdout + music.stderr).strip().splitlines()[-8:],
        "sfx": snd["level"], "copies": copied, "asr_ok": asr["ok"], "asr_notes": asr["notes"],
        "onset": onsets,
    }
    (QA / f"build_{SID}_{VER}.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps({k: summary[k] for k in (
        "file", "duration_s", "gate_verdict", "gate_fails", "gate_warns", "qa",
        "music_exit", "music_tail", "sfx", "asr_ok", "asr_notes")}, indent=2))
    bad = []
    if summary["gate_verdict"] != "PASS":
        bad.append("gate")
    if qa["polish_gate"]["exit"] != 0:
        bad.append("polish")
    if qa["picture_qa"]["exit"] != 0:
        bad.append("picture")
    if music.returncode != 0:
        bad.append("music")
    if snd["level"]["exit"] != 0:
        bad.append("sfx")
    if diff > 5:
        bad.append(f"loop_diff {diff}")
    if brief["payoff_frac"] < 0.70:
        bad.append("payoff")
    if not (-14.5 <= lufs <= -13.5):
        bad.append(f"lufs {lufs}")
    if peak > -1.0:
        bad.append(f"peak {peak}")
    if max(holds) > 3.001:
        bad.append("hold")
    if not asr["ok"]:
        bad.append("asr")
    if brief["frame0_black"] > 0.30:
        bad.append(f"black {brief['frame0_black']}")
    if bad:
        raise SystemExit("NOT PASS: " + ", ".join(bad))
    print("PASS", mp4.name, brief["runtime_s"], "loop_diff", diff, "lufs", lufs, "sha", sha[:12])
    return summary


if __name__ == "__main__":
    build()
