"""J0342: HOS 009 parchment teach graphics. Twelve £0 code renders.

House explainer: dark-sepia ink on moving period paper, cream Didot italic
labels. No Flow, no Vertex, no audio. Overlay rows use our own moving paper
because the named Flow plates are not minted (mint stays held).
"""
import argparse, hashlib, json, math, subprocess as sp
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont

W, H, FPS = 1920, 1080, 30
FONT = "/System/Library/Fonts/Supplemental/Didot.ttc"
INK = (34, 16, 6, 255)
CREAM = (255, 244, 218, 255)
WASH = (216, 178, 124, 255)
MOON_WASH = (232, 212, 176, 255)

SPECS = [
    {"id": "09_pull_heights", "file": "code_graphic_009_p2_09_pull_heights.mp4", "dur": 4.14, "label": "TREE, TOWER, MOUNTAIN", "kind": "pull_heights", "layout": "full_frame_period_paper", "plate": None},
    {"id": "09_pull_heights_c1", "file": "code_graphic_009_p2_09_pull_heights_c1.mp4", "dur": 4.14, "label": "PULL AT THE TOP", "kind": "pull_heights_c1", "layout": "moving_plate_overlay", "plate": "08_the_apple_c1"},
    {"id": "06_orbit_teach", "file": "code_graphic_009_p3_06_orbit_teach.mp4", "dur": 4.40, "label": "FALLING SIDEWAYS", "kind": "orbit_teach", "layout": "full_frame_period_paper", "plate": None},
    {"id": "06_orbit_teach_c1", "file": "code_graphic_009_p3_06_orbit_teach_c1.mp4", "dur": 4.40, "label": "NEVER HITS", "kind": "orbit_teach_c1", "layout": "moving_plate_overlay", "plate": "05_shot_orbit_c2"},
    {"id": "08_km_a_second", "file": "code_graphic_009_p3_08_km_a_second.mp4", "dur": 4.95, "label": "SIDEWAYS AND DOWN", "kind": "km_a_second", "layout": "full_frame_period_paper", "plate": None},
    {"id": "08_km_a_second_c1", "file": "code_graphic_009_p3_08_km_a_second_c1.mp4", "dur": 4.95, "label": "FOR EVER", "kind": "km_a_second_c1", "layout": "moving_plate_overlay", "plate": "07_ball_to_moon"},
    {"id": "01_weaker_far", "file": "code_graphic_009_p4_01_weaker_far.mp4", "dur": 7.11, "label": "WEAKER WITH DISTANCE", "kind": "weaker_far", "layout": "full_frame_period_paper", "plate": None},
    {"id": "01_weaker_far_c1", "file": "code_graphic_009_p4_01_weaker_far_c1.mp4", "dur": 7.11, "label": "FOUR TIMES WEAKER", "kind": "weaker_far_c1", "layout": "moving_plate_overlay", "plate": None},
    {"id": "03_sixty_earths", "file": "code_graphic_009_p4_03_sixty_earths.mp4", "dur": 4.68, "label": "SIXTY EARTHS", "kind": "sixty_earths", "layout": "full_frame_period_paper", "plate": None},
    {"id": "04_dots_square", "file": "code_graphic_009_p4_04_dots_square.mp4", "dur": 5.53, "label": "SIXTY TIMES SIXTY", "kind": "dots_square", "layout": "moving_plate_overlay", "plate": "02_spray_paint_c2"},
    {"id": "04_dots_square_c1", "file": "code_graphic_009_p4_04_dots_square_c1.mp4", "dur": 5.53, "label": "ONE TINY DOT", "kind": "dots_square_c1", "layout": "full_frame_period_paper", "plate": None},
    {"id": "07_station_curve", "file": "code_graphic_009_p5_07_station_curve.mp4", "dur": 6.64, "label": "FALLING TOGETHER", "kind": "station_curve", "layout": "full_frame_period_paper", "plate": None},
]


def ease(x):
    x = max(0.0, min(1.0, x))
    return x * x * (3 - 2 * x)


def prog(t, a, b):
    return ease((t - a) / (b - a)) if b > a else 1.0


