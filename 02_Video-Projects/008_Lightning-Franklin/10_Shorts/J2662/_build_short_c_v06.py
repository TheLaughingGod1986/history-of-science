#!/usr/bin/env python3
"""HOS 008 Short C v06 (J2662 — J2485 Fix List + SFX speech headroom + 2-pass loudnorm). £0. No upload.

Leaves hos_008_short_C_v03.mp4, v04, and v05 untouched on NAS, writing new version
hos_008_short_C_v06.mp4 and stems under 10_Shorts/J2662_v06/.
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import wave
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

REPO = Path(__file__).resolve().parents[4]
OWB = Path(os.environ.get("OWB_ROOT", str(REPO.parent / "orbit-with-ben")))
sys.path.insert(0, str(OWB / "scripts"))
import terminal_loop  # noqa: E402

SHARED = Path(
    os.environ.get(
        "HOS_008_SHARED",
        "/Volumes/data/studio-live/History Of Science/02_Video-Projects/008_Lightning-Franklin",
    )
)
PLATE = SHARED / "04_Generated-Clips"
VO = SHARED / "10_Shorts/vo_v02"
WORK = Path(
    os.environ.get(
        "J2662_WORK",
        "/Users/ben/.gemini/antigravity-cli/brain/bb728e9e-2e5d-405d-b6a3-63e0de5cc1ff/scratch/j2662_v06_work",
    )
)
PACK = Path(__file__).resolve().parent
FILM_GIT = REPO / "02_Video-Projects/008_Lightning-Franklin"
MASTER = SHARED / "10_Shorts/hos_008_short_C_v06.mp4"

W, H, FPS = 936, 1664, 24
UPSCALE = 2.3111
ATEMPO = 1.06
BODY_T0 = 2.10
BODY_IN, BODY_OUT = 5.720, 24.400
SR = 48000
FONT = "/System/Library/Fonts/Supplemental/Didot.ttc"
CREAM = (245, 232, 210, 255)
YEL = (255, 214, 70, 255)
INK = (28, 16, 10, 255)
TITLE = "Why Did Franklin Fly a Kite in a Storm?"

FRAMES = [
    ("S01", 49, "part05/raw/v01/19_skyline_strike_t1.mp4", 1.0, (600, 0, 405, 720)),
    ("S02", 69, "part05/raw/v01/01_house_rod_t1.mp4", 0.8, (180, 0, 405, 720)),
    ("S03", 70, "part05/raw/v01/07_giant_spark_t1.mp4", 0.6, (438, 0, 405, 720)),
    ("S04", 70, "part01/raw/v01/12_steeple_fire_t1.mp4", 0.8, (438, 0, 405, 720)),
    ("S05", 67, "part05/raw/v01/18_rod_closeup_t1.mp4", 0.0, (438, 0, 405, 720)),
    ("S06", 67, "part05/raw/v01/06_rod_fitting_t1.mp4", 4.0, (438, 0, 405, 720)),
    ("S07", 65, "part05/raw/v01/06_rod_fitting_c1_t1.mp4", 3.1, (438, 0, 405, 720)),
    ("S08", 49, "part05/raw/v01/14_safe_towers_t1.mp4", 4.2, (438, 0, 405, 720)),
    ("loop_tail", 24, "part05/raw/v01/19_skyline_strike_t1.mp4", 1.0, (600, 0, 405, 720)),
]
TOTAL_FRAMES = sum(n for _, n, _, _, _ in FRAMES)
TOTAL = TOTAL_FRAMES / FPS


def run(cmd: list[str], cwd: Path | None = None) -> None:
    r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    if r.returncode != 0:
        raise SystemExit(f"FAIL {' '.join(cmd[:8])}\n{r.stderr[-2000:]}")


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def copy_verified(src: Path, dst: Path) -> str:
    dst.parent.mkdir(parents=True, exist_ok=True)
    h_src = sha256(src)
    shutil.copy2(src, dst)
    h_dst = sha256(dst)
    if h_src != h_dst:
        raise SystemExit(f"SHA-256 mismatch copying {src} -> {dst}")
    return h_dst


def probe_dur(path: Path) -> float:
    return float(
        subprocess.check_output(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)],
            text=True,
        )
    )


def words_of(path: Path) -> list[dict]:
    data = json.loads(path.read_text())
    raw = data["words"] if isinstance(data, dict) and "words" in data else data
    out = []
    for w in raw:
        text = (w.get("text") or w.get("word") or "").strip()
        if not text:
            continue
        out.append({"text": text, "start": float(w["start"]), "end": float(w["end"])})
    return out


def timeline() -> list[dict]:
    t = 0.0
    rows = []
    for row, frames, rel, offset, crop in FRAMES:
        dur = frames / FPS
        rows.append(
            {
                "row": row,
                "timeline_in": t,
                "timeline_out": t + dur,
                "source": str(PLATE / rel),
                "upscale": UPSCALE,
                "video": True,
                "framing": {"offset": offset, "crop": list(crop), "output": [W, H]},
                **({"role": "prescribed_terminal_loop"} if row == "loop_tail" else {}),
            }
        )
        t += dur
    return rows


def build_picture(rows: list[dict]) -> Path:
    seg_dir = WORK / "segs"
    seg_dir.mkdir(parents=True, exist_ok=True)
    segs = []
    for i, row in enumerate(rows):
        frames = FRAMES[i][1]
        x, y, w, h = row["framing"]["crop"]
        dst = seg_dir / f"{i:02d}_{row['row']}.mp4"
        run(
            [
                "ffmpeg", "-y", "-v", "error", "-i", row["source"],
                "-vf",
                (
                    f"trim=start={row['framing']['offset']}:duration={frames / FPS:.6f},setpts=PTS-STARTPTS,"
                    f"crop={w}:{h}:{x}:{y},scale={W}:{H}:flags=lanczos,fps={FPS},format=yuv420p,setsar=1"
                ),
                "-frames:v", str(frames), "-an", "-c:v", "libx264", "-pix_fmt", "yuv420p",
                "-preset", "veryfast", "-crf", "16", "-r", str(FPS), str(dst),
            ]
        )
        got = int(
            subprocess.check_output(
                [
                    "ffprobe", "-v", "error", "-select_streams", "v:0", "-count_frames",
                    "-show_entries", "stream=nb_read_frames", "-of", "csv=p=0", str(dst),
                ],
                text=True,
            ).strip()
        )
        if got != frames:
            raise SystemExit(f"{row['row']}: {got} frames, wanted {frames}")
        segs.append(dst)
    lst = WORK / "pic.txt"
    lst.write_text("".join(f"file '{s}'\n" for s in segs))
    pic = WORK / "picture.mp4"
    run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", str(lst), "-c", "copy", "-movflags", "+faststart", str(pic)])
    return pic


def zero_crossing_near(mono: np.ndarray, idx: int, radius: int = 240) -> int:
    lo = max(1, idx - radius)
    hi = min(len(mono) - 1, idx + radius)
    best = idx
    best_val = abs(float(mono[idx]))
    for k in range(lo, hi):
        if (mono[k - 1] <= 0 <= mono[k]) or (mono[k - 1] >= 0 >= mono[k]):
            if abs(float(mono[k])) < best_val:
                best = k
                best_val = abs(float(mono[k]))
    return best


def build_s01_vo() -> tuple[Path, list[dict]]:
    src_wav = VO / "hos_008_short_C_s01_v03.wav"
    with wave.open(str(src_wav), "rb") as wf:
        ch, sw, sr, nframes = wf.getnchannels(), wf.getsampwidth(), wf.getframerate(), wf.getnframes()
        samples = np.frombuffer(wf.readframes(nframes), dtype=np.int16).reshape(-1, ch)
    if sr != SR or sw != 2:
        raise SystemExit(f"unexpected s01 format sr={sr} sw={sw}")
    mono = samples.mean(axis=1)
    trim0 = int(round(0.062 * SR))
    cut_a = zero_crossing_near(mono, int(round(0.245 * SR)))
    cut_b = zero_crossing_near(mono, int(round(0.780 * SR)))
    xf = int(round(0.015 * SR))
    left = samples[trim0:cut_a + xf].astype(np.float32)
    right = samples[cut_b - xf:].astype(np.float32)
    fade = np.linspace(0.0, 1.0, 2 * xf, dtype=np.float32)[:, None]
    spliced = np.vstack(
        [
            left[:-2 * xf],
            left[-2 * xf:] * (1.0 - fade) + right[:2 * xf] * fade,
            right[2 * xf:],
        ]
    )
    raw_splice = WORK / "s01_splice_raw.wav"
    with wave.open(str(raw_splice), "wb") as wf:
        wf.setnchannels(ch)
        wf.setsampwidth(2)
        wf.setframerate(SR)
        wf.writeframes(np.clip(np.round(spliced), -32768, 32767).astype(np.int16).tobytes())

    s01_out = WORK / "s01_v06.wav"
    run(["ffmpeg", "-y", "-v", "error", "-i", str(raw_splice), "-af", f"atempo={ATEMPO}", "-ar", str(SR), "-ac", "2", "-c:a", "pcm_s16le", str(s01_out)])

    removed_s = (cut_b - cut_a) / SR
    lead_s = trim0 / SR
    raw_words = words_of(VO / "stt/hos_008_short_C_s01_v03/stt_raw.json")
    open_words = []
    for w in raw_words:
        if w["text"].lower().strip(".,?!") == "rooftop":
            continue
        shift = lead_s + (removed_s if w["start"] > 0.5 else 0.0)
        open_words.append(
            {
                "text": w["text"],
                "start": round((w["start"] - shift) / ATEMPO, 3),
                "end": round((w["end"] - shift) / ATEMPO, 3),
            }
        )
    return s01_out, open_words


def build_vo() -> tuple[Path, list[dict]]:
    s01_wav, open_words = build_s01_vo()
    body_src = words_of(VO / "stt/hos_008_short_C_v02/stt_raw.json")
    body = []
    for w in body_src:
        if w["start"] >= BODY_IN - 0.001 and w["end"] <= BODY_OUT + 0.001:
            body.append(
                {
                    "text": w["text"],
                    "start": round(w["start"] - BODY_IN + BODY_T0, 3),
                    "end": round(w["end"] - BODY_IN + BODY_T0, 3),
                }
            )
    if not body or body[0]["text"].lower().rstrip(".") != "lightning":
        raise SystemExit(f"body does not start on Lightning: {body[:2]}")
    body[-1]["end"] = round(BODY_T0 + (BODY_OUT - BODY_IN), 3)
    spoken = open_words + body
    start = int(round(BODY_IN * SR))
    end = int(round(BODY_OUT * SR))
    vo = WORK / "vo.wav"
    run(
        [
            "ffmpeg", "-y", "-v", "error",
            "-i", str(s01_wav),
            "-i", str(VO / "hos_008_short_C_v02.wav"),
            "-filter_complex",
            (
                f"[0:a]aformat=sample_rates={SR}:channel_layouts=stereo,atrim=0:{BODY_T0:.3f},"
                f"apad=whole_dur={BODY_T0:.3f},asetpts=PTS-STARTPTS[a];"
                f"[1:a]aformat=sample_rates={SR}:channel_layouts=stereo,"
                f"atrim=start_sample={start}:end_sample={end},asetpts=PTS-STARTPTS[b];"
                f"[a][b]concat=n=2:v=0:a=1,apad=whole_dur={TOTAL:.6f},asetpts=PTS-STARTPTS[o]"
            ),
            "-map", "[o]", "-c:a", "pcm_s16le", str(vo),
        ]
    )
    return vo, spoken


def build_bed() -> tuple[Path, Path]:
    bed_full = WORK / "hos_008_short_C_v06_bed.wav"
    src = SHARED / "05_Music/lightning008_score_bed_v02.mp3"
    run(["ffmpeg", "-y", "-v", "error", "-ss", "96", "-t", f"{TOTAL + 1:.3f}", "-i", str(src), "-ac", "2", "-ar", str(SR), str(bed_full)])
    bed_stem = WORK / "bed.wav"
    run(
        [
            "ffmpeg", "-y", "-v", "error", "-i", str(bed_full),
            "-af", f"aformat=sample_rates={SR}:channel_layouts=stereo,atrim=0:{TOTAL:.6f},volume=-18dB",
            "-t", f"{TOTAL:.6f}", "-c:a", "pcm_s16le", str(bed_stem),
        ]
    )
    plan = {
        "created_at": "2026-11-17T10:32:00+00:00",
        "project": "hos_008_short_C_v06",
        "generate": False,
        "audio_file": bed_full.name,
        "source_take": "lightning008_score_bed_v02.mp3",
        "note": "23.1 s slice of the film's own v02 bed from 96 s. No new ElevenLabs take. £0.",
        "prompt": (
            "HOS 008 Short C, a slice of the film's own lightning bed. Soft gut-string quartet, "
            "a quiet baroque pulse, and one wooden flute, under a spoken explanation of the lightning rod. "
            "Leave room for a spoken voice. No vocals. Pace: 64-72 BPM. NOT the 007 vaccine wooden-harp bed, "
            "NOT the Trees of Air bed, NOT Orbit cosmic pads, Betelgeuse, Saturn, Sun, Venus, Light Speed, "
            "Mars or the nearest-star bed; no drums, no EDM, no cartoon sting, no menace drone."
        ),
    }
    (FILM_GIT / "05_Music").mkdir(parents=True, exist_ok=True)
    (FILM_GIT / "05_Music/hos_008_short_C_v06_bed_plan.json").write_text(json.dumps(plan, indent=2) + "\n")
    return bed_full, bed_stem


def build_sfx(rows: list[dict]) -> Path:
    kit = SHARED / "06_Sound-Effects/kit_v01"
    sfx = WORK / "sfx.wav"
    whoosh = kit / "sfx_hos_whoosh_soft_v01.wav"
    rumble = kit / "sfx_hos_rumble_low_v01.wav"
    tick = kit / "sfx_hos_tick_ink_v01.wav"
    s08 = next(r for r in rows if r["row"] == "S08")
    s04 = next(r for r in rows if r["row"] == "S04")
    tick_ms = int(round(s08["timeline_in"] * 1000))
    fire_ms = int(round(s04["timeline_in"] * 1000))
    run(
        [
            "ffmpeg", "-y", "-v", "error",
            "-i", str(whoosh), "-i", str(rumble), "-i", str(rumble), "-i", str(tick),
            "-filter_complex",
            (
                f"[0:a]aformat=sample_rates={SR}:channel_layouts=stereo,volume=-14dB[w];"
                f"[1:a]aformat=sample_rates={SR}:channel_layouts=stereo,atrim=0:2.0,volume=-20dB[r1];"
                f"[2:a]aformat=sample_rates={SR}:channel_layouts=stereo,atrim=0:2.8,volume=-18dB,adelay={fire_ms}|{fire_ms}[r2];"
                f"[3:a]aformat=sample_rates={SR}:channel_layouts=stereo,volume=-8dB,adelay={tick_ms}|{tick_ms}[t];"
                f"[w][r1][r2][t]amix=inputs=4:normalize=0:duration=longest,apad=whole_dur={TOTAL:.6f}[o]"
            ),
            "-map", "[o]", "-t", f"{TOTAL:.6f}", "-c:a", "pcm_s16le", str(sfx),
        ]
    )
    return sfx


def mix(vo: Path, bed_stem: Path, sfx_stem: Path) -> Path:
    raw = WORK / "mix_raw.wav"
    run(
        [
            "ffmpeg", "-y", "-v", "error", "-i", str(vo), "-i", str(bed_stem), "-i", str(sfx_stem),
            "-filter_complex",
            (
                f"[0:a]aformat=sample_rates={SR}:channel_layouts=stereo[v];"
                f"[1:a]aformat=sample_rates={SR}:channel_layouts=stereo[b];"
                f"[2:a]aformat=sample_rates={SR}:channel_layouts=stereo[s];"
                f"[v][b][s]amix=inputs=3:normalize=0:duration=first[o]"
            ),
            "-map", "[o]", "-t", f"{TOTAL:.6f}", "-c:a", "pcm_s16le", str(raw),
        ]
    )
    p1 = subprocess.run(
        ["ffmpeg", "-hide_banner", "-i", str(raw), "-af", "alimiter=limit=0.72:level=false,loudnorm=I=-14.0:TP=-2.0:LRA=11.0:print_format=json", "-f", "null", "-"],
        capture_output=True, text=True, check=True,
    )
    m = re.search(r"\{\s*\"input_i\".*?\}", p1.stderr, re.S)
    if not m:
        raise SystemExit("loudnorm pass 1 JSON missing")
    stats = json.loads(m.group(0))
    audio = WORK / "mix.wav"
    run(
        [
            "ffmpeg", "-y", "-v", "error", "-i", str(raw),
            "-af",
            (
                f"alimiter=limit=0.72:level=false,loudnorm=I=-14.0:TP=-2.0:LRA=11.0:"
                f"measured_I={stats['input_i']}:measured_TP={stats['input_tp']}:"
                f"measured_LRA={stats['input_lra']}:measured_thresh={stats['input_thresh']}:"
                f"offset={stats['target_offset']}:linear=true,alimiter=limit=0.78:level=false"
            ),
            "-ar", str(SR), "-ac", "2", "-t", f"{TOTAL:.6f}", "-c:a", "pcm_s16le", str(audio),
        ]
    )
    return audio


def font(size: int, index: int = 0) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(FONT, size, index=index)


def soft_panel(img: Image.Image, box: tuple[int, int, int, int]) -> None:
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    d.rounded_rectangle(box, radius=36, fill=(72, 44, 28, 150))
    layer = layer.filter(ImageFilter.GaussianBlur(8))
    img.alpha_composite(layer)


def draw_lines(img: Image.Image, lines: list[list[tuple[str, bool]]], size: int, y: int, index: int = 0) -> None:
    f = font(size, index)
    draw = ImageDraw.Draw(img)
    asc, desc = f.getmetrics()
    lh, gap = asc + desc, int(size * 0.16)
    space = f.getlength(" ")
    cy = y
    for line in lines:
        width = sum(f.getlength(t) for t, _ in line) + space * (len(line) - 1)
        x = (W - width) / 2
        for t, hot in line:
            draw.text((x, cy), t, font=f, fill=YEL if hot else CREAM, stroke_width=max(2, size // 18), stroke_fill=INK)
            x += f.getlength(t) + space
        cy += lh + gap


def render_hook(size: int) -> Image.Image:
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    f = font(size, 2)
    tokens = [("FRANKLIN'S", False), ("ROD", True)]
    if any(f.getlength(t) > W - 80 for t, _ in tokens):
        raise ValueError("hook too wide")
    cap = -f.getbbox("H", anchor="ls")[1]
    pitch = int(cap * 1.28)
    top = int(H * 0.27)
    shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    for i, (t, _) in enumerate(tokens):
        sd.text((W / 2, top + cap + i * pitch + 4), t, font=f, anchor="ms", fill=(18, 10, 6, 220), stroke_width=10, stroke_fill=(18, 10, 6, 220))
    img.alpha_composite(shadow.filter(ImageFilter.GaussianBlur(4)))
    draw = ImageDraw.Draw(img)
    for i, (t, hot) in enumerate(tokens):
        draw.text((W / 2, top + cap + i * pitch), t, font=f, anchor="ms", fill=YEL if hot else CREAM, stroke_width=7, stroke_fill=INK)
    return img


def group_body_sentences(body: list[dict]) -> list[list[dict]]:
    sentences: list[list[dict]] = []
    cur: list[dict] = []
    for w in body:
        cur.append(w)
        if w["text"][-1:] in ".?!":
            sentences.append(cur)
            cur = []
    if cur:
        sentences.append(cur)

    groups: list[list[dict]] = []
    for sent in sentences:
        clauses: list[list[dict]] = []
        c: list[dict] = []
        for w in sent:
            c.append(w)
            if w["text"][-1:] in ",;:":
                clauses.append(c)
                c = []
        if c:
            clauses.append(c)
        for cl in clauses:
            n = len(cl)
            if n <= 7:
                groups.append(cl)
            else:
                half = n // 2
                groups.append(cl[:half])
                groups.append(cl[half:])
    return groups


def render_captions(spoken: list[dict]) -> list[tuple[Path, float, float]]:
    body = [w for w in spoken if w["start"] >= BODY_T0 - 0.01]
    groups = group_body_sentences(body)
    chunks = []
    for idx, parts in enumerate(groups):
        t0 = parts[0]["start"]
        next_t0 = groups[idx + 1][0]["start"] if idx + 1 < len(groups) else TOTAL
        t1 = min(parts[-1]["end"] + 0.18, next_t0 - 0.04, TOTAL - 1.05)
        if t1 - t0 > 0.20:
            chunks.append((t0, t1, " ".join(p["text"] for p in parts)))
    out = []
    for n, (t0, t1, text) in enumerate(chunks):
        img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        soft_panel(img, (36, 1240, W - 36, 1488))
        words = [(w, False) for w in text.split()]
        lines, cur = [], []
        f = font(46)
        for tok in words:
            trial = " ".join(t for t, _ in cur + [tok])
            if cur and f.getlength(trial) > W - 120:
                lines.append(cur)
                cur = [tok]
            else:
                cur.append(tok)
        if cur:
            lines.append(cur)
        draw_lines(img, lines, 46, 1288)
        png = WORK / f"cap_{n:03d}.png"
        img.save(png)
        out.append((png, t0, t1))
    return out


def render_title() -> Path:
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    wash = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(wash)
    for yy in range(420):
        a = int(130 * (1 - yy / 420) ** 1.4)
        d.line([(0, yy), (W, yy)], fill=(48, 30, 18, a))
    img.alpha_composite(wash.filter(ImageFilter.GaussianBlur(2)))
    f = font(42, 2)
    tokens = [(w, False) for w in TITLE.split()]
    lines, cur = [], []
    for tok in tokens:
        trial = " ".join(t for t, _ in cur + [tok])
        if cur and f.getlength(trial) > W - 80:
            lines.append(cur)
            cur = [tok]
        else:
            cur.append(tok)
    if cur:
        lines.append(cur)
    draw_lines(img, lines, 42, 78, index=2)
    png = WORK / "title.png"
    img.save(png)
    return png


def render_data() -> Path:
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    band_h = int(W * 9 / 16)
    y0 = (H - band_h) // 2
    soft_panel(img, (70, y0 + 36, W - 70, y0 + 36 + 150))
    draw_lines(img, [[("20+", False), ("STRIKES", False)], [("A", False), ("YEAR", False)]], 58, y0 + 58, index=2)
    png = WORK / "data.png"
    img.save(png)
    return png


def mae(video: Path, t: float, source_t: float, crop: list[int]) -> float:
    expected = terminal_loop.frame(PLATE / "part05/raw/v01/19_skyline_strike_t1.mp4", source_t, crop)
    actual = terminal_loop.frame(video, t)
    return sum(abs(a - b) for a, b in zip(expected, actual)) / len(actual)


def burn(pic: Path, hook: Image.Image, caps: list[tuple[Path, float, float]], title: Path, data: Path, rows: list[dict]) -> Path:
    hook_png = WORK / "hook.png"
    hook.save(hook_png)
    s08 = next(r for r in rows if r["row"] == "S08")
    hook_end = round(rows[0]["timeline_out"] - 0.02, 3)
    data_t0 = max(s08["timeline_in"], 19.10)
    data_t1 = min(s08["timeline_out"] - 0.08, 20.95)
    overlays = [(hook_png, 0.0, hook_end), (title, 9.0, 14.0), (data, data_t0, data_t1)] + [(p, a, b) for p, a, b in caps]
    cmd = ["ffmpeg", "-y", "-v", "error", "-i", str(pic)]
    for png, _, _ in overlays:
        cmd += ["-loop", "1", "-i", str(png)]
    parts, last = [], "[0:v]"
    for i, (_, t0, t1) in enumerate(overlays, 1):
        parts.append(f"{last}[{i}:v]overlay=0:0:enable='between(t,{t0:.3f},{t1:.3f})'[v{i}]")
        last = f"[v{i}]"
    out = WORK / "picture_text.mp4"
    cmd += [
        "-filter_complex", ";".join(parts), "-map", last, "-frames:v", str(TOTAL_FRAMES),
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "veryfast", "-crf", "17",
        "-r", str(FPS), str(out),
    ]
    run(cmd)
    return out


def mux(video: Path, audio: Path, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    run(
        [
            "ffmpeg", "-y", "-v", "error", "-i", str(video), "-i", str(audio),
            "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
            "-ar", str(SR), "-ac", "2", "-movflags", "+faststart", str(dest),
        ]
    )


def main() -> None:
    local_only = "--local-only" in sys.argv
    if not local_only and MASTER.exists() and "--force" not in sys.argv:
        raise SystemExit(f"Refusing to overwrite existing NAS master {MASTER}; pass --force or bump version.")
    if WORK.exists():
        shutil.rmtree(WORK)
    WORK.mkdir(parents=True)
    PACK.mkdir(parents=True, exist_ok=True)

    rows = timeline()
    pic = build_picture(rows)
    vo, spoken = build_vo()
    bed_full, bed_stem = build_bed()
    sfx_stem = build_sfx(rows)
    audio = mix(vo, bed_stem, sfx_stem)
    caps = render_captions(spoken)
    title = render_title()
    data = render_data()

    open_crop = rows[0]["framing"]["crop"]
    hook_size = 104
    video = None
    while hook_size >= 64:
        try:
            hook = render_hook(hook_size)
        except ValueError:
            hook_size -= 8
            continue
        video = burn(pic, hook, caps, title, data, rows)
        scores = [mae(video, 0.0, 1.0, open_crop), mae(video, 0.958333, 1.958333, open_crop)]
        if max(scores) <= 7.5:
            break
        hook_size -= 8
    else:
        raise SystemExit("hook caption pushes opening frames past loop match")

    local_master = WORK / "hos_008_short_C_v06.mp4"
    mux(video, audio, local_master)

    words_json = {"words": spoken}
    local_meta = {
        "spoken": " ".join(w["text"] for w in spoken),
        "words": spoken,
        "vo": str(vo if local_only else SHARED / "10_Shorts/J2662_v06/vo.wav"),
        "last_word_end_s": spoken[-1]["end"],
        "hook_caption": {"text": "FRANKLIN'S ROD", "start_s": 0.0, "end_s": round(rows[0]["timeline_out"] - 0.02, 3)},
    }
    (WORK / "hos_008_short_C_v06_words.json").write_text(json.dumps(words_json, indent=2) + "\n")
    (WORK / "hos_008_short_C_v06_meta.json").write_text(json.dumps(local_meta, indent=2) + "\n")
    (PACK / "cuts.json").write_text(json.dumps(rows, indent=2) + "\n")
    (PACK / "spoken.json").write_text(json.dumps(spoken, indent=2) + "\n")

    if local_only:
        print("local_master", local_master, probe_dur(local_master), sha256(local_master), flush=True)
        return

    nas_stems = SHARED / "10_Shorts/J2662_v06"
    copy_verified(vo, nas_stems / "vo.wav")
    copy_verified(bed_stem, nas_stems / "bed.wav")
    copy_verified(sfx_stem, nas_stems / "sfx.wav")
    copy_verified(bed_full, SHARED / "05_Music/hos_008_short_C_v06_bed.wav")
    copy_verified(FILM_GIT / "05_Music/hos_008_short_C_v06_bed_plan.json", SHARED / "05_Music/hos_008_short_C_v06_bed_plan.json")
    master_sha = copy_verified(local_master, MASTER)
    (SHARED / "10_Shorts/hos_008_short_C_v06_words.json").write_text(json.dumps(words_json, indent=2) + "\n")
    (SHARED / "10_Shorts/hos_008_short_C_v06_meta.json").write_text(json.dumps(local_meta, indent=2) + "\n")
    print("master", MASTER, probe_dur(MASTER), master_sha, flush=True)


if __name__ == "__main__":
    main()
