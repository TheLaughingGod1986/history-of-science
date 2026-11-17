#!/usr/bin/env python3
"""J2652 (step 3/3): Build all 35 £0 v03f-timed free picture assets for HOS 013 Darwin & Wallace.

- Reads exact beat durations, chapter_title_window_s, and word-level overlay_cues from PICTURE_PLAN_v03f.json.
- Verifies SHA-256 of every raw Wikimedia public-domain scan/portrait on NAS before use.
- Renders 35 distinct 1920x1080 50fps H.264 .mp4 clips to NAS (code_graphics_v03f/), including:
  * All 5 newly converted v02 free rows (P2:10b, P3:09a, P4:07b, P5:02b_wide/_detail, P5:04b)
  * Distinct stage-by-stage animations across all split multi-beat graphics (_beat1/_beat2/_beat3)
  * Exact word-onset timing for anchored labels & WHO cards (<= 3.8s hold, one label/card at a time)
  * Chapter title cartouches strictly bounded to chapter_title_window_s (2.50s hold)
- Runs polish_gate.py and picture_qa.py on the 35-clip QA reel and saves 390px phone contact sheets.
- Spend: £0 / 0 credits. Does not touch v01, v02, or earlier timing roughs.
"""
from __future__ import annotations

from concurrent.futures import ProcessPoolExecutor
import hashlib
import json
import math
import shutil
import subprocess as sp
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

W, H, FPS = 1920, 1080, 50
FONT = "/System/Library/Fonts/Supplemental/Didot.ttc"
EDIT = Path(__file__).resolve().parent
FILM = EDIT.parent
OWB_ROOT = Path("/Users/benjaminoats/YouTube/orbit-with-ben")
NAS_FILM = Path("/Volumes/data/studio-live/History Of Science/02_Video-Projects") / FILM.name
NAS_EDIT = NAS_FILM / "07_Edit-Project"
NAS_RAW_DIR = NAS_EDIT / "archive_pulls_v01/raw"
NAS_OUT_DIR = NAS_EDIT / "code_graphics_v03f"
GIT_OUT_DIR = EDIT / "code_graphics_v03f"

CREAM = (246, 232, 202)
GOLD = (226, 184, 102)
PALE = (208, 188, 158)
TAN = (162, 132, 100)
CLAY = (118, 90, 70)
WHITE = (244, 240, 228)
TEAL = (118, 184, 192)
CRIMSON = (204, 88, 78)
DARK_INK = (44, 34, 26)

CHAPTER_TITLES = {
    2: ("II", "The Birds He Forgot to Label"),
    3: ("III", "The Engine and the Barnacles"),
    4: ("IV", "Fever in the Islands"),
    5: ("V", "The Night Nobody Noticed"),
    6: ("VI", "The Missing Piece"),
}

WHO_PORTRAIT_MAP = {
    "Fleeming Jenkin": "who_fleeming_jenkin",
    "Gregor Mendel": "who_gregor_mendel",
    "Charles Darwin": "who_charles_darwin",
    "Alfred Russel Wallace": "who_alfred_russel_wallace",
    "John Gould": "who_john_gould",
    "Thomas Malthus": "who_thomas_malthus",
    "Emma Darwin": "who_emma_darwin",
    "Charles Lyell": "who_charles_lyell",
    "Joseph Hooker": "who_joseph_hooker",
    "Herbert Spencer": "who_herbert_spencer",
}


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def fnt(size: int, italic: bool = False, bold: bool = False) -> ImageFont.FreeTypeFont:
    idx = 1 if italic else (2 if bold else 0)
    try:
        return ImageFont.truetype(FONT, size, index=idx)
    except Exception:
        return ImageFont.truetype(FONT, size, index=0)


def ease(u: float) -> float:
    u = max(0.0, min(1.0, u))
    return u * u * (3.0 - 2.0 * u)


def prog(t: float, a: float, b: float) -> float:
    return ease((t - a) / (b - a)) if b > a else 1.0


def make_base_canvas(seed: int = 1303) -> np.ndarray:
    """Warm Victorian study & parchment desk canvas (mean ~62, p95 ~115, luma std ~24, zero straight seams)."""
    y, x = np.mgrid[:H, :W].astype(np.float32)
    nx = (x - W * 0.5) / (W * 0.5)
    ny = (y - H * 0.5) / (H * 0.5)
    r2 = nx * nx * 0.82 + ny * ny * 1.04
    vignette = np.clip(1.0 - 0.68 * r2, 0.16, 1.0)

    wave1 = np.sin(nx * 5.4 + ny * 2.3) * 11.5 + np.cos(ny * 6.9 - nx * 3.6) * 9.5
    wave2 = np.sin((nx * nx + ny * ny) * 9.2) * 8.0
    rng = np.random.default_rng(seed)
    grain = rng.normal(0.0, 2.6, (H, W)).astype(np.float32)

    base = np.zeros((H, W, 3), np.float32)
    c_dark = np.array([24.0, 30.0, 40.0], np.float32)
    c_light = np.array([112.0, 96.0, 76.0], np.float32)
    for c in range(3):
        base[:, :, c] = c_dark[c] + (c_light[c] - c_dark[c]) * vignette + wave1 + wave2 + grain

    im = Image.fromarray(np.uint8(np.clip(base, 0, 255)), "RGB")
    d = ImageDraw.Draw(im)
    # Engraved botanical & meridian arcs in corners (high edge detail, zero straight full-frame lines)
    for k in range(8):
        rad = 160 + k * 52
        d.arc((-rad, -rad, rad * 2, rad * 2), 12, 82, fill=(134, 114, 88), width=2)
        d.arc((W - rad * 2, H - rad * 2, W + rad, H + rad), 192, 262, fill=(134, 114, 88), width=2)
        d.arc((W - rad * 2, -rad, W + rad, rad * 2), 98, 168, fill=(126, 106, 82), width=2)
        d.arc((-rad, H - rad * 2, rad * 2, H + rad), 278, 348, fill=(126, 106, 82), width=2)

    for cx, cy in ((205, 235), (1715, 845), (205, 845), (1715, 235)):
        for r in (38, 64, 92, 118):
            d.ellipse((cx - r, cy - r, cx + r, cy + r), outline=(138, 118, 90), width=2)
        for ang_deg in range(0, 360, 20):
            ang = math.radians(ang_deg)
            x1 = cx + int(32 * math.cos(ang))
            y1 = cy + int(32 * math.sin(ang))
            x2 = cx + int(122 * math.cos(ang))
            y2 = cy + int(122 * math.sin(ang))
            d.line((x1, y1, x2, y2), fill=(128, 108, 84), width=2)

    return np.asarray(im, dtype=np.uint8)


