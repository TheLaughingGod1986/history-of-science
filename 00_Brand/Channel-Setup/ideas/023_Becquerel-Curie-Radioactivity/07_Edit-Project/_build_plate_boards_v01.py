#!/usr/bin/env python3
"""HOS 023 (Radioactivity: Why Marie Curie's Notebooks Still Glow) pre-VO plate boards v01. J0448. No mint, no spend.

Built from 00_Brand/Channel-Setup/ideas/023_Becquerel-Curie-Radioactivity/curie_script_master_v01.md
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
        "Part 01 — The Cross in the Dark Drawer",
        [
            ("01_becquerel_dark_drawer_maltese_cross_1896", 0.0, 5.5, "A", False, "BURNED IN TOTAL DARKNESS", "Quality",
             "Quality: Short frame 0 / answer image (0:03) + Henri Becquerel pulling the wrapped glass plate from a dark wooden drawer on 1 March 1896 to reveal the jet-black silhouette of a copper Maltese cross beside a pale blue-violet radium vial.",
             STYLE + "In a dim Paris laboratory on 1 March 1896, physicist Henri Becquerel lifts a glass photographic plate out of a dark wooden desk drawer into a developing tray, where the crisp jet-black silhouette of a copper Maltese cross appears beside a glass vial glowing with soft pale blue-violet light." + QUAL_TAIL,
             {"kind": "WHEN", "label": "PARIS · 1 MARCH 1896", "timeline_step": "1/7 · 1 Mar 1896 (Becquerel's dark-drawer Maltese cross)", "hold_s": 3.5}),
            ("02_becquerel_drawer_vs_curie_shed_cauldron_and_lead_box", 5.5, 6.0, "B", False, "DRAWER, CAULDRON, LEAD BOX", "Quality",
             "Quality: readable faces (Henri Becquerel examining his Maltese cross plate on the left; Marie Curie stirring a steaming iron cauldron of pitchblende in the Rue Lhomond shed beside a lead-lined notebook box on the right).",
             STYLE + "Split period composition: on the left, Henri Becquerel holds up the glass plate showing the dark Maltese cross silhouette; on the right, Marie Curie stirs a steaming cast-iron basin of brown pitchblende ore with an iron rod in a wooden shed beside a lead-lined storage box." + QUAL_TAIL,
             None),
            ("03_uranium_salts_on_window_sill_waiting_for_sun", 11.5, 6.0, "C", False, "NO RAYS WITHOUT SUN?", "Fast",
             "Fast: daylight window sill where yellow-green uranium crystals rest on a black paper packet beside a brass coin under grey overcast clouds. Nothing emissive, no face.",
             STYLE + "On a wooden laboratory window sill under overcast daylight, a dish of yellow-green mineral crystals rests atop a folded black-paper packet beside a copper Maltese cross." + FAST_TAIL,
             {"kind": "WHEN", "label": "FEBRUARY 1896", "hold_s": 3.5}),
            ("04_uranium_1x_pitchblende_4x_radium_1000000x_chart", 17.5, 8.0, "E", False, "1X URANIUM · 4X ORE · 1,000,000X RADIUM", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked radioactivity comparison chart shows pure Uranium (1x baseline) against raw Joachimsthal Pitchblende ore (4x more active on the Curie electrometer) and pure Radium discovered in December 1898 (over 1,000,000x more active than uranium).",
             {"kind": "DATA", "label": "URANIUM 1× · PITCHBLENDE 4× · RADIUM 1,000,000×", "detail": "Inked radioactivity comparison chart on period paper comparing pure Uranium (1× baseline), raw Joachimsthal Pitchblende ore (4× uranium), and pure Radium (over 1,000,000× uranium)", "scale": "one million times more active than uranium — a single pinch of radium pouring out as many rays as an entire freight-train car of uranium rock", "who_card": "Henri Becquerel (1852–1908) — French physics professor · Marie Skłodowska Curie (1867–1934) — Polish-French physicist and chemist · Pierre Curie (1859–1906) — French physics professor", "when_stamp": "26 February 1896 · 1 March 1896 · December 1898", "hold_s": 3.8}),
            ("05_rue_lhomond_pitchblende_sacks_and_cauldron_pan", 25.5, 5.5, "A", False, "TONNES OF BROWN ORE SLAG", "Fast",
             "Fast: daylight pan across burlap sacks of brown Joachimsthal pitchblende residue and a heavy cast-iron basin in the Rue Lhomond courtyard between code graphics so two full-frame graphics never run back to back.",
             STYLE + "In cool overcast daylight, the camera tracks across stacked burlap sacks of dark brown mineral residue and a heavy cast-iron cauldron outside a weathered wooden shed." + FAST_TAIL,
             None),
            ("06_tonnes_of_pitchblende_to_01g_radium_scale_chart", 31.0, 8.0, "E", False, "0.1 GRAM FROM TONNES", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period parchment, an inked mass-ratio scale compares several tonnes (1,000,000+ grams) of brown pitchblende waste sacks against 0.1 gram (1 decigram) of pure radium chloride crystals in a tiny glass dish.",
             {"kind": "DATA", "label": "TONNES OF ORE → 0.1 GRAM OF PURE RADIUM (JULY 1902)", "detail": "Inked yield comparison showing several tonnes (1,000,000+ grams) of Joachimsthal pitchblende residue refined over 45 months down to 0.1 gram of pure radium chloride", "scale": "ten million parts of rock for one part of radium — like hunting for a single grain of salt hidden inside a swimming pool of sand", "hold_s": 3.8}),
            ("07_table_three_props_cross_quartz_electrometer_lead_box", 39.0, 5.5, "C", False, "PARIS, FEBRUARY 1896", "Fast",
             "Fast: daylight prop table (callback source for Part 05: copper Maltese cross on black paper packet, brass piezoelectric quartz electrometer column, lead-lined notebook box). Nothing emissive.",
             STYLE + "On a wooden laboratory workbench in soft window light sit three objects side by side: a copper Maltese cross on a black-paper packet, a brass piezoelectric quartz electrometer column with hanging weights, and a grey lead-lined archive box." + FAST_TAIL,
             None),
            ("08_explorer_dark_drawer_maltese_cross_peek", 62.0, 5.5, "A", True, None, "Quality",
             "Quality: Explorer beat 1 (locked character reference, after 1:00).",
             STYLE + "Standing on the edge of the open wooden desk drawer, the Explorer slides the drawer nearly shut to plunge the uranium crystal into darkness, peeks inside as the silhouette of the copper Maltese cross imprints onto the plate beneath, and jumps back in astonishment." + EXP_TAIL,
             None),
            ("09_paris_overcast_sky_and_closed_wooden_drawer", 67.5, 5.5, "B", False, "FOUR CLOUDY DAYS", "Fast",
             "Fast: daylight tilt from heavy grey winter clouds above Paris rooftops down to a closed wooden desk drawer inside the museum laboratory. No face, nothing emissive.",
             STYLE + "From heavy grey February clouds rolling over slate rooftops in Paris, the camera tilts through a tall window to a closed mahogany desk drawer inside a quiet museum laboratory." + FAST_TAIL,
             None),
        ],
    ),
    (
        2,
        "Part 02 — The Cloudy Week in Paris and the Maltese Cross",
        [
            ("01_poincare_becquerel_academy_and_sun_packet_1896", 73.0, 6.5, "A", False, "TRIGGERED BY SUNLIGHT?", "Quality",
             "Quality: readable faces (Henri Poincaré showing Röntgen's bone X-ray to Henri Becquerel at the French Academy on 20 January 1896; Becquerel placing uranium crystals on a black-paper packet in bright sunshine on 24 February 1896).",
             STYLE + "Paris, 20 January and 24 February 1896: at the French Academy of Sciences, bearded mathematician Henri Poincaré holds up a glass X-ray plate of a hand to Henri Becquerel; in his museum laboratory, Becquerel sets yellow-green uranium crystals and a silver coin atop a black-paper packet on a sunny window ledge." + QUAL_TAIL,
             {"kind": "WHO", "label": "Henri Poincaré (1854–1912) — French mathematician and physicist", "when_stamp": "Paris, 20 January 1896 · 24 February 1896", "hold_s": 3.8}),
            ("02_becquerel_developing_maltese_cross_1_march_1896", 79.5, 6.5, "B", False, "1 MARCH 1896 · FULL BLACKENING", "Quality",
             "Quality: readable face (Henri Becquerel in his darkroom on 1 March 1896 watching the jet-black silhouette of the copper Maltese cross appear at full strength on the glass plate).",
             STYLE + "Paris, 1 March 1896: Henri Becquerel bends over a porcelain developing tray in his laboratory as the sharp black silhouette of the copper Maltese cross emerges at full strength on the glass plate." + QUAL_TAIL,
             {"kind": "FACT", "label": "No sunlight needed at all", "when_stamp": "26 February 1896 · 1 March 1896 · 2 March 1896", "hold_s": 3.8}),
            ("03_drawer_exposure_0h_sun_vs_96h_dark_diagram", 86.0, 8.0, "E", False, "0 HOURS SUN = FULL EXPOSURE", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked exposure comparison contrasts Becquerel's sunlight hypothesis (0 hours of sun in the dark drawer = faint or zero image) against the 1 March 1896 developed plate (96 hours in total darkness = jet-black silhouette around the copper Maltese cross).",
             {"kind": "DATA", "label": "0 H SUNLIGHT · 96 H DARK DRAWER = FULL EXPOSURE", "detail": "Inked exposure comparison on period paper contrasting Becquerel's sunlight expectation (0 hours of sunlight = 0 exposure) against the 1 March 1896 result (96 hours in a pitch-dark drawer = full-strength blackening across the Maltese cross)", "scale": "four days locked in a pitch-black drawer with zero sunlight — and the rock burned an image as strong as midday sun", "hold_s": 3.8}),
            ("04_copper_maltese_cross_and_developed_plate_closeup", 94.0, 5.5, "C", False, "SPONTANEOUS RAYS", "Fast",
             "Fast: daylight macro shot of the thin copper Maltese cross resting beside the developed glass photographic plate showing its white cross shadow on a wooden desk. Nothing emissive, no face.",
             STYLE + "In crisp daylight on a mahogany desk, a small copper Maltese cross rests beside a developed glass photographic plate bearing its sharp silhouette." + FAST_TAIL,
             None),
        ],
    ),
    (
        3,
        "Part 03 — The Quartz Balance and the Pitchblende Shock",
        [
            ("01_marie_warsaw_floating_uni_to_paris_electrometer", 99.5, 6.5, "A", False, "PARIS · LATE 1897", "Quality",
             "Quality: readable faces (young Maria Skłodowska in Warsaw and operating the piezoelectric quartz electrometer in Paris alongside Pierre Curie and Jacques Curie).",
             STYLE + "Paris, late 1897: young physicist Marie Curie in a high-collared dark dress sits at a wooden bench beside Pierre Curie and Jacques Curie, placing weights on a vertical quartz-crystal balance connected to a brass ionization chamber and timing a light spot with a pocket stopwatch." + QUAL_TAIL,
             {"kind": "WHO", "label": "Jacques Curie (1856–1941) — French mineralogist and physicist", "fact_card": "Studied at secret university", "when_stamp": "Paris, 1891 · Late 1897", "hold_s": 3.8}),
            ("02_curie_electrometer_24_52_83_pa_bar_chart", 106.0, 8.0, "E", False, "24 PA URANIUM · 83 PA PITCHBLENDE", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked bar chart from Marie Curie's 12 April 1898 Academy note compares the piezoelectric quartz electrometer currents: Metallic Uranium = 24 picocoulombs/s (24 × 10⁻¹² A), Natural Chalcolite = 52 picocoulombs/s (~2× uranium), and Joachimsthal Pitchblende ore = 83 picocoulombs/s (~3.5–4× uranium).",
             {"kind": "DATA", "label": "URANIUM 24 PA · CHALCOLITE 52 PA · PITCHBLENDE 83 PA (~4×)", "detail": "Inked electrometer current bar chart from Marie Curie's 12 April 1898 Academy paper: Metallic Uranium = 24 pA, Natural Chalcolite = 52 pA (~2× uranium), Joachimsthal Pitchblende = 83 pA (~3.5–4× uranium)", "scale": "83 trillionths of an ampere — an electric current a hundred billion times smaller than a household lightbulb, measured with a stretched crystal of quartz and a stopwatch", "when_stamp": "12 April 1898", "timeline_step": "2/7 · 12 Apr 1898 (Pitchblende 4× more active than uranium)", "hold_s": 3.8}),
            ("03_pitchblende_lump_on_brass_condenser_plate_closeup", 114.0, 6.0, "B", False, "FOUR TIMES STRONGER THAN URANIUM", "Fast",
             "Fast: daylight close-up of a heavy black lump of Joachimsthal pitchblende placed between the two horizontal brass disc plates of the Curie ionization chamber while a brass weight drops onto the quartz balance pan. No face, nothing emissive.",
             STYLE + "In crisp daylight, a heavy dark lump of black pitchblende ore sits on the lower brass disc plate of an ionization chamber while a small brass weight is set onto the pan of a vertical quartz balance." + FAST_TAIL,
             None),
            ("04_piezoelectric_quartz_blade_and_stopwatch_bench", 120.0, 5.5, "C", False, "RADIOACTIVITY NAMED", "Fast",
             "Fast: daylight macro view of the thin transparent quartz crystal blade mounted in brass clamps beside a ticking silver pocket stopwatch on Marie Curie's bench. Nothing emissive.",
             STYLE + "In soft window light, a thin transparent quartz crystal blade hangs in brass clamps above a weight pan beside an open silver pocket stopwatch on a wooden laboratory bench." + FAST_TAIL,
             None),
        ],
    ),
    (
        4,
        "Part 04 — The Freezing Shed, 0.1 Gram of Radium and the Nobel Letter",
        [
            ("01_curie_shed_stirring_cauldron_and_fairy_lights", 125.5, 6.5, "A", False, "POLONIUM AND RADIUM · 1898–1902", "Quality",
             "Quality: readable faces (Marie and Pierre Curie with Gustave Bémont and Eugène-Anatole Demarçay; Marie stirring a 20-kg boiling cauldron in the Rue Lhomond shed and watching radium vials glow like 'faint, fairy lights' in the dark).",
             STYLE + "Rue Lhomond, Paris, 1898 to July 1902: inside the weathered wooden shed, Marie Curie stirs a steaming twenty-kilogram cast-iron cauldron of brown pitchblende with an iron rod beside Pierre Curie, Gustave Bémont and Eugène-Anatole Demarçay; as dusk falls, tiny glass dishes on the shelf glow with soft pale blue-violet light." + QUAL_TAIL,
             {"kind": "WHO", "label": "Gustave Bémont (1857–1932) — Paris laboratory chief · Eugène-Anatole Demarçay (1852–1903) — French spectroscopist", "when_stamp": "18 July 1898 · 26 December 1898 · July 1902 · March 1903", "timeline_step": "3/7 · Jul & Dec 1898 (Polonium & Radium) & 4/7 · Jul 1902 (0.1 g pure radium)", "hold_s": 3.8}),
            ("02_1903_nobel_nomination_letter_vs_mittag_leffler_and_1911", 132.0, 6.5, "B", False, "2 NOBELS IN 2 SCIENCES", "Quality",
             "Quality: readable faces (Swedish mathematician Gösta Mittag-Leffler warning Pierre Curie about the 1903 French nomination letter omitting Marie; Marie Curie receiving the 1903 Physics Nobel and 1911 Chemistry Nobel).",
             STYLE + "Split period portrait: on the left, Swedish mathematician Gösta Mittag-Leffler hands a warning letter to Pierre Curie; on the right, Marie Curie holds two gold Nobel medals in Stockholm." + QUAL_TAIL,
             {"kind": "WHO", "label": "Gösta Mittag-Leffler (1846–1927) — Swedish mathematician", "fact_card": "2 Nobels in 2 sciences", "when_stamp": "December 1903 · 1911", "timeline_step": "5/7 · Dec 1903 (Physics Nobel) & 6/7 · 1911 (Chemistry Nobel)", "hold_s": 3.8}),
            ("03_01g_radium_chloride_dish_on_balance_1902", 138.5, 5.5, "C", False, "\"FAINT, FAIRY LIGHTS\"", "Fast",
             "Fast: daylight close-up of a tiny porcelain watch glass holding 0.1 gram of white radium chloride crystals on a precision brass analytical balance. No face, nothing emissive.",
             STYLE + "In crisp daylight inside a glass balance case, a tiny porcelain watch glass holding a pinch of white crystalline salt rests on the brass pan of a precision analytical balance." + FAST_TAIL,
             None),
            ("04_explorer_radium_vial_thermometer_shed", 144.0, 5.5, "B", True, None, "Quality",
             "Quality: Explorer beat 2 (locked character reference).",
             STYLE + "Standing in the darkened wooden shed beside a row of tiny glass vials glowing with pale blue-violet light, the Explorer holds a small thermometer against a radium tube, sees the mercury column rise warmer than the room air, and warms its hands in amazement." + EXP_TAIL,
             None),
        ],
    ),
    (
        5,
        "Part 05 — Why Radium Glows for 1,600 Years and the Lead-Lined Notebooks",
        [
            ("01_timeline_1896_3500ad_and_1600yr_decay_curve", 149.5, 8.5, "E", False, "1,600-YEAR HALF-LIFE · 3500 AD", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, the 7-date timeline completes: 1 Mar 1896 (Becquerel drawer) · 12 Apr 1898 (Pitchblende 4× anomaly) · Jul & Dec 1898 (Polonium & Radium) · Jul 1902 (0.1 g pure radium) · Dec 1903 (Physics Nobel) · 1911 (Chemistry Nobel) · 3500 AD (one 1,600-year Radium-226 half-life later), alongside an inked decay chain (U-238 → Ra-226 → Pb-206) and 1,600-year half-life curve.",
             {"kind": "DATA", "label": "RADIUM-226 HALF-LIFE: 1,600 YEARS (1899 → 3500 AD)", "detail": "Animated 7-date timeline (1896 → 3500 AD) alongside an inked Radium-226 nuclear transmutation decay chain and 1,600-year half-life curve", "scale": "a half-life of 1,600 years — if a Roman emperor had spilled radium in 400 AD, half of those exact atoms would still be firing radiation today", "who_card": "Frederick Soddy (1877–1956) — English radiochemist", "fact_card": "Notebooks need lead for 1,600 yr", "when_stamp": "1902–1903 · 4 July 1934 · 3500 AD · 1896–3500 AD", "timeline_step": "7/7 · 3500 AD (One 1,600-year Radium-226 half-life later)", "hold_s": 3.8}),
            ("02_bnf_lead_lined_box_and_curie_notebook_paris", 158.0, 6.0, "A", False, "STILL RADIOACTIVE TODAY", "Fast",
             "Fast: daylight close-up in the Paris National Library archive as white-gloved hands lift a black cloth laboratory notebook out of a thick grey lead-lined box beside a brass Geiger probe. No readable text on plate, nothing emissive.",
             STYLE + "In bright archive daylight, white-gloved hands lift a worn black cloth-bound notebook out of a thick grey lead-lined storage box while a cylindrical metal detector probe rests beside the cover." + FAST_TAIL,
             None),
            ("03_munich_cannon_borer_and_joule_paddle_wheel_handoff", 164.0, 6.5, "C", False, "WHAT IS HEAT REALLY?", "Quality",
             "Quality: two horses turning a blunt steel borer inside a submerged brass cannon boiling water in Munich in January 1798, dissolving into James Prescott Joule's falling-weight brass paddle wheel in Manchester (handoff to 024 Thermodynamics).",
             STYLE + "Inside the Munich military arsenal in January 1798, two horses walk in a circle turning a blunt steel borer inside a brass cannon encased in a steaming wooden box of boiling water, dissolving into two lead weights on pulleys spinning a brass paddle wheel inside a copper cylinder." + QUAL_TAIL,
             {"kind": "WHEN", "label": "JANUARY 1798 · JUNE 1845", "hold_s": 3.5}),
            ("04_table_three_callback", 170.5, 2.4, "C", False, None, "reuse",
             "Reuse: verified unused moving window [5.50s..7.90s] of P1:07_table_three_props_cross_quartz_electrometer_lead_box (callback, £0).",
             "Reuse P1:07_table_three_props_cross_quartz_electrometer_lead_box [5.50s..7.90s] (2.40s distinct non-overlapping tail window from 8.00s source clip).",
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
                row["reuse_of"] = "P1:07_table_three_props_cross_quartz_electrometer_lead_box"
                row["reuse_window_s"] = [5.5, 7.9]
                row["reuse_audit"] = {
                    "source_row": "P1:07_table_three_props_cross_quartz_electrometer_lead_box",
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
            "film": "023_Becquerel-Curie-Radioactivity",
            "part": p_idx,
            "title": p_title,
            "version": "v01",
            "timing_status": "pre_vo_script_clock (built from curie_script_master_v01.md; retimes onto Scribe STT once VO locks)",
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
        "film": "023_Becquerel-Curie-Radioactivity",
        "version": "v01",
        "date": "2026-10-17",
        "owner": "gemini (J0448)",
        "status": "PRE_VO_BOARDS_V01_NO_MINT",
        "generation_authorized": False,
        "script": "00_Brand/Channel-Setup/ideas/023_Becquerel-Curie-Radioactivity/curie_script_master_v01.md",
        "sources": "00_Brand/Channel-Setup/ideas/023_Becquerel-Curie-Radioactivity/SOURCES_v01.md",
        "credit_snapshot": {
            "flow_Balance": 23740,
            "flow_floor": 0,
            "flow_read_at": "2026-10-15T21:42:22Z",
            "vertex_promo_gbp": 71.02,
            "vertex_usable_gbp": 70.02,
        },
        "totals": totals,
        "per_part": per_part_summary,
        "mint_order": "006 > 007 > 008 > 009 > 010 > 011 > 012 > 013 > 014 > 015 > 016 > 017 > 018 > 019 > 020 > 021 > 022 > 023. Nothing in 023 is generation_authorized.",
    }
    (EDIT / "PICTURE_PLAN_v01.json").write_text(json.dumps(plan, indent=2) + "\n")

    sl = [
        "# 023 Radioactivity: Why Marie Curie's Notebooks Still Glow — Shot list & plate boards v01 (pre-VO)",
        "",
        "Gemini, 17 Oct 2026, J0448. Built from `curie_script_master_v01.md` (91.6 PASS) and `SOURCES_v01.md`.",
        "**No mint, no spend.** Pre-VO clock timings (`172.9 s` base picture grid; re-times automatically onto Scribe word timestamps once long VO locks).",
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
        "# 023 price review v01 (pre-VO plate boards)",
        "",
        "Gemini, 17 Oct 2026, J0448. Boards only. **No mint. No spend. No merge.**",
        "Prepared from `curie_script_master_v01.md` (91.6 PASS) and `SOURCES_v01.md` so 023's full plate board rows, non-emissive Fast prompts, £0 code graphics, and Teach-on-Screen overlays are ready to re-time the moment long VO locks. Parked for Chief.",
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
        f"- **Quality ({totals['Quality']} rows):** readable faces (Henri Becquerel, Henri Poincaré, Marie Skłodowska Curie, Pierre Curie, Jacques Curie, Gustave Bémont, Eugène-Anatole Demarçay, Gösta Mittag-Leffler), emissive/glow scenes (1 March 1896 dark-drawer Maltese cross & pale blue-violet radium vial, Rue Lhomond 'faint, fairy lights', Munich cannon handoff), and the 2 Explorer beats.",
        f"- **Fast ({totals['Fast']} rows, non-emissive):** daylight prop and laboratory shots (uranium crystals on overcast window sill, Rue Lhomond pitchblende sacks & cauldron pan, 3-object callback bench, overcast Paris sky to closed desk drawer, copper Maltese cross & developed plate closeup, black pitchblende lump on brass condenser disc, quartz blade & stopwatch, 0.1 g radium chloride watch glass on analytical balance, BnF lead-lined notebook box). Zero candles, flames, sparks, or glowing elements on Fast.",
        f"- **£0 code graphics ({totals['code_graphic']} rows):**",
        "  1. `P1:04_uranium_1x_pitchblende_4x_radium_1000000x_chart` — Uranium (1×) vs Joachimsthal Pitchblende (4×) vs pure Radium (>1,000,000×) (`SCALE: one million times more active than uranium — a single pinch of radium pouring out as many rays as an entire freight-train car of uranium rock`)",
        "  2. `P1:06_tonnes_of_pitchblende_to_01g_radium_scale_chart` — several tonnes of brown pitchblende waste refined down to 0.1 g pure radium chloride (`SCALE: ten million parts of rock for one part of radium — like hunting for a single grain of salt hidden inside a swimming pool of sand`)",
        "  3. `P2:03_drawer_exposure_0h_sun_vs_96h_dark_diagram` — Becquerel's sunlight hypothesis (0 h sun = 0 exposure) vs 1 March 1896 result (96 h dark drawer = full blackening) (`SCALE: four days locked in a pitch-black drawer with zero sunlight — and the rock burned an image as strong as midday sun`)",
        "  4. `P3:02_curie_electrometer_24_52_83_pa_bar_chart` — Marie Curie's 12 April 1898 electrometer currents: Uranium 24 pA, Chalcolite 52 pA, Pitchblende 83 pA (`SCALE: 83 trillionths of an ampere — an electric current a hundred billion times smaller than a household lightbulb, measured with a stretched crystal of quartz and a stopwatch`)",
        "  5. `P5:01_timeline_1896_3500ad_and_1600yr_decay_curve` — completed 7-date timeline (1896 → 3500 AD) + Radium-226 1,600-year half-life decay curve (`SCALE: a half-life of 1,600 years — if a Roman emperor had spilled radium in 400 AD, half of those exact atoms would still be firing radiation today`)",
        f"- **£0 verified reuse ({totals['reuse']} row):** `P5:04_table_three_callback` uses the 2.40 s unused moving tail `[5.50s..7.90s]` of `P1:07_table_three_props_cross_quartz_electrometer_lead_box`.",
        "",
        "## Mint order",
        "",
        "006 > 007 > 008 > 009 > 010 > 011 > 012 > 013 > 014 > 015 > 016 > 017 > 018 > 019 > 020 > 021 > 022 > 023. `generation_authorized` is `false` on every row.",
    ])
    (EDIT / "PRICE_REVIEW_v01.md").write_text("\n".join(pr_lines) + "\n")
    print(f"023 v01 boards written: {totals['rows']} rows, Flow expected={totals['flow_credits_expected']}")


if __name__ == "__main__":
    main()
