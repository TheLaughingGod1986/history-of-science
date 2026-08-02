#!/usr/bin/env python3
"""Orbit Shorts on-screen caption renderer — finalverdict-style kinetic text.

Bold lowercase yellow/white beats, soft shadow, no brand chrome.
Used by *_shorts_v02 builders.
"""
from __future__ import annotations

from pathlib import Path
from typing import Iterable, Sequence

from PIL import Image, ImageDraw, ImageFilter, ImageFont

# Canvas
W, H = 1080, 1920

# Colors
YELLOW = (255, 230, 0, 255)  # #FFE600
WHITE = (255, 255, 255, 255)
STROKE = (10, 12, 18, 255)  # #0A0C12
SHADOW = (0, 0, 0, 190)

FONT_CANDIDATES = [
    Path("/System/Library/Fonts/Supplemental/Arial Black.ttf"),
    Path("/Library/Fonts/Arial Black.ttf"),
    Path("/System/Library/Fonts/Supplemental/Arial Bold.ttf"),
    Path("/System/Library/Fonts/Supplemental/Impact.ttf"),
]

ColorName = str  # "yellow" | "white"
LineSpec = tuple[str, ColorName]


def resolve_font(size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    for path in FONT_CANDIDATES:
        if path.exists():
            return ImageFont.truetype(str(path), size=size)
    return ImageFont.load_default()


def _rgba(name: ColorName) -> tuple[int, int, int, int]:
    return YELLOW if name == "yellow" else WHITE


def _text_size(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.ImageFont) -> tuple[int, int]:
    bbox = draw.textbbox((0, 0), text, font=font, stroke_width=0)
    return bbox[2] - bbox[0], bbox[3] - bbox[1]


def render_beat_png(
    path: Path,
    lines: Sequence[LineSpec],
    *,
    pointsize: int = 92,
    y_center: int = 780,
    line_gap: int = 18,
    shadow_blur: int = 6,
    shadow_offset: tuple[int, int] = (3, 5),
    stroke_width: int = 4,
) -> Path:
    """Render one caption beat (1–3 lowercase lines) onto a transparent 1080×1920 PNG."""
    path = Path(path)
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    font = resolve_font(pointsize)

    # Measure stack
    probe = ImageDraw.Draw(img)
    heights: list[int] = []
    widths: list[int] = []
    cleaned: list[LineSpec] = []
    for raw, color in lines:
        text = " ".join(str(raw).strip().lower().split())
        if not text:
            continue
        tw, th = _text_size(probe, text, font)
        widths.append(tw)
        heights.append(th)
        cleaned.append((text, color))
    if not cleaned:
        img.save(path)
        return path

    total_h = sum(heights) + line_gap * (len(cleaned) - 1)
    y = y_center - total_h // 2

    # Shadow layer
    shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sdraw = ImageDraw.Draw(shadow)
    yy = y
    for (text, _), th in zip(cleaned, heights):
        tw, _ = _text_size(sdraw, text, font)
        x = (W - tw) // 2
        sdraw.text(
            (x + shadow_offset[0], yy + shadow_offset[1]),
            text,
            font=font,
            fill=SHADOW,
        )
        yy += th + line_gap
    shadow = shadow.filter(ImageFilter.GaussianBlur(radius=shadow_blur))
    img = Image.alpha_composite(img, shadow)

    draw = ImageDraw.Draw(img)
    yy = y
    for (text, color), th in zip(cleaned, heights):
        tw, _ = _text_size(draw, text, font)
        x = (W - tw) // 2
        draw.text(
            (x, yy),
            text,
            font=font,
            fill=_rgba(color),
            stroke_width=stroke_width,
            stroke_fill=STROKE,
        )
        yy += th + line_gap

    path.parent.mkdir(parents=True, exist_ok=True)
    img.save(path)
    return path


def render_cta_png(
    path: Path,
    text: str = "full story on youtube →",
    *,
    pointsize: int = 44,
    y: int = 1580,
) -> Path:
    """Soft end CTA — lowercase white, no pill card."""
    return render_beat_png(
        path,
        [(text, "white")],
        pointsize=pointsize,
        y_center=y,
        stroke_width=3,
        shadow_blur=5,
    )


def auto_beats_from_phrases(
    phrases: Iterable[str],
    *,
    duration: float,
    hook_end: float = 7.0,
) -> list[dict]:
    """Split a list of short phrases across the opening hook window.

    Each phrase becomes one beat. Multi-word phrases can include ``\\n`` for stacked lines.
    Colors alternate yellow → white → yellow…
    """
    items = [p for p in phrases if str(p).strip()]
    if not items:
        return []
    window = min(max(hook_end, 3.0), max(duration - 4.5, 3.0))
    slot = window / len(items)
    beats: list[dict] = []
    t = 0.0
    for i, phrase in enumerate(items):
        parts = [x.strip() for x in str(phrase).replace("\\n", "\n").split("\n") if x.strip()]
        lines: list[LineSpec] = []
        for j, part in enumerate(parts):
            # First line of each beat starts yellow; alternate within stack
            base = i + j
            color: ColorName = "yellow" if base % 2 == 0 else "white"
            lines.append((part, color))
        t1 = window if i == len(items) - 1 else min(t + slot, window)
        beats.append({"start": round(t, 3), "end": round(t1, 3), "lines": lines})
        t = t1
    return beats


def ffmpeg_overlay_filter(
    beats: Sequence[dict],
    *,
    cta_start: float,
    beat_input_start: int = 1,
    has_cta: bool = True,
) -> str:
    """Build filter_complex tail that overlays beat PNGs + optional CTA on [base].

    Inputs: 0 = video, then beat PNGs starting at beat_input_start, then CTA last.
    """
    parts: list[str] = []
    label = "base"
    idx = beat_input_start
    for i, beat in enumerate(beats):
        nxt = f"b{i}"
        t0 = float(beat["start"])
        t1 = float(beat["end"])
        parts.append(
            f"[{label}][{idx}:v]overlay=0:0:enable='between(t,{t0:.3f},{t1:.3f})'"
            f":format=auto[{nxt}]"
        )
        label = nxt
        idx += 1

    if has_cta:
        parts.append(
            f"[{label}][{idx}:v]overlay=0:0:enable='gte(t,{cta_start:.3f})'"
            f":format=auto,format=yuv420p[v]"
        )
    else:
        parts.append(f"[{label}]format=yuv420p[v]")
    return ";".join(parts)


def vertical_base_filter(*, framed: bool = False) -> str:
    """Full-bleed vertical grade. framed=False removes the old white card border."""
    core = (
        "[0:v]split=2[bg][fg];"
        "[bg]scale=1080:1920:force_original_aspect_ratio=increase,"
        "crop=1080:1920,boxblur=22:1,eq=brightness=-0.32:saturation=0.9[bgv];"
        "[fg]scale=1080:1920:force_original_aspect_ratio=increase,"
        "crop=1080:1920,setsar=1[fgv];"
        "[bgv][fgv]overlay=0:0:format=auto"
    )
    if framed:
        return core + ",drawbox=x=28:y=(h-574)/2:w=1024:h=574:color=white@0.15:t=2[base]"
    return core + "[base]"
