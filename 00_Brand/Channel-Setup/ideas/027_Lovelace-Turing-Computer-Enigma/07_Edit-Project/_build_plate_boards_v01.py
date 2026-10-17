#!/usr/bin/env python3
"""HOS 027 (Breaking Enigma: How a Paper Tape Invented the Computer) pre-VO plate boards v01. J0463. No mint, no spend.

Built from 00_Brand/Channel-Setup/ideas/027_Lovelace-Turing-Computer-Enigma/turing_script_master_v01.md
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
        "Part 01 — The Brass Loom, the Paper Tape, and 159 Quintillion Keys",
        [
            ("01_lovelace_punched_card_turing_tape_and_bombe_1843_1940", 0.0, 5.5, "A", False, "CARDS, TAPE, ENIGMA", "Quality",
             "Quality: Short frame 0 / answer image (0:03) + Ada Lovelace in a candlelit London study in August 1843 tracing a Jacquard punched card beside Babbage's brass gears, morphing into Alan Turing's 1936 paper tape and the spinning bronze drums of the 1940 Bletchley Park Bombe.",
             STYLE + "In a warm candlelit London study in August 1843, mathematician Ada Lovelace traces a perforated pasteboard card beside brass Analytical Engine gearwheels, which ripple into a strip of paper tape and the spinning bronze drums of the Bletchley Park Bombe." + QUAL_TAIL,
             {"kind": "WHEN", "label": "LONDON, AUGUST 1843 · BLETCHLEY PARK, 18 MARCH 1940", "timeline_step": "1/6 · Aug 1843 (Lovelace publishes Note G algorithm for Babbage's Analytical Engine)", "hold_s": 3.5}),
            ("02_lovelace_cards_turing_tape_enigma_bombe_split", 5.5, 6.0, "B", False, "ONE UNIVERSAL MACHINE", "Quality",
             "Quality: three-panel period composition (Ada Lovelace's 1843 punched cards and brass gears on the left; Turing's 1936 paper-tape scanner in the centre; an Enigma rotor box wired to the Bletchley Park Bombe on the right).",
             STYLE + "Three-panel period composition: on the left, chained Jacquard punched cards feed into brass gearwork; in the centre, a mechanical read-write head steps along a paper strip; on the right, a three-rotor cipher machine connects by copper cables to spinning bronze drums." + QUAL_TAIL,
             None),
            ("03_babbage_and_herschel_1821_nautical_tables_by_steam", 11.5, 6.0, "C", False, "CALCULATIONS BY STEAM", "Quality",
             "Quality: readable faces (Charles Babbage and astronomer John Herschel in London in 1821 comparing hand-copied nautical tables covered in red ink corrections beside a stormy sea chart).",
             STYLE + "London, 1821: inventor Charles Babbage and astronomer John Herschel sit across a mahogany table strewn with bound nautical ledgers and a brass sextant, as Babbage strikes the table in frustration." + QUAL_TAIL,
             {"kind": "WHO", "label": "Charles Babbage (1791–1871) — English mathematician and inventor · John Herschel (1792–1871) — English mathematician and astronomer", "when_stamp": "London, 1821", "hold_s": 3.8}),
            ("04_lovelace_1843_note_g_and_turing_1936_universal_machine_chart", 17.5, 8.0, "E", False, "1843 NOTE G · 1936 UNIVERSAL TAPE", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked architecture comparison shows Babbage & Lovelace's August 1843 Analytical Engine (Punched Cards → 'Store' memory of 1,000 fifty-digit numbers ↔ 'Mill' processor computing Bernoulli number B₇ via nested loops) alongside Alan Turing's 28 May 1936 Universal Computing Machine (single tape of 0s and 1s holding both program and data).",
             {"kind": "DATA", "label": "1843 ANALYTICAL ENGINE (STORE + MILL) → 1936 UNIVERSAL TURING TAPE", "detail": "Inked architecture comparison on period paper showing Babbage & Lovelace's 1843 Analytical Engine (Punched Cards → 'Store' memory of 1,000 fifty-digit numbers ↔ 'Mill' processor with conditional branching) and Turing's 1936 Universal Machine", "scale": "Lovelace wrote a working computer program with nested loops a full 100 years before the first electronic computer was ever switched on", "who_card": "Ada Lovelace (1815–1852) — English mathematician · Alan Turing (1912–1954) — British mathematician and logician", "when_stamp": "August 1843 · 28 May 1936", "timeline_step": "2/6 · 28 May 1936 (Turing submits 'On Computable Numbers' / Universal Machine)", "hold_s": 3.8}),
            ("05_three_enigma_rotors_and_plugboard_cables_pan", 25.5, 5.5, "A", False, "THREE ROTORS + PLUGBOARD", "Fast",
             "Fast: daylight pan across three notched brass-and-ebonite Enigma scrambler rotors and ten braided plugboard patch cables on an oak workbench between code graphics so two full-frame graphics never run back to back. Nothing emissive.",
             STYLE + "In soft daylight on an oak table, the camera tracks across three brass-ringed cipher rotors with 26 spring-loaded electrical contacts beside braided cloth plugboard cables." + FAST_TAIL,
             None),
            ("06_159_quintillion_enigma_keys_vs_20_min_bombe_chart", 31.0, 8.0, "E", False, "159 QUINTILLION KEYS", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period parchment, an inked combinatorics chart multiplies Enigma's 3 rotor choices (60), 26³ rotor positions (17,576), and 10 plugboard cables (150,738,274,937,250) into 158,962,555,217,826,360,000 (~159 quintillion) settings — then slashes them to the daily key in under 20 minutes via Turing's closed electrical loop.",
             {"kind": "DATA", "label": "60 × 17,576 × 1.507×10¹⁴ = 158,962,555,217,826,360,000 KEYS → <20 MIN", "detail": "Inked scale chart of 158,962,555,217,826,360,000 (159 quintillion) Enigma settings vs Turing's 20-minute Bombe electrical sieve", "scale": "159 quintillion possible keys — twenty million times more combinations than there are grains of sand on all the beaches of Earth", "hold_s": 3.8}),
            ("07_table_three_props_jacquard_card_paper_tape_enigma_rotor", 39.0, 5.5, "C", False, "BLETCHLEY PARK, MARCH 1940", "Fast",
             "Fast: daylight prop table (callback source for Part 05: perforated Jacquard pasteboard card, coiled paper tape strip, brass Enigma scrambler rotor beside a Bombe drum). Nothing emissive.",
             STYLE + "On a wooden desk in soft window light sit three objects side by side: a perforated cream pasteboard loom card, a coiled strip of paper tape with square holes, and a brass cipher rotor wheel beside a bronze Bombe drum." + FAST_TAIL,
             None),
            ("08_explorer_pressing_enigma_key_self_encryption_flaw", 62.0, 5.5, "A", True, None, "Quality",
             "Quality: Explorer beat 1 (locked character reference, after 1:00).",
             STYLE + "Standing beside a wooden cipher box and a spinning bronze drum, the Explorer presses a metal key down, traces the copper wire path through three brass rotors and the reversing reflector, and points in triumph at the unlit first lamp on the lampboard." + EXP_TAIL,
             None),
            ("09_perforated_jacquard_card_sliding_over_brass_pins", 67.5, 5.5, "B", False, "PUNCHED PASTEBOARD CARD", "Fast",
             "Fast: daylight macro shot of a perforated Jacquard pasteboard card pressing against a row of spring-loaded brass feeler pins that selectively lift and block steel hooks. Nothing emissive, no face.",
             STYLE + "In crisp daylight, a perforated pasteboard card presses smoothly against a row of spring-loaded brass feeler pins: pins meeting holes pass straight through while pins meeting solid card push back." + FAST_TAIL,
             None),
        ],
    ),
    (
        2,
        "Part 02 — The Poet's Daughter and the Brass Loom",
        [
            ("01_ada_lovelace_1833_babbage_gears_and_jacquard_loom", 73.0, 6.5, "A", False, "THE SILK LOOM CARDS", "Quality",
             "Quality: readable face (seventeen-year-old Ada Byron, later Countess of Lovelace, examining Charles Babbage's brass gearwork in London on 5 June 1833 and studying Joseph Marie Jacquard's 1804 silk-weaving punched cards).",
             STYLE + "London, 5 June 1833: young Ada Byron in a Regency silk gown leans closely over a polished brass column of meshing number gears, then holds up a chain of perforated Jacquard loom cards." + QUAL_TAIL,
             {"kind": "WHO", "label": "Joseph Marie Jacquard (1752–1834) — French weaver and inventor", "when_stamp": "1804 · 5 June 1833 · 1834", "hold_s": 3.8}),
            ("02_lovelace_august_1843_note_g_bernoulli_b7_trace_table", 79.5, 8.0, "E", False, "NOTE G · BERNOULLI NUMBER B₇", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked trace table reproduces Ada Lovelace's August 1843 Note G algorithm calculating the seventh Bernoulli number (B₇) across variables V₁ through V₁₃ using arithmetic operations and two nested conditional-branching loops on Babbage's Mill and Store.",
             {"kind": "DATA", "label": "AUGUST 1843 NOTE G · VARIABLES V₁–V₁₃ & 2 NESTED LOOPS → B₇", "detail": "Inked trace table on period paper of Ada Lovelace's August 1843 Note G algorithm calculating the Bernoulli number B₇ using variables V₁–V₁₃ and two nested branching loops", "scale": "41 pages of visionary notes written in 1843 — programming nested loops for a machine whose brass gears still hadn't been built", "who_card": "Luigi Menabrea (1809–1896) — Italian military engineer and mathematician", "fact_card": "Notes 3× longer than paper", "when_stamp": "October 1842 · August 1843", "hold_s": 3.8}),
            ("03_lovelace_note_a_weaving_algebra_and_music_1843", 87.5, 6.5, "B", False, "SYMBOLS, MUSIC, LOGIC", "Quality",
             "Quality: readable face (Countess Ada Lovelace at her London writing desk in August 1843 as punched-card holes rise from her quill page and transform into brass musical notes and logical symbols).",
             STYLE + "London, August 1843: Countess Ada Lovelace writes with a quill pen beside a stack of perforated cards as carved brass musical notes and geometric logic symbols rise gracefully above the Analytical Engine." + QUAL_TAIL,
             None),
            ("04_analytical_engine_brass_store_columns_and_mill_pan", 94.0, 5.5, "C", False, "THE STORE AND THE MILL", "Fast",
             "Fast: daylight pan across Babbage's vertical stacks of meshing brass figure wheels in the Analytical Engine 'Mill' and 'Store'. Nothing emissive, no face.",
             STYLE + "In crisp window light, the camera glides past tall vertical columns of interlocking brass gearwheels and racks inside Babbage's mechanical engine." + FAST_TAIL,
             None),
        ],
    ),
    (
        3,
        "Part 03 — The Imaginary Paper Tape That Broke Mathematics",
        [
            ("01_turing_cambridge_1936_and_hilbert_decision_problem", 99.5, 6.5, "A", False, "CAMBRIDGE · 28 MAY 1936", "Quality",
             "Quality: readable faces (German mathematician David Hilbert posing the 1928 Entscheidungsproblem, and twenty-three-year-old Alan Turing at King's College, Cambridge in May 1936 sketching an infinite paper tape).",
             STYLE + "King's College, Cambridge, May 1936: twenty-three-year-old Alan Turing in a tweed jacket sits by a leaded window, sketching a long strip of squared paper tape while a portrait of bearded mathematician David Hilbert looks on." + QUAL_TAIL,
             {"kind": "WHO", "label": "David Hilbert (1862–1943) — German mathematician", "fact_card": "Proved some maths unsolvable", "when_stamp": "1928 · Cambridge, 28 May 1936", "hold_s": 3.8}),
            ("02_turing_1936_universal_machine_and_halting_problem_diagram", 106.0, 8.0, "E", False, "STORED-PROGRAM TAPE · HALTING PROOF", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked schematic shows Turing's 28 May 1936 Universal Computing Machine (U) scanning a single paper tape holding both the encoded rule-table of any machine M and its data bits, alongside the self-referential Halting Problem contradiction matrix proving no algorithm can decide whether an arbitrary program halts.",
             {"kind": "DATA", "label": "UNIVERSAL TAPE (PROGRAM + DATA IN 0S & 1S) + HALTING CONTRADICTION", "detail": "Inked diagram on period paper of Turing's 1936 Universal Machine tape (Instruction bits + Data bits on the same strip of 0s and 1s) alongside the self-referential Halting Problem contradiction matrix", "scale": "one rule-table small enough to write on a postcard can simulate every piece of software humanity will ever write", "hold_s": 3.8}),
            ("03_paper_tape_morphing_into_modern_stored_program_memory", 114.0, 6.5, "B", False, "ONE MACHINE FOR EVERYTHING", "Fast",
             "Fast: daylight tabletop view of a mechanical read-write head stepping across a paper tape strip beside a clean cutaway silicon memory wafer and brass gear linkage. Nothing emissive, no face.",
             STYLE + "In crisp daylight, a brass read-write head steps smoothly from square to square along a white paper tape beside a polished silicon memory wafer." + FAST_TAIL,
             None),
            ("04_cambridge_fountain_pen_and_typewriter_manuscript_bench", 120.5, 5.5, "C", False, "ON COMPUTABLE NUMBERS", "Fast",
             "Fast: daylight close-up of a 1930s mechanical typewriter and fountain pen beside a bound mathematical offprint on an oak desk in King's College. Nothing emissive, no face.",
             STYLE + "In soft daylight on an oak study desk, a black 1930s mechanical typewriter sits beside a fountain pen, a brass inkwell, and a stack of cream manuscript pages." + FAST_TAIL,
             None),
        ],
    ),
    (
        4,
        "Part 04 — 159 Quintillion Keys and Enigma's Fatal Flaw — Midpoint Twist",
        [
            ("01_rejewski_warsaw_1932_and_pyry_handover_25_july_1939", 126.0, 6.5, "A", False, "THE POLISH HANDOVER", "Quality",
             "Quality: readable face (Polish mathematician Marian Rejewski in spectacles handing his replica Enigma machine and wiring sheets to British cryptologists at Pyry near Warsaw on 25 July 1939).",
             STYLE + "Pyry forest near Warsaw, 25 July 1939: Polish mathematician Marian Rejewski in round spectacles opens a wooden crate to reveal a reconstructed military cipher machine and hands folded wiring diagrams to British intelligence officers." + QUAL_TAIL,
             {"kind": "WHO", "label": "Marian Rejewski (1905–1980) — Polish mathematician and cryptologist", "when_stamp": "December 1932 · 25 July 1939", "timeline_step": "3/6 · 25 Jul 1939 (Rejewski & Polish Cipher Bureau hand Enigma replicas to Britain)", "hold_s": 3.8}),
            ("02_turing_welchman_wettervorhersage_crib_loop_diagram", 132.5, 8.0, "E", False, "CRIB LOOP + DIAGONAL BOARD (<20 MIN)", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked electrical-loop circuit shows how matching a 16-letter guessed plaintext 'crib' (WETTERVORHERSAGE) against Enigma ciphertext — exploiting the reflector flaw that no letter can EVER encrypt to itself — forms a closed electrical loop across 36 spinning Bombe drum triplets and Gordon Welchman's diagonal board, rejecting 99.9999% of contradictory settings at the speed of electricity.",
             {"kind": "DATA", "label": "16-LETTER CRIB LOOP + DIAGONAL BOARD → REJECTS CONTRADICTIONS IN MS", "detail": "Inked electrical-loop diagram on period paper showing how matching a 16-letter 'WETTERVORHERSAGE' crib against ciphertext (where no letter can equal itself) forms a closed electrical loop across 36 spinning Bombe drum triplets", "scale": "what would take a human clerk millions of years by hand flashed through Welchman's diagonal board in milliseconds", "who_card": "Gordon Welchman (1906–1985) — British mathematician", "fact_card": "A letter never became itself", "when_stamp": "18 March 1940 · August 1940", "timeline_step": "4/6 · 18 Mar 1940 (First Bombe 'Victory' installed at Bletchley Park)", "hold_s": 3.8}),
            ("03_bombe_victory_stopping_on_key_bletchley_hut_8", 140.5, 6.5, "B", False, "CRACKED IN 20 MINUTES", "Quality",
             "Quality: readable faces (Alan Turing and Wrens in Hut 8 at Bletchley Park in 1940 watching the spinning bronze drums of the Bombe 'Victory' snap to a halt on a valid daily Enigma key).",
             STYLE + "Hut 8, Bletchley Park, 1940: Alan Turing and two Wrens in naval uniform watch rows of spinning bronze Bombe drums click sharply to a halt, then read the aligned rotor letters from the indicator dials." + QUAL_TAIL,
             None),
            ("04_explorer_diagonal_board_cascade_single_glowing_lamp", 147.0, 5.5, "B", True, None, "Quality",
             "Quality: Explorer beat 2 (locked character reference).",
             STYLE + "Standing in front of a wooden criss-cross wiring board with twenty-six small glass bulbs, the Explorer plugs a copper jumper lead into a socket, watches twenty-five bulbs snap dark in a fast cascade, and points to the single warm bulb left glowing." + EXP_TAIL,
             None),
        ],
    ),
    (
        5,
        "Part 05 — The Secret Kept for 30 Years and Your Digital World",
        [
            ("01_timeline_1843_2013_and_84000_messages_impact_chart", 152.5, 8.5, "E", False, "84,000 MESSAGES/MONTH · SAVED ~14M LIVES", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, the 6-date timeline completes: Aug 1843 (Lovelace Note G) · 28 May 1936 (Turing Universal Machine) · 25 Jul 1939 (Polish Pyry handover) · 18 Mar 1940 (Bletchley Bombe 'Victory') · Oct 1950 (Turing Test paper) · 7 Jun 1954 & 24 Dec 2013 (Turing dies at 41; Royal Pardon), alongside an inked Bletchley Park wartime impact chart (~84,000 messages decoded/month, shortening WWII in Europe by 2–4 years).",
             {"kind": "DATA", "label": "~84,000 MESSAGES/MONTH → SHORTENED WWII BY 2–4 YEARS (~14M LIVES)", "detail": "Animated 6-date timeline (Aug 1843 → 24 Dec 2013) alongside an inked Bletchley Park impact chart (~84,000 Enigma messages decoded/month, shortening WWII in Europe by an estimated 2–4 years and saving ~14 million lives)", "scale": "~84,000 intercepted Enigma messages decoded every month at Bletchley Park — shortening World War II in Europe by an estimated 2 to 4 years and saving ~14 million lives", "fact_card": "Kept secret until 1974", "when_stamp": "February 1946 · October 1950 · March 1952 · 7 June 1954 · 1974 · 24 December 2013", "timeline_step": "5/6 · Oct 1950 (Turing Test) & 6/6 · 7 Jun 1954 / 24 Dec 2013 (Death & Royal Pardon)", "hold_s": 3.8}),
            ("02_turing_1946_ace_blueprints_and_1950_mind_paper_bench", 161.0, 5.5, "A", False, "CAN MACHINES THINK?", "Fast",
             "Fast: daylight pan across Turing's February 1946 ACE computer circuit schematics and a 1950 philosophical journal beside a modern silicon processor wafer on an oak desk. Nothing emissive, no face.",
             STYLE + "In crisp daylight on an oak desk, rolled engineering blueprints and vacuum-tube delay-line tubes sit beside a bound philosophical journal and a gleaming silicon processor wafer." + FAST_TAIL,
             None),
            ("03_landsteiner_vienna_1900_6x6_blood_slides_handoff", 166.5, 6.5, "C", False, "WHY BLOOD CLUMPS", "Quality",
             "Quality: readable face (thirty-one-year-old Karl Landsteiner in Vienna in February 1900 pipetting serum onto a 6 × 6 grid of red blood drops on glass slides beside Richard Lewisohn's 1915 bottle of citrated blood — handoff to 028 Landsteiner Blood Types).",
             STYLE + "Vienna, February 1900: pathologist Karl Landsteiner in a white laboratory coat pipettes clear golden serum onto a six-by-six grid of red blood drops on glass slides beside a chilled glass bottle of citrated blood." + QUAL_TAIL,
             {"kind": "WHEN", "label": "FEBRUARY 1900 · JANUARY 1915", "hold_s": 3.5}),
            ("04_table_three_callback", 173.0, 2.4, "C", False, None, "reuse",
             "Reuse: verified unused moving window [5.50s..7.90s] of P1:07_table_three_props_jacquard_card_paper_tape_enigma_rotor (callback, £0).",
             "Reuse P1:07_table_three_props_jacquard_card_paper_tape_enigma_rotor [5.50s..7.90s] (2.40s distinct non-overlapping tail window from 8.00s source clip).",
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
                row["reuse_of"] = "P1:07_table_three_props_jacquard_card_paper_tape_enigma_rotor"
                row["reuse_window_s"] = [5.5, 7.9]
                row["reuse_audit"] = {
                    "source_row": "P1:07_table_three_props_jacquard_card_paper_tape_enigma_rotor",
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
            "film": "027_Lovelace-Turing-Computer-Enigma",
            "part": p_idx,
            "title": p_title,
            "version": "v01",
            "timing_status": "pre_vo_script_clock (built from turing_script_master_v01.md; retimes onto Scribe STT once VO locks)",
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
        "film": "027_Lovelace-Turing-Computer-Enigma",
        "version": "v01",
        "date": "2026-10-17",
        "owner": "gemini (J0463)",
        "status": "PRE_VO_BOARDS_V01_NO_MINT",
        "generation_authorized": False,
        "script": "00_Brand/Channel-Setup/ideas/027_Lovelace-Turing-Computer-Enigma/turing_script_master_v01.md",
        "sources": "00_Brand/Channel-Setup/ideas/027_Lovelace-Turing-Computer-Enigma/SOURCES_v01.md",
        "credit_snapshot": {
            "flow_Balance": 23740,
            "flow_floor": 0,
            "flow_read_at": "2026-10-15T21:42:22Z",
            "vertex_promo_gbp": 71.02,
            "vertex_usable_gbp": 70.02,
        },
        "totals": totals,
        "per_part": per_part_summary,
        "mint_order": "006 > 007 > 008 > 009 > 010 > 011 > 012 > 013 > 014 > 015 > 016 > 017 > 018 > 019 > 020 > 021 > 022 > 023 > 024 > 025 > 026 > 027. Nothing in 027 is generation_authorized.",
    }
    (EDIT / "PICTURE_PLAN_v01.json").write_text(json.dumps(plan, indent=2) + "\n")

    sl = [
        "# 027 Breaking Enigma: How a Paper Tape Invented the Computer — Shot list & plate boards v01 (pre-VO)",
        "",
        "Gemini, 17 Oct 2026, J0463. Built from `turing_script_master_v01.md` (94.3 PASS) and `SOURCES_v01.md`.",
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
        "# 027 price review v01 (pre-VO plate boards)",
        "",
        "Gemini, 17 Oct 2026, J0463. Boards only. **No mint. No spend. No merge.**",
        "Prepared from `turing_script_master_v01.md` (94.3 PASS) and `SOURCES_v01.md` so 027's full plate board rows, non-emissive Fast prompts, £0 code graphics, and Teach-on-Screen overlays are ready to re-time the moment long VO locks. Parked for Chief.",
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
        f"- **Quality ({totals['Quality']} rows):** readable faces (Ada Lovelace, Charles Babbage, John Herschel, Alan Turing, David Hilbert, Marian Rejewski, Karl Landsteiner), candlelit/glowing scenes (August 1843 candlelit London study & Bletchley Bombe answer image), and the 2 Explorer beats.",
        f"- **Fast ({totals['Fast']} rows, non-emissive):** daylight prop and mechanism shots (three Enigma rotors & plugboard cables pan, 3-object callback bench, perforated Jacquard card pressing brass pins, Babbage's Analytical Engine 'Store' & 'Mill' gear columns, paper tape read-write head beside silicon wafer, 1936 Cambridge typewriter & offprint desk, 1946 ACE blueprints & 1950 Mind paper). Zero candles, flames, sparks, or glowing elements on Fast.",
        f"- **£0 code graphics ({totals['code_graphic']} rows):**",
        "  1. `P1:04_lovelace_1843_note_g_and_turing_1936_universal_machine_chart` — Babbage & Lovelace's 1843 Analytical Engine ('Store' + 'Mill') alongside Turing's 1936 Universal Machine tape (`SCALE: Lovelace wrote a working computer program with nested loops a full 100 years before the first electronic computer was ever switched on`)",
        "  2. `P1:06_159_quintillion_enigma_keys_vs_20_min_bombe_chart` — 60 × 17,576 × 150,738,274,937,250 = 158,962,555,217,826,360,000 (~159 quintillion) Enigma keys vs Turing's <20-minute Bombe sieve (`SCALE: 159 quintillion possible keys — twenty million times more combinations than there are grains of sand on all the beaches of Earth`)",
        "  3. `P2:02_lovelace_august_1843_note_g_bernoulli_b7_trace_table` — Ada Lovelace's August 1843 Note G algorithm table calculating Bernoulli number B₇ across V₁–V₁₃ with two nested branching loops (`SCALE: 41 pages of visionary notes written in 1843 — programming nested loops for a machine whose brass gears still hadn't been built`)",
        "  4. `P3:02_turing_1936_universal_machine_and_halting_problem_diagram` — Turing's 28 May 1936 Universal Computing Machine stored-program tape + Halting Problem contradiction matrix (`SCALE: one rule-table small enough to write on a postcard can simulate every piece of software humanity will ever write`)",
        "  5. `P4:02_turing_welchman_wettervorhersage_crib_loop_diagram` — 16-letter 'WETTERVORHERSAGE' crib loop + Welchman's diagonal board across 36 Bombe drum triplets (`SCALE: what would take a human clerk millions of years by hand flashed through Welchman's diagonal board in milliseconds`)",
        "  6. `P5:01_timeline_1843_2013_and_84000_messages_impact_chart` — completed 6-date timeline (Aug 1843 → 24 Dec 2013) + Bletchley Park wartime impact (~84,000 messages decoded/month, shortening WWII by 2–4 years) (`SCALE: ~84,000 intercepted Enigma messages decoded every month at Bletchley Park — shortening World War II in Europe by an estimated 2 to 4 years and saving ~14 million lives`)",
        f"- **£0 verified reuse ({totals['reuse']} row):** `P5:04_table_three_callback` uses the 2.40 s unused moving tail `[5.50s..7.90s]` of `P1:07_table_three_props_jacquard_card_paper_tape_enigma_rotor`.",
        "",
        "## Mint order",
        "",
        "006 > 007 > 008 > 009 > 010 > 011 > 012 > 013 > 014 > 015 > 016 > 017 > 018 > 019 > 020 > 021 > 022 > 023 > 024 > 025 > 026 > 027. `generation_authorized` is `false` on every row.",
    ])
    (EDIT / "PRICE_REVIEW_v01.md").write_text("\n".join(pr_lines) + "\n")
    print(f"027 v01 boards written: {totals['rows']} rows, Flow expected={totals['flow_credits_expected']}")


if __name__ == "__main__":
    main()
