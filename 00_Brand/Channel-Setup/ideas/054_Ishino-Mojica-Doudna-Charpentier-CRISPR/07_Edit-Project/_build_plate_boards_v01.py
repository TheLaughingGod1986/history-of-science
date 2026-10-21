#!/usr/bin/env python3
"""HOS 054 (CRISPR Gene Scissors: The Secret Inside Yogurt Bacteria) pre-VO plate boards v01. J0600. No mint, no spend.

Built from 00_Brand/Channel-Setup/ideas/054_Ishino-Mojica-Doudna-Charpentier-CRISPR/crispr_script_master_v01.md
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
        "Part 01 — How a Bowl of Dairy Yogurt Revealed Programmable Scissors That Edit Human DNA",
        [
            ("01_yogurt_spoon_streptococcus_thermophilus_phage_mugshot_and_cas9_scissors", 0.0, 5.5, "A", False, "BACTERIAL DNA SCISSORS", "Quality",
             "Quality: Short frame 0 / answer image (0:03) + a porcelain spoon lifts creamy yogurt from a bowl, zooming into a Streptococcus thermophilus yogurt bacterium where a bacteriophage virus attacks; the bacterium snips a 30-letter mugshot of the viral DNA into its repeating CRISPR archive and hands a 20-letter guide RNA to Cas9 molecular scissors that slice a mutated human sickle-cell gene cleanly in two on 28 June 2012.",
             STYLE + "Split period-and-molecular scene: on the left, a porcelain spoon lifts creamy dairy yogurt beside a starter culture dish; on the right inside a bacterial cell, a Cas9 molecular scissors enzyme guided by a single RNA ribbon slices a target DNA double helix cleanly in two." + QUAL_TAIL,
             {"kind": "WHEN", "label": "28 JUNE 2012", "timeline_step": "4/4 · 28 Jun 2012 (Emmanuelle Charpentier & Jennifer Doudna engineer programmable single-guide RNA CRISPR-Cas9 scissors)", "hold_s": 3.5}),
            ("02_ishino_1987_mojica_2005_barrangou_2007_yogurt_and_charpentier_doudna_2012_split", 5.5, 6.0, "B", False, "PALINDROMES, YOGURT, CRISPR-Cas9", "Quality",
             "Quality: complex three-part composition (Yoshizumi Ishino in Osaka in December 1987 and Francisco Mojica in Alicante in February 2005 matching 29-bp repeats and 32-bp spacers to bacteriophages; Rodolphe Barrangou and Philippe Horvath at Danisco in March 2007 testing phage-resistant yogurt cultures; and Emmanuelle Charpentier and Jennifer Doudna on 28 June 2012 unveiling the single-guide RNA Cas9 scissors).",
             STYLE + "Three-panel period composition: on the left, Japanese and Spanish microbiologists inspecting repeating DNA sequence strips; in the centre, two dairy food scientists in white coats beside stainless-steel yogurt fermentation vats; on the right, two women biochemists presenting a molecular model of RNA-guided Cas9 gene scissors." + QUAL_TAIL,
             None),
            ("03_sickle_cell_capillary_jam_vs_cas9_20_letter_rna_snipping_single_dna_typo", 11.5, 6.0, "C", False, "1 TYPO IN 3 BILLION LETTERS", "Quality",
             "Quality: complex anatomical and molecular reveal (inside a human blood vessel, rigid crescent-shaped sickle red blood cells jam a narrow capillary because of a single A-to-T DNA typo in the beta-globin gene; cut to a Cas9 enzyme guided by a 20-letter RNA zipping past healthy letters to snip the exact target site).",
             STYLE + "Inside a warm crimson capillary vessel, crescent-shaped sickle red blood cells jam a narrow bend, dissolving to a molecular Cas9 enzyme guided by a twenty-step RNA ribbon locking onto one exact rung of a DNA helix and snipping both strands cleanly." + QUAL_TAIL,
             {"kind": "WHEN", "label": "DECEMBER 1987 · FEBRUARY 2005 · 23 MARCH 2007 · 28 JUNE 2012", "timeline_step": "1/4 · Dec 1987 (Ishino) · 2/4 · Feb 2005 (Mojica) · 3/4 · 23 Mar 2007 (Barrangou & Horvath) · 4/4 · 28 Jun 2012 (Charpentier & Doudna)", "hold_s": 3.5}),
            ("04_crispr_29bp_repeat_32bp_spacer_and_sgrna_4_to_20_1_1_trillion_address_chart", 17.5, 8.0, "E", False, "CRISPR 29-BP REPEAT / 32-BP VIRAL SPACER & 20-NT sgRNA + NGG PAM (4^20 = 1,099,511,627,776 ADDRESSES VS 3.2B HUMAN GENOME)", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked CRISPR array & Cas9 targeting diagram from Ishino (1987), Mojica (2005), Barrangou & Horvath (2007 Science), and Jinek, Chylinski, Doudna & Charpentier (28 June 2012 Science) shows 29-bp palindromic repeats separated by 32-bp viral protospacers, transcribed into a 20-nucleotide single-guide RNA (sgRNA) that locks Cas9 onto a matching 20-bp DNA target adjacent to a 3-bp NGG PAM sequence (4^20 = 1.1 trillion possible addresses).",
             {"kind": "DATA", "label": "CRISPR 29-BP REPEAT / 32-BP SPACER & 20-NT sgRNA TARGETING (4^20 = 1.1 TRILLION COMBINATIONS VS 3.2B GENOME)", "detail": "Inked CRISPR-Cas9 20-letter RNA address & specificity chart on period paper showing a 29-bp repeat / 32-bp viral spacer array and a 20-nucleotide sgRNA + NGG PAM locating a unique target among 3.2 billion human DNA base pairs (since 4^20 = 1,099,511,627,776 combinations)", "scale": "a twenty-letter RNA guide offers more than one trillion possible four-letter combinations — over three hundred times more addresses than there are letters in the entire three-billion-letter human genome, letting Cas9 find one exact genetic street address inside a cell", "who_card": "Yoshizumi Ishino (born 1957) — Japanese molecular biologist · Francisco J. M. Mojica (born 1963) — Spanish microbiologist · Rodolphe Barrangou (born 1974) — French-American food scientist · Philippe Horvath (born 1970) — French molecular biologist · Emmanuelle Charpentier (born 1968) — French microbiologist · Jennifer A. Doudna (born 1964) — American biochemist", "when_stamp": "December 1987 · February 2005 · 23 March 2007 · 28 June 2012", "hold_s": 3.8}),
            ("05_yogurt_jar_petri_dish_micropipette_and_brass_dna_scissors_model_pan", 25.5, 5.5, "A", False, "20-LETTER RNA POSTCODE", "Fast",
             "Fast: daylight macro pan across a glass dairy yogurt jar, a bacterial culture Petri dish, a precision micropipette, and a brass-and-wood Cas9 DNA-scissors model on an oak laboratory bench between code graphics so two full-frame graphics never run back to back. Nothing emissive, no face.",
             STYLE + "In crisp daylight on an oak laboratory bench, the camera pans smoothly across a glass jar of creamy yogurt, an agar Petri dish, a precision micropipette, and a brass-and-wood molecular DNA-scissors model." + FAST_TAIL,
             None),
            ("06_zfn_talen_protein_engineering_vs_crispr_cas9_20nt_rna_reprogramming_chart", 31.0, 8.0, "E", False, "4^20 = 1.1 TRILLION", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period parchment, an inked gene-editing reprogramming comparison chart contrasts earlier protein-guided nucleases (ZFNs and TALENs, requiring months of custom 3D protein engineering per DNA target) against RNA-guided CRISPR-Cas9 (1 universal Cas9 endonuclease + interchangeable 20-nucleotide guide RNA synthesized in hours).",
             {"kind": "DATA", "label": "CUSTOM PROTEIN NUCLEASES (MONTHS PER TARGET) VS UNIVERSAL CAS9 + 20-NT GUIDE RNA (HOURS PER TARGET)", "detail": "Inked gene-editing reprogramming comparison chart contrasting protein-guided nucleases (new 3D protein required for every DNA sequence) against RNA-guided CRISPR-Cas9 (1 universal Cas9 endonuclease + interchangeable 20-nt guide RNA)", "scale": "before CRISPR, targeting a new gene was like forging a brand-new steel key from scratch for every door in a city — whereas with CRISPR-Cas9, the steel scissors stay the same and you simply type a new twenty-letter postcode onto a strip of RNA", "hold_s": 3.8}),
            ("07_table_three_props_osaka_gel_film_yogurt_starter_vat_jar_and_cas9_sgrna_model", 39.0, 5.5, "C", False, "1987 TO 2023", "Fast",
             "Fast: daylight prop table (callback source for Part 05: Yoshizumi Ishino's 1987 Osaka sequencing gel film, a glass Danisco yogurt starter culture jar, and a brass-and-wood Cas9 single-guide RNA model). Nothing emissive.",
             STYLE + "On an oak workbench in soft window light sit three objects side by side: a framed 1987 DNA sequencing autoradiograph strip, a glass dairy yogurt culture jar with a porcelain spoon, and a brass-and-wood molecular scissors model with an RNA ribbon." + FAST_TAIL,
             None),
            ("08_explorer_dairy_sheriff_handing_20_letter_wanted_poster_to_cas9_scissors_at_ngg_sign", 62.0, 5.5, "A", True, None, "Quality",
             "Quality: Explorer beat 1 (locked character reference, after 1:00).",
             STYLE + "Standing beside a wooden mugshot wall inside a stylized bacterial cell, the Explorer hands a rolled scroll to a pair of brass molecular scissors that glide along a giant DNA rope, pause beside a three-pronged brass marker post, and snip an invading viral strand cleanly in half." + EXP_TAIL,
             None),
            ("09_yoshizumi_ishino_december_1987_osaka_examining_29bp_palindrome_gel", 67.5, 5.5, "B", False, "OSAKA, DECEMBER 1987", "Quality",
             "Quality: readable face (at Osaka University in December 1987, 30-year-old Japanese molecular biologist Yoshizumi Ishino examines a sequencing autoradiograph film showing five identical 29-base-pair palindromic repeats separated by 32-base-pair spacers in E. coli).",
             STYLE + "In a 1987 Osaka University molecular biology laboratory, young Japanese researcher Yoshizumi Ishino in a white lab coat holds up a developed DNA sequencing film and traces five repeating ladder patterns with a fine pen." + QUAL_TAIL,
             {"kind": "WHEN", "label": "OSAKA, DECEMBER 1987", "timeline_step": "1/4 · Dec 1987 (Yoshizumi Ishino discovers 29-bp palindromic repeats and 32-bp spacers in E. coli)", "hold_s": 3.5}),
        ],
    ),
    (
        2,
        "Part 02 — December 1987 – February 2005: Yoshizumi Ishino's Mystery Palindromes & Francisco Mojica's Viral Mugshot Discovery",
        [
            ("01_ishino_1987_osaka_and_mojica_jansen_1993_2005_alicante_viral_mugshots", 73.0, 6.5, "A", False, "VIRAL MUGSHOTS IN DNA", "Quality",
             "Quality: readable faces (Yoshizumi Ishino in Osaka in December 1987 tracing five 29-bp palindromic repeats on an autoradiograph film, dissolving to Spanish microbiologist Francisco Mojica in Alicante and Dutch biologist Ruud Jansen in 1993–February 2005 matching 32-bp CRISPR spacers to bacteriophage P1 genomes).",
             STYLE + "Split period scene: on the left in 1987 Osaka, Yoshizumi Ishino inspects a five-repeat DNA ladder film; on the right in 2005 Alicante, Spanish microbiologist Francisco Mojica and Dutch researcher Ruud Jansen compare bacterial spacer sequences against bacteriophage diagrams." + QUAL_TAIL,
             {"kind": "WHO", "label": "Ruud Jansen (born 1962) — Dutch molecular biologist", "fact_card": "Viral mugshots in DNA", "when_stamp": "December 1987 · 1993 · March 2002 · February 2005", "timeline_step": "2/4 · Feb 2005 (Francisco Mojica proves CRISPR spacers match bacteriophage viruses)", "hold_s": 3.8}),
            ("02_ishino_1987_jansen_2002_and_mojica_2005_crispr_locus_and_phage_match_chart", 79.5, 8.0, "E", False, "1987 ISHINO 29-BP REPEATS / 32-BP SPACERS, 2002 JANSEN CAS GENES & FEB 2005 MOJICA PHAGE MATCH (>40% BACTERIA, ~90% ARCHAEA)", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked CRISPR locus architecture & viral-spacer match chart from Ishino et al. (Dec 1987, J. Bacteriol. 169: 5429–5433), Jansen et al. (Mar 2002, Mol. Microbiol. 43: 1565–1575), and Mojica et al. (Feb 2005, J. Mol. Evol. 60: 174–182) shows 29-bp palindromic repeats interspaced with 32-bp spacers matching bacteriophage and plasmid genomes across >40% of bacteria and ~90% of archaea.",
             {"kind": "DATA", "label": "CRISPR LOCUS (29-BP REPEATS + 32-BP VIRAL SPACERS) PRESENT IN >40% OF BACTERIA & ~90% OF ARCHAEA", "detail": "Inked CRISPR locus architecture & viral-spacer match chart on period paper from Ishino et al. (Dec 1987, J. Bacteriol. 169: 5429–5433), Jansen et al. (Mar 2002, Mol. Microbiol. 43: 1565–1575), and Mojica et al. (Feb 2005, J. Mol. Evol. 60: 174–182) showing 29-bp palindromic repeats interspaced with 32-bp spacers matching bacteriophage and plasmid genomes across >40% of bacteria and ~90% of archaea", "scale": "for every single bacterium on Earth, there are ten bacteriophage viruses hunting it — so bacteria evolved a genetic mugshot book to remember every virus their ancestors survived", "hold_s": 3.8}),
            ("03_alicante_salt_marsh_sample_jars_and_sequencing_printout_closeup", 87.5, 6.5, "B", False, "2005 — SPACERS MATCH VIRUSES", "Fast",
             "Fast: daylight macro shot of Santa Pola salt-marsh water sample vials, a microscope slide, and a printed DNA alignment sheet with a brass fountain pen on an Alicante wooden desk. Nothing emissive, no face.",
             STYLE + "In crisp daylight on a wooden laboratory desk, glass sample jars of pink salt-marsh brine sit beside a microscope slide and a paper DNA sequence alignment sheet with a fountain pen." + FAST_TAIL,
             None),
            ("04_osaka_1987_autoradiograph_gel_tray_and_magnifying_loupe_pan", 94.0, 5.5, "C", False, "DECEMBER 1987 — FIVE REPEATS", "Fast",
             "Fast: daylight close-up pan across an electrophoresis gel tray, a developed black-and-white sequencing film strip, and a brass magnifying loupe on a 1987 workbench. Nothing emissive, no face.",
             STYLE + "In bright window light on a laboratory bench, an acrylic electrophoresis gel tray and a striped black-and-white DNA film strip rest beside a brass magnifying glass." + FAST_TAIL,
             None),
        ],
    ),
    (
        3,
        "Part 03 — 23 March 2007: How Yogurt Bacteria Proved CRISPR Is a Heritable Immune System — Midpoint Twist",
        [
            ("01_barrangou_ and_horvath_23_mar_2007_danisco_yogurt_phage_immunity", 99.5, 6.5, "A", False, "YOGURT BACTERIA SNIP VIRUSES", "Quality",
             "Quality: readable faces (Danisco food scientists Rodolphe Barrangou and Philippe Horvath on 23 March 2007 in white lab coats beside stainless-steel yogurt fermentation vats and Petri dishes, exposing Streptococcus thermophilus dairy starter cultures to bacteriophages 858 and 2972 and sequencing the surviving colonies).",
             STYLE + "In a modern dairy microbiology laboratory in March 2007, researchers Rodolphe Barrangou and Philippe Horvath in white coats inspect thriving yogurt starter colonies in Petri dishes beside gleaming stainless-steel milk fermentation vats." + QUAL_TAIL,
             {"kind": "FACT", "label": "Yogurt bacteria snip viruses", "when_stamp": "23 March 2007", "timeline_step": "3/4 · 23 Mar 2007 (Rodolphe Barrangou & Philippe Horvath prove yogurt bacteria use CRISPR-Cas9 as an adaptive immune system)", "hold_s": 3.8}),
            ("02_barrangou_horvath_2007_science_spacer_acquisition_10e5_to_10e7_phage_resistance_chart", 106.0, 8.0, "E", False, "23 MAR 2007 BARRANGOU & HORVATH: +1 VIRAL SPACER = 10^5× RESISTANCE, +2–4 SPACERS = >10^7× RESISTANCE (CAS9 REQUIRED)", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked Streptococcus thermophilus phage-resistance & spacer-acquisition chart from Barrangou, Fremaux, Deveau, Richards, Boyaval, Moineau, Romero & Horvath (23 March 2007, Science 315: 1709–1712) shows phage sensitivity dropping 10^5-fold with 1 acquired 30-bp viral spacer and >10^7-fold with 2–4 spacers while cas9 (cas5) inactivation abolishes immunity.",
             {"kind": "DATA", "label": "23 MAR 2007 YOGURT CRISPR PROOF: +1 SPACER CUTS PHAGE INFECTION 100,000× (10^5); +2–4 SPACERS CUT >10,000,000× (10^7)", "detail": "Inked Streptococcus thermophilus phage-resistance & spacer-acquisition chart on period paper from Barrangou, Fremaux, Deveau, Richards, Boyaval, Moineau, Romero & Horvath (23 March 2007, Science 315: 1709–1712) showing phage sensitivity dropping 10^5-fold with 1 acquired 30-bp viral spacer and >10^7-fold with 2–4 spacers while cas9 (cas5) inactivation abolishes immunity", "scale": "adding just one thirty-letter viral mugshot to a yogurt bacterium's CRISPR archive cuts virus infection a hundred thousand times — and every daughter cell inherits that shield the moment it divides", "hold_s": 3.8}),
            ("03_danisco_2007_resistant_vs_lysed_yogurt_culture_dishes_and_milk_flask_closeup", 114.0, 6.5, "B", False, "2007 — ADAPTIVE BACTERIAL IMMUNITY", "Fast",
             "Fast: daylight macro shot of a thriving phage-resistant Streptococcus thermophilus culture dish beside a lysed clear dish, a glass flask of warm milk, and a stainless-steel ladle on a dairy lab bench. Nothing emissive, no face.",
             STYLE + "In crisp daylight on a dairy laboratory table, two glass Petri dishes sit beside a flask of creamy milk and a steel tasting spoon, one dish brimming with healthy colonies." + FAST_TAIL,
             None),
            ("04_stainless_steel_yogurt_fermentation_vats_and_culture_vials_pan", 120.5, 5.5, "C", False, "23 MARCH 2007 — STREPTOCOCCUS THERMOPHILUS", "Fast",
             "Fast: daylight close-up pan across a row of brushed stainless-steel dairy starter vats, pressure gauges, and sealed glass starter culture vials. Nothing emissive, no face.",
             STYLE + "In bright window light inside a dairy research hall, brushed stainless-steel fermentation vessels and brass dial gauges sit beside a rack of glass starter culture vials." + FAST_TAIL,
             None),
        ],
    ),
    (
        4,
        "Part 04 — March 2011 – 28 June 2012: Emmanuelle Charpentier, Jennifer Doudna & the Programmable CRISPR-Cas9 Scissors",
        [
            ("01_charpentier_doudna_2011_san_juan_jinek_2012_sgrna_and_zhang_church_2013_human_cells", 126.0, 6.5, "A", False, "2 BLADES + 1 GUIDE RNA", "Quality",
             "Quality: readable faces (French microbiologist Emmanuelle Charpentier and American biochemist Jennifer Doudna walking down an Old San Juan cobblestone street in Puerto Rico in March 2011, dissolving to Martin Jinek in Berkeley on 28 June 2012 testing the fused single-guide RNA with Cas9 and Feng Zhang and George Church in January 2013 editing human cells).",
             STYLE + "Split period scene: on the left in March 2011, Emmanuelle Charpentier and Jennifer Doudna walk along a sunlit Old San Juan cobblestone street discussing RNA diagrams; on the right in June 2012, Martin Jinek, Feng Zhang, and George Church test single-guide RNA Cas9 scissors in laboratory dishes." + QUAL_TAIL,
             {"kind": "WHO", "label": "Martin Jinek (born 1979) — Czech biochemist · Feng Zhang (born 1981) — Chinese-American biochemist · George M. Church (born 1954) — American geneticist", "fact_card": "2 blades + 1 guide RNA", "when_stamp": "31 March 2011 · 28 June 2012 · January 2013 · 2020", "timeline_step": "4/4 · 28 Jun 2012 (Charpentier & Doudna publish programmable single-guide RNA CRISPR-Cas9 in Science; 2020 Nobel Prize)", "hold_s": 3.8}),
            ("02_deltcheva_2011_tracrrna_and_jinek_doudna_charpentier_2012_chimeric_sgrna_cas9_chart", 132.5, 8.0, "E", False, "31 MAR 2011 tracrRNA & 28 JUN 2012 JINEK/DOUDNA/CHARPENTIER CHIMERIC 20-NT sgRNA + HNH/RuvC CAS9 CLEAVAGE AT NGG PAM", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked dual-RNA vs chimeric single-guide RNA (sgRNA) Cas9 cleavage diagram from Deltcheva & Charpentier (31 Mar 2011 Nature 471: 602–607) and Jinek, Chylinski, Fonfara, Hauer, Doudna & Charpentier (28 Jun 2012 Science 337: 816–821) shows crRNA:tracrRNA fused into a single sgRNA with a customizable 20-nt 5' guide directing HNH and RuvC nuclease domains to cut both DNA strands 3 bp upstream of an NGG PAM.",
             {"kind": "DATA", "label": "28 JUN 2012 SINGLE-GUIDE RNA (crRNA + tracrRNA FUSION) DIRECTING HNH & RuvC BLADES 3 BP UPSTREAM OF NGG PAM", "detail": "Inked dual-RNA vs chimeric single-guide RNA (sgRNA) Cas9 cleavage diagram on period paper from Deltcheva & Charpentier (31 Mar 2011 Nature 471: 602–607) and Jinek, Chylinski, Fonfara, Hauer, Doudna & Charpentier (28 Jun 2012 Science 337: 816–821) showing crRNA:tracrRNA fused into a single sgRNA with a customizable 20-nt 5' guide directing HNH and RuvC nuclease domains to cut both DNA strands 3 bp upstream of an NGG PAM", "scale": "the three-letter PAM sign acts like a safety catch on a pair of scissors — because the bacterium's own CRISPR mugshot album lacks that three-letter tag, Cas9 slices invading viruses to pieces without ever cutting its own DNA", "hold_s": 3.8}),
            ("03_berkeley_2012_five_target_gel_lanes_pipette_and_cas9_ribbon_model_closeup", 140.5, 6.5, "B", False, "28 JUNE 2012 — PROGRAMMABLE SCISSORS", "Fast",
             "Fast: daylight macro shot of an agarose gel tray showing five cleanly cleaved DNA bands, a micropipette with reaction tubes, and a brass-and-wood model of Cas9 holding a single fused RNA loop on a Berkeley bench. Nothing emissive, no face.",
             STYLE + "In crisp daylight on a biochemistry bench, an agarose gel tray with five sharp DNA bands sits beside a micropipette, reaction tubes, and a brass-and-wood model of two RNA ribbons joined by a loop." + FAST_TAIL,
             None),
            ("04_explorer_stitching_crrna_and_tracrrna_into_single_guide_rna_and_snipping_dna_typo", 147.0, 5.5, "B", True, None, "Quality",
             "Quality: Explorer beat 2 (locked character reference).",
             STYLE + "Standing beside a giant DNA double helix, the Explorer stitches two separate coloured ribbons together with a four-bead loop into one single guide ribbon, slots it into a pair of brass molecular scissors, and snips a crooked rung cleanly out of the helix." + EXP_TAIL,
             None),
        ],
    ),
    (
        5,
        "Part 05 — From Yogurt Vats to Curing Sickle-Cell Disease — & How Your Inner Ear Amplifies Sound",
        [
            ("01_timeline_1987_2023_and_somatic_sickle_cell_stem_cell_cure_chart", 152.5, 8.5, "E", False, "1987–2023 TIMELINE · ISHINO REPEATS, MOJICA PHAGES, BARRANGOU YOGURT, DOUDNA/CHARPENTIER Cas9 & NOV 2023 CASGEVY SICKLE-CELL CURE", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, the 4-date timeline completes: Dec 1987 (Yoshizumi Ishino discovers 29-bp palindromic repeats and 32-bp spacers in E. coli) · Feb 2005 (Francisco Mojica proves CRISPR spacers match bacteriophage viruses) · 23 Mar 2007 (Rodolphe Barrangou & Philippe Horvath prove yogurt bacteria use CRISPR-Cas9 as an adaptive immune system) · 28 Jun 2012 (Emmanuelle Charpentier & Jennifer Doudna engineer programmable single-guide RNA CRISPR-Cas9 scissors; first human CRISPR cure approved Nov 2023).",
             {"kind": "DATA", "label": "1987–2023 CRISPR TIMELINE · OSAKA REPEATS, YOGURT PHAGES, 2012 sgRNA SCISSORS & NOV 2023 SICKLE-CELL STEM-CELL CURE", "detail": "Animated 4-date timeline (Dec 1987 → 28 Jun 2012 / Nov 2023) alongside the ex-vivo adult hematopoietic stem-cell editing cure for sickle-cell disease", "scale": "just twenty-five years separated Yoshizumi Ishino's puzzling bacterial repeats in nineteen eighty-seven from programmable DNA scissors in twenty twelve — and eleven years after that, the first human patients were cured of sickle-cell disease", "when_stamp": "1987–2023 · November 2023", "timeline_step": "4/4 · 1987–2023 timeline complete", "hold_s": 3.8}),
            ("02_stem_cell_infusion_bag_yogurt_bowl_and_cas9_model_on_plinth_pan", 161.0, 5.5, "A", False, "SOMATIC STEM-CELL CURE", "Fast",
             "Fast: daylight close-up of a clinical stem-cell infusion bag beside a porcelain bowl of yogurt and a brass Cas9 molecular scissors model on a wooden museum plinth. Nothing emissive, no face.",
             STYLE + "In crisp daylight on a wooden museum plinth, a clear medical stem-cell infusion bag hangs beside a porcelain bowl of dairy yogurt and a brass-and-wood molecular scissors model." + FAST_TAIL,
             None),
            ("03_helmholtz_1863_bekesy_1928_silver_dust_cochlea_and_kemp_1978_ear_echo_handoff", 166.5, 6.5, "C", False, "THE ECHOING INNER EAR", "Quality",
             "Quality: readable faces (Hermann von Helmholtz in 1863 beside a piano and Hungarian biophysicist Georg von Békésy in 1928–1947 sprinkling glittering silver dust onto the pea-sized spiral cochlea under strobe light, alongside British physicist David Kemp in July 1978 recording otoacoustic emissions from a living human ear — handoff to 055 Hearing & the Cochlea).",
             STYLE + "Split period scene: on the left in 1928 Budapest, Georg von Békésy peers through a microscope at silver dust glittering along a spiral inner-ear model beside Helmholtz's resonator; on the right in July 1978 London, physicist David Kemp records an acoustic echo from a miniature ear-canal microphone probe." + QUAL_TAIL,
             {"kind": "WHEN", "label": "1863 · 1928–1947 · JULY 1978", "hold_s": 3.5}),
            ("04_table_three_callback", 173.0, 2.4, "C", False, None, "reuse",
             "Reuse: verified unused moving window [5.50s..7.90s] of P1:07_table_three_props_osaka_gel_film_yogurt_starter_vat_jar_and_cas9_sgrna_model (callback, £0).",
             "Reuse P1:07_table_three_props_osaka_gel_film_yogurt_starter_vat_jar_and_cas9_sgrna_model [5.50s..7.90s] (2.40s distinct non-overlapping tail window from 8.00s source clip).",
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
                row["reuse_of"] = "P1:07_table_three_props_osaka_gel_film_yogurt_starter_vat_jar_and_cas9_sgrna_model"
                row["reuse_window_s"] = [5.5, 7.9]
                row["reuse_audit"] = {
                    "source_row": "P1:07_table_three_props_osaka_gel_film_yogurt_starter_vat_jar_and_cas9_sgrna_model",
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
            "film": "054_Ishino-Mojica-Doudna-Charpentier-CRISPR",
            "part": p_idx,
            "title": p_title,
            "version": "v01",
            "timing_status": "pre_vo_script_clock (built from crispr_script_master_v01.md; retimes onto Scribe STT once VO locks)",
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
        "film": "054_Ishino-Mojica-Doudna-Charpentier-CRISPR",
        "version": "v01",
        "date": "2026-10-18",
        "owner": "gemini (J0600)",
        "status": "PRE_VO_BOARDS_V01_NO_MINT",
        "generation_authorized": False,
        "script": "00_Brand/Channel-Setup/ideas/054_Ishino-Mojica-Doudna-Charpentier-CRISPR/crispr_script_master_v01.md",
        "sources": "00_Brand/Channel-Setup/ideas/054_Ishino-Mojica-Doudna-Charpentier-CRISPR/SOURCES_v01.md",
        "credit_snapshot": {
            "flow_balance": 23740,
            "flow_floor": 0,
            "flow_read_at": "2026-10-15T21:42:22Z",
            "vertex_promo_gbp": 71.02,
            "vertex_usable_gbp": 70.02,
        },
        "totals": totals,
        "per_part": per_part_summary,
        "mint_order": "006 > 007 > 008 > 009 > 010 > 011 > 012 > 013 > 014 > 015 > 016 > 017 > 018 > 019 > 020 > 021 > 022 > 023 > 024 > 025 > 026 > 027 > 028 > 029 > 030 > 031 > 032 > 033 > 034 > 035 > 036 > 037 > 038 > 039 > 040 > 041 > 042 > 043 > 044 > 045 > 046 > 047 > 048 > 049 > 050 > 051 > 052 > 053 > 054 > 055 > 056. Nothing in 054 is generation_authorized.",
    }
    (EDIT / "PICTURE_PLAN_v01.json").write_text(json.dumps(plan, indent=2) + "\n")

    sl = [
        "# 054 CRISPR Gene Scissors: The Secret Inside Yogurt Bacteria — Shot list & plate boards v01 (pre-VO)",
        "",
        "Gemini, 18 Oct 2026, J0600. Built from `crispr_script_master_v01.md` (`91.2 PASS`) and `SOURCES_v01.md`.",
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
        "# 054 price review v01 (pre-VO plate boards)",
        "",
        "Gemini, 18 Oct 2026, J0600. Boards only. **No mint. No spend. No merge.**",
        "Prepared from `crispr_script_master_v01.md` (`91.2 PASS`) and `SOURCES_v01.md` so 054's full plate board rows, non-emissive Fast prompts, £0 code graphics, and Teach-on-Screen overlays are ready to re-time the moment long VO locks. Parked for Chief.",
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
        f"- **Quality ({totals['Quality']} rows):** readable faces (Yoshizumi Ishino, Francisco J. M. Mojica, Ruud Jansen, Rodolphe Barrangou, Philippe Horvath, Emmanuelle Charpentier, Jennifer A. Doudna, Martin Jinek, Feng Zhang, George M. Church, Hermann von Helmholtz, Georg von Békésy, David T. Kemp), December 1987 Osaka E. coli 29-bp repeat discovery, February 2005 Alicante phage-spacer match, 23 March 2007 Danisco yogurt phage immunity proof, March 2011 Old San Juan & 28 June 2012 single-guide RNA Cas9 discovery, and the 2 Explorer beats.",
        f"- **Fast ({totals['Fast']} rows, non-emissive):** daylight prop and laboratory shots (yogurt jar, Petri dish, micropipette & brass Cas9 model pan, 3-object callback bench, Santa Pola salt-marsh vials & sequence alignment printout, Osaka 1987 electrophoresis gel tray & loupe, Danisco resistant vs lysed culture dishes & milk flask, stainless-steel yogurt fermentation vats, Berkeley 2012 five-lane gel tray & sgRNA model, clinical stem-cell infusion bag & yogurt bowl on museum plinth). Zero candles, flames, sparks, or glowing elements on Fast.",
        f"- **£0 code graphics ({totals['code_graphic']} rows):**",
        "  1. `P1:04_crispr_29bp_repeat_32bp_spacer_and_sgrna_4_to_20_1_1_trillion_address_chart` — 29-bp repeat / 32-bp viral spacer array and 20-nt sgRNA + NGG PAM locating a unique target among 3.2 billion human DNA base pairs (4^20 = 1,099,511,627,776 combinations) (`SCALE: a twenty-letter RNA guide offers more than one trillion possible four-letter combinations — over three hundred times more addresses than there are letters in the entire three-billion-letter human genome, letting Cas9 find one exact genetic street address inside a cell`)",
        "  2. `P1:06_zfn_talen_protein_engineering_vs_crispr_cas9_20nt_rna_reprogramming_chart` — protein-guided nucleases (ZFNs/TALENs, new 3D protein required per target) vs RNA-guided CRISPR-Cas9 (1 universal Cas9 + interchangeable 20-nt guide RNA) (`SCALE: before CRISPR, targeting a new gene was like forging a brand-new steel key from scratch for every door in a city — whereas with CRISPR-Cas9, the steel scissors stay the same and you simply type a new twenty-letter postcode onto a strip of RNA`)",
        "  3. `P2:02_ishino_1987_jansen_2002_and_mojica_2005_crispr_locus_and_phage_match_chart` — Ishino (1987), Jansen (2002), and Mojica (2005) CRISPR locus architecture and viral spacer matches across >40% of bacteria and ~90% of archaea (`SCALE: for every single bacterium on Earth, there are ten bacteriophage viruses hunting it — so bacteria evolved a genetic mugshot book to remember every virus their ancestors survived`)",
        "  4. `P3:02_barrangou_horvath_2007_science_spacer_acquisition_10e5_to_10e7_phage_resistance_chart` — Barrangou & Horvath's 23 March 2007 Streptococcus thermophilus phage-resistance chart (+1 spacer = 10^5-fold drop in sensitivity, +2–4 spacers = >10^7-fold drop, cas9 required) (`SCALE: adding just one thirty-letter viral mugshot to a yogurt bacterium's CRISPR archive cuts virus infection a hundred thousand times — and every daughter cell inherits that shield the moment it divides`)",
        "  5. `P4:02_deltcheva_2011_tracrrna_and_jinek_doudna_charpentier_2012_chimeric_sgrna_cas9_chart` — Deltcheva & Charpentier's 2011 tracrRNA and Jinek, Doudna & Charpentier's 28 June 2012 chimeric single-guide RNA directing HNH and RuvC cleavage 3 bp upstream of an NGG PAM (`SCALE: the three-letter PAM sign acts like a safety catch on a pair of scissors — because the bacterium's own CRISPR mugshot album lacks that three-letter tag, Cas9 slices invading viruses to pieces without ever cutting its own DNA`)",
        "  6. `P5:01_timeline_1987_2023_and_somatic_sickle_cell_stem_cell_cure_chart` — completed 4-date timeline (Dec 1987 → 28 Jun 2012 / Nov 2023) + ex-vivo adult stem-cell cure for sickle-cell disease (`SCALE: just twenty-five years separated Yoshizumi Ishino's puzzling bacterial repeats in nineteen eighty-seven from programmable DNA scissors in twenty twelve — and eleven years after that, the first human patients were cured of sickle-cell disease`)",
        f"- **£0 verified reuse ({totals['reuse']} row):** `P5:04_table_three_callback` uses the 2.40 s unused moving tail `[5.50s..7.90s]` of `P1:07_table_three_props_osaka_gel_film_yogurt_starter_vat_jar_and_cas9_sgrna_model`.",
        "",
        "## Mint order",
        "",
        "006 > 007 > 008 > 009 > 010 > 011 > 012 > 013 > 014 > 015 > 016 > 017 > 018 > 019 > 020 > 021 > 022 > 023 > 024 > 025 > 026 > 027 > 028 > 029 > 030 > 031 > 032 > 033 > 034 > 035 > 036 > 037 > 038 > 039 > 040 > 041 > 042 > 043 > 044 > 045 > 046 > 047 > 048 > 049 > 050 > 051 > 052 > 053 > 054 > 055 > 056. `generation_authorized` is `false` on every row.",
    ])
    (EDIT / "PRICE_REVIEW_v01.md").write_text("\n".join(pr_lines) + "\n")
    print(f"054 v01 boards written: {totals['rows']} rows, Flow expected={totals['flow_credits_expected']}")


if __name__ == "__main__":
    main()
