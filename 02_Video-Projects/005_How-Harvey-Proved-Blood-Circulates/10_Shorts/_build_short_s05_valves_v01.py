#!/usr/bin/env python3
"""HOS 005 Short s05 v01 (test B, search-titled): a stretch lifted from the long's own Part 04 (J0254).

No new VO, picture or bed. VO: part04_the_tied_arm_v01_raw.mp3, "Now the little doors. … and it slides
through easily." (57 words), with pauses capped at 0.6 s as in the long's VO finish. The Part 04 v02/v03
fix only replaced an earlier sentence, so this stretch is the long's own audio. Plates: the long's Part 04
KEEP takes (06 t1, 08 t4, 09 t3, 10 t3, 13 t3). Bed: the long's Part 04 temp bed. Hook on frame 0, word
captions, one person card (Fabricius · Padua, c. 1600, from the long's Part 02 line and label), the long's
title at 9–14 s, the last 4 s on the opening plate so it loops. Then caption check, gate_shorts_open,
vo_check, freezedetect, stills, iCloud phone copy. Never uploads.

    python3 _build_short_s05_valves_v01.py [--air-date YYYY-MM-DD] [--no-icloud]
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
import json  # noqa: E402
import shutil  # noqa: E402

from PIL import Image, ImageDraw, ImageFont  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _build_shorts_v03 as b  # noqa: E402

HERE, PROJ = b.HERE, b.PROJ
SID = "s05_valves"
VER = "v01"
JOB = "J0254"
WORK = HERE / f"_work_{SID}_{VER}"
RAW_VO = PROJ / "02_Voiceover/part04_the_tied_arm_v01_raw.mp3"
RAW_ALIGN = PROJ / "02_Voiceover/part04_the_tied_arm_v01_raw_align.json"
FIRST, LAST, BEFORE_LAST = "Now", "easily.", "through"
WIN = (46.0, 69.9)
MAX_PAUSE = 0.6
BED = PROJ / "05_Music/hos005-part04-temp_score_bed_v01.mp3"
HOOK = "DOORS IN **VEINS**"
CARD = ("FABRICIUS", "Padua, c. 1600")
CARD_IN, CARD_OUT, CARD_FADE = 5.5, 8.95, 0.35
BAND_TOP, BAND_H = (b.H - 608) // 2, 608
TITLE_DRAFT = "Why Do Veins Have Valves?"
SCRIPT_TXT = WORK / f"{SID}.txt"


def P4(name: str) -> Path:
    return b.CLIPS / f"part04/raw/v01/{name}.mp4"


# (index of the word the plate lands on, plate, in-point s, crop x on 1920×1080); "loop" = last 4 s.
BEATS = [(0, P4("13_one_way_t3"), 0.3, 656),             # Now the little doors.
         (4, P4("06_veins_swell_t1"), 4.0, 750),         # Along the swollen veins you can see small knots.
         (13, P4("08_knots_valve_t4"), 0.1, 656),        # Each one is a valve, the flaps Fabricius found.
         (22, P4("09_push_stops_t3"), 0.3, 800),         # Harvey presses a finger on a vein
         (30, P4("09_push_stops_t3"), 3.4, 800),         # and pushes the blood towards the hand.
         (36, P4("08_knots_valve_t4"), 4.6, 656),        # It stops dead at the next valve.
         (43, P4("10_slides_heart_t3"), 0.5, 1100),      # He pushes it the other way,
         ("loop", P4("13_one_way_t3"), 0.3, 656)]        # towards the heart, and it slides through easily.


def lifted_vo(work: Path) -> tuple[Path, list[tuple[str, float, float]]]:
    """Cut the stretch from the raw take, capping each pause at MAX_PAUSE; return the wav and remapped words."""
    words = [w for w in b.words_from_align(RAW_ALIGN) if WIN[0] <= w[1] <= WIN[1]]
    i0 = next(i for i, w in enumerate(words) if w[0] == FIRST)
    i1 = next(i for i, w in enumerate(words) if i > i0 and w[0] == LAST and words[i - 1][0] == BEFORE_LAST)
    words = words[i0:i1 + 1]
    spans: list[list[float]] = []
    for _, s, e in words:
        s0, e0 = s - 0.06, e + 0.06
        if spans and s0 - spans[-1][1] <= MAX_PAUSE:
            spans[-1][1] = max(spans[-1][1], e0)
        elif spans:
            spans.append([max(s0, spans[-1][1] + 0.0), e0])
        else:
            spans.append([s0, e0])
    pieces, out_t, remap = [], 0.0, []
    gap = MAX_PAUSE
    for k, (s, e) in enumerate(spans):
        if k:
            out_t += gap
        remap.append((s, e, out_t))
        out_t += e - s
    mapped = []
    for w, s, e in words:
        for rs, re_, ot in remap:
            if rs <= s <= re_:
                mapped.append((w, round(ot + s - rs, 3), round(ot + e - rs, 3)))
                break
    fc = []
    for k, (s, e) in enumerate(spans):
        fc.append(f"[0:a]atrim={s:.3f}:{e:.3f},asetpts=PTS-STARTPTS,"
                  f"afade=t=in:d=0.02,afade=t=out:st={e - s - 0.03:.3f}:d=0.03,"
                  f"aformat=sample_rates=48000:channel_layouts=stereo[s{k}]")
        if k + 1 < len(spans):
            fc.append(f"anullsrc=r=48000:cl=stereo,atrim=0:{gap:.3f}[g{k}]")
    order = "".join(f"[s{k}]" + (f"[g{k}]" if k + 1 < len(spans) else "") for k in range(len(spans)))
    n = len(spans) * 2 - 1
    fc.append(f"{order}concat=n={n}:v=0:a=1[a]")
    wav = work / f"hos_005_{SID}_vo_{VER}.wav"
    b.ff("-i", str(RAW_VO), "-filter_complex", ";".join(fc), "-map", "[a]", "-c:a", "pcm_s16le", str(wav))
    return wav, mapped


def render_card(path: Path, alpha: float = 1.0) -> dict:
    """Lower third of the 16:9 centre band: name on line one, place and date on line two."""
    size1 = int(BAND_H * 0.12)
    size2 = int(BAND_H * 0.075)
    f1 = ImageFont.truetype(b.FONT, size1, index=2)
    f2 = ImageFont.truetype(b.CTA_FONT, size2)
    img = Image.new("RGBA", (b.W, b.H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    x = 70
    y2 = BAND_TOP + BAND_H - 40
    y1 = y2 - size2 - 18
    shade = Image.new("RGBA", (b.W, b.H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shade)
    top = y1 - size1 - 30
    for yy in range(top, BAND_TOP + BAND_H):
        a = int(140 * min(1.0, (yy - top) / 120))
        sd.line([(0, yy), (b.W, yy)], fill=(0, 0, 0, a))
    img = Image.alpha_composite(img, shade)
    d = ImageDraw.Draw(img)
    d.text((x, y1), CARD[0], font=f1, anchor="ls", fill=b.YEL, stroke_width=4, stroke_fill=b.INK)
    d.text((x, y2), CARD[1], font=f2, anchor="ls", fill=b.CREAM, stroke_width=3, stroke_fill=b.INK)
    img.save(path)
    return {"name": CARD[0], "line2": CARD[1], "line1_px": size1, "line1_pct_of_band": 12.0,
            "band": [BAND_TOP, BAND_TOP + BAND_H], "in_s": CARD_IN, "out_s": CARD_OUT, "fade_s": CARD_FADE}


def build(air_date: str) -> dict:
    if WORK.exists():
        shutil.rmtree(WORK)
    WORK.mkdir(parents=True)
    vo, words = lifted_vo(WORK)
    SCRIPT_TXT.write_text(" ".join(w for w, _, _ in words) + "\n")
    vo_s = b.probe(vo)
    total = round(vo_s + b.TAIL_S, 3)
    if not 22.0 <= total <= 27.0:
        raise SystemExit(f"{SID}: {total} s outside 22–27 s")
    if not 55 <= len(words) <= 65:
        raise SystemExit(f"{SID}: {len(words)} words outside 55–65")

    cuts = []
    for w, src, ins, x in BEATS:
        t = 0.0 if w == 0 else (total - b.LOOP_S if w == "loop" else max(0.0, words[w][1] - 0.15))
        cuts.append((round(t, 3), src, ins, x, w))
    plan, segs = [], []
    for k, (t, src, ins, x, w) in enumerate(cuts):
        end = cuts[k + 1][0] if k + 1 < len(cuts) else total
        d = end - t
        if d < 1.2:
            raise SystemExit(f"{SID}: beat {k} only {d:.2f} s")
        out = WORK / f"seg_{k:02d}.mp4"
        b.seg(src, out, ins, d, x)
        segs.append(out)
        plan.append({"t0": t, "t1": round(end, 3), "plate": src.relative_to(PROJ).as_posix(), "in_s": ins,
                     "crop_x": x, "lands_on": w if w in (0, "loop") else words[w][0]})
    (WORK / "pic.txt").write_text("".join(f"file '{s.name}'\n" for s in segs))
    pic = WORK / "picture.mp4"
    b.ff("-f", "concat", "-safe", "0", "-i", "pic.txt", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "fast",
         "-crf", "17", "-r", str(b.FPS), "-t", f"{total:.3f}", str(pic), cwd=WORK)

    bed_gain = (b.mean_db(vo) - 20.0) - b.mean_db(BED)
    audio = WORK / "audio.wav"
    b.ff("-i", str(vo), "-stream_loop", "-1", "-i", str(BED), "-filter_complex",
         f"[0:a]aformat=sample_rates=48000:channel_layouts=stereo,apad=whole_dur={total:.3f}[v];"
         f"[1:a]aformat=sample_rates=48000:channel_layouts=stereo,atrim=0:{total:.3f},asetpts=PTS-STARTPTS,"
         f"volume={bed_gain:.2f}dB,afade=t=in:d=0.05,afade=t=out:st={total - 0.2:.3f}:d=0.2[b];"
         f"[v][b]amix=inputs=2:normalize=0:duration=first[a]",
         "-map", "[a]", "-t", f"{total:.3f}", "-c:a", "pcm_s16le", str(audio))

    chunks = b.chunk_words(words)
    overlays = []
    hook_png = WORK / "cap_hook.png"
    hook_meta = b.render_hook(hook_png, HOOK)
    overlays.append((hook_png, 0.0, 2.0, "hook", HOOK.replace("**", "")))
    for i, c in enumerate(chunks):
        png = WORK / f"cap_{i:03d}.png"
        b.render(png, c["text"], 52, 330, anchor="bottom")
        overlays.append((png, c["t0"], min(c["t1"], total - 0.05), "vo", c["text"]))
    title_png = WORK / "cap_title.png"
    b.render(title_png, b.TITLE, 62, 250, index=2, stroke=4)
    shade = Image.new("RGBA", (b.W, b.H), (0, 0, 0, 0))
    for yy in range(560):
        a = int(150 * (1 - yy / 560) ** 1.5)
        ImageDraw.Draw(shade).line([(0, yy), (b.W, yy)], fill=(0, 0, 0, a))
    Image.alpha_composite(shade, Image.open(title_png)).save(title_png)
    overlays.append((title_png, b.TITLE_IN, b.TITLE_OUT, "title", b.TITLE))
    cta = WORK / "cap_cta.png"
    b.render(cta, "watch the full film →", 44, 250, anchor="bottom", font_path=b.CTA_FONT)
    overlays.append((cta, total - b.LOOP_S, total - 0.08, "cta", "watch the full film →"))
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
    mp4 = HERE / f"hos_005_{SID}_{VER}.mp4"
    b.ff(*inputs, "-filter_complex", ";".join(fc), "-map", last, "-map", "1:a", "-c:v", "libx264",
         "-pix_fmt", "yuv420p", "-profile:v", "high", "-preset", "medium", "-crf", "18", "-r", str(b.FPS),
         "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2", "-t", f"{total:.3f}", "-movflags", "+faststart",
         str(mp4))
    timeline = [{"role": r, "text": t, "t0": round(a, 3), "t1": round(c, 3)} for _, a, c, r, t in overlays]
    timeline.append({"role": "who", "text": " · ".join(CARD), "t0": CARD_IN, "t1": CARD_OUT})
    (WORK / "timeline.json").write_text(json.dumps({"plan": plan, "overlays": timeline}, indent=2) + "\n")
    return {"id": SID, "job": JOB, "test": "B (search-titled)", "air_date_draft": air_date,
            "file": mp4.relative_to(PROJ).as_posix(), "sha256": b.sha256(mp4), "duration_s": round(b.probe(mp4), 3),
            "vo_source": RAW_VO.relative_to(PROJ).as_posix(), "vo_window_raw_s": list(WIN),
            "vo_s": round(vo_s, 3), "words": len(words), "max_pause_s": MAX_PAUSE,
            "bed": BED.name, "bed_gain_db": round(bed_gain, 2), "hook": HOOK.replace("**", ""),
            "hook_layer": hook_meta, "who_card": card_meta, "title_on_screen": b.TITLE,
            "youtube_title_draft": TITLE_DRAFT, "plan": plan, "captions": len(chunks), "timeline": timeline}


def caption_check(mp4: Path, timeline: list[dict]) -> dict:
    frames = WORK / "frames"
    frames.mkdir(parents=True, exist_ok=True)
    vo_rows = [r for r in timeline if r["role"] == "vo"]
    prev_text = prev_hash = None
    changes = matched = 0
    t, dur = 0.0, b.probe(mp4)
    import hashlib
    while t < dur - 0.05:
        crop = frames / f"c{t:05.1f}.png"
        b.ff("-ss", f"{t:.3f}", "-i", str(mp4), "-frames:v", "1", "-vf", "crop=1000:320:40:1250", str(crop))
        text = next((r["text"] for r in vo_rows if r["t0"] <= t < r["t1"]), None)
        h = hashlib.md5(crop.read_bytes()).hexdigest()
        if prev_text is not None and text != prev_text:
            changes += 1
            matched += h != prev_hash
        prev_text, prev_hash = text, h
        t += 0.5
    ratio = matched / changes if changes else 0.0
    return {"ok": changes >= 7 and ratio >= 0.7, "changes": changes, "ratio": round(ratio, 2)}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--air-date", default="2026-11-29")
    ap.add_argument("--no-icloud", action="store_true")
    ns = ap.parse_args()
    rec = build(ns.air_date)
    mp4 = PROJ / rec["file"]
    rec["caption_check"] = caption_check(mp4, rec.pop("timeline"))
    code, out = b.run([sys.executable, str(b.GATE), "check", str(mp4), "--air-date", ns.air_date])
    rec["gate"] = {"exit": code, "output": out}
    code, out = b.run([str(b.VO_PY), str(b.VO_CHECK), str(mp4), "--script", str(SCRIPT_TXT)])
    rec["vo_check"] = {"exit": code, "output": out}
    rec["freezedetect_starts"] = b.freeze(mp4)
    stills = []
    for t in (0.0, 3.5, 11.5, rec["duration_s"] - 1.0):
        st = WORK / f"{mp4.stem}_t{t:05.1f}.jpg"
        b.ff("-ss", f"{t:.3f}", "-i", str(mp4), "-frames:v", "1", "-q:v", "3", str(st))
        stills.append(st.relative_to(PROJ).as_posix())
    rec["stills"] = stills
    if not ns.no_icloud:
        b.ICLOUD.mkdir(parents=True, exist_ok=True)
        shutil.copy2(mp4, b.ICLOUD / mp4.name)
        rec["icloud"] = str(b.ICLOUD / mp4.name)
    (HERE / f"SHORT_{SID}_{VER}.json").write_text(json.dumps(rec, indent=2) + "\n")
    print(f"BUILT {SID} {rec['duration_s']} s {rec['words']} words sha {rec['sha256'][:12]} "
          f"captions {rec['caption_check']}")
    print(rec["gate"]["output"])
    print(rec["vo_check"]["output"])
    print(f"freezedetect: {len(rec['freezedetect_starts'])} events {rec['freezedetect_starts']}")


if __name__ == "__main__":
    main()
