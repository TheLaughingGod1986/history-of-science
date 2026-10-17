#!/usr/bin/env python3
"""HOS 020 (Penicillin: The Mouldy Dish That Saved 200 Million Lives) pre-VO plate boards v01. J0430. No mint, no spend.

Built from 00_Brand/Channel-Setup/ideas/020_Penicillin-Fleming-Florey/penicillin_script_master_v01.md
and SOURCES_v01.md. Nothing is generation_authorized.
"""
from __future__ import annotations

import json
import math
from pathlib import Path

EDIT = Path(__file__).resolve().parent
OUT = EDIT / "parts"
OUT.mkdir(parents=True, exist_ok=True)

FLOW_CREDITS = {"Quality": 100, "Fast": 10}
USD_PER_S = {"Quality": 0.20, "Fast": 0.10}
USD_PER_STILL = 0.039
GBP_PER_USD = 0.80
TAKES_PER_KEEP = {"Quality": round(70 / 27, 2), "Fast": round(94 / 48, 2)}
STILLS_PER_PLATE = round(171 / 75, 2)
VERTEX_LENGTHS = (4, 6, 8)

STYLE = "Premium Animistry-class 3D cartoon. "
FAST_TAIL = (
    " Daylight, window light or matte painted ink only. No candle, flame, glow, "
    "spark, fireball or lightning. No readable words or numbers anywhere. Silent. "
    "Continuous motion through the final frame. No Explorer. No Orbit."
)
QUAL_TAIL = (
    " No readable words or numbers anywhere. Silent. Continuous motion through "
    "the final frame. No Explorer. No Orbit."
)
EXP_TAIL = (
    " Exactly one Explorer, on model: round gold glasses, teal long coat, finished hair. "
    "No readable words or numbers anywhere. Silent. Continuous motion through the final frame. No Orbit."
)


