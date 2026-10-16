#!/usr/bin/env python3
"""HOS 069 (Prions: The Deadly Contagion With Zero DNA) pre-VO plate boards v01. J0676. No mint, no spend.

Built from 00_Brand/Channel-Setup/ideas/069_Alper-Gajdusek-Prusiner-Weissmann-Prions-Mad-Cow/prions_script_master_v01.md
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
        "Part 01 — The Radiation-Proof Mystery in London & the Domino Protein Inside Your Brain",
        [
            ("01_uv_beam_shattering_viral_dna_while_beta_sheet_prion_domino_flips_alpha_helix_prp", 0.0, 5.5, "A", False, "ZERO DNA, ZERO RNA", "Quality",
             "Quality: Short frame 0 / answer image (0:03) + an ultraviolet radiation beam shatters a viral DNA helix into fragments while beside it a flat, jagged beta-sheet prion protein (PrPSc) survives unscathed, touches a springy golden alpha-helix brain protein (PrPC), and snaps it into an identical flat beta-sheet in a chain of falling dominoes.",
             STYLE + "Split molecular scene: on the left, a violet light beam shatters a coiled viral DNA ladder into pieces while a flat metallic beta-sheet protein block stands untouched; on the right, that flat protein block touches a row of golden spiral alpha-helix springs and snaps them one after another into flat rigid sheets like falling dominoes." + QUAL_TAIL,
             {"kind": "WHEN", "label": "LONDON, MAY 1967", "timeline_step": "1/3 · 5 Sep 1959, 19 Feb 1966 & 20 May 1967 (William Hadlow links scrapie to kuru; Carleton Gajdusek & Michael Alpers prove kuru transmission; Tikvah Alper proves the scrapie agent resists UV radiation)", "hold_s": 3.5}),
            ("02_gajdusek_alpers_1966_hadlow_1959_alper_griffith_1967_and_prusiner_1982_weissmann_1993_split", 5.5, 6.0, "B", False, "KURU, RADIATION PROOF, PRION DOMINOES", "Quality",
             "Quality: complex three-part composition (Carleton Gajdusek and Michael Alpers in Papua New Guinea in February 1966 alongside William Hadlow comparing sheep scrapie and kuru brain slides; Tikvah Alper at Hammersmith Hospital in London in May 1967 blasting scrapie samples with ultraviolet radiation alongside John Stanley Griffith; and Stanley Prusiner at UCSF on 9 April 1982 purifying prion rods alongside Charles Weissmann in Zurich in July 1993 with his prion-knockout mice).",
             STYLE + "Three-panel period composition: on the left, Carleton Gajdusek, Michael Alpers, and William Hadlow in 1966 comparing spongiform microscope slides; in the centre, Tikvah Alper and John Stanley Griffith in 1967 London beside an ultraviolet irradiation chamber; on the right, Stanley Prusiner in 1982 San Francisco with ultracentrifuge tubes alongside Charles Weissmann in 1993 Zurich holding a healthy white knockout mouse." + QUAL_TAIL,
             None),
            ("03_normal_alpha_helical_prpc_on_neuron_membrane_refolded_by_prpsc_beta_sheet_template", 11.5, 6.0, "C", False, "ONE FOLD FLIPS THE NEXT", "Quality",
             "Quality: complex molecular reveal (on the membrane of a neuron, normal cellular prion protein PrPC with three springy alpha-helices meets a misfolded scrapie prion template PrPSc of flat beta-sheets, which refolds the normal coil into an indestructible beta-sheet stack).",
             STYLE + "Close-up molecular animation on a curved cell membrane: a three-coil golden spiral protein meets a rigid pleated beta-sheet block and unfolds then snaps flat into an identical pleated sheet." + QUAL_TAIL,
             {"kind": "WHEN", "label": "5 SEPTEMBER 1959 · 19 FEBRUARY 1966 · 20 MAY 1967 · 9 SEPTEMBER 1967 · 9 APRIL 1982 · 2 JULY 1993", "timeline_step": "1/3 · Sep 1959, Feb 1966 & May–Sep 1967 (Hadlow, Gajdusek, Alpers, Alper & Griffith) · 2/3 · Apr 1982 & Apr 1985 (Prusiner, Hood & Weissmann) · 3/3 · Jul 1993 (Büeler, Aguzzi & Weissmann)", "hold_s": 3.5}),
            ("04_alper_1967_uv_survival_and_prusiner_1982_1993_prpc_to_prpsc_conversion_chart", 17.5, 8.0, "E", False, "20 MAY 1967 ALPER 254 NM UV RESISTANCE & PRUSINER 1982/1993 PRPC (43% ALPHA-HELIX) → PRPSC (43% BETA-SHEET) CONVERSION", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked Ultraviolet Inactivation & PrP Conformational Conversion chart from Alper, Cramp, Haig & Clarke (20 May 1967 Nature 214: 764–766), Griffith (9 September 1967 Nature 215: 1043–1044), Prusiner (9 April 1982 Science 216: 136–144), Pan et al. (1 December 1993 PNAS 90: 10962–10966), and Büeler & Weissmann et al. (2 July 1993 Cell 73: 1339–1347) plots log survival against 254 nm UV dose and compares normal PrPC (43% alpha-helix, 3% beta-sheet, protease-sensitive) against infectious PrPSc (30% alpha-helix, 43% beta-sheet, protease-resistant).",
             {"kind": "DATA", "label": "1967 ALPER 254 NM UV SURVIVAL CURVE & 1982/1993 PRUSINER PRPC (43% α-HELIX, 3% β-SHEET) → PRPSC (43% β-SHEET) CONVERSION", "detail": "Inked UV radiation survival & PrPC-to-PrPSc secondary-structure chart on period paper contrasting nucleic-acid viruses (inactivated by 254 nm UV light) with the scrapie prion agent (resistant to 254 nm UV, nucleases, and 100 °C boiling, inactivated by protein-denaturing proteases/chaotropes) as normal PrPC (43% alpha-helix, 3% beta-sheet) refolds into PrPSc (43% beta-sheet)", "scale": "a prion is not a living parasite with its own genetic blueprint — it is a single misfolded crystal seed that snaps normal springy brain proteins into flat rigid sheets on contact, like one toppling domino knocking down an entire room", "who_card": "William J. Hadlow (1921–2015) — American veterinary pathologist · D. Carleton Gajdusek (1923–2008) — American virologist and paediatrician · Michael P. Alpers (born 1934) — Australian medical researcher · Tikvah Alper (1909–1995) — South African-born radiobiologist · John Stanley Griffith (1928–1972) — British biophysicist and mathematician · Stanley B. Prusiner (born 1942) — American neurologist and biochemist · Charles Weissmann (born 1931) — Swiss molecular biologist", "when_stamp": "5 September 1959 · 19 February 1966 · 20 May 1967 · 9 September 1967 · 9 April 1982 · 2 July 1993", "hold_s": 3.8}),
            ("05_alpha_helix_spring_model_beside_flat_beta_sheet_dominoes_and_1967_nature_offprint_pan", 25.5, 5.5, "A", False, "THE DOMINO SEED", "Fast",
             "Fast: daylight macro pan across a sculpted brass alpha-helix spring model, a row of flat iron beta-sheet dominoes, and a 1967 Nature offprint on an oak bench between code graphics so two full-frame graphics never run back to back. Nothing emissive, no face.",
             STYLE + "In crisp daylight on an oak laboratory bench, the camera pans smoothly across a coiled brass alpha-helix spring model, a row of flat iron domino blocks, and an open printed 1967 journal." + FAST_TAIL,
             None),
            ("06_weissmann_2_jul_1993_cell_prnp_knockout_mouse_resistance_chart", 31.0, 8.0, "E", False, "NO DOMINOES, NO DISEASE", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period parchment, an inked Weissmann Prnp0/0 Prion-Knockout Mouse Resistance chart (from Büeler, Aguzzi, Sailer, Greiner, Autenried, Aguet & Weissmann, 2 July 1993 Cell 73: 1339–1347) compares wild-type mice (Prnp+/+, 100% developing scrapie ~158 days / ~23 weeks after intracerebral prion inoculation) against Prnp0/0 knockout mice lacking the PrPC gene (0% disease and 0 prion replication >500 days / 70+ weeks after inoculation).",
             {"kind": "DATA", "label": "2 JUL 1993 WEISSMANN (CELL): PRNP+/+ WILD-TYPE MICE SUCCUMB AT ~23 WEEKS VS PRNP0/0 KNOCKOUT MICE 100% IMMUNE PAST 500+ DAYS", "detail": "Inked Büeler & Weissmann (2 July 1993 Cell 73: 1339–1347) Prnp0/0 knockout mouse survival chart showing wild-type Prnp+/+ mice succumbing at ~23 weeks post-inoculation vs Prnp0/0 mice remaining 100% symptom-free and prion-free past 70+ weeks", "scale": "removing the normal prion gene from a mouse is like taking all the standing dominoes off the table — you can flick a diseased prion domino into the brain, but with no normal dominoes to hit, the chain reaction stops dead", "hold_s": 3.8}),
            ("07_table_three_props_1959_kuru_slide_1982_prion_ultracentrifuge_tube_and_domino_protein_model", 39.0, 5.5, "C", False, "1959 TO 1993", "Fast",
             "Fast: daylight prop table (callback source for Part 05: William Hadlow's 1959 spongiform brain microscope slide, Stanley Prusiner's 1982 ultracentrifuge tube of purified PrP 27–30, and a sculpted brass-and-iron prion domino model). Nothing emissive.",
             STYLE + "On an oak workbench in soft window light sit three objects side by side: a stained brain-tissue microscope slide, a stoppered glass ultracentrifuge tube, and a sculpted pair of coiled and flat protein domino models." + FAST_TAIL,
             None),
            ("08_explorer_lifting_golden_prpc_spring_dominoes_to_stop_iron_prpsc_chain_reaction", 62.0, 5.5, "A", True, None, "Quality",
             "Quality: Explorer beat 1 (locked character reference, after 1:00).",
             STYLE + "Standing beside a long oak table of golden spring-shaped dominoes, the Explorer watches one flat iron domino snap the first three springs flat, then lifts a group of golden springs out of the line so the falling chain stops dead in front of an empty gap." + EXP_TAIL,
             None),
            ("09_tikvah_alper_may_1967_hammersmith_hospital_examining_uv_survival_curves", 67.5, 5.5, "B", False, "LONDON, MAY 1967", "Quality",
             "Quality: readable face (at Hammersmith Hospital in London in May 1967, South African-born radiobiologist Tikvah Alper examines radiation survival curves beside her ultraviolet irradiation chamber).",
             STYLE + "In a 1967 Hammersmith Hospital radiobiology laboratory in London, Tikvah Alper holds up a plotted radiation survival chart beside a brass-and-steel ultraviolet sample chamber." + QUAL_TAIL,
             {"kind": "WHEN", "label": "LONDON, 20 MAY 1967", "timeline_step": "1/3 · 20 May 1967 (Tikvah Alper proves the scrapie agent survives 254 nm UV radiation in Nature)", "hold_s": 3.5}),
        ],
    ),
    (
        2,
        "Part 02 — 5 September 1959, 19 February 1966 & May–September 1967: Kuru, Sheep Scrapie & Tikvah Alper's Radiation-Proof Heresy",
        [
            ("01_hadlow_1959_gajdusek_alpers_1966_kuru_and_alper_20_may_1967_london_uv_beam", 73.0, 6.5, "A", False, "SURVIVES DNA-SHREDDING RADIATION", "Quality",
             "Quality: readable faces (William Hadlow on 5 September 1959 comparing sheep scrapie and human kuru brain micrographs and Carleton Gajdusek with Michael Alpers in Papua New Guinea on 19 February 1966, dissolving to Tikvah Alper in London on 20 May 1967 irradiating scrapie samples with 254 nm UV light).",
             STYLE + "Split period scene: on the left, William Hadlow, Carleton Gajdusek, and Michael Alpers compare matching sponge-like vacuoles on sheep scrapie and human kuru microscope slides; on the right in May 1967 London, Tikvah Alper tests scrapie tubes inside a shielded ultraviolet irradiation apparatus." + QUAL_TAIL,
             {"kind": "FACT", "label": "Survives DNA-shredding radiation", "when_stamp": "1936 · 1957 · 5 September 1959 · 19 February 1966 · May 1966 · 20 May 1967 · 9 September 1967", "timeline_step": "1/3 · 5 Sep 1959, 19 Feb 1966 & 20 May 1967 (Hadlow links scrapie to kuru; Gajdusek & Alpers prove kuru transmission; Alper & Griffith propose replication without DNA)", "hold_s": 3.8}),
            ("02_hadlow_1959_gajdusek_1966_and_alper_20_may_1967_nature_uv_target_inactivation_chart", 79.5, 8.0, "E", False, "5 SEP 1959 HADLOW (LANCET) · 19 FEB 1966 GAJDUSEK & ALPERS (NATURE) · 20 MAY 1967 ALPER (NATURE 214: 764–766): 254 NM UV VIRAL INACTIVATION VS SCRAPIE RESISTANCE", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked Hadlow (5 September 1959 Lancet 274: 289–290), Gajdusek, Gibbs & Alpers (19 February 1966 Nature 209: 794–796), and Alper, Cramp, Haig & Clarke (20 May 1967 Nature 214: 764–766) ionizing and 254 nm UV radiation target-size & inactivation chart shows viral nucleic-acid inactivation vs scrapie resistance.",
             {"kind": "DATA", "label": "1959 HADLOW SCRAPIE-KURU LINK, 1966 GAJDUSEK TRANSMISSION & 20 MAY 1967 ALPER 254 NM UV RESISTANCE CURVE", "detail": "Inked Hadlow (5 September 1959 Lancet 274: 289–290), Gajdusek, Gibbs & Alpers (19 February 1966 Nature 209: 794–796), and Alper, Cramp, Haig & Clarke (20 May 1967 Nature 214: 764–766) ionizing/254 nm UV radiation target-size & inactivation chart on period paper showing viral nucleic-acid inactivation vs scrapie resistance", "scale": "blasting the scrapie agent with ultraviolet light that shreds DNA and RNA is like firing cannonballs at a ghost — every virus in the dish is blown apart, while the DNA-free scrapie particle walks straight through untouched", "hold_s": 3.8}),
            ("03_hammersmith_1967_uv_cuvette_rack_and_griffith_protein_dimer_notebook_closeup", 87.5, 6.5, "B", False, "20 MAY 1967 — REPLICATION WITHOUT DNA", "Fast",
             "Fast: daylight macro shot of quartz irradiation cuvettes in a brass rack beside John Stanley Griffith's September 1967 Nature protein-folding notebook diagrams on a bench. Nothing emissive, no face.",
             STYLE + "In crisp daylight on a 1967 London laboratory desk, a brass rack of quartz sample tubes sits beside an open notebook showing sketched protein subunit pairing diagrams." + FAST_TAIL,
             None),
            ("04_scrapie_and_kuru_spongiform_histology_slides_under_dual_brass_microscope_pan", 94.0, 5.5, "C", False, "5 SEPTEMBER 1959 — IDENTICAL SPONGIFORM HOLES", "Fast",
             "Fast: daylight close-up pan across two stained histology slides mounted side by side under a comparison microscope on an oak table. Nothing emissive, no face.",
             STYLE + "In bright window light on an oak table, a dual-stage brass comparison microscope holds two stained glass slides side by side beside a fountain pen." + FAST_TAIL,
             None),
        ],
    ),
    (
        3,
        "Part 03 — 9 April 1982 & 19 April 1985: Stanley Prusiner's Prion Heresy & the Enemy Inside Our Own Genome — Midpoint Twist",
        [
            ("01_stanley_prusiner_9_apr_1982_ucsf_prions_and_19_apr_1985_weissmann_hood_prnp_gene", 99.5, 6.5, "A", False, "SAME PROTEIN, TWO 3D FOLDS", "Quality",
             "Quality: readable faces (American neurologist Stanley Prusiner at UCSF on 9 April 1982 holding purified PrP 27–30 ultracentrifuge tubes and coining 'prion', dissolving to Charles Weissmann, Leroy Hood, and Prusiner on 19 April 1985 discovering the PRNP gene inside normal healthy mammalian chromosomes).",
             STYLE + "Split period scene: on the left in April 1982 San Francisco, Stanley Prusiner inspects a high-speed ultracentrifuge rotor and electron micrographs of prion rods; on the right in April 1985, Charles Weissmann and Prusiner point to the PRNP gene band present in healthy mouse, hamster, and human chromosomes." + QUAL_TAIL,
             {"kind": "FACT", "label": "Same protein, two 3D folds", "when_stamp": "1972 · 9 April 1982 · 19 April 1985 · 1 December 1993", "timeline_step": "2/3 · 9 Apr 1982 & 19 Apr 1985 (Stanley Prusiner isolates PrP 27–30 and coins 'prion' in Science; Oesch, Hood, Prusiner & Weissmann prove PRNP is a normal cellular gene)", "hold_s": 3.8}),
            ("02_prusiner_1982_science_oesch_1985_cell_and_pan_1993_pnas_ftir_alpha_beta_chart", 106.0, 8.0, "E", False, "9 APR 1982 PRUSINER (SCIENCE) · 19 APR 1985 OESCH/WEISSMANN (CELL) · 1 DEC 1993 PAN & PRUSINER (PNAS): PRPC (43% α-HELIX, 3% β-SHEET) VS PRPSC (30% α-HELIX, 43% β-SHEET)", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked Prusiner (9 April 1982 Science 216: 136–144), Oesch, Hood, Prusiner & Weissmann (19 April 1985 Cell 40: 735–746), and Pan et al. (1 December 1993 PNAS 90: 10962–10966) Fourier-transform infrared (FTIR) secondary structure & protease-resistance chart compares cellular PrPC (43% alpha-helix, 3% beta-sheet, digested by proteinase K) vs infectious PrPSc (30% alpha-helix, 43% beta-sheet, resistant PrP 27–30 core).",
             {"kind": "DATA", "label": "1982 PRUSINER PRION PURIFICATION, 1985 HOST PRNP GENE & 1993 FTIR FOLDING SHIFT (PRPC 43% α-HELIX → PRPSC 43% β-SHEET)", "detail": "Inked Prusiner (9 April 1982 Science 216: 136–144), Oesch, Hood, Prusiner & Weissmann (19 April 1985 Cell 40: 735–746), and Pan et al. (1 December 1993 PNAS 90: 10962–10966) Fourier-transform infrared (FTIR) secondary structure & protease-resistance chart on period paper comparing cellular PrPC (43% alpha-helix, 3% beta-sheet, digested by proteinase K) vs infectious PrPSc (30% alpha-helix, 43% beta-sheet, resistant PrP 27–30 core)", "scale": "normal PrPC and deadly PrPSc are built from the exact same string of amino-acid beads — the difference is like folding the exact same sheet of steel into a soft mattress spring versus hammering it into a flat crowbar that bends every spring it touches into another crowbar", "hold_s": 3.8}),
            ("03_ucsf_1982_ultracentrifuge_rotor_and_prp_27_30_prion_rod_micrograph_closeup", 114.0, 6.5, "B", False, "9 APRIL 1982 — PRIONS ('PROTEINACEOUS INFECTIOUS PARTICLES')", "Fast",
             "Fast: daylight macro shot of a brushed aluminium ultracentrifuge rotor beside a framed electron micrograph of rod-shaped PrP 27–30 assemblies and a bottle of proteinase K on a bench. Nothing emissive, no face.",
             STYLE + "In crisp daylight on a 1982 biochemistry bench, a machined metal ultracentrifuge rotor sits beside a printed micrograph of crystalline protein rods and a glass reagent vial." + FAST_TAIL,
             None),
            ("04_springy_golden_alpha_helix_prpc_model_beside_flat_pleated_beta_sheet_prpsc_model_pan", 120.5, 5.5, "C", False, "43% ALPHA-HELIX VS 43% BETA-SHEET", "Fast",
             "Fast: daylight close-up pan across two 3D ribbon models on an oak table: a three-helix spiral PrPC model and a flat pleated beta-sheet PrPSc stack. Nothing emissive, no face.",
             STYLE + "In bright window light on an oak table, a sculpted golden three-helix coil model sits beside a flat pleated iron beta-sheet stack built from the same coloured bead chain." + FAST_TAIL,
             None),
        ],
    ),
    (
        4,
        "Part 04 — 2 July 1993 & 1986–1997: Charles Weissmann's Knockout Mouse & the Mad Cow (BSE) Crisis",
        [
            ("01_charles_weissmann_adriano_aguzzi_2_jul_1993_zurich_prnp_knockout_mice_and_1997_nobel", 126.0, 6.5, "A", False, "KNOCKOUT MICE 100% IMMUNE", "Quality",
             "Quality: readable faces (Swiss molecular biologist Charles Weissmann and neuropathologist Adriano Aguzzi at the University of Zurich on 2 July 1993 with healthy white Prnp0/0 prion-knockout mice surviving past 500 days, dissolving to UK BSE epidemic curves and Stanley Prusiner receiving the 1997 Nobel Prize).",
             STYLE + "Split period scene: on the left in July 1993 Zurich, Charles Weissmann and Adriano Aguzzi examine lively white Prnp0/0 knockout mice beside a survival chart; on the right, Stanley Prusiner in October 1997 holds a protein model as the UK BSE epidemic curve drops after the feed ban." + QUAL_TAIL,
             {"kind": "FACT", "label": "Knockout mice 100% immune", "who_card": "Adriano Aguzzi (born 1960) — Italian-Swiss neuropathologist", "when_stamp": "November 1986 · 14 May 1992 · 2 July 1993 · 6 April 1996 · October 1997", "timeline_step": "3/3 · 2 Jul 1993 & Oct 1997 (Charles Weissmann & Adriano Aguzzi prove Prnp0/0 knockout mice are 100% immune to scrapie; Stanley Prusiner wins the 1997 Nobel Prize)", "hold_s": 3.8}),
            ("02_bueler_aguzzi_weissmann_2_jul_1993_cell_prion_titre_and_uk_bse_epidemic_chart", 132.5, 8.0, "E", False, "2 JUL 1993 BÜELER, AGUZZI & WEISSMANN (CELL: PRNP0/0 0 TITRE >500 DAYS) & UK BSE EPIDEMIC CURVE (>180,000 CATTLE, FEED BAN DECLINE)", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked Büeler, Aguzzi & Weissmann (2 July 1993 Cell 73: 1339–1347) brain prion-titre curve (log LD50 units over 50 weeks in Prnp+/+, Prnp+/0, and Prnp0/0 mice) alongside the UK BSE epidemic curve (1986–2000, >180,000 cattle, peaking in 1992–1993 after the July 1988 ruminant feed ban) shows zero prion multiplication in mice lacking normal PrPC.",
             {"kind": "DATA", "label": "2 JUL 1993 ZURICH PRNP0/0 KNOCKOUT TITRE CURVE (0 INFECTIVITY >500 DAYS) & 1986–2000 UK BSE EPIDEMIC (>180,000 CATTLE)", "detail": "Inked Büeler, Aguzzi & Weissmann (2 July 1993 Cell 73: 1339–1347) brain prion-titre curve (log LD50 units over 50 weeks in Prnp+/+, Prnp+/0, and Prnp0/0 mice) alongside the UK BSE epidemic curve (1986–2000, peaking in 1992–1993 after the July 1988 ruminant feed ban) on period paper", "scale": "a normal mouse brain is a room packed with standing PrPC dominoes where one PrPSc spark triggers a fatal avalanche in twenty-three weeks, whereas a Prnp0/0 knockout mouse brain is an empty floor where the spark simply dies out", "hold_s": 3.8}),
            ("03_zurich_1993_knockout_mouse_survival_ledger_and_1996_brain_graft_diagram_closeup", 140.5, 6.5, "B", False, "2 JULY 1993 — PRNP KNOCKOUT PROOF", "Fast",
             "Fast: daylight macro shot of a 1993 Zurich laboratory survival ledger showing 500-day healthy knockout cohorts beside a 1996 brain-graft diagram on a bench. Nothing emissive, no face.",
             STYLE + "In crisp daylight on a genetics bench, an open laboratory ledger showing flat survival lines past 500 days sits beside a wooden model of a mouse brain with a small highlighted graft zone." + FAST_TAIL,
             None),
            ("04_explorer_removing_standing_prpc_dominoes_from_knockout_brain_tray_so_prpsc_slides_harmlessly", 147.0, 5.5, "B", True, None, "Quality",
             "Quality: Explorer beat 2 (locked character reference).",
             STYLE + "Standing at a wooden demonstration table, the Explorer lifts the last standing golden spring dominoes off a brain-shaped tray and flicks a flat iron domino across the empty tray, where it slides harmlessly to a stop with nothing to knock over." + EXP_TAIL,
             None),
        ],
    ),
    (
        5,
        "Part 05 — Why Prions Changed How We Understand Alzheimer's & Parkinson's — & How Crushed Yeast Unlocked Enzymes",
        [
            ("01_timeline_1957_1997_and_prion_like_template_blocking_antibody_chart", 152.5, 8.5, "E", False, "1957–1997 TIMELINE · HADLOW/GAJDUSEK/ALPERS KURU, ALPER/GRIFFITH UV PROOF, PRUSINER PRIONS, WEISSMANN KNOCKOUT MICE & TEMPLATE BLOCKING", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, the 3-era timeline completes: 5 Sep 1959 & 19 Feb 1966 (William Hadlow links sheep scrapie to kuru; Carleton Gajdusek & Michael Alpers prove kuru is a slow transmissible spongiform encephalopathy, winning the 1976 Nobel Prize) · 20 May & 9 Sep 1967 (Tikvah Alper proves the scrapie agent survives nucleic-acid-shredding UV and ionizing radiation; John Stanley Griffith proposes self-replicating protein folding) · 9 Apr 1982, 19 Apr 1985 & 2 Jul 1993 (Stanley Prusiner isolates PrP and coins 'prion'; Prusiner, Hood & Weissmann find the PRNP gene in normal DNA; Charles Weissmann's Prnp0/0 knockout mice prove the protein-domino hypothesis and win Prusiner the 1997 Nobel Prize).",
             {"kind": "DATA", "label": "1957–1997 PRIONS TIMELINE · PROTEIN-TEMPLATED REFOLDING IN NEUROLOGY & BENEFICIAL YEAST PRION MEMORY", "detail": "Animated timeline (1957 → 1997) alongside a diagram showing therapeutic antibodies capping the PrPC-to-PrPSc contact interface to halt template propagation", "scale": "from mountain villages in Papua New Guinea to a radiation chamber in London and knockout mice in Zurich, prions proved that biological information can hide not just in a string of DNA letters, but in the 3D fold of a single protein", "when_stamp": "1957–1997", "timeline_step": "3/3 · 1957–1997 timeline complete", "hold_s": 3.8}),
            ("02_antibody_capped_prion_model_beside_brass_lock_and_key_enzyme_plinth_pan", 161.0, 5.5, "A", False, "BLOCKING THE PROTEIN DOMINO CHAIN", "Fast",
             "Fast: daylight close-up of a sculpted golden alpha-helix protein capped by a protective antibody clamp beside a brass lock-and-key enzyme model on a wooden museum plinth. Nothing emissive, no face.",
             STYLE + "In crisp daylight on a wooden museum plinth, a golden spiral protein model fitted with a protective brass shield clamp sits beside an ornate brass lock and key." + FAST_TAIL,
             None),
            ("03_fischer_1894_buchner_11_jan_1897_yeast_press_sumner_1926_urease_and_phillips_1965_lysozyme_handoff", 166.5, 6.5, "C", False, "ENZYMES, ZYMASE & MOLECULAR LOCKS", "Quality",
             "Quality: readable faces (Emil Fischer in Berlin in 1894 with his lock-and-key sugar models and Eduard Buchner in Munich on 11 January 1897 operating his 300-atmosphere hydraulic yeast press, dissolving to one-armed James Sumner at Cornell in August 1926 with jack-bean urease crystals and David Phillips in London on 22 May 1965 unveiling the 2-angstrom X-ray model of lysozyme — handoff to 070 Enzymes, Fermentation & the Lock-and-Key Active Site).",
             STYLE + "Split period scene: on the left in January 1897 Munich, Eduard Buchner presses crushed yeast at 300 atmospheres into bubbling cell-free juice beside Emil Fischer holding a brass lock and key; on the right in August 1926 Ithaca and May 1965 London, one-armed James Sumner peers at octahedral urease crystals while David Phillips points to a 3D atomic model of lysozyme." + QUAL_TAIL,
             {"kind": "WHEN", "label": "1857 · 1894 · 11 JANUARY 1897 · AUGUST 1926 · FEBRUARY 1958 · 22 MAY 1965", "hold_s": 3.5}),
            ("04_table_three_callback", 173.0, 2.4, "C", False, None, "reuse",
             "Reuse: verified unused moving window [5.50s..7.90s] of P1:07_table_three_props_1959_kuru_slide_1982_prion_ultracentrifuge_tube_and_domino_protein_model (callback, £0).",
             "Reuse P1:07_table_three_props_1959_kuru_slide_1982_prion_ultracentrifuge_tube_and_domino_protein_model [5.50s..7.90s] (2.40s distinct non-overlapping tail window from 8.00s source clip).",
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
                row["reuse_of"] = "P1:07_table_three_props_1959_kuru_slide_1982_prion_ultracentrifuge_tube_and_domino_protein_model"
                row["reuse_window_s"] = [5.5, 7.9]
                row["reuse_audit"] = {
                    "source_row": "P1:07_table_three_props_1959_kuru_slide_1982_prion_ultracentrifuge_tube_and_domino_protein_model",
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
            "film": "069_Alper-Gajdusek-Prusiner-Weissmann-Prions-Mad-Cow",
            "part": p_idx,
            "title": p_title,
            "version": "v01",
            "timing_status": "pre_vo_script_clock (built from prions_script_master_v01.md; retimes onto Scribe STT once VO locks)",
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
        "film": "069_Alper-Gajdusek-Prusiner-Weissmann-Prions-Mad-Cow",
        "version": "v01",
        "date": "2026-10-19",
        "owner": "gemini (J0676)",
        "status": "PRE_VO_BOARDS_V01_NO_MINT",
        "generation_authorized": False,
        "script": "00_Brand/Channel-Setup/ideas/069_Alper-Gajdusek-Prusiner-Weissmann-Prions-Mad-Cow/prions_script_master_v01.md",
        "sources": "00_Brand/Channel-Setup/ideas/069_Alper-Gajdusek-Prusiner-Weissmann-Prions-Mad-Cow/SOURCES_v01.md",
        "credit_snapshot": {
            "flow_balance": 23740,
            "flow_floor": 0,
            "flow_read_at": "2026-10-15T21:42:22Z",
            "vertex_promo_gbp": 71.02,
            "vertex_usable_gbp": 70.02,
        },
        "totals": totals,
        "per_part": per_part_summary,
        "mint_order": "006 > 007 > 008 > 009 > 010 > 011 > 012 > 013 > 014 > 015 > 016 > 017 > 018 > 019 > 020 > 021 > 022 > 023 > 024 > 025 > 026 > 027 > 028 > 029 > 030 > 031 > 032 > 033 > 034 > 035 > 036 > 037 > 038 > 039 > 040 > 041 > 042 > 043 > 044 > 045 > 046 > 047 > 048 > 049 > 050 > 051 > 052 > 053 > 054 > 055 > 056 > 057 > 058 > 059 > 060 > 061 > 062 > 063 > 064 > 065 > 066 > 067 > 068 > 069 > 070 > 071. Nothing in 069 is generation_authorized.",
    }
    (EDIT / "PICTURE_PLAN_v01.json").write_text(json.dumps(plan, indent=2) + "\n")

    sl = [
        "# 069 Prions: The Deadly Contagion With Zero DNA — Shot list & plate boards v01 (pre-VO)",
        "",
        "Gemini, 19 Oct 2026, J0676. Built from `prions_script_master_v01.md` (`92.0 PASS`) and `SOURCES_v01.md`.",
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
        "# 069 price review v01 (pre-VO plate boards)",
        "",
        "Gemini, 19 Oct 2026, J0676. Boards only. **No mint. No spend. No merge.**",
        "Prepared from `prions_script_master_v01.md` (`92.0 PASS`) and `SOURCES_v01.md` so 069's full plate board rows, non-emissive Fast prompts, £0 code graphics, and Teach-on-Screen overlays are ready to re-time the moment long VO locks. Parked for Chief.",
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
        f"- **Quality ({totals['Quality']} rows):** readable faces (William J. Hadlow, D. Carleton Gajdusek, Michael P. Alpers, Tikvah Alper, John Stanley Griffith, Stanley B. Prusiner, Charles Weissmann, Adriano Aguzzi, Emil Fischer, Eduard Buchner, James B. Sumner, David C. Phillips), May 1967 London 254 nm UV scrapie survival & PrPC-to-PrPSc domino conversion, 9 April 1982 UCSF prion rod purification & 19 April 1985 normal `PRNP` gene discovery, 2 July 1993 Zurich `Prnp⁰/⁰` knockout mouse proof, and the 2 Explorer beats.",
        f"- **Fast ({totals['Fast']} rows, non-emissive):** daylight prop and laboratory shots (sculpted brass alpha-helix spring & flat beta-sheet dominoes with 1967 *Nature* offprint pan, 3-object callback bench, quartz UV cuvette rack & Griffith protein-dimer notebook, dual-stage comparison microscope with scrapie and kuru histology slides, machined ultracentrifuge rotor & PrP 27–30 electron micrograph, 3D alpha-helix vs beta-sheet ribbon models, 1993 Zurich 500-day knockout mouse ledger & brain-graft model, antibody-capped prion model & brass lock-and-key enzyme plinth). Zero candles, flames, sparks, or glowing elements on Fast.",
        f"- **£0 code graphics ({totals['code_graphic']} rows):**",
        "  1. `P1:04_alper_1967_uv_survival_and_prusiner_1982_1993_prpc_to_prpsc_conversion_chart` — Alper (20 May 1967 *Nature*) 254 nm UV survival curve + Pan & Prusiner (1 December 1993 *PNAS*) `PrP^C` (`43%` α-helix, `3%` β-sheet) → `PrP^Sc` (`30%` α-helix, `43%` β-sheet) conversion (`SCALE: a prion is not a living parasite with its own genetic blueprint — it is a single misfolded crystal seed that snaps normal springy brain proteins into flat rigid sheets on contact, like one toppling domino knocking down an entire room`)",
        "  2. `P1:06_weissmann_2_jul_1993_cell_prnp_knockout_mouse_resistance_chart` — Büeler, Aguzzi & Weissmann (2 July 1993 *Cell*) `Prnp⁰/⁰` knockout mouse survival chart (`100%` symptom-free `>500 days` vs `~23 weeks` in wild-type mice) (`SCALE: removing the normal prion gene from a mouse is like taking all the standing dominoes off the table — you can flick a diseased prion domino into the brain, but with no normal dominoes to hit, the chain reaction stops dead`)",
        "  3. `P2:02_hadlow_1959_gajdusek_1966_and_alper_20_may_1967_nature_uv_target_inactivation_chart` — Hadlow (5 September 1959 *Lancet*), Gajdusek, Gibbs & Alpers (19 February 1966 *Nature*), and Alper et al. (20 May 1967 *Nature*) ionizing / 254 nm UV radiation target-size & inactivation chart (`SCALE: blasting the scrapie agent with ultraviolet light that shreds DNA and RNA is like firing cannonballs at a ghost — every virus in the dish is blown apart, while the DNA-free scrapie particle walks straight through untouched`)",
        "  4. `P3:02_prusiner_1982_science_oesch_1985_cell_and_pan_1993_pnas_ftir_alpha_beta_chart` — Prusiner (9 April 1982 *Science*), Oesch, Hood, Prusiner & Weissmann (19 April 1985 *Cell*), and Pan et al. (1 December 1993 *PNAS*) FTIR secondary-structure & proteinase-K resistance chart (`SCALE: normal PrPC and deadly PrPSc are built from the exact same string of amino-acid beads — the difference is like folding the exact same sheet of steel into a soft mattress spring versus hammering it into a flat crowbar that bends every spring it touches into another crowbar`)",
        "  5. `P4:02_bueler_aguzzi_weissmann_2_jul_1993_cell_prion_titre_and_uk_bse_epidemic_chart` — Büeler, Aguzzi & Weissmann (2 July 1993 *Cell*) brain prion-titre curve over 50 weeks alongside the 1986–2000 UK BSE epidemic curve (`>180,000` cattle) (`SCALE: a normal mouse brain is a room packed with standing PrPC dominoes where one PrPSc spark triggers a fatal avalanche in twenty-three weeks, whereas a Prnp0/0 knockout mouse brain is an empty floor where the spark simply dies out`)",
        "  6. `P5:01_timeline_1957_1997_and_prion_like_template_blocking_antibody_chart` — completed timeline (1957 → 1997) + therapeutic antibody capping the PrPC-to-PrPSc contact interface (`SCALE: from mountain villages in Papua New Guinea to a radiation chamber in London and knockout mice in Zurich, prions proved that biological information can hide not just in a string of DNA letters, but in the 3D fold of a single protein`)",
        f"- **£0 verified reuse ({totals['reuse']} row):** `P5:04_table_three_callback` uses the 2.40 s unused moving tail `[5.50s..7.90s]` of `P1:07_table_three_props_1959_kuru_slide_1982_prion_ultracentrifuge_tube_and_domino_protein_model`.",
        "",
        "## Mint order",
        "",
        "006 > 007 > 008 > 009 > 010 > 011 > 012 > 013 > 014 > 015 > 016 > 017 > 018 > 019 > 020 > 021 > 022 > 023 > 024 > 025 > 026 > 027 > 028 > 029 > 030 > 031 > 032 > 033 > 034 > 035 > 036 > 037 > 038 > 039 > 040 > 041 > 042 > 043 > 044 > 045 > 046 > 047 > 048 > 049 > 050 > 051 > 052 > 053 > 054 > 055 > 056 > 057 > 058 > 059 > 060 > 061 > 062 > 063 > 064 > 065 > 066 > 067 > 068 > 069 > 070 > 071. `generation_authorized` is `false` on every row.",
    ])
    (EDIT / "PRICE_REVIEW_v01.md").write_text("\n".join(pr_lines) + "\n")
    print(f"069 v01 boards written: {totals['rows']} rows, Flow expected={totals['flow_credits_expected']}")


if __name__ == "__main__":
    main()
