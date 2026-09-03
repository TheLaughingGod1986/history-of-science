#!/usr/bin/env python3
"""TEXT ONLY recut — Showrunner TYPE lock. Do not remint picture. Do not rewrite VO.

Phone-huge HOLD card: yellow hook + white rest. One card per Short.
Orbit house: Arial Black, #FFE600 / #FFFFFF, centre-safe. Not Didot bottom serif.
s01–s04 → punch_v02. s05 → punch_v03 (v02 picture HOLDS). Export 10_Shorts + iCloud HOS UAT.
Do not upload. Do not click phone verify. Related still _C92tIJCk8A.
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
VENV_DIR = HERE / "_venv"
VENV_PY = VENV_DIR / "bin" / "python"
if VENV_DIR.exists() and Path(sys.prefix) != VENV_DIR:
    os.execv(str(VENV_PY), [str(VENV_PY), *sys.argv])

from PIL import Image, ImageDraw, ImageFilter, ImageFont  # noqa: E402

W, H = 1080, 1920
YELLOW = (255, 230, 0, 255)  # #FFE600
WHITE = (255, 255, 255, 255)
STROKE = (10, 12, 18, 255)
SHADOW = (0, 0, 0, 200)
FONT_PATH = Path("/System/Library/Fonts/Supplemental/Arial Black.ttf")
CTA = "watch the full film →"
PARENT_ID = "_C92tIJCk8A"
ICLOUD = Path(
    "/Users/benjaminoats/Library/Mobile Documents/com~apple~CloudDocs/HOS UAT"
)

# Showrunner TYPE lock — exact case. One card. No extra slogans.
SHORTS = [
    {
        "id": "s01_shadow",
        "raw": HERE / "_work/s01_shadow/raw.mp4",
        "out": HERE / "hos_001_s01_shadow_punch_v02.mp4",
        "title": "An enemy that does not cast a shadow",
        "yellow": "How do you fight",
        "white": "an enemy that does not cast a shadow?",
    },
    {
        "id": "s02_pond",
        "raw": HERE / "_work/s02_pond/raw.mp4",
        "out": HERE / "hos_001_s02_pond_punch_v02.mp4",
        "title": "A drop of pond water is not empty",
        "yellow": "A drop of pond water",
        "white": "is not empty",
    },
    {
        "id": "s03_vector",
        "raw": HERE / "_work/s03_vector/raw.mp4",
        "out": HERE / "hos_001_s03_vector_punch_v02.mp4",
        "title": "You are the vector",
        "yellow": "You are",
        "white": "the vector",
    },
    {
        "id": "s04_flask",
        "raw": HERE / "_work/s04_flask/raw.mp4",
        "out": HERE / "hos_001_s04_flask_punch_v02.mp4",
        "title": "A flask shaped like a question mark",
        "yellow": "A flask",
        "white": "shaped like a question mark",
    },
    {
        "id": "s05_soap",
        "raw": HERE / "_work/s05_soap_v02/raw.mp4",
        "out": HERE / "hos_001_s05_soap_punch_v03.mp4",
        "title": "What else is still invisible?",
        "yellow": "What else",
        "white": "is still invisible?",
    },
]


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


def font(size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(str(FONT_PATH), size)


def wrap(text: str, fnt: ImageFont.FreeTypeFont, max_w: int) -> list[str]:
    words = text.split()
    lines: list[str] = []
    cur = ""
    for word in words:
        trial = (cur + " " + word).strip()
        if fnt.getlength(trial) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines or [text]


def measure(draw: ImageDraw.ImageDraw, text: str, fnt: ImageFont.FreeTypeFont) -> tuple[int, int]:
    bbox = draw.textbbox((0, 0), text, font=fnt, stroke_width=0)
    return bbox[2] - bbox[0], bbox[3] - bbox[1]


def render_card(path: Path, yellow: str, white: str) -> None:
    """One HOLD card. Yellow hook, then white rest. Sentence case as locked."""
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    probe_draw = ImageDraw.Draw(img)
    max_w = W - 96
    # Phone-huge. Shrink only if a single word still overflows after wrap.
    size = 96
    lines: list[tuple[str, tuple[int, int, int, int]]] = []
    heights: list[int] = []
    while size >= 56:
        fnt = font(size)
        yellow_lines = wrap(yellow, fnt, max_w)
        white_lines = wrap(white, fnt, max_w)
        trial: list[tuple[str, tuple[int, int, int, int]]] = []
        hs: list[int] = []
        overflow = False
        for piece, color in (
            *[(ln, YELLOW) for ln in yellow_lines],
            *[(ln, WHITE) for ln in white_lines],
        ):
            if fnt.getlength(piece) > max_w:
                overflow = True
                break
            _, th = measure(probe_draw, piece, fnt)
            trial.append((piece, color))
            hs.append(th)
        if not overflow and trial and len(trial) <= 5:
            lines, heights = trial, hs
            break
        size -= 4
    if not lines:
        raise SystemExit(f"could not fit TYPE card: {yellow!r} / {white!r}")

    gap = int(size * 0.18)
    block_h = sum(heights) + gap * (len(lines) - 1)
    # Optical centre, slightly above mid — Shorts UI safe.
    y0 = 760 - block_h // 2
    y0 = max(260, min(y0, 1100 - block_h))

    shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sdraw = ImageDraw.Draw(shadow)
    fnt = font(size)
    yy = y0
    for (text, _), th in zip(lines, heights):
        tw, _ = measure(sdraw, text, fnt)
        x = (W - tw) // 2
        sdraw.text((x + 4, yy + 6), text, font=fnt, fill=SHADOW)
        yy += th + gap
    shadow = shadow.filter(ImageFilter.GaussianBlur(radius=7))
    img = Image.alpha_composite(img, shadow)

    draw = ImageDraw.Draw(img)
    yy = y0
    stroke = 5 if size >= 72 else 4
    for (text, color), th in zip(lines, heights):
        tw, _ = measure(draw, text, fnt)
        x = (W - tw) // 2
        draw.text(
            (x, yy),
            text,
            font=fnt,
            fill=color,
            stroke_width=stroke,
            stroke_fill=STROKE,
        )
        yy += th + gap

    path.parent.mkdir(parents=True, exist_ok=True)
    img.save(path)


def render_cta(path: Path) -> None:
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    fnt = font(48)
    draw = ImageDraw.Draw(img)
    tw, th = measure(draw, CTA, fnt)
    x = (W - tw) // 2
    y = 1560
    shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sdraw = ImageDraw.Draw(shadow)
    sdraw.text((x + 3, y + 5), CTA, font=fnt, fill=SHADOW)
    shadow = shadow.filter(ImageFilter.GaussianBlur(radius=5))
    img = Image.alpha_composite(img, shadow)
    draw = ImageDraw.Draw(img)
    draw.text((x, y), CTA, font=fnt, fill=WHITE, stroke_width=3, stroke_fill=STROKE)
    img.save(path)


def overlay(raw: Path, card: Path, cta: Path, out: Path, total: float) -> None:
    cta_in = max(total - 4.0, 14.0)
    hold_end = cta_in - 0.08
    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-hide_banner",
            "-loglevel",
            "error",
            "-i",
            str(raw),
            "-loop",
            "1",
            "-i",
            str(card),
            "-loop",
            "1",
            "-i",
            str(cta),
            "-filter_complex",
            f"[0:v][1:v]overlay=0:0:enable='between(t,0.12,{hold_end:.3f})'[a];"
            f"[a][2:v]overlay=0:0:enable='between(t,{cta_in:.3f},{total - 0.04:.3f})'[v]",
            "-map",
            "[v]",
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
            "copy",
            "-t",
            f"{total:.3f}",
            "-shortest",
            "-movflags",
            "+faststart",
            str(out),
        ],
        check=True,
    )


def main() -> None:
    if not FONT_PATH.exists():
        raise SystemExit("Arial Black missing — abort")
    ICLOUD.mkdir(parents=True, exist_ok=True)
    work = HERE / "_work" / "type_v02"
    work.mkdir(parents=True, exist_ok=True)
    results = []
    for item in SHORTS:
        raw = item["raw"]
        if not raw.exists():
            raise SystemExit(f"missing raw picture (do not remint): {raw}")
        total = probe(raw)
        if total < 22.0 or total >= 28.0:
            raise SystemExit(f"{item['id']} raw {total:.2f}s — abort")
        card = work / f"{item['id']}_card.png"
        cta = work / f"{item['id']}_cta.png"
        render_card(card, item["yellow"], item["white"])
        render_cta(cta)
        out = item["out"]
        overlay(raw, card, cta, out, total)
        dur = probe(out)
        if dur < 22.0 or dur >= 28.0 or dur >= 40.0:
            raise SystemExit(f"{item['id']} exported {dur:.2f}s — abort")
        dest = ICLOUD / out.name
        dest.write_bytes(out.read_bytes())
        print(f"OK {item['id']} {dur:.2f}s → {out.name}", flush=True)
        results.append({**item, "duration": dur, "file": out.name})

    index_path = HERE / "SHORTS_PUNCH_INDEX_v01.json"
    index = json.loads(index_path.read_text())
    index["note"] = (
        "TYPE recut STOP for UAT. Yellow hook + white rest HOLD. "
        "Do not upload until PASS. Do not remint. Do not click phone verify. "
        "Related still _C92tIJCk8A. Zero /go/. Scheduled listings wait."
    )
    index["typeLock"] = "showrunner-2026-09-02"
    by_id = {it["id"]: it for it in index["items"]}
    for item, res in zip(SHORTS, results):
        row = by_id[item["id"]]
        row["file"] = res["file"]
        row["duration"] = res["duration"]
        row["status"] = "UAT"
        row["locked"] = False
        row["type"] = {"yellow": item["yellow"], "white": item["white"]}
        row["relatedVideoId"] = PARENT_ID
        row["go"] = None
        row["relatedApplied"] = False
        row["uat"] = (
            "TEXT ONLY TYPE recut. Picture/VO unchanged. "
            "One HOLD card. Last ~4s CTA. Stop for UAT."
        )
    index_path.write_text(json.dumps(index, indent=2) + "\n")
    shutil.copy2(index_path, ICLOUD / index_path.name)


if __name__ == "__main__":
    main()
