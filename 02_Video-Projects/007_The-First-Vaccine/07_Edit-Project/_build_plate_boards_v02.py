#!/usr/bin/env python3
"""HOS 007 plate boards v02. Boards only. No mint, no spend.

Applies CLAUDE_BOARDS_REVIEW_v01.md (J0315, a4474f9):
  §1 Flow-first price table in the HOS 009 format; Vertex is fallback only.
  §2 The ten lettering-risk plates become real scans, reframes, reuses or £0 code graphics.
  §3 The cheap notes: Plate I cutaway, body-learns as a code graphic, spines turned away,
     Explorer cover turned away, Jenner face lock, kite hand-off kept.

Reads parts/part-0N_plates_v01.json. Writes v02 beside them, plus PICTURE_PLAN_v02.json
and PRICE_REVIEW_v02.md.
"""

from __future__ import annotations

import json
import math
from copy import deepcopy
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PARTS = ROOT / "parts"

Q_TRY, F_TRY = 100, 10
Q_TAKES, F_TAKES = 2.59, 1.96  # 70/27 and 94/48, same as HOS 009
Q_EXP = math.ceil(Q_TRY * Q_TAKES)  # 259
F_EXP = math.ceil(F_TRY * F_TAKES)  # 20
V_Q, V_F = 0.16, 0.08  # GBP per second, Vertex fallback

# Same reading 009 v04 used. Not re-read. Nothing spent.
FLOW_LEFT = 23740
FLOW_READ_AT = "2026-10-15T21:42:22Z"
VERTEX_PROMO = 71.02
VERTEX_USABLE = 70.02
FLOW_008 = 5605
FLOW_009_T1 = 7354
FLOW_FLOOR = 3000

NO_GLYPH = (
    "No letters, glyphs or numbers anywhere in frame. "
    "Daylight from out of frame; no candle, flame, lantern, lamp or fire in shot. "
    "Silent. Continuous motion through the final frame."
)


def money(n: float) -> float:
    return round(n + 1e-9, 2)


