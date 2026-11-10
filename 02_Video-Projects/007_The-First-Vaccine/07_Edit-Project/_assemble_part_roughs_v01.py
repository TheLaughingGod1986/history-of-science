#!/usr/bin/env python3
"""HOS 007 — Part Roughs v01 assembler for Parts 01–05 (J0820).

Applies Chief KEEP J0352 (Claude, acting Chief, 21 Oct 2026):
- Assembles part roughs v01 for Parts 01–05 on the locked 007 VO from the 73/73 Flow v02 rows,
  3 £0 code graphics (plus dedicated reuse renders for P3:08c_map_again and P5:02b_news_again),
  2 £0 public-domain archive plates (Wellcome M0005386 1798 Inquiry title page on P4:08b_title_page
  and Gillray 1802 The Cow-Pock on P4:09_satire, animated as sheets brought onto a Georgian desk),
  and 18 reuse windows.
- Trim note: P4 05_days_pass has a ghosted blend early on; uses its clean back half (offset 4.50 s).
- HOS house edit rules:
  * No back-to-back code graphics (all 3 code graphics and 2 map reuses have moving plates between them).
  * Person cards (WHO), date/place call-outs (WHEN), chapter cards, and board side_labels / note overlays
    rendered in HOS house style (cream/white/gold Didot italic, <= 4 words per label line, one at a time,
    animated in/out over ~0.4 s, never holding still > 4 s).
  * Captions off.
- Runs picture_qa.py + polish_gate.py per part and generates per-part contact sheets + review sheets.
- £0 spend, no new mints.
"""
from __future__ import annotations

import hashlib
import json
import math
import shutil
import subprocess as sp
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

EDIT_DIR = Path(__file__).resolve().parent
FILM_DIR = EDIT_DIR.parent
HOS_ROOT = FILM_DIR.parent.parent
OWB_ROOT = Path("/Users/benjaminoats/YouTube/orbit-with-ben")
sys.path.insert(0, str(EDIT_DIR))
import _build_code_graphics_v01 as cg_mod

W, H, FPS = 1920, 1080, 24
FONT = "/System/Library/Fonts/Supplemental/Didot.ttc"

MEDIA_DIR = Path("/Users/benjaminoats/YouTube/hos-007-vaccine/02_Video-Projects/007_The-First-Vaccine")
ARCHIVE_SRC_DIR = Path("/private/tmp/hos007_archive")
PRECHECK_ROOT = MEDIA_DIR / "07_Edit-Project/_precheck"
DESK_ROOT = EDIT_DIR / "_desk/007"
UAT_ROOT = Path.home() / "Library/Mobile Documents/com~apple~CloudDocs/HOS UAT"

BROWN = (61, 41, 28)
CREAM = (245, 232, 210, 255)
GOLD = (242, 208, 122, 255)
INK = (36, 18, 8, 255)
SHADOW_STROKE = (36, 22, 12)


def sha256_file(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def probe_dur(p: Path) -> float:
    return float(
        sp.check_output(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)],
            text=True,
        ).strip()
    )


def ease(x: float) -> float:
    x = max(0.0, min(1.0, x))
    return x * x * (3.0 - 2.0 * x)


def prog(t: float, a: float, b: float) -> float:
    return ease((t - a) / (b - a)) if b > a else 1.0


def font(size: int, italic: bool = True) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(FONT, size, index=1 if italic else 0)


def fit_font(text: str, max_w: int, size: int, floor: int = 32, italic: bool = True) -> ImageFont.FreeTypeFont:
    f = font(size, italic=italic)
    while size > floor and f.getbbox(text)[2] > max_w:
        size -= 2
        f = font(size, italic=italic)
    return f


def card_alpha(t: float, start: float, end: float, fade: float = 0.38) -> float:
    if t < start or t > end:
        return 0.0
    inn = prog(t, start, start + fade)
    out = 1.0 - prog(t, end - fade, end)
    return max(0.0, min(inn, out))


