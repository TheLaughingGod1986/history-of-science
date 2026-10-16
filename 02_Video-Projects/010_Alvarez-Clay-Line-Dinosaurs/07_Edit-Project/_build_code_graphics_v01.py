#!/usr/bin/env python3
"""J0348: HOS 010 thirteen £0 teach graphics from plate boards v02.

Cream ink on a lifted navy field. Durations, file names and the three side
labels are read from the merged boards. Numbers on screen are only the ones
the boards and FACT_NOTES already allow: Gubbio about 30 times, Chicxulub
about 180 km. The early-1990s call-out is the date spoken on that beat.
No Flow, no Vertex, no audio, no place names.
"""
import argparse, hashlib, json, math, subprocess as sp
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont

W, H, FPS = 1920, 1080, 30
FONT = "/System/Library/Fonts/Supplemental/Didot.ttc"
ROOT = Path(__file__).resolve().parent
CREAM = (244, 228, 195)
GOLD = (214, 172, 96)
PALE = (196, 176, 148)
TAN = (150, 124, 96)
CLAY = (112, 86, 68)
WHITE = (236, 232, 220)
BLUE = (160, 196, 214)
INK = (232, 214, 186)

# Painted blobs, not a traced atlas. Names stay in code only.
CONTINENTS = {
    "namer": [(-168, 66), (-140, 70), (-100, 73), (-82, 68), (-62, 48), (-68, 44),
              (-78, 26), (-97, 22), (-110, 24), (-125, 40), (-140, 58), (-158, 62)],
    "samer": [(-78, 8), (-62, 10), (-48, 2), (-36, -8), (-38, -22), (-48, -36),
              (-68, -55), (-74, -48), (-76, -18), (-80, -2)],
    "europe": [(-10, 36), (-8, 44), (-6, 52), (0, 58), (8, 62), (14, 58), (12, 54),
               (20, 60), (28, 70), (40, 64), (44, 48), (28, 41), (18, 37), (10, 36), (2, 36)],
    "italy": [(7.5, 46), (9, 45), (11, 43.5), (13.5, 41.5), (15.5, 40.5), (16.2, 38.5),
              (14.5, 37.2), (12.2, 38.2), (10.2, 41), (8.2, 44)],
    "africa": [(-16, 20), (-8, 35), (10, 32), (32, 30), (43, 12), (50, 8), (42, -12),
               (34, -30), (20, -35), (14, -28), (12, -6), (8, 4), (-6, 6), (-14, 14)],
    "asia": [(40, 36), (48, 42), (60, 48), (70, 62), (100, 72), (140, 70), (178, 66),
             (160, 54), (142, 40), (128, 34), (122, 22), (108, 12), (98, 6), (80, 8),
             (68, 22), (56, 24), (44, 30)],
    "aus": [(114, -20), (128, -14), (142, -12), (152, -24), (150, -36), (136, -38),
            (120, -34), (114, -26)],
    "nz": [(166, -36), (174, -35), (178, -38), (178, -46), (172, -47), (166, -42)],
    "green": [(-62, 76), (-42, 82), (-22, 74), (-44, 62), (-68, 66)],
}
PINS = {"italy": (12.6, 41.6), "cliff": (10.5, 57.2), "nz": (174.0, -41.0)}
CARIB = (-84.0, 19.0)

