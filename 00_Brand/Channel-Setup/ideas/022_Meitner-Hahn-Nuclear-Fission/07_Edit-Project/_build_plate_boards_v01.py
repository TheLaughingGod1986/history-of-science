#!/usr/bin/env python3
"""HOS 022 (Nuclear Fission: The Walk in the Snow That Split the Atom) pre-VO plate boards v01. J0448. No mint, no spend.

Built from 00_Brand/Channel-Setup/ideas/022_Meitner-Hahn-Nuclear-Fission/fission_script_master_v01.md
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
        "Part 01 — The Tree Trunk in the Swedish Snow",
        [
            ("01_meitner_frisch_swedish_snow_log_split_1938", 0.0, 5.5, "A", False, "THE WALK THAT SPLIT THE ATOM", "Quality",
             "Quality: Short frame 0 / answer image (0:03) + readable faces (Lise Meitner on a fallen pine log and Otto Frisch on skis in Kungälv, Sweden on 24 December 1938) + glowing liquid-drop uranium nucleus snapping into two spheres.",
             STYLE + "In the snow-covered pine woods of Kungälv, Sweden on 24 December 1938, physicist Lise Meitner sits on a fallen pine log beside her nephew Otto Frisch on cross-country skis, sketching on a scrap of paper while above her pencil a heavy liquid-drop sphere stretches into a thin-waisted dumbbell and snaps into two smaller spheres with a bright golden flash." + QUAL_TAIL,
             {"kind": "WHEN", "label": "KUNGÄLV, SWEDEN · 24 DECEMBER 1938", "timeline_step": "5/8 · 24 Dec 1938 (Meitner & Frisch solve nuclear fission in the snow)", "hold_s": 3.5}),
            ("02_berlin_barium_beakers_vs_swedish_snow_nobel", 5.5, 6.0, "B", False, "BERLIN LAB, SWEDISH SNOW", "Quality",
             "Quality: readable faces (Otto Hahn and Fritz Strassmann in Berlin on the left; Lise Meitner in the Swedish snow beside a golden Nobel medal on the right).",
             STYLE + "Split period composition: on the left, Otto Hahn and Fritz Strassmann examine glass crystallization dishes of barium salts in their Berlin laboratory; on the right, Lise Meitner calculates on a scrap of paper on a snowy log in Sweden beside a gleaming gold medal." + QUAL_TAIL,
             None),
            ("03_neutron_bouncing_off_iron_sphere_chalkboard", 11.5, 6.0, "C", False, "UNBREAKABLE NUCLEUS?", "Fast",
             "Fast: daylight physics lecture room where a small metal marble rolls up to a heavy iron cannonball on a wooden bench and bounces harmlessly off. Nothing emissive, no face.",
             STYLE + "In crisp daylight on a wooden physics lecture bench, a small silver marble rolls gently against a massive dark iron cannonball sphere and rebounds harmlessly off its unyielding surface." + FAST_TAIL,
             {"kind": "WHEN", "label": "DECEMBER 1938", "hold_s": 3.5}),
            ("04_u235_barium_krypton_200mev_fission_chart", 17.5, 8.0, "E", False, "92 U → 56 BA + 36 KR · 200 MEV", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked nuclear-fission balance shows Uranium-235 (92 protons) absorbing 1 slow neutron, stretching into a dumbbell drop, and splitting into Barium (56 protons) + Krypton (36 protons) while releasing 200 million electron-volts (200 MeV) vs ~4 eV from burning one carbon atom in coal.",
             {"kind": "DATA", "label": "92 U → 56 BA + 36 KR · 200 MEV VS 4 EV COAL", "detail": "Inked nuclear-fission diagram comparing Uranium (92 protons) splitting into Barium (56 protons) + Krypton (36 protons) and releasing 200 million electron-volts (200 MeV) per atom vs ~4 eV from burning one atom of coal", "scale": "200 million electron-volts from a single atom — fifty million times more energy than burning one atom of coal, enough to make a visible grain of sand physically jump", "who_card": "Otto Hahn (1879–1968) — Berlin radiochemist · Fritz Strassmann (1902–1980) — Berlin analytical chemist · Lise Meitner (1878–1968) — Austrian-Swedish nuclear physicist · Otto Robert Frisch (1904–1979) — Austrian nuclear physicist", "when_stamp": "17 December 1938 · 24 December 1938", "hold_s": 3.8}),
            ("05_paraffin_block_and_crystallization_dishes_pan", 25.5, 5.5, "A", False, "FRACTIONAL CRYSTALLIZATION", "Fast",
             "Fast: daylight pan across white paraffin wax blocks, glass beakers, and porcelain crystallization dishes on Hahn and Strassmann's wooden Berlin workbench between code graphics so two full-frame graphics never run back to back.",
             STYLE + "In soft daylight, the camera tracks across blocks of white paraffin wax, glass funnels, and shallow porcelain crystallization dishes arranged on a wooden chemistry workbench." + FAST_TAIL,
             None),
            ("06_1kg_uranium_vs_2700_tonnes_coal_scale_chart", 31.0, 8.0, "E", False, "50 MILLION TIMES COAL", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period parchment, an inked energy-density scale shows 1 single splitting Uranium-235 atom (200 MeV) kicking a visible grain of sand upward, alongside 1 kilogram of Uranium-235 equalling 2.7 million kilograms (2,700 tonnes) of burning coal.",
             {"kind": "DATA", "label": "1 KG URANIUM-235 = 2,700 TONNES OF COAL", "detail": "Inked energy-density scale comparing 1 splitting Uranium-235 atom kicking a grain of sand and 1 kilogram of Uranium-235 against 2.7 million kilograms (2,700 tonnes) of coal", "scale": "one kilogram of uranium holds the energy of 2,700 tonnes of coal — a lump the size of a baseball matching a thirty-car freight train", "hold_s": 3.8}),
            ("07_table_three_props_paraffin_snow_log_paper_chamber", 39.0, 5.5, "C", False, "BERLIN, DECEMBER 1938", "Fast",
             "Fast: daylight prop table (callback source for Part 05: Berlin paraffin block and barium dish, folded letter with pine cone and pencil scrap, brass ionization chamber). Nothing emissive.",
             STYLE + "On a wooden laboratory workbench in soft daylight sit three objects side by side: a paraffin wax block beside a glass crystallization dish, a folded airmail letter with a pencil scrap and pine cone, and a cylindrical brass ionization chamber." + FAST_TAIL,
             None),
            ("08_explorer_barium_56_krypton_36_spheres", 62.0, 5.5, "A", True, None, "Quality",
             "Quality: Explorer beat 1 (locked character reference, after 1:00).",
             STYLE + "Standing on the wooden laboratory bench beside the glass crystallization dishes, the Explorer holds two smaller brass spheres up against a large uranium sphere on a balance pan, sees them balance cleanly, and gasps in realization." + EXP_TAIL,
             None),
            ("09_dutch_border_train_july_1938_departure", 67.5, 5.5, "B", False, "JULY 1938 ESCAPE", "Quality",
             "Quality: readable face (sixty-year-old Lise Meitner clutching a small leather handbag inside a train carriage pulling across the Dutch border in July 1938).",
             STYLE + "Inside a wooden railway carriage pulling away from a border station in July 1938, sixty-year-old Lise Meitner sits by the window in a dark coat, clutching a small leather handbag as the tracks slip past." + QUAL_TAIL,
             None),
        ],
    ),
    (
        2,
        "Part 02 — The Carpenter's Basement, the Escape and the Barium Mystery",
        [
            ("01_meitner_1907_carpenter_basement_and_1934_kwi", 73.0, 6.5, "A", False, "BANNED FROM UPSTAIRS LABS", "Quality",
             "Quality: readable faces (young Lise Meitner in the 1907 Berlin carpenter's basement workshop, then leading experiments upstairs with Otto Hahn and Fritz Strassmann in 1934).",
             STYLE + "Berlin, 1907 and 1934: in a cramped basement carpenter's shop with wooden workbenches and a separate street door, young Lise Meitner calibrates an electroscope, then stands upstairs in a bright 1934 laboratory beside Otto Hahn and Fritz Strassmann." + QUAL_TAIL,
             {"kind": "WHO", "label": "Enrico Fermi (1901–1954) — Italian physicist", "when_stamp": "Berlin, 1907 · 1934", "timeline_step": "2/8 · 1934 (Fermi bombards uranium with neutrons)", "hold_s": 3.8}),
            ("02_meitner_dutch_border_ten_marks_and_ring_1938", 79.5, 6.5, "B", False, "13 JULY 1938 · 10 MARKS", "Quality",
             "Quality: readable face (Lise Meitner crossing the Dutch border on 13 July 1938 with two small suitcases, a ten-mark coin/note in her purse, and a diamond ring).",
             STYLE + "Dutch border, 13 July 1938: sixty-year-old Lise Meitner sits tense in a railway compartment with two small leather suitcases at her feet, opening her clasp purse to reveal a single coin and a gold diamond ring." + QUAL_TAIL,
             {"kind": "FACT", "label": "Fled with 10 marks", "when_stamp": "March 1938 · 13 July 1938", "timeline_step": "3/8 · 13 Jul 1938 (Meitner flees Nazi Germany)", "hold_s": 3.8}),
            ("03_barium_fractional_crystallization_berlin_1938", 86.0, 5.5, "C", False, "17 DECEMBER 1938", "Fast",
             "Fast: daylight close-up of gloved chemist hands pouring clear solution between glass beakers and filtering white barium crystals on a Berlin bench. No face, nothing emissive.",
             STYLE + "In crisp window light on a Berlin laboratory bench, chemist hands pour clear liquid from a glass beaker through filter paper over fine white barium crystals." + FAST_TAIL,
             {"kind": "WHEN", "label": "17 DECEMBER 1938", "timeline_step": "4/8 · 17 Dec 1938 (Hahn & Strassmann find barium in Berlin)", "hold_s": 3.5}),
            ("04_uranium_92_vs_barium_56_atomic_scale_diagram", 91.5, 8.0, "E", False, "Z = 92 URANIUM → Z = 56 BARIUM", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked atomic-number scale compares Uranium (Z = 92) and Radium (Z = 88) against Barium (Z = 56 — 36 protons lighter than Uranium), beside Hahn's 19 December 1938 letter to Stockholm.",
             {"kind": "DATA", "label": "URANIUM (Z=92) VS BARIUM (Z=56 · -36 PROTONS)", "detail": "Inked atomic-number scale comparing Uranium (Z = 92) and Radium (Z = 88) against Barium (Z = 56 — 36 protons lighter than Uranium)", "scale": "chipping 36 protons off a uranium nucleus in one hit — like tossing a pebble at a boulder and watching the boulder split cleanly in half", "when_stamp": "19 December 1938", "hold_s": 3.8}),
        ],
    ),
    (
        3,
        "Part 03 — The Liquid Drop in the Snow and E = mc²",
        [
            ("01_kungalv_woods_meitner_and_frisch_on_skis", 99.5, 6.5, "A", False, "KUNGÄLV · 24 DECEMBER 1938", "Quality",
             "Quality: readable faces (Lise Meitner walking briskly through snowy Swedish woods beside Otto Frisch on cross-country skis, then sitting on a fallen tree trunk).",
             STYLE + "Kungälv, Sweden, 24 December 1938: in bright winter daylight among snow-covered pines, Lise Meitner walks briskly beside Otto Frisch on wooden cross-country skis, then sits with him on a fallen tree trunk with pencils and folded scraps of paper." + QUAL_TAIL,
             {"kind": "FACT", "label": "Solved on a snowy log", "when_stamp": "Kungälv, 24 December 1938", "hold_s": 3.8}),
            ("02_liquid_drop_dumbbell_and_emc2_200mev_diagram", 106.0, 8.0, "E", False, "56 + 36 = 92 · ΔM × C² = 200 MEV", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, Niels Bohr's liquid-drop model of Uranium-235 (92 protons) wobbles upon absorbing 1 slow neutron, stretches into a dumbbell, and snaps into Barium (56) + Krypton (36), with missing mass Δm ≈ 0.2 proton mass × c² = 200 MeV.",
             {"kind": "DATA", "label": "ΔM ≈ 0.2 PROTON MASS × C² = 200 MEV", "detail": "Inked liquid-drop and E = mc² calculation diagram showing 1 uranium nucleus (92p) → Barium (56p) + Krypton (36p), where missing mass Δm ≈ 0.2 proton mass × c² = 200 MeV", "scale": "one-fifth of a single proton's mass vanishes — and turns into enough energy to hurl the two atomic halves apart at a thirtieth of the speed of light", "who_card": "Niels Bohr (1885–1962) — Danish theoretical physicist", "hold_s": 3.8}),
            ("03_meitner_pencil_scrap_in_snow_closeup", 114.0, 6.0, "B", False, "E = MC² PROVED IN THE SNOW", "Fast",
             "Fast: daylight close-up of a gloved hand holding a wooden pencil sketching two separating circles on a scrap of paper resting on snow-dusted pine bark. No readable text on plate, nothing emissive.",
             STYLE + "In crisp winter daylight, a wool-gloved hand holds a wooden pencil sketching a waisted liquid drop splitting into two circles on a scrap of paper resting on a snow-dusted pine log." + FAST_TAIL,
             {"kind": "WHO", "label": "Albert Einstein (1879–1955) — German-born theoretical physicist", "when_stamp": "1905", "timeline_step": "1/8 · 1905 (Einstein's E = mc²)", "hold_s": 3.8}),
            ("04_pine_woods_snow_footprints_and_ski_tracks", 120.0, 5.5, "C", False, "CHRISTMAS EVE 1938", "Fast",
             "Fast: daylight tracking shot along fresh boot footprints and parallel ski tracks winding past a fallen pine trunk in the Swedish snow. Nothing emissive, no face.",
             STYLE + "In quiet winter daylight, fresh boot footprints and parallel wooden ski tracks wind side by side past a snow-covered fallen tree trunk in a Swedish pine forest." + FAST_TAIL,
             None),
        ],
    ),
    (
        4,
        "Part 04 — The Pulse in Copenhagen and the Missing Nobel",
        [
            ("01_bohr_forehead_slap_and_frisch_copenhagen_pulses", 125.5, 6.5, "A", False, "COPENHAGEN · JANUARY 1939", "Quality",
             "Quality: readable faces (Niels Bohr striking his forehead in astonishment on 3 January 1939 as Otto Frisch explains the split; Frisch watching giant ionization pulses in his Copenhagen basement lab on 13 January 1939).",
             STYLE + "Copenhagen, January 1939: Danish physicist Niels Bohr in a tweed suit strikes his forehead in joyful astonishment as Otto Frisch holds up a sketch of the splitting drop; in the basement lab, Frisch watches an oscilloscope pointer leap upward in tall sharp spikes." + QUAL_TAIL,
             {"kind": "FACT", "label": "Coined 'fission' from biology", "when_stamp": "Copenhagen, 3 January 1939 · 13 January 1939 · 11 February 1939", "timeline_step": "6/8 · 11 Feb 1939 (Nature paper coins 'fission')", "hold_s": 3.8}),
            ("02_hahn_berlin_paper_vs_meitner_1944_nobel_omission", 132.0, 6.5, "B", False, "49 NOMINATIONS · 0 NOBELS", "Quality",
             "Quality: readable faces (Otto Hahn in Berlin with the 6 January 1939 paper and receiving the 1944 Nobel Prize alone vs Lise Meitner in Stockholm).",
             STYLE + "Split period portrait: on the left, Otto Hahn sits at his Berlin desk and receives a gold Nobel medal in Stockholm; on the right, Lise Meitner stands quietly by a Stockholm window holding a printed journal." + QUAL_TAIL,
             {"kind": "FACT", "label": "Nominated 49 times, 0 Nobels", "when_stamp": "6 January 1939 · November 1945", "hold_s": 3.8}),
            ("03_periodic_table_tile_109_meitnerium_1997", 138.5, 5.5, "C", False, "ELEMENT 109: MEITNERIUM", "Fast",
             "Fast: daylight close-up of a brushed brass tile slotting into place on a wooden periodic table wall frame beside a framed portrait. No readable text on plate, nothing emissive.",
             STYLE + "In warm daylight, a polished brass square tile slots cleanly into the seventh row of a carved wooden periodic table wall frame beside a classic portrait frame." + FAST_TAIL,
             {"kind": "WHEN", "label": "1966 · 1997", "hold_s": 3.5}),
            ("04_explorer_polishing_element_109_tile", 144.0, 5.5, "B", True, None, "Quality",
             "Quality: Explorer beat 2 (locked character reference).",
             STYLE + "Standing beside the giant wooden periodic table wall chart, the Explorer polishes the gleaming brass tile of Element 109 with a soft cloth and tips its hat respectfully toward Lise Meitner's portrait." + EXP_TAIL,
             None),
        ],
    ),
    (
        5,
        "Part 05 — What E = mc² Really Converts and the Chain Reaction",
        [
            ("01_timeline_1905_1997_and_236_nucleon_conservation", 149.5, 8.5, "E", False, "0 PARTICLES DESTROYED · 0.1% MASS", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, the 8-date timeline completes: 1905 (Einstein E=mc²) · 1934 (Fermi neutrons) · 13 Jul 1938 (Meitner escape) · 17 Dec 1938 (Berlin barium) · 24 Dec 1938 (Kungälv snow calculation) · 11 Feb 1939 ('fission' coined) · 2 Dec 1942 (Chicago Pile-1) · 1997 (Element 109 Meitnerium), alongside an inked nucleon balance showing 92 protons + 144 neutrons = 236 nucleons conserved before and after fission while 0.1% binding mass turns into heat.",
             {"kind": "DATA", "label": "236 NUCLEONS BEFORE & AFTER · 0.1% BINDING MASS → HEAT", "detail": "Animated 8-date timeline (1905 → 1997) alongside an inked nucleon conservation balance showing 92 protons + 144 neutrons = 236 particles before and after fission (zero protons or neutrons destroyed; 0.1% binding mass converted to heat)", "scale": "zero protons or neutrons destroyed — releasing just one-thousandth (0.1%) of the atom's binding mass powers an entire city", "when_stamp": "2 December 1942 · 1905–1997", "timeline_step": "7/8 · 2 Dec 1942 (Chicago Pile-1) & 8/8 · 1997 (Element 109 Meitnerium)", "hold_s": 3.8}),
            ("02_chicago_pile_1_graphite_bricks_and_cadmium_rod_1942", 158.0, 6.0, "A", False, "TAMING THE CHAIN REACTION", "Fast",
             "Fast: daylight architectural view inside the squash court under Stagg Field on 2 December 1942 showing a stack of dark matte graphite bricks and a sliding cadmium control rod. No face, nothing emissive.",
             STYLE + "Inside a high-ceilinged brick squash court in daylight, a silver cadmium control rod slides smoothly out of a neat lattice of dark matte graphite blocks." + FAST_TAIL,
             None),
            ("03_becquerel_dark_drawer_and_curie_cauldron_handoff", 164.0, 6.5, "C", False, "THE SECRET OF RADIOACTIVITY", "Quality",
             "Quality: glowing uranium salt in Henri Becquerel's dark wooden drawer and Marie Curie's steaming pitchblende cauldron in Paris dissolving into Rumford's Munich cannon box (handoff to 023 Radioactivity).",
             STYLE + "In a dim Paris laboratory, a dark wooden desk drawer opens to reveal glowing uranium crystals on a wrapped photographic plate beside acopper cross and a steaming iron cauldron of pitchblende ore, dissolving into horses turning a brass cannon in a boiling water box." + QUAL_TAIL,
             {"kind": "WHEN", "label": "FEBRUARY 1896 · JANUARY 1798", "hold_s": 3.5}),
            ("04_table_three_callback", 170.5, 2.4, "C", False, None, "reuse",
             "Reuse: verified unused moving window [5.50s..7.90s] of P1:07_table_three_props_paraffin_snow_log_paper_chamber (callback, £0).",
             "Reuse P1:07_table_three_props_paraffin_snow_log_paper_chamber [5.50s..7.90s] (2.40s distinct non-overlapping tail window from 8.00s source clip).",
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
                row["reuse_of"] = "P1:07_table_three_props_paraffin_snow_log_paper_chamber"
                row["reuse_window_s"] = [5.5, 7.9]
                row["reuse_audit"] = {
                    "source_row": "P1:07_table_three_props_paraffin_snow_log_paper_chamber",
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
            "film": "022_Meitner-Hahn-Nuclear-Fission",
            "part": p_idx,
            "title": p_title,
            "version": "v01",
            "timing_status": "pre_vo_script_clock (built from fission_script_master_v01.md; retimes onto Scribe STT once VO locks)",
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
        "film": "022_Meitner-Hahn-Nuclear-Fission",
        "version": "v01",
        "date": "2026-10-17",
        "owner": "gemini (J0448)",
        "status": "PRE_VO_BOARDS_V01_NO_MINT",
        "generation_authorized": False,
        "script": "00_Brand/Channel-Setup/ideas/022_Meitner-Hahn-Nuclear-Fission/fission_script_master_v01.md",
        "sources": "00_Brand/Channel-Setup/ideas/022_Meitner-Hahn-Nuclear-Fission/SOURCES_v01.md",
        "credit_snapshot": {
            "flow_Balance": 23740,
            "flow_floor": 0,
            "flow_read_at": "2026-10-15T21:42:22Z",
            "vertex_promo_gbp": 71.02,
            "vertex_usable_gbp": 70.02,
        },
        "totals": totals,
        "per_part": per_part_summary,
        "mint_order": "006 > 007 > 008 > 009 > 010 > 011 > 012 > 013 > 014 > 015 > 016 > 017 > 018 > 019 > 020 > 021 > 022. Nothing in 022 is generation_authorized.",
    }
    (EDIT / "PICTURE_PLAN_v01.json").write_text(json.dumps(plan, indent=2) + "\n")

    sl = [
        "# 022 Nuclear Fission: The Walk in the Snow That Split the Atom — Shot list & plate boards v01 (pre-VO)",
        "",
        "Gemini, 17 Oct 2026, J0448. Built from `fission_script_master_v01.md` (92.2 PASS) and `SOURCES_v01.md`.",
        "**No mint, no spend.** Pre-VO clock timings (`172.9 s` base picture grid; re-times automatically onto Scribe word timestamps once long VO locks).",
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
        "# 022 price review v01 (pre-VO plate boards)",
        "",
        "Gemini, 17 Oct 2026, J0448. Boards only. **No mint. No spend. No merge.**",
        "Prepared from `fission_script_master_v01.md` (92.2 PASS) and `SOURCES_v01.md` so 022's full plate board rows, non-emissive Fast prompts, £0 code graphics, and Teach-on-Screen overlays are ready to re-time the moment long VO locks. Parked for Chief.",
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
        f"- **Quality ({totals['Quality']} rows):** readable faces (Lise Meitner, Otto Robert Frisch, Otto Hahn, Fritz Strassmann, Niels Bohr), emissive/glow scenes (24 Dec 1938 liquid-drop split flash, Paris uranium drawer handoff), and the 2 Explorer beats.",
        f"- **Fast ({totals['Fast']} rows, non-emissive):** daylight prop and laboratory shots (neutron marble bouncing off iron cannonball, Berlin paraffin & crystallization dishes pan, 3-object callback bench, barium filtration in Berlin, Meitner's pencil sketching on snow-dusted pine bark, footprints & ski tracks in Kungälv woods, Element 109 Meitnerium brass tile, Chicago Pile-1 graphite bricks & cadmium control rod). Zero candles, flames, sparks, or glowing elements on Fast.",
        f"- **£0 code graphics ({totals['code_graphic']} rows):**",
        "  1. `P1:04_u235_barium_krypton_200mev_fission_chart` — Uranium-235 (92p) + 1n → Barium (56p) + Krypton (36p) releasing 200 MeV vs ~4 eV coal (`SCALE: 200 million electron-volts from a single atom — fifty million times more energy than burning one atom of coal, enough to make a visible grain of sand physically jump`)",
        "  2. `P1:06_1kg_uranium_vs_2700_tonnes_coal_scale_chart` — 1 splitting U-235 atom kicking a grain of sand and 1 kg U-235 = 2,700 tonnes of coal (`SCALE: one kilogram of uranium holds the energy of 2,700 tonnes of coal — a lump the size of a baseball matching a thirty-car freight train`)",
        "  3. `P2:04_uranium_92_vs_barium_56_atomic_scale_diagram` — atomic-number scale comparing Uranium (Z=92) and Radium (Z=88) against Barium (Z=56, 36 protons lighter) (`SCALE: chipping 36 protons off a uranium nucleus in one hit — like tossing a pebble at a boulder and watching the boulder split cleanly in half`)",
        "  4. `P3:02_liquid_drop_dumbbell_and_emc2_200mev_diagram` — Niels Bohr's liquid-drop model stretching and snapping into Ba (56) + Kr (36) with Δm ≈ 0.2 proton mass × c² = 200 MeV (`SCALE: one-fifth of a single proton's mass vanishes — and turns into enough energy to hurl the two atomic halves apart at a thirtieth of the speed of light`)",
        "  5. `P5:01_timeline_1905_1997_and_236_nucleon_conservation` — completed 8-date timeline (1905 → 1997) + 236-nucleon conservation balance (`SCALE: zero protons or neutrons destroyed — releasing just one-thousandth (0.1%) of the atom's binding mass powers an entire city`)",
        f"- **£0 verified reuse ({totals['reuse']} row):** `P5:04_table_three_callback` uses the 2.40 s unused moving tail `[5.50s..7.90s]` of `P1:07_table_three_props_paraffin_snow_log_paper_chamber`.",
        "",
        "## Mint order",
        "",
        "006 > 007 > 008 > 009 > 010 > 011 > 012 > 013 > 014 > 015 > 016 > 017 > 018 > 019 > 020 > 021 > 022. `generation_authorized` is `false` on every row.",
    ])
    (EDIT / "PRICE_REVIEW_v01.md").write_text("\n".join(pr_lines) + "\n")
    print(f"022 v01 boards written: {totals['rows']} rows, Flow expected={totals['flow_credits_expected']}")


if __name__ == "__main__":
    main()
