#!/usr/bin/env python3
"""HOS 008 Short A v04 (J0912, £0). Locked VO unchanged.

J2224 FIX (7 Nov 2026): same Chief h47 recipe as v03, with row s06
(15.76–19.52 s) taken from the approved storm-shed plate
09_charge_string_c1_t1.mp4 at 0.60 s instead of a second stretch of
13_key_ribbon_t1.mp4. No generation, no upload.

    python3 _build_short_A_v04.py
"""
from __future__ import annotations

import hashlib
import json
import math
import struct
import subprocess
import sys
import wave
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
PROJ = HERE.parent
REPO = PROJ.parents[1]
OWB = Path("/Users/benjaminoats/YouTube/orbit-with-ben")
SHARED = Path("/Users/benjaminoats/YouTube/History Of Science/02_Video-Projects/008_Lightning-Franklin")
MEDIA = Path("/Users/benjaminoats/YouTube/hos-008-lightning/02_Video-Projects/008_Lightning-Franklin")
VO_MP3 = SHARED / "10_Shorts/vo_v02/hos_008_short_A_v02.mp3"
STT = SHARED / "10_Shorts/vo_v02/stt/hos_008_short_A_v02/stt_raw.json"
VO_SHA = "40ed4c4e2a1f2e58608cfe690bb8afd6e1d64c80eafb0a75f37d47648a7ba28e"
WORK = HERE / "_work_short_A_v04"
QA = HERE / "qa_short_A_v04"
SID = "short_A"
VER = "v04"
# 720p plates cannot fill 1080x1920 inside the 2.35x upscale limit (1920/720 = 2.67).
# The master is the largest even 9:16 that stays at 2.35x: 952x1692.
W, H, FPS = 952, 1692, 30
BAND_H = W * 9 // 16
BAND_TOP = (H - BAND_H) // 2
CREAM, INK, YEL = (245, 232, 210, 255), (28, 26, 28, 255), (255, 214, 70, 255)
FONT = "/System/Library/Fonts/Supplemental/Didot.ttc"
HOOK = "**NEVER** HIT IT"
LONG_TITLE = "Why Did Franklin Fly a Kite in a Storm?"
YT_TITLE = "Why Was Franklin's Kite Experiment So Dangerous?"
CARD_IN, CARD_OUT, CARD_FADE = 2.7, 6.2, 0.40
TITLE_IN, TITLE_OUT = 9.0, 14.0
TOTAL = 23.24
LOOP_S = 1.00
FRAME0_IN = 1.20  # loop plays up to this in-point, so the last frame matches frame 0
UPSCALE = 2.35

PLATES = {
    "kite": MEDIA / "04_Generated-Clips/part01/raw/v01/01_kite_open_t1.mp4",
    "climb": MEDIA / "04_Generated-Clips/part03/raw/v01/19_kite_climb_t1.mp4",
    "key": MEDIA / "04_Generated-Clips/part03/raw/v01/13_key_ribbon_t1.mp4",
    "twine": MEDIA / "04_Generated-Clips/part03/raw/v01/25_fibres_rise_t1.mp4",
    "knuckle": MEDIA / "04_Generated-Clips/part04/raw/v01/02_knuckle_spark_t1.mp4",
    "rod": MEDIA / "04_Generated-Clips/part04/raw/v01/10_richmann_rod_t1.mp4",
    "charge_key": MEDIA / "04_Generated-Clips/part04/raw/v01/09_charge_string_c1_t1.mp4",
}
CHARGE_KEY_SHA = "611e2633f2ea7f4417272b91af41b857bb6733d416363918a17a111be56f9c80"
# (t0, key, source in-point). Centre crop. S06 is the storm-shed key, once.
BEATS = [
    (0.00, "kite", FRAME0_IN),
    (2.58, "climb", 0.60),
    (5.76, "key", 0.60),
    (9.14, "twine", 0.60),
    (12.10, "knuckle", 0.60),
    (15.76, "charge_key", 0.60),
    (19.52, "rod", 0.60),
    (22.24, "kite", FRAME0_IN - LOOP_S),
]


def ff(*a: str, cwd: Path | None = None) -> None:
    subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", *a], check=True, cwd=cwd)


