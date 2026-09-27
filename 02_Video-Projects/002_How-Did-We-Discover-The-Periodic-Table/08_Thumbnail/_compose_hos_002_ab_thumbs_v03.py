#!/usr/bin/env python3
"""Compose HOS 002 A/B-test long thumbs B (v03 APPROVED) + C (v04 crop attempt).

Reuse live listing art (gallium / empty slot). No remint. No Flow. No Studio.
Rules: THUMBNAIL_AND_TITLE_RULES.md §2 — heavy sans caps, yellow hook word,
text off subject and out of bottom-right duration badge.

C v04: crop-only (no wash). If the crop is soft at 1280×720, STOP — Ben mints.
"""
from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = Path(__file__).resolve().parent
SELECTED = HERE / "Selected"
MAIN_SEL = Path(
    "/Users/benjaminoats/YouTube/History Of Science/02_Video-Projects/"
    "002_How-Did-We-Discover-The-Periodic-Table/08_Thumbnail/Selected"
)
ASSETS = Path("/Users/benjaminoats/.local/share/cursor-mac-mini-hos-worker/artifacts/assets")

WHITE = (255, 255, 255)
YELLOW = (255, 214, 46)
INK = (18, 12, 8)
SHADOW = (10, 6, 4, 220)

FONT = "/System/Library/Fonts/Supplemental/Arial Black.ttf"
FONT_FALLBACK = "/System/Library/Fonts/Supplemental/Impact.ttf"


def font(size: int) -> ImageFont.FreeTypeFont:
    for path in (FONT, FONT_FALLBACK):
        try:
            return ImageFont.truetype(path, size)
        except OSError:
            continue
    return ImageFont.load_default()


def load_src(candidates: list[Path]) -> Image.Image:
    for p in candidates:
        if p.exists():
            return Image.open(p).convert("RGB")
    raise SystemExit(f"missing source among {[str(c) for c in candidates]}")


def wash(im: Image.Image, box: tuple[int, int, int, int], sample: tuple[int, int, int, int], blur: int = 14) -> None:
    """Paint a soft scene-matched wash (B only — C v04 forbids wash)."""
    x0, y0, x1, y1 = box
    patch = im.crop(sample).resize((x1 - x0, y1 - y0), Image.Resampling.LANCZOS)
    patch = patch.filter(ImageFilter.GaussianBlur(blur))
    mask = Image.new("L", (x1 - x0, y1 - y0), 0)
    md = ImageDraw.Draw(mask)
    md.rounded_rectangle((0, 0, x1 - x0 - 1, y1 - y0 - 1), radius=28, fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(10))
    im.paste(patch, (x0, y0), mask)


