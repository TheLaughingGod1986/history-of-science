#!/usr/bin/env python3
"""HOS 048 (Malaria & Artemisinin: The 340 AD Scroll That Saved Millions) pre-VO plate boards v01. J0570. No mint, no spend.

Built from 00_Brand/Channel-Setup/ideas/048_Perkin-Ross-TuYouyou-Malaria-Quinine-Artemisinin/malaria_script_master_v01.md (91.6 PASS)
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
        "Part 01 — The Failed Malaria Cure That Dyed the World Purple and the 340 AD Scroll That Saved Millions",
        [
            ("01_perkin_easter_1856_purple_mauveine_silk_and_tu_youyou_4_oct_1971_cold_ether_scroll", 0.0, 5.5, "A", False, "PURPLE DYE AND ARTEMISININ", "Quality",
             "Quality: Short frame 0 / answer image (0:03) + split composition: on the left, in an East London attic lab during Easter 1856, 18-year-old William Henry Perkin dips a silk ribbon into a coal-tar flask expecting clear malaria medicine and pulls it out brilliant purple (Mauveine); on the right, in Beijing on 4 October 1971, 40-year-old chemist Tu Youyou unrolls Ge Hong's 340 AD medical scroll beside a cold diethyl-ether condenser dripping golden sweet-wormwood extract (Sample #191).",
             STYLE + "Split period laboratory scene: on the left in an 1856 East London attic lab, eighteen-year-old William Henry Perkin lifts a vivid purple-dyed silk ribbon from a dark coal-tar flask; on the right in 1971 Beijing, forty-year-old chemist Tu Youyou holds an unrolled bamboo-and-silk 340 AD medical scroll beside a glass condenser dripping golden sweet-wormwood extract." + QUAL_TAIL,
             {"kind": "WHEN", "label": "LONDON, EASTER 1856 · BEIJING, 4 OCTOBER 1971 · 340 AD", "timeline_step": "1/5 · 340 AD (Ge Hong writes cold-water Qinghao malaria recipe in China), 3/5 · Easter 1856 (William Henry Perkin synthesizes purple Mauveine while seeking quinine) & 5/5 · 4 Oct 1971 (Tu Youyou extracts Sample #191 artemisinin in 35 °C ether)", "hold_s": 3.5}),
            ("02_pelletier_1820_bark_perkin_1856_dye_ross_1897_mosquito_tu_youyou_1971_scroll_split", 5.5, 6.0, "B", False, "BARK, DYE, MOSQUITO, SCROLL", "Quality",
             "Quality: complex four-part composition (Pelletier and Caventou's 1820 cinchona bark and quinine crystals in Paris; Perkin's 1856 purple Mauveine flask in London; Ronald Ross's 20 August 1897 microscope in Secunderabad showing pigmented malaria cysts on a mosquito stomach wall; and Tu Youyou's 1971 Sample #191 crystal of artemisinin in Beijing).",
             STYLE + "Four-panel period composition: on the left, reddish Andean cinchona bark beside white quinine needles; second, a glass flask of vivid purple Mauveine dye with a violet silk ribbon; third, a brass microscope over a dissected dappled-winged Anopheles mosquito; on the right, an ancient Chinese medical scroll beside golden sweet-wormwood extract and white artemisinin crystals." + QUAL_TAIL,
             None),
            ("03_ronald_ross_20_aug_1897_secunderabad_sweating_over_brass_microscope_mosquito", 11.5, 6.0, "C", False, "20 AUGUST 1897", "Quality",
             "Quality: readable face (on 20 August 1897 in Secunderabad, India, Ronald Ross wipes sweat from his brow and peers through his brass microscope at the dissected stomach wall of an Anopheles mosquito dotted with black-pigmented Plasmodium cysts).",
             STYLE + "In a humid 1897 military hospital laboratory in Secunderabad, India, British surgeon Ronald Ross in a汗-dampened linen shirt wipes his brow and peers intently through a brass microscope at a glass slide holding a dissected dappled-winged mosquito." + QUAL_TAIL,
             {"kind": "WHEN", "label": "SECUNDERABAD, 20 AUGUST 1897", "timeline_step": "4/5 · 6 Nov 1880 & 20 Aug 1897 (Charles Laveran in Algeria and Ronald Ross in Secunderabad prove Plasmodium parasites inside female Anopheles mosquitoes cause malaria)", "hold_s": 3.5}),
            ("04_tu_youyou_1971_100c_boiling_12pct_vs_35c_cold_ether_sample_191_100pct_chart", 17.5, 8.0, "E", False, "100 °C BOILING (12–40% INHIBITION) VS 35 °C COLD ETHER SAMPLE #191 (100% PARASITE CLEARANCE)", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked extraction-temperature and parasite-clearance chart from Tu Youyou (1971–1972 & 2011 Nature Medicine 17: 1217–1220) compares traditional boiling-water/ethanol extraction of Artemisia annua at 80–100 °C (12% to 40% malaria inhibition, heat-destroying the peroxide bridge) against Tu Youyou's 4 October 1971 Sample #191 cold diethyl-ether extraction at 35 °C (100% parasite clearance in rodent and monkey malaria).",
             {"kind": "DATA", "label": "4 OCT 1971 SAMPLE #191: 100 °C BOILING (12–40% CURE) VS 35 °C COLD ETHER (100% MALARIA CLEARANCE)", "detail": "Inked extraction-temperature & parasite-clearance chart on period paper from Tu Youyou (1971–1972 & 2011 Nature Medicine 17: 1217–1220) comparing traditional boiling-water/ethanol extraction of Artemisia annua at 80–100 °C (12% to 40% malaria inhibition, heat-destroying the peroxide bridge) against Tu Youyou's 4 October 1971 Sample #191 cold diethyl-ether extraction at 35 °C (100% parasite clearance in rodent and monkey malaria)", "scale": "lowering the extraction heat from boiling water at one hundred degrees Celsius to gentle ether at thirty-five degrees jumped the cure rate from twelve per cent to a complete one hundred per cent", "who_card": "Pierre Pelletier (1788–1842) — French pharmacist · Joseph Caventou (1795–1877) — French pharmacist · William Henry Perkin (1838–1907) — English chemistry student · Charles Laveran (1845–1922) — French army physician · Ronald Ross (1857–1932) — British medical officer · Ge Hong (283–343 AD) — Chinese medical scholar · Tu Youyou (born 1930) — Chinese pharmaceutical chemist", "when_stamp": "1820 · Easter 1856 · 1880 · 20 August 1897 · 4 October 1971", "hold_s": 3.8}),
            ("05_cinchona_bark_quinine_vial_purple_mauveine_silk_and_sweet_wormwood_leaf_pan", 25.5, 5.5, "A", False, "4 OCTOBER 1971", "Fast",
             "Fast: daylight macro pan across reddish Peruvian cinchona bark, a stoppered vial of white quinine needles, a purple Mauveine silk ribbon, and fresh green Artemisia annua sweet-wormwood leaves on an oak bench between code graphics so two full-frame graphics never run back to back. Nothing emissive, no face.",
             STYLE + "In crisp daylight on an oak laboratory bench, the camera pans smoothly across strips of reddish Andean cinchona bark, a glass vial of white quinine crystals, a violet-dyed silk ribbon, and feathery green sweet-wormwood leaves." + FAST_TAIL,
             None),
            ("06_anopheles_2_5mg_mosquito_600k_deaths_vs_sharks_wolves_lethality_chart", 31.0, 8.0, "E", False, "100% PARASITE CLEARANCE", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period parchment, an inked global animal lethality comparison chart contrasts large predators (<10 to 100 human deaths/year) against the 2.5-milligram female Anopheles mosquito (~600,000 malaria deaths/year out of ~249 million cases, WHO World Malaria Report).",
             {"kind": "DATA", "label": "2.5 MG ANOPHELES MOSQUITO (~600,000 MALARIA DEATHS/YR ACROSS 249M CASES) VS SHARKS & WOLVES", "detail": "Inked global animal lethality comparison chart contrasting large predators (<10 to 100 deaths/yr) against the 2.5-milligram female Anopheles mosquito (~600,000 malaria deaths/yr out of ~249 million cases, WHO World Malaria Report)", "scale": "a single female Anopheles mosquito weighs less than a raindrop — about two and a half milligrams — yet mosquitoes kill more people every single year than every shark, lion, and wolf on Earth combined", "hold_s": 3.8}),
            ("07_table_three_props_cinchona_bark_ross_brass_microscope_and_ge_hong_scroll_ether_flask", 39.0, 5.5, "C", False, "340 AD TO 1971", "Fast",
             "Fast: daylight prop table (callback source for Part 05: Andean cinchona bark beside a vial of quinine sulfate, Ronald Ross's brass microscope with a mosquito slide, and Ge Hong's 340 AD scroll beside a glass flask of golden sweet-wormwood extract). Nothing emissive.",
             STYLE + "On an oak workbench in soft window light sit three objects side by side: reddish cinchona tree bark beside a vial of white quinine crystals, an antique brass microscope with a glass slide, and a bamboo scroll beside a flask of golden herbal extract." + FAST_TAIL,
             None),
            ("08_explorer_chilling_35c_ether_wormwood_flask_to_precipitate_intact_artemisinin_crystal", 62.0, 5.5, "A", True, None, "Quality",
             "Quality: Explorer beat 1 (locked character reference, after 1:00).",
             STYLE + "Standing between two glass extraction flasks of green sweet-wormwood leaves, the Explorer sees the steaming hot 100-degree flask crack a delicate molecular bridge into grey ash, then turns a brass valve to chill the second flask in a cool 35-degree bath as an intact golden artemisinin crystal precipitates at the bottom." + EXP_TAIL,
             None),
            ("09_pelletier_and_caventou_1820_paris_crystallising_white_quinine_from_cinchona_bark", 67.5, 5.5, "B", False, "PARIS, 1820", "Quality",
             "Quality: readable faces (in Paris in 1820, French pharmacists Pierre Pelletier and Joseph Caventou crystallize bitter white needles of quinine sulfate from strips of reddish Peruvian cinchona bark).",
             STYLE + "In an 1820 Paris pharmacy laboratory, French pharmacists Pierre Pelletier and Joseph Caventou in period frock coats hold up a glass crystallization dish of fine white quinine needles beside strips of reddish Peruvian cinchona bark." + QUAL_TAIL,
             {"kind": "WHEN", "label": "PARIS, 1820", "timeline_step": "2/5 · 1820 (Pelletier and Caventou in Paris isolate quinine from Andean cinchona bark)", "hold_s": 3.5}),
        ],
    ),
    (
        2,
        "Part 02 — 1820 & Easter 1856: Andean Fever Bark, Quinine & How William Perkin's Failed Malaria Cure Dyed the World Purple",
        [
            ("01_pelletier_caventou_1820_quinine_and_perkin_easter_1856_hofmann_purple_mauveine", 73.0, 6.5, "A", False, "REFUSED TO PATENT QUININE", "Quality",
             "Quality: readable faces (French pharmacists Pierre Pelletier and Joseph Caventou in 1820 Paris isolating white quinine crystals without a patent, dissolving to 18-year-old William Henry Perkin under professor August Wilhelm von Hofmann's assignment in March 1856 pulling a purple-stained silk cloth from a black coal-tar flask).",
             STYLE + "Split period scene: on the left in 1820 Paris, pharmacists Pierre Pelletier and Joseph Caventou present unpatented white quinine crystals; on the right in an 1856 London laboratory, professor August Wilhelm von Hofmann watches eighteen-year-old William Henry Perkin draw a brilliant purple-dyed silk cloth from a coal-tar beaker." + QUAL_TAIL,
             {"kind": "WHO", "label": "August Wilhelm von Hofmann (1818–1892) — German chemistry professor", "fact_card": "Refused to patent quinine", "when_stamp": "1820 · March 1856 · 1944", "timeline_step": "2/5 · 1820 (Pelletier and Caventou isolate quinine) & 3/5 · Easter 1856 (18-year-old William Henry Perkin accidentally synthesizes purple Mauveine dye while trying to make quinine)", "hold_s": 3.8}),
            ("02_perkin_1856_additive_aniline_formula_mauveine_vs_1820_quinine_3d_structure_chart", 79.5, 8.0, "E", False, "EASTER 1856 PERKIN REACTION: COAL-TAR ANILINE → PURPLE MAUVEINE (C26H23N4+) VS QUININE (C20H24N2O2, 2–8% BARK YIELD)", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked chemical-formula vs 3D-structure comparison diagram contrasts William Perkin's 1856 additive formula calculation (2 C10H13N + 3 O → C20H24N2O2 + H2O, which oxidized aniline into purple Mauveine C26H23N4+/C27H25N4+ instead of quinine, synthesized only in 1944) against Pelletier and Caventou's 1820 natural quinine alkaloid extracted at ~2–8% yield from Andean cinchona bark.",
             {"kind": "DATA", "label": "EASTER 1856 PERKIN: COAL-TAR ANILINE → PURPLE MAUVEINE VS QUININE (2–8% BARK YIELD; 10,000 SNAILS/G TYRIAN PURPLE)", "detail": "Inked chemical-formula vs 3D-structure comparison diagram on period paper contrasting William Perkin's 1856 additive formula calculation (2 C10H13N + 3 O → C20H24N2O2 + H2O, which produced purple Mauveine C26H23N4+/C27H25N4+ instead of quinine) against Pelletier and Caventou's 1820 natural quinine alkaloid extracted at ~2–8% yield from Andean cinchona bark", "scale": "in eighteen fifty-six, purple dye had to be crushed out of ten thousand Mediterranean sea snails just to make a single gram — until eighteen-year-old William Perkin brewed vibrant purple out of black coal-tar waste in his bedroom", "hold_s": 3.8}),
            ("03_perkin_1856_violet_mauveine_flask_dyed_purple_silk_and_coal_tar_bottle_closeup", 87.5, 6.5, "B", False, "EASTER 1856 — MAUVEINE", "Fast",
             "Fast: daylight macro shot of William Perkin's 1856 glass flask of deep violet Mauveine solution beside a strip of dyed purple silk and a dark bottle of coal-tar aniline on an oak attic bench. Nothing emissive, no face.",
             STYLE + "In crisp daylight on a wooden attic workbench, a glass flask of rich violet Mauveine liquid sits beside a folded strip of purple-dyed silk cloth and a stoppered bottle of dark coal tar." + FAST_TAIL,
             None),
            ("04_andean_cinchona_bark_bundles_and_1820_paris_quinine_apothecaries_jar_pan", 94.0, 5.5, "C", False, "1820 — QUININE ISOLATED", "Fast",
             "Fast: daylight close-up pan across dried bundles of Peruvian cinchona bark, a porcelain mortar and pestle, and an 1820 Paris apothecary jar of white quinine sulfate crystals on an oak table. Nothing emissive, no face.",
             STYLE + "In bright window light on an oak pharmacy counter, bundles of reddish Peruvian cinchona bark rest beside a porcelain mortar and pestle and a glass apothecary jar of white quinine powder." + FAST_TAIL,
             None),
        ],
    ),
    (
        3,
        "Part 03 — 6 November 1880 & 20 August 1897: Laveran's Wriggling Parasite & Ronald Ross's 'Mosquito Day' — Midpoint Twist",
        [
            ("01_laveran_6_nov_1880_algeria_parasite_and_ross_20_aug_1897_manson_husein_khan_grassi", 99.5, 6.5, "A", False, "DISSECTED 1,000 MOSQUITOES", "Quality",
             "Quality: readable faces (French army physician Charles Laveran on 6 November 1880 in Constantine, Algeria, spotting motile Plasmodium parasites in blood, dissolving to Ronald Ross in Secunderabad with Patrick Manson, patient Husein Khan, and Italian zoologist Giovanni Battista Grassi confirming Anopheles mosquito transmission).",
             STYLE + "Split period scene: on the left in an 1880 military hospital in Algeria, French army doctor Charles Laveran peers through a microscope at a blood slide; on the right in 1897 Secunderabad, surgeon Ronald Ross and patient Husein Khan examine a cage of dappled-winged Anopheles mosquitoes alongside zoologist Giovanni Battista Grassi." + QUAL_TAIL,
             {"kind": "WHO", "label": "Patrick Manson (1844–1922) — Scottish tropical physician · Husein Khan (fl. 1897) — Secunderabad hospital patient · Giovanni Battista Grassi (1854–1925) — Italian zoologist", "fact_card": "Dissected 1,000 mosquitoes", "when_stamp": "6 November 1880 · 16 August 1897 · 20 August 1897 · November 1898", "timeline_step": "4/5 · 6 Nov 1880 & 20 Aug 1897 (Charles Laveran in Algeria and Ronald Ross in Secunderabad prove Plasmodium parasites inside female Anopheles mosquitoes cause malaria)", "hold_s": 3.8}),
            ("02_laveran_ross_plasmodium_30000x_liver_amplification_and_48h_red_blood_cell_cycle_chart", 106.0, 8.0, "E", False, "20 AUG 1897 ROSS & LAVERAN: 1 SPOROZOITE → 30,000× IN 1 LIVER CELL → 10¹¹–10¹² RED BLOOD CELLS BURST EVERY 48 H", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked Plasmodium lifecycle and liver/blood amplification chart from Laveran (1880) and Ross (18 December 1897 British Medical Journal 2: 1786–1788) shows 10–100 mosquito-injected sporozoites multiplying ~10,000–30,000× inside a single liver cell before invading red blood cells and bursting 10¹¹–10¹² cells every 48 hours.",
             {"kind": "DATA", "label": "PLASMODIUM AMPLIFICATION: 1 SPOROZOITE → 30,000× PER LIVER CELL → 10¹¹–10¹² RED CELLS EVERY 48 HOURS", "detail": "Inked Plasmodium lifecycle & liver/blood amplification chart on period paper from Laveran (1880) and Ross (18 December 1897 British Medical Journal 2: 1786–1788) showing 10–100 mosquito-injected sporozoites multiplying ~10,000–30,000× inside a single liver cell before invading red blood cells and bursting 10¹¹–10¹² cells every 48 hours", "scale": "a single malaria parasite injected by one mosquito bite multiplies up to thirty thousand times inside one human liver cell before flooding the bloodstream with hundreds of billions of parasites", "hold_s": 3.8}),
            ("03_ross_20_aug_1897_secunderabad_notebook_brass_microscope_and_mosquito_slide", 114.0, 6.5, "B", False, "20 AUGUST 1897 — MOSQUITO DAY", "Fast",
             "Fast: daylight macro shot of Ronald Ross's 20 August 1897 laboratory notebook open beside his brass microscope, fine dissecting needles, and a mesh cage of dappled-winged Anopheles mosquitoes on a wooden table. Nothing emissive, no face.",
             STYLE + "In crisp daylight on a wooden dissection table, an open 1897 leather laboratory notebook with inked circle sketches sits beside a brass microscope, fine steel dissecting needles, and a small gauze mosquito cage." + FAST_TAIL,
             None),
            ("04_laveran_1880_blood_smear_slides_and_1897_bmj_offprint_pan", 120.5, 5.5, "C", False, "6 NOVEMBER 1880 — PLASMODIUM", "Fast",
             "Fast: daylight close-up pan across Charles Laveran's 1880 stained glass blood-smear slides in a wooden tray beside Ronald Ross's December 1897 British Medical Journal paper on an oak desk. Nothing emissive, no face.",
             STYLE + "In bright window light on an oak desk, a wooden slide tray of stained glass blood smears rests beside a printed 1897 medical journal and a brass magnifying lens." + FAST_TAIL,
             None),
        ],
    ),
    (
        4,
        "Part 04 — 340 AD & 4 October 1971: Tu Youyou's Sample #191, Ge Hong's Cold-Water Clue & Artemisinin",
        [
            ("01_tu_youyou_4_oct_1971_beijing_reading_ge_hong_340ad_scroll_by_35c_ether_condenser", 126.0, 6.5, "A", False, "SWALLOWED IT HERSELF FIRST", "Quality",
             "Quality: readable face (pharmaceutical chemist Tu Youyou in Beijing, January 1969 – 4 October 1971, comparing Ge Hong's 340 AD scroll 'Zhouhou Beiji Fang' against a 35 °C diethyl-ether condenser producing Sample #191 from sweet wormwood Artemisia annua).",
             STYLE + "In a 1971 Beijing laboratory, pharmaceutical chemist Tu Youyou in a white lab coat points to a classical 340 AD Chinese medical scroll on her bench beside a low-temperature 35-degree diethyl-ether distillation flask holding golden Sample #191 sweet-wormwood extract." + QUAL_TAIL,
             {"kind": "FACT", "label": "Swallowed it herself first", "when_stamp": "23 May 1967 · January 1969 · 4 October 1971 · July 1972 · November 1972 · 2015", "timeline_step": "1/5 · 340 AD (Ge Hong writes cold-water Qinghao recipe) & 5/5 · 4 Oct 1971 (Tu Youyou in Beijing uses 35 °C diethyl ether to create Sample #191 artemisinin with 100% malaria clearance)", "hold_s": 3.8}),
            ("02_tu_youyou_2000_recipes_380_extracts_sample_191_and_endoperoxide_heme_trap_chart", 132.5, 8.0, "E", False, "PROJECT 523 SCREENING FUNNEL: 2,000 RECIPES → 380 EXTRACTS → SAMPLE #191 (35 °C ETHER = 100% CURE VIA HEME-CLEAVED O–O BRIDGE)", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked screening-funnel and artemisinin endoperoxide mechanism diagram from Tu Youyou (2011 Nature Medicine 17: 1217–1220) shows 2,000 traditional recipes narrowed to 380 mouse-tested extracts and Sample #191 (4 October 1971, 35 °C ether extraction = 100% clearance), where the iron-rich heme inside malaria-infected red blood cells cleaves artemisinin's O–O endoperoxide bridge into parasite-killing free radicals.",
             {"kind": "DATA", "label": "SAMPLE #191 FUNNEL: 2,000 RECIPES → 380 EXTRACTS → 35 °C ETHER (100% CURE VIA IRON-CLEAVED O–O BRIDGE)", "detail": "Inked screening-funnel & artemisinin endoperoxide mechanism diagram on period paper from Tu Youyou (2011 Nature Medicine 17: 1217–1220) showing 2,000 traditional recipes narrowed to 380 mouse-tested extracts and Sample #191 (4 October 1971, 35 °C ether extraction = 100% clearance), where the iron-rich heme inside malaria-infected red blood cells cleaves artemisinin's O–O endoperoxide bridge into parasite-killing free radicals", "scale": "out of two thousand ancient recipes and three hundred and eighty lab extracts, it took batch number one hundred and ninety-one — brewed in cool ether at thirty-five degrees — to hit one hundred per cent cure", "hold_s": 3.8}),
            ("03_nov_1972_beijing_white_artemisinin_crystals_ge_hong_340ad_scroll_and_sample_191_flask", 140.5, 6.5, "B", False, "4 OCTOBER 1971 — SAMPLE #191", "Fast",
             "Fast: daylight macro shot of pure white crystalline needles of artemisinin (Qinghaosu) in a glass dish beside Ge Hong's 340 AD text, green Artemisia annua leaves, and the Sample #191 glass bottle on a Beijing laboratory bench. Nothing emissive, no face.",
             STYLE + "In crisp daylight on a laboratory bench, a glass petri dish of white crystalline artemisinin needles sits beside an unrolled 340 AD Chinese scroll, fresh sweet-wormwood leaves, and a stoppered glass sample bottle." + FAST_TAIL,
             None),
            ("04_explorer_sliding_artemisinin_mousetrap_into_iron_gorging_malaria_parasite", 147.0, 5.5, "B", True, None, "Quality",
             "Quality: Explorer beat 2 (locked character reference).",
             STYLE + "Watching a miniature malaria parasite gorge on red iron spheres inside a cutaway red blood cell model, the Explorer slides in a spring-loaded artemisinin molecular trap whose oxygen-oxygen bridge snaps shut the instant the parasite's stolen iron touches it." + EXP_TAIL,
             None),
        ],
    ),
    (
        5,
        "Part 05 — The Iron Mousetrap & Why John Dalton Had His Own Eyeballs Cut Open After Death",
        [
            ("01_timeline_340ad_to_1971_and_endoperoxide_iron_activation_chart", 152.5, 8.5, "E", False, "340 AD–1971 TIMELINE · 1,631 YEARS FROM GE HONG'S COLD-WATER SCROLL TO TU YOUYOU'S SAMPLE #191", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, the 5-date timeline completes: 340 AD (Ge Hong writes cold-water Qinghao malaria recipe in China) · 1820 (Pelletier and Caventou in Paris isolate quinine from Andean cinchona bark) · Easter 1856 (18-year-old William Henry Perkin in London accidentally synthesizes purple Mauveine dye while trying to make quinine) · 6 Nov 1880 & 20 Aug 1897 (Charles Laveran in Algeria and Ronald Ross in Secunderabad prove Plasmodium parasites inside female Anopheles mosquitoes cause malaria) · 4 Oct 1971 (Tu Youyou in Beijing uses 35 °C diethyl ether to create Sample #191 artemisinin with 100% malaria clearance) alongside the endoperoxide heme-activation diagram.",
             {"kind": "DATA", "label": "340 AD–1971 TIMELINE · 1,631 YEARS FROM GE HONG'S COLD-WATER RECIPE TO TU YOUYOU'S 100% SAMPLE #191", "detail": "Animated 5-date timeline (340 AD → 4 Oct 1971) alongside the endoperoxide heme-activation diagram", "scale": "sixteen hundred and thirty-one years separated Ge Hong's brush on a Chinese scroll in three-forty AD from Tu Youyou's cold-ether flask on the fourth of October nineteen seventy-one", "when_stamp": "340 AD–1971", "timeline_step": "5/5 · 340 AD–1971 timeline complete", "hold_s": 3.8}),
            ("02_intact_35c_endoperoxide_ring_model_and_artemisinin_combination_pack_pan", 161.0, 5.5, "A", False, "TRIGGERED BY STOLEN IRON", "Fast",
             "Fast: daylight close-up of a 3D ball-and-stick artemisinin molecule highlighting its intact oxygen-oxygen peroxide bridge beside dried Artemisia annua leaves and modern artemisinin tablets on a wooden museum plinth. Nothing emissive, no face.",
             STYLE + "In crisp daylight on a wooden museum plinth, a ball-and-stick molecular model of artemisinin with a red oxygen-oxygen bridge sits beside dried sweet-wormwood stems and a glass dish of white crystals." + FAST_TAIL,
             None),
            ("03_john_dalton_31_oct_1794_pink_geranium_ransome_28_jul_1844_eye_and_1995_dna_handoff", 166.5, 6.5, "C", False, "DALTON'S DISSECTED EYES", "Quality",
             "Quality: readable faces (28-year-old Quaker chemist John Dalton in Manchester on 31 October 1794 holding a pink geranium flower by candlelight, alongside physician Joseph Ransome on 28 July 1844 peering through Dalton's dissected eyeball and Hunt and Mollon's 1995 DNA tube — handoff to 049 Colour Vision).",
             STYLE + "Split period scene: on the left in 1794 Manchester, twenty-eight-year-old Quaker chemist John Dalton holds a pink crane's-bill geranium flower between a window and a candle; on the right in 1844 Manchester, physician Joseph Ransome peers through the clear rear window of Dalton's dissected eye at scarlet and green ribbons." + QUAL_TAIL,
             {"kind": "WHEN", "label": "31 OCTOBER 1794 · 28 JULY 1844 · 1995", "hold_s": 3.5}),
            ("04_table_three_callback", 173.0, 2.4, "C", False, None, "reuse",
             "Reuse: verified unused moving window [5.50s..7.90s] of P1:07_table_three_props_cinchona_bark_ross_brass_microscope_and_ge_hong_scroll_ether_flask (callback, £0).",
             "Reuse P1:07_table_three_props_cinchona_bark_ross_brass_microscope_and_ge_hong_scroll_ether_flask [5.50s..7.90s] (2.40s distinct non-overlapping tail window from 8.00s source clip).",
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
                row["reuse_of"] = "P1:07_table_three_props_cinchona_bark_ross_brass_microscope_and_ge_hong_scroll_ether_flask"
                row["reuse_window_s"] = [5.5, 7.9]
                row["reuse_audit"] = {
                    "source_row": "P1:07_table_three_props_cinchona_bark_ross_brass_microscope_and_ge_hong_scroll_ether_flask",
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
            "film": "048_Perkin-Ross-TuYouyou-Malaria-Quinine-Artemisinin",
            "part": p_idx,
            "title": p_title,
            "version": "v01",
            "timing_status": "pre_vo_script_clock (built from malaria_script_master_v01.md; retimes onto Scribe STT once VO locks)",
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
        "film": "048_Perkin-Ross-TuYouyou-Malaria-Quinine-Artemisinin",
        "version": "v01",
        "date": "2026-10-18",
        "owner": "gemini (J0570)",
        "status": "PRE_VO_BOARDS_V01_NO_MINT",
        "generation_authorized": False,
        "script": "00_Brand/Channel-Setup/ideas/048_Perkin-Ross-TuYouyou-Malaria-Quinine-Artemisinin/malaria_script_master_v01.md",
        "sources": "00_Brand/Channel-Setup/ideas/048_Perkin-Ross-TuYouyou-Malaria-Quinine-Artemisinin/SOURCES_v01.md",
        "credit_snapshot": {
            "flow_balance": 23740,
            "flow_floor": 0,
            "flow_read_at": "2026-10-15T21:42:22Z",
            "vertex_promo_gbp": 71.02,
            "vertex_usable_gbp": 70.02,
        },
        "totals": totals,
        "per_part": per_part_summary,
        "mint_order": "006 > 007 > 008 > 009 > 010 > 011 > 012 > 013 > 014 > 015 > 016 > 017 > 018 > 019 > 020 > 021 > 022 > 023 > 024 > 025 > 026 > 027 > 028 > 029 > 030 > 031 > 032 > 033 > 034 > 035 > 036 > 037 > 038 > 039 > 040 > 041 > 042 > 043 > 044 > 045 > 046 > 047 > 048 > 049 > 050. Nothing in 048 is generation_authorized.",
    }
    (EDIT / "PICTURE_PLAN_v01.json").write_text(json.dumps(plan, indent=2) + "\n")

    sl = [
        "# 048 Malaria & Artemisinin: The 340 AD Scroll That Saved Millions — Shot list & plate boards v01 (pre-VO)",
        "",
        "Gemini, 18 Oct 2026, J0570. Built from `malaria_script_master_v01.md` (`91.6 PASS`) and `SOURCES_v01.md`.",
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
        "# 048 price review v01 (pre-VO plate boards)",
        "",
        "Gemini, 18 Oct 2026, J0570. Boards only. **No mint. No spend. No merge.**",
        "Prepared from `malaria_script_master_v01.md` (`91.6 PASS`) and `SOURCES_v01.md` so 048's full plate board rows, non-emissive Fast prompts, £0 code graphics, and Teach-on-Screen overlays are ready to re-time the moment long VO locks. Parked for Chief.",
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
        f"- **Quality ({totals['Quality']} rows):** readable faces (William Henry Perkin, Tu Youyou, Pierre Pelletier, Joseph Caventou, August Wilhelm von Hofmann, Charles Laveran, Ronald Ross, Husein Khan, Giovanni Battista Grassi, John Dalton, Joseph Ransome), 1856 London Mauveine discovery, 1971 Beijing Sample #191 cold-ether extraction, 1897 Secunderabad mosquito dissection, 1820 Paris quinine isolation, and the 2 Explorer beats.",
        f"- **Fast ({totals['Fast']} rows, non-emissive):** daylight prop and laboratory shots (cinchona bark, quinine vial, purple Mauveine silk & Artemisia annua leaves pan, 3-object callback bench, Perkin's 1856 Mauveine flask & dyed silk, Andean cinchona bark bundles & 1820 apothecary jar, Ross's 20 August 1897 notebook & brass microscope, Laveran's 1880 blood-smear slides & 1897 BMJ paper, white crystalline artemisinin needles & Ge Hong's 340 AD scroll, 3D artemisinin endoperoxide ring model & dried wormwood stems). Zero candles, flames, sparks, or glowing elements on Fast.",
        f"- **£0 code graphics ({totals['code_graphic']} rows):**",
        "  1. `P1:04_tu_youyou_1971_100c_boiling_12pct_vs_35c_cold_ether_sample_191_100pct_chart` — Boiling-water extraction at 80–100 °C (12%–40% malaria inhibition) vs Tu Youyou's 4 October 1971 Sample #191 cold diethyl-ether extraction at 35 °C (100% parasite clearance) (`SCALE: lowering the extraction heat from boiling water at one hundred degrees Celsius to gentle ether at thirty-five degrees jumped the cure rate from twelve per cent to a complete one hundred per cent`)",
        "  2. `P1:06_anopheles_2_5mg_mosquito_600k_deaths_vs_sharks_wolves_lethality_chart` — Global animal lethality comparison: sharks, wolves & lions (<10–100 deaths/yr) vs the 2.5 mg female Anopheles mosquito (~600,000 malaria deaths/yr across ~249M cases) (`SCALE: a single female Anopheles mosquito weighs less than a raindrop — about two and a half milligrams — yet mosquitoes kill more people every single year than every shark, lion, and wolf on Earth combined`)",
        "  3. `P2:02_perkin_1856_additive_aniline_formula_mauveine_vs_1820_quinine_3d_structure_chart` — Perkin's Easter 1856 additive formula calculation (coal-tar aniline → purple Mauveine C26H23N4+ vs 10,000 sea snails/g Tyrian purple) vs Pelletier & Caventou's 1820 natural quinine alkaloid (~2–8% bark yield) (`SCALE: in eighteen fifty-six, purple dye had to be crushed out of ten thousand Mediterranean sea snails just to make a single gram — until eighteen-year-old William Perkin brewed vibrant purple out of black coal-tar waste in his bedroom`)",
        "  4. `P3:02_laveran_ross_plasmodium_30000x_liver_amplification_and_48h_red_blood_cell_cycle_chart` — Laveran (1880) & Ross (1897) Plasmodium amplification: 1 sporozoite → ~30,000× inside a single liver cell → 10¹¹–10¹² red blood cells burst every 48 hours (`SCALE: a single malaria parasite injected by one mosquito bite multiplies up to thirty thousand times inside one human liver cell before flooding the bloodstream with hundreds of billions of parasites`)",
        "  5. `P4:02_tu_youyou_2000_recipes_380_extracts_sample_191_and_endoperoxide_heme_trap_chart` — Project 523 screening funnel (2,000 recipes → 380 extracts → Sample #191 at 35 °C = 100% cure) & iron-heme cleavage of artemisinin's O–O endoperoxide bridge (`SCALE: out of two thousand ancient recipes and three hundred and eighty lab extracts, it took batch number one hundred and ninety-one — brewed in cool ether at thirty-five degrees — to hit one hundred per cent cure`)",
        "  6. `P5:01_timeline_340ad_to_1971_and_endoperoxide_iron_activation_chart` — completed 5-date timeline (340 AD → 4 Oct 1971) + endoperoxide heme-activation diagram (`SCALE: sixteen hundred and thirty-one years separated Ge Hong's brush on a Chinese scroll in three-forty AD from Tu Youyou's cold-ether flask on the fourth of October nineteen seventy-one`)",
        f"- **£0 verified reuse ({totals['reuse']} row):** `P5:04_table_three_callback` uses the 2.40 s unused moving tail `[5.50s..7.90s]` of `P1:07_table_three_props_cinchona_bark_ross_brass_microscope_and_ge_hong_scroll_ether_flask`.",
        "",
        "## Mint order",
        "",
        "006 > 007 > 008 > 009 > 010 > 011 > 012 > 013 > 014 > 015 > 016 > 017 > 018 > 019 > 020 > 021 > 022 > 023 > 024 > 025 > 026 > 027 > 028 > 029 > 030 > 031 > 032 > 033 > 034 > 035 > 036 > 037 > 038 > 039 > 040 > 041 > 042 > 043 > 044 > 045 > 046 > 047 > 048 > 049 > 050. `generation_authorized` is `false` on every row.",
    ])
    (EDIT / "PRICE_REVIEW_v01.md").write_text("\n".join(pr_lines) + "\n")
    print(f"048 v01 boards written: {totals['rows']} rows, Flow expected={totals['flow_credits_expected']}")


if __name__ == "__main__":
    main()
