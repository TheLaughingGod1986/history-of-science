#!/usr/bin/env python3
"""HOS 076 (The Pacemaker: One Wrong Resistor Saved Millions) pre-VO plate boards v01. J0706. No mint, no spend.

Built from 00_Brand/Channel-Setup/ideas/076_Ringer-Einthoven-Keith-Flack-Greatbatch-Heart-Pacemaker/heart_script_master_v01.md
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
        "Part 01 — The Salt-Bucket Monster in Leiden & the Wrong Resistor in Buffalo",
        [
            ("01_beating_heart_sa_node_his_purkinje_wave_p_q_r_s_t_trace_and_greatbatch_epoxy_pacemaker", 0.0, 5.5, "A", False, "100,000 HEARTBEATS EVERY DAY", "Quality",
             "Quality: Short frame 0 / answer image (0:03) + a human heart beats rhythmically as an electrical wave sweeps from the crescent-shaped sinoatrial (SA) node at the top of the right atrium, pauses 0.1 seconds at the AV node, and races down the Bundle of His and Purkinje fibres to trace a crisp P–Q–R–S–T electrocardiogram wave alongside Wilson Greatbatch's two-cubic-inch epoxy pacemaker.",
             STYLE + "Split anatomical-and-engineering scene: on the left, a cutaway human heart beats as a golden conduction wave travels from the upper right sinoatrial node through the AV node and ventricular fibres; on the right, a crisp P-Q-R-S-T electrocardiogram wave unrolls beside a hand-cast round epoxy pacemaker puck." + QUAL_TAIL,
             {"kind": "WHEN", "label": "BUFFALO, 7 MAY 1958", "timeline_step": "1/3 · 1882–1883 & 1906 (Sidney Ringer discovers calcium-driven cardiac contraction in London tap water; Arthur Keith and Martin Flack discover the sinoatrial node pacemaker in Kent)", "hold_s": 3.5}),
            ("02_ringer_1882_tap_water_keith_flack_1906_einthoven_1901_string_galvanometer_and_greatbatch_1958_split", 5.5, 6.0, "B", False, "TAP-WATER CALCIUM, 600-POUND ECG, ONE WRONG RESISTOR", "Quality",
             "Quality: complex three-part composition (Sidney Ringer at University College Hospital in London in 1882–1883 testing New River tap water vs distilled water on an isolated frog heart alongside Arthur Keith and Martin Flack in Bredgar, Kent in 1906 spotting the sinoatrial node; Willem Einthoven in Leiden in 1901–1903 operating his 600-pound water-cooled string galvanometer while a patient sits with both arms and one leg in buckets of salt water; and Wilson Greatbatch in Buffalo in 1956–7 May 1958 plugging in a 1-megaohm resistor and hearing his circuit pulse at 1 beat per second).",
             STYLE + "Three-panel period composition: on the left, Sidney Ringer in 1882 London with an isolated heart kymograph alongside Arthur Keith and Martin Flack in 1906 Kent; in the centre, Willem Einthoven in 1903 Leiden operating his giant water-cooled string galvanometer beside a patient with limbs in salt-water buckets; on the right, Wilson Greatbatch in 1958 Buffalo slotting a striped resistor into a transistor circuit beside his epoxy pacemaker." + QUAL_TAIL,
             None),
            ("03_isolated_heart_in_ringer_solution_beating_100000_times_daily_as_sa_node_paces_rhythm", 11.5, 6.0, "C", False, "THREE BILLION BEATS WITHOUT A BREAK", "Quality",
             "Quality: complex physiological reveal (an isolated heart suspended in warm oxygenated Ringer's solution keeps beating on its own at 60–100 beats per minute as the SA node paces 100,000 beats per day and ~2.5–3 billion beats in a lifetime).",
             STYLE + "In a glass perfusion chamber filled with clear oxygenated Ringer's solution, an isolated heart contracts rhythmically all by itself as the crescent sinoatrial node at the top of the right atrium initiates each wave." + QUAL_TAIL,
             {"kind": "WHEN", "label": "1882 · 1883 · 1901 · 1903 · 1906 · 1956 · 7 MAY 1958", "timeline_step": "1/3 · 1882–1883 & 1906 (Ringer, Keith & Flack) · 2/3 · 1901–1903 (Einthoven) · 3/3 · 1956 – 7 May 1958 (Greatbatch & Chardack)", "hold_s": 3.5}),
            ("04_ringer_1883_einthoven_1903_keith_flack_1907_and_greatbatch_1960_cardiac_conduction_ecg_chart", 17.5, 8.0, "E", False, "SA NODE (60–100 BPM = 100K/DAY) → AV NODE (0.1 S) → HIS-PURKINJE · EINTHOVEN 1 MV P-Q-R-S-T (2.5 µM QUARTZ STRING) & GREATBATCH 1 MΩ / 1.8 MS PULSE", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked Cardiac Conduction, Ringer Ion Balance, Einthoven ECG & Greatbatch Pacemaker chart from Ringer (1883 J. Physiol. 4: 29–42), Einthoven (1901 Arch. Néerl. / 1903 Pflügers Arch. 99: 472–480), Keith & Flack (April 1907 J. Anat. Physiol. 41: 172–189), and Chardack, Gage & Greatbatch (October 1960 Surgery 48: 643–654) shows the SA node → AV node (0.1 s delay) → Bundle of His → Purkinje fibre conduction pathway mapped onto Einthoven's P–Q–R–S–T wave (~1 mV skin potential), Ringer's Ca2+/K+/Na+ balance, and Greatbatch's 1.8 ms / 1 MΩ blocking-oscillator pacemaker pulse.",
             {"kind": "DATA", "label": "SA NODE (100,000 BEATS/DAY), EINTHOVEN P-Q-R-S-T (~1 MV ON 2.5 µM QUARTZ STRING) & GREATBATCH 1 MΩ / 1.8 MS PACEMAKER", "detail": "Inked cardiac electrical conduction & Einthoven P-Q-R-S-T electrocardiogram chart on period paper showing SA node pacemaker firing (60–100 bpm = 100,000 beats/day), AV node 100 ms delay, His-Purkinje ventricular sweep, skin voltage (~1 millivolt read by a 2.5 µm silvered quartz string in a 270 kg electromagnet), and Greatbatch's 1 MΩ / 1.8 ms implantable pacemaker pulse", "scale": "the electrical signal that reaches your skin from your beating heart is just one millivolt — three thousand times weaker than a single AA torch battery — yet Willem Einthoven read it by watching the shadow of a quartz thread four times thinner than a red blood cell", "who_card": "Sidney Ringer (1835–1910) — British physician and pharmacologist · Willem Einthoven (1860–1927) — Dutch physician and physiologist · Arthur Keith (1866–1955) — British anatomist and anthropologist · Martin William Flack (1882–1931) — British physiologist · Wilson Greatbatch (1919–2011) — American electrical engineer and inventor", "when_stamp": "1882 · 1883 · 1901 · 1903 · 1906 · 1956 · 7 May 1958", "hold_s": 3.8}),
            ("05_ringer_1883_kymograph_scroll_quartz_filament_holder_and_1903_pflugers_arch_offprint_pan", 25.5, 5.5, "A", False, "THE ONE-MILLIVOLT WHISPER", "Fast",
             "Fast: daylight macro pan across Sidney Ringer's 1883 smoked-drum kymograph trace, a brass quartz-filament holder, and a 1903 Pflügers Archiv offprint on an oak bench between code graphics so two full-frame graphics never run back to back. Nothing emissive, no face.",
             STYLE + "In crisp daylight on an oak physiology bench, the camera pans smoothly across a smoked-paper kymograph scroll, a brass frame holding a microscopic silvered quartz thread, and an open 1903 journal." + FAST_TAIL,
             None),
            ("06_einthoven_1901_1903_string_galvanometer_and_p_q_r_s_t_wave_chart", 31.0, 8.0, "E", False, "LEIDEN, 1901–1903", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period parchment, an inked Willem Einthoven String Galvanometer & P–Q–R–S–T Wave diagram (from Willem Einthoven, 1901 Arch. Néerl. Sci. Exactes Nat. 6: 625–633 & 1903 Pflügers Arch. 99: 472–480) shows a 2.5-micrometre silver-coated quartz filament stretched between the poles of a 600-pound (270 kg) water-cooled electromagnet deflecting under a 1 mV cardiac current from three salt-water limb buckets (Einthoven's Triangle) to trace the P wave (atrial depolarization), QRS complex (ventricular contraction), and T wave (repolarization).",
             {"kind": "DATA", "label": "1901–1903 EINTHOVEN (PFLÜGERS ARCH.): 270 KG ELECTROMAGNET + 2.5 µM QUARTZ STRING TRACING P-Q-R-S-T WAVE AT 1 MV", "detail": "Inked Willem Einthoven (1903 Pflügers Arch. 99: 472–480) string galvanometer specification & P-Q-R-S-T wave chart comparing Augustus Waller's sluggish 1887 capillary electrometer (A-B-C-D) against Einthoven's 2.5 µm quartz string galvanometer (P-Q-R-S-T)", "scale": "Einthoven's first ECG machine weighed as much as a grand piano, took five people to run, and needed underground telephone wires to carry heartbeats a mile from the hospital — today that same P-Q-R-S-T wave sits on a smartwatch on your wrist", "hold_s": 3.8}),
            ("07_table_three_props_1883_ringer_flask_1903_einthoven_salt_bucket_and_1958_greatbatch_resistor_puck", 39.0, 5.5, "C", False, "1883 TO 1958", "Fast",
             "Fast: daylight prop table (callback source for Part 05: Sidney Ringer's 1883 glass bottle of Ringer's solution, Willem Einthoven's 1903 porcelain salt-water limb jar with brass electrode, and Wilson Greatbatch's 1958 1-megaohm striped resistor beside his two-cubic-inch epoxy pacemaker puck). Nothing emissive.",
             STYLE + "On an oak workbench in soft window light sit three objects side by side: a stoppered glass bottle of Ringer's physiological salt solution, a cylindrical porcelain limb jar with a brass electrode plate, and a striped resistor beside a round epoxy-potted pacemaker puck." + FAST_TAIL,
             None),
            ("08_explorer_swapping_10k_orange_stripe_resistor_for_1m_green_stripe_resistor_on_heart_circuit_board", 62.0, 5.5, "A", True, None, "Quality",
             "Quality: Explorer beat 1 (locked character reference, after 1:00).",
             STYLE + "Standing beside a large brass circuit board wired to a mechanical heart model, the Explorer removes a small brown-black-orange resistor and slots in a brown-black-green one-megaohm resistor, setting the mechanical heart beating in a steady once-per-second rhythm." + EXP_TAIL,
             None),
            ("09_willem_einthoven_1903_leiden_adjusting_microscope_on_600_pound_string_galvanometer", 67.5, 5.5, "B", False, "THE FIRST TRUE ECG", "Quality",
             "Quality: readable face (in Leiden in 1903, Willem Einthoven adjusts the microscope lens aimed at the microscopic silvered quartz thread inside his 600-pound water-cooled electromagnet while a patient sits with both arms and one leg in porcelain jars of salt water).",
             STYLE + "In a 1903 Leiden physiology laboratory, Willem Einthoven adjusts the brass microscope barrel mounted between the massive iron coils of his water-cooled string galvanometer while a seated patient rests both hands and one foot in salt-water jars." + QUAL_TAIL,
             {"kind": "WHEN", "label": "LEIDEN, 1901–1903", "timeline_step": "2/3 · 1901–1903 (Willem Einthoven invents the string galvanometer and records the P–Q–R–S–T electrocardiogram)", "hold_s": 3.5}),
        ],
    ),
    (
        2,
        "Part 02 — 1882–1883 & Summer 1906: Sidney Ringer's London Tap-Water Mistake & Keith and Flack's Farmhouse Discovery of the SA Node",
        [
            ("01_sidney_ringer_1882_london_tap_water_and_keith_flack_1906_kent_sinoatrial_node", 73.0, 6.5, "A", False, "LONDON TAP WATER UNLOCKED THE HEART", "Quality",
             "Quality: readable faces (British physician Sidney Ringer at University College Hospital in London in 1882–1883 discovering that calcium and potassium ions in New River pipe water keep isolated hearts beating, dissolving to Sunao Tawara and Arthur Keith with Martin Flack in their Kent farmhouse cottage in Summer 1906 discovering the sinoatrial node).",
             STYLE + "Split period scene: on the left in 1883 London, Sidney Ringer compares distilled water and New River tap water flasks beside a beating frog-heart kymograph; on the right in Summer 1906 Kent, Arthur Keith and Martin Flack examine stained serial heart sections through a microscope." + QUAL_TAIL,
             {"kind": "FACT", "label": "London tap water unlocked the heart", "who_card": "Sunao Tawara (1873–1952) — Japanese pathologist and anatomist", "when_stamp": "1839 · 1882 · 1883 · 1893 · 1906 · April 1907", "timeline_step": "1/3 · 1882–1883 & 1906 (Sidney Ringer discovers Ca2+/K+ cardiac ion balance; Tawara maps the AV node; Keith & Flack discover the SA node)", "hold_s": 3.8}),
            ("02_ringer_1883_calcium_potassium_trace_and_keith_flack_1907_sa_node_conduction_chart", 79.5, 8.0, "E", False, "1883 RINGER (J. PHYSIOL.: NA+ + CA2+ + K+ HEART BEAT) & APR 1907 KEITH & FLACK (J. ANAT. PHYSIOL.: SA NODE PACEMAKER)", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked Sidney Ringer (1883 J. Physiol. 4: 29–42) frog-heart contraction trace (pure NaCl distilled water stopping vs Ca2+ + K+ Ringer's Solution restoring regular beats) alongside Keith & Flack (April 1907 J. Anat. Physiol. 41: 172–189) and Tawara (1906) SA node → AV node → Bundle of His → Purkinje conduction timing map.",
             {"kind": "DATA", "label": "1883 RINGER CA2+/K+ CONTRACTION TRACE & 1906/1907 KEITH-FLACK SA NODE → AV NODE → HIS-PURKINJE CONDUCTION MAP", "detail": "Inked Sidney Ringer (1883 J. Physiol. 4: 29–42) frog-heart contraction trace (pure NaCl distilled water stopping vs Ca2+ + K+ Ringer's Solution restoring regular beats) alongside Keith & Flack (April 1907 J. Anat. Physiol. 41: 172–189) and Tawara (1906) SA node → AV node → Bundle of His → Purkinje conduction timing map on period paper", "scale": "your heart's natural pacemaker — the sinoatrial node discovered by Keith and Flack — is smaller than a flattened grain of rice, yet that tiny speck of tissue fires three billion electrical sparks over your lifetime without a single wire from your brain", "hold_s": 3.8}),
            ("03_kent_1906_microtome_stained_mole_heart_slides_and_1907_journal_closeup", 87.5, 6.5, "B", False, "1906 — KEITH & FLACK DISCOVER THE SA NODE", "Fast",
             "Fast: daylight macro shot of a brass rotary microtome, paraffin wax ribbons, stained glass slides of the sinoatrial node, and an April 1907 Journal of Anatomy and Physiology offprint on a cottage table. Nothing emissive, no face.",
             STYLE + "In crisp daylight on a wooden table by a cottage window, a brass rotary microtome and trays of stained serial microscope slides sit beside an open 1907 anatomy journal." + FAST_TAIL,
             None),
            ("04_cutaway_heart_conduction_system_model_with_sa_node_av_node_and_purkinje_fibres_pan", 94.0, 5.5, "C", False, "SA NODE · AV NODE · HIS-PURKINJE NETWORK", "Fast",
             "Fast: daylight close-up pan across a sculpted anatomical heart model highlighting the golden crescent SA node, AV node, Bundle of His, and branching Purkinje network on an oak table. Nothing emissive, no face.",
             STYLE + "In bright window light on an oak table, a sculpted cutaway model of the human heart displays the golden sinoatrial node, atrioventricular node, and branching Purkinje conduction pathways." + FAST_TAIL,
             None),
        ],
    ),
    (
        3,
        "Part 03 — May 1887 & 1901–1903: Bulldog 'Jimmy', Willem Einthoven's 600-Pound String Galvanometer & the P–Q–R–S–T Wave — Midpoint Twist",
        [
            ("01_augustus_waller_1887_bulldog_jimmy_and_willem_einthoven_1901_1903_leiden_string_galvanometer", 99.5, 6.5, "A", False, "600-POUND ECG TOOK 5 PEOPLE", "Quality",
             "Quality: readable faces (British physiologist Augustus Desiré Waller at St Mary's Hospital in London in May 1887 with his pet bulldog 'Jimmy' standing with paws in glass salt-water jars, dissolving to Dutch physiologist Willem Einthoven in Leiden in 1901–1903 with his 600-pound water-cooled string galvanometer and P–Q–R–S–T photographic scroll).",
             STYLE + "Split period scene: on the left in May 1887 London, Augustus Waller watches his calm bulldog Jimmy stand with front and back paws in glass dishes of salt water wired to a mercury capillary tube; on the right in 1903 Leiden, Willem Einthoven holds a photographic scroll showing sharp P-Q-R-S-T electrocardiogram peaks." + QUAL_TAIL,
             {"kind": "FACT", "label": "600-pound ECG took 5 people", "who_card": "Augustus Desiré Waller (1856–1922) — British physiologist", "when_stamp": "May 1887 · 1895 · 1901 · 1903 · 1906 · 1911 · 1924", "timeline_step": "2/3 · May 1887 & 1901–1906 (Waller records the first human ECG; Einthoven builds the 600-lb string galvanometer and transmits hospital telecardiograms)", "hold_s": 3.8}),
            ("02_einthoven_1903_1906_string_galvanometer_p_q_r_s_t_and_leiden_telecardiogram_chart", 106.0, 8.0, "E", False, "1903 EINTHOVEN (PFLÜGERS ARCH.: P-Q-R-S-T VS WALLER A-B-C-D) & 1906 1.5 KM LEIDEN HOSPITAL-TO-LAB TELECARDIOGRAM", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked Willem Einthoven (1903 Pflügers Arch. 99: 472–480 & 1906 Arch. Int. Physiol. 4: 132–164) string galvanometer P-Q-R-S-T electrocardiogram vs Waller's 1887 capillary trace & 1.5 km Leiden hospital-to-lab telecardiogram schematic.",
             {"kind": "DATA", "label": "1903 EINTHOVEN P-Q-R-S-T TRACE (2.5 µM QUARTZ THREAD, 270 KG MAGNET) & 1906 1.5 KM LEIDEN TELECARDIOGRAM", "detail": "Inked Willem Einthoven (1903 Pflügers Arch. 99: 472–480 & 1906 Arch. Int. Physiol. 4: 132–164) string galvanometer P-Q-R-S-T electrocardiogram vs Waller's 1887 capillary trace & 1.5 km Leiden hospital-to-lab telecardiogram schematic on period paper", "scale": "Augustus Waller thought the ECG was a useless party trick for his pet bulldog — yet by stretching a quartz thread thinner than a cobweb inside a 600-pound magnet, Willem Einthoven built the lifeline that reads every heart attack on Earth", "hold_s": 3.8}),
            ("03_leiden_1903_600_pound_water_cooled_electromagnet_and_photographic_ecg_scroll_closeup", 114.0, 6.5, "B", False, "1901–1903 — EINTHOVEN'S P-Q-R-S-T ELECTROCARDIOGRAM", "Fast",
             "Fast: daylight macro shot of the heavy cast-iron water-cooled electromagnet coils of Einthoven's string galvanometer beside a developed black-and-white photographic strip showing P–Q–R–S–T waveforms on a bench. Nothing emissive, no face.",
             STYLE + "In crisp daylight in a 1903 Leiden laboratory, the massive water-cooled iron coils and brass microscope tubes of a string galvanometer sit beside a long photographic paper scroll of P-Q-R-S-T waves." + FAST_TAIL,
             None),
            ("04_einthoven_triangle_three_limb_lead_model_and_quartz_bow_arrow_pan", 120.5, 5.5, "C", False, "EINTHOVEN'S TRIANGLE & SILVERED QUARTZ THREAD", "Fast",
             "Fast: daylight close-up pan across a brass diagram model of Einthoven's equilateral three-lead triangle beside the wooden bow and quartz rod used to shoot microscopic quartz threads on an oak table. Nothing emissive, no face.",
             STYLE + "In bright window light on an oak table, a brass geometric model of Einthoven's three-lead triangle sits beside a wooden bow, a quartz rod, and a mounted silvered filament frame." + FAST_TAIL,
             None),
        ],
    ),
    (
        4,
        "Part 04 — 1956 – 7 May 1958: Wilson Greatbatch's Wrong Resistor & the First Implantable Pacemaker",
        [
            ("01_wilson_greatbatch_and_william_chardack_7_may_1958_buffalo_wrong_resistor_and_epoxy_pacemaker", 126.0, 6.5, "A", False, "1 MΩ WRONG RESISTOR", "Quality",
             "Quality: readable faces (American electrical engineer Wilson Greatbatch and thoracic surgeon William M. Chardack in Buffalo in 1956–7 May 1958 / 6 June 1960 with the brown-black-green 1-megaohm resistor plugged into their two-transistor blocking oscillator beside the two-cubic-inch epoxy-potted implantable pacemaker).",
             STYLE + "In a 1958 Buffalo workshop and laboratory, engineer Wilson Greatbatch and surgeon William Chardack examine a tiny brown-black-green striped resistor wired into a two-transistor oscillator beside their round epoxy-cast implantable pacemaker." + QUAL_TAIL,
             {"kind": "FACT", "label": "1 MΩ wrong resistor", "who_card": "William M. Chardack (1914–2006) — American thoracic surgeon", "when_stamp": "1952 · 1956 · 31 October 1957 · 7 May 1958 · 6 June 1960 · 1970", "timeline_step": "3/3 · 1956 – 7 May 1958 & 6 Jun 1960 (Wilson Greatbatch inserts a 1 MΩ resistor by mistake and with William Chardack builds the first implantable cardiac pacemaker)", "hold_s": 3.8}),
            ("02_greatbatch_1958_1960_blocking_oscillator_1_megaohm_pacemaker_circuit_chart", 132.5, 8.0, "E", False, "7 MAY 1958 & OCT 1960 CHARDACK, GAGE & GREATBATCH (SURGERY): 1 MΩ (GREEN STRIPE) VS 10 KΩ (ORANGE) → 1.8 MS PULSE EVERY 1.0 S", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked Wilson Greatbatch (1956–7 May 1958 / October 1960 Surgery 48: 643–654 & US Patent 3,057,356) blocking-oscillator implantable pacemaker circuit schematic (10 kΩ brown-black-orange intended vs 1 MΩ brown-black-green actual resistor producing a 1.8 ms pulse every 1.0 s on 1.35 V mercury-zinc / 1970 lithium-iodide cells).",
             {"kind": "DATA", "label": "1958/1960 GREATBATCH PACEMAKER CIRCUIT (1 MΩ GREEN-STRIPE RESISTOR → 1.8 MS PULSE AT 60 BPM, 8 COMPONENTS IN 2 IN³ EPOXY)", "detail": "Inked Wilson Greatbatch (1956–7 May 1958 / October 1960 Surgery 48: 643–654 & US Patent 3,057,356) blocking-oscillator implantable pacemaker circuit schematic (10 kΩ brown-black-orange intended vs 1 MΩ brown-black-green actual resistor producing a 1.8 ms pulse every 1.0 s on 1.35 V mercury-zinc / 1970 lithium-iodide cells) on period paper", "scale": "misreading a single green stripe for an orange stripe on a resistor the size of a grain of wheat increased the resistance one hundred times — turning a sound recorder into a two-cubic-inch artificial SA node that now keeps over three million human hearts beating", "hold_s": 3.8}),
            ("03_buffalo_1958_two_cubic_inch_epoxy_pacemaker_puck_mercury_cells_and_resistors_closeup", 140.5, 6.5, "B", False, "7 MAY 1958 — IMPLANTABLE PACEMAKER PROVED", "Fast",
             "Fast: daylight macro shot of Wilson Greatbatch's hand-cast two-cubic-inch clear epoxy pacemaker puck showing its eight components and mercury-zinc cells beside a brown-black-orange 10 kΩ resistor and a brown-black-green 1 MΩ resistor on a workbench. Nothing emissive, no face.",
             STYLE + "In crisp daylight on a 1958 electronics workbench, a round two-cubic-inch translucent epoxy pacemaker puck sits beside two colour-banded resistors and an open lab notebook." + FAST_TAIL,
             None),
            ("04_explorer_swapping_orange_stripe_for_green_stripe_on_resistor_and_potting_pacemaker_in_epoxy_mould", 147.0, 5.5, "B", True, None, "Quality",
             "Quality: Explorer beat 2 (locked character reference).",
             STYLE + "Standing at a wooden workbench beside a resistor colour chart, the Explorer swaps an orange third band for a green third band on a large resistor model and seals the compact transistor circuit inside a clear round epoxy mould." + EXP_TAIL,
             None),
        ],
    ),
    (
        5,
        "Part 05 — Three Million Pacemakers Beating Today — & How a Pet Buzzard, a Washed Liver & Pavlov's Dogs Unlocked Digestion",
        [
            ("01_timeline_1882_1970_and_modern_lithium_pacemaker_smartwatch_ecg_chart", 152.5, 8.5, "E", False, "1882–1970 TIMELINE · RINGER SOLUTION, EINTHOVEN 600-LB ECG, KEITH-FLACK SA NODE & GREATBATCH IMPLANTABLE PACEMAKER", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, the 3-era timeline completes: 1882–1883 & 1906 (Sidney Ringer discovers calcium-driven cardiac contraction in London tap water; Arthur Keith and Martin Flack discover the sinoatrial node pacemaker in Kent) · 1901–1903 (Willem Einthoven builds the 600-pound string galvanometer in Leiden and records the P–Q–R–S–T electrocardiogram, winning the 1924 Nobel Prize) · 1956 – 7 May 1958 & 1960 (Wilson Greatbatch accidentally inserts a 1-megaohm resistor in Buffalo and with William Chardack builds the first successful multi-year implantable cardiac pacemaker).",
             {"kind": "DATA", "label": "1882–1970 HEART, ECG & PACEMAKER TIMELINE · RINGER, EINTHOVEN, KEITH & FLACK, GREATBATCH & LITHIUM CELL", "detail": "Animated timeline (1882 → 1970) alongside an inked comparison of Einthoven's 270 kg string galvanometer and Greatbatch's 2-cubic-inch lithium-iodide implantable pacemaker", "scale": "from a London tap-water mistake and a 600-pound magnet in Leiden to a single wrong resistor in a Buffalo barn, scientists learned to read and restart the electrical spark of life", "when_stamp": "1882–1970", "timeline_step": "3/3 · 1882–1970 timeline complete", "hold_s": 3.8}),
            ("02_modern_coin_sized_titanium_pacemaker_beside_1958_epoxy_puck_on_plinth_pan", 161.0, 5.5, "A", False, "OVER 3 MILLION PACEMAKERS BEATING TODAY", "Fast",
             "Fast: daylight close-up of a modern coin-sized titanium lithium-iodide pacemaker beside Greatbatch's 1958 two-cubic-inch epoxy pacemaker puck on a wooden museum plinth. Nothing emissive, no face.",
             STYLE + "In crisp daylight on a wooden museum plinth, a sleek coin-sized titanium cardiac pacemaker sits beside a vintage round epoxy-potted pacemaker puck." + FAST_TAIL,
             None),
            ("03_reaumur_1752_buzzard_tubes_spallanzani_1780_claude_bernard_1857_washed_liver_and_pavlov_1897_handoff", 166.5, 6.5, "C", False, "DIGESTION, THE LIVER & HOMEOSTASIS", "Quality",
             "Quality: readable faces (René-Antoine de Réaumur in Paris in 1752 holding perforated metal digestion tubes beside his pet buzzard alongside Lazzaro Spallanzani in 1780, Claude Bernard at the Collège de France in 1848–1857 flushing a washed liver to discover glycogen and the milieu intérieur, and Ivan Pavlov in St Petersburg in 1897 — handoff to 077 Digestion, the Liver, Glycogen & Pavlov's Reflexes).",
             STYLE + "Split period scene: on the left, René-Antoine de Réaumur in 1752 Paris holding a perforated iron tube beside his perched buzzard alongside Lazzaro Spallanzani; on the right, Claude Bernard in 1857 Paris with his washed-liver apparatus beside Ivan Pavlov in 1897 St Petersburg." + QUAL_TAIL,
             {"kind": "WHEN", "label": "1752 · 1780 · 1848 · 1855 · 1897", "hold_s": 3.5}),
            ("04_table_three_callback", 173.0, 2.4, "C", False, None, "reuse",
             "Reuse: verified unused moving window [5.50s..7.90s] of P1:07_table_three_props_1883_ringer_flask_1903_einthoven_salt_bucket_and_1958_greatbatch_resistor_puck (callback, £0).",
             "Reuse P1:07_table_three_props_1883_ringer_flask_1903_einthoven_salt_bucket_and_1958_greatbatch_resistor_puck [5.50s..7.90s] (2.40s distinct non-overlapping tail window from 8.00s source clip).",
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
                row["reuse_of"] = "P1:07_table_three_props_1883_ringer_flask_1903_einthoven_salt_bucket_and_1958_greatbatch_resistor_puck"
                row["reuse_window_s"] = [5.5, 7.9]
                row["reuse_audit"] = {
                    "source_row": "P1:07_table_three_props_1883_ringer_flask_1903_einthoven_salt_bucket_and_1958_greatbatch_resistor_puck",
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
            "film": "076_Ringer-Einthoven-Keith-Flack-Greatbatch-Heart-Pacemaker",
            "part": p_idx,
            "title": p_title,
            "version": "v01",
            "timing_status": "pre_vo_script_clock (built from heart_script_master_v01.md; retimes onto Scribe STT once VO locks)",
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
        "film": "076_Ringer-Einthoven-Keith-Flack-Greatbatch-Heart-Pacemaker",
        "version": "v01",
        "date": "2026-10-20",
        "owner": "gemini (J0706)",
        "status": "PRE_VO_BOARDS_V01_NO_MINT",
        "generation_authorized": False,
        "script": "00_Brand/Channel-Setup/ideas/076_Ringer-Einthoven-Keith-Flack-Greatbatch-Heart-Pacemaker/heart_script_master_v01.md",
        "sources": "00_Brand/Channel-Setup/ideas/076_Ringer-Einthoven-Keith-Flack-Greatbatch-Heart-Pacemaker/SOURCES_v01.md",
        "credit_snapshot": {
            "flow_balance": 23740,
            "flow_floor": 0,
            "flow_read_at": "2026-10-15T21:42:22Z",
            "vertex_promo_gbp": 71.02,
            "vertex_usable_gbp": 70.02,
        },
        "totals": totals,
        "per_part": per_part_summary,
        "mint_order": "006 > 007 > 008 > 009 > 010 > 011 > 012 > 013 > 014 > 015 > 016 > 017 > 018 > 019 > 020 > 021 > 022 > 023 > 024 > 025 > 026 > 027 > 028 > 029 > 030 > 031 > 032 > 033 > 034 > 035 > 036 > 037 > 038 > 039 > 040 > 041 > 042 > 043 > 044 > 045 > 046 > 047 > 048 > 049 > 050 > 051 > 052 > 053 > 054 > 055 > 056 > 057 > 058 > 059 > 060 > 061 > 062 > 063 > 064 > 065 > 066 > 067 > 068 > 069 > 070 > 071 > 072 > 073 > 074 > 075 > 076 > 077. Nothing in 076 is generation_authorized.",
    }
    (EDIT / "PICTURE_PLAN_v01.json").write_text(json.dumps(plan, indent=2) + "\n")

    sl = [
        "# 076 The Pacemaker: One Wrong Resistor Saved Millions — Shot list & plate boards v01 (pre-VO)",
        "",
        "Gemini, 20 Oct 2026, J0706. Built from `heart_script_master_v01.md` (`90.8/100 PASS`) and `SOURCES_v01.md`.",
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
        "# 076 price review v01 (pre-VO plate boards)",
        "",
        "Gemini, 20 Oct 2026, J0706. Boards only. **No mint. No spend. No merge.**",
        "Prepared from `heart_script_master_v01.md` (`90.8/100 PASS`) and `SOURCES_v01.md` so 076's full plate board rows, non-emissive Fast prompts, £0 code graphics, and Teach-on-Screen overlays are ready to re-time the moment long VO locks. Parked for Chief.",
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
        f"- **Quality ({totals['Quality']} rows):** readable faces (Sidney Ringer, Sunao Tawara, Arthur Keith, Martin William Flack, Augustus Desiré Waller, Willem Einthoven, Wilson Greatbatch, William M. Chardack, René-Antoine de Réaumur, Lazzaro Spallanzani, Claude Bernard, Ivan Pavlov), 1882–1883 London tap-water frog heart & Summer 1906 Kent `SA node`, May 1887 Bulldog `'Jimmy'` & 1901–1903 Leiden `600-lb string galvanometer` (`P–Q–R–S–T`), 7 May 1958 Buffalo `1-MΩ` wrong-resistor implantable pacemaker, and the 2 Explorer beats.",
        f"- **Fast ({totals['Fast']} rows, non-emissive):** daylight prop and laboratory shots (1883 smoked-drum kymograph scroll, quartz-filament holder & 1903 *Pflügers Arch.* offprint pan, 3-object callback bench, 1906 Kent rotary microtome with serial heart slides & 1907 journal, sculpted cutaway heart conduction model, 1903 Leiden water-cooled string galvanometer coils & `P–Q–R–S–T` photographic scroll, brass `Einthoven's Triangle` & quartz-thread bow model, 1958 Buffalo `2 in³` epoxy pacemaker puck with `10 kΩ` vs `1 MΩ` resistors, modern coin-sized titanium pacemaker beside 1958 epoxy puck on museum plinth). Zero candles, flames, sparks, or glowing elements on Fast.",
        f"- **£0 code graphics ({totals['code_graphic']} rows):**",
        "  1. `P1:04_ringer_1883_einthoven_1903_keith_flack_1907_and_greatbatch_1960_cardiac_conduction_ecg_chart` — `SA node` (`60–100 bpm` = `100,000 beats/day`), `AV node` (`0.1 s` delay), Einthoven's `~1 mV` `P–Q–R–S–T` wave (`2.5 µm` quartz string in `270 kg` magnet), and Greatbatch's `1 MΩ` / `1.8 ms` pacemaker pulse (`SCALE: the electrical signal that reaches your skin from your beating heart is just one millivolt — three thousand times weaker than a single AA torch battery — yet Willem Einthoven read it by watching the shadow of a quartz thread four times thinner than a red blood cell`)",
        "  2. `P1:06_einthoven_1901_1903_string_galvanometer_and_p_q_r_s_t_wave_chart` — Willem Einthoven (1901–1903 *Pflügers Arch.*) string galvanometer specification & `P–Q–R–S–T` wave chart (`SCALE: Einthoven's first ECG machine weighed as much as a grand piano, took five people to run, and needed underground telephone wires to carry heartbeats a mile from the hospital — today that same P-Q-R-S-T wave sits on a smartwatch on your wrist`)",
        "  3. `P2:02_ringer_1883_calcium_potassium_trace_and_keith_flack_1907_sa_node_conduction_chart` — Sidney Ringer (1883 *J. Physiol.*) `Ca²⁺/K⁺/Na⁺` heart contraction trace & Keith and Flack (April 1907) `SA node` conduction map (`SCALE: your heart's natural pacemaker — the sinoatrial node discovered by Keith and Flack — is smaller than a flattened grain of rice, yet that tiny speck of tissue fires three billion electrical sparks over your lifetime without a single wire from your brain`)",
        "  4. `P3:02_einthoven_1903_1906_string_galvanometer_p_q_r_s_t_and_leiden_telecardiogram_chart` — Willem Einthoven (1903 & 1906) `P–Q–R–S–T` trace vs Waller's 1887 capillary curve & `1.5 km` Leiden hospital-to-lab telecardiogram (`SCALE: Augustus Waller thought the ECG was a useless party trick for his pet bulldog — yet by stretching a quartz thread thinner than a cobweb inside a 600-pound magnet, Willem Einthoven built the lifeline that reads every heart attack on Earth`)",
        "  5. `P4:02_greatbatch_1958_1960_blocking_oscillator_1_megaohm_pacemaker_circuit_chart` — Wilson Greatbatch & William Chardack (7 May 1958 / October 1960 *Surgery*) `1 MΩ` (brown-black-green) vs `10 kΩ` (brown-black-orange) blocking-oscillator pacemaker schematic (`SCALE: misreading a single green stripe for an orange stripe on a resistor the size of a grain of wheat increased the resistance one hundred times — turning a sound recorder into a two-cubic-inch artificial SA node that now keeps over three million human hearts beating`)",
        "  6. `P5:01_timeline_1882_1970_and_modern_lithium_pacemaker_smartwatch_ecg_chart` — completed timeline (1882 → 1970) + lithium-iodide implantable pacemaker & smartwatch ECG (`SCALE: from a London tap-water mistake and a 600-pound magnet in Leiden to a single wrong resistor in a Buffalo barn, scientists learned to read and restart the electrical spark of life`)",
        f"- **£0 verified reuse ({totals['reuse']} row):** `P5:04_table_three_callback` uses the 2.40 s unused moving tail `[5.50s..7.90s]` of `P1:07_table_three_props_1883_ringer_flask_1903_einthoven_salt_bucket_and_1958_greatbatch_resistor_puck`.",
        "",
        "## Mint order",
        "",
        "006 > 007 > 008 > 009 > 010 > 011 > 012 > 013 > 014 > 015 > 016 > 017 > 018 > 019 > 020 > 021 > 022 > 023 > 024 > 025 > 026 > 027 > 028 > 029 > 030 > 031 > 032 > 033 > 034 > 035 > 036 > 037 > 038 > 039 > 040 > 041 > 042 > 043 > 044 > 045 > 046 > 047 > 048 > 049 > 050 > 051 > 052 > 053 > 054 > 055 > 056 > 057 > 058 > 059 > 060 > 061 > 062 > 063 > 064 > 065 > 066 > 067 > 068 > 069 > 070 > 071 > 072 > 073 > 074 > 075 > 076 > 077. `generation_authorized` is `false` on every row.",
    ])
    (EDIT / "PRICE_REVIEW_v01.md").write_text("\n".join(pr_lines) + "\n")
    print(f"076 v01 boards written: {totals['rows']} rows, Flow expected={totals['flow_credits_expected']}")


if __name__ == "__main__":
    main()
