#!/usr/bin/env python3
"""HOS 080 (The Genetic Code: Cracked by an Outsider at 3 AM) pre-VO plate boards v01. J0738. No mint, no spend.

Built from 00_Brand/Channel-Setup/ideas/080_Beadle-Tatum-Palade-Brenner-Jacob-Nirenberg-Genetic-Code-mRNA/genetic_code_script_master_v01.md
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
        "Part 01 — The 4-Letter Vault, the RNA Tie Club & the 3:00 a.m. Eureka in Bethesda",
        [
            ("01_dna_to_mrna_ribosome_translation_and_nirenberg_matthaei_3am_poly_u_tube_14", 0.0, 5.5, "A", False, "CRACKING THE 64-WORD GENETIC CODE", "Quality",
             "Quality: Short frame 0 / answer image (0:03) + side by side, inside a living cell a gene on the DNA double helix is transcribed into a single-stranded messenger RNA (mRNA) ribbon that feeds through a two-part ribosome 3 letters (1 codon) at a time to link amino acids into a protein chain, while at the NIH in Bethesda at 3:00 a.m. on 27 May 1961 Heinrich Matthaei and Marshall Nirenberg watch test tube #14 (radioactive phenylalanine + poly-U RNA) spike to 39,800 counts per minute.",
             STYLE + "Split molecular-and-laboratory scene: on the left, a DNA double helix unzips to copy a single-stranded messenger RNA ribbon that threads through a two-subunit ribosome linking amino acid spheres; on the right, Marshall Nirenberg and Heinrich Matthaei in their 1961 Bethesda lab watch a radiation counter needle jump beside a rack of twenty test tubes." + QUAL_TAIL,
             {"kind": "WHEN", "label": "BETHESDA, 27 MAY 1961", "timeline_step": "1/3 · 15 Nov 1941 & Jan 1955 (George Beadle and Edward Tatum irradiate Neurospora bread mould at Stanford to prove One Gene–One Enzyme, and George Palade discovers ribosomes at the Rockefeller Institute)", "hold_s": 3.5}),
            ("02_beadle_tatum_1941_palade_1955_brenner_jacob_meselson_1960_and_nirenberg_matthaei_1961_split", 5.5, 6.0, "B", False, "BREAD MOULD, MESSENGER RNA, POLY-U AT 3 AM", "Quality",
             "Quality: complex three-part composition (George Beadle and Edward Tatum at Stanford in 1941 irradiating Neurospora bread mould tubes alongside George Palade at the Rockefeller Institute in 1955 discovering ribosomes; Sydney Brenner, François Jacob, and Matthew Meselson in King's College, Cambridge on Good Friday, 15 April 1960 and at Caltech discovering messenger RNA; and Marshall Nirenberg and Heinrich Matthaei at the NIH in Bethesda on 27 May 1961 decoding UUU = Phenylalanine).",
             STYLE + "Three-panel period composition: on the left, George Beadle and Edward Tatum in 1941 Stanford holding pink bread-mould culture tubes beside George Palade at his 1955 electron microscope; in the centre, Sydney Brenner, François Jacob, and Matthew Meselson in 1960 Cambridge and Caltech; on the right, Marshall Nirenberg and Heinrich Matthaei in 1961 Bethesda with their chilled mortar and test-tube rack." + QUAL_TAIL,
             None),
            ("03_ribosome_reading_mrna_at_15_to_20_codons_per_second_with_trna_adaptors_snapping_amino_acids", 11.5, 6.0, "C", False, "64 THREE-LETTER WORDS OF LIFE", "Quality",
             "Quality: complex molecular reveal (a ribosome racing along an mRNA strip at 15–20 codons per second as transfer RNA adaptors snap amino acids into a folding protein chain, beside a single-letter point mutation swapping one amino acid).",
             STYLE + "Inside a three-dimensional cellular interior, a two-part ribosome glides along a messenger RNA ribbon as cloverleaf transfer RNA adaptors click three-base triplets into place and fold a growing protein chain." + QUAL_TAIL,
             {"kind": "WHEN", "label": "1941 · 1955 · 15 APRIL 1960 · 13 MAY 1961 · 27 MAY 1961", "timeline_step": "1/3 · 1941 & 1955 (Beadle, Tatum & Palade) · 2/3 · 1960–1961 (Brenner, Jacob, Meselson & Crick) · 3/3 · 27 May 1961 – 1966 (Nirenberg, Matthaei & Khorana)", "hold_s": 3.5}),
            ("04_beadle_tatum_1941_palade_1955_brenner_jacob_1961_and_nirenberg_matthaei_1961_central_dogma_codon_chart", 17.5, 8.0, "E", False, "DNA (A,T,C,G) → MRNA (A,U,C,G) → 64 TRIPLET CODONS (4³ = 64) → TRNA & RIBOSOME → 20 AMINO ACIDS (UUU = PHE, 39,800 CPM)", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked Transcription, Messenger RNA, Ribosome Translation & 64-Codon Genetic Code chart from Beadle & Tatum (15 November 1941 PNAS 27: 499–506), George Palade (January 1955 J. Biophys. Biochem. Cytol. 1: 59–68), Brenner, Jacob & Meselson (13 May 1961 Nature 190: 576–581), Crick, Barnett, Brenner & Watts-Tobin (30 December 1961 Nature 192: 1227–1232), and Nirenberg & Matthaei (October 1961 PNAS 47: 1588–1602) maps DNA (A, T, C, G) → mRNA (A, U, C, G) → 64 triplet codons (4³ = 64) → tRNA adaptors → 20 amino acids on the ribosome, led by UUU = Phenylalanine (39,800 cpm vs 70 cpm background).",
             {"kind": "DATA", "label": "CENTRAL DOGMA (DNA → MRNA → RIBOSOME → PROTEIN), 4³ = 64 TRIPLET CODONS & NIRENBERG-MATTHAEI POLY-U (39,800 VS 70 CPM)", "detail": "Inked Central Dogma (DNA → mRNA → ribosome → protein) & 64-triplet genetic code table on period paper showing 4 bases read in 1-letter (4), 2-letter (16), vs 3-letter (4³ = 64) words for 20 amino acids, and Nirenberg & Matthaei's 27 May 1961 poly-U experiment (39,800 cpm 14C-phenylalanine incorporation vs 70 cpm control)", "scale": "if you read the four letters of DNA one at a time, you only get four words; in pairs, you only get sixteen — so life reads DNA in three-letter triplets, giving sixty-four possible words to spell twenty amino acids and punctuation stops", "who_card": "George Wells Beadle (1903–1989) — American geneticist · Edward Lawrie Tatum (1909–1975) — American biochemist and geneticist · George Emil Palade (1912–2008) — Romanian-American cell biologist · Sydney Brenner (1927–2019) — South African molecular biologist · François Jacob (1920–2013) — French geneticist and biologist · Matthew Meselson (born 1930) — American molecular biologist · Marshall Warren Nirenberg (1927–2010) — American biochemist · J. Heinrich Matthaei (born 1929) — German biochemist", "when_stamp": "1941 · 1955 · 15 April 1960 · 13 May 1961 · 27 May 1961", "hold_s": 3.8}),
            ("05_neurospora_culture_tubes_rna_tie_club_woollen_tie_and_1961_pnas_offprint_pan", 25.5, 5.5, "A", False, "15 TO 20 CODONS PER SECOND", "Fast",
             "Fast: daylight macro pan across Stanford Neurospora bread-mould glass slants, an RNA Tie Club woollen necktie with its stitched helix, and the October 1961 PNAS offprint on an oak bench between code graphics so two full-frame graphics never run back to back. Nothing emissive, no face.",
             STYLE + "In crisp daylight on an oak biochemistry bench, the camera pans smoothly across glass culture tubes of pink bread mould, a dark woollen necktie embroidered with a helix, and an open 1961 scientific journal." + FAST_TAIL,
             None),
            ("06_nirenberg_matthaei_27_may_1961_poly_u_phenylalanine_39800_cpm_chart", 31.0, 8.0, "E", False, "BETHESDA, 27 MAY 1961", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period parchment, an inked Marshall Nirenberg & Heinrich Matthaei (27 May 1961 Lab Notebook & October 1961 PNAS 47: 1588–1602) Cell-Free E. coli Ribosome & Poly-U Assay diagram shows 20 test tubes containing DNase-treated E. coli ribosome extract ('Matthaei's soup') and synthetic polyuridylic acid (UUUUUU...), where the tube with 14C-phenylalanine leaps from 70 counts per minute to 39,800 counts per minute.",
             {"kind": "DATA", "label": "27 MAY 1961 & OCT 1961 NIRENBERG & MATTHAEI (PNAS TABLE 1): POLY-U + 14C-PHENYLALANINE = 39,800 CPM VS 70 CPM CONTROL", "detail": "Inked Nirenberg & Matthaei (October 1961 PNAS 47: 1588–1602, Table 1) cell-free poly-U radioactive amino acid incorporation chart (39,800 cpm 14C-L-phenylalanine vs 70 cpm control and 0–100 cpm for the other 19 amino acids) on period paper", "scale": "feeding a ribbon of pure U-U-U-U-U into crushed bacteria and getting back a chain of pure phenylalanine was the Rosetta Stone of biology — like typing a single repeated letter into an alien cipher machine and watching it print out its first English word", "hold_s": 3.8}),
            ("07_table_three_props_1941_neurospora_tube_1960_centrifuge_rotor_and_1961_mortar_pestle_filter_disc", 39.0, 5.5, "C", False, "1941 TO 1968", "Fast",
             "Fast: daylight prop table (callback source for Part 05: Beadle and Tatum's 1941 stoppered Neurospora bread-mould tube #299, Brenner and Meselson's 1960 analytical ultracentrifuge rotor cell, and Nirenberg and Matthaei's 1961 porcelain mortar and pestle beside a brass planchet filter disc). Nothing emissive.",
             STYLE + "On an oak workbench in soft window light sit three objects side by side: a cotton-plugged glass tube of orange bread mould, a machined metal ultracentrifuge cell, and a porcelain mortar and pestle beside a small brass filter planchet." + FAST_TAIL,
             None),
            ("08_explorer_feeding_mrna_ribbon_through_brass_ribosome_printer_snapping_phenylalanine_beads", 62.0, 5.5, "A", True, None, "Quality",
             "Quality: Explorer beat 1 (locked character reference, after 1:00).",
             STYLE + "Standing between a glass nuclear vault containing a master DNA helix and a brass ribosome machine on a workbench, the Explorer feeds a golden messenger RNA ribbon through the ribosome slot as a mechanical arm clicks spherical amino acid beads onto a growing protein chain." + EXP_TAIL,
             None),
            ("09_marshall_nirenberg_aug_1961_moscow_congress_and_francis_crick_grand_hall", 67.5, 5.5, "B", False, "THE MOSCOW SURPRISE", "Quality",
             "Quality: readable faces (at the International Congress of Biochemistry in Moscow in August 1961, 34-year-old Marshall Nirenberg presents his poly-U result to a small seminar room before Francis Crick and Matthew Meselson bring him to the grand hall of 1,000 scientists).",
             STYLE + "In a 1961 Moscow congress lecture hall, young biochemist Marshall Nirenberg stands at a wooden lectern holding his test-tube data sheet as Francis Crick gestures him toward a packed grand auditorium." + QUAL_TAIL,
             {"kind": "WHEN", "label": "MOSCOW, AUGUST 1961", "timeline_step": "3/3 · 27 May 1961 & Aug 1961 (Marshall Nirenberg and Heinrich Matthaei crack UUU = Phenylalanine at 3:00 a.m. in Bethesda and stun the Moscow Biochemistry Congress)", "hold_s": 3.5}),
        ],
    ),
    (
        2,
        "Part 02 — 1941 & 1955: Irradiated Bread Mould (One Gene–One Enzyme) & George Palade's Ribosome Factories",
        [
            ("01_beadle_and_tatum_1941_stanford_neurospora_xray_tube_299_and_george_palade_1955_ribosomes", 73.0, 6.5, "A", False, "299TH TUBE PROVED GENE LAW", "Quality",
             "Quality: readable faces (American geneticist George Wells Beadle and biochemist Edward Lawrie Tatum at Stanford University in 1941 examining irradiated Neurospora crassa bread-mould tube #299 requiring Vitamin B6, dissolving to Romanian-American cell biologist George Emil Palade at the Rockefeller Institute in January 1955 discovering ribosomes under the electron microscope).",
             STYLE + "Split period scene: on the left in 1941 Stanford, George Beadle and Edward Tatum hold up glass culture tube 299 of pink Neurospora bread mould in front of rack rows; on the right in 1955 New York, George Palade examines an electron micrograph of ribosome granules." + QUAL_TAIL,
             {"kind": "FACT", "label": "299th tube proved gene law", "who_card": "Archibald Garrod (1857–1936) — British physician", "when_stamp": "1902 · 15 November 1941 · January 1955 · 1958", "timeline_step": "1/3 · 15 Nov 1941 & Jan 1955 (Beadle & Tatum prove One Gene–One Enzyme in Neurospora; George Palade discovers ribosomes)", "hold_s": 3.8}),
            ("02_beadle_tatum_1941_neurospora_tube_299_and_palade_1955_ribosome_em_chart", 79.5, 8.0, "E", False, "15 NOV 1941 BEADLE & TATUM (PNAS: NEUROSPORA TUBE #299 ONE GENE–ONE ENZYME) & JAN 1955 PALADE (RIBOSOME PROTEIN FACTORIES)", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked George Beadle & Edward Tatum (15 November 1941 PNAS 27: 499–506) Neurospora crassa X-ray mutant minimal vs supplemented growth chart (Tube #299 pyridoxine mutant & arginine pathway Enzymes A → B → C) alongside George Palade's (January 1955 J. Biophys. Biochem. Cytol. 1: 59–68) electron-microscope ribosome distribution on the endoplasmic reticulum.",
             {"kind": "DATA", "label": "1941 BEADLE & TATUM (PNAS TUBE #299 ONE GENE–ONE ENZYME) & 1955 GEORGE PALADE (20–30 NM RIBOSOME GRANULES, ~10M/CELL)", "detail": "Inked George Beadle & Edward Tatum (15 November 1941 PNAS 27: 499–506) Neurospora crassa X-ray mutant minimal vs supplemented growth chart (Tube #299 pyridoxine mutant & arginine pathway Enzymes A → B → C) alongside George Palade's (January 1955 J. Biophys. Biochem. Cytol. 1: 59–68) electron-microscope ribosome distribution on the endoplasmic reticulum on period paper", "scale": "a single human cell packs up to ten million ribosomes into a space smaller than a speck of dust — ten million microscopic 3D printers humming side by side to build every protein in your body", "hold_s": 3.8}),
            ("03_stanford_1941_neurospora_minimal_vs_vitamin_b6_tubes_and_1955_palade_micrograph_closeup", 87.5, 6.5, "B", False, "1941 & 1955 — ONE GENE–ONE ENZYME & RIBOSOMES", "Fast",
             "Fast: daylight macro shot of wooden test-tube racks holding minimal-medium vs pyridoxine-supplemented Neurospora crassa slants beside George Palade's 1955 electron micrograph plate of endoplasmic reticulum ribosomes on a bench. Nothing emissive, no face.",
             STYLE + "In crisp daylight on a 1955 genetics bench, a wooden rack of cotton-plugged glass culture tubes with orange bread mould sits beside a silver-gelatin electron micrograph plate of ribosome granules." + FAST_TAIL,
             None),
            ("04_cutaway_cell_model_showing_nuclear_dna_vault_and_endoplasmic_reticulum_ribosomes_pan", 94.0, 5.5, "C", False, "DNA IN THE NUCLEUS, RIBOSOMES IN THE CYTOPLASM", "Fast",
             "Fast: daylight close-up pan across a sculpted cutaway model of a eukaryotic cell showing the double-walled nucleus containing the DNA helix separated from the rough endoplasmic reticulum studded with ribosome beads on an oak table. Nothing emissive, no face.",
             STYLE + "In bright window light on an oak table, a sculpted cutaway cell model shows the central nucleus with its coiled DNA helix surrounded by folded endoplasmic reticulum membranes dotted with tiny ribosome spheres." + FAST_TAIL,
             None),
        ],
    ),
    (
        3,
        "Part 03 — Good Friday, 15 April 1960: The Missing Messenger (mRNA) & the 3-Letter Codon Proof — Midpoint Twist",
        [
            ("01_sydney_brenner_francois_jacob_and_francis_crick_good_friday_15_apr_1960_cambridge_and_meselson_caltech", 99.5, 6.5, "A", False, "MRNA IS A DISPOSABLE TAPE", "Quality",
             "Quality: readable faces (South African biologist Sydney Brenner, French geneticist François Jacob, and British biophysicist Francis Crick in Brenner's rooms at King's College, Cambridge on Good Friday, 15 April 1960 realizing that unstable RNA is the messenger, dissolving to Brenner, Jacob, and Matthew Meselson at Caltech in summer 1960 proving mRNA binds pre-existing ribosomes).",
             STYLE + "Split period scene: on the left in 1960 King's College Cambridge, Sydney Brenner, François Jacob, and Francis Crick leap up around a blackboard diagram of DNA, mRNA, and ribosomes; on the right at Caltech, Matthew Meselson loads heavy-isotope tubes into an analytical ultracentrifuge." + QUAL_TAIL,
             {"kind": "FACT", "label": "mRNA is a disposable tape", "who_card": "Francis Crick (1916–2004) — British molecular biologist and biophysicist · Jacques Monod (1910–1976) — French biochemist and geneticist", "when_stamp": "1957 · 15 April 1960 · 13 May 1961 · 30 December 1961", "timeline_step": "2/3 · 15 Apr 1960 – Dec 1961 (Brenner, Jacob & Meselson discover messenger RNA; Crick & Brenner prove the 3-letter triplet codon reading frame)", "hold_s": 3.8}),
            ("02_brenner_jacob_meselson_may_1961_mrna_gradient_and_crick_brenner_dec_1961_triplet_frameshift_chart", 106.0, 8.0, "E", False, "13 MAY 1961 BRENNER, JACOB & MESELSON (NATURE: 15N/13C MRNA ON PRE-EXISTING RIBOSOMES) & 30 DEC 1961 CRICK & BRENNER (+3 TRIPLET CODON PROOF)", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked Sydney Brenner, François Jacob & Matthew Meselson (13 May 1961 Nature 190: 576–581) heavy-isotope (15N/13C) ribosome density-gradient chart proving new phage mRNA binds pre-existing ribosomes alongside Crick, Barnett, Brenner & Watts-Tobin's (30 December 1961 Nature 192: 1227–1232) +1/+2 frameshift vs +3 triplet reading-frame restoration chart.",
             {"kind": "DATA", "label": "1961 BRENNER, JACOB & MESELSON (NATURE MRNA DENSITY GRADIENT) & CRICK-BRENNER (+1/+2 FRAMESHIFT VS +3 TRIPLET READING FRAME)", "detail": "Inked Sydney Brenner, François Jacob & Matthew Meselson (13 May 1961 Nature 190: 576–581) heavy-isotope (15N/13C) ribosome density-gradient chart proving new phage mRNA binds pre-existing ribosomes alongside Crick, Barnett, Brenner & Watts-Tobin's (30 December 1961 Nature 192: 1227–1232) +1/+2 frameshift vs +3 triplet reading-frame restoration chart on period paper", "scale": "Sydney Brenner and François Jacob proved that DNA never leaves the nucleus for the same reason an architect never leaves the only master blueprint of a skyscraper out in the mud — instead, the cell prints disposable mRNA photocopies and sends them out to the ribosome construction crew", "hold_s": 3.8}),
            ("03_caltech_1960_cesium_chloride_density_gradient_tubes_and_may_1961_nature_issue_closeup", 114.0, 6.5, "B", False, "15 APRIL 1960 & 13 MAY 1961 — MESSENGER RNA DISCOVERED", "Fast",
             "Fast: daylight macro shot of Caltech cesium-chloride density-gradient centrifuge tubes in a brass rack beside the 13 May 1961 and 30 December 1961 issues of Nature and bacteriophage plaque plates on a bench. Nothing emissive, no face.",
             STYLE + "In crisp daylight on a 1961 molecular biology bench, clear density-gradient centrifuge tubes in a brass stand sit beside agar Petri dishes of phage plaques and an open 1961 journal." + FAST_TAIL,
             None),
            ("04_triplet_reading_frame_wooden_letter_blocks_model_showing_plus_one_vs_plus_three_restoration_pan", 120.5, 5.5, "C", False, "THE THREE-LETTER TRIPLET READING FRAME", "Fast",
             "Fast: daylight close-up pan across a mechanical wooden reading-frame demonstrator with three-letter sliding windows showing how a single-base insertion scrambles downstream triplets while three insertions restore the frame on an oak table. Nothing emissive, no face.",
             STYLE + "In bright window light on an oak table, a brass-and-wood three-letter sliding reading-frame model shows nucleic acid base blocks grouped into neat triplets." + FAST_TAIL,
             None),
        ],
    ),
    (
        4,
        "Part 04 — 27 May 1961, 3:00 a.m.: Marshall Nirenberg, Heinrich Matthaei & the Poly-U (UUU = Phenylalanine) Breakthrough",
        [
            ("01_marshall_nirenberg_and_heinrich_matthaei_27_may_1961_3am_nih_bethesda_poly_u_eureka", 126.0, 6.5, "A", False, "UUU SPELLED FIRST LIFE WORD", "Quality",
             "Quality: readable faces (American biochemist Marshall Warren Nirenberg and German postdoctoral fellow J. Heinrich Matthaei at the NIH in Bethesda at 3:00 a.m. on 27 May 1961 testing 20 tubes of cell-free E. coli ribosome extract with poly-U RNA and discovering 39,800 cpm of 14C-phenylalanine incorporation, alongside Har Gobind Khorana completing the 64-codon dictionary).",
             STYLE + "Split period scene: on the left at 3:00 a.m. on 27 May 1961 in Bethesda, Heinrich Matthaei and Marshall Nirenberg examine the radiation counter readout beside twenty test tubes of cell-free ribosome extract; on the right, Har Gobind Khorana holds flasks of synthetic repeating RNA trinucleotides." + QUAL_TAIL,
             {"kind": "FACT", "label": "UUU spelled first life word", "who_card": "Har Gobind Khorana (1922–2011) — Indian-American biochemist", "when_stamp": "27 May 1961 · August 1961 · October 1961 · 1966 · 1968", "timeline_step": "3/3 · 27 May 1961 – 1968 (Nirenberg & Matthaei decode UUU = Phenylalanine at 3:00 a.m., and with Khorana & Holley complete the 64-codon genetic code)", "hold_s": 3.8}),
            ("02_nirenberg_matthaei_leder_and_khorana_1961_1966_complete_64_codon_genetic_code_dictionary_chart", 132.5, 8.0, "E", False, "1961–1966 NIRENBERG, MATTHAEI, LEDER & KHORANA: COMPLETE 64-CODON GENETIC CODE DICTIONARY (UUU = PHE, AUG = MET START, UAA/UAG/UGA STOP)", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked Marshall Nirenberg, Heinrich Matthaei, Philip Leder & Har Gobind Khorana (1961–1966; PNAS October 1961 47: 1588–1602) complete 64-codon genetic code dictionary wheel and table (61 amino-acid codons including AUG start + UAA, UAG, UGA stop codons).",
             {"kind": "DATA", "label": "1961–1966 NIRENBERG, MATTHAEI, LEDER & KHORANA: COMPLETE 64-CODON GENETIC CODE TABLE (61 AMINO-ACID CODONS + 3 STOP CODONS)", "detail": "Inked Marshall Nirenberg, Heinrich Matthaei, Philip Leder & Har Gobind Khorana (1961–1966; PNAS October 1961 47: 1588–1602) complete 64-codon genetic code dictionary wheel/table (61 amino-acid codons including AUG start + UAA, UAG, UGA stop codons) on period paper", "scale": "every living thing on Earth — from a blade of grass and a bacterium in your gut to the neurons firing in your brain right now — reads the exact same sixty-four-word dictionary that Marshall Nirenberg and Heinrich Matthaei cracked at three in the morning, proving that all life on Earth shares a single family tree", "hold_s": 3.8}),
            ("03_bethesda_1961_chilled_alumina_mortar_20_test_tube_rack_filter_planchets_and_notebook_closeup", 140.5, 6.5, "B", False, "27 MAY 1961, 3:00 A.M. — UUU = PHENYLALANINE", "Fast",
             "Fast: daylight macro shot of Matthaei and Nirenberg's chilled porcelain mortar and pestle with alumina powder, a rack of 20 glass test tubes, brass radiation-counter filter planchets, and the May 1961 lab notebook on a bench. Nothing emissive, no face.",
             STYLE + "In crisp daylight on a 1961 NIH Bethesda bench, a porcelain mortar and pestle sit beside a twenty-tube metal rack, circular brass filter planchets, and an open ruled laboratory notebook." + FAST_TAIL,
             None),
            ("04_explorer_turning_64_codon_cipher_wheel_to_match_uuu_to_phenylalanine_and_aug_to_start", 147.0, 5.5, "B", True, None, "Quality",
             "Quality: Explorer beat 2 (locked character reference).",
             STYLE + "Standing beside a large brass three-ring cipher wheel engraved with four base positions, the Explorer rotates the inner, middle, and outer rings to align three uracil markers and unlocks a compartment holding a phenylalanine sphere." + EXP_TAIL,
             None),
        ],
    ),
    (
        5,
        "Part 05 — The Universal Dictionary of Life — & How Plants See Light & Feel Gravity Without Eyes or Brains",
        [
            ("01_timeline_1941_1968_and_universal_64_codon_genetic_code_chart", 152.5, 8.5, "E", False, "1941–1968 TIMELINE · BEADLE-TATUM ONE GENE–ONE ENZYME, PALADE RIBOSOMES, BRENNER-JACOB-MESELSON MRNA & NIRENBERG-KHORANA 64-CODON CODE", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, the 3-era timeline completes: 15 Nov 1941 & Jan 1955 (George Beadle and Edward Tatum irradiate Neurospora bread mould at Stanford to prove One Gene–One Enzyme, and George Palade discovers ribosomes at the Rockefeller Institute) · 15 Apr 1960 – Dec 1961 (Sydney Brenner, François Jacob, and Matthew Meselson discover messenger RNA in Cambridge and Caltech, and Francis Crick and Brenner prove the 3-letter triplet codon reading frame) · 27 May 1961 – 1968 (Marshall Nirenberg and Heinrich Matthaei decode UUU = Phenylalanine at 3:00 a.m. in Bethesda, and with Har Gobind Khorana and Robert Holley complete the 64-codon genetic code, winning the 1968 Nobel Prize).",
             {"kind": "DATA", "label": "1941–1968 GENETIC CODE, MRNA & RIBOSOME TIMELINE · BEADLE, TATUM, PALADE, BRENNER, JACOB, MESELSON, CRICK, NIRENBERG & KHORANA", "detail": "Animated timeline (1941 → 1968) alongside an inked summary of One Gene–One Enzyme, ribosomes, messenger RNA transcription, and 64-codon translation", "scale": "from X-rayed bread mould at Stanford and a Good Friday conversation in Cambridge to a radiation counter ticking at 3 a.m. in Bethesda, scientists cracked the four-letter operating system of life on Earth", "when_stamp": "1941–1968", "timeline_step": "3/3 · 1941–1968 timeline complete", "hold_s": 3.8}),
            ("02_ribosome_mrna_model_beside_potted_seedling_bending_toward_window_light_on_plinth_pan", 161.0, 5.5, "A", False, "ONE UNIVERSAL 64-WORD LANGUAGE OF LIFE", "Fast",
             "Fast: daylight close-up of a sculpted DNA-mRNA-ribosome translation model beside a terracotta flowerpot whose green grass shoots curve smoothly toward a sunlit window on a wooden museum plinth. Nothing emissive, no face.",
             STYLE + "In crisp daylight on a wooden museum plinth, a sculpted ribosome and messenger RNA model sits beside a terracotta pot of green canary-grass seedlings bending toward a sunny window." + FAST_TAIL,
             None),
            ("03_charles_and_francis_darwin_1880_tin_foil_coleoptile_caps_went_1926_agar_auxin_and_ethylene_handoff", 166.5, 6.5, "C", False, "PLANT TROPISMS, AUXIN & ETHYLENE GAS", "Quality",
             "Quality: readable faces (Charles Darwin and his son Francis Darwin at Down House in November 1880 placing tiny tin-foil caps over canary-grass seedling tips, Frits Warmolt Went in Utrecht on 17 April 1926 collecting auxin in agar jelly blocks, and Dmitry Neljubow in 1901 with Richard Gane in 1934 discovering ethylene ripening gas — handoff to 081 Plant Tropisms, Auxin & Ethylene).",
             STYLE + "Split period scene: on the left in 1880 Down House, Charles Darwin and Francis Darwin fit tiny tin-foil caps onto grass seedling tips beside a window; on the right in 1926 Utrecht, young Frits Went places miniature agar jelly blocks onto oat coleoptile stumps." + QUAL_TAIL,
             {"kind": "WHEN", "label": "NOVEMBER 1880 · 1901 · 17 APRIL 1926 · 1934", "hold_s": 3.5}),
            ("04_table_three_callback", 173.0, 2.4, "C", False, None, "reuse",
             "Reuse: verified unused moving window [5.50s..7.90s] of P1:07_table_three_props_1941_neurospora_tube_1960_centrifuge_rotor_and_1961_mortar_pestle_filter_disc (callback, £0).",
             "Reuse P1:07_table_three_props_1941_neurospora_tube_1960_centrifuge_rotor_and_1961_mortar_pestle_filter_disc [5.50s..7.90s] (2.40s distinct non-overlapping tail window from 8.00s source clip).",
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
                row["reuse_of"] = "P1:07_table_three_props_1941_neurospora_tube_1960_centrifuge_rotor_and_1961_mortar_pestle_filter_disc"
                row["reuse_window_s"] = [5.5, 7.9]
                row["reuse_audit"] = {
                    "source_row": "P1:07_table_three_props_1941_neurospora_tube_1960_centrifuge_rotor_and_1961_mortar_pestle_filter_disc",
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
            "film": "080_Beadle-Tatum-Palade-Brenner-Jacob-Nirenberg-Genetic-Code-mRNA",
            "part": p_idx,
            "title": p_title,
            "version": "v01",
            "timing_status": "pre_vo_script_clock (built from genetic_code_script_master_v01.md; retimes onto Scribe STT once VO locks)",
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
        "film": "080_Beadle-Tatum-Palade-Brenner-Jacob-Nirenberg-Genetic-Code-mRNA",
        "version": "v01",
        "date": "2026-10-20",
        "owner": "gemini (J0738)",
        "status": "PRE_VO_BOARDS_V01_NO_MINT",
        "generation_authorized": False,
        "script": "00_Brand/Channel-Setup/ideas/080_Beadle-Tatum-Palade-Brenner-Jacob-Nirenberg-Genetic-Code-mRNA/genetic_code_script_master_v01.md",
        "sources": "00_Brand/Channel-Setup/ideas/080_Beadle-Tatum-Palade-Brenner-Jacob-Nirenberg-Genetic-Code-mRNA/SOURCES_v01.md",
        "credit_snapshot": {
            "flow_balance": 23740,
            "flow_floor": 0,
            "flow_read_at": "2026-10-15T21:42:22Z",
            "vertex_promo_gbp": 71.02,
            "vertex_usable_gbp": 70.02,
        },
        "totals": totals,
        "per_part": per_part_summary,
        "mint_order": "006 > 007 > 008 > 009 > 010 > 011 > 012 > 013 > 014 > 015 > 016 > 017 > 018 > 019 > 020 > 021 > 022 > 023 > 024 > 025 > 026 > 027 > 028 > 029 > 030 > 031 > 032 > 033 > 034 > 035 > 036 > 037 > 038 > 039 > 040 > 041 > 042 > 043 > 044 > 045 > 046 > 047 > 048 > 049 > 050 > 051 > 052 > 053 > 054 > 055 > 056 > 057 > 058 > 059 > 060 > 061 > 062 > 063 > 064 > 065 > 066 > 067 > 068 > 069 > 070 > 071 > 072 > 073 > 074 > 075 > 076 > 077 > 078 > 079 > 080 > 081 > 082 > 083. Nothing in 080 is generation_authorized.",
    }
    (EDIT / "PICTURE_PLAN_v01.json").write_text(json.dumps(plan, indent=2) + "\n")

    sl = [
        "# 080 The Genetic Code: Cracked by an Outsider at 3 AM — Shot list & plate boards v01 (pre-VO)",
        "",
        "Gemini, 20 Oct 2026, J0738. Built from `genetic_code_script_master_v01.md` (`90.3/100 PASS`) and `SOURCES_v01.md`.",
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
        "# 080 price review v01 (pre-VO plate boards)",
        "",
        "Gemini, 20 Oct 2026, J0738. Boards only. **No mint. No spend. No merge.**",
        "Prepared from `genetic_code_script_master_v01.md` (`90.3/100 PASS`) and `SOURCES_v01.md` so 080's full plate board rows, non-emissive Fast prompts, £0 code graphics, and Teach-on-Screen overlays are ready to re-time the moment long VO locks. Parked for Chief.",
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
        f"- **Quality ({totals['Quality']} rows):** readable faces (George Wells Beadle, Edward Lawrie Tatum, Archibald Garrod, George Emil Palade, Sydney Brenner, François Jacob, Matthew Meselson, Francis Crick, Jacques Monod, Marshall Warren Nirenberg, J. Heinrich Matthaei, Har Gobind Khorana, Charles Darwin, Francis Darwin, Frits Warmolt Went), 1941 Stanford irradiated *Neurospora* Tube #299 & 1955 Rockefeller `ribosome` discovery, Good Friday 15 April 1960 Cambridge & Caltech `messenger RNA` discovery, 27 May 1961 3:00 a.m. Bethesda `poly-U` (`UUU = Phenylalanine`) breakthrough & August 1961 Moscow Congress, and the 2 Explorer beats.",
        f"- **Fast ({totals['Fast']} rows, non-emissive):** daylight prop and laboratory shots (1941 *Neurospora* slants, RNA Tie Club woollen tie & October 1961 *PNAS* offprint pan, 3-object callback bench, minimal vs Vitamin B6 bread-mould racks & 1955 Palade ribosome electron micrograph, sculpted cutaway cell nucleus & rough ER ribosome model, 1960 Caltech cesium-chloride density-gradient tubes & May 1961 *Nature* issue, wooden 3-letter triplet reading-frame demonstrator, 1961 Bethesda chilled alumina mortar with 20-tube rack & brass filter planchets, sculpted ribosome/mRNA model beside phototropic grass seedlings on museum plinth). Zero candles, flames, sparks, or glowing elements on Fast.",
        f"- **£0 code graphics ({totals['code_graphic']} rows):**",
        "  1. `P1:04_beadle_tatum_1941_palade_1955_brenner_jacob_1961_and_nirenberg_matthaei_1961_central_dogma_codon_chart` — `DNA → mRNA → ribosome → protein`, `4³ = 64` triplet codons, and Nirenberg & Matthaei's `39,800 cpm` vs `70 cpm` `poly-U` breakthrough (`SCALE: if you read the four letters of DNA one at a time, you only get four words; in pairs, you only get sixteen — so life reads DNA in three-letter triplets, giving sixty-four possible words to spell twenty amino acids and punctuation stops`)",
        "  2. `P1:06_nirenberg_matthaei_27_may_1961_poly_u_phenylalanine_39800_cpm_chart` — Marshall Nirenberg & Heinrich Matthaei (27 May 1961 / October 1961 *PNAS* Table 1) 20-tube cell-free `poly-U` radioactive assay (`SCALE: feeding a ribbon of pure U-U-U-U-U into crushed bacteria and getting back a chain of pure phenylalanine was the Rosetta Stone of biology — like typing a single repeated letter into an alien cipher machine and watching it print out its first English word`)",
        "  3. `P2:02_beadle_tatum_1941_neurospora_tube_299_and_palade_1955_ribosome_em_chart` — George Beadle & Edward Tatum (15 November 1941 *PNAS*) *Neurospora* Tube #299 `One Gene–One Enzyme` chart + George Palade (January 1955) ribosome EM map (`SCALE: a single human cell packs up to ten million ribosomes into a space smaller than a speck of dust — ten million microscopic 3D printers humming side by side to build every protein in your body`)",
        "  4. `P3:02_brenner_jacob_meselson_may_1961_mrna_gradient_and_crick_brenner_dec_1961_triplet_frameshift_chart` — Brenner, Jacob & Meselson (13 May 1961 *Nature*) heavy-isotope `mRNA` density gradient & Crick, Barnett, Brenner & Watts-Tobin (30 December 1961 *Nature*) `+1/+2` vs `+3` triplet frameshift chart (`SCALE: Sydney Brenner and François Jacob proved that DNA never leaves the nucleus for the same reason an architect never leaves the only master blueprint of a skyscraper out in the mud — instead, the cell prints disposable mRNA photocopies and sends them out to the ribosome construction crew`)",
        "  5. `P4:02_nirenberg_matthaei_leder_and_khorana_1961_1966_complete_64_codon_genetic_code_dictionary_chart` — Nirenberg, Matthaei, Leder & Khorana (1961–1966) complete 64-codon genetic code dictionary (`SCALE: every living thing on Earth — from a blade of grass and a bacterium in your gut to the neurons firing in your brain right now — reads the exact same sixty-four-word dictionary that Marshall Nirenberg and Heinrich Matthaei cracked at three in the morning, proving that all life on Earth shares a single family tree`)",
        "  6. `P5:01_timeline_1941_1968_and_universal_64_codon_genetic_code_chart` — completed timeline (1941 → 1968) + One Gene–One Enzyme, ribosomes, mRNA & 64-codon genetic code (`SCALE: from X-rayed bread mould at Stanford and a Good Friday conversation in Cambridge to a radiation counter ticking at 3 a.m. in Bethesda, scientists cracked the four-letter operating system of life on Earth`)",
        f"- **£0 verified reuse ({totals['reuse']} row):** `P5:04_table_three_callback` uses the 2.40 s unused moving tail `[5.50s..7.90s]` of `P1:07_table_three_props_1941_neurospora_tube_1960_centrifuge_rotor_and_1961_mortar_pestle_filter_disc`.",
        "",
        "## Mint order",
        "",
        "006 > 007 > 008 > 009 > 010 > 011 > 012 > 013 > 014 > 015 > 016 > 017 > 018 > 019 > 020 > 021 > 022 > 023 > 024 > 025 > 026 > 027 > 028 > 029 > 030 > 031 > 032 > 033 > 034 > 035 > 036 > 037 > 038 > 039 > 040 > 041 > 042 > 043 > 044 > 045 > 046 > 047 > 048 > 049 > 050 > 051 > 052 > 053 > 054 > 055 > 056 > 057 > 058 > 059 > 060 > 061 > 062 > 063 > 064 > 065 > 066 > 067 > 068 > 069 > 070 > 071 > 072 > 073 > 074 > 075 > 076 > 077 > 078 > 079 > 080 > 081 > 082 > 083. `generation_authorized` is `false` on every row.",
    ])
    (EDIT / "PRICE_REVIEW_v01.md").write_text("\n".join(pr_lines) + "\n")
    print(f"080 v01 boards written: {totals['rows']} rows, Flow expected={totals['flow_credits_expected']}")


if __name__ == "__main__":
    main()
