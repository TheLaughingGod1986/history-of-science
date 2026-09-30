#!/usr/bin/env python3
"""HOS 004 Short covers live-v03 — lettering ONLY redo on Fri + Sun.

Keep painted scenes from covers_live_v02/stills/.
Match live 002 Short covers (Tellurium / Gallium / Gaps):
  HUGE chunky bold rounded display type · gold + cream · thick dark outline
  + drop shadow · 85–95% width · key word biggest.
Do NOT touch Tue (Ben still picking A/B). No Studio upload. STOP for Ben.
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
OUT = HERE / "covers_live_v03"
LIVE002 = REPO / (
    "02_Video-Projects/002_How-Did-We-Discover-The-Periodic-Table/"
    "08_Thumbnail/Shorts"
)
# Keep Tue cover from v02 (do not redo lettering)
TUE_KEEP = HERE / "covers_live_v02" / "hos_004_s03_they_laughed_cover_live_v02.jpg"
ICLOUD = Path.home() / (
    "Library/Mobile Documents/com~apple~CloudDocs/HOS UAT/"
    "004_Whats-Really-Inside-An-Atom/10_Shorts"
)
ART = Path.home() / ".local/share/cursor-mac-mini-hos-worker/artifacts"
AGENT = Path.home() / (
    "Library/Application Support/Cursor/AgentStores/"
    "cursor_agent_stores/bc-958ae0f3-be07-568f-a2ab-eb7f422d8839/files/artifacts"
)
PREVIEW = REPO / "00_Brand/Channel-Setup/tools/thumb_preview.py"

W, H = 1080, 1920
# Live Short covers use chunky rounded sans — NOT Georgia serif
FONT = "/System/Library/Fonts/Supplemental/Arial Rounded Bold.ttf"
FONT_FALLBACK = "/System/Library/Fonts/Supplemental/Arial Black.ttf"

CREAM = (248, 236, 205)
GOLD = (236, 188, 58)
GOLD_HI = (255, 220, 120)
TEAL = (95, 185, 182)
INK = (22, 12, 6)
EXTRUDE = (48, 28, 14)
SHADOW = (8, 5, 3)

LIVE_REFS = [
    LIVE002 / "hos_002_s01_empty_chairs_cover_live_v02.jpg",
    LIVE002 / "hos_002_s02_predict_metal_cover_live_v02.jpg",
    LIVE002 / "hos_002_s03_gallium_cover_live_v02.jpg",
    LIVE002 / "hos_002_s04_tellurium_cover_live_v02.jpg",
    LIVE002 / "hos_002_s05_other_table_cover_live_v02.jpg",
]

# line: (text, color, relative_size) — key word biggest
JOBS = [
    {
        "id": "s01",
        "still": STILLS / "s01_how_small_scene.png",
        "out": OUT / "hos_004_s01_how_small_cover_live_v03.jpg",
        "lines": [
            ("HOW", CREAM, 0.78),
            ("SMALL?", GOLD, 1.00),
        ],
    },
    {
        "id": "s02",
        "still": STILLS / "s02_every_eighth_scene.png",
        "out": OUT / "hos_004_s02_every_eighth_cover_live_v03.jpg",
        "lines": [
            ("EVERY", CREAM, 0.78),
            ("EIGHTH?", GOLD, 1.00),
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


def fit_size(text: str, target_w: int, *, lo: int = 60, hi: int = 260) -> int:
    """Largest size whose text width ≤ target_w."""
    best = lo
    while lo <= hi:
        mid = (lo + hi) // 2
        f = load_font(mid)
        w = int(f.getlength(text))
        if w <= target_w:
            best = mid
            lo = mid + 1
        else:
            hi = mid - 1
    return best


def draw_chunky_line(
    canvas: Image.Image,
    text: str,
    *,
    color: tuple[int, int, int],
    size: int,
    cx: int,
    cy: int,
) -> Image.Image:
    """3D chunky display: deep extrude + thick outline + cream highlight on gold."""
    f = load_font(size)
    stroke = max(12, size // 7)
    bbox = f.getbbox(text)
    tw = int(f.getlength(text))
    th = bbox[3] - bbox[1]
    x = cx - tw // 2
    y = cy - th // 2 - bbox[1]

    layer = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)

    # Soft drop shadow (far)
    for dx, dy in ((10, 16), (7, 12), (4, 8)):
        d.text(
            (x + dx, y + dy),
            text,
            font=f,
            fill=(*SHADOW, 210),
            stroke_width=stroke + 5,
            stroke_fill=(*SHADOW, 210),
        )

    # 3D extrude stack (down-right, bronze)
    for i in range(16, 0, -1):
        d.text(
            (x + i, y + i),
            text,
            font=f,
            fill=(*EXTRUDE, 255),
            stroke_width=stroke + 2,
            stroke_fill=(*EXTRUDE, 255),
        )

    # Main face + thick dark outline
    d.text(
        (x, y),
        text,
        font=f,
        fill=(*color, 255),
        stroke_width=stroke,
        stroke_fill=(*INK, 255),
    )

    # Cream top-edge accent on gold punch words (live Gallium/Iodine look)
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


def paint_type(
    im: Image.Image, lines: list[tuple[str, tuple[int, int, int], float]]
) -> tuple[Image.Image, dict]:
    """Stack lines at TOP spanning ~85–95% width; key word biggest."""
    top = im.crop((0, 0, W, int(H * 0.42)))
    top = ImageEnhance.Brightness(top).enhance(0.70)
    im.paste(top, (0, 0))

    target = int(W * 0.94)
    punch_idx = max(range(len(lines)), key=lambda i: lines[i][2])
    punch_size = fit_size(lines[punch_idx][0], target, lo=120, hi=300)

    widths: list[tuple[str, int, int]] = []
    for i, (text, _, rel) in enumerate(lines):
        if i == punch_idx:
            sz = punch_size
        else:
            sz = max(56, int(punch_size * rel))
            sz = fit_size(text, target, lo=40, hi=sz)
        widths.append((text, sz, int(load_font(sz).getlength(text))))

    span = widths[punch_idx][2] / W
    while span < 0.85 and widths[punch_idx][1] < 300:
        ns = widths[punch_idx][1] + 4
        nw = int(load_font(ns).getlength(widths[punch_idx][0]))
        if nw > target:
            break
        widths[punch_idx] = (widths[punch_idx][0], ns, nw)
        for i in range(len(widths)):
            if i == punch_idx:
                continue
            rel = lines[i][2] / lines[punch_idx][2]
            osz = max(56, int(widths[punch_idx][1] * rel))
            osz = fit_size(widths[i][0], target, lo=40, hi=osz)
            widths[i] = (widths[i][0], osz, int(load_font(osz).getlength(widths[i][0])))
        span = widths[punch_idx][2] / W

    canvas = im.convert("RGBA")
    y0 = 70
    cy = y0
    for (text, color, _), (_, sz, _) in zip(lines, widths):
        line_h = int(sz * 0.95)
        canvas = draw_chunky_line(
            canvas, text, color=color, size=sz, cx=W // 2, cy=cy + line_h // 2
        )
        cy += line_h

    meta = {
        "spans": [round(w / W, 3) for _, _, w in widths],
        "sizes": [sz for _, sz, _ in widths],
        "punch_span": round(span, 3),
    }
    return canvas.convert("RGB"), meta


def compose(job: dict) -> dict:
    im = Image.open(job["still"]).convert("RGB")
    im = ImageOps.fit(im, (W, H), Image.Resampling.LANCZOS)
    im, meta = paint_type(im, job["lines"])
    OUT.mkdir(parents=True, exist_ok=True)
    im.save(job["out"], "JPEG", quality=92, optimize=True, subsampling=1)
    im.save(job["out"].with_suffix(".png"))
    meta["id"] = job["id"]
    meta["out"] = str(job["out"])
    meta["lines"] = [t[0] for t in job["lines"]]
    return meta


def eight_up(fri: Path, sun: Path, tue: Path) -> Path:
    paths = list(LIVE_REFS) + [fri, sun, tue]
    assert len(paths) == 8
    tw, th = 270, 480
    gap = 10
    sheet = Image.new("RGB", (8 * tw + 9 * gap, th + 2 * gap), (245, 240, 230))
    x = gap
    for p in paths:
        tile = ImageOps.fit(Image.open(p).convert("RGB"), (tw, th), Image.Resampling.LANCZOS)
        sheet.paste(tile, (x, gap))
        x += tw + gap
    out = OUT / "hos_004_shorts_covers_live_v03_eight_up.jpg"
    sheet.save(out, "JPEG", quality=92)
    return out


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    metas = []
    for job in JOBS:
        if not job["still"].exists():
            raise SystemExit(f"missing still {job['still']}")
        m = compose(job)
        metas.append(m)
        print(
            f"{m['id']} punch_span={m['punch_span']} sizes={m['sizes']} spans={m['spans']} → {Path(m['out']).name}",
            flush=True,
        )
        if m["punch_span"] < 0.85:
            print(f"WARN {m['id']} punch_span {m['punch_span']} < 0.85", flush=True)

    if not TUE_KEEP.exists():
        raise SystemExit(f"missing Tue keep cover {TUE_KEEP}")
    tue_out = OUT / "hos_004_s03_they_laughed_cover_live_v02_kept.jpg"
    shutil.copy2(TUE_KEEP, tue_out)

    fri = OUT / "hos_004_s01_how_small_cover_live_v03.jpg"
    sun = OUT / "hos_004_s02_every_eighth_cover_live_v03.jpg"
    eight = eight_up(fri, sun, tue_out)
    print("eight_up", eight, flush=True)

    preview = OUT / "hos_004_shorts_covers_live_v03_thumb_preview.jpg"
    subprocess.run(
        [
            "python3",
            str(PREVIEW),
            "short",
            *[str(p) for p in LIVE_REFS],
            str(fri),
            str(sun),
            str(tue_out),
            "--out",
            str(preview),
        ],
        check=True,
    )
    print("thumb_preview", preview, flush=True)

    # iCloud as live_v03
    ICLOUD.mkdir(parents=True, exist_ok=True)
    for p in (fri, sun, tue_out, eight, preview):
        dest = ICLOUD / f"live_v03_{p.name}" if not p.name.startswith("hos_004") else ICLOUD / p.name.replace("live_v03", "live_v03")
        # Explicit names for Ben
        shutil.copy2(p, ICLOUD / p.name)
    # Also clear friendly aliases
    shutil.copy2(eight, ICLOUD / "hos_004_shorts_covers_live_v03_eight_up.jpg")
    shutil.copy2(preview, ICLOUD / "hos_004_shorts_covers_live_v03_thumb_preview.jpg")
    shutil.copy2(fri, ICLOUD / "live_v03_s01_how_small.jpg")
    shutil.copy2(sun, ICLOUD / "live_v03_s02_every_eighth.jpg")
    shutil.copy2(eight, ICLOUD / "live_v03_eight_up.jpg")
    shutil.copy2(preview, ICLOUD / "live_v03_thumb_preview.jpg")

    ART.mkdir(parents=True, exist_ok=True)
    AGENT.mkdir(parents=True, exist_ok=True)
    for name, src in [
        ("BEN_1206_covers_live_v03_eight_up.jpg", eight),
        ("BEN_1206_covers_live_v03_thumb_preview.jpg", preview),
        ("BEN_1206_s01_how_small_cover_live_v03.jpg", fri),
        ("BEN_1206_s02_every_eighth_cover_live_v03.jpg", sun),
    ]:
        shutil.copy2(src, ART / name)
        shutil.copy2(src, AGENT / name)

    report = {
        "ok": all(m["punch_span"] >= 0.85 for m in metas),
        "font": FONT,
        "fri_sun": metas,
        "tue": "kept live_v02 THEY LAUGHED? — Ben still picking A/B",
        "eight_up": str(eight),
        "thumb_preview": str(preview),
        "icloud": str(ICLOUD),
        "stop": "STOP for Ben — lettering redo Fri/Sun only; no Studio upload",
    }
    (OUT / "COVERS_LIVE_V03.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2)[:1500])
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