# kind, and timed labels (text, t0, t1). Each label is 4 words or fewer.
LABELS = {
    "02_layers_build": [],
    "08_two_clocks": [],
    "02_pyramid_muons": [],
    "07_clock_idea": [],
    "01_iridium_spike": [("THE IRIDIUM SPIKE", 0.6, 4.2), ("ABOUT 30 TIMES", 8.2, 11.8)],
    "03_world_pins": [("ALL AROUND THE WORLD", 1.0, 4.6)],
    "04_supernova_test": [],
    "05_ten_km": [],
    "07_food_chain": [],
    "10_where_hole": [],
    "03_caribbean_hunt": [("EARLY 1990s", 6.2, 9.8)],
    "05_ring_scale": [("ABOUT 180 KM WIDE", 2.0, 5.6)],
    "11_why_survive": [],
}
SIDE = {
    "01_iridium_spike": "THE IRIDIUM SPIKE",
    "03_world_pins": "ALL AROUND THE WORLD",
    "05_ring_scale": "ABOUT 180 KM WIDE",
}
HERO_T = {
    "layers": 6.4, "clocks": 8.0, "pyramid": 4.5, "clay": 8.0, "spike": 10.0,
    "pins": 13.0, "supernova": 16.5, "tenkm": 4.0, "food": 6.5, "hole": 3.6,
    "caribbean": 11.5, "ring": 4.2, "survive": 12.8,
}
ORDER = [
    (2, "02_layers_build", "layers"),
    (2, "08_two_clocks", "clocks"),
    (3, "02_pyramid_muons", "pyramid"),
    (3, "07_clock_idea", "clay"),
    (4, "01_iridium_spike", "spike"),
    (4, "03_world_pins", "pins"),
    (4, "04_supernova_test", "supernova"),
    (4, "05_ten_km", "tenkm"),
    (4, "07_food_chain", "food"),
    (4, "10_where_hole", "hole"),
    (5, "03_caribbean_hunt", "caribbean"),
    (5, "05_ring_scale", "ring"),
    (5, "11_why_survive", "survive"),
]


def ease(x):
    x = max(0.0, min(1.0, x))
    return x * x * (3 - 2 * x)


def prog(t, a, b):
    return ease((t - a) / (b - a)) if b > a else 1.0


def col(rgb, a=1.0):
    return (rgb[0], rgb[1], rgb[2], int(max(0, min(255, round(255 * a)))))


def navy():
    y, x = np.mgrid[:H, :W]
    nx = (x - W / 2) / (W / 2)
    ny = (y - H / 2) / (H / 2)
    v = np.clip(nx * nx + ny * ny, 0, 1)
    rng = np.random.default_rng(1010)
    noise = rng.normal(0, 1.5, (H, W))
    img = np.zeros((H, W, 3), np.float32)
    base = np.array([36, 54, 82], np.float32)
    lift = np.array([22, 26, 30], np.float32)
    for c in range(3):
        img[:, :, c] = base[c] + lift[c] * (1 - v) + noise
    return Image.fromarray(np.uint8(np.clip(img, 0, 255)), "RGB")


def chaikin(pts, iters=2):
    pts = list(pts)
    for _ in range(iters):
        nxt = []
        n = len(pts)
        for i in range(n):
            a, b = pts[i], pts[(i + 1) % n]
            nxt.append((0.75 * a[0] + 0.25 * b[0], 0.75 * a[1] + 0.25 * b[1]))
            nxt.append((0.25 * a[0] + 0.75 * b[0], 0.25 * a[1] + 0.75 * b[1]))
        pts = nxt
    return pts


def world_pt(lon, lat, scale=1.0, focus=(8, 12)):
    x = 960 + (lon - focus[0]) * 4.15 * scale
    y = 580 - (lat - focus[1]) * 5.15 * scale
    return (x, y)


def draw_world(d, scale=1.0, focus=(8, 12), alpha=1.0):
    for pts in CONTINENTS.values():
        pix = [world_pt(lon, lat, scale, focus) for lon, lat in pts]
        d.polygon(pix, fill=col(PALE, 0.42 * alpha))
        d.line(pix + [pix[0]], fill=col(CREAM, 0.9 * alpha), width=3)


def pin(d, x, y, p, rgb=GOLD):
    if p <= 0:
        return
    p = min(1.0, p)
    y0 = y - (1 - p) * 220
    d.line((x, y0 - 46, x, y0), fill=col(rgb, p), width=6)
    d.ellipse((x - 14, y0 - 68, x + 14, y0 - 40), outline=col(rgb, p), width=6)


def cliff_mark(d, x, y, p):
    if p <= 0:
        return
    h = 46 * p
    d.rectangle((x - 14, y - h, x + 14, y), fill=col(WHITE, p))
    d.rectangle((x - 14, y - h * 0.48, x + 14, y - h * 0.32), fill=col(CLAY, p))


