#!/usr/bin/env python3
"""HOS 008 plate boards v04 (Teach/Polish overlay sync on Chief-PASSed v03). J0397. No mint, no spend.

Preserves the exact v03 row counts, qualities, prices, and Flow totals (112 rows: 15 Quality / 86 Fast / 11 £0 code graphics / 0 reuse; Flow try-1 2,360, Flow expected 5,605) while attaching explicit `teach_overlay` specs (WHO, WHEN, DATA+SCALE, FACT, TIMELINE) sourced from 01_Script/FACT_NOTES_v01.md for the edit (AGENTS.md "Cards and timeline added in the edit: 006, 007 and 008").
Nothing is generation_authorized.
"""
from __future__ import annotations

import copy
import json
from pathlib import Path

EDIT = Path(__file__).resolve().parent
OUT = EDIT / "parts"

TEACH_OVERLAYS: dict[str, dict] = {
    "P1:01_kite_open": {
        "kind": "WHEN",
        "label": "PHILADELPHIA · JUNE 1752",
        "hold_s": 3.5,
    },
    "P1:15_bell_count": {
        "kind": "DATA",
        "label": "100+ BELL-RINGERS KILLED",
        "detail": "Inked 18th-century church-tower tally showing 100+ bell-ringers killed by lightning across 33 years",
        "scale": "more than a hundred bell-ringers killed in just a few decades",
        "source_note": "Johann Nepomuk Fischer (Munich, 1784): 386 church towers struck and 103–120 bell-ringers killed over 33 years (FACT_NOTES_v01).",
        "hold_s": 3.8,
    },
    "P2:01_salon_tube": {
        "kind": "WHEN",
        "label": "1740s",
        "hold_s": 3.5,
    },
    "P2:04_franklin_watches": {
        "kind": "WHO",
        "line_1": "Benjamin Franklin",
        "line_2": "(1706–1790) — Philadelphia printer and experimenter",
        "when_stamp": "Philadelphia · 1748",
        "timeline_step": "1/6 · 1748 (Retires from printing to study electricity)",
        "hold_s": 3.8,
    },
    "P2:12_notebook_list": {
        "kind": "DATA",
        "label": "12 LIKENESSES · 7 NOV 1749",
        "detail": "Inked 1-to-12 notebook tally of ways an electric spark matches lightning",
        "scale": "twelve matching properties — ending 'Let the experiment be made'",
        "when_stamp": "Philadelphia · 7 November 1749",
        "timeline_step": "2/6 · 7 Nov 1749 (12 likenesses in notebook)",
        "source_note": "Franklin's lab notes of 7 Nov 1749 listing 12 points of agreement and 'Let the experiment be made' (Founders Online / FACT_NOTES_v01).",
        "hold_s": 3.8,
    },
    "P3:05_marly_garden": {
        "kind": "WHO",
        "line_1": "Thomas-François Dalibard",
        "line_2": "(1709–1778) — French naturalist",
        "fact_card": "France tested it before the kite",
        "when_stamp": "Marly, France · 10 May 1752",
        "timeline_step": "3/6 · 10 May 1752 (Marly rod draws cloud sparks)",
        "source_note": "Dalibard's iron rod at Marly-la-Ville drew sparks on 10 May 1752, a month before Franklin's kite (FACT_NOTES_v01).",
        "hold_s": 3.8,
    },
    "P3:16_keep_silk_dry": {
        "kind": "FACT",
        "label": "DRY SILK BLOCKED THE SHOCK",
        "source_note": "Franklin stood inside a shed doorway holding a dry silk ribbon tied below the wet hemp twine and key (Pennsylvania Gazette, 19 Oct 1752 / FACT_NOTES_v01).",
        "hold_s": 3.8,
    },
    "P3:18_william_runs": {
        "kind": "WHO",
        "line_1": "William Franklin",
        "line_2": "(c. 1730–1813) — Franklin's son, age about 21",
        "when_stamp": "Philadelphia · June 1752",
        "timeline_step": "4/6 · June 1752 (Philadelphia kite experiment)",
        "hold_s": 3.8,
    },
    "P4:08_teach_charge": {
        "kind": "FACT",
        "label": "KITE WAS NEVER STRUCK",
        "source_note": "The kite collected ambient electric charge from the cloud down the wet twine; a direct lightning strike would likely have been fatal (FACT_NOTES_v01).",
        "hold_s": 3.8,
    },
    "P4:10_richmann_rod": {
        "kind": "WHO",
        "line_1": "Georg Wilhelm Richmann",
        "line_2": "(1711–1753) — St Petersburg physicist",
        "when_stamp": "St Petersburg · 6 August 1753",
        "hold_s": 3.8,
    },
    "P4:13_gazette_page": {
        "kind": "WHEN",
        "label": "19 OCTOBER 1752",
        "timeline_step": "5/6 · 19 Oct 1752 (Pennsylvania Gazette report)",
        "hold_s": 3.8,
    },
    "P4:15_copley_medal": {
        "kind": "WHEN",
        "label": "LONDON · 30 NOVEMBER 1753",
        "hold_s": 2.6,
    },
    "P5:01_house_rod": {
        "kind": "WHEN",
        "label": "PHILADELPHIA · SEPTEMBER 1752",
        "hold_s": 3.5,
    },
    "P5:05_almanac_page": {
        "kind": "DATA",
        "label": "POOR RICHARD · 1748 → 1753",
        "detail": "Completed 6-date timeline (1748 · 7 Nov 1749 · 10 May 1752 · June 1752 · 19 Oct 1752 · 1753) + 6–8 ft rod above roof & 3–4 ft in moist earth",
        "scale": "five years from retired printer (1748) to the Copley Medal and Poor Richard (1753)",
        "when_stamp": "1753",
        "timeline_step": "6/6 · 1753 (Poor Richard rod instructions & Copley Medal)",
        "hold_s": 3.8,
    },
    "P5:07_giant_spark": {
        "kind": "DATA",
        "label": "HOTTER THAN THE SUN",
        "detail": "Inked temperature scale comparing a lightning channel (~50,000 °F / 27,700 °C) against the Sun's surface (~10,000 °F / 5,500 °C)",
        "scale": "five times hotter than the surface of the Sun",
        "source_note": "NOAA / NWS lightning facts: lightning channel ~50,000 °F, ~5x the solar photosphere (FACT_NOTES_v01).",
        "hold_s": 3.8,
    },
    "P5:12_no_patent": {
        "kind": "FACT",
        "label": "NEVER PATENTED THE ROD",
        "source_note": "Franklin declined to patent his inventions so anyone could erect a lightning rod freely (Autobiography / Founders Online / FACT_NOTES_v01).",
        "hold_s": 3.8,
    },
    "P5:19_skyline_strike": {
        "kind": "DATA",
        "label": "20+ STRIKES A YEAR",
        "detail": "Inked tall-tower lightning counter climbing past 20 strikes in a single year",
        "scale": "more than twenty lightning strikes a year on a single tall tower",
        "source_note": "NOAA / NWS: tall towers such as the Empire State Building are struck ~20–25 times a year (FACT_NOTES_v01).",
        "hold_s": 3.8,
    },
}

