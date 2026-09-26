#!/usr/bin/env python3
"""HOS 003 Part 05 rough v02 — Ben NOT KEEP remint set + VO v02 + ominous bed.

KEEP 01–05 + 10–11; remint 06/07/09 v03 PASS; 08_v07 radiograph-hero PASS (plate-watch).
VO lock part04_berthas_ring_v02.txt + hos_003_part04_vo_v02_draft.*
No Veo mint. No Ben ping. No Explorer this part.
Labels + teach cards from PRODUCTION_BRIEF_PART04 (silent-readable + teaching density).
Trim VO to picture — no freeze-pad / loop / slow-mo. No DNA helix.
"""
from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

PROJ = Path(__file__).resolve().parents[1]
VIDEO_PROJECTS = PROJ.parents[0]  # …/02_Video-Projects
CLIPS = PROJ / "04_Generated-Clips" / "part05"
VO_TXT = PROJ / "02_Voiceover/part05_a_new_kind_of_seeing_v02.txt"
VO_TXT_SHA = "b9cd73c8d86ec1a04a15a29b6732d57f5474260a8ccb1191d197f536f9ed5bdd"
VO = PROJ / "02_Voiceover/05_Master/hos_003_part05_vo_v02_draft.wav"
VO_SHA = "ec7e3446d45f43c42c7ffcffc6012afae3a04ef89b807aaaf8b47bf933cfd343"
VO_MP3 = PROJ / "02_Voiceover/05_Master/hos_003_part05_vo_v02_draft.mp3"
VO_MP3_SHA = "a34a87986a21cb054de471e0447ca495b4fa3cf22dfc7923f1edc9c17ce127a3"
ALIGN = PROJ / "02_Voiceover/05_Master/hos_003_part05_vo_v02_draft_align.json"
ALIGN_SHA = "f2f0bb238aff5245731036ed0e93f61dcb9e51aff9b8afbf346ea76750ee4f99"
BED = (
    VIDEO_PROJECTS
    / "001_How-Did-We-Discover-Germs/05_Music/hos_001_part04_lab_bed_v06.wav"
)
OUT = PROJ / "09_Final-Export/hos_003_part05_rough_v01.mp4"
ICLOUD = (
    Path.home()
    / "Library/Mobile Documents/com~apple~CloudDocs/HOS UAT"
    / "hos_003_part05_rough_v01.mp4"
)
WORK = PROJ / "07_Edit-Project/_part05_v01_work"
LABEL_DIR = PROJ / "07_Edit-Project/_part05_v01_labels"
META = PROJ / "07_Edit-Project/part05_rough_v01_land_meta.json"
LAND = PROJ / "07_Edit-Project/ASSEMBLE_LAND.json"
XFADE = 0.35
CLIP_USE = 7.9  # timing board part-03_plates_v01.json
BED_VOL = 0.34
FPS = 24
DIDOT = "/System/Library/Fonts/Supplemental/Didot.ttc"

PLATES = [
    "01_chapter_new_seeing_v18.mp4",
    "02_what_are_xrays_v07.mp4",
    "03_spectrum_past_uv_v07.mp4",
    "04_soft_vs_bone_v02.mp4",
    "05_detector_then_now_v01.mp4",
    "06_explorer_diagram_v07.mp4",
    "07_why_groundbreaking_v07.mp4",
    "08_dentist_hospital_payoff_v01.mp4",
    "09_bigger_question_v03.mp4",
    "10_cardboard_glow_hold_v07.mp4",
    "11_soft_return_v10.mp4",
]

