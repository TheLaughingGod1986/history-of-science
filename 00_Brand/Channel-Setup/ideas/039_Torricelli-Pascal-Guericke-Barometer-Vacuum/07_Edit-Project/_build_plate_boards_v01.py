#!/usr/bin/env python3
"""HOS 039 (Atmospheric Pressure: Why 16 Horses Couldn't Pull Two Bowls Apart) pre-VO plate boards v01. J0524. No mint, no spend.

Built from 00_Brand/Channel-Setup/ideas/039_Torricelli-Pascal-Guericke-Barometer-Vacuum/barometer_script_master_v01.md
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
        "Part 01 — The Mercury Tube in Florence and Sixteen Horses in Germany",
        [
            ("01_guericke_8_may_1654_regensburg_16_horses_and_torricelli_1644_mercury_tube", 0.0, 5.5, "A", False, "SIXTEEN HORSES AND NO BOLTS", "Quality",
             "Quality: Short frame 0 / answer image (0:03) + in an imperial courtyard in Regensburg, Germany, on 8 May 1654, German mayor Otto von Guericke stands beside two 50-centimetre copper hemispheres sealed only with a greased leather ring while two teams of eight horses (16 horses total) strain against their harnesses without pulling the unbolted bowls apart, dissolving to a workshop in Florence in 1644 where Evangelista Torricelli and Vincenzo Viviani invert a four-foot glass tube of liquid mercury into a basin.",
             STYLE + "In a sunlit German courtyard on 8 May 1654, Otto von Guericke stands beside two joined copper hemispheres suspended on ropes while two teams of eight harnessed horses strain in opposite directions, dissolving to a Florentine workshop where Evangelista Torricelli and young Vincenzo Viviani hold an inverted four-foot glass tube of silvery mercury in a porcelain dish." + QUAL_TAIL,
             {"kind": "WHEN", "label": "REGENSBURG, 8 MAY 1654 · FLORENCE, 1644", "timeline_step": "2/6 · Jun 1644 (Torricelli & Viviani create the 30-inch mercury barometer and first sustained vacuum) & 4/6 · 8 May 1654 (Otto von Guericke's 16-horse Magdeburg hemispheres at Regensburg)", "hold_s": 3.5}),
            ("02_torricelli_1644_barometer_perier_1648_mountain_and_guericke_1654_hemispheres_split", 5.5, 6.0, "B", False, "MERCURY, MOUNTAIN, VACUUM", "Quality",
             "Quality: complex three-part split composition (Evangelista Torricelli's 1644 30-inch mercury barometer tube in Florence on the left; Florin Périer carrying a barometer up the volcanic peak of Puy-de-Dôme on 19 September 1648 in the centre; Otto von Guericke's 8 May 1654 Magdeburg hemispheres clamping shut against 16 horses on the right).",
             STYLE + "Three-panel period composition: on the left, a tall glass tube of silvery mercury standing in a porcelain basin in Florence; in the centre, a cloaked French experimentalist holding a wooden-framed barometer on a rocky mountain summit; on the right, two copper hemispheres held shut by air pressure against straining harness ropes." + QUAL_TAIL,
             None),
            ("03_torricelli_and_viviani_11_june_1644_florence_inverting_mercury_tube", 11.5, 6.0, "C", False, "THE FIRST VACUUM", "Quality",
             "Quality: readable faces (inside a Florentine workshop in June 1644, 35-year-old Evangelista Torricelli and 21-year-old Vincenzo Viviani invert a 1.2-metre glass tube of liquid mercury with a finger over its open end, submerging it into a dish of mercury as the silver column drops away from the sealed top).",
             STYLE + "Inside a sunlit 1644 workshop in Florence, thirty-five-year-old Italian physicist Evangelista Torricelli and young Vincenzo Viviani invert a four-foot glass tube of gleaming liquid mercury into a dish, watching the silvery column drop slightly to leave a clear empty space at the sealed top." + QUAL_TAIL,
             {"kind": "WHEN", "label": "FLORENCE, 11 JUNE 1644", "timeline_step": "2/6 · Jun 1644 (Evangelista Torricelli & Vincenzo Viviani create the 30-inch mercury barometer)", "hold_s": 3.5}),
            ("04_water_32ft_vs_mercury_30in_hydrostatic_balance_101kpa_chart", 17.5, 8.0, "E", False, "32 FEET (10.3 M) WATER VS 30 INCHES (760 MM) MERCURY (13.6× DENSER) = 14.7 PSI", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked height-and-density balance chart compares 10.3 metres (32 feet / 18 braccia) of water (density 1.0 g/cm³) against 760 millimetres (30 inches / 1.25 braccia) of liquid mercury (density 13.6 g/cm³), both balanced by downward atmospheric pressure of 101.3 kPa (14.7 lb/in² = 1.03 kg/cm²) at sea level.",
             {"kind": "DATA", "label": "10.3 M (32 FT) WATER (1.0 G/CM³) VS 760 MM (30 IN) MERCURY (13.6 G/CM³) = 101.3 KPA (14.7 PSI)", "detail": "Inked height-and-density balance chart on period paper comparing 10.3 metres (32 feet) of water (density 1.0 g/cm³) against 760 millimetres (30 inches) of liquid mercury (density 13.6 g/cm³), both exerting 101.3 kPa (14.7 lb/in²) at sea level", "scale": "because liquid mercury is nearly fourteen times heavier than water, a thirty-inch tube of mercury on your desk weighs the exact same per square inch as a thirty-two-foot tower of water three storeys high", "who_card": "Evangelista Torricelli (1608–1647) — Italian physicist · Blaise Pascal (1623–1662) — French mathematician · Otto von Guericke (1602–1686) — German engineer and mayor", "when_stamp": "1643 · 19 September 1648 · 8 May 1654", "hold_s": 3.8}),
            ("05_mercury_basin_glass_barometer_tube_and_brass_calipers_pan", 25.5, 5.5, "A", False, "FLORENCE, 1644", "Fast",
             "Fast: daylight macro pan across a porcelain basin of silvery liquid mercury, the base of a vertical glass barometer tube, and brass measuring calipers on an oak bench between code graphics so two full-frame graphics never run back to back. Nothing emissive, no face.",
             STYLE + "In crisp daylight on an oak laboratory bench, the camera pans smoothly across a porcelain dish of silvery liquid mercury supporting a vertical glass tube beside brass measuring calipers." + FAST_TAIL,
             None),
            ("06_atmospheric_load_14_7_psi_10_tonnes_on_human_body_scale_bar", 31.0, 8.0, "E", False, "TEN TONNES OF AIR", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period parchment, an inked atmospheric-load scale bar shows a 1-square-inch column of air reaching from sea level to space weighing 14.7 pounds (1.03 kg/cm² = 101,325 Pa), summing to ~10,000 kg (10 metric tonnes) of force pressing inward across the ~1.7 m² surface area of an adult human body.",
             {"kind": "DATA", "label": "14.7 PSI (1.03 KG/CM²) AIR PRESSURE = ~10,000 KG (10 TONNES) OVER AN ADULT BODY (~1.7 M²)", "detail": "Inked atmospheric-load scale bar showing 14.7 pounds per square inch (1.03 kg/cm² = 101,325 Pa) summing to ~10,000 kg (10 metric tonnes) over the ~1.7 m² surface area of a human body", "scale": "the air pressing inward on your skin right now weighs around ten tonnes — as heavy as a double-decker London bus, balanced only because the fluids inside your body push back out with the exact same force", "hold_s": 3.8}),
            ("07_table_three_props_suction_pump_cylinder_mercury_barometer_copper_hemispheres", 39.0, 5.5, "C", False, "1644 TO 1654", "Fast",
             "Fast: daylight prop table (callback source for Part 05: a wooden Florentine suction-pump cylinder, Torricelli's glass mercury tube in its basin, and Otto von Guericke's two copper Magdeburg hemispheres with a brass stopcock). Nothing emissive.",
             STYLE + "On an oak workbench in soft window light sit three objects side by side: a wooden suction-pump cylinder with an iron plunger, a tall glass mercury tube in a porcelain basin, and two joined copper hemispheres with a brass valve." + FAST_TAIL,
             None),
            ("08_explorer_tugging_miniature_brass_magdeburg_hemispheres_stopcock_hiss", 62.0, 5.5, "A", True, None, "Quality",
             "Quality: Explorer beat 1 (locked character reference, after 1:00).",
             STYLE + "Standing beside a miniature glass mercury barometer and tugging with both hands on two palm-sized brass Magdeburg hemispheres, the Explorer watches a tiny brass stopcock turn and tumbles gently backward as the two brass bowls fall effortlessly apart." + EXP_TAIL,
             None),
            ("09_torricelli_11_june_1644_florence_writing_ocean_of_air_letter_to_ricci", 67.5, 5.5, "B", False, "AN OCEAN OF AIR", "Quality",
             "Quality: readable face (on 11 June 1644 in Florence, Evangelista Torricelli dips his quill into ink beside his 30-inch mercury barometer and writes his letter to Michelangelo Ricci in Rome).",
             STYLE + "At a sunlit wooden desk in Florence on 11 June 1644, thirty-five-year-old Evangelista Torricelli dips a feather quill into an inkwell and writes on parchment beside a tall glass mercury barometer." + QUAL_TAIL,
             None),
        ],
    ),
    (
        2,
        "Part 02 — The 32-Foot Wall in Florence & Torricelli's 1644 Mercury Tube",
        [
            ("01_galileo_1638_florence_well_pump_and_torricelli_viviani_1644_barometer", 73.0, 6.5, "A", False, "STRAWS PUSH, NEVER SUCK", "Quality",
             "Quality: readable faces (Florentine well-diggers baffling an elderly Galileo Galilei in 1638 with a suction pump that fails above 18 braccia / 32 feet, dissolving to Evangelista Torricelli and 21-year-old Vincenzo Viviani inverting a 4-foot glass tube of mercury in 1644).",
             STYLE + "Split period scene: on the left in Florence in 1638, white-bearded Galileo Galilei inspects a tall wooden well pump with two baffled workmen; on the right in 1644, Evangelista Torricelli and young Vincenzo Viviani measure a 30-inch mercury column in a glass tube." + QUAL_TAIL,
             {"kind": "WHO", "label": "Vincenzo Viviani (1622–1703) — Italian mathematician", "fact_card": "Straws push, never suck", "when_stamp": "1638 · 11 June 1644", "timeline_step": "1/6 · 1638 (Galileo records the 18-braccia / 32-foot suction-pump limit in Florence)", "hold_s": 3.8}),
            ("02_florentine_18_braccia_32ft_pump_limit_vs_1_25_braccia_30in_mercury_diagram", 79.5, 8.0, "E", False, "18 BRACCIA (32 FT / 10.3 M) WATER PUMP LIMIT VS 1.25 BRACCIA (30 IN / 760 MM) MERCURY TUBE", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked pump-and-barometer diagram shows a Florentine suction pump failing above 18 braccia (32 feet / 10.3 m of water) beside Torricelli and Viviani's 1644 mercury tube stopping at 1.25 braccia (30 inches / 760 mm of mercury) with a Torricellian vacuum above.",
             {"kind": "DATA", "label": "1638 PUMP LIMIT (18 BRACCIA = 32 FT WATER) VS 1644 BAROMETER (1.25 BRACCIA = 30 IN MERCURY)", "detail": "Inked pump-and-barometer diagram on period paper showing a Florentine suction pump failing above 18 braccia (32 feet / 10.3 m of water) beside Torricelli & Viviani's 1644 mercury tube stopping at 1.25 braccia (30 inches / 760 mm of mercury) with a vacuum above", "scale": "if you tried to sip water through a vertical straw thirty-five feet tall, even the strongest vacuum pump on Earth could never lift the water to your lips", "hold_s": 3.8}),
            ("03_wooden_suction_pump_cutaway_piston_and_water_column_closeup", 87.5, 6.5, "B", False, "18 BRACCIA — 32 FEET", "Fast",
             "Fast: daylight macro shot of a glass-fronted cutaway model of a seventeenth-century wooden suction pump showing the rising leather piston and the water column stopping cleanly below the top valve. Nothing emissive, no face.",
             STYLE + "In crisp daylight on a demonstration bench, a cutaway wooden pump barrel with a glass window shows a leather piston rising while the clear water column beneath it stops below a gap of empty space." + FAST_TAIL,
             None),
            ("04_torricellian_vacuum_top_of_glass_mercury_tube_and_letter_closeup", 94.0, 5.5, "C", False, "11 JUN 1644 — THE FIRST BAROMETER", "Fast",
             "Fast: daylight close-up of the clear empty Torricellian vacuum space at the sealed top of Torricelli's inverted glass mercury tube beside his 11 June 1644 letter to Michelangelo Ricci. Nothing emissive, no face.",
             STYLE + "In bright window light on a Florentine desk, the camera frames the sealed upper dome of a vertical glass tube where a gleaming silver mercury column stops cleanly below an empty space beside an inked parchment page." + FAST_TAIL,
             None),
        ],
    ),
    (
        3,
        "Part 03 — Blaise Pascal's Red-Wine Tube & the 19 September 1648 Puy-de-Dôme Climb — Midpoint Twist",
        [
            ("01_pascal_1646_rouen_wine_tube_and_perier_19_sep_1648_puy_de_dome_summit", 99.5, 6.5, "A", False, "TESTED WITH A 46-FOOT WINE TUBE", "Quality",
             "Quality: readable faces (23-year-old Blaise Pascal in Rouen in late 1646 watching a 46-foot glass tube of red wine lashed to a ship's mast, dissolving to his brother-in-law Florin Périer reading a mercury barometer on the rocky summit of Puy-de-Dôme on 19 September 1648).",
             STYLE + "Split period scene: on the left in a Rouen courtyard in 1646, young Blaise Pascal points up at a forty-six-foot glass tube filled with dark red wine lashed to a wooden mast; on the right on 19 September 1648, Florin Périer in a cloak kneels on the windy rocky summit of Puy-de-Dôme reading a mercury barometer." + QUAL_TAIL,
             {"kind": "WHO", "label": "Florin Périer (1605–1672) — French experimentalist", "fact_card": "Tested with a 46-foot wine tube", "when_stamp": "1646 · 15 November 1647 · 19 September 1648", "timeline_step": "3/6 · 19 Sep 1648 (Florin Périer's Puy-de-Dôme climb for Blaise Pascal proves air pressure drops with altitude)", "hold_s": 3.8}),
            ("02_puy_de_dome_19_sep_1648_711mm_valley_to_627mm_summit_84mm_drop_chart", 106.0, 8.0, "E", False, "19 SEP 1648 PUY-DE-DÔME: 711 MM (395 M VALLEY) → 627 MM (1,465 M SUMMIT) = −84 MM DROP", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked altitude-vs-pressure chart from Florin Périer's 19 September 1648 Puy-de-Dôme climb shows mercury falling from 711 mm (26 pouces 3.5 lignes) at the Clermont Minims monastery garden (~395 m elevation) to 627 mm (23 pouces 2 lignes) at the Puy-de-Dôme summit (1,465 m, a drop of 84 mm / 3 pouces 1.5 lignes across ~1,000 m of altitude).",
             {"kind": "DATA", "label": "19 SEP 1648 PUY-DE-DÔME: 711 MM (VALLEY, 395 M) TO 627 MM (SUMMIT, 1,465 M) = 84 MM DROP", "detail": "Inked altitude-vs-pressure chart on period paper from Florin Périer's 19 September 1648 Puy-de-Dôme climb showing mercury falling from 711 mm (26 pouces 3.5 lignes) at the Clermont monastery garden (~395 m elevation) to 627 mm (23 pouces 2 lignes) at the Puy-de-Dôme summit (1,465 m, a drop of 84 mm across ~1,000 m of altitude)", "scale": "climbing just one kilometre up the mountain left roughly ten percent of Earth's atmosphere below their boots — dropping the mercury column by the length of a human thumb", "hold_s": 3.8}),
            ("03_perier_and_witnesses_19_sep_1648_puy_de_dome_summit_measuring_3_inch_drop", 114.0, 6.5, "B", False, "PUY-DE-DÔME — 84 MM DROP", "Quality",
             "Quality: readable faces (on the summit of Puy-de-Dôme on 19 September 1648, Florin Périer and five witnesses measure the 84-millimetre drop in the mercury column in amazement).",
             STYLE + "On the rocky windswept summit of Puy-de-Dôme on 19 September 1648, Florin Périer and five French scholars in cloaks and wide-brimmed hats point in amazement at a wooden-framed glass barometer where the mercury column has dropped three inches." + QUAL_TAIL,
             None),
            ("04_two_barometers_comparison_valley_monastery_garden_vs_mountain_summit", 120.5, 5.5, "C", False, "1,000 METRES HIGHER", "Fast",
             "Fast: daylight close-up of two brass-scaled glass mercury barometers side by side on a wooden stand showing a higher 711 mm level marked for the valley garden and a lower 627 mm level marked for the mountain summit. Nothing emissive, no face.",
             STYLE + "In crisp daylight on a stone ledge, two brass-framed glass mercury tubes stand side by side in porcelain dishes, with the right-hand mercury column sitting three inches lower than the left." + FAST_TAIL,
             None),
        ],
    ),
    (
        4,
        "Part 04 — Otto von Guericke's 16 Horses & Robert Boyle's Silent Watch",
        [
            ("01_guericke_8_may_1654_regensburg_16_horses_and_boyle_1660_oxford_watch_vacuum", 126.0, 6.5, "A", False, "16 HORSES COULDN'T OPEN IT", "Quality",
             "Quality: readable faces (Magdeburg mayor Otto von Guericke on 8 May 1654 in Regensburg directing two teams of eight horses hitched to his 50-centimetre copper hemispheres before Emperor Ferdinand III, dissolving to Robert Boyle and Robert Hooke in Oxford in 1660 listening to a ticking watch fade to silence inside an evacuated glass globe).",
             STYLE + "Split period scene: on the left in Regensburg on 8 May 1654, Otto von Guericke in a velvet coat directs sixteen straining horses hitched to two copper hemispheres; on the right in Oxford in 1660, Robert Boyle and young Robert Hooke lean close to a large glass vacuum globe containing a suspended brass pocket watch." + QUAL_TAIL,
             {"kind": "WHO", "label": "Robert Boyle (1627–1691) — Anglo-Irish chemist", "fact_card": "16 horses couldn't open it", "when_stamp": "1650 · 8 May 1654 · 1660 · 1662", "timeline_step": "5/6 · 1660–1662 (Robert Boyle & Robert Hooke prove sound vanishes in a vacuum and formulate Boyle's Law)", "hold_s": 3.8}),
            ("02_guericke_50cm_hemispheres_2_tonnes_and_boyle_1662_j_tube_pv_chart", 132.5, 8.0, "E", False, "50 CM HEMISPHERES (~20,000 N = 2 TONNES FORCE) & BOYLE'S 1662 J-TUBE (P × V = CONSTANT)", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked force-and-volume diagram shows Otto von Guericke's 50 cm Magdeburg hemispheres clamped by ~20,000 N (~2 tonnes) of outside air pressure alongside Robert Boyle's 1662 J-tube showing trapped air volume halving when mercury pressure doubles (29.75 → 59.5 inches Hg, P × V = constant).",
             {"kind": "DATA", "label": "50 CM MAGDEBURG HEMISPHERES (~2 TONNES FORCE) & BOYLE'S 1662 J-TUBE (P × V = CONSTANT)", "detail": "Inked force-and-volume diagram on period paper showing Otto von Guericke's 50 cm Magdeburg hemispheres clamped by ~20,000 N (~2 tonnes) of outside air pressure alongside Robert Boyle's 1662 J-tube showing gas volume halving when mercury pressure doubles (29.75 → 59.5 inches Hg, P × V = constant)", "scale": "on a fifty-centimetre copper sphere, the ordinary air of a spring afternoon clamps the two halves together with two tonnes of force — the weight of a full-grown rhinoceros sitting on the seam", "hold_s": 3.8}),
            ("03_guericke_copper_hemispheres_brass_stopcock_valve_opening_closeup", 140.5, 6.5, "B", False, "8 MAY 1654 — TWO TONNES OF AIR", "Fast",
             "Fast: daylight close-up of the two 50-centimetre copper Magdeburg hemispheres suspended from heavy iron rings as the small brass stopcock valve is turned and the two unbolted copper bowls separate cleanly. Nothing emissive, no face.",
             STYLE + "In bright courtyard daylight, a close-up shows two heavy copper hemispheres sealed on a leather ring with a brass stopcock valve turning open as the two copper halves part cleanly." + FAST_TAIL,
             None),
            ("04_explorer_bell_jar_vacuum_pump_silencing_brass_pocket_watch", 147.0, 5.5, "B", True, None, "Quality",
             "Quality: Explorer beat 2 (locked character reference).",
             STYLE + "Cranking a miniature wooden vacuum pump connected to a clear glass bell jar where a brass pocket watch hangs on a silk thread, the Explorer cups a hand to one ear as the rippling sound rings around the watch fade away while the watch hands keep spinning." + EXP_TAIL,
             None),
        ],
    ),
    (
        5,
        "Part 05 — How the Vacuum Built the Steam Engine & the Scientist Who Found Poison in Every Breath of Air",
        [
            ("01_timeline_1638_1712_and_newcomen_atmospheric_vacuum_engine_5_tonnes_chart", 152.5, 8.5, "E", False, "1638–1712 TIMELINE · NEWCOMEN 1712 VACUUM ENGINE (>5 TONNES DOWN-STROKE AT 12 STROKES/MIN)", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, the 6-date timeline completes: 1638 (Galileo records the 32-foot suction-pump limit in Florence) · Jun 1644 (Evangelista Torricelli & Vincenzo Viviani create the 30-inch mercury barometer and first sustained vacuum) · 19 Sep 1648 (Florin Périer's Puy-de-Dôme mountain climb for Blaise Pascal proves air pressure drops with altitude) · 8 May 1654 (Otto von Guericke's 16-horse Magdeburg hemispheres demonstration at Regensburg) · 1660–1662 (Robert Boyle & Robert Hooke prove sound vanishes in a vacuum and formulate Boyle's Law) · 1712 (Thomas Newcomen's atmospheric vacuum engine launches the Industrial Revolution), alongside Newcomen's 21-inch cylinder where cold water condenses steam into a vacuum so 14.7 psi outside air slams the piston down with >5 tonnes of force.",
             {"kind": "DATA", "label": "1638–1712 TIMELINE & NEWCOMEN 1712 ATMOSPHERIC ENGINE (21-IN BORE, >5 TONNES AIR FORCE)", "detail": "Animated 6-date timeline (1638 → 1712) alongside Thomas Newcomen's 1712 atmospheric engine cylinder (21-inch bore, 14.7 psi outside air driving the piston down with >5 tonnes of force at 12 strokes per minute)", "scale": "when cold water condensed the steam inside Newcomen's cylinder, the outside atmosphere slammed the piston down with over five tonnes of force twelve times a minute", "who_card": "Thomas Newcomen (1664–1729) — English engineer", "fact_card": "Steam engines ran on air weight", "when_stamp": "1690 · 1712 · 1638–1712", "timeline_step": "6/6 · 1712 (Thomas Newcomen's atmospheric vacuum engine launches the Industrial Revolution)", "hold_s": 3.8}),
            ("02_newcomen_1712_atmospheric_engine_beam_and_condensing_cylinder_model", 161.0, 5.5, "A", False, "PUSHED BY THE OCEAN OF AIR", "Fast",
             "Fast: daylight cutaway tabletop model of Thomas Newcomen's 1712 atmospheric beam engine showing a cold-water jet condensing steam inside the brass cylinder while outside air pushes the piston down and rocks the heavy oak beam. Nothing emissive, no face.",
             STYLE + "In crisp daylight on an engineering bench, a brass-and-oak cutaway model of a Newcomen atmospheric beam engine shows a piston descending inside a vertical brass cylinder as the overhead wooden beam rocks smoothly." + FAST_TAIL,
             None),
            ("03_rutherford_1904_pitchblende_and_patterson_1953_clean_lab_greenland_handoff", 166.5, 6.5, "C", False, "THE METEORITE AND THE POISON", "Quality",
             "Quality: readable faces (Ernest Rutherford on 20 May 1904 at the Royal Institution in London holding up a black lump of pitchblende before Lord Kelvin, beside Clair Patterson in his 1953 acid-scrubbed ultra-clean room at Caltech and 1965 Greenland snow trench — handoff to 040 Earth Age & Lead).",
             STYLE + "Split period scene: on the left in London on 20 May 1904, young Ernest Rutherford holds up a dark pitchblende stone before white-bearded Lord Kelvin in the front row; on the right in 1953, geochemist Clair Patterson in a white clean-room hood inspects a gleaming iron meteorite fragment beside a quartz flask." + QUAL_TAIL,
             {"kind": "WHEN", "label": "20 MAY 1904 · 1953 · 1965", "hold_s": 3.5}),
            ("04_table_three_callback", 173.0, 2.4, "C", False, None, "reuse",
             "Reuse: verified unused moving window [5.50s..7.90s] of P1:07_table_three_props_suction_pump_cylinder_mercury_barometer_copper_hemispheres (callback, £0).",
             "Reuse P1:07_table_three_props_suction_pump_cylinder_mercury_barometer_copper_hemispheres [5.50s..7.90s] (2.40s distinct non-overlapping tail window from 8.00s source clip).",
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
                row["reuse_of"] = "P1:07_table_three_props_suction_pump_cylinder_mercury_barometer_copper_hemispheres"
                row["reuse_window_s"] = [5.5, 7.9]
                row["reuse_audit"] = {
                    "source_row": "P1:07_table_three_props_suction_pump_cylinder_mercury_barometer_copper_hemispheres",
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
            "film": "039_Torricelli-Pascal-Guericke-Barometer-Vacuum",
            "part": p_idx,
            "title": p_title,
            "version": "v01",
            "timing_status": "pre_vo_script_clock (built from barometer_script_master_v01.md; retimes onto Scribe STT once VO locks)",
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
        "film": "039_Torricelli-Pascal-Guericke-Barometer-Vacuum",
        "version": "v01",
        "date": "2026-10-18",
        "owner": "gemini (J0524)",
        "status": "PRE_VO_BOARDS_V01_NO_MINT",
        "generation_authorized": False,
        "script": "00_Brand/Channel-Setup/ideas/039_Torricelli-Pascal-Guericke-Barometer-Vacuum/barometer_script_master_v01.md",
        "sources": "00_Brand/Channel-Setup/ideas/039_Torricelli-Pascal-Guericke-Barometer-Vacuum/SOURCES_v01.md",
        "credit_snapshot": {
            "flow_balance": 23740,
            "flow_floor": 0,
            "flow_read_at": "2026-10-15T21:42:22Z",
            "vertex_promo_gbp": 71.02,
            "vertex_usable_gbp": 70.02,
        },
        "totals": totals,
        "per_part": per_part_summary,
        "mint_order": "006 > 007 > 008 > 009 > 010 > 011 > 012 > 013 > 014 > 015 > 016 > 017 > 018 > 019 > 020 > 021 > 022 > 023 > 024 > 025 > 026 > 027 > 028 > 029 > 030 > 031 > 032 > 033 > 034 > 035 > 036 > 037 > 038 > 039. Nothing in 039 is generation_authorized.",
    }
    (EDIT / "PICTURE_PLAN_v01.json").write_text(json.dumps(plan, indent=2) + "\n")

    sl = [
        "# 039 Atmospheric Pressure: Why 16 Horses Couldn't Pull Two Bowls Apart — Shot list & plate boards v01 (pre-VO)",
        "",
        "Gemini, 18 Oct 2026, J0524. Built from `barometer_script_master_v01.md` (`93.8 PASS`) and `SOURCES_v01.md`.",
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
        "# 039 price review v01 (pre-VO plate boards)",
        "",
        "Gemini, 18 Oct 2026, J0524. Boards only. **No mint. No spend. No merge.**",
        "Prepared from `barometer_script_master_v01.md` (`93.8 PASS`) and `SOURCES_v01.md` so 039's full plate board rows, non-emissive Fast prompts, £0 code graphics, and Teach-on-Screen overlays are ready to re-time the moment long VO locks. Parked for Chief.",
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
        f"- **Quality ({totals['Quality']} rows):** readable faces (Evangelista Torricelli, Vincenzo Viviani, Galileo Galilei, Blaise Pascal, Florin Périer, Otto von Guericke, Robert Boyle, Ernest Rutherford, Lord Kelvin, Clair Patterson), 1654 Regensburg 16-horse courtyard demonstration, 1648 Puy-de-Dôme summit witnesses, and the 2 Explorer beats.",
        f"- **Fast ({totals['Fast']} rows, non-emissive):** daylight prop and laboratory shots (porcelain mercury basin & brass calipers pan, 3-object callback bench, cutaway wooden suction-pump cylinder, Torricellian vacuum at the top of the glass mercury tube, valley vs mountain barometer tubes side by side, copper Magdeburg hemispheres stopcock valve opening, Newcomen 1712 atmospheric beam engine model). Zero candles, flames, sparks, or glowing elements on Fast.",
        f"- **£0 code graphics ({totals['code_graphic']} rows):**",
        "  1. `P1:04_water_32ft_vs_mercury_30in_hydrostatic_balance_101kpa_chart` — 10.3 m (32 ft) of water (1.0 g/cm³) vs 760 mm (30 in) of liquid mercury (13.6 g/cm³), both exerting 101.3 kPa (14.7 psi) at sea level (`SCALE: because liquid mercury is nearly fourteen times heavier than water, a thirty-inch tube of mercury on your desk weighs the exact same per square inch as a thirty-two-foot tower of water three storeys high`)",
        "  2. `P1:06_atmospheric_load_14_7_psi_10_tonnes_on_human_body_scale_bar` — 14.7 lb/in² (1.03 kg/cm² = 101,325 Pa) summing to ~10,000 kg (10 metric tonnes) over the ~1.7 m² surface area of an adult body (`SCALE: the air pressing inward on your skin right now weighs around ten tonnes — as heavy as a double-decker London bus, balanced only because the fluids inside your body push back out with the exact same force`)",
        "  3. `P2:02_florentine_18_braccia_32ft_pump_limit_vs_1_25_braccia_30in_mercury_diagram` — Florentine suction pump failing above 18 braccia (32 ft / 10.3 m of water) beside Torricelli & Viviani's 1644 mercury tube stopping at 1.25 braccia (30 in / 760 mm) (`SCALE: if you tried to sip water through a vertical straw thirty-five feet tall, even the strongest vacuum pump on Earth could never lift the water to your lips`)",
        "  4. `P3:02_puy_de_dome_19_sep_1648_711mm_valley_to_627mm_summit_84mm_drop_chart` — Florin Périer's 19 September 1648 Puy-de-Dôme climb showing mercury falling from 711 mm (26 pouces 3.5 lignes at 395 m) to 627 mm (23 pouces 2 lignes at 1,465 m, an 84 mm drop across ~1,000 m) (`SCALE: climbing just one kilometre up the mountain left roughly ten percent of Earth's atmosphere below their boots — dropping the mercury column by the length of a human thumb`)",
        "  5. `P4:02_guericke_50cm_hemispheres_2_tonnes_and_boyle_1662_j_tube_pv_chart` — Otto von Guericke's 50 cm Magdeburg hemispheres clamped by ~20,000 N (~2 tonnes) of outside air pressure alongside Robert Boyle's 1662 J-tube (`P × V = constant`) (`SCALE: on a fifty-centimetre copper sphere, the ordinary air of a spring afternoon clamps the two halves together with two tonnes of force — the weight of a full-grown rhinoceros sitting on the seam`)",
        "  6. `P5:01_timeline_1638_1712_and_newcomen_atmospheric_vacuum_engine_5_tonnes_chart` — completed 6-date timeline (1638 → 1712) + Thomas Newcomen's 1712 atmospheric engine cylinder (21-inch bore, >5 tonnes down-stroke at 12 strokes/min) (`SCALE: when cold water condensed the steam inside Newcomen's cylinder, the outside atmosphere slammed the piston down with over five tonnes of force twelve times a minute`)",
        f"- **£0 verified reuse ({totals['reuse']} row):** `P5:04_table_three_callback` uses the 2.40 s unused moving tail `[5.50s..7.90s]` of `P1:07_table_three_props_suction_pump_cylinder_mercury_barometer_copper_hemispheres`.",
        "",
        "## Mint order",
        "",
        "006 > 007 > 008 > 009 > 010 > 011 > 012 > 013 > 014 > 015 > 016 > 017 > 018 > 019 > 020 > 021 > 022 > 023 > 024 > 025 > 026 > 027 > 028 > 029 > 030 > 031 > 032 > 033 > 034 > 035 > 036 > 037 > 038 > 039. `generation_authorized` is `false` on every row.",
    ])
    (EDIT / "PRICE_REVIEW_v01.md").write_text("\n".join(pr_lines) + "\n")
    print(f"039 v01 boards written: {totals['rows']} rows, Flow expected={totals['flow_credits_expected']}")


if __name__ == "__main__":
    main()