def qmark(d, cx, cy, p):
    if p <= 0:
        return
    font = ImageFont.truetype(FONT, 260, index=1)
    d.text((cx, cy), "?", font=font, fill=col(CREAM, min(1.0, p)), anchor="mm")


def _half_w(y, top, mid, bot, hw, neck):
    if y <= mid:
        u = (y - top) / max(1.0, mid - top)
        return hw * (1 - u) + neck * u
    u = (y - mid) / max(1.0, bot - mid)
    return neck * (1 - u) + hw * u


def _sand(d, cx, y0, y1, top, mid, bot, hw, neck, rgb):
    if y1 - y0 < 4:
        return
    w0 = max(4, _half_w(y0, top, mid, bot, hw, neck) - 10)
    w1 = max(4, _half_w(y1, top, mid, bot, hw, neck) - 10)
    d.polygon([(cx - w0, y0), (cx + w0, y0), (cx + w1, y1), (cx - w1, y1)], fill=rgb)


def hourglass(d, cx, top, bot, poured, a=1.0):
    mid = (top + bot) / 2
    hw, neck = 92, 14
    c = col(CREAM, a)
    d.line([(cx - hw, top), (cx - neck, mid), (cx + neck, mid), (cx + hw, top), (cx - hw, top)], fill=c, width=6)
    d.line([(cx - hw, bot), (cx - neck, mid), (cx + neck, mid), (cx + hw, bot), (cx - hw, bot)], fill=c, width=6)
    poured = max(0.0, min(1.0, poured))
    sand = col(GOLD, 0.92 * a)
    span = mid - top - 28
    _sand(d, cx, top + 14, top + 14 + span * (1 - poured), top, mid, bot, hw, neck, sand)
    _sand(d, cx, bot - 14 - span * poured, bot - 14, top, mid, bot, hw, neck, sand)
    if 0.04 < poured < 0.96:
        d.line((cx, mid - 6, cx, mid + 16), fill=sand, width=4)


def skyline(d, x0, ground, a, t):
    heights = [70, 120, 86, 168, 96, 140, 64, 110]
    x = x0
    for i, h in enumerate(heights):
        w = 48
        d.rectangle((x, ground - h, x + w, ground), outline=col(CREAM, a), width=4)
        blink = 0.35 + 0.65 * (0.5 + 0.5 * math.sin(t * 2.2 + i))
        for wy in range(ground - h + 16, ground - 12, 28):
            d.rectangle((x + 14, wy, x + 24, wy + 12), fill=col(GOLD, a * blink * 0.8))
        x += w + 10
    d.line((x0 - 20, ground, x + 10, ground), fill=col(CREAM, a), width=4)


def rock(d, cx, cy, r, t, a=1.0):
    pts = []
    for i in range(11):
        ang = -math.pi / 2 + i * (2 * math.pi / 11)
        wob = 0.78 + 0.22 * math.sin(i * 1.7)
        pts.append((cx + math.cos(ang) * r * wob, cy + math.sin(ang) * r * wob * 0.86))
    d.polygon(pts, fill=col(TAN, 0.55 * a), outline=col(CREAM, a))
    d.line(pts + [pts[0]], fill=col(CREAM, a), width=6)
    ang = t * 0.7
    d.line((cx + math.cos(ang) * r * 0.15, cy + math.sin(ang) * r * 0.1,
            cx + math.cos(ang) * r * 0.55, cy + math.sin(ang) * r * 0.4), fill=col(GOLD, 0.7 * a), width=5)


def fern(d, x, y, a):
    c = col(CREAM, a)
    d.line((x, y, x, y - 240), fill=c, width=6)
    for i, yy in enumerate(range(y - 36, y - 230, -32)):
        s = 28 + i * 8
        d.line((x, yy, x - s, yy - 18), fill=c, width=4)
        d.line((x, yy, x + s, yy - 18), fill=c, width=4)


