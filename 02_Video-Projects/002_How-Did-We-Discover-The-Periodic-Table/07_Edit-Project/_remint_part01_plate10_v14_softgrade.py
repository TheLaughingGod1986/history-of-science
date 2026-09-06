#!/usr/bin/env python3
"""Rebuild Part 01 plate 10 from pre-scrub real-Veo motion.

v13 colourless scrub introduced a visible blue rectangular mask (UAT FAIL).
Flow + Gemini Veo credits are exhausted again after Ben top-up burn.

Approach: start from pre-scrub real Veo clip (no blue mask), apply a soft
elliptical colourless grade under the grate only (no hard rectangle, no blue fill).
"""
from __future__ import annotations

import math
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image

PROJ = Path(__file__).resolve().parents[1]
SRC = PROJ / "04_Generated-Clips/part01/_rejected_uat_v13_plate10/10_rock_not_fire_v01_pre_scrub.mp4"
DEST = PROJ / "04_Generated-Clips/part01/raw/v01_fast/10_rock_not_fire_v01.mp4"
REJECT = PROJ / "04_Generated-Clips/part01/_rejected_uat_v14_plate10"
QA = PROJ / "07_Edit-Project/_qa_v14_plate10_prep"


def neutralize_frame(im: Image.Image) -> Image.Image:
    """Soft-desaturate warm under-grate glow; never paint a hard blue rect."""
    rgb = im.convert("RGB")
    w, h = rgb.size
    px = rgb.load()
    # Ore/grate sits left-center in this locked plate composition.
    cx, cy = int(w * 0.22), int(h * 0.64)
    rx, ry = int(w * 0.17), int(h * 0.20)
    for y in range(max(0, cy - ry), min(h, cy + ry)):
        for x in range(max(0, cx - rx), min(w, cx + rx)):
            nx = (x - cx) / rx
            ny = (y - cy) / ry
            d = math.sqrt(nx * nx + ny * ny)
            if d >= 1.0:
                continue
            fall = (1.0 - d) ** 2
            r, g, b = px[x, y]
            warm = r - max(g, b)
            if warm < 10:
                continue
            # Pull red toward local neutral; slight lift of B/G so haze reads colourless,
            # but keep B from racing ahead of R/G (avoids cyan/blue scrub look).
            target = int((g + b) * 0.5)
            nr = int(r - fall * 0.90 * (r - target))
            ng = int(g + fall * 0.12 * max(0, r - g))
            nb = int(b + fall * 0.10 * max(0, r - b))
            # Clamp so we never create B-dominant cool patch
            nb = min(nb, max(nr, ng) + 8)
            px[x, y] = (
                max(0, min(255, nr)),
                max(0, min(255, ng)),
                max(0, min(255, nb)),
            )
    return rgb


def blue_score(path: Path) -> float:
    im = Image.open(path).convert("RGB")
    w, h = im.size
    crop = im.crop((int(w * 0.05), int(h * 0.2), int(w * 0.45), int(h * 0.85)))
    px = list(crop.getdata())
    blue = sum(1 for r, g, b in px if b > r + 18 and b > g + 12 and b > 60)
    return blue / max(1, len(px))


def warm_score(path: Path) -> float:
    im = Image.open(path).convert("RGB")
    w, h = im.size
    crop = im.crop((int(w * 0.08), int(h * 0.45), int(w * 0.38), int(h * 0.82)))
    px = list(crop.getdata())
    warm = sum(1 for r, g, b in px if r > g + 22 and r > b + 22 and r > 90)
    return warm / max(1, len(px))


def main() -> None:
    if not SRC.exists():
        raise SystemExit(f"STOP: missing pre-scrub source {SRC}")
    REJECT.mkdir(parents=True, exist_ok=True)
    QA.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory(prefix="p10_v14_") as td:
        td_path = Path(td)
        inn = td_path / "in"
        out = td_path / "out"
        inn.mkdir()
        out.mkdir()
        subprocess.run(
            [
                "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
                "-i", str(SRC), "-fps_mode", "passthrough", str(inn / "f_%04d.png"),
            ],
            check=True,
        )
        frames = sorted(inn.glob("f_*.png"))
        if len(frames) < 24:
            raise SystemExit(f"STOP: too few frames {len(frames)}")
        print(f"frames={len(frames)} src={SRC.name}", flush=True)
        for i, fp in enumerate(frames, 1):
            im = Image.open(fp)
            neutralize_frame(im).save(out / fp.name)
            if i % 24 == 0:
                print(f"  graded {i}/{len(frames)}", flush=True)

        tmp = REJECT / "10_rock_not_fire_v14_softgrade.mp4"
        subprocess.run(
            [
                "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
                "-framerate", "24", "-i", str(out / "f_%04d.png"),
                "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18",
                "-movflags", "+faststart", str(tmp),
            ],
            check=True,
        )

        # QA stills
        for t, name in [(0.5, "v14_t05.jpg"), (2.0, "v14_t2.jpg"), (4.0, "v14_t4.jpg"), (6.0, "v14_t6.jpg")]:
            dest = QA / name
            subprocess.run(
                [
                    "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
                    "-ss", str(t), "-i", str(tmp), "-frames:v", "1", "-q:v", "2", str(dest),
                ],
                check=True,
            )
            print(
                f"QA {name} blue={blue_score(dest):.4f} warm={warm_score(dest):.4f}",
                flush=True,
            )

        # Gate: blue must stay near pre-scrub (not colourless-scrub levels)
        pre_still = QA / "pre_scrub_ref_t2.jpg"
        subprocess.run(
            [
                "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
                "-ss", "2", "-i", str(SRC), "-frames:v", "1", "-q:v", "2", str(pre_still),
            ],
            check=True,
        )
        bad_still = QA / "v13_colourless_ref_t2.jpg"
        colourless = PROJ / "04_Generated-Clips/part01/_rejected_uat_v13_plate10/10_rock_not_fire_v13_colourless.mp4"
        if colourless.exists():
            subprocess.run(
                [
                    "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
                    "-ss", "2", "-i", str(colourless), "-frames:v", "1", "-q:v", "2", str(bad_still),
                ],
                check=True,
            )
        b_new = blue_score(QA / "v14_t2.jpg")
        b_pre = blue_score(pre_still)
        w_new = warm_score(QA / "v14_t2.jpg")
        w_pre = warm_score(pre_still)
        print(f"GATE blue pre={b_pre:.4f} new={b_new:.4f} | warm pre={w_pre:.4f} new={w_new:.4f}", flush=True)
        if b_new > b_pre + 0.005:
            raise SystemExit(f"STOP: blue increased {b_pre:.4f} → {b_new:.4f}")
        if w_new > w_pre * 0.85 and w_new > 0.12:
            print("WARN: warm still high; continuing but flag for visual QA", flush=True)

        if DEST.exists():
            prev = REJECT / "10_rock_not_fire_v01_before_v14_softgrade.mp4"
            if prev.exists():
                prev.unlink()
            shutil.move(str(DEST), str(prev))
        shutil.copy2(tmp, DEST)
        print(f"SAVED {DEST} bytes={DEST.stat().st_size}", flush=True)


if __name__ == "__main__":
    main()