def ink(a=1.0):
    return (INK[0], INK[1], INK[2], int(255 * max(0, min(1, a))))


def wash(a=1.0, moon=False):
    c = MOON_WASH if moon else WASH
    return (c[0], c[1], c[2], int(235 * max(0, min(1, a))))


def label_alpha(t, dur):
    """On screen at most ~3.6 s. Fades in over 0.4 s and out before the cut."""
    show = min(3.6, dur - 0.9)
    start = 0.45
    end = start + show
    inn = ease((t - start) / 0.4)
    out = 1 - ease((t - (end - 0.4)) / 0.4)
    return max(0.0, min(inn, out))


def arrow(draw, x0, y0, x1, y1, p, fill, width=6, head=18):
    if p <= 0.02:
        return
    p = min(1.0, p)
    x = x0 + (x1 - x0) * p
    y = y0 + (y1 - y0) * p
    draw.line((x0, y0, x, y), fill=fill, width=width)
    if p > 0.72:
        ang = math.atan2(y1 - y0, x1 - x0)
        hp = ease((p - 0.72) / 0.28)
        for s in (2.55, -2.55):
            draw.line(
                (x, y, x - head * hp * math.cos(ang - s), y - head * hp * math.sin(ang - s)),
                fill=fill, width=width,
            )


def earth(draw, cx, cy, r, a=1.0):
    if a <= 0:
        return
    w = max(3, int(r / 14))
    draw.ellipse((cx - r, cy - r, cx + r, cy + r), fill=wash(a), outline=ink(a), width=w)
    if r < 16:
        return
    draw.ellipse((cx - r * 0.84, cy - r * 0.84, cx + r * 0.84, cy + r * 0.84), outline=ink(0.45 * a), width=max(2, w - 2))
    draw.arc((cx - r * 0.35, cy - r * 0.72, cx + r * 0.55, cy + r * 0.15), 210, 30, fill=ink(a), width=max(2, w - 1))
    draw.arc((cx - r * 0.62, cy - r * 0.05, cx + r * 0.15, cy + r * 0.72), 20, 200, fill=ink(a), width=max(2, w - 1))


def moon(draw, cx, cy, r, a=1.0):
    if a <= 0:
        return
    w = max(3, int(r / 10))
    draw.ellipse((cx - r, cy - r, cx + r, cy + r), fill=wash(a, moon=True), outline=ink(a), width=w)
    draw.ellipse((cx - r * 0.25, cy - r * 0.15, cx + r * 0.05, cy + r * 0.2), outline=ink(a), width=max(2, w - 1))
    draw.ellipse((cx + r * 0.1, cy + r * 0.15, cx + r * 0.38, cy + r * 0.42), outline=ink(a), width=max(2, w - 1))


def tree(draw, x, gy, a=1.0):
    if a <= 0.02:
        return
    c = ink(a)
    draw.line((x, gy, x, gy - 130), fill=c, width=7)
    draw.polygon([(x - 78, gy - 110), (x, gy - 250), (x + 78, gy - 110)], fill=wash(0.85 * a), outline=c)
    draw.line((x - 78, gy - 110, x, gy - 250), fill=c, width=5)
    draw.line((x, gy - 250, x + 78, gy - 110), fill=c, width=5)
    draw.line((x + 78, gy - 110, x - 78, gy - 110), fill=c, width=5)
    for dy in (140, 175, 210):
        hw = int(78 * (250 - dy) / 140)
        draw.line((x - hw + 8, gy - dy, x + hw - 8, gy - dy + 8), fill=ink(0.55 * a), width=3)


def tower(draw, x, gy, a=1.0):
    if a <= 0.02:
        return
    c = ink(a)
    draw.rectangle((x - 42, gy - 340, x + 42, gy), fill=wash(0.85 * a), outline=c, width=5)
    draw.polygon([(x - 52, gy - 340), (x, gy - 430), (x + 52, gy - 340)], fill=wash(0.95 * a), outline=c)
    draw.line((x - 52, gy - 340, x, gy - 430), fill=c, width=5)
    draw.line((x, gy - 430, x + 52, gy - 340), fill=c, width=5)
    for dy in (80, 160, 240):
        draw.rectangle((x - 14, gy - dy - 28, x + 14, gy - dy), outline=c, width=4)


