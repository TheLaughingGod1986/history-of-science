#!/usr/bin/env python3
"""HOS 004 Short covers live-v04 — teal middle word + edge clearance.

Ben 12:30: Fri HOW / so / SMALL? · Sun EVERY / eighth / ELEMENT?
Same chunky gold/cream Shorts lettering as live 002; ONE small TEAL middle;
no letter touching the edge. Scenes kept. Also builds Tue THE / carbolic / SPRAY
for the Lister Short (cover only; no upload of Tue).
"""
from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFont, ImageOps

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
STILLS = HERE / "covers_live_v02" / "stills"
OUT = HERE / "covers_live_v04"
TUE_STILL = REPO / (
    "02_Video-Projects/001_How-Did-We-Discover-Germs/10_Shorts/"
    "covers_live_v01/stills/s06_carbolic_spray_scene.jpg"
)
TUE_OUT_DIR = REPO / (
    "02_Video-Projects/001_How-Did-We-Discover-Germs/10_Shorts/covers_live_v01"
)
LIVE002 = REPO / (
    "02_Video-Projects/002_How-Did-We-Discover-The-Periodic-Table/"
    "08_Thumbnail/Shorts"
)
ICLOUD004 = Path.home() / (
    "Library/Mobile Documents/com~apple~CloudDocs/HOS UAT/"
    "004_Whats-Really-Inside-An-Atom/10_Shorts"
)
ICLOUD001 = Path.home() / (
    "Library/Mobile Documents/com~apple~CloudDocs/HOS UAT/"
    "001_How-Did-We-Discover-Germs/10_Shorts"
)
ART = Path.home() / ".local/share/cursor-mac-mini-hos-worker/artifacts"
AGENT = Path.home() / (
    "Library/Application Support/Cursor/AgentStores/"
    "cursor_agent_stores/bc-958ae0f3-be07-568f-a2ab-eb7f422d8839/files/artifacts"
)
PREVIEW = REPO / "00_Brand/Channel-Setup/tools/thumb_preview.py"

W, H = 1080, 1920
FONT = "/System/Library/Fonts/Supplemental/Arial Rounded Bold.ttf"
FONT_FALLBACK = "/System/Library/Fonts/Supplemental/Arial Black.ttf"

CREAM = (248, 236, 205)
GOLD = (236, 188, 58)
GOLD_HI = (255, 220, 120)
TEAL = (55, 168, 172)  # matches live 002 teal middle samples
INK = (22, 12, 6)
EXTRUDE = (48, 28, 14)
SHADOW = (8, 5, 3)

# Keep stroke + extrude clear of frame edge
EDGE_PAD = 56
MAX_FACE_SPAN = 0.90  # face width; stroke sits inside EDGE_PAD

LIVE_REFS = [
    LIVE002 / "hos_002_s01_empty_chairs_cover_live_v02.jpg",
    LIVE002 / "hos_002_s02_predict_metal_cover_live_v02.jpg",
    LIVE002 / "hos_002_s03_gallium_cover_live_v02.jpg",
    LIVE002 / "hos_002_s04_tellurium_cover_live_v02.jpg",
    LIVE002 / "hos_002_s05_other_table_cover_live_v02.jpg",
]

JOBS = [
    {
        "id": "s01",
        "still": STILLS / "s01_how_small_scene.png",
        "out": OUT / "hos_004_s01_how_small_cover_live_v04.jpg",
        "lines": [
            ("HOW", CREAM, 0.72),
            ("so", TEAL, 0.36),
            ("SMALL?", GOLD, 1.00),
        ],
    },
    {
        "id": "s02",
        "still": STILLS / "s02_every_eighth_scene.png",
        "out": OUT / "hos_004_s02_every_eighth_cover_live_v04.jpg",
        "lines": [
            ("EVERY", CREAM, 0.68),
            ("eighth", TEAL, 0.36),
            ("ELEMENT?", GOLD, 1.00),
        ],
    },
    {
        "id": "s06",
        "still": TUE_STILL,
        "out": TUE_OUT_DIR / "hos_001_s06_carbolic_spray_cover_live_v01.jpg",
        "lines": [
            ("THE", CREAM, 0.68),
            ("carbolic", TEAL, 0.40),
            ("SPRAY", GOLD, 1.00),
        ],
    },
]


