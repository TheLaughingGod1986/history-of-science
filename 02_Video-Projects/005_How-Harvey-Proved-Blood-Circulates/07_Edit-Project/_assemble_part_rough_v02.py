#!/usr/bin/env python3
"""HOS 005 Parts 02–05 rough v01: Vertex KEEP plates on the board windows + locked VO v01 + TEMP bed.

Part 01's assembler, per part. Board times are on the film timeline; the part rough runs from the
part's first VO word (film time vo_film_start_s = part time 0). Hard cuts, no freeze, no loop,
1920x1080 30 fps CFR. The last plate runs up to TAIL_S past the last VO word (as much as its clip
has left, at least 0.5 s), then picture and music fade.
VO: the board's vo_file unchanged (sha checked) + TEMP bed BED_REL_DB under the VO mean.
Labels: white Didot italic, top right, one at a time (LABELS: plate id → offset into the plate, text).
Chapter cards are added in the full join, not here.

  ~/.venvs/hos-vertex/bin/python 07_Edit-Project/_assemble_part_rough_v02.py --part N
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

PROJ = Path(__file__).resolve().parents[1]
REPO = PROJ.parents[1]
EDIT = PROJ / "07_Edit-Project"
ICLOUD_DIR = (Path.home() / "Library/Mobile Documents/com~apple~CloudDocs/HOS UAT"
              / "005_How-Harvey-Proved-Blood-Circulates/09_Final-Export")

FPS, W, H = 30, 1920, 1080
TAIL_S = 2.5
# Part → shorter tail where the VO's own trailing silence + TAIL_S would exceed vo_check's 1.5 s silence limit.
TAIL_S_PART: dict[str, float] = {"04": 2.0}
BED_REL_DB = -20.0
DIDOT = "/System/Library/Fonts/Supplemental/Didot.ttc"
LABEL_FADE = 0.28
LABEL_HOLD = 2.4

# Part → plate id → in-point into the KEEP clip (s).
IN_S: dict[str, dict[str, float]] = {"02": {}, "03": {}, "04": {"01_college_demo": 1.9, "08_knots_valve": 0.1, "11_two_fingers": 4.0}, "05": {}}
# Part → plate id → (offset into the plate's window, label text).
LABELS: dict[str, dict[str, tuple[float, str]]] = {
    "02": {
        "01_galen_scrolls": (0.5, "Galen · Rome, c. AD 170"),
        "03_eat_to_liver": (2.2, "Food → liver → blood"),
        "05_heart_stove": (0.5, "A stove, not a pump"),
        "06_septum_holes": (0.6, "Invisible holes?"),
        "08_vesalius_book": (0.6, "Andreas Vesalius, 1555"),
        "11_padua_explorer": (0.5, "Padua, c. 1600"),
        "12_fabricius": (2.0, "Fabricius"),
        "13_little_doors": (0.6, "Little doors"),
    },
    "03": {
        "01_cold_lecture_room": (0.6, "London, 1616"),
        "02_slow_hearts": (0.8, "Slow hearts"),
        "03_stove_to_muscle": (4.2, "A muscle"),
        "04_squeeze_pulse": (0.8, "Squeeze = pulse"),
        "07_thousand_beats": (0.6, "1,000 beats"),
        "09_jug_tower": (0.6, "More than your whole body"),
        "12_glowing_loop": (5.4, "The same blood → it circulates"),
        "13_one_minute": (1.0, "One lap · one minute"),
    },
    "04": {
        "01_college_demo": (0.6, "Nine years"),
        "02_linen_tie": (3.5, "A tight band"),
        "03_hand_pale": (0.6, "No blood in"),
        "05_arteries_veins_shut": (0.6, "Deep arteries"),
        "07_in_out_doors": (0.6, "In: arteries · out: veins"),
        "08_knots_valve": (3.6, "A valve"),
        "13_one_way": (0.6, "One way: to the heart"),
        "16_press_book": (2.6, "De Motu Cordis, 1628"),
        "18_aubrey": (0.6, "John Aubrey"),
    },
    "05": {
        "01_loop_gap": (0.6, "How does it cross?"),
        "03_old_harvey": (0.6, "William Harvey · 1578–1657"),
        "04_malpighi_slide": (0.6, "Marcello Malpighi · Bologna 1661"),
        "06_eyepiece_mesh": (0.6, "Capillaries"),
        "11_transfusion": (0.6, "First transfusions · 1660s"),
        "13_cuff": (0.6, "Harvey's band, today"),
    },
}


def sha256(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def probe(p: Path) -> float:
    return float(subprocess.check_output(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=nw=1:nk=1", str(p)], text=True).strip())


def mean_db(p: Path) -> float:
    err = subprocess.run(["ffmpeg", "-hide_banner", "-i", str(p), "-af", "volumedetect",
                          "-f", "null", "-"], capture_output=True, text=True).stderr
    return float(re.search(r"mean_volume: (-?[\d.]+) dB", err).group(1))


def run(cmd: list[str]) -> None:
    subprocess.run(cmd, check=True)


def render_label(text: str, dest: Path) -> None:
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    fnt = ImageFont.truetype(DIDOT, 56, index=1)
    d = ImageDraw.Draw(im)
    bb = d.textbbox((0, 0), text, font=fnt)
    x, y = W - (bb[2] - bb[0]) - 88, 86
    shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(shadow).text((x + 1, y + 2), text, font=fnt, fill=(8, 6, 4, 160))
    im = Image.alpha_composite(im, shadow.filter(ImageFilter.GaussianBlur(radius=1.6)))
    ImageDraw.Draw(im).text((x, y), text, font=fnt, fill=(246, 240, 230, 245))
    im.save(dest)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--part", required=True)
    ap.add_argument("--version", default="v01")
    a = ap.parse_args()
    part = f"{int(a.part):02d}"
    board = json.loads((EDIT / f"parts/part-{part}_plates_v02.json").read_text())
    log = json.loads((EDIT / f"PART{part}_MINT_LOG_v01.json").read_text())
    vo = PROJ / board["vo_file"]
    bed = PROJ / f"05_Music/hos005-part{part}-temp_score_bed_v01.mp3"
    out = PROJ / f"09_Final-Export/hos_005_part{part}_rough_{a.version}.mp4"
    meta_path = EDIT / f"part{part}_rough_{a.version}_meta.json"
    work = EDIT / f"_part{part}_rough_{a.version}_work"
    if sha256(vo) != board["vo_sha256"]:
        raise SystemExit(f"STOP: Part {part} VO is not the locked v01 take")
    plates = board["plates"]
    t_film0 = float(board["vo_film_start_s"])
    starts = [round(float(p["t_s"]) - t_film0, 3) for p in plates]
    if abs(starts[0]) > 0.05:
        raise SystemExit(f"STOP: first plate starts {starts[0]}s from the part's first word")
    starts[0] = 0.0
    vo_dur = probe(vo)
    missing = [p["id"] for p in plates if p["id"] not in log.get("plates", {})]
    if missing:
        raise SystemExit(f"STOP: plates without a KEEP: {missing}")
    last = plates[-1]["id"]
    last_left = (probe(REPO / log["plates"][last]["keep"]) - IN_S[part].get(last, 0.0)
                 - (vo_dur - starts[-1]))
    tail_s = round(min(TAIL_S_PART.get(part, TAIL_S), last_left - 0.05), 3)
    if tail_s < 0.5:
        raise SystemExit(f"STOP: last plate leaves only {last_left:.2f}s after the last word")
    total = vo_dur + tail_s
    if probe(bed) < total:
        raise SystemExit("STOP: bed shorter than the part")

    ids = [p["id"] for p in plates]
    labels = []
    for pid, (off, text) in sorted(LABELS[part].items(), key=lambda kv: starts[ids.index(kv[0])] + kv[1][0]):
        t0 = starts[ids.index(pid)] + off
        labels.append([t0, t0 + LABEL_HOLD, text])
    for i in range(len(labels) - 1):
        labels[i][1] = min(labels[i][1], labels[i + 1][0] - 0.15)
    for t0, t1, text in labels:
        if t1 - t0 < 0.8:
            raise SystemExit(f"STOP: label shorter than 0.8 s: {text}")

    work.mkdir(parents=True, exist_ok=True)
    out.parent.mkdir(parents=True, exist_ok=True)
    normed, plate_meta = [], []
    for i, pl in enumerate(plates):
        t0 = starts[i]
        t1 = starts[i + 1] if i + 1 < len(plates) else total
        frames = int(round(t1 * FPS)) - int(round(t0 * FPS))
        use = frames / FPS
        keep = log["plates"][pl["id"]]
        src = REPO / keep["keep"]
        in_s = IN_S[part].get(pl["id"], 0.0)
        if in_s + use > probe(src) + 1e-3:
            raise SystemExit(f"STOP: {pl['id']} needs {in_s + use:.2f}s of an {probe(src):.2f}s clip (no freeze-pad)")
        dst = work / f"n{i:02d}_{pl['id']}.mp4"
        run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-ss", f"{in_s:.3f}", "-i", str(src),
             "-vf", f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},fps={FPS},"
                    f"setsar=1,format=yuv420p",
             "-frames:v", str(frames), "-an", "-c:v", "libx264", "-preset", "veryfast", "-crf", "16",
             "-r", str(FPS), str(dst)])
        normed.append(dst)
        plate_meta.append({"id": pl["id"], "file": keep["keep"], "sha256": keep["sha256"],
                           "model": keep["model"], "path": "vertex", "take": keep["take"],
                           "part_t0": round(int(round(t0 * FPS)) / FPS, 3), "film_t0": round(t0 + t_film0, 3),
                           "use_s": round(use, 3), "in_s": in_s, "vo_land": pl.get("vo_land")})

    concat = work / "concat.txt"
    concat.write_text("".join(f"file '{p}'\n" for p in normed))
    picture = work / "picture.mp4"
    run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-f", "concat", "-safe", "0",
         "-i", str(concat), "-c", "copy", str(picture)])

    label_pngs = []
    for k, (t0, t1, text) in enumerate(labels):
        png = work / f"label_{k:02d}.png"
        render_label(text, png)
        label_pngs.append((t0, t1, png))

    vo_db, bed_db = mean_db(vo), mean_db(bed)
    bed_gain_db = (vo_db + BED_REL_DB) - bed_db
    inputs = ["-i", str(picture), "-i", str(vo), "-i", str(bed)]
    for t0, t1, png in label_pngs:
        inputs += ["-loop", "1", "-t", f"{t1 - t0:.3f}", "-framerate", str(FPS), "-i", str(png)]
    parts, cur = [], "[0:v]"
    for k, (t0, t1, _png) in enumerate(label_pngs):
        hold = t1 - t0
        parts.append(f"[{3 + k}:v]format=rgba,fade=t=in:st=0:d={LABEL_FADE}:alpha=1,"
                     f"fade=t=out:st={hold - LABEL_FADE:.3f}:d={LABEL_FADE}:alpha=1,"
                     f"setpts=PTS+{t0:.3f}/TB[lb{k}]")
        parts.append(f"{cur}[lb{k}]overlay=0:0:eof_action=pass[ov{k}]")
        cur = f"[ov{k}]"
    parts.append(f"{cur}fade=t=out:st={total - 1.0:.3f}:d=1.0,format=yuv420p,setsar=1[v]")
    afade = vo_dur + 0.3
    parts.append(f"[1:a]aresample=48000,pan=stereo|c0=c0|c1=c0,apad,atrim=0:{total:.3f}[vo]")
    parts.append(f"[2:a]atrim=0:{total:.3f},asetpts=PTS-STARTPTS,volume={bed_gain_db:.2f}dB,"
                 f"afade=t=in:st=0:d=0.4,afade=t=out:st={afade:.3f}:d={total - afade:.3f},"
                 "aformat=sample_rates=48000:channel_layouts=stereo[bed]")
    parts.append("[vo][bed]amix=inputs=2:normalize=0:duration=first,alimiter=limit=0.89:level=false[a]")
    run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", *inputs,
         "-filter_complex", ";".join(parts), "-map", "[v]", "-map", "[a]",
         "-c:v", "libx264", "-preset", "medium", "-crf", "17", "-pix_fmt", "yuv420p",
         "-r", str(FPS), "-fps_mode", "cfr", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2",
         "-t", f"{total:.3f}", "-movflags", "+faststart", str(out)])

    icloud = ICLOUD_DIR / out.name
    ICLOUD_DIR.mkdir(parents=True, exist_ok=True)
    shutil.copy2(out, icloud)
    streams = json.loads(subprocess.check_output(
        ["ffprobe", "-v", "error", "-show_entries", "stream=codec_type,width,height,r_frame_rate,"
         "avg_frame_rate,duration,channels,sample_rate", "-of", "json", str(out)], text=True))["streams"]
    err = subprocess.run(["ffmpeg", "-hide_banner", "-i", str(out), "-vf", "freezedetect=n=0.003:d=0.8",
                          "-an", "-f", "null", "-"], capture_output=True, text=True, errors="replace").stderr
    meta = {
        "out": str(out), "icloud": str(icloud), "sha256": sha256(out), "duration_s": probe(out),
        "streams": streams, "freeze_events_0p8s": err.count("freeze_start"),
        "vo": board["vo_file"], "vo_sha256": board["vo_sha256"], "vo_duration_s": vo_dur,
        "vo_film_start_s": t_film0, "tail_s": tail_s,
        "bed": {"temp": True, "file": str(bed.relative_to(REPO)), "sha256": sha256(bed),
                "vo_mean_db": vo_db, "bed_mean_db_raw": bed_db, "bed_gain_db": round(bed_gain_db, 2),
                "bed_rel_db_vs_vo": BED_REL_DB},
        "labels": [{"t0": round(t0, 3), "t1": round(t1, 3), "text": t} for t0, t1, t in labels],
        "cuts": "hard cuts on the board times",
        "plates": plate_meta,
    }
    meta_path.write_text(json.dumps(meta, indent=2, ensure_ascii=False) + "\n")
    print(f"SAVED {out}\nICLOUD {icloud}\nsha256 {meta['sha256']}\nduration {meta['duration_s']:.3f}s "
          f"freeze_events {meta['freeze_events_0p8s']} bed_gain {bed_gain_db:.2f} dB")


if __name__ == "__main__":
    main()