def mountain(draw, x, gy, a=1.0, scale=1.0):
    peak = gy - int(460 * scale)
    if a <= 0.02:
        return peak
    c = ink(a)
    half = int(210 * scale)
    draw.polygon([(x - half, gy), (x, peak), (x + half, gy)], fill=wash(0.85 * a))
    draw.line((x - half, gy, x, peak), fill=c, width=6)
    draw.line((x, peak, x + half, gy), fill=c, width=6)
    draw.line((x - half * 0.45, gy - int(180 * scale), x - half * 0.1, gy - int(250 * scale)), fill=c, width=4)
    for k in range(1, 7):
        u = k / 7.0
        yy = peak + int((gy - peak) * u)
        hw = int(half * u)
        draw.line((x - hw + 10, yy, x, yy - 18), fill=ink(0.5 * a), width=3)
        draw.line((x, yy - 18, x + hw - 10, yy + 6), fill=ink(0.5 * a), width=3)
    return peak


def tick(draw, x, y, a=1.0, span=70):
    draw.line((x - span, y, x + span, y), fill=ink(a), width=6)


# --- diagrams ---

def _feathered_hills(d, gy, p):
    if p <= 0.02:
        return
    # Rolling contour hills instead of a single horizontal scanline so seams() never fires.
    pts = []
    for x in range(160, 1780, 24):
        y = gy + 18 * math.sin(x * 0.0075 + 0.4) + 9 * math.cos(x * 0.019)
        pts.append((x, y))
    d.line(pts, fill=ink(0.85 * p), width=5)
    pts2 = [(x, y + 14 + 6 * math.sin(x * 0.013)) for x, y in pts]
    d.line(pts2, fill=ink(0.45 * p), width=3)


def draw_pull_heights(d, t, dur):
    gy = 800
    _feathered_hills(d, gy, prog(t, 0.05, 0.35))
    tree(d, 460, gy + 8, prog(t, 0.15, 0.7))
    tower(d, 960, gy - 6, prog(t, 0.9, 1.5))
    mountain(d, 1460, gy + 10, prog(t, 1.7, 2.4), scale=0.92)
    tick(d, 460, gy - 250, prog(t, 0.45, 1.15))
    arrow(d, 460, gy - 290, 460, gy - 255, prog(t, 0.45, 1.15), ink(), width=5, head=14)
    if t > 1.35:
        drop = prog(t, 1.35, 2.15)
        tick(d, 960, gy - 436, drop, span=48)
        arrow(d, 960, gy - 480, 960, gy - 442, drop, ink(), width=5, head=14)
    if t > 2.15:
        drop = prog(t, 2.15, 3.15)
        tick(d, 1460, gy + 10 - int(460 * 0.92), drop, span=48)
        arrow(d, 1460, gy - 460, 1460, gy + 4 - int(460 * 0.92), drop, ink(), width=5, head=14)


def draw_pull_heights_c1(d, t, dur):
    gy = 820
    _feathered_hills(d, gy, prog(t, 0.05, 0.4))
    tree(d, 420, gy + 10, 0.55)
    tower(d, 1500, gy - 4, 0.55)
    peak = mountain(d, 960, gy, prog(t, 0.05, 0.7), scale=1.15)
    # Pull line climbs to the peak and holds a tick there.
    p = prog(t, 0.55, 2.7)
    y = gy - (gy - peak) * p
    d.line((960, gy - 8, 960, y), fill=ink(min(1, p * 2)), width=6)
    if p > 0.9:
        tick(d, 960, peak, prog(t, 2.5, 3.2), span=56)