def load_font(size: int) -> ImageFont.FreeTypeFont:
    for path in (FONT, FONT_FALLBACK):
        try:
            return ImageFont.truetype(path, size)
        except OSError:
            continue
    return ImageFont.load_default()


def fit_size(text: str, target_w: int, *, lo: int = 40, hi: int = 280) -> int:
    best = lo
    while lo <= hi:
        mid = (lo + hi) // 2
        f = load_font(mid)
        if int(f.getlength(text)) <= target_w:
            best = mid
            lo = mid + 1
        else:
            hi = mid - 1
    return best


def stroke_for(size: int) -> int:
    return max(10, size // 7)


def draw_chunky_line(
    canvas: Image.Image,
    text: str,
    *,
    color: tuple[int, int, int],
    size: int,
    cx: int,
    cy: int,
) -> Image.Image:
    f = load_font(size)
    stroke = stroke_for(size)
    bbox = f.getbbox(text)
    tw = int(f.getlength(text))
    th = bbox[3] - bbox[1]
    x = cx - tw // 2
    y = cy - th // 2 - bbox[1]

    layer = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)

    for dx, dy in ((10, 16), (7, 12), (4, 8)):
        d.text(
            (x + dx, y + dy),
            text,
            font=f,
            fill=(*SHADOW, 210),
            stroke_width=stroke + 5,
            stroke_fill=(*SHADOW, 210),
        )

    extrude_n = 12 if color == TEAL else 16
    for i in range(extrude_n, 0, -1):
        d.text(
            (x + i, y + i),
            text,
            font=f,
            fill=(*EXTRUDE, 255),
            stroke_width=stroke + 2,
            stroke_fill=(*EXTRUDE, 255),
        )

    d.text(
        (x, y),
        text,
        font=f,
        fill=(*color, 255),
        stroke_width=stroke,
        stroke_fill=(*INK, 255),
    )

    if color == GOLD:
        mask = Image.new("L", canvas.size, 0)
        md = ImageDraw.Draw(mask)
        md.text(
            (x, y),
            text,
            font=f,
            fill=255,
            stroke_width=max(1, stroke // 3),
            stroke_fill=255,
        )
        band = Image.new("L", canvas.size, 0)
        ImageDraw.Draw(band).rectangle(
            (x - 20, y - 10, x + tw + 20, int(y + th * 0.40)), fill=255
        )
        mask = Image.composite(mask, Image.new("L", canvas.size, 0), band)
        hi_face = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
        ImageDraw.Draw(hi_face).text((x, y), text, font=f, fill=(*GOLD_HI, 200))
        layer = Image.alpha_composite(
            layer, Image.composite(hi_face, Image.new("RGBA", canvas.size, 0), mask)
        )

    return Image.alpha_composite(canvas.convert("RGBA"), layer)


def render_type_layer(
    lines: list[tuple[str, tuple[int, int, int], float]],
    widths: list[tuple[str, int, int]],
) -> Image.Image:
    """Lettering alone on transparent canvas (for edge measurement)."""
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    y0 = 64
    cy = y0
    for (text, color, _), (_, sz, _) in zip(lines, widths):
        line_h = int(sz * (0.82 if color == TEAL else 0.94))
        layer = draw_chunky_line(
            layer, text, color=color, size=sz, cx=W // 2, cy=cy + line_h // 2
        )
        cy += line_h + (6 if color == TEAL else 2)
    return layer


def size_lines(
    lines: list[tuple[str, tuple[int, int, int], float]],
) -> list[tuple[str, int, int]]:
    target = min(int(W * MAX_FACE_SPAN), W - 2 * EDGE_PAD - 40)
    punch_idx = max(range(len(lines)), key=lambda i: lines[i][2])
    punch_size = fit_size(lines[punch_idx][0], target, lo=100, hi=260)

    widths: list[tuple[str, int, int]] = []
    for i, (text, color, rel) in enumerate(lines):
        if i == punch_idx:
            sz = punch_size
        elif color == TEAL:
            sz = max(42, int(punch_size * rel))
            sz = fit_size(text, int(target * 0.70), lo=36, hi=sz)
        else:
            sz = max(52, int(punch_size * rel))
            sz = fit_size(text, target, lo=40, hi=sz)
        widths.append((text, sz, int(load_font(sz).getlength(text))))

    span = widths[punch_idx][2] / W
    while span < 0.84 and widths[punch_idx][1] < 260:
        ns = widths[punch_idx][1] + 3
        nw = int(load_font(ns).getlength(widths[punch_idx][0]))
        if nw > target:
            break
        widths[punch_idx] = (widths[punch_idx][0], ns, nw)
        for i in range(len(widths)):
            if i == punch_idx:
                continue
            rel = lines[i][2] / lines[punch_idx][2]
            hi = max(40, int(widths[punch_idx][1] * rel))
            tw = int(target * 0.70) if lines[i][1] == TEAL else target
            osz = fit_size(widths[i][0], tw, lo=36, hi=hi)
            widths[i] = (widths[i][0], osz, int(load_font(osz).getlength(widths[i][0])))
        span = widths[punch_idx][2] / W
    return widths


def paint_type(
    im: Image.Image, lines: list[tuple[str, tuple[int, int, int], float]]
) -> tuple[Image.Image, dict]:
    top = im.crop((0, 0, W, int(H * 0.42)))
    top = ImageEnhance.Brightness(top).enhance(0.68)
    im.paste(top, (0, 0))

    widths = size_lines(lines)
    punch_idx = max(range(len(lines)), key=lambda i: lines[i][2])
    type_layer = render_type_layer(lines, widths)
    bb = type_layer.split()[-1].getbbox()
    edge_ok = True
    if bb:
        left, top_y, right, bottom = bb
        edge_ok = (
            left >= EDGE_PAD - 4
            and right <= W - (EDGE_PAD - 4)
            and top_y >= 6
        )
        if not edge_ok:
            scale = min((W - 2 * EDGE_PAD) / max(1, right - left), 0.94)
            widths = [
                (
                    t,
                    max(36, int(sz * scale)),
                    int(load_font(max(36, int(sz * scale))).getlength(t)),
                )
                for t, sz, _ in widths
            ]
            type_layer = render_type_layer(lines, widths)
            bb = type_layer.split()[-1].getbbox()
            if bb:
                left, top_y, right, bottom = bb
                edge_ok = left >= EDGE_PAD - 4 and right <= W - (EDGE_PAD - 4)

    canvas = Image.alpha_composite(im.convert("RGBA"), type_layer)
    meta = {
        "spans": [round(w / W, 3) for _, _, w in widths],
        "sizes": [sz for _, sz, _ in widths],
        "punch_span": round(widths[punch_idx][2] / W, 3),
        "ink_bbox": list(bb) if bb else None,
        "edge_ok": edge_ok,
        "has_teal": any(c == TEAL for _, c, _ in lines),
    }
    return canvas.convert("RGB"), meta


def compose(job: dict) -> dict:
    im = Image.open(job["still"]).convert("RGB")
    # Prefer spray mist + table; bias crop slightly up for lettering room
    im = ImageOps.fit(im, (W, H), Image.Resampling.LANCZOS, centering=(0.50, 0.42))
    im, meta = paint_type(im, job["lines"])
    job["out"].parent.mkdir(parents=True, exist_ok=True)
    im.save(job["out"], "JPEG", quality=92, optimize=True, subsampling=1)
    meta["id"] = job["id"]
    meta["out"] = str(job["out"])
    meta["lines"] = [t[0] for t in job["lines"]]
    return meta


def eight_up(fri: Path, sun: Path, tue: Path) -> Path:
    paths = list(LIVE_REFS) + [fri, sun, tue]
    tw, th = 270, 480
    gap = 10
    sheet = Image.new("RGB", (8 * tw + 9 * gap, th + 2 * gap), (245, 240, 230))
    x = gap
    for p in paths:
        tile = ImageOps.fit(Image.open(p).convert("RGB"), (tw, th), Image.Resampling.LANCZOS)
        sheet.paste(tile, (x, gap))
        x += tw + gap
    out = OUT / "hos_004_shorts_covers_live_v04_eight_up.jpg"
    sheet.save(out, "JPEG", quality=92)
    return out


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    TUE_OUT_DIR.mkdir(parents=True, exist_ok=True)
    metas = []
    for job in JOBS:
        if not job["still"].exists():
            raise SystemExit(f"missing still {job['still']}")
        m = compose(job)
        metas.append(m)
        print(
            f"{m['id']} punch={m['punch_span']} teal={m['has_teal']} edge={m['edge_ok']} "
            f"sizes={m['sizes']} spans={m['spans']} → {Path(m['out']).name}",
            flush=True,
        )
        if not m["has_teal"]:
            raise SystemExit(f"FAIL {m['id']}: missing teal middle word")
        if not m["edge_ok"]:
            raise SystemExit(f"FAIL {m['id']}: lettering touches edge {m['ink_bbox']}")
        if m["punch_span"] < 0.82:
            print(f"WARN {m['id']} punch_span {m['punch_span']} < 0.82", flush=True)

    fri = OUT / "hos_004_s01_how_small_cover_live_v04.jpg"
    sun = OUT / "hos_004_s02_every_eighth_cover_live_v04.jpg"
    tue = TUE_OUT_DIR / "hos_001_s06_carbolic_spray_cover_live_v01.jpg"
    eight = eight_up(fri, sun, tue)
    print("eight_up", eight, flush=True)

    preview = OUT / "hos_004_shorts_covers_live_v04_thumb_preview.jpg"
    subprocess.run(
        [
            "python3",
            str(PREVIEW),
            "short",
            *[str(p) for p in LIVE_REFS],
            str(fri),
            str(sun),
            str(tue),
            "--out",
            str(preview),
        ],
        check=True,
    )

    ICLOUD004.mkdir(parents=True, exist_ok=True)
    ICLOUD001.mkdir(parents=True, exist_ok=True)
    for p, dest in [
        (fri, ICLOUD004 / "live_v04_s01_how_small.jpg"),
        (sun, ICLOUD004 / "live_v04_s02_every_eighth.jpg"),
        (eight, ICLOUD004 / "live_v04_eight_up.jpg"),
        (preview, ICLOUD004 / "live_v04_thumb_preview.jpg"),
        (fri, ICLOUD004 / fri.name),
        (sun, ICLOUD004 / sun.name),
        (tue, ICLOUD001 / tue.name),
        (tue, ICLOUD001 / "live_v01_s06_carbolic_spray.jpg"),
    ]:
        shutil.copy2(p, dest)

    ART.mkdir(parents=True, exist_ok=True)
    AGENT.mkdir(parents=True, exist_ok=True)
    for name, src in [
        ("BEN_1230_covers_live_v04_eight_up.jpg", eight),
        ("BEN_1230_covers_live_v04_thumb_preview.jpg", preview),
        ("BEN_1230_s01_how_small_cover_live_v04.jpg", fri),
        ("BEN_1230_s02_every_eighth_cover_live_v04.jpg", sun),
        ("BEN_1230_s06_carbolic_spray_cover_live_v01.jpg", tue),
    ]:
        shutil.copy2(src, ART / name)
        shutil.copy2(src, AGENT / name)

    report = {
        "ok": all(m["has_teal"] and m["edge_ok"] for m in metas),
        "font": FONT,
        "teal": TEAL,
        "jobs": metas,
        "eight_up": str(eight),
        "thumb_preview": str(preview),
        "fri_sun_for_studio": [str(fri), str(sun)],
        "tue_cover_no_upload": str(tue),
    }
    (OUT / "COVERS_LIVE_V04.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2)[:2000])
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
