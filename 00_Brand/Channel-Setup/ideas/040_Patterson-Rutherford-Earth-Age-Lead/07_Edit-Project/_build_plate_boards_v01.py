#!/usr/bin/env python3
"""HOS 040 (How Old Is the Earth? The 1953 Lab That Found Lead in Every Breath) pre-VO plate boards v01. J0524. No mint, no spend.

Built from 00_Brand/Channel-Setup/ideas/040_Patterson-Rutherford-Earth-Age-Lead/earth_age_script_master_v01.md
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
        "Part 01 — Pitchblende in London and the Acid-Scrubbed Clean Room in California",
        [
            ("01_patterson_1953_caltech_clean_room_meteorite_and_1965_greenland_ice_trench", 0.0, 5.5, "A", False, "THE METEORITE AND THE POISON", "Quality",
             "Quality: Short frame 0 / answer image (0:03) + inside the world's first positively pressurised acid-scrubbed ultra-clean laboratory at Caltech in 1953, 31-year-old American geochemist Clair Patterson in a plastic clean-suit dissolves a microscopic crystal from the Canyon Diablo iron meteorite in doubly distilled acid, dissolving to a deep snow tunnel in Greenland in 1965 where Patterson cores ancient ice layers.",
             STYLE + "Inside a gleaming 1953 acid-scrubbed clean laboratory at Caltech, thirty-one-year-old geochemist Clair Patterson in a white plastic clean-room hood holds a quartz flask beside a silver-grey iron meteorite fragment, dissolving to a crisp blue snow trench in Greenland where Patterson carves an ancient ice block." + QUAL_TAIL,
             {"kind": "WHEN", "label": "PASADENA, 1953 · GREENLAND, 1965", "timeline_step": "4/5 · Autumn 1953 (Clair Patterson's ultra-clean lab & Canyon Diablo meteorite lock Earth's age at 4.55 billion years) & 5/5 · 1965–1970 (Greenland ice cores expose 200× leaded-petrol spike)", "hold_s": 3.5}),
            ("02_rutherford_1904_pitchblende_patterson_1953_isochron_and_1965_ice_core_split", 5.5, 6.0, "B", False, "PITCHBLENDE, METEORITE, UNLEADED", "Quality",
             "Quality: complex three-part split composition (Ernest Rutherford holding up a black lump of pitchblende uranium ore before Lord Kelvin at the Royal Institution on 20 May 1904 on the left; Clair Patterson's 1953 mass-spectrometer trace of the Canyon Diablo meteorite at 4.55 billion years in the centre; Greenland ice-core snow blocks and an unleaded fuel nozzle on the right).",
             STYLE + "Three-panel period composition: on the left, a dark lump of pitchblende rock held above a polished lecture desk; in the centre, an iron meteorite slice beside a quartz beaker and paper strip chart; on the right, a pristine polar ice core cylinder beside a chrome fuel nozzle." + QUAL_TAIL,
             None),
            ("03_rutherford_20_may_1904_royal_institution_pitchblende_before_kelvin", 11.5, 6.0, "C", False, "TWENTY MAY 1904", "Quality",
             "Quality: readable faces (inside the wood-panelled lecture theatre of the Royal Institution in London on 20 May 1904, 32-year-old Ernest Rutherford holds a dark lump of pitchblende while 79-year-old white-bearded Lord Kelvin wakes up and watches sharply from the front row).",
             STYLE + "Inside the semicircular wood-panelled lecture theatre of the Royal Institution in London on 20 May 1904, thirty-two-year-old Ernest Rutherford in evening dress holds up a black lump of pitchblende while white-bearded Lord Kelvin sits bolt upright in the front row." + QUAL_TAIL,
             {"kind": "WHEN", "label": "LONDON, 20 MAY 1904", "timeline_step": "2/5 · 20 May 1904 (Ernest Rutherford presents radioactive heating and uranium-decay dating at the Royal Institution)", "hold_s": 3.5}),
            ("04_kelvin_20_40m_yr_vs_patterson_1953_canyon_diablo_4_55b_yr_isochron_chart", 17.5, 8.0, "E", False, "KELVIN COOLING LIMIT (20–40M YR) VS PATTERSON 1953 CANYON DIABLO METEORITE (4.55 ± 0.07 BILLION YR)", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked uranium-lead decay and age comparison chart contrasts Lord Kelvin's 1897 cooling limit (20–40 million years) against U-238 → Pb-206 (half-life 4.47 billion years) and U-235 → Pb-207 (half-life 704 million years) converging on Clair Patterson's autumn 1953 Canyon Diablo meteorite isochron at 4.55 billion years (± 70 million years).",
             {"kind": "DATA", "label": "KELVIN LIMIT (20–40M YR) VS PATTERSON 1953 CANYON DIABLO METEORITE (4.55 ± 0.07 BILLION YR)", "detail": "Inked uranium-lead decay & age comparison chart on period paper contrasting Lord Kelvin's 1897 cooling limit (20–40 million years) against uranium-to-lead radiometric dating of the Canyon Diablo meteorite by Clair Patterson in 1953 (4.55 billion years ± 70 million years — more than 100 times older than Kelvin's limit)", "scale": "if the entire four-point-five-five-billion-year history of the Earth were compressed into a single twenty-four-hour day, Lord Kelvin's twenty-million-year planet would have begun at eleven fifty-three at night — just seven minutes before midnight", "who_card": "Ernest Rutherford (1871–1937) — New Zealand-born physicist · William Thomson, Lord Kelvin (1824–1907) — British mathematical physicist · Clair Patterson (1922–1995) — American geochemist", "when_stamp": "20 May 1904 · Autumn 1953", "hold_s": 3.8}),
            ("05_canyon_diablo_iron_meteorite_slice_and_acid_washed_quartz_beaker_pan", 25.5, 5.5, "A", False, "CALTECH CLEAN LAB, 1953", "Fast",
             "Fast: daylight macro pan across a polished Widmanstätten-patterned slice of the Canyon Diablo iron meteorite and an acid-washed quartz beaker on a clean bench between code graphics so two full-frame graphics never run back to back. Nothing emissive, no face.",
             STYLE + "In crisp daylight on a spotless white laboratory bench, the camera pans across a polished slice of iron-nickel meteorite showing geometric crystalline patterns beside a clear quartz beaker." + FAST_TAIL,
             None),
            ("06_lead_contamination_scale_bar_prehistoric_1x_vs_1965_ice_and_lab_200x_chart", 31.0, 8.0, "E", False, "4.55 BILLION YEARS", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period parchment, an inked lead-contamination bar chart compares prehistoric natural lead levels in Greenland ice and deep-ocean water (1× baseline, <0.001 µg/kg snow) against post-1923 leaded-gasoline atmospheric fallout (~100–200× higher in 1965 ice cores and 200× in ordinary lab dust).",
             {"kind": "DATA", "label": "PREHISTORIC NATURAL LEAD (1×, <0.001 µG/KG ICE) VS POST-1923 LEADED PETROL SPIKE (200× HIGHER)", "detail": "Inked lead-contamination bar chart comparing prehistoric natural lead levels in Greenland ice and deep-ocean water (1× baseline, <0.001 µg/kg snow) against post-1923 leaded-gasoline atmospheric fallout (~100–200× higher in 1965 ice cores and 200× in lab dust)", "scale": "every single year by the nineteen sixties, car exhaust pipes were spraying hundreds of thousands of tonnes of microscopic lead dust into the sky — coating every leaf, snowdrift, and laboratory bench on Earth", "hold_s": 3.8}),
            ("07_table_three_props_pitchblende_canyon_diablo_meteorite_and_teflon_ice_bottle", 39.0, 5.5, "C", False, "1904 TO 1965", "Fast",
             "Fast: daylight prop table (callback source for Part 05: Ernest Rutherford's black pitchblende specimen, Clair Patterson's Canyon Diablo iron meteorite fragment in a quartz dish, and an acid-washed Teflon sample bottle from Greenland). Nothing emissive.",
             STYLE + "On an oak workbench in soft window light sit three objects side by side: a dark mineral lump of pitchblende, a metallic fragment of the Canyon Diablo meteorite in a clear quartz dish, and a white sample bottle beside a brass core tube." + FAST_TAIL,
             None),
            ("08_explorer_clean_suit_dusting_uranium_to_lead_hourglass_with_feather_duster", 62.0, 5.5, "A", True, None, "Quality",
             "Quality: Explorer beat 1 (locked character reference, after 1:00).",
             STYLE + "Wearing a translucent clean-room hood over the teal coat and holding a brass hourglass where green mineral grains trickle steadily into silver lead grains at the bottom, the Explorer uses a miniature feather duster to sweep grey soot specks off the outside glass." + EXP_TAIL,
             None),
            ("09_patterson_autumn_1953_argonne_mass_spectrometer_strip_chart_4_55_billion_years", 67.5, 5.5, "B", False, "ARGONNE LAB, 1953", "Quality",
             "Quality: readable face (in autumn 1953 inside the mass-spectrometer room at Argonne National Laboratory in Illinois, 31-year-old Clair Patterson stares in awe at the paper chart recorder as the lead-isotope peaks lock onto 4.55 billion years).",
             STYLE + "Inside the 1953 mass-spectrometer room at Argonne National Laboratory, thirty-one-year-old Clair Patterson leans over a brass strip-chart recorder with wide-eyed astonishment as an ink pen traces sharp peaks on a paper roll." + QUAL_TAIL,
             None),
        ],
    ),
    (
        2,
        "Part 02 — Lord Kelvin's Cooling Iron Globe & Rutherford's 20 May 1904 Royal Institution Gambit",
        [
            ("01_kelvin_1862_glasgow_cooling_globe_and_rutherford_1904_royal_institution", 73.0, 6.5, "A", False, "KELVIN DOZED IN ROW ONE", "Quality",
             "Quality: readable faces (Lord Kelvin calculating the cooling rate of a globe in Glasgow in 1862–1897, dissolving to 32-year-old Ernest Rutherford holding up black pitchblende before Lord Kelvin at the Royal Institution on 20 May 1904).",
             STYLE + "Split period scene: on the left in Glasgow, white-bearded Lord Kelvin measures a suspended iron sphere with a thermometer beside a chalkboard; on the right in London on 20 May 1904, young Ernest Rutherford holds up a dark lump of pitchblende as Lord Kelvin smiles from the front row." + QUAL_TAIL,
             {"kind": "WHO", "label": "Arthur Holmes (1890–1965) — English geologist", "fact_card": "Kelvin dozed in row one", "when_stamp": "1862 · 1897 · 20 May 1904 · 1907 · 1913", "timeline_step": "1/5 · 1862–1897 (Lord Kelvin calculates a 20–40 million year cooling Earth) & 3/5 · 1907–1913 (Boltwood & Holmes date rocks past 1.6 billion years)", "hold_s": 3.8}),
            ("02_kelvin_cooling_curve_vs_rutherford_radiogenic_heat_and_u238_4_47b_yr_chart", 79.5, 8.0, "E", False, "KELVIN COOLING CURVE (20–40M YR) VS RADIOGENIC HEAT & U-238 HALF-LIFE (4.47 BILLION YR)", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked cooling-curve vs radioactive-furnace chart compares Lord Kelvin's 1862–1897 conductive cooling curve (20–40 million years without internal heat) against Earth's radiogenic heat and U-238 → Pb-206 half-life clock (4.47 billion years, with Boltwood 1907 & Holmes 1913 dating ancient rocks to 1.6 billion years).",
             {"kind": "DATA", "label": "KELVIN COOLING (20–40M YR) VS U-238 → PB-206 HALF-LIFE (4.47B YR) & HOLMES 1913 ROCKS (1.6B YR)", "detail": "Inked cooling-curve vs radioactive-furnace chart on period paper comparing Lord Kelvin's 1862–1897 conductive cooling curve (cooling to present geothermal gradient in 20–40 million years without internal heat) against Earth's radiogenic heat and U-238 → Pb-206 half-life clock (4.47 billion years, Boltwood 1907 & Holmes 1913 rocks at 1.6 billion years)", "scale": "half of all the Uranium-238 atoms sealed inside a crystal when the Earth formed four and a half billion years ago have only just finished ticking over into lead today", "hold_s": 3.8}),
            ("03_pitchblende_mineral_zircon_crystal_and_holmes_1913_book_bench_pan", 87.5, 6.5, "B", False, "20 MAY 1904 — ATOMIC HOURGLASS", "Fast",
             "Fast: daylight close-up of Ernest Rutherford's black pitchblende specimen beside a glass vial of lead grains and Arthur Holmes's 1913 'The Age of the Earth' on a lecture bench. Nothing emissive, no face.",
             STYLE + "In crisp daylight on a polished wooden lecture bench, the camera pans across a dark mineral specimen of pitchblende, a glass vial of silvery lead pellets, and a cloth-bound geological treatise." + FAST_TAIL,
             None),
            ("04_brass_electroscope_and_rock_strata_core_specimens_daylight", 94.0, 5.5, "C", False, "1.6 BILLION YEARS, 1913", "Fast",
             "Fast: daylight macro shot of a brass gold-leaf electroscope beside labelled trays of ancient Precambrian rock cores and zircon crystals on an Edwardian geology table. Nothing emissive, no face.",
             STYLE + "In bright window light on a geology table, a brass cylindrical electroscope stands beside a wooden tray holding layered granite rock cores and a brass magnifying lens." + FAST_TAIL,
             None),
        ],
    ),
    (
        3,
        "Part 03 — 'Duck Soup,' Mysterious Lead & Clair Patterson's Ultra-Clean Room (1948–1953) — Midpoint Twist",
        [
            ("01_harrison_brown_1948_chicago_and_patterson_1952_caltech_acid_clean_room", 99.5, 6.5, "A", False, "THOUGHT HE HAD A HEART ATTACK", "Quality",
             "Quality: readable faces (geochemist Harrison Brown at the University of Chicago in 1948 handing a zircon crystal and Canyon Diablo meteorite fragment to 26-year-old Clair Patterson, dissolving to Patterson in a plastic clean-suit hood scrubbing quartz beakers in acid at Caltech in 1952–1953).",
             STYLE + "Split period scene: on the left in a 1948 Chicago laboratory, Harrison Brown hands a small iron meteorite fragment in tweezers to twenty-six-year-old Clair Patterson; on the right at Caltech in 1953, Patterson in a plastic clean-room hood rinses a clear quartz flask inside a sealed glass hood." + QUAL_TAIL,
             {"kind": "WHO", "label": "Harrison Brown (1917–1986) — American geochemist", "fact_card": "Thought he had a heart attack", "when_stamp": "1948 · 1952 · Autumn 1953 · 1956", "timeline_step": "4/5 · Autumn 1953 (Clair Patterson's ultra-clean lab & Canyon Diablo meteorite lock Earth's age at 4.55 billion years)", "hold_s": 3.8}),
            ("02_patterson_1953_1956_canyon_diablo_lead_isochron_4_55_billion_years_chart", 106.0, 8.0, "E", False, "1953/1956 PATTERSON LEAD-LEAD ISOCHRON: CANYON DIABLO TROILITE → 4.55 ± 0.07 BILLION YEARS", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked lead-lead isochron chart from Clair Patterson's 1953/1956 paper plots Pb-207/Pb-204 vs Pb-206/Pb-204 from the Canyon Diablo iron meteorite (primordial baseline) through stony meteorites and Pacific deep-sea sediment to lock the slope at 4.55 ± 0.07 billion years.",
             {"kind": "DATA", "label": "PATTERSON 1953/1956 LEAD-LEAD ISOCHRON: 4.55 ± 0.07 BILLION YEARS (SUB-0.1 MICROGRAM BLANK)", "detail": "Inked lead-lead isochron chart on period paper from Clair Patterson's 1953/1956 paper plotting Pb-207/Pb-204 vs Pb-206/Pb-204 from the Canyon Diablo iron meteorite (primordial baseline) through stony meteorites and Pacific deep-sea sediment to lock the slope at 4.55 ± 0.07 billion years", "scale": "to read that four-point-five-five-billion-year clock, Patterson had to scrub his laboratory until stray lead dust fell below a tenth of a millionth of a gram — smaller than a single speck of flour", "hold_s": 3.8}),
            ("03_patterson_autumn_1953_argonne_mass_spectrometer_console_and_chart", 114.0, 6.5, "B", False, "AUTUMN 1953 — 4.55 BILLION YEARS", "Quality",
             "Quality: readable face (in autumn 1953 at Argonne National Laboratory in Illinois, Clair Patterson watches the mass-spectrometer strip-chart pen trace the Canyon Diablo lead peaks locking 4.55 billion years).",
             STYLE + "Beside a tall steel mass-spectrometer magnet frame in autumn 1953, Clair Patterson holds a strip-chart printout and calculates with a slide rule at a wooden desk." + QUAL_TAIL,
             None),
            ("04_caltech_positive_pressure_air_filter_and_quartz_acid_still_closeup", 120.5, 5.5, "C", False, "FIRST ULTRA-CLEAN ROOM", "Fast",
             "Fast: daylight close-up of Clair Patterson's 1952 Caltech ultra-clean room apparatus: a doubly distilled quartz acid still and a sealed plastic air-filter duct on a spotless polyethylene bench. Nothing emissive, no face.",
             STYLE + "In crisp daylight inside a spotless white-walled clean room, clear liquid drips slowly through a curved quartz distillation tube into a sealed quartz flask." + FAST_TAIL,
             None),
        ],
    ),
    (
        4,
        "Part 04 — Deep Oceans, Greenland Ice Cores & the Poison in Every Car Tailpipe",
        [
            ("01_patterson_1963_ocean_sampler_and_1965_camp_century_greenland_ice_trench", 126.0, 6.5, "A", False, "200X MORE LEAD IN SNOW", "Quality",
             "Quality: readable face (Clair Patterson in a plastic clean-suit hood over his winter parka carving pristine ancient snow blocks inside a deep ice trench at Camp Century, Greenland, in 1965).",
             STYLE + "Inside a deep snow trench in Greenland in 1965, geochemist Clair Patterson wearing a clear plastic clean-suit hood over a heavy winter parka uses an acid-cleaned saw to carve a pristine block of ancient polar ice." + QUAL_TAIL,
             {"kind": "WHO", "label": "Thomas Midgley Jr. (1889–1944) — American engineer and chemist", "fact_card": "200x more lead in snow", "when_stamp": "1923 · 1963 · 1965 · 1969", "hold_s": 3.8}),
            ("02_greenland_ice_core_800bc_to_1965_200x_lead_spike_chart", 132.5, 8.0, "E", False, "GREENLAND ICE CORES (800 BC TO 1965): <0.001 µG/KG PREHISTORIC → >0.20 µG/KG (>200× SPIKE AFTER 1923)", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked Greenland ice-core timeline graph from Murozumi, Chow & Patterson (1965–1969) plots lead concentration in Greenland snow layers from 800 BC (~0.001 µg Pb/kg ice) through 1750 (~0.01 µg/kg) and 1923 (introduction of tetraethyl lead in petrol) to 1965 (>0.20 µg/kg — a >200-fold increase).",
             {"kind": "DATA", "label": "GREENLAND ICE CORES (800 BC–1965): <0.001 µG/KG NATURAL BASELINE TO >0.20 µG/KG (>200× SPIKE)", "detail": "Inked Greenland ice-core timeline graph on period paper from Murozumi, Chow & Patterson (1965–1969) plotting lead concentration in Greenland snow layers from 800 BC (~0.001 µg Pb/kg ice) through 1750 (~0.01 µg/kg) and 1923 (introduction of tetraethyl lead in petrol) to 1965 (>0.20 µg/kg — a >200-fold increase)", "scale": "a single tank of nineteen-sixties leaded petrol puffed more than thirty grams of pure toxic lead dust out of the tailpipe and straight into city air", "hold_s": 3.8}),
            ("03_melted_greenland_ice_samples_in_teflon_bottles_and_1965_paper_closeup", 140.5, 6.5, "B", False, "GREENLAND, 1965 — THE ICE RECORD", "Fast",
             "Fast: daylight close-up of melted Greenland ice samples in acid-washed translucent Teflon bottles beside a Cylindrical polar ice core section on a clean bench. Nothing emissive, no face.",
             STYLE + "In bright daylight inside a clean laboratory hood, three translucent white sample bottles sit beside a clear glass cylinder holding a pristine section of polar snow." + FAST_TAIL,
             None),
            ("04_explorer_in_parka_magnifying_ancient_ice_layers_with_1923_soot_band", 147.0, 5.5, "B", True, None, "Quality",
             "Quality: Explorer beat 2 (locked character reference).",
             STYLE + "Wearing a white winter parka trim over the teal coat inside a crisp blue polar snow trench, the Explorer slides a brass magnifying glass up a tall transparent column of ice layers that shine crystal-clear at the bottom before a dark grey band of exhaust dust clouds the top." + EXP_TAIL,
             None),
        ],
    ),
    (
        5,
        "Part 05 — The Scientist Who Refused to Yield & the Willow Bark That Became Aspirin",
        [
            ("01_timeline_1862_1970_and_80_percent_blood_lead_drop_chart", 152.5, 8.5, "E", False, "1862–1970 TIMELINE · >80% DROP IN CHILDREN'S BLOOD LEAD AFTER UNLEADED PETROL", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, the 5-date timeline completes: 1862–1897 (Lord Kelvin calculates a 20–40 million year cooling Earth) · 20 May 1904 (Ernest Rutherford presents radioactive heating and uranium-decay dating at the Royal Institution) · 1907–1913 (Bertram Boltwood & Arthur Holmes date rocks past 1.6 billion years) · Autumn 1953 (Clair Patterson's ultra-clean lab & Canyon Diablo meteorite lock Earth's age at 4.55 billion years) · 1965–1970 (Patterson's Greenland ice cores expose a 200× leaded-petrol spike and drive the Clean Air Act, cutting children's blood lead by >80%).",
             {"kind": "DATA", "label": "1862–1970 TIMELINE & >80% DROP IN CHILDREN'S BLOOD LEAD AFTER UNLEADED PETROL", "detail": "Animated 5-date timeline (1862–1897 → 1965–1970) alongside the 500–1,000× bone-lead enrichment in 1960s industrial humans and the >80% decline in children's blood-lead levels after the phase-out of leaded petrol", "scale": "within twenty years of switching petrol pumps to unleaded fuel, the amount of toxic lead circulating in children's bloodstreams dropped by more than four-fifths across the world", "fact_card": "Cut blood lead by 80%", "when_stamp": "September 1965 · June 1966 · 1970 · 1862–1970", "timeline_step": "5/5 · 1965–1970 (Patterson's Greenland ice cores expose a 200× leaded-petrol spike and drive the Clean Air Act, cutting children's blood lead by >80%)", "hold_s": 3.8}),
            ("02_prehistoric_bone_sample_vs_unleaded_fuel_nozzle_comparison_bench", 161.0, 5.5, "A", False, "OVER 80% DROP IN BLOOD LEAD", "Fast",
             "Fast: daylight side-by-side comparison on a museum bench showing an ancient Peruvian ceramic vessel and bone specimen inside a glass case beside a clean chrome unleaded fuel nozzle and catalytic converter cutaway. Nothing emissive, no face.",
             STYLE + "In crisp daylight on a display bench, a glass museum case holding an ancient Andean ceramic vessel sits beside a polished chrome fuel nozzle and a cutaway honeycomb catalytic filter." + FAST_TAIL,
             None),
            ("03_edward_stone_1763_willow_bark_and_felix_hoffmann_1897_aspirin_handoff", 166.5, 6.5, "C", False, "WILLOW BARK TO ASPIRIN", "Quality",
             "Quality: readable faces (Reverend Edward Stone on an Oxfordshire riverbank in 1763 tasting bitter white willow bark, beside 29-year-old chemist Felix Hoffmann in the Friedrich Bayer laboratory in Elberfeld on 10 August 1897 crystallising pure acetylsalicylic acid — handoff to 041 Aspirin & Painkillers).",
             STYLE + "Split period scene: on the left by an Oxfordshire river in 1763, country vicar Edward Stone holds a strip of pale willow bark beside a willow tree; on the right in an 1897 German laboratory, young chemist Felix Hoffmann holds up a glass flask of gleaming white acetylsalicylic acid crystals." + QUAL_TAIL,
             {"kind": "WHEN", "label": "25 APRIL 1763 · 10 AUGUST 1897 · 1971", "hold_s": 3.5}),
            ("04_table_three_callback", 173.0, 2.4, "C", False, None, "reuse",
             "Reuse: verified unused moving window [5.50s..7.90s] of P1:07_table_three_props_pitchblende_canyon_diablo_meteorite_and_teflon_ice_bottle (callback, £0).",
             "Reuse P1:07_table_three_props_pitchblende_canyon_diablo_meteorite_and_teflon_ice_bottle [5.50s..7.90s] (2.40s distinct non-overlapping tail window from 8.00s source clip).",
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
                row["reuse_of"] = "P1:07_table_three_props_pitchblende_canyon_diablo_meteorite_and_teflon_ice_bottle"
                row["reuse_window_s"] = [5.5, 7.9]
                row["reuse_audit"] = {
                    "source_row": "P1:07_table_three_props_pitchblende_canyon_diablo_meteorite_and_teflon_ice_bottle",
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
            "film": "040_Patterson-Rutherford-Earth-Age-Lead",
            "part": p_idx,
            "title": p_title,
            "version": "v01",
            "timing_status": "pre_vo_script_clock (built from earth_age_script_master_v01.md; retimes onto Scribe STT once VO locks)",
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
        "film": "040_Patterson-Rutherford-Earth-Age-Lead",
        "version": "v01",
        "date": "2026-10-18",
        "owner": "gemini (J0524)",
        "status": "PRE_VO_BOARDS_V01_NO_MINT",
        "generation_authorized": False,
        "script": "00_Brand/Channel-Setup/ideas/040_Patterson-Rutherford-Earth-Age-Lead/earth_age_script_master_v01.md",
        "sources": "00_Brand/Channel-Setup/ideas/040_Patterson-Rutherford-Earth-Age-Lead/SOURCES_v01.md",
        "credit_snapshot": {
            "flow_balance": 23740,
            "flow_floor": 0,
            "flow_read_at": "2026-10-15T21:42:22Z",
            "vertex_promo_gbp": 71.02,
            "vertex_usable_gbp": 70.02,
        },
        "totals": totals,
        "per_part": per_part_summary,
        "mint_order": "006 > 007 > 008 > 009 > 010 > 011 > 012 > 013 > 014 > 015 > 016 > 017 > 018 > 019 > 020 > 021 > 022 > 023 > 024 > 025 > 026 > 027 > 028 > 029 > 030 > 031 > 032 > 033 > 034 > 035 > 036 > 037 > 038 > 039 > 040. Nothing in 040 is generation_authorized.",
    }
    (EDIT / "PICTURE_PLAN_v01.json").write_text(json.dumps(plan, indent=2) + "\n")

    sl = [
        "# 040 How Old Is the Earth? The 1953 Lab That Found Lead in Every Breath — Shot list & plate boards v01 (pre-VO)",
        "",
        "Gemini, 18 Oct 2026, J0524. Built from `earth_age_script_master_v01.md` (`93.4 PASS`) and `SOURCES_v01.md`.",
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
        "# 040 price review v01 (pre-VO plate boards)",
        "",
        "Gemini, 18 Oct 2026, J0524. Boards only. **No mint. No spend. No merge.**",
        "Prepared from `earth_age_script_master_v01.md` (`93.4 PASS`) and `SOURCES_v01.md` so 040's full plate board rows, non-emissive Fast prompts, £0 code graphics, and Teach-on-Screen overlays are ready to re-time the moment long VO locks. Parked for Chief.",
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
        f"- **Quality ({totals['Quality']} rows):** readable faces (Clair Patterson, Ernest Rutherford, Lord Kelvin, Harrison Brown, Reverend Edward Stone, Felix Hoffmann), 1904 Royal Institution lecture theatre, 1953 Caltech ultra-clean lab & Argonne mass spectrometer, 1965 Greenland snow trench, and the 2 Explorer beats.",
        f"- **Fast ({totals['Fast']} rows, non-emissive):** daylight prop and laboratory shots (Canyon Diablo iron meteorite slice & acid-washed quartz beaker pan, 3-object callback bench, pitchblende specimen & lead pellets with Holmes's 1913 treatise, brass electroscope & Precambrian rock cores, Caltech quartz acid still in daylight, melted Greenland ice samples in Teflon bottles, ancient Peruvian vessel vs chrome unleaded nozzle). Zero candles, flames, sparks, or glowing elements on Fast.",
        f"- **£0 code graphics ({totals['code_graphic']} rows):**",
        "  1. `P1:04_kelvin_20_40m_yr_vs_patterson_1953_canyon_diablo_4_55b_yr_isochron_chart` — Lord Kelvin's 1897 cooling limit (20–40 million yr) vs Clair Patterson's 1953 Canyon Diablo meteorite U–Pb age (4.55 ± 0.07 billion yr) (`SCALE: if the entire four-point-five-five-billion-year history of the Earth were compressed into a single twenty-four-hour day, Lord Kelvin's twenty-million-year planet would have begun at eleven fifty-three at night — just seven minutes before midnight`)",
        "  2. `P1:06_lead_contamination_scale_bar_prehistoric_1x_vs_1965_ice_and_lab_200x_chart` — prehistoric natural lead baseline (1×, <0.001 µg/kg snow) vs post-1923 leaded-petrol fallout (~100–200× higher in 1965 Greenland ice cores and 200× in lab dust) (`SCALE: every single year by the nineteen sixties, car exhaust pipes were spraying hundreds of thousands of tonnes of microscopic lead dust into the sky — coating every leaf, snowdrift, and laboratory bench on Earth`)",
        "  3. `P2:02_kelvin_cooling_curve_vs_rutherford_radiogenic_heat_and_u238_4_47b_yr_chart` — Lord Kelvin's 1862–1897 conductive cooling curve vs Earth's radiogenic heat and U-238 → Pb-206 half-life clock (4.47 billion yr; Boltwood 1907 & Holmes 1913 rocks at 1.6 billion yr) (`SCALE: half of all the Uranium-238 atoms sealed inside a crystal when the Earth formed four and a half billion years ago have only just finished ticking over into lead today`)",
        "  4. `P3:02_patterson_1953_1956_canyon_diablo_lead_isochron_4_55_billion_years_chart` — Clair Patterson's 1953/1956 Pb-207/Pb-204 vs Pb-206/Pb-204 isochron from the Canyon Diablo iron meteorite locking 4.55 ± 0.07 billion years (`SCALE: to read that four-point-five-five-billion-year clock, Patterson had to scrub his laboratory until stray lead dust fell below a tenth of a millionth of a gram — smaller than a single speck of flour`)",
        "  5. `P4:02_greenland_ice_core_800bc_to_1965_200x_lead_spike_chart` — Murozumi, Chow & Patterson (1965–1969) Greenland ice-core lead curve from 800 BC (~0.001 µg/kg) to 1965 (>0.20 µg/kg, >200× increase after 1923 tetraethyl lead) (`SCALE: a single tank of nineteen-sixties leaded petrol puffed more than thirty grams of pure toxic lead dust out of the tailpipe and straight into city air`)",
        "  6. `P5:01_timeline_1862_1970_and_80_percent_blood_lead_drop_chart` — completed 5-date timeline (1862–1897 → 1965–1970) + >80% drop in children's blood-lead levels after unleaded petrol (`SCALE: within twenty years of switching petrol pumps to unleaded fuel, the amount of toxic lead circulating in children's bloodstreams dropped by more than four-fifths across the world`)",
        f"- **£0 verified reuse ({totals['reuse']} row):** `P5:04_table_three_callback` uses the 2.40 s unused moving tail `[5.50s..7.90s]` of `P1:07_table_three_props_pitchblende_canyon_diablo_meteorite_and_teflon_ice_bottle`.",
        "",
        "## Mint order",
        "",
        "006 > 007 > 008 > 009 > 010 > 011 > 012 > 013 > 014 > 015 > 016 > 017 > 018 > 019 > 020 > 021 > 022 > 023 > 024 > 025 > 026 > 027 > 028 > 029 > 030 > 031 > 032 > 033 > 034 > 035 > 036 > 037 > 038 > 039 > 040. `generation_authorized` is `false` on every row.",
    ])
    (EDIT / "PRICE_REVIEW_v01.md").write_text("\n".join(pr_lines) + "\n")
    print(f"040 v01 boards written: {totals['rows']} rows, Flow expected={totals['flow_credits_expected']}")


if __name__ == "__main__":
    main()
