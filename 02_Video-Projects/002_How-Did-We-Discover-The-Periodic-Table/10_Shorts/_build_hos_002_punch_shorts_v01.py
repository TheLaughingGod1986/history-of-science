#!/usr/bin/env python3
"""Punch 5 Shorts from hos_002_periodic_table_full_v01.mp4. No remint. Not LOCKED.

Do not upload. Zero /go/. Related target is empty until the long is public.
Captions via Pillow PNG + ffmpeg overlay (this ffmpeg has no drawtext/libass).
Abort if any Short is under 22s or ≥28s (never ≥40s).
"""
from __future__ import annotations

import json
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
PROJ = HERE.parent
SRC = PROJ / "09_Final-Export/hos_002_periodic_table_full_v01.mp4"
META = PROJ / "07_Edit-Project/part_full_v01_land_meta.json"
OUT_DIR = HERE
ICLOUD = Path.home() / "Library/Mobile Documents/com~apple~CloudDocs/HOS UAT"
FONT = "/System/Library/Fonts/Supplemental/Didot.ttc"
CTA_FONT = "/System/Library/Fonts/Supplemental/Times New Roman.ttf"

# Locked parent durations (hash-checked at join).
P01 = 0.0
P02 = 85.680
P03 = 169.680
P04 = 259.360
P05 = 387.120

PARENT = "How Did We Discover the Periodic Table?"
PARENT_ID = None  # no YouTube id yet — do not upload

# Punch windows on the STITCHED full cut. Story ~20s + 4s silent loop of the open.
SHORTS = [
    {
        "id": "s01_empty_chairs",
        "slot": "after long public · first Short (Thu ~21:00 UK)",
        "title": "The empty chairs were the cleverest part",
        "line": "He leaves seats empty on purpose.",
        "start": P04 + 42.00,
        "end": P04 + 62.00,
        "hold": 0.0,
        "loop_open": True,
    },
    {
        "id": "s02_predict_metal",
        "slot": "after long public · Sat ~11:30 UK",
        "title": "He predicted a metal before anyone found it",
        "line": "Chemistry can hunt a metal before anyone has found it.",
        "start": P04 + 68.00,
        "end": P04 + 88.00,
        "hold": 0.0,
        "loop_open": True,
    },
    {
        "id": "s03_gallium",
        "slot": "after long public · Mon ~11:30 UK",
        "title": "A drop of gallium that sat in the gap",
        "line": "It sits where eka-aluminium was told to sit.",
        "start": P05 + 5.00,
        "end": P05 + 26.20,
        "hold": 0.0,
        "loop_open": True,
    },
    {
        "id": "s04_tellurium",
        "slot": "after long public · Wed ~11:30 UK",
        "title": "Why tellurium and iodine sat wrong",
        "line": "Tellurium before iodine, because how they burn and salt matters more.",
        "start": P04 + 100.00,
        "end": P04 + 120.00,
        "hold": 0.0,
        "loop_open": True,
    },
    {
        "id": "s05_other_table",
        "slot": "after long public · Fri ~11:30 UK",
        "title": "What other table are we staring at?",
        "line": "What other table are we staring at — full of names, empty of order?",
        "start": P05 + 122.40,
        "end": P05 + 143.40,
        "hold": 0.0,
        "loop_open": True,
    },
]

W, H = 1080, 1920
CREAM = (245, 232, 210, 255)
INK = (28, 26, 28, 255)
VF_916 = (
    "scale=1920:1080,"
    "crop=608:1080:656:0,"
    "scale=1080:1920:flags=lanczos,"
    "setsar=1"
)


