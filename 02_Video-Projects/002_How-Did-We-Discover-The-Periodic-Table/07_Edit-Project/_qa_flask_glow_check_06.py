#!/usr/bin/env python3
"""Crop-check conical flask region for self-emissive / desk-lighting invent.

Used every mid+ frame on 06_explorer_leaves_gap try3. Self-REJECT if flask glow invent.
"""
from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path

from PIL import Image

# Ensure argparse is available even if import order changes in wrappers.
assert argparse is not None


# Center-right conical flask on the locked OTS desk composition.
FLASK_BOX = (0.48, 0.42, 0.68, 0.82)  # nx0, ny0, nx1, ny1
# Desk pool under flask (spill invent signal).
DESK_POOL_BOX = (0.46, 0.72, 0.72, 0.92)

# Calibrated vs try2 UAT fail stills / desk crops:
#   try2 t0.5 desk bright≈0.014 (OK pale)
#   try2 t4.5 desk bright≈0.127 (invent)
#   try2 t7.2 desk bright≈0.154 (invent)
#   UAT t72_glow flask-ish bright≈0.28 (HARD FAIL)
BRIGHT_FRAC_FAIL = 0.055
MEAN_LUMA_FAIL = 175.0
MID_TIMES = (3.0, 4.5, 6.0, 7.2)


def bright_stats(im: Image.Image, box: tuple[float, float, float, float]) -> dict:
    w, h = im.size
    x0, y0, x1, y1 = box
    crop = im.crop((int(w * x0), int(h * y0), int(w * x1), int(h * y1))).convert("RGB")
    px = list(crop.getdata())
    n = max(1, len(px))
    mean = tuple(sum(c[i] for c in px) / n for i in range(3))
    luma = 0.2126 * mean[0] + 0.7152 * mean[1] + 0.0722 * mean[2]
    # Hot self-emissive core (near-white / molten yellow-white).
    bright = sum(
        1
        for r, g, b in px
        if r > 220 and g > 195 and b > 120 and (r + g + b) / 3.0 > 205
    )
    # Saturated molten amber (high R/G, suppressed B) — desk invent companion.
    molten = sum(1 for r, g, b in px if r > 200 and g > 140 and b < 90 and r - b > 90)
    return {
        "mean_rgb": [round(x, 1) for x in mean],
        "luma": round(luma, 1),
        "bright_frac": round(bright / n, 4),
        "molten_frac": round(molten / n, 4),
        "w": crop.size[0],
        "h": crop.size[1],
    }


def extract_frame(mp4: Path, t: float, out: Path) -> None:
    out.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-ss",
            f"{t:.2f}",
            "-i",
            str(mp4),
            "-frames:v",
            "1",
            "-q:v",
            "2",
            str(out),
        ],
        check=True,
        capture_output=True,
    )


def judge_frame(path: Path, t: float, crop_dir: Path) -> dict:
    im = Image.open(path).convert("RGB")
    flask = bright_stats(im, FLASK_BOX)
    desk = bright_stats(im, DESK_POOL_BOX)
    flask_crop = im.crop(
        (
            int(im.size[0] * FLASK_BOX[0]),
            int(im.size[1] * FLASK_BOX[1]),
            int(im.size[0] * FLASK_BOX[2]),
            int(im.size[1] * FLASK_BOX[3]),
        )
    )
    desk_crop = im.crop(
        (
            int(im.size[0] * DESK_POOL_BOX[0]),
            int(im.size[1] * DESK_POOL_BOX[1]),
            int(im.size[0] * DESK_POOL_BOX[2]),
            int(im.size[1] * DESK_POOL_BOX[3]),
        )
    )
    fc = crop_dir / f"t{t:.1f}_flask.jpg"
    dc = crop_dir / f"t{t:.1f}_deskpool.jpg"
    flask_crop.save(fc, quality=92)
    desk_crop.save(dc, quality=92)

    reasons = []
    if flask["bright_frac"] >= BRIGHT_FRAC_FAIL:
        reasons.append(f"flask_bright_frac={flask['bright_frac']:.3f}>={BRIGHT_FRAC_FAIL}")
    if flask["luma"] >= MEAN_LUMA_FAIL and flask["bright_frac"] >= 0.03:
        reasons.append(f"flask_luma={flask['luma']:.1f}>={MEAN_LUMA_FAIL} with bright core")
    if flask["molten_frac"] >= 0.04:
        reasons.append(f"flask_molten_frac={flask['molten_frac']:.3f}>=0.04")
    if desk["bright_frac"] >= 0.08 and flask["bright_frac"] >= 0.03:
        reasons.append(
            f"desk_pool_bright={desk['bright_frac']:.3f} with flask invent (desk-lighting)"
        )

    return {
        "t": t,
        "frame": str(path),
        "flask_crop": str(fc),
        "desk_crop": str(dc),
        "flask": flask,
        "desk_pool": desk,
        "fail": bool(reasons),
        "reasons": reasons,
    }


