#!/usr/bin/env python3
"""J0809: Render the 21 re-timed teach overlays for v02 and composite onto hos_006_full_join_v02_base.mp4.

Applies every overlay timing fix from REVIEW_v01.md §3:
- All chapter cards and full-frame timelines start/end on exact cut boundaries (zero 2-10 frame flashes or spills).
- Part 02 overlays (num_169, fact_leaves, fact_gas) shifted by +5.46..+5.85 s to match restored Part 02 VO sync.
- Part 03 #35 sequences timeline_d2 (3:03.71-3:06.92) first and who_hales (3:06.92-3:10.21) second to match spoken order.
- Part 04 #52 separates ch_bubbles (4:33.50-4:35.08) and timeline_d4 (4:36.29-4:39.50) with 1.21 s of moving 01_villa_t1.mp4.
- Part 04 #53 lays num_500 at 4:43.58-4:47.17 while VO says 'more than five hundred experiments' (no spill into #54).
- Part 05 #68-#70 aligns ch_carbon, timeline_d5, who_senebier, who_saussure, and timeline_d6 to exact cut boundaries.
"""
from __future__ import annotations

import hashlib
import json
import math
import subprocess as sp
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

W, H, FPS = 1920, 1080, 24
FONT = "/System/Library/Fonts/Supplemental/Didot.ttc"

REPO = Path("/Users/benjaminoats/YouTube/History Of Science")
PROJ = REPO / "02_Video-Projects/006_Trees-Are-Made-Of-Air"
V02_DIR = Path(__file__).resolve().parent
TMP_DIR = Path("/private/tmp/hos006_join_v02")
BASE_JOIN = TMP_DIR / "hos_006_full_join_v02_base.mp4"
OV_OUT_DIR = TMP_DIR / "overlays_v02"
FINAL_OUT = V02_DIR / "hos_006_full_join_v02_teach.mp4"
LAY_JSON = V02_DIR / "LAY_TIMES_v02.json"
RENDER_JSON = V02_DIR / "TEACH_OVERLAYS_RENDER_v02.json"

BROWN = (61, 41, 28)
CREAM = (245, 232, 210, 255)
INK = (48, 28, 16, 255)

STAMPS = [
    "Vilvoorde, early 1600s",
    "Teddington, 1727",
    "Leeds, 1771",
    "Near London, 1779",
    "Geneva, 1782",
    "Geneva, 1804",
]

