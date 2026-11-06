#!/usr/bin/env python3
"""HOS 008 Short C v03. £0. No upload.

Layout C-v03a: C-Open-1 (hos_008_short_C_s01_v03) plus the contiguous
5.720–24.400 s body of hos_008_short_C_v02.wav. Picture is the J2175
9-cut schedule (crop 438,0,405,720 → 936×1664). The recorded opening
ends at 2.68 s, so sentence 1 stays whole and the first cut is at
68 frames (2.833 s), inside the 2.85 s hook gate. Body audio starts
at 2.90 s (0.22 s after the last opening word).
"""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

OWB = Path("/Users/benjaminoats/YouTube/orbit-with-ben")
sys.path.insert(0, str(OWB / "scripts"))
import terminal_loop  # noqa: E402

WT = Path("/Users/benjaminoats/_desk/worktrees/J2255")
FILM = WT / "02_Video-Projects/008_Lightning-Franklin"
SHARED = Path("/Users/benjaminoats/YouTube/History Of Science/02_Video-Projects/008_Lightning-Franklin")
PLATE = Path("/Users/benjaminoats/YouTube/hos-008-lightning/02_Video-Projects/008_Lightning-Franklin/04_Generated-Clips")
VO = SHARED / "10_Shorts/vo_v02"
WORK = Path("/private/tmp/j2255-short-c")
PACK = FILM / "10_Shorts/J2255"
MASTER = SHARED / "10_Shorts/hos_008_short_C_v03.mp4"

W, H, FPS = 936, 1664, 24
CROP = (438, 0, 405, 720)
UPSCALE = 2.3111
BODY_T0 = 2.90
BODY_IN, BODY_OUT = 5.720, 24.400
SR = 48000
FONT = "/System/Library/Fonts/Supplemental/Didot.ttc"
CREAM = (245, 232, 210, 255)
YEL = (255, 214, 70, 255)
INK = (42, 26, 16, 255)
TITLE = "Why Did Franklin Fly a Kite in a Storm?"

# Frame counts. S01 is 68/24 = 2.833 s so the whole 2.68 s sentence sits inside the 2.85 s hook gate.
FRAMES = [
    ("S01", 68, "part05/raw/v01/19_skyline_strike_t1.mp4", 1.0),
    ("S02", 69, "part05/raw/v01/01_house_rod_t1.mp4", 0.8),
    ("S03", 70, "part05/raw/v01/07_giant_spark_t1.mp4", 0.6),
    ("S04", 70, "part01/raw/v01/12_steeple_fire_t1.mp4", 0.8),
    ("S05", 67, "part05/raw/v01/18_rod_closeup_t1.mp4", 0.0),
    ("S06", 67, "part05/raw/v01/06_rod_fitting_t1.mp4", 1.5),
    ("S07", 65, "part05/raw/v01/06_rod_fitting_c1_t1.mp4", 1.5),
    ("S08", 45, "part05/raw/v01/14_safe_towers_t1.mp4", 4.2),
    ("loop_tail", 24, "part05/raw/v01/19_skyline_strike_t1.mp4", 1.0),
]
TOTAL_FRAMES = sum(n for _, n, _, _ in FRAMES)
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


def probe_dur(path: Path) -> float:
    return float(subprocess.check_output(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)], text=True))


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
    for row, frames, rel, offset in FRAMES:
        dur = frames / FPS
        rows.append({
            "row": row,
            "timeline_in": t,
            "timeline_out": t + dur,
            "source": str(PLATE / rel),
            "upscale": UPSCALE,
            "video": True,
            "framing": {"offset": offset, "crop": list(CROP), "output": [W, H]},
            **({"role": "prescribed_terminal_loop"} if row == "loop_tail" else {}),
        })
        t += dur
    return rows


