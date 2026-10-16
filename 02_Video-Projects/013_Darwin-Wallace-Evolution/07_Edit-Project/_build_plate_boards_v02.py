#!/usr/bin/env python3
"""HOS 013 plate boards v02 (aligned to darwin_script_master_v02.md + FACT_NOTES_v02.md). J0380. No mint, no spend.

Updates v01 pre-VO boards to fold in Chief's five J0307 / J0364 fixes in darwin_script_master_v02.md:
1. Part 03 (1844 order): 230-page essay and 5 July 1844 letter to Emma first
   (06_emma_and_sealed_packet_1844), then Vestiges of Creation ("A few months later...", Oct 1844)
   (07_vestiges_storm_oct_1844).
2. Part 04 (June 1858 order): 18 June arrival + 25 June fairness letter to Lyell
   (09_darwin_reads_smashed_1858), then Charles Waring Darwin's death three days later (28 June)
   (10_quiet_grief_down_house).
3. Part 04 (Wallace's age): updates Wallace from "late twenties" to "in his thirties"
   (35 in June 1858) and removes duplicate Explorer tail sentences in P2:10, P4:08, P6:05.
4. Part 05 (1 July 1858 & 22/24 Nov 1859): updates 05_timeline_and_1250_copies from
   "taken on day one" to "sold out before publication day / every copy ordered before the
   book even went on sale" (Murray's 22 Nov 1859 trade sale before 24 Nov publication).
5. Fixes P1:09 teach_overlay "hold_s" key typo and sets code_graphic_layout on all 8 code graphics.
Nothing is generation_authorized.
"""
from __future__ import annotations

import copy
import json
from pathlib import Path

EDIT = Path(__file__).resolve().parent
OUT = EDIT / "parts"


