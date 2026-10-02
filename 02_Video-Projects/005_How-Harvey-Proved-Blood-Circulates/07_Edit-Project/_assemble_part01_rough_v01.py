#!/usr/bin/env python3
"""HOS 005 Part 01 rough v01: Vertex KEEP plates on the board windows + locked VO v01 + TEMP bed.

Picture: part-01_plates_v02.json t_s windows, KEEP takes from PART01_MINT_LOG_v01.json,
hard cuts (no freeze, no loop, no slow-mo), 1920x1080 30 fps CFR. The last plate runs
TAIL_S past the last VO word, then picture and music fade.
Audio: part01_the_used_up_blood_v01.mp3 unchanged + TEMP bed measured and set BED_REL_DB
under the VO's mean for the whole runtime.
Labels: white Didot italic side labels, one at a time, on the VO word (word times from
faster-whisper on the locked take).

  ~/.venvs/hos-vertex/bin/python 07_Edit-Project/_assemble_part01_rough_v01.py
"""
from __future__ import annotations

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
BOARD = EDIT / "parts/part-01_plates_v02.json"
LOG = EDIT / "PART01_MINT_LOG_v01.json"
VO = PROJ / "02_Voiceover/part01_the_used_up_blood_v01.mp3"
VO_SHA = "17ef3c420ba0239e7df30cddfa33f61fb480b72661c43ea81effadefd17f4c15"
BED = PROJ / "05_Music/hos005-part01-temp_score_bed_v01.mp3"
OUT = PROJ / "09_Final-Export/hos_005_part01_rough_v01.mp4"
META = EDIT / "part01_rough_v01_meta.json"
WORK = EDIT / "_part01_rough_v01_work"
ICLOUD = (Path.home() / "Library/Mobile Documents/com~apple~CloudDocs/HOS UAT"
          / "005_How-Harvey-Proved-Blood-Circulates/09_Final-Export" / OUT.name)

