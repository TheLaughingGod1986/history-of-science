#!/usr/bin/env python3
"""HOS 004 gold-foil Short v02 (J0965, £0). v01 is not opened for write.

Audit fix #6 (STAYED60_UPCOMING_AUDIT_2026-10-25.md) plus the batch HB rules:
pause-trim the existing fin wav (no new TTS), first cut by 2.75 s, split the
three holds over 4 s, drop the "watch the full film" line, 1.0 s matched loop.
Runtime lands in 22–25 s. Plates are the KEEP Veo files already on the NAS.
05_flash_in_dark_v01.mp4 is not on disk; the thin-gold plate covers that split.

    python3 _build_backcat_gold_foil_v02.py
"""
from __future__ import annotations

import hashlib
import json
import math
import re
import shutil
import struct
import subprocess
import sys
import wave
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import _build_backcat_nov_v01 as bc  # noqa: E402

REPO = bc.REPO
MEDIA = bc.MEDIA
PROJ = MEDIA / "02_Video-Projects/004_Whats-Really-Inside-An-Atom"
NAS = Path("/Volumes/data/mac-mini-archive/2026-10-24/YouTube/History Of Science/"
           "02_Video-Projects/004_Whats-Really-Inside-An-Atom")
CLIPS = NAS / "04_Generated-Clips/part04/raw/v01"
VO_SRC = NAS / "10_Shorts/vo_backcat_v01/hos_004_backcat_gold_foil_vo_v01_fin.wav"
ALIGN_SRC = NAS / "10_Shorts/vo_backcat_v01/hos_004_backcat_gold_foil_vo_v01_fin_align.json"
OWB = Path("/Users/benjaminoats/YouTube/orbit-with-ben")
WORK = HERE / "_work_gold_foil_v02"
QA = HERE / "qa_gold_foil_v02"
SID, VER, JOB = "gold_foil", "v02", "J0965"
AIR, YT = "2026-11-01", "JyRjM-9Yc8g"
W, H, FPS = bc.W, bc.H, bc.FPS
LOOP_S = 1.00
FIRST_CUT = 2.75
HOLD_MAX = 3.80
MAX_PAUSE, MIN_TRIM = 0.15, 0.45
F0_IN, F0_CROP = 1.50, 560
HOOK = "IT CAME **BACK**"
TITLE = "What's Really Inside an Atom?"
SPOKEN = (
    "Tiny particles bounced back off gold foil. In nineteen-oh-nine, Rutherford's team "
    "fired tiny particles at gold thinner than paper. Almost all went straight through. "
    "About one in eight thousand bounced back. Rutherford said it was like firing a shell "
    "at tissue paper, and it came back and hit you. An atom's mass sits almost all in one "
    "tiny centre: the nucleus."
)

# (word index the plate lands on, or 0 / "loop"), file, in-point, crop x, sha prefix or ""
# Word indexes are the v01 fin alignment. Times are remapped after the pause trim.
BEATS = [
    (0, "12_shell_comes_back_v02.mp4", F0_IN, F0_CROP, "3764483d"),
    ("first", "03_fire_at_gold_v01.mp4", 0.50, 640, "d64e1b33"),       # 2.75 s, through "fired"
    (11, "04_thin_gold_foil_v01.mp4", 0.40, 656, ""),                  # fired … paper
    (19, "09_almost_all_pass_v02.mp4", 3.00, 520, "c73023c9"),         # Almost all went straight through
    (24, "07_green_flash_count_v02.mp4", 0.10, 656, "3c388ef1"),       # About one in eight thousand
    (31, "11_shell_tissue_v02.mp4", 1.20, 900, "78ee7164"),            # Rutherford said …
    (42, "10_one_bounces_v02.mp4", 0.40, 656, ""),                     # and it came back
    (49, "13_mass_packed_v02.mp4", 2.55, 656, "a770491d"),             # An atom's mass
    (56, "14_nucleus_electrons_v01.mp4", 0.80, 656, ""),               # one tiny centre: the nucleus
    ("loop", "12_shell_comes_back_v02.mp4", F0_IN - LOOP_S, F0_CROP, "3764483d"),
]
GREEN_MAX_OUT = 3.45


