#!/usr/bin/env python3
"""Chief h15 rod check. Measures the metal shaft, not the tip above the trace and not the hand."""
from __future__ import annotations

import json
import subprocess as sp
from pathlib import Path

import numpy as np

W, H, FPS = 1920, 1080, 24
LIMIT = 0.01 * W  # 19.2
PLATE = Path(
    "/Users/benjaminoats/YouTube/hos-008-lightning/02_Video-Projects"
    "/008_Lightning-Franklin/04_Generated-Clips/part05/raw/v01/06_rod_fitting_t1.mp4"
)
ALPHA = Path(
    "/private/tmp/j1267-hos008-rough-v09/code_graphics_v06"
    "/code_graphic_008_p5_10_metal_easy.mov"
)
OUT = Path("/private/tmp/j1267-hos008-rough-v09/ROD_TRACE.json")
OFF = 109 / FPS
USE = 42 / FPS


def plate_gray(t: float) -> np.ndarray:
    raw = sp.check_output([
        "ffmpeg", "-v", "error", "-ss", f"{t:.6f}", "-i", str(PLATE), "-frames:v", "1",
        "-vf", f"scale={W}:{H}:flags=lanczos,eq=brightness=0.04:contrast=0.96,format=gray",
        "-f", "rawvideo", "-",
    ])
    return np.frombuffer(raw, np.uint8).reshape(H, W).astype("float32")


def alpha_rgba(t: float) -> np.ndarray:
    raw = sp.check_output([
        "ffmpeg", "-v", "error", "-ss", f"{t:.6f}", "-i", str(ALPHA), "-frames:v", "1",
        "-f", "rawvideo", "-pix_fmt", "rgba", "-",
    ])
    return np.frombuffer(raw, np.uint8).reshape(H, W, 4)


def gold_mask(rgba: np.ndarray) -> np.ndarray:
    r, g, b, a = [rgba[:, :, i].astype(np.int16) for i in range(4)]
    return (a > 80) & (r > 150) & (g > 110) & (b < 150) & ((r - b) > 70) & ((r - g) > 15)


def trace_x_at(mask: np.ndarray, y: int, half: int = 8) -> float | None:
    sl = mask[max(0, y - half): y + half + 1, 1120:1240]
    xs = np.where(sl)[1] + 1120
    if len(xs) < 8:
        return None
    return float(np.median(xs))


def metal_pairs(row: np.ndarray, tx: float) -> list[dict]:
    s = np.convolve(row, np.ones(3) / 3, mode="same")
    d = np.diff(s)
    falls, rises = [], []
    for x in range(1120, 1280):
        if d[x] < -6 and d[x] <= d[x - 2:x + 3].min():
            falls.append(x)
        if d[x] > 6 and d[x] >= d[x - 2:x + 3].max():
            rises.append(x)
    out = []
    for f in falls:
        for r in rises:
            width = r - f
            if not (8 <= width <= 20):
                continue
            centre = (f + r) / 2
            if abs(centre - tx) > 40:
                continue
            depth = float(s[f:r + 1].min())
            if depth < 90:
                out.append({
                    "rod_x": centre,
                    "left": f,
                    "right": r,
                    "width": width,
                    "depth": round(depth, 1),
                })
            break
    return out


def choose(pairs: list[dict], tx: float) -> dict | None:
    if not pairs:
        return None
    # Darkest metal. A grip is shallower (depth ~70-85) than the shaft (~30-50).
    return min(pairs, key=lambda p: (p["depth"], abs(p["rod_x"] - tx)))


