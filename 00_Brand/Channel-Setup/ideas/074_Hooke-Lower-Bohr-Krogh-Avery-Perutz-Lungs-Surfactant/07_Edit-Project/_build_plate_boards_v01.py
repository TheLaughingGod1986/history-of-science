#!/usr/bin/env python3
"""HOS 074 (The Lungs: Why 300 Million Air Sacs Don't Collapse) pre-VO plate boards v01. J0706. No mint, no spend.

Built from 00_Brand/Channel-Setup/ideas/074_Hooke-Lower-Bohr-Krogh-Avery-Perutz-Lungs-Surfactant/lungs_script_master_v01.md
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
        "Part 01 — The Tennis-Court Sponge in Your Chest & the Copenhagen Bubble Showdown",
        [
            ("01_bronchial_tree_zooming_into_300m_alveoli_haemoglobin_t_to_r_snap_and_surfactant_monolayer", 0.0, 5.5, "A", False, "300 MILLION MICROSCOPIC AIR SACS", "Quality",
             "Quality: Short frame 0 / answer image (0:03) + a breathing human chest zooms down the branching bronchial tree into 300 million microscopic wet alveoli (0.2 mm diameter, 70–100 m2 tennis-court surface area), where oxygen molecules diffuse across a 0.5-micrometre barrier to snap a 4-subunit haemoglobin protein from its Tense (T) to Relaxed (R) state while a phospholipid surfactant monolayer stops the wet air sac from collapsing.",
             STYLE + "Split anatomical-and-molecular scene: on the left, a branching bronchial tree zooms into a cluster of wet microscopic alveoli lined with a golden surfactant film; on the right, oxygen spheres cross a thin capillary wall and click a four-subunit crimson haemoglobin protein into its open state." + QUAL_TAIL,
             {"kind": "WHEN", "label": "COPENHAGEN, 1910", "timeline_step": "1/3 · Oct 1667 & 1904 (Robert Hooke & Richard Lower prove venous blood turns scarlet by absorbing air; Christian Bohr discovers the sigmoidal haemoglobin O2 curve and Bohr Effect)", "hold_s": 3.5}),
            ("02_hooke_lower_1667_bohr_krogh_1904_1910_neergaard_avery_1959_and_perutz_1960_split", 5.5, 6.0, "B", False, "SCARLET BLOOD, SEVEN LITTLE DEVILS, LUNG SURFACTANT", "Quality",
             "Quality: complex three-part composition (Robert Hooke and Richard Lower at the Royal Society in London in October 1667 ventilating a lung with bellows as dark venous blood turns bright scarlet; Christian Bohr in Copenhagen in 1904 alongside August Krogh and Marie Krogh in 1910 reading their microtonometer gas bubble; and Kurt von Neergaard in Basel in 1929 with Mary Ellen Avery in Boston in May 1959 measuring infant lung surface tension alongside Max Perutz in Cambridge on 13 February 1960 unveiling the 3D X-ray model of haemoglobin).",
             STYLE + "Three-panel period composition: on the left, Robert Hooke and Richard Lower in 1667 London pumping double bellows into a lung as blood turns bright scarlet; in the centre, August and Marie Krogh in 1910 Copenhagen examining a tiny gas bubble inside a glass microtonometer beside Christian Bohr; on the right, Mary Ellen Avery in 1959 Boston at her surface-film trough alongside Max Perutz in 1960 Cambridge holding his 3D haemoglobin model." + QUAL_TAIL,
             None),
            ("03_alveoli_unfolding_into_75m2_tennis_court_and_surfactant_preventing_laplace_bubble_collapse", 11.5, 6.0, "C", False, "A TENNIS COURT FOLDED IN YOUR CHEST", "Quality",
             "Quality: complex visual reveal (an alveolus unfolds into a full 75-square-metre tennis court just 0.5 micrometres thick, while side by side a surfactant-coated alveolus stays effortlessly open on exhalation and a surfactant-free wet bubble snaps shut under Laplace surface tension).",
             STYLE + "In a bright anatomical hall, a cluster of microscopic lung air sacs unfolds across the floor into a full-sized tennis court while above it a surfactant-lined wet bubble breathes smoothly beside an unlined bubble that snaps shut." + QUAL_TAIL,
             {"kind": "WHEN", "label": "OCTOBER 1667 · 1904 · 1910 · 1929 · MAY 1959 · 13 FEBRUARY 1960", "timeline_step": "1/3 · Oct 1667 & 1904 (Hooke, Lower & Bohr) · 2/3 · 1910 (August & Marie Krogh) · 3/3 · May 1959 & 13 Feb 1960 (Avery & Perutz)", "hold_s": 3.5}),
            ("04_hooke_1667_bohr_1904_krogh_1910_avery_1959_and_perutz_1960_lung_diffusion_surfactant_chart", 17.5, 8.0, "E", False, "300M ALVEOLI (70–100 M2, 0.5 µM BARRIER) · KROGH PASSIVE O2 DIFFUSION · BOHR/PERUTZ 4-SUBUNIT HAEMOGLOBIN & AVERY SURFACTANT (<5 DYN/CM)", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked Alveolar Diffusion, Haemoglobin Cooperativity & Pulmonary Surfactant chart from Hooke & Lower (October 1667 / 1669 Tractatus de Corde), Christian Bohr, Hasselbalch & Krogh (1904 Skand. Arch. Physiol. 16: 402–412), August & Marie Krogh (1910 Skand. Arch. Physiol. 23: 179–278), Neergaard (1929 Z. Gesamte Exp. Med. 66: 373–394), Avery & Mead (May 1959 AMA J. Dis. Child. 97: 517–523), and Perutz et al. (13 February 1960 Nature 185: 416–422) shows alveolar oxygen tension always exceeding arterial blood PO2 (~100 vs ~95 mmHg, passive diffusion across 300 million alveoli / ~70–100 m2), the sigmoidal O2 dissociation curve (T-to-R cooperative shift + right-shift Bohr Effect), and DPPC surfactant slashing alveolar surface tension from ~50 to <5 dyn/cm.",
             {"kind": "DATA", "label": "300M ALVEOLI (70–100 M2), KROGH PASSIVE DIFFUSION, BOHR/PERUTZ HAEMOGLOBIN S-CURVE & AVERY SURFACTANT (<5 DYN/CM)", "detail": "Inked alveolar gas-exchange, haemoglobin S-curve & surfactant surface-tension chart on period paper showing 300,000,000 alveoli (~70–100 m2 area, 0.5 µm barrier), Krogh's passive diffusion gradient (alveolar PO2 > capillary PO2), Bohr & Perutz's 4-subunit haemoglobin cooperative O2 curve, and Avery's pulmonary surfactant lowering surface tension from ~50 dyn/cm to near 0 dyn/cm on exhalation", "scale": "your two lungs fold the surface area of an entire singles tennis court inside your ribcage — and every red blood cell races across that court in three-quarters of a second, snapping up oxygen through a wall fifty times thinner than tissue paper", "who_card": "Robert Hooke (1635–1703) — English natural philosopher and experimentalist · Richard Lower (1631–1691) — English physician and physiologist · Christian Bohr (1855–1911) — Danish physiologist · August Krogh (1874–1949) — Danish zoophysiologist · Marie Krogh (1874–1943) — Danish physician and physiologist · Mary Ellen Avery (1927–2011) — American paediatrician · Max Perutz (1914–2002) — Austrian-British molecular biologist", "when_stamp": "October 1667 · 1904 · 1910 · 1929 · May 1959 · 13 February 1960", "hold_s": 3.8}),
            ("05_1669_lower_tractatus_book_glass_microtonometer_and_1910_skand_arch_offprint_pan", 25.5, 5.5, "A", False, "THE TENNIS-COURT SPONGE IN YOUR CHEST", "Fast",
             "Fast: daylight macro pan across Richard Lower's 1669 Tractatus de Corde volume, a fine capillary glass microtonometer tube, and a 1910 Skandinavisches Archiv für Physiologie offprint on an oak bench between code graphics so two full-frame graphics never run back to back. Nothing emissive, no face.",
             STYLE + "In crisp daylight on an oak physiology bench, the camera pans smoothly across a leather-bound 1669 medical book, a brass-mounted capillary glass microtonometer, and an open 1910 physiology journal." + FAST_TAIL,
             None),
            ("06_august_and_marie_krogh_1910_skand_arch_microtonometer_seven_little_devils_diffusion_chart", 31.0, 8.0, "E", False, "COPENHAGEN, 1910", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period parchment, an inked August & Marie Krogh Microtonometer & 'Seven Little Devils' Diffusion diagram (from August Krogh & Marie Krogh, 1910 Skand. Arch. Physiol. 23: 179–278) shows a microscopic air bubble equilibrated against circulating arterial blood inside a capillary glass tube, plotting alveolar O2 pressure strictly above arterial blood O2 pressure under every condition (rest, exercise, and low oxygen).",
             {"kind": "DATA", "label": "1910 AUGUST & MARIE KROGH ('SEVEN LITTLE DEVILS'): ALVEOLAR PO2 ALWAYS EXCEEDS ARTERIAL PO2 (100% PASSIVE DIFFUSION)", "detail": "Inked August & Marie Krogh (1910 Skand. Arch. Physiol. 23: 179–278) microtonometer alveolar vs arterial oxygen partial pressure table proving alveolar PO2 is always higher than arterial blood PO2 (refuting active oxygen secretion and proving 100% passive physical diffusion)", "scale": "measuring the oxygen pressure of a single microscopic air bubble inside a hair-thin glass tube proved that your lungs don't need a single pump to push oxygen into your blood — oxygen flows downhill by itself like crowd-surfers pouring through an open stadium gate", "hold_s": 3.8}),
            ("07_table_three_props_1667_hooke_bellows_1910_krogh_microtonometer_and_1960_perutz_haemoglobin_model", 39.0, 5.5, "C", False, "1667 TO 1960", "Fast",
             "Fast: daylight prop table (callback source for Part 05: Robert Hooke's 1667 double wooden fireplace bellows, August and Marie Krogh's 1910 capillary glass microtonometer, and Max Perutz's 1960 stacked balsa-wood haemoglobin model). Nothing emissive.",
             STYLE + "On an oak workbench in soft window light sit three objects side by side: a pair of seventeenth-century wooden double bellows, a brass-and-glass capillary microtonometer, and a layered balsa-wood model of the four-subunit haemoglobin molecule." + FAST_TAIL,
             None),
            ("08_explorer_watching_first_oxygen_ball_pop_open_four_seat_haemoglobin_carriage_while_spraying_surfactant", 62.0, 5.5, "A", True, None, "Quality",
             "Quality: Explorer beat 1 (locked character reference, after 1:00).",
             STYLE + "Standing inside a translucent alveolar chamber beside a four-seat crimson haemoglobin carriage, the Explorer watches a blue oxygen sphere roll into the first seat and mechanically pop the other three seats wide open, while spraying a fine golden surfactant mist onto the curved chamber wall." + EXP_TAIL,
             None),
            ("09_august_and_marie_krogh_1910_copenhagen_measuring_gas_bubble_in_glass_microtonometer", 67.5, 5.5, "B", False, "THE SEVEN LITTLE DEVILS PROOF", "Quality",
             "Quality: readable faces (in Copenhagen in 1910, August Krogh and Marie Krogh peer through a microscope rule at a tiny gas bubble inside their glass microtonometer).",
             STYLE + "In a 1910 Copenhagen laboratory, August Krogh and Marie Krogh lean together over a brass microscope scale, measuring the diameter of a tiny gas bubble trapped inside a capillary glass microtonometer." + QUAL_TAIL,
             {"kind": "WHEN", "label": "COPENHAGEN, 1910", "timeline_step": "2/3 · 1910 (August & Marie Krogh publish 'The Seven Little Devils' proving passive alveolar O2 diffusion)", "hold_s": 3.5}),
        ],
    ),
    (
        2,
        "Part 02 — October 1667, 1904 & 1910: Hooke and Lower's Scarlet Blood, Christian Bohr's Curve & the Kroghs' 'Seven Little Devils'",
        [
            ("01_hooke_lower_24_oct_1667_london_scarlet_blood_and_bohr_krogh_1904_1910_copenhagen", 73.0, 6.5, "A", False, "PASSIVE DIFFUSION ACROSS A TENNIS COURT", "Quality",
             "Quality: readable faces (English natural philosopher Robert Hooke and physician Richard Lower at the Royal Society on 24 October 1667 ventilating a lung with double bellows as dark venous blood turns bright scarlet, dissolving to Danish physiologist Christian Bohr in 1904 and August & Marie Krogh in Copenhagen in 1910 measuring their microtonometer bubble).",
             STYLE + "Split period scene: on the left in October 1667 London, Robert Hooke and Richard Lower work double bellows to keep a lung inflated as dark venous blood turns bright crimson; on the right in 1910 Copenhagen, Christian Bohr looks on as August and Marie Krogh read their capillary microtonometer." + QUAL_TAIL,
             {"kind": "FACT", "label": "Passive diffusion across a tennis court", "when_stamp": "1661 · 24 October 1667 · 1669 · 1904 · 1910 · 1920", "timeline_step": "1/3 · Oct 1667, 1904 & 1910 (Hooke & Lower's scarlet blood; Christian Bohr's CO2 Bohr Effect; August & Marie Krogh's 'Seven Little Devils')", "hold_s": 3.8}),
            ("02_bohr_1904_co2_shift_and_krogh_1910_seven_little_devils_alveolar_diffusion_chart", 79.5, 8.0, "E", False, "1904 BOHR, HASSELBALCH & KROGH (SKAND. ARCH.: CO2 BOHR EFFECT) & 1910 AUGUST & MARIE KROGH ('SEVEN LITTLE DEVILS' PASSIVE DIFFUSION)", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked Christian Bohr, Hasselbalch & Krogh (1904 Skand. Arch. Physiol. 16: 402–412) CO2 Bohr-Effect oxygen dissociation shift & August and Marie Krogh (1910 Skand. Arch. Physiol. 23: 179–278 'Seven Little Devils') alveolar-to-arterial O2 diffusion curve.",
             {"kind": "DATA", "label": "1904 BOHR EFFECT (CO2 RIGHT-SHIFT) & 1910 KROGH 'SEVEN LITTLE DEVILS' ALVEOLAR-ARTERIAL PO2 GRADIENT", "detail": "Inked Christian Bohr, Hasselbalch & Krogh (1904 Skand. Arch. Physiol. 16: 402–412) CO2 Bohr-Effect oxygen dissociation shift & August and Marie Krogh (1910 Skand. Arch. Physiol. 23: 179–278 'Seven Little Devils') alveolar-to-arterial O2 diffusion curve on period paper", "scale": "August and Marie Krogh proved that your lungs don't need an energy-burning oxygen pump because evolution folded a tennis court of membrane fifty times thinner than tissue paper inside your chest — letting oxygen pour into your blood by pure physical diffusion", "hold_s": 3.8}),
            ("03_copenhagen_1910_seven_skand_arch_offprints_and_capillary_microtonometer_closeup", 87.5, 6.5, "B", False, "1910 — PASSIVE ALVEOLAR DIFFUSION PROVED", "Fast",
             "Fast: daylight macro shot of the seven 1910 Skandinavisches Archiv für Physiologie offprints fanned beside the brass-and-glass capillary microtonometer and graduated gas burettes on a bench. Nothing emissive, no face.",
             STYLE + "In crisp daylight on a 1910 Copenhagen laboratory bench, seven printed journal papers sit fanned beside a glass capillary microtonometer and graduated mercury gas burettes." + FAST_TAIL,
             None),
            ("04_cutaway_alveolar_sac_and_capillary_network_model_on_oak_table_pan", 94.0, 5.5, "C", False, "0.5-MICROMETRE BLOOD-GAS BARRIER", "Fast",
             "Fast: daylight close-up pan across a sculpted anatomical model of grape-like alveolar air sacs wrapped in a fine crimson-and-blue capillary mesh on an oak table. Nothing emissive, no face.",
             STYLE + "In bright window light on an oak table, a sculpted anatomical model shows clustered alveolar air sacs enveloped in a delicate lattice of blue and crimson capillary vessels." + FAST_TAIL,
             None),
        ],
    ),
    (
        3,
        "Part 03 — 1937 – 13 February 1960: Max Perutz's 22-Year X-Ray Quest & the Molecular Lung (Haemoglobin) — Midpoint Twist",
        [
            ("01_max_perutz_and_john_kendrew_13_feb_1960_cambridge_haemoglobin_xray_model", 99.5, 6.5, "A", False, "IRON MOVES 0.04 NANOMETRES", "Quality",
             "Quality: readable faces (Austrian-British molecular biologist Max Perutz and British molecular biologist John C. Kendrew at the Cavendish Laboratory in Cambridge on 13 February 1960 with X-ray diffraction plates of mercury-soaked horse haemoglobin crystals and the stacked balsa-wood 3D electron-density model of haemoglobin).",
             STYLE + "In the 1960 Cavendish Laboratory in Cambridge, Max Perutz and John Kendrew stand beside an X-ray diffraction film viewer, pointing to the four heme pockets on their stacked balsa-wood 3D model of haemoglobin." + QUAL_TAIL,
             {"kind": "FACT", "label": "Iron moves 0.04 nanometres", "who_card": "John C. Kendrew (1917–1997) — British molecular biologist", "when_stamp": "1862 · 1925 · 1937 · 1953 · 1958 · 13 February 1960 · 1962", "timeline_step": "3/3 · 13 Feb 1960 (Max Perutz solves the 3D X-ray crystal structure of haemoglobin at 5.5 Å resolution)", "hold_s": 3.8}),
            ("02_perutz_13_feb_1960_nature_haemoglobin_t_to_r_switch_and_sigmoidal_o2_curve_chart", 106.0, 8.0, "E", False, "13 FEB 1960 PERUTZ ET AL. (NATURE): 4-SUBUNIT HAEMOGLOBIN T-TO-R SWITCH (0.04 NM FE2+ SHIFT, 15° ROTATION) & SIGMOIDAL O2 CURVE", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked Max Perutz et al. (13 February 1960 Nature 185: 416–422 & 1970 Nature 228: 726–734) 4-subunit haemoglobin T-state (deoxy) to R-state (oxy) conformational switch & hyperbolic myoglobin vs sigmoidal haemoglobin O2 binding curve.",
             {"kind": "DATA", "label": "13 FEB 1960 PERUTZ HAEMOGLOBIN 3D STRUCTURE (0.04 NM IRON SHIFT → 15° SUBUNIT ROTATION) & SIGMOIDAL O2 CURVE", "detail": "Inked Max Perutz et al. (13 February 1960 Nature 185: 416–422 & 1970 Nature 228: 726–734) 4-subunit haemoglobin T-state (deoxy) to R-state (oxy) conformational switch & hyperbolic myoglobin vs sigmoidal haemoglobin O2 binding curve on period paper", "scale": "when the first oxygen molecule lands on haemoglobin, it tugs an iron atom by less than half the width of a single hydrogen atom — yet that tiny lever pull twists the entire ten-thousand-atom protein by fifteen degrees and throws open the doors for the next three oxygens", "hold_s": 3.8}),
            ("03_cambridge_1960_ruby_haemoglobin_crystals_xray_diffraction_plate_and_balsa_slices_closeup", 114.0, 6.5, "B", False, "13 FEBRUARY 1960 — 3D HAEMOGLOBIN STRUCTURE", "Fast",
             "Fast: daylight macro shot of a glass dish of ruby-red horse haemoglobin crystals beside a spotted circular X-ray diffraction film and contour-cut balsa-wood electron-density slices on a Cambridge bench. Nothing emissive, no face.",
             STYLE + "In crisp daylight on a 1960 Cambridge workbench, a glass dish of dark red haemoglobin crystals sits beside a spotted circular X-ray diffraction plate and stacked balsa-wood contour sheets." + FAST_TAIL,
             None),
            ("04_sculpted_four_subunit_haemoglobin_tetramer_with_four_heme_iron_rings_model_pan", 120.5, 5.5, "C", False, "TENSE (DEOXY) TO RELAXED (OXY) SWITCH", "Fast",
             "Fast: daylight close-up pan across a sculpted four-subunit haemoglobin model showing two alpha and two beta chains cradling four flat porphyrin heme rings with central iron spheres on an oak table. Nothing emissive, no face.",
             STYLE + "In bright window light on an oak table, a sculpted four-subunit protein model displays four folded globin chains each holding a flat crimson heme ring with a central silver iron sphere." + FAST_TAIL,
             None),
        ],
    ),
    (
        4,
        "Part 04 — 1929, 1957 & May 1959: Kurt von Neergaard, John Clements & Mary Ellen Avery's Discovery of Pulmonary Surfactant",
        [
            ("01_neergaard_1929_clements_1957_and_mary_ellen_avery_jere_mead_may_1959_boston_surfactant", 126.0, 6.5, "A", False, "SOAP FILM SAVES NEWBORNS", "Quality",
             "Quality: readable faces (Swiss physician Kurt von Neergaard in Basel in 1929 and American physiologist John A. Clements in 1957, dissolving to American paediatrician Mary Ellen Avery and physiologist Jere Mead in Boston in May 1959 measuring infant lung surface tension on their Langmuir-Wilhelmy surface film balance).",
             STYLE + "Split period scene: on the left, Kurt von Neergaard in 1929 Basel and John Clements in 1957 study lung pressure-volume curves; on the right in May 1959 Boston, Mary Ellen Avery and Jere Mead measure the surface tension of lung extracts on a brass surface-film balance trough." + QUAL_TAIL,
             {"kind": "FACT", "label": "Soap film saves newborns", "who_card": "Kurt von Neergaard (1887–1947) — Swiss physician and physiologist · John A. Clements (1923–2024) — American pulmonary physiologist · Jere Mead (1920–2009) — American respiratory physiologist", "when_stamp": "1929 · 1957 · May 1959 · January 1980", "timeline_step": "3/3 · 1929, 1957 & May 1959 (Neergaard, Clements & Mary Ellen Avery discover pulmonary surfactant and the cause of newborn RDS)", "hold_s": 3.8}),
            ("02_neergaard_1929_hysteresis_and_avery_mead_may_1959_surfactant_surface_tension_chart", 132.5, 8.0, "E", False, "1929 NEERGAARD (AIR VS SALINE LUNG HYSTERESIS) & MAY 1959 AVERY & MEAD (AMA J. DIS. CHILD.: <5 DYN/CM NORMAL VS 30.4 DYN/CM RDS)", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked Kurt von Neergaard (1929 Z. Gesamte Exp. Med. 66: 373–394) air vs saline lung pressure-volume hysteresis curve & Mary Ellen Avery and Jere Mead (May 1959 AMA J. Dis. Child. 97: 517–523) Langmuir trough minimum lung surface-tension table (normal lungs ~5–7 dyn/cm vs premature hyaline-membrane infant lungs ~30.4 dyn/cm).",
             {"kind": "DATA", "label": "1929 NEERGAARD AIR/SALINE HYSTERESIS & MAY 1959 AVERY & MEAD SURFACE TENSION (~5 DYN/CM NORMAL VS 30.4 DYN/CM PREMATURE RDS)", "detail": "Inked Kurt von Neergaard (1929 Z. Gesamte Exp. Med. 66: 373–394) air vs saline lung pressure-volume hysteresis curve & Mary Ellen Avery and Jere Mead (May 1959 AMA J. Dis. Child. 97: 517–523) Langmuir trough minimum lung surface-tension table (normal lungs ~5–7 dyn/cm vs premature hyaline-membrane infant lungs ~30.4 dyn/cm) on period paper", "scale": "without Mary Ellen Avery's phospholipid surfactant soap, inflating a newborn baby's wet microscopic lung bubbles on every breath is like trying to blow up three hundred million wet party balloons whose walls are glued together with superglue", "hold_s": 3.8}),
            ("03_boston_1959_langmuir_wilhelmy_surface_balance_trough_and_platinum_strip_closeup", 140.5, 6.5, "B", False, "MAY 1959 — PULMONARY SURFACTANT DEFICIENCY", "Fast",
             "Fast: daylight macro shot of the 1959 Boston Langmuir-Wilhelmy surface film balance trough with its hanging platinum strip, torsion dial reading 5 dynes/cm, and May 1959 AMA Journal of Diseases of Children offprint on a bench. Nothing emissive, no face.",
             STYLE + "In crisp daylight on a 1959 Boston laboratory bench, a rectangular Teflon-lined surface trough with a suspended platinum strip and torsion scale sits beside an open medical journal." + FAST_TAIL,
             None),
            ("04_explorer_coating_connected_glass_lung_bubbles_with_dppc_surfactant_to_stop_laplace_collapse", 147.0, 5.5, "B", True, None, "Quality",
             "Quality: Explorer beat 2 (locked character reference).",
             STYLE + "Standing beside two wet glass lung bubbles connected by a brass Y-tube, the Explorer watches the smaller unlined bubble shrink into the larger one, then coats both interiors with golden surfactant spheres so both bubbles expand and contract evenly together." + EXP_TAIL,
             None),
        ],
    ),
    (
        5,
        "Part 05 — Saving Premature Babies Around the World — & How One White-Eyed Fruit Fly Mapped Our Chromosomes",
        [
            ("01_timeline_1667_1980_and_surfactant_neonatal_survival_chart", 152.5, 8.5, "E", False, "1667–1980 TIMELINE · HOOKE/LOWER, BOHR, AUGUST & MARIE KROGH, NEERGAARD/CLEMENTS/AVERY SURFACTANT & PERUTZ HAEMOGLOBIN", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, the 3-era timeline completes: Oct 1667 & 1904 (Robert Hooke & Richard Lower prove venous blood turns scarlet by absorbing air in the lungs; Christian Bohr discovers the sigmoidal haemoglobin O2 curve and the Bohr Effect) · 1910 (August Krogh & Marie Krogh publish 'The Seven Little Devils' microtonometer proof that oxygen crosses the 300 million alveoli by 100% passive diffusion, winning the 1920 Nobel Prize) · May 1959 & 13 Feb 1960 (Kurt von Neergaard 1929, John Clements 1957 & Mary Ellen Avery May 1959 discover pulmonary surfactant and the cause of newborn respiratory distress; Max Perutz solves the 3D X-ray structure of haemoglobin, winning the 1962 Nobel Prize).",
             {"kind": "DATA", "label": "1667–1980 LUNGS, HAEMOGLOBIN & SURFACTANT TIMELINE · HOOKE/LOWER, BOHR, KROGH, AVERY & PERUTZ", "detail": "Animated timeline (1667 → 1980) alongside an inked summary of alveolar diffusion, haemoglobin T-to-R cooperativity, and exogenous surfactant therapy", "scale": "from fireplace bellows in seventeenth-century London to a microscopic gas bubble in Copenhagen, an X-ray beam in Cambridge, and a soap trough in Boston, scientists unlocked the tennis-court sponge that keeps us breathing", "when_stamp": "1667–1980", "timeline_step": "3/3 · 1667–1980 timeline complete", "hold_s": 3.8}),
            ("02_surfactant_vial_beside_3d_haemoglobin_and_alveolar_model_on_plinth_pan", 161.0, 5.5, "A", False, "MILLIONS OF NEWBORN LIVES SAVED", "Fast",
             "Fast: daylight close-up of a glass vial of pulmonary surfactant suspension beside a sculpted alveolar cluster and 4-subunit haemoglobin model on a wooden museum plinth. Nothing emissive, no face.",
             STYLE + "In crisp daylight on a wooden museum plinth, a small glass vial of white pulmonary surfactant sits beside a sculpted alveolar air-sac model and a four-subunit haemoglobin model." + FAST_TAIL,
             None),
            ("03_flemming_1879_mitosis_boveri_sutton_1902_stevens_1905_xy_and_morgan_sturtevant_1910_1913_fly_room_handoff", 166.5, 6.5, "C", False, "CHROMOSOMES, MITOSIS & THE FLY ROOM", "Quality",
             "Quality: readable faces (Walther Flemming in Kiel in 1879 staining salamander mitosis, Theodor Boveri and Walter Sutton in 1902–1903 alongside Nettie Stevens in 1905 discovering X and Y chromosomes, and Thomas Hunt Morgan in May 1910 with 19-year-old Alfred Sturtevant in January 1913 in Columbia's Fly Room — handoff to 075 Chromosomes, Mitosis & the Fly Room).",
             STYLE + "Split period scene: on the left, Walther Flemming in 1879 Kiel and Nettie Stevens in 1905 Bryn Mawr study stained chromosomes through brass microscopes; on the right in 1910–1913 New York, Thomas Hunt Morgan and young Alfred Sturtevant examine milk bottles of fruit flies beside a linear chromosome map." + QUAL_TAIL,
             {"kind": "WHEN", "label": "1879 · 1902 · 1905 · MAY 1910 · JANUARY 1913", "hold_s": 3.5}),
            ("04_table_three_callback", 173.0, 2.4, "C", False, None, "reuse",
             "Reuse: verified unused moving window [5.50s..7.90s] of P1:07_table_three_props_1667_hooke_bellows_1910_krogh_microtonometer_and_1960_perutz_haemoglobin_model (callback, £0).",
             "Reuse P1:07_table_three_props_1667_hooke_bellows_1910_krogh_microtonometer_and_1960_perutz_haemoglobin_model [5.50s..7.90s] (2.40s distinct non-overlapping tail window from 8.00s source clip).",
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
                row["reuse_of"] = "P1:07_table_three_props_1667_hooke_bellows_1910_krogh_microtonometer_and_1960_perutz_haemoglobin_model"
                row["reuse_window_s"] = [5.5, 7.9]
                row["reuse_audit"] = {
                    "source_row": "P1:07_table_three_props_1667_hooke_bellows_1910_krogh_microtonometer_and_1960_perutz_haemoglobin_model",
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
            "film": "074_Hooke-Lower-Bohr-Krogh-Avery-Perutz-Lungs-Surfactant",
            "part": p_idx,
            "title": p_title,
            "version": "v01",
            "timing_status": "pre_vo_script_clock (built from lungs_script_master_v01.md; retimes onto Scribe STT once VO locks)",
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
        "film": "074_Hooke-Lower-Bohr-Krogh-Avery-Perutz-Lungs-Surfactant",
        "version": "v01",
        "date": "2026-10-20",
        "owner": "gemini (J0706)",
        "status": "PRE_VO_BOARDS_V01_NO_MINT",
        "generation_authorized": False,
        "script": "00_Brand/Channel-Setup/ideas/074_Hooke-Lower-Bohr-Krogh-Avery-Perutz-Lungs-Surfactant/lungs_script_master_v01.md",
        "sources": "00_Brand/Channel-Setup/ideas/074_Hooke-Lower-Bohr-Krogh-Avery-Perutz-Lungs-Surfactant/SOURCES_v01.md",
        "credit_snapshot": {
            "flow_balance": 23740,
            "flow_floor": 0,
            "flow_read_at": "2026-10-15T21:42:22Z",
            "vertex_promo_gbp": 71.02,
            "vertex_usable_gbp": 70.02,
        },
        "totals": totals,
        "per_part": per_part_summary,
        "mint_order": "006 > 007 > 008 > 009 > 010 > 011 > 012 > 013 > 014 > 015 > 016 > 017 > 018 > 019 > 020 > 021 > 022 > 023 > 024 > 025 > 026 > 027 > 028 > 029 > 030 > 031 > 032 > 033 > 034 > 035 > 036 > 037 > 038 > 039 > 040 > 041 > 042 > 043 > 044 > 045 > 046 > 047 > 048 > 049 > 050 > 051 > 052 > 053 > 054 > 055 > 056 > 057 > 058 > 059 > 060 > 061 > 062 > 063 > 064 > 065 > 066 > 067 > 068 > 069 > 070 > 071 > 072 > 073 > 074 > 075 > 076 > 077. Nothing in 074 is generation_authorized.",
    }
    (EDIT / "PICTURE_PLAN_v01.json").write_text(json.dumps(plan, indent=2) + "\n")

    sl = [
        "# 074 The Lungs: Why 300 Million Air Sacs Don't Collapse — Shot list & plate boards v01 (pre-VO)",
        "",
        "Gemini, 20 Oct 2026, J0706. Built from `lungs_script_master_v01.md` (`91.0/100 PASS`) and `SOURCES_v01.md`.",
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
        "# 074 price review v01 (pre-VO plate boards)",
        "",
        "Gemini, 20 Oct 2026, J0706. Boards only. **No mint. No spend. No merge.**",
        "Prepared from `lungs_script_master_v01.md` (`91.0/100 PASS`) and `SOURCES_v01.md` so 074's full plate board rows, non-emissive Fast prompts, £0 code graphics, and Teach-on-Screen overlays are ready to re-time the moment long VO locks. Parked for Chief.",
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
        f"- **Quality ({totals['Quality']} rows):** readable faces (Robert Hooke, Richard Lower, Christian Bohr, August Krogh, Marie Krogh, Max Perutz, John C. Kendrew, Kurt von Neergaard, John A. Clements, Mary Ellen Avery, Jere Mead, Walther Flemming, Nettie Stevens, Thomas Hunt Morgan, Alfred Sturtevant), 24 October 1667 Royal Society bellows lung & 1910 Copenhagen `'Seven Little Devils'` microtonometer, 13 February 1960 Cambridge `3D haemoglobin` X-ray structure, May 1959 Boston `pulmonary surfactant` balance trough, and the 2 Explorer beats.",
        f"- **Fast ({totals['Fast']} rows, non-emissive):** daylight prop and laboratory shots (1669 Lower *Tractatus de Corde*, capillary glass microtonometer & 1910 *Skand. Arch.* offprint pan, 3-object callback bench, seven 1910 *Skand. Arch.* papers beside microtonometer & gas burettes, sculpted alveolar sac & capillary mesh model, ruby haemoglobin crystals with X-ray diffraction film & balsa-wood contour slices, sculpted 4-subunit haemoglobin tetramer model, 1959 Langmuir-Wilhelmy surface film balance trough, surfactant vial beside alveolar & haemoglobin models on museum plinth). Zero candles, flames, sparks, or glowing elements on Fast.",
        f"- **£0 code graphics ({totals['code_graphic']} rows):**",
        "  1. `P1:04_hooke_1667_bohr_1904_krogh_1910_avery_1959_and_perutz_1960_lung_diffusion_surfactant_chart` — `300 million` alveoli (`~70–100 m²`, `0.5 µm` barrier), Krogh's passive O₂ diffusion, Bohr/Perutz sigmoidal haemoglobin curve, and Avery's `<5 dyn/cm` surfactant (`SCALE: your two lungs fold the surface area of an entire singles tennis court inside your ribcage — and every red blood cell races across that court in three-quarters of a second, snapping up oxygen through a wall fifty times thinner than tissue paper`)",
        "  2. `P1:06_august_and_marie_krogh_1910_skand_arch_microtonometer_seven_little_devils_diffusion_chart` — August & Marie Krogh (1910 *Skand. Arch. Physiol.* `'Seven Little Devils'`) microtonometer alveolar vs arterial PO₂ table (`SCALE: measuring the oxygen pressure of a single microscopic air bubble inside a hair-thin glass tube proved that your lungs don't need a single pump to push oxygen into your blood — oxygen flows downhill by itself like crowd-surfers pouring through an open stadium gate`)",
        "  3. `P2:02_bohr_1904_co2_shift_and_krogh_1910_seven_little_devils_alveolar_diffusion_chart` — Christian Bohr et al. (1904) CO₂ Bohr Effect & August/Marie Krogh (1910) passive alveolar diffusion curve (`SCALE: August and Marie Krogh proved that your lungs don't need an energy-burning oxygen pump because evolution folded a tennis court of membrane fifty times thinner than tissue paper inside your chest — letting oxygen pour into your blood by pure physical diffusion`)",
        "  4. `P3:02_perutz_13_feb_1960_nature_haemoglobin_t_to_r_switch_and_sigmoidal_o2_curve_chart` — Max Perutz et al. (13 February 1960 *Nature*) 4-subunit haemoglobin `T → R` switch (`0.04 nm` Fe²⁺ shift, `15°` subunit rotation) & sigmoidal O₂ curve (`SCALE: when the first oxygen molecule lands on haemoglobin, it tugs an iron atom by less than half the width of a single hydrogen atom — yet that tiny lever pull twists the entire ten-thousand-atom protein by fifteen degrees and throws open the doors for the next three oxygens`)",
        "  5. `P4:02_neergaard_1929_hysteresis_and_avery_mead_may_1959_surfactant_surface_tension_chart` — Kurt von Neergaard (1929) air/saline lung hysteresis & Mary Ellen Avery and Jere Mead (May 1959 *AMA J. Dis. Child.*) `<5 dyn/cm` normal vs `30.4 dyn/cm` premature RDS surface-tension table (`SCALE: without Mary Ellen Avery's phospholipid surfactant soap, inflating a newborn baby's wet microscopic lung bubbles on every breath is like trying to blow up three hundred million wet party balloons whose walls are glued together with superglue`)",
        "  6. `P5:01_timeline_1667_1980_and_surfactant_neonatal_survival_chart` — completed timeline (1667 → 1980) + exogenous pulmonary surfactant therapy (`SCALE: from fireplace bellows in seventeenth-century London to a microscopic gas bubble in Copenhagen, an X-ray beam in Cambridge, and a soap trough in Boston, scientists unlocked the tennis-court sponge that keeps us breathing`)",
        f"- **£0 verified reuse ({totals['reuse']} row):** `P5:04_table_three_callback` uses the 2.40 s unused moving tail `[5.50s..7.90s]` of `P1:07_table_three_props_1667_hooke_bellows_1910_krogh_microtonometer_and_1960_perutz_haemoglobin_model`.",
        "",
        "## Mint order",
        "",
        "006 > 007 > 008 > 009 > 010 > 011 > 012 > 013 > 014 > 015 > 016 > 017 > 018 > 019 > 020 > 021 > 022 > 023 > 024 > 025 > 026 > 027 > 028 > 029 > 030 > 031 > 032 > 033 > 034 > 035 > 036 > 037 > 038 > 039 > 040 > 041 > 042 > 043 > 044 > 045 > 046 > 047 > 048 > 049 > 050 > 051 > 052 > 053 > 054 > 055 > 056 > 057 > 058 > 059 > 060 > 061 > 062 > 063 > 064 > 065 > 066 > 067 > 068 > 069 > 070 > 071 > 072 > 073 > 074 > 075 > 076 > 077. `generation_authorized` is `false` on every row.",
    ])
    (EDIT / "PRICE_REVIEW_v01.md").write_text("\n".join(pr_lines) + "\n")
    print(f"074 v01 boards written: {totals['rows']} rows, Flow expected={totals['flow_credits_expected']}")


if __name__ == "__main__":
    main()
