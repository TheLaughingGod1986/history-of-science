#!/usr/bin/env python3
"""HOS 065 (The Immune System: How Your DNA Builds a Billion Locks) pre-VO plate boards v01. J0661. No mint, no spend.

Built from 00_Brand/Channel-Setup/ideas/065_Metchnikoff-Behring-Burnet-Tonegawa-Immune-System-Antibodies/immune_script_master_v01.md
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
        "Part 01 — The Rose Thorn in a Starfish & the Genetic Slot Machine Inside Your Blood",
        [
            ("01_lymph_node_b_cells_y_shaped_antibody_locks_and_vdj_dna_slot_machine_reels", 0.0, 5.5, "A", False, "10 BILLION ANTIBODY LOCKS", "Quality",
             "Quality: Short frame 0 / answer image (0:03) + inside a human lymph node, millions of B-cells each display a unique Y-shaped antibody lock on their surface until a spiked virus hits the one matching B-cell, zooming inside its nucleus where modular V, D, and J gene segments click and shuffle together like a three-reel slot machine.",
             STYLE + "Split cellular-and-molecular scene: on the left, inside a lymph node, a spiked viral particle clicks into the one matching Y-shaped antibody receptor on a B-cell; on the right, inside the cell nucleus, three mechanical DNA reels of red V, gold D, and blue J blocks spin and lock together into a custom antibody gene." + QUAL_TAIL,
             {"kind": "WHEN", "label": "MESSINA, DECEMBER 1882", "timeline_step": "1/3 · Dec 1882 & 4 Dec 1890 (Élie Metchnikoff discovers phagocytes with a rose thorn in a starfish larva; Emil von Behring & Shibasaburo Kitasato discover serum antitoxin antibodies)", "hold_s": 3.5}),
            ("02_metchnikoff_1882_behring_kitasato_1890_burnet_1957_and_tonegawa_1976_split", 5.5, 6.0, "B", False, "PHAGOCYTES, CLONAL SELECTION, DNA SHUFFLING", "Quality",
             "Quality: complex three-part composition (Élie Metchnikoff in Messina, Sicily in December 1882 peering at a rose thorn inside a transparent starfish larva alongside Emil von Behring and Shibasaburo Kitasato in Berlin in December 1890; Frank Macfarlane Burnet in Melbourne in October 1957 sketching Clonal Selection; and Susumu Tonegawa in Basel in October 1976 mapping V(D)J DNA rearrangement).",
             STYLE + "Three-panel period composition: on the left, Élie Metchnikoff in 1882 Sicily at a brass microscope beside a tangerine tree and Emil von Behring with Shibasaburo Kitasato in 1890 Berlin holding serum vials; in the centre, Frank Macfarlane Burnet in 1957 Melbourne sketching a branching B-cell clone tree; on the right, Susumu Tonegawa in 1976 Basel inspecting restriction-enzyme DNA gel bands." + QUAL_TAIL,
             None),
            ("03_y_shaped_igg_antibody_locking_onto_spiked_virus_and_synthetic_hapten_chemical", 11.5, 6.0, "C", False, "A LOCK FOR EVERY POSSIBLE INVADER", "Quality",
             "Quality: complex conceptual and molecular reveal (a Y-shaped IgG antibody molecule snaps with atomic precision onto a spiked viral protein on one side and a freshly synthesized artificial laboratory chemical on the other).",
             STYLE + "Split molecular scene: on the left, a sculpted golden Y-shaped antibody molecule clamps its variable tips onto the surface spikes of a virus; on the right, an identical Y-shaped antibody frame with different variable tips locks precisely onto a geometric synthetic chemical flask molecule." + QUAL_TAIL,
             {"kind": "WHEN", "label": "DECEMBER 1882 · 4 DECEMBER 1890 · OCTOBER 1957 · OCTOBER 1976", "timeline_step": "1/3 · 1882 & 1890 (Metchnikoff; Behring & Kitasato) · 2/3 · Oct 1957 & May 1958 (Burnet; Nossal & Lederberg) · 3/3 · Oct 1976 (Tonegawa & Hozumi)", "hold_s": 3.5}),
            ("04_metchnikoff_1882_behring_1890_burnet_1957_tonegawa_1976_20000_genes_vs_10b_antibodies_chart", 17.5, 8.0, "E", False, "20,000 HUMAN GENES VS >10^10 (10 BILLION) ANTIBODY LOCKS VIA TONEGAWA OCT 1976 SOMATIC V(D)J RECOMBINATION (40 V × 23 D × 6 J + JUNCTIONAL DIVERSITY)", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked antibody repertoire & V(D)J somatic recombination chart from Metchnikoff (1884 Virchows Arch. 96: 177–195), Behring & Kitasato (4 December 1890 Dtsch. Med. Wochenschr. 16: 1113–1114), Burnet (October 1957 Aust. J. Sci. 20: 67–69), and Hozumi & Tonegawa (October 1976 PNAS 73: 3628–3632) compares the ~20,000 total genes in the human genome against the >10^10 (10 billion) distinct antibody and T-cell receptor specificities generated by combinatorial V-D-J gene segment splicing plus junctional diversity.",
             {"kind": "DATA", "label": "20,000 HUMAN GENES → >10,000,000,000 (10^10) UNIQUE ANTIBODIES VIA V(D)J DNA SPLICING (40 V × 23 D × 6 J + JUNCTIONS)", "detail": "Inked human genome vs antibody diversity chart on period paper comparing ~20,000 total human protein-coding genes against >10,000,000,000 (10^10) unique B-cell antibody locks created by shuffling ~40 V, 23 D, and 6 J heavy-chain gene segments with light-chain V-J segments and random junctional nucleotides", "scale": "if every one of your twenty thousand human genes were a single book, your immune system couldn't fill a small town library — yet by cutting and shuffling sentences from just a few dozen pages like a slot machine, your white blood cells print ten billion different security passcodes", "who_card": "Élie Metchnikoff (1845–1916) — Russian zoologist and immunologist · Emil von Behring (1854–1917) — German physician and bacteriologist · Shibasaburo Kitasato (1853–1931) — Japanese physician and bacteriologist · Frank Macfarlane Burnet (1899–1985) — Australian virologist and immunologist · Susumu Tonegawa (born 1939) — Japanese molecular biologist · Nobumichi Hozumi (born 1942) — Japanese immunologist", "when_stamp": "December 1882 · 4 December 1890 · October 1957 · October 1976", "hold_s": 3.8}),
            ("05_brass_microscope_rose_thorn_diphtheria_serum_vial_and_y_antibody_model_pan", 25.5, 5.5, "A", False, "20,000 GENES · 10 BILLION LOCKS", "Fast",
             "Fast: daylight macro pan across an 1882 brass monocular microscope, a rose stem with thorns, a stoppered glass serum vial, and a carved wooden Y-shaped antibody model on an oak bench between code graphics so two full-frame graphics never run back to back. Nothing emissive, no face.",
             STYLE + "In crisp daylight on an oak immunology bench, the camera pans smoothly across a polished brass microscope, a green rose stem with sharp thorns, a stoppered glass serum bottle, and a carved Y-shaped antibody model." + FAST_TAIL,
             None),
            ("06_burnet_1957_nossal_lederberg_1958_clonal_selection_2000_ab_per_sec_and_memory_curve_chart", 31.0, 8.0, "E", False, "2,000 ANTIBODIES PER SECOND", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period parchment, an inked Clonal Selection & Primary vs Secondary Immune Response curve (from Burnet 1957 & Nossal and Lederberg 1958 Nature 181: 1419–1420) shows a single naive B-cell binding an antigen, dividing into an army of thousands of plasma cells pumping out 2,000 antibody molecules per second, and leaving behind long-lived memory B-cells that launch a 100-fold faster, stronger secondary response on re-exposure.",
             {"kind": "DATA", "label": "CLONAL SELECTION (BURNET 1957): 1 MATCHING B-CELL → PLASMA ARMY (2,000 ANTIBODIES/S) + MEMORY CELLS (100× SECONDARY SURGE)", "detail": "Inked clonal selection & antibody titre curve showing a 5–10 day primary lag phase as 1 matching B-cell divides into thousands of plasma cells (~2,000 antibodies/cell/second) and memory B-cells that trigger an immediate, 100-fold higher IgG surge upon second exposure", "scale": "once the right B-cell meets its matching virus, it clones itself into an army of factories where each single cell fires out two thousand Y-shaped antibody missiles every single second", "hold_s": 3.8}),
            ("07_table_three_props_1882_starfish_slide_1890_antitoxin_vial_and_1976_vdj_blocks", 39.0, 5.5, "C", False, "1882 TO 1976", "Fast",
             "Fast: daylight prop table (callback source for Part 05: Élie Metchnikoff's 1882 glass microscope slide with a rose thorn, Behring & Kitasato's 1890 diphtheria antitoxin serum bottle, and Tonegawa's 1976 modular V-D-J wooden gene blocks). Nothing emissive.",
             STYLE + "On an oak workbench in soft window light sit three objects side by side: a glass microscope slide holding a tiny rose thorn, an amber glass bottle of diphtheria antitoxin serum, and three interlocking red, gold, and blue wooden V-D-J gene blocks." + FAST_TAIL,
             None),
            ("08_explorer_pulling_vdj_slot_machine_lever_to_build_custom_y_shaped_antibody_key", 62.0, 5.5, "A", True, None, "Quality",
             "Quality: Explorer beat 1 (locked character reference, after 1:00).",
             STYLE + "Standing inside a B-cell nucleus in front of a three-reel mechanical slot machine of red V, gold D, and blue J blocks, the Explorer pulls the brass lever to lock three blocks together and lifts out a freshly assembled Y-shaped antibody key." + EXP_TAIL,
             None),
            ("09_metchnikoff_dec_1882_messina_peering_at_starfish_larva_rose_thorn_phagocytes", 67.5, 5.5, "B", False, "MESSINA, DECEMBER 1882", "Quality",
             "Quality: readable face (in Messina, Sicily in December 1882, Élie Metchnikoff peers through his brass microscope at a transparent starfish bipinnaria larva surrounding a tiny rose thorn with mobile ameboid cells).",
             STYLE + "In a sunlit Sicilian study in December 1882 beside a small potted tangerine tree, bearded Russian zoologist Élie Metchnikoff peers intently through a brass microscope at a glass slide holding a transparent starfish larva and a tiny rose thorn." + QUAL_TAIL,
             {"kind": "WHEN", "label": "MESSINA, DECEMBER 1882", "timeline_step": "1/3 · Dec 1882 (Élie Metchnikoff discovers phagocytes with a rose thorn in a starfish larva in Messina, Sicily)", "hold_s": 3.5}),
        ],
    ),
    (
        2,
        "Part 02 — December 1882 & 4 December 1890: Metchnikoff's Starfish Rose Thorn (Phagocytes) vs Behring, Kitasato & Ehrlich's Blood Antibodies",
        [
            ("01_metchnikoff_1882_messina_phagocytes_and_behring_kitasato_1890_ehrlich_1900_antibodies", 73.0, 6.5, "A", False, "SOLDIER CELLS VS LIQUID ANTIBODIES", "Quality",
             "Quality: readable faces (Élie Metchnikoff in Messina in December 1882 watching mobile phagocytes swarm a rose thorn in a starfish larva, dissolving to Emil von Behring and Shibasaburo Kitasato in Berlin on 4 December 1890 demonstrating cell-free diphtheria antitoxin serum and Paul Ehrlich in 1900 sketching side-chain antibody receptors).",
             STYLE + "Split period scene: on the left in December 1882 Messina, Élie Metchnikoff sketches ameboid phagocytes swarming a rose thorn; on the right in Berlin, Emil von Behring and Shibasaburo Kitasato hold up clear diphtheria antitoxin serum while Paul Ehrlich draws lock-and-key side-chain receptors on a chalkboard." + QUAL_TAIL,
             {"kind": "FACT", "label": "Soldier cells vs liquid antibodies", "who_card": "Paul Ehrlich (1854–1915) — German physician and scientist", "when_stamp": "December 1882 · 1884 · 4 December 1890 · 1900 · 1908 · 1917", "timeline_step": "1/3 · Dec 1882, 4 Dec 1890 & 1900 (Metchnikoff's phagocytes + Behring, Kitasato & Ehrlich's humoral antibodies; 1901 & 1908 Nobel Prizes)", "hold_s": 3.8}),
            ("02_metchnikoff_1884_behring_kitasato_1890_ehrlich_1900_innate_phagocytes_vs_antibodies_chart", 79.5, 8.0, "E", False, "DEC 1882 METCHNIKOFF (INNATE PHAGOCYTES, MINUTES–HOURS) VS 4 DEC 1890 BEHRING & KITASATO / 1900 EHRLICH (ADAPTIVE SERUM ANTIBODIES, DAYS–LIFELONG)", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked Metchnikoff cellular phagocytosis (1882–1884) vs Behring & Kitasato humoral antitoxin serum protection (4 December 1890) & Ehrlich side-chain lock-and-key chart compares fast, non-specific innate phagocytes (hours) against specific adaptive serum antibodies (days to weeks, conferring lifelong immunity).",
             {"kind": "DATA", "label": "1882 METCHNIKOFF INNATE PHAGOCYTES (FAST, NON-SPECIFIC) + 1890 BEHRING/KITASATO & 1900 EHRLICH ANTIBODIES (LOCK-AND-KEY)", "detail": "Inked Metchnikoff cellular phagocytosis (1882–1884) vs Behring & Kitasato humoral antitoxin serum protection (4 December 1890) & Ehrlich side-chain lock-and-key chart on period paper comparing fast, non-specific innate phagocytes (hours) against specific adaptive serum antibodies (days to weeks, conferring lifelong immunity)", "scale": "your immune system fights with two armies at once — front-line phagocyte cells that swallow any stranger on sight within minutes, and custom-built antibody missiles that lock onto one exact target with pinpoint precision", "hold_s": 3.8}),
            ("03_messina_1882_brass_microscope_starfish_rose_thorn_drawing_and_serum_bottles_closeup", 87.5, 6.5, "B", False, "4 DECEMBER 1890 — ANTITOXIN ANTIBODIES", "Fast",
             "Fast: daylight macro shot of an 1884 lithographed drawing of phagocytes swarming a rose thorn beside amber glass bottles of 1890 diphtheria antitoxin serum on a wooden desk. Nothing emissive, no face.",
             STYLE + "In crisp daylight on a 19th-century laboratory desk, a detailed ink drawing of ameboid cells surrounding a rose thorn rests beside a brass microscope and stoppered glass bottles of antitoxin serum." + FAST_TAIL,
             None),
            ("04_ehrlich_1900_lock_and_key_side_chain_wooden_receptor_puzzle_models_pan", 94.0, 5.5, "C", False, "1900 — EHRLICH'S LOCK-AND-KEY RECEPTORS", "Fast",
             "Fast: daylight close-up pan across carved wooden lock-and-key receptor blocks matching Paul Ehrlich's 1900 side-chain diagrams on an oak table. Nothing emissive, no face.",
             STYLE + "In bright window light on an oak bench, carved wooden lock-and-key receptor blocks sit beside an open 1900 medical monograph showing geometric side-chain diagrams." + FAST_TAIL,
             None),
        ],
    ),
    (
        3,
        "Part 03 — October 1957 & May 1958: Linus Pauling's Wrong Guess & Frank Macfarlane Burnet's Clonal Selection Twist — Midpoint Twist",
        [
            ("01_macfarlane_burnet_oct_1957_melbourne_and_nossal_lederberg_may_1958_456_single_cells", 99.5, 6.5, "A", False, "ONE CELL, ONE PRE-MADE ANTIBODY", "Quality",
             "Quality: readable faces (Australian virologist Frank Macfarlane Burnet in Melbourne in October 1957 proposing the Clonal Selection Theory against Linus Pauling's 1940 folding-clay template model, alongside Gustav Nossal and Joshua Lederberg in May 1958 isolating 456 single B-cells in microdroplets to prove one cell makes only one antibody).",
             STYLE + "Split period scene: on the left in October 1957 Melbourne, Frank Macfarlane Burnet points to a diagram of pre-existing B-cell clones each wearing one lock; on the right in May 1958, Gustav Nossal and Joshua Lederberg peer through a microscope at single B-cells suspended in tiny oil microdroplets." + QUAL_TAIL,
             {"kind": "FACT", "label": "One cell, one pre-made antibody", "who_card": "Gustav J. V. Nossal (born 1931) — Australian immunologist · Joshua Lederberg (1925–2008) — American molecular biologist", "when_stamp": "1940 · 1955 · October 1957 · May 1958", "timeline_step": "2/3 · Oct 1957 & May 1958 (Frank Macfarlane Burnet proposes Clonal Selection Theory; Gustav Nossal & Joshua Lederberg prove one B-cell makes one antibody in 456 single cells)", "hold_s": 3.8}),
            ("02_burnet_oct_1957_and_nossal_lederberg_may_1958_456_single_cell_monospecificity_chart", 106.0, 8.0, "E", False, "OCT 1957 BURNET (AUST. J. SCI.) & 17 MAY 1958 NOSSAL & LEDERBERG (NATURE 181: 1419–1420): 456 SINGLE B-CELL MICRODROPLETS → 0 CELLS MAKE BOTH ANTIBODIES (100% ONE CELL, ONE ANTIBODY)", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked Burnet (October 1957, Aust. J. Sci. 20: 67–69) and Nossal & Lederberg (17 May 1958, Nature 181: 1419–1420) single-cell microdroplet antibody chart compares Pauling's 1940 instructional model (predicting individual cells make both anti-Salmonella antibodies) vs Nossal & Lederberg's 456 single-cell microdroplets (100% monospecific: each active B-cell produces only one antibody specificity).",
             {"kind": "DATA", "label": "OCT 1957 BURNET CLONAL SELECTION & MAY 1958 NOSSAL-LEDERBERG: 456 SINGLE B-CELLS → 0 DOUBLE PRODUCERS (1 CELL = 1 LOCK)", "detail": "Inked Burnet (October 1957, Aust. J. Sci. 20: 67–69) and Nossal & Lederberg (17 May 1958, Nature 181: 1419–1420) single-cell microdroplet antibody chart on period paper comparing Pauling's 1940 instructional model (predicting individual cells make both anti-Salmonella antibodies) vs Nossal & Lederberg's 456 single-cell microdroplets (100% monospecific: each active B-cell produces only one antibody specificity)", "scale": "instead of waiting for a burglar to show up and moulding a lock around his key, your body pre-builds a hundred million different locks before you are even born and waits to see which door the burglar tries", "hold_s": 3.8}),
            ("03_melbourne_1958_microdroplet_oil_chamber_slide_and_micromanipulator_pipette_closeup", 114.0, 6.5, "B", False, "OCTOBER 1957 — CLONAL SELECTION", "Fast",
             "Fast: daylight macro shot of a glass microdroplet oil chamber slide beside a brass micromanipulator pipette and the October 1957 Australian Journal of Science offprint on a bench. Nothing emissive, no face.",
             STYLE + "In crisp daylight on a 1958 Melbourne laboratory bench, a glass microdroplet chamber slide sits under a brass micromanipulator pipette beside a printed 1957 scientific journal." + FAST_TAIL,
             None),
            ("04_rack_of_numbered_pre_cut_brass_padlocks_and_single_matching_key_pan", 120.5, 5.5, "C", False, "PRE-BUILT BEFORE ANY GERM ARRIVES", "Fast",
             "Fast: daylight close-up pan across a wooden rack of dozens of differently shaped brass padlocks where a single key fits padlock #84 on an oak table. Nothing emissive, no face.",
             STYLE + "In bright window light on an oak table, a wooden display rack holds rows of uniquely shaped brass padlocks with a single brass key slotted into the one matching lock." + FAST_TAIL,
             None),
        ],
    ),
    (
        4,
        "Part 04 — October 1976: Susumu Tonegawa's Genetic Slot Machine (V(D)J Recombination)",
        [
            ("01_susumu_tonegawa_and_nobumichi_hozumi_oct_1976_basel_vdj_dna_recombination", 126.0, 6.5, "A", False, "IMMUNE CELLS SHUFFLE THEIR OWN DNA", "Quality",
             "Quality: readable faces (37-year-old Japanese molecular biologist Susumu Tonegawa and postdoctoral fellow Nobumichi Hozumi at the Basel Institute for Immunology in October 1976 comparing embryo DNA and adult B-cell DNA with restriction enzymes to prove somatic V(D)J recombination).",
             STYLE + "Split period scene: on the left at the Basel Institute for Immunology in October 1976, Susumu Tonegawa and Nobumichi Hozumi examine restriction-enzyme DNA hybridization plots; on the right, a chromosome diagram shows widely separated embryonic V, D, and J gene segments being cut and spliced together in an adult B-cell." + QUAL_TAIL,
             {"kind": "FACT", "label": "Immune cells shuffle their own DNA", "when_stamp": "1965 · October 1976 · 1987", "timeline_step": "3/3 · Oct 1976 (Susumu Tonegawa & Nobumichi Hozumi in Basel prove somatic V(D)J DNA recombination generates >10 billion antibodies from modular gene segments, winning the 1987 Nobel Prize)", "hold_s": 3.8}),
            ("02_hozumi_tonegawa_oct_1976_pnas_germline_vs_rearranged_b_cell_vdj_combinatorial_chart", 132.5, 8.0, "E", False, "OCT 1976 HOZUMI & TONEGAWA (PNAS 73: 3628–3632): EMBRYO SEPARATED V–C DNA FRAGMENTS VS SPLICED B-CELL V(D)J GENE (40 V × 23 D × 6 J × LIGHT CHAIN × JUNCTIONS > 10^10)", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked Hozumi & Tonegawa (October 1976, PNAS 73: 3628–3632) somatic V(D)J recombination chart shows embryonic germline DNA (widely separated V, D, J, and C gene segments on different restriction fragments) vs rearranged adult B-cell DNA (1 V + 1 D + 1 J spliced together next to C), multiplying ~40 VH x 23 DH x 6 JH x light-chain Vk/l-Jk/l x junctional additions into >10^10 unique antibodies.",
             {"kind": "DATA", "label": "OCT 1976 TONEGAWA & HOZUMI (PNAS): SOMATIC V(D)J RECOMBINATION SPLICES 40 V × 23 D × 6 J SEGMENTS INTO >10^10 ANTIBODIES", "detail": "Inked Hozumi & Tonegawa (October 1976, PNAS 73: 3628–3632) somatic V(D)J recombination chart on period paper showing embryonic germline DNA (widely separated V, D, J, and C gene segments on different restriction fragments) vs rearranged adult B-cell DNA (1 V + 1 D + 1 J spliced together next to C), multiplying ~40 VH × 23 DH × 6 JH × light-chain Vκ/λ-Jκ/λ × junctional additions into >10^10 unique antibodies", "scale": "with just three modularity reels — V, D, and J — plus random letters inserted at the joints, your DNA works like a combination lock where a few dozen dials can dial up ten billion different numbers", "hold_s": 3.8}),
            ("03_basel_1976_dna_restriction_fragment_gel_and_modular_vdj_blocks_closeup", 140.5, 6.5, "B", False, "OCTOBER 1976 — SOMATIC V(D)J RECOMBINATION", "Fast",
             "Fast: daylight macro shot of a 1976 restriction-enzyme electrophoresis gel autoradiograph print beside modular red V, gold D, and blue J gene blocks on a Basel workbench. Nothing emissive, no face.",
             STYLE + "In crisp daylight on a 1976 molecular biology bench, a plotted DNA restriction-fragment graph sits beside interlocking red, gold, and blue wooden V-D-J gene blocks." + FAST_TAIL,
             None),
            ("04_explorer_dialing_three_reel_vdj_combination_lock_to_10_billion_on_y_antibody_vault", 147.0, 5.5, "B", True, None, "Quality",
             "Quality: Explorer beat 2 (locked character reference).",
             STYLE + "Standing beside a large brass three-dial V-D-J combination lock mounted on a sculpted Y-shaped antibody gate, the Explorer spins the three numbered dials into alignment as the mechanical counter above clicks to ten billion." + EXP_TAIL,
             None),
        ],
    ),
    (
        5,
        "Part 05 — Why You Can Still Catch a Cold Twice — & How Scientists Discovered Cancer Hides Inside Our Own Genes",
        [
            ("01_timeline_1882_1976_and_antigenic_drift_mutating_virus_coat_chart", 152.5, 8.5, "E", False, "1882–1976 TIMELINE · METCHNIKOFF PHAGOCYTES, BEHRING/KITASATO ANTIBODIES, BURNET CLONAL SELECTION, TONEGAWA V(D)J & VIRAL ANTIGENIC DRIFT", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, the 3-era timeline completes: Dec 1882 & 4 Dec 1890 (Élie Metchnikoff discovers phagocytes with a rose thorn in a starfish larva; Emil von Behring & Shibasaburo Kitasato discover serum antitoxin antibodies, with Paul Ehrlich proposing lock-and-key receptors in 1900) · Oct 1957 & May 1958 (Frank Macfarlane Burnet proposes Clonal Selection Theory; Gustav Nossal & Joshua Lederberg prove one B-cell makes one antibody) · Oct 1976 (Susumu Tonegawa & Nobumichi Hozumi in Basel prove somatic V(D)J DNA recombination generates >10 billion antibodies from modular gene segments, winning the 1987 Nobel Prize).",
             {"kind": "DATA", "label": "1882–1976 IMMUNE SYSTEM TIMELINE · MEASLES STABLE COAT (LIFELONG IMMUNITY) VS FLU/COLD RNA ANTIGENIC DRIFT", "detail": "Animated timeline (1882 → 1976) alongside the stable measles surface antigen vs mutating influenza/rhinovirus antigenic drift diagram", "scale": "from a Christmas rose thorn in a Sicilian starfish to a genetic slot machine in Switzerland, a century of discovery explained how twenty thousand human genes guard you against a universe of unseen invaders", "when_stamp": "1882–1976", "timeline_step": "3/3 · 1882–1976 timeline complete", "hold_s": 3.8}),
            ("02_y_shaped_antibody_key_and_disguised_mutated_viral_spike_models_on_plinth_pan", 161.0, 5.5, "A", False, "WHY FLU & COLD VIRUSES ESCAPE OLD ANTIBODIES", "Fast",
             "Fast: daylight close-up of a brass Y-shaped antibody lock fitting a 1975 viral spike model beside a mutated 1976 viral spike model on a wooden museum plinth. Nothing emissive, no face.",
             STYLE + "In crisp daylight on a wooden museum plinth, a polished brass Y-shaped antibody model fits cleanly onto one sculpted viral spike while a second mutated viral spike beside it wears a changed geometric shape." + FAST_TAIL,
             None),
            ("03_peyton_rous_1911_knudson_1971_bishop_varmus_1976_src_and_lane_levine_old_1979_p53_handoff", 166.5, 6.5, "C", False, "ONCOGENES, TUMOUR SUPPRESSORS & P53", "Quality",
             "Quality: readable faces (Peyton Rous on 21 January 1911 filtering a chicken sarcoma virus, J. Michael Bishop and Harold Varmus in March 1976 discovering cellular proto-oncogene c-src, and Alfred Knudson in April 1971 with David Lane, Arnold Levine, and Lloyd Old in May 1979 discovering tumour suppressors and p53 — handoff to 066 Oncogenes, Tumour Suppressors & p53).",
             STYLE + "Split period scene: on the left, Peyton Rous in 1911 New York filters chicken tumour fluid while J. Michael Bishop and Harold Varmus in 1976 San Francisco point to the c-src gene inside a normal cell; on the right, Alfred Knudson and David Lane inspect a cell division brake dial marked p53." + QUAL_TAIL,
             {"kind": "WHEN", "label": "21 JANUARY 1911 · APRIL 1971 · MARCH 1976 · MAY 1979", "hold_s": 3.5}),
            ("04_table_three_callback", 173.0, 2.4, "C", False, None, "reuse",
             "Reuse: verified unused moving window [5.50s..7.90s] of P1:07_table_three_props_1882_starfish_slide_1890_antitoxin_vial_and_1976_vdj_blocks (callback, £0).",
             "Reuse P1:07_table_three_props_1882_starfish_slide_1890_antitoxin_vial_and_1976_vdj_blocks [5.50s..7.90s] (2.40s distinct non-overlapping tail window from 8.00s source clip).",
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
                row["reuse_of"] = "P1:07_table_three_props_1882_starfish_slide_1890_antitoxin_vial_and_1976_vdj_blocks"
                row["reuse_window_s"] = [5.5, 7.9]
                row["reuse_audit"] = {
                    "source_row": "P1:07_table_three_props_1882_starfish_slide_1890_antitoxin_vial_and_1976_vdj_blocks",
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
            "film": "065_Metchnikoff-Behring-Burnet-Tonegawa-Immune-System-Antibodies",
            "part": p_idx,
            "title": p_title,
            "version": "v01",
            "timing_status": "pre_vo_script_clock (built from immune_script_master_v01.md; retimes onto Scribe STT once VO locks)",
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
        "film": "065_Metchnikoff-Behring-Burnet-Tonegawa-Immune-System-Antibodies",
        "version": "v01",
        "date": "2026-10-19",
        "owner": "gemini (J0661)",
        "status": "PRE_VO_BOARDS_V01_NO_MINT",
        "generation_authorized": False,
        "script": "00_Brand/Channel-Setup/ideas/065_Metchnikoff-Behring-Burnet-Tonegawa-Immune-System-Antibodies/immune_script_master_v01.md",
        "sources": "00_Brand/Channel-Setup/ideas/065_Metchnikoff-Behring-Burnet-Tonegawa-Immune-System-Antibodies/SOURCES_v01.md",
        "credit_snapshot": {
            "flow_balance": 23740,
            "flow_floor": 0,
            "flow_read_at": "2026-10-15T21:42:22Z",
            "vertex_promo_gbp": 71.02,
            "vertex_usable_gbp": 70.02,
        },
        "totals": totals,
        "per_part": per_part_summary,
        "mint_order": "006 > 007 > 008 > 009 > 010 > 011 > 012 > 013 > 014 > 015 > 016 > 017 > 018 > 019 > 020 > 021 > 022 > 023 > 024 > 025 > 026 > 027 > 028 > 029 > 030 > 031 > 032 > 033 > 034 > 035 > 036 > 037 > 038 > 039 > 040 > 041 > 042 > 043 > 044 > 045 > 046 > 047 > 048 > 049 > 050 > 051 > 052 > 053 > 054 > 055 > 056 > 057 > 058 > 059 > 060 > 061 > 062 > 063 > 064 > 065 > 066 > 067 > 068. Nothing in 065 is generation_authorized.",
    }
    (EDIT / "PICTURE_PLAN_v01.json").write_text(json.dumps(plan, indent=2) + "\n")

    sl = [
        "# 065 The Immune System: How Your DNA Builds a Billion Locks — Shot list & plate boards v01 (pre-VO)",
        "",
        "Gemini, 19 Oct 2026, J0661. Built from `immune_script_master_v01.md` (`91.8 PASS`) and `SOURCES_v01.md`.",
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
        "# 065 price review v01 (pre-VO plate boards)",
        "",
        "Gemini, 19 Oct 2026, J0661. Boards only. **No mint. No spend. No merge.**",
        "Prepared from `immune_script_master_v01.md` (`91.8 PASS`) and `SOURCES_v01.md` so 065's full plate board rows, non-emissive Fast prompts, £0 code graphics, and Teach-on-Screen overlays are ready to re-time the moment long VO locks. Parked for Chief.",
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
        f"- **Quality ({totals['Quality']} rows):** readable faces (Élie Metchnikoff, Emil von Behring, Shibasaburo Kitasato, Paul Ehrlich, Frank Macfarlane Burnet, Gustav J. V. Nossal, Joshua Lederberg, Susumu Tonegawa, Nobumichi Hozumi, Peyton Rous, J. Michael Bishop, Harold Varmus, Alfred Knudson, David Lane), December 1882 Messina starfish rose-thorn phagocytes & 4 December 1890 Berlin diphtheria antitoxin serum, October 1957 Melbourne Clonal Selection & May 1958 `456 single-cell` microdroplet proof, October 1976 Basel `V(D)J` somatic DNA recombination, and the 2 Explorer beats.",
        f"- **Fast ({totals['Fast']} rows, non-emissive):** daylight prop and laboratory shots (1882 brass monocular microscope, rose stem with thorns, serum vial & wooden Y-shaped antibody model pan, 3-object callback bench, 1884 lithographed rose-thorn phagocyte drawing & amber antitoxin serum bottles, Paul Ehrlich's 1900 carved wooden lock-and-key receptor models, 1958 glass microdroplet oil chamber slide & brass micromanipulator pipette, wooden rack of uniquely shaped brass padlocks & matching key, 1976 DNA restriction-fragment plot & interlocking `V-D-J` wooden blocks, brass Y-shaped antibody model & mutated viral spike on museum plinth). Zero candles, flames, sparks, or glowing elements on Fast.",
        f"- **£0 code graphics ({totals['code_graphic']} rows):**",
        "  1. `P1:04_metchnikoff_1882_behring_1890_burnet_1957_tonegawa_1976_20000_genes_vs_10b_antibodies_chart` — human genome (`~20,000` genes) vs `>10¹⁰` (`10 billion`) unique B-cell antibody locks via Tonegawa's October 1976 somatic `V(D)J` recombination (`40 V × 23 D × 6 J` + junctional diversity) (`SCALE: if every one of your twenty thousand human genes were a single book, your immune system couldn't fill a small town library — yet by cutting and shuffling sentences from just a few dozen pages like a slot machine, your white blood cells print ten billion different security passcodes`)",
        "  2. `P1:06_burnet_1957_nossal_lederberg_1958_clonal_selection_2000_ab_per_sec_and_memory_curve_chart` — Burnet (1957) & Nossal and Lederberg (1958) Clonal Selection & Primary vs Secondary (`100×`, `2,000 antibodies/s`) immune response curve (`SCALE: once the right B-cell meets its matching virus, it clones itself into an army of factories where each single cell fires out two thousand Y-shaped antibody missiles every single second`)",
        "  3. `P2:02_metchnikoff_1884_behring_kitasato_1890_ehrlich_1900_innate_phagocytes_vs_antibodies_chart` — Metchnikoff (1882–1884) cellular phagocytosis vs Behring & Kitasato (4 December 1890) and Ehrlich (1900) lock-and-key humoral antibodies chart (`SCALE: your immune system fights with two armies at once — front-line phagocyte cells that swallow any stranger on sight within minutes, and custom-built antibody missiles that lock onto one exact target with pinpoint precision`)",
        "  4. `P3:02_burnet_oct_1957_and_nossal_lederberg_may_1958_456_single_cell_monospecificity_chart` — Burnet (October 1957, *Aust. J. Sci.* 20: 67–69) and Nossal & Lederberg (17 May 1958, *Nature* 181: 1419–1420) `456 single-cell` microdroplet monospecificity chart (`0` double producers = one cell, one antibody) (`SCALE: instead of waiting for a burglar to show up and moulding a lock around his key, your body pre-builds a hundred million different locks before you are even born and waits to see which door the burglar tries`)",
        "  5. `P4:02_hozumi_tonegawa_oct_1976_pnas_germline_vs_rearranged_b_cell_vdj_combinatorial_chart` — Hozumi & Tonegawa (October 1976, *PNAS* 73: 3628–3632) embryonic germline DNA vs rearranged adult B-cell `V(D)J` restriction-fragment & combinatorial diversity chart (`SCALE: with just three modularity reels — V, D, and J — plus random letters inserted at the joints, your DNA works like a combination lock where a few dozen dials can dial up ten billion different numbers`)",
        "  6. `P5:01_timeline_1882_1976_and_antigenic_drift_mutating_virus_coat_chart` — completed timeline (1882 → 1976) + measles stable surface antigen vs mutating influenza/rhinovirus antigenic drift diagram (`SCALE: from a Christmas rose thorn in a Sicilian starfish to a genetic slot machine in Switzerland, a century of discovery explained how twenty thousand human genes guard you against a universe of unseen invaders`)",
        f"- **£0 verified reuse ({totals['reuse']} row):** `P5:04_table_three_callback` uses the 2.40 s unused moving tail `[5.50s..7.90s]` of `P1:07_table_three_props_1882_starfish_slide_1890_antitoxin_vial_and_1976_vdj_blocks`.",
        "",
        "## Mint order",
        "",
        "006 > 007 > 008 > 009 > 010 > 011 > 012 > 013 > 014 > 015 > 016 > 017 > 018 > 019 > 020 > 021 > 022 > 023 > 024 > 025 > 026 > 027 > 028 > 029 > 030 > 031 > 032 > 033 > 034 > 035 > 036 > 037 > 038 > 039 > 040 > 041 > 042 > 043 > 044 > 045 > 046 > 047 > 048 > 049 > 050 > 051 > 052 > 053 > 054 > 055 > 056 > 057 > 058 > 059 > 060 > 061 > 062 > 063 > 064 > 065 > 066 > 067 > 068. `generation_authorized` is `false` on every row.",
    ])
    (EDIT / "PRICE_REVIEW_v01.md").write_text("\n".join(pr_lines) + "\n")
    print(f"065 v01 boards written: {totals['rows']} rows, Flow expected={totals['flow_credits_expected']}")


if __name__ == "__main__":
    main()