def sha256(p: Path) -> str:
    import hashlib

    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def probe(p: Path) -> float:
    r = subprocess.run(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "default=noprint_wrappers=1:nokey=1",
            str(p),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    return float(r.stdout.strip())


def ff(*args: str) -> None:
    subprocess.run(
        ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", *args], check=True
    )


def wrap_text(text: str, font: ImageFont.FreeTypeFont, max_w: int) -> list[str]:
    words = text.split()
    lines: list[str] = []
    cur = ""
    for word in words:
        trial = (cur + " " + word).strip()
        if font.getlength(trial) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines or [text]


def render_caption_png(
    path: Path, text: str, size: int, *, anchor: str, y: int, font_path: str = FONT
) -> None:
    font_obj = ImageFont.truetype(font_path, size)
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    max_w = W - 96
    lines = wrap_text(text, font_obj, max_w)
    heights = []
    for line in lines:
        bbox = font_obj.getbbox(line)
        heights.append(bbox[3] - bbox[1])
    gap = int(size * 0.28)
    block_h = sum(heights) + gap * (len(lines) - 1)
    if anchor == "bottom":
        top = H - y - block_h
    else:
        top = y
    cy = top
    stroke = 3
    for line, lh in zip(lines, heights):
        tw = font_obj.getlength(line)
        x = (W - tw) / 2
        for dx in range(-stroke, stroke + 1):
            for dy in range(-stroke, stroke + 1):
                if dx == 0 and dy == 0:
                    continue
                draw.text((x + dx, cy + dy), line, font=font_obj, fill=INK)
        draw.text((x, cy), line, font=font_obj, fill=CREAM)
        cy += lh + gap
    path.parent.mkdir(parents=True, exist_ok=True)
    img.save(path)


def caption_pngs(work: Path, item: dict, total: float) -> list[tuple[Path, float, float]]:
    line_png = work / "cap_line.png"
    title_png = work / "cap_title.png"
    cta_png = work / "cap_cta.png"
    render_caption_png(line_png, item["line"], 52, anchor="bottom", y=280)
    render_caption_png(title_png, PARENT, 34, anchor="top", y=220)
    render_caption_png(
        cta_png,
        "watch the full film →",
        40,
        anchor="bottom",
        y=240,
        font_path=CTA_FONT,
    )
    cta_in = max(total - 4.0, 14.4)
    return [
        (line_png, 0.20, cta_in - 0.10),
        (title_png, 9.00, 14.00),
        (cta_png, cta_in, total - 0.12),
    ]


def encode_916(src: Path, dst: Path, start: float, dur: float, *, silent: bool) -> None:
    common = [
        "-ss",
        f"{start:.3f}",
        "-t",
        f"{dur:.3f}",
        "-i",
        str(src),
        "-vf",
        VF_916,
        "-c:v",
        "libx264",
        "-pix_fmt",
        "yuv420p",
        "-profile:v",
        "high",
        "-preset",
        "fast",
        "-crf",
        "18",
        "-r",
        "24",
        "-movflags",
        "+faststart",
    ]
    if silent:
        ff(*common, "-an", str(dst))
        tmp = dst.with_suffix(".vid.mp4")
        dst.rename(tmp)
        ff(
            "-i",
            str(tmp),
            "-f",
            "lavfi",
            "-i",
            "anullsrc=r=48000:cl=stereo",
            "-shortest",
            "-c:v",
            "copy",
            "-c:a",
            "aac",
            "-b:a",
            "192k",
            "-ar",
            "48000",
            "-ac",
            "2",
            str(dst),
        )
        tmp.unlink()
    else:
        ff(
            *common,
            "-c:a",
            "aac",
            "-b:a",
            "192k",
            "-ar",
            "48000",
            "-ac",
            "2",
            str(dst),
        )


def loop_open(story_mp4: Path, dst: Path, loop: float) -> None:
    ff(
        "-i",
        str(story_mp4),
        "-f",
        "lavfi",
        "-i",
        "anullsrc=r=48000:cl=stereo",
        "-filter_complex",
        f"[0:v]trim=0:{loop:.3f},setpts=PTS-STARTPTS[v];"
        f"[1:a]atrim=0:{loop:.3f},asetpts=PTS-STARTPTS[a]",
        "-map",
        "[v]",
        "-map",
        "[a]",
        "-c:v",
        "libx264",
        "-pix_fmt",
        "yuv420p",
        "-preset",
        "fast",
        "-crf",
        "18",
        "-r",
        "24",
        "-c:a",
        "aac",
        "-b:a",
        "192k",
        str(dst),
    )


def fit_duration(story: float, hold: float, fill: float, loop: float) -> tuple[float, float, float, float]:
    total = story + hold + fill + loop
    if total < 22.0:
        fill += 22.0 - total
        total = story + hold + fill + loop
    if total > 27.0:
        over = total - 26.4
        for name in ("hold", "fill", "loop"):
            if over <= 0:
                break
            if name == "hold":
                cut = min(hold, over)
                hold -= cut
                over -= cut
            elif name == "fill":
                cut = min(max(0.0, fill - 8.0), over)
                fill -= cut
                over -= cut
            else:
                cut = min(max(0.0, loop - 3.5), over)
                loop -= cut
                over -= cut
        total = story + hold + fill + loop
    if not (22.0 <= total <= 27.05):
        raise SystemExit(f"duration {total:.2f} out of 22–27")
    return hold, fill, loop, total


def build_one(item: dict) -> Path:
    start = float(item["start"])
    end = float(item["end"])
    hold = float(item.get("hold") or 0)
    fill = float(item.get("fill_dur") or 0)
    story = end - start
    if story < 3:
        raise SystemExit(f"{item['id']}: story window too short")
    loop = 4.0 if item.get("loop_open") else 0.0
    hold, fill, loop, total = fit_duration(story, hold, fill, loop)

    work = OUT_DIR / "_work" / item["id"]
    work.mkdir(parents=True, exist_ok=True)
    story_mp4 = work / "story.mp4"
    encode_916(SRC, story_mp4, start, story, silent=False)

    parts = [story_mp4]
    if fill > 0.05:
        fill_mp4 = work / "fill.mp4"
        encode_916(
            SRC,
            fill_mp4,
            float(item["fill_start"]),
            fill,
            silent=True,
        )
        parts.append(fill_mp4)
    if loop > 0.05:
        head = work / "loop.mp4"
        loop_open(story_mp4, head, loop)
        parts.append(head)

    concat_txt = work / "concat.txt"
    concat_txt.write_text("".join(f"file '{p.name}'\n" for p in parts))
    raw = work / "raw.mp4"
    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-hide_banner",
            "-loglevel",
            "error",
            "-f",
            "concat",
            "-safe",
            "0",
            "-i",
            str(concat_txt),
            "-c",
            "copy",
            str(raw),
        ],
        check=True,
        cwd=work,
    )

    overlays = caption_pngs(work, item, total)
    inputs = ["-i", str(raw)]
    for png, _, _ in overlays:
        inputs += ["-loop", "1", "-i", str(png)]
    fc_parts = []
    last = "0:v"
    for i, (_, a, b) in enumerate(overlays, start=1):
        nxt = f"v{i}"
        fc_parts.append(
            f"[{last}][{i}:v]overlay=0:0:enable='between(t,{a:.2f},{b:.2f})'[{nxt}]"
        )
        last = nxt
    out = OUT_DIR / f"hos_002_{item['id']}_punch_v01.mp4"
    ff(
        *inputs,
        "-filter_complex",
        ";".join(fc_parts),
        "-map",
        f"[{last}]",
        "-map",
        "0:a",
        "-c:v",
        "libx264",
        "-pix_fmt",
        "yuv420p",
        "-preset",
        "fast",
        "-crf",
        "18",
        "-r",
        "24",
        "-c:a",
        "aac",
        "-b:a",
        "192k",
        "-shortest",
        "-movflags",
        "+faststart",
        str(out),
    )
    dur = probe(out)
    if dur < 22.0 or dur >= 28.0 or dur >= 40.0:
        raise SystemExit(f"{item['id']}: exported {dur:.2f}s — abort")
    dest = ICLOUD / out.name
    dest.write_bytes(out.read_bytes())
    print(f"OK {item['id']} {dur:.2f}s → {out.name}", flush=True)
    return out


