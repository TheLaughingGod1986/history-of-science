#!/usr/bin/env python3
"""J0882 Step 4: Assemble HOS 006 full_join_v04_teach.mp4 with all 11 Ben changes.

1. Replaces the 12 updated cuts (#03, #10, #14, #15, #16, #35, #36, #55, #59, #66, #88, #91)
   with the newly minted & polish-verified clips in master_v04/clips/.
2. Appends the 24.00 s (576 frames @ 24 fps) moving-picture closing tail (#92..#96, 8:27.83-8:51.83):
   - #92 (8:27.83-8:31.83, 4.00 s): moving golden-hour willow tree with the animated closing card
     naming next week's film ('Why Vaccines Are Named After a Cow', Thu 12 Nov) and channel/related film.
   - #93..#96 (8:31.83-8:51.83, 4 x 5.00 s = 20.00 s): 4 unused moving willow/garden plates for the
     20 s YouTube Studio end screen.
3. Renders and composites all 27 frame-accurate overlays (including all imperial + metric weight
   cards and the 6:07 Geneva, 1782 date/location card) using floating 1440 px walnut/gold house
   cards (zero horizontal split-panel seams).
"""
from __future__ import annotations

import hashlib
import json
import math
import shutil
import subprocess as sp
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H, FPS = 1920, 1080, 24
FONT = "/System/Library/Fonts/Supplemental/Didot.ttc"

REPO = Path("/Users/benjaminoats/YouTube/History Of Science")
PROJ = REPO / "02_Video-Projects/006_Trees-Are-Made-Of-Air"
V02_TEACH_DIR = PROJ / "07_Edit-Project/full_join_v02_teach"
V04_DIR = Path(__file__).resolve().parent
CLIPS_V04_DIR = V04_DIR / "clips"

NAS_MEDIA = Path(
    "/Volumes/data/mac-mini-archive/hos-worktrees/2026-10-22/hos-006-trees/02_Video-Projects/006_Trees-Are-Made-Of-Air"
)
OLD_PREFIX = "/Users/benjaminoats/YouTube/hos-006-trees/02_Video-Projects/006_Trees-Are-Made-Of-Air"

TMP_DIR = Path("/private/tmp/hos006_join_v04")
BASE_JOIN = TMP_DIR / "hos_006_full_join_v04_base.mp4"
OV_OUT_DIR = TMP_DIR / "overlays_v04"
FINAL_OUT = V04_DIR / "hos_006_full_join_v04_teach.mp4"
CUTS_V04_JSON = V04_DIR / "cuts_full_join_v04.json"
POOL_V04_JSON = V04_DIR / "pool_full_join_v04.json"
REVIEWED_OK_V04_JSON = V04_DIR / "picture_qa_reviewed_ok_v04.json"
LAY_JSON = V04_DIR / "LAY_TIMES_v04.json"
RENDER_JSON = V04_DIR / "TEACH_OVERLAYS_RENDER_v04.json"

BROWN = (61, 41, 28)
GOLD = (196, 154, 78)
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

