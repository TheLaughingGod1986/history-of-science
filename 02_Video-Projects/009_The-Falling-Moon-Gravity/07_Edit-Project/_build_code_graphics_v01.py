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
INK = (62, 34, 16, 255)
CREAM = (255, 244, 218, 255)
WASH = (168, 122, 78, 255)
MOON_WASH = (196, 174, 138, 255)

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
    return (c[0], c[1], c[2], int(230 * max(0, min(1, a))))


def label_alpha(t, dur):
    """On screen at most ~3.6 s. Fades in over 0.4 s and out before the cut."""
    show = min(3.6, dur - 0.9)
    start = 0.45
    end = start + show
    inn = ease((t - start) / 0.4)
    out = 1 - ease((t - (end - 0.4)) / 0.4)
    return max(0.0, min(inn, out))


def arrow(draw, x0, y0, x1, y1, p, fill, width=5, head=18):
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
    w = max(2, int(r / 16))
    draw.ellipse((cx - r, cy - r, cx + r, cy + r), fill=wash(a), outline=ink(a), width=w)
    if r < 16:
        return
    draw.arc((cx - r * 0.35, cy - r * 0.72, cx + r * 0.55, cy + r * 0.15), 210, 30, fill=ink(a), width=max(2, w - 1))
    draw.arc((cx - r * 0.62, cy - r * 0.05, cx + r * 0.15, cy + r * 0.72), 20, 200, fill=ink(a), width=max(2, w - 1))


def moon(draw, cx, cy, r, a=1.0):
    if a <= 0:
        return
    w = max(2, int(r / 12))
    draw.ellipse((cx - r, cy - r, cx + r, cy + r), fill=wash(a, moon=True), outline=ink(a), width=w)
    draw.ellipse((cx - r * 0.25, cy - r * 0.15, cx + r * 0.05, cy + r * 0.2), outline=ink(a), width=max(1, w - 1))
    draw.ellipse((cx + r * 0.1, cy + r * 0.15, cx + r * 0.38, cy + r * 0.42), outline=ink(a), width=max(1, w - 1))


def tree(draw, x, gy, a=1.0):
    c = ink(a)
    draw.line((x, gy, x, gy - 130), fill=c, width=6)
    draw.polygon([(x - 78, gy - 110), (x, gy - 250), (x + 78, gy - 110)], outline=c)
    draw.line((x - 78, gy - 110, x, gy - 250), fill=c, width=4)
    draw.line((x, gy - 250, x + 78, gy - 110), fill=c, width=4)
    draw.line((x + 78, gy - 110, x - 78, gy - 110), fill=c, width=4)


def tower(draw, x, gy, a=1.0):
    c = ink(a)
    draw.rectangle((x - 40, gy - 340, x + 40, gy), outline=c, width=4)
    draw.line((x - 52, gy - 340, x, gy - 430), fill=c, width=4)
    draw.line((x, gy - 430, x + 52, gy - 340), fill=c, width=4)
    for dy in (80, 160, 240):
        draw.rectangle((x - 12, gy - dy - 28, x + 12, gy - dy), outline=c, width=3)


def mountain(draw, x, gy, a=1.0, scale=1.0):
    c = ink(a)
    peak = gy - int(460 * scale)
    half = int(210 * scale)
    draw.line((x - half, gy, x, peak), fill=c, width=5)
    draw.line((x, peak, x + half, gy), fill=c, width=5)
    draw.line((x - half * 0.45, gy - int(180 * scale), x - half * 0.1, gy - int(250 * scale)), fill=c, width=3)
    return peak


def tick(draw, x, y, a=1.0, span=70):
    draw.line((x - span, y, x + span, y), fill=ink(a), width=5)


# --- diagrams ---

