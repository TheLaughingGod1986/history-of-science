#!/usr/bin/env python3
"""HOS 031 (Archimedes' Eureka: Why the Overflowing Bathtub Story Is Wrong) pre-VO plate boards v01. J0479. No mint, no spend.

Built from 00_Brand/Channel-Setup/ideas/031_Archimedes-Galileo-Buoyancy/archimedes_script_master_v01.md
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
        "Part 01 — The Golden Wreath, the Bathtub, and Galileo's Scale",
        [
            ("01_archimedes_syracuse_250bc_and_galileo_1586_underwater_balance", 0.0, 5.5, "A", False, "THE UNDERWATER BALANCE", "Quality",
             "Quality: Short frame 0 / answer image (0:03) + Archimedes in Syracuse around 250 BC lowering a brass beam balance holding a golden wreath crown on one side and a lump of pure gold on the other into a glass tank of water as the silver-mixed crown rises, alongside 22-year-old Galileo in Florence in 1586 winding fine brass wire along the balance arm.",
             STYLE + "In Syracuse around 250 BC, Greek mathematician Archimedes lowers a brass beam balance holding a golden laurel wreath on one side and a solid gold block on the other into a clear tank of water: the wreath rises while young Galileo in Florence in 1586 winds fine brass wire along the scale arm." + QUAL_TAIL,
             {"kind": "WHEN", "label": "SYRACUSE, ~250 BC · FLORENCE, 1586", "timeline_step": "1/6 · ~250 BC (Archimedes discovers buoyancy & tests King Hiero's crown)", "hold_s": 3.5}),
            ("02_crown_meniscus_underwater_balance_syracusia_palimpsest_split", 5.5, 6.0, "B", False, "CROWN, BUOYANCY, PALIMPSEST", "Quality",
             "Quality: complex three-part split composition (King Hiero II's golden wreath crown and a water meniscus bulge on the left; Archimedes' underwater hydrostatic balance tipping and the giant ship Syracusia in the centre; the 1229 Archimedes Palimpsest glowing under Stanford's 2005 X-ray beam on the right).",
             STYLE + "Three-panel period composition: on the left, a golden laurel wreath beside a brimming bronze water basin; in the centre, a submerged brass balance scale tipping beneath a grand ancient wooden ship; on the right, a medieval parchment book glowing with faint geometric diagrams." + QUAL_TAIL,
             None),
            ("03_king_hiero_syracuse_court_weighing_golden_wreath_dry_scale", 11.5, 6.0, "C", False, "SAME WEIGHT — OR STOLEN GOLD?", "Quality",
             "Quality: readable faces (King Hiero II in the royal court of Syracuse around 250 BC holding a gleaming golden laurel wreath on a dry balance scale beside an equal lump of gold while the nervous goldsmith watches).",
             STYLE + "Inside a sunlit marble court in Syracuse around 250 BC, bearded King Hiero II inspects a golden laurel wreath balanced level against a solid gold bar on a dry bronze scale while a nervous goldsmith looks on." + QUAL_TAIL,
             None),
            ("04_pure_gold_vs_silver_doped_crown_volume_and_buoyancy_chart", 17.5, 8.0, "E", False, "13.1 CM³ EXTRA VOLUME = 13.1 G LIFT", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period parchment, an inked diagram compares pure gold (density 19.32 g/cm³, 1,000 g = 51.8 cm³) against a 1,000 g crown mixed with 30% silver (density 10.49 g/cm³, volume = 64.8 cm³): in a 30 cm basin, the 13.1 cm³ difference raises the water level by just 0.18 mm (invisible under surface tension), whereas on Archimedes' and Galileo's 1586 underwater balance the extra 13.1 cm³ of displaced water pushes up on the crown with 13.1 grams of extra buoyant force.",
             {"kind": "DATA", "label": "1,000 G GOLD (51.8 CM³) VS 70/30 CROWN (64.8 CM³): 0.18 MM RISE VS 13.1 G LIFT", "detail": "Inked comparison diagram on period paper showing 1,000 g pure gold (51.8 cm³) vs 1,000 g 70/30 crown (64.8 cm³): a 13.1 cm³ (<1 tbsp) difference that raises a 30 cm bowl by 0.18 mm, but tips an underwater balance by 13.1 g", "scale": "13 cubic centimetres of extra volume is less than one tablespoon of water — raising a wide bowl by less than two sheets of paper, yet tipping an underwater scale by 13 full grams", "who_card": "Archimedes of Syracuse (~287–212 BC) — Greek mathematician and physicist · King Hiero II (~308–215 BC) — Greek ruler of Syracuse · Galileo Galilei (1564–1642) — Italian mathematician and physicist", "when_stamp": "~250 BC · 1586", "hold_s": 3.8}),
            ("05_galileo_brass_wire_windings_bilancetta_arm_pan", 25.5, 5.5, "A", False, "LA BILANCETTA · 1586", "Fast",
             "Fast: daylight macro pan across fine brass wire coils wound tightly along the bronze beam of Galileo's hydrostatic balance between code graphics so two full-frame graphics never run back to back. Nothing emissive, no face.",
             STYLE + "In crisp daylight on a Renaissance workbench, the camera pans closely along a bronze balance arm wrapped in hair-fine coils of gleaming brass wire." + FAST_TAIL,
             None),
            ("06_0_18_mm_water_rise_vs_13_1_g_underwater_balance_scale_card", 31.0, 8.0, "E", False, "LESS THAN ONE TABLESPOON", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period parchment, an inked scale card compares a 0.18-millimetre water rise clinging to a 30 cm bowl's rim (thinner than two sheets of paper, swamped by a 2–3 mm meniscus) against a 13.1-gram upward buoyant force tipping Galileo's wire-wrapped underwater balance.",
             {"kind": "DATA", "label": "0.18 MM WATER RISE (<2 SHEETS OF PAPER) VS 13.1 G BUOYANT LIFT", "detail": "Inked scale comparison of 0.18 mm water-level rise in a 30 cm basin vs 13.1 g buoyant lift on a submerged hydrostatic balance", "scale": "a water-level rise thinner than two sheets of paper becomes a 13-gram push on an underwater balance", "hold_s": 3.8}),
            ("07_table_three_props_golden_wreath_bilancetta_scale_palimpsest", 39.0, 5.5, "C", False, "FLORENCE, 1586", "Fast",
             "Fast: daylight prop table (callback source for Part 05: golden laurel wreath crown beside a solid gold bar, Galileo's wire-wrapped bronze hydrostatic balance over a glass water jar, and the medieval parchment prayer book). Nothing emissive.",
             STYLE + "On a wooden workbench in soft window light sit three objects side by side: a golden laurel wreath beside a gold bar, a wire-wrapped bronze balance scale suspended over a glass tank of water, and an open parchment manuscript." + FAST_TAIL,
             None),
            ("08_explorer_meniscus_bowl_vs_submerged_crown_balance", 62.0, 5.5, "A", True, None, "Quality",
             "Quality: Explorer beat 1 (locked character reference, after 1:00).",
             STYLE + "Peering through a magnifying glass at the rim of a wide water basin where the water bulges without spilling, the Explorer shakes its head, then hangs a tiny gold crown and a gold block on a miniature beam scale, dips both into a glass jar of water, and points in delight as the crown shoots upward." + EXP_TAIL,
             None),
            ("09_vitruvius_writing_scroll_beside_brimming_bronze_basin", 67.5, 5.5, "B", False, "VITRUVIUS · ~25 BC", "Quality",
             "Quality: readable face (Roman architect Vitruvius in a toga around 25 BC writing on a papyrus scroll beside a brimming bronze water basin).",
             STYLE + "In a Roman study around 25 BC, architect Vitruvius in a cream toga writes on a scroll with a reed pen beside a brimming bronze basin of water." + QUAL_TAIL,
             None),
        ],
    ),
    (
        2,
        "Part 02 — The King's Wreath and Vitruvius's Bathtub Myth",
        [
            ("01_archimedes_syracuse_bath_250bc_and_vitruvius_rome_25bc", 73.0, 6.5, "A", False, "SYRACUSE ~250 BC & ROME ~25 BC", "Quality",
             "Quality: readable faces (Archimedes stepping into a brimming stone bath in Syracuse around 250 BC as water spills over the rim, alongside Roman architect Vitruvius writing De Architectura in Rome around 25 BC more than 200 years later).",
             STYLE + "Split period scene: on the left, bearded Archimedes steps into a brimming stone bath in Syracuse as water spills over the edge; on the right, Roman architect Vitruvius writes on a scroll two centuries later." + QUAL_TAIL,
             {"kind": "WHO", "label": "Vitruvius (~80–15 BC) — Roman architect and engineer", "fact_card": "Written 200 years later", "when_stamp": "~250 BC · ~25 BC", "timeline_step": "3/6 · ~25 BC (Vitruvius records the Eureka bathtub story in De Architectura)", "hold_s": 3.8}),
            ("02_gold_19_32_vs_silver_10_49_density_and_crown_volume_diagram", 79.5, 8.0, "E", False, "GOLD (19.32 G/CM³) VS SILVER (10.49 G/CM³)", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked atomic density and volume comparison compares 1,000 grams of pure gold (density 19.32 g/cm³, volume 51.76 cm³) against 1,000 grams of a 70% gold / 30% silver crown (silver density 10.49 g/cm³, volume 64.83 cm³) — identical 1,000 g weight in air, 13.07 cm³ extra volume.",
             {"kind": "DATA", "label": "1,000 G PURE GOLD (51.76 CM³) VS 70/30 GOLD-SILVER CROWN (64.83 CM³)", "detail": "Inked atomic density and volume comparison on period paper showing 1,000 g pure gold (19.32 g/cm³, 51.76 cm³) vs 1,000 g 70% gold / 30% silver crown (64.83 cm³) — identical 1,000 g weight in air, 13.07 cm³ extra volume", "scale": "pure gold is almost twice as dense as silver — so hiding 30% silver inside a one-kilogram crown swells its volume by 13 cubic centimetres, less than a single tablespoon", "hold_s": 3.8}),
            ("03_vitruvius_brimming_pot_spilled_water_myth_demonstration", 87.5, 6.5, "B", False, "VITRUVIUS'S SPILLED WATER", "Fast",
             "Fast: daylight close-up of a golden laurel wreath being lowered on a cord into a wide bronze vessel filled to the brim as a few drops trickle down the spout into a clay cup. Nothing emissive, no face.",
             STYLE + "In crisp daylight, hands lower a golden laurel wreath on a braided cord into a brimming bronze basin as a trickle of water drips from the rim spout into a small clay cup." + FAST_TAIL,
             None),
            ("04_pure_gold_bar_and_larger_silver_bar_on_dry_scale_bench", 94.0, 5.5, "C", False, "TWICE AS DENSE", "Fast",
             "Fast: daylight macro shot of a compact gleaming gold ingot and a noticeably larger silver ingot resting in opposite pans of a dry bronze balance scale at dead level. Nothing emissive, no face.",
             STYLE + "In soft daylight on a stone table, a compact bar of pure gold and a visibly thicker bar of silver sit balanced dead level in the two pans of a bronze scale." + FAST_TAIL,
             None),
        ],
    ),
    (
        3,
        "Part 03 — Twenty-Two-Year-Old Galileo and The Little Balance",
        [
            ("01_galileo_florence_1586_writing_la_bilancetta_meniscus_bowl", 99.5, 6.5, "A", False, "FLORENCE · 1586", "Quality",
             "Quality: readable face (22-year-old Galileo Galilei in a Renaissance doublet in Florence in 1586 writing his first treatise La Bilancetta and examining water surface tension clinging in a 2–3 mm meniscus bulge above the rim of a 30-centimetre bronze bowl).",
             STYLE + "In a Florence workshop in 1586, twenty-two-year-old Galileo Galilei in a Renaissance doublet leans at eye level beside a thirty-centimetre bronze bowl, watching water bulge above the rim without spilling." + QUAL_TAIL,
             {"kind": "FACT", "label": "Meniscus hides 0.18 mm rise", "when_stamp": "1586", "timeline_step": "5/6 · 1586 (22-year-old Galileo writes La Bilancetta, proving the underwater balance)", "hold_s": 3.8}),
            ("02_archimedes_prop_7_and_galileo_1586_hydrostatic_balance_diagram", 106.0, 8.0, "E", False, "948.2 G VS 935.2 G IN WATER (13.1 G TIP)", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked schematic of Archimedes' Proposition 7 underwater balance (On Floating Bodies) and Galileo's 1586 wire-wrapped La Bilancetta shows 1,000 g pure gold (51.8 cm³ → −51.8 g buoyancy = 948.2 g apparent weight in water) vs 1,000 g 70/30 crown (64.8 cm³ → −64.8 g buoyancy = 935.2 g in water), tipping by 13.1 g.",
             {"kind": "DATA", "label": "PROPOSITION 7 IN WATER: 948.2 G (GOLD) VS 935.2 G (CROWN) = 13.1 G TIP", "detail": "Inked schematic on period paper of Archimedes' Proposition 7 underwater balance and Galileo's 1586 wire-wrapped La Bilancetta showing 1,000 g gold (948.2 g in water) vs 1,000 g 70/30 crown (935.2 g in water), tipping by 13.1 g", "scale": "instead of trying to spot a 0.18-millimetre water rise swamped by 3 millimetres of surface tension, dunking the balance turns that tiny volume difference into a 13-gram weight difference any scale can feel", "hold_s": 3.8}),
            ("03_galileo_counting_brass_wire_coils_with_thumbnail_closeup", 114.0, 6.5, "B", False, "PROPOSITION 7 IN WATER", "Quality",
             "Quality: readable face and hands (22-year-old Galileo in 1586 running his thumbnail across the fine brass wire coils on the arm of La Bilancetta as the underwater golden crown rises and the pure gold block sinks).",
             STYLE + "Florence, 1586: young Galileo Galilei slides a bronze counterweight and runs his thumbnail across fine brass wire coils on his balance arm as the submerged golden wreath rises in the water tank." + QUAL_TAIL,
             None),
            ("04_water_meniscus_bulge_on_30cm_bronze_rim_macro", 120.5, 5.5, "C", False, "2–3 MM SURFACE TENSION", "Fast",
             "Fast: daylight macro shot at rim level of water bulging 2–3 millimetres above the lip of a bronze basin by surface tension without spilling over, alongside wet droplets clinging to golden laurel leaves. Nothing emissive, no face.",
             STYLE + "In crisp daylight at rim level, water bulges in a smooth curved meniscus above the bronze lip of a wide basin without spilling, while droplets cling to a wet golden laurel leaf." + FAST_TAIL,
             None),
        ],
    ),
    (
        4,
        "Part 04 — The 4,000-Tonne Super-Ship and the Erased Prayer Book — Midpoint Twist",
        [
            ("01_syracusia_240bc_launch_and_myronas_1229_heiberg_1906_palimpsest", 126.0, 6.5, "A", False, "SYRACUSIA (~240 BC) & 1229 PALIMPSEST", "Quality",
             "Quality: readable faces (Archimedes overseeing the launch of King Hiero II's 110-metre, 4,000-tonne super-ship Syracusia in ~240 BC, dissolving into scribe Johannes Myronas in April 1229 scraping Archimedes' parchment into a prayer book and Danish scholar Johan Ludvig Heiberg in 1906 examining it with a magnifying glass in Constantinople).",
             STYLE + "Split period scene: on the left, Archimedes stands on the Syracuse quay beside the towering wooden hull of the giant ship Syracusia; on the right, scholar Johan Ludvig Heiberg in 1906 peers through a magnifying glass at faint geometric diagrams beneath medieval prayers." + QUAL_TAIL,
             {"kind": "WHO", "label": "Johannes Myronas (fl. 1229) — Christian scribe · Johan Ludvig Heiberg (1854–1928) — Danish philologist and historian", "fact_card": "Scraped into a prayer book", "when_stamp": "~240 BC · 212 BC · April 1229 · 1906", "timeline_step": "2/6 · ~240 BC (4,000-tonne Syracusia) & 4/6 · April 1229 (Archimedes Palimpsest scraped)", "hold_s": 3.8}),
            ("02_syracusia_4000t_displacement_and_2005_stanford_xray_palimpsest_diagram", 132.5, 8.0, "E", False, "4,000-TONNE DISPLACEMENT & 2005 X-RAY BEAM", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked two-part diagram shows (1) the 4,000-tonne ship Syracusia floating because its hollow hull displaces 4,000 tonnes of seawater while a solid metal bolt sinks, and (2) Stanford's May 2005 – August 2008 synchrotron X-ray fluorescence beam exciting microscopic iron atoms in Archimedes' erased 10th-century ink beneath the April 1229 prayer text.",
             {"kind": "DATA", "label": "4,000-TONNE SYRACUSIA HULL DISPLACEMENT & 2005 STANFORD X-RAY RECOVERY", "detail": "Inked two-part diagram on period paper showing (1) buoyancy of the 4,000-tonne ship Syracusia displacing 4,000 tonnes of seawater vs a sinking solid bolt, and (2) Stanford's 2005–2008 synchrotron X-ray fluorescence recovery of Archimedes' iron ink", "scale": "a 4,000-tonne palace ship floats effortlessly because its hollow hull pushes aside 4,000 tonnes of seawater — while a solid one-ounce bolt sinks because it pushes aside only a thimbleful", "when_stamp": "May 2005", "hold_s": 3.8}),
            ("03_stanford_2005_synchrotron_xray_scanning_archimedes_palimpsest", 140.5, 6.5, "B", False, "READ BY X-RAYS IN 2005", "Quality",
             "Quality: glowing X-ray fluorescence monitor + physicist in May 2005 at the Stanford Linear Accelerator Center scanning a mounted parchment page of the Archimedes Palimpsest as erased Greek diagrams of floating bodies glow orange.",
             STYLE + "At the Stanford synchrotron laboratory in May 2005, a physicist watches a precision scanner move a medieval parchment leaf across a narrow beam mount while hidden Greek geometric diagrams light up on a display." + QUAL_TAIL,
             None),
            ("04_explorer_xray_lantern_revealing_archimedes_spirals_prayer_book", 147.0, 5.5, "B", True, None, "Quality",
             "Quality: Explorer beat 2 (locked character reference).",
             STYLE + "Holding a medieval prayer book under a magnifying glass, the Explorer switches on a warm lantern behind the parchment: the top prayers fade translucent and Archimedes' hidden geometric spirals and balance diagrams shine through." + EXP_TAIL,
             None),
        ],
    ),
    (
        5,
        "Part 05 — Why Heavy Steel Ships Float and the Keyhole Into a Living Stomach",
        [
            ("01_timeline_250bc_2008_and_hydrostatic_depth_pressure_chart", 152.5, 8.5, "E", False, "P = ρ g h · UPWARD PRESSURE WINS", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, the 6-date timeline completes: ~250 BC (Archimedes discovers buoyancy & tests crown) · ~240 BC (4,000-tonne Syracusia) · ~25 BC (Vitruvius bathtub account) · April 1229 (Myronas scrapes Archimedes Palimpsest) · 1586 (Galileo writes La Bilancetta) · 1906 & May 2005–2008 (Heiberg rediscovers Palimpsest & Stanford X-rays recover text), alongside an inked hydrostatic depth-pressure diagram (P = ρ g h => F_b = ρ V g).",
             {"kind": "DATA", "label": "DEPTH PRESSURE (P = ρ g h) → UPWARD FORCE F_b = ρ V g", "detail": "Animated 6-date timeline (~250 BC → 2008) alongside an inked hydrostatic pressure diagram showing water pressure increasing with depth (P = ρ g h) so upward pressure on the bottom exceeds downward pressure on the top by F_b = ρ V g", "scale": "whether it is a 1-kilogram crown in a bowl, a 100,000-tonne steel ship in the ocean, or a continent floating on the mantle, every submerged object is lifted by the exact weight of the fluid it pushes aside", "fact_card": "Deeper water pushes up harder", "when_stamp": "~250 BC–2008", "timeline_step": "6/6 · 1906 & May 2005–2008 (Heiberg rediscovers Palimpsest; Stanford X-rays recover text)", "hold_s": 3.8}),
            ("02_archimedes_screw_and_floating_hull_model_in_water_tank", 161.0, 5.5, "A", False, "UPWARD PRESSURE WINS", "Fast",
             "Fast: daylight close-up of a wooden hull cross-section model floating high in a clear glass tank beside a bronze Archimedes' screw spiral lifting water. Nothing emissive, no face.",
             STYLE + "In crisp daylight, a hollow wooden ship hull model floats high in a clear glass water tank beside a turning bronze Archimedes' screw spiral." + FAST_TAIL,
             None),
            ("03_beaumont_1825_silk_string_and_marshall_1984_pylori_beaker_handoff", 166.5, 6.5, "C", False, "THE STOMACH WINDOW", "Quality",
             "Quality: readable faces (US Army surgeon William Beaumont at Fort Mackinac, Michigan, in May 1825 lowering a piece of beef on a silk string through Alexis St. Martin's healed stomach window, beside Australian doctor Barry Marshall in July 1984 raising a glass beaker of H. pylori bacteria — handoff to 032 Stomach Ulcers).",
             STYLE + "Fort Mackinac, Michigan, May 1825, and Perth, July 1984: surgeon William Beaumont holds a silk thread with a small piece of beef beside patient Alexis St. Martin, while physician Barry Marshall in a lab coat raises a glass beaker of cloudy broth." + QUAL_TAIL,
             {"kind": "WHEN", "label": "MAY 1825 · JULY 1984", "hold_s": 3.5}),
            ("04_table_three_callback", 173.0, 2.4, "C", False, None, "reuse",
             "Reuse: verified unused moving window [5.50s..7.90s] of P1:07_table_three_props_golden_wreath_bilancetta_scale_palimpsest (callback, £0).",
             "Reuse P1:07_table_three_props_golden_wreath_bilancetta_scale_palimpsest [5.50s..7.90s] (2.40s distinct non-overlapping tail window from 8.00s source clip).",
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
                row["reuse_of"] = "P1:07_table_three_props_golden_wreath_bilancetta_scale_palimpsest"
                row["reuse_window_s"] = [5.5, 7.9]
                row["reuse_audit"] = {
                    "source_row": "P1:07_table_three_props_golden_wreath_bilancetta_scale_palimpsest",
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
            "film": "031_Archimedes-Galileo-Buoyancy",
            "part": p_idx,
            "title": p_title,
            "version": "v01",
            "timing_status": "pre_vo_script_clock (built from archimedes_script_master_v01.md; retimes onto Scribe STT once VO locks)",
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
        "film": "031_Archimedes-Galileo-Buoyancy",
        "version": "v01",
        "date": "2026-10-17",
        "owner": "gemini (J0479)",
        "status": "PRE_VO_BOARDS_V01_NO_MINT",
        "generation_authorized": False,
        "script": "00_Brand/Channel-Setup/ideas/031_Archimedes-Galileo-Buoyancy/archimedes_script_master_v01.md",
        "sources": "00_Brand/Channel-Setup/ideas/031_Archimedes-Galileo-Buoyancy/SOURCES_v01.md",
        "credit_snapshot": {
            "flow_Balance": 23740,
            "flow_floor": 0,
            "flow_read_at": "2026-10-15T21:42:22Z",
            "vertex_promo_gbp": 71.02,
            "vertex_usable_gbp": 70.02,
        },
        "totals": totals,
        "per_part": per_part_summary,
        "mint_order": "006 > 007 > 008 > 009 > 010 > 011 > 012 > 013 > 014 > 015 > 016 > 017 > 018 > 019 > 020 > 021 > 022 > 023 > 024 > 025 > 026 > 027 > 028 > 029 > 030 > 031. Nothing in 031 is generation_authorized.",
    }
    (EDIT / "PICTURE_PLAN_v01.json").write_text(json.dumps(plan, indent=2) + "\n")

    sl = [
        "# 031 Archimedes' Eureka: Why the Overflowing Bathtub Story Is Wrong — Shot list & plate boards v01 (pre-VO)",
        "",
        "Gemini, 17 Oct 2026, J0479. Built from `archimedes_script_master_v01.md` (92.4 PASS) and `SOURCES_v01.md`.",
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
        "# 031 price review v01 (pre-VO plate boards)",
        "",
        "Gemini, 17 Oct 2026, J0479. Boards only. **No mint. No spend. No merge.**",
        "Prepared from `archimedes_script_master_v01.md` (92.4 PASS) and `SOURCES_v01.md` so 031's full plate board rows, non-emissive Fast prompts, £0 code graphics, and Teach-on-Screen overlays are ready to re-time the moment long VO locks. Parked for Chief.",
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
        f"- **Quality ({totals['Quality']} rows):** readable faces (Archimedes, King Hiero II, Galileo Galilei, Vitruvius, Johannes Myronas, Johan Ludvig Heiberg, William Beaumont, Barry Marshall), Stanford 2005 synchrotron scanner, and the 2 Explorer beats.",
        f"- **Fast ({totals['Fast']} rows, non-emissive):** daylight prop and laboratory shots (Galileo's brass wire windings on La Bilancetta pan, 3-object callback bench, brimming bronze vessel dripping into clay cup, gold vs silver ingots balanced on dry scale, 2–3 mm water surface-tension meniscus on bronze rim, wooden ship hull & Archimedes' screw in clear water tank). Zero candles, flames, sparks, or glowing elements on Fast.",
        f"- **£0 code graphics ({totals['code_graphic']} rows):**",
        "  1. `P1:04_pure_gold_vs_silver_doped_crown_volume_and_buoyancy_chart` — 1,000 g pure gold (51.8 cm³) vs 1,000 g 70/30 crown (64.8 cm³): 13.1 cm³ volume difference raising a 30 cm bowl by 0.18 mm vs 13.1 g buoyant lift on an underwater balance (`SCALE: 13 cubic centimetres of extra volume is less than one tablespoon of water — raising a wide bowl by less than two sheets of paper, yet tipping an underwater scale by 13 full grams`)",
        "  2. `P1:06_0_18_mm_water_rise_vs_13_1_g_underwater_balance_scale_card` — 0.18 mm water-level rise (<2 sheets of paper) vs 13.1 g buoyant push on Galileo's wire-wrapped underwater balance (`SCALE: a water-level rise thinner than two sheets of paper becomes a 13-gram push on an underwater balance`)",
        "  3. `P2:02_gold_19_32_vs_silver_10_49_density_and_crown_volume_diagram` — atomic density and volume comparison of pure gold (19.32 g/cm³, 51.76 cm³) vs 70/30 gold-silver crown (10.49 g/cm³ silver, 64.83 cm³ total) (`SCALE: pure gold is almost twice as dense as silver — so hiding 30% silver inside a one-kilogram crown swells its volume by 13 cubic centimetres, less than a single tablespoon`)",
        "  4. `P3:02_archimedes_prop_7_and_galileo_1586_hydrostatic_balance_diagram` — Archimedes' Proposition 7 underwater balance and Galileo's 1586 wire-wrapped La Bilancetta showing 948.2 g (gold in water) vs 935.2 g (crown in water) (`SCALE: instead of trying to spot a 0.18-millimetre water rise swamped by 3 millimetres of surface tension, dunking the balance turns that tiny volume difference into a 13-gram weight difference any scale can feel`)",
        "  5. `P4:02_syracusia_4000t_displacement_and_2005_stanford_xray_palimpsest_diagram` — 4,000-tonne ship Syracusia displacing 4,000 tonnes of seawater vs a sinking solid bolt, and Stanford's 2005–2008 synchrotron X-ray fluorescence recovery of Archimedes' iron ink (`SCALE: a 4,000-tonne palace ship floats effortlessly because its hollow hull pushes aside 4,000 tonnes of seawater — while a solid one-ounce bolt sinks because it pushes aside only a thimbleful`)",
        "  6. `P5:01_timeline_250bc_2008_and_hydrostatic_depth_pressure_chart` — completed 6-date timeline (~250 BC → 2008) + hydrostatic depth-pressure diagram (P = ρ g h => F_b = ρ V g) (`SCALE: whether it is a 1-kilogram crown in a bowl, a 100,000-tonne steel ship in the ocean, or a continent floating on the mantle, every submerged object is lifted by the exact weight of the fluid it pushes aside`)",
        f"- **£0 verified reuse ({totals['reuse']} row):** `P5:04_table_three_callback` uses the 2.40 s unused moving tail `[5.50s..7.90s]` of `P1:07_table_three_props_golden_wreath_bilancetta_scale_palimpsest`.",
        "",
        "## Mint order",
        "",
        "006 > 007 > 008 > 009 > 010 > 011 > 012 > 013 > 014 > 015 > 016 > 017 > 018 > 019 > 020 > 021 > 022 > 023 > 024 > 025 > 026 > 027 > 028 > 029 > 030 > 031. `generation_authorized` is `false` on every row.",
    ])
    (EDIT / "PRICE_REVIEW_v01.md").write_text("\n".join(pr_lines) + "\n")
    print(f"031 v01 boards written: {totals['rows']} rows, Flow expected={totals['flow_credits_expected']}")


if __name__ == "__main__":
    main()