def grazer(d, x, y, a):
    c = col(CREAM, a)
    d.ellipse((x - 70, y - 70, x + 70, y - 10), outline=c, width=5)
    d.ellipse((x + 48, y - 110, x + 96, y - 62), outline=c, width=5)
    d.line((x + 70, y - 78, x + 40, y - 40), fill=c, width=5)
    for lx in (-48, -16, 16, 46):
        d.line((x + lx, y - 16, x + lx - 6, y + 36), fill=c, width=5)
    d.line((x - 60, y - 36, x - 110, y - 20), fill=c, width=4)


def hunter(d, x, y, a):
    c = col(CREAM, a)
    d.ellipse((x - 36, y - 150, x + 36, y - 40), outline=c, width=5)
    d.ellipse((x - 22, y - 196, x + 22, y - 150), outline=c, width=5)
    d.line((x - 18, y - 40, x - 28, y + 36), fill=c, width=5)
    d.line((x + 16, y - 40, x + 26, y + 36), fill=c, width=5)
    d.line((x - 30, y - 120, x - 70, y - 90), fill=c, width=4)
    d.line((x + 54, y - 70, x + 96, y - 110), fill=c, width=4)


def bird(d, x, y, a):
    c = col(CREAM, a)
    d.ellipse((x - 36, y - 24, x + 40, y + 16), outline=c, width=5)
    d.polygon([(x + 36, y - 6), (x + 70, y - 14), (x + 36, y + 8)], outline=c)
    d.arc((x - 20, y - 46, x + 50, y + 10), 200, 20, fill=c, width=5)
    d.line((x - 30, y, x - 62, y - 16), fill=c, width=4)
    d.ellipse((x + 18, y - 16, x + 28, y - 6), fill=c)


def seed(d, x, y, a):
    c = col(CREAM, a)
    d.ellipse((x - 28, y - 48, x + 28, y + 48), outline=c, width=5)
    d.line((x, y - 48, x + 8, y - 78), fill=c, width=4)


def nest(d, x, y, a):
    c = col(CREAM, a)
    d.line((x - 120, y, x + 120, y), fill=c, width=4)
    d.arc((x - 54, y - 36, x + 54, y + 28), 200, 340, fill=c, width=5)
    d.arc((x - 70, y - 18, x - 10, y + 20), 210, 20, fill=col(GOLD, a), width=3)
    d.arc((x + 8, y - 16, x + 68, y + 22), 200, 10, fill=col(GOLD, a), width=3)


def tube(d, x, y, a):
    c = col(CREAM, a)
    d.rounded_rectangle((x - 36, y, x + 36, y + 210), radius=18, outline=c, width=6)
    d.rectangle((x - 28, y + 90, x + 28, y + 190), fill=col(GOLD, 0.55 * a))
    d.line((x - 28, y - 30, x - 28, y + 16), fill=c, width=6)
    d.line((x + 28, y - 30, x + 28, y + 16), fill=c, width=6)


SOUTH = chaikin([
    (400, 720), (520, 600), (660, 540), (800, 520), (920, 600),
    (1020, 540), (1160, 510), (1320, 540), (1460, 610), (1400, 720),
    (1220, 790), (1000, 810), (780, 780), (580, 760), (440, 780),
], iters=1)