def fmt_t(t: float) -> str:
    m = int(t // 60)
    s = t - 60 * m
    return f"{m}:{s:05.2f}"


def blank_prices() -> dict:
    return {
        "generation_authorized": False,
        "flow_model": None,
        "flow_clip_s": 0,
        "flow_credits_try1": 0,
        "flow_credits_expected": 0,
        "vertex_model": None,
        "vertex_clip_s": 0,
        "vertex_try1_gbp": 0.0,
        "vertex_expected_gbp": 0.0,
        "cost_try1_gbp": 0.0,
        "cost_expected_gbp": 0.0,
    }


def price_mint(plate: dict, quality: str) -> None:
    clip = int(plate["clip_s"])
    plate.update(blank_prices())
    plate["quality"] = quality
    plate["route"] = "flow-first"
    plate["flow_model"] = quality
    plate["flow_clip_s"] = clip
    plate["vertex_model"] = quality
    plate["vertex_clip_s"] = clip
    if quality == "Quality":
        plate["flow_credits_try1"] = Q_TRY
        plate["flow_credits_expected"] = Q_EXP
        plate["vertex_try1_gbp"] = money(clip * V_Q)
        plate["vertex_expected_gbp"] = money(clip * V_Q * Q_TAKES)
    elif quality == "Fast":
        plate["flow_credits_try1"] = F_TRY
        plate["flow_credits_expected"] = F_EXP
        plate["vertex_try1_gbp"] = money(clip * V_F)
        plate["vertex_expected_gbp"] = money(clip * V_F * F_TAKES)
    else:
        raise ValueError(quality)
    plate["cost_try1_gbp"] = plate["vertex_try1_gbp"]
    plate["cost_expected_gbp"] = plate["vertex_expected_gbp"]


def price_free(plate: dict, quality: str, route: str) -> None:
    plate.update(blank_prices())
    plate["quality"] = quality
    plate["route"] = route
    plate["clip_s"] = 0
    plate["prompt"] = None


def as_archive(plate: dict, source: dict, reason: str) -> None:
    price_free(plate, "archive", "archive")
    plate["engine_reason"] = reason
    plate["source"] = source
    plate.pop("prompt", None)


def as_code(plate: dict, spec: dict, reason: str) -> None:
    price_free(plate, "code_graphic", "code-graphic")
    plate["engine_reason"] = reason
    plate["code_graphic_spec"] = spec
    plate.pop("prompt", None)


def as_reuse(plate: dict, parent: str, reason: str) -> None:
    price_free(plate, "reuse", "reuse")
    plate["reuse_of"] = parent
    plate["engine_reason"] = reason
    plate.pop("prompt", None)


def code_spec(file: str, label: str | None, elements: list, animation: str, duration: float) -> dict:
    return {
        "file": file,
        "renderer": "python-pillow-ffmpeg (house explainer renderer, £0)",
        "style": "HOS cream-on-brown period-paper inked diagram, white/sepia Didot italic",
        "layout_mode": "full_frame_period_paper",
        "background_plate": None,
        "label": label,
        "elements": elements,
        "animation": animation,
        "duration_s": duration,
        "lettering": "No place names and no words inside the render. Any label is added in the edit.",
    }


TITLE_PAGE = {
    "work": "Edward Jenner, An Inquiry into the Causes and Effects of the Variolae Vaccinae, 1798, title page",
    "url": "https://wellcomecollection.org/works/megugzv3",
    "catalogue": "Wellcome Collection M0005386",
    "licence": "Public Domain Mark",
    "credit": "Edward Jenner, An Inquiry into the Causes and Effects of the Variolae Vaccinae, 1798, title page. Wellcome Collection M0005386. Public Domain Mark.",
    "treatment": "The real page, not a generated title. A hand turns the physical page so the motion lock holds (no Ken Burns push on a still). Any extra title is an edit overlay.",
}

GILLRAY = {
    "work": "James Gillray, The Cow-Pock — or — the Wonderful Effects of the New Inoculation!, 12 June 1802",
    "url": "https://www.loc.gov/item/94509853/",
    "also": "https://wellcomecollection.org/works/dsu7wxau",
    "catalogue": "Library of Congress 94509853; Wellcome Collection 11752i",
    "licence": "Public domain (published 1802). Library of Congress: no known restrictions. Wellcome: Public Domain Mark.",
    "credit": "James Gillray, The Cow-Pock, 12 June 1802. Library of Congress 94509853. Public domain.",
    "treatment": "The real print, not a pastiche. A hand brings the sheet into frame (object motion), not a Ken Burns push.",
}

PLATE_I = {
    "work": "Plate from Edward Jenner, An Inquiry..., 1798: the hand of Sarah Nelmes",
    "url": "https://wellcomecollection.org/works/scwhgw5a",
    "catalogue": "Wellcome Collection M0009446, illustration from the 1798 Inquiry",
    "licence": "Public Domain Mark",
    "credit": "The hand of Sarah Nelmes, from Jenner, An Inquiry into the Causes and Effects of the Variolae Vaccinae, 1798. Wellcome Collection M0009446. Public Domain Mark.",
    "treatment": "£0 cutaway after the generated study plate. Hand turns the page. Chief flag: the print shows cowpox pustules, and this film's forbidden list rejects sores. Claude asked for the real plate. It costs nothing, so dropping it does not change the mint total.",
}


def apply(part_no: int, plates: list) -> list:
    out = []
    for src in plates:
        p = deepcopy(src)
        p["v01_quality"] = src["quality"]
        p["v01_route"] = src["route"]
        key = (part_no, p["id"])
        if key == (4, "08b_title_page"):
            as_archive(
                p, TITLE_PAGE,
                "J0315 §2: real 1798 Inquiry title page. No generated lettering. £0.",
            )
        elif key == (4, "09_satire"):
            as_archive(
                p, GILLRAY,
                "J0315 §2: real Gillray Cow-Pock print, 1802. No generated etching captions. £0.",
            )
        elif key == (3, "09_casebook_open"):
            as_reuse(
                p, "P2:13_casebook",
                "J0315 §2: near-duplicate of the casebook. Reuse the reframed P2:13 plate. £0.",
            )
        elif key == (4, "01_page_turns"):
            as_reuse(
                p, "P3:05_quill_writes",
                "J0315 §2: near-duplicate of the quill. Reuse the reframed P3:05 plate. The 1 JULY 1796 overlay stays in the edit. £0.",
            )
        elif key == (1, "07_map_shadows"):
            as_code(
                p,
                code_spec(
                    "code_graphic_007_p1_07_map_shadows.mp4",
                    None,
                    [
                        "Inked coastline of Britain and the continent on period paper",
                        "Unmarked towns; grey shadows drift between them",
                    ],
                    "The coastline inks in, then the shadows drift. No place names. The side label THE SPECKLED MONSTER is added in the edit.",
                    p["use_s"],
                ),
                "J0315 §2: parchment map is a £0 code graphic. No invented place names.",
            )
        elif key == (4, "11_news_spreads"):
            as_code(
                p,
                code_spec(
                    "code_graphic_007_p4_11_news_spreads.mp4",
                    None,
                    [
                        "The same inked map",
                        "Small coaches, ships and riders carry tiny books outward from one unmarked city",
                    ],
                    "The map is already there; the riders move outward. No place names. The side label THE NEWS SPREADS is added in the edit.",
                    p["use_s"],
                ),
                "J0315 §2: news map is a £0 code graphic. No invented place names.",
            )
        elif key == (5, "08_body_learns"):
            as_code(
                p,
                code_spec(
                    "code_graphic_007_p5_08_body_learns.mp4",
                    "THE BODY LEARNS",
                    [
                        "Two ink shapes on period paper",
                        "The second shape takes the outline of the first",
                    ],
                    "The first shape inks in; the second meets it and takes its outline. Label fades in over about 0.4 s. No microbes, no gore.",
                    p["use_s"],
                ),
                "J0315 §3: mechanism beat is a £0 code graphic, not a Quality mint.",
            )
        elif key == (2, "12_hunter_letter"):
            p["prompt"] = (
                "Premium Animistry-class 3D cartoon. A folded letter seen edge-on on a desk by a window. "
                "The written face is turned away, so no handwriting is in focus. A hand lifts the folded edge. "
                + NO_GLYPH
            )
            p["engine_reason"] = (
                "J0315 §2: reframed. Page edge-on, no glyph in focus. "
                "Overlay \"Why not try the experiment?\" stays in the edit."
            )
            p["note"] = "Overlay \"Why not try the experiment?\" in the edit. No generated handwriting."
            price_mint(p, "Fast")
        elif key == (2, "13_casebook"):
            p["prompt"] = (
                "Premium Animistry-class 3D cartoon. A leather case-book on Jenner's desk, seen from the side. "
                "The page block is a pale edge. A hand turns a page so the written face never swings into focus. "
                + NO_GLYPH
            )
            p["engine_reason"] = "J0315 §2: the casebook master, reframed. No glyph in focus. Later casebook rows reuse this."
            price_mint(p, "Fast")
        elif key == (3, "05_quill_writes"):
            p["prompt"] = (
                "Premium Animistry-class 3D cartoon. Close on a quill tip and its shadow on the edge of a page. "
                "The page face is out of focus and turned away. No handwriting is visible. "
                + NO_GLYPH
            )
            p["engine_reason"] = (
                "J0315 §2: the quill master, tip and shadow only. "
                "Overlay 14 MAY 1796 stays in the edit."
            )
            p["note"] = "Overlay 14 MAY 1796 in the edit. No generated handwriting."
            price_mint(p, "Fast")
        elif key == (4, "06_line_underlined"):
            p["prompt"] = (
                "Premium Animistry-class 3D cartoon. Close on a quill tip drawing one firm line along a blank page edge. "
                "Shallow focus on the hand and the nib. The page face stays turned away. "
                + NO_GLYPH
            )
            p["engine_reason"] = (
                "J0315 §2: reframed. The line is the action; the words are the edit overlay, not generated glyphs."
            )
            p["note"] = "Overlay NO DISEASE FOLLOWED in the edit. No generated handwriting."
            price_mint(p, "Fast")
        elif key == (5, "10_history_book"):
            p["prompt"] = (
                "Premium Animistry-class 3D cartoon. A hand slides a closed old book onto a shelf. "
                "Every spine faces away from the camera or sits soft and out of focus, so no title is in frame. "
                + NO_GLYPH + " No Explorer."
            )
            p["engine_reason"] = "J0315 §2: spines turned away. Still a Fast mint; the lettering risk is gone."
            price_mint(p, "Fast")
        elif key == (4, "12_explorer_press"):
            p["prompt"] = (
                "Premium Animistry-class 3D cartoon. The Soho hand-press shop, 1798. Exactly ONE Explorer, on model: "
                "a young boy, messy wavy brown hair (full crown), round thin gold glasses, long teal coat, tan waistcoat, "
                "brown bow tie, satchel. He acts, then leaves. He picks up a freshly printed slim book from the stack, "
                "seen from the back and the page block, so the cover faces away and no lettering is in frame. "
                "He sniffs the ink, tucks it under his arm, and leaves. "
                + NO_GLYPH
            )
            p["engine_reason"] = (
                "Quality: the Explorer. J0315 §3: the cover faces away, so the lettering rule holds. "
                "The title is the real 1798 scan on 08b, not this cover."
            )
            price_mint(p, "Quality")
        elif key == (5, "11b_storm_builds"):
            p["engine_reason"] = (
                (p.get("engine_reason") or "Fast.")
                + " J0315 §3: kept. The 008 hand-off stays. No lightning."
            )
            price_mint(p, p["quality"])
        elif key == (5, "12_kite_storm"):
            p["engine_reason"] = (
                "Quality: storm light. J0315 §3: kept as the hand-off to 008. "
                "A faint flash stays in the clouds and never touches the kite."
            )
            p["note"] = "Hand-off to 008. Lightning never touches the kite. Can share an 008 plate."
            price_mint(p, "Quality")
        elif p["quality"] == "reuse" or p["route"] == "reuse":
            parent = p.get("reuse_of")
            as_reuse(
                p, parent,
                p.get("engine_reason") or "Reuse: a window of a KEEP clip, no new mint.",
            )
            if parent in ("P1:07_map_shadows", "P4:11_news_spreads"):
                p["engine_reason"] = f"Reuse of {parent}, which v02 makes a £0 code graphic. Still £0."
            # keep the v01 window notes
            for fld in ("clip_in_s", "reuse_window", "added"):
                if fld in src:
                    p[fld] = src[fld]
        else:
            price_mint(p, p["quality"])
            # Face lock: the first readable Jenner face is the master still.
            prompt = p.get("prompt") or ""
            if "Edward Jenner (readable face" in prompt and p["id"] != "08_jenner_window":
                p["face_lock"] = (
                    "After the first KEEP of P2:08_jenner_window, use that still as the start frame "
                    "so Jenner's face does not drift."
                )
        # The face-lock master itself still has a quill on a page. Turn that page away. Same mint.
        if key == (2, "08_jenner_window"):
            p["prompt"] = (
                "Premium Animistry-class 3D cartoon. Berkeley: a Georgian country house with a garden. "
                "Inside its panelled study, Edward Jenner (readable face, in his late forties, powdered hair tied back, "
                "dark coat, white neckcloth) sits at a desk by the window with a quill. The page is edge-on, "
                "so no handwriting is in focus. This still is the face lock for later Jenner plates. "
                + NO_GLYPH + " No Explorer."
            )
            p["engine_reason"] = (
                "Quality: a named person's readable face is the hero. "
                "J0315 face lock: this is the master still. Page turned edge-on so the quill draws no glyphs."
            )
            p["face_lock"] = "Master still. Later Jenner plates start from the first KEEP of this plate."
        out.append(p)
        if key == (3, "01_sarah_nelmes"):
            cut = deepcopy(p)
            # Split 2.00 s off Sarah's generated plate. The part length does not change.
            p["use_s"] = money(p["use_s"] - 2.0)
            cut["id"] = "01c_nelmes_plate"
            cut["t_s"] = money(p["t_s"] + p["use_s"])
            cut["t"] = fmt_t(cut["t_s"])
            cut["use_s"] = 2.0
            cut["added"] = True
            cut["explorer"] = False
            cut["side_label"] = "SARAH NELMES"
            cut["v01_quality"] = None
            cut["v01_route"] = None
            cut.pop("prompt", None)
            cut.pop("face_lock", None)
            as_archive(
                cut, PLATE_I,
                "J0315 §3: £0 cutaway of the real 1798 Plate (Sarah Nelmes' hand) after the generated study shot.",
            )
            cut["vo_land"] = p.get("vo_land")
            out.append(cut)
    return out


def load_parts() -> list[dict]:
    parts = []
    for n in range(1, 6):
        path = PARTS / f"part-0{n}_plates_v01.json"
        parts.append(json.loads(path.read_text()))
    return parts


def main() -> None:
    parts = load_parts()
    cum_flow = 0
    cum_vertex = 0.0
    per_part = []
    all_rows = []
    for n, part in enumerate(parts, start=1):
        plates = apply(n, part["plates"])
        counts = {
            "rows": 0, "Quality": 0, "Fast": 0, "code_graphic": 0,
            "archive": 0, "reuse": 0, "flow_try1": 0, "flow_expected": 0,
            "vertex_try1": 0.0, "vertex_expected": 0.0,
        }
        for p in plates:
            counts["rows"] += 1
            q = p["quality"]
            counts[q] = counts.get(q, 0) + 1
            cum_flow += p["flow_credits_expected"]
            cum_vertex = money(cum_vertex + p["vertex_expected_gbp"])
            p["cum_flow_credits_expected"] = cum_flow
            p["cum_vertex_expected_gbp"] = cum_vertex
            p["cum_expected_gbp"] = cum_vertex
            p["beyond_floor"] = cum_vertex > VERTEX_USABLE
            counts["flow_try1"] += p["flow_credits_try1"]
            counts["flow_expected"] += p["flow_credits_expected"]
            counts["vertex_try1"] = money(counts["vertex_try1"] + p["vertex_try1_gbp"])
            counts["vertex_expected"] = money(counts["vertex_expected"] + p["vertex_expected_gbp"])
            all_rows.append((n, p))
        part_out = deepcopy(part)
        part_out["status"] = "BOARD_V02"
        part_out["mint"] = False
        part_out["plates"] = plates
        part_out["counts"] = {
            "rows": counts["rows"],
            "mints": counts["Quality"] + counts["Fast"],
            "Quality": counts["Quality"],
            "Fast": counts["Fast"],
            "code_graphic": counts["code_graphic"],
            "archive": counts["archive"],
            "reuse": counts["reuse"],
        }
        part_out["house"] = (
            "STUDIO_PLAYBOOK.md §5. v02 by Cursor, 16 Oct 2026, J0322, from CLAUDE_BOARDS_REVIEW_v01.md. "
            "Flow-first. Vertex is fallback only. generation_authorized is false on every row. No mint."
        )
        (PARTS / f"part-0{n}_plates_v02.json").write_text(json.dumps(part_out, indent=2) + "\n")
        per_part.append({"part": n, **counts})

    film = {
        "rows": sum(x["rows"] for x in per_part),
        "Quality": sum(x["Quality"] for x in per_part),
        "Fast": sum(x["Fast"] for x in per_part),
        "code_graphic": sum(x["code_graphic"] for x in per_part),
        "archive": sum(x["archive"] for x in per_part),
        "reuse": sum(x["reuse"] for x in per_part),
        "mints": 0,
        "flow_try1": sum(x["flow_try1"] for x in per_part),
        "flow_expected": sum(x["flow_expected"] for x in per_part),
        "vertex_try1": money(sum(x["vertex_try1"] for x in per_part)),
        "vertex_expected": money(sum(x["vertex_expected"] for x in per_part)),
    }
    film["mints"] = film["Quality"] + film["Fast"]
    after_007 = FLOW_LEFT - film["flow_expected"]
    after_008 = after_007 - FLOW_008
    after_009 = after_008 - FLOW_009_T1

    plan = {
        "film": "007_The-First-Vaccine",
        "written": "2026-10-16",
        "task": "J0322. Boards v02 from CLAUDE_BOARDS_REVIEW_v01.md. No mint. No spend.",
        "shot_list": "07_Edit-Project/SHOT_LIST_v01.md",
        "readings": {
            "flow_credits_left": FLOW_LEFT,
            "flow_read_at": FLOW_READ_AT,
            "flow_note": "Same reading as HOS 009 PRICE_REVIEW_v04. Not re-read. Nothing spent since that note in this pass.",
            "vertex_promo_gbp": VERTEX_PROMO,
            "vertex_usable_gbp": VERTEX_USABLE,
            "vertex_note": "009 v04 reading, 2026-10-15T07:30:31Z, minus the £1 margin. Vertex is fallback only.",
        },
        "rates": {
            "flow_credits_try1": {"Quality": Q_TRY, "Fast": F_TRY},
            "takes_per_keep": {"Quality": Q_TAKES, "Fast": F_TAKES},
            "flow_credits_expected": {"Quality": Q_EXP, "Fast": F_EXP},
            "vertex_gbp_per_s": {"Quality": V_Q, "Fast": V_F},
            "note": "Same rates as HOS 009. Expected credits are ceil(try-1 × takes per keep).",
        },
        "vo_film_total_s": 512.15,
        "totals": film,
        "per_part": per_part,
        "mint_order": {
            "order": "006 is 0 Flow. Then 007, then 008 (5605), then 009 tranche 1 (7354). Same order as 009 v04.",
            "after_007": after_007,
            "after_007_and_008": after_008,
            "after_007_008_and_009_tranche_1": after_009,
            "floor": FLOW_FLOOR,
            "fits_on_flow": after_009 >= FLOW_FLOOR,
            "vertex_fits": film["vertex_expected"] <= VERTEX_USABLE,
        },
        "status": "BOARD_V02",
        "mint": False,
        "generation_authorized": False,
        "changes": [
            "P4:08b_title_page Fast mint → £0 Wellcome title page (M0005386).",
            "P4:09_satire Fast mint → £0 Gillray Cow-Pock, 1802 (LoC 94509853).",
            "P3:09_casebook_open and P4:01_page_turns cut to reuse (two near-duplicates).",
            "P2:12, P2:13, P3:05, P4:06 reframed: no glyph in focus. Overlays stay in the edit.",
            "P1:07_map_shadows and P4:11_news_spreads → £0 code-graphic maps. No place names.",
            "P5:10_history_book spines turned away. Still Fast.",
            "P5:08_body_learns Quality → £0 code graphic.",
            "P3:01c_nelmes_plate added: £0 Wellcome Plate of Sarah Nelmes, 2.0 s taken from 01_sarah_nelmes.",
            "P4:12_explorer_press cover faces away.",
            "Jenner face lock: P2:08_jenner_window is the master still. Page turned edge-on.",
            "P5 kite hand-off kept. Lightning never touches the kite.",
        ],
    }
    (ROOT / "PICTURE_PLAN_v02.json").write_text(json.dumps(plan, indent=2) + "\n")
    (ROOT / "PRICE_REVIEW_v02.md").write_text(render_review(film, per_part, after_007, after_008, after_009))
    print(json.dumps({"film": film, "after_009_t1": after_009}, indent=2))


def render_review(film: dict, per_part: list, after_007: int, after_008: int, after_009: int) -> str:
    def row(p):
        return (
            f"| Part {p['part']:02d} | {p['rows']} | {p['Quality']} | {p['Fast']} | "
            f"{p['code_graphic']} | {p['archive']} | {p['reuse']} | {p['flow_try1']} | "
            f"{p['flow_expected']} | £{p['vertex_try1']:.2f} | £{p['vertex_expected']:.2f} |"
        )

    lines = "\n".join(row(p) for p in per_part)
    fit = "fits" if after_009 >= FLOW_FLOOR else "does not fit"
    return f"""# 007 price review v02

Cursor, 16 Oct 2026, J0322. Boards only. **No mint. No spend. No merge.**
Applies `CLAUDE_BOARDS_REVIEW_v01.md` (J0315, a4474f9). Parked for the Chief's price pass.

## Readings

- Flow: **{FLOW_LEFT}** credits at {FLOW_READ_AT} (the 009 v04 read). Not re-read. Nothing spent in this pass.
- Vertex promo: **£{VERTEX_PROMO:.2f}**. Usable **£{VERTEX_USABLE:.2f}** after the £1 margin. The route stays Flow-first.

## Rates

Same rates as HOS 009. Expected credits are `ceil(try-1 × takes per keep)`.

| Model | Try-1 | Takes per keep | Expected per row |
|---|---:|---:|---:|
| Quality | {Q_TRY} | {Q_TAKES} (70/27) | {Q_EXP} |
| Fast | {F_TRY} | {F_TAKES} (94/48) | {F_EXP} |

Vertex, if it were the route: Quality £{V_Q:.2f}/s, Fast £{V_F:.2f}/s, clip lengths 4/6/8 s. It does not fit.

## Totals

v01 was 96 rows, 25 Quality / 55 Fast / 16 reuse, priced as Vertex (£58.24 try-1, £139.01 expected).
v02 is Flow-first. Six Fast mints and one Quality mint come off. One £0 archive cutaway is added. The VO timing is unchanged: the cutaway takes 2.0 s from `01_sarah_nelmes`.

| | rows | Quality | Fast | code | archive | reuse | Flow try-1 | Flow expected | Vertex try-1 | Vertex expected |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
{lines}
| **Film** | **{film['rows']}** | **{film['Quality']}** | **{film['Fast']}** | **{film['code_graphic']}** | **{film['archive']}** | **{film['reuse']}** | **{film['flow_try1']}** | **{film['flow_expected']}** | **£{film['vertex_try1']:.2f}** | **£{film['vertex_expected']:.2f}** |

All on Flow: **{film['flow_expected']}** expected against {FLOW_LEFT} left.
All on Vertex: DOES NOT FIT (£{film['vertex_expected']:.2f} expected vs £{VERTEX_USABLE:.2f} usable).

## Mint order

006 needs 0 Flow. Then 007, then 008 ({FLOW_008}), then 009 tranche 1 ({FLOW_009_T1}). Every mint job reads Flow live first and stops if the read after its spend would drop below {FLOW_FLOOR}. No top-up.

| After | Flow left | Against the {FLOW_FLOOR} floor |
|---|---:|---|
| 007 ({film['flow_expected']}) | {after_007} | above |
| 007 + 008 | {after_008} | above |
| 007 + 008 + 009 tranche 1 | {after_009} | {fit} |

## What changed

1. **P4 `08b_title_page`** is the real 1798 title page, Wellcome M0005386, Public Domain Mark. £0. A hand turns the page. No generated title.
2. **P4 `09_satire`** is Gillray's *The Cow-Pock* (12 June 1802), Library of Congress 94509853, public domain. £0. Not a pastiche.
3. **Two near-duplicate handwriting mints are cut.** `P3:09_casebook_open` reuses `P2:13_casebook`. `P4:01_page_turns` reuses `P3:05_quill_writes` (the 1 JULY 1796 overlay stays in the edit).
4. **Four handwriting plates stay Fast, reframed** so no glyph is in focus: `P2:12_hunter_letter` (page edge-on), `P2:13_casebook` (page block edge-on), `P3:05_quill_writes` (nib and shadow), `P4:06_line_underlined` (a line on a blank edge). The spoken overlays stay in the edit.
5. **Both parchment maps are £0 code graphics** (`P1:07_map_shadows`, `P4:11_news_spreads`). No place names in the render. Their old reuse rows stay reuse, still £0.
6. **`P5:10_history_book`** stays Fast. Spines face away.
7. **`P5:08_body_learns`** is a £0 code graphic (THE BODY LEARNS). That is the one Quality mint saved.
8. **`P3:01c_nelmes_plate`** is a £0 cutaway of the real 1798 plate of Sarah Nelmes' hand (Wellcome M0009446), 2.0 s taken from the generated study shot.
9. **`P4:12_explorer_press`** stays Quality. The book is seen from the back. The title lives on the real scan.
10. **Face lock.** `P2:08_jenner_window` is the master still, and its page is edge-on. Later readable Jenner faces start from the first KEEP of that plate.
11. **Kite hand-off kept** (`11b_storm_builds`, `12_kite_storm`). The flash never touches the kite.

`generation_authorized` is false on every row.

## For the Chief

No mint in this pass. Vertex does not fit. Flow {fit} in the order above: after 007, 008 and 009 tranche 1 the reading would show **{after_009}** left.

Two things are not a price question:

- **Plate I shows cowpox pustules.** The film's forbidden list rejects sores. Claude asked for the real plate as a £0 cutaway. Dropping `01c_nelmes_plate` does not change the mint total; the 2.0 s goes back onto `01_sarah_nelmes`.
- **Archive stills and the motion lock.** The lock forbids a Ken Burns push. The boards ask for a hand turning the page instead. If that is not enough, the price pass can waive one slow push on the title page and the Gillray print.

The code graphics (`P1:07`, `P4:11`, `P5:08`) are a `chart` job after this pass. They are not minted.
"""


if __name__ == "__main__":
    main()
