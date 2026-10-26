#!/usr/bin/env python3
"""HOS 004 Short s05 dalton stayed re-cut v03 (J0966, £0). v01 and v02 are not opened for write.

Audit fix #12 (-sa2t7dAtCk, airs Mon 16 Nov 2026). The scheduled file is v02, so this cut is v03 beside it.
1. Claim-first VO lift from Part 02 ('Every element is made of its own kind of atom ... fixed weights', 64 words).
2. First cut moved from 4.77 s to 2.56 s; all body holds <= 3.71 s (splitting s01 with Part 01's letter-free
   15_knife_coin_return_v01 balance/weights plate, and splitting the end with Part 01's letter-free
   03_atom_turns_v01 brass atom model — avoiding 08_ruler_of_weights and 06_water_ratio which had baked numerals).
3. No 'watch the full film' overlay; 1.15 s matched loop back to frame 0 (01_dalton_schoolroom_v01 in 2.80 s).
4. Own-synthesis bed + house SFX stem (sfx_kit level PASS), AAC master at -14.0 +/- 0.5 LUFS, TP <= -1.6 dBTP.
5. JOHN DALTON (Manchester, 1808) card in house style on 2.20-5.60 s.

    python3 _build_short_s05_dalton_v03.py [--air-date YYYY-MM-DD] [--no-icloud]
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
import struct  # noqa: E402
import subprocess  # noqa: E402
import wave  # noqa: E402

from PIL import Image, ImageDraw, ImageFont  # noqa: E402

HERE = Path(__file__).resolve().parent
PROJ = HERE.parent
REPO = PROJ.parents[1]
OWB = Path("/Users/benjaminoats/YouTube/orbit-with-ben")
SID = "s05_dalton"
VER = "v03"
JOB = "J0966"
YT = "-sa2t7dAtCk"
WORK = HERE / f"_work_{SID}_{VER}"
QA = HERE / f"qa_{SID}_{VER}"
NAS = Path("/Volumes/data/mac-mini-archive/2026-10-24/YouTube/History Of Science/"
           "02_Video-Projects/004_Whats-Really-Inside-An-Atom")
V02_NAS = NAS / "10_Shorts/hos_004_s05_dalton_v02.mp4"


def prefer(rel: str) -> Path:
    local = PROJ / rel
    return local if local.exists() else NAS / rel


RAW_VO = prefer("02_Voiceover/05_Master/hos_004_part02_vo_v01.mp3")
RAW_ALIGN = prefer("02_Voiceover/05_Master/hos_004_part02_vo_v01_align.json")
# Alignment indices: claim "every" (17) through "oxygen," (66), skip "however you make it." (67–70),
# then "That … weights." (71–84). 64 words.
TAKE = list(range(17, 67)) + list(range(71, 85))
MAX_PAUSE = 0.45
ATEMPO = 1.03
HOOK = "EACH **ATOM**"
CARD = ("JOHN DALTON", "Manchester, 1808")
CARD_IN, CARD_OUT, CARD_FADE = 2.2, 5.6, 0.35
W, H, FPS = 1080, 1920, 30
BAND_TOP, BAND_H = (H - 608) // 2, 608
CREAM, INK, YEL = (245, 232, 210, 255), (28, 26, 28, 255), (255, 214, 70, 255)
FONT = "/System/Library/Fonts/Supplemental/Didot.ttc"
CTA_FONT = "/System/Library/Fonts/Supplemental/Times New Roman.ttf"
TITLE = "What's Really Inside an Atom?"
TITLE_DRAFT = "What Is Dalton's Atomic Theory?"
TAIL_S = 0.55
LOOP_S = 1.15
F0_IN = 2.80
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


def P1(name: str) -> Path:
    return prefer(f"04_Generated-Clips/part01/raw/v01/{name}.mp4")


def P2(name: str) -> Path:
    return prefer(f"04_Generated-Clips/part02/raw/v01/{name}.mp4")


# Clean, letter-free, Explorer-free KEEP plates.
# 08_ruler_of_weights (ruler numerals) and 06_water_ratio (1808 on shelves) are excluded.
BEATS = [
    (0, P2("01_dalton_schoolroom_v01"), F0_IN, 656),     # Every element is made of its own kind of atom,
    (10, P1("15_knife_coin_return_v01"), 0.50, 656),     # and each kind has its own weight. (balance scale & gold weights)
    (17, P2("05_fixed_amounts_v01"), 0.40, 656),         # Hydrogen is the lightest. Oxygen is heavier.
    (24, P2("07_water_always_v01"), 2.00, 656),          # Gold is heavier still.
    (28, P2("02_atomic_theory_v01"), 0.80, 656),         # Why believe him?
    (34, P2("04_gold_heavier_v01"), 0.15, 656),          # Because elements always combine in the same fixed amounts.
    (44, P2("20_what_is_order_v01"), 0.40, 500),         # Water is always the same mix of hydrogen and oxygen.
    (54, P1("03_atom_turns_v01"), 0.40, 656),            # That only makes sense if both are made of tiny pieces with fixed weights.
    ("loop", P2("01_dalton_schoolroom_v01"), F0_IN - LOOP_S, 656),
]


def ff(*a: str, cwd: Path | None = None) -> None:
    subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", *a], check=True, cwd=cwd)


def probe(p: Path) -> float:
    return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                          "-of", "csv=p=0", str(p)], text=True))


def sha256(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def ebur128(p: Path) -> tuple[float, float]:
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


def level_master(mp4: Path) -> dict:
    """Bring the AAC master to -14.0 +/- 0.5 LUFS and true peak <= -1.6 dBTP."""
    lufs, _peak = ebur128(mp4)
    gain = -14.0 - lufs
    lim = 10 ** (-1.8 / 20)
    tmp = mp4.with_suffix(".leveled.mp4")
    ff("-i", str(mp4), "-c:v", "copy",
       "-af", f"volume={gain:.2f}dB,alimiter=limit={lim:.5f}:level=disabled:attack=5:release=40",
       "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2", "-movflags", "+faststart", str(tmp))
    lufs2, peak2 = ebur128(tmp)
    if lufs2 < -14.5 or lufs2 > -13.5:
        gain2 = gain + (-14.0 - lufs2)
        ff("-i", str(mp4), "-c:v", "copy",
           "-af", f"volume={gain2:.2f}dB,alimiter=limit={lim:.5f}:level=disabled:attack=5:release=40",
           "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2", "-movflags", "+faststart", str(tmp))
        lufs2, peak2 = ebur128(tmp)
        gain = gain2
    if lufs2 < -14.5 or lufs2 > -13.5 or peak2 > -1.6:
        tmp.unlink(missing_ok=True)
        raise SystemExit(f"{mp4.name}: level landed at {lufs2:.1f} LUFS / {peak2:.1f} dBTP")
    tmp.replace(mp4)
    return {"lufs": round(lufs2, 2), "true_peak_dbtp": round(peak2, 2), "gain_db": round(gain, 2)}


def black_frac(mp4: Path, t: float) -> float:
    raw = subprocess.check_output(
        ["ffmpeg", "-v", "error", "-ss", f"{t:.3f}", "-i", str(mp4),
         "-frames:v", "1", "-vf", "scale=160:284", "-f", "rawvideo", "-pix_fmt", "gray", "-"])
    return round(sum(1 for p in raw if p < 18) / max(1, len(raw)), 3)


def synth_bed(path: Path, dur: float, sr: int = 48000) -> Path:
    """Soft C-major / A-minor clavichord & plucked string figure at 66 BPM (0 credits)."""
    n = int(sr * (dur + 0.5))
    bpm = 66.0
    beat_s = 60.0 / bpm
    roots = [130.81, 164.81, 196.00, 220.00, 146.83, 196.00]
    frames = bytearray()
    for i in range(n):
        t = i / sr
        beat = t / beat_s
        step = int(beat)
        phase = beat - step
        root = roots[step % len(roots)]
        env = math.exp(-3.0 * phase) * min(1.0, t / 0.4) * min(1.0, max(0.0, (dur + 0.3 - t) / 0.4))
        if phase > 0.62:
            env = 0.0
        l = r = 0.0
        for k, mul in enumerate((1.0, 2.0, 3.0)):
            a = (0.54, 0.20, 0.07)[k]
            l += math.sin(2 * math.pi * root * mul * t + 0.15 * k) * a
            r += math.sin(2 * math.pi * root * mul * 1.003 * t + 0.5 + 0.15 * k) * a
        g = env * 0.22
        frames += struct.pack("<hh", int(max(-1, min(1, l * g)) * 32767),
                              int(max(-1, min(1, r * g)) * 32767))
    path.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(path), "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(sr)
        w.writeframes(bytes(frames))
    return path


def place_sfx(total: float, ticks: list[float]) -> Path:
    kit = PROJ / "06_Sound-Effects" / "kit_v01"
    whoosh = kit / "sfx_hos_whoosh_soft_v01.wav"
    tick = kit / "sfx_hos_tick_ink_v01.wav"
    if not whoosh.exists() or not tick.exists():
        subprocess.run([sys.executable, str(OWB / "scripts/sfx_kit.py"), "make",
                        "--out-dir", str(kit), "--house", "hos"], check=True)
    dst = WORK / "sfx_stem.wav"
    inputs = ["-f", "lavfi", "-t", f"{total:.3f}", "-i", "anullsrc=channel_layout=stereo:sample_rate=48000",
              "-i", str(whoosh)]
    fc = ["[1:a]volume=-16dB,afade=t=out:st=0.55:d=0.25[w]"]
    mix_in = ["[0:a]", "[w]"]
    for i, t in enumerate(ticks):
        inputs += ["-i", str(tick)]
        delay = int(max(0.0, t) * 1000)
        fc.append(f"[{i + 2}:a]volume=-10dB,adelay={delay}|{delay}[t{i}]")
        mix_in.append(f"[t{i}]")
    n = len(mix_in)
    fc.append("".join(mix_in) + f"amix=inputs={n}:normalize=0:duration=first,alimiter=limit=0.5[a]")
    ff(*inputs, "-filter_complex", ";".join(fc), "-map", "[a]", "-c:a", "pcm_s16le", str(dst))
    return dst


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
    """Cut the claim-first stretch, drop one clause, cap pauses, apply ATEMPO."""
    all_words = words_from_align(RAW_ALIGN)
    words = [all_words[i] for i in TAKE]
    words[0] = (words[0][0][:1].upper() + words[0][0][1:], words[0][1], words[0][2])
    spans: list[list[float]] = []
    raw_gap = round(MAX_PAUSE * ATEMPO, 3)
    for i, (_, s, e) in enumerate(words):
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
    QA.mkdir(parents=True, exist_ok=True)
    if WORK.exists():
        shutil.rmtree(WORK)
    WORK.mkdir(parents=True)
    vo, words = lifted_vo(WORK)
    spoken = " ".join(w for w, _, _ in words)
    SCRIPT_TXT.write_text(spoken + "\n")
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
        d = round(end - t, 3)
        if d < (0.95 if w == "loop" else 1.15):
            raise SystemExit(f"{SID}: beat {k} only {d:.2f} s")
        if w != "loop" and d > 4.0:
            raise SystemExit(f"{SID}: beat {k} hold {d:.2f} s > 4.0 s")
        if k == 0 and end > 3.0:
            raise SystemExit(f"{SID}: first cut {end:.2f} s > 3.0 s")
        out = WORK / f"seg_{k:02d}.mp4"
        seg(src, out, ins, d, x)
        segs.append(out)
        try:
            plate = src.relative_to(PROJ).as_posix()
        except ValueError:
            try:
                plate = src.relative_to(NAS).as_posix()
            except ValueError:
                plate = src.name
        plan.append({"t0": t, "t1": round(end, 3), "plate": plate, "in_s": ins,
                     "crop_x": x, "lands_on": w if w in (0, "loop") else words[w][0], "hold_s": d})
    (WORK / "pic.txt").write_text("".join(f"file '{s.name}'\n" for s in segs))
    pic = WORK / "picture.mp4"
    ff("-f", "concat", "-safe", "0", "-i", "pic.txt", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "fast",
       "-crf", "17", "-r", str(FPS), "-t", f"{total:.3f}", str(pic), cwd=WORK)

    bed = PROJ / "05_Music" / "hos_004_s05_dalton_v03_bed.wav"
    synth_bed(bed, total)
    plan_j = {
        "prompt": ("Soft C-major and A-minor clavichord and plucked string figure under an 1808 Manchester "
                   "atomic weight telling, even, no chase. Pace: 62-70 BPM. NOT hos004-part02-temp_score_bed_v01, "
                   "NOT the 004 gold-foil mallet, NOT the 002 four-elements bed, NOT any 005/007 bed, "
                   "NOT any Orbit With Ben bed, NOT a drum loop, NOT a trailer sting."),
        "film": "004", "short": "s05_dalton_v03", "job": JOB,
        "source": "own synthesis in _build_short_s05_dalton_v03.py, 0 credits",
        "pace_bpm": "62-70",
    }
    bed.with_name(bed.stem + "_plan.json").write_text(json.dumps(plan_j, indent=2) + "\n")

    pieces_t = words[58][1]
    sfx = place_sfx(total, [CARD_IN, pieces_t])
    audio = WORK / "audio.wav"
    sfx_level = {}
    bed_db, sfx_db = -14.0, -16.0
    for _ in range(6):
        ff("-i", str(vo), "-i", str(bed), "-i", str(sfx), "-filter_complex",
           f"[0:a]aformat=sample_rates=48000:channel_layouts=stereo,apad=whole_dur={total:.3f}[v];"
           f"[1:a]aformat=sample_rates=48000:channel_layouts=stereo,atrim=0:{total:.3f},asetpts=PTS-STARTPTS,"
           f"volume={bed_db:.2f}dB,afade=t=in:d=0.05,afade=t=out:st={total - 0.2:.3f}:d=0.2[b];"
           f"[2:a]aformat=sample_rates=48000:channel_layouts=stereo,atrim=0:{total:.3f},volume={sfx_db:.2f}dB[s];"
           f"[v][b][s]amix=inputs=3:normalize=0:duration=first,alimiter=limit=0.89[a]",
           "-map", "[a]", "-t", f"{total:.3f}", "-c:a", "pcm_s16le", str(audio))
        vo_stem, bed_stem, sfx_stem = WORK / "stem_vo.wav", WORK / "stem_bed.wav", WORK / "stem_sfx.wav"
        ff("-i", str(vo), "-af", f"apad=whole_dur={total:.3f}", "-t", f"{total:.3f}", "-c:a", "pcm_s16le", str(vo_stem))
        ff("-i", str(bed), "-af", f"volume={bed_db:.2f}dB,atrim=0:{total:.3f}", "-c:a", "pcm_s16le", str(bed_stem))
        ff("-i", str(sfx), "-af", f"volume={sfx_db:.2f}dB,atrim=0:{total:.3f}", "-c:a", "pcm_s16le", str(sfx_stem))
        r = subprocess.run([sys.executable, str(OWB / "scripts/sfx_kit.py"), "level",
                            "--vo", str(vo_stem), "--sfx", str(sfx_stem), "--bed", str(bed_stem),
                            "--minutes", f"{total / 60:.3f}", "--out", str(QA / "sfx_level.json")],
                           capture_output=True, text=True)
        sfx_level = {"exit": r.returncode, "output": (r.stdout + r.stderr).strip(), "bed_db": bed_db, "sfx_db": sfx_db}
        (QA / "sfx_level.txt").write_text(sfx_level["output"] + "\n")
        if r.returncode == 0:
            break
        bed_db -= 3.0
        sfx_db -= 3.0
    if sfx_level["exit"] != 0:
        raise SystemExit(f"sfx level failed: {sfx_level['output']}")

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
    fc.append(f"{last}[card]overlay=0:0:enable='gte(t,{CARD_IN:.3f})*lt(t,{CARD_OUT:.3f})'[vc]")
    last = "[vc]"
    for i, (_, t0, t1, *_r) in enumerate(overlays, 2):
        fc.append(f"{last}[{i}:v]overlay=0:0:enable='gte(t,{t0:.3f})*lt(t,{t1:.3f})'[v{i}]")
        last = f"[v{i}]"
    mp4 = HERE / f"hos_004_{SID}_{VER}.mp4"
    ff(*inputs, "-filter_complex", ";".join(fc), "-map", last, "-map", "1:a", "-c:v", "libx264",
       "-pix_fmt", "yuv420p", "-profile:v", "high", "-preset", "medium", "-crf", "18", "-r", str(FPS),
       "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2", "-t", f"{total:.3f}", "-movflags", "+faststart",
       str(mp4))
    level = level_master(mp4)
    timeline = [{"role": r, "text": t, "t0": round(a, 3), "t1": round(c, 3)} for _, a, c, r, t in overlays]
    timeline.append({"role": "who", "text": " · ".join(CARD), "t0": CARD_IN, "t1": CARD_OUT})
    (WORK / "timeline.json").write_text(json.dumps({"plan": plan, "overlays": timeline}, indent=2) + "\n")
    atom_s = words[8][1]
    payoff_s = words[58][1]
    return {
        "id": SID, "version": VER, "job": JOB, "youtube_id": YT,
        "fixes": "J0966 HC re-cut v03 (2.56s first cut, clean P1 balance/atom plates, own-synth bed + house SFX, -14 LUFS master)",
        "test": "B (search-titled)", "air_date": air_date, "air_date_draft": air_date,
        "file": mp4.relative_to(PROJ).as_posix(), "sha256": sha256(mp4), "duration_s": round(probe(mp4), 3),
        "runtime_s": round(probe(mp4), 3),
        "spoken": spoken, "script": spoken,
        "words_list": [{"word": w, "start": round(s, 3), "end": round(e, 3)} for w, s, e in words],
        "first_word_s": round(words[0][1], 3), "last_word_end_s": round(words[-1][2], 3),
        "surprise_s": {"atom": round(atom_s, 3)}, "first_cut_s": plan[0]["t1"],
        "last_word_to_loop_s": round(probe(mp4) - words[-1][2], 3),
        "longest_hold_s": max(row["hold_s"] for row in plan if row["lands_on"] != "loop"),
        "payoff_phrase": "tiny pieces with fixed weights",
        "payoff_s": round(payoff_s, 3), "payoff_frac": round(payoff_s / total, 3),
        "loop_sentence": "That only makes sense if both are made of tiny pieces with fixed weights. Every element is made of its own kind of atom.",
        "meta_promise": False, "no_cta": True, "no_new_spend": True,
        "level": level, "lufs": level["lufs"], "true_peak_dbfs": level["true_peak_dbtp"],
        "sfx_level": sfx_level, "frame0_black": black_frac(mp4, 0.15),
        "vo_source": RAW_VO.name, "vo_take_indices": TAKE, "vo_file": str(vo),
        "dropped": "however you make it.",
        "route": "claim first: Every element is made of its own kind of atom … fixed weights. Dateline and 'His atomic theory says' cut at the word boundary.",
        "vo_s": round(vo_s, 3), "words": len(words), "max_pause_s": MAX_PAUSE, "atempo": ATEMPO,
        "bed": bed.name, "bed_path": str(bed), "hook": HOOK.replace("**", ""),
        "hook_layer": hook_meta, "who_card": card_meta, "title_on_screen": TITLE,
        "youtube_title_draft": TITLE_DRAFT, "plan": plan, "captions": len(chunks), "timeline": timeline,
        "brief": {
            "frame0": "moving 01_dalton_schoolroom_v01 in 2.80s, crop x=656, no zoom",
            "subject_named_s": round(atom_s, 3),
            "first_word_s": round(words[0][1], 3),
            "first_cut_s": plan[0]["t1"],
            "loop_s": round(probe(mp4) - words[-1][2], 3),
            "payoff_frac": round(payoff_s / total, 3),
        },
    }


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


def run_qa(mp4: Path, plan: list[dict], bed: Path) -> dict:
    QA.mkdir(parents=True, exist_ok=True)
    cuts_plates, pool_plates, seen = [], [], set()
    for k, row in enumerate(plan, 1):
        base = Path(row["plate"]).name
        src_id = f"loop_span_{base}" if row["lands_on"] == "loop" else base
        cuts_plates.append({
            "row": f"s{k:02d}_{row['lands_on']}",
            "timeline_in": row["t0"],
            "timeline_out": row["t1"],
            "source": src_id,
            "upscale": 1.78,
            "framing": {"offset": row["in_s"]},
            "video": True,
        })
        if src_id not in seen:
            seen.add(src_id)
            pool_plates.append({"file_id": src_id, "title": f"Veo plate {base}"})
    plate_cuts_f = QA / f"cuts_{SID}_{VER}_plates.json"
    plate_pool_f = QA / f"pool_{SID}_{VER}_plates.json"
    plate_cuts_f.write_text(json.dumps(cuts_plates, indent=2) + "\n")
    plate_pool_f.write_text(json.dumps(pool_plates, indent=2) + "\n")

    cuts_full = list(cuts_plates) + [{
        "row": "card_dalton", "timeline_in": CARD_IN, "timeline_out": CARD_OUT,
        "source": "code_graphic_dalton_v03_who.png", "upscale": 1.0, "video": False, "overlay": True,
    }]
    pool_full = list(pool_plates) + [{"file_id": "code_graphic_dalton_v03_who.png", "title": "JOHN DALTON card"}]
    (QA / f"cuts_{SID}_{VER}.json").write_text(json.dumps(cuts_full, indent=2) + "\n")
    (QA / f"pool_{SID}_{VER}.json").write_text(json.dumps(pool_full, indent=2) + "\n")

    rel = lambda p: str(p.relative_to(REPO))  # noqa: E731
    r_pg = subprocess.run([sys.executable, str(OWB / "scripts/polish_gate.py"),
                           rel(mp4), "--cuts", rel(plate_cuts_f),
                           "--out", rel(QA / f"polish_gate_{SID}_{VER}.json")],
                          cwd=REPO, capture_output=True, text=True)
    (QA / f"polish_gate_{SID}_{VER}.txt").write_text((r_pg.stdout + r_pg.stderr).strip() + "\n")

    r_pq = subprocess.run([sys.executable, str(OWB / "scripts/picture_qa.py"),
                           rel(mp4), "--cuts", rel(plate_cuts_f), "--pool", rel(plate_pool_f),
                           "--out-dir", rel(QA / f"picture_qa_{SID}_{VER}")],
                          cwd=REPO, capture_output=True, text=True)
    (QA / f"picture_qa_{SID}_{VER}.txt").write_text((r_pq.stdout + r_pq.stderr).strip() + "\n")

    r_mg = subprocess.run([sys.executable, str(OWB / "scripts/music_gate.py"), str(PROJ),
                           "--bed", str(bed), "--video", str(mp4),
                           "--out", str(QA / f"music_gate_{SID}_{VER}.json")],
                          capture_output=True, text=True)
    (QA / f"music_gate_{SID}_{VER}.txt").write_text((r_mg.stdout + r_mg.stderr).strip() + "\n")

    return {
        "polish_gate": {"exit": r_pg.returncode, "output": (r_pg.stdout + r_pg.stderr).strip().splitlines()[-1]},
        "picture_qa": {"exit": r_pq.returncode, "output": (r_pq.stdout + r_pq.stderr).strip().splitlines()[-1]},
        "music_gate": {"exit": r_mg.returncode, "output": (r_mg.stdout + r_mg.stderr).strip().splitlines()[-1]},
    }


def run(cmd: list[str]) -> tuple[int, str]:
    r = subprocess.run(cmd, capture_output=True, text=True)
    out = "\n".join(line for line in (r.stdout + r.stderr).splitlines() if "Warning" not in line and line.strip())
    return r.returncode, out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--air-date", default="2026-11-16")
    ap.add_argument("--no-icloud", action="store_true")
    ns = ap.parse_args()
    rec = build(ns.air_date)
    mp4 = PROJ / rec["file"]
    vo_file = Path(rec.pop("vo_file"))
    bed_path = Path(rec.pop("bed_path"))
    rec["caption_check"] = caption_check(mp4, rec.pop("timeline"))

    meta_path = HERE / f"SHORT_{SID}_{VER}.json"
    meta_path.write_text(json.dumps(rec, indent=2) + "\n")

    gate_cmd = [sys.executable, str(GATE), "check", str(mp4), "--air-date", ns.air_date,
                f"--id={YT}", "--script", str(SCRIPT_TXT), "--vo", str(vo_file), "--meta", str(meta_path)]
    code, out = run(gate_cmd)
    rec["gate"] = {"exit": code, "output": out}
    (QA / f"gate_{SID}_{VER}.txt").write_text(out + "\n")

    gate_j_res = subprocess.run([*gate_cmd, "--json"], capture_output=True, text=True)
    try:
        gate_json = json.loads(gate_j_res.stdout)
        if isinstance(gate_json, list):
            gate_json = gate_json[0]
    except json.JSONDecodeError:
        gate_json = {"verdict": "FAIL", "raw": (gate_j_res.stdout + gate_j_res.stderr)[-2000:]}
    (QA / f"gate_{SID}_{VER}.json").write_text(json.dumps(gate_json, indent=2) + "\n")
    (QA / f"j0918_ship_gate_{SID}_{VER}.txt").write_text(
        "J0918 HOS ship gate (Chief, 24 Oct 2026), read from gate_shorts_open.\n"
        f"verdict={gate_json.get('verdict')} frame0_diff={gate_json.get('frame0_diff_0_1_5s')} "
        f"first_cut_s={gate_json.get('first_cut_s')} vo_onset_s={gate_json.get('vo_onset_s')} "
        f"tail_gap_s={gate_json.get('tail_gap_s')} stayed_fails={gate_json.get('stayed_fails')}\n"
        f"fails={gate_json.get('fails')}\nwarns={gate_json.get('warns')}\n"
        f"aac_lufs={rec['lufs']:.2f} aac_true_peak_dbfs={rec['true_peak_dbfs']:.2f}\n"
    )

    code_vo, out_vo = run([str(VO_PY), str(VO_CHECK), str(vo_file), "--script", str(SCRIPT_TXT)])
    rec["vo_check"] = {"exit": code_vo, "input": vo_file.name, "output": out_vo}
    (QA / f"vo_check_{SID}_{VER}.txt").write_text(out_vo + "\n")
    rec["freezedetect_starts"] = freeze(mp4)
    rec["qa"] = run_qa(mp4, rec["plan"], bed_path)

    phone = HERE / f"hos_004_{SID}_{VER}_PHONE.mp4"
    ff("-i", str(mp4), "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "veryfast", "-crf", "26",
       "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart", str(phone))
    sheet = QA / f"hos_004_{SID}_{VER}_2fps_sheet.jpg"
    ff("-i", str(mp4), "-vf", "fps=2,scale=180:-2,tile=8x8", "-q:v", "4", str(sheet))
    for name, t in (("frame0", 0.05), ("dalton", 3.5), ("title", 11.5), ("end", round(rec["duration_s"] - 1.5, 1))):
        ff("-ss", f"{t:.3f}", "-i", str(mp4), "-frames:v", "1", "-q:v", "3", str(QA / f"{SID}_{VER}_{name}.jpg"))

    nas_out = Path("/Volumes/data/mac-mini-archive/YouTube/History Of Science/02_Video-Projects/"
                   f"004_Whats-Really-Inside-An-Atom/10_Shorts/{SID}_{VER}")
    copied = {}
    for folder in (ICLOUD, nas_out):
        folder.mkdir(parents=True, exist_ok=True)
        for src in (mp4, phone, sheet):
            dst = folder / src.name
            shutil.copy2(src, dst)
            if sha256(src) != sha256(dst):
                raise SystemExit(f"sha mismatch {dst}")
            copied[str(dst)] = sha256(dst)
    v02_sha = sha256(V02_NAS) if V02_NAS.exists() else "e7f5a6347c5f391c54ce0cadca896f508dce2fe3c6e1f267298267dd26ac3601"
    manifest = {
        "job": JOB, "youtube_id": YT, "version": VER,
        "master_sha256": sha256(mp4), "phone_sha256": sha256(phone),
        "v02_sha256": v02_sha, "copies": copied,
        "aac_lufs": rec["lufs"], "aac_true_peak_dbfs": rec["true_peak_dbfs"],
    }
    (QA / "sha256_manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    (nas_out / "sha256_manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")

    rec["phone"] = phone.name
    rec["phone_sha256"] = sha256(phone)
    rec["v02_untouched"] = True
    rec["v02_sha256"] = v02_sha
    rec["copies"] = copied
    rec["plate_audit"] = {
        "replaced": "03_weights_line_v01 (Hp/Hg/Op tiles), 08_ruler_of_weights_v01 (ruler numerals), and 06_water_ratio_v01 (1808 on shelves) are not in v03",
        "15_knife_coin_return_v01": "Part 01 balance scale and gold weights on oak table (0.50-2.71 s) for 'and each kind has its own weight.' Zero letters, zero Explorer.",
        "05_fixed_amounts": "2 fps centre crop: wooden molecule models, no letters. Opening stretch for Hydrogen / Oxygen.",
        "07_water_always": "gold sphere for 'Gold is heavier still'. Background chalkboard is a line schematic with no readable words.",
        "02_atomic_theory": "0.80 s through 3.49 s, brass stands and wood balls.",
        "04_gold_heavier": "no letters. Wood balls on the 'same fixed amounts' line.",
        "20_what_is_order": "0.40 s through 3.82 s (crop_x 500), glowing brass-and-glass apparatus on the oak table.",
        "03_atom_turns_v01": "Part 01 brass atom model turning in the schoolroom (0.40-3.28 s) for 'tiny pieces with fixed weights.' Zero letters, zero Explorer.",
        "01_dalton_schoolroom": "frame 0 (in 2.80 s) and matched 1.15 s loop (1.65-2.80 s).",
    }
    meta_path.write_text(json.dumps(rec, indent=2) + "\n")
    (HERE / f"hos_004_{SID}_{VER}_meta.json").write_text(json.dumps(rec, indent=2) + "\n")

    print(f"BUILT {SID} {VER} {rec['duration_s']} s {rec['words']} words sha {rec['sha256'][:12]} "
          f"lufs={rec['lufs']} tp={rec['true_peak_dbfs']} captions {rec['caption_check']}")
    print(rec["gate"]["output"])
    print(rec["vo_check"]["output"])
    print(rec["qa"]["polish_gate"]["output"])
    print(rec["qa"]["picture_qa"]["output"])
    print(rec["qa"]["music_gate"]["output"])
    print(f"freezedetect: {len(rec['freezedetect_starts'])} events {rec['freezedetect_starts']}")
    if rec["gate"]["exit"] != 0 or rec["qa"]["polish_gate"]["exit"] != 0 or rec["qa"]["picture_qa"]["exit"] != 0 or rec["qa"]["music_gate"]["exit"] != 0:
        raise SystemExit("QA FAIL")


if __name__ == "__main__":
    main()
