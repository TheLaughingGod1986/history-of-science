#!/usr/bin/env python3
"""HOS 082 (Warfarin: How Rat Poison Saved Millions of Lives) pre-VO plate boards v01. J0738. No mint, no spend.

Built from 00_Brand/Channel-Setup/ideas/082_Bizzozero-Morawitz-McLean-Dam-Link-Blood-Clotting-Warfarin/blood_clotting_script_master_v01.md
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
        "Part 01 — The Liquid-to-Solid Tightrope, the Blizzard Milk Can & the Rat Poison That Saved a President",
        [
            ("01_platelet_fibrin_plug_sealing_nicked_vessel_and_ed_carlson_1933_blizzard_milk_can_in_madison", 0.0, 5.5, "A", False, "HOW BLOOD CLOTS & WARFARIN", "Quality",
             "Quality: Short frame 0 / answer image (0:03) + side by side, inside a nicked microscopic blood vessel, disc-shaped platelets rush to plug the breach while golden fibrin threads weave a tight fishing net over red blood cells to seal the cut, while on a freezing Saturday in February 1933 in Madison, Wisconsin, farmer Ed Carlson pours unclotted crimson cow's blood from a metal milk can onto biochemist Karl Paul Link's laboratory floor beside a bundle of spoiled sweet clover hay.",
             STYLE + "Split microscopic-and-laboratory scene: on the left, inside a nicked blood vessel, spiky platelet discs pile into a plug as golden fibrin strands weave a tight net over red blood cells; on the right in February 1933 Madison, Wisconsin, snow-dusted farmer Ed Carlson pours unclotted crimson blood from a metal milk can before biochemist Karl Paul Link beside spoiled sweet clover hay." + QUAL_TAIL,
             {"kind": "WHEN", "label": "MADISON, WISCONSIN, FEBRUARY 1933", "timeline_step": "1/3 · 1872, 1882 & 1905 (Alexander Schmidt discovers thrombin, Giulio Bizzozero discovers living blood platelets in Turin, and Paul Morawitz maps the four-factor clotting cascade)", "hold_s": 3.5}),
            ("02_bizzozero_1882_morawitz_1905_mclean_1916_dam_1935_and_karl_paul_link_1933_1948_split", 5.5, 6.0, "B", False, "PLATELETS, HEPARIN, VITAMIN K, WARFARIN", "Quality",
             "Quality: complex three-part composition (Giulio Bizzozero in Turin in 1882 peering at living blood platelets alongside Paul Morawitz in 1905 mapping the thrombin-fibrin cascade; medical student Jay McLean and William Howell at Johns Hopkins in 1916 discovering anticoagulant heparin alongside Henrik Dam in Copenhagen in 1929–1935 discovering Vitamin K; and Karl Paul Link in Madison, Wisconsin between February 1933 and 1948 crystallising dicoumarol and Warfarin).",
             STYLE + "Three-panel period composition: on the left, Giulio Bizzozero in 1882 Turin at his brass microscope beside Paul Morawitz in 1905; in the centre, Jay McLean and William Howell in 1916 Baltimore with unclotted blood beakers beside Henrik Dam in 1935 Copenhagen; on the right, Karl Paul Link and Harold Campbell in 1939 Madison examining dicoumarol crystals." + QUAL_TAIL,
             None),
            ("03_bleeding_unsealed_vessel_vs_thrombosis_blocked_artery_balanced_by_platelets_fibrin_and_heparin", 11.5, 6.0, "C", False, "CLOT vs BLEED BALANCE", "Quality",
             "Quality: complex vascular reveal (a split comparison of an unsealed vessel leaking blood in haemorrhage vs an unwanted clot blocking a coronary artery in thrombosis, balanced by platelets/fibrin vs heparin/Vitamin K).",
             STYLE + "In a cutaway three-dimensional view of two human blood vessels, the left vessel leaks red blood cells through an unsealed tear while the right vessel is blocked by a dense thrombus clot, with a central balance scale weighing platelet-fibrin mesh against anticoagulant molecules." + QUAL_TAIL,
             {"kind": "WHEN", "label": "1882 · 1905 · 1916 · 1929 · FEBRUARY 1933 · 1935 · 1948", "timeline_step": "1/3 · 1882 & 1905 (Bizzozero & Morawitz) · 2/3 · 1916 & 1929–1935 (Jay McLean & Henrik Dam) · 3/3 · Feb 1933 – Sep 1955 (Karl Paul Link, Harold Campbell & Warfarin)", "hold_s": 3.5}),
            ("04_bizzozero_1882_morawitz_1905_mclean_1916_dam_1935_and_link_1941_coagulation_warfarin_chart", 17.5, 8.0, "E", False, "MORAWITZ (1905) 4-FACTOR CASCADE (THROMBOPLASTIN + CA²⁺ → PROTHROMBIN → THROMBIN → FIBRIN), HEPARIN (1916) & VITAMIN K VS WARFARIN", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked Coagulation Cascade, Heparin, Vitamin K & Warfarin chart from Giulio Bizzozero (1882 Virchows Archiv 90: 261–332), Paul Morawitz (1905 Ergebnisse der Physiologie 4: 307–422), Jay McLean (1916 Am. J. Physiol. 41: 250–257), Henrik Dam (1935 Nature 135: 652–653), and Karl Paul Link & Harold Campbell (1940–1941 J. Biol. Chem. 138: 21–33) shows 1) Primary haemostasis: 150,000–400,000 platelets per microlitre (~15 million per drop) form a plug; 2) Coagulation cascade: Tissue Factor (thromboplastin) + Ca²⁺ activates Prothrombin → Thrombin, cleaving soluble Fibrinogen into insoluble Fibrin mesh; 3) Heparin brakes thrombin; and 4) Vitamin K arms clotting factors in the liver while Dicoumarol/Warfarin blocks Vitamin K recycling.",
             {"kind": "DATA", "label": "MORAWITZ (1905) 4-FACTOR COAGULATION CASCADE (THROMBOPLASTIN + CA²⁺ → PROTHROMBIN → THROMBIN → FIBRIN) & VITAMIN K VS WARFARIN CHART", "detail": "Inked Morawitz (1905) 4-factor coagulation cascade (Thromboplastin + Ca²⁺ → Prothrombin → Thrombin → Fibrinogen to Fibrin) & Vitamin K vs Warfarin liver cycle chart on period paper", "scale": "a single drop of your blood holds fifteen million microscopic platelet discs waiting like deflated life rafts — the instant a vessel wall rips, they inflate spiky arms in less than a second and pile into a sandbag dam before a net of fibrin steel cables locks them solid", "who_card": "Giulio Bizzozero (1846–1901) — Italian histologist and pathologist · Paul Morawitz (1879–1936) — German physician and physiologist · Jay McLean (1890–1957) — American medical student and surgeon · William Henry Howell (1860–1945) — American physiologist · Henrik Dam (1895–1976) — Danish biochemist · Karl Paul Link (1901–1978) — American biochemist", "when_stamp": "1882 · 1905 · 1916 · 1929 · February 1933 · 1935 · 1948", "hold_s": 3.8}),
            ("05_bizzozero_1882_virchows_archiv_plate_mclean_1916_beaker_and_sweet_clover_stems_pan", 25.5, 5.5, "A", False, "15 MILLION PLATELETS PER DROP", "Fast",
             "Fast: daylight macro pan across Giulio Bizzozero's 1882 Virchows Archiv lithograph of platelets, a glass vial of purified heparin, and dried yellow sweet clover stems on an oak bench between code graphics so two full-frame graphics never run back to back. Nothing emissive, no face.",
             STYLE + "In crisp daylight on an oak hematology bench, the camera pans smoothly across an open 1882 anatomical journal showing platelet drawings, a stoppered glass vial, and dried yellow sweet clover blossoms." + FAST_TAIL,
             None),
            ("06_karl_paul_link_and_harold_campbell_28_jun_1939_sweet_clover_coumarin_to_dicoumarol_warfarin_chart", 31.0, 8.0, "E", False, "MADISON, 28 JUNE 1939", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period parchment, an inked Karl Paul Link & Harold Campbell (28 June 1939–1941 J. Biol. Chem. 138: 21–33) Sweet Clover Coumarin-to-Dicoumarol Oxidation & Prothrombin Time chart shows mouldy Melilotus clover converting harmless coumarin into 3,3'-methylenebis(4-hydroxycoumarin) (dicoumarol) and synthetic derivative #42 (Warfarin), competitively blocking Vitamin K in the liver.",
             {"kind": "DATA", "label": "1939–1948 KARL PAUL LINK & HAROLD CAMPBELL: DICOUMAROL / WARFARIN PROTHROMBIN ACTIVITY CURVE & VITAMIN K REVERSAL", "detail": "Inked Karl Paul Link (1940–1948) dicoumarol/Warfarin plasma prothrombin activity curve & reversal by Vitamin K administration on period paper", "scale": "Warfarin and Vitamin K are molecular lookalikes — Warfarin slips into the liver's clotting-factor factory like a counterfeit key that jams the lock, and giving a patient a dose of real Vitamin K pops the counterfeit key right back out", "hold_s": 3.8}),
            ("07_table_three_props_1882_bizzozero_microscope_1916_mclean_heparin_beaker_and_1933_carlson_milk_can", 39.0, 5.5, "C", False, "1882 TO 1955", "Fast",
             "Fast: daylight prop table (callback source for Part 05: Giulio Bizzozero's 1882 brass microscope, Jay McLean's 1916 glass beaker and stoppered liver-extract bottle, and Ed Carlson's 1933 dented metal Wisconsin milk can beside a bundle of sweet clover hay). Nothing emissive.",
             STYLE + "On an oak workbench in soft window light sit three objects side by side: a polished 1882 brass microscope, a glass beaker beside an amber medicine bottle, and a dented steel dairy milk can next to dried sweet clover hay." + FAST_TAIL,
             None),
            ("08_explorer_tossing_platelet_sandbags_and_fibrin_fishing_net_onto_artery_leak_and_turning_warfarin_valve", 62.0, 5.5, "A", True, None, "Quality",
             "Quality: Explorer beat 1 (locked character reference, after 1:00).",
             STYLE + "Standing beside a translucent glass artery pipe where red blood cells rush past a sudden wall breach, the Explorer tosses disc-shaped platelet sandbags into the gap, casts a golden fibrin fishing net over them to seal the leak, and adjusts a brass control valve." + EXP_TAIL,
             None),
            ("09_september_1955_president_eisenhower_recovery_with_warfarin_coumadin_tablets", 67.5, 5.5, "B", False, "SEPTEMBER 1955", "Quality",
             "Quality: readable faces (in September 1955, after US President Dwight D. Eisenhower suffers a heart attack, cardiologist Paul Dudley White and doctors treat him with Karl Paul Link's Warfarin, transforming the former rat poison into a global life-saving medicine).",
             STYLE + "In a 1955 hospital room, a smiling physician holds up a small glass bottle of Warfarin tablets beside recovering President Dwight D. Eisenhower resting comfortably in bed." + QUAL_TAIL,
             {"kind": "WHEN", "label": "SEPTEMBER 1955", "timeline_step": "3/3 · Feb 1933 – Sep 1955 (Karl Paul Link and Harold Campbell isolate dicoumarol from spoiled clover hay, patent Warfarin in 1948, and see it treat President Eisenhower in September 1955)", "hold_s": 3.5}),
        ],
    ),
    (
        2,
        "Part 02 — 1882 & 1905: Giulio Bizzozero's Living Platelets & Paul Morawitz's Thrombin-Fibrin Net",
        [
            ("01_giulio_bizzozero_1882_turin_living_vessel_platelets_and_paul_morawitz_1905_fibrin_cascade", 73.0, 6.5, "A", False, "15 MILLION PLATELETS PER DROP", "Quality",
             "Quality: readable faces (Italian histologist Giulio Bizzozero at the University of Turin in 1882 peering through a microscope at living mesenteric blood vessels as platelets rush to plug a needle nick, dissolving to Baltic German physiologist Alexander Schmidt and German physician Paul Morawitz in 1905 mapping the four-factor coagulation cascade).",
             STYLE + "Split period scene: on the left in 1882 Turin, Giulio Bizzozero peers through a brass microscope at a living blood vessel mount; on the right in 1905 Heidelberg, Paul Morawitz traces the four-factor prothrombin-to-fibrin clotting diagram on a slate board." + QUAL_TAIL,
             {"kind": "FACT", "label": "15 million platelets per drop", "who_card": "Alexander Schmidt (1831–1894) — Baltic German physiologist", "when_stamp": "1872 · 1882 · 1905", "timeline_step": "1/3 · 1872, 1882 & 1905 (Schmidt discovers thrombin, Bizzozero discovers living blood platelets in Turin, and Morawitz maps the 4-factor clotting cascade)", "hold_s": 3.8}),
            ("02_bizzozero_1882_platelet_plug_and_morawitz_1905_four_factor_enzymatic_amplification_chart", 79.5, 8.0, "E", False, "1882 GIULIO BIZZOZERO (LIVING-VESSEL PLATELET PLUG) & 1905 PAUL MORAWITZ (4-FACTOR THROMBOPLASTIN-PROTHROMBIN-THROMBIN-FIBRIN CASCADE)", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked Giulio Bizzozero (1882 Virchows Archiv 90: 261–332) living-vessel platelet plug formation & Paul Morawitz (1905 Ergebnisse der Physiologie 4: 307–422) 4-factor enzymatic amplification cascade (Thromboplastin + Ca²⁺ → Prothrombin → Thrombin → Fibrinogen to insoluble Fibrin mesh).",
             {"kind": "DATA", "label": "1882 BIZZOZERO (VIRCHOWS ARCHIV PLATELET PLUG) & 1905 MORAWITZ (4-FACTOR THROMBIN-FIBRIN ENZYMATIC AMPLIFICATION CASCADE)", "detail": "Inked Giulio Bizzozero (1882 Virchows Archiv 90: 261–332) living-vessel platelet plug formation & Paul Morawitz (1905 Ergebnisse der Physiologie 4: 307–422) 4-factor enzymatic amplification cascade (Thromboplastin + Ca²⁺ → Prothrombin → Thrombin → Fibrinogen to insoluble Fibrin mesh) on period paper", "scale": "the clotting cascade works like an avalanche on a mountainside — one triggered molecule at the cut activates ten, ten activate a hundred, and within two minutes a single microscopic nick weaves millions of fibrin threads to lock the platelet dam solid", "hold_s": 3.8}),
            ("03_turin_1882_brass_microscope_slide_and_virchows_archiv_platelet_fibrin_drawing_closeup", 87.5, 6.5, "B", False, "1882 — BIZZOZERO DISCOVERS PLATELETS", "Fast",
             "Fast: daylight macro shot of Giulio Bizzozero's 1882 brass microscope stage holding a glass slide beside his Virchows Archiv illustration of spiky platelets and fibrin strands on an oak table. Nothing emissive, no face.",
             STYLE + "In crisp daylight on an 1882 Turin workbench, a brass microscope with a glass slide sits beside an open scientific journal showing inked illustrations of blood platelets and fibrin threads." + FAST_TAIL,
             None),
            ("04_cutaway_vessel_model_showing_discoid_platelets_sprouting_arms_and_fibrin_mesh_cables_pan", 94.0, 5.5, "C", False, "1882 & 1905 — PLATELET DAM & FIBRIN NET", "Fast",
             "Fast: daylight close-up pan across a sculpted anatomical model of a blood vessel wall where disc-shaped platelets lock into a plug wrapped in golden fibrin cables trapping red blood cells on an oak table. Nothing emissive, no face.",
             STYLE + "In bright window light on an oak table, a sculpted cutaway blood-vessel model shows pale platelet discs piled across a wall breach and bound tightly by golden fibrin mesh strands." + FAST_TAIL,
             None),
        ],
    ),
    (
        3,
        "Part 03 — 1916 & 1929–1935: Medical Student Jay McLean's Accidental Heparin & Henrik Dam's Vitamin K — Midpoint Twist",
        [
            ("01_jay_mclean_and_william_howell_1916_johns_hopkins_heparin_and_henrik_dam_1935_copenhagen_vitamin_k", 99.5, 6.5, "A", False, "CLOT HUNT FOUND BLOOD THINNER", "Quality",
             "Quality: readable faces (25-year-old American medical student Jay McLean and physiologist William Henry Howell at Johns Hopkins in 1916 watching a beaker of fresh blood mixed with aged liver extract refuse to clot, dissolving to Danish biochemist Henrik Dam in Copenhagen in 1929–1935 and American biochemist Edward Doisy isolating Vitamin K).",
             STYLE + "Split period scene: on the left in 1916 Baltimore, young medical student Jay McLean holds up a tilted glass beaker of liquid unclotted blood before Professor William Howell; on the right in 1935 Copenhagen, Henrik Dam examines green leafy extracts and prothrombin test tubes." + QUAL_TAIL,
             {"kind": "FACT", "label": "Clot hunt found blood thinner", "who_card": "Edward Adelbert Doisy (1893–1986) — American biochemist", "when_stamp": "1916 · 1918 · 1929 · 27 April 1935 · 1943", "timeline_step": "2/3 · 1916 & 1929–1935 (Medical student Jay McLean and William Howell at Johns Hopkins discover the anticoagulant heparin, and Henrik Dam in Copenhagen discovers Vitamin K)", "hold_s": 3.8}),
            ("02_jay_mclean_1916_heparin_clotting_time_and_henrik_dam_1935_vitamin_k_prothrombin_chart", 106.0, 8.0, "E", False, "1916 JAY MCLEAN (AM. J. PHYSIOL.: LIVER HEPARIN ANTICOAGULANT) & 27 APR 1935 HENRIK DAM (NATURE: VITAMIN K KOAGULATIONSVITAMIN)", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked Jay McLean (1916 Am. J. Physiol. 41: 250–257) heparphosphatide/heparin coagulation time curve (aged liver extract extending blood clotting time from 3–5 minutes to infinity) alongside Henrik Dam's (27 April 1935 Nature 135: 652–653) Vitamin K prothrombin restoration chart.",
             {"kind": "DATA", "label": "1916 JAY MCLEAN (HEPARIN CLOTTING INHIBITION CURVE) & 27 APR 1935 HENRIK DAM (NATURE: VITAMIN K PROTHROMBIN RESTORATION)", "detail": "Inked Jay McLean (1916 Am. J. Physiol. 41: 250–257) heparphosphatide/heparin coagulation time curve (aged liver extract extending blood clotting time from 3–5 minutes to infinity) alongside Henrik Dam's (27 April 1935 Nature 135: 652–653) Vitamin K prothrombin restoration chart on period paper", "scale": "Jay McLean went into the laboratory hunting for the accelerator pedal of blood clotting and accidentally discovered the emergency brake — heparin boosts your blood's natural anti-clotting shield a thousand times over", "hold_s": 3.8}),
            ("03_johns_hopkins_1916_heparin_beakers_and_copenhagen_1935_nature_vitamin_k_issue_closeup", 114.0, 6.5, "B", False, "1916 & 1935 — HEPARIN & VITAMIN K", "Fast",
             "Fast: daylight macro shot of Jay McLean's 1916 Johns Hopkins glass beakers of liquid vs clotted blood and liver-extract vials beside Henrik Dam's 27 April 1935 issue of Nature and green alfalfa leaves on a bench. Nothing emissive, no face.",
             STYLE + "In crisp daylight on a physiology bench, glass beakers and amber vials of liver extract sit beside fresh green alfalfa leaves and an open 1935 scientific journal." + FAST_TAIL,
             None),
            ("04_antithrombin_heparin_brake_vs_vitamin_k_liver_carboxylation_teaching_model_pan", 120.5, 5.5, "C", False, "HEPARIN THE EMERGENCY BRAKE, VITAMIN K THE CLOTTING IGNITION KEY", "Fast",
             "Fast: daylight close-up pan across a sculpted molecular teaching model comparing heparin locking antithrombin onto thrombin scissors versus Vitamin K arming prothrombin Gla-domain hooks on an oak table. Nothing emissive, no face.",
             STYLE + "In bright window light on an oak table, a sculpted molecular model shows a heparin chain clamping thrombin scissors shut beside a Vitamin K key fitting into a liver prothrombin model." + FAST_TAIL,
             None),
        ],
    ),
    (
        4,
        "Part 04 — February 1933–1955: Karl Paul Link's Blizzard Milk Can, Dicoumarol & Warfarin (From Rat Poison to President Eisenhower)",
        [
            ("01_karl_paul_link_and_harold_campbell_1933_blizzard_milk_can_to_28_jun_1939_dicoumarol_crystals", 126.0, 6.5, "A", False, "RAT POISON SAVED A PRESIDENT", "Quality",
             "Quality: readable faces (Wisconsin farmer Ed Carlson pouring unclotted cow's blood from a milk can onto Karl Paul Link's lab floor in February 1933, and biochemist Harold Campbell crystallising dicoumarol needles under a microscope at dawn on 28 June 1939, dissolving to compound #42 Warfarin in 1948 and President Eisenhower in September 1955).",
             STYLE + "Split period scene: on the left in February 1933 Madison, farmer Ed Carlson stands with his metal milk can and spoiled sweet clover hay beside Karl Paul Link; on the right at dawn on 28 June 1939, Harold Campbell and Karl Paul Link peer at crystalline dicoumarol needles on a microscope slide." + QUAL_TAIL,
             {"kind": "FACT", "label": "Rat poison saved a President", "who_card": "Harold A. Campbell (born 1913) — American biochemist", "when_stamp": "February 1933 · 28 June 1939 · 1941 · 1948 · April 1951 · September 1955", "timeline_step": "3/3 · Feb 1933 – Sep 1955 (Karl Paul Link and Harold Campbell isolate dicoumarol on 28 June 1939, patent Warfarin #42 in 1948, and see it treat President Eisenhower in September 1955)", "hold_s": 3.8}),
            ("02_link_campbell_stahmann_huebner_1940_1948_coumarin_to_dicoumarol_and_warfarin_42_vkor_chart", 132.5, 8.0, "E", False, "28 JUN 1939–1948 LINK & CAMPBELL (J. BIOL. CHEM.: MOULDY CLOVER COUMARIN → DICOUMAROL → WARFARIN #42 VITAMIN K EPOXIDE REDUCTASE BLOCK)", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked Karl Paul Link, Harold Campbell, Mark Stahmann & Charles Huebner (1940–1948; J. Biol. Chem. 138: 21–33 & Circulation 1959 19: 97–107) sweet clover coumarin → mould-oxidized dicoumarol → compound #42 Warfarin structure & Vitamin K epoxide reductase inhibition chart.",
             {"kind": "DATA", "label": "1939–1948 KARL PAUL LINK & HAROLD CAMPBELL: COUMARIN → DICOUMAROL → WARFARIN #42 & VITAMIN K EPOXIDE REDUCTASE INHIBITION CHART", "detail": "Inked Karl Paul Link, Harold Campbell, Mark Stahmann & Charles Huebner (1940–1948; J. Biol. Chem. 138: 21–33 & Circulation 1959 19: 97–107) sweet clover coumarin → mould-oxidized dicoumarol → compound #42 Warfarin structure & Vitamin K epoxide reductase inhibition chart on period paper", "scale": "fresh sweet clover smells like vanilla and cannot thin a single drop of blood — it takes mould in a damp barn to weld two of those vanilla-scented coumarin molecules together into a counterfeit Vitamin K key that stops the liver from arming blood clots", "hold_s": 3.8}),
            ("03_madison_1939_dicoumarol_crystal_slide_1948_warf_42_patent_and_1955_coumadin_bottle_closeup", 140.5, 6.5, "B", False, "1939–1955 — LINK ISOLATES DICOUMAROL & WARFARIN", "Fast",
             "Fast: daylight macro shot of Harold Campbell and Karl Paul Link's 28 June 1939 crystalline dicoumarol slide beside the 1948 WARF compound #42 patent sheet and a 1955 bottle of Coumadin Warfarin tablets on a bench. Nothing emissive, no face.",
             STYLE + "In crisp daylight on a Madison biochemistry bench, a glass slide of white dicoumarol crystals sits beside dried sweet clover stems, a 1948 patent sheet, and an amber tablet bottle." + FAST_TAIL,
             None),
            ("04_explorer_watching_mould_weld_two_coumarin_rings_into_warfarin_key_and_holding_vitamin_k_antidote_key", 147.0, 5.5, "B", True, None, "Quality",
             "Quality: Explorer beat 2 (locked character reference).",
             STYLE + "Inside a brass liver-factory workshop, the Explorer watches two single coumarin ring keys join into a twin Warfarin key that blocks a prothrombin stamping machine, while holding up a golden Vitamin K antidote key that unlocks it." + EXP_TAIL,
             None),
        ],
    ),
    (
        5,
        "Part 05 — The Clotting Tightrope That Saves Millions — & How a Darkened Room in Cairo Proved Your Eyes See Upside Down",
        [
            ("01_timeline_1882_1955_and_coagulation_platelets_heparin_vitamin_k_warfarin_chart", 152.5, 8.5, "E", False, "1882–1955 TIMELINE · BIZZOZERO PLATELETS, MORAWITZ FIBRIN, MCLEAN HEPARIN, DAM VITAMIN K & LINK WARFARIN", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, the 3-era timeline completes: 1872, 1882 & 1905 (Alexander Schmidt discovers thrombin, Giulio Bizzozero discovers living blood platelets in Turin, and Paul Morawitz maps the four-factor clotting cascade) · 1916 & 1929–1935 (Medical student Jay McLean and William Howell at Johns Hopkins discover the anticoagulant heparin, and Henrik Dam in Copenhagen discovers Vitamin K) · Feb 1933 – Sep 1955 (Karl Paul Link and Harold Campbell in Madison isolate dicoumarol from spoiled sweet clover hay after Ed Carlson's blizzard drive, patent Warfarin in 1948, and see it treat President Eisenhower in September 1955).",
             {"kind": "DATA", "label": "1882–1955 BLOOD CLOTTING, HEPARIN, VITAMIN K & WARFARIN TIMELINE · BIZZOZERO, MORAWITZ, MCLEAN, DAM & KARL PAUL LINK", "detail": "Animated timeline (1882 → 1955) alongside an inked summary of platelet plug formation, the thrombin-fibrin cascade, heparin, Vitamin K, and Warfarin", "scale": "from a medical student whose liver extract refused to clot and chicks bleeding in Copenhagen to a milk can of cow's blood in a Wisconsin blizzard, scientists mastered the life-and-death balance of human blood", "when_stamp": "1882–1955", "timeline_step": "3/3 · 1882–1955 timeline complete", "hold_s": 3.8}),
            ("02_blood_vessel_coagulation_model_beside_brass_spectacles_and_eye_model_on_plinth_pan", 161.0, 5.5, "A", False, "PLATELETS, HEPARIN, VITAMIN K & WARFARIN", "Fast",
             "Fast: daylight close-up of a sculpted blood-vessel platelet-and-fibrin model beside a cutaway anatomical human eye model and a pair of brass spectacles on a wooden museum plinth. Nothing emissive, no face.",
             STYLE + "In crisp daylight on a wooden museum plinth, a sculpted blood-vessel clotting model sits beside a cutaway anatomical eye model and a pair of vintage brass spectacles." + FAST_TAIL,
             None),
            ("03_ibn_al_haytham_1011_cairo_camera_obscura_kepler_1604_ox_eye_young_1801_and_snellen_1862_eye_chart_handoff", 166.5, 6.5, "C", False, "CAMERA OBSCURA, UPSIDE-DOWN RETINA & 20/20 GLASSES", "Quality",
             "Quality: readable faces (Ibn al-Haytham in his darkened pinhole room in Cairo in 1011 AD alongside Johannes Kepler in 1604 and Christoph Scheiner in 1619 watching an upside-down candle flame on the back of a peeled ox eye, Thomas Young in 1801, and Herman Snellen in 1862 with the 20/20 eye chart — handoff to 083 Eyes, Glasses & Optics).",
             STYLE + "Split period scene: on the left in 1011 AD Cairo, Ibn al-Haytham points to inverted light spots on the wall of his pinhole camera obscura; on the right in 1604 Prague and 1862 Utrecht, Johannes Kepler traces inverted retinal rays beside Herman Snellen pointing to a wall eye chart." + QUAL_TAIL,
             {"kind": "WHEN", "label": "1011 AD · 1604 · 1801 · 1862", "hold_s": 3.5}),
            ("04_table_three_callback", 173.0, 2.4, "C", False, None, "reuse",
             "Reuse: verified unused moving window [5.50s..7.90s] of P1:07_table_three_props_1882_bizzozero_microscope_1916_mclean_heparin_beaker_and_1933_carlson_milk_can (callback, £0).",
             "Reuse P1:07_table_three_props_1882_bizzozero_microscope_1916_mclean_heparin_beaker_and_1933_carlson_milk_can [5.50s..7.90s] (2.40s distinct non-overlapping tail window from 8.00s source clip).",
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
                row["reuse_of"] = "P1:07_table_three_props_1882_bizzozero_microscope_1916_mclean_heparin_beaker_and_1933_carlson_milk_can"
                row["reuse_window_s"] = [5.5, 7.9]
                row["reuse_audit"] = {
                    "source_row": "P1:07_table_three_props_1882_bizzozero_microscope_1916_mclean_heparin_beaker_and_1933_carlson_milk_can",
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
            "film": "082_Bizzozero-Morawitz-McLean-Dam-Link-Blood-Clotting-Warfarin",
            "part": p_idx,
            "title": p_title,
            "version": "v01",
            "timing_status": "pre_vo_script_clock (built from blood_clotting_script_master_v01.md; retimes onto Scribe STT once VO locks)",
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
        "film": "082_Bizzozero-Morawitz-McLean-Dam-Link-Blood-Clotting-Warfarin",
        "version": "v01",
        "date": "2026-10-20",
        "owner": "gemini (J0738)",
        "status": "PRE_VO_BOARDS_V01_NO_MINT",
        "generation_authorized": False,
        "script": "00_Brand/Channel-Setup/ideas/082_Bizzozero-Morawitz-McLean-Dam-Link-Blood-Clotting-Warfarin/blood_clotting_script_master_v01.md",
        "sources": "00_Brand/Channel-Setup/ideas/082_Bizzozero-Morawitz-McLean-Dam-Link-Blood-Clotting-Warfarin/SOURCES_v01.md",
        "credit_snapshot": {
            "flow_balance": 23740,
            "flow_floor": 0,
            "flow_read_at": "2026-10-15T21:42:22Z",
            "vertex_promo_gbp": 71.02,
            "vertex_usable_gbp": 70.02,
        },
        "totals": totals,
        "per_part": per_part_summary,
        "mint_order": "006 > 007 > 008 > 009 > 010 > 011 > 012 > 013 > 014 > 015 > 016 > 017 > 018 > 019 > 020 > 021 > 022 > 023 > 024 > 025 > 026 > 027 > 028 > 029 > 030 > 031 > 032 > 033 > 034 > 035 > 036 > 037 > 038 > 039 > 040 > 041 > 042 > 043 > 044 > 045 > 046 > 047 > 048 > 049 > 050 > 051 > 052 > 053 > 054 > 055 > 056 > 057 > 058 > 059 > 060 > 061 > 062 > 063 > 064 > 065 > 066 > 067 > 068 > 069 > 070 > 071 > 072 > 073 > 074 > 075 > 076 > 077 > 078 > 079 > 080 > 081 > 082 > 083. Nothing in 082 is generation_authorized.",
    }
    (EDIT / "PICTURE_PLAN_v01.json").write_text(json.dumps(plan, indent=2) + "\n")

    sl = [
        "# 082 Warfarin: How Rat Poison Saved Millions of Lives — Shot list & plate boards v01 (pre-VO)",
        "",
        "Gemini, 20 Oct 2026, J0738. Built from `blood_clotting_script_master_v01.md` (`91.0/100 PASS`) and `SOURCES_v01.md`.",
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
        "# 082 price review v01 (pre-VO plate boards)",
        "",
        "Gemini, 20 Oct 2026, J0738. Boards only. **No mint. No spend. No merge.**",
        "Prepared from `blood_clotting_script_master_v01.md` (`91.0/100 PASS`) and `SOURCES_v01.md` so 082's full plate board rows, non-emissive Fast prompts, £0 code graphics, and Teach-on-Screen overlays are ready to re-time the moment long VO locks. Parked for Chief.",
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
        f"- **Quality ({totals['Quality']} rows):** readable faces (Giulio Bizzozero, Alexander Schmidt, Paul Morawitz, Jay McLean, William Henry Howell, Henrik Dam, Edward Adelbert Doisy, Karl Paul Link, Harold A. Campbell, Ed Carlson, Dwight D. Eisenhower, Ibn al-Haytham, Johannes Kepler, Herman Snellen), 1882 Turin living-vessel `platelet` discovery & 1905 `thrombin-fibrin` cascade, 1916 Baltimore `heparin` discovery & 1929–1935 Copenhagen `Vitamin K` discovery, February 1933 Madison blizzard milk can to 28 June 1939 `dicoumarol` crystals & September 1955 `Warfarin` recovery, and the 2 Explorer beats.",
        f"- **Fast ({totals['Fast']} rows, non-emissive):** daylight prop and laboratory shots (1882 *Virchows Archiv* platelet lithograph, heparin vial & sweet clover stems pan, 3-object callback bench, 1882 Turin brass microscope & platelet-fibrin drawing, sculpted blood-vessel platelet plug & fibrin mesh model, 1916 Johns Hopkins unclotted vs clotted blood beakers & 27 April 1935 *Nature* issue with green alfalfa leaves, sculpted heparin-antithrombin vs Vitamin K molecular model, 1939 Madison dicoumarol crystal slide with 1948 WARF #42 patent & Coumadin bottle, sculpted blood-vessel clotting model beside anatomical eye model and brass spectacles on museum plinth). Zero candles, flames, sparks, or glowing elements on Fast.",
        f"- **£0 code graphics ({totals['code_graphic']} rows):**",
        "  1. `P1:04_bizzozero_1882_morawitz_1905_mclean_1916_dam_1935_and_link_1941_coagulation_warfarin_chart` — Bizzozero (1882) `15M platelets/drop`, Morawitz (1905) 4-factor cascade (`Thromboplastin + Ca²⁺ → Prothrombin → Thrombin → Fibrin`), McLean (1916) `heparin`, and Dam/Link `Vitamin K` vs `Warfarin` (`SCALE: a single drop of your blood holds fifteen million microscopic platelet discs waiting like deflated life rafts — the instant a vessel wall rips, they inflate spiky arms in less than a second and pile into a sandbag dam before a net of fibrin steel cables locks them solid`)",
        "  2. `P1:06_karl_paul_link_and_harold_campbell_28_jun_1939_sweet_clover_coumarin_to_dicoumarol_warfarin_chart` — Karl Paul Link & Harold Campbell (1939–1948) `dicoumarol`/`Warfarin` plasma prothrombin curve & reversal by `Vitamin K` (`SCALE: Warfarin and Vitamin K are molecular lookalikes — Warfarin slips into the liver's clotting-factor factory like a counterfeit key that jams the lock, and giving a patient a dose of real Vitamin K pops the counterfeit key right back out`)",
        "  3. `P2:02_bizzozero_1882_platelet_plug_and_morawitz_1905_four_factor_enzymatic_amplification_chart` — Giulio Bizzozero (1882 *Virchows Archiv*) living-vessel platelet plug + Paul Morawitz (1905) 4-factor enzymatic amplification cascade (`SCALE: the clotting cascade works like an avalanche on a mountainside — one triggered molecule at the cut activates ten, ten activate a hundred, and within two minutes a single microscopic nick weaves millions of fibrin threads to lock the platelet dam solid`)",
        "  4. `P3:02_jay_mclean_1916_heparin_clotting_time_and_henrik_dam_1935_vitamin_k_prothrombin_chart` — Jay McLean (1916 *Am. J. Physiol.*) liver `heparin` clotting inhibition curve & Henrik Dam (27 April 1935 *Nature*) `Vitamin K` prothrombin restoration (`SCALE: Jay McLean went into the laboratory hunting for the accelerator pedal of blood clotting and accidentally discovered the emergency brake — heparin boosts your blood's natural anti-clotting shield a thousand times over`)",
        "  5. `P4:02_link_campbell_stahmann_huebner_1940_1948_coumarin_to_dicoumarol_and_warfarin_42_vkor_chart` — Link, Campbell, Stahmann & Huebner (1940–1948) sweet clover `coumarin` → mould-oxidized `dicoumarol` → `#42 Warfarin` & Vitamin K epoxide reductase inhibition (`SCALE: fresh sweet clover smells like vanilla and cannot thin a single drop of blood — it takes mould in a damp barn to weld two of those vanilla-scented coumarin molecules together into a counterfeit Vitamin K key that stops the liver from arming blood clots`)",
        "  6. `P5:01_timeline_1882_1955_and_coagulation_platelets_heparin_vitamin_k_warfarin_chart` — completed timeline (1882 → 1955) + platelets, thrombin-fibrin cascade, heparin, Vitamin K & Warfarin (`SCALE: from a medical student whose liver extract refused to clot and chicks bleeding in Copenhagen to a milk can of cow's blood in a Wisconsin blizzard, scientists mastered the life-and-death balance of human blood`)",
        f"- **£0 verified reuse ({totals['reuse']} row):** `P5:04_table_three_callback` uses the 2.40 s unused moving tail `[5.50s..7.90s]` of `P1:07_table_three_props_1882_bizzozero_microscope_1916_mclean_heparin_beaker_and_1933_carlson_milk_can`.",
        "",
        "## Mint order",
        "",
        "006 > 007 > 008 > 009 > 010 > 011 > 012 > 013 > 014 > 015 > 016 > 017 > 018 > 019 > 020 > 021 > 022 > 023 > 024 > 025 > 026 > 027 > 028 > 029 > 030 > 031 > 032 > 033 > 034 > 035 > 036 > 037 > 038 > 039 > 040 > 041 > 042 > 043 > 044 > 045 > 046 > 047 > 048 > 049 > 050 > 051 > 052 > 053 > 054 > 055 > 056 > 057 > 058 > 059 > 060 > 061 > 062 > 063 > 064 > 065 > 066 > 067 > 068 > 069 > 070 > 071 > 072 > 073 > 074 > 075 > 076 > 077 > 078 > 079 > 080 > 081 > 082 > 083. `generation_authorized` is `false` on every row.",
    ])
    (EDIT / "PRICE_REVIEW_v01.md").write_text("\n".join(pr_lines) + "\n")
    print(f"082 v01 boards written: {totals['rows']} rows, Flow expected={totals['flow_credits_expected']}")


if __name__ == "__main__":
    main()