def fmt_t(sec: float) -> str:
    m = int(sec // 60)
    s = sec - m * 60
    return f"{m}:{s:05.2f}"


def main() -> None:
    plan_v1 = json.loads((EDIT / "PICTURE_PLAN_v01.json").read_text())
    parts_v2 = []

    for p_idx in range(1, 7):
        pdata = copy.deepcopy(json.loads((OUT / f"part-{p_idx:02d}_plates_v01.json").read_text()))
        pdata["version"] = "v02"
        pdata["timing_status"] = "pre_vo_script_clock_v02 (aligned to darwin_script_master_v02.md; retimes onto Scribe STT once VO locks)"

        if p_idx == 1:
            for r in pdata["plates"]:
                if r["id"] == "08_malay_hut_teaser":
                    r["prompt"] = (
                        "Premium Animistry-class 3D cartoon. A bamboo hut in the Malay Archipelago, 1858: "
                        "rain falls outside the open weave while Alfred Russel Wallace, a bearded naturalist in his "
                        "mid-thirties wearing round wire-rimmed spectacles and a linen shirt, seals a thin packet by "
                        "warm lamplight. No readable words or numbers anywhere. Silent. Continuous motion through the "
                        "final frame. No Explorer. No Orbit."
                    )
                if r["id"] == "09_plymouth_harbour_1831" and "teach_overlay" in r:
                    r["teach_overlay"] = {
                        "kind": "WHEN",
                        "label": "PLYMOUTH · 27 DECEMBER 1831",
                        "hold_s": 3.5,
                    }

        elif p_idx == 2:
            for r in pdata["plates"]:
                if r["id"] == "10_explorer_magnifying_beaks":
                    r["prompt"] = (
                        "Premium Animistry-class 3D cartoon. In the museum workroom, the Explorer leans over the "
                        "wooden specimen tray with a brass magnifying glass, comparing a stout nut-cracking finch beak "
                        "with a slender probing beak, then glances up thoughtfully. Exactly one Explorer, on model: "
                        "round gold glasses, teal long coat, finished hair. No readable words or numbers anywhere. "
                        "Silent. Continuous motion through the final frame. No Orbit."
                    )

        elif p_idx == 3:
            # Swap 06_vestiges_storm_1844 and 07_emma_and_sealed_packet per J0307 fix #1 (5 July 1844 essay/Emma first, Oct 1844 Vestiges second)
            r_vest = next(r for r in pdata["plates"] if r["id"] == "06_vestiges_storm_1844")
            r_emma = next(r for r in pdata["plates"] if r["id"] == "07_emma_and_sealed_packet")

            new_06 = copy.deepcopy(r_emma)
            new_06["id"] = "06_emma_and_sealed_packet_1844"
            new_06["t_s"] = 169.5
            new_06["t"] = fmt_t(169.5)
            new_06["use_s"] = 6.0
            new_06["side_label"] = "5 JULY 1844 · EMMA DARWIN"
            new_06["teach_overlay"] = {
                "kind": "WHO",
                "line_1": "Emma Darwin",
                "line_2": "(1808–1896) — Darwin's wife",
                "when_stamp": "Down House · 5 July 1844",
                "timeline_step": "4/7 · July 1844 (230-page essay sealed)",
                "hold_s": 3.8,
            }
            new_06["cum_flow_credits_expected"] = r_vest["cum_flow_credits_expected"]
            new_06["cum_vertex_expected_gbp"] = r_vest["cum_vertex_expected_gbp"]

            new_07 = copy.deepcopy(r_vest)
            new_07["id"] = "07_vestiges_storm_oct_1844"
            new_07["t_s"] = 175.5
            new_07["t"] = fmt_t(175.5)
            new_07["use_s"] = 5.5
            new_07["side_label"] = "OCTOBER 1844 · VESTIGES"
            new_07["teach_overlay"] = {
                "kind": "WHEN",
                "label": "OCTOBER 1844 · CRITICS ATTACK",
                "hold_s": 3.5,
            }
            new_07["prompt"] = (
                "Premium Animistry-class 3D cartoon. A Victorian lecture room in autumn 1844, a few months after "
                "Darwin sealed his sketch: stern gentlemen in dark coats gesture dismissively at an anonymous octavo "
                "book on a table. No readable words or numbers anywhere. Silent. Continuous motion through the final "
                "frame. No Explorer. No Orbit."
            )
            new_07["cum_flow_credits_expected"] = r_emma["cum_flow_credits_expected"]
            new_07["cum_vertex_expected_gbp"] = r_emma["cum_vertex_expected_gbp"]

            pdata["plates"][5] = new_06
            pdata["plates"][6] = new_07

        elif p_idx == 4:
            for r in pdata["plates"]:
                if r["id"] == "01_wallace_poor_collector":
                    r["prompt"] = (
                        "Premium Animistry-class 3D cartoon. 1850s: Alfred Russel Wallace, a self-taught naturalist "
                        "in his thirties, tall, bearded with round wire-rimmed spectacles and a simple linen field "
                        "shirt, packs wooden specimen crates on a dock. No readable words or numbers anywhere. Silent. "
                        "Continuous motion through the final frame. No Explorer. No Orbit."
                    )
                elif r["id"] == "08_explorer_watches_mail":
                    r["prompt"] = (
                        "Premium Animistry-class 3D cartoon. On the sunlit jetty, the Explorer stands beside a stack "
                        "of wooden specimen crates, watching the mail boat pull out toward the open sea. Exactly one "
                        "Explorer, on model: round gold glasses, teal long coat, finished hair. No readable words or "
                        "numbers anywhere. Silent. Continuous motion through the final frame. No Orbit."
                    )
                elif r["id"] == "09_darwin_reads_smashed_1858":
                    r["prompt"] = (
                        "Premium Animistry-class 3D cartoon. Down House study, June 1858: Darwin stands by the window "
                        "lowering Wallace's pages slowly and writing to Charles Lyell that he would rather lose his "
                        "priority than act unfairly. No readable words or numbers anywhere. Silent. Continuous motion "
                        "through the final frame. No Explorer. No Orbit."
                    )
                elif r["id"] == "10_quiet_grief_down_house":
                    r["side_label"] = "28 JUNE 1858"
                    r["prompt"] = (
                        "Premium Animistry-class 3D cartoon. Three days later at Down House, late June 1858: a quiet "
                        "sunlit corridor with a closed white door and a still garden visible through the tall sash "
                        "window. Daylight, window light or matte painted ink only. No candle, flame, glow, spark, "
                        "fireball or lightning. No readable words or numbers anywhere. Silent. Continuous motion "
                        "through the final frame. No Explorer. No Orbit."
                    )

        elif p_idx == 5:
            for r in pdata["plates"]:
                if r["id"] == "02_linnean_listeners_still":
                    r["side_label"] = "WALLACE NOT ASKED"
                elif r["id"] == "05_timeline_and_1250_copies":
                    r["side_label"] = "1,250 COPIES · PRE-SALE"
                    r["teach_overlay"] = {
                        "kind": "DATA",
                        "label": "1,250 COPIES · PRE-SALE",
                        "detail": "1835 → 1889 timeline + first printing of Origin (~1,250 copies) sold out before publication day",
                        "scale": "every copy ordered before the book even went on sale",
                        "hold_s": 3.8,
                    }
                    r["prompt"] = (
                        "Own code graphic: the 7-date inked timeline (1835 · 1837 · 1838 · 1844 · 1858 · 1859 · 1889) "
                        "completes across the top while booksellers' orders take all 1,250 green copies of the first "
                        "printing before publication day."
                    )

        elif p_idx == 6:
            for r in pdata["plates"]:
                if r["id"] == "05_explorer_garden_finch":
                    r["prompt"] = (
                        "Premium Animistry-class 3D cartoon. In the sunlit garden at Down House, the Explorer stands "
                        "quietly by a flowering pea trellis as a songbird lifts off from the hedge into the morning "
                        "sky. Exactly one Explorer, on model: round gold glasses, teal long coat, finished hair. No "
                        "readable words or numbers anywhere. Silent. Continuous motion through the final frame. No Orbit."
                    )

        for r in pdata["plates"]:
            r["generation_authorized"] = False
            if r.get("quality") == "code_graphic":
                r["code_graphic_layout"] = "full_frame_parchment"

        (OUT / f"part-{p_idx:02d}_plates_v02.json").write_text(json.dumps(pdata, indent=2) + "\n")
        parts_v2.append(pdata)

    plan_v2 = copy.deepcopy(plan_v1)
    plan_v2["version"] = "v02"
    plan_v2["written"] = "2026-10-16"
    plan_v2["task"] = "J0380: HOS 013 plate boards v02 (updated for darwin_script_master_v02.md + FACT_NOTES_v02.md + J0304 Gemini quote pass). Flow-first. Mint nothing. Parked for Chief."
    plan_v2["script"] = "01_Script/darwin_script_master_v02.md (92.6 PASS, J0307/J0364 chronology & age fixes applied)"
    plan_v2["facts_pass"] = "01_Script/FACT_NOTES_v02.md + 01_Script/GEMINI_QUOTE_PASS_J0304.md (30 OK, 0 PARTIAL, 0 FLAG)"
    plan_v2["vo_status"] = "Script v02 + FACT_NOTES_v02 complete on main; rows re-time automatically onto Scribe STT once long VO locks."
    plan_v2["v02_updates"] = [
        "Part 03: swapped 1844 order so 06_emma_and_sealed_packet_1844 (5 July 1844 essay + Emma letter) precedes 07_vestiges_storm_oct_1844 (Oct 1844 Vestiges reaction).",
        "Part 04: updated Wallace age to 'in his thirties' (35 in June 1858) and aligned 09_darwin_reads_smashed_1858 (25 June fairness letter) -> 10_quiet_grief_down_house (28 June).",
        "Part 05: updated 05_timeline_and_1250_copies to 'sold out before publication day / every copy ordered before the book even went on sale' (Murray's 22 Nov 1859 trade sale before 24 Nov publication).",
        "Cleaned duplicate Explorer tail strings in P2:10, P4:08, P6:05 and fixed P1:09 hold_s key."
    ]
    (EDIT / "PICTURE_PLAN_v02.json").write_text(json.dumps(plan_v2, indent=2) + "\n")

    # Write SHOT_LIST_v02.md
    lines = [
        "# 013 Darwin–Wallace — Shot list & plate boards v02 (pre-VO, synced to script v02)",
        "",
        "Gemini, 16 Oct 2026, J0380. Built from `01_Script/darwin_script_master_v02.md` (92.6 PASS, J0307/J0364 chronology & age fixes) and `01_Script/FACT_NOTES_v02.md` + `GEMINI_QUOTE_PASS_J0304.md` (30/30 OK).",
        "**No mint, no spend.** Pre-VO clock timings (`343.0 s` base picture grid; re-times automatically onto Scribe word timestamps once long VO locks).",
        "",
    ]
    for pdata in parts_v2:
        lines.append(f"## {pdata['title']}")
        lines.append("")
        lines.append("| Row | Start | Dur (s) | Route / Model | Side label / Teach overlay | Prompt / Source |")
        lines.append("|---|---:|---:|---|---|---|")
        for r in pdata["plates"]:
            rm = r.get("flow_model") or r.get("route")
            lbl = r.get("side_label") or ""
            if "teach_overlay" in r:
                lbl = f"{lbl} (`{r['teach_overlay']['kind']}`)".strip()
            pr = (r.get("prompt") or r.get("reference") or "")[:115] + "…"
            lines.append(f"| `P{pdata['part']}:{r['id']}` | {r['t']} | {r['use_s']:.2f} | {rm} | {lbl} | {pr} |")
        lines.append("")
    (EDIT / "SHOT_LIST_v02.md").write_text("\n".join(lines) + "\n")

    rev_v1 = (EDIT / "PRICE_REVIEW_v01.md").read_text()
    rev_v2 = (
        rev_v1.replace("# 013 price review v01 (pre-VO plate boards)", "# 013 price review v02 (pre-VO plate boards, synced to script v02)")
        .replace("J0365", "J0380")
        .replace("darwin_script_master_v01.md", "darwin_script_master_v02.md")
        .replace("1,250 day-one copies", "1,250 copies ordered at Murray's pre-publication trade sale")
    )
    (EDIT / "PRICE_REVIEW_v02.md").write_text(rev_v2)
    print("013 v02 boards written.")


if __name__ == "__main__":
    main()
