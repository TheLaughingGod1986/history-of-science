#!/usr/bin/env python3
"""HOS 037 (Superconductivity: The 1911 Lab That Made Electricity Flow Forever) pre-VO plate boards v01. J0509. No mint, no spend.

Built from 00_Brand/Channel-Setup/ideas/037_Onnes-Meissner-Superconductivity/superconductivity_script_master_v01.md (92.4 PASS)
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
        "Part 01 — The Coldest Room in the Universe and the Vanishing Resistance",
        [
            ("01_kamerlingh_onnes_8_april_1911_leiden_mercury_zero_ohms", 0.0, 5.5, "A", False, "ZERO RESISTANCE AT 4.2 KELVIN", "Quality",
             "Quality: Short frame 0 / answer image (0:03) + inside the Cryogenic Laboratory at Leiden University at 4:00 p.m. on 8 April 1911, Dutch physicist Heike Kamerlingh Onnes and technician Gilles Holst peer through a silvered glass cryostat bath of bubbling liquid helium (4.20 Kelvin) at a U-shaped capillary of frozen mercury while the mirror galvanometer needle drops dead to 0.00000 ohms.",
             STYLE + "Inside the Leiden University Cryogenic Laboratory on 8 April 1911, bearded Dutch physicist Heike Kamerlingh Onnes and young researcher Gilles Holst peer into a frost-covered glass cryostat of clear bubbling liquid helium surrounding a U-shaped mercury tube while a brass galvanometer needle drops to zero." + QUAL_TAIL,
             {"kind": "WHEN", "label": "LEIDEN, 8 APRIL 1911", "timeline_step": "2/5 · 8 Apr 1911 (Kamerlingh Onnes & Gilles Holst discover zero resistance in mercury at 4.20 K — 'Kwik nagenoeg nul')", "hold_s": 3.5}),
            ("02_helium_cryostat_1914_lead_ring_and_1933_meissner_levitation_split", 5.5, 6.0, "B", False, "LIQUID HELIUM, ZERO OHMS, LEVITATION", "Quality",
             "Quality: complex three-part split composition (Heike Kamerlingh Onnes's 10 July 1908 liquid helium cryostat and 8 April 1911 blue notebook on the left; a frost-covered lead ring carrying a battery-free persistent current in 1914 in the centre; Walther Meissner and Robert Ochsenfeld's 1933 magnetic expulsion levitating a magnet above a superconductor on the right).",
             STYLE + "Three-panel period composition: on the left, a silvered glass Dewar flask beside a small blue cloth notebook; in the centre, a frost-covered lead ring inside a glass bath beside a deflected brass compass needle; on the right, a bar magnet floating in mid-air above a chilled superconducting disc." + QUAL_TAIL,
             None),
            ("03_copper_coil_wheatstone_bridge_and_kelvin_curve_slate", 11.5, 6.0, "C", False, "KELVIN PREDICTED INFINITE RESISTANCE", "Fast",
             "Fast: daylight laboratory view of spools of braided copper wire, a brass Wheatstone bridge resistance box, and an inked slate diagram on an oak bench. Nothing emissive, no face.",
             STYLE + "In crisp daylight on a physics laboratory bench, spools of copper wire sit beside a polished brass Wheatstone bridge box with ivory pegs and a dark slate board." + FAST_TAIL,
             {"kind": "WHEN", "label": "1902", "hold_s": 3.5}),
            ("04_onnes_8_april_1911_mercury_resistance_cliff_4_20k_chart", 17.5, 8.0, "E", False, "8 APRIL 1911: MERCURY RESISTANCE PLUNGES >10,000× ACROSS 0.01 K AT 4.20 KELVIN", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked resistance-vs-temperature graph from Kamerlingh Onnes's April 1911 Leiden measurements shows solid mercury's resistance R/R₀ plunging by a factor of >10,000 across a 0.01 Kelvin cliff at 4.20 K (−268.95 °C) from 0.115 Ω to <10⁻⁵–10⁻⁷ Ω ('Kwik nagenoeg nul'), contrasted with Lord Kelvin's 1902 prediction curve.",
             {"kind": "DATA", "label": "8 APRIL 1911: SOLID MERCURY RESISTANCE PLUNGES >10,000× AT 4.20 K (−268.95 °C)", "detail": "Inked resistance-vs-temperature graph on period paper from Kamerlingh Onnes's April 1911 Leiden measurements showing frozen mercury's resistance plunging by a factor of >10,000 across a 0.01 Kelvin cliff at 4.20 K (−268.95 °C) to <10⁻⁷ ohms", "scale": "within a single hundredth of a degree at four point two Kelvin, the electrical friction inside solid mercury didn't fade away — it fell off a cliff by more than ten thousand times to zero", "who_card": "Heike Kamerlingh Onnes (1853–1926) — Dutch experimental physicist · Gilles Holst (1886–1968) — Dutch research physicist · Walther Meissner (1882–1974) — German physicist", "when_stamp": "10 July 1908 · 8 April 1911 · 1933 · 1957", "hold_s": 3.8}),
            ("05_quadruple_distilled_mercury_u_tube_capillary_and_galvanometer_pan", 25.5, 5.5, "A", False, "LEIDEN CRYOGENIC LAB, 1911", "Fast",
             "Fast: daylight macro pan across a U-shaped glass capillary filled with silvery mercury, platinum lead wires, and a brass mirror galvanometer on a wooden table between code graphics so two full-frame graphics never run back to back. Nothing emissive, no face.",
             STYLE + "In crisp daylight on a wooden laboratory bench, the camera pans across a thin U-shaped glass capillary tube filled with silvery mercury, brass binding posts, and a cylindrical brass mirror galvanometer." + FAST_TAIL,
             None),
            ("06_cryogenic_temperature_bar_293k_to_deep_space_2_7k_and_leiden_1_04k", 31.0, 8.0, "E", False, "COLDER THAN DEEP SPACE", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period parchment, an inked cryogenic temperature bar compares room temperature (293 K / +20 °C), liquid nitrogen (77 K / −196 °C), liquid hydrogen (20.4 K / −252.8 °C), liquid helium boiling point (4.22 K / −268.93 °C), the cosmic microwave background of deep space (2.7 K), and Leiden's pumped helium bath (1.04 K / −272.11 °C).",
             {"kind": "DATA", "label": "CRYOGENIC SCALE: 293 K ROOM TEMP → 77 K N₂ → 20.4 K H₂ → 4.22 K HE → 2.7 K DEEP SPACE → 1.04 K LEIDEN", "detail": "Inked cryogenic temperature bar comparing room temperature (293 K), liquid nitrogen (77 K), liquid hydrogen (20.4 K), liquid helium boiling point (4.22 K / −268.93 °C), cosmic microwave background of deep space (2.7 K), and Leiden's pumped helium (1.04 K / −272.11 °C)", "scale": "at one point zero four degrees above Absolute Zero, Kamerlingh Onnes's glass flask in the Netherlands was more than twice as cold as the deepest voids of outer space", "hold_s": 3.8}),
            ("07_table_three_props_dewar_flask_blue_notebook_levitating_magnet_dish", 39.0, 5.5, "C", False, "1908 TO 1987", "Fast",
             "Fast: daylight prop table (callback source for Part 05: a silvered glass Dewar flask, Kamerlingh Onnes's small blue cloth notebook with a fountain pen, and a frost-rimmed ceramic disc with a small bar magnet suspended above it). Nothing emissive.",
             STYLE + "On an oak workbench in soft window light sit three objects side by side: a silvered glass Dewar vacuum flask, a small blue cloth-bound notebook with a brass fountain pen, and a dark ceramic disc in a porcelain dish with a small metal cube hovering above it." + FAST_TAIL,
             None),
            ("08_explorer_cooper_pair_gliding_through_crystal_lattice_with_floating_magnet", 62.0, 5.5, "A", True, None, "Quality",
             "Quality: Explorer beat 1 (locked character reference, after 1:00).",
             STYLE + "Walking along a corridor of vibrating metal spheres where single electrons keep bumping, the Explorer links hands with a partner to form a synchronized pair: the pair glides effortlessly down a smooth channel between the spheres without a single collision while a small magnet floats above them." + EXP_TAIL,
             None),
            ("09_kamerlingh_onnes_and_holst_8_april_1911_blue_notebook_kwik_nagenoeg_nul", 67.5, 5.5, "B", False, "MERCURY PRACTICALLY ZERO", "Quality",
             "Quality: readable faces (in the Leiden laboratory on 8 April 1911, Heike Kamerlingh Onnes writes in his small blue notebook while Gilles Holst checks the Wheatstone bridge switches).",
             STYLE + "Inside the Leiden University laboratory on 8 April 1911, bearded physicist Heike Kamerlingh Onnes writes in a small blue notebook while young assistant Gilles Holst adjusts brass switches on a Wheatstone bridge." + QUAL_TAIL,
             None),
        ],
    ),
    (
        2,
        "Part 02 — The Race to Absolute Zero & the Teacup of Liquid Helium",
        [
            ("01_dewar_1898_london_vacuum_flask_and_onnes_10_july_1908_leiden", 73.0, 6.5, "A", False, "COLDER THAN DEEP SPACE", "Quality",
             "Quality: readable faces (Scottish chemist Sir James Dewar at the Royal Institution in London in 1898 holding his silvered vacuum flask of liquid hydrogen, contrasted with Heike Kamerlingh Onnes in Leiden on 10 July 1908 beside his brass cascade compressors).",
             STYLE + "Split period scene: on the left in London in 1898, bearded Scottish chemist James Dewar holds up a silvered double-walled vacuum flask; on the right in Leiden on 10 July 1908, Heike Kamerlingh Onnes stands beside tall brass cascade gas compressors." + QUAL_TAIL,
             {"kind": "WHO", "label": "James Dewar (1842–1923) — Scottish chemist and physicist", "fact_card": "Colder than deep space", "when_stamp": "1702 · 1848 · 1898 · 10 July 1908", "timeline_step": "1/5 · 10 Jul 1908 (Heike Kamerlingh Onnes liquefies 60 mL of helium at 4.22 K in Leiden)", "hold_s": 3.8}),
            ("02_onnes_10_july_1908_four_stage_cascade_liquefier_60ml_helium_diagram", 79.5, 8.0, "E", False, "10 JULY 1908: 4-STAGE CASCADE LIQUEFIER → 60 ML LIQUID HELIUM AT 4.22 K (PUMPED TO 1.04 K)", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked cascade cooling diagram shows Kamerlingh Onnes's 4-stage Leiden liquefier on 10 July 1908: methyl chloride (183 K) → ethylene (169 K) → oxygen/air (77 K) → liquid hydrogen (20.4 K) → 60 mL of liquid helium at 4.22 K (−268.93 °C), pumped down to 1.04 K.",
             {"kind": "DATA", "label": "10 JULY 1908 LEIDEN CASCADE: 183 K → 169 K → 77 K → 20.4 K → 60 ML LIQUID HELIUM AT 4.22 K", "detail": "Inked cascade cooling diagram on period paper showing Kamerlingh Onnes's 4-stage Leiden liquefier on 10 July 1908: methyl chloride (183 K) → ethylene (169 K) → oxygen/air (77 K) → liquid hydrogen (20.4 K) → 60 mL of liquid helium at 4.22 K (−268.93 °C), pumped down to 1.04 K", "scale": "sixty millilitres of liquid helium — barely enough to fill an espresso cup — made a room in Leiden colder than any natural place in the known universe", "hold_s": 3.8}),
            ("03_onnes_10_july_1908_730pm_60ml_liquid_helium_meniscus_in_dewar", 87.5, 6.5, "B", False, "10 JULY 1908 — LIQUID HELIUM", "Quality",
             "Quality: readable face (at 7:30 p.m. on 10 July 1908 in the Leiden Cryogenic Laboratory, Heike Kamerlingh Onnes peers into the central triple-walled glass Dewar flask and spots the shimmering meniscus of 60 millilitres of liquid helium).",
             STYLE + "In the Leiden Cryogenic Laboratory on the evening of 10 July 1908, Heike Kamerlingh Onnes peers closely through the unsilvered window of a triple-walled glass Dewar flask at the clear meniscus of liquid helium." + QUAL_TAIL,
             None),
            ("04_brass_cascade_compressors_and_glass_dewar_tubes_leiden_macro", 94.0, 5.5, "C", False, "4.22 KELVIN (−268.93 °C)", "Fast",
             "Fast: daylight macro shot of Leiden's polished brass cascade valves, copper cooling coils, and a silvered glass Dewar flask covered in white frost. Nothing emissive, no face.",
             STYLE + "In crisp daylight, polished brass pressure gauges and coiled copper pipes connect to a frost-dusted silvered glass Dewar vacuum flask." + FAST_TAIL,
             None),
        ],
    ),
    (
        3,
        "Part 03 — 'Kwik Nagenoeg Nul' — 8 April 1911 & the Current That Never Died",
        [
            ("01_holst_and_onnes_8_april_1911_galvanometer_and_1914_persistent_ring", 99.5, 6.5, "A", False, "CURRENT FLOWS 100,000+ YEARS", "Quality",
             "Quality: readable faces (technician Gilles Holst seated at the mirror galvanometer in the Leiden University basement at 4:00 p.m. on 8 April 1911 while Heike Kamerlingh Onnes cools the mercury capillary upstairs, dissolving to Onnes's 1914 disconnected superconducting lead ring).",
             STYLE + "In the Leiden University basement on 8 April 1911, young physicist Gilles Holst watches a brass mirror galvanometer scale drop to zero while Heike Kamerlingh Onnes disconnects battery wires from a chilled lead ring beside a deflected compass needle." + QUAL_TAIL,
             {"kind": "FACT", "label": "Current flows 100,000+ years", "when_stamp": "8 April 1911 · 1913 · 1914", "hold_s": 3.8}),
            ("02_onnes_1911_comm_122b_mercury_0_115_to_zero_ohms_and_lead_tin_chart", 106.0, 8.0, "E", False, "COMM. NO. 122B: MERCURY 0.115 Ω (4.3 K) → <10⁻⁵ Ω (4.20 K) · TIN (3.7 K) · LEAD (7.2 K)", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked resistance cliff chart from Kamerlingh Onnes's 1911 Leiden Communication No. 122b shows solid mercury resistance falling from 0.115 Ω at 4.3 K to <10⁻⁵ Ω at 4.20 K, alongside tin (Tc = 3.7 K), lead (Tc = 7.2 K), and Onnes's 1914 persistent-current ring (>100,000-year decay bound).",
             {"kind": "DATA", "label": "LEIDEN COMM. 122B: MERCURY 0.115 Ω → <10⁻⁵ Ω AT 4.20 K · TIN (3.7 K) & LEAD (7.2 K)", "detail": "Inked resistance cliff chart on period paper from Kamerlingh Onnes's 1911 Leiden Communication No. 122b showing solid mercury resistance falling from 0.115 Ω at 4.3 K to <10⁻⁵ Ω at 4.20 K, alongside lead (Tc = 7.2 K) and tin (Tc = 3.7 K)", "scale": "a current started inside a superconducting ring with the battery unplugged will keep circling longer than the entire history of human civilisation", "hold_s": 3.8}),
            ("03_leiden_1914_unplugged_superconducting_lead_ring_and_deflected_compass", 114.0, 6.5, "B", False, "1914 — NO BATTERY NEEDED", "Fast",
             "Fast: daylight close-up of a frost-covered ring of lead wire inside a glass cryostat with its battery knife-switch wide open and unplugged while a brass compass needle beside the glass stays deflected at a fixed angle. Nothing emissive, no face.",
             STYLE + "In crisp daylight on a laboratory table, a frost-covered lead ring sits inside a clear glass Dewar flask with disconnected copper battery leads hanging loose beside a brass compass whose needle holds a steady deflection." + FAST_TAIL,
             None),
            ("04_quadruple_mercury_distillation_glassware_bench_closeup", 120.5, 5.5, "C", False, "QUADRUPLE-DISTILLED MERCURY", "Fast",
             "Fast: daylight macro shot of Leiden's glass vacuum distillation flasks filled with mirror-bright liquid mercury beside a hair-thin U-shaped glass capillary tube. Nothing emissive, no face.",
             STYLE + "In bright window light on a wooden bench, linked glass distillation flasks hold pools of mirror-bright liquid mercury beside a delicate U-shaped capillary tube." + FAST_TAIL,
             None),
        ],
    ),
    (
        4,
        "Part 04 — The Meissner Levitation Shock & the 46-Year Quantum Mystery — Midpoint Twist",
        [
            ("01_meissner_ochsenfeld_october_1933_berlin_and_bardeen_cooper_schrieffer_1957", 126.0, 6.5, "A", False, "BARDEEN WON 2 PHYSICS NOBELS", "Quality",
             "Quality: readable faces (German physicists Walther Meissner and Robert Ochsenfeld in Berlin in October 1933 measuring magnetic flux expulsion around a cooled tin cylinder, alongside John Bardeen, Leon Cooper, and Robert Schrieffer at a blackboard in Urbana, Illinois, in February 1957).",
             STYLE + "Split period scene: on the left in Berlin in October 1933, German physicists Walther Meissner and Robert Ochsenfeld in 1930s suits measure magnetic lines around a frost-covered tin cylinder; on the right in Urbana in February 1957, John Bardeen, Leon Cooper, and young Robert Schrieffer stand before a chalkboard of wave diagrams." + QUAL_TAIL,
             {"kind": "WHO", "label": "Leon Cooper (1930–2024) — American theoretical physicist · Robert Schrieffer (1931–2019) — American physicist", "fact_card": "Bardeen won 2 Physics Nobels", "when_stamp": "October 1933 · 1945 · February 1957 · 1972", "timeline_step": "3/5 · Oct 1933 (Walther Meissner & Robert Ochsenfeld discover magnetic flux expulsion) & 4/5 · Feb 1957 (Bardeen, Cooper & Schrieffer publish BCS Cooper-pair theory)", "hold_s": 3.8}),
            ("02_meissner_effect_flux_expulsion_and_bcs_cooper_pair_phonon_diagram", 132.5, 8.0, "E", False, "MEISSNER EFFECT (B = 0 FLUX EXPULSION) & 1957 BCS COOPER-PAIR PHONON ATTRACTION", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked two-panel diagram compares a classical metal above Tc (magnetic field lines pass straight through; single electrons scatter off vibrating lattice ions, wasting heat) vs a superconductor below Tc (Meissner Effect expels magnetic field B = 0 to levitate a magnet; phonon lattice attraction binds electrons into frictionless BCS Cooper pairs).",
             {"kind": "DATA", "label": "MEISSNER EFFECT (B = 0 MAGNETIC EXPULSION) & 1957 BCS ELECTRON COOPER PAIRS", "detail": "Inked two-panel diagram on period paper comparing a classical metal above Tc (magnetic field lines penetrate; single electrons scatter) vs a superconductor below Tc (Meissner Effect expels magnetic field B = 0 to levitate a magnet; phonon lattice attraction binds electrons into frictionless BCS Cooper pairs)", "scale": "forty-six years elapsed between Kamerlingh Onnes seeing zero resistance in 1911 and Bardeen, Cooper, and Schrieffer explaining how two negative electrons team up through crystal vibrations in 1957", "hold_s": 3.8}),
            ("03_arkadiev_1945_levitating_bar_magnet_above_superconducting_lead_bowl", 140.5, 6.5, "B", False, "THE MEISSNER EFFECT, 1933", "Quality",
             "Quality: close-up of a small bar magnet floating locked in mid-air above a frost-covered superconducting lead bowl in 1945 as a physicist's hand nudges it and it springs back into place.",
             STYLE + "Above a frost-covered concave lead dish in a cryogenic bath, a small steel bar magnet floats steady in mid-air; a researcher's hand gently nudges the floating magnet with a wooden rod and it springs smoothly back to equilibrium." + QUAL_TAIL,
             None),
            ("04_explorer_riding_levitating_magnet_above_frosted_superconductor_disc", 147.0, 5.5, "B", True, None, "Quality",
             "Quality: Explorer beat 2 (locked character reference).",
             STYLE + "Pouring liquid helium from a silvered Dewar over a dark metal disc, the Explorer steps onto a heavy iron horseshoe magnet above it: as frost blooms across the disc, invisible magnetic spring lines lift the magnet with the Explorer riding steady in mid-air." + EXP_TAIL,
             None),
        ],
    ),
    (
        5,
        "Part 05 — The 1986 Liquid-Nitrogen Breakthrough, MRI Scanners & the Steam Train Full of Trumpets",
        [
            ("01_timeline_1908_1987_and_tc_4_2k_to_35k_to_93k_ybco_above_77k_chart", 152.5, 8.5, "E", False, "1908–1987 TIMELINE · TC CLIMBS FROM 4.2 K (1911) TO 35 K (1986) & 93 K YBCO (1987) > 77 K N₂", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, the 5-date timeline completes: 10 Jul 1908 (Kamerlingh Onnes liquefies helium at 4.22 K) · 8 Apr 1911 (mercury zero resistance at 4.20 K) · Oct 1933 (Meissner & Ochsenfeld magnetic expulsion) · Feb 1957 (Bardeen, Cooper & Schrieffer BCS theory) · Jan 1986 – Feb 1987 (Bednorz & Müller 35 K LBCO and Wu & Chu 93 K YBCO ceramic crossing the 77 K liquid-nitrogen boiling point).",
             {"kind": "DATA", "label": "1908–1987 TIMELINE & CRITICAL TEMP: 4.2 K (1911 HG) → 35 K (1986 LBCO) → 93 K (1987 YBCO > 77 K N₂)", "detail": "Animated 5-date timeline (1908 → 1987) alongside critical temperature climbing from 4.2 K (1911 Hg) to 35 K (1986 LBCO) and 93 K (1987 YBCO) above the 77 K (−196 °C) boiling point of liquid nitrogen", "scale": "jumping from 4.2 Kelvin liquid helium in 1911 to 93 Kelvin YBCO in 1987 meant cooling a superconductor with liquid nitrogen that costs pennies a litre instead of rare helium near Absolute Zero", "fact_card": "Liquid nitrogen is cheaper than milk", "when_stamp": "January 1986 · February 1987", "timeline_step": "5/5 · Jan 1986 – Feb 1987 (Bednorz & Müller's 35 K cuprate and Wu & Chu's 93 K YBCO cross the 77 K liquid-nitrogen threshold)", "hold_s": 3.8}),
            ("02_ybco_93k_ceramic_disc_levitating_magnet_in_77k_liquid_nitrogen_and_mri", 161.0, 5.5, "A", False, "93 KELVIN — ABOVE LIQUID NITROGEN", "Quality",
             "Quality: in a laboratory and hospital MRI suite, a black YBCO ceramic disc in a dish of 77 K liquid nitrogen locks a silver magnet levitating in mid-air beside a cut-away hospital MRI scanner coil.",
             STYLE + "In a bright laboratory, a black ceramic superconductor disc sits in a porcelain dish of misting liquid nitrogen with a silver magnet floating locked in mid-air above it, beside a hospital MRI scanner." + QUAL_TAIL,
             None),
            ("03_buys_ballot_3_june_1845_utrecht_steam_train_of_horn_players_handoff", 166.5, 6.5, "C", False, "THE TRAIN FULL OF TRUMPETS", "Quality",
             "Quality: readable faces (along the Utrecht–Maarssen railway line in the Netherlands on 3 June 1845, Dutch scientist Christophorus Buys Ballot stands beside the tracks as a steam locomotive roars past pulling an open flatbed car of brass horn players testing Christian Doppler's 1842 wave equation, beside Ernst Mach's 1887 spark photograph of a supersonic bullet — handoff to 038 Sound Waves & Doppler Effect).",
             STYLE + "Beside the Utrecht railway tracks on 3 June 1845, young Dutch scientist Christophorus Buys Ballot listens intently with a tuning fork as a billowing steam locomotive pulls an open wooden flatbed wagon of brass trumpet players blowing a steady note." + QUAL_TAIL,
             {"kind": "WHEN", "label": "25 MAY 1842 · 3 JUNE 1845 · 1887", "hold_s": 3.5}),
            ("04_table_three_callback", 173.0, 2.4, "C", False, None, "reuse",
             "Reuse: verified unused moving window [5.50s..7.90s] of P1:07_table_three_props_dewar_flask_blue_notebook_levitating_magnet_dish (callback, £0).",
             "Reuse P1:07_table_three_props_dewar_flask_blue_notebook_levitating_magnet_dish [5.50s..7.90s] (2.40s distinct non-overlapping tail window from 8.00s source clip).",
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
                row["reuse_of"] = "P1:07_table_three_props_dewar_flask_blue_notebook_levitating_magnet_dish"
                row["reuse_window_s"] = [5.5, 7.9]
                row["reuse_audit"] = {
                    "source_row": "P1:07_table_three_props_dewar_flask_blue_notebook_levitating_magnet_dish",
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
            "film": "037_Onnes-Meissner-Superconductivity",
            "part": p_idx,
            "title": p_title,
            "version": "v01",
            "timing_status": "pre_vo_script_clock (built from superconductivity_script_master_v01.md; retimes onto Scribe STT once VO locks)",
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
        "film": "037_Onnes-Meissner-Superconductivity",
        "version": "v01",
        "date": "2026-10-18",
        "owner": "gemini (J0509)",
        "status": "PRE_VO_BOARDS_V01_NO_MINT",
        "generation_authorized": False,
        "script": "00_Brand/Channel-Setup/ideas/037_Onnes-Meissner-Superconductivity/superconductivity_script_master_v01.md",
        "sources": "00_Brand/Channel-Setup/ideas/037_Onnes-Meissner-Superconductivity/SOURCES_v01.md",
        "credit_snapshot": {
            "flow_balance": 23740,
            "flow_floor": 0,
            "flow_read_at": "2026-10-15T21:42:22Z",
            "vertex_promo_gbp": 71.02,
            "vertex_usable_gbp": 70.02,
        },
        "totals": totals,
        "per_part": per_part_summary,
        "mint_order": "006 > 007 > 008 > 009 > 010 > 011 > 012 > 013 > 014 > 015 > 016 > 017 > 018 > 019 > 020 > 021 > 022 > 023 > 024 > 025 > 026 > 027 > 028 > 029 > 030 > 031 > 032 > 033 > 034 > 035 > 036 > 037. Nothing in 037 is generation_authorized.",
    }
    (EDIT / "PICTURE_PLAN_v01.json").write_text(json.dumps(plan, indent=2) + "\n")

    sl = [
        "# 037 Superconductivity: The 1911 Lab That Made Electricity Flow Forever — Shot list & plate boards v01 (pre-VO)",
        "",
        "Gemini, 18 Oct 2026, J0509. Built from `superconductivity_script_master_v01.md` (92.4 PASS) and `SOURCES_v01.md`.",
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
        "# 037 price review v01 (pre-VO plate boards)",
        "",
        "Gemini, 18 Oct 2026, J0509. Boards only. **No mint. No spend. No merge.**",
        "Prepared from `superconductivity_script_master_v01.md` (92.4 PASS) and `SOURCES_v01.md` so 037's full plate board rows, non-emissive Fast prompts, £0 code graphics, and Teach-on-Screen overlays are ready to re-time the moment long VO locks. Parked for Chief.",
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
        f"- **Quality ({totals['Quality']} rows):** readable faces (Heike Kamerlingh Onnes, Gilles Holst, James Dewar, Walther Meissner, Robert Ochsenfeld, John Bardeen, Leon Cooper, Robert Schrieffer, Christophorus Buys Ballot), levitation & MRI scenes, and the 2 Explorer beats.",
        f"- **Fast ({totals['Fast']} rows, non-emissive):** daylight prop and laboratory shots (copper coils & brass Wheatstone bridge box, quadruple-distilled mercury U-tube capillary & mirror galvanometer pan, 3-object callback bench, Leiden brass cascade valves & frosted Dewar, 1914 unplugged superconducting lead ring & deflected compass needle, quadruple mercury distillation glassware). Zero candles, flames, sparks, or glowing elements on Fast.",
        f"- **£0 code graphics ({totals['code_graphic']} rows):**",
        "  1. `P1:04_onnes_8_april_1911_mercury_resistance_cliff_4_20k_chart` — Kamerlingh Onnes's 8 April 1911 mercury curve plunging >10,000× across 0.01 K at 4.20 K (−268.95 °C) from 0.115 Ω to <10⁻⁵–10⁻⁷ Ω (`SCALE: within a single hundredth of a degree at four point two Kelvin, the electrical friction inside solid mercury didn't fade away — it fell off a cliff by more than ten thousand times to zero`)",
        "  2. `P1:06_cryogenic_temperature_bar_293k_to_deep_space_2_7k_and_leiden_1_04k` — cryogenic bar comparing 293 K room temp, 77 K liquid N₂, 20.4 K liquid H₂, 4.22 K liquid He, 2.7 K deep space, and 1.04 K Leiden pumped helium (`SCALE: at one point zero four degrees above Absolute Zero, Kamerlingh Onnes's glass flask in the Netherlands was more than twice as cold as the deepest voids of outer space`)",
        "  3. `P2:02_onnes_10_july_1908_four_stage_cascade_liquefier_60ml_helium_diagram` — Kamerlingh Onnes's 10 July 1908 4-stage cascade liquefier (183 K → 169 K → 77 K → 20.4 K → 60 mL liquid He at 4.22 K, pumped to 1.04 K) (`SCALE: sixty millilitres of liquid helium — barely enough to fill an espresso cup — made a room in Leiden colder than any natural place in the known universe`)",
        "  4. `P3:02_onnes_1911_comm_122b_mercury_0_115_to_zero_ohms_and_lead_tin_chart` — Leiden Comm. No. 122b mercury cliff (0.115 Ω at 4.3 K → <10⁻⁵ Ω at 4.20 K) alongside tin (3.7 K), lead (7.2 K) & 1914 persistent ring (>100,000-yr bound) (`SCALE: a current started inside a superconducting ring with the battery unplugged will keep circling longer than the entire history of human civilisation`)",
        "  5. `P4:02_meissner_effect_flux_expulsion_and_bcs_cooper_pair_phonon_diagram` — October 1933 Meissner Effect magnetic flux expulsion (`B = 0`) + February 1957 BCS phonon-mediated Cooper pairs (`SCALE: forty-six years elapsed between Kamerlingh Onnes seeing zero resistance in 1911 and Bardeen, Cooper, and Schrieffer explaining how two negative electrons team up through crystal vibrations in 1957`)",
        "  6. `P5:01_timeline_1908_1987_and_tc_4_2k_to_35k_to_93k_ybco_above_77k_chart` — completed 5-date timeline (1908 → 1987) + Tc climbing from 4.2 K (1911 Hg) to 35 K (1986 LBCO) and 93 K (1987 YBCO) above 77 K liquid N₂ (`SCALE: jumping from 4.2 Kelvin liquid helium in 1911 to 93 Kelvin YBCO in 1987 meant cooling a superconductor with liquid nitrogen that costs pennies a litre instead of rare helium near Absolute Zero`)",
        f"- **£0 verified reuse ({totals['reuse']} row):** `P5:04_table_three_callback` uses the 2.40 s unused moving tail `[5.50s..7.90s]` of `P1:07_table_three_props_dewar_flask_blue_notebook_levitating_magnet_dish`.",
        "",
        "## Mint order",
        "",
        "006 > 007 > 008 > 009 > 010 > 011 > 012 > 013 > 014 > 015 > 016 > 017 > 018 > 019 > 020 > 021 > 022 > 023 > 024 > 025 > 026 > 027 > 028 > 029 > 030 > 031 > 032 > 033 > 034 > 035 > 036 > 037. `generation_authorized` is `false` on every row.",
    ])
    (EDIT / "PRICE_REVIEW_v01.md").write_text("\n".join(pr_lines) + "\n")
    print(f"037 v01 boards written: {totals['rows']} rows, Flow expected={totals['flow_credits_expected']}")


if __name__ == "__main__":
    main()