def build_picture(rows: list[dict]) -> Path:
    seg_dir = WORK / "segs"
    seg_dir.mkdir(parents=True, exist_ok=True)
    segs = []
    for i, row in enumerate(rows):
        frames = FRAMES[i][1]
        x, y, w, h = CROP
        dst = seg_dir / f"{i:02d}_{row['row']}.mp4"
        run([
            "ffmpeg", "-y", "-v", "error", "-i", row["source"],
            "-vf", (f"trim=start={row['framing']['offset']}:duration={frames / FPS:.6f},setpts=PTS-STARTPTS,"
                    f"crop={w}:{h}:{x}:{y},scale={W}:{H}:flags=lanczos,fps={FPS},format=yuv420p,setsar=1"),
            "-frames:v", str(frames), "-an", "-c:v", "libx264", "-pix_fmt", "yuv420p",
            "-preset", "veryfast", "-crf", "16", "-r", str(FPS), str(dst),
        ])
        got = int(subprocess.check_output(
            ["ffprobe", "-v", "error", "-select_streams", "v:0", "-count_frames",
             "-show_entries", "stream=nb_read_frames", "-of", "csv=p=0", str(dst)], text=True).strip())
        if got != frames:
            raise SystemExit(f"{row['row']}: {got} frames, wanted {frames}")
        segs.append(dst)
    lst = WORK / "pic.txt"
    lst.write_text("".join(f"file '{s}'\n" for s in segs))
    pic = WORK / "picture.mp4"
    run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", str(lst),
         "-c", "copy", "-movflags", "+faststart", str(pic)])
    return pic


def build_vo() -> tuple[Path, list[dict]]:
    open_words = words_of(VO / "stt/hos_008_short_C_s01_v03/stt_raw.json")
    body_src = words_of(VO / "stt/hos_008_short_C_v02/stt_raw.json")
    body = []
    for w in body_src:
        if w["start"] >= BODY_IN - 0.001 and w["end"] <= BODY_OUT + 0.001:
            body.append({
                "text": w["text"],
                "start": round(w["start"] - BODY_IN + BODY_T0, 3),
                "end": round(w["end"] - BODY_IN + BODY_T0, 3),
            })
    if not body or body[0]["text"].lower().rstrip(".") != "lightning":
        raise SystemExit(f"body does not start on Lightning: {body[:2]}")
    body[-1]["end"] = round(BODY_T0 + (BODY_OUT - BODY_IN), 3)
    spoken = open_words + body
    start = int(round(BODY_IN * SR))
    end = int(round(BODY_OUT * SR))
    if start != 274560 or end != 1171200:
        raise SystemExit(f"body sample bounds {start}:{end}")
    vo = WORK / "vo.wav"
    run([
        "ffmpeg", "-y", "-v", "error",
        "-i", str(VO / "hos_008_short_C_s01_v03.wav"),
        "-i", str(VO / "hos_008_short_C_v02.wav"),
        "-filter_complex",
        (f"[0:a]aformat=sample_rates={SR}:channel_layouts=stereo,atrim=0:{BODY_T0:.3f},"
         f"apad=whole_dur={BODY_T0:.3f},asetpts=PTS-STARTPTS[a];"
         f"[1:a]aformat=sample_rates={SR}:channel_layouts=stereo,"
         f"atrim=start_sample={start}:end_sample={end},asetpts=PTS-STARTPTS[b];"
         f"[a][b]concat=n=2:v=0:a=1,apad=whole_dur={TOTAL:.6f},asetpts=PTS-STARTPTS[o]"),
        "-map", "[o]", "-c:a", "pcm_s16le", str(vo),
    ])
    return vo, spoken


def build_bed() -> Path:
    music = FILM / "05_Music"
    music.mkdir(parents=True, exist_ok=True)
    bed = music / "hos_008_short_C_v03_bed.wav"
    src = SHARED / "05_Music/lightning008_score_bed_v02.mp3"
    run(["ffmpeg", "-y", "-v", "error", "-ss", "96", "-t", f"{TOTAL + 1:.3f}", "-i", str(src),
         "-ac", "2", "-ar", str(SR), str(bed)])
    plan = {
        "created_at": "2026-11-06T15:50:00+00:00",
        "project": "hos_008_short_C_v03",
        "generate": False,
        "audio_file": bed.name,
        "source_take": "lightning008_score_bed_v02.mp3",
        "note": "23 s slice of the film's own v02 bed from 96 s. No new ElevenLabs take. £0.",
        "prompt": (
            "HOS 008 Short C, a slice of the film's own lightning bed. Soft gut-string quartet, "
            "a quiet baroque pulse, and one wooden flute, under a spoken explanation of the lightning rod. "
            "Leave room for a spoken voice. No vocals. Pace: 64-72 BPM. NOT the 007 vaccine wooden-harp bed, "
            "NOT the Trees of Air bed, NOT Orbit cosmic pads, Betelgeuse, Saturn, Sun, Venus, Light Speed, "
            "Mars or the nearest-star bed; no drums, no EDM, no cartoon sting, no menace drone."
        ),
    }
    (music / "hos_008_short_C_v03_bed_plan.json").write_text(json.dumps(plan, indent=2) + "\n")
    return bed


