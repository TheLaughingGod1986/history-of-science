#!/usr/bin/env python3
"""HOS 088 (Keystone Species: The Starfish Experiment That Shocked Ecology) pre-VO plate boards v01. J0805. No mint, no spend.

Built from 00_Brand/Channel-Setup/ideas/088_Elton-Lindeman-Carson-Paine-Food-Webs-Keystone-Species/food_webs_keystone_script_master_v01.md
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
        "Part 01 — Why Big Predators Are Rare & How Throwing Starfish Into the Sea Collapsed an Ecosystem",
        [
            ("01_four_tier_10_percent_energy_pyramid_and_robert_paine_1963_mukkaw_bay_crowbar_pisaster_starfish", 0.0, 5.5, "A", False, "THE 10% PYRAMID & KEYSTONE SPECIES", "Quality",
             "Quality: Short frame 0 / answer image (0:03) + side by side, a 4-tier ecological energy pyramid shrinks 10-fold at each step from 10,000 kg of green plants to 1,000 kg of herbivores, 100 kg of mesopredators, and 10 kg of top predator as 90% of energy escapes as heat, beside Robert Treat Paine III on the wave-lashed rocky shore of Mukkaw Bay, Washington in June 1963 prying a purple ochre starfish (Pisaster ochraceus) off a colourful 15-species tidepool ledge with a crowbar while the predator-free rock beside him collapses into a black wall of mussels.",
             STYLE + "Split ecological-and-historical scene: on the left, a sculpted four-tier pyramid of plants, rabbits, foxes, and a golden eagle shrinks tenfold at each step; on the right on the rocky Pacific shore of Mukkaw Bay in June 1963, ecologist Robert Paine pries a purple ochre starfish off a colourful tidepool rock with an iron crowbar beside a dark mussel-choked ledge." + QUAL_TAIL,
             {"kind": "WHEN", "label": "MUKKAW BAY, JUNE 1963", "timeline_step": "1/3 · 1927 & October 1942 (Charles Elton maps Arctic food webs and the Pyramid of Numbers, and Raymond Lindeman at Cedar Bog Lake proves the 10% trophic energy law)", "hold_s": 3.5}),
            ("02_elton_1927_lindeman_1942_paine_1963_starfish_and_rachel_carson_1962_silent_spring_split", 5.5, 6.0, "B", False, "10% ENERGY, KEYSTONE STARFISH, BIOMAGNIFICATION", "Quality",
             "Quality: complex three-part composition (Charles Elton on Arctic Bear Island in 1921–1927 and Raymond Lindeman at Cedar Bog Lake in 1942 measuring the 10% Trophic Energy Pyramid; Robert Paine at Mukkaw Bay in June 1963 tossing Pisaster starfish into the Pacific to discover keystone species and trophic cascades; and Rachel Carson in Silver Spring in September 1962 mapping DDT biomagnification up the food chain in Silent Spring).",
             STYLE + "Three-panel period composition: on the left, Charles Elton in 1927 Oxford and Raymond Lindeman in a 1941 Minnesota rowboat; in the centre, Robert Paine at 1963 Mukkaw Bay flinging a purple starfish into the surf; on the right, Rachel Carson in 1962 Silver Spring examining an osprey nest and food-chain chart." + QUAL_TAIL,
             None),
            ("03_roman_stone_arch_with_purple_starfish_keystone_15_species_vs_mussel_monoculture_collapse", 11.5, 6.0, "C", False, "15 SPECIES vs MONOCULTURE COLLAPSE", "Quality",
             "Quality: complex ecological reveal (a split comparison of an intact Roman stone arch held together by a single purple Pisaster starfish keystone at the top protecting 15 species of barnacles, chitons, limpets, sponges, and red algae below, vs pulling out that one keystone so dark California mussels overrun 100% of the rock and starve out 14 other species).",
             STYLE + "In a split coastal comparison, on the left a stone arch crowned by a purple starfish keystone shelters fifteen colourful tidepool species; on the right, removing the starfish keystone topples the arch as black mussels smother the entire rock face." + QUAL_TAIL,
             {"kind": "WHEN", "label": "1927 · OCTOBER 1942 · 27 SEPTEMBER 1962 · JUNE 1963 · 1966 · 1969", "timeline_step": "1/3 · 1927 & Oct 1942 (Elton & Lindeman) · 2/3 · 27 Sep 1962 (Carson Silent Spring) · 3/3 · June 1963–1969 (Paine keystone species)", "hold_s": 3.5}),
            ("04_elton_1927_lindeman_1942_10_percent_energy_pyramid_and_carson_1962_80000x_biomagnification_chart", 17.5, 8.0, "E", False, "LINDEMAN (1942): ~10% TROPHIC ENERGY TRANSFER & CARSON (1962): 80,000× CLEAR LAKE DDT BIOMAGNIFICATION", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked Food Webs, Trophic Energy Pyramid, Biomagnification & Keystone Species chart from Charles Elton (1927 Animal Ecology), Raymond Lindeman (October 1942 Ecology 23: 399–417), Rachel Carson (27 September 1962 Silent Spring), and Robert Paine (1966 Am. Nat. 100: 65–75 & 1969 Am. Nat. 103: 91–93) shows 1) Lindeman's ~10% energy transfer per trophic level (~90% lost as metabolic heat); 2) Carson's inverted DDT biomagnification pyramid (0.02 ppm water → 5 ppm plankton → 40–300 ppm fish → 1,600+ ppm grebes/eagles); and 3) Paine's Mukkaw Bay Pisaster removal crashing species diversity from 15 to 8 to 1.",
             {"kind": "DATA", "label": "1942 LINDEMAN (~10% TROPHIC ENERGY PYRAMID) & 1962 CARSON (80,000× CLEAR LAKE BIOMAGNIFICATION) CHART", "detail": "Inked Raymond Lindeman (1942) Cedar Bog Lake ~10% trophic energy transfer pyramid (100% primary producers → ~10% herbivores → ~1% primary carnivores → ~0.1% top predators) & Rachel Carson (1962) Clear Lake 80,000× DDT biomagnification curve on period paper", "scale": "because ninety percent of all food energy burns away as body heat at every step up the food chain, it takes ten thousand kilograms of grass to feed one thousand kilograms of rabbits, to feed one hundred kilograms of foxes, to keep a single ten-kilogram golden eagle alive", "who_cards": [
                 "Charles Sutherland Elton (1900–1991) — British ecologist and zoologist",
                 "Raymond Laurel Lindeman (1915–1942) — American ecologist",
                 "Rachel Louise Carson (1907–1964) — American marine biologist and conservationist",
                 "Robert Treat Paine III (1933–2016) — American zoologist and ecologist",
             ], "when_stamp": "1927 · October 1942 · 27 September 1962 · June 1963 · 1966 · 1969", "hold_s": 3.8}),
            ("05_elton_1927_animal_ecology_book_1942_ecology_journal_and_crowbar_starfish_pan", 25.5, 5.5, "A", False, "THE KEYSTONE OF THE LIVING WORLD", "Fast",
             "Fast: daylight close-up pan across Charles Elton's 1927 book Animal Ecology, Raymond Lindeman's October 1942 Ecology paper, and a sculpted purple Pisaster starfish beside a steel crowbar on an oak table. Nothing emissive, no face.",
             STYLE + "In warm window light on an oak table, an open 1927 ecology book and a 1942 scientific journal sit beside a sculpted purple ochre starfish, barnacle shells, and a steel crowbar." + FAST_TAIL,
             None),
            ("06_paine_1966_1969_mukkaw_bay_pisaster_removal_15_to_1_species_diversity_crash_chart", 31.0, 8.0, "E", False, "MUKKAW BAY, WASHINGTON, 1963–1966", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period parchment, an inked Robert Paine (1966 Am. Nat. 100: 65–75 & 1969 Am. Nat. 103: 91–93) Mukkaw Bay Keystone Predator Removal & Trophic Cascade diagram compares Control Plot (Pisaster ochraceus starfish present → eats dominant Mytilus californianus mussels → 15 intertidal species coexist) vs Starfish-Removal Plot (crowbar removal of Pisaster → Mytilus mussels monopolize rock space → species diversity crashes from 15 toward 1).",
             {"kind": "DATA", "label": "1966 & 1969 ROBERT PAINE (AM. NAT.): MUKKAW BAY PISASTER REMOVAL & 15 → 8 → 1 SPECIES DIVERSITY CRASH CHART", "detail": "Inked Robert Paine (1966) Mukkaw Bay intertidal species diversity crash (15 species with Pisaster starfish present vs rapid drop to 8 and 1 mussel monoculture when starfish are removed) on period paper", "scale": "a single purple starfish weighs less than a bag of sugar, yet by eating the bully mussel that would otherwise hog every square centimetre of rock, that one predator keeps fourteen other species of sea life alive", "hold_s": 3.8}),
            ("07_table_three_props_1942_plankton_net_jar_1962_silent_spring_book_and_1963_crowbar_starfish_arch", 39.0, 5.5, "C", False, "1927 TO 1969", "Fast",
             "Fast: daylight pan across three period props on a wooden bench: Lindeman's 1941 Cedar Bog Lake plankton net and sample jars, a 1962 first-edition copy of Rachel Carson's Silent Spring, and Paine's 1963 steel crowbar beside a stone keystone arch model (also provides 2.40s tail window [5.50s..7.90s] for P5:04 callback). Nothing emissive, no face.",
             STYLE + "In soft daylight on a wooden bench, a fine-mesh plankton net and glass lake-sediment jars sit beside a 1962 hardcover ecology book, an iron crowbar, and a miniature stone arch with a purple starfish keystone." + FAST_TAIL,
             None),
            ("08_explorer_sliding_purple_pisaster_starfish_keystone_back_into_15_species_tidepool_arch", 62.0, 5.5, "A", True, None, "Quality",
             "Quality: Explorer beat 1 (locked character reference, after 1:00).",
             STYLE + "Standing beside a giant sculpted stone arch built from fifteen colourful tidepool creatures, the Explorer catches the purple starfish keystone as an iron crowbar pries it loose and slides the starfish back into the apex of the arch so the encroaching black mussels retreat." + EXP_TAIL,
             None),
            ("09_raymond_and_eleanor_lindeman_1941_cedar_bog_lake_rowboat_hauling_plankton_nets", 67.5, 5.5, "B", False, "CEDAR BOG LAKE, 1941–1942", "Quality",
             "Quality: readable faces (at Cedar Bog Lake, Minnesota in 1941, 26-year-old Raymond Lindeman and his wife Eleanor Hall Lindeman haul up lake sediment and plankton nets in a small wooden rowboat to measure every calorie in the ecosystem).",
             STYLE + "In a wooden rowboat on a quiet reed-ringed Minnesota bog lake in 1941, young ecologists Raymond Lindeman and Eleanor Hall Lindeman lift a dripping plankton net and sediment corer into sample jars." + QUAL_TAIL,
             {"kind": "WHEN", "label": "CEDAR BOG LAKE, 1941–1942", "timeline_step": "1/3 · 1927 & October 1942 (Charles Elton maps Arctic food webs and Raymond Lindeman at Cedar Bog Lake proves the 10% trophic energy law)", "hold_s": 3.5}),
        ],
    ),
    (
        2,
        "Part 02 — 1927 & October 1942: Charles Elton's Arctic Food Web & Raymond Lindeman's 10% Trophic Energy Law",
        [
            ("01_charles_elton_1927_arctic_bear_island_food_web_and_lindeman_hutchinson_oct_1942_trophic_pyramid", 73.0, 6.5, "A", False, "90% ENERGY LOST PER STEP", "Quality",
             "Quality: readable faces (British ecologist Charles Sutherland Elton in 1927 tracing Arctic foxes, seabirds, and tundra plants into the first food web and Pyramid of Numbers, dissolving to Raymond Laurel Lindeman and Eleanor Hall Lindeman on Cedar Bog Lake with Yale mentor George Evelyn Hutchinson in October 1942 calculating the ~10% trophic energy transfer law).",
             STYLE + "Split period scene: on the left in 1927 Oxford, Charles Elton sketches an Arctic Bear Island food web and pyramid of numbers; on the right in October 1942 at Yale, George Evelyn Hutchinson holds Raymond and Eleanor Lindeman's Cedar Bog Lake trophic energy pyramid paper." + QUAL_TAIL,
             {"kind": "FACT", "label": "90% energy lost per step", "who_cards": [
                 "Eleanor Hall Lindeman (1914–2008) — American biologist and ecologist",
                 "George Evelyn Hutchinson (1903–1991) — British-American ecologist",
             ], "when_stamp": "1921 · 1927 · 1941 · October 1942", "timeline_step": "1/3 · 1927 & October 1942 (Charles Elton maps food webs and the Pyramid of Numbers; Raymond Lindeman proves the ~10% trophic energy transfer law)", "hold_s": 3.8}),
            ("02_elton_1927_arctic_food_web_and_lindeman_oct_1942_ecology_cedar_bog_lake_10_percent_energy_chart", 79.5, 8.0, "E", False, "1927 CHARLES ELTON (ANIMAL ECOLOGY: FOOD WEB & PYRAMID) & OCT 1942 RAYMOND LINDEMAN (ECOLOGY: ~10% TROPHIC ENERGY TRANSFER)", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked Charles Elton (1927 Animal Ecology) Arctic Bear Island food web & Pyramid of Numbers alongside Raymond Lindeman's (October 1942 Ecology 23: 399–417) Cedar Bog Lake cal/cm2/year trophic energy transfer pyramid (~10% progressive efficiency).",
             {"kind": "DATA", "label": "1927 ELTON ARCTIC FOOD WEB & OCT 1942 LINDEMAN (ECOLOGY 23: 399) CEDAR BOG LAKE ~10% TROPHIC ENERGY PYRAMID CHART", "detail": "Inked Charles Elton (1927 Animal Ecology) Arctic Bear Island food web & Pyramid of Numbers alongside Raymond Lindeman's (October 1942 Ecology 23: 399–417) Cedar Bog Lake cal/cm2/year trophic energy transfer pyramid (~10% progressive efficiency) on period paper", "scale": "if you eat a hundred-calorie steak, the cow had to eat roughly a thousand calories of grass, which had to soak up nearly a million calories of sunshine — meaning ninety percent of the energy is taxed away as heat at every single rung of nature's ladder", "hold_s": 3.8}),
            ("03_oxford_and_yale_1927_animal_ecology_and_oct_1942_ecology_trophic_dynamic_paper_closeup", 87.5, 6.5, "B", False, "1927 & 1942 — ELTON & LINDEMAN'S PYRAMID", "Fast",
             "Fast: daylight macro shot of Charles Elton's 1927 book Animal Ecology beside Raymond Lindeman's posthumous October 1942 Ecology paper 'The Trophic-Dynamic Aspect of Ecology' and Cedar Bog Lake sample vials on a desk. Nothing emissive, no face.",
             STYLE + "In crisp daylight on a university desk, an open 1927 ecology treatise and an October 1942 journal showing a trophic energy diagram sit beside labelled glass sample vials and a brass microscope." + FAST_TAIL,
             None),
            ("04_wooden_four_step_trophic_pyramid_model_with_90_percent_heat_loss_chutes_at_each_tier_pan", 94.0, 5.5, "C", False, "WHY BIG PREDATORS ARE ALWAYS RARE", "Fast",
             "Fast: daylight close-up pan across a four-tier wooden ecological pyramid demonstrator where 1,000 green marbles at the base drop 90% out through side chutes at each step, leaving 100 herbivore marbles, 10 carnivore marbles, and 1 top-predator marble at the apex. Nothing emissive, no face.",
             STYLE + "In bright window light on an oak table, a four-step wooden pyramid demonstrator funnels green glass marbles upward so only one in ten reaches each higher tier." + FAST_TAIL,
             None),
        ],
    ),
    (
        3,
        "Part 03 — June 1963: Robert Paine's Crowbar, Flying Starfish & the Discovery of Keystone Species and Trophic Cascades — Midpoint Twist",
        [
            ("01_robert_paine_june_1963_mukkaw_bay_crowbar_starfish_and_james_estes_1974_sea_otter_kelp_cascade", 99.5, 6.5, "A", False, "ONE STARFISH SAVED 15 SPECIES", "Quality",
             "Quality: readable faces (30-year-old zoologist Robert Treat Paine III at Mukkaw Bay in June 1963 prying purple Pisaster ochraceus starfish off an 8-metre rocky intertidal ledge with a steel crowbar and flinging them into the Pacific to discover keystone species in 1966–1969, dissolving to marine ecologist James A. Estes in the Aleutian Islands in 1974 observing sea otters controlling sea urchins to save kelp forests).",
             STYLE + "Split period scene: on the left at 1963 Mukkaw Bay, Robert Paine in rubber boots pries a purple starfish from a tidepool ledge with an iron crowbar; on the right in the 1974 Aleutian Islands, James Estes observes a sea otter floating above a lush underwater kelp forest and purple sea urchins." + QUAL_TAIL,
             {"kind": "FACT", "label": "One starfish saved 15 species", "who_card": "James A. Estes (born 1945) — American marine ecologist", "when_stamp": "1960 · June 1963 · January 1966 · January 1969 · 1974 · 1995", "timeline_step": "3/3 · June 1963–1969 & 1974–1995 (Robert Paine pries Pisaster starfish off Mukkaw Bay rocks to discover keystone species and trophic cascades, followed by James Estes's sea otters and Yellowstone's wolves)", "hold_s": 3.8}),
            ("02_paine_1966_1969_american_naturalist_mukkaw_bay_food_web_and_estes_1974_sea_otter_kelp_cascade_chart", 106.0, 8.0, "E", False, "1966 & 1969 ROBERT PAINE (AM. NAT.: KEYSTONE SPECIES) & 1974 JAMES ESTES (SCIENCE: SEA OTTER → URCHIN → KELP TROPHIC CASCADE)", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked Robert Paine (January 1966 Am. Nat. 100: 65–75 & January 1969 Am. Nat. 103: 91–93) Mukkaw Bay intertidal food web (Pisaster ochraceus apex predator controlling competitive dominant Mytilus californianus mussels) & 15-to-8-to-1 species diversity collapse curve alongside James Estes's (1974 Science 185: 1058–1060) sea otter → sea urchin → kelp forest trophic cascade.",
             {"kind": "DATA", "label": "1966–1969 PAINE (MUKKAW BAY 15 → 1 SPECIES COLLAPSE) & 1974 ESTES (SEA OTTER → URCHIN → KELP TROPHIC CASCADE) CHART", "detail": "Inked Robert Paine (January 1966 Am. Nat. 100: 65–75 & January 1969 Am. Nat. 103: 91–93) Mukkaw Bay intertidal food web & 15-to-8-to-1 species diversity collapse curve alongside James Estes's (1974 Science 185: 1058–1060) sea otter → sea urchin → kelp forest trophic cascade on period paper", "scale": "Robert Paine didn't need a particle accelerator or a million-dollar telescope to revolutionize ecology — he just needed a steel crowbar, a pair of rubber boots, and the patience to fling starfish into the waves at low tide", "hold_s": 3.8}),
            ("03_mukkaw_bay_and_seattle_1966_1969_american_naturalist_papers_pisaster_starfish_and_mussel_shells_closeup", 114.0, 6.5, "B", False, "1963–1969 — PAINE'S KEYSTONE SPECIES", "Fast",
             "Fast: daylight macro shot of Robert Paine's January 1966 and January 1969 American Naturalist papers beside a preserved purple Pisaster starfish, dark California mussel shells, and a steel crowbar on a bench. Nothing emissive, no face.",
             STYLE + "In crisp daylight on a marine station bench, two open 1966 and 1969 ecology journals sit beside a purple five-armed starfish model, clusters of dark blue-black mussel shells, and a steel crowbar." + FAST_TAIL,
             None),
            ("04_split_intertidal_diorama_comparing_diverse_15_species_tidepool_vs_single_mussel_barren_pan", 120.5, 5.5, "C", False, "CONTROL PLOT VS STARFISH-REMOVAL PLOT", "Fast",
             "Fast: daylight close-up pan across a two-sided coastal tidepool diorama comparing a vibrant 15-species rock ledge guarded by a purple starfish on the left with a monotonous wall of black mussels on the right. Nothing emissive, no face.",
             STYLE + "In bright window light on an oak table, a detailed coastal tidepool diorama contrasts a colourful 15-species rock garden guarded by a purple starfish on the left with a solid black mussel monoculture on the right." + FAST_TAIL,
             None),
        ],
    ),
    (
        4,
        "Part 04 — 27 September 1962: Rachel Carson's Silent Spring & How the 10% Pyramid Flips Into Biomagnification",
        [
            ("01_roy_barker_1958_rachel_carson_27_sep_1962_silent_spring_and_derek_ratcliffe_1967_eggshell_thinning", 126.0, 6.5, "A", False, "DDT MAGNIFIED 80,000 TIMES", "Quality",
             "Quality: readable faces (entomologist Roy Jean Barker in 1958 tracing DDT from elm leaves to earthworms to robins, dissolving to marine biologist Rachel Louise Carson on 27 September 1962 publishing Silent Spring to expose trophic biomagnification and British ornithologist Derek Almey Ratcliffe in 1967 measuring thinned peregrine falcon eggshells).",
             STYLE + "Split period scene: on the left in 1958–1962, Roy Barker and Rachel Carson examine earthworm and Clear Lake grebe tissue data beside a first-edition copy of Silent Spring; on the right in 1967 Britain, Derek Ratcliffe measures eggshell thickness with callipers in a museum collection." + QUAL_TAIL,
             {"kind": "FACT", "label": "DDT magnified 80,000 times", "who_cards": [
                 "Roy Jean Barker (1924–2011) — American entomologist and toxicologist",
                 "Derek Almey Ratcliffe (1929–2005) — British ecologist and ornithologist",
             ], "when_stamp": "1949 · 1958 · 1960 · 27 September 1962 · 1967 · 1972", "timeline_step": "2/3 · 27 September 1962 (Rachel Carson in Silent Spring proves persistent toxins like DDT biomagnify tens of thousands of times up the food chain)", "hold_s": 3.8}),
            ("02_hunt_bischoff_1960_carson_1962_clear_lake_80000x_biomagnification_and_ratcliffe_1967_eggshell_chart", 132.5, 8.0, "E", False, "1960–1962 CLEAR LAKE 80,000× BIOMAGNIFICATION (0.02 PPM WATER → 1,600 PPM GREBES) & 1967 RATCLIFFE EGGSHELL THINNING", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked Hunt & Bischoff (1960) & Rachel Carson (27 September 1962 Silent Spring) Clear Lake inverted biomagnification pyramid (0.02 ppm water → 5 ppm plankton → 40–300 ppm fish → 1,600 ppm western grebe fat = 80,000x amplification) & Derek Ratcliffe (1967 Nature 215: 208–210) raptor eggshell-thinning curve.",
             {"kind": "DATA", "label": "1960–1962 CLEAR LAKE 80,000× BIOMAGNIFICATION PYRAMID (0.02 → 5 → 300 → 1,600 PPM) & 1967 RATCLIFFE EGGSHELL CHART", "detail": "Inked Hunt & Bischoff (1960) & Rachel Carson (27 September 1962 Silent Spring) Clear Lake inverted biomagnification pyramid (0.02 ppm water → 5 ppm plankton → 40–300 ppm fish → 1,600 ppm western grebe fat = 80,000x amplification) & Derek Ratcliffe (1967 Nature 215: 208–210) raptor eggshell-thinning curve on period paper", "scale": "two parts per hundred million of insecticide in lake water is like two drops of ink in an Olympic swimming pool — yet by the time that water climbed four steps up the food chain, the poison had concentrated eighty thousand times inside the birds at the top", "hold_s": 3.8}),
            ("03_silver_spring_27_sep_1962_silent_spring_first_edition_and_ratcliffe_1967_nature_callipers_closeup", 140.5, 6.5, "B", False, "27 SEPTEMBER 1962 — CARSON'S SILENT SPRING", "Fast",
             "Fast: daylight macro shot of a first-edition copy of Rachel Carson's 27 September 1962 book Silent Spring beside Derek Ratcliffe's 1967 Nature paper and brass eggshell callipers on a desk. Nothing emissive, no face.",
             STYLE + "In crisp daylight on a study desk, a 1962 yellow-jacketed hardcover copy of Silent Spring sits beside an open 1967 scientific journal, brass callipers, and field notebooks." + FAST_TAIL,
             None),
            ("04_explorer_watching_persistent_red_ddt_markers_funnel_and_pack_into_top_predator_at_pyramid_apex", 147.0, 5.5, "B", True, None, "Quality",
             "Quality: Explorer beat 2 (locked character reference).",
             STYLE + "Standing beside a four-tier sculpted trophic pyramid where green food beads drop away by ninety percent at each step from plankton to minnows to large fish to an osprey at the top, the Explorer traces how persistent red chemical beads refuse to wash out and crowd tightly into the single bird at the apex." + EXP_TAIL,
             None),
        ],
    ),
    (
        5,
        "Part 05 — The Keystone at the Top of the Arch — & How a Robot Bee Cracked the Waggle Dance Code",
        [
            ("01_timeline_1927_1995_and_food_webs_10_percent_law_biomagnification_keystone_species_chart", 152.5, 8.5, "E", False, "1927–1995 TIMELINE · ELTON FOOD WEBS, LINDEMAN 10% LAW, CARSON BIOMAGNIFICATION & PAINE KEYSTONE SPECIES", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, the 3-era timeline completes: 1927 & October 1942 (Charles Elton maps Arctic food webs and the Pyramid of Numbers, and Raymond Lindeman at Cedar Bog Lake proves the 10% trophic energy law) · 27 September 1962 (Rachel Carson in Silent Spring proves persistent toxins like DDT biomagnify tens of thousands of times up the food chain) · June 1963–1969 & 1974–1995 (Robert Paine pries Pisaster starfish off Mukkaw Bay rocks to discover keystone species and trophic cascades, followed by James Estes's sea otters and Yellowstone's wolves).",
             {"kind": "DATA", "label": "1927–1995 FOOD WEBS, 10% LAW & KEYSTONE SPECIES TIMELINE · ELTON, LINDEMAN, CARSON, PAINE & ESTES", "detail": "Animated timeline (1927 → 1995) alongside an inked summary of food webs, the 10% trophic energy pyramid, biomagnification, and keystone species", "scale": "from an Arctic island and a Minnesota bog to a crowbar on a Washington tidepool, scientists discovered that the rarest creatures at the top of the food chain are the keystones holding the living world together", "when_stamp": "1927–1995", "timeline_step": "3/3 · 1927–1995 timeline complete", "hold_s": 3.8}),
            ("02_keystone_starfish_arch_and_10_percent_pyramid_beside_glass_beehive_and_brass_robot_bee_on_plinth_pan", 161.0, 5.5, "A", False, "FOOD WEBS, 10% LAW & KEYSTONE SPECIES", "Fast",
             "Fast: daylight close-up of a sculpted stone arch with a purple starfish keystone and a 4-tier energy pyramid beside a wooden glass-walled observation beehive and a miniature brass-and-wax mechanical robot bee on a museum plinth. Nothing emissive, no face.",
             STYLE + "In crisp daylight on a wooden museum plinth, a stone arch crowned by a purple starfish keystone sits beside a glass-walled wooden observation beehive and a miniature brass-and-wax mechanical bee." + FAST_TAIL,
             None),
            ("03_karl_von_frisch_1945_painted_bees_martin_lindauer_1951_and_axel_michelsen_1989_robot_bee_handoff", 166.5, 6.5, "C", False, "PAINTED BEES, WAGGLE DANCE & ROBOT BEE", "Quality",
             "Quality: readable faces (Karl von Frisch in Munich and Brunnwinkl in 1944–1946 watching paint-numbered honeybees dance a figure-eight waggle dance inside a glass observation hive, Martin Lindauer in 1951 mapping swarm democracy, and Axel Michelsen, Wolfgang Kirchner, and Martin Lindauer in 1989 operating a computer-controlled brass-and-wax mechanical robot bee inside a dark hive — handoff to 089 Honeybee Waggle Dance & Robot Bee).",
             STYLE + "Split period scene: on the left in 1945 Austria, Karl von Frisch times paint-numbered honeybees dancing a figure-eight pattern inside a glass observation hive; on the right in 1989, Axel Michelsen and Martin Lindauer guide a miniature brass-and-wax mechanical robot bee on a honeycomb." + QUAL_TAIL,
             {"kind": "WHEN", "label": "1944 · 1946 · 1951 · 1989", "hold_s": 3.5}),
            ("04_table_three_callback", 173.0, 2.4, "C", False, None, "reuse",
             "Reuse: verified unused moving window [5.50s..7.90s] of P1:07_table_three_props_1942_plankton_net_jar_1962_silent_spring_book_and_1963_crowbar_starfish_arch (callback, £0).",
             "Reuse P1:07_table_three_props_1942_plankton_net_jar_1962_silent_spring_book_and_1963_crowbar_starfish_arch [5.50s..7.90s] (2.40s distinct non-overlapping tail window from 8.00s source clip).",
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
                row["reuse_of"] = "P1:07_table_three_props_1942_plankton_net_jar_1962_silent_spring_book_and_1963_crowbar_starfish_arch"
                row["reuse_window_s"] = [5.5, 7.9]
                row["reuse_audit"] = {
                    "source_row": "P1:07_table_three_props_1942_plankton_net_jar_1962_silent_spring_book_and_1963_crowbar_starfish_arch",
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
            "film": "088_Elton-Lindeman-Carson-Paine-Food-Webs-Keystone-Species",
            "part": p_idx,
            "title": p_title,
            "version": "v01",
            "timing_status": "pre_vo_script_clock (built from food_webs_keystone_script_master_v01.md; retimes onto Scribe STT once VO locks)",
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
        "film": "088_Elton-Lindeman-Carson-Paine-Food-Webs-Keystone-Species",
        "version": "v01",
        "date": "2026-10-21",
        "owner": "gemini (J0805)",
        "status": "PRE_VO_BOARDS_V01_NO_MINT",
        "generation_authorized": False,
        "script": "00_Brand/Channel-Setup/ideas/088_Elton-Lindeman-Carson-Paine-Food-Webs-Keystone-Species/food_webs_keystone_script_master_v01.md",
        "sources": "00_Brand/Channel-Setup/ideas/088_Elton-Lindeman-Carson-Paine-Food-Webs-Keystone-Species/SOURCES_v01.md",
        "credit_snapshot": {
            "flow_balance": 23740,
            "flow_floor": 0,
            "flow_read_at": "2026-10-15T21:42:22Z",
            "vertex_promo_gbp": 71.02,
            "vertex_usable_gbp": 70.02,
        },
        "totals": totals,
        "per_part": per_part_summary,
        "mint_order": "006 > 007 > 008 > 009 > 010 > 011 > 012 > 013 > 014 > 015 > 016 > 017 > 018 > 019 > 020 > 021 > 022 > 023 > 024 > 025 > 026 > 027 > 028 > 029 > 030 > 031 > 032 > 033 > 034 > 035 > 036 > 037 > 038 > 039 > 040 > 041 > 042 > 043 > 044 > 045 > 046 > 047 > 048 > 049 > 050 > 051 > 052 > 053 > 054 > 055 > 056 > 057 > 058 > 059 > 060 > 061 > 062 > 063 > 064 > 065 > 066 > 067 > 068 > 069 > 070 > 071 > 072 > 073 > 074 > 075 > 076 > 077 > 078 > 079 > 080 > 081 > 082 > 083 > 084 > 085 > 086 > 087 > 088 > 089 > 090 > 091 > 092 > 093 > 094 > 095. Nothing in 088 is generation_authorized.",
    }
    (EDIT / "PICTURE_PLAN_v01.json").write_text(json.dumps(plan, indent=2) + "\n")

    sl = [
        "# 088 Keystone Species: The Starfish Experiment That Shocked Ecology — Shot list & plate boards v01 (pre-VO)",
        "",
        "Gemini, 21 Oct 2026, J0805. Built from `food_webs_keystone_script_master_v01.md` (`90.8/100 PASS`) and `SOURCES_v01.md`.",
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
        "# 088 price review v01 (pre-VO plate boards)",
        "",
        "Gemini, 21 Oct 2026, J0805. Boards only. **No mint. No spend. No merge.**",
        "Prepared from `food_webs_keystone_script_master_v01.md` (`90.8/100 PASS`) and `SOURCES_v01.md` so 088's full plate board rows, non-emissive Fast prompts, £0 code graphics, and Teach-on-Screen overlays are ready to re-time the moment long VO locks. Parked for Chief.",
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
        f"- **Quality ({totals['Quality']} rows):** readable faces (Charles Sutherland Elton, Raymond Laurel Lindeman, Eleanor Hall Lindeman, George Evelyn Hutchinson, Robert Treat Paine III, James A. Estes, Roy Jean Barker, Rachel Louise Carson, Derek Almey Ratcliffe, Karl von Frisch, Martin Lindauer, Axel Michelsen), 1927 Oxford Arctic food webs & October 1942 Cedar Bog Lake `10% trophic energy law`, June 1963 Mukkaw Bay `keystone species` starfish removal & 1974 sea-otter kelp cascade, 27 September 1962 *Silent Spring* `80,000×` DDT biomagnification & 1967 eggshell thinning, and the 2 Explorer beats.",
        f"- **Fast ({totals['Fast']} rows, non-emissive):** daylight prop and laboratory shots (Elton's 1927 *Animal Ecology*, 1942 *Ecology* journal & purple starfish / crowbar pan, 3-object callback bench, 1927 *Animal Ecology* & October 1942 *Ecology* paper with Cedar Bog Lake sample vials, 4-step wooden trophic energy pyramid demonstrator, Paine's 1966 & 1969 *American Naturalist* papers with *Pisaster* starfish & mussel shells, two-sided intertidal tidepool diorama comparing 15-species plot vs mussel monoculture, 1962 *Silent Spring* first edition with Ratcliffe's 1967 *Nature* paper & brass eggshell callipers, keystone starfish arch beside glass observation beehive & brass robot bee on museum plinth). Zero candles, flames, sparks, or glowing elements on Fast.",
        f"- **£0 code graphics ({totals['code_graphic']} rows):**",
        "  1. `P1:04_elton_1927_lindeman_1942_10_percent_energy_pyramid_and_carson_1962_80000x_biomagnification_chart` — Raymond Lindeman (1942) Cedar Bog Lake `~10%` trophic energy transfer pyramid & Rachel Carson (1962) Clear Lake `80,000×` DDT biomagnification curve (`SCALE: because ninety percent of all food energy burns away as body heat at every step up the food chain, it takes ten thousand kilograms of grass to feed one thousand kilograms of rabbits, to feed one hundred kilograms of foxes, to keep a single ten-kilogram golden eagle alive`)",
        "  2. `P1:06_paine_1966_1969_mukkaw_bay_pisaster_removal_15_to_1_species_diversity_crash_chart` — Robert Paine (1966 & 1969 *Am. Nat.*) Mukkaw Bay *Pisaster* starfish removal & `15 → 8 → 1` intertidal species diversity crash (`SCALE: a single purple starfish weighs less than a bag of sugar, yet by eating the bully mussel that would otherwise hog every square centimetre of rock, that one predator keeps fourteen other species of sea life alive`)",
        "  3. `P2:02_elton_1927_arctic_food_web_and_lindeman_oct_1942_ecology_cedar_bog_lake_10_percent_energy_chart` — Charles Elton (1927 *Animal Ecology*) Arctic Bear Island food web & Raymond Lindeman (October 1942 *Ecology* 23: 399–417) Cedar Bog Lake `cal/cm²/year` `~10%` trophic energy pyramid (`SCALE: if you eat a hundred-calorie steak, the cow had to eat roughly a thousand calories of grass, which had to soak up nearly a million calories of sunshine — meaning ninety percent of the energy is taxed away as heat at every single rung of nature's ladder`)",
        "  4. `P3:02_paine_1966_1969_american_naturalist_mukkaw_bay_food_web_and_estes_1974_sea_otter_kelp_cascade_chart` — Robert Paine (January 1966 & January 1969 *Am. Nat.*) Mukkaw Bay food web & James Estes (1974 *Science* 185: 1058–1060) sea otter → sea urchin → kelp forest trophic cascade (`SCALE: Robert Paine didn't need a particle accelerator or a million-dollar telescope to revolutionize ecology — he just needed a steel crowbar, a pair of rubber boots, and the patience to fling starfish into the waves at low tide`)",
        "  5. `P4:02_hunt_bischoff_1960_carson_1962_clear_lake_80000x_biomagnification_and_ratcliffe_1967_eggshell_chart` — Hunt & Bischoff (1960) & Rachel Carson (27 September 1962 *Silent Spring*) Clear Lake inverted biomagnification pyramid (`0.02 ppm` water → `1,600 ppm` grebes = `80,000×`) & Derek Ratcliffe (1967 *Nature* 215: 208–210) raptor eggshell-thinning curve (`SCALE: two parts per hundred million of insecticide in lake water is like two drops of ink in an Olympic swimming pool — yet by the time that water climbed four steps up the food chain, the poison had concentrated eighty thousand times inside the birds at the top`)",
        "  6. `P5:01_timeline_1927_1995_and_food_webs_10_percent_law_biomagnification_keystone_species_chart` — completed timeline (1927 → 1995) + food webs, the 10% energy law, biomagnification & keystone species (`SCALE: from an Arctic island and a Minnesota bog to a crowbar on a Washington tidepool, scientists discovered that the rarest creatures at the top of the food chain are the keystones holding the living world together`)",
        f"- **£0 verified reuse ({totals['reuse']} row):** `P5:04_table_three_callback` uses the 2.40 s unused moving tail `[5.50s..7.90s]` of `P1:07_table_three_props_1942_plankton_net_jar_1962_silent_spring_book_and_1963_crowbar_starfish_arch`.",
        "",
        "## Mint order",
        "",
        "006 > 007 > 008 > 009 > 010 > 011 > 012 > 013 > 014 > 015 > 016 > 017 > 018 > 019 > 020 > 021 > 022 > 023 > 024 > 025 > 026 > 027 > 028 > 029 > 030 > 031 > 032 > 033 > 034 > 035 > 036 > 037 > 038 > 039 > 040 > 041 > 042 > 043 > 044 > 045 > 046 > 047 > 048 > 049 > 050 > 051 > 052 > 053 > 054 > 055 > 056 > 057 > 058 > 059 > 060 > 061 > 062 > 063 > 064 > 065 > 066 > 067 > 068 > 069 > 070 > 071 > 072 > 073 > 074 > 075 > 076 > 077 > 078 > 079 > 080 > 081 > 082 > 083 > 084 > 085 > 086 > 087 > 088 > 089 > 090 > 091 > 092 > 093 > 094 > 095. `generation_authorized` is `false` on every row.",
    ])
    (EDIT / "PRICE_REVIEW_v01.md").write_text("\n".join(pr_lines) + "\n")
    print(f"088 v01 boards written: {totals['rows']} rows, Flow expected={totals['flow_credits_expected']}")


if __name__ == "__main__":
    main()
