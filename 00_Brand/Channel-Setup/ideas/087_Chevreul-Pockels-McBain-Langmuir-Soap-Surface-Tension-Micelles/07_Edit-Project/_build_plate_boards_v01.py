#!/usr/bin/env python3
"""HOS 087 (Soap: How a Kitchen Sink Unlocked Surface Tension) pre-VO plate boards v01. J0805. No mint, no spend.

Built from 00_Brand/Channel-Setup/ideas/087_Chevreul-Pockels-McBain-Langmuir-Soap-Surface-Tension-Micelles/soap_micelles_script_master_v01.md
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
        "Part 01 — Greasy Hands, the 1891 Kitchen-Sink Trough & the Two-Faced Molecule That Rips Viruses Apart",
        [
            ("01_water_beads_on_oil_amphiphilic_soap_micelles_and_agnes_pockels_1891_brunswick_kitchen_sink_trough", 0.0, 5.5, "A", False, "KITCHEN SINK & SOAP MICELLES", "Quality",
             "Quality: Short frame 0 / answer image (0:03) + side by side, pure water droplets bead up and roll off golden cooking oil on a human hand until two-faced amphiphilic soap molecules plunge their hydrophobic tails into the oil and viral lipid envelopes to trap them inside spherical micelles, beside Agnes Pockels at her kitchen sink in Brunswick, Germany on 12 March 1891 sliding a tin strip across her 70-cm rectangular tin trough while measuring water surface tension with a 6-mm porcelain button on a balance beam.",
             STYLE + "Split chemical-and-historical scene: on the left, two-faced pin-shaped soap molecules plunge their oily tails into golden grease droplets on a hand and snap into spherical micelles; on the right in 1891 Brunswick, Agnes Pockels stands at her kitchen sink sliding a tin strip across a 70-cm rectangular tin water trough with a suspended porcelain button balance." + QUAL_TAIL,
             {"kind": "WHEN", "label": "BRUNSWICK, 12 MARCH 1891", "timeline_step": "1/3 · 1823 & 12 March 1891 (Michel Eugène Chevreul in Paris proves fat saponification, and 19-year-old Agnes Pockels in Brunswick measures water surface tension and surface films at her kitchen sink with a 70-cm tin trough and porcelain button)", "hold_s": 3.5}),
            ("02_chevreul_1823_paris_pockels_1891_rayleigh_and_mcbain_1913_langmuir_blodgett_1917_1935_split", 5.5, 6.0, "B", False, "FAT SOAP, TIN TROUGH, MICELLES", "Quality",
             "Quality: complex three-part composition (Michel Eugène Chevreul in Paris in 1823 splitting animal fat with alkali into glycerin and fatty-acid soap salts; Agnes Pockels in Brunswick in 1881–1891 writing to Lord Rayleigh with her kitchen-sink surface-tension trough; and James William McBain at Bristol in 1913 unveiling spherical soap micelles alongside Irving Langmuir and Katharine Blodgett at General Electric in 1917–1935 measuring one-molecule-thick monolayers).",
             STYLE + "Three-panel period composition: on the left in 1823 Paris, Michel Eugène Chevreul separates tallow fat and alkali into soap and glycerin; in the centre in 1891 Brunswick, Agnes Pockels operates her tin trough at a kitchen sink beside Lord Rayleigh; on the right in 1913–1935, James McBain, Irving Langmuir, and Katharine Blodgett examine a spherical soap micelle model and monolayer trough." + QUAL_TAIL,
             None),
            ("03_polar_water_72_8_mnm_surface_tension_skin_vs_soap_crowbars_rupturing_grease_and_viral_envelope", 11.5, 6.0, "C", False, "WATER BEADS vs SOAP CROWBARS", "Quality",
             "Quality: complex physical-and-virological reveal (a split comparison of polar water molecules clinging together in a tight hydrogen-bonded skin at 72.8 mN/m that refuses to mix with oil, vs pin-shaped soap molecules wedging their oil-loving tails into a grease droplet and into the lipid bilayer envelope of a virus to pry it apart in 20 seconds).",
             STYLE + "In a split molecular comparison, on the left pure water droplets bead tightly on top of an oily film; on the right, pin-shaped soap molecules wedge their tails into a grease droplet and into a spherical viral lipid envelope, prying the coat apart and trapping the fragments inside micelles." + QUAL_TAIL,
             {"kind": "WHEN", "label": "1823 · 12 MARCH 1891 · 1913 · 1917 · 1935", "timeline_step": "1/3 · 1823 & 12 Mar 1891 (Chevreul & Pockels) · 2/3 · 1913 (McBain micelles) · 3/3 · 1917–1935 (Langmuir & Blodgett monolayers)", "hold_s": 3.5}),
            ("04_chevreul_1823_pockels_1891_surface_tension_and_langmuir_1917_2_5nm_monolayer_chart", 17.5, 8.0, "E", False, "POCKELS (1891): SOAP DROPS WATER SURFACE TENSION FROM 72.8 TO ~25 MN/M & LANGMUIR (1917): ~2.5-NM SINGLE-MOLECULE MONOLAYER", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked Saponification, Surface Tension, Micelle Self-Assembly & Monolayer chart from Michel Eugène Chevreul (1823 Recherches chimiques sur les corps gras d'origine animale), Agnes Pockels (12 March 1891 Nature 43: 437–439), James William McBain (1913 Trans. Faraday Soc. 9: 99–101), and Irving Langmuir (1917 J. Am. Chem. Soc. 39: 1848–1906) shows 1) Chevreul's triglyceride fat + 3 NaOH alkali → glycerol + 3 sodium stearate soap molecules; 2) Pockels's 70-cm tin trough showing pure water surface tension (72.8 mN/m) dropping sharply below 30 mN/m as a soap/oil film compresses; and 3) McBain's spherical micelles & Langmuir's ~2.5-nm single-molecule monolayer.",
             {"kind": "DATA", "label": "1891 AGNES POCKELS SURFACE TENSION DROP (72.8 → ~25 MN/M) & 1917 IRVING LANGMUIR ~2.5-NM MONOLAYER CHART", "detail": "Inked Agnes Pockels (1891) water surface tension drop (pure water 72.8 mN/m vs soapy water ~25 mN/m) & Irving Langmuir (1917) ~2.5-nanometre single-molecule fatty-acid monolayer chart on period paper", "scale": "a single soap film standing on water is just two and a half nanometres tall — thirty thousand times thinner than a sheet of kitchen foil — yet that one-molecule-thick carpet cuts water's surface tension by nearly two-thirds", "who_cards": [
                 "Michel Eugène Chevreul (1786–1889) — French chemist",
                 "Agnes Luise Wilhelmine Pockels (1862–1935) — German pioneer of surface science",
                 "John William Strutt, Lord Rayleigh (1842–1919) — British physicist",
                 "James William McBain (1882–1953) — Canadian-American physical chemist",
                 "Irving Langmuir (1881–1957) — American chemist and physicist",
                 "Katharine Burr Blodgett (1898–1979) — American physicist and chemist",
             ], "when_stamp": "1823 · 12 March 1891 · 1913 · 1917 · 1935", "hold_s": 3.8}),
            ("05_chevreul_1823_book_marseille_soap_block_and_pockels_1891_nature_paper_pan", 25.5, 5.5, "A", False, "TWO-FACED SOAP MOLECULES", "Fast",
             "Fast: daylight close-up pan across Michel Eugène Chevreul's 1823 treatise on animal fats, a block of olive-oil soap, and the 12 March 1891 issue of Nature on an oak table. Nothing emissive, no face.",
             STYLE + "In warm window light on an oak table, an open 1823 French chemistry volume sits beside a stamped block of Marseille soap, a glass flask of glycerin, and an open 1891 scientific journal." + FAST_TAIL,
             None),
            ("06_mcbain_1913_cmc_conductivity_curve_and_5nm_amphiphilic_soap_micelle_virus_chart", 31.0, 8.0, "E", False, "BRISTOL & SCHENECTADY, 1913–1917", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period parchment, an inked James William McBain (1913 Trans. Faraday Soc. 9: 99–101) Amphiphilic Soap Micelle & Viral Lipid Envelope Disruption diagram shows 50–100 sodium stearate molecules snapping into a spherical micelle above the critical micelle concentration (CMC), with hydrophobic C17H35 hydrocarbon tails pointing inward to trap oil or viral membrane lipids and hydrophilic -COO-Na+ heads facing outward into water.",
             {"kind": "DATA", "label": "1913 JAMES WILLIAM MCBAIN CRITICAL MICELLE CONCENTRATION (CMC) & 50–100 MOLECULE (~5-NM) SPHERICAL MICELLE CHART", "detail": "Inked McBain (1913) critical micelle concentration (CMC) conductivity curve & 50–100 soap molecules per ~5-nm spherical micelle on period paper", "scale": "a single drop of soapy water contains more than ten quadrillion microscopic micelles — each one a five-nanometre molecular cage with an oily inside that swallows grease and a water-loving outside that washes straight down the sink", "hold_s": 3.8}),
            ("07_table_three_props_1823_soap_flasks_1891_tin_trough_button_balance_and_1913_micelle_model", 39.0, 5.5, "C", False, "1823 TO 1935", "Fast",
             "Fast: daylight pan across three period props on a wooden bench: Chevreul's 1823 saponification flasks of tallow and glycerin, Agnes Pockels's 70-cm rectangular tin trough with its 6-mm porcelain button balance, and McBain's 1913 spherical soap micelle model (also provides 2.40s tail window [5.50s..7.90s] for P5:04 callback). Nothing emissive, no face.",
             STYLE + "In soft daylight on a laboratory bench, glass flasks of tallow fat and soap crystals sit beside a 70-cm rectangular tin water trough with a suspended porcelain button balance and a painted wooden model of a spherical soap micelle." + FAST_TAIL,
             None),
            ("08_explorer_sliding_tin_barrier_across_pockels_trough_packing_soap_monolayer_into_micelle_spheres", 62.0, 5.5, "A", True, None, "Quality",
             "Quality: Explorer beat 1 (locked character reference, after 1:00).",
             STYLE + "Standing beside a giant sculpted rectangular tin water trough, the Explorer slides a tin strip across the water surface to pack two-faced soap pins upright into a neat single-molecule carpet, then swirls the water so the soap pins snap into spherical micelles around a golden oil drop." + EXP_TAIL,
             None),
            ("09_agnes_pockels_10_jan_1891_brunswick_kitchen_sink_writing_letter_to_lord_rayleigh", 67.5, 5.5, "B", False, "BRUNSWICK, 10 JANUARY 1891", "Quality",
             "Quality: readable face (in Brunswick on 10 January 1891, Agnes Pockels writes her letter to Lord Rayleigh beside her 70-cm tin trough and 6-mm porcelain button balance at her kitchen sink).",
             STYLE + "In an 1891 Brunswick kitchen, Agnes Pockels sits beside her copper-and-stone kitchen sink where a 70-cm tin water trough and a small balance beam holding a 6-mm white porcelain button rest next to her handwritten letter to Lord Rayleigh." + QUAL_TAIL,
             {"kind": "WHEN", "label": "BRUNSWICK, 10 JANUARY 1891", "timeline_step": "1/3 · 1823 & 12 March 1891 (Chevreul's saponification proof & Agnes Pockels's kitchen-sink surface-tension trough published in Nature with Lord Rayleigh)", "hold_s": 3.5}),
        ],
    ),
    (
        2,
        "Part 02 — 1823 & 12 March 1891: Michel Eugène Chevreul's Saponification Proof & How 19-Year-Old Agnes Pockels Built the First Surface-Tension Trough at Her Kitchen Sink",
        [
            ("01_chevreul_1823_paris_fat_saponification_and_agnes_pockels_1891_kitchen_sink_button_trough", 73.0, 6.5, "A", False, "KITCHEN SINK MEASURED FILMS", "Quality",
             "Quality: readable faces (French chemist Michel Eugène Chevreul in Paris in 1823 isolating stearic and oleic fatty acids and glycerin from animal tallow during alkali saponification, dissolving to Agnes Pockels at her Brunswick kitchen sink in 1881–12 March 1891 measuring water surface tension with her 70-cm tin trough and 6-mm porcelain button balance and Lord Rayleigh reading her letter).",
             STYLE + "Split period scene: on the left in 1823 Paris, Michel Eugène Chevreul holds up crystal flasks of stearic acid and glycerol beside a soap kettle; on the right in 1891 Brunswick, Agnes Pockels measures water surface tension with a porcelain button touching her tin trough." + QUAL_TAIL,
             {"kind": "FACT", "label": "Kitchen sink measured films", "who_card": "Nicolas Leblanc (1742–1806) — French chemist and surgeon", "when_stamp": "1791 · 1813 · 1823 · 1881 · 10 January 1891 · 12 March 1891", "timeline_step": "1/3 · 1823 & 12 March 1891 (Chevreul proves fats are triglyceride esters split by alkali into soap and glycerin; Agnes Pockels invents the surface-tension trough at her kitchen sink)", "hold_s": 3.8}),
            ("02_chevreul_1823_triglyceride_saponification_and_pockels_1891_70cm_tin_trough_isotherm_chart", 79.5, 8.0, "E", False, "1823 CHEVREUL (TRIGLYCERIDE + 3 NAOH → GLYCEROL + 3 SOAP SALTS) & 12 MAR 1891 AGNES POCKELS (NATURE: 70-CM TROUGH & 6-MM BUTTON)", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked Michel Eugène Chevreul (1823) triglyceride fat + 3 NaOH saponification equation & Agnes Pockels (12 March 1891 Nature 43: 437–439) 70-cm tin trough & 6-mm button balance surface-tension compression curve.",
             {"kind": "DATA", "label": "1823 CHEVREUL SAPONIFICATION EQUATION & 12 MAR 1891 AGNES POCKELS (NATURE 43: 437) 70-CM TIN TROUGH COMPRESSION CURVE", "detail": "Inked Michel Eugène Chevreul (1823) triglyceride fat + 3 NaOH saponification equation & Agnes Pockels (12 March 1891 Nature 43: 437–439) 70-cm tin trough & 6-mm button balance surface-tension compression curve on period paper", "scale": "Agnes Pockels had no laboratory, no university salary, and no scientific instruments — just a seventy-centimetre tin pan, a six-millimetre coat button, and a kitchen sink — yet her measurements were so accurate that Nobel laureates used her exact trough design for the next hundred years", "hold_s": 3.8}),
            ("03_brunswick_and_london_12_mar_1891_nature_surface_tension_paper_and_tin_trough_closeup", 87.5, 6.5, "B", False, "1823 & 1891 — CHEVREUL, POCKELS & RAYLEIGH", "Fast",
             "Fast: daylight macro shot of Agnes Pockels's 12 March 1891 Nature paper 'Surface Tension' introduced by Lord Rayleigh beside her 70-cm tin trough, movable tin strip, and 6-mm porcelain button scale on a wooden table. Nothing emissive, no face.",
             STYLE + "In crisp daylight on a wooden table, an open 1891 scientific journal sits beside a rectangular tin water trough, a movable tin barrier strip, and a wooden balance arm holding a small white porcelain button." + FAST_TAIL,
             None),
            ("04_wooden_scale_beam_lifting_6mm_porcelain_button_from_clean_vs_soapy_water_meniscus_pan", 94.0, 5.5, "C", False, "MEASURING THE SKIN OF WATER WITH A COAT BUTTON", "Fast",
             "Fast: daylight close-up pan across a 6-mm white porcelain button suspended from a brass balance thread pulling up a tall water meniscus on clean water versus releasing easily on soapy water in a tin trough. Nothing emissive, no face.",
             STYLE + "In bright window light, a close-up shows a 6-mm white porcelain button hanging from a fine thread on a balance beam touching the clean water meniscus inside a tin trough." + FAST_TAIL,
             None),
        ],
    ),
    (
        3,
        "Part 03 — 1913: 'McBain's Nonsense!' & How Two-Faced Soap Molecules Snap Into Grease-Trapping Micelles — Midpoint Twist",
        [
            ("01_james_mcbain_1913_bristol_soap_conductivity_and_george_hartley_1936_spherical_micelles", 99.5, 6.5, "A", False, "MCBAIN'S NONSENSE PROVED TRUE", "Quality",
             "Quality: readable faces (Canadian physical chemist James William McBain at the University of Bristol in 1913 presenting electrical conductivity and osmotic pressure proof of colloidal soap micelles while a sceptical chemist scoffs, dissolving to George Stafford Hartley in 1936 demonstrating the spherical micelle model).",
             STYLE + "Split period scene: on the left in 1913 Bristol, James William McBain points to a conductivity bridge and a spherical cluster of pin-shaped soap molecules before a startled committee; on the right in 1936 London, George Stafford Hartley holds a cutaway model of a spherical micelle with oily tails inward and water-loving heads outward." + QUAL_TAIL,
             {"kind": "FACT", "label": "McBain's nonsense proved true", "who_card": "George Stafford Hartley (1909–1997) — British physical chemist", "when_stamp": "1913 · 1936", "timeline_step": "2/3 · 1913 & 1936 (James William McBain at Bristol discovers spherical soap micelles, and George Stafford Hartley maps their hydrophobic-inward, hydrophilic-outward sphere)", "hold_s": 3.8}),
            ("02_mcbain_1913_trans_faraday_soc_conductivity_osmotic_anomaly_and_5nm_micelle_self_assembly_chart", 106.0, 8.0, "E", False, "1913 JAMES WILLIAM MCBAIN (TRANS. FARADAY SOC.): CRITICAL MICELLE CONCENTRATION (CMC) & 50–100 MOLECULE SPHERICAL MICELLE", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked James William McBain (1913 Trans. Faraday Soc. 9: 99–101) soapy water electrical conductivity vs osmotic pressure anomaly & 50–100 amphiphilic soap molecules self-assembling above the Critical Micelle Concentration (CMC) into a ~5-nm grease-trapping spherical micelle.",
             {"kind": "DATA", "label": "1913 MCBAIN (TRANS. FARADAY SOC. 9: 99): CONDUCTIVITY VS OSMOTIC PRESSURE ANOMALY & ~5-NM SPHERICAL SOAP MICELLE CHART", "detail": "Inked James William McBain (1913 Trans. Faraday Soc. 9: 99–101) soapy water electrical conductivity vs osmotic pressure anomaly & 50–100 amphiphilic soap molecules self-assembling above the Critical Micelle Concentration (CMC) into a ~5-nm grease-trapping spherical micelle on period paper", "scale": "each soap molecule is like a tiny magnet with two opposite personalities — an oil-loving tail and a water-loving head — so fifty to a hundred of them team up into a microscopic sphere that hides a drop of grease on the inside while wearing a water-friendly disguise on the outside", "hold_s": 3.8}),
            ("03_bristol_1913_faraday_society_paper_conductivity_cell_and_cutaway_micelle_model_closeup", 114.0, 6.5, "B", False, "1913 — MCBAIN DISCOVERS SOAP MICELLES", "Fast",
             "Fast: daylight macro shot of James McBain's 1913 Transactions of the Faraday Society paper beside a glass conductivity cell with platinum electrodes and a cutaway wooden model of a spherical soap micelle trapping an oil droplet on a bench. Nothing emissive, no face.",
             STYLE + "In crisp daylight on a 1913 Bristol laboratory bench, an open chemistry journal sits beside a glass conductivity cell with brass terminals and a painted cutaway sphere of pin-shaped soap molecules enclosing a yellow oil core." + FAST_TAIL,
             None),
            ("04_anatomical_model_of_hydrophobic_tails_burying_into_oil_drop_and_lifting_off_skin_pan", 120.5, 5.5, "C", False, "HOW MICELLES LIFT GREASE INTO WATER", "Fast",
             "Fast: daylight close-up pan across a three-stage tabletop teaching model showing amphiphilic soap pins planting their tails into a grease droplet on skin, curling it into a spherical micelle, and floating free into water. Nothing emissive, no face.",
             STYLE + "In bright window light on an oak table, a three-stage physical teaching model shows pin-shaped soap molecules surrounding a golden grease drop and lifting it off a surface inside a spherical micelle cage." + FAST_TAIL,
             None),
        ],
    ),
    (
        4,
        "Part 04 — 1917–1935: Irving Langmuir & Katharine Blodgett's One-Molecule-Thick Films & Why 20 Seconds of Soap Shatters Viruses",
        [
            ("01_irving_langmuir_1917_and_katharine_blodgett_1935_ge_monolayer_trough_and_soap_rupturing_virus", 126.0, 6.5, "A", False, "SOAP CROWBARS RUPTURE VIRUSES", "Quality",
             "Quality: readable faces (American chemist Irving Langmuir in 1917 and physicist Katharine Burr Blodgett in 1935 at General Electric compressing a single-molecule fatty-acid monolayer on the Langmuir-Pockels trough to measure its ~2.5-nm height and 0.21-nm2 cross-section and depositing non-reflective glass coatings, alongside amphiphilic soap tails wedging into a viral lipid bilayer envelope during a 20-second handwash).",
             STYLE + "Split period scene: on the left at General Electric in 1917–1935, Irving Langmuir and Katharine Blodgett measure a single-molecule film on a Langmuir-Pockels water trough and dip a clear glass lens; on the right, pin-shaped soap molecules wedge their tails into a viral lipid envelope and pry it apart." + QUAL_TAIL,
             {"kind": "FACT", "label": "Soap crowbars rupture viruses", "when_stamp": "1917 · 1931 · 1935", "timeline_step": "3/3 · 1917–1935 (Irving Langmuir and Katharine Blodgett at General Electric prove surface films are one-molecule-thick monolayers and build non-reflective glass coatings)", "hold_s": 3.8}),
            ("02_langmuir_1917_jacs_pressure_area_isotherm_0_21nm2_2_5nm_and_20s_viral_lipid_envelope_disruption_chart", 132.5, 8.0, "E", False, "1917 IRVING LANGMUIR (JACS: 0.21 NM² CROSS-SECTION & ~2.5 NM HEIGHT) & 20-SECOND VIRAL LIPID ENVELOPE RUPTURE", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked Irving Langmuir (1917 J. Am. Chem. Soc. 39: 1848–1906) Langmuir-Pockels trough pressure-area isotherm (cross-sectional area ~0.21 nm2/molecule, height ~2.5 nm) & 20-second amphiphilic soap tail disruption of viral lipid bilayer envelopes.",
             {"kind": "DATA", "label": "1917 LANGMUIR (JACS 39: 1848) MONOLAYER ISOTHERM (0.21 NM² AREA, ~2.5 NM HEIGHT) & 20-SECOND VIRAL ENVELOPE RUPTURE CHART", "detail": "Inked Irving Langmuir (1917 J. Am. Chem. Soc. 39: 1848–1906) Langmuir-Pockels trough pressure-area isotherm (cross-sectional area ~0.21 nm2/molecule, height ~2.5 nm) & 20-second amphiphilic soap tail disruption of viral lipid bilayer envelopes on period paper", "scale": "by spreading a single drop of oil across Agnes Pockels's water trough and measuring the rectangle with an ordinary ruler, Irving Langmuir measured the height of a single molecule to within a billionth of a metre — and proved why twenty seconds of soap wedges open the fatty armour of a virus like a crowbar", "hold_s": 3.8}),
            ("03_schenectady_1917_jacs_paper_langmuir_blodgett_film_balance_and_1935_invisible_glass_closeup", 140.5, 6.5, "B", False, "1917–1935 — LANGMUIR & BLODGETT'S MONOLAYERS", "Fast",
             "Fast: daylight macro shot of Irving Langmuir's 1917 Journal of the American Chemical Society paper beside a brass Langmuir-Blodgett film-dipping mechanism and a half-coated non-reflective glass plate on a laboratory bench. Nothing emissive, no face.",
             STYLE + "In crisp daylight on a 1935 General Electric bench, an open chemistry journal sits beside a precision brass film-dipping trough and a glass lens frame showing crystal-clear anti-reflective coated glass." + FAST_TAIL,
             None),
            ("04_explorer_prying_open_viral_lipid_bilayer_envelope_with_amphiphilic_soap_crowbar_into_micelles", 147.0, 5.5, "B", True, None, "Quality",
             "Quality: Explorer beat 2 (locked character reference).",
             STYLE + "Standing beside a giant sculpted enveloped virus wrapped in a two-layered fatty lipid shell, the Explorer wedges the oily tail of a two-faced soap molecule bar into the fatty seam so the shell pops apart and curls into harmless spherical micelle cages." + EXP_TAIL,
             None),
        ],
    ),
    (
        5,
        "Part 05 — From a Kitchen Sink to Single Molecules — & Why Removing One Starfish Collapses an Entire Ecosystem",
        [
            ("01_timeline_1823_1935_and_saponification_pockels_trough_soap_micelles_langmuir_monolayers_chart", 152.5, 8.5, "E", False, "1823–1935 TIMELINE · CHEVREUL SAPONIFICATION, POCKELS KITCHEN TROUGH, MCBAIN MICELLES & LANGMUIR-BLODGETT MONOLAYERS", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, the 3-era timeline completes: 1823 (Michel Eugène Chevreul in Paris proves animal fats are triglyceride esters and explains how alkali saponification creates fatty-acid soap salts and glycerin) · 12 March 1891 (19-year-old Agnes Pockels in Brunswick measures water surface tension and surface films at her kitchen sink with a 70-cm tin trough and porcelain button, publishing in Nature with Lord Rayleigh) · 1913 & 1917–1935 (James William McBain at Bristol discovers spherical soap micelles, and Irving Langmuir and Katharine Blodgett at General Electric prove surface films are monolayers one molecule thick).",
             {"kind": "DATA", "label": "1823–1935 SOAP, SURFACE TENSION & MICELLES TIMELINE · CHEVREUL, POCKELS, RAYLEIGH, MCBAIN, LANGMUIR & BLODGETT", "detail": "Animated timeline (1823 → 1935) alongside an inked summary of fat saponification, Agnes Pockels's kitchen-sink trough, spherical soap micelles, and single-molecule monolayers", "scale": "from a Paris soap kettle and a German kitchen sink to single-molecule camera coatings and twenty-second virus-shattering handwashing, scientists proved that the most powerful chemistry in your home sits right beside your tap", "when_stamp": "1823–1935", "timeline_step": "3/3 · 1823–1935 timeline complete", "hold_s": 3.8}),
            ("02_pockels_tin_trough_and_soap_micelle_model_beside_purple_starfish_and_crowbar_on_plinth_pan", 161.0, 5.5, "A", False, "SAPONIFICATION, MONOLAYERS & MICELLES", "Fast",
             "Fast: daylight close-up of Agnes Pockels's rectangular tin trough and a spherical soap micelle model beside a sculpted purple ochre starfish and steel crowbar on a wooden museum plinth. Nothing emissive, no face.",
             STYLE + "In crisp daylight on a wooden museum plinth, a rectangular tin surface-tension trough and a cutaway soap micelle sphere sit beside a sculpted purple five-armed starfish and an iron crowbar." + FAST_TAIL,
             None),
            ("03_elton_1927_lindeman_1942_10_percent_pyramid_carson_1962_and_paine_1963_keystone_starfish_handoff", 166.5, 6.5, "C", False, "FOOD WEBS, 10% LAW & KEYSTONE STARFISH", "Quality",
             "Quality: readable faces (Charles Elton in 1927 mapping Arctic food webs, Raymond Lindeman at Cedar Bog Lake in October 1942 proving the 10% trophic energy law, Rachel Carson in September 1962 exposing DDT biomagnification in Silent Spring, and Robert Paine at Mukkaw Bay in June 1963 prying purple Pisaster starfish off the rocks with a crowbar — handoff to 088 Food Webs & Keystone Species).",
             STYLE + "Split period scene: on the left in 1927–1942, Charles Elton and Raymond Lindeman map a four-tier 10% ecological energy pyramid; on the right in June 1963 on a rocky Washington tidepool coast, ecologist Robert Paine pries a purple ochre starfish off a mussel-covered ledge with a crowbar." + QUAL_TAIL,
             {"kind": "WHEN", "label": "1927 · 1942 · 1962 · JUNE 1963", "hold_s": 3.5}),
            ("04_table_three_callback", 173.0, 2.4, "C", False, None, "reuse",
             "Reuse: verified unused moving window [5.50s..7.90s] of P1:07_table_three_props_1823_soap_flasks_1891_tin_trough_button_balance_and_1913_micelle_model (callback, £0).",
             "Reuse P1:07_table_three_props_1823_soap_flasks_1891_tin_trough_button_balance_and_1913_micelle_model [5.50s..7.90s] (2.40s distinct non-overlapping tail window from 8.00s source clip).",
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
                row["reuse_of"] = "P1:07_table_three_props_1823_soap_flasks_1891_tin_trough_button_balance_and_1913_micelle_model"
                row["reuse_window_s"] = [5.5, 7.9]
                row["reuse_audit"] = {
                    "source_row": "P1:07_table_three_props_1823_soap_flasks_1891_tin_trough_button_balance_and_1913_micelle_model",
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
            "film": "087_Chevreul-Pockels-McBain-Langmuir-Soap-Surface-Tension-Micelles",
            "part": p_idx,
            "title": p_title,
            "version": "v01",
            "timing_status": "pre_vo_script_clock (built from soap_micelles_script_master_v01.md; retimes onto Scribe STT once VO locks)",
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
        "film": "087_Chevreul-Pockels-McBain-Langmuir-Soap-Surface-Tension-Micelles",
        "version": "v01",
        "date": "2026-10-21",
        "owner": "gemini (J0805)",
        "status": "PRE_VO_BOARDS_V01_NO_MINT",
        "generation_authorized": False,
        "script": "00_Brand/Channel-Setup/ideas/087_Chevreul-Pockels-McBain-Langmuir-Soap-Surface-Tension-Micelles/soap_micelles_script_master_v01.md",
        "sources": "00_Brand/Channel-Setup/ideas/087_Chevreul-Pockels-McBain-Langmuir-Soap-Surface-Tension-Micelles/SOURCES_v01.md",
        "credit_snapshot": {
            "flow_balance": 23740,
            "flow_floor": 0,
            "flow_read_at": "2026-10-15T21:42:22Z",
            "vertex_promo_gbp": 71.02,
            "vertex_usable_gbp": 70.02,
        },
        "totals": totals,
        "per_part": per_part_summary,
        "mint_order": "006 > 007 > 008 > 009 > 010 > 011 > 012 > 013 > 014 > 015 > 016 > 017 > 018 > 019 > 020 > 021 > 022 > 023 > 024 > 025 > 026 > 027 > 028 > 029 > 030 > 031 > 032 > 033 > 034 > 035 > 036 > 037 > 038 > 039 > 040 > 041 > 042 > 043 > 044 > 045 > 046 > 047 > 048 > 049 > 050 > 051 > 052 > 053 > 054 > 055 > 056 > 057 > 058 > 059 > 060 > 061 > 062 > 063 > 064 > 065 > 066 > 067 > 068 > 069 > 070 > 071 > 072 > 073 > 074 > 075 > 076 > 077 > 078 > 079 > 080 > 081 > 082 > 083 > 084 > 085 > 086 > 087 > 088 > 089 > 090 > 091 > 092 > 093 > 094 > 095. Nothing in 087 is generation_authorized.",
    }
    (EDIT / "PICTURE_PLAN_v01.json").write_text(json.dumps(plan, indent=2) + "\n")

    sl = [
        "# 087 Soap: How a Kitchen Sink Unlocked Surface Tension — Shot list & plate boards v01 (pre-VO)",
        "",
        "Gemini, 21 Oct 2026, J0805. Built from `soap_micelles_script_master_v01.md` (`91.4/100 PASS`) and `SOURCES_v01.md`.",
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
        "# 087 price review v01 (pre-VO plate boards)",
        "",
        "Gemini, 21 Oct 2026, J0805. Boards only. **No mint. No spend. No merge.**",
        "Prepared from `soap_micelles_script_master_v01.md` (`91.4/100 PASS`) and `SOURCES_v01.md` so 087's full plate board rows, non-emissive Fast prompts, £0 code graphics, and Teach-on-Screen overlays are ready to re-time the moment long VO locks. Parked for Chief.",
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
        f"- **Quality ({totals['Quality']} rows):** readable faces (Michel Eugène Chevreul, Agnes Luise Wilhelmine Pockels, John William Strutt / Lord Rayleigh, James William McBain, George Stafford Hartley, Irving Langmuir, Katharine Burr Blodgett, Charles Elton, Raymond Lindeman, Rachel Carson, Robert Paine), 1823 Paris fat saponification & 12 March 1891 Brunswick kitchen-sink surface-tension trough, 1913 Bristol soap micelle discovery, 1917–1935 General Electric single-molecule monolayers & 20-second viral lipid envelope disruption, and the 2 Explorer beats.",
        f"- **Fast ({totals['Fast']} rows, non-emissive):** daylight prop and laboratory shots (Chevreul's 1823 treatise, Marseille soap block & 1891 *Nature* issue pan, 3-object callback bench, 12 March 1891 *Nature* paper with Pockels's 70-cm tin trough & 6-mm button balance, porcelain button lifting water meniscus in clean vs soapy water, 1913 *Trans. Faraday Soc.* paper with conductivity cell & cutaway micelle model, 3-stage tabletop micelle grease-lifting demonstrator, 1917 *JACS* paper with Langmuir-Blodgett trough & 1935 anti-reflective glass lens, Pockels tin trough & micelle model beside purple starfish & crowbar on museum plinth). Zero candles, flames, sparks, or glowing elements on Fast.",
        f"- **£0 code graphics ({totals['code_graphic']} rows):**",
        "  1. `P1:04_chevreul_1823_pockels_1891_surface_tension_and_langmuir_1917_2_5nm_monolayer_chart` — Agnes Pockels (1891) water surface tension drop (`72.8 mN/m` → `~25 mN/m`) & Irving Langmuir (1917) `~2.5-nm` single-molecule fatty-acid monolayer chart (`SCALE: a single soap film standing on water is just two and a half nanometres tall — thirty thousand times thinner than a sheet of kitchen foil — yet that one-molecule-thick carpet cuts water's surface tension by nearly two-thirds`)",
        "  2. `P1:06_mcbain_1913_cmc_conductivity_curve_and_5nm_amphiphilic_soap_micelle_virus_chart` — James William McBain (1913) Critical Micelle Concentration (`CMC`) conductivity curve & `50–100` soap molecules per `~5-nm` spherical micelle (`SCALE: a single drop of soapy water contains more than ten quadrillion microscopic micelles — each one a five-nanometre molecular cage with an oily inside that swallows grease and a water-loving outside that washes straight down the sink`)",
        "  3. `P2:02_chevreul_1823_triglyceride_saponification_and_pockels_1891_70cm_tin_trough_isotherm_chart` — Michel Eugène Chevreul (1823) triglyceride + `3 NaOH` saponification equation & Agnes Pockels (12 March 1891 *Nature* 43: 437–439) `70-cm` tin trough & `6-mm` button balance compression curve (`SCALE: Agnes Pockels had no laboratory, no university salary, and no scientific instruments — just a seventy-centimetre tin pan, a six-millimetre coat button, and a kitchen sink — yet her measurements were so accurate that Nobel laureates used her exact trough design for the next hundred years`)",
        "  4. `P3:02_mcbain_1913_trans_faraday_soc_conductivity_osmotic_anomaly_and_5nm_micelle_self_assembly_chart` — James William McBain (1913 *Trans. Faraday Soc.* 9: 99–101) conductivity vs osmotic pressure anomaly & `50–100` amphiphilic soap molecules self-assembling into a `~5-nm` spherical micelle (`SCALE: each soap molecule is like a tiny magnet with two opposite personalities — an oil-loving tail and a water-loving head — so fifty to a hundred of them team up into a microscopic sphere that hides a drop of grease on the inside while wearing a water-friendly disguise on the outside`)",
        "  5. `P4:02_langmuir_1917_jacs_pressure_area_isotherm_0_21nm2_2_5nm_and_20s_viral_lipid_envelope_disruption_chart` — Irving Langmuir (1917 *J. Am. Chem. Soc.* 39: 1848–1906) Langmuir-Pockels trough pressure-area isotherm (`~0.21 nm²` cross-section, `~2.5 nm` height) & 20-second viral lipid envelope disruption chart (`SCALE: by spreading a single drop of oil across Agnes Pockels's water trough and measuring the rectangle with an ordinary ruler, Irving Langmuir measured the height of a single molecule to within a billionth of a metre — and proved why twenty seconds of soap wedges open the fatty armour of a virus like a crowbar`)",
        "  6. `P5:01_timeline_1823_1935_and_saponification_pockels_trough_soap_micelles_langmuir_monolayers_chart` — completed timeline (1823 → 1935) + saponification, Agnes Pockels's kitchen-sink trough, spherical micelles & single-molecule monolayers (`SCALE: from a Paris soap kettle and a German kitchen sink to single-molecule camera coatings and twenty-second virus-shattering handwashing, scientists proved that the most powerful chemistry in your home sits right beside your tap`)",
        f"- **£0 verified reuse ({totals['reuse']} row):** `P5:04_table_three_callback` uses the 2.40 s unused moving tail `[5.50s..7.90s]` of `P1:07_table_three_props_1823_soap_flasks_1891_tin_trough_button_balance_and_1913_micelle_model`.",
        "",
        "## Mint order",
        "",
        "006 > 007 > 008 > 009 > 010 > 011 > 012 > 013 > 014 > 015 > 016 > 017 > 018 > 019 > 020 > 021 > 022 > 023 > 024 > 025 > 026 > 027 > 028 > 029 > 030 > 031 > 032 > 033 > 034 > 035 > 036 > 037 > 038 > 039 > 040 > 041 > 042 > 043 > 044 > 045 > 046 > 047 > 048 > 049 > 050 > 051 > 052 > 053 > 054 > 055 > 056 > 057 > 058 > 059 > 060 > 061 > 062 > 063 > 064 > 065 > 066 > 067 > 068 > 069 > 070 > 071 > 072 > 073 > 074 > 075 > 076 > 077 > 078 > 079 > 080 > 081 > 082 > 083 > 084 > 085 > 086 > 087 > 088 > 089 > 090 > 091 > 092 > 093 > 094 > 095. `generation_authorized` is `false` on every row.",
    ])
    (EDIT / "PRICE_REVIEW_v01.md").write_text("\n".join(pr_lines) + "\n")
    print(f"087 v01 boards written: {totals['rows']} rows, Flow expected={totals['flow_credits_expected']}")


if __name__ == "__main__":
    main()
