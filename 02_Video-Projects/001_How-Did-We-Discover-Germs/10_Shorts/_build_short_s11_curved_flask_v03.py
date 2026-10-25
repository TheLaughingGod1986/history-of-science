#!/usr/bin/env python3
"""HOS 001 Short s11 v03 (J0934, £0 local re-cut of 1-BZaFIMwYU).

Drops the rhetorical opener and opens on a splice of words already in
02_Voiceover/part04_proof_in_a_flask_v01.wav:
  "a flask" (4.10–4.74 s) + "stays clear." (16.18–17.04 s)
so flask and stays/clear land inside 0.06–1.50 s. Same file, so level and
room tone match. No new TTS, Veo, Flow or Vertex.

Picture: 01_question_mark_flask_v17.mp4 at frame 0 (in 1.60 s). First cut
about 2.45 s. The old 4.73 s hold is two plates, 03_dust_in_the_curve_v23
and 11_result_returns_v01, each about 2.4 s. No "watch the full film" overlay.
Loop is 1.0 s of the frame-0 plate, ending on the frame-0 frame.

    python3 _build_short_s11_curved_flask_v03.py
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

from PIL import Image, ImageDraw, ImageFont, ImageFilter  # noqa: E402

HERE = Path(__file__).resolve().parent
PROJ = HERE.parent
REPO = PROJ.parents[1]
NAS_PROJ = Path("/Volumes/data/mac-mini-archive/YouTube/History Of Science/"
                "02_Video-Projects/001_How-Did-We-Discover-Germs")
OWB = Path("/Users/benjaminoats/YouTube/orbit-with-ben")
SID, VER, JOB = "s11_curved_flask", "v03", "J0934"
AIR = "2026-10-27"
YT_ID = "1-BZaFIMwYU"
WORK = HERE / f"_work_{SID}_{VER}"
QA = HERE / f"qa_{SID}_{VER}"
W, H, FPS = 1080, 1920, 30
LOOP_S = 1.0
HOOK = "FLASK **STAYS**"
CARD = ("LOUIS PASTEUR", "Swan-neck flask, 1860s")
CARD_IN, CARD_OUT, CARD_FADE = 2.20, 5.90, 0.35
TITLE = "How Did We Discover Germs?"
TITLE_IN, TITLE_OUT = 9.0, 14.0
FONT = "/System/Library/Fonts/Supplemental/Didot.ttc"
CTA_FONT = "/System/Library/Fonts/Supplemental/Times New Roman.ttf"
CREAM, INK, YEL = (245, 232, 210, 255), (28, 26, 28, 255), (255, 214, 70, 255)
BAND_TOP, BAND_H = (H - 608) // 2, 608
# In 1.80 s, crop x=720: the centre band of this plate moves enough to clear the
# stayed gate (crop 640 at 1.60 s measured 1.48, under the 1.50 floor). Black ~19%.
FLASK_IN = 1.80
FLASK_CROP = 720
# Playback order. Times are in the Part 04 wav. The last line loops into line 1:
# "Keep the swan neck intact. A flask stays clear."
SPANS = [
    (4.10, 4.74),     # a flask
    (16.18, 17.04),   # stays clear.
    (6.72, 8.24),     # Boil broth.
    (10.62, 15.06),   # Air can drift — but dust and microbes settle in the curve.
    (37.55, 40.88),   # If life arrives as passengers from the outside,
    (54.78, 58.82),   # emptiness that stays empty — until contact.
    (17.24, 22.66),   # Break the neck, or tip the trap, and life blooms into cloudiness.
    (8.28, 10.50),    # Keep the swan neck intact.
]
PLATE = "04_Generated-Clips/part04/raw/v01_fast_probe"


def resolve_media(rel: str) -> Path:
    local = PROJ / rel
    if local.exists() and local.stat().st_size > 1000:
        return local
    alt = NAS_PROJ / rel
    if alt.exists():
        return alt
    return local


RAW_VO = resolve_media("02_Voiceover/part04_proof_in_a_flask_v01.wav")
ALIGN = resolve_media("02_Voiceover/part04_proof_in_a_flask_v01_align.json")


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


def mean_db(p: Path) -> float:
    err = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(p), "-af", "volumedetect", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    return float(re.search(r"mean_volume: (-?[\d.]+)", err).group(1))


def integrated_lufs(p: Path) -> float:
    err = subprocess.run(["ffmpeg", "-nostats", "-hide_banner", "-i", str(p), "-af", "ebur128", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    m = re.search(r"Integrated loudness:\s+I:\s+(-?[\d.]+) LUFS", err)
    if not m:
        raise SystemExit(f"no LUFS for {p.name}\n{err[-400:]}")
    return float(m.group(1))


def true_peak(p: Path) -> float:
    err = subprocess.run(["ffmpeg", "-nostats", "-hide_banner", "-i", str(p), "-af", "ebur128=peak=true", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    m = re.search(r"Peak:\s+(-?[\d.]+) dBFS", err)
    return float(m.group(1)) if m else 0.0


def words_in_align() -> list[tuple[str, float, float]]:
    d = json.loads(ALIGN.read_text())
    words, cur, t0, t1 = [], "", 0.0, 0.0
    for ch, a, b in zip(d["characters"], d["character_start_times_seconds"], d["character_end_times_seconds"]):
        if ch.isspace():
            if cur:
                words.append((cur, t0, t1))
            cur = ""
        else:
            if not cur:
                t0 = a
            cur += ch
            if ch not in ".,;:?!”\"'":
                t1 = b
    if cur:
        words.append((cur, t0, t1))
    return [(w, a, b) for w, a, b in words if w.strip("—–-")]


def lifted_vo(work: Path) -> tuple[Path, list[tuple[str, float, float]], list[dict]]:
    """Concat the spans in playback order. Per-span gain matches the opener's mean level."""
    src_words = words_in_align()
    bits = []
    for i, (a, b) in enumerate(SPANS):
        bit = work / f"span_{i:02d}.wav"
        ff("-ss", f"{a:.3f}", "-t", f"{b - a:.3f}", "-i", str(RAW_VO), "-ac", "2", "-ar", "48000",
           "-c:a", "pcm_s16le", str(bit))
        bits.append(bit)
    ref = mean_db(bits[0])
    gains = []
    leveled = []
    for i, bit in enumerate(bits):
        g = ref - mean_db(bit)
        g = max(-3.0, min(3.0, g))
        gains.append(round(g, 2))
        out = work / f"span_{i:02d}_g.wav"
        ff("-i", str(bit), "-af", f"volume={g:.2f}dB,afade=t=in:d=0.008,afade=t=out:st={max(0.02, probe(bit) - 0.012):.3f}:d=0.008",
           "-c:a", "pcm_s16le", str(out))
        leveled.append(out)
    lst = work / "vo_list.txt"
    lst.write_text("".join(f"file '{p.name}'\n" for p in leveled))
    speech = work / f"hos_001_{SID}_vo_{VER}.wav"
    ff("-f", "concat", "-safe", "0", "-i", "vo_list.txt", "-c:a", "pcm_s16le", str(speech), cwd=work)

    mapped: list[tuple[str, float, float]] = []
    cursor = 0.0
    span_meta = []
    for i, ((a, b), bit) in enumerate(zip(SPANS, leveled)):
        dur = probe(bit)
        picked = [(w, s, e) for w, s, e in src_words if a - 0.03 <= s < b - 0.04]
        for w, s, e in picked:
            mapped.append((w, round(cursor + (s - a), 3), round(cursor + (e - a), 3)))
        span_meta.append({"i": i, "src": [a, b], "out": round(cursor, 3), "dur": round(dur, 3),
                          "gain_db": gains[i], "words": " ".join(w for w, _, _ in picked)})
        cursor += dur
    return speech, mapped, span_meta