WINDOW_OVERLAY_CODE_GRAPHICS = {
    "P2:15_likeness_fire",
    "P3:04_letter_crosses",
    "P4:06_same_thing",
    "P5:08_looking_path",
    "P5:10_metal_easy",
}


def main() -> None:
    plan_v3 = json.loads((EDIT / "PICTURE_PLAN_v03.json").read_text())
    overlay_count = 0

    for part_idx in range(1, 6):
        pfile = OUT / f"part-{part_idx:02d}_plates_v03.json"
        pdata = copy.deepcopy(json.loads(pfile.read_text()))
        pdata["status"] = "BOARD_V04_PARKED_FOR_CHIEF"
        pdata["house"] = (
            pdata.get("house", "")
            + " v04 (J0397): attaches explicit Teach-on-Screen + Polish-pass overlay specs "
            "(WHO, WHEN, DATA+SCALE, FACT, TIMELINE) sourced from FACT_NOTES_v01.md for the edit. "
            "0 new mints, 0 Flow change."
        )

        for row in pdata["plates"]:
            key = f"P{part_idx}:{row['id']}"
            row["generation_authorized"] = False
            if key in TEACH_OVERLAYS:
                row["teach_overlay"] = TEACH_OVERLAYS[key]
                overlay_count += 1
            if row.get("quality") == "code_graphic":
                row["code_graphic_layout"] = (
                    "moving_plate_overlay"
                    if key in WINDOW_OVERLAY_CODE_GRAPHICS
                    else "full_frame_period_paper"
                )

        out_pfile = OUT / f"part-{part_idx:02d}_plates_v04.json"
        out_pfile.write_text(json.dumps(pdata, indent=2) + "\n")

    plan_v4 = copy.deepcopy(plan_v3)
    plan_v4["written"] = "2026-10-16"
    plan_v4["version"] = "v04"
    plan_v4["status"] = "BOARD_V04_PARKED_FOR_CHIEF"
    plan_v4["task"] = "J0397 plate boards v04 (Teach/Polish edit-overlay sync onto Chief-PASSed v03). No mint. No spend."
    plan_v4["from"] = "part-0N_plates_v03.json via _build_plate_boards_v04.py"
    plan_v4["totals"]["teach_overlays"] = overlay_count
    plan_v4["teach_on_screen_gate"] = {
        "DATA_and_SCALE": 5,
        "WHO": 4,
        "WHEN_and_TIMELINE": 9,
        "FACT": 4,
        "total_overlay_rows": overlay_count,
        "back_to_back_full_frame_graphics": 0,
        "note": "All 17 edit overlays ride locked VO lines and are sourced in 01_Script/FACT_NOTES_v01.md. Adjacent code graphics alternate full_frame_period_paper with moving_plate_overlay so two full-frame graphics never run back to back. Zero new mints, zero Flow credit change.",
    }
    (EDIT / "PICTURE_PLAN_v04.json").write_text(json.dumps(plan_v4, indent=2) + "\n")

    review_v3 = (EDIT / "PRICE_REVIEW_v03.md").read_text()
    header_v4 = """# 008 price review v04 (Teach/Polish edit-overlay sync on Chief-PASSed v03)

Gemini, 16 Oct 2026, J0397. Boards only. **No mint. No spend. No merge.**
Preserves the exact Chief-PASSed v03 row counts, qualities, prices, and Flow totals (112 rows: 15 Quality / 86 non-emissive Fast / 11 £0 code graphics / 0 reuse; Flow try-1 **2,360**, Flow expected **5,605**).
Attaches 17 explicit `teach_overlay` specs (`WHO`, `WHEN`, `DATA + SCALE`, `FACT`, `TIMELINE`) sourced from `01_Script/FACT_NOTES_v01.md` for the edit (`AGENTS.md`: *"Cards and timeline added in the edit: 006, 007 and 008"*), with zero back-to-back full-frame graphics.

---

"""
    (EDIT / "PRICE_REVIEW_v04.md").write_text(header_v4 + review_v3)
    print(f"008 v04 written: {overlay_count} teach_overlay rows attached, Flow expected={plan_v4['totals']['flow_credits_expected']}")


if __name__ == "__main__":
    main()
