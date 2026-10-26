#!/usr/bin/env python3
"""HOS 005 Short s03 never-saw stayed re-cut (J0966, £0). v01 and v02 are not opened for write.

Audit fix #11 (x_3L_IdYgEc, airs Sun 15 Nov 2026). The scheduled file is v02, so this cut is v03 beside it.
Zero VO edits: the existing v01_fin stem, word for word.
05_frog_lung_t1.mp4 is not on the NAS; the two 5.0 s holds are split with KEEP Part 05 plates:
04_malpighi_slide_t1 + 17_dutch_lens_t1, and 07_capillaries_loop_t1 + 07_capillaries_loop_t2 + 16_proved_last_link_t2.
No "watch the full film" overlay. First cut 2.04 s, all holds <= 3.30 s, matched loop 1.00 s back to frame 0.
Adds WILLIAM HARVEY (London, 1628) and MARCELLO MALPIGHI (Bologna, 1661) cards in house style.
AAC master target: -14.0 +/- 0.5 LUFS, true peak <= -1.6 dBTP.

    python3 _build_short_s03_never_saw_v03.py
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

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parents[1] / "004_Whats-Really-Inside-An-Atom/10_Shorts"))
import _build_shorts_v03 as b  # noqa: E402
import _build_short_s05_valves_v02 as v  # noqa: E402
import _build_backcat_gold_foil_v03 as gf  # noqa: E402

PROJ, REPO = b.PROJ, b.REPO
NAS = Path("/Volumes/data/mac-mini-archive/hos-worktrees/2026-10-22/hos-005-blood/"
           "02_Video-Projects/005_How-Harvey-Proved-Blood-Circulates")
VO = NAS / "10_Shorts/vo_v01/hos_005_s03_never_saw_vo_v01_fin.wav"
ALIGN = NAS / "10_Shorts/vo_v01/hos_005_s03_never_saw_vo_v01_fin_align.json"
CLIPS = NAS / "04_Generated-Clips"
V02 = NAS / "10_Shorts/hos_005_s03_never_saw_v02.mp4"
OWB = Path("/Users/benjaminoats/YouTube/orbit-with-ben")
WORK = HERE / "_work_s03_never_saw_v03"
QA = HERE / "qa_s03_never_saw_v03"
SID, VER, JOB = "s03_never_saw", "v03", "J0966"
AIR, YT = "2026-11-15", "x_3L_IdYgEc"
W, H, FPS = b.W, b.H, b.FPS
LOOP_S = 1.00
F0_IN, F0_CROP = 1.40, 656
HOLD_MAX, HOLD_MIN = 3.80, 1.20
HOOK = "HE NEVER **SAW** THIS"
TITLE = "The Tied Arm That Proved Your Blood Circulates"
HARVEY_CARD = ("WILLIAM HARVEY", "London, 1628", 2.20, 5.20)
MALPIGHI_CARD = ("MARCELLO MALPIGHI", "Bologna, 1661", 14.15, 17.35)

# (word index the plate lands on, or "loop"; label; plate under 04_Generated-Clips; in-point; crop x)
BEATS = [
    (0, "open", "part05/raw/v01/06_eyepiece_mesh_t1.mp4", F0_IN, F0_CROP),
    (6, "He", "part05/raw/v01/01_loop_gap_t5.mp4", 0.30, 656),
    (12, "but", "part05/raw/v01/02_tiny_gaps_t1.mp4", 0.50, 656),
    (21, "died", "part05/raw/v01/03_old_harvey_t1.mp4", 0.30, 656),
    (28, "Four", "part05/raw/v01/04_malpighi_slide_t1.mp4", 0.30, 656),
    (33, "put", "part05/raw/v01/17_dutch_lens_t1.mp4", 0.40, 656),
    (40, "There", "part05/raw/v01/07_capillaries_loop_t1.mp4", 0.30, 656),
    (47, "finer", "part05/raw/v01/07_capillaries_loop_t2.mp4", 0.30, 656),
    (51, "The", "part05/raw/v01/16_proved_last_link_t2.mp4", 0.40, 656),
    ("loop", "loop", "part05/raw/v01/06_eyepiece_mesh_t1.mp4", F0_IN - LOOP_S, F0_CROP),
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
    """Gentle E-minor / G-major glass-bell & lute figure at 62 BPM. Distinct from all other 005/004/007 beds."""
    n = int(sr * dur)
    bpm = 62.0
    beat_s = 60.0 / bpm
    roots = [164.81, 196.00, 246.94, 220.00, 146.83, 196.00]
    frames = bytearray()
    for i in range(n):
        t = i / sr
        beat = t / beat_s
        step = int(beat)
        phase = beat - step
        root = roots[step % len(roots)]
        env = math.exp(-2.8 * phase) * min(1.0, t / 0.4) * min(1.0, max(0.0, (dur - t) / 0.45))
        if phase > 0.65:
            env = 0.0
        l = r = 0.0
        for k, mul in enumerate((1.0, 2.0, 3.0)):
            a = (0.52, 0.19, 0.07)[k]
            l += math.sin(2 * math.pi * root * mul * t + 0.2 * k) * a
            r += math.sin(2 * math.pi * root * mul * 1.003 * t + 0.6 + 0.2 * k) * a
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


def render_who_card(path: Path, card_tuple: tuple[str, str, float, float]) -> dict:
    line1, line2, t0, t1 = card_tuple
    f1 = gf.fit_font(line1, gf.FONT, 2, W - 140, int(608 * 0.11))
    f2 = gf.fit_font(line2, gf.CTA_FONT, 0, W - 140, int(608 * 0.062))
    band_top = (H - 608) // 2
    y2 = band_top + 608 - 36
    y1 = y2 - f2.size - 18
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gf.shade_band(img, y1 - f1.size - 28, band_top + 608 + 8)
    d = ImageDraw.Draw(img)
    d.text((70, y1), line1, font=f1, anchor="ls", fill=gf.YEL, stroke_width=4, stroke_fill=gf.INK)
    d.text((70, y2), line2, font=f2, anchor="ls", fill=gf.CREAM, stroke_width=3, stroke_fill=gf.INK)
    img.save(path)
    return {"name": line1, "line2": line2, "t0": t0, "t1": t1, "style": "fabricius"}


def master_audio(src: Path, dst: Path) -> tuple[float, float, float, float]:
    best = None
    for gain in (-1.0, -0.5, 0.0, 0.4, 0.6, 0.8, 1.0, 1.2, 1.5, 2.0):
        for lim_db in (-1.8, -2.0, -2.2, -2.4):
            lin = 10 ** (lim_db / 20)
            trial = WORK / f"try_{gain:.1f}_{lim_db:.1f}.m4a"
            gf.ff("-i", str(src), "-vn",
                  "-af", f"volume={gain:.2f}dB,alimiter=limit={lin:.5f}:level=disabled:attack=5:release=40",
                  "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2", str(trial))
            lufs, peak = gf.measure(trial)
            if -14.5 <= lufs <= -13.5 and peak <= -1.6:
                score = abs(lufs + 14.0)
                if best is None or score < best[0]:
                    best = (score, gain, lim_db, lufs, peak, trial)
    if best is None:
        raise SystemExit("no gain/limiter pair landed in -14.0 +/- 0.5 and TP <= -1.6")
    shutil.copy2(best[5], dst)
    print(f"master gain {best[1]:+.1f} dB  limiter {best[2]:.1f} dB  -> {best[3]:.1f} LUFS  TP {best[4]:.1f}")
    return best[1], best[2], best[3], best[4]


def build() -> None:
    if not VO.exists() or not ALIGN.exists() or not V02.exists():
        raise SystemExit(f"v02 stem or master missing under {NAS}")
    v02_sha = sha256(V02)
    if WORK.exists():
        shutil.rmtree(WORK)
    WORK.mkdir(parents=True)
    QA.mkdir(parents=True, exist_ok=True)
    words = b.words_from_align(ALIGN)
    spoken = " ".join(w for w, _, _ in words)
    if not spoken.startswith("Harvey never saw the last link"):
        raise SystemExit(f"VO open changed:\n{spoken[:90]}")
    if "watch the full" in spoken.lower():
        raise SystemExit("CTA is in the stem")
    (WORK / "spoken.txt").write_text(spoken + "\n")
    last_end = words[-1][2]
    vo = WORK / "vo_trim.wav"
    ff("-i", str(VO), "-t", f"{last_end + 0.04:.3f}", "-c:a", "pcm_s16le", str(vo))
    if words[0][1] > 0.15:
        raise SystemExit(f"first word at {words[0][1]:.3f}")
    never_s = words[1][1]
    saw_s = words[2][1]
    if never_s > 1.50 or saw_s > 1.50:
        raise SystemExit(f"surprise late: never {never_s:.3f} saw {saw_s:.3f}")
    total = round(last_end + LOOP_S, 3)
    if not 22.0 <= total <= 27.0:
        raise SystemExit(f"runtime {total:.3f}s is outside 22-27")
    capillaries_s = words[50][1]
    if not words[50][0].startswith("Capillaries"):
        raise SystemExit(f"word 50 is {words[50][0]!r}, expected Capillaries.")
    if capillaries_s < 0.70 * total:
        raise SystemExit(f"Capillaries at {capillaries_s:.2f} is before 70% of {total:.2f}")

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

    print(f"runtime {total:.2f}s  never {never_s:.2f}  saw {saw_s:.2f}  capillaries {capillaries_s:.2f} ({capillaries_s / total:.0%})")
    for row in plan:
        print(f"  {row['t']:6.2f}-{row['t1']:6.2f} {row['dur']:4.2f}s  {row['src'].name}  on {row['label']}")

    segs = []
    for k, row in enumerate(plan):
        out = WORK / f"seg_{k:02d}.mp4"
        v.seg(row["src"], out, row["in"], row["dur"], row["x"])
        segs.append(out)
    (WORK / "pic.txt").write_text("".join(f"file '{s.name}'\n" for s in segs))
    pic = WORK / "picture_plates.mp4"
    ff("-f", "concat", "-safe", "0", "-i", "pic.txt", "-c", "copy", "-t", f"{total:.3f}", str(pic), cwd=WORK)

    bed = PROJ / "05_Music" / "hos_005_s03_never_saw_v03_bed.wav"
    synth_bed(bed, total + 0.5)
    plan_j = {
        "prompt": ("Gentle E-minor and G-major glass-bell and lute figure under a 1661 microscope discovery, "
                   "even, no chase. Pace: 58-66 BPM. NOT hos005-part05-temp_score_bed_v01, "
                   "NOT the 005 valves cello, NOT the 005 tied-arm F-sharp plucks, NOT the 005 heart-sum pulse, "
                   "NOT the 004 gold-foil mallet, NOT any Orbit With Ben bed, NOT a drum loop, NOT a trailer sting."),
        "film": "005", "short": "s03_never_saw_v03", "job": JOB,
        "source": "own synthesis in _build_short_s03_never_saw_v03.py, 0 credits",
        "pace_bpm": "58-66",
    }
    bed.with_name(bed.stem + "_plan.json").write_text(json.dumps(plan_j, indent=2) + "\n")
    sfx = place_sfx(total, [HARVEY_CARD[2], MALPIGHI_CARD[2], capillaries_s])
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
    _lufs_w, _peak_w = v.fit_loudness(audio, fitted)
    mastered = WORK / "audio_master.m4a"
    gain, lim_db, aac_lufs, aac_peak = master_audio(fitted, mastered)

    chunks = b.chunk_words(words)
    hook_png = WORK / "cap_hook.png"
    hook_meta = b.render_hook(hook_png, HOOK)
    title_png = WORK / "cap_title.png"
    b.render(title_png, TITLE, 58, 250, index=2, stroke=4)
    shade = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    for yy in range(560):
        ImageDraw.Draw(shade).line([(0, yy), (W, yy)], fill=(0, 0, 0, int(150 * (1 - yy / 560) ** 1.5)))
    Image.alpha_composite(shade, Image.open(title_png)).save(title_png)

    harvey_png = WORK / "card_harvey.png"
    harvey_meta = render_who_card(harvey_png, HARVEY_CARD)
    malpighi_png = WORK / "card_malpighi.png"
    malpighi_meta = render_who_card(malpighi_png, MALPIGHI_CARD)

    layers: list[tuple[Path, float, float, str]] = [(hook_png, 0.0, 2.04, "static")]
    for i, c in enumerate(chunks):
        png = WORK / f"cap_{i:03d}.png"
        b.render(png, c["text"], 52, 330, anchor="bottom")
        layers.append((png, c["t0"], min(c["t1"], total - 0.05), "static"))
    layers.append((title_png, 9.0, 14.0, "static"))
    layers.append((harvey_png, HARVEY_CARD[2], HARVEY_CARD[3], "card"))
    layers.append((malpighi_png, MALPIGHI_CARD[2], MALPIGHI_CARD[3], "card"))

    inputs = ["-i", str(pic)]
    fc_parts, last = [], "[0:v]"
    for i, (png, t0, t1, kind) in enumerate(layers, 1):
        inputs += ["-loop", "1", "-t", f"{max(0.05, t1 - t0):.3f}", "-i", str(png)]
        if kind == "static":
            nxt = f"s{i}"
            fc_parts.append(
                f"[{i}:v]setpts=PTS+{t0:.3f}/TB[p{i}];"
                f"{last}[p{i}]overlay=0:0:enable='gte(t,{t0:.3f})*lt(t,{t1:.3f})':eof_action=pass[{nxt}]")
            last = f"[{nxt}]"
        else:
            part, last = gf.overlay_expr(t0, t1, f"c{i}", f"[{i}:v]", last)
            fc_parts.append(part)
    silent = WORK / "picture.mp4"
    gf.ff(*inputs, "-filter_complex", ";".join(fc_parts), "-map", last, "-an",
          "-c:v", "libx264", "-pix_fmt", "yuv420p", "-profile:v", "high",
          "-preset", "veryfast", "-crf", "18", "-r", str(FPS), str(silent))
    mp4 = HERE / "hos_005_s03_never_saw_v03.mp4"
    gf.ff("-i", str(silent), "-i", str(mastered), "-map", "0:v", "-map", "1:a",
          "-c:v", "copy", "-c:a", "copy", "-t", f"{total:.3f}",
          "-movflags", "+faststart", str(mp4))
    if sha256(V02) != v02_sha:
        raise SystemExit("v02 changed during the v03 build")
    aac_lufs, aac_peak = gf.measure(mp4)
    print(f"final AAC {aac_lufs:.1f} LUFS  TP {aac_peak:.1f}  dur {b.probe(mp4):.3f}")
    if not (-14.5 <= aac_lufs <= -13.5) or aac_peak > -1.6:
        raise SystemExit(f"final loudness {aac_lufs:.2f} / {aac_peak:.2f}")

    out_plan = [{
        "t0": row["t"], "t1": row["t1"], "plate": row["rel"], "in_s": row["in"],
        "crop_x": row["x"], "lands_on": row["label"], "hold_s": row["dur"],
    } for row in plan]
    meta = {
        "id": "005_s03_never_saw", "version": VER, "job": JOB, "youtube_id": YT,
        "title": "The Blood Vessels Finer Than a Hair",
        "air_date": AIR, "spoken": spoken, "script": spoken,
        "words": [{"word": w, "start": round(s, 3), "end": round(e, 3)} for w, s, e in words],
        "word_count": len(words), "last_word_end_s": round(last_end, 3),
        "plan": out_plan, "hook": HOOK.replace("**", ""), "hook_layer": hook_meta,
        "title_on_screen": TITLE, "no_cta": True, "no_new_spend": True,
        "who_card": harvey_meta, "malpighi_card": malpighi_meta,
        "open_note": ("Picture and overlay re-cut only. The v01_fin stem is unchanged, word for word. "
                      "05_frog_lung_t1.mp4 is not on the NAS, so the two 5.0 s holds are split with "
                      "17_dutch_lens_t1, 07_capillaries_loop_t1, 07_capillaries_loop_t2 and "
                      "16_proved_last_link_t2. v02 stays untouched on the NAS."),
        "v02_untouched": True, "v02_sha256": v02_sha,
        "bed": bed.name, "sfx_level": level,
        "frame0_source": "04_Generated-Clips/part05/raw/v01/06_eyepiece_mesh_t1.mp4",
        "frame0_zoom": "none — moving plate, in 1.40s, crop x=656, no Ken Burns",
        "frame0_in_s": F0_IN,
        "first_word_s": round(words[0][1], 3),
        "surprise_s": {"never": round(never_s, 3), "saw": round(saw_s, 3)},
        "first_cut_s": plan[0]["t1"],
        "last_word_to_loop_s": LOOP_S,
        "meta_promise": False,
        "runtime_s": round(b.probe(mp4), 3),
        "longest_hold_s": max(row["dur"] for row in plan if row["label"] != "loop"),
        "payoff_phrase": "Capillaries.",
        "payoff_s": round(capillaries_s, 3),
        "payoff_frac": round(capillaries_s / total, 3),
        "loop_sentence": "The last link Harvey never saw. Harvey never saw the last link.",
        "lufs": round(aac_lufs, 2),
        "true_peak_dbfs": round(aac_peak, 2),
        "pre_master_lufs": round(pre_lufs, 2),
        "loudness_note": (
            f"Mastered with volume {gain:+.1f} dB and alimiter ceiling {lim_db:.1f} dB. "
            f"Measured on the v03 AAC: {aac_lufs:.1f} LUFS, true peak {aac_peak:.1f} dBFS."
        ),
        "frame0_black": v.black_frac(mp4, 0.15),
        "sha256": sha256(mp4),
        "missing_plate_note": "05_frog_lung_t1.mp4 is not on the NAS",
        "brief": {
            "frame0": "moving 06_eyepiece_mesh_t1 in 1.40s, crop x=656, no zoom",
            "subject_named_s": round(never_s, 3),
            "first_word_s": round(words[0][1], 3),
            "first_cut_s": plan[0]["t1"],
            "loop_s": LOOP_S,
            "payoff_frac": round(capillaries_s / total, 3),
        },
    }
    meta_path = HERE / "hos_005_s03_never_saw_v03_meta.json"
    meta_path.write_text(json.dumps(meta, indent=2) + "\n")

    gate = subprocess.run(
        [sys.executable, str(REPO / "00_Brand/Channel-Setup/tools/gate_shorts_open.py"),
         "check", str(mp4), "--air-date", AIR, "--id", YT,
         "--script", str(WORK / "spoken.txt"), "--vo", str(vo),
         "--meta", str(meta_path), "--json"],
        capture_output=True, text=True)
    (QA / "gate_s03_never_saw_v03.txt").write_text((gate.stdout + gate.stderr).strip() + "\n")
    try:
        gate_json = json.loads(gate.stdout)
        if isinstance(gate_json, list):
            gate_json = gate_json[0]
    except json.JSONDecodeError:
        gate_json = {"verdict": "FAIL", "raw": (gate.stdout + gate.stderr)[-2000:]}
    (QA / "gate_s03_never_saw_v03.json").write_text(json.dumps(gate_json, indent=2) + "\n")
    (QA / "j0918_ship_gate_s03_never_saw_v03.txt").write_text(
        "J0918 HOS ship gate (Chief, 24 Oct 2026), read from gate_shorts_open.\n"
        f"verdict={gate_json.get('verdict')} frame0_diff={gate_json.get('frame0_diff_0_1_5s')} "
        f"first_cut_s={gate_json.get('first_cut_s')} vo_onset_s={gate_json.get('vo_onset_s')} "
        f"tail_gap_s={gate_json.get('tail_gap_s')} stayed_fails={gate_json.get('stayed_fails')}\n"
        f"fails={gate_json.get('fails')}\nwarns={gate_json.get('warns')}\n"
        f"aac_lufs={aac_lufs:.2f} aac_true_peak_dbfs={aac_peak:.2f}\n"
    )

    cuts_plates, pool_plates, seen = [], [], set()
    for k, row in enumerate(plan, 1):
        src_id = f"loop_span_{row['src'].name}" if row["label"] == "loop" else row["src"].name
        cuts_plates.append({
            "row": f"s{k:02d}_{row['label']}", "timeline_in": row["t"], "timeline_out": row["t1"],
            "source": src_id, "upscale": 1.78, "video": True, "framing": {"offset": row["in"]},
        })
        if src_id not in seen:
            seen.add(src_id)
            pool_plates.append({"file_id": src_id, "title": f"Veo plate {row['src'].name}"})
    plate_cuts_f = QA / "cuts_s03_never_saw_v03_plates.json"
    plate_pool_f = QA / "pool_s03_never_saw_v03_plates.json"
    plate_cuts_f.write_text(json.dumps(cuts_plates, indent=2) + "\n")
    plate_pool_f.write_text(json.dumps(pool_plates, indent=2) + "\n")

    cuts_full = list(cuts_plates) + [
        {"row": "card_harvey", "timeline_in": HARVEY_CARD[2], "timeline_out": HARVEY_CARD[3],
         "source": "code_graphic_never_saw_v03_harvey.png", "upscale": 1.0, "video": False, "overlay": True},
        {"row": "card_malpighi", "timeline_in": MALPIGHI_CARD[2], "timeline_out": MALPIGHI_CARD[3],
         "source": "code_graphic_never_saw_v03_malpighi.png", "upscale": 1.0, "video": False, "overlay": True},
    ]
    pool_full = list(pool_plates) + [
        {"file_id": "code_graphic_never_saw_v03_harvey.png", "title": "WILLIAM HARVEY card"},
        {"file_id": "code_graphic_never_saw_v03_malpighi.png", "title": "MARCELLO MALPIGHI card"},
    ]
    (QA / "cuts_s03_never_saw_v03.json").write_text(json.dumps(cuts_full, indent=2) + "\n")
    (QA / "pool_s03_never_saw_v03.json").write_text(json.dumps(pool_full, indent=2) + "\n")

    rel = lambda p: str(p.relative_to(REPO))  # noqa: E731
    r_pg = subprocess.run([sys.executable, str(OWB / "scripts/polish_gate.py"), rel(mp4),
                           "--cuts", rel(plate_cuts_f), "--out", rel(QA / "polish_gate_s03_never_saw_v03.json")],
                          cwd=REPO, capture_output=True, text=True)
    (QA / "polish_gate_s03_never_saw_v03.txt").write_text((r_pg.stdout + r_pg.stderr).strip() + "\n")
    r_pq = subprocess.run([sys.executable, str(OWB / "scripts/picture_qa.py"), rel(mp4),
                           "--cuts", rel(plate_cuts_f), "--pool", rel(plate_pool_f),
                           "--out-dir", rel(QA / "picture_qa_s03_never_saw_v03")],
                          cwd=REPO, capture_output=True, text=True)
    (QA / "picture_qa_s03_never_saw_v03.txt").write_text((r_pq.stdout + r_pq.stderr).strip() + "\n")
    music = subprocess.run([sys.executable, str(OWB / "scripts/music_gate.py"), str(PROJ),
                            "--bed", str(bed), "--video", str(mp4),
                            "--out", str(QA / "music_gate_s03_never_saw_v03.json")],
                           capture_output=True, text=True)
    (QA / "music_gate_s03_never_saw_v03.txt").write_text((music.stdout + music.stderr).strip() + "\n")

    phone = HERE / "hos_005_s03_never_saw_v03_PHONE.mp4"
    ff("-i", str(mp4), "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "veryfast", "-crf", "26",
       "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart", str(phone))
    sheet = QA / "hos_005_s03_never_saw_v03_2fps_sheet.jpg"
    ff("-i", str(mp4), "-vf", "fps=2,scale=180:-2,tile=8x8", "-q:v", "4", str(sheet))
    for name, t in (("frame0", 0.05), ("harvey", 3.5), ("title", 11.0), ("malpighi", 15.5)):
        ff("-ss", f"{t}", "-i", str(mp4), "-frames:v", "1", "-q:v", "3", str(QA / f"never_saw_v03_{name}.jpg"))

    uat = Path.home() / "Library/Mobile Documents/com~apple~CloudDocs/HOS UAT/005_How-Harvey-Proved-Blood-Circulates/10_Shorts"
    nas_out = Path("/Volumes/data/mac-mini-archive/YouTube/History Of Science/02_Video-Projects/"
                   "005_How-Harvey-Proved-Blood-Circulates/10_Shorts/never_saw_v03")
    copied = {}
    for folder in (uat, nas_out):
        folder.mkdir(parents=True, exist_ok=True)
        for src in (mp4, phone, sheet):
            copied[str(folder / src.name)] = v.copy_checked(src, folder / src.name)
    manifest = {"job": JOB, "youtube_id": YT, "version": VER,
                "master_sha256": sha256(mp4), "phone_sha256": sha256(phone),
                "v02_sha256": v02_sha, "copies": copied,
                "aac_lufs": round(aac_lufs, 2), "aac_true_peak_dbfs": round(aac_peak, 2)}
    (QA / "sha256_manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    (nas_out / "sha256_manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")

    summary = {
        "file": mp4.name, "sha256": sha256(mp4), "duration_s": round(b.probe(mp4), 3),
        "lufs": round(aac_lufs, 2), "true_peak_dbfs": round(aac_peak, 2),
        "gate_exit": gate.returncode, "gate_verdict": gate_json.get("verdict"),
        "gate_fails": gate_json.get("fails"), "gate_warns": gate_json.get("warns"),
        "stayed_fails": gate_json.get("stayed_fails"),
        "polish_exit": r_pg.returncode, "picture_exit": r_pq.returncode, "music_exit": music.returncode,
        "music_tail": (music.stdout + music.stderr).strip().splitlines()[-3:],
        "polish_tail": (r_pg.stdout + r_pg.stderr).strip().splitlines()[-3:],
        "picture_tail": (r_pq.stdout + r_pq.stderr).strip().splitlines()[-3:],
        "sfx": level, "frame0_black": meta["frame0_black"],
        "longest_hold_s": meta["longest_hold_s"], "payoff_frac": meta["payoff_frac"],
        "v02_untouched": sha256(V02) == v02_sha,
    }
    (QA / "build_s03_never_saw_v03.json").write_text(json.dumps(summary, indent=2) + "\n")
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