def chunk_words(words: list[tuple[str, float, float]]) -> list[dict]:
    chunks, i, n = [], 0, len(words)
    while i < n:
        t0 = words[i][1]
        parts, t_end, j = [words[i][0]], words[i][2], i + 1
        while j < n:
            wj, sj, ej = words[j]
            if parts[-1][-1:] in ".?!":
                break
            if ej - t0 >= 1.55 and len(parts) >= 2:
                break
            if len(parts) >= 5 and sj - t0 >= 0.45:
                break
            parts.append(wj)
            t_end = ej
            j += 1
        t1 = words[j][1] if j < n else t_end + 0.12
        chunks.append({"text": " ".join(parts), "t0": round(t0, 3), "t1": round(min(t1, t_end + 0.12), 3)})
        i = j
    # Exclusive handovers: each chunk ends where the next starts.
    for k in range(len(chunks) - 1):
        chunks[k]["t1"] = chunks[k + 1]["t0"]
    return chunks


def render_text(path: Path, text: str, size: int, y: int, *, anchor: str = "top", font_path: str = FONT,
                index: int = 0, stroke: int = 3) -> None:
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
            draw.text((x, cy), t, font=font, fill=YEL if hot else CREAM, stroke_width=stroke, stroke_fill=INK)
            x += font.getlength(t) + space
        cy += lh + gap
    img.save(path)


