#!/usr/bin/env python3
"""HOS 005 full join v01: Parts 01–05 + chapter cards + cream end card + 20 s Studio end-screen hold.

UAT for Ben's moving-picture sign-off. Not a KEEP, not for upload.

- Part 01: picture from Ben's passed rough v01 (sha checked; its fade-to-black sits under the card),
  audio rebuilt from the locked VO + its TEMP bed at the rough's gain, running on under the card.
- Parts 02–05: `_assemble_part_rough_v02.py --part N --join` (same plates, labels and bed as the
  roughs; no fade; the bed carries under the card).
- Timeline (VO_RETIME_v01.json): each part's VO starts 2.5 s after the previous VO ends
  (0.6 s breath + 1.9 s card). Cards cross-fade in after the breath, never over a word.
- Out: the last line, Part 05's tail, the cream card (4 s, bed fading), then 20 s quiet hold.

  ~/.venvs/hos-vertex/bin/python 07_Edit-Project/_join_full_v01.py
"""
from __future__ import annotations

import hashlib
import json
import re
import shutil
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

PROJ = Path(__file__).resolve().parents[1]
REPO = PROJ.parents[1]
EDIT = PROJ / "07_Edit-Project"
WORK = EDIT / "_join_full_work"
OUT = PROJ / "09_Final-Export/hos_005_full_join_v01.mp4"
META = EDIT / "full_join_v01_meta.json"
ICLOUD_DIR = (Path.home() / "Library/Mobile Documents/com~apple~CloudDocs/HOS UAT"
              / "005_How-Harvey-Proved-Blood-Circulates/09_Final-Export")
# Copy of 004's cream end card (004 `04_Generated-Clips/part05/refs/hos_end_card_v01.png`).
END_CARD = PROJ / "04_Generated-Clips/part05/refs/hos_end_card_v01.png"

PART01_CUT = PROJ / "09_Final-Export/hos_005_part01_rough_v01.mp4"
PART01_SHA = "7661b6cf1897c6dabe60e09592b297f9ed21b253cb7c2946cc12f58732a9d098"
PART01_BED_GAIN_DB = -17.5

FPS, W, H = 30, 1920, 1080
CARD_BREATH_S = 0.6
CARD_TO_VO_S = 1.9
CARD_FADE_IN_S = 0.35
CARD_FADE_OUT_S = 0.25
CARD_OUT_LEAD_S = 0.1
END_CARD_S = 4.0
END_FADE_IN_S = 0.5
HOLD_S = 20.0

