#!/usr/bin/env python3
"""HOS 005 tied-arm Short v05 (J0965 c51, £0). v04 is not opened for write.

A gain plus true-peak limiter, and WILLIAM HARVEY / London, 1628 on 2.674–5.236
(02_linen_tie_t2). VO, frame 0, plates, cuts and the loop stay as v04.
AAC target: -14.0 +/- 0.5 LUFS, true peak <= -1.5.

    python3 _build_short_s02_tied_arm_v05.py
"""
from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "004_Whats-Really-Inside-An-Atom/10_Shorts"))
import _build_backcat_gold_foil_v03 as gf  # noqa: E402

REPO = HERE.parents[2]
PROJ = REPO / "02_Video-Projects/005_How-Harvey-Proved-Blood-Circulates"
OWB = Path("/Users/benjaminoats/YouTube/orbit-with-ben")
V04 = HERE / "hos_005_s02_the_tied_arm_v04.mp4"
V04_META = HERE / "hos_005_s02_the_tied_arm_v04_meta.json"
V04_SHA = "98a283d83db149e71393aee37a394f7075d51a73bb88ecb5f01e605d410d9523"
WORK = HERE / "_work_s02_tied_arm_v05"
QA = HERE / "qa_s02_tied_arm_v05"
STEMS = HERE / "_work_s02_tied_arm_v04"
JOB, AIR, YT = "J0965", "2026-11-08", "mTY67qet7cM"
W, H = gf.W, gf.H
WHO = ("WILLIAM HARVEY", "London, 1628", 2.674, 5.236)


def render_who(path: Path) -> dict:
    line1, line2, t0, t1 = WHO
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
    for gain in (0.4, 0.6, 0.8, 1.0, 1.2, 1.5):
        for lim_db in (-1.8, -2.0, -2.2, -2.4):
            lin = 10 ** (lim_db / 20)
            trial = WORK / f"try_{gain:.1f}_{lim_db:.1f}.m4a"
            gf.ff("-i", str(src), "-vn",
                  "-af", f"volume={gain:.2f}dB,alimiter=limit={lin:.5f}:level=disabled:attack=5:release=40",
                  "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2", str(trial))
            lufs, peak = gf.measure(trial)
            if -14.5 <= lufs <= -13.5 and peak <= -1.5:
                score = abs(lufs + 14.0)
                if best is None or score < best[0]:
                    best = (score, gain, lim_db, lufs, peak, trial)
    if best is None:
        raise SystemExit("no gain/limiter pair landed in -14.0 +/- 0.5 and TP <= -1.5")
    shutil.copy2(best[5], dst)
    print(f"master gain {best[1]:+.1f} dB  limiter {best[2]:.1f} dB  -> {best[3]:.1f} LUFS  TP {best[4]:.1f}")
    return best[1], best[2], best[3], best[4]


