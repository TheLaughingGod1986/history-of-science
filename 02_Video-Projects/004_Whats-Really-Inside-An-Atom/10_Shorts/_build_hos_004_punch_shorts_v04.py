#!/usr/bin/env python3
"""HOS 004 Shorts punch v04 — 30 fps CFR · quiet bed · captions · Ben PASS scripts.

Reuse S01/S03 VO; S02 VO is v04 ("Davy Medal for it.").
S01 picture: coin/atom/nucleus only — no stadium.
Do not upload.
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
BED_VOL = 0.07  # quiet under VO

SHORTS = [
    {
        "id": "s01_how_small",
        "air_date": "2026-10-16",
        "hook": "HOW SMALL?",
        "parent": "What's Really Inside an Atom?",
        "vo": HERE / "vo_v03/hos_004_s01_how_small_vo_v03.wav",
        "caption_lines": [
            "Cut a gold coin in half. Then again.",
            "How small can you go before it stops being gold?",
            "A gold atom is mostly empty — its nucleus is like a pea in a stadium.",
            "Keep going and you find what everything is made of —",
            "and why the periodic table is in the order it is.",
            "Watch What's Really Inside an Atom?",
        ],
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
        "caption_lines": [
            "Before Mendeleev, John Newlands lined the elements up like notes on a piano.",
            "He said every eighth element repeats — the law of octaves.",
            "Other chemists laughed at him for comparing chemistry to music.",
            "He was nearly right. Twenty-two years later, the Royal Society gave him the Davy Medal for it.",
            "Watch How Did We Discover the Periodic Table?",
        ],
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
        "caption_lines": [
            "The first X-ray of a person was his wife's hand.",
            "Bertha Röntgen held still while the plate recorded her bones —",
            "and her wedding ring sat clear around the living bone.",
            "That single plate proved you could see inside a living body without a knife.",
            "She held still for fifteen minutes, in December eighteen ninety-five.",
            "Watch How Did We Discover X-rays?",
        ],
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


def render(path: Path, text: str, size: int, anchor: str, y: int, font_path=FONT, fill=CREAM) -> None:
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
    """Return (picture_trim, open_src_for_loop_encode_args via open clip path)."""
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
    # open loop clip
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
        # loop bed quietly under VO
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


def caption_overlays(work: Path, item: dict, story: float, total: float) -> list[tuple[Path, float, float]]:
    lines = item["caption_lines"]
    n = len(lines)
    # distribute caption lines across story (not the silent loop)
    slot = story / n
    overlays: list[tuple[Path, float, float]] = []
    hook = work / "cap_hook.png"
    render(hook, item["hook"], 64, "top", 160, fill=YEL)
    overlays.append((hook, 0.0, min(3.2, story * 0.2)))
    for i, line in enumerate(lines):
        png = work / f"cap_line_{i:02d}.png"
        render(png, line, 42, "bottom", 300)
        t0 = i * slot
        t1 = min(story - 0.05, (i + 1) * slot)
        if i == 0:
            t0 = 0.15
        overlays.append((png, t0, t1))
    title = work / "cap_title.png"
    render(title, item["parent"], 34, "top", 220)
    overlays.append((title, min(9.0, story * 0.4), min(14.0, story * 0.65)))
    cta = work / "cap_cta.png"
    render(cta, "watch the full film →", 40, "bottom", 240, font_path=CTA_FONT)
    cta_in = max(total - 4.0, 14.4)
    overlays.append((cta, cta_in, total - 0.12))
    return overlays


def build_one(item: dict) -> dict:
    vo = Path(item["vo"])
    if not vo.exists():
        raise SystemExit(f"missing VO {vo}")
    vo_dur = probe(vo)
    story, loop, total = fit_story_loop(vo_dur)
    work = HERE / "_work_v04" / item["id"]
    work.mkdir(parents=True, exist_ok=True)

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

    # silent open loop at 30fps
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

    overlays = caption_overlays(work, item, story, total)
    inputs: list[str] = ["-i", str(raw)]
    for png, _, _ in overlays:
        inputs += ["-loop", "1", "-i", str(png)]
    fc = []
    last = "[0:v]"
    for i, (_, t0, t1) in enumerate(overlays, 1):
        out = f"[v{i}]"
        fc.append(f"{last}[{i}:v]overlay=0:0:enable='between(t,{t0:.3f},{t1:.3f})'{out}")
        last = out
    out_mp4 = HERE / f"hos_004_{item['id']}_punch_v04.mp4"
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
    print(f"BUILT {item['id']} dur={dur:.2f}s vo={vo_dur:.2f}s fps={FPS}", flush=True)
    ICLOUD.mkdir(parents=True, exist_ok=True)
    (ICLOUD / out_mp4.name).write_bytes(out_mp4.read_bytes())
    return {
        "id": item["id"],
        "air_date": item["air_date"],
        "file": str(out_mp4),
        "icloud": str(ICLOUD / out_mp4.name),
        "sha256": sha256(out_mp4),
        "duration_s": round(dur, 3),
        "vo_duration_s": round(vo_dur, 3),
        "fps": FPS,
        "parent": item["parent"],
        "hook": item["hook"],
    }


def main() -> None:
    records = [build_one(s) for s in SHORTS]
    meta = {
        "scripts": "SHORTS_PUNCH_SCRIPTS_v04.md",
        "version": "v04",
        "note": "Ben PASS. S02 ends Davy Medal for it. 30fps CFR. Quiet bed. No stadium on S01. Do not upload until phone UAT.",
        "shorts": records,
    }
    out = HERE / "SHORTS_PUNCH_INDEX_v04.json"
    out.write_text(json.dumps(meta, indent=2) + "\n")
    (ICLOUD / out.name).write_text(out.read_text())
    print(f"index={out}", flush=True)


if __name__ == "__main__":
    main()
