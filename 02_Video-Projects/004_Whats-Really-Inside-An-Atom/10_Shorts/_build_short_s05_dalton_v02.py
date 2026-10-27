#!/usr/bin/env python3
"""HOS 004 Short s05 v02 (J0306 FIX on J0298 v01). Same lift, two Chief fixes, no new spend.

1. The hydrogen/oxygen beat no longer uses 03_weights_line (Veo tiles Hp/Hg/Op). It uses
   05_fixed_amounts, checked at 2 fps with no letters in any frame.
2. The open is the claim, not the dateline. Lift starts at "every element…" (cut after
   "His atomic theory says"), runs through the payoff, and drops "however you make it."
   so the Short stays inside 22–27 s and 55–65 words.

Dalton is on screen from frame 0. The person card sits just after the 2 s hook. Gold uses
07_water_always (a gold sphere; the wood-grain 04 plate is kept for the later pieces beat).
Hook, captions, the 9–14 s title, the loop back to Dalton, and the Part 02 bed stay.
Never uploads.

    python3 _build_short_s05_dalton_v02.py [--air-date YYYY-MM-DD] [--no-icloud]
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

VENV_PY = Path("/Users/benjaminoats/YouTube/History Of Science/"
               "02_Video-Projects/001_How-Did-We-Discover-Germs/10_Shorts/_venv/bin/python")
if VENV_PY.exists() and Path(sys.executable) != VENV_PY:
    os.execv(str(VENV_PY), [str(VENV_PY), str(Path(__file__).resolve()), *sys.argv[1:]])

import argparse  # noqa: E402
import hashlib  # noqa: E402
import json  # noqa: E402
import math  # noqa: E402
import re  # noqa: E402
import shutil  # noqa: E402
import subprocess  # noqa: E402

from PIL import Image, ImageDraw, ImageFont  # noqa: E402

HERE = Path(__file__).resolve().parent
PROJ = HERE.parent
REPO = PROJ.parents[1]
CLIPS = PROJ / "04_Generated-Clips"
SID = "s05_dalton"
VER = "v02"
WORK = HERE / f"_work_{SID}_{VER}"
RAW_VO = PROJ / "02_Voiceover/05_Master/hos_004_part02_vo_v01.mp3"
RAW_ALIGN = PROJ / "02_Voiceover/05_Master/hos_004_part02_vo_v01_align.json"
# Alignment indices: claim "every" (17) through "oxygen," (66), skip "however you make it." (67–70),
# then "That … weights." (71–84). 64 words.
TAKE = list(range(17, 67)) + list(range(71, 85))
MAX_PAUSE = 0.45
ATEMPO = 1.03
BED = PROJ / "05_Music/hos004-part02-temp_score_bed_v01.mp3"
HOOK = "EACH **ATOM**"
CARD = ("JOHN DALTON", "Manchester, 1808")
CARD_IN, CARD_OUT, CARD_FADE = 2.2, 6.7, 0.35
W, H, FPS = 1080, 1920, 30
BAND_TOP, BAND_H = (H - 608) // 2, 608
CREAM, INK, YEL = (245, 232, 210, 255), (28, 26, 28, 255), (255, 214, 70, 255)
FONT = "/System/Library/Fonts/Supplemental/Didot.ttc"
CTA_FONT = "/System/Library/Fonts/Supplemental/Times New Roman.ttf"
TITLE = "What's Really Inside an Atom?"
TITLE_DRAFT = "What Is Dalton's Atomic Theory?"
TAIL_S = 0.55
LOOP_S = 3.2
TITLE_IN, TITLE_OUT = 9.0, 14.0
CHUNK_MAX_S, CHUNK_MAX_WORDS, CHUNK_MIN_S = 1.55, 5, 0.45
HOOK_CAP = 0.09
HOOK_PITCH = 1.32
UI_TOP = 0.75
GATE = Path(os.environ.get("HOS_GATE", REPO / "00_Brand/Channel-Setup/tools/gate_shorts_open.py"))
VO_CHECK = REPO / "00_Brand/Channel-Setup/tools/vo_check.py"
VO_PY = Path.home() / ".venvs/hos-vo/bin/python"
ICLOUD = Path.home() / ("Library/Mobile Documents/com~apple~CloudDocs/HOS UAT/"
                        "004_Whats-Really-Inside-An-Atom/10_Shorts")
SCRIPT_TXT = WORK / f"{SID}.txt"


def P2(name: str) -> Path:
    return CLIPS / f"part02/raw/v01/{name}.mp4"


# (index of the word the plate lands on, plate, in-point s, crop x on 1920x1080); "loop" = last LOOP_S s.
# In-points stay inside the letter-free stretch of each plate (checked at 2 fps, 15 Oct 2026).
BEATS = [
    (0, P2("01_dalton_schoolroom_v01"), 0.40, 656),   # Every element… Dalton at the balance, frame 0.
    (17, P2("05_fixed_amounts_v01"), 0.40, 656),      # Hydrogen / Oxygen. Replaces 03_weights_line. No letters.
    (24, P2("07_water_always_v01"), 2.00, 656),       # Gold is heavier still. Gold sphere, not the wood ball.
    (28, P2("02_atomic_theory_v01"), 0.80, 656),      # Why believe him? 0.80–3.49 s clears desk-edge seam and keeps papers out.
    (34, P2("04_gold_heavier_v01"), 0.15, 656),       # same fixed amounts. No letters.
    (47, P2("20_what_is_order_v01"), 0.40, 500),      # Water … tiny pieces. Unused Part 02 plate (0.40–3.82 s, crop 500), no letters/gutter.
    ("loop", P2("01_dalton_schoolroom_v01"), 0.40, 656),
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
            # A capital after a comma is a new sentence (the "however you make it" splice).
            if parts[-1][-1:] in ",;:" and sj - t0 >= CHUNK_MIN_S and (len(parts) >= 2 or wj[:1].isupper()):
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


def seg(src: Path, dst: Path, start: float, dur: float, x: int) -> None:
    if start + dur > probe(src) - 0.05:
        raise SystemExit(f"{src.name}: in {start} + {dur:.2f} s runs past the plate")
    vf = f"scale=1920:1080,crop=608:1080:{x}:0,scale={W}:{H}:flags=lanczos,setsar=1"
    ff("-ss", f"{start:.3f}", "-i", str(src), "-t", f"{dur:.3f}", "-filter_complex", vf, "-an", "-c:v", "libx264",
       "-pix_fmt", "yuv420p", "-preset", "fast", "-crf", "17", "-r", str(FPS), str(dst))


def lifted_vo(work: Path) -> tuple[Path, list[tuple[str, float, float]]]:
    """Cut the claim-first stretch, drop one clause, cap pauses, apply ATEMPO (v04 master route)."""
    all_words = words_from_align(RAW_ALIGN)
    words = [all_words[i] for i in TAKE]
    words[0] = (words[0][0][:1].upper() + words[0][0][1:], words[0][1], words[0][2])
    spans: list[list[float]] = []
    raw_gap = round(MAX_PAUSE * ATEMPO, 3)
    for i, (_, s, e) in enumerate(words):
        # The claim is cut on the word boundary after "says". A lead-in pad pulls in that
        # tail and the checker hears "as every". Start the first word on its own onset.
        s0 = s if i == 0 else s - 0.06
        e0 = e + 0.06
        if spans and s0 - spans[-1][1] <= raw_gap:
            spans[-1][1] = max(spans[-1][1], e0)
        elif spans:
            spans.append([max(s0, spans[-1][1] + 0.0), e0])
        else:
            spans.append([s0, e0])
    out_t, remap = 0.0, []
    for k, (s, e) in enumerate(spans):
        if k:
            out_t += raw_gap
        remap.append((s, e, out_t))
        out_t += e - s
    mapped = []
    for w, s, e in words:
        for rs, re_, ot in remap:
            if rs <= s <= re_:
                mapped.append((w, round((ot + s - rs) / ATEMPO, 3), round((ot + e - rs) / ATEMPO, 3)))
                break
    fc = []
    for k, (s, e) in enumerate(spans):
        fc.append(f"[0:a]atrim={s:.3f}:{e:.3f},asetpts=PTS-STARTPTS,"
                  f"afade=t=in:d=0.02,afade=t=out:st={e - s - 0.03:.3f}:d=0.03,"
                  f"aformat=sample_rates=48000:channel_layouts=stereo[s{k}]")
        if k + 1 < len(spans):
            fc.append(f"anullsrc=r=48000:cl=stereo,atrim=0:{raw_gap:.3f}[g{k}]")
    order = "".join(f"[s{k}]" + (f"[g{k}]" if k + 1 < len(spans) else "") for k in range(len(spans)))
    n = len(spans) * 2 - 1
    fc.append(f"{order}concat=n={n}:v=0:a=1,atempo={ATEMPO}[a]")
    wav = work / f"hos_004_{SID}_vo_{VER}.wav"
    ff("-i", str(RAW_VO), "-filter_complex", ";".join(fc), "-map", "[a]", "-c:a", "pcm_s16le", str(wav))
    return wav, mapped


def render_card(path: Path) -> dict:
    """Lower third of the 16:9 centre band: name on line one, place and date on line two."""
    size1 = int(BAND_H * 0.12)
    size2 = int(BAND_H * 0.075)
    f1 = ImageFont.truetype(FONT, size1, index=2)
    f2 = ImageFont.truetype(CTA_FONT, size2)
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    x = 70
    y2 = BAND_TOP + BAND_H - 40
    y1 = y2 - size2 - 18
    shade = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shade)
    top = y1 - size1 - 30
    bot = BAND_TOP + BAND_H + 80
    feather_in, feather_out = 120, 120
    for yy in range(top, bot):
        ramp_in = min(1.0, (yy - top) / feather_in)
        ramp_out = min(1.0, (bot - yy) / feather_out)
        w = 0.5 * (1.0 - math.cos(math.pi * min(ramp_in, ramp_out)))
        a = int(140 * w)
        sd.line([(0, yy), (W, yy)], fill=(0, 0, 0, a))
    img = Image.alpha_composite(img, shade)
    d = ImageDraw.Draw(img)
    d.text((x, y1), CARD[0], font=f1, anchor="ls", fill=YEL, stroke_width=4, stroke_fill=INK)
    d.text((x, y2), CARD[1], font=f2, anchor="ls", fill=CREAM, stroke_width=3, stroke_fill=INK)
    img.save(path)
    return {"name": CARD[0], "line2": CARD[1], "line1_px": size1, "line1_pct_of_band": 12.0,
            "band": [BAND_TOP, BAND_TOP + BAND_H], "in_s": CARD_IN, "out_s": CARD_OUT, "fade_s": CARD_FADE}


def build(air_date: str) -> dict:
    if WORK.exists():
        shutil.rmtree(WORK)
    WORK.mkdir(parents=True)
    vo, words = lifted_vo(WORK)
    SCRIPT_TXT.write_text(" ".join(w for w, _, _ in words) + "\n")
    vo_s = probe(vo)
    total = round(vo_s + TAIL_S, 3)
    if not 22.0 <= total <= 27.0:
        raise SystemExit(f"{SID}: {total} s outside 22–27 s")
    if not 55 <= len(words) <= 65:
        raise SystemExit(f"{SID}: {len(words)} words outside 55–65")

    cuts = []
    for w, src, ins, x in BEATS:
        if w == 0:
            t = 0.0
        elif w == "loop":
            t = total - LOOP_S
        else:
            t = max(0.0, words[w][1] - 0.15)
        cuts.append((round(t, 3), src, ins, x, w))
    plan, segs = [], []
    for k, (t, src, ins, x, w) in enumerate(cuts):
        end = cuts[k + 1][0] if k + 1 < len(cuts) else total
        d = end - t
        if d < 1.2:
            raise SystemExit(f"{SID}: beat {k} only {d:.2f} s")
        out = WORK / f"seg_{k:02d}.mp4"
        seg(src, out, ins, d, x)
        segs.append(out)
        plan.append({"t0": t, "t1": round(end, 3), "plate": src.relative_to(PROJ).as_posix(), "in_s": ins,
                     "crop_x": x, "lands_on": w if w in (0, "loop") else words[w][0]})
    (WORK / "pic.txt").write_text("".join(f"file '{s.name}'\n" for s in segs))
    pic = WORK / "picture.mp4"
    ff("-f", "concat", "-safe", "0", "-i", "pic.txt", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "fast",
       "-crf", "17", "-r", str(FPS), "-t", f"{total:.3f}", str(pic), cwd=WORK)

    bed_gain = (mean_db(vo) - 20.0) - mean_db(BED)
    audio = WORK / "audio.wav"
    ff("-i", str(vo), "-stream_loop", "-1", "-i", str(BED), "-filter_complex",
       f"[0:a]aformat=sample_rates=48000:channel_layouts=stereo,apad=whole_dur={total:.3f}[v];"
       f"[1:a]aformat=sample_rates=48000:channel_layouts=stereo,atrim=0:{total:.3f},asetpts=PTS-STARTPTS,"
       f"volume={bed_gain:.2f}dB,afade=t=in:d=0.05,afade=t=out:st={total - 0.2:.3f}:d=0.2[b];"
       f"[v][b]amix=inputs=2:normalize=0:duration=first[a]",
       "-map", "[a]", "-t", f"{total:.3f}", "-c:a", "pcm_s16le", str(audio))

    chunks = chunk_words(words)
    overlays = []
    hook_png = WORK / "cap_hook.png"
    hook_meta = render_hook(hook_png, HOOK)
    overlays.append((hook_png, 0.0, 2.0, "hook", HOOK.replace("**", "")))
    for i, c in enumerate(chunks):
        png = WORK / f"cap_{i:03d}.png"
        render(png, c["text"], 52, 330, anchor="bottom")
        overlays.append((png, c["t0"], min(c["t1"], total - 0.05), "vo", c["text"]))
    title_png = WORK / "cap_title.png"
    render(title_png, TITLE, 62, 250, index=2, stroke=4)
    shade = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    for yy in range(620):
        w = 0.5 * (1.0 + math.cos(math.pi * yy / 620))
        a = int(150 * w)
        ImageDraw.Draw(shade).line([(0, yy), (W, yy)], fill=(0, 0, 0, a))
    Image.alpha_composite(shade, Image.open(title_png)).save(title_png)
    overlays.append((title_png, TITLE_IN, TITLE_OUT, "title", TITLE))
    cta = WORK / "cap_cta.png"
    render(cta, "watch the full film →", 44, 250, anchor="bottom", font_path=CTA_FONT)
    overlays.append((cta, total - LOOP_S, total - 0.08, "cta", "watch the full film →"))
    card_png = WORK / "card_who.png"
    card_meta = render_card(card_png)

    inputs = ["-i", str(pic), "-i", str(audio)]
    for png, *_ in overlays:
        inputs += ["-loop", "1", "-i", str(png)]
    ci = 2 + len(overlays)
    inputs += ["-loop", "1", "-t", f"{total:.3f}", "-i", str(card_png)]
    fc, last = [], "[0:v]"
    fc.append(f"[{ci}:v]format=rgba,fade=t=in:st={CARD_IN}:d={CARD_FADE}:alpha=1,"
              f"fade=t=out:st={CARD_OUT - CARD_FADE}:d={CARD_FADE}:alpha=1[card]")
    fc.append(f"{last}[card]overlay=0:0:enable='between(t,{CARD_IN:.3f},{CARD_OUT:.3f})'[vc]")
    last = "[vc]"
    for i, (_, t0, t1, *_r) in enumerate(overlays, 2):
        fc.append(f"{last}[{i}:v]overlay=0:0:enable='between(t,{t0:.3f},{t1:.3f})'[v{i}]")
        last = f"[v{i}]"
    mp4 = HERE / f"hos_004_{SID}_{VER}.mp4"
    ff(*inputs, "-filter_complex", ";".join(fc), "-map", last, "-map", "1:a", "-c:v", "libx264",
       "-pix_fmt", "yuv420p", "-profile:v", "high", "-preset", "medium", "-crf", "18", "-r", str(FPS),
       "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2", "-t", f"{total:.3f}", "-movflags", "+faststart",
       str(mp4))
    timeline = [{"role": r, "text": t, "t0": round(a, 3), "t1": round(c, 3)} for _, a, c, r, t in overlays]
    timeline.append({"role": "who", "text": " · ".join(CARD), "t0": CARD_IN, "t1": CARD_OUT})
    (WORK / "timeline.json").write_text(json.dumps({"plan": plan, "overlays": timeline}, indent=2) + "\n")
    return {"id": SID, "job": "J0416", "fixes": "J0306 v02 (feathered shades + unused P2 plate on s06)", "test": "B (search-titled)", "air_date_draft": air_date,
            "file": mp4.relative_to(PROJ).as_posix(), "sha256": sha256(mp4), "duration_s": round(probe(mp4), 3),
            "vo_source": RAW_VO.relative_to(PROJ).as_posix(), "vo_take_indices": TAKE,
            "dropped": "however you make it.",
            "route": "claim first: Every element is made of its own kind of atom … fixed weights. Dateline and 'His atomic theory says' cut at the word boundary.",
            "vo_s": round(vo_s, 3), "words": len(words), "max_pause_s": MAX_PAUSE, "atempo": ATEMPO,
            "bed": BED.name, "bed_gain_db": round(bed_gain, 2), "hook": HOOK.replace("**", ""),
            "hook_layer": hook_meta, "who_card": card_meta, "title_on_screen": TITLE,
            "youtube_title_draft": TITLE_DRAFT, "plan": plan, "captions": len(chunks), "timeline": timeline}


def caption_check(mp4: Path, timeline: list[dict]) -> dict:
    frames = WORK / "frames"
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
    out = "\n".join(line for line in (r.stdout + r.stderr).splitlines() if "Warning" not in line and line.strip())
    return r.returncode, out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--air-date", default="2026-11-10")
    ap.add_argument("--no-icloud", action="store_true")
    ns = ap.parse_args()
    rec = build(ns.air_date)
    mp4 = PROJ / rec["file"]
    rec["caption_check"] = caption_check(mp4, rec.pop("timeline"))
    code, out = run([sys.executable, str(GATE), "check", str(mp4), "--air-date", ns.air_date])
    rec["gate"] = {"exit": code, "output": out}
    code, out = run([str(VO_PY), str(VO_CHECK), str(mp4), "--script", str(SCRIPT_TXT)])
    rec["vo_check"] = {"exit": code, "output": out}
    rec["freezedetect_starts"] = freeze(mp4)
    stills = []
    for t in (0.0, 11.5, 15.8, rec["duration_s"] - 1.0):
        st = WORK / f"{mp4.stem}_t{t:05.1f}.jpg"
        ff("-ss", f"{t:.3f}", "-i", str(mp4), "-frames:v", "1", "-q:v", "3", str(st))
        stills.append(st.relative_to(PROJ).as_posix())
    rec["stills"] = stills
    if not ns.no_icloud:
        ICLOUD.mkdir(parents=True, exist_ok=True)
        dst = ICLOUD / mp4.name
        dst.unlink(missing_ok=True)
        shutil.copy2(mp4, dst)
        rec["icloud"] = str(dst)
    rec["autocomplete_check"] = {
        "date": "2026-10-15",
        "source": "suggestqueries client=youtube ds=yt gl=GB signed-out",
        "hits": [
            "what is dalton's atomic theory",
            "what is dalton's atomic theory class 9",
            "what is dalton's atomic theory class 11",
            "what is dalton atomic model",
        ],
        "note": "What Is Dalton's Atomic Theory? is a signed-out GB YouTube autocomplete hit (also class 9, class 11, and dalton atomic model). v02 opens on the claim itself: 'Every element is made of its own kind of atom, and each kind has its own weight.' Gold-foil bounce is already scheduled as JyRjM-9Yc8g (1 Nov), so this is 004's second search-titled Short.",
    }
    rec["air_date_draft_note"] = "2026-11-10 used for the gate only; slot is Chief's call. Clear of 004 gold-foil 1 Nov (JyRjM-9Yc8g)."
    rec["who_card_note"] = "card is the long's own label JOHN DALTON · Manchester, 1808, on screen 2.2–6.7 s, just after the hook, because this lift does not speak the name. Clear of the 0–2 s hook and the 9–14 s title, so 'Why believe him?' already has a face and a name."
    rec["plate_audit"] = {
        "replaced": "03_weights_line_v01 (Hp/Hg/Op tiles) is not in v02",
        "05_fixed_amounts": "2 fps centre crop of all 8 s: wooden molecule models, no letters. Opening stretch for Hydrogen / Oxygen.",
        "07_water_always": "gold sphere for 'Gold is heavier still'. Background chalkboard is a line schematic with no readable words (checked a zoom at 2.2 s and the 2 fps sheet).",
        "02_atomic_theory": "0.80 s through 3.49 s, brass stands and wood balls (clears the early desk-edge seam and keeps the later paper close-up out).",
        "04_gold_heavier": "no letters. Wood balls on the 'same fixed amounts' line only. The gold line uses 07, so the soft wood-grain note is cleared.",
        "20_what_is_order": "0.40 s through 3.82 s (crop_x 500), glowing brass-and-glass apparatus on the oak table for 'Water is always the same mix… tiny pieces with fixed weights.' No letters, no Explorer, replaces second appearance of 05_fixed_amounts.",
        "06_water_ratio": "rejected: the shelves read 1808.",
        "08_ruler_of_weights": "rejected: the ruler carries numerals.",
        "01_dalton_schoolroom": "frame 0 and the loop. Wall charts are illegible line diagrams, the same plate v01 already used and Chief did not fail.",
        "long": "03_weights_line_v01 is in 07_Edit-Project/part02_rough_v01_land_meta.json at 9.143–13.943 s (vo: and each kind has its own weight. Hydrogen is the lightest. Oxygen is heavier.). The long was not touched.",
    }
    (HERE / f"SHORT_{SID}_{VER}.json").write_text(json.dumps(rec, indent=2) + "\n")
    print(f"BUILT {SID} {rec['duration_s']} s {rec['words']} words sha {rec['sha256'][:12]} "
          f"captions {rec['caption_check']}")
    print(rec["gate"]["output"])
    print(rec["vo_check"]["output"])
    print(f"freezedetect: {len(rec['freezedetect_starts'])} events {rec['freezedetect_starts']}")


if __name__ == "__main__":
    main()