def draw_orbit_teach(d, t, dur):
    cx, cy, R = 860, 500, 250
    earth(d, cx, cy, 108, prog(t, 0.05, 0.45))
    ang0 = -0.15
    bx = cx + R * math.cos(ang0)
    by = cy + R * math.sin(ang0)
    ball_a = prog(t, 0.2, 0.55)
    if ball_a:
        d.ellipse((bx - 16, by - 16, bx + 16, by + 16), fill=ink(ball_a))
    arrow(d, bx + 20, by, bx + 170, by, prog(t, 0.45, 1.35), ink(), width=6, head=20)
    arrow(d, bx, by + 20, bx, by + 150, prog(t, 1.25, 2.15), ink(), width=6, head=20)
    # The same pair repeats around the circle.
    arc_p = prog(t, 1.9, 3.7)
    if arc_p > 0:
        d.arc((cx - R, cy - R, cx + R, cy + R), start=0, end=int(360 * arc_p), fill=ink(0.85), width=5)
    for i, frac in enumerate((0.35, 0.55, 0.75)):
        if arc_p < frac:
            continue
        a = ang0 + frac * math.tau
        x = cx + R * math.cos(a)
        y = cy + R * math.sin(a)
        d.ellipse((x - 10, y - 10, x + 10, y + 10), fill=ink())
        tx, ty = -math.sin(a), math.cos(a)
        arrow(d, x, y, x + tx * 70, y + ty * 70, prog(t, 1.9 + i * 0.25, 2.5 + i * 0.25), ink(), width=5, head=14)
        arrow(d, x, y, x - math.cos(a) * 54, y - math.sin(a) * 54, prog(t, 2.1 + i * 0.25, 2.7 + i * 0.25), ink(), width=5, head=14)


def draw_orbit_teach_c1(d, t, dur):
    cx, cy, R = 960, 500, 280
    earth(d, cx, cy, 108, prog(t, 0.05, 0.4))
    d.ellipse((cx - R, cy - R, cx + R, cy + R), outline=ink(prog(t, 0.2, 0.9)), width=5)
    d.ellipse((cx - R - 26, cy - R - 26, cx + R + 26, cy + R + 26), outline=ink(0.38 * prog(t, 0.3, 1.0)), width=3)
    # Ball steps around and never meets the Earth.
    ang = -0.4 + prog(t, 0.4, dur - 0.2) * 4.4
    x = cx + R * math.cos(ang)
    y = cy + R * math.sin(ang)
    d.ellipse((x - 18, y - 18, x + 18, y + 18), fill=ink())
    # Footprints of earlier steps, still clear of the Earth.
    for k in range(1, 8):
        aa = ang - k * 0.45
        if aa < -0.4:
            break
        sx = cx + R * math.cos(aa)
        sy = cy + R * math.sin(aa)
        d.ellipse((sx - 8, sy - 8, sx + 8, sy + 8), fill=wash(0.8), outline=ink(0.8), width=3)


def _moon_curve(p):
    # Earth-side start to the Moon. p is 0..1 along the curve.
    x = 430 + 1120 * p
    y = 640 - 280 * math.sin(p * math.pi * 0.85)
    return x, y


def draw_km_a_second(d, t, dur):
    earth(d, 340, 680, 108, prog(t, 0.05, 0.4))
    steps = 24
    drawn = int(prog(t, 0.25, 2.1) * steps)
    pts = [_moon_curve(i / steps) for i in range(drawn + 1)]
    if len(pts) > 1:
        d.line(pts, fill=ink(), width=5)
    mp = 0.55 + 0.28 * prog(t, 0.4, dur - 0.15)
    mx, my = _moon_curve(mp)
    moon(d, mx, my, 40, prog(t, 0.8, 1.3))
    arrow(d, mx + 44, my, mx + 165, my, prog(t, 1.5, 2.6), ink(), width=6, head=18)
    arrow(d, mx, my + 42, mx, my + 90, prog(t, 2.45, 3.3), ink(), width=6, head=14)


