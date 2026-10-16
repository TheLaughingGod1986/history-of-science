#!/usr/bin/env python3
"""HOS 024 (Conservation of Energy: How a Blunt Cannon Boiled Water) pre-VO plate boards v01. J0448. No mint, no spend.

Built from 00_Brand/Channel-Setup/ideas/024_Rumford-Joule-Thermodynamics/joule_script_master_v01.md
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
        "Part 01 — The Cannon That Boiled Without Fire",
        [
            ("01_munich_cannon_borer_boiling_water_1798", 0.0, 5.5, "A", False, "BOILED WITH ZERO FIRE", "Quality",
             "Quality: Short frame 0 / answer image (0:03) + two horses in the Munich arsenal in January 1798 turning an iron shaft that presses a blunt steel borer into a brass cannon inside a boiling wooden water box as astonished spectators step back.",
             STYLE + "Inside the Munich military arsenal in January 1798, two bay horses walk in a circle turning an iron shaft that presses a blunt steel borer into a rotating brass cannon cylinder encased in a pine box of water; thick white steam erupts from the boiling water box as astonished onlookers step back." + QUAL_TAIL,
             {"kind": "WHEN", "label": "MUNICH · JANUARY 1798", "timeline_step": "2/6 · 25 Jan 1798 (Rumford boils water with blunt cannon borer)", "hold_s": 3.5}),
            ("02_rumford_cannon_vs_joule_falling_weight_paddle", 5.5, 6.0, "B", False, "CANNON, PADDLE WHEEL, ALPS", "Quality",
             "Quality: readable faces (Count Rumford beside his steaming cannon box in Munich on the left; James Prescott Joule releasing two lead weights spinning a brass paddle wheel in Manchester on the right).",
             STYLE + "Split period composition: on the left, Count Rumford in Bavarian coat stands beside his steaming wooden cannon box in Munich; on the right, bearded young brewer James Prescott Joule releases two lead weights on pulleys spinning a brass paddle wheel inside a copper cylinder in Manchester." + QUAL_TAIL,
             None),
            ("03_lavoisier_caloric_sponge_iron_bar_bench", 11.5, 6.0, "C", False, "HEAT AS A FLUID?", "Fast",
             "Fast: daylight wooden table with an open eighteenth-century chemistry treatise beside a blacksmith's hammer resting on an unheated iron bar and metal shavings. No readable text on plate, nothing emissive.",
             STYLE + "In crisp daylight on a wooden table, a leather-bound eighteenth-century chemistry volume lies open beside an iron blacksmith's hammer, an unheated iron bar, and fine metal shavings." + FAST_TAIL,
             {"kind": "WHEN", "label": "1789–1798", "timeline_step": "1/6 · 1789 (Lavoisier lists 'caloric' fluid)", "hold_s": 3.5}),
            ("04_rumford_boiling_curve_and_joule_772_ftlbf_chart", 17.5, 8.0, "E", False, "60°F → 212°F · 772 FT-LBF = 1°F", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked comparison shows Rumford's Munich cannon box rising from 60°F to 212°F (boiling) in 150 minutes alongside Joule's falling-weight paddle wheel converting 772.692 foot-pounds of mechanical work into 1 BTU of heat (raising 1 lb of water by 1°F = 4.184 J/cal).",
             {"kind": "DATA", "label": "60°F → 212°F (150 MIN) · 772 FT·LBF = 1°F IN 1 LB WATER", "detail": "Inked comparison of Rumford's 1798 cannon-boring water temperature curve (0 min: 60°F → 60 min: 107°F → 90 min: 142°F → 120 min: 178°F → 150 min: 212°F boiling) and Joule's mechanical equivalent of heat (772 ft·lbf per 1°F in 1 lb water = 4.184 J/cal)", "scale": "772 foot-pounds of work for a single degree Fahrenheit — you have to drop a twenty-nine-pound weight twenty times from chest height just to warm one pint of water by a single degree", "who_card": "Benjamin Thompson, Count Rumford (1753–1814) — American-Bavarian military engineer · James Prescott Joule (1818–1889) — Manchester brewer and physicist", "when_stamp": "January 1798 · 1843–1849", "hold_s": 3.8}),
            ("05_joule_copper_calorimeter_and_pulleys_pan", 25.5, 5.5, "A", False, "29-POUND LEAD WEIGHTS", "Fast",
             "Fast: daylight pan across Joule's insulated copper calorimeter cylinder, wooden pulleys, silk twine, and two 29-pound lead weights in the Manchester cellar between code graphics so two full-frame graphics never run back to back.",
             STYLE + "In soft cellar window light, the camera tracks from two cylindrical lead weights suspended on silk twine over wooden pulleys to a polished copper calorimeter cylinder on a wooden stand." + FAST_TAIL,
             None),
            ("06_dancer_thermometer_1_200th_deg_f_scale_chart", 31.0, 8.0, "E", False, "1/200TH OF A DEGREE", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period parchment, an inked thermometer scale zooms in on 1°F divided into 200 graduations (0.005°F), showing Joule's 0.563°F temperature rise after 20 drops of two 29-pound weights falling 63 inches.",
             {"kind": "DATA", "label": "0.005°F (1/200TH °F) RESOLUTION · 0.563°F RISE PER 20 DROPS", "detail": "Inked thermometer scale comparing 1 full degree Fahrenheit against Joule's 0.005°F (1/200th °F) measurement resolution and the 0.563°F rise per 20-drop paddle-wheel run", "scale": "reading one two-hundredth of a degree Fahrenheit by eye — like spotting the thickness of a human hair on a ruler from across a table", "hold_s": 3.8}),
            ("07_table_three_props_blunt_borer_paddle_wheel_thermometer", 39.0, 5.5, "C", False, "MUNICH ARSENAL, 1798", "Fast",
             "Fast: daylight prop table (callback source for Part 05: blunt steel cannon borer with small heap of brass dust, multi-vaned brass paddle wheel, three-foot glass thermometer in brass case). Nothing emissive.",
             STYLE + "On a wooden workbench in soft daylight sit three objects side by side: a blunt steel cannon borer beside a tiny pinch of brass dust, a multi-vaned brass paddle wheel, and a long glass thermometer in a brass case." + FAST_TAIL,
             None),
            ("08_explorer_cannon_box_thermometer_and_brass_dust", 62.0, 5.5, "A", True, None, "Quality",
             "Quality: Explorer beat 1 (locked character reference, after 1:00).",
             STYLE + "Standing on the rim of the wooden water box beside the turning brass cannon, the Explorer dips a brass thermometer into the bubbling water, looks down at the tiny pinch of brass dust on a scale pan below, and scratches its head in wonder." + EXP_TAIL,
             None),
            ("09_munich_water_box_lid_lifted_steam_cloud", 67.5, 5.5, "B", False, "BOILING AT 212°F", "Fast",
             "Fast: daylight close-up of wooden tongs lifting the pine lid off the water box encasing the rotating brass cannon cylinder as thick white steam billows upward. No face, nothing emissive.",
             STYLE + "In daylight inside the arsenal workshop, wooden tongs lift the pine lid off the water box around the turning brass cannon cylinder as thick white clouds of steam billow into the air." + FAST_TAIL,
             None),
        ],
    ),
    (
        2,
        "Part 02 — The Spy Who Boiled a Cannon and Married Lavoisier's Widow",
        [
            ("01_rumford_munich_arsenal_blunt_borer_25_jan_1798", 73.0, 6.5, "A", False, "\"WITHOUT ANY FIRE\"", "Quality",
             "Quality: readable face (Count Rumford in Bavarian coat watching two horses turn the iron shaft pressing the blunt steel borer with 10,000 lb of force into the submerged brass cannon cylinder).",
             STYLE + "Munich,January 1798: Count Rumford in a dark blue Bavarian coat holds a pocket watch beside the rotating brass cannon cylinder submerged in its wooden water box while two horses turn the drive shaft behind him." + QUAL_TAIL,
             {"kind": "WHEN", "label": "MUNICH · 25 JANUARY 1798", "hold_s": 3.5}),
            ("02_54g_brass_dust_vs_8514g_boiling_water_diagram", 79.5, 8.0, "E", False, "54 G DUST VS 8,514 G BOILING WATER", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked comparison contrasts the tiny 54-gram (837-grain) heap of brass dust scraped off by Rumford's blunt borer against the 8,514 grams (18.77 pounds) of cold water brought from 60°F to a rolling 212°F boil in 150 minutes.",
             {"kind": "DATA", "label": "837 GRAINS (54 G) BRASS DUST VS 18.77 LB (8,514 G) BOILING WATER", "detail": "Inked comparison on period paper contrasting the 54 grams (837 grains) of brass dust abraded by Rumford's blunt borer against the 8,514 grams (18.77 lb) of water heated from 60°F to 212°F in 150 minutes", "scale": "less than two ounces of brass dust — the weight of ten coins — while boiling more than two gallons of water with zero fire", "hold_s": 3.8}),
            ("03_blunt_steel_borer_and_837_grains_dust_closeup", 87.5, 5.5, "B", False, "837 GRAINS OF DUST", "Fast",
             "Fast: daylight macro view of the flat blunt nose of the steel cannon borer resting beside a tiny heap of golden brass dust on a balance pan. No face, nothing emissive.",
             STYLE + "In crisp daylight, the flat blunt steel tip of the cannon borer rests beside a small brass balance pan holding a tiny pinch of golden metallic dust." + FAST_TAIL,
             None),
            ("04_rumford_and_marie_anne_lavoisier_paris_1805", 93.0, 6.5, "C", False, "PARIS · OCTOBER 1805", "Quality",
             "Quality: readable faces (Count Rumford standing beside Marie-Anne Paulze Lavoisier in a grand Paris salon in October 1805 with Antoine Lavoisier's portrait on the wall).",
             STYLE + "Paris, October 1805: Count Rumford stands in a sunlit neoclassical Paris salon beside chemist Marie-Anne Paulze Lavoisier in an Empire gown, with a framed portrait of Antoine Lavoisier hanging on the wall behind them." + QUAL_TAIL,
             {"kind": "WHO", "label": "Marie-Anne Paulze Lavoisier (1758–1836) — French chemist and translator", "fact_card": "Married Lavoisier's widow", "when_stamp": "October 1805", "hold_s": 3.8}),
        ],
    ),
    (
        3,
        "Part 03 — The Brewer's Son, the Paddle Wheel and 772 Foot-Pounds",
        [
            ("01_joule_manchester_cellar_winding_29lb_weights", 99.5, 6.5, "A", False, "THE BREWERY CELLAR LAB", "Quality",
             "Quality: readable face (twenty-six-year-old James Prescott Joule in his Manchester brewery cellar winding up the two 29-pound lead weights connected to the brass paddle wheel).",
             STYLE + "Manchester, June 1845: in a quiet brick brewery cellar, bearded young physicist James Prescott Joule turns a wooden roller handle to wind up two twenty-nine-pound lead weights on pulleys connected by silk twine to a brass paddle wheel inside an insulated copper tank." + QUAL_TAIL,
             {"kind": "WHEN", "label": "MANCHESTER · 1840 · JUNE 1845", "timeline_step": "4/6 · 1843–1849 (Joule's paddle wheel fixes 772 ft·lbf/BTU)", "hold_s": 3.5}),
            ("02_joule_reading_dancer_thermometer_through_telescope", 106.0, 6.5, "B", False, "WITHIN 0.8% OF MODERN VALUE", "Quality",
             "Quality: readable face (James Prescott Joule peering through a horizontal travelling telescope at John Benjamin Dancer's three-foot glass thermometer).",
             STYLE + "In the draft-free Manchester cellar, James Prescott Joule peers through a brass sighting telescope mounted on a tripod at a tall glass stem thermometer dipping into the copper water cylinder." + QUAL_TAIL,
             {"kind": "WHO", "label": "John Benjamin Dancer (1812–1887) — Manchester instrument maker", "fact_card": "Within 0.8% of modern value", "when_stamp": "1849", "hold_s": 3.8}),
            ("03_joule_water_mercury_iron_convergence_chart", 112.5, 8.0, "E", False, "772.69 WATER · 774.08 MERCURY · 774.98 IRON", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked convergence chart compares Joule's independent 1845–1849 measurements of the mechanical equivalent of heat across three different materials: Water paddle wheel = 772.69 ft·lbf, Mercury paddle wheel = 774.08 ft·lbf, and Cast-iron friction = 774.98 ft·lbf (vs modern 778.17 ft·lbf).",
             {"kind": "DATA", "label": "WATER 772.69 · MERCURY 774.08 · IRON 774.98 FT·LBF (MODERN 778.17)", "detail": "Inked convergence chart on period paper comparing Joule's 1845–1849 measurements across three materials: Water paddle wheel = 772.69 ft·lbf, Mercury paddle wheel = 774.08 ft·lbf, Cast-iron friction = 774.98 ft·lbf", "scale": "three completely different substances — water, liquid mercury, and solid iron — all landing within less than one percent of the exact same number", "hold_s": 3.8}),
            ("04_cutaway_brass_paddle_wheel_eight_arms_baffles", 120.5, 5.5, "C", False, "EIGHT REVOLVING ARMS", "Fast",
             "Fast: daylight close-up of Joule's brass paddle wheel with eight revolving arms passing cleanly between four stationary copper vanes inside the open calorimeter tank. Nothing emissive, no face.",
             STYLE + "In crisp daylight, a polished brass paddle wheel with eight sets of revolving arms rotates smoothly between four stationary copper baffle vanes inside an open cylindrical tank." + FAST_TAIL,
             None),
        ],
    ),
    (
        4,
        "Part 04 — The Oxford Interruption and the Honeymoon Thermometer",
        [
            ("01_oxford_1847_joule_and_young_william_thomson", 126.0, 6.5, "A", False, "SAVED FROM SILENCE", "Quality",
             "Quality: readable faces (impatient chairman and James Prescott Joule on stage at Oxford on 23 June 1847; 23-year-old William Thomson standing up in the back row).",
             STYLE + "Oxford, 23 June 1847: in a tiered wooden lecture hall, James Prescott Joule stands beside his copper paddle-wheel cylinder while twenty-three-year-old William Thomson rises eagerly in the back row to ask a question." + QUAL_TAIL,
             {"kind": "WHO", "label": "William Thomson, Lord Kelvin (1824–1907) — Scottish physicist and mathematician", "when_stamp": "Oxford, 23 June 1847", "timeline_step": "5/6 · Jun & Aug 1847 (Oxford meeting, Alps honeymoon & Helmholtz)", "hold_s": 3.8}),
            ("02_chamonix_honeymoon_joule_with_waterfall_thermometer", 132.5, 6.5, "B", False, "CHAMONIX · AUGUST 1847", "Quality",
             "Quality: readable faces (William Thomson meeting newlywed James Prescott Joule walking beside his bride's carriage on the Chamonix mountain road carrying a long brass-cased thermometer).",
             STYLE + "Chamonix road, Swiss Alps, August 1847: in bright Alpine sunshine beneath snow-capped peaks, William Thomson greets newlywed James Prescott Joule walking beside a horse-drawn carriage while carrying a three-foot brass-cased thermometer toward a roaring mountain waterfall." + QUAL_TAIL,
             {"kind": "FACT", "label": "Brought thermometer on honeymoon", "when_stamp": "18 August 1847 · August 1847", "hold_s": 3.8}),
            ("03_mayer_java_1840_ship_and_helmholtz_1847_treatise", 139.0, 6.0, "C", False, "JAVA 1840 · BERLIN 1847", "Quality",
             "Quality: readable faces (ship's doctor Julius Robert Mayer on a sailing ship at Surabaya roadstead in July 1840 and Hermann von Helmholtz at his Berlin desk in 1847).",
             STYLE + "Split period composition: on the left, German ship's physician Julius Robert Mayer on a sunlit wooden ship deck in tropical Java examines a glass basin; on the right, Hermann von Helmholtz writes at his Berlin desk beside a brass pendulum." + QUAL_TAIL,
             {"kind": "WHO", "label": "Julius Robert Mayer (1814–1878) — German physician and physicist · Hermann von Helmholtz (1821–1894) — German physician and physicist", "fact_card": "Venous blood redder in tropics", "when_stamp": "Java, July 1840 · May 1842 · 1847", "timeline_step": "3/6 · Jul 1840 (Mayer observes bright red venous blood in Java)", "hold_s": 3.8}),
            ("04_explorer_alpine_waterfall_thermometer_splash", 145.0, 5.5, "B", True, None, "Quality",
             "Quality: Explorer beat 2 (locked character reference).",
             STYLE + "Standing on the wet mossy rocks at the foot of the Alpine waterfall, the Explorer holds an oversized brass thermometer out into the flying mist, gets splashed by a cold spray of water, and shakes droplets off its round gold glasses with a grin." + EXP_TAIL,
             None),
        ],
    ),
    (
        5,
        "Part 05 — Why Stirring Tea Doesn't Boil It and Why Perpetual Motion Fails",
        [
            ("01_timeline_1789_1850_and_4184j_heat_capacity_scale", 150.5, 8.5, "E", False, "4,184 JOULES PER KG·°C", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, the 6-date timeline completes: 1789 (Lavoisier caloric) · 25 Jan 1798 (Rumford cannon) · Jul 1840 (Mayer in Java) · 1843–1849 (Joule's 772 ft·lbf paddle wheel) · Jun & Aug 1847 (Oxford, Chamonix & Helmholtz) · 1850 (Clausius & Thomson Second Law), alongside an inked heat-capacity scale showing 4,184 joules required to raise 1 kg of water by 1°C.",
             {"kind": "DATA", "label": "4,184 JOULES PER KG·°C (= LIFTING 42 KG SUITCASE 10 M)", "detail": "Animated 6-date timeline (1789 → 1850) alongside an inked heat-capacity scale showing 4,184 joules required to warm 1 kilogram of water by 1°C", "scale": "4,184 joules to warm one kilogram of water by one degree Celsius — equal to lifting a 42-kilogram suitcase ten metres into the air", "who_card": "Rudolf Clausius (1822–1888) — German physicist", "when_stamp": "1850 · 1789–1850", "timeline_step": "6/6 · 1850 (Clausius & Thomson formulate the Second Law)", "hold_s": 3.8}),
            ("02_stirring_porcelain_teacup_and_cooling_steam_bench", 159.0, 5.5, "A", False, "THE SECOND LAW", "Fast",
             "Fast: daylight close-up of a silver spoon stirring warm tea inside a porcelain cup on a wooden table as gentle wisps of vapour drift into the cooler room air. Nothing emissive, no face.",
             STYLE + "In soft morning window light, a silver teaspoon stirs amber tea inside a white porcelain cup on a wooden table while faint wisps of warm vapour drift outward into the room." + FAST_TAIL,
             None),
            ("03_young_playing_card_sunbeam_and_arago_spot_handoff", 164.5, 6.5, "C", False, "WAVE OR PARTICLE?", "Quality",
             "Quality: physician Thomas Young holding the edge of a playing card inside a pinhole sunbeam in London on 24 November 1801 to cast striped interference bands, dissolving into François Arago's bright spot at the centre of a 2 mm disc's shadow (handoff to 025 Young/Fresnel/Einstein Light).",
             STYLE + "In a darkened London room in November 1801, a narrow pinhole sunbeam strikes the thin edge of a playing card held in a brass stand to cast glowing rainbow-edged interference stripes on the wall, dissolving into a bright star of light shining at the dead centre of a circular shadow." + QUAL_TAIL,
             {"kind": "WHEN", "label": "24 NOVEMBER 1801 · 15 MARCH 1819", "hold_s": 3.5}),
            ("04_table_three_callback", 171.0, 2.4, "C", False, None, "reuse",
             "Reuse: verified unused moving window [5.50s..7.90s] of P1:07_table_three_props_blunt_borer_paddle_wheel_thermometer (callback, £0).",
             "Reuse P1:07_table_three_props_blunt_borer_paddle_wheel_thermometer [5.50s..7.90s] (2.40s distinct non-overlapping tail window from 8.00s source clip).",
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
                row["reuse_of"] = "P1:07_table_three_props_blunt_borer_paddle_wheel_thermometer"
                row["reuse_window_s"] = [5.5, 7.9]
                row["reuse_audit"] = {
                    "source_row": "P1:07_table_three_props_blunt_borer_paddle_wheel_thermometer",
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
            "film": "024_Rumford-Joule-Thermodynamics",
            "part": p_idx,
            "title": p_title,
            "version": "v01",
            "timing_status": "pre_vo_script_clock (built from joule_script_master_v01.md; retimes onto Scribe STT once VO locks)",
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
        "film": "024_Rumford-Joule-Thermodynamics",
        "version": "v01",
        "date": "2026-10-17",
        "owner": "gemini (J0448)",
        "status": "PRE_VO_BOARDS_V01_NO_MINT",
        "generation_authorized": False,
        "script": "00_Brand/Channel-Setup/ideas/024_Rumford-Joule-Thermodynamics/joule_script_master_v01.md",
        "sources": "00_Brand/Channel-Setup/ideas/024_Rumford-Joule-Thermodynamics/SOURCES_v01.md",
        "credit_snapshot": {
            "flow_Balance": 23740,
            "flow_floor": 0,
            "flow_read_at": "2026-10-15T21:42:22Z",
            "vertex_promo_gbp": 71.02,
            "vertex_usable_gbp": 70.02,
        },
        "totals": totals,
        "per_part": per_part_summary,
        "mint_order": "006 > 007 > 008 > 009 > 010 > 011 > 012 > 013 > 014 > 015 > 016 > 017 > 018 > 019 > 020 > 021 > 022 > 023 > 024. Nothing in 024 is generation_authorized.",
    }
    (EDIT / "PICTURE_PLAN_v01.json").write_text(json.dumps(plan, indent=2) + "\n")

    sl = [
        "# 024 Conservation of Energy: How a Blunt Cannon Boiled Water — Shot list & plate boards v01 (pre-VO)",
        "",
        "Gemini, 17 Oct 2026, J0448. Built from `joule_script_master_v01.md` (90.9 PASS) and `SOURCES_v01.md`.",
        "**No mint, no spend.** Pre-VO clock timings (`173.4 s` base picture grid; re-times automatically onto Scribe word timestamps once long VO locks).",
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
        "# 024 price review v01 (pre-VO plate boards)",
        "",
        "Gemini, 17 Oct 2026, J0448. Boards only. **No mint. No spend. No merge.**",
        "Prepared from `joule_script_master_v01.md` (90.9 PASS) and `SOURCES_v01.md` so 024's full plate board rows, non-emissive Fast prompts, £0 code graphics, and Teach-on-Screen overlays are ready to re-time the moment long VO locks. Parked for Chief.",
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
        f"- **Quality ({totals['Quality']} rows):** readable faces (Benjamin Thompson Count Rumford, Marie-Anne Paulze Lavoisier, James Prescott Joule, William Thomson Lord Kelvin, Julius Robert Mayer, Hermann von Helmholtz), emissive/sunbeam scenes (Young playing-card sunbeam handoff), and the 2 Explorer beats.",
        f"- **Fast ({totals['Fast']} rows, non-emissive):** daylight prop and laboratory shots (Lavoisier textbook & iron bar with hammer, Joule copper calorimeter & pulleys pan, 3-object callback bench, Munich boiling water box lid lifted with steam, blunt steel cannon borer & 837 grains brass dust, cutaway 8-arm brass paddle wheel, porcelain teacup stirred with silver spoon). Zero candles, flames, sparks, or glowing elements on Fast.",
        f"- **£0 code graphics ({totals['code_graphic']} rows):**",
        "  1. `P1:04_rumford_boiling_curve_and_joule_772_ftlbf_chart` — Rumford's 1798 cannon-boring curve (60°F → 212°F in 150 min) and Joule's 772 ft·lbf per 1°F in 1 lb water (`SCALE: 772 foot-pounds of work for a single degree Fahrenheit — you have to drop a twenty-nine-pound weight twenty times from chest height just to warm one pint of water by a single degree`)",
        "  2. `P1:06_dancer_thermometer_1_200th_deg_f_scale_chart` — Dancer's 0.005°F (1/200th °F) thermometer graduations and 0.563°F rise per 20 drops (`SCALE: reading one two-hundredth of a degree Fahrenheit by eye — like spotting the thickness of a human hair on a ruler from across a table`)",
        "  3. `P2:02_54g_brass_dust_vs_8514g_boiling_water_diagram` — 54 g (837 grains) brass dust vs 8,514 g (18.77 lb) boiling water (`SCALE: less than two ounces of brass dust — the weight of ten coins — while boiling more than two gallons of water with zero fire`)",
        "  4. `P3:03_joule_water_mercury_iron_convergence_chart` — Joule's 1845–1849 mechanical equivalent across Water (772.69), Mercury (774.08), and Cast iron (774.98 ft·lbf) (`SCALE: three completely different substances — water, liquid mercury, and solid iron — all landing within less than one percent of the exact same number`)",
        "  5. `P5:01_timeline_1789_1850_and_4184j_heat_capacity_scale` — completed 6-date timeline (1789 → 1850) + 4,184 J/(kg·°C) water heat-capacity scale (`SCALE: 4,184 joules to warm one kilogram of water by one degree Celsius — equal to lifting a 42-kilogram suitcase ten metres into the air`)",
        f"- **£0 verified reuse ({totals['reuse']} row):** `P5:04_table_three_callback` uses the 2.40 s unused moving tail `[5.50s..7.90s]` of `P1:07_table_three_props_blunt_borer_paddle_wheel_thermometer`.",
        "",
        "## Mint order",
        "",
        "006 > 007 > 008 > 009 > 010 > 011 > 012 > 013 > 014 > 015 > 016 > 017 > 018 > 019 > 020 > 021 > 022 > 023 > 024. `generation_authorized` is `false` on every row.",
    ])
    (EDIT / "PRICE_REVIEW_v01.md").write_text("\n".join(pr_lines) + "\n")
    print(f"024 v01 boards written: {totals['rows']} rows, Flow expected={totals['flow_credits_expected']}")


if __name__ == "__main__":
    main()