def contact_strip(frames: list[Path], out: Path) -> None:
    imgs = [Image.open(p).convert("RGB") for p in frames]
    h = min(im.size[1] for im in imgs)
    resized = []
    for im in imgs:
        w = int(im.size[0] * (h / im.size[1]))
        resized.append(im.resize((w, h), Image.Resampling.LANCZOS))
    total_w = sum(im.size[0] for im in resized)
    strip = Image.new("RGB", (total_w, h))
    x = 0
    for im in resized:
        strip.paste(im, (x, 0))
        x += im.size[0]
    out.parent.mkdir(parents=True, exist_ok=True)
    strip.save(out, quality=90)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--mp4", type=Path, required=True)
    ap.add_argument("--out-dir", type=Path, required=True)
    ap.add_argument("--times", default="0.5,1.5,3.0,4.5,6.0,7.2")
    args = ap.parse_args()

    out = args.out_dir
    frames_dir = out / "frames"
    crops_dir = out / "flask_crops"
    frames_dir.mkdir(parents=True, exist_ok=True)
    crops_dir.mkdir(parents=True, exist_ok=True)

    times = [float(x) for x in args.times.split(",") if x.strip()]
    results = []
    frame_paths = []
    for t in times:
        fp = frames_dir / f"t{t:.1f}.jpg"
        extract_frame(args.mp4, t, fp)
        frame_paths.append(fp)
        results.append(judge_frame(fp, t, crops_dir))

    contact = out / "06_explorer_leaves_gap_contact_continuous_try3.jpg"
    contact_strip(frame_paths, contact)

    mid_fails = [r for r in results if r["t"] in MID_TIMES and r["fail"]]
    any_fail = [r for r in results if r["fail"]]
    verdict = "SELF_REJECT" if mid_fails else ("SELF_REJECT" if any_fail else "PASS_CANDIDATE")
    if mid_fails:
        reason = "flask glow invent mid→late: " + "; ".join(
            f"t{r['t']}:{','.join(r['reasons'])}" for r in mid_fails
        )
    elif any_fail:
        reason = "flask glow invent: " + "; ".join(
            f"t{r['t']}:{','.join(r['reasons'])}" for r in any_fail
        )
    else:
        reason = "flask liquids stay dull/matte translucent on mid crop-checks; no desk-lighting invent"

    report = {
        "plate": "06_explorer_leaves_gap",
        "try": 3,
        "gate": "CLEAN_LIGHT_flask_dull_matte",
        "verdict": verdict,
        "reason": reason,
        "thresholds": {
            "bright_frac_fail": BRIGHT_FRAC_FAIL,
            "mean_luma_fail": MEAN_LUMA_FAIL,
            "mid_times": list(MID_TIMES),
        },
        "frames": results,
        "contact_continuous": str(contact),
    }
    (out / "flask_glow_check.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))
    if verdict == "SELF_REJECT":
        raise SystemExit(2)


if __name__ == "__main__":
    main()