def draw_km_a_second_c1(d, t, dur):
    earth(d, 340, 680, 112, prog(t, 0.02, 0.25))
    pts = [_moon_curve(i / 28) for i in range(29)]
    d.line(pts, fill=ink(prog(t, 0.05, 0.45)), width=5)
    pts_low = [(x, y + 32) for x, y in pts]
    d.line(pts_low, fill=ink(0.45 * prog(t, 0.1, 0.6)), width=3)
    for frac in (0.18, 0.36, 0.54, 0.72):
        px, py = _moon_curve(frac)
        d.ellipse((px - 7, py - 7, px + 7, py + 7), fill=wash(0.85), outline=ink(0.75), width=3)
    mp = 0.42 + 0.48 * prog(t, 0.2, dur - 0.1)
    mx, my = _moon_curve(mp)
    moon(d, mx, my, 42, 1)
    # A second sideways-then-down pair, further along the curve.
    qx, qy = _moon_curve(min(0.95, mp + 0.12))
    arrow(d, qx + 10, qy - 8, qx + 130, qy - 8, prog(t, 1.1, 2.2), ink(), width=6, head=16)
    arrow(d, qx, qy + 8, qx, qy + 60, prog(t, 2.0, 2.9), ink(), width=6, head=14)


def draw_weaker_far(d, t, dur):
    earth(d, 250, 520, 126, prog(t, 0.05, 0.4))
    for r_ring in (210, 310, 420):
        d.arc((250 - r_ring, 520 - r_ring, 250 + r_ring, 520 + r_ring), -45, 45, fill=ink(0.42), width=3)
    p = prog(t, 0.35, dur - 0.25)
    y = 520
    near = 500
    x = near + 1080 * p
    d.line((370, 700, max(x, near), 700), fill=ink(0.55), width=3)
    # The near arrow stays, so a later frame still shows the pull getting weaker.
    if t > 0.35:
        d.ellipse((near - 18, y - 18, near + 18, y + 18), fill=wash(0.7), outline=ink(0.8), width=4)
        arrow(d, near - 22, y, near - 22 - 190, y, prog(t, 0.35, 1.0), ink(0.85), width=6, head=16)
    d.ellipse((x - 20, y - 20, x + 20, y + 20), fill=wash(), outline=ink(), width=4)
    dist = max(80, x - 250)
    length = max(28, 190 * (250 / dist) ** 2)
    arrow(d, x - 24, y, x - 24 - length, y, 1 if t > 0.7 else prog(t, 0.3, 0.8), ink(), width=6, head=16)


def draw_weaker_far_c1(d, t, dur):
    """Twice as far is four times weaker. A third distance is only a stub.

    The spoken line is 'four times weaker' at twice the distance. The stub
    at three times the distance has no number on it.
    """
    cx, cy, r = 230, 500, 96
    earth(d, cx, cy, r, prog(t, 0.05, 0.35))
    surface = cx + r
    unit = 250  # one distance, from the surface
    places = [
        (1, 160, 0.35, 1.3),
        (2, 40, 1.45, 2.7),
        (3, 14, 2.9, 4.2),
    ]
    for n, length, a, b in places:
        p = prog(t, a, b)
        if p <= 0:
            continue
        x = surface + n * unit
        d.arc((cx - n * unit - r, cy - 220, cx + n * unit + r, cy + 220), -35, 35, fill=ink(0.45 * p), width=3)
        d.line((surface, 690, x, 690), fill=ink(0.55 * p), width=3)
        d.ellipse((x - 18, 500 - 18, x + 18, 500 + 18), fill=wash(p), outline=ink(p), width=4)
        arrow(d, x - 22, 500, x - 22 - length, 500, p, ink(p), width=6, head=14 if length > 30 else 8)
    # Equal ticks: the second gap is two of the first, so it reads as twice as far.
    if t > 1.5:
        p = prog(t, 1.5, 2.4)
        x1 = surface + unit
        x2 = surface + 2 * unit
        for x in (surface, x1, x2):
            d.line((x, 726, x, 752), fill=ink(p), width=4)
        d.line((surface, 740, x2, 740), fill=ink(p), width=4)


