#!/usr/bin/env python3
"""HOS 003 Part 02 rough v03 — v02 pipeline with plate 08 CUT.

Ben settled 21 Sep 2026: lock 08_locks_the_door out of the assemble.
Do not use 08_locks_the_door_v01 / v02 / v03 (all bolt-through-metal FAIL).

Showrunner GO: VO lock part02_the_cardboard_v02.txt (sha f3454130…).
Do not use v01.txt. No 03_cardboard_waiting. No Explorer. No Orbit.
Labels from PART02_ASSEMBLE_V01_CUES.md (Part 01 v03 house).
UNKNOWN fallback no longer sits on the lock plate — short-hold on the X plate.
Keep COVERED TUBE through DETECTOR where picture exists. No freeze-pad.
"""
from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

PROJ = Path(__file__).resolve().parents[1]
CLIPS = PROJ / "04_Generated-Clips" / "part02"
VO_TXT = PROJ / "02_Voiceover/part02_the_cardboard_v02.txt"
VO_TXT_SHA = "f3454130086c42ea5545b2e149f193fe8d03ea2f0b7843155e48784ccb206975"
VO = PROJ / "02_Voiceover/05_Master/hos_003_part02_vo_v01_draft.wav"
ALIGN = PROJ / "02_Voiceover/05_Master/hos_003_part02_vo_v01_draft_align.json"
BED = Path(
    "/Users/benjaminoats/YouTube/History Of Science/02_Video-Projects/"
    "001_How-Did-We-Discover-Germs/05_Music/hos_001_part01_ominous_ward_v14_norm.wav"
)
OUT = PROJ / "09_Final-Export/hos_003_part02_rough_v03.mp4"
ICLOUD = (
    Path.home()
    / "Library/Mobile Documents/com~apple~CloudDocs/HOS UAT"
    / "hos_003_part02_rough_v03.mp4"
)
WORK = PROJ / "07_Edit-Project/_part02_v03_work"
LABEL_DIR = PROJ / "07_Edit-Project/_part02_v03_labels"
META = PROJ / "07_Edit-Project/part02_rough_v03_land_meta.json"
XFADE = 0.35
CLIP_USE = 8.0
BED_VOL = 0.34
FPS = 24
DIDOT = "/System/Library/Fonts/Supplemental/Didot.ttc"

# KEEP 02, 04–07, 09–11. Plate 08 CUT. No 03. No 01 chapter.
PLATES = [
    "02_tube_covered_v01.mp4",
    "04_should_stay_dark_v01.mp4",
    "05_glow_blooms_v02.mp4",
    "06_passes_soft_things_v03.mp4",
    "07_names_it_x_v01.mp4",
    "09_test_book_v01.mp4",
    "10_test_hand_metal_v01.mp4",
    "11_detector_hold_v01.mp4",
]
FORBIDDEN_PLATES = (
    "08_locks_the_door_v01.mp4",
    "08_locks_the_door_v02.mp4",
    "08_locks_the_door_v03.mp4",
)

# 8-plate map (NO 08). UNKNOWN fallback used to sit on the lock plate.
LABEL_WINDOW = {
    "COVERED TUBE": 0,
    "CARDBOARD": 1,
    "IT GLOWS": 2,
    "FLUORESCENT": 3,
    "X": 4,
    "UNKNOWN": 4,
    "A PATTERN": 6,
    "DETECTOR": 7,
}
CARD_WINDOW = {
    "WHY COVER THE TUBE": 0,
    "FLUORESCENT SCREEN": 3,
    "X FOR UNKNOWN": 4,
    "PATTERN, NOT GHOST": 6,
}


def probe(path: Path) -> float:
    return float(
        subprocess.check_output(
            [
                "ffprobe", "-v", "error", "-show_entries", "format=duration",
                "-of", "default=nw=1:nk=1", str(path),
            ],
            text=True,
        ).strip()
    )


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def _text_size(d: ImageDraw.ImageDraw, text: str, fnt: ImageFont.ImageFont) -> tuple[int, int]:
    bb = d.textbbox((0, 0), text, font=fnt)
    return bb[2] - bb[0], bb[3] - bb[1]