def measure() -> dict:
    samples = []
    worst = 0.0
    for pct in (10, 25, 50, 75, 90):
        t_row = USE * pct / 100
        gray = plate_gray(OFF + t_row)
        mask = gold_mask(alpha_rgba(t_row))
        ys = np.where(mask[:, 1140:1230].any(axis=1))[0]
        y_top, y_foot = int(ys.min()), int(ys.max())
        heights = {
            "top": y_top + 12,
            "mid": (y_top + y_foot) // 2,
            "foot": y_foot - 12,
        }
        # Mid shaft is the anchor. The rod is continuous, so top and foot
        # stay near it. The gripping hand is a separate edge off to the side.
        mid_y = heights["mid"]
        mid_tx = trace_x_at(mask, mid_y)
        mid_pairs = [
            p for p in metal_pairs(gray[mid_y - 2:mid_y + 3].mean(axis=0), mid_tx)
            if p["depth"] <= 55
        ]
        mid_pick = choose(mid_pairs, mid_tx)
        if mid_pick is None:
            raise RuntimeError(f"p{pct}: mid shaft not found")
        anchor = mid_pick["rod_x"]
        heights_out = []
        sample_worst = 0.0
        for name, y in heights.items():
            tx = trace_x_at(mask, y)
            if tx is None:
                raise RuntimeError(f"p{pct} {name}: no gold trace")
            cands = []
            for dy in range(-12, 32, 2):
                yy = int(np.clip(y + dy, 2, H - 3))
                if not (y_top <= yy <= y_foot):
                    continue
                band = gray[yy - 2:yy + 3].mean(axis=0)
                tx_y = trace_x_at(mask, yy) or tx
                for p in metal_pairs(band, tx_y):
                    if abs(p["rod_x"] - anchor) <= 24 and p["depth"] <= 68:
                        cands.append({**p, "y": yy, "dy": dy, "trace_x": tx_y})
            if not cands:
                raise RuntimeError(f"p{pct} {name}: rod not found near shaft {anchor:.0f}")
            # The shaft continues from the mid reading. The closest centre is the rod.
            # A narrow sliver beside the gripping hand sits further off and is not used.
            found = min(cands, key=lambda p: (abs(p["rod_x"] - anchor), abs(p["width"] - 12), p["depth"]))
            off = found["rod_x"] - found["trace_x"]
            sample_worst = max(sample_worst, abs(off))
            heights_out.append({
                "height": name,
                "y": found["y"],
                "asked_y": y,
                "rod_x": round(found["rod_x"], 1),
                "trace_x": round(found["trace_x"], 1),
                "offset_px": round(off, 1),
                "offset_pct_of_width": round(100 * off / W, 2),
                "width_px": found["width"],
                "depth": found["depth"],
                "edges": [found["left"], found["right"]],
            })
            print(
                f"  p{pct} {name:4} y={found['y']} rod={found['rod_x']:.1f} "
                f"trace={found['trace_x']:.1f} off={off:+.1f} w={found['width']} d={found['depth']}",
                flush=True,
            )
        worst = max(worst, sample_worst)
        samples.append({
            "pct": pct,
            "plate_s": round(OFF + t_row, 4),
            "row_s": round(t_row, 4),
            "shaft_anchor_x": round(anchor, 1),
            "worst_abs_px": round(sample_worst, 1),
            "pass": sample_worst <= LIMIT + 0.05,
            "heights": heights_out,
        })
        print(f"  p{pct} WORST {sample_worst:.1f} {'PASS' if sample_worst <= LIMIT + 0.05 else 'FAIL'}", flush=True)
    report = {
        "version": 2,
        "rule": "Chief h15: at p10/p25/p50/p75/p90, rod x vs trace x at the top, middle and foot of the gold trace. Worst of the three. Limit 1% of width.",
        "trace_span_y": [280, 920],
        "plate_in_point_s": OFF,
        "source_frame": 109,
        "source_frame_end_inclusive": 150,
        "window_frames": 42,
        "aim_pct": 1.0,
        "limit_px": LIMIT,
        "worst_abs_px": round(worst, 1),
        "align_ok": worst <= LIMIT + 0.05,
        "method": (
            "Rod centre is the midpoint of the dark metal shaft (edge pair, width 8-20 px, "
            "interior luma <= 68). The mid-row shaft anchors the search; top and foot "
            "use the pair whose centre stays within 24 px of that anchor, so the gripping "
            "hand is not counted as the rod. Trace x is the median gold-stroke pixel in "
            "the v06 alpha at that row. Locked alpha bb821f40 was not moved."
        ),
        "samples": samples,
    }
    OUT.write_text(json.dumps(report, indent=2) + "\n")
    print("ALIGN", "PASS" if report["align_ok"] else "FAIL", report["worst_abs_px"], flush=True)
    return report


if __name__ == "__main__":
    measure()
