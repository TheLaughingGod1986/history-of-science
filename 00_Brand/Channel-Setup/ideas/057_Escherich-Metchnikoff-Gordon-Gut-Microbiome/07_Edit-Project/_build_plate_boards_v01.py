#!/usr/bin/env python3
"""HOS 057 (The Gut Microbiome: 38 Trillion Bacteria Inside You) pre-VO plate boards v01. J0615. No mint, no spend.

Built from 00_Brand/Channel-Setup/ideas/057_Escherich-Metchnikoff-Gordon-Gut-Microbiome/microbiome_script_master_v01.md
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
        "Part 01 — Why Your Own DNA Can't Digest an Apple Without 38 Trillion Helpers",
        [
            ("01_apple_slice_digestive_tract_and_38_trillion_colon_bacteria_fermenting_fibre", 0.0, 5.5, "A", False, "38 TRILLION GUT BACTERIA", "Quality",
             "Quality: Short frame 0 / answer image (0:03) + a crisp red apple slice travels down a cross-section of the human digestive tract: in the small intestine, human enzymes absorb simple sugars while tough plant-fibre chains pass through untouched into the colon, where 38 trillion gut bacteria swarm over the fibres with molecular scissors and turn them into golden short-chain fatty-acid fuel.",
             STYLE + "Split anatomical-and-microscopic scene: on the left, a slice of red apple passes through the small intestine into the large intestine; on the right, swarms of friendly rod-shaped gut bacteria snip tangled green plant-fibre chains into golden nutrient droplets that feed the colon wall." + QUAL_TAIL,
             {"kind": "WHEN", "label": "MUNICH, 14 JULY 1885", "timeline_step": "1/4 · 14 Jul 1885 (Theodor Escherich discovers Bacterium coli commune / E. coli colonizing healthy newborn infants within hours of birth)", "hold_s": 3.5}),
            ("02_escherich_1885_metchnikoff_1907_reyniers_gustafsson_1946_and_gordon_2006_split", 5.5, 6.0, "B", False, "INFANT MICROBES, STERILE BUBBLES, 2 MILLION GENES", "Quality",
             "Quality: complex three-part composition (Theodor Escherich in Munich on 14 July 1885 examining newborn infant gut bacteria under his brass microscope and Élie Metchnikoff in Paris in 1907 drinking a bowl of sour Bulgarian yogurt; James Reyniers and Bengt Gustafsson in 1946–1959 peering through thick glass portholes into a pressurized stainless-steel germ-free mouse isolator; and Jeffrey Gordon at Washington University in St. Louis in 1996–2006 sequencing gut microbiome DNA).",
             STYLE + "Three-panel period composition: on the left, Theodor Escherich at a brass microscope in 1885 and Élie Metchnikoff holding a porcelain bowl of yogurt in 1907 Paris; in the centre, Bengt Gustafsson reaching through black rubber gloves into a steel germ-free mouse isolator tank in 1959; on the right, Jeffrey Gordon in 2006 St. Louis inspecting a gut microbiome gene map." + QUAL_TAIL,
             None),
            ("03_17_human_carb_enzymes_vs_tens_of_thousands_microbial_cazyme_scissors_split", 11.5, 6.0, "C", False, "17 HUMAN ENZYMES VS TENS OF THOUSANDS", "Quality",
             "Quality: complex anatomical and biochemical reveal (split comparison of a human intestinal cell holding a thin manual of just 17 carbohydrate-digesting enzymes capable of snipping only starch, table sugar, and milk lactose against a teeming gut bacterium deploying hundreds of plant-fibre enzymes slicing complex apple pectin and oat beta-glucan into butyrate fuel for the colon wall).",
             STYLE + "Split cellular scene: on the left, a human intestinal cell holds a tiny keyring of seventeen small scissors that bounce off a thick braided cable of apple pectin fibre; on the right, a friendly Bacteroides microbe deploys rows of specialised shears that cleanly slice the pectin cable into golden fuel blocks." + QUAL_TAIL,
             {"kind": "WHEN", "label": "14 JULY 1885 · 1907 · 1946 · 1959 · 21 DECEMBER 2006", "timeline_step": "1/4 · 14 Jul 1885 (Escherich) · 2/4 · 1907 (Metchnikoff) · 3/4 · 1946–1959 (Reyniers & Gustafsson) · 4/4 · 28 Mar 2003 & 21 Dec 2006 (Gordon, Hooper, Ley & Turnbaugh)", "hold_s": 3.5}),
            ("04_sender_milo_2016_and_gordon_2006_30t_human_cells_vs_38t_gut_bacteria_2m_genes_chart", 17.5, 8.0, "E", False, "30T HUMAN CELLS (20,000 GENES, 17 CARB ENZYMES) VS 38T GUT BACTERIA (0.2 KG, >2 MILLION GENES, THOUSANDS OF FIBRE CAZYMES)", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked human-vs-microbiome cell and gene census chart from Sender, Fuchs & Milo (August 2016, PLOS Biology 14: e1002533) and Turnbaugh, Ley & Gordon (21 December 2006, Nature 444: 1027–1031) compares ~30 trillion human cells (~20,000 human protein-coding genes, only ~17 carbohydrate enzymes) against ~38 trillion gut bacteria (~0.2 kg wet weight, >2,000,000 microbial genes, and >10,000 carbohydrate-active enzymes).",
             {"kind": "DATA", "label": "30T HUMAN CELLS (20,000 GENES, 17 CARB ENZYMES) VS 38T GUT BACTERIA (>2M GENES, 261 ENZYMES IN 1 SPECIES)", "detail": "Inked human vs gut microbiome census chart on period paper comparing 30 trillion human cells (20,000 human genes; 17 digestive carb enzymes) against 38 trillion bacterial cells in the colon (0.2 kg mass; >2 million microbial genes; thousands of fibre-digesting CAZymes)", "scale": "by cell count you are less than half human — for every ten human cells in your body, roughly thirteen microscopic bacteria ride along inside your gut, carrying a hundred times more genes than your own DNA", "who_card": "Theodor Escherich (1857–1911) — German-Austrian paediatrician · Élie Metchnikoff (1845–1916) — Russian-French immunologist · James A. Reyniers (1908–1967) — American bacteriologist · Bengt E. Gustafsson (1916–1986) — Swedish physician · Carl R. Woese (1928–2012) — American microbiologist · Jeffrey I. Gordon (born 1947) — American physician-scientist", "when_stamp": "14 July 1885 · 1907 · 1946 · 1959 · 21 December 2006", "hold_s": 3.8}),
            ("05_apple_oats_yogurt_bowl_and_brass_microscope_slide_pan", 25.5, 5.5, "A", False, "100× MORE MICROBIAL GENES", "Fast",
             "Fast: daylight macro pan across a sliced red apple, a wooden scoop of rolled oats, a porcelain bowl of Bulgarian yogurt, and a brass microscope slide on an oak bench between code graphics so two full-frame graphics never run back to back. Nothing emissive, no face.",
             STYLE + "In crisp daylight on an oak laboratory bench, the camera pans smoothly across a fresh red apple slice, a wooden scoop of rolled oats, a white porcelain bowl of thick yogurt, and a stained glass microscope slide." + FAST_TAIL,
             None),
            ("06_gustafsson_1959_germ_free_vs_colonized_mouse_30pct_calories_5x_caecum_vitamin_k_chart", 31.0, 8.0, "E", False, "+30% MORE FOOD WITHOUT GUT MICROBES", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked germ-free vs conventional mouse nutrition & Vitamin K chart from Gustafsson (1948/1959) and Wostmann (1981) shows a sterile isolator mouse requiring ~30% more calories to maintain body weight, with a 5× enlarged caecum and lethal Vitamin K bleeding unless supplemented, compared to a microbiome-colonized mouse fermenting plant fibres into short-chain fatty acids and synthesizing Vitamin K and B vitamins.",
             {"kind": "DATA", "label": "GERM-FREE MOUSE (+30% CALORIES, 5× CAECUM, 0 VITAMIN K) VS COLONIZED MOUSE (FIBRE FERMENTATION & VITAMIN K SYNTHESIS)", "detail": "Inked germ-free isolator mouse vs conventional mouse comparison chart showing +30% calorie requirement, 5× enlarged caecum of undigested fibre, and 0 endogenous Vitamin K synthesis in sterile mice vs normal weight, fibre fermentation, and microbial Vitamin K synthesis in colonized mice", "scale": "without gut bacteria, a mouse has to eat nearly a third more food just to stay the same weight — because the calories locked inside plant fibre pass straight through its body untouched", "hold_s": 3.8}),
            ("07_table_three_props_escherich_1885_slide_metchnikoff_1907_yogurt_jar_and_germ_free_glove_port", 39.0, 5.5, "C", False, "1885 TO 2016", "Fast",
             "Fast: daylight prop table (callback source for Part 05: Theodor Escherich's 1885 stained infant microbe slide box, Élie Metchnikoff's 1907 stoneware Bulgarian yogurt jar, and a polished steel germ-free isolator porthole ring). Nothing emissive.",
             STYLE + "On an oak workbench in soft window light sit three objects side by side: a wooden slide box of stained rod bacteria, a stoneware jar of Bulgarian sour milk, and a bolted stainless-steel isolator porthole ring." + FAST_TAIL,
             None),
            ("08_explorer_17_tooth_human_pocketknife_vs_bacteroides_261_blade_fibre_sawmill_butyrate", 62.0, 5.5, "A", True, None, "Quality",
             "Quality: Explorer beat 1 (locked character reference, after 1:00).",
             STYLE + "Standing beside a tangled bundle of green apple-and-oat plant fibre beams, the Explorer tries to saw a thick beam with a tiny seventeen-tooth pocketknife, then steps back smiling as a friendly cylindrical Bacteroides machine rolls up with spinning multi-blade shears and slices the fibre into golden butyrate fuel blocks." + EXP_TAIL,
             None),
            ("09_metchnikoff_1907_paris_lifting_porcelain_bowl_of_bulgarian_yogurt_beside_microscope", 67.5, 5.5, "B", False, "PARIS, 1907", "Quality",
             "Quality: readable face (in Paris in 1907, bearded Russian-French immunologist Élie Metchnikoff lifts a porcelain bowl of fermented Bulgarian sour milk beside his brass microscope at the Pasteur Institute).",
             STYLE + "In a 1907 Pasteur Institute laboratory in Paris, bearded immunologist Élie Metchnikoff in a white lab coat holds a porcelain bowl of Bulgarian sour milk beside a brass microscope and glass culture flasks." + QUAL_TAIL,
             {"kind": "WHEN", "label": "PARIS, 1907", "timeline_step": "2/4 · 1907 (Élie Metchnikoff proposes lactic-acid probiotics in Bulgarian yogurt)", "hold_s": 3.5}),
        ],
    ),
    (
        2,
        "Part 02 — 14 July 1885 & 1907: Theodor Escherich's Newborn Microbe Mystery & Élie Metchnikoff's Bulgarian Yogurt",
        [
            ("01_escherich_14_jul_1885_munich_newborn_ecoli_and_grigorov_metchnikoff_1907_bulgarian_yogurt", 73.0, 6.5, "A", False, "BORN STERILE, COLONIZED IN HOURS", "Quality",
             "Quality: readable faces (German-Austrian paediatrician Theodor Escherich on 14 July 1885 in Munich discovering rod-shaped Bacterium coli commune / E. coli in healthy newborn infants, dissolving to Bulgarian physician Stamen Grigorov in 1905 Geneva and Élie Metchnikoff in 1907 Paris examining Lactobacillus bulgaricus in Bulgarian sour milk).",
             STYLE + "Split period scene: on the left in 1885 Munich, young paediatrician Theodor Escherich inspects stained microscope slides of rod-shaped newborn gut bacteria; on the right in 1905–1907, Stamen Grigorov and Élie Metchnikoff examine Lactobacillus rods from stoneware bowls of Bulgarian yogurt." + QUAL_TAIL,
             {"kind": "FACT", "label": "Born sterile, colonized in hours", "who_card": "Stamen Grigorov (1878–1945) — Bulgarian physician", "when_stamp": "14 July 1885 · 1905 · 1907", "timeline_step": "1/4 · 14 Jul 1885 (Escherich newborn E. coli) & 2/4 · 1905–1907 (Grigorov & Metchnikoff Lactobacillus bulgaricus probiotics)", "hold_s": 3.8}),
            ("02_escherich_1885_newborn_colonization_10e10_per_gram_and_metchnikoff_1907_lactic_acid_ph_chart", 79.5, 8.0, "E", False, "14 JUL 1885 ESCHERICH & 1907 METCHNIKOFF: NEWBORN COLONIZATION (>10⁹–10¹⁰ BACTERIA/G) & LACTIC ACID FERMENTATION (PH ~4.0–4.5)", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked infant gut colonization & lactic-acid fermentation chart from Escherich (14 July 1885, Fortschritte der Medicin) and Metchnikoff (1907, The Prolongation of Life) shows a newborn's sterile digestive tract reaching >10⁹–10¹⁰ bacteria per gram of colon contents within days of birth, alongside Lactobacillus bulgaricus fermenting milk lactose into lactic acid (pH ~4.0–4.5) to suppress putrefactive microbes.",
             {"kind": "DATA", "label": "14 JUL 1885 & 1907: NEWBORN GUT COLONIZATION (>10¹⁰ BACTERIA/G IN DAYS) & LACTIC ACID FERMENTATION (PH 4.0–4.5)", "detail": "Inked infant gut colonization & lactic-acid fermentation chart on period paper from Escherich (14 July 1885, Fortschritte der Medicin) and Metchnikoff (1907, The Prolongation of Life) showing a newborn's sterile digestive tract reaching >10⁹–10¹⁰ bacteria per gram of colon contents within days of birth, alongside Lactobacillus bulgaricus fermenting milk lactose into lactic acid (pH ~4.0–4.5) to suppress putrefactive microbes", "scale": "inside a single gram of contents from your lower gut — a pinch no bigger than a paperclip — live more individual bacteria than there are human beings on the entire planet Earth", "hold_s": 3.8}),
            ("03_pasteur_institute_1907_prolongation_of_life_book_stoneware_yogurt_jug_and_bacilli_slide", 87.5, 6.5, "B", False, "1907 — THE FIRST PROBIOTIC", "Fast",
             "Fast: daylight macro shot of Metchnikoff's 1907 book beside a stoneware jug of Bulgarian fermented milk, a porcelain spoon, and a stained microscope slide of rod-shaped lactic-acid bacilli on a Paris oak table. Nothing emissive, no face.",
             STYLE + "In crisp daylight on a wooden laboratory table, a leather-bound volume sits beside a stoneware jug of thick fermented milk, a porcelain spoon, and a glass slide under a brass microscope." + FAST_TAIL,
             None),
            ("04_munich_1885_agar_culture_tubes_brass_microscope_and_infant_clinic_notebook_pan", 94.0, 5.5, "C", False, "14 JULY 1885 — ESCHERICHIA COLI", "Fast",
             "Fast: daylight close-up pan across 1885 glass gelatin-and-agar culture tubes in a wooden rack beside a brass monocular microscope and inked drawings of rod-shaped bacteria. Nothing emissive, no face.",
             STYLE + "In bright window light on an 1885 Munich clinic desk, a wooden rack of stoppered glass culture tubes sits beside a brass microscope and an open notebook sketched with rod-shaped bacteria." + FAST_TAIL,
             None),
        ],
    ),
    (
        3,
        "Part 03 — 1946–1959: The Germ-Free Bubble Mice That Needed 30% More Food & Bled Without Vitamin K — Midpoint Twist",
        [
            ("01_reyniers_1946_notre_dame_and_gustafsson_1959_lund_germ_free_steel_isolator_mice", 99.5, 6.5, "A", False, "STERILE MICE EAT 30% MORE", "Quality",
             "Quality: readable faces (American bacteriologist James Reyniers at Notre Dame in 1946 and Swedish physician Bengt Gustafsson at Lund University in 1948–1959 reaching through shoulder-length black rubber gloves bolted into pressurized stainless-steel germ-free isolator tanks to hand-feed sterile baby rats and mice).",
             STYLE + "Split period scene: on the left in 1946 Indiana, James Reyniers peers through a circular glass porthole while working inside a riveted stainless-steel germ-free isolator drum; on the right in 1959 Sweden, Bengt Gustafsson uses built-in black rubber gauntlets to feed sterile white rodents inside a sterile chamber." + QUAL_TAIL,
             {"kind": "FACT", "label": "Sterile mice eat 30% more", "when_stamp": "1946 · 1948 · 1959", "timeline_step": "3/4 · 1946–1959 (Reyniers & Gustafsson raise germ-free isolator rodents, proving gut bacteria synthesize Vitamin K and harvest ~30% more dietary energy)", "hold_s": 3.8}),
            ("02_reyniers_1946_gustafsson_1959_gnotobiotic_4_metric_caecum_calories_vitamin_k_immune_chart", 106.0, 8.0, "E", False, "1946–1959 GERM-FREE ISOLATOR PROOF: 5× SWOLLEN CAECUM, +30% CALORIC INTAKE, LETHAL VITAMIN K HAEMORRHAGE & SHRUNKEN IMMUNE TISSUE", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked gnotobiotic isolator physiology chart from Reyniers (1946) and Gustafsson (1948, 1959, Annals of the New York Academy of Sciences) compares germ-free vs conventional rodents across 4 metrics: caecum weight (5× larger in germ-free), daily caloric intake (+30% higher in germ-free), clotting time without dietary Vitamin K (lethal haemorrhage in germ-free vs normal clotting in colonized within 24–48 h), and intestinal lymphoid tissue (severely underdeveloped in germ-free).",
             {"kind": "DATA", "label": "1946–1959 GNOTOBIOTIC ISOLATORS: 5× CAECUM, +30% CALORIES, VITAMIN K CLOTTING IN 24–48 H & IMMUNE TRAINING", "detail": "Inked gnotobiotic isolator physiology chart on period paper from Reyniers (1946) and Gustafsson (1948, 1959, Annals of the New York Academy of Sciences) comparing germ-free vs conventional rodents across 4 metrics: caecum weight (5× larger in germ-free), daily caloric intake (+30% higher in germ-free), clotting time without dietary Vitamin K (lethal haemorrhage in germ-free vs normal clotting in colonized within 24–48 h), and intestinal lymphoid tissue (severely underdeveloped in germ-free)", "scale": "raising a mouse without gut bacteria is like trying to run a city without power plants, recycling crews, or a fire brigade — the mouse has to eat nearly a third more food just to stay warm, and a tiny scratch can bleed uncontrollably without bacterial Vitamin K", "hold_s": 3.8}),
            ("03_lund_1959_stainless_steel_isolator_porthole_rubber_gauntlets_and_vitamin_k_vials_closeup", 114.0, 6.5, "B", False, "MAY 1959 — MICROBIAL VITAMIN K", "Fast",
             "Fast: daylight macro shot of a stainless-steel germ-free isolator porthole with bolted black rubber gauntlets, autoclaved feed cylinders, and glass Vitamin K clotting test tubes. Nothing emissive, no face.",
             STYLE + "In crisp daylight inside a 1959 laboratory, a polished stainless-steel isolator tank with a thick glass porthole and black rubber gauntlets sits beside autoclaved feed canisters and glass clotting tubes." + FAST_TAIL,
             None),
            ("04_autoclaved_feed_scale_and_5x_caecum_anatomical_comparison_models_pan", 120.5, 5.5, "C", False, "1946 — GERM-FREE ISOLATORS", "Fast",
             "Fast: daylight close-up pan across a brass laboratory balance weighing 30% extra autoclaved pellets beside two anatomical gut models comparing a normal rodent caecum against a 5-fold swollen germ-free caecum. Nothing emissive, no face.",
             STYLE + "In bright window light on a laboratory bench, a brass balance scale heaped with extra feed pellets sits beside two painted anatomical models comparing a compact normal caecum and a five-times-larger distended caecum." + FAST_TAIL,
             None),
        ],
    ),
    (
        4,
        "Part 04 — 1977 & 1996–21 December 2006: Why 80% of Gut Microbes Hate Oxygen, Carl Woese's 16S Barcode & Jeffrey Gordon's Microbiome Revolution",
        [
            ("01_woese_1977_16s_rrna_and_gordon_hooper_ley_2003_2006_bacteroides_261_enzymes", 126.0, 6.5, "A", False, "1 BACTERIUM = 261 FIBRE ENZYMES", "Quality",
             "Quality: readable faces (Carl Woese in November 1977 reading 16S ribosomal RNA sequences, dissolving to Jeffrey Gordon, Lora Hooper, and Ruth Ley in St. Louis on 28 March 2003 – 21 December 2006 colonizing sterile mice with Bacteroides thetaiotaomicron and mapping its 261 fibre-digesting enzymes).",
             STYLE + "Split period scene: on the left in November 1977 Illinois, microbiologist Carl Woese inspects a backlit 16S ribosomal RNA fingerprint film; on the right in 2003–2006 St. Louis, Jeffrey Gordon, Lora Hooper, and Ruth Ley examine an anaerobic chamber and genome map showing two hundred and sixty-one carbohydrate enzymes." + QUAL_TAIL,
             {"kind": "FACT", "label": "1 bacterium = 261 fibre enzymes", "who_card": "Lora V. Hooper (born 1966) — American immunologist · Ruth E. Ley (born 1970) — British-American microbial ecologist", "when_stamp": "November 1977 · 28 March 2003 · 21 December 2006 · August 2016", "timeline_step": "4/4 · 28 Mar 2003 & 21 Dec 2006 (Gordon, Hooper, Ley & Turnbaugh sequence Bacteroides thetaiotaomicron's 261 fibre enzymes and prove the gut microbiome's metabolic & immune role; 2016 Sender & Milo 38T census)", "hold_s": 3.8}),
            ("02_xu_gordon_28_mar_2003_science_17_human_vs_261_bacteroides_enzymes_and_butyrate_colonocyte_chart", 132.5, 8.0, "E", False, "28 MAR 2003 & 21 DEC 2006: 17 HUMAN CARB ENZYMES VS 261 IN B. THETAIOTAOMICRON & SHORT-CHAIN FATTY ACIDS (60–70% OF COLON CELL ENERGY)", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked carbohydrate enzyme & colonocyte energy chart from Xu et al. & Gordon (28 March 2003, Science 299: 2074–2076) and Turnbaugh, Ley & Gordon (21 December 2006, Nature 444: 1027–1031) compares the human genome's ~17 digestive glycoside hydrolases against Bacteroides thetaiotaomicron's 261 glycoside hydrolases (and thousands across the whole microbiome), converting dietary plant fibre into short-chain fatty acids (butyrate, propionate, acetate) that supply 60–70% of colon cell energy.",
             {"kind": "DATA", "label": "17 HUMAN CARB ENZYMES VS 261 IN BACTEROIDES THETAIOTAOMICRON → BUTYRATE SUPPLIES 60–70% OF COLON WALL ENERGY", "detail": "Inked carbohydrate enzyme & colonocyte energy chart on period paper from Xu et al. & Gordon (28 March 2003, Science 299: 2074–2076) and Turnbaugh, Ley & Gordon (21 December 2006, Nature 444: 1027–1031) comparing the human genome's ~17 digestive glycoside hydrolases against Bacteroides thetaiotaomicron's 261 glycoside hydrolases (and thousands across the whole microbiome), converting dietary plant fibre into short-chain fatty acids (butyrate, propionate, acetate) that supply 60–70% of colon cell energy", "scale": "one single species of friendly gut bacterium carries fifteen times more fibre-digesting tools than the entire human genome — turning tough plant cell walls that would pass straight through us into the very fuel that keeps the lining of our gut alive", "hold_s": 3.8}),
            ("03_anaerobic_glove_box_16s_rrna_barcode_gel_and_short_chain_fatty_acid_models_closeup", 140.5, 6.5, "B", False, "BUTYRATE FEEDS YOUR COLON WALL", "Fast",
             "Fast: daylight macro shot of an anaerobic chamber airlock beside a 16S rRNA barcode sequence print and ball-and-stick models of butyrate, propionate, and acetate on a wooden bench. Nothing emissive, no face.",
             STYLE + "In crisp daylight on a microbiology workbench, a sealed anaerobic glove-box airlock sits beside a printed 16S RNA barcode strip and wooden ball-and-stick models of short-chain fatty acids." + FAST_TAIL,
             None),
            ("04_explorer_scanning_anaerobic_gut_microbes_with_16s_barcode_reader_and_feeding_butyrate_brick", 147.0, 5.5, "B", True, None, "Quality",
             "Quality: Explorer beat 2 (locked character reference).",
             STYLE + "Standing inside a vaulted colon chamber, the Explorer holds a brass barcode reader lens that reveals neat striped tags on rows of friendly anaerobic bacteria, then hands a golden butyrate fuel block to a smiling colon-wall cell." + EXP_TAIL,
             None),
        ],
    ),
    (
        5,
        "Part 05 — Why Feeding Your Gut Fibre Feeds You — & How Scientists Rewound an Adult Cell Back Into an Embryo",
        [
            ("01_timeline_1885_2016_and_dietary_fibre_to_butyrate_colon_barrier_chart", 152.5, 8.5, "E", False, "1885–2016 TIMELINE · ESCHERICH E. COLI, METCHNIKOFF PROBIOTICS, GERM-FREE ISOLATORS, GORDON 261 FIBRE ENZYMES & 38T MICROBIOME CENSUS", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, the 4-date timeline completes: 14 Jul 1885 (Theodor Escherich discovers Bacterium coli commune / E. coli colonizing healthy newborn infants within hours of birth) · 1907 (Élie Metchnikoff proposes lactic-acid probiotics in Bulgarian yogurt) · 1946–1959 (Reyniers & Gustafsson raise germ-free isolator rodents, proving gut bacteria synthesize Vitamin K and harvest ~30% more dietary energy) · 28 Mar 2003 & 21 Dec 2006 (Jeffrey Gordon, Lora Hooper, Ruth Ley & Peter Turnbaugh sequence Bacteroides thetaiotaomicron's 261 fibre enzymes and prove the gut microbiome's metabolic & immune role; 2016 Sender & Milo census of ~38 trillion bacteria vs ~30 trillion human cells).",
             {"kind": "DATA", "label": "1885–2016 GUT MICROBIOME TIMELINE · 38T BACTERIA (>2M GENES) FERMENTING FIBRE INTO BUTYRATE & VITAMIN K", "detail": "Animated 4-date timeline (1885 → 2016) alongside the dietary plant fibre → microbial fermentation → butyrate & immune T-cell regulation diagram", "scale": "every meal you eat is a banquet for two — your human enzymes take the simple sugars up front, while thirty-eight trillion ancient microbial partners in the back turn indigestible plants into vitamins, fuel, and lifelong immunity", "when_stamp": "1885–2016", "timeline_step": "4/4 · 1885–2016 timeline complete", "hold_s": 3.8}),
            ("02_oats_apples_beans_and_butyrate_molecular_model_on_museum_plinth_pan", 161.0, 5.5, "A", False, "FIBRE FEEDS 38 TRILLION HELPERS", "Fast",
             "Fast: daylight close-up of a bowl of oats, sliced apples, and beans beside a wooden molecular model of butyrate and a stoneware yogurt jar on a museum plinth. Nothing emissive, no face.",
             STYLE + "In crisp daylight on a wooden museum plinth, bowls of oats, sliced apples, and beans sit beside a wooden ball-and-stick butyrate model and a stoneware yogurt jar." + FAST_TAIL,
             None),
            ("03_mcculloch_till_1961_gurdon_1962_tadpole_and_yamanaka_2006_4_gene_ipsc_stem_cells_handoff", 166.5, 6.5, "C", False, "4 GENES REWIND AN ADULT CELL", "Quality",
             "Quality: readable faces (Ernest McCulloch and James Till in February 1961 counting mouse spleen colonies, John Gurdon at Oxford in December 1962 cloning a swimming frog tadpole from an adult gut cell, and Shinya Yamanaka in Kyoto on 25 August 2006 rewinding an adult skin cell back into an embryo with 4 master genes — handoff to 058 Stem Cells & iPSCs).",
             STYLE + "Split period scene: on the left in December 1962 Oxford, young biologist John Gurdon transfers an adult frog gut nucleus with a glass micropipette beside a dish of swimming tadpoles and Ernest McCulloch and James Till's spleen-colony slides; on the right in August 2006 Kyoto, Shinya Yamanaka inspects a dish of reprogrammed induced pluripotent stem cells." + QUAL_TAIL,
             {"kind": "WHEN", "label": "FEBRUARY 1961 · DECEMBER 1962 · 25 AUGUST 2006", "hold_s": 3.5}),
            ("04_table_three_callback", 173.0, 2.4, "C", False, None, "reuse",
             "Reuse: verified unused moving window [5.50s..7.90s] of P1:07_table_three_props_escherich_1885_slide_metchnikoff_1907_yogurt_jar_and_germ_free_glove_port (callback, £0).",
             "Reuse P1:07_table_three_props_escherich_1885_slide_metchnikoff_1907_yogurt_jar_and_germ_free_glove_port [5.50s..7.90s] (2.40s distinct non-overlapping tail window from 8.00s source clip).",
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
                row["reuse_of"] = "P1:07_table_three_props_escherich_1885_slide_metchnikoff_1907_yogurt_jar_and_germ_free_glove_port"
                row["reuse_window_s"] = [5.5, 7.9]
                row["reuse_audit"] = {
                    "source_row": "P1:07_table_three_props_escherich_1885_slide_metchnikoff_1907_yogurt_jar_and_germ_free_glove_port",
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
            "film": "057_Escherich-Metchnikoff-Gordon-Gut-Microbiome",
            "part": p_idx,
            "title": p_title,
            "version": "v01",
            "timing_status": "pre_vo_script_clock (built from microbiome_script_master_v01.md; retimes onto Scribe STT once VO locks)",
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
        "film": "057_Escherich-Metchnikoff-Gordon-Gut-Microbiome",
        "version": "v01",
        "date": "2026-10-19",
        "owner": "gemini (J0615)",
        "status": "PRE_VO_BOARDS_V01_NO_MINT",
        "generation_authorized": False,
        "script": "00_Brand/Channel-Setup/ideas/057_Escherich-Metchnikoff-Gordon-Gut-Microbiome/microbiome_script_master_v01.md",
        "sources": "00_Brand/Channel-Setup/ideas/057_Escherich-Metchnikoff-Gordon-Gut-Microbiome/SOURCES_v01.md",
        "credit_snapshot": {
            "flow_balance": 23740,
            "flow_floor": 0,
            "flow_read_at": "2026-10-15T21:42:22Z",
            "vertex_promo_gbp": 71.02,
            "vertex_usable_gbp": 70.02,
        },
        "totals": totals,
        "per_part": per_part_summary,
        "mint_order": "006 > 007 > 008 > 009 > 010 > 011 > 012 > 013 > 014 > 015 > 016 > 017 > 018 > 019 > 020 > 021 > 022 > 023 > 024 > 025 > 026 > 027 > 028 > 029 > 030 > 031 > 032 > 033 > 034 > 035 > 036 > 037 > 038 > 039 > 040 > 041 > 042 > 043 > 044 > 045 > 046 > 047 > 048 > 049 > 050 > 051 > 052 > 053 > 054 > 055 > 056 > 057 > 058 > 059. Nothing in 057 is generation_authorized.",
    }
    (EDIT / "PICTURE_PLAN_v01.json").write_text(json.dumps(plan, indent=2) + "\n")

    sl = [
        "# 057 The Gut Microbiome: 38 Trillion Bacteria Inside You — Shot list & plate boards v01 (pre-VO)",
        "",
        "Gemini, 19 Oct 2026, J0615. Built from `microbiome_script_master_v01.md` (`91.6 PASS`) and `SOURCES_v01.md`.",
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
        "# 057 price review v01 (pre-VO plate boards)",
        "",
        "Gemini, 19 Oct 2026, J0615. Boards only. **No mint. No spend. No merge.**",
        "Prepared from `microbiome_script_master_v01.md` (`91.6 PASS`) and `SOURCES_v01.md` so 057's full plate board rows, non-emissive Fast prompts, £0 code graphics, and Teach-on-Screen overlays are ready to re-time the moment long VO locks. Parked for Chief.",
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
        f"- **Quality ({totals['Quality']} rows):** readable faces (Theodor Escherich, Stamen Grigorov, Élie Metchnikoff, James A. Reyniers, Bengt E. Gustafsson, Carl R. Woese, Jeffrey I. Gordon, Lora V. Hooper, Ruth E. Ley, Ernest McCulloch, James Till, John Gurdon, Shinya Yamanaka), 14 July 1885 Munich newborn *E. coli* discovery & 1907 Paris Bulgarian yogurt probiotics, 1946–1959 stainless-steel germ-free isolator experiments, 28 March 2003 – 21 December 2006 *Bacteroides thetaiotaomicron* 261-enzyme & microbiome energy proof, and the 2 Explorer beats.",
        f"- **Fast ({totals['Fast']} rows, non-emissive):** daylight prop and laboratory shots (apple/oats/yogurt bowl & brass microscope slide pan, 3-object callback bench, 1907 *The Prolongation of Life* book & stoneware yogurt jug, 1885 Munich agar culture tubes & clinic notebook, 1959 stainless-steel isolator porthole & Vitamin K tubes, brass feed balance & 5× caecum anatomical models, anaerobic glove-box airlock & short-chain fatty-acid models, oats/apples/beans & butyrate model on museum plinth). Zero candles, flames, sparks, or glowing elements on Fast.",
        f"- **£0 code graphics ({totals['code_graphic']} rows):**",
        "  1. `P1:04_sender_milo_2016_and_gordon_2006_30t_human_cells_vs_38t_gut_bacteria_2m_genes_chart` — human vs gut microbiome census comparing 30 trillion human cells (20,000 human genes; 17 digestive carb enzymes) against 38 trillion bacterial cells in the colon (0.2 kg mass; >2 million microbial genes; thousands of fibre-digesting CAZymes) (`SCALE: by cell count you are less than half human — for every ten human cells in your body, roughly thirteen microscopic bacteria ride along inside your gut, carrying a hundred times more genes than your own DNA`)",
        "  2. `P1:06_gustafsson_1959_germ_free_vs_colonized_mouse_30pct_calories_5x_caecum_vitamin_k_chart` — germ-free isolator mouse vs conventional mouse comparison (+30% calorie requirement, 5× enlarged caecum, and 0 endogenous Vitamin K synthesis vs normal weight, fibre fermentation, and microbial Vitamin K synthesis) (`SCALE: without gut bacteria, a mouse has to eat nearly a third more food just to stay the same weight — because the calories locked inside plant fibre pass straight through its body untouched`)",
        "  3. `P2:02_escherich_1885_newborn_colonization_10e10_per_gram_and_metchnikoff_1907_lactic_acid_ph_chart` — Escherich (14 July 1885) newborn gut colonization reaching >10⁹–10¹⁰ bacteria/g within days of birth & Metchnikoff (1907) *Lactobacillus bulgaricus* lactic-acid fermentation (pH ~4.0–4.5) (`SCALE: inside a single gram of contents from your lower gut — a pinch no bigger than a paperclip — live more individual bacteria than there are human beings on the entire planet Earth`)",
        "  4. `P3:02_reyniers_1946_gustafsson_1959_gnotobiotic_4_metric_caecum_calories_vitamin_k_immune_chart` — Reyniers (1946) and Gustafsson (1948, 1959) gnotobiotic isolator 4-metric chart (5× caecum weight, +30% caloric intake, lethal Vitamin K bleeding cured in 24–48 h by gut microbes, and underdeveloped immune tissue) (`SCALE: raising a mouse without gut bacteria is like trying to run a city without power plants, recycling crews, or a fire brigade — the mouse has to eat nearly a third more food just to stay warm, and a tiny scratch can bleed uncontrollably without bacterial Vitamin K`)",
        "  5. `P4:02_xu_gordon_28_mar_2003_science_17_human_vs_261_bacteroides_enzymes_and_butyrate_colonocyte_chart` — Xu et al. & Gordon (28 March 2003, *Science*) and Turnbaugh, Ley & Gordon (21 December 2006, *Nature*) comparing 17 human digestive glycoside hydrolases against 261 in *Bacteroides thetaiotaomicron* converting fibre into butyrate (60–70% of colonocyte energy) (`SCALE: one single species of friendly gut bacterium carries fifteen times more fibre-digesting tools than the entire human genome — turning tough plant cell walls that would pass straight through us into the very fuel that keeps the lining of our gut alive`)",
        "  6. `P5:01_timeline_1885_2016_and_dietary_fibre_to_butyrate_colon_barrier_chart` — completed 4-date timeline (1885 → 2016) + dietary fibre fermentation into butyrate & immune T-cell regulation diagram (`SCALE: every meal you eat is a banquet for two — your human enzymes take the simple sugars up front, while thirty-eight trillion ancient microbial partners in the back turn indigestible plants into vitamins, fuel, and lifelong immunity`)",
        f"- **£0 verified reuse ({totals['reuse']} row):** `P5:04_table_three_callback` uses the 2.40 s unused moving tail `[5.50s..7.90s]` of `P1:07_table_three_props_escherich_1885_slide_metchnikoff_1907_yogurt_jar_and_germ_free_glove_port`.",
        "",
        "## Mint order",
        "",
        "006 > 007 > 008 > 009 > 010 > 011 > 012 > 013 > 014 > 015 > 016 > 017 > 018 > 019 > 020 > 021 > 022 > 023 > 024 > 025 > 026 > 027 > 028 > 029 > 030 > 031 > 032 > 033 > 034 > 035 > 036 > 037 > 038 > 039 > 040 > 041 > 042 > 043 > 044 > 045 > 046 > 047 > 048 > 049 > 050 > 051 > 052 > 053 > 054 > 055 > 056 > 057 > 058 > 059. `generation_authorized` is `false` on every row.",
    ])
    (EDIT / "PRICE_REVIEW_v01.md").write_text("\n".join(pr_lines) + "\n")
    print(f"057 v01 boards written: {totals['rows']} rows, Flow expected={totals['flow_credits_expected']}")


if __name__ == "__main__":
    main()
