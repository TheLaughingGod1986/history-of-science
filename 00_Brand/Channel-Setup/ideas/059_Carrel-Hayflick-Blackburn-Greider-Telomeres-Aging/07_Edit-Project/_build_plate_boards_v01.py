#!/usr/bin/env python3
"""HOS 059 (Telomeres: The Countdown Clock Inside Your Cells) pre-VO plate boards v01. J0631. No mint, no spend.

Built from 00_Brand/Channel-Setup/ideas/059_Carrel-Hayflick-Blackburn-Greider-Telomeres-Aging/telomeres_script_master_v01.md
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
        "Part 01 — The Shoelace Caps Counting Down Inside Your DNA",
        [
            ("01_dividing_chromosome_ttaggg_telomere_cap_50_divisions_and_greider_blackburn_telomerase", 0.0, 5.5, "A", False, "50 DIVISIONS & TELOMERE CAPS", "Quality",
             "Quality: Short frame 0 / answer image (0:03) + a dividing human chromosome zooms in to its protective shoelace-cap tips (repeating TTAGGG telomere sequences), where each cell division snips a piece off the cap until Leonard Hayflick's 50-division limit stops the cell — and then Carol Greider and Elizabeth Blackburn's Christmas Day 1984 enzyme telomerase stitches fresh TTAGGG repeats back onto the tip.",
             STYLE + "Split microscopic-and-laboratory scene: on the left, a dividing chromosome's protective golden shoelace cap shortens step by step until a molecular telomerase machine stitches fresh repeating links onto the tip; on the right on Christmas Day 1984 at Berkeley, Carol Greider and Elizabeth Blackburn inspect a banded autoradiogram film." + QUAL_TAIL,
             {"kind": "WHEN", "label": "BERKELEY, 25 DECEMBER 1984", "timeline_step": "4/4 · 25 Dec 1984 (Carol Greider & Elizabeth Blackburn discover telomerase on Christmas Day at UC Berkeley; 2009 Nobel Prize with Szostak)", "hold_s": 3.5}),
            ("02_carrel_1912_hayflick_1961_olovnikov_1971_subway_and_blackburn_greider_1984_split", 5.5, 6.0, "B", False, "CHICKEN HEART MYTH, 50 DIVISIONS, TELOMERASE", "Quality",
             "Quality: complex three-part composition (Alexis Carrel at the Rockefeller Institute in New York on 17 January 1912 tending his famous 'immortal' chicken-heart culture vs Leonard Hayflick in Philadelphia in December 1961 discovering the 50-division Hayflick Limit; Alexey Olovnikov in a Moscow subway station in 1971 sketching DNA replication tracks; and Elizabeth Blackburn and Carol Greider at UC Berkeley on Christmas Day, 25 December 1984 discovering telomerase).",
             STYLE + "Three-panel period composition: on the left, Alexis Carrel in 1912 New York beside a glass tissue flask and Leonard Hayflick in 1961 Philadelphia inspecting fibroblast culture bottles; in the centre, Alexey Olovnikov in a 1971 Moscow subway station sketching train tracks in a notebook; on the right, Elizabeth Blackburn and Carol Greider in 1984 Berkeley examining a telomerase gel ladder." + QUAL_TAIL,
             None),
            ("03_shoelace_aglet_morphing_to_chromosome_ttaggg_cap_fraying_across_50_divisions", 11.5, 6.0, "C", False, "DNA SHOELACE CAPS (TTAGGG)", "Quality",
             "Quality: complex conceptual and microscopic reveal (a frayed shoelace aglet morphs into the tip of a human chromosome capped by thousands of repeating TTAGGG letters, shrinking by 50–200 base pairs per division across 50 doublings until cellular senescence).",
             STYLE + "Split conceptual-and-microscopic scene: on the left, a braided cord's protective brass aglet tip frays away piece by piece; on the right, the matching tip of a coiled chromosome loses short repeating cap segments with each cell division." + QUAL_TAIL,
             {"kind": "WHEN", "label": "17 JANUARY 1912 · DECEMBER 1961 · 1971 · MARCH 1978 · 25 DECEMBER 1984", "timeline_step": "1/4 · 17 Jan 1912 (Carrel) · 2/4 · Dec 1961 (Hayflick & Moorhead) · 3/4 · 1971 & Mar 1978–1982 (Olovnikov, Blackburn & Szostak) · 4/4 · 25 Dec 1984 (Greider & Blackburn)", "hold_s": 3.5}),
            ("04_hayflick_1961_and_blackburn_greider_1984_telomere_15kb_to_4kb_50_divisions_chart", 17.5, 8.0, "E", False, "10–15 KB TTAGGG AT BIRTH → −50–200 BP/DIVISION → ~50 DIVISIONS (HAYFLICK LIMIT AT ~4 KB) VS TELOMERASE REBUILDING", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked Hayflick division limit & telomere shortening chart from Hayflick & Moorhead (December 1961 Exp. Cell Res. 25: 585–621), Blackburn & Gall (March 1978 J. Mol. Biol. 120: 33–53), and Greider & Blackburn (December 1985 Cell 43: 405–413) plots human telomere length (~10–15 kb of TTAGGG repeats at birth) dropping with each cell doubling until hitting the Hayflick senescence threshold at ~50 divisions (~4–5 kb), contrasted with germ cells, stem cells, and cancer cells maintaining telomere length via telomerase.",
             {"kind": "DATA", "label": "10–15 KB TTAGGG REPEATS AT BIRTH (−50–200 BP/DIVISION) → ~50 DIVISIONS HAYFLICK LIMIT VS TELOMERASE EXTENSION", "detail": "Inked human telomere attrition & Hayflick limit chart on period paper showing human chromosome ends starting with ~10,000–15,000 base pairs of TTAGGG repeats at birth, losing ~50–200 base pairs per cell division across ~50 doublings (the Hayflick Limit) down to the ~4,000-bp senescence barrier, while telomerase rebuilds TTAGGG repeats in germ and stem cells", "scale": "each of your forty-six chromosomes starts life with a protective DNA fuse about ten thousand letters long — and every time a cell divides, up to two hundred letters burn off the tip until after fifty divisions the fuse runs out", "who_card": "Alexis Carrel (1873–1944) — French surgeon and biologist · Leonard Hayflick (1928–2024) — American anatomist and microbiologist · Paul S. Moorhead (1927–2020) — American geneticist · Alexey M. Olovnikov (1936–2022) — Russian theoretical biologist · Elizabeth H. Blackburn (born 1948) — Australian-American molecular biologist · Jack W. Szostak (born 1952) — British-American geneticist · Carol W. Greider (born 1961) — American molecular biologist", "when_stamp": "17 January 1912 · December 1961 · 1971 · March 1978 · 25 December 1984", "hold_s": 3.8}),
            ("05_shoelace_aglets_carrel_flask_chromosome_model_and_brass_counter_pan", 25.5, 5.5, "A", False, "50–200 LETTERS LOST PER DIVISION", "Fast",
             "Fast: daylight macro pan across brass-tipped shoelace aglets, a vintage Carrel glass tissue-culture flask, a carved chromosome model with golden end-caps, and a brass 50-click tally counter on an oak bench between code graphics so two full-frame graphics never run back to back. Nothing emissive, no face.",
             STYLE + "In crisp daylight on an oak laboratory bench, the camera pans smoothly across brass-tipped shoelaces, a flat round Carrel glass culture flask, a wooden chromosome model with golden end-caps, and a brass tally counter." + FAST_TAIL,
             None),
            ("06_olovnikov_1971_watson_1972_lagging_strand_end_replication_subway_track_chart", 31.0, 8.0, "E", False, "THE END-REPLICATION PROBLEM", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period parchment, an inked DNA end-replication subway-train diagram (from Olovnikov 1971 & Watson 1972) compares leading-strand continuous synthesis against lagging-strand Okazaki fragments, where removing the terminal RNA primer leaves a 50–200 nucleotide uncopied gap at the chromosome end on every division.",
             {"kind": "DATA", "label": "OLOVNIKOV (1971) & WATSON (1972) END-REPLICATION PROBLEM: LAGGING-STRAND RNA PRIMER GAP LOSES 50–200 NT/DIVISION", "detail": "Inked end-replication problem diagram comparing leading-strand continuous synthesis against lagging-strand Okazaki fragments, where removing the terminal RNA primer leaves a 50–200 nucleotide uncopied gap at the chromosome end on every division", "scale": "the enzyme that copies your DNA is like a painter backing down a wooden hallway who can paint every floorboard except the final board he is standing on — so every copy of the hallway comes out one board shorter", "hold_s": 3.8}),
            ("07_table_three_props_carrel_1912_flask_hayflick_1961_culture_bottle_and_greider_1984_gel_plate", 39.0, 5.5, "C", False, "1912 TO 2009", "Fast",
             "Fast: daylight prop table (callback source for Part 05: Alexis Carrel's 1912 flat glass culture flask, Leonard Hayflick's 1961 glass fibroblast bottle, and Carol Greider's 1984 banded telomerase autoradiogram print). Nothing emissive.",
             STYLE + "On an oak workbench in soft window light sit three objects side by side: a vintage two-necked Carrel glass flask, a square glass cell-culture bottle, and a framed six-letter ladder gel print." + FAST_TAIL,
             None),
            ("08_explorer_rolling_telomerase_track_layer_to_extend_chromosome_railway_for_dna_polymerase_train", 62.0, 5.5, "A", True, None, "Quality",
             "Quality: Explorer beat 1 (locked character reference, after 1:00).",
             STYLE + "Standing at the end of a wooden railway track where a brass locomotive has halted at the cliff edge, the Explorer wheels in a clockwork track-laying cart that stamps six new wooden sleepers onto the end of the line so the locomotive can roll forward." + EXP_TAIL,
             None),
            ("09_carol_greider_25_dec_1984_berkeley_holding_telomerase_repeat_autoradiogram_film", 67.5, 5.5, "B", False, "BERKELEY, 25 DECEMBER 1984", "Quality",
             "Quality: readable face (at UC Berkeley on Christmas Day, 25 December 1984, 23-year-old graduate student Carol Greider holds up a freshly developed autoradiogram film showing ladder bands of newly synthesized telomere repeats).",
             STYLE + "In a 1984 UC Berkeley molecular biology lab, young graduate student Carol Greider in a white lab coat holds up a developed X-ray film displaying a crisp repeating ladder of six-base telomere bands." + QUAL_TAIL,
             {"kind": "WHEN", "label": "BERKELEY, 25 DECEMBER 1984", "timeline_step": "4/4 · 25 Dec 1984 (Carol Greider & Elizabeth Blackburn discover telomerase at UC Berkeley)", "hold_s": 3.5}),
        ],
    ),
    (
        2,
        "Part 02 — 17 January 1912 – December 1961: Alexis Carrel's 34-Year 'Immortal' Chicken Heart Myth & Leonard Hayflick's 50-Division Limit",
        [
            ("01_carrel_17_jan_1912_rockefeller_chicken_heart_and_hayflick_moorhead_dec_1961_wistar_50_limit", 73.0, 6.5, "A", False, "50 DIVISIONS, THEN CELLS STOP", "Quality",
             "Quality: readable faces (French surgeon Alexis Carrel on 17 January 1912 at the Rockefeller Institute in New York tending his embryonic chicken-heart flask, dissolving to American microbiologist Leonard Hayflick and cytogeneticist Paul Moorhead at the Wistar Institute in Philadelphia in December 1961 proving the 50-division Hayflick Limit).",
             STYLE + "Split period scene: on the left in 1912 New York, surgeon Alexis Carrel in a dark surgical cap pipettes chick-embryo broth into a flat glass culture flask; on the right in December 1961 Philadelphia, Leonard Hayflick and Paul Moorhead inspect human fibroblast culture bottles and chromosome slides." + QUAL_TAIL,
             {"kind": "FACT", "label": "50 divisions, then cells stop", "when_stamp": "17 January 1912 · 1946 · December 1961", "timeline_step": "1/4 · 17 Jan 1912 (Alexis Carrel's 34-year chicken-heart culture) & 2/4 · Dec 1961 (Hayflick & Moorhead prove the ~50-division Hayflick Limit)", "hold_s": 3.8}),
            ("02_hayflick_moorhead_dec_1961_phase_i_ii_iii_50_doublings_and_male_female_mix_chart", 79.5, 8.0, "E", False, "DEC 1961 HAYFLICK & MOORHEAD: ~50 ± 10 POPULATION DOUBLINGS (PHASE III SENESCENCE), 40-DOUBLING MALE + 10-DOUBLING FEMALE MIX & LIQUID-N2 MEMORY", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked Hayflick & Moorhead (December 1961, Experimental Cell Research 25: 585–621) growth curve & male/female co-culture chart shows Phase I (primary culture), Phase II (exponential growth across ~50 ± 10 population doublings), and Phase III (replicative senescence), alongside the 40-doubling male + 10-doubling female mixed-dish proof and liquid-nitrogen division memory.",
             {"kind": "DATA", "label": "DEC 1961 HAYFLICK & MOORHEAD: ~50 DOUBLINGS LIMIT, 40-DIV MALE + 10-DIV FEMALE MIXED DISH & CRYOPRESERVATION MEMORY", "detail": "Inked Hayflick & Moorhead (December 1961, Experimental Cell Research 25: 585–621) growth curve & male/female co-culture chart on period paper showing Phase I (primary culture), Phase II (exponential growth across ~50 ± 10 population doublings), and Phase III (replicative senescence), alongside the 40-doubling male + 10-doubling female mixed-dish proof and liquid-nitrogen division memory", "scale": "even if you freeze a human cell in liquid nitrogen at minus one hundred and ninety-six degrees for ten years after twenty divisions, the moment you thaw it out it remembers its exact count and divides only thirty more times", "hold_s": 3.8}),
            ("03_wistar_1961_glass_culture_bottles_liquid_nitrogen_dewar_and_chromosome_spread_closeup", 87.5, 6.5, "B", False, "DECEMBER 1961 — THE HAYFLICK LIMIT", "Fast",
             "Fast: daylight macro shot of square glass cell-culture bottles beside a stainless-steel liquid-nitrogen storage canister and a male/female karyotype print on a 1961 Philadelphia bench. Nothing emissive, no face.",
             STYLE + "In crisp daylight on a 1961 Philadelphia laboratory bench, square glass culture bottles sit beside a brushed steel cryo-storage canister and a printed chromosome karyotype sheet." + FAST_TAIL,
             None),
            ("04_rockefeller_1912_carrel_d_flask_glass_pipettes_and_embryo_extract_centrifuge_pan", 94.0, 5.5, "C", False, "17 JANUARY 1912 — CARREL'S FLASK", "Fast",
             "Fast: daylight close-up pan across a vintage 1912 Carrel D-flask, glass pipettes, and a hand-cranked centrifuge tube of unstrained chick-embryo broth. Nothing emissive, no face.",
             STYLE + "In bright window light on a 1912 laboratory table, a flat round Carrel glass flask sits beside glass pipettes and a brass hand-centrifuge holding glass broth tubes." + FAST_TAIL,
             None),
        ],
    ),
    (
        3,
        "Part 03 — 1938, 1971 & 1978–1982: Alexey Olovnikov's Moscow Subway Train & Elizabeth Blackburn and Jack Szostak's TTGGGG Shoelace Caps — Midpoint Twist",
        [
            ("01_olovnikov_1971_moscow_subway_and_blackburn_szostak_1978_1982_tetrahymena_yeast_telomeres", 99.5, 6.5, "A", False, "POND-SCUM CAPS WORK IN YEAST", "Quality",
             "Quality: readable faces (Russian theoretical biologist Alexey Olovnikov in a 1971 Moscow subway station sketching lagging-strand DNA tracks, dissolving to Elizabeth Blackburn and Jack Szostak in 1978–1982 sequencing Tetrahymena TTGGGG telomere repeats and proving they protect linear DNA in baker's yeast).",
             STYLE + "Split period scene: on the left in 1971 Moscow, Alexey Olovnikov stands on a tiled subway platform sketching train tracks as a DNA helix in his notebook; on the right in 1982, Elizabeth Blackburn and Jack Szostak examine a pond-water ciliate microscope slide and a yeast plasmid gel." + QUAL_TAIL,
             {"kind": "FACT", "label": "Pond-scum caps work in yeast", "who_card": "Hermann J. Muller (1890–1967) — American geneticist · Barbara McClintock (1902–1992) — American cytogeneticist", "when_stamp": "1938 · 1971 · March 1978 · 1982 · 1988", "timeline_step": "3/4 · 1971 & Mar 1978–1982 (Olovnikov predicts the DNA end-replication problem; Blackburn & Szostak sequence TTGGGG telomere repeats and prove cross-species protection in yeast)", "hold_s": 3.8}),
            ("02_olovnikov_1971_blackburn_gall_1978_szostak_1982_tetrahymena_ttgggg_yeast_human_ttaggg_chart", 106.0, 8.0, "E", False, "MAR 1978 BLACKBURN & GALL (TTGGGG), MAY 1982 SZOSTAK & BLACKBURN (YEAST PLASMID) & 1988 MOYZIS (HUMAN TTAGGG): CROSS-SPECIES TELOMERE CONSERVATION", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked Tetrahymena-to-yeast telomere conservation & TTAGGG repeat chart from Olovnikov (1971, Doklady / 1973 J. Theor. Biol. 41: 181–190), Blackburn & Gall (March 1978, J. Mol. Biol. 120: 33–53), Szostak & Blackburn (May 1982, Cell 29: 245–255), and Moyzis et al. (1988, PNAS 85: 6622–6626) shows Tetrahymena TTGGGG repeats protecting linear plasmids in yeast and human TTAGGG repeats (~10–15 kb at birth) capping all 46 human chromosomes.",
             {"kind": "DATA", "label": "1978–1988 TELOMERE CODE: TETRAHYMENA (TTGGGG) PROTECTS YEAST DNA & HUMAN (TTAGGG) CAPS ALL 46 CHROMOSOMES", "detail": "Inked Tetrahymena-to-yeast telomere conservation & TTAGGG repeat chart on period paper from Olovnikov (1971, Doklady / 1973 J. Theor. Biol. 41: 181–190), Blackburn & Gall (March 1978, J. Mol. Biol. 120: 33–53), Szostak & Blackburn (May 1982, Cell 29: 245–255), and Moyzis et al. (1988, PNAS 85: 6622–6626) showing Tetrahymena TTGGGG repeats protecting linear plasmids in yeast and human TTAGGG repeats (~10–15 kb at birth) capping all 46 human chromosomes", "scale": "the six-letter shoelace cap at the tip of your DNA is so ancient that when Blackburn and Szostak stitched telomeres from pond scum onto chromosomes inside baker's yeast, the yeast recognised the code across a billion years of evolution", "hold_s": 3.8}),
            ("03_yale_1978_tetrahymena_pond_flask_yeast_agar_plates_and_sequencing_gel_closeup", 114.0, 6.5, "B", False, "MAY 1982 — CROSS-SPECIES TELOMERES", "Fast",
             "Fast: daylight macro shot of a glass flask of Tetrahymena culture beside baker's yeast agar Petri dishes and a DNA sequencing autoradiogram on an oak bench. Nothing emissive, no face.",
             STYLE + "In crisp daylight on a molecular biology workbench, a glass Erlenmeyer flask of pond-ciliate culture sits beside agar Petri dishes of yeast colonies and a banded sequencing print." + FAST_TAIL,
             None),
            ("04_moscow_1971_notebook_railway_track_sketch_and_wooden_dna_primer_model_pan", 120.5, 5.5, "C", False, "1971 — MARGINOTOMY", "Fast",
             "Fast: daylight close-up pan across a Russian notebook open to an inked railway-track DNA sketch beside a wooden model of a lagging-strand primer gap. Nothing emissive, no face.",
             STYLE + "In bright window light on a wooden desk, an open notebook showing an inked sketch of a train on a DNA track sits beside a wooden block model of a chromosome end." + FAST_TAIL,
             None),
        ],
    ),
    (
        4,
        "Part 04 — Christmas Day, 25 December 1984: Carol Greider & Elizabeth Blackburn Discover Telomerase & the Double-Edged Sword of Immortality",
        [
            ("01_greider_and_blackburn_25_dec_1984_berkeley_telomerase_ladder_and_rna_template_discovery", 126.0, 6.5, "A", False, "CHRISTMAS DAY 1984: TELOMERASE", "Quality",
             "Quality: readable faces (graduate student Carol Greider and professor Elizabeth Blackburn at UC Berkeley on Christmas Day, 25 December 1984 examining the 6-base telomerase ladder film, alongside a model of telomerase's built-in RNA template stitching TTAGGG repeats onto chromosome ends).",
             STYLE + "Split period scene: on the left on 25 December 1984 at UC Berkeley, Carol Greider and Elizabeth Blackburn celebrate beside a lightbox holding a six-base repeating ladder autoradiogram; on the right, a molecular model shows the telomerase enzyme using its internal RNA template ribbon to stitch fresh six-letter blocks onto a chromosome tip." + QUAL_TAIL,
             {"kind": "FACT", "label": "Christmas Day 1984: telomerase", "when_stamp": "25 December 1984 · December 1985 · 2009", "timeline_step": "4/4 · 25 Dec 1984 (Carol Greider & Elizabeth Blackburn discover telomerase on Christmas Day at UC Berkeley; 2009 Nobel Prize with Szostak)", "hold_s": 3.8}),
            ("02_greider_blackburn_1985_1989_telomerase_rna_template_and_85_90pct_cancer_firewall_chart", 132.5, 8.0, "E", False, "25 DEC 1984 GREIDER & BLACKBURN: TELOMERASE RNA TEMPLATE (TERC + TERT) ACTIVE IN GERM/STEM CELLS, OFF IN SOMATIC (50-DIV ANTI-CANCER FIREWALL), REACTIVATED IN 85–90% OF CANCERS", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked telomerase ribonucleoprotein mechanism & aging-vs-cancer balance chart from Greider & Blackburn (December 1985, Cell 43: 405–413 & 1987/1989 Nature) and Kim et al. & Shay (23 December 1994, Science 266: 2011–2015) shows telomerase's built-in RNA template (TERC) and reverse transcriptase (TERT) adding TTAGGG repeats in germ/stem cells (and reactivated in ~85–90% of human cancers) while remaining silent in normal somatic cells to enforce the ~50-division anti-cancer Hayflick firewall.",
             {"kind": "DATA", "label": "TELOMERASE (TERT + TERC RNA TEMPLATE): ON IN STEM/GERM CELLS, OFF IN SOMATIC (ANTI-CANCER BRAKE), HACKED ON IN 85–90% OF CANCERS", "detail": "Inked telomerase ribonucleoprotein mechanism & aging-vs-cancer balance chart on period paper from Greider & Blackburn (December 1985, Cell 43: 405–413 & 1987/1989 Nature) and Kim et al. & Shay (23 December 1994, Science 266: 2011–2015) showing telomerase's built-in RNA template (TERC) and reverse transcriptase (TERT) adding TTAGGG repeats in germ/stem cells (and reactivated in ~85–90% of human cancers) while remaining silent in normal somatic cells to enforce the ~50-division anti-cancer Hayflick firewall", "scale": "telomerase is a molecular sewing machine that carries its own six-letter thread pattern inside its pocket — keeping stem cells and newborn babies young, while our normal body cells lock the machine away so rogue cells cannot divide into cancer", "hold_s": 3.8}),
            ("03_berkeley_1984_electrophoresis_rig_micropipettes_and_rna_template_model_closeup", 140.5, 6.5, "B", False, "ANTI-CANCER HAYFLICK FIREWALL", "Fast",
             "Fast: daylight macro shot of a vertical gel electrophoresis tank, micropipettes, and a wooden ribonucleoprotein model with a slotted RNA guide ribbon on a Berkeley bench. Nothing emissive, no face.",
             STYLE + "In crisp daylight on a 1984 Berkeley workbench, a vertical glass gel electrophoresis frame sits beside a rack of micropipettes and a carved wooden enzyme model holding a patterned template ribbon." + FAST_TAIL,
             None),
            ("04_explorer_locking_telomerase_sewing_machine_behind_50_division_anti_cancer_firewall_gate", 147.0, 5.5, "B", True, None, "Quality",
             "Quality: Explorer beat 2 (locked character reference).",
             STYLE + "Standing beside a brass fifty-click turnstile gate in a cellular workshop, the Explorer uses a golden sewing machine to stitch fresh end-caps onto a stem-cell cord, then locks a heavy brass padlock onto the machine when a rogue dividing cell tries to sneak past the turnstile." + EXP_TAIL,
             None),
        ],
    ),
    (
        5,
        "Part 05 — Why Turning Telomerase On Everywhere Isn't an Instant Fountain of Youth — & How Hormones Control Your Body",
        [
            ("01_timeline_1912_2009_and_aging_vs_cancer_telomere_tradeoff_chart", 152.5, 8.5, "E", False, "1912–2009 TIMELINE · CARREL CHICKEN HEART, HAYFLICK 50-DIVISION LIMIT, OLOVNIKOV/BLACKBURN/SZOSTAK TELOMERES & GREIDER/BLACKBURN TELOMERASE", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, the 4-date timeline completes: 17 Jan 1912 (Alexis Carrel starts his 34-year chicken-heart culture, launching the myth of natural cell immortality) · Dec 1961 (Leonard Hayflick & Paul Moorhead prove normal human fibroblasts stop dividing after ~50 doublings, the Hayflick Limit) · 1971 & Mar 1978–1982 (Alexey Olovnikov predicts the DNA end-replication problem; Elizabeth Blackburn & Jack Szostak sequence TTGGGG telomere repeats and prove cross-species protection in yeast) · 25 Dec 1984 (Carol Greider & Elizabeth Blackburn discover telomerase on Christmas Day at UC Berkeley; 2009 Nobel Prize with Szostak).",
             {"kind": "DATA", "label": "1912–2009 TELOMERE & AGING TIMELINE · 50-DIVISION HAYFLICK LIMIT, TTAGGG CAPS & TELOMERASE BALANCE", "detail": "Animated 4-date timeline (1912 → 2009) alongside the telomere attrition vs cancer firewall trade-off diagram", "scale": "from a thirty-four-year chicken-heart myth in New York to an X-ray film developed on Christmas night in California, scientists discovered that the tips of your chromosomes count every single division of your life", "when_stamp": "1912–2009", "timeline_step": "4/4 · 1912–2009 timeline complete", "hold_s": 3.8}),
            ("02_shoelace_aglets_chromosome_cap_model_and_50_division_hourglass_on_plinth_pan", 161.0, 5.5, "A", False, "50-DIVISION TUMOUR SHIELD", "Fast",
             "Fast: daylight close-up of a wooden chromosome model with brass shoelace-cap tips beside a sand hourglass and a framed gel ladder print on a museum plinth. Nothing emissive, no face.",
             STYLE + "In crisp daylight on a wooden museum plinth, a carved chromosome model with polished brass end-caps sits beside a glass sand hourglass and a framed six-step gel print." + FAST_TAIL,
             None),
            ("03_oliver_schafer_1894_adrenaline_and_bayliss_starling_16_jan_1902_secretin_hormones_handoff", 166.5, 6.5, "C", False, "16 JANUARY 1902 — HORMONES", "Quality",
             "Quality: readable faces (George Oliver and Edward Schäfer in March 1894 testing adrenal extract on blood pressure, alongside William Bayliss and Ernest Starling at University College London on 16 January 1902 discovering secretin and coining the word 'hormone' — handoff to 060 Hormones & Endocrinology).",
             STYLE + "Split period scene: on the left in March 1894 London, George Oliver and Edward Schäfer watch a mercury kymograph drum rise as adrenal extract enters the bloodstream; on the right on 16 January 1902 at University College London, William Bayliss and Ernest Starling observe pancreatic drops flowing in response to blood-borne secretin." + QUAL_TAIL,
             {"kind": "WHEN", "label": "MARCH 1894 · 16 JANUARY 1902", "hold_s": 3.5}),
            ("04_table_three_callback", 173.0, 2.4, "C", False, None, "reuse",
             "Reuse: verified unused moving window [5.50s..7.90s] of P1:07_table_three_props_carrel_1912_flask_hayflick_1961_culture_bottle_and_greider_1984_gel_plate (callback, £0).",
             "Reuse P1:07_table_three_props_carrel_1912_flask_hayflick_1961_culture_bottle_and_greider_1984_gel_plate [5.50s..7.90s] (2.40s distinct non-overlapping tail window from 8.00s source clip).",
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
                row["reuse_of"] = "P1:07_table_three_props_carrel_1912_flask_hayflick_1961_culture_bottle_and_greider_1984_gel_plate"
                row["reuse_window_s"] = [5.5, 7.9]
                row["reuse_audit"] = {
                    "source_row": "P1:07_table_three_props_carrel_1912_flask_hayflick_1961_culture_bottle_and_greider_1984_gel_plate",
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
            "film": "059_Carrel-Hayflick-Blackburn-Greider-Telomeres-Aging",
            "part": p_idx,
            "title": p_title,
            "version": "v01",
            "timing_status": "pre_vo_script_clock (built from telomeres_script_master_v01.md; retimes onto Scribe STT once VO locks)",
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
        "film": "059_Carrel-Hayflick-Blackburn-Greider-Telomeres-Aging",
        "version": "v01",
        "date": "2026-10-19",
        "owner": "gemini (J0631)",
        "status": "PRE_VO_BOARDS_V01_NO_MINT",
        "generation_authorized": False,
        "script": "00_Brand/Channel-Setup/ideas/059_Carrel-Hayflick-Blackburn-Greider-Telomeres-Aging/telomeres_script_master_v01.md",
        "sources": "00_Brand/Channel-Setup/ideas/059_Carrel-Hayflick-Blackburn-Greider-Telomeres-Aging/SOURCES_v01.md",
        "credit_snapshot": {
            "flow_balance": 23740,
            "flow_floor": 0,
            "flow_read_at": "2026-10-15T21:42:22Z",
            "vertex_promo_gbp": 71.02,
            "vertex_usable_gbp": 70.02,
        },
        "totals": totals,
        "per_part": per_part_summary,
        "mint_order": "006 > 007 > 008 > 009 > 010 > 011 > 012 > 013 > 014 > 015 > 016 > 017 > 018 > 019 > 020 > 021 > 022 > 023 > 024 > 025 > 026 > 027 > 028 > 029 > 030 > 031 > 032 > 033 > 034 > 035 > 036 > 037 > 038 > 039 > 040 > 041 > 042 > 043 > 044 > 045 > 046 > 047 > 048 > 049 > 050 > 051 > 052 > 053 > 054 > 055 > 056 > 057 > 058 > 059 > 060 > 061 > 062. Nothing in 059 is generation_authorized.",
    }
    (EDIT / "PICTURE_PLAN_v01.json").write_text(json.dumps(plan, indent=2) + "\n")

    sl = [
        "# 059 Telomeres: The Countdown Clock Inside Your Cells — Shot list & plate boards v01 (pre-VO)",
        "",
        "Gemini, 19 Oct 2026, J0631. Built from `telomeres_script_master_v01.md` (`92.4 PASS`) and `SOURCES_v01.md`.",
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
        "# 059 price review v01 (pre-VO plate boards)",
        "",
        "Gemini, 19 Oct 2026, J0631. Boards only. **No mint. No spend. No merge.**",
        "Prepared from `telomeres_script_master_v01.md` (`92.4 PASS`) and `SOURCES_v01.md` so 059's full plate board rows, non-emissive Fast prompts, £0 code graphics, and Teach-on-Screen overlays are ready to re-time the moment long VO locks. Parked for Chief.",
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
        f"- **Quality ({totals['Quality']} rows):** readable faces (Alexis Carrel, Leonard Hayflick, Paul S. Moorhead, Hermann J. Muller, Barbara McClintock, Alexey M. Olovnikov, Elizabeth H. Blackburn, Jack W. Szostak, Carol W. Greider, George Oliver, Edward Schäfer, William Bayliss, Ernest Starling), 17 January 1912 Rockefeller chicken-heart culture & December 1961 Wistar 50-division Hayflick Limit, 1971 Moscow subway end-replication insight & 1978–1982 *Tetrahymena*/yeast telomere conservation, Christmas Day 25 December 1984 UC Berkeley telomerase discovery, and the 2 Explorer beats.",
        f"- **Fast ({totals['Fast']} rows, non-emissive):** daylight prop and laboratory shots (brass shoelace aglets, Carrel glass flask, chromosome model & 50-click tally counter pan, 3-object callback bench, 1961 square glass culture bottles, cryo-canister & karyotype print, 1912 Carrel D-flask & hand-centrifuge, 1978 *Tetrahymena* Erlenmeyer flask & yeast agar plates, 1971 Russian notebook railway-track DNA sketch & wooden primer-gap model, 1984 Berkeley vertical gel electrophoresis rig & RNA-template wooden model, chromosome model with brass shoelace-cap tips & sand hourglass on museum plinth). Zero candles, flames, sparks, or glowing elements on Fast.",
        f"- **£0 code graphics ({totals['code_graphic']} rows):**",
        "  1. `P1:04_hayflick_1961_and_blackburn_greider_1984_telomere_15kb_to_4kb_50_divisions_chart` — human telomere attrition & Hayflick limit chart showing ~10,000–15,000 bp of TTAGGG repeats at birth losing ~50–200 bp/division across ~50 doublings down to ~4,000 bp vs telomerase extension (`SCALE: each of your forty-six chromosomes starts life with a protective DNA fuse about ten thousand letters long — and every time a cell divides, up to two hundred letters burn off the tip until after fifty divisions the fuse runs out`)",
        "  2. `P1:06_olovnikov_1971_watson_1972_lagging_strand_end_replication_subway_track_chart` — Olovnikov (1971) & Watson (1972) end-replication problem diagram comparing leading-strand continuous synthesis against lagging-strand terminal RNA primer gap (`SCALE: the enzyme that copies your DNA is like a painter backing down a wooden hallway who can paint every floorboard except the final board he is standing on — so every copy of the hallway comes out one board shorter`)",
        "  3. `P2:02_hayflick_moorhead_dec_1961_phase_i_ii_iii_50_doublings_and_male_female_mix_chart` — Hayflick & Moorhead (December 1961, *Exp. Cell Res.*) Phase I/II/III ~50 ± 10 population doubling curve, 40-doubling male + 10-doubling female mixed-dish proof, and liquid-nitrogen memory (`SCALE: even if you freeze a human cell in liquid nitrogen at minus one hundred and ninety-six degrees for ten years after twenty divisions, the moment you thaw it out it remembers its exact count and divides only thirty more times`)",
        "  4. `P3:02_olovnikov_1971_blackburn_gall_1978_szostak_1982_tetrahymena_ttgggg_yeast_human_ttaggg_chart` — Blackburn & Gall (March 1978), Szostak & Blackburn (May 1982), and Moyzis et al. (1988) *Tetrahymena* `TTGGGG` to yeast and human `TTAGGG` telomere conservation chart (`SCALE: the six-letter shoelace cap at the tip of your DNA is so ancient that when Blackburn and Szostak stitched telomeres from pond scum onto chromosomes inside baker's yeast, the yeast recognised the code across a billion years of evolution`)",
        "  5. `P4:02_greider_blackburn_1985_1989_telomerase_rna_template_and_85_90pct_cancer_firewall_chart` — Greider & Blackburn (Dec 1985 *Cell* & 1989 *Nature*) and Kim, Shay & Wright (23 Dec 1994 *Science*) telomerase RNA-template (`TERC + TERT`) mechanism and ~50-division anti-cancer firewall (~85–90% cancer reactivation) (`SCALE: telomerase is a molecular sewing machine that carries its own six-letter thread pattern inside its pocket — keeping stem cells and newborn babies young, while our normal body cells lock the machine away so rogue cells cannot divide into cancer`)",
        "  6. `P5:01_timeline_1912_2009_and_aging_vs_cancer_telomere_tradeoff_chart` — completed 4-date timeline (1912 → 2009) + telomere attrition vs anti-cancer firewall trade-off diagram (`SCALE: from a thirty-four-year chicken-heart myth in New York to an X-ray film developed on Christmas night in California, scientists discovered that the tips of your chromosomes count every single division of your life`)",
        f"- **£0 verified reuse ({totals['reuse']} row):** `P5:04_table_three_callback` uses the 2.40 s unused moving tail `[5.50s..7.90s]` of `P1:07_table_three_props_carrel_1912_flask_hayflick_1961_culture_bottle_and_greider_1984_gel_plate`.",
        "",
        "## Mint order",
        "",
        "006 > 007 > 008 > 009 > 010 > 011 > 012 > 013 > 014 > 015 > 016 > 017 > 018 > 019 > 020 > 021 > 022 > 023 > 024 > 025 > 026 > 027 > 028 > 029 > 030 > 031 > 032 > 033 > 034 > 035 > 036 > 037 > 038 > 039 > 040 > 041 > 042 > 043 > 044 > 045 > 046 > 047 > 048 > 049 > 050 > 051 > 052 > 053 > 054 > 055 > 056 > 057 > 058 > 059 > 060 > 061 > 062. `generation_authorized` is `false` on every row.",
    ])
    (EDIT / "PRICE_REVIEW_v01.md").write_text("\n".join(pr_lines) + "\n")
    print(f"059 v01 boards written: {totals['rows']} rows, Flow expected={totals['flow_credits_expected']}")


if __name__ == "__main__":
    main()