def draw_pull_heights(d, t, dur):
    gy = 800
    d.line((180, gy, 1740, gy), fill=ink(prog(t, 0.05, 0.35)), width=3)
    tree(d, 460, gy, prog(t, 0.15, 0.7))
    tower(d, 960, gy, prog(t, 0.9, 1.5))
    mountain(d, 1460, gy, prog(t, 1.7, 2.4), scale=0.92)
    tick(d, 460, gy - 250, prog(t, 0.45, 1.15))
    if t > 1.35:
        drop = prog(t, 1.35, 2.15)
        tick(d, 960, gy - 430, drop, span=48)
    if t > 2.15:
        drop = prog(t, 2.15, 3.15)
        tick(d, 1460, gy - int(460 * 0.92), drop, span=48)


def draw_pull_heights_c1(d, t, dur):
    gy = 820
    peak = mountain(d, 960, gy, prog(t, 0.05, 0.7), scale=1.15)
    # Pull line climbs to the peak and holds a tick there.
    p = prog(t, 0.55, 2.7)
    y = gy - (gy - peak) * p
    d.line((960, gy - 8, 960, y), fill=ink(min(1, p * 2)), width=5)
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
    arrow(d, bx + 20, by, bx + 170, by, prog(t, 0.45, 1.35), ink(), width=5, head=20)
    arrow(d, bx, by + 20, bx, by + 150, prog(t, 1.25, 2.15), ink(), width=5, head=20)
    # The same pair repeats around the circle.
    arc_p = prog(t, 1.9, 3.7)
    if arc_p > 0:
        d.arc((cx - R, cy - R, cx + R, cy + R), start=0, end=int(360 * arc_p), fill=ink(0.85), width=4)
    for i, frac in enumerate((0.35, 0.55, 0.75)):
        if arc_p < frac:
            continue
        a = ang0 + frac * math.tau
        x = cx + R * math.cos(a)
        y = cy + R * math.sin(a)
        d.ellipse((x - 8, y - 8, x + 8, y + 8), fill=ink())
        tx, ty = -math.sin(a), math.cos(a)
        arrow(d, x, y, x + tx * 70, y + ty * 70, prog(t, 1.9 + i * 0.25, 2.5 + i * 0.25), ink(), width=4, head=14)
        arrow(d, x, y, x - math.cos(a) * 54, y - math.sin(a) * 54, prog(t, 2.1 + i * 0.25, 2.7 + i * 0.25), ink(), width=4, head=14)


def draw_orbit_teach_c1(d, t, dur):
    cx, cy, R = 960, 500, 280
    earth(d, cx, cy, 100, prog(t, 0.05, 0.4))
    d.ellipse((cx - R, cy - R, cx + R, cy + R), outline=ink(prog(t, 0.2, 0.9)), width=4)
    # Ball steps around and never meets the Earth.
    ang = -0.4 + prog(t, 0.4, dur - 0.2) * 4.4
    x = cx + R * math.cos(ang)
    y = cy + R * math.sin(ang)
    d.ellipse((x - 16, y - 16, x + 16, y + 16), fill=ink())
    # Footprints of earlier steps, still clear of the Earth.
    for k in range(1, 5):
        aa = ang - k * 0.55
        if aa < -0.4:
            break
        sx = cx + R * math.cos(aa)
        sy = cy + R * math.sin(aa)
        d.ellipse((sx - 6, sy - 6, sx + 6, sy + 6), outline=ink(0.7), width=2)


def _moon_curve(p):
    # Earth-side start to the Moon. p is 0..1 along the curve.
    x = 430 + 1120 * p
    y = 640 - 280 * math.sin(p * math.pi * 0.85)
    return x, y