def paint(bg, kind, t, dur):
    im = bg.convert("RGBA")
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    if kind == "layers":
        rests = [860, 760, 660, 560, 460, 360]
        shades = [TAN, PALE, CLAY, PALE, TAN, PALE]
        for i, (y0, shade) in enumerate(zip(rests, shades)):
            p = prog(t, 0.25 + i * 0.7, 1.3 + i * 0.7)
            y = y0 - (1 - p) * 160
            h = 86
            pts = [(120, y + 8)]
            for x in range(120, 1800, 48):
                pts.append((x, y + math.sin(x * 0.012 + i) * 7))
            pts += [(1800, y + 8), (1800, y + h), (120, y + h)]
            d.polygon(pts, fill=col(shade, 0.55 * p))
            d.line(pts[: len(pts) - 2], fill=col(CREAM, 0.85 * p), width=3)
        if t > 6.2:
            for i in range(8):
                yy = 200 + ((t * 40 + i * 90) % 700)
                d.ellipse((400 + i * 160, yy, 406 + i * 160, yy + 6), fill=col(CREAM, 0.5))
    elif kind == "clocks":
        hourglass(d, 620, 250, 900, prog(t, 1.4, 6.2))
        slow = min(0.18, prog(t, 2.0, dur) * 0.18)
        hourglass(d, 1300, 250, 900, min(0.08, slow))
        if t > 2:
            drip = (t * 0.45) % 1
            d.ellipse((1294, 560 + drip * 120, 1306, 572 + drip * 120), fill=col(GOLD, 0.9))
    elif kind == "pyramid":
        apex, bl, br = (960, 180), (560, 900), (1360, 900)
        p = prog(t, 0.2, 1.6)
        d.line([apex, bl, br, apex], fill=col(CREAM, p), width=6)
        for i in range(1, 8):
            yy = apex[1] + (br[1] - apex[1]) * (i / 8) 
            tt = (yy - apex[1]) / (bl[1] - apex[1])
            left = apex[0] + (bl[0] - apex[0]) * tt
            right = apex[0] + (br[0] - apex[0]) * tt
            if p > i / 10:
                d.line((left, yy, right, yy), fill=col(PALE, 0.7 * p), width=3)
        if t > 1.1:
            for i in range(8):
                phase = (t * 0.28 + i / 8) % 1
                yy = apex[1] + 40 + phase * (bl[1] - apex[1] - 60)
                tt = (yy - apex[1]) / (bl[1] - apex[1])
                left = apex[0] + (bl[0] - apex[0]) * tt
                right = apex[0] + (br[0] - apex[0]) * tt
                xx = left + 30 + (right - left - 60) * ((i * 0.17) % 1)
                d.line((xx, yy - 20, xx + 4, yy + 64), fill=col(BLUE, 0.95), width=5)
    elif kind == "clay":
        for x, dense in ((430, True), (1130, False)):
            d.rounded_rectangle((x, 240, x + 340, 900), radius=18, outline=col(CREAM, 1), width=6)
            d.rectangle((x + 8, 250, x + 332, 890), fill=col(CLAY, 0.45))
        rng = np.random.default_rng(7)
        for i in range(70):
            xx = 460 + rng.random() * 280
            yy = 280 + rng.random() * 580
            tw = 0.45 + 0.55 * (0.5 + 0.5 * math.sin(t * 3 + i))
            d.ellipse((xx, yy, xx + 7, yy + 7), fill=col(GOLD, tw))
        for i, (xx, yy) in enumerate(((1210, 520), (1320, 640), (1260, 760))):
            tw = 0.4 + 0.6 * (0.5 + 0.5 * math.sin(t * 1.4 + i))
            d.ellipse((xx, yy, xx + 8, yy + 8), fill=col(GOLD, 0.35 * tw))
    elif kind == "spike":
        for i, y in enumerate(range(280, 900, 70)):
            shade = CLAY if i == 5 else PALE
            d.rectangle((180, y, 1740, y + 64), fill=col(shade, 0.18))
        peak_i = 42
        peak_x = 240 + peak_i * (1440 / 69)
        d.rectangle((peak_x - 36, 280, peak_x + 36, 900), fill=col(CLAY, 0.45))
        pts = []
        for i in range(70):
            x = 240 + i * (1440 / 69)
            base = 820
            if peak_i - 4 <= i <= peak_i + 4:
                peak = 1 - abs(i - peak_i) / 4
                base = 820 - peak * 480
            pts.append((x, base))
        draw_n = int(prog(t, 0.4, 9.5) * (len(pts) - 1))
        if draw_n >= 1:
            d.line(pts[: draw_n + 1], fill=col(GOLD, 1), width=8)
        if t > 9:
            pulse = 0.6 + 0.4 * math.sin(t * 2)
            d.ellipse((pts[peak_i][0] - 12, pts[peak_i][1] - 12, pts[peak_i][0] + 12, pts[peak_i][1] + 12), fill=col(CREAM, pulse))
    elif kind == "pins":
        a = prog(t, 0.2, 1.4)
        draw_world(d, alpha=a)
        pin(d, *world_pt(*PINS["italy"]), prog(t, 2.2, 3.6))
        cx, cy = world_pt(*PINS["cliff"])
        cliff_mark(d, cx, cy + 8, prog(t, 6.0, 7.6))
        pin(d, *world_pt(*PINS["nz"]), prog(t, 10.0, 11.6))
    elif kind == "supernova":
        cx, cy, flare = 520, 360, prog(t, 1.5, 3.2) * (1 - prog(t, 4.0, 6.5))
        r = 28 + flare * 70
        d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=col(GOLD, 0.85))
        for i in range(8):
            ang = i * math.pi / 4 + t * 0.15
            d.line((cx, cy, cx + math.cos(ang) * (r + 40 + flare * 50), cy + math.sin(ang) * (r + 40)), fill=col(CREAM, 0.8), width=4)
        line_p = prog(t, 5.5, 11.0)
        if line_p > 0:
            x2 = cx + (1380 - cx) * line_p
            y2 = cy + (640 - cy) * line_p
            steps = 18
            for i in range(int(steps * line_p)):
                u = i / steps
                d.ellipse((cx + (1380 - cx) * u - 4, cy + (640 - cy) * u - 4,
                           cx + (1380 - cx) * u + 4, cy + (640 - cy) * u + 4), fill=col(CREAM, 0.9))
        if t > 8:
            tube(d, 1380, 560, prog(t, 8.0, 11.5))
        if t > 12.5:
            cross = prog(t, 12.5, 15.5)
            s = 70 * cross
            d.line((cx - s, cy - s, cx + s, cy + s), fill=col(CREAM, cross), width=10)
            d.line((cx + s, cy - s, cx - s, cy + s), fill=col(CREAM, cross), width=10)
    elif kind == "tenkm":
        skyline(d, 1180, 860, prog(t, 0.3, 1.6), t)
        rock(d, 520, 420, 300, t, prog(t, 0.2, 1.2))
    elif kind == "food":
        fern(d, 480, 780, prog(t, 0.3, 1.4) * (1 - 0.65 * prog(t, 2.4, 3.6)))
        grazer(d, 960, 760, prog(t, 2.6, 3.8) * (1 - 0.6 * prog(t, 4.6, 5.8)))
        hunter(d, 1420, 760, prog(t, 4.8, 6.0) * (1 - 0.45 * prog(t, 6.4, 7.4)))
    elif kind == "hole":
        draw_world(d, alpha=prog(t, 0.15, 1.1))
        qx, qy = world_pt(-38, 22)
        qmark(d, qx, qy, prog(t, 1.2, 2.6))
    elif kind == "caribbean":
        z = prog(t, 1.6, 10.5)
        scale = 1 + 1.15 * z
        focus = (8 + (CARIB[0] - 8) * z, 12 + (CARIB[1] - 12) * z)
        draw_world(d, scale=scale, focus=focus, alpha=1)
        cx, cy = world_pt(*CARIB, scale, focus)
        ring_a = prog(t, 4.0, 6.0)
        wob = 6 * math.sin(t * 1.3)
        if ring_a > 0:
            r = 90 + wob
            d.ellipse((cx - r, cy - r, cx + r, cy + r), outline=col(GOLD, 0.85 * ring_a), width=6)
    elif kind == "ring":
        p = prog(t, 0.2, 1.6)
        d.polygon(SOUTH, fill=col(PALE, 0.5 * p))
        d.line(SOUTH + [SOUTH[0]], fill=col(CREAM, p), width=5)
        rp = prog(t, 1.6, 3.8)
        box = (860, 560, 1180, 800)
        if rp > 0.98:
            d.ellipse(box, outline=col(GOLD, 1), width=10)
        elif rp > 0:
            d.arc(box, start=0, end=max(2, int(359 * rp)), fill=col(GOLD, 1), width=10)
    elif kind == "survive":
        bird(d, 480, 560, prog(t, 0.6, 2.0))
        seed(d, 960, 560, prog(t, 4.2, 5.6))
        nest(d, 1420, 640, prog(t, 7.8, 9.2))
        arc_p = prog(t, 10.2, 12.6)
        if arc_p > 0:
            d.arc((360, 300, 1560, 860), start=200, end=int(200 + 140 * arc_p), fill=col(GOLD, 0.8), width=6)
    else:
        raise ValueError(kind)
    im = Image.alpha_composite(im, ov)
    return im.convert("RGB")


