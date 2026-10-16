#!/usr/bin/env python3
"""HOS 070 (Enzymes: The Molecular Locks That Speed Up Life) pre-VO plate boards v01. J0676. No mint, no spend.

Built from 00_Brand/Channel-Setup/ideas/070_Fischer-Buchner-Sumner-Phillips-Enzymes-Catalysts/enzymes_script_master_v01.md
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
        "Part 01 — The 300-Atmosphere Yeast Press in Munich & the Molecular Locks Inside Every Cell",
        [
            ("01_munich_hydraulic_press_crushing_yeast_into_bubbling_zymase_and_lysozyme_cleft_snapping_sugar", 0.0, 5.5, "A", False, "LIFE WITHOUT LIVING CELLS", "Quality",
             "Quality: Short frame 0 / answer image (0:03) + a heavy cast-iron hydraulic press in Munich crushes brewer's yeast mixed with quartz sand into clear, cell-free amber liquid that erupts with streams of carbon dioxide bubbles when sugar is poured in, zooming into a 3D lysozyme enzyme cleft clamping around a sugar chain and snapping it in half.",
             STYLE + "Split laboratory-and-molecular scene: on the left, a cast-iron hydraulic press squeezes crushed yeast through canvas into a glass flask of clear amber juice that fizzes vigorously with bubbles when sugar syrup is added; on the right, a sculpted 3D lysozyme enzyme cleft clamps around a six-ring sugar chain, bends the fourth ring, and snaps the bond in two." + QUAL_TAIL,
             {"kind": "WHEN", "label": "MUNICH, 11 JANUARY 1897", "timeline_step": "1/3 · 1857, 1894 & 11 Jan 1897 (Louis Pasteur claims fermentation requires living yeast; Emil Fischer proposes the Lock-and-Key model; Eduard Buchner discovers cell-free Zymase fermentation)", "hold_s": 3.5}),
            ("02_fischer_1894_buchner_1897_sumner_1926_urease_and_koshland_1958_phillips_1965_lysozyme_split", 5.5, 6.0, "B", False, "LOCK AND KEY, UREASE CRYSTALS, X-RAY LYSOZYME", "Quality",
             "Quality: complex three-part composition (Emil Fischer in Berlin in 1894 fitting mirror-image sugar models into a brass lock alongside Eduard Buchner in Munich in January 1897 operating his hydraulic yeast press; one-armed James Sumner at Cornell in August 1926 peering through a microscope at octahedral jack-bean urease crystals; and Daniel Koshland in February 1958 with David Phillips at the Royal Institution in London in May 1965 unveiling the 3D atomic model of hen egg-white lysozyme).",
             STYLE + "Three-panel period composition: on the left, Emil Fischer in 1894 Berlin with mirror-image molecular models beside Eduard Buchner in 1897 Munich at his hydraulic press; in the centre, one-armed James Sumner in 1926 Cornell looking through a brass microscope at octahedral urease crystals; on the right, Daniel Koshland in 1958 and David Phillips in 1965 London beside the 3D atomic model of lysozyme." + QUAL_TAIL,
             None),
            ("03_catalase_enzyme_firing_40_million_oxygen_bubbles_per_second_beside_still_beaker", 11.5, 6.0, "C", False, "40 MILLION REACTIONS PER SECOND", "Quality",
             "Quality: complex molecular reveal (a catalase enzyme molecule splits 40 million hydrogen peroxide molecules per second into streams of water and oxygen bubbles while beside it an uncatalysed glass beaker of hydrogen peroxide sits completely still).",
             STYLE + "Split comparison scene: on the left, a four-subunit catalase protein machine rapidly splits incoming peroxide molecules into a rising torrent of tiny oxygen bubbles; on the right, an uncatalysed glass beaker of clear liquid sits completely still." + QUAL_TAIL,
             {"kind": "WHEN", "label": "1894 · 11 JANUARY 1897 · AUGUST 1926 · FEBRUARY 1958 · 22 MAY 1965", "timeline_step": "1/3 · 1894 & Jan 1897 (Fischer & Buchner) · 2/3 · Aug 1926 & Jul 1930 (Sumner & Northrop) · 3/3 · Feb 1958 & May 1965 (Koshland & Phillips)", "hold_s": 3.5}),
            ("04_fischer_1894_buchner_1897_sumner_1926_koshland_1958_phillips_1965_activation_energy_chart", 17.5, 8.0, "E", False, "ENZYME TRANSITION-STATE BARRIER (ΔG‡) · UREASE 10^14× SPEEDUP (3,000,000 YRS → MILLISECONDS) & CATALASE 40,000,000 H2O2/SEC", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked Enzyme Activation-Energy & Rate-Enhancement chart from Fischer (1894 Ber. Dtsch. Chem. Ges. 27: 2985–2993), Buchner (11 January 1897 Ber. Dtsch. Chem. Ges. 30: 117–124), Sumner (August 1926 J. Biol. Chem. 69: 435–441), Koshland (February 1958 PNAS 44: 98–104), and Blake, Koenig, Mair, North, Phillips & Sarma (22 May 1965 Nature 206: 757–761) plots free energy (G) along a reaction coordinate — comparing uncatalysed vs enzyme-catalysed transition-state barrier (Delta G‡) — alongside jack-bean urease's ~10^14-fold rate acceleration (from ~3,000,000 years uncatalysed to milliseconds) and catalase decomposing 40,000,000 H2O2 molecules per second.",
             {"kind": "DATA", "label": "ENZYME ACTIVATION-ENERGY TUNNEL (ΔG‡) · UREASE ~10^14× ACCELERATION (3M YRS → MS) & CATALASE 40,000,000 H2O2 MOLECULES/SEC", "detail": "Inked activation-energy & catalytic rate-acceleration chart on period paper comparing uncatalysed vs enzyme-catalysed transition-state barrier (Delta G‡) and showing urease speeding up urea hydrolysis by ~10^14-fold (from ~3,000,000 years uncatalysed to milliseconds) and catalase decomposing 40,000,000 H2O2 molecules per second", "scale": "an enzyme lowers the energy mountain a chemical reaction has to climb — like blasting a flat railway tunnel straight through the base of Mount Everest so molecules can zip across in milliseconds instead of waiting millions of years", "who_card": "Hermann Emil Fischer (1852–1919) — German organic chemist · Eduard Buchner (1860–1917) — German chemist and zymologist · James B. Sumner (1887–1955) — American biochemist · Daniel E. Koshland Jr. (1920–2007) — American biochemist · David C. Phillips (1924–1999) — British structural biologist", "when_stamp": "1894 · 11 January 1897 · August 1926 · February 1958 · 22 May 1965", "hold_s": 3.8}),
            ("05_mirror_image_sugar_models_brass_lock_and_key_and_1894_berichte_offprint_pan", 25.5, 5.5, "A", False, "THE TUNNEL THROUGH THE MOUNTAIN", "Fast",
             "Fast: daylight macro pan across a pair of mirror-image wooden ball-and-stick sugar models, a brass lock and key, and an 1894 German chemistry journal on an oak bench between code graphics so two full-frame graphics never run back to back. Nothing emissive, no face.",
             STYLE + "In crisp daylight on an oak chemistry bench, the camera pans smoothly across right- and left-handed wooden ball-and-stick sugar models, a heavy brass lock and key, and an open 1894 printed journal." + FAST_TAIL,
             None),
            ("06_buchner_11_jan_1897_berichte_300_atm_cell_free_yeast_press_zymase_chart", 31.0, 8.0, "E", False, "MUNICH, JANUARY 1897", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period parchment, an inked Buchner Cell-Free Yeast Press & Zymase Fermentation diagram (from Eduard Buchner, 11 January 1897 Ber. Dtsch. Chem. Ges. 30: 117–124) shows 1,000 g brewer's yeast ground with 1,000 g quartz sand and 200 g kieselguhr (diatomaceous earth), squeezed at 300 atmospheres in a hydraulic press to yield 500 mL of sterile, cell-free press-juice (Presssaft) that converts sucrose/glucose into CO2 gas and ethyl alcohol with 0 living cells.",
             {"kind": "DATA", "label": "11 JAN 1897 BUCHNER (BERICHTE): 1 KG YEAST + 1 KG QUARTZ SAND AT 300 ATM → 500 ML CELL-FREE ZYMASE JUICE BREWING CO2 & ETHANOL", "detail": "Inked Buchner (11 January 1897 Ber. Dtsch. Chem. Ges. 30: 117–124) cell-free yeast press-juice protocol and CO2 evolution table showing 1 kg yeast + 1 kg quartz sand + 200 g kieselguhr pressed at 300 atm -> 500 mL cell-free juice producing grams of CO2 and ethanol with 0 living cells", "scale": "squeezing yeast at three hundred atmospheres with sharp quartz sand shreds every living cell wall like glass in a blender — yet when sugar hits the dead juice, the invisible protein machines inside keep right on brewing alcohol and carbon dioxide", "hold_s": 3.8}),
            ("07_table_three_props_1894_brass_lock_key_1897_zymase_flask_and_1926_urease_crystal_slide", 39.0, 5.5, "C", False, "1894 TO 1965", "Fast",
             "Fast: daylight prop table (callback source for Part 05: Emil Fischer's 1894 brass lock and key, Eduard Buchner's 1897 flask of amber cell-free yeast press-juice with quartz sand mortar, and James Sumner's 1926 octahedral urease crystal slide). Nothing emissive.",
             STYLE + "On an oak workbench in soft window light sit three objects side by side: an ornate brass lock and key, a glass flask of clear amber yeast extract beside a porcelain mortar, and a stained microscope slide of octahedral protein crystals." + FAST_TAIL,
             None),
            ("08_explorer_bending_substrate_rod_in_flexible_active_site_glove_to_open_tunnel_through_wall", 62.0, 5.5, "A", True, None, "Quality",
             "Quality: Explorer beat 1 (locked character reference, after 1:00).",
             STYLE + "Standing beside a tall stone barrier wall, the Explorer slots a wooden substrate rod into a hinged brass glove vise that bends the rod into a strained curve, opening a low arched tunnel straight through the base of the wall as the rod snaps cleanly in two." + EXP_TAIL,
             None),
            ("09_eduard_buchner_jan_1897_munich_watching_co2_bubbles_in_cell_free_yeast_juice", 67.5, 5.5, "B", False, "FERMENTATION WITHOUT CELLS", "Quality",
             "Quality: readable face (in Munich in January 1897, German chemist Eduard Buchner watches streams of carbon dioxide bubbles rise through a glass flask of golden, completely cell-free yeast press-juice).",
             STYLE + "In an 1897 Munich chemistry laboratory, Eduard Buchner holds up a glass flask of clear golden cell-free yeast juice fizzing with rising streams of carbon dioxide bubbles beside his cast-iron hydraulic press." + QUAL_TAIL,
             {"kind": "WHEN", "label": "MUNICH, 11 JANUARY 1897", "timeline_step": "1/3 · 11 Jan 1897 (Eduard Buchner proves cell-free Zymase fermentation at 300 atmospheres)", "hold_s": 3.5}),
        ],
    ),
    (
        2,
        "Part 02 — 1857, 1894 & 11 January 1897: Pasteur's 'Vital Force', Emil Fischer's Lock-and-Key & Eduard Buchner's 300-Atmosphere Yeast Press",
        [
            ("01_emil_fischer_1894_berlin_lock_and_key_and_buchner_hahn_11_jan_1897_munich_yeast_press", 73.0, 6.5, "A", False, "DEAD YEAST JUICE BREWS ALCOHOL", "Quality",
             "Quality: readable faces (German chemist Hermann Emil Fischer in Berlin in 1894 testing mirror-image sugar models with a brass lock and key, dissolving to Eduard Buchner and Martin Hahn in Munich on 11 January 1897 grinding 1 kg of brewer's yeast with quartz sand and kieselguhr under a 300-atmosphere hydraulic press).",
             STYLE + "Split period scene: on the left in 1894 Berlin, Emil Fischer fits right- and left-handed wooden sugar models into a brass lock; on the right in January 1897 Munich, Eduard Buchner and Martin Hahn turn the wheel of a 300-atmosphere hydraulic press squeezing crushed yeast into a bubbling flask." + QUAL_TAIL,
             {"kind": "FACT", "label": "Dead yeast juice brews alcohol", "who_card": "Wilhelm Kühne (1837–1900) — German physiologist", "when_stamp": "1833 · 1857 · 1877 · 1894 · 11 January 1897 · 1907", "timeline_step": "1/3 · 1857, 1894 & 11 Jan 1897 (Pasteur's vitalism; Fischer's Lock-and-Key model; Buchner's 300-atm cell-free Zymase fermentation)", "hold_s": 3.8}),
            ("02_fischer_1894_glucoside_stereospecificity_and_buchner_1897_300_atm_zymase_yield_chart", 79.5, 8.0, "E", False, "1894 FISCHER (BERICHTE: ALPHA VS BETA GLUCOSIDE LOCK-AND-KEY) & 11 JAN 1897 BUCHNER (300 ATM CELL-FREE PRESSSAFT CO2 + ETHANOL)", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked Fischer (1894 Ber. Dtsch. Chem. Ges. 27: 2985–2993) alpha- vs beta-methyl glucoside stereospecificity chart & Buchner (11 January 1897 Ber. Dtsch. Chem. Ges. 30: 117–124) 300-atmosphere cell-free yeast press-juice CO2/ethanol yield chart shows right-handed sugar hydrolysis vs left-handed rejection and cell-free fermentation.",
             {"kind": "DATA", "label": "1894 FISCHER ALPHA/BETA GLUCOSIDE LOCK-AND-KEY & 1897 BUCHNER 300-ATM CELL-FREE YEAST JUICE CO2/ETHANOL YIELD", "detail": "Inked Fischer (1894 Ber. Dtsch. Chem. Ges. 27: 2985–2993) alpha- vs beta-methyl glucoside stereospecificity chart & Buchner (11 January 1897 Ber. Dtsch. Chem. Ges. 30: 117–124) 300-atmosphere cell-free yeast press-juice CO2/ethanol yield chart on period paper", "scale": "Emil Fischer's lock-and-key discovery showed that a yeast enzyme is as picky as a front-door Yale lock — a right-handed sugar key slides straight in and turns, while its left-handed mirror image can't even enter the keyhole", "hold_s": 3.8}),
            ("03_munich_1897_300_atm_pressure_gauge_and_quartz_sand_mortar_closeup", 87.5, 6.5, "B", False, "11 JANUARY 1897 — ZYMASE (CELL-FREE FERMENTATION)", "Fast",
             "Fast: daylight macro shot of a brass 300-atmosphere pressure gauge on a cast-iron press beside a porcelain mortar filled with brewer's yeast, quartz sand, and kieselguhr on a bench. Nothing emissive, no face.",
             STYLE + "In crisp daylight on an 1897 Munich laboratory bench, a round brass pressure dial reading 300 atmospheres sits beside a heavy porcelain mortar and pestle holding ground yeast paste and fine quartz sand." + FAST_TAIL,
             None),
            ("04_bubbling_amber_presssaft_flask_and_gas_measuring_burette_pan", 94.0, 5.5, "C", False, "ZERO LIVING CELLS", "Fast",
             "Fast: daylight close-up pan across a glass Erlenmeyer flask of clear amber cell-free yeast extract fizzing with CO2 bubbles connected by rubber tubing to a glass gas burette. Nothing emissive, no face.",
             STYLE + "In bright window light on an oak table, a glass flask of clear golden yeast extract fizzes with tiny rising bubbles beside a graduated glass gas-measuring tube." + FAST_TAIL,
             None),
        ],
    ),
    (
        3,
        "Part 03 — August 1926 & 1930: One-Armed James Sumner vs Nobel Laureate Richard Willstätter — Midpoint Twist",
        [
            ("01_james_sumner_aug_1926_cornell_urease_crystals_and_northrop_1930_pepsin_vs_willstatter", 99.5, 6.5, "A", False, "ENZYMES ARE PURE FOLDED PROTEINS", "Quality",
             "Quality: readable faces (one-armed American biochemist James B. Sumner at Cornell in August 1926 peering into his microscope at octahedral jack-bean urease crystals with his left coat sleeve pinned, dissolving to Richard Willstätter's dispute and John Howard Northrop in July 1930 crystallising stomach pepsin).",
             STYLE + "Split period scene: on the left in August 1926 Ithaca, one-armed biochemist James Sumner adjusts a brass microscope with his right hand beside a flask of jack-bean extract; on the right in July 1930 Princeton, John Howard Northrop holds up a dish of crystalline pepsin opposite a sceptical Richard Willstätter." + QUAL_TAIL,
             {"kind": "FACT", "label": "Enzymes are pure folded proteins", "who_card": "Richard Willstätter (1872–1942) — German organic chemist · John Howard Northrop (1891–1987) — American biochemist", "when_stamp": "1917 · August 1926 · 20 July 1930 · 1932 · 1946", "timeline_step": "2/3 · Aug 1926 & 20 Jul 1930 (One-armed James Sumner crystallises jack-bean urease and John Howard Northrop crystallises pepsin, proving enzymes are pure proteins)", "hold_s": 3.8}),
            ("02_sumner_aug_1926_jbc_octahedral_urease_and_northrop_20_jul_1930_pepsin_crystal_chart", 106.0, 8.0, "E", False, "AUG 1926 SUMNER (J. BIOL. CHEM. 69: 435–441: OCTAHEDRAL UREASE CRYSTALS, 10^14× RATE) & 20 JUL 1930 NORTHROP CRYSTALLINE PEPSIN", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked Sumner (August 1926 J. Biol. Chem. 69: 435–441) octahedral jack-bean urease crystal activity table & Northrop (20 July 1930 J. Gen. Physiol. 13: 739–766) crystalline pepsin solubility/activity proof shows constant specific enzymatic activity across repeated protein recrystallisations and urease's 10^14-fold catalytic rate acceleration.",
             {"kind": "DATA", "label": "AUG 1926 SUMNER OCTAHEDRAL UREASE CRYSTALS (~10^14× SPEEDUP) & JUL 1930 NORTHROP PEPSIN RECRYSTALLISATION PROOF", "detail": "Inked Sumner (August 1926 J. Biol. Chem. 69: 435–441) octahedral jack-bean urease crystal activity table & Northrop (20 July 1930 J. Gen. Physiol. 13: 739–766) crystalline pepsin solubility/activity proof on period paper showing constant specific enzymatic activity across repeated protein recrystallisations and urease's 10^14-fold catalytic rate acceleration", "scale": "Willstätter missed the protein in his diluted enzyme solutions because enzymes are so powerful that a pinch of enzyme too small for a 1920s protein test to spot could still chew through millions of molecules a second", "hold_s": 3.8}),
            ("03_cornell_1926_jack_beans_acetone_flask_and_octahedral_crystal_sketch_closeup", 114.0, 6.5, "B", False, "AUGUST 1926 — CRYSTALLINE UREASE IS PURE PROTEIN", "Fast",
             "Fast: daylight macro shot of white jack beans in a porcelain dish beside a stoppered bottle of acetone and a 1926 microscope drawing of sharp octahedral urease crystals on a bench. Nothing emissive, no face.",
             STYLE + "In crisp daylight on a 1926 Cornell laboratory bench, a porcelain dish of white jack beans sits beside a glass reagent bottle and an inked micrograph drawing of eight-sided octahedral crystals." + FAST_TAIL,
             None),
            ("04_octahedral_urease_and_hexagonal_pepsin_crystal_models_on_oak_table_pan", 120.5, 5.5, "C", False, "20 JULY 1930 — CRYSTALLINE PEPSIN & TRYPSIN", "Fast",
             "Fast: daylight close-up pan across two faceted glass crystal models on an oak table: an eight-sided octahedral urease crystal and a six-sided hexagonal prism pepsin crystal. Nothing emissive, no face.",
             STYLE + "In bright window light on an oak table, a faceted octahedral crystal model sits beside a hexagonal prism crystal model and a pair of brass callipers." + FAST_TAIL,
             None),
        ],
    ),
    (
        4,
        "Part 04 — February 1958 & 22 May 1965: Daniel Koshland's Induced-Fit Glove & David Phillips's 3D X-Ray Movie of Lysozyme",
        [
            ("01_daniel_koshland_feb_1958_induced_fit_and_david_phillips_louise_johnson_22_may_1965_lysozyme", 126.0, 6.5, "A", False, "BENDS SUGAR RINGS UNTIL THEY SNAP", "Quality",
             "Quality: readable faces (American biochemist Daniel E. Koshland Jr. in February 1958 demonstrating his flexible induced-fit active-site model, dissolving to David C. Phillips, Colin Blake, and Louise Johnson at the Royal Institution in London on 22 May 1965 unveiling the 2-angstrom 3D X-ray model of hen egg-white lysozyme).",
             STYLE + "Split period scene: on the left in February 1958 New York, Daniel Koshland demonstrates a flexible glove model clamping around a substrate rod; on the right in May 1965 London, David Phillips and Louise Johnson point to the active-site cleft of their wire-and-brass 3D atomic model of lysozyme." + QUAL_TAIL,
             {"kind": "FACT", "label": "Bends sugar rings until they snap", "who_card": "Linus Pauling (1901–1994) — American chemist · Louise N. Johnson (1940–2012) — British structural biochemist", "when_stamp": "1922 · 1946 · February 1958 · 22 May 1965", "timeline_step": "3/3 · Feb 1958 & 22 May 1965 (Daniel Koshland proposes the Induced-Fit flexible active site; David Phillips & Louise Johnson solve the first 2-angstrom 3D X-ray enzyme structure, lysozyme)", "hold_s": 3.8}),
            ("02_koshland_feb_1958_pnas_induced_fit_and_phillips_22_may_1965_nature_lysozyme_cleft_chart", 132.5, 8.0, "E", False, "FEB 1958 KOSHLAND (PNAS: INDUCED FIT) & 22 MAY 1965 BLAKE & PHILLIPS (NATURE 206: 757–761: 2-Å LYSOZYME SUBSITES A–F, GLU35 & ASP52)", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked Koshland (February 1958 PNAS 44: 98–104) Induced-Fit conformational alignment diagram & Blake, Koenig, Mair, North, Phillips & Sarma (22 May 1965 Nature 206: 757–761) 2-angstrom hen egg-white lysozyme 129-amino-acid active-site cleft chart shows subsites A–F distorting bacterial peptidoglycan sugar ring D into a half-chair transition state between Glu35 and Asp52.",
             {"kind": "DATA", "label": "1958 KOSHLAND INDUCED-FIT GLOVE & 22 MAY 1965 PHILLIPS 2-Å LYSOZYME CLEFT (129 AA, SUBSITES A–F, GLU35 & ASP52 RING-D CLEAVAGE)", "detail": "Inked Koshland (February 1958 PNAS 44: 98–104) Induced-Fit conformational alignment diagram & Blake, Koenig, Mair, North, Phillips & Sarma (22 May 1965 Nature 206: 757–761) 2-angstrom hen egg-white lysozyme 129-amino-acid active-site cleft chart on period paper showing subsites A–F distorting bacterial peptidoglycan sugar ring D into a half-chair transition state between Glu35 and Asp52", "scale": "breaking a sugar chain with lysozyme is like snapping a green stick over your knee — the enzyme's cleft grabs both ends and bends the middle ring into a tight curve until the two chemical claws clip the strained bond with effortless ease", "hold_s": 3.8}),
            ("03_royal_institution_1965_perspex_electron_density_stack_and_brass_lysozyme_model_closeup", 140.5, 6.5, "B", False, "22 MAY 1965 — LYSOZYME AT 2 ANGSTROMS", "Fast",
             "Fast: daylight macro shot of stacked clear Perspex contour sheets inked with X-ray electron-density maps beside a brass wire model of the lysozyme cleft on a bench. Nothing emissive, no face.",
             STYLE + "In crisp daylight on a 1965 London workbench, a stack of transparent acrylic sheets inked with contour rings sits beside a brass skeletal model of a protein cleft holding a six-ring sugar chain." + FAST_TAIL,
             None),
            ("04_explorer_inside_lysozyme_cleft_bending_sugar_ring_d_and_snipping_bond_with_glu35_asp52", 147.0, 5.5, "B", True, None, "Quality",
             "Quality: Explorer beat 2 (locked character reference).",
             STYLE + "Standing beside a large sculpted model of the lysozyme active-site cleft, the Explorer pulls the two hinged sides of the cleft inward to bend the fourth ring of a six-ring wooden sugar chain into a strained sofa shape, then presses two brass cutter levers together to snap the bond cleanly." + EXP_TAIL,
             None),
        ],
    ),
    (
        5,
        "Part 05 — Why Aspirin & Penicillin Work by Jamming Enzymes — & How a Two-Molecule Soap Bubble Keeps Your Cells Alive",
        [
            ("01_timeline_1857_1965_and_enzyme_inhibitor_drug_keyhole_chart", 152.5, 8.5, "E", False, "1857–1965 TIMELINE · FISCHER LOCK-AND-KEY, BUCHNER ZYMASE, SUMNER/NORTHROP CRYSTALS, KOSHLAND INDUCED FIT, PHILLIPS LYSOZYME & DRUG INHIBITORS", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, the 3-era timeline completes: 1857, 1894 & 11 Jan 1897 (Louis Pasteur claims fermentation requires living yeast; Emil Fischer proposes the Lock-and-Key enzyme model; Eduard Buchner crushes yeast at 300 atm and discovers cell-free Zymase fermentation, winning the 1907 Nobel Prize) · Aug 1926 & 20 Jul 1930 (James Sumner crystallises jack-bean urease with one arm and John Howard Northrop crystallises pepsin, proving enzymes are pure proteins and winning the 1946 Nobel Prize) · Feb 1958 & 22 May 1965 (Daniel Koshland proposes the Induced-Fit flexible active site; David Phillips & Louise Johnson solve the first 2-angstrom 3D X-ray structure of an enzyme, hen egg-white lysozyme).",
             {"kind": "DATA", "label": "1857–1965 ENZYMES TIMELINE · STRUCTURE-BASED DRUG DESIGN (ASPIRIN BLOCKING COX & PENICILLIN BLOCKING BACTERIAL TRANSPEPTIDASE)", "detail": "Animated timeline (1857 → 1965) alongside an inked diagram of competitive and suicide enzyme inhibition showing aspirin and penicillin plugging target active-site keyholes", "scale": "from a 300-atmosphere yeast press in Munich to an X-ray beam in London, scientists proved that life's chemistry needs no magic vital force — only folded protein machines that bend molecules across the finish line", "when_stamp": "1857–1965", "timeline_step": "3/3 · 1857–1965 timeline complete", "hold_s": 3.8}),
            ("02_inhibitor_key_in_enzyme_cleft_beside_phospholipid_bilayer_membrane_model_on_plinth_pan", 161.0, 5.5, "A", False, "HOW MEDICINES JAM ENZYME LOCKS", "Fast",
             "Fast: daylight close-up of a custom-cut brass inhibitor key fitted tightly into a sculpted enzyme cleft beside a two-layer phospholipid membrane model on a wooden museum plinth. Nothing emissive, no face.",
             STYLE + "In crisp daylight on a wooden museum plinth, a sculpted protein lock plugged by a precision brass inhibitor key sits beside a cross-section model of a two-layer phospholipid cell membrane." + FAST_TAIL,
             None),
            ("03_overton_1895_gorter_grendel_1_apr_1925_skou_1957_singer_nicolson_1972_and_agre_1992_aquaporin_handoff", 166.5, 6.5, "C", False, "CELL MEMBRANES, BILAYERS & AQUAPORINS", "Quality",
             "Quality: readable faces (Ernest Overton in Zurich in 1895 alongside Evert Gorter and François Grendel in Leiden on 1 April 1925 drawing a silk thread across their 2:1 red-blood-cell lipid monolayer trough, dissolving to Jens Christian Skou in Aarhus in February 1957 with shore crabs, Jonathan Singer and Garth Nicolson on 18 February 1972 with the Fluid Mosaic Model, and Peter Agre in Baltimore on 17 April 1992 with exploding aquaporin frog oocytes — handoff to 071 Cell Membranes, Bilayers & Aquaporins).",
             STYLE + "Split period scene: on the left in April 1925 Leiden, Evert Gorter and François Grendel draw a silk thread across a water trough to measure a two-to-one red-blood-cell lipid film beside Ernest Overton; on the right in 1957 Aarhus, 1972 California, and 1992 Baltimore, Jens Christian Skou, Jonathan Singer, and Peter Agre point to a two-molecule lipid bilayer studded with sodium-potassium pumps and aquaporin water channels." + QUAL_TAIL,
             {"kind": "WHEN", "label": "1895 · 1 APRIL 1925 · FEBRUARY 1957 · 18 FEBRUARY 1972 · 17 APRIL 1992", "hold_s": 3.5}),
            ("04_table_three_callback", 173.0, 2.4, "C", False, None, "reuse",
             "Reuse: verified unused moving window [5.50s..7.90s] of P1:07_table_three_props_1894_brass_lock_key_1897_zymase_flask_and_1926_urease_crystal_slide (callback, £0).",
             "Reuse P1:07_table_three_props_1894_brass_lock_key_1897_zymase_flask_and_1926_urease_crystal_slide [5.50s..7.90s] (2.40s distinct non-overlapping tail window from 8.00s source clip).",
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
                row["reuse_of"] = "P1:07_table_three_props_1894_brass_lock_key_1897_zymase_flask_and_1926_urease_crystal_slide"
                row["reuse_window_s"] = [5.5, 7.9]
                row["reuse_audit"] = {
                    "source_row": "P1:07_table_three_props_1894_brass_lock_key_1897_zymase_flask_and_1926_urease_crystal_slide",
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
            "film": "070_Fischer-Buchner-Sumner-Phillips-Enzymes-Catalysts",
            "part": p_idx,
            "title": p_title,
            "version": "v01",
            "timing_status": "pre_vo_script_clock (built from enzymes_script_master_v01.md; retimes onto Scribe STT once VO locks)",
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
        "film": "070_Fischer-Buchner-Sumner-Phillips-Enzymes-Catalysts",
        "version": "v01",
        "date": "2026-10-19",
        "owner": "gemini (J0676)",
        "status": "PRE_VO_BOARDS_V01_NO_MINT",
        "generation_authorized": False,
        "script": "00_Brand/Channel-Setup/ideas/070_Fischer-Buchner-Sumner-Phillips-Enzymes-Catalysts/enzymes_script_master_v01.md",
        "sources": "00_Brand/Channel-Setup/ideas/070_Fischer-Buchner-Sumner-Phillips-Enzymes-Catalysts/SOURCES_v01.md",
        "credit_snapshot": {
            "flow_balance": 23740,
            "flow_floor": 0,
            "flow_read_at": "2026-10-15T21:42:22Z",
            "vertex_promo_gbp": 71.02,
            "vertex_usable_gbp": 70.02,
        },
        "totals": totals,
        "per_part": per_part_summary,
        "mint_order": "006 > 007 > 008 > 009 > 010 > 011 > 012 > 013 > 014 > 015 > 016 > 017 > 018 > 019 > 020 > 021 > 022 > 023 > 024 > 025 > 026 > 027 > 028 > 029 > 030 > 031 > 032 > 033 > 034 > 035 > 036 > 037 > 038 > 039 > 040 > 041 > 042 > 043 > 044 > 045 > 046 > 047 > 048 > 049 > 050 > 051 > 052 > 053 > 054 > 055 > 056 > 057 > 058 > 059 > 060 > 061 > 062 > 063 > 064 > 065 > 066 > 067 > 068 > 069 > 070 > 071. Nothing in 070 is generation_authorized.",
    }
    (EDIT / "PICTURE_PLAN_v01.json").write_text(json.dumps(plan, indent=2) + "\n")

    sl = [
        "# 070 Enzymes: The Molecular Locks That Speed Up Life — Shot list & plate boards v01 (pre-VO)",
        "",
        "Gemini, 19 Oct 2026, J0676. Built from `enzymes_script_master_v01.md` (`91.6 PASS`) and `SOURCES_v01.md`.",
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
        "# 070 price review v01 (pre-VO plate boards)",
        "",
        "Gemini, 19 Oct 2026, J0676. Boards only. **No mint. No spend. No merge.**",
        "Prepared from `enzymes_script_master_v01.md` (`91.6 PASS`) and `SOURCES_v01.md` so 070's full plate board rows, non-emissive Fast prompts, £0 code graphics, and Teach-on-Screen overlays are ready to re-time the moment long VO locks. Parked for Chief.",
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
        f"- **Quality ({totals['Quality']} rows):** readable faces (Hermann Emil Fischer, Eduard Buchner, Wilhelm Kühne, James B. Sumner, Richard Willstätter, John Howard Northrop, Linus Pauling, Daniel E. Koshland Jr., David C. Phillips, Louise N. Johnson, Charles Ernest Overton, Evert Gorter, François Grendel, Jens Christian Skou, S. Jonathan Singer, Peter Agre), 11 January 1897 Munich 300-atm cell-free `Zymase` yeast press & catalase `40,000,000 H₂O₂/s` reaction, August 1926 Cornell octahedral `urease` & July 1930 `pepsin` crystallisation, February 1958 `Induced-Fit` & 22 May 1965 2-angstrom X-ray `lysozyme` active-site cleft, and the 2 Explorer beats.",
        f"- **Fast ({totals['Fast']} rows, non-emissive):** daylight prop and laboratory shots (mirror-image wooden sugar models, brass lock & key and 1894 *Berichte* offprint pan, 3-object callback bench, 300-atm brass pressure gauge & porcelain mortar with quartz sand and kieselguhr, bubbling amber `Presssaft` flask & gas burette, jack beans with acetone bottle & octahedral crystal drawing, faceted octahedral `urease` & hexagonal `pepsin` crystal models, stacked Perspex X-ray electron-density sheets & brass `lysozyme` cleft model, custom-cut brass inhibitor key in enzyme lock & phospholipid bilayer plinth). Zero candles, flames, sparks, or glowing elements on Fast.",
        f"- **£0 code graphics ({totals['code_graphic']} rows):**",
        "  1. `P1:04_fischer_1894_buchner_1897_sumner_1926_koshland_1958_phillips_1965_activation_energy_chart` — transition-state activation-energy barrier (`ΔG‡`) + jack-bean `urease` `~10¹⁴-fold` rate acceleration (`~3,000,000 years` → milliseconds) & `catalase` `4 × 10⁷ H₂O₂/s` (`SCALE: an enzyme lowers the energy mountain a chemical reaction has to climb — like blasting a flat railway tunnel straight through the base of Mount Everest so molecules can zip across in milliseconds instead of waiting millions of years`)",
        "  2. `P1:06_buchner_11_jan_1897_berichte_300_atm_cell_free_yeast_press_zymase_chart` — Eduard Buchner (11 January 1897 *Ber. Dtsch. Chem. Ges.*) `1,000 g` yeast + `1,000 g` quartz sand + `200 g` kieselguhr at `300 atm` → `500 mL` sterile cell-free `Zymase` juice brewing `CO₂` and ethanol with `0` living cells (`SCALE: squeezing yeast at three hundred atmospheres with sharp quartz sand shreds every living cell wall like glass in a blender — yet when sugar hits the dead juice, the invisible protein machines inside keep right on brewing alcohol and carbon dioxide`)",
        "  3. `P2:02_fischer_1894_glucoside_stereospecificity_and_buchner_1897_300_atm_zymase_yield_chart` — Emil Fischer (1894 *Ber. Dtsch. Chem. Ges.*) α- vs β-methyl glucoside Lock-and-Key stereospecificity & Buchner (11 January 1897) cell-free `CO₂`/ethanol yield chart (`SCALE: Emil Fischer's lock-and-key discovery showed that a yeast enzyme is as picky as a front-door Yale lock — a right-handed sugar key slides straight in and turns, while its left-handed mirror image can't even enter the keyhole`)",
        "  4. `P3:02_sumner_aug_1926_jbc_octahedral_urease_and_northrop_20_jul_1930_pepsin_crystal_chart` — James Sumner (August 1926 *J. Biol. Chem.*) octahedral jack-bean `urease` crystal activity table & John Howard Northrop (20 July 1930 *J. Gen. Physiol.*) crystalline `pepsin` recrystallisation proof (`SCALE: Willstätter missed the protein in his diluted enzyme solutions because enzymes are so powerful that a pinch of enzyme too small for a 1920s protein test to spot could still chew through millions of molecules a second`)",
        "  5. `P4:02_koshland_feb_1958_pnas_induced_fit_and_phillips_22_may_1965_nature_lysozyme_cleft_chart` — Daniel Koshland (February 1958 *PNAS*) `Induced-Fit` diagram & Blake/Phillips et al. (22 May 1965 *Nature*) `2 Å` `129-amino-acid` `lysozyme` subsites A–F distorting ring D between `Glu35` and `Asp52` (`SCALE: breaking a sugar chain with lysozyme is like snapping a green stick over your knee — the enzyme's cleft grabs both ends and bends the middle ring into a tight curve until the two chemical claws clip the strained bond with effortless ease`)",
        "  6. `P5:01_timeline_1857_1965_and_enzyme_inhibitor_drug_keyhole_chart` — completed timeline (1857 → 1965) + competitive enzyme inhibition (aspirin blocking `COX`, penicillin blocking bacterial transpeptidase) (`SCALE: from a 300-atmosphere yeast press in Munich to an X-ray beam in London, scientists proved that life's chemistry needs no magic vital force — only folded protein machines that bend molecules across the finish line`)",
        f"- **£0 verified reuse ({totals['reuse']} row):** `P5:04_table_three_callback` uses the 2.40 s unused moving tail `[5.50s..7.90s]` of `P1:07_table_three_props_1894_brass_lock_key_1897_zymase_flask_and_1926_urease_crystal_slide`.",
        "",
        "## Mint order",
        "",
        "006 > 007 > 008 > 009 > 010 > 011 > 012 > 013 > 014 > 015 > 016 > 017 > 018 > 019 > 020 > 021 > 022 > 023 > 024 > 025 > 026 > 027 > 028 > 029 > 030 > 031 > 032 > 033 > 034 > 035 > 036 > 037 > 038 > 039 > 040 > 041 > 042 > 043 > 044 > 045 > 046 > 047 > 048 > 049 > 050 > 051 > 052 > 053 > 054 > 055 > 056 > 057 > 058 > 059 > 060 > 061 > 062 > 063 > 064 > 065 > 066 > 067 > 068 > 069 > 070 > 071. `generation_authorized` is `false` on every row.",
    ])
    (EDIT / "PRICE_REVIEW_v01.md").write_text("\n".join(pr_lines) + "\n")
    print(f"070 v01 boards written: {totals['rows']} rows, Flow expected={totals['flow_credits_expected']}")


if __name__ == "__main__":
    main()