def main() -> None:
    if not SRC.exists():
        raise SystemExit(f"STOP: missing full cut {SRC} — run _join_hos_002_full_v01.py")
    if META.exists():
        want = json.loads(META.read_text())["sha256"]
        got = sha256(SRC)
        if got != want:
            raise SystemExit(f"STOP: full v01 sha mismatch {got} != {want}")
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    ICLOUD.mkdir(parents=True, exist_ok=True)
    meta = []
    for item in SHORTS:
        p = build_one(item)
        meta.append(
            {
                **item,
                "file": p.name,
                "duration": probe(p),
                "relatedVideoId": PARENT_ID,
                "go": None,
                "status": "UAT",
                "locked": False,
                "upload": False,
            }
        )
    index = {
        "parentId": PARENT_ID,
        "parentTitle": PARENT,
        "parentUrl": None,
        "source": SRC.name,
        "sourceSha": sha256(SRC),
        "note": (
            "Not LOCKED. Stop for UAT. Do not upload. Do not schedule. "
            "Do not lead the channel with a Short. Related = this film only "
            "after the long listing exists. Zero /go/."
        ),
        "schedule": [
            {
                "when": s["slot"],
                "id": s["id"],
                "title": s["title"],
            }
            for s in SHORTS
        ],
        "items": meta,
    }
    index_path = OUT_DIR / "SHORTS_PUNCH_INDEX_v01.json"
    index_path.write_text(json.dumps(index, indent=2) + "\n")
    try:
        (ICLOUD / f"hos_002_{index_path.name}").write_text(index_path.read_text())
    except OSError as exc:
        print(f"WARN iCloud index copy skipped ({exc})", flush=True)
    print(f"INDEX {index_path}", flush=True)


if __name__ == "__main__":
    main()
