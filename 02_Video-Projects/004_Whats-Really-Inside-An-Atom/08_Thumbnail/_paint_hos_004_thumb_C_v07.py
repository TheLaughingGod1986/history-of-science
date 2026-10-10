#!/usr/bin/env python3
"""HOS 004 thumb C v07: repaint "THE HIDDEN NUMBER" with the tiles painted into the scene.

Thumb audit 9 Oct item 1 (v06 tiles were a pasted rectangle, right third smeared); Claude on
OWB #99 (comment 6084771583): repaint C as v07 under HOS rules 2.1-2.8, Te 52 / I 53 hand-lettered.

  paint [--n N]       Vertex gemini-2.5-flash-image plates (blank tiles, painted title) -> _assets_v07/
  letter <plate.jpg>  hand-letter Te 52 / I 53 on the plate's tile faces -> Selected/ + preview
  letter ... --v07b   same plate, 52/53 about 2x in one ink style -> ..._v07b (desk #180, J0106)

Python: ~/.venvs/hos-vertex/bin/python for `paint`. Media stays out of git. Nothing to Studio.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
sys.path.insert(0, str(REPO / "04_Audio" / "tools"))
from ai_spend_hook import spend as ai_spend  # noqa: E402

ASSETS = HERE / "_assets_v07"
SELECTED = HERE / "Selected"
LOG = HERE / "THUMB_C_V07_LOG.json"
STEM = "hos_004_thumb_C_hidden_number_live_v07"
PREVIEW_TOOL = REPO / "00_Brand/Channel-Setup/tools/thumb_preview.py"
STYLE_SHEET = REPO / "00_Brand/Channel-Setup/tools/style_sheet.py"

LIVE_A = HERE / "Selected/hos_004_thumb_A_atom_live_v04.jpg"
OLD_C = HERE / "Selected/hos_004_thumb_C_hidden_number_live_v04.jpg"
EXPLORER_REF = REPO / "01_Character/05_Generation-References/hos-explorer-reference-v01.jpg"

PROJECT = "gen-lang-client-0538779324"
LOCATION = "us-central1"
IMAGE_MODEL = "gemini-2.5-flash-image"
USD_PER_STILL = 0.039
GBP_PER_USD = 0.80
MAX_PAINTS = 4

W, H = 1280, 720
CREAM = (245, 232, 200)
GOLD = (232, 178, 48)
INK = (28, 18, 10)
SHADOW = (12, 8, 4)
GEORGIA = "/System/Library/Fonts/Supplemental/Georgia Bold.ttf"
# Georgia's old-style figures make 52 read as 5 squared; numbers need lining figures.
NUMERALS = "/System/Library/Fonts/Supplemental/Times New Roman Bold.ttf"

PROMPT = (
    "Image 1 is the live History of Science long thumbnail: match its premium 3D cartoon painting, "
    "warm golden library light, bookshelves, green curtain, arched window, and its painted serif "
    "title lettering with gold flourishes exactly. Image 2 is the earlier layout of this thumbnail, "
    "for composition only; do not copy its text or its tile positions. Image 3 is the Explorer: match "
    "him exactly (round thin gold glasses, teal long coat, tan waistcoat, brown bow tie, messy brown "
    "hair, satchel), exactly one Explorer.\n\n"
    "Paint a new 16:9 thumbnail in the same golden library. Hero object: two large square "
    "periodic-table element tiles side by side, standing upright on a polished wooden desk, "
    "painted as solid physical objects in the scene: thick carved wooden frames, smooth cream "
    "enamel faces, soft contact shadows on the desk, warm window light and gentle rim glow on "
    "their edges, the right-hand tile glowing slightly warmer gold. The tile faces are COMPLETELY "
    "BLANK: no letters, no numbers, no symbols, no marks of any kind on them. Together the two "
    "tiles fill about the middle-right half of the frame, from about 40% to 88% of the width, "
    "tops at about 15% of the height, bottoms resting on the desk at about 78% of the height. "
    "Both tiles fully in frame with clear space around them. Keep the bottom-right corner of "
    "the frame empty desk and shadow only (a duration badge sits there).\n\n"
    "Upper left: the painted title lettering in the same style as Image 1, two lines: 'THE HIDDEN' "
    "in cream, and below it 'NUMBER' larger in gold, with small gold flourishes above and below. "
    "Spell it exactly THE HIDDEN NUMBER. No other text anywhere in the picture.\n\n"
    "Lower left: the Explorer small, about a third of the frame height, standing at the desk, "
    "looking up at the tiles with curiosity. He is a garnish, not the subject.\n\n"
    "HARD REJECT: any text other than THE HIDDEN NUMBER, letters or numbers on the tiles, flat "
    "shapes, split panels, photoreal, a plain dark background, objects cut off by the frame edge, "
    "anything in the bottom-right corner, logos, an orange robot."
)


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def load_log() -> dict:
    if LOG.exists():
        return json.loads(LOG.read_text())
    return {"film": "004_Whats-Really-Inside-An-Atom", "what": "thumb C v07 repaint",
            "authority": "OWB #99 comment 6084771583 (Claude, 9 Oct 2026); job J0097",
            "model": IMAGE_MODEL, "path": "vertex", "vertex_project": PROJECT,
            "prompt": PROMPT, "paints": [], "lettered": []}


def save_log(log: dict) -> None:
    log["cost_usd_total"] = round(sum(p["cost_usd"] for p in log["paints"]), 3)
    LOG.write_text(json.dumps(log, indent=2, ensure_ascii=False) + "\n")


def paint(n: int) -> None:
    import google.auth
    from google import genai
    from google.genai import types

    log = load_log()
    if len(log["paints"]) + n > MAX_PAINTS:
        raise SystemExit(f"STOP: {len(log['paints'])} paints already; cap is {MAX_PAINTS}")
    creds, _ = google.auth.default(scopes=["https://www.googleapis.com/auth/cloud-platform"])
    if not creds:
        raise SystemExit("STOP: no ADC")
    c = genai.Client(vertexai=True, project=PROJECT, location=LOCATION)
    parts = [types.Part.from_bytes(data=p.read_bytes(), mime_type="image/jpeg")
             for p in (LIVE_A, OLD_C, EXPLORER_REF)] + [PROMPT]
    ASSETS.mkdir(parents=True, exist_ok=True)
    for _ in range(n):
        k = len(log["paints"]) + 1
        dest = ASSETS / f"{STEM}_plate{k:02d}.jpg"
        print(f"PAINT {k} model={IMAGE_MODEL} path=vertex", flush=True)
        r = c.models.generate_content(
            model=IMAGE_MODEL, contents=parts,
            config=types.GenerateContentConfig(response_modalities=["IMAGE"],
                                               image_config=types.ImageConfig(aspect_ratio="16:9")))
        data = None
        for cand in r.candidates or []:
            for part in (cand.content.parts if cand.content else []) or []:
                if part.inline_data and part.inline_data.data:
                    data = part.inline_data.data
        log["paints"].append({"k": k, "file": dest.name if data else None,
                              "cost_usd": USD_PER_STILL, "at": now()})
        save_log(log)
        ai_spend("vertex", round(USD_PER_STILL * GBP_PER_USD, 3), "HOS:004",
                 f"thumb C v07 plate {k:02d} ({IMAGE_MODEL})", by="cursor")
        if not data:
            print(f"  no image for paint {k}", flush=True)
            continue
        tmp = dest.with_suffix(".bin")
        tmp.write_bytes(data)
        subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", str(tmp),
                        "-vf", f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H}",
                        "-frames:v", "1", "-q:v", "2", str(dest)], check=True)
        tmp.unlink(missing_ok=True)
        print(f"SAVED {dest}", flush=True)


def paint_word(draw: ImageDraw.ImageDraw, text: str, *, cx: int, cy: int, size: int,
               fill: tuple[int, int, int], font: str = GEORGIA) -> None:
    """The cream/gold painted bevel used on C v06 for Te / I and 52 / 53."""
    f = ImageFont.truetype(font, size)
    l, t, r, b = draw.textbbox((0, 0), text, font=f)
    x = int(cx - (r - l) / 2 - l)
    y = int(cy - (b - t) / 2 - t)
    for dx, dy in ((4, 5), (2, 3)):
        draw.text((x + dx, y + dy), text, font=f, fill=SHADOW)
    draw.text((x, y), text, font=f, fill=INK, stroke_width=max(3, size // 18), stroke_fill=INK)
    draw.text((x, y), text, font=f, fill=fill)


def number_v07b(draw: ImageDraw.ImageDraw, text: str, *, x0: int, y0: int, fw: int, fh: int) -> None:
    """v07b (desk #180 6085214049): 52 and 53 in one neutral style, cap height ~25% of the tile,
    top-left inside the face, dark ink with a light outline so neither reads as the answer."""
    size = int(fh * 0.34)
    f = ImageFont.truetype(NUMERALS, size)
    l, t, r, b = draw.textbbox((0, 0), text, font=f)
    x = x0 + int(fw * 0.10) - l
    y = y0 + int(fh * 0.07) - t
    stroke = max(3, size // 24)
    draw.text((x + 4, y + 5), text, font=f, fill=SHADOW, stroke_width=stroke, stroke_fill=SHADOW)
    draw.text((x, y), text, font=f, fill=INK, stroke_width=stroke, stroke_fill=CREAM)


def letter(plate: Path, te: tuple[int, int, int, int], i: tuple[int, int, int, int],
           v07b: bool = False) -> None:
    im = Image.open(plate).convert("RGB")
    if im.size != (W, H):
        raise SystemExit(f"plate is {im.size}, expected {(W, H)}")
    draw = ImageDraw.Draw(im)
    for sym, num, (x0, y0, x1, y1), col in (("Te", "52", te, CREAM), ("I", "53", i, GOLD)):
        fw, fh = x1 - x0, y1 - y0
        if v07b:
            number_v07b(draw, num, x0=x0, y0=y0, fw=fw, fh=fh)
        else:
            n_size = max(40, int(fh * 0.19))
            paint_word(draw, num, cx=x0 + int(fw * 0.21), cy=y0 + int(fh * 0.15), size=n_size,
                       fill=col, font=NUMERALS)
        s_size = max(110, int(min(fw * 0.62, fh * 0.55)))
        paint_word(draw, sym, cx=x0 + fw // 2, cy=y0 + int(fh * 0.58), size=s_size, fill=col)
    stem = f"{STEM}b" if v07b else STEM
    SELECTED.mkdir(parents=True, exist_ok=True)
    jpg = SELECTED / f"{stem}.jpg"
    im.save(SELECTED / f"{stem}.png")
    im.save(jpg, quality=92, optimize=True)
    preview = SELECTED / f"{stem}_preview.jpg"
    subprocess.run([sys.executable, str(PREVIEW_TOOL), "long", str(jpg), "--out", str(preview)], check=True)
    family = SELECTED / ("hos_004_thumbs_v07b_family_vs_live.jpg" if v07b
                         else "hos_004_thumbs_v07_family_vs_live.jpg")
    subprocess.run([sys.executable, str(STYLE_SHEET), "long", str(jpg), "--out", str(family)], check=False)
    log = load_log()
    entry = {"plate": plate.name, "te_face": te, "i_face": i, "out": jpg.name, "at": now()}
    if v07b:
        entry.update(version="v07b", authority="desk #180 6084986948 + 6085214049; job J0106",
                     numbers="52/53 cap ~25% of tile height, Times New Roman Bold, ink + cream outline")
    log["lettered"].append(entry)
    save_log(log)
    print(f"SAVED {jpg}\nPREVIEW {preview}\nFAMILY {family}", flush=True)


def main() -> None:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("paint")
    p.add_argument("--n", type=int, default=2)
    q = sub.add_parser("letter")
    q.add_argument("plate", type=Path)
    q.add_argument("--te", type=int, nargs=4, required=True, metavar=("X0", "Y0", "X1", "Y1"))
    q.add_argument("--i", type=int, nargs=4, required=True, metavar=("X0", "Y0", "X1", "Y1"))
    q.add_argument("--v07b", action="store_true", help="52/53 ~2x, one neutral style -> ..._v07b")
    a = ap.parse_args()
    if a.cmd == "paint":
        paint(a.n)
    else:
        letter(a.plate, tuple(a.te), tuple(a.i), v07b=a.v07b)


if __name__ == "__main__":
    main()