def probe(p: Path) -> float:
    return float(subprocess.check_output(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)], text=True))


def sha256(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def words() -> list[tuple[str, float, float]]:
    raw = json.loads(STT.read_text())["words"]
    out = []
    for w in raw:
        text = (w.get("text") or "").strip()
        if text:
            out.append((text, float(w["start"]), float(w["end"])))
    return out


def chunk_words(ws: list[tuple[str, float, float]]) -> list[dict]:
    chunks, i, n = [], 0, len(ws)
    while i < n:
        t0 = ws[i][1]
        parts, t_end, j = [ws[i][0]], ws[i][2], i + 1
        while j < n:
            wj, sj, ej = ws[j]
            if parts[-1][-1:] in ".?!":
                break
            if parts[-1][-1:] in ",;:" and sj - t0 >= 0.45 and (len(parts) >= 2 or wj[:1].isupper()):
                break
            if len(parts) >= 5 and sj - t0 >= 0.45:
                break
            if ej - t0 >= 1.55 and len(parts) >= 2:
                break
            parts.append(wj)
            t_end = ej
            j += 1
        t1 = ws[j][1] if j < n else t_end + 0.25
        t0_show = max(t0, 2.0)  # frame 0–2 s is the hook caption only
        if t1 > t0_show + 0.12:
            chunks.append({"text": " ".join(parts), "t0": round(t0_show, 3), "t1": round(min(t1, TOTAL - 0.05), 3)})
        i = j
    return chunks


def render_text(path: Path, text: str, size: int, y: int, *, index: int = 1, anchor: str = "top") -> None:
    font = ImageFont.truetype(FONT, size, index=index)
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
            draw.text((x, cy), t, font=font, fill=YEL if hot else CREAM, stroke_width=4, stroke_fill=INK)
            x += font.getlength(t) + space
        cy += lh + gap
    img.save(path)


def render_hook(path: Path) -> dict:
    size = 100
    font = None
    cap = 0
    while True:
        font = ImageFont.truetype(FONT, size, index=2)
        cap = -font.getbbox("H", anchor="ls")[1]
        if cap >= 0.09 * H:
            break
        size += 1
    tokens = [(w.strip("*"), w.startswith("**")) for w in HOOK.split()]
    widest = max(font.getlength(t) for t, _ in tokens)
    pitch = round(cap * 1.32)
    block = pitch * (len(tokens) - 1) + cap
    top = (H - block) // 2
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    for k, (t, hot) in enumerate(tokens):
        base = top + cap + k * pitch
        draw.text((W / 2, base), t, font=font, anchor="ms", fill=YEL if hot else CREAM,
                  stroke_width=6, stroke_fill=INK)
    img.save(path)
    return {"font_size": size, "cap_px": cap, "cap_pct": round(100 * cap / H, 2),
            "block_pct": [round(100 * top / H, 1), round(100 * (top + block) / H, 1)],
            "widest_pct": round(100 * widest / W, 1)}


def render_card(path: Path) -> dict:
    size = int(BAND_H * 0.115)
    font = ImageFont.truetype(FONT, size, index=2)
    text = "PHILADELPHIA · 1752"
    while font.getlength(text) > W - 120 and size > 48:
        size -= 2
        font = ImageFont.truetype(FONT, size, index=2)
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    y = BAND_TOP + BAND_H - 36
    # Year in yellow, place name in cream. One line, inside the centre band.
    place, year = "PHILADELPHIA · ", "1752"
    full_w = font.getlength(place + year)
    x = (W - full_w) / 2
    draw.text((x, y), place, font=font, anchor="ls", fill=CREAM, stroke_width=4, stroke_fill=INK)
    draw.text((x + font.getlength(place), y), year, font=font, anchor="ls", fill=YEL, stroke_width=4, stroke_fill=INK)
    img.save(path)
    return {"text": text, "size_px": size, "pct_of_band": round(100 * size / BAND_H, 1),
            "in_s": CARD_IN, "out_s": CARD_OUT}


def seg(src: Path, dst: Path, start: float, dur: float) -> None:
    if start < 0 or start + dur > probe(src) + 0.02:
        raise SystemExit(f"{src.name}: in {start} + {dur:.2f}s exceeds {probe(src):.2f}s")
    # 1280x720 scaled 2.35x, then the centre 9:16 (952x1692).
    vf = "scale=3008:1692:flags=lanczos,crop=952:1692:1028:0,setsar=1,fps=30"
    ff("-i", str(src), "-ss", f"{start:.3f}", "-t", f"{dur:.3f}", "-vf", vf, "-an",
       "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "veryfast", "-crf", "18", str(dst))


def synth_bed(path: Path, dur: float, sr: int = 48000) -> None:
    """Sparse D-minor plucked figure at 68 BPM. Own synthesis, no credit spend."""
    n = int(sr * (dur + 0.4))
    beat = 60.0 / 68.0
    roots = [146.83, 174.61, 220.00, 130.81, 196.00, 164.81]
    frames = bytearray()
    for i in range(n):
        t = i / sr
        phase = (t / beat) % 1.0
        root = roots[int(t / beat) % len(roots)]
        env = math.exp(-3.4 * phase) * min(1.0, t / 0.35) * min(1.0, max(0.0, (dur + 0.2 - t) / 0.35))
        if phase > 0.55:
            env = 0.0
        sample = 0.0
        for k, mul in enumerate((1.0, 2.0, 3.0)):
            sample += math.sin(2 * math.pi * root * mul * t) * (0.55, 0.18, 0.07)[k]
        g = env * 0.20
        v = int(max(-1, min(1, sample * g)) * 32767)
        frames += struct.pack("<hh", v, v)
    path.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(path), "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(sr)
        w.writeframes(bytes(frames))


def place_sfx(total: float) -> Path:
    kit = SHARED / "06_Sound-Effects/kit_v01"
    whoosh, tick = kit / "sfx_hos_whoosh_soft_v01.wav", kit / "sfx_hos_tick_ink_v01.wav"
    dst = WORK / "sfx_stem.wav"
    delay = int(CARD_IN * 1000)
    ff("-f", "lavfi", "-t", f"{total:.3f}", "-i", "anullsrc=channel_layout=stereo:sample_rate=48000",
       "-i", str(whoosh), "-i", str(tick), "-filter_complex",
       "[1:a]volume=-16dB,afade=t=out:st=0.55:d=0.25[w];"
       f"[2:a]volume=-10dB,adelay={delay}|{delay}[t];"
       "[0:a][w][t]amix=inputs=3:normalize=0:duration=first,alimiter=limit=0.5[a]",
       "-map", "[a]", "-c:a", "pcm_s16le", str(dst))
    return dst


def ebur128(p: Path) -> tuple[float, float]:
    err = subprocess.run(
        ["ffmpeg", "-nostats", "-hide_banner", "-i", str(p), "-af", "ebur128=peak=true", "-f", "null", "-"],
        capture_output=True, text=True).stderr
    i_lines = [ln for ln in err.splitlines() if ln.strip().startswith("I:") and "LUFS" in ln]
    p_lines = [ln for ln in err.splitlines() if ln.strip().startswith("Peak:") and "dBFS" in ln]
    if not i_lines or not p_lines:
        raise SystemExit(f"ebur128 failed on {p.name}")
    lufs = float(i_lines[-1].split("I:")[1].split("LUFS")[0].strip())
    peak = float(p_lines[-1].split("Peak:")[1].split("dBFS")[0].strip())
    return lufs, peak


def level_master(mp4: Path) -> dict:
    """Gate window is −14.0 ±0.5 LUFS and true peak ≤ −1.6 dBTP. A −14 / −1.5
    loudnorm target measures hot on a 23 s file, so the target sits lower."""
    tmp = mp4.with_suffix(".leveled.mp4")
    target, tp = -11.5, -2.0
    lufs2, peak2 = 0.0, 0.0
    for _ in range(3):
        ff("-i", str(mp4), "-c:v", "copy",
           "-af", f"loudnorm=I={target:.1f}:TP={tp:.1f}:LRA=11",
           "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2", "-movflags", "+faststart", str(tmp))
        lufs2, peak2 = ebur128(tmp)
        if -14.5 <= lufs2 <= -13.5 and peak2 <= -1.6:
            break
        target += (-14.0 - lufs2)
        if peak2 > -1.6:
            tp -= 0.3
    if not (-14.5 <= lufs2 <= -13.5) or peak2 > -1.6:
        tmp.unlink(missing_ok=True)
        raise SystemExit(f"level landed at {lufs2:.1f} LUFS / {peak2:.1f} dBTP")
    tmp.replace(mp4)
    return {"lufs": round(lufs2, 2), "true_peak_dbtp": round(peak2, 2), "loudnorm_I": round(target, 2)}


def build() -> dict:
    if sha256(VO_MP3) != VO_SHA:
        raise SystemExit("locked VO hash mismatch; refusing to continue")
    if sha256(PLATES["charge_key"]) != CHARGE_KEY_SHA:
        raise SystemExit("charge-string plate hash mismatch; refusing to continue")
    ws = words()
    if not 55 <= len(ws) <= 65:
        raise SystemExit(f"{len(ws)} words outside 55–65")
    if ws[0][1] > 0.15:
        raise SystemExit(f"first word at {ws[0][1]} s")
    payoff = next(w for w in ws if w[0].startswith("If"))
    WORK.mkdir(parents=True, exist_ok=True)
    QA.mkdir(parents=True, exist_ok=True)
    vo = WORK / "vo.wav"
    ff("-i", str(VO_MP3), "-ar", "48000", "-ac", "2", str(vo))
    if abs(probe(vo) - 22.24) > 0.05:
        raise SystemExit(f"VO duration {probe(vo)} is not the locked 22.24s")

    segs, plan = [], []
    for k, (t0, key, inn) in enumerate(BEATS):
        t1 = BEATS[k + 1][0] if k + 1 < len(BEATS) else TOTAL
        dur = round(t1 - t0, 3)
        if k == 0 and t1 > 3.0:
            raise SystemExit("first cut later than 3.0s")
        if key != "kite" or t0 == 0:
            if dur > 4.0:
                raise SystemExit(f"hold {dur}s")
        out = WORK / f"seg_{k:02d}.mp4"
        seg(PLATES[key], out, inn, dur)
        segs.append(out)
        plan.append({"t0": t0, "t1": t1, "plate": PLATES[key].name, "in_s": inn, "hold_s": dur,
                     "lands_on": "loop" if t0 >= 22.24 else "plate", "upscale": UPSCALE})
    (WORK / "pic.txt").write_text("".join(f"file '{s.name}'\n" for s in segs))
    pic = WORK / "picture.mp4"
    ff("-f", "concat", "-safe", "0", "-i", "pic.txt", "-c:v", "libx264", "-pix_fmt", "yuv420p",
       "-preset", "veryfast", "-crf", "18", "-r", str(FPS), "-t", f"{TOTAL:.3f}", str(pic), cwd=WORK)

    bed = PROJ / "05_Music" / "hos_008_short_A_v04_bed.wav"
    synth_bed(bed, TOTAL)
    prompt = (
        "Sparse D-minor plucked figure under a kite in a storm, quiet and even, room for a spoken voice. "
        "Pace: 64-76 BPM. NOT the 008 long gut-string quartet, NOT the 007 vaccine bed, NOT the Trees of Air bed, "
        "NOT any Orbit With Ben cosmic pad, NOT a drum loop, NOT a trailer sting."
    )
    bed.with_name(bed.stem + "_plan.json").write_text(json.dumps({
        "prompt": prompt, "film": "008", "short": "short_A_v04", "job": "J0912",
        "source": "own synthesis in _build_short_A_v04.py, 0 credits", "pace_bpm": "64-76",
    }, indent=2) + "\n")

    sfx = place_sfx(TOTAL)
    audio = WORK / "audio.wav"
    bed_db, sfx_db, sfx_level = -16.0, -18.0, {}
    for _ in range(6):
        ff("-i", str(vo), "-i", str(bed), "-i", str(sfx), "-filter_complex",
           f"[0:a]aformat=sample_rates=48000:channel_layouts=stereo,apad=whole_dur={TOTAL:.3f}[v];"
           f"[1:a]aformat=sample_rates=48000:channel_layouts=stereo,atrim=0:{TOTAL:.3f},asetpts=PTS-STARTPTS,"
           f"volume={bed_db:.2f}dB,afade=t=in:d=0.05,afade=t=out:st={TOTAL - 0.25:.3f}:d=0.25[b];"
           f"[2:a]aformat=sample_rates=48000:channel_layouts=stereo,atrim=0:{TOTAL:.3f},volume={sfx_db:.2f}dB[s];"
           "[v][b][s]amix=inputs=3:normalize=0:duration=first,alimiter=limit=0.89[a]",
           "-map", "[a]", "-t", f"{TOTAL:.3f}", "-c:a", "pcm_s16le", str(audio))
        stems = {}
        for name, src, extra in (
            ("vo", vo, f"apad=whole_dur={TOTAL:.3f}"),
            ("bed", bed, f"volume={bed_db:.2f}dB,atrim=0:{TOTAL:.3f}"),
            ("sfx", sfx, f"volume={sfx_db:.2f}dB,atrim=0:{TOTAL:.3f}"),
        ):
            stems[name] = WORK / f"stem_{name}.wav"
            ff("-i", str(src), "-af", extra, "-t", f"{TOTAL:.3f}", "-c:a", "pcm_s16le", str(stems[name]))
        r = subprocess.run([sys.executable, str(OWB / "scripts/sfx_kit.py"), "level",
                            "--vo", str(stems["vo"]), "--sfx", str(stems["sfx"]), "--bed", str(stems["bed"]),
                            "--minutes", f"{TOTAL / 60:.3f}"], capture_output=True, text=True)
        sfx_level = {"exit": r.returncode, "output": (r.stdout + r.stderr).strip(), "bed_db": bed_db, "sfx_db": sfx_db}
        if r.returncode == 0:
            break
        bed_db -= 3.0
        sfx_db -= 3.0
    if sfx_level["exit"] != 0:
        raise SystemExit(f"sfx level failed: {sfx_level['output']}")

    chunks = chunk_words(ws)
    overlays = []
    hook_png = WORK / "cap_hook.png"
    hook_meta = render_hook(hook_png)
    overlays.append((hook_png, 0.0, 2.0, "hook", "NEVER HIT IT"))
    for i, c in enumerate(chunks):
        png = WORK / f"cap_{i:03d}.png"
        render_text(png, c["text"], 52, 330, anchor="bottom")
        overlays.append((png, c["t0"], c["t1"], "vo", c["text"]))
    title_png = WORK / "cap_title.png"
    render_text(title_png, LONG_TITLE, 58, 220, index=2)
    overlays.append((title_png, TITLE_IN, TITLE_OUT, "title", LONG_TITLE))
    card_png = WORK / "card_when.png"
    card_meta = render_card(card_png)

    inputs = ["-i", str(pic), "-i", str(audio)]
    for png, *_ in overlays:
        inputs += ["-loop", "1", "-i", str(png)]
    ci = 2 + len(overlays)
    inputs += ["-loop", "1", "-t", f"{TOTAL:.3f}", "-i", str(card_png)]
    fc, last = [], "[0:v]"
    fc.append(f"[{ci}:v]format=rgba,fade=t=in:st={CARD_IN}:d={CARD_FADE}:alpha=1,"
              f"fade=t=out:st={CARD_OUT - CARD_FADE}:d={CARD_FADE}:alpha=1[card]")
    fc.append(f"{last}[card]overlay=0:0:enable='between(t,{CARD_IN:.3f},{CARD_OUT:.3f})'[vc]")
    last = "[vc]"
    for i, (_, t0, t1, *_r) in enumerate(overlays, 2):
        fc.append(f"{last}[{i}:v]overlay=0:0:enable='between(t,{t0:.3f},{t1:.3f})'[v{i}]")
        last = f"[v{i}]"
    mp4 = HERE / "hos_008_short_A_v04.mp4"
    ff(*inputs, "-filter_complex", ";".join(fc), "-map", last, "-map", "1:a",
       "-c:v", "libx264", "-pix_fmt", "yuv420p", "-profile:v", "high", "-preset", "veryfast",
       "-crf", "18", "-r", str(FPS), "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2",
       "-t", f"{TOTAL:.3f}", "-movflags", "+faststart", str(mp4))
    level = level_master(mp4)
    return {
        "file": str(mp4), "sha256": sha256(mp4), "duration_s": round(probe(mp4), 3),
        "vo_sha256": VO_SHA, "words": len(ws), "first_word_s": ws[0][1],
        "payoff_word": payoff[0], "payoff_s": payoff[1],
        "payoff_frac_of_total": round(payoff[1] / TOTAL, 3),
        "last_word_s": ws[-1][2], "last_word_to_end_s": round(TOTAL - ws[-1][2], 3),
        "level": level, "hook": hook_meta, "card": card_meta, "sfx_level": sfx_level,
        "plan": plan, "youtube_title_draft": YT_TITLE, "title_on_screen": LONG_TITLE,
        "bed": str(bed), "upscale": UPSCALE,
        "spoken": " ".join(w for w, _, _ in ws),
    }


def gates(info: dict) -> dict:
    mp4 = Path(info["file"])
    cuts, pool, seen = [], [], set()
    for k, row in enumerate(info["plan"], 1):
        src = f"loop_{row['plate']}" if row["lands_on"] == "loop" else row["plate"]
        cuts.append({"row": f"s{k:02d}", "timeline_in": row["t0"], "timeline_out": row["t1"],
                     "source": src, "upscale": row["upscale"], "video": True,
                     "framing": {"offset": row["in_s"]}})
        if src not in seen:
            seen.add(src)
            pool.append({"file_id": src, "title": f"Flow plate {row['plate']}"})
    # The date card is an edit overlay on moving picture. Plate gates score the plates.
    # A still overlay row is what polish_gate calls push jitter.
    cuts_f, pool_f = QA / "cuts.json", QA / "pool.json"
    cuts_f.write_text(json.dumps(cuts, indent=2) + "\n")
    pool_f.write_text(json.dumps(pool, indent=2) + "\n")
    out = {}
    for name, cmd in (
        ("polish", [sys.executable, str(OWB / "scripts/polish_gate.py"), str(mp4),
                    "--cuts", str(cuts_f), "--out", str(QA / "polish_gate.json")]),
        ("picture", [sys.executable, str(OWB / "scripts/picture_qa.py"), str(mp4),
                     "--cuts", str(cuts_f), "--pool", str(pool_f), "--out-dir", str(QA / "picture_qa")]),
        ("music", [sys.executable, str(OWB / "scripts/music_gate.py"), str(PROJ),
                   "--bed", info["bed"], "--video", str(mp4), "--out", str(QA / "music_gate.json")]),
        ("open", [sys.executable, str(REPO / "00_Brand/Channel-Setup/tools/gate_shorts_open.py"), "check", str(mp4),
                  "--air-date", "2026-11-18", "--script", str(WORK / "spoken.txt"), "--vo", str(WORK / "vo.wav")]),
    ):
        r = subprocess.run(cmd, capture_output=True, text=True)
        text = (r.stdout + r.stderr).strip()
        (QA / f"{name}.txt").write_text(text + "\n")
        out[name] = {"exit": r.returncode, "tail": text[-1500:]}
    return out


def main() -> None:
    info = build()
    (WORK / "spoken.txt").write_text(info["spoken"] + "\n")
    info["gates"] = gates(info)
    sfx_text = info["sfx_level"].get("output", "")
    (QA / "sfx.txt").write_text(sfx_text + "\n")
    info["gates"]["sfx"] = {"exit": info["sfx_level"]["exit"], "tail": sfx_text[-1500:]}
    (QA / "BUILD.json").write_text(json.dumps(info, indent=2) + "\n")
    print(json.dumps({k: info[k] for k in (
        "file", "sha256", "duration_s", "words", "first_word_s", "payoff_s",
        "payoff_frac_of_total", "last_word_to_end_s", "level", "upscale")}, indent=2))
    for name, g in info["gates"].items():
        print(f"GATE {name} exit {g['exit']}")


if __name__ == "__main__":
    main()
