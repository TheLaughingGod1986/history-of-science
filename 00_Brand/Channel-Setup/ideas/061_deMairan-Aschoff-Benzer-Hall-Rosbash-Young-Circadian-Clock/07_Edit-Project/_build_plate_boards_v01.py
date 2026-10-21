#!/usr/bin/env python3
"""HOS 061 (The Circadian Clock: The 24-Hour Timer Inside Your Cells) pre-VO plate boards v01. J0631. No mint, no spend.

Built from 00_Brand/Channel-Setup/ideas/061_deMairan-Aschoff-Benzer-Hall-Rosbash-Young-Circadian-Clock/circadian_script_master_v01.md
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
        "Part 01 — The Plant in the Dark Cupboard & the 24-Hour Hourglass Inside Your Cells",
        [
            ("01_de_mairan_1729_paris_dark_cupboard_mimosa_and_per_tim_nuclear_hourglass_cycle", 0.0, 5.5, "A", False, "24-HOUR CLOCK IN THE DARK", "Quality",
             "Quality: Short frame 0 / answer image (0:03) + inside a pitch-black Parisian cupboard in 1729, a sensitive Mimosa plant still unfolds its green leaves at dawn and folds them at dusk, zooming into a single human cell where golden PER and TIM clock proteins accumulate all evening until midnight, enter the nucleus, and switch off their own genes on a 24-hour cycle.",
             STYLE + "Split historical-and-cellular scene: on the left in 1729 Paris, a potted Mimosa pudica plant inside a dark wooden cupboard unfolds its green leaves on schedule; on the right, inside a living cell, golden PER and TIM protein spheres accumulate in the cytoplasm until midnight, pair up, and enter the nucleus to flip their own gene switch off." + QUAL_TAIL,
             {"kind": "WHEN", "label": "PARIS, 1729", "timeline_step": "1/4 · 1729 (Jean-Jacques d'Ortous de Mairan proves a Mimosa plant in a pitch-black Paris cupboard still opens and closes its leaves on a daily cycle)", "hold_s": 3.5}),
            ("02_de_mairan_1729_paris_aschoff_1962_andechs_bunker_and_benzer_konopka_hall_rosbash_young_split", 5.5, 6.0, "B", False, "DARK CUPBOARD, BUNKER, PERIOD GENE", "Quality",
             "Quality: complex three-part composition (Jean-Jacques d'Ortous de Mairan in Paris in 1729 opening his dark cupboard to find his Mimosa plant wide awake; Jürgen Aschoff monitoring volunteers in the Andechs underground bunker in Bavaria in 1962; and Seymour Benzer and Ronald Konopka at Caltech in September 1971 alongside Jeffrey Hall, Michael Rosbash, and Michael Young in 1984–1994 mapping the Period/Timeless molecular clock).",
             STYLE + "Three-panel period composition: on the left, Jean-Jacques d'Ortous de Mairan in 1729 Paris peeking into a wooden cupboard at an open Mimosa plant; in the centre, Jürgen Aschoff in 1962 Bavaria inspecting a strip-chart recorder outside a concrete underground bunker; on the right, Seymour Benzer and Ronald Konopka in 1971 Pasadena beside fruit-fly vials and Jeffrey Hall, Michael Rosbash, and Michael Young inspecting a molecular clock model." + QUAL_TAIL,
             None),
            ("03_human_scn_20000_neuron_master_clock_and_peripheral_organ_clocks_in_liver_heart_skin", 11.5, 6.0, "C", False, "BILLIONS OF CELLULAR CLOCKS", "Quality",
             "Quality: complex anatomical and conceptual reveal (a human anatomical cross-section shows not only the master 20,000-neuron suprachiasmatic nucleus clock in the hypothalamus behind the eyes, but billions of individual 24-hour molecular clocks ticking inside liver, heart, muscle, and skin cells).",
             STYLE + "Split anatomical-and-microscopic scene: on the left, a cross-section of the human head and torso highlights the master suprachiasmatic clock above the optic nerves alongside synchronised clock dials in the liver, heart, and kidneys; on the right, a cluster of liver cells each turns its own internal 24-hour protein gear." + QUAL_TAIL,
             {"kind": "WHEN", "label": "1729 · 15 JUNE 1962 · SEPTEMBER 1971 · OCTOBER 1984 · 1994", "timeline_step": "1/4 · 1729 (de Mairan) · 2/4 · Jun–Sep 1962 (Aschoff & Siffre) · 3/4 · Sep 1971 (Konopka & Benzer) · 4/4 · 1984–1994 (Hall, Rosbash & Young)", "hold_s": 3.5}),
            ("04_de_mairan_1729_aschoff_1962_konopka_benzer_1971_24h11m_and_period_mutants_chart", 17.5, 8.0, "E", False, "HUMAN FREE-RUNNING CLOCK (24 H 11 MIN) & KONOPKA-BENZER SEP 1971 PERIOD MUTANTS: PERS (19 H), PERL (28 H) & PER0 (ARRHYTHMIC)", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked circadian actogram & Konopka-Benzer Period mutant rhythm chart from de Mairan (1729 Hist. Acad. Roy. Sci. p. 35), Aschoff (15 June 1962 Science 136: 963–966), Konopka & Benzer (September 1971 PNAS 68: 2112–2116), and Hall, Rosbash & Young (1984–1994 Cell / Science) plots wild-type 24.0-hour rhythms alongside human free-running bunker drift (24 h 11 min average, Czeisler 1999) and the three Drosophila Period mutants: short-period perS (19 hours), long-period perL (28 hours), and arrhythmic per0.",
             {"kind": "DATA", "label": "WILD-TYPE (24.0 H) · HUMAN BUNKER PERIOD (24 H 11 MIN) · DROSOPHILA PERIOD MUTANTS: PERS (19 H), PERL (28 H), PER0 (0)", "detail": "Inked circadian period comparison chart on period paper showing wild-type 24-hour rhythm, human free-running bunker period (24 h 11 min average, drifting ~11 minutes later every day without morning sunlight), and Konopka & Benzer's September 1971 single-gene Period (per) mutants running at 19 hours (perS), 28 hours (perL), or losing all rhythm (per0)", "scale": "without morning sunlight to reset your eyes, the natural clock inside a human body runs about twenty-four hours and eleven minutes long — drifting eleven minutes later every single day like a pocket watch that runs slightly slow", "who_card": "Jean-Jacques d'Ortous de Mairan (1678–1771) — French astronomer and geophysicist · Jürgen Aschoff (1913–1998) — German physician and physiologist · Seymour Benzer (1921–2007) — American physicist and geneticist · Ronald J. Konopka (1947–2015) — American geneticist · Jeffrey C. Hall (born 1945) — American geneticist · Michael Rosbash (born 1944) — American geneticist · Michael W. Young (born 1949) — American geneticist", "when_stamp": "1729 · 15 June 1962 · September 1971 · October 1984 · 1994", "hold_s": 3.8}),
            ("05_brass_pocket_watch_sand_hourglass_potted_mimosa_and_drosophila_vial_pan", 25.5, 5.5, "A", False, "24 HOURS AND 11 MINUTES", "Fast",
             "Fast: daylight macro pan across an open-face brass pocket watch, a glass sand hourglass, a terracotta pot with a sensitive Mimosa plant, and a stoppered glass fruit-fly vial on an oak bench between code graphics so two full-frame graphics never run back to back. Nothing emissive, no face.",
             STYLE + "In crisp daylight on an oak laboratory bench, the camera pans smoothly across an open brass pocket watch, a wooden-framed sand hourglass, a small potted Mimosa plant, and a cotton-stoppered glass fruit-fly culture vial." + FAST_TAIL,
             None),
            ("06_hall_rosbash_young_1990_1994_per_tim_ttfl_molecular_hourglass_oscillation_chart", 31.0, 8.0, "E", False, "THE PER/TIM CELLULAR HOURGLASS", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period parchment, an inked transcription-translation negative feedback loop (TTFL) hourglass diagram & 24-hour oscillation curve (from Hardin, Hall & Rosbash 1990 Nature and Vosshall, Price, Sehgal & Young 1994 Science) shows CLOCK/CYC turning on the period (per) and timeless (tim) genes by day, PER and TIM proteins building up in the cytoplasm all evening until they pair up with DOUBLETIME (DBT), enter the nucleus around midnight, and repress their own transcription until dawn degrades them.",
             {"kind": "DATA", "label": "1984–1994 HALL, ROSBASH & YOUNG: 24-HOUR PER/TIM NEGATIVE-FEEDBACK LOOP (12 H BUILDUP → MIDNIGHT SHUTOFF → 12 H DECAY)", "detail": "Inked 24-hour PER/TIM protein & mRNA oscillation curve across a day-night cycle showing per mRNA peaking in early evening followed ~4–6 hours later by nuclear PER/TIM protein complex peaking late at night to repress transcription", "scale": "every cell in your body tells time like an old sand hourglass — spending twelve hours trickling PER and TIM protein grains into a pile until at midnight the pile tips over, shuts off the tap, and takes twelve hours to drain away", "hold_s": 3.8}),
            ("07_table_three_props_1729_mimosa_pot_1962_bunker_strip_chart_and_1971_caltech_fly_tubes", 39.0, 5.5, "C", False, "1729 TO 2017", "Fast",
             "Fast: daylight prop table (callback source for Part 05: de Mairan's 1729 potted Mimosa pudica plant, Jürgen Aschoff's 1962 bunker actogram strip-chart roll, and Konopka & Benzer's 1971 glass fruit-fly activity tubes). Nothing emissive.",
             STYLE + "On an oak workbench in soft window light sit three objects side by side: a terracotta pot holding a green Mimosa plant, a paper roll of plotted actogram bars, and a rack of three glass fruit-fly tubes." + FAST_TAIL,
             None),
            ("08_explorer_stacking_per_and_tim_blocks_in_cellular_clock_tower_to_flip_midnight_lever", 62.0, 5.5, "A", True, None, "Quality",
             "Quality: Explorer beat 1 (locked character reference, after 1:00).",
             STYLE + "Inside a wooden cellular clock tower, the Explorer stacks carved golden PER and TIM blocks into a tall column until the top block trips an overhead brass lever to the OFF position, then watches the blocks unstack by dawn so the lever resets." + EXP_TAIL,
             None),
            ("09_konopka_and_benzer_sep_1971_caltech_watching_19h_24h_28h_drosophila_activity_counters", 67.5, 5.5, "B", False, "CALTECH, SEPTEMBER 1971", "Quality",
             "Quality: readable faces (at Caltech in September 1971, graduate student Ronald Konopka and Seymour Benzer watch three glass tubes of fruit flies connected to activity counters ticking at 19 hours, 24 hours, and 28 hours).",
             STYLE + "In a 1971 Caltech genetics laboratory, Seymour Benzer and young Ronald Konopka lean over a bench of three glass fruit-fly tubes connected to mechanical paper strip recorders plotting 19-hour, 24-hour, and 28-hour rhythms." + QUAL_TAIL,
             {"kind": "WHEN", "label": "CALTECH, SEPTEMBER 1971", "timeline_step": "3/4 · Sep 1971 (Ronald Konopka & Seymour Benzer at Caltech discover the Period clock gene in mutant fruit flies)", "hold_s": 3.5}),
        ],
    ),
    (
        2,
        "Part 02 — 1729 – 1962: De Mairan's Dark Cupboard, Franz Halberg's 'Circadian' Rhythm & Jürgen Aschoff's Underground Bunker",
        [
            ("01_de_mairan_1729_halberg_1959_aschoff_1962_bunker_and_siffre_1962_alpine_glacier_cave", 73.0, 6.5, "A", False, "HUMAN CLOCK: 24 HOURS, 11 MINUTES", "Quality",
             "Quality: readable faces (astronomer Jean-Jacques d'Ortous de Mairan in 1729 Paris peeking into a pitch-black cupboard at his Mimosa plant, dissolving to Franz Halberg in 1959 coining 'circadian', Jürgen Aschoff in the Andechs underground bunker in June 1962, and French geologist Michel Siffre camping 130 metres underground in the Scarasson alpine cave from July to September 1962).",
             STYLE + "Split period scene: on the left in 1729 Paris, Jean-Jacques d'Ortous de Mairan opens a dark wooden cupboard to find his Mimosa plant's leaves wide open; on the right in summer 1962, Jürgen Aschoff checks a bunker chart recorder while helmeted geologist Michel Siffre writes in his logbook beside an underground glacier tent." + QUAL_TAIL,
             {"kind": "FACT", "label": "Human clock: 24 hours, 11 minutes", "who_card": "Franz Halberg (1919–2013) — Romanian-American chronobiologist · Michel Siffre (1939–2024) — French geologist and speleologist", "when_stamp": "1729 · 1832 · 1959 · 15 June 1962 · 16 July 1962", "timeline_step": "1/4 · 1729 (de Mairan's dark cupboard plant) & 2/4 · Jun–Sep 1962 (Aschoff's bunker & Siffre's cave prove the ~24 h 11 min human circadian day)", "hold_s": 3.8}),
            ("02_aschoff_1962_siffre_1962_czeisler_1999_human_free_running_24h11m_actogram_chart", 79.5, 8.0, "E", False, "JUN–SEP 1962 ASCHOFF (ANDECHS BUNKER) & SIFFRE (58-DAY CAVE) + 1999 CZEISLER: INTRINSIC HUMAN CIRCADIAN PERIOD = 24.18 H (24 H 11 MIN)", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked Aschoff (15 June 1962, Science 136: 963–966), Siffre (July–September 1962 Scarasson cave log), and Czeisler et al. (25 June 1999, Science 284: 2177–2181) human free-running actogram & body-temperature rhythm chart shows sleep-wake and core temperature cycles drifting slightly later each day in constant conditions with an intrinsic human period of 24.18 hours (24 h 11 min).",
             {"kind": "DATA", "label": "1962 ASCHOFF BUNKER & SIFFRE 58-DAY CAVE + 1999 CZEISLER: HUMAN INTERNAL PERIOD = 24.18 HOURS (24 H 11 MIN)", "detail": "Inked Aschoff (15 June 1962, Science 136: 963–966), Siffre (July–September 1962 Scarasson cave log), and Czeisler et al. (25 June 1999, Science 284: 2177–2181) human free-running actogram & body-temperature rhythm chart on period paper showing sleep-wake and core temperature cycles drifting slightly later each day in constant conditions with an intrinsic human period of 24.18 hours (24 h 11 min)", "scale": "when Michel Siffre climbed out of his pitch-black alpine cave on the fourteenth of September nineteen sixty-two after fifty-eight days without a watch, his internal body clock had drifted so steadily that he thought it was still the twentieth of August", "hold_s": 3.8}),
            ("03_andechs_1962_bunker_strip_chart_recorder_and_calendar_logbook_closeup", 87.5, 6.5, "B", False, "JUNE 1962 — THE INTERNAL CIRCADIAN DAY", "Fast",
             "Fast: daylight macro shot of a multi-channel paper strip-chart recorder plotting diagonal free-running sleep-wake bars beside a 1962 field notebook and thermometer on a control desk. Nothing emissive, no face.",
             STYLE + "In crisp daylight on a 1962 Bavarian control-room desk, a mechanical strip-chart recorder traces diagonal daily activity bars beside a cloth-bound logbook and a glass mercury thermometer." + FAST_TAIL,
             None),
            ("04_paris_1729_wooden_cupboard_with_potted_mimosa_pudica_leaves_pan", 94.0, 5.5, "C", False, "1729 — DE MAIRAN'S CUPBOARD", "Fast",
             "Fast: daylight close-up pan across an 18th-century carved oak cupboard with its doors ajar revealing a healthy potted Mimosa pudica plant and a quill notebook. Nothing emissive, no face.",
             STYLE + "In bright window light in an 18th-century Parisian study, a carved oak cupboard stands with its doors slightly ajar revealing a potted green Mimosa plant beside a quill pen and inkwell." + FAST_TAIL,
             None),
        ],
    ),
    (
        3,
        "Part 03 — September 1971: Seymour Benzer & Ronald Konopka's Mutant Fruit Flies (The Period Gene) — Midpoint Twist",
        [
            ("01_benzer_and_konopka_sep_1971_caltech_19h_28h_arrhythmic_period_mutant_flies", 99.5, 6.5, "A", False, "ONE GENE SETS THE 24-HOUR DAY", "Quality",
             "Quality: readable faces (physicist-turned-geneticist Seymour Benzer and graduate student Ronald Konopka at Caltech in September 1971 screening Drosophila melanogaster mutants in constant darkness and discovering three single-gene Period mutants running at 19 hours, 28 hours, and 0 hours).",
             STYLE + "Split period scene: on the left in September 1971 at Caltech, Seymour Benzer and Ronald Konopka examine glass vials of fruit flies under a stereo microscope; on the right, three clock dials above three fly vials tick at 19 hours, 28 hours, and a stopped arrhythmic hand." + QUAL_TAIL,
             {"kind": "FACT", "label": "One gene sets the 24-hour day", "when_stamp": "September 1971", "timeline_step": "3/4 · Sep 1971 (Ronald Konopka & Seymour Benzer discover the first clock gene, Period, in Drosophila)", "hold_s": 3.8}),
            ("02_konopka_benzer_sep_1971_pnas_drosophila_per_s_19h_per_l_28h_per_0_x_chromosome_chart", 106.0, 8.0, "E", False, "SEP 1971 KONOPKA & BENZER (PNAS): WILD-TYPE (24 H), PERS (19 H), PERL (28 H) & PER0 (ARRHYTHMIC) ALL MAP TO ONE X-CHROMOSOME GENE (PERIOD)", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked Konopka & Benzer (September 1971, PNAS 68: 2112–2116) Drosophila eclosion & locomotor activity rhythm chart compares wild-type (24.0 h period), per^01 (arrhythmic), per^S (19.0 h period), and per^L1 (28.0 h period) all mapping to a single locus on the X chromosome.",
             {"kind": "DATA", "label": "SEP 1971 KONOPKA & BENZER: 1 X-CHROMOSOME GENE (PERIOD) SETS 24 H (WT), 19 H (PERS), 28 H (PERL) OR ARRHYTHMIC (PER0)", "detail": "Inked Konopka & Benzer (September 1971, PNAS 68: 2112–2116) Drosophila eclosion & locomotor activity rhythm chart on period paper comparing wild-type (24.0 h period), per^01 (arrhythmic), per^S (19.0 h period), and per^L1 (28.0 h period) all mapping to a single locus on the X chromosome", "scale": "changing a single genetic letter inside the Period gene was like turning the regulating screw on the back of a grandfather clock — speeding a fly's entire day up to nineteen hours or slowing it down to twenty-eight", "hold_s": 3.8}),
            ("03_caltech_1971_x_chromosome_linkage_map_and_eclosion_counter_printout_closeup", 114.0, 6.5, "B", False, "SEPTEMBER 1971 — THE FIRST CLOCK GENE", "Fast",
             "Fast: daylight macro shot of a banded giant salivary-gland X-chromosome map print beside three paper actogram strips and glass Drosophila vials on a 1971 Caltech bench. Nothing emissive, no face.",
             STYLE + "In crisp daylight on a 1971 Caltech genetics workbench, a printed X-chromosome band map sits beside three plotted rhythm strips and a rack of glass fruit-fly vials." + FAST_TAIL,
             None),
            ("04_grandfather_clock_regulating_pendulum_nut_and_dna_codon_wheel_model_pan", 120.5, 5.5, "C", False, "19 HOURS · 24 HOURS · 28 HOURS", "Fast",
             "Fast: daylight close-up pan across a brass grandfather-clock pendulum regulating nut beside a carved wooden DNA triplet model on an oak table. Nothing emissive, no face.",
             STYLE + "In bright window light on an oak table, a polished brass clock pendulum with an adjustable regulating nut sits beside a carved wooden DNA helix model." + FAST_TAIL,
             None),
        ],
    ),
    (
        4,
        "Part 04 — 1984–1994 & 2002: Hall, Rosbash & Young Crack the PER/TIM Molecular Hourglass (2017 Nobel Prize) & How Blue Light Resets Your Brain (Melanopsin)",
        [
            ("01_hall_rosbash_young_1984_1994_per_tim_loop_and_berson_8_feb_2002_melanopsin_blue_light", 126.0, 6.5, "A", False, "BLUE LIGHT (480 NM) RESETS YOUR CLOCK", "Quality",
             "Quality: readable faces (geneticists Jeffrey Hall, Michael Rosbash, and Michael Young in October 1984 – 1994 cloning Period and Timeless to solve the 24-hour PER/TIM negative-feedback loop, dissolving to neuroscientist David Berson on 8 February 2002 identifying 480-nm blue-light melanopsin retinal ganglion cells wiring straight to the brain's SCN master clock).",
             STYLE + "Split period scene: on the left, Jeffrey Hall, Michael Rosbash, and Michael Young examine a 24-hour PER/TIM feedback diagram and sequencing gel; on the right in February 2002, David Berson inspects a retinal diagram showing sky-blue light hitting melanopsin ganglion cells wired to the 20,000-neuron SCN clock." + QUAL_TAIL,
             {"kind": "FACT", "label": "Blue light (480 nm) resets your clock", "who_card": "David M. Berson (born 1953) — American neuroscientist", "when_stamp": "October 1984 · February 1990 · March 1994 · 8 February 2002 · 2017", "timeline_step": "4/4 · 1984–1994 & 2002 (Hall, Rosbash & Young solve the PER/TIM feedback hourglass, 2017 Nobel Prize; Berson & Hattar discover 480-nm blue-light melanopsin retinal cells)", "hold_s": 3.8}),
            ("02_hall_rosbash_young_1990_1994_per_tim_dbt_and_berson_2002_480nm_melanopsin_scn_chart", 132.5, 8.0, "E", False, "1984–1994 HALL, ROSBASH & YOUNG (PER/TIM/DBT 24-H LOOP, 2017 NOBEL) & 8 FEB 2002 BERSON: ~480-NM BLUE-LIGHT MELANOPSIN IPRGCS → 20,000-NEURON SCN", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked PER/TIM/DBT feedback loop & melanopsin 480-nm blue-light phase-resetting chart from Bargiello, Jackson & Young (October 1984, Nature 312: 752–754), Zehring et al., Rosbash & Hall (December 1984, Cell 39: 369–376), Hardin, Hall & Rosbash (8 February 1990, Nature 343: 536–540), Vosshall, Price, Sehgal & Young (18 March 1994, Science 263: 1606–1609), and Berson, Dunn & Takao (8 February 2002, Science 295: 1070–1073) shows the 24-hour PER/TIM nuclear negative feedback loop and ~480-nm melanopsin ipRGC signaling to the 20,000-neuron SCN.",
             {"kind": "DATA", "label": "PER/TIM/DBT 24-H FEEDBACK HOURGLASS (1984–1994) & 480-NM BLUE-LIGHT MELANOPSIN RETINAL CELLS → 20,000-NEURON SCN (2002)", "detail": "Inked PER/TIM/DBT feedback loop & melanopsin 480-nm blue-light phase-resetting chart on period paper from Bargiello, Jackson & Young (October 1984, Nature 312: 752–754), Zehring et al., Rosbash & Hall (December 1984, Cell 39: 369–376), Hardin, Hall & Rosbash (8 February 1990, Nature 343: 536–540), Vosshall, Price, Sehgal & Young (18 March 1994, Science 263: 1606–1609), and Berson, Dunn & Takao (8 February 2002, Science 295: 1070–1073) showing the 24-hour PER/TIM nuclear negative feedback loop and ~480-nm melanopsin ipRGC signaling to the 20,000-neuron SCN", "scale": "staring at a bright blue phone screen at midnight hits your retina with four-hundred-and-eighty-nanometre sky-blue light — fooling the twenty thousand clock neurons at the base of your brain into thinking dawn has just broken", "hold_s": 3.8}),
            ("03_anatomical_eye_retina_model_and_scn_clock_dial_with_blue_prism_filter_closeup", 140.5, 6.5, "B", False, "8 FEBRUARY 2002 — HOW BLUE LIGHT RESETS YOUR BRAIN", "Fast",
             "Fast: daylight macro shot of a painted anatomical eye and retina model beside a blue-tinted glass optical filter and a 24-hour brass clock dial on a workbench. Nothing emissive, no face.",
             STYLE + "In crisp daylight on a neuroscience bench, a painted anatomical model of the human eye and optic nerve sits beside a sky-blue glass optical filter and a 24-hour brass dial." + FAST_TAIL,
             None),
            ("04_explorer_resetting_20000_neuron_scn_master_clock_dial_with_blue_optical_prism", 147.0, 5.5, "B", True, None, "Quality",
             "Quality: Explorer beat 2 (locked character reference).",
             STYLE + "Standing beside a large brass retinal lens and a 24-hour master clock dial, the Explorer slides a sky-blue glass prism into a beam of morning window light and watches the brass clock hands snap cleanly into alignment with sunrise." + EXP_TAIL,
             None),
        ],
    ),
    (
        5,
        "Part 05 — Why Jet Lag Happens When Your Organ Clocks Split Apart — & How Your Muscles Turn Food Into Motion",
        [
            ("01_timeline_1729_2017_and_scn_vs_liver_gut_jet_lag_desynchrony_chart", 152.5, 8.5, "E", False, "1729–2017 TIMELINE · DE MAIRAN CUPBOARD, ASCHOFF BUNKER, KONOPKA & BENZER PERIOD GENE, HALL/ROSBASH/YOUNG PER/TIM & BERSON MELANOPSIN", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, the 4-date timeline completes: 1729 (Jean-Jacques d'Ortous de Mairan proves a Mimosa plant in a pitch-black Paris cupboard still opens and closes its leaves on a daily cycle) · Jun–Sep 1962 (Jürgen Aschoff's Andechs bunker & Michel Siffre's alpine cave prove humans have an endogenous ~24.2-hour circadian rhythm, refined to 24 h 11 min by Czeisler 1999) · Sep 1971 (Ronald Konopka & Seymour Benzer at Caltech discover the first single-gene clock mutants — 19 h, 28 h, and arrhythmic — in the Drosophila Period gene) · 1984–1994 & 2002 (Jeffrey Hall, Michael Rosbash & Michael Young clone Period and Timeless and solve the PER/TIM negative-feedback hourglass, winning the 2017 Nobel Prize; David Berson & Samer Hattar identify 480-nm blue-light melanopsin retinal cells in 2002).",
             {"kind": "DATA", "label": "1729–2017 CIRCADIAN CLOCK TIMELINE · LIGHT-RESET BRAIN SCN CLOCK VS MEAL-RESET LIVER & GUT CLOCKS (JET LAG)", "detail": "Animated 4-date timeline (1729 → 2017) alongside the brain SCN vs peripheral organ (liver, gut, muscle) jet-lag resynchronization diagram", "scale": "from a sensitive houseplant locked in a dark Paris cupboard to a twenty-four-hour protein hourglass inside every cell, three centuries of science revealed how living things keep time with the turning Earth", "when_stamp": "1729–2017", "timeline_step": "4/4 · 1729–2017 timeline complete", "hold_s": 3.8}),
            ("02_two_world_time_zone_clocks_london_and_new_york_beside_anatomical_liver_model_pan", 161.0, 5.5, "A", False, "BRAIN CLOCK VS LIVER & GUT CLOCKS", "Fast",
             "Fast: daylight close-up of two brass world-time clocks set to London and New York beside a painted anatomical model of the brain and liver on a wooden museum plinth. Nothing emissive, no face.",
             STYLE + "In crisp daylight on a wooden museum plinth, two brass world-time dials set five hours apart sit beside a painted anatomical model of the brain and liver." + FAST_TAIL,
             None),
            ("03_lohmann_1929_atp_szent_gyorgyi_1942_threads_and_huxleys_22_may_1954_sliding_filaments_handoff", 166.5, 6.5, "C", False, "ATP & SLIDING MUSCLE FILAMENTS", "Quality",
             "Quality: readable faces (Albert Szent-Györgyi in 1942 dripping ATP onto rabbit actomyosin threads that contract in a dish, alongside Hugh Huxley and Andrew Huxley on 22 May 1954 proving the Sliding Filament Theory of muscle contraction — handoff to 062 Muscles, ATP & the Sliding Filament Motor).",
             STYLE + "Split period scene: on the left in 1942 Szeged, Albert Szent-Györgyi drips ATP solution onto a protein thread in a glass dish and watches it contract; on the right on 22 May 1954, Hugh Huxley and Andrew Huxley inspect sarcomere micrographs showing thick myosin hands pulling thin actin ropes." + QUAL_TAIL,
             {"kind": "WHEN", "label": "AUGUST 1929 · 1942 · 22 MAY 1954", "hold_s": 3.5}),
            ("04_table_three_callback", 173.0, 2.4, "C", False, None, "reuse",
             "Reuse: verified unused moving window [5.50s..7.90s] of P1:07_table_three_props_1729_mimosa_pot_1962_bunker_strip_chart_and_1971_caltech_fly_tubes (callback, £0).",
             "Reuse P1:07_table_three_props_1729_mimosa_pot_1962_bunker_strip_chart_and_1971_caltech_fly_tubes [5.50s..7.90s] (2.40s distinct non-overlapping tail window from 8.00s source clip).",
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
                row["reuse_of"] = "P1:07_table_three_props_1729_mimosa_pot_1962_bunker_strip_chart_and_1971_caltech_fly_tubes"
                row["reuse_window_s"] = [5.5, 7.9]
                row["reuse_audit"] = {
                    "source_row": "P1:07_table_three_props_1729_mimosa_pot_1962_bunker_strip_chart_and_1971_caltech_fly_tubes",
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
            "film": "061_deMairan-Aschoff-Benzer-Hall-Rosbash-Young-Circadian-Clock",
            "part": p_idx,
            "title": p_title,
            "version": "v01",
            "timing_status": "pre_vo_script_clock (built from circadian_script_master_v01.md; retimes onto Scribe STT once VO locks)",
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
        "film": "061_deMairan-Aschoff-Benzer-Hall-Rosbash-Young-Circadian-Clock",
        "version": "v01",
        "date": "2026-10-19",
        "owner": "gemini (J0631)",
        "status": "PRE_VO_BOARDS_V01_NO_MINT",
        "generation_authorized": False,
        "script": "00_Brand/Channel-Setup/ideas/061_deMairan-Aschoff-Benzer-Hall-Rosbash-Young-Circadian-Clock/circadian_script_master_v01.md",
        "sources": "00_Brand/Channel-Setup/ideas/061_deMairan-Aschoff-Benzer-Hall-Rosbash-Young-Circadian-Clock/SOURCES_v01.md",
        "credit_snapshot": {
            "flow_balance": 23740,
            "flow_floor": 0,
            "flow_read_at": "2026-10-15T21:42:22Z",
            "vertex_promo_gbp": 71.02,
            "vertex_usable_gbp": 70.02,
        },
        "totals": totals,
        "per_part": per_part_summary,
        "mint_order": "006 > 007 > 008 > 009 > 010 > 011 > 012 > 013 > 014 > 015 > 016 > 017 > 018 > 019 > 020 > 021 > 022 > 023 > 024 > 025 > 026 > 027 > 028 > 029 > 030 > 031 > 032 > 033 > 034 > 035 > 036 > 037 > 038 > 039 > 040 > 041 > 042 > 043 > 044 > 045 > 046 > 047 > 048 > 049 > 050 > 051 > 052 > 053 > 054 > 055 > 056 > 057 > 058 > 059 > 060 > 061 > 062. Nothing in 061 is generation_authorized.",
    }
    (EDIT / "PICTURE_PLAN_v01.json").write_text(json.dumps(plan, indent=2) + "\n")

    sl = [
        "# 061 The Circadian Clock: The 24-Hour Timer Inside Your Cells — Shot list & plate boards v01 (pre-VO)",
        "",
        "Gemini, 19 Oct 2026, J0631. Built from `circadian_script_master_v01.md` (`91.9 PASS`) and `SOURCES_v01.md`.",
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
        "# 061 price review v01 (pre-VO plate boards)",
        "",
        "Gemini, 19 Oct 2026, J0631. Boards only. **No mint. No spend. No merge.**",
        "Prepared from `circadian_script_master_v01.md` (`91.9 PASS`) and `SOURCES_v01.md` so 061's full plate board rows, non-emissive Fast prompts, £0 code graphics, and Teach-on-Screen overlays are ready to re-time the moment long VO locks. Parked for Chief.",
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
        f"- **Quality ({totals['Quality']} rows):** readable faces (Jean-Jacques d'Ortous de Mairan, Jürgen Aschoff, Franz Halberg, Michel Siffre, Seymour Benzer, Ronald J. Konopka, Jeffrey C. Hall, Michael Rosbash, Michael W. Young, David M. Berson, Albert Szent-Györgyi, Hugh Huxley, Andrew Huxley), 1729 Paris dark-cupboard *Mimosa* experiment & June–September 1962 Andechs bunker / Scarasson alpine cave isolation, September 1971 Caltech *Drosophila* `Period` mutant discovery, 1984–1994 `PER/TIM` feedback hourglass & 2002 `480-nm` blue-light melanopsin retinal cells, and the 2 Explorer beats.",
        f"- **Fast ({totals['Fast']} rows, non-emissive):** daylight prop and laboratory shots (open brass pocket watch, sand hourglass, potted *Mimosa* & glass *Drosophila* vial pan, 3-object callback bench, 1962 Bavarian strip-chart recorder & thermometer, 1729 carved oak cupboard with potted *Mimosa* & quill notebook, 1971 X-chromosome band map & plotted actogram strips, brass grandfather-clock pendulum nut & wooden DNA helix model, painted anatomical eye/retina model & sky-blue glass filter, two brass world-time clocks & brain/liver model on museum plinth). Zero candles, flames, sparks, or glowing elements on Fast.",
        f"- **£0 code graphics ({totals['code_graphic']} rows):**",
        "  1. `P1:04_de_mairan_1729_aschoff_1962_konopka_benzer_1971_24h11m_and_period_mutants_chart` — wild-type 24-hour rhythm, human free-running bunker period (`24 h 11 min`), and Konopka & Benzer's September 1971 single-gene `Period` mutants (`perS` 19 h, `perL` 28 h, `per0` arrhythmic) (`SCALE: without morning sunlight to reset your eyes, the natural clock inside a human body runs about twenty-four hours and eleven minutes long — drifting eleven minutes later every single day like a pocket watch that runs slightly slow`)",
        "  2. `P1:06_hall_rosbash_young_1990_1994_per_tim_ttfl_molecular_hourglass_oscillation_chart` — Hardin, Hall & Rosbash (1990 *Nature*) and Vosshall, Price, Sehgal & Young (1994 *Science*) 24-hour `PER/TIM` transcription-translation negative feedback loop curve (`SCALE: every cell in your body tells time like an old sand hourglass — spending twelve hours trickling PER and TIM protein grains into a pile until at midnight the pile tips over, shuts off the tap, and takes twelve hours to drain away`)",
        "  3. `P2:02_aschoff_1962_siffre_1962_czeisler_1999_human_free_running_24h11m_actogram_chart` — Aschoff (15 June 1962 *Science*), Siffre (1962 Scarasson cave log), and Czeisler et al. (25 June 1999 *Science*) human free-running actogram & body-temperature rhythm chart (`24.18 h = 24 h 11 min`) (`SCALE: when Michel Siffre climbed out of his pitch-black alpine cave on the fourteenth of September nineteen sixty-two after fifty-eight days without a watch, his internal body clock had drifted so steadily that he thought it was still the twentieth of August`)",
        "  4. `P3:02_konopka_benzer_sep_1971_pnas_drosophila_per_s_19h_per_l_28h_per_0_x_chromosome_chart` — Konopka & Benzer (September 1971, *PNAS*) *Drosophila* eclosion & locomotor activity rhythm chart mapping `perS` (19 h), `perL` (28 h), and `per0` to the X-chromosome `Period` locus (`SCALE: changing a single genetic letter inside the Period gene was like turning the regulating screw on the back of a grandfather clock — speeding a fly's entire day up to nineteen hours or slowing it down to twenty-eight`)",
        "  5. `P4:02_hall_rosbash_young_1990_1994_per_tim_dbt_and_berson_2002_480nm_melanopsin_scn_chart` — Hall, Rosbash & Young (1984–1994) `PER/TIM/DBT` nuclear negative feedback loop and Berson, Dunn & Takao (8 February 2002 *Science*) `~480-nm` blue-light melanopsin `ipRGC` signaling to the 20,000-neuron SCN (`SCALE: staring at a bright blue phone screen at midnight hits your retina with four-hundred-and-eighty-nanometre sky-blue light — fooling the twenty thousand clock neurons at the base of your brain into thinking dawn has just broken`)",
        "  6. `P5:01_timeline_1729_2017_and_scn_vs_liver_gut_jet_lag_desynchrony_chart` — completed 4-date timeline (1729 → 2017) + brain SCN vs liver/gut peripheral clock jet-lag resynchronization diagram (`SCALE: from a sensitive houseplant locked in a dark Paris cupboard to a twenty-four-hour protein hourglass inside every cell, three centuries of science revealed how living things keep time with the turning Earth`)",
        f"- **£0 verified reuse ({totals['reuse']} row):** `P5:04_table_three_callback` uses the 2.40 s unused moving tail `[5.50s..7.90s]` of `P1:07_table_three_props_1729_mimosa_pot_1962_bunker_strip_chart_and_1971_caltech_fly_tubes`.",
        "",
        "## Mint order",
        "",
        "006 > 007 > 008 > 009 > 010 > 011 > 012 > 013 > 014 > 015 > 016 > 017 > 018 > 019 > 020 > 021 > 022 > 023 > 024 > 025 > 026 > 027 > 028 > 029 > 030 > 031 > 032 > 033 > 034 > 035 > 036 > 037 > 038 > 039 > 040 > 041 > 042 > 043 > 044 > 045 > 046 > 047 > 048 > 049 > 050 > 051 > 052 > 053 > 054 > 055 > 056 > 057 > 058 > 059 > 060 > 061 > 062. `generation_authorized` is `false` on every row.",
    ])
    (EDIT / "PRICE_REVIEW_v01.md").write_text("\n".join(pr_lines) + "\n")
    print(f"061 v01 boards written: {totals['rows']} rows, Flow expected={totals['flow_credits_expected']}")


if __name__ == "__main__":
    main()
