#!/usr/bin/env python3
"""HOS 005 Short s05 valves v02 (J0965, £0). v01 is not opened for write.

Audit fix #8. The sentence "Inside your veins are tiny one-way doors — valves"
is not on disk, so the open is the existing line "Along the swollen veins…",
with "Now the little doors." dropped and the two pauses over 0.15 s capped.
No new speech. Plates are the Part 04 KEEP takes already on the NAS.
First cut 2.45 s, holds ≤ 3.8 s, no "watch the full film", 1.50 s matched loop.
Runtime lands at 22 s or more, and "towards the heart" stays past 70%.

    python3 _build_short_s05_valves_v02.py
"""
from __future__ import annotations

import hashlib
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

from PIL import Image, ImageDraw, ImageFont  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _build_shorts_v03 as b  # noqa: E402

HERE, PROJ, REPO = b.HERE, b.PROJ, b.REPO
NAS = Path("/Volumes/data/mac-mini-archive/hos-worktrees/2026-10-22/hos-005-blood/"
           "02_Video-Projects/005_How-Harvey-Proved-Blood-Circulates")
RAW = NAS / "02_Voiceover/part04_the_tied_arm_v01_raw.mp3"
ALIGN = NAS / "02_Voiceover/part04_the_tied_arm_v01_raw_align.json"
CLIPS = NAS / "04_Generated-Clips/part04/raw/v01"
OWB = Path("/Users/benjaminoats/YouTube/orbit-with-ben")
WORK = HERE / "_work_s05_valves_v02"
QA = HERE / "qa_s05_valves_v02"
SID, VER, JOB = "s05_valves", "v02", "J0965"
AIR, YT = "2026-11-05", "PlihWC5uA2E"
W, H, FPS = b.W, b.H, b.FPS
LOOP_S = 1.35
FIRST_CUT = 2.45
F0_IN, F0_CROP = 1.60, 656
HOLD_MAX, HOLD_MIN = 3.80, 1.20
HOOK = "ONE **WAY**"
TITLE = "The Tied Arm That Proved Your Blood Circulates"
CARD = ("FABRICIUS", "Padua, c. 1600")
V01 = HERE / "hos_005_s05_valves_v01.mp4"
# Raw spans of words already on the Part 04 take. "Now the little doors." is left out.
# (label, raw start, raw end, plate, in-point, crop, land word)
PIECES = [
    ("along", 48.88, 52.20),
    ("each", 52.26, 56.44),
    ("harvey", 56.52, 61.72),
    ("stops", 61.84, 64.52),
    ("other", 64.66, 69.56),
]
GAPS = [0.13, 0.15, 0.15, 0.15]  # the 0.19 s and 0.21 s joins are capped at 0.15 s
# Picture. Times are filled from the remapped words. land is a word, "open", "cut" or "loop".
BEATS = [
    ("open", "13_one_way_t3.mp4", F0_IN, F0_CROP),
    ("cut", "06_veins_swell_t1.mp4", 2.20, 750),
    ("valve,", "08_knots_valve_t4.mp4", 0.40, 656),
    ("Harvey", "09_push_stops_t3.mp4", 0.50, 800),
    ("pushes", "09_push_stops_t2.mp4", 0.40, 800),
    ("It", "11_two_fingers_t3.mp4", 0.80, 656),
    ("He", "10_slides_heart_t3.mp4", 0.60, 1100),
    ("towards", "10_slides_heart_t2.mp4", 1.00, 656),
    ("loop", "13_one_way_t3.mp4", F0_IN - LOOP_S, F0_CROP),
]


def ff(*a: str, cwd: Path | None = None) -> None:
    subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", *a], check=True, cwd=cwd)


