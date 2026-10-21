#!/usr/bin/env python3
"""HOS 077 (Digestion: The Pet Buzzard & The Washed Liver) pre-VO plate boards v01. J0723. No mint, no spend.

Built from 00_Brand/Channel-Setup/ideas/077_Reaumur-Spallanzani-Bernard-Pavlov-Digestion-Liver/digestion_script_master_v01.md
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
        "Part 01 — The Pet Buzzard's Iron Tube & the Washed Liver in Paris",
        [
            ("01_reaumur_pet_buzzard_perforated_iron_tube_beside_stomach_pancreas_villi_and_liver_glycogen_refinery", 0.0, 5.5, "A", False, "THE 9-METRE CHEMICAL REFINERY", "Quality",
             "Quality: Short frame 0 / answer image (0:03) + side by side, René-Antoine de Réaumur's pet buzzard regurgitates an uncrushed perforated iron tube whose meat inside has been completely dissolved by gastric juice, while inside a human abdomen the stomach, pancreas, small-intestinal villi, and 1.5-kilogram liver convert food into glucose and glycogen to hold blood sugar at 1 gram per litre.",
             STYLE + "Split historical-and-anatomical scene: on the left, a perched buzzard coughs up an uncrushed perforated iron tube from which dissolved meat juice drips; on the right, a cutaway digestive tract and crimson liver convert meal nutrients into branched glycogen chains." + QUAL_TAIL,
             {"kind": "WHEN", "label": "PARIS, 24 MARCH 1857", "timeline_step": "1/3 · 1752 & 1780 (René-Antoine de Réaumur feeds perforated metal tubes of meat to his pet buzzard and Lazzaro Spallanzani swallows linen pouches to prove gastric digestion is chemical)", "hold_s": 3.5}),
            ("02_reaumur_1752_buzzard_spallanzani_1780_claude_bernard_1857_washed_liver_and_pavlov_1897_split", 5.5, 6.0, "B", False, "BUZZARD TUBES, WASHED LIVER, PAVLOV'S REFLEXES", "Quality",
             "Quality: complex three-part composition (René-Antoine de Réaumur in Paris in 1752 feeding perforated metal tubes packed with meat to his pet buzzard alongside Lazzaro Spallanzani in Pavia in 1780; Claude Bernard at the Collège de France in Paris in 1848–24 March 1857 flushing a liver with cold water and discovering glycogen and the milieu intérieur alongside Walter Cannon in 1926; and Ivan Pavlov in St Petersburg in 1897–1904 measuring cephalic vagus-nerve gastric secretion).",
             STYLE + "Three-panel period composition: on the left, René-Antoine de Réaumur in 1752 Paris holding a perforated metal tube beside his buzzard and Lazzaro Spallanzani in 1780 Pavia; in the centre, Claude Bernard in 1857 Paris flushing a liver on a porcelain tray beside Walter Cannon; on the right, Ivan Pavlov in 1897 St Petersburg observing a dog's gastric secretion flask." + QUAL_TAIL,
             None),
            ("03_single_teaspoon_of_glucose_on_brass_scale_balanced_by_1_5kg_liver_glycogen_storage", 11.5, 6.0, "C", False, "ONE TEASPOON OF SUGAR IN ALL YOUR BLOOD", "Quality",
             "Quality: complex physiological reveal (a single level teaspoon of white glucose — 5 grams total in 5 litres of human blood = 100 mg/dL — sits steady on a brass balance scale while the 1.5-kg liver absorbs a flood of meal sugar into branched glycogen chains and releases it smoothly back into the bloodstream overnight).",
             STYLE + "On an oak laboratory table, a single silver teaspoon heaped with five grams of white sugar crystals sits balanced on a brass scale beside a five-litre glass carboy of blood while a cutaway liver model locks incoming sugar spheres into branched chains and releases them one by one." + QUAL_TAIL,
             {"kind": "WHEN", "label": "1752 · 1780 · 1848 · 1855 · 24 MARCH 1857 · 1897 · 1926", "timeline_step": "1/3 · 1752 & 1780 (Réaumur & Spallanzani) · 2/3 · 1848–1857 & 1926 (Bernard & Cannon) · 3/3 · 1897–1904 (Pavlov)", "hold_s": 3.5}),
            ("04_reaumur_1752_spallanzani_1780_bernard_1857_pavlov_1897_and_cannon_1926_digestion_glycogen_chart", 17.5, 8.0, "E", False, "9-M DIGESTIVE TRACT (~30 M2 VILLI) · GASTRIC HCL/PEPSIN (PH 1.5–2.0) · BERNARD PANCREATIC LIPOLYSIS & HEPATIC GLYCOGEN (~100 G BUFFERING 5 L BLOOD AT 1 G/L = 5 G)", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked Chemical Digestion, Pancreatic Lipolysis, Hepatic Glycogen & Cephalic Reflex chart from Réaumur (1752 Mém. Acad. Roy. Sci. 266–307 & 461–495), Spallanzani (1780 Dissertazioni di fisica animale, e vegetabile), Claude Bernard (1848, 1855 & 24 March 1857 C. R. Acad. Sci. 44: 578–586), Pavlov (1897 / 1902 The Work of the Digestive Glands), and Walter Cannon (1926 / 1929 Physiol. Rev. 9: 399–431) maps the 9-metre digestive tract (~30 m2 villous/microvillous absorptive surface), pancreatic lipase/bile fat emulsification, liver glycogen storage (~100 g hepatic reserve buffering blood glucose at ~1 g/L = 5 mmol/L), and Pavlov's vagal cephalic phase.",
             {"kind": "DATA", "label": "GASTRIC PEPSIN/HCL (PH 1.5–2.0), BERNARD PANCREATIC FAT & LIVER GLYCOGEN BUFFER (~100 G HOLDING 5 L BLOOD AT 1.0 G/L = 5 G GLUCOSE) & PAVLOV VAGAL CURVE", "detail": "Inked digestive tract & hepatic glycogen homeostasis chart on period paper showing gastric pepsin/HCl protein cleavage (pH 1.5–2.0), Bernard's pancreatic fat emulsification and liver glycogen buffer (~100 g glycogen maintaining 5 L blood at ~1.0 g/L glucose = 5 grams total), and Pavlov's vagus-nerve cephalic secretion curve", "scale": "all five litres of blood in your body hold just five grams of dissolved glucose at any moment — a single level teaspoon of sugar — because your liver acts like a rechargeable battery that locks away a whole cup of sugar after dinner and drips it out grain by grain while you sleep", "who_card": "René-Antoine Ferchault de Réaumur (1683–1757) — French physicist and naturalist · Lazzaro Spallanzani (1729–1799) — Italian priest and biologist · Claude Bernard (1813–1878) — French physiologist · Ivan Petrovich Pavlov (1849–1936) — Russian physiologist · Walter Bradford Cannon (1871–1945) — American physiologist", "when_stamp": "1752 · 1780 · 1848 · 1855 · 24 March 1857 · 1897 · 1926", "hold_s": 3.8}),
            ("05_reaumur_1752_engraving_perforated_iron_tubes_and_1857_comptes_rendus_offprint_pan", 25.5, 5.5, "A", False, "THE INTERNAL OCEAN THERMOSTAT", "Fast",
             "Fast: daylight macro pan across Réaumur's 1752 copperplate engraving of perforated metal digestion tubes, two grated iron tubes on a dish, and an 1857 Comptes Rendus offprint on an oak bench between code graphics so two full-frame graphics never run back to back. Nothing emissive, no face.",
             STYLE + "In crisp daylight on an oak physiology bench, the camera pans smoothly across a 1752 copperplate engraving of digestion tubes, two perforated iron cylinders, and an open 1857 French academy journal." + FAST_TAIL,
             None),
            ("06_claude_bernard_1855_1857_comptes_rendus_washed_liver_glycogen_chart", 31.0, 8.0, "E", False, "PARIS, 1855–1857", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period parchment, an inked Claude Bernard Washed-Liver Glycogen & Milieu Intérieur diagram (from Claude Bernard, 1855 C. R. Acad. Sci. 41: 461–469 & 24 March 1857 C. R. Acad. Sci. 44: 578–586) shows portal vein blood entering a dog's liver with zero sugar on a meat-only diet while hepatic vein blood exits rich in glucose, alongside a perfused, water-washed dead liver regenerating glucose overnight from insoluble hepatic glycogen.",
             {"kind": "DATA", "label": "1855 & 24 MAR 1857 CLAUDE BERNARD (C. R. ACAD. SCI.): PORTAL VEIN (0 SUGAR) VS HEPATIC VEIN (+GLUCOSE) & WASHED-LIVER GLYCOGEN REGENERATION", "detail": "Inked Claude Bernard (1855 & 24 March 1857 C. R. Acad. Sci.) portal vs hepatic vein glucose table & water-washed liver glycogen-to-glucose conversion chart on period paper", "scale": "flushing a dead liver with cold water until its sugar hit zero and finding it full of sugar again the next morning proved the liver isn't just a filter — it is a chemical pantry that bakes and slices its own animal starch", "hold_s": 3.8}),
            ("07_table_three_props_1752_reaumur_iron_tube_1857_bernard_glycogen_jar_and_1897_pavlov_gastric_flask", 39.0, 5.5, "C", False, "1752 TO 1926", "Fast",
             "Fast: daylight prop table (callback source for Part 05: Réaumur's 1752 perforated iron buzzard tube with sponge, Claude Bernard's 1857 glass specimen jar of white glycogen powder, and Ivan Pavlov's 1897 graduated glass gastric-juice collection flask). Nothing emissive.",
             STYLE + "On an oak workbench in soft window light sit three objects side by side: a perforated iron digestion cylinder with a small sea sponge, a stoppered glass jar of white glycogen powder, and a graduated glass gastric collection flask." + FAST_TAIL,
             None),
            ("08_explorer_locking_meal_sugar_cubes_into_branched_glycogen_chains_in_liver_vault_to_hold_5g_blood_gauge_steady", 62.0, 5.5, "A", True, None, "Quality",
             "Quality: Explorer beat 1 (locked character reference, after 1:00).",
             STYLE + "Standing beside a brass blood-sugar dial gauge connected to a cutaway liver vault, the Explorer catches a cascade of white sugar cubes, clicks them into branched glycogen chains inside the vault, and unclips one cube at a time so the brass dial needle stays rock-steady." + EXP_TAIL,
             None),
            ("09_claude_bernard_mar_1857_paris_precipitating_white_glycogen_from_liver_extract", 67.5, 5.5, "B", False, "THE DISCOVERY OF GLYCOGEN", "Quality",
             "Quality: readable face (at the Collège de France in Paris in March 1857, Claude Bernard precipitates white glycogen powder from a boiled liver extract using alcohol beside his water-flushed liver perfusion tray).",
             STYLE + "In his 1857 Collège de France laboratory in Paris, Claude Bernard pours alcohol into a glass beaker of clear liver extract, watching snow-white flakes of glycogen precipitate beside a water-washed perfusion tray." + QUAL_TAIL,
             {"kind": "WHEN", "label": "PARIS, 1855–1857", "timeline_step": "2/3 · 1855 – 24 Mar 1857 (Claude Bernard discovers the glycogenic function of the liver and isolates glycogen)", "hold_s": 3.5}),
        ],
    ),
    (
        2,
        "Part 02 — 1752 & 1780: Réaumur's Pet Buzzard, Spallanzani's Swallowed Linen Bags & the Chemical Stomach",
        [
            ("01_reaumur_1752_paris_pet_buzzard_iron_tubes_and_spallanzani_1780_pavia_linen_bags", 73.0, 6.5, "A", False, "METAL TUBES PROVED CHEMICAL DIGESTION", "Quality",
             "Quality: readable faces (French physicist René-Antoine Ferchault de Réaumur in Paris in 1752 examining uncrushed perforated iron tubes regurgitated by his pet buzzard with the meat inside dissolved, dissolving to Italian priest-biologist Lazzaro Spallanzani in Pavia in 1780 holding perforated wooden tubes and linen bags alongside glass dishes of gastric juice).",
             STYLE + "Split period scene: on the left in 1752 Paris, René-Antoine de Réaumur holds up an uncrushed grated iron tube beside his pet buzzard and squeezes gastric liquid from a tiny sponge; on the right in 1780 Pavia, Lazzaro Spallanzani compares small linen digestion pouches and glass vials of gastric juice." + QUAL_TAIL,
             {"kind": "FACT", "label": "Metal tubes proved chemical digestion", "who_card": "Giovanni Alfonso Borelli (1608–1679) — Italian physicist and physiologist · William Prout (1785–1850) — British physician and chemist · Theodor Schwann (1810–1882) — German physiologist", "when_stamp": "1680 · 1752 · 1780 · 1823 · 1836", "timeline_step": "1/3 · 1752 & 1780 (Réaumur's pet-buzzard metal tubes & Spallanzani's gastric-juice experiments prove digestion is chemical)", "hold_s": 3.8}),
            ("02_reaumur_1752_metal_tube_sponge_and_spallanzani_1780_chemical_gastric_juice_chart", 79.5, 8.0, "E", False, "1752 RÉAUMUR (MÉM. ACAD. ROY. SCI.: PERFORATED IRON TUBES & SPONGES) & 1780 SPALLANZANI (IN-VITRO GASTRIC SOLVENT PROOF)", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked René-Antoine de Réaumur (1752 Mém. Acad. Roy. Sci. 266–307 & 461–495) perforated metal-tube & sponge gastric-juice experiment and Lazzaro Spallanzani (1780 Dissertazioni di fisica animale, e vegetabile) in-vitro vs in-vivo chemical digestion chart.",
             {"kind": "DATA", "label": "1752 RÉAUMUR PERFORATED IRON BUZZARD TUBES & 1780 SPALLANZANI IN-VITRO GASTRIC SOLVENT CHART (HCL 1823 & PEPSIN 1836)", "detail": "Inked René-Antoine de Réaumur (1752 Mém. Acad. Roy. Sci. 266–307 & 461–495) perforated metal-tube & sponge gastric-juice experiment and Lazzaro Spallanzani (1780 Dissertazioni di fisica animale, e vegetabile) in-vitro vs in-vivo chemical digestion chart on period paper", "scale": "by locking meat inside an iron cage that no muscle could squeeze and watching it melt away anyway, Réaumur proved that your stomach isn't a rock crusher — it is an acid bath that unzips food molecule by molecule", "hold_s": 3.8}),
            ("03_paris_1752_grated_iron_tubes_sponges_and_spallanzani_wooden_tubes_linen_pouches_closeup", 87.5, 6.5, "B", False, "1752 & 1780 — CHEMICAL DIGESTION PROVED", "Fast",
             "Fast: daylight macro shot of Réaumur's grated iron and tin tubes with small sponges beside Spallanzani's perforated wooden tubes, tiny stitched linen bags, and glass vials of clear gastric juice on a bench. Nothing emissive, no face.",
             STYLE + "In crisp daylight on an eighteenth-century natural-history bench, grated iron cylinders and sponges sit beside perforated wooden tubes, small tied linen pouches, and glass dishes of gastric liquid." + FAST_TAIL,
             None),
            ("04_cutaway_stomach_model_showing_gastric_pits_hcl_and_pepsin_cleaving_protein_chains_pan", 94.0, 5.5, "C", False, "HYDROCHLORIC ACID & PEPSIN", "Fast",
             "Fast: daylight close-up pan across a sculpted anatomical model of the human stomach rugae and gastric glands alongside a molecular model of pepsin cleaving a folded protein chain on an oak table. Nothing emissive, no face.",
             STYLE + "In bright window light on an oak table, a sculpted cutaway model of the human stomach wall and gastric glands sits beside a molecular model of pepsin snipping a coiled protein chain." + FAST_TAIL,
             None),
        ],
    ),
    (
        3,
        "Part 03 — 1848 – 24 March 1857: Claude Bernard's Pancreatic Fat Proof, the Overnight Washed Liver (Glycogen) & the Milieu Intérieur — Midpoint Twist",
        [
            ("01_claude_bernard_1848_1857_paris_washed_liver_glycogen_and_walter_cannon_1926_homeostasis", 99.5, 6.5, "A", False, "DEAD WASHED LIVER MADE SUGAR", "Quality",
             "Quality: readable faces (French physiologist Claude Bernard at the Collège de France in Paris in 1848–24 March 1857 discovering pancreatic fat emulsification and finding that a water-washed dead liver left overnight regenerates fresh glucose from hepatic glycogen, dissolving to Harvard physiologist Walter Bradford Cannon in 1926 formulating homeostasis).",
             STYLE + "Split period scene: on the left in 1855–1857 Paris, Claude Bernard tests a water-flushed liver on a porcelain tray with copper-reduction tubes turning brick-red with fresh glucose; on the right in 1926 Boston, Walter Cannon points to a steady blood-glucose homeostasis chart." + QUAL_TAIL,
             {"kind": "FACT", "label": "Dead washed liver made sugar", "when_stamp": "1848 · 24 September 1855 · 24 March 1857 · 1865 · 1926 · 1929", "timeline_step": "2/3 · 1848 – 24 Mar 1857 & 1926 (Claude Bernard discovers pancreatic lipolysis, hepatic glycogen, and the milieu intérieur; Walter Cannon coins homeostasis)", "hold_s": 3.8}),
            ("02_bernard_1848_1857_pancreatic_fat_and_washed_liver_glycogen_cannon_1926_homeostasis_chart", 106.0, 8.0, "E", False, "1848–1857 CLAUDE BERNARD (C. R. ACAD. SCI.: PANCREATIC LIPOLYSIS & WASHED-LIVER GLYCOGEN) & 1926 WALTER CANNON HOMEOSTASIS (~1.0 G/L)", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked Claude Bernard (1848, 1855 & 24 March 1857 C. R. Acad. Sci. 41: 461–469 & 44: 578–586) pancreatic fat digestion & washed-liver glycogen regeneration chart alongside Walter Cannon's (1926 / 1929 Physiol. Rev. 9: 399–431) blood-glucose homeostasis band (~1.0 g/L).",
             {"kind": "DATA", "label": "1848–1857 BERNARD PANCREATIC FAT & WASHED-LIVER GLYCOGEN CHART + 1926 CANNON HOMEOSTASIS BAND (~1.0 G/L BLOOD GLUCOSE)", "detail": "Inked Claude Bernard (1848, 1855 & 24 March 1857 C. R. Acad. Sci. 41: 461–469 & 44: 578–586) pancreatic fat digestion & washed-liver glycogen regeneration chart alongside Walter Cannon's (1926 / 1929 Physiol. Rev. 9: 399–431) blood-glucose homeostasis band (~1.0 g/L) on period paper", "scale": "Claude Bernard realized that you don't really live in the dry air of your bedroom — your cells still live inside a warm, salty internal ocean, and your liver is the thermostat that keeps that ocean's fuel supply from ever running dry", "hold_s": 3.8}),
            ("03_paris_1857_liver_perfusion_funnel_barreswil_copper_tubes_and_glycogen_powder_closeup", 114.0, 6.5, "B", False, "1855–1857 — CLAUDE BERNARD'S GLYCOGEN & MILIEU INTÉRIEUR", "Fast",
             "Fast: daylight macro shot of Claude Bernard's water-perfusion glass tubing on a porcelain tray beside blue and brick-red Barreswil/Fehling copper sugar-test tubes and a watch glass of white glycogen powder on a bench. Nothing emissive, no face.",
             STYLE + "In crisp daylight on an 1857 Paris laboratory bench, a glass water-perfusion apparatus sits beside a rack of blue and brick-red copper-reduction test tubes and a watch glass of white glycogen powder." + FAST_TAIL,
             None),
            ("04_cutaway_liver_lobule_pancreatic_duct_and_intestinal_villi_model_on_oak_table_pan", 120.5, 5.5, "C", False, "PANCREATIC ENZYMES, BILE & LIVER GLYCOGEN", "Fast",
             "Fast: daylight close-up pan across a sculpted anatomical model of the duodenum receiving the bile and pancreatic ducts alongside hexagonal liver lobules and finger-like intestinal villi on an oak table. Nothing emissive, no face.",
             STYLE + "In bright window light on an oak table, a sculpted anatomical model shows the liver, gallbladder, and pancreas emptying into the small intestine lined with finger-like villi." + FAST_TAIL,
             None),
        ],
    ),
    (
        4,
        "Part 04 — 1897–1904: Ivan Pavlov's Digestive Pouches, Sham Feeding & How the Brain Primes the Gut",
        [
            ("01_ivan_pavlov_1897_1904_st_petersburg_digestive_glands_and_cephalic_vagus_reflex", 126.0, 6.5, "A", False, "PAVLOV WON FOR DIGESTION", "Quality",
             "Quality: readable face (Russian physiologist Ivan Petrovich Pavlov at the Institute of Experimental Medicine in St Petersburg in 1897–1904 measuring pure gastric juice secreted in lockstep via the vagus nerve during cephalic sham feeding, earning the 1904 Nobel Prize in Physiology or Medicine).",
             STYLE + "In his 1897 St Petersburg physiology laboratory, Ivan Pavlov observes clear gastric juice dripping into a graduated glass flask as a healthy dog eagerly eats from a porcelain dinner bowl." + QUAL_TAIL,
             {"kind": "FACT", "label": "Pavlov won for digestion", "when_stamp": "1897 · 1902 · 12 December 1904", "timeline_step": "3/3 · 1897–1904 (Ivan Pavlov proves cephalic vagus-nerve digestive reflexes in St Petersburg, winning the 1904 Nobel Prize)", "hold_s": 3.8}),
            ("02_pavlov_1897_1902_work_of_digestive_glands_cephalic_vagus_and_secretin_curve_chart", 132.5, 8.0, "E", False, "1897/1902 PAVLOV (WORK OF THE DIGESTIVE GLANDS): CEPHALIC VAGUS-NERVE SECRETION CURVE & 1902 BAYLISS-STARLING DUODENAL SECRETIN", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked Ivan Pavlov (1897 / 1902 The Work of the Digestive Glands) Pavlov-pouch & sham-feeding vagus-nerve gastric secretion curve (cephalic phase vs gastric phase vs Bayliss-Starling 1902 intestinal secretin phase).",
             {"kind": "DATA", "label": "1897 PAVLOV CEPHALIC VAGUS-NERVE GASTRIC SECRETION CURVE (5-MIN LATENCY) & ENZYME ADAPTATION TO BREAD, MEAT & MILK", "detail": "Inked Ivan Pavlov (1897 / 1902 The Work of the Digestive Glands) Pavlov-pouch & sham-feeding vagus-nerve gastric secretion curve (cephalic phase vs gastric phase vs Bayliss-Starling 1902 intestinal secretin phase) on period paper", "scale": "Ivan Pavlov proved that digestion starts in your head before your fork even reaches your mouth — the smell of baking bread sends a vagus-nerve telegram down from your brain so your stomach acid is already warm and waiting when the first bite arrives", "hold_s": 3.8}),
            ("03_st_petersburg_1897_graduated_gastric_juice_flasks_and_work_of_digestive_glands_book_closeup", 140.5, 6.5, "B", False, "1897 — PAVLOV PROVES CEPHALIC DIGESTIVE REFLEXES", "Fast",
             "Fast: daylight macro shot of graduated glass gastric-juice flasks labeled for bread, meat, and milk meals beside Pavlov's 1897/1902 Lectures on the Work of the Principal Digestive Glands volume and 1904 Nobel diploma scroll on a bench. Nothing emissive, no face.",
             STYLE + "In crisp daylight on a 1904 St Petersburg bench, three graduated glass flasks of clear digestive juice sit beside an open physiology monograph and a gold-embossed diploma scroll." + FAST_TAIL,
             None),
            ("04_explorer_pulling_vagus_nerve_telegraph_lever_to_start_stomach_and_pancreas_before_meal_arrives", 147.0, 5.5, "B", True, None, "Quality",
             "Quality: Explorer beat 2 (locked character reference).",
             STYLE + "Standing beside a brass telegraph key wired along a sculpted vagus-nerve cable from a brain model to a glass stomach and pancreas model, the Explorer taps the telegraph key as the aroma of a loaf of bread wafts by, starting a warm shower of digestive droplets before the bread even enters the tube." + EXP_TAIL,
             None),
        ],
    ),
    (
        5,
        "Part 05 — The Internal Ocean Inside You — & What Happens When You Cut the Bridge Between the Left and Right Brain",
        [
            ("01_timeline_1752_1926_and_digestive_refinery_homeostasis_chart", 152.5, 8.5, "E", False, "1752–1926 TIMELINE · RÉAUMUR & SPALLANZANI, CLAUDE BERNARD GLYCOGEN & MILIEU INTÉRIEUR, PAVLOV VAGAL REFLEXES & CANNON HOMEOSTASIS", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, the 3-era timeline completes: 1752 & 1780 (René-Antoine de Réaumur feeds perforated metal tubes of meat to his pet buzzard and Lazzaro Spallanzani swallows linen pouches to prove gastric digestion is chemical) · 1848 – 24 Mar 1857 & 1926 (Claude Bernard discovers pancreatic fat digestion, isolates hepatic glycogen from a washed liver, and formulates the milieu intérieur, named homeostasis by Walter Cannon in 1926) · 1897–1904 (Ivan Pavlov uses gastric pouches and sham feeding in St Petersburg to prove cephalic vagus-nerve digestive reflexes, winning the 1904 Nobel Prize).",
             {"kind": "DATA", "label": "1752–1926 DIGESTION, LIVER GLYCOGEN & HOMEOSTASIS TIMELINE · RÉAUMUR, SPALLANZANI, BERNARD, PAVLOV & CANNON", "detail": "Animated timeline (1752 → 1926) alongside an inked summary of chemical gastric digestion, pancreatic lipolysis, hepatic glycogen buffering, and cephalic vagal control", "scale": "from an iron tube coughed up by a pet buzzard to a washed liver on a Paris bench and a dog's dinner bowl in St Petersburg, scientists unlocked the chemical refinery that fuels every cell in your body", "when_stamp": "1752–1926", "timeline_step": "3/3 · 1752–1926 timeline complete", "hold_s": 3.8}),
            ("02_sculpted_digestive_tract_and_liver_model_beside_split_hemisphere_brain_model_on_plinth_pan", 161.0, 5.5, "A", False, "HOMEOSTASIS — 1 TEASPOON OF SUGAR IN 5 LITRES OF BLOOD", "Fast",
             "Fast: daylight close-up of a sculpted digestive tract and liver model beside a two-hemisphere human brain model showing the corpus callosum bridge on a wooden museum plinth. Nothing emissive, no face.",
             STYLE + "In crisp daylight on a wooden museum plinth, a sculpted anatomical model of the stomach, pancreas, and liver sits beside a two-hemisphere human brain model connected by the white corpus callosum bridge." + FAST_TAIL,
             None),
            ("03_broca_1861_left_frontal_lobe_penfield_1937_homunculus_and_sperry_gazzaniga_1962_1967_split_brain_handoff", 166.5, 6.5, "C", False, "LEFT BRAIN, RIGHT BRAIN & SPLIT BRAIN", "Quality",
             "Quality: readable faces (Paul Broca in Paris on 18 April 1861 mapping speech to the left frontal lobe, Wilder Penfield in Montreal in December 1937 mapping the motor and sensory homunculus, and Roger Sperry with Michael Gazzaniga at Caltech in 1962–1967 testing split-brain patients across a divided screen — handoff to 078 Left Brain, Right Brain & Split-Brain Patients).",
             STYLE + "Split period scene: on the left, Paul Broca in 1861 Paris and Wilder Penfield in 1937 Montreal map the left speech centre and cortical homunculus; on the right in 1960s California, Roger Sperry and Michael Gazzaniga test a split-brain patient reaching behind a divided tachistoscope screen." + QUAL_TAIL,
             {"kind": "WHEN", "label": "18 APRIL 1861 · 1874 · DECEMBER 1937 · 1962 · 1967", "hold_s": 3.5}),
            ("04_table_three_callback", 173.0, 2.4, "C", False, None, "reuse",
             "Reuse: verified unused moving window [5.50s..7.90s] of P1:07_table_three_props_1752_reaumur_iron_tube_1857_bernard_glycogen_jar_and_1897_pavlov_gastric_flask (callback, £0).",
             "Reuse P1:07_table_three_props_1752_reaumur_iron_tube_1857_bernard_glycogen_jar_and_1897_pavlov_gastric_flask [5.50s..7.90s] (2.40s distinct non-overlapping tail window from 8.00s source clip).",
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
                row["reuse_of"] = "P1:07_table_three_props_1752_reaumur_iron_tube_1857_bernard_glycogen_jar_and_1897_pavlov_gastric_flask"
                row["reuse_window_s"] = [5.5, 7.9]
                row["reuse_audit"] = {
                    "source_row": "P1:07_table_three_props_1752_reaumur_iron_tube_1857_bernard_glycogen_jar_and_1897_pavlov_gastric_flask",
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
            "film": "077_Reaumur-Spallanzani-Bernard-Pavlov-Digestion-Liver",
            "part": p_idx,
            "title": p_title,
            "version": "v01",
            "timing_status": "pre_vo_script_clock (built from digestion_script_master_v01.md; retimes onto Scribe STT once VO locks)",
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
        "film": "077_Reaumur-Spallanzani-Bernard-Pavlov-Digestion-Liver",
        "version": "v01",
        "date": "2026-10-20",
        "owner": "gemini (J0723)",
        "status": "PRE_VO_BOARDS_V01_NO_MINT",
        "generation_authorized": False,
        "script": "00_Brand/Channel-Setup/ideas/077_Reaumur-Spallanzani-Bernard-Pavlov-Digestion-Liver/digestion_script_master_v01.md",
        "sources": "00_Brand/Channel-Setup/ideas/077_Reaumur-Spallanzani-Bernard-Pavlov-Digestion-Liver/SOURCES_v01.md",
        "credit_snapshot": {
            "flow_balance": 23740,
            "flow_floor": 0,
            "flow_read_at": "2026-10-15T21:42:22Z",
            "vertex_promo_gbp": 71.02,
            "vertex_usable_gbp": 70.02,
        },
        "totals": totals,
        "per_part": per_part_summary,
        "mint_order": "006 > 007 > 008 > 009 > 010 > 011 > 012 > 013 > 014 > 015 > 016 > 017 > 018 > 019 > 020 > 021 > 022 > 023 > 024 > 025 > 026 > 027 > 028 > 029 > 030 > 031 > 032 > 033 > 034 > 035 > 036 > 037 > 038 > 039 > 040 > 041 > 042 > 043 > 044 > 045 > 046 > 047 > 048 > 049 > 050 > 051 > 052 > 053 > 054 > 055 > 056 > 057 > 058 > 059 > 060 > 061 > 062 > 063 > 064 > 065 > 066 > 067 > 068 > 069 > 070 > 071 > 072 > 073 > 074 > 075 > 076 > 077 > 078 > 079 > 080. Nothing in 077 is generation_authorized.",
    }
    (EDIT / "PICTURE_PLAN_v01.json").write_text(json.dumps(plan, indent=2) + "\n")

    sl = [
        "# 077 Digestion: The Pet Buzzard & The Washed Liver — Shot list & plate boards v01 (pre-VO)",
        "",
        "Gemini, 20 Oct 2026, J0723. Built from `digestion_script_master_v01.md` (`91.4/100 PASS`) and `SOURCES_v01.md`.",
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
        "# 077 price review v01 (pre-VO plate boards)",
        "",
        "Gemini, 20 Oct 2026, J0723. Boards only. **No mint. No spend. No merge.**",
        "Prepared from `digestion_script_master_v01.md` (`91.4/100 PASS`) and `SOURCES_v01.md` so 077's full plate board rows, non-emissive Fast prompts, £0 code graphics, and Teach-on-Screen overlays are ready to re-time the moment long VO locks. Parked for Chief.",
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
        f"- **Quality ({totals['Quality']} rows):** readable faces (René-Antoine Ferchault de Réaumur, Lazzaro Spallanzani, Giovanni Alfonso Borelli, William Prout, Theodor Schwann, Claude Bernard, Walter Bradford Cannon, Ivan Petrovich Pavlov, Paul Broca, Wilder Penfield, Roger Sperry, Michael Gazzaniga), 1752 Paris pet-buzzard perforated iron tubes & 1780 Pavia gastric-juice experiments, 1848–24 March 1857 Paris washed-liver `glycogen` discovery & `milieu intérieur`, 1897–1904 St Petersburg cephalic `vagus-nerve` digestive reflexes, and the 2 Explorer beats.",
        f"- **Fast ({totals['Fast']} rows, non-emissive):** daylight prop and laboratory shots (1752 Réaumur engraving, perforated iron tubes & 1857 *Comptes Rendus* offprint pan, 3-object callback bench, grated iron cylinders with sponges & Spallanzani's wooden tubes and linen pouches, sculpted cutaway stomach & pepsin cleavage model, 1857 Paris liver-perfusion tray with Barreswil copper tubes & white glycogen powder, sculpted liver/pancreas/duodenum villi model, 1897 St Petersburg graduated gastric-juice flasks & 1904 Nobel scroll, sculpted digestive-liver model beside two-hemisphere brain model on museum plinth). Zero candles, flames, sparks, or glowing elements on Fast.",
        f"- **£0 code graphics ({totals['code_graphic']} rows):**",
        "  1. `P1:04_reaumur_1752_spallanzani_1780_bernard_1857_pavlov_1897_and_cannon_1926_digestion_glycogen_chart` — `9 m` digestive tract (`~30 m²` villous surface), gastric HCl/pepsin (`pH 1.5–2.0`), Bernard's pancreatic lipolysis and `~100 g` hepatic `glycogen` buffer (`5 L` blood held at `~1.0 g/L` = `5 g` glucose), and Pavlov's vagal curve (`SCALE: all five litres of blood in your body hold just five grams of dissolved glucose at any moment — a single level teaspoon of sugar — because your liver acts like a rechargeable battery that locks away a whole cup of sugar after dinner and drips it out grain by grain while you sleep`)",
        "  2. `P1:06_claude_bernard_1855_1857_comptes_rendus_washed_liver_glycogen_chart` — Claude Bernard (1855 & 24 March 1857 *C. R. Acad. Sci.*) portal vs hepatic vein glucose & water-washed liver `glycogen` regeneration chart (`SCALE: flushing a dead liver with cold water until its sugar hit zero and finding it full of sugar again the next morning proved the liver isn't just a filter — it is a chemical pantry that bakes and slices its own animal starch`)",
        "  3. `P2:02_reaumur_1752_metal_tube_sponge_and_spallanzani_1780_chemical_gastric_juice_chart` — René-Antoine de Réaumur (1752) perforated metal buzzard tubes & Lazzaro Spallanzani (1780) chemical gastric-juice chart (`SCALE: by locking meat inside an iron cage that no muscle could squeeze and watching it melt away anyway, Réaumur proved that your stomach isn't a rock crusher — it is an acid bath that unzips food molecule by molecule`)",
        "  4. `P3:02_bernard_1848_1857_pancreatic_fat_and_washed_liver_glycogen_cannon_1926_homeostasis_chart` — Claude Bernard (1848–1857) pancreatic fat digestion & washed-liver `glycogen` chart + Walter Cannon (1926/1929) blood-glucose `homeostasis` band (`SCALE: Claude Bernard realized that you don't really live in the dry air of your bedroom — your cells still live inside a warm, salty internal ocean, and your liver is the thermostat that keeps that ocean's fuel supply from ever running dry`)",
        "  5. `P4:02_pavlov_1897_1902_work_of_digestive_glands_cephalic_vagus_and_secretin_curve_chart` — Ivan Pavlov (1897/1902 *The Work of the Digestive Glands*) Pavlov-pouch & sham-feeding vagus-nerve gastric secretion curve (`SCALE: Ivan Pavlov proved that digestion starts in your head before your fork even reaches your mouth — the smell of baking bread sends a vagus-nerve telegram down from your brain so your stomach acid is already warm and waiting when the first bite arrives`)",
        "  6. `P5:01_timeline_1752_1926_and_digestive_refinery_homeostasis_chart` — completed timeline (1752 → 1926) + chemical digestion, hepatic glycogen & homeostasis (`SCALE: from an iron tube coughed up by a pet buzzard to a washed liver on a Paris bench and a dog's dinner bowl in St Petersburg, scientists unlocked the chemical refinery that fuels every cell in your body`)",
        f"- **£0 verified reuse ({totals['reuse']} row):** `P5:04_table_three_callback` uses the 2.40 s unused moving tail `[5.50s..7.90s]` of `P1:07_table_three_props_1752_reaumur_iron_tube_1857_bernard_glycogen_jar_and_1897_pavlov_gastric_flask`.",
        "",
        "## Mint order",
        "",
        "006 > 007 > 008 > 009 > 010 > 011 > 012 > 013 > 014 > 015 > 016 > 017 > 018 > 019 > 020 > 021 > 022 > 023 > 024 > 025 > 026 > 027 > 028 > 029 > 030 > 031 > 032 > 033 > 034 > 035 > 036 > 037 > 038 > 039 > 040 > 041 > 042 > 043 > 044 > 045 > 046 > 047 > 048 > 049 > 050 > 051 > 052 > 053 > 054 > 055 > 056 > 057 > 058 > 059 > 060 > 061 > 062 > 063 > 064 > 065 > 066 > 067 > 068 > 069 > 070 > 071 > 072 > 073 > 074 > 075 > 076 > 077 > 078 > 079 > 080. `generation_authorized` is `false` on every row.",
    ])
    (EDIT / "PRICE_REVIEW_v01.md").write_text("\n".join(pr_lines) + "\n")
    print(f"077 v01 boards written: {totals['rows']} rows, Flow expected={totals['flow_credits_expected']}")


if __name__ == "__main__":
    main()