def grade_left(im: Image.Image, width: int = 560, alpha: int = 110) -> Image.Image:
    """Smooth left darken for type legibility — no hard rectangle."""
    overlay = Image.new("RGBA", im.size, (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    for i in range(width):
        a = int(alpha * (1.0 - i / width) ** 1.4)
        if a <= 0:
            continue
        od.line([(i, 0), (i, im.height)], fill=(16, 10, 6, a))
    return Image.alpha_composite(im.convert("RGBA"), overlay).convert("RGB")


def draw_words(
    im: Image.Image,
    lines: list[list[tuple[str, tuple[int, int, int]]]],
    *,
    x: int,
    y: int,
    size: int,
    max_w: int,
    gap: float = 1.02,
) -> None:
    draw = ImageDraw.Draw(im)
    cy = y
    for line in lines:
        text = " ".join(w for w, _ in line)
        fsize = size
        f = font(fsize)
        while f.getlength(text) > max_w and fsize > 40:
            fsize -= 2
            f = font(fsize)
        stroke = max(7, fsize // 9)
        cx = x
        for w, color in line:
            draw.text((cx + 4, cy + 5), w, font=f, fill=SHADOW, stroke_width=stroke + 3, stroke_fill=SHADOW)
            draw.text((cx, cy), w, font=f, fill=color, stroke_width=stroke, stroke_fill=INK)
            cx += int(f.getlength(w + " "))
        cy += int(fsize * gap)


def save_jpg(im: Image.Image, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    rgb = im.convert("RGB").resize((1280, 720), Image.Resampling.LANCZOS)
    q = 90
    rgb.save(dest, "JPEG", quality=q, optimize=True, subsampling=1)
    while dest.stat().st_size > 1_900_000 and q > 70:
        q -= 4
        rgb.save(dest, "JPEG", quality=q, optimize=True, subsampling=1)
    print(f"{dest.name}  {dest.stat().st_size} B  {rgb.size}  q={q}", flush=True)


def compose_b() -> Path:
    """Gallium blob only — HE PREDICTED THIS (PREDICTED yellow). No Explorer. Ben APPROVED v03."""
    src = load_src(
        [
            MAIN_SEL / "hos_002_thumb_A_gallium_live_v02.png",
            ASSETS / "hos_002_thumb_A_gallium_live_v02b.png",
            ASSETS / "hos_002_thumb_A_gallium_live_v02.png",
            SELECTED / "hos_002_thumb_A_gallium_live_v02.png",
        ]
    )
    im = src.resize((1280, 720), Image.Resampling.LANCZOS)
    im = im.crop((360, 40, 1240, 700)).resize((1280, 720), Image.Resampling.LANCZOS)
    wash(im, (0, 0, 280, 220), sample=(400, 40, 700, 200), blur=22)
    im = grade_left(im, width=520, alpha=130)
    draw_words(
        im,
        [[("HE", WHITE)], [("PREDICTED", YELLOW)], [("THIS", WHITE)]],
        x=40,
        y=48,
        size=110,
        max_w=620,
        gap=0.98,
    )
    dest = SELECTED / "hos_002_thumb_B_predicted_v03.jpg"
    save_jpg(im, dest)
    return dest


def compose_c_v04() -> Path:
    """Glowing empty slot — LEFT EMPTY ON PURPOSE. Crop-only, no wash.

    Slot ~25% frame width, a little right of centre. Source is 1280×720 only;
    the crop needed for 1/4-width hero is ~3.4× upscale — check sharpness at
    100% before shipping. Soft → STOP; Ben mints a new still.
    """
    src = load_src(
        [
            MAIN_SEL / "hos_002_thumb_C_empty_slot_live_v02.png",
            ASSETS / "hos_002_thumb_C_empty_slot_live_v02b.png",
            ASSETS / "hos_002_thumb_C_empty_slot_live_v02.png",
            SELECTED / "hos_002_thumb_C_empty_slot_live_v02.png",
        ]
    )
    src = src.resize((1280, 720), Image.Resampling.LANCZOS)
    # Slot + glow bbox in source (detector + visual)
    slot = (760, 270, 855, 395)
    slot_w = slot[2] - slot[0]
    slot_cx = (slot[0] + slot[2]) / 2
    slot_cy = (slot[1] + slot[3]) / 2
    # ≥25% of 1280 → crop_w ≤ slot_w * 1280 / 320
    crop_w = min(int(slot_w * 1280 / 320), 380)
    crop_h = int(round(crop_w * 9 / 16))
    scale = 1280 / crop_w
    out_slot_cx = 1280 * 0.58
    crop_left = int(round(slot_cx - out_slot_cx / scale))
    crop_top = int(round(slot_cy - (720 * 0.48) / scale))
    crop_left = max(0, min(crop_left, 1280 - crop_w))
    crop_top = max(0, min(crop_top, 720 - crop_h))
    box = (crop_left, crop_top, crop_left + crop_w, crop_top + crop_h)
    print(
        f"C v04 crop {box} scale={scale:.2f}x "
        f"slot_share={100 * slot_w * scale / 1280:.1f}%",
        flush=True,
    )
    im = src.crop(box).resize((1280, 720), Image.Resampling.LANCZOS)
    # No wash — grade only
    im = grade_left(im, width=500, alpha=125)
    draw_words(
        im,
        [[("LEFT", WHITE)], [("EMPTY", YELLOW)], [("ON PURPOSE", WHITE)]],
        x=36,
        y=40,
        size=96,
        max_w=560,
        gap=0.96,
    )
    dest = SELECTED / "hos_002_thumb_C_empty_on_purpose_v04.jpg"
    save_jpg(im, dest)
    return dest


def compose_c_v05() -> Path:
    """C v05 from Flow Nano Banana still — same type layout as v04, no wash.

    Source already composed at hero scale (~1/4-width glowing slot, right of
    centre, calm top-left). Only a gentle downscale 1376×768 → 1280×720.
    """
    src = load_src(
        [
            HERE / "_stills_v05" / "hos_002_empty_slot_hero_v01.jpg",
        ]
    )
    sw, sh = src.size
    # Minimal geometry tweak: keep nearly full frame (slot already ~1/4 width).
    # Optional 2% trim from bottom bookshelf only if needed — default full frame.
    scale = 1280 / sw
    print(
        f"C v05 source {sw}x{sh} scale={scale:.3f}x (downscale, no hero crop)",
        flush=True,
    )
    im = src.resize((1280, 720), Image.Resampling.LANCZOS)
    im = grade_left(im, width=500, alpha=125)
    draw_words(
        im,
        [[("LEFT", WHITE)], [("EMPTY", YELLOW)], [("ON PURPOSE", WHITE)]],
        x=36,
        y=40,
        size=96,
        max_w=560,
        gap=0.96,
    )
    dest = SELECTED / "hos_002_thumb_C_empty_on_purpose_v05.jpg"
    save_jpg(im, dest)
    return dest


def main() -> None:
    SELECTED.mkdir(parents=True, exist_ok=True)
    # B v03 is Ben-approved — do not regenerate unless asked.
    c = compose_c_v05()
    print("DONE", c.name, flush=True)


if __name__ == "__main__":
    main()
