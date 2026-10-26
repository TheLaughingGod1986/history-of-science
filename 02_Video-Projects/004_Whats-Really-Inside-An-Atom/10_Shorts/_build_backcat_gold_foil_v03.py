#!/usr/bin/env python3
"""HOS 004 gold-foil Short v03 (J0965 c51, £0). v01 and v02 are not opened for write.

Cards and a true-peak limiter only. VO words, frame 0, plates, cuts and the
loop stay as v02. ERNEST RUTHERFORD / Manchester, 1909 on 2.75–5.54.
"1 in 8,000" on 10.95–13.65. AAC target: -14.0 +/- 0.5 LUFS, true peak <= -1.5.

    python3 _build_backcat_gold_foil_v03.py
"""
from __future__ import annotations

import hashlib
import json
import math
import shutil
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
PROJ = REPO / "02_Video-Projects/004_Whats-Really-Inside-An-Atom"
OWB = Path("/Users/benjaminoats/YouTube/orbit-with-ben")
V02 = HERE / "hos_004_backcat_gold_foil_v02.mp4"
V02_META = HERE / "hos_004_backcat_gold_foil_v02_meta.json"
V02_SHA = "11e2b42a48820a4c10434ba4e5dbb2075fae509c98f9075d70e97352307b1292"
WORK = HERE / "_work_gold_foil_v03"
QA = HERE / "qa_gold_foil_v03"
STEMS = HERE / "_work_gold_foil_v02"
JOB, AIR, YT = "J0965", "2026-11-01", "JyRjM-9Yc8g"
W, H = 1080, 1920
FONT = "/System/Library/Fonts/Supplemental/Didot.ttc"
CTA_FONT = "/System/Library/Fonts/Supplemental/Times New Roman.ttf"
YEL, CREAM, INK = (255, 214, 70, 255), (245, 232, 210, 255), (28, 26, 28, 255)
# Lower third of the 16:9 band: under the top title shade, above the caption row.
WHO = ("ERNEST RUTHERFORD", "Manchester, 1909", 2.75, 5.54)
CALLOUT = ("1 in 8,000", 10.95, 13.65)
LIMIT_DB = -1.8  # measured: AAC lands at -14.4 LUFS / -1.7 dBTP


def ff(*a: str) -> None:
    subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", *a], check=True)


def sha256(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def probe(p: Path) -> float:
    out = subprocess.check_output(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)],
        text=True)
    return float(out.strip())


def measure(p: Path) -> tuple[float, float]:
    err = subprocess.run(
        ["ffmpeg", "-nostats", "-hide_banner", "-i", str(p), "-af", "ebur128=peak=true", "-f", "null", "-"],
        capture_output=True, text=True).stderr
    i_lines = [ln for ln in err.splitlines() if ln.strip().startswith("I:") and "LUFS" in ln]
    p_lines = [ln for ln in err.splitlines() if "Peak:" in ln and "dBFS" in ln]
    if not i_lines or not p_lines:
        raise SystemExit(f"ebur128 failed on {p}")
    lufs = float(i_lines[-1].split("I:")[1].split("LUFS")[0].strip())
    peak = float(p_lines[-1].split("Peak:")[1].split("dBFS")[0].strip())
    return lufs, peak


def fit_font(text: str, path: str, index: int, max_w: float, size: int) -> ImageFont.FreeTypeFont:
    while size > 28:
        font = ImageFont.truetype(path, size, index=index)
        if font.getlength(text) <= max_w:
            return font
        size -= 2
    return ImageFont.truetype(path, 28, index=index)


def shade_band(img: Image.Image, top: int, bot: int) -> None:
    shade = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(shade)
    span = max(1, bot - top)
    for yy in range(top, bot):
        ramp = min(1.0, (yy - top) / 80, (bot - yy) / 80, 1.0)
        # rise over the first and last 80 px; full weight in the middle
        edge = min((yy - top) / 80, (bot - yy) / 80, 1.0)
        wgt = 0.5 * (1.0 - math.cos(math.pi * edge))
        draw.line([(0, yy), (W, yy)], fill=(0, 0, 0, int(130 * wgt)))
    img.alpha_composite(shade)


