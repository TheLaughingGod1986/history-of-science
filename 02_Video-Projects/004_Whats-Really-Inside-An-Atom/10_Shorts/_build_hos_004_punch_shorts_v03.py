#!/usr/bin/env python3
"""Punch 3 HOS 004 release-week Shorts from plates + dedicated VO v03.

Ben PASS scripts. Picture rules:
  S01 (Fri→004): coin, atom, nucleus ONLY — no stadium plates.
  S02 (Sun→002): Newlands / octave plates from 002.
  S03 (Tue→003): Bertha hand / ring plates from 003.

1080×1920. Captions. Last ~4s open loop. Zero /go/. Do not upload.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
VENV_DIR = Path(
    "/Users/benjaminoats/YouTube/History Of Science/"
    "02_Video-Projects/001_How-Did-We-Discover-Germs/10_Shorts/_venv"
)
VENV_PY = VENV_DIR / "bin" / "python"
if VENV_DIR.exists() and Path(sys.prefix) != VENV_DIR:
    os.execv(str(VENV_PY), [str(VENV_PY), *sys.argv])

from PIL import Image, ImageDraw, ImageFont  # noqa: E402

REPO = HERE.parents[2]
PROJ = HERE.parent
PROJ002 = REPO / "02_Video-Projects/002_How-Did-We-Discover-The-Periodic-Table"
PROJ003 = REPO / "02_Video-Projects/003_Invisible-Bones-X-Rays"
OUT_DIR = HERE
ICLOUD = Path.home() / (
    "Library/Mobile Documents/com~apple~CloudDocs/HOS UAT/"
    "004_Whats-Really-Inside-An-Atom/10_Shorts"
)
FONT = "/System/Library/Fonts/Supplemental/Didot.ttc"
CTA_FONT = "/System/Library/Fonts/Supplemental/Times New Roman.ttf"
W, H = 1080, 1920
CREAM = (245, 232, 210, 255)
INK = (28, 26, 28, 255)
HOOK_YELLOW = (255, 214, 70, 255)

VF_916 = (
    "scale=1920:1080,"
    "crop=608:1080:656:0,"
    "scale=1080:1920:flags=lanczos,"
    "setsar=1"
)

# Trim Veo ease-in (~0.4s) so frame 0 is mid-action.
EASE = 0.40

SHORTS = [
    {
        "id": "s01_how_small",
        "slot": "Fri 16 Oct 2026 11:30 Europe/London",
        "air_date": "2026-10-16",
        "title": "How small can you cut gold?",
        "hook": "HOW SMALL?",
        "line": "Cut a gold coin in half. Then again.",
        "parent": "What's Really Inside an Atom?",
        "parent_id": None,
        "vo": HERE / "vo_v03/hos_004_s01_how_small_vo_v03.wav",
        "plates": [
            # coin → atom → nucleus ONLY (Ben: NO stadium)
            PROJ / "04_Generated-Clips/part01/raw/v01/01_coin_halves_v01.mp4",
            PROJ / "04_Generated-Clips/part01/raw/v01/02_atom_answer_v01.mp4",
            PROJ / "04_Generated-Clips/part01/raw/v01/03_atom_turns_v01.mp4",
            PROJ / "04_Generated-Clips/part04/raw/v01/14_nucleus_electrons_v01.mp4",
            PROJ / "04_Generated-Clips/part04/raw/v01/19_nucleus_question_v02.mp4",
        ],
        "forbid_substr": ["stadium", "pea_stadium", "explorer_stadium"],
    },
    {
        "id": "s02_every_eighth",
        "slot": "Sun 18 Oct 2026 11:30 Europe/London",
        "air_date": "2026-10-18",
        "title": "Every eighth element repeats",
        "hook": "EVERY EIGHTH?",
        "line": "Before Mendeleev, John Newlands lined the elements up like notes on a piano.",
        "parent": "How Did We Discover the Periodic Table?",
        "parent_id": "AL_-qlWko_g",
        "vo": HERE / "vo_v03/hos_004_s02_every_eighth_vo_v03.wav",
        "plates": [
            PROJ002 / "04_Generated-Clips/part02/raw/v06_kenburns/07_newlands_octave_kb_v06.mp4",
            PROJ002 / "04_Generated-Clips/part02/raw/v06_kenburns/08_piano_gag_fail_kb_v06.mp4",
            PROJ002 / "04_Generated-Clips/part02/raw/v06_kenburns/09_almost_right_kb_v06.mp4",
            PROJ002 / "04_Generated-Clips/part02/raw/v06_kenburns/10_ruler_crooked_kb_v06.mp4",
        ],
        "forbid_substr": [],
    },
    {
        "id": "s03_her_ring",
        "slot": "Tue 20 Oct 2026 11:30 Europe/London",
        "air_date": "2026-10-20",
        "title": "Bertha's ring on the first X-ray",
        "hook": "HER RING",
        "line": "The first X-ray of a person was his wife's hand.",
        "parent": "How Did We Discover X-rays?",
        "parent_id": "frP_YrNShsU",
        "vo": HERE / "vo_v03/hos_004_s03_her_ring_vo_v03.wav",
        "plates": [
            PROJ003 / "04_Generated-Clips/part04/02_hand_on_plate_v02.mp4",
            PROJ003 / "04_Generated-Clips/part04/03_bones_and_ring_v02.mp4",
            PROJ003 / "04_Generated-Clips/part04/11_proof_hold_v02.mp4",
            PROJ003 / "04_Generated-Clips/part04/04_haunted_becomes_fact_v02.mp4",
        ],
        "forbid_substr": ["cardboard", "glowing"],
    },
]


def probe(p: Path) -> float:
    r = subprocess.run(
        [
            "ffprobe", "-v", "error", "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1", str(p),
        ],
        check=True, capture_output=True, text=True,
    )
    return float(r.stdout.strip())


def ff(*args: str) -> None:
    subprocess.run(
        ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", *args], check=True
    )


def sha256(p: Path) -> str:
    import hashlib
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def wrap_text(text: str, font: ImageFont.FreeTypeFont, max_w: int) -> list[str]:
    words = text.split()
    lines: list[str] = []
    cur = ""
    for word in words:
        trial = (cur + " " + word).strip()
        if font.getlength(trial) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines or [text]


def render_caption_png(
    path: Path,
    text: str,
    size: int,
    *,
    anchor: str,
    y: int,
    font_path: str = FONT,
    fill=CREAM,
) -> None:
    font_obj = ImageFont.truetype(font_path, size)
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    max_w = W - 96
    lines = wrap_text(text, font_obj, max_w)
    heights = []
    for line in lines:
        bbox = font_obj.getbbox(line)
        heights.append(bbox[3] - bbox[1])
    gap = int(size * 0.28)
    block_h = sum(heights) + gap * (len(lines) - 1)
    if anchor == "bottom":
        top = H - y - block_h
    else:
        top = y
    cy = top
    stroke = 3
    for line, lh in zip(lines, heights):
        tw = font_obj.getlength(line)
        x = (W - tw) / 2
        for dx in range(-stroke, stroke + 1):
            for dy in range(-stroke, stroke + 1):
                if dx == 0 and dy == 0:
                    continue
                draw.text((x + dx, cy + dy), line, font=font_obj, fill=INK)
        draw.text((x, cy), line, font=font_obj, fill=fill)
        cy += lh + gap
    path.parent.mkdir(parents=True, exist_ok=True)
    img.save(path)


def encode_plate_916(src: Path, dst: Path, start: float, dur: float) -> None:
    ff(
        "-ss", f"{start:.3f}",
        "-t", f"{dur:.3f}",
        "-i", str(src),
        "-vf", VF_916,
        "-an",
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-profile:v", "high",
        "-preset", "fast", "-crf", "18", "-r", "24",
        "-movflags", "+faststart",
        str(dst),
    )


def build_picture_bed(item: dict, work: Path, need: float) -> Path:
    plates = list(item["plates"])
    for p in plates:
        if not p.exists():
            raise SystemExit(f"STOP: missing plate {p}")
        low = str(p).lower()
        for bad in item.get("forbid_substr") or []:
            if bad.lower() in low:
                raise SystemExit(f"STOP: forbidden plate {p} matches {bad}")
    # Usable per plate after ease trim (~7.2s of 8s)
    usable = []
    for p in plates:
        d = probe(p)
        u = max(0.5, d - EASE - 0.3)
        usable.append((p, u))
    # Cycle unique plates to cover need (never freeze-pad; never stadium)
    segs: list[Path] = []
    covered = 0.0
    idx = 0
    while covered < need - 0.05:
        if idx >= len(usable) * 3:
            raise SystemExit(f"{item['id']}: not enough unique motion for {need:.1f}s")
        p, u = usable[idx % len(usable)]
        take = min(u, need - covered)
        # Prefer first ~take from after ease-in; if revisiting, offset into plate
        revisit = idx // len(usable)
        start = EASE + min(0.8 * revisit, max(0.0, u - take))
        out = work / f"seg_{idx:02d}.mp4"
        encode_plate_916(p, out, start, take)
        segs.append(out)
        covered += take
        idx += 1
    concat_txt = work / "pic_concat.txt"
    concat_txt.write_text("".join(f"file '{s.name}'\n" for s in segs))
    pic = work / "picture.mp4"
    subprocess.run(
        [
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            "-f", "concat", "-safe", "0", "-i", str(concat_txt),
            "-c", "copy", str(pic),
        ],
        check=True, cwd=work,
    )
    # Hard trim to exact need
    trim = work / "picture_trim.mp4"
    ff(
        "-i", str(pic), "-t", f"{need:.3f}",
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "fast", "-crf", "18", "-r", "24",
        "-an", str(trim),
    )
    return trim


def loop_open_clip(open_src: Path, dst: Path, loop: float) -> None:
    # Re-encode open plate window as silent loop tail
    encode_plate_916(open_src, dst, EASE, loop)


def caption_pngs(work: Path, item: dict, total: float) -> list[tuple[Path, float, float]]:
    hook_png = work / "cap_hook.png"
    line_png = work / "cap_line.png"
    title_png = work / "cap_title.png"
    cta_png = work / "cap_cta.png"
    render_caption_png(hook_png, item["hook"], 64, anchor="top", y=160, fill=HOOK_YELLOW)
    render_caption_png(line_png, item["line"], 44, anchor="bottom", y=300)
    render_caption_png(title_png, item["parent"], 34, anchor="top", y=220)
    render_caption_png(
        cta_png, "watch the full film →", 40, anchor="bottom", y=240, font_path=CTA_FONT
    )
    cta_in = max(total - 4.0, 14.4)
    return [
        (hook_png, 0.00, 3.20),
        (line_png, 0.20, cta_in - 0.10),
        (title_png, 9.00, 14.00),
        (cta_png, cta_in, total - 0.12),
    ]


def fit_story_and_loop(vo_dur: float) -> tuple[float, float, float]:
    """Return (story_pic, loop, total) in 22–27 band.

    Story carries VO; last ~4s is a silent open-picture loop.
    """
    loop = 4.0
    story = vo_dur
    total = story + loop
    if total > 27.0:
        over = total - 27.0
        cut_loop = min(over, max(0.0, loop - 3.5))
        loop -= cut_loop
        over -= cut_loop
        if over > 0:
            story = max(18.0, story - over)
        total = story + loop
    if total < 22.0:
        story = 22.0 - loop
        total = 22.0
    if not (22.0 <= total <= 27.05):
        raise SystemExit(f"cannot fit vo={vo_dur:.2f} into 22–27 (got {total:.2f})")
    return story, loop, total


def build_one(item: dict) -> dict:
    vo = Path(item["vo"])
    if not vo.exists():
        raise SystemExit(f"STOP: missing VO {vo}")
    vo_dur = probe(vo)
    story, loop, total = fit_story_and_loop(vo_dur)
    work = OUT_DIR / "_work_v03" / item["id"]
    work.mkdir(parents=True, exist_ok=True)

    pic = build_picture_bed(item, work, story)
    open_plate = item["plates"][0]
    loop_mp4 = work / "loop.mp4"
    loop_open_clip(open_plate, loop_mp4, loop)

    # Mix: picture + VO (trim/pad VO to story), then silent loop
    story_av = work / "story_av.mp4"
    # Pad or trim VO to story length
    vo_fit = work / "vo_fit.wav"
    if vo_dur < story:
        pad = story - vo_dur
        ff(
            "-i", str(vo),
            "-af", f"apad=pad_dur={pad:.3f}",
            "-t", f"{story:.3f}",
            "-ar", "48000", "-ac", "2",
            str(vo_fit),
        )
    else:
        ff(
            "-i", str(vo),
            "-t", f"{story:.3f}",
            "-ar", "48000", "-ac", "2",
            str(vo_fit),
        )
    ff(
        "-i", str(pic),
        "-i", str(vo_fit),
        "-map", "0:v", "-map", "1:a",
        "-c:v", "copy",
        "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2",
        "-shortest",
        str(story_av),
    )
    # Silent audio on loop
    loop_av = work / "loop_av.mp4"
    ff(
        "-i", str(loop_mp4),
        "-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo",
        "-shortest",
        "-c:v", "copy",
        "-c:a", "aac", "-b:a", "192k",
        str(loop_av),
    )
    concat_txt = work / "av_concat.txt"
    concat_txt.write_text(f"file '{story_av.name}'\nfile '{loop_av.name}'\n")
    raw = work / "raw.mp4"
    subprocess.run(
        [
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            "-f", "concat", "-safe", "0", "-i", str(concat_txt),
            "-c", "copy", str(raw),
        ],
        check=True, cwd=work,
    )

    overlays = caption_pngs(work, item, total)
    inputs: list[str] = ["-i", str(raw)]
    for png, _, _ in overlays:
        inputs += ["-loop", "1", "-i", str(png)]
    fc_parts = []
    last = "[0:v]"
    for i, (_, t0, t1) in enumerate(overlays, start=1):
        out = f"[v{i}]"
        fc_parts.append(
            f"{last}[{i}:v]overlay=0:0:enable='between(t,{t0:.3f},{t1:.3f})'{out}"
        )
        last = out
    fc = ";".join(fc_parts)
    out_mp4 = OUT_DIR / f"hos_004_{item['id']}_punch_v03.mp4"
    ff(
        *inputs,
        "-filter_complex", fc,
        "-map", last, "-map", "0:a",
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "fast", "-crf", "18", "-r", "24",
        "-c:a", "aac", "-b:a", "192k",
        "-t", f"{total:.3f}",
        "-movflags", "+faststart",
        str(out_mp4),
    )
    dur = probe(out_mp4)
    if dur >= 40:
        raise SystemExit(f"ABORT ≥40s: {out_mp4} {dur}")
    if not (22.0 <= dur <= 27.5):
        print(f"WARN duration {dur:.2f}s outside 22–27 for {item['id']}", flush=True)

    ICLOUD.mkdir(parents=True, exist_ok=True)
    icloud_dst = ICLOUD / out_mp4.name
    icloud_dst.write_bytes(out_mp4.read_bytes())

    rec = {
        "id": item["id"],
        "slot": item["slot"],
        "air_date": item["air_date"],
        "title": item["title"],
        "parent": item["parent"],
        "parent_id": item["parent_id"],
        "file": str(out_mp4),
        "icloud": str(icloud_dst),
        "sha256": sha256(out_mp4),
        "duration_s": round(dur, 3),
        "vo_duration_s": round(vo_dur, 3),
        "story_s": round(story, 3),
        "loop_s": round(loop, 3),
        "plates": [str(p) for p in item["plates"]],
    }
    print(
        f"BUILT {item['id']} dur={dur:.2f}s vo={vo_dur:.2f}s → {out_mp4.name}",
        flush=True,
    )
    return rec


def main() -> None:
    records = [build_one(item) for item in SHORTS]
    meta = {
        "scripts": "SHORTS_PUNCH_SCRIPTS_v03.md",
        "version": "v03",
        "note": "Ben PASS edits. S01 picture coin/atom/nucleus only — no stadium. Do not upload.",
        "shorts": records,
    }
    out = OUT_DIR / "SHORTS_PUNCH_INDEX_v03.json"
    out.write_text(json.dumps(meta, indent=2) + "\n")
    print(f"index={out}", flush=True)


if __name__ == "__main__":
    main()
