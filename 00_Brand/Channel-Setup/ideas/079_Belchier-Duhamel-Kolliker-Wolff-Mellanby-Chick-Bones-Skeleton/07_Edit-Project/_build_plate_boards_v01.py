#!/usr/bin/env python3
"""HOS 079 (Your Skeleton: Rebuilt From Scratch Every 10 Years) pre-VO plate boards v01. J0723. No mint, no spend.

Built from 00_Brand/Channel-Setup/ideas/079_Belchier-Duhamel-Kolliker-Wolff-Mellanby-Chick-Bones-Skeleton/bones_script_master_v01.md
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
        "Part 01 — The Crimson Pig Bones, the Harbour Crane in Your Thigh & the Living Skeleton",
        [
            ("01_living_femur_osteoclasts_osteoblasts_along_culmann_crane_lines_beside_belchier_red_bone_and_vienna_sun", 0.0, 5.5, "A", False, "A NEW SKELETON EVERY 10 YEARS", "Quality",
             "Quality: Short frame 0 / answer image (0:03) + side by side, inside a living human femur acid-spraying osteoclasts dissolve microscopic tunnels while osteoblast bricklayers weave collagen ropes and hydroxyapatite crystals along the exact stress lines of Karl Culmann's 1866 iron crane, beside John Belchier's 1736 crimson madder-dyed pig bone and Harriette Chick's 1922 Vienna sunlight ward.",
             STYLE + "Split anatomical-and-historical scene: on the left, a cutaway human thighbone reveals microscopic osteoclasts and osteoblasts rebuilding arched trabecular struts that match an iron harbour crane; on the right, a crimson madder-ringed bone sits beside a sunny Vienna hospital balcony." + QUAL_TAIL,
             {"kind": "WHEN", "label": "LONDON, 1736", "timeline_step": "1/3 · 1736–1739 & 1873 (John Belchier and Duhamel du Monceau use red madder-root dye to prove bones grow in living rings, and Albert von Kölliker discovers bone-dissolving osteoclasts partnering with osteoblasts)", "hold_s": 3.5}),
            ("02_belchier_1736_duhamel_1739_kolliker_1873_culmann_wolff_1866_1892_and_chick_1922_vienna_split", 5.5, 6.0, "B", False, "RED RINGS, IRON CRANE, VITAMIN D", "Quality",
             "Quality: complex three-part composition (John Belchier in London in 1736 and Henri-Louis Duhamel du Monceau in Paris in 1739 examining alternating red and white madder-root growth rings in bone alongside Albert von Kölliker in Würzburg in 1873; Karl Culmann and Hermann von Meyer in Zurich in 1866 with Julius Wolff in Berlin in 1892 comparing a human femur cross-section to an iron crane; and Edward Mellanby, Elmer McCollum, and Harriette Chick in 1919–1922 curing rickets with cod-liver oil and ultraviolet sunlight).",
             STYLE + "Three-panel period composition: on the left, John Belchier in 1736 London and Duhamel du Monceau in 1739 Paris holding red-and-white ringed bones alongside Albert von Kölliker; in the centre, Karl Culmann in 1866 Zurich and Julius Wolff in 1892 Berlin comparing a sectioned femur to an iron crane drawing; on the right, Harriette Chick in 1922 Vienna with cod-liver oil and infant bone X-rays." + QUAL_TAIL,
             None),
            ("03_femoral_head_collagen_cables_and_hydroxyapatite_crystals_bearing_400kg_vs_rubber_and_chalk_bone", 11.5, 6.0, "C", False, "STRONGER THAN REINFORCED CONCRETE", "Quality",
             "Quality: complex biomechanical reveal (a cross-section of the human femoral head supporting 400 kg of impact load shows flexible collagen protein cables interwoven with hard hydroxyapatite calcium-phosphate crystals, while unmineralized rickets bone bends like rubber and collagen-stripped brittle bone shatters like chalk).",
             STYLE + "In a three-dimensional cutaway of a human femoral head under heavy load, golden braided collagen cables and white calcium-phosphate crystals lock together into resilient arches beside a bending demineralized bone model and a brittle chalky bone model." + QUAL_TAIL,
             {"kind": "WHEN", "label": "1736 · 1739 · 1845 · 1866 · 1873 · 1892 · 1919 · 1922", "timeline_step": "1/3 · 1736–1873 (Belchier, Duhamel & Kölliker) · 2/3 · 1866 & 1892 (Meyer, Culmann & Wolff) · 3/3 · 1919–1922 (Mellanby, McCollum & Chick)", "hold_s": 3.5}),
            ("04_belchier_1736_kolliker_1873_wolff_1892_and_chick_1922_bone_remodelling_crane_vitamin_d_chart", 17.5, 8.0, "E", False, "OSTEOCLAST HCL RESORPTION & OSTEOBLAST COLLAGEN/HYDROXYAPATITE (~10%/YR = 10-YR RENEWAL) · CULMANN-WOLFF CRANE ARCHES & VITAMIN D", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked Bone Remodelling, Trabecular Stress Trajectories & Vitamin D Mineralization chart from John Belchier (1736 Phil. Trans. R. Soc. 39: 287–288), Duhamel du Monceau (1739 Mém. Acad. Roy. Sci. 1–13), Albert von Kölliker (1873 Die normale Resorption des Knochengewebes), Julius Wolff (1892 Das Gesetz der Transformation der Knochen), Elmer McCollum (1922 J. Biol. Chem. 53: 293–312), and Harriette Chick (1922 The Lancet 200: 7–11) shows osteoclast acid resorption, osteoblast collagen/hydroxyapatite deposition (~10% annual adult bone turnover = 100% in 10 years), Culmann's crane stress lines in the proximal femur, and UV-B / Vitamin D calcium absorption.",
             {"kind": "DATA", "label": "OSTEOCLAST/OSTEOBLAST REMODELLING (10%/YR = 10-YR SKELETON RENEWAL), CULMANN-WOLFF CRANE STRESS ARCHES & VITAMIN D MINERALIZATION", "detail": "Inked bone remodelling & Wolff's Law mechanical stress chart on period paper showing osteoclast HCl/protease resorption vs osteoblast collagen + hydroxyapatite deposition (10% annual turnover = 10-year complete renewal), Culmann's 1866 Fairbairn crane stress trajectories in the femoral neck, and Vitamin D calcium mineralization", "scale": "your skeleton is not a stone monument — it is a busy highway under non-stop roadworks, where microscopic crews rip up ten percent of the pavement every year so every bone in your body is completely replaced every ten years", "who_card": "John Belchier (1706–1785) — British surgeon · Henri-Louis Duhamel du Monceau (1700–1782) — French botanist and engineer · John Goodsir (1814–1867) — Scottish anatomist · Albert von Kölliker (1817–1905) — Swiss anatomist and histologist · Karl Culmann (1821–1881) — Swiss structural engineer · Julius Wolff (1836–1902) — German orthopaedic surgeon · Edward Mellanby (1884–1955) — British pharmacologist · Elmer Verner McCollum (1879–1967) — American biochemist · Harriette Chick (1875–1977) — British nutritionist and microbiologist", "when_stamp": "1736 · 1739 · 1845 · 1866 · 1873 · 1892 · 1919 · 1922", "hold_s": 3.8}),
            ("05_belchier_1736_phil_trans_offprint_madder_root_and_sectioned_femur_pan", 25.5, 5.5, "A", False, "10% OF YOUR BONE REPLACED EVERY YEAR", "Fast",
             "Fast: daylight macro pan across John Belchier's 1736 Philosophical Transactions paper, dried crimson madder roots in a porcelain dish, and a longitudinally sectioned human femur on an oak bench between code graphics so two full-frame graphics never run back to back. Nothing emissive, no face.",
             STYLE + "In crisp daylight on an oak anatomy bench, the camera pans smoothly across a 1736 Royal Society journal, a dish of red madder roots, and a sawed-open femur displaying internal bone arches." + FAST_TAIL,
             None),
            ("06_culmann_1866_and_wolff_1892_femur_trabecular_arch_vs_fairbairn_crane_chart", 31.0, 8.0, "E", False, "ZURICH & BERLIN, 1866–1892", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period parchment, an inked Karl Culmann & Julius Wolff (1866 / 1892 Das Gesetz der Transformation der Knochen) Femoral Trabecular Arch vs Fairbairn Harbour Crane diagram shows the curved compressive and tensile trajectories calculated by Culmann for an iron crane beside a coronal section of the human proximal femur whose spongy bone struts (trabeculae) trace the exact same mathematical curves.",
             {"kind": "DATA", "label": "1866 CULMANN & 1892 WOLFF (DAS GESETZ DER TRANSFORMATION DER KNOCHEN): IRON CRANE STRESS LINES = HUMAN FEMUR TRABECULAR ARCHES", "detail": "Inked Julius Wolff (1892 Das Gesetz der Transformation der Knochen, Plates I–II) & Karl Culmann (1866) mathematical principal-stress trajectories in the iron crane vs human proximal femur trabecular arches on period paper", "scale": "hollowing out the middle of your thighbone and stringing microscopic bone arches only along the exact lines of force makes your femur half as heavy as solid rock yet just as strong — the exact trick engineers use to build iron bridges and cranes", "hold_s": 3.8}),
            ("07_table_three_props_1739_ringed_bone_1892_crane_femur_plate_and_1922_cod_liver_oil_bottle", 39.0, 5.5, "C", False, "1736 TO 1928", "Fast",
             "Fast: daylight prop table (callback source for Part 05: Duhamel du Monceau's 1739 red-and-white madder-ringed bone cross-section, Julius Wolff's 1892 sectioned femur beside a miniature brass Fairbairn crane model, and Harriette Chick's 1922 amber glass bottle of cod-liver oil with a silver spoon). Nothing emissive.",
             STYLE + "On an oak workbench in soft window light sit three objects side by side: a bone cross-section with concentric red and white rings, a sectioned thighbone next to a miniature brass harbour crane, and an amber bottle of cod-liver oil beside a silver spoon." + FAST_TAIL,
             None),
            ("08_explorer_in_hard_hat_inside_trabecular_bone_arches_helping_osteoblast_weave_collagen_and_calcium", 62.0, 5.5, "A", True, None, "Quality",
             "Quality: Explorer beat 1 (locked character reference, after 1:00).",
             STYLE + "Wearing a small brass hard hat inside the vaulted trabecular arches of a giant bone model, the Explorer watches a sculpted osteoclast dissolve a cracked strut and then helps lash golden collagen cables across the arch and trowel white mineral crystals along the stress line." + EXP_TAIL,
             None),
            ("09_harriette_chick_and_elsie_dalyell_1922_vienna_sunlight_veranda_and_wrist_xrays", 67.5, 5.5, "B", False, "THE VIENNA SUNLIGHT TRIAL", "Quality",
             "Quality: readable faces (in Vienna in 1922, Harriette Chick and Elsie Dalyell wheel infants in cots out onto the sunny hospital veranda while comparing bone X-rays of children given cod-liver oil or sunlight).",
             STYLE + "On a bright 1922 Vienna hospital veranda, nutritionist Harriette Chick and physician Elsie Dalyell hold up infant wrist X-ray plates to the daylight beside baby cots warmed by the sun." + QUAL_TAIL,
             {"kind": "WHEN", "label": "VIENNA, 1 JULY 1922", "timeline_step": "3/3 · 1919–1922 (Edward Mellanby, Elmer McCollum, and Harriette Chick prove Vitamin D from cod-liver oil or sunlight cures rickets)", "hold_s": 3.5}),
        ],
    ),
    (
        2,
        "Part 02 — 1736–1873: The Calico Printer's Crimson Pig Bones, Osteoclast Wrecking Crews & Osteoblast Bricklayers",
        [
            ("01_belchier_1736_london_duhamel_1739_paris_red_madder_bones_and_kolliker_1873_wurzburg_osteoclasts", 73.0, 6.5, "A", False, "RED DYE REVEALED BONE RINGS", "Quality",
             "Quality: readable faces (British surgeon John Belchier in London in 1736 examining crimson madder-dyed pig bones and French polymath Henri-Louis Duhamel du Monceau in Paris in 1739 showing concentric red and white bone growth rings, dissolving to Swiss histologist Albert von Kölliker in Würzburg in 1873 identifying multinucleated bone-resorbing osteoclasts).",
             STYLE + "Split period scene: on the left, John Belchier in 1736 London and Duhamel du Monceau in 1739 Paris hold up sawed-open bones displaying alternating crimson and white rings; on the right in 1873 Würzburg, Albert von Kölliker peers through his brass microscope at multinucleated osteoclasts." + QUAL_TAIL,
             {"kind": "FACT", "label": "Red dye revealed bone rings", "who_card": "Carl Gegenbaur (1826–1903) — German anatomist", "when_stamp": "1736 · 1739 · 1845 · 1864 · 1873", "timeline_step": "1/3 · 1736–1873 (Belchier & Duhamel prove living bone growth rings with madder dye; Goodsir, Gegenbaur & Kölliker discover osteoblasts and osteoclasts)", "hold_s": 3.8}),
            ("02_belchier_1736_duhamel_1739_madder_rings_and_kolliker_1873_osteoclast_osteoblast_chart", 79.5, 8.0, "E", False, "1736 BELCHIER & 1739 DUHAMEL (MADDER GROWTH RINGS) & 1873 KÖLLIKER (OSTEOCLAST HCL RESORPTION + OSTEOBLAST COLLAGEN/HYDROXYAPATITE)", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked John Belchier (1736 Phil. Trans. R. Soc. 39: 287–288) & Duhamel du Monceau (1739 Mém. Acad. Roy. Sci. 1–13) alternating red-and-white madder-root periosteal bone growth rings alongside Albert von Kölliker's (1873 Die normale Resorption des Knochengewebes) osteoclast acid resorption pit and osteoblast collagen-hydroxyapatite deposition diagram.",
             {"kind": "DATA", "label": "1736/1739 MADDER BONE GROWTH RINGS & 1873 KÖLLIKER OSTEOCLAST ACID PIT VS OSTEOBLAST COLLAGEN + HYDROXYAPATITE COMPOSITE", "detail": "Inked John Belchier (1736 Phil. Trans. R. Soc. 39: 287–288) & Duhamel du Monceau (1739 Mém. Acad. Roy. Sci. 1–13) alternating red-and-white madder-root periosteal bone growth rings alongside Albert von Kölliker's (1873) osteoclast acid resorption pit and osteoblast collagen-hydroxyapatite deposition diagram on period paper", "scale": "bone gets its secret strength from the exact same partnership as reinforced concrete — flexible collagen protein ropes act like the steel rebar that stops bone from snapping, while hard calcium crystals act like the poured cement that stops it from squashing", "hold_s": 3.8}),
            ("03_wurzburg_1873_microscope_kolliker_lithograph_and_red_white_ringed_bone_slices_closeup", 87.5, 6.5, "B", False, "1873 — KÖLLIKER DISCOVERS OSTEOCLASTS", "Fast",
             "Fast: daylight macro shot of Albert von Kölliker's 1873 Leipzig monograph lithograph of multinucleated osteoclasts beside a brass microscope and polished bone cross-sections with concentric red and white madder rings on a bench. Nothing emissive, no face.",
             STYLE + "In crisp daylight on an 1873 Würzburg histology bench, an open illustrated bone-resorption monograph sits beside a brass microscope and bone cross-sections ringed in crimson and white." + FAST_TAIL,
             None),
            ("04_cutaway_osteon_model_showing_braided_collagen_cables_and_hydroxyapatite_crystals_pan", 94.0, 5.5, "C", False, "COLLAGEN ROPES & CALCIUM CRYSTALS", "Fast",
             "Fast: daylight close-up pan across a sculpted architectural model of a bone osteon showing concentric lamellae of braided golden collagen cables encrusted with white hydroxyapatite crystals on an oak table. Nothing emissive, no face.",
             STYLE + "In bright window light on an oak table, a sculpted cutaway model of a cylindrical bone osteon reveals braided collagen protein cables reinforced with hexagonal calcium-phosphate crystals." + FAST_TAIL,
             None),
        ],
    ),
    (
        3,
        "Part 03 — 1866 & 1892: The Harbour Crane Inside Your Thighbone (Karl Culmann & Julius Wolff's Law) — Midpoint Twist",
        [
            ("01_meyer_and_culmann_1866_zurich_crane_femur_and_julius_wolff_1892_berlin_wolffs_law", 99.5, 6.5, "A", False, "CRANE MATCHED HUMAN THIGHBONE", "Quality",
             "Quality: readable faces (Swiss anatomist Georg Hermann von Meyer and structural engineer Karl Culmann at ETH Zurich in 1866 comparing the spongy trabecular bone arches of a sliced human femur to the mathematical stress lines of Culmann's iron Fairbairn harbour crane, dissolving to Berlin orthopaedic surgeon Julius Wolff in 1892 formulating Wolff's Law).",
             STYLE + "Split period scene: on the left in 1866 Zurich, anatomist Hermann von Meyer and engineer Karl Culmann hold a sawed-open human femur beside a drafted stress diagram of a curved iron crane; on the right in 1892 Berlin, surgeon Julius Wolff traces the matching trabecular arches in his folio atlas." + QUAL_TAIL,
             {"kind": "FACT", "label": "Crane matched human thighbone", "who_card": "Georg Hermann von Meyer (1815–1892) — Swiss anatomist", "when_stamp": "1866 · 1867 · 1870 · 1892", "timeline_step": "2/3 · 1866 & 1892 (Karl Culmann recognizes crane stress trajectories in Hermann von Meyer's femur section; Julius Wolff formulates Wolff's Law)", "hold_s": 3.8}),
            ("02_culmann_1866_wolff_1892_trabecular_stress_tennis_arm_and_astronaut_bone_loss_chart", 106.0, 8.0, "E", False, "1866 CULMANN & 1892 WOLFF'S LAW: FEMORAL TRABECULAR STRESS LINES, TENNIS HUMERUS (+20–35% CORTEX) & SPACEFLIGHT LOSS (−1 TO −2%/MO)", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked Karl Culmann (1866) & Julius Wolff (1892 Das Gesetz der Transformation der Knochen) femoral trabecular stress-trajectory chart alongside tennis-player dominant vs non-dominant humeral cortical thickness (+20–35%) and astronaut microgravity bone loss (−1% to −2% per month).",
             {"kind": "DATA", "label": "1866/1892 WOLFF'S LAW CHART: CRANE VS FEMUR STRESS TRAJECTORIES, TENNIS SERVING ARM (+20–35% THICKER) & MICROGRAVITY LOSS (−1–2%/MO)", "detail": "Inked Karl Culmann (1866) & Julius Wolff (1892 Das Gesetz der Transformation der Knochen) femoral trabecular stress-trajectory chart alongside tennis-player dominant vs non-dominant humeral cortical thickness (+20–35%) and astronaut microgravity bone loss (−1% to −2% per month) on period paper", "scale": "astronauts on the International Space Station have to strap themselves to treadmills and vacuum-resistance machines for two hours every day — because without gravity tugging on their bones, their own osteoclasts assume they don't need a skeleton anymore and start dissolving it away", "hold_s": 3.8}),
            ("03_berlin_1892_wolff_folio_plates_coronal_femur_section_and_brass_fairbairn_crane_closeup", 114.0, 6.5, "B", False, "1892 — JULIUS WOLFF'S LAW OF BONE REMODELLING", "Fast",
             "Fast: daylight macro shot of Plate I of Julius Wolff's 1892 Das Gesetz der Transformation der Knochen beside a coronal human femur section and a brass scale model of a curved Fairbairn harbour crane on a bench. Nothing emissive, no face.",
             STYLE + "In crisp daylight on an 1892 Berlin engineering bench, an open folio plate of crane and bone trajectories sits beside a sliced human femur and a brass model of a curved harbour crane." + FAST_TAIL,
             None),
            ("04_osteocyte_mechanosensor_network_inside_trabecular_bone_struts_model_on_oak_table_pan", 120.5, 5.5, "C", False, "OSTEOCYTE STRESS SENSORS & TRABECULAR ARCHES", "Fast",
             "Fast: daylight close-up pan across a sculpted anatomical model of spongy trabecular bone arches showing star-shaped osteocyte sensor cells linked by microscopic canaliculi tunnels on an oak table. Nothing emissive, no face.",
             STYLE + "In bright window light on an oak table, a sculpted cutaway model of trabecular bone arches shows star-shaped osteocyte cells connected through a fine web of microscopic bone channels." + FAST_TAIL,
             None),
        ],
    ),
    (
        4,
        "Part 04 — 1919–1922: Smoky Cities, Bowed Legs (Rickets) & How Mellanby, McCollum and Harriette Chick Unlocked Vitamin D",
        [
            ("01_mellanby_1919_mccollum_1922_cod_liver_oil_and_harriette_chick_1922_vienna_vitamin_d_sunlight", 126.0, 6.5, "A", False, "SUNLIGHT MAKES BONE VITAMIN", "Quality",
             "Quality: readable faces (British pharmacologist Edward Mellanby in 1919 and American biochemist Elmer Verner McCollum in August 1922 isolating Vitamin D in oxidized cod-liver oil, dissolving to British nutritionist Harriette Chick and Elsie Dalyell in Vienna in July 1922 proving by infant X-rays that both cod-liver oil and ultraviolet sunlight cure rickets).",
             STYLE + "Split period scene: on the left, Edward Mellanby and Elmer McCollum test oxidized cod-liver oil flasks in a biochemistry laboratory; on the right in 1922 Vienna, Harriette Chick and Elsie Dalyell compare healed infant wrist X-rays from the cod-liver oil and sunlight wards." + QUAL_TAIL,
             {"kind": "FACT", "label": "Sunlight makes bone vitamin", "who_card": "Kurt Huldschinsky (1883–1940) — German paediatrician · Elsie Jean Dalyell (1881–1948) — Australian pathologist and physician", "when_stamp": "15 March 1919 · 1 July 1922 · August 1922 · 1924 · 1928", "timeline_step": "3/3 · 1919–1928 (Mellanby, Huldschinsky, McCollum, and Harriette Chick prove Vitamin D from cod-liver oil or UV sunlight mineralizes bone and cures rickets)", "hold_s": 3.8}),
            ("02_mccollum_aug_1922_oxidized_cod_liver_oil_and_chick_jul_1922_vienna_rickets_xray_chart", 132.5, 8.0, "E", False, "1 JUL 1922 CHICK ET AL. (LANCET VIENNA TRIAL) & AUG 1922 MCCOLLUM (J. BIOL. CHEM.): COD-LIVER OIL OR UV SUNLIGHT → VITAMIN D CALCIUM MINERALIZATION", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked Elmer McCollum (August 1922 J. Biol. Chem. 53: 293–312) oxidized cod-liver oil Vitamin D proof & Harriette Chick (1 July 1922 The Lancet 200: 7–11) Vienna infant rickets X-ray healing chart (winter dark ward vs cod-liver oil vs UV sunlight exposure).",
             {"kind": "DATA", "label": "1922 MCCOLLUM (J. BIOL. CHEM.) & HARRIETTE CHICK (LANCET VIENNA 75-INFANT TRIAL): DARK WINTER WARD VS COD-LIVER OIL OR UV SUNLIGHT", "detail": "Inked Elmer McCollum (1922 J. Biol. Chem. 53: 293–312) oxidized cod-liver oil Vitamin D proof & Harriette Chick (1 July 1922 The Lancet 200: 7–11) Vienna infant rickets X-ray healing chart (winter dark ward vs cod-liver oil vs UV sunlight exposure) on period paper", "scale": "Harriette Chick proved that Vitamin D isn't really a vitamin at all — it is a sunlight-powered hormone that your skin brews out of cholesterol whenever ultraviolet rays hit your arms, unlocking the gate that lets calcium from your lunch enter your bones", "hold_s": 3.8}),
            ("03_vienna_1922_cod_liver_oil_bottles_wrist_xray_plates_and_lancet_report_closeup", 140.5, 6.5, "B", False, "1922 — MCCOLLUM & CHICK PROVE VITAMIN D", "Fast",
             "Fast: daylight macro shot of amber cod-liver oil bottles and a dosing spoon beside comparative infant wrist X-ray plates (rachitic vs mineralized) and the July 1922 Lancet report on a bench. Nothing emissive, no face.",
             STYLE + "In crisp daylight on a 1922 Vienna clinic table, amber bottles of cod-liver oil and a silver spoon sit beside comparative wrist X-ray plates and an open medical journal." + FAST_TAIL,
             None),
            ("04_explorer_turning_sunlight_cholesterol_ring_into_vitamin_d_key_to_unlock_calcium_gate_for_bone", 147.0, 5.5, "B", True, None, "Quality",
             "Quality: Explorer beat 2 (locked character reference).",
             STYLE + "Standing beside a brass gate between an intestinal absorption model and a trabecular bone scaffold, the Explorer fits a golden Vitamin D key into the lock and swings the gate wide, letting white calcium spheres roll onto the collagen cables of the bone." + EXP_TAIL,
             None),
        ],
    ),
    (
        5,
        "Part 05 — The Living Cathedral Inside You — & How Scientists Cracked the 4-Letter Genetic Code",
        [
            ("01_timeline_1736_1928_and_living_skeleton_remodelling_vitamin_d_chart", 152.5, 8.5, "E", False, "1736–1928 TIMELINE · BELCHIER & DUHAMEL MADDER RINGS, KÖLLIKER OSTEOCLASTS, CULMANN-WOLFF CRANE LAW & CHICK-MCCOLLUM VITAMIN D", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, the 3-era timeline completes: 1736–1739 & 1873 (John Belchier and Duhamel du Monceau use red madder-root dye to prove bones grow in living rings, and Albert von Kölliker discovers bone-dissolving osteoclasts partnering with osteoblasts) · 1866 & 1892 (Swiss crane engineer Karl Culmann spots principal-stress trajectories in the human femur, inspiring Julius Wolff's Law of mechanical bone remodelling) · 1919–1928 (Edward Mellanby, Elmer McCollum, and Harriette Chick prove in London, Baltimore, and Vienna that Vitamin D from cod-liver oil or ultraviolet sunlight mineralizes bone and cures rickets).",
             {"kind": "DATA", "label": "1736–1928 BONE REMODELLING, WOLFF'S LAW & VITAMIN D TIMELINE · BELCHIER, DUHAMEL, KÖLLIKER, CULMANN, WOLFF, MCCOLLUM & CHICK", "detail": "Animated timeline (1736 → 1928) alongside an inked summary of 10-year osteoblast/osteoclast bone turnover, Culmann-Wolff mechanical stress trajectories, and Vitamin D mineralization", "scale": "from crimson pig bones on a London dinner table to an iron crane in Zurich and sunny hospital balconies in Vienna, scientists discovered how your body rebuilds its entire skeleton every ten years", "when_stamp": "1736–1928", "timeline_step": "3/3 · 1736–1928 timeline complete", "hold_s": 3.8}),
            ("02_sectioned_femur_and_braided_collagen_model_beside_dna_mrna_ribosome_model_on_plinth_pan", 161.0, 5.5, "A", False, "206 LIVING BONES REBUILT EVERY 10 YEARS", "Fast",
             "Fast: daylight close-up of a sectioned human femur and braided collagen-hydroxyapatite model beside a DNA double helix, mRNA ribbon, and ribosome model on a wooden museum plinth. Nothing emissive, no face.",
             STYLE + "In crisp daylight on a wooden museum plinth, a sectioned human femur and braided collagen cable model sit beside a sculpted DNA helix, messenger RNA ribbon, and ribosome model." + FAST_TAIL,
             None),
            ("03_beadle_tatum_1941_bread_mould_palade_1955_brenner_jacob_1960_mrna_and_nirenberg_matthaei_1961_handoff", 166.5, 6.5, "C", False, "MRNA, RIBOSOMES & THE GENETIC CODE", "Quality",
             "Quality: readable faces (George Beadle and Edward Tatum in 1941 irradiating bread mould alongside George Palade in 1955, Sydney Brenner, François Jacob, and Matthew Meselson on Good Friday 1960 discovering messenger RNA, and Marshall Nirenberg and Heinrich Matthaei at the NIH at 3:00 a.m. on 27 May 1961 decoding UUU = Phenylalanine — handoff to 080 Messenger RNA, Ribosomes & the Genetic Code).",
             STYLE + "Split period scene: on the left, George Beadle and Edward Tatum in 1941 Stanford with Neurospora culture tubes beside Sydney Brenner and François Jacob in 1960 Cambridge; on the right in 1961 Bethesda, Marshall Nirenberg and Heinrich Matthaei examine test tube racks and a paper radiation tape reading 39,800 counts." + QUAL_TAIL,
             {"kind": "WHEN", "label": "1941 · 1955 · 15 APRIL 1960 · 27 MAY 1961", "hold_s": 3.5}),
            ("04_table_three_callback", 173.0, 2.4, "C", False, None, "reuse",
             "Reuse: verified unused moving window [5.50s..7.90s] of P1:07_table_three_props_1739_ringed_bone_1892_crane_femur_plate_and_1922_cod_liver_oil_bottle (callback, £0).",
             "Reuse P1:07_table_three_props_1739_ringed_bone_1892_crane_femur_plate_and_1922_cod_liver_oil_bottle [5.50s..7.90s] (2.40s distinct non-overlapping tail window from 8.00s source clip).",
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
                row["reuse_of"] = "P1:07_table_three_props_1739_ringed_bone_1892_crane_femur_plate_and_1922_cod_liver_oil_bottle"
                row["reuse_window_s"] = [5.5, 7.9]
                row["reuse_audit"] = {
                    "source_row": "P1:07_table_three_props_1739_ringed_bone_1892_crane_femur_plate_and_1922_cod_liver_oil_bottle",
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
            "film": "079_Belchier-Duhamel-Kolliker-Wolff-Mellanby-Chick-Bones-Skeleton",
            "part": p_idx,
            "title": p_title,
            "version": "v01",
            "timing_status": "pre_vo_script_clock (built from bones_script_master_v01.md; retimes onto Scribe STT once VO locks)",
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
        "film": "079_Belchier-Duhamel-Kolliker-Wolff-Mellanby-Chick-Bones-Skeleton",
        "version": "v01",
        "date": "2026-10-20",
        "owner": "gemini (J0723)",
        "status": "PRE_VO_BOARDS_V01_NO_MINT",
        "generation_authorized": False,
        "script": "00_Brand/Channel-Setup/ideas/079_Belchier-Duhamel-Kolliker-Wolff-Mellanby-Chick-Bones-Skeleton/bones_script_master_v01.md",
        "sources": "00_Brand/Channel-Setup/ideas/079_Belchier-Duhamel-Kolliker-Wolff-Mellanby-Chick-Bones-Skeleton/SOURCES_v01.md",
        "credit_snapshot": {
            "flow_balance": 23740,
            "flow_floor": 0,
            "flow_read_at": "2026-10-15T21:42:22Z",
            "vertex_promo_gbp": 71.02,
            "vertex_usable_gbp": 70.02,
        },
        "totals": totals,
        "per_part": per_part_summary,
        "mint_order": "006 > 007 > 008 > 009 > 010 > 011 > 012 > 013 > 014 > 015 > 016 > 017 > 018 > 019 > 020 > 021 > 022 > 023 > 024 > 025 > 026 > 027 > 028 > 029 > 030 > 031 > 032 > 033 > 034 > 035 > 036 > 037 > 038 > 039 > 040 > 041 > 042 > 043 > 044 > 045 > 046 > 047 > 048 > 049 > 050 > 051 > 052 > 053 > 054 > 055 > 056 > 057 > 058 > 059 > 060 > 061 > 062 > 063 > 064 > 065 > 066 > 067 > 068 > 069 > 070 > 071 > 072 > 073 > 074 > 075 > 076 > 077 > 078 > 079 > 080. Nothing in 079 is generation_authorized.",
    }
    (EDIT / "PICTURE_PLAN_v01.json").write_text(json.dumps(plan, indent=2) + "\n")

    sl = [
        "# 079 Your Skeleton: Rebuilt From Scratch Every 10 Years — Shot list & plate boards v01 (pre-VO)",
        "",
        "Gemini, 20 Oct 2026, J0723. Built from `bones_script_master_v01.md` (`91.0/100 PASS`) and `SOURCES_v01.md`.",
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
        "# 079 price review v01 (pre-VO plate boards)",
        "",
        "Gemini, 20 Oct 2026, J0723. Boards only. **No mint. No spend. No merge.**",
        "Prepared from `bones_script_master_v01.md` (`91.0/100 PASS`) and `SOURCES_v01.md` so 079's full plate board rows, non-emissive Fast prompts, £0 code graphics, and Teach-on-Screen overlays are ready to re-time the moment long VO locks. Parked for Chief.",
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
        f"- **Quality ({totals['Quality']} rows):** readable faces (John Belchier, Henri-Louis Duhamel du Monceau, John Goodsir, Carl Gegenbaur, Albert von Kölliker, Georg Hermann von Meyer, Karl Culmann, Julius Wolff, Edward Mellanby, Kurt Huldschinsky, Elmer Verner McCollum, Harriette Chick, Elsie Jean Dalyell, George Beadle, Edward Tatum, Sydney Brenner, François Jacob, Marshall Nirenberg, Heinrich Matthaei), 1736 London crimson madder-dyed bones & 1739 concentric bone rings, 1873 Würzburg `osteoclast` discovery, 1866 Zurich crane-in-the-femur & 1892 Berlin `Wolff's Law`, 1919–1922 Vienna `Vitamin D` rickets cure, and the 2 Explorer beats.",
        f"- **Fast ({totals['Fast']} rows, non-emissive):** daylight prop and laboratory shots (1736 Belchier *Phil. Trans.* offprint, dried madder root & sectioned femur pan, 3-object callback bench, 1873 Kölliker monograph lithograph with brass microscope & ringed bone slices, sculpted osteon collagen-hydroxyapatite model, 1892 Berlin Wolff folio plates with sectioned femur & brass harbour crane model, sculpted osteocyte mechanosensor network inside trabecular arches, 1922 Vienna cod-liver oil bottles with infant wrist X-rays & *Lancet* report, sectioned femur & collagen model beside DNA/mRNA/ribosome model on museum plinth). Zero candles, flames, sparks, or glowing elements on Fast.",
        f"- **£0 code graphics ({totals['code_graphic']} rows):**",
        "  1. `P1:04_belchier_1736_kolliker_1873_wolff_1892_and_chick_1922_bone_remodelling_crane_vitamin_d_chart` — `osteoclast` HCl resorption & `osteoblast` collagen/hydroxyapatite deposition (`~10%/yr` = `10-year` complete renewal), Culmann-Wolff crane stress trajectories, and `Vitamin D` calcium mineralization (`SCALE: your skeleton is not a stone monument — it is a busy highway under non-stop roadworks, where microscopic crews rip up ten percent of the pavement every year so every bone in your body is completely replaced every ten years`)",
        "  2. `P1:06_culmann_1866_and_wolff_1892_femur_trabecular_arch_vs_fairbairn_crane_chart` — Karl Culmann (1866) & Julius Wolff (1892 *Das Gesetz der Transformation der Knochen*) iron crane stress lines vs human proximal femur trabecular arches (`SCALE: hollowing out the middle of your thighbone and stringing microscopic bone arches only along the exact lines of force makes your femur half as heavy as solid rock yet just as strong — the exact trick engineers use to build iron bridges and cranes`)",
        "  3. `P2:02_belchier_1736_duhamel_1739_madder_rings_and_kolliker_1873_osteoclast_osteoblast_chart` — John Belchier (1736) & Duhamel du Monceau (1739) alternating red-and-white madder bone rings + Albert von Kölliker (1873) osteoclast/osteoblast composite chart (`SCALE: bone gets its secret strength from the exact same partnership as reinforced concrete — flexible collagen protein ropes act like the steel rebar that stops bone from snapping, while hard calcium crystals act like the poured cement that stops it from squashing`)",
        "  4. `P3:02_culmann_1866_wolff_1892_trabecular_stress_tennis_arm_and_astronaut_bone_loss_chart` — Culmann (1866) & Wolff (1892) trabecular stress adaptation, tennis serving-arm hypertrophy (`+20–35%`), and astronaut microgravity bone loss (`−1% to −2%/month`) (`SCALE: astronauts on the International Space Station have to strap themselves to treadmills and vacuum-resistance machines for two hours every day — because without gravity tugging on their bones, their own osteoclasts assume they don't need a skeleton anymore and start dissolving it away`)",
        "  5. `P4:02_mccollum_aug_1922_oxidized_cod_liver_oil_and_chick_jul_1922_vienna_rickets_xray_chart` — Elmer McCollum (August 1922 *J. Biol. Chem.*) oxidized cod-liver oil `Vitamin D` proof & Harriette Chick (1 July 1922 *The Lancet*) Vienna 75-infant rickets X-ray trial (`SCALE: Harriette Chick proved that Vitamin D isn't really a vitamin at all — it is a sunlight-powered hormone that your skin brews out of cholesterol whenever ultraviolet rays hit your arms, unlocking the gate that lets calcium from your lunch enter your bones`)",
        "  6. `P5:01_timeline_1736_1928_and_living_skeleton_remodelling_vitamin_d_chart` — completed timeline (1736 → 1928) + 10-year bone remodelling, Wolff's Law & Vitamin D (`SCALE: from crimson pig bones on a London dinner table to an iron crane in Zurich and sunny hospital balconies in Vienna, scientists discovered how your body rebuilds its entire skeleton every ten years`)",
        f"- **£0 verified reuse ({totals['reuse']} row):** `P5:04_table_three_callback` uses the 2.40 s unused moving tail `[5.50s..7.90s]` of `P1:07_table_three_props_1739_ringed_bone_1892_crane_femur_plate_and_1922_cod_liver_oil_bottle`.",
        "",
        "## Mint order",
        "",
        "006 > 007 > 008 > 009 > 010 > 011 > 012 > 013 > 014 > 015 > 016 > 017 > 018 > 019 > 020 > 021 > 022 > 023 > 024 > 025 > 026 > 027 > 028 > 029 > 030 > 031 > 032 > 033 > 034 > 035 > 036 > 037 > 038 > 039 > 040 > 041 > 042 > 043 > 044 > 045 > 046 > 047 > 048 > 049 > 050 > 051 > 052 > 053 > 054 > 055 > 056 > 057 > 058 > 059 > 060 > 061 > 062 > 063 > 064 > 065 > 066 > 067 > 068 > 069 > 070 > 071 > 072 > 073 > 074 > 075 > 076 > 077 > 078 > 079 > 080. `generation_authorized` is `false` on every row.",
    ])
    (EDIT / "PRICE_REVIEW_v01.md").write_text("\n".join(pr_lines) + "\n")
    print(f"079 v01 boards written: {totals['rows']} rows, Flow expected={totals['flow_credits_expected']}")


if __name__ == "__main__":
    main()
