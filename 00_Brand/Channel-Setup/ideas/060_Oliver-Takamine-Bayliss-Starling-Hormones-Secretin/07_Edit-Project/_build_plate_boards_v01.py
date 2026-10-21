#!/usr/bin/env python3
"""HOS 060 (Hormones: The Secret Messages in Your Blood) pre-VO plate boards v01. J0631. No mint, no spend.

Built from 00_Brand/Channel-Setup/ideas/060_Oliver-Takamine-Bayliss-Starling-Hormones-Secretin/hormones_script_master_v01.md
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
        "Part 01 — The Afternoon Experiment That Overturned Ivan Pavlov",
        [
            ("01_bayliss_starling_16_jan_1902_ucl_severed_nerves_secretin_blood_messenger_and_pancreas", 0.0, 5.5, "A", False, "WIRELESS BLOOD MESSAGES", "Quality",
             "Quality: Short frame 0 / answer image (0:03) + inside a physiology laboratory at University College London on 16 January 1902, William Bayliss and Ernest Starling sever every electrical nerve wire connected to a loop of small intestine, drip dilute hydrochloric acid inside, and watch golden chemical messenger molecules (secretin) enter the red bloodstream and trigger the pancreas to gush clear digestive juice.",
             STYLE + "Split laboratory-and-anatomical scene: on the left at University College London on 16 January 1902, William Bayliss and Ernest Starling snip the white nerve fibres around an intestinal loop and drip dilute acid from a glass pipette; on the right, golden secretin messenger spheres ride the red bloodstream into the pancreas, which pours clear droplets into a glass recording funnel." + QUAL_TAIL,
             {"kind": "WHEN", "label": "LONDON, 16 JANUARY 1902", "timeline_step": "2/4 · 16 Jan 1902 (William Bayliss & Ernest Starling sever every nerve to a jejunal loop at UCL and prove acid releases the blood-borne chemical messenger secretin)", "hold_s": 3.5}),
            ("02_oliver_schafer_1894_ucl_takamine_uenaka_1900_ny_and_bayliss_starling_1902_1905_split", 5.5, 6.0, "B", False, "ADRENALINE, SECRETIN, HORMONES", "Quality",
             "Quality: complex three-part composition (George Oliver and Edward Schäfer at UCL in March 1894 watching a mercury blood-pressure gauge shoot skyward from adrenal extract; Jokichi Takamine and Keizo Uenaka in New York in July–November 1900 crystallising pure adrenaline needles; and William Bayliss and Ernest Starling at UCL on 16 January 1902 discovering secretin and coining 'hormone' in June 1905).",
             STYLE + "Three-panel period composition: on the left, George Oliver and Edward Schäfer in 1894 London watching a mercury manometer column surge upward; in the centre, Jokichi Takamine and Keizo Uenaka in 1900 New York inspecting sparkling white adrenaline crystals in a glass dish; on the right, William Bayliss and Ernest Starling in 1902 London beside a smoked kymograph drum." + QUAL_TAIL,
             None),
            ("03_adrenal_glands_releasing_adrenaline_burst_into_bloodstream_to_heart_lungs_and_pupils", 11.5, 6.0, "C", False, "CHEMICAL ALARM IN YOUR BLOOD", "Quality",
             "Quality: complex anatomical and physiological reveal (a sudden fright causes the tiny triangular adrenal glands atop the kidneys to release a burst of adrenaline molecules into the bloodstream, racing to the heart, lungs, and pupils in seconds).",
             STYLE + "Split anatomical-and-street scene: on the left, a startled pedestrian steps back from a rushing motor car as his pupils widen; on the right, inside the torso, the triangular adrenal glands atop the kidneys release golden chemical crystals into the bloodstream that race up to the beating heart and lungs." + QUAL_TAIL,
             {"kind": "WHEN", "label": "MARCH 1894 · 1900–1901 · 16 JANUARY 1902 · 20 JUNE 1905", "timeline_step": "1/4 · Mar 1894 & 1901 (Oliver & Schäfer; Takamine & Uenaka) · 2/4 · 16 Jan 1902 (Bayliss & Starling) · 3/4 · 20 Jun 1905 (Starling coins 'hormone')", "hold_s": 3.5}),
            ("04_oliver_schafer_1894_takamine_1901_bayliss_starling_1902_nerve_vs_hormone_1ppb_chart", 17.5, 8.0, "E", False, "WIRED NERVES (MILLISECONDS) VS WIRELESS BLOOD HORMONES (ADRENALINE, SECRETIN, INSULIN, THYROXINE ACTIVE AT ~1 PART PER BILLION)", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked endocrine vs nervous communication & hormone potency chart from Oliver & Schäfer (March 1894 J. Physiol. 16: i–iv), Takamine (1901 Am. J. Pharm. 73: 523–531), and Bayliss & Starling (1902 J. Physiol. 28: 325–353; Starling June 1905 Lancet) compares fast electrical nerve impulses (~1–100 m/s along wired axons) with blood-borne chemical hormones (adrenaline, secretin, insulin, thyroxine) travelling via the circulation to target receptors at concentrations of 1 part per million to 1 part per billion.",
             {"kind": "DATA", "label": "ELECTRICAL NERVE WIRES (MS) VS BLOOD-BORNE HORMONES (ACTIVE AT ~1 PART PER BILLION across 5 L OF BLOOD)", "detail": "Inked comparison chart on period paper showing electrical nerve reflexes (wired point-to-point in milliseconds) vs blood-borne endocrine hormones (wireless broadcast through 5 litres of blood in seconds to minutes, active at picomolar-to-nanomolar concentrations, ~1 part per billion)", "scale": "a single hormone in your blood is so potent that it works at one part per billion — like dissolving a single pinch of salt inside an Olympic swimming pool and having every cell in the pool taste it", "who_card": "George Oliver (1841–1915) — British physician · Edward Sharpey-Schäfer (1850–1935) — British physiologist · Jokichi Takamine (1854–1922) — Japanese chemist · Keizo Uenaka (1876–1960) — Japanese chemist · William M. Bayliss (1860–1924) — British physiologist · Ernest H. Starling (1866–1927) — British physiologist", "when_stamp": "March 1894 · 1900–1901 · 16 January 1902 · 20 June 1905", "hold_s": 3.8}),
            ("05_porcelain_mortar_pestle_hcl_dropper_bottle_and_mercury_manometer_pan", 25.5, 5.5, "A", False, "1 PART PER BILLION IN BLOOD", "Fast",
             "Fast: daylight macro pan across a porcelain mortar and pestle with fine sand, a glass dropper bottle of dilute hydrochloric acid, and a brass-and-glass mercury U-tube manometer on an oak bench between code graphics so two full-frame graphics never run back to back. Nothing emissive, no face.",
             STYLE + "In crisp daylight on an oak physiology bench, the camera pans smoothly across a white porcelain mortar and pestle holding fine sand, a stoppered glass reagent bottle, and a vertical glass U-tube mercury manometer." + FAST_TAIL,
             None),
            ("06_bayliss_starling_16_jan_1902_denervated_jejunum_loop_and_120s_pancreatic_flow_chart", 31.0, 8.0, "E", False, "16 JANUARY 1902: SECRETIN", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period parchment, an inked Bayliss & Starling 16 January 1902 denervated jejunum loop & pancreatic secretion rate chart (from Bayliss & Starling 1902, J. Physiol. 28: 325–353) shows zero secretion at baseline, followed by a sharp surge of pancreatic flow ~2 minutes (120 seconds) after either instilling 0.4% HCl into the completely denervated intestinal loop or injecting acid-extracted intestinal mucosa (secretin) into the jugular vein.",
             {"kind": "DATA", "label": "16 JAN 1902 BAYLISS & STARLING: DENERVATED JEJUNUM LOOP + 0.4% HCL → SECRETIN IN BLOOD → PANCREAS SURGE IN ~120 SECONDS", "detail": "Inked pancreatic secretion rate chart (drops per minute vs time) from Bayliss & Starling (1902, J. Physiol. 28: 325–353) showing zero secretion at baseline, followed by a sharp surge of pancreatic flow ~2 minutes after either instilling acid into the denervated intestinal loop or injecting acid-extracted intestinal mucosa (secretin) into the jugular vein", "scale": "even with every nerve wire severed by a scalpel, it took just one hundred and twenty seconds for a chemical letter posted in the gut to ride the bloodstream and unlock the pancreas", "hold_s": 3.8}),
            ("07_table_three_props_oliver_1894_vial_takamine_1900_crystals_and_starling_1902_mortar_kymograph", 39.0, 5.5, "C", False, "1894 TO 1977", "Fast",
             "Fast: daylight prop table (callback source for Part 05: George Oliver's 1894 glass adrenal extract vial, Jokichi Takamine's 1900 dish of adrenaline needle crystals, and Ernest Starling's 1902 porcelain mortar beside a brass kymograph drum). Nothing emissive.",
             STYLE + "On an oak workbench in soft window light sit three objects side by side: a small amber glass apothecary vial, a watch glass of white needle crystals, and a porcelain mortar and pestle beside a brass recording drum." + FAST_TAIL,
             None),
            ("08_explorer_dropping_wax_sealed_secretin_envelope_into_bloodstream_past_cut_telegraph_wires", 62.0, 5.5, "A", True, None, "Quality",
             "Quality: Explorer beat 1 (locked character reference, after 1:00).",
             STYLE + "Standing beside a wooden telegraph pole whose copper wires have been snipped in two, the Explorer drops a wax-sealed parchment envelope into a red river channel, where it floats downstream and springs open a brass padlock on a pancreatic sluice gate." + EXP_TAIL,
             None),
            ("09_starling_and_bayliss_16_jan_1902_ucl_grinding_mucosa_in_mortar_beside_ticking_kymograph", 67.5, 5.5, "B", False, "UCL, 16 JANUARY 1902", "Quality",
             "Quality: readable faces (at University College London on the afternoon of 16 January 1902, Ernest Starling grinds intestinal lining with sand and weak acid in a porcelain mortar while William Bayliss watches the recording drum tick off drops of pancreatic juice).",
             STYLE + "In a 1902 University College London physiology lab, Ernest Starling grinds tissue in a white porcelain mortar with sand and dilute acid while William Bayliss points delightedly at a smoked kymograph drum ticking off rapid droplets." + QUAL_TAIL,
             {"kind": "WHEN", "label": "UCL, 16 JANUARY 1902", "timeline_step": "2/4 · 16 Jan 1902 (Bayliss & Starling discover secretin at University College London)", "hold_s": 3.5}),
        ],
    ),
    (
        2,
        "Part 02 — March 1894 – 1901: George Oliver, Edward Schäfer & Jokichi Takamine Crystallise Adrenaline",
        [
            ("01_addison_1855_oliver_schafer_mar_1894_ucl_and_takamine_uenaka_1900_1901_adrenaline_crystals", 73.0, 6.5, "A", False, "FIRST PURE HORMONE: ADRENALINE (1901)", "Quality",
             "Quality: readable faces (English physician Thomas Addison in 1855 examining the adrenal glands atop the kidneys, dissolving to George Oliver and Edward Sharpey-Schäfer at UCL in March 1894 watching a mercury blood-pressure manometer shoot skyward, and Japanese chemists Jokichi Takamine and Keizo Uenaka in New York on 21 July 1900 – 1901 crystallising pure adrenaline).",
             STYLE + "Split period scene: on the left in March 1894 London, George Oliver and Edward Schäfer stare in astonishment as the mercury float in a tall glass manometer shoots to the top of the tube; on the right in July 1900 New York, Jokichi Takamine and young Keizo Uenaka hold up a test tube of sparkling white adrenaline crystals." + QUAL_TAIL,
             {"kind": "FACT", "label": "First pure hormone: adrenaline (1901)", "who_card": "Thomas Addison (1793–1860) — English physician · John Jacob Abel (1857–1938) — American pharmacologist", "when_stamp": "1855 · March 1894 · 21 July 1900 · 1901", "timeline_step": "1/4 · Mar 1894 & 1901 (Oliver & Schäfer discover adrenal blood-pressure surge; Takamine & Uenaka crystallise pure adrenaline)", "hold_s": 3.8}),
            ("02_oliver_schafer_1894_kymograph_blood_pressure_surge_and_takamine_1901_adrenaline_c9h13no3_chart", 79.5, 8.0, "E", False, "MAR 1894 OLIVER & SCHÄFER (BP SURGE ~100 → >240 MMHG) & 1901 TAKAMINE & UENAKA CRYSTALLINE ADRENALINE (C9H13NO3)", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked Oliver & Schäfer (March 1894, J. Physiol. 16: i–iv & 1895 J. Physiol. 18: 230–276) arterial blood-pressure kymograph tracing & Takamine (1901) crystalline adrenaline (C9H13NO3) potency chart shows intravenous suprarenal extract driving arterial pressure from ~100 mmHg to >240 mmHg within seconds via arteriolar vasoconstriction.",
             {"kind": "DATA", "label": "MAR 1894 OLIVER & SCHÄFER (ARTERIAL BP ~100 → >240 MMHG) & 1901 TAKAMINE PURE CRYSTALLINE ADRENALINE (C9H13NO3)", "detail": "Inked Oliver & Schäfer (March 1894, J. Physiol. 16: i–iv & 1895 J. Physiol. 18: 230–276) arterial blood-pressure kymograph tracing & Takamine (1901) crystalline adrenaline (C9H13NO3) potency chart on period paper showing intravenous suprarenal extract driving arterial pressure from ~100 mmHg to >240 mmHg within seconds via arteriolar vasoconstriction", "scale": "Takamine's adrenaline crystals were so powerful that injecting a single millionth of a gram — a speck far too small for the human eye to see — made blood pressure surge inside seconds", "hold_s": 3.8}),
            ("03_new_york_1900_watch_glass_adrenaline_rosette_crystals_and_microscope_closeup", 87.5, 6.5, "B", False, "1901 — CRYSTALLISING PURE ADRENALINE", "Fast",
             "Fast: daylight macro shot of a glass watch dish containing crystalline white rosette clusters beside a brass monocular microscope and a leather laboratory notebook on a 1900 New York bench. Nothing emissive, no face.",
             STYLE + "In crisp daylight on a 1900 New York chemistry bench, a glass watch dish of fine white needle-crystal rosettes sits beside a brass microscope and an open laboratory ledger." + FAST_TAIL,
             None),
            ("04_ucl_1894_mercury_manometer_column_and_radial_artery_spring_gauge_pan", 94.0, 5.5, "C", False, "MARCH 1894 — THE MERCURY SURGE", "Fast",
             "Fast: daylight close-up pan across a brass-and-glass mercury blood-pressure manometer column, a glass syringe, and George Oliver's wrist pulse spring gauge on an oak table. Nothing emissive, no face.",
             STYLE + "In bright window light on an 1894 London laboratory table, a tall glass mercury manometer column sits beside a brass wrist arteriometer dial and a small glass vial." + FAST_TAIL,
             None),
        ],
    ),
    (
        3,
        "Part 03 — 16 January 1902: William Bayliss & Ernest Starling Cut Every Nerve and Discover Secretin — Midpoint Twist",
        [
            ("01_pavlov_st_petersburg_nervism_vs_bayliss_starling_16_jan_1902_ucl_denervated_gut_secretin", 99.5, 6.5, "A", False, "CUT EVERY NERVE; GUT STILL TALKED", "Quality",
             "Quality: readable faces (Russian physiologist Ivan Pavlov in St. Petersburg diagramming vagus nerve reflexes, dissolving to British brothers-in-law William Bayliss and Ernest Starling at UCL on Thursday afternoon, 16 January 1902 severing every nerve to an isolated loop of intestine and watching the pancreas still gush juice two minutes after acid touches the gut).",
             STYLE + "Split period scene: on the left in St. Petersburg, bearded Ivan Pavlov points to a chalkboard diagram of brain-to-gut nerve wires; on the right on 16 January 1902 in London, William Bayliss and Ernest Starling watch pancreatic droplets fall rapidly into a funnel after every nerve to the gut loop has been cut." + QUAL_TAIL,
             {"kind": "FACT", "label": "Cut every nerve; gut still talked", "who_card": "Ivan P. Pavlov (1849–1936) — Russian physiologist", "when_stamp": "16 January 1902", "timeline_step": "2/4 · 16 Jan 1902 (Bayliss & Starling sever all nerves to an intestinal loop and discover the chemical messenger secretin)", "hold_s": 3.8}),
            ("02_bayliss_starling_1902_four_step_secretin_proof_and_pavlov_replication_chart", 106.0, 8.0, "E", False, "16 JAN 1902 BAYLISS & STARLING 4-STEP PROOF: (1) INTACT + ACID → FLOW, (2) NERVES CUT + ACID → FLOW, (3) ACID IN VEIN → 0, (4) MUCOSA EXTRACT (SECRETIN) IN VEIN → MASSIVE FLOW", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked Bayliss & Starling (1902, Proc. R. Soc. Lond. 69: 352–353 & J. Physiol. 28: 325–353) four-step experimental proof chart compares (1) acid in intact duodenum -> secretion, (2) acid in completely denervated jejunum loop -> full secretion after ~2 min, (3) acid injected directly into blood vein -> 0 secretion, and (4) acid-ground jejunal mucosa extract (secretin) injected into vein -> massive pancreatic secretion.",
             {"kind": "DATA", "label": "16 JAN 1902 4-STEP PROOF: NERVES CUT + ACID = FULL FLOW · ACID IN VEIN = 0 · SECRETIN EXTRACT IN VEIN = MASSIVE FLOW", "detail": "Inked Bayliss & Starling (1902, Proc. R. Soc. Lond. 69: 352–353 & J. Physiol. 28: 325–353) four-step experimental proof chart on period paper comparing (1) acid in intact duodenum -> secretion, (2) acid in completely denervated jejunum loop -> full secretion after ~2 min, (3) acid injected directly into blood vein -> 0 secretion, and (4) acid-ground jejunal mucosa extract (secretin) injected into vein -> massive pancreatic secretion", "scale": "when Pavlov's lab in St. Petersburg repeated Bayliss and Starling's nerve-cut experiment and saw the pancreas pour out juice with every wire cut, Pavlov stepped out of his office, shook his head, and said: 'Of course they are right — we cannot claim a monopoly on truth'", "hold_s": 3.8}),
            ("03_ucl_1902_smoked_kymograph_drum_drop_recorder_and_filter_funnel_closeup", 114.0, 6.5, "B", False, "16 JANUARY 1902 — A CHEMICAL REFLEX!", "Fast",
             "Fast: daylight macro shot of a smoked-paper kymograph drum with a white stylus tracing rapid tick marks beside a porcelain mortar with sand and a glass filter funnel on a 1902 London bench. Nothing emissive, no face.",
             STYLE + "In crisp daylight on a 1902 London physiology bench, a rotating brass kymograph drum with a stylus tracing sharp tick marks sits beside a white porcelain mortar and a glass filter funnel." + FAST_TAIL,
             None),
            ("04_anatomical_model_of_duodenum_pancreas_and_blood_vessels_with_cut_wires_pan", 120.5, 5.5, "C", False, "BLOOD VESSELS ONLY, ZERO NERVES", "Fast",
             "Fast: daylight close-up pan across a painted anatomical model of the duodenum, pancreas, and red/blue blood vessels beside surgical scissors and a dropper bottle of 0.4% HCl. Nothing emissive, no face.",
             STYLE + "In bright window light on a wooden table, a painted anatomical model of the small intestine and pancreas linked by red and blue blood vessels sits beside steel surgical scissors and a glass dropper bottle." + FAST_TAIL,
             None),
        ],
    ),
    (
        4,
        "Part 04 — 20 June 1905 – 1977: Coining the Word 'Hormone' & How the Brain Commands Every Gland (The Master Switch)",
        [
            ("01_starling_hardy_vesey_1905_cambridge_dinner_kendall_1914_thyroxine_and_yalow_1959_ria", 126.0, 6.5, "A", False, "'HORMONE' MEANS 'TO SET IN MOTION'", "Quality",
             "Quality: readable faces (Ernest Starling dining at Gonville and Caius College, Cambridge with William Hardy and classicist W. T. Vesey to coin 'hormone' for his 20 June 1905 Croonian Lecture, dissolving to Edward Kendall crystallising thyroid thyroxine on Christmas Day 1914 and medical physicist Rosalyn Yalow in 1959 inventing radioimmunoassay to measure hormones down to a trillionth of a gram).",
             STYLE + "Split period scene: on the left in June 1905 London, Ernest Starling delivers his Croonian Lecture at the Royal College of Physicians beneath a banner of the Greek root hormōn; on the right, Edward Kendall in 1914 inspects thyroxine crystals while Rosalyn Yalow in 1959 loads radioimmunoassay test tubes in her Bronx laboratory." + QUAL_TAIL,
             {"kind": "FACT", "label": "\"Hormone\" means \"to set in motion\"", "who_card": "Edward C. Kendall (1886–1972) — American biochemist · Rosalyn S. Yalow (1921–2011) — American medical physicist", "when_stamp": "20 June 1905 · 25 December 1914 · 1959 · 1977", "timeline_step": "3/4 · 20 Jun 1905 (Ernest Starling coins 'hormone' in his Croonian Lecture) & 4/4 · 1914–1977 (Kendall isolates thyroxine; Rosalyn Yalow invents radioimmunoassay, 1977 Nobel Prize)", "hold_s": 3.8}),
            ("02_starling_1905_kendall_1914_yalow_1959_endocrine_network_and_picogram_ria_chart", 132.5, 8.0, "E", False, "20 JUN 1905 STARLING ('HORMONE'), 25 DEC 1914 KENDALL (THYROXINE) & 1959 YALOW & BERSON RADIOIMMUNOASSAY (10^-12 G/ML PICOGRAM SENSITIVITY)", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked human endocrine network & radioimmunoassay sensitivity chart from Starling (August 1905, Lancet 166: 339–341), Kendall (1915, JAMA / 1950 Nobel), and Yalow & Berson (1959–1960, Nature / J. Clin. Invest.) maps the hypothalamus-pituitary master axis, thyroid (thyroxine), adrenal (adrenaline, cortisol), pancreas (secretin, insulin), and gonads, detected at picogram-per-millilitre (10^-12 g/mL) levels.",
             {"kind": "DATA", "label": "HUMAN ENDOCRINE AXIS (HYPOTHALAMUS-PITUITARY, THYROID, ADRENAL, PANCREAS) & YALOW 1959 RIA (10^-12 G/ML SENSITIVITY)", "detail": "Inked human endocrine network & radioimmunoassay sensitivity chart on period paper from Starling (August 1905, Lancet 166: 339–341), Kendall (1915, JAMA / 1950 Nobel), and Yalow & Berson (1959–1960, Nature / J. Clin. Invest.) mapping the hypothalamus-pituitary master axis, thyroid (thyroxine), adrenal (adrenaline, cortisol), pancreas (secretin, insulin), and gonads, detected at picogram-per-millilitre (10^-12 g/mL) levels", "scale": "Rosalyn Yalow's 1959 hormone detector was so sensitive it could spot a single lump of sugar dissolved in a lake sixty miles long", "hold_s": 3.8}),
            ("03_royal_college_1905_croonian_manuscript_and_bronx_va_1959_ria_test_tube_rack_closeup", 140.5, 6.5, "B", False, "MEASURING HORMONES AT ONE TRILLIONTH OF A GRAM", "Fast",
             "Fast: daylight macro shot of Starling's bound 1905 Croonian Lecture offprint beside a stainless-steel rack of glass radioimmunoassay test tubes and a precision dial gauge on an oak bench. Nothing emissive, no face.",
             STYLE + "In crisp daylight on a laboratory bench, a vintage printed lecture booklet sits beside a steel rack of glass assay tubes and a brushed-metal precision counter dial." + FAST_TAIL,
             None),
            ("04_explorer_dispatching_colour_coded_hormone_keys_from_hypothalamus_pituitary_switchboard", 147.0, 5.5, "B", True, None, "Quality",
             "Quality: Explorer beat 2 (locked character reference).",
             STYLE + "Standing at a grand brass central switchboard, the Explorer dispatches differently shaped brass keys into a clear glass pneumatic blood tube, where each key travels to unlock its matching organ door while bypassing every other lock." + EXP_TAIL,
             None),
        ],
    ),
    (
        5,
        "Part 05 — Why Your Nerves and Hormones Are Two Halves of One System — & How Your Cells Tell Time in Pitch Darkness",
        [
            ("01_timeline_1894_1977_and_hypothalamus_pituitary_neuroendocrine_bridge_chart", 152.5, 8.5, "E", False, "1894–1977 TIMELINE · OLIVER/SCHÄFER & TAKAMINE ADRENALINE, BAYLISS & STARLING SECRETIN, 'HORMONE' (1905) & YALOW RIA", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, the 4-date timeline completes: Mar 1894 & 1901 (George Oliver & Edward Schäfer discover adrenal blood-pressure surge at UCL; Jokichi Takamine & Keizo Uenaka crystallise pure adrenaline) · 16 Jan 1902 (William Bayliss & Ernest Starling sever every nerve to a jejunal loop at UCL and prove acid releases the blood-borne chemical messenger secretin) · 20 Jun 1905 (Ernest Starling coins the word 'hormone' from Greek hormōn, 'to set in motion', in his Croonian Lecture) · 1914–1977 (Edward Kendall isolates thyroxine & cortisone; Banting & Best isolate insulin; Rosalyn Yalow invents radioimmunoassay and Guillemin & Schally map brain-pituitary neuroendocrine control).",
             {"kind": "DATA", "label": "1894–1977 ENDOCRINOLOGY TIMELINE · NERVE CABLES + WIRELESS BLOOD HORMONES UNITED BY THE HYPOTHALAMUS", "detail": "Animated 4-date timeline (1894 → 1977) alongside the hypothalamus-pituitary neuroendocrine bridge diagram uniting millisecond nerve cables with blood-borne hormone broadcasts", "scale": "from a single afternoon nerve-cutting experiment in London to over fifty known human hormones, Bayliss and Starling revealed the wireless chemical postal service that runs your body", "when_stamp": "1894–1977", "timeline_step": "4/4 · 1894–1977 timeline complete", "hold_s": 3.8}),
            ("02_telegraph_key_and_wax_sealed_chemical_vials_linked_by_brass_bridge_on_plinth_pan", 161.0, 5.5, "A", False, "NERVE CABLES + BLOOD BROADCASTS", "Fast",
             "Fast: daylight close-up of a brass telegraph key connected by a sculpted bridge to a carousel of stoppered glass hormone vials on a wooden museum plinth. Nothing emissive, no face.",
             STYLE + "In crisp daylight on a wooden museum plinth, a vintage brass telegraph key links across a carved wooden bridge to a tray of labelled glass apothecary vials and a mercury manometer." + FAST_TAIL,
             None),
            ("03_de_mairan_1729_dark_cupboard_mimosa_and_benzer_konopka_sep_1971_period_flies_handoff", 166.5, 6.5, "C", False, "THE 24-HOUR CIRCADIAN CLOCK", "Quality",
             "Quality: readable faces (Jean-Jacques d'Ortous de Mairan in Paris in 1729 opening his dark cupboard to find his Mimosa plant wide awake at dawn, alongside Seymour Benzer and Ronald Konopka at Caltech in September 1971 discovering the Period clock gene in mutant fruit flies — handoff to 061 The Circadian Clock).",
             STYLE + "Split period scene: on the left in 1729 Paris, astronomer Jean-Jacques d'Ortous de Mairan opens a dark wooden cupboard to see a potted Mimosa plant unfolding its green leaves; on the right in September 1971 at Caltech, Seymour Benzer and Ronald Konopka inspect glass vials of fruit flies beside a 24-hour rhythm chart." + QUAL_TAIL,
             {"kind": "WHEN", "label": "1729 · SEPTEMBER 1971", "hold_s": 3.5}),
            ("04_table_three_callback", 173.0, 2.4, "C", False, None, "reuse",
             "Reuse: verified unused moving window [5.50s..7.90s] of P1:07_table_three_props_oliver_1894_vial_takamine_1900_crystals_and_starling_1902_mortar_kymograph (callback, £0).",
             "Reuse P1:07_table_three_props_oliver_1894_vial_takamine_1900_crystals_and_starling_1902_mortar_kymograph [5.50s..7.90s] (2.40s distinct non-overlapping tail window from 8.00s source clip).",
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
                row["reuse_of"] = "P1:07_table_three_props_oliver_1894_vial_takamine_1900_crystals_and_starling_1902_mortar_kymograph"
                row["reuse_window_s"] = [5.5, 7.9]
                row["reuse_audit"] = {
                    "source_row": "P1:07_table_three_props_oliver_1894_vial_takamine_1900_crystals_and_starling_1902_mortar_kymograph",
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
            "film": "060_Oliver-Takamine-Bayliss-Starling-Hormones-Secretin",
            "part": p_idx,
            "title": p_title,
            "version": "v01",
            "timing_status": "pre_vo_script_clock (built from hormones_script_master_v01.md; retimes onto Scribe STT once VO locks)",
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
        "film": "060_Oliver-Takamine-Bayliss-Starling-Hormones-Secretin",
        "version": "v01",
        "date": "2026-10-19",
        "owner": "gemini (J0631)",
        "status": "PRE_VO_BOARDS_V01_NO_MINT",
        "generation_authorized": False,
        "script": "00_Brand/Channel-Setup/ideas/060_Oliver-Takamine-Bayliss-Starling-Hormones-Secretin/hormones_script_master_v01.md",
        "sources": "00_Brand/Channel-Setup/ideas/060_Oliver-Takamine-Bayliss-Starling-Hormones-Secretin/SOURCES_v01.md",
        "credit_snapshot": {
            "flow_balance": 23740,
            "flow_floor": 0,
            "flow_read_at": "2026-10-15T21:42:22Z",
            "vertex_promo_gbp": 71.02,
            "vertex_usable_gbp": 70.02,
        },
        "totals": totals,
        "per_part": per_part_summary,
        "mint_order": "006 > 007 > 008 > 009 > 010 > 011 > 012 > 013 > 014 > 015 > 016 > 017 > 018 > 019 > 020 > 021 > 022 > 023 > 024 > 025 > 026 > 027 > 028 > 029 > 030 > 031 > 032 > 033 > 034 > 035 > 036 > 037 > 038 > 039 > 040 > 041 > 042 > 043 > 044 > 045 > 046 > 047 > 048 > 049 > 050 > 051 > 052 > 053 > 054 > 055 > 056 > 057 > 058 > 059 > 060 > 061 > 062. Nothing in 060 is generation_authorized.",
    }
    (EDIT / "PICTURE_PLAN_v01.json").write_text(json.dumps(plan, indent=2) + "\n")

    sl = [
        "# 060 Hormones: The Secret Messages in Your Blood — Shot list & plate boards v01 (pre-VO)",
        "",
        "Gemini, 19 Oct 2026, J0631. Built from `hormones_script_master_v01.md` (`91.2 PASS`) and `SOURCES_v01.md`.",
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
        "# 060 price review v01 (pre-VO plate boards)",
        "",
        "Gemini, 19 Oct 2026, J0631. Boards only. **No mint. No spend. No merge.**",
        "Prepared from `hormones_script_master_v01.md` (`91.2 PASS`) and `SOURCES_v01.md` so 060's full plate board rows, non-emissive Fast prompts, £0 code graphics, and Teach-on-Screen overlays are ready to re-time the moment long VO locks. Parked for Chief.",
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
        f"- **Quality ({totals['Quality']} rows):** readable faces (George Oliver, Edward Sharpey-Schäfer, Jokichi Takamine, Keizo Uenaka, William M. Bayliss, Ernest H. Starling, Thomas Addison, John Jacob Abel, Ivan P. Pavlov, Edward C. Kendall, Rosalyn S. Yalow, Jean-Jacques d'Ortous de Mairan, Seymour Benzer, Ronald J. Konopka), March 1894 UCL adrenal blood-pressure shock & July 1900 – 1901 New York pure crystalline adrenaline, 16 January 1902 UCL nerve-cut jejunum `secretin` discovery, 20 June 1905 Croonian Lecture coining 'hormone' & 1959 radioimmunoassay, and the 2 Explorer beats.",
        f"- **Fast ({totals['Fast']} rows, non-emissive):** daylight prop and laboratory shots (porcelain mortar and pestle with sand, dilute HCl dropper bottle & glass U-tube mercury manometer pan, 3-object callback bench, 1900 New York watch dish of white adrenaline needle-crystal rosettes & brass microscope, 1894 UCL mercury manometer column & wrist pulse gauge, 1902 smoked kymograph drum & glass filter funnel, painted anatomical model of duodenum/pancreas blood vessels & surgical scissors, 1905 Croonian Lecture booklet & steel rack of RIA assay tubes, brass telegraph key & apothecary vials bridge on museum plinth). Zero candles, flames, sparks, or glowing elements on Fast.",
        f"- **£0 code graphics ({totals['code_graphic']} rows):**",
        "  1. `P1:04_oliver_schafer_1894_takamine_1901_bayliss_starling_1902_nerve_vs_hormone_1ppb_chart` — wired electrical nerve impulses (~1–100 m/s) vs wireless blood-borne endocrine hormones (`adrenaline`, `secretin`, `insulin`, `thyroxine`) active at ~1 part per billion (`SCALE: a single hormone in your blood is so potent that it works at one part per billion — like dissolving a single pinch of salt inside an Olympic swimming pool and having every cell in the pool taste it`)",
        "  2. `P1:06_bayliss_starling_16_jan_1902_denervated_jejunum_loop_and_120s_pancreatic_flow_chart` — Bayliss & Starling (16 January 1902, *J. Physiol.*) denervated jejunum loop diagram & pancreatic secretion rate curve surging ~120 seconds after acid or venous `secretin` (`SCALE: even with every nerve wire severed by a scalpel, it took just one hundred and twenty seconds for a chemical letter posted in the gut to ride the bloodstream and unlock the pancreas`)",
        "  3. `P2:02_oliver_schafer_1894_kymograph_blood_pressure_surge_and_takamine_1901_adrenaline_c9h13no3_chart` — Oliver & Schäfer (March 1894, *J. Physiol.*) arterial blood-pressure kymograph tracing (~100 → >240 mmHg) & Takamine (1901) crystalline adrenaline (`C9H13NO3`) potency chart (`SCALE: Takamine's adrenaline crystals were so powerful that injecting a single millionth of a gram — a speck far too small for the human eye to see — made blood pressure surge inside seconds`)",
        "  4. `P3:02_bayliss_starling_1902_four_step_secretin_proof_and_pavlov_replication_chart` — Bayliss & Starling (1902, *Proc. R. Soc.* & *J. Physiol.*) 4-step experimental proof comparing intact duodenum + acid, denervated loop + acid, intravenous acid control, and intravenous mucosal extract (`secretin`) (`SCALE: when Pavlov's lab in St. Petersburg repeated Bayliss and Starling's nerve-cut experiment and saw the pancreas pour out juice with every wire cut, Pavlov stepped out of his office, shook his head, and said: 'Of course they are right — we cannot claim a monopoly on truth'`)",
        "  5. `P4:02_starling_1905_kendall_1914_yalow_1959_endocrine_network_and_picogram_ria_chart` — Starling (1905 *Lancet*), Kendall (1914 thyroxine), and Yalow & Berson (1959–1960) human endocrine network & radioimmunoassay picogram (`10^-12 g/mL`) sensitivity chart (`SCALE: Rosalyn Yalow's 1959 hormone detector was so sensitive it could spot a single lump of sugar dissolved in a lake sixty miles long`)",
        "  6. `P5:01_timeline_1894_1977_and_hypothalamus_pituitary_neuroendocrine_bridge_chart` — completed 4-date timeline (1894 → 1977) + hypothalamus-pituitary neuroendocrine bridge diagram (`SCALE: from a single afternoon nerve-cutting experiment in London to over fifty known human hormones, Bayliss and Starling revealed the wireless chemical postal service that runs your body`)",
        f"- **£0 verified reuse ({totals['reuse']} row):** `P5:04_table_three_callback` uses the 2.40 s unused moving tail `[5.50s..7.90s]` of `P1:07_table_three_props_oliver_1894_vial_takamine_1900_crystals_and_starling_1902_mortar_kymograph`.",
        "",
        "## Mint order",
        "",
        "006 > 007 > 008 > 009 > 010 > 011 > 012 > 013 > 014 > 015 > 016 > 017 > 018 > 019 > 020 > 021 > 022 > 023 > 024 > 025 > 026 > 027 > 028 > 029 > 030 > 031 > 032 > 033 > 034 > 035 > 036 > 037 > 038 > 039 > 040 > 041 > 042 > 043 > 044 > 045 > 046 > 047 > 048 > 049 > 050 > 051 > 052 > 053 > 054 > 055 > 056 > 057 > 058 > 059 > 060 > 061 > 062. `generation_authorized` is `false` on every row.",
    ])
    (EDIT / "PRICE_REVIEW_v01.md").write_text("\n".join(pr_lines) + "\n")
    print(f"060 v01 boards written: {totals['rows']} rows, Flow expected={totals['flow_credits_expected']}")


if __name__ == "__main__":
    main()
