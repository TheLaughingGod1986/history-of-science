#!/usr/bin/env python3
"""HOS 005 Short s04 v02 (J0934, £0 re-cut of 5n7xFQRBUvI).

Reorder the Part 02 raw take. Drop "Here is what Galen taught."
Open on "heart wasn't a pump at all." The aligned word "The" (27.94–28.72)
sits on silence, so the piece starts at the real onset of "heart".
Then "It was a warm stove…", then the liver and veins (13.56–27.66).
Pauses stay at or under 0.20 s. No new speech.

Picture: 05_heart_stove_t1 at frame 0, first cut 2.15 s, later holds ≤3.8 s,
no "watch the full film" card, 1.0 s loop back onto the frame-0 plate.
The Galen card from v01 stays. Payoff leads (Chief correction 3); the
mechanism is the second beat and the last line loops into line 1.

    python3 _build_short_s04_galen_v02.py
"""
from __future__ import annotations

import json
import math
import os
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
SID, VER, JOB = "s04_galen_stove", "v02", "J0934"
AIR, YT = "2026-10-31", "5n7xFQRBUvI"
TAIL_S = 1.00
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
# (src start, src end). Gaps between pieces are room tone, ≤0.20 s word to word.
PIECES = [(28.66, 30.751), (30.878, 35.071), (13.590, 27.630)]
GAPS = (0.14, 0.14)
# Words kept from the raw alignment, one tuple of (src lo, src hi) per piece.
WORD_WINDOWS = [(28.70, 30.80), (30.85, 35.12), (13.55, 27.70)]


def ff(*a: str, cwd: Path | None = None) -> None:
    subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", *a], check=True, cwd=cwd)


def plate(name: str) -> Path:
    p = CLIPS / name
    if not p.exists() or p.stat().st_size < 1000:
        raise SystemExit(f"missing plate {p}")
    return p


def slice_wav(src: Path, dst: Path, t0: float, t1: float, fade: float = 0.015) -> None:
    dur = t1 - t0
    ff("-ss", f"{t0:.3f}", "-i", str(src), "-t", f"{dur:.3f}",
       "-af", (f"aformat=sample_rates=48000:channel_layouts=stereo,"
               f"afade=t=in:d={fade:.3f},afade=t=out:st={max(0.0, dur - fade - 0.005):.3f}:d={fade:.3f}"),
       "-c:a", "pcm_s16le", str(dst))


def room_gap(src: Path, dst: Path, dur: float) -> None:
    """Quiet room from the take (28.12–28.52, between nourishment and heart)."""
    ff("-ss", "28.12", "-t", "0.40", "-i", str(src),
       "-af", "aformat=sample_rates=48000:channel_layouts=stereo",
       "-c:a", "pcm_s16le", str(WORK / "room.wav"))
    ff("-stream_loop", "-1", "-i", str(WORK / "room.wav"), "-t", f"{dur:.3f}",
       "-af", f"afade=t=in:d=0.01,afade=t=out:st={max(0.0, dur - 0.015):.3f}:d=0.01",
       "-c:a", "pcm_s16le", str(dst))


def build_vo() -> tuple[Path, list[tuple[str, float, float]]]:
    raw_words = b.words_from_align(ALIGN)
    parts: list[Path] = []
    cursor = 0.0
    mapped: list[tuple[str, float, float]] = []
    for i, ((a, c), (lo, hi)) in enumerate(zip(PIECES, WORD_WINDOWS)):
        piece = WORK / f"vo_p{i}.wav"
        slice_wav(RAW, piece, a, c)
        parts.append(piece)
        for w, s, e in raw_words:
            if lo <= s and e <= hi:
                mapped.append((w, round(cursor + (s - a), 3), round(cursor + (e - a), 3)))
        cursor += c - a
        if i < len(GAPS):
            gap = WORK / f"vo_g{i}.wav"
            room_gap(RAW, gap, GAPS[i])
            parts.append(gap)
            cursor += GAPS[i]
    tail = WORK / "vo_tail.wav"
    room_gap(RAW, tail, TAIL_S)
    parts.append(tail)
    lst = WORK / "vo_concat.txt"
    lst.write_text("".join(f"file '{p.name}'\n" for p in parts))
    vo = WORK / f"hos_005_{SID}_vo_{VER}.wav"
    ff("-f", "concat", "-safe", "0", "-i", str(lst), "-c:a", "pcm_s16le", str(vo), cwd=WORK)
    return vo, mapped


