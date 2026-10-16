#!/usr/bin/env python3
"""HOS 081 (Plant Hormones: How Darwin's Blindfolded Grass Sees Light) pre-VO plate boards v01. J0738. No mint, no spend.

Built from 00_Brand/Channel-Setup/ideas/081_Darwin-Went-Neljubow-Gane-Plant-Tropisms-Auxin/plant_tropisms_script_master_v01.md
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
        "Part 01 — The Blindfolded Grass Tip, the 3:00 a.m. Jelly Cube & the Invisible Gas in the Fruit Bowl",
        [
            ("01_darwin_1880_blindfolded_canary_grass_tip_vs_uncovered_shoot_and_auxin_shaded_cell_elongation", 0.0, 5.5, "A", False, "HOW PLANTS SEE WITHOUT EYES", "Quality",
             "Quality: Short frame 0 / answer image (0:03) + side by side, in Charles and Francis Darwin's dark study at Down House in November 1880, an uncovered canary-grass seedling bends sharply toward a single candle flame while a seedling wearing a tiny 2-millimetre tin-foil cap on its extreme tip stands ramrod straight and blind, beside a cross-section of a plant shoot where blue light drives green auxin hormone molecules to the shaded side so the shaded cells stretch longer and curve the stem toward the sun.",
            STYLE + "Split botanical-and-cellular scene: on the left in Charles and Francis Darwin's 1880 Down House study, an uncovered canary-grass shoot bends toward a candle while a twin shoot capped with a tiny silver tin-foil helmet stands straight; on the right, a cutaway green stem shows auxin molecules gathering on the shaded side as shaded cells elongate." + QUAL_TAIL,
             {"kind": "WHEN", "label": "DOWN HOUSE, KENT, NOVEMBER 1880", "timeline_step": "1/3 · 1806, Nov 1880 & 1900 (Thomas Andrew Knight's waterwheel, Charles and Francis Darwin prove the 1–2 mm grass tip senses light at Down House, and Gottlieb Haberlandt and Bohumil Němec discover falling-starch statolith gravity sensors in root caps)", "hold_s": 3.5}),
            ("02_darwin_1880_haberlandt_nemec_1900_went_1926_and_neljubow_1901_gane_1934_split", 5.5, 6.0, "B", False, "BLINDFOLDED GRASS, AGAR JELLY, ETHYLENE GAS", "Quality",
             "Quality: complex three-part composition (Charles and Francis Darwin at Down House in November 1880 fitting tin-foil caps onto canary-grass coleoptile tips alongside Gottlieb Haberlandt and Bohumil Němec in 1900 watching starch statoliths sink in root-cap cells; Frits Warmolt Went in Utrecht at 3:00 a.m. on 17 April 1926 placing severed oat tips onto 2-millimetre agar jelly blocks to isolate auxin; and Dmitry Neljubow in St Petersburg in 1901 and Richard Gane in Cambridge in 1934 discovering ethylene ripening gas).",
             STYLE + "Three-panel period composition: on the left, Charles and Francis Darwin in 1880 Down House placing tiny tin-foil caps on grass seedlings beside a root-cap microscope slide; in the centre, Frits Went in his 1926 Utrecht lab setting oat tips on tiny agar jelly cubes; on the right, Dmitry Neljubow in 1901 St Petersburg and Richard Gane in 1934 Cambridge with glass cold traps and apples." + QUAL_TAIL,
             None),
            ("03_horizontal_seedling_root_bending_down_via_statoliths_and_shoot_bending_up_toward_window_light", 11.5, 6.0, "C", False, "PHOTOTROPISM & GRAVITROPISM", "Quality",
             "Quality: complex botanical reveal (a knocked-over seedling in a room whose root tip curves downward via falling statolith starch grains while its shoot curves upward against gravity and bends toward a sunlit window).",
             STYLE + "In a cross-section of soil and sunlit room air, a tipped terracotta pot holds a green seedling whose white root tip curves downward into the soil as microscopic starch grains settle in the root cap while its green shoot curves upward toward a sunlit window." + QUAL_TAIL,
             {"kind": "WHEN", "label": "NOVEMBER 1880 · 1900 · 1901 · 1913 · 17 APRIL 1926 · 1934", "timeline_step": "1/3 · Nov 1880 & 1900 (Darwin, Haberlandt & Němec) · 2/3 · 1913 & 17 Apr 1926 (Boysen-Jensen & Frits Went) · 3/3 · 1901 & 29 Dec 1934 (Neljubow & Richard Gane)", "hold_s": 3.5}),
            ("04_darwin_1880_haberlandt_1900_went_1926_and_gane_1934_plant_tropisms_auxin_ethylene_chart", 17.5, 8.0, "E", False, "DARWIN (1880) & WENT (17 APR 1926): AUXIN SHADED-SIDE CELL ELONGATION, ROOT-CAP STATOLITHS (1900) & ETHYLENE C2H4 RIPENING (1901/1934)", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked Plant Tropisms, Auxin & Ethylene Hormone chart from Charles & Francis Darwin (November 1880 The Power of Movement in Plants), Gottlieb Haberlandt & Bohumil Němec (1900 Ber. Dtsch. Bot. Ges.), Peter Boysen-Jensen (1910–1913), Frits Warmolt Went (1926/1928 Proc. K. Akad. Wet. Amsterdam 30: 10–19), and Dmitry Neljubow (1901) & Richard Gane (1934 Nature 134: 1008) shows 1) Phototropism: blue light on the 1–2 mm coleoptile tip redistributes auxin (indole-3-acetic acid) to the shaded side, elongating shaded stem cells; 2) Gravitropism: falling amyloplast statoliths in root-cap cells redirect auxin to the lower side, inhibiting lower root cells so the root bends down; and 3) Ethylene (C2H4) gas triggering fruit ripening.",
             {"kind": "DATA", "label": "DARWIN (1880) & FRITS WENT (17 APR 1926) COLEOPTILE PHOTOTROPISM & AGAR-BLOCK AUXIN CURVATURE BIOASSAY CHART", "detail": "Inked Darwin (1880) & Frits Went (17 April 1926) coleoptile phototropism & agar-block curvature bioassay chart (uncovered tip bends toward light; tin-foil-capped tip = 0° bend; asymmetric auxin agar block in darkness = curvature proportional to auxin concentration) on period paper", "scale": "a plant doesn't bend toward a window by flexing muscles on the sunny side — it pumps auxin growth hormone to the shady side so the shady cells inflate with water and stretch longer like the outer rail of a curving train track", "who_card": "Charles Darwin (1809–1882) — English naturalist · Francis Darwin (1848–1925) — English botanist · Gottlieb Haberlandt (1854–1945) — Austrian botanist · Bohumil Němec (1873–1966) — Czech botanist · Peter Boysen-Jensen (1883–1959) — Danish plant physiologist · Frits Warmolt Went (1903–1990) — Dutch-American botanist · Dmitry Nikolayevich Neljubow (1876–1926) — Russian plant physiologist · Richard Gane (1904–1981) — British plant physiologist", "when_stamp": "November 1880 · 1900 · 1901 · 1913 · 17 April 1926 · 1934", "hold_s": 3.8}),
            ("05_darwin_1880_book_tin_foil_caps_and_went_1926_agar_block_cutter_pan", 25.5, 5.5, "A", False, "SHADED CELLS STRETCH LONGER", "Fast",
             "Fast: daylight macro pan across Charles and Francis Darwin's 1880 book The Power of Movement in Plants, tiny rolled tin-foil coleoptile caps, and Frits Went's brass agar-block guillotine cutter on an oak bench between code graphics so two full-frame graphics never run back to back. Nothing emissive, no face.",
             STYLE + "In crisp daylight on an oak botanical workbench, the camera pans smoothly across an open 1880 botany volume, miniature silver tin-foil caps in a glass dish, and a brass agar-jelly cutter." + FAST_TAIL,
             None),
            ("06_frits_went_17_apr_1926_utrecht_avena_agar_block_curvature_bioassay_chart", 31.0, 8.0, "E", False, "UTRECHT, 17 APRIL 1926", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period parchment, an inked Frits Went (17 April 1926, Utrecht) Avena Coleoptile Agar-Block Bioassay diagram shows 12 severed oat tips placed on a tiny agar jelly block for 1 hour, then the lifeless agar cube placed off-centre on a decapitated oat stump in complete darkness, bending the shoot 10°–20° away from the agar block.",
             {"kind": "DATA", "label": "17 APR 1926 FRITS WENT (PROC. K. AKAD. WET. AMSTERDAM): AVENA AGAR-BLOCK CURVATURE ANGLE VS AUXIN CONCENTRATION", "detail": "Inked Frits Went (1926/1928) Avena curvature angle (degrees of bending vs number of coleoptile tips / auxin concentration in agar) chart on period paper", "scale": "just one ten-millionth of a gram of auxin trapped inside a two-millimetre cube of jelly is enough to make thousands of oat shoots bend in pitch darkness", "hold_s": 3.8}),
            ("07_table_three_props_1880_darwin_tinfoil_cap_1926_went_agar_block_rack_and_1934_gane_apple_jar", 39.0, 5.5, "C", False, "1880 TO 1934", "Fast",
             "Fast: daylight prop table (callback source for Part 05: Darwin's 1880 potted canary-grass shoot with a tiny tin-foil cap, Frits Went's 1926 brass Avena rack holding agar jelly blocks, and Richard Gane's 1934 glass bell jar of Worcester Pearmain apples). Nothing emissive.",
             STYLE + "On an oak workbench in soft window light sit three objects side by side: a terracotta pot of canary-grass seedlings with tiny tin-foil caps, a brass clamp rack holding agar jelly cubes, and a glass bell jar containing red apples." + FAST_TAIL,
             None),
            ("08_explorer_placing_tinfoil_hat_on_left_oat_shoot_and_agar_jelly_cube_on_right_shoot_bending_toward_lantern", 62.0, 5.5, "A", True, None, "Quality",
             "Quality: Explorer beat 1 (locked character reference, after 1:00).",
             STYLE + "Standing between two giant potted oat shoots in a Victorian greenhouse beside a brass lantern, the Explorer places a tiny silver tin-foil cap over the left shoot tip while setting a translucent agar jelly cube onto the shaded edge of the right shoot stump so its shaded side stretches and curves toward the lantern." + EXP_TAIL,
             None),
            ("09_richard_gane_1934_cambridge_56kg_apples_cold_trap_ethylene_isolation", 67.5, 5.5, "B", False, "CAMBRIDGE, 1934", "Quality",
             "Quality: readable face (in Cambridge in December 1934, British plant physiologist Richard Gane collects air streaming over 56 kilograms of ripening Worcester Pearmain apples through glass cold traps at -65 °C to isolate ethylene gas).",
             STYLE + "In a 1934 Cambridge laboratory, British plant physiologist Richard Gane inspects frosted glass U-tube cold traps connected to a sealed chamber filled with ripening red Worcester Pearmain apples." + QUAL_TAIL,
             {"kind": "WHEN", "label": "CAMBRIDGE, 29 DECEMBER 1934", "timeline_step": "3/3 · 1901 & 29 Dec 1934 (Dmitry Neljubow discovers ethylene bends pea shoots in St Petersburg, and Richard Gane in Cambridge proves ripening apples synthesize ethylene gas)", "hold_s": 3.5}),
        ],
    ),
    (
        2,
        "Part 02 — November 1880 & 1900: Charles & Francis Darwin's Blindfolded Grass Tips (Phototropism) & Falling-Starch Gravity Sensors (Gravitropism)",
        [
            ("01_charles_and_francis_darwin_nov_1880_down_house_tinfoil_caps_and_haberlandt_nemec_1900_statoliths", 73.0, 6.5, "A", False, "2MM FOIL CAP BLINDED GRASS", "Quality",
             "Quality: readable faces (English naturalist Charles Darwin and botanist Francis Darwin at Down House in November 1880 fitting tiny 2-mm tin-foil caps and blackened glass tubes onto canary-grass coleoptile tips, dissolving to Austrian botanist Gottlieb Haberlandt and Czech botanist Bohumil Němec in 1900 discovering falling starch statoliths in root-cap cells).",
             STYLE + "Split period scene: on the left in 1880 Down House, elderly Charles Darwin and Francis Darwin fit tiny tin-foil caps onto canary-grass seedling tips; on the right in 1900 Graz and Prague, Gottlieb Haberlandt and Bohumil Němec examine root-cap cells packed with settling starch grains under brass microscopes." + QUAL_TAIL,
             {"kind": "FACT", "label": "2mm foil cap blinded grass", "who_card": "Thomas Andrew Knight (1759–1838) — British horticulturist and botanist", "when_stamp": "1806 · November 1880 · 1900", "timeline_step": "1/3 · 1806, Nov 1880 & 1900 (Knight's waterwheel, Charles & Francis Darwin's blindfolded coleoptile tips, and Haberlandt & Němec's root-cap statoliths)", "hold_s": 3.8}),
            ("02_darwin_nov_1880_five_condition_coleoptile_tip_and_haberlandt_nemec_1900_statolith_chart", 79.5, 8.0, "E", False, "NOV 1880 CHARLES & FRANCIS DARWIN (5-CONDITION COLEOPTILE TIP PHOTOTROPISM) & 1900 HABERLANDT & NĚMEC (ROOT-CAP STATOLITH GRAVITROPISM)", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked Charles & Francis Darwin (November 1880 The Power of Movement in Plants) 5-condition coleoptile tip experiment (1: intact bends; 2: tip cut off = no bend; 3: opaque tin-foil cap on tip = no bend; 4: clear glass cap on tip = bends; 5: opaque collar on lower stem = bends) alongside Haberlandt & Němec's (1900) root-cap statolith sedimentation diagram.",
             {"kind": "DATA", "label": "NOV 1880 DARWIN (5-CONDITION COLEOPTILE PHOTOTROPISM) & 1900 HABERLANDT-NĚMEC (ROOT-CAP AMYLOPLAST STATOLITH SEDIMENTATION)", "detail": "Inked Charles & Francis Darwin (November 1880 The Power of Movement in Plants) 5-condition coleoptile tip experiment (1: intact bends; 2: tip cut off = no bend; 3: opaque tin-foil cap on tip = no bend; 4: clear glass cap on tip = bends; 5: opaque collar on lower stem = bends) alongside Haberlandt & Němec's (1900) root-cap statolith sedimentation diagram on period paper", "scale": "covering just the top one-and-a-half millimetres of a seedling with tin foil while leaving the rest of the stem in bright sunlight is like putting a blindfold over a runner's eyes while leaving their legs free — the muscles work, but they have no idea which way to turn", "hold_s": 3.8}),
            ("03_down_house_1880_black_sand_tray_tinfoil_and_glass_caps_with_power_of_movement_book_closeup", 87.5, 6.5, "B", False, "1880 — DARWIN'S COLEOPTILE TIP EXPERIMENT", "Fast",
             "Fast: daylight macro shot of Down House wooden seedling trays filled with black sand where 1-mm canary-grass tips poke out beside tin-foil caps, clear glass micro-tubes, and page 474 of The Power of Movement in Plants on a table. Nothing emissive, no face.",
             STYLE + "In crisp daylight on a Victorian study table, a wooden tray of canary-grass shoots with tiny tin-foil and clear glass caps sits beside an open 1880 illustrated botanical book." + FAST_TAIL,
             None),
            ("04_thomas_andrew_knight_1806_wooden_waterwheel_and_root_cap_statolith_cutaway_model_pan", 94.0, 5.5, "C", False, "1806 & 1900 — WATERWHEEL & ROOT-CAP STATOLITHS", "Fast",
             "Fast: daylight close-up pan across a miniature 1806 wooden waterwheel rimmed with sprouted bean seedlings alongside a sculpted cutaway root-cap cell model showing dense starch statolith spheres resting on the lower cell wall. Nothing emissive, no face.",
             STYLE + "In bright window light on an oak bench, a small wooden waterwheel holding sprouted bean seedlings sits beside a sculpted cutaway root-cap cell model with white starch spheres settled on its bottom floor." + FAST_TAIL,
             None),
        ],
    ),
    (
        3,
        "Part 03 — 1913 & 17 April 1926, 3:00 a.m.: Boysen-Jensen's Gelatin Bridge & Frits Went's Agar-Jelly Isolation of Auxin — Midpoint Twist",
        [
            ("01_peter_boysen_jensen_1913_gelatin_mica_and_frits_went_17_apr_1926_3am_utrecht_auxin_eureka", 99.5, 6.5, "A", False, "SHADY CELLS STRETCH LONGER", "Quality",
             "Quality: readable faces (Danish plant physiologist Peter Boysen-Jensen in Copenhagen in 1913 testing gelatin vs shaded-side mica flakes and Hungarian botanist Árpád Paál in 1919, dissolving to 23-year-old Dutch botanist Frits Warmolt Went at 3:00 a.m. on 17 April 1926 in his Utrecht laboratory watching headless oat shoots bend away from lifeless auxin-soaked agar jelly cubes).",
             STYLE + "Split period scene: on the left in 1913 Copenhagen, Peter Boysen-Jensen inserts a thin mica flake into the shaded side of an oat coleoptile; on the right in 1926 Utrecht, young Frits Went examines a row of decapitated oat shoots curved away from tiny agar jelly cubes." + QUAL_TAIL,
             {"kind": "FACT", "label": "Shady cells stretch longer", "who_card": "Árpád Paál (1889–1943) — Hungarian botanist · Kenneth Vivian Thimann (1904–1997) — British-American plant physiologist", "when_stamp": "1910 · 1913 · 1919 · 17 April 1926 · 1927", "timeline_step": "2/3 · 1913 & 17 Apr 1926 (Boysen-Jensen proves the signal crosses gelatin on the shaded side, and Frits Went isolates auxin in agar jelly at 3:00 a.m. in Utrecht)", "hold_s": 3.8}),
            ("02_boysen_jensen_1913_paal_1919_and_frits_went_1926_cholodny_went_auxin_redistribution_chart", 106.0, 8.0, "E", False, "1913 BOYSEN-JENSEN (SHADED-SIDE MICA VS GELATIN), 1919 PAÁL & 17 APR 1926 FRITS WENT (AGAR-BLOCK AUXIN & CHOLODNY-WENT STEM VS ROOT CURVE)", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked Boysen-Jensen (1913), Árpád Paál (1919) & Frits Went (17 April 1926) Cholodny–Went Auxin Redistribution diagram (gelatin passes signal; mica on shaded side blocks bending; asymmetric auxin agar block bends shoot in dark; opposite auxin dose-response curves in stems vs roots).",
             {"kind": "DATA", "label": "1913 BOYSEN-JENSEN, 1919 PAÁL & 1926–1927 CHOLODNY–WENT AUXIN REDISTRIBUTION & STEM VS ROOT DOSE-RESPONSE CHART", "detail": "Inked Boysen-Jensen (1913), Árpád Paál (1919) & Frits Went (17 April 1926) Cholodny–Went Auxin Redistribution diagram (gelatin passes signal; mica on shaded side blocks bending; asymmetric auxin agar block bends shoot in dark; opposite auxin dose-response curves in stems vs roots) on period paper", "scale": "the exact same auxin hormone molecule makes a shoot grow up toward the sun and a root grow down into the soil — because in stems extra auxin acts like an accelerator on the shady side, while in roots extra auxin acts like a brake on the bottom side", "hold_s": 3.8}),
            ("03_utrecht_1926_avena_coleoptile_rack_2mm_agar_blocks_protractor_and_notebook_closeup", 114.0, 6.5, "B", False, "17 APRIL 1926 — FRITS WENT ISOLATES AUXIN", "Fast",
             "Fast: daylight macro shot of Frits Went's 1926 Utrecht brass Avena coleoptile holder with decapitated oat shoots bent 15° under 2×2 mm agar blocks beside a glass plate of severed oat tips and a brass protractor on a bench. Nothing emissive, no face.",
             STYLE + "In crisp daylight on a 1926 Utrecht botany bench, a brass rack of curved decapitated oat shoots topped with tiny agar jelly cubes sits beside a glass slide of twelve oat tips and a brass protractor." + FAST_TAIL,
             None),
            ("04_cutaway_stem_vs_root_auxin_cell_elongation_model_showing_shaded_stem_stretch_and_lower_root_inhibition_pan", 120.5, 5.5, "C", False, "CHOLODNY–WENT AUXIN MODEL: ACCELERATOR IN STEMS, BRAKE IN ROOTS", "Fast",
             "Fast: daylight close-up pan across a sculpted botanical teaching model comparing shaded-side auxin stretching stem cells longer versus lower-side auxin slowing root cells so the shoot curves up and the root curves down on an oak table. Nothing emissive, no face.",
             STYLE + "In bright window light on an oak table, a sculpted botanical cutaway model shows elongated cells on the shaded side of a curving green shoot beside shortened cells on the underside of a downward-curving root." + FAST_TAIL,
             None),
        ],
    ),
    (
        4,
        "Part 04 — 1901 & 1934: Leaking Streetlamp Gas in St Petersburg & Richard Gane's Ethylene Fruit-Ripening Proof",
        [
            ("01_dmitry_neljubow_1901_st_petersburg_pea_seedlings_and_richard_gane_1934_cambridge_apple_ethylene", 126.0, 6.5, "A", False, "APPLES BREATHE RIPENING GAS", "Quality",
             "Quality: readable faces (21-year-old Russian botanist Dmitry Neljubow at St Petersburg University in 1901 comparing horizontally bent pea seedlings in coal-gas-contaminated lab air to straight seedlings in outside air, dissolving to American physiologist Frank Denny in 1924 and British physiologist Richard Gane in Cambridge on 29 December 1934 condensing ethylene from 56 kg of ripening apples).",
             STYLE + "Split period scene: on the left in 1901 St Petersburg, young Dmitry Neljubow compares horizontally bent pea shoots in lab air against tall straight shoots under a clean-air bell jar; on the right in 1934 Cambridge, Richard Gane collects condensed ethylene from a chamber of ripening apples." + QUAL_TAIL,
             {"kind": "FACT", "label": "Apples breathe ripening gas", "who_card": "Frank Earl Denny (1883–1964) — American plant physiologist", "when_stamp": "1901 · 1924 · 29 December 1934", "timeline_step": "3/3 · 1901, 1924 & 29 Dec 1934 (Neljubow discovers 0.1 ppm ethylene bends pea seedlings, Denny yellows lemons, and Gane proves ripening apples synthesize ethylene hormone)", "hold_s": 3.8}),
            ("02_neljubow_1901_pea_triple_response_and_richard_gane_1934_climacteric_apple_ethylene_chart", 132.5, 8.0, "E", False, "1901 DMITRY NELJUBOW (0.1 PPM C2H4 PEA TRIPLE RESPONSE) & 29 DEC 1934 RICHARD GANE (NATURE: 56 KG APPLES SYNTHESIZE ETHYLENE RIPENING GAS)", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked Dmitry Neljubow (1901 Beih. Bot. Centralbl. 10: 128–139) pea-seedling ethylene triple-response threshold (0.1 ppm C2H4) & Richard Gane (29 December 1934 Nature 134: 1008) climacteric apple ethylene autocatalytic burst chart.",
             {"kind": "DATA", "label": "1901 NELJUBOW (0.1 PPM ETHYLENE TRIPLE RESPONSE) & 29 DEC 1934 RICHARD GANE (NATURE: 56 KG APPLES AUTOCATALYTIC ETHYLENE BURST)", "detail": "Inked Dmitry Neljubow (1901 Beih. Bot. Centralbl. 10: 128–139) pea-seedling ethylene triple-response threshold (0.1 ppm C2H4) & Richard Gane (29 December 1934 Nature 134: 1008) climacteric apple ethylene autocatalytic burst chart on period paper", "scale": "ethylene gas is so potent that a single ripe banana sealed in a paper bag with hard green avocados acts like a chemical radio transmitter, broadcasting a two-carbon gas that tells every fruit around it to turn starch into sugar", "hold_s": 3.8}),
            ("03_cambridge_1934_glass_cold_traps_worcester_pearmain_apples_and_dec_1934_nature_issue_closeup", 140.5, 6.5, "B", False, "1934 — RICHARD GANE PROVES APPLES MAKE ETHYLENE", "Fast",
             "Fast: daylight macro shot of Richard Gane's 1934 Cambridge glass cold-trap condenser tubes beside a wooden crate of red Worcester Pearmain apples, a vial of ethylene dibromide, and the 29 December 1934 issue of Nature on a bench. Nothing emissive, no face.",
             STYLE + "In crisp daylight on a 1934 Cambridge laboratory bench, glass U-tube cold traps sit beside a crate of red Worcester Pearmain apples, a stoppered glass vial, and an open 1934 journal." + FAST_TAIL,
             None),
            ("04_explorer_setting_ripe_yellow_banana_in_crate_of_green_fruit_as_ethylene_rings_turn_them_yellow", 147.0, 5.5, "B", True, None, "Quality",
             "Quality: Explorer beat 2 (locked character reference).",
             STYLE + "Standing beside a wooden crate of hard green bananas and avocados, the Explorer places a single ripe yellow banana in the centre as visible concentric rings of ethylene vapour drift outward and turn the surrounding fruit bright yellow." + EXP_TAIL,
             None),
        ],
    ),
    (
        5,
        "Part 05 — The Silent Sensory World of Plants — & How Spoiled Clover Hay Turned Rat Poison Into a Blood Thinner",
        [
            ("01_timeline_1880_1934_and_plant_tropisms_auxin_statoliths_ethylene_chart", 152.5, 8.5, "E", False, "1880–1934 TIMELINE · DARWIN PHOTOTROPISM, HABERLANDT-NĚMEC STATOLITHS, BOYSEN-JENSEN & WENT AUXIN, NELJUBOW & GANE ETHYLENE", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, the 3-era timeline completes: 1806, Nov 1880 & 1900 (Thomas Andrew Knight's waterwheel, Charles and Francis Darwin prove the 1–2 mm grass tip senses light at Down House, and Gottlieb Haberlandt and Bohumil Němec discover falling-starch statolith gravity sensors in root caps) · 1913 & 17 Apr 1926 (Peter Boysen-Jensen proves the phototropic signal crosses gelatin on the shaded side, and Frits Warmolt Went isolates auxin in agar jelly at 3:00 a.m. in Utrecht) · 1901 & 29 Dec 1934 (Dmitry Neljubow discovers ethylene gas bends pea shoots in St Petersburg, and Richard Gane in Cambridge proves ripening apples manufacture ethylene hormone).",
             {"kind": "DATA", "label": "1880–1934 PLANT HORMONES & TROPISMS TIMELINE · DARWIN, HABERLANDT, NĚMEC, BOYSEN-JENSEN, WENT, NELJUBOW & GANE", "detail": "Animated timeline (1880 → 1934) alongside an inked summary of coleoptile phototropism, root-cap statolith gravitropism, auxin redistribution, and ethylene ripening", "scale": "from tiny tin-foil helmets in Charles Darwin's greenhouse and a cube of jelly at three in the morning to a crate of apples in Cambridge, scientists proved that plants navigate the world without a single eye or nerve", "when_stamp": "1880–1934", "timeline_step": "3/3 · 1880–1934 timeline complete", "hold_s": 3.8}),
            ("02_sunlit_windowsill_plant_and_fruit_bowl_beside_coagulation_glassware_on_plinth_pan", 161.0, 5.5, "A", False, "AUXIN, STATOLITHS & ETHYLENE", "Fast",
             "Fast: daylight close-up of a terracotta pot of green seedlings bending toward a sunny window beside a bowl of ripe apples and bananas and a brass microscope on a wooden museum plinth. Nothing emissive, no face.",
             STYLE + "In crisp daylight on a wooden museum plinth, a potted green plant bending toward window light sits beside a bowl of ripe apples and bananas and a polished brass microscope." + FAST_TAIL,
             None),
            ("03_bizzozero_1882_platelets_mclean_1916_heparin_and_karl_paul_link_1933_blizzard_milk_can_warfarin_handoff", 166.5, 6.5, "C", False, "PLATELETS, HEPARIN & WARFARIN", "Quality",
             "Quality: readable faces (Giulio Bizzozero in Turin in 1882 discovering blood platelets alongside Paul Morawitz's 1905 fibrin net, medical student Jay McLean in 1916 discovering anticoagulant heparin, and Karl Paul Link in Madison in February 1933 with farmer Ed Carlson's milk can of unclotted cow's blood and Warfarin — handoff to 082 Blood Clotting, Heparin & Warfarin).",
             STYLE + "Split period scene: on the left in 1882 Turin and 1916 Baltimore, Giulio Bizzozero peers through his brass microscope beside Jay McLean holding a beaker of unclotted blood; on the right in February 1933 Madison, Wisconsin, farmer Ed Carlson sets a metal milk can of unclotted blood and spoiled sweet clover hay before Karl Paul Link." + QUAL_TAIL,
             {"kind": "WHEN", "label": "1882 · 1905 · 1916 · FEBRUARY 1933", "hold_s": 3.5}),
            ("04_table_three_callback", 173.0, 2.4, "C", False, None, "reuse",
             "Reuse: verified unused moving window [5.50s..7.90s] of P1:07_table_three_props_1880_darwin_tinfoil_cap_1926_went_agar_block_rack_and_1934_gane_apple_jar (callback, £0).",
             "Reuse P1:07_table_three_props_1880_darwin_tinfoil_cap_1926_went_agar_block_rack_and_1934_gane_apple_jar [5.50s..7.90s] (2.40s distinct non-overlapping tail window from 8.00s source clip).",
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
                row["reuse_of"] = "P1:07_table_three_props_1880_darwin_tinfoil_cap_1926_went_agar_block_rack_and_1934_gane_apple_jar"
                row["reuse_window_s"] = [5.5, 7.9]
                row["reuse_audit"] = {
                    "source_row": "P1:07_table_three_props_1880_darwin_tinfoil_cap_1926_went_agar_block_rack_and_1934_gane_apple_jar",
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
            "film": "081_Darwin-Went-Neljubow-Gane-Plant-Tropisms-Auxin",
            "part": p_idx,
            "title": p_title,
            "version": "v01",
            "timing_status": "pre_vo_script_clock (built from plant_tropisms_script_master_v01.md; retimes onto Scribe STT once VO locks)",
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
        "film": "081_Darwin-Went-Neljubow-Gane-Plant-Tropisms-Auxin",
        "version": "v01",
        "date": "2026-10-20",
        "owner": "gemini (J0738)",
        "status": "PRE_VO_BOARDS_V01_NO_MINT",
        "generation_authorized": False,
        "script": "00_Brand/Channel-Setup/ideas/081_Darwin-Went-Neljubow-Gane-Plant-Tropisms-Auxin/plant_tropisms_script_master_v01.md",
        "sources": "00_Brand/Channel-Setup/ideas/081_Darwin-Went-Neljubow-Gane-Plant-Tropisms-Auxin/SOURCES_v01.md",
        "credit_snapshot": {
            "flow_balance": 23740,
            "flow_floor": 0,
            "flow_read_at": "2026-10-15T21:42:22Z",
            "vertex_promo_gbp": 71.02,
            "vertex_usable_gbp": 70.02,
        },
        "totals": totals,
        "per_part": per_part_summary,
        "mint_order": "006 > 007 > 008 > 009 > 010 > 011 > 012 > 013 > 014 > 015 > 016 > 017 > 018 > 019 > 020 > 021 > 022 > 023 > 024 > 025 > 026 > 027 > 028 > 029 > 030 > 031 > 032 > 033 > 034 > 035 > 036 > 037 > 038 > 039 > 040 > 041 > 042 > 043 > 044 > 045 > 046 > 047 > 048 > 049 > 050 > 051 > 052 > 053 > 054 > 055 > 056 > 057 > 058 > 059 > 060 > 061 > 062 > 063 > 064 > 065 > 066 > 067 > 068 > 069 > 070 > 071 > 072 > 073 > 074 > 075 > 076 > 077 > 078 > 079 > 080 > 081 > 082 > 083. Nothing in 081 is generation_authorized.",
    }
    (EDIT / "PICTURE_PLAN_v01.json").write_text(json.dumps(plan, indent=2) + "\n")

    sl = [
        "# 081 Plant Hormones: How Darwin's Blindfolded Grass Sees Light — Shot list & plate boards v01 (pre-VO)",
        "",
        "Gemini, 20 Oct 2026, J0738. Built from `plant_tropisms_script_master_v01.md` (`91.0/100 PASS`) and `SOURCES_v01.md`.",
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
        "# 081 price review v01 (pre-VO plate boards)",
        "",
        "Gemini, 20 Oct 2026, J0738. Boards only. **No mint. No spend. No merge.**",
        "Prepared from `plant_tropisms_script_master_v01.md` (`91.0/100 PASS`) and `SOURCES_v01.md` so 081's full plate board rows, non-emissive Fast prompts, £0 code graphics, and Teach-on-Screen overlays are ready to re-time the moment long VO locks. Parked for Chief.",
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
        f"- **Quality ({totals['Quality']} rows):** readable faces (Charles Darwin, Francis Darwin, Thomas Andrew Knight, Gottlieb Haberlandt, Bohumil Němec, Peter Boysen-Jensen, Árpád Paál, Frits Warmolt Went, Kenneth Vivian Thimann, Dmitry Nikolayevich Neljubow, Frank Earl Denny, Richard Gane, Giulio Bizzozero, Jay McLean, Karl Paul Link), November 1880 Down House tin-foil coleoptile tip experiments & 1900 root-cap `statolith` discovery, 1913 Copenhagen gelatin/mica tests & 17 April 1926 3:00 a.m. Utrecht `auxin` agar-block discovery, 1901 St Petersburg & 29 December 1934 Cambridge `ethylene` fruit-ripening proof, and the 2 Explorer beats.",
        f"- **Fast ({totals['Fast']} rows, non-emissive):** daylight prop and laboratory shots (1880 *The Power of Movement in Plants* volume, rolled tin-foil caps & brass agar cutter pan, 3-object callback bench, Down House black-sand seedling tray with foil and glass caps, 1806 Knight wooden waterwheel & sculpted root-cap statolith model, 1926 Utrecht brass *Avena* coleoptile rack with 2×2 mm agar cubes & protractor, sculpted stem vs root Cholodny–Went cell-elongation model, 1934 Cambridge glass cold traps with Worcester Pearmain apples & December 1934 *Nature* issue, sunlit windowsill plant & fruit bowl beside brass microscope on museum plinth). Zero candles, flames, sparks, or glowing elements on Fast.",
        f"- **£0 code graphics ({totals['code_graphic']} rows):**",
        "  1. `P1:04_darwin_1880_haberlandt_1900_went_1926_and_gane_1934_plant_tropisms_auxin_ethylene_chart` — Darwin (1880) & Frits Went (17 April 1926) coleoptile phototropism & agar-block `auxin` curvature bioassay, Haberlandt & Němec (1900) root-cap `statoliths`, and Neljubow/Gane `ethylene` (`SCALE: a plant doesn't bend toward a window by flexing muscles on the sunny side — it pumps auxin growth hormone to the shady side so the shady cells inflate with water and stretch longer like the outer rail of a curving train track`)",
        "  2. `P1:06_frits_went_17_apr_1926_utrecht_avena_agar_block_curvature_bioassay_chart` — Frits Went (17 April 1926, Utrecht) *Avena* coleoptile agar-block curvature angle vs `auxin` concentration (`SCALE: just one ten-millionth of a gram of auxin trapped inside a two-millimetre cube of jelly is enough to make thousands of oat shoots bend in pitch darkness`)",
        "  3. `P2:02_darwin_nov_1880_five_condition_coleoptile_tip_and_haberlandt_nemec_1900_statolith_chart` — Charles & Francis Darwin (November 1880 *The Power of Movement in Plants*) 5-condition coleoptile tip experiment + Haberlandt & Němec (1900) root-cap `statolith` sedimentation (`SCALE: covering just the top one-and-a-half millimetres of a seedling with tin foil while leaving the rest of the stem in bright sunlight is like putting a blindfold over a runner's eyes while leaving their legs free — the muscles work, but they have no idea which way to turn`)",
        "  4. `P3:02_boysen_jensen_1913_paal_1919_and_frits_went_1926_cholodny_went_auxin_redistribution_chart` — Boysen-Jensen (1913), Árpád Paál (1919) & Frits Went (1926–1927) Cholodny–Went `auxin` redistribution & opposite stem vs root dose-response curves (`SCALE: the exact same auxin hormone molecule makes a shoot grow up toward the sun and a root grow down into the soil — because in stems extra auxin acts like an accelerator on the shady side, while in roots extra auxin acts like a brake on the bottom side`)",
        "  5. `P4:02_neljubow_1901_pea_triple_response_and_richard_gane_1934_climacteric_apple_ethylene_chart` — Dmitry Neljubow (1901) `0.1 ppm` `ethylene` pea triple-response & Richard Gane (29 December 1934 *Nature*) 56 kg apple climacteric `ethylene` burst (`SCALE: ethylene gas is so potent that a single ripe banana sealed in a paper bag with hard green avocados acts like a chemical radio transmitter, broadcasting a two-carbon gas that tells every fruit around it to turn starch into sugar`)",
        "  6. `P5:01_timeline_1880_1934_and_plant_tropisms_auxin_statoliths_ethylene_chart` — completed timeline (1880 → 1934) + phototropism, statoliths, auxin & ethylene (`SCALE: from tiny tin-foil helmets in Charles Darwin's greenhouse and a cube of jelly at three in the morning to a crate of apples in Cambridge, scientists proved that plants navigate the world without a single eye or nerve`)",
        f"- **£0 verified reuse ({totals['reuse']} row):** `P5:04_table_three_callback` uses the 2.40 s unused moving tail `[5.50s..7.90s]` of `P1:07_table_three_props_1880_darwin_tinfoil_cap_1926_went_agar_block_rack_and_1934_gane_apple_jar`.",
        "",
        "## Mint order",
        "",
        "006 > 007 > 008 > 009 > 010 > 011 > 012 > 013 > 014 > 015 > 016 > 017 > 018 > 019 > 020 > 021 > 022 > 023 > 024 > 025 > 026 > 027 > 028 > 029 > 030 > 031 > 032 > 033 > 034 > 035 > 036 > 037 > 038 > 039 > 040 > 041 > 042 > 043 > 044 > 045 > 046 > 047 > 048 > 049 > 050 > 051 > 052 > 053 > 054 > 055 > 056 > 057 > 058 > 059 > 060 > 061 > 062 > 063 > 064 > 065 > 066 > 067 > 068 > 069 > 070 > 071 > 072 > 073 > 074 > 075 > 076 > 077 > 078 > 079 > 080 > 081 > 082 > 083. `generation_authorized` is `false` on every row.",
    ])
    (EDIT / "PRICE_REVIEW_v01.md").write_text("\n".join(pr_lines) + "\n")
    print(f"081 v01 boards written: {totals['rows']} rows, Flow expected={totals['flow_credits_expected']}")


if __name__ == "__main__":
    main()
