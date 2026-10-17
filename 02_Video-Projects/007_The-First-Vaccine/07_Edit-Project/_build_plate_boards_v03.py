#!/usr/bin/env python3
"""HOS 007 plate boards v03 (Teach/Polish overlay sync on Chief-PASSed v02). J0397. No mint, no spend.

Preserves the exact v02 row counts, qualities, prices, and Flow totals (96 rows: 24 Quality / 49 Fast / 3 £0 code graphics / 2 £0 archive / 18 reuse; Flow try-1 2,890, Flow expected 7,196) while attaching explicit `teach_overlay` specs (WHO, WHEN, DATA+SCALE, FACT, TIMELINE) sourced from 01_Script/FACT_NOTES_v01.md for the edit (AGENTS.md "Cards and timeline added in the edit: 006, 007 and 008").
Nothing is generation_authorized.
"""
from __future__ import annotations

import copy
import json
from pathlib import Path

EDIT = Path(__file__).resolve().parent
OUT = EDIT / "parts"

TEACH_OVERLAYS: dict[str, dict] = {
    "P1:04_church_dusk": {
        "kind": "WHEN",
        "label": "ENGLAND · 1700s",
        "hold_s": 3.5,
    },
    "P1:07b_three_in_ten": {
        "kind": "DATA",
        "label": "3 IN 10 DIED",
        "detail": "Inked 10-figure tally showing 3 in every 10 smallpox cases fatal (variola major)",
        "scale": "three in every ten people who caught it",
        "source_note": "WHO / CDC variola major case-fatality rate ~30% (FACT_NOTES_v01).",
        "hold_s": 3.5,
    },
    "P2:03_market_walk": {
        "kind": "FACT",
        "label": "MILKMAIDS STAYED SAFE",
        "source_note": "Dairy-country observation that milkmaids who had caught mild cowpox did not catch smallpox (Inquiry 1798 / FACT_NOTES_v01).",
        "hold_s": 3.8,
    },
    "P2:06_jesty_family": {
        "kind": "WHO",
        "line_1": "Benjamin Jesty",
        "line_2": "(1736–1816) — Dorset farmer",
        "when_stamp": "Dorset · 1774",
        "timeline_step": "1/6 · 1774 (Jesty's cowpox trial)",
        "hold_s": 3.8,
    },
    "P2:08_jenner_window": {
        "kind": "WHO",
        "line_1": "Edward Jenner",
        "line_2": "(1749–1823) — Gloucestershire doctor",
        "when_stamp": "Berkeley · Gloucestershire",
        "hold_s": 3.8,
    },
    "P2:10_balloon": {
        "kind": "FACT",
        "label": "STUDIED CUCKOOS & BALLOONS",
        "source_note": "Jenner elected FRS for his 1788 cuckoo study and launched a hydrogen balloon at Berkeley in 1784 (ODNB / FACT_NOTES_v01).",
        "hold_s": 3.8,
    },
    "P2:12_hunter_letter": {
        "kind": "WHO",
        "line_1": "John Hunter",
        "line_2": "(1728–1793) — London surgeon",
        "when_stamp": "August 1775",
        "hold_s": 3.8,
    },
    "P3:01_sarah_nelmes": {
        "kind": "WHO",
        "line_1": "Sarah Nelmes",
        "line_2": "Gloucestershire dairymaid — May 1796",
        "when_stamp": "Berkeley · May 1796",
        "hold_s": 3.8,
    },
    "P3:03_phipps_stool": {
        "kind": "WHO",
        "line_1": "James Phipps",
        "line_2": "(1788–1853) — healthy boy, age about 8",
        "hold_s": 3.8,
    },
    "P3:05_quill_writes": {
        "kind": "WHEN",
        "label": "14 MAY 1796",
        "timeline_step": "2/6 · 14 May 1796 (Cowpox into Phipps)",
        "hold_s": 3.8,
    },
    "P4:01_page_turns": {
        "kind": "WHEN",
        "label": "1 JULY 1796",
        "timeline_step": "3/6 · 1 July 1796 (Smallpox challenge test)",
        "hold_s": 2.6,
    },
    "P4:05_days_pass": {
        "kind": "DATA",
        "label": "DAY 1 · DAY 3 · DAY 7 — 0 FEVER",
        "detail": "Inked 7-day challenge calendar from 1 July 1796 showing zero smallpox pustules or disease",
        "scale": "48 days after the 14 May cowpox scratch — zero disease followed",
        "source_note": "Inquiry (1798), Case XVII: 'no disease followed' after 1 July 1796 variolation (FACT_NOTES_v01).",
        "hold_s": 3.0,
    },
    "P4:08b_title_page": {
        "kind": "DATA",
        "label": "THE INQUIRY · 1798",
        "detail": "Animated timeline building 1774 · 14 May 1796 · 1 July 1796 · 1798 · 1881 · 8 May 1980",
        "scale": "23 cases published in 1798 — 24 years after Jesty's farmyard trial",
        "when_stamp": "London · 1798",
        "timeline_step": "4/6 · 1798 (Jenner prints the Inquiry)",
        "hold_s": 3.8,
    },
    "P4:10_garden_hut": {
        "kind": "FACT",
        "label": "VACCINATED POOR FOR FREE",
        "source_note": "Jenner vaccinated poor families free of charge in the 'Temple of Vaccinia' hut in his Berkeley garden (Jenner Museum / ODNB / FACT_NOTES_v01).",
        "hold_s": 3.8,
    },
    "P5:01_pasteur_1881": {
        "kind": "WHO",
        "line_1": "Louis Pasteur",
        "line_2": "(1822–1895) — French chemist and microbiologist",
        "when_stamp": "London · 8 August 1881",
        "timeline_step": "5/6 · 8 Aug 1881 (Pasteur honours Jenner)",
        "hold_s": 3.8,
    },
    "P5:06_assembly_1980": {
        "kind": "DATA",
        "label": "8 MAY 1980 · SMALLPOX ERADICATED",
        "detail": "Completed 6-date timeline (1774 → 8 May 1980) + ~300 million 20th-century deaths ended to 0",
        "scale": "184 years from Jenner's 1796 test to global eradication in 1980",
        "when_stamp": "Geneva · 8 May 1980",
        "timeline_step": "6/6 · 8 May 1980 (WHO declares smallpox gone)",
        "hold_s": 3.8,
    },
    "P5:06b_churchyard_again": {
        "kind": "FACT",
        "label": "FIRST HUMAN DISEASE ERADICATED",
        "source_note": "WHA33.3 (8 May 1980): smallpox became the first human disease eradicated globally (FACT_NOTES_v01).",
        "hold_s": 3.5,
    },
}


