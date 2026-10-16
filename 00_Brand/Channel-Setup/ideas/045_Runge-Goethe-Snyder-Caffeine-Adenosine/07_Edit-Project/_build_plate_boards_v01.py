#!/usr/bin/env python3
"""HOS 045 (Coffee & Caffeine: The Plant Pesticide That Blocks Sleep) pre-VO plate boards v01. J0555. No mint, no spend.

Built from 00_Brand/Channel-Setup/ideas/045_Runge-Goethe-Snyder-Caffeine-Adenosine/caffeine_script_master_v01.md
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
        "Part 01 — A Cat's Eye, a Poet's Box of Beans, and the Wooden Block Under Your Brain's Brake Pedal",
        [
            ("01_goethe_3_oct_1819_jena_mocha_beans_to_runge_and_adenosine_receptor_lock", 0.0, 5.5, "A", False, "THE SLEEP-BRAKE BLOCKER", "Quality",
             "Quality: Short frame 0 / answer image (0:03) + in Jena, Germany, on 3 October 1819, 70-year-old Johann Wolfgang von Goethe hands a wooden box of green Arabian mocha coffee beans to 25-year-old chemist Friedlieb Ferdinand Runge; the camera dives into a steaming porcelain coffee cup and through a human neural synapse where a double-ringed caffeine molecule slips into an adenosine receptor and blocks drowsy adenosine molecules from docking.",
             STYLE + "In a sunlit 1819 Jena drawing room, seventy-year-old poet Johann Wolfgang von Goethe in a dark coat hands a carved wooden box of green Arabian coffee beans to twenty-five-year-old chemist Friedlieb Ferdinand Runge beside a porcelain coffee cup and a brass molecular lock model." + QUAL_TAIL,
             {"kind": "WHEN", "label": "JENA, 3 OCTOBER 1819", "timeline_step": "1/5 · 3 Oct 1819 (Goethe hands 25-year-old Friedlieb Ferdinand Runge a box of Arabian mocha coffee beans in Jena; Runge isolates white caffeine crystals, published 1820)", "hold_s": 3.5}),
            ("02_runge_1819_caffeine_needles_caterpillar_honeybee_and_snyder_1981_receptor_split", 5.5, 6.0, "B", False, "BEANS, BUGS, BRAIN RECEPTORS", "Quality",
             "Quality: complex three-part split composition (Friedlieb Ferdinand Runge's 1819 glass dish of silky white caffeine crystal needles in Jena on the left; a coffee leaf paralysing a chewing caterpillar while coffee-flower nectar feeds a foraging honeybee in the centre; Solomon Snyder and John Daly's 1981 adenosine-receptor molecular lock model on the right).",
             STYLE + "Three-panel period composition: on the left, a glass watch-dish of long silky white caffeine crystal needles; in the centre, a green coffee branch with red cherries, a white blossom, and a honeybee; on the right, a brass-and-wood molecular lock-and-key model." + QUAL_TAIL,
             None),
            ("03_runge_3_oct_1819_jena_showing_dilated_cat_pupil_to_goethe", 11.5, 6.0, "C", False, "JENA, 3 OCTOBER 1819", "Quality",
             "Quality: readable faces + animal (in Jena on 3 October 1819, Friedlieb Ferdinand Runge shows Johann Wolfgang von Goethe a live cat whose left pupil is wide open from a drop of belladonna extract while Goethe holds out a box of green Arabian mocha beans).",
             STYLE + "In an 1819 Jena study, young chemist Friedlieb Ferdinand Runge in a borrowed frock coat gently holds a calm tabby cat with one wide dilated pupil and one narrow slit pupil while seventy-year-old Johann Wolfgang von Goethe reaches for a wooden box of green coffee beans." + QUAL_TAIL,
             {"kind": "WHEN", "label": "3 OCTOBER 1819", "timeline_step": "1/5 · 3 Oct 1819 (Runge demonstrates belladonna pupil dilation on a cat to Goethe and receives Arabian mocha coffee beans)", "hold_s": 3.5}),
            ("04_adenosine_vs_caffeine_purine_ring_and_2b_cups_120k_tonnes_chart", 17.5, 8.0, "E", False, "CAFFEINE (1,3,7-TRIMETHYLXANTHINE, ~95 MG/CUP) BLOCKS ADENOSINE RECEPTORS · >2B COFFEE + >3B TEA CUPS/DAY (120,000 TONNES/YR)", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked molecular structure and daily global consumption chart compares adenosine (adenine ring + ribose sugar) against caffeine (1,3,7-trimethylxanthine, ~1–2% of roasted coffee bean dry weight, ~95 mg per 240 mL cup) across humanity's >2 billion cups of coffee and >3 billion cups of tea consumed every single day (~120,000 tonnes of pure caffeine a year).",
             {"kind": "DATA", "label": "CAFFEINE (~95 MG/CUP, 1.5% BEAN WEIGHT) VS ADENOSINE LOCK · >2B COFFEE CUPS/DAY (120,000 TONNES/YR)", "detail": "Inked molecular structure and daily global consumption chart on period paper comparing adenosine (adenine ring + ribose sugar) against caffeine (1,3,7-trimethylxanthine, ~1–2% of roasted coffee bean dry weight, ~95 mg per 240 mL cup) across humanity's >2 billion cups of coffee and >3 billion cups of tea consumed every single day (~120,000 tonnes of pure caffeine a year)", "scale": "humanity drinks more than two billion cups of coffee every day — swallowing enough pure caffeine each year to equal the weight of twelve Eiffel Towers", "who_card": "Johann Wolfgang von Goethe (1749–1832) — German poet and statesman · Friedlieb Ferdinand Runge (1794–1867) — German analytical chemist · Hermann Emil Fischer (1852–1919) — German organic chemist · John W. Daly (1933–2008) — American bioorganic chemist · Solomon H. Snyder (born 1938) — American neuroscientist", "when_stamp": "3 October 1819 · 1895 · May 1981", "hold_s": 3.8}),
            ("05_green_arabica_coffee_beans_roasted_beans_and_white_caffeine_crystals_pan", 25.5, 5.5, "A", False, "JENA, 3 OCTOBER 1819", "Fast",
             "Fast: daylight macro pan across a wooden box of green Arabian coffee beans, dark roasted coffee beans, a brass mortar and pestle, and a glass dish of silky white caffeine needles on an oak table between code graphics so two full-frame graphics never run back to back. Nothing emissive, no face.",
             STYLE + "In crisp daylight on an oak laboratory table, the camera pans smoothly across a wooden box of pale green coffee beans, dark roasted coffee beans, a brass mortar and pestle, and a glass watch-dish heaped with silky white needle crystals." + FAST_TAIL,
             None),
            ("06_leaf_pesticide_15000_ppm_vs_floral_nectar_25_ppm_3x_bee_memory_chart", 31.0, 8.0, "E", False, "PESTICIDE IN LEAVES, BRIBE IN NECTAR", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period parchment, an inked concentration and effect chart contrasts toxic leaf and seed caffeine (~15,000 parts per million = 1–2% dry weight, lethal insect pesticide, Nathanson 1984) against floral nectar caffeine (~25 parts per million = 600-fold lower dose giving a 3× honeybee 24-hour flower-scent memory boost, Wright 2013).",
             {"kind": "DATA", "label": "15,000 PPM LEAF PESTICIDE (NATHANSON 1984) VS 25 PPM NECTAR (600× LOWER, 3× BEE MEMORY, WRIGHT 2013)", "detail": "Inked concentration & effect chart contrasting toxic leaf/seed caffeine (~15,000 parts per million = lethal insect pesticide) against floral nectar caffeine (~25 parts per million = 3× honeybee 24-hour flower-scent memory boost)", "scale": "a coffee bush packs six hundred times more caffeine into its seeds to poison hungry bugs than it slips into its flower nectar to bribe honeybees into remembering its address", "hold_s": 3.8}),
            ("07_table_three_props_goethe_bean_box_watch_glass_caffeine_needles_purine_model", 39.0, 5.5, "C", False, "1819 TO 2014", "Fast",
             "Fast: daylight prop table (callback source for Part 05: Goethe's wooden box of green Arabian mocha beans, Runge's glass watch-dish of silky white caffeine needles, and a brass-and-wood 1,3,7-trimethylxanthine purine ring molecular model). Nothing emissive.",
             STYLE + "On an oak workbench in soft window light sit three objects side by side: a carved wooden box of green coffee beans, a glass watch-dish of long white needle crystals, and a brass ball-and-stick double-ring molecular model." + FAST_TAIL,
             None),
            ("08_explorer_watching_white_caffeine_crystal_key_block_blue_sleep_keyhole", 62.0, 5.5, "A", True, None, "Quality",
             "Quality: Explorer beat 1 (locked character reference, after 1:00).",
             STYLE + "Sitting at a miniature wooden desk, the Explorer watches a blue key float toward a brass keyhole on the desk before a tiny white crystal shaped like a twin key hops out of a porcelain teacup, slips into the keyhole first without turning it, and leaves blue keys stacking up outside." + EXP_TAIL,
             None),
            ("09_runge_late_1819_jena_sublimating_white_kaffebase_needles_in_glass_flask", 67.5, 5.5, "B", False, "\"KAFFEBASE\", JENA 1819", "Quality",
             "Quality: readable face + glass sublimation apparatus (in Jena in late 1819, Friedlieb Ferdinand Runge sublimates long, silky white needles of 'Kaffebase' caffeine inside a glass flask).",
             STYLE + "In a cold 1819 Jena laboratory, twenty-five-year-old chemist Friedlieb Ferdinand Runge peers closely at a glass dome flask lined inside with sparkling white needle-shaped crystals." + QUAL_TAIL,
             None),
        ],
    ),
    (
        2,
        "Part 02 — 3 October 1819: The Cat's Eye, Goethe's Mocha Beans & Friedlieb Ferdinand Runge's 'Kaffebase'",
        [
            ("01_dobereiner_and_runge_3_oct_1819_jena_cat_visit_to_goethe_and_fischer_1895", 73.0, 6.5, "A", False, "BORROWED COAT, LIVE CAT", "Quality",
             "Quality: readable faces (chemistry professor Johann Wolfgang Döbereiner sending 25-year-old Friedlieb Ferdinand Runge in a borrowed frock coat and top hat with a live cat to Johann Wolfgang von Goethe's study on 3 October 1819, dissolving to Hermann Emil Fischer in Berlin synthesising caffeine in 1895).",
             STYLE + "Split period scene: on the left in 1819 Jena, professor Johann Wolfgang Döbereiner adjusts the borrowed coat of young Friedlieb Ferdinand Runge holding a tabby cat before Goethe; on the right in 1895 Berlin, bearded chemist Hermann Emil Fischer inspects a flask of synthetic purine crystals." + QUAL_TAIL,
             {"kind": "WHO", "label": "Johann Wolfgang Döbereiner (1780–1849) — German chemistry professor", "fact_card": "Borrowed coat, live cat", "when_stamp": "15th century · 17th century · 3 October 1819 · 1820 · 1895 · 1897", "timeline_step": "1/5 · 3 Oct 1819 (Goethe hands 25-year-old Friedlieb Ferdinand Runge a box of Arabian mocha coffee beans in Jena; Runge isolates white caffeine crystals, published 1820) & 2/5 · 1895–1897 (Emil Fischer determines caffeine's 1,3,7-trimethylxanthine purine structure and synthesises it from scratch)", "hold_s": 3.8}),
            ("02_runge_1820_100g_beans_to_1_5g_caffeine_and_fischer_1895_purine_structure_chart", 79.5, 8.0, "E", False, "1819–1820 RUNGE ISOLATION (1.2–1.5 G PER 100 G BEANS) & 1895–1897 FISCHER PURINE RING (C8H10N4O2, SUBLIMATES 235–238 °C)", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked chemical isolation and purine-ring diagram from Friedlieb Ferdinand Runge (1820, Neueste phytochemische Entdeckungen) and Emil Fischer (1895–1897) shows 100 grams of green Coffea arabica beans yielding ~1.2 to 1.5 grams of silky white caffeine crystals (C8H10N4O2, sublimating at 235–238 °C) built around a two-ring purine core with three methyl (CH3) groups.",
             {"kind": "DATA", "label": "100 G GREEN ARABICA BEANS → 1.2–1.5 G WHITE CAFFEINE NEEDLES (C8H10N4O2, 1,3,7-TRIMETHYLXANTHINE)", "detail": "Inked chemical isolation & purine-ring diagram on period paper from Friedlieb Ferdinand Runge (1820, Neueste phytochemische Entdeckungen) and Emil Fischer (1895–1897) showing 100 grams of green Coffea arabica beans yielding ~1.2 to 1.5 grams of silky white caffeine crystals (C8H10N4O2, melting/sublimating at 235–238 °C) built around a two-ring purine core with three methyl (CH3) groups", "scale": "every single cup of brewed coffee holds roughly a tenth of a gram of pure white caffeine needles — about the weight of three grains of rice", "hold_s": 3.8}),
            ("03_jena_bench_watch_glass_white_kaffebase_needles_and_goethe_bean_box_closeup", 87.5, 6.5, "B", False, "1819 — RUNGE'S \"KAFFEBASE\"", "Fast",
             "Fast: daylight macro shot of Runge's glass watch-glass of long, silky white 'Kaffebase' needles beside Goethe's wooden mocha-bean box and three grains of rice on a brass balance scale. Nothing emissive, no face.",
             STYLE + "In crisp daylight on a wooden laboratory bench, a glass watch-dish of long silky white caffeine crystal needles sits beside a carved wooden box of green coffee beans and a small brass balance pan holding three grains of white rice." + FAST_TAIL,
             None),
            ("04_fischer_1895_berlin_purine_molecular_models_and_1820_runge_monograph_pan", 94.0, 5.5, "C", False, "1895 — EMIL FISCHER'S PURINE", "Fast",
             "Fast: daylight close-up of Emil Fischer's 1895 brass-and-wood ball-and-stick model of the 1,3,7-trimethylxanthine purine ring beside Runge's 1820 printed phytochemistry book on an oak desk. Nothing emissive, no face.",
             STYLE + "In bright window light on an oak desk, a vintage wooden ball-and-stick molecular model of a double purine ring rests beside an open nineteenth-century German chemistry volume and a stoppered glass vial of white crystals." + FAST_TAIL,
             None),
        ],
    ),
    (
        3,
        "Part 03 — Why Plants Make Caffeine: The 1984 Bug-Killing Neurotoxin & the 2013 Honeybee Memory Bribe — Midpoint Twist",
        [
            ("01_nathanson_5_oct_1984_caterpillar_pesticide_and_wright_8_mar_2013_honeybee_memory", 99.5, 6.5, "A", False, "TRIPLES BEE SCENT MEMORY", "Quality",
             "Quality: readable faces + insects (Harvard neurologist James A. Nathanson on 5 October 1984 testing coffee-leaf caffeine on feeding hornworm caterpillars, dissolving to neuroethologist Geraldine A. Wright on 8 March 2013 testing lightly caffeinated floral nectar on foraging honeybees).",
             STYLE + "Split scene: on the left in a 1984 Harvard laboratory, neurologist James Nathanson observes a green hornworm caterpillar recoiling from a coffee leaf; on the right in a 2013 lab, Geraldine Wright watches a honeybee extend its proboscis toward a white coffee blossom." + QUAL_TAIL,
             {"kind": "WHO", "label": "James A. Nathanson (born 1947) — American neurologist · Geraldine A. Wright (born 1970) — insect neuroethologist", "fact_card": "Triples bee scent memory", "when_stamp": "5 October 1984 · 8 March 2013 · 5 September 2014", "timeline_step": "4/5 · 5 Oct 1984 (James Nathanson in Science proves high-dose leaf/seed caffeine evolved as a natural insect-paralysing pesticide) & 5/5 · 8 Mar 2013–5 Sep 2014 (Geraldine Wright in Science proves low-dose floral nectar caffeine triples honeybee scent memory; coffee genome confirms convergent evolution)", "hold_s": 3.8}),
            ("02_nathanson_1984_larval_lethality_and_wright_2013_3x_24h_bee_memory_chart", 106.0, 8.0, "E", False, "5 OCT 1984 PESTICIDE (1–2% LEAF CAFFEINE KILLS LARVAE) & 8 MAR 2013 NECTAR BRIBE (25 PPM TRIPLES 24-HOUR BEE MEMORY)", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked survival and memory bar chart combines James Nathanson (5 October 1984, Science) insect lethality curves (1–2% leaf caffeine killing ~90–100% of feeding hornworm larvae) and Geraldine Wright (8 March 2013, Science) honeybee conditioning trials (caffeinated nectar tripling 24-hour olfactory memory retention vs plain sugar water).",
             {"kind": "DATA", "label": "1–2% LEAF CAFFEINE = LETHAL BUG POISON (1984) · 25 PPM NECTAR = 3× 24-HOUR BEE SCENT MEMORY (2013)", "detail": "Inked survival & memory bar chart on period paper combining James Nathanson (1984, Science) insect lethality curves (1–2% leaf caffeine killing ~90–100% of feeding hornworm larvae) and Geraldine Wright (2013, Science) honeybee conditioning trials (caffeinated nectar tripling 24-hour olfactory memory retention vs plain sugar water)", "scale": "at leaf strength, caffeine is a lethal neurotoxin that paralyses caterpillars — yet diluted six hundred times in flower nectar, it works like a study drug that triples a honeybee's memory overnight", "hold_s": 3.8}),
            ("03_coffea_arabica_branch_red_cherries_white_blossoms_and_botanical_tray_closeup", 114.0, 6.5, "B", False, "1984 & 2013 — POISON AND BRIBE", "Fast",
             "Fast: daylight botanical close-up of a Coffea arabica branch bearing glossy green leaves, red coffee cherries, and fragrant white blossoms beside a glass pipette and botanical specimen tray on an oak bench. Nothing emissive, no face.",
             STYLE + "In crisp daylight on a botanical worktable, a fresh coffee branch with glossy green leaves, ripe red coffee berries, and white star-shaped blossoms rests beside a glass dropper and a porcelain dish of coffee seeds." + FAST_TAIL,
             None),
            ("04_coffee_tea_and_cacao_botanical_specimens_three_continents_pan", 120.5, 5.5, "C", False, "5 SEPTEMBER 2014 — CONVERGENT EVOLUTION", "Fast",
             "Fast: daylight pan across three botanical specimens on a museum table: African Coffea arabica beans, Asian Camellia sinensis tea leaves, and South American Theobroma cacao pods. Nothing emissive, no face.",
             STYLE + "In bright window light on a museum table, three botanical specimens sit side by side: roasted coffee beans, dried green tea leaves, and a split brown cacao pod revealing cocoa beans." + FAST_TAIL,
             None),
        ],
    ),
    (
        4,
        "Part 04 — May 1981: Adenosine Exhaust, Solomon Snyder & John Daly's Molecular Lock, and Why the 'Caffeine Crash' Happens",
        [
            ("01_snyder_daly_and_fredholm_may_1981_adenosine_receptor_binding_discovery", 126.0, 6.5, "A", False, "BLOCKS BRAKE, NOT GAS", "Quality",
             "Quality: readable faces (neuroscientist Solomon H. Snyder in Baltimore and bioorganic chemist John W. Daly at NIH in May 1981 inspecting brain adenosine-receptor binding curves alongside Swedish pharmacologist Bertil B. Fredholm's receptor model).",
             STYLE + "In a 1981 pharmacology laboratory, neuroscientist Solomon Snyder and chemist John Daly examine plotted receptor-binding curves on paper beside three-dimensional ball-and-stick models of adenosine and caffeine." + QUAL_TAIL,
             {"kind": "WHO", "label": "Bertil B. Fredholm (born 1943) — Swedish pharmacologist", "fact_card": "Blocks brake, not gas", "when_stamp": "1929 · May 1981", "timeline_step": "3/5 · May 1981 (Solomon Snyder, John Daly, and Bertil Fredholm prove coffee-dose caffeine keeps humans awake by blocking A1 and A2A adenosine sleep receptors)", "hold_s": 3.8}),
            ("02_snyder_daly_1981_10_50_um_adenosine_block_and_5h_half_life_crash_chart", 132.5, 8.0, "E", False, "MAY 1981 PNAS: 10–50 µM CAFFEINE BLOCKS A1/A2A ADENOSINE RECEPTORS (VS >1,000 µM PDE) · 5-HOUR HALF-LIFE CRASH", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked receptor-affinity and half-life curve from Snyder, Katims, Annau, Bruns & Daly (May 1981, PNAS) shows caffeine competitively blocking brain adenosine receptors at 10–50 micromolar blood concentrations (1–2 cups of coffee) vs >1,000 micromolar needed for phosphodiesterase inhibition, alongside the ~5-hour human metabolic half-life curve showing unblocked adenosine accumulation causing the afternoon crash.",
             {"kind": "DATA", "label": "MAY 1981 PNAS: 10–50 µM CAFFEINE BLOCKS ADENOSINE RECEPTORS · ~5-HOUR LIVER HALF-LIFE & ADENOSINE CRASH", "detail": "Inked receptor-affinity & half-life curve on period paper from Snyder, Katims, Annau, Bruns & Daly (May 1981, PNAS) showing caffeine competitively blocking brain adenosine receptors at 10–50 micromolar blood concentrations (1–2 cups of coffee) vs >1,000 micromolar needed for phosphodiesterase inhibition, alongside the ~5-hour human metabolic half-life curve showing unblocked adenosine accumulation causing the afternoon crash", "scale": "a single cup of coffee floods your bloodstream with roughly three hundred quintillion caffeine molecules — parking a fake key inside up to half of your brain's sleep receptors within forty-five minutes", "hold_s": 3.8}),
            ("03_adenosine_and_caffeine_3d_ball_and_stick_purine_models_side_by_side_closeup", 140.5, 6.5, "B", False, "MAY 1981 — THE FALSE KEY", "Fast",
             "Fast: daylight macro shot of two 3D ball-and-stick molecular models on a lab bench — adenosine on the left and caffeine on the right — showing their matching double-ringed purine skeletons beside a brass keyhole block. Nothing emissive, no face.",
             STYLE + "In crisp daylight on a wooden laboratory bench, two painted wooden ball-and-stick molecular models of adenosine and caffeine sit side by side revealing their matching double-ringed cores beside a brass lock mechanism." + FAST_TAIL,
             None),
            ("04_explorer_wedging_white_crystal_block_under_brass_sleep_brake_pedal", 147.0, 5.5, "B", True, None, "Quality",
             "Quality: Explorer beat 2 (locked character reference).",
             STYLE + "Standing between a brass foot pedal and a ticking five-hour clock dial, the Explorer wedges a white crystal block under the brake pedal while blue wooden spheres pile up on a shelf above, then gasps as the clock hand reaches five and the block slips out." + EXP_TAIL,
             None),
        ],
    ),
    (
        5,
        "Part 05 — Why Caffeine Can't Replace Sleep & How an 8-Year-Old Boy and a Cave Proved Your Sleeping Brain Never Rests",
        [
            ("01_timeline_1819_2014_and_5h_half_life_4pm_to_2am_clearance_chart", 152.5, 8.5, "E", False, "1819–2014 TIMELINE · 5-HOUR HALF-LIFE (200 MG AT 4 PM → 100 MG AT 9 PM → 50 MG AT 2 AM)", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, the 5-date timeline completes: 3 Oct 1819 (Goethe hands 25-year-old Friedlieb Ferdinand Runge a box of Arabian mocha coffee beans in Jena; Runge isolates white caffeine crystals, published 1820) · 1895–1897 (Emil Fischer determines caffeine's 1,3,7-trimethylxanthine purine structure and synthesises it from scratch) · May 1981 (Solomon Snyder, John Daly, and Bertil Fredholm prove coffee-dose caffeine keeps humans awake by blocking A1 and A2A adenosine sleep receptors) · 5 Oct 1984 (James Nathanson in Science proves high-dose leaf/seed caffeine evolved as a natural insect-paralysing pesticide) · 8 Mar 2013–5 Sep 2014 (Geraldine Wright in Science proves low-dose floral nectar caffeine triples honeybee scent memory; coffee genome confirms convergent evolution) alongside the 5-hour human liver half-life clearance curve (200 mg at 4:00 p.m. → 100 mg at 9:00 p.m. → 50 mg at 2:00 a.m.).",
             {"kind": "DATA", "label": "1819–2014 TIMELINE · 5-HOUR HUMAN LIVER HALF-LIFE (4 PM ESPRESSO = 50% STILL BLOCKING RECEPTORS AT 9 PM)", "detail": "Animated 5-date timeline (3 Oct 1819 → 8 Mar 2013–5 Sep 2014) alongside the 5-hour human liver half-life clearance curve (200 mg at 4:00 p.m. → 100 mg at 9:00 p.m. → 50 mg at 2:00 a.m.)", "scale": "because caffeine has a five-hour half-life in the human liver, drinking a double espresso at four in the afternoon is like drinking half an espresso right before you climb into bed at nine o'clock at night", "fact_card": "Five-hour human half-life", "when_stamp": "4:00 p.m. · 9:00 p.m. · 2:00 a.m. · 1819–2014", "timeline_step": "5/5 · 1819–2014 timeline complete", "hold_s": 3.8}),
            ("02_espresso_cup_sand_hourglass_and_pocket_watch_on_bedside_table_pan", 161.0, 5.5, "A", False, "DELAYS SLEEP, NEVER REPLACES IT", "Fast",
             "Fast: daylight close-up of a porcelain espresso cup, a brass sand hourglass filled with blue sand, and a mechanical pocket watch on a wooden bedside table. Nothing emissive, no face.",
             STYLE + "In soft window light on a wooden table, a porcelain espresso cup sits beside a brass hourglass filled with fine blue sand and a mechanical pocket watch." + FAST_TAIL,
             None),
            ("03_berger_1924_eeg_kleitman_1938_cave_aserinsky_1953_rem_and_nedergaard_2013_sleep_handoff", 166.5, 6.5, "C", False, "CAVES, DREAMS, BRAIN WASHING", "Quality",
             "Quality: readable faces (Hans Berger's 6 July 1924 first human EEG brainwave recording, Nathaniel Kleitman's June 1938 Mammoth Cave experiment, Eugene Aserinsky's 4 September 1953 REM sleep polygraph pens wired to his 8-year-old son Armond in Chicago, and Maiken Nedergaard's 18 October 2013 glymphatic brain-washing system — handoff to 046 Sleep & REM).",
             STYLE + "In a 1952 Chicago sleep laboratory, graduate student Eugene Aserinsky watches ink polygraph pens trace rapid eye-movement waves beside his sleeping eight-year-old son Armond and an EEG brainwave drum." + QUAL_TAIL,
             {"kind": "WHEN", "label": "6 JULY 1924 · JUNE 1938 · 4 SEPTEMBER 1953 · 18 OCTOBER 2013", "hold_s": 3.5}),
            ("04_table_three_callback", 173.0, 2.4, "C", False, None, "reuse",
             "Reuse: verified unused moving window [5.50s..7.90s] of P1:07_table_three_props_goethe_bean_box_watch_glass_caffeine_needles_purine_model (callback, £0).",
             "Reuse P1:07_table_three_props_goethe_bean_box_watch_glass_caffeine_needles_purine_model [5.50s..7.90s] (2.40s distinct non-overlapping tail window from 8.00s source clip).",
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
                row["reuse_of"] = "P1:07_table_three_props_goethe_bean_box_watch_glass_caffeine_needles_purine_model"
                row["reuse_window_s"] = [5.5, 7.9]
                row["reuse_audit"] = {
                    "source_row": "P1:07_table_three_props_goethe_bean_box_watch_glass_caffeine_needles_purine_model",
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
            "film": "045_Runge-Goethe-Snyder-Caffeine-Adenosine",
            "part": p_idx,
            "title": p_title,
            "version": "v01",
            "timing_status": "pre_vo_script_clock (built from caffeine_script_master_v01.md; retimes onto Scribe STT once VO locks)",
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
        "film": "045_Runge-Goethe-Snyder-Caffeine-Adenosine",
        "version": "v01",
        "date": "2026-10-18",
        "owner": "gemini (J0555)",
        "status": "PRE_VO_BOARDS_V01_NO_MINT",
        "generation_authorized": False,
        "script": "00_Brand/Channel-Setup/ideas/045_Runge-Goethe-Snyder-Caffeine-Adenosine/caffeine_script_master_v01.md",
        "sources": "00_Brand/Channel-Setup/ideas/045_Runge-Goethe-Snyder-Caffeine-Adenosine/SOURCES_v01.md",
        "credit_snapshot": {
            "flow_balance": 23740,
            "flow_floor": 0,
            "flow_read_at": "2026-10-15T21:42:22Z",
            "vertex_promo_gbp": 71.02,
            "vertex_usable_gbp": 70.02,
        },
        "totals": totals,
        "per_part": per_part_summary,
        "mint_order": "006 > 007 > 008 > 009 > 010 > 011 > 012 > 013 > 014 > 015 > 016 > 017 > 018 > 019 > 020 > 021 > 022 > 023 > 024 > 025 > 026 > 027 > 028 > 029 > 030 > 031 > 032 > 033 > 034 > 035 > 036 > 037 > 038 > 039 > 040 > 041 > 042 > 043 > 044 > 045. Nothing in 045 is generation_authorized.",
    }
    (EDIT / "PICTURE_PLAN_v01.json").write_text(json.dumps(plan, indent=2) + "\n")

    sl = [
        "# 045 Coffee & Caffeine: The Plant Pesticide That Blocks Sleep — Shot list & plate boards v01 (pre-VO)",
        "",
        "Gemini, 18 Oct 2026, J0555. Built from `caffeine_script_master_v01.md` (`91.8 PASS`) and `SOURCES_v01.md`.",
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
        "# 045 price review v01 (pre-VO plate boards)",
        "",
        "Gemini, 18 Oct 2026, J0555. Boards only. **No mint. No spend. No merge.**",
        "Prepared from `caffeine_script_master_v01.md` (`91.8 PASS`) and `SOURCES_v01.md` so 045's full plate board rows, non-emissive Fast prompts, £0 code graphics, and Teach-on-Screen overlays are ready to re-time the moment long VO locks. Parked for Chief.",
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
        f"- **Quality ({totals['Quality']} rows):** readable faces (Johann Wolfgang von Goethe, Friedlieb Ferdinand Runge, Johann Wolfgang Döbereiner, Hermann Emil Fischer, James A. Nathanson, Geraldine A. Wright, Solomon H. Snyder, John W. Daly, Eugene Aserinsky, Armond Aserinsky), 1819 Jena drawing room and cat pupil demonstration, 1984 Harvard & 2013 bee conditioning scenes, 1981 Johns Hopkins/NIH receptor scenes, and the 2 Explorer beats.",
        f"- **Fast ({totals['Fast']} rows, non-emissive):** daylight prop and botanical shots (green vs roasted coffee beans & white caffeine crystals pan, 3-object callback bench, Runge's watch-glass of Kaffebase needles & three grains of rice on brass scale, Emil Fischer's 1895 purine ball-and-stick model & Runge's 1820 monograph, Coffea arabica branch with red cherries & white blossoms, coffee/tea/cacao convergent evolution specimen tray, adenosine vs caffeine 3D molecular models side by side, espresso cup & sand hourglass on bedside table). Zero candles, flames, sparks, or glowing elements on Fast.",
        f"- **£0 code graphics ({totals['code_graphic']} rows):**",
        "  1. `P1:04_adenosine_vs_caffeine_purine_ring_and_2b_cups_120k_tonnes_chart` — Adenosine vs caffeine (1,3,7-trimethylxanthine, ~95 mg/cup) across >2 billion cups of coffee and >3 billion cups of tea/day (~120,000 tonnes/yr) (`SCALE: humanity drinks more than two billion cups of coffee every day — swallowing enough pure caffeine each year to equal the weight of twelve Eiffel Towers`)",
        "  2. `P1:06_leaf_pesticide_15000_ppm_vs_floral_nectar_25_ppm_3x_bee_memory_chart` — High-dose leaf/seed caffeine (~15,000 ppm lethal insect pesticide, Nathanson 1984) vs low-dose floral nectar caffeine (~25 ppm = 3× honeybee 24-hour scent memory, Wright 2013) (`SCALE: a coffee bush packs six hundred times more caffeine into its seeds to poison hungry bugs than it slips into its flower nectar to bribe honeybees into remembering its address`)",
        "  3. `P2:02_runge_1820_100g_beans_to_1_5g_caffeine_and_fischer_1895_purine_structure_chart` — Runge's 1820 isolation (100 g green Coffea arabica beans → 1.2–1.5 g white caffeine needles, sublimating at 235–238 °C) & Fischer's 1895–1897 C8H10N4O2 purine ring (`SCALE: every single cup of brewed coffee holds roughly a tenth of a gram of pure white caffeine needles — about the weight of three grains of rice`)",
        "  4. `P3:02_nathanson_1984_larval_lethality_and_wright_2013_3x_24h_bee_memory_chart` — Nathanson (1984, *Science*) 90–100% hornworm larval lethality vs Wright (2013, *Science*) 3× 24-hour honeybee olfactory memory retention (`SCALE: at leaf strength, caffeine is a lethal neurotoxin that paralyses caterpillars — yet diluted six hundred times in flower nectar, it works like a study drug that triples a honeybee's memory overnight`)",
        "  5. `P4:02_snyder_daly_1981_10_50_um_adenosine_block_and_5h_half_life_crash_chart` — Snyder & Daly (May 1981, *PNAS*) 10–50 µM competitive A1/A2A adenosine-receptor block vs >1,000 µM PDE threshold & ~5-hour half-life crash curve (`SCALE: a single cup of coffee floods your bloodstream with roughly three hundred quintillion caffeine molecules — parking a fake key inside up to half of your brain's sleep receptors within forty-five minutes`)",
        "  6. `P5:01_timeline_1819_2014_and_5h_half_life_4pm_to_2am_clearance_chart` — completed 5-date timeline (1819 → 2014) + 5-hour human liver half-life clearance curve (200 mg at 4:00 p.m. → 100 mg at 9:00 p.m. → 50 mg at 2:00 a.m.) (`SCALE: because caffeine has a five-hour half-life in the human liver, drinking a double espresso at four in the afternoon is like drinking half an espresso right before you climb into bed at nine o'clock at night`)",
        f"- **£0 verified reuse ({totals['reuse']} row):** `P5:04_table_three_callback` uses the 2.40 s unused moving tail `[5.50s..7.90s]` of `P1:07_table_three_props_goethe_bean_box_watch_glass_caffeine_needles_purine_model`.",
        "",
        "## Mint order",
        "",
        "006 > 007 > 008 > 009 > 010 > 011 > 012 > 013 > 014 > 015 > 016 > 017 > 018 > 019 > 020 > 021 > 022 > 023 > 024 > 025 > 026 > 027 > 028 > 029 > 030 > 031 > 032 > 033 > 034 > 035 > 036 > 037 > 038 > 039 > 040 > 041 > 042 > 043 > 044 > 045. `generation_authorized` is `false` on every row.",
    ])
    (EDIT / "PRICE_REVIEW_v01.md").write_text("\n".join(pr_lines) + "\n")
    print(f"045 v01 boards written: {totals['rows']} rows, Flow expected={totals['flow_credits_expected']}")


if __name__ == "__main__":
    main()
