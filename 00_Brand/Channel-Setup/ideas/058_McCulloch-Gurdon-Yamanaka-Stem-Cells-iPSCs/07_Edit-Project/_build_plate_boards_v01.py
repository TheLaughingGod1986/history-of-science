#!/usr/bin/env python3
"""HOS 058 (Stem Cells: How Scientists Rewound an Adult Cell) pre-VO plate boards v01. J0615. No mint, no spend.

Built from 00_Brand/Channel-Setup/ideas/058_McCulloch-Gurdon-Yamanaka-Stem-Cells-iPSCs/stem_cells_script_master_v01.md
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
        "Part 01 — The Four-Gene Time Machine Inside Your Skin",
        [
            ("01_adult_skin_fibroblast_rewound_by_4_yamanaka_factors_into_ipsc_and_beating_heart_cell", 0.0, 5.5, "A", False, "4 GENES REWIND AN ADULT CELL", "Quality",
             "Quality: Short frame 0 / answer image (0:03) + a flat adult skin fibroblast in a glass Petri dish receives four genetic switches (Oct3/4, Sox2, Klf4, c-Myc), rewinds like a clock into a round embryonic-like Induced Pluripotent Stem Cell (iPSC) discovered by Shinya Yamanaka on 25 August 2006, and then differentiates into a rhythmically beating red heart muscle cell and a branching brain neuron.",
             STYLE + "Split microscopic-and-laboratory scene: on the left, a flat spindle-shaped skin fibroblast cell rounds up into a dome-shaped pluripotent stem-cell colony that transforms into rhythmically pulsing red heart-muscle cells; on the right in August 2006 Kyoto, Shinya Yamanaka inspects a 24-well culture plate." + QUAL_TAIL,
             {"kind": "WHEN", "label": "KYOTO, 25 AUGUST 2006", "timeline_step": "4/4 · 25 Aug 2006 & Nov 2007 (Shinya Yamanaka & Kazutoshi Takahashi reprogram mouse and human adult skin fibroblasts into iPSCs using 4 transcription factors: Oct3/4, Sox2, Klf4, c-Myc)", "hold_s": 3.5}),
            ("02_mcculloch_till_1961_toronto_gurdon_1962_oxford_and_yamanaka_takahashi_2006_kyoto_split", 5.5, 6.0, "B", False, "SPLEEN NODULES, CLONED FROGS, 4 YAMANAKA FACTORS", "Quality",
             "Quality: complex three-part composition (Ernest McCulloch and James Till in Toronto in February 1961 counting tiny regeneration nodules on mouse spleens to prove blood-making stem cells exist; young John Gurdon at Oxford in December 1962 transplanting an adult frog intestinal nucleus into an egg cell under a microscope; and Shinya Yamanaka and Kazutoshi Takahashi at Kyoto University on 25 August 2006 narrowing 24 candidate factors down to the 4 Yamanaka Factors).",
             STYLE + "Three-panel period composition: on the left, Ernest McCulloch and James Till in 1961 Toronto examining mouse spleen colonies; in the centre, young John Gurdon in 1962 Oxford transferring a frog nucleus with a glass micropipette; on the right, Shinya Yamanaka and Kazutoshi Takahashi in 2006 Kyoto examining iPSC culture dishes." + QUAL_TAIL,
             None),
            ("03_bone_marrow_2m_red_blood_cells_per_sec_vs_waddington_1957_epigenetic_valley_split", 11.5, 6.0, "C", False, "2 MILLION NEW BLOOD CELLS A SECOND", "Quality",
             "Quality: complex anatomical and conceptual reveal (inside the spongy red marrow of a human bone, a single hematopoietic stem cell divides to generate red blood cells, white blood cells, and platelets at 2,000,000 red cells per second, contrasted with Conrad Waddington's 1957 epigenetic hill where an embryonic marble rolls down into a deep specialized valley).",
             STYLE + "Split anatomical-and-sculptural scene: on the left, inside spongy red bone marrow, a master blood stem cell divides into streams of red blood discs, white cells, and platelets; on the right, a glass marble rolls down a carved wooden hillside of branching valleys into a deep skin-cell groove." + QUAL_TAIL,
             {"kind": "WHEN", "label": "FEBRUARY 1961 · DECEMBER 1962 · 25 AUGUST 2006", "timeline_step": "1/4 · Feb 1961 & Feb 1963 (McCulloch & Till) · 2/4 · Dec 1962 (Gurdon) · 4/4 · 25 Aug 2006 (Yamanaka & Takahashi)", "hold_s": 3.5}),
            ("04_till_mcculloch_1961_gurdon_1962_yamanaka_2006_24_to_4_factor_reprogramming_chart", 17.5, 8.0, "E", False, "20,000 HUMAN GENES (~200 CELL TYPES) & YAMANAKA'S 24-TO-4 FACTOR FUNNEL (OCT3/4, SOX2, KLF4, C-MYC) REWINDING ADULT SKIN TO IPSC", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked cellular reprogramming & Yamanaka factor funnel chart from Till & McCulloch (February 1961 Radiation Research 14: 213–222), Gurdon (December 1962 J. Embryol. Exp. Morphol. 10: 622–640), and Takahashi & Yamanaka (25 August 2006 Cell 126: 663–676) shows all ~200 human cell types sharing the same 3-billion-base-pair genome (~20,000 genes), where narrowing 24 embryonic candidate genes down to just 4 transcription factors (Oct3/4, Sox2, Klf4, c-Myc) erases epigenetic bookmarks and rewinds adult fibroblasts into pluripotent stem cells.",
             {"kind": "DATA", "label": "1 EGG → ~200 CELL TYPES (2M RED CELLS/S) ← REWOUND BY 4 YAMANAKA FACTORS (FROM 24 CANDIDATES OUT OF 20,000 GENES)", "detail": "Inked cellular reprogramming & stem-cell hierarchy chart on period paper showing 1 fertilized egg → pluripotent embryonic stem cells (capable of becoming all ~200 human cell types) → multipotent adult hematopoietic stem cells (producing ~2 million red blood cells/second) ← rewound by Yamanaka's 4 transcription factors (from 24 candidates out of ~20,000 genes) back into Induced Pluripotent Stem Cells (iPSCs)", "scale": "out of the twenty thousand genes in your DNA book, flipping just four master switches is enough to erase a skin cell's memory of what it is and rewind its clock all the way back to day one", "who_card": "Ernest A. McCulloch (1926–2011) — Canadian physician · James E. Till (born 1931) — Canadian biophysicist · John B. Gurdon (born 1933) — British developmental biologist · Shinya Yamanaka (born 1962) — Japanese stem-cell scientist · Kazutoshi Takahashi (born 1977) — Japanese molecular biologist", "when_stamp": "February 1961 · December 1962 · 25 August 2006", "hold_s": 3.8}),
            ("05_glass_micropipette_xenopus_dish_24_well_plate_and_waddington_marble_board_pan", 25.5, 5.5, "A", False, "4 MASTER SWITCH GENES", "Fast",
             "Fast: daylight macro pan across a glass nuclear-transfer micropipette, a Petri dish, a 24-well culture plate, and a carved wooden Waddington landscape model on an oak laboratory bench between code graphics so two full-frame graphics never run back to back. Nothing emissive, no face.",
             STYLE + "In crisp daylight on an oak laboratory bench, the camera pans smoothly across a fine glass micropipette holder, a 24-well culture plate, a brass dissecting lens, and a carved wooden hill model with branching grooves." + FAST_TAIL,
             None),
            ("06_waddington_1957_epigenetic_landscape_vs_gurdon_1962_scnt_and_yamanaka_2006_4_factor_chart", 31.0, 8.0, "E", False, "REWINDING THE CELL'S CLOCK", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period parchment, an inked Waddington epigenetic landscape & reprogramming chart (from Conrad Waddington 1957 & Yamanaka 2012 Nobel Lecture) compares normal one-way embryonic differentiation (totipotent/pluripotent summit → ~200 specialized adult cell valleys locked by DNA methylation and histone marks) against somatic cell nuclear transfer (Gurdon 1962) and 4-factor iPSC reprogramming (Yamanaka 2006) pushing the adult cell back to the pluripotent summit.",
             {"kind": "DATA", "label": "WADDINGTON ONE-WAY EPIGENETIC HILL (~200 ADULT VALLEYS) VS GURDON SCNT (1962) & YAMANAKA 4-FACTOR IPSC SKI LIFT (2006)", "detail": "Inked Waddington epigenetic landscape & reprogramming chart comparing normal one-way embryonic differentiation (totipotent/pluripotent summit → ~200 specialized adult cell valleys locked by DNA methylation and histone marks) against somatic cell nuclear transfer (Gurdon 1962) and 4-factor iPSC reprogramming (Yamanaka 2006) pushing the adult cell back to the pluripotent summit", "scale": "for a hundred years biologists thought a specialized cell was like a boulder that had rolled to the bottom of a mountain and could never roll back up — until Gurdon and Yamanaka built a four-gene ski lift back to the top", "hold_s": 3.8}),
            ("07_table_three_props_toronto_1961_spleen_slide_gurdon_1962_micropipette_and_yamanaka_24_well_plate", 39.0, 5.5, "C", False, "1961 TO 2012", "Fast",
             "Fast: daylight prop table (callback source for Part 05: McCulloch & Till's 1961 stained spleen-colony slide box, John Gurdon's 1962 glass nuclear-transfer micropipette, and Yamanaka's 2006 24-well culture plate). Nothing emissive.",
             STYLE + "On an oak workbench in soft window light sit three objects side by side: a wooden box of stained microscope slides, a brass-mounted glass micropipette, and a clear 24-well cell culture tray." + FAST_TAIL,
             None),
            ("08_explorer_attaching_4_yamanaka_thrusters_to_push_marble_up_waddington_hill", 62.0, 5.5, "A", True, None, "Quality",
             "Quality: Explorer beat 1 (locked character reference, after 1:00).",
             STYLE + "Standing at the bottom of a steep grooved wooden hill, the Explorer clips four small brass clockwork winders onto a heavy glass marble and watches with a delighted grin as the marble rolls smoothly straight back up the slope to the summit turntable." + EXP_TAIL,
             None),
            ("09_john_gurdon_dec_1962_oxford_inspecting_cloned_xenopus_tadpoles_beneath_framed_school_report", 67.5, 5.5, "B", False, "OXFORD, DECEMBER 1962", "Quality",
             "Quality: readable face (at Oxford in December 1962, young British biologist John Gurdon peers through his dissecting microscope at swimming Xenopus tadpoles cloned from adult intestinal cells, while his framed 1949 Eton school report hangs on the wall behind him).",
             STYLE + "In a 1962 Oxford zoology laboratory, young John Gurdon in a tweed jacket and lab coat peers through a dissecting microscope at a glass dish of swimming frog tadpoles beneath a framed school report card on the oak wall." + QUAL_TAIL,
             {"kind": "WHEN", "label": "OXFORD, DECEMBER 1962", "timeline_step": "2/4 · Dec 1962 (John Gurdon clones swimming Xenopus frogs from differentiated intestinal cell nuclei)", "hold_s": 3.5}),
        ],
    ),
    (
        2,
        "Part 02 — February 1961 & February 1963: Ernest McCulloch, James Till & the Spleen Bumps That Proved Adult Stem Cells Exist",
        [
            ("01_waddington_1957_edinburgh_and_mcculloch_till_becker_1961_1963_toronto_spleen_colonies", 73.0, 6.5, "A", False, "1 CELL BUILDS ALL BLOOD TYPES", "Quality",
             "Quality: readable faces (British biologist Conrad Waddington in 1957 sketching an epigenetic hill, dissolving to Canadian physician Ernest McCulloch, biophysicist James Till, and Andrew Becker in Toronto in February 1961 – 2 February 1963 counting clonal blood-forming nodules on mouse spleens).",
             STYLE + "Split period scene: on the left in 1957 Edinburgh, Conrad Waddington sketches a marble rolling down branching valleys; on the right in 1961–1963 Toronto, Ernest McCulloch, James Till, and Andrew Becker inspect chromosome spreads and spleen nodules under a microscope." + QUAL_TAIL,
             {"kind": "FACT", "label": "1 cell builds all blood types", "who_card": "Conrad H. Waddington (1905–1975) — British developmental biologist · Andrew J. Becker (born 1936) — Canadian medical researcher", "when_stamp": "1957 · February 1961 · 2 February 1963", "timeline_step": "1/4 · Feb 1961 & Feb 1963 (Ernest McCulloch, James Till & Andrew Becker prove clonal self-renewing blood stem cells in mouse spleen colonies)", "hold_s": 3.8}),
            ("02_till_mcculloch_1961_1963_cfu_s_linear_dose_and_2m_rbc_per_sec_clonal_tree_chart", 79.5, 8.0, "E", False, "FEB 1961 & 2 FEB 1963 TILL, MCCULLOCH & BECKER: 1 CLONAL MARROW STEM CELL (~1 IN 10,000) → RED CELLS (2M/S), WHITE CELLS & PLATELETS", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked Till & McCulloch spleen-colony linear dose-response & clonal stem-cell chart from Till & McCulloch (February 1961, Radiation Research 14: 213–222) and Becker, McCulloch & Till (2 February 1963, Nature 197: 452–454) shows 1 bone-marrow hematopoietic stem cell (CFU-S, ~1 in 10,000 marrow cells) both self-renewing and differentiating into erythrocytes (2 million/sec), leukocytes, and megakaryocytes/platelets.",
             {"kind": "DATA", "label": "FEB 1961 & 2 FEB 1963: 1 BONE-MARROW STEM CELL (~1 IN 10,000) SELF-RENEWS & BUILDS 2 MILLION RED BLOOD CELLS/SECOND", "detail": "Inked Till & McCulloch spleen-colony linear dose-response & clonal stem-cell chart on period paper from Till & McCulloch (February 1961, Radiation Research 14: 213–222) and Becker, McCulloch & Till (2 February 1963, Nature 197: 452–454) showing 1 bone-marrow hematopoietic stem cell (CFU-S, ~1 in 10,000 marrow cells) both self-renewing and differentiating into erythrocytes (2 million/sec), leukocytes, and megakaryocytes/platelets", "scale": "only about one cell in every ten thousand inside your bone marrow is a true blood stem cell — yet that tiny handful of master cells manufactures two million fresh red blood cells every single second of your life", "hold_s": 3.8}),
            ("03_toronto_1963_chromosome_marker_spread_and_spleen_colony_counting_dish_closeup", 87.5, 6.5, "B", False, "2 FEBRUARY 1963 — ONE CELL BUILDS ALL BLOOD", "Fast",
             "Fast: daylight macro shot of a chromosome-marker karyotype photograph beside a glass dish with a millimeter grid and a brass tally counter on a 1963 Toronto workbench. Nothing emissive, no face.",
             STYLE + "In crisp daylight on a 1963 Toronto laboratory bench, a black-and-white chromosome karyotype print sits beside a glass grid dish, a brass hand tally counter, and a fountain pen." + FAST_TAIL,
             None),
            ("04_bone_marrow_cross_section_model_and_blood_smear_slides_pan", 94.0, 5.5, "C", False, "FEBRUARY 1961 — SPLEEN COLONIES", "Fast",
             "Fast: daylight close-up pan across an anatomical bone-marrow cross-section model and a tray of stained red-and-white blood smear slides beside a microscope. Nothing emissive, no face.",
             STYLE + "In bright window light on an oak bench, a painted anatomical model of spongy bone marrow sits beside a tray of stained blood smear slides and a binocular microscope." + FAST_TAIL,
             None),
        ],
    ),
    (
        3,
        "Part 03 — 1949 & December 1962: The Boy Ranked 250th Out of 250 Who Cloned a Frog From a Gut Cell — Midpoint Twist",
        [
            ("01_gurdon_1949_eton_report_dec_1962_oxford_cloned_xenopus_and_wilmut_campbell_1996_dolly", 99.5, 6.5, "A", False, "RANKED 250TH OF 250 IN BIOLOGY", "Quality",
             "Quality: readable faces (15-year-old John Gurdon in 1949 reading his biology report card, dissolving to John Gurdon in December 1962 at Oxford transplanting an adult frog intestinal cell nucleus into an enucleated Xenopus egg to hatch swimming cloned tadpoles, and Ian Wilmut and Keith Campbell on 5 July 1996 with Dolly the cloned sheep).",
             STYLE + "Split period scene: on the left in December 1962 Oxford, John Gurdon works at a micromanipulator beneath his framed 1949 school report while cloned Xenopus tadpoles swim in a glass dish; on the right in July 1996 Scotland, Ian Wilmut and Keith Campbell stand beside white Finn Dorset sheep Dolly." + QUAL_TAIL,
             {"kind": "FACT", "label": "Ranked 250th of 250 in biology", "who_card": "Ian Wilmut (1944–2023) — British embryologist · Keith H. S. Campbell (1954–2012) — British biologist", "when_stamp": "1949 · 1952 · December 1962 · 5 July 1996", "timeline_step": "2/4 · Dec 1962 (John Gurdon clones Xenopus frogs from intestinal nuclei) & 3/4 · 5 Jul 1996 (Wilmut & Campbell clone Dolly the sheep)", "hold_s": 3.8}),
            ("02_gurdon_dec_1962_xenopus_intestinal_scnt_and_dolly_5_jul_1996_genome_equivalence_chart", 106.0, 8.0, "E", False, "DEC 1962 GURDON (XENOPUS INTESTINAL SCNT) & 5 JUL 1996 WILMUT/CAMPBELL (DOLLY): ADULT SPECIALIZED CELLS RETAIN THE ENTIRE INTACT GENOME", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked somatic cell nuclear transfer (SCNT) diagram from Gurdon (December 1962, J. Embryol. Exp. Morphol. 10: 622–640) and Wilmut, Schnieke, McWhir, Kind & Campbell (27 February 1997, Nature 385: 810–813, Dolly born 5 July 1996) shows an enucleated egg cell reprogramming a differentiated adult intestinal (Xenopus) or mammary (sheep) nucleus back to totipotency.",
             {"kind": "DATA", "label": "DEC 1962 GURDON (FROG GUT NUCLEUS) & 5 JUL 1996 DOLLY THE SHEEP: ADULT CELLS RETAIN 100% OF THE 3B-LETTER GENOME", "detail": "Inked somatic cell nuclear transfer (SCNT) diagram on period paper from Gurdon (December 1962, J. Embryol. Exp. Morphol. 10: 622–640) and Wilmut, Schnieke, McWhir, Kind & Campbell (27 February 1997, Nature 385: 810–813, Dolly born 5 July 1996) showing an enucleated egg cell reprogramming a differentiated adult intestinal (Xenopus) or mammary (sheep) nucleus back to totipotency", "scale": "every single skin cell on your fingertip still carries the complete, unabridged instruction manual to build a beating heart, two eyes, and a brain — it has simply placed sticky notes over every chapter except 'How to Be Skin'", "hold_s": 3.8}),
            ("03_oxford_1962_framed_eton_report_card_and_xenopus_tadpole_dish_closeup", 114.0, 6.5, "B", False, "DECEMBER 1962 — ADULT DNA NEVER FORGETS", "Fast",
             "Fast: daylight macro shot of a framed vintage handwritten report card on an oak wall above a glass Petri dish of swimming tadpoles and a brass micromanipulator knob. Nothing emissive, no face.",
             STYLE + "In crisp daylight in an Oxford lab, the camera tilts from a framed vintage report card on an oak wall down to a glass dish of swimming frog tadpoles beside a brass micromanipulator." + FAST_TAIL,
             None),
            ("04_glass_nuclear_transfer_pipette_and_amphibian_embryo_stages_model_pan", 120.5, 5.5, "C", False, "5 JULY 1996 — DOLLY THE SHEEP", "Fast",
             "Fast: daylight close-up pan across a pulled glass micropipette needle and a row of carved wax models showing frog cleavage and tadpole stages on a wooden bench. Nothing emissive, no face.",
             STYLE + "In bright window light on a zoology bench, a fine glass micropipette in a brass clamp sits beside a row of painted wax models showing an egg dividing into a tadpole." + FAST_TAIL,
             None),
        ],
    ),
    (
        4,
        "Part 04 — 25 August 2006 & November 2007: Shinya Yamanaka's 24-Gene Hunt & the 4-Gene Time Machine (iPSCs)",
        [
            ("01_yamanaka_and_takahashi_25_aug_2006_kyoto_24_to_4_factors_ipsc_discovery", 126.0, 6.5, "A", False, "4 GENES REWIND ADULT SKIN", "Quality",
             "Quality: readable faces (Japanese stem-cell scientist Shinya Yamanaka and postdoctoral researcher Kazutoshi Takahashi at Kyoto University on 25 August 2006 & 30 November 2007 testing 24 candidate embryonic genes by one-by-one subtraction until 4 transcription factors Oct3/4, Sox2, Klf4, and c-Myc rewind adult skin fibroblasts into Induced Pluripotent Stem Cell colonies).",
             STYLE + "Split period scene: on the left in August 2006 Kyoto, Shinya Yamanaka and Kazutoshi Takahashi inspect a 24-well culture plate where subtracting single genes reveals the four essential Yamanaka Factors; on the right, reprogrammed human skin cells form round pluripotent stem-cell colonies that differentiate into beating red heart muscle." + QUAL_TAIL,
             {"kind": "FACT", "label": "4 genes rewind adult skin", "who_card": "James A. Thomson (born 1958) — American developmental biologist", "when_stamp": "November 1998 · 25 August 2006 · November 2007 · 2012", "timeline_step": "3/4 · Nov 1998 (James Thomson isolates human embryonic stem cells) & 4/4 · 25 Aug 2006 & Nov 2007 (Yamanaka & Takahashi 4-factor iPSCs; 2012 Nobel Prize)", "hold_s": 3.8}),
            ("02_takahashi_yamanaka_25_aug_2006_24_minus_1_subtraction_to_4_factors_ipsc_germ_layers_chart", 132.5, 8.0, "E", False, "25 AUG 2006 & 30 NOV 2007 TAKAHASHI & YAMANAKA: 24−1 SUBTRACTION → 4 FACTORS (OCT3/4, SOX2, KLF4, C-MYC) → IPSCS → ALL 3 GERM LAYERS", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked 24-to-4 factor subtraction & iPSC differentiation chart from Takahashi & Yamanaka (25 August 2006, Cell 126: 663–676) and Takahashi et al. & Yamanaka (30 November 2007, Cell 131: 861–872) shows 24 candidate embryonic genes narrowed by 24−1 elimination to 4 essential transcription factors (Oct3/4, Sox2, Klf4, c-Myc) reprogramming adult human dermal fibroblasts into iPSCs that differentiate into all 3 germ layers (neurons, cardiomyocytes, gut endoderm).",
             {"kind": "DATA", "label": "24 CANDIDATE GENES (24−1 SCREEN) → 4 YAMANAKA FACTORS (OCT3/4, SOX2, KLF4, C-MYC) REWIND SKIN TO IPSCS", "detail": "Inked 24-to-4 factor subtraction & iPSC differentiation chart on period paper from Takahashi & Yamanaka (25 August 2006, Cell 126: 663–676) and Takahashi et al. & Yamanaka (30 November 2007, Cell 131: 861–872) showing 24 candidate embryonic genes narrowed by 24−1 elimination to 4 essential transcription factors (Oct3/4, Sox2, Klf4, c-Myc) reprogramming adult human dermal fibroblasts into iPSCs that differentiate into all 3 germ layers (neurons, cardiomyocytes, gut endoderm)", "scale": "testing twenty-four genes one by one yielded zero stem cells — because cellular reprogramming is like a four-dial combination vault that only swings open when all four Yamanaka dials are turned together", "hold_s": 3.8}),
            ("03_kyoto_2006_24_well_subtraction_plate_pipette_and_cardiomyocyte_dish_closeup", 140.5, 6.5, "B", False, "SKIN CELLS REWOUND INTO HEART MUSCLE", "Fast",
             "Fast: daylight macro shot of a 24-well cell-culture plate beside a precision micropipette rack and an anatomical model of red heart-muscle fibres on a Kyoto workbench. Nothing emissive, no face.",
             STYLE + "In crisp daylight on a Kyoto laboratory bench, a clear 24-well culture plate sits beside a rack of precision pipettes and a detailed anatomical model of branching red heart-muscle fibres." + FAST_TAIL,
             None),
            ("04_explorer_spinning_4_yamanaka_combination_dials_on_epigenetic_vault_door", 147.0, 5.5, "B", True, None, "Quality",
             "Quality: Explorer beat 2 (locked character reference).",
             STYLE + "Standing before a grand brass vault door with four large combination wheels, the Explorer turns all four dials into alignment and swings the heavy door open to reveal a bright workshop of pulsing red heart-muscle models and branching golden nerve trees." + EXP_TAIL,
             None),
        ],
    ),
    (
        5,
        "Part 05 — Why Your DNA Never Deletes Its Chapters — & the Countdown Clock That Makes Us Age",
        [
            ("01_timeline_1961_2012_and_epigenetic_bookmarks_on_3b_letter_dna_encyclopedia_chart", 152.5, 8.5, "E", False, "1961–2012 TIMELINE · MCCULLOCH & TILL MARROW STEM CELLS, GURDON CLONED FROGS, DOLLY THE SHEEP & YAMANAKA 4-GENE IPSCS", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, the 4-date timeline completes: Feb 1961 & Feb 1963 (Ernest McCulloch & James Till prove self-renewing multipotent blood stem cells in mouse spleen colonies) · Dec 1962 (John Gurdon clones swimming Xenopus frogs from differentiated intestinal cell nuclei, proving adult cells retain the full genome) · 5 Jul 1996 & Nov 1998 (Wilmut & Campbell clone Dolly the sheep; James Thomson isolates human embryonic stem cells) · 25 Aug 2006 & Nov 2007 (Shinya Yamanaka & Kazutoshi Takahashi reprogram mouse and human adult skin fibroblasts into iPSCs using 4 transcription factors: Oct3/4, Sox2, Klf4, c-Myc; 2012 Nobel Prize with Gurdon).",
             {"kind": "DATA", "label": "1961–2012 STEM CELL TIMELINE · SAME 20,000-GENE DNA BOOK IN EVERY CELL, REWOUND BY 4 YAMANAKA FACTORS", "detail": "Animated 4-date timeline (1961 → 2012) alongside the 3-billion-letter DNA encyclopedia & epigenetic bookmark removal diagram", "scale": "a boy who finished two-hundred-and-fiftieth out of two hundred and fifty in school biology and a surgeon hunting for four genetic switches proved that no cell in your body ever forgets where it came from", "when_stamp": "1961–2012", "timeline_step": "4/4 · 1961–2012 timeline complete", "hold_s": 3.8}),
            ("02_leather_dna_encyclopedia_volumes_with_ribbon_bookmarks_and_4_brass_keys_on_plinth_pan", 161.0, 5.5, "A", False, "SAME DNA BOOK, DIFFERENT BOOKMARKS", "Fast",
             "Fast: daylight close-up of leather-bound DNA encyclopedia volumes with coloured ribbon bookmarks beside four brass master keys on a wooden museum plinth. Nothing emissive, no face.",
             STYLE + "In crisp daylight on a wooden museum plinth, a set of leather-bound encyclopedia volumes with coloured ribbon bookmarks sits beside four polished brass keys and a glass culture dish." + FAST_TAIL,
             None),
            ("03_hayflick_dec_1961_50_division_limit_and_blackburn_greider_25_dec_1984_telomerase_handoff", 166.5, 6.5, "C", False, "50 DIVISIONS & TELOMERE CAPS", "Quality",
             "Quality: readable faces (Leonard Hayflick in December 1961 in Philadelphia discovering the 50-division Hayflick Limit in human fibroblasts, alongside Elizabeth Blackburn and Carol Greider at Berkeley on Christmas Day, 25 December 1984 discovering the telomere-rebuilding enzyme telomerase — handoff to 059 Telomeres & Aging).",
             STYLE + "Split period scene: on the left in December 1961 Philadelphia, Leonard Hayflick compares a vigorous young cell flask with a flask halted after fifty divisions; on the right on 25 December 1984 Berkeley, Elizabeth Blackburn and Carol Greider inspect an autoradiogram showing repeating six-letter telomere caps built by telomerase." + QUAL_TAIL,
             {"kind": "WHEN", "label": "DECEMBER 1961 · 25 DECEMBER 1984", "hold_s": 3.5}),
            ("04_table_three_callback", 173.0, 2.4, "C", False, None, "reuse",
             "Reuse: verified unused moving window [5.50s..7.90s] of P1:07_table_three_props_toronto_1961_spleen_slide_gurdon_1962_micropipette_and_yamanaka_24_well_plate (callback, £0).",
             "Reuse P1:07_table_three_props_toronto_1961_spleen_slide_gurdon_1962_micropipette_and_yamanaka_24_well_plate [5.50s..7.90s] (2.40s distinct non-overlapping tail window from 8.00s source clip).",
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
                row["reuse_of"] = "P1:07_table_three_props_toronto_1961_spleen_slide_gurdon_1962_micropipette_and_yamanaka_24_well_plate"
                row["reuse_window_s"] = [5.5, 7.9]
                row["reuse_audit"] = {
                    "source_row": "P1:07_table_three_props_toronto_1961_spleen_slide_gurdon_1962_micropipette_and_yamanaka_24_well_plate",
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
            "film": "058_McCulloch-Gurdon-Yamanaka-Stem-Cells-iPSCs",
            "part": p_idx,
            "title": p_title,
            "version": "v01",
            "timing_status": "pre_vo_script_clock (built from stem_cells_script_master_v01.md; retimes onto Scribe STT once VO locks)",
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
        "film": "058_McCulloch-Gurdon-Yamanaka-Stem-Cells-iPSCs",
        "version": "v01",
        "date": "2026-10-19",
        "owner": "gemini (J0615)",
        "status": "PRE_VO_BOARDS_V01_NO_MINT",
        "generation_authorized": False,
        "script": "00_Brand/Channel-Setup/ideas/058_McCulloch-Gurdon-Yamanaka-Stem-Cells-iPSCs/stem_cells_script_master_v01.md",
        "sources": "00_Brand/Channel-Setup/ideas/058_McCulloch-Gurdon-Yamanaka-Stem-Cells-iPSCs/SOURCES_v01.md",
        "credit_snapshot": {
            "flow_balance": 23740,
            "flow_floor": 0,
            "flow_read_at": "2026-10-15T21:42:22Z",
            "vertex_promo_gbp": 71.02,
            "vertex_usable_gbp": 70.02,
        },
        "totals": totals,
        "per_part": per_part_summary,
        "mint_order": "006 > 007 > 008 > 009 > 010 > 011 > 012 > 013 > 014 > 015 > 016 > 017 > 018 > 019 > 020 > 021 > 022 > 023 > 024 > 025 > 026 > 027 > 028 > 029 > 030 > 031 > 032 > 033 > 034 > 035 > 036 > 037 > 038 > 039 > 040 > 041 > 042 > 043 > 044 > 045 > 046 > 047 > 048 > 049 > 050 > 051 > 052 > 053 > 054 > 055 > 056 > 057 > 058 > 059. Nothing in 058 is generation_authorized.",
    }
    (EDIT / "PICTURE_PLAN_v01.json").write_text(json.dumps(plan, indent=2) + "\n")

    sl = [
        "# 058 Stem Cells: How Scientists Rewound an Adult Cell — Shot list & plate boards v01 (pre-VO)",
        "",
        "Gemini, 19 Oct 2026, J0615. Built from `stem_cells_script_master_v01.md` (`91.8 PASS`) and `SOURCES_v01.md`.",
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
        "# 058 price review v01 (pre-VO plate boards)",
        "",
        "Gemini, 19 Oct 2026, J0615. Boards only. **No mint. No spend. No merge.**",
        "Prepared from `stem_cells_script_master_v01.md` (`91.8 PASS`) and `SOURCES_v01.md` so 058's full plate board rows, non-emissive Fast prompts, £0 code graphics, and Teach-on-Screen overlays are ready to re-time the moment long VO locks. Parked for Chief.",
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
        f"- **Quality ({totals['Quality']} rows):** readable faces (Ernest A. McCulloch, James E. Till, Conrad H. Waddington, Andrew J. Becker, John B. Gurdon, Ian Wilmut, Keith H. S. Campbell, James A. Thomson, Shinya Yamanaka, Kazutoshi Takahashi, Leonard Hayflick, Elizabeth Blackburn, Carol Greider), February 1961 – 2 February 1963 Toronto mouse spleen-colony stem cell proof, December 1962 Oxford *Xenopus* nuclear transfer & 5 July 1996 Dolly the sheep, 25 August 2006 – 30 November 2007 Kyoto 4-factor iPSC discovery, and the 2 Explorer beats.",
        f"- **Fast ({totals['Fast']} rows, non-emissive):** daylight prop and laboratory shots (glass micropipette, 24-well plate & carved wooden Waddington hill model pan, 3-object callback bench, 1963 chromosome-marker print & tally counter, bone-marrow cross-section model & blood smear slides, framed 1949 Eton report card & swimming tadpole dish, pulled glass micropipette & wax amphibian cleavage models, 24-well subtraction plate & red heart-muscle fibre model, leather-bound DNA encyclopedia volumes with ribbon bookmarks & 4 brass keys on museum plinth). Zero candles, flames, sparks, or glowing elements on Fast.",
        f"- **£0 code graphics ({totals['code_graphic']} rows):**",
        "  1. `P1:04_till_mcculloch_1961_gurdon_1962_yamanaka_2006_24_to_4_factor_reprogramming_chart` — cellular reprogramming & stem-cell hierarchy chart showing 1 fertilized egg → ~200 cell types (~2M red blood cells/sec) ← rewound by Yamanaka's 4 transcription factors (from 24 candidates out of ~20,000 genes) back into iPSCs (`SCALE: out of the twenty thousand genes in your DNA book, flipping just four master switches is enough to erase a skin cell's memory of what it is and rewind its clock all the way back to day one`)",
        "  2. `P1:06_waddington_1957_epigenetic_landscape_vs_gurdon_1962_scnt_and_yamanaka_2006_4_factor_chart` — Waddington 1957 one-way epigenetic hill (~200 specialized valleys) vs Gurdon 1962 SCNT & Yamanaka 2006 4-factor iPSC reprogramming (`SCALE: for a hundred years biologists thought a specialized cell was like a boulder that had rolled to the bottom of a mountain and could never roll back up — until Gurdon and Yamanaka built a four-gene ski lift back to the top`)",
        "  3. `P2:02_till_mcculloch_1961_1963_cfu_s_linear_dose_and_2m_rbc_per_sec_clonal_tree_chart` — Till, McCulloch & Becker (Feb 1961 & 2 Feb 1963) spleen-colony linear dose-response & clonal stem-cell chart (~1 in 10,000 marrow cells self-renewing and producing 2M red blood cells/sec, white cells & platelets) (`SCALE: only about one cell in every ten thousand inside your bone marrow is a true blood stem cell — yet that tiny handful of master cells manufactures two million fresh red blood cells every single second of your life`)",
        "  4. `P3:02_gurdon_dec_1962_xenopus_intestinal_scnt_and_dolly_5_jul_1996_genome_equivalence_chart` — Gurdon (Dec 1962) *Xenopus* intestinal SCNT and Wilmut & Campbell (5 Jul 1996) Dolly the sheep somatic cell nuclear transfer chart proving adult cells retain 100% of the genome (`SCALE: every single skin cell on your fingertip still carries the complete, unabridged instruction manual to build a beating heart, two eyes, and a brain — it has simply placed sticky notes over every chapter except 'How to Be Skin'`)",
        "  5. `P4:02_takahashi_yamanaka_25_aug_2006_24_minus_1_subtraction_to_4_factors_ipsc_germ_layers_chart` — Takahashi & Yamanaka (25 Aug 2006 & 30 Nov 2007, *Cell*) 24−1 factor subtraction screen isolating Oct3/4, Sox2, Klf4 & c-Myc to reprogram adult skin fibroblasts into all 3 germ layers (`SCALE: testing twenty-four genes one by one yielded zero stem cells — because cellular reprogramming is like a four-dial combination vault that only swings open when all four Yamanaka dials are turned together`)",
        "  6. `P5:01_timeline_1961_2012_and_epigenetic_bookmarks_on_3b_letter_dna_encyclopedia_chart` — completed 4-date timeline (1961 → 2012) + 3-billion-letter DNA encyclopedia & epigenetic bookmark removal diagram (`SCALE: a boy who finished two-hundred-and-fiftieth out of two hundred and fifty in school biology and a surgeon hunting for four genetic switches proved that no cell in your body ever forgets where it came from`)",
        f"- **£0 verified reuse ({totals['reuse']} row):** `P5:04_table_three_callback` uses the 2.40 s unused moving tail `[5.50s..7.90s]` of `P1:07_table_three_props_toronto_1961_spleen_slide_gurdon_1962_micropipette_and_yamanaka_24_well_plate`.",
        "",
        "## Mint order",
        "",
        "006 > 007 > 008 > 009 > 010 > 011 > 012 > 013 > 014 > 015 > 016 > 017 > 018 > 019 > 020 > 021 > 022 > 023 > 024 > 025 > 026 > 027 > 028 > 029 > 030 > 031 > 032 > 033 > 034 > 035 > 036 > 037 > 038 > 039 > 040 > 041 > 042 > 043 > 044 > 045 > 046 > 047 > 048 > 049 > 050 > 051 > 052 > 053 > 054 > 055 > 056 > 057 > 058 > 059. `generation_authorized` is `false` on every row.",
    ])
    (EDIT / "PRICE_REVIEW_v01.md").write_text("\n".join(pr_lines) + "\n")
    print(f"058 v01 boards written: {totals['rows']} rows, Flow expected={totals['flow_credits_expected']}")


if __name__ == "__main__":
    main()
