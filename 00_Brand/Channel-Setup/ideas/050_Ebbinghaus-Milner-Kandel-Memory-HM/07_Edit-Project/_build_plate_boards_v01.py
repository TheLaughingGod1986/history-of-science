#!/usr/bin/env python3
"""HOS 050 (Memory & Forgetting: The Man Who Lived in 30-Second Loops) pre-VO plate boards v01. J0585. No mint, no spend.

Built from 00_Brand/Channel-Setup/ideas/050_Ebbinghaus-Milner-Kandel-Memory-HM/memory_script_master_v01.md (92.2 PASS)
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
        "Part 01 — The Man Who Forgot Every 30 Seconds Yet Mastered a Mirror Star He Swore He'd Never Seen",
        [
            ("01_brenda_milner_1955_patient_hm_mirror_star_and_kandel_sea_slug_synapse_doubling", 0.0, 5.5, "A", False, "TWO SEPARATE MEMORIES", "Quality",
             "Quality: Short frame 0 / answer image (0:03) + in a quiet room in Connecticut in 1955–1957, neuropsychologist Brenda Milner holds a metal screen over 29-year-old Henry Molaison's (Patient H.M.'s) hand as he traces a double-outlined five-pointed star while looking only into a mirror, paired with giant sea-slug neurons growing double the number of physical synaptic terminals.",
             STYLE + "Split period scene: on the left in a 1955 Connecticut room, neuropsychologist Brenda Milner holds a metal baffle over Henry Molaison's hand as he traces a five-pointed star reflected in a mirror; on the right, a microscopic neural branch sprouts double the number of physical synaptic terminals." + QUAL_TAIL,
             {"kind": "WHEN", "label": "HARTFORD, CONNECTICUT, 1955–1957", "timeline_step": "2/4 · 25 Aug 1953 & 1957 (William Scoville and Brenda Milner study Patient H.M., proving declarative memory requires the hippocampus while motor skill memory is separate)", "hold_s": 3.5}),
            ("02_ebbinghaus_1885_metronome_milner_1957_mirror_star_and_kandel_aplysia_synapses_split", 5.5, 6.0, "B", False, "FORGETTING, PATIENT H.M., SYNAPSES", "Quality",
             "Quality: complex three-part composition (Hermann Ebbinghaus's 1885 ticking metronome and cards of nonsense syllables in Berlin; William Scoville's 25 August 1953 hippocampus model and Brenda Milner's 1957 mirror-star puzzle; and Eric Kandel's Aplysia sea-slug synapse doubling its terminals from 1,300 to 2,600).",
             STYLE + "Three-panel period composition: on the left, a brass metronome beside stacks of three-letter syllable cards in an 1885 Berlin study; in the centre, a tabletop mirror-star tracing apparatus beside a seahorse-shaped hippocampus model; on the right, an Aplysia sea slug in a glass aquarium beside a neuron model doubling its terminal branches." + QUAL_TAIL,
             None),
            ("03_patient_hm_1957_day3_tracing_five_pointed_mirror_star_flawlessly_before_milner", 11.5, 6.0, "C", False, "ZERO CONSCIOUS MEMORY", "Quality",
             "Quality: readable faces (in 1955–1957 in Connecticut, Henry Molaison looks at Brenda Milner's mirror-tracing apparatus as a complete novelty on Trial Day 3, then guides his pencil smoothly around the five-pointed star with near-zero line crossings).",
             STYLE + "In a 1957 Connecticut sitting room, twenty-nine-year-old Henry Molaison looks puzzled at a metal-shielded mirror-drawing stand as Brenda Milner watches, then guides his pencil smoothly and accurately along a five-pointed star reflected in the mirror." + QUAL_TAIL,
             {"kind": "WHEN", "label": "1955–1957", "timeline_step": "2/4 · 25 Aug 1953 & 1957 (Patient H.M. masters the 3-day mirror-star task with zero conscious recall)", "hold_s": 3.5}),
            ("04_ebbinghaus_1885_forgetting_curve_42pct_20min_and_milner_hm_mirror_star_error_chart", 17.5, 8.0, "E", False, "EBBINGHAUS 1885 FORGETTING CURVE (42% AT 20 MIN, 25% AT 6 DAYS) & MILNER 1957 H.M. MIRROR STAR (~30 → <3 ERRORS AT 0% RECALL)", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked Ebbinghaus forgetting curve and Milner 3-day mirror-drawing error chart shows nonsense-syllable retention dropping to 42% after 20 minutes, 33% after 24 hours, and 25% after 6 days (Ebbinghaus 1885), juxtaposed with Patient H.M.'s mirror-star errors plummeting from ~30 on Day 1 to <3 on Day 3 while declarative recall stayed at 0% (Scoville & Milner 1957; Milner 1962).",
             {"kind": "DATA", "label": "EBBINGHAUS FORGETTING (58% LOST IN 20 MIN) VS PATIENT H.M. MIRROR STAR (~30 → <3 ERRORS AT 0% CONSCIOUS RECALL)", "detail": "Inked Ebbinghaus forgetting curve & Milner 3-day mirror-drawing error chart on period paper showing nonsense-syllable retention dropping to 42% after 20 minutes, 33% after 24 hours, and 25% after 6 days (Ebbinghaus 1885), juxtaposed with Patient H.M.'s mirror-star errors plummeting from ~30 on Day 1 to <3 on Day 3 while declarative recall stayed at 0% (Scoville & Milner 1957; Milner 1962)", "scale": "without review, your brain throws away more than half of a new list within the first hour — yet a motor skill learned by your hands can survive for decades even if your hippocampus is completely gone", "who_card": "Hermann Ebbinghaus (1850–1909) — German experimental psychologist · William Beecher Scoville (1906–1984) — American neurosurgeon · Brenda Milner (born 1918) — British-Canadian neuropsychologist · Henry Molaison (1926–2008) — American amnesia patient (H.M.) · Tim Bliss (born 1940) — British neuroscientist · Terje Lømo (born 1935) — Norwegian physiologist · Eric Kandel (born 1929) — Austrian-American neurobiologist", "when_stamp": "1885 · 25 August 1953 · 1957 · 1966–1973 · 2000", "hold_s": 3.8}),
            ("05_brass_metronome_syllable_cards_mirror_star_sheet_and_seahorse_hippocampus_model_pan", 25.5, 5.5, "A", False, "25 AUGUST 1953", "Fast",
             "Fast: daylight macro pan across a ticking brass metronome, stack of card slips, a five-pointed star tracing sheet beside a tabletop mirror, and a carved wooden seahorse beside a brain model on an oak bench between code graphics so two full-frame graphics never run back to back. Nothing emissive, no face.",
             STYLE + "In crisp daylight on an oak laboratory bench, the camera pans smoothly across a polished brass metronome, stacks of paper index cards, a five-pointed star drawing sheet with a tilted mirror, and a carved anatomical brain model." + FAST_TAIL,
             None),
            ("06_kandel_bailey_short_term_1300_vs_long_term_creb_2600_synaptic_terminals_chart", 31.0, 8.0, "E", False, "DOUBLE THE SYNAPSES", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period parchment, an inked synaptic plasticity bar chart from Eric Kandel and Craig Bailey (1983–2000) compares short-term memory (0 new terminals, temporary cyclic-AMP/glutamate boost across ~1,300 terminals lasting minutes) against long-term memory (CREB-driven gene expression doubling physical synaptic terminals from ~1,300 to ~2,600 per sensory neuron, alongside Aplysia's 20,000 neurons vs 86 billion human neurons).",
             {"kind": "DATA", "label": "KANDEL & BAILEY SYNAPTIC GROWTH: 1,300 TERMINALS (SHORT-TERM) → 2,600 TERMINALS (LONG-TERM CREB DOUBLING)", "detail": "Inked synaptic plasticity bar chart comparing short-term memory (0 new terminals, temporary cyclic-AMP/glutamate boost lasting minutes) against long-term memory (CREB-driven gene expression doubling physical synaptic terminals from ~1,300 to ~2,600 per sensory neuron)", "scale": "a sea slug has only twenty thousand nerve cells compared with your eighty-six billion — yet every time you turn a short-term thought into a lifelong memory, your brain cells physically sprout twice as many microscopic branches", "hold_s": 3.8}),
            ("07_table_three_props_ebbinghaus_metronome_milner_mirror_star_and_kandel_synapse_model", 39.0, 5.5, "C", False, "1885 TO 2000", "Fast",
             "Fast: daylight prop table (callback source for Part 05: Ebbinghaus's 1885 brass metronome and syllable cards, Brenda Milner's 1957 mirror-star tracing stand, and Kandel's branching synaptic terminal model). Nothing emissive.",
             STYLE + "On an oak workbench in soft window light sit three objects side by side: a vintage brass metronome beside stacked index cards, a tabletop mirror-star drawing apparatus with a wooden pencil, and a brass-and-wood model of branching neuron terminals." + FAST_TAIL,
             None),
            ("08_explorer_between_padlocked_hippocampus_cabinet_and_working_motor_mirror_star_cabinet", 62.0, 5.5, "A", True, None, "Quality",
             "Quality: Explorer beat 1 (locked character reference, after 1:00).",
             STYLE + "Standing between two wooden brain filing cabinets — a padlocked seahorse-shaped hippocampus cabinet and an open gear-driven motor-memory cabinet — the Explorer pulls a lever on the second cabinet and smoothly traces a five-pointed star reflected in a mirror." + EXP_TAIL,
             None),
            ("09_hermann_ebbinghaus_1885_berlin_flipping_nonsense_syllable_cards_by_metronome", 67.5, 5.5, "B", False, "BERLIN, 1885", "Quality",
             "Quality: readable face (in Berlin in 1885, Hermann Ebbinghaus sits before a ticking brass metronome flipping cards printed with three-letter nonsense syllables).",
             STYLE + "In an 1885 Berlin study, thirty-five-year-old German psychologist Hermann Ebbinghaus in a dark frock coat sits at a wooden desk flipping small paper cards in rhythm with a ticking brass metronome." + QUAL_TAIL,
             {"kind": "WHEN", "label": "BERLIN, 1885", "timeline_step": "1/4 · 1885 (Hermann Ebbinghaus in Berlin publishes the mathematical Forgetting Curve from 2,300 nonsense syllables)", "hold_s": 3.5}),
        ],
    ),
    (
        2,
        "Part 02 — 1879–1885 & 1950: Hermann Ebbinghaus's 2,300 Nonsense Syllables, the Forgetting Curve & Karl Lashley's 30-Year Maze Hunt",
        [
            ("01_ebbinghaus_1885_berlin_2300_syllables_and_karl_lashley_1950_rat_maze_engram_hunt", 73.0, 6.5, "A", False, "2,300 NONSENSE SYLLABLES", "Quality",
             "Quality: readable faces (Hermann Ebbinghaus in Berlin from 1879–1885 testing himself on 2,300 nonsense syllables by a 150-BPM metronome, dissolving to American neuropsychologist Karl Lashley in 1920–1950 watching a trained rat run a wooden maze).",
             STYLE + "Split period scene: on the left in an 1885 Berlin study, Hermann Ebbinghaus records retention scores beside stacks of syllable cards and a brass metronome; on the right in a 1950 psychology lab, Karl Lashley watches a white laboratory rat sprint faultlessly through a wooden maze." + QUAL_TAIL,
             {"kind": "WHO", "label": "Karl Lashley (1890–1958) — American neuropsychologist", "fact_card": "2,300 nonsense syllables", "when_stamp": "1879–1885 · 1885 · 1920–1950 · 1950", "timeline_step": "1/4 · 1885 (Hermann Ebbinghaus in Berlin publishes the mathematical Forgetting Curve from 2,300 nonsense syllables)", "hold_s": 3.8}),
            ("02_ebbinghaus_1885_exponential_forgetting_vs_spaced_repetition_retention_chart", 79.5, 8.0, "E", False, "1885 EBBINGHAUS FORGETTING CURVE (58% LOST AT 20 MIN, 66% AT 1 DAY, 75% AT 6 DAYS) VS SPACED REPETITION", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked Ebbinghaus forgetting vs spaced-repetition curve from Hermann Ebbinghaus (1885, Über das Gedächtnis) shows exponential memory decay (58% lost at 20 min, 66% at 1 day, 75% at 6 days, 79% at 31 days) vs step-wise relearning savings that flatten decay into permanent storage.",
             {"kind": "DATA", "label": "1885 EBBINGHAUS CURVE: 58% LOST AT 20 MIN & 75% AT 6 DAYS VS SPACED-REPETITION FLATTENING", "detail": "Inked Ebbinghaus forgetting vs spaced-repetition curve on period paper from Hermann Ebbinghaus (1885, Über das Gedächtnis) showing exponential memory decay (58% lost at 20 min, 66% at 1 day, 75% at 6 days, 79% at 31 days) vs step-wise relearning savings that flatten decay into permanent storage", "scale": "within twenty minutes of cramming a new list, more than half of it has already evaporated from your brain — unless you reset the curve with spaced review", "hold_s": 3.8}),
            ("03_ebbinghaus_1885_uber_das_gedachtnis_book_metronome_and_card_box_closeup", 87.5, 6.5, "B", False, "1885 — THE FORGETTING CURVE", "Fast",
             "Fast: daylight macro shot of Hermann Ebbinghaus's 1885 leather-bound volume 'Über das Gedächtnis' beside a wooden box of 2,300 paper cards and a brass metronome on an oak desk. Nothing emissive, no face.",
             STYLE + "In crisp daylight on a wooden study desk, an 1885 German psychology book sits beside a long wooden index-card box packed with paper slips and a brass metronome." + FAST_TAIL,
             None),
            ("04_lashley_1950_wooden_rat_maze_and_cortical_diagram_pan", 94.0, 5.5, "C", False, "1950 — THE ENGRAM HUNT", "Fast",
             "Fast: daylight close-up pan across Karl Lashley's 1950 tabletop wooden labyrinth maze, a brass stopwatch, and a carved wooden cerebral cortex model on a laboratory table. Nothing emissive, no face.",
             STYLE + "In bright window light on a laboratory bench, a miniature wooden tabletop maze rests beside a mechanical brass stopwatch and a painted wooden brain cortex model." + FAST_TAIL,
             None),
        ],
    ),
    (
        3,
        "Part 03 — 25 August 1953 & 1957: Patient H.M. (Henry Molaison) & Brenda Milner's Mirror-Star Twist — Midpoint Twist",
        [
            ("01_scoville_25_aug_1953_hippocampus_and_brenda_milner_1957_patient_hm_mirror_star", 99.5, 6.5, "A", False, "SWORE HE'D NEVER SEEN IT", "Quality",
             "Quality: readable faces (neurosurgeon William Beecher Scoville on 25 August 1953 in Hartford examining a brain model of the medial temporal lobe and hippocampus, dissolving to Brenda Milner in 1955–1957 testing Henry Molaison at his kitchen table with the mirror-star drawing apparatus).",
             STYLE + "Split period scene: on the left in a 1953 Hartford hospital office, neurosurgeon William Scoville points to the seahorse-shaped hippocampus on an anatomical brain model; on the right in 1957, Brenda Milner watches Henry Molaison trace a five-pointed star reflected in a mirror." + QUAL_TAIL,
             {"kind": "FACT", "label": "Swore he'd never seen it", "when_stamp": "25 August 1953 · 1955–1957 · 1957 · 1962 · 2008", "timeline_step": "2/4 · 25 Aug 1953 & 1957 (William Scoville and Brenda Milner study Patient H.M., proving declarative memory requires the hippocampus while motor skill memory is separate)", "hold_s": 3.8}),
            ("02_milner_1962_patient_hm_3_day_30_trial_mirror_star_error_drop_vs_zero_recall_chart", 106.0, 8.0, "E", False, "1957–1962 MILNER MIRROR-STAR CURVE: ~30 ERRORS (DAY 1) → <3 ERRORS (DAY 3, 30 TRIALS) AT 0% DECLARATIVE RECALL", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked 3-day mirror-drawing learning curve from Brenda Milner (1962, Physiologie de l'Hippocampe, & Scoville & Milner 1957 J. Neurol. Neurosurg. Psychiatry 20: 11–21) shows Patient H.M.'s error score dropping across 30 trials over 3 days from ~30 line-crossings on Trial 1 to <3 on Day 3 while conscious recognition of the apparatus remained 0%.",
             {"kind": "DATA", "label": "PATIENT H.M. MIRROR-STAR TEST: ~30 ERRORS ON DAY 1 → <3 ERRORS ON DAY 3 (0% CONSCIOUS RECOGNITION)", "detail": "Inked 3-day mirror-drawing learning curve on period paper from Brenda Milner (1962, Physiologie de l'Hippocampe, & Scoville & Milner 1957 J. Neurol. Neurosurg. Psychiatry 20: 11–21) showing Patient H.M.'s error score dropping across 30 trials over 3 days from ~30 line-crossings on Trial 1 to <3 on Day 3 while conscious recognition of the apparatus remained 0%", "scale": "for fifty-five years, Henry Molaison lived inside a thirty-second sliding window of the present — yet his hands learned new skills as smoothly as yours", "hold_s": 3.8}),
            ("03_milner_1957_mirror_star_tracing_apparatus_metal_baffle_and_pencil_closeup", 114.0, 6.5, "B", False, "1957 — PROCEDURAL VS DECLARATIVE", "Fast",
             "Fast: daylight macro shot of Brenda Milner's 1957 mirror-drawing apparatus — an upright mirror, metal hand-baffle screen, and paper sheet with a double-outlined five-pointed star and neat pencil track — on an oak table. Nothing emissive, no face.",
             STYLE + "In crisp daylight on a wooden table, a psychological mirror-tracing stand with an angled metal hand shield and an upright mirror reflects a paper sheet bearing a neatly traced five-pointed star and a wooden pencil." + FAST_TAIL,
             None),
            ("04_seahorse_beside_anatomical_hippocampus_model_and_1957_jnnp_paper_pan", 120.5, 5.5, "C", False, "25 AUGUST 1953 — THE HIPPOCAMPUS", "Fast",
             "Fast: daylight close-up pan across a dried museum seahorse specimen beside a cutaway anatomical model of the human hippocampus and Scoville and Milner's 1957 journal paper on an oak desk. Nothing emissive, no face.",
             STYLE + "In bright window light on an oak desk, a preserved museum seahorse rests right beside a matching seahorse-shaped hippocampus brain model and an open 1957 neurological journal." + FAST_TAIL,
             None),
        ],
    ),
    (
        4,
        "Part 04 — 1966–2000: Bliss & Lømo's High-Frequency Spark & Eric Kandel's Sea Slug (How a Thought Grows New Flesh)",
        [
            ("01_bliss_lomo_1966_oslo_ltp_and_eric_kandel_craig_bailey_aplysia_giant_neurons", 126.0, 6.5, "A", False, "20,000 GIANT SLUG NEURONS", "Quality",
             "Quality: readable faces (Tim Bliss and Terje Lømo in Oslo in 1966–1973 recording Long-Term Potentiation in the hippocampus, dissolving to Eric Kandel and Craig Bailey at Columbia University in 1970–2000 examining a California sea slug Aplysia californica and its 1-millimetre giant neurons).",
             STYLE + "Split period scene: on the left in a 1966 Oslo physiology lab, Terje Lømo and Tim Bliss inspect a rising synaptic trace on a paper chart recorder; on the right at Columbia University, Eric Kandel and Craig Bailey observe a California sea slug in a glass seawater tank beside a microscope." + QUAL_TAIL,
             {"kind": "WHO", "label": "Donald Hebb (1904–1985) — Canadian neuropsychologist · Craig H. Bailey (born 1951) — American neurobiologist", "fact_card": "20,000 giant slug neurons", "when_stamp": "1949 · 1966 · 1973 · 1983 · 2000", "timeline_step": "3/4 · 1966–1973 (Tim Bliss and Terje Lømo discover Long-Term Potentiation in the hippocampus) & 4/4 · 1983–2000 (Eric Kandel and Craig Bailey prove in Aplysia sea slugs that long-term memory activates CREB to double physical synaptic terminals from ~1,300 to ~2,600)", "hold_s": 3.8}),
            ("02_kandel_bailey_1983_short_term_camp_vs_long_term_creb_1300_to_2600_synapses_chart", 132.5, 8.0, "E", False, "1983–2000 KANDEL & BAILEY: 1 PULSE SHORT-TERM (cAMP, 1,300 TERMINALS) VS 5 SPACED PULSES LONG-TERM (CREB DOUBLES TO 2,600 TERMINALS)", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked short-term vs long-term synaptic architecture diagram from Eric Kandel & Craig Bailey (1983 Science 220: 91–93 & 2000 Nobel Lecture) shows 1 training pulse causing temporary cAMP/glutamate enhancement across 1,300 existing terminals (short-term memory, minutes) vs 4–5 spaced training pulses activating CREB gene transcription to grow ~2,600 physical terminals (long-term memory, weeks).",
             {"kind": "DATA", "label": "SHORT-TERM (cAMP, 1,300 TERMINALS) VS LONG-TERM MEMORY (CREB GENE SWITCH DOUBLES SYNAPSES TO 2,600)", "detail": "Inked short-term vs long-term synaptic architecture diagram on period paper from Eric Kandel & Craig Bailey (1983 Science 220: 91–93 & 2000 Nobel Lecture) showing 1 training pulse causing temporary cAMP/glutamate enhancement across 1,300 existing terminals (short-term memory, minutes) vs 4–5 spaced training pulses activating CREB gene transcription to grow ~2,600 physical terminals (long-term memory, weeks)", "scale": "learning something for the rest of your life literally changes the physical anatomy of your brain — sprouting twice as many microscopic bridges between the nerve cells that carry that memory", "hold_s": 3.8}),
            ("03_aplysia_sea_slug_tank_micromanipulator_and_giant_neuron_dish_closeup", 140.5, 6.5, "B", False, "1983–2000 — CREB & SYNAPTIC GROWTH", "Fast",
             "Fast: daylight macro shot of a glass seawater dish, brass micromanipulator dials, and a 3D anatomical model comparing a 1,300-terminal neuron against a 2,600-terminal neuron on a Columbia laboratory bench. Nothing emissive, no face.",
             STYLE + "In crisp daylight on a neurobiology workbench, a precision brass micromanipulator sits beside a glass Petri dish and two contrasting 3D neuron models: one with sparse branches and the other with double the synaptic terminals." + FAST_TAIL,
             None),
            ("04_explorer_switching_on_creb_nucleus_workshop_to_build_double_synaptic_bridges", 147.0, 5.5, "B", True, None, "Quality",
             "Quality: Explorer beat 2 (locked character reference).",
             STYLE + "Standing inside a giant cutaway neuron, the Explorer rings a spaced-training bell five times to unlock the cell nucleus workshop, sending out tiny wooden bridge-beams that double the number of synaptic bridges linking to the neighbouring neuron." + EXP_TAIL,
             None),
        ],
    ),
    (
        5,
        "Part 05 — Why Your Brain Rewires Itself When You Learn & Why Chili Peppers Trick Your Mouth Into Feeling on Fire",
        [
            ("01_timeline_1885_2000_and_dual_memory_synaptic_consolidation_chart", 152.5, 8.5, "E", False, "1885–2000 TIMELINE · FORGETTING CURVE, PATIENT H.M. HIPPOCAMPUS & CREB SYNAPTIC DOUBLING (1,300 → 2,600)", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, the 4-date timeline completes: 1885 (Hermann Ebbinghaus in Berlin publishes the mathematical Forgetting Curve from 2,300 nonsense syllables) · 25 Aug 1953 & 1957 (William Scoville and Brenda Milner study Patient H.M., proving declarative memory requires the hippocampus while motor skill memory is separate) · 1966–1973 (Tim Bliss and Terje Lømo discover Long-Term Potentiation in the hippocampus) · 1983–2000 (Eric Kandel and Craig Bailey prove in Aplysia sea slugs that long-term memory activates CREB to double physical synaptic terminals from ~1,300 to ~2,600).",
             {"kind": "DATA", "label": "1885–2000 MEMORY TIMELINE · EBBINGHAUS CURVE, PATIENT H.M. DUAL MEMORY & KANDEL 2,600-SYNAPSE GROWTH", "detail": "Animated 4-date timeline (1885 → 2000) alongside the hippocampal indexing and CREB synaptic doubling diagram", "scale": "by the time you finish watching this nine-minute film, the neurons inside your hippocampus have already begun firing the genetic switches to wire these stories into physical branches inside your brain", "when_stamp": "1885–2000", "timeline_step": "4/4 · 1885–2000 timeline complete", "hold_s": 3.8}),
            ("02_spaced_study_calendar_metronome_and_branching_synapse_sculpture_pan", 161.0, 5.5, "A", False, "NEURONS THAT FIRE TOGETHER", "Fast",
             "Fast: daylight close-up of an open spaced-review study notebook beside a brass metronome and a golden branching synaptic tree model on a wooden museum plinth. Nothing emissive, no face.",
             STYLE + "In crisp daylight on a wooden museum plinth, an open leather notebook with spaced study dates sits beside a brass metronome and a detailed brass sculpture of branching neuron synapses." + FAST_TAIL,
             None),
            ("03_scoville_may_1912_chili_dilution_and_david_julius_23_oct_1997_trpv1_handoff", 166.5, 6.5, "C", False, "CHILI HEAT AND PEPPERMINT COLD", "Quality",
             "Quality: readable faces (pharmacist Wilbur Scoville in May 1912 diluting chili pepper extract in sugar water, alongside molecular physiologist David Julius on 23 October 1997 and Ardem Patapoutian in 2002 with red chili peppers, green peppermint leaves, and TRPV1/TRPM8 ion channel models — handoff to 051 Pain, Temperature & Touch Receptors).",
             STYLE + "Split period scene: on the left in a 1912 Detroit pharmacy lab, pharmacist Wilbur Scoville pipettes red chili pepper extract into a row of glass sugar-water beakers; on the right in 1997 San Francisco, physiologist David Julius examines a molecular ion-channel gate beside fresh red chilies and green peppermint leaves." + QUAL_TAIL,
             {"kind": "WHEN", "label": "MAY 1912 · 23 OCTOBER 1997 · 2002", "hold_s": 3.5}),
            ("04_table_three_callback", 173.0, 2.4, "C", False, None, "reuse",
             "Reuse: verified unused moving window [5.50s..7.90s] of P1:07_table_three_props_ebbinghaus_metronome_milner_mirror_star_and_kandel_synapse_model (callback, £0).",
             "Reuse P1:07_table_three_props_ebbinghaus_metronome_milner_mirror_star_and_kandel_synapse_model [5.50s..7.90s] (2.40s distinct non-overlapping tail window from 8.00s source clip).",
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
                row["reuse_of"] = "P1:07_table_three_props_ebbinghaus_metronome_milner_mirror_star_and_kandel_synapse_model"
                row["reuse_window_s"] = [5.5, 7.9]
                row["reuse_audit"] = {
                    "source_row": "P1:07_table_three_props_ebbinghaus_metronome_milner_mirror_star_and_kandel_synapse_model",
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
            "film": "050_Ebbinghaus-Milner-Kandel-Memory-HM",
            "part": p_idx,
            "title": p_title,
            "version": "v01",
            "timing_status": "pre_vo_script_clock (built from memory_script_master_v01.md; retimes onto Scribe STT once VO locks)",
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
        "film": "050_Ebbinghaus-Milner-Kandel-Memory-HM",
        "version": "v01",
        "date": "2026-10-18",
        "owner": "gemini (J0585)",
        "status": "PRE_VO_BOARDS_V01_NO_MINT",
        "generation_authorized": False,
        "script": "00_Brand/Channel-Setup/ideas/050_Ebbinghaus-Milner-Kandel-Memory-HM/memory_script_master_v01.md",
        "sources": "00_Brand/Channel-Setup/ideas/050_Ebbinghaus-Milner-Kandel-Memory-HM/SOURCES_v01.md",
        "credit_snapshot": {
            "flow_balance": 23740,
            "flow_floor": 0,
            "flow_read_at": "2026-10-15T21:42:22Z",
            "vertex_promo_gbp": 71.02,
            "vertex_usable_gbp": 70.02,
        },
        "totals": totals,
        "per_part": per_part_summary,
        "mint_order": "006 > 007 > 008 > 009 > 010 > 011 > 012 > 013 > 014 > 015 > 016 > 017 > 018 > 019 > 020 > 021 > 022 > 023 > 024 > 025 > 026 > 027 > 028 > 029 > 030 > 031 > 032 > 033 > 034 > 035 > 036 > 037 > 038 > 039 > 040 > 041 > 042 > 043 > 044 > 045 > 046 > 047 > 048 > 049 > 050 > 051 > 052 > 053. Nothing in 050 is generation_authorized.",
    }
    (EDIT / "PICTURE_PLAN_v01.json").write_text(json.dumps(plan, indent=2) + "\n")

    sl = [
        "# 050 Memory & Forgetting: The Man Who Lived in 30-Second Loops — Shot list & plate boards v01 (pre-VO)",
        "",
        "Gemini, 18 Oct 2026, J0585. Built from `memory_script_master_v01.md` (`92.2 PASS`) and `SOURCES_v01.md`.",
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
        "# 050 price review v01 (pre-VO plate boards)",
        "",
        "Gemini, 18 Oct 2026, J0585. Boards only. **No mint. No spend. No merge.**",
        "Prepared from `memory_script_master_v01.md` (`92.2 PASS`) and `SOURCES_v01.md` so 050's full plate board rows, non-emissive Fast prompts, £0 code graphics, and Teach-on-Screen overlays are ready to re-time the moment long VO locks. Parked for Chief.",
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
        f"- **Quality ({totals['Quality']} rows):** readable faces (Brenda Milner, Henry Molaison / Patient H.M., Hermann Ebbinghaus, Karl Lashley, William Beecher Scoville, Tim Bliss, Terje Lømo, Eric Kandel, Craig Bailey, Wilbur Scoville, David Julius), 1955–1957 Connecticut mirror-star test, 1885 Berlin nonsense-syllable metronome experiments, 1953 Hartford hippocampus surgery, 1966 Oslo LTP & Columbia Aplysia sea-slug lab, and the 2 Explorer beats.",
        f"- **Fast ({totals['Fast']} rows, non-emissive):** daylight prop and laboratory shots (brass metronome, syllable cards, mirror-star sheet & hippocampus model pan, 3-object callback bench, Ebbinghaus's 1885 *Über das Gedächtnis* book & card box, Lashley's 1950 wooden rat maze & stopwatch, Milner's 1957 mirror-drawing stand & metal hand shield, preserved seahorse beside hippocampus model & 1957 JNNP paper, brass micromanipulator & 1,300 vs 2,600 terminal models, spaced study calendar & branching synapse sculpture). Zero candles, flames, sparks, or glowing elements on Fast.",
        f"- **£0 code graphics ({totals['code_graphic']} rows):**",
        "  1. `P1:04_ebbinghaus_1885_forgetting_curve_42pct_20min_and_milner_hm_mirror_star_error_chart` — Ebbinghaus's 1885 forgetting curve (42% left at 20 min, 33% at 24 h, 25% at 6 days) juxtaposed with Brenda Milner's 3-day Patient H.M. mirror-star error drop (~30 → <3 errors at 0% declarative recall) (`SCALE: without review, your brain throws away more than half of a new list within the first hour — yet a motor skill learned by your hands can survive for decades even if your hippocampus is completely gone`)",
        "  2. `P1:06_kandel_bailey_short_term_1300_vs_long_term_creb_2600_synaptic_terminals_chart` — Kandel & Bailey's short-term (1,300 terminals) vs long-term CREB-driven synaptic doubling (2,600 terminals per sensory neuron, alongside Aplysia's 20,000 neurons vs 86B human neurons) (`SCALE: a sea slug has only twenty thousand nerve cells compared with your eighty-six billion — yet every time you turn a short-term thought into a lifelong memory, your brain cells physically sprout twice as many microscopic branches`)",
        "  3. `P2:02_ebbinghaus_1885_exponential_forgetting_vs_spaced_repetition_retention_chart` — Ebbinghaus's 1885 exponential forgetting curve (58% lost at 20 min, 75% at 6 days) vs spaced-repetition relearning savings (`SCALE: within twenty minutes of cramming a new list, more than half of it has already evaporated from your brain — unless you reset the curve with spaced review`)",
        "  4. `P3:02_milner_1962_patient_hm_3_day_30_trial_mirror_star_error_drop_vs_zero_recall_chart` — Milner's 1957/1962 3-day 30-trial Patient H.M. mirror-drawing learning curve (~30 → <3 errors) vs 0% conscious recall (`SCALE: for fifty-five years, Henry Molaison lived inside a thirty-second sliding window of the present — yet his hands learned new skills as smoothly as yours`)",
        "  5. `P4:02_kandel_bailey_1983_short_term_camp_vs_long_term_creb_1300_to_2600_synapses_chart` — Kandel & Bailey's 1983–2000 1-pulse cAMP short-term enhancement (1,300 terminals) vs 5-pulse CREB long-term structural doubling (2,600 terminals) (`SCALE: learning something for the rest of your life literally changes the physical anatomy of your brain — sprouting twice as many microscopic bridges between the nerve cells that carry that memory`)",
        "  6. `P5:01_timeline_1885_2000_and_dual_memory_synaptic_consolidation_chart` — completed 4-date timeline (1885 → 2000) + hippocampal indexing and CREB synaptic doubling diagram (`SCALE: by the time you finish watching this nine-minute film, the neurons inside your hippocampus have already begun firing the genetic switches to wire these stories into physical branches inside your brain`)",
        f"- **£0 verified reuse ({totals['reuse']} row):** `P5:04_table_three_callback` uses the 2.40 s unused moving tail `[5.50s..7.90s]` of `P1:07_table_three_props_ebbinghaus_metronome_milner_mirror_star_and_kandel_synapse_model`.",
        "",
        "## Mint order",
        "",
        "006 > 007 > 008 > 009 > 010 > 011 > 012 > 013 > 014 > 015 > 016 > 017 > 018 > 019 > 020 > 021 > 022 > 023 > 024 > 025 > 026 > 027 > 028 > 029 > 030 > 031 > 032 > 033 > 034 > 035 > 036 > 037 > 038 > 039 > 040 > 041 > 042 > 043 > 044 > 045 > 046 > 047 > 048 > 049 > 050 > 051 > 052 > 053. `generation_authorized` is `false` on every row.",
    ])
    (EDIT / "PRICE_REVIEW_v01.md").write_text("\n".join(pr_lines) + "\n")
    print(f"050 v01 boards written: {totals['rows']} rows, Flow expected={totals['flow_credits_expected']}")


if __name__ == "__main__":
    main()