PLATE_SHA = {
    "01_chapter_new_seeing_v18.mp4": "10ece3e997b4522da91edfe059945510c51bd5a56df1c58f161278741128c209",
    "02_what_are_xrays_v07.mp4": "a72e4d1e297750cf18e5188bc5e015bf004a79a118b86ae5011a455386786447",
    "03_spectrum_past_uv_v07.mp4": "083016197ce3f2ca8856e89f19f7675e55cfe672d83eee472963a7c407ee0488",
    "04_soft_vs_bone_v02.mp4": "2bd9aaca582944d9c122495e73e96beb402711eeef0f732d1ce3d1a76b985aee",
    "05_detector_then_now_v01.mp4": "2757c97ec17dab363f98cdf7ae919e55d1df21ba54702a1ba732d52d7ef51d66",
    "06_explorer_diagram_v07.mp4": "4228941dcb9b7d8ca8622012ade1e057eb7cda874ef5efb4ddc0b7acf8186ff2",
    "07_why_groundbreaking_v07.mp4": "cc55595f2e7ba9dc3a599c9b5d3710f996cb077e5e3c29c0dfe1a66fec6cfdca",
    "08_dentist_hospital_payoff_v01.mp4": "93df956a5a56105405079e5da675f1ce541a3a08ce623783956250fec1e46389",
    "09_bigger_question_v03.mp4": "fed9f00bffcc8e31daa5e17f57aab65fe356e2d9addac799fabd0f520392bbe2",
    "10_cardboard_glow_hold_v07.mp4": "b29f216cd05a0bfccef00fdcad24f82c751bd891b13328ff7a033975bc1ac2fd",
    "11_soft_return_v10.mp4": "95e5c481749963137ae2417eb7140b5e4ce05a1d1cd8d602db1d10246c98e789",
}