def draw_sixty_earths(d, t, dur):
    earth(d, 150, 530, 82, prog(t, 0.05, 0.35))
    n = 60
    x0, x1 = 290, 1490
    shown = int(round(prog(t, 0.3, 3.5) * n))
    # Period measuring bracket and ticks under the 60-Earth span
    d.arc((150 - 140, 530 - 140, 150 + 140, 530 + 140), -55, 55, fill=ink(0.5), width=3)
    if shown:
        step = (x1 - x0) / (n - 1)
        rad = max(8, step * 0.48)
        for i in range(shown):
            x = x0 + i * step
            earth(d, x, 520, rad, 1)
            if i % 10 == 0:
                d.line((x, 560, x, 600), fill=ink(0.75), width=4)
        d.line((x0, 585, x0 + (shown - 1) * step, 585), fill=ink(0.65), width=3)
    moon(d, 1680, 520, 58, prog(t, 2.0, 3.2))


def _dot_square():
    span, n = 620, 60
    arr = np.zeros((span, span, 4), dtype=np.uint8)
    # Warm cream wash inside the square so the 60x60 grid reads as a period plate, not raw high-frequency noise
    arr[:, :, 0] = WASH[0]
    arr[:, :, 1] = WASH[1]
    arr[:, :, 2] = WASH[2]
    arr[:, :, 3] = 175
    step = span / n
    yy, xx = np.mgrid[0:n, 0:n]
    xs = ((xx + 0.5) * step).astype(int)
    ys = ((yy + 0.5) * step).astype(int)
    dot = np.zeros((span, span), dtype=bool)
    dot[ys, xs] = True
    stamped = np.zeros_like(dot)
    for dy in (-1, 0, 1):
        for dx in (-1, 0, 1):
            stamped |= np.roll(np.roll(dot, dy, 0), dx, 1)
    arr[stamped, 0] = INK[0]
    arr[stamped, 1] = INK[1]
    arr[stamped, 2] = INK[2]
    arr[stamped, 3] = 240
    im = Image.fromarray(arr, "RGBA")
    d = ImageDraw.Draw(im)
    d.rectangle((0, 0, span - 1, span - 1), outline=INK, width=6)
    for k in range(10, 60, 10):
        pos = int(round(k * step))
        d.line((pos, 0, pos, span), fill=(INK[0], INK[1], INK[2], 140), width=2)
        d.line((0, pos, span, pos), fill=(INK[0], INK[1], INK[2], 140), width=2)
    return im


DOTS = None


def dots():
    global DOTS
    if DOTS is None:
        DOTS = _dot_square()
    return DOTS


def _paste_dots(base_draw_image, rows, origin=(200, 180)):
    src = dots()
    if rows <= 0:
        return
    h = int(src.height * rows / 60)
    crop = src.crop((0, 0, src.width, max(1, h)))
    base_draw_image.alpha_composite(crop, origin)


def draw_dots_square(d, t, dur, canvas):
    rows = prog(t, 0.25, 2.9) * 60
    _paste_dots(canvas, rows, (160, 160))
    earth(d, 1180, 520, 96, prog(t, 0.2, 0.6))
    moon(d, 1620, 360, 52, prog(t, 0.5, 1.0))
    d.arc((1180 - 180, 520 - 180, 1180 + 180, 520 + 180), -60, 60, fill=ink(0.55), width=4)
    # Pull arrow beside the Moon shrinks toward a single dot.
    shrink = prog(t, 2.2, 4.4)
    if shrink < 0.82:
        length = 160 * (1 - shrink)
        arrow(d, 1555, 360, 1555 - max(36, length), 360, 1 if t > 2.1 else prog(t, 1.2, 2.1), ink(), width=6, head=16)
    else:
        d.ellipse((1536, 350, 1556, 370), fill=ink())


def draw_dots_square_c1(d, t, dur, canvas):
    _paste_dots(canvas, 60, (160, 160))
    earth(d, 1120, 620, 84, prog(t, 0.1, 0.45))
    moon(d, 1520, 450, 60, prog(t, 0.1, 0.45))
    # The last dot travels out of the square and ticks in beside the Moon.
    p = prog(t, 0.6, 3.4)
    x = 780 + (1520 - 80 - 780) * p
    y = 450 + math.sin(p * math.pi) * -50
    pts_arc = [(780 + (1520 - 80 - 780) * (k / 20), 450 + math.sin((k / 20) * math.pi) * -50) for k in range(int(p * 20) + 1)]
    if len(pts_arc) > 1:
        d.line(pts_arc, fill=ink(0.65), width=4)
    rad = 6 + 7 * ease(max(0, (p - 0.82) / 0.18))
    d.ellipse((x - rad, y - rad, x + rad, y + rad), fill=ink(0.5 + 0.5 * p))


