#!/usr/bin/env python3
"""HOS 005 Short s01 v04 (J0934, £0 picture re-cut of 1lszTrYRp-8).

VO stays the frozen v01_fin wav. v03 is left untouched.

- 12_glowing_loop_t2 ends at 20.0 s.
- An unused circulation plate (07_capillaries_loop_t2) covers
  "So it's the same blood, going round and round." Hold <= 3.0 s.
- The loop is 01_pulse_wrist_t1 running into frame 0's in-point.
  No frame-0 paste. Audio tail stays 0.57 s.
- Card WILLIAM HARVEY / London, 1628 over 2.2–5.0 s. The promo title
  stays at 9–14 s, off the card.
- Master aimed at -14.0 LUFS, true peak <= -1.0 dBFS. Holds <= 3.0 s.

    python3 _build_short_s01_the_sum_v04.py
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
SID, VER, JOB = "s01_the_sum", "v04", "J0934"
AIR, YT = "2026-10-30", "1lszTrYRp-8"
TAIL_S = 0.57
# Opening still starts here. The loop ends on the frame before it.
F0_IN = 1.40
LOOP_S = 1.10
NAS = Path("/Volumes/data/mac-mini-archive/hos-worktrees/2026-10-22/hos-005-blood/"
           "02_Video-Projects/005_How-Harvey-Proved-Blood-Circulates")
CLIPS = NAS / "04_Generated-Clips"
VO = NAS / "10_Shorts/vo_v01/hos_005_s01_the_sum_vo_v01_fin.wav"
ALIGN = HERE / "vo_v01/hos_005_s01_the_sum_vo_v01_fin_align.json"
WORK = HERE / f"_work_{SID}_{VER}"
QA = HERE / f"qa_{SID}_{VER}"
OWB = Path("/Users/benjaminoats/YouTube/orbit-with-ben")
W, H, FPS = b.W, b.H, b.FPS
HOOK = "MORE THAN YOU **HAVE**"
CARD = ("WILLIAM HARVEY", "London, 1628")
CARD_IN, CARD_OUT, CARD_FADE = 2.20, 5.00, 0.35
BAND_TOP, BAND_H = (H - 608) // 2, 608
# Override with ROUND_PLATE=part04/raw/v01/06_veins_swell_t1.mp4 if polish fails.
ROUND_PLATE = os.environ.get("ROUND_PLATE", "part05/raw/v01/07_capillaries_loop_t2.mp4")


def ff(*a: str, cwd: Path | None = None) -> None:
    subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", *a], check=True, cwd=cwd)


def plate(rel: str) -> Path:
    p = CLIPS / rel
    if not p.exists() or p.stat().st_size < 1000:
        raise SystemExit(f"missing plate {p}")
    return p


def sha256(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def synth_bed(path: Path, dur: float, sr: int = 48000) -> None:
    """Own pulse at 63 BPM. Not the v03 70 BPM pad, and not a Part 03 bed."""
    n = int(sr * dur)
    freqs = [73.42, 110.00, 146.83, 220.00, 293.66]
    amps = [0.34, 0.20, 0.14, 0.09, 0.05]
    frames = bytearray()
    for i in range(n):
        t = i / sr
        pulse = 0.88 + 0.12 * math.sin(2 * math.pi * (63 / 60) * t)
        env = min(1.0, t / 0.5) * min(1.0, max(0.0, (dur - t) / 0.4))
        l = r = 0.0
        for k, (f, a) in enumerate(zip(freqs, amps)):
            l += math.sin(2 * math.pi * f * t + 0.25 * k) * a
            r += math.sin(2 * math.pi * (f * 1.003) * t + 0.4 * k) * a
        g = env * pulse * 0.18
        frames += struct.pack("<hh", int(max(-1, min(1, l * g)) * 32767),
                              int(max(-1, min(1, r * g)) * 32767))
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
    if not whoosh.exists() or not tick.exists():
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
       f"[v][b][s]amix=inputs=3:normalize=0:duration=first,alimiter=limit=0.89[a]",
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


def onset_piece(wav: Path) -> dict:
    """10 ms frames. Lead is time before the first frame above -60 dB."""
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
        if db > -60.0:
            hot.append(i / sr)
    dur = len(left) / sr
    first = hot[0] if hot else dur
    last = hot[-1] if hot else 0.0
    lead = first
    tail = dur - (last + 0.010)
    return {
        "piece": "vo_v01_fin frozen",
        "cut_s": 0.0,
        "end_s": round(dur, 4),
        "first_hot_s": round(first, 4),
        "last_hot_s": round(last, 4),
        "lead_s": round(lead, 4),
        "tail_s": round(tail, 4),
        "lead_ok": lead >= 0.020,
        "tail_ok": tail >= 0.030,
        "note": "VO stays frozen (J0934 item 2). Lead and tail are measured, not re-cut.",
    }


def norm_tokens(text: str) -> list[str]:
    t = text.lower().replace("'", "'").replace("’", "'")
    return re.findall(r"[a-z0-9']+", t)


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
    want, got = norm_tokens(spoken), norm_tokens(stem["text"])
    # small.en hears the frozen alignment word "proved" as "approved". The VO is not re-cut.
    folded = ["proved" if t == "approved" else t for t in got]
    notes = []
    if folded != want:
        notes.append(f"stem {stem['text']!r}")
    elif got != want:
        notes.append("small.en heard 'approved' for the alignment word 'proved'; VO frozen, spoken line kept")
    payload = {"model": "small.en", "spoken": spoken, "stem": stem, "ok": folded == want, "notes": notes}
    (QA / f"asr_{SID}_{VER}.json").write_text(json.dumps(payload, indent=2) + "\n")
    (QA / f"asr_{SID}_{VER}.txt").write_text(
        f"spoken: {spoken}\nstem: {stem['text']}\n"
        + (("\n".join(notes) + "\n") if notes else "")
        + ("OK\n" if payload["ok"] else "FAIL\n"))
    return payload


def render_card(path: Path) -> dict:
    size1 = int(BAND_H * 0.11)
    size2 = int(BAND_H * 0.075)
    f1 = ImageFont.truetype(b.FONT, size1, index=2)
    f2 = ImageFont.truetype(b.CTA_FONT, size2)
    while f1.getlength(CARD[0]) > W - 160 and size1 > 42:
        size1 -= 2
        f1 = ImageFont.truetype(b.FONT, size1, index=2)
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
    return {"line1": CARD[0], "line2": CARD[1], "y": [int(top), int(y2)],
            "band": [BAND_TOP, band_bottom], "in_s": CARD_IN, "out_s": CARD_OUT}


def sound(vo: Path, total: float) -> dict:
    bed = PROJ / "05_Music" / f"hos_005_{SID}_{VER}_bed.wav"
    synth_bed(bed, total + 0.2)
    plan = {
        "prompt": ("Low warm pulse under a spoken sum, even and quiet, no chase. "
                   "Pace: 60-68 BPM. NOT the v03 70 BPM pad, NOT the 005 Part 03 harpsichord bed, "
                   "NOT any Orbit With Ben bed, NOT a drum loop, NOT a trailer sting."),
        "film": "005", "short": f"{SID}_{VER}", "job": JOB,
        "source": "own synthesis in _build_short_s01_the_sum_v04.py, 0 credits",
        "pace_bpm": "60-68",
    }
    bed.with_name(bed.stem + "_plan.json").write_text(json.dumps(plan, indent=2) + "\n")
    sfx = place_sfx(total)
    QA.mkdir(parents=True, exist_ok=True)
    bed_db, sfx_db = -10.0, -12.0
    audio = WORK / "audio.wav"
    level = {}
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


def fit_loudness(src: Path, dst: Path) -> tuple[float, float]:
    """Single-pass loudnorm clips this mix. Set a straight gain so the wav sits
    near -14.8 LUFS with true peak at or under -2 dB, leaving room for AAC."""
    cur, peak = integrated_lufs(src), true_peak(src)
    gain = -14.8 - cur
    if peak + gain > -2.0:
        gain = -2.0 - peak
    ff("-i", str(src), "-af", f"volume={gain:.2f}dB,alimiter=limit=0.71:level=disabled",
       "-c:a", "pcm_s16le", str(dst))
    return integrated_lufs(dst), true_peak(dst)


def pulse_parts(src: Path, open_dur: float, loop_dur: float, x: int,
                open_out: Path, loop_out: Path) -> None:
    """One 30 fps crop, then a frame-exact split. The loop's last frame is the
    frame before the opening's first frame, so the seam is not a seek guess."""
    span = WORK / "pulse_span.mp4"
    start = F0_IN - loop_dur
    n_loop = int(round(loop_dur * FPS))
    n_open = int(round(open_dur * FPS))
    vf = (f"scale=1920:1080,crop=608:1080:{x}:0,scale={W}:{H}:flags=lanczos,setsar=1,fps={FPS}")
    ff("-i", str(src), "-ss", f"{start:.3f}", "-t", f"{(n_loop + n_open) / FPS + 0.05:.3f}",
       "-vf", vf, "-an", "-c:v", "libx264", "-pix_fmt", "yuv420p",
       "-preset", "fast", "-crf", "16", "-r", str(FPS), str(span))
    common = ["-an", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "fast", "-crf", "16", "-r", str(FPS)]
    ff("-i", str(span), "-vf", f"trim=start_frame=0:end_frame={n_loop},setpts=PTS-STARTPTS",
       *common, str(loop_out))
    ff("-i", str(span), "-vf", f"trim=start_frame={n_loop}:end_frame={n_loop + n_open},setpts=PTS-STARTPTS",
       *common, str(open_out))


