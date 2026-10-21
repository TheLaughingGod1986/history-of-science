#!/usr/bin/env python3
"""HOS 062 (How Muscles Work: The Walking Motors Inside Your Cells) pre-VO plate boards v01. J0646. No mint, no spend.

Built from 00_Brand/Channel-Setup/ideas/062_Lohmann-SzentGyorgyi-Huxley-Muscles-Sliding-Filament/muscles_script_master_v01.md
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
        "Part 01 — The Walking Hands & the Battery You Burn Your Body Weight Of Every Day",
        [
            ("01_flexing_bicep_sarcomere_myosin_heads_walking_along_actin_ropes_with_atp", 0.0, 5.5, "A", False, "WALKING MOLECULAR HANDS", "Quality",
             "Quality: Short frame 0 / answer image (0:03) + inside a flexing human bicep, a striped muscle sarcomere zooms in to reveal billions of thick myosin motor heads grabbing thin actin ropes, snapping a phosphate off an ATP molecule, and hauling the ropes hand-over-hand without either protein filament ever changing length.",
             STYLE + "Split anatomical-and-molecular scene: on the left, a flexing human arm reveals striped muscle fibres; on the right, inside a sarcomere, rows of golden myosin motor heads reach out to grab braided red actin ropes and pull them hand-over-hand as Z-disc walls slide closer together." + QUAL_TAIL,
             {"kind": "WHEN", "label": "LONDON, 22 MAY 1954", "timeline_step": "3/4 · 22 May 1954 (Andrew Huxley & Rolf Niedergerke at Cambridge and Hugh Huxley & Jean Hanson at MIT publish back-to-back papers in Nature proving the Sliding Filament Theory)", "hold_s": 3.5}),
            ("02_lohmann_fiske_subbarow_1929_szent_gyorgyi_1942_szeged_and_huxleys_22_may_1954_split", 5.5, 6.0, "B", False, "ATP BATTERY, LIVING THREADS, SLIDING FILAMENTS", "Quality",
             "Quality: complex three-part composition (Karl Lohmann in Heidelberg and Cyrus Fiske with Yellapragada SubbaRow at Harvard in August–October 1929 isolating ATP from muscle; Albert Szent-Györgyi in Szeged, Hungary in 1942 dripping ATP onto actomyosin threads that violently contract; and Hugh Huxley with Jean Hanson at MIT alongside Andrew Huxley with Rolf Niedergerke at Cambridge publishing back-to-back in Nature on 22 May 1954).",
             STYLE + "Three-panel period composition: on the left, Karl Lohmann and Yellapragada SubbaRow in 1929 holding test tubes of purified muscle ATP; in the centre, Albert Szent-Györgyi in 1942 Szeged dripping ATP onto a contracting actomyosin thread in a glass dish; on the right, Hugh Huxley and Andrew Huxley in May 1954 comparing electron micrographs and interference microscope slides." + QUAL_TAIL,
             None),
            ("03_brass_balance_scale_50g_atp_recycling_1000_times_to_balance_60kg_human_figure", 11.5, 6.0, "C", False, "YOUR BODY WEIGHT IN ATP EVERY DAY", "Quality",
             "Quality: complex conceptual and anatomical reveal (a brass balance scale holds a 50-gram golden pile of ATP crystals on one pan, which recycles 1,000 times across 24 hours to balance a 60-kilogram human figure on the other pan).",
             STYLE + "Split conceptual-and-laboratory scene: on the left, a large brass balance scale holds a small 50-gram hen-egg-sized pile of golden ATP crystals on one pan balancing a full-sized human statue on the other pan as a mechanical counter clicks to 1,000; on the right, muscle fibres contract smoothly." + QUAL_TAIL,
             {"kind": "WHEN", "label": "AUGUST 1929 · OCTOBER 1929 · 1942 · 22 MAY 1954", "timeline_step": "1/4 · Aug–Oct 1929 (Lohmann; Fiske & SubbaRow) · 2/4 · 1942 (Szent-Györgyi & Straub) · 3/4 · 22 May 1954 (Hugh Huxley & Hanson; Andrew Huxley & Niedergerke)", "hold_s": 3.5}),
            ("04_lohmann_1929_szent_gyorgyi_1942_huxleys_22_may_1954_sarcomere_sliding_filament_chart", 17.5, 8.0, "E", False, "22 MAY 1954 HUXLEY & HANSON / HUXLEY & NIEDERGERKE: 2.5 → 1.6 µM SARCOMERE CONTRACTION WITH CONSTANT 1.6-µM A-BAND & 50–75 KG/DAY ATP TURNOVER", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked sarcomere band-length & sliding-filament chart from Lohmann (August 1929 Naturwissenschaften 17: 624–625), Szent-Györgyi (1942 Studies Inst. Med. Chem. Szeged), Andrew Huxley & Niedergerke (22 May 1954 Nature 173: 971–973), and Hugh Huxley & Hanson (22 May 1954 Nature 173: 973–976) compares relaxed (~2.5 micrometres) and contracted (~1.6 micrometres) muscle sarcomeres, proving thick myosin filaments (A-band, 1.6 micrometres) and thin actin filaments (1.0 micrometre) never shorten, but slide past each other powered by ~50–75 kg/day of recycled ATP.",
             {"kind": "DATA", "label": "SARCOMERE (2.5 → 1.6 µM): THICK MYOSIN A-BAND (1.6 µM) & THIN ACTIN (1.0 µM) SLIDE WITHOUT SHRINKING (~60 KG/DAY ATP)", "detail": "Inked sarcomere sliding-filament chart on period paper comparing relaxed (~2.5 micrometres) and contracted (~1.6 micrometres) muscle sarcomeres, proving thick myosin filaments (A-band, 1.6 micrometres) and thin actin filaments (1.0 micrometre) never shorten, but slide past each other powered by ~50–75 kg/day of recycled ATP", "scale": "when you lift a heavy suitcase, not a single protein fibre inside your arm actually shrinks — instead, billions of microscopic myosin hands haul actin ropes hand-over-hand like a tug-of-war team pulling a ship into harbour", "who_card": "Karl Lohmann (1898–1978) — German biochemist · Cyrus H. Fiske (1890–1978) — American biochemist · Yellapragada SubbaRow (1895–1948) — Indian biochemist · Albert Szent-Györgyi (1893–1986) — Hungarian biochemist · Hugh E. Huxley (1924–2013) — British molecular biologist · Jean Hanson (1919–1973) — British biophysicist · Andrew F. Huxley (1917–2012) — British physiologist · Rolf Niedergerke (1921–2011) — German-British physiologist", "when_stamp": "August 1929 · October 1929 · 1942 · 22 May 1954", "hold_s": 3.8}),
            ("05_wooden_sarcomere_sliding_rod_model_glass_pipette_and_brass_dynamometer_pan", 25.5, 5.5, "A", False, "FIBRES SLIDE, NEVER SHRINK", "Fast",
             "Fast: daylight macro pan across a wooden interlocking sliding-rod sarcomere model, a glass dropper bottle, and a brass grip dynamometer gauge on an oak bench between code graphics so two full-frame graphics never run back to back. Nothing emissive, no face.",
             STYLE + "In crisp daylight on an oak physiology bench, the camera pans smoothly across a carved wooden model of interlocking sliding rods, a glass pipette in a stand, and a polished brass hand dynamometer gauge." + FAST_TAIL,
             None),
            ("06_huxley_1969_lymn_taylor_1971_four_step_atp_cross_bridge_10nm_power_stroke_chart", 31.0, 8.0, "E", False, "THE 10-NANOMETRE POWER STROKE", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period parchment, an inked 4-step actomyosin cross-bridge ATPase cycle diagram (from Hugh Huxley 1969 Science 164: 1356–1365 & Lymn and Taylor 1971 Biochemistry 10: 4617–4624) shows ATP binding (detachment from rigor), ATP hydrolysis to ADP + Pi (cocking the myosin lever arm), actin re-attachment, and phosphate release driving a ~5–10 nanometre, ~4 piconewton power stroke.",
             {"kind": "DATA", "label": "4-STEP CROSS-BRIDGE CYCLE (HUXLEY 1969 / LYMN & TAYLOR 1971): ATP DETACHES → ADP+PI COCKS → ~10-NM, ~4-PN POWER STROKE", "detail": "Inked 4-step actomyosin cross-bridge cycle diagram showing ATP binding (detachment from rigor), ATP hydrolysis to ADP + Pi (cocking the myosin lever arm), actin re-attachment, and phosphate release driving a ~5–10 nanometre, ~4 piconewton power stroke", "scale": "each individual myosin hand pulls the rope just ten billionths of a metre — ten nanometres — yet trillions of them firing together in your legs can launch your entire body into the air", "hold_s": 3.8}),
            ("07_table_three_props_1929_atp_vial_1942_szeged_thread_dish_and_1954_nature_issue", 39.0, 5.5, "C", False, "1929 TO 1971", "Fast",
             "Fast: daylight prop table (callback source for Part 05: Karl Lohmann's 1929 glass vial of ATP barium salt, Albert Szent-Györgyi's 1942 glass Petri dish of actomyosin threads, and the 22 May 1954 issue of Nature beside a sarcomere micrograph). Nothing emissive.",
             STYLE + "On an oak workbench in soft window light sit three objects side by side: a stoppered glass vial of white ATP powder, a glass Petri dish holding fine protein threads, and a bound 1954 journal open beside a striped muscle micrograph." + FAST_TAIL,
             None),
            ("08_explorer_slotting_atp_battery_into_myosin_hand_to_pull_actin_rope_in_sarcomere", 62.0, 5.5, "A", True, None, "Quality",
             "Quality: Explorer beat 1 (locked character reference, after 1:00).",
             STYLE + "Standing inside a giant wooden sarcomere frame, the Explorer slots a golden three-ring ATP battery block into a mechanical brass myosin hand, watching the hand release the red actin rope, cock backward, grab a fresh rung, and haul the Z-disc wall inward." + EXP_TAIL,
             None),
            ("09_szent_gyorgyi_1942_szeged_dripping_atp_onto_contracting_rabbit_actomyosin_threads", 67.5, 5.5, "B", False, "SZEGED, 1942", "Quality",
             "Quality: readable face (at the University of Szeged in Hungary in 1942, Albert Szent-Györgyi squeezes a fine thread of rabbit actomyosin into a glass dish and watches it violently contract the instant a drop of ATP touches it).",
             STYLE + "In a 1942 Szeged laboratory, Hungarian biochemist Albert Szent-Györgyi leans over a glass Petri dish with a pipette, watching in wonder as a pale protein thread of rabbit actomyosin visibly bunches and contracts upon receiving a drop of clear ATP solution." + QUAL_TAIL,
             {"kind": "WHEN", "label": "SZEGED, 1942", "timeline_step": "2/4 · 1941–1942 (Albert Szent-Györgyi & Brunó Straub in Szeged discover actin and make actomyosin threads contract in a dish with ATP)", "hold_s": 3.5}),
        ],
    ),
    (
        2,
        "Part 02 — August–October 1929 & 1941–1942: The ATP Battery & Albert Szent-Györgyi's Living Muscle Threads",
        [
            ("01_lohmann_heidelberg_fiske_subbarow_harvard_1929_atp_and_szent_gyorgyi_straub_1942_szeged", 73.0, 6.5, "A", False, "LIFELESS THREADS CONTRACTED IN A DISH", "Quality",
             "Quality: readable faces (Karl Lohmann in Heidelberg and Cyrus Fiske with Yellapragada SubbaRow at Harvard in August–October 1929 isolating ATP from muscle tissue, dissolving to Albert Szent-Györgyi and Brunó Straub at the University of Szeged in 1941–1942 purifying actin and watching actomyosin threads contract with ATP).",
             STYLE + "Split period scene: on the left in 1929, Karl Lohmann in Heidelberg and Yellapragada SubbaRow with Cyrus Fiske at Harvard inspect precipitated ATP crystals; on the right in 1942 Szeged, Albert Szent-Györgyi and young Brunó Straub watch artificial actomyosin threads contract in a glass dish." + QUAL_TAIL,
             {"kind": "FACT", "label": "Lifeless threads contracted in a dish", "who_card": "Brunó F. Straub (1914–1996) — Hungarian biochemist", "when_stamp": "August 1929 · October 1929 · 1939 · 1941 · 1942", "timeline_step": "1/4 · Aug–Oct 1929 & 1939 (Lohmann and Fiske & SubbaRow isolate ATP; Engelhardt & Lyubimova prove myosin is an ATPase) & 2/4 · 1941–1942 (Szent-Györgyi & Straub contract actomyosin threads with ATP)", "hold_s": 3.8}),
            ("02_lohmann_fiske_subbarow_1929_atp_60kg_turnover_and_szent_gyorgyi_1942_actomyosin_chart", 79.5, 8.0, "E", False, "AUG–OCT 1929 LOHMANN / FISKE & SUBBAROW (ATP → ADP + PI, ~50–75 KG/DAY TURNOVER) & 1942 SZENT-GYÖRGYI & STRAUB ACTOMYOSIN CONTRACTION", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked ATP hydrolysis energy & Szent-Györgyi actomyosin contraction chart from Lohmann (August 1929, Naturwissenschaften 17: 624–625), Fiske & SubbaRow (October 1929, Science 70: 381–382), Engelhardt & Lyubimova (1939, Nature 144: 668–669), and Szent-Györgyi (1942) shows ATP splitting into ADP + Pi (~30.5 to 50 kJ/mol released) to drive actomyosin thread superprecipitation and contraction, with the human body holding ~50–100 g of ATP and recycling ~50–75 kg/day.",
             {"kind": "DATA", "label": "1929 ATP TRIPHOSPHATE SPRING (~50 G POOL RECYCLED ~1,000× = ~60 KG/DAY) & 1942 ACTIN + MYOSIN + ATP CONTRACTION", "detail": "Inked ATP hydrolysis energy & Szent-Györgyi actomyosin contraction chart on period paper from Lohmann (August 1929, Naturwissenschaften 17: 624–625), Fiske & SubbaRow (October 1929, Science 70: 381–382), Engelhardt & Lyubimova (1939, Nature 144: 668–669), and Szent-Györgyi (1942) showing ATP splitting into ADP + Pi (~30.5 to 50 kJ/mol released) to drive actomyosin thread superprecipitation and contraction, with the human body holding ~50–100 g of ATP and recycling ~50–75 kg/day", "scale": "your body holds only about fifty grams of ATP at any one moment, yet because every molecule is discharged and recharged nearly a thousand times a day, you burn through your own body weight in ATP every twenty-four hours", "hold_s": 3.8}),
            ("03_szeged_1942_glass_syringe_extruding_actomyosin_thread_and_pipette_closeup", 87.5, 6.5, "B", False, "1942 — LIFE IN A GLASS DISH", "Fast",
             "Fast: daylight macro shot of a glass syringe extruding a pale protein thread into a glass dish beside a dropper bottle of ATP and a pair of brass callipers on a 1942 Szeged bench. Nothing emissive, no face.",
             STYLE + "In crisp daylight on a 1942 Hungarian workbench, a glass syringe rests beside a Petri dish containing a contracted protein thread, a glass dropper bottle, and brass measuring callipers." + FAST_TAIL,
             None),
            ("04_harvard_heidelberg_1929_colorimeter_tubes_and_three_phosphate_model_pan", 94.0, 5.5, "C", False, "AUGUST–OCTOBER 1929 — DISCOVERING ATP", "Fast",
             "Fast: daylight close-up pan across a rack of blue Fiske-SubbaRow phosphate colorimeter tubes beside a wooden ball-and-stick model of adenosine triphosphate on an oak table. Nothing emissive, no face.",
             STYLE + "In bright window light on a 1929 chemistry bench, a wooden rack of blue-tinted glass colorimeter tubes sits beside a carved wooden ball-and-stick model of a three-phosphate molecule." + FAST_TAIL,
             None),
        ],
    ),
    (
        3,
        "Part 03 — 22 May 1954: Two Unrelated Huxleys Publish Back-to-Back in Nature & Prove the Sliding Filament Theory — Midpoint Twist",
        [
            ("01_hugh_huxley_jean_hanson_mit_and_andrew_huxley_rolf_niedergerke_cambridge_22_may_1954", 99.5, 6.5, "A", False, "22 MAY 1954: TWO HUXLEYS, ONE ISSUE", "Quality",
             "Quality: readable faces (Hugh Huxley and Jean Hanson at MIT using electron microscopy and X-ray diffraction alongside Andrew Huxley and Rolf Niedergerke at Cambridge using interference microscopy, publishing back-to-back in Nature on Saturday, 22 May 1954 to prove the Sliding Filament Theory).",
             STYLE + "Split period scene: on the left at MIT in 1954, Hugh Huxley and Jean Hanson examine electron micrographs of overlapping thick myosin and thin actin filaments; on the right at Cambridge in 1954, Andrew Huxley and Rolf Niedergerke adjust a custom interference microscope showing constant dark A-bands in a living muscle fibre." + QUAL_TAIL,
             {"kind": "FACT", "label": "22 May 1954: two Huxleys, one issue", "when_stamp": "1953 · 22 May 1954", "timeline_step": "3/4 · 22 May 1954 (Andrew Huxley & Rolf Niedergerke and Hugh Huxley & Jean Hanson publish back-to-back in Nature proving the Sliding Filament Theory)", "hold_s": 3.8}),
            ("02_huxley_niedergerke_and_huxley_hanson_22_may_1954_nature_constant_a_band_sliding_chart", 106.0, 8.0, "E", False, "22 MAY 1954 NATURE (HUXLEY & NIEDERGERKE PP. 971–973; HUXLEY & HANSON PP. 973–976): CONSTANT 1.6-µM A-BAND VS SHRINKING I-BAND & H-ZONE", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked Andrew Huxley & Niedergerke (22 May 1954, Nature 173: 971–973) and Hugh Huxley & Hanson (22 May 1954, Nature 173: 973–976) sarcomere striation measurement chart plots A-band width (constant at ~1.6 micrometres across all sarcomere lengths from 3.0 down to 1.6 micrometres) vs I-band and H-zone widths decreasing linearly as thin actin filaments slide past thick myosin filaments.",
             {"kind": "DATA", "label": "22 MAY 1954 NATURE BACK-TO-BACK: A-BAND STAYS 1.6 µM CONSTANT WHILE I-BAND & H-ZONE NARROW AS FILAMENTS SLIDE", "detail": "Inked Andrew Huxley & Niedergerke (22 May 1954, Nature 173: 971–973) and Hugh Huxley & Hanson (22 May 1954, Nature 173: 973–976) sarcomere striation measurement chart on period paper plotting A-band width (constant at ~1.6 micrometres across all sarcomere lengths from 3.0 down to 1.6 micrometres) vs I-band and H-zone widths decreasing linearly as thin actin filaments slide past thick myosin filaments", "scale": "if you interlace the fingers of your left and right hands and slide your palms together, your overall span gets shorter even though not a single finger changed length — and that is how every muscle in your body contracts", "hold_s": 3.8}),
            ("03_cambridge_mit_1954_sarcomere_electron_micrograph_plates_and_nature_journal_closeup", 114.0, 6.5, "B", False, "22 MAY 1954 — THE SLIDING FILAMENT THEORY", "Fast",
             "Fast: daylight macro shot of glass electron-microscope photographic plates showing striped sarcomere A-bands and I-bands beside a brass vernier calliper and the 22 May 1954 Nature offprint. Nothing emissive, no face.",
             STYLE + "In crisp daylight on a 1954 biophysics bench, glass photographic plates of striped muscle sarcomeres sit beside a brass vernier calliper and a printed scientific journal open to two side-by-side papers." + FAST_TAIL,
             None),
            ("04_interlocking_wooden_comb_teeth_sliding_model_and_interference_microscope_prism_pan", 120.5, 5.5, "C", False, "A-BAND NEVER CHANGES LENGTH", "Fast",
             "Fast: daylight close-up pan across a brass-and-wood sliding filament demonstration jig with interlocking thick and thin rods beside an optical microscope prism. Nothing emissive, no face.",
             STYLE + "In bright window light on a wooden laboratory table, a mechanical demonstration model of thick golden rods and thin red rods slides smoothly together without either set of rods changing length." + FAST_TAIL,
             None),
        ],
    ),
    (
        4,
        "Part 04 — 1957–1971: Walking Molecular Hands (Cross-Bridges), the Rigor Mortis Paradox & How Calcium Pulls the Trigger",
        [
            ("01_hugh_huxley_1957_1969_cross_bridges_ebashi_1963_troponin_and_lymn_taylor_1971_cycle", 126.0, 6.5, "A", False, "NO ATP LOCKS MUSCLES STIFF", "Quality",
             "Quality: readable faces (Hugh Huxley in 1957–1969 examining high-resolution electron micrographs of myosin cross-bridges, Japanese pharmacologist Setsuro Ebashi in 1963–1965 discovering troponin and the calcium trigger, and Edwin Taylor and Richard Lymn in December 1971 mapping the 4-step ATPase cross-bridge cycle).",
             STYLE + "Split period scene: on the left in Cambridge, Hugh Huxley points to tiny myosin cross-bridge side-arms on an electron micrograph print while Setsuro Ebashi in Tokyo inspects a calcium-troponin muscle trace; on the right in 1971 Chicago, Edwin Taylor and Richard Lymn diagram the four-step ATP release and power-stroke cycle." + QUAL_TAIL,
             {"kind": "FACT", "label": "No ATP locks muscles stiff", "who_card": "Setsuro Ebashi (1922–2006) — Japanese pharmacologist", "when_stamp": "1957 · 1963 · 20 June 1969 · December 1971", "timeline_step": "4/4 · 1957–1971 (Hugh Huxley images myosin cross-bridges; Setsuro Ebashi discovers the calcium-troponin switch; Lymn & Taylor map the 4-step ATP cross-bridge cycle)", "hold_s": 3.8}),
            ("02_huxley_1969_ebashi_1963_lymn_taylor_1971_calcium_troponin_and_rigor_release_chart", 132.5, 8.0, "E", False, "1963–1965 EBASHI (CA2+ + TROPONIN UNLOCKS TROPOMYOSIN) & 1969–1971 HUXLEY / LYMN-TAYLOR (ATP DETACHES RIGOR → 10-NM POWER STROKE)", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked Hugh Huxley (1969, Science 164: 1356–1365), Lymn & Taylor (December 1971, Biochemistry 10: 4617–4624), and Ebashi (1963–1965, Nature) calcium-troponin switch & actomyosin cross-bridge cycle chart shows Ca2+ binding troponin to shift tropomyosin off actin binding sites, followed by ATP detachment from rigor, hydrolysis cocking, and Pi-release 10-nm power stroke.",
             {"kind": "DATA", "label": "EBASHI CA2+-TROPONIN SWITCH (1963) + LYMN-TAYLOR CYCLE (1971): ATP RELEASES RIGOR LOCK → 10-NM MYOSIN POWER STROKE", "detail": "Inked Hugh Huxley (1969, Science 164: 1356–1365), Lymn & Taylor (December 1971, Biochemistry 10: 4617–4624), and Ebashi (1963–1965, Nature) calcium-troponin switch & actomyosin cross-bridge cycle chart on period paper showing Ca2+ binding troponin to shift tropomyosin off actin binding sites, followed by ATP detachment, hydrolysis cocking, and Pi-release 10-nm power stroke", "scale": "counterintuitively, a muscle doesn't need fresh ATP to grab the rope — it needs fresh ATP to let go of the rope for the next pull, which is why running out of ATP after death locks muscles rigid in rigor mortis", "hold_s": 3.8}),
            ("03_wooden_actin_helix_with_tropomyosin_latch_and_myosin_lever_arm_model_closeup", 140.5, 6.5, "B", False, "DECEMBER 1971 — THE CROSS-BRIDGE POWER STROKE", "Fast",
             "Fast: daylight macro shot of a sculpted molecular model of a braided actin filament with a movable tropomyosin safety bar and a hinged brass myosin head on a workbench. Nothing emissive, no face.",
             STYLE + "In crisp daylight on a biophysics bench, a detailed wooden and brass model shows a braided actin rope fitted with a hinged troponin-tropomyosin safety bar beside a spring-loaded myosin lever arm." + FAST_TAIL,
             None),
            ("04_explorer_unlocking_troponin_safety_cable_with_calcium_key_and_releasing_rigor_clamp", 147.0, 5.5, "B", True, None, "Quality",
             "Quality: Explorer beat 2 (locked character reference).",
             STYLE + "Standing beside a braided red actin rope guarded by a brass safety rail, the Explorer turns a silver calcium key in the troponin lock to slide the safety rail aside, then inserts a golden ATP block into a clamped myosin hand so it releases and pulls the next rung." + EXP_TAIL,
             None),
        ],
    ),
    (
        5,
        "Part 05 — Why Muscle Fatigue Isn't 'Lactic Acid' — & How Mitochondria Recharge Your Body Weight in ATP",
        [
            ("01_timeline_1929_1971_and_phosphate_fatigue_vs_lactate_fuel_chart", 152.5, 8.5, "E", False, "1929–1971 TIMELINE · LOHMANN/FISKE/SUBBAROW ATP, SZENT-GYÖRGYI ACTOMYOSIN, 1954 HUXLEYS SLIDING FILAMENTS & 1969–1971 CROSS-BRIDGE CYCLE", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, the 4-date timeline completes: Aug–Oct 1929 & 1939 (Karl Lohmann and Cyrus Fiske & Yellapragada SubbaRow isolate ATP from muscle; Engelhardt & Lyubimova prove myosin is an ATPase enzyme) · 1941–1942 (Albert Szent-Györgyi & Brunó Straub in Szeged discover actin and make actomyosin threads contract in a dish with ATP) · 22 May 1954 (Andrew Huxley & Rolf Niedergerke at Cambridge and Hugh Huxley & Jean Hanson at MIT publish back-to-back papers in Nature proving the Sliding Filament Theory) · 1957–1971 (Hugh Huxley images myosin cross-bridges; Setsuro Ebashi discovers the calcium-troponin switch; Lymn & Taylor map the 4-step ATP cross-bridge cycle).",
             {"kind": "DATA", "label": "1929–1971 MUSCLE & ATP TIMELINE · INORGANIC PHOSPHATE (PI) FATIGUE VS LACTATE FUEL & 60 KG/DAY ATP RECYCLING", "detail": "Animated 4-date timeline (1929 → 1971) alongside the inorganic phosphate (Pi) cross-bridge fatigue vs lactate fuel diagram", "scale": "from rabbit muscle threads shrinking on a table in war-torn Hungary to two Englishmen named Huxley publishing side by side in Nature, science revealed the walking molecular motors that move every breath, heartbeat, and step of your life", "when_stamp": "1929–1971", "timeline_step": "4/4 · 1929–1971 timeline complete", "hold_s": 3.8}),
            ("02_sliding_filament_model_and_rechargeable_atp_phosphate_dial_on_plinth_pan", 161.0, 5.5, "A", False, "LACTATE IS FUEL; PHOSPHATE JAMS THE MOTOR", "Fast",
             "Fast: daylight close-up of a brass-and-wood sliding sarcomere model beside a three-phosphate ATP wheel on a wooden museum plinth. Nothing emissive, no face.",
             STYLE + "In crisp daylight on a wooden museum plinth, a polished brass-and-wood sliding sarcomere model sits beside a three-ring phosphate wheel and a framed 1954 micrograph." + FAST_TAIL,
             None),
            ("03_krebs_1937_sheffield_mitchell_1961_cornwall_and_margulis_1967_mitochondria_handoff", 166.5, 6.5, "C", False, "MITOCHONDRIA: RECHARGING 60 KG OF ATP", "Quality",
             "Quality: readable faces (Hans Krebs at the University of Sheffield in June 1937 mapping the Citric Acid Cycle, alongside Peter Mitchell in July 1961 and Lynn Margulis in March 1967 revealing how mitochondria spin ATP synthase to recharge 60 kg of ATP a day — handoff to 063 Mitochondria, the Krebs Cycle & ATP Synthase).",
             STYLE + "Split period scene: on the left in June 1937 Sheffield, biochemist Hans Krebs sketches the circular Citric Acid Cycle wheel beside manometer flasks; on the right, inside a mitochondrion, a rotary ATP synthase turbine spins at high speed to stitch phosphate groups back onto ADP." + QUAL_TAIL,
             {"kind": "WHEN", "label": "JUNE 1937 · JULY 1961 · MARCH 1967", "hold_s": 3.5}),
            ("04_table_three_callback", 173.0, 2.4, "C", False, None, "reuse",
             "Reuse: verified unused moving window [5.50s..7.90s] of P1:07_table_three_props_1929_atp_vial_1942_szeged_thread_dish_and_1954_nature_issue (callback, £0).",
             "Reuse P1:07_table_three_props_1929_atp_vial_1942_szeged_thread_dish_and_1954_nature_issue [5.50s..7.90s] (2.40s distinct non-overlapping tail window from 8.00s source clip).",
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
                row["reuse_of"] = "P1:07_table_three_props_1929_atp_vial_1942_szeged_thread_dish_and_1954_nature_issue"
                row["reuse_window_s"] = [5.5, 7.9]
                row["reuse_audit"] = {
                    "source_row": "P1:07_table_three_props_1929_atp_vial_1942_szeged_thread_dish_and_1954_nature_issue",
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
            "film": "062_Lohmann-SzentGyorgyi-Huxley-Muscles-Sliding-Filament",
            "part": p_idx,
            "title": p_title,
            "version": "v01",
            "timing_status": "pre_vo_script_clock (built from muscles_script_master_v01.md; retimes onto Scribe STT once VO locks)",
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
        "film": "062_Lohmann-SzentGyorgyi-Huxley-Muscles-Sliding-Filament",
        "version": "v01",
        "date": "2026-10-19",
        "owner": "gemini (J0646)",
        "status": "PRE_VO_BOARDS_V01_NO_MINT",
        "generation_authorized": False,
        "script": "00_Brand/Channel-Setup/ideas/062_Lohmann-SzentGyorgyi-Huxley-Muscles-Sliding-Filament/muscles_script_master_v01.md",
        "sources": "00_Brand/Channel-Setup/ideas/062_Lohmann-SzentGyorgyi-Huxley-Muscles-Sliding-Filament/SOURCES_v01.md",
        "credit_snapshot": {
            "flow_balance": 23740,
            "flow_floor": 0,
            "flow_read_at": "2026-10-15T21:42:22Z",
            "vertex_promo_gbp": 71.02,
            "vertex_usable_gbp": 70.02,
        },
        "totals": totals,
        "per_part": per_part_summary,
        "mint_order": "006 > 007 > 008 > 009 > 010 > 011 > 012 > 013 > 014 > 015 > 016 > 017 > 018 > 019 > 020 > 021 > 022 > 023 > 024 > 025 > 026 > 027 > 028 > 029 > 030 > 031 > 032 > 033 > 034 > 035 > 036 > 037 > 038 > 039 > 040 > 041 > 042 > 043 > 044 > 045 > 046 > 047 > 048 > 049 > 050 > 051 > 052 > 053 > 054 > 055 > 056 > 057 > 058 > 059 > 060 > 061 > 062 > 063 > 064 > 065. Nothing in 062 is generation_authorized.",
    }
    (EDIT / "PICTURE_PLAN_v01.json").write_text(json.dumps(plan, indent=2) + "\n")

    sl = [
        "# 062 How Muscles Work: The Walking Motors Inside Your Cells — Shot list & plate boards v01 (pre-VO)",
        "",
        "Gemini, 19 Oct 2026, J0646. Built from `muscles_script_master_v01.md` (`91.2 PASS`) and `SOURCES_v01.md`.",
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
        "# 062 price review v01 (pre-VO plate boards)",
        "",
        "Gemini, 19 Oct 2026, J0646. Boards only. **No mint. No spend. No merge.**",
        "Prepared from `muscles_script_master_v01.md` (`91.2 PASS`) and `SOURCES_v01.md` so 062's full plate board rows, non-emissive Fast prompts, £0 code graphics, and Teach-on-Screen overlays are ready to re-time the moment long VO locks. Parked for Chief.",
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
        f"- **Quality ({totals['Quality']} rows):** readable faces (Karl Lohmann, Cyrus H. Fiske, Yellapragada SubbaRow, Albert Szent-Györgyi, Brunó F. Straub, Hugh E. Huxley, Jean Hanson, Andrew F. Huxley, Rolf Niedergerke, Setsuro Ebashi, Edwin W. Taylor, Richard W. Lymn, Hans Krebs), August–October 1929 Heidelberg/Harvard ATP isolation & 1942 Szeged contracting rabbit actomyosin threads, 22 May 1954 MIT/Cambridge back-to-back *Nature* sliding-filament proof, 1957–1971 myosin cross-bridges, calcium-troponin switch & rigor-release cycle, and the 2 Explorer beats.",
        f"- **Fast ({totals['Fast']} rows, non-emissive):** daylight prop and laboratory shots (wooden interlocking sliding-rod sarcomere model, glass pipette & brass dynamometer pan, 3-object callback bench, 1942 Szeged glass syringe extruding actomyosin thread & brass callipers, 1929 blue phosphate colorimeter tubes & wooden ball-and-stick ATP model, 1954 glass electron-microscope sarcomere plates & vernier calliper, brass-and-wood sliding filament demonstration jig, wooden actin rope with hinged troponin safety bar & spring-loaded myosin lever arm, sliding sarcomere model & three-ring phosphate wheel on museum plinth). Zero candles, flames, sparks, or glowing elements on Fast.",
        f"- **£0 code graphics ({totals['code_graphic']} rows):**",
        "  1. `P1:04_lohmann_1929_szent_gyorgyi_1942_huxleys_22_may_1954_sarcomere_sliding_filament_chart` — sarcomere band-length & sliding-filament chart (`2.5 → 1.6 µm`) showing thick myosin A-band (`1.6 µm`) and thin actin (`1.0 µm`) sliding without shrinking, powered by `~50–75 kg/day` recycled ATP (`SCALE: when you lift a heavy suitcase, not a single protein fibre inside your arm actually shrinks — instead, billions of microscopic myosin hands haul actin ropes hand-over-hand like a tug-of-war team pulling a ship into harbour`)",
        "  2. `P1:06_huxley_1969_lymn_taylor_1971_four_step_atp_cross_bridge_10nm_power_stroke_chart` — Hugh Huxley (1969 *Science*) & Lymn and Taylor (1971 *Biochemistry*) 4-step actomyosin cross-bridge ATPase cycle & `~10-nm` power stroke chart (`SCALE: each individual myosin hand pulls the rope just ten billionths of a metre — ten nanometres — yet trillions of them firing together in your legs can launch your entire body into the air`)",
        "  3. `P2:02_lohmann_fiske_subbarow_1929_atp_60kg_turnover_and_szent_gyorgyi_1942_actomyosin_chart` — Lohmann (August 1929), Fiske & SubbaRow (October 1929), Engelhardt & Lyubimova (1939), and Szent-Györgyi (1942) ATP hydrolysis (`~50 g` pool recycled `~1,000×/day` = `~60 kg/day`) & actomyosin contraction chart (`SCALE: your body holds only about fifty grams of ATP at any one moment, yet because every molecule is discharged and recharged nearly a thousand times a day, you burn through your own body weight in ATP every twenty-four hours`)",
        "  4. `P3:02_huxley_niedergerke_and_huxley_hanson_22_may_1954_nature_constant_a_band_sliding_chart` — Andrew Huxley & Niedergerke and Hugh Huxley & Hanson (22 May 1954, *Nature* 173: 971–976) sarcomere striation measurement chart showing constant `1.6-µm` A-band width vs narrowing I-band and H-zone (`SCALE: if you interlace the fingers of your left and right hands and slide your palms together, your overall span gets shorter even though not a single finger changed length — and that is how every muscle in your body contracts`)",
        "  5. `P4:02_huxley_1969_ebashi_1963_lymn_taylor_1971_calcium_troponin_and_rigor_release_chart` — Setsuro Ebashi (1963–1965 *Nature*) `Ca²⁺`-troponin-tropomyosin switch & Lymn-Taylor (1971) rigor-detachment ATPase cycle (`SCALE: counterintuitively, a muscle doesn't need fresh ATP to grab the rope — it needs fresh ATP to let go of the rope for the next pull, which is why running out of ATP after death locks muscles rigid in rigor mortis`)",
        "  6. `P5:01_timeline_1929_1971_and_phosphate_fatigue_vs_lactate_fuel_chart` — completed 4-date timeline (1929 → 1971) + inorganic phosphate (`Pi`) fatigue vs lactate fuel diagram (`SCALE: from rabbit muscle threads shrinking on a table in war-torn Hungary to two Englishmen named Huxley publishing side by side in Nature, science revealed the walking molecular motors that move every breath, heartbeat, and step of your life`)",
        f"- **£0 verified reuse ({totals['reuse']} row):** `P5:04_table_three_callback` uses the 2.40 s unused moving tail `[5.50s..7.90s]` of `P1:07_table_three_props_1929_atp_vial_1942_szeged_thread_dish_and_1954_nature_issue`.",
        "",
        "## Mint order",
        "",
        "006 > 007 > 008 > 009 > 010 > 011 > 012 > 013 > 014 > 015 > 016 > 017 > 018 > 019 > 020 > 021 > 022 > 023 > 024 > 025 > 026 > 027 > 028 > 029 > 030 > 031 > 032 > 033 > 034 > 035 > 036 > 037 > 038 > 039 > 040 > 041 > 042 > 043 > 044 > 045 > 046 > 047 > 048 > 049 > 050 > 051 > 052 > 053 > 054 > 055 > 056 > 057 > 058 > 059 > 060 > 061 > 062 > 063 > 064 > 065. `generation_authorized` is `false` on every row.",
    ])
    (EDIT / "PRICE_REVIEW_v01.md").write_text("\n".join(pr_lines) + "\n")
    print(f"062 v01 boards written: {totals['rows']} rows, Flow expected={totals['flow_credits_expected']}")


if __name__ == "__main__":
    main()