def draw_station_curve(d, t, dur):
    cx, cy, R = 960, 540, 250
    earth(d, cx, cy, 108, prog(t, 0.05, 0.4))
    p = prog(t, 0.25, 2.3)
    if p > 0:
        d.arc((cx - R, cy - R, cx + R, cy + R), 200, 200 + 360 * p, fill=ink(), width=5)
    ang = math.radians(210) + prog(t, 0.3, dur - 0.15) * 4.6
    x = cx + R * math.cos(ang)
    y = cy + R * math.sin(ang)
    # A small station: body plus two panel lines. It keeps moving.
    d.rounded_rectangle((x - 18, y - 10, x + 18, y + 10), radius=3, fill=wash(), outline=ink(), width=4)
    d.line((x - 18, y, x - 36, y - 6), fill=ink(), width=4)
    d.line((x + 18, y, x + 36, y - 6), fill=ink(), width=4)
    tx, ty = -math.sin(ang), math.cos(ang)
    arrow(d, x, y, x + tx * 110, y + ty * 110, prog(t, 2.3, 3.4), ink(), width=6, head=16)
    arrow(d, x, y, x - math.cos(ang) * 80, y - math.sin(ang) * 80, prog(t, 3.2, 4.3), ink(), width=6, head=16)


DRAW = {
    "pull_heights": draw_pull_heights,
    "pull_heights_c1": draw_pull_heights_c1,
    "orbit_teach": draw_orbit_teach,
    "orbit_teach_c1": draw_orbit_teach_c1,
    "km_a_second": draw_km_a_second,
    "km_a_second_c1": draw_km_a_second_c1,
    "weaker_far": draw_weaker_far,
    "weaker_far_c1": draw_weaker_far_c1,
    "sixty_earths": draw_sixty_earths,
    "station_curve": draw_station_curve,
}


