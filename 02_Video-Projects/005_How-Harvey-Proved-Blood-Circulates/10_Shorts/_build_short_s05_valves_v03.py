#!/usr/bin/env python3
"""HOS 005 valves Short v03 (J0965 c51, £0). v01 and v02 are not opened for write.

Re-lays the v02 hook, captions and title on the clean plate picture, so the
FABRICIUS card can end at the 7.82 cut instead of running over Harvey's hand.
Adds WILLIAM HARVEY / London, 1628 on 7.82–10.837. Gain plus a true-peak limiter.
VO words, frame 0, plates, cuts and the loop stay as v02.
AAC target: -14.0 +/- 0.5 LUFS, true peak <= -1.5.

    python3 _build_short_s05_valves_v03.py
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
V02 = HERE / "hos_005_s05_valves_v02.mp4"
V02_META = HERE / "hos_005_s05_valves_v02_meta.json"
V02_SHA = "ed9b7f084a2e875e8e09fd7995c0b4eeecbb044a3699665d5a409671d91ab664"
SRC = HERE / "_work_s05_valves_v02"
WORK = HERE / "_work_s05_valves_v03"
QA = HERE / "qa_s05_valves_v03"
JOB, AIR, YT = "J0965", "2026-11-05", "PlihWC5uA2E"
W, H = gf.W, gf.H
FAB = (6.150, 7.820)
HARVEY = ("WILLIAM HARVEY", "London, 1628", 7.820, 10.837)
CHUNK_MAX_S, CHUNK_MAX_WORDS, CHUNK_MIN_S = 1.55, 5, 0.45


def chunk_words(words: list[tuple[str, float, float]]) -> list[dict]:
    chunks, i, n = [], 0, len(words)
    while i < n:
        t0 = words[i][1]
        parts, t_end, j = [words[i][0]], words[i][2], i + 1
        while j < n:
            wj, sj, ej = words[j]
            if parts[-1][-1:] in ".?!":
                break
            if parts[-1][-1:] in ",;:" and len(parts) >= 2 and sj - t0 >= CHUNK_MIN_S:
                break
            if len(parts) >= CHUNK_MAX_WORDS and sj - t0 >= CHUNK_MIN_S:
                break
            if ej - t0 >= CHUNK_MAX_S and len(parts) >= 2:
                break
            parts.append(wj)
            t_end = ej
            j += 1
        t1 = words[j][1] if j < n else t_end + 0.25
        chunks.append({"text": " ".join(parts), "t0": round(t0, 3), "t1": round(t1, 3)})
        i = j
    return chunks


def render_who(path: Path) -> dict:
    line1, line2, t0, t1 = HARVEY
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
    if gf.sha256(V02) != V02_SHA:
        raise SystemExit(f"v02 sha changed ({gf.sha256(V02)[:12]})")
    pic = SRC / "picture.mp4"
    if not pic.exists():
        raise SystemExit("clean v02 picture is missing")
    if WORK.exists():
        shutil.rmtree(WORK)
    WORK.mkdir(parents=True)
    QA.mkdir(parents=True, exist_ok=True)
    base = json.loads(V02_META.read_text())
    words = [(w["word"], w["start"], w["end"]) for w in base["words"]]
    total = base["runtime_s"]
    chunks = chunk_words(words)
    caps = [SRC / f"cap_{i:03d}.png" for i in range(len(chunks))]
    missing = [p.name for p in caps if not p.exists()]
    if missing:
        raise SystemExit(f"caption pngs missing: {missing[:6]}")
    for need in ("cap_hook.png", "cap_title.png", "cap_who.png"):
        if not (SRC / need).exists():
            raise SystemExit(f"missing {need}")
    who = render_who(WORK / "card_harvey.png")
    fab_meta = {"name": "FABRICIUS", "line2": "Padua, c. 1600", "t0": FAB[0], "t1": FAB[1],
                "style": "fabricius", "note": "ended at the 7.82 cut, was 6.15–9.35 on v02"}

    layers: list[tuple[Path, float, float, str]] = [(SRC / "cap_hook.png", 0.0, 2.20, "static")]
    for png, c in zip(caps, chunks):
        layers.append((png, c["t0"], min(c["t1"], total - 0.05), "static"))
    layers.append((SRC / "cap_title.png", 9.0, 14.0, "static"))
    layers.append((SRC / "cap_who.png", FAB[0], FAB[1], "card"))
    layers.append((WORK / "card_harvey.png", HARVEY[2], HARVEY[3], "card"))

    mastered = WORK / "audio_master.m4a"
    gain, lim_db, _a, _b = master_audio(V02, mastered)

    inputs = ["-i", str(pic)]
    fc_parts, last = [], "[0:v]"
    for i, (png, t0, t1, kind) in enumerate(layers, 1):
        inputs += ["-loop", "1", "-t", f"{max(0.05, t1 - t0):.3f}", "-i", str(png)]
        if kind == "static":
            nxt = f"s{i}"
            fc_parts.append(
                f"[{i}:v]setpts=PTS+{t0:.3f}/TB[p{i}];"
                f"{last}[p{i}]overlay=0:0:enable='between(t,{t0:.3f},{t1:.3f})':eof_action=pass[{nxt}]")
            last = f"[{nxt}]"
        else:
            part, last = gf.overlay_expr(t0, t1, f"c{i}", f"[{i}:v]", last)
            fc_parts.append(part)
    silent = WORK / "picture.mp4"
    gf.ff(*inputs, "-filter_complex", ";".join(fc_parts), "-map", last, "-an",
          "-c:v", "libx264", "-pix_fmt", "yuv420p", "-profile:v", "high",
          "-preset", "veryfast", "-crf", "18", "-r", "30", str(silent))
    mp4 = HERE / "hos_005_s05_valves_v03.mp4"
    gf.ff("-i", str(silent), "-i", str(mastered), "-map", "0:v", "-map", "1:a",
          "-c:v", "copy", "-c:a", "copy", "-t", f"{gf.probe(V02):.3f}",
          "-movflags", "+faststart", str(mp4))
    if gf.sha256(V02) != V02_SHA:
        raise SystemExit("v02 was written during the v03 build")
    aac_lufs, aac_peak = gf.measure(mp4)
    print(f"final AAC {aac_lufs:.1f} LUFS  TP {aac_peak:.1f}  dur {gf.probe(mp4):.3f}")
    if not (-14.5 <= aac_lufs <= -13.5) or aac_peak > -1.5:
        raise SystemExit(f"final loudness {aac_lufs:.2f} / {aac_peak:.2f}")
    if abs(gf.probe(mp4) - total) > 0.08:
        raise SystemExit("runtime moved")

    meta = dict(base)
    meta.update({
        "version": "v03", "job": JOB, "v02_untouched": True, "v02_sha256": V02_SHA,
        "changes": "FABRICIUS ends at 7.82; WILLIAM HARVEY card; true-peak limiter",
        "who_card": fab_meta, "harvey_card": who,
        "lufs": round(aac_lufs, 2), "true_peak_dbfs": round(aac_peak, 2),
        "loudness_note": (
            f"v02 AAC was -14.7 LUFS / -0.9 dBTP. volume {gain:+.1f} dB then "
            f"alimiter ceiling {lim_db:.1f} dB. Measured on the v03 AAC: "
            f"{aac_lufs:.1f} LUFS, true peak {aac_peak:.1f} dBFS."
        ),
        "sha256": gf.sha256(mp4), "runtime_s": round(gf.probe(mp4), 3),
    })
    meta_path = HERE / "hos_005_s05_valves_v03_meta.json"
    meta_path.write_text(json.dumps(meta, indent=2) + "\n")
    gate = subprocess.run(
        [sys.executable, str(REPO / "00_Brand/Channel-Setup/tools/gate_shorts_open.py"),
         "check", str(mp4), "--air-date", AIR, "--id", YT,
         "--script", str(SRC / "spoken.txt"), "--vo", str(SRC / "vo_trim.wav"),
         "--meta", str(meta_path), "--json"],
        capture_output=True, text=True)
    (QA / "gate_s05_valves_v03.txt").write_text((gate.stdout + gate.stderr).strip() + "\n")
    try:
        gate_json = json.loads(gate.stdout)
        if isinstance(gate_json, list):
            gate_json = gate_json[0]
    except json.JSONDecodeError:
        gate_json = {"verdict": "FAIL", "raw": (gate.stdout + gate.stderr)[-2000:]}
    (QA / "gate_s05_valves_v03.json").write_text(json.dumps(gate_json, indent=2) + "\n")
    (QA / "j0918_ship_gate_s05_valves_v03.txt").write_text(
        "J0918 HOS ship gate, v03 Fabricius ends 7.82, Harvey card, master.\n"
        f"verdict={gate_json.get('verdict')} frame0_diff={gate_json.get('frame0_diff_0_1_5s')} "
        f"first_cut_s={gate_json.get('first_cut_s')} vo_onset_s={gate_json.get('vo_onset_s')} "
        f"tail_gap_s={gate_json.get('tail_gap_s')} stayed_fails={gate_json.get('stayed_fails')}\n"
        f"fails={gate_json.get('fails')}\nwarns={gate_json.get('warns')}\n"
        f"aac_lufs={aac_lufs:.2f} aac_true_peak_dbfs={aac_peak:.2f}\n"
    )
    cuts_src = HERE / "qa_s05_valves_v02/cuts_s05_valves_v02.json"
    pool_src = HERE / "qa_s05_valves_v02/pool_s05_valves_v02.json"
    plate = QA / "cuts_s05_valves_v03_plates.json"
    plate.write_text(cuts_src.read_text())
    cuts = json.loads(cuts_src.read_text())
    cuts.append({"row": "card_fabricius", "timeline_in": FAB[0], "timeline_out": FAB[1],
                 "source": "code_graphic_valves_v03_fabricius.png", "upscale": 1.0,
                 "video": False, "overlay": True})
    cuts.append({"row": "card_harvey", "timeline_in": HARVEY[2], "timeline_out": HARVEY[3],
                 "source": "code_graphic_valves_v03_harvey.png", "upscale": 1.0,
                 "video": False, "overlay": True})
    (QA / "cuts_s05_valves_v03.json").write_text(json.dumps(cuts, indent=2) + "\n")
    pool = json.loads(pool_src.read_text())
    pool += [
        {"file_id": "code_graphic_valves_v03_fabricius.png", "title": "FABRICIUS card"},
        {"file_id": "code_graphic_valves_v03_harvey.png", "title": "WILLIAM HARVEY card"},
    ]
    (QA / "pool_s05_valves_v03.json").write_text(json.dumps(pool, indent=2) + "\n")
    rel = lambda p: str(p.relative_to(REPO))  # noqa: E731
    r_pg = subprocess.run([sys.executable, str(OWB / "scripts/polish_gate.py"), rel(mp4),
                           "--cuts", rel(plate), "--out", rel(QA / "polish_gate_s05_valves_v03.json")],
                          cwd=REPO, capture_output=True, text=True)
    (QA / "polish_gate_s05_valves_v03.txt").write_text((r_pg.stdout + r_pg.stderr).strip() + "\n")
    r_pq = subprocess.run([sys.executable, str(OWB / "scripts/picture_qa.py"), rel(mp4),
                           "--cuts", rel(plate), "--pool", rel(pool_src),
                           "--out-dir", rel(QA / "picture_qa_s05_valves_v03")],
                          cwd=REPO, capture_output=True, text=True)
    (QA / "picture_qa_s05_valves_v03.txt").write_text((r_pq.stdout + r_pq.stderr).strip() + "\n")
    bed = PROJ / "05_Music" / base["bed"]
    music = subprocess.run([sys.executable, str(OWB / "scripts/music_gate.py"), str(PROJ),
                            "--bed", str(bed), "--video", str(mp4),
                            "--out", str(QA / "music_gate_s05_valves_v03.json")],
                           capture_output=True, text=True)
    (QA / "music_gate_s05_valves_v03.txt").write_text((music.stdout + music.stderr).strip() + "\n")
    r_sfx = subprocess.run([sys.executable, str(OWB / "scripts/sfx_kit.py"), "level",
                            "--vo", str(SRC / "stem_vo.wav"), "--sfx", str(SRC / "stem_sfx.wav"),
                            "--bed", str(SRC / "stem_bed.wav"),
                            "--minutes", f"{total / 60:.3f}", "--out", str(QA / "sfx_level.json")],
                           capture_output=True, text=True)
    (QA / "sfx_level.txt").write_text((r_sfx.stdout + r_sfx.stderr).strip() + "\n")
    phone = HERE / "hos_005_s05_valves_v03_PHONE.mp4"
    gf.ff("-i", str(mp4), "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "veryfast", "-crf", "26",
          "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart", str(phone))
    sheet = QA / "hos_005_s05_valves_v03_2fps_sheet.jpg"
    gf.ff("-i", str(mp4), "-vf", "fps=2,scale=180:-2,tile=8x8", "-q:v", "4", str(sheet))
    for name, t in (("frame0", 0.05), ("fabricius", 7.0), ("harvey", 9.2)):
        gf.ff("-ss", f"{t}", "-i", str(mp4), "-frames:v", "1", "-q:v", "3",
              str(QA / f"valves_v03_{name}.jpg"))
    uat = Path.home() / "Library/Mobile Documents/com~apple~CloudDocs/HOS UAT/005_How-Harvey-Proved-Blood-Circulates/10_Shorts"
    nas_out = Path("/Volumes/data/mac-mini-archive/YouTube/History Of Science/02_Video-Projects/"
                   "005_How-Harvey-Proved-Blood-Circulates/10_Shorts/valves_v03")
    copied = {}
    for folder in (uat, nas_out):
        folder.mkdir(parents=True, exist_ok=True)
        for src in (mp4, phone, sheet):
            dst = folder / src.name
            shutil.copy2(src, dst)
            if gf.sha256(src) != gf.sha256(dst):
                raise SystemExit(f"sha mismatch {dst}")
            copied[str(dst)] = gf.sha256(dst)
    manifest = {"job": JOB, "youtube_id": YT, "version": "v03",
                "master_sha256": gf.sha256(mp4), "phone_sha256": gf.sha256(phone),
                "v02_sha256": gf.sha256(V02), "copies": copied,
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
        "v02_untouched": True,
    }
    (QA / "build_s05_valves_v03.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))
    bad = []
    if gate_json.get("verdict") != "PASS":
        bad.append("gate")
    for name, code in (("polish", r_pg.returncode), ("picture", r_pq.returncode),
                       ("music", music.returncode), ("sfx", r_sfx.returncode)):
        if code:
            bad.append(name)
    if bad:
        raise SystemExit("FAIL " + ",".join(bad))


if __name__ == "__main__":
    main()