FPS, W, H = 30, 1920, 1080
TAIL_S = 2.5
BED_REL_DB = -20.0
DIDOT = "/System/Library/Fonts/Supplemental/Didot.ttc"
IN_S = {"01_pulse_wrist": 1.0}
LABELS = [
    (0.60, 2.80, "Your pulse"),
    (9.40, 11.80, "Made, then used up"),
    (12.70, 14.90, "One band"),
    (22.00, 23.00, "A sum"),
    (23.05, 24.05, "A band"),
    (24.10, 26.40, "Tiny doors"),
    (36.80, 39.40, "London, 1616"),
    (40.90, 43.40, "William Harvey"),
]
LABEL_FADE = 0.28


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
    if sha256(VO) != VO_SHA:
        raise SystemExit("STOP: Part 01 VO is not the locked v01 take")
    board = json.loads(BOARD.read_text())
    log = json.loads(LOG.read_text())
    plates = board["plates"]
    vo_dur = probe(VO)
    total = vo_dur + TAIL_S
    if probe(BED) < total:
        raise SystemExit("STOP: bed shorter than the part")
    missing = [p["id"] for p in plates if p["id"] not in log.get("plates", {})]
    if missing:
        raise SystemExit(f"STOP: plates without a KEEP: {missing}")
    for a, b, _ in LABELS:
        if b - a < 0.8:
            raise SystemExit("STOP: label shorter than 0.8 s")
    if any(LABELS[i][1] > LABELS[i + 1][0] for i in range(len(LABELS) - 1)):
        raise SystemExit("STOP: two labels on screen at once")

    WORK.mkdir(parents=True, exist_ok=True)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    starts = [float(p["t_s"]) for p in plates]
    normed, plate_meta = [], []
    for i, pl in enumerate(plates):
        t0 = starts[i]
        t1 = starts[i + 1] if i + 1 < len(plates) else total
        frames = int(round(t1 * FPS)) - int(round(t0 * FPS))
        use = frames / FPS
        src = REPO / log["plates"][pl["id"]]["keep"]
        in_s = IN_S.get(pl["id"], 0.0)
        if in_s + use > probe(src) + 1e-3:
            raise SystemExit(f"STOP: {pl['id']} needs {in_s + use:.2f}s of an {probe(src):.2f}s clip (no freeze-pad)")
        dst = WORK / f"n{i:02d}_{pl['id']}.mp4"
        run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-ss", f"{in_s:.3f}", "-i", str(src),
             "-vf", f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},fps={FPS},"
                    f"setsar=1,format=yuv420p",
             "-frames:v", str(frames), "-an", "-c:v", "libx264", "-preset", "veryfast", "-crf", "16",
             "-r", str(FPS), str(dst)])
        normed.append(dst)
        plate_meta.append({"id": pl["id"], "file": log["plates"][pl["id"]]["keep"],
                           "sha256": log["plates"][pl["id"]]["sha256"],
                           "model": log["plates"][pl["id"]]["model"], "path": "vertex",
                           "film_t0": round(int(round(t0 * FPS)) / FPS, 3), "use_s": round(use, 3),
                           "in_s": in_s, "vo_land": pl.get("vo_land")})

    concat = WORK / "concat.txt"
    concat.write_text("".join(f"file '{p}'\n" for p in normed))
    picture = WORK / "picture.mp4"
    run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-f", "concat", "-safe", "0",
         "-i", str(concat), "-c", "copy", str(picture)])

    label_pngs = []
    for k, (a, b, text) in enumerate(LABELS):
        png = WORK / f"label_{k:02d}.png"
        render_label(text, png)
        label_pngs.append((a, b, png))

    vo_db, bed_db = mean_db(VO), mean_db(BED)
    bed_gain_db = (vo_db + BED_REL_DB) - bed_db
    inputs = ["-i", str(picture), "-i", str(VO), "-i", str(BED)]
    for a, b, png in label_pngs:
        inputs += ["-loop", "1", "-t", f"{b - a:.3f}", "-framerate", str(FPS), "-i", str(png)]
    parts, cur = [], "[0:v]"
    for k, (a, b, _png) in enumerate(label_pngs):
        hold = b - a
        parts.append(f"[{3 + k}:v]format=rgba,fade=t=in:st=0:d={LABEL_FADE}:alpha=1,"
                     f"fade=t=out:st={hold - LABEL_FADE:.3f}:d={LABEL_FADE}:alpha=1,"
                     f"setpts=PTS+{a:.3f}/TB[lb{k}]")
        parts.append(f"{cur}[lb{k}]overlay=0:0:eof_action=pass[ov{k}]")
        cur = f"[ov{k}]"
    vfade = total - 1.0
    parts.append(f"{cur}fade=t=out:st={vfade:.3f}:d=1.0,format=yuv420p,setsar=1[v]")
    afade = vo_dur + 0.3
    # Mono VO → both channels at full level (a plain stereo aformat drops it 3 dB).
    parts.append(f"[1:a]aresample=48000,pan=stereo|c0=c0|c1=c0,apad,atrim=0:{total:.3f}[vo]")
    parts.append(f"[2:a]atrim=0:{total:.3f},asetpts=PTS-STARTPTS,volume={bed_gain_db:.2f}dB,"
                 f"afade=t=in:st=0:d=0.4,afade=t=out:st={afade:.3f}:d={total - afade:.3f},"
                 "aformat=sample_rates=48000:channel_layouts=stereo[bed]")
    parts.append("[vo][bed]amix=inputs=2:normalize=0:duration=first,alimiter=limit=0.89:level=false[a]")
    run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", *inputs,
         "-filter_complex", ";".join(parts), "-map", "[v]", "-map", "[a]",
         "-c:v", "libx264", "-preset", "medium", "-crf", "17", "-pix_fmt", "yuv420p",
         "-r", str(FPS), "-fps_mode", "cfr", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2",
         "-t", f"{total:.3f}", "-movflags", "+faststart", str(OUT)])

    ICLOUD.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(OUT, ICLOUD)
    streams = json.loads(subprocess.check_output(
        ["ffprobe", "-v", "error", "-show_entries", "stream=codec_type,width,height,r_frame_rate,"
         "avg_frame_rate,duration,channels,sample_rate", "-of", "json", str(OUT)], text=True))["streams"]
    meta = {
        "out": str(OUT), "icloud": str(ICLOUD), "sha256": sha256(OUT), "duration_s": probe(OUT),
        "streams": streams, "vo": str(VO.relative_to(REPO)), "vo_sha256": VO_SHA,
        "vo_duration_s": vo_dur, "tail_s": TAIL_S,
        "bed": {"temp": True, "file": str(BED.relative_to(REPO)), "sha256": sha256(BED),
                "vo_mean_db": vo_db, "bed_mean_db_raw": bed_db, "bed_gain_db": round(bed_gain_db, 2),
                "bed_rel_db_vs_vo": BED_REL_DB},
        "labels": [{"t0": a, "t1": b, "text": t} for a, b, t in LABELS],
        "cuts": "hard cuts on the board times (board xfade 0.35 s would need freeze-pad on 7.9 s plates)",
        "plates": plate_meta,
    }
    META.write_text(json.dumps(meta, indent=2, ensure_ascii=False) + "\n")
    print(f"SAVED {OUT}\nICLOUD {ICLOUD}\nsha256 {meta['sha256']}\nduration {meta['duration_s']:.3f}s "
          f"bed_gain {bed_gain_db:.2f} dB (VO mean {vo_db} dB, bed raw {bed_db} dB)")


if __name__ == "__main__":
    main()
