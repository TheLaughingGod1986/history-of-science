#!/usr/bin/env python3
"""Plate UAT for 11_publish_gaps try9 — continuous contact + text-edge + lamp/flask invent.

Self-REJECT on readable invented text OR lamp/flask invent.
Text-edge crop-check every mid frame (bottom band + BR).
"""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

TIMES = (0.5, 1.5, 3.0, 4.5, 6.0, 7.2)
MID_TIMES = (3.0, 4.5, 6.0, 7.2)

# Flask / desk invent regions tuned for boardtop crop (flasks upper-mid).
FLASK_BOX = (0.20, 0.18, 0.55, 0.62)
DESK_POOL_BOX = (0.25, 0.55, 0.70, 0.88)
LEFT_FIXTURE_BOX = (0.00, 0.05, 0.22, 0.55)
# Front-edge invent zone = bottom band of frame (should stay wood/holes, not SECURITY lip).
BOTTOM_EDGE_BOX = (0.10, 0.78, 0.95, 0.99)
BR_EDGE_BOX = (0.45, 0.62, 0.98, 0.98)


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
    bright = sum(
        1
        for r, g, b in px
        if r > 220 and g > 195 and b > 120 and (r + g + b) / 3.0 > 205
    )
    molten = sum(1 for r, g, b in px if r > 200 and g > 140 and b < 90 and r - b > 90)
    warm_fixture = sum(
        1 for r, g, b in px if r > 170 and g > 110 and b < 90 and r - b > 70 and r > g
    )
    # Dark glyph candidates on light cream (text invent heuristic).
    textish = 0
    arr = crop.load()
    cw, ch = crop.size
    for y in range(ch):
        for x in range(cw):
            r, g, b = arr[x, y]
            luma_p = 0.2126 * r + 0.7152 * g + 0.0722 * b
            if luma_p < 55 and r < 95 and g < 95 and b < 95:
                sx, sy = min(cw - 1, x + 6), max(0, y - 6)
                rr, gg, bb = arr[sx, sy]
                if rr > 175 and gg > 165 and bb > 150:
                    textish += 1
    return {
        "mean_rgb": [round(x, 1) for x in mean],
        "luma": round(luma, 1),
        "bright_frac": round(bright / n, 4),
        "molten_frac": round(molten / n, 4),
        "warm_fixture_frac": round(warm_fixture / n, 4),
        "textish_px": textish,
        "textish_frac": round(textish / n, 5),
    }


def contact_strip(frames: list[Path], out: Path, labels: list[str] | None = None) -> None:
    imgs = [Image.open(p).convert("RGB") for p in frames]
    target_h = 240
    resized = []
    for i, im in enumerate(imgs):
        w = int(im.size[0] * (target_h / im.size[1]))
        r = im.resize((w, target_h), Image.Resampling.LANCZOS)
        if labels:
            d = ImageDraw.Draw(r)
            d.rectangle([0, 0, 70, 22], fill=(0, 0, 0))
            d.text((4, 4), labels[i], fill=(255, 255, 120))
        resized.append(r)
    total_w = sum(im.size[0] for im in resized)
    strip = Image.new("RGB", (total_w, target_h))
    x = 0
    for im in resized:
        strip.paste(im, (x, 0))
        x += im.size[0]
    out.parent.mkdir(parents=True, exist_ok=True)
    strip.save(out, quality=90)