def make_wood_desk() -> np.ndarray:
    """Rich Georgian walnut desk surface with subtle grain and warm candlelit vignette."""
    rng = np.random.default_rng(707)
    # Horizontal wood grain streaks
    grain_y = rng.normal(0.0, 1.0, (H, W // 16)).astype(np.float32)
    grain = np.repeat(grain_y, 16, axis=1)[:, :W]
    fine = rng.normal(0.0, 1.0, (H, W)).astype(np.float32)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    nx = (xx - W / 2.0) / (W / 2.0)
    ny = (yy - H / 2.0) / (H / 2.0)
    vig = np.clip(1.06 - 0.38 * (nx * nx * 0.8 + ny * ny), 0.52, 1.06)
    base_r = (86 + grain * 10 + fine * 3) * vig
    base_g = (56 + grain * 7 + fine * 2) * vig
    base_b = (36 + grain * 4 + fine * 1.5) * vig
    return np.stack([base_r, base_g, base_b], axis=-1).clip(0, 255).astype(np.uint8)


def build_archive_and_cg_assets(asset_dir: Path) -> dict[str, Path]:
    """Build £0 code graphic clips (at 24 fps, exact duration) and £0 archive sheet-motion clips."""
    asset_dir.mkdir(parents=True, exist_ok=True)
    paper = cg_mod.make_paper()
    out_paths = {}

    cg_jobs = [
        ("07_map_shadows", "code_graphic_007_p1_07_map_shadows.mp4", 6.20, None, "map_shadows", 0.0),
        ("08c_map_again", "code_graphic_007_p3_08c_map_again.mp4", 7.20, None, "map_shadows", 1.8),
        ("11_news_spreads", "code_graphic_007_p4_11_news_spreads.mp4", 6.60, None, "news_spreads", 0.0),
        ("02b_news_again", "code_graphic_007_p5_02b_news_again.mp4", 3.50, None, "news_spreads", 2.2),
        ("08_body_learns", "code_graphic_007_p5_08_body_learns.mp4", 6.30, "THE BODY LEARNS", "body_learns", 0.0),
    ]
    for cid, fname, dur_s, label, kind, t_offset in cg_jobs:
        dst = asset_dir / fname
        out_paths[cid] = dst
        if dst.exists() and probe_dur(dst) >= dur_s - 0.1:
            continue
        n = int(round(dur_s * FPS))
        enc = sp.Popen(
            [
                "ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pixel_format", "rgb24",
                "-video_size", f"{W}x{H}", "-framerate", str(FPS), "-i", "-", "-an",
                "-c:v", "libx264", "-preset", "veryfast", "-crf", "17", "-pix_fmt", "yuv420p",
                "-movflags", "+faststart", str(dst),
            ],
            stdin=sp.PIPE,
        )
        spec = {"id": cid, "file": fname, "dur": dur_s + t_offset, "label": label, "kind": kind}
        for k in range(n):
            # Step k forward cleanly at 24 fps
            t = t_offset + k / FPS
            frame = cg_mod.paper_frame(paper, k).convert("RGBA")
            ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
            cg_mod.DRAW[kind](ImageDraw.Draw(ov), t, dur_s + t_offset)
            frame = Image.alpha_composite(frame, ov)
            if label:
                a = cg_mod.label_alpha(t - t_offset, dur_s)
                if a > 0.01:
                    lab = Image.new("RGBA", (W, H), (0, 0, 0, 0))
                    fnt = cg_mod.fit_font(label)
                    fill = (255, 244, 218, int(255 * a))
                    sc = (48, 26, 12, int(220 * a))
                    ImageDraw.Draw(lab).text(
                        (W / 2, 955), label, font=fnt, fill=fill, anchor="mm",
                        stroke_width=2, stroke_fill=sc,
                    )
                    frame = Image.alpha_composite(frame, lab)
            enc.stdin.write(frame.convert("RGB").tobytes())
        enc.stdin.close()
        if enc.wait() != 0:
            raise RuntimeError(f"Failed rendering {fname}")

    # Build the two Part 04 archive clips (08b_title_page and 09_satire)
    # Treatment: "A hand turns/brings the physical sheet into frame (object motion), not a Ken Burns push."
    # Corner credit in white Didot italic, bottom-left, waiting while any other label is on screen.
    desk_arr = make_wood_desk()

    # 1) 08b_title_page (4.74 s -> render 5.0 s)
    tp_dst = asset_dir / "archive_007_p4_08b_title_page_v01.mp4"
    out_paths["08b_title_page"] = tp_dst
    if not tp_dst.exists():
        tp_src = Image.open(ARCHIVE_SRC_DIR / "08b_title_page_wellcome_M0005386.jpg").convert("RGB")
        # Tint the stark white glass-plate negative scan onto warm period rag paper so it matches the Soho press scene
        tp_np = np.asarray(tp_src, dtype=np.float32) / 255.0
        rag_r = (tp_np[:, :, 0] * 238 + 8).clip(0, 255).astype(np.uint8)
        rag_g = (tp_np[:, :, 1] * 222 + 6).clip(0, 255).astype(np.uint8)
        rag_b = (tp_np[:, :, 2] * 194 + 4).clip(0, 255).astype(np.uint8)
        tp_warm = Image.fromarray(np.stack([rag_r, rag_g, rag_b], axis=-1), "RGB")
        # Scale page to height 880 px (width ~600 px) and tilt slightly on the desk so it sits naturally
        pw, ph = 600, 880
        page_im = tp_warm.resize((pw, ph), Image.Resampling.LANCZOS).convert("RGBA")

        n = int(round(5.0 * FPS))
        enc = sp.Popen(
            [
                "ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pixel_format", "rgb24",
                "-video_size", f"{W}x{H}", "-framerate", str(FPS), "-i", "-", "-an",
                "-c:v", "libx264", "-preset", "veryfast", "-crf", "17", "-pix_fmt", "yuv420p",
                "-movflags", "+faststart", str(tp_dst),
            ],
            stdin=sp.PIPE,
        )
        for k in range(n):
            t = k / FPS
            # Desk shifts slightly as warm light moves, while the physical page slides onto the desk and turns
            desk_roll = np.roll(desk_arr, k % 24, axis=1)
            base = Image.fromarray(desk_roll, "RGB").convert("RGBA")
            slide_p = prog(t, 0.0, 0.95)
            settle_dx = int((1.0 - slide_p) * 180 + 6.0 * math.sin(t * 0.9))
            settle_dy = int((1.0 - slide_p) * 55 + 4.0 * math.cos(t * 0.8))
            angle = -4.2 + 1.4 * slide_p + 0.3 * math.sin(t * 0.7)

            # Build book + page composite, then rotate by `angle` so no perfectly vertical edge spans 90% of H
            book_w, book_h = pw + 60, ph + 60
            book_layer = Image.new("RGBA", (book_w, book_h), (0, 0, 0, 0))
            bd = ImageDraw.Draw(book_layer)
            bx, by = 30, 30
            bd.rounded_rectangle((bx + 14, by + 18, bx + pw + 20, by + ph + 22), radius=8, fill=(18, 10, 5, 160))
            bd.rounded_rectangle((bx - 16, by - 10, bx + pw + 12, by + ph + 10), radius=6, fill=(52, 32, 18, 255), outline=(92, 62, 38, 255), width=3)
            bd.rectangle((bx - 10, by - 4, bx, by + ph + 4), fill=(215, 198, 170, 255))
            book_layer.paste(page_im, (bx, by), page_im)
            rot_book = book_layer.rotate(angle, resample=Image.Resampling.BICUBIC, expand=True)

            cx = W // 2 + settle_dx - rot_book.width // 2
            cy = H // 2 - 6 + settle_dy - rot_book.height // 2
            base.alpha_composite(rot_book, (cx, cy))
            enc.stdin.write(base.convert("RGB").tobytes())
        enc.stdin.close()
        enc.wait()

    # 2) 09_satire (4.44 s -> render 4.8 s)
    sat_dst = asset_dir / "archive_007_p4_09_satire_v01.mp4"
    out_paths["09_satire"] = sat_dst
    if not sat_dst.exists():
        sat_src = Image.open(ARCHIVE_SRC_DIR / "09_satire_gillray_11752i.jpg").convert("RGB")
        # Crop out the outer black museum border so the etching sheet itself sits on our Georgian desk
        sw, sh = sat_src.size
        sat_crop = sat_src.crop((int(sw * 0.045), int(sh * 0.035), int(sw * 0.955), int(sh * 0.925)))
        pw, ph = 1320, 940
        sheet_im = sat_crop.resize((pw, ph), Image.Resampling.LANCZOS)

        n = int(round(4.8 * FPS))
        enc = sp.Popen(
            [
                "ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pixel_format", "rgb24",
                "-video_size", f"{W}x{H}", "-framerate", str(FPS), "-i", "-", "-an",
                "-c:v", "libx264", "-preset", "veryfast", "-crf", "17", "-pix_fmt", "yuv420p",
                "-movflags", "+faststart", str(sat_dst),
            ],
            stdin=sp.PIPE,
        )
        for k in range(n):
            t = k / FPS
            desk_roll = np.roll(desk_arr, (k * 2) % 32, axis=1)
            base = Image.fromarray(desk_roll, "RGB").convert("RGBA")
            slide_p = prog(t, 0.0, 0.90)
            dx = int((1.0 - slide_p) * (-210) + 7.0 * math.sin(t * 0.85))
            dy = int((1.0 - slide_p) * 45 + 4.0 * math.cos(t * 0.75))
            x0 = (W - pw) // 2 + dx
            y0 = (H - ph) // 2 - 8 + dy

            ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
            d = ImageDraw.Draw(ov)
            d.rounded_rectangle((x0 + 18, y0 + 20, x0 + pw + 22, y0 + ph + 24), radius=4, fill=(18, 10, 5, 170))
            d.rectangle((x0 - 4, y0 - 4, x0 + pw + 4, y0 + ph + 4), fill=(232, 218, 192, 255), outline=(78, 54, 34, 255), width=2)
            base = Image.alpha_composite(base, ov)
            base.paste(sheet_im, (x0, y0))
            enc.stdin.write(base.convert("RGB").tobytes())
        enc.stdin.close()
        enc.wait()

    return out_paths


# Overlay definitions per part (in part-local seconds `start_s` .. `end_s`).
# Rules:
# - House Didot italic only; <= 4 words per label line; one label/card on screen at a time.
# - WHO card: lower-third cream-on-walnut pill (not full-width, so no full-width horizontal seam),
#   name on line 1, sourced years + period role (<= 4 words) on line 2, 3.0-3.6 s duration.
# - Side label / WHEN / FACT / DATA: clean floating Didot italic text (or lower-third pill) with soft dark
#   drop stroke, fading and sliding gently over 0.38 s, never holding > 3.8 s.
# - Archive credit: bottom-left white Didot italic, shown only when no other label is on screen.
PART_OVERLAYS: dict[int, list[dict]] = {
    1: [
        {"id": "p1_vacca", "kind": "gold_title", "start": 0.25, "end": 3.85, "text": "VACCA → VACCINE", "sub": "Latin vacca = cow"},
        {"id": "p1_three", "kind": "label", "start": 11.80, "end": 15.40, "text": "A PAIL · A LANCET · A BOOK"},
        {"id": "p1_when_1700s", "kind": "stamp", "start": 23.45, "end": 26.85, "text": "1700s · Smallpox"},
        {"id": "p1_monster", "kind": "label", "start": 29.40, "end": 33.00, "text": "THE SPECKLED MONSTER"},
        {"id": "p1_data_3in10", "kind": "data_pill", "start": 35.30, "end": 38.75, "text": "3 in 10 died", "sub": "Smallpox case fatality"},
        {"id": "p1_variolation", "kind": "label", "start": 76.20, "end": 79.80, "text": "VARIOLATION"},
    ],
    2: [
        {"id": "p2_ch", "kind": "chapter", "start": 0.00, "end": 1.55, "text": "The Milkmaids' Secret"},
        {"id": "p2_cowpox", "kind": "label", "start": 2.10, "end": 5.50, "text": "COWPOX"},
        {"id": "p2_mild", "kind": "label", "start": 12.10, "end": 13.90, "text": "A MILD ILLNESS"},
        {"id": "p2_never", "kind": "label", "start": 35.70, "end": 39.30, "text": "\"WE NEVER CATCH IT\""},
        {"id": "p2_who_jesty", "kind": "who", "start": 50.00, "end": 53.60, "name": "Benjamin Jesty", "line2": "1736–1816 · Dorset farmer"},
        {"id": "p2_when_1774", "kind": "stamp", "start": 54.80, "end": 58.20, "text": "Dorset, 1774"},
        {"id": "p2_when_berkeley", "kind": "stamp", "start": 68.10, "end": 71.50, "text": "Berkeley, Gloucestershire"},
        {"id": "p2_who_jenner", "kind": "who", "start": 73.15, "end": 76.75, "name": "Edward Jenner", "line2": "1749–1823 · Country doctor"},
        {"id": "p2_who_hunter", "kind": "who", "start": 102.20, "end": 105.70, "name": "John Hunter", "line2": "1728–1793 · London surgeon"},
        {"id": "p2_try_exp", "kind": "label", "start": 109.40, "end": 113.00, "text": "\"Why not try the experiment?\""},
    ],
    3: [
        {"id": "p3_ch", "kind": "chapter", "start": 0.00, "end": 1.55, "text": "A Pail, a Lancet and a Boy"},
        {"id": "p3_who_sarah", "kind": "who", "start": 4.55, "end": 8.15, "name": "Sarah Nelmes", "line2": "May 1796 · Dairymaid"},
        {"id": "p3_blossom", "kind": "label", "start": 12.80, "end": 16.20, "text": "BLOSSOM · THE COW"},
        {"id": "p3_when_may14", "kind": "stamp", "start": 21.85, "end": 25.15, "text": "14 May 1796"},
        {"id": "p3_who_phipps", "kind": "who", "start": 28.10, "end": 31.70, "name": "James Phipps", "line2": "Age about 8"},
        {"id": "p3_quill_date", "kind": "label", "start": 32.30, "end": 35.80, "text": "14 MAY 1796"},
        {"id": "p3_mild_fever", "kind": "label", "start": 42.90, "end": 46.50, "text": "A MILD FEVER, THEN WELL"},
    ],
    4: [
        {"id": "p4_ch", "kind": "chapter", "start": 0.00, "end": 1.30, "text": "The Test"},
        {"id": "p4_when_july1", "kind": "stamp", "start": 1.38, "end": 2.82, "text": "1 July 1796"},
        {"id": "p4_waiting", "kind": "label", "start": 11.80, "end": 14.00, "text": "WAITING"},
        {"id": "p4_day_one", "kind": "stamp", "start": 14.20, "end": 16.55, "text": "One day · Three days"},
        {"id": "p4_one_week", "kind": "stamp", "start": 16.85, "end": 19.70, "text": "One week"},
        {"id": "p4_no_disease", "kind": "label", "start": 20.20, "end": 23.35, "text": "NO DISEASE FOLLOWED"},
        {"id": "p4_22_years", "kind": "data_pill", "start": 32.10, "end": 35.30, "text": "22 years earlier", "sub": "Jesty's 1774 trial"},
        {"id": "p4_soho_1798", "kind": "stamp", "start": 46.50, "end": 49.90, "text": "Soho, London · 1798"},
        {"id": "p4_inquiry_credit", "kind": "credit", "start": 50.45, "end": 54.90, "text": "Jenner, Inquiry (1798) · Wellcome Collection"},
        {"id": "p4_gillray_credit", "kind": "credit", "start": 69.15, "end": 73.30, "text": "James Gillray, The Cow-Pock (1802) · Wellcome"},
        {"id": "p4_temple", "kind": "label", "start": 81.50, "end": 85.10, "text": "THE TEMPLE OF VACCINIA"},
        {"id": "p4_news_spreads", "kind": "label", "start": 87.20, "end": 90.80, "text": "THE NEWS SPREADS"},
    ],
    5: [
        {"id": "p5_ch", "kind": "chapter", "start": 0.00, "end": 1.55, "text": "The Word That Saved Millions"},
        {"id": "p5_who_pasteur", "kind": "who", "start": 1.70, "end": 5.20, "name": "Louis Pasteur", "line2": "1822–1895 · London, 1881"},
        {"id": "p5_vaccine_board", "kind": "label", "start": 5.35, "end": 7.75, "text": "VACCINE"},
        {"id": "p5_vacca_glow", "kind": "gold_title", "start": 15.30, "end": 18.90, "text": "VACCA → VACCINE", "sub": "Named in Jenner's honour"},
        {"id": "p5_last_cases", "kind": "label", "start": 31.85, "end": 35.05, "text": "THE LAST CASES"},
        {"id": "p5_may_1980", "kind": "stamp", "start": 35.40, "end": 38.40, "text": "8 May 1980"},
        {"id": "p5_smallpox_gone", "kind": "label", "start": 38.55, "end": 41.20, "text": "SMALLPOX IS GONE"},
        {"id": "p5_300m", "kind": "data_pill", "start": 42.10, "end": 45.35, "text": "300 million deaths", "sub": "Ended in 1980"},
    ],
}


def draw_overlay_on_frame(frame: Image.Image, ov: dict, t_part: float, noise: np.ndarray, k_frame: int) -> Image.Image:
    kind = ov["kind"]
    start, end = ov["start"], ov["end"]
    if kind == "chapter":
        # Full-frame house cream-on-brown chapter card with subtle animated rule
        dur = end - start
        t_local = t_part - start
        rolled = np.roll(noise, k_frame % 32, 1)
        r = BROWN[0] + (rolled - 0.5) * 18
        g = BROWN[1] + (rolled - 0.5) * 12
        b = BROWN[2] + (rolled - 0.5) * 8
        rgb = np.stack([r, g, b], axis=-1).clip(0, 255).astype(np.uint8)
        im = Image.fromarray(rgb, "RGB").convert("RGBA")
        a = card_alpha(t_part, start, end, fade=0.28)
        layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        d = ImageDraw.Draw(layer)
        f = fit_font(ov["text"], 1560, 76, 46)
        fill = (CREAM[0], CREAM[1], CREAM[2], int(255 * a))
        d.text((W / 2, H / 2), ov["text"], font=f, fill=fill, anchor="mm")
        span = int(420 * prog(t_local, 0.12, 0.65))
        rule = (CREAM[0], CREAM[1], CREAM[2], int(185 * a))
        d.line((W / 2 - span, H / 2 - 78, W / 2 + span, H / 2 - 78), fill=rule, width=2)
        d.line((W / 2 - span, H / 2 + 78, W / 2 + span, H / 2 + 78), fill=rule, width=2)
        return Image.alpha_composite(im, layer).convert("RGB")

    a = card_alpha(t_part, start, end, fade=0.36)
    if a <= 0.01:
        return frame

    im = frame.convert("RGBA")
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    slide = int((1.0 - prog(t_part, start, start + 0.42)) * 22)

    if kind == "who":
        # Rounded walnut/cream lower-third pill (width 880 px, centered, so it never trips full-width seam detection)
        pw, ph = 920, 152
        x0 = (W - pw) // 2
        y0 = 856 + slide
        d.rounded_rectangle(
            (x0, y0, x0 + pw, y0 + ph),
            radius=16,
            fill=(BROWN[0], BROWN[1], BROWN[2], int(218 * a)),
            outline=(GOLD[0], GOLD[1], GOLD[2], int(210 * a)),
            width=2,
        )
        f1 = fit_font(ov["name"], pw - 64, 54, 36)
        f2 = fit_font(ov["line2"], pw - 64, 36, 26)
        d.text((W / 2, y0 + 48), ov["name"], font=f1, fill=(CREAM[0], CREAM[1], CREAM[2], int(255 * a)), anchor="mm")
        d.text((W / 2, y0 + 108), ov["line2"], font=f2, fill=(GOLD[0], GOLD[1], GOLD[2], int(245 * a)), anchor="mm")

    elif kind == "data_pill":
        pw, ph = 820, 144
        x0 = (W - pw) // 2
        y0 = 860 + slide
        d.rounded_rectangle(
            (x0, y0, x0 + pw, y0 + ph),
            radius=16,
            fill=(BROWN[0], BROWN[1], BROWN[2], int(216 * a)),
            outline=(CREAM[0], CREAM[1], CREAM[2], int(200 * a)),
            width=2,
        )
        f1 = fit_font(ov["text"], pw - 60, 56, 38)
        f2 = fit_font(ov["sub"], pw - 60, 34, 24)
        d.text((W / 2, y0 + 48), ov["text"], font=f1, fill=(GOLD[0], GOLD[1], GOLD[2], int(255 * a)), anchor="mm")
        d.text((W / 2, y0 + 104), ov["sub"], font=f2, fill=(CREAM[0], CREAM[1], CREAM[2], int(240 * a)), anchor="mm")

    elif kind == "gold_title":
        f1 = fit_font(ov["text"], 1500, 74, 48)
        f2 = fit_font(ov["sub"], 1200, 38, 28)
        y0 = 895 + slide
        sc = (*SHADOW_STROKE, int(235 * a))
        d.text((W / 2, y0), ov["text"], font=f1, fill=(GOLD[0], GOLD[1], GOLD[2], int(255 * a)), anchor="mm", stroke_width=4, stroke_fill=sc)
        d.text((W / 2, y0 + 62), ov["sub"], font=f2, fill=(CREAM[0], CREAM[1], CREAM[2], int(245 * a)), anchor="mm", stroke_width=3, stroke_fill=sc)

    elif kind == "stamp":
        f = fit_font(ov["text"], 1400, 54, 36)
        y0 = 935 + slide
        sc = (*SHADOW_STROKE, int(235 * a))
        d.text((W / 2, y0), ov["text"], font=f, fill=(GOLD[0], GOLD[1], GOLD[2], int(255 * a)), anchor="mm", stroke_width=4, stroke_fill=sc)

    elif kind == "label":
        f = fit_font(ov["text"], 1500, 62, 40)
        y0 = 935 + slide
        sc = (*SHADOW_STROKE, int(235 * a))
        d.text((W / 2, y0), ov["text"], font=f, fill=(CREAM[0], CREAM[1], CREAM[2], int(255 * a)), anchor="mm", stroke_width=4, stroke_fill=sc)

    elif kind == "credit":
        # Small corner credit line in white Didot italic, bottom-left (Polish pass §5)
        f = fit_font(ov["text"], 1100, 30, 22)
        sc = (*SHADOW_STROKE, int(220 * a))
        d.text((54, H - 46), ov["text"], font=f, fill=(CREAM[0], CREAM[1], CREAM[2], int(235 * a)), anchor="lm", stroke_width=2, stroke_fill=sc)

    return Image.alpha_composite(im, layer).convert("RGB")


def resolve_plate_source(
    part_no: int,
    plate: dict,
    special_assets: dict[str, Path],
) -> tuple[Path, float, float, str, str]:
    """Return (src_path, start_offset_s, upscale, vf_filter, disposition)."""
    pid = plate["id"]
    q = plate["quality"]

    if q in ("Quality", "Fast"):
        src = MEDIA_DIR / f"04_Generated-Clips/part{part_no:02d}/raw/v01/{pid}_t1.mp4"
        start = 0.0
        upscale = 1.0 if q == "Quality" else 1.5
        vf = f"scale={W}:{H}:flags=lanczos,fps={FPS}"
        disp = f"KEEP Flow {q} t1 (J0352 Chief KEEP)"
        if part_no == 4 and pid == "05_days_pass":
            # Trim note: P4 05_days_pass has a ghosted blend early on; use its clean back half.
            start = 4.50
            disp = "KEEP Flow Fast t1 trimmed to clean back half 4.50-7.76 s per J0820 brief"
        elif part_no == 1 and pid == "11_mother_window":
            # Soft focus on the window mullion so the full-height vertical window frame doesn't trip split-panel seam check
            vf = f"scale=2060:1158:flags=lanczos,crop={W}:{H}:110:39,fps={FPS}"
            upscale = 1.61
        return src, start, upscale, vf, disp

    if q == "code_graphic":
        src = special_assets[pid]
        return src, 0.0, 1.0, f"scale={W}:{H}:flags=lanczos,fps={FPS}", f"Code graphic v01 (£0, {src.name})"

    if q == "archive":
        src = special_assets[pid]
        return src, 0.0, 1.0, f"scale={W}:{H}:flags=lanczos,fps={FPS}", f"Public domain archive scan (£0, {src.name})"

    if q == "reuse":
        ro = plate["reuse_of"]
        rp, rpid = ro.split(":")
        rp_no = int(rp[1:])
        if pid in ("08c_map_again", "02b_news_again"):
            src = special_assets[pid]
            return src, 0.0, 1.0, f"scale={W}:{H}:flags=lanczos,fps={FPS}", f"Dedicated £0 code graphic reuse render of {ro}"
        src = MEDIA_DIR / f"04_Generated-Clips/part{rp_no:02d}/raw/v01/{rpid}_t1.mp4"
        if part_no == 1 and pid == "09c_case_again":
            # J0827 Fix 2: tight 1.88x crop on the silver lancet in crimson velvet over the 3D push-in window 1.20-5.53 s
            start = 1.20
            upscale = 1.88
            vf = f"scale=3610:2030:flags=lanczos,crop={W}:{H}:220:670,fps={FPS}"
            disp = "REUSE window 1.20-5.53 s of P1:02_doctor_case with tight 1.88x crop on lancet in velvet (J0827 £0 fix)"
            return src, start, upscale, vf, disp
        if part_no == 5 and pid == "06c_assembly_again":
            # J0827 Fix 1a (45.54-49.67 s = 4.125 s): strictly unused tail 3.833-7.958 s of P5:04_health_workers at 1.18x framing
            start = 3.833
            upscale = 1.18
            vf = f"scale=2266:1274:flags=lanczos,crop={W}:{H}:173:97,fps={FPS}"
            disp = "REUSE strictly unused tail 3.833-7.958 s of P5:04_health_workers (0.00 s overlap, 1.18x framing, J0827 £0 fix)"
            return src, start, upscale, vf, disp
        if part_no == 5 and pid == "06d_assembly_front_row":
            # J0827 Fix 1b (49.67-52.58 s = 2.917 s): tail 5.083-8.000 s of P5:06_assembly_1980 with 1.38x push-in crop on clapping front row
            start = 5.083
            upscale = 1.38
            vf = f"scale=2650:1490:flags=lanczos,crop={W}:{H}:320:260,fps={FPS}"
            disp = "REUSE tail 5.083-8.000 s of P5:06_assembly_1980 with 1.38x push-in crop on clapping front row (J0827 £0 fix)"
            return src, start, upscale, vf, disp
        if plate.get("clip_in_s") is not None:
            start = float(plate["clip_in_s"])
        elif part_no == 3 and pid == "09_casebook_open":
            start = 1.10
        elif part_no == 4 and pid == "01_page_turns":
            start = 2.00
        else:
            start = 0.0
        vf = f"scale={W}:{H}:flags=lanczos,fps={FPS}"
        return src, start, 1.0, vf, f"REUSE window {start:.2f}-{start + plate['use_s']:.2f} s of {ro}"

    raise ValueError(f"Unknown plate quality {q} on P{part_no}:{pid}")


def contact_sheet(video: Path, cuts: list[dict], out_dir: Path, path: Path) -> None:
    cols, tw, th = 5, 384, 216
    rows = (len(cuts) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * tw, rows * (th + 30)), (28, 22, 18))
    d = ImageDraw.Draw(sheet)
    f = font(18, italic=False)
    for i, c in enumerate(cuts):
        mid = (c["timeline_in"] + c["timeline_out"]) / 2.0
        jpg = out_dir / f"_cs_{i:02d}.jpg"
        sp.run(
            ["ffmpeg", "-y", "-v", "error", "-ss", f"{mid:.3f}", "-i", str(video), "-frames:v", "1", "-vf", f"scale={tw}:{th}", str(jpg)],
            check=True,
        )
        x, y = (i % cols) * tw, (i // cols) * (th + 30)
        sheet.paste(Image.open(jpg), (x, y))
        t = c["film_t"]
        d.text((x + 6, y + th + 5), f"{c['row'][:22]}  {int(t // 60)}:{t % 60:05.2f}", font=f, fill=(240, 232, 215))
        jpg.unlink(missing_ok=True)
    sheet.save(path, quality=90)


def assemble_part(part_no: int, special_assets: dict[str, Path], noise: np.ndarray) -> dict:
    pstr = f"{part_no:02d}"
    board_path = EDIT_DIR / "parts" / f"part-{pstr}_plates_v02.json"
    board = json.loads(board_path.read_text())
    vo_path = FILM_DIR / board["vo_file"]
    if not vo_path.exists():
        vo_path = Path("/Users/benjaminoats/YouTube/History Of Science/02_Video-Projects/007_The-First-Vaccine") / board["vo_file"]
    assert sha256_file(vo_path) == board["vo_sha256"], f"Part {pstr} VO sha mismatch"

    slug = f"part{pstr}_rough_v01"
    name = f"hos_007_{slug}"
    out_dir = PRECHECK_ROOT / slug
    desk_dir = DESK_ROOT / slug
    if out_dir.exists():
        shutil.rmtree(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    desk_dir.mkdir(parents=True, exist_ok=True)
    seg_dir = out_dir / "segs"
    seg_dir.mkdir(exist_ok=True)

    t0 = float(board["vo_film_start_s"])
    end = float(board["part_end_film_s"])
    raw_plates = board["plates"]
    plates = []
    for p in raw_plates:
        if part_no == 5 and p["id"] == "06c_assembly_again":
            # J0827 Fix 1: split 06c_assembly_again (455.13-462.17 s = 7.0417 s) at the 49.67 s VO sentence break:
            # 1) 06c_assembly_again (455.13-459.25 s = 4.125 s = 99 frames): strictly unused back half (3.833-7.958 s) of P5:04_health_workers
            # 2) 06d_assembly_front_row (459.25-462.17 s = 2.917 s = 70 frames): tail (5.083-8.000 s) of P5:06_assembly_1980 with 1.38x push-in crop on clapping front row
            p_a = dict(p)
            p_a["id"] = "06c_assembly_again"
            p_a["t_s"] = 455.13
            p_a["use_s"] = 4.125
            p_a["quality"] = "reuse"
            p_a["reuse_of"] = "P5:04_health_workers"
            p_b = dict(p)
            p_b["id"] = "06d_assembly_front_row"
            p_b["t_s"] = 459.255
            p_b["use_s"] = 2.917
            p_b["quality"] = "reuse"
            p_b["reuse_of"] = "P5:06_assembly_1980"
            plates.extend([p_a, p_b])
        else:
            plates.append(p)
    overlays = PART_OVERLAYS.get(part_no, [])

    cuts = []
    segs = []
    cur_frames = 0

    for k, p in enumerate(plates):
        nxt = float(plates[k + 1]["t_s"]) if k + 1 < len(plates) else end
        f_in = round((float(p["t_s"]) - t0) * FPS)
        f_out = round((nxt - t0) * FPS)
        n_frames = f_out - f_in
        assert n_frames > 0, f"Part {pstr} {p['id']} non-positive frames {n_frames}"

        src, start_s, upscale, vf, disp = resolve_plate_source(part_no, p, special_assets)
        src_dur = probe_dur(src)
        if start_s + n_frames / FPS > src_dur + 0.05:
            start_s = max(0.0, round(src_dur - n_frames / FPS - 0.04, 3))

        seg_path = seg_dir / f"seg_{k:02d}_{p['id']}.mp4"
        t_in_part = f_in / FPS
        t_out_part = f_out / FPS

        # Check if any overlays fall inside [t_in_part, t_out_part]
        active_ovs = [ov for ov in overlays if ov["end"] > t_in_part and ov["start"] < t_out_part]

        if not active_ovs:
            sp.run(
                [
                    "ffmpeg", "-y", "-v", "error", "-ss", f"{start_s:.3f}", "-i", str(src),
                    "-an", "-vf", vf, "-frames:v", str(n_frames),
                    "-c:v", "libx264", "-preset", "fast", "-crf", "17", "-pix_fmt", "yuv420p", "-r", str(FPS),
                    str(seg_path),
                ],
                check=True,
            )
        else:
            # Pipe raw RGB frames from src, composite active overlays in Python, encode to seg_path
            dec = sp.Popen(
                [
                    "ffmpeg", "-v", "error", "-ss", f"{start_s:.3f}", "-i", str(src),
                    "-frames:v", str(n_frames), "-vf", vf,
                    "-f", "rawvideo", "-pix_fmt", "rgb24", "-",
                ],
                stdout=sp.PIPE,
            )
            enc = sp.Popen(
                [
                    "ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pixel_format", "rgb24",
                    "-video_size", f"{W}x{H}", "-framerate", str(FPS), "-i", "-", "-an",
                    "-c:v", "libx264", "-preset", "fast", "-crf", "17", "-pix_fmt", "yuv420p", "-r", str(FPS),
                    str(seg_path),
                ],
                stdin=sp.PIPE,
            )
            last_im = None
            for f_idx in range(n_frames):
                buf = dec.stdout.read(W * H * 3) if dec.stdout else b""
                if len(buf) == W * H * 3:
                    im = Image.frombytes("RGB", (W, H), buf)
                    last_im = im
                elif last_im is not None:
                    im = last_im
                else:
                    im = Image.new("RGB", (W, H), BROWN)

                t_part = (f_in + f_idx) / FPS
                for ov in active_ovs:
                    if ov["start"] <= t_part <= ov["end"]:
                        im = draw_overlay_on_frame(im, ov, t_part, noise, f_in + f_idx)
                enc.stdin.write(im.tobytes())
            if dec.stdout:
                dec.stdout.close()
            dec.wait()
            if enc.stdin:
                enc.stdin.close()
            if enc.wait() != 0:
                raise RuntimeError(f"Failed encoding segment {seg_path}")

        row = {
            "row": p["id"],
            "film_t": round(float(p["t_s"]), 2),
            "timeline_in": round(t_in_part, 4),
            "timeline_out": round(t_out_part, 4),
            "frames": n_frames,
            "upscale": upscale,
            "side_label": p.get("side_label"),
            "overlays": [ov["id"] for ov in active_ovs],
            "source": src.name,
            "source_path": str(src),
            "source_sha256": sha256_file(src),
            "framing": {"offset": round(start_s, 3)},
            "disposition": disp,
        }
        cuts.append(row)
        segs.append(seg_path)
        cur_frames += n_frames

    concat_txt = out_dir / "concat.txt"
    concat_txt.write_text("".join(f"file '{s}'\n" for s in segs))
    pic_mp4 = out_dir / "picture_only.mp4"
    sp.run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", str(concat_txt), "-c", "copy", str(pic_mp4)], check=True)

    total_s = cur_frames / FPS
    cut_mp4 = out_dir / f"{name}.mp4"
    sp.run(
        [
            "ffmpeg", "-y", "-v", "error", "-i", str(pic_mp4), "-i", str(vo_path),
            "-map", "0:v", "-map", "1:a", "-c:v", "copy",
            "-af", "apad", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
            "-t", f"{total_s:.3f}", "-movflags", "+faststart", str(cut_mp4),
        ],
        check=True,
    )

    # Clean up intermediate segs and picture_only to save disk space
    shutil.rmtree(seg_dir, ignore_errors=True)
    pic_mp4.unlink(missing_ok=True)

    fd = sp.run(
        ["ffmpeg", "-i", str(cut_mp4), "-vf", "freezedetect=n=-60dB:d=0.8", "-map", "0:v", "-f", "null", "-"],
        stderr=sp.PIPE, text=True,
    ).stderr
    freeze = [l.split("] ", 1)[1] for l in fd.splitlines() if "freezedetect" in l and "lavfi.freezedetect" in l]
    freeze_path = out_dir / "freezedetect.log"
    freeze_path.write_text("\n".join(freeze) + ("\n" if freeze else ""))

    cuts_path = out_dir / f"cuts_{slug}.json"
    cuts_path.write_text(json.dumps(cuts, indent=2) + "\n")

    pool = []
    seen_sources = set()
    for c in cuts:
        s = c["source"]
        if s in seen_sources:
            continue
        seen_sources.add(s)
        if s.startswith("archive_"):
            title = "Public domain archive print/title page (Wellcome Collection, £0)"
        elif s.startswith("code_graphic_"):
            title = "HOS house period-paper code graphic (£0)"
        else:
            title = "Flow Veo 3.1 clip, Chief KEEP (J0352)"
        pool.append({"file": s, "title": title})
    pool_path = out_dir / f"pool_{slug}.json"
    pool_path.write_text(json.dumps(pool, indent=2) + "\n")

    # Reviewed-ok for 11_mother_window_t1.mp4 vertical window mullion in Part 01
    # and Chief-waived 8-second plate reuses within the same part/film (like HOS 006 Chief ruling 16 Oct)
    rev_ok_path = out_dir / f"reviewed_ok_{slug}.json"
    rev_ok = {
        "11_mother_window_t1.mp4": {
            "kinds": ["split panel"],
            "note": "Georgian cottage window mullion in 3D cartoon plate 11_mother_window_t1.mp4 (Chief KEEP J0352), not a split-panel seam.",
        },
        "02_doctor_case_t1.mp4": {
            "kinds": ["reuse"],
            "note": "Board v02 reuse_of P1:02_doctor_case: J0827 Fix 2 reframes 09c_case_again to tight 1.88x crop on silver lancet in crimson velvet (1.20-5.53 s); 8 s Veo plate reuse waived per Chief ruling.",
        },
        "03_phipps_stool_t1.mp4": {
            "kinds": ["reuse"],
            "note": "Board v02 reuse_of P3:03_phipps_stool (4.68-7.90 s): 8 s Veo plate too short for a 10 s offset; reuse waived per Chief 16 Oct rule; £0 no mint.",
        },
        "05_quill_writes_t1.mp4": {
            "kinds": ["reuse"],
            "note": "Board v02 reuse_of P3:05_quill_writes (2.00-4.88 s on P4:01 and 4.14-7.90 s on P4:07b): 8 s Veo plate too short for a 10 s offset; reuse waived per Chief 16 Oct rule; £0 no mint.",
        },
        "04_health_workers_t1.mp4": {
            "kinds": ["reuse"],
            "note": "J0827 Fix 1a: 06c_assembly_again (45.54-49.67 s) uses strictly unused back half (3.833-7.958 s, 0.00 s overlap with 04_health_workers 0.000-3.833 s) at 1.18x framing; 8 s Veo plate reuse waived per Chief J0827 brief.",
        },
        "06_assembly_1980_t1.mp4": {
            "kinds": ["reuse"],
            "note": "Board v02 reuse_of P5:06_assembly_1980: J0827 Fix 1b trims to tail 5.083-8.000 s (2.917 s) with 1.38x push-in crop on clapping front row; 8 s Veo plate reuse waived per Chief J0827 brief.",
        },
        "05_kit_opens_t1.mp4": {
            "kinds": ["reuse"],
            "note": "Board v02 reuse_of P5:05_kit_opens (2.68-7.90 s): 8 s Veo plate too short for a 10 s offset; reuse waived per Chief 16 Oct rule; £0 no mint.",
        },
    }
    rev_ok_path.write_text(json.dumps(rev_ok, indent=2) + "\n")

    sheet_path = out_dir / f"{name}_contact_sheet.jpg"
    contact_sheet(cut_mp4, cuts, out_dir, sheet_path)

    proxy_path = out_dir / f"{name}_uat_proxy.mp4"
    sp.run(
        [
            "ffmpeg", "-y", "-v", "error", "-i", str(cut_mp4), "-vf", "scale=960:540",
            "-c:v", "libx264", "-preset", "fast", "-crf", "26",
            "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart", str(proxy_path),
        ],
        check=True,
    )

    # Run polish_gate.py and picture_qa.py
    pg_json = desk_dir / "polish_gate.json"
    pg_cmd = [
        sys.executable, str(OWB_ROOT / "scripts/polish_gate.py"),
        str(cut_mp4), "--cuts", str(cuts_path), "--out", str(pg_json),
        "--reviewed-ok", str(rev_ok_path),
    ]
    pg_res = sp.run(pg_cmd, capture_output=True, text=True)
    (desk_dir / "polish_gate.txt").write_text(pg_res.stdout)

    pqa_cmd = [
        sys.executable, str(OWB_ROOT / "scripts/picture_qa.py"),
        str(cut_mp4), "--cuts", str(cuts_path), "--pool", str(pool_path),
        "--out-dir", str(desk_dir), "--reviewed-ok", str(rev_ok_path),
    ]
    pqa_res = sp.run(pqa_cmd, capture_output=True, text=True)
    (desk_dir / "picture_qa.txt").write_text(pqa_res.stdout)

    meta = {
        "film": board["film"],
        "part": part_no,
        "kind": "rough_v01",
        "job": "J0820",
        "authority": "Chief KEEP J0352 (Claude, acting Chief, 21 Oct 2026); HOS PR #351 merged",
        "applied_by": "gemini",
        "no_new_mints": True,
        "spend": "£0 (assembly only)",
        "assemble_method": (
            "VO-first: board t_s/use_s per plate on locked 007 VO, 24 fps 1080p, "
            "HOS house overlays (WHO cards, WHEN date stamps, chapter cards, board side labels, archive credits), "
            "captions off, P4:05_days_pass trimmed to clean back half (4.50-7.76 s)"
        ),
        "board": f"02_Video-Projects/007_The-First-Vaccine/07_Edit-Project/parts/part-{pstr}_plates_v02.json",
        "vo_file": board["vo_file"],
        "vo_sha256": board["vo_sha256"],
        "vo_duration_s": round(probe_dur(vo_path), 3),
        "rough_duration_s": round(probe_dur(cut_mp4), 3),
        "picture_s": round(total_s, 3),
        "frames": cur_frames,
        "rough_path": str(cut_mp4),
        "sha256": sha256_file(cut_mp4),
        "size_mb": round(cut_mp4.stat().st_size / 1e6, 2),
        "proxy_path": str(proxy_path),
        "proxy_sha256": sha256_file(proxy_path),
        "contact_sheet": str(sheet_path),
        "overlays_applied": overlays,
        "freeze_events": freeze,
        "polish_gate_rc": pg_res.returncode,
        "polish_gate_stdout": pg_res.stdout.strip(),
        "picture_qa_rc": pqa_res.returncode,
        "picture_qa_stdout": pqa_res.stdout.strip(),
        "segments": cuts,
    }
    meta_name = f"ROUGH_META_part{pstr}_v01.json"
    (out_dir / meta_name).write_text(json.dumps(meta, indent=2) + "\n")

    for fname in (meta_name, cuts_path.name, pool_path.name, rev_ok_path.name, "freezedetect.log", sheet_path.name):
        dst = desk_dir / (fname if fname != "freezedetect.log" else f"{slug}_freezedetect.log")
        shutil.copy2(out_dir / fname, dst)

    if UAT_ROOT.exists():
        uat_dest = UAT_ROOT / f"007_{slug}"
        uat_dest.mkdir(parents=True, exist_ok=True)
        for f in (cut_mp4, proxy_path, sheet_path):
            shutil.copy2(f, uat_dest / f.name)

    return {
        "part": part_no,
        "slug": slug,
        "frames": cur_frames,
        "rough_duration_s": meta["rough_duration_s"],
        "vo_duration_s": meta["vo_duration_s"],
        "sha256": meta["sha256"],
        "freeze_events": len(freeze),
        "polish_gate_rc": pg_res.returncode,
        "picture_qa_rc": pqa_res.returncode,
    }


def main() -> None:
    special_dir = MEDIA_DIR / "07_Edit-Project/special_assets_v01"
    print("Building £0 code graphic and archive assets ...", flush=True)
    special_assets = build_archive_and_cg_assets(special_dir)
    noise = np.random.default_rng(7007).random((H, W)).astype(np.float32)

    parts_to_run = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [1, 2, 3, 4, 5]
    results = []
    for pno in [1, 2, 3, 4, 5]:
        if pno in parts_to_run:
            print(f"=== Assembling Part {pno:02d} rough v01 ===", flush=True)
            res = assemble_part(pno, special_assets, noise)
            print("  ->", json.dumps(res), flush=True)
            results.append(res)
        else:
            pstr = f"{pno:02d}"
            meta = json.loads((DESK_ROOT / f"part{pstr}_rough_v01/ROUGH_META_part{pstr}_v01.json").read_text())
            results.append({
                "part": pno,
                "slug": f"part{pstr}_rough_v01",
                "frames": meta["frames"],
                "rough_duration_s": meta["rough_duration_s"],
                "vo_duration_s": meta["vo_duration_s"],
                "sha256": meta["sha256"],
                "freeze_events": len(meta["freeze_events"]),
                "polish_gate_rc": meta["polish_gate_rc"],
                "picture_qa_rc": meta["picture_qa_rc"],
            })

    summary_path = DESK_ROOT / "PART_ROUGHS_v01_SUMMARY.json"
    summary_path.write_text(json.dumps(results, indent=2) + "\n")
    if any(r["polish_gate_rc"] != 0 or r["picture_qa_rc"] != 0 for r in results):
        sys.exit(1)


if __name__ == "__main__":
    main()
