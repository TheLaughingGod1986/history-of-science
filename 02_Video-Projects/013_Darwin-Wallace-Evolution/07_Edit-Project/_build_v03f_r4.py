#!/usr/bin/env python3
"""J2652 (v03f-r4): Polish all 35 £0 free graphics per Claude review #6945397541 & Chief #6957443445.

Fixes all three items from Claude's 390px sheet review while preserving v01/v02/v03..v03f_r3 untouched:
1. Unclips all bottom-left archival source credit lines (eliminating [:52] truncation on P2:12a, P3:10a, P4:06b,
   P5:05b, P5:09, P6:04b) so every credit ends on a full word/year and fits with >=600px horizontal margin.
2. Enlarges bottom-left credits (28 -> 40px white Didot italic with dark drop-shadow + 1px stroke weight so thin
   Didot hairlines survive 1920->390 downsampling) and enlarges small labels/tags across the set:
   - Anchored top-left badges (incl. '1,250 COPIES PRE-SOLD'): 54 -> 62px
   - WHO lower-third cards: 48/34 -> 54/42px
   - P1:10 year & page tags ('1844 / 230 PAGES', '1858 / PACKET'): 34px floating -> 58/46px in dark house panel
   - P3:03 'OFFSPRING BORN' & 'FOOD SUPPLY': 40 -> 58/56px
   - P5:07 timeline years (36 -> 48px) & secondary chart labels across P1:08, P2:06b, P2:09, P2:10b, P3:06,
     P3:09a, P3:12, P4:05, P4:07b, P5:02b, P5:04b, P6:03 (34-44 -> 46-56px).
3. Verifies P2:01_card_p02 renders 'Part II / The Birds He Forgot to Label' across chapter_title_window_s
   [75.12, 77.62] (0.00-2.50s), samples P2:01's contact-sheet hero frame at t=1.25s (mid-title window), and
   writes CHAPTER_WINDOWS_v03f_r4_390px.jpg showing both windows (t=1.25s title + post-title motif/WHO) for P2..P6.
4. Runs polish_gate.py + picture_qa.py on the 35-clip v03f-r4 reel and builds the 515s v03f-r4 NAS diagnostic rough.
"""
from __future__ import annotations

import collections
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
import json
import math
import os
from pathlib import Path
import shutil
import subprocess as sp
import textwrap

import numpy as np
from PIL import Image, ImageDraw, ImageFont

import _build_code_graphics_v03f as base_cg

W, H, FPS = base_cg.W, base_cg.H, base_cg.FPS
EDIT = Path(__file__).resolve().parent
FILM = EDIT.parent
OUT = EDIT / "timing_rough_J2652"
GIT_CG = EDIT / "code_graphics_v03f"
NAS_FILM = Path("/Volumes/data/studio-live/History Of Science/02_Video-Projects") / FILM.name
NAS_CG = NAS_FILM / "07_Edit-Project/code_graphics_v03f"
NAS_ROUGH = NAS_FILM / "07_Edit-Project/timing_rough_J2652"
OWB_ROOT = Path("/Users/benjaminoats/YouTube/orbit-with-ben")
SCRATCH = Path(os.environ.get("STUDIO_SCRATCH", "/private/tmp")) / "J2652-render-v03f-r4"
ARIAL_FONT = "/System/Library/Fonts/Supplemental/Arial.ttf"

CREAM = base_cg.CREAM
GOLD = base_cg.GOLD
PALE = base_cg.PALE
TAN = base_cg.TAN
CLAY = base_cg.CLAY
WHITE = base_cg.WHITE
TEAL = base_cg.TEAL
CRIMSON = base_cg.CRIMSON
DARK_INK = base_cg.DARK_INK

ARCHIVE_CREDITS: dict[str, str] = {
    "darwin_tree_1837": "Cambridge University Library · MS DAR 121:36 (1837)",
    "gould_finches_1845": "John Gould · Journal of Researches (1845)",
    "vestiges_1844_title": "Robert Chambers · Vestiges of the Natural History of Creation (1844)",
    "malthus_1798_title": "Thomas Robert Malthus · Principle of Population, 1st ed. (1798)",
    "who_joseph_hooker": "Joseph Hooker · Kilburn daguerreotype (c. 1852)",
    "origin_1859_title": "Charles Darwin · On the Origin of Species, 1st ed. (1859)",
    "darwinism_1889_title": "Alfred Russel Wallace · Darwinism, 1st ed. (1889)",
    "mendel_1866_paper": "Gregor Mendel · Versuche über Pflanzen-Hybriden (1866)",
}

PENDING_RETAKE_ROWS = {
    "P1:03a_unlabelled_birds",
    "P1:07_darwin_1837_desk",
    "P3:02a_malthus_lamplight",
}


def fnt(size: int, italic: bool = False, bold: bool = False) -> ImageFont.FreeTypeFont:
    return base_cg.fnt(size, italic=italic, bold=bold)


def ease(u: float) -> float:
    return base_cg.ease(u)


def prog(t: float, a: float, b: float) -> float:
    return base_cg.prog(t, a, b)


def text_wh(d: ImageDraw.ImageDraw, txt: str, font: ImageFont.FreeTypeFont, stroke: int = 1) -> tuple[int, int]:
    if "→" in txt:
        parts = [p.strip() for p in txt.split("→")]
        arrow_span = int(font.size * 1.35)
        widths = []
        max_h = 0
        for p in parts:
            b = d.textbbox((0, 0), p, font=font, stroke_width=stroke)
            widths.append(b[2] - b[0])
            max_h = max(max_h, b[3] - b[1])
        return sum(widths) + arrow_span * (len(parts) - 1), max_h
    b = d.textbbox((0, 0), txt, font=font, stroke_width=stroke)
    return b[2] - b[0], b[3] - b[1]


