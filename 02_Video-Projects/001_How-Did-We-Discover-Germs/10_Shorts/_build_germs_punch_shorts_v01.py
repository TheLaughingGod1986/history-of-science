#!/usr/bin/env python3
"""Punch 5 Shorts from hos_001_germs_full_v02.mp4. No remint. Not LOCKED.

Related target: _C92tIJCk8A. Zero /go/. Export to 10_Shorts + iCloud HOS UAT.
Captions via Pillow PNG + ffmpeg overlay (this ffmpeg has no drawtext/libass).
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
VENV_DIR = HERE / "_venv"
VENV_PY = VENV_DIR / "bin" / "python"
if VENV_DIR.exists() and Path(sys.prefix) != VENV_DIR:
    os.execv(str(VENV_PY), [str(VENV_PY), *sys.argv])

from PIL import Image, ImageDraw, ImageFont  # noqa: E402

PROJ = HERE.parent
SRC = PROJ / "09_Final-Export/hos_001_germs_full_v02.mp4"
SHA = "f49fae7872e9ae16d76e76d01e00444e6fa6159956ee0375fb1df8234d9df195"
OUT_DIR = HERE
ICLOUD = Path(
    "/Users/benjaminoats/Library/Mobile Documents/com~apple~CloudDocs/HOS UAT"
)
FONT = "/System/Library/Fonts/Supplemental/Didot.ttc"
CTA_FONT = "/System/Library/Fonts/Supplemental/Times New Roman.ttf"

P03 = 159.877
P04 = 230.765
P05 = 313.325
CARD = 359.405

PARENT = "How Did We Discover Germs?"
PARENT_ID = "_C92tIJCk8A"

# 9:16 1080x1920. Picture in 1s. 22–27s. Captions. No remint.
# Align: P03 "you are the vector" 44.820 → 204.697
#        P04 "He won with a flask" 3.093 → 233.858
#        P05 soap 31.056 → 344.381 · last question 43.264 → 356.589
SHORTS = [
    {
        "id": "s01_shadow",
        "slot": "Fri 4 Sep 2026 11:30 Europe/London",
        "title": "An enemy that does not cast a shadow",
        "line": "So how do you fight an enemy that does not cast a shadow?",
        "start": 74.10,
        "end": 80.05,
        # Unique earlier death-ward motion (not the hook window). Silent fill.
        "fill_start": 18.00,
        "fill_dur": 14.2,
        "hold": 0.0,
        "loop_open": True,
    },
    {
        "id": "s02_pond",
        "slot": "Sat 5 Sep 2026 11:30 Europe/London",
        "title": "A drop of pond water is not empty",
        "line": "A drop of pond water is not empty.",
        "start": 80.14,
        "end": 100.64,
        "hold": 0.0,
        "loop_open": True,
    },
    {
        "id": "s03_vector",
        "slot": "Sun 6 Sep 2026 11:30 Europe/London",
        "title": "You are the vector",
        "line": "You are the vector.",
        "start": 203.20,
        "end": 223.70,
        "hold": 0.0,
        "loop_open": True,
    },
    {
        "id": "s04_flask",
        "slot": "Mon 7 Sep 2026 11:30 Europe/London",
        "title": "A flask shaped like a question mark",
        "line": "He won with a flask shaped like a question mark.",
        "start": 233.70,
        "end": 254.20,
        "hold": 0.0,
        "loop_open": True,
    },
    {
        "id": "s05_soap",
        "slot": "Tue 8 Sep 2026 11:30 Europe/London",
        "title": "What else is still invisible?",
        "line": "Every time soap meets your hands.",
        "start": 343.20,
        "end": CARD - 0.08,
        "hold": 3.5,
        "loop_open": True,
    },
]

W, H = 1080, 1920
CREAM = (245, 232, 210, 255)
INK = (28, 26, 28, 255)
VF_916 = (
    "scale=1920:1080,"
    "crop=608:1080:656:0,"
    "scale=1080:1920:flags=lanczos,"
    "setsar=1"
)


def sha256(p: Path) -> str:
    import hashlib

    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def probe(p: Path) -> float:
    r = subprocess.run(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "default=noprint_wrappers=1:nokey=1",
            str(p),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    return float(r.stdout.strip())


def ff(*args: str) -> None:
    subprocess.run(
        ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", *args], check=True
    )


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
    path: Path, text: str, size: int, *, anchor: str, y: int, font_path: str = FONT
) -> None:
    font = ImageFont.truetype(font_path, size)
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    max_w = W - 96
    lines = wrap_text(text, font, max_w)
    heights = []
    for line in lines:
        bbox = font.getbbox(line)
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
        tw = font.getlength(line)
        x = (W - tw) / 2
        for dx in range(-stroke, stroke + 1):
            for dy in range(-stroke, stroke + 1):
                if dx == 0 and dy == 0:
                    continue
                draw.text((x + dx, cy + dy), line, font=font, fill=INK)
        draw.text((x, cy), line, font=font, fill=CREAM)
        cy += lh + gap
    path.parent.mkdir(parents=True, exist_ok=True)
    img.save(path)


def caption_pngs(work: Path, item: dict, total: float) -> list[tuple[Path, float, float]]:
    line_png = work / "cap_line.png"
    title_png = work / "cap_title.png"
    cta_png = work / "cap_cta.png"
    render_caption_png(line_png, item["line"], 52, anchor="bottom", y=280)
    render_caption_png(title_png, PARENT, 38, anchor="top", y=220)
    render_caption_png(
        cta_png,
        "watch the full film →",
        40,
        anchor="bottom",
        y=240,
        font_path=CTA_FONT,
    )
    cta_in = max(total - 4.0, 14.4)
    return [
        (line_png, 0.20, cta_in - 0.10),
        (title_png, 9.00, 14.00),
        (cta_png, cta_in, total - 0.12),
    ]


def encode_916(src: Path, dst: Path, start: float, dur: float, *, silent: bool) -> None:
    common = [
        "-ss",
        f"{start:.3f}",
        "-t",
        f"{dur:.3f}",
        "-i",
        str(src),
        "-vf",
        VF_916,
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
        "24",
        "-movflags",
        "+faststart",
    ]
    if silent:
        ff(
            *common,
            "-an",
            str(dst),
        )
        # add silent stereo so concat stays A/V aligned
        tmp = dst.with_suffix(".vid.mp4")
        dst.rename(tmp)
        ff(
            "-i",
            str(tmp),
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
            "-ar",
            "48000",
            "-ac",
            "2",
            str(dst),
        )
        tmp.unlink()
    else:
        ff(
            *common,
            "-c:a",
            "aac",
            "-b:a",
            "192k",
            "-ar",
            "48000",
            "-ac",
            "2",
            str(dst),
        )


def freeze_hold(story_mp4: Path, dst: Path, hold: float) -> None:
    ff(
        "-sseof",
        "-0.08",
        "-i",
        str(story_mp4),
        "-f",
        "lavfi",
        "-i",
        "anullsrc=r=48000:cl=stereo",
        "-filter_complex",
        f"[0:v]loop=loop=-1:size=1:start=0,trim=duration={hold:.3f},setpts=PTS-STARTPTS[v];"
        f"[1:a]atrim=0:{hold:.3f},asetpts=PTS-STARTPTS[a]",
        "-map",
        "[v]",
        "-map",
        "[a]",
        "-c:v",
        "libx264",
        "-pix_fmt",
        "yuv420p",
        "-preset",
        "fast",
        "-crf",
        "18",
        "-r",
        "24",
        "-c:a",
        "aac",
        "-b:a",
        "192k",
        str(dst),
    )


def loop_open(story_mp4: Path, dst: Path, loop: float) -> None:
    ff(
        "-i",
        str(story_mp4),
        "-f",
        "lavfi",
        "-i",
        "anullsrc=r=48000:cl=stereo",
        "-filter_complex",
        f"[0:v]trim=0:{loop:.3f},setpts=PTS-STARTPTS[v];"
        f"[1:a]atrim=0:{loop:.3f},asetpts=PTS-STARTPTS[a]",
        "-map",
        "[v]",
        "-map",
        "[a]",
        "-c:v",
        "libx264",
        "-pix_fmt",
        "yuv420p",
        "-preset",
        "fast",
        "-crf",
        "18",
        "-r",
        "24",
        "-c:a",
        "aac",
        "-b:a",
        "192k",
        str(dst),
    )


def fit_duration(story: float, hold: float, fill: float, loop: float) -> tuple[float, float, float, float]:
    total = story + hold + fill + loop
    if total < 22.0:
        fill += 22.0 - total
        total = story + hold + fill + loop
    if total > 27.0:
        over = total - 26.4
        for name in ("hold", "fill", "loop"):
            if over <= 0:
                break
            if name == "hold":
                cut = min(hold, over)
                hold -= cut
                over -= cut
            elif name == "fill":
                cut = min(max(0.0, fill - 8.0), over)
                fill -= cut
                over -= cut
            else:
                cut = min(max(0.0, loop - 3.5), over)
                loop -= cut
                over -= cut
        total = story + hold + fill + loop
    if not (22.0 <= total <= 27.05):
        raise SystemExit(f"duration {total:.2f} out of 22–27")
    return hold, fill, loop, total


def build_one(item: dict) -> Path:
    start = float(item["start"])
    end = float(item["end"])
    hold = float(item.get("hold") or 0)
    fill = float(item.get("fill_dur") or 0)
    story = end - start
    if story < 3:
        raise SystemExit(f"{item['id']}: story window too short")
    loop = 4.0 if item.get("loop_open") else 0.0
    hold, fill, loop, total = fit_duration(story, hold, fill, loop)

    work = OUT_DIR / "_work" / item["id"]
    work.mkdir(parents=True, exist_ok=True)
    story_mp4 = work / "story.mp4"
    encode_916(SRC, story_mp4, start, story, silent=False)

    parts = [story_mp4]
    if fill > 0.05:
        fill_mp4 = work / "fill.mp4"
        encode_916(
            SRC,
            fill_mp4,
            float(item["fill_start"]),
            fill,
            silent=True,
        )
        parts.append(fill_mp4)
    if hold > 0.05:
        last = work / "hold.mp4"
        freeze_hold(story_mp4, last, hold)
        parts.append(last)
    if loop > 0.05:
        head = work / "loop.mp4"
        loop_open(story_mp4, head, loop)
        parts.append(head)

    concat_txt = work / "concat.txt"
    concat_txt.write_text("".join(f"file '{p.name}'\n" for p in parts))
    raw = work / "raw.mp4"
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
            str(concat_txt),
            "-c",
            "copy",
            str(raw),
        ],
        check=True,
        cwd=work,
    )

    overlays = caption_pngs(work, item, total)
    inputs = ["-i", str(raw)]
    for png, _, _ in overlays:
        inputs += ["-loop", "1", "-i", str(png)]
    fc_parts = []
    last = "0:v"
    for i, (_, a, b) in enumerate(overlays, start=1):
        nxt = f"v{i}"
        fc_parts.append(
            f"[{last}][{i}:v]overlay=0:0:enable='between(t,{a:.2f},{b:.2f})'[{nxt}]"
        )
        last = nxt
    out = OUT_DIR / f"hos_001_{item['id']}_punch_v01.mp4"
    ff(
        *inputs,
        "-filter_complex",
        ";".join(fc_parts),
        "-map",
        f"[{last}]",
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
        "24",
        "-c:a",
        "aac",
        "-b:a",
        "192k",
        "-shortest",
        "-movflags",
        "+faststart",
        str(out),
    )
    dur = probe(out)
    if dur < 22.0 or dur >= 28.0 or dur >= 40.0:
        raise SystemExit(f"{item['id']}: exported {dur:.2f}s — abort")
    dest = ICLOUD / out.name
    dest.write_bytes(out.read_bytes())
    print(f"OK {item['id']} {dur:.2f}s → {out.name}", flush=True)
    return out


def overlay_captions(item: dict, raw: Path, total: float, out: Path) -> None:
    work = raw.parent
    overlays = caption_pngs(work, item, total)
    inputs = ["-i", str(raw)]
    for png, _, _ in overlays:
        inputs += ["-loop", "1", "-i", str(png)]
    fc_parts = []
    last = "0:v"
    for i, (_, a, b) in enumerate(overlays, start=1):
        nxt = f"v{i}"
        fc_parts.append(
            f"[{last}][{i}:v]overlay=0:0:enable='between(t,{a:.2f},{b:.2f})'[{nxt}]"
        )
        last = nxt
    ff(
        *inputs,
        "-filter_complex",
        ";".join(fc_parts),
        "-map",
        f"[{last}]",
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
        "24",
        "-c:a",
        "aac",
        "-b:a",
        "192k",
        "-t",
        f"{total:.3f}",
        "-shortest",
        "-movflags",
        "+faststart",
        str(out),
    )


def main() -> None:
    if sha256(SRC) != SHA:
        raise SystemExit("v02 sha mismatch — abort, do not remint")
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    ICLOUD.mkdir(parents=True, exist_ok=True)
    overlay_only = "--overlay-only" in sys.argv
    meta = []
    for item in SHORTS:
        if overlay_only:
            work = OUT_DIR / "_work" / item["id"]
            raw = work / "raw.mp4"
            if not raw.exists():
                raise SystemExit(f"missing {raw}")
            total = probe(raw)
            out = OUT_DIR / f"hos_001_{item['id']}_punch_v01.mp4"
            overlay_captions(item, raw, total, out)
            dur = probe(out)
            if dur < 22.0 or dur >= 28.0:
                raise SystemExit(f"{item['id']}: exported {dur:.2f}s — abort")
            (ICLOUD / out.name).write_bytes(out.read_bytes())
            print(f"OK {item['id']} {dur:.2f}s → {out.name}", flush=True)
            p = out
        else:
            p = build_one(item)
        meta.append(
            {
                **item,
                "file": p.name,
                "duration": probe(p),
                "relatedVideoId": PARENT_ID,
                "go": None,
                "status": "UAT",
                "locked": False,
            }
        )
    index = {
        "parentId": PARENT_ID,
        "parentTitle": PARENT,
        "parentUrl": f"https://youtu.be/{PARENT_ID}",
        "source": "hos_001_germs_full_v02.mp4",
        "sourceSha": SHA,
        "note": (
            "Not LOCKED. Stop for UAT. Do not upload before UAT. "
            "None before Premiere. None earlier than Fri 4 Sep 11:30 London. "
            "Related = _C92tIJCk8A only. Zero /go/."
        ),
        "schedule": [
            {
                "when": "Fri 4 Sep 2026 11:30 Europe/London",
                "id": "s01_shadow",
                "title": "An enemy that does not cast a shadow",
            },
            {
                "when": "Sat 5 Sep 2026 11:30 Europe/London",
                "id": "s02_pond",
                "title": "A drop of pond water is not empty",
            },
            {
                "when": "Sun 6 Sep 2026 11:30 Europe/London",
                "id": "s03_vector",
                "title": "You are the vector",
            },
            {
                "when": "Mon 7 Sep 2026 11:30 Europe/London",
                "id": "s04_flask",
                "title": "A flask shaped like a question mark",
            },
            {
                "when": "Tue 8 Sep 2026 11:30 Europe/London",
                "id": "s05_soap",
                "title": "What else is still invisible?",
            },
        ],
        "items": meta,
    }
    index_path = OUT_DIR / "SHORTS_PUNCH_INDEX_v01.json"
    index_path.write_text(json.dumps(index, indent=2) + "\n")
    (ICLOUD / index_path.name).write_text(index_path.read_text())


if __name__ == "__main__":
    main()