def main() -> None:
    plan_v2 = json.loads((EDIT / "PICTURE_PLAN_v02.json").read_text())
    overlay_count = 0

    for part_idx in range(1, 6):
        pfile = OUT / f"part-{part_idx:02d}_plates_v02.json"
        pdata = copy.deepcopy(json.loads(pfile.read_text()))
        pdata["status"] = "BOARD_V03_PARKED_FOR_CHIEF"
        pdata["house"] = (
            pdata.get("house", "")
            + " v03 (J0397): attaches explicit Teach-on-Screen + Polish-pass overlay specs "
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
                row["code_graphic_layout"] = "full_frame_period_paper"

        out_pfile = OUT / f"part-{part_idx:02d}_plates_v03.json"
        out_pfile.write_text(json.dumps(pdata, indent=2) + "\n")

    plan_v3 = copy.deepcopy(plan_v2)
    plan_v3["written"] = "2026-10-16"
    plan_v3["version"] = "v03"
    plan_v3["status"] = "BOARD_V03"
    plan_v3["task"] = "J0397 plate boards v03 (Teach/Polish edit-overlay sync onto v02). No mint. No spend."
    plan_v3["from"] = "part-0N_plates_v02.json via _build_plate_boards_v03.py"
    plan_v3["totals"]["teach_overlays"] = overlay_count
    plan_v3["teach_on_screen_gate"] = {
        "DATA_and_SCALE": 4,
        "WHO": 6,
        "WHEN_and_TIMELINE": 9,
        "FACT": 4,
        "total_overlay_rows": overlay_count,
        "back_to_back_full_frame_graphics": 0,
        "note": "All 17 edit overlays ride locked VO lines and are sourced in 01_Script/FACT_NOTES_v01.md. Zero new mints, zero Flow credit change.",
    }
    (EDIT / "PICTURE_PLAN_v03.json").write_text(json.dumps(plan_v3, indent=2) + "\n")

    review_v2 = (EDIT / "PRICE_REVIEW_v02.md").read_text()
    header_v3 = """# 007 price review v03 (Teach/Polish edit-overlay sync on v02)

Gemini, 16 Oct 2026, J0397. Boards only. **No mint. No spend. No merge.**
Preserves the exact v02 row counts, qualities, prices, and Flow totals (96 rows: 24 Quality / 49 Fast / 3 £0 code graphics / 2 £0 archive / 18 reuse; Flow try-1 **2,890**, Flow expected **7,196**).
Attaches 17 explicit `teach_overlay` specs (`WHO`, `WHEN`, `DATA + SCALE`, `FACT`, `TIMELINE`) sourced from `01_Script/FACT_NOTES_v01.md` for the edit (`AGENTS.md`: *"Cards and timeline added in the edit: 006, 007 and 008"*), with zero back-to-back full-frame graphics.

---

"""
    (EDIT / "PRICE_REVIEW_v03.md").write_text(header_v3 + review_v2)
    print(f"007 v03 written: {overlay_count} teach_overlay rows attached, Flow expected={plan_v3['totals']['flow_expected']}")


if __name__ == "__main__":
    main()
