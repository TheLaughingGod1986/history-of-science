#!/usr/bin/env python3
"""HOS 051 (Spicy Chilis & Cold Mint: The Chemical Trick Inside Your Mouth) pre-VO plate boards v01. J0585. No mint, no spend.

Built from 00_Brand/Channel-Setup/ideas/051_Scoville-Julius-Patapoutian-Spicy-Capsaicin-TRPV1/spicy_script_master_v01.md (93.2 PASS)
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
        "Part 01 — Why a Cold Chili Pepper Feels Like 43 °C Fire & a Mint Leaf Feels Like Ice",
        [
            ("01_thermometer_37c_habanero_trpv1_43c_and_menthol_trpm8_26c_nerve_doors", 0.0, 5.5, "A", False, "HIJACKED THERMOMETER DOORS", "Quality",
             "Quality: Short frame 0 / answer image (0:03) + a glass thermometer inside a mouth biting a fiery red habanero chili stays locked at a calm 37.0 °C while the camera dives into the tongue's nerve endings to show a capsaicin molecule wedging open the exact same TRPV1 ion-channel trapdoor that springs open at 43 °C scalding heat, contrasted with a green peppermint menthol crystal wedging open the cold TRPM8 channel below 26 °C.",
             STYLE + "Split period-and-molecular scene: on the left, a glass mercury thermometer beside a sliced red habanero chili pepper and a green peppermint leaf stays steady at body temperature; on the right, a molecular capsaicin key wedges open a red nerve-membrane gate while a crystalline menthol key wedges open a blue cold gate." + QUAL_TAIL,
             {"kind": "WHEN", "label": "MAY 1912 · 23 OCTOBER 1997", "timeline_step": "2/5 · May 1912 (Wilbur Scoville in Detroit invents the 16,000,000-unit human dilution taste test) & 4/5 · 23 Oct 1997 (David Julius and Michael Caterina clone TRPV1)", "hold_s": 3.5}),
            ("02_scoville_1912_detroit_julius_1997_ucsf_trpv1_and_thrasher_bird_chiltepin_split", 5.5, 6.0, "B", False, "SCOVILLE, TRPV1 & TRPM8, BIRDS VS MAMMALS", "Quality",
             "Quality: complex three-part composition (Wilbur Scoville in Detroit in May 1912 diluting pepper extract across flasks of sweetened water; David Julius's 1997 UCSF petri dish of kidney cells flashing bright green as capsaicin and 43 °C water open TRPV1 alongside Ardem Patapoutian's 2002 cold TRPM8 channel; and a wild curve-billed thrasher bird gulping red chiltepin peppers whole while a desert mouse spits crushed seeds out).",
             STYLE + "Three-panel period composition: on the left, a 1912 Detroit pharmacy bench with graduated glass dilution flasks and red pepper extract; in the centre, a 1997 microscope dish glowing emerald green beside a water bath; on the right, a desert thrasher bird swallowing bright red wild chilies on a bush while a small field mouse recoils." + QUAL_TAIL,
             None),
            ("03_caterina_julius_23_oct_1997_ucsf_petri_dish_flashing_to_capsaicin_and_43c_water", 11.5, 6.0, "C", False, "SAME DOOR FOR CHILI AND HEAT", "Quality",
             "Quality: readable faces (in San Francisco on 23 October 1997, Michael Caterina and David Julius watch a fluorescence monitor where engineered cells flash with rushing calcium ions first when touched by a drop of capsaicin, and then identically when warmed across the 43 °C pain threshold with pure hot water).",
             STYLE + "In a 1997 San Francisco laboratory, physiologist David Julius and postdoctoral fellow Michael Caterina watch a microscope monitor as a dish of cells flashes bright green first from a pipette drop of chili extract and then from clean warm water." + QUAL_TAIL,
             {"kind": "WHEN", "label": "SAN FRANCISCO, 23 OCTOBER 1997", "timeline_step": "4/5 · 23 Oct 1997 (David Julius and Michael Caterina clone TRPV1, proving capsaicin and 43 °C heat open the same ion channel)", "hold_s": 3.5}),
            ("04_trpm8_26c_trpv1_43c_thermal_activation_and_scoville_16m_shu_chart", 17.5, 8.0, "E", False, "TRPM8 (<26 °C / MENTHOL) & TRPV1 (>43 °C / CAPSAICIN) THERMAL CURVES + SCOVILLE SCALE (0 TO 16,000,000 SHU)", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked dual-receptor temperature & Scoville dilution chart from Caterina & Julius (1997 Nature) and McKemy/Julius & Peier/Patapoutian (2002 Nature/Cell) plots nerve-channel current from 8 °C to 55 °C — TRPM8 opening below 26 °C (and shifting warmer with menthol) and TRPV1 snapping open above 43 °C (and shifting below 37 °C with capsaicin) — alongside Scoville Heat Units spanning 0 (bell pepper), 5,000 (jalapeño), 300,000 (habanero), and 16,000,000 (pure capsaicin).",
             {"kind": "DATA", "label": "TRPM8 (<26 °C) & TRPV1 (>43 °C) THERMAL GATES + SCOVILLE SCALE (0 TO 16,000,000 SHU)", "detail": "Inked dual-receptor temperature & Scoville dilution chart on period paper showing TRPM8 opening below 26 °C (or with menthol at 37 °C) and TRPV1 opening above 43 °C (or with capsaicin at 37 °C), paired with Scoville Heat Units spanning 0 (bell pepper), 5,000 (jalapeño), 300,000 (habanero), and 16,000,000 (pure capsaicin)", "scale": "one drop of pure capsaicin diluted into sixteen million drops of water — about eight hundred litres, or five full bathtubs — still sets a human tongue tingling", "who_card": "John Clough Thresh (1850–1932) — British pharmaceutical chemist · Wilbur Lincoln Scoville (1865–1942) — American pharmacist · David Julius (born 1955) — American physiologist · Michael J. Caterina (born 1965) — American neurobiologist · Ardem Patapoutian (born 1967) — Lebanese-American molecular biologist", "when_stamp": "1876 · May 1912 · 23 October 1997 · February–March 2002", "hold_s": 3.8}),
            ("05_red_chili_peppers_peppermint_leaves_scoville_flasks_and_thermometer_pan", 25.5, 5.5, "A", False, "16,000,000 DROPS", "Fast",
             "Fast: daylight macro pan across fresh red habanero and cayenne peppers, green peppermint leaves, graduated glass dilution flasks, and a brass-mounted glass thermometer on an oak bench between code graphics so two full-frame graphics never run back to back. Nothing emissive, no face.",
             STYLE + "In crisp daylight on an oak laboratory bench, the camera pans smoothly across glossy red chili peppers, fresh green peppermint sprigs, a row of glass volumetric flasks, and a vintage mercury thermometer." + FAST_TAIL,
             None),
            ("06_trpv1_43c_to_30c_capsaicin_threshold_shift_and_trpm8_menthol_shift_chart", 31.0, 8.0, "E", False, "43 °C ALARM AT 37 °C", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period parchment, an inked TRPV1 threshold-shift graph shows activation temperature dropping from 43 °C (normal noxious heat threshold) to <33 °C when capsaicin binds so normal 37 °C mouth warmth continuously fires pain signals, while TRPM8 cold activation shifts from <26 °C up to >34 °C when peppermint menthol binds.",
             {"kind": "DATA", "label": "TRPV1 THRESHOLD SHIFT (43 °C → <33 °C WITH CAPSAICIN) & TRPM8 SHIFT (<26 °C → >34 °C WITH MENTHOL)", "detail": "Inked TRPV1 threshold-shift graph showing activation temperature dropping from 43 °C (normal noxious heat threshold) to <33 °C when capsaicin binds, while TRPM8 cold activation shifts from <26 °C up to >34 °C when peppermint menthol binds", "scale": "the chili isn't heating your mouth at all — it rewires the thermostat on your nerve doors so your own thirty-seven-degree blood feels like scalding water", "hold_s": 3.8}),
            ("07_table_three_props_scoville_flask_chili_and_mint_with_trpv1_trpm8_gate_models", 39.0, 5.5, "C", False, "1876 TO 2002", "Fast",
             "Fast: daylight prop table (callback source for Part 05: Wilbur Scoville's 1912 graduated glass dilution flask and dropper, fresh red chili peppers beside green peppermint leaves, and carved brass-and-wood models of the TRPV1 and TRPM8 ion-channel gates). Nothing emissive.",
             STYLE + "On an oak workbench in soft window light sit three objects side by side: a glass dilution flask with a dropper of red pepper extract, fresh red chilies beside green peppermint leaves, and a pair of detailed brass-and-wood molecular gate models." + FAST_TAIL,
             None),
            ("08_explorer_between_43c_fire_trpv1_door_and_26c_ice_trpm8_door_with_chili_and_mint_keys", 62.0, 5.5, "A", True, None, "Quality",
             "Quality: Explorer beat 1 (locked character reference, after 1:00).",
             STYLE + "Standing between two giant brass nerve-membrane trapdoors — a red door and a blue door — the Explorer watches a tiny chili-pepper key pick the red lock and a peppermint-leaf key pick the blue lock, ringing both alarm bells while a central mercury thermometer stays dead still." + EXP_TAIL,
             None),
            ("09_wilbur_scoville_may_1912_detroit_lining_up_sugar_water_flasks_for_five_tasters", 67.5, 5.5, "B", False, "DETROIT, MAY 1912", "Quality",
             "Quality: readable faces (in Detroit in May 1912, pharmacist Wilbur Scoville lines up glass flasks of sugar water and a dropper of dark red pepper extract before five tasters, followed by water sliding off greasy red capsaicin oil while milk dissolves it).",
             STYLE + "In a 1912 Detroit pharmaceutical laboratory, pharmacist Wilbur Scoville in a white coat lines up graduated glass flasks of sugar water and a glass dropper of red chili extract before five seated tasters." + QUAL_TAIL,
             {"kind": "WHEN", "label": "DETROIT, MAY 1912", "timeline_step": "2/5 · May 1912 (Wilbur Scoville in Detroit invents the 16,000,000-unit human dilution taste test)", "hold_s": 3.5}),
        ],
    ),
    (
        2,
        "Part 02 — 1876 & May 1912: John Clough Thresh's Capsaicin Crystals, Wilbur Scoville's 16-Million-Drop Taste Test & Why Water Fails",
        [
            ("01_thresh_1876_capsaicin_crystals_and_scoville_may_1912_detroit_five_tasters_panel", 73.0, 6.5, "A", False, "1 IN 16,000,000 DILUTION", "Quality",
             "Quality: readable faces (British chemist John Clough Thresh in 1876 isolating colourless crystals of capsaicin from cayenne pepper, dissolving to American pharmacist Wilbur Lincoln Scoville in May 1912 at Parke-Davis in Detroit handing measured glasses of sweetened pepper dilution to a panel of five human tasters).",
             STYLE + "Split period scene: on the left in an 1876 British pharmacy lab, John Clough Thresh examines colourless crystals in a glass dish beside red cayenne pods; on the right in May 1912 in Detroit, Wilbur Scoville hands small tasting glasses of diluted pepper water to five tasters." + QUAL_TAIL,
             {"kind": "FACT", "label": "1 in 16,000,000 dilution", "when_stamp": "1876 · May 1912 · 1919", "timeline_step": "1/5 · 1876 (John Clough Thresh isolates pure crystalline capsaicin) & 2/5 · May 1912 (Wilbur Scoville invents the 16,000,000-unit dilution scale)", "hold_s": 3.8}),
            ("02_scoville_1912_dilution_scale_0_to_16m_shu_and_milk_casein_solubility_chart", 79.5, 8.0, "E", False, "MAY 1912 SCOVILLE SCALE (0 TO 16,000,000 SHU) & HYDROPHOBIC CAPSAICIN TAIL VS MILK CASEIN", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked Scoville dilution & hydrophobic solubility chart from Wilbur Scoville (May 1912, J. Am. Pharm. Assoc. 1: 453–454) and E. K. Nelson (1919) compares bell pepper (0 SHU), jalapeño (~5,000 SHU), cayenne (~40,000 SHU), habanero (~300,000 SHU), and pure capsaicin (16,000,000 SHU) alongside casein micelles in milk stripping hydrophobic capsaicin off nerve membranes.",
             {"kind": "DATA", "label": "SCOVILLE SCALE (0 TO 16,000,000 SHU) & WATER-INSOLUBLE CAPSAICIN TAIL LIFTED BY MILK CASEIN", "detail": "Inked Scoville dilution & hydrophobic solubility chart on period paper from Wilbur Scoville (May 1912, J. Am. Pharm. Assoc. 1: 453–454) comparing bell pepper (0 SHU), jalapeño (~5,000 SHU), cayenne (~40,000 SHU), habanero (~300,000 SHU), and pure capsaicin (16,000,000 SHU) alongside casein micelles in milk stripping hydrophobic capsaicin off nerve membranes", "scale": "drinking cold water on a chili burn is like trying to wash motor oil off your hands with plain water — while milk's casein proteins act like tiny detergent sponges that lift the greasy capsaicin molecule off your nerves", "hold_s": 3.8}),
            ("03_scoville_1912_graduated_cylinders_parke_davis_liniment_and_1912_paper_closeup", 87.5, 6.5, "B", False, "MAY 1912 — THE SCOVILLE SCALE", "Fast",
             "Fast: daylight macro shot of Wilbur Scoville's graduated glass cylinders beside an amber apothecary bottle of chili liniment and the May 1912 pharmacy journal on an oak bench. Nothing emissive, no face.",
             STYLE + "In crisp daylight on an oak pharmacy bench, tall graduated glass cylinders and a glass pipette rest beside an amber apothecary bottle of pepper extract and an open 1912 pharmaceutical journal." + FAST_TAIL,
             None),
            ("04_water_beading_off_red_capsaicin_oil_vs_white_milk_dissolving_droplets_pan", 94.0, 5.5, "C", False, "1919 — GREASY HYDROCARBON TAIL", "Fast",
             "Fast: daylight close-up pan across a glass dish where clear water beads off a glossy red oil droplet, beside a second glass dish where creamy white milk surrounds and lifts the red droplet cleanly away. Nothing emissive, no face.",
             STYLE + "In bright window light on a laboratory table, two glass dishes sit side by side: in the first, clear water slides off a glossy red oil drop; in the second, white milk swirls around the red oil and lifts it cleanly into suspension." + FAST_TAIL,
             None),
        ],
    ),
    (
        3,
        "Part 03 — 1947–1960 & 23 October 1997: Miklós Jancsó's Clue & David Julius's Petri-Dish Hunt for TRPV1 — Midpoint Twist",
        [
            ("01_jancso_1947_szeged_and_david_julius_caterina_23_oct_1997_pool_11_trpv1", 99.5, 6.5, "A", False, "OPENS AT 43 °C HEAT", "Quality",
             "Quality: readable faces (Hungarian pharmacologist Miklós Jancsó in Szeged in 1947–1960 studying thermal pain nerves, dissolving to American physiologist David Julius and neurobiologist Michael Caterina at UCSF on 23 October 1997 screening 14,000 sensory-nerve gene pools in Fura-2 kidney cells and heating the bath across 43 °C).",
             STYLE + "Split period scene: on the left in a 1950s Hungarian laboratory, pharmacologist Miklós Jancsó records skin temperature responses beside a thermometer; on the right in 1997 San Francisco, David Julius and Michael Caterina watch Petri dish number eleven light up under a microscope beside a heated water bath." + QUAL_TAIL,
             {"kind": "WHO", "label": "Miklós Jancsó (1903–1966) — Hungarian pharmacologist", "fact_card": "Opens at 43 °C heat", "when_stamp": "1947–1960 · 23 October 1997", "timeline_step": "3/5 · 1947–1960 (Miklós Jancsó shows capsaicin selectively excites heat-pain nociceptors) & 4/5 · 23 Oct 1997 (David Julius and Michael Caterina clone TRPV1)", "hold_s": 3.8}),
            ("02_caterina_julius_1997_fura2_calcium_and_43c_trpv1_inward_current_chart", 106.0, 8.0, "E", False, "23 OCT 1997 CATERINA & JULIUS (NATURE): 14,000 GENE POOLS → POOL #11 (TRPV1) SNAPS OPEN TO CAPSAICIN & ≥43 °C HEAT", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked Fura-2 calcium-fluorescence & thermal current trace from Caterina, Julius et al. (23 October 1997, Nature 389: 816–824) shows zero current in control HEK293 kidney cells vs massive inward Ca2+/Na+ current in TRPV1-expressing cells triggered identically by 1 micromolar capsaicin or by stepping bath temperature across 43 °C.",
             {"kind": "DATA", "label": "23 OCT 1997 TRPV1 CLONING: IDENTICAL INWARD CURRENT TO CAPSAICIN AND ≥43 °C NOXIOUS HEAT", "detail": "Inked Fura-2 calcium-fluorescence & thermal current trace on period paper from Caterina, Julius et al. (23 October 1997, Nature 389: 816–824) showing zero current in control HEK293 cells vs massive inward Ca2+/Na+ current in TRPV1-expressing cells triggered identically by 1 micromolar capsaicin or by stepping bath temperature across 43 °C", "scale": "forty-three degrees Celsius is the exact razor's edge where warm water turns into tissue-damaging pain — and TRPV1 is the molecular tripwire that guards your skin and tongue", "hold_s": 3.8}),
            ("03_ucsf_1997_petri_dish_tray_micropipette_and_43c_water_bath_closeup", 114.0, 6.5, "B", False, "23 OCTOBER 1997 — TRPV1 CLONED", "Fast",
             "Fast: daylight macro shot of a numbered tray of glass culture dishes, a precision micropipette, and a brushed-steel laboratory water bath with a glass thermometer on a UCSF bench. Nothing emissive, no face.",
             STYLE + "In crisp daylight on a molecular biology workbench, a precision micropipette rests beside a grid of glass culture dishes and a stainless-steel water bath with a mercury thermometer." + FAST_TAIL,
             None),
            ("04_cutaway_trpv1_four_subunit_ion_channel_pore_and_capsaicin_pocket_model_pan", 120.5, 5.5, "C", False, "14,000 SENSORY GENES", "Fast",
             "Fast: daylight close-up pan across a 3D brass-and-wood cutaway architectural model of the four-subunit TRPV1 ion channel pore showing the side pocket where the capsaicin molecule wedges the gate open. Nothing emissive, no face.",
             STYLE + "In bright window light on an oak bench, a detailed brass-and-wood cutaway model of a four-part cell-membrane channel gate shows a small key wedged into its side pocket, holding the central pore wide open." + FAST_TAIL,
             None),
        ],
    ),
    (
        4,
        "Part 04 — July 2001 & February–March 2002: The Cold Menthol Door (TRPM8) & Why Birds Eat Fiery Chilis Like Candy",
        [
            ("01_tewksbury_2001_thrasher_bird_chiltepin_and_patapoutian_jordt_2002_trpm8_avian_trpv1", 126.0, 6.5, "A", False, "BIRDS FEEL ZERO CHILI BURN", "Quality",
             "Quality: readable faces (ecologist Joshua Tewksbury in the Arizona desert in July 2001 watching a curve-billed thrasher swallow red chiltepin peppers whole while a packrat spits them out, dissolving to Ardem Patapoutian and Sven-Eric Jordt in February–March 2002 comparing the cold/menthol TRPM8 channel and the capsaicin-immune avian TRPV1 channel).",
             STYLE + "Split period scene: on the left in the sunny Arizona desert, ecologist Joshua Tewksbury observes a curve-billed thrasher bird gulping red wild chilies from a bush; on the right in a 2002 California lab, Ardem Patapoutian and Sven-Eric Jordt inspect models of the cold menthol receptor and bird heat receptor." + QUAL_TAIL,
             {"kind": "WHO", "label": "Joshua J. Tewksbury (born 1969) — American ecologist · Sven-Eric Jordt (born 1969) — German-American pharmacologist", "fact_card": "Birds feel zero chili burn", "when_stamp": "July 2001 · 8 February 2002 · 7–8 March 2002 · 2021", "timeline_step": "5/5 · Jul 2001–Mar 2002 (Tewksbury & Jordt prove birds are immune to capsaicin while Julius and Ardem Patapoutian discover the cold/menthol channel TRPM8; 2021 Nobel Prize)", "hold_s": 3.8}),
            ("02_tewksbury_2001_seed_survival_and_jordt_julius_2002_mammal_vs_bird_trpv1_chart", 132.5, 8.0, "E", False, "2001–2002 MAMMAL (0% SEED SURVIVAL, CAPSAICIN SENSITIVE) VS BIRD (VIABLE SEEDS, CAPSAICIN IMMUNE) TRPV1 CHART", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked mammalian vs avian TRPV1 & seed-survival comparison chart from Tewksbury & Nabhan (26 July 2001, Nature 412: 403–404) and Jordt & Julius (8 February 2002, Cell 108: 421–430) shows 0% seed germination after rodent molar chewing vs high germination after bird gut passage, paired with mammal TRPV1 firing maximally to capsaicin + 43 °C heat while avian TRPV1 fires to >43 °C heat but 0% to capsaicin.",
             {"kind": "DATA", "label": "RODENT MOLARS (0% SEED GERMINATION) VS BIRD DISPERSAL & AVIAN TRPV1 CAPSAICIN IMMUNITY", "detail": "Inked mammalian vs avian TRPV1 & seed-survival comparison chart on period paper from Tewksbury & Nabhan (26 July 2001, Nature 412: 403–404) and Jordt & Julius (8 February 2002, Cell 108: 421–430) showing 0% seed germination after rodent chewing vs high germination after bird gut passage, paired with mammal TRPV1 firing maximally to capsaicin + 43 °C heat while avian TRPV1 fires to >43 °C heat but 0% to capsaicin", "scale": "a wild bird can swallow a habanero or Carolina Reaper pepper as if it were a sweet blueberry — because chili plants engineered capsaicin specifically to lock onto mammal teeth while giving winged seed-couriers a free pass", "hold_s": 3.8}),
            ("03_peppermint_leaves_menthol_crystals_and_trpm8_cold_channel_model_closeup", 140.5, 6.5, "B", False, "MARCH 2002 — TRPM8 COLD DOOR", "Fast",
             "Fast: daylight macro shot of fresh green peppermint leaves, translucent menthol crystals in a watch glass, and a blue-tinted brass model of the TRPM8 cold receptor gate on a laboratory bench. Nothing emissive, no face.",
             STYLE + "In crisp daylight on a wooden workbench, fresh green peppermint leaves and clear menthol prisms in a glass dish sit beside a blue-patinated brass model of a cell-membrane cold gate." + FAST_TAIL,
             None),
            ("04_explorer_at_wild_chili_bush_watching_capsaicin_key_bounce_off_bird_lock_and_open_rodent_alarm", 147.0, 5.5, "B", True, None, "Quality",
             "Quality: Explorer beat 2 (locked character reference).",
             STYLE + "Standing beside a bush of bright red chili peppers with two wooden lockboxes — a bird courier box and a rodent grinder box — the Explorer watches a red chili key bounce harmlessly off the bird keyhole while clicking into the rodent lock and ringing its alarm bell." + EXP_TAIL,
             None),
        ],
    ),
    (
        5,
        "Part 05 — Why Ice Water Fails on Spicy Food — & Why a Yacht Experiment With Jellyfish Venom Revealed the Mystery of Allergies",
        [
            ("01_timeline_1876_2021_and_milk_casein_vs_8pct_capsaicin_pain_patch_chart", 152.5, 8.5, "E", False, "1876–2021 TIMELINE · THRESH CAPSAICIN, SCOVILLE 16M SHU, JANCSÓ, JULIUS TRPV1 (43 °C) & PATAPOUTIAN TRPM8 (<26 °C)", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, the 5-date timeline completes: 1876 (John Clough Thresh in London isolates pure crystalline capsaicin) · May 1912 (Wilbur Scoville in Detroit invents the 16,000,000-unit human dilution taste test) · 1947–1960 (Miklós Jancsó shows capsaicin selectively excites and desensitises heat-pain nociceptors) · 23 Oct 1997 (David Julius and Michael Caterina clone TRPV1, proving capsaicin and 43 °C heat open the same ion channel) · Jul 2001–Mar 2002 (Tewksbury & Jordt prove birds are immune to capsaicin while Julius and Ardem Patapoutian discover the cold/menthol channel TRPM8; 2021 Nobel Prize), alongside the milk-casein and 8% capsaicin pain-patch defunctionalisation diagram.",
             {"kind": "DATA", "label": "1876–2021 THERMAL RECEPTOR TIMELINE · SCOVILLE 16M SHU, TRPV1 (43 °C), TRPM8 (<26 °C) & 8% PAIN PATCH", "detail": "Animated 5-date timeline (1876 → 2021) alongside the hydrophobic water-repelling vs milk-casein and TRPV1 pain-patch defunctionalisation diagram", "scale": "every time you bite into a spicy curry or brush your teeth with mint, you are playing a molecular piano of temperature doors that took one hundred and twenty-six years of chemistry and neuroscience to decode", "when_stamp": "1876–2021", "timeline_step": "5/5 · 1876–2021 timeline complete", "hold_s": 3.8}),
            ("02_milk_glass_chili_pepper_and_8pct_capsaicin_medical_patch_on_plinth_pan", 161.0, 5.5, "A", False, "FALSE ALARM, NOT TISSUE BURN", "Fast",
             "Fast: daylight close-up of a glass of white milk beside red chili peppers, green mint leaves, and a medical dermal pain patch on a wooden museum plinth. Nothing emissive, no face.",
             STYLE + "In crisp daylight on a wooden museum plinth, a tall glass of milk sits beside fresh red chili peppers, green peppermint leaves, and a neatly packaged medical skin patch." + FAST_TAIL,
             None),
            ("03_richet_portier_1901_yacht_neptune_15_feb_1902_and_ishizaka_1966_ige_handoff", 166.5, 6.5, "C", False, "THE 1901 YACHT PARADOX", "Quality",
             "Quality: readable faces (French physiologists Charles Richet and Paul Portier aboard Prince Albert I of Monaco's yacht Princesse Alice II in July 1901 and in Paris on 15 February 1902 testing sea-anemone venom on the dog Neptune, alongside Henry Dale's 1910 histamine, Daniel Bovet's 1937 antihistamine, and Kimishige and Teruko Ishizaka's July 1966 IgE antibody — handoff to 052 Allergies & Anaphylaxis).",
             STYLE + "Split period scene: on the left in July 1901 aboard an ocean research yacht, French scientists Charles Richet and Paul Portier inspect a purple Portuguese man-of-war in a glass jar; on the right in 1966 Denver, immunologists Kimishige and Teruko Ishizaka examine a Y-shaped allergy antibody model." + QUAL_TAIL,
             {"kind": "WHEN", "label": "JULY 1901 · 15 FEBRUARY 1902 · 1910 · 1937 · JULY 1966", "hold_s": 3.5}),
            ("04_table_three_callback", 173.0, 2.4, "C", False, None, "reuse",
             "Reuse: verified unused moving window [5.50s..7.90s] of P1:07_table_three_props_scoville_flask_chili_and_mint_with_trpv1_trpm8_gate_models (callback, £0).",
             "Reuse P1:07_table_three_props_scoville_flask_chili_and_mint_with_trpv1_trpm8_gate_models [5.50s..7.90s] (2.40s distinct non-overlapping tail window from 8.00s source clip).",
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
                row["reuse_of"] = "P1:07_table_three_props_scoville_flask_chili_and_mint_with_trpv1_trpm8_gate_models"
                row["reuse_window_s"] = [5.5, 7.9]
                row["reuse_audit"] = {
                    "source_row": "P1:07_table_three_props_scoville_flask_chili_and_mint_with_trpv1_trpm8_gate_models",
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
            "film": "051_Scoville-Julius-Patapoutian-Spicy-Capsaicin-TRPV1",
            "part": p_idx,
            "title": p_title,
            "version": "v01",
            "timing_status": "pre_vo_script_clock (built from spicy_script_master_v01.md; retimes onto Scribe STT once VO locks)",
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
        "film": "051_Scoville-Julius-Patapoutian-Spicy-Capsaicin-TRPV1",
        "version": "v01",
        "date": "2026-10-18",
        "owner": "gemini (J0585)",
        "status": "PRE_VO_BOARDS_V01_NO_MINT",
        "generation_authorized": False,
        "script": "00_Brand/Channel-Setup/ideas/051_Scoville-Julius-Patapoutian-Spicy-Capsaicin-TRPV1/spicy_script_master_v01.md",
        "sources": "00_Brand/Channel-Setup/ideas/051_Scoville-Julius-Patapoutian-Spicy-Capsaicin-TRPV1/SOURCES_v01.md",
        "credit_snapshot": {
            "flow_balance": 23740,
            "flow_floor": 0,
            "flow_read_at": "2026-10-15T21:42:22Z",
            "vertex_promo_gbp": 71.02,
            "vertex_usable_gbp": 70.02,
        },
        "totals": totals,
        "per_part": per_part_summary,
        "mint_order": "006 > 007 > 008 > 009 > 010 > 011 > 012 > 013 > 014 > 015 > 016 > 017 > 018 > 019 > 020 > 021 > 022 > 023 > 024 > 025 > 026 > 027 > 028 > 029 > 030 > 031 > 032 > 033 > 034 > 035 > 036 > 037 > 038 > 039 > 040 > 041 > 042 > 043 > 044 > 045 > 046 > 047 > 048 > 049 > 050 > 051 > 052 > 053. Nothing in 051 is generation_authorized.",
    }
    (EDIT / "PICTURE_PLAN_v01.json").write_text(json.dumps(plan, indent=2) + "\n")

    sl = [
        "# 051 Spicy Chilis & Cold Mint: The Chemical Trick Inside Your Mouth — Shot list & plate boards v01 (pre-VO)",
        "",
        "Gemini, 18 Oct 2026, J0585. Built from `spicy_script_master_v01.md` (`93.2 PASS`) and `SOURCES_v01.md`.",
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
        "# 051 price review v01 (pre-VO plate boards)",
        "",
        "Gemini, 18 Oct 2026, J0585. Boards only. **No mint. No spend. No merge.**",
        "Prepared from `spicy_script_master_v01.md` (`93.2 PASS`) and `SOURCES_v01.md` so 051's full plate board rows, non-emissive Fast prompts, £0 code graphics, and Teach-on-Screen overlays are ready to re-time the moment long VO locks. Parked for Chief.",
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
        f"- **Quality ({totals['Quality']} rows):** readable faces (John Clough Thresh, Wilbur Lincoln Scoville, Miklós Jancsó, David Julius, Michael Caterina, Ardem Patapoutian, Joshua Tewksbury, Sven-Eric Jordt, Charles Richet, Paul Portier, Kimishige & Teruko Ishizaka), May 1912 Detroit 5-taster dilution test, 23 October 1997 UCSF Pool #11 TRPV1 discovery, 2001–2002 Arizona thrasher bird & TRPM8 cold receptor lab, and the 2 Explorer beats.",
        f"- **Fast ({totals['Fast']} rows, non-emissive):** daylight prop and laboratory shots (red chilies, peppermint leaves, Scoville flasks & thermometer pan, 3-object callback bench, Scoville's 1912 graduated cylinders & Parke-Davis liniment bottle, water beading off red capsaicin oil vs white milk casein suspension, UCSF 1997 culture dish tray & 43 °C water bath, cutaway brass-and-wood TRPV1 pore model, peppermint leaves & menthol crystals beside TRPM8 model, milk glass & 8% capsaicin patch on plinth). Zero candles, flames, sparks, or glowing elements on Fast.",
        f"- **£0 code graphics ({totals['code_graphic']} rows):**",
        "  1. `P1:04_trpm8_26c_trpv1_43c_thermal_activation_and_scoville_16m_shu_chart` — TRPM8 (<26 °C / menthol) and TRPV1 (>43 °C / capsaicin) thermal activation curves paired with the Scoville scale from 0 to 16,000,000 SHU (`SCALE: one drop of pure capsaicin diluted into sixteen million drops of water — about eight hundred litres, or five full bathtubs — still sets a human tongue tingling`)",
        "  2. `P1:06_trpv1_43c_to_30c_capsaicin_threshold_shift_and_trpm8_menthol_shift_chart` — TRPV1 threshold shift from 43 °C down below 37 °C body temperature with capsaicin, and TRPM8 cold threshold shift with menthol (`SCALE: the chili isn't heating your mouth at all — it rewires the thermostat on your nerve doors so your own thirty-seven-degree blood feels like scalding water`)",
        "  3. `P2:02_scoville_1912_dilution_scale_0_to_16m_shu_and_milk_casein_solubility_chart` — Wilbur Scoville's May 1912 dilution scale (0 to 16,000,000 SHU) and hydrophobic capsaicin hydrocarbon tail solubilised by milk casein micelles (`SCALE: drinking cold water on a chili burn is like trying to wash motor oil off your hands with plain water — while milk's casein proteins act like tiny detergent sponges that lift the greasy capsaicin molecule off your nerves`)",
        "  4. `P3:02_caterina_julius_1997_fura2_calcium_and_43c_trpv1_inward_current_chart` — Caterina & Julius's 23 October 1997 Nature Fura-2 calcium fluorescence and inward current trace triggered identically by capsaicin and ≥43 °C physical heat (`SCALE: forty-three degrees Celsius is the exact razor's edge where warm water turns into tissue-damaging pain — and TRPV1 is the molecular tripwire that guards your skin and tongue`)",
        "  5. `P4:02_tewksbury_2001_seed_survival_and_jordt_julius_2002_mammal_vs_bird_trpv1_chart` — Tewksbury & Nabhan's July 2001 rodent (0% seed survival) vs bird seed dispersal and Jordt & Julius's 8 February 2002 avian TRPV1 capsaicin-insensitivity chart (`SCALE: a wild bird can swallow a habanero or Carolina Reaper pepper as if it were a sweet blueberry — because chili plants engineered capsaicin specifically to lock onto mammal teeth while giving winged seed-couriers a free pass`)",
        "  6. `P5:01_timeline_1876_2021_and_milk_casein_vs_8pct_capsaicin_pain_patch_chart` — completed 5-date timeline (1876 → 2021) + milk-casein and 8% capsaicin patch defunctionalisation diagram (`SCALE: every time you bite into a spicy curry or brush your teeth with mint, you are playing a molecular piano of temperature doors that took one hundred and twenty-six years of chemistry and neuroscience to decode`)",
        f"- **£0 verified reuse ({totals['reuse']} row):** `P5:04_table_three_callback` uses the 2.40 s unused moving tail `[5.50s..7.90s]` of `P1:07_table_three_props_scoville_flask_chili_and_mint_with_trpv1_trpm8_gate_models`.",
        "",
        "## Mint order",
        "",
        "006 > 007 > 008 > 009 > 010 > 011 > 012 > 013 > 014 > 015 > 016 > 017 > 018 > 019 > 020 > 021 > 022 > 023 > 024 > 025 > 026 > 027 > 028 > 029 > 030 > 031 > 032 > 033 > 034 > 035 > 036 > 037 > 038 > 039 > 040 > 041 > 042 > 043 > 044 > 045 > 046 > 047 > 048 > 049 > 050 > 051 > 052 > 053. `generation_authorized` is `false` on every row.",
    ])
    (EDIT / "PRICE_REVIEW_v01.md").write_text("\n".join(pr_lines) + "\n")
    print(f"051 v01 boards written: {totals['rows']} rows, Flow expected={totals['flow_credits_expected']}")


if __name__ == "__main__":
    main()
