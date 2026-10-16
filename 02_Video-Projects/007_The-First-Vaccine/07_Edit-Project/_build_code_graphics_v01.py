"""J0344: HOS 007 three £0 code graphics from plate boards v02.

P1:07_map_shadows, P4:11_news_spreads, P5:08_body_learns.
House explainer: dark-sepia ink on moving period paper. No Flow, no Vertex,
no audio, no place names. Map side labels are added in the edit.
"""
import argparse, hashlib, json, math, subprocess as sp
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont

W, H, FPS = 1920, 1080, 30
FONT = "/System/Library/Fonts/Supplemental/Didot.ttc"
INK = (62, 34, 16, 255)
CREAM = (255, 244, 218, 255)
WASH = (176, 132, 86, 255)
SHADOW = (92, 84, 76, 255)

def _chaikin(pts, iters=1):
    for _ in range(iters):
        nxt = []
        n = len(pts)
        for i in range(n):
            a, b = pts[i], pts[(i + 1) % n]
            nxt.append((0.75 * a[0] + 0.25 * b[0], 0.75 * a[1] + 0.25 * b[1]))
            nxt.append((0.25 * a[0] + 0.75 * b[0], 0.25 * a[1] + 0.75 * b[1]))
        pts = nxt
    return pts


# Outer coasts only, then one smooth pass. Cornwall, Wales and the Channel stay readable.
# Not a traced atlas, and no names are drawn.
BRITAIN = _chaikin([
    (700, 70), (780, 100), (750, 170), (830, 220), (780, 310),
    (860, 390), (820, 470), (920, 530), (830, 580), (890, 640),
    (800, 700), (700, 720), (600, 690), (490, 770), (560, 660),
    (500, 580), (440, 500), (530, 430), (470, 330), (560, 240),
    (500, 150), (610, 90),
])
IRELAND = _chaikin([
    (250, 300), (340, 270), (410, 330), (420, 430),
    (360, 530), (270, 540), (190, 460), (180, 350),
])
EUROPE = _chaikin([
    (1040, 640), (1140, 550), (1280, 510), (1440, 540), (1580, 620),
    (1680, 720), (1600, 820), (1700, 910), (1540, 980), (1380, 900),
    (1220, 1000), (1080, 930), (980, 820), (1040, 720), (990, 670),
])
# Unmarked towns on the land. Names stay in code only.
TOWNS = {
    "se": (760, 650),
    "north": (690, 180),
    "west": (530, 520),
    "mid": (740, 430),
    "low": (1200, 580),
    "inland": (1380, 700),
    "south": (1240, 900),
    "isle": (300, 420),
}
SHADOW_PAIRS = (("se", "north"), ("west", "mid"), ("low", "inland"), ("inland", "south"), ("se", "low"))

SPECS = [
    {
        "id": "07_map_shadows",
        "file": "code_graphic_007_p1_07_map_shadows.mp4",
        "dur": 5.96,
        "label": None,
        "kind": "map_shadows",
    },
    {
        "id": "11_news_spreads",
        "file": "code_graphic_007_p4_11_news_spreads.mp4",
        "dur": 6.42,
        "label": None,
        "kind": "news_spreads",
    },
    {
        "id": "08_body_learns",
        "file": "code_graphic_007_p5_08_body_learns.mp4",
        "dur": 6.08,
        "label": "THE BODY LEARNS",
        "kind": "body_learns",
    },
]


def ease(x):
    x = max(0.0, min(1.0, x))
    return x * x * (3 - 2 * x)


def prog(t, a, b):
    return ease((t - a) / (b - a)) if b > a else 1.0


def ink(a=1.0):
    return (INK[0], INK[1], INK[2], int(255 * max(0, min(1, a))))


def wash(a=1.0):
    return (WASH[0], WASH[1], WASH[2], int(150 * max(0, min(1, a))))


def shadow(a=1.0):
    return (SHADOW[0], SHADOW[1], SHADOW[2], int(88 * max(0, min(1, a))))


def close(pts):
    return pts + [pts[0]]


def path_len(pts):
    return sum(math.hypot(b[0] - a[0], b[1] - a[1]) for a, b in zip(pts, pts[1:]))


def point_at(pts, dist):
    for a, b in zip(pts, pts[1:]):
        L = math.hypot(b[0] - a[0], b[1] - a[1])
        if dist <= L or L == 0:
            t = 0 if L == 0 else dist / L
            return (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)
        dist -= L
    return pts[-1]


