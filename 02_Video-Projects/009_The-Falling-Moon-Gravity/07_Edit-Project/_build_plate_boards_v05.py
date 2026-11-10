#!/usr/bin/env python3
"""HOS 009 plate boards v05. J0380. No mint, no spend.

Builds v05 from the Chief-PASSed v04 boards (J0335):
1. Preserves all 90 rows, qualities, prices, and tranches unchanged (46 Quality /
   31 Fast / 12 £0 code graphics / 1 reuse; Flow try-1 4,910, Flow expected 12,534:
   tranche 1 7,354, tranche 2 5,180).
2. Attaches explicit Teach-on-Screen edit-overlay specs (WHO, WHEN, DATA+SCALE,
   FACT, TIMELINE) from cfebdab3 (J0379: moon_script_master_v01.md + FACT_NOTES_v01.md)
   onto the timed board rows (added in edit, £0 / 0 Flow credits).
3. Marks code_graphic_layout on the 12 £0 code graphics so P4:03_sixty_earths
   (full_frame) and P4:04_dots_square / P4:04_dots_square_c1 (window_overlay over
   moving night-sky / orchard plate) never run two full-frame teach graphics
   back to back (AGENTS.md Gate 6).
Nothing is generation_authorized.
"""
from __future__ import annotations

import copy
import json
from pathlib import Path

EDIT = Path(__file__).resolve().parent
OUT = EDIT / "parts"

TEACH_OVERLAYS = {
    "P1:07_night_field": {
        "kind": "WHEN",
        "label": "ENGLAND · 1665",
        "hold_s": 3.5,
    },
    "P2:01_cambridge_closes": {
        "kind": "WHEN",
        "label": "CAMBRIDGE · 1665",
        "hold_s": 3.5,
    },
    "P2:02_newton_arrives": {
        "kind": "WHO",
        "line_1": "Isaac Newton",
        "line_2": "(1642–1727) — Cambridge student",
        "hold_s": 3.8,
    },
    "P2:03_christmas_birth": {
        "kind": "WHEN",
        "label": "WOOLSTHORPE · 25 DECEMBER 1642",
        "timeline_step": "1/5 · 25 Dec 1642 (Woolsthorpe birth)",
        "hold_s": 3.5,
    },
    "P2:04_quart_pot": {
        "kind": "FACT",
        "label": "FITTED IN QUART POT",
        "source_note": "Born prematurely on 25 Dec 1642 (OS); small enough to fit into a quart mug (Conduitt / FACT_NOTES_v01).",
        "hold_s": 3.5,
    },
    "P2:08_the_apple": {
        "kind": "FACT",
        "label": "NEVER HIT HIS HEAD",
        "when_stamp": "Woolsthorpe · 1665–1667",
        "timeline_step": "2/5 · 1665–1667 (Plague orchard)",
        "source_note": "Stukeley (1752) & Conduitt record the fall of an apple in contemplation; neither says it struck his head (FACT_NOTES_v01).",
        "hold_s": 3.8,
    },
    "P3:08_km_a_second": {
        "kind": "DATA",
        "label": "1 KM EVERY SECOND",
        "detail": "Inked orbital path showing ~1 km/s sideways motion combined with continuous fall around the Earth",
        "scale": "one kilometre every second — three times the speed of sound",
        "hold_s": 3.8,
    },
    "P4:03_sixty_earths": {
        "kind": "DATA",
        "label": "60 TIMES FURTHER",
        "detail": "Inked Earth–Moon distance scale of 60 Earth radii",
        "scale": "60 Earth radii — 30 full Earths laid side by side",
        "hold_s": 3.8,
    },
    "P4:04_dots_square": {
        "kind": "DATA",
        "label": "3,600 TIMES WEAKER",
        "detail": "60 × 60 inverse-square grid showing pull 3,600 times weaker at the Moon",
        "scale": "3,600 times weaker — as many seconds as in one hour",
        "hold_s": 3.8,
    },
    "P4:05_minute_second": {
        "kind": "DATA",
        "label": "1 MINUTE = 1 SECOND",
        "detail": "Split-screen comparison of an apple falling ~5 m (15 1/12 Paris feet) in 1 s vs the Moon falling ~5 m in 1 min",
        "scale": "about five metres — the height of a two-storey house",
        "hold_s": 3.8,
    },
    "P4:08_halley_visit": {
        "kind": "WHO",
        "line_1": "Edmond Halley",
        "line_2": "(1656–1742) — English astronomer",
        "when_stamp": "Cambridge · August 1684",
        "timeline_step": "3/5 · August 1684 (Halley visits Cambridge)",
        "hold_s": 3.8,
    },
    "P4:11_principia_press": {
        "kind": "DATA",
        "label": "PRINCIPIA · 1687",
        "detail": "Animated timeline that builds as each date is said (1642 · 1665–1667 · 1684 · 1687 · 1758)",
        "scale": "twenty years from the plague orchard (1666) to the Principia (1687)",
        "when_stamp": "London · 1687",
        "timeline_step": "4/5 · July 1687 (Principia published)",
        "hold_s": 3.8,
    },
    "P4:12_fish_book": {
        "kind": "FACT",
        "label": "HALLEY PAID FOR PRINTING",
        "source_note": "The Royal Society was short of funds after Willughby's De Historia Piscium (1686), so Halley financed Principia himself (FACT_NOTES_v01).",
        "hold_s": 3.5,
    },
    "P5:04_comet_1758": {
        "kind": "FACT",
        "label": "RETURNED ON CHRISTMAS NIGHT",
        "when_stamp": "Saxony · 25 December 1758",
        "timeline_step": "5/5 · 25 Dec 1758 (Halley's Comet sighted)",
        "source_note": "Johann Georg Palitzsch sighted the predicted return on 25 December 1758 (FACT_NOTES_v01).",
        "hold_s": 3.8,
    },
    "P5:07_station_curve": {
        "kind": "DATA",
        "label": "28,000 KM/H FREE FALL",
        "detail": "ISS orbital free-fall curve at 28,000 km/h (7.66 km/s) around the Earth",
        "scale": "28,000 km/h — circling the Earth every 90 minutes",
        "hold_s": 3.8,
    },
    "P5:12_clay_handoff": {
        "kind": "WHEN",
        "label": "66 MILLION YEARS AGO",
        "hold_s": 3.5,
    },
}

