#!/usr/bin/env python3
"""HOS 003 Part 04 rough v01 — KEEP 01/05/06 + remint v02 plates + VO v02 + ominous bed.

CoS assemble UNLOCKED after remint plate-first PASS.
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
CLIPS = PROJ / "04_Generated-Clips" / "part04"
VO_TXT = PROJ / "02_Voiceover/part04_berthas_ring_v02.txt"
VO_TXT_SHA = "45bea4466e68ce5cd7a1fa3e70745694e8fcaa979037de74c52a914cd47bb375"
VO = PROJ / "02_Voiceover/05_Master/hos_003_part04_vo_v02_draft.wav"
VO_SHA = "96274dd968681651b14f5b7cb0a49e3a3d1f8a90787a4a645db29a28864f7345"
VO_MP3 = PROJ / "02_Voiceover/05_Master/hos_003_part04_vo_v02_draft.mp3"
VO_MP3_SHA = "7f8cd470ebc43f51a67a7a2f288c74a5ae7a81247d3135bae482379f55137d9f"
ALIGN = PROJ / "02_Voiceover/05_Master/hos_003_part04_vo_v02_draft_align.json"
ALIGN_SHA = "483aafb8426644e13bb8878a3e48978e6903831ea1eddc7ff8159ef890268c7c"
BED = (
    VIDEO_PROJECTS
    / "001_How-Did-We-Discover-Germs/05_Music/hos_001_part01_ominous_ward_v14_norm.wav"
)
OUT = PROJ / "09_Final-Export/hos_003_part04_rough_v01.mp4"
ICLOUD = (
    Path.home()
    / "Library/Mobile Documents/com~apple~CloudDocs/HOS UAT"
    / "hos_003_part04_rough_v01.mp4"
)
WORK = PROJ / "07_Edit-Project/_part04_v01_work"
LABEL_DIR = PROJ / "07_Edit-Project/_part04_v01_labels"
META = PROJ / "07_Edit-Project/part04_rough_v01_land_meta.json"
LAND = PROJ / "07_Edit-Project/ASSEMBLE_LAND.json"
XFADE = 0.35
CLIP_USE = 7.9  # timing board part-03_plates_v01.json
BED_VOL = 0.34
FPS = 24
DIDOT = "/System/Library/Fonts/Supplemental/Didot.ttc"

PLATES = [
    "01_chapter_bertha_v01.mp4",
    "02_hand_on_plate_v02.mp4",
    "03_bones_and_ring_v02.mp4",
    "04_haunted_becomes_fact_v02.mp4",
    "05_letters_fly_v01.mp4",
    "06_labs_copy_tube_v01.mp4",
    "07_doctors_lean_in_v02.mp4",
    "08_bullet_break_map_v02.mp4",
    "09_body_as_map_v02.mp4",
    "10_why_groundbreaking_v02.mp4",
    "11_proof_hold_v02.mp4",
]

PLATE_SHA = {
    "01_chapter_bertha_v01.mp4": "aaa965401496001ee22aee81df1b22b1ff4aa23fbf12196ef4709346ae06da0d",
    "02_hand_on_plate_v02.mp4": "b06f98adb1c351d3b5dbfbfcada01beb6ee31d40d2e7ddd5709f9de313bea565",
    "03_bones_and_ring_v02.mp4": "3114e1d20eb87fe25eeffba7f303d533a800fa8b94d81d398293800e22fd1137",
    "04_haunted_becomes_fact_v02.mp4": "c34b2523e3d748ec454a11b10bb20e79748adcf02cad9523f329bafa745aabff",
    "05_letters_fly_v01.mp4": "14fe15df5251c5bc5b71bac0e4c7aff65db28fc1f6db07ded99bb4815595d486",
    "06_labs_copy_tube_v01.mp4": "1053af11faa9079eafb76d98f78cd50eb7afbc0ad003afd2cd48fa22b0a0d5b2",
    "07_doctors_lean_in_v02.mp4": "6dd55759a0e3128bc3b05c06a2c6bf4befa69448009a300573cf6e956f03b218",
    "08_bullet_break_map_v02.mp4": "7cf0b82359c5110a8799bab60288b19f4704f9e0a8244a746c7564a3ec6c4051",
    "09_body_as_map_v02.mp4": "bcd637c019741ca9255ab2ad68a197c8b3c12fba574ae13ec3536cc33e66d21b",
    "10_why_groundbreaking_v02.mp4": "3f143748d8f35723dece18a183036eed370fb6819dcc80f12f380b09243fd5a4",
    "11_proof_hold_v02.mp4": "a28f2d0a7ca5b341688e7a416c12118010a4721164a537a0c53a638ccc96fd41",
}

# Plate index for each side label / teach card (01→11 = 0..10)
LABEL_WINDOW = {
    "BERTHA'S RING": 2,
    "PROOF": 3,
    "MEDICINE": 6,
    "A NEW EYE": 9,
}
CARD_WINDOW = {
    "WITNESS": 1,
    "DENSITY": 2,
    "IT SPREADS": 4,
    "NO KNIFE": 9,
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
    w_ring = _win(windows, "BERTHA'S RING")
    w_proof = _win(windows, "PROOF")
    w_med = _win(windows, "MEDICINE")
    w_eye = _win(windows, "A NEW EYE")
    w_wit = windows[CARD_WINDOW["WITNESS"]]
    w_dens = windows[CARD_WINDOW["DENSITY"]]
    w_spread = windows[CARD_WINDOW["IT SPREADS"]]

    fallback_labels = [
        (w_ring[0] + 0.55, w_ring[1] - 0.65, "BERTHA'S RING"),
        (w_proof[0] + 0.5, w_proof[1] - 0.6, "PROOF"),
        (w_med[0] + 0.5, w_med[1] - 0.55, "MEDICINE"),
        (w_eye[0] + 0.45, min(w_eye[1] - 0.35, pic_dur - 0.12), "A NEW EYE"),
    ]
    fallback_cards = [
        (
            w_wit[0] + 1.6,
            min(w_wit[1] - 0.25, w_wit[0] + 6.0),
            "WITNESS",
            "A living hand makes the claim undeniable.",
        ),
        (
            w_dens[0] + 2.0,
            min(w_dens[1] - 0.25, w_dens[0] + 6.2),
            "DENSITY",
            "Metal stops more ray than bone — darker on the plate.",
        ),
        (
            w_spread[0] + 1.6,
            min(w_spread[1] - 0.25, w_spread[0] + 6.0),
            "IT SPREADS",
            "Labs copy the tube; the method travels.",
        ),
        (
            w_eye[0] + 1.8,
            min(w_eye[1] - 0.2, w_eye[0] + 6.2, pic_dur - 0.1),
            "NO KNIFE",
            "Medicine can ask the skeleton without opening the skin.",
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
                t_of("wedding ring", "bertha", "bones — and her wedding", default=fallback_labels[0][0]),
                LABEL_WINDOW["BERTHA'S RING"],
            ),
            3.8,
            "BERTHA'S RING",
        ),
        (
            snap_to_plate(
                t_of("haunted glow becomes a fact", "fact you can hold", default=fallback_labels[1][0]),
                LABEL_WINDOW["PROOF"],
            ),
            3.6,
            "PROOF",
        ),
        (
            snap_to_plate(
                t_of("doctors lean in", "doctors lean", default=fallback_labels[2][0]),
                LABEL_WINDOW["MEDICINE"],
            ),
            3.8,
            "MEDICINE",
        ),
        (
            snap_to_plate(
                t_of("diagnosis gains a new eye", "new eye", default=fallback_labels[3][0]),
                LABEL_WINDOW["A NEW EYE"],
                late_bias=0.5,
            ),
            3.6,
            "A NEW EYE",
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
                t_of("why her hand", "living person makes", default=fallback_cards[0][0]),
                CARD_WINDOW["WITNESS"],
                late_bias=1.6,
            ),
            4.0,
            "WITNESS",
            "A living hand makes the claim undeniable.",
        ),
        (
            snap_to_plate(
                t_of("a ring makes density", "density obvious", default=fallback_cards[1][0]),
                CARD_WINDOW["DENSITY"],
                late_bias=2.0,
            ),
            4.0,
            "DENSITY",
            "Metal stops more ray than bone — darker on the plate.",
        ),
        (
            snap_to_plate(
                t_of("letters fly", "labs copy the tube", default=fallback_cards[2][0]),
                CARD_WINDOW["IT SPREADS"],
                late_bias=1.5,
            ),
            3.8,
            "IT SPREADS",
            "Labs copy the tube; the method travels.",
        ),
        (
            snap_to_plate(
                t_of("without opening the skin", "ask the skeleton", "why is that groundbreaking", default=fallback_cards[3][0]),
                CARD_WINDOW["NO KNIFE"],
                late_bias=1.8,
            ),
            4.0,
            "NO KNIFE",
            "Medicine can ask the skeleton without opening the skin.",
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
    text = "Bertha's Ring"
    fnt = font(48, italic=True)
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
    if VO_TXT.name != "part04_berthas_ring_v02.txt" or not VO_TXT.exists():
        raise SystemExit("STOP: VO lock is part04_berthas_ring_v02.txt — do not use v01")
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
    # No Explorer this part
    for name in PLATES:
        if "explorer" in name.lower():
            raise SystemExit(f"STOP: No Explorer on Part 04 — found {name}")


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
        "part": 4,
        "title": "Bertha's Ring",
        "status": "LANDED",
        "reason": "Part 04 rough v01 — KEEP 01/05/06 + remint v02 8 plates; CoS assemble unlock after plate-first PASS",
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
        "timing_board": "07_Edit-Project/parts/part-04_plates_v01.json",
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
        "cues": "07_Edit-Project/PRODUCTION_BRIEF_PART04_v01.md",
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
            "Ominous ward bed under VO. No Explorer. "
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