def ff(*a: str, cwd: Path | None = None) -> None:
    subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", *a], check=True, cwd=cwd)


def sha256(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def silences(wav: Path, dur: float) -> list[tuple[float, float]]:
    err = subprocess.run(
        ["ffmpeg", "-hide_banner", "-nostats", "-i", str(wav),
         "-af", "silencedetect=n=-42dB:d=0.18", "-f", "null", "-"],
        capture_output=True, text=True).stderr
    st = [float(x) for x in re.findall(r"silence_start: (-?[\d.]+)", err)]
    en = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", err)]
    if len(en) < len(st):
        en.append(dur)
    return [(max(0.0, a), b) for a, b in zip(st, en)]


def tighten(src: Path, align: Path, dst: Path, align_out: Path) -> tuple[list[tuple[float, float]], float]:
    """Cap inter-sentence silences over 0.45 s to 0.15 s. Words stay in one piece."""
    d = bc.probe(src)
    keep, cur = [], 0.0
    for a, b in silences(src, d):
        if b - a < MIN_TRIM or a <= 0.02 or b >= d - 0.02:
            continue
        keep.append((cur, a + MAX_PAUSE / 2))
        cur = b - MAX_PAUSE / 2
    if cur < d - 0.001:
        keep.append((cur, d))
    if not keep:
        keep = [(0.0, d)]

    def remap(t: float) -> float:
        out = 0.0
        for a, b in keep:
            if t <= a:
                return out
            if t <= b:
                return out + (t - a)
            out += b - a
        return out

    parts = "".join(
        f"[0:a]atrim={a:.4f}:{b:.4f},asetpts=PTS-STARTPTS[s{i}];" for i, (a, b) in enumerate(keep))
    fc = parts + "".join(f"[s{i}]" for i in range(len(keep))) + f"concat=n={len(keep)}:v=0:a=1[a]"
    ff("-i", str(src), "-filter_complex", fc, "-map", "[a]", "-c:a", "pcm_s16le", "-ar", "48000", "-ac", "2", str(dst))
    al = json.loads(align.read_text())
    al["character_start_times_seconds"] = [round(remap(t), 4) for t in al["character_start_times_seconds"]]
    al["character_end_times_seconds"] = [round(remap(t), 4) for t in al["character_end_times_seconds"]]
    align_out.write_text(json.dumps(al) + "\n")
    saved = round(d - bc.probe(dst), 3)
    return keep, saved


def plate(name: str, prefix: str) -> Path:
    p = CLIPS / name
    if not p.exists() or p.stat().st_size < 1000:
        raise SystemExit(f"missing plate {p}")
    digest = sha256(p)
    if prefix and not digest.startswith(prefix):
        raise SystemExit(f"{name}: sha {digest[:8]} is not KEEP {prefix}")
    return p


def seg(src: Path, dst: Path, start: float, dur: float, x: int) -> None:
    if start < 0 or start + dur > bc.probe(src) - 0.04:
        raise SystemExit(f"{src.name}: in {start:.2f} + {dur:.2f} runs past the plate")
    vf = f"scale=1920:1080,crop=608:1080:{x}:0,scale={W}:{H}:flags=lanczos,setsar=1,fps={FPS}"
    ff("-ss", f"{start:.3f}", "-i", str(src), "-t", f"{dur:.3f}", "-vf", vf, "-an",
       "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "veryfast", "-crf", "18", "-r", str(FPS), str(dst))


def synth_bed(path: Path, dur: float, sr: int = 48000) -> None:
    """Soft mallet figure at 72 BPM. Not the part-04 pad and not the 005 sum pulse."""
    n = int(sr * dur)
    roots = [110.00, 130.81, 164.81, 196.00]
    frames = bytearray()
    for i in range(n):
        t = i / sr
        beat = (72 / 60) * t
        step = int(beat) % 4
        phase = beat - int(beat)
        env = math.exp(-3.2 * phase) * min(1.0, t / 0.4) * min(1.0, max(0.0, (dur - t) / 0.35))
        f0 = roots[step]
        l = r = 0.0
        for k, mul in enumerate((1.0, 2.0, 3.0)):
            a = (0.55, 0.22, 0.08)[k]
            l += math.sin(2 * math.pi * f0 * mul * t) * a
            r += math.sin(2 * math.pi * f0 * mul * 1.004 * t + 0.3) * a
        g = env * 0.22
        frames += struct.pack("<hh", int(max(-1, min(1, l * g)) * 32767),
                              int(max(-1, min(1, r * g)) * 32767))
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
        delay = int(t * 1000)
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
    cur, peak = integrated_lufs(src), true_peak(src)
    gain = -14.8 - cur
    if peak + gain > -2.0:
        gain = -2.0 - peak
    ff("-i", str(src), "-af", f"volume={gain:.2f}dB,alimiter=limit=0.71:level=disabled",
       "-c:a", "pcm_s16le", str(dst))
    return integrated_lufs(dst), true_peak(dst)


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


def build() -> None:
    if WORK.exists():
        shutil.rmtree(WORK)
    WORK.mkdir(parents=True)
    QA.mkdir(parents=True, exist_ok=True)
    vo = WORK / "vo_v02.wav"
    align = WORK / "align_v02.json"
    _keep, saved = tighten(VO_SRC, ALIGN_SRC, vo, align)
    words = bc.words_from_align(align)
    spoken = " ".join(w for w, _, _ in words)
    if spoken != SPOKEN:
        raise SystemExit(f"spoken line changed:\n{spoken}")
    (WORK / "spoken.txt").write_text(spoken + "\n")
    last_end = words[-1][2]
    # Drop the finished-file room tone so the loop gap is exactly LOOP_S.
    vo_trim = WORK / "vo_trim.wav"
    ff("-i", str(vo), "-t", f"{last_end + 0.06:.3f}", "-c:a", "pcm_s16le", str(vo_trim))
    vo = vo_trim
    if words[0][1] > 0.15:
        raise SystemExit(f"first word at {words[0][1]:.3f}")
    bounced = next(s for w, s, _e in words if w.lower().startswith("bounced"))
    if bounced > 1.50:
        raise SystemExit(f"bounced late at {bounced:.3f}")
    nucleus = next(s for w, s, _e in words if w.lower().startswith("nucleus"))
    total = round(last_end + LOOP_S, 3)
    if not 22.0 <= total <= 25.0:
        raise SystemExit(f"runtime {total:.3f}s is outside 22–25 (saved {saved}s on the pauses)")
    if nucleus < 0.70 * total:
        raise SystemExit(f"nucleus at {nucleus:.2f} is before 70% of {total:.2f}")

    cuts = []
    for idx, name, ins, x, pre in BEATS:
        src = plate(name, pre)
        if idx == 0:
            t, label = 0.0, "open"
        elif idx == "first":
            t, label = FIRST_CUT, "fired"
        elif idx == "loop":
            t, label = round(last_end, 3), "loop"
        else:
            t, label = round(words[idx][1], 3), words[idx][0]
        cuts.append({"t": t, "src": src, "in": ins, "x": x, "lands": idx, "label": label})
    cuts.sort(key=lambda c: c["t"])
    plan = []
    for k, c in enumerate(cuts):
        end = cuts[k + 1]["t"] if k + 1 < len(cuts) else total
        dur = round(end - c["t"], 3)
        limit = HOLD_MAX if c["lands"] != "loop" else 1.55
        floor = 1.15 if c["lands"] != "loop" else 0.95
        if not floor <= dur <= limit:
            raise SystemExit(f"hold {c['label']} {c['t']:.2f}-{end:.2f} = {dur:.2f}s")
        if c["src"].name.startswith("07_green") and c["in"] + dur > GREEN_MAX_OUT:
            raise SystemExit(f"green flash would run to {c['in'] + dur:.2f}s")
        plan.append({**c, "t1": round(end, 3), "dur": dur})

    print(f"saved {saved}s  runtime {total:.2f}s  bounced {bounced:.2f}  nucleus {nucleus:.2f} "
          f"({nucleus / total:.0%})")
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

    bed = PROJ / "05_Music" / "hos_004_backcat_gold_foil_v02_bed.wav"
    synth_bed(bed, total + 0.4)
    plan_j = {
        "prompt": ("Quiet mallet figure under a 1909 laboratory telling, even, no chase. "
                   "Pace: 68-76 BPM. NOT hos004-part04-temp_score_bed_v01, NOT the 005 heart-sum pulse, "
                   "NOT any Orbit With Ben bed, NOT a drum loop, NOT a trailer sting."),
        "film": "004", "short": "gold_foil_v02", "job": JOB,
        "source": "own synthesis in _build_backcat_gold_foil_v02.py, 0 credits",
        "pace_bpm": "68-76",
    }
    bed.with_name(bed.stem + "_plan.json").write_text(json.dumps(plan_j, indent=2) + "\n")
    nucleus_t = next(row["t"] for row in plan if row["src"].name.startswith("14_nucleus"))
    sfx = place_sfx(total, [9.05, nucleus_t])
    audio = WORK / "audio.wav"
    level = {}
    bed_db, sfx_db = -12.0, -14.0
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
    pre_lufs, _pre_peak = integrated_lufs(audio), true_peak(audio)
    lufs, peak = fit_loudness(audio, fitted)

    chunks = bc.chunk_words(words)
    overlays = []
    hook_png = WORK / "cap_hook.png"
    hook_meta = bc.render_hook(hook_png, HOOK)
    overlays.append((hook_png, 0.0, 2.40, "hook", HOOK.replace("**", "")))
    for i, c in enumerate(chunks):
        png = WORK / f"cap_{i:03d}.png"
        bc.render(png, c["text"], 52, 330, anchor="bottom")
        overlays.append((png, c["t0"], min(c["t1"], total - 0.05), "vo", c["text"]))
    from PIL import Image, ImageDraw
    title_png = WORK / "cap_title.png"
    bc.render(title_png, TITLE, 62, 250, index=2, stroke=4)
    shade = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    for yy in range(560):
        ImageDraw.Draw(shade).line([(0, yy), (W, yy)], fill=(0, 0, 0, int(150 * (1 - yy / 560) ** 1.5)))
    Image.alpha_composite(shade, Image.open(title_png)).save(title_png)
    overlays.append((title_png, 9.0, 14.0, "title", TITLE))

    inputs = ["-i", str(pic), "-i", str(fitted)]
    for png, *_r in overlays:
        inputs += ["-loop", "1", "-i", str(png)]
    fc, last = [], "[0:v]"
    for i, (_png, t0, t1, *_r) in enumerate(overlays, 2):
        fc.append(f"{last}[{i}:v]overlay=0:0:enable='between(t,{t0:.3f},{t1:.3f})'[v{i}]")
        last = f"[v{i}]"
    mp4 = HERE / "hos_004_backcat_gold_foil_v02.mp4"
    ff(*inputs, "-filter_complex", ";".join(fc), "-map", last, "-map", "1:a",
       "-c:v", "libx264", "-pix_fmt", "yuv420p", "-profile:v", "high", "-preset", "veryfast", "-crf", "18",
       "-r", str(FPS), "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2",
       "-t", f"{total:.3f}", "-movflags", "+faststart", str(mp4))

    out_plan = []
    for row in plan:
        out_plan.append({
            "t0": row["t"], "t1": row["t1"], "plate": row["src"].name, "in_s": row["in"],
            "crop_x": row["x"], "lands_on": row["label"], "hold_s": row["dur"],
        })
    meta = {
        "id": "004_gold_foil", "version": VER, "job": JOB, "youtube_id": YT,
        "title": "Why Gold Foil Bounced Rutherford's Particles Back",
        "air_date": AIR, "spoken": spoken, "script": spoken,
        "words": [{"word": w, "start": round(s, 3), "end": round(e, 3)} for w, s, e in words],
        "word_count": len(words), "last_word_end_s": round(last_end, 3),
        "plan": out_plan, "hook": HOOK.replace("**", ""), "hook_layer": hook_meta,
        "title_on_screen": TITLE, "no_cta": True, "no_new_spend": True,
        "pause_saved_s": saved, "v01_untouched": True,
        "bed": bed.name, "sfx_level": level,
        "frame0_source": "04_Generated-Clips/part04/raw/v01/12_shell_comes_back_v02.mp4",
        "frame0_zoom": "none — moving plate, in 1.5s, crop x=560, no Ken Burns",
        "frame0_in_s": F0_IN,
        "first_word_s": round(words[0][1], 3),
        "surprise_s": {"bounced": round(bounced, 3), "gold": round(next(s for w, s, _e in words if w.lower().startswith("gold")), 3)},
        "first_cut_s": FIRST_CUT,
        "last_word_to_loop_s": LOOP_S,
        "meta_promise": False,
        "runtime_s": round(bc.probe(mp4), 3),
        "longest_hold_s": max(row["dur"] for row in plan if row["lands"] != "loop"),
        "payoff_phrase": "the nucleus",
        "payoff_s": round(nucleus, 3),
        "payoff_frac": round(nucleus / total, 3),
        "loop_sentence": "An atom's mass sits almost all in one tiny centre: the nucleus. Tiny particles bounced back off gold foil.",
        "lufs_wav": round(lufs, 2),
        "true_peak_wav_dbfs": round(peak, 2),
        "pre_master_lufs": round(pre_lufs, 2),
        "frame0_black": black_frac(mp4, 0.15),
        "sha256": sha256(mp4),
        "missing_plate_note": "05_flash_in_dark_v01.mp4 is not on the NAS; 04_thin_gold_foil_v01.mp4 splits the fire-at-gold hold",
    }
    meta_path = HERE / "hos_004_backcat_gold_foil_v02_meta.json"
    meta_path.write_text(json.dumps(meta, indent=2) + "\n")

    gate = subprocess.run(
        [sys.executable, str(REPO / "00_Brand/Channel-Setup/tools/gate_shorts_open.py"),
         "check", str(mp4), "--air-date", AIR, "--id", YT,
         "--script", str(WORK / "spoken.txt"), "--vo", str(vo),
         "--meta", str(meta_path), "--json"],
        capture_output=True, text=True)
    (QA / "gate_gold_foil_v02.txt").write_text((gate.stdout + gate.stderr).strip() + "\n")
    try:
        gate_json = json.loads(gate.stdout)
        if isinstance(gate_json, list):
            gate_json = gate_json[0]
    except json.JSONDecodeError:
        gate_json = {"verdict": "FAIL", "raw": (gate.stdout + gate.stderr)[-2000:]}
    (QA / "gate_gold_foil_v02.json").write_text(json.dumps(gate_json, indent=2) + "\n")
    (QA / "j0918_ship_gate_gold_foil_v02.txt").write_text(
        "J0918 HOS ship gate (Chief, 24 Oct 2026), read from gate_shorts_open.\n"
        f"verdict={gate_json.get('verdict')} frame0_diff={gate_json.get('frame0_diff_0_1_5s')} "
        f"first_cut_s={gate_json.get('first_cut_s')} vo_onset_s={gate_json.get('vo_onset_s')} "
        f"tail_gap_s={gate_json.get('tail_gap_s')} stayed_fails={gate_json.get('stayed_fails')}\n"
        f"fails={gate_json.get('fails')}\nwarns={gate_json.get('warns')}\n"
    )

    cuts_j, pool, seen = [], [], set()
    for k, row in enumerate(plan, 1):
        src_id = f"loop_span_{row['src'].name}" if row["lands"] == "loop" else row["src"].name
        cuts_j.append({
            "row": f"s{k:02d}_{row['label']}", "timeline_in": row["t"], "timeline_out": row["t1"],
            "source": src_id, "upscale": 1.78, "video": True, "framing": {"offset": row["in"]},
        })
        if src_id not in seen:
            seen.add(src_id)
            pool.append({"file_id": src_id, "title": f"Veo plate {row['src'].name}"})
    cuts_f = QA / "cuts_gold_foil_v02.json"
    pool_f = QA / "pool_gold_foil_v02.json"
    cuts_f.write_text(json.dumps(cuts_j, indent=2) + "\n")
    pool_f.write_text(json.dumps(pool, indent=2) + "\n")
    rel = lambda p: str(p.relative_to(REPO))  # noqa: E731
    r_pg = subprocess.run([sys.executable, str(OWB / "scripts/polish_gate.py"), rel(mp4),
                           "--cuts", rel(cuts_f), "--out", rel(QA / "polish_gate_gold_foil_v02.json")],
                          cwd=REPO, capture_output=True, text=True)
    (QA / "polish_gate_gold_foil_v02.txt").write_text((r_pg.stdout + r_pg.stderr).strip() + "\n")
    r_pq = subprocess.run([sys.executable, str(OWB / "scripts/picture_qa.py"), rel(mp4),
                           "--cuts", rel(cuts_f), "--pool", rel(pool_f),
                           "--out-dir", rel(QA / "picture_qa_gold_foil_v02")],
                          cwd=REPO, capture_output=True, text=True)
    (QA / "picture_qa_gold_foil_v02.txt").write_text((r_pq.stdout + r_pq.stderr).strip() + "\n")
    music = subprocess.run([sys.executable, str(OWB / "scripts/music_gate.py"), str(PROJ),
                            "--bed", str(bed), "--video", str(mp4),
                            "--out", str(QA / "music_gate_gold_foil_v02.json")],
                           capture_output=True, text=True)
    (QA / "music_gate_gold_foil_v02.txt").write_text((music.stdout + music.stderr).strip() + "\n")

    phone = HERE / "hos_004_backcat_gold_foil_v02_PHONE.mp4"
    ff("-i", str(mp4), "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "veryfast", "-crf", "26",
       "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart", str(phone))
    sheet = QA / "hos_004_backcat_gold_foil_v02_2fps_sheet.jpg"
    ff("-i", str(mp4), "-vf", "fps=2,scale=180:-2,tile=8x8", "-q:v", "4", str(sheet))
    for name, t in (("frame0", 0.05), ("title", 11.5)):
        ff("-ss", f"{t}", "-i", str(mp4), "-frames:v", "1", "-q:v", "3", str(QA / f"gold_foil_v02_{name}.jpg"))

    uat = Path.home() / "Library/Mobile Documents/com~apple~CloudDocs/HOS UAT/004_Whats-Really-Inside-An-Atom/10_Shorts"
    nas_out = Path("/Volumes/data/mac-mini-archive/YouTube/History Of Science/02_Video-Projects/"
                   "004_Whats-Really-Inside-An-Atom/10_Shorts/gold_foil_v02")
    copied = {}
    for folder in (uat, nas_out):
        for src in (mp4, phone, sheet):
            copied[str(folder / src.name)] = copy_checked(src, folder / src.name)
    manifest = {"job": JOB, "youtube_id": YT, "master_sha256": sha256(mp4), "phone_sha256": sha256(phone),
                "copies": copied}
    (QA / "sha256_manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    (nas_out / "sha256_manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")

    summary = {
        "file": mp4.name, "sha256": sha256(mp4), "duration_s": round(bc.probe(mp4), 3),
        "gate_exit": gate.returncode, "gate_verdict": gate_json.get("verdict"),
        "gate_fails": gate_json.get("fails"), "gate_warns": gate_json.get("warns"),
        "polish_exit": r_pg.returncode, "picture_exit": r_pq.returncode,
        "music_exit": music.returncode,
        "music_tail": (music.stdout + music.stderr).strip().splitlines()[-8:],
        "polish_tail": (r_pg.stdout + r_pg.stderr).strip().splitlines()[-8:],
        "picture_tail": (r_pq.stdout + r_pq.stderr).strip().splitlines()[-8:],
        "sfx": level, "frame0_black": meta["frame0_black"], "lufs_wav": meta["lufs_wav"],
        "longest_hold_s": meta["longest_hold_s"], "payoff_frac": meta["payoff_frac"],
    }
    (QA / "build_gold_foil_v02.json").write_text(json.dumps(summary, indent=2) + "\n")
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
