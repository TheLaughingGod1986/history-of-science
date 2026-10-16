#!/usr/bin/env python3
"""HOS 067 (Hox Genes: The Hidden Map That Built Your Body) pre-VO plate boards v01. J0661. No mint, no spend.

Built from 00_Brand/Channel-Setup/ideas/067_Driesch-Mangold-Spemann-Lewis-Gehring-Embryo-Hox-Genes/embryo_script_master_v01.md
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
        "Part 01 — The Blonde Baby Hair in Freiburg & the 180-Letter Map Inside Every Embryo",
        [
            ("01_fertilised_egg_dividing_into_striped_embryo_with_colinear_hox_chromosome_blocks", 0.0, 5.5, "A", False, "ONE CELL TO A HUMAN BODY", "Quality",
             "Quality: Short frame 0 / answer image (0:03) + a single fertilised egg cell divides into a hollow sphere and then a striped embryo as colour-coded Hox gene blocks (red head, gold thorax, blue abdomen and limbs) click into exact head-to-tail order along the chromosome and across the developing body.",
             STYLE + "Split embryonic-and-genetic scene: on the left, a single translucent egg cell divides into a segmented embryo painted with red head, gold thorax, and blue abdomen stripes; on the right, matching red, gold, and blue Hox blocks align in the exact same head-to-tail order along a chromosome track." + QUAL_TAIL,
             {"kind": "WHEN", "label": "NAPLES, 1891", "timeline_step": "1/3 · 1891 & May 1921 (Hans Driesch shakes 2-cell sea-urchin embryos into identical twins in Naples; Hilde Mangold & Hans Spemann discover the embryonic Organizer in Freiburg)", "hold_s": 3.5}),
            ("02_driesch_1891_mangold_spemann_1921_lewis_nusslein_volhard_wieschaus_1978_1980_and_gehring_1984_split", 5.5, 6.0, "B", False, "THE ORGANIZER, FOUR-WINGED FLY, HOMEOBOX", "Quality",
             "Quality: complex three-part composition (Hans Driesch in Naples in 1891 shaking a two-cell sea-urchin embryo alongside Hilde Mangold and Hans Spemann in Freiburg in May 1921 grafting a newt embryo with a fine blond hair loop; Edward B. Lewis at Caltech in December 1978 examining a four-winged Ultrabithorax fruit fly alongside Christiane Nüsslein-Volhard and Eric Wieschaus in Heidelberg in October 1980; and Matthew Scott and Walter Gehring in 1984–1995 revealing the 180-bp Homeobox and Pax6 eye switch).",
             STYLE + "Three-panel period composition: on the left, Hans Driesch in 1891 Naples with sea-urchin twins alongside Hilde Mangold and Hans Spemann in 1921 Freiburg grafting a newt embryo with a blond hair loop; in the centre, Edward Lewis in 1978 Pasadena with a four-winged fruit fly alongside Christiane Nüsslein-Volhard and Eric Wieschaus at a dual microscope; on the right, Matthew Scott and Walter Gehring inspecting Homeobox DNA gels." + QUAL_TAIL,
             None),
            ("03_human_skeleton_cervical_thoracic_lumbar_vertebrae_aligned_with_colinear_hox_chromosome_clusters", 11.5, 6.0, "C", False, "THE HEAD-TO-TAIL GPS MAP", "Quality",
             "Quality: complex conceptual and anatomical reveal (a sculpted human skeleton highlights its cervical, thoracic, and lumbar vertebrae alongside the four matching colinear human HOX gene clusters lined up in the exact same head-to-tail sequence on the chromosomes).",
             STYLE + "Split anatomical-and-chromosome scene: on the left, an articulated anatomical skeleton model highlights its red neck vertebrae, gold rib-bearing chest vertebrae, and blue lower-back vertebrae; on the right, four parallel chromosome rods display red, gold, and blue HOX gene blocks in the exact same head-to-tail sequence." + QUAL_TAIL,
             {"kind": "WHEN", "label": "1891 · MAY 1921 · 7 DECEMBER 1978 · 30 OCTOBER 1980 · 1984", "timeline_step": "1/3 · 1891 & May 1921 (Driesch; Mangold & Spemann) · 2/3 · Dec 1978 & Oct 1980 (Lewis; Nüsslein-Volhard & Wieschaus) · 3/3 · 1984 & Mar 1995 (Scott & Gehring Homeobox & Pax6)", "hold_s": 3.5}),
            ("04_lewis_1978_nusslein_volhard_wieschaus_1980_scott_gehring_1984_hox_colinearity_chart", 17.5, 8.0, "E", False, "8 FRUIT-FLY HOX GENES VS 39 HUMAN HOX GENES (4 CLUSTERS): 180-BP HOMEOBOX (60-AA HOMEODOMAIN) IN HEAD-TO-TAIL COLINEAR ORDER", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked Hox Gene Colinearity & Embryonic Body-Plan chart from Spemann & Mangold (1924 Arch. Mikr. Anat. Entw. 100: 599–638), Lewis (7 December 1978 Nature 276: 565–570), Nüsslein-Volhard & Wieschaus (30 October 1980 Nature 287: 795–801), and Scott & Weiner / McGinnis, Levine, Hafen, Kuroiwa & Gehring (March–July 1984 Nature 308: 428–433 & PNAS 81: 4115–4119) aligns the 8 Drosophila Hox genes along chromosome 3 with the 39 human HOX genes across 4 clusters (HOXA, HOXB, HOXC, HOXD), showing 3'-to-5' chromosomal order matching anterior-to-posterior (head-to-tail) expression driven by the conserved 180-bp homeobox (60-amino-acid homeodomain).",
             {"kind": "DATA", "label": "COLINEAR HOX ARCHITECT GENES: 8 FLY HOX GENES ↔ 39 HUMAN HOX GENES (4 CLUSTERS) SHARING THE 180-BP HOMEOBOX IN HEAD-TO-TAIL ORDER", "detail": "Inked chromosomal colinearity chart on period paper comparing the 8 fruit-fly homeotic genes (lab, pb, Dfd, Scr, Antp, Ubx, abd-A, Abd-B) and the 39 mammalian/human HOX genes (4 clusters), all sharing the conserved 180-base-pair homeobox (60-amino-acid DNA-binding homeodomain) and arranged along the chromosome in the exact head-to-tail order of the body segments they build", "scale": "your body's master architect genes are lined up along your chromosome like stations on a railway line — the genes at the front of the DNA strand build your head and neck, the middle genes build your chest and ribs, and the genes at the end build your lower back and limbs", "who_card": "Hans Driesch (1867–1941) — German experimental embryologist · Hilde Mangold (1898–1924) — German embryologist · Hans Spemann (1869–1941) — German embryologist · Edward B. Lewis (1918–2004) — American developmental geneticist · Christiane Nüsslein-Volhard (born 1942) — German developmental geneticist · Eric F. Wieschaus (born 1947) — American developmental biologist · Matthew P. Scott (born 1953) — American developmental geneticist · Walter J. Gehring (1939–2014) — Swiss developmental biologist", "when_stamp": "1891 · May 1921 · 7 December 1978 · 30 October 1980 · 1984", "hold_s": 3.8}),
            ("05_wax_dissecting_dish_blond_hair_loop_glass_needle_and_hox_block_model_pan", 25.5, 5.5, "A", False, "STATIONS ON A RAILWAY LINE", "Fast",
             "Fast: daylight macro pan across a 1921 wax-lined glass dissecting dish, a fine glass micro-needle holding a tiny loop of blond hair, and a colour-coded wooden Hox gene block bar on an oak bench between code graphics so two full-frame graphics never run back to back. Nothing emissive, no face.",
             STYLE + "In crisp daylight on an oak embryology bench, the camera pans smoothly across a wax-lined glass dissecting dish, a fine glass pipette with a tiny blond hair loop, and a row of red, gold, and blue wooden Hox blocks." + FAST_TAIL,
             None),
            ("06_spemann_mangold_may_1921_1924_organizer_dorsal_lip_chimera_um132_chart", 31.0, 8.0, "E", False, "THE SPEMANN-MANGOLD ORGANIZER", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period parchment, an inked Spemann-Mangold Dorsal Blastopore Lip Transplant diagram (from Spemann & Mangold 1924 Arch. Mikr. Anat. Entw. 100: 599–638, embryo 1921 Um 132) shows a tiny unpigmented graft from Triton cristatus transplanted onto the ventral flank of a dark Triton taeniatus host embryo, inducing >80% dark host belly cells to fold into a complete secondary neural tube, notochord, somites, and twin head.",
             {"kind": "DATA", "label": "MAY 1921 SPEMANN & MANGOLD ORGANIZER (EMBRYO UM 132): PALE DORSAL LIP GRAFT RECRUITS >80% DARK HOST BELLY CELLS INTO TWIN SPINE", "detail": "Inked Spemann-Mangold (May 1921 / 1924 Arch. Mikr. Anat. Entw. 100: 599–638) chimera cross-section showing unpigmented donor organizer cells (dorsal blastopore lip) recruiting >80% pigmented host ventral ectoderm cells into a secondary brain and spinal cord", "scale": "transplanting a speck of organizer tissue smaller than a pinhead onto an embryo's belly is like dropping a conductor onto a building site — it orders the surrounding skin cells to stop making belly skin and build a second brain and spine instead", "hold_s": 3.8}),
            ("07_table_three_props_1891_sea_urchin_tube_1921_hair_loop_dish_and_1978_four_winged_fly_model", 39.0, 5.5, "C", False, "1891 TO 1995", "Fast",
             "Fast: daylight prop table (callback source for Part 05: Hans Driesch's 1891 stoppered glass seawater tube, Hilde Mangold's 1921 wax dish with a glass baby-hair loop tool, and Edward Lewis's 1978 four-winged fruit-fly brass model). Nothing emissive.",
             STYLE + "On an oak workbench in soft window light sit three objects side by side: a stoppered glass tube of seawater, a wax-lined dish with a fine glass hair-loop microneedle, and a sculpted brass four-winged fruit fly model." + FAST_TAIL,
             None),
            ("08_explorer_flipping_ubx_thorax_railway_switch_on_chromosome_track_for_four_winged_fly", 62.0, 5.5, "A", True, None, "Quality",
             "Quality: Explorer beat 1 (locked character reference, after 1:00).",
             STYLE + "Standing beside a brass railway signal box along a chromosome track of red, gold, and blue stations, the Explorer pulls a polished brass switch lever at the middle thorax station as a sculpted fruit-fly model unfolds a gleaming second pair of wings." + EXP_TAIL,
             None),
            ("09_hilde_mangold_may_1921_freiburg_grafting_newt_embryo_with_blond_baby_hair_loop", 67.5, 5.5, "B", False, "FREIBURG, MAY 1921", "Quality",
             "Quality: readable face (in Freiburg in May 1921, 22-year-old Hilde Mangold leans over her dissecting microscope, tightening a microscopic loop of fine blond baby hair around a newt embryo in a wax-lined dish).",
             STYLE + "In a sunlit 1921 Freiburg zoology laboratory, 22-year-old German embryologist Hilde Mangold peers through a brass binocular dissecting microscope while guiding a delicate glass needle tipped with a tiny loop of blond baby hair over a newt embryo dish." + QUAL_TAIL,
             {"kind": "WHEN", "label": "FREIBURG, MAY 1921", "timeline_step": "1/3 · May 1921 (Hilde Mangold & Hans Spemann transplant the newt dorsal blastopore lip in Freiburg and discover the embryonic Organizer)", "hold_s": 3.5}),
        ],
    ),
    (
        2,
        "Part 02 — 1891 & May 1921: Hans Driesch's Shaken Twins & Hilde Mangold's Blond Hair Loop (The Spemann-Mangold Organizer)",
        [
            ("01_hans_driesch_1891_naples_sea_urchin_twins_and_mangold_spemann_may_1921_freiburg_organizer", 73.0, 6.5, "A", False, "BELLY SKIN BECOMES A BRAIN", "Quality",
             "Quality: readable faces (German embryologist Hans Driesch in Naples in Spring 1891 shaking 2-cell sea-urchin embryos apart into complete twin larvae, dissolving to 22-year-old Hilde Mangold and Hans Spemann in Freiburg in May 1921 grafting the unpigmented dorsal blastopore lip onto a dark newt embryo).",
             STYLE + "Split period scene: on the left in 1891 Naples, Hans Driesch holds a glass tube of seawater showing two separated sea-urchin cells growing into complete twin larvae; on the right in May 1921 Freiburg, Hilde Mangold and Hans Spemann inspect a dark newt embryo growing a pale-induced twin neural tube." + QUAL_TAIL,
             {"kind": "FACT", "label": "Belly skin becomes a brain", "who_card": "Wilhelm Roux (1850–1924) — German anatomist and embryologist", "when_stamp": "1888 · 1891 · May 1921 · September 1924 · 1935", "timeline_step": "1/3 · 1891 & May 1921 (Hans Driesch's sea-urchin twin regulation + Hilde Mangold & Hans Spemann's Organizer transplant; 1935 Nobel Prize)", "hold_s": 3.8}),
            ("02_roux_1888_vs_driesch_1891_twins_and_spemann_mangold_1921_1924_chimera_chart", 79.5, 8.0, "E", False, "1891 DRIESCH (SHAKEN 2-CELL SEA URCHIN → 2 COMPLETE TWIN LARVAE) & MAY 1921 SPEMANN-MANGOLD (EMBRYO UM 132: >80% HOST BELLY CELLS FORM TWIN SPINE)", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked Roux (1888 hot-needle half-embryo) vs Driesch (1891 shaken 2-cell and 4-cell sea-urchin blastomere separation yielding 100% complete miniature pluteus larvae) and Spemann & Mangold (May 1921 / 1924 embryo Um 132) chimeric neural tube cell-origin chart shows pale donor organizer cells inducing dark host ventral belly cells to fold into a second neural tube, notochord, and twin head.",
             {"kind": "DATA", "label": "1891 DRIESCH (2 SEPARATED CELLS → 2 COMPLETE TWINS) & MAY 1921 MANGOLD-SPEMANN ORGANIZER (>80% HOST BELLY CELLS IN TWIN SPINE)", "detail": "Inked Roux (1888 hot-needle half-embryo) vs Driesch (1891 shaken 2-cell and 4-cell sea-urchin blastomere separation yielding 100% complete miniature pluteus larvae) and Spemann & Mangold (May 1921 / 1924 embryo Um 132) chimeric neural tube cell-origin chart on period paper", "scale": "Hilde Mangold's two-colour newt transplant worked like building a house out of white and black bricks — when the new twin spine appeared, over four-fifths of its bricks were black belly bricks that the tiny white organizer patch had recruited on the spot", "hold_s": 3.8}),
            ("03_freiburg_1921_microscope_slide_um132_and_blond_hair_loop_pipette_closeup", 87.5, 6.5, "B", False, "MAY 1921 — THE SPEMANN-MANGOLD ORGANIZER", "Fast",
             "Fast: daylight macro shot of histological slide Um 132 beside a fine glass pipette tipped with a blond baby-hair loop and a wax-lined embryo dish on a 1921 Freiburg bench. Nothing emissive, no face.",
             STYLE + "In crisp daylight on a 1921 wooden laboratory bench, a stained glass microscope slide sits beside a wax-lined dissecting dish and a delicate glass hair-loop micro-instrument." + FAST_TAIL,
             None),
            ("04_two_colour_white_and_dark_newt_embryo_graft_wax_models_pan", 94.0, 5.5, "C", False, "WHITE GRAFT · DARK HOST TWIN SPINE", "Fast",
             "Fast: daylight close-up pan across a sequence of three sculpted two-tone wax embryology models on an oak table showing a pale dorsal lip graft inducing a secondary neural groove in a dark host embryo. Nothing emissive, no face.",
             STYLE + "In bright window light on an oak bench, three vintage two-tone wax embryology models show a tiny pale graft on a dark sphere folding into a twin neural ridge." + FAST_TAIL,
             None),
        ],
    ),
    (
        3,
        "Part 03 — 7 December 1978 & 30 October 1980: Edward Lewis's Four-Winged Fruit Fly & Nüsslein-Volhard and Wieschaus's Striped Embryo Screen — Midpoint Twist",
        [
            ("01_edward_lewis_dec_1978_caltech_four_winged_fly_and_nusslein_volhard_wieschaus_oct_1980_embl", 99.5, 6.5, "A", False, "LEGS GROWING ON A FLY'S HEAD", "Quality",
             "Quality: readable faces (American geneticist Edward B. Lewis at Caltech on 7 December 1978 examining a four-winged Ultrabithorax Drosophila fruit fly, dissolving to Christiane Nüsslein-Volhard and Eric Wieschaus sitting face-to-face across a dual microscope at EMBL Heidelberg on 30 October 1980 screening 27,000 mutant fly lines).",
             STYLE + "Split period scene: on the left in December 1978 Pasadena, Edward Lewis examines a four-winged fruit fly under a stereomicroscope; on the right in October 1980 Heidelberg, Christiane Nüsslein-Volhard and Eric Wieschaus sit across a dual-headed microscope surrounded by glass fly vials." + QUAL_TAIL,
             {"kind": "FACT", "label": "Legs growing on a fly's head", "when_stamp": "1894 · 1915 · 7 December 1978 · 30 October 1980 · 1995", "timeline_step": "2/3 · 7 Dec 1978 & 30 Oct 1980 (Edward Lewis maps the colinear Bithorax complex; Christiane Nüsslein-Volhard & Eric Wieschaus map the 15 segmentation genes; 1995 Nobel Prize)", "hold_s": 3.8}),
            ("02_nusslein_volhard_wieschaus_30_oct_1980_and_lewis_7_dec_1978_nature_segmentation_hox_chart", 106.0, 8.0, "E", False, "30 OCT 1980 NÜSSLEIN-VOLHARD & WIESCHAUS (15 GENES: GAP → 7 PAIR-RULE → 14 SEGMENT-POLARITY STRIPES) & 7 DEC 1978 LEWIS (8 COLINEAR HOX SELECTORS)", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked Nüsslein-Volhard & Wieschaus (30 October 1980, Nature 287: 795–801) and Lewis (7 December 1978, Nature 276: 565–570) Drosophila segmentation hierarchy chart shows Maternal gradient (Bicoid anterior-to-posterior concentration curve) -> Gap genes -> Pair-rule 7-stripe genes -> 14 Segment-polarity stripes -> 8 Colinear Homeotic (Hox) selector genes.",
             {"kind": "DATA", "label": "1980 HEIDELBERG SCREEN (15 GENES: MATERNAL → GAP → 7 PAIR-RULE → 14 STRIPES) + 1978 LEWIS COLINEAR BITHORAX / HOX MAP", "detail": "Inked Nüsslein-Volhard & Wieschaus (30 October 1980, Nature 287: 795–801) and Lewis (7 December 1978, Nature 276: 565–570) Drosophila segmentation hierarchy chart on period paper showing Maternal gradient (Bicoid anterior-to-posterior concentration curve) -> Gap genes -> Pair-rule 7-stripe genes -> 14 Segment-polarity stripes -> 8 Colinear Homeotic (Hox) selector genes", "scale": "building a body from a single round egg is like painting a map on a blank globe — first a smooth gradient of maternal ink marks the North Pole as the head, then three waves of stencil genes divide the globe into fourteen numbered stripes, and finally each stripe reads its own Hox address code", "hold_s": 3.8}),
            ("03_heidelberg_1980_seven_stripe_embryo_slide_and_caltech_four_winged_fly_model_closeup", 114.0, 6.5, "B", False, "30 OCTOBER 1980 — THE EMBRYONIC STRIPE CASCADE", "Fast",
             "Fast: daylight macro shot of a stained 7-stripe pair-rule Drosophila embryo slide beside a sculpted four-winged Ultrabithorax fly model and rack of glass fly vials on a bench. Nothing emissive, no face.",
             STYLE + "In crisp daylight on a 1980 genetics bench, a stained seven-striped embryo microscope slide sits beside a sculpted four-winged fruit-fly model and a wooden rack of cotton-plugged glass vials." + FAST_TAIL,
             None),
            ("04_fourteen_numbered_embryo_segment_wooden_rings_and_colinear_chromosome_rod_pan", 120.5, 5.5, "C", False, "7 DECEMBER 1978 — COLINEAR BODY SEGMENTS", "Fast",
             "Fast: daylight close-up pan across a segmented wooden model of a 14-ring insect embryo aligned directly above a matching colour-coded chromosome bar on an oak table. Nothing emissive, no face.",
             STYLE + "In bright window light on an oak table, a fourteen-ring painted wooden embryo model sits parallel to a brass chromosome bar with matching red, gold, and blue slider blocks." + FAST_TAIL,
             None),
        ],
    ),
    (
        4,
        "Part 04 — March–July 1984 & 24 March 1995: The 180-Letter Homeobox & Why a Mouse Gene Builds an Eye on a Fruit Fly's Leg",
        [
            ("01_scott_weiner_mcginnis_levine_gehring_1984_homeobox_and_halder_gehring_24_mar_1995_pax6_eye", 126.0, 6.5, "A", False, "MOUSE GENE BUILDS A FLY EYE", "Quality",
             "Quality: readable faces (Matthew Scott, William McGinnis, and Walter Gehring in March–July 1984 discovering the conserved 180-bp Homeobox across flies, frogs, mice, and humans, dissolving to Georg Halder, Patrick Callaerts, and Walter Gehring on 24 March 1995 inducing a red compound fruit-fly eye on a fly's leg using the mouse Pax6 gene).",
             STYLE + "Split period scene: on the left in 1984 Bloomington and Basel, Matthew Scott, William McGinnis, and Walter Gehring inspect cross-species Southern blots showing the 180-letter Homeobox across flies and vertebrates; on the right in March 1995 Basel, Walter Gehring points to a red compound fruit-fly eye grown on a fly's leg by a mouse Pax6 gene." + QUAL_TAIL,
             {"kind": "FACT", "label": "Mouse gene builds a fly eye", "who_card": "William McGinnis (born 1952) — American molecular biologist", "when_stamp": "29 March 1984 · July 1984 · 24 March 1995", "timeline_step": "3/3 · Mar–Jul 1984 & 24 Mar 1995 (Scott, McGinnis, Levine & Gehring discover the 180-bp Homeobox across animals; Gehring's team induces a fly eye on a leg with mouse Pax6)", "hold_s": 3.8}),
            ("02_mcginnis_gehring_1984_cell_cross_species_homeobox_and_halder_gehring_1995_science_pax6_chart", 132.5, 8.0, "E", False, "MAR–JUL 1984 SCOTT & GEHRING (180-BP HOMEOBOX / 60-AA HOMEODOMAIN, >75–90% IDENTITY) & 24 MAR 1995 HALDER & GEHRING (MOUSE PAX6 INDUCES FLY COMPOUND EYE)", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked McGinnis, Garber, Wirz, Kuroiwa & Gehring (July 1984, Cell 38: 675–680) cross-species Southern blot & Halder, Callaerts & Gehring (24 March 1995, Science 267: 1788–1792) Pax6/eyeless ectopic eye-induction chart shows the 180-bp homeobox (60-aa homeodomain with >75–90% sequence identity between Drosophila and human HOX) and mouse Pax6 cDNA inducing compound eyes on Drosophila legs, wings, and antennae.",
             {"kind": "DATA", "label": "1984 HOMEOBOX (180 BP / 60 AA, >75–90% FLY–HUMAN IDENTITY) & 24 MAR 1995 MOUSE PAX6 → ECTOPIC DROSOPHILA EYE ON LEG", "detail": "Inked McGinnis, Garber, Wirz, Kuroiwa & Gehring (July 1984, Cell 38: 675–680) cross-species Southern blot & Halder, Callaerts & Gehring (24 March 1995, Science 267: 1788–1792) Pax6/eyeless ectopic eye-induction chart on period paper showing the 180-bp homeobox (60-aa homeodomain with >75–90% sequence identity between Drosophila and human HOX) and mouse Pax6 cDNA inducing compound eyes on Drosophila legs, wings, and antennae", "scale": "swapping the mouse Pax6 gene into a fruit fly is like unplugging the 'Turn on the headlights' dashboard switch from a lorry and plugging it into a motorbike — the switch itself is identical, and the motorbike turns on its own headlight", "hold_s": 3.8}),
            ("03_basel_1984_homeodomain_helix_turn_helix_model_and_1995_pax6_eye_micrograph_closeup", 140.5, 6.5, "B", False, "24 MARCH 1995 — DEEP HOMOLOGY (PAX6)", "Fast",
             "Fast: daylight macro shot of a 60-amino-acid three-helix homeodomain protein model docked in a DNA major groove beside a 1995 scanning electron micrograph print of a compound eye on a fly leg. Nothing emissive, no face.",
             STYLE + "In crisp daylight on a 1995 Basel laboratory bench, a sculpted three-helix homeodomain protein model docked into a wooden DNA groove sits beside a framed monochrome micrograph of a faceted insect eye." + FAST_TAIL,
             None),
            ("04_explorer_unplugging_pax6_master_eye_switch_from_mouse_model_into_fruit_fly_knee", 147.0, 5.5, "B", True, None, "Quality",
             "Quality: Explorer beat 2 (locked character reference).",
             STYLE + "Standing between a sculpted laboratory mouse model and a large brass fruit-fly model, the Explorer unplugs a golden brass master switch key from the mouse and slots it into the knee socket of the fruit fly, where a faceted red compound eye unfolds." + EXP_TAIL,
             None),
        ],
    ),
    (
        5,
        "Part 05 — Why Your Ten Fingers Aren't Ten Identical Thumbs — & Why Identical Twins Grow Up Different",
        [
            ("01_timeline_1891_1995_and_tabin_1993_sonic_hedgehog_limb_bud_digit_gradient_chart", 152.5, 8.5, "E", False, "1891–1995 TIMELINE · DRIESCH TWINS, MANGOLD-SPEMANN ORGANIZER, LEWIS/NÜSSLEIN-VOLHARD/WIESCHAUS, 180-BP HOMEOBOX, PAX6 & 1993 SONIC HEDGEHOG DIGITS", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, the 3-era timeline completes: 1891 & May 1921 (Hans Driesch shakes 2-cell sea-urchin embryos into identical twins in Naples; Hilde Mangold & Hans Spemann transplant the newt dorsal blastopore lip in Freiburg and discover the embryonic Organizer, winning the 1935 Nobel Prize) · 7 Dec 1978 & 30 Oct 1980 (Edward B. Lewis maps the colinear Bithorax complex and 4-winged Ultrabithorax fly; Christiane Nüsslein-Volhard & Eric Wieschaus map the 15 fruit-fly segmentation genes, sharing the 1995 Nobel Prize) · Mar–Jul 1984 & 24 Mar 1995 (Matthew Scott & Walter Gehring discover the conserved 180-bp Homeobox across flies, frogs, mice, and humans, and Gehring's team induces a fruit-fly eye on a fly's leg using the mouse Pax6 gene).",
             {"kind": "DATA", "label": "1891–1995 EMBRYO & HOX TIMELINE · DEC 1993 TABIN SONIC HEDGEHOG (SHH) LIMB-BUD GRADIENT PATTERNING PINKY TO THUMB", "detail": "Animated timeline (1891 → 1995) alongside Clifford Tabin's December 1993 Sonic hedgehog (SHH) Zone of Polarizing Activity gradient patterning digits 5 to 1 across nested HOXD9–HOXD13 genes", "scale": "from a loop of baby hair in 1921 to a mouse gene inside a fruit fly in 1995, scientists proved that every animal with a head and a heart is built from the same half-billion-year-old genetic blueprint", "when_stamp": "December 1993 · 1891–1995", "timeline_step": "3/3 · 1891–1995 timeline complete", "hold_s": 3.8}),
            ("02_embryonic_hand_limb_bud_sonic_hedgehog_gradient_and_five_digits_model_on_plinth_pan", 161.0, 5.5, "A", False, "SONIC HEDGEHOG & YOUR FIVE FINGERS", "Fast",
             "Fast: daylight close-up of a sculpted embryonic hand limb-bud model with nested colour-coded HOXD bands beside an articulated five-fingered hand model on a wooden museum plinth. Nothing emissive, no face.",
             STYLE + "In crisp daylight on a wooden museum plinth, a sculpted embryonic limb-bud model painted with nested colour gradient bands sits beside an articulated wooden five-fingered hand." + FAST_TAIL,
             None),
            ("03_mary_lyon_1961_calico_cat_allfrey_1964_holliday_riggs_1975_jirtle_2003_and_esteller_2005_twins_handoff", 166.5, 6.5, "C", False, "EPIGENETICS, CALICO CATS & IDENTICAL TWINS", "Quality",
             "Quality: readable faces (Mary Lyon on 22 April 1961 with an orange-and-black calico cat and mottled mice, Vincent Allfrey in May 1964 with Robin Holliday and Arthur Riggs in January 1975 mapping histone spools and DNA methylation, and Randy Jirtle in August 2003 with Manel Esteller in July 2005 comparing yellow and brown Agouti mice and identical twins — handoff to 068 Epigenetics, Calico Cats & Identical Twins).",
             STYLE + "Split period scene: on the left in April 1961 Oxfordshire, Mary Lyon holds a patchwork orange-and-black calico cat beside Vincent Allfrey and Robin Holliday inspecting histone spools and methylated DNA; on the right, Randy Jirtle holds a yellow obese Agouti mouse beside its lean brown twin while Manel Esteller compares identical twin chromosome maps." + QUAL_TAIL,
             {"kind": "WHEN", "label": "22 APRIL 1961 · MAY 1964 · JANUARY 1975 · AUGUST 2003 · JULY 2005", "hold_s": 3.5}),
            ("04_table_three_callback", 173.0, 2.4, "C", False, None, "reuse",
             "Reuse: verified unused moving window [5.50s..7.90s] of P1:07_table_three_props_1891_sea_urchin_tube_1921_hair_loop_dish_and_1978_four_winged_fly_model (callback, £0).",
             "Reuse P1:07_table_three_props_1891_sea_urchin_tube_1921_hair_loop_dish_and_1978_four_winged_fly_model [5.50s..7.90s] (2.40s distinct non-overlapping tail window from 8.00s source clip).",
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
                row["reuse_of"] = "P1:07_table_three_props_1891_sea_urchin_tube_1921_hair_loop_dish_and_1978_four_winged_fly_model"
                row["reuse_window_s"] = [5.5, 7.9]
                row["reuse_audit"] = {
                    "source_row": "P1:07_table_three_props_1891_sea_urchin_tube_1921_hair_loop_dish_and_1978_four_winged_fly_model",
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
            "film": "067_Driesch-Mangold-Spemann-Lewis-Gehring-Embryo-Hox-Genes",
            "part": p_idx,
            "title": p_title,
            "version": "v01",
            "timing_status": "pre_vo_script_clock (built from embryo_script_master_v01.md; retimes onto Scribe STT once VO locks)",
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
        "film": "067_Driesch-Mangold-Spemann-Lewis-Gehring-Embryo-Hox-Genes",
        "version": "v01",
        "date": "2026-10-19",
        "owner": "gemini (J0661)",
        "status": "PRE_VO_BOARDS_V01_NO_MINT",
        "generation_authorized": False,
        "script": "00_Brand/Channel-Setup/ideas/067_Driesch-Mangold-Spemann-Lewis-Gehring-Embryo-Hox-Genes/embryo_script_master_v01.md",
        "sources": "00_Brand/Channel-Setup/ideas/067_Driesch-Mangold-Spemann-Lewis-Gehring-Embryo-Hox-Genes/SOURCES_v01.md",
        "credit_snapshot": {
            "flow_balance": 23740,
            "flow_floor": 0,
            "flow_read_at": "2026-10-15T21:42:22Z",
            "vertex_promo_gbp": 71.02,
            "vertex_usable_gbp": 70.02,
        },
        "totals": totals,
        "per_part": per_part_summary,
        "mint_order": "006 > 007 > 008 > 009 > 010 > 011 > 012 > 013 > 014 > 015 > 016 > 017 > 018 > 019 > 020 > 021 > 022 > 023 > 024 > 025 > 026 > 027 > 028 > 029 > 030 > 031 > 032 > 033 > 034 > 035 > 036 > 037 > 038 > 039 > 040 > 041 > 042 > 043 > 044 > 045 > 046 > 047 > 048 > 049 > 050 > 051 > 052 > 053 > 054 > 055 > 056 > 057 > 058 > 059 > 060 > 061 > 062 > 063 > 064 > 065 > 066 > 067 > 068. Nothing in 067 is generation_authorized.",
    }
    (EDIT / "PICTURE_PLAN_v01.json").write_text(json.dumps(plan, indent=2) + "\n")

    sl = [
        "# 067 Hox Genes: The Hidden Map That Built Your Body — Shot list & plate boards v01 (pre-VO)",
        "",
        "Gemini, 19 Oct 2026, J0661. Built from `embryo_script_master_v01.md` (`91.4 PASS`) and `SOURCES_v01.md`.",
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
        "# 067 price review v01 (pre-VO plate boards)",
        "",
        "Gemini, 19 Oct 2026, J0661. Boards only. **No mint. No spend. No merge.**",
        "Prepared from `embryo_script_master_v01.md` (`91.4 PASS`) and `SOURCES_v01.md` so 067's full plate board rows, non-emissive Fast prompts, £0 code graphics, and Teach-on-Screen overlays are ready to re-time the moment long VO locks. Parked for Chief.",
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
        f"- **Quality ({totals['Quality']} rows):** readable faces (Hans Driesch, Hilde Mangold, Hans Spemann, Wilhelm Roux, Edward B. Lewis, Christiane Nüsslein-Volhard, Eric F. Wieschaus, Matthew P. Scott, William McGinnis, Walter J. Gehring, Mary F. Lyon, Vincent G. Allfrey, Robin Holliday, Randy L. Jirtle, Manel Esteller), 1891 Naples sea-urchin twin blastomeres & May 1921 Freiburg blond baby-hair Organizer transplant, December 1978 Caltech four-winged `Ultrabithorax` fly & October 1980 EMBL Heidelberg `27,000-line` screen, 1984 `180-bp Homeobox` & 24 March 1995 mouse `Pax6` ectopic fly-eye induction, and the 2 Explorer beats.",
        f"- **Fast ({totals['Fast']} rows, non-emissive):** daylight prop and laboratory shots (1921 wax dissecting dish, blond hair-loop microneedle & wooden `Hox` block pan, 3-object callback bench, histological slide `Um 132` & hair-loop pipette, two-tone pale/dark wax embryology graft models, 1980 7-stripe embryo slide & four-winged fly model with glass vials, 14-ring wooden embryo model aligned with brass chromosome bar, 60-aa three-helix homeodomain model in DNA groove & 1995 compound eye micrograph, embryonic limb-bud `Sonic hedgehog` model & wooden 5-fingered hand on museum plinth). Zero candles, flames, sparks, or glowing elements on Fast.",
        f"- **£0 code graphics ({totals['code_graphic']} rows):**",
        "  1. `P1:04_lewis_1978_nusslein_volhard_wieschaus_1980_scott_gehring_1984_hox_colinearity_chart` — `8` *Drosophila* `Hox` genes aligned with `39` human `HOX` genes (`4 clusters`) sharing the conserved `180-bp` homeobox (`60-aa` homeodomain) in `3'→5'` head-to-tail colinear order (`SCALE: your body's master architect genes are lined up along your chromosome like stations on a railway line — the genes at the front of the DNA strand build your head and neck, the middle genes build your chest and ribs, and the genes at the end build your lower back and limbs`)",
        "  2. `P1:06_spemann_mangold_may_1921_1924_organizer_dorsal_lip_chimera_um132_chart` — Spemann & Mangold (May 1921 / 1924, embryo `1921 Um 132`) pale donor dorsal blastopore lip recruiting `>80%` dark host ventral belly cells into a twin neural tube and spine (`SCALE: transplanting a speck of organizer tissue smaller than a pinhead onto an embryo's belly is like dropping a conductor onto a building site — it orders the surrounding skin cells to stop making belly skin and build a second brain and spine instead`)",
        "  3. `P2:02_roux_1888_vs_driesch_1891_twins_and_spemann_mangold_1921_1924_chimera_chart` — Roux (1888 half-embryo) vs Driesch (1891 shaken 2-cell sea-urchin twins) and Spemann-Mangold (1921/1924) chimeric neural tube cell-origin chart (`SCALE: Hilde Mangold's two-colour newt transplant worked like building a house out of white and black bricks — when the new twin spine appeared, over four-fifths of its bricks were black belly bricks that the tiny white organizer patch had recruited on the spot`)",
        "  4. `P3:02_nusslein_volhard_wieschaus_30_oct_1980_and_lewis_7_dec_1978_nature_segmentation_hox_chart` — Nüsslein-Volhard & Wieschaus (30 October 1980 *Nature*, `15` segmentation genes: maternal `Bicoid` → `gap` → `7 pair-rule` → `14 segment-polarity` stripes) & Lewis (7 December 1978 *Nature*, `8` colinear `Hox` selectors) (`SCALE: building a body from a single round egg is like painting a map on a blank globe — first a smooth gradient of maternal ink marks the North Pole as the head, then three waves of stencil genes divide the globe into fourteen numbered stripes, and finally each stripe reads its own Hox address code`)",
        "  5. `P4:02_mcginnis_gehring_1984_cell_cross_species_homeobox_and_halder_gehring_1995_science_pax6_chart` — McGinnis & Gehring (July 1984 *Cell*) cross-species `180-bp` Homeobox Southern blot (`>75–90%` homeodomain identity) & Halder, Callaerts & Gehring (24 March 1995 *Science*) mouse `Pax6` ectopic fly-eye chart (`SCALE: swapping the mouse Pax6 gene into a fruit fly is like unplugging the 'Turn on the headlights' dashboard switch from a lorry and plugging it into a motorbike — the switch itself is identical, and the motorbike turns on its own headlight`)",
        "  6. `P5:01_timeline_1891_1995_and_tabin_1993_sonic_hedgehog_limb_bud_digit_gradient_chart` — completed timeline (1891 → 1995) + Clifford Tabin's December 1993 `Sonic hedgehog` (`SHH`) limb-bud gradient patterning digits 5 to 1 (`SCALE: from a loop of baby hair in 1921 to a mouse gene inside a fruit fly in 1995, scientists proved that every animal with a head and a heart is built from the same half-billion-year-old genetic blueprint`)",
        f"- **£0 verified reuse ({totals['reuse']} row):** `P5:04_table_three_callback` uses the 2.40 s unused moving tail `[5.50s..7.90s]` of `P1:07_table_three_props_1891_sea_urchin_tube_1921_hair_loop_dish_and_1978_four_winged_fly_model`.",
        "",
        "## Mint order",
        "",
        "006 > 007 > 008 > 009 > 010 > 011 > 012 > 013 > 014 > 015 > 016 > 017 > 018 > 019 > 020 > 021 > 022 > 023 > 024 > 025 > 026 > 027 > 028 > 029 > 030 > 031 > 032 > 033 > 034 > 035 > 036 > 037 > 038 > 039 > 040 > 041 > 042 > 043 > 044 > 045 > 046 > 047 > 048 > 049 > 050 > 051 > 052 > 053 > 054 > 055 > 056 > 057 > 058 > 059 > 060 > 061 > 062 > 063 > 064 > 065 > 066 > 067 > 068. `generation_authorized` is `false` on every row.",
    ])
    (EDIT / "PRICE_REVIEW_v01.md").write_text("\n".join(pr_lines) + "\n")
    print(f"067 v01 boards written: {totals['rows']} rows, Flow expected={totals['flow_credits_expected']}")


if __name__ == "__main__":
    main()