def _draw_vector_arrow(
    d: ImageDraw.ImageDraw,
    x0: int,
    cy: int,
    span: int,
    size: int,
    fill: tuple[int, int, int],
    shadow: bool = True,
) -> None:
    pad = max(12, int(size * 0.22))
    ax0, ax1 = x0 + pad, x0 + span - pad
    head_len = max(14, int(size * 0.28))
    head_half = max(8, int(size * 0.17))
    w = max(4, int(round(size * 0.08)))
    if shadow:
        sc = (22, 17, 13)
        d.line((ax0 + 2, cy + 2, ax1 - head_len // 2 + 2, cy + 2), fill=sc, width=w)
        d.polygon([(ax1 + 2, cy + 2), (ax1 - head_len + 2, cy - head_half + 2), (ax1 - head_len + 2, cy + head_half + 2)], fill=sc)
    d.line((ax0, cy, ax1 - head_len // 2, cy), fill=fill, width=w)
    d.polygon([(ax1, cy), (ax1 - head_len, cy - head_half), (ax1 - head_len, cy + head_half)], fill=fill)


def draw_crisp_text(
    d: ImageDraw.ImageDraw,
    xy: tuple[int, int],
    txt: str,
    font: ImageFont.FreeTypeFont,
    fill: tuple[int, int, int],
    shadow: bool = True,
    stroke: int = 1,
) -> None:
    x, y = xy
    if "→" in txt:
        parts = [p.strip() for p in txt.split("→")]
        arrow_span = int(font.size * 1.35)
        ref_b = d.textbbox((0, y), "H", font=font, stroke_width=stroke)
        mid_y = (ref_b[1] + ref_b[3]) // 2
        cur_x = x
        for i, p in enumerate(parts):
            if p:
                draw_crisp_text(d, (cur_x, y), p, font, fill, shadow=shadow, stroke=stroke)
                pb = d.textbbox((0, 0), p, font=font, stroke_width=stroke)
                cur_x += (pb[2] - pb[0])
            if i < len(parts) - 1:
                _draw_vector_arrow(d, cur_x, mid_y, arrow_span, font.size, fill, shadow=shadow)
                cur_x += arrow_span
        return
    if shadow:
        d.text((x + 2, y + 2), txt, font=font, fill=(22, 17, 13), stroke_width=stroke, stroke_fill=(22, 17, 13))
    d.text((x, y), txt, font=font, fill=fill, stroke_width=stroke, stroke_fill=fill)


def draw_centered_text(
    d: ImageDraw.ImageDraw,
    cx: int,
    y: int,
    txt: str,
    font: ImageFont.FreeTypeFont,
    fill: tuple[int, int, int],
    shadow: bool = True,
    stroke: int = 1,
) -> None:
    tw, _ = text_wh(d, txt, font, stroke=stroke)
    x = cx - tw // 2
    draw_crisp_text(d, (x, y), txt, font, fill, shadow=shadow, stroke=stroke)


def draw_anchored_cues_r4(
    im: Image.Image,
    d: ImageDraw.ImageDraw,
    abs_t: float,
    row_t0: float,
    row_t1: float,
    cues: list[dict],
    portrait_cache: dict[str, Image.Image],
    show_portrait: bool = True,
) -> bool:
    for cue in cues:
        c0 = max(row_t0, float(cue["display_start_s"]))
        c1 = min(row_t1, float(cue["display_end_s"]), float(cue["display_start_s"]) + 3.80)
        if abs_t < c0 or abs_t > c1 or (c1 - c0) < 0.12:
            continue
        fade = min(0.35, (c1 - c0) * 0.35)
        a = min(prog(abs_t, c0, c0 + fade), prog(c1, abs_t, c1 - fade))
        if a <= 0.03:
            continue
        ov = cue["overlay"]
        kind = ov.get("kind", "LABEL")
        if kind == "WHO":
            name = ov.get("line_1", "")
            sub = ov.get("line_2", "")
            pid = base_cg.WHO_PORTRAIT_MAP.get(name)
            if show_portrait and pid and pid in portrait_cache:
                med = portrait_cache[pid]
                py = 195 + int(12 * (1.0 - a))
                px = 1320
                im.paste(med, (px, py), med)
            f_name = fnt(54, italic=True)
            f_sub = fnt(42, italic=True)
            w_name, _ = text_wh(d, name, f_name)
            w_sub, _ = text_wh(d, sub, f_sub)
            bx0, by0 = 112, H - 252
            bx1 = max(1060, bx0 + max(w_name, w_sub) + 64)
            by1 = H - 82
            d.rounded_rectangle((bx0, by0, bx1, by1), radius=24, fill=(50, 40, 30), outline=GOLD, width=4)
            draw_crisp_text(d, (bx0 + 30, by0 + 18), name, f_name, GOLD)
            draw_crisp_text(d, (bx0 + 30, by0 + 92), sub, f_sub, CREAM)
            return True
        else:
            label = ov.get("label") or ov.get("line_1") or ""
            if not label:
                continue
            font = fnt(62, italic=True)
            col = tuple(int(v * a + 48 * (1.0 - a)) for v in WHITE)
            tw, _ = text_wh(d, label, font)
            bx0, by0 = 104, 60
            bx1, by1 = bx0 + tw + 58, 170
            d.rounded_rectangle((bx0, by0, bx1, by1), radius=20, fill=(46, 36, 26), outline=GOLD, width=4)
            draw_crisp_text(d, (bx0 + 28, by0 + 18), label, font, col)
            return True
    return False


def draw_archive_credit_r4(d: ImageDraw.ImageDraw, arch_id: str, cue_active: bool, t: float) -> None:
    """Full-word bottom-left credit in crisp white Didot italic (40px); waits while any other label/card is active."""
    if cue_active or t < 0.20:
        return
    credit = ARCHIVE_CREDITS[arch_id]
    assert credit[-1].isalnum() or credit.endswith(")"), f"Credit does not end cleanly: {credit}"
    font = fnt(40, italic=True)
    tw, _ = text_wh(d, credit, font)
    assert 112 + tw <= W - 112, f"Credit overflows frame width ({112 + tw} > {W - 112}): {credit}"
    draw_crisp_text(d, (112, H - 82), credit, font, WHITE, shadow=True, stroke=1)


def render_row_frame_r4(
    im: Image.Image,
    d: ImageDraw.ImageDraw,
    row: dict,
    t: float,
    dur: float,
    cues: list[dict],
    scan_cache: dict[str, Image.Image],
    portrait_cache: dict[str, Image.Image],
) -> None:
    rid = row["id"]
    pnum = int(row["part"])
    abs_t = float(row["t_s"]) + t
    u = t / max(dur, 0.01)

    # 1. Chapter cards (strictly respect chapter_title_window_s <= 2.50s)
    if rid.startswith("01_card_p"):
        ch_num, title = base_cg.CHAPTER_TITLES[pnum]
        ch_win = row.get("chapter_title_window_s") or [row["t_s"], min(row["t_end_s"], row["t_s"] + 2.50)]
        win_dur = max(0.5, float(ch_win[1]) - float(ch_win[0]))
        cx, cy = W // 2, H // 2
        if t <= win_dur:
            a = min(prog(t, 0.0, 0.35), prog(win_dur, t, win_dur - 0.35))
            rx = int(610 + 36 * ease(t / win_dur))
            ry = int(242 + 14 * ease(t / win_dur))
            d.rounded_rectangle((cx - rx, cy - ry, cx + rx, cy + ry), radius=48, fill=(56, 46, 36), outline=GOLD, width=5)
            d.rounded_rectangle((cx - rx + 18, cy - ry + 18, cx + rx - 18, cy + ry - 18), radius=38, outline=CREAM, width=2)
            if a > 0.05:
                f_num = fnt(56, italic=True)
                f_tit = fnt(72, italic=True)
                draw_centered_text(d, cx, cy - 106, f"Part {ch_num}", f_num, GOLD)
                draw_centered_text(d, cx, cy - 12, title, f_tit, CREAM)
            ang = -0.65 + 1.3 * (t / win_dur)
            d.line((cx - 155, cy + 122, cx + int(155 * math.cos(ang)), cy + 122 + int(28 * math.sin(ang))), fill=GOLD, width=4)
            d.ellipse((cx - 8, cy + 114, cx + 8, cy + 130), fill=CREAM)
        else:
            post_u = (t - win_dur) / max(0.2, dur - win_dur)
            d.rounded_rectangle((190, 175, 1180, 775), radius=34, fill=(64, 52, 40), outline=GOLD, width=4)
            for k in range(5):
                rr = 95 + k * 44 + int(10 * math.sin(post_u * math.pi + k))
                d.arc((685 - rr, 475 - rr, 685 + rr, 475 + rr), 15 + k * 25, 225 + k * 25, fill=GOLD if k % 2 == 0 else CREAM, width=3)
            ang = 0.25 + 0.45 * ease(post_u)
            d.line((685, 310, 685 - int(220 * math.sin(ang)), 310 + int(280 * math.cos(ang))), fill=CREAM, width=5)
            d.line((685, 310, 685 + int(220 * math.sin(ang)), 310 + int(280 * math.cos(ang))), fill=GOLD, width=5)
            d.ellipse((675, 300, 695, 320), fill=GOLD, outline=CREAM, width=3)
            draw_anchored_cues_r4(im, d, abs_t, row["t_s"], row["t_end_s"], cues, portrait_cache, show_portrait=True)
        return

    # 2. Cream end card
    if rid == "09_cream_end_card":
        base_cg.render_row_frame(im, d, row, t, dur, cues, scan_cache, portrait_cache)
        return

    # 3. P1:08 split into 3 distinct beats
    if rid.startswith("08_cg_i_think_tree_beat"):
        cue_active = draw_anchored_cues_r4(im, d, abs_t, row["t_s"], row["t_end_s"], cues, portrait_cache)
        if rid.endswith("_beat1"):
            base_cg.paste_doc_card(im, d, scan_cache["darwin_tree_1837"], 540, 680, 470, 545, zoom=1.04 + 0.08 * ease(u), focus_xy=(0.5, 0.62))
            nodes = [
                ((1280, 750), (1280, 575), 0.0, 0.25),
                ((1280, 575), (1100, 425), 0.20, 0.52),
                ((1280, 575), (1460, 425), 0.24, 0.56),
                ((1100, 425), (995, 280), 0.48, 0.82),
                ((1100, 425), (1185, 270), 0.52, 0.86),
                ((1460, 425), (1370, 270), 0.56, 0.90),
                ((1460, 425), (1565, 280), 0.60, 0.94),
            ]
            for (x0, y0), (x1, y1), a0, a1 in nodes:
                s = prog(u, a0, a1)
                if s > 0:
                    xm, ym = int(x0 + (x1 - x0) * s), int(y0 + (y1 - y0) * s)
                    d.line((x0, y0, xm, ym), fill=GOLD, width=7)
                    if s >= 0.95:
                        d.ellipse((x1 - 10, y1 - 10, x1 + 10, y1 + 10), fill=CREAM, outline=GOLD, width=3)
            if not cue_active:
                draw_centered_text(d, 1280, 795, "ONE ROOT → MANY", fnt(52, italic=True), CREAM)
        elif rid.endswith("_beat2"):
            px, py, bw, bh = base_cg.paste_doc_card(im, d, scan_cache["darwin_tree_1837"], 760, 620, 620, 540, zoom=1.35 + 0.14 * ease(u), focus_xy=(0.48, 0.16))
            ul = int(340 * prog(t, 0.25, dur * 0.75))
            d.line((px + 170, py + 195, px + 170 + ul, py + 195), fill=GOLD, width=7)
            d.rounded_rectangle((1090, 350, 1790, 675), radius=28, fill=(54, 44, 34), outline=GOLD, width=4)
            draw_centered_text(d, 1440, 405, "“I think”", fnt(86, italic=True), GOLD)
            draw_centered_text(d, 1440, 548, "NOTEBOOK B · 1837", fnt(48, italic=True), CREAM)
        else:
            base_cg.paste_doc_card(im, d, scan_cache["darwin_tree_1837"], 440, 560, 410, 560, zoom=1.08, focus_xy=(0.5, 0.5))
            bar_p = prog(t, 0.15, dur * 0.78)
            bx0, by0, bw, bh = 730, 540, 990, 76
            d.rounded_rectangle((bx0, by0, bx0 + bw, by0 + bh), radius=22, fill=(46, 38, 30), outline=GOLD, width=4)
            fill_w = int((bw - 10) * bar_p)
            if fill_w > 14:
                d.rounded_rectangle((bx0 + 5, by0 + 5, bx0 + 5 + fill_w, by0 + bh - 5), radius=18, fill=GOLD)
            yr = 1838 + int(round(20 * bar_p))
            draw_crisp_text(d, (bx0, by0 - 104), f"1838  →  {yr}", fnt(68, italic=True), GOLD)
            if not cue_active:
                draw_crisp_text(d, (bx0, by0 + 102), f"{int(round(20 * bar_p))} YEARS LOCKED AWAY", fnt(52, italic=True), CREAM)
        return

    # 4. P1:10 globe arc (enlarged 1844 / 230 PAGES & 1858 / PACKET inside dark house panel)
    if rid == "10_cg_globe_arc":
        cue_active = draw_anchored_cues_r4(im, d, abs_t, row["t_s"], row["t_end_s"], cues, portrait_cache)
        gx, gy, gr = 595, 555, 330
        d.ellipse((gx - gr, gy - gr, gx + gr, gy + gr), fill=(38, 56, 72), outline=GOLD, width=5)
        for lat in (-185, -92, 0, 92, 185):
            d.arc((gx - gr + 26, gy + lat - 52, gx + gr - 26, gy + lat + 52), 10, 170, fill=(88, 110, 128), width=2)
        kent, malay = (gx - 112, gy - 144), (gx + 185, gy + 66)
        d.ellipse((kent[0] - 11, kent[1] - 11, kent[0] + 11, kent[1] + 11), fill=CREAM, outline=GOLD, width=3)
        d.ellipse((malay[0] - 11, malay[1] - 11, malay[0] + 11, malay[1] + 11), fill=GOLD, outline=CREAM, width=3)
        arc_p = prog(t, 0.2, dur * 0.76)
        pts = [
            (int((1 - (k / 48.0)) * malay[0] + (k / 48.0) * kent[0]),
             int((1 - (k / 48.0)) * malay[1] + (k / 48.0) * kent[1] - 144 * math.sin((k / 48.0) * math.pi)))
            for k in range(max(2, int(48 * arc_p)) + 1)
        ]
        if len(pts) >= 2:
            d.line(pts, fill=GOLD, width=7)

        # Right comparison house panel so year & page tags read clearly at 390px
        d.rounded_rectangle((1015, 250, 1835, 865), radius=30, fill=(52, 42, 32), outline=GOLD, width=4)
        st_p = prog(t, 0.5, dur * 0.85)
        for k in range(max(1, int(18 * st_p))):
            yy = 650 - k * 16
            d.rounded_rectangle((1095, yy - 12, 1365, yy), radius=4, fill=CREAM, outline=TAN, width=2)
        d.rounded_rectangle((1485, 618, 1755, 650), radius=6, fill=GOLD, outline=CREAM, width=2)
        if not cue_active:
            draw_centered_text(d, 1230, 682, "1844", fnt(58, italic=True), CREAM)
            draw_centered_text(d, 1230, 756, "230 PAGES", fnt(46, italic=True), CREAM)
            draw_centered_text(d, 1620, 682, "1858", fnt(58, italic=True), GOLD)
            draw_centered_text(d, 1620, 756, "PACKET", fnt(46, italic=True), GOLD)
        return

    # 5. P2:06b tortoise shells
    if rid == "06b_cg_tortoise_shells":
        cue_active = draw_anchored_cues_r4(im, d, abs_t, row["t_s"], row["t_end_s"], cues, portrait_cache)
        p_draw = prog(t, 0.15, dur * 0.78)
        d.rounded_rectangle((180, 230, 880, 845), radius=30, fill=(56, 46, 36), outline=CREAM, width=3)
        d.rounded_rectangle((1040, 230, 1740, 845), radius=30, fill=(56, 46, 36), outline=GOLD, width=4)
        cx1, cy1 = 530, 610
        d.chord((cx1 - 245, cy1 - 225, cx1 + 245, cy1 + 80), 180, 180 + int(180 * p_draw), fill=(98, 80, 58), outline=CREAM, width=5)
        for r_sc in range(3):
            d.arc((cx1 - 180 + r_sc * 40, cy1 - 170 + r_sc * 25, cx1 + 180 - r_sc * 40, cy1 + 20), 195, 345, fill=GOLD, width=3)
        cx2, cy2 = 1390, 610
        d.chord((cx2 - 245, cy2 - 255, cx2 + 245, cy2 + 80), 205, 205 + int(155 * p_draw), fill=(118, 92, 64), outline=GOLD, width=5)
        if p_draw > 0.2:
            d.arc((cx2 - 260, cy2 - 215, cx2 - 105, cy2 - 40), 250, 70, fill=CREAM, width=6)
        if not cue_active:
            draw_centered_text(d, cx1, cy1 + 114, "DOME SHELL", fnt(52, italic=True), CREAM)
            draw_centered_text(d, cx2, cy2 + 114, "SADDLE ARCH", fnt(52, italic=True), GOLD)
        return

    # 6. P2:09 finch toolbox split into beat1 and beat2
    if rid.startswith("09_cg_finch_toolbox_beat"):
        cue_active = draw_anchored_cues_r4(im, d, abs_t, row["t_s"], row["t_end_s"], cues, portrait_cache)
        if rid.endswith("_beat1"):
            base_cg.paste_doc_card(im, d, scan_cache["gould_finches_1845"], 600, 620, 470, 545, zoom=1.04 + 0.08 * ease(u), focus_xy=(0.35, 0.35))
            beaks = [
                ("1. HEAVY NUTCRACKER", 390, 64, GOLD),
                ("2. STOUT SEED PLIERS", 650, 46, CREAM),
            ]
            for idx, (lbl, yy, depth, col) in enumerate(beaks):
                s = prog(t, 0.35 + idx * 1.4, 2.0 + idx * 1.4)
                if s > 0:
                    bx, blen = 900, int(195 * s)
                    d.rounded_rectangle((865, yy - 98, 1815, yy + 98), radius=22, fill=(52, 42, 32), outline=col, width=3)
                    d.polygon([(bx, yy - depth), (bx + blen, yy), (bx, yy + depth)], fill=col, outline=WHITE)
                    if not cue_active:
                        draw_crisp_text(d, (bx + 225, yy - 28), lbl, fnt(46, italic=True), col)
        else:
            base_cg.paste_doc_card(im, d, scan_cache["gould_finches_1845"], 600, 620, 470, 535, zoom=1.22 + 0.10 * ease(u), focus_xy=(0.68, 0.72))
            beaks = [
                ("3. FINE TWEEZERS", 385, 28, PALE),
                ("4. CACTUS PROBE", 645, 16, TEAL),
            ]
            for idx, (lbl, yy, depth, col) in enumerate(beaks):
                s = prog(t, 0.25 + idx * 1.2, 1.8 + idx * 1.2)
                if s > 0:
                    bx, blen = 900, int(220 * s)
                    d.rounded_rectangle((865, yy - 98, 1815, yy + 98), radius=22, fill=(52, 42, 32), outline=col, width=3)
                    d.polygon([(bx, yy - depth), (bx + blen, yy), (bx, yy + depth)], fill=col, outline=WHITE)
                    if not cue_active:
                        draw_crisp_text(d, (bx + 245, yy - 28), lbl, fnt(46, italic=True), col)
            draw_archive_credit_r4(d, "gould_finches_1845", cue_active, t)
        return

    # 7. P2:10b_shipmate_tagged_tray
    if rid == "10b_shipmate_tagged_tray":
        cue_active = draw_anchored_cues_r4(im, d, abs_t, row["t_s"], row["t_end_s"], cues, portrait_cache)
        base_cg.paste_doc_card(im, d, scan_cache["gould_finches_1845"], 640, 620, 510, 535, zoom=1.08 + 0.08 * ease(u), focus_xy=(0.5, 0.45))
        tags = [("CHATHAM ISLAND", 290), ("JAMES ISLAND", 520), ("CHARLES ISLAND", 750)]
        for idx, (island, yy) in enumerate(tags):
            s = prog(t, 0.15 + idx * 0.55, 0.95 + idx * 0.55)
            if s > 0:
                tx = int(995 + 40 * (1.0 - s))
                d.rounded_rectangle((tx, yy - 64, tx + 730, yy + 64), radius=18, fill=(232, 214, 182), outline=GOLD, width=4)
                d.ellipse((tx + 28, yy - 12, tx + 52, yy + 12), fill=(56, 46, 36), outline=GOLD, width=3)
                d.line((tx - 60, yy, tx + 28, yy), fill=TAN, width=4)
                if idx == 0 and not cue_active:
                    draw_crisp_text(d, (tx + 82, yy - 28), island, fnt(48, italic=True), DARK_INK, shadow=False)
                else:
                    d.line((tx + 85, yy - 12, tx + 590, yy - 12), fill=CLAY, width=4)
                    d.line((tx + 85, yy + 16, tx + 450, yy + 16), fill=TAN, width=3)
        return

    # 8. Standard single-beat archive composites (12a, 10a, 06b, 05b, 09, 04b)
    if rid in (
        "12a_arch_notebook_tree_zoom",
        "10a_arch_vestiges_1844",
        "06b_arch_malthus_1798",
        "05b_arch_origin_1859_title",
        "09_arch_darwinism_1889",
        "04b_arch_mendel_1866_paper",
    ):
        arch_id = (row.get("archive_source") or {}).get("id")
        assert arch_id in ARCHIVE_CREDITS, f"Missing explicit archive credit for {arch_id}"
        src_im = scan_cache[arch_id]
        cue_active = draw_anchored_cues_r4(im, d, abs_t, row["t_s"], row["t_end_s"], cues, portrait_cache, show_portrait=True)
        cx = 640 if rid == "04b_arch_mendel_1866_paper" else (W // 2 + int(24 * math.sin(u * math.pi)))
        cy = H // 2 - 12 + int(12 * math.cos(u * math.pi))
        px, py, bw, bh = base_cg.paste_doc_card(im, d, src_im, 720, 620, cx, cy, zoom=1.02 + 0.14 * ease(u))
        ring_p = prog(t, 0.35, min(dur - 0.3, 3.4))
        d.arc((px + bw // 2 - 220, py + bh // 2 - 115, px + bw // 2 + 220, py + bh // 2 + 115), 0, int(360 * ring_p), fill=GOLD, width=6)
        draw_archive_credit_r4(d, arch_id, cue_active, t)
        return

    # 9. P3:03 Malthus curve split into beat1 ('OFFSPRING BORN') and beat2 ('FOOD SUPPLY')
    if rid.startswith("03_cg_malthus_curve_beat"):
        cue_active = draw_anchored_cues_r4(im, d, abs_t, row["t_s"], row["t_end_s"], cues, portrait_cache)
        ox, oy, gw, gh = 250, 840, 1420, 580
        d.rounded_rectangle((190, 200, 1730, 895), radius=30, fill=(52, 42, 32), outline=GOLD, width=4)
        for gx_grid in range(ox + 180, ox + gw, 180):
            d.line((gx_grid, oy - gh + 20, gx_grid, oy), fill=(76, 62, 48), width=2)
        d.line((ox, oy - gh, ox, oy), fill=CREAM, width=5)
        d.line((ox, oy, ox + gw, oy), fill=CREAM, width=5)
        if rid.endswith("_beat1"):
            p_c = prog(t, 0.15, dur * 0.80)
            exp_pts = [
                (int(ox + gw * (k / 80.0)), int(oy - 55 - (gh - 95) * ((math.exp(2.8 * (k / 80.0)) - 1.0) / (math.exp(2.8) - 1.0))))
                for k in range(max(2, int(80 * p_c)) + 1)
            ]
            d.line(exp_pts, fill=CRIMSON, width=9)
            if not cue_active:
                lx = max(295, min(1150, exp_pts[-1][0] - 460))
                ly = max(238, exp_pts[-1][1] - 84)
                draw_crisp_text(d, (lx, ly), "OFFSPRING BORN", fnt(58, italic=True), GOLD)
        else:
            exp_pts = [
                (int(ox + gw * (k / 80.0)), int(oy - 55 - (gh - 95) * ((math.exp(2.8 * (k / 80.0)) - 1.0) / (math.exp(2.8) - 1.0))))
                for k in range(81)
            ]
            d.line(exp_pts, fill=CRIMSON, width=9)
            p_f = prog(t, 0.12, dur * 0.72)
            n_f = max(2, int(80 * p_f))
            lin_pts = [(int(ox + gw * (k / 80.0)), int(oy - 145 - 85 * (k / 80.0))) for k in range(n_f + 1)]
            d.line(lin_pts, fill=TEAL, width=8)
            for k in range(10, n_f, 8):
                d.line((exp_pts[k][0], exp_pts[k][1] + 10, lin_pts[k][0], lin_pts[k][1] - 10), fill=GOLD, width=3)
            if not cue_active:
                lx = max(295, min(1240, lin_pts[-1][0] - 380))
                ly = min(760, lin_pts[-1][1] + 24)
                draw_crisp_text(d, (lx, ly), "FOOD SUPPLY", fnt(56, italic=True), TEAL)
        return

    # 10. P3:06 natural selection sieve
    if rid.startswith("06_nature_keeps_fit_beat"):
        cue_active = draw_anchored_cues_r4(im, d, abs_t, row["t_s"], row["t_end_s"], cues, portrait_cache)
        sieve_y = 555
        d.rounded_rectangle((210, 195, 1710, 885), radius=30, fill=(52, 42, 32), outline=GOLD, width=4)
        for k in range(13):
            sx = 310 + k * 108
            d.ellipse((sx - 28, sieve_y - 20, sx + 28, sieve_y + 20), fill=TAN, outline=CREAM, width=3)
        if rid.endswith("_beat1"):
            p_fall = prog(t, 0.15, dur * 0.82)
            profiles = [(520, 18, PALE, False), (960, 32, CREAM, False), (1400, 58, GOLD, True)]
            for cx, depth, col, passes in profiles:
                max_y = 750 if passes else sieve_y - 62
                cy = int(285 + (max_y - 285) * p_fall)
                d.polygon([(cx - 80, cy - depth), (cx + 105, cy), (cx - 80, cy + depth)], fill=col, outline=WHITE)
            if not cue_active:
                draw_centered_text(d, 960, 795, "ONES THAT FIT", fnt(54, italic=True), GOLD)
        else:
            cx, cy = 960, 690
            r_glow = int(165 + 25 * math.sin(u * math.pi))
            d.ellipse((cx - r_glow, cy - 110, cx + r_glow, cy + 110), outline=GOLD, width=4)
            d.polygon([(cx - 130, cy - 78), (cx + 165, cy), (cx - 130, cy + 78)], fill=GOLD, outline=CREAM)
            if not cue_active:
                draw_centered_text(d, cx, 275, "DEEP BEAK SURVIVES", fnt(56, italic=True), CREAM)
        return

    # 11. P3:09a_essay_1844_sealed (keeps r3 show_portrait=False fix)
    if rid == "09a_essay_1844_sealed":
        cue_active = draw_anchored_cues_r4(im, d, abs_t, row["t_s"], row["t_end_s"], cues, portrait_cache, show_portrait=False)
        st_p = prog(t, 0.10, dur * 0.55)
        n_sheets = max(2, int(24 * st_p))
        for k in range(n_sheets):
            yy = 760 - k * 14
            d.rounded_rectangle((310, yy - 14, 830, yy), radius=5, fill=CREAM, outline=TAN, width=2)
        if st_p > 0.65:
            rp = prog(st_p, 0.65, 1.0)
            d.rectangle((548, int(760 - n_sheets * 14), 592, 762), fill=CRIMSON, outline=GOLD, width=2)
            if rp > 0.5:
                d.ellipse((538, 560, 602, 624), fill=CRIMSON, outline=GOLD, width=4)
        d.rounded_rectangle((960, 280, 1750, 770), radius=28, fill=(52, 42, 32), outline=GOLD, width=4)
        years = ["1835", "1837", "1838", "1844"]
        tl_p = prog(t, 0.25, dur * 0.75)
        d.line((1040, 535, 1040 + int(600 * tl_p), 535), fill=GOLD, width=6)
        for idx, yr in enumerate(years):
            dx = 1040 + idx * 200
            if tl_p >= idx / 3.2:
                active = yr == "1844"
                d.ellipse((dx - 16, 519, dx + 16, 551), fill=GOLD if active else CREAM, outline=GOLD, width=4)
                if active and not cue_active:
                    draw_centered_text(d, dx, 425, "1844", fnt(56, italic=True), GOLD)
        return

    # 12. P3:12 barnacle counter
    if rid == "12_cg_barnacle_counter":
        cue_active = draw_anchored_cues_r4(im, d, abs_t, row["t_s"], row["t_end_s"], cues, portrait_cache)
        p_cnt = prog(t, 0.18, dur * 0.80)
        yr = 1846 + int(round(8 * p_cnt))
        yrs_done = int(round(8 * p_cnt))
        cx, cy = 590, 545
        d.rounded_rectangle((cx - 315, cy - 195, cx + 315, cy + 195), radius=36, fill=(54, 44, 34), outline=GOLD, width=5)
        draw_centered_text(d, cx, cy - 125, f"{yr}", fnt(126, italic=True), GOLD)
        if not cue_active:
            draw_centered_text(d, cx, cy + 52, f"{yrs_done} OF 8 YEARS", fnt(50, italic=True), CREAM)
        for v in range(4):
            vp = prog(p_cnt, v * 0.20, (v + 1) * 0.24)
            if vp > 0:
                vx = 1040 + v * 165
                vy = int(745 - 360 * vp)
                d.rounded_rectangle((vx, vy, vx + 132, 745), radius=14, fill=(68, 94, 84), outline=GOLD, width=4)
                d.line((vx + 24, vy + 55, vx + 108, vy + 55), fill=GOLD, width=4)
        return

    # 13. P4:05 Wallace counter
    if rid.startswith("05_cg_wallace_counter_beat"):
        cue_active = draw_anchored_cues_r4(im, d, abs_t, row["t_s"], row["t_end_s"], cues, portrait_cache)
        islands = [
            [(280, 470), (450, 555), (505, 670), (365, 635)],
            [(545, 685), (785, 705), (815, 760), (565, 740)],
            [(630, 440), (825, 420), (865, 585), (670, 600)],
            [(915, 470), (1040, 450), (1020, 625), (905, 605)],
            [(1110, 515), (1245, 495), (1265, 585), (1120, 595)],
            [(1315, 545), (1575, 565), (1605, 700), (1345, 670)],
        ]
        d.rounded_rectangle((210, 210, 1710, 860), radius=34, fill=(40, 58, 72), outline=GOLD, width=4)
        p_map = prog(t, 0.12, dur * 0.82) if rid.endswith("_beat1") else 1.0
        prev_pt = None
        for idx, poly in enumerate(islands):
            d.polygon(poly, fill=(82, 106, 78), outline=GOLD, width=3)
            cx = sum(p[0] for p in poly) // len(poly)
            cy = sum(p[1] for p in poly) // len(poly)
            if p_map >= (idx + 0.6) / len(islands):
                d.ellipse((cx - 12, cy - 12, cx + 12, cy + 12), fill=GOLD, outline=CREAM, width=3)
                if prev_pt:
                    d.line((prev_pt[0], prev_pt[1], cx, cy), fill=CREAM, width=3)
                prev_pt = (cx, cy)
        if rid.endswith("_beat1"):
            if not cue_active:
                draw_crisp_text(d, (275, 255), "MALAY ARCHIPELAGO · 1854", fnt(54, italic=True), CREAM)
        else:
            p_cnt = prog(t, 0.10, dur * 0.78)
            count_val = int(round(125660 * p_cnt))
            d.rounded_rectangle((915, 235, 1680, 480), radius=28, fill=(54, 44, 34), outline=GOLD, width=5)
            draw_crisp_text(d, (965, 258), f"{count_val:,}", fnt(108, italic=True), GOLD)
            if not cue_active:
                draw_crisp_text(d, (965, 396), "SPECIMENS · 1854–1862", fnt(46, italic=True), CREAM)
        return

    # 14. P4:07b_packet_to_mailbag
    if rid == "07b_packet_to_mailbag":
        cue_active = draw_anchored_cues_r4(im, d, abs_t, row["t_s"], row["t_end_s"], cues, portrait_cache)
        d.rounded_rectangle((190, 200, 1730, 880), radius=34, fill=(40, 58, 72), outline=GOLD, width=5)
        d.polygon([(340, 310), (540, 290), (620, 410), (470, 430)], fill=(82, 102, 78), outline=TAN, width=3)
        d.polygon([(580, 450), (860, 470), (820, 740), (640, 710)], fill=(88, 104, 76), outline=TAN, width=3)
        d.polygon([(920, 360), (1380, 380), (1460, 580), (1080, 560)], fill=(82, 102, 78), outline=TAN, width=3)
        d.polygon([(1420, 620), (1600, 610), (1630, 705), (1440, 695)], fill=(92, 112, 82), outline=GOLD, width=3)
        ternate = (1525, 655)
        down_house = (435, 355)
        d.ellipse((ternate[0] - 12, ternate[1] - 12, ternate[0] + 12, ternate[1] + 12), fill=GOLD, outline=CREAM, width=3)
        d.ellipse((down_house[0] - 12, down_house[1] - 12, down_house[0] + 12, down_house[1] + 12), fill=CREAM, outline=GOLD, width=3)
        p_route = prog(t, 0.12, dur * 0.84)
        pts = [
            (int((1 - (k / 60.0)) * ternate[0] + (k / 60.0) * down_house[0]),
             int((1 - (k / 60.0)) * ternate[1] + (k / 60.0) * down_house[1] + 155 * math.sin((k / 60.0) * math.pi)))
            for k in range(max(2, int(60 * p_route)) + 1)
        ]
        if len(pts) >= 2:
            d.line(pts, fill=GOLD, width=6)
            ex, ey = pts[-1]
            d.rounded_rectangle((ex - 46, ey - 30, ex + 46, ey + 30), radius=8, fill=CREAM, outline=GOLD, width=3)
            d.line((ex - 42, ey - 26, ex, ey + 4), fill=TAN, width=3)
            d.line((ex + 42, ey - 26, ex, ey + 4), fill=TAN, width=3)
            d.ellipse((ex - 11, ey - 8, ex + 11, ey + 14), fill=CRIMSON, outline=GOLD, width=2)
        if not cue_active:
            draw_crisp_text(d, (255, 780), "TERNATE → DOWN HOUSE · 18 JUNE 1858", fnt(50, italic=True), CREAM)
        return

    # 15. P5:02b_joint_papers_lectern (_wide and _detail; keeps r3 show_portrait=False fix)
    if rid.startswith("02b_joint_papers_lectern_"):
        cue_active = draw_anchored_cues_r4(im, d, abs_t, row["t_s"], row["t_end_s"], cues, portrait_cache, show_portrait=False)
        hooker = portrait_cache["who_joseph_hooker"]
        if rid.endswith("_wide"):
            d.rounded_rectangle((190, 210, 1250, 860), radius=32, fill=(56, 44, 34), outline=GOLD, width=5)
            p_in = prog(t, 0.10, dur * 0.70)
            d.rounded_rectangle((255, 300, 685, 780), radius=16, fill=CREAM, outline=TAN, width=4)
            for ln in range(8):
                d.line((300, 390 + ln * 42, 635, 390 + ln * 42), fill=CLAY, width=4)
            d.rounded_rectangle((745, 300, 1175, 780), radius=16, fill=(240, 224, 192), outline=GOLD, width=4)
            for ln in range(8):
                d.line((790, 390 + ln * 42, 1125, 390 + ln * 42), fill=CLAY, width=4)
            rib_w = int(920 * p_in)
            if rib_w > 20:
                d.rectangle((255, 535, 255 + rib_w, 558), fill=CRIMSON, outline=GOLD, width=2)
            im.paste(hooker, (1375, 235 + int(10 * math.sin(u * math.pi))), hooker)
            if not cue_active:
                draw_centered_text(d, 1545, 622, "1 JULY 1858 · LONDON", fnt(46, italic=True), GOLD)
        else:
            base_cg.paste_doc_card(im, d, scan_cache["who_joseph_hooker_raw"], 510, 610, 505, 540, zoom=1.06 + 0.12 * ease(u), focus_xy=(0.5, 0.35))
            d.rounded_rectangle((875, 245, 1765, 515), radius=24, fill=(242, 226, 194), outline=GOLD, width=4)
            d.rounded_rectangle((875, 565, 1765, 830), radius=24, fill=(236, 218, 184), outline=CREAM, width=4)
            for base_y in (355, 665):
                for ln in range(3):
                    d.line((925, base_y + ln * 42, 1690, base_y + ln * 42), fill=CLAY, width=4)
            hl = int(680 * prog(t, 0.2, dur * 0.75))
            d.line((925, 324, 925 + hl, 324), fill=GOLD, width=6)
            if not cue_active:
                draw_crisp_text(d, (925, 264), "1844 SKETCH + 1858 ESSAY", fnt(48, italic=True), DARK_INK, shadow=False)
        return

    # 16. P5:04b_bell_report_1859
    if rid == "04b_bell_report_1859":
        cue_active = draw_anchored_cues_r4(im, d, abs_t, row["t_s"], row["t_end_s"], cues, portrait_cache)
        px, py, bw, bh = 460, 205, 1000, 700
        d.rounded_rectangle((px - 22, py - 22, px + bw + 22, py + bh + 22), radius=28, fill=(52, 42, 32), outline=GOLD, width=5)
        d.rounded_rectangle((px, py, px + bw, py + bh), radius=16, fill=(242, 228, 198), outline=TAN, width=3)
        d.line((px + 120, py + 122, px + bw - 120, py + 122), fill=DARK_INK, width=4)
        for ln in range(9):
            yy = py + 188 + ln * 50
            col = CRIMSON if ln == 5 else (128, 108, 86)
            d.line((px + 110, yy, px + bw - 110, yy), fill=col, width=5 if ln == 5 else 3)
        ul_p = prog(t, 0.35, dur * 0.80)
        ul_w = int((bw - 220) * ul_p)
        if ul_w > 12:
            d.line((px + 110, py + 188 + 5 * 50 + 14, px + 110 + ul_w, py + 188 + 5 * 50 + 14), fill=GOLD, width=8)
        if not cue_active:
            draw_centered_text(d, px + bw // 2, py + 44, "MAY 1859 · ANNUAL REPORT", fnt(50, italic=True), DARK_INK, shadow=False)
        return

    # 17. P5:07 timeline origin
    if rid == "07_cg_timeline_origin":
        cue_active = draw_anchored_cues_r4(im, d, abs_t, row["t_s"], row["t_end_s"], cues, portrait_cache)
        dates = ["1835", "1837", "1838", "1844", "1858", "1859", "1889"]
        p_tl = prog(t, 0.12, dur * 0.78)
        d.rounded_rectangle((140, 240, 1780, 870), radius=32, fill=(52, 42, 32), outline=GOLD, width=4)
        x0, x1, yy = 240, 1680, 495
        cur_x = int(x0 + (x1 - x0) * p_tl)
        d.line((x0, yy, cur_x, yy), fill=GOLD, width=7)
        for idx, yr in enumerate(dates):
            dx = x0 + int((x1 - x0) * (idx / (len(dates) - 1)))
            if cur_x >= dx - 5:
                d.ellipse((dx - 16, yy - 16, dx + 16, yy + 16), fill=GOLD if yr == "1859" else CREAM, outline=GOLD, width=4)
                y_off = -92 if idx % 2 == 0 else 38
                draw_centered_text(d, dx, yy + y_off, yr, fnt(48, italic=True), GOLD if yr == "1859" else CREAM)
        n_b = max(1, int(10 * p_tl))
        for b in range(n_b):
            bx = 520 + b * 88
            d.rounded_rectangle((bx, 690, bx + 68, 820), radius=8, fill=(64, 98, 76), outline=GOLD, width=3)
        if not cue_active:
            cnt = int(round(1250 * p_tl))
            draw_centered_text(d, 960, 608, f"{cnt:,} COPIES ORDERED", fnt(52, italic=True), CREAM)
        return

    # 18. P6:03 blending beaks
    if rid.startswith("03_cg_blending_beaks_beat"):
        cue_active = draw_anchored_cues_r4(im, d, abs_t, row["t_s"], row["t_end_s"], cues, portrait_cache)
        d.rounded_rectangle((180, 210, 1740, 875), radius=32, fill=(52, 42, 32), outline=GOLD, width=4)
        if rid.endswith("_beat1"):
            gens = [
                ("1", 400, 68, (226, 184, 102)),
                ("1/2", 960, 44, (196, 166, 118)),
                ("1/4", 1520, 28, (164, 148, 130)),
            ]
            for idx, (frac, cx, depth, col) in enumerate(gens):
                s = prog(t, 0.2 + idx * 1.6, 1.9 + idx * 1.6)
                if s > 0:
                    cy, blen = 555, int(185 * s)
                    d.polygon([(cx - 85, cy - depth), (cx - 85 + blen, cy), (cx - 85, cy + depth)], fill=col, outline=CREAM)
                    draw_centered_text(d, cx, cy - 170, frac, fnt(76, italic=True), col)
            if not cue_active:
                draw_centered_text(d, 960, 760, "HALVED EACH GENERATION", fnt(52, italic=True), CREAM)
        else:
            gens = [
                ("1", 330, 64, (226, 184, 102)),
                ("1/2", 730, 42, (196, 166, 118)),
                ("1/4", 1130, 28, (164, 148, 130)),
                ("1/8", 1530, 16, (136, 134, 132)),
            ]
            fade_wash = prog(t, 0.25, dur * 0.78)
            for idx, (frac, cx, depth, col) in enumerate(gens):
                s = 1.0 if idx < 3 else fade_wash
                if s > 0:
                    cy, blen = 555, int(165 * s)
                    wcol = tuple(int(c * (1.0 - 0.35 * fade_wash) + 128 * (0.35 * fade_wash)) for c in col)
                    d.polygon([(cx - 75, cy - depth), (cx - 75 + blen, cy), (cx - 75, cy + depth)], fill=wcol, outline=CREAM)
                    draw_centered_text(d, cx, cy - 162, frac, fnt(68, italic=True), wcol)
            if not cue_active:
                draw_centered_text(d, 960, 760, "DILUTED TO GREY", fnt(54, italic=True), PALE)
        return

    raise RuntimeError(f"Unhandled free row id: {rid}")


def _render_single_row_r4(task: tuple[int, dict, list[dict], str]) -> dict:
    idx, row, row_cues, tag = task
    assert base_cg._G_BASE is not None
    pnum = int(row["part"])
    rid = row["id"]
    dur = round(float(row["t_end_s"]) - float(row["t_s"]), 2)
    n_frames = max(15, int(round(dur * FPS)))

    # For P2:01_card_p02 (no overlapping WHO cue after 2.50s), sample hero frame at t=1.25s (mid-title window)
    if rid == "01_card_p02":
        hero_idx = min(n_frames - 1, int(round(1.25 * FPS)))
    else:
        hero_idx = n_frames // 2

    cg_name = f"code_graphic_013_{tag}_p{pnum}_{rid}.mp4"
    still_name = f"code_graphic_013_{tag}_p{pnum}_{rid}.jpg"
    mp4_path = NAS_CG / cg_name
    still_path = NAS_CG / still_name
    assert not mp4_path.exists(), f"Refusing overwrite on NAS: {mp4_path}"

    cmd = [
        "ffmpeg", "-y", "-v", "error",
        "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
        "-i", "-",
        "-an", "-c:v", "libx264", "-preset", "ultrafast", "-crf", "18", "-pix_fmt", "yuv420p",
        "-threads", "2",
        str(mp4_path),
    ]
    enc = sp.Popen(cmd, stdin=sp.PIPE)
    min_mean = 999.0
    min_p95 = 999.0
    min_std = 999.0
    try:
        for f_idx in range(n_frames):
            t = f_idx / FPS
            shift_x = int(8 * math.sin(2 * math.pi * (t / max(dur, 1.5)) + idx * 0.37))
            frame_arr = np.roll(base_cg._G_BASE, shift_x, axis=1).copy()
            im = Image.fromarray(frame_arr, "RGB")
            d = ImageDraw.Draw(im)
            render_row_frame_r4(im, d, row, t, dur, row_cues, base_cg._G_SCANS, base_cg._G_PORTRAITS)
            if f_idx in (0, hero_idx, n_frames - 1):
                gray = np.asarray(im.convert("L"), dtype=np.float32)
                min_mean = min(min_mean, float(gray.mean()))
                min_p95 = min(min_p95, float(np.percentile(gray, 95)))
                min_std = min(min_std, float(gray.std()))
            if f_idx == hero_idx:
                im.save(still_path, quality=92)
            assert enc.stdin is not None
            enc.stdin.write(im.tobytes())
    finally:
        if enc.stdin:
            enc.stdin.close()
        if enc.wait() != 0:
            raise RuntimeError(f"ffmpeg failed on {cg_name}")

    actual_dur = round(n_frames / FPS, 2)
    return {
        "idx": idx,
        "id": f"P{pnum}:{rid}",
        "source_row_v02": row["source_row_v02"],
        "source_kind": row["source_kind"],
        "file": cg_name,
        "nas_path": str(mp4_path),
        "still": still_name,
        "hero_sample_s": round(hero_idx / FPS, 2),
        "t_s": row["t_s"],
        "t_end_s": row["t_end_s"],
        "use_s": dur,
        "encoded_frames": n_frames,
        "encoded_s": actual_dur,
        "fps": FPS,
        "min_sample_mean_luma": round(min_mean, 2),
        "min_sample_p95": round(min_p95, 2),
        "min_sample_std": round(min_std, 2),
        "near_black": "PASS" if (min_mean >= 28.0 and min_p95 >= 50.0) else "FAIL",
        "sha256_mp4": base_cg.digest(mp4_path),
        "sha256_still": base_cg.digest(still_path),
        "spend": "£0",
    }


def build_chapter_windows_sheet(free_rows: list[dict], all_cues: list[dict]) -> Path:
    """Build 390px verification strip proving both title window (t=1.25s) and post-title window for P2:01 & P6:01."""
    samples: list[tuple[str, Image.Image]] = []
    for r in free_rows:
        if not r["id"].startswith("01_card_p"):
            continue
        rk = f"P{r['part']}:{r['id']}"
        dur = round(float(r["t_end_s"]) - float(r["t_s"]), 2)
        ov = [
            c for c in all_cues
            if max(float(r["t_s"]), float(c["display_start_s"])) < min(float(r["t_end_s"]), float(c["display_end_s"]))
        ]
        times = [1.25, 3.80] if dur > 3.2 else [1.25]
        for t in times:
            im = Image.fromarray(base_cg._G_BASE.copy(), "RGB")
            d = ImageDraw.Draw(im)
            render_row_frame_r4(im, d, r, t, dur, ov, base_cg._G_SCANS, base_cg._G_PORTRAITS)
            samples.append((f"{rk} @ t={t:.2f}s (film {r['t_s'] + t:.2f}s)", im.resize((390, 219), Image.Resampling.LANCZOS)))

    cols, tw, th = 4, 390, 219
    rows_n = math.ceil(len(samples) / cols)
    sheet = Image.new("RGB", (cols * tw, rows_n * (th + 42)), (28, 34, 44))
    sd = ImageDraw.Draw(sheet)
    sfont = fnt(18, italic=True)
    for i, (lbl, thumb) in enumerate(samples):
        x, y = (i % cols) * tw, (i // cols) * (th + 42)
        sheet.paste(thumb, (x, y))
        sd.text((x + 6, y + th + 6), lbl, fill=CREAM, font=sfont)
    out_p = GIT_CG / "CHAPTER_WINDOWS_v03f_r4_390px.jpg"
    sheet.save(out_p, quality=90)
    nas_ch = NAS_CG / out_p.name
    if not nas_ch.exists():
        shutil.copy2(out_p, nas_ch)
    return out_p


ARROW_PATCH_IDS = {
    "P1:08_cg_i_think_tree_beat1",
    "P1:08_cg_i_think_tree_beat3",
    "P4:07b_packet_to_mailbag",
}


def main() -> None:
    import sys
    patch_arrows = "--patch-arrows" in sys.argv
    nas_tag = "v03f_r4b" if patch_arrows else "v03f_r4"
    if not patch_arrows:
        assert not (OUT / "ROUGH_MANIFEST_v03f_r4.json").exists(), "v03f_r4 already exists; refusing overwrite"
    NAS_CG.mkdir(parents=True, exist_ok=True)
    GIT_CG.mkdir(parents=True, exist_ok=True)

    arch_items = json.loads((EDIT / "archive_pulls_v01/ARCHIVE_PULLS_RAW_v01.json").read_text())
    for item in arch_items:
        nas_p = Path(item["nas_raw"])
        assert nas_p.exists() and base_cg.digest(nas_p) == item["sha256"], f"Raw archive mismatch: {nas_p}"

    plan = json.loads((EDIT / "PICTURE_PLAN_v03f.json").read_text())
    all_cues = [c for c in plan["overlay_cues"] if c.get("status") == "ANCHORED"]
    free_rows = [r for r in plan["rows"] if r["source_kind"] in ("code_graphic", "free_archive")]
    assert len(free_rows) == 35

    base_cg._init_worker(arch_items)
    if patch_arrows:
        prev_cg = json.loads((GIT_CG / "CODE_GRAPHICS_v03f_r4.json").read_text())
        rendered_rows = list(prev_cg["rendered_clips"])
        for idx, r in enumerate(free_rows):
            rk = f"P{r['part']}:{r['id']}"
            if rk in ARROW_PATCH_IDS:
                ov = [
                    c for c in all_cues
                    if max(float(r["t_s"]), float(c["display_start_s"])) < min(float(r["t_end_s"]), float(c["display_end_s"]))
                ]
                rec = _render_single_row_r4((idx, r, ov, nas_tag))
                assert rec["near_black"] == "PASS", f"Near-black failed on {rk}"
                rendered_rows[idx] = rec
                print(f"Patched vector arrow on {rk} -> {rec['file']}", flush=True)
            else:
                existing = rendered_rows[idx]
                assert base_cg.digest(Path(existing["nas_path"])) == existing["sha256_mp4"], f"Hash mismatch: {rk}"
    else:
        tasks = []
        for idx, r in enumerate(free_rows):
            ov = [
                c for c in all_cues
                if max(float(r["t_s"]), float(c["display_start_s"])) < min(float(r["t_end_s"]), float(c["display_end_s"]))
            ]
            tasks.append((idx, r, ov, nas_tag))

        print(f"Rendering {len(tasks)} v03f-r4 £0 free clips at {W}x{H}@{FPS}fps across 4 workers...", flush=True)
        rendered_rows = []
        with ProcessPoolExecutor(max_workers=4, initializer=base_cg._init_worker, initargs=(arch_items,)) as ex:
            for rec in ex.map(_render_single_row_r4, tasks):
                rendered_rows.append(rec)
                print(
                    f"[{rec['idx']+1:02d}/{len(tasks):02d}] {rec['id']:38s} -> {rec['encoded_s']:4.2f}s "
                    f"mean={rec['min_sample_mean_luma']} std={rec['min_sample_std']} {rec['near_black']}",
                    flush=True,
                )
        rendered_rows.sort(key=lambda x: x["idx"])
        for rec in rendered_rows:
            assert rec["near_black"] == "PASS", f"Near-black failed on {rec['id']}"

    ch_sheet_path = build_chapter_windows_sheet(free_rows, all_cues)

    # Build 390px contact sheet of all 35 v03f-r4 free clips
    cols, tw, th = 4, 390, 219
    rows_n = math.ceil(len(rendered_rows) / cols)
    sheet_im = Image.new("RGB", (cols * tw, rows_n * (th + 42)), (28, 34, 44))
    sd = ImageDraw.Draw(sheet_im)
    sfont = fnt(18, italic=True)
    for i, rec in enumerate(rendered_rows):
        st = Image.open(NAS_CG / rec["still"]).resize((tw, th), Image.Resampling.LANCZOS)
        x, y = (i % cols) * tw, (i // cols) * (th + 42)
        sheet_im.paste(st, (x, y))
        sd.text((x + 6, y + th + 4), f"{rec['id'][:30]} ({rec['t_s']:.2f}-{rec['t_end_s']:.2f}s)", fill=CREAM, font=sfont)
    sheet_path = GIT_CG / "CONTACT_SHEET_v03f_r4_390px.jpg"
    sheet_im.save(sheet_path, quality=90)
    nas_sheet = NAS_CG / f"CONTACT_SHEET_{nas_tag}_390px.jpg"
    assert not nas_sheet.exists(), f"Refusing overwrite on NAS: {nas_sheet}"
    shutil.copy2(sheet_path, nas_sheet)

    # Build QA reel & run polish_gate + picture_qa
    cuts, pool = [], []
    cur_t = 0.0
    for rec in rendered_rows:
        dur = rec["encoded_s"]
        cuts.append({
            "row": rec["id"],
            "timeline_in": round(cur_t, 3),
            "timeline_out": round(cur_t + dur, 3),
            "source": rec["file"],
            "upscale": 1.0,
            "framing": {"offset": 0.0},
            "video": True,
        })
        pool.append({"file_id": rec["file"], "title": f"own code graphic {rec['id']}"})
        cur_t += dur

    concat_txt = NAS_CG / f"concat_list_{nas_tag}.txt"
    assert not concat_txt.exists()
    concat_txt.write_text("".join(f"file '{NAS_CG / rec['file']}'\n" for rec in rendered_rows))
    reel_mp4 = NAS_CG / f"code_graphics_013_reel_{nas_tag}.mp4"
    assert not reel_mp4.exists()
    sp.run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", str(concat_txt), "-c", "copy", str(reel_mp4)], check=True)

    (GIT_CG / "cuts_v03f_r4_cg.json").write_text(json.dumps(cuts, indent=2) + "\n")
    (GIT_CG / "pool_v03f_r4_cg.json").write_text(json.dumps(pool, indent=2) + "\n")

    pg_json = GIT_CG / "polish_gate_v03f_r4.json"
    pg_res = sp.run([
        "python3", str(OWB_ROOT / "scripts/polish_gate.py"),
        str(reel_mp4),
        "--cuts", str(GIT_CG / "cuts_v03f_r4_cg.json"),
        "--out", str(pg_json),
        "--no-jitter",
    ], capture_output=True, text=True, check=True)
    (GIT_CG / "polish_gate_v03f_r4.txt").write_text(pg_res.stdout)
    print(pg_res.stdout, end="", flush=True)

    pqa_dir = GIT_CG / "picture_qa_v03f_r4"
    pqa_dir.mkdir(parents=True, exist_ok=True)
    pqa_res = sp.run([
        "python3", str(OWB_ROOT / "scripts/picture_qa.py"),
        str(reel_mp4),
        "--cuts", str(GIT_CG / "cuts_v03f_r4_cg.json"),
        "--pool", str(GIT_CG / "pool_v03f_r4_cg.json"),
        "--out-dir", str(pqa_dir),
        "--no-jitter",
    ], capture_output=True, text=True, check=True)
    (GIT_CG / "picture_qa_v03f_r4.txt").write_text(pqa_res.stdout)
    print(pqa_res.stdout, end="", flush=True)

    cg_manifest = {
        "film": "013_Darwin-Wallace-Evolution",
        "version": "v03f_r4",
        "task": "J2652",
        "plan_sha256": base_cg.digest(EDIT / "PICTURE_PLAN_v03f.json"),
        "spend": "£0",
        "credits_spent": 0,
        "fps": FPS,
        "resolution": f"{W}x{H}",
        "rendered_clips_count": len(rendered_rows),
        "reel_nas_path": str(reel_mp4),
        "reel_sha256": base_cg.digest(reel_mp4),
        "contact_sheet_390px": str(sheet_path.relative_to(EDIT)),
        "chapter_windows_sheet_390px": str(ch_sheet_path.relative_to(EDIT)),
        "rendered_clips": rendered_rows,
    }
    (GIT_CG / "CODE_GRAPHICS_v03f_r4.json").write_text(json.dumps(cg_manifest, indent=2) + "\n")
    for fn in (
        "cuts_v03f_r4_cg.json",
        "pool_v03f_r4_cg.json",
        "CODE_GRAPHICS_v03f_r4.json",
        "polish_gate_v03f_r4.json",
        "polish_gate_v03f_r4.txt",
        "picture_qa_v03f_r4.txt",
    ):
        nas_fn = fn.replace("v03f_r4", nas_tag)
        assert not (NAS_CG / nas_fn).exists(), f"Refusing overwrite on NAS: {NAS_CG / nas_fn}"
        shutil.copy2(GIT_CG / fn, NAS_CG / nas_fn)

    # Build complete 515s v03f-r4 diagnostic rough
    if SCRATCH.exists():
        shutil.rmtree(SCRATCH)
    SCRATCH.mkdir(parents=True, exist_ok=True)

    vo = NAS_FILM / "02_Voiceover/hos_013_vo_v03a.wav"
    assert base_cg.digest(vo) == plan["vo_sha256"], "VO WAV hash mismatch"
    cg_by_row = {rec["id"]: rec for rec in rendered_rows}

    raw_assets: dict[str, dict] = {}
    for r in plan["rows"]:
        if r["source_kind"] not in ("new_mint_quality", "existing_plate_reuse"):
            continue
        key = "P1:01_study_beaks" if r["source_kind"] == "existing_plate_reuse" else r["source_row_v02"]
        part, rid = key.split(":")
        raw = NAS_FILM / "04_Generated-Clips/archive_v01_pass1" / f"P{int(part[1:]):02d}_{rid}_t1.mp4"
        receipt = Path(str(raw) + ".sha256.json")
        if raw.exists() and receipt.exists():
            expected = json.loads(receipt.read_text())["sha256"]
            assert base_cg.digest(raw) == expected, f"Archive receipt mismatch: {raw.name}"
            dur_av = float(sp.check_output([
                "ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(raw)
            ]))
            raw_assets[r["source_row_v02"]] = {
                "source": str(raw),
                "source_sha256": expected,
                "available_s": dur_av,
            }

    watermark = SCRATCH / "diagnostic_watermark.png"
    wi = Image.new("RGBA", (960, 540), (0, 0, 0, 0))
    wd = ImageDraw.Draw(wi)
    wd.rectangle((8, 502, 490, 534), fill=(0, 0, 0, 190))
    wd.text((12, 507), "TIMING ONLY - RAW TAKE - NOT KEEP", font=ImageFont.truetype(ARIAL_FONT, 18), fill=(255, 235, 0, 255))
    wi.save(watermark)

    def render_beat(item: tuple[int, dict]) -> tuple[int, Path, dict]:
        i, r = item
        row_key = f"P{r['part']}:{r['id']}"
        duration = round(r["t_end_s"] - r["t_s"], 2)
        target = SCRATCH / f"row_{i:03d}.mp4"
        frame = SCRATCH / f"frame_{i:03d}.jpg"

        if r["source_kind"] in ("code_graphic", "free_archive"):
            cg_rec = cg_by_row[row_key]
            cg_path = Path(cg_rec["nas_path"])
            sp.run([
                "ffmpeg", "-v", "error", "-y", "-i", str(cg_path),
                "-vf", "scale=960:540:flags=lanczos,setsar=1,fps=50",
                "-frames:v", str(round(duration * 50)),
                "-an", "-c:v", "libx264", "-preset", "ultrafast", "-crf", "23", "-pix_fmt", "yuv420p",
                "-threads", "2", str(target),
            ], check=True)
            sample_t = 1.25 if r["id"] == "01_card_p02" else (duration / 2)
            record = {
                "row": row_key,
                "start_s": r["t_s"],
                "end_s": r["t_end_s"],
                "status": "v03f_free_render",
                "source": str(cg_path),
                "source_offset_s": 0.0,
                "source_sha256": cg_rec["sha256_mp4"],
                "crop": None,
                "reason": "Built £0 v03f-r4 1920x1080@50fps render (unclipped archival credits, enlarged 390px labels, verified P2:01 title)",
            }
        elif r["source_row_v02"] in raw_assets:
            ra = raw_assets[r["source_row_v02"]]
            source = ra["source"]
            avail = ra["available_s"]
            offset = float(r["source_window_s"][0])
            retime_factor = None
            if r["source_row_v02"] == "P2:11_island_split_vision":
                retime_factor = round(8.00 / avail, 6)
            elif r["source_row_v02"] == "P3:02b_notebook_d_open":
                offset = round(7.90 - duration, 2)
            is_detail = ("_beat2" in r["id"] or r["id"].endswith("_detail"))
            crop = "crop=trunc(iw*0.88/2)*2:trunc(ih*0.88/2)*2," if is_detail else ""
            if retime_factor is not None:
                vf = f"setpts={retime_factor:.6f}*PTS,trim=start={offset:.3f}:duration={duration:.3f},setpts=PTS-STARTPTS,{crop}scale=960:540:flags=lanczos,setsar=1,fps=50"
                args = ["-i", source, "-i", str(watermark)]
            else:
                assert offset + duration <= avail + 0.002
                vf = f"{crop}scale=960:540:flags=lanczos,setsar=1,fps=50"
                args = ["-ss", str(offset), "-i", source, "-i", str(watermark)]
            sp.run([
                "ffmpeg", "-v", "error", "-y", *args,
                "-filter_complex", f"[0:v]{vf}[base];[base][1:v]overlay=0:0",
                "-frames:v", str(round(duration * 50)),
                "-an", "-c:v", "libx264", "-preset", "ultrafast", "-crf", "26", "-pix_fmt", "yuv420p",
                "-threads", "2", str(target),
            ], check=True)
            sample_t = duration / 2
            note = "Raw first take only; NOT KEEP"
            if r["source_row_v02"] in PENDING_RETAKE_ROWS:
                note += " (pending Quality retake per Chief #6822411223)"
            elif retime_factor is not None:
                note += f" (retimed x{retime_factor:.4f} 7.917->8.00s per Chief #6822411223, no freeze)"
            elif r["source_row_v02"] == "P3:02b_notebook_d_open":
                note += f" (shifted in-point {offset:.2f}-7.90s per Chief #6822305911/#6822411223)"
            record = {
                "row": row_key,
                "start_s": r["t_s"],
                "end_s": r["t_end_s"],
                "status": "raw_pass1_take",
                "source": source,
                "source_offset_s": offset,
                "source_sha256": ra["source_sha256"],
                "retime_factor": retime_factor,
                "crop": "centred 88 percent diagnostic detail" if is_detail else None,
                "reason": note,
            }
        else:
            reason = "Unminted Quality row — awaits J2529 Pass-1 Part 5/6 generation (0 credits spent)"
            im = Image.new("RGB", (960, 540), "#293340")
            d = ImageDraw.Draw(im)
            lines = [
                "J2652 DIAGNOSTIC — UNMINTED PASS-1 ROW",
                row_key,
                f"{r['t_s']:.2f}–{r['t_end_s']:.2f} s ({duration:.2f} s)",
                reason,
                "",
                *textwrap.wrap(r["shot_description"], 64),
            ]
            d.multiline_text((28, 25), "\n".join(lines), font=ImageFont.truetype(ARIAL_FONT, 22), fill="white", spacing=7)
            slate = SCRATCH / f"row_{i:03d}.png"
            im.save(slate)
            sp.run([
                "ffmpeg", "-v", "error", "-y", "-loop", "1", "-framerate", "50", "-i", str(slate),
                "-vf", "setsar=1,fps=50", "-frames:v", str(round(duration * 50)),
                "-an", "-c:v", "libx264", "-preset", "ultrafast", "-crf", "27", "-pix_fmt", "yuv420p",
                "-threads", "2", str(target),
            ], check=True)
            sample_t = duration / 2
            record = {
                "row": row_key,
                "start_s": r["t_s"],
                "end_s": r["t_end_s"],
                "status": "diagnostic_slate",
                "source": None,
                "source_offset_s": None,
                "source_sha256": None,
                "crop": None,
                "reason": reason,
            }

        sp.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{sample_t:.3f}", "-i", str(target), "-frames:v", "1", str(frame)], check=True)
        return i, frame, record

    print(f"Assembling 515s v03f-r4 diagnostic rough across {len(plan['rows'])} beats...", flush=True)
    results = []
    with ThreadPoolExecutor(max_workers=4) as ex:
        for res in ex.map(render_beat, list(enumerate(plan["rows"]))):
            results.append(res)
    results.sort(key=lambda x: x[0])
    inventory = [r[2] for r in results]
    sheets = [(r[1], r[2]) for r in results]

    concat = SCRATCH / "concat.txt"
    concat.write_text("".join(f"file 'row_{i:03d}.mp4'\n" for i in range(len(plan["rows"]))))

    ass = SCRATCH / "onsets.ass"

    def stamp(t: float) -> str:
        return f"{int(t // 3600)}:{int(t // 60) % 60:02d}:{t % 60:05.2f}"

    header = (
        "[Script Info]\nScriptType: v4.00+\nPlayResX: 960\nPlayResY: 540\n[V4+ Styles]\n"
        "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, "
        "Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, "
        "Alignment, MarginL, MarginR, MarginV, Encoding\n"
        "Style: Default,Arial,20,&H0000FFFF,&H0000FFFF,&H00000000,&H80000000,0,0,0,0,100,100,0,0,3,2,0,8,20,20,12,1\n"
        "[Events]\nFormat: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n"
    )
    events = [
        f"Dialogue: 0,{stamp(c['display_start_s'])},{stamp(c['display_end_s'])},Default,,0,0,0,,PLANNED CUE: {c['overlay'].get('line_1', c['overlay'].get('label', ''))}"
        for c in plan["overlay_cues"] if c["status"] == "ANCHORED"
    ]
    ass.write_text(header + "\n".join(events) + "\n")

    master = SCRATCH / f"hos_013_timing_rough_J2652_{nas_tag}.mp4"
    sp.run([
        "ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", str(concat),
        "-i", str(vo), "-i", str(ass),
        "-map", "0:v", "-map", "1:a", "-map", "2:s",
        "-c:v", "copy", "-c:s", "mov_text",
        "-threads", "2", "-c:a", "aac", "-b:a", "192k", "-af", "apad", "-t", "515",
        "-movflags", "+faststart", str(master),
    ], check=True)
    sp.run(["ffmpeg", "-v", "error", "-i", str(master), "-f", "null", "-"], check=True)

    n_pages = math.ceil(len(sheets) / 20)
    sheet_paths = []
    for page in range(n_pages):
        im = Image.new("RGB", (390 * 4, 260 * 5), "#202733")
        d = ImageDraw.Draw(im)
        for k, (path, r) in enumerate(sheets[page * 20:(page + 1) * 20]):
            x = (k % 4) * 390
            y = (k // 4) * 260
            thumb = Image.open(path).resize((390, 219), Image.Resampling.LANCZOS)
            im.paste(thumb, (x, y))
            tag = "FREE" if r["status"] == "v03f_free_render" else ("RAW" if r["status"] == "raw_pass1_take" else "SLATE")
            d.text((x + 4, y + 221), f"{r['row']} [{tag}]\n{r['start_s']:.2f}–{r['end_s']:.2f}s", font=ImageFont.truetype(ARIAL_FONT, 12), fill="white")
        dest_git = OUT / f"phone_contact_v03f_r4_{page + 1:02d}.jpg"
        im.save(dest_git, quality=90)
        sheet_paths.append(dest_git)

    NAS_ROUGH.mkdir(parents=True, exist_ok=True)
    copies = []
    for src in [master, *sheet_paths]:
        nas_name = src.name.replace("v03f_r4", nas_tag) if nas_tag != "v03f_r4" and "v03f_r4" in src.name else src.name
        dest = NAS_ROUGH / nas_name
        assert not dest.exists(), f"Refusing overwrite on NAS: {dest}"
        shutil.copy2(src, dest)
        assert base_cg.digest(src) == base_cg.digest(dest)
        copies.append({"path": str(dest), "sha256": base_cg.digest(dest)})

    counts = collections.Counter(r["status"] for r in inventory)
    (OUT / "asset_inventory_v03f_r4.json").write_text(json.dumps(inventory, indent=2, ensure_ascii=False) + "\n")
    (OUT / "ROUGH_MANIFEST_v03f_r4.json").write_text(json.dumps({
        "files": copies,
        "vo_sha256": base_cg.digest(vo),
        "plan_sha256": base_cg.digest(EDIT / "PICTURE_PLAN_v03f.json"),
        "code_graphics_v03f_r4_sha256": base_cg.digest(GIT_CG / "CODE_GRAPHICS_v03f_r4.json"),
        "duration_s": 515,
        "fps": 50,
        "credits_spent": 0,
        "gbp_spent": 0,
        "approved": False,
        "status_counts": dict(counts),
        "slates": counts["diagnostic_slate"],
        "limitations": (
            "All 35 £0 code-graphic/archive beats use finished v03f-r4 1920x1080@50fps renders (fixing all 3 items from "
            "Claude review #6945397541: unclipped bottom-left archival credits, enlarged 390px tags/labels, and verified "
            "P2:01 Part II title window). 58 beats use receipt-verified Pass-1 takes marked NOT KEEP (including Chief "
            "#6822411223 P2:11 x1.0105 retime and P3:02b 3.82-7.90s window; rows P1:03a, P1:07, P3:02a still await Pass-1 "
            "retakes). 11 beats (P5:08a through P6:08b) remain explicit slates awaiting J2529 Pass-1 Part 5/6 generation. "
            "No music/SFX; no audio or moving-video perception claimed."
        ),
    }, indent=2, ensure_ascii=False) + "\n")
    shutil.rmtree(SCRATCH, ignore_errors=True)
    print(f"V03F_R4 COMPLETE: {dict(counts)} — NAS COPY & FULL DECODE VERIFIED", flush=True)


if __name__ == "__main__":
    main()