def word_gap(d: ImageDraw.ImageDraw, fnt: ImageFont.ImageFont) -> int:
    a, _ = _text_size(d, "n", fnt)
    b, _ = _text_size(d, "n n", fnt)
    gap = b - 2 * a
    return max(14, gap if gap > 6 else max(16, fnt.size // 3 if hasattr(fnt, "size") else 18))


def measure_words(d: ImageDraw.ImageDraw, text: str, fnt: ImageFont.ImageFont) -> tuple[int, int, int]:
    words = text.split()
    if not words:
        return 0, 0, 16
    gap = word_gap(d, fnt)
    widths = [_text_size(d, w, fnt)[0] for w in words]
    height = max(_text_size(d, w, fnt)[1] for w in words)
    total = sum(widths) + gap * (len(words) - 1)
    return total, height, gap


def draw_words(
    d: ImageDraw.ImageDraw,
    xy: tuple[float, float],
    text: str,
    fnt: ImageFont.ImageFont,
    fill: tuple[int, int, int, int],
) -> None:
    x, y = xy
    words = text.split()
    gap = word_gap(d, fnt)
    for i, word in enumerate(words):
        d.text((x, y), word, font=fnt, fill=fill)
        x += _text_size(d, word, fnt)[0] + (gap if i < len(words) - 1 else 0)


def font(size: int, *, italic: bool = False, bold: bool = False) -> ImageFont.FreeTypeFont:
    idx = 2 if bold else 1 if italic else 0
    try:
        return ImageFont.truetype(DIDOT, size, index=idx)
    except OSError:
        try:
            return ImageFont.truetype(
                "/System/Library/Fonts/Supplemental/Georgia.ttf", size
            )
        except OSError:
            return ImageFont.load_default()


def load_align_text(path: Path) -> tuple[str, list[float], list[float]]:
    raw = json.loads(path.read_text())
    chars = raw.get("characters") or []
    starts = raw.get("character_start_times_seconds") or []
    ends = raw.get("character_end_times_seconds") or []
    text = "".join(chars)
    return text, [float(x) for x in starts], [float(x) for x in ends]


def find_phrase(text: str, starts: list[float], ends: list[float], needle: str) -> float | None:
    hay = text.lower()
    n = needle.lower()
    i = hay.find(n)
    if i < 0:
        return None
    if i >= len(starts):
        return None
    return starts[i]


def plate_windows(n: int, use: float, xfade: float) -> list[tuple[float, float]]:
    wins: list[tuple[float, float]] = []
    t = 0.0
    for i in range(n):
        wins.append((t, t + use))
        t = t + use - xfade
    return wins


def _win(windows: list[tuple[float, float]], name: str) -> tuple[float, float]:
    return windows[LABEL_WINDOW[name]]


def cue_from_align(
    align_path: Path,
    pic_dur: float,
    windows: list[tuple[float, float]],
) -> tuple[list[tuple[float, float, str]], list[tuple[float, float, str, str]]]:
    w_tube = _win(windows, "COVERED TUBE")
    w_card = _win(windows, "CARDBOARD")
    w_glow = _win(windows, "IT GLOWS")
    w_fluor = _win(windows, "FLUORESCENT")
    w_x = _win(windows, "X")
    w_pattern = _win(windows, "A PATTERN")
    w_det = _win(windows, "DETECTOR")
    fallback_labels = [
        (w_tube[0] + 0.6, w_tube[1] - 0.8, "COVERED TUBE"),
        (w_card[0] + 0.5, w_card[1] - 0.6, "CARDBOARD"),
        (w_glow[0] + 0.5, w_glow[1] - 0.6, "IT GLOWS"),
        (w_fluor[0] + 0.5, w_fluor[1] - 0.6, "FLUORESCENT"),
        (w_x[0] + 0.5, w_x[0] + 3.4, "X"),
        (w_x[0] + 3.6, min(w_x[1] - 0.45, w_x[0] + 5.8), "UNKNOWN"),
        (w_pattern[0] + 0.5, w_pattern[1] - 0.5, "A PATTERN"),
        (w_det[0] + 0.4, min(w_det[1] - 0.3, pic_dur - 0.15), "DETECTOR"),
    ]
    fallback_cards = [
        (
            w_tube[0] + 3.2,
            min(w_tube[1] - 0.2, w_tube[0] + 6.6),
            "WHY COVER THE TUBE",
            "Cathode rays were supposed to stay inside.",
        ),
        (
            w_fluor[0] + 2.4,
            min(w_fluor[1] - 0.2, w_fluor[0] + 6.4),
            "FLUORESCENT SCREEN",
            "A screen painted to glow when light hits it.",
        ),
        (
            w_x[0] + 2.8,
            min(w_x[1] - 0.35, w_x[0] + 6.6),
            "X FOR UNKNOWN",
            "He names the new ray X — unknown.",
        ),
        (
            w_pattern[0] + 2.6,
            min(w_pattern[1] - 0.2, w_pattern[0] + 6.6),
            "PATTERN, NOT GHOST",
            "Book, hand, metal change the glow on purpose.",
        ),
    ]
    if not align_path.exists():
        return fallback_labels, fallback_cards

    text, starts, ends = load_align_text(align_path)
    if not text or not starts:
        return fallback_labels, fallback_cards

    def t_of(*needles: str, default: float) -> float:
        for n in needles:
            hit = find_phrase(text, starts, ends, n)
            if hit is not None:
                return hit
        return default

    def hold(start: float, seconds: float) -> tuple[float, float]:
        a = max(0.15, start)
        b = min(pic_dur - 0.12, a + seconds)
        if b <= a + 1.1:
            b = min(pic_dur - 0.08, a + 1.4)
        return a, b

    raw = [
        (t_of("covers the tube", "wraps it carefully", default=fallback_labels[0][0]), 4.2, "COVERED TUBE"),
        (t_of("cardboard screen", "cardboard should", default=fallback_labels[1][0]), 3.6, "CARDBOARD"),
        (t_of("fluorescent screen", "fluorescent", default=fallback_labels[3][0]), 3.4, "FLUORESCENT"),
        (t_of("soft glow blooms", "it does not", default=fallback_labels[2][0]), 3.6, "IT GLOWS"),
        (t_of("calls it x", "he calls it x", default=fallback_labels[4][0]), 3.4, "X"),
        (t_of("for unknown", "unknown ray", default=fallback_labels[5][0]), 2.6, "UNKNOWN"),
        (t_of("pattern, not ghost", "the glow changes", default=fallback_labels[6][0]), 3.8, "A PATTERN"),
        (t_of("first detector", "glowing cardboard is the first", default=fallback_labels[7][0]), 3.8, "DETECTOR"),
    ]
    labels: list[tuple[float, float, str]] = []
    for start, dur, name in raw:
        if start >= pic_dur - 0.4:
            snap = _win(windows, name)
            # Late VO (pattern / detector) is past the mix. Snap onto remaining
            # picture, but do not crowd X / UNKNOWN — those beats are still spoken.
            if name == "A PATTERN":
                start = max(snap[0] + 0.45, snap[1] - 2.6)
                dur = min(dur, 2.4)
            elif name == "UNKNOWN":
                start = snap[0] + 0.45
                dur = min(dur, 2.4)
            else:
                start = snap[0] + 0.45
        a, b = hold(start, dur)
        labels.append((a, b, name))

    labels.sort(key=lambda x: x[0])
    cleaned: list[tuple[float, float, str]] = []
    for a, b, name in labels:
        if cleaned and a < cleaned[-1][1] + 0.12:
            prev_a, prev_b, prev_n = cleaned[-1]
            keep = max(prev_a + 2.2, min(prev_b, a))
            cleaned[-1] = (prev_a, keep, prev_n)
            a = keep + 0.16
            b = min(pic_dur - 0.08, max(a + 2.2, b))
            if b <= a + 1.15:
                continue
        cleaned.append((a, b, name))

    cards_raw = [
        (
            t_of("fluorescent screen", "chemical that glows", default=fallback_cards[1][0]) + 0.15,
            4.2,
            "FLUORESCENT SCREEN",
            "A screen painted to glow when light hits it.",
        ),
        (
            t_of("covers the tube", "stay trapped", default=fallback_cards[0][0]) + 2.4,
            3.8,
            "WHY COVER THE TUBE",
            "Cathode rays were supposed to stay inside.",
        ),
        (
            t_of("for unknown", "calls it x", default=fallback_cards[2][0]) + 0.35,
            4.0,
            "X FOR UNKNOWN",
            "He names the new ray X — unknown.",
        ),
        (
            t_of("pattern, not ghost", "with metal", default=fallback_cards[3][0]) + 0.2,
            4.0,
            "PATTERN, NOT GHOST",
            "Book, hand, metal change the glow on purpose.",
        ),
    ]
    cards: list[tuple[float, float, str, str]] = []
    for start, dur, title, body in cards_raw:
        if start >= pic_dur - 0.6:
            owner = CARD_WINDOW.get(title)
            if owner is None:
                continue
            if title.startswith("PATTERN"):
                start = windows[owner][1] - 3.2
            else:
                start = windows[owner][0] + 1.8
        a, b = hold(start, dur)
        cards.append((a, b, title, body))
    cards.sort(key=lambda x: x[0])
    card_clean: list[tuple[float, float, str, str]] = []
    for a, b, title, body in cards:
        if card_clean and a < card_clean[-1][1]:
            a = card_clean[-1][1] + 0.2
            b = min(pic_dur - 0.08, a + 3.4)
            if b <= a + 1.2:
                continue
        card_clean.append((a, b, title, body))
    return cleaned, card_clean


def render_side_label(text: str, dest: Path) -> None:
    w, h = 1920, 1080
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    size = 92 if len(text.strip()) <= 2 else 56
    fnt = font(size, italic=True)
    tw, th, _gap = measure_words(d, text, fnt)
    x = w - tw - 88
    y = 78 if size > 70 else 86
    shadow = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    draw_words(sd, (x + 1, y + 2), text, fnt, (8, 6, 4, 160))
    shadow = shadow.filter(ImageFilter.GaussianBlur(radius=1.6))
    im = Image.alpha_composite(im, shadow)
    d = ImageDraw.Draw(im)
    draw_words(d, (x, y), text, fnt, (246, 240, 230, 245))
    dest.parent.mkdir(parents=True, exist_ok=True)
    im.save(dest)


def render_teach_card(title: str, body: str, dest: Path) -> None:
    w, h = 1920, 1080
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    title_f = font(30, italic=True)
    body_f = font(24, italic=False)
    pad_x, pad_y = 28, 22
    tw, th, _ = measure_words(d, title, title_f)
    bw, bh, _ = measure_words(d, body, body_f)
    box_w = max(tw, bw) + pad_x * 2
    box_h = th + bh + pad_y * 2 + 14
    x0, y0 = 72, h - box_h - 78
    d.rounded_rectangle(
        (x0, y0, x0 + box_w, y0 + box_h),
        radius=22,
        fill=(18, 14, 12, 210),
    )
    draw_words(d, (x0 + pad_x, y0 + pad_y - 2), title, title_f, (246, 238, 224, 250))
    draw_words(
        d,
        (x0 + pad_x, y0 + pad_y + th + 8),
        body,
        body_f,
        (230, 220, 204, 235),
    )
    dest.parent.mkdir(parents=True, exist_ok=True)
    im.save(dest)


def _assert_no_plate_08() -> None:
    joined = " ".join(PLATES)
    if "03_" in joined:
        raise SystemExit("STOP: 03_cardboard_waiting is parked — assemble without it")
    if any(name.startswith("08_locks_the_door") for name in PLATES):
        raise SystemExit("STOP: plate 08 CUT — do not assemble 08_locks_the_door v01/v02/v03")
    if any(name in FORBIDDEN_PLATES for name in PLATES):
        raise SystemExit("STOP: forbidden 08_locks_the_door take in PLATES")
    if len(PLATES) != 8:
        raise SystemExit(f"STOP: v03 must be 8 plates (no 08); got {len(PLATES)}")


def main() -> None:
    _assert_no_plate_08()
    if VO_TXT.name != "part02_the_cardboard_v02.txt" or not VO_TXT.exists():
        raise SystemExit("STOP: VO lock is part02_the_cardboard_v02.txt — do not use v01")
    got_txt = sha256(VO_TXT)
    if got_txt != VO_TXT_SHA:
        raise SystemExit(f"STOP: VO txt sha {got_txt} != locked {VO_TXT_SHA}")
    for name in PLATES:
        p = CLIPS / name
        if not p.exists() or p.stat().st_size < 100_000:
            raise SystemExit(f"missing plate {p}")
    if not VO.exists():
        raise SystemExit(f"missing VO {VO} — run 02_Voiceover/_generate_part02_vo_v01.py")
    if not BED.exists():
        raise SystemExit(f"missing bed {BED}")

    WORK.mkdir(parents=True, exist_ok=True)
    LABEL_DIR.mkdir(parents=True, exist_ok=True)
    OUT.parent.mkdir(parents=True, exist_ok=True)

    n = len(PLATES)
    pic_dur = n * CLIP_USE - (n - 1) * XFADE
    vo_dur = probe(VO)
    mix_dur = min(pic_dur, vo_dur)
    windows = plate_windows(n, CLIP_USE, XFADE)
    labels, cards = cue_from_align(ALIGN, mix_dur, windows)

    print(f"VO={vo_dur:.3f}s picture={pic_dur:.3f}s mix={mix_dur:.3f}s", flush=True)
    if vo_dur - mix_dur > 0.4:
        print(
            f"VO_TRIM note: VO {vo_dur:.1f}s vs picture {pic_dur:.1f}s — "
            f"{vo_dur - mix_dur:.1f}s overhang cut for v03 (no freeze-pad; "
            "plate 08 CUT; 03_cardboard_waiting still parked)",
            flush=True,
        )

    label_pngs: list[tuple[float, float, Path]] = []
    for i, (a, b, text) in enumerate(labels):
        png = LABEL_DIR / f"side_{i:02d}.png"
        render_side_label(text, png)
        label_pngs.append((a, b, png))
        print(f"  LABEL {a:.2f}-{b:.2f} {text}", flush=True)

    card_pngs: list[tuple[float, float, Path]] = []
    for i, (a, b, title, body) in enumerate(cards):
        png = LABEL_DIR / f"card_{i:02d}.png"
        render_teach_card(title, body, png)
        card_pngs.append((a, b, png))
        print(f"  CARD  {a:.2f}-{b:.2f} {title}", flush=True)

    overlays = [("label", a, b, p) for a, b, p in label_pngs] + [
        ("card", a, b, p) for a, b, p in card_pngs
    ]

    normed: list[Path] = []
    for i, name in enumerate(PLATES):
        src = CLIPS / name
        dst = WORK / f"n{i:02d}.mp4"
        subprocess.run(
            [
                "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
                "-i", str(src),
                "-t", f"{CLIP_USE:.3f}",
                "-vf",
                "scale=1920:1080:force_original_aspect_ratio=decrease,"
                "pad=1920:1080:(ow-iw)/2:(oh-ih)/2,"
                f"fps={FPS},format=yuv420p,setsar=1",
                "-an",
                "-c:v", "libx264", "-preset", "fast", "-crf", "18",
                str(dst),
            ],
            check=True,
        )
        normed.append(dst)

    inputs: list[str] = []
    for p in normed:
        inputs += ["-i", str(p)]
    vo_i = n
    bed_i = n + 1
    inputs += ["-i", str(VO), "-i", str(BED)]
    overlay_start = n + 2
    for _kind, _a, _b, png in overlays:
        inputs += ["-loop", "1", "-t", f"{mix_dur:.3f}", "-i", str(png)]

    parts: list[str] = []
    cur = "[0:v]"
    for i in range(1, n):
        offset = i * CLIP_USE - i * XFADE
        out = f"[v{i}]" if i < n - 1 else "[vout]"
        parts.append(
            f"{cur}[{i}:v]xfade=transition=fade:duration={XFADE}:offset={offset:.3f}{out}"
        )
        cur = out

    cur = "[vout]"
    for li, (_kind, a, b, _png) in enumerate(overlays):
        idx = overlay_start + li
        nxt = f"[ov{li}]"
        fade = 0.28
        hold = max(0.8, b - a)
        parts.append(
            f"[{idx}:v]format=rgba,"
            f"fade=t=in:st=0:d={fade}:alpha=1,"
            f"fade=t=out:st={max(fade, hold - fade):.3f}:d={fade}:alpha=1,"
            f"setpts=PTS+{a:.3f}/TB[og{li}];"
            f"{cur}[og{li}]overlay=0:0:eof_action=pass{nxt}"
        )
        cur = nxt

    parts.append(f"{cur}format=yuv420p,setsar=1[v]")
    fade_start = max(0.0, mix_dur - 2.4)
    parts.append(
        f"[{vo_i}:a]atrim=0:{mix_dur:.3f},asetpts=PTS-STARTPTS,"
        f"aformat=sample_rates=48000:channel_layouts=stereo[vo];"
        f"[{bed_i}:a]aloop=loop=-1:size=2e9,atrim=0:{mix_dur:.3f},asetpts=PTS-STARTPTS,"
        f"volume={BED_VOL},afade=t=out:st={fade_start:.3f}:d=2.3,"
        f"aformat=sample_rates=48000:channel_layouts=stereo[bed];"
        f"[vo][bed]amix=inputs=2:duration=first:dropout_transition=0[a]"
    )
    fc = ";".join(parts)

    cmd = [
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
        *inputs,
        "-filter_complex", fc,
        "-map", "[v]", "-map", "[a]",
        "-c:v", "libx264", "-preset", "medium", "-crf", "18",
        "-pix_fmt", "yuv420p", "-r", str(FPS),
        "-c:a", "aac", "-b:a", "192k",
        "-movflags", "+faststart",
        "-t", f"{mix_dur:.3f}",
        str(OUT),
    ]
    subprocess.run(cmd, check=True)

    digest = sha256(OUT)
    ICLOUD.parent.mkdir(parents=True, exist_ok=True)
    ICLOUD.write_bytes(OUT.read_bytes())
    dur = probe(OUT)
    meta = {
        "cut": OUT.name,
        "path": str(OUT),
        "icloud": str(ICLOUD),
        "bytes": OUT.stat().st_size,
        "sha256": digest,
        "duration_s": dur,
        "vo_s": vo_dur,
        "picture_s": pic_dur,
        "mix_s": mix_dur,
        "vo_trim_s": max(0.0, vo_dur - mix_dur),
        "bed": BED.name,
        "bed_vol": BED_VOL,
        "plates": PLATES,
        "parked": [
            "01_chapter_cardboard_v01",
            "03_cardboard_waiting",
            "08_locks_the_door_v01",
            "08_locks_the_door_v02",
            "08_locks_the_door_v03",
        ],
        "forbidden": list(FORBIDDEN_PLATES),
        "labels": [{"t0": a, "t1": b, "text": t} for a, b, t in labels],
        "teach_cards": [
            {"t0": a, "t1": b, "title": title, "body": body}
            for a, b, title, body in cards
        ],
        "house": (
            "No Explorer. No Orbit. Flat-cardboard brief. Continuous 1x motion. "
            "Plate 08 CUT — do not use locks_the_door v01/v02/v03."
        ),
    }
    META.write_text(json.dumps(meta, indent=2) + "\n")

    print(f"LANDED {OUT}", flush=True)
    print(f"BYTES {OUT.stat().st_size}", flush=True)
    print(f"SHA256 {digest}", flush=True)
    print(f"DUR {dur:.3f} (mix {mix_dur:.3f})", flush=True)
    print(f"ICLOUD {ICLOUD} bytes={ICLOUD.stat().st_size}", flush=True)
    print(f"BED {BED.name} vol={BED_VOL} fade_out@{fade_start:.2f}", flush=True)
    print("PLATES " + " | ".join(PLATES), flush=True)
    print(f"META {META}", flush=True)


if __name__ == "__main__":
    main()
