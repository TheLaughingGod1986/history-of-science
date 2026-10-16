#!/usr/bin/env python3
"""HOS 072 (The Kidney: How Sausage Skin Saved Millions) pre-VO plate boards v01. J0706. No mint, no spend.

Built from 00_Brand/Channel-Setup/ideas/072_Bowman-Ludwig-Richards-Smith-Kolff-Kidneys-Dialysis/kidneys_script_master_v01.md
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
        "Part 01 — The Sausage-Casing Drum in Kampen & the 180-Litre Bathtub Inside You",
        [
            ("01_kidney_nephron_glomerulus_bowman_capsule_180_litre_filtrate_and_kolff_sausage_drum", 0.0, 5.5, "A", False, "180 LITRES FILTERED EVERY DAY", "Quality",
             "Quality: Short frame 0 / answer image (0:03) + a human kidney cross-section zooms into one of two million microscopic nephrons as high-pressure blood enters the glomerular capillary knot inside Bowman's capsule, squeezing out 180 litres of clear fluid a day while Willem Kolff's rotating wooden drum wrapped in cellophane sausage casing spins in a Kampen hospital bath beside it.",
             STYLE + "Split anatomical-and-historical scene: on the left, a kidney cross-section zooms into a microscopic glomerular capillary knot cradled inside Bowman's cup squeezing clear fluid into a winding tubule; on the right, a slatted wooden drum wound with cellophane sausage tubing rotates in a porcelain bath." + QUAL_TAIL,
             {"kind": "WHEN", "label": "KAMPEN, 11 SEPTEMBER 1945", "timeline_step": "1/3 · 17 Feb 1842 & 1844 (William Bowman maps Bowman's capsule; Carl Ludwig proposes hydrostatic glomerular ultrafiltration)", "hold_s": 3.5}),
            ("02_bowman_1842_ludwig_1844_wearn_richards_1924_homer_smith_1934_and_kolff_1945_split", 5.5, 6.0, "B", False, "BOWMAN'S CAPSULE, QUARTZ MICROPIPETTE, SAUSAGE-SKIN DIALYSIS", "Quality",
             "Quality: complex three-part composition (William Bowman at King's College Hospital in London on 17 February 1842 injecting dye to reveal Bowman's capsule alongside Carl Ludwig in Marburg in 1844; Joseph Wearn and Alfred Newton Richards at the University of Pennsylvania in October 1924 guiding a 10-micrometre quartz micropipette into a living frog glomerulus alongside Homer Smith at NYU in 1934 measuring 125 mL/min inulin clearance; and Willem Kolff in Kampen on 11 September 1945 rotating his cellophane sausage-casing drum to wake Patient #16 Sofia Schafstadt from a fatal uremic coma).",
             STYLE + "Three-panel period composition: on the left, William Bowman in 1842 London peering through a brass microscope beside Carl Ludwig; in the centre, Joseph Wearn and Alfred Richards in 1924 Philadelphia guiding a quartz micropipette into a frog kidney alongside Homer Smith in 1934 New York; on the right, Willem Kolff in September 1945 Kampen tending his rotating wooden-drum dialyser beside his waking patient." + QUAL_TAIL,
             None),
            ("03_5_litre_blood_carboy_pouring_36_times_into_180_litre_bathtub_with_99_percent_reabsorption", 11.5, 6.0, "C", False, "99% RECLAIMED BEFORE IT LEAVES", "Quality",
             "Quality: complex visual reveal (a 5-litre glass carboy of red blood pours thirty-six times into a 180-litre bathtub of clear glomerular filtrate, while aquaporin and sodium-potassium pumps along the nephron tubule pull 178.5 litres of water and 100% of the glucose back into the bloodstream, leaving 1.5 litres of golden urine).",
             STYLE + "In a warm laboratory hall, a five-litre glass carboy of crimson blood cycles through a glass glomerular sieve into a full bathtub of clear filtrate while brass pumps along a coiled glass tubule return ninety-nine percent of the water and all golden sugar crystals back to the blood." + QUAL_TAIL,
             {"kind": "WHEN", "label": "17 FEBRUARY 1842 · 1844 · 1 OCTOBER 1924 · 1934 · 11 SEPTEMBER 1945", "timeline_step": "1/3 · 17 Feb 1842 & 1844 (Bowman & Ludwig) · 2/3 · 1 Oct 1924 & 1934 (Wearn, Richards & Smith) · 3/3 · 17 Mar 1943 – 11 Sep 1945 (Kolff)", "hold_s": 3.5}),
            ("04_bowman_1842_richards_1924_smith_1935_and_kolff_1944_nephron_filtration_dialysis_chart", 17.5, 8.0, "E", False, "GFR = 125 ML/MIN (180 L/DAY ACROSS 2M NEPHRONS) · 100% GLUCOSE & 99% WATER REABSORBED · KOLFF CELLOPHANE DIALYSIS", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked Nephron Ultrafiltration, Reabsorption & Dialysis chart from Bowman (17 February 1842 Phil. Trans. R. Soc. 132: 57–80), Ludwig (1844), Wearn & Richards (1 October 1924 Am. J. Physiol. 71: 209–227), Shannon & Smith (July 1935 J. Clin. Invest. 14: 393–401), and Kolff et al. (1944 Acta Med. Scand. 117: 121–134) shows glomerular filtration rate (GFR = 125 mL/min = 180 L/day across ~2 million nephrons), 100% glucose and ~99% water tubular reabsorption, and urea clearance across a semipermeable cellophane sausage membrane.",
             {"kind": "DATA", "label": "180 L/DAY GLOMERULAR FILTRATION (125 ML/MIN), 99% WATER & 100% GLUCOSE REABSORPTION, 1.5 L/DAY URINE", "detail": "Inked nephron filtration & reabsorption balance chart on period paper showing 5 litres total blood volume filtered 36 times/day at 125 mL/min = 180 litres/day glomerular filtrate, 99% water and 100% glucose reabsorbed along the proximal tubule, Loop of Henle, and collecting duct, and 1.5 litres/day urine output", "scale": "your kidneys clean your house by throwing every single piece of furniture out the window thirty-six times a day — and then running downstairs to carry ninety-nine percent of the furniture back inside while leaving the rubbish on the pavement", "who_card": "William Bowman (1816–1892) — English surgeon and microscopist · Carl Ludwig (1816–1895) — German physiologist · Joseph T. Wearn (1893–1984) — American physician and pharmacologist · Alfred Newton Richards (1876–1966) — American pharmacologist · Homer W. Smith (1895–1962) — American renal physiologist · Willem Johan Kolff (1911–2009) — Dutch physician and inventor", "when_stamp": "17 February 1842 · 1844 · 1 October 1924 · 1934 · 11 September 1945", "hold_s": 3.8}),
            ("05_bowman_1842_plate_quartz_micropipette_holder_and_1924_ajp_offprint_pan", 25.5, 5.5, "A", False, "THE TWO-MILLION-CUP CLEANING PLANT", "Fast",
             "Fast: daylight macro pan across William Bowman's 1842 engraved glomerular plate, a brass micromanipulator holding a fine quartz micropipette, and a 1924 American Journal of Physiology offprint on an oak bench between code graphics so two full-frame graphics never run back to back. Nothing emissive, no face.",
             STYLE + "In crisp daylight on an oak physiology bench, the camera pans smoothly across an 1842 anatomical engraving of glomerular capsules, a brass micromanipulator holding a hair-thin quartz needle, and an open 1924 journal." + FAST_TAIL,
             None),
            ("06_wearn_richards_1_oct_1924_ajp_quartz_micropipette_glomerular_puncture_chart", 31.0, 8.0, "E", False, "PHILADELPHIA, 1 OCTOBER 1924", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period parchment, an inked Wearn & Richards Quartz Micropipette Glomerular Puncture diagram (from Joseph T. Wearn & Alfred N. Richards, 1 October 1924 Am. J. Physiol. 71: 209–227) shows a micromanipulator driving a 10-micrometre sharpened quartz capillary tube into a single Bowman's capsule on the illuminated surface of a living frog kidney, withdrawing ~1 microlitre of protein-free plasma containing glucose and chloride that vanish in the bladder urine.",
             {"kind": "DATA", "label": "1 OCT 1924 WEARN & RICHARDS (AM. J. PHYSIOL.): GLOMERULAR FILTRATE = 0 PROTEIN + FULL GLUCOSE/NACL; BLADDER URINE = 0 GLUCOSE", "detail": "Inked Wearn & Richards (1 October 1924 Am. J. Physiol. 71: 209–227) frog glomerular fluid vs bladder urine chemical table showing glomerular filtrate has 0 protein, full blood glucose, and full NaCl, while final bladder urine has 0 glucose and ~1/10th the salt", "scale": "puncturing a single Bowman's capsule with a quartz needle ten micrometres wide is like threading a needle thinner than a human hair into a water balloon the size of a grain of sand without popping the blood vessels inside", "hold_s": 3.8}),
            ("07_table_three_props_1842_bowman_microscope_1924_quartz_micropipette_and_1945_kolff_sausage_spool", 39.0, 5.5, "C", False, "1842 TO 1945", "Fast",
             "Fast: daylight prop table (callback source for Part 05: William Bowman's 1842 brass microscope with injected kidney slide, Alfred Richards's 1924 quartz micropipette in its brass holder, and Willem Kolff's 1945 spool of cellophane sausage casing). Nothing emissive.",
             STYLE + "On an oak workbench in soft window light sit three objects side by side: an 1842 brass microscope with a red-and-blue injected kidney slide, a brass micromanipulator holding a fine quartz capillary needle, and a wooden spool of transparent cellophane sausage casing." + FAST_TAIL,
             None),
            ("08_explorer_pouring_marbles_sugar_cubes_and_water_beads_into_glass_bowman_capsule_and_reclaiming_99_percent", 62.0, 5.5, "A", True, None, "Quality",
             "Quality: Explorer beat 1 (locked character reference, after 1:00).",
             STYLE + "Standing beside a tall glass model of Bowman's capsule and its winding nephron tubule, the Explorer pours red blood marbles, golden sugar cubes, and blue water beads into the sieve; the red marbles stay in the upper vessel while brass hands along the glass pipe snatch every golden sugar cube and ninety-nine of every hundred blue beads back out of the drain." + EXP_TAIL,
             None),
            ("09_wearn_and_richards_oct_1924_philadelphia_guiding_quartz_micropipette_into_frog_glomerulus", 67.5, 5.5, "B", False, "THE MICROPIPETTE PROOF", "Quality",
             "Quality: readable faces (in Philadelphia in October 1924, Joseph Wearn and Alfred Newton Richards peer through a stereoscopic microscope as a quartz micropipette draws a glistening microlitre droplet from a single living frog Bowman's capsule).",
             STYLE + "In a 1924 Philadelphia laboratory, Joseph Wearn and Alfred Newton Richards lean over a binocular microscope, turning a brass micromanipulator screw to guide a fine quartz needle into a single glomerular capsule." + QUAL_TAIL,
             {"kind": "WHEN", "label": "PHILADELPHIA, 1 OCTOBER 1924", "timeline_step": "2/3 · 1 Oct 1924 (Wearn & Richards prove glomerular filtration and tubular reabsorption with a quartz micropipette)", "hold_s": 3.5}),
        ],
    ),
    (
        2,
        "Part 02 — 17 February 1842 & 1 October 1924: William Bowman's Microscopic Cup & Alfred Richards's Quartz Needle",
        [
            ("01_william_bowman_1842_london_and_wearn_richards_1924_philadelphia_quartz_micropuncture", 73.0, 6.5, "A", False, "80 KM OF KIDNEY TUBES", "Quality",
             "Quality: readable faces (25-year-old English surgeon William Bowman at King's College Hospital in London on 17 February 1842 examining dye-injected renal glomeruli nested inside Bowman's capsules, dissolving to Carl Ludwig in Marburg in 1844 and Joseph Wearn with Alfred Newton Richards in Philadelphia on 1 October 1924 guiding a 10-micrometre quartz micropipette into a living frog kidney).",
             STYLE + "Split period scene: on the left in February 1842 London, young surgeon William Bowman sketches a dye-injected glomerular tuft nested inside its capsule beside a brass microscope; on the right in October 1924 Philadelphia, Joseph Wearn and Alfred Richards withdraw glomerular fluid with a quartz micropipette." + QUAL_TAIL,
             {"kind": "FACT", "label": "80 km of kidney tubes", "when_stamp": "1666 · 17 February 1842 · 1844 · 1874 · 1 October 1924", "timeline_step": "1/3 · 17 Feb 1842 & 1 Oct 1924 (Bowman's glomerular capsule; Ludwig's ultrafiltration; Wearn & Richards's micropuncture proof)", "hold_s": 3.8}),
            ("02_bowman_1842_capsule_and_wearn_richards_1924_nephron_micropuncture_reabsorption_chart", 79.5, 8.0, "E", False, "17 FEB 1842 BOWMAN (PHIL. TRANS.) GLOMERULAR CAPSULE & 1 OCT 1924 WEARN & RICHARDS (AM. J. PHYSIOL.) PROXIMAL TUBULE REABSORPTION", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked Bowman (17 February 1842 Phil. Trans. R. Soc. 132: 57–80) glomerular capsule diagram & Wearn & Richards (1 October 1924 Am. J. Physiol. 71: 209–227) micropuncture reabsorption profile along the nephron (showing 100% glucose reabsorption in the proximal tubule and 99% water/NaCl reabsorption) proves mechanical filtration followed by selective tubular reclamation.",
             {"kind": "DATA", "label": "1842 BOWMAN CAPSULE & 1924 WEARN-RICHARDS MICROPUNCTURE PROFILE (100% GLUCOSE & 99% WATER REABSORBED ACROSS 80 KM OF TUBULES)", "detail": "Inked Bowman (17 February 1842 Phil. Trans. R. Soc. 132: 57–80) glomerular capsule diagram & Wearn & Richards (1 October 1924 Am. J. Physiol. 71: 209–227) micropuncture reabsorption profile along the nephron (showing 100% glucose reabsorption in the proximal tubule and 99% water/NaCl reabsorption) on period paper", "scale": "your two fist-sized kidneys pack two million microscopic filter cups connected to eighty kilometres of hair-thin tubing — enough microscopic plumbing coiled inside your lower back to stretch from London to Brighton", "hold_s": 3.8}),
            ("03_philadelphia_1924_brass_micromanipulator_and_10um_quartz_needle_closeup", 87.5, 6.5, "B", False, "1 OCTOBER 1924 — GLOMERULAR ULTRAFILTRATION PROVED", "Fast",
             "Fast: daylight macro shot of a 1924 brass micromanipulator holding a sharpened 10-micrometre quartz capillary needle above an illuminated glass specimen stage beside micro-Benedict glucose test tubes on a bench. Nothing emissive, no face.",
             STYLE + "In crisp daylight on a 1924 Philadelphia bench, a precision brass micromanipulator holds a fine quartz capillary needle above a glass stage beside a rack of micro-assay capillary tubes." + FAST_TAIL,
             None),
            ("04_cutaway_bowman_capsule_and_proximal_tubule_model_on_oak_table_pan", 94.0, 5.5, "C", False, "ULTRAFILTRATION & TUBULAR REABSORPTION", "Fast",
             "Fast: daylight close-up pan across a sculpted anatomical model of Bowman's capsule cradling the glomerular capillary tuft and leading into the coiled proximal convoluted tubule on an oak table. Nothing emissive, no face.",
             STYLE + "In bright window light on an oak table, a sculpted anatomical model shows a crimson glomerular capillary knot nestled inside a hollow ivory cup that winds into a coiled tubule." + FAST_TAIL,
             None),
        ],
    ),
    (
        3,
        "Part 03 — 1934–1953: Homer Smith's 180-Litre Shock & Why Fish Evolution Built Your Kidney Backwards — Midpoint Twist",
        [
            ("01_homer_smith_james_shannon_1934_nyu_inulin_and_werner_kuhn_1951_loop_of_henle", 99.5, 6.5, "A", False, "36X YOUR BLOOD FILTERED DAILY", "Quality",
             "Quality: readable faces (American renal physiologist Homer W. Smith and James A. Shannon at NYU in 1934–July 1935 measuring 125 mL/min = 180 L/day human GFR with Jerusalem artichoke inulin, dissolving to Friedrich Henle's 1862 and Swiss chemist Werner Kuhn's 1951 hairpin Loop of Henle countercurrent osmotic multiplier).",
             STYLE + "Split period scene: on the left in 1934 New York, Homer Smith and James Shannon hold flasks of purified Jerusalem artichoke inulin beside a 180-litre volumetric chart; on the right in 1951 Basel, Werner Kuhn points to a hairpin Loop of Henle countercurrent model." + QUAL_TAIL,
             {"kind": "FACT", "label": "36x your blood filtered daily", "who_card": "James A. Shannon (1904–1994) — American renal physiologist · Friedrich Gustav Jakob Henle (1809–1885) — German anatomist · Werner Kuhn (1899–1963) — Swiss physical chemist", "when_stamp": "1862 · 1934 · July 1935 · 1951 · 1953", "timeline_step": "2/3 · 1934–1935 & 1951 (Homer Smith & James Shannon measure 180 L/day GFR with inulin; Werner Kuhn solves the Loop of Henle countercurrent multiplier)", "hold_s": 3.8}),
            ("02_smith_shannon_1935_jci_inulin_gfr_and_kuhn_1951_loop_of_henle_countercurrent_chart", 106.0, 8.0, "E", False, "JULY 1935 SHANNON & SMITH (J. CLIN. INVEST.: INULIN GFR = 125 ML/MIN = 180 L/DAY) & 1951 KUHN LOOP OF HENLE (300 → 1,200 MOSM/L)", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked Homer Smith & James Shannon (July 1935 J. Clin. Invest. 14: 393–401) human inulin clearance chart (GFR = 125 mL/min = 180 L/day) alongside Werner Kuhn (1951 Z. Elektrochem. 55: 539–558) Loop of Henle countercurrent osmotic gradient diagram (300 to 1,200 mOsm/L medullary gradient rescuing 99% of filtered water).",
             {"kind": "DATA", "label": "1935 SMITH/SHANNON INULIN GFR (125 ML/MIN = 180 L/DAY) & 1951 KUHN LOOP OF HENLE GRADIENT (300 → 1,200 MOSM/L)", "detail": "Inked Homer Smith & James Shannon (July 1935 J. Clin. Invest. 14: 393–401) human inulin clearance chart (GFR = 125 mL/min = 180 L/day) alongside Werner Kuhn (1951) Loop of Henle countercurrent osmotic gradient diagram (300 to 1,200 mOsm/L medullary gradient rescuing 99% of filtered water) on period paper", "scale": "because our ancient fish ancestors needed a giant bilge pump to bail out river water, your kidneys still dump a 180-litre bathtub of fluid every day — and use the hairpin Loop of Henle like a salt sponge to wring 99% of that bathtub back into your veins", "hold_s": 3.8}),
            ("03_nyu_1934_jerusalem_artichoke_tubers_inulin_jar_and_clearance_flasks_closeup", 114.0, 6.5, "B", False, "1934 — INULIN GLOMERULAR FILTRATION RATE", "Fast",
             "Fast: daylight macro shot of Jerusalem artichoke tubers beside a stoppered bottle of white inulin powder, volumetric flasks, and a 1935 Journal of Clinical Investigation offprint on a bench. Nothing emissive, no face.",
             STYLE + "In crisp daylight on a 1934 New York physiology bench, knobby Jerusalem artichoke roots and a glass jar of white purified inulin powder sit beside graduated glass cylinders and an open journal." + FAST_TAIL,
             None),
            ("04_hairpin_loop_of_henle_countercurrent_multiplier_model_on_oak_table_pan", 120.5, 5.5, "C", False, "1934 & 1951 — 180 L/DAY GFR & COUNTERCURRENT MULTIPLIER", "Fast",
             "Fast: daylight close-up pan across a sculpted hairpin Loop of Henle model showing the descending and ascending limbs diving into a graduated salt-gradient block alongside the collecting duct on an oak table. Nothing emissive, no face.",
             STYLE + "In bright window light on an oak table, a sculpted hairpin Loop of Henle model dives through a four-tier medullary block with brass salt-transfer arrows and a parallel collecting duct." + FAST_TAIL,
             None),
        ],
    ),
    (
        4,
        "Part 04 — 17 March 1943 – 11 September 1945: Willem Kolff's Sausage-Casing Artificial Kidney in Nazi-Occupied Holland",
        [
            ("01_willem_kolff_11_sep_1945_kampen_rotating_sausage_casing_drum_and_sofia_schafstadt", 126.0, 6.5, "A", False, "BUILT FROM SAUSAGE SKIN", "Quality",
             "Quality: readable faces (Dutch physician Willem Johan Kolff in Kampen Municipal Hospital on 11 September 1945 operating his rotating wooden-slat drum wrapped in 40 metres of cellophane sausage casing in a 100-litre porcelain enamel bath driven by a sewing-machine motor, saving 67-year-old Patient #16 Sofia Maria Schafstadt from a uremic coma).",
             STYLE + "In a 1945 Kampen hospital room, Dutch physician Willem Kolff monitors his rotating slatted wooden drum wound with forty metres of cellophane sausage tubing in an enamel bath as elderly patient Sofia Schafstadt wakes in her hospital bed." + QUAL_TAIL,
             {"kind": "FACT", "label": "Built from sausage skin", "who_card": "Thomas Graham (1805–1869) — Scottish physical chemist · Sofia Maria Schafstadt (1878–1952) — First surviving hemodialysis patient", "when_stamp": "1861 · October 1938 · 17 March 1943 · 1944 · 11 September 1945 · 1960", "timeline_step": "3/3 · 17 Mar 1943 – 11 Sep 1945 (Willem Kolff builds the rotating-drum cellophane sausage-casing artificial kidney in Kampen and saves Sofia Schafstadt)", "hold_s": 3.8}),
            ("02_kolff_1944_acta_med_scand_and_11_sep_1945_kampen_dialysis_urea_clearance_chart", 132.5, 8.0, "E", False, "1944 KOLFF (ACTA MED. SCAND.) & 11 SEP 1945 KAMPEN: 40 M CELLOPHANE SAUSAGE CASING (1.5 M2) CLEARS 60 G UREA IN 11.5 HOURS", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked Willem Kolff (1944 Acta Med. Scand. 117: 121–134 & 11 September 1945 Sofia Schafstadt Kampen chart) rotating-drum cellophane dialyser schematic & blood urea clearance curve (40 metres of cellophane sausage tubing with ~1.5 m2 surface area in a 100-litre saline bath clearing 60 grams of urea over 11.5 hours and dropping blood urea nitrogen from coma levels to recovery).",
             {"kind": "DATA", "label": "11 SEP 1945 KOLFF ROTATING-DRUM DIALYSER (40 M CELLOPHANE SAUSAGE TUBING) CLEARING 60 G UREA OVER 11.5 HOURS", "detail": "Inked Willem Kolff (1944 Acta Med. Scand. 117: 121–134 & 11 September 1945 Sofia Schafstadt Kampen chart) rotating-drum cellophane dialyser schematic & blood urea clearance curve (40 metres of cellophane sausage tubing with ~1.5 m2 surface area in a 100-litre saline bath clearing 60 grams of urea over 11.5 hours and dropping blood urea nitrogen from coma levels to recovery) on period paper", "scale": "Willem Kolff replaced two million microscopic Bowman's capsules with forty metres of butcher's sausage skin wrapped round a wooden drum — using tiny pores in cellulose that let small urea poison molecules slip out into salt water while holding every red blood cell inside", "hold_s": 3.8}),
            ("03_kampen_1945_wooden_slat_drum_cellophane_tubing_and_enamel_bath_closeup", 140.5, 6.5, "B", False, "11 SEPTEMBER 1945 — FIRST LIFE SAVED BY DIALYSIS", "Fast",
             "Fast: daylight macro shot of Kolff's horizontal wooden-slat drum wound with transparent cellophane sausage casing sitting in a white porcelain enamel bath beside a Ford water-pump coupling on a hospital cart. Nothing emissive, no face.",
             STYLE + "In crisp daylight in a 1945 Dutch hospital room, a horizontal slatted wooden drum wound with ribbons of cellophane tubing sits in a white enamel tub." + FAST_TAIL,
             None),
            ("04_explorer_turning_kolff_wooden_drum_as_urea_motes_exit_sausage_pores_and_red_marbles_stay_inside", 147.0, 5.5, "B", True, None, "Quality",
             "Quality: Explorer beat 2 (locked character reference).",
             STYLE + "Standing beside Kolff's rotating wooden-slat drum in its porcelain bath, the Explorer turns the drum handle as crimson blood marbles and tiny grey urea motes spiral through the transparent sausage casing; the grey motes drift out through microscopic pores into the bathwater while every crimson marble rolls safely back through the return tube." + EXP_TAIL,
             None),
        ],
    ),
    (
        5,
        "Part 05 — From Kampen to Modern Dialysis & Transplants — & How Giant Trees Pull Water 100 Metres High Without a Pump",
        [
            ("01_timeline_1842_1960_and_modern_dialysis_transplant_chart", 152.5, 8.5, "E", False, "1842–1960 TIMELINE · BOWMAN CAPSULE, LUDWIG, WEARN-RICHARDS MICROPUNCTURE, SMITH 180 L/DAY GFR, KOLFF DIALYSIS & MURRAY TRANSPLANT", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, the 3-era timeline completes: 17 Feb 1842 & 1844 (William Bowman maps Bowman's capsule at King's College London; Carl Ludwig proposes hydrostatic glomerular ultrafiltration) · 1 Oct 1924 & 1934 (Joseph Wearn & Alfred Newton Richards puncture a living frog glomerulus with a quartz micropipette to prove filtration and reabsorption; Homer Smith & James Shannon use inulin to measure human GFR at 125 mL/min = 180 L/day) · 17 Mar 1943 – 11 Sep 1945 (Willem Kolff builds the rotating-drum cellophane sausage-casing artificial kidney in Nazi-occupied Kampen and saves Patient #16 Sofia Schafstadt).",
             {"kind": "DATA", "label": "1842–1960 KIDNEY & DIALYSIS TIMELINE · BOWMAN, LUDWIG, WEARN-RICHARDS, HOMER SMITH, KOLFF & SCRIBNER", "detail": "Animated timeline (1842 → 1960) alongside an inked comparison of Bowman's nephron and Kolff's rotating-drum / modern hollow-fibre dialyser", "scale": "from a 25-year-old surgeon's microscope in London to a hair-thin quartz needle in Philadelphia and forty metres of sausage skin in wartime Holland, scientists unlocked the two-million-filter cleaning plant that keeps our blood pure", "when_stamp": "1842–1960 · 23 December 1954", "timeline_step": "3/3 · 1842–1960 timeline complete", "hold_s": 3.8}),
            ("02_modern_hollow_fibre_dialyser_cartridge_beside_kolff_wooden_drum_model_on_plinth_pan", 161.0, 5.5, "A", False, "DIALYSIS & KIDNEY TRANSPLANTS", "Fast",
             "Fast: daylight close-up of a modern transparent hollow-fibre dialyser cartridge containing ten thousand capillary fibres beside a miniature wooden-drum Kolff dialyser on a wooden museum plinth. Nothing emissive, no face.",
             STYLE + "In crisp daylight on a wooden museum plinth, a modern clear cylinder packed with thousands of white hollow dialysis fibres sits beside a miniature slatted wooden drum wrapped in cellophane." + FAST_TAIL,
             None),
            ("03_hales_1727_grapevine_gauge_strasburger_1891_poisoned_oak_dixon_joly_1894_and_scholander_1965_redwood_handoff", 166.5, 6.5, "C", False, "XYLEM, TRANSPIRATION & COHESION-TENSION", "Quality",
             "Quality: readable faces (Stephen Hales in Teddington in 1727 tying a mercury gauge to a grapevine, Eduard Strasburger in Bonn in 1891 with his 22-metre picric-acid poisoned oak tree, Henry Dixon and John Joly in Dublin on 15 November 1894, and Per Scholander in the California redwoods on 16 April 1965 with his rifle and pressure bomb — handoff to 073 Xylem, Transpiration & Cohesion-Tension).",
             STYLE + "Split period scene: on the left, Stephen Hales in 1727 and Henry Dixon with John Joly in 1894 Dublin study sap ascent beside Eduard Strasburger's 22-metre oak trunk; on the right in April 1965 California, Per Scholander aims a hunting rifle toward a giant redwood canopy beside a steel pressure bomb." + QUAL_TAIL,
             {"kind": "WHEN", "label": "1727 · 1891 · 15 NOVEMBER 1894 · 16 APRIL 1965", "hold_s": 3.5}),
            ("04_table_three_callback", 173.0, 2.4, "C", False, None, "reuse",
             "Reuse: verified unused moving window [5.50s..7.90s] of P1:07_table_three_props_1842_bowman_microscope_1924_quartz_micropipette_and_1945_kolff_sausage_spool (callback, £0).",
             "Reuse P1:07_table_three_props_1842_bowman_microscope_1924_quartz_micropipette_and_1945_kolff_sausage_spool [5.50s..7.90s] (2.40s distinct non-overlapping tail window from 8.00s source clip).",
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
                row["reuse_of"] = "P1:07_table_three_props_1842_bowman_microscope_1924_quartz_micropipette_and_1945_kolff_sausage_spool"
                row["reuse_window_s"] = [5.5, 7.9]
                row["reuse_audit"] = {
                    "source_row": "P1:07_table_three_props_1842_bowman_microscope_1924_quartz_micropipette_and_1945_kolff_sausage_spool",
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
            "film": "072_Bowman-Ludwig-Richards-Smith-Kolff-Kidneys-Dialysis",
            "part": p_idx,
            "title": p_title,
            "version": "v01",
            "timing_status": "pre_vo_script_clock (built from kidneys_script_master_v01.md; retimes onto Scribe STT once VO locks)",
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
        "film": "072_Bowman-Ludwig-Richards-Smith-Kolff-Kidneys-Dialysis",
        "version": "v01",
        "date": "2026-10-20",
        "owner": "gemini (J0706)",
        "status": "PRE_VO_BOARDS_V01_NO_MINT",
        "generation_authorized": False,
        "script": "00_Brand/Channel-Setup/ideas/072_Bowman-Ludwig-Richards-Smith-Kolff-Kidneys-Dialysis/kidneys_script_master_v01.md",
        "sources": "00_Brand/Channel-Setup/ideas/072_Bowman-Ludwig-Richards-Smith-Kolff-Kidneys-Dialysis/SOURCES_v01.md",
        "credit_snapshot": {
            "flow_balance": 23740,
            "flow_floor": 0,
            "flow_read_at": "2026-10-15T21:42:22Z",
            "vertex_promo_gbp": 71.02,
            "vertex_usable_gbp": 70.02,
        },
        "totals": totals,
        "per_part": per_part_summary,
        "mint_order": "006 > 007 > 008 > 009 > 010 > 011 > 012 > 013 > 014 > 015 > 016 > 017 > 018 > 019 > 020 > 021 > 022 > 023 > 024 > 025 > 026 > 027 > 028 > 029 > 030 > 031 > 032 > 033 > 034 > 035 > 036 > 037 > 038 > 039 > 040 > 041 > 042 > 043 > 044 > 045 > 046 > 047 > 048 > 049 > 050 > 051 > 052 > 053 > 054 > 055 > 056 > 057 > 058 > 059 > 060 > 061 > 062 > 063 > 064 > 065 > 066 > 067 > 068 > 069 > 070 > 071 > 072 > 073 > 074 > 075 > 076 > 077. Nothing in 072 is generation_authorized.",
    }
    (EDIT / "PICTURE_PLAN_v01.json").write_text(json.dumps(plan, indent=2) + "\n")

    sl = [
        "# 072 The Kidney: How Sausage Skin Saved Millions — Shot list & plate boards v01 (pre-VO)",
        "",
        "Gemini, 20 Oct 2026, J0706. Built from `kidneys_script_master_v01.md` (`91.5/100 PASS`) and `SOURCES_v01.md`.",
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
        "# 072 price review v01 (pre-VO plate boards)",
        "",
        "Gemini, 20 Oct 2026, J0706. Boards only. **No mint. No spend. No merge.**",
        "Prepared from `kidneys_script_master_v01.md` (`91.5/100 PASS`) and `SOURCES_v01.md` so 072's full plate board rows, non-emissive Fast prompts, £0 code graphics, and Teach-on-Screen overlays are ready to re-time the moment long VO locks. Parked for Chief.",
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
        f"- **Quality ({totals['Quality']} rows):** readable faces (William Bowman, Carl Ludwig, Joseph T. Wearn, Alfred Newton Richards, Homer W. Smith, James A. Shannon, Friedrich Henle, Werner Kuhn, Willem Johan Kolff, Thomas Graham, Sofia Maria Schafstadt, Stephen Hales, Eduard Strasburger, Henry Horatio Dixon, John Joly, Per Fredrik Scholander), 17 February 1842 London Bowman's capsule & 1 October 1924 Philadelphia quartz micropipette glomerular puncture, 1934–1935 NYU `180 L/day` inulin GFR & 1951 Basel `Loop of Henle` countercurrent multiplier, 11 September 1945 Kampen rotating sausage-casing artificial kidney saving Patient #16 Sofia Schafstadt, and the 2 Explorer beats.",
        f"- **Fast ({totals['Fast']} rows, non-emissive):** daylight prop and laboratory shots (1842 Bowman glomerular plate, brass micromanipulator with quartz micropipette & 1924 *Am. J. Physiol.* offprint pan, 3-object callback bench, 1924 brass micromanipulator & micro-Benedict assay tubes, sculpted Bowman's capsule & proximal tubule model, Jerusalem artichoke tubers with purified inulin jar & volumetric flasks, sculpted hairpin Loop of Henle countercurrent block, 1945 slatted wooden drum with cellophane sausage tubing in enamel bath, modern hollow-fibre dialyser cartridge beside miniature wooden-drum model on museum plinth). Zero candles, flames, sparks, or glowing elements on Fast.",
        f"- **£0 code graphics ({totals['code_graphic']} rows):**",
        "  1. `P1:04_bowman_1842_richards_1924_smith_1935_and_kolff_1944_nephron_filtration_dialysis_chart` — `125 mL/min` (`180 L/day`) GFR across `~2 million` nephrons, `100%` glucose and `~99%` water reabsorption, and `1.5 L/day` urine (`SCALE: your kidneys clean your house by throwing every single piece of furniture out the window thirty-six times a day — and then running downstairs to carry ninety-nine percent of the furniture back inside while leaving the rubbish on the pavement`)",
        "  2. `P1:06_wearn_richards_1_oct_1924_ajp_quartz_micropipette_glomerular_puncture_chart` — Joseph Wearn & Alfred Richards (1 October 1924 *Am. J. Physiol.*) frog glomerular filtrate vs bladder urine chemical table (`SCALE: puncturing a single Bowman's capsule with a quartz needle ten micrometres wide is like threading a needle thinner than a human hair into a water balloon the size of a grain of sand without popping the blood vessels inside`)",
        "  3. `P2:02_bowman_1842_capsule_and_wearn_richards_1924_nephron_micropuncture_reabsorption_chart` — William Bowman (17 February 1842 *Phil. Trans.*) glomerular capsule & Wearn/Richards (1924) proximal tubular reabsorption profile (`SCALE: your two fist-sized kidneys pack two million microscopic filter cups connected to eighty kilometres of hair-thin tubing — enough microscopic plumbing coiled inside your lower back to stretch from London to Brighton`)",
        "  4. `P3:02_smith_shannon_1935_jci_inulin_gfr_and_kuhn_1951_loop_of_henle_countercurrent_chart` — Homer Smith & James Shannon (July 1935 *J. Clin. Invest.*) human inulin clearance (`125 mL/min` = `180 L/day`) & Werner Kuhn (1951) `Loop of Henle` `300 → 1,200 mOsm/L` countercurrent multiplier (`SCALE: because our ancient fish ancestors needed a giant bilge pump to bail out river water, your kidneys still dump a 180-litre bathtub of fluid every day — and use the hairpin Loop of Henle like a salt sponge to wring 99% of that bathtub back into your veins`)",
        "  5. `P4:02_kolff_1944_acta_med_scand_and_11_sep_1945_kampen_dialysis_urea_clearance_chart` — Willem Kolff (1944 *Acta Med. Scand.* & 11 September 1945 Kampen chart) `40 m` cellophane sausage-casing rotating drum clearing `60 g` urea in `11.5 hours` (`SCALE: Willem Kolff replaced two million microscopic Bowman's capsules with forty metres of butcher's sausage skin wrapped round a wooden drum — using tiny pores in cellulose that let small urea poison molecules slip out into salt water while holding every red blood cell inside`)",
        "  6. `P5:01_timeline_1842_1960_and_modern_dialysis_transplant_chart` — completed timeline (1842 → 1960) + hollow-fibre hemodialysis & kidney transplantation (`SCALE: from a 25-year-old surgeon's microscope in London to a hair-thin quartz needle in Philadelphia and forty metres of sausage skin in wartime Holland, scientists unlocked the two-million-filter cleaning plant that keeps our blood pure`)",
        f"- **£0 verified reuse ({totals['reuse']} row):** `P5:04_table_three_callback` uses the 2.40 s unused moving tail `[5.50s..7.90s]` of `P1:07_table_three_props_1842_bowman_microscope_1924_quartz_micropipette_and_1945_kolff_sausage_spool`.",
        "",
        "## Mint order",
        "",
        "006 > 007 > 008 > 009 > 010 > 011 > 012 > 013 > 014 > 015 > 016 > 017 > 018 > 019 > 020 > 021 > 022 > 023 > 024 > 025 > 026 > 027 > 028 > 029 > 030 > 031 > 032 > 033 > 034 > 035 > 036 > 037 > 038 > 039 > 040 > 041 > 042 > 043 > 044 > 045 > 046 > 047 > 048 > 049 > 050 > 051 > 052 > 053 > 054 > 055 > 056 > 057 > 058 > 059 > 060 > 061 > 062 > 063 > 064 > 065 > 066 > 067 > 068 > 069 > 070 > 071 > 072 > 073 > 074 > 075 > 076 > 077. `generation_authorized` is `false` on every row.",
    ])
    (EDIT / "PRICE_REVIEW_v01.md").write_text("\n".join(pr_lines) + "\n")
    print(f"072 v01 boards written: {totals['rows']} rows, Flow expected={totals['flow_credits_expected']}")


if __name__ == "__main__":
    main()