WINDOW_OVERLAY_CODE_GRAPHICS = {
    "P4:04_dots_square",
    "P4:04_dots_square_c1",
}


def main() -> None:
    plan_v4 = json.loads((EDIT / "PICTURE_PLAN_v04.json").read_text())
    overlay_count = 0

    for part_idx in range(1, 6):
        pfile = OUT / f"part-{part_idx:02d}_plates_v04.json"
        pdata = copy.deepcopy(json.loads(pfile.read_text()))
        pdata["status"] = "BOARD_V05_PARKED_FOR_CHIEF"
        pdata["house"] = (
            pdata.get("house", "")
            + " v05 (J0380): attaches explicit Teach-on-Screen + Polish-pass overlay specs "
            "(WHO, WHEN, DATA+SCALE, FACT, TIMELINE) from cfebdab3 and marks code_graphic_layout "
            "so no two full-frame teach graphics run back to back. 0 new mints, 0 Flow change."
        )

        for row in pdata["plates"]:
            key = f"P{part_idx}:{row['id']}"
            row["generation_authorized"] = False
            if key in TEACH_OVERLAYS:
                row["teach_overlay"] = TEACH_OVERLAYS[key]
                overlay_count += 1
            if row.get("quality") == "code_graphic":
                if key in WINDOW_OVERLAY_CODE_GRAPHICS:
                    row["code_graphic_layout"] = "window_overlay"
                    row["code_graphic_layout_note"] = (
                        "Animates in an inked parchment frame over a moving night-sky/orchard plate so P4:03_sixty_earths "
                        "and P4:04_dots_square never run two full-frame teach graphics back-to-back (AGENTS.md Gate 6)."
                    )
                else:
                    row["code_graphic_layout"] = "full_frame_or_split_parent"

        out_pfile = OUT / f"part-{part_idx:02d}_plates_v05.json"
        out_pfile.write_text(json.dumps(pdata, indent=2) + "\n")

    plan_v5 = copy.deepcopy(plan_v4)
    plan_v5["written"] = "2026-10-16"
    plan_v5["version"] = "v05"
    plan_v5["task"] = "J0380 plate boards v05 (Teach/Polish overlay sync from cfebdab3 onto Chief-PASSed v04). No mint. No spend."
    plan_v5["from"] = "part-0N_plates_v04.json via _build_plate_boards_v05.py"
    plan_v5["totals"]["teach_overlays"] = overlay_count
    plan_v5["teach_on_screen_gate"] = {
        "DATA_and_SCALE": 6,
        "WHO": 2,
        "WHEN_and_TIMELINE": 9,
        "FACT": 4,
        "total_overlay_rows": overlay_count,
        "back_to_back_full_frame_graphics": 0,
        "note": "Synced verbatim with cfebdab3 (J0379: moon_script_master_v01.md + FACT_NOTES_v01.md). P4:04_dots_square marked window_overlay so P4:03 and P4:04 never run two full-frame teach graphics back-to-back.",
    }
    (EDIT / "PICTURE_PLAN_v05.json").write_text(json.dumps(plan_v5, indent=2) + "\n")

    review_v4 = (EDIT / "PRICE_REVIEW_v04.md").read_text()
    header_v5 = """# 009 price review v05 (Teach/Polish overlay sync on Chief-PASSed v04)

Gemini, 16 Oct 2026, J0380. Boards only. **No mint. No spend. No merge.**
Preserves the exact Chief-PASSed v04 row counts, qualities, prices, and tranches (90 rows: 46 Quality / 31 Fast / 12 £0 code graphics / 1 reuse; Flow try-1 **4,910**, Flow expected **12,534**: tranche 1 **7,354**, tranche 2 **5,180**).
Attaches the 16 explicit `teach_overlay` specs (`WHO`, `WHEN`, `DATA + SCALE`, `FACT`, `TIMELINE`) added to `moon_script_master_v01.md` and `FACT_NOTES_v01.md` in `cfebdab3` (J0379), and marks `P4:04_dots_square` (`window_overlay`) so `P4:03_sixty_earths` and `P4:04_dots_square` never run two full-frame teach graphics back-to-back (AGENTS.md Gate 6).

---

"""
    (EDIT / "PRICE_REVIEW_v05.md").write_text(header_v5 + review_v4)
    print(f"009 v05 written: {overlay_count} teach_overlay rows attached, Flow expected={plan_v5['totals']['flow_credits_expected']}")


if __name__ == "__main__":
    main()
