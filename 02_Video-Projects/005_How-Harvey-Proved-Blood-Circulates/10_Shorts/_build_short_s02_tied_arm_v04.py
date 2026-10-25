#!/usr/bin/env python3
"""HOS 005 Short s02 tied arm stayed re-cut (J0965, £0). v01, v02 and v03 are not opened for write.

Audit fix #9. The scheduled file is v03, so this cut is v04 beside it.
Zero VO edits: the existing v03 stem, word for word. Picture only.
05_loosen_warm_t2.mp4 and 08_finger_push_t1.mp4 are not on the NAS.
The long holds are split with KEEP plates that are: arteries shut, the graded
loosen, the hand glow, and steering home. No "watch the full film".
First cut 2.67 s, holds ≤ 3.8 s, matched loop 1.00 s.

    python3 _build_short_s02_tied_arm_v04.py
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

from PIL import Image, ImageDraw  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _build_shorts_v03 as b  # noqa: E402
import _build_short_s05_valves_v02 as v  # noqa: E402

HERE, PROJ, REPO = b.HERE, b.PROJ, b.REPO
NAS = Path("/Volumes/data/mac-mini-archive/hos-worktrees/2026-10-22/hos-005-blood/"
           "02_Video-Projects/005_How-Harvey-Proved-Blood-Circulates")
VO = NAS / "10_Shorts/vo_v03/hos_005_s02_the_tied_arm_vo_v03_fin.wav"
ALIGN = NAS / "10_Shorts/vo_v03/hos_005_s02_the_tied_arm_vo_v03_fin_align.json"
CLIPS = NAS / "04_Generated-Clips"
V03 = NAS / "10_Shorts/hos_005_s02_the_tied_arm_v03.mp4"
OWB = Path("/Users/benjaminoats/YouTube/orbit-with-ben")
WORK = HERE / "_work_s02_tied_arm_v04"
QA = HERE / "qa_s02_tied_arm_v04"
SID, VER, JOB = "s02_tied_arm", "v04", "J0965"
AIR, YT = "2026-11-08", "mTY67qet7cM"
W, H, FPS = b.W, b.H, b.FPS
LOOP_S = 1.00
F0_IN, F0_CROP = 1.50, 640
HOLD_MAX, HOLD_MIN = 3.80, 1.20
HOOK = "ONE TIGHT **BAND**"
TITLE = "The Tied Arm That Proved Your Blood Circulates"
# (word index the plate lands on, or "loop"; label; plate under 04_Generated-Clips; in-point; crop x)
BEATS = [
    (0, "open", "part01/raw/v01/03_band_tightens_t3.mp4", F0_IN, F0_CROP),
    (7, "William", "part04/raw/v01/02_linen_tie_t2.mp4", 0.30, 450),
    (13, "arm", "part01/raw/v01/04_sum_band_doors_t2.mp4", 0.40, 656),
    (16, "hand", "part04/graded_v04/03_hand_pale_t4_graded_v04.mp4", 1.50, 100),
    (20, "No", "part04/raw/v01/05_arteries_veins_shut_t2.mp4", 0.50, 656),
    (25, "He", "part04/graded_v04/04_stopped_loosen_t5_graded_v04.mp4", 1.50, 560),
    (31, "veins", "part04/raw/v01/06_veins_swell_t1.mp4", 3.00, 560),
    (40, "So", "part04/raw/v01/07_in_out_doors_t2.mp4", 1.50, 620),
    (47, "and", "part04/raw/v01/15_your_hand_glow_t2.mp4", 0.40, 656),
    (53, "Look", "part04/raw/v01/12_stays_fills_t1.mp4", 0.50, 656),
    (57, "That", "part04/raw/v01/14_steering_home_t1.mp4", 0.40, 700),
    ("loop", "loop", "part01/raw/v01/03_band_tightens_t3.mp4", F0_IN - LOOP_S, F0_CROP),
]


def ff(*a: str, cwd: Path | None = None) -> None:
    v.ff(*a, cwd=cwd)


def sha256(p: Path) -> str:
    return v.sha256(p)


def plate(rel: str) -> Path:
    p = CLIPS / rel
    if not p.exists() or p.stat().st_size < 1000:
        raise SystemExit(f"missing plate {p}")
    return p


def land_time(words, idx) -> float:
    if idx == 0:
        return 0.0
    return round(max(0.0, words[idx][1] - 0.15), 3)


def synth_bed(path: Path, dur: float, sr: int = 48000) -> None:
    """Soft F-sharp plucks at 58 BPM. Not the valves cello, not the part 04 pad."""
    n = int(sr * dur)
    bpm = 58.0
    beat_s = 60.0 / bpm
    roots = [92.50, 138.59, 185.00, 116.54]
    frames = bytearray()
    for i in range(n):
        t = i / sr
        beat = t / beat_s
        step = int(beat)
        phase = beat - step
        root = roots[step % 4]
        env = math.exp(-3.4 * phase) * min(1.0, t / 0.4) * min(1.0, max(0.0, (dur - t) / 0.45))
        if phase > 0.55:
            env = 0.0
        l = r = 0.0
        for k, mul in enumerate((1.0, 2.0, 3.0)):
            a = (0.55, 0.16, 0.06)[k]
            l += math.sin(2 * math.pi * root * mul * t) * a
            r += math.sin(2 * math.pi * root * mul * 1.004 * t + 0.7) * a
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
        delay = int(max(0.0, t) * 1000)
        fc.append(f"[{i + 2}:a]volume=-10dB,adelay={delay}|{delay}[t{i}]")
        mix_in.append(f"[t{i}]")
    n = len(mix_in)
    fc.append("".join(mix_in) + f"amix=inputs={n}:normalize=0:duration=first,alimiter=limit=0.5[a]")
    ff(*inputs, "-filter_complex", ";".join(fc), "-map", "[a]", "-c:a", "pcm_s16le", str(dst))
    return dst


def black_frac(mp4: Path, t: float) -> float:
    return v.black_frac(mp4, t)


def copy_checked(src: Path, dst: Path) -> str:
    return v.copy_checked(src, dst)


def word_at(words, i: int) -> str:
    return words[i][0]


def build() -> None:
    if not VO.exists() or not ALIGN.exists() or not V03.exists():
        raise SystemExit(f"v03 stem or master missing under {NAS}")
    v03_sha = sha256(V03)
    if WORK.exists():
        shutil.rmtree(WORK)
    WORK.mkdir(parents=True)
    QA.mkdir(parents=True, exist_ok=True)
    words = b.words_from_align(ALIGN)
    spoken = " ".join(w for w, _, _ in words)
    if not spoken.startswith("One band proved your blood goes round"):
        raise SystemExit(f"VO open changed:\n{spoken[:90]}")
    if "watch the full" in spoken.lower() or "little doors" in spoken.lower():
        raise SystemExit("CTA or dropped line is in the stem")
    (WORK / "spoken.txt").write_text(spoken + "\n")
    shutil.copy2(VO, WORK / "vo_v03.wav")
    vo = WORK / "vo_v03.wav"
    if words[0][1] > 0.15:
        raise SystemExit(f"first word at {words[0][1]:.3f}")
    band_s = words[1][1]
    proved_s = words[2][1]
    if band_s > 1.50 or proved_s > 1.50:
        raise SystemExit(f"subject late: band {band_s:.3f} proved {proved_s:.3f}")
    last_end = words[-1][2]
    total = round(last_end + LOOP_S, 3)
    if not 22.0 <= total <= 27.0:
        raise SystemExit(f"runtime {total:.3f}s is outside 22–27")
    comes = words[48][1]
    if word_at(words, 48).rstrip(".,") != "comes":
        raise SystemExit(f"word 48 is {word_at(words, 48)!r}, expected comes")
    if comes < 0.70 * total:
        raise SystemExit(f"comes at {comes:.2f} is before 70% of {total:.2f}")

    cuts = []
    for idx, label, rel, ins, x in BEATS:
        src = plate(rel)
        t = last_end if idx == "loop" else land_time(words, idx)
        cuts.append({"t": round(t, 3), "src": src, "rel": rel, "in": ins, "x": x, "label": label})
    cuts.sort(key=lambda c: c["t"])
    plan = []
    for k, c in enumerate(cuts):
        end = cuts[k + 1]["t"] if k + 1 < len(cuts) else total
        dur = round(end - c["t"], 3)
        limit = 1.55 if c["label"] == "loop" else HOLD_MAX
        floor = 0.90 if c["label"] == "loop" else HOLD_MIN
        if not floor <= dur <= limit:
            raise SystemExit(f"hold {c['label']} {c['t']:.2f}-{end:.2f} = {dur:.2f}s")
        if k == 0 and end > 3.0:
            raise SystemExit(f"first cut at {end:.2f}")
        plan.append({**c, "t1": round(end, 3), "dur": dur})

    print(f"runtime {total:.2f}s  band {band_s:.2f}  proved {proved_s:.2f}  comes {comes:.2f} ({comes / total:.0%})")
    print(spoken)
    for row in plan:
        print(f"  {row['t']:6.2f}-{row['t1']:6.2f} {row['dur']:4.2f}s  {row['src'].name}  on {row['label']}")

    segs = []
    for k, row in enumerate(plan):
        out = WORK / f"seg_{k:02d}.mp4"
        v.seg(row["src"], out, row["in"], row["dur"], row["x"])
        segs.append(out)
    (WORK / "pic.txt").write_text("".join(f"file '{s.name}'\n" for s in segs))
    pic = WORK / "picture.mp4"
    ff("-f", "concat", "-safe", "0", "-i", "pic.txt", "-c", "copy", "-t", f"{total:.3f}", str(pic), cwd=WORK)

    bed = PROJ / "05_Music" / "hos_005_s02_tied_arm_v04_bed.wav"
    synth_bed(bed, total + 0.5)
    plan_j = {
        "prompt": ("Soft plucked strings under a close look at a tied arm, even, no chase. "
                   "Pace: 54-62 BPM. NOT hos005-part04-temp_score_bed_v01, NOT the 005 valves cello, "
                   "NOT the 004 gold-foil mallet, NOT the 002 four-elements bed, NOT the 005 heart-sum pulse, "
                   "NOT any Orbit With Ben bed, NOT a drum loop, NOT a trailer sting."),
        "film": "005", "short": "s02_tied_arm_v04", "job": JOB,
        "source": "own synthesis in _build_short_s02_tied_arm_v04.py, 0 credits",
        "pace_bpm": "54-62",
    }
    bed.with_name(bed.stem + "_plan.json").write_text(json.dumps(plan_j, indent=2) + "\n")
    loosened = words[26][1]
    swelled = words[36][1]
    veins_back = words[52][1]
    sfx = place_sfx(total, [loosened, swelled, veins_back])
    audio = WORK / "audio.wav"
    level = {}
    bed_db, sfx_db = -14.0, -16.0
    for _ in range(6):
        v.mix(vo, bed, sfx, total, audio, bed_db, sfx_db)
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
    pre_lufs = v.integrated_lufs(audio)
    lufs, peak = v.fit_loudness(audio, fitted)

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

    inputs = ["-i", str(pic), "-i", str(fitted)]
    for png, *_r in overlays:
        inputs += ["-loop", "1", "-i", str(png)]
    fc, last = [], "[0:v]"
    for i, (_png, t0, t1, *_r) in enumerate(overlays, 2):
        fc.append(f"{last}[{i}:v]overlay=0:0:enable='between(t,{t0:.3f},{t1:.3f})'[v{i}]")
        last = f"[v{i}]"
    mp4 = HERE / "hos_005_s02_the_tied_arm_v04.mp4"
    ff(*inputs, "-filter_complex", ";".join(fc), "-map", last, "-map", "1:a",
       "-c:v", "libx264", "-pix_fmt", "yuv420p", "-profile:v", "high", "-preset", "veryfast", "-crf", "18",
       "-r", str(FPS), "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2",
       "-t", f"{total:.3f}", "-movflags", "+faststart", str(mp4))

    if sha256(V03) != v03_sha:
        raise SystemExit("v03 changed during the build")
    out_plan = [{
        "t0": row["t"], "t1": row["t1"], "plate": row["rel"], "in_s": row["in"],
        "crop_x": row["x"], "lands_on": row["label"], "hold_s": row["dur"],
    } for row in plan]
    meta = {
        "id": "005_s02_tied_arm", "version": VER, "job": JOB, "youtube_id": YT,
        "title": "One Tight Band Proved Your Blood Goes Round",
        "air_date": AIR, "spoken": spoken, "script": spoken,
        "words": [{"word": w, "start": round(s, 3), "end": round(e, 3)} for w, s, e in words],
        "word_count": len(words), "last_word_end_s": round(last_end, 3),
        "plan": out_plan, "hook": HOOK.replace("**", ""), "hook_layer": hook_meta,
        "title_on_screen": TITLE, "no_cta": True, "no_new_spend": True,
        "open_note": ("Picture re-cut only. The v03 stem is unchanged, including every word. "
                      "05_loosen_warm_t2.mp4 and 08_finger_push_t1.mp4 are not on the NAS, so the "
                      "long holds are split with 05_arteries_veins_shut_t2, the graded loosen plate, "
                      "15_your_hand_glow_t2 and 14_steering_home_t1. v03 stays the scheduled file."),
        "v03_untouched": True, "v03_sha256": v03_sha,
        "bed": bed.name, "sfx_level": level,
        "frame0_source": "04_Generated-Clips/part01/raw/v01/03_band_tightens_t3.mp4",
        "frame0_zoom": "none — moving plate, in 1.5s, crop x=640, no Ken Burns",
        "frame0_in_s": F0_IN,
        "first_word_s": round(words[0][1], 3),
        "surprise_s": {"band": round(band_s, 3), "proved": round(proved_s, 3)},
        "first_cut_s": plan[0]["t1"],
        "last_word_to_loop_s": LOOP_S,
        "meta_promise": False,
        "runtime_s": round(b.probe(mp4), 3),
        "longest_hold_s": max(row["dur"] for row in plan if row["label"] != "loop"),
        "payoff_phrase": "comes home through the veins",
        "payoff_s": round(comes, 3),
        "payoff_frac": round(comes / total, 3),
        "loop_sentence": "That blood is heading home now. One band proved your blood goes round.",
        "lufs_wav": round(lufs, 2),
        "true_peak_wav_dbfs": round(peak, 2),
        "pre_master_lufs": round(pre_lufs, 2),
        "frame0_black": black_frac(mp4, 0.15),
        "sha256": sha256(mp4),
        "missing_plate_note": "05_loosen_warm_t2.mp4 and 08_finger_push_t1.mp4 are not on the NAS",
        "brief": {
            "frame0": "moving 03_band_tightens_t3, no zoom",
            "subject_named_s": round(band_s, 3),
            "first_word_s": round(words[0][1], 3),
            "first_cut_s": plan[0]["t1"],
            "loop_s": LOOP_S,
            "payoff_frac": round(comes / total, 3),
        },
    }
    meta_path = HERE / "hos_005_s02_the_tied_arm_v04_meta.json"
    meta_path.write_text(json.dumps(meta, indent=2) + "\n")

    gate = subprocess.run(
        [sys.executable, str(REPO / "00_Brand/Channel-Setup/tools/gate_shorts_open.py"),
         "check", str(mp4), "--air-date", AIR, "--id", YT,
         "--script", str(WORK / "spoken.txt"), "--vo", str(vo),
         "--meta", str(meta_path), "--json"],
        capture_output=True, text=True)
    (QA / "gate_s02_tied_arm_v04.txt").write_text((gate.stdout + gate.stderr).strip() + "\n")
    try:
        gate_json = json.loads(gate.stdout)
        if isinstance(gate_json, list):
            gate_json = gate_json[0]
    except json.JSONDecodeError:
        gate_json = {"verdict": "FAIL", "raw": (gate.stdout + gate.stderr)[-2000:]}
    (QA / "gate_s02_tied_arm_v04.json").write_text(json.dumps(gate_json, indent=2) + "\n")
    (QA / "j0918_ship_gate_s02_tied_arm_v04.txt").write_text(
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
    cuts_f = QA / "cuts_s02_tied_arm_v04.json"
    pool_f = QA / "pool_s02_tied_arm_v04.json"
    cuts_f.write_text(json.dumps(cuts_j, indent=2) + "\n")
    pool_f.write_text(json.dumps(pool, indent=2) + "\n")
    rel = lambda p: str(p.relative_to(REPO))  # noqa: E731
    r_pg = subprocess.run([sys.executable, str(OWB / "scripts/polish_gate.py"), rel(mp4),
                           "--cuts", rel(cuts_f), "--out", rel(QA / "polish_gate_s02_tied_arm_v04.json")],
                          cwd=REPO, capture_output=True, text=True)
    (QA / "polish_gate_s02_tied_arm_v04.txt").write_text((r_pg.stdout + r_pg.stderr).strip() + "\n")
    r_pq = subprocess.run([sys.executable, str(OWB / "scripts/picture_qa.py"), rel(mp4),
                           "--cuts", rel(cuts_f), "--pool", rel(pool_f),
                           "--out-dir", rel(QA / "picture_qa_s02_tied_arm_v04")],
                          cwd=REPO, capture_output=True, text=True)
    (QA / "picture_qa_s02_tied_arm_v04.txt").write_text((r_pq.stdout + r_pq.stderr).strip() + "\n")
    music = subprocess.run([sys.executable, str(OWB / "scripts/music_gate.py"), str(PROJ),
                            "--bed", str(bed), "--video", str(mp4),
                            "--out", str(QA / "music_gate_s02_tied_arm_v04.json")],
                           capture_output=True, text=True)
    (QA / "music_gate_s02_tied_arm_v04.txt").write_text((music.stdout + music.stderr).strip() + "\n")

    phone = HERE / "hos_005_s02_the_tied_arm_v04_PHONE.mp4"
    ff("-i", str(mp4), "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "veryfast", "-crf", "26",
       "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart", str(phone))
    sheet = QA / "hos_005_s02_the_tied_arm_v04_2fps_sheet.jpg"
    ff("-i", str(mp4), "-vf", "fps=2,scale=180:-2,tile=8x8", "-q:v", "4", str(sheet))
    for name, t in (("frame0", 0.05), ("title", 11.0)):
        ff("-ss", f"{t}", "-i", str(mp4), "-frames:v", "1", "-q:v", "3", str(QA / f"s02_tied_arm_v04_{name}.jpg"))

    uat = Path.home() / ("Library/Mobile Documents/com~apple~CloudDocs/HOS UAT/"
                         "005_How-Harvey-Proved-Blood-Circulates/10_Shorts/tied_arm_v04")
    nas_out = Path("/Volumes/data/mac-mini-archive/YouTube/History Of Science/02_Video-Projects/"
                   "005_How-Harvey-Proved-Blood-Circulates/10_Shorts/tied_arm_v04")
    copied = {}
    for folder in (uat, nas_out):
        for src in (mp4, phone, sheet):
            copied[str(folder / src.name)] = copy_checked(src, folder / src.name)
    manifest = {"job": JOB, "youtube_id": YT, "master_sha256": sha256(mp4), "phone_sha256": sha256(phone),
                "v03_sha256": v03_sha, "copies": copied,
                "lufs": meta["lufs_wav"], "true_peak_dbfs": meta["true_peak_wav_dbfs"]}
    (QA / "sha256_manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    (nas_out / "sha256_manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    meta["sha256"] = sha256(mp4)
    meta["frame0_black"] = black_frac(mp4, 0.15)
    meta_path.write_text(json.dumps(meta, indent=2) + "\n")

    summary = {
        "file": mp4.name, "sha256": sha256(mp4), "duration_s": round(b.probe(mp4), 3),
        "gate_exit": gate.returncode, "gate_verdict": gate_json.get("verdict"),
        "gate_fails": gate_json.get("fails"), "gate_warns": gate_json.get("warns"),
        "stayed_fails": gate_json.get("stayed_fails"),
        "polish_exit": r_pg.returncode, "picture_exit": r_pq.returncode, "music_exit": music.returncode,
        "music_tail": (music.stdout + music.stderr).strip().splitlines()[-4:],
        "polish_tail": (r_pg.stdout + r_pg.stderr).strip().splitlines()[-4:],
        "picture_tail": (r_pq.stdout + r_pq.stderr).strip().splitlines()[-6:],
        "sfx": level, "frame0_black": meta["frame0_black"], "lufs_wav": meta["lufs_wav"],
        "longest_hold_s": meta["longest_hold_s"], "payoff_frac": meta["payoff_frac"],
        "v03_sha": v03_sha,
    }
    (QA / "build_s02_tied_arm_v04.json").write_text(json.dumps(summary, indent=2) + "\n")
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
    if meta["frame0_black"] > 0.30:
        bad.append("black")
    if bad:
        raise SystemExit("FAIL " + ",".join(bad))


if __name__ == "__main__":
    build()
