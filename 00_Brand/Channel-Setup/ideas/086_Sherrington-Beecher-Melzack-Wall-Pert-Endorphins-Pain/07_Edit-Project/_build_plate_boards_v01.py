#!/usr/bin/env python3
"""HOS 086 (Endorphins: How Your Brain Makes Its Own Morphine) pre-VO plate boards v01. J0805. No mint, no spend.

Built from 00_Brand/Channel-Setup/ideas/086_Sherrington-Beecher-Melzack-Wall-Pert-Endorphins-Pain/pain_endorphins_script_master_v01.md
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
        "Part 01 — The Stubbed Toe Reflex, the Anzio Beachhead Paradox & the Brain's Own Morphine",
        [
            ("01_spinal_dorsal_horn_pain_gate_and_beecher_1944_anzio_beachhead_tent_endorphin_receptors", 0.0, 5.5, "A", False, "THE PAIN GATE & ENDORPHINS", "Quality",
             "Quality: Short frame 0 / answer image (0:03) + side by side, in a spinal cord dorsal horn cross-section fast blue A-beta touch signals from rubbing a bumped shin slam a neural gate shut in front of slow red C-fibre pain signals, beside Harvard doctor Henry Knowles Beecher in a medical tent on the Anzio beachhead in Italy in February 1944 speaking with a calm wounded soldier who waves away a morphine syringe while golden endorphin molecules lock onto opioid receptors in the brain.",
             STYLE + "Split anatomical-and-historical scene: on the left, a cutaway spinal cord dorsal horn shows fast blue touch nerve signals swinging a brass gate shut in front of slow red pain nerve fibres; on the right in a 1944 Anzio medical tent, physician Henry Beecher talks with a calm wounded soldier on a cot who waves away a morphine syringe." + QUAL_TAIL,
             {"kind": "WHEN", "label": "ANZIO, ITALY, FEBRUARY 1944", "timeline_step": "1/3 · 1664, 1906 & 1944–1955 (Replacing Descartes's bell-rope myth, Charles Sherrington discovers nociceptors, and Henry Knowles Beecher on the Anzio beachhead discovers stress analgesia and the placebo effect)", "hold_s": 3.5}),
            ("02_sherrington_1906_beecher_1944_melzack_wall_1965_mit_gate_and_pert_snyder_kosterlitz_1973_1975_split", 5.5, 6.0, "B", False, "NOCICEPTORS, SPINAL GATE, ENDORPHINS", "Quality",
             "Quality: complex three-part composition (Charles Scott Sherrington at Liverpool and Oxford in 1906 mapping nociceptors and Henry Knowles Beecher at Anzio in 1944; Ronald Melzack and Patrick Wall at MIT on 19 November 1965 unveiling the Gate Control Theory of Pain; and Candace Pert and Solomon Snyder at Johns Hopkins in March 1973 with John Hughes and Hans Kosterlitz in Aberdeen in December 1975 isolating opioid receptors and enkephalins/endorphins).",
             STYLE + "Three-panel period composition: on the left, Charles Sherrington in 1906 Oxford beside Henry Beecher in 1944 Anzio; in the centre, Ronald Melzack and Patrick Wall at 1965 MIT pointing to their spinal dorsal horn gate diagram; on the right, Candace Pert and Solomon Snyder in 1973 Baltimore alongside Hans Kosterlitz and John Hughes in 1975 Aberdeen." + QUAL_TAIL,
             None),
            ("03_fast_a_delta_20ms_sharp_pain_flash_vs_slow_c_fibre_1ms_throbbing_ache_comparison", 11.5, 6.0, "C", False, "FAST FLASH vs SLOW ACHE", "Quality",
             "Quality: complex physiological reveal (a split comparison of a hand pulling back from a hot pan in 0.1 seconds as fast myelinated A-delta fibres at 20 m/s trigger the sharp first flash of pain followed 1 second later by slow unmyelinated C fibres at 1 m/s carrying the deep throbbing ache, vs the tissue injury that occurs when nociceptor alarms are missing).",
             STYLE + "In a cutaway anatomical nerve comparison, a hand pulls back from a hot iron pan as a thick insulated A-delta nerve cable carries a fast sharp pulse to the spine while a thin uninsulated C-fibre cable carries a slow second wave behind it." + QUAL_TAIL,
             {"kind": "WHEN", "label": "1906 · 1944 · 1955 · 19 NOVEMBER 1965 · 9 MARCH 1973 · 18 DECEMBER 1975", "timeline_step": "1/3 · 1906 & 1944–1955 (Sherrington & Beecher) · 2/3 · 19 Nov 1965 (Melzack & Wall) · 3/3 · 1973 & 1975 (Pert, Snyder, Hughes & Kosterlitz)", "hold_s": 3.5}),
            ("04_sherrington_1906_melzack_wall_1965_gate_control_and_pert_kosterlitz_1973_1975_endorphin_chart", 17.5, 8.0, "E", False, "MELZACK & WALL (1965): A-BETA TOUCH (35–75 M/S) CLOSES SPINAL GATE AGAINST A-DELTA (5–30 M/S) & C-FIBRE (0.5–2 M/S) PAIN", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked Nociception, Spinal Gate Control & Endogenous Opioid Analgesia chart from Charles Sherrington (1906 The Integrative Action of the Nervous System), Henry Beecher (1946 Ann. Surg. 123: 96–105 & 1955 JAMA 159: 1602–1606), Ronald Melzack & Patrick Wall (19 November 1965 Science 150: 971–979), Candace Pert & Solomon Snyder (9 March 1973 Science 179: 1011–1014), and John Hughes & Hans Kosterlitz (18 December 1975 Nature 258: 577–579) shows 1) Peripheral A-delta (5–30 m/s) and C-fibre (0.5–2 m/s) nociceptors; 2) Spinal dorsal horn substantia gelatinosa (SG) inhibitory gate closed by fast A-beta touch fibres (35–75 m/s); and 3) Descending brainstem analgesia releasing endogenous enkephalins/endorphins onto mu/delta opioid receptors.",
             {"kind": "DATA", "label": "1965 MELZACK & WALL NERVE CONDUCTION VELOCITY (A-BETA 35–75 M/S VS A-DELTA 5–30 M/S VS C-FIBRE 0.5–2 M/S) & SPINAL GATE CHART", "detail": "Inked Melzack & Wall (1965) nerve conduction velocity comparison (A-beta touch fibres 35–75 m/s vs A-delta sharp pain 5–30 m/s vs C-fibre throbbing pain 0.5–2 m/s) & spinal dorsal horn Gate Control circuit on period paper", "scale": "your touch nerves race up to your spine at seventy-five metres per second — as fast as an express train — while your throbbing pain nerves crawl at just one metre per second, a walking pace, so rubbing a bumped shin lets the touch signals reach your spinal cord first and slam the gate shut before the pain arrives", "who_card": "Charles Scott Sherrington (1857–1952) — British neurophysiologist · Henry Knowles Beecher (1904–1976) — American anaesthesiologist and researcher · Ronald Melzack (1929–2019) — Canadian psychologist · Patrick David Wall (1925–2001) — British neuroscientist · Candace Beebe Pert (1946–2013) — American neuroscientist and pharmacologist · Solomon Halbert Snyder (born 1938) — American neuroscientist · John Hughes (born 1942) — British pharmacologist · Hans Walter Kosterlitz (1903–1996) — German-British pharmacologist", "when_stamp": "1906 · 1944 · 1955 · 19 November 1965 · 9 March 1973 · 18 December 1975", "hold_s": 3.8}),
            ("05_sherrington_1906_book_1965_science_gate_diagram_and_opium_poppy_capsule_vial_pan", 25.5, 5.5, "A", False, "THE BRAIN'S OWN PAINKILLER", "Fast",
             "Fast: daylight macro pan across Charles Sherrington's 1906 The Integrative Action of the Nervous System, the 19 November 1965 Science Gate Control diagram, and a dried opium poppy seed capsule beside a glass vial on an oak bench between code graphics so two full-frame graphics never run back to back. Nothing emissive, no face.",
             STYLE + "In crisp daylight on an oak neurophysiology bench, the camera pans smoothly across an open 1906 neuroscience volume, a 1965 spinal gate circuit page, and a dried poppy seed pod beside a stoppered glass vial." + FAST_TAIL,
             None),
            ("06_beecher_1946_anzio_morphine_demand_and_pert_snyder_kosterlitz_1973_1975_opioid_endorphin_chart", 31.0, 8.0, "E", False, "BALTIMORE & ABERDEEN, 1973–1975", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period parchment, an inked Candace Pert & Solomon Snyder (9 March 1973 Science 179: 1011–1014) Stereospecific Opioid Receptor Binding & Hughes/Kosterlitz (18 December 1975 Nature 258: 577–579) Met-Enkephalin / Leu-Enkephalin Pentapeptide Structure diagram compares plant morphine with the brain's 5-amino-acid enkephalin and 31-amino-acid beta-endorphin keys locking into the same mu-opioid receptor alongside Henry Beecher's (1946) Anzio battlefield (~25%) vs civilian surgical (>80%) morphine demand.",
             {"kind": "DATA", "label": "1946 BEECHER ANZIO MORPHINE DEMAND (~25% VS >80% CIVILIAN) & 1973–1975 PERT/SNYDER/KOSTERLITZ OPIOID RECEPTOR & ENDORPHIN CHART", "detail": "Inked Beecher (1946) Anzio battlefield vs civilian surgical morphine demand (only ~25% of severely wounded Anzio soldiers requested morphine vs >80% of civilian surgical patients) & Pert/Snyder/Kosterlitz (1973–1975) opioid receptor / endorphin lock-and-key chart on period paper", "scale": "molecule for molecule, your brain's own beta-endorphin is eighteen to thirty times more potent at silencing pain than hospital morphine — and your brainstem can flood your spinal cord with it in seconds during a crisis", "hold_s": 3.8}),
            ("07_table_three_props_1906_kymograph_drum_1965_spinal_gate_model_and_1973_filtration_manifold_vials", 39.0, 5.5, "C", False, "1906 TO 1975", "Fast",
             "Fast: daylight prop table (callback source for Part 05: Sherrington's 1906 smoked-paper reflex kymograph drum, Melzack and Wall's 1965 brass-and-wood spinal dorsal horn gate model, and Pert and Snyder's 1973 vacuum filtration manifold with glass scintillation vials). Nothing emissive.",
             STYLE + "On an oak workbench in soft window light sit three objects side by side: a brass reflex kymograph drum, a wooden-and-brass spinal gate demonstrator, and a multi-port stainless-steel filter manifold beside small glass vials." + FAST_TAIL,
             None),
            ("08_explorer_swinging_spinal_dorsal_horn_gate_shut_with_fast_touch_cable_and_locking_it_with_endorphin_key", 62.0, 5.5, "A", True, None, "Quality",
             "Quality: Explorer beat 1 (locked character reference, after 1:00).",
             STYLE + "Standing beside a giant sculpted spinal cord dorsal horn gate where slow red pain spheres roll up a lower track, the Explorer pulls a fast blue touch lever to swing the heavy brass gate shut and clicks a golden endorphin key into the gate's padlock." + EXP_TAIL,
             None),
            ("09_ronald_melzack_and_patrick_wall_19_nov_1965_mit_gate_control_diagram_and_tens_stimulator", 67.5, 5.5, "B", False, "CAMBRIDGE, 19 NOVEMBER 1965", "Quality",
             "Quality: readable faces (at MIT in Cambridge on 19 November 1965, Canadian psychologist Ronald Melzack and British neuroscientist Patrick David Wall demonstrate their spinal dorsal horn Gate Control diagram and a transcutaneous electrical nerve stimulation TENS unit).",
             STYLE + "In a 1965 MIT neurophysiology laboratory, Ronald Melzack and Patrick Wall stand before a chalkboard diagram of the spinal dorsal horn gate holding a small electrical nerve stimulator box." + QUAL_TAIL,
             {"kind": "WHEN", "label": "CAMBRIDGE, 19 NOVEMBER 1965", "timeline_step": "2/3 · 19 November 1965 (Ronald Melzack and Patrick Wall at MIT publish the Gate Control Theory of Pain, proving fast A-beta touch fibres close a gate in the spinal cord's dorsal horn)", "hold_s": 3.5}),
        ],
    ),
    (
        2,
        "Part 02 — 1664, 1906 & February 1944: Descartes's Bell-Rope Myth, Charles Sherrington's Nociceptors & Henry Beecher's Anzio Beachhead Paradox",
        [
            ("01_sherrington_1906_oxford_nociceptors_and_henry_beecher_feb_1944_anzio_beachhead_wounded_soldiers", 73.0, 6.5, "A", False, "75% REFUSED ANZIO MORPHINE", "Quality",
             "Quality: readable faces (René Descartes's 1664 bell-rope pain engraving and British neurophysiologist Charles Scott Sherrington in 1906 mapping nociceptors, dissolving to Harvard anaesthesiologist Henry Knowles Beecher in February 1944 inside an Anzio beachhead tent examining wounded soldiers who refuse morphine).",
             STYLE + "Split period scene: on the left in 1906 Oxford, Charles Sherrington traces nociceptor reflex arcs beside René Descartes's 1664 boy-and-fire bell-rope engraving; on the right in February 1944 Anzio, physician Henry Beecher records notes beside a calm wounded soldier on a stretcher." + QUAL_TAIL,
             {"kind": "FACT", "label": "75% refused Anzio morphine", "who_cards": [
                 "René Descartes (1596–1650) — French philosopher and mathematician",
                 "Herbert Spencer Gasser (1888–1963) — American physiologist",
                 "Joseph Erlanger (1874–1965) — American physiologist",
             ], "when_stamp": "1664 · 1906 · February 1944 · 1946 · 1955", "timeline_step": "1/3 · 1664, 1906 & 1944–1955 (Replacing Descartes's bell-rope myth, Sherrington discovers nociceptors; Beecher documents Anzio battlefield analgesia and the placebo effect)", "hold_s": 3.8}),
            ("02_sherrington_1906_a_delta_vs_c_fibre_nociceptors_and_beecher_1946_1955_anzio_placebo_chart", 79.5, 8.0, "E", False, "1906 SHERRINGTON (NOCICEPTORS: A-DELTA 20 M/S VS C-FIBRE 1 M/S) & 1946/1955 BEECHER (ANZIO 25–32% VS 83% CIVILIAN MORPHINE & 35% PLACEBO)", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked Charles Sherrington (1906) & Erlanger/Gasser two-wave nociceptor conduction chart (fast A-delta first pain at 20 m/s vs slow C-fibre second pain at 1 m/s) alongside Henry Beecher's (1946 Ann. Surg. 123: 96–105 & 1955 JAMA 159: 1602) Anzio battlefield wounds (only 25–32% requesting morphine) vs civilian surgical wounds (83% requesting morphine) & 35% placebo analgesia chart.",
             {"kind": "DATA", "label": "1906 SHERRINGTON TWO-WAVE NOCICEPTORS (20 M/S VS 1 M/S) & 1946–1955 BEECHER ANZIO (25–32% VS 83% MORPHINE) & 35% PLACEBO CHART", "detail": "Inked Charles Sherrington (1906) & Erlanger/Gasser two-wave nociceptor conduction chart (fast A-delta first pain at 20 m/s vs slow C-fibre second pain at 1 m/s) alongside Henry Beecher's (1946 Ann. Surg. 123: 96–105 & 1955 JAMA 159: 1602) Anzio battlefield wounds (only 25–32% requesting morphine) vs civilian surgical wounds (83% requesting morphine) & 35% placebo analgesia chart on period paper", "scale": "if you are six feet tall and stub your bare toe in the dark, the sharp A-delta flash reaches your brain in less than a tenth of a second, while the slow C-fibre throbbing ache takes nearly two full seconds to climb the exact same leg", "hold_s": 3.8}),
            ("03_descartes_1664_traite_de_l_homme_engraving_sherrington_1906_and_beecher_1946_annals_of_surgery_closeup", 87.5, 6.5, "B", False, "1906 & 1944 — NOCICEPTORS & THE ANZIO PARADOX", "Fast",
             "Fast: daylight macro shot of René Descartes's 1664 Traité de l'homme bell-rope plate, Charles Sherrington's 1906 book, and Henry Beecher's 1946 Annals of Surgery and 1955 JAMA papers beside an Army medical field notebook on a bench. Nothing emissive, no face.",
             STYLE + "In crisp daylight on a medical library table, an open 1664 woodcut of a bell-rope nerve pathway sits beside a 1906 physiology book, a 1946 surgical journal, and a canvas medical field kit." + FAST_TAIL,
             None),
            ("04_cutaway_skin_model_showing_free_nerve_ending_nociceptors_and_myelinated_a_delta_vs_c_fibres_pan", 94.0, 5.5, "C", False, "TWO SPEEDS OF PAIN ALARM CABLES", "Fast",
             "Fast: daylight close-up pan across a sculpted anatomical skin cross-section showing high-threshold free nerve ending nociceptors feeding both a thick myelinated A-delta cable and a thin unmyelinated C-fibre cable on an oak table. Nothing emissive, no face.",
             STYLE + "In bright window light on an oak table, a painted anatomical skin cross-section model shows branching nociceptor nerve endings connected to a thick insulated A-delta nerve cable and a thin uninsulated C-fibre cable." + FAST_TAIL,
             None),
        ],
    ),
    (
        3,
        "Part 03 — 19 November 1965: Ronald Melzack & Patrick Wall's Gate Control Theory of Pain — Midpoint Twist",
        [
            ("01_ronald_melzack_and_patrick_wall_19_nov_1965_mit_science_spinal_dorsal_horn_gate_control_theory", 99.5, 6.5, "A", False, "TOUCH SLAMS SPINAL PAIN GATE", "Quality",
             "Quality: readable faces (Canadian psychologist Ronald Melzack and British neuroscientist Patrick David Wall at MIT on 19 November 1965 publishing the Gate Control Theory of Pain in Science, showing how fast A-beta touch fibres excite substantia gelatinosa inhibitory interneurons in the spinal dorsal horn to block slow C pain fibres).",
             STYLE + "Split period scene: on the left at 1965 MIT, Ronald Melzack and Patrick Wall trace the dorsal horn substantia gelatinosa gate circuit in their Science paper; on the right, a close-up anatomical model shows fast blue touch fibres activating an inhibitory neuron that blocks slow red pain signals." + QUAL_TAIL,
             {"kind": "FACT", "label": "Touch slams spinal pain gate", "when_stamp": "19 November 1965 · 1967", "timeline_step": "2/3 · 19 November 1965 (Melzack & Wall publish the Gate Control Theory of Pain in Science, explaining why rubbing a bump or 1967 TENS stimulation blocks pain in the spinal cord)", "hold_s": 3.8}),
            ("02_melzack_wall_19_nov_1965_science_dorsal_horn_substantia_gelatinosa_gate_control_circuit_chart", 106.0, 8.0, "E", False, "19 NOV 1965 RONALD MELZACK & PATRICK WALL (SCIENCE): SPINAL DORSAL HORN SUBSTANTIA GELATINOSA (SG) GATE CONTROL CIRCUIT", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked Ronald Melzack & Patrick Wall (19 November 1965 Science 150: 971–979) dorsal horn Gate Control circuit diagram (Substantia Gelatinosa SG inhibitory interneuron excited (+) by large A-beta touch fibres and inhibited (−) by small C pain fibres, modulating Transmission T-cell output to the brain, plus Central Control top-down inhibition).",
             {"kind": "DATA", "label": "19 NOV 1965 MELZACK & WALL (SCIENCE 150: 971): DORSAL HORN SUBSTANTIA GELATINOSA (SG) GATE CONTROL CIRCUIT DIAGRAM", "detail": "Inked Ronald Melzack & Patrick Wall (19 November 1965 Science 150: 971–979) dorsal horn Gate Control circuit diagram (Substantia Gelatinosa SG inhibitory interneuron excited (+) by large A-beta touch fibres and inhibited (−) by small C pain fibres, modulating Transmission T-cell output to the brain) on period paper", "scale": "your spinal cord's dorsal horn works like a nightclub bouncer at a narrow doorway — when slow pain signals arrive alone, the door swings wide open, but when you rub your stubbed toe, a crowd of fast touch signals arrives first and tells the bouncer to bolt the door shut", "hold_s": 3.8}),
            ("03_mit_1965_science_pain_mechanisms_issue_mcgill_pain_questionnaire_and_1967_tens_unit_closeup", 114.0, 6.5, "B", False, "19 NOVEMBER 1965 — THE GATE CONTROL THEORY OF PAIN", "Fast",
             "Fast: daylight macro shot of the 19 November 1965 Science issue open to Melzack and Wall's 'Pain Mechanisms: A New Theory' gate diagram beside an early 1967 TENS nerve stimulator and electrode pads on a bench. Nothing emissive, no face.",
             STYLE + "In crisp daylight on a 1965 MIT laboratory desk, an open scientific journal showing the dorsal horn gate circuit diagram sits beside a vintage metal electrical nerve stimulator box with surface electrode pads." + FAST_TAIL,
             None),
            ("04_mechanical_spinal_dorsal_horn_bouncer_gate_demonstrator_comparing_c_fibres_vs_a_beta_touch_pan", 120.5, 5.5, "C", False, "HOW RUBBING A BUMP CLOSES THE SPINAL GATE", "Fast",
             "Fast: daylight close-up pan across a brass-and-wood mechanical spinal gate demonstrator showing how large blue A-beta touch spheres trip a spring lever that closes the dorsal horn gate before small red C-fibre pain spheres arrive on an oak table. Nothing emissive, no face.",
             STYLE + "In bright window light on an oak table, a brass-and-wood mechanical track model shows fast blue touch spheres tripping a gate lever shut in front of slow red pain spheres." + FAST_TAIL,
             None),
        ],
    ),
    (
        4,
        "Part 04 — 9 March 1973 & 18 December 1975: Candace Pert & Solomon Snyder's Opioid Receptors & John Hughes & Hans Kosterlitz's Endorphins",
        [
            ("01_candace_pert_solomon_snyder_1973_opioid_receptors_and_hughes_kosterlitz_1975_aberdeen_enkephalins", 126.0, 6.5, "A", False, "BRAIN MAKES ITS OWN MORPHINE", "Quality",
             "Quality: readable faces (German pharmacist Friedrich Sertürner in 1804 isolating morphine, 26-year-old graduate student Candace Beebe Pert and Solomon Halbert Snyder at Johns Hopkins in 1972–9 March 1973 discovering brain opioid receptors with radioactive naloxone, dissolving to John Hughes and 72-year-old Hans Walter Kosterlitz in Aberdeen on 18 December 1975 isolating enkephalins / endorphins).",
             STYLE + "Split period scene: on the left in 1973 Johns Hopkins, Candace Pert and Solomon Snyder examine radiation counter tape beside their filtration manifold and Friedrich Sertürner's 1804 morphine bottle; on the right in 1975 Aberdeen, Hans Kosterlitz and John Hughes hold up the five-amino-acid enkephalin peptide model." + QUAL_TAIL,
             {"kind": "FACT", "label": "Brain makes its own morphine", "who_card": "Friedrich Wilhelm Sertürner (1783–1841) — German pharmacist and chemist", "when_stamp": "1804 · 22 September 1972 · 9 March 1973 · 18 December 1975 · 1978", "timeline_step": "3/3 · 1973 & 1975 (Candace Pert and Solomon Snyder at Johns Hopkins discover brain opioid receptors, and John Hughes and Hans Kosterlitz in Aberdeen isolate enkephalins and endorphins, the brain's own morphine)", "hold_s": 3.8}),
            ("02_pert_snyder_1973_science_3h_naloxone_opioid_receptor_and_hughes_kosterlitz_1975_nature_enkephalin_chart", 132.5, 8.0, "E", False, "9 MAR 1973 PERT & SNYDER (SCIENCE: [³H]NALOXONE OPIOID RECEPTOR) & 18 DEC 1975 HUGHES & KOSTERLITZ (NATURE: ENKEPHALIN / ENDORPHIN)", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked Candace Pert & Solomon Snyder (9 March 1973 Science 179: 1011–1014) radioactive [³H]naloxone opioid receptor binding chart & John Hughes & Hans Kosterlitz (18 December 1975 Nature 258: 577–579) Met/Leu-enkephalin & beta-endorphin inhibition of pain neurotransmitter release.",
             {"kind": "DATA", "label": "1973 PERT & SNYDER ([³H]NALOXONE OPIOID RECEPTOR BINDING) & 1975 HUGHES & KOSTERLITZ (MET/LEU-ENKEPHALIN & BETA-ENDORPHIN) CHART", "detail": "Inked Candace Pert & Solomon Snyder (9 March 1973 Science 179: 1011–1014) radioactive [³H]naloxone opioid receptor binding chart & John Hughes & Hans Kosterlitz (18 December 1975 Nature 258: 577–579) Met/Leu-enkephalin & beta-endorphin inhibition of pain neurotransmitter release on period paper", "scale": "Hans Kosterlitz and John Hughes had to haul buckets of frozen pig brains from a Scottish slaughterhouse for two years to isolate a pinch of enkephalin crystals — proving that every human head carries its own built-in pharmacy of natural morphine", "hold_s": 3.8}),
            ("03_baltimore_1973_filtration_manifold_scintillation_vials_and_aberdeen_1975_nature_enkephalin_paper_closeup", 140.5, 6.5, "B", False, "1973 & 1975 — OPIOID RECEPTORS & ENDORPHINS", "Fast",
             "Fast: daylight macro shot of Pert and Snyder's 1973 glass-fibre filter manifold and scintillation vials beside the 9 March 1973 Science and 18 December 1975 Nature issues and a five-amino-acid pentapeptide ball-and-stick model on a bench. Nothing emissive, no face.",
             STYLE + "In crisp daylight on a 1975 pharmacology bench, a stainless-steel filter manifold and glass scintillation vials sit beside an open 1975 journal and a five-bead pentapeptide molecular model." + FAST_TAIL,
             None),
            ("04_explorer_fitting_five_bead_enkephalin_and_beta_endorphin_key_into_mu_opioid_receptor_blocking_pain", 147.0, 5.5, "B", True, None, "Quality",
             "Quality: Explorer beat 2 (locked character reference).",
             STYLE + "Standing beside a giant sculpted mu-opioid receptor keyhole on a spinal nerve terminal, the Explorer fits a golden five-bead enkephalin peptide key into the receptor lock so a brass shutter slides closed and stops red pain neurotransmitter spheres from crossing the synapse." + EXP_TAIL,
             None),
        ],
    ),
    (
        5,
        "Part 05 — The Spinal Gate & the Pharmacy in Your Head — & How a Kitchen Sink Unlocked Why Soap Destroys Grease and Viruses",
        [
            ("01_timeline_1906_1975_and_nociceptors_spinal_gate_control_opioid_receptors_endorphins_chart", 152.5, 8.5, "E", False, "1906–1975 TIMELINE · SHERRINGTON NOCICEPTORS, BEECHER ANZIO PARADOX, MELZACK-WALL SPINAL GATE & PERT-SNYDER-KOSTERLITZ ENDORPHINS", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, the 3-era timeline completes: 1664, 1906 & 1944–1955 (Replacing Descartes's bell-rope myth, Charles Sherrington discovers nociceptors, and Henry Knowles Beecher on the Anzio beachhead discovers stress analgesia and the placebo effect) · 19 November 1965 (Ronald Melzack and Patrick Wall at MIT publish the Gate Control Theory of Pain, proving fast A-beta touch fibres close a gate in the spinal cord's dorsal horn) · 1973 & 1975 (Candace Pert and Solomon Snyder at Johns Hopkins discover brain opioid receptors, and John Hughes and Hans Kosterlitz in Aberdeen isolate enkephalins and endorphins, the brain's own morphine).",
             {"kind": "DATA", "label": "1906–1975 PAIN, GATE CONTROL & ENDORPHINS TIMELINE · SHERRINGTON, BEECHER, MELZACK, WALL, PERT, SNYDER, HUGHES & KOSTERLITZ", "detail": "Animated timeline (1906 → 1975) alongside an inked summary of nociceptors, the spinal dorsal horn pain gate, opioid receptors, and endogenous endorphins", "scale": "from a muddy medical tent on an Italian beach to a spinal gate at MIT and slaughterhouse pig brains in Scotland, scientists discovered that the greatest painkiller on Earth is brewed inside your own head", "when_stamp": "1906–1975", "timeline_step": "3/3 · 1906–1975 timeline complete", "hold_s": 3.8}),
            ("02_spinal_gate_and_endorphin_lock_model_beside_bar_of_soap_and_pockels_tin_trough_on_plinth_pan", 161.0, 5.5, "A", False, "THE SPINAL GATE & THE PHARMACY IN YOUR HEAD", "Fast",
             "Fast: daylight close-up of a sculpted spinal pain-gate and endorphin receptor model beside a block of Marseille olive-oil soap and Agnes Pockels's rectangular tin surface-tension trough on a wooden museum plinth. Nothing emissive, no face.",
             STYLE + "In crisp daylight on a wooden museum plinth, a brass-and-wood spinal gate model and golden peptide key sit beside a block of traditional soap and a rectangular tin water trough with a porcelain button." + FAST_TAIL,
             None),
            ("03_chevreul_1823_saponification_agnes_pockels_1891_kitchen_sink_trough_and_mcbain_1913_soap_micelles_handoff", 166.5, 6.5, "C", False, "SAPONIFICATION, KITCHEN TROUGH & SOAP MICELLES", "Quality",
             "Quality: readable faces (Michel Eugène Chevreul in Paris in 1823 demonstrating fat saponification, 19-year-old Agnes Pockels in Brunswick in 1891 measuring water surface tension at her kitchen sink with a tin trough and a porcelain button published with Lord Rayleigh in Nature, and James McBain in 1913 with Irving Langmuir in 1917 unveiling soap micelles and monolayers — handoff to 087 Soap, Agnes Pockels & Micelles).",
             STYLE + "Split period scene: on the left in 1891 Brunswick, young German physicist Agnes Pockels stands at her kitchen sink sliding a tin strip across a rectangular water trough with a suspended porcelain button; on the right in 1913–1917, James McBain and Irving Langmuir point to a spherical soap micelle model trapping grease." + QUAL_TAIL,
             {"kind": "WHEN", "label": "1823 · 12 MARCH 1891 · 1913 · 1917", "hold_s": 3.5}),
            ("04_table_three_callback", 173.0, 2.4, "C", False, None, "reuse",
             "Reuse: verified unused moving window [5.50s..7.90s] of P1:07_table_three_props_1906_kymograph_drum_1965_spinal_gate_model_and_1973_filtration_manifold_vials (callback, £0).",
             "Reuse P1:07_table_three_props_1906_kymograph_drum_1965_spinal_gate_model_and_1973_filtration_manifold_vials [5.50s..7.90s] (2.40s distinct non-overlapping tail window from 8.00s source clip).",
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
                row["reuse_of"] = "P1:07_table_three_props_1906_kymograph_drum_1965_spinal_gate_model_and_1973_filtration_manifold_vials"
                row["reuse_window_s"] = [5.5, 7.9]
                row["reuse_audit"] = {
                    "source_row": "P1:07_table_three_props_1906_kymograph_drum_1965_spinal_gate_model_and_1973_filtration_manifold_vials",
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
            "film": "086_Sherrington-Beecher-Melzack-Wall-Pert-Endorphins-Pain",
            "part": p_idx,
            "title": p_title,
            "version": "v01",
            "timing_status": "pre_vo_script_clock (built from pain_endorphins_script_master_v01.md; retimes onto Scribe STT once VO locks)",
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
        "film": "086_Sherrington-Beecher-Melzack-Wall-Pert-Endorphins-Pain",
        "version": "v01",
        "date": "2026-10-21",
        "owner": "gemini (J0805)",
        "status": "PRE_VO_BOARDS_V01_NO_MINT",
        "generation_authorized": False,
        "script": "00_Brand/Channel-Setup/ideas/086_Sherrington-Beecher-Melzack-Wall-Pert-Endorphins-Pain/pain_endorphins_script_master_v01.md",
        "sources": "00_Brand/Channel-Setup/ideas/086_Sherrington-Beecher-Melzack-Wall-Pert-Endorphins-Pain/SOURCES_v01.md",
        "credit_snapshot": {
            "flow_balance": 23740,
            "flow_floor": 0,
            "flow_read_at": "2026-10-15T21:42:22Z",
            "vertex_promo_gbp": 71.02,
            "vertex_usable_gbp": 70.02,
        },
        "totals": totals,
        "per_part": per_part_summary,
        "mint_order": "006 > 007 > 008 > 009 > 010 > 011 > 012 > 013 > 014 > 015 > 016 > 017 > 018 > 019 > 020 > 021 > 022 > 023 > 024 > 025 > 026 > 027 > 028 > 029 > 030 > 031 > 032 > 033 > 034 > 035 > 036 > 037 > 038 > 039 > 040 > 041 > 042 > 043 > 044 > 045 > 046 > 047 > 048 > 049 > 050 > 051 > 052 > 053 > 054 > 055 > 056 > 057 > 058 > 059 > 060 > 061 > 062 > 063 > 064 > 065 > 066 > 067 > 068 > 069 > 070 > 071 > 072 > 073 > 074 > 075 > 076 > 077 > 078 > 079 > 080 > 081 > 082 > 083 > 084 > 085 > 086 > 087 > 088 > 089 > 090 > 091 > 092 > 093 > 094 > 095. Nothing in 086 is generation_authorized.",
    }
    (EDIT / "PICTURE_PLAN_v01.json").write_text(json.dumps(plan, indent=2) + "\n")

    sl = [
        "# 086 Endorphins: How Your Brain Makes Its Own Morphine — Shot list & plate boards v01 (pre-VO)",
        "",
        "Gemini, 21 Oct 2026, J0805. Built from `pain_endorphins_script_master_v01.md` (`90.8/100 PASS`) and `SOURCES_v01.md`.",
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
        "# 086 price review v01 (pre-VO plate boards)",
        "",
        "Gemini, 21 Oct 2026, J0805. Boards only. **No mint. No spend. No merge.**",
        "Prepared from `pain_endorphins_script_master_v01.md` (`90.8/100 PASS`) and `SOURCES_v01.md` so 086's full plate board rows, non-emissive Fast prompts, £0 code graphics, and Teach-on-Screen overlays are ready to re-time the moment long VO locks. Parked for Chief.",
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
        f"- **Quality ({totals['Quality']} rows):** readable faces (René Descartes, Charles Scott Sherrington, Henry Knowles Beecher, Ronald Melzack, Patrick David Wall, Friedrich Wilhelm Sertürner, Candace Beebe Pert, Solomon Halbert Snyder, John Hughes, Hans Walter Kosterlitz, Agnes Pockels, James William McBain, Irving Langmuir), 1906 Oxford `nociceptor` mapping & February 1944 Anzio beachhead battlefield analgesia, 19 November 1965 MIT `Gate Control Theory of Pain` & `TENS` demonstration, 9 March 1973 Johns Hopkins `[³H]naloxone` `opioid receptor` discovery & 18 December 1975 Aberdeen `enkephalin / endorphin` isolation, and the 2 Explorer beats.",
        f"- **Fast ({totals['Fast']} rows, non-emissive):** daylight prop and laboratory shots (Sherrington's 1906 book, 1965 *Science* Gate Control diagram & dried opium poppy capsule pan, 3-object callback bench, Descartes's 1664 *Traité de l'homme* engraving with 1946 *Annals of Surgery* & canvas field kit, cutaway skin model showing free nerve ending nociceptors with myelinated A-delta vs unmyelinated C fibres, 19 November 1965 *Science* issue with 1967 TENS box & electrode pads, mechanical dorsal horn gate track demonstrator, 1973 stainless-steel filtration manifold & scintillation vials with 1975 *Nature* issue & pentapeptide model, spinal gate model beside Marseille soap & Agnes Pockels's tin surface-tension trough on museum plinth). Zero candles, flames, sparks, or glowing elements on Fast.",
        f"- **£0 code graphics ({totals['code_graphic']} rows):**",
        "  1. `P1:04_sherrington_1906_melzack_wall_1965_gate_control_and_pert_kosterlitz_1973_1975_endorphin_chart` — Melzack & Wall (1965) nerve conduction velocity comparison (`A-beta 35–75 m/s` vs `A-delta 5–30 m/s` vs `C-fibre 0.5–2 m/s`) & spinal dorsal horn Gate Control circuit (`SCALE: your touch nerves race up to your spine at seventy-five metres per second — as fast as an express train — while your throbbing pain nerves crawl at just one metre per second, a walking pace, so rubbing a bumped shin lets the touch signals reach your spinal cord first and slam the gate shut before the pain arrives`)",
        "  2. `P1:06_beecher_1946_anzio_morphine_demand_and_pert_snyder_kosterlitz_1973_1975_opioid_endorphin_chart` — Henry Beecher (1946) Anzio battlefield (`~25%`) vs civilian surgical (`>80%`) morphine demand & Pert/Snyder/Kosterlitz (1973–1975) opioid receptor / endorphin lock-and-key chart (`SCALE: molecule for molecule, your brain's own beta-endorphin is eighteen to thirty times more potent at silencing pain than hospital morphine — and your brainstem can flood your spinal cord with it in seconds during a crisis`)",
        "  3. `P2:02_sherrington_1906_a_delta_vs_c_fibre_nociceptors_and_beecher_1946_1955_anzio_placebo_chart` — Charles Sherrington (1906) two-wave nociceptor conduction chart (`20 m/s` vs `1 m/s`) & Henry Beecher (1946 & 1955) Anzio analgesia & `35%` placebo chart (`SCALE: if you are six feet tall and stub your bare toe in the dark, the sharp A-delta flash reaches your brain in less than a tenth of a second, while the slow C-fibre throbbing ache takes nearly two full seconds to climb the exact same leg`)",
        "  4. `P3:02_melzack_wall_19_nov_1965_science_dorsal_horn_substantia_gelatinosa_gate_control_circuit_chart` — Ronald Melzack & Patrick Wall (19 November 1965 *Science* 150: 971–979) dorsal horn `Substantia Gelatinosa` (`SG`) Gate Control circuit diagram (`SCALE: your spinal cord's dorsal horn works like a nightclub bouncer at a narrow doorway — when slow pain signals arrive alone, the door swings wide open, but when you rub your stubbed toe, a crowd of fast touch signals arrives first and tells the bouncer to bolt the door shut`)",
        "  5. `P4:02_pert_snyder_1973_science_3h_naloxone_opioid_receptor_and_hughes_kosterlitz_1975_nature_enkephalin_chart` — Candace Pert & Solomon Snyder (9 March 1973 *Science*) `[³H]naloxone` opioid receptor binding & John Hughes & Hans Kosterlitz (18 December 1975 *Nature*) enkephalin/endorphin chart (`SCALE: Hans Kosterlitz and John Hughes had to haul buckets of frozen pig brains from a Scottish slaughterhouse for two years to isolate a pinch of enkephalin crystals — proving that every human head carries its own built-in pharmacy of natural morphine`)",
        "  6. `P5:01_timeline_1906_1975_and_nociceptors_spinal_gate_control_opioid_receptors_endorphins_chart` — completed timeline (1906 → 1975) + nociceptors, the Anzio paradox, spinal Gate Control & endogenous endorphins (`SCALE: from a muddy medical tent on an Italian beach to a spinal gate at MIT and slaughterhouse pig brains in Scotland, scientists discovered that the greatest painkiller on Earth is brewed inside your own head`)",
        f"- **£0 verified reuse ({totals['reuse']} row):** `P5:04_table_three_callback` uses the 2.40 s unused moving tail `[5.50s..7.90s]` of `P1:07_table_three_props_1906_kymograph_drum_1965_spinal_gate_model_and_1973_filtration_manifold_vials`.",
        "",
        "## Mint order",
        "",
        "006 > 007 > 008 > 009 > 010 > 011 > 012 > 013 > 014 > 015 > 016 > 017 > 018 > 019 > 020 > 021 > 022 > 023 > 024 > 025 > 026 > 027 > 028 > 029 > 030 > 031 > 032 > 033 > 034 > 035 > 036 > 037 > 038 > 039 > 040 > 041 > 042 > 043 > 044 > 045 > 046 > 047 > 048 > 049 > 050 > 051 > 052 > 053 > 054 > 055 > 056 > 057 > 058 > 059 > 060 > 061 > 062 > 063 > 064 > 065 > 066 > 067 > 068 > 069 > 070 > 071 > 072 > 073 > 074 > 075 > 076 > 077 > 078 > 079 > 080 > 081 > 082 > 083 > 084 > 085 > 086 > 087 > 088 > 089 > 090 > 091 > 092 > 093 > 094 > 095. `generation_authorized` is `false` on every row.",
    ])
    (EDIT / "PRICE_REVIEW_v01.md").write_text("\n".join(pr_lines) + "\n")
    print(f"086 v01 boards written: {totals['rows']} rows, Flow expected={totals['flow_credits_expected']}")


if __name__ == "__main__":
    main()