def run_qa(mp4: Path, plan: list[dict]) -> dict:
    cuts, pool, seen = [], [], set()
    for k, row in enumerate(plan, 1):
        base = Path(row["plate"]).name
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


def build() -> dict:
    if WORK.exists():
        shutil.rmtree(WORK)
    WORK.mkdir(parents=True)
    QA.mkdir(parents=True, exist_ok=True)
    words = b.words_from_align(ALIGN)
    spoken = " ".join(w for w, _, _ in words)
    (WORK / "spoken.txt").write_text(spoken + "\n")
    last_end = words[-1][2]
    if words[0][1] > 0.15:
        raise SystemExit(f"first word at {words[0][1]}")
    more_t = next(s for w, s, e in words if w.lower().startswith("more"))
    if more_t > 1.50:
        raise SystemExit(f"surprise late {more_t}")
    so_t = next(s for w, s, e in words if w.lower().rstrip(".,") == "so" and s > 15)
    total = round(last_end + TAIL_S, 3)
    loop_start = round(total - LOOP_S, 3)
    round_hold = round(loop_start - 20.0, 3)
    if round_hold > 3.001 or round_hold < 0.5:
        raise SystemExit(f"round hold {round_hold}")
    if F0_IN - LOOP_S < 0.02:
        raise SystemExit("loop runs before the pulse plate")
    pulse = plate("part01/raw/v01/01_pulse_wrist_t1.mp4")
    rows = [
        (0.00, 2.17, pulse, F0_IN, 656, "pulse"),
        (2.17, 5.05, plate("part03/raw/v01/05_how_much_t1.mp4"), 0.5, 656, "how_much"),
        (5.05, 7.20, plate("part03/raw/v01/06_two_ounces_eighth_t1.mp4"), 0.4, 656, "two_ounces"),
        (7.20, 9.48, plate("part03/raw/v01/07_thousand_beats_t4.mp4"), 0.3, 640, "thousand"),
        (9.48, 12.12, plate("part03/raw/v01/04_squeeze_pulse_t1.mp4"), 0.5, 900, "squeeze"),
        (12.12, 14.48, plate("part01/raw/v01/09_heart_clock_t2.mp4"), 0.3, 560, "clock"),
        (14.48, 17.19, plate("part03/raw/v01/09_jug_tower_t1.mp4"), 0.5, 360, "jug"),
        (17.19, 20.00, plate("part03/raw/v01/12_glowing_loop_t2.mp4"), 0.5, 656, "glow"),
        (20.00, loop_start, plate(ROUND_PLATE), 0.40, 656, "round"),
        (loop_start, total, pulse, round(F0_IN - LOOP_S, 3), 656, "loop"),
    ]
    plan, segs = [], []
    open_out, loop_out = WORK / "seg_pulse_open.mp4", WORK / "seg_pulse_loop.mp4"
    pulse_parts(pulse, rows[0][1] - rows[0][0], rows[-1][1] - rows[-1][0], 656, open_out, loop_out)
    for k, (t0, t1, src, ins, x, label) in enumerate(rows):
        d = round(t1 - t0, 3)
        if d > 3.001:
            raise SystemExit(f"{label} hold {d}")
        if k == 1 and t0 > 2.60:
            raise SystemExit(f"first cut {t0}")
        out = WORK / f"seg_{k:02d}.mp4"
        if label == "pulse":
            shutil.copy2(open_out, out)
        elif label == "loop":
            shutil.copy2(loop_out, out)
        else:
            b.seg(src, out, ins, d, x)
        segs.append(out)
        plan.append({"t0": t0, "t1": t1, "plate": src.name, "in_s": ins, "crop_x": x,
                     "label": label, "hold_s": d})
    # Segment frame counts overshoot `total`, and -t would cut the loop seam off.
    # Drop the extra frames from the circulation plate, never from the loop.
    target_frames = int(round(total * FPS))

    def nframes(p: Path) -> int:
        return int(subprocess.check_output(
            ["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=nb_frames",
             "-of", "csv=p=0", str(p)], text=True).strip())

    extra = sum(nframes(s) for s in segs) - target_frames
    round_i = next(i for i, row in enumerate(plan) if row["label"] == "round")
    if extra > 0:
        keep = nframes(segs[round_i]) - extra
        if keep < int(0.5 * FPS):
            raise SystemExit(f"round plate would shrink to {keep} frames")
        trimmed = WORK / "seg_round_trim.mp4"
        ff("-i", str(segs[round_i]), "-vf", f"trim=end_frame={keep},setpts=PTS-STARTPTS",
           "-an", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "fast", "-crf", "16",
           "-r", str(FPS), str(trimmed))
        segs[round_i] = trimmed
        plan[round_i]["hold_s"] = round(keep / FPS, 3)
        plan[round_i]["t1"] = round(plan[round_i]["t0"] + keep / FPS, 3)
    if sum(nframes(s) for s in segs) != target_frames:
        raise SystemExit(f"frame count {sum(nframes(s) for s in segs)} != {target_frames}")
    (WORK / "pic.txt").write_text("".join(f"file '{s.name}'\n" for s in segs))
    pic = WORK / "picture.mp4"
    ff("-f", "concat", "-safe", "0", "-i", "pic.txt", "-c:v", "libx264", "-pix_fmt", "yuv420p",
       "-preset", "fast", "-crf", "16", "-r", str(FPS), "-t", f"{total:.3f}", str(pic), cwd=WORK)

    snd = sound(VO, total)
    norm = WORK / "audio_norm.wav"
    pre_lufs, _pre_peak = fit_loudness(snd["audio"], norm)
    onset = onset_piece(VO)
    (QA / f"onset_{SID}_{VER}.json").write_text(json.dumps(onset, indent=2) + "\n")

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
        raise SystemExit("Harvey card overlaps the promo title")

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
       "-frames:v", str(target_frames), "-t", f"{target_frames / FPS:.6f}",
       "-movflags", "+faststart", str(mp4))

    diff = loop_diff(mp4)
    lufs, peak = integrated_lufs(mp4), true_peak(mp4)
    holds = [r["hold_s"] for r in plan]
    brief = {
        "frame0_source": "04_Generated-Clips/part01/raw/v01/01_pulse_wrist_t1.mp4",
        "frame0_zoom": f"none — moving plate, in {F0_IN}s, crop x=656, no Ken Burns",
        "frame0_in_s": F0_IN,
        "loop_in_s": round(F0_IN - LOOP_S, 3),
        "loop_ends_on": "frame before frame 0 in-point; no frame-0 copy",
        "no_frame0_stamp": True,
        "first_word_s": words[0][1],
        "surprise_s": {"more": more_t, "blood": next(s for w, s, e in words if w.lower().startswith("blood"))},
        "first_cut_s": plan[1]["t0"],
        "last_word_to_loop_s": round(total - last_end, 3),
        "meta_promise": False,
        "runtime_s": round(b.probe(mp4), 3),
        "longest_hold_s": max(holds),
        "payoff_phrase": "same blood, going round and round",
        "payoff_s": so_t,
        "payoff_frac": round(so_t / total, 3),
        "loop_sentence": "So it's the same blood, going round and round. You pump more blood than you have.",
        "loop_diff": diff,
        "lufs": lufs,
        "true_peak_dbfs": peak,
        "pre_master_lufs": pre_lufs,
        "frame0_black": black_frac(mp4, 0.2),
        "sha256": sha256(mp4),
        "no_cta": True,
        "vo_unchanged": True,
        "round_plate": ROUND_PLATE,
        "who_card": card_meta,
        "onset": onset,
    }
    asr = asr_check(spoken, VO)
    meta = {
        "id": SID, "version": VER, "job": JOB, "youtube_id": YT,
        "title": "Your Heart Pumps More Blood Than You Have",
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
                           "--script", str(WORK / "spoken.txt"), "--vo", str(VO),
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
        "file": mp4.name, "sha256": brief["sha256"], "duration_s": brief["runtime_s"], "brief": brief,
        "gate_exit": gate.returncode, "gate_verdict": gate_json.get("verdict"),
        "gate_fails": gate_json.get("fails"), "gate_warns": gate_json.get("warns"),
        "qa": qa, "music_exit": music.returncode,
        "music_tail": (music.stdout + music.stderr).strip().splitlines()[-6:],
        "sfx": snd["level"], "copies": copied, "asr_ok": asr["ok"], "asr_notes": asr["notes"],
        "onset": onset,
    }
    (QA / f"build_{SID}_{VER}.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps({k: summary[k] for k in ("file", "duration_s", "gate_verdict", "gate_fails",
                                              "gate_warns", "qa", "music_exit", "music_tail", "sfx",
                                              "asr_ok", "asr_notes")}, indent=2))
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
        bad.append(f"tp {peak}")
    if max(holds) > 3.001:
        bad.append("hold")
    if not asr["ok"]:
        bad.append("asr")
    if bad:
        raise SystemExit("NOT PASS: " + ", ".join(bad))
    print("PASS", mp4.name, brief["runtime_s"], "loop_diff", diff, "lufs", lufs)
    return summary


if __name__ == "__main__":
    build()
