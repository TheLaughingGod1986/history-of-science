#!/usr/bin/env python3
"""HOS 005 Short s01 v03 (J0934, £0 picture re-cut of 1lszTrYRp-8).

No VO edit. The finished v01_fin wav is reused as recorded. Picture only:
the 5.05–9.48 s hold on 07_thousand_beats_t4 is split at 7.20 s. The first
half uses part03 06_two_ounces_eighth_t1 (the minted plate; the audit's
06_two_ounces_t1 name is this file). No "watch the full film" overlay.
Audio tail stays 0.57 s. The last frame is the frame-0 pulse plate.

    python3 _build_short_s01_the_sum_v03.py
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

from PIL import Image, ImageDraw, ImageFilter  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _build_shorts_v03 as b  # noqa: E402

HERE, PROJ, REPO = b.HERE, b.PROJ, b.REPO
SID, VER, JOB = "s01_the_sum", "v03", "J0934"
AIR, YT = "2026-10-30", "1lszTrYRp-8"
TAIL_S = 0.57
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


def ff(*a: str, cwd: Path | None = None) -> None:
    subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", *a], check=True, cwd=cwd)


def plate(rel: str) -> Path:
    p = CLIPS / rel
    if not p.exists() or p.stat().st_size < 1000:
        raise SystemExit(f"missing plate {p}")
    return p


def synth_bed(path: Path, dur: float, sr: int = 48000) -> None:
    """Own pad. Not the Part 03 ElevenLabs bed, and not an Orbit bed."""
    n = int(sr * dur)
    freqs = [82.41, 123.47, 196.00, 246.94, 329.63]
    amps = [0.32, 0.24, 0.16, 0.11, 0.07]
    frames = bytearray()
    for i in range(n):
        t = i / sr
        pulse = 0.84 + 0.16 * math.sin(2 * math.pi * (70 / 60) * t)
        env = min(1.0, t / 0.4) * min(1.0, max(0.0, (dur - t) / 0.35))
        l = r = 0.0
        for k, (f, a) in enumerate(zip(freqs, amps)):
            l += math.sin(2 * math.pi * f * t + 0.3 * k) * a
            r += math.sin(2 * math.pi * (f * 1.002) * t + 0.5 * k) * a
        g = env * pulse * 0.20
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
    if not whoosh.exists():
        subprocess.run([sys.executable, str(OWB / "scripts/sfx_kit.py"), "make",
                        "--out-dir", str(kit), "--house", "hos"], check=True)
    dst = WORK / "sfx_stem.wav"
    ff("-f", "lavfi", "-t", f"{total:.3f}", "-i", "anullsrc=channel_layout=stereo:sample_rate=48000",
       "-i", str(whoosh), "-filter_complex",
       "[1:a]volume=-16dB,afade=t=out:st=0.7:d=0.2[w];"
       "[0:a][w]amix=inputs=2:normalize=0:duration=first,alimiter=limit=0.5[a]",
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


def force_last_frame(pic: Path, total: float) -> None:
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


def sound(vo: Path, total: float) -> dict:
    bed = PROJ / "05_Music" / f"hos_005_{SID}_{VER}_bed.wav"
    synth_bed(bed, total + 0.2)
    plan = {
        "prompt": ("Low warm pulse under a spoken sum, even and quiet, no chase. "
                   "Pace: 66-76 BPM. NOT the 005 Part 03 harpsichord bed, NOT any Orbit With Ben bed, "
                   "NOT a drum loop, NOT a trailer sting."),
        "film": "005", "short": f"{SID}_{VER}", "job": JOB,
        "source": "own synthesis in _build_short_s01_the_sum_v03.py, 0 credits",
    }
    bed.with_name(bed.stem + "_plan.json").write_text(json.dumps(plan, indent=2) + "\n")
    sfx = place_sfx(total)
    QA.mkdir(parents=True, exist_ok=True)
    bed_db, sfx_db = -8.0, -8.0
    audio = WORK / "audio.wav"
    level = {}
    for _ in range(4):
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


def run_qa(mp4: Path, plan: list[dict]) -> dict:
    cuts, pool, seen = [], [], set()
    for k, row in enumerate(plan, 1):
        base = Path(row["plate"]).name
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
    return {"polish_gate": {"exit": r_pg.returncode, "tail": (r_pg.stdout + r_pg.stderr).strip().splitlines()[-4:]},
            "picture_qa": {"exit": r_pq.returncode, "tail": (r_pq.stdout + r_pq.stderr).strip().splitlines()[-6:]}}


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
    total = round(last_end + TAIL_S, 3)
    # v02 beat times (word start − 0.15), with the 5.05–9.48 hold split at 7.20.
    pulse = plate("part01/raw/v01/01_pulse_wrist_t1.mp4")
    rows = [
        (0.00, 2.17, pulse, 1.0, 656, "pulse"),
        (2.17, 5.05, plate("part03/raw/v01/05_how_much_t1.mp4"), 0.5, 656, "how_much"),
        (5.05, 7.20, plate("part03/raw/v01/06_two_ounces_eighth_t1.mp4"), 0.4, 656, "two_ounces"),
        (7.20, 9.48, plate("part03/raw/v01/07_thousand_beats_t4.mp4"), 0.3, 640, "thousand"),
        (9.48, 12.12, plate("part03/raw/v01/04_squeeze_pulse_t1.mp4"), 0.5, 900, "squeeze"),
        (12.12, 14.48, plate("part01/raw/v01/09_heart_clock_t2.mp4"), 0.3, 560, "clock"),
        (14.48, 17.19, plate("part03/raw/v01/09_jug_tower_t1.mp4"), 0.5, 360, "jug"),
        (17.19, round(total - 3.80, 3), plate("part03/raw/v01/12_glowing_loop_t2.mp4"), 0.5, 656, "glow"),
        (round(total - 3.80, 3), total, pulse, 1.0, 656, "loop"),
    ]
    plan, segs = [], []
    for k, (t0, t1, src, ins, x, label) in enumerate(rows):
        d = round(t1 - t0, 3)
        if d > 4.0:
            raise SystemExit(f"{label} hold {d}")
        if k == 1 and t0 > 3.0:
            raise SystemExit(f"first cut {t0}")
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

    snd = sound(VO, total)
    norm = WORK / "audio_norm.wav"
    ff("-i", str(snd["audio"]), "-af", "loudnorm=I=-14:TP=-1.5:LRA=11", "-c:a", "pcm_s16le", str(norm))

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

    inputs = ["-i", str(pic), "-i", str(norm)]
    for png, *_ in overlays:
        inputs += ["-loop", "1", "-i", str(png)]
    fc, last = [], "[0:v]"
    for i, (_, t0, t1) in enumerate(overlays, 2):
        fc.append(f"{last}[{i}:v]overlay=0:0:enable='between(t,{t0:.3f},{t1:.3f})'[v{i}]")
        last = f"[v{i}]"
    mp4 = HERE / f"hos_005_{SID}_{VER}.mp4"
    ff(*inputs, "-filter_complex", ";".join(fc), "-map", last, "-map", "1:a",
       "-c:v", "libx264", "-pix_fmt", "yuv420p", "-profile:v", "high", "-preset", "medium", "-crf", "18",
       "-r", str(FPS), "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2",
       "-t", f"{total:.3f}", "-movflags", "+faststart", str(mp4))
    # Stamp the picture's frame 0 onto the finished last frame, after captions.
    stamped = WORK / "stamped.mp4"
    nframes = int(round(total * FPS))
    # A still input has one frame, so loop it and cover the last two frames.
    ff("-i", str(mp4), "-loop", "1", "-i", str(WORK / "frame0_pic.png"), "-filter_complex",
       f"[1:v]scale={W}:{H},fps={FPS},format=yuv420p[f];"
       f"[0:v][f]overlay=enable='gte(n,{nframes - 2})'[v]",
       "-map", "[v]", "-map", "0:a", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "fast", "-crf", "16",
       "-r", str(FPS), "-c:a", "copy", "-t", f"{total:.3f}", "-movflags", "+faststart", str(stamped))
    stamped.replace(mp4)

    diff = loop_diff(mp4)
    lufs, peak = integrated_lufs(mp4), true_peak(mp4)
    payoff = next(s for w, s, e in words if w.lower().startswith("so") and s > 15)
    holds = [r["hold_s"] for r in plan if r["label"] != "loop"]
    brief = {
        "frame0_source": "04_Generated-Clips/part01/raw/v01/01_pulse_wrist_t1.mp4",
        "frame0_zoom": "none — moving plate, in 1.0s, crop x=656, no Ken Burns",
        "first_word_s": words[0][1],
        "surprise_s": {"more": more_t, "blood": next(s for w, s, e in words if w.lower().startswith("blood"))},
        "first_cut_s": plan[1]["t0"],
        "last_word_to_loop_s": round(total - last_end, 3),
        "meta_promise": False,
        "runtime_s": round(b.probe(mp4), 3),
        "longest_hold_s": max(holds + [plan[-1]["hold_s"]]),
        "payoff_phrase": "same blood, going round and round",
        "payoff_s": payoff,
        "payoff_frac": round(payoff / total, 3),
        "loop_sentence": "So it's the same blood, going round and round. You pump more blood than you have.",
        "loop_diff": diff,
        "lufs": lufs,
        "true_peak_dbfs": peak,
        "frame0_black": black_frac(mp4, 0.2),
        "no_cta": True,
        "vo_unchanged": True,
        "split": "5.05-7.20 06_two_ounces_eighth_t1; 7.20-9.48 07_thousand_beats_t4",
    }
    meta = {
        "id": SID, "version": VER, "job": JOB, "youtube_id": YT,
        "title": "Your Heart Pumps More Blood Than You Have",
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
        "file": mp4.name, "duration_s": brief["runtime_s"], "brief": brief,
        "gate_exit": gate.returncode, "gate_verdict": gate_json.get("verdict"),
        "gate_fails": gate_json.get("fails"), "gate_warns": gate_json.get("warns"),
        "qa": qa, "music_exit": music.returncode,
        "music_tail": (music.stdout + music.stderr).strip().splitlines()[-6:],
        "sfx": snd["level"], "copies": copied,
    }
    (QA / f"build_{SID}_{VER}.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps({k: summary[k] for k in ("file", "duration_s", "gate_verdict", "gate_fails",
                                              "gate_warns", "qa", "music_exit", "music_tail", "sfx")}, indent=2))
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
    if brief["payoff_frac"] < 0.70:
        bad.append("payoff")
    if bad:
        raise SystemExit("NOT PASS: " + ", ".join(bad))
    print("PASS", mp4.name, brief["runtime_s"])
    return summary


if __name__ == "__main__":
    build()