def render_who(path: Path) -> dict:
    line1, line2, t0, t1 = WHO
    f1 = fit_font(line1, FONT, 2, W - 140, int(608 * 0.105))
    f2 = fit_font(line2, CTA_FONT, 0, W - 140, int(608 * 0.062))
    band_top = (H - 608) // 2
    y2 = band_top + 608 - 36
    y1 = y2 - f2.size - 18
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    shade_band(img, y1 - f1.size - 28, band_top + 608 + 8)
    d = ImageDraw.Draw(img)
    d.text((70, y1), line1, font=f1, anchor="ls", fill=YEL, stroke_width=4, stroke_fill=INK)
    d.text((70, y2), line2, font=f2, anchor="ls", fill=CREAM, stroke_width=3, stroke_fill=INK)
    img.save(path)
    return {"name": line1, "line2": line2, "t0": t0, "t1": t1, "style": "fabricius"}


def render_callout(path: Path) -> dict:
    text, t0, t1 = CALLOUT
    f1 = fit_font(text, FONT, 2, W - 160, int(608 * 0.16))
    band_top = (H - 608) // 2
    y1 = band_top + 608 - 48
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    shade_band(img, y1 - f1.size - 24, band_top + 608 + 8)
    d = ImageDraw.Draw(img)
    d.text((W / 2, y1), text, font=f1, anchor="ms", fill=YEL, stroke_width=4, stroke_fill=INK)
    img.save(path)
    return {"text": text, "t0": t0, "t1": t1, "style": "callout"}


def overlay_expr(t0: float, t1: float, tag: str, src: str, last: str) -> tuple[str, str]:
    dur = t1 - t0
    fade_in, fade_out = 0.40, 0.30
    out_st = max(fade_in + 0.05, dur - fade_out)
    x = f"if(lt(t\\,{t0 + fade_in:.3f})\\,-48*(1-(t-{t0:.3f})/{fade_in:.2f})\\,0)"
    chain = (
        f"{src}format=rgba,fade=t=in:st=0:d={fade_in:.2f}:alpha=1,"
        f"fade=t=out:st={out_st:.3f}:d={fade_out:.2f}:alpha=1,"
        f"setpts=PTS+{t0:.3f}/TB[{tag}]"
    )
    nxt = f"v{tag}"
    over = (
        f"{last}[{tag}]overlay=x='{x}':y=0:"
        f"enable='between(t,{t0:.3f},{t1:.3f})':eof_action=pass[{nxt}]"
    )
    return chain + ";" + over, f"[{nxt}]"