def synth_bed(path: Path, dur: float, sr: int = 48000) -> None:
    """Own pad. Not the Part 02 temp bed, and not an Orbit bed."""
    n = int(sr * dur)
    freqs = [73.42, 110.00, 164.81, 220.00, 277.18]
    amps = [0.34, 0.22, 0.14, 0.10, 0.06]
    frames = bytearray()
    for i in range(n):
        t = i / sr
        pulse = 0.86 + 0.14 * math.sin(2 * math.pi * (64 / 60) * t)
        env = min(1.0, t / 0.45) * min(1.0, max(0.0, (dur - t) / 0.4))
        left = right = 0.0
        for k, (f, a) in enumerate(zip(freqs, amps)):
            left += math.sin(2 * math.pi * f * t + 0.4 * k) * a
            right += math.sin(2 * math.pi * (f * 1.003) * t + 0.2 * k) * a
        g = env * pulse * 0.18
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


def sound(vo: Path, total: float) -> dict:
    bed = PROJ / "05_Music" / f"hos_005_{SID}_{VER}_bed.wav"
    synth_bed(bed, total + 0.2)
    plan = {
        "prompt": ("Low warm drone under a spoken history, even and quiet, no chase. "
                   "Pace: 60-70 BPM. NOT the 005 Part 02 harpsichord temp bed, "
                   "NOT the 005 s01 heart-sum pad, NOT any Orbit With Ben bed, "
                   "NOT a drum loop, NOT a trailer sting."),
        "film": "005", "short": f"{SID}_{VER}", "job": JOB,
        "source": "own synthesis in _build_short_s04_galen_v02.py, 0 credits",
        "Pace": "60-70 BPM",
    }
    bed.with_name(bed.stem + "_plan.json").write_text(json.dumps(plan, indent=2) + "\n")
    sfx = place_sfx(total)
    QA.mkdir(parents=True, exist_ok=True)
    bed_db, sfx_db = -8.0, -8.0
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
            differ = abs(r - r2) + abs(g - g2) + abs(bl - b2) > 80
            if differ and (cream or ink):
                mpix[x, y] = 255
    mask = mask.filter(ImageFilter.MaxFilter(5))
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
    # Feather the shade. A hard stop at the band edge reads as a split-panel seam.
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
            "band": [BAND_TOP, BAND_TOP + BAND_H]}


def bounds_for(words: list[tuple[str, float, float]], total: float) -> list[float]:
    def at(token: str, after: float = 0.0) -> float:
        return next(s for w, s, _e in words if w.lower().startswith(token) and s >= after)

    you_t = at("you")
    liver_t = at("liver")
    veins_t = at("veins")
    flesh_t = at("flesh")
    anchors = [0.0, 2.15, you_t, liver_t, veins_t, flesh_t, round(total - TAIL_S, 3), total]
    bounds = [anchors[0]]
    for a, c in zip(anchors, anchors[1:]):
        span = c - a
        if span > 3.75:
            n = math.ceil(span / 3.55)
            for i in range(1, n):
                bounds.append(round(a + span * i / n, 3))
        bounds.append(round(c, 3))
    # Merge a sliver into the previous cut when the join still fits under 3.8 s.
    merged = [bounds[0]]
    for t in bounds[1:]:
        if t - merged[-1] < 1.55 and t < total - 0.05 and (len(merged) < 2 or t - merged[-2] <= 3.80):
            continue
        merged.append(t)
    if merged[-1] != total:
        merged.append(total)
    return merged


