#!/usr/bin/env python3
"""HOS 066 (Cancer Genes: The Stuck Gas Pedal Inside Your Own DNA) pre-VO plate boards v01. J0661. No mint, no spend.

Built from 00_Brand/Channel-Setup/ideas/066_Rous-Knudson-Bishop-Varmus-Lane-Cancer-Oncogenes-p53/cancer_script_master_v01.md
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
        "Part 01 — The Chicken Virus in New York & the Stuck Gas Pedal Inside Your Own DNA",
        [
            ("01_dividing_cell_dna_stuck_oncogene_gas_pedal_and_snapped_rb1_p53_brake_levers", 0.0, 5.5, "A", False, "STUCK ACCELERATOR & CUT BRAKES", "Quality",
             "Quality: Short frame 0 / answer image (0:03) + inside a dividing human cell nucleus, a DNA double helix displays a green growth-accelerator pedal and two red emergency brake levers; when a mutation jams the green pedal down and snaps both brake levers, the cell divides out of control while a five-ton elephant stands beside forty golden brake shields.",
             STYLE + "Split cellular-and-comparative scene: on the left, inside a cell nucleus, a brass green accelerator pedal jams to the floor while two red hydraulic brake cables snap on a dividing DNA helix; on the right, an African elephant stands guarded by forty golden four-part shield rings." + QUAL_TAIL,
             {"kind": "WHEN", "label": "NEW YORK, 21 JANUARY 1911", "timeline_step": "1/4 · 21 Jan 1911 (Peyton Rous filters the first cancer-causing retrovirus, Rous Sarcoma Virus, waiting 55 years for his 1966 Nobel Prize)", "hold_s": 3.5}),
            ("02_rous_1911_knudson_1971_bishop_varmus_1976_and_lane_levine_old_1979_split", 5.5, 6.0, "B", False, "RSV VIRUS, PROTO-ONCOGENES, P53 GUARDIAN", "Quality",
             "Quality: complex three-part composition (Peyton Rous in New York on 21 January 1911 passing fluid from a barred Plymouth Rock hen's sarcoma through a porcelain filter; Alfred Knudson in Houston in April 1971 plotting his Two-Hit retinoblastoma curve alongside Michael Bishop and Harold Varmus at UCSF in March 1976; and David Lane, Arnold Levine, and Lloyd Old in May 1979 discovering the p53 guardian protein).",
             STYLE + "Three-panel period composition: on the left, Peyton Rous in 1911 New York filtering chicken tumour fluid beside a barred Plymouth Rock hen; in the centre, Alfred Knudson in 1971 Houston plotting a two-hit curve alongside Michael Bishop and Harold Varmus in 1976 San Francisco; on the right, David Lane, Arnold Levine, and Lloyd Old in 1979 inspecting a four-part p53 guardian clamp on DNA." + QUAL_TAIL,
             None),
            ("03_tetrameric_p53_guardian_clamp_scanning_dividing_cell_dna_at_checkpoint_gate", 11.5, 6.0, "C", False, "GUARDING 37 TRILLION CELLS", "Quality",
             "Quality: complex conceptual and molecular reveal (a healthy dividing cell pauses at a checkpoint gate as the four-part p53 guardian protein scans the DNA double helix for damage before allowing division to proceed).",
             STYLE + "Inside a luminous cell nucleus, a sculpted golden four-part p53 guardian complex slides along a spiralling DNA double helix at a brass checkpoint gate, pausing over a nicked rung while repair enzymes stitch the strand back together." + QUAL_TAIL,
             {"kind": "WHEN", "label": "21 JANUARY 1911 · APRIL 1971 · 11 MARCH 1976 · MAY 1979", "timeline_step": "1/4 · 21 Jan 1911 (Peyton Rous RSV) · 2/4 · Apr 1971 & Oct 1986 (Knudson Two-Hit & RB1) · 3/4 · 11 Mar 1976 (Bishop & Varmus c-src) · 4/4 · May 1979, Apr 1989 & Oct 2015 (p53 & Elephant Peto's Paradox)", "hold_s": 3.5}),
            ("04_rous_1911_knudson_1971_bishop_varmus_1976_lane_vogelstein_p53_accelerator_vs_brakes_chart", 17.5, 8.0, "E", False, "PROTO-ONCOGENE ACCELERATOR (1 HIT: C-SRC / RAS) VS TUMOUR-SUPPRESSOR BRAKES (2 HITS: RB1 & TP53, BROKEN IN >50% OF CANCERS)", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked Proto-Oncogene Accelerator vs Tumour-Suppressor Two-Hit Brake chart from Rous (21 January 1911 J. Exp. Med. 13: 397–411), Knudson (April 1971 PNAS 68: 820–823), Stehelin, Varmus, Bishop & Vogt (11 March 1976 Nature 260: 170–173), and Lane & Crawford / Linzer & Levine (March–May 1979 Nature 278: 261–263 & Cell 17: 43–52) compares a dominant gain-of-function mutation in 1 allele of a proto-oncogene (c-src / RAS -> stuck accelerator) against recessive loss-of-function two-hit mutations required to disable both maternal and paternal alleles of a tumour suppressor (RB1 / TP53 -> cut brakes, with TP53 mutated in >50% of human cancers).",
             {"kind": "DATA", "label": "ONCOGENE STUCK GAS PEDAL (1 MUTATED ALLELE: C-SRC / HRAS) + TUMOUR-SUPPRESSOR CUT BRAKES (2 HITS: RB1 & TP53 IN >50% OF CANCERS)", "detail": "Inked accelerator vs dual-brake cancer genetics chart on period paper showing proto-oncogene activation (1 mutated allele = stuck gas pedal, e.g. c-src or HRAS codon 12 G->T single-letter typo) plus Knudson's Two-Hit tumour-suppressor inactivation (both maternal and paternal alleles of RB1 or TP53 cut, with p53 broken in >50% of human cancers)", "scale": "turning a healthy cell into a tumour is like a runaway car — it takes a stuck gas pedal in a single growth gene plus cutting both independent emergency brake cables", "who_card": "Peyton Rous (1879–1970) — American experimental pathologist · Alfred G. Knudson Jr. (1922–2016) — American physician and cancer geneticist · J. Michael Bishop (born 1936) — American virologist and molecular biologist · Harold E. Varmus (born 1939) — American virologist and cancer biologist · Dominique Stehelin (born 1943) — French molecular oncologist · David P. Lane (born 1952) — British molecular oncologist · Arnold J. Levine (born 1939) — American molecular biologist · Lloyd J. Old (1933–2011) — American cancer immunologist", "when_stamp": "21 January 1911 · April 1971 · 11 March 1976 · May 1979", "hold_s": 3.8}),
            ("05_berkefeld_filter_candle_retinoblastoma_graph_and_brass_pedal_brake_model_pan", 25.5, 5.5, "A", False, "STUCK PEDAL + TWO CUT BRAKES", "Fast",
             "Fast: daylight macro pan across a 1911 Berkefeld porcelain filter candle, a plotted two-hit logarithmic graph, and a brass accelerator-and-dual-brake mechanical model on an oak bench between code graphics so two full-frame graphics never run back to back. Nothing emissive, no face.",
             STYLE + "In crisp daylight on an oak pathology bench, the camera pans smoothly across a white Berkefeld porcelain filter candle in a glass flask, an inked logarithmic graph, and a brass pedal-and-twin-brake mechanism." + FAST_TAIL,
             None),
            ("06_peto_1977_abegglen_schiffman_maley_lynch_2015_elephant_40_tp53_alleles_chart", 31.0, 8.0, "E", False, "40 COPIES OF THE P53 BRAKE", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period parchment, an inked Peto's Paradox & Elephant TP53 Copy-Number chart (from Peto 1977 & Abegglen, Schiffman, Maley & Lynch et al., 8 October 2015 JAMA 314: 1850–1860) compares humans (1 copy / 2 alleles of TP53, ~11–25% cancer mortality across ~37 trillion cells) against African and Asian elephants (100x more cells than humans, yet <4.8% cancer mortality because elephants carry 20 copies / 40 alleles of TP53 that trigger rapid apoptosis of DNA-damaged cells).",
             {"kind": "DATA", "label": "PETO'S PARADOX (JAMA 2015): HUMANS (2 TP53 ALLELES, ~11–25% CANCER MORTALITY) VS ELEPHANTS (100× CELLS, 40 TP53 ALLELES, <5% MORTALITY)", "detail": "Inked Peto's Paradox chart comparing human TP53 gene copies (1 locus = 2 alleles, ~11–25% lifetime cancer mortality across ~37 trillion cells) vs elephant TP53 copies (20 loci = 40 alleles across ~100x more cells, <4.8% cancer mortality via hyper-sensitive p53 DNA-damage self-destruction)", "scale": "an elephant has a hundred times more cells than you do, yet because every elephant cell carries forty copies of the p53 brake gene instead of two, elephants almost never get cancer", "hold_s": 3.8}),
            ("07_table_three_props_1911_berkefeld_filter_1971_two_hit_chart_and_p53_tetramer_model", 39.0, 5.5, "C", False, "1911 TO 2015", "Fast",
             "Fast: daylight prop table (callback source for Part 05: Peyton Rous's 1911 Berkefeld filter flask, Alfred Knudson's 1971 semi-log two-hit chart, and a sculpted golden four-part p53 guardian model). Nothing emissive.",
             STYLE + "On an oak workbench in soft window light sit three objects side by side: a white porcelain Berkefeld filter candle in a glass flask, a framed two-hit logarithmic graph, and a sculpted four-part brass p53 DNA clamp model." + FAST_TAIL,
             None),
            ("08_explorer_prying_up_stuck_oncogene_gas_pedal_and_pulling_p53_guardian_brake_in_brass_car", 62.0, 5.5, "A", True, None, "Quality",
             "Quality: Explorer beat 1 (locked character reference, after 1:00).",
             STYLE + "Sitting inside a vintage brass motorcar representing a dividing cell, the Explorer pries up a jammed green accelerator pedal with one hand while pulling a four-part brass emergency brake lever with the other to bring the car smoothly to a halt." + EXP_TAIL,
             None),
            ("09_peyton_rous_21_jan_1911_new_york_filtering_chicken_sarcoma_extract", 67.5, 5.5, "B", False, "NEW YORK, 21 JANUARY 1911", "Quality",
             "Quality: readable face (in New York on 21 January 1911, 31-year-old Peyton Rous at his Rockefeller Institute workbench pours cell-free tumour extract through a Berkefeld filter candle).",
             STYLE + "In a 1911 Rockefeller Institute laboratory in New York, young American pathologist Peyton Rous pours clear fluid through a white porcelain Berkefeld filter candle into a glass Erlenmeyer flask beside a barred Plymouth Rock hen." + QUAL_TAIL,
             {"kind": "WHEN", "label": "NEW YORK, 21 JANUARY 1911", "timeline_step": "1/4 · 21 Jan 1911 (Peyton Rous proves cell-free transmission of chicken sarcoma via Rous Sarcoma Virus)", "hold_s": 3.5}),
        ],
    ),
    (
        2,
        "Part 02 — 21 January 1911 & 11 March 1976: Peyton Rous's 55-Year Wait & Bishop and Varmus's Proto-Oncogene Shock",
        [
            ("01_peyton_rous_1911_new_york_and_bishop_varmus_stehelin_vogt_11_mar_1976_ucsf_c_src", 73.0, 6.5, "A", False, "CANCER GENES ARE OUR OWN GENES", "Quality",
             "Quality: readable faces (Peyton Rous on 21 January 1911 demonstrating cell-free transmission of chicken sarcoma, dissolving to J. Michael Bishop, Harold Varmus, Dominique Stehelin, and Peter Vogt on 11 March 1976 hybridizing viral src cDNA probes to normal uninfected vertebrate DNA).",
             STYLE + "Split period scene: on the left in 1911 New York, Peyton Rous holds a Berkefeld filter flask beside a Plymouth Rock hen; on the right in March 1976 San Francisco, Michael Bishop, Harold Varmus, Dominique Stehelin, and Peter Vogt inspect DNA hybridization curves showing c-src inside normal cells." + QUAL_TAIL,
             {"kind": "FACT", "label": "Cancer genes are our own genes", "who_card": "Peter K. Vogt (born 1932) — German-American virologist and geneticist · Robert A. Weinberg (born 1942) — American cancer biologist", "when_stamp": "1775 · 21 January 1911 · 1966 · 1970 · 11 March 1976 · 1982 · 1989", "timeline_step": "3/4 · 11 Mar 1976 (Stehelin, Varmus, Bishop & Vogt prove viral src is a captured normal cellular proto-oncogene c-src; 1989 Nobel Prize)", "hold_s": 3.8}),
            ("02_stehelin_varmus_bishop_vogt_11_mar_1976_nature_c_src_hybridization_and_hras_chart", 79.5, 8.0, "E", False, "11 MAR 1976 STEHELIN, VARMUS, BISHOP & VOGT (NATURE 260: 170–173): VIRAL V-SRC IS STOLEN CELLULAR PROTO-ONCOGENE C-SRC + 1982 HUMAN HRAS CODON 12 G→T TYPO", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked Stehelin, Varmus, Bishop & Vogt (11 March 1976, Nature 260: 170–173) radioactive cDNA hybridization curve shows viral v-src probe binding strongly to uninfected normal chicken, duck, quail, turkey, and emu cellular DNA (proving c-src is a conserved vertebrate proto-oncogene, plus Weinberg/Barbacid 1982 single G->T codon 12 mutation in human HRAS).",
             {"kind": "DATA", "label": "11 MAR 1976 BISHOP & VARMUS (NATURE): VIRAL SRC HYBRIDIZES TO NORMAL CELLULAR C-SRC PROTO-ONCOGENE + 1982 HUMAN HRAS G→T TYPO", "detail": "Inked Stehelin, Varmus, Bishop & Vogt (11 March 1976, Nature 260: 170–173) radioactive cDNA hybridization curve on period paper showing viral v-src probe binding strongly to uninfected normal chicken, duck, quail, turkey, and emu cellular DNA (proving c-src is a conserved vertebrate proto-oncogene, plus Weinberg/Barbacid 1982 single G->T codon 12 mutation in human HRAS)", "scale": "Peyton Rous's virus didn't bring an alien poison into the cell — like a car thief who hot-wires your own ignition, it stole a normal growth gene that every healthy cell uses to heal wounds and welded the gas pedal to the floor", "hold_s": 3.8}),
            ("03_ucsf_1976_c_src_autoradiograph_and_1982_hras_sequencing_gel_closeup", 87.5, 6.5, "B", False, "11 MARCH 1976 — PROTO-ONCOGENES DISCOVERED", "Fast",
             "Fast: daylight macro shot of a 1976 DNA hybridization plot beside a 1982 sequencing gel strip and a March 1976 Nature offprint on a wooden bench. Nothing emissive, no face.",
             STYLE + "In crisp daylight on a 1976 San Francisco laboratory bench, a plotted DNA hybridization curve rests beside a glass autoradiograph plate and a printed scientific journal." + FAST_TAIL,
             None),
            ("04_normal_wound_healing_switch_vs_jammed_oncogene_accelerator_pedal_model_pan", 94.0, 5.5, "C", False, "NORMAL GROWTH SWITCH VS STUCK GAS PEDAL", "Fast",
             "Fast: daylight close-up pan across two brass mechanical pedals on an oak table: one spring-loaded pedal that returns cleanly to rest, and a second pedal jammed down by a wedged bolt. Nothing emissive, no face.",
             STYLE + "In bright window light on an oak table, two brass mechanical foot pedals sit side by side: one balanced on a clean return spring, and the other wedged flat to the floor by a heavy brass bolt." + FAST_TAIL,
             None),
        ],
    ),
    (
        3,
        "Part 03 — April 1971 & 16 October 1986: Alfred Knudson's 'Two-Hit' Equation & the Discovery of Tumour Suppressor Brakes — Midpoint Twist",
        [
            ("01_alfred_knudson_apr_1971_houston_two_hit_graph_and_dryja_weinberg_16_oct_1986_rb1", 99.5, 6.5, "A", False, "TWO BRAKE CABLES IN EVERY CELL", "Quality",
             "Quality: readable faces (American paediatric geneticist Alfred G. Knudson Jr. in Houston in April 1971 plotting 48 retinoblastoma cases on a semi-log graph, dissolving to Thaddeus Dryja, Stephen Friend, and Robert Weinberg in Boston on 16 October 1986 cloning the RB1 tumour-suppressor gene).",
             STYLE + "Split period scene: on the left in April 1971 Houston, Alfred Knudson plots a straight one-hit line and a curved two-hit line on a graph of 48 childhood eye-cancer cases; on the right in October 1986 Boston, Thaddeus Dryja and Robert Weinberg inspect chromosome 13 RB1 DNA bands." + QUAL_TAIL,
             {"kind": "FACT", "label": "Two brake cables in every cell", "who_card": "Thaddeus P. Dryja (born 1940) — American ophthalmologist and geneticist", "when_stamp": "1969 · April 1971 · 1983 · 16 October 1986", "timeline_step": "2/4 · Apr 1971 & 16 Oct 1986 (Alfred Knudson publishes the Two-Hit retinoblastoma equation; Friend, Weinberg & Dryja clone the RB1 tumour suppressor)", "hold_s": 3.8}),
            ("02_knudson_apr_1971_pnas_48_case_retinoblastoma_one_hit_vs_two_hit_survival_curve_chart", 106.0, 8.0, "E", False, "APR 1971 KNUDSON (PNAS 68: 820–823): 48 RETINOBLASTOMA CASES → BILATERAL HEREDITARY 1-HIT LINE VS UNILATERAL SPORADIC 2-HIT CURVE (BOTH RB1 ALLELES CUT)", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked Knudson (April 1971, PNAS 68: 820–823) semi-logarithmic retinoblastoma survival curve plots 48 bilateral (hereditary, one-hit linear exponential log S = -kt, mean 3 tumours) vs unilateral (non-hereditary, two-hit quadratic curve, 1 tumour) cases, proving recessive two-hit inactivation of both maternal and paternal RB1 alleles.",
             {"kind": "DATA", "label": "APR 1971 KNUDSON TWO-HIT CURVE (48 CASES, PNAS): HEREDITARY 1-HIT LINE VS SPORADIC 2-HIT CURVE (2 RB1 BRAKE CABLES PER CELL)", "detail": "Inked Knudson (April 1971, PNAS 68: 820–823) semi-logarithmic retinoblastoma survival curve on period paper plotting 48 bilateral (hereditary, one-hit linear exponential log S = -kt, mean 3 tumors) vs unilateral (non-hereditary, two-hit quadratic curve, 1 tumor) cases, proving recessive two-hit inactivation of both maternal and paternal RB1 alleles", "scale": "having two copies of every tumour-suppressor gene is like flying on an airliner with twin backup hydraulic brakes — if random chance cuts one cable in a million cells, the backup cable still stops the plane, unless lightning strikes the exact same cell twice", "hold_s": 3.8}),
            ("03_boston_1986_chromosome_13_rb1_southern_blot_and_twin_brake_cable_model_closeup", 114.0, 6.5, "B", False, "APRIL 1971 — KNUDSON'S TWO-HIT HYPOTHESIS", "Fast",
             "Fast: daylight macro shot of a 1986 chromosome 13q14 RB1 Southern blot autoradiograph beside a pair of braided steel brake cables mounted on a wooden block. Nothing emissive, no face.",
             STYLE + "In crisp daylight on a 1986 genetics bench, a monochrome DNA Southern blot film sits beside a demonstration rig of two parallel braided brass brake cables." + FAST_TAIL,
             None),
            ("04_maternal_and_paternal_chromosome_13_pair_wooden_models_with_rb1_locks_pan", 120.5, 5.5, "C", False, "16 OCTOBER 1986 — THE RB1 BRAKE GENE", "Fast",
             "Fast: daylight close-up pan across two carved wooden chromosome 13 models each fitted with a brass RB1 brake clasp on an oak table. Nothing emissive, no face.",
             STYLE + "In bright window light on an oak table, two matched wooden chromosome models lie side by side, each secured at its midpoint by a heavy brass brake clasp." + FAST_TAIL,
             None),
        ],
    ),
    (
        4,
        "Part 04 — May 1979, 14 April 1989 & 8 October 2015: p53 ('The Guardian of the Genome') & Why Giant Elephants Almost Never Get Cancer (Peto's Paradox)",
        [
            ("01_lane_levine_old_may_1979_vogelstein_1989_and_schiffman_lynch_oct_2015_elephant_p53", 126.0, 6.5, "A", False, "ELEPHANTS CARRY 40 P53 ALLELES", "Quality",
             "Quality: readable faces (David Lane, Arnold Levine, and Lloyd Old in March–May 1979 discovering the 53-kDa p53 protein, dissolving to Bert Vogelstein on 14 April 1989 proving TP53 is the master tumour suppressor and Joshua Schiffman, Carlo Maley, and Vincent Lynch on 8 October 2015 revealing 20 copies / 40 alleles of TP53 in elephants).",
             STYLE + "Split period scene: on the left, David Lane, Arnold Levine, and Bert Vogelstein examine chromosome 17p p53 tumour-suppressor gels; on the right, Joshua Schiffman, Carlo Maley, and Vincent Lynch stand beside an African elephant chart showing twenty TP53 gene copies and forty alleles." + QUAL_TAIL,
             {"kind": "FACT", "label": "Elephants carry 40 p53 alleles", "who_card": "Bert Vogelstein (born 1949) — American oncologist and cancer geneticist · Richard Peto (born 1943) — British statistician and epidemiologist", "when_stamp": "1977 · March 1979 · May 1979 · 14 April 1989 · 1992 · 8 October 2015", "timeline_step": "4/4 · May 1979, 14 Apr 1989 & 8 Oct 2015 (Lane, Crawford, Levine & Old discover p53; Vogelstein proves TP53 is the master brake; Schiffman, Maley & Lynch show elephants carry 40 TP53 alleles)", "hold_s": 3.8}),
            ("02_vogelstein_1989_science_tp53_and_schiffman_lynch_2015_jama_elephant_apoptosis_chart", 132.5, 8.0, "E", False, "14 APR 1989 VOGELSTEIN (SCIENCE: TP53 BROKEN IN >50% OF CANCERS) & 8 OCT 2015 SCHIFFMAN/LYNCH (JAMA: ELEPHANT 40 TP53 ALLELES → >2× DNA-DAMAGE APOPTOSIS)", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked Vogelstein (14 April 1989, Science 244: 217–221) chromosome 17p TP53 two-hit loss & Schiffman/Lynch (8 October 2015, JAMA 314: 1850–1860) ionizing-radiation lymphocyte apoptosis chart shows elephant cells (40 TP53 alleles) undergoing p53-mediated apoptosis at >2x the rate of healthy human cells (2 TP53 alleles) and >5x the rate of Li-Fraumeni syndrome cells (1 TP53 allele).",
             {"kind": "DATA", "label": "1989 VOGELSTEIN (TP53 IN >50% OF CANCERS) & 2015 JAMA ELEPHANT STUDY (40 TP53 ALLELES → >2× APOPTOSIS OF DAMAGED CELLS)", "detail": "Inked Vogelstein (14 April 1989, Science 244: 217–221) chromosome 17p TP53 two-hit loss & Schiffman/Lynch (8 October 2015, JAMA 314: 1850–1860) ionizing-radiation lymphocyte apoptosis chart on period paper showing elephant cells (40 TP53 alleles) undergoing p53-mediated apoptosis at >2x the rate of healthy human cells (2 TP53 alleles) and >5x the rate of Li-Fraumeni syndrome cells (1 TP53 allele)", "scale": "instead of repairing borderline DNA damage and risking a typo, an elephant cell with forty p53 guardians hits the self-destruct button the instant its DNA is scratched", "hold_s": 3.8}),
            ("03_sculpted_p53_tetramer_clamping_dna_helix_beside_elephant_40_allele_tray_closeup", 140.5, 6.5, "B", False, "8 OCTOBER 2015 — SOLVING PETO'S PARADOX", "Fast",
             "Fast: daylight macro shot of a sculpted golden four-part p53 tetramer model wrapped around a DNA double helix beside a wooden tray holding forty miniature brass p53 shields. Nothing emissive, no face.",
             STYLE + "In crisp daylight on a laboratory bench, a sculpted four-part brass p53 protein model clamps around a wooden DNA helix beside an organized tray of forty small brass guardian shields." + FAST_TAIL,
             None),
            ("04_explorer_at_elephant_40_p53_inspection_desk_pressing_apoptosis_self_destruct_button", 147.0, 5.5, "B", True, None, "Quality",
             "Quality: Explorer beat 2 (locked character reference).",
             STYLE + "Standing at a wooden DNA inspection desk surrounded by forty brass guardian dials, the Explorer spots a cracked rung on a passing DNA belt and presses a large red mechanical reset lever." + EXP_TAIL,
             None),
        ],
    ),
    (
        5,
        "Part 05 — How Precision Cancer Drugs Lock the Stuck Pedal — & How One Single Egg Cell Knows Where to Build Your Head and Hands",
        [
            ("01_timeline_1911_2015_and_imatinib_gleevec_locking_bcr_abl_pocket_chart", 152.5, 8.5, "E", False, "1911–2015 TIMELINE · ROUS RSV, KNUDSON TWO-HIT, BISHOP/VARMUS C-SRC, LANE/LEVINE/VOGELSTEIN P53, ELEPHANT 40 TP53 & 2001 GLEEVEC PRECISION KEY", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, the 4-date timeline completes: 21 Jan 1911 (Peyton Rous filters the first cancer-causing retrovirus, RSV, waiting 55 years for his 1966 Nobel Prize) · Apr 1971 & Oct 1986 (Alfred Knudson publishes the Two-Hit retinoblastoma equation proving recessive tumour-suppressor brakes; Weinberg & Dryja clone RB1) · 11 Mar 1976 (Stehelin, Varmus, Bishop & Vogt prove viral src is a stolen normal cellular proto-oncogene c-src, winning the 1989 Nobel Prize) · May 1979, Apr 1989 & Oct 2015 (Lane, Crawford, Levine & Old discover p53, Vogelstein proves TP53 is the master tumour suppressor mutated in >50% of cancers, and Schiffman & Lynch show elephants carry 20 copies / 40 alleles of TP53).",
             {"kind": "DATA", "label": "1911–2015 CANCER GENETICS TIMELINE · MAY 2001 IMATINIB (GLEEVEC) LOCKING THE STUCK BCR-ABL ONCOGENE POCKET", "detail": "Animated 4-date timeline (1911 → 2015) alongside Brian Druker's May 2001 imatinib (Gleevec) precision key locking the BCR-ABL oncogene ATP pocket", "scale": "from a Long Island chicken in 1911 to forty guardian genes inside an elephant, a century of detective work revealed that cancer is the shadow of the very genes that built us", "when_stamp": "May 2001 · 1911–2015", "timeline_step": "4/4 · 1911–2015 timeline complete", "hold_s": 3.8}),
            ("02_precision_imatinib_key_fitting_bcr_abl_kinase_pocket_model_on_plinth_pan", 161.0, 5.5, "A", False, "LOCKING THE STUCK GAS PEDAL", "Fast",
             "Fast: daylight close-up of a precision brass molecular key slotted cleanly into the active pocket of a sculpted kinase protein model on a wooden museum plinth. Nothing emissive, no face.",
             STYLE + "In crisp daylight on a wooden museum plinth, a precision-machined brass molecular key slots snugly into the pocket of a sculpted protein enzyme model, locking its hinge closed." + FAST_TAIL,
             None),
            ("03_driesch_1891_mangold_spemann_1921_organizer_lewis_1978_and_gehring_1984_hox_handoff", 166.5, 6.5, "C", False, "THE ORGANIZER & HOX BODY-PLAN GENES", "Quality",
             "Quality: readable faces (Hans Driesch in 1891 shaking sea-urchin twin embryos in Naples, Hilde Mangold and Hans Spemann in May 1921 grafting the newt Organizer with a loop of blond baby hair, and Edward B. Lewis in December 1978 with Christiane Nüsslein-Volhard, Eric Wieschaus, Matthew Scott, and Walter Gehring in 1980–1984 discovering the 180-bp Homeobox / Hox genes — handoff to 067 Embryo Organizer & Hox Genes).",
             STYLE + "Split period scene: on the left in May 1921 Freiburg, young Hilde Mangold and Hans Spemann use a tiny blond hair loop to graft a newt embryo beside Hans Driesch's 1891 sea-urchin twins; on the right, Edward Lewis, Christiane Nüsslein-Volhard, Eric Wieschaus, and Walter Gehring point to a four-winged fruit fly and a colour-coded Hox chromosome map." + QUAL_TAIL,
             {"kind": "WHEN", "label": "1891 · MAY 1921 · DECEMBER 1978 · OCTOBER 1980 · 1984", "hold_s": 3.5}),
            ("04_table_three_callback", 173.0, 2.4, "C", False, None, "reuse",
             "Reuse: verified unused moving window [5.50s..7.90s] of P1:07_table_three_props_1911_berkefeld_filter_1971_two_hit_chart_and_p53_tetramer_model (callback, £0).",
             "Reuse P1:07_table_three_props_1911_berkefeld_filter_1971_two_hit_chart_and_p53_tetramer_model [5.50s..7.90s] (2.40s distinct non-overlapping tail window from 8.00s source clip).",
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
                row["reuse_of"] = "P1:07_table_three_props_1911_berkefeld_filter_1971_two_hit_chart_and_p53_tetramer_model"
                row["reuse_window_s"] = [5.5, 7.9]
                row["reuse_audit"] = {
                    "source_row": "P1:07_table_three_props_1911_berkefeld_filter_1971_two_hit_chart_and_p53_tetramer_model",
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
            "film": "066_Rous-Knudson-Bishop-Varmus-Lane-Cancer-Oncogenes-p53",
            "part": p_idx,
            "title": p_title,
            "version": "v01",
            "timing_status": "pre_vo_script_clock (built from cancer_script_master_v01.md; retimes onto Scribe STT once VO locks)",
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
        "film": "066_Rous-Knudson-Bishop-Varmus-Lane-Cancer-Oncogenes-p53",
        "version": "v01",
        "date": "2026-10-19",
        "owner": "gemini (J0661)",
        "status": "PRE_VO_BOARDS_V01_NO_MINT",
        "generation_authorized": False,
        "script": "00_Brand/Channel-Setup/ideas/066_Rous-Knudson-Bishop-Varmus-Lane-Cancer-Oncogenes-p53/cancer_script_master_v01.md",
        "sources": "00_Brand/Channel-Setup/ideas/066_Rous-Knudson-Bishop-Varmus-Lane-Cancer-Oncogenes-p53/SOURCES_v01.md",
        "credit_snapshot": {
            "flow_balance": 23740,
            "flow_floor": 0,
            "flow_read_at": "2026-10-15T21:42:22Z",
            "vertex_promo_gbp": 71.02,
            "vertex_usable_gbp": 70.02,
        },
        "totals": totals,
        "per_part": per_part_summary,
        "mint_order": "006 > 007 > 008 > 009 > 010 > 011 > 012 > 013 > 014 > 015 > 016 > 017 > 018 > 019 > 020 > 021 > 022 > 023 > 024 > 025 > 026 > 027 > 028 > 029 > 030 > 031 > 032 > 033 > 034 > 035 > 036 > 037 > 038 > 039 > 040 > 041 > 042 > 043 > 044 > 045 > 046 > 047 > 048 > 049 > 050 > 051 > 052 > 053 > 054 > 055 > 056 > 057 > 058 > 059 > 060 > 061 > 062 > 063 > 064 > 065 > 066 > 067 > 068. Nothing in 066 is generation_authorized.",
    }
    (EDIT / "PICTURE_PLAN_v01.json").write_text(json.dumps(plan, indent=2) + "\n")

    sl = [
        "# 066 Cancer Genes: The Stuck Gas Pedal Inside Your Own DNA — Shot list & plate boards v01 (pre-VO)",
        "",
        "Gemini, 19 Oct 2026, J0661. Built from `cancer_script_master_v01.md` (`90.8 PASS`) and `SOURCES_v01.md`.",
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
        "# 066 price review v01 (pre-VO plate boards)",
        "",
        "Gemini, 19 Oct 2026, J0661. Boards only. **No mint. No spend. No merge.**",
        "Prepared from `cancer_script_master_v01.md` (`90.8 PASS`) and `SOURCES_v01.md` so 066's full plate board rows, non-emissive Fast prompts, £0 code graphics, and Teach-on-Screen overlays are ready to re-time the moment long VO locks. Parked for Chief.",
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
        f"- **Quality ({totals['Quality']} rows):** readable faces (Peyton Rous, Alfred G. Knudson Jr., J. Michael Bishop, Harold E. Varmus, Dominique Stehelin, Peter K. Vogt, Robert A. Weinberg, Thaddeus P. Dryja, David P. Lane, Arnold J. Levine, Lloyd J. Old, Bert Vogelstein, Richard Peto, Hans Driesch, Hilde Mangold, Hans Spemann, Edward B. Lewis, Walter J. Gehring), 21 January 1911 New York Rous Sarcoma Virus filtration, 11 March 1976 UCSF `c-src` proto-oncogene discovery, April 1971 Houston `Two-Hit` retinoblastoma graph & 16 October 1986 `RB1` cloning, May 1979–2015 `p53` & elephant `40 TP53 alleles` discovery, and the 2 Explorer beats.",
        f"- **Fast ({totals['Fast']} rows, non-emissive):** daylight prop and laboratory shots (1911 Berkefeld porcelain filter candle, two-hit graph & brass pedal-and-brake model pan, 3-object callback bench, 1976 `c-src` hybridization plot & 1982 sequencing gel strip, normal vs wedged brass accelerator pedals, 1986 chromosome 13 `RB1` Southern blot & twin braided brake cables, paired wooden chromosome 13 models with brass `RB1` clasps, sculpted 4-part `p53` DNA clamp beside 40 miniature shields, precision `imatinib` brass key slotted into `BCR-ABL` kinase model on museum plinth). Zero candles, flames, sparks, or glowing elements on Fast.",
        f"- **£0 code graphics ({totals['code_graphic']} rows):**",
        "  1. `P1:04_rous_1911_knudson_1971_bishop_varmus_1976_lane_vogelstein_p53_accelerator_vs_brakes_chart` — dominant proto-oncogene accelerator (`1 hit`: `c-src` / `HRAS` codon 12 `G→T`) vs recessive Two-Hit tumour-suppressor brakes (`2 hits`: `RB1` & `TP53` mutated in `>50%` of cancers) (`SCALE: turning a healthy cell into a tumour is like a runaway car — it takes a stuck gas pedal in a single growth gene plus cutting both independent emergency brake cables`)",
        "  2. `P1:06_peto_1977_abegglen_schiffman_maley_lynch_2015_elephant_40_tp53_alleles_chart` — Peto's Paradox (1977) & Abegglen/Schiffman/Maley/Lynch (8 October 2015 *JAMA*): humans (`2 TP53 alleles`, `~11–25%` cancer mortality) vs elephants (`100×` more cells, `20 copies / 40 alleles of TP53`, `<4.8%` cancer mortality) (`SCALE: an elephant has a hundred times more cells than you do, yet because every elephant cell carries forty copies of the p53 brake gene instead of two, elephants almost never get cancer`)",
        "  3. `P2:02_stehelin_varmus_bishop_vogt_11_mar_1976_nature_c_src_hybridization_and_hras_chart` — Stehelin, Varmus, Bishop & Vogt (11 March 1976, *Nature* 260: 170–173) `c-src` vertebrate DNA hybridization curve + Weinberg/Barbacid (1982) human `HRAS` single-letter mutation (`SCALE: Peyton Rous's virus didn't bring an alien poison into the cell — like a car thief who hot-wires your own ignition, it stole a normal growth gene that every healthy cell uses to heal wounds and welded the gas pedal to the floor`)",
        "  4. `P3:02_knudson_apr_1971_pnas_48_case_retinoblastoma_one_hit_vs_two_hit_survival_curve_chart` — Knudson (April 1971, *PNAS* 68: 820–823) `48-case` retinoblastoma semi-log curve comparing hereditary bilateral (`1-hit` linear exponential) vs sporadic unilateral (`2-hit` curve) (`SCALE: having two copies of every tumour-suppressor gene is like flying on an airliner with twin backup hydraulic brakes — if random chance cuts one cable in a million cells, the backup cable still stops the plane, unless lightning strikes the exact same cell twice`)",
        "  5. `P4:02_vogelstein_1989_science_tp53_and_schiffman_lynch_2015_jama_elephant_apoptosis_chart` — Vogelstein (14 April 1989 *Science*) `TP53` two-hit inactivation & Schiffman/Lynch (8 October 2015 *JAMA*) elephant lymphocyte radiation apoptosis (`>2×` human rate) (`SCALE: instead of repairing borderline DNA damage and risking a typo, an elephant cell with forty p53 guardians hits the self-destruct button the instant its DNA is scratched`)",
        "  6. `P5:01_timeline_1911_2015_and_imatinib_gleevec_locking_bcr_abl_pocket_chart` — completed 4-date timeline (1911 → 2015) + Brian Druker's May 2001 `imatinib` (`Gleevec`) precision molecular key locking `BCR-ABL` (`SCALE: from a Long Island chicken in 1911 to forty guardian genes inside an elephant, a century of detective work revealed that cancer is the shadow of the very genes that built us`)",
        f"- **£0 verified reuse ({totals['reuse']} row):** `P5:04_table_three_callback` uses the 2.40 s unused moving tail `[5.50s..7.90s]` of `P1:07_table_three_props_1911_berkefeld_filter_1971_two_hit_chart_and_p53_tetramer_model`.",
        "",
        "## Mint order",
        "",
        "006 > 007 > 008 > 009 > 010 > 011 > 012 > 013 > 014 > 015 > 016 > 017 > 018 > 019 > 020 > 021 > 022 > 023 > 024 > 025 > 026 > 027 > 028 > 029 > 030 > 031 > 032 > 033 > 034 > 035 > 036 > 037 > 038 > 039 > 040 > 041 > 042 > 043 > 044 > 045 > 046 > 047 > 048 > 049 > 050 > 051 > 052 > 053 > 054 > 055 > 056 > 057 > 058 > 059 > 060 > 061 > 062 > 063 > 064 > 065 > 066 > 067 > 068. `generation_authorized` is `false` on every row.",
    ])
    (EDIT / "PRICE_REVIEW_v01.md").write_text("\n".join(pr_lines) + "\n")
    print(f"066 v01 boards written: {totals['rows']} rows, Flow expected={totals['flow_credits_expected']}")


if __name__ == "__main__":
    main()
