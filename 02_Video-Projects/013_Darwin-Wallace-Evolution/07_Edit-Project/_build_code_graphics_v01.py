#!/usr/bin/env python3
"""J2476: Build all £0 picture assets for HOS 013 Darwin & Wallace:
- 10 framed WHO portrait overlays from public-domain Wikimedia Commons portraits
- 22 rendered 1920x1080 30fps H.264 .mp4 clips + .jpg hero stills (16 code graphics/maps/diagrams/cards + 6 archive composites)
- Concatenated QA reel on NAS scratch + cuts_v01.json + pool_v01.json
- Runs picture_qa.py and polish_gate.py and writes picture_qa_v01.txt + polish_gate_v01.txt + CODE_GRAPHICS_v01.json + CONTACT_SHEET.jpg
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

W, H, FPS = 1920, 1080, 30
FONT = "/System/Library/Fonts/Supplemental/Didot.ttc"
EDIT = Path(__file__).resolve().parent
FILM = EDIT.parent
HOS_ROOT = FILM.parents[1]
OWB_ROOT = Path("/Users/benjaminoats/YouTube/orbit-with-ben")
NAS_EDIT = Path("/Volumes/data/studio-live/History Of Science/02_Video-Projects/013_Darwin-Wallace-Evolution/07_Edit-Project")
RAW_DIR = EDIT / "archive_pulls_v01/raw"
OUT_DIR = EDIT / "code_graphics_v01"

CREAM = (244, 228, 195)
GOLD = (218, 176, 98)
PALE = (202, 182, 152)
TAN = (156, 128, 98)
CLAY = (118, 90, 70)
WHITE = (240, 236, 224)
TEAL = (116, 178, 186)
CRIMSON = (196, 86, 78)
GREEN = (124, 176, 112)


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


def make_base_canvas(seed: int = 1301) -> np.ndarray:
    """Warm lifted study/parchment desk background with rich organic detail (std > 24, mean > 48, no straight seams)."""
    y, x = np.mgrid[:H, :W].astype(np.float32)
    nx = (x - W * 0.5) / (W * 0.5)
    ny = (y - H * 0.5) / (H * 0.5)
    r2 = nx * nx * 0.85 + ny * ny * 1.05
    vignette = np.clip(1.0 - 0.58 * r2, 0.25, 1.0)

    # Organic swirling parchment / mahogany wave texture so every column and row has natural variance
    wave1 = np.sin(nx * 5.2 + ny * 2.1) * 9.0 + np.cos(ny * 6.7 - nx * 3.4) * 7.5
    wave2 = np.sin((nx * nx + ny * ny) * 9.5) * 6.0
    rng = np.random.default_rng(seed)
    grain = rng.normal(0.0, 2.2, (H, W)).astype(np.float32)

    base = np.zeros((H, W, 3), np.float32)
    # Warm mahogany-slate center lifting to rich amber-parchment tones
    c_dark = np.array([28.0, 36.0, 48.0], np.float32)
    c_light = np.array([76.0, 66.0, 54.0], np.float32)
    for c in range(3):
        base[:, :, c] = c_dark[c] + (c_light[c] - c_dark[c]) * vignette + wave1 + wave2 + grain

    # Add subtle curved botanical specimen arcs in the corners so edge density and std are high everywhere
    im = Image.fromarray(np.uint8(np.clip(base, 0, 255)), "RGB")
    d = ImageDraw.Draw(im)
    for k in range(6):
        rad = 180 + k * 55
        d.arc((-rad, -rad, rad * 2, rad * 2), 15, 78, fill=(98, 84, 66), width=2)
        d.arc((W - rad * 2, H - rad * 2, W + rad, H + rad), 195, 258, fill=(98, 84, 66), width=2)
        d.arc((W - rad * 2, -rad, W + rad, rad * 2), 102, 165, fill=(92, 78, 62), width=2)
        d.arc((-rad, H - rad * 2, rad * 2, H + rad), 282, 345, fill=(92, 78, 62), width=2)

    # Subtle compass rose medallions in left and right background margins
    for cx, cy in ((210, 240), (1710, 840), (210, 840), (1710, 240)):
        for r in (42, 68, 94):
            d.ellipse((cx - r, cy - r, cx + r, cy + r), outline=(104, 88, 68), width=2)
        for ang_deg in range(0, 360, 30):
            ang = math.radians(ang_deg)
            x1 = cx + int(36 * math.cos(ang))
            y1 = cy + int(36 * math.sin(ang))
            x2 = cx + int(98 * math.cos(ang))
            y2 = cy + int(98 * math.sin(ang))
            d.line((x1, y1, x2, y2), fill=(96, 82, 64), width=2)

    return np.asarray(im, dtype=np.uint8)


def build_who_overlays() -> list[dict]:
    """Build 10 framed circular/oval cut-out WHO portrait overlays from raw public-domain files."""
    who_dir = OUT_DIR / "who_overlays"
    who_dir.mkdir(parents=True, exist_ok=True)
    meta_list = json.loads((EDIT / "archive_pulls_v01/ARCHIVE_PULLS_RAW_v01.json").read_text())
    out_records = []
    for item in meta_list:
        if item["kind"] != "portrait":
            continue
        src = FILM / item["local_raw"]
        im = Image.open(src).convert("RGB")
        # Center-crop square and frame in warm brass/cream medallion on transparent RGBA
        w, h = im.size
        s = min(w, h)
        left = (w - s) // 2
        top = max(0, (h - s) // 3)
        im_sq = im.crop((left, top, left + s, top + s)).resize((360, 360), Image.Resampling.LANCZOS)

        canvas = Image.new("RGBA", (400, 400), (0, 0, 0, 0))
        mask = Image.new("L", (360, 360), 0)
        ImageDraw.Draw(mask).ellipse((4, 4, 356, 356), fill=255)
        canvas.paste(im_sq, (20, 20), mask)

        d = ImageDraw.Draw(canvas)
        d.ellipse((16, 16, 384, 384), outline=(218, 176, 98, 255), width=6)
        d.ellipse((24, 24, 376, 376), outline=(244, 228, 195, 220), width=2)

        out_png = who_dir / f"{item['id']}_overlay.png"
        canvas.save(out_png)
        if NAS_EDIT.exists():
            nas_who = NAS_EDIT / "code_graphics_v01/who_overlays"
            nas_who.mkdir(parents=True, exist_ok=True)
            shutil.copy2(out_png, nas_who / out_png.name)
        out_records.append({
            "id": item["id"],
            "description": item["description"],
            "overlay_png": f"07_Edit-Project/code_graphics_v01/who_overlays/{out_png.name}",
            "source_raw": item["local_raw"],
            "licence": item["licence"],
            "sha256": digest(out_png),
        })
    return out_records


def draw_side_label(d: ImageDraw.ImageDraw, text: str | None, t: float, dur: float) -> None:
    """Draw house white Didot italic label (<= 4 words, fades in/out over 0.4s, holds <= 3.8s)."""
    if not text:
        return
    t0 = 0.25
    t1 = min(dur - 0.20, t0 + 3.60)
    if t < t0 or t > t1:
        return
    a = min(prog(t, t0, t0 + 0.35), prog(t1, t, t1 - 0.35))
    if a <= 0.02:
        return
    font = fnt(54, italic=True)
    c = tuple(int(v * a + 40 * (1 - a)) for v in WHITE)
    d.text((130, 88), text, font=font, fill=c)
    # Underline flourish
    bbox = d.textbbox((130, 88), text, font=font)
    w_line = int((bbox[2] - bbox[0]) * prog(t, t0, t0 + 0.55))
    if w_line > 8:
        d.arc((130, bbox[3] + 6, 130 + w_line, bbox[3] + 22), 180, 360, fill=GOLD, width=3)


def draw_archive_credit(d: ImageDraw.ImageDraw, credit: str, t: float, dur: float, has_label: bool) -> None:
    """Corner credit line in white Didot italic bottom-left; waits until side_label finishes (one label at a time)."""
    t_start = 3.90 if (has_label and dur > 4.4) else 0.30
    if t < t_start:
        return
    font = fnt(28, italic=True)
    d.text((110, H - 78), credit, font=font, fill=PALE)


def render_frame_content(
    im: Image.Image,
    d: ImageDraw.ImageDraw,
    rid: str,
    pnum: int,
    t: float,
    dur: float,
    side_label: str | None,
    teach: dict | None,
    arch_id: str | None,
    arch_cache: dict[str, Image.Image],
) -> None:
    u = t / max(dur, 0.01)

    # 1. Chapter cards
    if rid.startswith("01_card_p"):
        ch_num = {2: "II", 3: "III", 4: "IV", 5: "V", 6: "VI"}[pnum]
        title = (teach or {}).get("title", "")
        p_in = prog(t, 0.0, 0.45)
        # Draw ornate curved parchment cartouche (rounded arcs, never full-frame straight seams)
        cx, cy = W // 2, H // 2
        rx = int(580 + 40 * p_in)
        ry = int(230 + 15 * p_in)
        d.rounded_rectangle((cx - rx, cy - ry, cx + rx, cy + ry), radius=48, fill=(58, 48, 38), outline=GOLD, width=4)
        d.rounded_rectangle((cx - rx + 18, cy - ry + 18, cx + rx - 18, cy + ry - 18), radius=38, outline=CREAM, width=2)
        f_num = fnt(52, italic=True)
        f_tit = fnt(68, italic=True)
        b1 = d.textbbox((0, 0), f"Part {ch_num}", font=f_num)
        d.text((cx - (b1[2] - b1[0]) // 2, cy - 95), f"Part {ch_num}", font=f_num, fill=GOLD)
        b2 = d.textbbox((0, 0), title, font=f_tit)
        d.text((cx - (b2[2] - b2[0]) // 2, cy - 8), title, font=f_tit, fill=CREAM)
        # Animated compass needle sweep below title
        ang = -0.6 + 1.2 * u
        nx = cx + int(140 * math.cos(ang))
        ny = cy + 115 + int(28 * math.sin(ang))
        d.line((cx - 140, cy + 115, nx, ny), fill=GOLD, width=4)
        d.ellipse((cx - 8, cy + 107, cx + 8, cy + 123), fill=CREAM)
        return

    # 2. End card
    if rid == "09_cream_end_card":
        cx, cy = W // 2, H // 2
        for k in range(10):
            r = int(120 + k * 42 + 18 * math.sin(u * math.pi + k * 0.5))
            d.ellipse((cx - r, cy - int(r * 0.62), cx + r, cy + int(r * 0.62)), outline=GOLD if k % 2 == 0 else TAN, width=3)
        # Branching tree motif in center
        branches = [
            ((cx, cy + 160), (cx, cy + 30)),
            ((cx, cy + 30), (cx - 110, cy - 60)),
            ((cx, cy + 30), (cx + 110, cy - 60)),
            ((cx - 110, cy - 60), (cx - 170, cy - 145)),
            ((cx - 110, cy - 60), (cx - 55, cy - 150)),
            ((cx + 110, cy - 60), (cx + 55, cy - 150)),
            ((cx + 110, cy - 60), (cx + 170, cy - 145)),
        ]
        for (x0, y0), (x1, y1) in branches:
            d.line((x0, y0, x1, y1), fill=CREAM, width=5)
            d.ellipse((x1 - 7, y1 - 7, x1 + 7, y1 + 7), fill=GOLD)
        return

    # 3. Archive composites (ARCH)
    if arch_id and rid in (
        "12a_arch_notebook_tree_zoom",
        "10a_arch_vestiges_1844",
        "06b_arch_malthus_1798",
        "05b_arch_origin_1859_title",
        "09_arch_darwinism_1889",
        "04b_arch_mendel_1866_paper",
    ):
        src_im = arch_cache[arch_id]
        # Smooth 2.5D zoom + pan on angled parchment card over desk
        zoom = 1.0 + 0.12 * ease(u)
        pan_x = int(28 * math.sin(u * math.pi))
        pan_y = int(18 * math.cos(u * math.pi))
        tw = int(760 * zoom)
        th = int(580 * zoom)
        doc_resized = src_im.resize((tw, th), Image.Resampling.LANCZOS)
        # Crop center 720x540
        cx0 = (tw - 720) // 2
        cy0 = (th - 540) // 2
        doc_crop = doc_resized.crop((cx0, cy0, cx0 + 720, cy0 + 540))

        px = (W - 720) // 2 + pan_x
        py = (H - 540) // 2 + 20 + pan_y
        # Rounded brass frame behind document
        d.rounded_rectangle((px - 22, py - 22, px + 742, py + 562), radius=28, fill=(52, 42, 34), outline=GOLD, width=5)
        im.paste(doc_crop, (px, py))

        # Animated gold ink callout ring / highlight trace over document
        ring_p = prog(t, 0.4, min(dur - 0.3, 3.2))
        rx = px + 360
        ry = py + 270
        d.arc((rx - 220, ry - 110, rx + 220, ry + 110), 0, int(360 * ring_p), fill=GOLD, width=6)

        draw_side_label(d, side_label, t, dur)
        credit = (teach or {}).get("credit", "Public Domain Archive")
        draw_archive_credit(d, credit, t, dur, bool(side_label))
        return

    # 4. Data & Explainer Code Graphics (CG)
    if rid == "08_cg_i_think_tree":
        # Left side: Darwin's 1837 Notebook B p. 36 scan + animated gold branching trace
        src_im = arch_cache["darwin_tree_1837"].resize((540, 660), Image.Resampling.LANCZOS)
        px = 180 + int(14 * math.sin(u * math.pi))
        py = 210
        d.rounded_rectangle((px - 16, py - 16, px + 556, py + 676), radius=24, fill=(54, 44, 34), outline=GOLD, width=4)
        im.paste(src_im, (px, py))

        # Animated branching tree on right + 20-year bar (1838 -> 1858)
        tree_p = prog(t, 0.3, 6.5)
        nodes = [
            ((1180, 620), (1180, 470), 0.0, 0.25),
            ((1180, 470), (1030, 350), 0.20, 0.50),
            ((1180, 470), (1330, 350), 0.25, 0.55),
            ((1030, 350), (950, 240), 0.45, 0.75),
            ((1030, 350), (1100, 235), 0.50, 0.80),
            ((1330, 350), (1250, 235), 0.55, 0.85),
            ((1330, 350), (1420, 240), 0.60, 0.90),
        ]
        for (x0, y0), (x1, y1), a0, a1 in nodes:
            s = prog(tree_p, a0, a1)
            if s > 0:
                xm = int(x0 + (x1 - x0) * s)
                ym = int(y0 + (y1 - y0) * s)
                d.line((x0, y0, xm, ym), fill=GOLD, width=6)
                if s >= 0.95:
                    d.ellipse((x1 - 9, y1 - 9, x1 + 9, y1 + 9), fill=CREAM, outline=GOLD, width=3)

        # 20-year secrecy bar (1838 -> 1858)
        bar_p = prog(t, 5.5, 13.5)
        bx0, by0, bw, bh = 880, 740, 780, 54
        d.rounded_rectangle((bx0, by0, bx0 + bw, by0 + bh), radius=18, fill=(46, 38, 30), outline=TAN, width=3)
        fill_w = int((bw - 8) * bar_p)
        if fill_w > 12:
            d.rounded_rectangle((bx0 + 4, by0 + 4, bx0 + 4 + fill_w, by0 + bh - 4), radius=14, fill=GOLD)
        yr = 1838 + int(round(20 * bar_p))
        d.text((bx0, by0 - 52), f"1838  →  {yr}   ({int(round(20 * bar_p))} YEARS)", font=fnt(40, italic=True), fill=CREAM)
        draw_side_label(d, side_label, t, dur)
        return

    if rid == "10_cg_globe_arc":
        # Inked world globe disc + sweeping arc from Malay Archipelago to Kent + 230p vs 20p stacks
        gx, gy, gr = 680, 560, 330
        d.ellipse((gx - gr, gy - gr, gx + gr, gy + gr), fill=(36, 52, 68), outline=GOLD, width=5)
        for lat in (-180, -90, 0, 90, 180):
            d.arc((gx - gr + 25, gy + lat - 55, gx + gr - 25, gy + lat + 55), 10, 170, fill=(78, 98, 116), width=2)
        # Kent pin & Malay pin
        kent = (gx - 110, gy - 145)
        malay = (gx + 185, gy + 65)
        d.ellipse((kent[0] - 10, kent[1] - 10, kent[0] + 10, kent[1] + 10), fill=CREAM, outline=GOLD, width=3)
        d.ellipse((malay[0] - 10, malay[1] - 10, malay[0] + 10, malay[1] + 10), fill=GOLD, outline=CREAM, width=3)
        arc_p = prog(t, 0.2, dur * 0.75)
        steps = max(2, int(45 * arc_p))
        pts = []
        for k in range(steps + 1):
            s = k / 45.0
            px = (1 - s) * malay[0] + s * kent[0]
            py = (1 - s) * malay[1] + s * kent[1] - 140 * math.sin(s * math.pi)
            pts.append((int(px), int(py)))
        if len(pts) >= 2:
            d.line(pts, fill=GOLD, width=6)

        # Right side: 230-page 1844 stack vs 20-page 1858 packet
        st_p = prog(t, 0.6, dur * 0.85)
        n_pages = max(1, int(18 * st_p))
        for k in range(n_pages):
            yy = 720 - k * 14
            d.rounded_rectangle((1190, yy - 12, 1420, yy), radius=4, fill=CREAM, outline=TAN, width=2)
        d.text((1205, 745), "1844 · 230p", font=fnt(34, italic=True), fill=CREAM)
        d.rounded_rectangle((1500, 695, 1710, 720), radius=4, fill=GOLD, outline=CREAM, width=2)
        d.text((1515, 745), "1858 · Packet", font=fnt(34, italic=True), fill=GOLD)
        draw_side_label(d, side_label, t, dur)
        return

    if rid == "06b_cg_tortoise_shells":
        # Left: Dome shell profile; Right: High saddle-backed arch profile
        p_draw = prog(t, 0.15, dur * 0.80)
        # Dome shell
        cx1, cy1 = 560, 640
        d.chord((cx1 - 240, cy1 - 220, cx1 + 240, cy1 + 80), 180, 180 + int(180 * p_draw), fill=(92, 76, 56), outline=CREAM, width=5)
        for r_sc in range(3):
            d.arc((cx1 - 180 + r_sc * 40, cy1 - 170 + r_sc * 25, cx1 + 180 - r_sc * 40, cy1 + 20), 195, 345, fill=GOLD, width=3)
        d.text((cx1 - 130, cy1 + 100), "DOME SHELL", font=fnt(38, italic=True), fill=CREAM)

        # Saddle-backed shell with high front notch
        cx2, cy2 = 1340, 640
        d.chord((cx2 - 240, cy2 - 250, cx2 + 240, cy2 + 80), 205, 205 + int(155 * p_draw), fill=(112, 88, 62), outline=GOLD, width=5)
        # High front arch callout
        arch_r = int(75 * p_draw)
        if arch_r > 10:
            d.arc((cx2 - 255, cy2 - 210, cx2 - 105, cy2 - 40), 250, 70, fill=CREAM, width=6)
        d.text((cx2 - 155, cy2 + 100), "SADDLE ARCH", font=fnt(38, italic=True), fill=GOLD)
        draw_side_label(d, side_label, t, dur)
        return

    if rid == "09_cg_finch_toolbox":
        # Center-left: Gould's 1845 finches lithograph; Right: 4 beak profiles + tool icons
        src_im = arch_cache["gould_finches_1845"].resize((620, 640), Image.Resampling.LANCZOS)
        px = 170 + int(12 * math.sin(u * math.pi))
        py = 230
        d.rounded_rectangle((px - 14, py - 14, px + 634, py + 654), radius=24, fill=(54, 44, 34), outline=GOLD, width=4)
        im.paste(src_im, (px, py))

        beaks = [
            ("1. HEAVY NUTCRACKER", 270, 56, GOLD),
            ("2. STOUT PLIERS", 430, 40, CREAM),
            ("3. FINE TWEEZERS", 590, 26, PALE),
            ("4. SLENDER PROBE", 750, 16, TEAL),
        ]
        for idx, (lbl, yy, depth, col) in enumerate(beaks):
            s = prog(t, 0.5 + idx * 1.6, 2.2 + idx * 1.6)
            if s > 0:
                bx = 930
                blen = int(170 * s)
                d.polygon([(bx, yy - depth), (bx + blen, yy), (bx, yy + depth)], fill=col, outline=WHITE)
                d.text((bx + 210, yy - 22), lbl, font=fnt(36, italic=True), fill=col)
        draw_side_label(d, side_label, t, dur)
        return

    if rid == "03_cg_malthus_curve":
        # Malthus exponential birth curve vs flat linear food line
        ox, oy, gw, gh = 260, 820, 1380, 560
        # Curved axes brackets
        d.line((ox, oy - gh, ox, oy), fill=CREAM, width=4)
        d.line((ox, oy, ox + gw, oy), fill=CREAM, width=4)
        p_c = prog(t, 0.25, dur * 0.82)
        n_pts = max(2, int(80 * p_c))
        exp_pts = []
        lin_pts = []
        for k in range(n_pts + 1):
            s = k / 80.0
            xx = int(ox + gw * s)
            y_food = int(oy - 140 - 95 * s)
            y_born = int(oy - 60 - (gh - 90) * ((math.exp(2.8 * s) - 1.0) / (math.exp(2.8) - 1.0)))
            exp_pts.append((xx, y_born))
            lin_pts.append((xx, y_food))
        if len(lin_pts) >= 2:
            d.line(lin_pts, fill=TEAL, width=6)
            d.line(exp_pts, fill=CRIMSON, width=7)
            d.text((lin_pts[-1][0] - 240, lin_pts[-1][1] + 22), "FOOD SUPPLY", font=fnt(34, italic=True), fill=TEAL)
            d.text((exp_pts[-1][0] - 260, max(160, exp_pts[-1][1] - 48)), "OFFSPRING BORN", font=fnt(34, italic=True), fill=GOLD)
        draw_side_label(d, side_label, t, dur)
        return

    if rid == "06_nature_keeps_fit":
        # Natural selection sieve: 3 beak depths descend toward hard seed barrier; deep beak passes & glows gold
        p_fall = prog(t, 0.2, dur * 0.78)
        sieve_y = 560
        for k in range(14):
            sx = 310 + k * 95
            d.ellipse((sx - 24, sieve_y - 18, sx + 24, sieve_y + 18), fill=TAN, outline=CREAM, width=3)
        profiles = [
            (540, 18, PALE, False, "SHALLOW"),
            (960, 32, CREAM, False, "MEDIUM"),
            (1380, 56, GOLD, True, "DEEP BEAK SURVIVES"),
        ]
        for cx, depth, col, passes, lbl in profiles:
            max_y = 770 if passes else sieve_y - 55
            cy = int(260 + (max_y - 260) * p_fall)
            d.polygon([(cx - 70, cy - depth), (cx + 90, cy), (cx - 70, cy + depth)], fill=col, outline=WHITE)
            d.text((cx - 110, cy + depth + 18), lbl, font=fnt(32, italic=True), fill=col)
        draw_side_label(d, side_label, t, dur)
        return

    if rid == "12_cg_barnacle_counter":
        # 1846 -> 1854 counter + 4 monograph volumes
        p_cnt = prog(t, 0.2, dur * 0.80)
        yr = 1846 + int(round(8 * p_cnt))
        yrs_done = int(round(8 * p_cnt))
        cx, cy = 620, 540
        d.rounded_rectangle((cx - 290, cy - 170, cx + 290, cy + 170), radius=36, fill=(54, 44, 34), outline=GOLD, width=5)
        d.text((cx - 210, cy - 110), f"{yr}", font=fnt(120, italic=True), fill=GOLD)
        d.text((cx - 180, cy + 45), f"{yrs_done} OF 8 YEARS", font=fnt(42, italic=True), fill=CREAM)
        # 4 barnacle monograph volumes appearing on right
        for v in range(4):
            vp = prog(p_cnt, v * 0.20, (v + 1) * 0.24)
            if vp > 0:
                vx = 1080 + v * 155
                vy = int(720 - 340 * vp)
                d.rounded_rectangle((vx, vy, vx + 125, 720), radius=12, fill=(68, 92, 82), outline=GOLD, width=4)
                d.text((vx + 32, vy + 45), f"VOL.{v+1}", font=fnt(28, italic=True), fill=CREAM)
        draw_side_label(d, side_label, t, dur)
        return

    if rid == "05_cg_wallace_counter":
        # Malay Archipelago island chain + 0 -> 125,660 specimen counter
        p_cnt = prog(t, 0.2, dur * 0.85)
        count_val = int(round(125660 * p_cnt))
        islands = [
            [(310, 460), (470, 540), (520, 650), (390, 620)],
            [(560, 670), (790, 690), (820, 740), (580, 725)],
            [(640, 440), (830, 420), (870, 580), (680, 595)],
            [(920, 470), (1040, 450), (1020, 620), (910, 600)],
            [(1110, 510), (1240, 495), (1260, 580), (1120, 590)],
            [(1310, 540), (1560, 560), (1590, 690), (1340, 660)],
        ]
        for idx, poly in enumerate(islands):
            d.polygon(poly, fill=(76, 98, 74), outline=GOLD, width=3)
            cx = sum(p[0] for p in poly) // len(poly)
            cy = sum(p[1] for p in poly) // len(poly)
            if p_cnt >= (idx + 1) / 7.0:
                d.ellipse((cx - 10, cy - 10, cx + 10, cy + 10), fill=GOLD, outline=CREAM, width=3)
        # Specimen counter box top-right
        d.rounded_rectangle((1020, 170, 1740, 390), radius=28, fill=(52, 42, 34), outline=GOLD, width=4)
        d.text((1065, 195), f"{count_val:,}", font=fnt(104, italic=True), fill=GOLD)
        d.text((1070, 315), "SPECIMENS · 1854–1862", font=fnt(36, italic=True), fill=CREAM)
        draw_side_label(d, side_label, t, dur)
        return

    if rid == "07_cg_timeline_origin":
        # 7-date master timeline (1835 .. 1889) + 1,250 copies pre-sold
        dates = [
            ("1835", "Galápagos"),
            ("1837", "Notebook B"),
            ("1838", "Malthus"),
            ("1844", "230p Essay"),
            ("1858", "Wallace"),
            ("1859", "Origin"),
            ("1889", "Darwinism"),
        ]
        p_tl = prog(t, 0.15, dur * 0.78)
        x0, x1, yy = 180, 1740, 520
        cur_x = int(x0 + (x1 - x0) * p_tl)
        d.line((x0, yy, cur_x, yy), fill=GOLD, width=6)
        for idx, (yr, tag) in enumerate(dates):
            dx = x0 + int((x1 - x0) * (idx / (len(dates) - 1)))
            if cur_x >= dx - 5:
                d.ellipse((dx - 14, yy - 14, dx + 14, yy + 14), fill=GOLD if yr == "1859" else CREAM, outline=GOLD, width=4)
                y_off = -95 if idx % 2 == 0 else 45
                d.text((dx - 48, yy + y_off), yr, font=fnt(38, italic=True), fill=GOLD)
                d.text((dx - 68, yy + y_off + 44), tag, font=fnt(26, italic=True), fill=CREAM)
        # Bottom callout: 1,250 copies ordered before opening day
        cnt = int(round(1250 * p_tl))
        d.rounded_rectangle((620, 740, 1300, 880), radius=24, fill=(48, 68, 54), outline=GOLD, width=4)
        d.text((670, 775), f"{cnt:,} COPIES PRE-SOLD", font=fnt(48, italic=True), fill=CREAM)
        draw_side_label(d, side_label, t, dur)
        return

    if rid == "03_cg_blending_beaks":
        # Blending inheritance dilution across 4 generations: 1 -> 1/2 -> 1/4 -> 1/8
        gens = [
            ("GEN 1 · FULL DEPTH", 340, 62, (218, 176, 98), "1"),
            ("GEN 2 · BLENDED", 740, 42, (192, 162, 114), "1/2"),
            ("GEN 3 · DILUTED", 1140, 28, (164, 148, 128), "1/4"),
            ("GEN 4 · WASHED OUT", 1540, 18, (138, 134, 130), "1/8"),
        ]
        for idx, (lbl, cx, depth, col, frac) in enumerate(gens):
            s = prog(t, 0.3 + idx * 1.8, 2.2 + idx * 1.8)
            if s > 0:
                cy = 540
                blen = int(160 * s)
                d.polygon([(cx - 75, cy - depth), (cx - 75 + blen, cy), (cx - 75, cy + depth)], fill=col, outline=CREAM)
                d.text((cx - 65, cy - 140), frac, font=fnt(64, italic=True), fill=col)
                d.text((cx - 115, cy + 95), lbl, font=fnt(28, italic=True), fill=CREAM)
        draw_side_label(d, side_label, t, dur)
        return


def build_all() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    who_records = build_who_overlays()
    print(f"Built {len(who_records)} WHO portrait overlays")

    # Preload raw archive scans
    arch_meta = {
        item["id"]: item
        for item in json.loads((EDIT / "archive_pulls_v01/ARCHIVE_PULLS_RAW_v01.json").read_text())
    }
    arch_cache: dict[str, Image.Image] = {}
    for aid, item in arch_meta.items():
        if item["kind"] == "scan":
            arch_cache[aid] = Image.open(FILM / item["local_raw"]).convert("RGB")

    # Gather all CG and ARCH rows from part-01..06_plates_v01.json
    free_specs = []
    for pnum in range(1, 7):
        pdoc = json.loads((EDIT / f"parts/part-{pnum:02d}_plates_v01.json").read_text())
        for r in pdoc["plates"]:
            if r["route"] in ("code-graphic", "archive"):
                free_specs.append((pnum, r))

    base_canvas = make_base_canvas(1301)

    nas_cg_dir = NAS_EDIT / "code_graphics_v01"
    nas_cg_dir.mkdir(parents=True, exist_ok=True)

    rendered_rows = []
    cuts = []
    pool = []
    cur_t = 0.0

    for idx, (pnum, r) in enumerate(free_specs):
        rid = r["id"]
        dur = float(r["use_s"])
        n_frames = max(15, int(round(dur * FPS)))
        hero_idx = n_frames // 2
        cg_name = f"code_graphic_013_p{pnum}_{rid}.mp4"
        still_name = f"code_graphic_013_p{pnum}_{rid}.jpg"
        mp4_path = nas_cg_dir / cg_name
        still_path = OUT_DIR / still_name

        cmd = [
            "ffmpeg", "-y", "-v", "error",
            "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
            "-i", "-",
            "-an", "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p",
            str(mp4_path),
        ]
        enc = sp.Popen(cmd, stdin=sp.PIPE)
        min_mean = 999.0
        min_p95 = 999.0
        try:
            for f_idx in range(n_frames):
                t = f_idx / FPS
                # Subtle background drift so every frame moves smoothly
                shift_x = int(6 * math.sin(2 * math.pi * (t / max(dur, 1.5))))
                frame_arr = np.roll(base_canvas, shift_x, axis=1).copy()
                im = Image.fromarray(frame_arr, "RGB")
                d = ImageDraw.Draw(im)
                render_frame_content(
                    im, d, rid, pnum, t, dur,
                    r.get("side_label"),
                    r.get("teach_overlay"),
                    (r.get("archive_source") or {}).get("id"),
                    arch_cache,
                )
                if f_idx in (0, hero_idx, n_frames - 1):
                    gray = np.asarray(im.convert("L"), dtype=np.float32)
                    min_mean = min(min_mean, float(gray.mean()))
                    min_p95 = min(min_p95, float(np.percentile(gray, 95)))
                if f_idx == hero_idx:
                    im.save(still_path, quality=92)
                    shutil.copy2(still_path, nas_cg_dir / still_name)
                enc.stdin.write(im.tobytes())
        finally:
            enc.stdin.close()
            if enc.wait() != 0:
                raise RuntimeError(f"ffmpeg failed on {cg_name}")

        actual_dur = round(n_frames / FPS, 3)
        cuts.append({
            "row": f"P{pnum}:{rid}",
            "timeline_in": round(cur_t, 3),
            "timeline_out": round(cur_t + actual_dur, 3),
            "source": cg_name,
            "upscale": 1.0,
            "framing": {"offset": 0.0},
            "video": True,
        })
        pool.append({
            "file_id": cg_name,
            "title": f"own code graphic P{pnum}:{rid}",
        })
        cur_t += actual_dur

        rec = {
            "id": f"P{pnum}:{rid}",
            "file": cg_name,
            "nas_path": str(mp4_path),
            "still": still_name,
            "use_s": dur,
            "encoded_frames": n_frames,
            "encoded_s": actual_dur,
            "film_start_s": r["t_s"],
            "route": r["route"],
            "side_label": r.get("side_label"),
            "min_sample_mean_luma": round(min_mean, 2),
            "min_sample_p95": round(min_p95, 2),
            "near_black": "PASS" if (min_mean >= 28.0 and min_p95 >= 50.0) else "FAIL",
            "sha256_mp4": digest(mp4_path),
            "sha256_still": digest(still_path),
            "spend": "£0",
        }
        rendered_rows.append(rec)
        print(f"[{idx+1:02d}/{len(free_specs):02d}] {rec['id']} -> {cg_name} ({actual_dur:.2f}s) mean={rec['min_sample_mean_luma']} p95={rec['min_sample_p95']} {rec['near_black']}", flush=True)

    # Build contact sheet of all 22 stills
    cols, tw, th = 4, 480, 270
    rows_n = math.ceil(len(rendered_rows) / cols)
    sheet_im = Image.new("RGB", (cols * tw, rows_n * (th + 40)), (28, 36, 48))
    sd = ImageDraw.Draw(sheet_im)
    sfont = fnt(22, italic=True)
    for i, rec in enumerate(rendered_rows):
        st = Image.open(OUT_DIR / rec["still"]).resize((tw, th), Image.Resampling.LANCZOS)
        x, y = (i % cols) * tw, (i // cols) * (th + 40)
        sheet_im.paste(st, (x, y))
        sd.text((x + 10, y + th + 8), f"{rec['id']} ({rec['use_s']:.2f}s)", fill=CREAM, font=sfont)
    sheet_im.save(OUT_DIR / "CONTACT_SHEET.jpg", quality=90)
    shutil.copy2(OUT_DIR / "CONTACT_SHEET.jpg", nas_cg_dir / "CONTACT_SHEET.jpg")

    # Concatenate all 22 mp4s on NAS into a QA reel and run picture_qa.py + polish_gate.py
    concat_txt = nas_cg_dir / "concat_list.txt"
    concat_txt.write_text("".join(f"file '{nas_cg_dir / rec['file']}'\n" for rec in rendered_rows))
    reel_mp4 = nas_cg_dir / "code_graphics_013_reel_v01.mp4"
    sp.run([
        "ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0",
        "-i", str(concat_txt), "-c", "copy", str(reel_mp4)
    ], check=True)

    (OUT_DIR / "cuts_v01.json").write_text(json.dumps(cuts, indent=2) + "\n")
    (OUT_DIR / "pool_v01.json").write_text(json.dumps(pool, indent=2) + "\n")
    (OUT_DIR / "CODE_GRAPHICS_v01.json").write_text(json.dumps({
        "film": "013_Darwin-Wallace-Evolution",
        "version": "v01",
        "task": "J2476",
        "spend": "£0",
        "who_overlays_count": len(who_records),
        "who_overlays": who_records,
        "rendered_clips_count": len(rendered_rows),
        "rendered_clips": rendered_rows,
    }, indent=2) + "\n")

    # Run polish_gate.py
    pg_json = OUT_DIR / "polish_gate_v01.json"
    pg_res = sp.run([
        "python3", str(OWB_ROOT / "scripts/polish_gate.py"),
        str(reel_mp4),
        "--cuts", str(OUT_DIR / "cuts_v01.json"),
        "--out", str(pg_json),
        "--no-jitter",
    ], capture_output=True, text=True, check=True)
    (OUT_DIR / "polish_gate_v01.txt").write_text(pg_res.stdout)
    print(pg_res.stdout, end="")

    # Run picture_qa.py
    pqa_dir = OUT_DIR / "picture_qa_v01"
    pqa_dir.mkdir(parents=True, exist_ok=True)
    pqa_res = sp.run([
        "python3", str(OWB_ROOT / "scripts/picture_qa.py"),
        str(reel_mp4),
        "--cuts", str(OUT_DIR / "cuts_v01.json"),
        "--pool", str(OUT_DIR / "pool_v01.json"),
        "--out-dir", str(pqa_dir),
        "--no-jitter",
    ], capture_output=True, text=True, check=True)
    (OUT_DIR / "picture_qa_v01.txt").write_text(pqa_res.stdout)
    print(pqa_res.stdout, end="")

    # Copy metadata to NAS
    for fn in ("cuts_v01.json", "pool_v01.json", "CODE_GRAPHICS_v01.json", "polish_gate_v01.json", "polish_gate_v01.txt", "picture_qa_v01.txt"):
        shutil.copy2(OUT_DIR / fn, nas_cg_dir / fn)
    if (EDIT / "archive_pulls_v01").exists():
        shutil.copytree(EDIT / "archive_pulls_v01", NAS_EDIT / "archive_pulls_v01", dirs_exist_ok=True)


if __name__ == "__main__":
    build_all()
