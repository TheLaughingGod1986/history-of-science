#!/usr/bin/env python3
"""HOS 041 (Willow Bark to Aspirin & How Painkillers Work) pre-VO plate boards v01. J0540. No mint, no spend.

Built from 00_Brand/Channel-Setup/ideas/041_Stone-Hoffmann-Vane-Aspirin-Painkillers/aspirin_script_master_v01.md
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
        "Part 01 — The Willow Tree in Oxfordshire and the Dye Factory in Germany",
        [
            ("01_hoffmann_10_aug_1897_elberfeld_aspirin_flask_and_stone_1763_willow_bark", 0.0, 5.5, "A", False, "FROM TREE BARK TO ASPIRIN", "Quality",
             "Quality: Short frame 0 / answer image (0:03) + inside the Friedrich Bayer & Co. laboratory in Elberfeld, Germany, on 10 August 1897, 29-year-old chemist Felix Hoffmann crystallises pure white acetylsalicylic acid (Aspirin) in a glass flask beside a letter from his rheumatism-stricken father, dissolving to an Oxfordshire riverbank in 1758–1763 where Reverend Edward Stone tastes a strip of bitter white willow bark.",
             STYLE + "Inside an 1897 German pharmaceutical laboratory in Elberfeld, twenty-nine-year-old chemist Felix Hoffmann in a dark waistcoat holds up a glass flask of gleaming white acetylsalicylic acid crystals, dissolving to an Oxfordshire riverbank where clergyman Edward Stone peels a strip of pale willow bark." + QUAL_TAIL,
             {"kind": "WHEN", "label": "ELBERFELD, 10 AUGUST 1897 · OXFORDSHIRE, 25 APRIL 1763", "timeline_step": "1/5 · 25 Apr 1763 (Reverend Edward Stone reports curing 50 fever patients with white willow bark) & 3/5 · 10 Aug 1897 (Felix Hoffmann synthesises pure acetylsalicylic acid at Bayer)", "hold_s": 3.5}),
            ("02_stone_1763_willow_letter_hoffmann_1897_notebook_and_vane_1971_cox_split", 5.5, 6.0, "B", False, "WILLOW BARK, 1897 LAB, COX ENZYME", "Quality",
             "Quality: complex three-part split composition (Reverend Edward Stone's 25 April 1763 Royal Society letter on white willow bark on the left; Felix Hoffmann's 10 August 1897 lab notebook entry and white crystals in the centre; Sir John Vane's 1971 cyclooxygenase enzyme model on the right).",
             STYLE + "Three-panel period composition: on the left, dried strips of willow bark beside a brass mortar and pestle; in the centre, a glass flask of white needle crystals on an open leather notebook; on the right, a brass-and-wood lock-and-key enzyme model beside a white tablet." + QUAL_TAIL,
             None),
            ("03_hoffmann_and_eichengrun_10_aug_1897_elberfeld_water_bath_acetylation", 11.5, 6.0, "C", False, "10 AUGUST 1897", "Quality",
             "Quality: readable faces (inside the Elberfeld lab on 10 August 1897, 29-year-old Felix Hoffmann working alongside lab head Arthur Eichengrün reacts salicylic acid with acetic anhydride over a warm water bath).",
             STYLE + "Inside the 1897 Bayer laboratory in Elberfeld, twenty-nine-year-old chemist Felix Hoffmann and colleague Arthur Eichengrün inspect a glass reflux condenser over a copper water bath as pure white crystals form." + QUAL_TAIL,
             {"kind": "WHEN", "label": "ELBERFELD, 10 AUGUST 1897", "timeline_step": "3/5 · 10 Aug 1897 (Felix Hoffmann synthesises pure acetylsalicylic acid at Bayer in Elberfeld)", "hold_s": 3.5}),
            ("04_stone_1763_50_patients_hoffmann_1897_asa_and_40000_tonnes_annual_chart", 17.5, 8.0, "E", False, "1763 WILLOW BARK (50 PATIENTS) → 1897 ACETYLSALICYLIC ACID → ~40,000 TONNES (~100B TABLETS/YR)", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked clinical and chemical chart shows Edward Stone's 1763 trial (50 of 50 ague/fever patients relieved with 20 grains / ~1.3 g of dried willow bark every 4 hours), Felix Hoffmann's 10 August 1897 acetylation (salicylic acid + acetic anhydride → 100% pure acetylsalicylic acid), and global consumption (~40,000 tonnes / ~100 billion tablets per year).",
             {"kind": "DATA", "label": "1763 WILLOW BARK (50 PATIENTS) · 10 AUG 1897 ASA SYNTHESIS · ~40,000 TONNES (~100B PILLS/YR)", "detail": "Inked clinical & chemical chart on period paper showing Edward Stone's 1763 trial (50 of 50 ague/fever patients relieved with 20 grains / ~1.3 g of dried willow bark every 4 hours), Felix Hoffmann's 10 August 1897 acetylation (salicylic acid + acetic anhydride → acetylsalicylic acid, 100% pure crystals), and global consumption (~40,000 tonnes / ~100 billion tablets per year)", "scale": "humans swallow roughly forty thousand tonnes of aspirin every single year — more than a hundred billion little white tablets, enough to stretch to the Moon and back", "who_card": "Edward Stone (1702–1768) — English clergyman and natural philosopher · Felix Hoffmann (1868–1946) — German industrial chemist · John Vane (1927–2004) — British pharmacologist", "when_stamp": "25 April 1763 · 10 August 1897 · 23 June 1971", "hold_s": 3.8}),
            ("05_white_willow_bark_meadowsweet_blossoms_and_glass_crystal_dish_pan", 25.5, 5.5, "A", False, "ELBERFELD, 1897", "Fast",
             "Fast: daylight macro pan across strips of dried white willow bark, cream-coloured meadowsweet blossoms, and a glass dish of pure white needle crystals on an oak bench between code graphics so two full-frame graphics never run back to back. Nothing emissive, no face.",
             STYLE + "In crisp daylight on an oak apothecary bench, the camera pans smoothly across dried strips of willow bark, cream meadowsweet flowers, and a glass dish of white needle crystals." + FAST_TAIL,
             None),
            ("06_seventy_four_year_mechanism_mystery_bar_1897_hoffmann_to_1971_vane", 31.0, 8.0, "E", False, "74 YEARS OF MYSTERY", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period parchment, an inked 74-year mystery bar compares 10 August 1897 (acetylsalicylic acid synthesised at Bayer) to 23 June 1971 (John Vane proves aspirin irreversibly inhibits prostaglandin synthesis via the COX enzyme).",
             {"kind": "DATA", "label": "74-YEAR MECHANISM GAP: 10 AUG 1897 (SYNTHESIS) TO 23 JUN 1971 (JOHN VANE COX DISCOVERY)", "detail": "Inked 74-year mystery bar comparing 10 August 1897 (acetylsalicylic acid synthesised at Bayer) to 23 June 1971 (John Vane proves aspirin irreversibly inhibits prostaglandin synthesis via the COX enzyme)", "scale": "for nearly three-quarters of a century, doctors prescribed the world's most popular medicine completely blind to what it did inside a human cell", "hold_s": 3.8}),
            ("07_table_three_props_willow_bark_tin_amber_aspirin_bottle_kymograph_drum", 39.0, 5.5, "C", False, "1763 TO 1971", "Fast",
             "Fast: daylight prop table (callback source for Part 05: Reverend Edward Stone's baker's tin of dried willow bark, an 1899 amber glass pharmaceutical bottle of acetylsalicylic acid powder, and John Vane's brass kymograph recording drum). Nothing emissive.",
             STYLE + "On an oak workbench in soft window light sit three objects side by side: an iron baker's tray holding dried willow bark and a brass mortar, an amber glass apothecary bottle, and a brass revolving kymograph drum." + FAST_TAIL,
             None),
            ("08_explorer_capping_clockwork_enzyme_alarm_bell_with_white_aspirin_shield", 62.0, 5.5, "A", True, None, "Quality",
             "Quality: Explorer beat 1 (locked character reference, after 1:00).",
             STYLE + "Standing beside a vibrating brass alarm bell where a tiny clockwork enzyme hammer strikes the bell, the Explorer slips a smooth white cap over the hammer head, silencing the vibrating bell instantly with a relieved smile." + EXP_TAIL,
             None),
            ("09_john_vane_june_1971_london_examining_kymograph_prostaglandin_trace", 67.5, 5.5, "B", False, "LONDON, JUNE 1971", "Quality",
             "Quality: readable face (in June 1971 at the Royal College of Surgeons in London, 44-year-old British pharmacologist John Vane examines a kymograph tissue trace showing aspirin completely halting prostaglandin release).",
             STYLE + "Inside a 1971 London pharmacology laboratory, forty-four-year-old British scientist John Vane in a white lab coat smiles as he inspects a revolving kymograph drum where a stylus trace drops flat." + QUAL_TAIL,
             None),
        ],
    ),
    (
        2,
        "Part 02 — Bitter Willow Bark, a Baker's Oven & the Acid That Burned Stomachs",
        [
            ("01_edward_stone_1763_oxfordshire_willow_bark_and_piria_1838_salicylic_acid", 73.0, 6.5, "A", False, "BAKED BARK IN A BREAD OVEN", "Quality",
             "Quality: readable faces (Reverend Edward Stone in Chipping Norton, Oxfordshire, in 1758–1763 drying white willow bark in a baker's oven and weighing 20-grain doses, dissolving to Italian chemist Raffaele Piria in 1838 isolating salicylic acid in his laboratory).",
             STYLE + "Split period scene: on the left in Oxfordshire in 1763, clergyman Edward Stone grinds oven-dried willow bark in a brass mortar beside a balance scale; on the right in 1838, Italian chemist Raffaele Piria pours yellow salicin solution into a glass crystallization dish." + QUAL_TAIL,
             {"kind": "WHO", "label": "Raffaele Piria (1814–1865) — Italian chemist", "fact_card": "Baked bark in a bread oven", "when_stamp": "1550 BC · 1758 · 25 April 1763 · 1828 · 1838 · 1876", "timeline_step": "1/5 · 25 Apr 1763 (Stone reports 50 fever patients cured with willow bark) & 2/5 · 1828–1838 (Buchner, Leroux & Piria isolate salicin and salicylic acid)", "hold_s": 3.8}),
            ("02_stone_1763_1lb_bark_20_grains_to_1876_4_6g_corrosive_salicylic_acid_chart", 79.5, 8.0, "E", False, "1763 WILLOW BARK (20 GRAINS = 1.3 G, 50 CURED) → 1838–1876 SALICYLIC ACID (4–6 G/DAY CORROSIVE DOSE)", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked extraction and dose diagram shows 1 pound of dried white willow bark (Edward Stone 1763, 50 fever patients cured with 20 grains / 1.3 g) yielding salicin (1828) and salicylic acid (Piria 1838), where arthritis patients in 1876 required 4–6 grams per day of corrosive raw acid.",
             {"kind": "DATA", "label": "1763 WILLOW BARK (20 GRAINS / 1.3 G, 50 CURED) VS 1876 SALICYLIC ACID (4–6 G/DAY CAUSTIC DOSE)", "detail": "Inked extraction & dose diagram on period paper showing 1 pound of dried white willow bark (Edward Stone 1763, 50 fever patients cured with 20 grains / 1.3 g) yielding salicin (1828) and salicylic acid (Piria 1838), where arthritis patients required 4–6 grams per day of corrosive acid", "scale": "to calm swollen joints in the eighteen seventies, arthritis patients had to swallow up to six grams of raw salicylic acid every single day — a dose so caustic it stripped the lining of their stomachs", "hold_s": 3.8}),
            ("03_dried_willow_bark_in_bakers_tin_and_brass_grain_scales_closeup", 87.5, 6.5, "B", False, "25 APRIL 1763 — 50 PATIENTS", "Fast",
             "Fast: daylight macro shot of oven-dried white willow bark strips in an iron baking tray beside a brass apothecary balance weighing pale powder on parchment paper. Nothing emissive, no face.",
             STYLE + "In crisp daylight on a wooden table, dried curls of willow bark rest in an iron baking tin beside a brass apothecary balance and a small pile of ground bark powder." + FAST_TAIL,
             None),
            ("04_yellow_salicin_and_needle_salicylic_acid_crystals_in_glass_dishes", 94.0, 5.5, "C", False, "1838 — SALICYLIC ACID", "Fast",
             "Fast: daylight close-up of two glass apothecary dishes side by side: golden-yellow salicin crystals from willow bark on the left and sharp white salicylic acid needles beside meadowsweet blossoms on the right. Nothing emissive, no face.",
             STYLE + "In bright window light on a laboratory bench, two shallow glass dishes hold pale yellow crystals and sharp white needle crystals beside a sprig of meadowsweet flowers." + FAST_TAIL,
             None),
        ],
    ),
    (
        3,
        "Part 03 — Felix Hoffmann's 10 August 1897 Notebook & Why Bayer Almost Shelved Aspirin — Midpoint Twist",
        [
            ("01_hoffmann_eichengrun_and_dreser_1897_elberfeld_lab_dispute", 99.5, 6.5, "A", False, "BOSS FEARED IT HURT THE HEART", "Quality",
             "Quality: readable faces (29-year-old Felix Hoffmann and pharmaceutical head Arthur Eichengrün on 10 August 1897 at Bayer in Elberfeld presenting pure acetylsalicylic acid to pharmacology chief Heinrich Dreser, who shakes his head in refusal).",
             STYLE + "Inside the 1897 Bayer laboratory in Elberfeld, young chemist Felix Hoffmann and Arthur Eichengrün hold out a glass jar of pure white acetylsalicylic acid crystals while bearded pharmacology chief Heinrich Dreser raises a hand in refusal." + QUAL_TAIL,
             {"kind": "WHO", "label": "Arthur Eichengrün (1867–1949) — German chemist · Heinrich Dreser (1860–1924) — German pharmacologist", "fact_card": "Boss feared it hurt the heart", "when_stamp": "1853 · 10 August 1897 · 21 August 1897 · 6 March 1899", "timeline_step": "3/5 · 10 Aug 1897 (Felix Hoffmann synthesises pure acetylsalicylic acid — Aspirin — at Bayer in Elberfeld)", "hold_s": 3.8}),
            ("02_hoffmann_10_aug_1897_acetylation_oh_to_ococh3_gastric_shield_chart", 106.0, 8.0, "E", False, "10 AUG 1897 ACETYLATION: SALICYLIC ACID (−OH BURNS STOMACH) → ACETYLSALICYLIC ACID (−OCOCH3 SHIELD)", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked molecular and gastric-irritation comparison chart from Hoffmann's 10 August 1897 notebook shows salicylic acid (exposed phenolic −OH group irritating stomach mucosa) vs acetylsalicylic acid (acetyl group −COCH3 shielding the stomach before releasing active salicylate in the bloodstream).",
             {"kind": "DATA", "label": "10 AUG 1897 ACETYLATION: SALICYLIC ACID (−OH) + ACETIC ANHYDRIDE → ACETYLSALICYLIC ACID (−OCOCH3)", "detail": "Inked molecular & gastric-irritation comparison chart on period paper from Hoffmann's 10 August 1897 notebook showing salicylic acid (exposed phenolic −OH group irritating stomach mucosa) vs acetylsalicylic acid (acetyl group −COCH3 shielding the stomach before releasing active salicylate in the bloodstream)", "scale": "swapping a single hydrogen atom for an acetyl group turned a corrosive crystal that burned the throat into a gentle tablet that passed safely through the stomach", "hold_s": 3.8}),
            ("03_eichengrun_1898_berlin_clinical_trial_doctors_confirming_pain_relief", 114.0, 6.5, "B", False, "6 MARCH 1899 — ASPIRIN", "Quality",
             "Quality: readable faces (Arthur Eichengrün in 1898 handing packets of acetylsalicylic acid powder to a Berlin physician who reports rapid fever and pain relief with zero stomach burn).",
             STYLE + "In an 1898 Berlin clinic, chemist Arthur Eichengrün watches a bearded physician examine a smiling rheumatism patient flexing his fingers comfortably beside a tray of white powder packets." + QUAL_TAIL,
             None),
            ("04_hoffmann_1897_lab_notebook_glass_reflux_flask_and_amber_bottles_pan", 120.5, 5.5, "C", False, "100% PURE CRYSTALS", "Fast",
             "Fast: daylight close-up of Felix Hoffmann's open 1897 laboratory notebook beside a glass reflux flask of white acetylsalicylic acid crystals and early amber glass apothecary bottles. Nothing emissive, no face.",
             STYLE + "In crisp daylight on a wooden chemical bench, a glass flask filled with pure white needle crystals sits beside an open leather-bound notebook and two amber glass bottles." + FAST_TAIL,
             None),
        ],
    ),
    (
        4,
        "Part 04 — How Does a Pill Know Where It Hurts? John Vane's 1971 Prostaglandin Breakthrough",
        [
            ("01_john_vane_23_june_1971_royal_college_of_surgeons_cox_enzyme_discovery", 126.0, 6.5, "A", False, "PLUGS THE PAIN ENZYME TUNNEL", "Quality",
             "Quality: readable face (44-year-old British pharmacologist John Vane on 23 June 1971 at the Royal College of Surgeons in London demonstrating his superfusion tissue bioassay apparatus that proved aspirin blocks prostaglandin synthesis).",
             STYLE + "Inside the Royal College of Surgeons laboratory in London in June 1971, British pharmacologist John Vane adjusts a vertical glass organ-bath cascade connected to a brass kymograph drum." + QUAL_TAIL,
             {"kind": "FACT", "label": "Plugs the pain enzyme tunnel", "when_stamp": "23 June 1971 · 1975 · 1982", "timeline_step": "4/5 · 23 Jun 1971 (John Vane discovers aspirin blocks prostaglandin synthesis via the COX enzyme)", "hold_s": 3.8}),
            ("02_vane_1971_and_roth_majerus_1975_cox_serine530_acetylation_lock_diagram", 132.5, 8.0, "E", False, "1971–1975 COX ENZYME LOCK: ASPIRIN ACETYLATES SERINE-530 TO BLOCK PROSTAGLANDINS BY >95%", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked enzyme-lock diagram from John Vane (1971) and Roth & Majerus (1975) shows arachidonic acid entering the cyclooxygenase (COX) enzyme channel to produce pain/fever prostaglandins and clotting thromboxane A2 vs acetylsalicylic acid permanently acetylating Serine-530 to block the channel by >95%.",
             {"kind": "DATA", "label": "1971 VANE & 1975 ROTH/MAJERUS: ASPIRIN ACETYLATES SERINE-530 IN COX CHANNEL (>95% BLOCKADE)", "detail": "Inked enzyme-lock diagram on period paper from John Vane (1971) and Roth & Majerus (1975) showing arachidonic acid entering the cyclooxygenase (COX) enzyme channel to produce pain/fever prostaglandins and clotting thromboxane A2 vs acetylsalicylic acid permanently acetylating Serine-530 to block the channel by >95%", "scale": "a single three-hundred-milligram aspirin tablet — weighing less than five grains of rice — floods your bloodstream with a quintillion molecules that silence pain factories from head to toe", "hold_s": 3.8}),
            ("03_mechanical_brass_lock_and_key_enzyme_tunnel_model_closeup", 140.5, 6.5, "B", False, "23 JUNE 1971 — PROSTAGLANDINS", "Fast",
             "Fast: daylight macro shot of a carved wooden-and-brass lock-and-key model of the COX enzyme tunnel where a small white acetyl plug slides into the channel and blocks a grooved fatty-acid rod from entering. Nothing emissive, no face.",
             STYLE + "In bright daylight on a demonstration table, a sculpted brass-and-wood enzyme tunnel model shows a small white cylindrical plug sliding into the channel to block a brass rod." + FAST_TAIL,
             None),
            ("04_explorer_inserting_acetyl_key_into_cox_enzyme_tunnel_gate", 147.0, 5.5, "B", True, None, "Quality",
             "Quality: Explorer beat 2 (locked character reference).",
             STYLE + "Standing beside a sculpted brass tunnel gate representing the COX enzyme, the Explorer slides a fitting white key into the keyhole inside the tunnel and turns it shut so dark spiky alarm spheres bounce harmlessly away." + EXP_TAIL,
             None),
        ],
    ),
    (
        5,
        "Part 05 — The Drug Once Feared to Hurt the Heart Now Saves Millions of Hearts — & the Ruby Laser That Built the Internet",
        [
            ("01_timeline_1763_1988_and_isis2_23_percent_heart_attack_drop_chart", 152.5, 8.5, "E", False, "1763–1988 TIMELINE · 8–10 DAY PLATELET BLOCKADE · 23% HEART-ATTACK MORTALITY DROP (ISIS-2)", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, the 5-date timeline completes: 25 Apr 1763 (Reverend Edward Stone reports curing 50 fever patients with dried white willow bark to the Royal Society) · 1828–1838 (Buchner, Leroux & Raffaele Piria isolate salicin and salicylic acid) · 10 Aug 1897 (Felix Hoffmann synthesises pure acetylsalicylic acid — Aspirin — at Bayer in Elberfeld) · 23 Jun 1971 (John Vane discovers aspirin blocks prostaglandin synthesis via the COX enzyme) · 1975–1988 (Roth & Majerus prove irreversible platelet COX-1 acetylation; ISIS-2 trial of 17,187 patients proves low-dose aspirin cuts heart-attack mortality by 23%).",
             {"kind": "DATA", "label": "1763–1988 TIMELINE & ISIS-2 TRIAL (17,187 PATIENTS: −23% HEART-ATTACK MORTALITY WITH LOW-DOSE ASPIRIN)", "detail": "Animated 5-date timeline (25 Apr 1763 → 1975–1988) alongside 8–10 day irreversible platelet thromboxane A2 blockade (75–81 mg dose) and the 1988 ISIS-2 trial of 17,187 patients showing a 23% drop in vascular mortality", "scale": "one tiny seventy-five-milligram aspirin tablet disables a blood platelet's clotting factory for its entire ten-day life — cutting heart-attack deaths by nearly a quarter", "fact_card": "Cuts heart-attack deaths 23%", "when_stamp": "1988 · 1763–1988", "timeline_step": "5/5 · 1975–1988 (Roth & Majerus prove irreversible platelet COX-1 acetylation; ISIS-2 trial of 17,187 patients proves low-dose aspirin cuts heart-attack mortality by 23%)", "hold_s": 3.8}),
            ("02_coronary_artery_platelet_model_and_low_dose_aspirin_tablet_comparison", 161.0, 5.5, "A", False, "23% DROP IN VASCULAR DEATHS", "Fast",
             "Fast: daylight cutaway anatomical model of a clear glass arterial tube where smooth red discs and pale platelets flow freely past a tiny white low-dose aspirin tablet on a medical desk. Nothing emissive, no face.",
             STYLE + "In crisp daylight on a medical demonstration desk, a clear glass tube model shows smooth red discs flowing freely beside a small white tablet in a brass holder." + FAST_TAIL,
             None),
            ("03_maiman_16_may_1960_pink_ruby_laser_and_kao_1966_glass_fibre_handoff", 166.5, 6.5, "C", False, "THE RUBY AND THE GLASS THREAD", "Quality",
             "Quality: readable faces (Theodore Maiman on 16 May 1960 at Hughes Research Laboratories in Malibu holding his fingertip-sized pink ruby crystal inside a coiled flashlamp, beside Charles Kao in 1966 in Harlow, England, inspecting an ultra-pure silica optical fibre — handoff to 042 Lasers & Fibre Optics).",
             STYLE + "Split period scene: on the left in a 1960 California optics lab, physicist Theodore Maiman holds up a miniature cylindrical housing containing a pink ruby crystal inside a helical quartz tube; on the right in 1966 in England, engineer Charles Kao examines a spool of hair-thin clear glass fibre." + QUAL_TAIL,
             {"kind": "WHEN", "label": "1917 · 16 MAY 1960 · 1966", "hold_s": 3.5}),
            ("04_table_three_callback", 173.0, 2.4, "C", False, None, "reuse",
             "Reuse: verified unused moving window [5.50s..7.90s] of P1:07_table_three_props_willow_bark_tin_amber_aspirin_bottle_kymograph_drum (callback, £0).",
             "Reuse P1:07_table_three_props_willow_bark_tin_amber_aspirin_bottle_kymograph_drum [5.50s..7.90s] (2.40s distinct non-overlapping tail window from 8.00s source clip).",
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
                row["reuse_of"] = "P1:07_table_three_props_willow_bark_tin_amber_aspirin_bottle_kymograph_drum"
                row["reuse_window_s"] = [5.5, 7.9]
                row["reuse_audit"] = {
                    "source_row": "P1:07_table_three_props_willow_bark_tin_amber_aspirin_bottle_kymograph_drum",
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
            "film": "041_Stone-Hoffmann-Vane-Aspirin-Painkillers",
            "part": p_idx,
            "title": p_title,
            "version": "v01",
            "timing_status": "pre_vo_script_clock (built from aspirin_script_master_v01.md; retimes onto Scribe STT once VO locks)",
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
        "film": "041_Stone-Hoffmann-Vane-Aspirin-Painkillers",
        "version": "v01",
        "date": "2026-10-18",
        "owner": "gemini (J0540)",
        "status": "PRE_VO_BOARDS_V01_NO_MINT",
        "generation_authorized": False,
        "script": "00_Brand/Channel-Setup/ideas/041_Stone-Hoffmann-Vane-Aspirin-Painkillers/aspirin_script_master_v01.md",
        "script_review_score": 91.9,
        "sources": "00_Brand/Channel-Setup/ideas/041_Stone-Hoffmann-Vane-Aspirin-Painkillers/SOURCES_v01.md",
        "credit_snapshot": {
            "flow_balance": 23740,
            "flow_floor": 0,
            "flow_read_at": "2026-10-15T21:42:22Z",
            "vertex_promo_gbp": 71.02,
            "vertex_usable_gbp": 70.02,
        },
        "totals": totals,
        "per_part": per_part_summary,
        "mint_order": "006 > 007 > 008 > 009 > 010 > 011 > 012 > 013 > 014 > 015 > 016 > 017 > 018 > 019 > 020 > 021 > 022 > 023 > 024 > 025 > 026 > 027 > 028 > 029 > 030 > 031 > 032 > 033 > 034 > 035 > 036 > 037 > 038 > 039 > 040 > 041. Nothing in 041 is generation_authorized.",
    }
    (EDIT / "PICTURE_PLAN_v01.json").write_text(json.dumps(plan, indent=2) + "\n")

    sl = [
        "# 041 Aspirin: The Bitter Tree Bark That Became the World's Pill — Shot list & plate boards v01 (pre-VO)",
        "",
        "Gemini, 18 Oct 2026, J0540. Built from `aspirin_script_master_v01.md` (`91.9 PASS`) and `SOURCES_v01.md`.",
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
        "# 041 price review v01 (pre-VO plate boards)",
        "",
        "Gemini, 18 Oct 2026, J0540. Boards only. **No mint. No spend. No merge.**",
        "Prepared from `aspirin_script_master_v01.md` (`91.9 PASS`) and `SOURCES_v01.md` so 041's full plate board rows, non-emissive Fast prompts, £0 code graphics, and Teach-on-Screen overlays are ready to re-time the moment long VO locks. Parked for Chief.",
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
        f"- **Quality ({totals['Quality']} rows):** readable faces (Felix Hoffmann, Reverend Edward Stone, Arthur Eichengrün, Heinrich Dreser, Raffaele Piria, Sir John Vane, Theodore Maiman, Charles Kao), 1897 Elberfeld Bayer laboratory scenes, 1898 Berlin clinical trial, 1971 Royal College of Surgeons bioassay lab, and the 2 Explorer beats.",
        f"- **Fast ({totals['Fast']} rows, non-emissive):** daylight prop and laboratory shots (white willow bark, meadowsweet flowers & crystal dish pan, 3-object callback bench, oven-dried willow bark in a baker's tin & brass scales, yellow salicin vs white salicylic acid needle crystals, Hoffmann's 1897 lab notebook & amber bottles, sculpted brass-and-wood COX enzyme tunnel model, coronary artery platelet flow model). Zero candles, flames, sparks, or glowing elements on Fast.",
        f"- **£0 code graphics ({totals['code_graphic']} rows):**",
        "  1. `P1:04_stone_1763_50_patients_hoffmann_1897_asa_and_40000_tonnes_annual_chart` — Stone's 1763 willow-bark trial (50 patients, 20 grains / 1.3 g), Hoffmann's 10 August 1897 acetylation, and ~40,000 tonnes (~100 billion tablets/yr) global consumption (`SCALE: humans swallow roughly forty thousand tonnes of aspirin every single year — more than a hundred billion little white tablets, enough to stretch to the Moon and back`)",
        "  2. `P1:06_seventy_four_year_mechanism_mystery_bar_1897_hoffmann_to_1971_vane` — 74-year mechanism gap from 10 August 1897 synthesis at Bayer to 23 June 1971 John Vane COX/prostaglandin discovery (`SCALE: for nearly three-quarters of a century, doctors prescribed the world's most popular medicine completely blind to what it did inside a human cell`)",
        "  3. `P2:02_stone_1763_1lb_bark_20_grains_to_1876_4_6g_corrosive_salicylic_acid_chart` — 1 lb dried white willow bark (Stone 1763) → salicin (1828) → salicylic acid (Piria 1838; 4–6 g/day corrosive arthritis dose in 1876) (`SCALE: to calm swollen joints in the eighteen seventies, arthritis patients had to swallow up to six grams of raw salicylic acid every single day — a dose so caustic it stripped the lining of their stomachs`)",
        "  4. `P3:02_hoffmann_10_aug_1897_acetylation_oh_to_ococh3_gastric_shield_chart` — salicylic acid (exposed phenolic −OH irritating stomach mucosa) vs Hoffmann's 10 August 1897 acetylsalicylic acid (−OCOCH3 gastric shield) (`SCALE: swapping a single hydrogen atom for an acetyl group turned a corrosive crystal that burned the throat into a gentle tablet that passed safely through the stomach`)",
        "  5. `P4:02_vane_1971_and_roth_majerus_1975_cox_serine530_acetylation_lock_diagram` — Vane (1971) & Roth/Majerus (1975) Serine-530 acetylation blocking the cyclooxygenase (COX) enzyme channel by >95% (`SCALE: a single three-hundred-milligram aspirin tablet — weighing less than five grains of rice — floods your bloodstream with a quintillion molecules that silence pain factories from head to toe`)",
        "  6. `P5:01_timeline_1763_1988_and_isis2_23_percent_heart_attack_drop_chart` — completed 5-date timeline (1763 → 1988) + 8–10 day irreversible platelet thromboxane blockade and 23% vascular mortality reduction in the 17,187-patient ISIS-2 trial (`SCALE: one tiny seventy-five-milligram aspirin tablet disables a blood platelet's clotting factory for its entire ten-day life — cutting heart-attack deaths by nearly a quarter`)",
        f"- **£0 verified reuse ({totals['reuse']} row):** `P5:04_table_three_callback` uses the 2.40 s unused moving tail `[5.50s..7.90s]` of `P1:07_table_three_props_willow_bark_tin_amber_aspirin_bottle_kymograph_drum`.",
        "",
        "## Mint order",
        "",
        "006 > 007 > 008 > 009 > 010 > 011 > 012 > 013 > 014 > 015 > 016 > 017 > 018 > 019 > 020 > 021 > 022 > 023 > 024 > 025 > 026 > 027 > 028 > 029 > 030 > 031 > 032 > 033 > 034 > 035 > 036 > 037 > 038 > 039 > 040 > 041. `generation_authorized` is `false` on every row.",
    ])
    (EDIT / "PRICE_REVIEW_v01.md").write_text("\n".join(pr_lines) + "\n")
    print(f"041 v01 boards written: {totals['rows']} rows, Flow expected={totals['flow_credits_expected']}")


if __name__ == "__main__":
    main()
