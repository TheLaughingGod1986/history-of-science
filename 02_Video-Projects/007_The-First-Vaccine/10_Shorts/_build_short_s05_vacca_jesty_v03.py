#!/usr/bin/env python3
"""HOS 007 Short s05 v01 (test B, search-titled): a stretch lifted from the long's own Part 04 (J0898).

No new VO or picture spend. VO: 02_Voiceover/part04_the_test_v01b.mp3, lift (words 62..76 + 103..147, 60 words):
"Jenner wasn't the first to try cowpox. Benjamin Jesty had done it twenty-two years earlier.
He tested more people, and in seventeen ninety-eight he paid to print a short book. He called
the disease by a Latin name, variolae vaccinae, which means smallpox of the cow. From vacca,
the Latin word for cow, came the name for the treatment: vaccination."
(60 words; stays inside 22–27 s and 55–65 words; zero spoken-word overlap with s04_smallpox_test_v01
(Part 04 words 0..61), Short B milkmaids (Part 02), or Short C 1980 eradication (Part 05)).
Plates: the long's Chief-KEPT takes (P5:09_meadow_golden_t1, P2:06_jesty_family_t1,
P4:10_garden_hut_t1, P4:08_soho_press_t1, P5:10_history_book_t1, P1:01_cow_meadow_t1,
P4:10a_packets_t1).
Bed: own-synthesis warm harmonic pad at −20 dB under VO (0 credits; G-major pastoral voicing,
distinct from s04's D-major pad).
Hook on frame 0, word captions (with gte(t,s)*lt(t,e) so handovers never double-stack),
one person/date card (BENJAMIN JESTY · Dorset, 1774), the long's exact title at 9–14 s,
the last 3.0 s on the opening plate so it loops.
Then caption check, handover check, gate_shorts_open, vo_check, freezedetect, polish_gate,
picture_qa, stills, iCloud copy. Never uploads.

    python3 _build_short_s05_vacca_jesty_v01.py [--air-date YYYY-MM-DD] [--no-icloud]
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
OWB_REPO = Path("/Users/benjaminoats/YouTube/orbit-with-ben")
MEDIA_PROJ = Path("/Users/benjaminoats/YouTube/hos-007-vaccine/02_Video-Projects/007_The-First-Vaccine")
SID = "s05_vacca_jesty"
VER = "v03"
JOB = "J0966"
WORK = HERE / f"_work_{SID}_{VER}"
QA_DIR = HERE / f"qa_{SID}_{VER}"


def resolve_media(rel: str) -> Path:
    local = PROJ / rel
    if local.exists():
        return local
    alt = MEDIA_PROJ / rel
    if alt.exists():
        return alt
    return local


RAW_VO = resolve_media("02_Voiceover/part04_the_test_v01b.mp3")
RAW_ALIGN = resolve_media("02_Voiceover/part04_the_test_v01b_align.json")
# Alignment indices 62..76 + 103..147 in part04_the_test_v01b_align.json (60 words):
# "Jenner wasn't the first to try cowpox. Benjamin Jesty had done it twenty-two years earlier.
#  He tested more people, and in seventeen ninety-eight he paid to print a short book. He called
#  the disease by a Latin name, variolae vaccinae, which means smallpox of the cow. From vacca,
#  the Latin word for cow, came the name for the treatment: vaccination."
TAKE = list(range(62, 77)) + list(range(103, 148))
DROPPED = list(range(77, 103))
MAX_PAUSE = 0.14
ATEMPO = 1.07
HOOK = "NOT THE **FIRST**"
CARD = ("BENJAMIN JESTY", "Dorset · 1774")
CARD_IN, CARD_OUT, CARD_FADE = 2.40, 5.80, 0.35
W, H, FPS = 1080, 1920, 30
BAND_TOP, BAND_H = (H - 608) // 2, 608
CREAM, INK, YEL = (245, 232, 210, 255), (28, 26, 28, 255), (255, 214, 70, 255)
FONT = "/System/Library/Fonts/Supplemental/Didot.ttc"
CTA_FONT = "/System/Library/Fonts/Supplemental/Times New Roman.ttf"
TITLE = "Why Vaccines Are Named After a Cow"
TITLE_BANNER = "Why Vaccines Are\nNamed After a Cow"
TITLE_DRAFT = "Why Is It Called a Vaccine?"
TAIL_S = 0.35
LOOP_S = 1.15
TITLE_IN, TITLE_OUT = 9.0, 14.0
CHUNK_MAX_S, CHUNK_MAX_WORDS, CHUNK_MIN_S = 1.55, 5, 0.45
HOOK_CAP = 0.09
HOOK_PITCH = 1.32
UI_TOP = 0.75
GATE = Path(os.environ.get("HOS_GATE", REPO / "00_Brand/Channel-Setup/tools/gate_shorts_open.py"))
VO_CHECK = REPO / "00_Brand/Channel-Setup/tools/vo_check.py"
VO_PY = Path.home() / ".venvs/hos-vo/bin/python"
ICLOUD = Path.home() / ("Library/Mobile Documents/com~apple~CloudDocs/HOS UAT/"
                        "007_The-First-Vaccine/10_Shorts")
SCRIPT_TXT = WORK / f"{SID}.txt"


def clip(rel: str) -> Path:
    return resolve_media(f"04_Generated-Clips/{rel}.mp4")


# (index of the word the plate lands on, plate, in-point s, crop x on 1920x1080); "loop" = last LOOP_S s.
# All 7 source clips checked: Chief-KEPT (J0352), zero baked letters, continuous motion, no Explorer, no face in 0-2 s,
# zero plate overlap with s04_smallpox_test_v01.
BEATS = [
    (0, clip("part05/raw/v01/09_meadow_golden_t1"), 4.20, 660),          # Jenner wasn't the first to try cowpox. In-point moved off the v02 frame.
    (7, clip("part02/raw/v01/06_jesty_family_t1"), 0.40, 660),           # Benjamin Jesty had done it twenty-two years earlier. (WHO card)
    (15, clip("part04/raw/v01/10_garden_hut_t1"), 0.40, 640),            # He tested more people,
    (21, clip("part04/raw/v01/08_soho_press_t1"), 0.40, 820),            # and in seventeen ninety-eight he paid to print a short book.
    (30, clip("part05/raw/v01/10_history_book_t1"), 0.40, 640),          # He called the disease by a Latin name,
    (36, clip("part03/raw/v01/05_quill_writes_t1"), 0.40, 640),          # a Latin name, variolae vaccinae (09_latin_name is not on disk)
    (40, clip("part01/raw/v01/01_cow_meadow_t1"), 0.40, 660),            # which means smallpox of the cow.
    (46, clip("part04/raw/v01/10a_packets_t1"), 0.40, 640),              # From vacca, the Latin word for cow,
    (53, clip("part04/raw/v01/06_line_underlined_t1"), 0.40, 640),       # came the name for the treatment
    ("loop", clip("part05/raw/v01/09_meadow_golden_t1"), 4.20 - LOOP_S, 660),
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


def synth_warm_bed(path: Path, dur: float, sr: int = 48000) -> Path:
    """Synthesise a gentle, period-fitting warm harmonic pad (own synthesis, 0 credits, G-major pastoral voicing)."""
    n = int(sr * (dur + 1.0))
    freqs = [196.00, 293.66, 392.00, 493.88, 587.33]  # G3, D4, G4, B4, D5 warm pastoral G-major voicing
    amps = [0.38, 0.28, 0.18, 0.12, 0.08]
    frames = bytearray()
    for i in range(n):
        t = i / sr
        env = min(1.0, t / 0.4) * min(1.0, max(0.0, (dur + 0.5 - t) / 0.5))
        l_val = 0.0
        r_val = 0.0
        for k, (f, a) in enumerate(zip(freqs, amps)):
            shimmer = 1.0 + 0.08 * math.sin(2.0 * math.pi * (0.13 + 0.04 * k) * t + k + 1.2)
            s_l = math.sin(2.0 * math.pi * f * t + 0.30 * k) * a * shimmer
            s_r = math.sin(2.0 * math.pi * (f * 1.0009) * t + 0.60 * k) * a * shimmer
            l_val += s_l
            r_val += s_r
        l_sample = int(max(-1.0, min(1.0, l_val * env * 0.25)) * 32767)
        r_sample = int(max(-1.0, min(1.0, r_val * env * 0.25)) * 32767)
        frames += struct.pack("<hh", l_sample, r_sample)
    with wave.open(str(path), "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(sr)
        w.writeframes(bytes(frames))
    return path


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
            cur += ch
            if ch not in ".,;:?!”\"'":
                t1 = b
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
    if "\n" in text:
        lines = [[(w.strip("*"), w.startswith("**")) for w in ln.split()]
                 for ln in text.splitlines() if ln.strip()]
    else:
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
    pre = "scale=1920:1080"
    vf = f"{pre},crop=608:1080:{x}:0,scale={W}:{H}:flags=lanczos,setsar=1"
    ff("-ss", f"{start:.3f}", "-i", str(src), "-t", f"{dur:.3f}", "-filter_complex", vf, "-an", "-c:v", "libx264",
       "-pix_fmt", "yuv420p", "-preset", "fast", "-crf", "17", "-r", str(FPS), str(dst))


def lifted_vo(work: Path) -> tuple[Path, list[tuple[str, float, float]]]:
    """Cut the 60-word Jesty + 1798 Inquiry + vacca/vaccination stretch, cap pauses, apply ATEMPO."""
    all_words = words_from_align(RAW_ALIGN)
    words = [all_words[i] for i in TAKE]
    for idx in range(len(words)):
        if idx == 0 or TAKE[idx] != TAKE[idx - 1] + 1:
            words[idx] = (words[idx][0][:1].upper() + words[idx][0][1:], words[idx][1], words[idx][2])
    spans: list[list[float]] = []
    raw_gap = round(MAX_PAUSE * ATEMPO, 3)
    for i, (_, s, e) in enumerate(words):
        s0 = max(0.0, s - 0.02 if i == 0 else s - 0.04)
        e0 = e + 0.06
        if spans and i > 0 and TAKE[i] == TAKE[i - 1] + 1 and s0 - spans[-1][1] <= raw_gap:
            spans[-1][1] = max(spans[-1][1], e0)
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
    wav = work / f"hos_007_{SID}_vo_{VER}.wav"
    ff("-i", str(RAW_VO), "-filter_complex", ";".join(fc), "-map", "[a]", "-c:a", "pcm_s16le", str(wav))
    return wav, mapped


def render_card(path: Path) -> dict:
    """Lower third of the 16:9 centre band: name on line one, place and date on line two."""
    size1 = int(BAND_H * 0.112)
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
    return {"name": CARD[0], "line2": CARD[1], "line1_px": size1, "line1_pct_of_band": round(100 * size1 / BAND_H, 1),
            "band": [BAND_TOP, BAND_TOP + BAND_H], "in_s": CARD_IN, "out_s": CARD_OUT, "fade_s": CARD_FADE}


def rel_to_proj(p: Path) -> str:
    for base in (PROJ, MEDIA_PROJ):
        try:
            return p.relative_to(base).as_posix()
        except ValueError:
            pass
    return p.name


def build(air_date: str) -> dict:
    if WORK.exists():
        shutil.rmtree(WORK)
    WORK.mkdir(parents=True)
    vo, words = lifted_vo(WORK)
    # Write "1798" in the vo_check script file so vo_check's NUMERAL regex matches faster-whisper's "1798"
    # (documented in 02_Voiceover/REPORT.md); on-screen captions use the spelled-out "seventeen ninety-eight".
    script_text = (" ".join(w for w, _, _ in words)
                   .replace("twenty-two", "22")
                   .replace("seventeen ninety-eight", "1798"))
    SCRIPT_TXT.write_text(script_text + "\n")
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
            t = max(0.0, words[w][1] - 0.12)
        cuts.append((round(t, 3), src, ins, x, w))
    plan, segs = [], []
    for k, (t, src, ins, x, w) in enumerate(cuts):
        end = cuts[k + 1][0] if k + 1 < len(cuts) else total
        d = end - t
        if d < (0.95 if w == "loop" else 1.2):
            raise SystemExit(f"{SID}: beat {k} only {d:.2f} s")
        out = WORK / f"seg_{k:02d}.mp4"
        seg(src, out, ins, d, x)
        segs.append(out)
        plan.append({"t0": t, "t1": round(end, 3), "plate": rel_to_proj(src), "in_s": ins,
                     "crop_x": x, "lands_on": w if w in (0, "loop") else words[w][0]})
    (WORK / "pic.txt").write_text("".join(f"file '{s.name}'\n" for s in segs))
    pic = WORK / "picture.mp4"
    ff("-f", "concat", "-safe", "0", "-i", "pic.txt", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "fast",
       "-crf", "17", "-r", str(FPS), "-t", f"{total:.3f}", str(pic), cwd=WORK)

    bed = synth_warm_bed(WORK / "hos007_s05_synth_pad_v01.wav", total)
    bed_gain = (mean_db(vo) - 20.0) - mean_db(bed)
    audio = WORK / "audio.wav"
    ff("-i", str(vo), "-i", str(bed), "-filter_complex",
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
    render(title_png, TITLE_BANNER, 60, 250, index=2, stroke=4)
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
    mp4 = HERE / f"hos_007_{SID}_{VER}.mp4"
    ff(*inputs, "-filter_complex", ";".join(fc), "-map", last, "-map", "1:a", "-c:v", "libx264",
       "-pix_fmt", "yuv420p", "-profile:v", "high", "-preset", "medium", "-crf", "18", "-r", str(FPS),
       "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2", "-t", f"{total:.3f}", "-movflags", "+faststart",
       str(mp4))
    timeline = [{"role": r, "text": t, "t0": round(a, 3), "t1": round(c, 3)} for _, a, c, r, t in overlays]
    timeline.append({"role": "who", "text": " · ".join(CARD), "t0": CARD_IN, "t1": CARD_OUT})
    (WORK / "timeline.json").write_text(json.dumps({"plan": plan, "overlays": timeline}, indent=2) + "\n")
    return {"id": SID, "version": VER, "job": JOB, "test": "B (search-titled)", "air_date_draft": air_date,
            "file": mp4.relative_to(PROJ).as_posix(), "sha256": sha256(mp4), "duration_s": round(probe(mp4), 3),
            "vo_source": rel_to_proj(RAW_VO), "vo_take_indices": TAKE,
            "dropped": DROPPED,
            "route": "60-word sentence-aligned lift from Part 04 (62..76 + 103..147): Jenner wasn't the first to try cowpox. Benjamin Jesty had done it twenty-two years earlier. He tested more people, and in seventeen ninety-eight he paid to print a short book. He called the disease by a Latin name, variolae vaccinae, which means smallpox of the cow. From vacca, the Latin word for cow, came the name for the treatment: vaccination.",
            "vo_s": round(vo_s, 3), "words": len(words), "max_pause_s": MAX_PAUSE, "atempo": ATEMPO,
            "bed": f"{bed.name} (own synthesis, 0 credits)", "bed_gain_db": round(bed_gain, 2),
            "hook": HOOK.replace("**", ""), "hook_layer": hook_meta, "who_card": card_meta,
            "title_on_screen": TITLE, "youtube_title_draft": TITLE_DRAFT, "plan": plan,
            "captions": len(chunks), "timeline": timeline}


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


def sample_handovers(mp4: Path, timeline: list[dict], sample_n: int = 10) -> dict:
    """Sample caption handovers (before/after frames at 30 fps) to verify 1 caption per frame (no double stack)."""
    vo_rows = [r for r in timeline if r["role"] == "vo"]
    handover_dir = WORK / "handovers"
    handover_dir.mkdir(parents=True, exist_ok=True)

    dur = probe(mp4)
    n_frames = int(round(dur * FPS))
    max_active_any_frame = 0
    for f_idx in range(n_frames):
        t = f_idx / FPS
        active = [r for r in vo_rows if r["t0"] <= t < r["t1"]]
        if len(active) > max_active_any_frame:
            max_active_any_frame = len(active)

    all_boundaries = [(k, vo_rows[k], vo_rows[k + 1]) for k in range(len(vo_rows) - 1)]
    sampled = all_boundaries[:sample_n]
    samples_out = []
    tiles = []

    for idx, (k, r_prev, r_next) in enumerate(sampled, 1):
        b = r_prev["t1"]
        f_prev = math.ceil(b * FPS) - 1
        f_next = math.ceil(b * FPS)
        t_prev = round(f_prev / FPS, 4)
        t_next = round(f_next / FPS, 4)

        active_prev = [r["text"] for r in vo_rows if r["t0"] <= (f_prev / FPS) < r["t1"]]
        active_next = [r["text"] for r in vo_rows if r["t0"] <= (f_next / FPS) < r["t1"]]
        active_at_b = [r["text"] for r in vo_rows if r["t0"] <= b < r["t1"]]

        p_prev = handover_dir / f"h{idx:02d}_f{f_prev:04d}_prev.png"
        p_next = handover_dir / f"h{idx:02d}_f{f_next:04d}_next.png"
        ff("-i", str(mp4), "-vf", f"select=eq(n\\,{f_prev}),crop=1000:260:40:1360",
           "-frames:v", "1", str(p_prev))
        ff("-i", str(mp4), "-vf", f"select=eq(n\\,{f_next}),crop=1000:260:40:1360",
           "-frames:v", "1", str(p_next))

        cap_a = Image.open(WORK / f"cap_{k:03d}.png").crop((40, 1360, 1040, 1620))
        cap_b = Image.open(WORK / f"cap_{k + 1:03d}.png").crop((40, 1360, 1040, 1620))
        im_prev = Image.open(p_prev).convert("RGB")
        im_next = Image.open(p_next).convert("RGB")

        def cream_hit_ratio(im_rgb: Image.Image, cap_rgba: Image.Image, other_rgba: Image.Image) -> float:
            px_im = im_rgb.load()
            px_c = cap_rgba.load()
            px_o = other_rgba.load()
            w_, h_ = im_rgb.size
            fill_hits = fill_pts = stroke_hits = stroke_pts = 0
            for yy in range(h_):
                for xx in range(w_):
                    r, g, bl, al = px_c[xx, yy]
                    if al == 255 and px_o[xx, yy][3] == 0:
                        ir, ig, ib = px_im[xx, yy]
                        if r > 210 and g > 200 and bl > 180:
                            fill_pts += 1
                            if ir > 190 and ig > 180 and ib > 160:
                                fill_hits += 1
                        elif r < 40 and g < 40 and bl < 40:
                            stroke_pts += 1
                            if ir < 65 and ig < 65 and ib < 65:
                                stroke_hits += 1
            f_ratio = fill_hits / fill_pts if fill_pts else 0.0
            s_ratio = stroke_hits / stroke_pts if stroke_pts else 0.0
            return round(min(f_ratio, s_ratio), 3)

        prev_has_a = cream_hit_ratio(im_prev, cap_a, cap_b)
        prev_has_b = cream_hit_ratio(im_prev, cap_b, cap_a)
        next_has_a = cream_hit_ratio(im_next, cap_a, cap_b)
        next_has_b = cream_hit_ratio(im_next, cap_b, cap_a)

        one_caption_each = (
            len(active_prev) == 1
            and len(active_next) == 1
            and len(active_at_b) == 1
            and prev_has_a >= 0.85
            and prev_has_b <= 0.15
            and next_has_b >= 0.85
            and next_has_a <= 0.15
        )
        samples_out.append({
            "handover": idx,
            "boundary_s": b,
            "prev_frame": f_prev,
            "prev_t_s": t_prev,
            "prev_caption": active_prev[0] if active_prev else None,
            "next_frame": f_next,
            "next_t_s": t_next,
            "next_caption": active_next[0] if active_next else None,
            "active_count_prev": len(active_prev),
            "active_count_at_boundary": len(active_at_b),
            "active_count_next": len(active_next),
            "pixel_fill_prev": {"caption_a": prev_has_a, "caption_b": prev_has_b},
            "pixel_fill_next": {"caption_a": next_has_a, "caption_b": next_has_b},
            "one_caption_each": one_caption_each,
        })
        tiles.append((idx, b, f_prev, r_prev["text"], im_prev, f_next, r_next["text"], im_next))

    sheet = Image.new("RGB", (1020, 140 * len(tiles)), (18, 18, 20))
    sd = ImageDraw.Draw(sheet)
    lbl_font = ImageFont.truetype(CTA_FONT, 18)
    for row_i, (idx, b, f_prev, txt_a, im_prev, f_next, txt_b, im_next) in enumerate(tiles):
        y0 = row_i * 140
        p1 = im_prev.resize((490, 127))
        p2 = im_next.resize((490, 127))
        sheet.paste(p1, (10, y0 + 10))
        sheet.paste(p2, (520, y0 + 10))
        sd.text((14, y0 + 12), f"#{idx:02d} @ {b:.3f}s | f{f_prev} ({f_prev/FPS:.3f}s): {txt_a}",
                font=lbl_font, fill=(255, 214, 70))
        sd.text((524, y0 + 12), f"f{f_next} ({f_next/FPS:.3f}s): {txt_b}",
                font=lbl_font, fill=(140, 240, 160))
    sheet_path = WORK / f"hos_007_{SID}_{VER}_handovers_10.jpg"
    sheet.save(sheet_path, quality=90)

    all_ok = max_active_any_frame == 1 and all(s["one_caption_each"] for s in samples_out)
    if not all_ok:
        raise SystemExit(f"handover check failed: max_active={max_active_any_frame}, samples={samples_out}")
    return {
        "ok": all_ok,
        "total_handovers": len(all_boundaries),
        "sampled_handovers": len(samples_out),
        "max_active_vo_captions_any_frame": max_active_any_frame,
        "sheet": sheet_path.relative_to(PROJ).as_posix(),
        "samples": samples_out,
    }


def freeze(mp4: Path) -> list[str]:
    err = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(mp4), "-vf",
                          "freezedetect=n=0.003:d=0.8", "-map", "0:v", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    return re.findall(r"freeze_start: ([\d.]+)", err)


def run_qa(mp4: Path, plan: list[dict]) -> dict:
    """Run polish_gate and picture_qa into QA_DIR so QA sweep files are present and PASS."""
    QA_DIR.mkdir(parents=True, exist_ok=True)
    cuts_data, pool_data, seen = [], [], set()
    for k, row in enumerate(plan, 1):
        base = Path(row["plate"]).name
        src_id = f"loop_end_{base}" if row["lands_on"] == "loop" else base
        cuts_data.append({
            "row": f"s{k:02d}_{row['lands_on']}",
            "timeline_in": row["t0"],
            "timeline_out": row["t1"],
            "source": src_id,
            "upscale": 1.0,
            "framing": {"offset": row["in_s"]},
            "video": True,
        })
        if src_id not in seen:
            seen.add(src_id)
            title = f"Loop end plate {base}" if row["lands_on"] == "loop" else f"Flow Veo 3.1 plate {base}"
            pool_data.append({"file_id": src_id, "title": title})
    cuts_f = QA_DIR / f"cuts_{SID}_{VER}.json"
    pool_f = QA_DIR / f"pool_{SID}_{VER}.json"
    cuts_f.write_text(json.dumps(cuts_data, indent=2) + "\n")
    pool_f.write_text(json.dumps(pool_data, indent=2) + "\n")

    pg_json = QA_DIR / f"polish_gate_{SID}_{VER}.json"
    pg_txt = QA_DIR / f"polish_gate_{SID}_{VER}.txt"
    r_pg = subprocess.run([sys.executable, str(OWB_REPO / "scripts/polish_gate.py"),
                           str(mp4.relative_to(REPO)), "--cuts", str(cuts_f.relative_to(REPO)),
                           "--out", str(pg_json.relative_to(REPO))],
                          cwd=REPO, capture_output=True, text=True)
    pg_out = (r_pg.stdout + r_pg.stderr).strip()
    pg_txt.write_text(pg_out + "\n")

    pqa_dir = QA_DIR / f"picture_qa_{SID}_{VER}"
    pqa_txt = QA_DIR / f"picture_qa_{SID}_{VER}.txt"
    r_pqa = subprocess.run([sys.executable, str(OWB_REPO / "scripts/picture_qa.py"),
                            str(mp4.relative_to(REPO)), "--cuts", str(cuts_f.relative_to(REPO)),
                            "--pool", str(pool_f.relative_to(REPO)),
                            "--out-dir", str(pqa_dir.relative_to(REPO))],
                           cwd=REPO, capture_output=True, text=True)
    pqa_out = (r_pqa.stdout + r_pqa.stderr).strip()
    pqa_txt.write_text(pqa_out + "\n")
    return {
        "polish_gate": {"exit": r_pg.returncode, "output": pg_out.splitlines()[-1] if pg_out else ""},
        "picture_qa": {"exit": r_pqa.returncode, "output": pqa_out.splitlines()[-1] if pqa_out else ""},
    }


def run(cmd: list[str]) -> tuple[int, str]:
    r = subprocess.run(cmd, capture_output=True, text=True)
    out = "\n".join(line for line in (r.stdout + r.stderr).splitlines() if "Warning" not in line and line.strip())
    return r.returncode, out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--air-date", default="2026-11-17")
    ap.add_argument("--no-icloud", action="store_true")
    ns = ap.parse_args()
    rec = build(ns.air_date)
    mp4 = PROJ / rec["file"]
    timeline = rec.pop("timeline")
    rec["caption_check"] = caption_check(mp4, timeline)
    rec["handover_check"] = sample_handovers(mp4, timeline, sample_n=10)
    code, out = run([sys.executable, str(GATE), "check", str(mp4), "--air-date", ns.air_date])
    rec["gate"] = {"exit": code, "output": out}
    code, out = run([str(VO_PY), str(VO_CHECK), str(mp4), "--script", str(SCRIPT_TXT)])
    rec["vo_check"] = {"exit": code, "output": out}
    rec["freezedetect_starts"] = freeze(mp4)
    rec["qa"] = run_qa(mp4, rec["plan"])
    stills = []
    for t in (0.0, 4.0, 11.5, 17.5, round(rec["duration_s"] - 1.0, 1)):
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
        "date": "2026-10-24",
        "source": "suggestqueries client=youtube ds=yt gl=GB signed-out",
        "hits": [
            "why is it called vaccines",
            "vaccine latin words",
            "benjamin jesty",
            "who invented the first vaccine",
            "edward jenner cowpox vaccine",
        ],
        "note": "Signed-out GB YouTube autocomplete returns 'why is it called vaccines', 'vaccine latin words', 'benjamin jesty', 'who invented the first vaccine', and 'edward jenner cowpox vaccine' as exact hits (24 Oct 2026). Title draft 'Why Is It Called a Vaccine?' (with 'Who Tried Cowpox Before Edward Jenner?' and 'Where Does the Word Vaccine Come From?' as alternatives) is answered directly by the lifted Part 04 VO: Benjamin Jesty's 1774 cowpox inoculation 22 years before Jenner, Jenner's 1798 Inquiry naming the disease variolae vaccinae ('smallpox of the cow'), and vacca (Latin for cow) giving us 'vaccination'. Second built search-titled Short on HOS 007 (completing 007's Test B pair alongside s04_smallpox_test_v01). Chief's call.",
    }
    rec["air_date_draft_note"] = "2027-01-26 used for the gate only; slot is Chief's call."
    rec["who_card_note"] = "card BENJAMIN JESTY · Dorset · 1774 on screen 2.40–5.80 s while 'Benjamin Jesty' is said. No watch-the-full-film line. Loop is 1.15 s back onto the frame-0 meadow."
    rec["overlap_note"] = "Second built search-titled Short lifted from HOS 007's long VO (Part 04 words 62..76 + 103..147: Jesty 1774, 1798 Inquiry, variolae vaccinae / vacca -> vaccination). Zero spoken-word or plate overlap with s04_smallpox_test_v01 (Part 04 words 0..61), 007 Short B (Part 02 milkmaids' secret), or 007 Short C (Part 05 1980 global eradication)."
    (HERE / f"SHORT_{SID}_{VER}.json").write_text(json.dumps(rec, indent=2) + "\n")
    print(f"BUILT {SID} {VER} {rec['duration_s']} s {rec['words']} words sha {rec['sha256'][:12]} "
          f"captions {rec['caption_check']} handovers_ok={rec['handover_check']['ok']} "
          f"(sampled {rec['handover_check']['sampled_handovers']}/{rec['handover_check']['total_handovers']})")
    print(rec["gate"]["output"])
    print(rec["vo_check"]["output"])
    print(rec["qa"]["polish_gate"]["output"])
    print(rec["qa"]["picture_qa"]["output"])
    print(f"freezedetect: {len(rec['freezedetect_starts'])} events {rec['freezedetect_starts']}")


if __name__ == "__main__":
    main()