def sha256(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def plate(name: str) -> Path:
    p = CLIPS / name
    if not p.exists() or p.stat().st_size < 1000:
        raise SystemExit(f"missing plate {p}")
    return p


def seg(src: Path, dst: Path, start: float, dur: float, x: int) -> None:
    if start < 0 or start + dur > b.probe(src) - 0.04:
        raise SystemExit(f"{src.name}: in {start:.2f} + {dur:.2f} runs past the plate ({b.probe(src):.2f})")
    vf = f"scale=1920:1080,crop=608:1080:{x}:0,scale={W}:{H}:flags=lanczos,setsar=1,fps={FPS}"
    ff("-ss", f"{start:.3f}", "-i", str(src), "-t", f"{dur:.3f}", "-vf", vf, "-an",
       "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "veryfast", "-crf", "18", "-r", str(FPS), str(dst))


def build_vo(words_src: list[tuple[str, float, float]]) -> tuple[Path, list[tuple[str, float, float]]]:
    """Splice the five spans. Words stay in one piece. No new speech."""
    bits = []
    for i, (_lab, a, b) in enumerate(PIECES):
        bits.append(f"[0:a]atrim={a:.3f}:{b:.3f},asetpts=PTS-STARTPTS,"
                    f"afade=t=in:d=0.004,afade=t=out:st={b - a - 0.012:.3f}:d=0.010[s{i}]")
        if i < len(GAPS):
            bits.append(f"anullsrc=r=48000:cl=stereo,atrim=0:{GAPS[i]:.3f}[g{i}]")
    order = "".join(f"[s{i}]" + (f"[g{i}]" if i < len(GAPS) else "") for i in range(len(PIECES)))
    bits.append(f"{order}concat=n={len(PIECES) + len(GAPS)}:v=0:a=1[a]")
    wav = WORK / "vo_v02.wav"
    ff("-i", str(RAW), "-filter_complex", ";".join(bits), "-map", "[a]", "-c:a", "pcm_s16le", str(wav))
    mapped = []
    out = 0.0
    for i, (_lab, a, b) in enumerate(PIECES):
        for w, s, e in words_src:
            if a - 0.01 <= s and e <= b + 0.02:
                mapped.append((w, round(out + (s - a), 3), round(out + (e - a), 3)))
        out += (b - a)
        if i < len(GAPS):
            out += GAPS[i]
    return wav, mapped


def find_word(words, text: str, which: int = 0) -> float:
    hits = [s for w, s, _e in words if w == text or w.lower().startswith(text.lower())]
    # exact token first
    exact = [s for w, s, _e in words if w.rstrip(",.;:") == text.rstrip(",.;:")]
    use = exact or hits
    if which >= len(use):
        raise SystemExit(f"word {text!r} #{which} not in the stem ({[w for w, _, _ in words]})")
    return use[which]


def synth_bed(path: Path, dur: float, sr: int = 48000) -> None:
    """Low cello fifths at 64 BPM. Not the Part 04 pad, not the gold-foil mallets, not the heart-sum pulse."""
    n = int(sr * dur)
    roots = [73.42, 110.00, 146.83, 98.00]  # D2, A2, D3, G2 — a different figure from the 004 mallet
    frames = bytearray()
    for i in range(n):
        t = i / sr
        beat = (64 / 60) * t
        step = int(beat) % 8
        phase = beat - int(beat)
        if step in (1, 5):
            env = 0.0
        else:
            root = roots[step % 4]
            env = math.exp(-1.6 * phase) * min(1.0, t / 0.5) * min(1.0, max(0.0, (dur - t) / 0.4))
            l = r = 0.0
            for k, mul in enumerate((1.0, 2.0, 3.0, 4.0)):
                a = (0.62, 0.18, 0.08, 0.04)[k]
                l += math.sin(2 * math.pi * root * mul * t) * a
                r += math.sin(2 * math.pi * root * mul * 1.003 * t + 0.4) * a
            g = env * 0.28
            frames += struct.pack("<hh", int(max(-1, min(1, l * g)) * 32767),
                                  int(max(-1, min(1, r * g)) * 32767))
            continue
        frames += struct.pack("<hh", 0, 0)
    path.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(path), "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(sr)
        w.writeframes(bytes(frames))


def place_sfx(total: float, ticks: list[float]) -> Path:
    kit = PROJ / "06_Sound-Effects" / "kit_v01"
    whoosh = kit / "sfx_hos_whoosh_soft_v01.wav"
    tick = kit / "sfx_hos_tick_ink_v01.wav"
    if not whoosh.exists() or not tick.exists():
        subprocess.run([sys.executable, str(OWB / "scripts/sfx_kit.py"), "make",
                        "--out-dir", str(kit), "--house", "hos"], check=True)
    dst = WORK / "sfx_stem.wav"
    inputs = ["-f", "lavfi", "-t", f"{total:.3f}", "-i", "anullsrc=channel_layout=stereo:sample_rate=48000",
              "-i", str(whoosh)]
    fc = ["[1:a]volume=-16dB,afade=t=out:st=0.55:d=0.25[w]"]
    mix_in = ["[0:a]", "[w]"]
    for i, t in enumerate(ticks):
        inputs += ["-i", str(tick)]
        delay = int(max(0.0, t) * 1000)
        fc.append(f"[{i + 2}:a]volume=-10dB,adelay={delay}|{delay}[t{i}]")
        mix_in.append(f"[t{i}]")
    n = len(mix_in)
    fc.append("".join(mix_in) + f"amix=inputs={n}:normalize=0:duration=first,alimiter=limit=0.5[a]")
    ff(*inputs, "-filter_complex", ";".join(fc), "-map", "[a]", "-c:a", "pcm_s16le", str(dst))
    return dst


def mix(vo: Path, bed: Path, sfx: Path, total: float, dst: Path, bed_db: float, sfx_db: float) -> None:
    ff("-i", str(vo), "-i", str(bed), "-i", str(sfx), "-filter_complex",
       f"[0:a]aformat=sample_rates=48000:channel_layouts=stereo,apad=whole_dur={total:.3f}[v];"
       f"[1:a]aformat=sample_rates=48000:channel_layouts=stereo,atrim=0:{total:.3f},volume={bed_db:.2f}dB[b];"
       f"[2:a]aformat=sample_rates=48000:channel_layouts=stereo,atrim=0:{total:.3f},volume={sfx_db:.2f}dB[s];"
       "[v][b][s]amix=inputs=3:normalize=0:duration=first,alimiter=limit=0.89[a]",
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
    """Raise the mix toward -14 LUFS. The limiter holds the true peak; the raw VO peaks early."""
    cur = integrated_lufs(src)
    gain = -14.2 - cur
    ff("-i", str(src), "-af",
       f"volume={gain:.2f}dB,alimiter=limit=0.89:attack=5:release=40:level=disabled",
       "-c:a", "pcm_s16le", str(dst))
    got, peak = integrated_lufs(dst), true_peak(dst)
    if got < -16.0 and peak < -1.5:
        extra = min(-14.2 - got, -1.2 - peak)
        if extra > 0.4:
            ff("-i", str(dst), "-af",
               f"volume={extra:.2f}dB,alimiter=limit=0.89:attack=5:release=40:level=disabled",
               "-c:a", "pcm_s16le", str(dst) + ".2.wav")
            shutil.move(str(dst) + ".2.wav", dst)
            got, peak = integrated_lufs(dst), true_peak(dst)
    return got, peak


def black_frac(mp4: Path, t: float) -> float:
    raw = subprocess.check_output(
        ["ffmpeg", "-v", "error", "-ss", f"{t:.3f}", "-i", str(mp4),
         "-frames:v", "1", "-vf", "scale=160:284", "-f", "rawvideo", "-pix_fmt", "gray", "-"])
    return round(sum(1 for p in raw if p < 18) / max(1, len(raw)), 3)


def copy_checked(src: Path, dst: Path) -> str:
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)
    if sha256(src) != sha256(dst):
        raise SystemExit(f"sha mismatch after copy: {dst}")
    return sha256(dst)


def render_card(path: Path) -> dict:
    size1 = int(608 * 0.12)
    size2 = int(608 * 0.075)
    f1 = ImageFont.truetype(b.FONT, size1, index=2)
    f2 = ImageFont.truetype(b.CTA_FONT, size2)
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    band_top = (H - 608) // 2
    y2 = band_top + 608 - 40
    y1 = y2 - size2 - 18
    shade = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shade)
    top, bot = y1 - size1 - 30, band_top + 608 + 80
    for yy in range(top, bot):
        ramp = min(1.0, (yy - top) / 120, (bot - yy) / 120)
        wgt = 0.5 * (1.0 - math.cos(math.pi * ramp))
        sd.line([(0, yy), (W, yy)], fill=(0, 0, 0, int(140 * wgt)))
    img = Image.alpha_composite(img, shade)
    d = ImageDraw.Draw(img)
    d.text((70, y1), CARD[0], font=f1, anchor="ls", fill=b.YEL, stroke_width=4, stroke_fill=b.INK)
    d.text((70, y2), CARD[1], font=f2, anchor="ls", fill=b.CREAM, stroke_width=3, stroke_fill=b.INK)
    img.save(path)
    return {"name": CARD[0], "line2": CARD[1]}


def build() -> None:
    if not RAW.exists() or not ALIGN.exists():
        raise SystemExit(f"raw VO missing: {RAW}")
    v01_sha = sha256(V01) if V01.exists() else ""
    if WORK.exists():
        shutil.rmtree(WORK)
    WORK.mkdir(parents=True)
    QA.mkdir(parents=True, exist_ok=True)
    src_words = b.words_from_align(ALIGN)
    vo, words = build_vo(src_words)
    spoken = " ".join(w for w, _, _ in words)
    if not spoken.startswith("Along the swollen veins"):
        raise SystemExit(f"open is not the veins line:\n{spoken[:80]}")
    if "little doors" in spoken.lower() or "one-way doors" in spoken.lower():
        raise SystemExit("dropped or missing line leaked into the stem")
    (WORK / "spoken.txt").write_text(spoken + "\n")
    last_end = words[-1][2]
    vo_trim = WORK / "vo_trim.wav"
    ff("-i", str(vo), "-t", f"{last_end + 0.04:.3f}", "-c:a", "pcm_s16le", str(vo_trim))
    vo = vo_trim
    if words[0][1] > 0.15:
        raise SystemExit(f"first word at {words[0][1]:.3f}")
    veins = find_word(words, "veins")
    if veins > 1.50:
        raise SystemExit(f"veins late at {veins:.3f}")
    towards = find_word(words, "towards", 1)  # the payoff, not "towards the hand"
    total = round(last_end + LOOP_S, 3)
    if total < 22.0 or total > 27.0:
        raise SystemExit(f"runtime {total:.3f}s is outside 22–27 (last word {last_end:.3f})")
    if towards < 0.70 * total:
        raise SystemExit(f"towards at {towards:.2f} is before 70% of {total:.2f}")

    cuts = []
    pushes_seen = 0
    for land, name, ins, x in BEATS:
        src = plate(name)
        if land == "open":
            t, label = 0.0, "open"
        elif land == "cut":
            t, label = FIRST_CUT, "knots"
        elif land == "loop":
            t, label = round(last_end, 3), "loop"
        elif land == "pushes":
            t = find_word(words, "pushes", pushes_seen)
            pushes_seen += 1
            label = "pushes"
        elif land == "towards":
            t, label = towards, "towards"
        elif land == "He":
            t, label = find_word(words, "He", 0), "He"
        else:
            t, label = find_word(words, land), land
        cuts.append({"t": round(t, 3), "src": src, "in": ins, "x": x, "label": label})
    cuts.sort(key=lambda c: c["t"])
    plan = []
    for k, c in enumerate(cuts):
        end = cuts[k + 1]["t"] if k + 1 < len(cuts) else total
        dur = round(end - c["t"], 3)
        limit = HOLD_MAX if c["label"] != "loop" else 1.55
        floor = HOLD_MIN if c["label"] != "loop" else 1.20
        if not floor <= dur <= limit:
            raise SystemExit(f"hold {c['label']} {c['t']:.2f}-{end:.2f} = {dur:.2f}s")
        if k == 0 and not (c["t"] == 0 and end <= 3.0):
            raise SystemExit(f"first cut at {end:.2f}")
        plan.append({**c, "t1": round(end, 3), "dur": dur})
    if plan[0]["t1"] > 3.0:
        raise SystemExit(f"first cut {plan[0]['t1']:.2f} > 3")

    print(f"runtime {total:.2f}s  veins {veins:.2f}  towards {towards:.2f} ({towards / total:.0%})")
    print(spoken)
    for row in plan:
        print(f"  {row['t']:6.2f}-{row['t1']:6.2f} {row['dur']:4.2f}s  {row['src'].name}  on {row['label']}")

    segs = []
    for k, row in enumerate(plan):
        out = WORK / f"seg_{k:02d}.mp4"
        seg(row["src"], out, row["in"], row["dur"], row["x"])
        segs.append(out)
    (WORK / "pic.txt").write_text("".join(f"file '{s.name}'\n" for s in segs))
    pic = WORK / "picture.mp4"
    ff("-f", "concat", "-safe", "0", "-i", "pic.txt", "-c", "copy", "-t", f"{total:.3f}", str(pic), cwd=WORK)

    bed = PROJ / "05_Music" / "hos_005_s05_valves_v02_bed.wav"
    synth_bed(bed, total + 0.4)
    plan_j = {
        "prompt": ("Low cello fifths under a close look at a vein, even, no chase. "
                   "Pace: 60-68 BPM. NOT hos005-part04-temp_score_bed_v01, NOT the 004 gold-foil mallet, "
                   "NOT the 005 heart-sum pulse, NOT any Orbit With Ben bed, NOT a drum loop, NOT a trailer sting."),
        "film": "005", "short": "s05_valves_v02", "job": JOB,
        "source": "own synthesis in _build_short_s05_valves_v02.py, 0 credits",
        "pace_bpm": "60-68",
    }
    bed.with_name(bed.stem + "_plan.json").write_text(json.dumps(plan_j, indent=2) + "\n")
    valve_t = find_word(words, "valve,")
    harvey_t = find_word(words, "Harvey")
    sfx = place_sfx(total, [valve_t, harvey_t, towards])
    audio = WORK / "audio.wav"
    level = {}
    bed_db, sfx_db = -14.0, -16.0
    for _ in range(6):
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
        (QA / "sfx_level.txt").write_text(level["output"] + "\n")
        if r.returncode == 0:
            break
        bed_db -= 3.0
        sfx_db -= 3.0
    if level["exit"] != 0:
        raise SystemExit(f"sfx level failed: {level['output']}")
    fitted = WORK / "audio_fit.wav"
    pre_lufs = integrated_lufs(audio)
    lufs, peak = fit_loudness(audio, fitted)

    chunks = b.chunk_words(words)
    overlays = []
    hook_png = WORK / "cap_hook.png"
    hook_meta = b.render_hook(hook_png, HOOK)
    overlays.append((hook_png, 0.0, 2.20, "hook", HOOK.replace("**", "")))
    for i, c in enumerate(chunks):
        png = WORK / f"cap_{i:03d}.png"
        b.render(png, c["text"], 52, 330, anchor="bottom")
        overlays.append((png, c["t0"], min(c["t1"], total - 0.05), "vo", c["text"]))
    title_png = WORK / "cap_title.png"
    b.render(title_png, TITLE, 58, 250, index=2, stroke=4)
    shade = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    for yy in range(560):
        ImageDraw.Draw(shade).line([(0, yy), (W, yy)], fill=(0, 0, 0, int(150 * (1 - yy / 560) ** 1.5)))
    Image.alpha_composite(shade, Image.open(title_png)).save(title_png)
    overlays.append((title_png, 9.0, 14.0, "title", TITLE))
    fab = find_word(words, "Fabricius")
    card_png = WORK / "cap_who.png"
    card_meta = render_card(card_png)
    overlays.append((card_png, fab, min(fab + 3.2, total - 0.2), "who", "FABRICIUS"))

    inputs = ["-i", str(pic), "-i", str(fitted)]
    for png, *_r in overlays:
        inputs += ["-loop", "1", "-i", str(png)]
    fc, last = [], "[0:v]"
    for i, (_png, t0, t1, *_r) in enumerate(overlays, 2):
        fc.append(f"{last}[{i}:v]overlay=0:0:enable='between(t,{t0:.3f},{t1:.3f})'[v{i}]")
        last = f"[v{i}]"
    mp4 = HERE / "hos_005_s05_valves_v02.mp4"
    ff(*inputs, "-filter_complex", ";".join(fc), "-map", last, "-map", "1:a",
       "-c:v", "libx264", "-pix_fmt", "yuv420p", "-profile:v", "high", "-preset", "veryfast", "-crf", "18",
       "-r", str(FPS), "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2",
       "-t", f"{total:.3f}", "-movflags", "+faststart", str(mp4))

    if v01_sha and sha256(V01) != v01_sha:
        raise SystemExit("v01 changed during the build")
    out_plan = [{
        "t0": row["t"], "t1": row["t1"], "plate": row["src"].name, "in_s": row["in"],
        "crop_x": row["x"], "lands_on": row["label"], "hold_s": row["dur"],
    } for row in plan]
    meta = {
        "id": "005_s05_valves", "version": VER, "job": JOB, "youtube_id": YT,
        "title": "Why Do Veins Have Valves?",
        "air_date": AIR, "spoken": spoken, "script": spoken,
        "words": [{"word": w, "start": round(s, 3), "end": round(e, 3)} for w, s, e in words],
        "word_count": len(words), "last_word_end_s": round(last_end, 3),
        "plan": out_plan, "hook": HOOK.replace("**", ""), "hook_layer": hook_meta,
        "title_on_screen": TITLE, "who": card_meta, "no_cta": True, "no_new_spend": True,
        "open_note": ("'Inside your veins are tiny one-way doors — valves' is not on disk. "
                      "Opened on the existing 'Along the swollen veins…' and dropped 'Now the little doors.' "
                      "The 0.19 s and 0.21 s joins are capped at 0.15 s. No words were sped up, so 'valve' "
                      "stays where the take says it."),
        "v01_untouched": True, "v01_sha256": v01_sha,
        "bed": bed.name, "sfx_level": level,
        "frame0_source": "04_Generated-Clips/part04/raw/v01/13_one_way_t3.mp4",
        "frame0_zoom": "none — moving plate, in 1.6s, crop x=656, no Ken Burns",
        "frame0_in_s": F0_IN,
        "first_word_s": round(words[0][1], 3),
        "surprise_s": {"veins": round(veins, 3), "valve": round(find_word(words, "valve,"), 3)},
        "first_cut_s": plan[0]["t1"],
        "last_word_to_loop_s": LOOP_S,
        "meta_promise": False,
        "runtime_s": round(b.probe(mp4), 3),
        "longest_hold_s": max(row["dur"] for row in plan if row["label"] != "loop"),
        "payoff_phrase": "towards the heart",
        "payoff_s": round(towards, 3),
        "payoff_frac": round(towards / total, 3),
        "loop_sentence": "He pushes it the other way, towards the heart, and it slides through easily. Along the swollen veins you can see small knots.",
        "lufs_wav": round(lufs, 2),
        "true_peak_wav_dbfs": round(peak, 2),
        "pre_master_lufs": round(pre_lufs, 2),
        "frame0_black": black_frac(mp4, 0.15),
        "sha256": sha256(mp4),
        "brief": {
            "frame0": "moving 13_one_way_t3, no zoom",
            "subject_named_s": round(veins, 3),
            "first_word_s": round(words[0][1], 3),
            "first_cut_s": plan[0]["t1"],
            "loop_s": LOOP_S,
            "payoff_frac": round(towards / total, 3),
        },
    }
    meta_path = HERE / "hos_005_s05_valves_v02_meta.json"
    meta_path.write_text(json.dumps(meta, indent=2) + "\n")

    gate = subprocess.run(
        [sys.executable, str(REPO / "00_Brand/Channel-Setup/tools/gate_shorts_open.py"),
         "check", str(mp4), "--air-date", AIR, "--id", YT,
         "--script", str(WORK / "spoken.txt"), "--vo", str(vo),
         "--meta", str(meta_path), "--json"],
        capture_output=True, text=True)
    (QA / "gate_s05_valves_v02.txt").write_text((gate.stdout + gate.stderr).strip() + "\n")
    try:
        gate_json = json.loads(gate.stdout)
        if isinstance(gate_json, list):
            gate_json = gate_json[0]
    except json.JSONDecodeError:
        gate_json = {"verdict": "FAIL", "raw": (gate.stdout + gate.stderr)[-2000:]}
    (QA / "gate_s05_valves_v02.json").write_text(json.dumps(gate_json, indent=2) + "\n")
    (QA / "j0918_ship_gate_s05_valves_v02.txt").write_text(
        "J0918 HOS ship gate (Chief, 24 Oct 2026), read from gate_shorts_open.\n"
        f"verdict={gate_json.get('verdict')} frame0_diff={gate_json.get('frame0_diff_0_1_5s')} "
        f"first_cut_s={gate_json.get('first_cut_s')} vo_onset_s={gate_json.get('vo_onset_s')} "
        f"tail_gap_s={gate_json.get('tail_gap_s')} stayed_fails={gate_json.get('stayed_fails')}\n"
        f"fails={gate_json.get('fails')}\nwarns={gate_json.get('warns')}\n"
    )

    cuts_j, pool, seen = [], [], set()
    for k, row in enumerate(plan, 1):
        src_id = f"loop_span_{row['src'].name}" if row["label"] == "loop" else row["src"].name
        cuts_j.append({
            "row": f"s{k:02d}_{row['label']}", "timeline_in": row["t"], "timeline_out": row["t1"],
            "source": src_id, "upscale": 1.78, "video": True, "framing": {"offset": row["in"]},
        })
        if src_id not in seen:
            seen.add(src_id)
            pool.append({"file_id": src_id, "title": f"Veo plate {row['src'].name}"})
    cuts_f = QA / "cuts_s05_valves_v02.json"
    pool_f = QA / "pool_s05_valves_v02.json"
    cuts_f.write_text(json.dumps(cuts_j, indent=2) + "\n")
    pool_f.write_text(json.dumps(pool, indent=2) + "\n")
    rel = lambda p: str(p.relative_to(REPO))  # noqa: E731
    r_pg = subprocess.run([sys.executable, str(OWB / "scripts/polish_gate.py"), rel(mp4),
                           "--cuts", rel(cuts_f), "--out", rel(QA / "polish_gate_s05_valves_v02.json")],
                          cwd=REPO, capture_output=True, text=True)
    (QA / "polish_gate_s05_valves_v02.txt").write_text((r_pg.stdout + r_pg.stderr).strip() + "\n")
    r_pq = subprocess.run([sys.executable, str(OWB / "scripts/picture_qa.py"), rel(mp4),
                           "--cuts", rel(cuts_f), "--pool", rel(pool_f),
                           "--out-dir", rel(QA / "picture_qa_s05_valves_v02")],
                          cwd=REPO, capture_output=True, text=True)
    (QA / "picture_qa_s05_valves_v02.txt").write_text((r_pq.stdout + r_pq.stderr).strip() + "\n")
    music = subprocess.run([sys.executable, str(OWB / "scripts/music_gate.py"), str(PROJ),
                            "--bed", str(bed), "--video", str(mp4),
                            "--out", str(QA / "music_gate_s05_valves_v02.json")],
                           capture_output=True, text=True)
    (QA / "music_gate_s05_valves_v02.txt").write_text((music.stdout + music.stderr).strip() + "\n")

    phone = HERE / "hos_005_s05_valves_v02_PHONE.mp4"
    ff("-i", str(mp4), "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "veryfast", "-crf", "26",
       "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart", str(phone))
    sheet = QA / "hos_005_s05_valves_v02_2fps_sheet.jpg"
    ff("-i", str(mp4), "-vf", "fps=2,scale=180:-2,tile=8x8", "-q:v", "4", str(sheet))
    for name, t in (("frame0", 0.05), ("title", 11.0)):
        ff("-ss", f"{t}", "-i", str(mp4), "-frames:v", "1", "-q:v", "3", str(QA / f"s05_valves_v02_{name}.jpg"))

    uat = Path.home() / "Library/Mobile Documents/com~apple~CloudDocs/HOS UAT/005_How-Harvey-Proved-Blood-Circulates/10_Shorts/valves_v02"
    nas_out = Path("/Volumes/data/mac-mini-archive/YouTube/History Of Science/02_Video-Projects/"
                   "005_How-Harvey-Proved-Blood-Circulates/10_Shorts/valves_v02")
    copied = {}
    for folder in (uat, nas_out):
        for src in (mp4, phone, sheet):
            copied[str(folder / src.name)] = copy_checked(src, folder / src.name)
    manifest = {"job": JOB, "youtube_id": YT, "master_sha256": sha256(mp4), "phone_sha256": sha256(phone),
                "v01_sha256": sha256(V01), "copies": copied}
    (QA / "sha256_manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    (nas_out / "sha256_manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    meta["sha256"] = sha256(mp4)
    meta["frame0_black"] = black_frac(mp4, 0.15)
    meta_path.write_text(json.dumps(meta, indent=2) + "\n")

    summary = {
        "file": mp4.name, "sha256": sha256(mp4), "duration_s": round(b.probe(mp4), 3),
        "gate_exit": gate.returncode, "gate_verdict": gate_json.get("verdict"),
        "gate_fails": gate_json.get("fails"), "gate_warns": gate_json.get("warns"),
        "polish_exit": r_pg.returncode, "picture_exit": r_pq.returncode,
        "music_exit": music.returncode,
        "music_tail": (music.stdout + music.stderr).strip().splitlines()[-6:],
        "polish_tail": (r_pg.stdout + r_pg.stderr).strip().splitlines()[-6:],
        "picture_tail": (r_pq.stdout + r_pq.stderr).strip().splitlines()[-8:],
        "sfx": level, "frame0_black": meta["frame0_black"], "lufs_wav": meta["lufs_wav"],
        "longest_hold_s": meta["longest_hold_s"], "payoff_frac": meta["payoff_frac"],
        "veins_s": round(veins, 3), "v01_sha": sha256(V01),
    }
    (QA / "build_s05_valves_v02.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))
    bad = []
    if summary["gate_verdict"] != "PASS":
        bad.append("gate")
    if r_pg.returncode != 0:
        bad.append("polish")
    if r_pq.returncode != 0:
        bad.append("picture")
    if music.returncode != 0:
        bad.append("music")
    if bad:
        raise SystemExit("FAIL " + ",".join(bad))


if __name__ == "__main__":
    build()
