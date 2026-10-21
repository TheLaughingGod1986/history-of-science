#!/usr/bin/env python3
"""HOS 063 (Mitochondria: How Swallowed Bacteria Power Your Cells) pre-VO plate boards v01. J0646. No mint, no spend.

Built from 00_Brand/Channel-Setup/ideas/063_Krebs-Mitchell-Margulis-Mitochondria-ATP/mitochondria_script_master_v01.md
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
        "Part 01 — The Lightning-Bolt Proton Dam & the Ancient Bacteria Inside You",
        [
            ("01_mitochondrion_5nm_proton_dam_180mv_and_100rps_atp_synthase_rotary_waterwheel", 0.0, 5.5, "A", False, "THE ROTARY PROTON TURBINE", "Quality",
             "Quality: Short frame 0 / answer image (0:03) + inside a double-membraned mitochondrion, protons (H+) are pumped across a 5-nanometre inner membrane dam to build a 180-millivolt electric potential, then rush back through a spinning golden rotary waterwheel (ATP synthase, spinning at 100 revolutions per second) that stamps phosphates onto ADP to make ATP molecules.",
             STYLE + "Inside a double-membraned mitochondrion, golden proton spheres are pumped across a five-nanometre inner membrane dam and rush back through a spinning golden rotary ATP synthase turbine that stamps phosphate rings onto ADP molecules to release fresh ATP." + QUAL_TAIL,
             {"kind": "WHEN", "label": "SHEFFIELD, JUNE 1937", "timeline_step": "1/4 · Jun–Aug 1937 (Hans Krebs & William Arthur Johnson at Sheffield use pigeon breast muscle to discover the 8-step Citric Acid Cycle, rejected by Nature)", "hold_s": 3.5}),
            ("02_krebs_johnson_1937_sheffield_mitchell_moyle_1961_glynn_house_and_margulis_1967_split", 5.5, 6.0, "B", False, "KREBS CYCLE, PROTON DAM, ANCIENT BACTERIA", "Quality",
             "Quality: complex three-part composition (Hans Krebs and William Arthur Johnson at the University of Sheffield in June 1937 measuring oxygen uptake in minced pigeon breast muscle while holding a rejection letter from Nature; Peter Mitchell and Jennifer Moyle in their private laboratory at Glynn House in Cornwall in July 1961 sketching a proton dam across a membrane; and Lynn Margulis at Boston University in March 1967 tracing circular mitochondrial DNA back to an ancient swallowed bacterium).",
             STYLE + "Three-panel period composition: on the left, Hans Krebs and William Arthur Johnson in 1937 Sheffield beside Warburg manometers holding a rejection letter; in the centre, Peter Mitchell and Jennifer Moyle at Glynn House in Cornwall in 1961 sketching a proton membrane dam; on the right, Lynn Margulis in 1967 Boston pointing to a circular mitochondrial DNA ring inside a double-membraned bacterium." + QUAL_TAIL,
             None),
            ("03_five_nm_mitochondrial_inner_membrane_180mv_beside_30mv_per_m_storm_cloud_scale", 11.5, 6.0, "C", False, "30 MILLION VOLTS PER METRE", "Quality",
             "Quality: complex conceptual and physical scale comparison (a 5-nanometre mitochondrial inner membrane carrying 180 millivolts of proton charge sits beside a storm cloud discharging a 30-million-volt-per-metre lightning bolt).",
             STYLE + "Split scale scene: on the left, a cross-section of a five-nanometre mitochondrial inner membrane holds back a dense reservoir of golden protons; on the right, a dark storm cloud above a landscape discharges a bright lightning bolt representing thirty million volts per metre." + QUAL_TAIL,
             {"kind": "WHEN", "label": "JUNE 1937 · 8 JULY 1961 · MARCH 1967 · 18 AUGUST 1994", "timeline_step": "1/4 · Jun 1937 (Krebs & Johnson) · 2/4 · 8 Jul 1961 (Mitchell & Moyle) · 3/4 · Mar 1967 (Margulis) · 4/4 · 18 Aug 1994 (Boyer & Walker)", "hold_s": 3.5}),
            ("04_krebs_1937_mitchell_1961_boyer_walker_1994_margulis_1967_respiration_chemiosmosis_chart", 17.5, 8.0, "E", False, "1937 KREBS CYCLE (8 STEPS) · 1961 MITCHELL PROTON DAM (180 MV = 30 MV/M) · 1994 BOYER/WALKER ATP SYNTHASE (100 REV/S) · 1967 MARGULIS ENDOSYMBIOSIS", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked 3-stage cellular respiration & chemiosmotic proton-motive force chart from Krebs & Johnson (June–August 1937 Enzymologia 4: 148–156), Mitchell (8 July 1961 Nature 191: 144–148), Boyer & Walker (18 August 1994 Nature 370: 621–628), and Margulis (March 1967 J. Theor. Biol. 14: 225–274) shows: (1) the 8-step Krebs Citric Acid Cycle stripping CO2 and loading NADH/FADH2, (2) the Electron Transport Chain pumping H+ across the 5-nm inner membrane (~150–180 mV = ~30 MV/m) to spin the F1Fo-ATP synthase rotary turbine (~100 rev/s, 3 ATP per turn, ~30–32 ATP per glucose), and (3) the double membrane and 37-gene circular mtDNA of alpha-proteobacterial endosymbiosis.",
             {"kind": "DATA", "label": "8-STEP KREBS CYCLE → 180-MV / 5-NM PROTON DAM (~30 MV/M) → 100-RPS ATP SYNTHASE (~30–32 ATP/GLUCOSE)", "detail": "Inked cellular respiration & chemiosmosis chart on period paper showing the 8-step Krebs Cycle (2 CO2 + 3 NADH + 1 FADH2 + 1 GTP per acetyl-CoA), the 150–180 mV proton gradient across the 5-nm inner mitochondrial membrane (~30 million V/m), and F1Fo-ATP synthase spinning at ~100–130 rev/s to synthesize 3 ATP per 360° rotation (~30–32 ATP per glucose molecule)", "scale": "a voltage of just 180 millivolts across a membrane five billionths of a metre thick creates an electric field of thirty million volts per metre — as intense as a bolt of lightning inside every cell of your body", "who_card": "Hans A. Krebs (1900–1981) — German-British biochemist · William A. Johnson (1913–1994) — British biochemist · Peter D. Mitchell (1920–1992) — British biochemist · Paul D. Boyer (1918–2018) — American biochemist · John E. Walker (born 1941) — British chemist · Lynn Margulis (1938–2011) — American evolutionary biologist", "when_stamp": "June 1937 · 8 July 1961 · March 1967 · 18 August 1994", "hold_s": 3.8}),
            ("05_warburg_manometer_flask_brass_voltmeter_and_rotary_waterwheel_model_pan", 25.5, 5.5, "A", False, "30 MILLION VOLTS PER METRE", "Fast",
             "Fast: daylight macro pan across a glass Warburg manometer flask, a vintage brass millivoltmeter, and a carved wooden rotary turbine model on an oak bench between code graphics so two full-frame graphics never run back to back. Nothing emissive, no face.",
             STYLE + "In crisp daylight on an oak biochemistry bench, the camera pans smoothly across a glass Warburg U-tube manometer flask, a brass dial millivoltmeter, and a wooden model of a three-lobed rotary turbine." + FAST_TAIL,
             None),
            ("06_meerman_brown_2014_bmj_10kg_fat_oxidation_to_8_4kg_exhaled_co2_mass_balance_chart", 31.0, 8.0, "E", False, "84% BREATHED OUT AS CO2", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period parchment, an inked mass-balance chart of human metabolism & weight loss (from Lavoisier 1789 & Meerman and Brown December 2014 BMJ 349: g7257) shows 10 kilograms of human fat (C55H104O6) combining with 29 kilograms of inhaled oxygen (O2) inside mitochondria to turn into 8.4 kilograms of exhaled carbon dioxide gas (CO2, 84%) and 1.6 kilograms of water (H2O, 16%).",
             {"kind": "DATA", "label": "MITOCHONDRIAL FAT OXIDATION (MEERMAN & BROWN 2014 BMJ): 10 KG FAT + 29 KG O2 → 8.4 KG EXHALED CO2 (84%) + 1.6 KG H2O (16%)", "detail": "Inked mitochondrial oxidation & weight-loss stoichiometry chart showing 10 kg of oxidised fat + 29 kg of O2 yielding 8.4 kg of exhaled CO2 (84% of lost mass) and 1.6 kg of H2O (16% of lost mass) via the Krebs cycle and electron transport chain", "scale": "when you exercise and lose ten kilograms of body fat, your fat doesn't turn into heat or sweat — 8.4 kilograms of it leaves your body through your lungs as invisible carbon dioxide gas", "hold_s": 3.8}),
            ("07_table_three_props_1937_sheffield_manometer_1961_glynn_house_ph_meter_and_1994_atp_rotor", 39.0, 5.5, "C", False, "1937 TO 1994", "Fast",
             "Fast: daylight prop table (callback source for Part 05: Hans Krebs's 1937 glass Warburg manometer flask, Peter Mitchell's 1961 Glynn House glass pH electrode, and a 3D brass-and-wood model of the F1-ATPase rotary motor). Nothing emissive.",
             STYLE + "On an oak workbench in soft window light sit three objects side by side: a glass Warburg manometer flask, a glass-bulb pH electrode in a wooden stand, and a carved three-lobed rotary ATP synthase model." + FAST_TAIL,
             None),
            ("08_explorer_opening_proton_dam_sluice_gate_to_spin_atp_synthase_waterwheel", 62.0, 5.5, "A", True, None, "Quality",
             "Quality: Explorer beat 1 (locked character reference, after 1:00).",
             STYLE + "Standing on the rim of a five-nanometre mitochondrial inner-membrane dam, the Explorer turns a brass wheel to open a sluice gate, letting golden proton spheres rush through a spinning rotary ATP synthase waterwheel and catching freshly stamped ATP blocks three at a time." + EXP_TAIL,
             None),
            ("09_krebs_june_1937_sheffield_reading_nature_rejection_letter_beside_pigeon_muscle_manometers", 67.5, 5.5, "B", False, "SHEFFIELD, JUNE 1937", "Quality",
             "Quality: readable face (at the University of Sheffield in June 1937, Hans Krebs opens a polite rejection letter from the editor of Nature while manometer tubes bubble with minced pigeon breast muscle on his bench).",
             STYLE + "In a 1937 Sheffield laboratory, biochemist Hans Krebs holds a typed rejection letter beside a row of glass Warburg manometer flasks containing minced pigeon breast muscle and a notebook open to a circular eight-step chemical diagram." + QUAL_TAIL,
             {"kind": "WHEN", "label": "SHEFFIELD, JUNE 1937", "timeline_step": "1/4 · Jun–Aug 1937 (Hans Krebs & William Arthur Johnson discover the Citric Acid Cycle in Sheffield; rejected by Nature, published in Enzymologia)", "hold_s": 3.5}),
        ],
    ),
    (
        2,
        "Part 02 — June 1937: Pigeon Breast Muscle, the Nature Rejection Letter & the Spinning Krebs Cycle",
        [
            ("01_krebs_and_johnson_june_1937_sheffield_pigeon_muscle_manometers_and_nature_rejection", 73.0, 6.5, "A", False, "REJECTED BY NATURE IN JUNE 1937", "Quality",
             "Quality: readable faces (refugee biochemist Hans Krebs and graduate student William Arthur Johnson at the University of Sheffield in June–August 1937 measuring oxygen consumption and citrate formation in minced pigeon breast muscle, alongside the June 1937 rejection letter from Nature).",
             STYLE + "Split period scene: on the left in June 1937 Sheffield, Hans Krebs and William Arthur Johnson pipette citrate solution into glass Warburg manometer flasks; on the right, Krebs smiles wryly at a typed rejection letter resting next to his circular Citric Acid Cycle drawing." + QUAL_TAIL,
             {"kind": "FACT", "label": "Rejected by Nature in June 1937", "when_stamp": "April 1933 · 10 June 1937 · August 1937 · 1953", "timeline_step": "1/4 · Jun–Aug 1937 (Hans Krebs & William Arthur Johnson prove the 8-step Citric Acid Cycle in pigeon breast muscle)", "hold_s": 3.8}),
            ("02_krebs_johnson_aug_1937_enzymologia_eight_step_citric_acid_cycle_wheel_chart", 79.5, 8.0, "E", False, "JUNE–AUGUST 1937 KREBS & JOHNSON (ENZYMOLOGIA 4: 148–156): 8-STEP CITRIC ACID CYCLE (OXALOACETATE + ACETYL-COA → CITRATE → 2 CO2 + 3 NADH + 1 FADH2 + 1 GTP)", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked 8-step Krebs Citric Acid Cycle diagram from Krebs & Johnson (August 1937, Enzymologia 4: 148–156) shows 2-carbon acetyl-CoA condensing with 4-carbon oxaloacetate to form 6-carbon citrate, then stepping through isocitrate, alpha-ketoglutarate, succinyl-CoA, succinate, fumarate, and malate to release 2 CO2 molecules and load 3 NADH, 1 FADH2, and 1 GTP/ATP per turn.",
             {"kind": "DATA", "label": "1937 KREBS CYCLE: 4-C OXALOACETATE + 2-C ACETYL-COA → 6-C CITRATE → 2 CO2 EXHALED + 3 NADH + 1 FADH2 + 1 GTP", "detail": "Inked 8-step Krebs Citric Acid Cycle diagram on period paper from Krebs & Johnson (August 1937, Enzymologia 4: 148–156) showing 2-carbon acetyl-CoA condensing with 4-carbon oxaloacetate to form 6-carbon citrate, then stepping through isocitrate, alpha-ketoglutarate, succinyl-CoA, succinate, fumarate, and malate to release 2 CO2 molecules and load 3 NADH, 1 FADH2, and 1 GTP/ATP per turn", "scale": "the Krebs cycle works like a waterwheel that never gets used up — a four-carbon bucket picks up a two-carbon piece of food, drops off two carbon dioxide molecules that you breathe out of your lungs, and comes right back around for the next load", "hold_s": 3.8}),
            ("03_sheffield_1937_rejection_letter_circular_cycle_notebook_and_manometer_closeup", 87.5, 6.5, "B", False, "JUNE 1937 — THE SPINNING CARBON WHEEL", "Fast",
             "Fast: daylight macro shot of a fountain-pen notebook open to an 8-spoke chemical wheel beside a folded envelope and glass Warburg manometer flasks on a 1937 Sheffield desk. Nothing emissive, no face.",
             STYLE + "In crisp daylight on a 1937 wooden laboratory desk, a cloth-bound notebook showing an inked circular wheel diagram rests beside a fountain pen, a cream envelope, and glass Warburg manometer tubes." + FAST_TAIL,
             None),
            ("04_wooden_four_carbon_and_two_carbon_six_carbon_citrate_wheel_model_pan", 94.0, 5.5, "C", False, "8 STEPS · 2 CO2 BREATHED OUT", "Fast",
             "Fast: daylight close-up pan across a carved wooden 8-spoke waterwheel holding four-carbon and two-carbon ball-and-stick blocks on an oak table. Nothing emissive, no face.",
             STYLE + "In bright window light on an oak bench, a carved wooden eight-spoke wheel carries interlocking four-ball and two-ball molecular models around a circular track." + FAST_TAIL,
             None),
        ],
    ),
    (
        3,
        "Part 03 — 8 July 1961: The 'Ox-Phos Wars' & Peter Mitchell's Country-Mansion Proton Dam (Chemiosmosis) — Midpoint Twist",
        [
            ("01_peter_mitchell_and_jennifer_moyle_8_july_1961_glynn_house_cornwall_proton_dam", 99.5, 6.5, "A", False, "A 30-MILLION-VOLT-PER-METRE DAM", "Quality",
             "Quality: readable faces (British biochemist Peter Mitchell and experimental partner Jennifer Moyle in their restored Regency manor house laboratory at Glynn House, Cornwall, proving the 8 July 1961 Nature chemiosmotic hypothesis that mitochondria pump protons across a 5-nm inner membrane to build a 180-mV proton dam).",
             STYLE + "Split period scene: on the left at Glynn House in Cornwall, Peter Mitchell and Jennifer Moyle measure proton pulses with a glass pH electrode in isolated mitochondria; on the right, a cross-section of the inner mitochondrial membrane shows four respiratory complexes pumping protons behind a dam to spin ATP synthase." + QUAL_TAIL,
             {"kind": "FACT", "label": "A 30-million-volt-per-metre dam", "who_card": "Jennifer Moyle (1921–2016) — British biochemist", "when_stamp": "1948 · July 1957 · 8 July 1961 · 1966 · 1974", "timeline_step": "2/4 · 8 Jul 1961 (Peter Mitchell proposes the chemiosmotic proton-motive force in Nature, proven with Jennifer Moyle at Glynn House)", "hold_s": 3.8}),
            ("02_mitchell_1961_moyle_1967_racker_stoeckenius_1974_chemiosmotic_proton_motive_force_chart", 106.0, 8.0, "E", False, "8 JULY 1961 MITCHELL (NATURE 191: 144–148) & 1974 RACKER-STOECKENIUS: ΔΨ (180 MV) + ΔPH ACROSS 5-NM MEMBRANE (~30 MV/M) DRIVES ATP SYNTHESIS", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked Mitchell & Moyle chemiosmotic proton-motive force chart from Mitchell (8 July 1961, Nature 191: 144–148) and Racker & Stoeckenius (1974, J. Biol. Chem. 249: 662–663) plots inner mitochondrial membrane potential Δψ (~150–180 mV) + ΔpH (~0.5–1.0 pH unit, total proton-motive force ~200–220 mV across 5 nm = ~30–40 MV/m) driving ATP synthesis.",
             {"kind": "DATA", "label": "8 JULY 1961 MITCHELL CHEMIOSMOSIS: ΔΨ (~180 MV) + ΔPH ACROSS 5-NM MEMBRANE (~30 MV/M) DRIVES ATP SYNTHASE", "detail": "Inked Mitchell & Moyle chemiosmotic proton-motive force chart on period paper from Mitchell (8 July 1961, Nature 191: 144–148) and Racker & Stoeckenius (1974, J. Biol. Chem. 249: 662–663) plotting inner mitochondrial membrane potential Δψ (~150–180 mV) + ΔpH (~0.5–1.0 pH unit, total proton-motive force ~200–220 mV across 5 nm = ~30–40 MV/m) driving ATP synthesis", "scale": "just as Hoover Dam holds back a lake of water so the rushing torrent can spin hydroelectric turbines, your mitochondria pump protons behind a five-nanometre membrane dam so the rushing protons can spin ATP synthase", "hold_s": 3.8}),
            ("03_glynn_house_cornwall_ph_electrode_reaction_vessel_and_strip_recorder_closeup", 114.0, 6.5, "B", False, "8 JULY 1961 — CHEMIOSMOSIS", "Fast",
             "Fast: daylight macro shot of a water-jacketed glass reaction vessel fitted with a sensitive pH electrode beside a paper strip-chart recorder on a bench at Glynn House. Nothing emissive, no face.",
             STYLE + "In crisp window light on a Cornish manor laboratory bench, a water-jacketed glass reaction vessel with a fine pH electrode sits beside a mechanical paper strip-chart recorder tracing a sharp acid jump." + FAST_TAIL,
             None),
            ("04_wooden_hydroelectric_dam_sluice_and_bilayer_membrane_proton_pump_model_pan", 120.5, 5.5, "C", False, "180 MILLIVOLTS ACROSS 5 NANOMETRES", "Fast",
             "Fast: daylight close-up pan across a brass-and-wood miniature dam sluice model beside a sculpted lipid-bilayer membrane model on an oak table. Nothing emissive, no face.",
             STYLE + "In bright daylight on an oak table, a carved wooden miniature dam and waterwheel sit beside a sculpted cross-section model of a double-layered cell membrane." + FAST_TAIL,
             None),
        ],
    ),
    (
        4,
        "Part 04 — March 1967 & August 1994: The World's Smallest Rotary Turbine (ATP Synthase) & Lynn Margulis's Swallowed-Bacteria Proof",
        [
            ("01_boyer_walker_18_aug_1994_rotary_atp_synthase_and_lynn_margulis_march_1967_endosymbiosis", 126.0, 6.5, "A", False, "15 REJECTIONS FOR ENDOSYMBIOSIS", "Quality",
             "Quality: readable faces (Paul Boyer and John Walker on 18 August 1994 revealing the 2.8-Å atomic crystal structure of the spinning F1-ATPase rotary motor, dissolving to 29-year-old Lynn Margulis in March 1967 publishing her 15-times-rejected paper proving mitochondria evolved from ancient swallowed alpha-proteobacteria).",
             STYLE + "Split period scene: on the left in August 1994 Cambridge, John Walker and Paul Boyer examine the three-lobed atomic model of spinning F1-ATP synthase; on the right in March 1967 Boston, young Lynn Margulis holds her published journal paper beside a diagram of a host cell swallowing an ancient bacterium." + QUAL_TAIL,
             {"kind": "FACT", "label": "15 rejections for endosymbiosis", "when_stamp": "1963 · March 1967 · 18 August 1994 · March 1997", "timeline_step": "3/4 · Mar 1967 (Lynn Margulis proves endosymbiosis) & 4/4 · 18 Aug 1994 (Paul Boyer & John Walker solve the rotary ATP synthase turbine)", "hold_s": 3.8}),
            ("02_boyer_walker_1994_atp_synthase_32_vs_2_atp_and_margulis_1967_16569bp_mtdna_chart", 132.5, 8.0, "E", False, "MARCH 1967 MARGULIS (ENDOSYMBIOSIS, 16,569-BP 37-GENE MTDNA) & 18 AUG 1994 BOYER/WALKER (100-RPS ATP SYNTHASE: 32 ATP VS 2 ATP GLYCOLYSIS)", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked Boyer & Walker rotary ATP synthase (18 August 1994, Nature 370: 621–628) and Margulis endosymbiosis (March 1967, J. Theor. Biol. 14: 225–274) chart compares anaerobic glycolysis (2 ATP per glucose) vs aerobic mitochondrial oxidative phosphorylation (~30–32 ATP per glucose — a 15-fold energy leap) alongside the 16,569-base-pair maternal circular mitochondrial genome (37 genes).",
             {"kind": "DATA", "label": "MARGULIS ENDOSYMBIOSIS (1967, 16,569-BP CIRCULAR MTDNA) & WALKER/BOYER ROTARY ATP SYNTHASE (1994): 32 ATP VS 2 ATP (15× LEAP)", "detail": "Inked Boyer & Walker rotary ATP synthase (18 August 1994, Nature 370: 621–628) and Margulis endosymbiosis (March 1967, J. Theor. Biol. 14: 225–274) chart on period paper comparing anaerobic glycolysis (2 ATP per glucose) vs aerobic mitochondrial oxidative phosphorylation (~30–32 ATP per glucose — a 15-fold energy leap) alongside the 16,569-base-pair maternal circular mitochondrial genome (37 genes)", "scale": "without the ancient bacteria living inside your cells, a molecule of sugar would give you only two molecules of ATP instead of thirty-two — leaving complex animals with fifteen times too little energy to run, think, or keep a heart beating", "hold_s": 3.8}),
            ("03_brass_and_wood_f1fo_atp_synthase_rotary_camshaft_and_circular_mtdna_ring_closeup", 140.5, 6.5, "B", False, "18 AUGUST 1994 — THE ROTARY TURBINE INSIDE AN ANCIENT BACTERIUM", "Fast",
             "Fast: daylight macro shot of a sculpted brass-and-wood F1Fo-ATP synthase rotary c-ring and central gamma shaft beside a circular 37-gene bacterial DNA ring model on a workbench. Nothing emissive, no face.",
             STYLE + "In crisp daylight on a structural biology bench, a brass-and-wood mechanical model of the F1Fo-ATP synthase rotor and central camshaft sits beside a circular ring model of mitochondrial DNA." + FAST_TAIL,
             None),
            ("04_explorer_tracing_circular_mtdna_ring_to_two_billion_year_endosymbiosis_handshake", 147.0, 5.5, "B", True, None, "Quality",
             "Quality: Explorer beat 2 (locked character reference).",
             STYLE + "Inside a double-membraned mitochondrion, the Explorer holds up a circular ring of mitochondrial DNA and looks through a window showing a large primitive host cell welcoming a smaller oxygen-breathing bacterium inside without digesting it." + EXP_TAIL,
             None),
        ],
    ),
    (
        5,
        "Part 05 — Why All Your Mitochondria Come From Your Mother — & the Mystery of Living Crystals (Viruses)",
        [
            ("01_timeline_1937_1994_and_maternal_16569bp_mitochondrial_dna_inheritance_chart", 152.5, 8.5, "E", False, "1937–1994 TIMELINE · KREBS CYCLE, MITCHELL PROTON DAM, MARGULIS ENDOSYMBIOSIS, BOYER/WALKER ATP SYNTHASE & 100% MATERNAL MTDNA", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, the 4-date timeline completes: June–August 1937 (Hans Krebs & William Arthur Johnson at Sheffield use pigeon breast muscle to discover the 8-step Citric Acid Cycle, rejected by Nature) · 8 July 1961 (Peter Mitchell proposes the chemiosmotic proton-motive force across the inner mitochondrial membrane, proven with Jennifer Moyle at Glynn House) · March 1967 (Lynn Margulis publishes her 15-times-rejected paper proving mitochondria evolved from ancient swallowed bacteria via endosymbiosis) · 18 August 1994 (Paul Boyer & John Walker reveal at atomic resolution that ATP synthase is a rotary molecular turbine spinning at ~100 rev/s).",
             {"kind": "DATA", "label": "1937–1994 MITOCHONDRIA TIMELINE · 100% MATERNAL 16,569-BP CIRCULAR MTDNA INHERITANCE (1981 / 1987)", "detail": "Animated 4-date timeline (1937 → 1994) alongside the 100% maternal 16,569-base-pair circular mitochondrial DNA inheritance diagram", "scale": "from a rejected letter on pigeon muscle in Sheffield to a country-house lab in Cornwall and a two-billion-year bacterial partnership, three rebel scientists revealed why mitochondria truly are the powerhouse of the cell", "when_stamp": "April 1981 · January 1987 · 1937–1994", "timeline_step": "4/4 · 1937–1994 timeline complete", "hold_s": 3.8}),
            ("02_maternal_circular_mtdna_ring_and_double_membrane_mitochondrion_model_on_plinth_pan", 161.0, 5.5, "A", False, "100% MATERNAL MITOCHONDRIAL DNA", "Fast",
             "Fast: daylight close-up of a circular brass-and-wood 37-gene mitochondrial DNA ring beside a sectioned mitochondrion model on a wooden museum plinth. Nothing emissive, no face.",
             STYLE + "In crisp daylight on a wooden museum plinth, a polished circular ring model of 37-gene maternal mitochondrial DNA sits beside a cross-sectioned double-membrane mitochondrion model." + FAST_TAIL,
             None),
            ("03_ivanovsky_1892_filter_stanley_1935_tmv_crystals_and_hershey_chase_1952_blender_handoff", 166.5, 6.5, "C", False, "VIRUSES: LIVING CRYSTALS & THE BLENDER", "Quality",
             "Quality: readable faces (Dmitri Ivanovsky on 12 February 1892 pouring tobacco sap through a Chamberland porcelain filter, Wendell Stanley on 28 June 1935 holding a jar of crystalline Tobacco Mosaic Virus needles, and Alfred Hershey with Martha Chase on 20 September 1952 beside their Waring kitchen blender — handoff to 064 Viruses, Crystallization & the Hershey-Chase Blender).",
             STYLE + "Split period scene: on the left, Dmitri Ivanovsky filters tobacco leaf sap through a white porcelain candle while Wendell Stanley holds up a glass jar of white virus crystals; on the right in September 1952, Alfred Hershey and Martha Chase run a silver Waring kitchen blender to shear bacteriophages off bacteria." + QUAL_TAIL,
             {"kind": "WHEN", "label": "12 FEBRUARY 1892 · 28 JUNE 1935 · 20 SEPTEMBER 1952", "hold_s": 3.5}),
            ("04_table_three_callback", 173.0, 2.4, "C", False, None, "reuse",
             "Reuse: verified unused moving window [5.50s..7.90s] of P1:07_table_three_props_1937_sheffield_manometer_1961_glynn_house_ph_meter_and_1994_atp_rotor (callback, £0).",
             "Reuse P1:07_table_three_props_1937_sheffield_manometer_1961_glynn_house_ph_meter_and_1994_atp_rotor [5.50s..7.90s] (2.40s distinct non-overlapping tail window from 8.00s source clip).",
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
                row["reuse_of"] = "P1:07_table_three_props_1937_sheffield_manometer_1961_glynn_house_ph_meter_and_1994_atp_rotor"
                row["reuse_window_s"] = [5.5, 7.9]
                row["reuse_audit"] = {
                    "source_row": "P1:07_table_three_props_1937_sheffield_manometer_1961_glynn_house_ph_meter_and_1994_atp_rotor",
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
            "film": "063_Krebs-Mitchell-Margulis-Mitochondria-ATP",
            "part": p_idx,
            "title": p_title,
            "version": "v01",
            "timing_status": "pre_vo_script_clock (built from mitochondria_script_master_v01.md; retimes onto Scribe STT once VO locks)",
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
        "film": "063_Krebs-Mitchell-Margulis-Mitochondria-ATP",
        "version": "v01",
        "date": "2026-10-19",
        "owner": "gemini (J0646)",
        "status": "PRE_VO_BOARDS_V01_NO_MINT",
        "generation_authorized": False,
        "script": "00_Brand/Channel-Setup/ideas/063_Krebs-Mitchell-Margulis-Mitochondria-ATP/mitochondria_script_master_v01.md",
        "sources": "00_Brand/Channel-Setup/ideas/063_Krebs-Mitchell-Margulis-Mitochondria-ATP/SOURCES_v01.md",
        "credit_snapshot": {
            "flow_balance": 23740,
            "flow_floor": 0,
            "flow_read_at": "2026-10-15T21:42:22Z",
            "vertex_promo_gbp": 71.02,
            "vertex_usable_gbp": 70.02,
        },
        "totals": totals,
        "per_part": per_part_summary,
        "mint_order": "006 > 007 > 008 > 009 > 010 > 011 > 012 > 013 > 014 > 015 > 016 > 017 > 018 > 019 > 020 > 021 > 022 > 023 > 024 > 025 > 026 > 027 > 028 > 029 > 030 > 031 > 032 > 033 > 034 > 035 > 036 > 037 > 038 > 039 > 040 > 041 > 042 > 043 > 044 > 045 > 046 > 047 > 048 > 049 > 050 > 051 > 052 > 053 > 054 > 055 > 056 > 057 > 058 > 059 > 060 > 061 > 062 > 063 > 064 > 065. Nothing in 063 is generation_authorized.",
    }
    (EDIT / "PICTURE_PLAN_v01.json").write_text(json.dumps(plan, indent=2) + "\n")

    sl = [
        "# 063 Mitochondria: How Swallowed Bacteria Power Your Cells — Shot list & plate boards v01 (pre-VO)",
        "",
        "Gemini, 19 Oct 2026, J0646. Built from `mitochondria_script_master_v01.md` (`92.0 PASS`) and `SOURCES_v01.md`.",
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
        "# 063 price review v01 (pre-VO plate boards)",
        "",
        "Gemini, 19 Oct 2026, J0646. Boards only. **No mint. No spend. No merge.**",
        "Prepared from `mitochondria_script_master_v01.md` (`92.0 PASS`) and `SOURCES_v01.md` so 063's full plate board rows, non-emissive Fast prompts, £0 code graphics, and Teach-on-Screen overlays are ready to re-time the moment long VO locks. Parked for Chief.",
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
        f"- **Quality ({totals['Quality']} rows):** readable faces (Hans A. Krebs, William A. Johnson, Peter D. Mitchell, Jennifer Moyle, Paul D. Boyer, John E. Walker, Lynn Margulis, Dmitri Ivanovsky, Wendell M. Stanley, Alfred D. Hershey, Martha Chase), June 1937 Sheffield pigeon-muscle manometers & *Nature* rejection letter, 8 July 1961 Glynn House chemiosmotic proton dam (`180 mV` across `5 nm` = `30 MV/m`), March 1967 endosymbiosis & 18 August 1994 atomic `F1Fo-ATP synthase` rotary motor (`~100 rev/s`), and the 2 Explorer beats.",
        f"- **Fast ({totals['Fast']} rows, non-emissive):** daylight prop and laboratory shots (glass Warburg manometer flask, brass millivoltmeter & wooden rotary turbine pan, 3-object callback bench, 1937 Sheffield notebook with 8-spoke chemical wheel & manometers, wooden 8-spoke waterwheel carrying 4-carbon and 2-carbon blocks, Cornish water-jacketed reaction vessel & pH electrode strip recorder, miniature wooden hydroelectric dam & lipid-bilayer model, brass-and-wood `F1Fo-ATP synthase` camshaft & circular `mtDNA` ring, maternal 37-gene `mtDNA` ring & sectioned mitochondrion on museum plinth). Zero candles, flames, sparks, or glowing elements on Fast.",
        f"- **£0 code graphics ({totals['code_graphic']} rows):**",
        "  1. `P1:04_krebs_1937_mitchell_1961_boyer_walker_1994_margulis_1967_respiration_chemiosmosis_chart` — 3-stage cellular respiration & chemiosmotic proton-motive force chart showing the 8-step Krebs Cycle, the `150–180 mV` proton gradient across the `5-nm` inner membrane (`~30 million V/m`), and `F1Fo-ATP synthase` spinning at `~100 rev/s` (`~30–32 ATP/glucose`) (`SCALE: a voltage of just 180 millivolts across a membrane five billionths of a metre thick creates an electric field of thirty million volts per metre — as intense as a bolt of lightning inside every cell of your body`)",
        "  2. `P1:06_meerman_brown_2014_bmj_10kg_fat_oxidation_to_8_4kg_exhaled_co2_mass_balance_chart` — Lavoisier (1789) & Meerman and Brown (December 2014 *BMJ* 349: g7257) human fat oxidation mass-balance chart (`10 kg` fat + `29 kg O₂` → `8.4 kg` exhaled `CO₂` [84%] + `1.6 kg H₂O` [16%]) (`SCALE: when you exercise and lose ten kilograms of body fat, your fat doesn't turn into heat or sweat — 8.4 kilograms of it leaves your body through your lungs as invisible carbon dioxide gas`)",
        "  3. `P2:02_krebs_johnson_aug_1937_enzymologia_eight_step_citric_acid_cycle_wheel_chart` — Krebs & Johnson (August 1937, *Enzymologia* 4: 148–156) 8-step Citric Acid Cycle diagram (`2 CO₂` + `3 NADH` + `1 FADH₂` + `1 GTP` per turn) (`SCALE: the Krebs cycle works like a waterwheel that never gets used up — a four-carbon bucket picks up a two-carbon piece of food, drops off two carbon dioxide molecules that you breathe out of your lungs, and comes right back around for the next load`)",
        "  4. `P3:02_mitchell_1961_moyle_1967_racker_stoeckenius_1974_chemiosmotic_proton_motive_force_chart` — Mitchell (8 July 1961, *Nature* 191: 144–148) & Racker and Stoeckenius (1974) chemiosmotic proton-motive force chart (`Δψ ~180 mV` + `ΔpH` across `5 nm` = `~30 MV/m`) (`SCALE: just as Hoover Dam holds back a lake of water so the rushing torrent can spin hydroelectric turbines, your mitochondria pump protons behind a five-nanometre membrane dam so the rushing protons can spin ATP synthase`)",
        "  5. `P4:02_boyer_walker_1994_atp_synthase_32_vs_2_atp_and_margulis_1967_16569bp_mtdna_chart` — Boyer & Walker (18 August 1994, *Nature* 370: 621–628) rotary ATP synthase & Margulis (March 1967, *J. Theor. Biol.* 14: 225–274) endosymbiosis chart (`~30–32 ATP` vs `2 ATP` from glycolysis; `16,569-bp` circular `mtDNA`) (`SCALE: without the ancient bacteria living inside your cells, a molecule of sugar would give you only two molecules of ATP instead of thirty-two — leaving complex animals with fifteen times too little energy to run, think, or keep a heart beating`)",
        "  6. `P5:01_timeline_1937_1994_and_maternal_16569bp_mitochondrial_dna_inheritance_chart` — completed 4-date timeline (1937 → 1994) + 100% maternal `16,569-bp` mitochondrial DNA inheritance diagram (`SCALE: from a rejected letter on pigeon muscle in Sheffield to a country-house lab in Cornwall and a two-billion-year bacterial partnership, three rebel scientists revealed why mitochondria truly are the powerhouse of the cell`)",
        f"- **£0 verified reuse ({totals['reuse']} row):** `P5:04_table_three_callback` uses the 2.40 s unused moving tail `[5.50s..7.90s]` of `P1:07_table_three_props_1937_sheffield_manometer_1961_glynn_house_ph_meter_and_1994_atp_rotor`.",
        "",
        "## Mint order",
        "",
        "006 > 007 > 008 > 009 > 010 > 011 > 012 > 013 > 014 > 015 > 016 > 017 > 018 > 019 > 020 > 021 > 022 > 023 > 024 > 025 > 026 > 027 > 028 > 029 > 030 > 031 > 032 > 033 > 034 > 035 > 036 > 037 > 038 > 039 > 040 > 041 > 042 > 043 > 044 > 045 > 046 > 047 > 048 > 049 > 050 > 051 > 052 > 053 > 054 > 055 > 056 > 057 > 058 > 059 > 060 > 061 > 062 > 063 > 064 > 065. `generation_authorized` is `false` on every row.",
    ])
    (EDIT / "PRICE_REVIEW_v01.md").write_text("\n".join(pr_lines) + "\n")
    print(f"063 v01 boards written: {totals['rows']} rows, Flow expected={totals['flow_credits_expected']}")


if __name__ == "__main__":
    main()