# Plate index for each side label / teach card (01→11 = 0..10)
LABEL_WINDOW = {
    "X-RAYS": 1,
    "INVISIBLE LIGHT": 2,
    "A DETECTOR": 4,
    "YOUR WORLD": 7,
}
CARD_WINDOW = {
    "HIGH ENERGY": 1,
    "DENSITY": 3,
    "NO KNIFE": 6,
    "STILL RONTGEN": 7,
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
    if i < 0 or i >= len(starts):
        return None
    return starts[i]


def plate_windows(n: int, use: float, xfade: float) -> list[tuple[float, float]]:
    wins: list[tuple[float, float]] = []
    t = 0.0
    for _ in range(n):
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
    w_x = _win(windows, "X-RAYS")
    w_inv = _win(windows, "INVISIBLE LIGHT")
    w_det = _win(windows, "A DETECTOR")
    w_world = _win(windows, "YOUR WORLD")
    w_he = windows[CARD_WINDOW["HIGH ENERGY"]]
    w_dens = windows[CARD_WINDOW["DENSITY"]]
    w_knife = windows[CARD_WINDOW["NO KNIFE"]]
    w_ront = windows[CARD_WINDOW["STILL RONTGEN"]]

    fallback_labels = [
        (w_x[0] + 0.55, w_x[1] - 0.65, "X-RAYS"),
        (w_inv[0] + 0.5, w_inv[1] - 0.6, "INVISIBLE LIGHT"),
        (w_det[0] + 0.5, w_det[1] - 0.55, "A DETECTOR"),
        (w_world[0] + 0.45, min(w_world[1] - 0.35, pic_dur - 0.12), "YOUR WORLD"),
    ]
    fallback_cards = [
        (
            w_he[0] + 1.6,
            min(w_he[1] - 0.25, w_he[0] + 6.0),
            "HIGH ENERGY",
            "Light with more punch than your eyes catch — past ultraviolet.",
        ),
        (
            w_dens[0] + 1.8,
            min(w_dens[1] - 0.25, w_dens[0] + 6.0),
            "DENSITY",
            "Soft tissue lets more through; bone and metal stop more.",
        ),
        (
            w_knife[0] + 1.6,
            min(w_knife[1] - 0.25, w_knife[0] + 6.0),
            "NO KNIFE",
            "Doctors see inside a living body without surgery.",
        ),
        (
            w_ront[0] + 1.6,
            min(w_ront[1] - 0.2, w_ront[0] + 6.0, pic_dur - 0.1),
            "STILL RÖNTGEN",
            "Same idea — safer dose, clearer detector.",
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

    def snap_to_plate(start: float, owner: int, *, late_bias: float = 0.55) -> float:
        a0, a1 = windows[owner]
        if start < a0 + 0.2 or start > a1 - 0.8 or start >= pic_dur - 0.5:
            return a0 + late_bias
        return start

    raw = [
        (
            snap_to_plate(
                t_of("what are x-rays", "so what are x-rays", default=fallback_labels[0][0]),
                LABEL_WINDOW["X-RAYS"],
            ),
            3.8,
            "X-RAYS",
        ),
        (
            snap_to_plate(
                t_of("past ultraviolet", "electromagnetic spectrum", default=fallback_labels[1][0]),
                LABEL_WINDOW["INVISIBLE LIGHT"],
            ),
            3.6,
            "INVISIBLE LIGHT",
        ),
        (
            snap_to_plate(
                t_of("a detector", "cardboard once", default=fallback_labels[2][0]),
                LABEL_WINDOW["A DETECTOR"],
            ),
            3.8,
            "A DETECTOR",
        ),
        (
            snap_to_plate(
                t_of("dentist", "hospital", "your world", "everyday", default=fallback_labels[3][0]),
                LABEL_WINDOW["YOUR WORLD"],
                late_bias=0.5,
            ),
            3.6,
            "YOUR WORLD",
        ),
    ]
    labels: list[tuple[float, float, str]] = []
    for start, dur, name in raw:
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
            snap_to_plate(
                t_of("more punch", "high-energy light", "higher energy", default=fallback_cards[0][0]),
                CARD_WINDOW["HIGH ENERGY"],
                late_bias=1.6,
            ),
            4.0,
            "HIGH ENERGY",
            "Light with more punch than your eyes catch — past ultraviolet.",
        ),
        (
            snap_to_plate(
                t_of("map of density", "soft tissue more than bone", "draw a map of density", default=fallback_cards[1][0]),
                CARD_WINDOW["DENSITY"],
                late_bias=1.8,
            ),
            4.0,
            "DENSITY",
            "Soft tissue lets more through; bone and metal stop more.",
        ),
        (
            snap_to_plate(
                t_of("without a knife", "without surgery", "why is that groundbreaking", default=fallback_cards[2][0]),
                CARD_WINDOW["NO KNIFE"],
                late_bias=1.6,
            ),
            4.0,
            "NO KNIFE",
            "Doctors see inside a living body without surgery.",
        ),
        (
            snap_to_plate(
                t_of("safer dose", "clearer detector", "still", "röentgen", "roentgen", default=fallback_cards[3][0]),
                CARD_WINDOW["STILL RONTGEN"],
                late_bias=1.6,
            ),
            4.0,
            "STILL RÖNTGEN",
            "Same idea — safer dose, clearer detector.",
        ),
    ]
    cards: list[tuple[float, float, str, str]] = []
    for start, dur, title, body in cards_raw:
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
    size = 56
    fnt = font(size, italic=True)
    tw, th, _gap = measure_words(d, text, fnt)
    x = w - tw - 88
    y = 86
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
    # Wrap long body onto two lines if needed for card width
    body_line = body
    tw, th, _ = measure_words(d, title, title_f)
    bw, bh, _ = measure_words(d, body_line, body_f)
    max_body = 1180
    lines = [body_line]
    if bw > max_body:
        words = body_line.split()
        mid = len(words) // 2
        lines = [" ".join(words[:mid]), " ".join(words[mid:])]
        bw = max(measure_words(d, ln, body_f)[0] for ln in lines)
        bh = measure_words(d, lines[0], body_f)[1] * len(lines) + 6 * (len(lines) - 1)
    box_w = max(tw, bw) + pad_x * 2
    box_h = th + bh + pad_y * 2 + 14
    x0, y0 = 72, h - box_h - 78
    d.rounded_rectangle(
        (x0, y0, x0 + box_w, y0 + box_h),
        radius=22,
        fill=(18, 14, 12, 210),
    )
    draw_words(d, (x0 + pad_x, y0 + pad_y - 2), title, title_f, (246, 238, 224, 250))
    y_body = y0 + pad_y + th + 8
    for ln in lines:
        draw_words(d, (x0 + pad_x, y_body), ln, body_f, (230, 220, 204, 235))
        y_body += measure_words(d, ln, body_f)[1] + 6
    dest.parent.mkdir(parents=True, exist_ok=True)
    im.save(dest)


def render_chapter_stamp(dest: Path) -> None:
    """Quiet chapter open — place/title only, not a brand bumper."""
    w, h = 1920, 1080
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    text = "A New Kind of Seeing"
    fnt = font(42, italic=True)
    tw, th, _ = measure_words(d, text, fnt)
    x, y = 96, 120
    pad = 18
    d.rounded_rectangle(
        (x - pad, y - pad, x + tw + pad, y + th + pad),
        radius=14,
        fill=(12, 10, 8, 170),
    )
    draw_words(d, (x, y), text, fnt, (236, 228, 214, 245))
    dest.parent.mkdir(parents=True, exist_ok=True)
    im.save(dest)


def _assert_assets() -> None:
    if VO_TXT.name != "part05_a_new_kind_of_seeing_v02.txt" or not VO_TXT.exists():
        raise SystemExit("STOP: VO lock is part05_a_new_kind_of_seeing_v02.txt — do not use v01")
    got_txt = sha256(VO_TXT)
    if got_txt != VO_TXT_SHA:
        raise SystemExit(f"STOP: VO txt sha {got_txt} != locked {VO_TXT_SHA}")
    for path, expect in (
        (VO, VO_SHA),
        (VO_MP3, VO_MP3_SHA),
        (ALIGN, ALIGN_SHA),
    ):
        if not path.exists():
            raise SystemExit(f"STOP: missing VO master {path}")
        got = sha256(path)
        if got != expect:
            raise SystemExit(f"STOP: sha mismatch {path.name}: {got} != {expect}")
    if not BED.exists():
        raise SystemExit(f"STOP: missing bed {BED}")
    for name in PLATES:
        p = CLIPS / name
        if not p.exists() or p.stat().st_size < 100_000:
            raise SystemExit(f"STOP: missing plate {p}")
        got = sha256(p)
        expect = PLATE_SHA[name]
        if got != expect:
            raise SystemExit(f"STOP: plate sha {name}: {got} != {expect}")
    if len(PLATES) != 11:
        raise SystemExit(f"STOP: expect 11 plates 01→11; got {len(PLATES)}")
    # Explorer allowed once — plate 06 only
    explorers = [n for n in PLATES if "explorer" in n.lower()]
    if explorers != ["06_explorer_diagram_v07.mp4"]:
        raise SystemExit(f"STOP: Explorer plate must be exactly 06_explorer_diagram_v07; got {explorers}")


def write_land(
    digest: str,
    dur: float,
    vo_dur: float,
    pic_dur: float,
    mix_dur: float,
    labels: list[tuple[float, float, str]],
    cards: list[tuple[float, float, str, str]],
) -> None:
    plate_list = [
        {"file": name, "sha256": PLATE_SHA[name], "order": i + 1}
        for i, name in enumerate(PLATES)
    ]
    payload = {
        "film": "003_Invisible-Bones-X-Rays",
        "part": 5,
        "title": "A New Kind of Seeing",
        "status": "LANDED",
        "reason": "Part 05 rough v01 — KEEP 01_v18 CREATE v14 + 02–10 + 11_v10; Option A chapter overlay",
        "output_path": str(OUT),
        "sha256": digest,
        "duration_s": dur,
        "bytes": OUT.stat().st_size,
        "missing_paths": [],
        "vo_lock": {
            "text": str(VO_TXT.relative_to(PROJ)),
            "text_sha256": VO_TXT_SHA,
            "wav": str(VO.relative_to(PROJ)),
            "wav_sha256": VO_SHA,
            "mp3": str(VO_MP3.relative_to(PROJ)),
            "mp3_sha256": VO_MP3_SHA,
            "align": str(ALIGN.relative_to(PROJ)),
            "align_sha256": ALIGN_SHA,
            "duration_s": vo_dur,
        },
        "music_source": str(BED),
        "music_name": BED.name,
        "bed_vol": BED_VOL,
        "timing_board": "07_Edit-Project/parts/part-05_plates_v01.json",
        "clip_use_s": CLIP_USE,
        "xfade_s": XFADE,
        "picture_s": pic_dur,
        "mix_s": mix_dur,
        "vo_trim_s": max(0.0, vo_dur - mix_dur),
        "plates": plate_list,
        "plate_versions_verified": [
            {"file": name, "sha256": PLATE_SHA[name]} for name in PLATES
        ],
        "labels": [{"t0": a, "t1": b, "text": t} for a, b, t in labels],
        "teach_cards": [
            {"t0": a, "t1": b, "title": title, "body": body}
            for a, b, title, body in cards
        ],
        "cues": "07_Edit-Project/PRODUCTION_BRIEF_PART05_v01.md + PART05_ASSEMBLE_V01_CUES.md",
        "do_not": [
            "mint new Veo",
            "remint plates",
            "invent VO",
            "ping Ben",
            "Public upload",
        ],
        "landed_at": __import__("datetime").datetime.now(
            __import__("datetime").timezone(__import__("datetime").timedelta(hours=1))
        ).isoformat(),
        "house": (
            "Silent-readable + teaching density. Continuous 1x motion. "
            "Lab bed under VO. Explorer once on plate 06. Chapter overlay A New Kind of Seeing. "
            "No DNA helix. VO trimmed to picture (no freeze-pad)."
        ),
    }
    LAND.write_text(json.dumps(payload, indent=2) + "\n")


def main() -> None:
    _assert_assets()

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
            f"{vo_dur - mix_dur:.1f}s overhang cut for v02 (no freeze-pad; soft note OK)",
            flush=True,
        )

    chapter = LABEL_DIR / "chapter_stamp.png"
    render_chapter_stamp(chapter)

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

    # Chapter stamp early on plate 01, then side labels + teach cards
    overlays: list[tuple[str, float, float, Path]] = [
        ("chapter", 1.4, 4.8, chapter),
    ]
    overlays += [("label", a, b, p) for a, b, p in label_pngs]
    overlays += [("card", a, b, p) for a, b, p in card_pngs]

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

    # A/V duration match check
    v_dur = float(
        subprocess.check_output(
            [
                "ffprobe", "-v", "error", "-select_streams", "v:0",
                "-show_entries", "stream=duration", "-of", "default=nw=1:nk=1",
                str(OUT),
            ],
            text=True,
        ).strip()
        or dur
    )
    a_dur = float(
        subprocess.check_output(
            [
                "ffprobe", "-v", "error", "-select_streams", "a:0",
                "-show_entries", "stream=duration", "-of", "default=nw=1:nk=1",
                str(OUT),
            ],
            text=True,
        ).strip()
        or dur
    )
    if abs(v_dur - a_dur) > 0.08:
        raise SystemExit(f"STOP: A/V mismatch v={v_dur:.3f} a={a_dur:.3f}")

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
        "plate_sha256": PLATE_SHA,
        "labels": [{"t0": a, "t1": b, "text": t} for a, b, t in labels],
        "teach_cards": [
            {"t0": a, "t1": b, "title": title, "body": body}
            for a, b, title, body in cards
        ],
        "house": (
            "No Explorer. Silent-readable + teaching density. "
            "Continuous 1x motion. Ominous ward bed. No DNA helix. No Veo mint."
        ),
    }
    META.write_text(json.dumps(meta, indent=2) + "\n")
    write_land(digest, dur, vo_dur, pic_dur, mix_dur, labels, cards)

    print(f"LANDED {OUT}", flush=True)
    print(f"BYTES {OUT.stat().st_size}", flush=True)
    print(f"SHA256 {digest}", flush=True)
    print(f"DUR {dur:.3f} (mix {mix_dur:.3f})", flush=True)
    print(f"AV v={v_dur:.3f} a={a_dur:.3f}", flush=True)
    print(f"ICLOUD {ICLOUD} bytes={ICLOUD.stat().st_size}", flush=True)
    print(f"BED {BED.name} vol={BED_VOL} fade_out@{fade_start:.2f}", flush=True)
    print("PLATES " + " | ".join(PLATES), flush=True)
    print(f"META {META}", flush=True)
    print(f"LAND {LAND}", flush=True)


if __name__ == "__main__":
    main()
