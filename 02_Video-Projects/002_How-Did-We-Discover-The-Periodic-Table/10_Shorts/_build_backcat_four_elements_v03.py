#!/usr/bin/env python3
"""HOS 002 four-elements Short v03 (J0965 c51, £0). v01 and v02 are not opened for write.

Gain plus a true-peak limiter, and three cards. VO words, the 1.40x open,
frame 0, plates, cuts and the loop stay as v02. "aren't" stays at 1.47 s.
ANTOINE LAVOISIER / Paris, 1789 on 12.24–14.91. A 33 count-up on 17.87–20.10.
LIGHT + HEAT on 20.10–22.54. AAC target: -14.0 +/- 0.5 LUFS, true peak <= -1.5.

    python3 _build_backcat_four_elements_v03.py
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
PROJ = REPO / "02_Video-Projects/002_How-Did-We-Discover-The-Periodic-Table"
OWB = Path("/Users/benjaminoats/YouTube/orbit-with-ben")
V02 = HERE / "hos_002_backcat_four_elements_v02.mp4"
V02_META = HERE / "hos_002_backcat_four_elements_v02_meta.json"
V02_SHA = "df2d58a1d1330b892f0f3b3b4feb30ea459d59578aa72f5675747d604abddbf7"
WORK = HERE / "_work_four_elements_v03"
QA = HERE / "qa_four_elements_v03"
STEMS = HERE / "_work_four_elements_v02"
JOB, AIR, YT = "J0965", "2026-11-03", "Pp5LmjsduI4"
W, H = gf.W, gf.H
WHO = ("ANTOINE LAVOISIER", "Paris, 1789", 12.243, 14.907)
COUNT = (17.867, 20.097, 33, 18.946)  # t0, t1, end value, arrive at "thirty-three"
LIGHT = ("LIGHT + HEAT", 20.097, 22.500)
FONT, CTA = gf.FONT, gf.CTA_FONT


def render_who(path: Path) -> dict:
    line1, line2, t0, t1 = WHO
    f1 = gf.fit_font(line1, FONT, 2, W - 140, int(608 * 0.095))
    f2 = gf.fit_font(line2, CTA, 0, W - 140, int(608 * 0.062))
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


def render_line(path: Path, text: str) -> None:
    f1 = gf.fit_font(text, FONT, 2, W - 160, int(608 * 0.15))
    band_top = (H - 608) // 2
    y1 = band_top + 608 - 48
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gf.shade_band(img, y1 - f1.size - 24, band_top + 608 + 8)
    d = ImageDraw.Draw(img)
    d.text((W / 2, y1), text, font=f1, anchor="ms", fill=gf.YEL, stroke_width=4, stroke_fill=gf.INK)
    img.save(path)


def count_mov(path: Path) -> dict:
    t0, t1, end, arrive_at = COUNT
    dur = t1 - t0
    n = max(2, int(round(dur * 30)))
    arrive = max(1, int(round((arrive_at - t0) * 30)))
    frames = WORK / "count_frames"
    frames.mkdir(parents=True)
    for i in range(n):
        val = end if i >= arrive else int(round(end * i / arrive))
        render_line(frames / f"f_{i:04d}.png", str(val))
    gf.ff("-framerate", "30", "-i", str(frames / "f_%04d.png"), "-c:v", "qtrle", str(path))
    return {"text": str(end), "t0": t0, "t1": t1, "arrive_s": arrive_at, "style": "count-up"}


def master_audio(src: Path, dst: Path) -> tuple[float, float, float, float]:
    best = None
    for gain in (3.2, 3.5, 3.8, 4.0, 4.2):
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
    if gf.sha256(V02) != V02_SHA:
        raise SystemExit(f"v02 sha changed ({gf.sha256(V02)[:12]})")
    if WORK.exists():
        shutil.rmtree(WORK)
    WORK.mkdir(parents=True)
    QA.mkdir(parents=True, exist_ok=True)
    base = json.loads(V02_META.read_text())
    if abs(base["surprise_s"]["aren't"] - 1.474) > 0.02:
        raise SystemExit("aren't is no longer at 1.47 s")
    who = render_who(WORK / "card_lavoisier.png")
    count = count_mov(WORK / "count.mov")
    render_line(WORK / "card_light.png", LIGHT[0])
    light = {"text": LIGHT[0], "t0": LIGHT[1], "t1": LIGHT[2], "style": "callout"}

    mastered = WORK / "audio_master.m4a"
    gain, lim_db, lufs, peak = master_audio(V02, mastered)

    d_who = WHO[3] - WHO[2]
    d_light = LIGHT[2] - LIGHT[1]
    c1, last = gf.overlay_expr(WHO[2], WHO[3], "who", "[1:v]", "[0:v]")
    dur_c = COUNT[1] - COUNT[0]
    c_chain = (
        f"[2:v]format=rgba,fade=t=in:st=0:d=0.30:alpha=1,"
        f"fade=t=out:st={max(0.4, dur_c - 0.28):.3f}:d=0.28:alpha=1,"
        f"setpts=PTS+{COUNT[0]:.3f}/TB[num]"
    )
    c_over = (
        f"{last}[num]overlay=0:0:enable='between(t,{COUNT[0]:.3f},{COUNT[1]:.3f})':eof_action=pass[vnum]"
    )
    last = "[vnum]"
    c3, last = gf.overlay_expr(LIGHT[1], LIGHT[2], "heat", "[3:v]", last)
    fc = ";".join([c1, c_chain, c_over, c3])
    silent = WORK / "picture.mp4"
    gf.ff("-i", str(V02),
          "-loop", "1", "-t", f"{d_who:.3f}", "-i", str(WORK / "card_lavoisier.png"),
          "-i", str(WORK / "count.mov"),
          "-loop", "1", "-t", f"{d_light:.3f}", "-i", str(WORK / "card_light.png"),
          "-filter_complex", fc, "-map", last, "-an",
          "-c:v", "libx264", "-pix_fmt", "yuv420p", "-profile:v", "high",
          "-preset", "veryfast", "-crf", "18", "-r", "30", str(silent))
    mp4 = HERE / "hos_002_backcat_four_elements_v03.mp4"
    gf.ff("-i", str(silent), "-i", str(mastered),
          "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "copy",
          "-t", f"{gf.probe(V02):.3f}", "-movflags", "+faststart", str(mp4))
    if gf.sha256(V02) != V02_SHA:
        raise SystemExit("v02 was written during the v03 build")
    aac_lufs, aac_peak = gf.measure(mp4)
    print(f"final AAC {aac_lufs:.1f} LUFS  TP {aac_peak:.1f}  dur {gf.probe(mp4):.3f}")
    if not (-14.5 <= aac_lufs <= -13.5) or aac_peak > -1.5:
        raise SystemExit(f"final loudness {aac_lufs:.2f} / {aac_peak:.2f} missed the target")
    if abs(gf.probe(mp4) - base["runtime_s"]) > 0.05:
        raise SystemExit(f"runtime moved: {gf.probe(mp4):.3f} vs v02 {base['runtime_s']}")

    meta = dict(base)
    meta.update({
        "version": "v03", "job": JOB, "v02_untouched": True, "v02_sha256": V02_SHA,
        "changes": "master gain plus Lavoisier card, 33 count-up, LIGHT + HEAT",
        "who_card": who, "count_up": count, "callout": light,
        "open_atempo": 1.4, "arent_s": base["surprise_s"]["aren't"],
        "lufs": round(aac_lufs, 2), "true_peak_dbfs": round(aac_peak, 2),
        "loudness_note": (
            f"v02 AAC was -17.9 LUFS / -3.0 dBTP. volume {gain:+.1f} dB then "
            f"alimiter ceiling {lim_db:.1f} dB. Measured on the v03 AAC: "
            f"{aac_lufs:.1f} LUFS, true peak {aac_peak:.1f} dBFS."
        ),
        "sha256": gf.sha256(mp4), "runtime_s": round(gf.probe(mp4), 3),
    })
    meta_path = HERE / "hos_002_backcat_four_elements_v03_meta.json"
    meta_path.write_text(json.dumps(meta, indent=2) + "\n")

    spoken = STEMS / "spoken.txt"
    vo = STEMS / "vo_trim.wav"
    gate = subprocess.run(
        [sys.executable, str(REPO / "00_Brand/Channel-Setup/tools/gate_shorts_open.py"),
         "check", str(mp4), "--air-date", AIR, "--id", YT,
         "--script", str(spoken), "--vo", str(vo), "--meta", str(meta_path), "--json"],
        capture_output=True, text=True)
    (QA / "gate_four_elements_v03.txt").write_text((gate.stdout + gate.stderr).strip() + "\n")
    try:
        gate_json = json.loads(gate.stdout)
        if isinstance(gate_json, list):
            gate_json = gate_json[0]
    except json.JSONDecodeError:
        gate_json = {"verdict": "FAIL", "raw": (gate.stdout + gate.stderr)[-2000:]}
    (QA / "gate_four_elements_v03.json").write_text(json.dumps(gate_json, indent=2) + "\n")
    (QA / "j0918_ship_gate_four_elements_v03.txt").write_text(
        "J0918 HOS ship gate, v03 cards + master gain.\n"
        f"verdict={gate_json.get('verdict')} frame0_diff={gate_json.get('frame0_diff_0_1_5s')} "
        f"first_cut_s={gate_json.get('first_cut_s')} vo_onset_s={gate_json.get('vo_onset_s')} "
        f"tail_gap_s={gate_json.get('tail_gap_s')} stayed_fails={gate_json.get('stayed_fails')}\n"
        f"fails={gate_json.get('fails')}\nwarns={gate_json.get('warns')}\n"
        f"aac_lufs={aac_lufs:.2f} aac_true_peak_dbfs={aac_peak:.2f} arent_s={base['surprise_s']['aren\'t']}\n"
    )

    cuts_src = HERE / "qa_four_elements_v02/cuts_four_elements_v02.json"
    pool_src = HERE / "qa_four_elements_v02/pool_four_elements_v02.json"
    plate_cuts = QA / "cuts_four_elements_v03_plates.json"
    plate_cuts.write_text(cuts_src.read_text())
    cuts = json.loads(cuts_src.read_text())
    for row, t0, t1, src, title in (
        ("card_lavoisier", WHO[2], WHO[3], "code_graphic_four_elements_v03_lavoisier.png", "ANTOINE LAVOISIER card"),
        ("card_33", COUNT[0], COUNT[1], "code_graphic_four_elements_v03_33.png", "33 count-up"),
        ("card_light", LIGHT[1], LIGHT[2], "code_graphic_four_elements_v03_light.png", "LIGHT + HEAT"),
    ):
        cuts.append({"row": row, "timeline_in": t0, "timeline_out": t1, "source": src,
                     "upscale": 1.0, "video": False, "overlay": True})
    (QA / "cuts_four_elements_v03.json").write_text(json.dumps(cuts, indent=2) + "\n")
    pool = json.loads(pool_src.read_text())
    pool += [
        {"file_id": "code_graphic_four_elements_v03_lavoisier.png", "title": "ANTOINE LAVOISIER card"},
        {"file_id": "code_graphic_four_elements_v03_33.png", "title": "33 count-up"},
        {"file_id": "code_graphic_four_elements_v03_light.png", "title": "LIGHT + HEAT"},
    ]
    (QA / "pool_four_elements_v03.json").write_text(json.dumps(pool, indent=2) + "\n")
    rel = lambda p: str(p.relative_to(REPO))  # noqa: E731
    r_pg = subprocess.run(
        [sys.executable, str(OWB / "scripts/polish_gate.py"), rel(mp4),
         "--cuts", rel(plate_cuts), "--out", rel(QA / "polish_gate_four_elements_v03.json")],
        cwd=REPO, capture_output=True, text=True)
    (QA / "polish_gate_four_elements_v03.txt").write_text((r_pg.stdout + r_pg.stderr).strip() + "\n")
    r_pq = subprocess.run(
        [sys.executable, str(OWB / "scripts/picture_qa.py"), rel(mp4),
         "--cuts", rel(plate_cuts), "--pool", rel(pool_src),
         "--out-dir", rel(QA / "picture_qa_four_elements_v03")],
        cwd=REPO, capture_output=True, text=True)
    (QA / "picture_qa_four_elements_v03.txt").write_text((r_pq.stdout + r_pq.stderr).strip() + "\n")
    bed = PROJ / "05_Music" / "hos_002_backcat_four_elements_v02_bed.wav"
    music = subprocess.run(
        [sys.executable, str(OWB / "scripts/music_gate.py"), str(PROJ),
         "--bed", str(bed), "--video", str(mp4),
         "--out", str(QA / "music_gate_four_elements_v03.json")],
        capture_output=True, text=True)
    (QA / "music_gate_four_elements_v03.txt").write_text((music.stdout + music.stderr).strip() + "\n")
    r_sfx = subprocess.run(
        [sys.executable, str(OWB / "scripts/sfx_kit.py"), "level",
         "--vo", str(STEMS / "stem_vo.wav"), "--sfx", str(STEMS / "stem_sfx.wav"),
         "--bed", str(STEMS / "stem_bed.wav"), "--minutes", f"{base['runtime_s'] / 60:.3f}",
         "--out", str(QA / "sfx_level.json")],
        capture_output=True, text=True)
    (QA / "sfx_level.txt").write_text((r_sfx.stdout + r_sfx.stderr).strip() + "\n")

    phone = HERE / "hos_002_backcat_four_elements_v03_PHONE.mp4"
    gf.ff("-i", str(mp4), "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "veryfast", "-crf", "26",
          "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart", str(phone))
    sheet = QA / "hos_002_backcat_four_elements_v03_2fps_sheet.jpg"
    gf.ff("-i", str(mp4), "-vf", "fps=2,scale=180:-2,tile=8x8", "-q:v", "4", str(sheet))
    for name, t in (("frame0", 0.05), ("lavoisier", 13.4), ("count", 19.4), ("light", 21.2)):
        gf.ff("-ss", f"{t}", "-i", str(mp4), "-frames:v", "1", "-q:v", "3",
              str(QA / f"four_elements_v03_{name}.jpg"))

    uat = Path.home() / "Library/Mobile Documents/com~apple~CloudDocs/HOS UAT/002_How-Did-We-Discover-The-Periodic-Table/10_Shorts"
    nas_out = Path("/Volumes/data/mac-mini-archive/YouTube/History Of Science/02_Video-Projects/"
                   "002_How-Did-We-Discover-The-Periodic-Table/10_Shorts/four_elements_v03")
    copied = {}
    for folder in (uat, nas_out):
        folder.mkdir(parents=True, exist_ok=True)
        for src in (mp4, phone, sheet):
            dst = folder / src.name
            shutil.copy2(src, dst)
            if gf.sha256(src) != gf.sha256(dst):
                raise SystemExit(f"sha mismatch after copy: {dst}")
            copied[str(dst)] = gf.sha256(dst)
    manifest = {
        "job": JOB, "youtube_id": YT, "version": "v03",
        "master_sha256": gf.sha256(mp4), "phone_sha256": gf.sha256(phone),
        "v02_sha256": gf.sha256(V02), "copies": copied,
        "aac_lufs": round(aac_lufs, 2), "aac_true_peak_dbfs": round(aac_peak, 2),
    }
    (QA / "sha256_manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    (nas_out / "sha256_manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    summary = {
        "file": mp4.name, "sha256": gf.sha256(mp4), "duration_s": round(gf.probe(mp4), 3),
        "lufs": round(aac_lufs, 2), "true_peak_dbfs": round(aac_peak, 2),
        "gain_db": gain, "limiter_db": lim_db,
        "gate_exit": gate.returncode, "gate_verdict": gate_json.get("verdict"),
        "gate_fails": gate_json.get("fails"),
        "polish_exit": r_pg.returncode, "picture_exit": r_pq.returncode,
        "music_exit": music.returncode, "sfx_exit": r_sfx.returncode,
        "polish_tail": (r_pg.stdout + r_pg.stderr).strip().splitlines()[-4:],
        "picture_tail": (r_pq.stdout + r_pq.stderr).strip().splitlines()[-4:],
        "music_tail": (music.stdout + music.stderr).strip().splitlines()[-3:],
        "sfx_tail": (r_sfx.stdout + r_sfx.stderr).strip().splitlines()[-3:],
        "v02_untouched": gf.sha256(V02) == V02_SHA,
    }
    (QA / "build_four_elements_v03.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))
    bad = [name for name, code, ok in (
        ("gate", gate.returncode, gate_json.get("verdict") == "PASS"),
        ("polish", r_pg.returncode, r_pg.returncode == 0),
        ("picture", r_pq.returncode, r_pq.returncode == 0),
        ("music", music.returncode, music.returncode == 0),
        ("sfx", r_sfx.returncode, r_sfx.returncode == 0),
    ) if not ok]
    if bad:
        raise SystemExit("FAIL " + ",".join(bad))


if __name__ == "__main__":
    main()
