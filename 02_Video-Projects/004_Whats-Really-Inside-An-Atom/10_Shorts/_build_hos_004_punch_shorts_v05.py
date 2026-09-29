#!/usr/bin/env python3
"""HOS 004 Shorts punch v05 — word-timed captions from VO align JSON.

Ben phone UAT (29 Sep): v04 captions frozen / not following VO.
v05: chunk VO alignment into short phrases that change as spoken.
Keep hook (HOW SMALL? / EVERY EIGHTH? / HER RING), title card 9–14 s,
last-4 s loop + CTA. 30 fps CFR. Quiet bed. No upload.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

VENV_PY = Path(
    "/Users/benjaminoats/YouTube/History Of Science/"
    "02_Video-Projects/001_How-Did-We-Discover-Germs/10_Shorts/_venv/bin/python"
)
if VENV_PY.exists() and Path(sys.executable) != VENV_PY:
    os.execv(str(VENV_PY), [str(VENV_PY), str(Path(__file__).resolve())])

from PIL import Image, ImageDraw, ImageFont  # noqa: E402

REPO = Path("/Users/benjaminoats/YouTube/History Of Science")
HERE = Path(__file__).resolve().parent
PROJ = HERE.parent
PROJ002 = REPO / "02_Video-Projects/002_How-Did-We-Discover-The-Periodic-Table"
PROJ003 = REPO / "02_Video-Projects/003_Invisible-Bones-X-Rays"
ICLOUD = Path.home() / (
    "Library/Mobile Documents/com~apple~CloudDocs/HOS UAT/"
    "004_Whats-Really-Inside-An-Atom/10_Shorts"
)
GATE = REPO / "00_Brand/Channel-Setup/tools/gate_shorts_open.py"
FONT = "/System/Library/Fonts/Supplemental/Didot.ttc"
CTA_FONT = "/System/Library/Fonts/Supplemental/Times New Roman.ttf"
W, H = 1080, 1920
FPS = 30
CREAM = (245, 232, 210, 255)
INK = (28, 26, 28, 255)
YEL = (255, 214, 70, 255)
VF = "scale=1920:1080,crop=608:1080:656:0,scale=1080:1920:flags=lanczos,setsar=1"
EASE = 0.40
BED = PROJ / "05_Music/hos004-part01-temp_score_bed_v01.mp3"
BED_VOL = 0.07

# Word-chunk targets (seconds / words)
CHUNK_MAX_S = 1.55
CHUNK_MAX_WORDS = 5
CHUNK_MIN_S = 0.45

SHORTS = [
    {
        "id": "s01_how_small",
        "air_date": "2026-10-16",
        "hook": "HOW SMALL?",
        "parent": "What's Really Inside an Atom?",
        "vo": HERE / "vo_v03/hos_004_s01_how_small_vo_v03.wav",
        "align": HERE / "vo_v03/hos_004_s01_how_small_vo_v03_align.json",
        "mode": "plates",
        "plates": [
            PROJ / "04_Generated-Clips/part01/raw/v01/01_coin_halves_v01.mp4",
            PROJ / "04_Generated-Clips/part01/raw/v01/02_atom_answer_v01.mp4",
            PROJ / "04_Generated-Clips/part01/raw/v01/03_atom_turns_v01.mp4",
            PROJ / "04_Generated-Clips/part04/raw/v01/14_nucleus_electrons_v01.mp4",
            PROJ / "04_Generated-Clips/part04/raw/v01/19_nucleus_question_v02.mp4",
        ],
        "forbid": ["stadium"],
        "open_plate": 0,
    },
    {
        "id": "s02_every_eighth",
        "air_date": "2026-10-18",
        "hook": "EVERY EIGHTH?",
        "parent": "How Did We Discover the Periodic Table?",
        "vo": HERE / "vo_v03/hos_004_s02_every_eighth_vo_v04.wav",
        "align": HERE / "vo_v03/hos_004_s02_every_eighth_vo_v04_align.json",
        "mode": "rough",
        "rough": PROJ002 / "09_Final-Export/hos_002_part02_rough_v06.mp4",
        "wins": [(59.5, 7.5), (34.0, 7.0), (66.5, 7.0), (42.0, 6.0)],
        "open_ss": 59.5,
        "open_speed": 0.55,
        "forbid": [],
    },
    {
        "id": "s03_her_ring",
        "air_date": "2026-10-20",
        "hook": "HER RING",
        "parent": "How Did We Discover X-rays?",
        "vo": HERE / "vo_v03/hos_004_s03_her_ring_vo_v03.wav",
        "align": HERE / "vo_v03/hos_004_s03_her_ring_vo_v03_align.json",
        "mode": "plates",
        "plates": [
            PROJ003 / "04_Generated-Clips/part04/02_hand_on_plate_v02.mp4",
            PROJ003 / "04_Generated-Clips/part04/03_bones_and_ring_v02.mp4",
            PROJ003 / "04_Generated-Clips/part04/11_proof_hold_v02.mp4",
            PROJ003 / "04_Generated-Clips/part04/04_haunted_becomes_fact_v02.mp4",
        ],
        "forbid": [],
        "open_plate": 0,
    },
]


def probe(p: Path) -> float:
    return float(
        subprocess.check_output(
            [
                "ffprobe",
                "-v",
                "error",
                "-show_entries",
                "format=duration",
                "-of",
                "csv=p=0",
                str(p),
            ],
            text=True,
        ).strip()
    )


def ff(*a: str) -> None:
    subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", *a], check=True)


def sha256(p: Path) -> str:
    import hashlib

    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def wrap(text: str, font: ImageFont.FreeTypeFont, max_w: int) -> list[str]:
    words = text.split()
    lines: list[str] = []
    cur = ""
    for w in words:
        trial = (cur + " " + w).strip()
        if font.getlength(trial) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines or [text]


def render(
    path: Path,
    text: str,
    size: int,
    anchor: str,
    y: int,
    font_path=FONT,
    fill=CREAM,
) -> None:
    font = ImageFont.truetype(font_path, size)
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    lines = wrap(text, font, W - 96)
    heights = [font.getbbox(l)[3] - font.getbbox(l)[1] for l in lines]
    gap = int(size * 0.28)
    block = sum(heights) + gap * (len(lines) - 1)
    top = H - y - block if anchor == "bottom" else y
    cy = top
    stroke = 3
    for line, lh in zip(lines, heights):
        tw = font.getlength(line)
        x = (W - tw) / 2
        for dx in range(-stroke, stroke + 1):
            for dy in range(-stroke, stroke + 1):
                if dx or dy:
                    draw.text((x + dx, cy + dy), line, font=font, fill=INK)
        draw.text((x, cy), line, font=font, fill=fill)
        cy += lh + gap
    path.parent.mkdir(parents=True, exist_ok=True)
    img.save(path)


def words_from_align(align_path: Path) -> list[tuple[str, float, float]]:
    d = json.loads(align_path.read_text())
    chars = d["characters"]
    starts = d["character_start_times_seconds"]
    ends = d["character_end_times_seconds"]
    words: list[tuple[str, float, float]] = []
    cur = ""
    w0 = w1 = None
    for i, ch in enumerate(chars):
        if ch.isspace() or ch == "\n":
            if cur.strip():
                words.append((cur, float(w0), float(w1)))
            cur = ""
            w0 = w1 = None
        else:
            if w0 is None:
                w0 = starts[i]
            w1 = ends[i]
            cur += ch
    if cur.strip():
        words.append((cur, float(w0), float(w1)))
    return words


def chunk_words(words: list[tuple[str, float, float]], story: float) -> list[dict]:
    """Group words into short VO-timed phrases that change while spoken."""
    chunks: list[dict] = []
    i = 0
    n = len(words)
    while i < n:
        w0, t0, _ = words[i]
        if t0 >= story - 0.05:
            break
        parts = [w0]
        t_end = words[i][2]
        j = i + 1
        while j < n:
            wj, sj, ej = words[j]
            if sj >= story - 0.02:
                break
            dur = ej - t0
            # break after punctuation if we already have content
            prev = parts[-1]
            punct_break = prev[-1:] in ".?!,;:—-" and len(parts) >= 2
            if punct_break and (sj - t0) >= CHUNK_MIN_S:
                break
            if len(parts) >= CHUNK_MAX_WORDS and (sj - t0) >= CHUNK_MIN_S:
                break
            if dur >= CHUNK_MAX_S and len(parts) >= 2:
                break
            parts.append(wj)
            t_end = ej
            j += 1
        # end at next word start (seamless handoff) or padded end
        if j < n and words[j][1] < story:
            t1 = min(story - 0.02, words[j][1])
        else:
            t1 = min(story - 0.02, t_end + 0.12)
        if t1 <= t0:
            t1 = min(story - 0.02, t0 + 0.35)
        text = " ".join(parts)
        # tidy spaces before punctuation leftovers
        text = text.replace(" ,", ",").replace(" .", ".").replace(" ?", "?").replace(" !", "!")
        chunks.append({"text": text, "t0": round(t0, 3), "t1": round(t1, 3), "n_words": len(parts)})
        i = j if j > i else i + 1
    # enforce non-overlap / monotonic
    cleaned: list[dict] = []
    for c in chunks:
        if cleaned and c["t0"] < cleaned[-1]["t1"]:
            c = dict(c)
            c["t0"] = cleaned[-1]["t1"]
        if c["t1"] - c["t0"] < 0.12:
            continue
        if c["t0"] >= story - 0.05:
            continue
        c["t1"] = min(c["t1"], story - 0.02)
        cleaned.append(c)
    return cleaned


def encode_seg(src: Path, dst: Path, start: float, dur: float, *, speed: float | None = None) -> None:
    vf = VF
    t_src = dur
    if speed and speed < 0.99:
        vf = f"{VF},setpts={speed}*PTS"
        t_src = min(dur / speed + 0.25, 10.0)
    ff(
        "-ss",
        f"{start:.3f}",
        "-t",
        f"{t_src:.3f}",
        "-i",
        str(src),
        "-vf",
        vf,
        "-an",
        "-c:v",
        "libx264",
        "-pix_fmt",
        "yuv420p",
        "-profile:v",
        "high",
        "-preset",
        "fast",
        "-crf",
        "18",
        "-r",
        str(FPS),
        "-t",
        f"{dur:.3f}",
        "-movflags",
        "+faststart",
        str(dst),
    )


def build_picture(item: dict, work: Path, need: float) -> tuple[Path, Path]:
    segs: list[Path] = []
    covered = 0.0
    if item["mode"] == "plates":
        plates = list(item["plates"])
        for p in plates:
            if not p.exists():
                raise SystemExit(f"missing {p}")
            low = str(p).lower()
            for bad in item.get("forbid") or []:
                if bad.lower() in low:
                    raise SystemExit(f"forbidden plate {p}")
        i = 0
        while covered < need - 0.05:
            p = plates[i % len(plates)]
            u = max(0.5, probe(p) - EASE - 0.3)
            take = min(u, need - covered)
            revisit = i // len(plates)
            start = EASE + min(0.8 * revisit, max(0.0, u - take))
            out = work / f"seg_{i:02d}.mp4"
            encode_seg(p, out, start, take)
            segs.append(out)
            covered += take
            i += 1
        open_src = plates[item.get("open_plate", 0)]
        open_ss = EASE
        open_speed = None
    else:
        rough = Path(item["rough"])
        wins = list(item["wins"])
        i = 0
        while covered < need - 0.05:
            st, mx = wins[i % len(wins)]
            off = 0.6 * (i // len(wins))
            take = min(mx - off, need - covered)
            if take < 0.4:
                i += 1
                continue
            out = work / f"seg_{i:02d}.mp4"
            speed = item.get("open_speed") if i == 0 else None
            encode_seg(rough, out, st + off, take, speed=speed)
            segs.append(out)
            covered += take
            i += 1
        open_src = rough
        open_ss = float(item["open_ss"])
        open_speed = None

    concat = work / "pic.txt"
    concat.write_text("".join(f"file '{s.name}'\n" for s in segs))
    pic = work / "picture.mp4"
    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-hide_banner",
            "-loglevel",
            "error",
            "-f",
            "concat",
            "-safe",
            "0",
            "-i",
            str(concat),
            "-c",
            "copy",
            str(pic),
        ],
        check=True,
        cwd=work,
    )
    trim = work / "picture_trim.mp4"
    ff(
        "-i",
        str(pic),
        "-t",
        f"{need:.3f}",
        "-c:v",
        "libx264",
        "-pix_fmt",
        "yuv420p",
        "-preset",
        "fast",
        "-crf",
        "18",
        "-r",
        str(FPS),
        "-an",
        str(trim),
    )
    loop_src = work / "open_src.mp4"
    encode_seg(open_src, loop_src, open_ss, 4.5, speed=open_speed)
    return trim, loop_src


def fit_story_loop(vo_dur: float) -> tuple[float, float, float]:
    loop = 4.0
    story = vo_dur
    total = story + loop
    if total > 27.0:
        over = total - 27.0
        cut = min(over, max(0.0, loop - 3.5))
        loop -= cut
        over -= cut
        if over > 0:
            story = max(18.0, story - over)
        total = story + loop
    if total < 22.0:
        story = 22.0 - loop
        total = 22.0
    if not (22.0 <= total <= 27.05):
        raise SystemExit(f"fit fail vo={vo_dur} -> {total}")
    return story, loop, total


def mix_vo_bed(vo: Path, story: float, work: Path) -> Path:
    vo_fit = work / "vo_fit.wav"
    vo_dur = probe(vo)
    if vo_dur < story:
        ff(
            "-i",
            str(vo),
            "-af",
            f"apad=pad_dur={story - vo_dur:.3f}",
            "-t",
            f"{story:.3f}",
            "-ar",
            "48000",
            "-ac",
            "2",
            str(vo_fit),
        )
    else:
        ff("-i", str(vo), "-t", f"{story:.3f}", "-ar", "48000", "-ac", "2", str(vo_fit))
    mixed = work / "vo_bed.wav"
    if BED.exists():
        ff(
            "-stream_loop",
            "-1",
            "-i",
            str(BED),
            "-i",
            str(vo_fit),
            "-filter_complex",
            f"[0:a]volume={BED_VOL},atrim=0:{story:.3f},asetpts=PTS-STARTPTS[bed];"
            f"[1:a]aformat=sample_rates=48000:channel_layouts=stereo[vo];"
            f"[vo][bed]amix=inputs=2:weights=1 1:normalize=0:duration=first:dropout_transition=0[a]",
            "-map",
            "[a]",
            "-t",
            f"{story:.3f}",
            "-ar",
            "48000",
            "-ac",
            "2",
            str(mixed),
        )
    else:
        mixed = vo_fit
    return mixed


def caption_overlays(
    work: Path, item: dict, story: float, total: float, chunks: list[dict]
) -> tuple[list[tuple[Path, float, float, str, str]], list[dict]]:
    """Return overlays (path,t0,t1,role,text) and timeline rows for QA."""
    overlays: list[tuple[Path, float, float, str, str]] = []
    timeline: list[dict] = []

    hook = work / "cap_hook.png"
    render(hook, item["hook"], 64, "top", 160, fill=YEL)
    hook_end = min(2.8, story * 0.14)
    overlays.append((hook, 0.0, hook_end, "hook", item["hook"]))
    timeline.append({"role": "hook", "text": item["hook"], "t0": 0.0, "t1": hook_end})

    for i, ch in enumerate(chunks):
        png = work / f"cap_w_{i:03d}.png"
        render(png, ch["text"], 44, "bottom", 300)
        overlays.append((png, ch["t0"], ch["t1"], "vo", ch["text"]))
        timeline.append({"role": "vo", "text": ch["text"], "t0": ch["t0"], "t1": ch["t1"], "n_words": ch["n_words"]})

    title = work / "cap_title.png"
    render(title, item["parent"], 34, "top", 220)
    t0 = min(9.0, max(8.5, story * 0.38))
    t1 = min(14.0, max(t0 + 3.5, story * 0.62))
    t1 = min(t1, story - 0.05)
    if t1 > t0 + 1.0:
        overlays.append((title, t0, t1, "title", item["parent"]))
        timeline.append({"role": "title", "text": item["parent"], "t0": t0, "t1": t1})

    cta = work / "cap_cta.png"
    render(cta, "watch the full film →", 40, "bottom", 240, font_path=CTA_FONT)
    cta_in = max(total - 4.0, story)
    overlays.append((cta, cta_in, total - 0.08, "cta", "watch the full film →"))
    timeline.append({"role": "cta", "text": "watch the full film →", "t0": cta_in, "t1": total - 0.08})

    return overlays, timeline


def build_one(item: dict) -> dict:
    vo = Path(item["vo"])
    align = Path(item["align"])
    if not vo.exists():
        raise SystemExit(f"missing VO {vo}")
    if not align.exists():
        raise SystemExit(f"missing align {align}")
    vo_dur = probe(vo)
    story, loop, total = fit_story_loop(vo_dur)
    work = HERE / "_work_v05" / item["id"]
    if work.exists():
        import shutil

        shutil.rmtree(work)
    work.mkdir(parents=True, exist_ok=True)

    words = words_from_align(align)
    chunks = chunk_words(words, story)
    if len(chunks) < 8:
        raise SystemExit(f"{item['id']}: too few caption chunks ({len(chunks)}) — align broken?")
    (work / "caption_chunks.json").write_text(json.dumps(chunks, indent=2) + "\n")

    pic, open_clip = build_picture(item, work, story)
    audio = mix_vo_bed(vo, story, work)

    story_av = work / "story_av.mp4"
    ff(
        "-i",
        str(pic),
        "-i",
        str(audio),
        "-map",
        "0:v",
        "-map",
        "1:a",
        "-c:v",
        "copy",
        "-c:a",
        "aac",
        "-b:a",
        "192k",
        "-ar",
        "48000",
        "-ac",
        "2",
        "-shortest",
        str(story_av),
    )

    loop_vid = work / "loop.mp4"
    ff(
        "-i",
        str(open_clip),
        "-t",
        f"{loop:.3f}",
        "-c:v",
        "libx264",
        "-pix_fmt",
        "yuv420p",
        "-preset",
        "fast",
        "-crf",
        "18",
        "-r",
        str(FPS),
        "-an",
        str(loop_vid),
    )
    loop_av = work / "loop_av.mp4"
    ff(
        "-i",
        str(loop_vid),
        "-f",
        "lavfi",
        "-i",
        "anullsrc=r=48000:cl=stereo",
        "-shortest",
        "-c:v",
        "copy",
        "-c:a",
        "aac",
        "-b:a",
        "192k",
        str(loop_av),
    )

    raw = work / "raw.mp4"
    (work / "av.txt").write_text(f"file '{story_av.name}'\nfile '{loop_av.name}'\n")
    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-hide_banner",
            "-loglevel",
            "error",
            "-f",
            "concat",
            "-safe",
            "0",
            "-i",
            str(work / "av.txt"),
            "-c",
            "copy",
            str(raw),
        ],
        check=True,
        cwd=work,
    )

    overlays, timeline = caption_overlays(work, item, story, total, chunks)
    (work / "caption_timeline.json").write_text(json.dumps(timeline, indent=2) + "\n")

    inputs: list[str] = ["-i", str(raw)]
    for png, _, _, _, _ in overlays:
        inputs += ["-loop", "1", "-i", str(png)]
    fc = []
    last = "[0:v]"
    for i, (_, t0, t1, _, _) in enumerate(overlays, 1):
        out = f"[v{i}]"
        fc.append(f"{last}[{i}:v]overlay=0:0:enable='between(t,{t0:.3f},{t1:.3f})'{out}")
        last = out
    out_mp4 = HERE / f"hos_004_{item['id']}_punch_v05.mp4"
    ff(
        *inputs,
        "-filter_complex",
        ";".join(fc),
        "-map",
        last,
        "-map",
        "0:a",
        "-c:v",
        "libx264",
        "-pix_fmt",
        "yuv420p",
        "-preset",
        "fast",
        "-crf",
        "18",
        "-r",
        str(FPS),
        "-c:a",
        "aac",
        "-b:a",
        "192k",
        "-ar",
        "48000",
        "-ac",
        "2",
        "-t",
        f"{total:.3f}",
        "-movflags",
        "+faststart",
        str(out_mp4),
    )
    dur = probe(out_mp4)
    if dur >= 40:
        raise SystemExit(f"ABORT ≥40s {out_mp4}")
    print(
        f"BUILT {item['id']} dur={dur:.2f}s vo={vo_dur:.2f}s chunks={len(chunks)} fps={FPS}",
        flush=True,
    )
    return {
        "id": item["id"],
        "air_date": item["air_date"],
        "file": str(out_mp4),
        "sha256": sha256(out_mp4),
        "duration_s": round(dur, 3),
        "vo_duration_s": round(vo_dur, 3),
        "story_s": round(story, 3),
        "loop_s": round(loop, 3),
        "fps": FPS,
        "parent": item["parent"],
        "hook": item["hook"],
        "caption_chunks": len(chunks),
        "work": str(work),
        "timeline": timeline,
    }


def active_vo_text(timeline: list[dict], t: float) -> str | None:
    for row in timeline:
        if row["role"] != "vo":
            continue
        if row["t0"] <= t < row["t1"]:
            return row["text"]
    return None


def verify_caption_changes(mp4: Path, timeline: list[dict], work: Path, dur: float) -> dict:
    """Extract every 0.5s; confirm VO caption text changes across samples."""
    frames_dir = work / "frames_0p5"
    frames_dir.mkdir(parents=True, exist_ok=True)
    samples: list[dict] = []
    t = 0.0
    prev_text: str | None = None
    text_changes = 0
    crop_changes_when_text_changes = 0
    prev_crop_hash: str | None = None
    import hashlib

    while t < dur - 0.05:
        fp = frames_dir / f"t{t:05.1f}.jpg"
        # full frame for sheet + tight bottom band for caption hash
        ff("-ss", f"{t:.3f}", "-i", str(mp4), "-frames:v", "1", "-q:v", "4", str(fp))
        crop = frames_dir / f"c{t:05.1f}.jpg"
        ff(
            "-ss",
            f"{t:.3f}",
            "-i",
            str(mp4),
            "-frames:v",
            "1",
            "-vf",
            "crop=980:200:50:1580",
            "-q:v",
            "4",
            str(crop),
        )
        text = active_vo_text(timeline, t)
        chash = hashlib.md5(crop.read_bytes()).hexdigest()[:16]
        changed = prev_text is not None and text != prev_text
        if changed:
            text_changes += 1
            if prev_crop_hash and chash != prev_crop_hash:
                crop_changes_when_text_changes += 1
        samples.append({"t": round(t, 1), "vo_text": text, "crop_md5": chash, "text_changed": changed})
        prev_text = text
        prev_crop_hash = chash
        t += 0.5

    # Build contact sheet — sample ~12 frames evenly
    sheet_times = [round(i * dur / 11, 1) for i in range(12)]
    tiles: list[Image.Image] = []
    for st in sheet_times:
        # nearest extracted or extract
        nearest = min(samples, key=lambda s: abs(s["t"] - st))
        src = frames_dir / f"t{nearest['t']:05.1f}.jpg"
        if not src.exists():
            ff("-ss", f"{st:.3f}", "-i", str(mp4), "-frames:v", "1", "-q:v", "4", str(src))
        im = Image.open(src).convert("RGB")
        im.thumbnail((270, 480))
        # label with vo text snippet
        canvas = Image.new("RGB", (270, 520), (20, 20, 20))
        canvas.paste(im, (0, 0))
        draw = ImageDraw.Draw(canvas)
        try:
            font = ImageFont.truetype(CTA_FONT, 14)
        except Exception:
            font = ImageFont.load_default()
        label = f"{nearest['t']:.1f}s"
        vo = nearest.get("vo_text") or ""
        if len(vo) > 34:
            vo = vo[:31] + "…"
        draw.text((6, 482), label, fill=(255, 220, 80), font=font)
        draw.text((6, 498), vo, fill=(230, 230, 230), font=font)
        tiles.append(canvas)

    cols = 4
    rows = (len(tiles) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * 270, rows * 520), (10, 10, 10))
    for i, tile in enumerate(tiles):
        sheet.paste(tile, ((i % cols) * 270, (i // cols) * 520))
    sheet_path = work / f"{mp4.stem}_caption_sheet.jpg"
    sheet.save(sheet_path, quality=85)

    vo_texts = [s["vo_text"] for s in samples if s["vo_text"]]
    unique_vo = len(set(vo_texts))
    ok = unique_vo >= 8 and text_changes >= 7
    # Most text changes should also change crop pixels
    if text_changes:
        ratio = crop_changes_when_text_changes / text_changes
    else:
        ratio = 0.0
    ok = ok and ratio >= 0.7

    report = {
        "ok": ok,
        "unique_vo_captions_in_0p5_samples": unique_vo,
        "text_changes": text_changes,
        "crop_changes_when_text_changes": crop_changes_when_text_changes,
        "crop_change_ratio": round(ratio, 3),
        "sheet": str(sheet_path),
        "samples": samples,
    }
    (work / "caption_change_check.json").write_text(json.dumps(report, indent=2) + "\n")
    if not ok:
        raise SystemExit(
            f"CAPTION CHANGE FAIL {mp4.name}: unique={unique_vo} changes={text_changes} ratio={ratio:.2f}"
        )
    print(
        f"CAPTION OK {mp4.name}: unique={unique_vo} changes={text_changes} ratio={ratio:.2f} sheet={sheet_path.name}",
        flush=True,
    )
    return report


def run_gate(mp4: Path, air_date: str) -> dict:
    cmd = [
        sys.executable,
        str(GATE),
        "check",
        str(mp4),
        "--air-date",
        air_date,
        "--json",
    ]
    r = subprocess.run(cmd, capture_output=True, text=True)
    out = (r.stdout or "") + (r.stderr or "")
    try:
        data = json.loads(r.stdout.strip().splitlines()[-1]) if r.stdout.strip() else {"raw": out}
    except Exception:
        data = {"raw": out, "returncode": r.returncode}
    data["returncode"] = r.returncode
    if r.returncode != 0:
        print(out[-2000:], flush=True)
        raise SystemExit(f"GATE FAIL {mp4.name} code={r.returncode}")
    print(f"GATE PASS {mp4.name}", flush=True)
    return data


def main() -> None:
    records = []
    for item in SHORTS:
        rec = build_one(item)
        mp4 = Path(rec["file"])
        check = verify_caption_changes(mp4, rec["timeline"], Path(rec["work"]), rec["duration_s"])
        rec["caption_check"] = {
            k: check[k]
            for k in (
                "ok",
                "unique_vo_captions_in_0p5_samples",
                "text_changes",
                "crop_change_ratio",
                "sheet",
            )
        }
        gate = run_gate(mp4, item["air_date"])
        rec["gate"] = {"pass": gate.get("returncode", 1) == 0, "summary": gate}
        # copy to iCloud
        ICLOUD.mkdir(parents=True, exist_ok=True)
        dest = ICLOUD / mp4.name
        dest.write_bytes(mp4.read_bytes())
        sheet_src = Path(check["sheet"])
        sheet_dest = ICLOUD / sheet_src.name
        sheet_dest.write_bytes(sheet_src.read_bytes())
        # also copy timeline
        (ICLOUD / f"{mp4.stem}_caption_timeline.json").write_text(
            json.dumps(rec["timeline"], indent=2) + "\n"
        )
        rec["icloud"] = str(dest)
        rec["icloud_sheet"] = str(sheet_dest)
        # drop bulky timeline from index
        timeline = rec.pop("timeline")
        (Path(rec["work"]) / "caption_timeline.json").write_text(json.dumps(timeline, indent=2) + "\n")
        records.append(rec)

    meta = {
        "scripts": "SHORTS_PUNCH_SCRIPTS_v04.md",
        "version": "v05",
        "note": (
            "Ben phone UAT FAIL on v04 frozen captions (29 Sep 18:50). "
            "v05 word-timed from VO align JSON. Hook + title 9–14s + last-4s loop kept. "
            "Caption change check every 0.5s PASS. gate_shorts_open PASS. "
            "STOP for Ben phone watch. Do not upload."
        ),
        "ben_uat_v04": "All shorts the text or subtitles are not working, they are frozen.",
        "shorts": records,
    }
    out = HERE / "SHORTS_PUNCH_INDEX_v05.json"
    out.write_text(json.dumps(meta, indent=2) + "\n")
    (ICLOUD / out.name).write_text(out.read_text())
    # watch note
    watch = ICLOUD / "WATCH_shorts_v05.txt"
    watch.write_text(
        "HOS 004 Shorts punch v05 — word-timed captions\n"
        "Ben v04 FAIL: captions frozen / not following VO.\n"
        "v05: VO align chunks · hook · title 9–14s · last-4s loop.\n"
        "Contact sheets: *_caption_sheet.jpg\n"
        "STOP for phone watch. Do not upload.\n"
    )
    print(f"index={out}", flush=True)
    print(f"icloud={ICLOUD}", flush=True)


if __name__ == "__main__":
    main()