def stroke(draw, pts, p, fill, width):
    if p <= 0.01 or len(pts) < 2:
        return
    total = path_len(pts)
    remain = total * min(1.0, p)
    for a, b in zip(pts, pts[1:]):
        L = math.hypot(b[0] - a[0], b[1] - a[1])
        if remain <= 0:
            return
        if remain >= L - 0.1:
            draw.line((a[0], a[1], b[0], b[1]), fill=fill, width=width)
            remain -= L
        else:
            t = remain / L if L else 0
            draw.line((a[0], a[1], a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t), fill=fill, width=width)
            return


def land(draw, pts, p, width=5):
    if p > 0.92:
        draw.polygon(pts, fill=wash(min(1.0, (p - 0.92) / 0.08)))
    stroke(draw, close(pts), p, ink(min(1.0, p * 1.4)), width)


def town(draw, xy, a):
    if a <= 0.02:
        return
    x, y = xy
    c = ink(a)
    r = 7
    draw.ellipse((x - r, y - r, x + r, y + r), outline=c, width=3)
    draw.ellipse((x - 2, y - 2, x + 2, y + 2), fill=c)


def drift(a, b, t, phase):
    u = 0.5 + 0.42 * math.sin(t * 0.55 + phase)
    return (a[0] + (b[0] - a[0]) * u, a[1] + (b[1] - a[1]) * u)


def shadows(draw, t, a):
    if a <= 0.02:
        return
    for i, (p, q) in enumerate(SHADOW_PAIRS):
        x, y = drift(TOWNS[p], TOWNS[q], t, i * 1.3)
        rx, ry = 78 + 10 * math.sin(t * 0.4 + i), 36 + 6 * math.cos(t * 0.5 + i)
        draw.ellipse((x - rx, y - ry, x + rx, y + ry), fill=shadow(a))


def coast(draw, t, already=False):
    if already:
        bp = ip = ep = 1.0
    else:
        bp = prog(t, 0.05, 1.45)
        ip = prog(t, 0.55, 1.7)
        ep = prog(t, 0.85, 2.15)
    land(draw, BRITAIN, bp, width=6)
    land(draw, IRELAND, ip, width=5)
    land(draw, EUROPE, ep, width=6)
    # Short wave marks in the channel only, so the gap reads as water.
    sea = 1.0 if already else prog(t, 1.9, 2.5)
    if sea > 0:
        c = ink(0.28 * sea)
        for y0 in (560, 640, 720):
            stroke(draw, [(860, y0), (910, y0 - 14), (960, y0 + 6), (1005, y0 - 8)], sea, c, 2)
    ta = 1.0 if already else prog(t, 1.7, 2.3)
    for key in TOWNS:
        town(draw, TOWNS[key], ta)
    return bp


def rider(draw, x, y, a):
    c = ink(a)
    draw.ellipse((x - 22, y - 8, x + 18, y + 10), outline=c, width=3)
    draw.line((x - 12, y + 8, x - 18, y + 22), fill=c, width=3)
    draw.line((x + 10, y + 8, x + 18, y + 22), fill=c, width=3)
    draw.line((x - 2, y - 8, x - 2, y - 22), fill=c, width=3)
    draw.ellipse((x - 8, y - 34, x + 4, y - 22), outline=c, width=3)
    book(draw, x + 22, y - 18, a)


def coach(draw, x, y, a):
    c = ink(a)
    draw.rounded_rectangle((x - 26, y - 14, x + 20, y + 6), radius=3, outline=c, width=3)
    draw.ellipse((x - 16, y + 2, x - 4, y + 14), outline=c, width=3)
    draw.ellipse((x + 6, y + 2, x + 18, y + 14), outline=c, width=3)
    book(draw, x + 2, y - 26, a)


def ship(draw, x, y, a):
    c = ink(a)
    draw.polygon([(x - 28, y), (x + 22, y), (x + 10, y + 14), (x - 16, y + 14)], outline=c)
    draw.line((x - 28, y, x + 22, y), fill=c, width=3)
    draw.line((x - 16, y + 14, x + 10, y + 14), fill=c, width=3)
    draw.line((x, y, x, y - 28), fill=c, width=3)
    draw.line((x, y - 22, x + 18, y - 8), fill=c, width=3)
    book(draw, x + 24, y - 10, a)


def book(draw, x, y, a):
    c = ink(a)
    draw.rectangle((x - 8, y - 10, x + 8, y + 10), outline=c, width=2)
    draw.line((x, y - 10, x, y + 10), fill=c, width=2)


