#!/usr/bin/env python3
"""HOS 089 (The Waggle Dance: How a Robot Bee Proved Bees Can Talk) pre-VO plate boards v01. J0805. No mint, no spend.

Built from 00_Brand/Channel-Setup/ideas/089_Frisch-Lindauer-Michelsen-Honeybee-Waggle-Dance-Robot-Bee/waggle_dance_script_master_v01.md
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
        "Part 01 — The Sugar Dish Behind the Hill, the Glass Hive & the 1989 Mechanical Robot Bee",
        [
            ("01_vertical_honeycomb_60_deg_waggle_dance_and_von_frisch_1945_brunnwinkl_michelsen_1989_robot_bee", 0.0, 5.5, "A", False, "THE WAGGLE DANCE & ROBOT BEE", "Quality",
             "Quality: Short frame 0 / answer image (0:03) + side by side, inside a vertical honeycomb a paint-numbered honeybee performs a figure-eight waggle dance tilted 60 degrees to the right of straight up matching the 60-degree angle between the Sun and a distant meadow of flowers outside, beside Austrian biologist Karl von Frisch at Brunnwinkl in Summer 1945 timing the dance through a glass observation hive with a stopwatch and protractor and Danish biophysicist Axel Michelsen in 1989 operating a wax-coated brass mechanical robot bee with a vibrating razor-blade wing.",
             STYLE + "Split entomological-and-historical scene: on the left, a paint-dotted honeybee dances a figure-eight waggle run tilted 60 degrees from vertical on a honeycomb while outside the Sun shines 60 degrees from a flower meadow; on the right, Karl von Frisch in 1945 Austria observes through a glass hive beside Axel Michelsen in 1989 guiding a miniature brass-and-wax robot bee." + QUAL_TAIL,
             {"kind": "WHEN", "label": "BRUNNWINKL, AUSTRIA, SUMMER 1945", "timeline_step": "1/3 · 1914 & Summer 1944–1946 (Karl von Frisch in Munich and Brunnwinkl proves honeybees see colour and ultraviolet light, then uses paint-numbered bees in a glass hive to decode the figure-eight waggle dance sun-to-gravity code)", "hold_s": 3.5}),
            ("02_von_frisch_1914_1946_painted_bees_lindauer_1951_swarm_vote_and_michelsen_1989_robot_bee_split", 5.5, 6.0, "B", False, "PAINTED BEES, SWARM VOTE, ROBOT BEE", "Quality",
             "Quality: complex three-part composition (Karl von Frisch in Munich and Brunnwinkl in 1914–1946 dabbing paint onto numbered honeybees and decoding the figure-eight waggle dance; Martin Lindauer in Munich in 1951–1955 mapping house-hunting scout bees voting on a swarm; and Axel Michelsen, Wolfgang Kirchner, and Martin Lindauer in Odense and Würzburg in 1989 programming a computer-controlled robot bee to recruit real foragers).",
             STYLE + "Three-panel period composition: on the left in 1945 Brunnwinkl, Karl von Frisch dabs coloured paint onto feeding honeybees; in the centre in 1951 Munich, Martin Lindauer maps waggle dances on a hanging bee swarm; on the right in 1989 Würzburg, Axel Michelsen and Wolfgang Kirchner operate their computer-driven brass robot bee inside a hive." + QUAL_TAIL,
             None),
            ("03_red_dotted_scout_bee_held_in_hive_while_recruited_sisters_fly_2km_over_hill_to_exact_dish", 11.5, 6.0, "C", False, "NO GUIDE, EXACT GPS", "Quality",
             "Quality: complex behavioural reveal (a split comparison of a lone red-dotted scout bee returning from a sugar dish 2 km away, dancing on the dark vertical comb, and then being held inside a small mesh cage in the hive while dozens of recruited sister bees fly straight out across a hill to the exact dish without a guide).",
             STYLE + "In a split landscape-and-hive comparison, on the left a paint-marked scout bee finishes her figure-eight dance inside the hive while on the right dozens of recruited honeybees fly straight over a green hillside to land on a glass dish of sugar water." + QUAL_TAIL,
             {"kind": "WHEN", "label": "1914 · 1944 · 1946 · 1949 · 1951 · 1989", "timeline_step": "1/3 · 1914 & 1944–1946 (von Frisch waggle code) · 2/3 · 1949 & 1951–1955 (polarized sky & Lindauer swarm democracy) · 3/3 · June 1989 (Michelsen robot bee)", "hold_s": 3.5}),
            ("04_von_frisch_1946_sun_to_gravity_angle_code_1s_per_km_and_michelsen_1989_robot_bee_chart", 17.5, 8.0, "E", False, "VON FRISCH (1946): STRAIGHT UP = SUN ANGLE & ~1 S WAGGLE ≈ 1 KM DISTANCE", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked Honeybee Waggle Dance Sun-to-Gravity Vector Code, Polarized-Light Compass & 1989 Robot Bee Recruitment chart from Karl von Frisch (1914 Zool. Jahrb., 1946 Experientia 2: 397–405 & 1949 Experientia 5: 142–148), Martin Lindauer (1955 Z. vergl. Physiol. 37: 263–324), and Axel Michelsen, Wolfgang Kirchner & Martin Lindauer (1989 Naturwissenschaften 76: 277–280) shows 1) Outside: angle alpha between the Sun and the food source; 2) Inside on the vertical dark comb: waggle run angled at that exact angle alpha relative to straight up (gravity), where ~1 second of waggling ≈ 1 km distance; and 3) Michelsen's 1989 brass-and-wax robot bee vibrating at 280 Hz recruiting real bees to targets 250–1,000 m away.",
             {"kind": "DATA", "label": "1946 KARL VON FRISCH (EXPERIENTIA 2: 397): SUN-TO-GRAVITY WAGGLE ANGLE & ~1 S ≈ 1,000 M DISTANCE CURVE", "detail": "Inked Karl von Frisch (1946 Experientia 2: 397–405) waggle dance angle (0° straight up = toward Sun; 60° right of vertical = 60° right of Sun; 180° straight down = away from Sun) & waggle-run duration vs distance curve (~1 second waggle run ≈ 1,000 metres flight distance) on period paper", "scale": "a honeybee's brain weighs just one milligram — a millionth of a kilogram, smaller than a single sesame seed — yet inside a pitch-black hive she converts the angle of the Sun in the sky into the pull of gravity under her feet with the precision of a compass", "who_cards": [
                 "Karl Ritter von Frisch (1886–1982) — Austrian ethologist and zoologist",
                 "Martin Lindauer (1918–2008) — German behavioral biologist",
                 "Axel Michelsen (born 1940) — Danish biophysicist",
                 "Wolfgang H. Kirchner (born 1959) — German behavioral biologist",
             ], "when_stamp": "1914 · 1944 · 1946 · 1949 · 1951 · 1989", "hold_s": 3.8}),
            ("05_von_frisch_five_colour_shellac_paint_jars_stopwatch_and_1946_experientia_paper_pan", 25.5, 5.5, "A", False, "THE SOLAR COMPASS IN THE DARK", "Fast",
             "Fast: daylight close-up pan across Karl von Frisch's five small jars of white, red, blue, yellow, and green shellac paint, fine artist brushes, a mechanical stopwatch, and his 1946 Experientia paper on an oak table. Nothing emissive, no face.",
             STYLE + "In warm window light on an oak table, five small glass jars of coloured shellac paint and fine brushes sit beside a mechanical pocket stopwatch, a brass protractor, and an open 1946 scientific journal." + FAST_TAIL,
             None),
            ("06_michelsen_kirchner_lindauer_1989_280hz_brass_robot_bee_and_polar_recruitment_accuracy_chart", 31.0, 8.0, "E", False, "ODENSE & WÜRZBURG, 1989", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period parchment, an inked Axel Michelsen, Wolfgang Kirchner & Martin Lindauer (1989 Naturwissenschaften 76: 277–280) Computer-Controlled Mechanical Robot Bee diagram shows the wax-coated brass body, the step-motor rotating the waggle angle, the electromagnetic driver vibrating the razor-blade wing at 280 Hz, and the directional flight distribution of real honeybees arriving at control vs target meadows.",
             {"kind": "DATA", "label": "1989 MICHELSEN, KIRCHNER & LINDAUER (NATURWISSENSCHAFTEN 76: 277): 280-HZ ROBOT BEE & >80% DIRECTIONAL RECRUITMENT CHART", "detail": "Inked Michelsen, Kirchner & Lindauer (1989) robot-bee directional and distance recruitment accuracy chart (over 80% of recruited bees arriving along the robot's programmed compass vector and distance) on period paper", "scale": "to make a single half-kilogram jar of honey, a hive's foragers have to visit two million flowers and fly nearly ninety thousand kilometres — more than twice around the Earth — which is why wasting energy searching blindly without the waggle dance would starve the colony", "hold_s": 3.8}),
            ("07_table_three_props_1914_blue_grey_card_grid_1945_glass_hive_protractor_and_1989_brass_robot_bee", 39.0, 5.5, "C", False, "1914 TO 1989", "Fast",
             "Fast: daylight pan across three period props on a wooden bench: von Frisch's 1914 blue-and-grey checkerboard colour-test cards, his 1945 glass-walled observation hive with a brass protractor, and Michelsen's 1989 beeswax-coated brass mechanical robot bee on its stepper-motor rod (also provides 2.40s tail window [5.50s..7.90s] for P5:04 callback). Nothing emissive, no face.",
             STYLE + "In soft daylight on a wooden bench, a checkerboard of grey cards with one blue square and a watch glass sit beside a wooden glass-walled observation hive with a brass protractor and a miniature brass-and-wax mechanical bee on a metal rod." + FAST_TAIL,
             None),
            ("08_explorer_rotating_60_deg_plumb_line_protractor_on_honeycomb_with_1989_brass_robot_bee", 62.0, 5.5, "A", True, None, "Quality",
             "Quality: Explorer beat 1 (locked character reference, after 1:00).",
             STYLE + "Standing beside a giant vertical honeycomb with a brass plumb-line hanging straight down, the Explorer rotates a brass protractor arm to 60 degrees right of vertical while a miniature beeswax-coated brass robot bee waggles along the 60-degree track and sends honeybees flying out the hive entrance." + EXP_TAIL,
             None),
            ("09_karl_von_frisch_summer_1945_brunnwinkl_painting_numbered_dots_on_honeybees_at_sugar_dish", 67.5, 5.5, "B", False, "BRUNNWINKL, SUMMER 1945", "Quality",
             "Quality: readable face (at Brunnwinkl, Austria in Summer 1945, Karl von Frisch dabs tiny coded dots of white, red, blue, yellow, and green shellac paint onto honeybees at a sugar dish so he can identify bee #1 to #599 inside his glass hive).",
             STYLE + "In a sunlit Austrian lakeside garden in Summer 1945, zoologist Karl von Frisch leans over a glass sugar-water dish with a fine paintbrush, gently touching a tiny dot of red and white paint onto a feeding honeybee's back." + QUAL_TAIL,
             {"kind": "WHEN", "label": "BRUNNWINKL, SUMMER 1945", "timeline_step": "1/3 · 1914 & Summer 1944–1946 (Karl von Frisch decodes honeybee colour vision and the figure-eight waggle dance in Brunnwinkl)", "hold_s": 3.5}),
        ],
    ),
    (
        2,
        "Part 02 — 1914–1923 & Summer 1944–1946: Karl von Frisch's Painted Bees, the Glass Hive & How Gravity Becomes the Sun",
        [
            ("01_carl_von_hess_1910_vs_karl_von_frisch_1914_blue_card_test_and_1945_brunnwinkl_waggle_dance", 73.0, 6.5, "A", False, "GRAVITY STANDS FOR THE SUN", "Quality",
             "Quality: readable faces (German ophthalmologist Carl von Hess in 1910 claiming invertebrates are colour-blind, answered by young Austrian zoologist Karl Ritter von Frisch in 1914 placing a blue card inside a checkerboard of 30 grey cards to prove honeybees see colour, and at Brunnwinkl in Summer 1944–1946 watching paint-numbered bees in a glass observation hive perform the figure-eight waggle dance).",
             STYLE + "Split period scene: on the left in 1914 Munich, Karl von Frisch watches honeybees land squarely on a single blue square among thirty shades of grey while Carl von Hess looks on; on the right in 1945 Brunnwinkl, von Frisch times a figure-eight waggle dance through his glass observation hive with a stopwatch." + QUAL_TAIL,
             {"kind": "FACT", "label": "Gravity stands for the Sun", "who_card": "Carl von Hess (1863–1923) — German ophthalmologist", "when_stamp": "1910 · 1914 · 1923 · Summer 1944 · Summer 1945 · 1946", "timeline_step": "1/3 · 1914 & Summer 1944–1946 (Karl von Frisch proves honeybee colour vision and decodes the figure-eight waggle dance sun-to-gravity transposition)", "hold_s": 3.8}),
            ("02_von_frisch_1914_colour_vision_grid_and_1946_experientia_sun_to_gravity_angle_distance_chart", 79.5, 8.0, "E", False, "1914 VON FRISCH (BLUE-IN-30-GREYS COLOUR PROOF) & 1946 VON FRISCH (EXPERIENTIA: SUN-TO-GRAVITY ANGLE & 100–6,000 M DISTANCE)", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked Karl von Frisch (1914 Zool. Jahrb. 35: 1–188) blue-card-in-30-greys colour vision proof alongside his (1946 Experientia 2: 397–405) figure-eight waggle dance sun-to-gravity angle transposition & waggle-duration-to-distance curve (100 m to 6,000 m).",
             {"kind": "DATA", "label": "1914 VON FRISCH (30-GREY COLOUR GRID) & 1946 VON FRISCH (EXPERIENTIA 2: 397) SUN-TO-GRAVITY WAGGLE CODE CHART", "detail": "Inked Karl von Frisch (1914 Zool. Jahrb. 35: 1–188) blue-card-in-30-greys colour vision proof alongside his (1946 Experientia 2: 397–405) figure-eight waggle dance sun-to-gravity angle transposition & waggle-duration-to-distance curve (100 m to 6,000 m) on period paper", "scale": "by dabbing five spots of coloured shellac paint onto a bee's back, Karl von Frisch could recognize bee number three hundred and forty-two at a glance among fifty thousand sisters — and watched her turn the pull of Earth's gravity into a solar map", "hold_s": 3.8}),
            ("03_brunnwinkl_1946_experientia_die_tanze_der_bienen_paper_paint_kit_and_glass_hive_closeup", 87.5, 6.5, "B", False, "1944–1946 — VON FRISCH'S WAGGLE CODE", "Fast",
             "Fast: daylight macro shot of Karl von Frisch's 1946 Experientia paper 'Die Tänze der Bienen' beside his five-jar shellac paint kit, numbered bee code card, and wooden glass observation hive on a bench. Nothing emissive, no face.",
             STYLE + "In crisp daylight on a field table, an open 1946 scientific journal showing figure-eight bee dance diagrams sits beside five small paint bottles, a pocket stopwatch, and a wooden glass-paned observation hive." + FAST_TAIL,
             None),
            ("04_mechanical_protractor_model_converting_solar_azimuth_angle_to_vertical_honeycomb_gravity_angle_pan", 94.0, 5.5, "C", False, "HOW STRAIGHT UP STANDS FOR THE SUN", "Fast",
             "Fast: daylight close-up pan across a brass-and-wood teaching model showing how a 60-degree horizontal angle between the Sun and a flower patch outside is transposed onto a 60-degree angle from vertical gravity on a honeycomb inside. Nothing emissive, no face.",
             STYLE + "In bright window light on an oak table, a brass-and-wood mechanical teaching model links an outdoor solar compass dial at 60 degrees to a vertical honeycomb dial tilted 60 degrees right of a hanging plumb-bob." + FAST_TAIL,
             None),
        ],
    ),
    (
        3,
        "Part 03 — 1949–1955: The Polarized-Sky Compass, the 15-Degree-per-Hour Clock & Martin Lindauer's Swarm Democracy — Midpoint Twist",
        [
            ("01_von_frisch_1949_polaroid_sky_compass_and_martin_lindauer_1951_1955_swarm_house_hunting_democracy", 99.5, 6.5, "A", False, "SWARMS VOTE BY WAGGLE DANCE", "Quality",
             "Quality: readable faces (Karl von Frisch in 1948–1949 holding a Polaroid sheet over an observation hive to prove honeybees read ultraviolet polarized skylight when the Sun is behind clouds, dissolving to his student Martin Lindauer in 1951–1955 tracking paint-numbered scout bees on a hanging honeybee swarm as they debate 20 candidate tree cavities by waggle dancing and shift their dance angle 15 degrees per hour in darkness).",
             STYLE + "Split period scene: on the left in 1949 Brunnwinkl, Karl von Frisch rotates a triangular Polaroid filter window over a horizontal honeycomb; on the right in 1951 Munich, Martin Lindauer takes notes beside a hanging honeybee swarm where paint-marked scout bees dance for competing nest sites." + QUAL_TAIL,
             {"kind": "FACT", "label": "Swarms vote by waggle dance", "when_stamp": "1948 · 1949 · 1951 · 1955 · 1973", "timeline_step": "2/3 · 1949 & 1951–1955 (Karl von Frisch discovers the bee's ultraviolet polarized-sky compass, and Martin Lindauer discovers time-compensated marathon dances and swarm house-hunting democracy)", "hold_s": 3.8}),
            ("02_von_frisch_1949_polaroid_sky_compass_and_lindauer_1955_swarm_20_sites_to_1_consensus_chart", 106.0, 8.0, "E", False, "1949 VON FRISCH (EXPERIENTIA: POLARIZED-SKY COMPASS) & 1955 MARTIN LINDAUER (20 NEST SITES → 1 UNANIMOUS SWARM CONSENSUS & 15°/HR CLOCK)", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked Karl von Frisch (1949 Experientia 5: 142–148) Polaroid-filter ultraviolet sky-polarization compass experiment & Martin Lindauer's (1955 Z. vergl. Physiol. 37: 263–324) 5-day swarm house-hunting consensus chart (20 candidate nest sites narrowing to 1 unanimous winner + 15 deg/hour time-compensated waggle angle shift).",
             {"kind": "DATA", "label": "1949 VON FRISCH (POLARIZED-SKY COMPASS) & 1955 LINDAUER (20 SITES → 1 SWARM CONSENSUS & 15°/HR CLOCK) CHART", "detail": "Inked Karl von Frisch (1949 Experientia 5: 142–148) Polaroid-filter ultraviolet sky-polarization compass experiment & Martin Lindauer's (1955 Z. vergl. Physiol. 37: 263–324) 5-day swarm house-hunting consensus chart (20 candidate nest sites narrowing to 1 unanimous winner + 15 deg/hour time-compensated waggle angle shift) on period paper", "scale": "a marathon scout bee dancing in a windowless room for four hours automatically rotates her waggle angle by sixty degrees — fifteen degrees every hour — tracking the moving Sun across the sky without ever peeking outside", "hold_s": 3.8}),
            ("03_munich_1949_polaroid_octagon_filter_and_lindauer_1955_swarm_house_hunting_maps_closeup", 114.0, 6.5, "B", False, "1949–1955 — POLARIZED SKY & SWARM DEMOCRACY", "Fast",
             "Fast: daylight macro shot of Karl von Frisch's 1949 octagonal Polaroid sky-filter viewer beside Martin Lindauer's 1955 Zeitschrift für vergleichende Physiologie swarm consensus maps on a wooden desk. Nothing emissive, no face.",
             STYLE + "In crisp daylight on a laboratory desk, an octagonal brass-framed polarizing filter wheel sits beside an open 1955 scientific journal showing vector fan maps of scout-bee nest votes." + FAST_TAIL,
             None),
            ("04_compound_eye_ommatidia_ultraviolet_polarization_analyzer_and_15_deg_hour_clock_gear_model_pan", 120.5, 5.5, "C", False, "READING POLARIZED BLUE SKY THROUGH ONE PATCH OF BLUE", "Fast",
             "Fast: daylight close-up pan across a sculpted anatomical model of a honeybee's compound eye dorsal rim ommatidia aligned with an ultraviolet polarization pattern dial and a 15-degree-per-hour clock gear on an oak table. Nothing emissive, no face.",
             STYLE + "In bright window light on an oak table, a painted anatomical model of a honeybee's compound eye facets sits beside a brass 15-degree-per-hour solar clock dial and a sky-polarization wheel." + FAST_TAIL,
             None),
        ],
    ),
    (
        4,
        "Part 04 — June 1989: The 20-Year Odor Controversy & How Axel Michelsen's Mechanical Robot Bee Proved the Dance Code",
        [
            ("01_james_gould_1975_ocelli_test_and_michelsen_kirchner_lindauer_june_1989_mechanical_robot_bee", 126.0, 6.5, "A", False, "ROBOT BEE SENT REAL BEES", "Quality",
             "Quality: readable faces (American ethologist James L. Gould at Princeton in 1975 covering dancers' ocelli eyes to misdirect recruits, dissolving to Danish biophysicist Axel Michelsen, Wolfgang H. Kirchner, and Martin Lindauer in June 1989 lowering a computer-controlled beeswax-coated brass mechanical robot bee with a 280-Hz vibrating razor-blade wing into a dark hive and recruiting real honeybees to programmed field targets).",
             STYLE + "Split period scene: on the left in 1975 Princeton, James Gould tests ocelli-masked honeybees in an observation hive; on the right in June 1989 Würzburg, Axel Michelsen, Wolfgang Kirchner, and Martin Lindauer watch real honeybees crowd around their computer-controlled brass-and-razor-blade mechanical robot bee." + QUAL_TAIL,
             {"kind": "FACT", "label": "Robot bee sent real bees", "who_cards": [
                 "Adrian M. Wenner (1928–2023) — American biologist",
                 "James L. Gould (born 1945) — American ethologist and evolutionary biologist",
             ], "when_stamp": "1967 · 1975 · June 1989", "timeline_step": "3/3 · June 1989 (Axel Michelsen, Wolfgang Kirchner, and Martin Lindauer build a computer-controlled brass-and-wax mechanical robot bee pulsing at 280 Hz that sends real honeybees to programmed field targets)", "hold_s": 3.8}),
            ("02_michelsen_kirchner_lindauer_june_1989_naturwissenschaften_robot_bee_280hz_and_polar_histogram_chart", 132.5, 8.0, "E", False, "JUNE 1989 MICHELSEN, KIRCHNER & LINDAUER (NATURWISSENSCHAFTEN): 280-HZ BRASS ROBOT BEE & 8-STATION RECRUITMENT HISTOGRAM", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked Axel Michelsen, Wolfgang Kirchner & Martin Lindauer (June 1989 Naturwissenschaften 76: 277–280) computer-controlled brass-and-razor-blade robot bee schematic (280-Hz wing vibration pulses + stepper-motor figure-eight waggle trajectory) & field capture polar histogram of recruited honeybees at 8 compass bait stations.",
             {"kind": "DATA", "label": "JUNE 1989 MICHELSEN, KIRCHNER & LINDAUER (NATURWISSENSCHAFTEN 76: 277): 280-HZ ROBOT BEE & 8-STATION POLAR HISTOGRAM", "detail": "Inked Axel Michelsen, Wolfgang Kirchner & Martin Lindauer (June 1989 Naturwissenschaften 76: 277–280) computer-controlled brass-and-razor-blade robot bee schematic (280-Hz wing vibration pulses + stepper-motor figure-eight waggle trajectory) & field capture polar histogram of recruited honeybees at 8 compass bait stations on period paper", "scale": "Axel Michelsen's robot bee was made from a scrap of brass tubing, a sliver of a shaving razor blade, and a coat of beeswax — yet when a computer made it waggle in the dark, living honeybees obeyed its directions and flew to an empty meadow a kilometre away", "hold_s": 3.8}),
            ("03_wurzburg_and_odense_june_1989_brass_razor_blade_robot_bee_stepper_motor_and_paper_closeup", 140.5, 6.5, "B", False, "JUNE 1989 — MICHELSEN'S ROBOT BEE", "Fast",
             "Fast: daylight macro shot of the June 1989 beeswax-coated brass mechanical robot bee with its single razor-blade wing mounted on its stepper-motor rod beside the June 1989 Naturwissenschaften paper on a laboratory bench. Nothing emissive, no face.",
             STYLE + "In crisp daylight on a 1989 biophysics bench, a miniature beeswax-coated brass mechanical bee with a thin steel razor-blade wing mounted on a stepper-motor shaft sits beside an open 1989 scientific journal." + FAST_TAIL,
             None),
            ("04_explorer_holding_bee_antenna_model_to_280hz_vibrating_razor_blade_wing_of_1989_brass_robot_bee", 147.0, 5.5, "B", True, None, "Quality",
             "Quality: Explorer beat 2 (locked character reference).",
             STYLE + "Standing beside the beeswax-coated brass mechanical robot bee on a vertical honeycomb, the Explorer holds a sculpted model of a honeybee antenna with Johnston's organ close to the vibrating razor-blade wing as acoustic air-particle ripples travel into the antenna joint." + EXP_TAIL,
             None),
        ],
    ),
    (
        5,
        "Part 05 — The Sesame-Seed GPS — & How Horse Blood and Pit-Viper Venom Saved Millions of Lives",
        [
            ("01_timeline_1914_1989_and_colour_vision_waggle_dance_polarized_compass_swarm_democracy_robot_bee_chart", 152.5, 8.5, "E", False, "1914–1989 TIMELINE · VON FRISCH WAGGLE DANCE & POLARIZED COMPASS, LINDAUER SWARM DEMOCRACY & MICHELSEN ROBOT BEE", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, the 3-era timeline completes: 1914 & Summer 1944–1946 (Karl von Frisch in Munich and Brunnwinkl proves honeybees see colour and ultraviolet light, then uses paint-numbered bees in a glass hive to decode the figure-eight waggle dance sun-to-gravity code) · 1949 & 1951–1955 (Karl von Frisch discovers the bee's ultraviolet polarized-sky compass, and Martin Lindauer discovers time-compensated marathon dances and swarm house-hunting democracy) · June 1989 (Axel Michelsen, Wolfgang Kirchner, and Martin Lindauer build a computer-controlled brass-and-wax mechanical robot bee pulsing at 280 Hz that sends real honeybees to programmed field targets).",
             {"kind": "DATA", "label": "1914–1989 HONEYBEE WAGGLE DANCE & ROBOT BEE TIMELINE · VON FRISCH, LINDAUER, GOULD, MICHELSEN & KIRCHNER", "detail": "Animated timeline (1914 → 1989) alongside an inked summary of honeybee colour vision, the sun-to-gravity waggle code, polarized-sky navigation, swarm democracy, and the 1989 mechanical robot bee", "scale": "from five dots of shellac paint on an Austrian lakeside to a vibrating razor-blade robot in a dark hive, scientists proved that the smallest brains in your garden speak a mathematical language of the Sun", "when_stamp": "1914–1989", "timeline_step": "3/3 · 1914–1989 timeline complete", "hold_s": 3.8}),
            ("02_glass_observation_hive_and_brass_robot_bee_beside_viper_fang_model_and_antivenom_vial_on_plinth_pan", 161.0, 5.5, "A", False, "SUN, GRAVITY & THE WAGGLE DANCE", "Fast",
             "Fast: daylight close-up of a wooden glass-walled observation hive and brass mechanical robot bee beside a sculpted hollow viper fang and an 1894 Pasteur Institute antivenom serum bottle on a wooden museum plinth. Nothing emissive, no face.",
             STYLE + "In crisp daylight on a wooden museum plinth, a glass observation hive and miniature brass robot bee sit beside a sculpted hollow viper fang model, a glass wine goblet, and a vintage serum vial." + FAST_TAIL,
             None),
            ("03_francesco_redi_1664_viper_wineglass_albert_calmette_1894_horse_antivenom_and_ferreira_1965_captopril_handoff", 166.5, 6.5, "C", False, "VIPER FANG, HORSE ANTIVENOM & CAPTOPRIL", "Quality",
             "Quality: readable faces (Francesco Redi at the Medici Court in Florence in 1664 watching Jacopo Sozzi drink viper venom in wine beside a dissected hollow viper fang, Albert Calmette and Césaire Phisalix in Paris on 10 February 1894 presenting horse-serum antivenom, and Sérgio Ferreira, David Cushman, and Miguel Ondetti in 1965–1975 turning Bothrops jararaca pit-viper venom into the blood-pressure pill Captopril — handoff to 090 Snake Venom, Antivenom & Captopril).",
             STYLE + "Split period scene: on the left in 1664 Florence, court physician Francesco Redi examines a hollow viper fang while Jacopo Sozzi raises a goblet of wine; on the right in 1894–1975, Albert Calmette holds a horse-serum antivenom vial beside Sérgio Ferreira and David Cushman with a Bothrops jararaca viper peptide model." + QUAL_TAIL,
             {"kind": "WHEN", "label": "1664 · 10 FEBRUARY 1894 · 1965 · 1975", "hold_s": 3.5}),
            ("04_table_three_callback", 173.0, 2.4, "C", False, None, "reuse",
             "Reuse: verified unused moving window [5.50s..7.90s] of P1:07_table_three_props_1914_blue_grey_card_grid_1945_glass_hive_protractor_and_1989_brass_robot_bee (callback, £0).",
             "Reuse P1:07_table_three_props_1914_blue_grey_card_grid_1945_glass_hive_protractor_and_1989_brass_robot_bee [5.50s..7.90s] (2.40s distinct non-overlapping tail window from 8.00s source clip).",
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
                row["reuse_of"] = "P1:07_table_three_props_1914_blue_grey_card_grid_1945_glass_hive_protractor_and_1989_brass_robot_bee"
                row["reuse_window_s"] = [5.5, 7.9]
                row["reuse_audit"] = {
                    "source_row": "P1:07_table_three_props_1914_blue_grey_card_grid_1945_glass_hive_protractor_and_1989_brass_robot_bee",
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
            "film": "089_Frisch-Lindauer-Michelsen-Honeybee-Waggle-Dance-Robot-Bee",
            "part": p_idx,
            "title": p_title,
            "version": "v01",
            "timing_status": "pre_vo_script_clock (built from waggle_dance_script_master_v01.md; retimes onto Scribe STT once VO locks)",
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
        "film": "089_Frisch-Lindauer-Michelsen-Honeybee-Waggle-Dance-Robot-Bee",
        "version": "v01",
        "date": "2026-10-21",
        "owner": "gemini (J0805)",
        "status": "PRE_VO_BOARDS_V01_NO_MINT",
        "generation_authorized": False,
        "script": "00_Brand/Channel-Setup/ideas/089_Frisch-Lindauer-Michelsen-Honeybee-Waggle-Dance-Robot-Bee/waggle_dance_script_master_v01.md",
        "sources": "00_Brand/Channel-Setup/ideas/089_Frisch-Lindauer-Michelsen-Honeybee-Waggle-Dance-Robot-Bee/SOURCES_v01.md",
        "credit_snapshot": {
            "flow_balance": 23740,
            "flow_floor": 0,
            "flow_read_at": "2026-10-15T21:42:22Z",
            "vertex_promo_gbp": 71.02,
            "vertex_usable_gbp": 70.02,
        },
        "totals": totals,
        "per_part": per_part_summary,
        "mint_order": "006 > 007 > 008 > 009 > 010 > 011 > 012 > 013 > 014 > 015 > 016 > 017 > 018 > 019 > 020 > 021 > 022 > 023 > 024 > 025 > 026 > 027 > 028 > 029 > 030 > 031 > 032 > 033 > 034 > 035 > 036 > 037 > 038 > 039 > 040 > 041 > 042 > 043 > 044 > 045 > 046 > 047 > 048 > 049 > 050 > 051 > 052 > 053 > 054 > 055 > 056 > 057 > 058 > 059 > 060 > 061 > 062 > 063 > 064 > 065 > 066 > 067 > 068 > 069 > 070 > 071 > 072 > 073 > 074 > 075 > 076 > 077 > 078 > 079 > 080 > 081 > 082 > 083 > 084 > 085 > 086 > 087 > 088 > 089 > 090 > 091 > 092 > 093 > 094 > 095. Nothing in 089 is generation_authorized.",
    }
    (EDIT / "PICTURE_PLAN_v01.json").write_text(json.dumps(plan, indent=2) + "\n")

    sl = [
        "# 089 The Waggle Dance: How a Robot Bee Proved Bees Can Talk — Shot list & plate boards v01 (pre-VO)",
        "",
        "Gemini, 21 Oct 2026, J0805. Built from `waggle_dance_script_master_v01.md` (`92.3/100 PASS`) and `SOURCES_v01.md`.",
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
        "# 089 price review v01 (pre-VO plate boards)",
        "",
        "Gemini, 21 Oct 2026, J0805. Boards only. **No mint. No spend. No merge.**",
        "Prepared from `waggle_dance_script_master_v01.md` (`92.3/100 PASS`) and `SOURCES_v01.md` so 089's full plate board rows, non-emissive Fast prompts, £0 code graphics, and Teach-on-Screen overlays are ready to re-time the moment long VO locks. Parked for Chief.",
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
        f"- **Quality ({totals['Quality']} rows):** readable faces (Karl Ritter von Frisch, Carl von Hess, Martin Lindauer, James L. Gould, Axel Michelsen, Wolfgang H. Kirchner, Francesco Redi, Albert Calmette, Sérgio Henrique Ferreira, David W. Cushman), 1914 Munich colour-card proof & Summer 1945 Brunnwinkl glass observation hive `waggle dance` decoding, 1949 polarized-sky compass & 1951–1955 swarm house-hunting democracy, June 1989 computer-controlled `280-Hz` brass-and-wax `mechanical robot bee`, and the 2 Explorer beats.",
        f"- **Fast ({totals['Fast']} rows, non-emissive):** daylight prop and laboratory shots (von Frisch's 5-colour shellac paint jars, stopwatch & 1946 *Experientia* paper pan, 3-object callback bench, 1946 *Experientia* paper with paint kit & glass observation hive, brass-and-wood solar azimuth to honeycomb gravity-angle teaching model, 1949 octagonal Polaroid sky filter with Lindauer's 1955 swarm maps, compound eye dorsal-rim polarization model with `15°/hour` solar clock dial, June 1989 beeswax-coated brass robot bee on stepper-motor rod with *Naturwissenschaften* paper, glass hive & robot bee beside hollow viper fang model & 1894 antivenom vial on museum plinth). Zero candles, flames, sparks, or glowing elements on Fast.",
        f"- **£0 code graphics ({totals['code_graphic']} rows):**",
        "  1. `P1:04_von_frisch_1946_sun_to_gravity_angle_code_1s_per_km_and_michelsen_1989_robot_bee_chart` — Karl von Frisch (1946 *Experientia* 2: 397–405) sun-to-gravity waggle angle (`0°` straight up = toward Sun; `60°` right = `60°` right of Sun) & `~1 s ≈ 1,000 m` distance curve (`SCALE: a honeybee's brain weighs just one milligram — a millionth of a kilogram, smaller than a single sesame seed — yet inside a pitch-black hive she converts the angle of the Sun in the sky into the pull of gravity under her feet with the precision of a compass`)",
        "  2. `P1:06_michelsen_kirchner_lindauer_1989_280hz_brass_robot_bee_and_polar_recruitment_accuracy_chart` — Axel Michelsen, Wolfgang Kirchner & Martin Lindauer (1989 *Naturwissenschaften* 76: 277–280) `280-Hz` mechanical robot bee & `>80%` directional recruitment chart (`SCALE: to make a single half-kilogram jar of honey, a hive's foragers have to visit two million flowers and fly nearly ninety thousand kilometres — more than twice around the Earth — which is why wasting energy searching blindly without the waggle dance would starve the colony`)",
        "  3. `P2:02_von_frisch_1914_colour_vision_grid_and_1946_experientia_sun_to_gravity_angle_distance_chart` — Karl von Frisch (1914 *Zool. Jahrb.* 35: 1–188) blue-card-in-30-greys colour vision proof & (1946 *Experientia*) waggle angle and `100–6,000 m` distance curve (`SCALE: by dabbing five spots of coloured shellac paint onto a bee's back, Karl von Frisch could recognize bee number three hundred and forty-two at a glance among fifty thousand sisters — and watched her turn the pull of Earth's gravity into a solar map`)",
        "  4. `P3:02_von_frisch_1949_polaroid_sky_compass_and_lindauer_1955_swarm_20_sites_to_1_consensus_chart` — Karl von Frisch (1949 *Experientia* 5: 142–148) Polaroid ultraviolet sky-compass & Martin Lindauer (1955 *Z. vergl. Physiol.* 37: 263–324) `20 → 1` swarm house-hunting consensus & `15°/hour` clock shift (`SCALE: a marathon scout bee dancing in a windowless room for four hours automatically rotates her waggle angle by sixty degrees — fifteen degrees every hour — tracking the moving Sun across the sky without ever peeking outside`)",
        "  5. `P4:02_michelsen_kirchner_lindauer_june_1989_naturwissenschaften_robot_bee_280hz_and_polar_histogram_chart` — Michelsen, Kirchner & Lindauer (June 1989 *Naturwissenschaften* 76: 277–280) `280-Hz` brass-and-razor-blade robot bee schematic & 8-station polar capture histogram (`SCALE: Axel Michelsen's robot bee was made from a scrap of brass tubing, a sliver of a shaving razor blade, and a coat of beeswax — yet when a computer made it waggle in the dark, living honeybees obeyed its directions and flew to an empty meadow a kilometre away`)",
        "  6. `P5:01_timeline_1914_1989_and_colour_vision_waggle_dance_polarized_compass_swarm_democracy_robot_bee_chart` — completed timeline (1914 → 1989) + bee colour vision, sun-to-gravity waggle dance, polarized-sky compass, swarm democracy & the 1989 mechanical robot bee (`SCALE: from five dots of shellac paint on an Austrian lakeside to a vibrating razor-blade robot in a dark hive, scientists proved that the smallest brains in your garden speak a mathematical language of the Sun`)",
        f"- **£0 verified reuse ({totals['reuse']} row):** `P5:04_table_three_callback` uses the 2.40 s unused moving tail `[5.50s..7.90s]` of `P1:07_table_three_props_1914_blue_grey_card_grid_1945_glass_hive_protractor_and_1989_brass_robot_bee`.",
        "",
        "## Mint order",
        "",
        "006 > 007 > 008 > 009 > 010 > 011 > 012 > 013 > 014 > 015 > 016 > 017 > 018 > 019 > 020 > 021 > 022 > 023 > 024 > 025 > 026 > 027 > 028 > 029 > 030 > 031 > 032 > 033 > 034 > 035 > 036 > 037 > 038 > 039 > 040 > 041 > 042 > 043 > 044 > 045 > 046 > 047 > 048 > 049 > 050 > 051 > 052 > 053 > 054 > 055 > 056 > 057 > 058 > 059 > 060 > 061 > 062 > 063 > 064 > 065 > 066 > 067 > 068 > 069 > 070 > 071 > 072 > 073 > 074 > 075 > 076 > 077 > 078 > 079 > 080 > 081 > 082 > 083 > 084 > 085 > 086 > 087 > 088 > 089 > 090 > 091 > 092 > 093 > 094 > 095. `generation_authorized` is `false` on every row.",
    ])
    (EDIT / "PRICE_REVIEW_v01.md").write_text("\n".join(pr_lines) + "\n")
    print(f"089 v01 boards written: {totals['rows']} rows, Flow expected={totals['flow_credits_expected']}")


if __name__ == "__main__":
    main()