def fmt_t(sec: float) -> str:
    m = int(sec // 60)
    s = sec - m * 60
    return f"{m}:{s:05.2f}"


def price_row(q: str, use_s: float) -> dict:
    if q in ("Quality", "Fast"):
        clip = next(L for L in VERTEX_LENGTHS if L >= use_s - 1e-6)
        try1 = USD_PER_S[q] * clip * GBP_PER_USD
        exp = try1 * TAKES_PER_KEEP[q] + STILLS_PER_PLATE * USD_PER_STILL * GBP_PER_USD
        fexp = math.ceil(FLOW_CREDITS[q] * TAKES_PER_KEEP[q])
        return {
            "route": "flow-first",
            "flow_model": f"Veo 3.1 {q}",
            "flow_clip_s": 8,
            "flow_credits_try1": FLOW_CREDITS[q],
            "flow_credits_expected": fexp,
            "vertex_model": "veo-3.1-generate-001" if q == "Quality" else "veo-3.1-fast-generate-001",
            "vertex_clip_s": clip,
            "vertex_try1_gbp": round(try1, 2),
            "vertex_expected_gbp": round(exp, 2),
        }
    return {
        "route": "code-graphic" if q == "code_graphic" else q,
        "flow_model": None,
        "flow_clip_s": 0,
        "flow_credits_try1": 0,
        "flow_credits_expected": 0,
        "vertex_model": None,
        "vertex_clip_s": 0,
        "vertex_try1_gbp": 0.0,
        "vertex_expected_gbp": 0.0,
    }


PARTS_SPEC = [
    (
        1,
        "Part 01 — The Mould in the Turret Room",
        [
            ("01_turret_room_petri_dish_clear_halo", 0.0, 5.5, "A", False, "THE CLEAR HALO", "Quality",
             "Quality: Short frame 0 / answer image (0:03) + dramatic macro reveal of blue-green Penicillium mould dissolving golden Staphylococcus colonies into a crystal-clear halo.",
             STYLE + "London, 3 September 1928: in a cramped St Mary's Hospital turret laboratory, a gloved hand lifts the glass lid of an unwashed Petri dish; around a fuzzy blue-green circle of Penicillium mould, colonies of golden Staphylococcus bacteria melt into a crystal-clear halo, dissolving into rows of amber penicillin vials." + QUAL_TAIL,
             {"kind": "WHEN", "label": "LONDON · 3 SEPTEMBER 1928", "timeline_step": "1/7 · 3 Sep 1928 (Fleming's St Mary's Petri dish)", "hold_s": 3.5}),
            ("02_fleming_dish_vs_oxford_bedpans_and_melon", 5.5, 6.0, "B", False, "DISH, BEDPAN, MELON", "Quality",
             "Quality: readable faces (Alexander Fleming in London; Norman Heatley and Howard Florey in wartime Oxford).",
             STYLE + "Split period composition: on the left at St Mary's Hospital, Alexander Fleming in a bow tie and white coat peers at a single glass Petri dish; on the right in wartime Oxford, Norman Heatley and Howard Florey tend stacks of rectangular ceramic bedpan vessels beside a golden cantaloupe melon." + QUAL_TAIL,
             None),
            ("03_thorn_scratch_bacteria_and_carbolic_shelf", 11.5, 6.0, "C", False, "ONE SCRATCH COULD KILL", "Fast",
             "Fast: daylight macro view of a rose-thorn scratch on a hand cutting to 3D cartoon red blood cells and dividing cocci bacteria beside a 1930s shelf of bandages and brown bottles. Nothing emissive, no face.",
             STYLE + "In daylight, a tiny rose-thorn scratch on a finger transitions to red blood cells and dividing golden cocci bacteria inside a vessel beside a 1930s wooden apothecary shelf of brown glass bottles and rolled bandages." + FAST_TAIL,
             {"kind": "WHEN", "label": "BEFORE 1941", "hold_s": 3.5}),
            ("04_fleming_broth_vs_peoria_cantaloupe_yield_chart", 17.5, 8.0, "E", False, "2 U/ML VS 2,000+ U/ML (1,000×)", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked comparison shows Fleming's 1928 Penicillium notatum broth (~2 units/mL, needing 2,000 litres to treat 1 patient) against the 1943 Peoria cantaloupe strain Penicillium chrysogenum (2,000+ units/mL in deep fermentation tanks, a 1,000-fold jump).",
             {"kind": "DATA", "label": "2 U/ML (2,000 L) VS 2,000+ U/ML (1,000× JUMP)", "detail": "Inked comparison of Fleming's 1928 mould broth (~2 units/mL, requiring 2,000 litres for 1 human course) vs the 1943 Peoria cantaloupe deep-tank strain (2,000+ units/mL, a 1,000-fold yield jump that produced 2.3 million D-Day doses)", "scale": "2,000 litres of mould broth for a single patient — twenty full bathtubs of liquid just to make a few teaspoons of medicine", "who_card": "Alexander Fleming (1881–1955) — Scottish hospital bacteriologist · Howard Florey (1898–1968) — Oxford pathology professor · Ernst Chain (1906–1979) — Oxford refugee biochemist · Norman Heatley (1911–2004) — Oxford biochemist", "when_stamp": "3 September 1928 · May 1940 · July 1943", "hold_s": 3.8}),
            ("05_st_marys_petri_stacks_and_lysol_tray_pan", 25.5, 5.5, "A", False, "UNWASHED DISHES", "Fast",
             "Fast: daylight pan across stacked glass Petri dishes and a shallow tray of Lysol disinfectant by a sash window between code graphics so two full-frame graphics never run back to back.",
             STYLE + "In soft London window light, the camera tracks across towers of stacked glass Petri dishes beside a shallow enamel tray of green Lysol disinfectant on a wooden laboratory bench." + FAST_TAIL,
             None),
            ("06_one_modern_pill_vs_1940_oxford_output_chart", 31.0, 8.0, "E", False, "20 BATHTUBS IN ONE PILL", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period parchment, an inked scale comparison shows 1 modern 500-milligram penicillin tablet (~800,000 units) outweighing the entire Oxford laboratory broth output of 1940 (~2 million units needed per severe 1941 patient).",
             {"kind": "DATA", "label": "1 PILL (500 MG / 800,000 U) VS 1940 LAB OUTPUT", "detail": "Inked scale comparison showing 1 modern 500 mg penicillin tablet (~800,000 units) vs the ~2 million units needed to treat a single severe infection in 1941", "scale": "one pill in your hand holds more penicillin than an entire Oxford laboratory could brew in months in 1940", "hold_s": 3.8}),
            ("07_table_three_props_dish_bedpan_melon", 39.0, 5.5, "C", False, "PADDINGTON, 1928", "Fast",
             "Fast: daylight prop table (callback source for Part 05: glass Petri dish with blue-green mould, rectangular ceramic Oxford bedpan vessel, golden cantaloupe melon). Nothing emissive.",
             STYLE + "On a wooden laboratory bench in soft window light sit three objects side by side: a glass Petri dish with a blue-green mould colony, a rectangular white ceramic Oxford bedpan vessel, and a golden netted cantaloupe melon." + FAST_TAIL,
             None),
            ("08_explorer_st_marys_halo_magnifier", 62.0, 5.5, "A", True, None, "Quality",
             "Quality: Explorer beat 1 (locked character reference, after 1:00).",
             STYLE + "Standing on the cluttered wooden bench beside the Lysol tray at St Mary's Hospital, the Explorer holds a brass magnifying glass up to the clear ring around the blue-green mould colony, tilts its head in wonder as the bacterial dots vanish inside the boundary, and taps its notebook." + EXP_TAIL,
             None),
            ("09_gloved_hand_pausing_over_lysol_tray", 67.5, 5.5, "B", False, "TOP OF THE STACK", "Fast",
             "Fast: daylight close-up of a hand in a white lab coat sleeve pausing over the top glass Petri dish sitting high and dry above a shallow Lysol disinfectant tray. No face, nothing emissive.",
             STYLE + "In daylight on a wooden bench, a hand in a white coat sleeve pauses just as it lifts the top glass Petri dish from a tall stack rising above a shallow tray of green disinfectant." + FAST_TAIL,
             None),
        ],
    ),
    (
        2,
        'Part 02 — "That\'s Funny" and the Ten-Year Shelf',
        [
            ("01_fleming_and_pryce_turret_room_1928", 85.0, 6.5, "A", False, '"THAT\'S FUNNY"', "Quality",
             "Quality: readable faces (Alexander Fleming and former assistant Merlin Pryce in the St Mary's turret lab on 3 September 1928).",
             STYLE + "London, 3 September 1928: in his tiny turret laboratory at St Mary's Hospital, Alexander Fleming in a bow tie and white lab coat holds up the contaminated Petri dish above a Lysol tray and shows the clear zone around the blue-green mould to his former assistant Merlin Pryce." + QUAL_TAIL,
             {"kind": "WHO", "line_1": "Merlin Pryce", "line_2": "(1902–1976) — St Mary's assistant pathologist", "when_stamp": "August 1928 · London, 3 September 1928", "hold_s": 3.8}),
            ("02_lysozyme_tear_dish_and_1929_golden_broth", 91.5, 6.0, "B", False, "7 MARCH 1929 · PENICILLIN", "Fast",
             "Fast: daylight bench close-up of a 1922 culture dish beside golden Penicillium notatum mould juice filtering through glass funnels into glass flasks. No face, nothing emissive.",
             STYLE + "In soft daylight on a laboratory bench, golden liquid broth from a surface mat of blue-green Penicillium mould filters through a glass funnel into a conical flask beside a glass culture dish." + FAST_TAIL,
             {"kind": "FACT", "label": "Diluted 1 in 800, still lethal", "when_stamp": "1922 · 7 March 1929 · June 1929", "timeline_step": "2/7 · Jun 1929 (Fleming publishes penicillin paper)", "hold_s": 3.8}),
            ("03_dilution_1_in_800_and_wbc_safety_chart", 97.5, 8.0, "E", False, "1 IN 800 DILUTION · WBC SAFE", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked dilution bar chart shows Fleming's 1929 mould broth killing Staphylococcus aureus even when diluted 1 part in 800 while leaving human white blood cells unharmed (vs carbolic acid killing white blood cells), alongside the unstable molecule breaking down by 1931.",
             {"kind": "DATA", "label": "1:800 DILUTION LETHAL TO STAPH · 100% WBC SAFE", "detail": "Inked dilution bar chart showing Fleming's 1929 mould broth killing Staphylococcus aureus at 1:800 dilution while leaving human white blood cells unharmed (vs carbolic acid killing white blood cells faster than bacteria)", "scale": "1 drop of mould broth in 800 drops of water — and it still stopped deadly Staphylococcus cold", "when_stamp": "1931", "hold_s": 3.8}),
            ("04_journal_on_library_shelf_1931_1938", 105.5, 5.5, "C", False, "TEN YEARS ON A SHELF", "Fast",
             "Fast: daylight tracking shot across a quiet Oxford library shelf where the bound 1929 British Journal of Experimental Pathology sits untouched in dust. Nothing emissive.",
             STYLE + "In quiet afternoon window light, a bound scientific journal volume sits on a tall wooden library shelf as dust motes drift through the air." + FAST_TAIL,
             None),
        ],
    ),
    (
        3,
        "Part 03 — The Bedpan Factory and the Eight Mice",
        [
            ("01_florey_chain_heatley_oxford_extraction_1938", 111.0, 6.5, "A", False, "OXFORD, 1938–1940", "Quality",
             "Quality: readable faces (Howard Florey, Ernst Chain, and Norman Heatley at the Sir William Dunn School of Pathology in Oxford).",
             STYLE + "Oxford, 1938–1940: at the Sir William Dunn School of Pathology, Howard Florey in wire-rimmed spectacles and Ernst Chain with a dark moustache examine Fleming's 1929 paper while Norman Heatley in rolled sleeves adjusts a tall chilled glass counter-current extraction rig built from glass pipes and milk churns." + QUAL_TAIL,
             {"kind": "WHEN", "label": "OXFORD · 1938–1940", "hold_s": 3.5}),
            ("02_ceramic_bedpan_vessels_rack_may_1940", 117.5, 6.5, "B", False, "BREWED IN BEDPANS", "Fast",
             "Fast: daylight shot of hundreds of flat rectangular white ceramic vessels modelled on hospital bedpans stacked on Oxford laboratory racks as gloved hands pipette brown liquid. No face, nothing emissive.",
             STYLE + "In daylight inside the Oxford pathology laboratory, hundreds of flat rectangular white ceramic vessels modelled on hospital bedpans line floor-to-ceiling wooden racks while gloved hands harvest tiny pinches of brown penicillin powder." + FAST_TAIL,
             {"kind": "FACT", "label": "Brewed in ceramic bedpans", "when_stamp": "25 May 1940 · 26 May 1940 · 24 August 1940", "timeline_step": "3/7 · 25 May 1940 (Oxford 8-mouse trial)", "hold_s": 3.8}),
            ("03_eight_mice_trial_25_may_1940_chart", 124.0, 8.0, "E", False, "0/4 CONTROLS VS 4/4 TREATED", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked experimental outcome chart of the 25 May 1940 Oxford mouse trial shows 8 white mice injected with 110 million virulent Streptococcus pyogenes bacteria: 4 untreated controls (0 of 4 survived past 17 hours) vs 4 penicillin-treated mice (4 of 4 survived).",
             {"kind": "DATA", "label": "110M STREPTOCOCCUS · 0/4 CONTROLS VS 4/4 TREATED", "detail": "Inked experimental outcome chart of the 25 May 1940 Oxford mouse trial (8 mice injected with 110 million Streptococcus pyogenes: 4 untreated controls 0/4 survived past 17 hours vs 4 penicillin-treated mice 4/4 survived)", "scale": "110 million lethal bacteria injected into a mouse weighing less than an ounce — and every single treated mouse lived", "hold_s": 3.8}),
            ("04_four_healthy_white_mice_in_cage_morning", 132.0, 5.5, "C", False, "SUNDAY MORNING · 4/4 ALIVE", "Fast",
             "Fast: morning daylight close-up of four healthy white laboratory mice scampering actively around wood shavings inside a wire-mesh cage beside an open laboratory notebook. No face, nothing emissive.",
             STYLE + "In crisp Sunday morning window light, four healthy white mice scamper briskly through clean wood shavings inside a laboratory cage beside an open fountain-pen notebook and a tiny brown glass vial." + FAST_TAIL,
             None),
        ],
    ),
    (
        4,
        "Part 04 — The Policeman's Urine and the Mouldy Cantaloupe",
        [
            ("01_radcliffe_infirmary_alexander_and_heatley_bike_1941", 137.5, 6.5, "A", False, "OXFORD · 12 FEBRUARY 1941", "Quality",
             "Quality: readable faces (Dr Charles Fletcher treating policeman Albert Alexander at the Radcliffe Infirmary while Norman Heatley bicycles through Oxford winter snow with glass bottles).",
             STYLE + "Oxford, 12 February 1941: in a Radcliffe Infirmary ward, young physician Charles Fletcher in a white coat prepares a syringe of brown penicillin beside constable Albert Alexander's hospital bed, while outside in the Oxford winter snow Norman Heatley pedals a bicycle carrying glass bottles in a basket back to the pathology lab." + QUAL_TAIL,
             {"kind": "WHO", "line_1": "Albert Alexander & Charles Fletcher", "line_2": "Alexander (1897–1941) · Fletcher (1911–1995)", "fact_card": "Recycled from patient urine", "when_stamp": "Oxford, 12 February 1941 · 15 March 1941", "timeline_step": "4/7 · 12 Feb 1941 (Albert Alexander first human treatment)", "hold_s": 3.8}),
            ("02_peoria_moyer_raper_and_mary_hunt_cantaloupe_1943", 144.0, 6.5, "B", False, "PEORIA · JULY 1943", "Quality",
             "Quality: readable faces (Andrew Moyer, Kenneth Raper, and microbiological aide Mary Hunt holding the golden-mouldy Peoria cantaloupe melon beside deep fermentation tanks).",
             STYLE + "Peoria, Illinois, July 1943: at the USDA fermentation laboratory, Andrew Moyer and Kenneth Raper stand beside deep steel fermentation tanks of corn steep liquor as microbiological aide Mary Hunt holds up a golden-mouldy cantaloupe melon from a Peoria grocery market." + QUAL_TAIL,
             {"kind": "WHO", "line_1": "Andrew Moyer, Kenneth Raper & Mary Hunt", "line_2": "Moyer (1899–1959) · Raper (1908–1987) · Hunt (fl. 1943)", "fact_card": "Mouldy melon gave 1,000x yield", "when_stamp": "Peoria, July 1941 · July 1943 · 6 June 1944", "timeline_step": "5/7 · Jul 1943 (Mary Hunt's Peoria cantaloupe strain)", "hold_s": 3.8}),
            ("03_us_wartime_penicillin_output_1943_1945_chart", 150.5, 8.0, "E", False, "21B → 1,663B → 6,800B UNITS", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked wartime production chart shows US penicillin output rocketing from 21 billion units in 1943 to 1,663 billion units in 1944 (including 2.3 million D-Day doses on 6 June 1944) and 6,800 billion units (6.8 trillion) in 1945.",
             {"kind": "DATA", "label": "21B (1943) → 1,663B (1944) → 6,800B UNITS (1945)", "detail": "Inked wartime production chart showing US penicillin output climbing from 21 billion units (1943) to 1,663 billion units (1944, 2.3M D-Day doses) and 6,800 billion units (1945)", "scale": "from barely enough powder on a fingernail to treat one Oxford policeman in 1941 to 6.8 trillion units a year by 1945 — enough for every Allied soldier on D-Day", "when_stamp": "6 June 1944 · 1945", "timeline_step": "6/7 · 6 Jun 1944 (2.3 million D-Day doses)", "hold_s": 3.8}),
            ("04_explorer_peoria_melon_and_fermenter_salute", 158.5, 5.5, "B", True, None, "Quality",
             "Quality: Explorer beat 2 (locked character reference).",
             STYLE + "Standing beside the Peoria laboratory bench between Fleming's shallow glass Petri dish and the golden cantaloupe melon, the Explorer compares a tiny eyedropper vial against a towering steel fermentation tank and salutes the mouldy melon." + EXP_TAIL,
             None),
        ],
    ),
    (
        5,
        "Part 05 — Why Penicillin Pops Bacteria Like Balloons and Fleming's Warning",
        [
            ("01_timeline_1928_1945_and_20atm_beta_lactam_burst", 164.0, 8.5, "E", False, "20 ATMOSPHERES · BETA-LACTAM RING", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, the 7-date timeline completes: 3 Sep 1928 (St Mary's dish) · Jun 1929 (Penicillin paper) · 25 May 1940 (8-mouse trial) · 12 Feb 1941 (Albert Alexander) · Jul 1943 (Peoria cantaloupe) · 6 Jun 1944 (D-Day doses) · May 1945 (Dorothy Hodgkin X-ray structure), alongside an inked diagram of penicillin's 4-atom beta-lactam ring bursting a 20-atmosphere bacterium.",
             {"kind": "DATA", "label": "20 ATMOSPHERES (3× BIKE TYRE) · 1928 → 1945", "detail": "Animated 7-date timeline (1928 → 1945) alongside an inked beta-lactam cell-wall diagram showing a Staphylococcus bacterium at 20 atmospheres internal pressure bursting when penicillin blocks peptidoglycan cross-linking", "scale": "20 atmospheres of pressure inside a bacterium — three times the pressure of a racing bicycle tyre, popped when penicillin unlocks its cell wall", "who_card": "Dorothy Hodgkin (1910–1994) — Oxford X-ray crystallographer", "when_stamp": "May 1945 · 1928–1945", "timeline_step": "7/7 · May 1945 (Dorothy Hodgkin's X-ray structure)", "hold_s": 3.8}),
            ("02_stockholm_nobel_1945_fleming_florey_chain", 172.5, 6.0, "A", False, "FLEMING'S 1945 WARNING", "Quality",
             "Quality: readable faces (Alexander Fleming, Howard Florey, and Ernst Chain in evening dress in Stockholm on 11 December 1945).",
             STYLE + "Stockholm, 11 December 1945: in a grand ceremonial hall, Alexander Fleming, Howard Florey, and Ernst Chain in formal evening dress hold their Nobel medals and diplomas as Fleming speaks earnestly at the lectern." + QUAL_TAIL,
             {"kind": "WHEN", "label": "11 DECEMBER 1945", "hold_s": 3.5}),
            ("03_faraday_mercury_cup_motor_and_iron_ring_handoff", 178.5, 6.5, "C", False, "THE POWER BEHIND THE LAB", "Fast",
             "Fast: daylight basement workbench shot showing Faraday's 1821 glass cup of silver mercury with a suspended copper wire and upright bar magnet beside his 1831 6-inch iron ring wound in calico-insulated copper wire (handoff to 021 Faraday/Ørsted). Nothing emissive, no face.",
             STYLE + "In soft basement window light on a wooden laboratory table, a copper wire suspended from a cork whirls in circles inside a glass cup of silver liquid mercury around an upright bar magnet beside a six-inch iron ring wrapped in calico-insulated copper wire." + FAST_TAIL,
             None),
            ("04_table_three_callback", 185.0, 2.4, "C", False, None, "reuse",
             "Reuse: verified unused moving window [5.50s..7.90s] of P1:07_table_three_props_dish_bedpan_melon (callback, £0).",
             "Reuse P1:07_table_three_props_dish_bedpan_melon [5.50s..7.90s] (2.40s distinct non-overlapping tail window from 8.00s source clip).",
             None),
        ],
    ),
]


def main() -> None:
    per_part_summary = []
    all_parts = []
    cum_flow = 0
    cum_vx = 0.0
    overlay_count = 0

    for p_idx, p_title, rows_spec in PARTS_SPEC:
        plates = []
        p_counts = {
            "rows": 0,
            "Quality": 0,
            "Fast": 0,
            "code_graphic": 0,
            "reuse": 0,
            "flow_credits_try1": 0,
            "flow_credits_expected": 0,
            "vertex_try1_gbp": 0.0,
            "vertex_expected_gbp": 0.0,
        }
        for (rid, t_s, use_s, fam, exp_flag, lbl, qual, reason, prompt, overlay) in rows_spec:
            priced = price_row(qual, use_s)
            cum_flow += priced["flow_credits_expected"]
            cum_vx = round(cum_vx + priced["vertex_expected_gbp"], 2)

            row = {
                "id": rid,
                "t": fmt_t(t_s),
                "t_s": round(t_s, 2),
                "use_s": round(use_s, 2),
                "family": fam,
                "explorer": exp_flag,
                "character_reference": (
                    "01_Character/02_Explorer-Lock/explorer_ turnaround_sheet.png"
                    if exp_flag
                    else None
                ),
                "side_label": lbl,
                "quality": qual,
                "quality_reason": reason,
                "generation_authorized": False,
                "prompt": prompt if qual in ("Quality", "Fast") else None,
                "reference": prompt if qual not in ("Quality", "Fast") else None,
            }
            if overlay:
                row["teach_overlay"] = overlay
                overlay_count += 1
            if qual == "reuse":
                row["reuse_of"] = "P1:07_table_three_props_dish_bedpan_melon"
                row["reuse_window_s"] = [5.5, 7.9]
                row["reuse_audit"] = {
                    "source_row": "P1:07_table_three_props_dish_bedpan_melon",
                    "source_raw_s": 8.0,
                    "source_usable_s": 7.9,
                    "source_used_s": 5.5,
                    "unused_usable_s": 2.4,
                    "required_use_s": 2.4,
                    "shortfall_usable_s": 0.0,
                    "distinct_window": True,
                    "window_s": [5.5, 7.9],
                    "resolution": "verified_unused_tail_reuse",
                }
            row.update(priced)
            row["cum_flow_credits_expected"] = cum_flow
            row["cum_vertex_expected_gbp"] = cum_vx
            plates.append(row)

            p_counts["rows"] += 1
            p_counts[qual] += 1
            p_counts["flow_credits_try1"] += priced["flow_credits_try1"]
            p_counts["flow_credits_expected"] += priced["flow_credits_expected"]
            p_counts["vertex_try1_gbp"] = round(p_counts["vertex_try1_gbp"] + priced["vertex_try1_gbp"], 2)
            p_counts["vertex_expected_gbp"] = round(p_counts["vertex_expected_gbp"] + priced["vertex_expected_gbp"], 2)

        part_doc = {
            "film": "020_Penicillin-Fleming-Florey",
            "part": p_idx,
            "title": p_title,
            "version": "v01",
            "timing_status": "pre_vo_script_clock (built from penicillin_script_master_v01.md; retimes onto Scribe STT once VO locks)",
            "mint": False,
            "summary": {"part": p_idx, "title": p_title, **p_counts},
            "plates": plates,
        }
        (OUT / f"part-{p_idx:02d}_plates_v01.json").write_text(json.dumps(part_doc, indent=2) + "\n")
        per_part_summary.append({"part": p_idx, "title": p_title, **p_counts})
        all_parts.append(part_doc)

    totals = {
        "rows": sum(p["rows"] for p in per_part_summary),
        "Quality": sum(p["Quality"] for p in per_part_summary),
        "Fast": sum(p["Fast"] for p in per_part_summary),
        "code_graphic": sum(p["code_graphic"] for p in per_part_summary),
        "reuse": sum(p["reuse"] for p in per_part_summary),
        "flow_credits_try1": sum(p["flow_credits_try1"] for p in per_part_summary),
        "flow_credits_expected": sum(p["flow_credits_expected"] for p in per_part_summary),
        "vertex_try1_gbp": round(sum(p["vertex_try1_gbp"] for p in per_part_summary), 2),
        "vertex_expected_gbp": round(sum(p["vertex_expected_gbp"] for p in per_part_summary), 2),
        "explorer": 2,
        "teach_overlays": overlay_count,
    }

    plan = {
        "film": "020_Penicillin-Fleming-Florey",
        "version": "v01",
        "written": "2026-10-17",
        "task": "J0430: HOS 020 pre-VO plate boards v01 (from penicillin_script_master_v01.md + SOURCES_v01.md). Flow-first. Mint nothing. Parked for Chief.",
        "script": "penicillin_script_master_v01.md (93.4 PASS)",
        "facts_pass": "SOURCES_v01.md (8 rows)",
        "vo_status": "Awaiting Chief script sign-off and long VO recording; rows re-time automatically onto Scribe STT once VO locks.",
        "readings": {
            "flow_credits_left": 23740,
            "flow_read_at": "2026-10-15T21:42:22Z",
            "vertex_promo_gbp": 71.02,
            "vertex_usable_gbp": 70.02,
        },
        "totals": totals,
        "per_part": per_part_summary,
        "mint_order": "006 > 007 > 008 > 009 > 010 > 011 > 012 > 013 > 014 > 015 > 016 > 017 > 018 > 019 > 020. Nothing in 020 is generation_authorized.",
    }
    (EDIT / "PICTURE_PLAN_v01.json").write_text(json.dumps(plan, indent=2) + "\n")

    sl = [
        "# 020 Penicillin: The Mouldy Dish That Saved 200 Million Lives — Shot list & plate boards v01 (pre-VO)",
        "",
        "Gemini, 17 Oct 2026, J0430. Built from `penicillin_script_master_v01.md` (93.4 PASS) and `SOURCES_v01.md`.",
        "**No mint, no spend.** Pre-VO clock timings (`187.4 s` base picture grid; re-times automatically onto Scribe word timestamps once long VO locks).",
        "",
    ]
    for pdoc in all_parts:
        sl.append(f"## {pdoc['title']}")
        sl.append("")
        sl.append("| Row | Start | Dur (s) | Route / Model | Side label / Teach overlay | Prompt / Source |")
        sl.append("|---|---:|---:|---|---|---|")
        for r in pdoc["plates"]:
            rm = r.get("flow_model") or r.get("route")
            lbl = r.get("side_label") or ""
            if "teach_overlay" in r:
                lbl = f"{lbl} (`{r['teach_overlay']['kind']}`)".strip()
            pr = (r.get("prompt") or r.get("reference") or "")[:115] + "…"
            sl.append(f"| `P{pdoc['part']}:{r['id']}` | {r['t']} | {r['use_s']:.2f} | {rm} | {lbl} | {pr} |")
        sl.append("")
    (EDIT / "SHOT_LIST_v01.md").write_text("\n".join(sl) + "\n")

    pr_lines = [
        "# 020 price review v01 (pre-VO plate boards)",
        "",
        "Gemini, 17 Oct 2026, J0430. Boards only. **No mint. No spend. No merge.**",
        "Prepared from `penicillin_script_master_v01.md` (93.4 PASS) and `SOURCES_v01.md` so 020's full plate board rows, non-emissive Fast prompts, £0 code graphics, and Teach-on-Screen overlays are ready to re-time the moment long VO locks. Parked for Chief.",
        "",
        "## Totals (base 25-row board before VO continuation splits)",
        "",
        "| Part | Title | Rows | Quality | Fast | £0 code | £0 reuse | Flow try-1 | Flow expected | Vertex try-1 | Vertex expected |",
        "|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for p in per_part_summary:
        pr_lines.append(
            f"| Part 0{p['part']} | {p['title']} | {p['rows']} | {p['Quality']} | {p['Fast']} | {p['code_graphic']} | {p['reuse']} | {p['flow_credits_try1']} | {p['flow_credits_expected']} | £{p['vertex_try1_gbp']:.2f} | £{p['vertex_expected_gbp']:.2f} |"
        )
    pr_lines.append(
        f"| **Film** | | **{totals['rows']}** | **{totals['Quality']}** | **{totals['Fast']}** | **{totals['code_graphic']}** | **{totals['reuse']}** | **{totals['flow_credits_try1']}** | **{totals['flow_credits_expected']}** | **£{totals['vertex_try1_gbp']:.2f}** | **£{totals['vertex_expected_gbp']:.2f}** |"
    )
    pr_lines.extend([
        "",
        "## Route breakdown",
        "",
        f"- **Quality ({totals['Quality']} rows):** readable faces (Alexander Fleming, Merlin Pryce, Howard Florey, Ernst Chain, Norman Heatley, Albert Alexander, Charles Fletcher, Andrew Moyer, Kenneth Raper, Mary Hunt), Short frame 0 / answer image (St Mary's Petri dish halo), and the 2 Explorer beats.",
        f"- **Fast ({totals['Fast']} rows, non-emissive):** daylight prop and laboratory shots (rose-thorn scratch & dividing cocci bacteria, St Mary's stacked Petri dishes & Lysol tray, 3-object callback bench, hand over Lysol stack, 1929 golden mould broth filtration, 1929 journal on library shelf, ceramic bedpan vessels rack, 4 healthy treated white mice in cage, Faraday mercury-cup motor & iron ring handoff). Zero candles, flames, sparks, or glowing elements on Fast.",
        f"- **£0 code graphics ({totals['code_graphic']} rows):**",
        "  1. `P1:04_fleming_broth_vs_peoria_cantaloupe_yield_chart` — Fleming's 1928 mould broth (~2 U/mL, 2,000 L per patient) vs 1943 Peoria cantaloupe deep-tank strain (2,000+ U/mL, 1,000-fold jump) (`SCALE: 2,000 litres of mould broth for a single patient — twenty full bathtubs of liquid just to make a few teaspoons of medicine`)",
        "  2. `P1:06_one_modern_pill_vs_1940_oxford_output_chart` — 1 modern 500 mg penicillin tablet (~800,000 U) vs 1940 Oxford laboratory output (`SCALE: one pill in your hand holds more penicillin than an entire Oxford laboratory could brew in months in 1940`)",
        "  3. `P2:03_dilution_1_in_800_and_wbc_safety_chart` — Fleming's 1929 broth killing Staphylococcus at 1:800 dilution while sparing white blood cells (`SCALE: 1 drop of mould broth in 800 drops of water — and it still stopped deadly Staphylococcus cold`)",
        "  4. `P3:03_eight_mice_trial_25_may_1940_chart` — 25 May 1940 Oxford trial: 8 mice injected with 110M Streptococcus (0/4 controls vs 4/4 treated survived) (`SCALE: 110 million lethal bacteria injected into a mouse weighing less than an ounce — and every single treated mouse lived`)",
        "  5. `P4:03_us_wartime_penicillin_output_1943_1945_chart` — US wartime penicillin production climbing from 21B units (1943) to 1,663B (1944, 2.3M D-Day doses) and 6,800B (1945) (`SCALE: from barely enough powder on a fingernail to treat one Oxford policeman in 1941 to 6.8 trillion units a year by 1945 — enough for every Allied soldier on D-Day`)",
        "  6. `P5:01_timeline_1928_1945_and_20atm_beta_lactam_burst` — completed 7-date timeline (1928 → 1945) + Dorothy Hodgkin's May 1945 beta-lactam ring bursting a 20-atmosphere bacterium (`SCALE: 20 atmospheres of pressure inside a bacterium — three times the pressure of a racing bicycle tyre, popped when penicillin unlocks its cell wall`)",
        f"- **£0 verified reuse ({totals['reuse']} row):** `P5:04_table_three_callback` uses the 2.40 s unused moving tail `[5.50s..7.90s]` of `P1:07_table_three_props_dish_bedpan_melon`.",
        "",
        "## Mint order",
        "",
        "006 > 007 > 008 > 009 > 010 > 011 > 012 > 013 > 014 > 015 > 016 > 017 > 018 > 019 > 020. `generation_authorized` is `false` on every row.",
    ])
    (EDIT / "PRICE_REVIEW_v01.md").write_text("\n".join(pr_lines) + "\n")
    print(f"020 v01 boards written: {totals['rows']} rows, Flow expected={totals['flow_credits_expected']}")


if __name__ == "__main__":
    main()
