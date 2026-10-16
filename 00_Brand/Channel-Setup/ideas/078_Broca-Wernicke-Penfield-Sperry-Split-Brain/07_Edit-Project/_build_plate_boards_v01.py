#!/usr/bin/env python3
"""HOS 078 (Split Brain: Two Minds Inside One Human Skull) pre-VO plate boards v01. J0723. No mint, no spend.

Built from 00_Brand/Channel-Setup/ideas/078_Broca-Wernicke-Penfield-Sperry-Split-Brain/split_brain_script_master_v01.md
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
        "Part 01 — The Man Who Could Only Say 'Tan' & the Two Minds in One Skull",
        [
            ("01_two_cerebral_hemispheres_corpus_callosum_bridge_and_sperry_gazzaniga_tachistoscope_left_hand_spoon", 0.0, 5.5, "A", False, "TWO MINDS IN ONE SKULL", "Quality",
             "Quality: Short frame 0 / answer image (0:03) + side by side, a 1.4-kilogram human brain split into left and right cerebral hemispheres connected by the 200-million-axon corpus callosum bridge, while at Caltech in 1962 Roger Sperry and Michael Gazzaniga flash an image of a spoon to a split-brain patient's left visual field: the patient shakes his head while his left hand reaches behind a screen and picks up the spoon.",
             STYLE + "Split anatomical-and-laboratory scene: on the left, a cutaway human brain shows the left and right cerebral hemispheres linked by the dense white corpus callosum band; on the right, a split-brain patient seated at a divided screen shakes his head while his left hand reaches beneath the screen and lifts a silver spoon." + QUAL_TAIL,
             {"kind": "WHEN", "label": "PARIS, 18 APRIL 1861", "timeline_step": "1/3 · 18 Apr 1861 & 1874 (Paul Broca presents patient 'Tan' in Paris and Carl Wernicke maps speech comprehension, proving language is lateralized to the left hemisphere)", "hold_s": 3.5}),
            ("02_broca_1861_paris_wernicke_1874_penfield_1937_montreal_and_sperry_gazzaniga_1962_caltech_split", 5.5, 6.0, "B", False, "BROCA'S AREA, PENFIELD'S MAP, SPLIT BRAIN", "Quality",
             "Quality: complex three-part composition (Pierre Paul Broca at Bicêtre Hospital in Paris on 18 April 1861 examining the left frontal lobe of Louis Victor Leborgne alongside Carl Wernicke in Breslau in 1874; Wilder Penfield at the Montreal Neurological Institute in December 1937 placing tiny paper tickets on an awake patient's exposed cortex to map the motor and sensory homunculus; and Roger Sperry and Michael Gazzaniga at Caltech in 1962–1967 testing split-brain patient W.J. at a tachistoscope screen).",
             STYLE + "Three-panel period composition: on the left, Paul Broca in 1861 Paris holding a preserved brain specimen alongside Carl Wernicke in 1874 Breslau; in the centre, Wilder Penfield in 1937 Montreal gently touching a fine probe to an awake patient's cortex; on the right, Roger Sperry and Michael Gazzaniga in 1962 Caltech testing a patient at a tachistoscope screen." + QUAL_TAIL,
             None),
            ("03_corpus_callosum_200_million_axon_bridge_linking_left_speech_right_hand_and_right_spatial_left_hand", 11.5, 6.0, "C", False, "THE 200-MILLION-WIRE BRIDGE", "Quality",
             "Quality: complex anatomical reveal (a cross-section of the human brain shows the 200-million-axon corpus callosum superhighway linking the left hemisphere controlling speech and the right hand with the right hemisphere controlling spatial vision and the left hand, before a surgical micro-instrument parts the bridge to stop runaway seizures).",
             STYLE + "In a three-dimensional anatomical cross-section of the human brain, two hundred million white nerve fibres arch across the central corpus callosum bridge between the left and right hemispheres before parting cleanly down the midline." + QUAL_TAIL,
             {"kind": "WHEN", "label": "18 APRIL 1861 · 1874 · DECEMBER 1937 · 1962 · 1967", "timeline_step": "1/3 · 1861 & 1874 (Broca & Wernicke) · 2/3 · 1870 & Dec 1937 (Fritsch, Hitzig & Penfield) · 3/3 · 1962–1967 (Sperry, Bogen & Gazzaniga)", "hold_s": 3.5}),
            ("04_broca_1861_wernicke_1874_penfield_1937_and_sperry_gazzaniga_1962_lateralization_split_brain_chart", 17.5, 8.0, "E", False, "LEFT HEMISPHERE (BROCA 1861 & WERNICKE 1874) · PENFIELD 1937 CORTICAL HOMUNCULUS · 200M-AXON CORPUS CALLOSUM & 100-MS TACHISTOSCOPE", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked Cerebral Lateralization, Cortical Homunculus & Split-Brain Corpus Callosum chart from Paul Broca (18 April 1861 Bull. Soc. Anthropol. Paris 2: 235–238), Carl Wernicke (1874 Der aphasische Symptomencomplex), Wilder Penfield & Edwin Boldrey (December 1937 Brain 60: 389–443), and Michael Gazzaniga, Joseph Bogen & Roger Sperry (1962 PNAS 48: 1765–1769 & 1965 Brain 88: 221–236) shows left-hemisphere Broca's and Wernicke's language areas, Penfield's motor/sensory homunculus along the central sulcus, and contralateral visual/tactile pathways across the 200-million-axon corpus callosum.",
             {"kind": "DATA", "label": "BROCA (1861) & WERNICKE (1874) LEFT LANGUAGE NETWORK, PENFIELD (1937) HOMUNCULUS & SPERRY-GAZZANIGA (1962) 200M-AXON CORPUS CALLOSUM CHART", "detail": "Inked cerebral hemisphere lateralization, Penfield cortical homunculus & Sperry-Gazzaniga split-brain tachistoscope chart on period paper showing Broca's area (left inferior frontal gyrus, 1861), Wernicke's area (left superior temporal gyrus, 1874), the 200-million-axon corpus callosum, and 0.1-second left- vs right-visual-field tachistoscope responses", "scale": "the corpus callosum bridge connecting the two halves of your brain packs two hundred million nerve fibres into a band the size of a folded thumb — more wiring than all the transatlantic internet cables on Earth combined", "who_card": "Pierre Paul Broca (1824–1880) — French surgeon and anthropologist · Carl Wernicke (1848–1905) — German physician and neuroanatomist · Wilder Graves Penfield (1891–1976) — American-Canadian neurosurgeon · Roger Wolcott Sperry (1913–1994) — American neurobiologist · Michael S. Gazzaniga (born 1939) — American cognitive neuroscientist", "when_stamp": "18 April 1861 · 1874 · December 1937 · 1962 · 1967", "hold_s": 3.8}),
            ("05_broca_1861_bulletin_offprint_homunculus_sketch_and_tachistoscope_lens_barrel_pan", 25.5, 5.5, "A", False, "4 BILLION MESSAGES PER SECOND", "Fast",
             "Fast: daylight macro pan across Paul Broca's 1861 Paris anthropological society offprint, Penfield's 1937 homunculus diagram sketch, and a brass tachistoscope shutter lens on an oak bench between code graphics so two full-frame graphics never run back to back. Nothing emissive, no face.",
             STYLE + "In crisp daylight on an oak neuroanatomy bench, the camera pans smoothly across an 1861 French medical journal, a charcoal cortical map sketch, and a brass shutter lens barrel." + FAST_TAIL,
             None),
            ("06_gazzaniga_bogen_sperry_1962_pnas_1965_brain_split_brain_tachistoscope_chart", 31.0, 8.0, "E", False, "CALTECH, 1962–1967", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period parchment, an inked Roger Sperry & Michael Gazzaniga (1962 PNAS 48: 1765–1769 & 1965 Brain 88: 221–236) Split-Brain Tachistoscope & Contralateral Visual Field diagram shows a central fixation point where an image flashed for 0.1 seconds to the right visual field reaches the speaking left hemisphere (patient names 'SPOON'), while an image flashed to the left visual field reaches only the mute right hemisphere (patient says 'I saw nothing' while the left hand selects the spoon by touch).",
             {"kind": "DATA", "label": "1962 GAZZANIGA, BOGEN & SPERRY (PNAS): 0.1-S HEMIFIELD FLASH → RIGHT VISUAL FIELD (SPEECH) VS LEFT VISUAL FIELD (LEFT-HAND RETRIEVAL)", "detail": "Inked Gazzaniga, Bogen & Sperry (1962 PNAS 48: 1765–1769) split-brain left vs right visual field verbal naming vs left-hand tactile selection table on period paper", "scale": "flashing a picture for one-tenth of a second to the left side of a split-brain patient's gaze is like slipping a secret note into the right half of a house after the telephone line to the front door has been cut", "hold_s": 3.8}),
            ("07_table_three_props_1861_broca_brain_cast_1937_penfield_probe_and_1962_caltech_spoon_blocks", 39.0, 5.5, "C", False, "1861 TO 1981", "Fast",
             "Fast: daylight prop table (callback source for Part 05: Paul Broca's 1861 plaster brain cast showing the left frontal lobe lesion, Wilder Penfield's 1937 bipolar cortical stimulating probe with tiny paper tickets, and Roger Sperry's 1962 silver test spoon beside red-and-white Kohs pattern blocks). Nothing emissive.",
             STYLE + "On an oak workbench in soft window light sit three objects side by side: a painted plaster cast of a human brain hemisphere, a slender silver cortical probe beside tiny paper squares, and a silver spoon next to red-and-white wooden pattern cubes." + FAST_TAIL,
             None),
            ("08_explorer_at_raised_corpus_callosum_drawbridge_helping_right_brain_pull_left_hand_spoon_lever", 62.0, 5.5, "A", True, None, "Quality",
             "Quality: Explorer beat 1 (locked character reference, after 1:00).",
             STYLE + "Standing beside a raised wooden drawbridge between two brass control desks inside a sculpted brain model, the Explorer catches a picture card showing a spoon on the right-hand desk and pulls a brass lever that makes a mechanical left hand below lift a silver spoon while the left-hand desk operator shrugs." + EXP_TAIL,
             None),
            ("09_wilder_penfield_dec_1937_montreal_placing_paper_slips_on_awake_cortex", 67.5, 5.5, "B", False, "MAPPING THE LIVING CORTEX", "Quality",
             "Quality: readable face (at the Montreal Neurological Institute in December 1937, Wilder Penfield gently touches a 1-millivolt stimulating electrode to the exposed motor cortex of an awake patient under local anaesthesia while placing tiny paper slips along the brain).",
             STYLE + "In a 1937 Montreal neurological operating theatre, neurosurgeon Wilder Penfield holds a fine silver stimulating probe and places tiny white paper squares along the exposed cerebral cortex while his assistant sketches the map." + QUAL_TAIL,
             {"kind": "WHEN", "label": "MONTREAL, DECEMBER 1937", "timeline_step": "2/3 · December 1937 (Wilder Penfield and Edwin Boldrey map the motor and sensory cortical homunculus in awake patients)", "hold_s": 3.5}),
        ],
    ),
    (
        2,
        "Part 02 — 18 April 1861 & 1874: Patient 'Tan', Paul Broca's Left Frontal Lobe & Carl Wernicke's Two-Part Language Engine",
        [
            ("01_paul_broca_18_apr_1861_paris_patient_tan_brain_and_carl_wernicke_1874_breslau", 73.0, 6.5, "A", False, "PATIENT SAID ONLY 'TAN'", "Quality",
             "Quality: readable faces (French surgeon Pierre Paul Broca at Bicêtre Hospital in Paris on 12–18 April 1861 examining Louis Victor Leborgne 'Tan' and presenting the preserved brain showing the left third frontal convolution lesion on 18 April 1861, dissolving to 26-year-old German physician Carl Wernicke in Breslau in 1874 mapping the left superior temporal comprehension centre).",
             STYLE + "Split period scene: on the left in 1861 Paris, surgeon Paul Broca points to the lesion on the left frontal lobe of a preserved brain specimen before colleagues; on the right in 1874 Breslau, young physician Carl Wernicke traces the left temporal speech pathway on a brain model." + QUAL_TAIL,
             {"kind": "FACT", "label": "Patient said only 'Tan'", "who_card": "Pierre Flourens (1794–1867) — French physiologist", "when_stamp": "12 April 1861 · 17 April 1861 · 18 April 1861 · 1865 · 1874", "timeline_step": "1/3 · 18 Apr 1861 & 1874 (Broca presents patient 'Tan' and Wernicke maps comprehension, proving left-hemisphere language lateralization)", "hold_s": 3.8}),
            ("02_broca_1861_1865_and_wernicke_1874_left_hemisphere_language_arcuate_fasciculus_chart", 79.5, 8.0, "E", False, "18 APR 1861 & 1865 BROCA (BULL. SOC. ANTHROPOL. PARIS: LEFT FRONTAL SPEECH) & 1874 WERNICKE (LEFT TEMPORAL COMPREHENSION)", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked Paul Broca (18 April 1861 Bull. Soc. Anthropol. Paris 2: 235–238 & 1865 Bull. Soc. Anthropol. Paris 6: 377–393) and Carl Wernicke (1874 Der aphasische Symptomencomplex) left-hemisphere language network diagram showing Broca's area (speech production, left inferior frontal gyrus), Wernicke's area (speech comprehension, left superior temporal gyrus), and the arcuate fasciculus pathway.",
             {"kind": "DATA", "label": "1861/1865 BROCA'S AREA (LEFT FRONTAL SPEECH PRODUCTION) & 1874 WERNICKE'S AREA (LEFT TEMPORAL COMPREHENSION) NETWORK", "detail": "Inked Paul Broca (18 April 1861 Bull. Soc. Anthropol. Paris 2: 235–238 & 1865 Bull. Soc. Anthropol. Paris 6: 377–393) and Carl Wernicke (1874 Der aphasische Symptomencomplex) left-hemisphere language network diagram showing Broca's area (speech production, left inferior frontal gyrus), Wernicke's area (speech comprehension, left superior temporal gyrus), and the arcuate fasciculus pathway on period paper", "scale": "Paul Broca and Carl Wernicke proved that speaking a single sentence is like a two-room telegraph office in the left half of your brain — Wernicke's room writes the message in words, and Broca's room taps it out to your mouth", "hold_s": 3.8}),
            ("03_paris_1861_preserved_leborgne_left_frontal_lesion_specimen_jar_and_1874_wernicke_monograph_closeup", 87.5, 6.5, "B", False, "18 APRIL 1861 — BROCA'S AREA DISCOVERED", "Fast",
             "Fast: daylight macro shot of Paul Broca's 1861 glass specimen jar containing the preserved left frontal lobe lesion of Louis Victor Leborgne beside Carl Wernicke's 1874 Breslau monograph and brass callipers on a bench. Nothing emissive, no face.",
             STYLE + "In crisp daylight on a nineteenth-century Paris anatomy bench, a glass specimen jar holding a preserved human brain sits beside brass callipers and an open 1874 neuroanatomy monograph." + FAST_TAIL,
             None),
            ("04_cutaway_left_hemisphere_model_showing_broca_area_wernicke_area_and_arcuate_fasciculus_bundle_pan", 94.0, 5.5, "C", False, "WE SPEAK WITH THE LEFT HEMISPHERE", "Fast",
             "Fast: daylight close-up pan across a sculpted anatomical model of the left cerebral hemisphere highlighting the inferior frontal Broca's region, the superior temporal Wernicke's region, and the curved arcuate fibre bundle connecting them on an oak table. Nothing emissive, no face.",
             STYLE + "In bright window light on an oak table, a sculpted cutaway model of the left cerebral hemisphere displays the frontal speech hub and temporal comprehension hub linked by an arched white fibre bundle." + FAST_TAIL,
             None),
        ],
    ),
    (
        3,
        "Part 03 — 1870 & December 1937: Fritsch & Hitzig's Crossed Wires and Wilder Penfield's Awake Cortical Homunculus",
        [
            ("01_fritsch_hitzig_1870_berlin_motor_cortex_and_penfield_boldrey_dec_1937_montreal_homunculus", 99.5, 6.5, "A", False, "BRAIN FEELS ZERO DIRECT PAIN", "Quality",
             "Quality: readable faces (German physiologists Gustav Fritsch and Eduard Hitzig in Berlin in 1870 stimulating the motor cortex to prove contralateral movement, dissolving to neurosurgeon Wilder Graves Penfield and Edwin Boldrey in Montreal in December 1937 placing tiny paper slips across the exposed cortex of an awake patient to map the motor and sensory homunculus).",
             STYLE + "Split period scene: on the left in 1870 Berlin, Gustav Fritsch and Eduard Hitzig test a fine galvanic wire probe on a cortical model; on the right in 1937 Montreal, Wilder Penfield and Edwin Boldrey map the exposed motor strip beside a sculpted giant-handed homunculus figure." + QUAL_TAIL,
             {"kind": "FACT", "label": "Brain feels zero direct pain", "who_card": "Gustav Fritsch (1838–1927) — German physiologist · Eduard Hitzig (1838–1907) — German neuropsychiatrist · Edwin Boldrey (1906–1988) — American neurosurgeon", "when_stamp": "1870 · December 1937", "timeline_step": "2/3 · 1870 & Dec 1937 (Fritsch & Hitzig prove contralateral motor cortex control; Penfield & Boldrey map the awake cortical homunculus)", "hold_s": 3.8}),
            ("02_penfield_boldrey_dec_1937_brain_motor_and_sensory_cortical_homunculus_chart", 106.0, 8.0, "E", False, "DEC 1937 PENFIELD & BOLDREY (BRAIN): AWAKE CORTICAL STIMULATION & DISPROPORTIONATE MOTOR/SENSORY HOMUNCULUS (GIANT HANDS & LIPS)", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked Wilder Penfield & Edwin Boldrey (December 1937 Brain 60: 389–443) motor and sensory cortical homunculus chart comparing true anatomical body-surface percentage vs cortical representation area (giant thumb/hand, lips & tongue vs tiny trunk/legs) along the precentral and postcentral gyri.",
             {"kind": "DATA", "label": "DEC 1937 PENFIELD & BOLDREY (BRAIN): MOTOR & SENSORY CORTICAL HOMUNCULUS PROPORTIONS (GIANT THUMB, HAND, LIPS & TONGUE VS TRUNK)", "detail": "Inked Wilder Penfield & Edwin Boldrey (December 1937 Brain 60: 389–443) motor and sensory cortical homunculus chart on period paper comparing true anatomical body-surface percentage vs cortical representation area (giant thumb/hand, lips & tongue vs tiny trunk/legs) along the precentral and postcentral gyri", "scale": "on the sensory map inside your brain, your two thumbs and your lips take up more cortical real estate than your entire chest, back, and legs combined — because your brain allocates space by precision, not size", "hold_s": 3.8}),
            ("03_montreal_1937_cortical_probe_paper_tickets_and_3d_sculpted_homunculus_model_closeup", 114.0, 6.5, "B", False, "DECEMBER 1937 — PENFIELD'S CORTICAL HOMUNCULUS", "Fast",
             "Fast: daylight macro shot of Wilder Penfield's bipolar stimulating electrode and tiny paper tickets beside a sculpted three-dimensional cortical homunculus figure with giant hands, thumbs, and lips on a bench. Nothing emissive, no face.",
             STYLE + "In crisp daylight on a 1937 Montreal laboratory bench, a slender silver cortical probe and tiny white paper squares sit beside a sculpted homunculus figure with enormous hands and lips." + FAST_TAIL,
             None),
            ("04_precentral_motor_and_postcentral_sensory_gyrus_arch_model_on_oak_table_pan", 120.5, 5.5, "C", False, "CONTRALATERAL MOTOR & SENSORY STRIPS", "Fast",
             "Fast: daylight close-up pan across a sculpted anatomical arch model of the precentral motor gyrus and postcentral somatosensory gyrus draped with miniature hand, face, and foot emblems on an oak table. Nothing emissive, no face.",
             STYLE + "In bright window light on an oak table, a sculpted coronal brain-arch model shows the motor and sensory cortical strips mapped with miniature sculpted hands, lips, and feet." + FAST_TAIL,
             None),
        ],
    ),
    (
        4,
        "Part 04 — 1962–1967: Roger Sperry, Michael Gazzaniga & the Split-Brain Midpoint Twist",
        [
            ("01_roger_sperry_and_michael_gazzaniga_1962_1967_caltech_split_brain_tachistoscope_patient_wj", 126.0, 6.5, "A", False, "LEFT HAND KNEW SECRET", "Quality",
             "Quality: readable faces (American neurobiologist Roger Wolcott Sperry and graduate student Michael S. Gazzaniga at Caltech in 1962–1967 testing split-brain patient W.J. at a 0.1-second tachistoscope screen where the right hemisphere guides the left hand to pick up a hidden spoon while the speaking left hemisphere claims it saw nothing).",
             STYLE + "In a 1962 Caltech laboratory in Pasadena, Roger Sperry and young Michael Gazzaniga observe a split-brain patient seated at a tachistoscope screen as his left hand reaches behind the curtain to select a spoon." + QUAL_TAIL,
             {"kind": "FACT", "label": "Left hand knew secret", "who_card": "Joseph E. Bogen (1926–2005) — American neurosurgeon", "when_stamp": "1953 · 15 October 1962 · 1965 · 1967 · 8 December 1981", "timeline_step": "3/3 · 1962–1981 (Roger Sperry, Joseph Bogen, and Michael Gazzaniga test split-brain patients at Caltech, winning the 1981 Nobel Prize)", "hold_s": 3.8}),
            ("02_gazzaniga_bogen_sperry_1962_1965_split_brain_hemifield_and_left_brain_interpreter_chart", 132.5, 8.0, "E", False, "15 OCT 1962 PNAS & 1965 BRAIN (GAZZANIGA, BOGEN & SPERRY): 100-MS TACHISTOSCOPE, RIGHT-HAND VS LEFT-HAND BLOCKS & LEFT-BRAIN INTERPRETER", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked Gazzaniga, Bogen & Sperry (1962 PNAS 48: 1765–1769 & 1965 Brain 88: 221–236) split-brain lateralized tachistoscope & Left-Brain Interpreter diagram showing 100-ms hemifield presentation, 100% verbal naming for right visual field vs 0% verbal naming + accurate left-hand retrieval for left visual field, and superior left-hand spatial block construction.",
             {"kind": "DATA", "label": "1962–1967 SPERRY & GAZZANIGA SPLIT-BRAIN CHART: 100-MS FLASH, LEFT-HAND KOHS SPATIAL BLOCKS & CHICKEN-SHOVEL LEFT-BRAIN INTERPRETER", "detail": "Inked Gazzaniga, Bogen & Sperry (1962 PNAS 48: 1765–1769 & 1965 Brain 88: 221–236) split-brain lateralized tachistoscope & Left-Brain Interpreter diagram on period paper showing 100-ms hemifield presentation, 100% verbal naming for right visual field vs 0% verbal naming + accurate left-hand retrieval for left visual field, and superior left-hand spatial block construction", "scale": "flashing a secret command to the right half of a split-brain patient's brain and watching the left hand obey while the mouth invents an excuse proved that your left brain has a built-in press secretary that makes up a sensible story whenever it doesn't know why you did something", "hold_s": 3.8}),
            ("03_caltech_1962_tachistoscope_screen_hidden_spoon_tray_and_kohs_pattern_blocks_closeup", 140.5, 6.5, "B", False, "1962 — SPERRY & GAZZANIGA PROVE SPLIT-BRAIN CONSCIOUSNESS", "Fast",
             "Fast: daylight macro shot of the Caltech divided tachistoscope screen with its veiled tactile object tray (spoon, key, pencil) beside red-and-white Kohs spatial pattern blocks on a workbench. Nothing emissive, no face.",
             STYLE + "In crisp daylight on a 1962 Caltech psychology table, a divided viewing screen with a curtained hand slot revealing a spoon and key sits beside red-and-white wooden pattern blocks." + FAST_TAIL,
             None),
            ("04_explorer_flashing_snow_and_chicken_cards_at_split_desk_as_left_hand_grabs_shovel", 147.0, 5.5, "B", True, None, "Quality",
             "Quality: Explorer beat 2 (locked character reference).",
             STYLE + "Sitting behind a divided wooden tachistoscope desk, the Explorer holds up a picture of a snowstorm on one side and a chicken claw on the other as a mechanical left hand grabs a miniature snow shovel and a right hand points to a toy chicken." + EXP_TAIL,
             None),
        ],
    ),
    (
        5,
        "Part 05 — Why the 'Left-Brain vs Right-Brain' Myth Is Wrong — & How Your Skeleton Rebuilds Itself Every 10 Years",
        [
            ("01_timeline_1861_1981_and_integrated_two_hemisphere_corpus_callosum_chart", 152.5, 8.5, "E", False, "1861–1981 TIMELINE · BROCA & WERNICKE LEFT SPEECH, PENFIELD HOMUNCULUS & SPERRY-GAZZANIGA 200M-AXON CORPUS CALLOSUM", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, the 3-era timeline completes: 18 Apr 1861 & 1874 (Paul Broca presents patient 'Tan' in Paris and Carl Wernicke maps speech comprehension, proving language is lateralized to the left hemisphere) · 1870 & Dec 1937 (Fritsch & Hitzig discover contralateral motor cortex control in Berlin and Wilder Penfield maps the motor and sensory homunculus in awake patients in Montreal) · 1962–1981 (Roger Sperry and Michael Gazzaniga test split-brain patients at Caltech, proving the 200-million-axon corpus callosum unites two specialized hemispheres and winning the 1981 Nobel Prize).",
             {"kind": "DATA", "label": "1861–1981 CEREBRAL HEMISPHERES, HOMUNCULUS & SPLIT-BRAIN TIMELINE · BROCA, WERNICKE, PENFIELD, SPERRY & GAZZANIGA", "detail": "Animated timeline (1861 → 1981) alongside an inked summary of left-hemisphere language lateralization, the cortical homunculus, and 200-million-axon corpus callosum integration", "scale": "from a Paris hospital patient who could only say 'Tan' to numbered paper tickets on an awake brain and a 0.1-second flash screen at Caltech, scientists discovered how two hemispheres weave one human mind", "when_stamp": "1861–1981", "timeline_step": "3/3 · 1861–1981 timeline complete", "hold_s": 3.8}),
            ("02_intact_two_hemisphere_brain_model_beside_Protective_human_skull_and_femur_on_plinth_pan", 161.0, 5.5, "A", False, "200 MILLION FIBRES UNITING BOTH HEMISPHERES", "Fast",
             "Fast: daylight close-up of an intact two-hemisphere human brain model showing the corpus callosum beside a protective human skull and sectioned femur showing trabecular bone arches on a wooden museum plinth. Nothing emissive, no face.",
             STYLE + "In crisp daylight on a wooden museum plinth, a sculpted two-hemisphere brain model sits beside a cutaway human skull and a sectioned thighbone revealing internal bone arches." + FAST_TAIL,
             None),
            ("03_belchier_1736_red_madder_pig_bones_kolliker_1873_wolff_1892_crane_femur_and_chick_1922_vitamin_d_handoff", 166.5, 6.5, "C", False, "BONE REMODELLING, WOLFF'S LAW & VITAMIN D", "Quality",
             "Quality: readable faces (John Belchier in London in 1736 and Duhamel du Monceau in 1739 examining crimson madder-dyed bone rings alongside Albert von Kölliker in 1873, Karl Culmann and Julius Wolff in 1866–1892 comparing a human femur to an iron crane, and Harriette Chick in 1922 Vienna curing rickets with cod-liver oil and sunlight — handoff to 079 Bone Remodelling, Wolff's Law & Vitamin D).",
             STYLE + "Split period scene: on the left, John Belchier in 1736 London and Duhamel du Monceau with red-and-white ringed bones beside Julius Wolff comparing a sectioned femur to an iron harbour crane; on the right, Harriette Chick in 1922 Vienna examining infant wrist X-rays on a sunny hospital veranda." + QUAL_TAIL,
             {"kind": "WHEN", "label": "1736 · 1739 · 1866 · 1873 · 1892 · 1922", "hold_s": 3.5}),
            ("04_table_three_callback", 173.0, 2.4, "C", False, None, "reuse",
             "Reuse: verified unused moving window [5.50s..7.90s] of P1:07_table_three_props_1861_broca_brain_cast_1937_penfield_probe_and_1962_caltech_spoon_blocks (callback, £0).",
             "Reuse P1:07_table_three_props_1861_broca_brain_cast_1937_penfield_probe_and_1962_caltech_spoon_blocks [5.50s..7.90s] (2.40s distinct non-overlapping tail window from 8.00s source clip).",
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
                row["reuse_of"] = "P1:07_table_three_props_1861_broca_brain_cast_1937_penfield_probe_and_1962_caltech_spoon_blocks"
                row["reuse_window_s"] = [5.5, 7.9]
                row["reuse_audit"] = {
                    "source_row": "P1:07_table_three_props_1861_broca_brain_cast_1937_penfield_probe_and_1962_caltech_spoon_blocks",
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
            "film": "078_Broca-Wernicke-Penfield-Sperry-Split-Brain",
            "part": p_idx,
            "title": p_title,
            "version": "v01",
            "timing_status": "pre_vo_script_clock (built from split_brain_script_master_v01.md; retimes onto Scribe STT once VO locks)",
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
        "film": "078_Broca-Wernicke-Penfield-Sperry-Split-Brain",
        "version": "v01",
        "date": "2026-10-20",
        "owner": "gemini (J0723)",
        "status": "PRE_VO_BOARDS_V01_NO_MINT",
        "generation_authorized": False,
        "script": "00_Brand/Channel-Setup/ideas/078_Broca-Wernicke-Penfield-Sperry-Split-Brain/split_brain_script_master_v01.md",
        "sources": "00_Brand/Channel-Setup/ideas/078_Broca-Wernicke-Penfield-Sperry-Split-Brain/SOURCES_v01.md",
        "credit_snapshot": {
            "flow_balance": 23740,
            "flow_floor": 0,
            "flow_read_at": "2026-10-15T21:42:22Z",
            "vertex_promo_gbp": 71.02,
            "vertex_usable_gbp": 70.02,
        },
        "totals": totals,
        "per_part": per_part_summary,
        "mint_order": "006 > 007 > 008 > 009 > 010 > 011 > 012 > 013 > 014 > 015 > 016 > 017 > 018 > 019 > 020 > 021 > 022 > 023 > 024 > 025 > 026 > 027 > 028 > 029 > 030 > 031 > 032 > 033 > 034 > 035 > 036 > 037 > 038 > 039 > 040 > 041 > 042 > 043 > 044 > 045 > 046 > 047 > 048 > 049 > 050 > 051 > 052 > 053 > 054 > 055 > 056 > 057 > 058 > 059 > 060 > 061 > 062 > 063 > 064 > 065 > 066 > 067 > 068 > 069 > 070 > 071 > 072 > 073 > 074 > 075 > 076 > 077 > 078 > 079 > 080. Nothing in 078 is generation_authorized.",
    }
    (EDIT / "PICTURE_PLAN_v01.json").write_text(json.dumps(plan, indent=2) + "\n")

    sl = [
        "# 078 Split Brain: Two Minds Inside One Human Skull — Shot list & plate boards v01 (pre-VO)",
        "",
        "Gemini, 20 Oct 2026, J0723. Built from `split_brain_script_master_v01.md` (`91.8/100 PASS`) and `SOURCES_v01.md`.",
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
        "# 078 price review v01 (pre-VO plate boards)",
        "",
        "Gemini, 20 Oct 2026, J0723. Boards only. **No mint. No spend. No merge.**",
        "Prepared from `split_brain_script_master_v01.md` (`91.8/100 PASS`) and `SOURCES_v01.md` so 078's full plate board rows, non-emissive Fast prompts, £0 code graphics, and Teach-on-Screen overlays are ready to re-time the moment long VO locks. Parked for Chief.",
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
        f"- **Quality ({totals['Quality']} rows):** readable faces (Pierre Paul Broca, Carl Wernicke, Pierre Flourens, Gustav Fritsch, Eduard Hitzig, Wilder Graves Penfield, Edwin Boldrey, Roger Wolcott Sperry, Michael S. Gazzaniga, Joseph E. Bogen, John Belchier, Henri-Louis Duhamel du Monceau, Julius Wolff, Harriette Chick), 18 April 1861 Paris patient `'Tan'` left frontal lobe & 1874 Breslau `Wernicke's area`, December 1937 Montreal awake cortical `homunculus` stimulation, 1962–1967 Caltech `0.1 s` tachistoscope `split-brain` experiments, and the 2 Explorer beats.",
        f"- **Fast ({totals['Fast']} rows, non-emissive):** daylight prop and laboratory shots (1861 Broca bulletin offprint, 1937 homunculus sketch & brass tachistoscope shutter pan, 3-object callback bench, 1861 preserved brain jar & 1874 Wernicke monograph, sculpted cutaway left hemisphere language model, 1937 Montreal cortical probe with paper tickets & 3D sculpted homunculus model, precentral/postcentral cortical arch model, 1962 Caltech divided tachistoscope screen with hidden spoon tray & Kohs pattern blocks, intact two-hemisphere brain model beside skull and sectioned femur on museum plinth). Zero candles, flames, sparks, or glowing elements on Fast.",
        f"- **£0 code graphics ({totals['code_graphic']} rows):**",
        "  1. `P1:04_broca_1861_wernicke_1874_penfield_1937_and_sperry_gazzaniga_1962_lateralization_split_brain_chart` — Broca's area (1861), Wernicke's area (1874), Penfield's `homunculus` (1937), and the `200-million-axon` `corpus callosum` (`SCALE: the corpus callosum bridge connecting the two halves of your brain packs two hundred million nerve fibres into a band the size of a folded thumb — more wiring than all the transatlantic internet cables on Earth combined`)",
        "  2. `P1:06_gazzaniga_bogen_sperry_1962_pnas_1965_brain_split_brain_tachistoscope_chart` — Gazzaniga, Bogen & Sperry (1962 *PNAS* & 1965 *Brain*) `0.1 s` (`100 ms`) left vs right visual field tachistoscope table (`SCALE: flashing a picture for one-tenth of a second to the left side of a split-brain patient's gaze is like slipping a secret note into the right half of a house after the telephone line to the front door has been cut`)",
        "  3. `P2:02_broca_1861_1865_and_wernicke_1874_left_hemisphere_language_arcuate_fasciculus_chart` — Paul Broca (18 April 1861 & 1865) and Carl Wernicke (1874) left-hemisphere language network & arcuate fasciculus diagram (`SCALE: Paul Broca and Carl Wernicke proved that speaking a single sentence is like a two-room telegraph office in the left half of your brain — Wernicke's room writes the message in words, and Broca's room taps it out to your mouth`)",
        "  4. `P3:02_penfield_boldrey_dec_1937_brain_motor_and_sensory_cortical_homunculus_chart` — Wilder Penfield & Edwin Boldrey (December 1937 *Brain*) motor and sensory cortical `homunculus` proportions (`SCALE: on the sensory map inside your brain, your two thumbs and your lips take up more cortical real estate than your entire chest, back, and legs combined — because your brain allocates space by precision, not size`)",
        "  5. `P4:02_gazzaniga_bogen_sperry_1962_1965_split_brain_hemifield_and_left_brain_interpreter_chart` — Sperry & Gazzaniga (1962–1967) split-brain lateralized tachistoscope, Kohs block superiority & `Left-Brain Interpreter` chart (`SCALE: flashing a secret command to the right half of a split-brain patient's brain and watching the left hand obey while the mouth invents an excuse proved that your left brain has a built-in press secretary that makes up a sensible story whenever it doesn't know why you did something`)",
        "  6. `P5:01_timeline_1861_1981_and_integrated_two_hemisphere_corpus_callosum_chart` — completed timeline (1861 → 1981) + left language lateralization, cortical homunculus & `200-million-axon` corpus callosum integration (`SCALE: from a Paris hospital patient who could only say 'Tan' to numbered paper tickets on an awake brain and a 0.1-second flash screen at Caltech, scientists discovered how two hemispheres weave one human mind`)",
        f"- **£0 verified reuse ({totals['reuse']} row):** `P5:04_table_three_callback` uses the 2.40 s unused moving tail `[5.50s..7.90s]` of `P1:07_table_three_props_1861_broca_brain_cast_1937_penfield_probe_and_1962_caltech_spoon_blocks`.",
        "",
        "## Mint order",
        "",
        "006 > 007 > 008 > 009 > 010 > 011 > 012 > 013 > 014 > 015 > 016 > 017 > 018 > 019 > 020 > 021 > 022 > 023 > 024 > 025 > 026 > 027 > 028 > 029 > 030 > 031 > 032 > 033 > 034 > 035 > 036 > 037 > 038 > 039 > 040 > 041 > 042 > 043 > 044 > 045 > 046 > 047 > 048 > 049 > 050 > 051 > 052 > 053 > 054 > 055 > 056 > 057 > 058 > 059 > 060 > 061 > 062 > 063 > 064 > 065 > 066 > 067 > 068 > 069 > 070 > 071 > 072 > 073 > 074 > 075 > 076 > 077 > 078 > 079 > 080. `generation_authorized` is `false` on every row.",
    ])
    (EDIT / "PRICE_REVIEW_v01.md").write_text("\n".join(pr_lines) + "\n")
    print(f"078 v01 boards written: {totals['rows']} rows, Flow expected={totals['flow_credits_expected']}")


if __name__ == "__main__":
    main()