CARRIERS = [
    ("rider", [TOWNS["se"], TOWNS["mid"], TOWNS["north"]], 0.2),
    ("coach", [TOWNS["se"], (940, 660), TOWNS["low"], TOWNS["inland"]], 0.35),
    ("ship", [(620, 760), (360, 800), (80, 840)], 0.55),
    ("coach", [TOWNS["low"], TOWNS["south"]], 1.15),
    ("rider", [TOWNS["west"], TOWNS["isle"]], 1.45),
    ("rider", [TOWNS["se"], TOWNS["mid"], TOWNS["north"]], 3.15),
    ("ship", [(700, 740), (300, 790), (40, 830)], 3.4),
    ("coach", [TOWNS["inland"], (1600, 680)], 3.6),
]


def travel(draw, kind, pts, start, t):
    if t < start:
        return
    total = path_len(pts)
    dist = min(total, (t - start) * 210)
    # Keep the last stretch moving: once a carrier arrives, it eases off the end
    # only if the path itself runs off the map. Otherwise it holds the last
    # third in a slow creep so the frame never freezes.
    if dist >= total - 1 and pts[-1][0] > 120:
        dist = total * (0.72 + 0.28 * (0.5 + 0.5 * math.sin((t - start) * 0.8)))
    x, y = point_at(pts, dist)
    a = min(1.0, (t - start) / 0.25)
    {"rider": rider, "coach": coach, "ship": ship}[kind](draw, x, y, a)


def draw_map_shadows(d, t, dur):
    coast(d, t, already=False)
    shadows(d, t, prog(t, 2.4, 3.3))


def draw_news(d, t, dur):
    coast(d, t, already=True)
    shadows(d, t, 0.35)
    for kind, pts, start in CARRIERS:
        travel(d, kind, pts, start, t)
        # A second wave reuses the same roads so motion lasts the whole shot.
        travel(d, kind, pts, start + 2.8, t)


def blob(cx, cy, rx, ry, wobble, phase):
    raw = []
    n = 28
    for i in range(n):
        a = -math.pi / 2 + i * math.tau / n
        w = 1 + wobble * math.sin(i * 1.7 + phase) + 0.5 * wobble * math.sin(i * 3.1 + phase)
        raw.append((cx + rx * w * math.cos(a), cy + ry * w * math.sin(a)))
    return _chaikin(raw, 2)


def draw_body(d, t, dur):
    pulse = 1 + 0.02 * math.sin(t * 1.7)
    ax, ay = 720, 460
    a_pts = blob(ax, ay, 190 * pulse, 230 * pulse, 0.10, 0.6)
    grow = prog(t, 0.15, 1.35)
    if grow > 0.9:
        d.polygon(a_pts, fill=wash(min(1, (grow - 0.9) / 0.1)))
    stroke(d, close(a_pts), grow, ink(), 6)

    meet = prog(t, 1.05, 2.3)
    morph = prog(t, 2.2, 3.9)
    bx = 1320 - 280 * meet
    by = 460 + 8 * math.sin(t * 1.4)
    start = blob(bx, by, 150 * pulse, 180 * pulse, 0.02, 2.4)
    target = blob(1080, 460, 190 * pulse, 230 * pulse, 0.10, 0.6)
    b_pts = [
        (p[0] + (q[0] - p[0]) * morph, p[1] + (q[1] - p[1]) * morph)
        for p, q in zip(start, target)
    ]
    ba = prog(t, 0.95, 1.35)
    if morph > 0.55:
        d.polygon(b_pts, fill=wash(min(1, (morph - 0.55) / 0.35)))
    stroke(d, close(b_pts), ba, ink(ba), 6)


def label_alpha(t, dur):
    show = min(3.6, dur - 0.9)
    start = 2.5
    end = start + show
    inn = ease((t - start) / 0.4)
    out = 1 - ease((t - (end - 0.4)) / 0.4)
    return max(0.0, min(inn, out, 1.0))


DRAW = {
    "map_shadows": draw_map_shadows,
    "news_spreads": draw_news,
    "body_learns": draw_body,
}