# 27 strictly ordered, frame-aligned overlay specs [start_frame, end_frame) @ 24 fps
SPECS = [
    {
        "id": "who_aristotle", "kind": "who", "cut": 6, "row": "P1 06_aristotle",
        "start_frame": 600, "end_frame": 686, "v01_window": "25.00-28.58",
        "name": "Aristotle", "label": "plants eat soil", "years": "384–322 BC",
        "layout": "lower_third_over_plate", "note": "Inside #06 (0:25.00-0:28.58)",
    },
    {
        "id": "timeline_d1", "kind": "timeline", "drop": 0, "cut": 9, "row": "P1 09_vilvoorde",
        "start_frame": 954, "end_frame": 1031, "v01_window": "39.75-42.96",
        "label": STAMPS[0], "layout": "full_frame_period_paper",
        "note": "Starts on #09 cut (0:39.75-0:42.96)",
    },
    {
        "id": "who_helmont", "kind": "who", "cut": 10, "row": "P1 10_van_helmont_sack",
        "start_frame": 1080, "end_frame": 1166, "v01_window": "45.00-48.58",
        "name": "Jan Baptist van Helmont", "label": "physician and chemist", "years": "1580–1644",
        "layout": "lower_third_over_plate", "note": "Inside #10 (0:45.00-0:48.58) over 10_van_helmont_sack_v04",
    },
    {
        "id": "ch_five_years", "kind": "chapter", "cut": 13, "row": "P2 01_furnace_soil",
        "start_frame": 1480, "end_frame": 1518, "v01_window": "61.67-63.25",
        "label": "Five Years and Two Ounces", "layout": "chapter_cream_on_brown",
        "note": "Part 02 chapter card on #13 cut (1:01.67-1:03.25)",
    },
    {
        "id": "wt_5lb", "kind": "weight", "cut": 15, "row": "P2 03_willow_shoot_scale",
        "start_frame": 1754, "end_frame": 1850, "v01_window": "73.08-77.08",
        "label": "5 lb (about 2.3 kg)", "sub": "young willow tree  ·  starting weight",
        "layout": "lower_third_over_plate",
        "note": "Ben change #3 & #4: 5 lb (about 2.3 kg) on 03_willow_shoot_scale_v04 (1:13.08-1:17.08)",
    },
    {
        "id": "num_169", "kind": "number_dual", "target_lb": 169, "target_kg": 77,
        "cut": 20, "row": "P2 09_weights_169",
        "start_frame": 2564, "end_frame": 2652, "v01_window": "106.83-110.50",
        "label": "169 lb (about 77 kg)", "sub": "after five years  ·  weight of a grown man",
        "layout": "lower_third_over_plate",
        "note": "Ben change #4: 169 lb (about 77 kg) animated counter inside #20 (1:46.83-1:50.50)",
    },
    {
        "id": "fact_leaves", "kind": "fact", "cut": 21, "row": "P2 10_fallen_leaves",
        "start_frame": 2660, "end_frame": 2737, "v01_window": "110.83-114.04",
        "label": "Leaves not weighed", "sub": "four autumns of fallen leaves excluded",
        "layout": "lower_third_over_plate",
        "note": "Inside #21 (1:50.83-1:54.04) when VO says 'didn't even count the leaves'",
    },
    {
        "id": "wt_2oz", "kind": "weight", "cut": 23, "row": "P2 12_pointer_short",
        "start_frame": 2912, "end_frame": 3006, "v01_window": "121.33-125.25",
        "label": "200 lb (about 91 kg)", "sub": "less about 2 oz (about 57 g) of soil",
        "layout": "lower_third_over_plate",
        "note": "Ben change #4: 200 lb (about 91 kg) less about 2 oz (about 57 g) inside #23 (2:01.33-2:05.25)",
    },
    {
        "id": "wt_164lb", "kind": "weight", "cut": 24, "row": "P2 13_tree_vs_pinch",
        "start_frame": 3014, "end_frame": 3108, "v01_window": "125.58-129.50",
        "label": "164 lb (about 74 kg) of new tree", "sub": "only 2 oz (about 57 g) of soil gone",
        "layout": "lower_third_over_plate",
        "note": "Ben change #4: 164 lb (about 74 kg) vs 2 oz (about 57 g) inside #24 (2:05.58-2:09.50)",
    },
    {
        "id": "wt_62lb", "kind": "weight", "cut": 29, "row": "P2 18_charcoal_hearth",
        "start_frame": 3692, "end_frame": 3786, "v01_window": "153.83-157.75",
        "label": "62 lb (about 28 kg) of charcoal", "sub": "burned by van Helmont",
        "layout": "lower_third_over_plate",
        "note": "Ben change #4: 62 lb (about 28 kg) of charcoal inside #29 (2:33.83-2:37.75)",
    },
    {
        "id": "wt_1lb", "kind": "weight", "cut": 30, "row": "P2 19_ash_mound",
        "start_frame": 3793, "end_frame": 3873, "v01_window": "158.04-161.38",
        "label": "1 lb (about 0.45 kg) of ash", "sub": "left behind  ·  the rest became gas",
        "layout": "lower_third_over_plate",
        "note": "Ben change #4: 1 lb (about 0.45 kg) of ash inside #30 (2:38.04-2:41.38)",
    },
    {
        "id": "fact_gas", "kind": "fact", "cut": 32, "row": "P2 21_gas_window",
        "start_frame": 4000, "end_frame": 4077, "v01_window": "166.67-169.88",
        "label": "Coined the word gas", "sub": "from the Greek chaos  ·  mostly CO2",
        "layout": "lower_third_over_plate",
        "note": "Inside #32 (2:46.67-2:49.88) when VO says 'He gave it a new name: gas'",
    },
    {
        "id": "ch_mint", "kind": "chapter", "cut": 34, "row": "P3 01_soil_to_sky",
        "start_frame": 4288, "end_frame": 4326, "v01_window": "178.67-180.25",
        "label": "The Air That Mint Repaired", "layout": "chapter_cream_on_brown",
        "note": "Part 03 chapter card on #34 cut (2:58.67-3:00.25)",
    },
    {
        "id": "timeline_d2", "kind": "timeline", "drop": 1, "cut": 35, "row": "P3 02_hales_branch",
        "start_frame": 4409, "end_frame": 4486, "v01_window": "183.71-186.92",
        "label": STAMPS[1], "layout": "full_frame_period_paper",
        "note": "Sequenced first on #35 cut (3:03.71-3:06.92) when VO says 'Just outside London, in 1727'",
    },
    {
        "id": "who_hales", "kind": "who", "cut": 35, "row": "P3 02_hales_branch",
        "start_frame": 4486, "end_frame": 4565, "v01_window": "186.92-190.21",
        "name": "Stephen Hales", "label": "country parson", "years": "1677–1761",
        "layout": "lower_third_over_plate",
        "note": "Sequenced second inside #35 (3:06.92-3:10.21) over 02_hales_branch_v04",
    },
    {
        "id": "timeline_d3", "kind": "timeline", "drop": 2, "cut": 39, "row": "P3 06_leeds_brewery",
        "start_frame": 4939, "end_frame": 5016, "v01_window": "205.79-209.00",
        "label": STAMPS[2], "layout": "full_frame_period_paper",
        "note": "Starts on #39 cut (3:25.79-3:29.00)",
    },
    {
        "id": "who_priestley", "kind": "who", "cut": 40, "row": "P3 07_priestley",
        "start_frame": 5047, "end_frame": 5133, "v01_window": "210.29-213.88",
        "name": "Joseph Priestley", "label": "Leeds minister", "years": "1733–1804",
        "layout": "lower_third_over_plate",
        "note": "Starts on #40 cut (3:30.29-3:33.88)",
    },
    {
        "id": "ch_bubbles", "kind": "chapter", "cut": 52, "row": "P4 01_villa",
        "start_frame": 6564, "end_frame": 6602, "v01_window": "273.50-275.08",
        "label": "Bubbles in the Sunlight", "layout": "chapter_cream_on_brown",
        "note": "Starts on Part 04 #52 cut (4:33.50-4:35.08)",
    },
    {
        "id": "timeline_d4", "kind": "timeline", "drop": 3, "cut": 52, "row": "P4 01_villa",
        "start_frame": 6631, "end_frame": 6708, "v01_window": "276.29-279.50",
        "label": STAMPS[3], "layout": "full_frame_period_paper",
        "note": "Separated from ch_bubbles by 1.21s moving plate (4:36.29-4:39.50)",
    },
    {
        "id": "who_ingenhousz", "kind": "who", "cut": 53, "row": "P4 02_ingenhousz_jars",
        "start_frame": 6720, "end_frame": 6802, "v01_window": "280.00-283.42",
        "name": "Jan Ingenhousz", "label": "Dutch physician", "years": "1730–1799",
        "layout": "lower_third_over_plate", "note": "Inside #53 (4:40.00-4:43.42)",
    },
    {
        "id": "num_500", "kind": "number", "target": 500, "cut": 53, "row": "P4 02_ingenhousz_jars",
        "start_frame": 6806, "end_frame": 6892, "v01_window": "283.58-287.17",
        "label": "500 experiments", "layout": "lower_third_over_plate",
        "note": "Inside #53 (4:43.58-4:47.17) when VO says 'more than five hundred experiments'",
    },
    {
        "id": "ch_carbon", "kind": "chapter", "cut": 68, "row": "P5 01_geneva_lake",
        "start_frame": 8770, "end_frame": 8808, "v01_window": "365.42-367.00",
        "label": "Carbon From the Sky", "layout": "chapter_cream_on_brown",
        "note": "Part 05 chapter card on #68 cut (6:05.42-6:07.00)",
    },
    {
        "id": "when_geneva_1782", "kind": "when", "cut": 68, "row": "P5 01_geneva_lake",
        "start_frame": 8808, "end_frame": 8876, "v01_window": "367.00-369.83",
        "label": "Geneva, 1782", "sub": "Lake Geneva  ·  Republic of Geneva",
        "layout": "lower_third_over_plate",
        "note": "Ben change #9: 6:07 house WHEN/WHERE card over 01_geneva_lake (6:07.00-6:09.83)",
    },
    {
        "id": "timeline_d5", "kind": "timeline", "drop": 4, "cut": 69, "row": "P5 02_senebier_jars",
        "start_frame": 8878, "end_frame": 8950, "v01_window": "369.92-372.92",
        "label": STAMPS[4], "layout": "full_frame_period_paper",
        "note": "Starts on #69 cut (6:09.92-6:12.92)",
    },
    {
        "id": "who_senebier", "kind": "who", "cut": 69, "row": "P5 02_senebier_jars",
        "start_frame": 8957, "end_frame": 9039, "v01_window": "373.21-376.62",
        "name": "Jean Senebier", "label": "Genevan pastor", "years": "1742–1809",
        "layout": "lower_third_over_plate",
        "note": "Inside #69 (6:13.21-6:16.62) while Senebier sentence finishes",
    },
    {
        "id": "who_saussure", "kind": "who", "cut": 70, "row": "P5 03_de_saussure",
        "start_frame": 9057, "end_frame": 9125, "v01_window": "377.38-380.21",
        "name": "Nicolas-Théodore de Saussure", "label": "Genevan chemist", "years": "1767–1845",
        "layout": "lower_third_over_plate",
        "note": "Starts on #70 cut (6:17.38-6:20.21)",
    },
    {
        "id": "timeline_d6", "kind": "timeline", "drop": 5, "cut": 70, "row": "P5 03_de_saussure",
        "start_frame": 9125, "end_frame": 9201, "v01_window": "380.21-383.38",
        "label": STAMPS[5], "layout": "full_frame_period_paper",
        "note": "Inside #70 (6:20.21-6:23.38), ending cleanly on #70/#71 cut",
    },
    {
        "id": "closing_next_film", "kind": "closing", "cut": 92, "row": "P5 25_closing_card",
        "start_frame": 12190, "end_frame": 12280, "v01_window": "507.92-511.67",
        "label": "Why Vaccines Are Named After a Cow",
        "sub": "Next film  ·  Thursday 12 November  ·  @HistoryOfScienceYT",
        "layout": "lower_third_over_plate",
        "note": "Ben change #10: 8:28 closing line card naming next week's film ('Why Vaccines Are Named After a Cow', Thu 12 Nov) over moving willow plate, followed by 20 s moving end-screen room (#93..#96)",
    },
]


