#!/usr/bin/env python3
"""HOS 073 (Xylem: How Trees Beat the 10-Metre Limit) pre-VO plate boards v01. J0706. No mint, no spend.

Built from 00_Brand/Channel-Setup/ideas/073_Hales-Strasburger-Dixon-Joly-Scholander-Trees-Xylem/xylem_script_master_v01.md
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
        "Part 01 — The Poisoned 22-Metre Oak in Bonn & the 10-Metre Suction Wall",
        [
            ("01_10_3m_vacuum_suction_pipe_cavitating_vs_100m_california_redwood_pulling_water_under_negative_15_atm", 0.0, 5.5, "A", False, "100 METRES WITHOUT A PUMP", "Quality",
             "Quality: Short frame 0 / answer image (0:03) + side by side, a glass suction pipe snaps into a boiling vacuum cavitation gap at 10.3 metres (34 feet) while a 100-metre California redwood tree pulls unbroken blue threads of water all the way to its top needles through microscopic dead xylem pipes under -15 atmospheres of tension.",
             STYLE + "Split forest-and-physics scene: on the left, a tall vertical glass suction pipe stalls as the water column breaks into a boiling vapour gap at ten metres; on the right, a towering California coast redwood pulls continuous blue streams of water up microscopic wooden xylem conduits to its hundred-metre crown." + QUAL_TAIL,
             {"kind": "WHEN", "label": "DUBLIN, 15 NOVEMBER 1894", "timeline_step": "1/3 · 1727 & 1891 (Stephen Hales measures root pressure & transpiration; Eduard Strasburger proves a 22-m poisoned oak lifts water through dead xylem)", "hold_s": 3.5}),
            ("02_hales_1727_grapevine_strasburger_1891_poisoned_oak_dixon_joly_1894_and_scholander_1965_rifle_split", 5.5, 6.0, "B", False, "GRAPEVINE GAUGE, POISONED OAK, RIFLE PRESSURE BOMB", "Quality",
             "Quality: complex three-part composition (Stephen Hales in his Teddington vicarage garden in 1727 tying a glass mercury manometer onto a cut grapevine stump; Eduard Strasburger in Bonn in 1891 hoisting a 22-metre sawed-off oak trunk into a vat of yellow picric acid poison alongside Henry Dixon and John Joly at Trinity College Dublin on 15 November 1894; and Per Scholander in the California redwood forest in April 1965 aiming a .22 rifle at a 90-metre tree crown beside his steel pressure bomb).",
             STYLE + "Three-panel period composition: on the left, Stephen Hales in 1727 Teddington tying a glass mercury tube to a cut grapevine; in the centre, Eduard Strasburger in 1891 Bonn hoisting a twenty-two-metre oak trunk into yellow picric acid alongside Henry Dixon and John Joly in 1894 Dublin; on the right, Per Scholander in 1965 California aiming a hunting rifle at a redwood twig beside a steel pressure chamber." + QUAL_TAIL,
             None),
            ("03_microscopic_50um_xylem_conduit_with_hydrogen_bonded_water_chain_and_bordered_pit_valve", 11.5, 6.0, "C", False, "-15 ATMOSPHERES OF NEGATIVE TENSION", "Quality",
             "Quality: complex microscopic reveal (zooming inside a 50-micrometre xylem vessel in a redwood trunk: hydrogen-bonded water molecules cling together in an unbroken chain under -15 atmospheres of negative tension while bordered pit-membrane safety valves block a cavitation air bubble in a neighbouring pipe from spreading).",
             STYLE + "Macro cutaway inside two parallel wooden xylem tubes: in the left conduit, linked water molecules rise smoothly in an unbroken chain under tension while a torus-margo bordered pit valve slams shut against an air bubble forming in the neighbouring conduit." + QUAL_TAIL,
             {"kind": "WHEN", "label": "1727 · 1891 · 15 NOVEMBER 1894 · 16 APRIL 1965", "timeline_step": "1/3 · 1727 & 1891 (Hales & Strasburger) · 2/3 · 15 Nov 1894 (Dixon & Joly) · 3/3 · 16 Apr 1965 (Scholander)", "hold_s": 3.5}),
            ("04_hales_1727_strasburger_1891_dixon_joly_1894_and_scholander_1965_xylem_tension_chart", 17.5, 8.0, "E", False, "10.3 M VACUUM LIMIT VS -15 TO -20 ATM REDWOOD XYLEM TENSION (90–100 M) & -80 ATM DESERT SHRUBS", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked Xylem Ascent of Sap & Cohesion-Tension chart from Hales (1727 Vegetable Staticks), Strasburger (1891), Dixon & Joly (15 November 1894 / 1895 Phil. Trans. R. Soc. B 186: 563–576), and Scholander, Hammel, Bradstreet & Hemmingsen (16 April 1965 Science 148: 339–346) compares the 10.3-metre (+1 atm to 0 atm) mechanical suction limit against the -15 to -20 atm negative xylem pressure gradient at 90–100 metres in Sequoia sempervirens (and -80 atm in desert shrubs), driven by 5-nm leaf cell-wall menisci and hydrogen-bond water cohesion (tensile strength up to ~250–300 atm).",
             {"kind": "DATA", "label": "10.3 M SUCTION LIMIT (+1 → 0 ATM) VS -15 TO -20 ATM REDWOOD XYLEM TENSION (100 M) & -80 ATM DESERT SHRUBS", "detail": "Inked sap-ascent pressure chart on period paper showing mechanical suction failing at +1 to 0 atm (10.3 m water height), Hales's spring grapevine root pressure (+1.1 atm = 82.5 cm Hg, dropping to 0 in summer), Strasburger's dead poisoned oak lifting water 22 m, and Dixon-Joly / Scholander negative xylem tension reaching -15 to -20 atm at 90–100 m (and -80 atm in desert plants)", "scale": "a vacuum pump tries to push water up from the bottom using one atmosphere of air pressure and gives up at ten metres — a redwood tree pulls water from the top like a climber hauling a steel cable, because bubble-free water molecules cling together with a tensile strength a tenth as strong as steel wire", "who_card": "Stephen Hales (1677–1761) — English clergyman and physiologist · Eduard Strasburger (1844–1912) — German-Polish botanist · Henry Horatio Dixon (1869–1953) — Irish plant physiologist · John Joly (1857–1933) — Irish physicist and geologist · Per Fredrik Scholander (1905–1980) — Norwegian-American physiologist", "when_stamp": "1727 · 1891 · 15 November 1894 · 16 April 1965", "hold_s": 3.8}),
            ("05_hales_1727_vegetable_staticks_plate_xylem_wood_block_and_1895_phil_trans_offprint_pan", 25.5, 5.5, "A", False, "THE HUNDRED-METRE WATERFALL RUNNING UPWARDS", "Fast",
             "Fast: daylight macro pan across Stephen Hales's 1727 Vegetable Staticks engraving, a polished cross-section of redwood xylem wood, and an 1895 Philosophical Transactions offprint on an oak bench between code graphics so two full-frame graphics never run back to back. Nothing emissive, no face.",
             STYLE + "In crisp daylight on an oak botany bench, the camera pans smoothly across a 1727 copperplate book open to a grapevine mercury gauge, a polished wedge of redwood timber, and an 1895 Royal Society offprint." + FAST_TAIL,
             None),
            ("06_dixon_joly_15_nov_1894_phil_trans_leaf_meniscus_cohesion_tension_chart", 31.0, 8.0, "E", False, "DUBLIN, 15 NOVEMBER 1894", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period parchment, an inked Dixon & Joly Leaf Meniscus & Cohesion-Tension diagram (from Henry H. Dixon & John Joly, read 15 November 1894, Phil. Trans. R. Soc. Lond. B 186: 563–576) shows water evaporating from microscopic curved nanopores in spongy mesophyll cell walls inside a leaf, creating surface-tension capillary pull transmitted down continuous dead xylem conduits all the way from leaf to root.",
             {"kind": "DATA", "label": "15 NOV 1894 DIXON & JOLY (PHIL. TRANS. B): 5–10 NM LEAF MENISCUS PULL & ~250–300 ATM WATER TENSILE STRENGTH", "detail": "Inked Dixon & Joly (1895 Phil. Trans. R. Soc. B 186: 563–576) capillary meniscus pull & water tensile strength table showing nanopores (~5–10 nm radius) generating up to -150 to -300 atmospheres of capillary tension without cavitating in air-free xylem tubes", "scale": "billions of microscopic water curves in a tree's leaves act like billions of tiny tug-of-war hands pulling on the same unbroken liquid rope — every time one water molecule evaporates into the sky, the entire hundred-metre chain shifts one molecule higher", "hold_s": 3.8}),
            ("07_table_three_props_1727_hales_manometer_1894_dixon_glass_bulb_and_1965_scholander_pressure_bomb", 39.0, 5.5, "C", False, "1727 TO 1965", "Fast",
             "Fast: daylight prop table (callback source for Part 05: Stephen Hales's 1727 U-shaped glass mercury manometer, Dixon & Joly's 1894 glass pressure chamber with a leafy twig, and Per Scholander's 1965 steel pressure-bomb chamber with dial gauge). Nothing emissive.",
             STYLE + "On an oak workbench in soft window light sit three objects side by side: a 1727 U-shaped glass mercury gauge, an 1894 thick-walled glass bulb holding a leafy branch, and a 1965 cylindrical steel pressure chamber with a brass dial gauge." + FAST_TAIL,
             None),
            ("08_explorer_stalling_at_10m_suction_tube_then_hauling_linked_water_molecule_chain_up_narrow_xylem_pipe", 62.0, 5.5, "A", True, None, "Quality",
             "Quality: Explorer beat 1 (locked character reference, after 1:00).",
             STYLE + "Standing between a wide glass vacuum pipe that stalls with a vapour gap at the ten-metre mark and a narrow wooden xylem pipe, the Explorer links blue water-molecule spheres into a tight chain inside the xylem pipe and hoists the unbroken chain smoothly upward toward the treetop." + EXP_TAIL,
             None),
            ("09_dixon_and_joly_15_nov_1894_dublin_observing_leafy_branch_transpiring_inside_glass_pressure_chamber", 67.5, 5.5, "B", False, "THE COHESION-TENSION PROOF", "Quality",
             "Quality: readable faces (at Trinity College Dublin on 15 November 1894, Henry Horatio Dixon and John Joly seal a leafy branch into a glass pressure chamber and watch it keep drawing water up its stem even against compressed air).",
             STYLE + "In an 1894 Trinity College Dublin laboratory, Henry Horatio Dixon and John Joly lean beside a thick glass pressure vessel containing a leafy maple branch whose lower stem draws water steadily from a graduated tube." + QUAL_TAIL,
             {"kind": "WHEN", "label": "DUBLIN, 15 NOVEMBER 1894", "timeline_step": "2/3 · 15 Nov 1894 (Dixon & Joly unveil the Cohesion-Tension Theory of sap ascent)", "hold_s": 3.5}),
        ],
    ),
    (
        2,
        "Part 02 — 1727 & 1891: Stephen Hales's Bleeding Grapevine & Eduard Strasburger's 22-Metre Poisoned Oak",
        [
            ("01_stephen_hales_1727_teddington_grapevine_and_eduard_strasburger_1891_bonn_22m_poisoned_oak", 73.0, 6.5, "A", False, "DEAD WOOD LIFTS WATER", "Quality",
             "Quality: readable faces (English clergyman Stephen Hales in his Teddington vicarage garden in 1727 measuring sunflower transpiration and spring grapevine root pressure of 32.5 inches of mercury, dissolving to German-Polish botanist Eduard Strasburger in Bonn in 1891 hoisting a 22-metre sawed-off oak tree into a vat of yellow picric acid poison and red fuchsin dye).",
             STYLE + "Split period scene: on the left in 1727 Teddington, clergyman Stephen Hales notes the mercury level in a glass manometer tied to a spring grapevine stump beside a weighed potted sunflower; on the right in 1891 Bonn, Eduard Strasburger watches red dye climb a twenty-two-metre oak trunk standing in a vat of yellow picric acid." + QUAL_TAIL,
             {"kind": "FACT", "label": "Dead wood lifts water", "when_stamp": "1727 · 1884 · 1891", "timeline_step": "1/3 · 1727 & 1891 (Hales's Vegetable Staticks; Strasburger's 22-metre picric-acid poisoned oak)", "hold_s": 3.8}),
            ("02_hales_1727_manometer_and_strasburger_1891_22m_poisoned_oak_sap_ascent_chart", 79.5, 8.0, "E", False, "1727 HALES (VEGETABLE STATICKS: +82.5 CM HG SPRING ROOT PRESSURE VS 0 IN SUMMER) & 1891 STRASBURGER 22-M POISONED OAK", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked Stephen Hales (1727 Vegetable Staticks Exps. I & XXXVI) sunflower transpiration & grapevine mercury manometer chart (+82.5 cm Hg = +1.1 atm spring root pressure vs 0 atm in summer) alongside Eduard Strasburger (1891) 22-metre picric-acid poisoned oak sap-ascent diagram (surpassing the 10.3-metre vacuum limit with 0 living cells).",
             {"kind": "DATA", "label": "1727 HALES (+1.1 ATM SPRING ROOT PRESSURE) & 1891 STRASBURGER 22-M PICRIC-ACID POISONED OAK (SURPASSING 10.3 M WITH 0 LIVING CELLS)", "detail": "Inked Stephen Hales (1727 Vegetable Staticks Exps. I & XXXVI) sunflower transpiration & grapevine mercury manometer chart (+82.5 cm Hg = +1.1 atm spring root pressure vs 0 atm in summer) alongside Eduard Strasburger (1891) 22-metre picric-acid poisoned oak sap-ascent diagram (surpassing the 10.3-metre vacuum limit with 0 living cells) on period paper", "scale": "Eduard Strasburger poisoning a seventy-foot oak tree and watching it keep drinking water to the top proved that a tree's plumbing has no living hearts — the wooden xylem tubes are dead microscopic drinking straws that work by pure physics", "hold_s": 3.8}),
            ("03_bonn_1891_oak_trunk_in_picric_acid_and_fuchsin_dye_vats_with_stained_leaves_closeup", 87.5, 6.5, "B", False, "1891 — DEAD XYLEM LIFTS WATER 22 METRES", "Fast",
             "Fast: daylight macro shot of the cut base of an oak trunk resting in a wooden tub of yellow picric acid and red fuchsin dye beside a cross-section of crimson-stained xylem vessels on a bench. Nothing emissive, no face.",
             STYLE + "In crisp daylight at the base of a wooden scaffold, a sawed oak trunk stands in a wooden tub of crimson dye beside a sliced wood disc showing red-stained outer xylem rings." + FAST_TAIL,
             None),
            ("04_microscopic_dead_xylem_tracheids_and_vessel_elements_model_on_oak_table_pan", 94.0, 5.5, "C", False, "HOLLOW LIGNIFIED XYLEM PIPES", "Fast",
             "Fast: daylight close-up pan across a sculpted wooden-and-brass cutaway model of hollow lignified xylem vessel elements and tracheids with spiral wall thickenings and bordered pits on an oak table. Nothing emissive, no face.",
             STYLE + "In bright window light on an oak table, a sculpted cutaway model of plant xylem conduits shows hollow lignified tubes reinforced with spiral rings and circular bordered pit valves." + FAST_TAIL,
             None),
        ],
    ),
    (
        3,
        "Part 03 — 15 November 1894: Henry Dixon & John Joly's Cohesion-Tension Theory in Dublin — Midpoint Twist",
        [
            ("01_marcellin_berthelot_1850_paris_sealed_tube_and_dixon_joly_15_nov_1894_dublin_cohesion_tension", 99.5, 6.5, "A", False, "WATER STRONGER THAN STEEL", "Quality",
             "Quality: readable faces (French chemist Marcellin Berthelot in Paris in 1850 stretching bubble-free water in a sealed glass tube to -50 atmospheres, dissolving to Irish botanist Henry Horatio Dixon and physicist John Joly at Trinity College Dublin on 15 November 1894 unveiling the Cohesion-Tension Theory).",
             STYLE + "Split period scene: on the left in 1850 Paris, Marcellin Berthelot examines a thick-walled sealed glass tube of stretched bubble-free water; on the right in November 1894 Dublin, Henry Horatio Dixon and John Joly point to a leaf-meniscus diagram beside their glass pressure apparatus." + QUAL_TAIL,
             {"kind": "FACT", "label": "Water stronger than steel", "who_card": "Marcellin Berthelot (1827–1907) — French physical chemist", "when_stamp": "1850 · 15 November 1894 · 1895", "timeline_step": "2/3 · 1850 & 15 Nov 1894 (Berthelot proves -50 atm negative tension in water; Dixon & Joly formulate the Cohesion-Tension Theory)", "hold_s": 3.8}),
            ("02_berthelot_1850_negative_pressure_tube_and_dixon_joly_1894_1895_cohesion_tension_chart", 106.0, 8.0, "E", False, "1850 BERTHELOT (-50 ATM SEALED WATER TUBE) & 15 NOV 1894 DIXON & JOLY (PHIL. TRANS. B: COHESION-TENSION UP TO ~250–300 ATM)", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked Berthelot (1850 Ann. Chim. Phys. 30: 232–237) sealed-tube negative water tension apparatus (-50 atm) & Dixon & Joly (15 November 1894 / 1895 Phil. Trans. R. Soc. B 186: 563–576) Cohesion-Tension model (5-nm leaf cell-wall menisci pulling unbroken hydrogen-bonded water columns through 20–200 µm xylem conduits with up to ~250–300 atm tensile strength).",
             {"kind": "DATA", "label": "1850 BERTHELOT (-50 ATM WATER TENSION) & 1894 DIXON-JOLY COHESION-TENSION MODEL (~250–300 ATM TENSILE STRENGTH)", "detail": "Inked Berthelot (1850 Ann. Chim. Phys. 30: 232–237) sealed-tube negative water tension apparatus (-50 atm) & Dixon & Joly (15 November 1894 / 1895 Phil. Trans. R. Soc. B 186: 563–576) Cohesion-Tension model (5-nm leaf cell-wall menisci pulling unbroken hydrogen-bonded water columns through 20–200 µm xylem conduits with up to ~250–300 atm tensile strength) on period paper", "scale": "inside a microscopic bubble-free xylem tube, hydrogen bonds lock water molecules together so tightly that it takes nearly three hundred atmospheres of pull to rip the water column apart — enough tensile strength to lift water not just a hundred metres, but nearly three kilometres into the sky", "hold_s": 3.8}),
            ("03_dublin_1894_bertelot_sealed_glass_tubes_and_porous_clay_atmometer_closeup", 114.0, 6.5, "B", False, "15 NOVEMBER 1894 — COHESION-TENSION THEORY", "Fast",
             "Fast: daylight macro shot of thick-walled Berthelot glass tubes alongside a porous white clay evaporating cup connected to a vertical glass water column and mercury reservoir on a Dublin physics bench. Nothing emissive, no face.",
             STYLE + "In crisp daylight on an 1894 Dublin laboratory bench, thick-walled sealed glass capillary tubes sit beside a porous white ceramic cup drawing a continuous column of water and mercury up a vertical glass tube." + FAST_TAIL,
             None),
            ("04_leaf_mesophyll_5nm_cell_wall_meniscus_and_hydrogen_bond_chain_model_pan", 120.5, 5.5, "C", False, "TRANSPIRATION PULL & HYDROGEN BONDING", "Fast",
             "Fast: daylight close-up pan across a sculpted leaf cross-section model showing stomatal pores, spongy mesophyll cells, and curved water menisci pulling a chain of linked water spheres up a xylem vein on an oak table. Nothing emissive, no face.",
             STYLE + "In bright window light on an oak table, a sculpted cutaway model of a green leaf shows open stomatal gates below spongy mesophyll cells where curved blue water menisci pull a vertical chain of linked water spheres up a wooden vein." + FAST_TAIL,
             None),
        ],
    ),
    (
        4,
        "Part 04 — 16 April 1965: Per Scholander's Hunting Rifle & the Pressure Bomb in the California Redwoods",
        [
            ("01_per_scholander_and_harold_hammel_16_apr_1965_california_redwoods_rifle_and_pressure_bomb", 126.0, 6.5, "A", False, "DESERT SHRUBS PULL -80 ATM", "Quality",
             "Quality: readable faces (Norwegian-American physiologist Per Fredrik Scholander and Harold T. Hammel in the California redwood forest on 16 April 1965 aiming a .22 hunting rifle at the 82-metre crown of a coast redwood Sequoia sempervirens and testing the shot twig in their steel pressure bomb reading -15 to -17 atmospheres).",
             STYLE + "In a sun-dappled 1965 California redwood grove, Per Scholander and Harold Hammel collect a freshly shot high redwood twig and seal it into a cylindrical steel pressure chamber with its cut stem protruding as the brass gauge reads fifteen atmospheres." + QUAL_TAIL,
             {"kind": "FACT", "label": "Desert shrubs pull -80 atm", "who_card": "Harold T. Hammel (1921–2005) — American comparative physiologist", "when_stamp": "16 April 1965", "timeline_step": "3/3 · 16 Apr 1965 (Per Scholander & Harold Hammel prove -15 to -80 atm negative xylem pressure with a rifle and steel pressure bomb)", "hold_s": 3.8}),
            ("02_scholander_16_apr_1965_science_pressure_bomb_and_redwood_desert_tension_gradient_chart", 132.5, 8.0, "E", False, "16 APR 1965 SCHOLANDER ET AL. (SCIENCE): REDWOOD HYDROSTATIC GRADIENT (-7 TO -17 ATM AT 82 M) & DESERT CREOSOTE (-80 ATM)", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked Scholander, Hammel, Bradstreet & Hemmingsen (16 April 1965 Science 148: 339–346) pressure-bomb schematic & vertical xylem hydrostatic tension gradient in 80–90 m Sequoia sempervirens and Douglas fir (-7 atm at 12 m to -15 to -17 atm at 82 m, matching the 0.1 atm/m gravity line, plus -35 to -60 atm in halophytes/mangroves and -80 atm in desert creosote Larrea).",
             {"kind": "DATA", "label": "16 APR 1965 SCHOLANDER PRESSURE BOMB (SCIENCE): -17 ATM AT 82 M IN REDWOODS, -60 ATM IN MANGROVES & -80 ATM IN DESERT CREOSOTE", "detail": "Inked Scholander, Hammel, Bradstreet & Hemmingsen (16 April 1965 Science 148: 339–346) pressure-bomb schematic & vertical xylem hydrostatic tension gradient in 80–90 m Sequoia sempervirens and Douglas fir (-7 atm at 12 m to -15 to -17 atm at 82 m, matching the 0.1 atm/m gravity line, plus -35 to -60 atm in halophytes/mangroves and -80 atm in desert creosote Larrea) on period paper", "scale": "Per Scholander's pressure bomb works like measuring how hard a stretched elastic band was pulling by seeing how many kilograms of weight it takes to push the snapped end back to the starting line — proving desert bushes pull water with eighty atmospheres of suction, enough negative pressure to suck fresh water straight out of salty ocean mud", "hold_s": 3.8}),
            ("03_california_1965_scholander_steel_pressure_bomb_with_protruding_redwood_stem_and_gauge_closeup", 140.5, 6.5, "B", False, "16 APRIL 1965 — NEGATIVE XYLEM PRESSURE PROVED", "Fast",
             "Fast: daylight macro shot of the steel Scholander pressure bomb with a freshly cut redwood twig protruding through its screw-cap rubber gasket as a bead of sap appears at the cut xylem surface beside a brass pressure gauge and nitrogen cylinder. Nothing emissive, no face.",
             STYLE + "In crisp daylight on a field table under redwood trees, a heavy steel pressure chamber holds a redwood twig whose cut stem pokes through a brass cap with a glistening drop of sap beside a high-pressure dial gauge." + FAST_TAIL,
             None),
            ("04_explorer_turning_nitrogen_valve_on_cutaway_pressure_bomb_to_push_retracted_water_column_back_to_stem_tip", 147.0, 5.5, "B", True, None, "Quality",
             "Quality: Explorer beat 2 (locked character reference).",
             STYLE + "Standing beside a cutaway steel pressure chamber holding a leafy redwood shoot, the Explorer watches the blue water column inside the stem snap backward when cut, then turns a brass nitrogen valve until compressed gas pushes the blue water column right back to the cut tip." + EXP_TAIL,
             None),
        ],
    ),
    (
        5,
        "Part 05 — Why No Tree Can Grow Past 130 Metres — & Why Your Lungs Don't Collapse Every Time You Exhale",
        [
            ("01_timeline_1727_2004_and_koch_sillett_130m_tree_height_limit_chart", 152.5, 8.5, "E", False, "1727–2004 TIMELINE · HALES, STRASBURGER, DIXON & JOLY, SCHOLANDER PRESSURE BOMB & KOCH-SILLETT 122–130 M HEIGHT LIMIT", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, the 3-era timeline completes: 1727 & 1891 (Stephen Hales measures sunflower transpiration and spring grapevine root pressure in Vegetable Staticks; Eduard Strasburger poisons a 22-metre oak tree and proves dead xylem lifts water past the 10.3-m suction limit) · 15 Nov 1894 (Henry Horatio Dixon & John Joly unveil the Cohesion-Tension Theory at Trinity College Dublin) · 16 Apr 1965 & 22 Apr 2004 (Per Scholander uses a hunting rifle and steel pressure bomb to measure -15 to -80 atm negative xylem pressure in redwoods and desert shrubs; George Koch & Stephen Sillett establish the 122–130 m maximum height limit of trees).",
             {"kind": "DATA", "label": "1727–2004 XYLEM & COHESION-TENSION TIMELINE · KOCH & SILLETT (2004 NATURE) 122–130 M MAXIMUM TREE HEIGHT CEILING", "detail": "Animated timeline (1727 → 2004) alongside Koch, Sillett, Jennings & Davis (22 April 2004 Nature 428: 851–854) coast redwood height ceiling chart (-18 atm xylem tension at 110+ m closing stomata and limiting maximum height to 122–130 m)", "scale": "from a vicar's garden in Teddington to a poisoned oak in Bonn, a physics lab in Dublin, and a rifle shot in the California redwoods, scientists proved that every tall tree on Earth is a silent waterfall running upwards on stretched liquid wires", "who_card": "George W. Koch (born 1958) — American plant ecophysiologist", "when_stamp": "1727–2004 · 22 April 2004", "timeline_step": "3/3 · 1727–2004 timeline complete", "hold_s": 3.8}),
            ("02_redwood_top_needle_branch_beside_scholander_pressure_gauge_on_plinth_pan", 161.0, 5.5, "A", False, "122–130 METRE TREE HEIGHT LIMIT", "Fast",
             "Fast: daylight close-up of a compact, scale-like upper-canopy coast redwood twig beside a brass Scholander pressure gauge and a cross-section of redwood trunk rings on a wooden museum plinth. Nothing emissive, no face.",
             STYLE + "In crisp daylight on a wooden museum plinth, a dense top-canopy coast redwood branchlet sits beside a brass pressure-bomb dial gauge and a polished slice of redwood growth rings." + FAST_TAIL,
             None),
            ("03_hooke_lower_1667_bellows_lung_krogh_1910_microtonometer_avery_1959_surfactant_and_perutz_1960_haemoglobin_handoff", 166.5, 6.5, "C", False, "LUNGS, ALVEOLI, HAEMOGLOBIN & SURFACTANT", "Quality",
             "Quality: readable faces (Robert Hooke and Richard Lower at the Royal Society in 1667 ventilating a lung with bellows, August and Marie Krogh in Copenhagen in 1910 reading their Seven Little Devils microtonometer, Mary Ellen Avery in Boston in May 1959 measuring newborn lung surfactant, and Max Perutz in Cambridge on 13 February 1960 with his 3D haemoglobin model — handoff to 074 Lungs, Alveoli, Haemoglobin & Pulmonary Surfactant).",
             STYLE + "Split period scene: on the left, Robert Hooke and Richard Lower in 1667 London beside August and Marie Krogh in 1910 Copenhagen with their glass microtonometer; on the right, Mary Ellen Avery in 1959 Boston at her surface-tension trough beside Max Perutz in 1960 Cambridge holding his 3D haemoglobin model." + QUAL_TAIL,
             {"kind": "WHEN", "label": "1667 · 1910 · 1929 · MAY 1959 · 13 FEBRUARY 1960", "hold_s": 3.5}),
            ("04_table_three_callback", 173.0, 2.4, "C", False, None, "reuse",
             "Reuse: verified unused moving window [5.50s..7.90s] of P1:07_table_three_props_1727_hales_manometer_1894_dixon_glass_bulb_and_1965_scholander_pressure_bomb (callback, £0).",
             "Reuse P1:07_table_three_props_1727_hales_manometer_1894_dixon_glass_bulb_and_1965_scholander_pressure_bomb [5.50s..7.90s] (2.40s distinct non-overlapping tail window from 8.00s source clip).",
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
                row["reuse_of"] = "P1:07_table_three_props_1727_hales_manometer_1894_dixon_glass_bulb_and_1965_scholander_pressure_bomb"
                row["reuse_window_s"] = [5.5, 7.9]
                row["reuse_audit"] = {
                    "source_row": "P1:07_table_three_props_1727_hales_manometer_1894_dixon_glass_bulb_and_1965_scholander_pressure_bomb",
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
            "film": "073_Hales-Strasburger-Dixon-Joly-Scholander-Trees-Xylem",
            "part": p_idx,
            "title": p_title,
            "version": "v01",
            "timing_status": "pre_vo_script_clock (built from xylem_script_master_v01.md; retimes onto Scribe STT once VO locks)",
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
        "film": "073_Hales-Strasburger-Dixon-Joly-Scholander-Trees-Xylem",
        "version": "v01",
        "date": "2026-10-20",
        "owner": "gemini (J0706)",
        "status": "PRE_VO_BOARDS_V01_NO_MINT",
        "generation_authorized": False,
        "script": "00_Brand/Channel-Setup/ideas/073_Hales-Strasburger-Dixon-Joly-Scholander-Trees-Xylem/xylem_script_master_v01.md",
        "sources": "00_Brand/Channel-Setup/ideas/073_Hales-Strasburger-Dixon-Joly-Scholander-Trees-Xylem/SOURCES_v01.md",
        "credit_snapshot": {
            "flow_balance": 23740,
            "flow_floor": 0,
            "flow_read_at": "2026-10-15T21:42:22Z",
            "vertex_promo_gbp": 71.02,
            "vertex_usable_gbp": 70.02,
        },
        "totals": totals,
        "per_part": per_part_summary,
        "mint_order": "006 > 007 > 008 > 009 > 010 > 011 > 012 > 013 > 014 > 015 > 016 > 017 > 018 > 019 > 020 > 021 > 022 > 023 > 024 > 025 > 026 > 027 > 028 > 029 > 030 > 031 > 032 > 033 > 034 > 035 > 036 > 037 > 038 > 039 > 040 > 041 > 042 > 043 > 044 > 045 > 046 > 047 > 048 > 049 > 050 > 051 > 052 > 053 > 054 > 055 > 056 > 057 > 058 > 059 > 060 > 061 > 062 > 063 > 064 > 065 > 066 > 067 > 068 > 069 > 070 > 071 > 072 > 073 > 074 > 075 > 076 > 077. Nothing in 073 is generation_authorized.",
    }
    (EDIT / "PICTURE_PLAN_v01.json").write_text(json.dumps(plan, indent=2) + "\n")

    sl = [
        "# 073 Xylem: How Trees Beat the 10-Metre Limit — Shot list & plate boards v01 (pre-VO)",
        "",
        "Gemini, 20 Oct 2026, J0706. Built from `xylem_script_master_v01.md` (`91.9/100 PASS`) and `SOURCES_v01.md`.",
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
        "# 073 price review v01 (pre-VO plate boards)",
        "",
        "Gemini, 20 Oct 2026, J0706. Boards only. **No mint. No spend. No merge.**",
        "Prepared from `xylem_script_master_v01.md` (`91.9/100 PASS`) and `SOURCES_v01.md` so 073's full plate board rows, non-emissive Fast prompts, £0 code graphics, and Teach-on-Screen overlays are ready to re-time the moment long VO locks. Parked for Chief.",
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
        f"- **Quality ({totals['Quality']} rows):** readable faces (Stephen Hales, Eduard Strasburger, Marcellin Berthelot, Henry Horatio Dixon, John Joly, Per Fredrik Scholander, Harold T. Hammel, George W. Koch, Robert Hooke, Richard Lower, August Krogh, Marie Krogh, Mary Ellen Avery, Max Perutz), 1727 Teddington grapevine manometer & 1891 Bonn `22-m` picric-acid poisoned oak, 15 November 1894 Dublin `Cohesion-Tension` apparatus, 16 April 1965 California redwood `.22` rifle & steel `Scholander pressure bomb` (`-15` to `-80 atm`), and the 2 Explorer beats.",
        f"- **Fast ({totals['Fast']} rows, non-emissive):** daylight prop and laboratory shots (1727 *Vegetable Staticks* plate, redwood xylem block & 1895 *Phil. Trans.* offprint pan, 3-object callback bench, 1891 Bonn oak trunk base in picric acid and fuchsin dye vats, sculpted lignified xylem vessel and bordered-pit valve model, 1850 Berthelot sealed tubes & 1894 porous clay atmometer, sculpted leaf mesophyll `5 nm` meniscus & water-chain model, 1965 steel Scholander pressure bomb with protruding redwood stem & dial gauge, top-canopy redwood twig beside pressure gauge on museum plinth). Zero candles, flames, sparks, or glowing elements on Fast.",
        f"- **£0 code graphics ({totals['code_graphic']} rows):**",
        "  1. `P1:04_hales_1727_strasburger_1891_dixon_joly_1894_and_scholander_1965_xylem_tension_chart` — `10.3 m` mechanical suction limit vs `-15` to `-20 atm` redwood xylem tension (`90–100 m`) and `-80 atm` desert shrubs (`SCALE: a vacuum pump tries to push water up from the bottom using one atmosphere of air pressure and gives up at ten metres — a redwood tree pulls water from the top like a climber hauling a steel cable, because bubble-free water molecules cling together with a tensile strength a tenth as strong as steel wire`)",
        "  2. `P1:06_dixon_joly_15_nov_1894_phil_trans_leaf_meniscus_cohesion_tension_chart` — Henry Dixon & John Joly (15 November 1894 *Phil. Trans. R. Soc. B*) `5–10 nm` leaf cell-wall meniscus pull & water tensile strength table (`SCALE: billions of microscopic water curves in a tree's leaves act like billions of tiny tug-of-war hands pulling on the same unbroken liquid rope — every time one water molecule evaporates into the sky, the entire hundred-metre chain shifts one molecule higher`)",
        "  3. `P2:02_hales_1727_manometer_and_strasburger_1891_22m_poisoned_oak_sap_ascent_chart` — Stephen Hales (1727 *Vegetable Staticks*) `+82.5 cm Hg` (`+1.1 atm`) spring root pressure & Eduard Strasburger (1891) `22-m` picric-acid poisoned oak (`SCALE: Eduard Strasburger poisoning a seventy-foot oak tree and watching it keep drinking water to the top proved that a tree's plumbing has no living hearts — the wooden xylem tubes are dead microscopic drinking straws that work by pure physics`)",
        "  4. `P3:02_berthelot_1850_negative_pressure_tube_and_dixon_joly_1894_1895_cohesion_tension_chart` — Marcellin Berthelot (1850) `-50 atm` sealed water tube & Dixon/Joly (1894/1895 *Phil. Trans. B*) `Cohesion-Tension` model up to `~250–300 atm` (`SCALE: inside a microscopic bubble-free xylem tube, hydrogen bonds lock water molecules together so tightly that it takes nearly three hundred atmospheres of pull to rip the water column apart — enough tensile strength to lift water not just a hundred metres, but nearly three kilometres into the sky`)",
        "  5. `P4:02_scholander_16_apr_1965_science_pressure_bomb_and_redwood_desert_tension_gradient_chart` — Per Scholander et al. (16 April 1965 *Science*) pressure-bomb schematic & `-7` to `-17 atm` redwood hydrostatic gradient + `-80 atm` desert creosote (`SCALE: Per Scholander's pressure bomb works like measuring how hard a stretched elastic band was pulling by seeing how many kilograms of weight it takes to push the snapped end back to the starting line — proving desert bushes pull water with eighty atmospheres of suction, enough negative pressure to suck fresh water straight out of salty ocean mud`)",
        "  6. `P5:01_timeline_1727_2004_and_koch_sillett_130m_tree_height_limit_chart` — completed timeline (1727 → 2004) + George Koch & Stephen Sillett (22 April 2004 *Nature*) `122–130 m` maximum tree height limit (`SCALE: from a vicar's garden in Teddington to a poisoned oak in Bonn, a physics lab in Dublin, and a rifle shot in the California redwoods, scientists proved that every tall tree on Earth is a silent waterfall running upwards on stretched liquid wires`)",
        f"- **£0 verified reuse ({totals['reuse']} row):** `P5:04_table_three_callback` uses the 2.40 s unused moving tail `[5.50s..7.90s]` of `P1:07_table_three_props_1727_hales_manometer_1894_dixon_glass_bulb_and_1965_scholander_pressure_bomb`.",
        "",
        "## Mint order",
        "",
        "006 > 007 > 008 > 009 > 010 > 011 > 012 > 013 > 014 > 015 > 016 > 017 > 018 > 019 > 020 > 021 > 022 > 023 > 024 > 025 > 026 > 027 > 028 > 029 > 030 > 031 > 032 > 033 > 034 > 035 > 036 > 037 > 038 > 039 > 040 > 041 > 042 > 043 > 044 > 045 > 046 > 047 > 048 > 049 > 050 > 051 > 052 > 053 > 054 > 055 > 056 > 057 > 058 > 059 > 060 > 061 > 062 > 063 > 064 > 065 > 066 > 067 > 068 > 069 > 070 > 071 > 072 > 073 > 074 > 075 > 076 > 077. `generation_authorized` is `false` on every row.",
    ])
    (EDIT / "PRICE_REVIEW_v01.md").write_text("\n".join(pr_lines) + "\n")
    print(f"073 v01 boards written: {totals['rows']} rows, Flow expected={totals['flow_credits_expected']}")


if __name__ == "__main__":
    main()