def make_paper():
    rng = np.random.default_rng(7)
    small = rng.random((H // 4 + 8, W // 4 + 8)).astype(np.float32)
    paper = np.repeat(np.repeat(small, 4, 0), 4, 1)[:H, :W]
    fine = rng.random((H, W)).astype(np.float32)
    return paper * 0.85 + fine * 0.15


def paper_frame(paper, k):
    shift = (k // 2) % 48
    rolled = np.roll(np.roll(paper, shift, 1), shift // 3, 0)
    r = 118 + rolled * 40
    g = 80 + rolled * 28
    b = 46 + rolled * 16
    rgb = np.stack([r, g, b], axis=-1).clip(0, 255).astype(np.uint8)
    return Image.fromarray(rgb, "RGB")


def fit_font(text):
    size = 78
    font = ImageFont.truetype(FONT, size, index=1)
    while size > 48 and font.getbbox(text)[2] > 1400:
        size -= 4
        font = ImageFont.truetype(FONT, size, index=1)
    return font


def paint(paper, spec, k):
    t = k / FPS
    frame = paper_frame(paper, k).convert("RGBA")
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    DRAW[spec["kind"]](ImageDraw.Draw(ov), t, spec["dur"])
    frame = Image.alpha_composite(frame, ov)
    if spec["label"]:
        a = label_alpha(t, spec["dur"])
        if a > 0.01:
            lab = Image.new("RGBA", (W, H), (0, 0, 0, 0))
            font = fit_font(spec["label"])
            fill = (CREAM[0], CREAM[1], CREAM[2], int(255 * a))
            stroke_c = (48, 26, 12, int(220 * a))
            ImageDraw.Draw(lab).text(
                (W / 2, 960), spec["label"], font=font, fill=fill, anchor="mm",
                stroke_width=2, stroke_fill=stroke_c,
            )
            frame = Image.alpha_composite(frame, lab)
    return frame.convert("RGB")


def render_one(paper, spec, out):
    n = int(round(spec["dur"] * FPS))
    hero_k = int(min(spec["dur"] - 0.4, spec["dur"] * 0.72) * FPS)
    still_path = out / (Path(spec["file"]).stem + ".jpg")
    early_path = out / (Path(spec["file"]).stem + "_early.jpg")
    min_mean, min_p95 = 999.0, 999.0
    path = out / spec["file"]
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
            if k % 15 == 0 or k in (hero_k, int(0.35 * FPS)):
                g = np.asarray(frame.convert("L"))
                min_mean = min(min_mean, float(g.mean()))
                min_p95 = min(min_p95, float(np.percentile(g, 95)))
            if k == int(0.35 * FPS):
                frame.save(early_path, quality=90)
            if k == hero_k:
                frame.save(still_path, quality=90)
            enc.stdin.write(frame.tobytes())
    finally:
        enc.stdin.close()
        if enc.wait() != 0:
            raise RuntimeError(f"ffmpeg failed for {spec['file']}")
    words = spec["label"].split() if spec["label"] else []
    probe = sp.check_output(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)],
        text=True,
    ).strip()
    rec = {
        "id": spec["id"],
        "file": spec["file"],
        "duration_s": spec["dur"],
        "probed_duration_s": round(float(probe), 3),
        "fps": FPS,
        "width": W,
        "height": H,
        "label": spec["label"],
        "label_words": len(words),
        "layout": "full_frame_period_paper",
        "background": "moving period paper",
        "lettering": "none in the map renders" if spec["label"] is None else spec["label"],
        "min_sample_mean_luma": round(min_mean, 2),
        "min_sample_p95": round(min_p95, 2),
        "near_black": "PASS" if (min_mean >= 28 or min_p95 >= 50) else "FAIL",
        "still": still_path.name,
        "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        "bytes": path.stat().st_size,
        "audio": "none",
    }
    return rec


def sheet(out, rows):
    tw, th = 640, 360
    im = Image.new("RGB", (len(rows) * tw, th + 48), (92, 64, 40))
    d = ImageDraw.Draw(im)
    font = ImageFont.truetype(FONT, 28, index=1)
    for i, rec in enumerate(rows):
        still = Image.open(out / rec["still"]).resize((tw, th))
        im.paste(still, (i * tw, 0))
        d.text((i * tw + 12, th + 8), rec["id"], font=font, fill=(255, 244, 218))
    im.save(out / "code_graphics_v01_sheet.jpg", quality=90)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--only", default="")
    args = ap.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    for spec in SPECS:
        words = spec["label"].split() if spec["label"] else []
        if len(words) > 4:
            raise SystemExit(f"{spec['id']} label has {len(words)} words")
    want = set(args.only.split(",")) if args.only else None
    paper = make_paper()
    rows = []
    for spec in SPECS:
        if want and spec["id"] not in want:
            continue
        print("Rendering", spec["id"], flush=True)
        rows.append(render_one(paper, spec, args.out))
    if not want:
        sheet(args.out, rows)
        (args.out / "CODE_GRAPHICS_v01.json").write_text(json.dumps(rows, indent=2) + "\n")
    fails = [r["id"] for r in rows if r["near_black"] != "PASS" or r["label_words"] > 4]
    print(json.dumps([{k: r[k] for k in ("id", "probed_duration_s", "near_black", "min_sample_mean_luma", "label_words")} for r in rows], indent=2))
    if fails:
        raise SystemExit(f"fails: {fails}")


if __name__ == "__main__":
    main()