def sha256_file(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def ease(x: float) -> float:
    x = max(0.0, min(1.0, x))
    return x * x * (3 - 2 * x)


def prog(t: float, a: float, b: float) -> float:
    return ease((t - a) / (b - a)) if b > a else 1.0


def font(size: int, italic: bool = True) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(FONT, size, index=1 if italic else 0)


def fit(text: str, max_w: int, size: int, floor: int = 32, italic: bool = True) -> ImageFont.FreeTypeFont:
    f = font(size, italic=italic)
    while size > floor and f.getbbox(text)[2] > max_w:
        size -= 2
        f = font(size, italic=italic)
    return f


def make_paper() -> tuple[np.ndarray, np.ndarray]:
    rng = np.random.default_rng(6)
    small = rng.random((H // 4 + 8, W // 4 + 8)).astype(np.float32)
    paper = np.repeat(np.repeat(small, 4, 0), 4, 1)[:H, :W]
    fine = rng.random((H, W)).astype(np.float32)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
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
    inn = prog(t, 0.10, 0.45)
    out = 1.0 - prog(t, dur - 0.45, dur - 0.08)
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
    """Floating walnut/gold lower-third card with soft-feathered horizontal edges (zero split-panel seams)."""
    a = card_alpha(t, dur)
    if a <= 0.01:
        return base
    im = base.convert("RGBA")
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    slide = int((1 - prog(t, 0.10, 0.45)) * 28)
    bx0, bx1 = 300, 1620
    by0, by1 = 804 + slide, 1020 + slide
    mask = Image.new("L", (W, H), 0)
    md = ImageDraw.Draw(mask)
    md.rounded_rectangle([bx0, by0, bx1, by1], radius=18, fill=int(234 * a))
    mask = mask.filter(ImageFilter.GaussianBlur(radius=6))
    card_fill = Image.new("RGBA", (W, H), (BROWN[0], BROWN[1], BROWN[2], 255))
    ov.paste(card_fill, (0, 0), mask)
    d = ImageDraw.Draw(ov)
    line_a = int(255 * a)
    span = int(360 * prog(t, 0.15, 0.65))
    d.line((W / 2 - span, by0 + 10, W / 2 + span, by0 + 10), fill=(GOLD[0], GOLD[1], GOLD[2], int(200 * a)), width=2)
    d.line((W / 2 - span, by1 - 10, W / 2 + span, by1 - 10), fill=(GOLD[0], GOLD[1], GOLD[2], int(200 * a)), width=2)
    if len(lines) == 1:
        text, size = lines[0]
        f = fit(text, 1240, size, 36)
        d.text((W / 2, (by0 + by1) / 2), text, font=f, fill=(CREAM[0], CREAM[1], CREAM[2], line_a), anchor="mm")
    else:
        y = by0 + 34
        for idx, (text, size) in enumerate(lines):
            f = fit(text, 1240, size, 32)
            col = (CREAM[0], CREAM[1], CREAM[2], line_a) if idx == 0 else (228, 212, 184, line_a)
            d.text((W / 2, y), text, font=f, fill=col, anchor="mt")
            y += size + 18
    return Image.alpha_composite(im, ov).convert("RGB")


def draw_closing_card(base: Image.Image, t: float, dur: float) -> Image.Image:
    """House cream-on-walnut closing card over moving willow plate, naming next week's film."""
    a = card_alpha(t, dur)
    if a <= 0.01:
        return base
    im = base.convert("RGBA")
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    slide = int((1 - prog(t, 0.10, 0.48)) * 28)
    bx0, bx1 = 220, 1700
    by0, by1 = 260 + slide, 820 + slide
    bg_a = int(238 * a)
    fg_a = int(255 * a)
    d.rounded_rectangle(
        [bx0, by0, bx1, by1],
        radius=18,
        fill=(BROWN[0], BROWN[1], BROWN[2], bg_a),
        outline=(GOLD[0], GOLD[1], GOLD[2], fg_a),
        width=4,
    )
    d.rounded_rectangle(
        [bx0 + 16, by0 + 16, bx1 - 16, by1 - 16],
        radius=12,
        outline=(CREAM[0], CREAM[1], CREAM[2], int(150 * a)),
        width=2,
    )
    f_hdr = font(30, italic=False)
    f_sub = font(38, italic=True)
    f_ttl = fit("Why Vaccines Are Named After a Cow", 1360, 68, 44, italic=True)
    f_ftr = font(32, italic=True)

    d.text(
        (W / 2, by0 + 62),
        "HISTORY OF SCIENCE  ·  DISCOVERY. WONDER. PROOF.",
        font=f_hdr,
        fill=(GOLD[0], GOLD[1], GOLD[2], fg_a),
        anchor="mt",
    )
    span = int(460 * prog(t, 0.18, 0.75))
    d.line((W / 2 - span, by0 + 118, W / 2 + span, by0 + 118), fill=(GOLD[0], GOLD[1], GOLD[2], int(190 * a)), width=2)

    d.text(
        (W / 2, by0 + 150),
        "Next film  ·  Thursday 12 November",
        font=f_sub,
        fill=(232, 216, 188, fg_a),
        anchor="mt",
    )
    d.text(
        (W / 2, by0 + 240),
        "Why Vaccines Are Named After a Cow",
        font=f_ttl,
        fill=(CREAM[0], CREAM[1], CREAM[2], fg_a),
        anchor="mt",
    )
    d.line((W / 2 - span, by0 + 365, W / 2 + span, by0 + 365), fill=(GOLD[0], GOLD[1], GOLD[2], int(160 * a)), width=2)
    d.text(
        (W / 2, by0 + 402),
        "Watch on @HistoryOfScienceYT  ·  Up next: What's Really Inside an Atom?",
        font=f_ftr,
        fill=(228, 212, 184, fg_a),
        anchor="mt",
    )
    return Image.alpha_composite(im, ov).convert("RGB")


def draw_number(base: Image.Image, t: float, dur: float, target: int, unit: str) -> Image.Image:
    shown = int(round(target * prog(t, 0.20, 1.50)))
    return draw_band(base, t, dur, [(f"{shown} {unit}", 76)])


def draw_number_dual(base: Image.Image, t: float, dur: float, target_lb: int, target_kg: int, sub: str) -> Image.Image:
    p = prog(t, 0.20, 1.50)
    lb = int(round(target_lb * p))
    kg = int(round(target_kg * p))
    return draw_band(base, t, dur, [(f"{lb} lb (about {kg} kg)", 66), (sub, 38)])


def who_lines(spec: dict) -> list[tuple[str, int]]:
    lines = [(spec["name"], 62)]
    years = spec.get("years")
    role = spec["label"]
    if years and role != years:
        lines.append((f"{years}  ·  {role}", 38))
    else:
        lines.append((role, 38))
    return lines


def open_cut_plate(cuts_v04: list[dict], spec: dict) -> sp.Popen:
    cut_idx = spec["cut"] - 1
    c = cuts_v04[cut_idx]
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


def render_overlay(spec: dict, cuts_v04: list[dict], paper_vig: tuple[np.ndarray, np.ndarray], noise: np.ndarray) -> dict:
    sf = spec["start_frame"]
    ef = spec["end_frame"]
    n = ef - sf
    dur = n / FPS
    path = OV_OUT_DIR / f"code_graphic_006_{spec['id']}_v04.mp4"
    still_path = OV_OUT_DIR / f"code_graphic_006_{spec['id']}_v04.jpg"
    hero = min(n - 1, int(0.55 * n))
    use_plate = spec["layout"] == "lower_third_over_plate"
    plate = open_cut_plate(cuts_v04, spec) if use_plate else None
    last = None
    enc = sp.Popen(
        [
            "ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pixel_format", "rgb24",
            "-video_size", f"{W}x{H}", "-framerate", str(FPS), "-i", "-", "-an",
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
                    frame = draw_number(base, t, dur, spec["target"], "experiments")
                elif spec["kind"] == "number_dual":
                    frame = draw_number_dual(base, t, dur, spec["target_lb"], spec["target_kg"], spec["sub"])
                elif spec["kind"] == "who":
                    frame = draw_band(base, t, dur, who_lines(spec))
                elif spec["kind"] in ("weight", "when", "fact"):
                    sub = spec.get("sub")
                    lines = [(spec["label"], 64), (sub, 38)] if sub else [(spec["label"], 68)]
                    frame = draw_band(base, t, dur, lines)
                elif spec["kind"] == "closing":
                    frame = draw_closing_card(base, t, dur)
                else:
                    frame = draw_band(base, t, dur, [(spec["label"], 68)])
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
        "sub": spec.get("sub"),
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
        "sha256": sha256_file(path),
    }


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


def build_cuts_and_base() -> list[dict]:
    cuts_v02 = json.loads((V02_TEACH_DIR / "cuts_full_join_v02.json").read_text())
    pool_v02 = json.loads((V02_TEACH_DIR / "pool_full_join_v02.json").read_text())

    v04_replacements = {
        3: ("03_pot_jar_leaf_v04.mp4", 180, 1.0, "Flow Nano Banana 2 still + push-in: middle mint in terracotta pot on table (J0882 #1)"),
        10: ("10_van_helmont_sack_v04.mp4", 154, 1.0, "Flow Nano Banana 2 still + push-in: soil sack stays on brass scale (J0882 #2)"),
        14: ("02_balance_200_house_v04.mp4", 140, 1.32, "02_balance_200_t1 top-cropped + imperial & metric counter 200 lb (about 91 kg) (J0882 #4)"),
        15: ("03_willow_shoot_scale_v04.mp4", 103, 1.0, "Flow Nano Banana 2 still + push-in: whole 5-lb willow sapling with roots on scale (J0882 #3)"),
        16: ("04_lid_rain_v04.mp4", 153, 1.0, "Flow Nano Banana 2 still + rain animation: perforated tin-plated iron lid over pot (J0882 #5)"),
        35: ("02_hales_branch_v04.mp4", 156, 1.0, "Flow Nano Banana 2 still + push-in: Stephen Hales with leafy branch upright in glass jar (J0882 #6)"),
        36: ("03_water_level_v04.mp4", 125, 1.0, "Flow Nano Banana 2 still + underwater bubbles: sprig upright in sealed water jar (J0882 #6)"),
        55: ("04_sunny_window_v04.mp4", 109, 1.0, "Flow Nano Banana 2 still + underwater bubbles inside jars on sunny windowsill (J0882 #7)"),
        59: ("08_explorer_shade_v04.mp4", 173, 1.0, "Clean underwater-bubble halves of 08_explorer_shade t2 + t1 joined with 8f xfade (J0882 #7)"),
        66: ("15_leaf_turns_sun_v04.mp4", 70, 1.0, "Smooth push-in on 15_leaf_turns_sun_t1.png with zero plant rotation (J0882 #8)"),
        88: ("21_three_objects_v04.mp4", 123, 1.0, "Flow Nano Banana 2 still + push-in: three containers on table, pot under middle jar (J0882 #1)"),
        91: ("24_gold_foil_crop_v04.mp4", 156, 1.25, "Cropped 24_gold_foil_t1 removing ceiling ATOMOS sign (J0882)"),
    }

    cuts_v04 = []
    cur_frames = 0

    for idx, c in enumerate(cuts_v02):
        row = dict(c)
        cut_num = idx + 1
        sp_str = str(row["source_path"])
        if sp_str.startswith(OLD_PREFIX):
            sp_str = sp_str.replace(OLD_PREFIX, str(NAS_MEDIA), 1)
            row["source_path"] = sp_str

        if cut_num in v04_replacements:
            fname, n_f, up, disp = v04_replacements[cut_num]
            clip_p = CLIPS_V04_DIR / fname
            row["source"] = fname
            row["source_path"] = str(clip_p)
            row["source_sha256"] = sha256_file(clip_p)
            row["frames"] = n_f
            row["upscale"] = up
            row["framing"] = {"offset": 0.0}
            row["disposition"] = disp

        n_frames = int(row["frames"])
        t_in = cur_frames / FPS
        cur_frames += n_frames
        t_out = cur_frames / FPS
        row["film_t"] = round(t_in, 3)
        row["timeline_in"] = t_in
        row["timeline_out"] = t_out
        cuts_v04.append(row)

    assert cur_frames == 12188, f"Expected 12188 frames at end of #91, got {cur_frames}"

    # Append 5 moving-picture closing cuts (#92..#96 = 96 + 4*120 = 576 frames = 24.000 s)
    tail_specs = [
        (
            "25_closing_card",
            NAS_MEDIA / "04_Generated-Clips/flow_vs_vertex_fair_test_20261004/01_willow_air_flow_fast_t1.mp4",
            96,
            "Next-film closing card ('Why Vaccines Are Named After a Cow', Thu 12 Nov) over moving golden-hour willow plate (J0882 #10)",
        ),
        (
            "26_endscreen_01",
            NAS_MEDIA / "04_Generated-Clips/part01/raw/v01/12_garden_sky_t1.mp4",
            120,
            "20 s Studio end-screen room (0-5 s): moving willow sapling in sunny brick garden (J0882 #10)",
        ),
        (
            "27_endscreen_02",
            NAS_MEDIA / "04_Generated-Clips/part02/raw/v01/14_why_grown_t1.mp4",
            120,
            "20 s Studio end-screen room (5-10 s): moving full-grown willow tree in walled garden (J0882 #10)",
        ),
        (
            "28_endscreen_03",
            NAS_MEDIA / "04_Generated-Clips/part02/raw/v01/06_garden_years_lite_t1.mp4",
            120,
            "20 s Studio end-screen room (10-15 s): moving autumn willow leaves in walled garden (J0882 #10)",
        ),
        (
            "29_endscreen_04",
            NAS_MEDIA / "04_Generated-Clips/part01/raw/v01/09_vilvoorde_t1.mp4",
            120,
            "20 s Studio end-screen room (15-20 s): moving Vilvoorde Flemish house and garden trees (J0882 #10)",
        ),
    ]

    for row_name, clip_p, n_f, disp in tail_specs:
        t_in = cur_frames / FPS
        cur_frames += n_f
        t_out = cur_frames / FPS
        cuts_v04.append(
            {
                "row": row_name,
                "film_t": round(t_in, 3),
                "timeline_in": t_in,
                "timeline_out": t_out,
                "frames": n_f,
                "upscale": 1.0,
                "side_label": None,
                "source": clip_p.name,
                "source_path": str(clip_p),
                "source_sha256": sha256_file(clip_p),
                "framing": {"offset": 0.0},
                "disposition": disp,
                "part": 5,
            }
        )

    assert cur_frames == 12764, f"Expected 12764 frames (531.833333 s), got {cur_frames}"

    pool_map = {(p["file"], p["part"]): dict(p) for p in pool_v02}
    for row in cuts_v04:
        key = (row["source"], row["part"])
        if key not in pool_map:
            pool_map[key] = {
                "file": row["source"],
                "title": "HOS 3D cartoon clip, Chief/J0882 KEEP",
                "part": row["part"],
            }
    pool_v04 = list(pool_map.values())

    CUTS_V04_JSON.write_text(json.dumps(cuts_v04, indent=2) + "\n")
    POOL_V04_JSON.write_text(json.dumps(pool_v04, indent=2) + "\n")

    # Copy and update reviewed_ok for the few existing reuse waivers
    rev_ok = json.loads((V02_TEACH_DIR / "picture_qa_reviewed_ok_v02_teach.json").read_text())
    REVIEWED_OK_V04_JSON.write_text(json.dumps(rev_ok, indent=2) + "\n")

    print(f"Wrote {CUTS_V04_JSON.name}: {len(cuts_v04)} cuts, {cur_frames} frames ({cur_frames / FPS:.6f} s)", flush=True)

    if BASE_JOIN.exists() and BASE_JOIN.stat().st_size > 100_000_000:
        print(f"Reusing existing base video join {BASE_JOIN}", flush=True)
        return cuts_v04

    if TMP_DIR.exists():
        shutil.rmtree(TMP_DIR)
    TMP_DIR.mkdir(parents=True, exist_ok=True)

    seg_files = []
    for idx, row in enumerate(cuts_v04):
        clip_path = Path(row["source_path"])
        if not clip_path.exists():
            raise FileNotFoundError(f"Cut #{idx + 1} missing source_path: {clip_path}")
        n_frames = int(row["frames"])
        in_s = float(row.get("framing", {}).get("offset", 0.0))
        seg_out = TMP_DIR / f"seg_{idx:03d}.mp4"
        cut_num = idx + 1
        if cut_num == 53:
            vf = "fps=24,scale=2112:1188:flags=lanczos,crop=1920:1080:96:108,setsar=1,format=yuv420p"
        elif cut_num == 57:
            vf = "fps=24,scale=2048:1152:flags=lanczos,crop=1920:1080:64:0,setsar=1,format=yuv420p"
        elif cut_num == 96:
            # Subtle 0.6 s fade out at the very end of the 20 s end screen (after midpoint)
            vf = "fps=24,scale=1920:1080:flags=lanczos,fade=t=out:st=4.40:d=0.60,setsar=1,format=yuv420p"
        else:
            vf = "fps=24,scale=1920:1080:flags=lanczos,setsar=1,format=yuv420p"
        cmd = ["ffmpeg", "-y", "-v", "error"]
        if in_s > 0.001:
            cmd += ["-ss", f"{in_s:.6f}"]
        cmd += [
            "-i", str(clip_path),
            "-frames:v", str(n_frames),
            "-vf", vf,
            "-c:v", "libx264", "-preset", "veryfast", "-crf", "16",
            "-r", "24", "-an", str(seg_out),
        ]
        sp.run(cmd, check=True)
        seg_files.append(seg_out)

    concat_list = TMP_DIR / "concat.txt"
    concat_list.write_text("".join(f"file '{p}'\n" for p in seg_files))

    sp.run(
        [
            "ffmpeg", "-y", "-v", "error",
            "-f", "concat", "-safe", "0",
            "-i", str(concat_list),
            "-c", "copy", str(BASE_JOIN),
        ],
        check=True,
    )
    for p in seg_files:
        p.unlink(missing_ok=True)

    nb = sp.check_output(
        [
            "ffprobe", "-v", "error", "-count_frames", "-select_streams", "v:0",
            "-show_entries", "stream=nb_read_frames,duration", "-of", "csv=p=0", str(BASE_JOIN),
        ],
        text=True,
    ).strip()
    print(f"Built base video join {BASE_JOIN}: duration,frames={nb}", flush=True)
    return cuts_v04


def main() -> None:
    V04_DIR.mkdir(parents=True, exist_ok=True)
    cuts_v04 = build_cuts_and_base()
    OV_OUT_DIR.mkdir(parents=True, exist_ok=True)

    paper_vig = make_paper()
    noise = np.random.default_rng(6006).random((H, W)).astype(np.float32)

    rendered = []
    for spec in SPECS:
        r = render_overlay(spec, cuts_v04, paper_vig, noise)
        rendered.append(r)
        print(
            f"  {r['id']:18s} #{r['cut']:02d} frames={r['start_frame']:5d}..{r['end_frame']:5d} "
            f"({r['mm_ss']}) -> {r['file']}",
            flush=True,
        )

    for a, b in zip(rendered, rendered[1:]):
        if b["start_frame"] < a["end_frame"]:
            raise RuntimeError(f"Overlap: {a['id']} and {b['id']}")

    save_sheet(rendered, V04_DIR / "teach_laid_sheet_v04.jpg")
    base_sha = sha256_file(BASE_JOIN)

    lay_doc = {
        "job": "J0882",
        "master": str(BASE_JOIN),
        "master_sha256": base_sha,
        "rows": [{k: v for k, v in r.items() if k not in ("path", "still")} for r in rendered],
    }
    LAY_JSON.write_text(json.dumps(lay_doc, indent=2) + "\n")
    RENDER_JSON.write_text(json.dumps(lay_doc, indent=2) + "\n")

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
        "-map", f"[{last}]",
        "-an",
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "17",
        "-pix_fmt", "yuv420p", "-r", "24",
        "-movflags", "+faststart",
        str(FINAL_OUT),
    ]
    print(f"Compositing {len(rendered)} overlays onto {FINAL_OUT} ...", flush=True)
    sp.run(cmd, check=True)

    nb = sp.check_output(
        [
            "ffprobe", "-v", "error", "-count_frames", "-select_streams", "v:0",
            "-show_entries", "stream=nb_read_frames,duration", "-of", "csv=p=0", str(FINAL_OUT),
        ],
        text=True,
    ).strip()
    final_sha = sha256_file(FINAL_OUT)
    (V04_DIR / "SHA256_video_v04.txt").write_text(f"{final_sha}  {FINAL_OUT.name}\n")
    print(f"Built {FINAL_OUT}: duration,frames={nb} sha256={final_sha}", flush=True)


if __name__ == "__main__":
    main()
