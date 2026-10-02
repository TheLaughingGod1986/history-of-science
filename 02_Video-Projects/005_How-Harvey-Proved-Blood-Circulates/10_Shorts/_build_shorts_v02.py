#!/usr/bin/env python3
"""HOS 005 Shorts A–C v02: v01's cut, VO and captions with the frame-0 hook caption re-set to rules §3.3.

v02 changes only the hook layer (desk 5949489005): hook-word cap height 8–10% of the frame, one word per
line (two words don't fit 1080 px at that size), the block vertically centred and clear of the bottom UI.
Air dates are the approved ones (A 30 Oct, B 8 Nov, C 15 Nov). Plates, in-points, crops, VO, bed and the
word captions are v01's. Then caption-change check, gate_shorts_open, vo_check, freezedetect, frame-0 and
title-frame stills, iCloud phone copy.

    python3 _build_shorts_v02.py [--only s01 …] [--no-icloud]
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

VENV_PY = Path("/Users/benjaminoats/YouTube/History Of Science/"
               "02_Video-Projects/001_How-Did-We-Discover-Germs/10_Shorts/_venv/bin/python")
if VENV_PY.exists() and Path(sys.executable) != VENV_PY:
    os.execv(str(VENV_PY), [str(VENV_PY), str(Path(__file__).resolve()), *sys.argv[1:]])

from PIL import Image, ImageDraw, ImageFont  # noqa: E402

HERE = Path(__file__).resolve().parent
PROJ = HERE.parent
REPO = PROJ.parents[1]
CLIPS = PROJ / "04_Generated-Clips"
VO = HERE / "vo_v01"
WORK = HERE / "_work_v02"
VER = "v02"
GATE = Path(os.environ.get("HOS_GATE", REPO / "00_Brand/Channel-Setup/tools/gate_shorts_open.py"))
VO_CHECK = REPO / "00_Brand/Channel-Setup/tools/vo_check.py"
VO_PY = Path.home() / ".venvs/hos-vo/bin/python"
ICLOUD = Path.home() / ("Library/Mobile Documents/com~apple~CloudDocs/HOS UAT/"
                        "005_How-Harvey-Proved-Blood-Circulates/10_Shorts")
FONT = "/System/Library/Fonts/Supplemental/Didot.ttc"
CTA_FONT = "/System/Library/Fonts/Supplemental/Times New Roman.ttf"
W, H, FPS = 1080, 1920, 30
CREAM, INK, YEL = (245, 232, 210, 255), (28, 26, 28, 255), (255, 214, 70, 255)
TITLE = "The Tied Arm That Proved Your Blood Circulates"
TAIL_S = 0.55
LOOP_S = 4.0
TITLE_IN, TITLE_OUT = 9.0, 14.0
CHUNK_MAX_S, CHUNK_MAX_WORDS, CHUNK_MIN_S = 1.55, 5, 0.45
HOOK_CAP = 0.09          # hook cap height, fraction of H (rules §3.3: 8–10%)
HOOK_PITCH = 1.32        # line pitch, multiple of the cap height
UI_TOP = 0.75            # Shorts bottom UI (title, channel, sound) starts about here


def P(part: int, name: str) -> Path:
    return CLIPS / f"part{part:02d}/raw/v01/{name}.mp4"


# beats: (word index the plate lands on, plate, in-point s, crop x on 1920×1080). The last beat is the loop.
SHORTS = [
    {"id": "s01_the_sum", "air_date": "2026-10-30", "hook": "MORE THAN YOU **HAVE**",
     "bed": PROJ / "05_Music/hos005-part03-temp_score_bed_v01.mp3",
     "beats": [(0, P(1, "01_pulse_wrist_t1"), 1.0, 656),
               (7, P(3, "05_how_much_t1"), 0.5, 656),        # One London doctor…
               (15, P(3, "07_thousand_beats_t4"), 0.3, (540, 900)),  # Say the heart holds two ounces… an eighth
               (25, P(3, "04_squeeze_pulse_t1"), 0.5, 900),   # of that goes out. In half an hour,
               (33, P(1, "09_heart_clock_t2"), 0.3, 560),     # it beats more than a thousand times.
               (40, P(3, "09_jug_tower_t1"), 0.5, 360),       # That's more blood…
               (48, P(3, "12_glowing_loop_t2"), 0.5, 656),    # Food could never…
               ("loop", P(1, "01_pulse_wrist_t1"), 1.0, 656)]},
    {"id": "s02_the_tied_arm", "air_date": "2026-11-08", "hook": "ONE TIGHT **BAND**",
     "bed": PROJ / "05_Music/hos005-part04-temp_score_bed_v01.mp3",
     "beats": [(0, P(1, "03_band_tightens_t3"), 0.8, 640),
               (7, P(4, "02_linen_tie_t2"), 0.3, 450),        # William Harvey tied it…
               (16, P(4, "03_hand_pale_t4"), 1.5, 100),       # The hand went pale.
               (20, P(4, "04_stopped_loosen_t5"), 1.5, 560),  # No blood was getting in. He loosened it…
               (31, P(4, "06_veins_swell_t1"), 3.0, 560),     # The veins below the band swelled…
               (40, P(4, "07_in_out_doors_t2"), 1.5, 620),    # So blood goes in through the arteries…
               ("loop", P(1, "03_band_tightens_t3"), 0.8, 640)]},  # Look at your hand…
    {"id": "s03_never_saw", "air_date": "2026-11-15", "hook": "HE NEVER **SAW** THIS",
     "bed": PROJ / "05_Music/hos005-part05-temp_score_bed_v01.mp3",
     "beats": [(0, P(5, "06_eyepiece_mesh_t1"), 0.3, 656),
               (6, P(5, "01_loop_gap_t5"), 0.3, 656),         # He proved your blood goes round,
               (12, P(5, "02_tiny_gaps_t1"), 0.5, 656),       # but not how it crosses…
               (21, P(5, "03_old_harvey_t1"), 0.3, 656),      # He died in sixteen fifty-seven…
               (28, P(5, "04_malpighi_slide_t1"), 0.3, 656),  # Four years later, Marcello Malpighi…
               (40, P(5, "07_capillaries_loop_t2"), 0.3, 656),  # There it was…
               ("loop", P(5, "06_eyepiece_mesh_t1"), 0.3, 656)]},
]


def ff(*a: str, cwd: Path | None = None) -> None:
    subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", *a], check=True, cwd=cwd)


def probe(p: Path) -> float:
    return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                          "-of", "csv=p=0", str(p)], text=True))


def sha256(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def mean_db(p: Path) -> float:
    err = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(p), "-af", "volumedetect", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    return float(re.search(r"mean_volume: (-?[\d.]+)", err).group(1))


def words_from_align(path: Path) -> list[tuple[str, float, float]]:
    d = json.loads(path.read_text())
    words, cur, t0, t1 = [], "", 0.0, 0.0
    for ch, a, b in zip(d["characters"], d["character_start_times_seconds"], d["character_end_times_seconds"]):
        if ch.isspace():
            if cur:
                words.append((cur, t0, t1))
            cur = ""
        else:
            if not cur:
                t0 = a
            cur, t1 = cur + ch, b
    if cur:
        words.append((cur, t0, t1))
    return words


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
        chunks.append({"text": " ".join(parts), "t0": round(t0, 3), "t1": round(t1, 3), "n_words": len(parts)})
        i = j
    return chunks


def render(path: Path, text: str, size: int, y: int, *, anchor: str = "top", font_path: str = FONT,
           index: int = 0, fill=CREAM, stroke: int = 3) -> None:
    """Centred lines; words wrapped in ** are yellow."""
    font = ImageFont.truetype(font_path, size, index=index)
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    tokens = [(w.strip("*"), w.startswith("**")) for w in text.split()]
    lines, cur = [], []
    for tok in tokens:
        trial = " ".join(t for t, _ in cur + [tok])
        if cur and font.getlength(trial) > W - 96:
            lines.append(cur)
            cur = [tok]
        else:
            cur.append(tok)
    lines.append(cur)
    asc, desc = font.getmetrics()
    lh, gap = asc + desc, int(size * 0.12)
    block = lh * len(lines) + gap * (len(lines) - 1)
    cy = H - y - block if anchor == "bottom" else y
    space = font.getlength(" ")
    for line in lines:
        x = (W - font.getlength(" ".join(t for t, _ in line))) / 2
        for t, hot in line:
            draw.text((x, cy), t, font=font, fill=YEL if hot else fill, stroke_width=stroke, stroke_fill=INK)
            x += font.getlength(t) + space
        cy += lh + gap
    img.save(path)


def render_hook(path: Path, text: str) -> dict:
    """One word per line, sized so the cap height is HOOK_CAP of H, the block centred on the frame."""
    size = 100
    while True:
        font = ImageFont.truetype(FONT, size, index=2)
        cap = -font.getbbox("H", anchor="ls")[1]
        if cap >= HOOK_CAP * H:
            break
        size += 1
    tokens = [(w.strip("*"), w.startswith("**")) for w in text.split()]
    widest = max(font.getlength(t) for t, _ in tokens)
    if widest > W - 80:
        raise SystemExit(f"hook word {widest:.0f} px wider than the frame")
    pitch = round(cap * HOOK_PITCH)
    block = pitch * (len(tokens) - 1) + cap
    top = (H - block) // 2
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    for k, (t, hot) in enumerate(tokens):
        base = top + cap + k * pitch
        draw.text((W / 2, base), t, font=font, anchor="ms", fill=YEL if hot else CREAM, stroke_width=6,
                  stroke_fill=INK)
    img.save(path)
    bottom = top + block
    if bottom > UI_TOP * H:
        raise SystemExit(f"hook block ends at {bottom / H:.1%}, inside the bottom UI")
    return {"font_size": size, "cap_px": cap, "cap_pct": round(100 * cap / H, 2), "lines": len(tokens),
            "block_pct": [round(100 * top / H, 1), round(100 * bottom / H, 1)],
            "widest_pct": round(100 * widest / W, 1)}


def seg(src: Path, dst: Path, start: float, dur: float, x: int | tuple[int, int]) -> None:
    """x = left edge of a full-height 9:16 crop, or (x, width) for a wider window over a blurred fill."""
    if start + dur > probe(src) - 0.05:
        raise SystemExit(f"{src.name}: in {start} + {dur:.2f} s runs past the plate")
    if isinstance(x, tuple):
        x0, w = x
        vf = (f"scale=1920:1080,split[a][b];[a]crop=608:1080:{x0 + (w - 608) // 2}:0,scale={W}:{H},"
              f"boxblur=24:2,eq=brightness=-0.10[bg];[b]crop={w}:1080:{x0}:0,scale={W}:-2:flags=lanczos[fg];"
              f"[bg][fg]overlay=0:(H-h)/2,setsar=1")
    else:
        vf = f"scale=1920:1080,crop=608:1080:{x}:0,scale={W}:{H}:flags=lanczos,setsar=1"
    ff("-ss", f"{start:.3f}", "-i", str(src), "-t", f"{dur:.3f}", "-filter_complex", vf, "-an", "-c:v", "libx264",
       "-pix_fmt", "yuv420p", "-preset", "fast", "-crf", "17", "-r", str(FPS), str(dst))


def build(item: dict) -> dict:
    sid = item["id"]
    vo = VO / f"hos_005_{sid}_vo_v01_fin.wav"
    words = words_from_align(VO / f"hos_005_{sid}_vo_v01_fin_align.json")
    vo_s = probe(vo)
    total = round(vo_s + TAIL_S, 3)
    if not 22.0 <= total <= 27.0:
        raise SystemExit(f"{sid}: {total} s outside 22–27 s")
    work = WORK / sid
    if work.exists():
        shutil.rmtree(work)
    work.mkdir(parents=True)

    cuts = []
    for k, (w, src, ins, x) in enumerate(item["beats"]):
        t = 0.0 if w == 0 else (total - LOOP_S if w == "loop" else max(0.0, words[w][1] - 0.15))
        cuts.append((round(t, 3), src, ins, x, w))
    plan, segs = [], []
    for k, (t, src, ins, x, w) in enumerate(cuts):
        end = cuts[k + 1][0] if k + 1 < len(cuts) else total
        d = end - t
        if d < 1.2:
            raise SystemExit(f"{sid}: beat {k} only {d:.2f} s")
        out = work / f"seg_{k:02d}.mp4"
        seg(src, out, ins, d, x)
        segs.append(out)
        plan.append({"t0": t, "t1": round(end, 3), "plate": src.relative_to(PROJ).as_posix(), "in_s": ins,
                     "crop_x": x, "lands_on": w if w in (0, "loop") else words[w][0]})
    (work / "pic.txt").write_text("".join(f"file '{s.name}'\n" for s in segs))
    pic = work / "picture.mp4"
    ff("-f", "concat", "-safe", "0", "-i", "pic.txt", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "fast",
       "-crf", "17", "-r", str(FPS), "-t", f"{total:.3f}", str(pic), cwd=work)

    bed_gain = (mean_db(vo) - 20.0) - mean_db(item["bed"])
    audio = work / "audio.wav"
    ff("-i", str(vo), "-stream_loop", "-1", "-i", str(item["bed"]), "-filter_complex",
       f"[0:a]aformat=sample_rates=48000:channel_layouts=stereo,apad=whole_dur={total:.3f}[v];"
       f"[1:a]aformat=sample_rates=48000:channel_layouts=stereo,atrim=0:{total:.3f},asetpts=PTS-STARTPTS,"
       f"volume={bed_gain:.2f}dB,afade=t=in:d=0.05,afade=t=out:st={total - 0.2:.3f}:d=0.2[b];"
       f"[v][b]amix=inputs=2:normalize=0:duration=first[a]",
       "-map", "[a]", "-t", f"{total:.3f}", "-c:a", "pcm_s16le", str(audio))

    chunks = chunk_words(words)
    overlays = []
    hook_png = work / "cap_hook.png"
    hook_meta = render_hook(hook_png, item["hook"])
    overlays.append((hook_png, 0.0, 2.6, "hook", item["hook"].replace("**", "")))
    for i, c in enumerate(chunks):
        png = work / f"cap_{i:03d}.png"
        render(png, c["text"], 52, 330, anchor="bottom")
        overlays.append((png, c["t0"], min(c["t1"], total - 0.05), "vo", c["text"]))
    title_png = work / "cap_title.png"
    render(title_png, TITLE, 62, 250, index=2, stroke=4)
    shade = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    for yy in range(560):
        a = int(150 * (1 - yy / 560) ** 1.5)
        ImageDraw.Draw(shade).line([(0, yy), (W, yy)], fill=(0, 0, 0, a))
    Image.alpha_composite(shade, Image.open(title_png)).save(title_png)
    overlays.append((title_png, TITLE_IN, TITLE_OUT, "title", TITLE))
    cta = work / "cap_cta.png"
    render(cta, "watch the full film →", 44, 250, anchor="bottom", font_path=CTA_FONT)
    overlays.append((cta, total - LOOP_S, total - 0.08, "cta", "watch the full film →"))

    inputs = ["-i", str(pic), "-i", str(audio)]
    for png, *_ in overlays:
        inputs += ["-loop", "1", "-i", str(png)]
    fc, last = [], "[0:v]"
    for i, (_, t0, t1, *_r) in enumerate(overlays, 2):
        fc.append(f"{last}[{i}:v]overlay=0:0:enable='between(t,{t0:.3f},{t1:.3f})'[v{i}]")
        last = f"[v{i}]"
    mp4 = HERE / f"hos_005_{sid}_{VER}.mp4"
    ff(*inputs, "-filter_complex", ";".join(fc), "-map", last, "-map", "1:a", "-c:v", "libx264",
       "-pix_fmt", "yuv420p", "-profile:v", "high", "-preset", "medium", "-crf", "18", "-r", str(FPS),
       "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2", "-t", f"{total:.3f}", "-movflags", "+faststart",
       str(mp4))
    timeline = [{"role": r, "text": t, "t0": round(a, 3), "t1": round(b, 3)} for _, a, b, r, t in overlays]
    (work / "timeline.json").write_text(json.dumps({"plan": plan, "overlays": timeline}, indent=2) + "\n")
    return {"id": sid, "air_date": item["air_date"], "file": mp4.relative_to(PROJ).as_posix(), "sha256": sha256(mp4),
            "duration_s": round(probe(mp4), 3), "vo": vo.name, "vo_s": round(vo_s, 3),
            "bed": item["bed"].name, "bed_gain_db": round(bed_gain, 2), "hook": item["hook"].replace("**", ""),
            "hook_layer": hook_meta,
            "title": TITLE, "plan": plan, "captions": len(chunks), "timeline": timeline}


def caption_check(mp4: Path, timeline: list[dict]) -> dict:
    """Every 0.5 s: the caption band changes when the spoken chunk changes."""
    frames = WORK / mp4.stem.replace("hos_005_", "").replace(f"_{VER}", "") / "frames"
    frames.mkdir(parents=True, exist_ok=True)
    vo_rows = [r for r in timeline if r["role"] == "vo"]
    prev_text = prev_hash = None
    changes = matched = 0
    t, dur = 0.0, probe(mp4)
    while t < dur - 0.05:
        crop = frames / f"c{t:05.1f}.png"
        ff("-ss", f"{t:.3f}", "-i", str(mp4), "-frames:v", "1", "-vf", "crop=1000:320:40:1250", str(crop))
        text = next((r["text"] for r in vo_rows if r["t0"] <= t < r["t1"]), None)
        h = hashlib.md5(crop.read_bytes()).hexdigest()
        if prev_text is not None and text != prev_text:
            changes += 1
            matched += h != prev_hash
        prev_text, prev_hash = text, h
        t += 0.5
    ratio = matched / changes if changes else 0.0
    return {"ok": changes >= 7 and ratio >= 0.7, "changes": changes, "ratio": round(ratio, 2)}


def freeze(mp4: Path) -> list[str]:
    err = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(mp4), "-vf",
                          "freezedetect=n=0.003:d=0.8", "-map", "0:v", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    return re.findall(r"freeze_start: ([\d.]+)", err)


def run(cmd: list[str]) -> tuple[int, str]:
    r = subprocess.run(cmd, capture_output=True, text=True)
    out = "\n".join(l for l in (r.stdout + r.stderr).splitlines() if "Warning" not in l and l.strip())
    return r.returncode, out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", nargs="*")
    ap.add_argument("--no-icloud", action="store_true")
    ns = ap.parse_args()
    index_p = HERE / f"SHORTS_INDEX_{VER}.json"
    index = json.loads(index_p.read_text()) if index_p.exists() else {
        "scripts": "SHORTS_SCRIPTS_v01.md", "task": "PR #180 comment 5949489005",
        "change": "frame-0 hook caption only (rules §3.3); otherwise v01", "shorts": {}}
    for item in SHORTS:
        if ns.only and item["id"] not in ns.only:
            continue
        rec = build(item)
        mp4 = PROJ / rec["file"]
        rec["caption_check"] = caption_check(mp4, rec.pop("timeline"))
        code, out = run([sys.executable, str(GATE), "check", str(mp4), "--air-date", item["air_date"]])
        rec["gate"] = {"exit": code, "output": out}
        code, out = run([str(VO_PY), str(VO_CHECK), str(mp4), "--script", str(VO / f"{item['id']}.txt")])
        rec["vo_check"] = {"exit": code, "output": out}
        rec["freezedetect_starts"] = freeze(mp4)
        still = WORK / item["id"] / f"{mp4.stem}_title_frame.jpg"
        ff("-ss", "11.5", "-i", str(mp4), "-frames:v", "1", "-q:v", "3", str(still))
        rec["title_still"] = still.relative_to(PROJ).as_posix()
        f0 = WORK / item["id"] / f"{mp4.stem}_frame0.jpg"
        ff("-i", str(mp4), "-frames:v", "1", "-q:v", "2", str(f0))
        rec["frame0_still"] = f0.relative_to(PROJ).as_posix()
        if not ns.no_icloud:
            ICLOUD.mkdir(parents=True, exist_ok=True)
            shutil.copy2(mp4, ICLOUD / mp4.name)
            rec["icloud"] = str(ICLOUD / mp4.name)
        index["shorts"][item["id"]] = rec
        print(f"BUILT {item['id']} {rec['duration_s']} s sha {rec['sha256'][:12]} captions {rec['caption_check']}")
        print(rec["gate"]["output"])
        print(rec["vo_check"]["output"])
        print(f"freezedetect: {len(rec['freezedetect_starts'])} events {rec['freezedetect_starts']}")
    index_p.write_text(json.dumps(index, indent=2) + "\n")


if __name__ == "__main__":
    main()