def draw_km_a_second(d, t, dur):
    earth(d, 340, 680, 96, prog(t, 0.05, 0.4))
    steps = 24
    drawn = int(prog(t, 0.25, 2.1) * steps)
    pts = [_moon_curve(i / steps) for i in range(drawn + 1)]
    if len(pts) > 1:
        d.line(pts, fill=ink(), width=4)
    mp = 0.55 + 0.28 * prog(t, 0.4, dur - 0.15)
    mx, my = _moon_curve(mp)
    moon(d, mx, my, 34, prog(t, 0.8, 1.3))
    arrow(d, mx + 40, my, mx + 150, my, prog(t, 1.5, 2.6), ink(), width=5, head=18)
    arrow(d, mx, my + 36, mx, my + 78, prog(t, 2.45, 3.3), ink(), width=5, head=14)


def draw_km_a_second_c1(d, t, dur):
    earth(d, 340, 680, 96, prog(t, 0.02, 0.25))
    pts = [_moon_curve(i / 28) for i in range(29)]
    d.line(pts, fill=ink(prog(t, 0.05, 0.45)), width=4)
    mp = 0.42 + 0.48 * prog(t, 0.2, dur - 0.1)
    mx, my = _moon_curve(mp)
    moon(d, mx, my, 34, 1)
    # A second sideways-then-down pair, further along the curve.
    qx, qy = _moon_curve(min(0.95, mp + 0.12))
    arrow(d, qx + 10, qy - 8, qx + 120, qy - 8, prog(t, 1.1, 2.2), ink(), width=5, head=16)
    arrow(d, qx, qy + 8, qx, qy + 52, prog(t, 2.0, 2.9), ink(), width=5, head=14)


def draw_weaker_far(d, t, dur):
    earth(d, 250, 520, 120, prog(t, 0.05, 0.4))
    p = prog(t, 0.35, dur - 0.25)
    y = 520
    near = 500
    x = near + 1080 * p
    d.line((370, 700, max(x, near), 700), fill=ink(0.45), width=2)
    # The near arrow stays, so a later frame still shows the pull getting weaker.
    if t > 0.35:
        d.ellipse((near - 16, y - 16, near + 16, y + 16), outline=ink(0.7), width=3)
        arrow(d, near - 22, y, near - 22 - 190, y, prog(t, 0.35, 1.0), ink(0.75), width=5, head=16)
    d.ellipse((x - 18, y - 18, x + 18, y + 18), fill=wash(), outline=ink(), width=3)
    dist = max(80, x - 250)
    length = max(28, 190 * (250 / dist) ** 2)
    arrow(d, x - 24, y, x - 24 - length, y, 1 if t > 0.7 else prog(t, 0.3, 0.8), ink(), width=5, head=16)


def draw_weaker_far_c1(d, t, dur):
    """Twice as far is four times weaker. A third distance is only a stub.

    The spoken line is 'four times weaker' at twice the distance. The stub
    at three times the distance has no number on it.
    """
    cx, cy, r = 230, 500, 78
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
        d.line((surface, 690, x, 690), fill=ink(0.4 * p), width=2)
        d.ellipse((x - 16, 500 - 16, x + 16, 500 + 16), fill=wash(p), outline=ink(p), width=3)
        arrow(d, x - 22, 500, x - 22 - length, 500, p, ink(p), width=5, head=14 if length > 30 else 8)
    # Equal ticks: the second gap is two of the first, so it reads as twice as far.
    if t > 1.5:
        p = prog(t, 1.5, 2.4)
        x1 = surface + unit
        x2 = surface + 2 * unit
        for x in (surface, x1, x2):
            d.line((x, 730, x, 748), fill=ink(p), width=3)
        d.line((surface, 740, x2, 740), fill=ink(p), width=3)


def draw_sixty_earths(d, t, dur):
    earth(d, 150, 530, 62, prog(t, 0.05, 0.35))
    n = 60
    x0, x1 = 280, 1480
    shown = int(round(prog(t, 0.3, 3.5) * n))
    if shown:
        step = (x1 - x0) / (n - 1)
        rad = max(6, step * 0.46)
        for i in range(shown):
            x = x0 + i * step
            earth(d, x, 520, rad, 1)
    moon(d, 1680, 520, 46, prog(t, 3.2, 4.0))