def render_hook(path: Path) -> dict:
    tokens = [(w.strip("*"), w.startswith("**")) for w in HOOK.split()]
    size = 60
    while True:
        font = ImageFont.truetype(FONT, size, index=2)
        cap = -font.getbbox("H", anchor="ls")[1]
        if cap >= 0.086 * H:
            break
        size += 1
    widest = max(font.getlength(t) for t, _ in tokens)
    if widest > W - 80:
        raise SystemExit(f"hook too wide ({widest:.0f}px)")
    pitch = round(cap * 1.28)
    block = pitch * (len(tokens) - 1) + cap
    # Above the stayed-gate centre band (y < 0.28 H), so the hook does not freeze that band.
    top = int(0.025 * H)
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    for k, (t, hot) in enumerate(tokens):
        base = top + cap + k * pitch
        draw.text((W / 2, base), t, font=font, anchor="ms", fill=YEL if hot else CREAM,
                  stroke_width=6, stroke_fill=INK)
    img.save(path)
    if top + block > 0.27 * H:
        raise SystemExit(f"hook ends at {(top + block) / H:.1%}, inside the stayed-gate centre band")
    return {"font_size": size, "cap_pct": round(100 * cap / H, 2),
            "block_pct": [round(100 * top / H, 1), round(100 * (top + block) / H, 1)]}


def render_card(path: Path) -> None:
    size1 = int(BAND_H * 0.11)
    size2 = int(BAND_H * 0.075)
    f1 = ImageFont.truetype(FONT, size1, index=2)
    f2 = ImageFont.truetype(CTA_FONT, size2)
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    x = 70
    y2 = BAND_TOP + BAND_H - 40
    y1 = y2 - size2 - 18
    shade = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shade)
    top, bot = y1 - size1 - 30, BAND_TOP + BAND_H + 80
    for yy in range(top, bot):
        ramp = min(1.0, (yy - top) / 120, (bot - yy) / 120)
        a = int(140 * 0.5 * (1 - math.cos(math.pi * ramp)))
        sd.line([(0, yy), (W, yy)], fill=(0, 0, 0, a))
    img = Image.alpha_composite(img, shade)
    d = ImageDraw.Draw(img)
    d.text((x, y1), CARD[0], font=f1, anchor="ls", fill=YEL, stroke_width=4, stroke_fill=INK)
    d.text((x, y2), CARD[1], font=f2, anchor="ls", fill=CREAM, stroke_width=3, stroke_fill=INK)
    img.save(path)


def plate(name: str) -> Path:
    p = resolve_media(f"{PLATE}/{name}.mp4")
    if not p.exists():
        raise SystemExit(f"missing plate {p}")
    return p


def seg(src: Path, dst: Path, start: float, dur: float, x: int) -> None:
    if start < 0:
        raise SystemExit(f"{src.name}: negative in-point {start}")
    if start + dur > probe(src) - 0.04:
        raise SystemExit(f"{src.name}: in {start} + {dur:.2f} runs past the plate ({probe(src):.2f})")
    vf = (f"trim=start={start:.4f}:duration={dur:.4f},setpts=PTS-STARTPTS,"
          f"scale=1920:1080,crop=608:1080:{x}:0,scale={W}:{H}:flags=lanczos,fps={FPS},setsar=1")
    ff("-i", str(src), "-filter_complex", vf, "-an", "-c:v", "libx264", "-pix_fmt", "yuv420p",
       "-preset", "fast", "-crf", "16", "-r", str(FPS), str(dst))


def body_cuts(vo_s: float) -> list[tuple[float, float, Path, float, int, str]]:
    """(t0, t1, plate, in_s, crop_x, label). First cut at 2.45 s. Dust and result ~2.4 s."""
    flask = plate("01_question_mark_flask_v17")
    rows = [
        ("flask", flask, FLASK_IN, FLASK_CROP),
        ("boil", plate("02_boil_broth_v04"), 0.45, 480),
        ("dust", plate("03_dust_in_the_curve_v23"), 0.40, 640),
        ("passengers", plate("08_passengers_v20"), 0.35, 380),
        ("clear", plate("04_still_clear_v21"), 0.45, 640),
        ("tip", plate("05_tip_the_trap_v17"), 0.40, 600),
        ("bloom", plate("07_bloom_cloud_v13"), 0.40, 500),
        ("result", plate("11_result_returns_v01"), 0.50, 560),
        ("sceptics", plate("09_sceptics_watch_v17"), 0.40, 420),
    ]
    # Fixed first cut, then the rest share the body. Dust and result stay near 2.4 s.
    holds = [2.45, 2.55, 2.40, 2.70, 2.70, 2.65, 2.55, 2.40]
    used = sum(holds)
    tail = vo_s - used
    if tail < 1.6:
        raise SystemExit(f"body tail {tail:.2f}s too short (vo {vo_s:.2f}); widen a span")
    if tail > 3.9:
        raise SystemExit(f"body tail {tail:.2f}s over 3.9s (vo {vo_s:.2f})")
    holds.append(tail)
    out = []
    t = 0.0
    for (label, src, ins, x), d in zip(rows, holds):
        out.append((round(t, 3), round(t + d, 3), src, ins, x, label))
        t += d
    n_loop = round(LOOP_S * FPS)
    loop_in = FLASK_IN - (n_loop - 1) / FPS
    out.append((round(vo_s, 3), round(vo_s + LOOP_S, 3), flask, loop_in, FLASK_CROP, "loop"))
    return out


