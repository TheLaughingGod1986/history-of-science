#!/usr/bin/env python3
"""HOS 036 (Scurvy & Vitamins: The 1747 Ship Trial That Saved Two Million Men) pre-VO plate boards v01. J0509. No mint, no spend.

Built from 00_Brand/Channel-Setup/ideas/036_Lind-Eijkman-Scurvy-Vitamins/vitamins_script_master_v01.md (92.9 PASS)
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
        "Part 01 — The Warship in the English Channel and the Two Oranges",
        [
            ("01_lind_1747_hms_salisbury_six_pairs_two_oranges_and_lemon", 0.0, 5.5, "A", False, "TWO ORANGES AND A LEMON", "Quality",
             "Quality: Short frame 0 / answer image (0:03) + in the forward sickbay of the 50-gun warship HMS Salisbury pitching in the English Channel on 20 May 1747, 30-year-old Scottish surgeon James Lind hands two fresh oranges and one lemon to a pair of scurvy-crippled sailors in canvas hammocks while five other pairs receive cider, vinegar, seawater, vitriol, or spice paste.",
             STYLE + "Inside the timber sickbay of HMS Salisbury in the English Channel on 20 May 1747, thirty-year-old Scottish surgeon James Lind in a blue naval coat hands two bright oranges and a yellow lemon to two sailors resting in canvas hammocks while five other pairs of sailors wait along the bulkhead." + QUAL_TAIL,
             {"kind": "WHEN", "label": "HMS SALISBURY, 20 MAY 1747", "timeline_step": "1/5 · 20 May 1747 (James Lind's 12-sailor 6-pair controlled trial cures scurvy in 6 days with oranges and lemons)", "hold_s": 3.5}),
            ("02_hms_salisbury_trial_navy_lime_vat_and_eijkman_java_chickens_split", 5.5, 6.0, "B", False, "TRIAL, LIMES, BROWN RICE", "Quality",
             "Quality: complex three-part split composition (James Lind's six-pair trial table aboard HMS Salisbury on 20 May 1947 on the left; a Royal Navy copper vat swapping Mediterranean lemons for West Indian limes in the centre; Christiaan Eijkman's Java courtyard in 1890 where paralysed chickens stand up after switching from white rice to brown rice on the right).",
             STYLE + "Three-panel period composition: on the left, two fresh oranges and a lemon beside six glass medicine bottles on a ship's oak table; in the centre, a polished copper vat and crates of green West Indian limes; on the right, lively brown chickens pecking unpolished brown rice in a sunlit Javanese courtyard." + QUAL_TAIL,
             None),
            ("03_1740s_warship_salt_beef_hardtack_and_unravelling_collagen_rope", 11.5, 6.0, "C", False, "COLLAGEN UNRAVELLING", "Fast",
             "Fast: daylight below-deck view of wooden barrels of salt beef and hardtack ship's biscuit beside a fraying three-strand collagen rope model on an oak table. Nothing emissive, no face.",
             STYLE + "In soft daylight from a deck grating aboard a wooden sailing ship, open barrels of salted beef and ship's biscuits sit beside a thick three-strand rope whose fibres are unravelling on an oak table." + FAST_TAIL,
             {"kind": "WHEN", "label": "1740–1747", "hold_s": 3.5}),
            ("04_anson_1300_of_1955_deaths_and_lind_6_pair_trial_chart", 17.5, 8.0, "E", False, "ANSON VOYAGE (~1,300 SCURVY VS 4 BATTLE DEATHS) · LIND'S 6-PAIR TRIAL (2 ORANGES + 1 LEMON)", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked clinical-trial and mortality chart compares Commodore George Anson's 1740–1744 circumnavigation (1,955 men embarked; ~1,300 died of disease/scurvy vs only 4 killed by enemy action) against James Lind's 20 May 1747 HMS Salisbury 12-man 6-pair controlled trial (cider, vitriol, vinegar, half-pint seawater, garlic-mustard paste, vs 2 oranges + 1 lemon recovering in 6 days).",
             {"kind": "DATA", "label": "ANSON 1740–1744 (~1,300 SCURVY VS 4 BATTLE DEATHS) & LIND'S 20 MAY 1747 6-PAIR TRIAL", "detail": "Inked clinical-trial & mortality chart on period paper comparing George Anson's 1740–1744 voyage (1,955 men embarked; ~1,300 died of scurvy/disease vs 4 in battle) against James Lind's 20 May 1747 HMS Salisbury 12-man 6-pair trial (2 oranges + 1 lemon cured in 6 days)", "scale": "on Anson's four-year voyage around the world, scurvy killed more than two hundred and fifty sailors for every single man killed by enemy cannon fire", "who_card": "James Lind (1716–1794) — Scottish Royal Navy surgeon · Christiaan Eijkman (1858–1930) — Dutch physician and pathologist · Casimir Funk (1884–1967) — Polish biochemist", "when_stamp": "20 May 1747 · 1890 · 1912", "hold_s": 3.8}),
            ("05_six_remedy_vessels_cider_vitriol_vinegar_seawater_paste_citrus_pan", 25.5, 5.5, "A", False, "SIX DAILY REMEDIES", "Fast",
             "Fast: daylight macro pan across the six remedies from James Lind's 1747 trial arranged on a wooden surgeon's bench between code graphics so two full-frame graphics never run back to back: a jug of cider, a dropper vial of vitriol, a cruet of vinegar, a pewter cup of seawater, a mortar of garlic-mustard paste, and two fresh oranges with one lemon. Nothing emissive, no face.",
             STYLE + "In crisp daylight on a ship surgeon's wooden bench, the camera pans across six remedies in a neat row: an earthenware cider jug, a glass dropper bottle, a vinegar cruet, a pewter cup of seawater, a spice mortar, and two fresh oranges beside a bright yellow lemon." + FAST_TAIL,
             None),
            ("06_1955_crew_bar_and_130mg_citrus_vs_10mg_vitamin_c_threshold_card", 31.0, 8.0, "E", False, "10 MILLIGRAMS A DAY", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period parchment, an inked bar chart compares 1,955 total crew on Anson's 1740–1744 voyage against ~1,300 scurvy/disease deaths and 4 battle deaths, alongside ~130 mg/day of Vitamin C in two oranges and one lemon vs the 10 mg/day minimum threshold (the weight of a single grain of rice) needed to prevent scurvy.",
             {"kind": "DATA", "label": "1,955 CREW (~1,300 SCURVY VS 4 BATTLE) & ~130 MG CITRUS VS 10 MG/DAY VITAMIN C MINIMUM", "detail": "Inked bar chart comparing 1,955 total crew vs ~1,300 disease/scurvy deaths and 4 battle deaths (1740–1744), contrasted with ~130 mg/day of Vitamin C in 2 oranges + 1 lemon vs the 10 mg/day minimum needed to prevent scurvy", "scale": "ten milligrams of vitamin C a day — the weight of a single grain of rice — is all it takes to keep your body's collagen from falling apart", "hold_s": 3.8}),
            ("07_table_three_props_oranges_lemon_brown_rice_bowl_paprika_crystals", 39.0, 5.5, "C", False, "1747 TO 1932", "Fast",
             "Fast: daylight prop table (callback source for Part 05: two fresh oranges and a halved lemon on a pewter plate, a bamboo bowl of unpolished brown rice, and a glass dish of crystalline ascorbic acid beside red Hungarian paprika peppers). Nothing emissive.",
             STYLE + "On an oak workbench in soft window light sit three objects side by side: two oranges and a halved lemon on a pewter plate, a woven bowl of unpolished brown rice, and a glass dish of white vitamin C crystals beside two red paprika peppers." + FAST_TAIL,
             None),
            ("08_explorer_orange_juice_drop_clasping_three_strand_collagen_rope", 62.0, 5.5, "A", True, None, "Quality",
             "Quality: Explorer beat 1 (locked character reference, after 1:00).",
             STYLE + "Holding a thick three-stranded rope of collagen fibres that begins fraying apart, the Explorer squeezes a bright golden drop of orange juice onto the rope: brass-gold rings clasp the three strands tightly back together so the rope holds firm." + EXP_TAIL,
             None),
            ("09_hms_salisbury_deck_26_may_1747_cured_sailor_at_ship_wheel", 67.5, 5.5, "B", False, "CURED IN SIX DAYS", "Quality",
             "Quality: readable faces (on the sunlit main deck of HMS Salisbury on 26 May 1747, the two citrus-fed sailors stand upright and healthy — one gripping the ship's wooden wheel while James Lind smiles beside him).",
             STYLE + "On the sunlit wooden deck of HMS Salisbury in May 1747, a recovered sailor grips the ship's helm wheel with strong hands while surgeon James Lind records notes in his leather journal beside him." + QUAL_TAIL,
             None),
        ],
    ),
    (
        2,
        "Part 02 — Why Humans Can't Make Vitamin C & the World's First Clinical Trial",
        [
            ("01_lind_20_may_1747_hms_salisbury_twelve_sailors_six_pairs", 73.0, 6.5, "A", False, "FIRST CONTROLLED CLINICAL TRIAL", "Quality",
             "Quality: readable faces (aboard HMS Salisbury on 20 May 1747, 30-year-old Scottish surgeon James Lind lines up 12 scurvy-stricken sailors in six matched pairs of hammocks and distributes the six test remedies).",
             STYLE + "Aboard HMS Salisbury on 20 May 1747, Scottish naval surgeon James Lind walks between six matched pairs of sailors in canvas hammocks, handing two oranges and a lemon to the sixth pair." + QUAL_TAIL,
             {"kind": "FACT", "label": "First controlled clinical trial", "when_stamp": "1741 · 20 May 1747 · 1753", "hold_s": 3.8}),
            ("02_lind_1747_six_pair_clinical_trial_table_diagram", 79.5, 8.0, "E", False, "LIND'S 20 MAY 1747 HMS SALISBURY 6-PAIR CONTROLLED TRIAL (2/2 CURED IN 6 DAYS ON CITRUS)", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked six-row clinical trial table shows James Lind's 20 May 1747 HMS Salisbury experiment (12 sailors, 6 pairs, identical diet, 6 treatments over 6 days: 1 quart cider, 25 drops elixir of vitriol, 2 spoonfuls vinegar, half-pint seawater, garlic-mustard paste, vs 2 oranges + 1 lemon = 2/2 recovered in 6 days).",
             {"kind": "DATA", "label": "LIND'S 20 MAY 1747 6-PAIR CLINICAL TRIAL (CIDER, VITRIOL, VINEGAR, SEAWATER, PASTE VS CITRUS)", "detail": "Inked six-row clinical trial table on period paper showing James Lind's 20 May 1747 HMS Salisbury experiment (12 sailors, 6 pairs, identical diet, 6 treatments over 6 days: cider, vitriol, vinegar, half-pint seawater, garlic-mustard paste, vs 2 oranges + 1 lemon = 2/2 recovered in 6 days)", "scale": "two oranges and a lemon held about 130 milligrams of vitamin C a day — thirteen times the ten-milligram daily threshold needed to restart collagen synthesis within forty-eight hours", "hold_s": 3.8}),
            ("03_lind_1753_treatise_of_the_scurvy_and_halved_lemon_closeup", 87.5, 6.5, "B", False, "20 MAY 1747 — SIX PAIRS", "Fast",
             "Fast: daylight close-up of James Lind's leather-bound 1753 book A Treatise of the Scurvy lying open on a mahogany naval desk beside two oranges, a halved lemon on a pewter plate, and a brass compass. Nothing emissive, no face.",
             STYLE + "In soft daylight on a mahogany naval cabin desk, an open leather-bound treatise rests beside two fresh oranges, a halved lemon on a pewter plate, and a brass pocket compass." + FAST_TAIL,
             None),
            ("04_collagen_triple_helix_braided_rope_cross_link_model", 94.0, 5.5, "C", False, "COLLAGEN TRIPLE HELIX", "Fast",
             "Fast: daylight anatomical model of a triple-stranded collagen protein cable clasped by golden vitamin-C cross-link rings on a wooden workbench. Nothing emissive, no face.",
             STYLE + "In crisp daylight on a laboratory bench, a detailed three-dimensional model of a three-stranded collagen helix is held tightly together by polished brass cross-link rings." + FAST_TAIL,
             None),
        ],
    ),
    (
        3,
        "Part 03 — The Boiled Juice, the 'Limey' Swap & How Germ Theory Blinded Medicine — Midpoint Twist",
        [
            ("01_blane_1795_haslar_hospital_lemons_and_1860s_west_indian_lime_swap", 99.5, 6.5, "A", False, "LIMES HAD HALF THE VITAMIN C", "Quality",
             "Quality: readable faces (Scottish physician Sir Gilbert Blane in 1795 inspecting crates of fresh Mediterranean lemons outside Haslar Naval Hospital, contrasted with 1860s Admiralty clerks pumping West Indian lime juice through copper pipes).",
             STYLE + "Split period scene: on the left in 1795, Scottish physician Gilbert Blane in a powdered wig and dark coat inspects crates of bright yellow Mediterranean lemons at Haslar Naval Hospital; on the right in the 1860s, dockyard workers pump green West Indian lime juice through long copper pipes into naval barrels." + QUAL_TAIL,
             {"kind": "WHO", "label": "Gilbert Blane (1749–1834) — Scottish physician", "fact_card": "Limes had half the vitamin C", "when_stamp": "1795 · 1860s · 1912", "timeline_step": "2/5 · 1795 (Gilbert Blane's Royal Navy lemon-juice mandate cuts Haslar scurvy admissions from 1,457 to 2)", "hold_s": 3.8}),
            ("02_mediterranean_lemon_53mg_vs_west_indian_lime_29mg_and_haslar_chart", 106.0, 8.0, "E", False, "LEMONS (53 MG) VS LIMES (29 MG) VS BOILED ROB (~0 MG) · HASLAR SCURVY 1,457 (1780) → 2 (1806)", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked comparison bar shows raw Mediterranean lemon juice (~53 mg Vitamin C / 100 g) vs West Indian lime juice (~29 mg / 100 g before copper oxidation) vs Lind's boiled 'rob' syrup (~0–5 mg / 100 g after prolonged boiling), alongside Haslar Naval Hospital scurvy admissions dropping from 1,457 in 1780 to 2 in 1806 after Blane's 1795 lemon mandate.",
             {"kind": "DATA", "label": "LEMON (53 MG/100G) VS LIME (29 MG/100G) VS BOILED ROB (~0 MG) & HASLAR 1,457 → 2", "detail": "Inked comparison bar on period paper showing raw Mediterranean lemon juice (~53 mg Vitamin C / 100 g) vs West Indian lime juice (~29 mg / 100 g before copper oxidation) vs Lind's boiled 'rob' syrup (~0–5 mg / 100 g), alongside Haslar Naval Hospital scurvy admissions dropping from 1,457 in 1780 to 2 in 1806", "scale": "swapping Mediterranean lemons for copper-pumped West Indian limes cut the anti-scurvy power of a sailor's daily ration by more than half", "hold_s": 3.8}),
            ("03_portsmouth_1860s_copper_pipes_and_lime_juice_casks_closeup", 114.0, 6.5, "B", False, "THE 1860s LIME SWAP", "Fast",
             "Fast: daylight dockyard view of wooden casks, green West Indian limes in a crate, and long copper transfer pipes filling glass naval ration bottles. Nothing emissive, no face.",
             STYLE + "In bright daylight inside a Victorian naval victualling yard, crates of green limes sit beside wooden casks connected by long copper pipes to rows of glass ration bottles." + FAST_TAIL,
             None),
            ("04_scott_1912_antarctic_sledge_and_man_hauling_provisions", 120.5, 5.5, "C", False, "ANTARCTICA, 1912", "Quality",
             "Quality: explorers in windproof woollens hauling a wooden supply sledge across the white Antarctic ice shelf in 1912.",
             STYLE + "Across a windswept white Antarctic ice plain in 1912, four polar explorers in canvas parkas haul a loaded wooden sledge through blowing snow." + QUAL_TAIL,
             None),
        ],
    ),
    (
        4,
        "Part 04 — Christiaan Eijkman's Beriberi Chickens & Casimir Funk's 'Vitamines'",
        [
            ("01_eijkman_1890_java_courtyard_chickens_and_hopkins_funk_1912", 126.0, 6.5, "A", False, "A STINGY COOK CURED THE CHICKENS", "Quality",
             "Quality: readable faces (Dutch military doctor Christiaan Eijkman in Batavia, Java, in November 1890 watching paralysed chickens stand up and walk after switching from white rice to unpolished brown rice, alongside British biochemist Frederick Gowland Hopkins and Polish biochemist Casimir Funk in London in 1912).",
             STYLE + "Split period scene: on the left in a sunlit Java courtyard in November 1890, Dutch physician Christiaan Eijkman in a white tropical coat watches brown chickens stand up and peck unpolished brown rice from a bamboo tray; on the right in London in 1912, biochemists Frederick Gowland Hopkins and Casimir Funk hold up a glass tube of rice-bran crystals." + QUAL_TAIL,
             {"kind": "WHO", "label": "Frederick Gowland Hopkins (1861–1947) — British biochemist", "fact_card": "A stingy cook cured the chickens", "when_stamp": "17 June 1890 · 27 November 1890 · 1901 · 1912 · 1929", "timeline_step": "3/5 · Jun–Nov 1890 (Christiaan Eijkman's Java chickens recover on brown rice) & 4/5 · 1912 (Casimir Funk coins 'vitamine' & Hopkins proves accessory food factors)", "hold_s": 3.8}),
            ("02_eijkman_vorderman_1895_java_prison_survey_300x_beriberi_chart", 132.5, 8.0, "E", False, "JAVA PRISONS (101 PRISONS, ~280,000 INMATES): WHITE RICE 278/10,000 VS BROWN RICE 0.9/10,000 (300×)", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked epidemiological chart from Eijkman and Vorderman's 1895–1896 Java prison survey (~280,000 prisoners across 101 prisons) compares prisons feeding polished white rice (~278 beriberi cases per 10,000 inmates, 1 in 36) against prisons feeding unpolished brown rice (~0.9 per 10,000, 1 in 10,000 — a 300-fold difference from the rice bran skin alone).",
             {"kind": "DATA", "label": "JAVA PRISON SURVEY (~280,000 INMATES): WHITE RICE (278/10,000) VS BROWN RICE (0.9/10,000 = 300×)", "detail": "Inked epidemiological chart on period paper from Eijkman & Vorderman's 1895–1896 Java prison survey (~280,000 prisoners across 101 prisons): polished white rice (~278 beriberi cases per 10,000 inmates) vs unpolished brown rice (~0.9 per 10,000) — a 300-fold difference", "scale": "stripping the paper-thin silver bran skin off white rice raised a prisoner's risk of beriberi paralysis three hundred times over", "hold_s": 3.8}),
            ("03_funk_1912_lister_institute_rice_bran_vitamin_b1_isolation", 140.5, 6.5, "B", False, "1912 — FUNK COINS 'VITAMINE'", "Quality",
             "Quality: readable face (28-year-old Polish biochemist Casimir Funk at the Lister Institute in London in June 1912 holding a glass crystallisation tube of rice-bran thiamine crystals beside his notebook).",
             STYLE + "Inside the Lister Institute laboratory in London in June 1912, young biochemist Casimir Funk in a white coat holds a glass tube of fine crystals extracted from brown rice bran up to the window light." + QUAL_TAIL,
             None),
            ("04_explorer_peeling_silver_bran_wrapper_off_brown_rice_grain", 147.0, 5.5, "B", True, None, "Quality",
             "Quality: Explorer beat 2 (locked character reference).",
             STYLE + "Examining a large brown grain of rice with its silver bran coat intact beside a polished white grain, the Explorer gently peels back the paper-thin silver skin of the brown grain to reveal golden vitamin crystals tucked inside the wrapper." + EXP_TAIL,
             None),
        ],
    ),
    (
        5,
        "Part 05 — Hungarian Paprika, Why Mega-Doses Wash Away & the Coldest Room in the Universe",
        [
            ("01_timeline_1747_1932_and_szent_gyorgyi_paprika_200mg_saturation_chart", 152.5, 8.5, "E", False, "1747–1932 TIMELINE · PAPRIKA (200 MG/100G = 4× LEMON) · 200 MG/DAY SATURATION", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, the 5-date timeline completes: 20 May 1747 (James Lind's 6-pair trial on HMS Salisbury) · 1795 (Gilbert Blane's Royal Navy lemon order) · Jun–Nov 1890 (Christiaan Eijkman's Java brown-rice chickens) · 1912 (Casimir Funk coins 'vitamine' & Hopkins proves accessory factors) · 1932 (Albert Szent-Györgyi & Charles Glen King isolate ascorbic acid / Vitamin C from Hungarian paprika), alongside paprika (~200 mg Vitamin C / 100 g, 4× lemons) and human plasma saturation at ~200 mg/day.",
             {"kind": "DATA", "label": "1747–1932 TIMELINE & HUNGARIAN PAPRIKA (200 MG/100G = 4× LEMON) · ~200 MG/DAY SATURATION", "detail": "Animated 5-date timeline (1747 → 1932) alongside Hungarian paprika (~200 mg Vitamin C / 100 g, 4× citrus) and human plasma/tissue saturation at ~200 mg/day flushing excess water-soluble mega-doses", "scale": "a single medium orange (~70 mg of Vitamin C) holds seven times the ten-milligram daily dose that would have saved two million sailors across the Age of Sail", "who_card": "Albert Szent-Györgyi (1893–1986) — Hungarian biochemist", "fact_card": "Paprika has 4× lemon's vitamin C", "when_stamp": "1932 · 1937", "timeline_step": "5/5 · 1932 (Albert Szent-Györgyi & Charles Glen King identify ascorbic acid / Vitamin C and extract pounds from Hungarian paprika)", "hold_s": 3.8}),
            ("02_szent_gyorgyi_1932_szeged_red_paprika_and_ascorbic_acid_crystals", 161.0, 5.5, "A", False, "SZEGED PAPRIKA, 1932", "Quality",
             "Quality: readable face (Hungarian biochemist Albert Szent-Györgyi in Szeged in October 1932 smiling as he holds a plate of bright red Hungarian paprika peppers beside a large glass jar of pure white ascorbic acid crystals).",
             STYLE + "In a 1932 laboratory in Szeged, Hungary, biochemist Albert Szent-Györgyi smiles while holding a dinner plate of bright red paprika peppers beside a glass jar filled with pure white ascorbic acid crystals." + QUAL_TAIL,
             None),
            ("03_kamerlingh_onnes_1911_leiden_liquid_helium_and_mercury_zero_ohms_handoff", 166.5, 6.5, "C", False, "ZERO RESISTANCE AT 4.2 KELVIN", "Quality",
             "Quality: readable faces (Dutch physicist Heike Kamerlingh Onnes and Gilles Holst in the Cryogenic Laboratory at Leiden University on 10 July 1908 and 8 April 1911 peering into a frost-covered glass Dewar of liquid helium at 4.20 Kelvin as frozen mercury's resistance drops to zero — handoff to 037 Superconductivity).",
             STYLE + "Inside the Leiden University cryogenic laboratory on 8 April 1911, bearded Dutch physicist Heike Kamerlingh Onnes and young assistant Gilles Holst inspect a frost-rimmed silvered glass Dewar flask of liquid helium beside a brass mirror galvanometer resting at zero." + QUAL_TAIL,
             {"kind": "WHEN", "label": "10 JULY 1908 · 8 APRIL 1911", "hold_s": 3.5}),
            ("04_table_three_callback", 173.0, 2.4, "C", False, None, "reuse",
             "Reuse: verified unused moving window [5.50s..7.90s] of P1:07_table_three_props_oranges_lemon_brown_rice_bowl_paprika_crystals (callback, £0).",
             "Reuse P1:07_table_three_props_oranges_lemon_brown_rice_bowl_paprika_crystals [5.50s..7.90s] (2.40s distinct non-overlapping tail window from 8.00s source clip).",
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
                row["reuse_of"] = "P1:07_table_three_props_oranges_lemon_brown_rice_bowl_paprika_crystals"
                row["reuse_window_s"] = [5.5, 7.9]
                row["reuse_audit"] = {
                    "source_row": "P1:07_table_three_props_oranges_lemon_brown_rice_bowl_paprika_crystals",
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
            "film": "036_Lind-Eijkman-Scurvy-Vitamins",
            "part": p_idx,
            "title": p_title,
            "version": "v01",
            "timing_status": "pre_vo_script_clock (built from vitamins_script_master_v01.md; retimes onto Scribe STT once VO locks)",
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
        "film": "036_Lind-Eijkman-Scurvy-Vitamins",
        "version": "v01",
        "date": "2026-10-18",
        "owner": "gemini (J0509)",
        "status": "PRE_VO_BOARDS_V01_NO_MINT",
        "generation_authorized": False,
        "script": "00_Brand/Channel-Setup/ideas/036_Lind-Eijkman-Scurvy-Vitamins/vitamins_script_master_v01.md",
        "sources": "00_Brand/Channel-Setup/ideas/036_Lind-Eijkman-Scurvy-Vitamins/SOURCES_v01.md",
        "credit_snapshot": {
            "flow_balance": 23740,
            "flow_floor": 0,
            "flow_read_at": "2026-10-15T21:42:22Z",
            "vertex_promo_gbp": 71.02,
            "vertex_usable_gbp": 70.02,
        },
        "totals": totals,
        "per_part": per_part_summary,
        "mint_order": "006 > 007 > 008 > 009 > 010 > 011 > 012 > 013 > 014 > 015 > 016 > 017 > 018 > 019 > 020 > 021 > 022 > 023 > 024 > 025 > 026 > 027 > 028 > 029 > 030 > 031 > 032 > 033 > 034 > 035 > 036. Nothing in 036 is generation_authorized.",
    }
    (EDIT / "PICTURE_PLAN_v01.json").write_text(json.dumps(plan, indent=2) + "\n")

    sl = [
        "# 036 Scurvy & Vitamins: The 1747 Ship Trial That Saved Two Million Men — Shot list & plate boards v01 (pre-VO)",
        "",
        "Gemini, 18 Oct 2026, J0509. Built from `vitamins_script_master_v01.md` (92.9 PASS) and `SOURCES_v01.md`.",
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
        "# 036 price review v01 (pre-VO plate boards)",
        "",
        "Gemini, 18 Oct 2026, J0509. Boards only. **No mint. No spend. No merge.**",
        "Prepared from `vitamins_script_master_v01.md` (92.9 PASS) and `SOURCES_v01.md` so 036's full plate board rows, non-emissive Fast prompts, £0 code graphics, and Teach-on-Screen overlays are ready to re-time the moment long VO locks. Parked for Chief.",
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
        f"- **Quality ({totals['Quality']} rows):** readable faces (James Lind, Gilbert Blane, Christiaan Eijkman, Frederick Gowland Hopkins, Casimir Funk, Albert Szent-Györgyi, Heike Kamerlingh Onnes, Gilles Holst), polar expedition scene, and the 2 Explorer beats.",
        f"- **Fast ({totals['Fast']} rows, non-emissive):** daylight prop and laboratory shots (1740s salt beef & hardtack casks beside fraying collagen rope model, six HMS Salisbury remedies pan, 3-object callback bench, Lind's 1753 treatise & halved lemon on mahogany naval desk, braided collagen triple-helix model, 1860s Portsmouth copper pipes & West Indian lime casks). Zero candles, flames, sparks, or glowing elements on Fast.",
        f"- **£0 code graphics ({totals['code_graphic']} rows):**",
        "  1. `P1:04_anson_1300_of_1955_deaths_and_lind_6_pair_trial_chart` — George Anson's 1740–1744 circumnavigation (~1,300 scurvy/disease deaths vs 4 battle deaths out of 1,955 men) + James Lind's 20 May 1747 HMS Salisbury 12-man 6-pair controlled trial (`SCALE: on Anson's four-year voyage around the world, scurvy killed more than two hundred and fifty sailors for every single man killed by enemy cannon fire`)",
        "  2. `P1:06_1955_crew_bar_and_130mg_citrus_vs_10mg_vitamin_c_threshold_card` — 1,955 crew bar (~1,300 scurvy vs 4 battle) + ~130 mg/day Vitamin C in 2 oranges + 1 lemon vs 10 mg/day minimum threshold (`SCALE: ten milligrams of vitamin C a day — the weight of a single grain of rice — is all it takes to keep your body's collagen from falling apart`)",
        "  3. `P2:02_lind_1747_six_pair_clinical_trial_table_diagram` — James Lind's 20 May 1747 six-row clinical trial table (cider, vitriol, vinegar, half-pint seawater, garlic-mustard paste, vs 2 oranges + 1 lemon = 2/2 cured in 6 days) (`SCALE: two oranges and a lemon held about 130 milligrams of vitamin C a day — thirteen times the ten-milligram daily threshold needed to restart collagen synthesis within forty-eight hours`)",
        "  4. `P3:02_mediterranean_lemon_53mg_vs_west_indian_lime_29mg_and_haslar_chart` — raw Mediterranean lemon juice (~53 mg/100 g) vs West Indian lime (~29 mg/100 g) vs boiled 'rob' (~0–5 mg/100 g) + Haslar Naval Hospital scurvy admissions dropping from 1,457 (1780) to 2 (1806) (`SCALE: swapping Mediterranean lemons for copper-pumped West Indian limes cut the anti-scurvy power of a sailor's daily ration by more than half`)",
        "  5. `P4:02_eijkman_vorderman_1895_java_prison_survey_300x_beriberi_chart` — Eijkman & Vorderman's 1895–1896 Java prison survey (~280,000 prisoners across 101 prisons): polished white rice (~278/10,000) vs unpolished brown rice (~0.9/10,000 = 300× difference) (`SCALE: stripping the paper-thin silver bran skin off white rice raised a prisoner's risk of beriberi paralysis three hundred times over`)",
        "  6. `P5:01_timeline_1747_1932_and_szent_gyorgyi_paprika_200mg_saturation_chart` — completed 5-date timeline (1747 → 1932) + Hungarian paprika (~200 mg Vitamin C / 100 g = 4× lemon) + human plasma saturation at ~200 mg/day (`SCALE: a single medium orange (~70 mg of Vitamin C) holds seven times the ten-milligram daily dose that would have saved two million sailors across the Age of Sail`)",
        f"- **£0 verified reuse ({totals['reuse']} row):** `P5:04_table_three_callback` uses the 2.40 s unused moving tail `[5.50s..7.90s]` of `P1:07_table_three_props_oranges_lemon_brown_rice_bowl_paprika_crystals`.",
        "",
        "## Mint order",
        "",
        "006 > 007 > 008 > 009 > 010 > 011 > 012 > 013 > 014 > 015 > 016 > 017 > 018 > 019 > 020 > 021 > 022 > 023 > 024 > 025 > 026 > 027 > 028 > 029 > 030 > 031 > 032 > 033 > 034 > 035 > 036. `generation_authorized` is `false` on every row.",
    ])
    (EDIT / "PRICE_REVIEW_v01.md").write_text("\n".join(pr_lines) + "\n")
    print(f"036 v01 boards written: {totals['rows']} rows, Flow expected={totals['flow_credits_expected']}")


if __name__ == "__main__":
    main()
