#!/usr/bin/env python3
"""HOS 006 Part 03 rough v01 (J0137): the 16 kept Vertex takes on the locked v02 VO. No spend.

VO-first, like Part 02 rough v02: every plate sits at its board time (parts/part-03_plates_v01.json, t_s from
vo_film_start_s) for its board use_s, hard cuts, 24 fps 1080p. Row 16_repair_reuse is the 3.00-6.84 s window of
14_trees_breathe. P3:06_leeds_brewery is a Flow plate minted after the Mon 12 Oct refill (J0140), so its slot holds a
labelled plate board of the right length. Picture runs to part_end_film_s; the VO is padded with silence to match.

Media stays out of git: the cut and scratch go to _precheck/part03_rough_v01/; the meta, cut list, freeze log and
contact sheet are copied to _desk/006/part03_rough_v01/ for the PR
(picture_qa.py --out-dir there adds PICTURE_QA.md, picture_qa.json and picture_qa_review.jpg).

  python3 _assemble_part03_rough_v01.py [--uat-dir "<iCloud HOS UAT>"]
"""
import argparse
import hashlib
import json
import shutil
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
FILM = HERE.parent
BOARD = HERE / "parts" / "part-03_plates_v01.json"
MINT_LOG = HERE / "PART03_MINT_LOG_v01.json"
OUT = HERE / "_precheck" / "part03_rough_v01"
DESK = HERE / "_desk" / "006" / "part03_rough_v01"
FPS = 24
W, H = 1920, 1080
NAME = "hos_006_part03_rough_v01"
X264 = ["-c:v", "libx264", "-preset", "medium", "-crf", "17", "-pix_fmt", "yuv420p", "-r", str(FPS)]
FONT = "/System/Library/Fonts/Supplemental/Georgia Italic.ttf"


def run(cmd):
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def probe_dur(p: Path) -> float:
    return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                          "-of", "csv=p=0", str(p)]).decode().strip())


def keep_files() -> dict:
    """{plate: kept take} from the mint log on origin/main (the KEEP marks land there), sha-checked on disk."""
    rel = MINT_LOG.relative_to(FILM.parents[1])
    try:
        log = json.loads(subprocess.check_output(["git", "-C", str(HERE), "show", f"origin/main:{rel}"]))
    except subprocess.CalledProcessError:
        log = json.loads(MINT_LOG.read_text())
    out = {}
    for t in log["takes"]:
        if t.get("status") == "KEEP":
            f = FILM.parents[1] / t["file"]
            assert sha(f) == t["sha256"], f"{t['plate']}: file on disk does not match the KEEP sha"
            out[t["plate"]] = f
    return out


def placeholder_png(plate: dict, path: Path):
    img = Image.new("RGB", (W, H), (58, 64, 74))
    d = ImageDraw.Draw(img)
    big, mid = ImageFont.truetype(FONT, 88), ImageFont.truetype(FONT, 52)
    lines = [(f"P3:06 · {plate['side_label']}", big, (240, 236, 226)),
             ("Flow plate pending (J0140)", mid, (214, 206, 190)),
             (f"placeholder · {plate['use_s']:.2f} s · {plate['t']}", mid, (190, 184, 172))]
    y = H // 2 - 150
    for text, font, fill in lines:
        w = d.textlength(text, font=font)
        d.text(((W - w) / 2, y), text, font=font, fill=fill)
        y += 130
    img.save(path)