def _dot_square():
    span, n = 620, 60
    im = Image.new("RGBA", (span, span), (0, 0, 0, 0))
    arr = np.zeros((span, span, 4), dtype=np.uint8)
    step = span / n
    yy, xx = np.mgrid[0:n, 0:n]
    xs = ((xx + 0.5) * step).astype(int)
    ys = ((yy + 0.5) * step).astype(int)
    arr[ys, xs, 0] = INK[0]
    arr[ys, xs, 1] = INK[1]
    arr[ys, xs, 2] = INK[2]
    arr[ys, xs, 3] = 255
    # 3x3 stamp so the dots read at full frame.
    stamped = np.zeros_like(arr)
    for dy in (-1, 0, 1):
        for dx in (-1, 0, 1):
            stamped = np.maximum(stamped, np.roll(np.roll(arr, dy, 0), dx, 1))
    return Image.fromarray(stamped, "RGBA")


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
    earth(d, 1180, 520, 70, prog(t, 0.2, 0.6))
    moon(d, 1620, 360, 36, prog(t, 0.5, 1.0))
    # Pull arrow beside the Moon shrinks toward a single dot.
    shrink = prog(t, 2.2, 4.4)
    if shrink < 0.82:
        length = 160 * (1 - shrink)
        arrow(d, 1570, 360, 1570 - max(36, length), 360, 1 if t > 2.1 else prog(t, 1.2, 2.1), ink(), width=5, head=16)
    else:
        d.ellipse((1546, 352, 1562, 368), fill=ink())


def draw_dots_square_c1(d, t, dur, canvas):
    _paste_dots(canvas, 60, (160, 160))
    moon(d, 1500, 470, 48, prog(t, 0.1, 0.45))
    # The last dot travels out of the square and ticks in beside the Moon.
    p = prog(t, 0.6, 3.4)
    x = 780 + (1500 - 70 - 780) * p
    y = 470 + math.sin(p * math.pi) * -30
    rad = 4 + 6 * ease(max(0, (p - 0.82) / 0.18))
    d.ellipse((x - rad, y - rad, x + rad, y + rad), fill=ink(0.3 + 0.7 * p))


def draw_station_curve(d, t, dur):
    cx, cy, R = 960, 540, 250
    earth(d, cx, cy, 92, prog(t, 0.05, 0.4))
    p = prog(t, 0.25, 2.3)
    if p > 0:
        d.arc((cx - R, cy - R, cx + R, cy + R), 200, 200 + 360 * p, fill=ink(), width=5)
    ang = math.radians(210) + prog(t, 0.3, dur - 0.15) * 4.6
    x = cx + R * math.cos(ang)
    y = cy + R * math.sin(ang)
    # A small station: body plus two panel lines. It keeps moving.
    d.rounded_rectangle((x - 16, y - 8, x + 16, y + 8), radius=3, outline=ink(), width=3)
    d.line((x - 16, y, x - 32, y - 6), fill=ink(), width=3)
    d.line((x + 16, y, x + 32, y - 6), fill=ink(), width=3)
    tx, ty = -math.sin(ang), math.cos(ang)
    arrow(d, x, y, x + tx * 110, y + ty * 110, prog(t, 2.3, 3.4), ink(), width=5, head=16)
    arrow(d, x, y, x - math.cos(ang) * 80, y - math.sin(ang) * 80, prog(t, 3.2, 4.3), ink(), width=5, head=16)


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
    # A second finer grain so flat areas don't band.
    fine = rng.random((H, W)).astype(np.float32)
    return paper * 0.85 + fine * 0.15


def paper_frame(paper, k):
    shift = (k // 2) % 48
    rolled = np.roll(np.roll(paper, shift, 1), shift // 3, 0)
    r = 112 + rolled * 42
    g = 74 + rolled * 30
    b = 42 + rolled * 18
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
