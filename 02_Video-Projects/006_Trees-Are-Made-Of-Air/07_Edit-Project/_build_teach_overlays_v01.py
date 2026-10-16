#!/usr/bin/env python3
"""J0332: HOS 006 £0 teach overlays from TEACH_OVERLAYS_v01.md.

Chief (16 Oct): no full_join_v02. Times are the v01 film clock.
House only: cream Didot italic on brown, or ink on moving period paper.
Silent. No bed, no mint, no spoken-line changes.

WHO, FACT and number cards are lower thirds over a moving excerpt of
full_join_v01 (review composite). The timeline and the chapter cards are
full-frame house graphics. The edit lays them; this does not recut the join.

Where a WHO card and a timeline drop share a time, they are separate assets.
Lay the WHO card, then the timeline marker. Do not stack them.
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
JOIN = Path(
    "/Volumes/data/mac-mini-archive/YouTube/History Of Science/"
    "02_Video-Projects/006_Trees-Are-Made-Of-Air/07_Edit-Project/"
    "full_join_v01/hos_006_full_join_v01.mp4"
)
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
STAMP_AT = [40.0, 184.0, 206.0, 274.0, 370.0, 377.0]

# label = the 4-word line (role, stamp, fact, or number). name is line one of a WHO card.
SPECS = [
    {"id": "timeline_d1", "kind": "timeline", "drop": 0, "film_s": 40.0, "dur": 3.2, "label": STAMPS[0], "layout": "full_frame_period_paper"},
    {"id": "timeline_d2", "kind": "timeline", "drop": 1, "film_s": 184.0, "dur": 3.2, "label": STAMPS[1], "layout": "full_frame_period_paper", "lay": "After the Stephen Hales WHO card. Not stacked with it."},
    {"id": "timeline_d3", "kind": "timeline", "drop": 2, "film_s": 206.0, "dur": 3.2, "label": STAMPS[2], "layout": "full_frame_period_paper"},
    {"id": "timeline_d4", "kind": "timeline", "drop": 3, "film_s": 274.0, "dur": 3.2, "label": STAMPS[3], "layout": "full_frame_period_paper", "lay": "After the chapter card Bubbles in the Sunlight. Not stacked with it."},
    {"id": "timeline_d5", "kind": "timeline", "drop": 4, "film_s": 370.0, "dur": 3.0, "label": STAMPS[4], "layout": "full_frame_period_paper"},
    {"id": "timeline_d6", "kind": "timeline", "drop": 5, "film_s": 377.0, "dur": 3.2, "label": STAMPS[5], "layout": "full_frame_period_paper", "lay": "After the de Saussure WHO card. The 1804 stamp is this marker, not a second line on the card."},
    {"id": "num_169", "kind": "number", "film_s": 101.0, "dur": 3.2, "label": "169 pounds", "target": 169, "layout": "lower_third_over_plate", "row": "P2 09_weights_169"},
    {"id": "num_500", "kind": "number", "film_s": 287.0, "dur": 3.6, "label": "500 experiments", "target": 500, "layout": "lower_third_over_plate", "row": "P4 03_plunge_leaf", "lay": "Next row after the Ingenhousz WHO card, so the two are not stacked."},
    {"id": "who_aristotle", "kind": "who", "film_s": 25.0, "dur": 3.6, "name": "Aristotle", "label": "plants eat soil", "layout": "lower_third_over_plate", "row": "P1 06_aristotle", "years": None},
    {"id": "who_helmont", "kind": "who", "film_s": 45.0, "dur": 3.6, "name": "Jan Baptist van Helmont", "label": "physician and chemist", "years": "1580–1644", "layout": "lower_third_over_plate", "row": "P1 10_van_helmont_sack"},
    {"id": "who_hales", "kind": "who", "film_s": 184.0, "dur": 3.4, "name": "Stephen Hales", "label": "country parson", "years": "1677–1761", "layout": "lower_third_over_plate", "row": "P3 02_hales_branch", "lay": "Name and years first. Timeline marker Teddington, 1727 after this card."},
    {"id": "who_priestley", "kind": "who", "film_s": 210.0, "dur": 3.6, "name": "Joseph Priestley", "label": "Leeds minister", "layout": "lower_third_over_plate", "row": "P3 07_priestley", "years": None},
    {"id": "who_ingenhousz", "kind": "who", "film_s": 280.0, "dur": 3.4, "name": "Jan Ingenhousz", "label": "Dutch physician", "years": "1730–1799", "layout": "lower_third_over_plate", "row": "P4 02_ingenhousz_jars"},
    {"id": "who_senebier", "kind": "who", "film_s": 374.0, "dur": 3.4, "name": "Jean Senebier", "label": "Genevan pastor", "years": "1742–1809", "layout": "lower_third_over_plate", "row": "P5 02_senebier_jars"},
    {"id": "who_saussure", "kind": "who", "film_s": 377.0, "dur": 3.4, "name": "Nicolas-Théodore de Saussure", "label": "1767–1845", "years": "1767–1845", "layout": "lower_third_over_plate", "row": "P5 03_de_saussure", "lay": "Line two is the years only. FACT_NOTES names no role. Timeline marker follows."},
    {"id": "fact_leaves", "kind": "fact", "film_s": 105.0, "dur": 3.2, "label": "Leaves not weighed", "layout": "lower_third_over_plate", "row": "P2 10_fallen_leaves"},
    {"id": "fact_gas", "kind": "fact", "film_s": 161.0, "dur": 3.2, "label": "Coined the word gas", "layout": "lower_third_over_plate", "row": "P2 21_gas_window"},
    {"id": "ch_five_years", "kind": "chapter", "film_s": 62.0, "dur": 1.6, "label": "Five Years and Two Ounces", "layout": "chapter_cream_on_brown"},
    {"id": "ch_mint", "kind": "chapter", "film_s": 179.0, "dur": 1.6, "label": "The Air That Mint Repaired", "layout": "chapter_cream_on_brown"},
    {"id": "ch_bubbles", "kind": "chapter", "film_s": 274.0, "dur": 1.6, "label": "Bubbles in the Sunlight", "layout": "chapter_cream_on_brown", "lay": "Then the Near London, 1779 timeline marker. Not stacked."},
    {"id": "ch_carbon", "kind": "chapter", "film_s": 365.0, "dur": 1.6, "label": "Carbon From the Sky", "layout": "chapter_cream_on_brown"},
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


def word_count(text: str) -> int:
    cleaned = text.replace("·", " ").replace(",", " ").replace("—", " ").replace("-", " ")
    return len([w for w in cleaned.split() if w])


def clock(seconds: float) -> str:
    s = int(round(seconds))
    return f"{s // 60}:{s % 60:02d}"


def make_paper() -> np.ndarray:
    rng = np.random.default_rng(6)
    small = rng.random((H // 4 + 8, W // 4 + 8)).astype(np.float32)
    paper = np.repeat(np.repeat(small, 4, 0), 4, 1)[:H, :W]
    fine = rng.random((H, W)).astype(np.float32)
    return paper * 0.85 + fine * 0.15


def paper_frame(paper: np.ndarray, k: int) -> Image.Image:
    shift = (k // 2) % 40
    rolled = np.roll(np.roll(paper, shift, 1), shift // 3, 0)
    r = 168 + rolled * 48
    g = 132 + rolled * 36
    b = 96 + rolled * 22
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


def open_plate(start_s: float, n: int) -> sp.Popen:
    return sp.Popen(
        [
            "ffmpeg", "-v", "error", "-ss", f"{start_s:.3f}", "-i", str(JOIN),
            "-frames:v", str(n), "-vf", "scale=1920:1080,fps=24",
            "-f", "rawvideo", "-pix_fmt", "rgb24", "-",
        ],
        stdout=sp.PIPE,
    )


def read_frame(proc: sp.Popen, last: Image.Image | None) -> Image.Image | None:
    buf = proc.stdout.read(W * H * 3) if proc.stdout else b""
    if len(buf) < W * H * 3:
        return last
    return Image.frombytes("RGB", (W, H), buf)


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
    d.line((120, top, 120 + int(1680 * prog(t, 0.15, 0.7)), top), fill=(CREAM[0], CREAM[1], CREAM[2], int(255 * a)), width=2)
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


def render(spec: dict, paper: np.ndarray, noise: np.ndarray, out: Path) -> dict:
    n = max(8, int(round(spec["dur"] * FPS)))
    path = out / f"code_graphic_006_{spec['id']}.mp4"
    still_path = out / f"code_graphic_006_{spec['id']}.jpg"
    hero = min(n - 1, int(0.55 * n))
    use_plate = spec["layout"] == "lower_third_over_plate" and JOIN.exists()
    plate = open_plate(spec["film_s"], n) if use_plate else None
    last = None
    enc = sp.Popen(
        [
            "ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pixel_format", "rgb24",
            "-video_size", f"{W}x{H}", "-framerate", str(FPS), "-i", "-", "-an",
            "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p",
            "-movflags", "+faststart", str(path),
        ],
        stdin=sp.PIPE,
    )
    min_mean, min_p95 = 999.0, 999.0
    try:
        for k in range(n):
            t = k / FPS
            if spec["kind"] == "timeline":
                frame = draw_timeline(paper_frame(paper, k), t, spec["drop"])
            elif spec["kind"] == "chapter":
                frame = draw_chapter(noise, k, t, spec["dur"], spec["label"])
            else:
                if plate is not None:
                    last = read_frame(plate, last)
                base = last if last is not None else paper_frame(paper, k)
                if spec["kind"] == "number":
                    unit = "pounds" if spec["target"] == 169 else "experiments"
                    frame = draw_number(base, t, spec["dur"], spec["target"], unit)
                elif spec["kind"] == "who":
                    frame = draw_band(base, t, spec["dur"], who_lines(spec))
                else:
                    frame = draw_band(base, t, spec["dur"], [(spec["label"], 72)])
            if k % 12 == 0 or k == hero:
                g = np.asarray(frame.convert("L"))
                min_mean = min(min_mean, float(g.mean()))
                min_p95 = min(min_p95, float(np.percentile(g, 95)))
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
    label_words = word_count(spec["label"])
    if spec["kind"] == "chapter":
        label_words_rule = "chapter title, one line"
    elif spec["kind"] == "who":
        label_words_rule = "role line" if spec.get("years") != spec["label"] else "years only"
    else:
        label_words_rule = "label"
    rec = {
        "id": spec["id"],
        "kind": spec["kind"],
        "file": path.name,
        "still": still_path.name,
        "film_s": spec["film_s"],
        "film_clock": clock(spec["film_s"]),
        "row": spec.get("row"),
        "duration_s": spec["dur"],
        "fps": FPS,
        "width": W,
        "height": H,
        "label": spec["label"],
        "name": spec.get("name"),
        "years": spec.get("years"),
        "label_words": label_words,
        "label_words_rule": label_words_rule,
        "layout": spec["layout"],
        "lay": spec.get("lay", ""),
        "background": "moving full_join_v01 excerpt" if use_plate and last is not None else spec["layout"],
        "min_sample_mean_luma": round(min_mean, 2),
        "min_sample_p95": round(min_p95, 2),
        "near_black": "PASS" if (min_mean >= 28 or min_p95 >= 50) else "FAIL",
        "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        "bytes": path.stat().st_size,
    }
    limit = 12 if spec["kind"] == "chapter" else 4
    rec["words_ok"] = label_words <= limit
    return rec


def sheet(out: Path, rows: list[dict]) -> None:
    cols = 5
    tw, th = 384, 216
    rows_n = math.ceil(len(rows) / cols)
    im = Image.new("RGB", (cols * tw, rows_n * (th + 28)), BROWN)
    d = ImageDraw.Draw(im)
    f = font(16)
    for i, rec in enumerate(rows):
        still = Image.open(out / rec["still"]).resize((tw, th))
        x, y = (i % cols) * tw, (i // cols) * (th + 28)
        im.paste(still, (x, y))
        d.text((x + 6, y + th + 4), f"{rec['film_clock']}  {rec['label'][:42]}", font=f, fill=CREAM)
    im.save(out / "teach_overlays_v01_sheet.jpg", quality=90)


def main() -> None:
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--only", default="")
    args = ap.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    want = set(a for a in args.only.split(",") if a)
    for spec in SPECS:
        if spec["kind"] == "chapter":
            continue
        n = word_count(spec["label"])
        if n > 4:
            raise SystemExit(f"{spec['id']} label has {n} words: {spec['label']}")
        if spec["kind"] == "who" and spec.get("years") is None and any(ch.isdigit() for ch in spec["label"]):
            raise SystemExit(f"{spec['id']} prints a year that FACT_NOTES does not give")
    paper = make_paper()
    noise = np.random.default_rng(6006).random((H, W)).astype(np.float32)
    rows = []
    for spec in SPECS:
        if want and spec["id"] not in want:
            continue
        print("Rendering", spec["id"], flush=True)
        rows.append(render(spec, paper, noise, args.out))
    if not want:
        sheet(args.out, rows)
    doc = {
        "job": "J0332",
        "master": "hos_006_full_join_v01.mp4",
        "master_sha256": "7bf649f857acc6a66b88347dd5351fb183c73a491f268e7543e14efc5155cde6",
        "source": "TEACH_OVERLAYS_v01.md",
        "style": "cream Didot italic on brown, or ink timeline on moving period paper",
        "audio": "silent",
        "spend": 0,
        "rows": rows,
    }
    (args.out / "TEACH_OVERLAYS_RENDER_v01.json").write_text(json.dumps(doc, indent=2) + "\n")
    fails = [r["id"] for r in rows if r["near_black"] != "PASS" or not r["words_ok"]]
    print("done", len(rows), "fails", fails or "none", flush=True)
    if fails:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
