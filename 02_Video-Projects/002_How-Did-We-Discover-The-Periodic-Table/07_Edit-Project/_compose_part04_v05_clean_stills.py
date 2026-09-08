#!/usr/bin/env python3
"""Compose I2V start frames for Part 04 v05 — NO hard fills / brown panels / sky boxes.

v04 failed because rectangular leather + flat sky overlays shipped unblended.
v05 start frames are continuous desk DNA from v01 02b / rough, with only tiny
yellow house-token pixels replaced by nearby leather (not a slab).
"""
from __future__ import annotations

import subprocess
from pathlib import Path

from PIL import Image, ImageFilter

PROJ = Path(__file__).resolve().parents[1]
RAW_V01 = PROJ / "04_Generated-Clips/part04/raw/v01_fast"
ROUGH_V03 = PROJ / "09_Final-Export/hos_002_part04_rough_v03.mp4"
STILLS = PROJ / "04_Generated-Clips/part04/refs/v05_stills"
PLATE_02B = RAW_V01 / "02b_cards_sixty_three_v01.mp4"
PLATE_02 = RAW_V01 / "02_mendeleev_desk_cards_v01.mp4"


def grab(src: Path, ss: float, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        [
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            "-ss", str(ss), "-i", str(src), "-frames:v", "1", str(dest),
        ],
        check=True,
    )


def is_house_token(r: int, g: int, b: int) -> bool:
    """Small glowing yellow house-icon detector (not orange flask / warm wood)."""
    if r < 215 or g < 175:
        return False
    if b > 130:
        return False
    if (r - b) < 110 or (g - b) < 70:
        return False
    if abs(r - g) > 40:
        return False
    return True


def scrub_house_tokens_only(src: Path, dest: Path) -> dict:
    """Replace yellow house-token pixels with nearby leather — never a rectangle."""
    im = Image.open(src).convert("RGB")
    w, h = im.size
    pix = im.load()
    # Prefer leather samples from mid-right book faces (below typical token zone)
    samples: list[tuple[int, int, int]] = []
    for y in range(int(h * 0.55), int(h * 0.78)):
        for x in range(int(w * 0.72), int(w * 0.92), 2):
            r, g, b = pix[x, y]
            if is_house_token(r, g, b):
                continue
            if r > 200 and g > 200 and b > 190:
                continue
            if 40 < r < 170 and 25 < g < 120 and b < 90:
                samples.append((r, g, b))
    leather = (
        tuple(sum(c[i] for c in samples) // len(samples) for i in range(3))
        if samples
        else (110, 72, 48)
    )

    hit = 0
    # Only right-half upper book zone — never paint a full panel
    x0, x1 = int(w * 0.62), w
    y0, y1 = 0, int(h * 0.62)
    for y in range(y0, y1):
        for x in range(x0, x1):
            r, g, b = pix[x, y]
            if not is_house_token(r, g, b):
                continue
            # blend with local neighborhood (non-token) if available
            nbrs: list[tuple[int, int, int]] = []
            for dy in (-3, -1, 1, 3, 5):
                for dx in (-4, -2, 2, 4):
                    nx, ny = x + dx, y + dy
                    if not (0 <= nx < w and 0 <= ny < h):
                        continue
                    rr, gg, bb = pix[nx, ny]
                    if is_house_token(rr, gg, bb):
                        continue
                    if 35 < rr < 180 and 20 < gg < 130 and bb < 100:
                        nbrs.append((rr, gg, bb))
            if nbrs:
                col = tuple(sum(c[i] for c in nbrs) // len(nbrs) for i in range(3))
            else:
                col = leather
            pix[x, y] = col
            hit += 1

    # Mild soften only on touched pixels via full-frame light blur of a mask — skip
    # if few hits (avoid looking like a panel).
    out = im
    if hit > 40:
        out = im.filter(ImageFilter.GaussianBlur(radius=0.4))
        # keep sharp base for non-token areas
        base = Image.open(src).convert("RGB")
        mask = Image.new("L", (w, h), 0)
        mp = mask.load()
        bp = base.load()
        op = out.load()
        for y in range(y0, y1):
            for x in range(x0, x1):
                r, g, b = bp[x, y]
                if is_house_token(r, g, b):
                    mp[x, y] = 220
        out = Image.composite(out, base, mask)

    dest.parent.mkdir(parents=True, exist_ok=True)
    out.save(dest, quality=95)
    meta = {
        "src": str(src),
        "dest": str(dest),
        "house_token_pixels": hit,
        "leather": leather,
        "method": "token_clone_only_no_rect_fill",
    }
    print(
        f"wrote {dest.name} token_hits={hit} leather={leather} bytes={dest.stat().st_size}",
        flush=True,
    )
    return meta


def main() -> None:
    STILLS.mkdir(parents=True, exist_ok=True)
    grab(PLATE_02B, 1.0, STILLS / "_grab_02b_t1.jpg")
    grab(PLATE_02B, 3.5, STILLS / "_grab_02b_t35.jpg")
    grab(PLATE_02B, 5.5, STILLS / "_grab_02b_t55.jpg")
    grab(PLATE_02, 2.0, STILLS / "_grab_02_t2.jpg")
    if ROUGH_V03.exists():
        # ~18–19s is 02b picture on rough — use only as DNA reference grab (will token-scrub)
        grab(ROUGH_V03, 18.5, STILLS / "_grab_rough_t185.jpg")

    metas = []
    metas.append(
        scrub_house_tokens_only(STILLS / "_grab_02b_t1.jpg", STILLS / "02b_desk_clean_i2v.jpg")
    )
    metas.append(
        scrub_house_tokens_only(STILLS / "_grab_02b_t35.jpg", STILLS / "02b_desk_clean_alt.jpg")
    )
    metas.append(
        scrub_house_tokens_only(STILLS / "_grab_02b_t55.jpg", STILLS / "02b_desk_clean_t1.jpg")
    )
    # plate 02 DNA — continuous desk, may include hands; useful T2V/I2V alt only
    scrub_house_tokens_only(STILLS / "_grab_02_t2.jpg", STILLS / "02b_desk_clean_from_02.jpg")
    if (STILLS / "_grab_rough_t185.jpg").exists():
        # If rough already has brown panel, skip as primary — still write for audit
        scrub_house_tokens_only(
            STILLS / "_grab_rough_t185.jpg", STILLS / "02b_desk_clean_from_rough.jpg"
        )

    (STILLS / "compose_meta.json").write_text(
        __import__("json").dumps({"stills": metas, "rule": "no_rect_hard_fill"}, indent=2)
    )
    print(f"OK v05 stills → {STILLS}", flush=True)


if __name__ == "__main__":
    main()