def picture(words: list[tuple[str, float, float]], total: float) -> tuple[Path, list[dict]]:
    stove = plate("05_heart_stove_t1.mp4")
    # septum, centuries and why_believe t2 fail polish as split panels.
    middles = [
        plate("08_vesalius_book_t1.mp4"),
        plate("01_galen_scrolls_t1.mp4"),
        plate("03_eat_to_liver_t1.mp4"),
        plate("09_vesalius_nothing_t2.mp4"),
        plate("04_veins_soak_t1.mp4"),
        plate("07_doctors_believe_t1.mp4"),
        plate("10_why_believe_t1.mp4"),
        plate("08_vesalius_book_t1.mp4"),
    ]
    cuts = bounds_for(words, total)
    rows = []
    mid_i = 0
    for i in range(len(cuts) - 1):
        t0, t1 = cuts[i], cuts[i + 1]
        if i == 0:
            src, label, ins = stove, "stove", 0.30
        elif i == len(cuts) - 2:
            src, label, ins = stove, "loop", 0.30
        else:
            src = middles[mid_i]
            mid_i += 1
            label = src.stem
            ins = 0.40
        rows.append((t0, t1, src, ins, 656, label))
    if mid_i > len(middles):
        raise SystemExit(f"need {mid_i} middle plates, have {len(middles)}")
    plan, segs = [], []
    for k, (t0, t1, src, ins, x, label) in enumerate(rows):
        d = round(t1 - t0, 3)
        if d > 3.80:
            raise SystemExit(f"{label} hold {d}")
        if k == 1 and t0 > 3.0:
            raise SystemExit(f"first cut {t0}")
        if label != "loop" and d < 1.50:
            raise SystemExit(f"{label} only {d}")
        out = WORK / f"seg_{k:02d}.mp4"
        b.seg(src, out, ins, d, x)
        segs.append(out)
        plan.append({"t0": t0, "t1": t1, "plate": src.name, "in_s": ins, "crop_x": x,
                     "label": label, "hold_s": d})
    (WORK / "pic.txt").write_text("".join(f"file '{s.name}'\n" for s in segs))
    pic = WORK / "picture.mp4"
    ff("-f", "concat", "-safe", "0", "-i", "pic.txt", "-c:v", "libx264", "-pix_fmt", "yuv420p",
       "-preset", "fast", "-crf", "16", "-r", str(FPS), "-t", f"{total:.3f}", str(pic), cwd=WORK)
    ff("-i", str(pic), "-frames:v", "1", str(WORK / "frame0_pic.png"))
    return pic, plan


def run_qa(mp4: Path, plan: list[dict]) -> dict:
    cuts, pool, seen = [], [], set()
    for k, row in enumerate(plan, 1):
        base = row["plate"]
        src_id = f"loop_end_{base}" if row["label"] == "loop" else base
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


def max_gap(words: list[tuple[str, float, float]]) -> float:
    return max(words[i + 1][1] - words[i][2] for i in range(len(words) - 1))