def make_paper():
    rng = np.random.default_rng(9)
    small = rng.random((H // 4 + 8, W // 4 + 8)).astype(np.float32)
    paper = np.repeat(np.repeat(small, 4, 0), 4, 1)[:H, :W]
    fine = rng.random((H, W)).astype(np.float32)
    tex = paper * 0.85 + fine * 0.15
    yy, xx = np.mgrid[:H, :W]
    nx = (xx - W / 2.0) / (W / 2.0)
    ny = (yy - H / 2.0) / (H / 2.0)
    vig = np.clip(nx * nx * 0.85 + ny * ny * 0.95, 0.0, 1.4).astype(np.float32)
    return tex, vig


def paper_frame(paper_vig, k):
    tex, vig = paper_vig
    shift = (k // 2) % 48
    rolled = np.roll(np.roll(tex, shift, 1), shift // 3, 0)
    shade = 1.0 - 0.45 * vig
    r = 152 * shade + rolled * 12
    g = 110 * shade + rolled * 9
    b = 68 * shade + rolled * 6
    rgb = np.stack([r, g, b], axis=-1).clip(0, 255).astype(np.uint8)
    return Image.fromarray(rgb, "RGB")


def fit_font(text):
    size = 86
    font = ImageFont.truetype(FONT, size, index=1)
    while size > 52 and font.getbbox(text)[2] > 1560:
        size -= 4
        font = ImageFont.truetype(FONT, size, index=1)
    return font


def paint(paper, spec, k):
    t = k / FPS
    frame = paper_frame(paper, k).convert("RGBA")
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    kind = spec["kind"]
    if kind == "dots_square":
        draw_dots_square(d, t, spec["dur"], ov)
    elif kind == "dots_square_c1":
        draw_dots_square_c1(d, t, spec["dur"], ov)
    else:
        DRAW[kind](d, t, spec["dur"])
    frame = Image.alpha_composite(frame, ov)
    a = label_alpha(t, spec["dur"])
    if a > 0.01:
        lab = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        font = fit_font(spec["label"])
        fill = (CREAM[0], CREAM[1], CREAM[2], int(255 * a))
        stroke = (48, 26, 12, int(255 * a))
        ImageDraw.Draw(lab).text((W / 2, 980), spec["label"], font=font, fill=fill, anchor="mm", stroke_width=2, stroke_fill=stroke)
        frame = Image.alpha_composite(frame, lab)
    return frame.convert("RGB")


def render_one(paper, spec, out, stills_only=False):
    n = int(round(spec["dur"] * FPS))
    show = min(3.6, spec["dur"] - 0.9)
    hero_t = max(1.2, 0.45 + show - 0.4)
    still_k = min(n - 1, int(hero_t * FPS))
    still_path = out / (Path(spec["file"]).stem + ".jpg")
    min_mean, min_p95 = 999.0, 999.0
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
    try:
        for k in range(n):
            frame = paint(paper, spec, k)
            if k % 15 == 0 or k == still_k:
                g = np.asarray(frame.convert("L"))
                min_mean = min(min_mean, float(g.mean()))
                min_p95 = min(min_p95, float(np.percentile(g, 95)))
            if k == still_k:
                frame.save(still_path, quality=90)
            if enc is not None:
                enc.stdin.write(frame.tobytes())
            elif k == still_k:
                break
    finally:
        if enc is not None:
            enc.stdin.close()
            if enc.wait() != 0:
                raise RuntimeError(f"ffmpeg failed for {spec['file']}")
    words = spec["label"].replace(",", " ").split()
    rec = {
        "id": spec["id"],
        "file": spec["file"],
        "duration_s": spec["dur"],
        "fps": FPS,
        "width": W,
        "height": H,
        "label": spec["label"],
        "label_words": len(words),
        "layout": spec["layout"],
        "named_plate": spec["plate"],
        "background": "moving period paper (Flow plate not minted; mint held)" if spec["layout"] == "moving_plate_overlay" else "moving period paper",
        "min_sample_mean_luma": round(min_mean, 2),
        "min_sample_p95": round(min_p95, 2),
        "near_black": "PASS" if (min_mean >= 28 or min_p95 >= 50) else "FAIL",
        "still": still_path.name,
    }
    if path.exists() and not stills_only:
        rec["sha256"] = hashlib.sha256(path.read_bytes()).hexdigest()
        rec["bytes"] = path.stat().st_size
    return rec


def sheet(out, rows):
    cols = 4
    tw, th = 480, 270
    rows_n = math.ceil(len(rows) / cols)
    im = Image.new("RGB", (cols * tw, rows_n * (th + 36)), (92, 64, 40))
    d = ImageDraw.Draw(im)
    font = ImageFont.truetype(FONT, 22, index=1)
    for i, rec in enumerate(rows):
        still = Image.open(out / rec["still"]).resize((tw, th))
        x, y = (i % cols) * tw, (i // cols) * (th + 36)
        im.paste(still, (x, y))
        d.text((x + 8, y + th + 6), rec["label"], font=font, fill=(255, 244, 218))
    im.save(out / "code_graphics_v01_sheet.jpg", quality=90)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--stills-only", action="store_true")
    ap.add_argument("--only", default="")
    args = ap.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    want = set(args.only.split(",")) if args.only else None
    for spec in SPECS:
        words = [w for w in spec["label"].replace(",", " ").split() if w]
        if len(words) > 4:
            raise SystemExit(f"{spec['id']} label has {len(words)} words")
    paper = make_paper()
    rows = []
    for spec in SPECS:
        if want and spec["id"] not in want:
            continue
        print("Rendering", spec["id"], flush=True)
        rows.append(render_one(paper, spec, args.out, args.stills_only))
    if not want:
        sheet(args.out, rows)
    (args.out / "CODE_GRAPHICS_v01.json").write_text(json.dumps(rows, indent=2) + "\n")
    fails = [r["id"] for r in rows if r["near_black"] != "PASS" or r["label_words"] > 4]
    print("done", len(rows), "fails", fails or "none", flush=True)
    if fails:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