def judge(mp4: Path, out_dir: Path, try_id: str = "9") -> dict:
    frames_dir = out_dir / "frames"
    edge_dir = out_dir / "edge_crops"
    flask_dir = out_dir / "flask_crops"
    fixture_dir = out_dir / "fixture_crops"
    for d in (frames_dir, edge_dir, flask_dir, fixture_dir):
        d.mkdir(parents=True, exist_ok=True)

    frame_paths: list[Path] = []
    results = []
    edge_paths: list[Path] = []
    for t in TIMES:
        fp = frames_dir / f"t{t:.1f}.jpg"
        extract_frame(mp4, t, fp)
        # also copy to plate-named stills
        still = out_dir / f"11_publish_gaps_t{t:.1f}.jpg"
        still.write_bytes(fp.read_bytes())
        frame_paths.append(still)

        im = Image.open(fp).convert("RGB")
        w, h = im.size
        flask = box_stats(im, FLASK_BOX)
        desk = box_stats(im, DESK_POOL_BOX)
        left = box_stats(im, LEFT_FIXTURE_BOX)
        bottom = box_stats(im, BOTTOM_EDGE_BOX)
        br = box_stats(im, BR_EDGE_BOX)

        # save crops
        def save_box(box, path):
            x0, y0, x1, y1 = box
            im.crop((int(w * x0), int(h * y0), int(w * x1), int(h * y1))).save(path, quality=92)

        save_box(FLASK_BOX, flask_dir / f"t{t:.1f}_flask.jpg")
        save_box(DESK_POOL_BOX, flask_dir / f"t{t:.1f}_deskpool.jpg")
        save_box(LEFT_FIXTURE_BOX, fixture_dir / f"t{t:.1f}_left.jpg")
        ep = edge_dir / f"t{t:.1f}_bottom_edge.jpg"
        save_box(BOTTOM_EDGE_BOX, ep)
        save_box(BR_EDGE_BOX, edge_dir / f"t{t:.1f}_BR_edge.jpg")
        edge_paths.append(ep)

        reasons = []
        lamp_invent = left["warm_fixture_frac"] >= 0.085 or (
            left["bright_frac"] >= 0.06 and left["warm_fixture_frac"] >= 0.05
        )
        flask_invent = (
            flask["bright_frac"] >= 0.055
            or flask["molten_frac"] >= 0.04
            or (desk["bright_frac"] >= 0.08 and flask["bright_frac"] >= 0.03)
        )
        # Heuristic only — human/videoReview still owns SECURITY/RESULT call.
        text_heuristic = bottom["textish_frac"] >= 0.004 or br["textish_frac"] >= 0.0045
        if lamp_invent:
            reasons.append(
                f"lamp_invent left warm={left['warm_fixture_frac']:.4f} bright={left['bright_frac']:.4f}"
            )
        if flask_invent:
            reasons.append(
                f"flask_glow bright={flask['bright_frac']:.4f} molten={flask['molten_frac']:.4f} desk={desk['bright_frac']:.4f}"
            )
        if text_heuristic:
            reasons.append(
                f"text_edge_heuristic bottom={bottom['textish_frac']:.5f} BR={br['textish_frac']:.5f}"
            )

        results.append(
            {
                "t": t,
                "lamp_invent": lamp_invent,
                "flask_invent": flask_invent,
                "text_edge_heuristic": text_heuristic,
                "left": left,
                "flask": flask,
                "desk": desk,
                "bottom_edge": bottom,
                "br_edge": br,
                "reasons": reasons,
            }
        )

    contact = out_dir / f"11_publish_gaps_contact_continuous_try{try_id}.jpg"
    contact_strip(frame_paths, contact, [f"t{t}" for t in TIMES])
    edge_contact = out_dir / f"11_publish_gaps_edge_contact_try{try_id}.jpg"
    contact_strip(edge_paths, edge_contact, [f"t{t}" for t in TIMES])

    mid = [r for r in results if r["t"] in MID_TIMES]
    lamp_fail = any(r["lamp_invent"] for r in mid)
    flask_fail = any(r["flask_invent"] for r in mid)
    text_heur_fail = any(r["text_edge_heuristic"] for r in mid)

    report = {
        "plate": "11_publish_gaps",
        "try": try_id,
        "sha256": sha256(mp4),
        "bytes": mp4.stat().st_size,
        "duration_probe": "expect ~8s",
        "gates_heuristic": {
            "lamp_invent": "FAIL" if lamp_fail else "CLEAR",
            "flask_glow_invent": "FAIL" if flask_fail else "CLEAR",
            "text_edge_heuristic": "FAIL" if text_heur_fail else "CLEAR_HEURISTIC",
        },
        "note": (
            "text invent final call requires visual/videoReview of edge crops + stills "
            "(SECURITY/RESULT). Heuristic flags dark-on-cream only."
        ),
        "frames": results,
        "contact_continuous": str(contact),
        "edge_contact": str(edge_contact),
        "plate_library_lock_sha": "4b8ed25",
    }
    (out_dir / f"plate_qa_11_try{try_id}.json").write_text(json.dumps(report, indent=2) + "\n")
    (out_dir / f"invent_heuristics_try{try_id}.json").write_text(
        json.dumps(
            {
                "plate": "11_publish_gaps",
                "try": try_id,
                "frames": results,
                "fail_reasons": [x for r in results for x in r["reasons"]],
            },
            indent=2,
        )
        + "\n"
    )
    print(json.dumps(report, indent=2))
    return report


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--mp4", type=Path, required=True)
    ap.add_argument("--out-dir", type=Path, required=True)
    ap.add_argument("--try", dest="try_id", default="9")
    args = ap.parse_args()
    judge(args.mp4, args.out_dir, args.try_id)


if __name__ == "__main__":
    main()