def main() -> None:
    if gf.sha256(V04) != V04_SHA:
        raise SystemExit(f"v04 sha changed ({gf.sha256(V04)[:12]})")
    if WORK.exists():
        shutil.rmtree(WORK)
    WORK.mkdir(parents=True)
    QA.mkdir(parents=True, exist_ok=True)
    base = json.loads(V04_META.read_text())
    who = render_who(WORK / "card_harvey.png")
    mastered = WORK / "audio_master.m4a"
    gain, lim_db, _lufs, _peak = master_audio(V04, mastered)
    dur = WHO[3] - WHO[2]
    chain, last = gf.overlay_expr(WHO[2], WHO[3], "who", "[1:v]", "[0:v]")
    silent = WORK / "picture.mp4"
    gf.ff("-i", str(V04), "-loop", "1", "-t", f"{dur:.3f}", "-i", str(WORK / "card_harvey.png"),
          "-filter_complex", chain, "-map", last, "-an",
          "-c:v", "libx264", "-pix_fmt", "yuv420p", "-profile:v", "high",
          "-preset", "veryfast", "-crf", "18", "-r", "30", str(silent))
    mp4 = HERE / "hos_005_s02_the_tied_arm_v05.mp4"
    gf.ff("-i", str(silent), "-i", str(mastered), "-map", "0:v", "-map", "1:a",
          "-c:v", "copy", "-c:a", "copy", "-t", f"{gf.probe(V04):.3f}",
          "-movflags", "+faststart", str(mp4))
    if gf.sha256(V04) != V04_SHA:
        raise SystemExit("v04 was written during the v05 build")
    aac_lufs, aac_peak = gf.measure(mp4)
    print(f"final AAC {aac_lufs:.1f} LUFS  TP {aac_peak:.1f}  dur {gf.probe(mp4):.3f}")
    if not (-14.5 <= aac_lufs <= -13.5) or aac_peak > -1.5:
        raise SystemExit(f"final loudness {aac_lufs:.2f} / {aac_peak:.2f}")
    if abs(gf.probe(mp4) - base["runtime_s"]) > 0.05:
        raise SystemExit("runtime moved")

    meta = dict(base)
    meta.update({
        "version": "v05", "job": JOB, "v04_untouched": True, "v04_sha256": V04_SHA,
        "changes": "master gain plus WILLIAM HARVEY card on the linen tie",
        "who_card": who,
        "lufs": round(aac_lufs, 2), "true_peak_dbfs": round(aac_peak, 2),
        "loudness_note": (
            f"v04 AAC was -14.7 LUFS / -0.9 dBTP. volume {gain:+.1f} dB then "
            f"alimiter ceiling {lim_db:.1f} dB. Measured on the v05 AAC: "
            f"{aac_lufs:.1f} LUFS, true peak {aac_peak:.1f} dBFS."
        ),
        "sha256": gf.sha256(mp4), "runtime_s": round(gf.probe(mp4), 3),
    })
    meta_path = HERE / "hos_005_s02_the_tied_arm_v05_meta.json"
    meta_path.write_text(json.dumps(meta, indent=2) + "\n")
    gate = subprocess.run(
        [sys.executable, str(REPO / "00_Brand/Channel-Setup/tools/gate_shorts_open.py"),
         "check", str(mp4), "--air-date", AIR, "--id", YT,
         "--script", str(STEMS / "spoken.txt"), "--vo", str(STEMS / "vo_v03.wav"),
         "--meta", str(meta_path), "--json"],
        capture_output=True, text=True)
    (QA / "gate_s02_tied_arm_v05.txt").write_text((gate.stdout + gate.stderr).strip() + "\n")
    try:
        gate_json = json.loads(gate.stdout)
        if isinstance(gate_json, list):
            gate_json = gate_json[0]
    except json.JSONDecodeError:
        gate_json = {"verdict": "FAIL", "raw": (gate.stdout + gate.stderr)[-2000:]}
    (QA / "gate_s02_tied_arm_v05.json").write_text(json.dumps(gate_json, indent=2) + "\n")
    (QA / "j0918_ship_gate_s02_tied_arm_v05.txt").write_text(
        "J0918 HOS ship gate, v05 Harvey card + master.\n"
        f"verdict={gate_json.get('verdict')} frame0_diff={gate_json.get('frame0_diff_0_1_5s')} "
        f"first_cut_s={gate_json.get('first_cut_s')} vo_onset_s={gate_json.get('vo_onset_s')} "
        f"tail_gap_s={gate_json.get('tail_gap_s')} stayed_fails={gate_json.get('stayed_fails')}\n"
        f"fails={gate_json.get('fails')}\nwarns={gate_json.get('warns')}\n"
        f"aac_lufs={aac_lufs:.2f} aac_true_peak_dbfs={aac_peak:.2f}\n"
    )
    cuts_src = HERE / "qa_s02_tied_arm_v04/cuts_s02_tied_arm_v04.json"
    pool_src = HERE / "qa_s02_tied_arm_v04/pool_s02_tied_arm_v04.json"
    plate = QA / "cuts_s02_tied_arm_v05_plates.json"
    plate.write_text(cuts_src.read_text())
    cuts = json.loads(cuts_src.read_text())
    cuts.append({"row": "card_harvey", "timeline_in": WHO[2], "timeline_out": WHO[3],
                 "source": "code_graphic_tied_arm_v05_harvey.png", "upscale": 1.0,
                 "video": False, "overlay": True})
    (QA / "cuts_s02_tied_arm_v05.json").write_text(json.dumps(cuts, indent=2) + "\n")
    pool = json.loads(pool_src.read_text())
    pool.append({"file_id": "code_graphic_tied_arm_v05_harvey.png", "title": "WILLIAM HARVEY card"})
    (QA / "pool_s02_tied_arm_v05.json").write_text(json.dumps(pool, indent=2) + "\n")
    rel = lambda p: str(p.relative_to(REPO))  # noqa: E731
    r_pg = subprocess.run([sys.executable, str(OWB / "scripts/polish_gate.py"), rel(mp4),
                           "--cuts", rel(plate), "--out", rel(QA / "polish_gate_s02_tied_arm_v05.json")],
                          cwd=REPO, capture_output=True, text=True)
    (QA / "polish_gate_s02_tied_arm_v05.txt").write_text((r_pg.stdout + r_pg.stderr).strip() + "\n")
    r_pq = subprocess.run([sys.executable, str(OWB / "scripts/picture_qa.py"), rel(mp4),
                           "--cuts", rel(plate), "--pool", rel(pool_src),
                           "--out-dir", rel(QA / "picture_qa_s02_tied_arm_v05")],
                          cwd=REPO, capture_output=True, text=True)
    (QA / "picture_qa_s02_tied_arm_v05.txt").write_text((r_pq.stdout + r_pq.stderr).strip() + "\n")
    bed = PROJ / "05_Music" / base["bed"]
    music = subprocess.run([sys.executable, str(OWB / "scripts/music_gate.py"), str(PROJ),
                            "--bed", str(bed), "--video", str(mp4),
                            "--out", str(QA / "music_gate_s02_tied_arm_v05.json")],
                           capture_output=True, text=True)
    (QA / "music_gate_s02_tied_arm_v05.txt").write_text((music.stdout + music.stderr).strip() + "\n")
    r_sfx = subprocess.run([sys.executable, str(OWB / "scripts/sfx_kit.py"), "level",
                            "--vo", str(STEMS / "stem_vo.wav"), "--sfx", str(STEMS / "stem_sfx.wav"),
                            "--bed", str(STEMS / "stem_bed.wav"),
                            "--minutes", f"{base['runtime_s'] / 60:.3f}",
                            "--out", str(QA / "sfx_level.json")],
                           capture_output=True, text=True)
    (QA / "sfx_level.txt").write_text((r_sfx.stdout + r_sfx.stderr).strip() + "\n")
    phone = HERE / "hos_005_s02_the_tied_arm_v05_PHONE.mp4"
    gf.ff("-i", str(mp4), "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "veryfast", "-crf", "26",
          "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart", str(phone))
    sheet = QA / "hos_005_s02_the_tied_arm_v05_2fps_sheet.jpg"
    gf.ff("-i", str(mp4), "-vf", "fps=2,scale=180:-2,tile=8x8", "-q:v", "4", str(sheet))
    for name, t in (("frame0", 0.05), ("harvey", 4.0)):
        gf.ff("-ss", f"{t}", "-i", str(mp4), "-frames:v", "1", "-q:v", "3",
              str(QA / f"tied_arm_v05_{name}.jpg"))
    uat = Path.home() / "Library/Mobile Documents/com~apple~CloudDocs/HOS UAT/005_How-Harvey-Proved-Blood-Circulates/10_Shorts"
    nas_out = Path("/Volumes/data/mac-mini-archive/YouTube/History Of Science/02_Video-Projects/"
                   "005_How-Harvey-Proved-Blood-Circulates/10_Shorts/tied_arm_v05")
    copied = {}
    for folder in (uat, nas_out):
        folder.mkdir(parents=True, exist_ok=True)
        for src in (mp4, phone, sheet):
            dst = folder / src.name
            shutil.copy2(src, dst)
            if gf.sha256(src) != gf.sha256(dst):
                raise SystemExit(f"sha mismatch {dst}")
            copied[str(dst)] = gf.sha256(dst)
    manifest = {"job": JOB, "youtube_id": YT, "version": "v05",
                "master_sha256": gf.sha256(mp4), "phone_sha256": gf.sha256(phone),
                "v04_sha256": gf.sha256(V04), "copies": copied,
                "aac_lufs": round(aac_lufs, 2), "aac_true_peak_dbfs": round(aac_peak, 2)}
    (QA / "sha256_manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    (nas_out / "sha256_manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    summary = {
        "file": mp4.name, "lufs": round(aac_lufs, 2), "true_peak_dbfs": round(aac_peak, 2),
        "gate_verdict": gate_json.get("verdict"), "gate_fails": gate_json.get("fails"),
        "polish_exit": r_pg.returncode, "picture_exit": r_pq.returncode,
        "music_exit": music.returncode, "sfx_exit": r_sfx.returncode,
        "polish_tail": (r_pg.stdout + r_pg.stderr).strip().splitlines()[-3:],
        "picture_tail": (r_pq.stdout + r_pq.stderr).strip().splitlines()[-3:],
        "music_tail": (music.stdout + music.stderr).strip().splitlines()[-2:],
        "v04_untouched": True,
    }
    (QA / "build_s02_tied_arm_v05.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))
    bad = []
    if gate_json.get("verdict") != "PASS":
        bad.append("gate")
    if r_pg.returncode or r_pq.returncode or music.returncode or r_sfx.returncode:
        bad += [n for n, c in (("polish", r_pg.returncode), ("picture", r_pq.returncode),
                               ("music", music.returncode), ("sfx", r_sfx.returncode)) if c]
    if bad:
        raise SystemExit("FAIL " + ",".join(bad))


if __name__ == "__main__":
    main()
