#!/usr/bin/env python3
"""HOS 056 (How We Smell: The 400 Piano Keys Inside Your Nose) pre-VO plate boards v01. J0615. No mint, no spend.

Built from 00_Brand/Channel-Setup/ideas/056_Buck-Axel-Olfaction-Smell/olfaction_script_master_v01.md
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
        "Part 01 — How 400 Molecular Locks Play Piano Chords Inside Your Nose",
        [
            ("01_blindfolded_apple_potato_pinched_nose_and_buck_axel_1991_400_olfactory_receptors", 0.0, 5.5, "A", False, "400 KEYS, 10,000 SCENTS", "Quality",
             "Quality: Short frame 0 / answer image (0:03) + a blindfolded volunteer pinching their nose shut bites a cube of raw apple and a cube of raw potato without telling them apart until they release their fingers and a puff of retro-nasal aroma molecules rises up the back of the throat to a postage-stamp patch of yellow olfactory neurons at the roof of the nasal cavity, playing a chord across 400 receptors and olfactory bulb glomeruli discovered by Linda Buck and Richard Axel on 5 April 1991.",
             STYLE + "Split period-and-anatomical scene: on the left, a blindfolded volunteer releases a pinched nose while tasting slices of apple and potato; on the right, aroma plumes rise to the roof of the nasal cavity where olfactory sensory neurons play a chord across four hundred receptor locks." + QUAL_TAIL,
             {"kind": "WHEN", "label": "NEW YORK, 5 APRIL 1991", "timeline_step": "2/4 · 5 Apr 1991 (Linda Buck & Richard Axel use PCR to discover the ~1,000-gene mammalian / ~400-gene human olfactory receptor family, 3% of the genome)", "hold_s": 3.5}),
            ("02_amoore_1952_oxford_buck_axel_1991_columbia_and_malnic_buck_1999_chord_split", 5.5, 6.0, "B", False, "MOLECULAR LOCKS, 1,000 GENES, SCENT CHORDS", "Quality",
             "Quality: complex three-part composition (John Amoore at Oxford in 1952 comparing differently shaped odour molecules; Linda Buck and Richard Axel at Columbia University on 5 April 1991 using PCR to uncover the 1,000-gene olfactory receptor family; and Linda Buck and Bettina Malnic at Harvard on 5 March 1999 imaging nasal neurons to prove the combinatorial chord code of smell).",
             STYLE + "Three-panel period composition: on the left, British biochemist John Amoore fitting carved molecular shapes into lock sockets in 1952; in the centre, Linda Buck and Richard Axel in 1991 New York inspecting a multi-band PCR gel; on the right, Linda Buck and Bettina Malnic in 1999 Boston mapping scent chords across a piano-like receptor grid." + QUAL_TAIL,
             None),
            ("03_retronasal_aroma_plume_behind_palate_to_5cm2_olfactory_epithelium", 11.5, 6.0, "C", False, "80% OF FLAVOUR IS SMELL", "Quality",
             "Quality: complex anatomical cross-section reveal (a human head chewing food: with the nostrils pinched shut, only basic taste buds on the tongue respond, whereas opening the nose sends volatile aroma plumes up the pharynx behind the soft palate to the 5 cm² olfactory epithelium at the roof of the nasal cavity).",
             STYLE + "Anatomical cross-section of a human head chewing a berry: as the nostrils open, a warm stream of tiny coloured aroma spheres wafts up the back of the throat behind the soft palate to brush across a postage-stamp yellow patch of sensory cilia at the roof of the nose." + QUAL_TAIL,
             {"kind": "WHEN", "label": "1952 · 5 APRIL 1991 · DECEMBER 1994 · NOVEMBER 1996 · 5 MARCH 1999", "timeline_step": "1/4 · 1952 (Amoore) · 2/4 · 5 Apr 1991 (Buck & Axel) · 3/4 · Dec 1994 & Nov 1996 (Vassar, Mombaerts, Buck & Axel) · 4/4 · 5 Mar 1999 (Malnic & Buck)", "hold_s": 3.5}),
            ("04_buck_axel_1991_sensory_gene_count_3_cones_vs_400_human_1000_mouse_olfactory_receptors_chart", 17.5, 8.0, "E", False, "3 COLOUR CONE GENES & ~35 TASTE GENES VS ~400 HUMAN (~1,000 MAMMALIAN) OLFACTORY RECEPTOR GENES (~3% OF GENOME)", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked sensory receptor gene count & combinatorial olfaction chart from Buck & Axel (5 April 1991 Cell 65: 175–187) and Malnic, Hirono, Sato & Buck (5 March 1999 Cell 96: 713–723) contrasts human vision (3 colour cone genes) and taste (~30–40 taste receptor genes across 5 basic tastes) against olfaction (~1,000 receptor genes in mice / ~390–400 functional + ~460 pseudogenes in humans = ~3% of all human genes).",
             {"kind": "DATA", "label": "3 VISION CONE GENES & ~35 TASTE GENES VS ~400 HUMAN (~1,000 MOUSE) OLFACTORY RECEPTOR GENES (~3% OF ENTIRE GENOME)", "detail": "Inked human sensory gene allocation & combinatorial receptor chart on period paper comparing 3 colour-vision cone genes and ~35 taste genes against ~400 functional human (~1,000 mammalian) olfactory receptor genes (~3% of the 20,000-gene genome) encoding >10,000 distinct odour chords", "scale": "your eyes need just three colour genes to see the entire rainbow — yet your DNA devotes four hundred working genes, or three out of every hundred genes in your body, solely to building smell locks inside your nose", "who_card": "John E. Amoore (1930–1998) — British biochemist · Linda B. Buck (born 1947) — American neurobiologist · Richard Axel (born 1946) — American molecular biologist · Robert Vassar (born 1961) — American neurobiologist · Peter Mombaerts (born 1962) — Belgian neuroscientist · Bettina Malnic (born 1966) — Brazilian biochemist", "when_stamp": "1952 · 5 April 1991 · December 1994 · November 1996 · 5 March 1999", "hold_s": 3.8}),
            ("05_perfume_flacon_coffee_beans_rose_petals_and_brass_molecular_lock_model_pan", 25.5, 5.5, "A", False, "COMBINATORIAL PIANO CHORDS", "Fast",
             "Fast: daylight macro pan across a cut-glass perfume bottle, roasted coffee beans, fresh rose petals, and a brass-and-wood 7-helix receptor lock model on an oak laboratory bench between code graphics so two full-frame graphics never run back to back. Nothing emissive, no face.",
             STYLE + "In crisp daylight on an oak laboratory bench, the camera pans smoothly across a glass perfume stopper bottle, dark roasted coffee beans, red rose petals, and a brass seven-column receptor lock model." + FAST_TAIL,
             None),
            ("06_one_to_one_400_smells_vs_combinatorial_piano_chord_billions_of_scents_chart", 31.0, 8.0, "E", False, "400 RECEPTOR KEYS → BILLIONS OF CHORDS", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period parchment, an inked combinatorial chord math chart from Malnic & Buck (5 March 1999, Cell) compares a 1-to-1 lock-and-key model (400 receptors = only 400 smells) against Buck's combinatorial receptor code (400 receptors taken 3 to 5 at a time = millions to billions of unique receptor chords).",
             {"kind": "DATA", "label": "1-TO-1 LOCK MODEL (400 SMELLS) VS COMBINATORIAL PIANO-CHORD CODE (400 RECEPTORS IN 3–5 KEY CHORDS = BILLIONS OF SCENTS)", "detail": "Inked combinatorial chord math chart comparing a 1-to-1 lock-and-key model (400 receptors = only 400 smells) against Buck's combinatorial receptor code (400 receptors taken 3 to 5 at a time = millions to billions of unique receptor chords)", "scale": "if each smell receptor recognised only one scent, you could smell only four hundred things — instead, your nose plays those four hundred receptors like chords on a piano, where pressing just four keys at once creates over a billion possible combinations", "hold_s": 3.8}),
            ("07_table_three_props_amoore_shape_blocks_buck_1991_pcr_gel_and_piano_chord_odorant_board", 39.0, 5.5, "C", False, "1952 TO 2004", "Fast",
             "Fast: daylight prop table (callback source for Part 05: John Amoore's 1952 carved wooden stereochemical lock-and-key blocks, Linda Buck's 1991 multi-band olfactory receptor PCR gel plate, and a miniature brass-keyed scent chord board). Nothing emissive.",
             STYLE + "On an oak workbench in soft window light sit three objects side by side: carved wooden molecular lock-and-key blocks, a framed multi-band DNA gel plate, and a miniature wooden keyboard with glass scent vials." + FAST_TAIL,
             None),
            ("08_explorer_playing_400_key_olfactory_piano_1_octanol_rose_chord_vs_octanoic_acid_goat_chord", 62.0, 5.5, "A", True, None, "Quality",
             "Quality: Explorer beat 1 (locked character reference, after 1:00).",
             STYLE + "Sitting at a grand wooden keyboard connected to brass scent pipes, the Explorer presses a three-key chord that releases a gentle swirl of rose petals and orange blossoms, then shifts one finger by a single key and leans back as a greenish puff of goat-cheese vapour wafts up." + EXP_TAIL,
             None),
            ("09_linda_buck_5_apr_1991_columbia_examining_1000_gene_olfactory_receptor_gel", 67.5, 5.5, "B", False, "NEW YORK, 5 APRIL 1991", "Quality",
             "Quality: readable face (at Columbia University in New York in April 1991, American neurobiologist Linda Buck examines a restriction-digest PCR gel displaying dozens of newly amplified G-protein-coupled olfactory receptor DNA bands).",
             STYLE + "In a 1991 Columbia University molecular biology lab, neurobiologist Linda Buck in a white lab coat holds up a developed electrophoresis gel covered in a dense ladder of receptor gene bands." + QUAL_TAIL,
             {"kind": "WHEN", "label": "NEW YORK, 5 APRIL 1991", "timeline_step": "2/4 · 5 Apr 1991 (Linda Buck & Richard Axel discover the ~1,000-gene olfactory receptor family in Cell)", "hold_s": 3.5}),
        ],
    ),
    (
        2,
        "Part 02 — 50 BC, 1952 & 5 April 1991: Lucretius's Shaped Atoms, John Amoore's Stereochemical Locks & Linda Buck and Richard Axel's 1,000-Gene Shock",
        [
            ("01_amoore_1952_oxford_stereochemical_models_and_buck_axel_5_apr_1991_columbia_gpcr_discovery", 73.0, 6.5, "A", False, "3% OF ALL YOUR GENES", "Quality",
             "Quality: readable faces (British biochemist John Amoore at Oxford in 1952 fitting shaped molecular models into stereochemical receptor sockets, dissolving to Linda Buck and Richard Axel at Columbia University on 5 April 1991 discovering the ~1,000-gene mammalian / ~400-gene human 7-transmembrane GPCR olfactory receptor family).",
             STYLE + "Split period scene: on the left in 1952 Oxford, biochemist John Amoore fits wooden ball-and-stick odour models into carved sockets; on the right in April 1991 New York, Linda Buck and Richard Axel celebrate beside a gel revealing hundreds of seven-transmembrane smell receptor genes." + QUAL_TAIL,
             {"kind": "FACT", "label": "3% of all your genes", "when_stamp": "50 BC · 1952 · 5 April 1991 · 2004", "timeline_step": "1/4 · 1952 (Amoore stereochemical theory) & 2/4 · 5 Apr 1991 (Buck & Axel 1,000-gene family; 2004 Nobel Prize)", "hold_s": 3.8}),
            ("02_buck_axel_5_apr_1991_cell_7tm_gpcr_1000_mouse_400_human_olfactory_gene_family_chart", 79.5, 8.0, "E", False, "5 APR 1991 BUCK & AXEL: 7-TRANSMEMBRANE GPCR OLFACTORY RECEPTOR FAMILY (~1,000 RODENT GENES, ~400 HUMAN FUNCTIONAL + ~460 PSEUDOGENES = ~3% OF PROTEOME)", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked mammalian & human olfactory receptor multigene family chart from Buck & Axel (5 April 1991, Cell 65: 175–187) shows 7-transmembrane GPCR odorant receptors comprising ~1,000 genes in rodents and ~390–400 functional genes (+ ~460 pseudogenes) in humans, representing ~3–4% of the entire mammalian proteome.",
             {"kind": "DATA", "label": "5 APR 1991 BUCK & AXEL: ~1,000 MAMMALIAN / ~400 HUMAN 7-TM GPCR SMELL GENES (~3% OF ALL HUMAN GENES)", "detail": "Inked mammalian & human olfactory receptor multigene family chart on period paper from Buck & Axel (5 April 1991, Cell 65: 175–187) showing 7-transmembrane GPCR odorant receptors comprising ~1,000 genes in rodents and ~390–400 functional genes (+ ~460 pseudogenes) in humans, representing ~3–4% of the entire mammalian proteome", "scale": "out of the roughly twenty thousand protein-coding genes that build your entire body — your heart, brain, bones, and muscles — roughly one out of every thirty genes is dedicated solely to helping you smell", "hold_s": 3.8}),
            ("03_columbia_1991_pcr_tubes_restriction_digest_gel_and_7tm_ribbon_sketch_closeup", 87.5, 6.5, "B", False, "5 APRIL 1991 — 1,000 SMELL GENES", "Fast",
             "Fast: daylight macro shot of PCR microcentrifuge tubes, a restriction-digest gel photograph, and an inked notebook diagram of a 7-transmembrane receptor snake on a Columbia workbench. Nothing emissive, no face.",
             STYLE + "In crisp daylight on a laboratory desk, a rack of PCR micro-tubes sits beside a multi-lane gel print and an open notebook showing a seven-loop membrane protein sketch." + FAST_TAIL,
             None),
            ("04_oxford_1952_ball_and_stick_odour_molecules_and_carved_lock_sockets_pan", 94.0, 5.5, "C", False, "1952 — STEREOCHEMICAL LOCKS", "Fast",
             "Fast: daylight close-up pan across vintage 1952 wooden ball-and-stick molecular models and matching concave pocket moulds alongside glass stoppered scent bottles. Nothing emissive, no face.",
             STYLE + "In bright window light on an Oxford chemistry bench, wooden ball-and-stick molecular models sit beside carved wooden socket moulds and glass apothecary scent bottles." + FAST_TAIL,
             None),
        ],
    ),
    (
        3,
        "Part 03 — December 1994 – November 1996: The 'One Neuron, One Receptor' Rule & the Brain's Glowing Smell Map (Glomeruli) — Midpoint Twist",
        [
            ("01_vassar_buck_1994_and_mombaerts_axel_nov_1996_one_neuron_one_receptor_glomerular_convergence", 99.5, 6.5, "A", False, "1 NEURON = 1 RECEPTOR GENE", "Quality",
             "Quality: readable faces (Linda Buck, Robert Vassar, Peter Mombaerts, and Richard Axel in December 1994 – November 1996 examining blue tau-lacZ stained olfactory sensory neurons whose scattered axons converge through the cribriform plate onto one single glomerulus sphere in the olfactory bulb).",
             STYLE + "Split period scene: on the left in 1994, Linda Buck and Robert Vassar inspect microscope slides of nasal sensory tissue; on the right in November 1996, Peter Mombaerts and Richard Axel trace blue-dyed nerve fibres converging from thousands of scattered cells onto a single blue point on the olfactory bulb." + QUAL_TAIL,
             {"kind": "FACT", "label": "1 neuron = 1 receptor gene", "when_stamp": "December 1994 · November 1996", "timeline_step": "3/4 · Dec 1994 & Nov 1996 (Vassar, Ressler, Mombaerts, Buck & Axel prove the 1-neuron-1-receptor rule and glomerular convergence in the olfactory bulb)", "hold_s": 3.8}),
            ("02_vassar_buck_1994_and_mombaerts_axel_1996_10000_axons_to_1_glomerulus_wiring_chart", 106.0, 8.0, "E", False, "DEC 1994 & NOV 1996: 6–10M NASAL NEURONS (1 RECEPTOR/CELL) CONVERGING ~10,000 AXONS PER RECEPTOR ONTO FIXED OLFACTORY BULB GLOMERULI", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked olfactory epithelium-to-glomerulus convergence wiring diagram from Vassar, Chao, Sitcheran, Nuñez, Vosshall & Axel (16 Dec 1994, Cell 79: 981–991), Ressler, Sullivan & Buck (16 Dec 1994, Cell 79: 1245–1255), and Mombaerts, Wang, Dulac, Chao, Nemes, Mendelsohn, Edmondson & Axel (15 Nov 1996, Cell 87: 675–686) shows ~6–10 million scattered nasal neurons (each expressing 1 of ~400 human / ~1,000 mouse receptor genes) sorting through the cribriform plate so all ~10,000 axons of the same receptor converge onto fixed glomeruli in the olfactory bulb.",
             {"kind": "DATA", "label": "6–10M NASAL NEURONS (1 RECEPTOR GENE/NEURON) SORTING ~10,000 AXONS OF EACH TYPE ONTO 1 GLOMERULUS STATION", "detail": "Inked olfactory epithelium-to-glomerulus convergence wiring diagram on period paper from Vassar, Chao, Sitcheran, Nuñez, Vosshall & Axel (16 Dec 1994, Cell 79: 981–991), Ressler, Sullivan & Buck (16 Dec 1994, Cell 79: 1245–1255), and Mombaerts, Wang, Dulac, Chao, Nemes, Mendelsohn, Edmondson & Axel (15 Nov 1996, Cell 87: 675–686) showing ~6–10 million scattered nasal neurons (each expressing 1 of ~400 human / ~1,000 mouse receptor genes) sorting through the cribriform plate so all ~10,000 axons of the same receptor converge onto fixed glomeruli in the olfactory bulb", "scale": "imagine ten thousand people wearing the same colour shirt scattered randomly across a packed stadium — yet when they walk out the exits, every single person in a blue shirt automatically meets at the exact same lamppost outside", "hold_s": 3.8}),
            ("03_cribriform_plate_sieve_and_blue_tau_lacz_glomerulus_convergence_model_closeup", 114.0, 6.5, "B", False, "NOVEMBER 1996 — GLOMERULAR CONVERGENCE", "Fast",
             "Fast: daylight macro shot of an anatomical model showing coloured thread axons passing through a perforated bone sieve plate to gather into neat colour-sorted spheres on the olfactory bulb beside stained microscope slides. Nothing emissive, no face.",
             STYLE + "In crisp daylight on a neurobiology workbench, a detailed anatomical model shows coloured silk threads passing through a perforated bone plate and bundling by colour into neat spheres beside glass microscope slides." + FAST_TAIL,
             None),
            ("04_postage_stamp_5cm2_olfactory_epithelium_and_microscope_slides_pan", 120.5, 5.5, "C", False, "DECEMBER 1994 — ONE NEURON, ONE RECEPTOR", "Fast",
             "Fast: daylight close-up pan across a postage-stamp scale marker beside a histological slide tray of nasal sensory epithelium and a brass binocular microscope. Nothing emissive, no face.",
             STYLE + "In bright window light on an oak bench, a wooden slide tray of stained nasal tissue sections sits beside a postage-stamp scale card and a brass microscope." + FAST_TAIL,
             None),
        ],
    ),
    (
        4,
        "Part 04 — 5 March 1999: Linda Buck & Bettina Malnic's Combinatorial Piano-Chord Code & the Proust Memory Highway",
        [
            ("01_malnic_and_buck_5_mar_1999_harvard_combinatorial_scent_chord_and_proust_memory_pathway", 126.0, 6.5, "A", False, "1 ATOM FLIPS ROSE TO SWEAT", "Quality",
             "Quality: readable faces (Brazilian biochemist Bettina Malnic and American neurobiologist Linda Buck at Harvard Medical School on 5 March 1999 comparing 1-octanol rose/citrus receptor chords against octanoic acid rancid-sweat chords, alongside the direct 2-synapse olfactory bulb pathway to the amygdala and hippocampus).",
             STYLE + "Split period scene: on the left in March 1999 at Harvard Medical School, Bettina Malnic and Linda Buck compare two 8-carbon molecular models that trigger different receptor combinations; on the right, a brain model traces the direct two-step pathway from the olfactory bulb into the amygdala and seahorse-shaped hippocampus." + QUAL_TAIL,
             {"kind": "FACT", "label": "1 atom flips rose to sweat", "when_stamp": "5 March 1999", "timeline_step": "4/4 · 5 Mar 1999 (Malnic & Buck prove the combinatorial piano-chord code of smell; 2004 Nobel Prize)", "hold_s": 3.8}),
            ("02_malnic_buck_5_mar_1999_1_octanol_vs_octanoic_acid_chord_matrix_and_2_synapse_limbic_chart", 132.5, 8.0, "E", False, "5 MAR 1999 MALNIC & BUCK: 1-OCTANOL (-OH, ROSE/CITRUS CHORD) VS OCTANOIC ACID (-COOH, SWEAT/GOAT CHORD) & 2-SYNAPSE AMYGDALA/HIPPOCAMPUS HIGHWAY", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked combinatorial odorant-receptor matrix & chemical-shift chart from Malnic, Hirono, Sato & Buck (5 March 1999, Cell 96: 713–723) shows 1-octanol (8 carbons + OH, sweet rose/citrus chord) vs octanoic acid (8 carbons + COOH, rancid sweat/goat chord) activating overlapping but distinct combinations of olfactory receptors, alongside the direct 2-synapse olfactory bulb → amygdala/hippocampus memory pathway.",
             {"kind": "DATA", "label": "5 MAR 1999 COMBINATORIAL MATRIX: 1-OCTANOL (-OH ROSE CHORD) VS OCTANOIC ACID (-COOH SWEAT CHORD) & 2-SYNAPSE MEMORY PATH", "detail": "Inked combinatorial odorant-receptor matrix & chemical-shift chart on period paper from Malnic, Hirono, Sato & Buck (5 March 1999, Cell 96: 713–723) showing 1-octanol (8 carbons + OH, sweet rose/citrus chord) vs octanoic acid (8 carbons + COOH, rancid sweat/goat chord) activating overlapping but distinct combinations of olfactory receptors, alongside the direct 2-synapse olfactory bulb → amygdala/hippocampus memory pathway", "scale": "swapping just one oxygen atom at the tip of an eight-carbon chain is like changing one note in a major piano chord to a minor dissonance — instantly flipping the smell in your brain from fresh citrus to rancid sweat", "hold_s": 3.8}),
            ("03_octanol_and_octanoic_acid_8_carbon_models_beside_rose_and_goat_cheese_closeup", 140.5, 6.5, "B", False, "2 SYNAPSES TO MEMORY & EMOTION", "Fast",
             "Fast: daylight macro shot of two 8-carbon ball-and-stick models (1-octanol with an -OH tip beside a fresh rose and orange slice; octanoic acid with a -COOH tip beside a wedge of aged goat cheese) on a wooden bench. Nothing emissive, no face.",
             STYLE + "In crisp daylight on an oak table, two eight-carbon ball-and-stick molecular models sit side by side: one beside a fresh pink rose and orange slice, the other beside a wedge of aged goat cheese." + FAST_TAIL,
             None),
            ("04_explorer_plugging_10000_colour_coded_nasal_wires_into_matching_olfactory_bulb_spheres", 147.0, 5.5, "B", True, None, "Quality",
             "Quality: Explorer beat 2 (locked character reference).",
             STYLE + "Standing at a grand brass switchboard beneath a perforated bone archway, the Explorer pulls a brass lever that routes a fresh-baked-bread scent chord down a two-stop express track straight into the hippocampus and amygdala memory vault, opening a childhood kitchen window before the visual thalamus train has left the station." + EXP_TAIL,
             None),
        ],
    ),
    (
        5,
        "Part 05 — Why Pinching Your Nose Erases Flavour — & Why 38 Trillion Bacteria Rule Your Gut",
        [
            ("01_timeline_1952_2004_and_retronasal_flavour_vs_5_basic_tongue_tastes_chart", 152.5, 8.5, "E", False, "1952–2004 TIMELINE · AMOORE LOCKS, BUCK & AXEL 1,000 GENES, GLOMERULAR CONVERGENCE & MALNIC/BUCK COMBINATORIAL CHORD CODE", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, the 4-date timeline completes: 1952 (John Amoore proposes the stereochemical lock-and-key theory of odour shapes) · 5 Apr 1991 (Linda Buck & Richard Axel use PCR to discover the ~1,000-gene mammalian / ~400-gene human olfactory receptor family, 3% of the genome) · Dec 1994 & Nov 1996 (Vassar, Ressler, Mombaerts, Buck & Axel prove the 1-neuron-1-receptor rule and glomerular convergence in the olfactory bulb) · 5 Mar 1999 (Malnic & Buck prove the combinatorial piano-chord code of smell; 2004 Nobel Prize).",
             {"kind": "DATA", "label": "1952–2004 OLFACTION TIMELINE · 400 HUMAN RECEPTOR GENES (3% OF GENOME), 1-NEURON-1-RECEPTOR MAP & COMBINATORIAL SCENT CHORDS", "detail": "Animated 4-date timeline (1952 → 2004) alongside the retro-nasal olfaction (80% of flavour) vs 5 basic tongue tastes diagram", "scale": "every single breath you take pulls millions of invisible airborne molecules across a postage-stamp keyboard of four hundred receptor types, playing silent chords that let you smell rain, coffee, and childhood memories in a heartbeat", "when_stamp": "1952–2004", "timeline_step": "4/4 · 1952–2004 timeline complete", "hold_s": 3.8}),
            ("02_apple_potato_slices_coffee_cup_and_400_key_receptor_model_on_plinth_pan", 161.0, 5.5, "A", False, "5 TONGUE TASTES + 400 NASAL KEYS = FLAVOUR", "Fast",
             "Fast: daylight close-up of apple and potato slices beside a porcelain cup of coffee and a brass 7-helix olfactory receptor model on a wooden museum plinth. Nothing emissive, no face.",
             STYLE + "In crisp daylight on a wooden museum plinth, slices of fresh apple and raw potato sit beside a porcelain coffee cup and a brass seven-helix receptor lock model." + FAST_TAIL,
             None),
            ("03_escherich_1885_metchnikoff_1907_yogurt_and_gordon_2006_38_trillion_gut_microbiome_handoff", 166.5, 6.5, "C", False, "38 TRILLION GUT BACTERIA", "Quality",
             "Quality: readable faces (Theodor Escherich on 14 July 1885 and Nobel laureate Élie Metchnikoff in 1907 in Paris beside a bowl of Bulgarian yogurt, alongside Jeffrey Gordon on 21 December 2006 mapping the 38-trillion-cell human gut microbiome digesting plant fibres — handoff to 057 Gut Microbiome).",
             STYLE + "Split period scene: on the left in 1907 Paris, bearded biologist Élie Metchnikoff examines lactic acid microbes beside a bowl of yogurt and Theodor Escherich's culture tubes; on the right in 2006, Jeffrey Gordon studies a model of thirty-eight trillion gut bacteria breaking down complex plant fibres." + QUAL_TAIL,
             {"kind": "WHEN", "label": "14 JULY 1885 · 1907 · 21 DECEMBER 2006", "hold_s": 3.5}),
            ("04_table_three_callback", 173.0, 2.4, "C", False, None, "reuse",
             "Reuse: verified unused moving window [5.50s..7.90s] of P1:07_table_three_props_amoore_shape_blocks_buck_1991_pcr_gel_and_piano_chord_odorant_board (callback, £0).",
             "Reuse P1:07_table_three_props_amoore_shape_blocks_buck_1991_pcr_gel_and_piano_chord_odorant_board [5.50s..7.90s] (2.40s distinct non-overlapping tail window from 8.00s source clip).",
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
                row["reuse_of"] = "P1:07_table_three_props_amoore_shape_blocks_buck_1991_pcr_gel_and_piano_chord_odorant_board"
                row["reuse_window_s"] = [5.5, 7.9]
                row["reuse_audit"] = {
                    "source_row": "P1:07_table_three_props_amoore_shape_blocks_buck_1991_pcr_gel_and_piano_chord_odorant_board",
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
            "film": "056_Buck-Axel-Olfaction-Smell",
            "part": p_idx,
            "title": p_title,
            "version": "v01",
            "timing_status": "pre_vo_script_clock (built from olfaction_script_master_v01.md; retimes onto Scribe STT once VO locks)",
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
        "film": "056_Buck-Axel-Olfaction-Smell",
        "version": "v01",
        "date": "2026-10-19",
        "owner": "gemini (J0615)",
        "status": "PRE_VO_BOARDS_V01_NO_MINT",
        "generation_authorized": False,
        "script": "00_Brand/Channel-Setup/ideas/056_Buck-Axel-Olfaction-Smell/olfaction_script_master_v01.md",
        "sources": "00_Brand/Channel-Setup/ideas/056_Buck-Axel-Olfaction-Smell/SOURCES_v01.md",
        "credit_snapshot": {
            "flow_balance": 23740,
            "flow_floor": 0,
            "flow_read_at": "2026-10-15T21:42:22Z",
            "vertex_promo_gbp": 71.02,
            "vertex_usable_gbp": 70.02,
        },
        "totals": totals,
        "per_part": per_part_summary,
        "mint_order": "006 > 007 > 008 > 009 > 010 > 011 > 012 > 013 > 014 > 015 > 016 > 017 > 018 > 019 > 020 > 021 > 022 > 023 > 024 > 025 > 026 > 027 > 028 > 029 > 030 > 031 > 032 > 033 > 034 > 035 > 036 > 037 > 038 > 039 > 040 > 041 > 042 > 043 > 044 > 045 > 046 > 047 > 048 > 049 > 050 > 051 > 052 > 053 > 054 > 055 > 056 > 057 > 058 > 059. Nothing in 056 is generation_authorized.",
    }
    (EDIT / "PICTURE_PLAN_v01.json").write_text(json.dumps(plan, indent=2) + "\n")

    sl = [
        "# 056 How We Smell: The 400 Piano Keys Inside Your Nose — Shot list & plate boards v01 (pre-VO)",
        "",
        "Gemini, 19 Oct 2026, J0615. Built from `olfaction_script_master_v01.md` (`92.2 PASS`) and `SOURCES_v01.md`.",
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
        "# 056 price review v01 (pre-VO plate boards)",
        "",
        "Gemini, 19 Oct 2026, J0615. Boards only. **No mint. No spend. No merge.**",
        "Prepared from `olfaction_script_master_v01.md` (`92.2 PASS`) and `SOURCES_v01.md` so 056's full plate board rows, non-emissive Fast prompts, £0 code graphics, and Teach-on-Screen overlays are ready to re-time the moment long VO locks. Parked for Chief.",
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
        f"- **Quality ({totals['Quality']} rows):** readable faces (John E. Amoore, Linda B. Buck, Richard Axel, Robert Vassar, Peter Mombaerts, Bettina Malnic, Theodor Escherich, Élie Metchnikoff, Jeffrey Gordon), 1952 Oxford stereochemical odour models, 5 April 1991 Columbia University 1,000-gene olfactory receptor discovery, December 1994 – November 1996 1-neuron-1-receptor & glomerular convergence proof, 5 March 1999 Harvard combinatorial scent-chord & limbic memory pathway, and the 2 Explorer beats.",
        f"- **Fast ({totals['Fast']} rows, non-emissive):** daylight prop and laboratory shots (perfume flacon, coffee beans, rose petals & brass 7-helix lock model pan, 3-object callback bench, Columbia 1991 PCR tubes, restriction-digest gel & 7-transmembrane sketch, Oxford 1952 ball-and-stick odour models & carved sockets, cribriform plate sieve & colour-sorted glomerular convergence model, 5 cm² postage-stamp olfactory epithelium slide tray & microscope, 1-octanol rose/citrus vs octanoic acid goat-cheese 8-carbon models, apple/potato slices & coffee cup on museum plinth). Zero candles, flames, sparks, or glowing elements on Fast.",
        f"- **£0 code graphics ({totals['code_graphic']} rows):**",
        "  1. `P1:04_buck_axel_1991_sensory_gene_count_3_cones_vs_400_human_1000_mouse_olfactory_receptors_chart` — human sensory gene allocation comparing 3 colour-vision cone genes and ~35 taste genes against ~400 functional human (~1,000 mammalian) olfactory receptor genes (~3% of the 20,000-gene genome) (`SCALE: your eyes need just three colour genes to see the entire rainbow — yet your DNA devotes four hundred working genes, or three out of every hundred genes in your body, solely to building smell locks inside your nose`)",
        "  2. `P1:06_one_to_one_400_smells_vs_combinatorial_piano_chord_billions_of_scents_chart` — 1-to-1 lock-and-key model (400 smells) vs Malnic & Buck's combinatorial piano-chord code (400 receptors taken 3 to 5 at a time = billions of chords) (`SCALE: if each smell receptor recognised only one scent, you could smell only four hundred things — instead, your nose plays those four hundred receptors like chords on a piano, where pressing just four keys at once creates over a billion possible combinations`)",
        "  3. `P2:02_buck_axel_5_apr_1991_cell_7tm_gpcr_1000_mouse_400_human_olfactory_gene_family_chart` — Buck & Axel's 5 April 1991 7-transmembrane GPCR olfactory receptor multigene family (~1,000 rodent genes, ~390–400 functional human genes + ~460 pseudogenes = ~3% of proteome) (`SCALE: out of the roughly twenty thousand protein-coding genes that build your entire body — your heart, brain, bones, and muscles — roughly one out of every thirty genes is dedicated solely to helping you smell`)",
        "  4. `P3:02_vassar_buck_1994_and_mombaerts_axel_1996_10000_axons_to_1_glomerulus_wiring_chart` — Vassar/Buck (Dec 1994) and Mombaerts/Axel (Nov 1996) 1-neuron-1-receptor rule and ~10,000-to-1 glomerular convergence across 6–10 million nasal neurons (`SCALE: imagine ten thousand people wearing the same colour shirt scattered randomly across a packed stadium — yet when they walk out the exits, every single person in a blue shirt automatically meets at the exact same lamppost outside`)",
        "  5. `P4:02_malnic_buck_5_mar_1999_1_octanol_vs_octanoic_acid_chord_matrix_and_2_synapse_limbic_chart` — Malnic & Buck's 5 March 1999 combinatorial odorant-receptor matrix (1-octanol rose/citrus chord vs octanoic acid sweat/goat chord) and direct 2-synapse olfactory bulb → amygdala/hippocampus memory pathway (`SCALE: swapping just one oxygen atom at the tip of an eight-carbon chain is like changing one note in a major piano chord to a minor dissonance — instantly flipping the smell in your brain from fresh citrus to rancid sweat`)",
        "  6. `P5:01_timeline_1952_2004_and_retronasal_flavour_vs_5_basic_tongue_tastes_chart` — completed 4-date timeline (1952 → 2004) + retro-nasal olfaction (80% of flavour) vs 5 basic tongue tastes diagram (`SCALE: every single breath you take pulls millions of invisible airborne molecules across a postage-stamp keyboard of four hundred receptor types, playing silent chords that let you smell rain, coffee, and childhood memories in a heartbeat`)",
        f"- **£0 verified reuse ({totals['reuse']} row):** `P5:04_table_three_callback` uses the 2.40 s unused moving tail `[5.50s..7.90s]` of `P1:07_table_three_props_amoore_shape_blocks_buck_1991_pcr_gel_and_piano_chord_odorant_board`.",
        "",
        "## Mint order",
        "",
        "006 > 007 > 008 > 009 > 010 > 011 > 012 > 013 > 014 > 015 > 016 > 017 > 018 > 019 > 020 > 021 > 022 > 023 > 024 > 025 > 026 > 027 > 028 > 029 > 030 > 031 > 032 > 033 > 034 > 035 > 036 > 037 > 038 > 039 > 040 > 041 > 042 > 043 > 044 > 045 > 046 > 047 > 048 > 049 > 050 > 051 > 052 > 053 > 054 > 055 > 056 > 057 > 058 > 059. `generation_authorized` is `false` on every row.",
    ])
    (EDIT / "PRICE_REVIEW_v01.md").write_text("\n".join(pr_lines) + "\n")
    print(f"056 v01 boards written: {totals['rows']} rows, Flow expected={totals['flow_credits_expected']}")


if __name__ == "__main__":
    main()