# Exact frame-aligned windows [start_frame, end_frame) @ 24 fps matching REVIEW_v01.md §3
SPECS = [
    {
        "id": "who_aristotle", "kind": "who", "cut": 6, "row": "P1 06_aristotle",
        "start_frame": 600, "end_frame": 686, "v01_window": "25.00-28.58",
        "name": "Aristotle", "label": "plants eat soil", "years": None,
        "layout": "lower_third_over_plate", "note": "KEEP inside #06 (0:25.00-0:28.58)",
    },
    {
        "id": "timeline_d1", "kind": "timeline", "drop": 0, "cut": 9, "row": "P1 09_vilvoorde",
        "start_frame": 954, "end_frame": 1031, "v01_window": "40.00-43.21",
        "label": STAMPS[0], "layout": "full_frame_period_paper",
        "note": "Shifted to start on #09 cut (0:39.75-0:42.96) eliminating 6-frame manor flash",
    },
    {
        "id": "who_helmont", "kind": "who", "cut": 10, "row": "P1 10_van_helmont_sack",
        "start_frame": 1080, "end_frame": 1166, "v01_window": "45.00-48.58",
        "name": "Jan Baptist van Helmont", "label": "physician and chemist", "years": "1580–1644",
        "layout": "lower_third_over_plate", "note": "KEEP inside #10 (0:45.00-0:48.58)",
    },
    {
        "id": "ch_five_years", "kind": "chapter", "cut": 13, "row": "P2 01_furnace_soil",
        "start_frame": 1480, "end_frame": 1518, "v01_window": "62.00-63.58",
        "label": "Five Years and Two Ounces", "layout": "chapter_cream_on_brown",
        "note": "Shifted to start on Part 02 #13 cut (1:01.67-1:03.25) eliminating 8-frame furnace flash",
    },
    {
        "id": "num_169", "kind": "number", "target": 169, "cut": 20, "row": "P2 09_weights_169",
        "start_frame": 2564, "end_frame": 2641, "v01_window": "101.00-104.21",
        "label": "169 pounds", "layout": "lower_third_over_plate",
        "note": "Shifted +5.83s into #20 (1:46.83-1:50.04) on cropped 09_weights_169 when VO says '169 pounds'",
    },
    {
        "id": "fact_leaves", "kind": "fact", "cut": 21, "row": "P2 10_fallen_leaves",
        "start_frame": 2658, "end_frame": 2735, "v01_window": "105.00-108.21",
        "label": "Leaves not weighed", "layout": "lower_third_over_plate",
        "note": "Shifted +5.75s into #21 (1:50.75-1:53.96) when VO says 'didn't even count the leaves'",
    },
    {
        "id": "fact_gas", "kind": "fact", "cut": 32, "row": "P2 21_gas_window",
        "start_frame": 4000, "end_frame": 4077, "v01_window": "161.00-164.21",
        "label": "Coined the word gas", "layout": "lower_third_over_plate",
        "note": "Shifted +5.67s into #32 (2:46.67-2:49.88) when VO says 'He gave it a new name: gas'",
    },
    {
        "id": "ch_mint", "kind": "chapter", "cut": 34, "row": "P3 01_soil_to_sky",
        "start_frame": 4288, "end_frame": 4326, "v01_window": "179.00-180.58",
        "label": "The Air That Mint Repaired", "layout": "chapter_cream_on_brown",
        "note": "Shifted to start on Part 03 #34 cut (2:58.67-3:00.25) eliminating 8-frame sapling flash",
    },
    {
        "id": "timeline_d2", "kind": "timeline", "drop": 1, "cut": 35, "row": "P3 02_hales_branch",
        "start_frame": 4409, "end_frame": 4486, "v01_window": "187.42-190.62",
        "label": STAMPS[1], "layout": "full_frame_period_paper",
        "note": "Sequenced first on #35 cut (3:03.71-3:06.92) when VO says 'Just outside London, in 1727'",
    },
    {
        "id": "who_hales", "kind": "who", "cut": 35, "row": "P3 02_hales_branch",
        "start_frame": 4486, "end_frame": 4565, "v01_window": "184.00-187.42",
        "name": "Stephen Hales", "label": "country parson", "years": "1677–1761",
        "layout": "lower_third_over_plate",
        "note": "Sequenced second inside #35 (3:06.92-3:10.21) when VO says 'Stephen Hales', ending at #35/#36 cut",
    },
    {
        "id": "timeline_d3", "kind": "timeline", "drop": 2, "cut": 39, "row": "P3 06_leeds_brewery",
        "start_frame": 4939, "end_frame": 5016, "v01_window": "206.00-209.21",
        "label": STAMPS[2], "layout": "full_frame_period_paper",
        "note": "Shifted to start on #39 cut (3:25.79-3:29.00) eliminating 5-frame brewery flash",
    },
    {
        "id": "who_priestley", "kind": "who", "cut": 40, "row": "P3 07_priestley",
        "start_frame": 5047, "end_frame": 5133, "v01_window": "210.00-213.58",
        "name": "Joseph Priestley", "label": "Leeds minister", "years": None,
        "layout": "lower_third_over_plate",
        "note": "Shifted to start on #40 cut (3:30.29-3:33.88) eliminating 7-frame spill at tail of #39",
    },
    {
        "id": "ch_bubbles", "kind": "chapter", "cut": 52, "row": "P4 01_villa",
        "start_frame": 6564, "end_frame": 6602, "v01_window": "274.00-275.58",
        "label": "Bubbles in the Sunlight", "layout": "chapter_cream_on_brown",
        "note": "Starts on Part 04 #52 cut (4:33.50-4:35.08), leaving 1.21s of moving 01_villa_t1 before timeline_d4",
    },
    {
        "id": "timeline_d4", "kind": "timeline", "drop": 3, "cut": 52, "row": "P4 01_villa",
        "start_frame": 6631, "end_frame": 6708, "v01_window": "275.58-278.79",
        "label": STAMPS[3], "layout": "full_frame_period_paper",
        "note": "Separated from ch_bubbles by 1.21s moving plate (4:36.29-4:39.50); ends on #52/#53 cut",
    },
    {
        "id": "who_ingenhousz", "kind": "who", "cut": 53, "row": "P4 02_ingenhousz_jars",
        "start_frame": 6720, "end_frame": 6802, "v01_window": "280.00-283.42",
        "name": "Jan Ingenhousz", "label": "Dutch physician", "years": "1730–1799",
        "layout": "lower_third_over_plate", "note": "KEEP inside #53 (4:40.00-4:43.42)",
    },
    {
        "id": "num_500", "kind": "number", "target": 500, "cut": 53, "row": "P4 02_ingenhousz_jars",
        "start_frame": 6806, "end_frame": 6892, "v01_window": "287.00-290.58",
        "label": "500 experiments", "layout": "lower_third_over_plate",
        "note": "Moved into #53 (4:43.58-4:47.17) when VO says 'more than five hundred experiments' (zero spill into #54)",
    },
    {
        "id": "ch_carbon", "kind": "chapter", "cut": 68, "row": "P5 01_geneva_lake",
        "start_frame": 8770, "end_frame": 8808, "v01_window": "365.00-366.58",
        "label": "Carbon From the Sky", "layout": "chapter_cream_on_brown",
        "note": "Shifted to start on Part 05 #68 cut (6:05.42-6:07.00) eliminating 10-frame spill at tail of #67",
    },
    {
        "id": "timeline_d5", "kind": "timeline", "drop": 4, "cut": 69, "row": "P5 02_senebier_jars",
        "start_frame": 8878, "end_frame": 8950, "v01_window": "370.00-373.00",
        "label": STAMPS[4], "layout": "full_frame_period_paper",
        "note": "Shifted to start on #69 cut (6:09.92-6:12.92) eliminating 2-frame flash",
    },
    {
        "id": "who_senebier", "kind": "who", "cut": 69, "row": "P5 02_senebier_jars",
        "start_frame": 8957, "end_frame": 9039, "v01_window": "374.00-377.00",
        "name": "Jean Senebier", "label": "Genevan pastor", "years": "1742–1809",
        "layout": "lower_third_over_plate",
        "note": "Inside #69 (6:13.21-6:16.62) while Senebier sentence finishes",
    },
    {
        "id": "who_saussure", "kind": "who", "cut": 70, "row": "P5 03_de_saussure",
        "start_frame": 9057, "end_frame": 9125, "v01_window": "377.00-380.42",
        "name": "Nicolas-Théodore de Saussure", "label": "1767–1845", "years": "1767–1845",
        "layout": "lower_third_over_plate",
        "note": "Shifted to start on #70 cut (6:17.38-6:20.21) eliminating 9-frame spill at tail of #69",
    },
    {
        "id": "timeline_d6", "kind": "timeline", "drop": 5, "cut": 70, "row": "P5 03_de_saussure",
        "start_frame": 9125, "end_frame": 9201, "v01_window": "380.42-383.62",
        "label": STAMPS[5], "layout": "full_frame_period_paper",
        "note": "Inside #70 (6:20.21-6:23.38), ending cleanly on #70/#71 cut with zero spill into #71",
    },
]