def make_oval_portrait(src_im: Image.Image, size: int = 340) -> Image.Image:
    w, h = src_im.size
    s = min(w, h)
    left = (w - s) // 2
    top = max(0, (h - s) // 3)
    im_sq = src_im.crop((left, top, left + s, top + s)).resize((size - 36, size - 36), Image.Resampling.LANCZOS)
    canvas = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    mask = Image.new("L", (size - 36, size - 36), 0)
    ImageDraw.Draw(mask).ellipse((4, 4, size - 40, size - 40), fill=255)
    canvas.paste(im_sq, (18, 18), mask)
    d = ImageDraw.Draw(canvas)
    d.ellipse((12, 12, size - 12, size - 12), outline=(226, 184, 102, 255), width=6)
    d.ellipse((20, 20, size - 20, size - 20), outline=(246, 232, 202, 225), width=2)
    return canvas


def draw_anchored_cues(
    im: Image.Image,
    d: ImageDraw.ImageDraw,
    abs_t: float,
    row_t0: float,
    row_t1: float,
    cues: list[dict],
    portrait_cache: dict[str, Image.Image],
    show_portrait: bool = True,
) -> bool:
    """Draw any active anchored overlay cue at abs_t. Returns True if a label/card is visible (enforcing one-at-a-time)."""
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
            # Sourced oval portrait medallion with gentle parallax
            pid = WHO_PORTRAIT_MAP.get(name)
            if show_portrait and pid and pid in portrait_cache:
                med = portrait_cache[pid]
                py = 195 + int(12 * (1.0 - a))
                px = 1320
                im.paste(med, (px, py), med)
            # Lower-third cream-on-brown house card (name line 1, years & role line 2)
            bx0, by0, bx1, by1 = 120, H - 235, 980, H - 92
            d.rounded_rectangle((bx0, by0, bx1, by1), radius=22, fill=(52, 42, 32), outline=GOLD, width=4)
            d.text((bx0 + 28, by0 + 18), name, font=fnt(48, italic=True), fill=GOLD)
            d.text((bx0 + 28, by0 + 78), sub, font=fnt(34, italic=True), fill=CREAM)
            return True
        else:
            label = ov.get("label") or ov.get("line_1") or ""
            if not label:
                continue
            font = fnt(54, italic=True)
            col = tuple(int(v * a + 48 * (1.0 - a)) for v in WHITE)
            d.rounded_rectangle((112, 74, 112 + d.textbbox((0, 0), label, font=font)[2] + 44, 162), radius=18, fill=(48, 38, 28), outline=GOLD, width=3)
            d.text((134, 86), label, font=font, fill=col)
            return True
    return False


def draw_archive_credit_if_clear(d: ImageDraw.ImageDraw, credit: str, cue_active: bool, t: float) -> None:
    """Corner credit line in white Didot italic bottom-left; waits whenever any other label/card is on screen."""
    if cue_active or t < 0.20:
        return
    font = fnt(28, italic=True)
    d.text((112, H - 72), credit, font=font, fill=PALE)


def paste_doc_card(
    im: Image.Image,
    d: ImageDraw.ImageDraw,
    src_im: Image.Image,
    box_w: int,
    box_h: int,
    cx: int,
    cy: int,
    zoom: float = 1.0,
    focus_xy: tuple[float, float] = (0.5, 0.5),
) -> tuple[int, int, int, int]:
    tw = max(box_w + 4, int(box_w * zoom))
    th = max(box_h + 4, int(box_h * zoom))
    resized = src_im.resize((tw, th), Image.Resampling.LANCZOS)
    fx, fy = focus_xy
    x0 = max(0, min(tw - box_w, int((tw - box_w) * fx)))
    y0 = max(0, min(th - box_h, int((th - box_h) * fy)))
    cropped = resized.crop((x0, y0, x0 + box_w, y0 + box_h))
    px, py = cx - box_w // 2, cy - box_h // 2
    d.rounded_rectangle((px - 20, py - 20, px + box_w + 20, py + box_h + 20), radius=26, fill=(52, 42, 32), outline=GOLD, width=5)
    d.rounded_rectangle((px - 10, py - 10, px + box_w + 10, py + box_h + 10), radius=18, outline=CREAM, width=2)
    im.paste(cropped, (px, py))
    return px, py, box_w, box_h


def render_row_frame(
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
        ch_num, title = CHAPTER_TITLES[pnum]
        ch_win = row.get("chapter_title_window_s") or [row["t_s"], min(row["t_end_s"], row["t_s"] + 2.50)]
        win_dur = max(0.5, float(ch_win[1]) - float(ch_win[0]))
        cx, cy = W // 2, H // 2
        if t <= win_dur:
            a = min(prog(t, 0.0, 0.38), prog(win_dur, t, win_dur - 0.38))
            rx = int(590 + 36 * ease(t / win_dur))
            ry = int(235 + 14 * ease(t / win_dur))
            d.rounded_rectangle((cx - rx, cy - ry, cx + rx, cy + ry), radius=48, fill=(56, 46, 36), outline=GOLD, width=5)
            d.rounded_rectangle((cx - rx + 18, cy - ry + 18, cx + rx - 18, cy + ry - 18), radius=38, outline=CREAM, width=2)
            if a > 0.05:
                f_num = fnt(52, italic=True)
                f_tit = fnt(68, italic=True)
                b1 = d.textbbox((0, 0), f"Part {ch_num}", font=f_num)
                d.text((cx - (b1[2] - b1[0]) // 2, cy - 98), f"Part {ch_num}", font=f_num, fill=GOLD)
                b2 = d.textbbox((0, 0), title, font=f_tit)
                d.text((cx - (b2[2] - b2[0]) // 2, cy - 10), title, font=f_tit, fill=CREAM)
            ang = -0.65 + 1.3 * (t / win_dur)
            d.line((cx - 145, cy + 118, cx + int(145 * math.cos(ang)), cy + 118 + int(28 * math.sin(ang))), fill=GOLD, width=4)
            d.ellipse((cx - 8, cy + 110, cx + 8, cy + 126), fill=CREAM)
        else:
            # Post-title animated case-file desk motif (so P2:01 2.50-6.10s and P6:01 2.50-5.34s stay rich & clear for WHO cards)
            post_u = (t - win_dur) / max(0.2, dur - win_dur)
            d.rounded_rectangle((190, 175, 1180, 775), radius=34, fill=(64, 52, 40), outline=GOLD, width=4)
            # Inked specimen case-file rings & meridian lines
            for k in range(5):
                rr = 95 + k * 44 + int(10 * math.sin(post_u * math.pi + k))
                d.arc((685 - rr, 475 - rr, 685 + rr, 475 + rr), 15 + k * 25, 225 + k * 25, fill=GOLD if k % 2 == 0 else CREAM, width=3)
            # Compass divider arms opening smoothly
            ang = 0.25 + 0.45 * ease(post_u)
            d.line((685, 310, 685 - int(220 * math.sin(ang)), 310 + int(280 * math.cos(ang))), fill=CREAM, width=5)
            d.line((685, 310, 685 + int(220 * math.sin(ang)), 310 + int(280 * math.cos(ang))), fill=GOLD, width=5)
            d.ellipse((675, 300, 695, 320), fill=GOLD, outline=CREAM, width=3)
            draw_anchored_cues(im, d, abs_t, row["t_s"], row["t_end_s"], cues, portrait_cache, show_portrait=True)
            if pnum == 6:
                # Credit Jenkin portrait only if needed; portrait is PD engraving
                pass
        return

    # 2. Cream end card
    if rid == "09_cream_end_card":
        cx, cy = W // 2, H // 2
        d.rounded_rectangle((cx - 560, cy - 280, cx + 560, cy + 280), radius=46, fill=(72, 58, 44), outline=GOLD, width=4)
        for k in range(9):
            r = int(110 + k * 42 + 16 * math.sin(u * math.pi + k * 0.5))
            d.ellipse((cx - r, cy - int(r * 0.60), cx + r, cy + int(r * 0.60)), outline=GOLD if k % 2 == 0 else TAN, width=3)
        branches = [
            ((cx, cy + 165), (cx, cy + 30)),
            ((cx, cy + 30), (cx - 115, cy - 60)),
            ((cx, cy + 30), (cx + 115, cy - 60)),
            ((cx - 115, cy - 60), (cx - 175, cy - 148)),
            ((cx - 115, cy - 60), (cx - 55, cy - 152)),
            ((cx + 115, cy - 60), (cx + 55, cy - 152)),
            ((cx + 115, cy - 60), (cx + 175, cy - 148)),
        ]
        for (x0, y0), (x1, y1) in branches:
            d.line((x0, y0, x1, y1), fill=CREAM, width=5)
            d.ellipse((x1 - 8, y1 - 8, x1 + 8, y1 + 8), fill=GOLD)
        return

    # 3. P1:08 split into 3 distinct beats
    if rid.startswith("08_cg_i_think_tree_beat"):
        cue_active = draw_anchored_cues(im, d, abs_t, row["t_s"], row["t_end_s"], cues, portrait_cache)
        if rid.endswith("_beat1"):
            paste_doc_card(im, d, scan_cache["darwin_tree_1837"], 540, 680, 470, 545, zoom=1.04 + 0.08 * ease(u), focus_xy=(0.5, 0.62))
            nodes = [
                ((1280, 760), (1280, 580), 0.0, 0.25),
                ((1280, 580), (1100, 430), 0.20, 0.52),
                ((1280, 580), (1460, 430), 0.24, 0.56),
                ((1100, 430), (995, 285), 0.48, 0.82),
                ((1100, 430), (1185, 275), 0.52, 0.86),
                ((1460, 430), (1370, 275), 0.56, 0.90),
                ((1460, 430), (1565, 285), 0.60, 0.94),
            ]
            for (x0, y0), (x1, y1), a0, a1 in nodes:
                s = prog(u, a0, a1)
                if s > 0:
                    xm, ym = int(x0 + (x1 - x0) * s), int(y0 + (y1 - y0) * s)
                    d.line((x0, y0, xm, ym), fill=GOLD, width=7)
                    if s >= 0.95:
                        d.ellipse((x1 - 10, y1 - 10, x1 + 10, y1 + 10), fill=CREAM, outline=GOLD, width=3)
            if not cue_active:
                d.text((1090, 815), "ONE ROOT → MANY", font=fnt(42, italic=True), fill=CREAM)
            draw_archive_credit_if_clear(d, "Cambridge Univ. Library · MS DAR 121:36 (PD)", cue_active or True, t)
        elif rid.endswith("_beat2"):
            # Zoom into upper "I think" header of Notebook B p. 36
            px, py, bw, bh = paste_doc_card(im, d, scan_cache["darwin_tree_1837"], 760, 620, 640, 540, zoom=1.35 + 0.14 * ease(u), focus_xy=(0.48, 0.16))
            ul = int(340 * prog(t, 0.25, dur * 0.75))
            d.line((px + 170, py + 195, px + 170 + ul, py + 195), fill=GOLD, width=7)
            d.rounded_rectangle((1120, 360, 1740, 660), radius=28, fill=(54, 44, 34), outline=GOLD, width=4)
            d.text((1175, 420), "“I think”", font=fnt(82, italic=True), fill=GOLD)
            d.text((1180, 545), "NOTEBOOK B · 1837", font=fnt(38, italic=True), fill=CREAM)
        else:
            # Beat 3: 20-year secrecy bar (1838 -> 1858)
            paste_doc_card(im, d, scan_cache["darwin_tree_1837"], 440, 560, 410, 560, zoom=1.08, focus_xy=(0.5, 0.5))
            bar_p = prog(t, 0.15, dur * 0.78)
            bx0, by0, bw, bh = 740, 540, 980, 74
            d.rounded_rectangle((bx0, by0, bx0 + bw, by0 + bh), radius=22, fill=(46, 38, 30), outline=GOLD, width=4)
            fill_w = int((bw - 10) * bar_p)
            if fill_w > 14:
                d.rounded_rectangle((bx0 + 5, by0 + 5, bx0 + 5 + fill_w, by0 + bh - 5), radius=18, fill=GOLD)
            yr = 1838 + int(round(20 * bar_p))
            d.text((bx0, by0 - 95), f"1838  →  {yr}", font=fnt(64, italic=True), fill=GOLD)
            if not cue_active:
                d.text((bx0, by0 + 105), f"{int(round(20 * bar_p))} YEARS LOCKED AWAY", font=fnt(42, italic=True), fill=CREAM)
        return

    # 4. P1:10 globe arc
    if rid == "10_cg_globe_arc":
        cue_active = draw_anchored_cues(im, d, abs_t, row["t_s"], row["t_end_s"], cues, portrait_cache)
        gx, gy, gr = 650, 555, 340
        d.ellipse((gx - gr, gy - gr, gx + gr, gy + gr), fill=(38, 56, 72), outline=GOLD, width=5)
        for lat in (-190, -95, 0, 95, 190):
            d.arc((gx - gr + 26, gy + lat - 55, gx + gr - 26, gy + lat + 55), 10, 170, fill=(88, 110, 128), width=2)
        kent, malay = (gx - 115, gy - 148), (gx + 190, gy + 68)
        d.ellipse((kent[0] - 11, kent[1] - 11, kent[0] + 11, kent[1] + 11), fill=CREAM, outline=GOLD, width=3)
        d.ellipse((malay[0] - 11, malay[1] - 11, malay[0] + 11, malay[1] + 11), fill=GOLD, outline=CREAM, width=3)
        arc_p = prog(t, 0.2, dur * 0.76)
        pts = []
        for k in range(max(2, int(48 * arc_p)) + 1):
            s = k / 48.0
            pts.append((int((1 - s) * malay[0] + s * kent[0]), int((1 - s) * malay[1] + s * kent[1] - 148 * math.sin(s * math.pi))))
        if len(pts) >= 2:
            d.line(pts, fill=GOLD, width=7)
        st_p = prog(t, 0.5, dur * 0.85)
        for k in range(max(1, int(18 * st_p))):
            yy = 730 - k * 15
            d.rounded_rectangle((1160, yy - 12, 1410, yy), radius=4, fill=CREAM, outline=TAN, width=2)
        d.rounded_rectangle((1490, 700, 1730, 728), radius=5, fill=GOLD, outline=CREAM, width=2)
        if not cue_active:
            d.text((1170, 755), "1844 · 230 PAGES", font=fnt(34, italic=True), fill=CREAM)
            d.text((1495, 755), "1858 · PACKET", font=fnt(34, italic=True), fill=GOLD)
        return

    # 5. P2:06b tortoise shells
    if rid == "06b_cg_tortoise_shells":
        cue_active = draw_anchored_cues(im, d, abs_t, row["t_s"], row["t_end_s"], cues, portrait_cache)
        p_draw = prog(t, 0.15, dur * 0.78)
        d.rounded_rectangle((180, 230, 880, 830), radius=30, fill=(56, 46, 36), outline=CREAM, width=3)
        d.rounded_rectangle((1040, 230, 1740, 830), radius=30, fill=(56, 46, 36), outline=GOLD, width=4)
        cx1, cy1 = 530, 620
        d.chord((cx1 - 245, cy1 - 225, cx1 + 245, cy1 + 80), 180, 180 + int(180 * p_draw), fill=(98, 80, 58), outline=CREAM, width=5)
        for r_sc in range(3):
            d.arc((cx1 - 180 + r_sc * 40, cy1 - 170 + r_sc * 25, cx1 + 180 - r_sc * 40, cy1 + 20), 195, 345, fill=GOLD, width=3)
        cx2, cy2 = 1390, 620
        d.chord((cx2 - 245, cy2 - 255, cx2 + 245, cy2 + 80), 205, 205 + int(155 * p_draw), fill=(118, 92, 64), outline=GOLD, width=5)
        if p_draw > 0.2:
            d.arc((cx2 - 260, cy2 - 215, cx2 - 105, cy2 - 40), 250, 70, fill=CREAM, width=6)
        if not cue_active:
            d.text((cx1 - 140, cy1 + 108), "DOME SHELL", font=fnt(40, italic=True), fill=CREAM)
            d.text((cx2 - 165, cy2 + 108), "SADDLE ARCH", font=fnt(40, italic=True), fill=GOLD)
        return

    # 6. P2:09 finch toolbox split into beat1 (heavy seed beaks) and beat2 (slender insect/cactus probes)
    if rid.startswith("09_cg_finch_toolbox_beat"):
        cue_active = draw_anchored_cues(im, d, abs_t, row["t_s"], row["t_end_s"], cues, portrait_cache)
        if rid.endswith("_beat1"):
            paste_doc_card(im, d, scan_cache["gould_finches_1845"], 620, 640, 490, 560, zoom=1.04 + 0.08 * ease(u), focus_xy=(0.35, 0.35))
            beaks = [
                ("1. HEAVY NUTCRACKER", 390, 64, GOLD),
                ("2. STOUT SEED PLIERS", 650, 46, CREAM),
            ]
            for idx, (lbl, yy, depth, col) in enumerate(beaks):
                s = prog(t, 0.35 + idx * 1.4, 2.0 + idx * 1.4)
                if s > 0:
                    bx, blen = 930, int(210 * s)
                    d.rounded_rectangle((890, yy - 95, 1760, yy + 95), radius=22, fill=(52, 42, 32), outline=col, width=3)
                    d.polygon([(bx, yy - depth), (bx + blen, yy), (bx, yy + depth)], fill=col, outline=WHITE)
                    if not cue_active:
                        d.text((bx + 240, yy - 24), lbl, font=fnt(38, italic=True), fill=col)
        else:
            paste_doc_card(im, d, scan_cache["gould_finches_1845"], 620, 640, 490, 560, zoom=1.22 + 0.10 * ease(u), focus_xy=(0.68, 0.72))
            beaks = [
                ("3. FINE TWEEZERS", 390, 28, PALE),
                ("4. CACTUS PROBE", 650, 16, TEAL),
            ]
            for idx, (lbl, yy, depth, col) in enumerate(beaks):
                s = prog(t, 0.25 + idx * 1.2, 1.8 + idx * 1.2)
                if s > 0:
                    bx, blen = 930, int(245 * s)
                    d.rounded_rectangle((890, yy - 95, 1760, yy + 95), radius=22, fill=(52, 42, 32), outline=col, width=3)
                    d.polygon([(bx, yy - depth), (bx + blen, yy), (bx, yy + depth)], fill=col, outline=WHITE)
                    if not cue_active:
                        d.text((bx + 265, yy - 24), lbl, font=fnt(38, italic=True), fill=col)
            draw_archive_credit_if_clear(d, "John Gould · Journal of Researches (1845, PD)", cue_active, t)
        return

    # 7. NEW v02 free_archive: P2:10b_shipmate_tagged_tray
    if rid == "10b_shipmate_tagged_tray":
        cue_active = draw_anchored_cues(im, d, abs_t, row["t_s"], row["t_end_s"], cues, portrait_cache)
        paste_doc_card(im, d, scan_cache["gould_finches_1845"], 660, 640, 530, 540, zoom=1.08 + 0.08 * ease(u), focus_xy=(0.5, 0.45))
        tags = [("CHATHAM ISLAND", 290), ("JAMES ISLAND", 520), ("CHARLES ISLAND", 750)]
        for idx, (island, yy) in enumerate(tags):
            s = prog(t, 0.15 + idx * 0.55, 0.95 + idx * 0.55)
            if s > 0:
                tx = int(1020 + 40 * (1.0 - s))
                d.rounded_rectangle((tx, yy - 62, tx + 680, yy + 62), radius=18, fill=(232, 214, 182), outline=GOLD, width=4)
                d.ellipse((tx + 28, yy - 12, tx + 52, yy + 12), fill=(56, 46, 36), outline=GOLD, width=3)
                d.line((tx - 65, yy, tx + 28, yy), fill=TAN, width=4)
                if idx == 0 and not cue_active:
                    d.text((tx + 82, yy - 24), island, font=fnt(38, italic=True), fill=DARK_INK)
                else:
                    # Decorative inked specimen ledger rule lines so only 1 readable label shows at a time
                    d.line((tx + 85, yy - 12, tx + 560, yy - 12), fill=CLAY, width=4)
                    d.line((tx + 85, yy + 16, tx + 430, yy + 16), fill=TAN, width=3)
        draw_archive_credit_if_clear(d, "Gould · Darwin's Finches (1845, PD)", True, t)
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
        src_im = scan_cache[arch_id]
        cue_active = draw_anchored_cues(im, d, abs_t, row["t_s"], row["t_end_s"], cues, portrait_cache, show_portrait=True)
        cx = 640 if rid == "04b_arch_mendel_1866_paper" else (W // 2 + int(24 * math.sin(u * math.pi)))
        cy = H // 2 + 12 + int(14 * math.cos(u * math.pi))
        px, py, bw, bh = paste_doc_card(im, d, src_im, 720, 620, cx, cy, zoom=1.02 + 0.14 * ease(u))
        ring_p = prog(t, 0.35, min(dur - 0.3, 3.4))
        d.arc((px + bw // 2 - 220, py + bh // 2 - 115, px + bw // 2 + 220, py + bh // 2 + 115), 0, int(360 * ring_p), fill=GOLD, width=6)
        credit = (row.get("archive_source") or {}).get("description", "Public Domain Archive")[:52]
        draw_archive_credit_if_clear(d, credit, cue_active, t)
        return

    # 9. P3:03 Malthus curve split into beat1 (steep birth curve) and beat2 (flat food limit + survival gap)
    if rid.startswith("03_cg_malthus_curve_beat"):
        cue_active = draw_anchored_cues(im, d, abs_t, row["t_s"], row["t_end_s"], cues, portrait_cache)
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
            d.line(exp_pts, fill=CRIMSON, width=8)
            if not cue_active:
                d.text((exp_pts[-1][0] - 280, max(225, exp_pts[-1][1] - 54)), "OFFSPRING BORN", font=fnt(40, italic=True), fill=GOLD)
        else:
            exp_pts = [
                (int(ox + gw * (k / 80.0)), int(oy - 55 - (gh - 95) * ((math.exp(2.8 * (k / 80.0)) - 1.0) / (math.exp(2.8) - 1.0))))
                for k in range(81)
            ]
            d.line(exp_pts, fill=CRIMSON, width=8)
            p_f = prog(t, 0.12, dur * 0.72)
            n_f = max(2, int(80 * p_f))
            lin_pts = [(int(ox + gw * (k / 80.0)), int(oy - 145 - 85 * (k / 80.0))) for k in range(n_f + 1)]
            d.line(lin_pts, fill=TEAL, width=7)
            for k in range(10, n_f, 8):
                d.line((exp_pts[k][0], exp_pts[k][1] + 10, lin_pts[k][0], lin_pts[k][1] - 10), fill=GOLD, width=3)
            if not cue_active:
                d.text((lin_pts[-1][0] - 250, lin_pts[-1][1] + 24), "FOOD SUPPLY", font=fnt(40, italic=True), fill=TEAL)
        return

    # 10. P3:06 natural selection sieve split into beat1 (sieve filtering) and beat2 (deep beak selected)
    if rid.startswith("06_nature_keeps_fit_beat"):
        cue_active = draw_anchored_cues(im, d, abs_t, row["t_s"], row["t_end_s"], cues, portrait_cache)
        sieve_y = 560
        d.rounded_rectangle((210, 195, 1710, 885), radius=30, fill=(52, 42, 32), outline=GOLD, width=4)
        for k in range(13):
            sx = 310 + k * 108
            d.ellipse((sx - 28, sieve_y - 20, sx + 28, sieve_y + 20), fill=TAN, outline=CREAM, width=3)
        if rid.endswith("_beat1"):
            p_fall = prog(t, 0.15, dur * 0.82)
            profiles = [(520, 18, PALE, False), (960, 32, CREAM, False), (1400, 58, GOLD, True)]
            for cx, depth, col, passes in profiles:
                max_y = 765 if passes else sieve_y - 62
                cy = int(285 + (max_y - 285) * p_fall)
                d.polygon([(cx - 80, cy - depth), (cx + 105, cy), (cx - 80, cy + depth)], fill=col, outline=WHITE)
            if not cue_active:
                d.text((760, 805), "ONES THAT FIT", font=fnt(42, italic=True), fill=GOLD)
        else:
            # Beat 2: zoomed survival focus on the deep gold beak below the hard-seed barrier
            cx, cy = 960, 690
            r_glow = int(165 + 25 * math.sin(u * math.pi))
            d.ellipse((cx - r_glow, cy - 110, cx + r_glow, cy + 110), outline=GOLD, width=4)
            d.polygon([(cx - 130, cy - 78), (cx + 165, cy), (cx - 130, cy + 78)], fill=GOLD, outline=CREAM)
            if not cue_active:
                d.text((cx - 185, 290), "DEEP BEAK SURVIVES", font=fnt(44, italic=True), fill=CREAM)
        return

    # 11. NEW v02 code_graphic: P3:09a_essay_1844_sealed
    if rid == "09a_essay_1844_sealed":
        cue_active = draw_anchored_cues(im, d, abs_t, row["t_s"], row["t_end_s"], cues, portrait_cache, show_portrait=False)
        # Left: 230-page fair-copy manuscript stack bound with crimson ribbon + wax seal
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
        # Right: timeline step 4/7 (1835 · 1837 · 1838 · [1844])
        d.rounded_rectangle((960, 280, 1740, 770), radius=28, fill=(52, 42, 32), outline=GOLD, width=4)
        years = ["1835", "1837", "1838", "1844"]
        tl_p = prog(t, 0.25, dur * 0.75)
        d.line((1040, 525, 1040 + int(600 * tl_p), 525), fill=GOLD, width=6)
        for idx, yr in enumerate(years):
            dx = 1040 + idx * 200
            if tl_p >= idx / 3.2:
                active = yr == "1844"
                d.ellipse((dx - 16, 509, dx + 16, 541), fill=GOLD if active else CREAM, outline=GOLD, width=4)
                if active and not cue_active:
                    d.text((dx - 52, 435), "1844", font=fnt(44, italic=True), fill=GOLD)
        return

    # 12. P3:12 barnacle counter
    if rid == "12_cg_barnacle_counter":
        cue_active = draw_anchored_cues(im, d, abs_t, row["t_s"], row["t_end_s"], cues, portrait_cache)
        p_cnt = prog(t, 0.18, dur * 0.80)
        yr = 1846 + int(round(8 * p_cnt))
        yrs_done = int(round(8 * p_cnt))
        cx, cy = 590, 545
        d.rounded_rectangle((cx - 300, cy - 185, cx + 300, cy + 185), radius=36, fill=(54, 44, 34), outline=GOLD, width=5)
        d.text((cx - 195, cy - 115), f"{yr}", font=fnt(124, italic=True), fill=GOLD)
        if not cue_active:
            d.text((cx - 180, cy + 52), f"{yrs_done} OF 8 YEARS", font=fnt(42, italic=True), fill=CREAM)
        for v in range(4):
            vp = prog(p_cnt, v * 0.20, (v + 1) * 0.24)
            if vp > 0:
                vx = 1040 + v * 165
                vy = int(745 - 360 * vp)
                d.rounded_rectangle((vx, vy, vx + 132, 745), radius=14, fill=(68, 94, 84), outline=GOLD, width=4)
                d.line((vx + 24, vy + 55, vx + 108, vy + 55), fill=GOLD, width=4)
        return

    # 13. P4:05 Wallace counter split into beat1 (Malay islands map) and beat2 (0 -> 125,660 specimen counter)
    if rid.startswith("05_cg_wallace_counter_beat"):
        cue_active = draw_anchored_cues(im, d, abs_t, row["t_s"], row["t_end_s"], cues, portrait_cache)
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
                d.text((280, 260), "MALAY ARCHIPELAGO · 1854", font=fnt(44, italic=True), fill=CREAM)
        else:
            p_cnt = prog(t, 0.10, dur * 0.78)
            count_val = int(round(125660 * p_cnt))
            d.rounded_rectangle((960, 245, 1660, 465), radius=28, fill=(54, 44, 34), outline=GOLD, width=5)
            d.text((1015, 275), f"{count_val:,}", font=fnt(108, italic=True), fill=GOLD)
            if not cue_active:
                d.text((1020, 398), "SPECIMENS · 1854–1862", font=fnt(34, italic=True), fill=CREAM)
        return

    # 14. NEW v02 code_graphic: P4:07b_packet_to_mailbag
    if rid == "07b_packet_to_mailbag":
        cue_active = draw_anchored_cues(im, d, abs_t, row["t_s"], row["t_end_s"], cues, portrait_cache)
        d.rounded_rectangle((190, 200, 1730, 880), radius=34, fill=(40, 58, 72), outline=GOLD, width=5)
        # Stylised Old World coastline silhouette arcs (Europe -> Suez/Cape -> Malay Archipelago)
        d.polygon([(340, 310), (540, 290), (620, 410), (470, 430)], fill=(82, 102, 78), outline=TAN, width=3)
        d.polygon([(580, 450), (860, 470), (820, 740), (640, 710)], fill=(88, 104, 76), outline=TAN, width=3)
        d.polygon([(920, 360), (1380, 380), (1460, 580), (1080, 560)], fill=(82, 102, 78), outline=TAN, width=3)
        d.polygon([(1420, 620), (1600, 610), (1630, 705), (1440, 695)], fill=(92, 112, 82), outline=GOLD, width=3)
        ternate = (1525, 655)
        down_house = (435, 355)
        d.ellipse((ternate[0] - 12, ternate[1] - 12, ternate[0] + 12, ternate[1] + 12), fill=GOLD, outline=CREAM, width=3)
        d.ellipse((down_house[0] - 12, down_house[1] - 12, down_house[0] + 12, down_house[1] + 12), fill=CREAM, outline=GOLD, width=3)
        p_route = prog(t, 0.12, dur * 0.84)
        pts = []
        for k in range(max(2, int(60 * p_route)) + 1):
            s = k / 60.0
            px = int((1 - s) * ternate[0] + s * down_house[0])
            py = int((1 - s) * ternate[1] + s * down_house[1] + 155 * math.sin(s * math.pi))
            pts.append((px, py))
        if len(pts) >= 2:
            d.line(pts, fill=GOLD, width=6)
            ex, ey = pts[-1]
            # Travelling wax-sealed packet icon
            d.rounded_rectangle((ex - 46, ey - 30, ex + 46, ey + 30), radius=8, fill=CREAM, outline=GOLD, width=3)
            d.line((ex - 42, ey - 26, ex, ey + 4), fill=TAN, width=3)
            d.line((ex + 42, ey - 26, ex, ey + 4), fill=TAN, width=3)
            d.ellipse((ex - 11, ey - 8, ex + 11, ey + 14), fill=CRIMSON, outline=GOLD, width=2)
        if not cue_active:
            d.text((260, 785), "TERNATE → DOWN HOUSE · 18 JUNE 1858", font=fnt(40, italic=True), fill=CREAM)
        return

    # 15. NEW v02 free_archive: P5:02b_joint_papers_lectern (_wide and _detail)
    if rid.startswith("02b_joint_papers_lectern_"):
        cue_active = draw_anchored_cues(im, d, abs_t, row["t_s"], row["t_end_s"], cues, portrait_cache, show_portrait=False)
        hooker = portrait_cache["who_joseph_hooker"]
        if rid.endswith("_wide"):
            # Wide Linnean lectern dossier: Darwin 1844 extract + Wallace 1858 essay + Hooker portrait medallion
            d.rounded_rectangle((190, 210, 1260, 860), radius=32, fill=(56, 44, 34), outline=GOLD, width=5)
            p_in = prog(t, 0.10, dur * 0.70)
            # Left paper bundle (Darwin 1844)
            d.rounded_rectangle((260, 300, 690, 780), radius=16, fill=CREAM, outline=TAN, width=4)
            for ln in range(8):
                d.line((305, 390 + ln * 42, 640, 390 + ln * 42), fill=CLAY, width=4)
            # Right paper bundle (Wallace 1858)
            d.rounded_rectangle((750, 300, 1180, 780), radius=16, fill=(240, 224, 192), outline=GOLD, width=4)
            for ln in range(8):
                d.line((795, 390 + ln * 42, 1130, 390 + ln * 42), fill=CLAY, width=4)
            # Crimson ribbon tying both together
            rib_w = int(920 * p_in)
            if rib_w > 20:
                d.rectangle((260, 535, 260 + rib_w, 558), fill=CRIMSON, outline=GOLD, width=2)
            im.paste(hooker, (1360, 240 + int(10 * math.sin(u * math.pi))), hooker)
            if not cue_active:
                d.text((1320, 625), "1 JULY 1858 · LONDON", font=fnt(38, italic=True), fill=GOLD)
        else:
            # Detail zoom on Hooker daguerreotype + twin dated priority folios
            paste_doc_card(im, d, scan_cache["who_joseph_hooker_raw"], 520, 620, 520, 540, zoom=1.06 + 0.12 * ease(u), focus_xy=(0.5, 0.35))
            d.rounded_rectangle((880, 250, 1730, 515), radius=24, fill=(242, 226, 194), outline=GOLD, width=4)
            d.rounded_rectangle((880, 565, 1730, 830), radius=24, fill=(236, 218, 184), outline=CREAM, width=4)
            for base_y in (350, 665):
                for ln in range(3):
                    d.line((930, base_y + ln * 42, 1660, base_y + ln * 42), fill=CLAY, width=4)
            hl = int(680 * prog(t, 0.2, dur * 0.75))
            d.line((930, 315, 930 + hl, 315), fill=GOLD, width=6)
            if not cue_active:
                d.text((930, 268), "1844 SKETCH + 1858 ESSAY", font=fnt(38, italic=True), fill=DARK_INK)
        draw_archive_credit_if_clear(d, "Joseph Hooker · Kilburn daguerreotype (c. 1852, PD)", True if not cue_active else cue_active, t)
        return

    # 16. NEW v02 code_graphic: P5:04b_bell_report_1859
    if rid == "04b_bell_report_1859":
        cue_active = draw_anchored_cues(im, d, abs_t, row["t_s"], row["t_end_s"], cues, portrait_cache)
        # Inked period presidential report page on mahogany lectern
        px, py, bw, bh = 460, 185, 1000, 720
        d.rounded_rectangle((px - 22, py - 22, px + bw + 22, py + bh + 22), radius=28, fill=(52, 42, 32), outline=GOLD, width=5)
        d.rounded_rectangle((px, py, px + bw, py + bh), radius=16, fill=(242, 228, 198), outline=TAN, width=3)
        # Engraved typographic rule lines representing the presidential address page
        d.line((px + 120, py + 115, px + bw - 120, py + 115), fill=DARK_INK, width=4)
        for ln in range(9):
            yy = py + 185 + ln * 52
            col = CRIMSON if ln == 5 else (128, 108, 86)
            d.line((px + 110, yy, px + bw - 110, yy), fill=col, width=5 if ln == 5 else 3)
        # Animated candle-gold & crimson underline drawing under the key line
        ul_p = prog(t, 0.35, dur * 0.80)
        ul_w = int((bw - 220) * ul_p)
        if ul_w > 12:
            d.line((px + 110, py + 185 + 5 * 52 + 14, px + 110 + ul_w, py + 185 + 5 * 52 + 14), fill=GOLD, width=8)
        if not cue_active:
            d.text((px + 250, py + 48), "MAY 1859 · ANNUAL REPORT", font=fnt(38, italic=True), fill=DARK_INK)
        return

    # 17. P5:07 timeline origin
    if rid == "07_cg_timeline_origin":
        cue_active = draw_anchored_cues(im, d, abs_t, row["t_s"], row["t_end_s"], cues, portrait_cache)
        dates = ["1835", "1837", "1838", "1844", "1858", "1859", "1889"]
        p_tl = prog(t, 0.12, dur * 0.78)
        d.rounded_rectangle((140, 250, 1780, 860), radius=32, fill=(52, 42, 32), outline=GOLD, width=4)
        x0, x1, yy = 220, 1700, 500
        cur_x = int(x0 + (x1 - x0) * p_tl)
        d.line((x0, yy, cur_x, yy), fill=GOLD, width=7)
        for idx, yr in enumerate(dates):
            dx = x0 + int((x1 - x0) * (idx / (len(dates) - 1)))
            if cur_x >= dx - 5:
                d.ellipse((dx - 15, yy - 15, dx + 15, yy + 15), fill=GOLD if yr == "1859" else CREAM, outline=GOLD, width=4)
                y_off = -85 if idx % 2 == 0 else 42
                d.text((dx - 44, yy + y_off), yr, font=fnt(36, italic=True), fill=GOLD if yr == "1859" else CREAM)
        # Green cloth octavo book stacks rising at bottom
        n_b = max(1, int(10 * p_tl))
        for b in range(n_b):
            bx = 520 + b * 88
            d.rounded_rectangle((bx, 680, bx + 68, 810), radius=8, fill=(64, 98, 76), outline=GOLD, width=3)
        if not cue_active:
            cnt = int(round(1250 * p_tl))
            d.text((660, 615), f"{cnt:,} COPIES ORDERED", font=fnt(42, italic=True), fill=CREAM)
        return

    # 18. P6:03 blending beaks split into beat1 (1 -> 1/2 -> 1/4) and beat2 (1/4 -> 1/8 grey wash)
    if rid.startswith("03_cg_blending_beaks_beat"):
        cue_active = draw_anchored_cues(im, d, abs_t, row["t_s"], row["t_end_s"], cues, portrait_cache)
        d.rounded_rectangle((180, 210, 1740, 870), radius=32, fill=(52, 42, 32), outline=GOLD, width=4)
        if rid.endswith("_beat1"):
            gens = [
                ("1", 400, 68, (226, 184, 102)),
                ("1/2", 960, 44, (196, 166, 118)),
                ("1/4", 1520, 28, (164, 148, 130)),
            ]
            for idx, (frac, cx, depth, col) in enumerate(gens):
                s = prog(t, 0.2 + idx * 1.6, 1.9 + idx * 1.6)
                if s > 0:
                    cy, blen = 560, int(185 * s)
                    d.polygon([(cx - 85, cy - depth), (cx - 85 + blen, cy), (cx - 85, cy + depth)], fill=col, outline=CREAM)
                    d.text((cx - 55, cy - 165), frac, font=fnt(72, italic=True), fill=col)
            if not cue_active:
                d.text((710, 765), "HALVED EACH GENERATION", font=fnt(40, italic=True), fill=CREAM)
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
                    cy, blen = 560, int(165 * s)
                    wcol = tuple(int(c * (1.0 - 0.35 * fade_wash) + 128 * (0.35 * fade_wash)) for c in col)
                    d.polygon([(cx - 75, cy - depth), (cx - 75 + blen, cy), (cx - 75, cy + depth)], fill=wcol, outline=CREAM)
                    d.text((cx - 50, cy - 155), frac, font=fnt(64, italic=True), fill=wcol)
            if not cue_active:
                d.text((740, 765), "DILUTED TO GREY", font=fnt(42, italic=True), fill=PALE)
        return

    raise RuntimeError(f"Unhandled free row id: {rid}")


_G_BASE: np.ndarray | None = None
_G_SCANS: dict[str, Image.Image] = {}
_G_PORTRAITS: dict[str, Image.Image] = {}


def _init_worker(arch_items: list[dict]) -> None:
    global _G_BASE, _G_SCANS, _G_PORTRAITS
    _G_BASE = make_base_canvas(1303)
    _G_SCANS = {}
    _G_PORTRAITS = {}
    for item in arch_items:
        p = Path(item["nas_raw"])
        im = Image.open(p).convert("RGB")
        if item["kind"] == "scan":
            _G_SCANS[item["id"]] = im
        else:
            _G_PORTRAITS[item["id"]] = make_oval_portrait(im, 340)
            if item["id"] == "who_joseph_hooker":
                _G_SCANS["who_joseph_hooker_raw"] = im


def _render_single_row(task: tuple[int, dict, list[dict]]) -> dict:
    idx, row, row_cues = task
    assert _G_BASE is not None
    pnum = int(row["part"])
    rid = row["id"]
    dur = round(float(row["t_end_s"]) - float(row["t_s"]), 2)
    n_frames = max(15, int(round(dur * FPS)))
    hero_idx = n_frames // 2

    cg_name = f"code_graphic_013_v03f_p{pnum}_{rid}.mp4"
    still_name = f"code_graphic_013_v03f_p{pnum}_{rid}.jpg"
    mp4_path = NAS_OUT_DIR / cg_name
    still_path = NAS_OUT_DIR / still_name

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
            frame_arr = np.roll(_G_BASE, shift_x, axis=1).copy()
            im = Image.fromarray(frame_arr, "RGB")
            d = ImageDraw.Draw(im)
            render_row_frame(im, d, row, t, dur, row_cues, _G_SCANS, _G_PORTRAITS)
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
        "sha256_mp4": digest(mp4_path),
        "sha256_still": digest(still_path),
        "spend": "£0",
    }


def build_all() -> None:
    NAS_OUT_DIR.mkdir(parents=True, exist_ok=True)
    GIT_OUT_DIR.mkdir(parents=True, exist_ok=True)

    arch_items = json.loads((EDIT / "archive_pulls_v01/ARCHIVE_PULLS_RAW_v01.json").read_text())
    for item in arch_items:
        nas_p = Path(item["nas_raw"])
        assert nas_p.exists(), f"Missing NAS raw archive file: {nas_p}"
        assert digest(nas_p) == item["sha256"], f"SHA-256 mismatch on {nas_p}"

    plan = json.loads((EDIT / "PICTURE_PLAN_v03f.json").read_text())
    all_cues = [c for c in plan["overlay_cues"] if c.get("status") == "ANCHORED"]
    free_rows = [r for r in plan["rows"] if r["source_kind"] in ("code_graphic", "free_archive")]
    assert len(free_rows) == 35, f"Expected 35 free rows in PICTURE_PLAN_v03f.json, got {len(free_rows)}"

    tasks = []
    for idx, r in enumerate(free_rows):
        overlapping_cues = [
            c for c in all_cues
            if max(float(r["t_s"]), float(c["display_start_s"])) < min(float(r["t_end_s"]), float(c["display_end_s"]))
        ]
        tasks.append((idx, r, overlapping_cues))

    print(f"Rendering {len(tasks)} v03f £0 free clips at {W}x{H}@{FPS}fps across 4 workers...", flush=True)
    rendered_rows: list[dict] = []
    with ProcessPoolExecutor(max_workers=4, initializer=_init_worker, initargs=(arch_items,)) as ex:
        for rec in ex.map(_render_single_row, tasks):
            rendered_rows.append(rec)
            print(
                f"[{rec['idx']+1:02d}/{len(tasks):02d}] {rec['id']:38s} -> {rec['encoded_s']:4.2f}s "
                f"mean={rec['min_sample_mean_luma']} std={rec['min_sample_std']} {rec['near_black']}",
                flush=True,
            )

    rendered_rows.sort(key=lambda x: x["idx"])
    for rec in rendered_rows:
        assert rec["near_black"] == "PASS", f"Near-black failed on {rec['id']}"

    # Build 390px phone readability sheet of all 35 v03f graphics (4 cols x 9 rows, exact 390x219 thumbnails)
    cols, tw, th = 4, 390, 219
    rows_n = math.ceil(len(rendered_rows) / cols)
    sheet_im = Image.new("RGB", (cols * tw, rows_n * (th + 42)), (28, 34, 44))
    sd = ImageDraw.Draw(sheet_im)
    sfont = fnt(18, italic=True)
    for i, rec in enumerate(rendered_rows):
        st = Image.open(NAS_OUT_DIR / rec["still"]).resize((tw, th), Image.Resampling.LANCZOS)
        x, y = (i % cols) * tw, (i // cols) * (th + 42)
        sheet_im.paste(st, (x, y))
        sd.text((x + 6, y + th + 4), f"{rec['id'][:30]} ({rec['t_s']:.2f}-{rec['t_end_s']:.2f}s)", fill=CREAM, font=sfont)
    sheet_path = GIT_OUT_DIR / "CONTACT_SHEET_v03f_390px.jpg"
    sheet_im.save(sheet_path, quality=90)
    shutil.copy2(sheet_path, NAS_OUT_DIR / sheet_path.name)

    # Build QA reel on NAS and run polish_gate.py + picture_qa.py
    cuts = []
    pool = []
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
        pool.append({
            "file_id": rec["file"],
            "title": f"own code graphic {rec['id']}",
        })
        cur_t += dur

    concat_txt = NAS_OUT_DIR / "concat_list_v03f.txt"
    concat_txt.write_text("".join(f"file '{NAS_OUT_DIR / rec['file']}'\n" for rec in rendered_rows))
    reel_mp4 = NAS_OUT_DIR / "code_graphics_013_reel_v03f.mp4"
    sp.run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", str(concat_txt), "-c", "copy", str(reel_mp4)], check=True)

    (GIT_OUT_DIR / "cuts_v03f_cg.json").write_text(json.dumps(cuts, indent=2) + "\n")
    (GIT_OUT_DIR / "pool_v03f_cg.json").write_text(json.dumps(pool, indent=2) + "\n")

    pg_json = GIT_OUT_DIR / "polish_gate_v03f.json"
    pg_res = sp.run([
        "python3", str(OWB_ROOT / "scripts/polish_gate.py"),
        str(reel_mp4),
        "--cuts", str(GIT_OUT_DIR / "cuts_v03f_cg.json"),
        "--out", str(pg_json),
        "--no-jitter",
    ], capture_output=True, text=True, check=True)
    (GIT_OUT_DIR / "polish_gate_v03f.txt").write_text(pg_res.stdout)
    print(pg_res.stdout, end="")

    pqa_dir = GIT_OUT_DIR / "picture_qa_v03f"
    pqa_dir.mkdir(parents=True, exist_ok=True)
    pqa_res = sp.run([
        "python3", str(OWB_ROOT / "scripts/picture_qa.py"),
        str(reel_mp4),
        "--cuts", str(GIT_OUT_DIR / "cuts_v03f_cg.json"),
        "--pool", str(GIT_OUT_DIR / "pool_v03f_cg.json"),
        "--out-dir", str(pqa_dir),
        "--no-jitter",
    ], capture_output=True, text=True, check=True)
    (GIT_OUT_DIR / "picture_qa_v03f.txt").write_text(pqa_res.stdout)
    print(pqa_res.stdout, end="")

    manifest = {
        "film": "013_Darwin-Wallace-Evolution",
        "version": "v03f",
        "task": "J2652",
        "plan_sha256": digest(EDIT / "PICTURE_PLAN_v03f.json"),
        "spend": "£0",
        "credits_spent": 0,
        "fps": FPS,
        "resolution": f"{W}x{H}",
        "rendered_clips_count": len(rendered_rows),
        "reel_nas_path": str(reel_mp4),
        "reel_sha256": digest(reel_mp4),
        "contact_sheet_390px": str(sheet_path.relative_to(EDIT)),
        "rendered_clips": rendered_rows,
    }
    (GIT_OUT_DIR / "CODE_GRAPHICS_v03f.json").write_text(json.dumps(manifest, indent=2) + "\n")
    for fn in ("cuts_v03f_cg.json", "pool_v03f_cg.json", "CODE_GRAPHICS_v03f.json", "polish_gate_v03f.json", "polish_gate_v03f.txt", "picture_qa_v03f.txt"):
        shutil.copy2(GIT_OUT_DIR / fn, NAS_OUT_DIR / fn)
    print("ALL 35 V03F FREE GRAPHICS BUILT & QA PASSED", flush=True)


if __name__ == "__main__":
    build_all()