def build_sfx(rows: list[dict]) -> Path:
    kit = SHARED / "06_Sound-Effects/kit_v01"
    sfx = WORK / "sfx.wav"
    whoosh = kit / "sfx_hos_whoosh_soft_v01.wav"
    rumble = kit / "sfx_hos_rumble_low_v01.wav"
    tick = kit / "sfx_hos_tick_ink_v01.wav"
    s08 = next(r for r in rows if r["row"] == "S08")
    s04 = next(r for r in rows if r["row"] == "S04")
    tick_ms = int(s08["timeline_in"] * 1000)
    fire_ms = int(s04["timeline_in"] * 1000)
    run([
        "ffmpeg", "-y", "-v", "error",
        "-i", str(whoosh), "-i", str(rumble), "-i", str(rumble), "-i", str(tick),
        "-filter_complex",
        (f"[0:a]aformat=sample_rates={SR}:channel_layouts=stereo,volume=-4dB[w];"
         f"[1:a]aformat=sample_rates={SR}:channel_layouts=stereo,atrim=0:2.8,volume=-10dB[r1];"
         f"[2:a]aformat=sample_rates={SR}:channel_layouts=stereo,atrim=0:2.8,volume=-12dB,adelay={fire_ms}|{fire_ms}[r2];"
         f"[3:a]aformat=sample_rates={SR}:channel_layouts=stereo,volume=-2dB,adelay={tick_ms}|{tick_ms}[t];"
         f"[w][r1][r2][t]amix=inputs=4:normalize=0:duration=longest,apad=whole_dur={TOTAL:.6f}[o]"),
        "-map", "[o]", "-t", f"{TOTAL:.6f}", "-c:a", "pcm_s16le", str(sfx),
    ])
    return sfx


def mix(vo: Path, bed: Path, sfx: Path) -> Path:
    audio = WORK / "mix.wav"
    run([
        "ffmpeg", "-y", "-v", "error", "-i", str(vo), "-i", str(bed), "-i", str(sfx),
        "-filter_complex",
        (f"[0:a]aformat=sample_rates={SR}:channel_layouts=stereo[v];"
         f"[1:a]aformat=sample_rates={SR}:channel_layouts=stereo,atrim=0:{TOTAL:.6f},volume=-18dB[b];"
         f"[2:a]aformat=sample_rates={SR}:channel_layouts=stereo,volume=-6dB[s];"
         f"[v][b][s]amix=inputs=3:normalize=0:duration=first,loudnorm=I=-14:TP=-2.0:LRA=11[o]"),
        "-map", "[o]", "-t", f"{TOTAL:.6f}", "-c:a", "pcm_s16le", str(audio),
    ])
    return audio


def font(size: int, index: int = 0) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(FONT, size, index=index)


def soft_panel(img: Image.Image, box: tuple[int, int, int, int]) -> None:
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    d.rounded_rectangle(box, radius=36, fill=(72, 44, 28, 150))
    layer = layer.filter(ImageFilter.GaussianBlur(8))
    img.alpha_composite(layer)


def draw_lines(img: Image.Image, lines: list[tuple[str, bool]], size: int, y: int, index: int = 0) -> None:
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
    block = cap + pitch
    top = int(H * 0.34)
    draw = ImageDraw.Draw(img)
    for i, (t, hot) in enumerate(tokens):
        draw.text((W / 2, top + cap + i * pitch), t, font=f, anchor="ms",
                  fill=YEL if hot else CREAM, stroke_width=5, stroke_fill=INK)
    img.info["block"] = block
    return img


