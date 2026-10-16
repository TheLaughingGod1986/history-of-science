#!/usr/bin/env python3
"""HOS 052 (Allergies & Anaphylaxis: The 1901 Yacht Test That Went Backwards) pre-VO plate boards v01. J0585. No mint, no spend.

Built from 00_Brand/Channel-Setup/ideas/052_Richet-Dale-Bovet-Ishizaka-Allergies-Anaphylaxis-IgE/allergies_script_master_v01.md (91.8 PASS)
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
        "Part 01 — Why a Harmless Peanut or Pollen Grain Detonates an Ancient Worm-Killing Bomb",
        [
            ("01_richet_portier_1901_yacht_neptune_and_ige_mast_cell_histamine_degranulation", 0.0, 5.5, "A", False, "PROTECTION TURNED BACKWARDS", "Quality",
             "Quality: Short frame 0 / answer image (0:03) + aboard Prince Albert of Monaco's yacht Princesse Alice II in July 1901 and in Paris on 15 February 1902, Charles Richet and Paul Portier expect a tiny 0.1-millilitre booster dose of sea-anemone toxin to protect a healthy dog named Neptune, only for Y-shaped IgE antibodies sitting on a mast cell to detonate a storm of histamine granules at a harmless pollen grain.",
             STYLE + "Split period-and-microscopic scene: on the left in 1901–1902, French scientists Charles Richet and Paul Portier hold a small glass syringe beside a healthy dog and a jar of sea-anemone tentacles; on the right, Y-shaped antibodies on a spherical mast cell release a burst of purple histamine granules when touched by a golden pollen grain." + QUAL_TAIL,
             {"kind": "WHEN", "label": "JULY 1901 · 15 FEBRUARY 1902", "timeline_step": "1/5 · Jul 1901 & 15 Feb 1902 (Charles Richet and Paul Portier discover anaphylaxis in dogs primed with sea-anemone venom)", "hold_s": 3.5}),
            ("02_yacht_1901_man_of_war_dale_bovet_histamine_and_ishizaka_1966_ige_worm_split", 5.5, 6.0, "B", False, "ANAPHYLAXIS, HISTAMINE, IgE & WORMS", "Quality",
             "Quality: complex three-part composition (Charles Richet and Paul Portier aboard Prince Albert I's yacht Princesse Alice II hauling up purple Portuguese man-of-war jellyfish in 1901; Henry Dale's 1910 histamine vial and Daniel Bovet's 1937 antihistamine key at the Pasteur Institute; and Kimishige and Teruko Ishizaka in Denver in July 1966 isolating the 1-in-10-million IgE antibody that expels parasitic hookworms).",
             STYLE + "Three-panel period composition: on the left, scientists on a 1901 steam yacht deck inspecting a purple Portuguese man-of-war in a glass jar; in the centre, a 1937 Paris pharmacy bench with glass vials and a receptor lock-and-key model; on the right, a 1966 immunology bench with Y-shaped antibody models sweeping a hookworm away." + QUAL_TAIL,
             None),
            ("03_richet_portier_15_feb_1902_paris_day22_tiny_second_dose_shock_paradox", 11.5, 6.0, "C", False, "DAY 22 SHOCK", "Quality",
             "Quality: readable faces (in Paris on 15 February 1902, Charles Richet and Paul Portier prepare a tiny 0.1 cc syringe of actinia extract on Day 22 after a harmless priming dose, expecting complete immunity, when the second contact instead triggers immediate systemic shock).",
             STYLE + "In a 1902 Paris physiology laboratory, bearded physiologist Charles Richet and marine biologist Paul Portier look astonished at a kymograph blood-pressure drum dropping sharply after a tiny 22-day booster dose." + QUAL_TAIL,
             {"kind": "WHEN", "label": "PARIS, 15 FEBRUARY 1902", "timeline_step": "1/5 · 15 Feb 1902 (Richet and Portier discover anaphylaxis on Day 22)", "hold_s": 3.5}),
            ("04_igg_10m_vs_ige_100_ng_ml_100000_ratio_and_22_day_anaphylaxis_latency_chart", 17.5, 8.0, "E", False, "SERUM IgG (10,000,000 ng/mL) VS IgE (100 ng/mL = 100,000× RARER) & 22-DAY SENSITIZATION WINDOW", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked serum antibody scale & mast-cell degranulation chart from Portier & Richet (15 Feb 1902) and Ishizaka & Ishizaka (July 1966 J. Immunol.) contrasts human serum IgG (~10 mg/mL = 10,000,000 ng/mL) against IgE (~0.0001 mg/mL = 100 ng/mL, a 100,000-to-1 ratio) alongside Richet's 22-day sensitization window followed by <120-second histamine shock on dose 2.",
             {"kind": "DATA", "label": "HUMAN SERUM IgG (10,000,000 ng/mL) VS ALLERGY ANTIBODY IgE (100 ng/mL = 100,000× RARER)", "detail": "Inked serum antibody scale & mast-cell degranulation chart on period paper contrasting human serum IgG (~10 mg/mL = 10,000,000 ng/mL) against IgE (~0.0001 mg/mL = 100 ng/mL, a 100,000-to-1 ratio) alongside Richet's 22-day sensitization window followed by <120-second histamine shock on dose 2", "scale": "hunting for the allergy antibody in human blood was like searching for a single red marble buried inside a stadium of ten million white marbles — because almost every IgE molecule is parked like a hair-trigger tripwire on the surface of your mast cells", "who_card": "Charles Richet (1850–1935) — French physiologist · Paul Portier (1866–1962) — French marine biologist · Clemens von Pirquet (1874–1929) — Austrian paediatrician · Henry Hallett Dale (1875–1968) — British pharmacologist · Daniel Bovet (1907–1992) — Swiss-Italian pharmacologist · Kimishige Ishizaka (1925–2018) — Japanese-American immunologist · Teruko Ishizaka (1926–2019) — Japanese-American immunologist", "when_stamp": "15 February 1902 · 24 July 1906 · 1910 · 1937 · July 1966", "hold_s": 3.8}),
            ("05_sea_anemone_jar_brass_syringe_histamine_vial_and_y_shaped_ige_model_pan", 25.5, 5.5, "A", False, "1 IN 10 MILLION", "Fast",
             "Fast: daylight macro pan across a glass specimen jar holding a preserved sea anemone, a vintage 1902 brass-and-glass syringe, a glass vial of histamine crystals, and a brass Y-shaped antibody model on an oak bench between code graphics so two full-frame graphics never run back to back. Nothing emissive, no face.",
             STYLE + "In crisp daylight on an oak laboratory bench, the camera pans smoothly across a glass specimen jar with a sea anemone, a vintage graduated glass syringe, a small apothecary vial, and a Y-shaped brass antibody model." + FAST_TAIL,
             None),
            ("06_mast_cell_ige_cross_linking_and_histamine_cascade_vs_antihistamine_chart", 31.0, 8.0, "E", False, "100,000× RARER TRIPWIRE", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period parchment, an inked mast-cell cross-linking & histamine cascade diagram shows 1 allergen molecule (pollen or peanut protein) bridging 2 surface-bound FcεRI-IgE antibodies to release pre-packed histamine granules in <60 seconds, dropping arterial blood pressure and narrowing bronchial airways until epinephrine or Bovet's antihistamine blocks the cascade.",
             {"kind": "DATA", "label": "MAST-CELL CROSS-LINKING: 1 ALLERGEN BRIDGING 2 IgE TRIPWIRES RELEASES ~1,000 HISTAMINE GRANULES IN <60 S", "detail": "Inked mast-cell cross-linking & histamine cascade diagram showing 1 allergen molecule bridging 2 surface-bound IgE antibodies to release pre-packed histamine granules in <60 seconds, dropping arterial blood pressure and narrowing bronchial airways", "scale": "a single mast cell carries up to a thousand microscopic bags of histamine — and cross-linking just two antibody tripwires on its skin is enough to detonate the entire cell", "hold_s": 3.8}),
            ("07_table_three_props_1901_jellyfish_jar_1937_antihistamine_vial_and_1966_ige_mast_model", 39.0, 5.5, "C", False, "1901 TO 2015", "Fast",
             "Fast: daylight prop table (callback source for Part 05: Richet and Portier's 1901 specimen jar, Daniel Bovet's 1937 Pasteur Institute antihistamine bottle, and the Ishizakas' 1966 Y-shaped IgE mast-cell model). Nothing emissive.",
             STYLE + "On an oak workbench in soft window light sit three objects side by side: a glass specimen jar from an ocean expedition, a 1937 glass reagent bottle, and a carved wooden mast-cell model studded with Y-shaped brass tripwires." + FAST_TAIL,
             None),
            ("08_explorer_at_mast_cell_grenade_capping_receptor_bell_as_pollen_grain_bridges_ige_wires", 62.0, 5.5, "A", True, None, "Quality",
             "Quality: Explorer beat 1 (locked character reference, after 1:00).",
             STYLE + "Standing beside a giant round mast-cell sphere covered in Y-shaped brass tripwires, the Explorer watches a tiny golden pollen grain bridge two tripwires at once and slides a shield-shaped safety cap over the receptor bell to silence the alarm." + EXP_TAIL,
             None),
            ("09_richet_portier_july_1901_aboard_yacht_princesse_alice_ii_with_man_of_war_jar", 67.5, 5.5, "B", False, "ATLANTIC OCEAN, JULY 1901", "Quality",
             "Quality: readable faces (in July 1901 aboard Prince Albert I of Monaco's steam yacht Princesse Alice II in the Atlantic, Charles Richet and Paul Portier examine the stinging tentacles of a Portuguese man-of-war in a glass jar on deck).",
             STYLE + "On the sunny wooden deck of a 1901 steam research yacht in the Atlantic Ocean, French scientists Charles Richet and Paul Portier inspect a purple Portuguese man-of-war suspended inside a glass specimen jar beside ocean dredging nets." + QUAL_TAIL,
             {"kind": "WHEN", "label": "ATLANTIC OCEAN, JULY 1901", "timeline_step": "1/5 · Jul 1901 & 15 Feb 1902 (Richet and Portier study marine venoms aboard Princesse Alice II and discover anaphylaxis)", "hold_s": 3.5}),
        ],
    ),
    (
        2,
        "Part 02 — July 1901 – 15 February 1902: The Yacht Princesse Alice II, the Dog Named Neptune & Why Vaccination Went Backwards",
        [
            ("01_yacht_princesse_alice_ii_1901_neptune_15_feb_1902_and_pirquet_24_jul_1906_allergy", 73.0, 6.5, "A", False, "AGAINST PROTECTION (1902)", "Quality",
             "Quality: readable faces (Charles Richet and Paul Portier aboard Prince Albert I's yacht Princesse Alice II in July 1901 and in Paris on 15 February 1902 discovering anaphylaxis on Day 22, followed by Viennese paediatrician Clemens von Pirquet on 24 July 1906 coining 'allergy').",
             STYLE + "Split period scene: on the left in a 1902 Paris laboratory, Charles Richet and Paul Portier record the Day-22 anaphylactic reaction in their notebook beside a healthy brown dog; on the right in 1906 Vienna, paediatrician Clemens von Pirquet writes at his clinic desk." + QUAL_TAIL,
             {"kind": "FACT", "label": "Against protection (1902)", "when_stamp": "July 1901 · 15 February 1902 · 24 July 1906 · 1913", "timeline_step": "1/5 · Jul 1901 & 15 Feb 1902 (anaphylaxis) & 2/5 · 24 Jul 1906 (Clemens von Pirquet coins allergy)", "hold_s": 3.8}),
            ("02_portier_richet_15_feb_1902_dose_response_2cc_vs_01cc_day22_anaphylaxis_chart", 79.5, 8.0, "E", False, "15 FEB 1902 PORTIER & RICHET: UNTREATED DOG SURVIVES >2.0 cc/kg VS PRIMED DOG (DAY 22) SHOCK AT 0.10 cc/kg (>20× DROP)", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked dose-response & latent-period chart from Portier & Richet (15 February 1902, C. R. Soc. Biol. 54: 170–172) contrasts an untreated dog surviving >2.0 cc/kg of actinia toxin for days against a primed dog (22 days after a tiny first dose) suffering fatal shock within 25 minutes from just 0.10 cc/kg (a >20-fold drop in lethal threshold).",
             {"kind": "DATA", "label": "15 FEB 1902 ANAPHYLAXIS DOSE PARADOX: >2.0 cc/kg SURVIVED ON DOSE 1 VS 0.10 cc/kg SHOCK ON DAY 22", "detail": "Inked dose-response & latent-period chart on period paper from Portier & Richet (15 February 1902, C. R. Soc. Biol. 54: 170–172) contrasting an untreated dog surviving >2.0 cc/kg of actinia toxin for days against a primed dog (22 days after a tiny first dose) suffering fatal shock within 25 minutes from just 0.10 cc/kg (a >20-fold drop in lethal threshold)", "scale": "a dose twenty times too small to hurt a first-time animal became lethal in minutes on the second visit — because the danger wasn't the jellyfish poison anymore, it was the body's own counter-attack", "hold_s": 3.8}),
            ("03_comptes_rendus_15_feb_1902_manuscript_syringe_and_monaco_expedition_jar_closeup", 87.5, 6.5, "B", False, "15 FEBRUARY 1902 — ANAPHYLAXIS", "Fast",
             "Fast: daylight macro shot of Richet and Portier's 15 February 1902 Comptes Rendus manuscript beside a graduated glass syringe and a Monaco oceanographic specimen jar on an oak desk. Nothing emissive, no face.",
             STYLE + "In crisp daylight on a French physiology desk, an open 1902 scientific journal rests beside a brass-and-glass syringe and a glass specimen jar containing sea anemones." + FAST_TAIL,
             None),
            ("04_yacht_dredging_net_compass_and_22_day_calendar_ledger_pan", 94.0, 5.5, "C", False, "24 JULY 1906 — ALLERGY", "Fast",
             "Fast: daylight close-up pan across a brass maritime compass, coiled hemp dredging rope, and an open 22-day laboratory ledger with fountain pen on a wooden table. Nothing emissive, no face.",
             STYLE + "In bright window light on an oak table, a brass ship's compass and coiled sampling line sit beside an open leather laboratory diary and a fountain pen." + FAST_TAIL,
             None),
        ],
    ),
    (
        3,
        "Part 03 — 1910, 1937 & 1953: Henry Dale's Histamine Bomb, Mast Cells & Daniel Bovet's First Antihistamine — Midpoint Twist",
        [
            ("01_henry_dale_1910_histamine_daniel_bovet_staub_1937_929f_and_riley_1953_mast_cells", 99.5, 6.5, "A", False, "FIRST ANTIHISTAMINE IN 1937", "Quality",
             "Quality: readable faces (British pharmacologist Henry Hallett Dale in London in 1910–1927 demonstrating histamine shock, dissolving to Swiss-Italian pharmacologist Daniel Bovet and French biochemist Anne-Marie Staub at the Pasteur Institute in Paris in 1937 synthesising the first antihistamine 929F, and James Riley in Dundee in 1953 revealing purple histamine granules packed inside tissue mast cells).",
             STYLE + "Split period scene: on the left in a 1910 London pharmacology lab, Henry Dale inspects a physiological kymograph trace; on the right in 1937 Paris, Daniel Bovet and Anne-Marie Staub hold up a glass vial of compound 929F beside a microscope showing granule-packed mast cells." + QUAL_TAIL,
             {"kind": "WHO", "label": "James F. Riley (1912–1985) — British physician and anatomist · Anne-Marie Staub (1914–2012) — French biochemist", "fact_card": "First antihistamine in 1937", "when_stamp": "1910 · 1927 · 1937 · 1953 · 1957", "timeline_step": "3/5 · 1910 & 1937 (Henry Dale identifies histamine and Daniel Bovet synthesises the first antihistamine 929F)", "hold_s": 3.8}),
            ("02_dale_1910_histamine_shock_riley_1953_mast_cell_and_bovet_1937_929f_blockade_chart", 106.0, 8.0, "E", False, "1910–1953 HISTAMINE & MAST-CELL GRANULES VS 1937 BOVET & STAUB 929F H1 RECEPTOR BLOCKADE & EPINEPHRINE", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked histamine vs antihistamine receptor-blockade chart from Dale & Laidlaw (1910 J. Physiol. 41: 318–344), Bovet & Staub (1937 C. R. Soc. Biol. 124: 547–549), and Riley & West (1953 J. Physiol. 120: 528–537) shows mast-cell histamine granules causing airway constriction and vascular leakage, blocked competitively at H1 receptors by Bovet's 1937 compound 929F and countered physiologically by epinephrine.",
             {"kind": "DATA", "label": "HISTAMINE GRANULE RELEASE (1910/1953) VS BOVET'S 1937 H1 ANTIHISTAMINE CAP & ADRENALINE RESCUE", "detail": "Inked histamine vs antihistamine receptor-blockade chart on period paper from Dale & Laidlaw (1910 J. Physiol. 41: 318–344), Bovet & Staub (1937 C. R. Soc. Biol. 124: 547–549), and Riley & West (1953 J. Physiol. 120: 528–537) showing mast-cell histamine granules causing airway constriction and vascular leakage, blocked competitively at H1 receptors by Bovet's 1937 compound 929F and countered physiologically by epinephrine", "scale": "your own nose, skin, and lungs are lined with millions of pre-loaded histamine grenades — and an antihistamine tablet works by slipping a safety cap over the receptor lock before the histamine can turn it", "hold_s": 3.8}),
            ("03_pasteur_institute_1937_vial_929f_and_mast_cell_microscope_slide_closeup", 114.0, 6.5, "B", False, "1937 — FIRST ANTIHISTAMINE", "Fast",
             "Fast: daylight macro shot of a glass reagent vial of compound 929F beside a brass microscope holding a purple-stained slide of granule-filled mast cells on a 1937 Pasteur Institute bench. Nothing emissive, no face.",
             STYLE + "In crisp daylight on a Paris laboratory workbench, a glass reagent bottle sits beside a brass microscope with a purple-stained histology slide and a wooden slide box." + FAST_TAIL,
             None),
            ("04_adrenaline_ampoule_autoinjector_and_bronchial_airway_model_pan", 120.5, 5.5, "C", False, "1953 — MAST CELL GRANULES", "Fast",
             "Fast: daylight close-up pan across a vintage glass ampoule of adrenaline, a modern spring-loaded autoinjector cylinder, and a cutaway anatomical model of bronchial airways on an oak table. Nothing emissive, no face.",
             STYLE + "In bright window light on a medical workbench, a small glass ampoule and a cylindrical emergency autoinjector rest beside a cutaway anatomical model of open lung airways." + FAST_TAIL,
             None),
        ],
    ),
    (
        4,
        "Part 04 — 1921 & July 1966: Prausnitz & Küstner's Fish-Allergy Blood Swap & Kimishige and Teruko Ishizaka's 1-in-10-Million IgE",
        [
            ("01_prausnitz_kustner_1921_serum_transfer_and_kimishige_teruko_ishizaka_july_1966_ige", 126.0, 6.5, "A", False, "100,000× RARER ANTIBODY", "Quality",
             "Quality: readable faces (Carl Prausnitz in Breslau in 1921 injecting a drop of Heinz Küstner's fish-allergic serum into his own forearm to transfer a wheal-and-flare hive, dissolving to husband-and-wife immunologists Kimishige Ishizaka and Teruko Ishizaka in Denver in July 1966 purifying the 100-nanogram-per-millilitre IgE antibody).",
             STYLE + "Split period scene: on the left in a 1921 German clinic, Carl Prausnitz and Heinz Küstner examine a localized skin test on a forearm; on the right in a 1966 Denver immunology lab, Kimishige and Teruko Ishizaka hold up a glass gel plate showing the purified IgE antibody band." + QUAL_TAIL,
             {"kind": "WHO", "label": "Carl Prausnitz (1876–1963) — German-British bacteriologist · Heinz Küstner (1897–1963) — German gynaecologist and bacteriologist", "fact_card": "100,000× rarer antibody", "when_stamp": "1921 · July 1966 · 1967 · February 1968", "timeline_step": "4/5 · 1921 & Jul 1966 (Prausnitz & Küstner transfer allergy in serum; Kimishige and Teruko Ishizaka purify the 100 ng/mL IgE antibody)", "hold_s": 3.8}),
            ("02_prausnitz_1921_transfer_and_ishizaka_1966_ige_vs_parasitic_worm_defense_chart", 132.5, 8.0, "E", False, "1921 PRAUSNITZ-KÜSTNER TRANSFER & JULY 1966 ISHIZAKA IgE (100 ng/mL) ANTI-HELMINTH WORM DEFENSE CHART", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked Prausnitz-Küstner skin transfer & IgE vs parasitic-worm defense diagram from Prausnitz & Küstner (1921 Zbl. Bakt. 86: 160–169) and Ishizaka, Ishizaka & Hornbrook (July 1966, J. Immunol. 97: 75–85) shows serum IgE (100 ng/mL vs 10,000,000 ng/mL IgG) arming mast cells to expel macroscopic helminth worms and degrade venoms, misfiring on harmless pollen/peanut proteins in worm-free modern environments.",
             {"kind": "DATA", "label": "JULY 1966 IgE (100 ng/mL) MACROSCOPIC PARASITE DEFENSE VS MODERN POLLEN/PEANUT MISFIRE", "detail": "Inked Prausnitz-Küstner skin transfer & IgE vs parasitic-worm defense diagram on period paper from Prausnitz & Küstner (1921 Zbl. Bakt. 86: 160–169) and Ishizaka, Ishizaka & Hornbrook (July 1966, J. Immunol. 97: 75–85) showing serum IgE (100 ng/mL vs 10,000,000 ng/mL IgG) arming mast cells to expel macroscopic helminth worms and degrade venoms, misfiring on harmless pollen/peanut proteins in worm-free modern environments", "scale": "a white blood cell trying to swallow a parasitic hookworm is like a mouse trying to swallow a python — so evolution built the IgE histamine bomb to flood the tunnels and blast the giant invader out", "hold_s": 3.8}),
            ("03_denver_1966_immunodiffusion_gel_plate_centrifuge_tubes_and_ige_model_closeup", 140.5, 6.5, "B", False, "JULY 1966 — IgE DISCOVERED", "Fast",
             "Fast: daylight macro shot of the Ishizakas' 1966 glass immunodiffusion gel plate with curved precipitin arcs, glass centrifuge tubes, and a Y-shaped brass IgE antibody model on a Denver laboratory bench. Nothing emissive, no face.",
             STYLE + "In crisp daylight on an immunology workbench, a clear glass gel-diffusion plate with delicate white curved arcs sits beside glass centrifuge tubes and a Y-shaped brass antibody model." + FAST_TAIL,
             None),
            ("04_explorer_pulling_ige_mast_cell_flush_lever_to_blast_giant_hookworm_out_of_tunnel", 147.0, 5.5, "B", True, None, "Quality",
             "Quality: Explorer beat 2 (locked character reference).",
             STYLE + "Standing beside a tiny white blood cell dwarfed by a giant cartoon hookworm inside a tunnel, the Explorer pulls a red mast-cell flush lever that blasts the giant worm right out of the tunnel with a wave of water spray." + EXP_TAIL,
             None),
        ],
    ),
    (
        5,
        "Part 05 — Why Early Peanuts Cut Allergy by 81% — & How a Boiling Yellowstone Puddle Unlocked DNA",
        [
            ("01_timeline_1901_2015_and_gideon_lack_leap_trial_81pct_peanut_allergy_reduction_chart", 152.5, 8.5, "E", False, "1901–2015 TIMELINE · RICHET ANAPHYLAXIS, PIRQUET ALLERGY, DALE & BOVET HISTAMINE, ISHIZAKA IgE & LACK 81% LEAP TRIAL", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, the 5-date timeline completes: Jul 1901 & 15 Feb 1902 (Charles Richet and Paul Portier discover anaphylaxis in dogs primed with sea-anemone venom) · 24 Jul 1906 (Clemens von Pirquet coins the word allergy) · 1910 & 1937 (Henry Dale identifies histamine and Daniel Bovet synthesises the first antihistamine 929F) · 1921 & Jul 1966 (Prausnitz & Küstner transfer allergy in serum; Kimishige and Teruko Ishizaka purify the 100 ng/mL IgE antibody) · 26 Feb 2015 (Gideon Lack's LEAP trial proves early infant peanut introduction cuts peanut allergy by 81%: 17.2% avoidance vs 3.2% consumption).",
             {"kind": "DATA", "label": "1901–2015 ALLERGY TIMELINE & 26 FEB 2015 LEAP TRIAL (17.2% AVOIDANCE VS 3.2% EARLY PEANUT = 81% DROP)", "detail": "Animated 5-date timeline (1901 → 2015) alongside the LEAP trial bar chart (17.2% peanut allergy in avoidance group vs 3.2% in early-consumption group = 81% reduction)", "scale": "what began as a baffling jellyfish experiment aboard a prince's yacht in nineteen oh-one now lets doctors disarm the body's hair-trigger grenades and stop food allergies before they ever start", "who_card": "Gideon Lack (born 1961) — British paediatric allergist", "when_stamp": "26 February 2015 · 1901–2015", "timeline_step": "5/5 · 1901–2015 timeline complete", "hold_s": 3.8}),
            ("02_smooth_peanut_butter_spoon_epipen_and_ige_model_on_plinth_pan", 161.0, 5.5, "A", False, "81% FEWER PEANUT ALLERGIES", "Fast",
             "Fast: daylight close-up of a baby spoon of smooth peanut puree beside whole roasted peanuts, an emergency autoinjector cylinder, and a brass Y-shaped antibody model on a wooden museum plinth. Nothing emissive, no face.",
             STYLE + "In crisp daylight on a wooden museum plinth, a small spoon of smooth peanut butter and roasted peanuts sit beside a cylindrical medical autoinjector and a brass Y-shaped antibody sculpture." + FAST_TAIL,
             None),
            ("03_thomas_brock_19_sep_1966_yellowstone_70c_mullis_1983_pcr_and_jeffreys_1984_dna_handoff", 166.5, 6.5, "C", False, "1 BILLION DNA COPIES", "Quality",
             "Quality: readable faces (microbiologist Thomas Brock kneeling beside the steaming 70 °C waters of Mushroom Spring in Yellowstone National Park on 19 September 1966, alongside Kary Mullis in April 1983 doubling DNA 1,073,741,824 times with PCR and Alec Jeffreys on 10 September 1984 holding up the first DNA fingerprint X-ray — handoff to 053 PCR & DNA Fingerprinting).",
             STYLE + "Split period scene: on the left in September 1966 in Yellowstone National Park, microbiologist Thomas Brock lifts a microscope slide from a steaming turquoise geothermal pool; on the right in 1984 Leicester, geneticist Alec Jeffreys holds up a developed DNA barcode X-ray film beside a thermal cycler." + QUAL_TAIL,
             {"kind": "WHEN", "label": "19 SEPTEMBER 1966 · APRIL 1983 · 10 SEPTEMBER 1984", "hold_s": 3.5}),
            ("04_table_three_callback", 173.0, 2.4, "C", False, None, "reuse",
             "Reuse: verified unused moving window [5.50s..7.90s] of P1:07_table_three_props_1901_jellyfish_jar_1937_antihistamine_vial_and_1966_ige_mast_model (callback, £0).",
             "Reuse P1:07_table_three_props_1901_jellyfish_jar_1937_antihistamine_vial_and_1966_ige_mast_model [5.50s..7.90s] (2.40s distinct non-overlapping tail window from 8.00s source clip).",
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
                row["reuse_of"] = "P1:07_table_three_props_1901_jellyfish_jar_1937_antihistamine_vial_and_1966_ige_mast_model"
                row["reuse_window_s"] = [5.5, 7.9]
                row["reuse_audit"] = {
                    "source_row": "P1:07_table_three_props_1901_jellyfish_jar_1937_antihistamine_vial_and_1966_ige_mast_model",
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
            "film": "052_Richet-Dale-Bovet-Ishizaka-Allergies-Anaphylaxis-IgE",
            "part": p_idx,
            "title": p_title,
            "version": "v01",
            "timing_status": "pre_vo_script_clock (built from allergies_script_master_v01.md; retimes onto Scribe STT once VO locks)",
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
        "film": "052_Richet-Dale-Bovet-Ishizaka-Allergies-Anaphylaxis-IgE",
        "version": "v01",
        "date": "2026-10-18",
        "owner": "gemini (J0585)",
        "status": "PRE_VO_BOARDS_V01_NO_MINT",
        "generation_authorized": False,
        "script": "00_Brand/Channel-Setup/ideas/052_Richet-Dale-Bovet-Ishizaka-Allergies-Anaphylaxis-IgE/allergies_script_master_v01.md",
        "sources": "00_Brand/Channel-Setup/ideas/052_Richet-Dale-Bovet-Ishizaka-Allergies-Anaphylaxis-IgE/SOURCES_v01.md",
        "credit_snapshot": {
            "flow_balance": 23740,
            "flow_floor": 0,
            "flow_read_at": "2026-10-15T21:42:22Z",
            "vertex_promo_gbp": 71.02,
            "vertex_usable_gbp": 70.02,
        },
        "totals": totals,
        "per_part": per_part_summary,
        "mint_order": "006 > 007 > 008 > 009 > 010 > 011 > 012 > 013 > 014 > 015 > 016 > 017 > 018 > 019 > 020 > 021 > 022 > 023 > 024 > 025 > 026 > 027 > 028 > 029 > 030 > 031 > 032 > 033 > 034 > 035 > 036 > 037 > 038 > 039 > 040 > 041 > 042 > 043 > 044 > 045 > 046 > 047 > 048 > 049 > 050 > 051 > 052 > 053. Nothing in 052 is generation_authorized.",
    }
    (EDIT / "PICTURE_PLAN_v01.json").write_text(json.dumps(plan, indent=2) + "\n")

    sl = [
        "# 052 Allergies & Anaphylaxis: The 1901 Yacht Test That Went Backwards — Shot list & plate boards v01 (pre-VO)",
        "",
        "Gemini, 18 Oct 2026, J0585. Built from `allergies_script_master_v01.md` (`91.8 PASS`) and `SOURCES_v01.md`.",
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
        "# 052 price review v01 (pre-VO plate boards)",
        "",
        "Gemini, 18 Oct 2026, J0585. Boards only. **No mint. No spend. No merge.**",
        "Prepared from `allergies_script_master_v01.md` (`91.8 PASS`) and `SOURCES_v01.md` so 052's full plate board rows, non-emissive Fast prompts, £0 code graphics, and Teach-on-Screen overlays are ready to re-time the moment long VO locks. Parked for Chief.",
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
        f"- **Quality ({totals['Quality']} rows):** readable faces (Charles Richet, Paul Portier, Clemens von Pirquet, Henry Hallett Dale, Daniel Bovet, Anne-Marie Staub, James Riley, Carl Prausnitz, Heinz Küstner, Kimishige Ishizaka, Teruko Ishizaka, Gideon Lack, Thomas Brock, Kary Mullis, Alec Jeffreys), July 1901 *Princesse Alice II* yacht expedition & 15 February 1902 Paris Day-22 anaphylaxis discovery, 1910–1937 histamine & Pasteur Institute 929F antihistamine lab, 1921 Breslau serum transfer & July 1966 Denver IgE isolation, and the 2 Explorer beats.",
        f"- **Fast ({totals['Fast']} rows, non-emissive):** daylight prop and laboratory shots (sea-anemone specimen jar, brass syringe, histamine vial & Y-shaped IgE model pan, 3-object callback bench, 15 February 1902 *Comptes Rendus* manuscript & syringe, maritime compass & 22-day ledger, Pasteur Institute 1937 compound 929F vial & mast-cell microscope slide, adrenaline ampoule & bronchial airway model, Denver 1966 immunodiffusion gel plate & centrifuge tubes, smooth peanut spoon & autoinjector on plinth). Zero candles, flames, sparks, or glowing elements on Fast.",
        f"- **£0 code graphics ({totals['code_graphic']} rows):**",
        "  1. `P1:04_igg_10m_vs_ige_100_ng_ml_100000_ratio_and_22_day_anaphylaxis_latency_chart` — human serum IgG (10,000,000 ng/mL) vs IgE (100 ng/mL = 100,000× rarer) and Richet's 22-day sensitization window followed by <120 s histamine shock (`SCALE: hunting for the allergy antibody in human blood was like searching for a single red marble buried inside a stadium of ten million white marbles — because almost every IgE molecule is parked like a hair-trigger tripwire on the surface of your mast cells`)",
        "  2. `P1:06_mast_cell_ige_cross_linking_and_histamine_cascade_vs_antihistamine_chart` — mast-cell FcεRI-IgE cross-linking by a single allergen molecule releasing ~1,000 histamine granules in <60 s (`SCALE: a single mast cell carries up to a thousand microscopic bags of histamine — and cross-linking just two antibody tripwires on its skin is enough to detonate the entire cell`)",
        "  3. `P2:02_portier_richet_15_feb_1902_dose_response_2cc_vs_01cc_day22_anaphylaxis_chart` — Portier & Richet's 15 February 1902 dose-response chart (>2.0 cc/kg survived on Dose 1 vs fatal shock within 25 min from 0.10 cc/kg on Day 22, a >20-fold drop in lethal threshold) (`SCALE: a dose twenty times too small to hurt a first-time animal became lethal in minutes on the second visit — because the danger wasn't the jellyfish poison anymore, it was the body's own counter-attack`)",
        "  4. `P3:02_dale_1910_histamine_shock_riley_1953_mast_cell_and_bovet_1937_929f_blockade_chart` — Dale's 1910 histamine shock, Riley's 1953 mast-cell granules, and Bovet & Staub's 1937 compound 929F competitive H1 blockade + epinephrine physiological rescue (`SCALE: your own nose, skin, and lungs are lined with millions of pre-loaded histamine grenades — and an antihistamine tablet works by slipping a safety cap over the receptor lock before the histamine can turn it`)",
        "  5. `P4:02_prausnitz_1921_transfer_and_ishizaka_1966_ige_vs_parasitic_worm_defense_chart` — Prausnitz-Küstner 1921 passive serum transfer and Ishizaka July 1966 IgE (100 ng/mL) anti-helminth worm expulsion vs modern pollen/peanut misfire (`SCALE: a white blood cell trying to swallow a parasitic hookworm is like a mouse trying to swallow a python — so evolution built the IgE histamine bomb to flood the tunnels and blast the giant invader out`)",
        "  6. `P5:01_timeline_1901_2015_and_gideon_lack_leap_trial_81pct_peanut_allergy_reduction_chart` — completed 5-date timeline (1901 → 2015) + Gideon Lack's 26 February 2015 LEAP trial bar chart (17.2% avoidance vs 3.2% early peanut = 81% reduction) (`SCALE: what began as a baffling jellyfish experiment aboard a prince's yacht in nineteen oh-one now lets doctors disarm the body's hair-trigger grenades and stop food allergies before they ever start`)",
        f"- **£0 verified reuse ({totals['reuse']} row):** `P5:04_table_three_callback` uses the 2.40 s unused moving tail `[5.50s..7.90s]` of `P1:07_table_three_props_1901_jellyfish_jar_1937_antihistamine_vial_and_1966_ige_mast_model`.",
        "",
        "## Mint order",
        "",
        "006 > 007 > 008 > 009 > 010 > 011 > 012 > 013 > 014 > 015 > 016 > 017 > 018 > 019 > 020 > 021 > 022 > 023 > 024 > 025 > 026 > 027 > 028 > 029 > 030 > 031 > 032 > 033 > 034 > 035 > 036 > 037 > 038 > 039 > 040 > 041 > 042 > 043 > 044 > 045 > 046 > 047 > 048 > 049 > 050 > 051 > 052 > 053. `generation_authorized` is `false` on every row.",
    ])
    (EDIT / "PRICE_REVIEW_v01.md").write_text("\n".join(pr_lines) + "\n")
    print(f"052 v01 boards written: {totals['rows']} rows, Flow expected={totals['flow_credits_expected']}")


if __name__ == "__main__":
    main()
