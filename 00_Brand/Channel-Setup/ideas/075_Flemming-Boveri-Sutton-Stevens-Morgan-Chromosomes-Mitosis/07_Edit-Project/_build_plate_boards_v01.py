#!/usr/bin/env python3
"""HOS 075 (Chromosomes: How One White-Eyed Fly Mapped DNA) pre-VO plate boards v01. J0706. No mint, no spend.

Built from 00_Brand/Channel-Setup/ideas/075_Flemming-Boveri-Sutton-Stevens-Morgan-Chromosomes-Mitosis/chromosomes_script_master_v01.md
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
        "Part 01 — The White-Eyed Fly in the Banana Bottle & the 46 Threads Inside You",
        [
            ("01_46_crimson_chromosomes_splitting_in_mitosis_beside_white_eyed_fruit_fly_in_columbia_milk_bottle", 0.0, 5.5, "A", False, "46 CHROMOSOMES & ONE WHITE-EYED FLY", "Quality",
             "Quality: Short frame 0 / answer image (0:03) + inside a dividing cell nucleus, 46 crimson-stained chromosomes line up along a mitotic spindle and zip cleanly into two identical daughter cells, while beside it in Columbia University's Fly Room a single white-eyed male fruit fly (Drosophila melanogaster) stands out among hundreds of red-eyed flies inside a glass milk bottle.",
             STYLE + "Split cellular-and-laboratory scene: on the left, crimson X-shaped chromosomes align along a mitotic spindle and pull cleanly apart into two daughter cells; on the right, a glass milk bottle on a workbench reveals a single snow-white-eyed male fruit fly surrounded by brick-red-eyed fruit flies." + QUAL_TAIL,
             {"kind": "WHEN", "label": "NEW YORK, MAY 1910", "timeline_step": "1/3 · 1879–1883 (Walther Flemming stains salamander chromosomes to discover chromatin and mitosis in Kiel; Edouard van Beneden discovers chromosome halving in meiosis)", "hold_s": 3.5}),
            ("02_flemming_1879_boveri_sutton_1902_stevens_1905_morgan_1910_and_sturtevant_1913_split", 5.5, 6.0, "B", False, "DYED MITOSIS, WHITE-EYED FLY, FIRST GENE MAP", "Quality",
             "Quality: complex three-part composition (Walther Flemming at the University of Kiel in 1879 staining translucent salamander cells with aniline dye alongside Theodor Boveri, Walter Sutton with Kansas lubber grasshoppers, and Nettie Stevens at Bryn Mawr in 1905 discovering the X and Y sex chromosomes; Thomas Hunt Morgan in Room 613 of Columbia University's Schermerhorn Hall in May 1910 peering through a hand lens at a lone white-eyed male fruit fly among milk bottles of mashed bananas; and 19-year-old Alfred Sturtevant in January 1913 sketching the first linear chromosome map of six X-linked genes).",
             STYLE + "Three-panel period composition: on the left, Walther Flemming in 1879 Kiel and Nettie Stevens in 1905 Bryn Mawr with brass microscopes beside Walter Sutton and Theodor Boveri; in the centre, Thomas Hunt Morgan in May 1910 New York examining a glass milk bottle of fruit flies with a jeweller's loupe; on the right, young Alfred Sturtevant in 1913 sketching a linear six-gene chromosome map." + QUAL_TAIL,
             None),
            ("03_2m_dna_thread_spooling_into_23_homologous_chromosome_pairs_with_chiasma_crossover_and_xy_pair", 11.5, 6.0, "C", False, "TWO METRES PACKED INTO 46 BUNDLES", "Quality",
             "Quality: complex microscopic reveal (two metres of DNA thread spool tightly into 23 pairs of homologous chromosomes — 46 in mitosis vs 23 shuffled haploid chromosomes with chiasma crossovers in meiosis — alongside an X and Y sex chromosome pair).",
             STYLE + "Macro nuclear animation: two metres of fine double-helical thread wind tightly around histone spools into twenty-three pairs of homologous chromosomes that exchange segments at X-shaped crossover points alongside a paired X and Y sex chromosome." + QUAL_TAIL,
             {"kind": "WHEN", "label": "1879 · 1902 · 1903 · 1905 · MAY 1910 · JANUARY 1913", "timeline_step": "1/3 · 1879–1883 (Flemming & van Beneden) · 2/3 · 1902–1905 (Boveri, Sutton & Nettie Stevens) · 3/3 · May 1910 – Jan 1913 (Morgan & Sturtevant)", "hold_s": 3.5}),
            ("04_flemming_1879_sutton_1903_stevens_1905_morgan_1910_and_sturtevant_1913_chromosome_chart", 17.5, 8.0, "E", False, "DIPLOID MITOSIS (46 → 46+46) VS HAPLOID MEIOSIS (46 → 4×23) · STEVENS XX/XY · MORGAN X-LINKED WHITE EYE & STURTEVANT LINEAR MAP", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked Mitosis, Meiosis, Sex-Linkage & Chromosome Mapping chart from Flemming (1879–1882 Zellsubstanz, Kern und Zelltheilung), Boveri (1902) & Sutton (1902–1903 Biol. Bull. 4: 231–251), Stevens (1905 Carnegie Inst. Wash. Publ. 36), Morgan (22 July 1910 Science 32: 120–122), and Sturtevant (January 1913 J. Exp. Zool. 14: 43–59) compares human diploid mitosis (2n = 46 → 46 + 46) against haploid meiosis (2n = 46 → 4 × n = 23 with homologous crossing over), Morgan's X-linked 3:1 white-eye male inheritance, and Sturtevant's linear centimorgan map of 6 Drosophila X-chromosome genes.",
             {"kind": "DATA", "label": "MITOSIS (46 → 46+46) VS MEIOSIS (46 → 4×23), STEVENS XX/XY SEX CHROMOSOMES & STURTEVANT 1913 LINEAR CENTIMORGAN MAP", "detail": "Inked mitosis vs meiosis chromosome division & Sturtevant linear gene-map chart on period paper showing diploid mitosis (46 chromosomes → 2 identical cells of 46), meiosis (23 homologous pairs crossing over → 4 unique gametes of 23), XX vs XY sex determination, and Sturtevant's 1913 crossover recombination map (1% crossover = 1 map unit / centimorgan across 6 X-linked genes)", "scale": "packing two metres of DNA into forty-six microscopic chromosomes inside a cell nucleus six micrometres wide is like winding forty kilometres of ultra-fine sewing thread into forty-six neat bobbins inside a walnut shell — and then splitting every bobbin in half without a single knot", "who_card": "Walther Flemming (1843–1905) — German anatomist and cell biologist · Theodor Boveri (1862–1915) — German zoologist and cytologist · Walter Stanborough Sutton (1877–1916) — American geneticist and physician · Nettie Maria Stevens (1861–1912) — American geneticist · Thomas Hunt Morgan (1866–1945) — American evolutionary biologist and geneticist · Alfred Henry Sturtevant (1891–1970) — American geneticist", "when_stamp": "1879 · 1902 · 1903 · 1905 · May 1910 · January 1913", "hold_s": 3.8}),
            ("05_flemming_1882_zellsubstanz_lithograph_aniline_dye_bottle_and_1910_science_offprint_pan", 25.5, 5.5, "A", False, "FORTY-SIX MICROSCOPIC THREADS", "Fast",
             "Fast: daylight macro pan across Walther Flemming's 1882 Zellsubstanz lithograph plate of salamander mitosis, a glass bottle of crimson aniline dye, and a 1910 Science offprint on an oak bench between code graphics so two full-frame graphics never run back to back. Nothing emissive, no face.",
             STYLE + "In crisp daylight on an oak cytology bench, the camera pans smoothly across an 1882 lithographed plate of dividing chromosomes, a stoppered bottle of crimson aniline stain, and an open 1910 journal." + FAST_TAIL,
             None),
            ("06_morgan_22_jul_1910_science_white_eye_cross_and_sturtevant_jan_1913_six_gene_map_chart", 31.0, 8.0, "E", False, "COLUMBIA UNIVERSITY, 1910–1913", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period parchment, an inked Thomas Hunt Morgan White-Eyed Drosophila & Alfred Sturtevant Six-Gene Crossover Map diagram (from T. H. Morgan, 22 July 1910 Science 32: 120–122 & A. H. Sturtevant, January 1913 J. Exp. Zool. 14: 43–59) shows F1 all red-eyed hybrids and F2 3:1 red-to-white ratio where 100% of white-eyed flies are male (XrY), alongside Sturtevant's linear X-chromosome map spacing yellow (0.0), white (1.0), vermilion (30.7), miniature (33.7), and rudimentary (57.6) by crossover frequency.",
             {"kind": "DATA", "label": "22 JUL 1910 MORGAN F2 SEX-LINKED CROSS (3,470 RED : 782 WHITE MALES, 0 WHITE FEMALES) & JAN 1913 STURTEVANT 6-GENE LINEAR MAP", "detail": "Inked Morgan (22 July 1910 Science 32: 120–122) F2 sex-linked cross (2,459 red-eyed females, 1,011 red-eyed males, 0 white-eyed females, 782 white-eyed males) & Sturtevant (January 1913 J. Exp. Zool. 14: 43–59) six-factor linear crossover map on period paper", "scale": "Alfred Sturtevant realized that chromosomes swap pieces at random like two beaded necklaces tangling in a drawer — so if two beads get separated ten times more often than two others, they must sit ten times farther apart along the string", "hold_s": 3.8}),
            ("07_table_three_props_1879_flemming_stained_slide_1910_morgan_milk_bottle_and_1913_sturtevant_map_ruler", 39.0, 5.5, "C", False, "1879 TO 1913", "Fast",
             "Fast: daylight prop table (callback source for Part 05: Walther Flemming's 1879 crimson-stained salamander mitosis slide, Thomas Hunt Morgan's 1910 cotton-stoppered glass milk bottle with banana mash, and Alfred Sturtevant's 1913 brass ruler and index-card gene map). Nothing emissive.",
             STYLE + "On an oak workbench in soft window light sit three objects side by side: a microscope slide stained crimson with mitotic figures, a cotton-plugged glass milk bottle holding fruit flies, and a brass ruler resting across ruled index cards." + FAST_TAIL,
             None),
            ("08_explorer_measuring_crossover_distance_between_gene_markers_on_braided_chromosome_ropes_with_surveyor_tape", 62.0, 5.5, "A", True, None, "Quality",
             "Quality: Explorer beat 1 (locked character reference, after 1:00).",
             STYLE + "Standing between two thick braided red and blue chromosome ropes studded with coloured gene markers, the Explorer swaps a crossed-over segment between the two ropes and measures the distance between two markers with a brass surveyor's tape." + EXP_TAIL,
             None),
            ("09_morgan_and_sturtevant_1911_columbia_fly_room_counting_drosophila_under_hand_lenses", 67.5, 5.5, "B", False, "THE FLY ROOM BREAKTHROUGH", "Quality",
             "Quality: readable faces (in Room 613 of Schermerhorn Hall at Columbia University in 1911, Thomas Hunt Morgan and 19-year-old Alfred Sturtevant count red-eyed and white-eyed fruit flies under magnifying lenses beside milk bottles of mashed bananas).",
             STYLE + "In Columbia University's crowded 1911 Fly Room lined with glass milk bottles, Thomas Hunt Morgan and young undergraduate Alfred Sturtevant lean over a porcelain sorting plate with magnifying lenses." + QUAL_TAIL,
             {"kind": "WHEN", "label": "COLUMBIA UNIVERSITY, 1910–1913", "timeline_step": "3/3 · May 1910 – Jan 1913 (Morgan proves X-linked chromosome inheritance; Sturtevant builds the first linear chromosome map)", "hold_s": 3.5}),
        ],
    ),
    (
        2,
        "Part 02 — 1879–1905: Walther Flemming's Dyed Salamander Threads, Boveri & Sutton's Grasshoppers, and Nettie Stevens's X and Y Chromosomes",
        [
            ("01_walther_flemming_1879_kiel_mitosis_sutton_1902_grasshoppers_and_nettie_stevens_1905_xy_chromosomes", 73.0, 6.5, "A", False, "46 CHROMOSOMES IN 23 PAIRS", "Quality",
             "Quality: readable faces (German anatomist Walther Flemming in Kiel in 1879–1882 observing crimson aniline-stained salamander mitosis, dissolving to Edouard van Beneden, Theodor Boveri, Walter Sutton with Kansas lubber grasshoppers in 1902–1903, and Nettie Maria Stevens at Bryn Mawr in 1905 identifying the X and Y sex chromosomes in mealworm beetles).",
             STYLE + "Split period scene: on the left in 1879 Kiel, Walther Flemming sketches crimson-stained salamander chromosomes splitting lengthwise under his brass microscope; on the right in 1905 Bryn Mawr, Nettie Maria Stevens compares paired XX and unequal XY mealworm chromosomes beside Walter Sutton and Theodor Boveri." + QUAL_TAIL,
             {"kind": "FACT", "label": "46 chromosomes in 23 pairs", "who_card": "Edouard van Beneden (1846–1910) — Belgian embryologist and cytologist", "when_stamp": "1879 · 1882 · 1883 · 1888 · 1902 · 1903 · 1905", "timeline_step": "1/3 · 1879–1905 (Flemming discovers mitosis; van Beneden discovers meiosis; Boveri & Sutton propose the Chromosome Theory; Nettie Stevens discovers X and Y sex chromosomes)", "hold_s": 3.8}),
            ("02_flemming_1882_mitosis_sutton_1903_meiosis_and_nettie_stevens_1905_xy_karyotype_chart", 79.5, 8.0, "E", False, "1882 FLEMMING MITOSIS (2N = 46) VS 1903 SUTTON MEIOSIS (2N → N = 23) & 1905 NETTIE STEVENS XX/XY SEX CHROMOSOMES", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked Walther Flemming (1882 Zellsubstanz, Kern und Zelltheilung) salamander mitosis phases (prophase, metaphase, anaphase, telophase keeping 2n = 46 constant) vs Walter Sutton (1903 Biol. Bull. 4: 231–251) grasshopper meiosis reduction division (2n → n = 23) & Nettie Stevens (1905 Carnegie Inst. Wash. Publ. 36) XX/XY sex chromosome karyotype chart.",
             {"kind": "DATA", "label": "1882 FLEMMING MITOSIS (2N=46), 1903 SUTTON MEIOSIS (N=23) & 1905 STEVENS XX/XY SEX DETERMINATION", "detail": "Inked Walther Flemming (1882 Zellsubstanz, Kern und Zelltheilung) salamander mitosis phases (prophase, metaphase, anaphase, telophase keeping 2n = 46 constant) vs Walter Sutton (1903 Biol. Bull. 4: 231–251) grasshopper meiosis reduction division (2n → n = 23) & Nettie Stevens (1905 Carnegie Inst. Wash. Publ. 36) XX/XY sex chromosome karyotype chart on period paper", "scale": "mitosis is like photocopying a forty-six-volume encyclopaedia so two libraries get the exact same set — while meiosis shuffles your mother's twenty-three volumes with your father's twenty-three volumes to print a brand-new twenty-three-volume edition for every egg or sperm", "hold_s": 3.8}),
            ("03_bryn_mawr_1905_camera_lucida_mealworm_xy_drawings_and_microscope_slides_closeup", 87.5, 6.5, "B", False, "1905 — NETTIE STEVENS DISCOVERS X AND Y", "Fast",
             "Fast: daylight macro shot of Nettie Stevens's 1905 camera-lucida ink drawings of mealworm beetle chromosomes (20 equal chromosomes in the female vs 19 large and 1 tiny Y chromosome in the male) beside stained glass slides and a brass microscope on a bench. Nothing emissive, no face.",
             STYLE + "In crisp daylight on a 1905 Bryn Mawr laboratory bench, pen-and-ink chromosome plates and stained glass slides sit beside a brass microscope and camera-lucida prism." + FAST_TAIL,
             None),
            ("04_sculpted_mitotic_spindle_and_paired_x_and_y_chromosome_models_on_oak_table_pan", 94.0, 5.5, "C", False, "MITOSIS, MEIOSIS & SEX DETERMINATION", "Fast",
             "Fast: daylight close-up pan across a sculpted wooden-and-brass model of mitotic sister chromatids separating on spindle fibres beside a large X and small Y chromosome pair on an oak table. Nothing emissive, no face.",
             STYLE + "In bright window light on an oak table, a sculpted model shows crimson sister chromatids separating along brass spindle rods beside a paired large X and small Y chromosome model." + FAST_TAIL,
             None),
        ],
    ),
    (
        3,
        "Part 03 — May 1910: Sceptic Thomas Hunt Morgan & the One White-Eyed Fruit Fly That Proved Him Wrong — Midpoint Twist",
        [
            ("01_thomas_hunt_morgan_may_1910_columbia_fly_room_spotting_white_eyed_male_drosophila", 99.5, 6.5, "A", False, "ALL 782 WHITE-EYED FLIES WERE MALE", "Quality",
             "Quality: readable face (American evolutionary biologist Thomas Hunt Morgan in Room 613 of Columbia University's Schermerhorn Hall in May–July 1910 holding a jeweller's loupe to a glass milk bottle where one snow-white-eyed male Drosophila melanogaster sits among hundreds of brick-red-eyed flies, then counting 3,470 red-eyed and 782 exclusively male white-eyed F2 grandchildren).",
             STYLE + "In Columbia University's 1910 Fly Room, Thomas Hunt Morgan peers through a brass hand lens at a glass milk bottle where a single white-eyed male fruit fly stands among red-eyed flies." + QUAL_TAIL,
             {"kind": "FACT", "label": "All 782 white-eyed flies were male", "when_stamp": "1909 · May 1910 · 22 July 1910", "timeline_step": "2/3 · May – 22 Jul 1910 (Thomas Hunt Morgan discovers the white-eyed male Drosophila and proves X-linked chromosome inheritance)", "hold_s": 3.8}),
            ("02_morgan_22_jul_1910_science_x_linked_white_eye_punnett_and_f2_count_chart", 106.0, 8.0, "E", False, "22 JUL 1910 MORGAN (SCIENCE): F2 SEX-LINKED CROSS = 2,459 RED FEMALES, 1,011 RED MALES, 782 WHITE MALES & 0 WHITE FEMALES", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked Thomas Hunt Morgan (22 July 1910 Science 32: 120–122) X-linked white-eye Drosophila cross Punnett diagram & F2 count chart (2,459 red females, 1,011 red males, 782 white males, 0 white females).",
             {"kind": "DATA", "label": "22 JUL 1910 MORGAN (SCIENCE): 2,459 RED FEMALES, 1,011 RED MALES, 782 WHITE MALES & 0 WHITE FEMALES (X-LINKED PROOF)", "detail": "Inked Thomas Hunt Morgan (22 July 1910 Science 32: 120–122) X-linked white-eye Drosophila cross Punnett diagram & F2 count chart (2,459 red females, 1,011 red males, 782 white males, 0 white females) on period paper", "scale": "because a male only has one X chromosome with no backup copy on his tiny Y chromosome, a recessive mutation on the X chromosome is like flying a single-engine plane — if that one engine sputters, you see it straight away, whereas a female flies with twin X engines", "hold_s": 3.8}),
            ("03_columbia_1910_milk_bottles_etheriser_funnel_and_porcelain_fly_counting_plate_closeup", 114.0, 6.5, "B", False, "22 JULY 1910 — SEX-LINKED CHROMOSOME INHERITANCE", "Fast",
             "Fast: daylight macro shot of cotton-stoppered glass milk bottles, a small glass etheriser bottle, a camel-hair sorting brush, and a white porcelain counting plate on a Fly Room bench. Nothing emissive, no face.",
             STYLE + "In crisp daylight on a 1910 Columbia laboratory bench, cotton-stoppered glass milk bottles sit beside a fine camel-hair brush, a brass hand lens, and a white porcelain sorting plate." + FAST_TAIL,
             None),
            ("04_sculpted_drosophila_four_chromosome_pair_karyotype_model_on_oak_table_pan", 120.5, 5.5, "C", False, "WHITE-EYE GENE ON THE X CHROMOSOME", "Fast",
             "Fast: daylight close-up pan across a sculpted model of the four chromosome pairs of Drosophila melanogaster showing the rod-like X chromosome with its white-eye locus beside the hooked Y chromosome on an oak table. Nothing emissive, no face.",
             STYLE + "In bright window light on an oak table, a sculpted chromosome model shows the four chromosome pairs of the fruit fly, highlighting the X chromosome with a white marker band beside the hooked Y chromosome." + FAST_TAIL,
             None),
        ],
    ),
    (
        4,
        "Part 04 — 1909–January 1913: Frans Janssens's Chiasmata & 19-Year-Old Alfred Sturtevant's All-Nighter Genetic Map",
        [
            ("01_frans_janssens_1909_chiasmata_sturtevant_jan_1913_all_nighter_map_and_mcclintock_1931", 126.0, 6.5, "A", False, "FIRST GENE MAP BY A 19-YEAR-OLD", "Quality",
             "Quality: readable faces (Belgian cytologist Frans Alfons Janssens in Louvain in 1909 observing X-shaped meiotic chiasmata, dissolving to 19-year-old Columbia undergraduate Alfred Henry Sturtevant in 1911–January 1913 calculating his six-gene linear crossover map and Barbara McClintock in August 1931 confirming physical crossover in maize chromosomes).",
             STYLE + "Split period scene: on the left, Frans Janssens in 1909 Belgium and Barbara McClintock in 1931 Cornell examine crossed-over chromosomes under microscopes; on the right in 1911–1913 New York, nineteen-year-old Alfred Sturtevant plots six genes along a straight line at his desk." + QUAL_TAIL,
             {"kind": "FACT", "label": "First gene map by a 19-year-old", "who_card": "Frans Alfons Janssens (1863–1924) — Belgian Catholic priest and cell biologist · Barbara McClintock (1902–1992) — American cytogeneticist", "when_stamp": "1909 · 1911 · January 1913 · August 1931 · 1933", "timeline_step": "3/3 · 1909, Jan 1913 & Aug 1931 (Janssens discovers chiasmata; 19-year-old Alfred Sturtevant publishes the first linear chromosome map; Creighton & McClintock prove physical crossover)", "hold_s": 3.8}),
            ("02_janssens_1909_chiasmata_and_sturtevant_jan_1913_six_gene_linear_chromosome_map_chart", 132.5, 8.0, "E", False, "1909 JANSSENS (LA CELLULE: CHIASMATYPE) & JAN 1913 STURTEVANT (J. EXP. ZOOL.): 6-GENE LINEAR MAP (0.0 → 1.0 → 30.7 → 33.7 → 57.6 CM)", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked Frans Janssens (1909 La Cellule 25: 387–486) meiotic chiasma crossover diagram & Alfred Sturtevant (January 1913 J. Exp. Zool. 14: 43–59) additive linear map of 6 X-linked Drosophila genes (B/yellow = 0.0, C/white = 1.0, O/vermilion = 30.7, P/miniature = 33.7, R/rudimentary = 57.6).",
             {"kind": "DATA", "label": "1909 JANSSENS CHIASMATA & JAN 1913 STURTEVANT ADDITIVE 6-GENE LINEAR X-CHROMOSOME MAP (1% CROSSOVER = 1 CENTIMORGAN)", "detail": "Inked Frans Janssens (1909 La Cellule 25: 387–486) meiotic chiasma crossover diagram & Alfred Sturtevant (January 1913 J. Exp. Zool. 14: 43–59) additive linear map of 6 X-linked Drosophila genes (B/yellow = 0.0, C/white = 1.0, O/vermilion = 30.7, P/miniature = 33.7, R/rudimentary = 57.6) on period paper", "scale": "Alfred Sturtevant mapped invisible genes the way you could map stations on an underground train line with your eyes closed — just by counting how often a random power cut stops the train between any two stations", "hold_s": 3.8}),
            ("03_columbia_1913_sturtevant_journal_of_experimental_zoology_linear_map_and_index_cards_closeup", 140.5, 6.5, "B", False, "JANUARY 1913 — FIRST LINEAR GENETIC MAP", "Fast",
             "Fast: daylight macro shot of Alfred Sturtevant's January 1913 Journal of Experimental Zoology paper open to the linear six-gene map beside stacks of handwritten fly-cross ledger cards and a brass slide rule on a desk. Nothing emissive, no face.",
             STYLE + "In crisp daylight on a 1913 study desk, an open biology journal displaying a horizontal chromosome line sits beside stacks of handwritten breeding ledger cards and a brass slide rule." + FAST_TAIL,
             None),
            ("04_explorer_aligning_three_gene_tokens_on_additive_centimorgan_ruler_at_desk", 147.0, 5.5, "B", True, None, "Quality",
             "Quality: Explorer beat 2 (locked character reference).",
             STYLE + "Sitting at a wooden desk beside a long brass ruler, the Explorer slides three coloured gene tokens into place along a single straight track, locking the short one-unit gap and the longer thirty-two-unit gap together so they add up to the exact total span." + EXP_TAIL,
             None),
        ],
    ),
    (
        5,
        "Part 05 — From the Fly Room to the Human Genome Project — & Why Your Heart Beats 100,000 Times a Day All by Itself",
        [
            ("01_timeline_1879_1956_and_tjio_levan_46_human_karyotype_genome_map_chart", 152.5, 8.5, "E", False, "1879–1956 TIMELINE · FLEMMING MITOSIS, BOVERI/SUTTON, STEVENS XX/XY, MORGAN/STURTEVANT FLY ROOM & TJIO/LEVAN 46 HUMAN CHROMOSOMES", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, the 3-era timeline completes: 1879–1883 (Walther Flemming stains salamander chromosomes to discover chromatin and mitosis in Kiel; Edouard van Beneden discovers chromosome halving in meiosis) · 1902–1905 (Theodor Boveri and Walter Sutton propose the Chromosome Theory of Inheritance; Nettie Stevens discovers X and Y sex chromosomes in mealworm beetles) · May 1910 – Jan 1913 (Thomas Hunt Morgan discovers X-linked inheritance in a white-eyed male Drosophila at Columbia; 19-year-old Alfred Sturtevant publishes the first linear chromosome map, winning Morgan the 1933 Nobel Prize).",
             {"kind": "DATA", "label": "1879–1956 CHROMOSOME & GENE-MAPPING TIMELINE · FLEMMING, SUTTON/BOVERI, STEVENS, MORGAN, STURTEVANT & TJIO/LEVAN (2N=46)", "detail": "Animated timeline (1879 → 1956) alongside Tjio & Levan (1956 Hereditas 42: 1–6) 46-chromosome human karyotype (22 autosome pairs + XX/XY) and Sturtevant's centimorgan genetic map", "scale": "from aniline fabric dye on salamander gills in Germany to rotting bananas in New York milk bottles, scientists proved that our entire hereditary blueprint rides on forty-six microscopic threads", "when_stamp": "1879–1933 · 1956", "timeline_step": "3/3 · 1879–1933 timeline complete", "hold_s": 3.8}),
            ("02_human_46_chromosome_karyotype_board_beside_columbia_milk_bottle_on_plinth_pan", 161.0, 5.5, "A", False, "46 HUMAN CHROMOSOMES MAPPED", "Fast",
             "Fast: daylight close-up of a sculpted 23-pair human chromosome karyotype display board beside a vintage glass Drosophila milk bottle on a wooden museum plinth. Nothing emissive, no face.",
             STYLE + "In crisp daylight on a wooden museum plinth, a relief display board of twenty-three paired human chromosomes sits beside a vintage glass milk bottle." + FAST_TAIL,
             None),
            ("03_ringer_1882_tap_water_einthoven_1901_string_galvanometer_keith_flack_1906_sa_node_and_greatbatch_1958_pacemaker_handoff", 166.5, 6.5, "C", False, "THE HEART, THE ECG & THE PACEMAKER", "Quality",
             "Quality: readable faces (Sidney Ringer in London in 1882–1883 testing tap water on an isolated heart, Willem Einthoven in Leiden in 1901–1903 operating his 600-pound string galvanometer ECG, Arthur Keith and Martin Flack in Kent in 1906, and Wilson Greatbatch in Buffalo on 7 May 1958 with his wrong-resistor implantable pacemaker — handoff to 076 The Heart, the ECG & the Pacemaker).",
             STYLE + "Split period scene: on the left, Sidney Ringer in 1882 London and Willem Einthoven in 1903 Leiden beside his water-cooled string galvanometer and salt-water limb buckets; on the right, Arthur Keith and Martin Flack in 1906 Kent alongside Wilson Greatbatch in 1958 Buffalo holding his two-cubic-inch epoxy pacemaker." + QUAL_TAIL,
             {"kind": "WHEN", "label": "1882 · 1901 · 1906 · 1958", "hold_s": 3.5}),
            ("04_table_three_callback", 173.0, 2.4, "C", False, None, "reuse",
             "Reuse: verified unused moving window [5.50s..7.90s] of P1:07_table_three_props_1879_flemming_stained_slide_1910_morgan_milk_bottle_and_1913_sturtevant_map_ruler (callback, £0).",
             "Reuse P1:07_table_three_props_1879_flemming_stained_slide_1910_morgan_milk_bottle_and_1913_sturtevant_map_ruler [5.50s..7.90s] (2.40s distinct non-overlapping tail window from 8.00s source clip).",
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
                row["reuse_of"] = "P1:07_table_three_props_1879_flemming_stained_slide_1910_morgan_milk_bottle_and_1913_sturtevant_map_ruler"
                row["reuse_window_s"] = [5.5, 7.9]
                row["reuse_audit"] = {
                    "source_row": "P1:07_table_three_props_1879_flemming_stained_slide_1910_morgan_milk_bottle_and_1913_sturtevant_map_ruler",
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
            "film": "075_Flemming-Boveri-Sutton-Stevens-Morgan-Chromosomes-Mitosis",
            "part": p_idx,
            "title": p_title,
            "version": "v01",
            "timing_status": "pre_vo_script_clock (built from chromosomes_script_master_v01.md; retimes onto Scribe STT once VO locks)",
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
        "film": "075_Flemming-Boveri-Sutton-Stevens-Morgan-Chromosomes-Mitosis",
        "version": "v01",
        "date": "2026-10-20",
        "owner": "gemini (J0706)",
        "status": "PRE_VO_BOARDS_V01_NO_MINT",
        "generation_authorized": False,
        "script": "00_Brand/Channel-Setup/ideas/075_Flemming-Boveri-Sutton-Stevens-Morgan-Chromosomes-Mitosis/chromosomes_script_master_v01.md",
        "sources": "00_Brand/Channel-Setup/ideas/075_Flemming-Boveri-Sutton-Stevens-Morgan-Chromosomes-Mitosis/SOURCES_v01.md",
        "credit_snapshot": {
            "flow_balance": 23740,
            "flow_floor": 0,
            "flow_read_at": "2026-10-15T21:42:22Z",
            "vertex_promo_gbp": 71.02,
            "vertex_usable_gbp": 70.02,
        },
        "totals": totals,
        "per_part": per_part_summary,
        "mint_order": "006 > 007 > 008 > 009 > 010 > 011 > 012 > 013 > 014 > 015 > 016 > 017 > 018 > 019 > 020 > 021 > 022 > 023 > 024 > 025 > 026 > 027 > 028 > 029 > 030 > 031 > 032 > 033 > 034 > 035 > 036 > 037 > 038 > 039 > 040 > 041 > 042 > 043 > 044 > 045 > 046 > 047 > 048 > 049 > 050 > 051 > 052 > 053 > 054 > 055 > 056 > 057 > 058 > 059 > 060 > 061 > 062 > 063 > 064 > 065 > 066 > 067 > 068 > 069 > 070 > 071 > 072 > 073 > 074 > 075 > 076 > 077. Nothing in 075 is generation_authorized.",
    }
    (EDIT / "PICTURE_PLAN_v01.json").write_text(json.dumps(plan, indent=2) + "\n")

    sl = [
        "# 075 Chromosomes: How One White-Eyed Fly Mapped DNA — Shot list & plate boards v01 (pre-VO)",
        "",
        "Gemini, 20 Oct 2026, J0706. Built from `chromosomes_script_master_v01.md` (`91.9/100 PASS`) and `SOURCES_v01.md`.",
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
        "# 075 price review v01 (pre-VO plate boards)",
        "",
        "Gemini, 20 Oct 2026, J0706. Boards only. **No mint. No spend. No merge.**",
        "Prepared from `chromosomes_script_master_v01.md` (`91.9/100 PASS`) and `SOURCES_v01.md` so 075's full plate board rows, non-emissive Fast prompts, £0 code graphics, and Teach-on-Screen overlays are ready to re-time the moment long VO locks. Parked for Chief.",
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
        f"- **Quality ({totals['Quality']} rows):** readable faces (Walther Flemming, Edouard van Beneden, Theodor Boveri, Walter Sutton, Nettie Maria Stevens, Thomas Hunt Morgan, Frans Alfons Janssens, Alfred Henry Sturtevant, Barbara McClintock, Sidney Ringer, Willem Einthoven, Arthur Keith, Martin Flack, Wilson Greatbatch), 1879 Kiel salamander mitosis & 1905 Bryn Mawr `XX/XY` sex chromosomes, May–July 1910 Columbia Fly Room white-eyed *Drosophila*, January 1913 Sturtevant six-gene linear chromosome map, and the 2 Explorer beats.",
        f"- **Fast ({totals['Fast']} rows, non-emissive):** daylight prop and laboratory shots (1882 Flemming *Zellsubstanz* lithograph, aniline dye bottle & 1910 *Science* offprint pan, 3-object callback bench, 1905 Bryn Mawr camera-lucida mealworm drawings & slides, sculpted mitotic spindle & `X/Y` chromosome models, Columbia Fly Room milk bottles with brush & sorting plate, sculpted *Drosophila* 4-pair chromosome model, January 1913 *J. Exp. Zool.* map & index cards, 23-pair human karyotype display board beside milk bottle on museum plinth). Zero candles, flames, sparks, or glowing elements on Fast.",
        f"- **£0 code graphics ({totals['code_graphic']} rows):**",
        "  1. `P1:04_flemming_1879_sutton_1903_stevens_1905_morgan_1910_and_sturtevant_1913_chromosome_chart` — diploid mitosis (`2n = 46 → 46 + 46`) vs haploid meiosis (`2n = 46 → 4 × 23`), `XX/XY` sex chromosomes, and Sturtevant's `1913` centimorgan gene map (`SCALE: packing two metres of DNA into forty-six microscopic chromosomes inside a cell nucleus six micrometres wide is like winding forty kilometres of ultra-fine sewing thread into forty-six neat bobbins inside a walnut shell — and then splitting every bobbin in half without a single knot`)",
        "  2. `P1:06_morgan_22_jul_1910_science_white_eye_cross_and_sturtevant_jan_1913_six_gene_map_chart` — Thomas Hunt Morgan (22 July 1910 *Science*) `3,470` red : `782` white-eyed male F₂ cross & Alfred Sturtevant (January 1913 *J. Exp. Zool.*) 6-gene linear X-chromosome map (`SCALE: Alfred Sturtevant realized that chromosomes swap pieces at random like two beaded necklaces tangling in a drawer — so if two beads get separated ten times more often than two others, they must sit ten times farther apart along the string`)",
        "  3. `P2:02_flemming_1882_mitosis_sutton_1903_meiosis_and_nettie_stevens_1905_xy_karyotype_chart` — Walther Flemming (1882) salamander mitosis phases, Walter Sutton (1903) grasshopper meiosis, and Nettie Stevens (1905) `XX/XY` sex chromosome karyotype (`SCALE: mitosis is like photocopying a forty-six-volume encyclopaedia so two libraries get the exact same set — while meiosis shuffles your mother's twenty-three volumes with your father's twenty-three volumes to print a brand-new twenty-three-volume edition for every egg or sperm`)",
        "  4. `P3:02_morgan_22_jul_1910_science_x_linked_white_eye_punnett_and_f2_count_chart` — Thomas Hunt Morgan (22 July 1910 *Science*) X-linked white-eye Punnett square & F₂ count (`2,459` red females, `1,011` red males, `782` white males, `0` white females) (`SCALE: because a male only has one X chromosome with no backup copy on his tiny Y chromosome, a recessive mutation on the X chromosome is like flying a single-engine plane — if that one engine sputters, you see it straight away, whereas a female flies with twin X engines`)",
        "  5. `P4:02_janssens_1909_chiasmata_and_sturtevant_jan_1913_six_gene_linear_chromosome_map_chart` — Frans Janssens (1909 *La Cellule*) meiotic chiasmata & Alfred Sturtevant (January 1913 *J. Exp. Zool.*) additive 6-gene linear map (`0.0 → 1.0 → 30.7 → 33.7 → 57.6 cM`) (`SCALE: Alfred Sturtevant mapped invisible genes the way you could map stations on an underground train line with your eyes closed — just by counting how often a random power cut stops the train between any two stations`)",
        "  6. `P5:01_timeline_1879_1956_and_tjio_levan_46_human_karyotype_genome_map_chart` — completed timeline (1879 → 1956) + Tjio & Levan (1956) `46` human chromosomes & Human Genome Project linkage map (`SCALE: from aniline fabric dye on salamander gills in Germany to rotting bananas in New York milk bottles, scientists proved that our entire hereditary blueprint rides on forty-six microscopic threads`)",
        f"- **£0 verified reuse ({totals['reuse']} row):** `P5:04_table_three_callback` uses the 2.40 s unused moving tail `[5.50s..7.90s]` of `P1:07_table_three_props_1879_flemming_stained_slide_1910_morgan_milk_bottle_and_1913_sturtevant_map_ruler`.",
        "",
        "## Mint order",
        "",
        "006 > 007 > 008 > 009 > 010 > 011 > 012 > 013 > 014 > 015 > 016 > 017 > 018 > 019 > 020 > 021 > 022 > 023 > 024 > 025 > 026 > 027 > 028 > 029 > 030 > 031 > 032 > 033 > 034 > 035 > 036 > 037 > 038 > 039 > 040 > 041 > 042 > 043 > 044 > 045 > 046 > 047 > 048 > 049 > 050 > 051 > 052 > 053 > 054 > 055 > 056 > 057 > 058 > 059 > 060 > 061 > 062 > 063 > 064 > 065 > 066 > 067 > 068 > 069 > 070 > 071 > 072 > 073 > 074 > 075 > 076 > 077. `generation_authorized` is `false` on every row.",
    ])
    (EDIT / "PRICE_REVIEW_v01.md").write_text("\n".join(pr_lines) + "\n")
    print(f"075 v01 boards written: {totals['rows']} rows, Flow expected={totals['flow_credits_expected']}")


if __name__ == "__main__":
    main()
