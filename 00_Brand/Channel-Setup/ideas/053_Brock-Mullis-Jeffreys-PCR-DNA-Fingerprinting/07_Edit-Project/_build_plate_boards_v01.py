#!/usr/bin/env python3
"""HOS 053 (PCR & DNA Fingerprinting: The Boiling Yellowstone Puddle) pre-VO plate boards v01. J0600. No mint, no spend.

Built from 00_Brand/Channel-Setup/ideas/053_Brock-Mullis-Jeffreys-PCR-DNA-Fingerprinting/pcr_script_master_v01.md
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
        "Part 01 — How a 70 °C Yellowstone Hot Spring Turned One DNA Strand Into a Billion Copies",
        [
            ("01_thomas_brock_19_sep_1966_yellowstone_mushroom_spring_taq_pcr_1b_and_jeffreys_xray", 0.0, 5.5, "A", False, "1 BILLION DNA COPIES", "Quality",
             "Quality: Short frame 0 / answer image (0:03) + beside the steaming turquoise waters of Mushroom Spring in Yellowstone National Park on 19 September 1966, microbiologist Thomas Brock lifts a glass microscope slide covered in pink-orange Thermus aquaticus bacteria at 70 °C, dissolving into a PCR thermal cycler tube where heat-proof Taq polymerase doubles a single DNA strand 30 times into 1,073,741,824 copies alongside Alec Jeffreys's 10 September 1984 DNA fingerprint barcode X-ray.",
             STYLE + "Split period-and-molecular scene: on the left beside a steaming turquoise Yellowstone geothermal spring in 1966, microbiologist Thomas Brock lifts a glass microscope slide covered in pink-orange bacterial mats; on the right, a heat-proof enzyme zips along a DNA double helix multiplying one strand into a towering stack of copies beside a darkroom DNA barcode film." + QUAL_TAIL,
             {"kind": "WHEN", "label": "YELLOWSTONE NATIONAL PARK, 19 SEPTEMBER 1966", "timeline_step": "1/4 · 19 Sep 1966 (Thomas Brock and Hudson Freeze discover Thermus aquaticus in Yellowstone's 70 °C Mushroom Spring; Taq polymerase isolated in 1976)", "hold_s": 3.5}),
            ("02_yellowstone_1966_mushroom_spring_mullis_1983_highway128_and_jeffreys_1984_xray_split", 5.5, 6.0, "B", False, "YELLOWSTONE, PCR, DNA FINGERPRINTING", "Quality",
             "Quality: complex three-part composition (Thomas Brock and Hudson Freeze at Yellowstone's 70 °C Mushroom Spring on 19 September 1966; Kary Mullis driving along California Highway 128 in April 1983 visualising exponential 2^n DNA doubling; and Sir Alec Jeffreys in Leicester at 9:05 a.m. on 10 September 1984 holding up the first DNA fingerprint X-ray film).",
             STYLE + "Three-panel period composition: on the left, two scientists sampling a turquoise Yellowstone hot spring in 1966; in the centre, a 1983 California redwood highway beneath a branching diagram of doubling DNA ladders; on the right, a 1984 British geneticist in a darkroom holding up a striped X-ray autoradiograph." + QUAL_TAIL,
             None),
            ("03_cetus_1985_ecoli_polymerase_boiling_at_95c_vs_1988_yellowstone_taq_surviving_30_cycles", 11.5, 6.0, "C", False, "SURVIVING 95 °C HEAT", "Quality",
             "Quality: readable faces (in a Cetus laboratory in 1983–1988, Randall Saiki and Kary Mullis watch ordinary E. coli DNA polymerase denature at 95 °C after Cycle 1, whereas Yellowstone's Thermus aquaticus Taq polymerase breezes through 95 °C unzipping and 72 °C copying for 30 continuous cycles inside one closed tube).",
             STYLE + "In a 1980s California molecular biology lab, biochemists Randall Saiki and Kary Mullis compare two racks of microcentrifuge tubes in a heated water bath as the Yellowstone enzyme tube stays crystal clear and active through thirty cycles." + QUAL_TAIL,
             {"kind": "WHEN", "label": "1983–1988", "timeline_step": "2/4 · Apr 1983 (Kary Mullis conceives PCR) & 4/4 · 29 Jan 1988 (Saiki, Mullis & colleagues combine Taq polymerase with PCR)", "hold_s": 3.5}),
            ("04_pcr_30_cycle_exponential_2_to_30_1073741824_copies_and_thermal_cycle_chart", 17.5, 8.0, "E", False, "PCR 3-STEP THERMAL CYCLE (95 °C → 54 °C → 72 °C) & 30-CYCLE DOUBLING (2^30 = 1,073,741,824 COPIES)", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked PCR exponential amplification & thermal-cycle graph from Brock & Freeze (1969), Saiki & Mullis (1985/1988 Science), and Jeffreys (1985 Nature) plots 3-step cycling (95 °C unzip, 54 °C anneal, 72 °C Taq copy) multiplying 1 target DNA molecule by 2^30 = 1,073,741,824 copies in 30 cycles while Taq polymerase retains activity at 75–80 °C.",
             {"kind": "DATA", "label": "PCR EXPONENTIAL DOUBLING: 1 DNA STRAND → 1,024 (10 CYCLES) → 1,073,741,824 COPIES (30 CYCLES = 2^30)", "detail": "Inked PCR exponential amplification & thermal-cycle graph on period paper showing 3-step cycling (95 °C unzip, 54 °C anneal, 72 °C Taq copy) multiplying 1 target DNA molecule by 2^30 = 1,073,741,824 copies in 30 cycles while Taq polymerase retains activity at 75–80 °C", "scale": "searching for one gene inside all three billion letters of human DNA without PCR is like hunting for a single needle in a haystack the size of a stadium — whereas thirty cycles of PCR turn that needle into a billion-needle mountain while leaving the hay behind", "who_card": "Thomas D. Brock (1926–2021) — American microbiologist · Hudson Freeze (born 1946) — American biochemist · Alice Chien (born 1952) — Taiwanese-American biochemist · Kary B. Mullis (1944–2019) — American biochemist · Alec J. Jeffreys (born 1950) — British geneticist", "when_stamp": "19 September 1966 · 1976 · April 1983 · 10 September 1984", "hold_s": 3.8}),
            ("05_yellowstone_slide_atcc_vial_micropipette_pcr_tubes_and_dna_helix_model_pan", 25.5, 5.5, "A", False, "70 °C HOT SPRING", "Fast",
             "Fast: daylight macro pan across a glass microscope slide tied with string, a freeze-dried culture vial, a precision micropipette with PCR microcentrifuge tubes, and a brass-and-wood DNA double-helix model on an oak bench between code graphics so two full-frame graphics never run back to back. Nothing emissive, no face.",
             STYLE + "In crisp daylight on an oak laboratory bench, the camera pans smoothly across a glass microscope slide tied with twine, a sealed glass culture vial, a precision micropipette beside tiny PCR tubes, and a brass DNA double-helix model." + FAST_TAIL,
             None),
            ("06_ecoli_polymerase_vs_yellowstone_taq_95c_thermal_survival_chart", 31.0, 8.0, "E", False, "2^30 = 1,073,741,824", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period parchment, an inked enzyme thermal-stability chart compares E. coli DNA polymerase I (0% activity after 1 minute at 95 °C) against Yellowstone Thermus aquaticus Taq polymerase (living at 70–79 °C, optimal DNA synthesis at 75–80 °C, half-life >40 minutes at 95 °C across 30 denaturation cycles).",
             {"kind": "DATA", "label": "E. COLI POLYMERASE (0% AT 95 °C) VS YELLOWSTONE TAQ POLYMERASE (75–80 °C OPTIMUM, SURVIVES 95 °C CYCLING)", "detail": "Inked enzyme thermal-stability chart comparing E. coli DNA polymerase I (0% activity after 1 minute at 95 °C) against Thermus aquaticus Taq polymerase (optimal synthesis at 75–80 °C and surviving 30 cycles of 95 °C DNA denaturation)", "scale": "ninety-five degrees Celsius is five degrees below boiling water — hot enough to cook an egg white solid in seconds, yet Yellowstone's Taq enzyme copies DNA right through the heat without flinching", "hold_s": 3.8}),
            ("07_table_three_props_yellowstone_slide_jar_pcr_thermal_block_and_jeffreys_xray_film", 39.0, 5.5, "C", False, "1966 TO 1988", "Fast",
             "Fast: daylight prop table (callback source for Part 05: Thomas Brock's 1966 Yellowstone glass slide jar, a brushed-aluminium PCR thermal cycler block with micro-tubes, and Alec Jeffreys's 1984 striped DNA autoradiograph plate). Nothing emissive.",
             STYLE + "On an oak workbench in soft window light sit three objects side by side: a glass jar holding microscope slides on twine, a brushed-metal PCR tube block with a micropipette, and a framed black-and-white striped DNA barcode plate." + FAST_TAIL,
             None),
            ("08_explorer_handing_70c_yellowstone_fireproof_helmet_to_taq_builder_at_95c_dna_geyser", 62.0, 5.5, "A", True, None, "Quality",
             "Quality: Explorer beat 1 (locked character reference, after 1:00).",
             STYLE + "Standing beside a steaming geyser basin where an ordinary enzyme model droops in the heat, the Explorer hands a brass heat-shield helmet to a tiny molecular builder, who zips briskly up and down a giant DNA ladder." + EXP_TAIL,
             None),
            ("09_thomas_brock_and_hudson_freeze_19_sep_1966_dipping_glass_slides_in_mushroom_spring", 67.5, 5.5, "B", False, "YELLOWSTONE, 19 SEPTEMBER 1966", "Quality",
             "Quality: readable faces (on 19 September 1966 in Yellowstone National Park, microbiologist Thomas Brock and undergraduate Hudson Freeze dip glass slides tied to strings into the steaming 70 °C outflow channel of Mushroom Spring).",
             STYLE + "Beside the steaming turquoise runoff channel of Mushroom Spring in Yellowstone National Park in 1966, microbiologist Thomas Brock and young researcher Hudson Freeze lower glass microscope slides on twine into the hot water." + QUAL_TAIL,
             {"kind": "WHEN", "label": "YELLOWSTONE, 19 SEPTEMBER 1966", "timeline_step": "1/4 · 19 Sep 1966 (Thomas Brock and Hudson Freeze discover Thermus aquaticus in Yellowstone's 70 °C Mushroom Spring)", "hold_s": 3.5}),
        ],
    ),
    (
        2,
        "Part 02 — 19 September 1966 & 1976: Thomas Brock's Boiling Yellowstone Spring (Thermus aquaticus) & the Heat-Proof Taq Enzyme",
        [
            ("01_brock_freeze_1966_mushroom_spring_yt1_and_alice_chien_1976_cincinnati_taq", 73.0, 6.5, "A", False, "LIVES IN 70 °C WATER", "Quality",
             "Quality: readable faces (Thomas Brock and Hudson Freeze on 19 September 1966 sampling the 70 °C pink-orange mats of Mushroom Spring in Yellowstone and depositing strain YT-1 into the ATCC, dissolving to Alice Chien, David Edgar, and John Trela in 1976 at the University of Cincinnati purifying Taq DNA polymerase).",
             STYLE + "Split period scene: on the left at Yellowstone's Mushroom Spring in 1966, Thomas Brock and Hudson Freeze transfer pink-orange geothermal bacteria into a culture tube; on the right in a 1976 Cincinnati biochemistry lab, Alice Chien purifies heat-stable DNA polymerase in a glass column." + QUAL_TAIL,
             {"kind": "FACT", "label": "Lives in 70 °C water", "when_stamp": "19 September 1966 · August 1969 · 1976", "timeline_step": "1/4 · 19 Sep 1966 & 1976 (Thermus aquaticus YT-1 isolated at 70 °C and Taq polymerase purified)", "hold_s": 3.8}),
            ("02_brock_1969_thermus_aquaticus_70c_growth_and_chien_1976_taq_80c_optimum_chart", 79.5, 8.0, "E", False, "1966/1969 THERMUS AQUATICUS GROWTH (40–79 °C, OPTIMUM 70 °C) & 1976 CHIEN TAQ POLYMERASE PEAK (75–80 °C)", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked Yellowstone geothermal temperature & Taq activity chart from Brock & Freeze (August 1969, J. Bacteriol. 98: 289–297) and Chien, Edgar & Trela (1976, J. Bacteriol. 127: 1550–1557) shows Thermus aquaticus strain YT-1 growing from 40 °C to 79 °C (optimum 70 °C) and purified Taq polymerase reaching peak DNA synthesis at 75–80 °C.",
             {"kind": "DATA", "label": "THERMUS AQUATICUS GROWTH (OPTIMUM 70 °C, MAX 79 °C) & TAQ POLYMERASE SYNTHESIS PEAK (75–80 °C)", "detail": "Inked Yellowstone geothermal temperature & Taq activity chart on period paper from Brock & Freeze (August 1969, J. Bacteriol. 98: 289–297) and Chien, Edgar & Trela (1976, J. Bacteriol. 127: 1550–1557) showing Thermus aquaticus strain YT-1 growing from 40 °C to 79 °C (optimum 70 °C) and purified Taq polymerase reaching peak DNA synthesis at 75–80 °C", "scale": "seventy degrees Celsius is hot enough to scald human skin in one second — yet for Yellowstone's Thermus aquaticus, seventy degrees is a comfortable room temperature", "hold_s": 3.8}),
            ("03_yellowstone_field_notebook_mercury_thermometer_and_atcc_yt1_ampoule_closeup", 87.5, 6.5, "B", False, "19 SEPTEMBER 1966 — STRAIN YT-1", "Fast",
             "Fast: daylight macro shot of Thomas Brock's 1966 field notebook, a brass-cased geothermal thermometer, glass microscope slides, and a sealed glass ATCC culture ampoule on an oak bench. Nothing emissive, no face.",
             STYLE + "In crisp daylight on a wooden field desk, an open 1966 leather field notebook sits beside a brass-cased mercury thermometer, glass microscope slides on string, and a sealed glass culture vial." + FAST_TAIL,
             None),
            ("04_cincinnati_1976_chromatography_column_and_75_80c_water_bath_pan", 94.0, 5.5, "C", False, "1976 — TAQ POLYMERASE", "Fast",
             "Fast: daylight close-up pan across a glass protein-purification column, rack of test tubes, and a stainless-steel water bath on a 1976 biochemistry table. Nothing emissive, no face.",
             STYLE + "In bright window light on a biochemistry bench, a vertical glass chromatography column and rack of glass test tubes sit beside a brushed-steel water bath." + FAST_TAIL,
             None),
        ],
    ),
    (
        3,
        "Part 03 — April 1983 – January 1988: Kary Mullis's Moonlight Drive (PCR) & Swapping in Yellowstone's Taq — Midpoint Twist",
        [
            ("01_kary_mullis_april_1983_highway128_and_randall_saiki_erlich_1988_taq_pcr", 99.5, 6.5, "A", False, "2^30 = 1,073,741,824 COPIES", "Quality",
             "Quality: readable faces (Kary Mullis driving along Highway 128 through the California redwoods in April 1983 conceiving exponential PCR primer doubling, dissolving to Randall Saiki, Henry Erlich, and Mullis at Cetus Corporation in 1985–1988 replacing boiled E. coli enzyme with Yellowstone Taq polymerase).",
             STYLE + "Split period scene: on the left in April 1983, chemist Kary Mullis drives along a tree-lined California mountain road while visualising two DNA primers bracketing a gene; on the right in 1988 at Cetus, Randall Saiki and Henry Erlich load a sealed PCR tube of Taq enzyme into an automated thermal cycler." + QUAL_TAIL,
             {"kind": "WHO", "label": "Randall K. Saiki (born 1955) — American molecular biologist · Henry A. Erlich (born 1943) — American human geneticist", "fact_card": "2^30 = 1,073,741,824 copies", "when_stamp": "April 1983 · 16 December 1983 · 20 December 1985 · 29 January 1988 · 1993", "timeline_step": "2/4 · Apr 1983 (Kary Mullis conceives PCR) & 4/4 · 29 Jan 1988 (Saiki, Mullis & colleagues combine Taq with PCR)", "hold_s": 3.8}),
            ("02_saiki_mullis_1985_manual_klenow_vs_1988_automated_closed_tube_taq_pcr_chart", 106.0, 8.0, "E", False, "1985 MANUAL KLENOW PCR (OPEN TUBE EVERY 95 °C CYCLE) VS 1988 AUTOMATED CLOSED-TUBE YELLOWSTONE TAQ PCR (10^6–10^9×)", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked E. coli Klenow vs Taq PCR automation chart from Saiki et al. & Mullis (20 Dec 1985 Science 230: 1350–1354 & 29 Jan 1988 Science 239: 487–491) shows manual enzyme addition required at every 95 °C cycle with E. coli polymerase vs continuous closed-tube 30-cycle exponential amplification (10^6 to 10^9-fold specificity at 72 °C) with Yellowstone Taq polymerase.",
             {"kind": "DATA", "label": "1985 MANUAL E. COLI PCR (30 ENZYME ADDITIONS) VS 1988 CLOSED-TUBE TAQ PCR (2^30 = 1.07B COPIES)", "detail": "Inked E. coli Klenow vs Taq PCR automation chart on period paper from Saiki et al. & Mullis (20 Dec 1985 Science 230: 1350–1354 & 29 Jan 1988 Science 239: 487–491) showing manual enzyme addition required at every 95 °C cycle with E. coli polymerase vs continuous closed-tube 30-cycle exponential amplification (10^6 to 10^9-fold specificity at 72 °C) with Yellowstone Taq polymerase", "scale": "doubling one molecule thirty times in a row is like folding a sheet of paper thirty times — it grows from a single invisible strand into more than a billion copies inside a droplet smaller than a teardrop", "hold_s": 3.8}),
            ("03_three_water_baths_95c_54c_72c_stopwatch_and_pcr_tubes_closeup", 114.0, 6.5, "B", False, "29 JANUARY 1988 — TAQ PCR", "Fast",
             "Fast: daylight macro shot of three stainless-steel laboratory water baths, a mechanical stopwatch, a micropipette, and a rack of sealed PCR tubes on a Cetus bench. Nothing emissive, no face.",
             STYLE + "In crisp daylight on a molecular biology workbench, three stainless-steel water baths sit side by side with a brass stopwatch, a micropipette, and a rack of closed microcentrifuge tubes." + FAST_TAIL,
             None),
            ("04_dna_double_helix_model_with_two_primer_bookmarks_and_thermal_cycler_pan", 120.5, 5.5, "C", False, "APRIL 1983 — THE PRIMER BRACKET", "Fast",
             "Fast: daylight close-up pan across a brass-and-wood DNA double-helix model showing two coloured primer brackets locked onto opposite strands beside a tabletop thermal cycler block. Nothing emissive, no face.",
             STYLE + "In bright window light on an oak bench, a detailed brass-and-wood model of an unzipped DNA ladder shows two short primer brackets clamped onto opposite strands beside an aluminium thermal block." + FAST_TAIL,
             None),
        ],
    ),
    (
        4,
        "Part 04 — 9:05 a.m., 10 September 1984 & 1986: Alec Jeffreys's 'Eureka!' Darkroom X-Ray (DNA Fingerprinting) & the First Exoneration",
        [
            ("01_alec_jeffreys_10_sep_1984_leicester_darkroom_xray_and_svante_paabo_ancient_dna", 126.0, 6.5, "A", False, "9:05 A.M. DNA BARCODE", "Quality",
             "Quality: readable faces (British geneticist Alec Jeffreys at the University of Leicester at 9:05 a.m. on Monday 10 September 1984 pulling the first DNA fingerprint X-ray film from the developing tank, dissolving to evolutionary geneticist Svante Pääbo amplifying ancient Neanderthal bone DNA with PCR).",
             STYLE + "Split period scene: on the left on 10 September 1984 at the University of Leicester, bearded geneticist Alec Jeffreys holds up a freshly developed X-ray film covered in dark horizontal DNA barcode bands; on the right, evolutionary geneticist Svante Pääbo samples a fossil bone in a cleanroom." + QUAL_TAIL,
             {"kind": "WHO", "label": "Svante Pääbo (born 1955) — Swedish evolutionary geneticist", "fact_card": "9:05 a.m. DNA barcode", "when_stamp": "10 September 1984 · 7 March 1985 · 1986–1987", "timeline_step": "3/4 · 10 Sep 1984 (Alec Jeffreys in Leicester discovers DNA fingerprinting; exonerates Richard Buckland in 1986)", "hold_s": 3.8}),
            ("02_jeffreys_1985_minisatellite_vntr_barcode_inheritance_and_1986_exoneration_chart", 132.5, 8.0, "E", False, "10 SEP 1984 / 1985 JEFFREYS VNTR BARCODE (<1 IN 10^9–10^12 MATCH) & 1986 FIRST DNA EXONERATION (RICHARD BUCKLAND)", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked minisatellite VNTR/STR barcode & random-match probability chart from Jeffreys, Wilson & Thein (7 March 1985, Nature 314: 67–73) shows polymorphic tandem repeat lengths inherited 50% from each parent and reducing random match probability across multiple loci to <1 in 10^9–10^12 (excluding identical twins), paired with the 1986 exoneration of Richard Buckland.",
             {"kind": "DATA", "label": "10 SEP 1984 DNA FINGERPRINT BARCODE (<1 IN 10^9 MATCH ODDS) & 1986 FIRST INNOCENT EXONERATION", "detail": "Inked minisatellite VNTR/STR barcode & random-match probability chart on period paper from Jeffreys, Wilson & Thein (7 March 1985, Nature 314: 67–73) showing polymorphic tandem repeat lengths inherited 50% from each parent and reducing random match probability across multiple loci to <1 in 10^9–10^12 (excluding identical twins), paired with PCR amplification from a single pg of DNA", "scale": "although ninety-nine point nine per cent of your DNA is identical to the person sitting next to you, counting the stutters at just a dozen repeating spots makes your genetic barcode rarer than one in a billion", "hold_s": 3.8}),
            ("03_leicester_1984_autoradiograph_barcode_film_gel_tray_and_magnifying_loupe_closeup", 140.5, 6.5, "B", False, "10 SEPTEMBER 1984 — EUREKA!", "Fast",
             "Fast: daylight macro shot of a developed black-and-white autoradiograph film showing multi-lane DNA barcode bands, a brass magnifying loupe, and an electrophoresis gel tray on a Leicester workbench. Nothing emissive, no face.",
             STYLE + "In crisp daylight on a genetics workbench, a black-and-white striped autoradiograph film rests on a white board beside a brass magnifying glass and an acrylic gel electrophoresis tray." + FAST_TAIL,
             None),
            ("04_explorer_comparing_crime_scene_dna_barcode_to_clear_innocent_suspect_and_match_real_culprit", 147.0, 5.5, "B", True, None, "Quality",
             "Quality: Explorer beat 2 (locked character reference).",
             STYLE + "Standing before three giant sliding wooden barcode frames, the Explorer slides the middle frame aside to show its stripes do not match the evidence frame, unlocking an exoneration gate, then slides the third frame into place where every stripe aligns." + EXP_TAIL,
             None),
        ],
    ),
    (
        5,
        "Part 05 — Why the First DNA Crime Test Freed an Innocent Boy — & How Yogurt Bacteria Gave Us CRISPR Gene Scissors",
        [
            ("01_timeline_1966_1988_and_yellowstone_taq_pcr_to_dna_fingerprinting_chart", 152.5, 8.5, "E", False, "1966–1988 TIMELINE · BROCK 70 °C THERMUS AQUATICUS, MULLIS 2^30 PCR, JEFFREYS DNA BARCODE & SAIKI TAQ AUTOMATION", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, the 4-date timeline completes: 19 Sep 1966 (Thomas Brock and Hudson Freeze discover Thermus aquaticus in Yellowstone's 70 °C Mushroom Spring; Taq polymerase isolated in 1976) · Apr 1983 (Kary Mullis conceives the Polymerase Chain Reaction to double DNA 2^30 = 1.07 billion times) · 10 Sep 1984 (Alec Jeffreys in Leicester discovers DNA fingerprinting; exonerates Richard Buckland in 1986) · 29 Jan 1988 (Saiki, Mullis & colleagues combine Taq polymerase with PCR for automated single-tube amplification).",
             {"kind": "DATA", "label": "1966–1988 DNA TIMELINE · YELLOWSTONE 70 °C TAQ, MULLIS 2^30 PCR & JEFFREYS 1984/1986 DNA EXONERATION", "detail": "Animated 4-date timeline (19 Sep 1966 → 29 Jan 1988) alongside the single-cell PCR amplification and forensic exoneration diagram", "scale": "a single free sample of pink bacteria lifted from a Yellowstone puddle in nineteen sixty-six now powers billions of diagnostic and forensic DNA tests around the globe every year", "when_stamp": "1966–1988", "timeline_step": "4/4 · 1966–1988 timeline complete", "hold_s": 3.8}),
            ("02_yellowstone_slide_pcr_tube_and_dna_barcode_film_on_museum_plinth_pan", 161.0, 5.5, "A", False, "FIRST TEST FREED THE INNOCENT", "Fast",
             "Fast: daylight close-up of a Yellowstone microscope slide jar beside a PCR microcentrifuge tube rack and a framed DNA fingerprint barcode plate on a wooden museum plinth. Nothing emissive, no face.",
             STYLE + "In crisp daylight on a wooden museum plinth, a glass jar with microscope slides sits beside a brushed-metal rack of tiny PCR tubes and a framed DNA barcode film." + FAST_TAIL,
             None),
            ("03_mojica_1993_barrangou_2007_yogurt_phages_and_charpentier_doudna_28_jun_2012_crispr_handoff", 166.5, 6.5, "C", False, "PROGRAMMABLE GENE SCISSORS", "Quality",
             "Quality: readable faces (Spanish microbiologist Francisco Mojica and dairy scientist Rodolphe Barrangou in March 2007 studying yogurt bacteria fighting bacteriophages, alongside Emmanuelle Charpentier and Jennifer Doudna on 28 June 2012 unveiling programmable CRISPR-Cas9 gene scissors — handoff to 054 CRISPR Gene Editing).",
             STYLE + "Split period scene: on the left in 2007, dairy microbiologists inspect bacterial cultures beside a model of viral mugshot repeats; on the right in June 2012, biochemists Emmanuelle Charpentier and Jennifer Doudna guide a molecular Cas9 scissors model to snip a precise letter on a DNA helix." + QUAL_TAIL,
             {"kind": "WHEN", "label": "DECEMBER 1987 · FEBRUARY 2005 · 23 MARCH 2007 · 28 JUNE 2012", "hold_s": 3.5}),
            ("04_table_three_callback", 173.0, 2.4, "C", False, None, "reuse",
             "Reuse: verified unused moving window [5.50s..7.90s] of P1:07_table_three_props_yellowstone_slide_jar_pcr_thermal_block_and_jeffreys_xray_film (callback, £0).",
             "Reuse P1:07_table_three_props_yellowstone_slide_jar_pcr_thermal_block_and_jeffreys_xray_film [5.50s..7.90s] (2.40s distinct non-overlapping tail window from 8.00s source clip).",
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
                row["reuse_of"] = "P1:07_table_three_props_yellowstone_slide_jar_pcr_thermal_block_and_jeffreys_xray_film"
                row["reuse_window_s"] = [5.5, 7.9]
                row["reuse_audit"] = {
                    "source_row": "P1:07_table_three_props_yellowstone_slide_jar_pcr_thermal_block_and_jeffreys_xray_film",
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
            "film": "053_Brock-Mullis-Jeffreys-PCR-DNA-Fingerprinting",
            "part": p_idx,
            "title": p_title,
            "version": "v01",
            "timing_status": "pre_vo_script_clock (built from pcr_script_master_v01.md; retimes onto Scribe STT once VO locks)",
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
        "film": "053_Brock-Mullis-Jeffreys-PCR-DNA-Fingerprinting",
        "version": "v01",
        "date": "2026-10-18",
        "owner": "gemini (J0600)",
        "status": "PRE_VO_BOARDS_V01_NO_MINT",
        "generation_authorized": False,
        "script": "00_Brand/Channel-Setup/ideas/053_Brock-Mullis-Jeffreys-PCR-DNA-Fingerprinting/pcr_script_master_v01.md",
        "sources": "00_Brand/Channel-Setup/ideas/053_Brock-Mullis-Jeffreys-PCR-DNA-Fingerprinting/SOURCES_v01.md",
        "credit_snapshot": {
            "flow_balance": 23740,
            "flow_floor": 0,
            "flow_read_at": "2026-10-15T21:42:22Z",
            "vertex_promo_gbp": 71.02,
            "vertex_usable_gbp": 70.02,
        },
        "totals": totals,
        "per_part": per_part_summary,
        "mint_order": "006 > 007 > 008 > 009 > 010 > 011 > 012 > 013 > 014 > 015 > 016 > 017 > 018 > 019 > 020 > 021 > 022 > 023 > 024 > 025 > 026 > 027 > 028 > 029 > 030 > 031 > 032 > 033 > 034 > 035 > 036 > 037 > 038 > 039 > 040 > 041 > 042 > 043 > 044 > 045 > 046 > 047 > 048 > 049 > 050 > 051 > 052 > 053 > 054 > 055 > 056. Nothing in 053 is generation_authorized.",
    }
    (EDIT / "PICTURE_PLAN_v01.json").write_text(json.dumps(plan, indent=2) + "\n")

    sl = [
        "# 053 PCR & DNA Fingerprinting: The Boiling Yellowstone Puddle — Shot list & plate boards v01 (pre-VO)",
        "",
        "Gemini, 18 Oct 2026, J0600. Built from `pcr_script_master_v01.md` (`91.1 PASS`) and `SOURCES_v01.md`.",
        "**No mint, no spend.** Pre-VO clock timings (`175.4 s` base picture grid; re-times automatically onto Scribe word timestamps once long VO locks).",
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
        "# 053 price review v01 (pre-VO plate boards)",
        "",
        "Gemini, 18 Oct 2026, J0600. Boards only. **No mint. No spend. No merge.**",
        "Prepared from `pcr_script_master_v01.md` (`91.1 PASS`) and `SOURCES_v01.md` so 053's full plate board rows, non-emissive Fast prompts, £0 code graphics, and Teach-on-Screen overlays are ready to re-time the moment long VO locks. Parked for Chief.",
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
        f"- **Quality ({totals['Quality']} rows):** readable faces (Thomas D. Brock, Hudson Freeze, Alice Chien, Kary B. Mullis, Randall K. Saiki, Henry A. Erlich, Alec J. Jeffreys, Svante Pääbo, Francisco Mojica, Rodolphe Barrangou, Emmanuelle Charpentier, Jennifer Doudna), 19 September 1966 Yellowstone 70 °C Mushroom Spring sampling, 1976 Cincinnati Taq purification, April 1983 Highway 128 & 1985–1988 Cetus PCR automation, 10 September 1984 Leicester darkroom DNA fingerprint X-ray, and the 2 Explorer beats.",
        f"- **Fast ({totals['Fast']} rows, non-emissive):** daylight prop and laboratory shots (Yellowstone microscope slide, ATCC vial, micropipette, PCR tubes & DNA helix model pan, 3-object callback bench, Brock's 1966 field notebook & geothermal thermometer, Cincinnati 1976 chromatography column & water bath, 3-temperature PCR water baths & stopwatch, DNA double-helix model with primer brackets, Leicester 1984 autoradiograph film & gel tray, Yellowstone slide & PCR rack on museum plinth). Zero candles, flames, sparks, or glowing elements on Fast.",
        f"- **£0 code graphics ({totals['code_graphic']} rows):**",
        "  1. `P1:04_pcr_30_cycle_exponential_2_to_30_1073741824_copies_and_thermal_cycle_chart` — 3-step PCR thermal cycling (95 °C unzip, 54 °C primer anneal, 72 °C Taq extension) multiplying 1 DNA strand by 2^30 = 1,073,741,824 copies (`SCALE: searching for one gene inside all three billion letters of human DNA without PCR is like hunting for a single needle in a haystack the size of a stadium — whereas thirty cycles of PCR turn that needle into a billion-needle mountain while leaving the hay behind`)",
        "  2. `P1:06_ecoli_polymerase_vs_yellowstone_taq_95c_thermal_survival_chart` — E. coli DNA polymerase I (0% activity after 1 min at 95 °C) vs Yellowstone Thermus aquaticus Taq polymerase (75–80 °C optimum, surviving 30 cycles at 95 °C) (`SCALE: ninety-five degrees Celsius is five degrees below boiling water — hot enough to cook an egg white solid in seconds, yet Yellowstone's Taq enzyme copies DNA right through the heat without flinching`)",
        "  3. `P2:02_brock_1969_thermus_aquaticus_70c_growth_and_chien_1976_taq_80c_optimum_chart` — Brock & Freeze's 1966/1969 Thermus aquaticus strain YT-1 growth curve (40–79 °C, optimum 70 °C) and Chien's 1976 Taq polymerase synthesis peak (75–80 °C) (`SCALE: seventy degrees Celsius is hot enough to scald human skin in one second — yet for Yellowstone's Thermus aquaticus, seventy degrees is a comfortable room temperature`)",
        "  4. `P3:02_saiki_mullis_1985_manual_klenow_vs_1988_automated_closed_tube_taq_pcr_chart` — Saiki & Mullis's 1985 manual E. coli Klenow PCR (opening the tube after every 95 °C cycle) vs 1988 automated closed-tube Yellowstone Taq PCR (`SCALE: doubling one molecule thirty times in a row is like folding a sheet of paper thirty times — it grows from a single invisible strand into more than a billion copies inside a droplet smaller than a teardrop`)",
        "  5. `P4:02_jeffreys_1985_minisatellite_vntr_barcode_inheritance_and_1986_exoneration_chart` — Alec Jeffreys's 10 September 1984 / 1985 minisatellite VNTR/STR barcode (<1 in 10^9–10^12 match odds) and 1986 exoneration of Richard Buckland (`SCALE: although ninety-nine point nine per cent of your DNA is identical to the person sitting next to you, counting the stutters at just a dozen repeating spots makes your genetic barcode rarer than one in a billion`)",
        "  6. `P5:01_timeline_1966_1988_and_yellowstone_taq_pcr_to_dna_fingerprinting_chart` — completed 4-date timeline (19 Sep 1966 → 29 Jan 1988) + single-cell PCR and forensic exoneration diagram (`SCALE: a single free sample of pink bacteria lifted from a Yellowstone puddle in nineteen sixty-six now powers billions of diagnostic and forensic DNA tests around the globe every year`)",
        f"- **£0 verified reuse ({totals['reuse']} row):** `P5:04_table_three_callback` uses the 2.40 s unused moving tail `[5.50s..7.90s]` of `P1:07_table_three_props_yellowstone_slide_jar_pcr_thermal_block_and_jeffreys_xray_film`.",
        "",
        "## Mint order",
        "",
        "006 > 007 > 008 > 009 > 010 > 011 > 012 > 013 > 014 > 015 > 016 > 017 > 018 > 019 > 020 > 021 > 022 > 023 > 024 > 025 > 026 > 027 > 028 > 029 > 030 > 031 > 032 > 033 > 034 > 035 > 036 > 037 > 038 > 039 > 040 > 041 > 042 > 043 > 044 > 045 > 046 > 047 > 048 > 049 > 050 > 051 > 052 > 053 > 054 > 055 > 056. `generation_authorized` is `false` on every row.",
    ])
    (EDIT / "PRICE_REVIEW_v01.md").write_text("\n".join(pr_lines) + "\n")
    print(f"053 v01 boards written: {totals['rows']} rows, Flow expected={totals['flow_credits_expected']}")


if __name__ == "__main__":
    main()
