#!/usr/bin/env python3
"""Plate UAT for 05_columns_families try1 — continuous contact + lamp crops.

Self-REJECT on lava drip / molten bead / open shade-cup / underside bulb /
practical lamp invent. Readable cards OK. No assemble.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw

TIMES = (0.0, 1.0, 2.0, 3.5, 5.0, 6.5, 7.5)
# Upper-left / top invent zones where v21 lava lived.
LAMP_BOX = (0.00, 0.00, 0.28, 0.42)
TOP_BOX = (0.15, 0.00, 0.55, 0.28)
DESK_GLOW_BOX = (0.05, 0.35, 0.40, 0.70)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


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


def box_stats(im: Image.Image, box: tuple[float, float, float, float]) -> dict:
    w, h = im.size
    x0, y0, x1, y1 = box
    crop = im.crop((int(w * x0), int(h * y0), int(w * x1), int(h * y1))).convert("RGB")
    px = list(crop.getdata())
    n = max(1, len(px))
    mean = tuple(sum(c[i] for c in px) / n for i in range(3))
    luma = 0.2126 * mean[0] + 0.7152 * mean[1] + 0.0722 * mean[2]
    # Hot molten / lava bead candidates: very warm, saturated, bright.
    molten = sum(1 for r, g, b in px if r > 210 and g > 120 and b < 90 and r - b > 110 and r > g)
    # Bright bulb / open shade-cup look-in.
    bulb = sum(1 for r, g, b in px if r > 230 and g > 200 and b > 140 and (r + g + b) / 3.0 > 210)
    warm_fixture = sum(
        1 for r, g, b in px if r > 180 and g > 120 and b < 100 and r - b > 80 and r > g + 10
    )
    return {
        "mean_rgb": [round(x, 1) for x in mean],
        "luma": round(luma, 1),
        "molten_frac": round(molten / n, 4),
        "bulb_frac": round(bulb / n, 4),
        "warm_fixture_frac": round(warm_fixture / n, 4),
    }


def contact_strip(frames: list[Path], out: Path, labels: list[str] | None = None) -> None:
    imgs = [Image.open(p).convert("RGB") for p in frames]
    target_h = 220
    resized = []
    for i, im in enumerate(imgs):
        w = int(im.size[0] * (target_h / im.size[1]))
        r = im.resize((w, target_h), Image.Resampling.LANCZOS)
        if labels:
            d = ImageDraw.Draw(r)
            d.rectangle([0, 0, 72, 22], fill=(0, 0, 0))
            d.text((4, 4), labels[i], fill=(255, 255, 120))
        resized.append(r)
    total_w = sum(im.size[0] for im in resized)
    strip = Image.new("RGB", (total_w, target_h))
    x = 0
    for im in resized:
        strip.paste(im, (x, 0))
        x += im.size[0]
    out.parent.mkdir(parents=True, exist_ok=True)
    strip.save(out, quality=92)


def probe_duration(mp4: Path) -> float:
    r = subprocess.run(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "default=nw=1:nk=1",
            str(mp4),
        ],
        capture_output=True,
        text=True,
        check=True,
    )
    return float(r.stdout.strip())


def judge(mp4: Path, out_dir: Path, try_id: str = "1") -> dict:
    frames_dir = out_dir / "frames"
    lamp_dir = out_dir / "lamp_crops"
    for d in (frames_dir, lamp_dir):
        d.mkdir(parents=True, exist_ok=True)

    frame_paths: list[Path] = []
    lamp_paths: list[Path] = []
    results = []
    reject_reasons: list[str] = []

    for t in TIMES:
        fp = frames_dir / f"t{t:.1f}.jpg"
        extract_frame(mp4, t, fp)
        still = out_dir / f"05_columns_families_t{t:.1f}.jpg"
        still.write_bytes(fp.read_bytes())
        frame_paths.append(still)

        im = Image.open(fp).convert("RGB")
        w, h = im.size
        lamp = box_stats(im, LAMP_BOX)
        top = box_stats(im, TOP_BOX)
        desk = box_stats(im, DESK_GLOW_BOX)

        def save_box(box, path):
            x0, y0, x1, y1 = box
            im.crop((int(w * x0), int(h * y0), int(w * x1), int(h * y1))).save(path, quality=92)

        lp = lamp_dir / f"t{t:.1f}_lamp.jpg"
        save_box(LAMP_BOX, lp)
        save_box(TOP_BOX, lamp_dir / f"t{t:.1f}_top.jpg")
        save_box(DESK_GLOW_BOX, lamp_dir / f"t{t:.1f}_deskglow.jpg")
        lamp_paths.append(lp)

        reasons = []
        lava = lamp["molten_frac"] >= 0.012 or top["molten_frac"] >= 0.01
        bulb = lamp["bulb_frac"] >= 0.045 and lamp["warm_fixture_frac"] >= 0.04
        fixture = lamp["warm_fixture_frac"] >= 0.09 and lamp["bulb_frac"] >= 0.02
        desk_lava = desk["molten_frac"] >= 0.02 and desk["warm_fixture_frac"] >= 0.05
        if lava:
            reasons.append(
                f"lava/molten bead lamp={lamp['molten_frac']:.4f} top={top['molten_frac']:.4f}"
            )
        if bulb:
            reasons.append(
                f"underside_bulb/open_cup bulb={lamp['bulb_frac']:.4f} warm={lamp['warm_fixture_frac']:.4f}"
            )
        if fixture:
            reasons.append(
                f"practical_lamp_invent warm={lamp['warm_fixture_frac']:.4f} bulb={lamp['bulb_frac']:.4f}"
            )
        if desk_lava:
            reasons.append(
                f"desk_lava_invent molten={desk['molten_frac']:.4f} warm={desk['warm_fixture_frac']:.4f}"
            )
        reject_reasons.extend(reasons)
        results.append(
            {
                "t": t,
                "lava_molten": lava,
                "underside_bulb": bulb,
                "lamp_invent": fixture,
                "desk_lava": desk_lava,
                "lamp": lamp,
                "top": top,
                "desk": desk,
                "reasons": reasons,
            }
        )

    contact = out_dir / f"05_columns_families_contact_continuous_try{try_id}.jpg"
    contact_strip(frame_paths, contact, [f"t{t}" for t in TIMES])
    lamp_contact = out_dir / f"05_columns_families_lamp_contact_try{try_id}.jpg"
    contact_strip(lamp_paths, lamp_contact, [f"t{t}" for t in TIMES])

    auto_fail = any(
        r["lava_molten"] or r["underside_bulb"] or r["lamp_invent"] or r["desk_lava"] for r in results
    )
    verdict = "SELF_REJECT" if auto_fail else "KEEP_CANDIDATE_PENDING_HUMAN"
    dur = probe_duration(mp4)
    digest = sha256(mp4)
    report = {
        "plate": "05_columns_families",
        "try": try_id,
        "verdict": verdict,
        "model": "Veo 3.1 - Quality",
        "mp4": mp4.name,
        "sha256": digest,
        "duration_s": dur,
        "bytes": mp4.stat().st_size,
        "auto_fail": auto_fail,
        "reject_reasons": sorted(set(reject_reasons)),
        "frames": results,
        "contact_continuous": str(contact.name),
        "lamp_contact": str(lamp_contact.name),
        "assemble": False,
        "note": (
            "Heuristic auto-gate for lava/bulb/fixture invent. Human still owns final KEEP. "
            "Readable cards OK. No assemble this run."
        ),
    }
    (out_dir / f"plate_qa_05_try{try_id}.json").write_text(json.dumps(report, indent=2) + "\n")
    (out_dir / "sha256.txt").write_text(digest + "\n")
    return report


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--mp4", required=True, type=Path)
    ap.add_argument("--out", required=True, type=Path)
    ap.add_argument("--try", dest="try_id", default="1")
    ap.add_argument("--copy-start", type=Path, default=None)
    args = ap.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    if args.copy_start and args.copy_start.exists():
        shutil.copy2(args.copy_start, args.out / args.copy_start.name)
    report = judge(args.mp4, args.out, args.try_id)
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
