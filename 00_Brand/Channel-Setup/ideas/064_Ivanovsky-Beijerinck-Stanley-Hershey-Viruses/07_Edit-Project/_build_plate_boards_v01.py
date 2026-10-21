#!/usr/bin/env python3
"""HOS 064 (Viruses: The Living Crystals That Hijack Your Cells) pre-VO plate boards v01. J0646. No mint, no spend.

Built from 00_Brand/Channel-Setup/ideas/064_Ivanovsky-Beijerinck-Stanley-Hershey-Viruses/viruses_script_master_v01.md
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
        "Part 01 — The Salt Crystal in a Jar & the Radioactive Kitchen Blender",
        [
            ("01_tmv_needle_crystals_jar_to_tobacco_leaf_and_t2_bacteriophage_syringes_with_blender", 0.0, 5.5, "A", False, "LIVING CRYSTALS & VIRAL SYRINGES", "Quality",
             "Quality: Short frame 0 / answer image (0:03) + a glass jar of sparkling white needle crystals of Tobacco Mosaic Virus dissolves into a drop of water on a green leaf, zooming in 100,000 times to show lunar-lander bacteriophages landing on a bacterium and injecting DNA strands like microscopic syringes while a silver Waring blender spins in the laboratory behind them.",
             STYLE + "Split laboratory-and-microscopic scene: on the left, a glass jar of white needle crystals dissolves into a water droplet on a green tobacco leaf; on the right, lunar-lander bacteriophages land on a rod-shaped bacterium and inject golden DNA filaments like hypodermic syringes while a silver Waring blender whirls in the background." + QUAL_TAIL,
             {"kind": "WHEN", "label": "ST. PETERSBURG, 12 FEBRUARY 1892", "timeline_step": "1/4 · 12 Feb 1892 & 1898 (Dmitri Ivanovsky shows tobacco mosaic sap stays infectious through a bacteria-blocking Chamberland porcelain filter; Martinus Beijerinck names it a 'virus')", "hold_s": 3.5}),
            ("02_ivanovsky_1892_beijerinck_1898_filter_stanley_1935_crystals_and_hershey_chase_1952_blender_split", 5.5, 6.0, "B", False, "PORCELAIN FILTER, VIRUS CRYSTALS, BLENDER PROOF", "Quality",
             "Quality: complex three-part composition (Dmitri Ivanovsky in St. Petersburg on 12 February 1892 and Martinus Beijerinck in Delft in 1898 pressing mottled tobacco sap through a Chamberland porcelain filter; Wendell Stanley at the Rockefeller Institute in Princeton on 28 June 1935 holding up a vial of sparkling crystalline Tobacco Mosaic Virus needles; and Alfred Hershey with Martha Chase at Cold Spring Harbor in September 1952 running a Waring blender with radioactive T2 bacteriophages).",
             STYLE + "Three-panel period composition: on the left, Dmitri Ivanovsky and Martinus Beijerinck filtering green tobacco sap through an unglazed white porcelain candle; in the centre, Wendell Stanley in 1935 Princeton holding up a flask of white crystalline virus needles; on the right, Alfred Hershey and Martha Chase in 1952 Cold Spring Harbor operating a silver Waring kitchen blender." + QUAL_TAIL,
             None),
            ("03_two_thousand_nm_ecoli_bacterium_beside_300nm_tmv_rod_and_200nm_t2_bacteriophage_scale", 11.5, 6.0, "C", False, "NOT ALIVE, YET IT MULTIPLIES", "Quality",
             "Quality: complex conceptual and physical scale comparison (a 2,000-nanometre E. coli bacterium humming with ribosomes and ATP batteries towers beside a 300-nanometre Tobacco Mosaic Virus rod and a 200-nanometre T2 bacteriophage that sits completely inert like a mineral crystal until it touches the cell wall).",
             STYLE + "Split scale scene: on the left, a giant two-thousand-nanometre E. coli bacterium hums with internal ribosomes and golden ATP gears; on the right, a crystalline three-hundred-nanometre Tobacco Mosaic Virus rod and a geometric lunar-lander bacteriophage sit motionless until touching the bacterial surface." + QUAL_TAIL,
             {"kind": "WHEN", "label": "12 FEBRUARY 1892 · 1898 · 28 JUNE 1935 · 19 DECEMBER 1936 · 20 SEPTEMBER 1952", "timeline_step": "1/4 · 1892 & 1898 (Ivanovsky & Beijerinck) · 2/4 · 1915–1917 (Twort & d'Hérelle) · 3/4 · 1935–1936 (Stanley; Bawden & Pirie) · 4/4 · 20 Sep 1952 (Hershey & Chase)", "hold_s": 3.5}),
            ("04_ivanovsky_1892_beijerinck_1898_stanley_1935_hershey_chase_1952_size_and_blender_chart", 17.5, 8.0, "E", False, "1892–1898 FILTERABLE VIRUS (30–300 NM VS 2,000-NM BACTERIUM) · 1935–1936 TMV CRYSTALS (95% PROTEIN : 5% RNA) · 1952 HERSHEY-CHASE BLENDER (32P DNA IN, 80% 35S PROTEIN OUT)", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked size-scale & Hershey-Chase radioactive blender chart from Ivanovsky (12 February 1892 Bull. Acad. Imp. Sci. St.-Pétersbourg 35: 67–70), Beijerinck (1898 Verh. K. Akad. Wet. Amsterdam 65: 3–21), Stanley (28 June 1935 Science 81: 644–645), Bawden & Pirie (19 December 1936 Nature 138: 1051–1052), and Hershey & Chase (20 September 1952 J. Gen. Physiol. 36: 39–56) compares a human red blood cell (~8,000 nm), an E. coli bacterium (~2,000 nm), a Chamberland filter pore (~100–200 nm), a Tobacco Mosaic Virus rod (300 x 18 nm, 95% protein + 5% RNA), and a polio/rhinovirus (~30 nm), alongside Hershey & Chase's Waring blender separation showing 80% of 35S-labelled viral protein coats sheared off in the supernatant while 32P-labelled viral DNA enters the bacterial pellet.",
             {"kind": "DATA", "label": "E. COLI (2,000 NM) VS CHAMBERLAND PORE (100–200 NM) VS TMV (300×18 NM) & RHINOVIRUS (30 NM) · HERSHEY-CHASE 32P DNA INJECTION", "detail": "Inked microbial filtration & Hershey-Chase blender chart on period paper comparing human red blood cell (8,000 nm), E. coli bacterium (2,000 nm), Chamberland porcelain filter pore (100–200 nm), TMV rod (300 × 18 nm, 95% protein : 5% RNA), and rhinovirus (30 nm), plus Hershey-Chase 35S protein (80% extracellular) vs 32P DNA (intracellular injection)", "scale": "if a single E. coli bacterium were the size of a double-decker bus, a cold virus beside it would be no bigger than a football — easily slipping straight through a bacterium-proof porcelain filter", "who_card": "Dmitri Ivanovsky (1864–1920) — Russian botanist · Martinus Beijerinck (1851–1931) — Dutch microbiologist · Wendell M. Stanley (1904–1971) — American biochemist · Frederick C. Bawden (1908–1972) — British plant pathologist · Norman W. Pirie (1907–1997) — British biochemist · Alfred D. Hershey (1908–1997) — American geneticist · Martha Chase (1927–2003) — American geneticist", "when_stamp": "12 February 1892 · 1898 · 28 June 1935 · 19 December 1936 · 20 September 1952", "hold_s": 3.8}),
            ("05_chamberland_porcelain_filter_candle_mottled_tobacco_leaf_and_crystal_vial_pan", 25.5, 5.5, "A", False, "BUS VS FOOTBALL", "Fast",
             "Fast: daylight macro pan across an unglazed white Chamberland porcelain filter candle, a mottled green tobacco leaf, and a stoppered glass vial of white crystals on an oak bench between code graphics so two full-frame graphics never run back to back. Nothing emissive, no face.",
             STYLE + "In crisp daylight on an oak botany bench, the camera pans smoothly across an unglazed white porcelain Chamberland filter candle, a mosaic-spotted green tobacco leaf, and a stoppered glass vial of white needle crystals." + FAST_TAIL,
             None),
            ("06_stanley_1935_bawden_pirie_1936_franklin_1955_tmv_2130_subunits_6395nt_rna_helix_chart", 31.0, 8.0, "E", False, "2,130 PROTEIN BRICKS AROUND ONE RNA STRAND", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period parchment, an inked TMV helical nucleoprotein assembly diagram (from Stanley 1935, Bawden & Pirie 1936, Helmut Ruska 1939 electron micrographs, & Rosalind Franklin 1955–1956 X-ray diffraction) shows 2,130 identical protein subunits stacking in a hollow 300-nanometre spiral tube around a single 6,400-letter strand of RNA.",
             {"kind": "DATA", "label": "TMV HELICAL ARCHITECTURE (300 × 18 NM): 2,130 IDENTICAL PROTEIN SUBUNITS (95%) WRAPPED AROUND 1 STRAND OF 6,395-NT RNA (5%)", "detail": "Inked Tobacco Mosaic Virus (TMV) architecture diagram showing a 300 nm × 18 nm hollow helical rod built from 2,130 identical coat-protein subunits (95% by mass) wrapped around a single 6,395-nucleotide strand of RNA (5% by mass)", "scale": "a tobacco mosaic virus is just one strand of genetic instructions wrapped in 2,130 identical protein bricks — so uniform that billions of them stack together in a jar like salt crystals", "hold_s": 3.8}),
            ("07_table_three_props_1892_porcelain_filter_1935_tmv_crystal_vial_and_1952_waring_blender", 39.0, 5.5, "C", False, "1892 TO 1952", "Fast",
             "Fast: daylight prop table (callback source for Part 05: Dmitri Ivanovsky's 1892 Chamberland porcelain filter candle, Wendell Stanley's 1935 glass vial of TMV crystals, and Alfred Hershey & Martha Chase's 1952 chrome Waring blender). Nothing emissive.",
             STYLE + "On an oak workbench in soft window light sit three objects side by side: a white porcelain Chamberland filter candle in a glass flask, a stoppered vial of white virus crystals, and a vintage chrome Waring kitchen blender." + FAST_TAIL,
             None),
            ("08_explorer_watching_bacteriophage_inject_dna_while_waring_blender_shears_protein_coat", 62.0, 5.5, "A", True, None, "Quality",
             "Quality: Explorer beat 1 (locked character reference, after 1:00).",
             STYLE + "Standing beside a vintage chrome Waring kitchen blender at Cold Spring Harbor, the Explorer watches a lunar-lander bacteriophage inject a blue DNA coil into a rod-shaped bacterium while spinning blades shear the empty red protein shell off the outside." + EXP_TAIL,
             None),
            ("09_wendell_stanley_28_june_1935_princeton_holding_flask_of_crystalline_tmv_needles", 67.5, 5.5, "B", False, "PRINCETON, 28 JUNE 1935", "Quality",
             "Quality: readable face (in Princeton on 28 June 1935, Wendell Stanley holds a glass flask of silky white crystalline needles harvested from a ton of crushed tobacco leaves).",
             STYLE + "In a 1935 Princeton chemistry laboratory, American biochemist Wendell Stanley holds a glass Erlenmeyer flask up to the window light, admiring a swirling suspension of silky white Tobacco Mosaic Virus needle crystals beside crates of tobacco leaves." + QUAL_TAIL,
             {"kind": "WHEN", "label": "PRINCETON, 28 JUNE 1935", "timeline_step": "3/4 · 28 Jun 1935 & Dec 1936 (Wendell Stanley crystallises Tobacco Mosaic Virus like salt; Bawden & Pirie prove it is 95% protein and 5% RNA)", "hold_s": 3.5}),
        ],
    ),
    (
        2,
        "Part 02 — 12 February 1892 & 1898: The Porcelain Filter & Martinus Beijerinck's 'Contagious Living Fluid' (Virus)",
        [
            ("01_ivanovsky_12_feb_1892_st_petersburg_beijerinck_1898_delft_and_dherelle_1917_bacteriophages", 73.0, 6.5, "A", False, "MULTIPLIED AFTER PASSING THROUGH PORCELAIN", "Quality",
             "Quality: readable faces (Russian botanist Dmitri Ivanovsky on 12 February 1892 pouring mottled tobacco sap through a Chamberland porcelain filter candle, dissolving to Dutch microbiologist Martinus Beijerinck in 1898 proving serial replication in living leaves and coining 'contagium vivum fluidum' ('virus'), and Félix d'Hérelle in September 1917 discovering bacteria-eating bacteriophages).",
             STYLE + "Split period scene: on the left in 1892 St. Petersburg, Dmitri Ivanovsky pours crushed tobacco sap through a white porcelain Chamberland filter candle; on the right in 1898 Delft, Martinus Beijerinck inoculates healthy green tobacco leaves with clear filtrate while Félix d'Hérelle holds up a bacterial culture cleared by bacteriophages." + QUAL_TAIL,
             {"kind": "FACT", "label": "Multiplied after passing through porcelain", "who_card": "Félix d'Hérelle (1873–1949) — French-Canadian microbiologist", "when_stamp": "1884 · 12 February 1892 · 1898 · 4 December 1915 · 3 September 1917", "timeline_step": "1/4 · 12 Feb 1892 & 1898 (Ivanovsky & Beijerinck discover filterable viruses) & 2/4 · 1915–1917 (Twort & d'Hérelle discover bacteriophages)", "hold_s": 3.8}),
            ("02_ivanovsky_1892_beijerinck_1898_porcelain_filtration_and_serial_replication_chart", 79.5, 8.0, "E", False, "12 FEB 1892 IVANOVSKY & 1898 BEIJERINCK: PORCELAIN-FILTERED 'CONTAGIUM VIVUM FLUIDUM' (VIRUS) AMPLIFIES ACROSS SERIAL LEAF PASSAGES VS DILUTING TOXIN", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked Ivanovsky (1892) & Beijerinck (1898) serial-dilution vs chemical toxin chart shows a chemical toxin's potency dropping to zero across 10-fold serial dilutions while Beijerinck's porcelain-filtered Tobacco Mosaic Virus ('contagium vivum fluidum') amplifies exponentially back to 100% infectious titre inside each living host leaf.",
             {"kind": "DATA", "label": "1892 IVANOVSKY & 1898 BEIJERINCK: CHEMICAL TOXIN DILUTES TO 0% VS FILTERED VIRUS AMPLIFYING TO 100% IN LIVING CELLS", "detail": "Inked Ivanovsky (1892) & Beijerinck (1898) serial-dilution vs chemical toxin chart on period paper showing a chemical toxin's potency dropping to zero across 10-fold serial dilutions while Beijerinck's porcelain-filtered Tobacco Mosaic Virus ('contagium vivum fluidum') amplifies exponentially back to 100% infectious titre inside each living host leaf", "scale": "if you drop a pinch of poison into a lake, it dilutes until it is harmless — yet one microscopic drop of Beijerinck's filtered liquid turned an entire field of healthy plants into factories making millions of new copies", "hold_s": 3.8}),
            ("03_delft_1898_porcelain_filter_apparatus_agar_diffusion_plate_and_tobacco_leaves_closeup", 87.5, 6.5, "B", False, "1898 — CONTAGIOUS LIVING FLUID ('VIRUS')", "Fast",
             "Fast: daylight macro shot of a glass vacuum filtration flask holding a white Chamberland porcelain candle beside potted tobacco plants with mosaic-mottled leaves on a 1898 Delft bench. Nothing emissive, no face.",
             STYLE + "In crisp daylight on an 1898 Dutch laboratory bench, a vacuum filtration flask fitted with a white unglazed porcelain filter candle sits beside glass Petri dishes and potted green tobacco plants." + FAST_TAIL,
             None),
            ("04_mortar_and_pestle_crushing_tobacco_leaves_and_glass_dropper_bottles_pan", 94.0, 5.5, "C", False, "12 FEBRUARY 1892 — FILTERABLE GERMS", "Fast",
             "Fast: daylight close-up pan across a ceramic mortar and pestle holding crushed tobacco leaves beside a row of numbered serial-passage glass dropper bottles on an oak table. Nothing emissive, no face.",
             STYLE + "In bright window light on an oak bench, a white ceramic mortar and pestle with crushed green leaves sits beside a neat row of stoppered glass dropper bottles." + FAST_TAIL,
             None),
        ],
    ),
    (
        3,
        "Part 03 — 28 June 1935: Wendell Stanley Crystallises a Virus Like Table Salt & the Electron Microscope Sees It — Midpoint Twist",
        [
            ("01_wendell_stanley_28_june_1935_tmv_crystals_bawden_pirie_1936_rna_and_ruska_1939_em", 99.5, 6.5, "A", False, "CRYSTALLISED IN A JAR LIKE SALT", "Quality",
             "Quality: readable faces (American biochemist Wendell Stanley on 28 June 1935 isolating silky white needle crystals of pure Tobacco Mosaic Virus, dissolving to Frederick Bawden and Norman Pirie on 19 December 1936 proving the crystals are 95% protein and 5% RNA, and Helmut Ruska in May 1939 taking the first electron-microscope photographs of 300-nm TMV rods).",
             STYLE + "Split period scene: on the left in June 1935 Princeton, Wendell Stanley examines sparkling needle crystals of Tobacco Mosaic Virus while Frederick Bawden and Norman Pirie test the 5% RNA core; on the right in May 1939 Berlin, Helmut Ruska sits at an early electron microscope column displaying 300-nanometre virus rods." + QUAL_TAIL,
             {"kind": "FACT", "label": "Crystallised in a jar like salt", "who_card": "Helmut Ruska (1908–1973) — German physician and virologist", "when_stamp": "28 June 1935 · 19 December 1936 · 1938 · 1939", "timeline_step": "3/4 · 28 Jun 1935, Dec 1936 & May 1939 (Stanley crystallises TMV; Bawden & Pirie find 95% protein + 5% RNA; Helmut Ruska photographs viruses with the electron microscope)", "hold_s": 3.8}),
            ("02_stanley_1935_bawden_pirie_1936_ruska_1939_tmv_composition_and_em_resolution_chart", 106.0, 8.0, "E", False, "28 JUNE 1935 STANLEY (SCIENCE, 10^-9 G/ML INFECTIOUS CRYSTALS) · 19 DEC 1936 BAWDEN & PIRIE (95% PROTEIN + 5% RNA) · MAY 1939 RUSKA 300×18-NM EM", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked Stanley (28 June 1935, Science 81: 644–645), Bawden & Pirie (19 December 1936, Nature 138: 1051–1052), and Ruska & Kausche (May 1939, Naturwissenschaften 27: 292–299) TMV composition & electron-microscope resolution chart shows visible-light microscopy limit (~200 nm) vs electron-microscope imaging of 300 x 18 nm TMV rods (95% protein coat + 5% RNA core, infectious at 10^-9 g/mL).",
             {"kind": "DATA", "label": "1935 STANLEY TMV CRYSTALS (10^-9 G/ML) · 1936 BAWDEN & PIRIE (95% PROTEIN + 5% RNA) · 1939 RUSKA EM (300 × 18 NM VS 200-NM LIGHT LIMIT)", "detail": "Inked Stanley (28 June 1935, Science 81: 644–645), Bawden & Pirie (19 December 1936, Nature 138: 1051–1052), and Ruska & Kausche (May 1939, Naturwissenschaften 27: 292–299) TMV composition & electron-microscope resolution chart on period paper showing visible-light microscopy limit (~200 nm) vs electron-microscope imaging of 300 × 18 nm TMV rods (95% protein coat + 5% RNA core, infectious at 10^-9 g/mL)", "scale": "a tobacco mosaic virus is ten times smaller than the wavelength of green light, making it physically invisible to any optical microscope on Earth until Helmut Ruska used a beam of electrons to photograph it in 1939", "hold_s": 3.8}),
            ("03_princeton_1935_tmv_crystal_vial_and_1939_berlin_electron_micrograph_plate_closeup", 114.0, 6.5, "B", False, "28 JUNE 1935 — THE LIVING CRYSTAL", "Fast",
             "Fast: daylight macro shot of a glass vial of white crystalline TMV needles beside a 1939 glass electron-microscope photographic plate showing 300-nanometre virus rods on a bench. Nothing emissive, no face.",
             STYLE + "In crisp daylight on a 1939 laboratory bench, a stoppered glass vial of white needle crystals sits beside a monochrome photographic plate showing sharp rod-shaped virus particles." + FAST_TAIL,
             None),
            ("04_helical_wooden_2130_brick_capsid_and_coiled_rna_thread_model_pan", 120.5, 5.5, "C", False, "95% PROTEIN · 5% RNA", "Fast",
             "Fast: daylight close-up pan across a sculpted architectural model of a hollow spiral cylinder of protein bricks enclosing a single red RNA thread on an oak table. Nothing emissive, no face.",
             STYLE + "In bright window light on an oak table, a sculpted cylindrical model of interlocking spiral blocks reveals a single red helical thread winding up its hollow core." + FAST_TAIL,
             None),
        ],
    ),
    (
        4,
        "Part 04 — 20 September 1952: Alfred Hershey, Martha Chase & the Radioactive Waring Blender Experiment",
        [
            ("01_alfred_hershey_and_martha_chase_20_sep_1952_cold_spring_harbor_waring_blender", 126.0, 6.5, "A", False, "PROTEIN STAYS OUTSIDE; DNA GOES IN", "Quality",
             "Quality: readable faces (geneticist Alfred Hershey and 24-year-old researcher Martha Chase at Cold Spring Harbor on 20 September 1952 labelling T2 bacteriophages with 35S and 32P and shearing empty protein coats off infected E. coli bacteria in a Waring kitchen blender).",
             STYLE + "Split period scene: on the left at Cold Spring Harbor in September 1952, Alfred Hershey and young Martha Chase pour a bacteriophage culture into a chrome Waring kitchen blender beside a centrifuge; on the right, T2 phages inject their 32P DNA into E. coli while empty 35S protein shells are spun off into the liquid." + QUAL_TAIL,
             {"kind": "FACT", "label": "Protein stays outside; DNA goes in", "when_stamp": "20 September 1952", "timeline_step": "4/4 · 20 Sep 1952 (Alfred Hershey & Martha Chase use 35S/32P radioactive phages and a Waring blender to prove viruses inject pure DNA to hijack cells)", "hold_s": 3.8}),
            ("02_hershey_chase_20_sep_1952_j_gen_physiol_35s_protein_vs_32p_dna_blender_chart", 132.5, 8.0, "E", False, "20 SEP 1952 HERSHEY & CHASE (J. GEN. PHYSIOL. 36: 39–56): 80% OF 35S VIRAL PROTEIN SHEARED OFF OUTSIDE VS 32P VIRAL DNA INJECTED INSIDE PELLET", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked Hershey & Chase Waring blender experiment chart (from Hershey & Chase, 20 September 1952, J. Gen. Physiol. 36: 39–56) plots blender agitation time (0 to 8 minutes) vs extracellular 35S protein coat sheared into the supernatant (~80%) while ~70–85% of 32P viral DNA remains inside the infected E. coli pellet to direct progeny phage assembly.",
             {"kind": "DATA", "label": "20 SEP 1952 HERSHEY-CHASE BLENDER: 80% 35S PROTEIN SHELLS OUTSIDE IN SUPERNATANT VS 32P DNA INSIDE BACTERIAL PELLET", "detail": "Inked Hershey & Chase Waring blender experiment chart on period paper (from Hershey & Chase, 20 September 1952, J. Gen. Physiol. 36: 39–56) plotting blender agitation time (0 to 8 minutes) vs extracellular 35S protein coat sheared into the supernatant (~80%) while ~70–85% of 32P viral DNA remains inside the infected E. coli pellet to direct progeny phage assembly", "scale": "the Hershey-Chase blender experiment proved that a virus protein coat is nothing more than a disposable delivery van — it parks on the outside of your cell wall, injects its DNA or RNA instructions inside, and gets left behind", "hold_s": 3.8}),
            ("03_cold_spring_harbor_1952_waring_blender_centrifuge_tubes_and_geiger_counter_closeup", 140.5, 6.5, "B", False, "20 SEPTEMBER 1952 — DNA IS THE VIRAL PAYLOAD", "Fast",
             "Fast: daylight macro shot of a vintage chrome Waring blender beside two glass centrifuge tubes (marked supernatant and bacterial pellet) and an analog Geiger counter dial on a 1952 workbench. Nothing emissive, no face.",
             STYLE + "In crisp daylight on a 1952 genetics workbench, a chrome Waring kitchen blender sits beside a rack of glass centrifuge tubes and an analog Geiger-counter meter." + FAST_TAIL,
             None),
            ("04_explorer_checking_supernatant_and_bacterial_pellet_with_geiger_counter_probe", 147.0, 5.5, "B", True, None, "Quality",
             "Quality: Explorer beat 2 (locked character reference).",
             STYLE + "Standing beside a large glass centrifuge tube after spinning, the Explorer holds a brass Geiger probe against the clear upper liquid of empty red phage shells and then lowers it to the bottom bacterial pellet where blue DNA coils move the needle." + EXP_TAIL,
             None),
        ],
    ),
    (
        5,
        "Part 05 — Why Antibiotics Never Cure a Viral Cold — & How Your Immune System Recognises a Billion New Invaders",
        [
            ("01_timeline_1892_1952_and_antibiotic_cell_wall_target_vs_intracellular_virus_chart", 152.5, 8.5, "E", False, "1892–1952 TIMELINE · IVANOVSKY/BEIJERINCK FILTER, TWORT/D'HÉRELLE PHAGES, STANLEY TMV CRYSTALS, HERSHEY-CHASE BLENDER & WHY ANTIBIOTICS FAIL", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, the 4-date timeline completes: 12 Feb 1892 & 1898 (Dmitri Ivanovsky shows tobacco mosaic sap stays infectious through a bacteria-blocking Chamberland porcelain filter; Martinus Beijerinck proves replication in living tissue and names it a 'virus') · 1915–1917 (Frederick Twort & Félix d'Hérelle discover bacteria-eating viruses, bacteriophages) · 28 June 1935 & Dec 1936 (Wendell Stanley crystallises Tobacco Mosaic Virus like salt; Bawden & Pirie prove it is 95% protein and 5% RNA; Helmut Ruska photographs viruses in 1938–1939) · 20 Sep 1952 (Alfred Hershey & Martha Chase use 35S/32P radioactive phages and a Waring blender to prove viruses inject pure DNA to hijack cells).",
             {"kind": "DATA", "label": "1892–1952 VIRUS DISCOVERY TIMELINE · BACTERIAL CELL WALLS/RIBOSOMES (ANTIBIOTIC TARGETS) VS INTRACELLULAR VIRUSES", "detail": "Animated 4-date timeline (1892 → 1952) alongside the bacterial antibiotic target vs intracellular viral replication diagram", "scale": "from crushed tobacco leaves in Russia to sparkling crystals in New Jersey and a kitchen blender in New York, sixty years of detective work revealed the non-living genetic pirates that shaped all life on Earth", "when_stamp": "June 1970 · 1892–1952", "timeline_step": "4/4 · 1892–1952 timeline complete", "hold_s": 3.8}),
            ("02_bacterium_cell_wall_model_vs_icosahedral_virus_capsid_model_on_plinth_pan", 161.0, 5.5, "A", False, "WHY ANTIBIOTICS NEVER TOUCH A VIRUS", "Fast",
             "Fast: daylight close-up of a sectioned bacterial cell-wall model beside a geometric icosahedral virus capsid model on a wooden museum plinth. Nothing emissive, no face.",
             STYLE + "In crisp daylight on a wooden museum plinth, a cross-sectioned bacterial cell model sits beside a geometric twenty-sided viral capsid model and a lunar-lander phage sculpture." + FAST_TAIL,
             None),
            ("03_metchnikoff_1882_starfish_behring_1890_serum_burnet_1957_and_tonegawa_1976_vdj_handoff", 166.5, 6.5, "C", False, "PHAGOCYTES, ANTIBODIES & V(D)J RECOMBINATION", "Quality",
             "Quality: readable faces (Élie Metchnikoff in December 1882 peering at a starfish larva rose thorn, Emil von Behring and Shibasaburo Kitasato in December 1890 holding diphtheria antitoxin serum, and Frank Macfarlane Burnet in October 1957 with Susumu Tonegawa in October 1976 mapping clonal selection and V(D)J recombination — handoff to 065 The Immune System, Antibodies & V(D)J Recombination).",
             STYLE + "Split period scene: on the left in December 1882 Sicily, Élie Metchnikoff inspects a starfish larva around a rose thorn while Emil von Behring and Shibasaburo Kitasato hold a vial of diphtheria antitoxin; on the right, Frank Macfarlane Burnet and Susumu Tonegawa point to Y-shaped antibody locks and shuffling V, D, and J gene blocks." + QUAL_TAIL,
             {"kind": "WHEN", "label": "DECEMBER 1882 · 4 DECEMBER 1890 · OCTOBER 1957 · OCTOBER 1976", "hold_s": 3.5}),
            ("04_table_three_callback", 173.0, 2.4, "C", False, None, "reuse",
             "Reuse: verified unused moving window [5.50s..7.90s] of P1:07_table_three_props_1892_porcelain_filter_1935_tmv_crystal_vial_and_1952_waring_blender (callback, £0).",
             "Reuse P1:07_table_three_props_1892_porcelain_filter_1935_tmv_crystal_vial_and_1952_waring_blender [5.50s..7.90s] (2.40s distinct non-overlapping tail window from 8.00s source clip).",
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
                row["reuse_of"] = "P1:07_table_three_props_1892_porcelain_filter_1935_tmv_crystal_vial_and_1952_waring_blender"
                row["reuse_window_s"] = [5.5, 7.9]
                row["reuse_audit"] = {
                    "source_row": "P1:07_table_three_props_1892_porcelain_filter_1935_tmv_crystal_vial_and_1952_waring_blender",
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
            "film": "064_Ivanovsky-Beijerinck-Stanley-Hershey-Viruses",
            "part": p_idx,
            "title": p_title,
            "version": "v01",
            "timing_status": "pre_vo_script_clock (built from viruses_script_master_v01.md; retimes onto Scribe STT once VO locks)",
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
        "film": "064_Ivanovsky-Beijerinck-Stanley-Hershey-Viruses",
        "version": "v01",
        "date": "2026-10-19",
        "owner": "gemini (J0646)",
        "status": "PRE_VO_BOARDS_V01_NO_MINT",
        "generation_authorized": False,
        "script": "00_Brand/Channel-Setup/ideas/064_Ivanovsky-Beijerinck-Stanley-Hershey-Viruses/viruses_script_master_v01.md",
        "sources": "00_Brand/Channel-Setup/ideas/064_Ivanovsky-Beijerinck-Stanley-Hershey-Viruses/SOURCES_v01.md",
        "credit_snapshot": {
            "flow_balance": 23740,
            "flow_floor": 0,
            "flow_read_at": "2026-10-15T21:42:22Z",
            "vertex_promo_gbp": 71.02,
            "vertex_usable_gbp": 70.02,
        },
        "totals": totals,
        "per_part": per_part_summary,
        "mint_order": "006 > 007 > 008 > 009 > 010 > 011 > 012 > 013 > 014 > 015 > 016 > 017 > 018 > 019 > 020 > 021 > 022 > 023 > 024 > 025 > 026 > 027 > 028 > 029 > 030 > 031 > 032 > 033 > 034 > 035 > 036 > 037 > 038 > 039 > 040 > 041 > 042 > 043 > 044 > 045 > 046 > 047 > 048 > 049 > 050 > 051 > 052 > 053 > 054 > 055 > 056 > 057 > 058 > 059 > 060 > 061 > 062 > 063 > 064 > 065. Nothing in 064 is generation_authorized.",
    }
    (EDIT / "PICTURE_PLAN_v01.json").write_text(json.dumps(plan, indent=2) + "\n")

    sl = [
        "# 064 Viruses: The Living Crystals That Hijack Your Cells — Shot list & plate boards v01 (pre-VO)",
        "",
        "Gemini, 19 Oct 2026, J0646. Built from `viruses_script_master_v01.md` (`92.7 PASS`) and `SOURCES_v01.md`.",
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
        "# 064 price review v01 (pre-VO plate boards)",
        "",
        "Gemini, 19 Oct 2026, J0646. Boards only. **No mint. No spend. No merge.**",
        "Prepared from `viruses_script_master_v01.md` (`92.7 PASS`) and `SOURCES_v01.md` so 064's full plate board rows, non-emissive Fast prompts, £0 code graphics, and Teach-on-Screen overlays are ready to re-time the moment long VO locks. Parked for Chief.",
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
        f"- **Quality ({totals['Quality']} rows):** readable faces (Dmitri Ivanovsky, Martinus Beijerinck, Félix d'Hérelle, Wendell M. Stanley, Frederick C. Bawden, Norman W. Pirie, Helmut Ruska, Alfred D. Hershey, Martha Chase, Élie Metchnikoff, Emil von Behring, Shibasaburo Kitasato, Frank Macfarlane Burnet, Susumu Tonegawa), 12 February 1892 St. Petersburg & 1898 Delft porcelain filtration, 28 June 1935 Princeton Tobacco Mosaic Virus needle crystals & May 1939 Berlin electron microscopy, 20 September 1952 Cold Spring Harbor Waring blender experiment (`35S` protein vs `32P` DNA), and the 2 Explorer beats.",
        f"- **Fast ({totals['Fast']} rows, non-emissive):** daylight prop and laboratory shots (unglazed white Chamberland porcelain filter candle, mosaic tobacco leaf & crystal vial pan, 3-object callback bench, 1898 Delft vacuum filtration flask & potted tobacco plants, ceramic mortar and pestle & serial-passage dropper bottles, 1935 TMV crystal vial & 1939 electron-micrograph plate, sculpted 2,130-subunit helical capsid & coiled RNA model, 1952 chrome Waring blender, centrifuge tubes & Geiger dial, bacterial cell-wall model vs icosahedral viral capsid on museum plinth). Zero candles, flames, sparks, or glowing elements on Fast.",
        f"- **£0 code graphics ({totals['code_graphic']} rows):**",
        "  1. `P1:04_ivanovsky_1892_beijerinck_1898_stanley_1935_hershey_chase_1952_size_and_blender_chart` — microbial filtration scale (`8,000-nm` RBC, `2,000-nm` *E. coli*, `100–200-nm` Chamberland filter pore, `300 × 18-nm` TMV rod, `30-nm` rhinovirus) & Hershey-Chase `35S/32P` blender chart (`SCALE: if a single E. coli bacterium were the size of a double-decker bus, a cold virus beside it would be no bigger than a football — easily slipping straight through a bacterium-proof porcelain filter`)",
        "  2. `P1:06_stanley_1935_bawden_pirie_1936_franklin_1955_tmv_2130_subunits_6395nt_rna_helix_chart` — Tobacco Mosaic Virus (`300 × 18 nm`) helical nucleoprotein diagram (`2,130` identical coat-protein subunits [95%] wrapped around `1` strand of `6,395-nt` RNA [5%]) (`SCALE: a tobacco mosaic virus is just one strand of genetic instructions wrapped in 2,130 identical protein bricks — so uniform that billions of them stack together in a jar like salt crystals`)",
        "  3. `P2:02_ivanovsky_1892_beijerinck_1898_porcelain_filtration_and_serial_replication_chart` — Ivanovsky (1892) & Beijerinck (1898) serial-dilution vs chemical toxin chart showing filtered *contagium vivum fluidum* (`virus`) amplifying to 100% across living leaves (`SCALE: if you drop a pinch of poison into a lake, it dilutes until it is harmless — yet one microscopic drop of Beijerinck's filtered liquid turned an entire field of healthy plants into factories making millions of new copies`)",
        "  4. `P3:02_stanley_1935_bawden_pirie_1936_ruska_1939_tmv_composition_and_em_resolution_chart` — Stanley (28 June 1935 *Science*, `10⁻⁹ g/mL` infectious crystals), Bawden & Pirie (19 December 1936 *Nature*, `95% protein + 5% RNA`), and Ruska & Kausche (May 1939, `300 × 18 nm` EM vs `200-nm` optical limit) chart (`SCALE: a tobacco mosaic virus is ten times smaller than the wavelength of green light, making it physically invisible to any optical microscope on Earth until Helmut Ruska used a beam of electrons to photograph it in 1939`)",
        "  5. `P4:02_hershey_chase_20_sep_1952_j_gen_physiol_35s_protein_vs_32p_dna_blender_chart` — Hershey & Chase (20 September 1952, *J. Gen. Physiol.* 36: 39–56) Waring blender agitation curve (`~80%` extracellular `35S` protein sheared into supernatant vs intracellular `32P` viral DNA in pellet) (`SCALE: the Hershey-Chase blender experiment proved that a virus protein coat is nothing more than a disposable delivery van — it parks on the outside of your cell wall, injects its DNA or RNA instructions inside, and gets left behind`)",
        "  6. `P5:01_timeline_1892_1952_and_antibiotic_cell_wall_target_vs_intracellular_virus_chart` — completed 4-date timeline (1892 → 1952) + bacterial antibiotic target vs intracellular virus replication diagram (`SCALE: from crushed tobacco leaves in Russia to sparkling crystals in New Jersey and a kitchen blender in New York, sixty years of detective work revealed the non-living genetic pirates that shaped all life on Earth`)",
        f"- **£0 verified reuse ({totals['reuse']} row):** `P5:04_table_three_callback` uses the 2.40 s unused moving tail `[5.50s..7.90s]` of `P1:07_table_three_props_1892_porcelain_filter_1935_tmv_crystal_vial_and_1952_waring_blender`.",
        "",
        "## Mint order",
        "",
        "006 > 007 > 008 > 009 > 010 > 011 > 012 > 013 > 014 > 015 > 016 > 017 > 018 > 019 > 020 > 021 > 022 > 023 > 024 > 025 > 026 > 027 > 028 > 029 > 030 > 031 > 032 > 033 > 034 > 035 > 036 > 037 > 038 > 039 > 040 > 041 > 042 > 043 > 044 > 045 > 046 > 047 > 048 > 049 > 050 > 051 > 052 > 053 > 054 > 055 > 056 > 057 > 058 > 059 > 060 > 061 > 062 > 063 > 064 > 065. `generation_authorized` is `false` on every row.",
    ])
    (EDIT / "PRICE_REVIEW_v01.md").write_text("\n".join(pr_lines) + "\n")
    print(f"064 v01 boards written: {totals['rows']} rows, Flow expected={totals['flow_credits_expected']}")


if __name__ == "__main__":
    main()
