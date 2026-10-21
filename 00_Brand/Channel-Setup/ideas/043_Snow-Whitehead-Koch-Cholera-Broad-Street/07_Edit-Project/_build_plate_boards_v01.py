#!/usr/bin/env python3
"""HOS 043 (The Broad Street Pump: How One Doctor's Map Stopped a Plague) pre-VO plate boards v01. J0540. No mint, no spend.

Built from 00_Brand/Channel-Setup/ideas/043_Snow-Whitehead-Koch-Cholera-Broad-Street/cholera_script_master_v01.md
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
        "Part 01 — Six Hundred Deaths on One London Street and the Missing Iron Handle",
        [
            ("01_snow_and_whitehead_8_sep_1854_soho_broad_street_pump_handle_removed", 0.0, 5.5, "A", False, "THE PUMP HANDLE THAT SAVED LONDON", "Quality",
             "Quality: Short frame 0 / answer image (0:03) + on the cobblestone corner of Broad Street and Cambridge Street in Soho, London, on the morning of 8 September 1854, a workman unbolts and removes the heavy iron handle from the Broad Street public water pump while 41-year-old physician John Snow and Reverend Henry Whitehead hold an inked street map covered in black mortality bars.",
             STYLE + "On a foggy 1854 Soho cobblestone street corner, a Victorian parish workman uses an iron spanner to lift the curved cast-iron handle off a street water pump while physician John Snow in a dark frock coat and clergyman Henry Whitehead hold an open street map marked with black ink bars." + QUAL_TAIL,
             {"kind": "WHEN", "label": "SOHO, LONDON, 8 SEPTEMBER 1854", "timeline_step": "2/5 · 31 Aug – 8 Sep 1854 (616 die around the Soho Broad Street pump; John Snow maps the outbreak and convinces the parish to remove the pump handle on 8 Sep)", "hold_s": 3.5}),
            ("02_snow_1854_water_table_soho_dot_map_and_koch_comma_bacillus_split", 5.5, 6.0, "B", False, "TWO PIPES, ONE MAP, THE GERM", "Quality",
             "Quality: complex three-part split composition (John Snow's 1854 South London water-company comparison table on the left; Snow's Soho dot-and-bar map clustering around the Broad Street pump in the centre; Filippo Pacini's 1854 and Robert Koch's 1883 comma-shaped Vibrio cholerae bacterium under a brass microscope on the right).",
             STYLE + "Three-panel Victorian scientific composition: on the left, two iron water pipes beside glass sample bottles; in the centre, an inked street map clustered with black bars around a street pump; on the right, a brass microscope beside a circular slide view of curved comma-shaped microbes." + QUAL_TAIL,
             None),
            ("03_snow_2_sep_1854_soho_door_to_door_notebook_inquiry", 11.5, 6.0, "C", False, "2 SEPTEMBER 1854", "Quality",
             "Quality: readable faces (on 2–6 September 1854 in Soho, London, 41-year-old John Snow walks past lime-washed doorways and horse-drawn hearses, notebook in hand, questioning bereaved neighbours within 250 yards of the Broad Street pump).",
             STYLE + "In a narrow 1854 Soho street with shuttered windows, forty-one-year-old physician John Snow in a dark frock coat and top hat writes intently in a leather pocket notebook while speaking with a grieving resident on a doorstep." + QUAL_TAIL,
             {"kind": "WHEN", "label": "SOHO, 2 SEPTEMBER 1854", "timeline_step": "2/5 · 31 Aug – 8 Sep 1854 (John Snow walks house to house in Soho mapping the Broad Street cholera outbreak)", "hold_s": 3.5}),
            ("04_soho_616_deaths_250_yards_vs_70_lion_brewery_workers_0_deaths_chart", 17.5, 8.0, "E", False, "SOHO (616 DEATHS, 73/83 NEAR PUMP) VS LION BREWERY (70 WORKERS, 0 DEATHS) & CESSPOOL 2 FT 8 IN", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked Soho mortality and distance chart from John Snow (1855) and the Parish Inquiry Report (1855) shows 616 fatal cholera cases around the Broad Street pump (73 of the first 83 deaths within 250 yards drank its water; leaking cesspool at 40 Broad Street just 2 ft 8 in / 81 cm from the well) vs 0 deaths among the 70 Lion Brewery workers next door who drank malt beer and 5 deaths among 535 Poland Street Workhouse inmates with their own private well.",
             {"kind": "DATA", "label": "BROAD ST PUMP: 616 DEATHS (73/83 FIRST CASES) VS 70 BREWERY MEN (0 DEATHS) · CESSPOOL 2 FT 8 IN", "detail": "Inked Soho mortality & distance chart on period paper from John Snow (1855) and the Parish Inquiry Report (1855) showing 616 fatal cholera cases around the Broad Street pump (73 of the first 83 deaths within 250 yards of the pump drank its water) vs 0 deaths among the 70 Lion Brewery workers next door who drank malt beer and 5 deaths among 535 Poland Street Workhouse inmates who had their own private well", "scale": "inside a circle just two hundred and fifty yards across — less than a three-minute walk — more than six hundred neighbours died in ten days, while seventy brewery workers right across the street didn't lose a single man", "who_card": "John Snow (1813–1858) — English physician and anaesthetist · Henry Whitehead (1825–1896) — Anglican curate of St Luke's, Soho", "when_stamp": "8 September 1854", "hold_s": 3.8}),
            ("05_unbolted_cast_iron_pump_handle_spanner_and_glass_water_jar_pan", 25.5, 5.5, "A", False, "SOHO, 1854", "Fast",
             "Fast: daylight macro pan across the unbolted curved cast-iron pump handle, heavy iron bolts, a Victorian spanner, and a glass bottle of clear well water on a stone ledge between code graphics so two full-frame graphics never run back to back. Nothing emissive, no face.",
             STYLE + "In crisp daylight on a stone workbench, the camera pans smoothly across a heavy curved cast-iron water pump handle, two iron hex bolts, a steel spanner, and a clear glass apothecary bottle of water." + FAST_TAIL,
             None),
            ("06_south_london_grand_experiment_southwark_315_vs_lambeth_37_per_10000_chart", 31.0, 8.0, "E", False, "8.5× HIGHER DEATH RATE", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period parchment, an inked South London Grand Experiment bar chart from John Snow (1855, Table IX) compares 40,046 Southwark & Vauxhall houses (1,263 cholera deaths = 315 per 10,000 houses, drawing sewage-tainted Thames water at Battersea) vs 26,107 Lambeth Company houses (98 deaths = 37 per 10,000 houses, drawing clean water upstream at Thames Ditton — an 8.5× higher death rate on the exact same streets).",
             {"kind": "DATA", "label": "SOUTH LONDON (1854): SOUTHWARK & VAUXHALL (315/10,000 HOUSES) VS LAMBETH (37/10,000 — 8.5× LOWER)", "detail": "Inked South London Grand Experiment bar chart from John Snow (1855, Table IX) comparing 40,046 Southwark & Vauxhall houses (1,263 cholera deaths = 315 per 10,000 houses) vs 26,107 Lambeth Company houses (98 deaths = 37 per 10,000 houses) in the first four weeks of the 1854 epidemic", "scale": "two families living next door to each other on the exact same street breathed the exact same air — yet the family whose water pipe came from downstream sewage died at more than eight times the rate of their neighbour", "hold_s": 3.8}),
            ("07_table_three_props_unbolted_pump_handle_soho_map_and_silver_nitrate_vials", 39.0, 5.5, "C", False, "1849 TO 1884", "Fast",
             "Fast: daylight prop table (callback source for Part 05: the unbolted cast-iron Broad Street pump handle, John Snow's rolled inked map of Soho with a brass magnifying glass, and two glass water-testing vials with a silver nitrate dropper bottle). Nothing emissive.",
             STYLE + "On an oak study table in soft window light sit three objects side by side: a heavy cast-iron water pump handle, a rolled street map beside a brass magnifying glass, and two glass water sample vials next to an amber dropper bottle." + FAST_TAIL,
             None),
            ("08_explorer_lifting_miniature_pump_handle_to_stop_falling_black_dominoes", 62.0, 5.5, "A", True, None, "Quality",
             "Quality: Explorer beat 1 (locked character reference, after 1:00).",
             STYLE + "Peering through a brass magnifying glass at a miniature tabletop street map where tiny black dominoes topple outward from a miniature iron water pump, the Explorer uses small brass pliers to lift the handle off the miniature pump, halting the dominoes instantly." + EXP_TAIL,
             None),
            ("09_john_snow_september_1854_ruling_black_mortality_bars_on_soho_map", 67.5, 5.5, "B", False, "LONDON, SEPTEMBER 1854", "Quality",
             "Quality: readable face (in his Sackville Street study in September 1854, 41-year-old physician John Snow rules black ink bars onto Charles Cheffins's street map of Soho).",
             STYLE + "In a Victorian London study lit by a tall window, forty-one-year-old physician John Snow leans over a wooden desk with a brass ruler and dip pen, drawing neat black ink bars beside a street pump on a large map." + QUAL_TAIL,
             None),
        ],
    ),
    (
        2,
        "Part 02 — The Miasma Myth & John Snow's 300,000-Person South London Experiment",
        [
            ("01_chadwick_miasma_street_grate_and_snow_1854_south_london_silver_nitrate_test", 73.0, 6.5, "A", False, "TESTED TAP WATER DOOR TO DOOR", "Quality",
             "Quality: readable faces (Sanitary Commissioner Edwin Chadwick pointing to foul vapour rising from a London street grate in 1849, dissolving to 41-year-old physician John Snow in 1854 knocking on doors in South London and testing tap water in glass vials with silver nitrate).",
             STYLE + "Split Victorian scene: on the left, Sanitary Commissioner Edwin Chadwick gestures toward a cast-iron street sewer grate; on the right in South London in 1854, physician John Snow holds up a glass vial of tap water on a doorstep as white cloudy precipitate forms." + QUAL_TAIL,
             {"kind": "WHO", "label": "Edwin Chadwick (1800–1890) — English social reformer and sanitary commissioner", "fact_card": "Tested tap water door to door", "when_stamp": "1831 · 1849 · 1852 · 1853 · 1854", "timeline_step": "1/5 · 1849 (John Snow publishes On the Mode of Communication of Cholera proposing waterborne transmission) & 3/5 · 1854–1855 (Snow's South London Grand Experiment proves 315 vs 37 deaths per 10,000 houses)", "hold_s": 3.8}),
            ("02_snow_1855_intermingled_south_london_pipes_300000_people_315_vs_37_chart", 79.5, 8.0, "E", False, "300,000 PEOPLE ON SAME STREETS: SOUTHWARK (1,263 DEATHS / 40,046 HOUSES) VS LAMBETH (98 / 26,107)", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked street-pipe and mortality comparison diagram from John Snow (1855, On the Mode of Communication of Cholera) shows intermingled Southwark & Vauxhall pipes (sewage-tainted Thames at Battersea: 1,263 deaths in 40,046 houses = 315 per 10,000) vs Lambeth Company pipes (clean Thames Ditton intake: 98 deaths in 26,107 houses = 37 per 10,000).",
             {"kind": "DATA", "label": "300,000 SOUTH LONDONERS: SOUTHWARK PIPE (315/10,000 DEATHS) VS LAMBETH PIPE (37/10,000 DEATHS)", "detail": "Inked street-pipe & mortality comparison diagram on period paper from John Snow (1855, On the Mode of Communication of Cholera) showing intermingled Southwark & Vauxhall pipes (sewage-tainted Thames at Battersea: 1,263 deaths in 40,046 houses = 315 per 10,000) vs Lambeth Company pipes (clean Thames Ditton intake: 98 deaths in 26,107 houses = 37 per 10,000)", "scale": "three hundred thousand Londoners living side by side on the exact same streets unwittingly took part in a blind medical trial — and the dirty pipe killed more than eight times as many neighbours as the clean one", "hold_s": 3.8}),
            ("03_two_cast_iron_water_pipes_under_cobblestones_and_silver_nitrate_test_vials", 87.5, 6.5, "B", False, "1854 — THE GRAND EXPERIMENT", "Fast",
             "Fast: daylight macro shot of two glass water sample jars (one cloudy with white silver-chloride precipitate from salty Battersea river water, one crystal clear from Thames Ditton) beside a reagent bottle on a wooden table. Nothing emissive, no face.",
             STYLE + "In crisp daylight on a wooden table, two clear glass sample jars stand side by side—one filled with milky white precipitate and one crystal clear—beside a glass dropper bottle and an open ledger." + FAST_TAIL,
             None),
            ("04_snow_1849_pamphlet_and_1855_table_ix_ledger_with_brass_compass_pan", 94.0, 5.5, "C", False, "315 VS 37 PER 10,000 HOUSES", "Fast",
             "Fast: daylight close-up of John Snow's open statistical ledger and brass dividers beside a folded Victorian street map of South London. Nothing emissive, no face.",
             STYLE + "In bright window light on a study desk, an open ruled ledger book and brass measuring dividers rest beside a folded coloured map of London districts." + FAST_TAIL,
             None),
        ],
    ),
    (
        3,
        "Part 03 — 2–8 September 1854: The Brewery Workers, the Hampstead Widow & the Broad Street Map — Midpoint Twist",
        [
            ("01_snow_questioning_lion_brewery_foreman_and_farr_mortality_registers", 99.5, 6.5, "A", False, "WIDOW HAD SOHO WATER CARTED", "Quality",
             "Quality: readable faces (physician John Snow on 3–7 September 1854 questioning Lion Brewery manager Mr Huggins outside the Broad Street brewery while consulting mortality address lists from Registrar-General William Farr).",
             STYLE + "Outside a brick Victorian brewery on Broad Street in 1854, physician John Snow with his open notebook speaks with a stout brewery manager standing beside wooden malt barrels while workmen carry copper jugs." + QUAL_TAIL,
             {"kind": "WHO", "label": "William Farr (1807–1883) — British epidemiologist and statistician", "fact_card": "Widow had Soho water carted", "when_stamp": "31 August 1854 · 3 September 1854 · 7 September 1854", "timeline_step": "2/5 · 31 Aug – 8 Sep 1854 (616 die around the Soho Broad Street pump; Snow maps the outbreak and convinces the parish to remove the pump handle on 8 Sep)", "hold_s": 3.8}),
            ("02_snow_1855_soho_anomalies_brewery_70_workhouse_535_and_hampstead_widow_chart", 106.0, 8.0, "E", False, "BROAD ST PUMP (73/83 WITHIN 250 YDS) · LION BREWERY (0/70) · WORKHOUSE (5/535) · HAMPSTEAD (4 MILES)", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked Soho anomaly and distance chart from Snow (1855) shows the Broad Street pump zone (616 total deaths; 73 of first 83 within 250 yards) vs Lion Brewery (70 workers, 0 deaths — drank beer), Poland Street Workhouse (535 inmates, 5 deaths — private well), and Susannah Eley in Hampstead (4 miles away, fatal dose delivered by bottle on 31 Aug 1854).",
             {"kind": "DATA", "label": "SOHO PROOF: 73/83 NEAR PUMP · 0/70 BREWERY MEN · 5/535 WORKHOUSE · HAMPSTEAD BOTTLE 4 MILES AWAY", "detail": "Inked Soho anomaly & distance chart on period paper from Snow (1855) showing the Broad Street pump zone (616 total deaths; 73 of first 83 within 250 yards) vs Lion Brewery (70 workers, 0 deaths — drank beer), Poland Street Workhouse (535 inmates, 5 deaths — private well), and Susannah Eley in Hampstead (4 miles away, fatal dose delivered by bottle on 31 Aug 1854)", "scale": "a single bottle of Broad Street water carried four miles across London to high, clean air in Hampstead was enough to kill both the widow who drank it and her niece", "hold_s": 3.8}),
            ("03_snow_7_sep_1854_presenting_map_to_st_james_parish_board_of_guardians", 114.0, 6.5, "B", False, "8 SEPTEMBER 1854 — HANDLE REMOVED", "Quality",
             "Quality: readable faces (on the evening of 7 September 1854 in St James's vestry hall, John Snow spreads his inked Soho mortality map before the skeptical Parish Board of Guardians, pointing to the cluster around the Broad Street pump).",
             STYLE + "Inside an 1854 oak-panelled parish boardroom, physician John Snow points to a large street map covered in black clusters while seated Victorian vestrymen lean forward in astonishment." + QUAL_TAIL,
             None),
            ("04_wooden_brewery_cask_pewter_tankard_and_wicker_water_carboy_pan", 120.5, 5.5, "C", False, "70 BREWERY WORKERS — 0 DEATHS", "Fast",
             "Fast: daylight close-up of an oak brewery cask and pewter beer tankard beside a wicker-wrapped glass water carboy bottle on a wooden cart bed. Nothing emissive, no face.",
             STYLE + "In crisp daylight on a wooden table, a small oak beer cask and a pewter tankard sit beside a large glass bottle encased in woven wicker." + FAST_TAIL,
             None),
        ],
    ),
    (
        4,
        "Part 04 — Reverend Henry Whitehead's Cesspool Discovery at 40 Broad Street & the Comma Bacterium",
        [
            ("01_whitehead_and_york_april_1855_40_broad_street_cesspool_and_koch_microscope", 126.0, 6.5, "A", False, "CESSPOOL LEAKED 2 FT 8 IN AWAY", "Quality",
             "Quality: readable faces (29-year-old Anglican curate Reverend Henry Whitehead in April 1855 watching surveyor Jehoshaphat York excavate the crumbling brick cesspool at 40 Broad Street just 2 feet 8 inches from the well shaft, dissolving to Filippo Pacini in 1854 and Robert Koch in 1883–1884 viewing comma-shaped Vibrio cholerae under a brass microscope).",
             STYLE + "Split Victorian scene: on the left in an 1855 Soho street excavation, curate Henry Whitehead and surveyor Jehoshaphat York hold a wooden measuring rod across a narrow gap between a brick cesspool and a circular well shaft; on the right, bacteriologist Robert Koch peers through a brass microscope." + QUAL_TAIL,
             {"kind": "WHO", "label": "Filippo Pacini (1812–1883) — Italian anatomist and microscopist · Robert Koch (1843–1910) — German physician and bacteriologist", "fact_card": "Cesspool leaked 2 ft 8 in away", "when_stamp": "28 August 1854 · April 1855 · August 1883 · January 1884", "timeline_step": "3/5 · 1854–1855 (Henry Whitehead traces the Broad Street index case to a leaking cesspool 2 ft 8 in from the well; Filippo Pacini describes Vibrio cholerae) & 5/5 · 1883–1884 (Robert Koch isolates and cultures the cholera comma bacillus)", "hold_s": 3.8}),
            ("02_york_april_1855_40_broad_st_2ft_8in_cesspool_cross_section_and_vibrio_chart", 132.5, 8.0, "E", False, "APRIL 1855 EXCAVATION: 40 BROAD ST CESSPOOL 2 FT 8 IN (81 CM) FROM WELL + VIBRIO CHOLERAE (1.5–2 µM)", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked architectural cross-section and bacterial diagram from York's April 1855 excavation of 40 Broad Street shows the cesspool 2 feet 8 inches (81 cm) from the Broad Street pump well shaft (28–31 Aug 1854 index case Frances Lewis) alongside Filippo Pacini's 1854 and Robert Koch's 1884 comma-shaped Vibrio cholerae (~1.5–2 micrometres long).",
             {"kind": "DATA", "label": "40 BROAD ST CESSPOOL: 2 FT 8 IN (81 CM) FROM PUMP WELL + PACINI (1854) / KOCH (1884) COMMA BACILLUS", "detail": "Inked architectural cross-section & bacterial diagram on period paper from York's April 1855 excavation of 40 Broad Street (cesspool 2 feet 8 inches / 81 cm from the Broad Street pump well shaft, 28–31 Aug 1854 index case) alongside Filippo Pacini's 1854 and Robert Koch's 1884 comma-shaped Vibrio cholerae (~1.5–2 micrometres long)", "scale": "just thirty-two inches of crumbling brick — less than the length of an umbrella — separated a leaking cesspool at number forty Broad Street from the drinking water of an entire neighbourhood", "hold_s": 3.8}),
            ("03_york_1855_architectural_well_plan_brass_microscope_and_glass_slides_closeup", 140.5, 6.5, "B", False, "APRIL 1855 — 40 BROAD STREET", "Fast",
             "Fast: daylight macro shot of surveyor Jehoshaphat York's architectural cross-section drawing of the Broad Street well beside a Victorian brass monocular microscope and glass specimen slides on a wooden desk. Nothing emissive, no face.",
             STYLE + "In bright daylight on a wooden desk, an inked architectural cross-section drawing of a brick well sits beside a polished brass Victorian microscope and a wooden tray of glass slides." + FAST_TAIL,
             None),
            ("04_explorer_sliding_copper_shield_between_leaking_cesspool_and_well_model", 147.0, 5.5, "B", True, None, "Quality",
             "Quality: Explorer beat 2 (locked character reference).",
             STYLE + "Inspecting a cutaway tabletop brick model where dark droplets seep through crumbling mortar between a miniature cesspool and a well shaft, the Explorer slides a bright copper barrier plate between the brick walls so the well water below turns crystal clear." + EXP_TAIL,
             None),
        ],
    ),
    (
        5,
        "Part 05 — Joseph Bazalgette's Sewers, Modern Epidemiology & How Earthquakes Let Us See Earth's Solid Core",
        [
            ("01_timeline_1849_1884_bazalgette_82_miles_sewers_and_cholera_under_1_percent_chart", 152.5, 8.5, "E", False, "1849–1884 TIMELINE · BAZALGETTE'S 82 MILES OF SEWERS · TREATED CHOLERA FATALITY >50% TO <1%", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, the 5-date timeline completes: 1849 (John Snow publishes On the Mode of Communication of Cholera proposing waterborne transmission) · 31 Aug – 8 Sep 1854 (616 die around the Soho Broad Street pump; Snow maps the outbreak and convinces the parish to remove the pump handle on 8 Sep) · 1854–1855 (Snow's South London Grand Experiment proves 315 vs 37 deaths per 10,000 houses; Henry Whitehead traces the Broad Street index case to a leaking cesspool 2 ft 8 in from the well; Filippo Pacini describes Vibrio cholerae) · 1859–1866 (Bazalgette builds 82 miles of London intercepting sewers; William Farr uses Snow's water-pipe method to pinpoint the 1866 East London outbreak) · 1883–1884 (Robert Koch isolates and cultures the cholera comma bacillus in Egypt and India).",
             {"kind": "DATA", "label": "1849–1884 TIMELINE · BAZALGETTE'S 82 MILES OF SEWERS · TREATED CHOLERA DEATHS: >50% → <1%", "detail": "Animated 5-date timeline (1849 → 1883–1884) alongside Joseph Bazalgette's 82 miles of intercepting brick sewers and the drop in treated cholera fatality from >50% to <1%", "scale": "replacing polluted river water with clean pipes and sewers — plus simple salt-and-sugar rehydration — cut the death rate of treated cholera from more than half of all patients to less than one in a hundred", "fact_card": "Cut cholera deaths under 1%", "when_stamp": "June 1858 · 1866 · 1849–1884", "timeline_step": "4/5 · 1859–1866 (Bazalgette builds 82 miles of London intercepting sewers; William Farr uses Snow's water-pipe method to pinpoint the 1866 East London outbreak) & 5/5 · 1883–1884 (Robert Koch isolates and cultures the cholera comma bacillus)", "hold_s": 3.8}),
            ("02_bazalgette_victorian_brick_intercepting_sewer_arch_and_embankment_model", 161.0, 5.5, "A", False, "CLEAN WATER SAVES MILLIONS", "Fast",
             "Fast: daylight architectural scale model of Joseph Bazalgette's oval Portland-cement brick intercepting sewer tunnel beneath the Thames Embankment beside rolled engineering blueprints. Nothing emissive, no face.",
             STYLE + "In crisp daylight on an engineering table, a detailed masonry cutaway model of a Victorian oval brick sewer arch beneath a stone river embankment sits beside rolled blue-and-cream plans." + FAST_TAIL,
             None),
            ("03_mohorovicic_1909_gutenberg_1914_and_inge_lehmann_1936_earth_core_handoff", 166.5, 6.5, "C", False, "EARTHQUAKES TO EARTH'S CORE", "Quality",
             "Quality: readable faces (Danish seismologist Inge Lehmann in 1936 in Copenhagen holding oatmeal-box seismograph cards beside Andrija Mohorovičić's 1909 Zagreb seismograph and a cutaway globe revealing Earth's liquid outer core and solid metal inner core — handoff to 044 Earth's Solid Inner Core).",
             STYLE + "Split period scene: on the left in a 1936 Copenhagen garden study, Danish seismologist Inge Lehmann holds cardboard index cards marked with earthquake wave traces beside a brass seismograph drum; on the right, a cutaway terrestrial globe reveals a solid metallic inner core inside a liquid outer core." + QUAL_TAIL,
             {"kind": "WHEN", "label": "8 OCTOBER 1909 · 1914 · 1936", "hold_s": 3.5}),
            ("04_table_three_callback", 173.0, 2.4, "C", False, None, "reuse",
             "Reuse: verified unused moving window [5.50s..7.90s] of P1:07_table_three_props_unbolted_pump_handle_soho_map_and_silver_nitrate_vials (callback, £0).",
             "Reuse P1:07_table_three_props_unbolted_pump_handle_soho_map_and_silver_nitrate_vials [5.50s..7.90s] (2.40s distinct non-overlapping tail window from 8.00s source clip).",
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
                row["reuse_of"] = "P1:07_table_three_props_unbolted_pump_handle_soho_map_and_silver_nitrate_vials"
                row["reuse_window_s"] = [5.5, 7.9]
                row["reuse_audit"] = {
                    "source_row": "P1:07_table_three_props_unbolted_pump_handle_soho_map_and_silver_nitrate_vials",
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
            "film": "043_Snow-Whitehead-Koch-Cholera-Broad-Street",
            "part": p_idx,
            "title": p_title,
            "version": "v01",
            "timing_status": "pre_vo_script_clock (built from cholera_script_master_v01.md; retimes onto Scribe STT once VO locks)",
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
        "film": "043_Snow-Whitehead-Koch-Cholera-Broad-Street",
        "version": "v01",
        "date": "2026-10-18",
        "owner": "gemini (J0540)",
        "status": "PRE_VO_BOARDS_V01_NO_MINT",
        "generation_authorized": False,
        "script": "00_Brand/Channel-Setup/ideas/043_Snow-Whitehead-Koch-Cholera-Broad-Street/cholera_script_master_v01.md",
        "script_review_score": 91.0,
        "sources": "00_Brand/Channel-Setup/ideas/043_Snow-Whitehead-Koch-Cholera-Broad-Street/SOURCES_v01.md",
        "credit_snapshot": {
            "flow_balance": 23740,
            "flow_floor": 0,
            "flow_read_at": "2026-10-15T21:42:22Z",
            "vertex_promo_gbp": 71.02,
            "vertex_usable_gbp": 70.02,
        },
        "totals": totals,
        "per_part": per_part_summary,
        "mint_order": "006 > 007 > 008 > 009 > 010 > 011 > 012 > 013 > 014 > 015 > 016 > 017 > 018 > 019 > 020 > 021 > 022 > 023 > 024 > 025 > 026 > 027 > 028 > 029 > 030 > 031 > 032 > 033 > 034 > 035 > 036 > 037 > 038 > 039 > 040 > 041 > 042 > 043. Nothing in 043 is generation_authorized.",
    }
    (EDIT / "PICTURE_PLAN_v01.json").write_text(json.dumps(plan, indent=2) + "\n")

    sl = [
        "# 043 The Broad Street Pump: How One Doctor's Map Stopped a Plague — Shot list & plate boards v01 (pre-VO)",
        "",
        "Gemini, 18 Oct 2026, J0540. Built from `cholera_script_master_v01.md` (`91.0 PASS`) and `SOURCES_v01.md`.",
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
        "# 043 price review v01 (pre-VO plate boards)",
        "",
        "Gemini, 18 Oct 2026, J0540. Boards only. **No mint. No spend. No merge.**",
        "Prepared from `cholera_script_master_v01.md` (`91.0 PASS`) and `SOURCES_v01.md` so 043's full plate board rows, non-emissive Fast prompts, £0 code graphics, and Teach-on-Screen overlays are ready to re-time the moment long VO locks. Parked for Chief.",
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
        f"- **Quality ({totals['Quality']} rows):** readable faces (John Snow, Reverend Henry Whitehead, Edwin Chadwick, William Farr, Filippo Pacini, Robert Koch, Inge Lehmann), 1854 Soho Broad Street pump handle removal & St James's vestry board meeting, April 1855 40 Broad Street excavation, and the 2 Explorer beats.",
        f"- **Fast ({totals['Fast']} rows, non-emissive):** daylight prop and laboratory shots (unbolted cast-iron pump handle, bolts & spanner pan, 3-object callback bench, Southwark vs Lambeth silver-nitrate water sample jars, John Snow's 1855 Table IX ledger & brass dividers, Lion Brewery oak cask & wicker water carboy, surveyor York's 1855 well cross-section & brass microscope, Joseph Bazalgette's brick intercepting sewer arch model). Zero candles, flames, sparks, or glowing elements on Fast.",
        f"- **£0 code graphics ({totals['code_graphic']} rows):**",
        "  1. `P1:04_soho_616_deaths_250_yards_vs_70_lion_brewery_workers_0_deaths_chart` — 616 fatal cholera cases around the Broad Street pump (73 of first 83 within 250 yards) vs 0 deaths among 70 Lion Brewery workers and 5 deaths among 535 Workhouse inmates (`SCALE: inside a circle just two hundred and fifty yards across — less than a three-minute walk — more than six hundred neighbours died in ten days, while seventy brewery workers right across the street didn't lose a single man`)",
        "  2. `P1:06_south_london_grand_experiment_southwark_315_vs_lambeth_37_per_10000_chart` — Snow's 1854 South London Table IX comparing 40,046 Southwark & Vauxhall houses (315 deaths per 10,000) vs 26,107 Lambeth Company houses (37 per 10,000 — 8.5× lower) (`SCALE: two families living next door to each other on the exact same street breathed the exact same air — yet the family whose water pipe came from downstream sewage died at more than eight times the rate of their neighbour`)",
        "  3. `P2:02_snow_1855_intermingled_south_london_pipes_300000_people_315_vs_37_chart` — intermingled Southwark & Vauxhall (Battersea sewage intake) vs Lambeth (Thames Ditton intake) street pipes across 300,000 South Londoners (`SCALE: three hundred thousand Londoners living side by side on the exact same streets unwittingly took part in a blind medical trial — and the dirty pipe killed more than eight times as many neighbours as the clean one`)",
        "  4. `P3:02_snow_1855_soho_anomalies_brewery_70_workhouse_535_and_hampstead_widow_chart` — Soho pump cluster (73/83 closest to pump), Lion Brewery (0/70), Poland Street Workhouse (5/535), and Hampstead widow Susannah Eley 4 miles away (`SCALE: a single bottle of Broad Street water carried four miles across London to high, clean air in Hampstead was enough to kill both the widow who drank it and her niece`)",
        "  5. `P4:02_york_april_1855_40_broad_st_2ft_8in_cesspool_cross_section_and_vibrio_chart` — Jehoshaphat York's April 1855 excavation of 40 Broad Street (cesspool 2 ft 8 in / 81 cm from pump well) + Pacini (1854) & Koch (1884) comma-shaped *Vibrio cholerae* (`SCALE: just thirty-two inches of crumbling brick — less than the length of an umbrella — separated a leaking cesspool at number forty Broad Street from the drinking water of an entire neighbourhood`)",
        "  6. `P5:01_timeline_1849_1884_bazalgette_82_miles_sewers_and_cholera_under_1_percent_chart` — completed 5-date timeline (1849 → 1883–1884) + Bazalgette's 82 miles of intercepting brick sewers and treated cholera fatality drop from >50% to <1% (`SCALE: replacing polluted river water with clean pipes and sewers — plus simple salt-and-sugar rehydration — cut the death rate of treated cholera from more than half of all patients to less than one in a hundred`)",
        f"- **£0 verified reuse ({totals['reuse']} row):** `P5:04_table_three_callback` uses the 2.40 s unused moving tail `[5.50s..7.90s]` of `P1:07_table_three_props_unbolted_pump_handle_soho_map_and_silver_nitrate_vials`.",
        "",
        "## Mint order",
        "",
        "006 > 007 > 008 > 009 > 010 > 011 > 012 > 013 > 014 > 015 > 016 > 017 > 018 > 019 > 020 > 021 > 022 > 023 > 024 > 025 > 026 > 027 > 028 > 029 > 030 > 031 > 032 > 033 > 034 > 035 > 036 > 037 > 038 > 039 > 040 > 041 > 042 > 043. `generation_authorized` is `false` on every row.",
    ])
    (EDIT / "PRICE_REVIEW_v01.md").write_text("\n".join(pr_lines) + "\n")
    print(f"043 v01 boards written: {totals['rows']} rows, Flow expected={totals['flow_credits_expected']}")


if __name__ == "__main__":
    main()