def synth_bed(path: Path, dur: float, sr: int = 48000) -> None:
    """Own pad, D-leaning partials, slow 72 BPM swell. Not the v02 F-major bed."""
    n = int(sr * dur)
    freqs = [98.0, 155.56, 246.94, 311.13, 415.30]
    amps = [0.34, 0.26, 0.18, 0.12, 0.08]
    frames = bytearray()
    for i in range(n):
        t = i / sr
        pulse = 0.82 + 0.18 * math.sin(2 * math.pi * (72 / 60) * t)
        env = min(1.0, t / 0.35) * min(1.0, max(0.0, (dur - t) / 0.30))
        l = r = 0.0
        for k, (f, a) in enumerate(zip(freqs, amps)):
            l += math.sin(2 * math.pi * f * t + 0.4 * k) * a
            r += math.sin(2 * math.pi * (f * 1.0015) * t + 0.7 * k) * a
        g = env * pulse * 0.22
        frames += struct.pack("<hh", int(max(-1, min(1, l * g)) * 32767), int(max(-1, min(1, r * g)) * 32767))
    with wave.open(str(path), "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(sr)
        w.writeframes(bytes(frames))


def place_sfx(work: Path, total: float) -> Path:
    kit = PROJ / "06_Sound-Effects" / "kit_v01"
    if not (kit / "sfx_hos_whoosh_soft_v01.wav").exists():
        subprocess.run([sys.executable, str(OWB / "scripts/sfx_kit.py"), "make", "--out-dir", str(kit),
                        "--house", "hos"], check=True)
    whoosh = kit / "sfx_hos_whoosh_soft_v01.wav"
    tick = kit / "sfx_hos_tick_ink_v01.wav"
    dst = work / "sfx_stem.wav"
    # Whoosh at frame 0, one ink tick as the Pasteur card arrives. Quiet; the level gate sets the gain.
    ff("-f", "lavfi", "-t", f"{total:.3f}", "-i", "anullsrc=channel_layout=stereo:sample_rate=48000",
       "-i", str(whoosh), "-i", str(tick),
       "-filter_complex",
       "[1:a]volume=-16dB,afade=t=out:st=0.75:d=0.2[w];"
       "[2:a]volume=-10dB,adelay=2200|2200[t];"
       "[0:a][w][t]amix=inputs=3:normalize=0:duration=first,alimiter=limit=0.5[a]",
       "-map", "[a]", "-c:a", "pcm_s16le", str(dst))
    return dst


def mix(vo: Path, bed: Path, sfx: Path, total: float, dst: Path, bed_db: float, sfx_db: float) -> None:
    ff("-i", str(vo), "-i", str(bed), "-i", str(sfx), "-filter_complex",
       f"[0:a]aformat=sample_rates=48000:channel_layouts=stereo,apad=whole_dur={total:.3f}[v];"
       f"[1:a]aformat=sample_rates=48000:channel_layouts=stereo,atrim=0:{total:.3f},volume={bed_db:.2f}dB[b];"
       f"[2:a]aformat=sample_rates=48000:channel_layouts=stereo,atrim=0:{total:.3f},volume={sfx_db:.2f}dB[s];"
       f"[v][b][s]amix=inputs=3:normalize=0:duration=first,alimiter=limit=0.9[a]",
       "-map", "[a]", "-t", f"{total:.3f}", "-c:a", "pcm_s16le", str(dst))


def force_last_frame(pic: Path, total: float) -> None:
    """Last picture frame becomes the frame-0 picture, so the loop seam matches."""
    frame0 = WORK / "frame0_pic.png"
    ff("-i", str(pic), "-frames:v", "1", str(frame0))
    n = int(round(total * FPS))
    tmp = WORK / "picture_matched.mp4"
    ff("-i", str(pic), "-i", str(frame0), "-filter_complex",
       f"[1:v]scale={W}:{H},fps={FPS},format=yuv420p[f];"
       f"[0:v][f]overlay=enable='eq(n,{n - 1})'[v]",
       "-map", "[v]", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "fast", "-crf", "16",
       "-r", str(FPS), "-t", f"{total:.3f}", str(tmp))
    tmp.replace(pic)


def loop_diff(mp4: Path) -> float:
    """Mean abs luma diff, last frame vs frame 0, with hook/caption/card text masked."""
    a = WORK / "diff_a.png"
    b = WORK / "diff_b.png"
    ff("-i", str(mp4), "-frames:v", "1", str(a))
    ff("-sseof", "-0.05", "-i", str(mp4), "-frames:v", "1", str(b))
    im_a = Image.open(a).convert("RGB")
    im_b = Image.open(b).convert("RGB").resize(im_a.size)
    im_b.save(b)
    # Text mask: pixels on frame 0 that are cream or yellow and differ from the last frame.
    pa, pb = im_a.load(), im_b.load()
    w, h = im_a.size
    mask = Image.new("L", (w, h), 0)
    mpix = mask.load()
    for y in range(h):
        for x in range(w):
            r, g, bl = pa[x, y]
            r2, g2, b2 = pb[x, y]
            cream = r > 200 and g > 185 and bl > 150 and abs(r - g) < 50
            ink = r < 40 and g < 40 and bl < 40
            differ = abs(r - r2) + abs(g - g2) + abs(bl - b2) > 80
            if differ and (cream or ink):
                mpix[x, y] = 255
    mask = mask.filter(ImageFilter.MaxFilter(5))
    mpix = mask.load()
    acc = n = 0
    for y in range(0, h, 2):
        for x in range(0, w, 2):
            if mpix[x, y]:
                continue
            r, g, bl = pa[x, y]
            r2, g2, b2 = pb[x, y]
            la = 0.2126 * r + 0.7152 * g + 0.0722 * bl
            lb = 0.2126 * r2 + 0.7152 * g2 + 0.0722 * b2
            acc += abs(la - lb)
            n += 1
    return round(acc / max(1, n), 2)


def black_frac(mp4: Path, t: float) -> float:
    raw = subprocess.check_output(["ffmpeg", "-v", "error", "-ss", f"{t:.3f}", "-i", str(mp4),
                                   "-frames:v", "1", "-vf", "scale=160:284", "-f", "rawvideo", "-pix_fmt", "gray", "-"])
    dark = sum(1 for p in raw if p < 18)
    return round(dark / max(1, len(raw)), 3)


def synth_and_gates(vo: Path, total: float) -> dict:
    bed = PROJ / "05_Music" / f"hos_001_{SID}_{VER}_bed.wav"
    bed.parent.mkdir(parents=True, exist_ok=True)
    synth_bed(bed, total + 0.2)
    plan = {
        "prompt": ("Quiet laboratory pad under a spoken demonstration, slow and even, no chase. "
                   "Pace: 68-78 BPM. NOT a trailer sting, NOT a piano solo, NOT the F-major flask pad "
                   "from s11 v02, NOT any Orbit With Ben bed, NOT a drum loop."),
        "film": "001",
        "short": f"{SID}_{VER}",
        "job": JOB,
        "source": "own synthesis in _build_short_s11_curved_flask_v03.py, 0 credits",
    }
    bed.with_name(bed.stem + "_plan.json").write_text(json.dumps(plan, indent=2) + "\n")
    sfx = place_sfx(WORK, total)
    vo_i = integrated_lufs(vo)
    # Start well under the VO. The level gate reads these stems, not the loudnormed mix.
    bed_db, sfx_db = -8.0, -8.0
    audio = WORK / "audio.wav"
    level = {}
    for _ in range(4):
        mix(vo, bed, sfx, total, audio, bed_db, sfx_db)
        # Stems at the same gain the mix uses, padded to the cut, so the gate's clocks line up.
        vo_stem = WORK / "stem_vo.wav"
        bed_stem = WORK / "stem_bed.wav"
        sfx_stem = WORK / "stem_sfx.wav"
        ff("-i", str(vo), "-af", f"apad=whole_dur={total:.3f}", "-t", f"{total:.3f}", "-c:a", "pcm_s16le", str(vo_stem))
        ff("-i", str(bed), "-af", f"volume={bed_db:.2f}dB,atrim=0:{total:.3f}", "-c:a", "pcm_s16le", str(bed_stem))
        ff("-i", str(sfx), "-af", f"volume={sfx_db:.2f}dB,atrim=0:{total:.3f}", "-c:a", "pcm_s16le", str(sfx_stem))
        r = subprocess.run([sys.executable, str(OWB / "scripts/sfx_kit.py"), "level",
                            "--vo", str(vo_stem), "--sfx", str(sfx_stem), "--bed", str(bed_stem),
                            "--minutes", f"{total / 60:.3f}", "--out", str(QA / "sfx_level.json")],
                           capture_output=True, text=True)
        level = {"exit": r.returncode, "output": (r.stdout + r.stderr).strip(), "bed_db": bed_db, "sfx_db": sfx_db}
        if r.returncode == 0:
            break
        bed_db -= 3.0
        sfx_db -= 3.0
    return {"audio": audio, "bed": bed, "level": level, "vo_i": vo_i}


def run_qa(mp4: Path, plan: list[dict]) -> dict:
    QA.mkdir(parents=True, exist_ok=True)
    cuts, pool, seen = [], [], set()
    for k, row in enumerate(plan, 1):
        base = Path(row["plate"]).name
        src_id = f"loop_end_{base}" if row["label"] == "loop" else base
        cuts.append({"row": f"s{k:02d}_{row['label']}", "timeline_in": row["t0"], "timeline_out": row["t1"],
                     "source": src_id, "upscale": round(1080 / 608, 3), "video": True,
                     "framing": {"offset": row["in_s"]}})
        if src_id not in seen:
            seen.add(src_id)
            pool.append({"file_id": src_id, "title": f"Flow Veo plate {base}"})
    cuts_f = QA / f"cuts_{SID}_{VER}.json"
    pool_f = QA / f"pool_{SID}_{VER}.json"
    cuts_f.write_text(json.dumps(cuts, indent=2) + "\n")
    pool_f.write_text(json.dumps(pool, indent=2) + "\n")
    rel = lambda p: str(p.relative_to(REPO))  # noqa: E731
    r_pg = subprocess.run([sys.executable, str(OWB / "scripts/polish_gate.py"), rel(mp4),
                           "--cuts", rel(cuts_f), "--out", rel(QA / f"polish_gate_{SID}_{VER}.json")],
                          cwd=REPO, capture_output=True, text=True)
    (QA / f"polish_gate_{SID}_{VER}.txt").write_text((r_pg.stdout + r_pg.stderr).strip() + "\n")
    r_pq = subprocess.run([sys.executable, str(OWB / "scripts/picture_qa.py"), rel(mp4),
                           "--cuts", rel(cuts_f), "--pool", rel(pool_f),
                           "--out-dir", rel(QA / f"picture_qa_{SID}_{VER}")],
                          cwd=REPO, capture_output=True, text=True)
    (QA / f"picture_qa_{SID}_{VER}.txt").write_text((r_pq.stdout + r_pq.stderr).strip() + "\n")
    return {"polish_gate": {"exit": r_pg.returncode, "tail": (r_pg.stdout + r_pg.stderr).strip().splitlines()[-3:]},
            "picture_qa": {"exit": r_pq.returncode, "tail": (r_pq.stdout + r_pq.stderr).strip().splitlines()[-5:]}}


def sheet_2fps(mp4: Path) -> Path:
    out = QA / f"{mp4.stem}_2fps_sheet.jpg"
    ff("-i", str(mp4), "-vf", "fps=2,scale=180:-2,tile=8x6", "-q:v", "4", str(out))
    return out


def copy_out(mp4: Path, phone: Path, sheet: Path) -> dict:
    uat = Path.home() / "Library/Mobile Documents/com~apple~CloudDocs/HOS UAT/001_How-Did-We-Discover-Germs/10_Shorts"
    nas = NAS_PROJ / "10_Shorts" / f"{SID}_{VER}"
    copied = []
    for folder in (uat, nas):
        if not folder.parent.exists() and folder == nas:
            continue
        folder.mkdir(parents=True, exist_ok=True)
        for src in (mp4, phone, sheet):
            shutil.copy2(src, folder / src.name)
            copied.append(str(folder / src.name))
    return {"copied": copied}


def build() -> dict:
    if WORK.exists():
        shutil.rmtree(WORK)
    WORK.mkdir(parents=True)
    QA.mkdir(parents=True, exist_ok=True)
    vo, words, span_meta = lifted_vo(WORK)
    spoken = " ".join(w for w, _, _ in words)
    (WORK / "spoken.txt").write_text(spoken + "\n")
    vo_s = probe(vo)
    total = round(vo_s + LOOP_S, 3)
    if not 18.0 <= total <= 24.05:
        raise SystemExit(f"duration {total}s outside 18–24 s (vo {vo_s:.2f})")
    # Surprise words.
    by = {w.strip(".,").lower(): (s, e) for w, s, e in words}
    flask_t = next(s for w, s, e in words if w.lower().startswith("flask"))
    clear_t = next(s for w, s, e in words if w.lower().startswith("clear"))
    stays_t = next(s for w, s, e in words if w.lower().startswith("stays"))
    if flask_t > 1.50 or clear_t > 1.50:
        raise SystemExit(f"claim late: flask {flask_t} clear {clear_t}")
    if words[0][1] > 0.15:
        raise SystemExit(f"first word at {words[0][1]}")

    cuts = body_cuts(vo_s)
    segs = []
    plan = []
    for k, (t0, t1, src, ins, x, label) in enumerate(cuts):
        d = t1 - t0
        if d > 4.01:
            raise SystemExit(f"{label} hold {d:.2f}s")
        if k == 1 and t0 > 2.60:
            raise SystemExit(f"first cut {t0}")
        out = WORK / f"seg_{k:02d}.mp4"
        seg(src, out, ins, d, x)
        segs.append(out)
        plan.append({"t0": t0, "t1": round(t1, 3), "plate": str(src), "in_s": round(ins, 4),
                     "crop_x": x, "label": label, "hold_s": round(d, 3)})
    (WORK / "pic.txt").write_text("".join(f"file '{s.name}'\n" for s in segs))
    pic = WORK / "picture.mp4"
    ff("-f", "concat", "-safe", "0", "-i", "pic.txt", "-c:v", "libx264", "-pix_fmt", "yuv420p",
       "-preset", "fast", "-crf", "16", "-r", str(FPS), "-t", f"{total:.3f}", str(pic), cwd=WORK)
    force_last_frame(pic, total)

    sound = synth_and_gates(vo, total)
    audio = sound["audio"]
    norm = WORK / "audio_norm.wav"
    ff("-i", str(audio), "-af", "loudnorm=I=-14:TP=-1.5:LRA=11", "-c:a", "pcm_s16le", str(norm))

    chunks = chunk_words(words)
    overlays = []
    hook_png = WORK / "cap_hook.png"
    hook_meta = render_hook(hook_png)
    overlays.append((hook_png, 0.0, 2.0))
    for i, c in enumerate(chunks):
        png = WORK / f"cap_{i:03d}.png"
        render_text(png, c["text"], 52, 330, anchor="bottom")
        overlays.append((png, c["t0"], min(c["t1"], total - 0.05)))
    title_png = WORK / "cap_title.png"
    render_text(title_png, TITLE, 58, 250, index=2, stroke=4)
    shade = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    for yy in range(560):
        a = int(140 * 0.5 * (1 + math.cos(math.pi * yy / 560)))
        ImageDraw.Draw(shade).line([(0, yy), (W, yy)], fill=(0, 0, 0, a))
    Image.alpha_composite(shade, Image.open(title_png)).save(title_png)
    overlays.append((title_png, TITLE_IN, min(TITLE_OUT, total - 0.2)))
    card_png = WORK / "card_who.png"
    render_card(card_png)

    inputs = ["-i", str(pic), "-i", str(norm)]
    for png, *_ in overlays:
        inputs += ["-loop", "1", "-i", str(png)]
    ci = 2 + len(overlays)
    inputs += ["-loop", "1", "-t", f"{total:.3f}", "-i", str(card_png)]
    fc = [f"[{ci}:v]format=rgba,fade=t=in:st={CARD_IN}:d={CARD_FADE}:alpha=1,"
          f"fade=t=out:st={CARD_OUT - CARD_FADE}:d={CARD_FADE}:alpha=1[card]",
          f"[0:v][card]overlay=0:0:enable='gte(t,{CARD_IN:.3f})*lt(t,{CARD_OUT:.3f})'[vc]"]
    last = "[vc]"
    for i, (_, t0, t1) in enumerate(overlays, 2):
        fc.append(f"{last}[{i}:v]overlay=0:0:enable='gte(t,{t0:.3f})*lt(t,{t1:.3f})'[v{i}]")
        last = f"[v{i}]"
    mp4 = HERE / f"hos_001_{SID}_{VER}.mp4"
    ff(*inputs, "-filter_complex", ";".join(fc), "-map", last, "-map", "1:a",
       "-c:v", "libx264", "-pix_fmt", "yuv420p", "-profile:v", "high", "-preset", "medium", "-crf", "18",
       "-r", str(FPS), "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2",
       "-t", f"{total:.3f}", "-movflags", "+faststart", str(mp4))

    lufs = integrated_lufs(mp4)
    peak = true_peak(mp4)
    diff = loop_diff(mp4)
    holds = [r["hold_s"] for r in plan if r["label"] != "loop"]
    life_t = next(s for w, s, e in words if w.lower().startswith("life") and s > 10)
    payoff = life_t
    last_end = words[-1][2]
    tail_gap = round(total - last_end, 3)
    brief = {
        "frame0_source": f"{PLATE}/01_question_mark_flask_v17.mp4",
        "frame0_zoom": "none — moving plate, in 1.80s, crop x=720, no Ken Burns",
        "first_word_s": words[0][1],
        "surprise_s": {"flask": flask_t, "stays": stays_t, "clear": clear_t},
        "first_cut_s": plan[1]["t0"],
        "last_word_to_loop_s": tail_gap,
        "meta_promise": False,
        "runtime_s": round(probe(mp4), 3),
        "longest_hold_s": max(holds),
        "payoff_phrase": "life blooms into cloudiness",
        "payoff_s": payoff,
        "payoff_frac": round(payoff / total, 3),
        "loop_sentence": "Keep the swan neck intact. A flask stays clear.",
        "loop_diff": diff,
        "lufs": lufs,
        "true_peak_dbfs": peak,
        "frame0_black": black_frac(mp4, 0.2),
    }
    meta = {
        "id": SID, "version": VER, "job": JOB, "youtube_id": YT_ID,
        "title": "What Is the Pasteur Swan Neck Flask Experiment?",
        "air_date": AIR, "spoken": spoken, "script": spoken,
        "words": [{"word": w, "start": s, "end": e} for w, s, e in words],
        "word_count": len(words), "vo_s": round(vo_s, 3), "last_word_end_s": last_end,
        "spans": span_meta, "plan": [{**r, "plate": Path(r["plate"]).name} for r in plan],
        "hook": HOOK.replace("**", ""), "hook_layer": hook_meta,
        "who_card": {"name": CARD[0], "line2": CARD[1], "in_s": CARD_IN, "out_s": CARD_OUT},
        "title_on_screen": TITLE, "no_cta": True, "no_new_spend": True,
        "bed": sound["bed"].name, "sfx_level": sound["level"],
        **brief,
    }
    meta_path = HERE / f"hos_001_{SID}_{VER}_meta.json"
    meta_path.write_text(json.dumps(meta, indent=2) + "\n")
    (HERE / f"SHORT_{SID}_{VER}.json").write_text(json.dumps(meta, indent=2) + "\n")

    gate = subprocess.run([sys.executable, str(REPO / "00_Brand/Channel-Setup/tools/gate_shorts_open.py"),
                           "check", str(mp4), "--air-date", AIR, "--id", YT_ID,
                           "--script", str(WORK / "spoken.txt"), "--vo", str(vo),
                           "--meta", str(meta_path), "--json"],
                          capture_output=True, text=True)
    (QA / f"gate_{SID}_{VER}.txt").write_text((gate.stdout + gate.stderr).strip() + "\n")
    try:
        gate_json = json.loads(gate.stdout)
        if isinstance(gate_json, list):
            gate_json = gate_json[0]
    except json.JSONDecodeError:
        gate_json = {"verdict": "FAIL", "raw": gate.stdout[-1500:], "err": gate.stderr[-800:]}
    (QA / f"gate_{SID}_{VER}.json").write_text(json.dumps(gate_json, indent=2) + "\n")

    qa = run_qa(mp4, plan)
    music = subprocess.run([sys.executable, str(OWB / "scripts/music_gate.py"), str(PROJ),
                            "--bed", str(sound["bed"]), "--video", str(mp4),
                            "--out", str(QA / f"music_gate_{SID}_{VER}.json")],
                           capture_output=True, text=True)
    (QA / f"music_gate_{SID}_{VER}.txt").write_text((music.stdout + music.stderr).strip() + "\n")

    phone = HERE / f"hos_001_{SID}_{VER}_PHONE.mp4"
    ff("-i", str(mp4), "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "fast", "-crf", "26",
       "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart", str(phone))
    sheet = sheet_2fps(mp4)
    copies = copy_out(mp4, phone, sheet)

    summary = {
        "file": mp4.name, "sha256": sha256(mp4), "duration_s": brief["runtime_s"],
        "spoken": spoken, "brief": brief, "gate_exit": gate.returncode,
        "gate_verdict": gate_json.get("verdict"), "gate_fails": gate_json.get("fails"),
        "gate_warns": gate_json.get("warns"), "qa": qa,
        "music_exit": music.returncode, "music_tail": (music.stdout + music.stderr).strip().splitlines()[-4:],
        "sfx": sound["level"], "copies": copies, "phone": phone.name,
    }
    (QA / f"build_{SID}_{VER}.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps({k: summary[k] for k in ("file", "duration_s", "gate_verdict", "gate_fails", "gate_warns",
                                              "qa", "music_exit", "music_tail", "sfx", "brief")}, indent=2))
    return summary


def main() -> None:
    argparse.ArgumentParser().parse_args()
    rec = build()
    bad = []
    if rec["gate_verdict"] != "PASS":
        bad.append("gate")
    if rec["qa"]["polish_gate"]["exit"] != 0:
        bad.append("polish")
    if rec["qa"]["picture_qa"]["exit"] != 0:
        bad.append("picture")
    if rec["music_exit"] != 0:
        bad.append("music")
    if rec["sfx"]["exit"] != 0:
        bad.append("sfx")
    if rec["brief"]["loop_diff"] > 15:
        bad.append(f"loop_diff {rec['brief']['loop_diff']}")
    if rec["brief"]["payoff_frac"] < 0.70:
        bad.append(f"payoff {rec['brief']['payoff_frac']}")
    if bad:
        raise SystemExit("NOT PASS: " + ", ".join(bad))
    print("PASS", rec["file"], rec["duration_s"], "s")


if __name__ == "__main__":
    main()
