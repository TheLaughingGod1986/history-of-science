#!/usr/bin/env python3
"""HOS 068 (Epigenetics: Why Identical Twins Grow Up Different) pre-VO plate boards v01. J0676. No mint, no spend.

Built from 00_Brand/Channel-Setup/ideas/068_Lyon-Allfrey-Holliday-Jirtle-Esteller-Epigenetics-Twins/epigenetics_script_master_v01.md
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
        "Part 01 — The Calico Cat in Oxfordshire & the Chemical Sticky Notes on Your DNA",
        [
            ("01_female_calico_cat_beside_identical_twins_and_barr_body_with_histone_methyl_switches", 0.0, 5.5, "A", False, "ONE GENOME, DIFFERENT DESTINIES", "Quality",
             "Quality: Short frame 0 / answer image (0:03) + an orange-and-black female calico cat sits beside two identical human twins as the camera zooms into their chromosomes: in the cat's cells, one of the two X chromosomes crumples into a silent Barr body sphere, while along the twins' identical DNA strands, green histone acetyl switches and red methyl tags flip genes on and off.",
             STYLE + "Split cellular-and-portrait scene: on the left, an orange-and-black patchwork calico cat sits beside a pair of identical human twins; on the right, inside a cell nucleus, one X chromosome folds into a compact sphere while green acetyl keys and red methyl clasps flip along a DNA strand wound around golden histone spools." + QUAL_TAIL,
             {"kind": "WHEN", "label": "HARWELL, 22 APRIL 1961", "timeline_step": "1/3 · 1942, 1949 & 22 Apr 1961 (Conrad Waddington coins epigenetics; Murray Barr spots the Barr body; Mary Lyon discovers random X-chromosome inactivation in mottled mice and calico cats)", "hold_s": 3.5}),
            ("02_mary_lyon_1961_allfrey_1964_holliday_riggs_1975_and_jirtle_2003_esteller_2005_split", 5.5, 6.0, "B", False, "X-INACTIVATION, HISTONE SPOOLS, TWIN EPIGENOMES", "Quality",
             "Quality: complex three-part composition (Mary Lyon at Harwell in Oxfordshire on 22 April 1961 examining mottled female mice and a tortoiseshell cat; Vincent Allfrey in New York in May 1964 and Robin Holliday with Arthur Riggs in January 1975 mapping histone acetylation and CpG DNA methylation; and Randy Jirtle at Duke in August 2003 holding a yellow obese Agouti mouse beside its lean brown genetically identical twin alongside Manel Esteller in Madrid in July 2005).",
             STYLE + "Three-panel period composition: on the left, Mary Lyon in 1961 Oxfordshire holding a mottled mouse beside an orange-and-black calico cat; in the centre, Vincent Allfrey in 1964 New York and Robin Holliday with Arthur Riggs in 1975 inspecting histone spools and methylated DNA; on the right, Randy Jirtle in 2003 with a yellow and a brown Agouti mouse alongside Manel Esteller in 2005 Madrid comparing twin chromosome maps." + QUAL_TAIL,
             None),
            ("03_two_metre_dna_thread_wound_on_histone_octamer_spools_with_methyl_locks_and_acetyl_keys", 11.5, 6.0, "C", False, "DNA IS THE HARDWARE, EPIGENETICS IS THE SOFTWARE", "Quality",
             "Quality: complex conceptual and molecular reveal (a two-metre DNA thread wraps around eight-part histone octamer spools: where red methyl clamps lock the CpG letters, the spool stays tightly shut; where green acetyl tags loosen the histone tails, RNA polymerase reads the open gene).",
             STYLE + "Split molecular chromatin scene: on the left, tightly packed golden histone spools clamped with red methyl locks hold their DNA thread shut; on the right, green acetyl keys loosen the histone tails so the DNA unspools for a passing polymerase enzyme." + QUAL_TAIL,
             {"kind": "WHEN", "label": "22 APRIL 1961 · MAY 1964 · JANUARY 1975 · AUGUST 2003 · 26 JULY 2005", "timeline_step": "1/3 · 1942, 1949 & Apr 1961 (Waddington, Barr & Lyon) · 2/3 · May 1964 & Jan 1975 (Allfrey; Holliday, Pugh & Riggs) · 3/3 · Aug 2003 & Jul 2005 (Waterland & Jirtle; Fraga & Esteller)", "hold_s": 3.5}),
            ("04_lyon_1961_allfrey_1964_holliday_riggs_1975_jirtle_2003_esteller_2005_epigenome_drift_chart", 17.5, 8.0, "E", False, "HISTONE ACETYL (GENE ON) VS CPG METHYLATION (5MC, GENE OFF) & ESTELLER JULY 2005 80-TWIN-PAIR EPIGENETIC DRIFT (50-YR TWINS 4× DIVERGENCE VS 3-YR TWINS)", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked Epigenetic Chromatin Switch & Twin Drift chart from Lyon (22 April 1961 Nature 190: 372–373), Allfrey, Faulkner & Mirsky (May 1964 PNAS 51: 786–794), Holliday & Pugh / Riggs (January 1975 Science 187: 226–232 & Cytogenet. Cell Genet. 14: 9–25), Waterland & Jirtle (August 2003 Mol. Cell. Biol. 23: 5293–5300), and Fraga & Esteller et al. (26 July 2005 PNAS 102: 10604–10609) compares active euchromatin (acetylated histone tails + unmethylated CpG islands = gene ON) against silenced heterochromatin (deacetylated histones + 5-methylcytosine CH3 tags + XIST Barr body = gene OFF), alongside Fraga & Esteller's 80-twin-pair comparison showing 3-year-old identical twins with near-identical profiles vs 50-year-old twins with 4x greater gene-expression divergence.",
             {"kind": "DATA", "label": "HISTONE ACETYLATION (ON) VS CPG METHYLATION (OFF) · ESTELLER 2005 (80 TWIN PAIRS): 50-YR TWINS SHOW ~4× EPIGENETIC DIVERGENCE VS 3-YR TWINS", "detail": "Inked chromatin switch & twin epigenetic drift chart on period paper showing histone tail acetylation (gene ON) vs cytosine CpG methylation (5mC, gene OFF) and comparing 80 monozygotic twin pairs (aged 3 to 74, Fraga & Esteller 2005 PNAS) where 50-year-old twins living apart show ~4x more differentially expressed genes and divergent 5mC/histone marks than 3-year-old twins", "scale": "if your DNA sequence is the printed musical score of a symphony, epigenetic methyl and acetyl tags are the conductor's pencil marks — telling each cell which instruments to play loud and which to silence completely", "who_card": "Mary F. Lyon (1925–2014) — British geneticist · Vincent G. Allfrey (1921–2002) — American cell biologist · Robin Holliday (1932–2014) — British molecular biologist · Arthur D. Riggs (1939–2022) — American geneticist · Randy L. Jirtle (born 1947) — American epigenetics researcher · Robert A. Waterland (born 1966) — American nutritional geneticist · Manel Esteller (born 1968) — Spanish cancer researcher", "when_stamp": "22 April 1961 · May 1964 · January 1975 · August 2003 · 26 July 2005", "hold_s": 3.8}),
            ("05_calico_coat_diagram_histone_spool_model_and_musical_score_with_pencil_marks_pan", 25.5, 5.5, "A", False, "THE CONDUCTOR'S PENCIL MARKS", "Fast",
             "Fast: daylight macro pan across an open musical score with conductor's pencil markings, a carved wooden histone spool wound with cord, and a 1961 Nature offprint on an oak bench between code graphics so two full-frame graphics never run back to back. Nothing emissive, no face.",
             STYLE + "In crisp daylight on an oak genetics bench, the camera pans smoothly across an open symphony score marked with red and green pencil annotations, a wooden histone spool wound with braided cord, and a printed 1961 journal." + FAST_TAIL,
             None),
            ("06_mary_lyon_22_apr_1961_nature_x_inactivation_calico_mosaic_chart", 31.0, 8.0, "E", False, "WHY CALICO CATS ARE FEMALE", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period parchment, an inked Calico Cat X-Inactivation (Lyonization) mosaic map (from Barr & Bertram 1949 & Mary Lyon, 22 April 1961 Nature 190: 372–373) shows an early XX female cat embryo (~100–1,000 cells) where each cell randomly compacts either its orange-allele X chromosome or its black-allele X chromosome into an inactive Barr body coated in XIST RNA, growing into clonal patches of orange and black fur.",
             {"kind": "DATA", "label": "22 APR 1961 MARY LYON (NATURE): RANDOM XX INACTIVATION (50% PATERNAL / 50% MATERNAL BARR BODY) → CLONAL ORANGE & BLACK CALICO PATCHES", "detail": "Inked Mary Lyon (22 April 1961 Nature 190: 372–373) X-chromosome dosage-compensation diagram showing random inactivation of 1 of 2 X chromosomes (50% paternal X / 50% maternal X compacted into a silent Barr body) in early female mammalian embryos, producing clonal orange-and-black coat mosaicism in XX calico females (while XY males are solid orange or black, with rare 1-in-3,000 XXY Klinefelter male calicos)", "scale": "a female calico cat is a walking map of epigenetic switches — every orange patch on her coat is a family of skin cells that switched off the black X chromosome, and every black patch switched off the orange X chromosome", "hold_s": 3.8}),
            ("07_table_three_props_1961_calico_slide_1964_histone_spool_and_2003_methyl_vitamin_bottle", 39.0, 5.5, "C", False, "1961 TO 2005", "Fast",
             "Fast: daylight prop table (callback source for Part 05: Mary Lyon's 1961 Barr-body microscope slide, Vincent Allfrey's 1964 wooden histone octamer spool model, and Waterland & Jirtle's 2003 amber glass bottle of folic acid and B12 methyl-donor vitamins). Nothing emissive.",
             STYLE + "On an oak workbench in soft window light sit three objects side by side: a stained Barr-body microscope slide, a sculpted wooden histone spool wound with DNA cord, and an amber glass bottle of vitamin tablets." + FAST_TAIL,
             None),
            ("08_explorer_swapping_red_methyl_padlock_for_green_acetyl_key_on_histone_spool", 62.0, 5.5, "A", True, None, "Quality",
             "Quality: Explorer beat 1 (locked character reference, after 1:00).",
             STYLE + "Standing beside a large golden histone spool wound with DNA cord, the Explorer unclips a red brass methyl padlock and slots in a green brass acetyl key that loosens the spool so a ribbon of RNA unwinds." + EXP_TAIL,
             None),
            ("09_mary_lyon_22_apr_1961_harwell_examining_mottled_female_mice_and_calico_coat_map", 67.5, 5.5, "B", False, "HARWELL, 22 APRIL 1961", "Quality",
             "Quality: readable face (at Harwell in Oxfordshire on 22 April 1961, British geneticist Mary Lyon examines mottled coat patterns on female mice in her genetics colony).",
             STYLE + "In a 1961 Harwell genetics laboratory in Oxfordshire, British geneticist Mary Lyon gently examines a mottled tortoiseshell mouse beside her notebook of X-chromosome coat-colour pedigrees." + QUAL_TAIL,
             {"kind": "WHEN", "label": "HARWELL, 22 APRIL 1961", "timeline_step": "1/3 · 22 Apr 1961 (Mary Lyon publishes random X-chromosome inactivation in Nature)", "hold_s": 3.5}),
        ],
    ),
    (
        2,
        "Part 02 — 1942, 1949 & 22 April 1961: Mary Lyon's Calico Cat Puzzle & X-Chromosome Inactivation (Lyonization)",
        [
            ("01_waddington_1942_barr_1949_and_mary_lyon_22_apr_1961_harwell_x_inactivation", 73.0, 6.5, "A", False, "ONE X CHROMOSOME CRUMPLED SILENT", "Quality",
             "Quality: readable faces (Conrad Hal Waddington in 1942 sketching his epigenetic landscape and Murray Barr on 30 April 1949 spotting the female Barr body in cat nerve cells, dissolving to Mary Lyon at Harwell on 22 April 1961 connecting the crumpled X chromosome to mottled mice and calico cats).",
             STYLE + "Split period scene: on the left, Conrad Waddington sketches a branching valley landscape while Murray Barr peers through a microscope at a dark Barr body in a female cat neuron; on the right in April 1961 Harwell, Mary Lyon points from a calico cat's orange-and-black patches to a diagram of one open and one compacted X chromosome." + QUAL_TAIL,
             {"kind": "FACT", "label": "One X chromosome crumpled silent", "who_card": "Conrad Hal Waddington (1905–1975) — British embryologist · Murray L. Barr (1908–1995) — Canadian neuroanatomist", "when_stamp": "1942 · 30 April 1949 · 1959 · 22 April 1961", "timeline_step": "1/3 · 1942, 1949 & 22 Apr 1961 (Waddington coins epigenetics; Barr spots the female Barr body; Mary Lyon proves random X-inactivation)", "hold_s": 3.8}),
            ("02_waddington_1942_barr_1949_and_lyon_22_apr_1961_nature_clonal_x_inactivation_chart", 79.5, 8.0, "E", False, "1942 WADDINGTON EPIGENETIC LANDSCAPE · 1949 BARR BODY · 22 APR 1961 LYON (NATURE 190: 372–373): RANDOM EMBRYONIC X SILENCING + 100% CLONAL MITOTIC MEMORY", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked Waddington (1942 epigenetic landscape), Barr & Bertram (30 April 1949 Nature 163: 676–677 female nucleolar satellite / Barr body), and Mary Lyon (22 April 1961 Nature 190: 372–373) X-inactivation inheritance chart shows random embryonic X silencing followed by 100% clonal mitotic memory across all descendant somatic cell divisions.",
             {"kind": "DATA", "label": "1949 BARR BODY & 22 APR 1961 MARY LYON X-INACTIVATION: RANDOM EMBRYONIC SILENCING + 100% CLONAL MEMORY ACROSS CELL DIVISIONS", "detail": "Inked Waddington (1942 epigenetic landscape), Barr & Bertram (30 April 1949 Nature 163: 676–677 female nucleolar satellite / Barr body), and Mary Lyon (22 April 1961 Nature 190: 372–373) X-inactivation inheritance chart on period paper showing random embryonic X silencing followed by 100% clonal mitotic memory across all descendant somatic cell divisions", "scale": "silencing an entire X chromosome inside a female cell is like vacuum-packing one of two identical instruction manuals into a locked vault — and every time that cell divides, the photocopy machine faithfully locks the exact same manual away in the new cell", "hold_s": 3.8}),
            ("03_harwell_1961_barr_body_microscope_slide_and_waddington_landscape_model_closeup", 87.5, 6.5, "B", False, "22 APRIL 1961 — LYONIZATION", "Fast",
             "Fast: daylight macro shot of a stained female cell microscope slide showing a condensed Barr body beside a sculpted wooden model of Waddington's branching valley landscape on a bench. Nothing emissive, no face.",
             STYLE + "In crisp daylight on a 1961 laboratory desk, a stained microscope slide under a brass lens sits beside a carved wooden relief model of branching valleys and a brass marble." + FAST_TAIL,
             None),
            ("04_open_x_chromosome_model_beside_compacted_barr_body_sphere_pan", 94.0, 5.5, "C", False, "ONE OPEN X · ONE SILENT BARR BODY", "Fast",
             "Fast: daylight close-up pan across two sculpted chromosome models on an oak table: one open X-shaped chromosome model and its twin folded into a tight, wrapped sphere. Nothing emissive, no face.",
             STYLE + "In bright window light on an oak table, an open sculpted X chromosome model rests beside an identical X chromosome compacted into a tightly wrapped sphere." + FAST_TAIL,
             None),
        ],
    ),
    (
        3,
        "Part 03 — May 1964 & 24 January 1975: Histone Cotton Reels & DNA Methylation Sticky Notes — Midpoint Twist",
        [
            ("01_vincent_allfrey_may_1964_histone_acetylation_and_holliday_pugh_riggs_jan_1975_methylation", 99.5, 6.5, "A", False, "CHEMICAL LOCKS COPIED AT DIVISION", "Quality",
             "Quality: readable faces (American cell biologist Vincent Allfrey in New York in May 1964 discovering histone tail acetylation switches, dissolving to Robin Holliday, John Pugh, and Arthur Riggs in January 1975 demonstrating how DNMT1 copies CpG DNA methylation marks across cell division).",
             STYLE + "Split period scene: on the left in May 1964 New York, Vincent Allfrey points to acetyl tags loosening eight-part histone spools; on the right in January 1975, Robin Holliday and Arthur Riggs trace a dividing DNA double helix where a maintenance enzyme copies methyl tags onto the new strand." + QUAL_TAIL,
             {"kind": "FACT", "label": "Chemical locks copied at division", "who_card": "C. David Allis (1951–2023) — American molecular biologist", "when_stamp": "May 1964 · 1974 · 24 January 1975 · 1996", "timeline_step": "2/3 · May 1964 & 24 Jan 1975 (Vincent Allfrey discovers histone acetylation switches; Robin Holliday, John Pugh & Arthur Riggs propose heritable CpG DNA methylation)", "hold_s": 3.8}),
            ("02_allfrey_1964_pnas_histone_acetylation_and_holliday_riggs_1975_cpg_methylation_copy_chart", 106.0, 8.0, "E", False, "MAY 1964 ALLFREY (PNAS: HISTONE ACETYLATION → RNA SYNTHESIS ON) & 24 JAN 1975 HOLLIDAY/PUGH & RIGGS (SEMI-CONSERVATIVE CPG 5MC COPYING VIA DNMT1)", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked Allfrey, Faulkner & Mirsky (May 1964, PNAS 51: 786–794) histone acetylation transcription chart & Holliday & Pugh (24 January 1975, Science 187: 226–232) / Riggs (1975) semi-conservative CpG DNA methylation inheritance diagram shows 2 metres of DNA packed into a 6-um nucleus on nucleosome spools and DNMT1 copying 5-methylcytosine (5mC) tags from the parental CpG strand onto the newly replicated daughter strand.",
             {"kind": "DATA", "label": "1964 ALLFREY HISTONE ACETYLATION (2 M DNA IN 6-µM NUCLEUS) & 1975 HOLLIDAY/RIGGS SEMI-CONSERVATIVE CPG METHYLATION COPYING", "detail": "Inked Allfrey, Faulkner & Mirsky (May 1964, PNAS 51: 786–794) histone acetylation transcription chart & Holliday & Pugh (24 January 1975, Science 187: 226–232) / Riggs (1975) semi-conservative CpG DNA methylation inheritance diagram on period paper showing DNMT1 copying 5-methylcytosine (5mC) tags from the parental CpG strand onto the newly replicated daughter strand", "scale": "copying methyl tags during cell division works like tracing carbon paper — when the two DNA strands unzip to replicate, the old strand still wears its methyl sticky notes, and a maintenance enzyme immediately stamps matching sticky notes onto the fresh copy", "hold_s": 3.8}),
            ("03_nucleosome_beads_on_a_string_model_and_1975_science_methylation_diagram_closeup", 114.0, 6.5, "B", False, "24 JANUARY 1975 — DNA METHYLATION MEMORY", "Fast",
             "Fast: daylight macro shot of an eight-part wooden nucleosome beads-on-a-string model beside the 24 January 1975 Science paper showing CpG methyl copying on a bench. Nothing emissive, no face.",
             STYLE + "In crisp daylight on a 1975 molecular biology bench, a row of eight-part wooden histone spools strung with braided DNA cord sits beside an open scientific journal diagram of methylated CpG base pairs." + FAST_TAIL,
             None),
            ("04_replicating_dna_fork_model_with_symmetric_red_cpg_methyl_pins_pan", 120.5, 5.5, "C", False, "MAY 1964 — HISTONE ACETYLATION SWITCHES", "Fast",
             "Fast: daylight close-up pan across a brass-and-wood DNA replication fork model where symmetric red pins mark matching C-G steps on both daughter strands. Nothing emissive, no face.",
             STYLE + "In bright window light on an oak table, a wooden DNA Y-fork model displays paired red brass pins clipped onto matching cytosine-guanine rungs along both daughter branches." + FAST_TAIL,
             None),
        ],
    ),
    (
        4,
        "Part 04 — August 2003 & 26 July 2005: The Yellow-to-Brown Agouti Mouse & Why Identical Twins Drift Apart",
        [
            ("01_waterland_jirtle_aug_2003_duke_agouti_mice_and_fraga_esteller_26_jul_2005_madrid_twins", 126.0, 6.5, "A", False, "DIET SILENCED THE YELLOW MOUSE GENE", "Quality",
             "Quality: readable faces (Robert Waterland and Randy Jirtle at Duke University in August 2003 holding a yellow obese Agouti mouse beside its lean brown genetically identical sibling whose mother received methyl-donor vitamins, dissolving to Manel Esteller in Madrid on 26 July 2005 comparing 80 pairs of identical twins aged 3 to 74).",
             STYLE + "Split period scene: on the left in August 2003 Durham, Randy Jirtle and Robert Waterland compare a plump yellow Agouti mouse with its sleek brown genetically identical sibling; on the right in July 2005 Madrid, Manel Esteller points to chromosome maps from 3-year-old and 50-year-old identical twins." + QUAL_TAIL,
             {"kind": "FACT", "label": "Diet silenced the yellow mouse gene", "when_stamp": "August 2003 · 26 July 2005", "timeline_step": "3/3 · Aug 2003 & 26 Jul 2005 (Waterland & Jirtle silence the yellow Agouti mouse gene with maternal methyl-donor vitamins; Fraga & Esteller prove identical twins diverge epigenetically with age)", "hold_s": 3.8}),
            ("02_waterland_jirtle_aug_2003_agouti_methylation_and_esteller_jul_2005_pnas_80_twins_chart", 132.5, 8.0, "E", False, "AUG 2003 WATERLAND & JIRTLE (AGOUTI A^VY METHYLATION SHIFT → BROWN HEALTHY PUPS) & 26 JUL 2005 FRAGA & ESTELLER (PNAS: 80 TWIN PAIRS, 4× DRIFT AT AGE 50)", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked Waterland & Jirtle (August 2003, Mol. Cell. Biol. 23: 5293–5300) Agouti viable yellow (A^vy) CpG methylation & coat-phenotype chart and Fraga & Esteller (26 July 2005, PNAS 102: 10604–10609) 80-pair monozygotic twin epigenetic divergence plot shows maternal folic acid / B12 / choline / betaine silencing the IAP retrotransposon and 50-year-old twins exhibiting 4x greater gene-expression differences than 3-year-old twins.",
             {"kind": "DATA", "label": "2003 JIRTLE AGOUTI DIET METHYLATION SHIFT & 2005 ESTELLER 80-TWIN-PAIR STUDY (4× EPIGENETIC DIVERGENCE IN 50-YR VS 3-YR TWINS)", "detail": "Inked Waterland & Jirtle (August 2003, Mol. Cell. Biol. 23: 5293–5300) Agouti viable yellow (A^vy) CpG methylation & coat-phenotype chart and Fraga & Esteller (26 July 2005, PNAS 102: 10604–10609) 80-pair monozygotic twin epigenetic divergence plot on period paper", "scale": "the yellow obese Agouti mouse and the lean brown mouse are genetically as identical as two prints from the same photographic negative — the only difference is a handful of microscopic methyl tags that switched the runaway gene off", "hold_s": 3.8}),
            ("03_duke_2003_methyl_donor_vitamin_vials_and_madrid_2005_twin_chromosome_karyotype_closeup", 140.5, 6.5, "B", False, "26 JULY 2005 — IDENTICAL TWIN EPIGENETIC DRIFT", "Fast",
             "Fast: daylight macro shot of labelled glass vials of folic acid, vitamin B12, choline, and betaine beside a 2005 side-by-side twin chromosome methylation map on a bench. Nothing emissive, no face.",
             STYLE + "In crisp daylight on a genetics bench, four stoppered glass vials of vitamin supplements sit beside a printed colour-coded chromosome comparison chart of young and old identical twins." + FAST_TAIL,
             None),
            ("04_explorer_stamping_methyl_tags_onto_agouti_gene_switch_between_yellow_and_brown_mouse_models", 147.0, 5.5, "B", True, None, "Quality",
             "Quality: Explorer beat 2 (locked character reference).",
             STYLE + "Standing at a genetics workbench between a sculpted yellow mouse model and a sleek brown mouse model, the Explorer clips a row of red brass methyl clamps onto the upstream switch of a DNA track, shifting the indicator dial from yellow to brown." + EXP_TAIL,
             None),
        ],
    ),
    (
        5,
        "Part 05 — Why Babies Are Born Young (Epigenetic Reset) — & How a Misfolded Protein Spreads Disease Without Any DNA",
        [
            ("01_timeline_1942_2005_and_embryonic_epigenetic_reprogramming_reset_chart", 152.5, 8.5, "E", False, "1942–2005 TIMELINE · WADDINGTON/BARR/LYON X-INACTIVATION, ALLFREY HISTONES, HOLLIDAY/RIGGS METHYLATION, JIRTLE AGOUTI MICE, ESTELLER TWINS & EMBRYONIC RESET", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, the 3-era timeline completes: 1942, 1949 & 22 Apr 1961 (Conrad Waddington coins epigenetics; Murray Barr spots the Barr body; Mary Lyon discovers random X-chromosome inactivation in mottled mice and calico cats) · May 1964 & Jan 1975 (Vincent Allfrey discovers histone acetylation switches; Robin Holliday, John Pugh & Arthur Riggs propose heritable CpG DNA methylation) · Aug 2003 & 26 Jul 2005 (Robert Waterland & Randy Jirtle silence the yellow Agouti mouse gene with maternal methyl-donor vitamins; Mario Fraga & Manel Esteller prove identical twins diverge epigenetically with age).",
             {"kind": "DATA", "label": "1942–2005 EPIGENETICS TIMELINE · GERMLINE & EARLY EMBRYO EPIGENETIC REPROGRAMMING (~95% METHYLATION RESET TO AGE ZERO)", "detail": "Animated timeline (1942 → 2005) alongside the mammalian germline and pre-implantation embryo epigenetic reprogramming curve wiping ~95% of parental methylation marks clean", "scale": "from a patchwork calico cat in Oxfordshire to eighty pairs of identical twins in Madrid, epigenetics revealed that your DNA writes the alphabet of life, but chemical switches write the story", "when_stamp": "1942–2005", "timeline_step": "3/3 · 1942–2005 timeline complete", "hold_s": 3.8}),
            ("02_clean_slate_embryo_dna_spool_and_folded_vs_misfolded_prion_protein_models_on_plinth_pan", 161.0, 5.5, "A", False, "WIPING THE EPIGENETIC SLATE CLEAN", "Fast",
             "Fast: daylight close-up of a freshly un-tagged golden histone DNA spool beside a pair of sculpted alpha-helical and beta-sheet protein models on a wooden museum plinth. Nothing emissive, no face.",
             STYLE + "In crisp daylight on a wooden museum plinth, a clean golden histone spool wound with un-tagged DNA cord sits beside a sculpted spiral protein model and a flat beta-sheet domino protein model." + FAST_TAIL,
             None),
            ("03_gajdusek_alper_1966_1967_prusiner_9_apr_1982_prions_and_weissmann_1993_knockout_mice_handoff", 166.5, 6.5, "C", False, "PRIONS, KURU & MAD COW DISEASE", "Quality",
             "Quality: readable faces (Carleton Gajdusek and Michael Alpers in Papua New Guinea on 19 February 1966 alongside Tikvah Alper in London on 20 May 1967 irradiating scrapie samples with UV light, Stanley Prusiner in San Francisco on 9 April 1982 coining 'prion' for proteinaceous infectious particles, and Charles Weissmann in Zurich on 2 July 1993 proving Prnp-knockout mice are completely immune to prions — handoff to 069 Prions, Scrapie, Kuru & Mad Cow Disease).",
             STYLE + "Split period scene: on the left in 1967 London, radiobiologist Tikvah Alper tests scrapie brain extract under an ultraviolet lamp alongside Carleton Gajdusek; on the right in April 1982 San Francisco and July 1993 Zurich, Stanley Prusiner and Charles Weissmann point to a misfolded PrPSc protein converting normal alpha-helical proteins like a chain of falling dominoes." + QUAL_TAIL,
             {"kind": "WHEN", "label": "19 FEBRUARY 1966 · 20 MAY 1967 · 9 APRIL 1982 · 2 JULY 1993", "hold_s": 3.5}),
            ("04_table_three_callback", 173.0, 2.4, "C", False, None, "reuse",
             "Reuse: verified unused moving window [5.50s..7.90s] of P1:07_table_three_props_1961_calico_slide_1964_histone_spool_and_2003_methyl_vitamin_bottle (callback, £0).",
             "Reuse P1:07_table_three_props_1961_calico_slide_1964_histone_spool_and_2003_methyl_vitamin_bottle [5.50s..7.90s] (2.40s distinct non-overlapping tail window from 8.00s source clip).",
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
                row["reuse_of"] = "P1:07_table_three_props_1961_calico_slide_1964_histone_spool_and_2003_methyl_vitamin_bottle"
                row["reuse_window_s"] = [5.5, 7.9]
                row["reuse_audit"] = {
                    "source_row": "P1:07_table_three_props_1961_calico_slide_1964_histone_spool_and_2003_methyl_vitamin_bottle",
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
            "film": "068_Lyon-Allfrey-Holliday-Jirtle-Esteller-Epigenetics-Twins",
            "part": p_idx,
            "title": p_title,
            "version": "v01",
            "timing_status": "pre_vo_script_clock (built from epigenetics_script_master_v01.md; retimes onto Scribe STT once VO locks)",
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
        "film": "068_Lyon-Allfrey-Holliday-Jirtle-Esteller-Epigenetics-Twins",
        "version": "v01",
        "date": "2026-10-19",
        "owner": "gemini (J0676)",
        "status": "PRE_VO_BOARDS_V01_NO_MINT",
        "generation_authorized": False,
        "script": "00_Brand/Channel-Setup/ideas/068_Lyon-Allfrey-Holliday-Jirtle-Esteller-Epigenetics-Twins/epigenetics_script_master_v01.md",
        "sources": "00_Brand/Channel-Setup/ideas/068_Lyon-Allfrey-Holliday-Jirtle-Esteller-Epigenetics-Twins/SOURCES_v01.md",
        "credit_snapshot": {
            "flow_balance": 23740,
            "flow_floor": 0,
            "flow_read_at": "2026-10-15T21:42:22Z",
            "vertex_promo_gbp": 71.02,
            "vertex_usable_gbp": 70.02,
        },
        "totals": totals,
        "per_part": per_part_summary,
        "mint_order": "006 > 007 > 008 > 009 > 010 > 011 > 012 > 013 > 014 > 015 > 016 > 017 > 018 > 019 > 020 > 021 > 022 > 023 > 024 > 025 > 026 > 027 > 028 > 029 > 030 > 031 > 032 > 033 > 034 > 035 > 036 > 037 > 038 > 039 > 040 > 041 > 042 > 043 > 044 > 045 > 046 > 047 > 048 > 049 > 050 > 051 > 052 > 053 > 054 > 055 > 056 > 057 > 058 > 059 > 060 > 061 > 062 > 063 > 064 > 065 > 066 > 067 > 068 > 069 > 070 > 071. Nothing in 068 is generation_authorized.",
    }
    (EDIT / "PICTURE_PLAN_v01.json").write_text(json.dumps(plan, indent=2) + "\n")

    sl = [
        "# 068 Epigenetics: Why Identical Twins Grow Up Different — Shot list & plate boards v01 (pre-VO)",
        "",
        "Gemini, 19 Oct 2026, J0676. Built from `epigenetics_script_master_v01.md` (`91.8 PASS`) and `SOURCES_v01.md`.",
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
        "# 068 price review v01 (pre-VO plate boards)",
        "",
        "Gemini, 19 Oct 2026, J0676. Boards only. **No mint. No spend. No merge.**",
        "Prepared from `epigenetics_script_master_v01.md` (`91.8 PASS`) and `SOURCES_v01.md` so 068's full plate board rows, non-emissive Fast prompts, £0 code graphics, and Teach-on-Screen overlays are ready to re-time the moment long VO locks. Parked for Chief.",
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
        f"- **Quality ({totals['Quality']} rows):** readable faces (Mary F. Lyon, Conrad Hal Waddington, Murray L. Barr, Vincent G. Allfrey, Robin Holliday, Arthur D. Riggs, Robert A. Waterland, Randy L. Jirtle, Manel Esteller, Tikvah Alper, Carleton Gajdusek, Stanley B. Prusiner, Charles Weissmann), 22 April 1961 Harwell calico-patch `X-chromosome inactivation` (`Lyonization`), May 1964 New York histone acetylation & January 1975 `CpG` DNA methylation memory, August 2003 Duke yellow-to-brown `Agouti` mouse vitamin study & 26 July 2005 Madrid `80-twin-pair` epigenome study, and the 2 Explorer beats.",
        f"- **Fast ({totals['Fast']} rows, non-emissive):** daylight prop and laboratory shots (annotated symphony score, wooden histone spool & 1961 *Nature* offprint pan, 3-object callback bench, stained female Barr-body microscope slide & carved Waddington valley relief model, open X chromosome beside compacted Barr-body sphere model, 8-part wooden nucleosome beads-on-a-string model & 1975 *Science* paper, wooden DNA replication Y-fork with symmetric red `CpG` pins, methyl-donor vitamin vials & twin chromosome methylation chart, clean-slate histone spool & sculpted alpha-helix vs beta-sheet prion models on museum plinth). Zero candles, flames, sparks, or glowing elements on Fast.",
        f"- **£0 code graphics ({totals['code_graphic']} rows):**",
        "  1. `P1:04_lyon_1961_allfrey_1964_holliday_riggs_1975_jirtle_2003_esteller_2005_epigenome_drift_chart` — histone tail acetylation (`gene ON`) vs `CpG` cytosine methylation (`5mC`, `gene OFF`) + Fraga & Esteller (26 July 2005 *PNAS*) `80-twin-pair` comparison (`4×` greater gene-expression divergence in 50-year-old vs 3-year-old identical twins) (`SCALE: if your DNA sequence is the printed musical score of a symphony, epigenetic methyl and acetyl tags are the conductor's pencil marks — telling each cell which instruments to play loud and which to silence completely`)",
        "  2. `P1:06_mary_lyon_22_apr_1961_nature_x_inactivation_calico_mosaic_chart` — Mary Lyon (22 April 1961 *Nature*) random embryonic `X-chromosome inactivation` (`50%` paternal / `50%` maternal Barr body) producing clonal orange-and-black mosaic patches in female `XX` calico cats (`SCALE: a female calico cat is a walking map of epigenetic switches — every orange patch on her coat is a family of skin cells that switched off the black X chromosome, and every black patch switched off the orange X chromosome`)",
        "  3. `P2:02_waddington_1942_barr_1949_and_lyon_22_apr_1961_nature_clonal_x_inactivation_chart` — Waddington (1942 epigenetic landscape), Barr & Bertram (30 April 1949 *Nature* Barr body), and Lyon (22 April 1961 *Nature*) random X silencing + `100%` clonal mitotic memory chart (`SCALE: silencing an entire X chromosome inside a female cell is like vacuum-packing one of two identical instruction manuals into a locked vault — and every time that cell divides, the photocopy machine faithfully locks the exact same manual away in the new cell`)",
        "  4. `P3:02_allfrey_1964_pnas_histone_acetylation_and_holliday_riggs_1975_cpg_methylation_copy_chart` — Allfrey, Faulkner & Mirsky (May 1964 *PNAS*) histone acetylation transcription chart (`2 m` DNA in `6-µm` nucleus) & Holliday/Pugh (24 January 1975 *Science*) / Riggs (1975) semi-conservative `DNMT1` `CpG` methylation copying diagram (`SCALE: copying methyl tags during cell division works like tracing carbon paper — when the two DNA strands unzip to replicate, the old strand still wears its methyl sticky notes, and a maintenance enzyme immediately stamps matching sticky notes onto the fresh copy`)",
        "  5. `P4:02_waterland_jirtle_aug_2003_agouti_methylation_and_esteller_jul_2005_pnas_80_twins_chart` — Waterland & Jirtle (August 2003 *Mol. Cell. Biol.*) `Agouti viable yellow` (`A^vy`) maternal vitamin methylation shift & Fraga/Esteller (26 July 2005 *PNAS*) `80-twin-pair` epigenetic drift plot (`SCALE: the yellow obese Agouti mouse and the lean brown mouse are genetically as identical as two prints from the same photographic negative — the only difference is a handful of microscopic methyl tags that switched the runaway gene off`)",
        "  6. `P5:01_timeline_1942_2005_and_embryonic_epigenetic_reprogramming_reset_chart` — completed timeline (1942 → 2005) + embryonic germline reprogramming curve (`~95%` methylation reset to age zero) (`SCALE: from a patchwork calico cat in Oxfordshire to eighty pairs of identical twins in Madrid, epigenetics revealed that your DNA writes the alphabet of life, but chemical switches write the story`)",
        f"- **£0 verified reuse ({totals['reuse']} row):** `P5:04_table_three_callback` uses the 2.40 s unused moving tail `[5.50s..7.90s]` of `P1:07_table_three_props_1961_calico_slide_1964_histone_spool_and_2003_methyl_vitamin_bottle`.",
        "",
        "## Mint order",
        "",
        "006 > 007 > 008 > 009 > 010 > 011 > 012 > 013 > 014 > 015 > 016 > 017 > 018 > 019 > 020 > 021 > 022 > 023 > 024 > 025 > 026 > 027 > 028 > 029 > 030 > 031 > 032 > 033 > 034 > 035 > 036 > 037 > 038 > 039 > 040 > 041 > 042 > 043 > 044 > 045 > 046 > 047 > 048 > 049 > 050 > 051 > 052 > 053 > 054 > 055 > 056 > 057 > 058 > 059 > 060 > 061 > 062 > 063 > 064 > 065 > 066 > 067 > 068 > 069 > 070 > 071. `generation_authorized` is `false` on every row.",
    ])
    (EDIT / "PRICE_REVIEW_v01.md").write_text("\n".join(pr_lines) + "\n")
    print(f"068 v01 boards written: {totals['rows']} rows, Flow expected={totals['flow_credits_expected']}")


if __name__ == "__main__":
    main()