def label_layer(labels, t):
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    if not labels:
        return ov
    d = ImageDraw.Draw(ov)
    shown = []
    for text, t0, t1 in labels:
        words = text.split()
        if len(words) > 4:
            raise SystemExit(f"label has {len(words)} words: {text}")
        a = prog(t, t0, t0 + 0.4) * (1 - prog(t, t1 - 0.4, t1))
        if a > 0.02:
            shown.append((text, a))
    y = 150
    for text, a in shown:
        size = 68 if len(text) < 22 else 58
        font = ImageFont.truetype(FONT, size, index=1)
        d.text((W / 2, y), text, font=font, fill=col(CREAM, a), anchor="mm",
               stroke_width=2, stroke_fill=col((20, 28, 44), a))
        y += 84
    return ov


def load_specs():
    specs = []
    for part, pid, kind in ORDER:
        board_path = ROOT / "parts" / f"part-{part:02d}_plates_v02.json"
        board = json.loads(board_path.read_text())
        row = next(p for p in board["plates"] if p["id"] == pid)
        if row["route"] != "code-graphic":
            raise SystemExit(f"{pid} route is {row['route']}")
        side = row.get("side_label")
        if SIDE.get(pid) != side:
            raise SystemExit(f"{pid} side_label {side!r} != {SIDE.get(pid)!r}")
        labels = LABELS[pid]
        for text, t0, t1 in labels:
            if t1 - t0 > 4.0:
                raise SystemExit(f"{text} holds {t1 - t0:.2f}s")
            if len(text.split()) > 4:
                raise SystemExit(text)
        if side and side not in [text for text, _, _ in labels]:
            raise SystemExit(f"missing side label {side}")
        specs.append({
            "id": pid,
            "part": part,
            "kind": kind,
            "file": row["code_graphic_spec"]["file"],
            "dur": row["use_s"],
            "t_s": row["t_s"],
            "vo_land": row["vo_land"],
            "shows": row["code_graphic_spec"]["shows"],
            "labels": labels,
            "board": board_path.name,
        })
    if len(specs) != 13:
        raise SystemExit(f"expected 13 graphics, got {len(specs)}")
    return specs