def ease(x: float) -> float:
    x = max(0.0, min(1.0, x))
    return x * x * (3 - 2 * x)


def prog(t: float, a: float, b: float) -> float:
    return ease((t - a) / (b - a)) if b > a else 1.0


def font(size: int, italic: bool = True) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(FONT, size, index=1 if italic else 0)


def fit(text: str, max_w: int, size: int, floor: int = 36) -> ImageFont.FreeTypeFont:
    f = font(size)
    while size > floor and f.getbbox(text)[2] > max_w:
        size -= 2
        f = font(size)
    return f


def make_paper() -> tuple[np.ndarray, np.ndarray]:
    rng = np.random.default_rng(6)
    small = rng.random((H // 4 + 8, W // 4 + 8)).astype(np.float32)
    paper = np.repeat(np.repeat(small, 4, 0), 4, 1)[:H, :W]
    fine = rng.random((H, W)).astype(np.float32)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    # Warm candlelit parchment vignette so luma_std >= 22 (well above polish_gate's 18.0 WARN threshold)
    rad2 = ((xx - W / 2) / (W / 2)) ** 2 + ((yy - H / 2) / (H / 2)) ** 2
    vig = np.clip(1.08 - 0.30 * rad2, 0.62, 1.08)
    return paper * 0.80 + fine * 0.20, vig


def paper_frame(paper_vig: tuple[np.ndarray, np.ndarray], k: int) -> Image.Image:
    paper, vig = paper_vig
    shift = (k // 2) % 40
    rolled = np.roll(np.roll(paper, shift, 1), shift // 3, 0)
    r = (166 + rolled * 56) * vig
    g = (130 + rolled * 44) * vig
    b = (94 + rolled * 30) * vig
    rgb = np.stack([r, g, b], axis=-1).clip(0, 255).astype(np.uint8)
    return Image.fromarray(rgb, "RGB")


def brown_frame(noise: np.ndarray, k: int) -> Image.Image:
    rolled = np.roll(noise, k % 32, 1)
    r = BROWN[0] + (rolled - 0.5) * 18
    g = BROWN[1] + (rolled - 0.5) * 12
    b = BROWN[2] + (rolled - 0.5) * 8
    rgb = np.stack([r, g, b], axis=-1).clip(0, 255).astype(np.uint8)
    return Image.fromarray(rgb, "RGB")


def card_alpha(t: float, dur: float) -> float:
    inn = prog(t, 0.12, 0.48)
    out = 1.0 - prog(t, dur - 0.48, dur - 0.08)
    return max(0.0, min(inn, out))


def draw_timeline(base: Image.Image, t: float, drop: int) -> Image.Image:
    im = base.convert("RGBA")
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    xs = [200 + i * 300 for i in range(6)]
    y = 500
    line_p = 1.0 if drop else prog(t, 0.15, 0.85)
    x1 = 140 + (1780 - 140) * line_p
    d.line((140, y, x1, y), fill=INK, width=6)
    for i in range(drop + 1):
        if xs[i] > x1 + 8 and i == drop:
            continue
        arriving = i == drop
        p = prog(t, 0.35, 1.05) if arriving else 1.0
        dy = int((1 - p) * 70)
        a = int(255 * p)
        ink = (INK[0], INK[1], INK[2], a)
        d.line((xs[i], y - 36 + dy, xs[i], y + 36 + dy), fill=ink, width=5)
        d.ellipse((xs[i] - 11, y - 11 + dy, xs[i] + 11, y + 11 + dy), fill=ink)
        place, _, year = STAMPS[i].partition(", ")
        f_place = fit(place, 280, 54, 40)
        f_year = fit(year, 280, 44, 32)
        d.text((xs[i], y + 58 + dy), place, font=f_place, fill=ink, anchor="mt")
        d.text((xs[i], y + 118 + dy), year, font=f_year, fill=ink, anchor="mt")
    im = Image.alpha_composite(im, ov)
    return im.convert("RGB")


def draw_band(base: Image.Image, t: float, dur: float, lines: list[tuple[str, int]]) -> Image.Image:
    a = card_alpha(t, dur)
    if a <= 0.01:
        return base
    im = base.convert("RGBA")
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    slide = int((1 - prog(t, 0.12, 0.5)) * 36)
    top = 790 + slide
    band_a = int(218 * a)
    d.rectangle((0, top, W, H), fill=(BROWN[0], BROWN[1], BROWN[2], band_a))
    d.line(
        (120, top, 120 + int(1680 * prog(t, 0.15, 0.7)), top),
        fill=(CREAM[0], CREAM[1], CREAM[2], int(255 * a)),
        width=2,
    )
    y = top + 48
    for text, size in lines:
        f = fit(text, 1680, size, 34)
        fill = (CREAM[0], CREAM[1], CREAM[2], int(255 * a))
        d.text((W / 2, y), text, font=f, fill=fill, anchor="mt")
        y += size + 12
    return Image.alpha_composite(im, ov).convert("RGB")


def draw_number(base: Image.Image, t: float, dur: float, target: int, unit: str) -> Image.Image:
    shown = int(round(target * prog(t, 0.25, 1.7)))
    return draw_band(base, t, dur, [(f"{shown} {unit}", 92)])


def draw_chapter(noise: np.ndarray, k: int, t: float, dur: float, title: str) -> Image.Image:
    im = brown_frame(noise, k).convert("RGBA")
    a = card_alpha(t, dur)
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    f = fit(title, 1600, 78, 48)
    fill = (CREAM[0], CREAM[1], CREAM[2], int(255 * a))
    d.text((W / 2, H / 2), title, font=f, fill=fill, anchor="mm")
    span = int(420 * prog(t, 0.2, 0.75))
    rule = (CREAM[0], CREAM[1], CREAM[2], int(180 * a))
    d.line((W / 2 - span, H / 2 - 80, W / 2 + span, H / 2 - 80), fill=rule, width=2)
    d.line((W / 2 - span, H / 2 + 80, W / 2 + span, H / 2 + 80), fill=rule, width=2)
    return Image.alpha_composite(im, ov).convert("RGB")


def who_lines(spec: dict) -> list[tuple[str, int]]:
    lines = [(spec["name"], 64)]
    years = spec.get("years")
    role = spec["label"]
    if years and role != years:
        lines.append((f"{years}  ·  {role}", 40))
    else:
        lines.append((role, 40))
    return lines


def open_cut_plate(cuts_v02: list[dict], spec: dict) -> sp.Popen:
    cut_idx = spec["cut"] - 1
    c = cuts_v02[cut_idx]
    cut_start_f = int(round(c["timeline_in"] * FPS))
    cut_end_f = int(round(c["timeline_out"] * FPS))
    sf = spec["start_frame"]
    ef = spec["end_frame"]
    assert cut_start_f <= sf and ef <= cut_end_f, (
        f"{spec['id']} [{sf}..{ef}] outside cut #{spec['cut']} [{cut_start_f}..{cut_end_f}]"
    )
    rel_sf = sf - cut_start_f
    rel_ef = ef - cut_start_f
    in_s = float(c.get("framing", {}).get("offset", 0.0))
    if spec["cut"] == 53:
        scale_vf = "scale=2112:1188:flags=lanczos,crop=1920:1080:96:108"
    else:
        scale_vf = "scale=1920:1080:flags=lanczos"
    cmd = ["ffmpeg", "-v", "error"]
    if in_s > 0.001:
        cmd += ["-ss", f"{in_s:.6f}"]
    cmd += [
        "-i", str(c["source_path"]),
        "-vf", f"fps=24,trim=start_frame={rel_sf}:end_frame={rel_ef},setpts=PTS-STARTPTS,{scale_vf}",
        "-f", "rawvideo", "-pix_fmt", "rgb24", "-",
    ]
    return sp.Popen(cmd, stdout=sp.PIPE)


def read_frame(proc: sp.Popen, last: Image.Image | None) -> Image.Image | None:
    buf = proc.stdout.read(W * H * 3) if proc.stdout else b""
    if len(buf) < W * H * 3:
        return last
    return Image.frombytes("RGB", (W, H), buf)


def render_overlay(spec: dict, cuts_v02: list[dict], paper_vig: tuple[np.ndarray, np.ndarray], noise: np.ndarray) -> dict:
    sf = spec["start_frame"]
    ef = spec["end_frame"]
    n = ef - sf
    dur = n / FPS
    path = OV_OUT_DIR / f"code_graphic_006_{spec['id']}_v02.mp4"
    still_path = OV_OUT_DIR / f"code_graphic_006_{spec['id']}_v02.jpg"
    hero = min(n - 1, int(0.55 * n))
    use_plate = spec["layout"] == "lower_third_over_plate"
    plate = open_cut_plate(cuts_v02, spec) if use_plate else None
    last = None
    enc = sp.Popen(
        [
            "ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pixel_format", "rgb24",
            " -video_size".strip(), f"{W}x{H}", "-framerate", str(FPS), "-i", "-", "-an",
            "-c:v", "libx264", "-preset", "veryfast", "-crf", "17", "-pix_fmt", "yuv420p",
            str(path),
        ],
        stdin=sp.PIPE,
    )
    try:
        for k in range(n):
            t = k / FPS
            if spec["kind"] == "timeline":
                frame = draw_timeline(paper_frame(paper_vig, k), t, spec["drop"])
            elif spec["kind"] == "chapter":
                frame = draw_chapter(noise, k, t, dur, spec["label"])
            else:
                if plate is not None:
                    last = read_frame(plate, last)
                base = last if last is not None else paper_frame(paper_vig, k)
                if spec["kind"] == "number":
                    unit = "pounds" if spec["target"] == 169 else "experiments"
                    frame = draw_number(base, t, dur, spec["target"], unit)
                elif spec["kind"] == "who":
                    frame = draw_band(base, t, dur, who_lines(spec))
                else:
                    frame = draw_band(base, t, dur, [(spec["label"], 72)])
            if k == hero:
                frame.save(still_path, quality=90)
            enc.stdin.write(frame.tobytes())
    finally:
        if enc.stdin:
            enc.stdin.close()
        if enc.wait() != 0:
            raise RuntimeError(f"ffmpeg failed for {spec['id']}")
        if plate is not None:
            if plate.stdout:
                plate.stdout.close()
            plate.wait()

    start_s = sf / FPS
    end_s = ef / FPS
    return {
        "id": spec["id"],
        "kind": spec["kind"],
        "cut": spec["cut"],
        "row": spec["row"],
        "file": path.name,
        "path": str(path),
        "still": str(still_path),
        "layout": spec["layout"],
        "label": spec["label"],
        "name": spec.get("name"),
        "years": spec.get("years"),
        "v01_window": spec["v01_window"],
        "start_frame": sf,
        "end_frame": ef,
        "frames": n,
        "start": round(start_s, 6),
        "end": round(end_s, 6),
        "dur": round(dur, 6),
        "mm_ss": f"{int(start_s // 60)}:{start_s % 60:05.2f}–{int(end_s // 60)}:{end_s % 60:05.2f}",
        "note": spec["note"],
        "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
    }


def save_sheet(rows: list[dict], out_jpg: Path) -> None:
    cols = 5
    tw, th = 384, 216
    rows_n = math.ceil(len(rows) / cols)
    im = Image.new("RGB", (cols * tw, rows_n * (th + 28)), BROWN)
    d = ImageDraw.Draw(im)
    f = font(16)
    for i, rec in enumerate(rows):
        still = Image.open(rec["still"]).resize((tw, th))
        x, y = (i % cols) * tw, (i // cols) * (th + 28)
        im.paste(still, (x, y))
        d.text((x + 6, y + th + 4), f"{rec['mm_ss']} {rec['id']}", font=f, fill=CREAM)
    im.save(out_jpg, quality=90)


def main() -> None:
    OV_OUT_DIR.mkdir(parents=True, exist_ok=True)
    V02_DIR.mkdir(parents=True, exist_ok=True)
    cuts_v02 = json.loads((V02_DIR / "cuts_full_join_v02.json").read_text())

    paper_vig = make_paper()
    noise = np.random.default_rng(6006).random((H, W)).astype(np.float32)

    rendered = []
    for spec in SPECS:
        r = render_overlay(spec, cuts_v02, paper_vig, noise)
        rendered.append(r)
        print(f"  {r['id']:16s} #{r['cut']:02d} frames={r['start_frame']:4d}..{r['end_frame']:4d} ({r['mm_ss']}) -> {r['file']}", flush=True)

    # Verify strict monotonic ordering and zero overlap
    for a, b in zip(rendered, rendered[1:]):
        if b["start_frame"] < a["end_frame"]:
            raise RuntimeError(f"Overlap: {a['id']} and {b['id']}")

    save_sheet(rendered, V02_DIR / "teach_laid_sheet_v02.jpg")
    base_sha = hashlib.sha256(BASE_JOIN.read_bytes()).hexdigest()

    lay_doc = {
        "job": "J0809",
        "master": str(BASE_JOIN),
        "master_sha256": base_sha,
        "audio": "copy of full_join_v01_teach; no bed",
        "rows": [{k: v for k, v in r.items() if k not in ("path", "still")} for r in rendered],
    }
    LAY_JSON.write_text(json.dumps(lay_doc, indent=2) + "\n")
    RENDER_JSON.write_text(json.dumps(lay_doc, indent=2) + "\n")

    # Composite all 21 overlays onto BASE_JOIN with frame-exact enable='between(n,sf,ef-1)'
    cmd = ["ffmpeg", "-y", "-v", "error", "-i", str(BASE_JOIN)]
    for r in rendered:
        cmd += ["-i", r["path"]]

    parts = ["[0:v]format=yuv420p[v0]"]
    for i, r in enumerate(rendered):
        sf = r["start_frame"]
        ef = r["end_frame"]
        start_s = sf / FPS
        parts.append(f"[{i + 1}:v]fps=24,setpts=PTS-STARTPTS+{start_s:.6f}/TB,format=yuv420p[o{i}]")
        parts.append(
            f"[v{i}][o{i}]overlay=x=0:y=0:eof_action=pass:repeatlast=0:shortest=0:"
            f"enable='between(n,{sf},{ef - 1})'[v{i + 1}]"
        )
    last = f"v{len(rendered)}"
    cmd += [
        "-filter_complex", ";".join(parts),
        "-map", f"[{last}]", "-map", "0:a",
        "-c:a", "copy",
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "17",
        "-pix_fmt", "yuv420p", "-r", "24",
        "-movflags", "+faststart",
        str(FINAL_OUT),
    ]
    print(f"Compositing 21 overlays onto {FINAL_OUT} ...", flush=True)
    sp.run(cmd, check=True)

    nb = sp.check_output(
        [
            "ffprobe", "-v", "error", "-count_frames", "-select_streams", "v:0",
            "-show_entries", "stream=nb_read_frames,duration", "-of", "csv=p=0", str(FINAL_OUT),
        ],
        text=True,
    ).strip()
    final_sha = hashlib.sha256(FINAL_OUT.read_bytes()).hexdigest()
    (V02_DIR / "SHA256.txt").write_text(f"{final_sha}  hos_006_full_join_v02_teach.mp4\n")
    print(f"Built {FINAL_OUT}: duration,frames={nb} sha256={final_sha}", flush=True)


if __name__ == "__main__":
    main()
