#!/usr/bin/env python3
"""HOS 071 (Cell Membranes: The Two-Molecule Skin of Life) pre-VO plate boards v01. J0706. No mint, no spend.

Built from 00_Brand/Channel-Setup/ideas/071_Overton-Gorter-Skou-Singer-Agre-Cell-Membrane-Aquaporins/cell_membrane_script_master_v01.md
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
        "Part 01 — The Soap-Film Trough in Leiden & the Two-Molecule Wall Around Every Cell",
        [
            ("01_soap_bubble_morphing_into_5nm_phospholipid_bilayer_with_sodium_pump_and_aquaporin_stream", 0.0, 5.5, "A", False, "TWO MOLECULES THICK", "Quality",
             "Quality: Short frame 0 / answer image (0:03) + a soap bubble morphs into a living cell membrane just 5 nanometres (two phospholipid molecules) thick: golden hydrophilic heads face the water outside and inside while oily hydrophobic tails point inward, as a rotating Na+/K+-ATPase pump ejects sodium ions and an hourglass aquaporin channel funnels a single-file stream of 3 billion water molecules per second.",
             STYLE + "Split macro-and-molecular scene: on the left, an iridescent soap bubble transforms into a curved cell membrane; on the right, a cross-section of the two-molecule phospholipid bilayer shows golden round heads facing water and double tails facing inward while a protein pump cycles sodium and potassium ions and an hourglass channel streams single-file water molecules." + QUAL_TAIL,
             {"kind": "WHEN", "label": "LEIDEN, 1 APRIL 1925", "timeline_step": "1/3 · 1895 & 1 Apr 1925 (Ernest Overton discovers the lipid permeability barrier; Evert Gorter & François Grendel measure the 2:1 red-blood-cell lipid monolayer on water)", "hold_s": 3.5}),
            ("02_overton_1895_gorter_grendel_1925_skou_1957_singer_nicolson_1972_and_agre_1992_split", 5.5, 6.0, "B", False, "2:1 LIPID BILAYER, CRAB NERVE PUMP, AQUAPORINS", "Quality",
             "Quality: complex three-part composition (Ernest Overton in Zurich in 1895 alongside Evert Gorter and François Grendel in Leiden on 1 April 1925 drawing a silk thread across a Langmuir water trough to measure their 2:1 red-blood-cell lipid monolayer; Jens Christian Skou in Aarhus in February 1957 with 25,000 shore crabs alongside Jonathan Singer and Garth Nicolson in California on 18 February 1972 unveiling the Fluid Mosaic Model; and Peter Agre and Gregory Preston at Johns Hopkins in October 1991 / April 1992 watching CHIP28 aquaporin frog oocytes swell and burst in distilled water).",
             STYLE + "Three-panel period composition: on the left, Evert Gorter and François Grendel in 1925 Leiden drawing a silk thread across a water trough beside Ernest Overton; in the centre, Jens Christian Skou in 1957 Denmark with shore crabs alongside Jonathan Singer and Garth Nicolson in 1972 with a fluid mosaic model; on the right, Peter Agre and Gregory Preston in 1991 Baltimore watching frog eggs swell and burst in a dish of water." + QUAL_TAIL,
             None),
            ("03_5nm_phospholipid_bilayer_blocking_ions_while_na_k_atpase_pumps_3_na_out_and_2_k_in", 11.5, 6.0, "C", False, "ONE-THIRD OF YOUR BODY'S ENERGY", "Quality",
             "Quality: complex molecular reveal (a 5-nanometre phospholipid bilayer cross-section shows the hydrophobic oil core blocking charged Na+ and K+ ions while the Na+/K+-ATPase pump uses ATP to eject 3 Na+ ions and import 2 K+ ions, maintaining the cell's electrical battery).",
             STYLE + "Close-up molecular animation of a two-layer phospholipid membrane: charged sodium spheres bounce off the oily interior until a transmembrane protein pump opens, ejecting three sodium spheres outward and drawing two potassium spheres inward." + QUAL_TAIL,
             {"kind": "WHEN", "label": "1895 · 1 APRIL 1925 · FEBRUARY 1957 · 18 FEBRUARY 1972 · 17 APRIL 1992", "timeline_step": "1/3 · 1895 & Apr 1925 (Overton, Gorter & Grendel) · 2/3 · Feb 1957 & Feb 1972 (Skou, Singer & Nicolson) · 3/3 · Oct 1991 / Apr 1992 (Preston & Agre)", "hold_s": 3.5}),
            ("04_gorter_grendel_1925_skou_1957_singer_1972_and_agre_1992_membrane_transport_chart", 17.5, 8.0, "E", False, "GORTER & GRENDEL 2:1 BILAYER (5 NM) · SKOU NA+/K+-ATPASE (3 NA+ OUT / 2 K+ IN, ~30% RESTING ATP) & AGRE AQUAPORIN-1 (3×10^9 H2O/S)", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked Cell Membrane Architecture & Permeability chart from Overton (1895 Vierteljahrsschr. Naturforsch. Ges. Zürich 40: 159–201), Gorter & Grendel (1 April 1925 J. Exp. Med. 41: 439–443), Skou (February 1957 Biochim. Biophys. Acta 23: 394–401), Singer & Nicolson (18 February 1972 Science 175: 720–731), and Preston & Agre et al. (17 April 1992 Science 256: 385–387) shows the 5 nm bimolecular lipid leaflet (2.0:1 monolayer-to-cell surface area ratio), the Na+/K+-ATPase 3 Na+ out / 2 K+ in cycle (~30% of resting mammalian ATP), lateral protein diffusion in the fluid bilayer, and Aquaporin-1 (CHIP28) single-file water permeability (~3 x 10^9 H2O molecules/s per channel with 0 proton leakage).",
             {"kind": "DATA", "label": "1925 2:1 LIPID BILAYER (5 NM), 1957 SKOU NA+/K+ PUMP (~30% RESTING ATP) & 1992 AGRE AQUAPORIN-1 (~3×10^9 H2O/SEC)", "detail": "Inked phospholipid bilayer & membrane transport chart on period paper showing Gorter & Grendel's 2.0:1 lipid monolayer-to-erythrocyte area ratio (5 nm bilayer thickness), Skou's Na+/K+-ATPase pump (3 Na+ out, 2 K+ in per ATP, consuming ~30% of resting mammalian ATP), and Agre's Aquaporin-1 water channel (~3,000,000,000 H2O molecules/second with 0 proton leakage)", "scale": "the membrane around every cell in your body is a self-sealing soap bubble just two molecules thick — twenty thousand times thinner than a sheet of kitchen paper, yet studded with protein gates that check the passport of every atom trying to cross", "who_card": "Charles Ernest Overton (1865–1933) — British-Swedish physiologist · Evert Gorter (1881–1954) — Dutch paediatrician and biochemist · François Grendel (1897–1969) — Dutch chemist · Jens Christian Skou (1918–2018) — Danish physiologist · S. Jonathan Singer (1924–2017) — American cell biologist · Garth L. Nicolson (born 1943) — American biochemist · Peter Agre (born 1949) — American haematologist and molecular biologist", "when_stamp": "1895 · 1 April 1925 · February 1957 · 18 February 1972 · 17 April 1992", "hold_s": 3.8}),
            ("05_langmuir_water_trough_with_silk_thread_phospholipid_model_and_1925_jem_offprint_pan", 25.5, 5.5, "A", False, "THE TWO-MOLECULE BORDER GATE", "Fast",
             "Fast: daylight macro pan across a brass Langmuir water trough with a silk thread, a sculpted wooden phospholipid model, and a 1925 Journal of Experimental Medicine offprint on an oak bench between code graphics so two full-frame graphics never run back to back. Nothing emissive, no face.",
             STYLE + "In crisp daylight on an oak physiology bench, the camera pans smoothly across a rectangular brass water trough spanned by a fine silk thread, a sculpted two-tailed lipid model, and an open 1925 journal." + FAST_TAIL,
             None),
            ("06_gorter_grendel_1_apr_1925_jem_2_to_1_erythrocyte_lipid_monolayer_trough_chart", 31.0, 8.0, "E", False, "LEIDEN, 1 APRIL 1925", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period parchment, an inked Gorter & Grendel Langmuir Trough 2:1 Monolayer Experiment diagram (from Evert Gorter & François Grendel, 1 April 1925 J. Exp. Med. 41: 439–443) shows acetone-extracted lipids from a counted volume of red blood cells across 6 mammalian species (human, dog, sheep, rabbit, guinea pig, goat) spread as a monomolecular film on water between brass barriers, occupying 2.0x the total surface area of the intact cells.",
             {"kind": "DATA", "label": "1 APR 1925 GORTER & GRENDEL (J. EXP. MED.): ERYTHROCYTE LIPID MONOLAYER AREA = 2.0 : 1 CELL SURFACE AREA (6 SPECIES)", "detail": "Inked Gorter & Grendel (1 April 1925 J. Exp. Med. 41: 439–443) erythrocyte lipid-monolayer table across 6 mammalian species showing measured monolayer area to erythrocyte surface area ratio of ~2.0:1 (proving a bimolecular lipid layer with polar heads facing water and non-polar hydrocarbon chains facing inward)", "scale": "spreading all the fat molecules from a red blood cell flat onto water is like unpeeling a two-ply tissue into a single sheet — when the single sheet covers exactly twice the area of the cell, you know the cell was wrapped in two layers back to back", "hold_s": 3.8}),
            ("07_table_three_props_1925_langmuir_trough_1957_shore_crab_jar_and_1991_oocyte_petri_dish", 39.0, 5.5, "C", False, "1925 TO 1992", "Fast",
             "Fast: daylight prop table (callback source for Part 05: Gorter & Grendel's 1925 brass Langmuir trough barrier with silk thread, Skou's 1957 preserved green shore crab specimen jar, and Agre's 1991 glass Petri dish of frog oocytes). Nothing emissive.",
             STYLE + "On an oak workbench in soft window light sit three objects side by side: a brass water-trough slide bar with a silk thread, a glass specimen jar holding a green shore crab, and a glass Petri dish of round frog eggs." + FAST_TAIL,
             None),
            ("08_explorer_unzipping_two_layer_phospholipid_jacket_off_red_blood_cell_onto_two_water_squares", 62.0, 5.5, "A", True, None, "Quality",
             "Quality: Explorer beat 1 (locked character reference, after 1:00).",
             STYLE + "Standing beside a rectangular brass water trough, the Explorer unzips a two-layered golden-and-silver jacket off a sculpted red blood cell model and lays the two layers flat side by side across the water surface, filling exactly two equal squares." + EXP_TAIL,
             None),
            ("09_gorter_and_grendel_1_apr_1925_leiden_drawing_silk_thread_across_lipid_monolayer_trough", 67.5, 5.5, "B", False, "THE 2:1 SOAP-FILM PROOF", "Quality",
             "Quality: readable faces (in Leiden on 1 April 1925, Dutch paediatrician Evert Gorter and chemist François Grendel draw a fine silk thread across a tray of water to compress a one-molecule-thick film of red-blood-cell lipids).",
             STYLE + "In a 1925 Leiden laboratory, Evert Gorter and François Grendel lean over a brass Langmuir trough, sliding a silk thread barrier to compress a shimmering monolayer of red-blood-cell lipids." + QUAL_TAIL,
             {"kind": "WHEN", "label": "LEIDEN, 1 APRIL 1925", "timeline_step": "1/3 · 1 Apr 1925 (Gorter & Grendel prove the 2:1 phospholipid bilayer in red blood cells)", "hold_s": 3.5}),
        ],
    ),
    (
        2,
        "Part 02 — 1895 & 1 April 1925: Ernest Overton's Oil Barrier & Gorter and Grendel's 2:1 Soap-Trough Miracle",
        [
            ("01_ernest_overton_1895_zurich_oil_barrier_and_gorter_grendel_1_apr_1925_leiden_trough", 73.0, 6.5, "A", False, "TWO MISTAKES CANCELLED OUT", "Quality",
             "Quality: readable faces (British-Swedish physiologist Charles Ernest Overton in Zurich in 1895 testing olive-oil and water dye permeability on plant root hairs and tadpoles, dissolving to Evert Gorter and François Grendel in Leiden on 1 April 1925 measuring their 2:1 red-blood-cell lipid monolayer).",
             STYLE + "Split period scene: on the left in 1895 Zurich, Charles Ernest Overton compares olive-oil and water dye jars beside a brass microscope; on the right in April 1925 Leiden, Evert Gorter and François Grendel measure the surface area of red-blood-cell lipids on their water trough." + QUAL_TAIL,
             {"kind": "FACT", "label": "Two mistakes cancelled out", "when_stamp": "1665 · 1895 · 1899 · 1917 · 1 April 1925 · 1966", "timeline_step": "1/3 · 1895 & 1 Apr 1925 (Overton's lipophilic barrier; Gorter & Grendel's 2:1 red-blood-cell phospholipid bilayer)", "hold_s": 3.8}),
            ("02_overton_1895_olive_oil_partition_and_gorter_grendel_1925_bar_1966_double_error_chart", 79.5, 8.0, "E", False, "1895 OVERTON OLIVE-OIL PARTITION CURVE & 1 APR 1925 GORTER & GRENDEL 2:1 BILAYER (WITH BAR, DEAMER & CORNWELL 1966 DOUBLE-ERROR CANCELLATION)", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked Overton (1895) olive-oil/water partition permeability curve & Gorter & Grendel (1 April 1925 J. Exp. Med. 41: 439–443) 2:1 erythrocyte lipid-monolayer ratio chart (with Bar, Deamer & Cornwell 26 August 1966 Science 153: 1010–1012 double-error correction showing incomplete acetone extraction and dry-cell surface underestimation cancelling out) proves the bimolecular phospholipid bilayer.",
             {"kind": "DATA", "label": "1895 OVERTON LIPID PARTITION & 1925 GORTER/GRENDEL 2.0:1 BILAYER RATIO (1966 BAR/DEAMER DOUBLE-ERROR PROOF)", "detail": "Inked Overton (1895) olive-oil/water partition permeability curve & Gorter & Grendel (1 April 1925 J. Exp. Med. 41: 439–443) 2:1 erythrocyte lipid-monolayer ratio chart (with Bar, Deamer & Cornwell 1966 Science 153: 1010–1012 double-error correction) on period paper", "scale": "Gorter and Grendel getting the right two-to-one bilayer answer from an incomplete fat extraction and a shrunken cell measurement is like miscounting your change by ten pence when the shopkeeper also undercharged you by ten pence — both errors vanished and left the exact truth", "hold_s": 3.8}),
            ("03_leiden_1925_acetone_extraction_flask_hemocytometer_slide_and_vernier_trough_closeup", 87.5, 6.5, "B", False, "1 APRIL 1925 — BIMOLECULAR LIPID LAYER (2:1)", "Fast",
             "Fast: daylight macro shot of a glass flask of acetone-extracted red-blood-cell lipids, a ruled glass hemocytometer counting slide, and a brass vernier scale on a water trough on a bench. Nothing emissive, no face.",
             STYLE + "In crisp daylight on a 1925 Leiden laboratory bench, a stoppered glass extraction flask and a ruled glass blood-counting slide sit beside the brass vernier scale of a water trough." + FAST_TAIL,
             None),
            ("04_two_layer_phospholipid_bilayer_cross_section_model_on_oak_table_pan", 94.0, 5.5, "C", False, "HYDROPHILIC HEADS · HYDROPHOBIC TAILS", "Fast",
             "Fast: daylight close-up pan across a sculpted wooden-and-brass model of a two-molecule phospholipid bilayer showing round polar heads facing outward and paired hydrocarbon tails pointing inward. Nothing emissive, no face.",
             STYLE + "In bright window light on an oak table, a sculpted two-layer phospholipid bilayer model shows rows of round golden heads facing outward and paired silver tails pointing inward." + FAST_TAIL,
             None),
        ],
    ),
    (
        3,
        "Part 03 — February 1957 & 18 February 1972: 25,000 Boiled Crabs (The Sodium-Potassium Pump) & the Fluid Mosaic Model — Midpoint Twist",
        [
            ("01_jens_christian_skou_feb_1957_aarhus_crabs_and_singer_nicolson_18_feb_1972_fluid_mosaic", 99.5, 6.5, "A", False, "PROTEINS FLOAT IN LIQUID FAT", "Quality",
             "Quality: readable faces (Danish physiologist Jens Christian Skou at Aarhus University in February 1957 isolating the Na+/K+-ATPase pump from 25,000 green shore crabs, dissolving to Michael Edidin in March 1970 and Jonathan Singer with Garth Nicolson at UC San Diego on 18 February 1972 unveiling the Fluid Mosaic Model).",
             STYLE + "Split period scene: on the left in February 1957 Aarhus, Jens Christian Skou tests crab-nerve homogenates beside crates of green shore crabs; on the right in February 1972 California, Jonathan Singer and Garth Nicolson point to a model of globular protein icebergs floating through a liquid lipid bilayer." + QUAL_TAIL,
             {"kind": "FACT", "label": "Proteins float in liquid fat", "who_card": "Michael Edidin (born 1939) — American cell biologist", "when_stamp": "1935 · February 1957 · March 1970 · 18 February 1972 · 1997", "timeline_step": "2/3 · Feb 1957 & 18 Feb 1972 (Jens Christian Skou isolates the Na+/K+-ATPase pump from 25,000 crabs; Jonathan Singer & Garth Nicolson propose the Fluid Mosaic Model)", "hold_s": 3.8}),
            ("02_skou_feb_1957_bba_na_k_atpase_and_frye_edidin_1970_singer_nicolson_1972_fluid_mosaic_chart", 106.0, 8.0, "E", False, "FEB 1957 SKOU (BBA: CRAB-NERVE NA+/K+-ATPASE) & MAR 1970 FRYE/EDIDIN + 18 FEB 1972 SINGER & NICOLSON (SCIENCE: FLUID MOSAIC DIFFUSION IN 40 MIN)", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked Skou (February 1957 Biochim. Biophys. Acta 23: 394–401) crab-nerve Na+/K+-ATPase activation curve (requiring both Na+ and K+ ions to hydrolyse ATP) & Frye & Edidin (March 1970 J. Cell Sci. 7: 319–335) / Singer & Nicolson (18 February 1972 Science 175: 720–731) Fluid Mosaic lateral diffusion chart shows 100% intermixing of mouse-human membrane antigens in 40 minutes at 37 °C.",
             {"kind": "DATA", "label": "FEB 1957 SKOU NA+/K+-ATPASE CURVE & 1970/1972 SINGER-NICOLSON FLUID MOSAIC DIFFUSION (100% MIXING IN 40 MIN AT 37 °C)", "detail": "Inked Skou (February 1957 Biochim. Biophys. Acta 23: 394–401) crab-nerve Na+/K+-ATPase activation curve (requiring both Na+ and K+ ions to hydrolyse ATP) & Frye & Edidin (March 1970 J. Cell Sci. 7: 319–335) / Singer & Nicolson (18 February 1972 Science 175: 720–731) Fluid Mosaic lateral diffusion chart (100% intermixing of mouse-human membrane antigens in 40 minutes at 37 °C) on period paper", "scale": "the Fluid Mosaic Model proved that your cell membrane isn't a brick wall — it is a crowded Venice canal two molecules deep, where protein gondolas and pumping stations drift and spin through a liquid oil sea", "hold_s": 3.8}),
            ("03_aarhus_1957_shore_crab_nerve_dissection_tray_and_atpase_assay_tubes_closeup", 114.0, 6.5, "B", False, "FEBRUARY 1957 — THE SODIUM-POTASSIUM PUMP", "Fast",
             "Fast: daylight macro shot of a green shore crab specimen on a dissection tray beside labelled glass test tubes of Na+, K+, and Mg2+ buffer and a 1957 Biochimica et Biophysica Acta offprint on a bench. Nothing emissive, no face.",
             STYLE + "In crisp daylight on a 1957 Aarhus physiology bench, a preserved green shore crab on a porcelain tray sits beside a rack of glass assay tubes and an open scientific paper." + FAST_TAIL,
             None),
            ("04_singer_nicolson_1972_fluid_mosaic_model_with_transmembrane_protein_icebergs_pan", 120.5, 5.5, "C", False, "18 FEBRUARY 1972 — THE FLUID MOSAIC MODEL", "Fast",
             "Fast: daylight close-up pan across a sculpted 1972 Fluid Mosaic membrane model showing large carved protein channels and pumps spanning a two-layer phospholipid bilayer on an oak table. Nothing emissive, no face.",
             STYLE + "In bright window light on an oak table, a sculpted architectural model of the Fluid Mosaic cell membrane shows globular protein channels embedded across a two-layer sea of golden lipid spheres." + FAST_TAIL,
             None),
        ],
    ),
    (
        4,
        "Part 04 — 9 October 1991 & 17 April 1992: Peter Agre's Exploding Frog Eggs & the Aquaporin Water Channel",
        [
            ("01_peter_agre_gregory_preston_oct_1991_apr_1992_exploding_frog_eggs_and_aquaporin_hourglass", 126.0, 6.5, "A", False, "3 BILLION WATERS PER SECOND", "Quality",
             "Quality: readable faces (American haematologist Peter Agre and postdoc Gregory Preston at Johns Hopkins on 9 October 1991 / 17 April 1992 watching six CHIP28 Aquaporin-1 frog eggs swell and burst in distilled water beside six intact control eggs, dissolving to Roderick MacKinnon and the October 2000 2.8-angstrom hourglass structure of Aquaporin-1).",
             STYLE + "Split period scene: on the left in October 1991 Baltimore, Peter Agre and Gregory Preston peer into a Petri dish where six aquaporin-injected frog eggs swell and burst open beside six calm control eggs; on the right, they point to a 2.8-angstrom hourglass channel model flipping single-file water molecules." + QUAL_TAIL,
             {"kind": "FACT", "label": "3 billion waters per second", "who_card": "Gregory M. Preston (born 1958) — American molecular biologist · Roderick MacKinnon (born 1956) — American biophysicist", "when_stamp": "1988 · 9 October 1991 · 17 April 1992 · October 2000 · 2003", "timeline_step": "3/3 · 9 Oct 1991 / 17 Apr 1992 & Oct 2000 (Peter Agre & Gregory Preston discover Aquaporin-1 via exploding frog oocytes; 2.8-angstrom NPA hourglass structure solved)", "hold_s": 3.8}),
            ("02_preston_agre_17_apr_1992_science_oocyte_swelling_and_murata_2000_nature_2_8a_npa_chart", 132.5, 8.0, "E", False, "17 APR 1992 PRESTON & AGRE (SCIENCE: CHIP28 OOCYTE RUPTURE IN 3 MIN) & OCT 2000 MURATA/AGRE (NATURE: 2.8-Å NPA HOURGLASS, 3×10^9 H2O/S, 0 H+)", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked Preston, Carroll, Guggino & Agre (17 April 1992 Science 256: 385–387) Xenopus oocyte osmotic swelling & explosion curve (CHIP28/Aquaporin-1 vs control in hypotonic buffer over 3 minutes) alongside Murata, Fujiyoshi & Agre (5 October 2000 Nature 407: 599–605) 2.8-angstrom NPA hourglass dipole water-flip diagram shows 3 x 10^9 water molecules per second streaming in single file with zero proton (H+) conduction.",
             {"kind": "DATA", "label": "17 APR 1992 AGRE CHIP28 OOCYTE SWELLING CURVE (3 MIN RUPTURE) & 2000 2.8-Å AQUAPORIN NPA HOURGLASS (3×10^9 H2O/S, 0 PROTONS)", "detail": "Inked Preston, Carroll, Guggino & Agre (17 April 1992 Science 256: 385–387) Xenopus oocyte osmotic swelling & explosion curve (CHIP28/Aquaporin-1 vs water-injected control in hypotonic 70 mosM buffer over 3 minutes, reversibly blocked by HgCl2) alongside Murata, Fujiyoshi & Agre (October 2000 Nature 407: 599–605) 2.8-angstrom NPA hourglass dipole water-flip diagram on period paper", "scale": "an aquaporin channel is like a stadium turnstile exactly one water molecule wide — three billion water molecules sprint through in single file every second, but at the midpoint two electric magnets spin each water molecule halfway round so acid protons trying to hop along the line are stopped cold", "hold_s": 3.8}),
            ("03_baltimore_1991_control_vs_burst_xenopus_oocyte_dishes_and_stopwatch_closeup", 140.5, 6.5, "B", False, "17 APRIL 1992 — AQUAPORIN WATER CHANNELS", "Fast",
             "Fast: daylight macro shot of two labelled glass Petri dishes — six intact frog oocytes on the left and six burst frog oocytes on the right — beside a mechanical stopwatch reading three minutes on a bench. Nothing emissive, no face.",
             STYLE + "In crisp daylight on a 1991 Baltimore laboratory bench, two glass Petri dishes of frog eggs — six intact spheres in the left dish and six ruptured shells in the right dish — sit beside a silver mechanical stopwatch." + FAST_TAIL,
             None),
            ("04_explorer_at_aquaporin_hourglass_turnstile_flipping_single_file_water_molecules_and_blocking_protons", 147.0, 5.5, "B", True, None, "Quality",
             "Quality: Explorer beat 2 (locked character reference).",
             STYLE + "Standing beside a large cut-away hourglass model of the Aquaporin channel, the Explorer guides a single-file line of red-and-white water molecule models through the narrow 2.8-angstrom waist, rotating the middle water model halfway round at the central brass NPA clasp while closing a gate bar against a cluster of proton spheres." + EXP_TAIL,
             None),
        ],
    ),
    (
        5,
        "Part 05 — Why Soap Dissolves Viruses & How Liposomes Deliver Medicines — & How Sausage Casings Built the First Artificial Kidney",
        [
            ("01_timeline_1895_2003_and_soap_micelle_liposome_bilayer_chart", 152.5, 8.5, "E", False, "1895–2003 TIMELINE · OVERTON/GORTER-GRENDEL 2:1 BILAYER, SKOU PUMP, SINGER-NICOLSON FLUID MOSAIC, AGRE AQUAPORINS & LIPOSOMES", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, the 3-era timeline completes: 1895 & 1 Apr 1925 (Ernest Overton discovers the lipid permeability barrier; Evert Gorter & François Grendel measure the 2:1 red-blood-cell lipid monolayer on water, proving the phospholipid bilayer) · Feb 1957 & 18 Feb 1972 (Jens Christian Skou isolates the Na+/K+-ATPase sodium-potassium pump from 25,000 crabs, winning the 1997 Nobel Prize; Jonathan Singer & Garth Nicolson propose the Fluid Mosaic Model) · 9 Oct 1991 / 17 Apr 1992 (Peter Agre & Gregory Preston prove CHIP28 / Aquaporin-1 is the cellular water channel via exploding frog oocytes, winning the 2003 Nobel Prize).",
             {"kind": "DATA", "label": "1895–2003 CELL MEMBRANE TIMELINE · SOAP DISRUPTION OF VIRAL ENVELOPES & BANGHAM 1964 SYNTHETIC LIPOSOMES", "detail": "Animated timeline (1895 → 2003) alongside an inked diagram of amphiphilic soap molecules prying apart viral lipid envelopes and synthetic two-molecule liposomes encapsulating cargo", "scale": "from a silk thread on a water trough in Leiden to twenty-five thousand shore crabs in Denmark and six exploding frog eggs in Baltimore, scientists proved that the two-molecule skin around every cell is a living, breathing border gate", "when_stamp": "1895–2003", "timeline_step": "3/3 · 1895–2003 timeline complete", "hold_s": 3.8}),
            ("02_synthetic_liposome_sphere_beside_rotating_wooden_drum_dialysis_model_on_plinth_pan", 161.0, 5.5, "A", False, "SOAP MOLECULES & LIPID NANOPARTICLES", "Fast",
             "Fast: daylight close-up of a cut-away spherical two-layer liposome model beside a miniature rotating wooden slatted drum wrapped in cellophane sausage tubing on a wooden museum plinth. Nothing emissive, no face.",
             STYLE + "In crisp daylight on a wooden museum plinth, a cut-away spherical two-layer lipid vesicle model sits beside a rotating slatted wooden drum wound with cellophane tubing." + FAST_TAIL,
             None),
            ("03_bowman_1842_ludwig_1844_wearn_richards_1924_homer_smith_1934_and_kolff_1943_1945_kidney_handoff", 166.5, 6.5, "C", False, "KIDNEYS, THE NEPHRON & KOLFF'S DIALYSIS MACHINE", "Quality",
             "Quality: readable faces (William Bowman in London in February 1842 and Carl Ludwig in 1844 mapping Bowman's capsule, Joseph Wearn and Alfred Richards in 1924 puncturing a frog glomerulus with a quartz micropipette alongside Homer Smith in 1934 measuring 180 litres a day, and Dutch physician Willem Kolff in Kampen in 1943–September 1945 operating his rotating sausage-casing artificial kidney — handoff to 072 Kidneys, the Nephron & Willem Kolff's Dialysis Machine).",
             STYLE + "Split period scene: on the left, William Bowman in 1842 London and Alfred Richards in 1924 with a quartz micropipette map the microscopic nephron filter cup; on the right in September 1945 Kampen, Dutch doctor Willem Kolff tends his rotating wooden-drum artificial kidney wound with cellophane sausage casing." + QUAL_TAIL,
             {"kind": "WHEN", "label": "FEBRUARY 1842 · 1844 · 1924 · 1934 · 11 SEPTEMBER 1945", "hold_s": 3.5}),
            ("04_table_three_callback", 173.0, 2.4, "C", False, None, "reuse",
             "Reuse: verified unused moving window [5.50s..7.90s] of P1:07_table_three_props_1925_langmuir_trough_1957_shore_crab_jar_and_1991_oocyte_petri_dish (callback, £0).",
             "Reuse P1:07_table_three_props_1925_langmuir_trough_1957_shore_crab_jar_and_1991_oocyte_petri_dish [5.50s..7.90s] (2.40s distinct non-overlapping tail window from 8.00s source clip).",
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
                row["reuse_of"] = "P1:07_table_three_props_1925_langmuir_trough_1957_shore_crab_jar_and_1991_oocyte_petri_dish"
                row["reuse_window_s"] = [5.5, 7.9]
                row["reuse_audit"] = {
                    "source_row": "P1:07_table_three_props_1925_langmuir_trough_1957_shore_crab_jar_and_1991_oocyte_petri_dish",
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
            "film": "071_Overton-Gorter-Skou-Singer-Agre-Cell-Membrane-Aquaporins",
            "part": p_idx,
            "title": p_title,
            "version": "v01",
            "timing_status": "pre_vo_script_clock (built from cell_membrane_script_master_v01.md; retimes onto Scribe STT once VO locks)",
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
        "film": "071_Overton-Gorter-Skou-Singer-Agre-Cell-Membrane-Aquaporins",
        "version": "v01",
        "date": "2026-10-20",
        "owner": "gemini (J0706)",
        "status": "PRE_VO_BOARDS_V01_NO_MINT",
        "generation_authorized": False,
        "script": "00_Brand/Channel-Setup/ideas/071_Overton-Gorter-Skou-Singer-Agre-Cell-Membrane-Aquaporins/cell_membrane_script_master_v01.md",
        "sources": "00_Brand/Channel-Setup/ideas/071_Overton-Gorter-Skou-Singer-Agre-Cell-Membrane-Aquaporins/SOURCES_v01.md",
        "credit_snapshot": {
            "flow_balance": 23740,
            "flow_floor": 0,
            "flow_read_at": "2026-10-15T21:42:22Z",
            "vertex_promo_gbp": 71.02,
            "vertex_usable_gbp": 70.02,
        },
        "totals": totals,
        "per_part": per_part_summary,
        "mint_order": "006 > 007 > 008 > 009 > 010 > 011 > 012 > 013 > 014 > 015 > 016 > 017 > 018 > 019 > 020 > 021 > 022 > 023 > 024 > 025 > 026 > 027 > 028 > 029 > 030 > 031 > 032 > 033 > 034 > 035 > 036 > 037 > 038 > 039 > 040 > 041 > 042 > 043 > 044 > 045 > 046 > 047 > 048 > 049 > 050 > 051 > 052 > 053 > 054 > 055 > 056 > 057 > 058 > 059 > 060 > 061 > 062 > 063 > 064 > 065 > 066 > 067 > 068 > 069 > 070 > 071 > 072 > 073 > 074 > 075 > 076 > 077. Nothing in 071 is generation_authorized.",
    }
    (EDIT / "PICTURE_PLAN_v01.json").write_text(json.dumps(plan, indent=2) + "\n")

    sl = [
        "# 071 Cell Membranes: The Two-Molecule Skin of Life — Shot list & plate boards v01 (pre-VO)",
        "",
        "Gemini, 20 Oct 2026, J0706. Built from `cell_membrane_script_master_v01.md` (`91.8/100 PASS`) and `SOURCES_v01.md`.",
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
        "# 071 price review v01 (pre-VO plate boards)",
        "",
        "Gemini, 20 Oct 2026, J0706. Boards only. **No mint. No spend. No merge.**",
        "Prepared from `cell_membrane_script_master_v01.md` (`91.8/100 PASS`) and `SOURCES_v01.md` so 071's full plate board rows, non-emissive Fast prompts, £0 code graphics, and Teach-on-Screen overlays are ready to re-time the moment long VO locks. Parked for Chief.",
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
        f"- **Quality ({totals['Quality']} rows):** readable faces (Charles Ernest Overton, Evert Gorter, François Grendel, Jens Christian Skou, Michael Edidin, S. Jonathan Singer, Garth L. Nicolson, Peter Agre, Gregory M. Preston, Roderick MacKinnon, William Bowman, Alfred N. Richards, Willem J. Kolff), 1 April 1925 Leiden `2:1` red-blood-cell lipid monolayer Langmuir trough, February 1957 Aarhus `25,000-crab` `Na⁺/K⁺-ATPase` & 18 February 1972 `Fluid Mosaic Model`, 9 October 1991 / 17 April 1992 Baltimore exploding `CHIP28` (`Aquaporin-1`) frog oocytes, and the 2 Explorer beats.",
        f"- **Fast ({totals['Fast']} rows, non-emissive):** daylight prop and laboratory shots (brass Langmuir water trough with silk thread, sculpted phospholipid model & 1925 *J. Exp. Med.* offprint pan, 3-object callback bench, acetone extraction flask with hemocytometer slide & vernier trough scale, sculpted 2-layer phospholipid bilayer cross-section model, green shore crab dissection tray & `ATPase` assay tubes, 1972 `Fluid Mosaic` architectural model, intact vs ruptured *Xenopus* oocyte Petri dishes & 3-minute stopwatch, cut-away liposome sphere & rotating wooden-drum dialysis model on museum plinth). Zero candles, flames, sparks, or glowing elements on Fast.",
        f"- **£0 code graphics ({totals['code_graphic']} rows):**",
        "  1. `P1:04_gorter_grendel_1925_skou_1957_singer_1972_and_agre_1992_membrane_transport_chart` — `5 nm` phospholipid bilayer (`2.0:1` monolayer ratio), Skou's `Na⁺/K⁺-ATPase` (`3 Na⁺` out / `2 K⁺` in, `~30%` resting mammalian ATP) & Agre's `Aquaporin-1` (`~3 × 10⁹ H₂O/s`, `0` proton leakage) (`SCALE: the membrane around every cell in your body is a self-sealing soap bubble just two molecules thick — twenty thousand times thinner than a sheet of kitchen paper, yet studded with protein gates that check the passport of every atom trying to cross`)",
        "  2. `P1:06_gorter_grendel_1_apr_1925_jem_2_to_1_erythrocyte_lipid_monolayer_trough_chart` — Evert Gorter & François Grendel (1 April 1925 *J. Exp. Med.*) `2.0:1` erythrocyte lipid-monolayer table across 6 mammalian species (`SCALE: spreading all the fat molecules from a red blood cell flat onto water is like unpeeling a two-ply tissue into a single sheet — when the single sheet covers exactly twice the area of the cell, you know the cell was wrapped in two layers back to back`)",
        "  3. `P2:02_overton_1895_olive_oil_partition_and_gorter_grendel_1925_bar_1966_double_error_chart` — Ernest Overton (1895) olive-oil partition curve & Gorter/Grendel (1925) + Bar, Deamer & Cornwell (26 August 1966 *Science*) double-error cancellation chart (`SCALE: Gorter and Grendel getting the right two-to-one bilayer answer from an incomplete fat extraction and a shrunken cell measurement is like miscounting your change by ten pence when the shopkeeper also undercharged you by ten pence — both errors vanished and left the exact truth`)",
        "  4. `P3:02_skou_feb_1957_bba_na_k_atpase_and_frye_edidin_1970_singer_nicolson_1972_fluid_mosaic_chart` — Jens Christian Skou (February 1957 *BBA*) `Na⁺/K⁺-ATPase` activation curve & Frye/Edidin (March 1970) + Singer & Nicolson (18 February 1972 *Science*) `Fluid Mosaic` lateral diffusion chart (`100%` intermixing in `40 min` at `37 °C`) (`SCALE: the Fluid Mosaic Model proved that your cell membrane isn't a brick wall — it is a crowded Venice canal two molecules deep, where protein gondolas and pumping stations drift and spin through a liquid oil sea`)",
        "  5. `P4:02_preston_agre_17_apr_1992_science_oocyte_swelling_and_murata_2000_nature_2_8a_npa_chart` — Preston & Agre (17 April 1992 *Science*) *Xenopus* oocyte osmotic swelling curve (`3 min` rupture) & Murata, Fujiyoshi & Agre (5 October 2000 *Nature*) `2.8 Å` `NPA` hourglass dipole water-flip diagram (`SCALE: an aquaporin channel is like a stadium turnstile exactly one water molecule wide — three billion water molecules sprint through in single file every second, but at the midpoint two electric magnets spin each water molecule halfway round so acid protons trying to hop along the line are stopped cold`)",
        "  6. `P5:01_timeline_1895_2003_and_soap_micelle_liposome_bilayer_chart` — completed timeline (1895 → 2003) + soap disruption of viral lipid envelopes & Alec Bangham's 1964 synthetic liposomes (`SCALE: from a silk thread on a water trough in Leiden to twenty-five thousand shore crabs in Denmark and six exploding frog eggs in Baltimore, scientists proved that the two-molecule skin around every cell is a living, breathing border gate`)",
        f"- **£0 verified reuse ({totals['reuse']} row):** `P5:04_table_three_callback` uses the 2.40 s unused moving tail `[5.50s..7.90s]` of `P1:07_table_three_props_1925_langmuir_trough_1957_shore_crab_jar_and_1991_oocyte_petri_dish`.",
        "",
        "## Mint order",
        "",
        "006 > 007 > 008 > 009 > 010 > 011 > 012 > 013 > 014 > 015 > 016 > 017 > 018 > 019 > 020 > 021 > 022 > 023 > 024 > 025 > 026 > 027 > 028 > 029 > 030 > 031 > 032 > 033 > 034 > 035 > 036 > 037 > 038 > 039 > 040 > 041 > 042 > 043 > 044 > 045 > 046 > 047 > 048 > 049 > 050 > 051 > 052 > 053 > 054 > 055 > 056 > 057 > 058 > 059 > 060 > 061 > 062 > 063 > 064 > 065 > 066 > 067 > 068 > 069 > 070 > 071 > 072 > 073 > 074 > 075 > 076 > 077. `generation_authorized` is `false` on every row.",
    ])
    (EDIT / "PRICE_REVIEW_v01.md").write_text("\n".join(pr_lines) + "\n")
    print(f"071 v01 boards written: {totals['rows']} rows, Flow expected={totals['flow_credits_expected']}")


if __name__ == "__main__":
    main()