def build() -> dict:
    if WORK.exists():
        shutil.rmtree(WORK)
    WORK.mkdir(parents=True)
    QA.mkdir(parents=True, exist_ok=True)
    vo, words = build_vo()
    spoken = " ".join(w for w, _, _ in words)
    (WORK / "spoken.txt").write_text(spoken + "\n")
    if words[0][0].lower() != "heart":
        raise SystemExit(f"opener is {words[0][0]!r}, expected heart")
    if words[0][1] > 0.15:
        raise SystemExit(f"first word at {words[0][1]}")
    pump_t = next(s for w, s, _e in words if w.lower().startswith("pump"))
    if pump_t > 1.45:
        raise SystemExit(f"pump at {pump_t}")
    gap = round(max_gap(words), 3)
    if gap > 0.20:
        raise SystemExit(f"pause {gap:.3f}s")
    if "Here is what" in spoken or "taught" in spoken.lower():
        raise SystemExit("setup line still in")
    last_end = words[-1][2]
    total = round(last_end + TAIL_S, 3)
    if not 18.0 <= total <= 24.0:
        raise SystemExit(f"duration {total}")
    pic, plan = picture(words, total)
    snd = sound(vo, total)
    norm = WORK / "audio_norm.wav"
    ff("-i", str(snd["audio"]), "-af", "loudnorm=I=-13.3:TP=-1.5:LRA=11", "-c:a", "pcm_s16le", str(norm))

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
    card_png = WORK / "card_who.png"
    card_meta = render_card(card_png)

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
       "-t", f"{total:.3f}", "-movflags", "+faststart", str(mp4))
    stamped = WORK / "stamped.mp4"
    nframes = int(round(total * FPS))
    ff("-i", str(mp4), "-loop", "1", "-i", str(WORK / "frame0_pic.png"), "-filter_complex",
       f"[1:v]scale={W}:{H},fps={FPS},format=yuv420p[f];"
       f"[0:v][f]overlay=enable='gte(n,{nframes - 2})'[v]",
       "-map", "[v]", "-map", "0:a", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "fast", "-crf", "16",
       "-r", str(FPS), "-c:a", "copy", "-t", f"{total:.3f}", "-movflags", "+faststart", str(stamped))
    stamped.replace(mp4)

    diff = loop_diff(mp4)
    lufs, peak = integrated_lufs(mp4), true_peak(mp4)
    holds = [r["hold_s"] for r in plan]
    you_t = next(s for w, s, _e in words if w.lower().startswith("you"))
    brief = {
        "frame0_source": "04_Generated-Clips/part02/raw/v01/05_heart_stove_t1.mp4",
        "frame0_zoom": "none — moving plate, in 0.30s, crop x=656, no Ken Burns",
        "first_word_s": words[0][1],
        "surprise_s": {"pump": pump_t, "wasnt": next(s for w, s, _e in words if w.lower().startswith("wasn"))},
        "first_cut_s": plan[1]["t0"],
        "last_word_to_loop_s": round(total - last_end, 3),
        "meta_promise": False,
        "runtime_s": round(b.probe(mp4), 3),
        "longest_hold_s": max(holds),
        "payoff_phrase": "heart wasn't a pump",
        "payoff_s": pump_t,
        "payoff_frac": round(pump_t / total, 3),
        "payoff_leads": True,
        "second_beat_s": you_t,
        "loop_sentence": "and your flesh soaks it up as nourishment. heart wasn't a pump at all.",
        "loop_diff": diff,
        "lufs": lufs,
        "true_peak_dbfs": peak,
        "frame0_black": black_frac(mp4, 0.2),
        "max_word_gap_s": round(gap, 3),
        "no_cta": True,
        "dropped_setup": "Here is what Galen taught.",
        "the_trimmed": "Aligned 'The' (27.94-28.72) is silence. Open on heart at src 28.66.",
        "who_card": card_meta,
    }
    meta = {
        "id": SID, "version": VER, "job": JOB, "youtube_id": YT,
        "title": "Is the Heart a Pump?",
        "air_date": AIR, "spoken": spoken, "script": spoken,
        "words": [{"word": w, "start": s, "end": e} for w, s, e in words],
        "word_count": len(words), "last_word_end_s": last_end,
        "plan": plan, "hook": HOOK.replace("**", ""),
        "title_on_screen": b.TITLE, "no_cta": True, "no_new_spend": True,
        "bed": snd["bed"].name, "sfx_level": snd["level"], **brief,
    }
    meta_path = HERE / f"hos_005_{SID}_{VER}_meta.json"
    meta_path.write_text(json.dumps(meta, indent=2) + "\n")
    (HERE / f"SHORT_{SID}_{VER}.json").write_text(json.dumps(meta, indent=2) + "\n")

    gate = subprocess.run([sys.executable, str(REPO / "00_Brand/Channel-Setup/tools/gate_shorts_open.py"),
                           "check", str(mp4), "--air-date", AIR, "--id", YT,
                           "--script", str(WORK / "spoken.txt"),
                           "--vo", str(WORK / "stem_vo.wav"),
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
        "file": mp4.name, "duration_s": brief["runtime_s"], "spoken": spoken,
        "pump_s": pump_t, "first_word_s": words[0][1], "max_gap": gap,
        "brief": brief, "gate_exit": gate.returncode, "gate_verdict": gate_json.get("verdict"),
        "gate_fails": gate_json.get("fails"), "gate_warns": gate_json.get("warns"),
        "qa": qa, "music_exit": music.returncode,
        "music_tail": (music.stdout + music.stderr).strip().splitlines()[-8:],
        "sfx": snd["level"], "copies": copied, "sha256": b.sha256(mp4),
    }
    (QA / f"build_{SID}_{VER}.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps({k: summary[k] for k in (
        "file", "duration_s", "spoken", "pump_s", "first_word_s", "max_gap",
        "gate_verdict", "gate_fails", "gate_warns", "qa", "music_exit", "music_tail", "sfx")}, indent=2))
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
    if diff > 15:
        bad.append(f"loop_diff {diff}")
    if brief["last_word_to_loop_s"] > 1.05:
        bad.append("tail")
    if brief["frame0_black"] > 0.30:
        bad.append(f"black {brief['frame0_black']}")
    if not ( -14.5 <= lufs <= -13.5):
        bad.append(f"lufs {lufs}")
    if peak > -1.0:
        bad.append(f"peak {peak}")
    if bad:
        raise SystemExit("NOT PASS: " + ", ".join(bad))
    print("PASS", mp4.name, brief["runtime_s"], "sha", summary["sha256"][:12])
    return summary


if __name__ == "__main__":
    build()
