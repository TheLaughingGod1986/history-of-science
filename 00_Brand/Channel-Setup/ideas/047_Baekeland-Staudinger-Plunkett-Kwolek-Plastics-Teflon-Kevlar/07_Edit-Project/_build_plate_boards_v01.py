#!/usr/bin/env python3
"""HOS 047 (Teflon & Kevlar: The Lab Accidents Stronger Than Steel) pre-VO plate boards v01. J0555/J0570. No mint, no spend.

Built from 00_Brand/Channel-Setup/ideas/047_Baekeland-Staudinger-Plunkett-Kwolek-Plastics-Teflon-Kevlar/plastics_script_master_v01.md (91.0 PASS)
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
        "Part 01 — The 'Empty' Gas Cylinder That Still Weighed Full Weight and the Cloudy Beaker Stronger Than Steel",
        [
            ("01_plunkett_6_apr_1938_sawed_teflon_cylinder_and_kwolek_1965_cloudy_kevlar_spinneret", 0.0, 5.5, "A", False, "SLIPPERIEST AND STRONGEST", "Quality",
             "Quality: Short frame 0 / answer image (0:03) + in Deepwater, New Jersey, on the morning of 6 April 1938, 27-year-old chemist Roy Plunkett and assistant Jack Rebok saw open a frozen steel gas cylinder to reveal a coating of waxy white Teflon powder, while in Wilmington, Delaware, in 1965, 41-year-old chemist Stephanie Kwolek pours a cloudy, opalescent liquid into a spinneret to draw a golden Kevlar fibre five times stronger than steel.",
             STYLE + "Split period laboratory scene: on the left in 1938 New Jersey, twenty-seven-year-old chemist Roy Plunkett and Jack Rebok saw open a frosted steel gas cylinder lined inside with waxy white Teflon powder; on the right in 1965 Delaware, forty-one-year-old chemist Stephanie Kwolek pours a cloudy buttermilk-like liquid into a spinneret drawing a golden Kevlar thread." + QUAL_TAIL,
             {"kind": "WHEN", "label": "DEEPWATER, NEW JERSEY, 6 APRIL 1938 · WILMINGTON, 1965", "timeline_step": "3/5 · 6 Apr 1938 (Roy Plunkett and Jack Rebok saw open an 'empty' frozen TFE gas cylinder at DuPont to discover PTFE / Teflon) & 5/5 · 1965 (Stephanie Kwolek spins a cloudy liquid-crystalline aramid solution into bulletproof Kevlar)", "hold_s": 3.5}),
            ("02_baekeland_1907_bakelizer_staudinger_1920_chain_plunkett_1938_teflon_kwolek_1965_kevlar_split", 5.5, 6.0, "B", False, "CHAINS, TEFLON, KEVLAR", "Quality",
             "Quality: complex three-part split composition (Leo Baekeland's July 1907 cast-iron 'Bakelizer' pressure vessel and Hermann Staudinger's 1920 macromolecule polymer chain on the left; Roy Plunkett's sawed-open 6 April 1938 tetrafluoroethylene cylinder lined with white PTFE in the centre; Stephanie Kwolek's 1965 aligned liquid-crystalline Kevlar rods stopping a lead bullet on the right).",
             STYLE + "Three-panel period composition: on the left, a heavy cast-iron pressure vessel beside a long ball-and-stick polymer chain; in the centre, a sawed-open steel cylinder coated inside with white PTFE powder; on the right, a woven golden Kevlar vest catching a flattened lead bullet." + QUAL_TAIL,
             None),
            ("03_plunkett_and_rebok_6_apr_1938_poking_wire_into_silent_valve_on_scale", 11.5, 6.0, "C", False, "6 APRIL 1938", "Quality",
             "Quality: readable faces (on 6 April 1938 in Deepwater, New Jersey, Roy Plunkett and Jack Rebok poke a wire through the open valve of a frozen steel gas cylinder on a balance scale and hear nothing hiss out).",
             STYLE + "In a 1938 DuPont laboratory in New Jersey, young chemist Roy Plunkett and technician Jack Rebok lean over a frosted steel gas cylinder sitting on a heavy brass balance scale as Rebok pokes a thin wire through the open top valve." + QUAL_TAIL,
             {"kind": "WHEN", "label": "6 APRIL 1938", "timeline_step": "3/5 · 6 Apr 1938 (Roy Plunkett and Jack Rebok discover frozen TFE gas polymerized into solid PTFE / Teflon inside the cylinder)", "hold_s": 3.5}),
            ("04_steel_vs_kevlar_5x_strength_3_6gpa_and_teflon_0_04_wet_ice_friction_chart", 17.5, 8.0, "E", False, "KEVLAR (3.6 GPA AT 1.44 G/CM³ = 5× STEEL BY WEIGHT) & TEFLON (0.04 FRICTION = WET ICE ON WET ICE)", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked tensile-strength and friction comparison chart contrasts structural steel (tensile strength ~0.5–0.8 GPa, density 7.8 g/cm³) against Stephanie Kwolek's 1965 Kevlar aramid fibre (tensile strength ~3.6 GPa, density 1.44 g/cm³ = 5× stronger than steel on an equal-weight basis) and Roy Plunkett's 1938 PTFE / Teflon (coefficient of friction ~0.04, matching wet ice on wet ice, stable up to 260 °C).",
             {"kind": "DATA", "label": "KEVLAR (3.6 GPA AT 1.44 G/CM³ = 5× STEEL BY WEIGHT) · TEFLON (0.04 FRICTION = WET ICE ON WET ICE)", "detail": "Inked tensile-strength & friction comparison chart on period paper contrasting structural steel (tensile strength ~0.5–0.8 GPa, density 7.8 g/cm³) against Stephanie Kwolek's 1965 Kevlar aramid fibre (tensile strength ~3.6 GPa, density 1.44 g/cm³ = 5× stronger than steel on an equal-weight basis) and Roy Plunkett's 1938 PTFE / Teflon (coefficient of friction ~0.04, matching wet ice on wet ice, stable up to 260 °C)", "scale": "pound for pound, Stephanie Kwolek's golden Kevlar thread is five times stronger than steel — while Roy Plunkett's white Teflon is as slippery as wet ice sliding on wet ice", "who_card": "Leo Baekeland (1863–1944) — Belgian-American industrial chemist · Hermann Staudinger (1881–1965) — German organic chemist · Roy J. Plunkett (1910–1994) — American organic chemist · Stephanie Kwolek (1923–2014) — American polymer chemist", "when_stamp": "July 1907 · 1920 · 6 April 1938 · 1965", "hold_s": 3.8}),
            ("05_ivory_billiard_ball_amber_bakelite_block_teflon_ring_and_kevlar_spool_pan", 25.5, 5.5, "A", False, "6 APRIL 1938", "Fast",
             "Fast: daylight macro pan across an ivory billiard ball, an amber Bakelite block, a waxy white PTFE ring, and a spool of golden Kevlar fibre on an oak bench between code graphics so two full-frame graphics never run back to back. Nothing emissive, no face.",
             STYLE + "In crisp daylight on an oak laboratory bench, the camera pans smoothly across a carved cream billiard ball, a dark amber Bakelite moulding, a smooth white PTFE ring, and a wound spool of golden Kevlar thread." + FAST_TAIL,
             None),
            ("06_monomer_vs_staudinger_1920_macromolecule_100k_1m_da_chain_chart", 31.0, 8.0, "E", False, "5× STRONGER THAN STEEL", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period parchment, an inked monomer vs macromolecule chain-length chart compares small organic molecules (<500 Da) and the 1920 '5,000 Da ceiling' dogma against Hermann Staudinger's covalent polymer chains (100,000 to >1,000,000 Da, linking 10,000+ monomer units end to end).",
             {"kind": "DATA", "label": "STAUDINGER 1920 MACROMOLECULES: <500 DA MONOMERS & 5,000 DA DOGMA VS 100,000–1,000,000+ DA CHAINS", "detail": "Inked monomer vs macromolecule chain-length chart comparing small organic molecules (<500 Da) and the 1920 '5,000 Da ceiling' dogma against Staudinger's covalent polymer chains (100,000 to >1,000,000 Da)", "scale": "if a single monomer gas molecule were the size of a paperclip, a single polymer molecule inside a Teflon pan would be a continuous chain of paperclips stretching across a football pitch", "hold_s": 3.8}),
            ("07_table_three_props_bakelizer_pot_sawed_teflon_cylinder_golden_kevlar_spool", 39.0, 5.5, "C", False, "1907 TO 1965", "Fast",
             "Fast: daylight prop table (callback source for Part 05: Baekeland's miniature cast-iron Bakelizer vessel with amber Bakelite, Plunkett's sawed-open steel cylinder lined with white PTFE powder, and Kwolek's beaker of cloudy liquid beside a spool of golden Kevlar fibre). Nothing emissive.",
             STYLE + "On an oak workbench in soft window light sit three objects side by side: a cast-iron Bakelizer pressure pot beside an amber resin block, a sawed-open steel gas cylinder lined with white powder, and a spool of golden Kevlar thread." + FAST_TAIL,
             None),
            ("08_explorer_sliding_egg_down_white_teflon_ramp_into_golden_kevlar_hammock_under_anvil", 62.0, 5.5, "A", True, None, "Quality",
             "Quality: Explorer beat 1 (locked character reference, after 1:00).",
             STYLE + "Standing before two miniature test stations, the Explorer slides a fried egg effortlessly down a slick white Teflon ramp and catches a heavy iron anvil in a woven golden Kevlar hammock that does not stretch a millimetre." + EXP_TAIL,
             None),
            ("09_leo_baekeland_july_1907_yonkers_opening_iron_bakelizer_pressure_vessel", 67.5, 5.5, "B", False, "YONKERS, JULY 1907", "Quality",
             "Quality: readable face (in Yonkers, New York, in July 1907, 43-year-old Belgian-American chemist Leo Baekeland opens his heavy iron 'Bakelizer' pressure vessel and lifts out a gleaming amber block of Bakelite).",
             STYLE + "In a 1907 Yonkers laboratory, forty-three-year-old chemist Leo Baekeland in a dark waistcoat unbolts the lid of a heavy cast-iron pressure vessel and lifts out a smooth amber block of Bakelite." + QUAL_TAIL,
             None),
        ],
    ),
    (
        2,
        "Part 02 — July 1907 & 1920: Leo Baekeland's 'Bakelizer' & Why Chemists Mocked Hermann Staudinger's Giant Chains",
        [
            ("01_baekeland_july_1907_yonkers_bakelite_and_staudinger_1920_zurich_lecture", 73.0, 6.5, "A", False, "WARNED GIANT MOLECULES IMPOSSIBLE", "Quality",
             "Quality: readable faces (Leo Baekeland in July 1907 in Yonkers moulding amber Bakelite from phenol and formaldehyde, dissolving to 39-year-old German chemist Hermann Staudinger at ETH Zurich in 1920–1926 defending giant covalent macromolecules against critics).",
             STYLE + "Split period scene: on the left in 1907 Yonkers, Leo Baekeland pours amber phenol-formaldehyde resin into a mould; on the right in a 1920 Zurich lecture hall, Hermann Staudinger holds up a long linked chain model before sceptical professors." + QUAL_TAIL,
             {"kind": "FACT", "label": "Warned giant molecules impossible", "when_stamp": "July 1907 · 1920 · 1926 · 1953", "timeline_step": "1/5 · Jul 1907 (Leo Baekeland in Yonkers, New York, invents Bakelite, the first fully synthetic plastic) & 2/5 · 1920–1926 (Hermann Staudinger proves polymers are giant covalent macromolecule chains of thousands of atoms)", "hold_s": 3.8}),
            ("02_staudinger_1920_covalent_macromolecule_chain_vs_5000_da_colloidal_clump_chart", 79.5, 8.0, "E", False, "1920 STAUDINGER 'ÜBER POLYMERISATION': COVALENT MACROMOLECULE CHAINS (10,000–100,000+ UNITS) VS <5,000 DA CLUMP MYTH", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked polymer-chain vs colloidal-clump comparison diagram from Hermann Staudinger (1920, Berichte der deutschen chemischen Gesellschaft 53: 1073–1085) contrasts the old micelle/aggregate myth (<5,000 Da rings) against Staudinger's covalent macromolecule chains (10,000 to >100,000 repeating monomer units remaining giant chains even after hydrogenation).",
             {"kind": "DATA", "label": "1920 STAUDINGER PROOF: GIANT COVALENT MACROMOLECULE CHAINS (10,000–100,000+ UNITS) VS <5,000 DA AGGREGATE MYTH", "detail": "Inked polymer-chain vs colloidal-clump comparison diagram on period paper from Hermann Staudinger (1920, Berichte der deutschen chemischen Gesellschaft 53: 1073–1085) contrasting the old micelle/aggregate myth (<5,000 Da rings) against Staudinger's covalent macromolecule chains (10,000 to >100,000 repeating monomer units remaining giant chains even after hydrogenation)", "scale": "chemists in nineteen twenty insisted no single molecule could hold more than a few hundred atoms — yet Hermann Staudinger proved a single strand of rubber or plastic is a continuous chain of hundreds of thousands of atoms bolted together", "hold_s": 3.8}),
            ("03_bakelite_telephone_radio_casing_and_ivory_billiard_balls_closeup", 87.5, 6.5, "B", False, "JULY 1907 — BAKELITE", "Fast",
             "Fast: daylight macro shot of a vintage dark-amber Bakelite rotary telephone and radio casing beside elephant-ivory billiard balls and Baekeland's glass flasks of phenol and formaldehyde on an oak bench. Nothing emissive, no face.",
             STYLE + "In crisp daylight on a wooden table, a polished dark-brown Bakelite telephone and vintage radio casing sit beside cream billiard balls and two stoppered glass reagent bottles." + FAST_TAIL,
             None),
            ("04_staudinger_1920_berichte_paper_and_linked_brass_chain_model_pan", 94.0, 5.5, "C", False, "1920 — MACROMOLECULES", "Fast",
             "Fast: daylight close-up of Hermann Staudinger's 1920 printed Berichte paper beside a long coiled chain of thousands of linked brass paperclips and a viscometer tube on an oak desk. Nothing emissive, no face.",
             STYLE + "In bright window light on an oak desk, an open 1920 German chemistry journal lies beside a glass Ostwald viscometer tube and a long continuous chain of linked brass clips." + FAST_TAIL,
             None),
        ],
    ),
    (
        3,
        "Part 03 — 6 April 1938: Roy Plunkett's 'Empty' Frozen Cylinder & Why Nothing Sticks to Teflon — Midpoint Twist",
        [
            ("01_plunkett_and_rebok_6_apr_1938_hacksawing_open_steel_cylinder_of_white_ptfe", 99.5, 6.5, "A", False, "SAWED STEEL TANK OPEN", "Quality",
             "Quality: readable faces (27-year-old chemist Roy Plunkett and technician Jack Rebok on 6 April 1938 at DuPont's Jackson Laboratory in Deepwater, New Jersey, sawing open the 'empty' steel TFE gas cylinder with a hacksaw to reveal waxy white PTFE Teflon powder, alongside French engineer Marc Grégoire in 1954 with a PTFE-coated aluminium frying pan).",
             STYLE + "Split period scene: on the left in a 1938 DuPont lab, Roy Plunkett and Jack Rebok saw a steel gas cylinder in half with a hacksaw to reveal a thick white inner crust of PTFE powder; on the right in 1954 France, engineer Marc Grégoire holds a non-stick aluminium skillet." + QUAL_TAIL,
             {"kind": "WHO", "label": "Jack Rebok (1914–1999) — DuPont laboratory technician · Marc Grégoire (1906–1996) — French engineer and Tefal founder", "fact_card": "Sawed steel tank open", "when_stamp": "6 April 1938 · 1943 · 1945 · 1954", "timeline_step": "3/5 · 6 Apr 1938 (Roy Plunkett and Jack Rebok saw open an 'empty' frozen TFE gas cylinder at DuPont to discover PTFE / Teflon) & 4/5 · 1954 (Marc Grégoire coats aluminium pans with Teflon to create Tefal non-stick cookware)", "hold_s": 3.8}),
            ("02_plunkett_1938_c2f4_mass_balance_and_485_kj_mol_c_f_bond_armour_chart", 106.0, 8.0, "E", False, "6 APR 1938 PTFE DISCOVERY: 100% MASS CONSERVATION (C2F4 GAS → SOLID PTFE) · 485 KJ/MOL C–F BOND ARMOUR (0.04 FRICTION)", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked cylinder mass-balance and carbon-fluorine bond chart from Roy Plunkett (6 April 1938 notebook & US Patent 2,230,654) shows gaseous C2F4 polymerising at 100% mass conservation into solid PTFE chains armoured by 485 kJ/mol C–F bonds (coefficient of friction 0.04, melting point 327 °C).",
             {"kind": "DATA", "label": "6 APR 1938 TEFLON: C2F4 GAS → SOLID PTFE (100% WEIGHT KEPT) · 485 KJ/MOL C–F ARMOUR (0.04 FRICTION)", "detail": "Inked cylinder mass-balance & carbon-fluorine bond chart on period paper from Roy Plunkett (6 April 1938 notebook & US Patent 2,230,654) showing gaseous C2F4 polymerising at 100% mass conservation into solid PTFE chains armored by 485 kJ/mol C–F bonds (coefficient of friction 0.04, melting point 327 °C)", "scale": "the fluorine armour around a Teflon chain is so aloof that boiling acid, molten sodium, and burnt egg whites slide off it with the same friction as wet ice on wet ice", "hold_s": 3.8}),
            ("03_sawed_steel_cylinder_cross_section_white_ptfe_powder_and_fluorine_chain_model", 114.0, 6.5, "B", False, "6 APRIL 1938 — TEFLON (PTFE)", "Fast",
             "Fast: daylight macro shot of the sawed-open steel cylinder cross-section packed with waxy white PTFE powder beside a green-and-black carbon-fluorine molecular chain model and a non-stick pan on an oak bench. Nothing emissive, no face.",
             STYLE + "In crisp daylight on a laboratory bench, a sawed-open steel cylinder half filled with waxy white powder sits beside a green-and-black ball-and-stick fluorocarbon chain model and a coated aluminium pan." + FAST_TAIL,
             None),
            ("04_plunkett_1941_patent_notebook_and_brass_balance_scale_pan", 120.5, 5.5, "C", False, "1945 — TEFLON TRADEMARK", "Fast",
             "Fast: daylight close-up pan across Roy Plunkett's 6 April 1938 laboratory notebook, US Patent 2,230,654 diagram, and a brass balance scale on an oak desk. Nothing emissive, no face.",
             STYLE + "In bright window light on an oak desk, an open 1938 laboratory notebook and printed patent drawing rest beside a heavy brass balance scale and a glass dish of white PTFE powder." + FAST_TAIL,
             None),
        ],
    ),
    (
        4,
        "Part 04 — 1965: Stephanie Kwolek's Cloudy Beaker, the Reluctant Spinneret Operator & Bulletproof Kevlar",
        [
            ("01_kwolek_1965_wilmington_cloudy_liquid_crystal_beaker_and_charles_smullen_spinneret", 126.0, 6.5, "A", False, "FIVE TIMES STEEL'S STRENGTH", "Quality",
             "Quality: readable faces (41-year-old DuPont polymer chemist Stephanie Kwolek in Wilmington, Delaware, in 1965 holding up a beaker of cloudy, buttermilk-like liquid-crystalline poly-para-phenylene terephthalamide solution and persuading spinneret technician Charles Smullen to spin it into golden Kevlar fibre).",
             STYLE + "In a 1965 DuPont laboratory in Wilmington, forty-one-year-old chemist Stephanie Kwolek holds up a glass beaker of cloudy opalescent liquid beside technician Charles Smullen at a metal spinneret machine winding shimmering golden Kevlar thread onto a bobbin." + QUAL_TAIL,
             {"kind": "WHO", "label": "Charles Smullen (1920–2005) — DuPont spinneret technician", "fact_card": "Five times steel's strength", "when_stamp": "1964 · 1965", "timeline_step": "5/5 · 1965 (Stephanie Kwolek spins a cloudy liquid-crystalline aramid solution into bulletproof Kevlar, 5× stronger than steel by weight)", "hold_s": 3.8}),
            ("02_kwolek_1965_tangled_nylon_0_8gpa_vs_aligned_liquid_crystal_kevlar_3_6gpa_chart", 132.5, 8.0, "E", False, "1965 KWOLEK LIQUID CRYSTALS: TANGLED NYLON (0.8 GPA) VS ALIGNED KEVLAR RODS (3.6 GPA AT 1.44 G/CM³ = 5× STEEL BY WEIGHT)", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked polymer-alignment and strength diagram from Stephanie Kwolek (1965 notebook & US Patent 3,671,542) compares tangled amorphous nylon chains (~0.8 GPa tensile strength) against Kwolek's parallel liquid-crystalline poly-para-phenylene terephthalamide (Kevlar) rods linked by inter-chain hydrogen bonds (~3.6 GPa tensile strength at 1.44 g/cm³ density vs steel's ~0.5–0.8 GPa at 7.8 g/cm³).",
             {"kind": "DATA", "label": "1965 KEVLAR DISCOVERY: ALIGNED LIQUID-CRYSTAL RODS (3.6 GPA, 1.44 G/CM³) = 5× STRONGER THAN STEEL BY WEIGHT", "detail": "Inked polymer-alignment & strength diagram on period paper from Stephanie Kwolek (1965 notebook & US Patent 3,671,542) comparing tangled amorphous nylon chains (~0.8 GPa tensile strength) against Kwolek's parallel liquid-crystalline poly-para-phenylene terephthalamide (Kevlar) rods linked by inter-chain hydrogen bonds (~3.6 GPa tensile strength at 1.44 g/cm³ density vs steel's ~0.5–0.8 GPa at 7.8 g/cm³)", "scale": "a strand of Stephanie Kwolek's Kevlar thinner than a shoelace can hold up an entire family car — five times the strength of a steel wire of the exact same weight", "hold_s": 3.8}),
            ("03_cloudy_liquid_crystal_beaker_platinum_spinneret_nozzle_and_golden_kevlar_bobbin", 140.5, 6.5, "B", False, "1965 — LIQUID-CRYSTAL KEVLAR", "Fast",
             "Fast: daylight macro shot of a glass beaker of cloudy opalescent liquid beside a polished metal spinneret nozzle, a wound bobbin of golden Kevlar yarn, and a woven ballistic vest swatch on an oak bench. Nothing emissive, no face.",
             STYLE + "In crisp daylight on a laboratory bench, a glass beaker of cloudy buttermilk-like liquid sits beside a perforated metal spinneret cap, a bobbin of golden Kevlar yarn, and a woven yellow fabric panel." + FAST_TAIL,
             None),
            ("04_explorer_comparing_tangled_rope_knot_against_aligned_wooden_logs_lifting_car", 147.0, 5.5, "B", True, None, "Quality",
             "Quality: Explorer beat 2 (locked character reference).",
             STYLE + "Standing at a wooden demonstration bench, the Explorer compares a loose tangled pile of string against neat parallel golden rods locked side by side that effortlessly lift a miniature iron motorcar off the table." + EXP_TAIL,
             None),
        ],
    ),
    (
        5,
        "Part 05 — The Double-Edged Legacy of Eternal Chains & How a 1,600-Year-Old Recipe Cured Malaria",
        [
            ("01_timeline_1907_1965_and_400m_tonnes_yr_global_polymer_scale_chart", 152.5, 8.5, "E", False, "1907–1965 TIMELINE · 400 MILLION TONNES/YR SYNTHETIC POLYMERS · >3,000 LIVES SAVED BY KEVLAR", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, the 5-date timeline completes: Jul 1907 (Leo Baekeland in Yonkers, New York, invents Bakelite, the first fully synthetic plastic) · 1920–1926 (Hermann Staudinger proves polymers are giant covalent macromolecule chains of thousands of atoms) · 6 Apr 1938 (Roy Plunkett and Jack Rebok saw open an 'empty' frozen TFE gas cylinder at DuPont to discover PTFE / Teflon) · 1954 (Marc Grégoire coats aluminium pans with Teflon to create Tefal non-stick cookware) · 1965 (Stephanie Kwolek spins a cloudy liquid-crystalline aramid solution into bulletproof Kevlar, 5× stronger than steel by weight) alongside the 400 million tonnes/year global plastic production curve.",
             {"kind": "DATA", "label": "1907–1965 TIMELINE · 400 MILLION TONNES/YR GLOBAL POLYMERS · >3,000 POLICE OFFICERS SAVED BY KEVLAR", "detail": "Animated 5-date timeline (Jul 1907 → 1965) alongside humanity's 400 million tonnes/year synthetic polymer production and Kevlar's >3,000 documented lives saved", "scale": "humanity went from Leo Baekeland's single iron pot in nineteen oh seven to making four hundred million tonnes of synthetic polymers every single year — more than the total weight of every human alive on Earth", "fact_card": "Saved 3,000+ police officers", "when_stamp": "1907–1965", "timeline_step": "5/5 · 1907–1965 timeline complete", "hold_s": 3.8}),
            ("02_kevlar_helmet_spacecraft_teflon_seal_and_recyclable_polymer_chain_model_pan", 161.0, 5.5, "A", False, "BUILT TO LAST FOREVER", "Fast",
             "Fast: daylight close-up of a woven golden Kevlar protective vest, a machined white PTFE spacecraft seal ring, and a modular snap-apart polymer chain model on a museum plinth. Nothing emissive, no face.",
             STYLE + "In crisp daylight on a wooden museum plinth, a woven golden Kevlar vest panel sits beside a precision white PTFE seal ring and a colourful modular ball-and-stick polymer chain." + FAST_TAIL,
             None),
            ("03_perkin_easter_1856_mauveine_ross_1897_mosquito_and_tu_youyou_1971_artemisinin_handoff", 166.5, 6.5, "C", False, "COAL TAR, MOSQUITOES, ARTEMISININ", "Quality",
             "Quality: readable faces (18-year-old William Henry Perkin during Easter 1856 holding a purple Mauveine-dyed silk strip in his London attic lab, Ronald Ross on 20 August 1897 at his microscope in India, and Tu Youyou on 4 October 1971 in Beijing with a 340 AD Chinese scroll and sweet wormwood extract — handoff to 048 Malaria, Quinine & Artemisinin).",
             STYLE + "Split period scene: on the left in an 1856 London attic lab, eighteen-year-old William Henry Perkin lifts a brilliant purple silk cloth from a coal-tar beaker; on the right in 1971 Beijing, chemist Tu Youyou holds a flask of clear cold-ether sweet wormwood extract beside an ancient Chinese scroll." + QUAL_TAIL,
             {"kind": "WHEN", "label": "EASTER 1856 · 20 AUGUST 1897 · 4 OCTOBER 1971", "hold_s": 3.5}),
            ("04_table_three_callback", 173.0, 2.4, "C", False, None, "reuse",
             "Reuse: verified unused moving window [5.50s..7.90s] of P1:07_table_three_props_bakelizer_pot_sawed_teflon_cylinder_golden_kevlar_spool (callback, £0).",
             "Reuse P1:07_table_three_props_bakelizer_pot_sawed_teflon_cylinder_golden_kevlar_spool [5.50s..7.90s] (2.40s distinct non-overlapping tail window from 8.00s source clip).",
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
                row["reuse_of"] = "P1:07_table_three_props_bakelizer_pot_sawed_teflon_cylinder_golden_kevlar_spool"
                row["reuse_window_s"] = [5.5, 7.9]
                row["reuse_audit"] = {
                    "source_row": "P1:07_table_three_props_bakelizer_pot_sawed_teflon_cylinder_golden_kevlar_spool",
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
            "film": "047_Baekeland-Staudinger-Plunkett-Kwolek-Plastics-Teflon-Kevlar",
            "part": p_idx,
            "title": p_title,
            "version": "v01",
            "timing_status": "pre_vo_script_clock (built from plastics_script_master_v01.md; retimes onto Scribe STT once VO locks)",
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
        "film": "047_Baekeland-Staudinger-Plunkett-Kwolek-Plastics-Teflon-Kevlar",
        "version": "v01",
        "date": "2026-10-18",
        "owner": "gemini (J0555/J0570)",
        "status": "PRE_VO_BOARDS_V01_NO_MINT",
        "generation_authorized": False,
        "script": "00_Brand/Channel-Setup/ideas/047_Baekeland-Staudinger-Plunkett-Kwolek-Plastics-Teflon-Kevlar/plastics_script_master_v01.md",
        "sources": "00_Brand/Channel-Setup/ideas/047_Baekeland-Staudinger-Plunkett-Kwolek-Plastics-Teflon-Kevlar/SOURCES_v01.md",
        "credit_snapshot": {
            "flow_balance": 23740,
            "flow_floor": 0,
            "flow_read_at": "2026-10-15T21:42:22Z",
            "vertex_promo_gbp": 71.02,
            "vertex_usable_gbp": 70.02,
        },
        "totals": totals,
        "per_part": per_part_summary,
        "mint_order": "006 > 007 > 008 > 009 > 010 > 011 > 012 > 013 > 014 > 015 > 016 > 017 > 018 > 019 > 020 > 021 > 022 > 023 > 024 > 025 > 026 > 027 > 028 > 029 > 030 > 031 > 032 > 033 > 034 > 035 > 036 > 037 > 038 > 039 > 040 > 041 > 042 > 043 > 044 > 045 > 046 > 047 > 048 > 049 > 050. Nothing in 047 is generation_authorized.",
    }
    (EDIT / "PICTURE_PLAN_v01.json").write_text(json.dumps(plan, indent=2) + "\n")

    sl = [
        "# 047 Teflon & Kevlar: The Lab Accidents Stronger Than Steel — Shot list & plate boards v01 (pre-VO)",
        "",
        "Gemini, 18 Oct 2026, J0555/J0570. Built from `plastics_script_master_v01.md` (`91.0 PASS`) and `SOURCES_v01.md`.",
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
        "# 047 price review v01 (pre-VO plate boards)",
        "",
        "Gemini, 18 Oct 2026, J0555/J0570. Boards only. **No mint. No spend. No merge.**",
        "Prepared from `plastics_script_master_v01.md` (`91.0 PASS`) and `SOURCES_v01.md` so 047's full plate board rows, non-emissive Fast prompts, £0 code graphics, and Teach-on-Screen overlays are ready to re-time the moment long VO locks. Parked for Chief.",
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
        f"- **Quality ({totals['Quality']} rows):** readable faces (Roy Plunkett, Jack Rebok, Stephanie Kwolek, Charles Smullen, Leo Baekeland, Hermann Staudinger, Marc Grégoire, William Henry Perkin, Tu Youyou), 1938 Deepwater Teflon discovery, 1965 Wilmington Kevlar spinning, 1907 Yonkers Bakelizer, 1920 Zurich macromolecule lecture, and the 2 Explorer beats.",
        f"- **Fast ({totals['Fast']} rows, non-emissive):** daylight prop and laboratory shots (ivory billiard ball, amber Bakelite, white PTFE ring & golden Kevlar spool pan, 3-object callback bench, Bakelite rotary telephone & radio casing, Staudinger's 1920 *Berichte* paper & linked brass clip chain, sawed-open steel cylinder cross-section & fluorocarbon chain model, Plunkett's 1938 notebook & brass scale, cloudy liquid-crystal beaker & metal spinneret nozzle, Kevlar vest swatch & PTFE spacecraft seal). Zero candles, flames, sparks, or glowing elements on Fast.",
        f"- **£0 code graphics ({totals['code_graphic']} rows):**",
        "  1. `P1:04_steel_vs_kevlar_5x_strength_3_6gpa_and_teflon_0_04_wet_ice_friction_chart` — Structural steel (~0.5–0.8 GPa at 7.8 g/cm³) vs Stephanie Kwolek's 1965 Kevlar (~3.6 GPa at 1.44 g/cm³ = 5× stronger by weight) and Roy Plunkett's 1938 PTFE / Teflon (0.04 friction = wet ice on wet ice) (`SCALE: pound for pound, Stephanie Kwolek's golden Kevlar thread is five times stronger than steel — while Roy Plunkett's white Teflon is as slippery as wet ice sliding on wet ice`)",
        "  2. `P1:06_monomer_vs_staudinger_1920_macromolecule_100k_1m_da_chain_chart` — Small monomer (<500 Da) and 1920 '5,000 Da ceiling' dogma vs Staudinger's 100,000–1,000,000+ Da covalent polymer chains (`SCALE: if a single monomer gas molecule were the size of a paperclip, a single polymer molecule inside a Teflon pan would be a continuous chain of paperclips stretching across a football pitch`)",
        "  3. `P2:02_staudinger_1920_covalent_macromolecule_chain_vs_5000_da_colloidal_clump_chart` — Staudinger's 1920 *Über Polymerisation* covalent macromolecule chains (10,000–100,000+ repeating units) vs the colloidal-aggregate myth (`SCALE: chemists in nineteen twenty insisted no single molecule could hold more than a few hundred atoms — yet Hermann Staudinger proved a single strand of rubber or plastic is a continuous chain of hundreds of thousands of atoms bolted together`)",
        "  4. `P3:02_plunkett_1938_c2f4_mass_balance_and_485_kj_mol_c_f_bond_armour_chart` — Plunkett's 6 April 1938 100% mass-conserved C2F4 → PTFE polymerization & 485 kJ/mol C–F bond armour (0.04 friction, 327 °C melting point) (`SCALE: the fluorine armour around a Teflon chain is so aloof that boiling acid, molten sodium, and burnt egg whites slide off it with the same friction as wet ice on wet ice`)",
        "  5. `P4:02_kwolek_1965_tangled_nylon_0_8gpa_vs_aligned_liquid_crystal_kevlar_3_6gpa_chart` — Kwolek's 1965 tangled nylon (~0.8 GPa) vs aligned liquid-crystalline Kevlar rods (~3.6 GPa at 1.44 g/cm³ = 5× stronger than steel by weight) (`SCALE: a strand of Stephanie Kwolek's Kevlar thinner than a shoelace can hold up an entire family car — five times the strength of a steel wire of the exact same weight`)",
        "  6. `P5:01_timeline_1907_1965_and_400m_tonnes_yr_global_polymer_scale_chart` — completed 5-date timeline (Jul 1907 → 1965) + 400 million tonnes/year global polymer production & >3,000 lives saved by Kevlar (`SCALE: humanity went from Leo Baekeland's single iron pot in nineteen oh seven to making four hundred million tonnes of synthetic polymers every single year — more than the total weight of every human alive on Earth`)",
        f"- **£0 verified reuse ({totals['reuse']} row):** `P5:04_table_three_callback` uses the 2.40 s unused moving tail `[5.50s..7.90s]` of `P1:07_table_three_props_bakelizer_pot_sawed_teflon_cylinder_golden_kevlar_spool`.",
        "",
        "## Mint order",
        "",
        "006 > 007 > 008 > 009 > 010 > 011 > 012 > 013 > 014 > 015 > 016 > 017 > 018 > 019 > 020 > 021 > 022 > 023 > 024 > 025 > 026 > 027 > 028 > 029 > 030 > 031 > 032 > 033 > 034 > 035 > 036 > 037 > 038 > 039 > 040 > 041 > 042 > 043 > 044 > 045 > 046 > 047. `generation_authorized` is `false` on every row.",
    ])
    (EDIT / "PRICE_REVIEW_v01.md").write_text("\n".join(pr_lines) + "\n")
    print(f"047 v01 boards written: {totals['rows']} rows, Flow expected={totals['flow_credits_expected']}")


if __name__ == "__main__":
    main()