def main() -> None:
    if sha256(V02) != V02_SHA:
        raise SystemExit(f"v02 sha changed; refusing to build on a different master ({sha256(V02)[:12]})")
    if WORK.exists():
        shutil.rmtree(WORK)
    WORK.mkdir(parents=True)
    QA.mkdir(parents=True, exist_ok=True)
    base = json.loads(V02_META.read_text())
    who = render_who(WORK / "card_rutherford.png")
    call = render_callout(WORK / "card_8000.png")

    lin = 10 ** (LIMIT_DB / 20)
    mastered = WORK / "audio_master.m4a"
    ff("-i", str(V02), "-vn",
       "-af", f"alimiter=limit={lin:.5f}:level=disabled:attack=5:release=40",
       "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2", str(mastered))
    lufs, peak = measure(mastered)
    print(f"master AAC {lufs:.1f} LUFS  TP {peak:.1f}")
    if not (-14.5 <= lufs <= -13.5) or peak > -1.5:
        raise SystemExit(f"loudness {lufs:.2f} / {peak:.2f} is outside -14.0+/-0.5 and TP<=-1.5")

    d1, d2 = WHO[3] - WHO[2], CALLOUT[2] - CALLOUT[1]
    c1, last = overlay_expr(WHO[2], WHO[3], "who", "[1:v]", "[0:v]")
    c2, last = overlay_expr(CALLOUT[1], CALLOUT[2], "num", "[2:v]", last)
    fc = c1 + ";" + c2
    silent = WORK / "picture.mp4"
    ff("-i", str(V02),
       "-loop", "1", "-t", f"{d1:.3f}", "-i", str(WORK / "card_rutherford.png"),
       "-loop", "1", "-t", f"{d2:.3f}", "-i", str(WORK / "card_8000.png"),
       "-filter_complex", fc, "-map", last, "-an",
       "-c:v", "libx264", "-pix_fmt", "yuv420p", "-profile:v", "high",
       "-preset", "veryfast", "-crf", "18", "-r", "30", str(silent))
    mp4 = HERE / "hos_004_backcat_gold_foil_v03.mp4"
    ff("-i", str(silent), "-i", str(mastered),
       "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "copy",
       "-t", f"{probe(V02):.3f}", "-movflags", "+faststart", str(mp4))
    if sha256(V02) != V02_SHA:
        raise SystemExit("v02 was written during the v03 build")
    aac_lufs, aac_peak = measure(mp4)
    print(f"final AAC {aac_lufs:.1f} LUFS  TP {aac_peak:.1f}  dur {probe(mp4):.3f}")
    if not (-14.5 <= aac_lufs <= -13.5) or aac_peak > -1.5:
        raise SystemExit(f"final loudness {aac_lufs:.2f} / {aac_peak:.2f} missed the target")
    if abs(probe(mp4) - base["runtime_s"]) > 0.05:
        raise SystemExit(f"runtime moved: {probe(mp4):.3f} vs v02 {base['runtime_s']}")

    meta = dict(base)
    meta.update({
        "version": "v03",
        "job": JOB,
        "v02_untouched": True,
        "v02_sha256": V02_SHA,
        "changes": "true-peak limiter plus Rutherford card and 1 in 8,000 call-out",
        "who_card": who,
        "callout": call,
        "lufs": round(aac_lufs, 2),
        "true_peak_dbfs": round(aac_peak, 2),
        "loudness_note": (
            f"v02 AAC was -14.3 LUFS / -1.4 dBTP. alimiter ceiling {LIMIT_DB:.1f} dB "
            f"(level=disabled). Measured on the v03 AAC: {aac_lufs:.1f} LUFS, true peak {aac_peak:.1f} dBFS."
        ),
        "sha256": sha256(mp4),
        "runtime_s": round(probe(mp4), 3),
    })
    meta_path = HERE / "hos_004_backcat_gold_foil_v03_meta.json"
    meta_path.write_text(json.dumps(meta, indent=2) + "\n")

    spoken = WORK / "spoken.txt"
    spoken.write_text(base["spoken"] + "\n")
    vo = STEMS / "vo_trim.wav"
    gate = subprocess.run(
        [sys.executable, str(REPO / "00_Brand/Channel-Setup/tools/gate_shorts_open.py"),
         "check", str(mp4), "--air-date", AIR, "--id", YT,
         "--script", str(spoken), "--vo", str(vo), "--meta", str(meta_path), "--json"],
        capture_output=True, text=True)
    (QA / "gate_gold_foil_v03.txt").write_text((gate.stdout + gate.stderr).strip() + "\n")
    try:
        gate_json = json.loads(gate.stdout)
        if isinstance(gate_json, list):
            gate_json = gate_json[0]
    except json.JSONDecodeError:
        gate_json = {"verdict": "FAIL", "raw": (gate.stdout + gate.stderr)[-2000:]}
    (QA / "gate_gold_foil_v03.json").write_text(json.dumps(gate_json, indent=2) + "\n")
    (QA / "j0918_ship_gate_gold_foil_v03.txt").write_text(
        "J0918 HOS ship gate (Chief, 24 Oct 2026), read from gate_shorts_open. v03 cards + limiter.\n"
        f"verdict={gate_json.get('verdict')} frame0_diff={gate_json.get('frame0_diff_0_1_5s')} "
        f"first_cut_s={gate_json.get('first_cut_s')} vo_onset_s={gate_json.get('vo_onset_s')} "
        f"tail_gap_s={gate_json.get('tail_gap_s')} stayed_fails={gate_json.get('stayed_fails')}\n"
        f"fails={gate_json.get('fails')}\nwarns={gate_json.get('warns')}\n"
        f"aac_lufs={aac_lufs:.2f} aac_true_peak_dbfs={aac_peak:.2f}\n"
    )

    cuts_src = HERE / "qa_gold_foil_v02/cuts_gold_foil_v02.json"
    pool_src = HERE / "qa_gold_foil_v02/pool_gold_foil_v02.json"
    cuts = json.loads(cuts_src.read_text())
    cuts.append({
        "row": "card_rutherford", "timeline_in": WHO[2], "timeline_out": WHO[3],
        "source": "code_graphic_gold_foil_v03_rutherford.png", "upscale": 1.0,
        "video": False, "overlay": True, "framing": {"note": "lower third of 16:9 band"},
    })
    cuts.append({
        "row": "card_8000", "timeline_in": CALLOUT[1], "timeline_out": CALLOUT[2],
        "source": "code_graphic_gold_foil_v03_8000.png", "upscale": 1.0,
        "video": False, "overlay": True, "framing": {"note": "lower third of 16:9 band"},
    })
    cuts_f = QA / "cuts_gold_foil_v03.json"
    pool_f = QA / "pool_gold_foil_v03.json"
    pool = json.loads(pool_src.read_text())
    pool.append({"file_id": "code_graphic_gold_foil_v03_rutherford.png", "title": "ERNEST RUTHERFORD card"})
    pool.append({"file_id": "code_graphic_gold_foil_v03_8000.png", "title": "1 in 8,000 call-out"})
    cuts_f.write_text(json.dumps(cuts, indent=2) + "\n")
    pool_f.write_text(json.dumps(pool, indent=2) + "\n")
    rel = lambda p: str(p.relative_to(REPO))  # noqa: E731

    # Polish and picture QA score the plate rows, as v02 did. The cards are overlays on those plates.
    plate_cuts = QA / "cuts_gold_foil_v03_plates.json"
    plate_cuts.write_text(cuts_src.read_text())
    r_pg = subprocess.run(
        [sys.executable, str(OWB / "scripts/polish_gate.py"), rel(mp4),
         "--cuts", rel(plate_cuts), "--out", rel(QA / "polish_gate_gold_foil_v03.json")],
        cwd=REPO, capture_output=True, text=True)
    (QA / "polish_gate_gold_foil_v03.txt").write_text((r_pg.stdout + r_pg.stderr).strip() + "\n")
    r_pq = subprocess.run(
        [sys.executable, str(OWB / "scripts/picture_qa.py"), rel(mp4),
         "--cuts", rel(plate_cuts), "--pool", rel(pool_src),
         "--out-dir", rel(QA / "picture_qa_gold_foil_v03")],
        cwd=REPO, capture_output=True, text=True)
    (QA / "picture_qa_gold_foil_v03.txt").write_text((r_pq.stdout + r_pq.stderr).strip() + "\n")
    bed = PROJ / "05_Music" / "hos_004_backcat_gold_foil_v02_bed.wav"
    music = subprocess.run(
        [sys.executable, str(OWB / "scripts/music_gate.py"), str(PROJ),
         "--bed", str(bed), "--video", str(mp4),
         "--out", str(QA / "music_gate_gold_foil_v03.json")],
        capture_output=True, text=True)
    (QA / "music_gate_gold_foil_v03.txt").write_text((music.stdout + music.stderr).strip() + "\n")
    r_sfx = subprocess.run(
        [sys.executable, str(OWB / "scripts/sfx_kit.py"), "level",
         "--vo", str(STEMS / "stem_vo.wav"), "--sfx", str(STEMS / "stem_sfx.wav"),
         "--bed", str(STEMS / "stem_bed.wav"), "--minutes", f"{base['runtime_s'] / 60:.3f}",
         "--out", str(QA / "sfx_level.json")],
        capture_output=True, text=True)
    (QA / "sfx_level.txt").write_text((r_sfx.stdout + r_sfx.stderr).strip() + "\n")

    phone = HERE / "hos_004_backcat_gold_foil_v03_PHONE.mp4"
    ff("-i", str(mp4), "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "veryfast", "-crf", "26",
       "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart", str(phone))
    sheet = QA / "hos_004_backcat_gold_foil_v03_2fps_sheet.jpg"
    ff("-i", str(mp4), "-vf", "fps=2,scale=180:-2,tile=8x8", "-q:v", "4", str(sheet))
    for name, t in (("frame0", 0.05), ("title", 11.5), ("rutherford", 4.1), ("callout", 12.2)):
        ff("-ss", f"{t}", "-i", str(mp4), "-frames:v", "1", "-q:v", "3", str(QA / f"gold_foil_v03_{name}.jpg"))

    uat = Path.home() / "Library/Mobile Documents/com~apple~CloudDocs/HOS UAT/004_Whats-Really-Inside-An-Atom/10_Shorts"
    nas_out = Path("/Volumes/data/mac-mini-archive/YouTube/History Of Science/02_Video-Projects/"
                   "004_Whats-Really-Inside-An-Atom/10_Shorts/gold_foil_v03")
    copied = {}
    for folder in (uat, nas_out):
        folder.mkdir(parents=True, exist_ok=True)
        for src in (mp4, phone, sheet):
            dst = folder / src.name
            shutil.copy2(src, dst)
            if sha256(src) != sha256(dst):
                raise SystemExit(f"sha mismatch after copy: {dst}")
            copied[str(dst)] = sha256(dst)
    manifest = {
        "job": JOB, "youtube_id": YT, "version": "v03",
        "master_sha256": sha256(mp4), "phone_sha256": sha256(phone),
        "v02_sha256": sha256(V02), "copies": copied,
        "aac_lufs": round(aac_lufs, 2), "aac_true_peak_dbfs": round(aac_peak, 2),
    }
    (QA / "sha256_manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    (nas_out / "sha256_manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")

    summary = {
        "file": mp4.name, "sha256": sha256(mp4), "duration_s": round(probe(mp4), 3),
        "lufs": round(aac_lufs, 2), "true_peak_dbfs": round(aac_peak, 2),
        "gate_exit": gate.returncode, "gate_verdict": gate_json.get("verdict"),
        "gate_fails": gate_json.get("fails"), "gate_warns": gate_json.get("warns"),
        "polish_exit": r_pg.returncode, "picture_exit": r_pq.returncode,
        "music_exit": music.returncode, "sfx_exit": r_sfx.returncode,
        "polish_tail": (r_pg.stdout + r_pg.stderr).strip().splitlines()[-6:],
        "picture_tail": (r_pq.stdout + r_pq.stderr).strip().splitlines()[-6:],
        "music_tail": (music.stdout + music.stderr).strip().splitlines()[-6:],
        "sfx_tail": (r_sfx.stdout + r_sfx.stderr).strip().splitlines()[-4:],
        "v02_untouched": sha256(V02) == V02_SHA,
    }
    (QA / "build_gold_foil_v03.json").write_text(json.dumps(summary, indent=2) + "\n")
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
    if r_sfx.returncode != 0:
        bad.append("sfx")
    if bad:
        raise SystemExit("FAIL " + ",".join(bad))


if __name__ == "__main__":
    main()