def render_captions(spoken: list[dict]) -> list[tuple[Path, float, float]]:
    body = [w for w in spoken if w["start"] >= BODY_T0 - 0.01]
    chunks = []
    i = 0
    while i < len(body):
        parts = [body[i]]
        j = i + 1
        while j < len(body):
            if parts[-1]["text"][-1:] in ".?!":
                break
            if body[j]["end"] - parts[0]["start"] > 3.4 or len(parts) >= 6:
                break
            parts.append(body[j])
            j += 1
        t0 = parts[0]["start"]
        t1 = min(parts[-1]["end"] + 0.18, TOTAL - 1.05)
        if t1 - t0 > 0.25:
            chunks.append((t0, t1, " ".join(p["text"] for p in parts)))
        i = j if j > i else i + 1
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


def mae(video: Path, t: float, source_t: float) -> float:
    expected = terminal_loop.frame(PLATE / "part05/raw/v01/19_skyline_strike_t1.mp4", source_t, list(CROP))
    actual = terminal_loop.frame(video, t)
    return sum(abs(a - b) for a, b in zip(expected, actual)) / len(actual)


def burn(pic: Path, hook: Image.Image, caps: list[tuple[Path, float, float]], title: Path, data: Path, rows: list[dict]) -> Path:
    hook_png = WORK / "hook.png"
    hook.save(hook_png)
    s08 = next(r for r in rows if r["row"] == "S08")
    data_t0 = max(s08["timeline_in"], 19.90)
    data_t1 = min(s08["timeline_out"] - 0.08, 21.55)
    overlays = [(hook_png, 0.0, BODY_T0), (title, 9.0, 14.0), (data, data_t0, data_t1)] + [
        (p, a, b) for p, a, b in caps
    ]
    cmd = ["ffmpeg", "-y", "-v", "error", "-i", str(pic)]
    for png, _, _ in overlays:
        cmd += ["-loop", "1", "-i", str(png)]
    parts, last = [], "[0:v]"
    for i, (_, t0, t1) in enumerate(overlays, 1):
        parts.append(f"{last}[{i}:v]overlay=0:0:enable='between(t,{t0:.3f},{t1:.3f})'[v{i}]")
        last = f"[v{i}]"
    out = WORK / "picture_text.mp4"
    cmd += ["-filter_complex", ";".join(parts), "-map", last, "-frames:v", str(TOTAL_FRAMES),
            "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "veryfast", "-crf", "17",
            "-r", str(FPS), str(out)]
    run(cmd)
    return out


def mux(video: Path, audio: Path, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    run(["ffmpeg", "-y", "-v", "error", "-i", str(video), "-i", str(audio),
         "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
         "-ar", str(SR), "-ac", "2", "-movflags", "+faststart", str(dest)])


def main() -> None:
    if WORK.exists():
        import shutil
        shutil.rmtree(WORK)
    WORK.mkdir(parents=True)
    PACK.mkdir(parents=True, exist_ok=True)
    rows = timeline()
    print(f"timeline {TOTAL:.6f}s {TOTAL_FRAMES} frames", flush=True)
    pic = build_picture(rows)
    print("picture", probe_dur(pic), flush=True)
    vo, spoken = build_vo()
    print("vo", probe_dur(vo), "words", len(spoken), "last", spoken[-1], flush=True)
    bed = build_bed()
    sfx = build_sfx(rows)
    audio = mix(vo, bed, sfx)
    caps = render_captions(spoken)
    title = render_title()
    data = render_data()
    hook_size = 96
    video = None
    while hook_size >= 64:
        try:
            hook = render_hook(hook_size)
        except ValueError:
            hook_size -= 8
            continue
        video = burn(pic, hook, caps, title, data, rows)
        scores = [mae(video, 0.0, 1.0), mae(video, 0.958333, 1.958333)]
        print(f"hook {hook_size} mae {scores}", flush=True)
        if max(scores) <= 7.5:
            break
        hook_size -= 8
    else:
        raise SystemExit("hook caption pushes the opening frames past the loop match")
    mux(video, audio, MASTER)
    (PACK / "cuts.json").write_text(json.dumps(rows, indent=2) + "\n")
    (PACK / "spoken.json").write_text(json.dumps(spoken, indent=2) + "\n")
    print("master", MASTER, probe_dur(MASTER), sha256(MASTER), flush=True)


if __name__ == "__main__":
    main()