CARDS = {
    "02": ("PART 02", "c. AD 170", "The Liver That Made Blood"),
    "03": ("PART 03", "1616", "The Sum That Broke the Old Idea"),
    "04": ("PART 04", "1628", "The Tied Arm"),
    "05": ("PART 05", "1661", "The Vessels He Never Saw"),
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


def run(cmd: list[str]) -> None:
    subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", *cmd], check=True)


def font(size: int, bold: bool = False, italic: bool = False) -> ImageFont.FreeTypeFont:
    name = "Georgia" + (" Bold" if bold else "") + (" Italic" if italic else "")
    return ImageFont.truetype(f"/System/Library/Fonts/Supplemental/{name}.ttf", size)


def render_card(part: str, dest: Path) -> None:
    """004's parchment chapter card (`_join_hos_004_full_v03.py`), 005 titles."""
    label, date, title = CARDS[part]
    stripe_a, stripe_b = (28, 20, 16), (36, 24, 18)
    plaque, ink, rule, muted = (234, 220, 196), (48, 32, 20), (92, 64, 40), (96, 68, 44)
    im = Image.new("RGB", (W, H), stripe_a)
    d = ImageDraw.Draw(im)
    for y in range(0, H, 28):
        if (y // 28) % 2 == 0:
            d.rectangle((0, y, W, y + 14), fill=stripe_b)
    x0, y0, x1, y1 = 220, 240, 1700, 840
    d.rounded_rectangle((x0 - 8, y0 - 8, x1 + 8, y1 + 8), radius=6, outline=rule, width=3)
    d.rounded_rectangle((x0, y0, x1, y1), radius=4, fill=plaque)
    d.rounded_rectangle((x0 + 18, y0 + 18, x1 - 18, y1 - 18), radius=2, outline=ink, width=3)

    def center(text: str, y: int, fnt, fill) -> None:
        bb = d.textbbox((0, 0), text, font=fnt)
        d.text(((W - (bb[2] - bb[0])) / 2, y), text, font=fnt, fill=fill)

    center(label, 320, font(34), muted)
    cx, cy = W / 2, 390
    d.line((cx - 200, cy, cx - 16, cy), fill=rule, width=2)
    d.ellipse((cx - 5, cy - 5, cx + 5, cy + 5), fill=ink)
    d.line((cx + 16, cy, cx + 200, cy), fill=rule, width=2)
    center(date, 420, font(110, bold=True), ink)
    center(title, 580, font(40, italic=True), muted)
    im.save(dest)


def part01_segment(vo: Path, bed: Path, vo_dur: float, dest: Path) -> None:
    total = vo_dur + CARD_BREATH_S + CARD_TO_VO_S
    cut_dur = probe(PART01_CUT)
    pad = max(0.0, total - cut_dur) + 0.1
    fade_st = total - 0.4
    run(["-i", str(PART01_CUT), "-i", str(vo), "-i", str(bed),
         "-filter_complex",
         f"[0:v]tpad=stop_mode=clone:stop_duration={pad:.3f},trim=0:{total:.3f},setpts=PTS-STARTPTS,"
         f"format=yuv420p,setsar=1[v];"
         f"[1:a]aresample=48000,pan=stereo|c0=c0|c1=c0,apad,atrim=0:{total:.3f}[vo];"
         f"[2:a]atrim=0:{total:.3f},asetpts=PTS-STARTPTS,volume={PART01_BED_GAIN_DB:.2f}dB,"
         f"afade=t=in:st=0:d=0.4,afade=t=out:st={fade_st:.3f}:d=0.4,"
         "aformat=sample_rates=48000:channel_layouts=stereo[bed];"
         "[vo][bed]amix=inputs=2:normalize=0:duration=first,alimiter=limit=0.89:level=false[a]",
         "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-preset", "medium", "-crf", "17",
         "-r", str(FPS), "-fps_mode", "cfr", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2",
         "-t", f"{total:.3f}", str(dest)])


def main() -> None:
    WORK.mkdir(parents=True, exist_ok=True)
    if sha256(PART01_CUT) != PART01_SHA:
        raise SystemExit("STOP: Part 01 cut is not Ben's passed rough v01")
    if not END_CARD.exists():
        raise SystemExit(f"STOP: missing end card {END_CARD}")

    segs: list[Path] = []
    vo_durs: dict[str, float] = {}
    for n in range(1, 6):
        part = f"{n:02d}"
        board = json.loads((EDIT / f"parts/part-{part}_plates_v02.json").read_text())
        vo = PROJ / board["vo_file"]
        if sha256(vo) != board["vo_sha256"]:
            raise SystemExit(f"STOP: Part {part} VO is not the locked v01 take")
        vo_durs[part] = probe(vo)
        if part == "01":
            seg = WORK / "part01" / "part01_join.mp4"
            seg.parent.mkdir(parents=True, exist_ok=True)
            part01_segment(vo, PROJ / "05_Music/hos005-part01-temp_score_bed_v01.mp3", vo_durs[part], seg)
        else:
            subprocess.run([str(Path.home() / ".venvs/hos-vertex/bin/python"),
                            str(EDIT / "_assemble_part_rough_v02.py"), "--part", part, "--join"], check=True)
            seg = WORK / f"part{part}" / f"part{part}_join.mp4"
        segs.append(seg)

    durs = [probe(s) for s in segs]
    starts = [0.0]
    for d in durs[:-1]:
        starts.append(starts[-1] + d)

    cards = []
    for i, part in enumerate(["02", "03", "04", "05"], start=1):
        png = WORK / f"card_{part}.png"
        render_card(part, png)
        t_in = starts[i - 1] + vo_durs[f"{i:02d}"] + CARD_BREATH_S
        cards.append((t_in, starts[i] - CARD_OUT_LEAD_S + CARD_FADE_OUT_S, png, part))
    end_in = starts[4] + durs[4] - END_CARD_S
    film = starts[4] + durs[4]

    inputs: list[str] = []
    for s in segs:
        inputs += ["-i", str(s)]
    fc = [f"{''.join(f'[{k}:v][{k}:a]' for k in range(5))}concat=n=5:v=1:a=1[cv][ca]"]
    cur = "[cv]"
    for k, (t0, t1, png, _part) in enumerate(cards):
        idx = 5 + k
        inputs += ["-loop", "1", "-framerate", str(FPS), "-t", f"{t1 - t0:.3f}", "-i", str(png)]
        hold = t1 - t0
        fc.append(f"[{idx}:v]format=rgba,fade=t=in:st=0:d={CARD_FADE_IN_S}:alpha=1,"
                  f"fade=t=out:st={hold - CARD_FADE_OUT_S:.3f}:d={CARD_FADE_OUT_S}:alpha=1,"
                  f"setpts=PTS+{t0:.3f}/TB[c{k}]")
        fc.append(f"{cur}[c{k}]overlay=0:0:eof_action=pass[o{k}]")
        cur = f"[o{k}]"
    eidx = 5 + len(cards)
    inputs += ["-loop", "1", "-framerate", str(FPS), "-t", f"{END_CARD_S + HOLD_S:.3f}", "-i", str(END_CARD)]
    fc.append(f"{cur}tpad=stop_mode=clone:stop_duration={HOLD_S:.3f}[vp]")
    fc.append(f"[{eidx}:v]scale={W}:{H},format=rgba,fade=t=in:st=0:d={END_FADE_IN_S}:alpha=1,"
              f"setpts=PTS+{end_in:.3f}/TB[ec]")
    fc.append("[vp][ec]overlay=0:0:eof_action=pass,format=yuv420p,setsar=1[v]")
    fc.append(f"[ca]apad=pad_dur={HOLD_S:.3f}[a]")
    total = film + HOLD_S
    run([*inputs, "-filter_complex", ";".join(fc), "-map", "[v]", "-map", "[a]",
         "-c:v", "libx264", "-preset", "medium", "-crf", "17", "-pix_fmt", "yuv420p",
         "-r", str(FPS), "-fps_mode", "cfr", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2",
         "-t", f"{total:.3f}", "-movflags", "+faststart", str(OUT)])

    ICLOUD_DIR.mkdir(parents=True, exist_ok=True)
    shutil.copy2(OUT, ICLOUD_DIR / OUT.name)
    streams = json.loads(subprocess.check_output(
        ["ffprobe", "-v", "error", "-show_entries", "stream=codec_type,width,height,r_frame_rate,"
         "duration,channels,sample_rate", "-of", "json", str(OUT)], text=True))["streams"]
    err = subprocess.run(["ffmpeg", "-hide_banner", "-i", str(OUT), "-vf", "freezedetect=n=0.003:d=0.8",
                          "-an", "-f", "null", "-"], capture_output=True, text=True, errors="replace").stderr
    freezes = [(float(a), float(b)) for a, b in zip(re.findall(r"freeze_start: ([\d.]+)", err),
                                                    re.findall(r"freeze_end: ([\d.]+)", err) + [str(total)])]
    holds = [(t0, t1) for t0, t1, _p, _n in cards] + [(end_in, total)]
    unexplained = [f for f in freezes if not any(f[0] >= h0 - 0.5 and f[1] <= h1 + 0.5 for h0, h1 in holds)]
    meta = {
        "out": str(OUT.relative_to(REPO)), "sha256": sha256(OUT), "duration_s": probe(OUT),
        "status": "UAT for Ben's moving-picture sign-off; not a KEEP; no upload",
        "streams": streams,
        "parts": [{"part": f"{n + 1:02d}", "film_start_s": round(starts[n], 3), "segment_s": round(durs[n], 3),
                   "vo_s": round(vo_durs[f"{n + 1:02d}"], 3), "segment_sha256": sha256(segs[n])}
                  for n in range(5)],
        "part01_picture": {"file": str(PART01_CUT.relative_to(REPO)), "sha256": PART01_SHA},
        "cards": [{"part": p, "in_s": round(t0, 3), "out_s": round(t1, 3), "text": " · ".join(CARDS[p])}
                  for t0, t1, _png, p in cards],
        "end_card": {"file": str(END_CARD.relative_to(REPO)), "sha256": sha256(END_CARD),
                     "in_s": round(end_in, 3), "hold_s": HOLD_S},
        "freezes": freezes, "freezes_outside_cards": unexplained,
    }
    META.write_text(json.dumps(meta, indent=2, ensure_ascii=False) + "\n")
    print(f"SAVED {OUT}\nICLOUD {ICLOUD_DIR / OUT.name}\nsha256 {meta['sha256']}\n"
          f"duration {meta['duration_s']:.3f}s freezes {len(freezes)} outside_cards {len(unexplained)}")
    for c in meta["cards"]:
        print(f"card {c['part']} {c['in_s']:.2f}–{c['out_s']:.2f} {c['text']}")
    print(f"end card {end_in:.2f} · hold to {total:.2f}")


if __name__ == "__main__":
    main()