def digest(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def render_one(bg, spec, out, stills_only=False):
    n = math.ceil(spec["dur"] * FPS)
    hero = min(n - 1, int(min(HERO_T[spec["kind"]], spec["dur"] - 0.15) * FPS))
    still_path = out / (Path(spec["file"]).stem + ".jpg")
    path = out / spec["file"]
    enc = None
    if not stills_only:
        enc = sp.Popen(
            ["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pixel_format", "rgb24",
             "-video_size", f"{W}x{H}", "-framerate", str(FPS), "-i", "-", "-an",
             "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p",
             "-movflags", "+faststart", str(path)],
            stdin=sp.PIPE,
        )
    min_mean, min_p95 = 999.0, 999.0
    frames = [hero] if stills_only else range(n)
    try:
        for k in frames:
            t = k / FPS
            frame = paint(bg, spec["kind"], t, spec["dur"])
            lab = label_layer(spec["labels"], t)
            if lab.getbbox():
                frame = Image.alpha_composite(frame.convert("RGBA"), lab).convert("RGB")
            if stills_only or k % 15 == 0 or k == hero:
                g = np.asarray(frame.convert("L"))
                min_mean = min(min_mean, float(g.mean()))
                min_p95 = min(min_p95, float(np.percentile(g, 95)))
            if k == hero:
                frame.save(still_path, quality=90)
            if enc is not None:
                enc.stdin.write(frame.tobytes())
    finally:
        if enc is not None:
            enc.stdin.close()
            if enc.wait() != 0:
                raise RuntimeError(f"ffmpeg failed for {spec['file']}")
    words = []
    for text, _, _ in spec["labels"]:
        words.append({"text": text, "words": len(text.split())})
    rec = {
        "id": f"P{spec['part']}:{spec['id']}",
        "file": spec["file"],
        "use_s": spec["dur"],
        "encoded_frames": n,
        "encoded_s": round(n / FPS, 3),
        "film_start_s": spec["t_s"],
        "vo_land": spec["vo_land"],
        "shows": spec["shows"],
        "labels": words,
        "board": spec["board"],
        "min_sample_mean_luma": round(min_mean, 2),
        "min_sample_p95": round(min_p95, 2),
        "near_black": "PASS" if (min_mean >= 28 or min_p95 >= 50) else "FAIL",
        "still": still_path.name,
        "spend": "£0",
    }
    if path.exists() and not stills_only:
        probe = json.loads(sp.check_output(["ffprobe", "-v", "error", "-show_streams", "-of", "json", str(path)]))
        v = next(s for s in probe["streams"] if s["codec_type"] == "video")
        if any(s.get("codec_type") == "audio" for s in probe["streams"]):
            raise SystemExit(f"audio on {path.name}")
        if (int(v["width"]), int(v["height"])) != (W, H):
            raise SystemExit(f"size {path.name}")
        rec["sha256"] = digest(path)
        rec["bytes"] = path.stat().st_size
        rec["probed_nb_frames"] = int(v["nb_frames"])
    return rec


def sheet(out, rows):
    cols, tw, th = 4, 480, 270
    rows_n = math.ceil(len(rows) / cols)
    im = Image.new("RGB", (cols * tw, rows_n * (th + 40)), (28, 40, 62))
    d = ImageDraw.Draw(im)
    font = ImageFont.truetype(FONT, 22, index=1)
    for i, rec in enumerate(rows):
        still = Image.open(out / rec["still"]).resize((tw, th))
        x, y = (i % cols) * tw, (i // cols) * (th + 40)
        im.paste(still, (x, y))
        d.text((x + 8, y + th + 8), rec["id"], fill=CREAM, font=font)
    im.save(out / "CONTACT_SHEET.jpg", quality=90)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=ROOT / "code_graphics_v01")
    ap.add_argument("--stills-only", action="store_true")
    ap.add_argument("--only", default="")
    args = ap.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    specs = load_specs()
    if args.only:
        specs = [s for s in specs if args.only in s["id"] or args.only in s["kind"]]
        if not specs:
            raise SystemExit(f"no match for {args.only}")
    bg = navy()
    rows = []
    for spec in specs:
        rec = render_one(bg, spec, args.out, args.stills_only)
        rows.append(rec)
        print(rec["id"], rec["near_black"], rec["min_sample_mean_luma"], rec["labels"], flush=True)
        if rec["near_black"] != "PASS":
            raise SystemExit(f"near-black FAIL {rec['id']}")
    if not args.only:
        sheet(args.out, rows)
        (args.out / "CODE_GRAPHICS_v01.json").write_text(json.dumps(rows, indent=2) + "\n")
        files = sorted(p for p in args.out.iterdir() if p.suffix in {".jpg", ".json", ".py"})
        (args.out / "SHA256SUMS.txt").write_text("".join(f"{digest(p)}  {p.name}\n" for p in files))
    fails = [r["id"] for r in rows if r["near_black"] != "PASS"]
    if fails:
        raise SystemExit(f"FAIL {fails}")
    print(f"OK {len(rows)}", "stills" if args.stills_only else "rendered")


if __name__ == "__main__":
    main()
