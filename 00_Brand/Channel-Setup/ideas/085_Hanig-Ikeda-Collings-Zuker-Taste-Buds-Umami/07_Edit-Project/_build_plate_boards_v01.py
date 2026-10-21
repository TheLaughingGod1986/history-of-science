#!/usr/bin/env python3
"""HOS 085 (Umami: Why Your School Tongue Map Was a Lie) pre-VO plate boards v01. J0753. No mint, no spend.

Built from 00_Brand/Channel-Setup/ideas/085_Hanig-Ikeda-Collings-Zuker-Taste-Buds-Umami/taste_umami_script_master_v01.md
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
        "Part 01 — The 100-Year Textbook 'Tongue Map' Myth & the 38-Kilogram Pot of Seaweed Soup",
        [
            ("01_crossed_out_1942_tongue_map_whole_tongue_five_tastes_and_ikeda_1908_38kg_kelp_30g_umami_crystals", 0.0, 5.5, "A", False, "THE TONGUE MAP MYTH & UMAMI", "Quality",
             "Quality: Short frame 0 / answer image (0:03) + side by side, a crossed-out 1942 school textbook 'Tongue Map' (Sweet tip, Salty front edges, Sour sides, Bitter back) is replaced by a human tongue where every taste bud lights up in all five colours across the entire surface, beside Kikunae Ikeda in Tokyo on 25 July 1908 lifting a porcelain dish of 30 grams of glistening white monosodium glutamate (umami) crystals rendered from a giant 38-kilogram stack of dried konbu kelp.",
             STYLE + "Split historical-and-anatomical scene: on the left, a crossed-out four-zone tongue chart gives way to a sculpted human tongue whose papillae respond in five colours across the entire surface; on the right in 1908 Tokyo, chemist Kikunae Ikeda holds a porcelain evaporating dish of white glutamate crystals beside a tall bundle of dried dark-green kelp." + QUAL_TAIL,
             {"kind": "WHEN", "label": "TOKYO, 25 JULY 1908", "timeline_step": "1/3 · 1867 & 1901–1942 (Gustav Schwalbe and Christian Lovén discover microscopic taste buds, and David Pauli Hänig measures small threshold differences around the tongue that Edwin Boring's 1942 graph accidentally turns into the false textbook Tongue Map)", "hold_s": 3.5}),
            ("02_hanig_1901_boring_1942_ikeda_1908_38kg_kelp_and_collings_1974_zuker_ryba_2002_receptors_split", 5.5, 6.0, "B", False, "MISREAD GRAPH, 38 KG KELP, 5 TASTE LOCKS", "Quality",
             "Quality: complex three-part composition (David Pauli Hänig in Leipzig in 1901 testing tongue sensitivity with a fine brush and Edwin Boring at Harvard in 1942 drawing the misread graph; Kikunae Ikeda at Tokyo Imperial University in 1908 boiling 38 kg of konbu kelp down to 30 g of glutamate crystals; and Virginia Collings in 1974 with Nirupa Chaudhari, Charles Zuker, and Nicholas Ryba in 1999–2002 mapping the T1R and T2R taste receptors).",
             STYLE + "Three-panel period composition: on the left, David Pauli Hänig in 1901 Leipzig touching a fine brush to a volunteer's tongue beside Edwin Boring in 1942; in the centre, Kikunae Ikeda in 1908 Tokyo stirring a porcelain evaporating basin of kelp broth; on the right, Virginia Collings in 1974 alongside Charles Zuker and Nicholas Ryba in 2002 with a five-taste receptor model." + QUAL_TAIL,
             None),
            ("03_tongue_papilla_cross_section_with_onion_shaped_taste_buds_testing_five_taste_molecules", 11.5, 6.0, "C", False, "10,000 CHEMICAL GUARDS", "Quality",
             "Quality: complex anatomical reveal (a close-up of a tongue papilla cross-section showing onion-shaped taste buds with 50–100 receptor cells testing incoming food molecules: green for Sweet carbohydrates, blue for Salty sodium ions, gold for Umami amino acids, yellow for Sour acids, and red warning signals for Bitter toxins).",
             STYLE + "In a three-dimensional cutaway of a tongue papilla trench, onion-shaped taste buds with clustered sensory cells and microvilli pores catch differently shaped coloured molecules for sweet, salty, umami, sour, and bitter." + QUAL_TAIL,
             {"kind": "WHEN", "label": "1901 · 25 JULY 1908 · 1942 · 1974 · 1999 · 2002", "timeline_step": "1/3 · 1867 & 1901–1942 (Schwalbe, Lovén, Hänig & Boring) · 2/3 · 25 July 1908 – 1974 (Ikeda, Kodama, Kuninaka & Collings) · 3/3 · 1999–2002 (Chaudhari, Zuker & Ryba)", "hold_s": 3.5}),
            ("04_hanig_1901_boring_1942_ikeda_1908_38kg_kelp_and_zuker_2002_five_taste_receptor_chart", 17.5, 8.0, "E", False, "IKEDA (1908): 38,000 G KELP → 30 G GLUTAMATE (UMAMI) · BITTER QUININE (~0.000008 M) VS SWEET SUCROSE (~0.01 M) · T1R/T2R RECEPTORS", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked Human Taste Buds, the 1901–1942 Tongue Map Myth, Ikeda's 1908 Umami Isolation & the 1999–2002 Five-Taste Receptor Lock chart from David Pauli Hänig (1901 Philosophische Studien 17: 576–623), Kikunae Ikeda (1908/1909 J. Chem. Soc. Tokyo 30: 820–836), Edwin Boring (1942), Virginia Collings (1974 Perception & Psychophysics 16: 169–174), and Chaudhari, Zuker & Ryba (1999–2002 Cell & Nature) shows 1) Hänig's small ~10–20% threshold differences vs Boring's unlabelled 1942 curves; 2) Ikeda's 38 kg konbu kelp → 30 g L-glutamic acid crystals; and 3) The 5 receptor families: T1R2+T1R3 (Sweet), T1R1+T1R3 / mGluR4 (Umami), 25 T2Rs (Bitter), ENaC (Salty), and OTOP1 (Sour) distributed across all tongue regions.",
             {"kind": "DATA", "label": "KIKUNAE IKEDA (1908) 38,000 G KONBU KELP → 30 G L-GLUTAMIC ACID (UMAMI) & BITTER (~0.000008 M) VS SWEET (~0.01 M) THRESHOLD CHART", "detail": "Inked Kikunae Ikeda (1908) 38,000 grams dried konbu kelp → 30 grams L-glutamic acid (umami) crystal extraction & 5-taste receptor threshold comparison (bitter quinine detected at ~0.000008 M vs sweet sucrose at ~0.01 M) on period paper", "scale": "your bitter taste receptors are more than a thousand times more sensitive than your sweet receptors — because missing a spoonful of sugar only costs you a few calories, whereas swallowing a single mouthful of bitter plant poison could cost you your life", "who_card": "David Pauli Hänig (born 1864) — German philosopher and psychophysicist · Edwin Garrigues Boring (1886–1968) — American experimental psychologist · Virginia B. Collings (fl. 1974) — American psychologist · Kikunae Ikeda (1864–1936) — Japanese chemist · Nirupa Chaudhari (fl. 2000) — American neuroscientist · Charles S. Zuker (born 1957) — Chilean-American molecular neurobiologist · Nicholas J. P. Ryba (fl. 1999–2002) — British-American molecular biologist", "when_stamp": "1901 · 25 July 1908 · 1942 · 1974 · 1999 · 2002", "hold_s": 3.8}),
            ("05_hanig_1901_journal_camel_hair_brush_dried_konbu_kelp_and_glutamate_crystal_bottle_pan", 25.5, 5.5, "A", False, "FIVE TASTES ACROSS THE WHOLE TONGUE", "Fast",
             "Fast: daylight macro pan across David Pauli Hänig's 1901 Philosophische Studien volume with a fine camel-hair brush, a bundle of dried konbu kelp, and a glass bottle of white monosodium glutamate crystals on an oak bench between code graphics so two full-frame graphics never run back to back. Nothing emissive, no face.",
             STYLE + "In crisp daylight on an oak chemistry bench, the camera pans smoothly across an open 1901 German journal with a fine camel-hair brush, a folded sheet of dried dark-green kelp, and a stoppered glass bottle of white crystals." + FAST_TAIL,
             None),
            ("06_zuker_ryba_2001_2002_t1r2_t1r3_sweet_t1r1_t1r3_umami_and_25_t2r_bitter_receptor_chart", 31.0, 8.0, "E", False, "SAN DIEGO & BETHESDA, 2002", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period parchment, an inked Charles Zuker & Nicholas Ryba (2001–2002 Cell & Nature) Heterodimeric Taste Receptor Lock diagram shows how the shared T1R3 subunit pairs with T1R2 to form the Sweet sugar receptor (T1R2+T1R3), pairs with T1R1 to form the Umami amino-acid receptor (T1R1+T1R3, boosted 8-fold by IMP/GMP ribonucleotides), and sits alongside 25 T2R Bitter toxin receptors across the whole tongue.",
             {"kind": "DATA", "label": "2001–2002 CHARLES ZUKER & NICHOLAS RYBA (CELL & NATURE): T1R2+T1R3 (SWEET), T1R1+T1R3 (UMAMI + 8× IMP/GMP) & 25 T2R (BITTER) RECEPTORS", "detail": "Inked Zuker & Ryba (2001–2002) T1R2+T1R3 (Sweet), T1R1+T1R3 (Umami + 8× IMP/GMP synergy) & 25-gene T2R (Bitter) receptor family architecture on period paper", "scale": "your cells replace every worn-out taste bud receptor every ten to fourteen days — which is why scalding your tongue on hot soup only dulls your taste for a few days before a brand-new set of taste buds grows back", "hold_s": 3.8}),
            ("07_table_three_props_1901_camel_brush_vials_1908_porcelain_dish_glutamate_and_1974_filter_paper_discs", 39.0, 5.5, "C", False, "1867 TO 2002", "Fast",
             "Fast: daylight prop table (callback source for Part 05: Hänig's 1901 fine camel-hair brush and four glass taste vials, Ikeda's 1908 porcelain evaporating dish of white glutamate crystals, and Collings's 1974 tweezers and tiny filter-paper taste discs). Nothing emissive.",
             STYLE + "On an oak workbench in soft window light sit three objects side by side: a wooden rack of four glass solution vials with a camel-hair brush, a porcelain evaporating dish of white glutamate crystals, and a Petri dish of tiny filter-paper discs with brass forceps." + FAST_TAIL,
             None),
            ("08_explorer_tipping_over_fake_tongue_map_signboard_and_fitting_glutamate_crystal_into_t1r1_t1r3_lock", 62.0, 5.5, "A", True, None, "Quality",
             "Quality: Explorer beat 1 (locked character reference, after 1:00).",
             STYLE + "Standing on a giant sculpted tongue papilla model beside a wooden easel showing a four-zone tongue chart, the Explorer tips the easel flat and fits a faceted golden glutamate crystal into a twin-subunit receptor lock so colourful markers spring up across the entire tongue model." + EXP_TAIL,
             None),
            ("09_virginia_collings_1974_pittsburgh_filter_paper_disc_whole_tongue_taste_test", 67.5, 5.5, "B", False, "PITTSBURGH, 1974", "Quality",
             "Quality: readable face (at the University of Pittsburgh in 1974, American psychologist Virginia B. Collings uses brass forceps to touch tiny filter-paper discs soaked in sweet, salty, sour, and bitter solutions to the tip, sides, and back of a volunteer's tongue, proving all regions detect all tastes).",
             STYLE + "In a 1974 University of Pittsburgh psychophysics laboratory, psychologist Virginia Collings holds fine forceps with a tiny filter-paper disc beside a volunteer and a five-region tongue sensitivity chart." + QUAL_TAIL,
             {"kind": "WHEN", "label": "PITTSBURGH, 1974", "timeline_step": "2/3 · 25 July 1908, 1913, 1960 & 1974 (Kikunae Ikeda in Tokyo boils 38 kg of konbu kelp down to 30 g of glutamate crystals to discover umami, Kodama and Kuninaka find the 8× nucleotide synergy, and Virginia Collings proves all tastes work across the whole tongue)", "hold_s": 3.5}),
        ],
    ),
    (
        2,
        "Part 02 — 1867, 1901, 1942 & 1974: Taste Buds, David Hänig's Brush & How Edwin Boring Accidentally Created the 100-Year 'Tongue Map' Myth",
        [
            ("01_schwalbe_loven_1867_taste_buds_hanig_1901_leipzig_brush_and_boring_1942_unlabelled_graph", 73.0, 6.5, "A", False, "ALL BUDS TASTE ALL FLAVOURS", "Quality",
             "Quality: readable faces (German anatomist Gustav Schwalbe and Swedish physician Christian Lovén in 1867 discovering microscopic onion-shaped taste buds, and German researcher David Pauli Hänig in Leipzig in 1901 touching a fine camel-hair brush dipped in taste solutions to a volunteer's tongue, dissolving to Harvard psychologist Edwin Garrigues Boring in 1942 plotting the unlabelled graph).",
             STYLE + "Split period scene: on the left in 1901 Leipzig, David Pauli Hänig touches a fine brush to a subject's tongue tip beside Gustav Schwalbe and Christian Lovén's 1867 microscope drawing of onion-shaped taste buds; on the right in 1942 Harvard, Edwin Boring drafts a four-curve graph without vertical numbers." + QUAL_TAIL,
             {"kind": "FACT", "label": "All buds taste all flavours", "who_card": "Gustav Schwalbe (1844–1916) — German anatomist and histologist · Christian Lovén (1835–1904) — Swedish physician and physiologist", "when_stamp": "1867 · 1901 · 1942 · 1974", "timeline_step": "1/3 · 1867 & 1901–1942 (Schwalbe & Lovén discover taste buds; Hänig's 1901 threshold data is misplotted by Boring in 1942 into the Tongue Map myth)", "hold_s": 3.8}),
            ("02_hanig_1901_true_threshold_curve_vs_boring_1942_normalized_tongue_map_and_collings_1974_chart", 79.5, 8.0, "E", False, "1901 DAVID PAULI HÄNIG (PHILOS. STUD.) TRUE THRESHOLD SENSITIVITY VS 1942 EDWIN BORING UNLABELLED GRAPH & 1974 VIRGINIA COLLINGS PROOF", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked David Pauli Hänig (1901 Philosophische Studien 17: 576–623) true threshold sensitivity curve vs Edwin Boring's (1942) normalized graph that spawned the false textbook Tongue Map & Virginia Collings's (1974) whole-tongue verification chart.",
             {"kind": "DATA", "label": "1901 HÄNIG TRUE THRESHOLD SENSITIVITY VS 1942 BORING NORMALIZED GRAPH & 1974 COLLINGS WHOLE-TONGUE VERIFICATION CHART", "detail": "Inked David Pauli Hänig (1901 Philosophische Studien 17: 576–623) true threshold sensitivity curve vs Edwin Boring's (1942) normalized graph that spawned the false textbook Tongue Map & Virginia Collings's (1974) whole-tongue verification chart on period paper", "scale": "the real sensitivity difference between the tip and the back of your tongue that Hänig measured in 1901 is smaller than the difference between one grain of sugar and two grains of sugar in a glass of water — yet a single unlabelled graph in 1942 turned that tiny ripple into a hundred-year textbook myth", "hold_s": 3.8}),
            ("03_leipzig_1901_philosophische_studien_boring_1942_book_and_1974_collings_filter_discs_closeup", 87.5, 6.5, "B", False, "1901–1974 — HÄNIG, BORING & COLLINGS", "Fast",
             "Fast: daylight macro shot of David Pauli Hänig's 1901 Philosophische Studien table, Edwin Boring's 1942 Sensation and Perception volume open to the four-curve graph, and Virginia Collings's 1974 filter-paper discs on a bench. Nothing emissive, no face.",
             STYLE + "In crisp daylight on a psychophysics library desk, an open 1901 German journal and a 1942 psychology volume showing a four-curve graph sit beside a glass dish of tiny filter-paper discs and brass forceps." + FAST_TAIL,
             None),
            ("04_brass_microscope_and_1867_histological_slide_of_papilla_trench_onion_taste_buds_pan", 94.0, 5.5, "C", False, "1867 — PAPILLAE VS MICROSCOPIC TASTE BUDS", "Fast",
             "Fast: daylight close-up pan across an 1867 brass monocular microscope and a stained glass histological slide next to a sculpted anatomical model showing onion-shaped taste buds tucked into the side trenches of a tongue papilla on an oak table. Nothing emissive, no face.",
             STYLE + "In bright window light on an oak table, an 1867 brass microscope and glass slide sit beside a painted cutaway model of a tongue papilla showing onion-shaped taste buds nestled in its side trenches." + FAST_TAIL,
             None),
        ],
    ),
    (
        3,
        "Part 03 — 25 July 1908: Kikunae Ikeda's 38 Kilograms of Konbu Kelp & the Discovery of Umami — Midpoint Twist",
        [
            ("01_kikunae_ikeda_25_jul_1908_tokyo_38kg_kelp_30g_glutamate_umami_and_kodama_1913_kuninaka_1960_synergy", 99.5, 6.5, "A", False, "38 KG KELP YIELDED UMAMI", "Quality",
             "Quality: readable faces (Japanese chemist Kikunae Ikeda at Tokyo Imperial University in 1907–25 July 1908 boiling 38 kilograms of dried konbu kelp in giant porcelain evaporating dishes and isolating 30 grams of pure L-glutamic acid / monosodium glutamate crystals to name umami, dissolving to Shintaro Kodama in 1913 with dried bonito IMP and Akira Kuninaka in 1960 with shiitake mushroom GMP discovering the 8-fold umami synergy).",
             STYLE + "Split period scene: on the left in 1908 Tokyo, chemist Kikunae Ikeda holds up a sample bottle of thirty grams of white glutamate crystals beside large porcelain evaporating dishes and bundles of dried kelp; on the right, Shintaro Kodama and Akira Kuninaka compare dried bonito flakes and shiitake mushrooms with crystal vials." + QUAL_TAIL,
             {"kind": "FACT", "label": "38 kg kelp yielded umami", "who_card": "Shintaro Kodama (fl. 1913) — Japanese chemist · Akira Kuninaka (born 1929) — Japanese microbiologist and biochemist", "when_stamp": "1907 · 25 July 1908 · 1913 · 1960", "timeline_step": "2/3 · 25 July 1908, 1913 & 1960 (Kikunae Ikeda extracts 30 g of glutamate from 38 kg of konbu kelp and names umami; Kodama and Kuninaka discover the 8× IMP/GMP synergy)", "hold_s": 3.8}),
            ("02_ikeda_1908_38kg_kelp_to_30g_glutamate_and_kuninaka_1960_8x_imp_gmp_umami_synergy_chart", 106.0, 8.0, "E", False, "25 JULY 1908 KIKUNAE IKEDA (38 KG KONBU KELP → 30 G L-GLUTAMIC ACID / MSG) & 1913/1960 KODAMA & KUNINAKA (8× IMP/GMP UMAMI SYNERGY)", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked Kikunae Ikeda (1908 J. Chem. Soc. Tokyo 30: 820–836) 38 kg konbu kelp → 30 g L-glutamic acid isolation & Akira Kuninaka (1960) 8× glutamate + IMP/GMP umami synergy curve.",
             {"kind": "DATA", "label": "1908 KIKUNAE IKEDA (38 KG KELP → 30 G GLUTAMATE) & 1960 AKIRA KUNINAKA (8× GLUTAMATE + IMP/GMP UMAMI SYNERGY) CHART", "detail": "Inked Kikunae Ikeda (1908 J. Chem. Soc. Tokyo 30: 820–836) 38 kg konbu kelp → 30 g L-glutamic acid isolation & Akira Kuninaka (1960) 8× glutamate + IMP/GMP umami synergy curve on period paper", "scale": "Kikunae Ikeda had to boil down thirty-eight kilograms of dried seaweed — a pile as heavy as a ten-year-old child — just to harvest thirty grams of pure umami crystals, barely enough to fill two tablespoons", "hold_s": 3.8}),
            ("03_tokyo_1908_glutamic_acid_sample_bottle_patent_and_1909_j_chem_soc_tokyo_paper_closeup", 114.0, 6.5, "B", False, "25 JULY 1908 — IKEDA DISCOVERS UMAMI", "Fast",
             "Fast: daylight macro shot of Kikunae Ikeda's 1908 glass sample bottle of L-glutamic acid crystals beside his porcelain evaporating basin, dried konbu kelp, and his 1909 Journal of the Chemical Society of Tokyo paper on a bench. Nothing emissive, no face.",
             STYLE + "In crisp daylight on a 1908 Tokyo chemistry bench, a stoppered glass sample bottle of white glutamate crystals sits beside a porcelain evaporating dish, dried kelp strips, and an open Japanese chemistry journal." + FAST_TAIL,
             None),
            ("04_umami_synergy_display_parmesan_tomato_beef_shiitake_and_kelp_bonito_dashi_bowls_pan", 120.5, 5.5, "C", False, "GLUTAMATE + RIBONUCLEOTIDES = 8× UMAMI SYNERGY", "Fast",
             "Fast: daylight close-up pan across three paired culinary ingredient sets on an oak table illustrating glutamate + nucleotide (IMP/GMP) synergy: aged cheese with ripe tomatoes, beef with shiitake mushrooms, and konbu kelp with bonito flakes. Nothing emissive, no face.",
             STYLE + "In bright window light on an oak table, three neatly arranged wooden trays display aged parmesan cheese beside ripe red tomatoes, dried shiitake mushrooms beside beef, and dried kelp beside bonito flakes." + FAST_TAIL,
             None),
        ],
    ),
    (
        4,
        "Part 04 — 1999–2002: Nirupa Chaudhari, Charles Zuker & Nicholas Ryba Discover the Molecular Locks for All Five Tastes (T1R, T2R, ENaC & OTOP1)",
        [
            ("01_chaudhari_2000_mglur4_and_zuker_ryba_2000_2002_t2r_bitter_t1r2_t1r3_sweet_and_t1r1_t1r3_umami_receptors", 126.0, 6.5, "A", False, "T1R1+T1R3 PROVED UMAMI", "Quality",
             "Quality: readable faces (neuroscientist Nirupa Chaudhari in 2000 identifying taste mGluR4 glutamate receptors and molecular biologists Charles S. Zuker and Nicholas J. P. Ryba in 2000–March 2002 identifying the 25 T2R bitter receptors, the T1R2+T1R3 sweet receptor, and the T1R1+T1R3 umami amino-acid receptor across all regions of the tongue).",
             STYLE + "Split period scene: on the left in 2000 Miami, neuroscientist Nirupa Chaudhari inspects a taste-bud receptor micrograph; on the right in 2002 San Diego and Bethesda, Charles Zuker and Nicholas Ryba stand beside a three-dimensional model of the heterodimeric T1R1+T1R3 umami and T1R2+T1R3 sweet receptor locks." + QUAL_TAIL,
             {"kind": "FACT", "label": "T1R1+T1R3 proved umami", "when_stamp": "1999 · 2000 · 2001 · March 2002 · 2018", "timeline_step": "3/3 · 1999–2002 (Nirupa Chaudhari, Charles Zuker, and Nicholas Ryba identify the T1R and T2R taste receptor families, proving T1R1+T1R3 is the dedicated molecular lock for umami)", "hold_s": 3.8}),
            ("02_chaudhari_2000_and_zuker_ryba_2000_2002_five_taste_molecular_receptor_table_chart", 132.5, 8.0, "E", False, "2000–2002 CHAUDHARI, ZUKER & RYBA (NATURE NEUROSCI., CELL & NATURE): 5-TASTE RECEPTOR TABLE (T1R2+T1R3, T1R1+T1R3, 25 T2RS, ENAC, OTOP1)", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked Chaudhari (2000 Nature Neurosci. 3: 113–119) & Zuker/Ryba (2000–2002 Cell 100: 693, Cell 106: 381 & Nature 416: 199–202) 5-taste molecular receptor table (Sweet = T1R2+T1R3; Umami = T1R1+T1R3 + mGluR4; Bitter = 25 T2Rs; Salty = ENaC Na⁺ channel; Sour = OTOP1 H⁺ channel).",
             {"kind": "DATA", "label": "2000–2002 CHAUDHARI, ZUKER & RYBA: FIVE-TASTE MOLECULAR RECEPTOR TABLE (T1R2+T1R3 SWEET, T1R1+T1R3 UMAMI, 25 T2R BITTER, ENAC, OTOP1)", "detail": "Inked Chaudhari (2000 Nature Neurosci. 3: 113–119) & Zuker/Ryba (2000–2002 Cell 100: 693, Cell 106: 381 & Nature 416: 199–202) 5-taste molecular receptor table (Sweet = T1R2+T1R3; Umami = T1R1+T1R3 + mGluR4; Bitter = 25 T2Rs; Salty = ENaC Na⁺ channel; Sour = OTOP1 H⁺ channel) on period paper", "scale": "human breast milk contains ten times more free glutamate than cow's milk — meaning the very first flavour a newborn baby's T1R1+T1R3 receptors fall in love with on day one of life is Kikunae Ikeda's fifth taste, umami", "hold_s": 3.8}),
            ("03_san_diego_2002_nature_amino_acid_receptor_issue_and_five_receptor_lock_models_closeup", 140.5, 6.5, "B", False, "2000–2002 — CHAUDHARI, ZUKER & RYBA'S TASTE RECEPTORS", "Fast",
             "Fast: daylight macro shot of the 14 March 2002 Nature issue ('An amino-acid taste receptor') and 2000–2001 Cell offprints beside five colour-coded molecular receptor models on a bench. Nothing emissive, no face.",
             STYLE + "In crisp daylight on a 2002 molecular biology bench, an open scientific journal sits beside five colour-coded sculpted protein receptor models mounted on brass stands." + FAST_TAIL,
             None),
            ("04_explorer_locking_glutamate_key_and_imp_pin_into_t1r1_t1r3_venus_flytrap_receptor_doorway", 147.0, 5.5, "B", True, None, "Quality",
             "Quality: Explorer beat 2 (locked character reference).",
             STYLE + "Standing before five sculpted molecular receptor doorways on a giant taste-bud cell surface, the Explorer inserts a golden glutamate key and a small nucleotide pin into the hinged Venus-flytrap jaws of the umami receptor doorway so its brass bell rings." + EXP_TAIL,
             None),
        ],
    ),
    (
        5,
        "Part 05 — Five Tastes Across Your Whole Tongue — & How Your Brain Blocks Pain With Its Own Morphine",
        [
            ("01_timeline_1867_2002_and_five_basic_tastes_tongue_map_umami_receptors_chart", 152.5, 8.5, "E", False, "1867–2002 TIMELINE · SCHWALBE-LOVÉN TASTE BUDS, HÄNIG-BORING TONGUE MAP MYTH, IKEDA UMAMI & CHAUDHARI-ZUKER-RYBA RECEPTORS", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, the 3-era timeline completes: 1867 & 1901–1942 (Gustav Schwalbe and Christian Lovén discover microscopic taste buds, and David Pauli Hänig measures small threshold differences around the tongue that Edwin Boring's 1942 graph accidentally turns into the false textbook Tongue Map) · 25 July 1908, 1913, 1960 & 1974 (Kikunae Ikeda in Tokyo boils 38 kg of konbu kelp down to 30 g of glutamate crystals to discover umami, Kodama and Kuninaka find the 8× nucleotide synergy, and Virginia Collings proves all tastes work across the whole tongue) · 1999–2002 (Nirupa Chaudhari, Charles Zuker, and Nicholas Ryba identify the T1R and T2R taste receptor families, proving T1R1+T1R3 is the dedicated molecular lock for umami).",
             {"kind": "DATA", "label": "1867–2002 TASTE BUDS, TONGUE MAP MYTH & UMAMI RECEPTORS TIMELINE · SCHWALBE, LOVÉN, HÄNIG, IKEDA, COLLINGS, CHAUDHARI, ZUKER & RYBA", "detail": "Animated timeline (1867 → 2002) alongside an inked summary of taste buds, the 1901–1942 Tongue Map myth, Kikunae Ikeda's 1908 umami extraction, and the 5-taste receptor families", "scale": "from a misread German graph that fooled schoolbooks for a century to a giant pot of Tokyo seaweed broth and the molecular locks on ten thousand taste buds, scientists revealed how every bite on your tongue tests the chemistry of life", "when_stamp": "1867–2002", "timeline_step": "3/3 · 1867–2002 timeline complete", "hold_s": 3.8}),
            ("02_five_taste_tongue_model_and_glutamate_crystals_beside_spinal_cord_gate_model_on_plinth_pan", 161.0, 5.5, "A", False, "SWEET, SALTY, SOUR, BITTER & UMAMI", "Fast",
             "Fast: daylight close-up of a sculpted five-taste human tongue model and Ikeda's glutamate crystal bottle beside a cutaway spinal-cord dorsal horn gate model on a wooden museum plinth. Nothing emissive, no face.",
             STYLE + "In crisp daylight on a wooden museum plinth, a sculpted human tongue model with five colour-coded taste bud locks sits beside a glass bottle of white glutamate crystals and a brass spinal-gate model." + FAST_TAIL,
             None),
            ("03_sherrington_1906_nociceptors_beecher_1944_anzio_melzack_wall_1965_pain_gate_and_pert_kosterlitz_1975_endorphins_handoff", 166.5, 6.5, "C", False, "NOCICEPTORS, ANZIO PARADOX, PAIN GATE & ENDORPHINS", "Quality",
             "Quality: readable faces (Charles Sherrington in 1906 mapping nociceptors, Henry Knowles Beecher in 1944 inside an Anzio beachhead medical tent, Ronald Melzack and Patrick Wall at MIT in 1965 unveiling the spinal Gate Control Theory of Pain, and Candace Pert, Solomon Snyder, John Hughes, and Hans Kosterlitz in 1973–1975 discovering opioid receptors and endorphins — handoff to 086 Pain, Gate Control & Endorphins).",
             STYLE + "Split period scene: on the left in 1944 Anzio, physician Henry Beecher speaks with a calm wounded soldier in a field tent beside Ronald Melzack and Patrick Wall's 1965 spinal gate diagram; on the right in 1973–1975, Candace Pert and Hans Kosterlitz inspect an opioid receptor lock-and-key model." + QUAL_TAIL,
             {"kind": "WHEN", "label": "1906 · 1944 · 1965 · 1975", "hold_s": 3.5}),
            ("04_table_three_callback", 173.0, 2.4, "C", False, None, "reuse",
             "Reuse: verified unused moving window [5.50s..7.90s] of P1:07_table_three_props_1901_camel_brush_vials_1908_porcelain_dish_glutamate_and_1974_filter_paper_discs (callback, £0).",
             "Reuse P1:07_table_three_props_1901_camel_brush_vials_1908_porcelain_dish_glutamate_and_1974_filter_paper_discs [5.50s..7.90s] (2.40s distinct non-overlapping tail window from 8.00s source clip).",
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
                row["reuse_of"] = "P1:07_table_three_props_1901_camel_brush_vials_1908_porcelain_dish_glutamate_and_1974_filter_paper_discs"
                row["reuse_window_s"] = [5.5, 7.9]
                row["reuse_audit"] = {
                    "source_row": "P1:07_table_three_props_1901_camel_brush_vials_1908_porcelain_dish_glutamate_and_1974_filter_paper_discs",
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
            "film": "085_Hanig-Ikeda-Collings-Zuker-Taste-Buds-Umami",
            "part": p_idx,
            "title": p_title,
            "version": "v01",
            "timing_status": "pre_vo_script_clock (built from taste_umami_script_master_v01.md; retimes onto Scribe STT once VO locks)",
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
        "film": "085_Hanig-Ikeda-Collings-Zuker-Taste-Buds-Umami",
        "version": "v01",
        "date": "2026-10-21",
        "owner": "gemini (J0753)",
        "status": "PRE_VO_BOARDS_V01_NO_MINT",
        "generation_authorized": False,
        "script": "00_Brand/Channel-Setup/ideas/085_Hanig-Ikeda-Collings-Zuker-Taste-Buds-Umami/taste_umami_script_master_v01.md",
        "sources": "00_Brand/Channel-Setup/ideas/085_Hanig-Ikeda-Collings-Zuker-Taste-Buds-Umami/SOURCES_v01.md",
        "credit_snapshot": {
            "flow_balance": 23740,
            "flow_floor": 0,
            "flow_read_at": "2026-10-15T21:42:22Z",
            "vertex_promo_gbp": 71.02,
            "vertex_usable_gbp": 70.02,
        },
        "totals": totals,
        "per_part": per_part_summary,
        "mint_order": "006 > 007 > 008 > 009 > 010 > 011 > 012 > 013 > 014 > 015 > 016 > 017 > 018 > 019 > 020 > 021 > 022 > 023 > 024 > 025 > 026 > 027 > 028 > 029 > 030 > 031 > 032 > 033 > 034 > 035 > 036 > 037 > 038 > 039 > 040 > 041 > 042 > 043 > 044 > 045 > 046 > 047 > 048 > 049 > 050 > 051 > 052 > 053 > 054 > 055 > 056 > 057 > 058 > 059 > 060 > 061 > 062 > 063 > 064 > 065 > 066 > 067 > 068 > 069 > 070 > 071 > 072 > 073 > 074 > 075 > 076 > 077 > 078 > 079 > 080 > 081 > 082 > 083 > 084 > 085 > 086. Nothing in 085 is generation_authorized.",
    }
    (EDIT / "PICTURE_PLAN_v01.json").write_text(json.dumps(plan, indent=2) + "\n")

    sl = [
        "# 085 Umami: Why Your School Tongue Map Was a Lie — Shot list & plate boards v01 (pre-VO)",
        "",
        "Gemini, 21 Oct 2026, J0753. Built from `taste_umami_script_master_v01.md` (`90.6/100 PASS`) and `SOURCES_v01.md`.",
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
        "# 085 price review v01 (pre-VO plate boards)",
        "",
        "Gemini, 21 Oct 2026, J0753. Boards only. **No mint. No spend. No merge.**",
        "Prepared from `taste_umami_script_master_v01.md` (`90.6/100 PASS`) and `SOURCES_v01.md` so 085's full plate board rows, non-emissive Fast prompts, £0 code graphics, and Teach-on-Screen overlays are ready to re-time the moment long VO locks. Parked for Chief.",
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
        f"- **Quality ({totals['Quality']} rows):** readable faces (Gustav Schwalbe, Christian Lovén, David Pauli Hänig, Edwin Garrigues Boring, Virginia B. Collings, Kikunae Ikeda, Shintaro Kodama, Akira Kuninaka, Nirupa Chaudhari, Charles S. Zuker, Nicholas J. P. Ryba, Henry Knowles Beecher, Candace Beebe Pert, Hans Walter Kosterlitz), 1901 Leipzig brush threshold test vs 1942 unlabelled `Tongue Map` myth & 1974 Pittsburgh filter-paper debunking, 25 July 1908 Tokyo `38 kg` *konbu* kelp extraction of `30 g` `L-glutamic acid / umami` & `8×` nucleotide synergy, 2000–2002 `T1R` and `T2R` receptor discoveries, and the 2 Explorer beats.",
        f"- **Fast ({totals['Fast']} rows, non-emissive):** daylight prop and laboratory shots (1901 *Philosophische Studien* volume with camel-hair brush, dried *konbu* kelp & glutamate crystal bottle pan, 3-object callback bench, 1901/1942/1974 journals with filter-paper taste discs, 1867 brass microscope & histological slide of papilla trench taste buds, 1908 Tokyo glutamic acid sample bottle with porcelain evaporating dish & 1909 *J. Chem. Soc. Tokyo* paper, culinary `8×` umami synergy display of parmesan/tomato, beef/shiitake & kelp/bonito, March 2002 *Nature* issue with 5 colour-coded receptor models, sculpted 5-taste tongue model & glutamate bottle beside spinal gate model on museum plinth). Zero candles, flames, sparks, or glowing elements on Fast.",
        f"- **£0 code graphics ({totals['code_graphic']} rows):**",
        "  1. `P1:04_hanig_1901_boring_1942_ikeda_1908_38kg_kelp_and_zuker_2002_five_taste_receptor_chart` — Kikunae Ikeda (1908) `38,000 g` dried *konbu* kelp → `30 g` L-glutamic acid (`umami`) crystal extraction & 5-taste receptor threshold comparison (`bitter quinine ~0.000008 M` vs `sweet sucrose ~0.01 M`) (`SCALE: your bitter taste receptors are more than a thousand times more sensitive than your sweet receptors — because missing a spoonful of sugar only costs you a few calories, whereas swallowing a single mouthful of bitter plant poison could cost you your life`)",
        "  2. `P1:06_zuker_ryba_2001_2002_t1r2_t1r3_sweet_t1r1_t1r3_umami_and_25_t2r_bitter_receptor_chart` — Charles Zuker & Nicholas Ryba (2001–2002 *Cell* & *Nature*) `T1R2+T1R3` (Sweet), `T1R1+T1R3` (Umami + `8×` IMP/GMP synergy) & 25-gene `T2R` (Bitter) receptor architecture (`SCALE: your cells replace every worn-out taste bud receptor every ten to fourteen days — which is why scalding your tongue on hot soup only dulls your taste for a few days before a brand-new set of taste buds grows back`)",
        "  3. `P2:02_hanig_1901_true_threshold_curve_vs_boring_1942_normalized_tongue_map_and_collings_1974_chart` — David Pauli Hänig (1901 *Philosophische Studien*) true threshold sensitivity curve vs Edwin Boring's (1942) normalized graph & Virginia Collings's (1974) whole-tongue verification chart (`SCALE: the real sensitivity difference between the tip and the back of your tongue that Hänig measured in 1901 is smaller than the difference between one grain of sugar and two grains of sugar in a glass of water — yet a single unlabelled graph in 1942 turned that tiny ripple into a hundred-year textbook myth`)",
        "  4. `P3:02_ikeda_1908_38kg_kelp_to_30g_glutamate_and_kuninaka_1960_8x_imp_gmp_umami_synergy_chart` — Kikunae Ikeda (1908 *J. Chem. Soc. Tokyo*) `38 kg` kelp → `30 g` L-glutamic acid isolation & Akira Kuninaka (1960) `8×` glutamate + IMP/GMP umami synergy curve (`SCALE: Kikunae Ikeda had to boil down thirty-eight kilograms of dried seaweed — a pile as heavy as a ten-year-old child — just to harvest thirty grams of pure umami crystals, barely enough to fill two tablespoons`)",
        "  5. `P4:02_chaudhari_2000_and_zuker_ryba_2000_2002_five_taste_molecular_receptor_table_chart` — Nirupa Chaudhari (2000 *Nat. Neurosci.*) & Charles Zuker / Nicholas Ryba (2000–2002 *Cell* & *Nature*) 5-taste molecular receptor table (`SCALE: human breast milk contains ten times more free glutamate than cow's milk — meaning the very first flavour a newborn baby's T1R1+T1R3 receptors fall in love with on day one of life is Kikunae Ikeda's fifth taste, umami`)",
        "  6. `P5:01_timeline_1867_2002_and_five_basic_tastes_tongue_map_umami_receptors_chart` — completed timeline (1867 → 2002) + taste buds, the 1901–1942 Tongue Map myth, Ikeda's 1908 umami discovery & the 5-taste receptor locks (`SCALE: from a misread German graph that fooled schoolbooks for a century to a giant pot of Tokyo seaweed broth and the molecular locks on ten thousand taste buds, scientists revealed how every bite on your tongue tests the chemistry of life`)",
        f"- **£0 verified reuse ({totals['reuse']} row):** `P5:04_table_three_callback` uses the 2.40 s unused moving tail `[5.50s..7.90s]` of `P1:07_table_three_props_1901_camel_brush_vials_1908_porcelain_dish_glutamate_and_1974_filter_paper_discs`.",
        "",
        "## Mint order",
        "",
        "006 > 007 > 008 > 009 > 010 > 011 > 012 > 013 > 014 > 015 > 016 > 017 > 018 > 019 > 020 > 021 > 022 > 023 > 024 > 025 > 026 > 027 > 028 > 029 > 030 > 031 > 032 > 033 > 034 > 035 > 036 > 037 > 038 > 039 > 040 > 041 > 042 > 043 > 044 > 045 > 046 > 047 > 048 > 049 > 050 > 051 > 052 > 053 > 054 > 055 > 056 > 057 > 058 > 059 > 060 > 061 > 062 > 063 > 064 > 065 > 066 > 067 > 068 > 069 > 070 > 071 > 072 > 073 > 074 > 075 > 076 > 077 > 078 > 079 > 080 > 081 > 082 > 083 > 084 > 085 > 086. `generation_authorized` is `false` on every row.",
    ])
    (EDIT / "PRICE_REVIEW_v01.md").write_text("\n".join(pr_lines) + "\n")
    print(f"085 v01 boards written: {totals['rows']} rows, Flow expected={totals['flow_credits_expected']}")


if __name__ == "__main__":
    main()