def contact_sheet(video: Path, cuts: list, path: Path):
    cols, tw, th = 6, 320, 180
    rows = (len(cuts) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * tw, rows * (th + 28)), (20, 20, 20))
    d = ImageDraw.Draw(sheet)
    f = ImageFont.truetype(FONT, 18)
    for i, c in enumerate(cuts):
        mid = (c["timeline_in"] + c["timeline_out"]) / 2
        jpg = OUT / f"_sheet_{i:02d}.jpg"
        run(["ffmpeg", "-y", "-ss", f"{mid:.3f}", "-i", str(video), "-frames:v", "1", "-vf", f"scale={tw}:{th}", str(jpg)])
        x, y = (i % cols) * tw, (i // cols) * (th + 28)
        sheet.paste(Image.open(jpg), (x, y))
        t = c["film_t"]
        d.text((x + 6, y + th + 4), f"{c['row']}  {int(t // 60)}:{t % 60:05.2f}", font=f, fill=(235, 235, 235))
        jpg.unlink()
    sheet.save(path, quality=88)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--uat-dir")
    a = ap.parse_args()
    board = json.loads(BOARD.read_text())
    vo = FILM / board["vo_file"]
    assert sha(vo) == board["vo_sha256"], "VO sha does not match the board"
    keeps = keep_files()
    t0, end = board["vo_film_start_s"], board["part_end_film_s"]
    OUT.mkdir(parents=True, exist_ok=True)
    seg_dir = OUT / "segs"
    seg_dir.mkdir(exist_ok=True)

    plates = board["plates"]
    cuts, segs = [], []
    for k, p in enumerate(plates):
        nxt = plates[k + 1]["t_s"] if k + 1 < len(plates) else end
        f_in, f_out = round((p["t_s"] - t0) * FPS), round((nxt - t0) * FPS)
        n = f_out - f_in
        seg = seg_dir / f"seg_{k:02d}_{p['id']}.mp4"
        row = dict(row=p["id"], film_t=p["t_s"], timeline_in=f_in / FPS, timeline_out=f_out / FPS, frames=n,
                   upscale=1.0, side_label=p.get("side_label"))
        if p["route"] == "flow":
            png = seg_dir / "placeholder_06_leeds_brewery.png"
            placeholder_png(p, png)
            run(["ffmpeg", "-y", "-loop", "1", "-framerate", str(FPS), "-i", str(png), "-frames:v", str(n), *X264, str(seg)])
            row.update(source="placeholder_06_leeds_brewery_card.png", framing=dict(offset=None),
                       disposition="PLACEHOLDER (Flow plate after Mon 12 Oct refill, J0140)")
        else:
            if p["route"] == "reuse":
                src_id = p["reuse_of"].split(":", 1)[1]
                start = float(p["clip_in_s"])
                disp = f"REUSE window {start:.2f}-{start + n / FPS:.2f} s of {src_id}"
            else:
                src_id, start, disp = p["id"], 0.0, "KEEP t1 (Chief, desk #180 6102934743)"
            src = keeps[src_id]
            assert start + n / FPS <= probe_dur(src) + 1e-3, f"{p['id']}: window runs past the clip"
            run(["ffmpeg", "-y", "-ss", f"{start:.3f}", "-i", str(src), "-an", "-vf", f"scale={W}:{H},fps={FPS}",
                 "-frames:v", str(n), *X264, str(seg)])
            row.update(source=src.name, source_path=str(src), source_sha256=sha(src), framing=dict(offset=start),
                       disposition=disp)
        segs.append(seg)
        cuts.append(row)

    concat = OUT / "concat.txt"
    concat.write_text("".join(f"file '{s}'\n" for s in segs))
    pic = OUT / "picture_only.mp4"
    run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(concat), "-c", "copy", str(pic)])
    total = round((end - t0) * FPS) / FPS
    cut = OUT / f"{NAME}.mp4"
    run(["ffmpeg", "-y", "-i", str(pic), "-i", str(vo), "-map", "0:v", "-map", "1:a", "-c:v", "copy",
         "-af", "apad", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-t", f"{total:.3f}", "-movflags", "+faststart", str(cut)])

    fd = subprocess.run(["ffmpeg", "-i", str(cut), "-vf", "freezedetect=n=-60dB:d=0.8", "-map", "0:v", "-f", "null", "-"],
                        stderr=subprocess.PIPE, text=True).stderr
    freeze = [l.split("] ", 1)[1] for l in fd.splitlines() if "freezedetect" in l and "lavfi.freezedetect" in l]
    (OUT / "freezedetect.log").write_text("\n".join(freeze) + "\n")

    (OUT / "cuts_part03_rough_v01.json").write_text(json.dumps(cuts, indent=1))
    pool = [dict(file=c["source"], title="Vertex Veo 3.1 clip, Chief KEEP" if "placeholder" not in c["source"]
                 else "placeholder plate board for the Flow slot") for c in cuts]
    (OUT / "pool_part03_rough_v01.json").write_text(json.dumps(pool, indent=1))
    sheet = OUT / f"{NAME}_contact_sheet.jpg"
    contact_sheet(cut, cuts, sheet)
    proxy = OUT / f"{NAME}_uat_proxy.mp4"
    run(["ffmpeg", "-y", "-i", str(cut), "-vf", "scale=960:540", "-c:v", "libx264", "-preset", "medium", "-crf", "26",
         "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart", str(proxy)])

    meta = dict(film=board["film"], part=3, kind="rough_v01", job="J0137", authority="Chief job J0137 (12 Oct); KEEP desk #180 6102934743",
                applied_by="cursor", no_new_mints=True, spend="none",
                assemble_method="VO-first: board t_s/use_s per plate, hard cuts, 24 fps 1080p, VO padded to part end",
                board=str(BOARD.relative_to(FILM.parents[1])), vo_file=board["vo_file"], vo_sha256=board["vo_sha256"],
                vo_duration_s=round(probe_dur(vo), 3), rough_duration_s=round(probe_dur(cut), 3), picture_s=total,
                rough_path=str(cut), sha256=sha(cut), size_mb=round(cut.stat().st_size / 1e6, 2),
                proxy_path=str(proxy), proxy_sha256=sha(proxy), contact_sheet=str(sheet),
                held_slot=dict(row="06_leeds_brewery", t=plates[5]["t"], use_s=plates[5]["use_s"], route="flow", job="J0140",
                               note="labelled plate board placeholder until the Flow mint"),
                not_in_v01=["side labels / WHO cards / chapter card (edit overlays, added at the fine cut)", "music bed", "xfades (board 0.35 s)"],
                freeze_events=freeze, segments=cuts)
    (OUT / f"ROUGH_META_part03_v01.json").write_text(json.dumps(meta, indent=1))
    DESK.mkdir(parents=True, exist_ok=True)
    for f in ("ROUGH_META_part03_v01.json", "cuts_part03_rough_v01.json", "freezedetect.log", sheet.name):
        dst = DESK / (f if f != "freezedetect.log" else "part03_rough_v01_freezedetect.log")
        shutil.copy2(OUT / f, dst)
    if a.uat_dir:
        u = Path(a.uat_dir)
        u.mkdir(parents=True, exist_ok=True)
        for f in (cut, proxy, sheet):
            shutil.copy2(f, u / f.name)
    print(json.dumps({k: meta[k] for k in ("rough_duration_s", "vo_duration_s", "sha256", "size_mb", "freeze_events")}, indent=1))


if __name__ == "__main__":
    main()
