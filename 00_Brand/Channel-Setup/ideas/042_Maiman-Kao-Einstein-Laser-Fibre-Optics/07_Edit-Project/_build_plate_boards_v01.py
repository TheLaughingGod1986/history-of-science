#!/usr/bin/env python3
"""HOS 042 (Lasers & Fibre Optics: The Pink Ruby That Built the Internet) pre-VO plate boards v01. J0540. No mint, no spend.

Built from 00_Brand/Channel-Setup/ideas/042_Maiman-Kao-Einstein-Laser-Fibre-Optics/laser_script_master_v01.md
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
        "Part 01 — The Fingertip Ruby in Malibu and the Glass Thread Under the Ocean",
        [
            ("01_maiman_16_may_1960_malibu_ruby_laser_and_kao_1966_harlow_optical_fibre", 0.0, 5.5, "A", False, "RUBY LASER TO INTERNET", "Quality",
             "Quality: Short frame 0 / answer image (0:03) + inside Hughes Research Laboratories in Malibu, California, on 16 May 1960, 32-year-old physicist Theodore Maiman slips a 1-centimetre pink synthetic ruby rod inside a coiled xenon photographer's flashlamp and fires the first deep-red 694.3-nanometre laser beam, transitioning into pulses of light racing through an undersea glass optical fibre studied by Charles Kao in Harlow, England, in January 1966.",
             STYLE + "Inside a 1960 California physics lab, thirty-two-year-old physicist Theodore Maiman holds a miniature cylindrical housing where a coiled quartz flashlamp surrounds a pink ruby crystal firing a razor-sharp red beam, transitioning to engineer Charles Kao in England inspecting a clear silica glass thread." + QUAL_TAIL,
             {"kind": "WHEN", "label": "MALIBU, 16 MAY 1960 · HARLOW, JANUARY 1966", "timeline_step": "4/6 · 16 May 1960 (Theodore Maiman fires the first 694.3 nm synthetic pink ruby laser in Malibu) & 5/6 · Jan–Jul 1966 (Charles Kao & George Hockham prove <20 dB/km purified silica glass fibres can carry laser signals)", "hold_s": 3.5}),
            ("02_einstein_1917_photon_paper_maiman_1960_ruby_coil_and_kao_1966_fibre_split", 5.5, 6.0, "B", False, "1917 QUANTUM, 1960 RUBY, 1966 FIBRE", "Quality",
             "Quality: complex three-part split composition (Albert Einstein's 1917 Berlin quantum paper showing stimulated emission on the left; Theodore Maiman's 16 May 1960 coiled flashlamp and silvered ruby rod in the centre; Charles Kao's 1966 total-internal-reflection glass fibre diagram on the right).",
             STYLE + "Three-panel period composition: on the left, an open physics manuscript beside a brass atomic model; in the centre, a pink synthetic ruby cylinder nested inside a helical quartz lamp; on the right, a spool of hair-thin clear silica glass fibre on a laboratory bench." + QUAL_TAIL,
             None),
            ("03_maiman_and_dhaenens_16_may_1960_malibu_wiring_flashlamp_and_ruby_rod", 11.5, 6.0, "C", False, "16 MAY 1960", "Quality",
             "Quality: readable faces (inside Hughes Research Laboratories on 16 May 1960, Theodore Maiman and assistant Irnee D'Haenens wire a high-voltage power supply to a helical xenon flashlamp wrapped around a 1 cm by 2 cm silver-coated pink synthetic ruby cylinder).",
             STYLE + "Inside Hughes Research Laboratories in Malibu in May 1960, physicist Theodore Maiman and assistant Irnee D'Haenens connect leads to an aluminium cylinder housing a pink ruby rod and coiled xenon flash tube." + QUAL_TAIL,
             {"kind": "WHEN", "label": "MALIBU, 16 MAY 1960", "timeline_step": "4/6 · 16 May 1960 (Theodore Maiman fires the first laser at Hughes Labs in Malibu)", "hold_s": 3.5}),
            ("04_einstein_1917_maiman_694nm_ruby_and_kao_1000_to_0_2_db_km_fibre_chart", 17.5, 8.0, "E", False, "1917 STIMULATED EMISSION → 16 MAY 1960 RUBY (694.3 NM) → 1966–1979 FIBRE (1,000 TO 0.2 DB/KM)", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked comparison chart contrasts ordinary torchlight (incoherent waves spreading wide) vs Maiman's 16 May 1960 ruby laser (coherent 694.3 nm waves in lockstep) and 1960s optical glass (1,000 dB/km attenuation, losing 99% of light in 20 m) vs Charles Kao's 1966 target (<20 dB/km) and modern silica fibre (0.2 dB/km, carrying 99% of intercontinental internet data at ~200,000 km/s).",
             {"kind": "DATA", "label": "694.3 NM COHERENT RUBY LASER · GLASS LOSS: 1,000 DB/KM (1960) → <20 DB/KM (KAO 1966) → 0.2 DB/KM", "detail": "Inked comparison chart on period paper contrasting ordinary torchlight (incoherent waves of many wavelengths spreading wide) vs Maiman's 16 May 1960 ruby laser (single 694.3-nanometre wavelength, coherent waves in lockstep) and 1960s optical glass (1,000 dB/km attenuation, losing 99% of light in 20 metres) vs Charles Kao's 1966 target (<20 dB/km) and modern silica fibre (0.2 dB/km, carrying 99% of intercontinental internet data at ~200,000 km/s)", "scale": "ordinary glass in nineteen sixty swallowed ninety-nine percent of a light beam in just twenty metres — the length of a cricket pitch — whereas today's purified glass fibres carry a laser pulse a hundred kilometres without losing the signal", "who_card": "Albert Einstein (1879–1955) — German-born theoretical physicist · Theodore Maiman (1927–2007) — American physicist · Charles Kao (1933–2018) — Shanghai-born electrical engineer", "when_stamp": "1917 · 16 May 1960 · January 1966", "hold_s": 3.8}),
            ("05_pink_synthetic_ruby_boule_silvered_rod_and_unlit_xenon_coil_pan", 25.5, 5.5, "A", False, "MALIBU, 1960", "Fast",
             "Fast: daylight macro pan across a pink synthetic ruby boule, a 1 cm by 2 cm silvered pink ruby cylinder, and an unlit helical quartz flash tube on a wooden optics bench between code graphics so two full-frame graphics never run back to back. Nothing emissive, no face.",
             STYLE + "In crisp daylight on a wooden optics bench, the camera pans smoothly across a faceted pink synthetic ruby crystal, a small silver-tipped pink cylinder, and an unlit coiled quartz tube." + FAST_TAIL,
             None),
            ("06_human_hair_100um_vs_single_mode_optical_fibre_9um_core_99_percent_internet_chart", 31.0, 8.0, "E", False, "THINNER THAN A HAIR", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period parchment, an inked scale and bandwidth bar compares a 100-micrometre human hair to a 9-micrometre single-mode optical fibre core (125-micrometre cladding) carrying terabits of laser data per second across 99% of transoceanic internet routes.",
             {"kind": "DATA", "label": "100 µM HUMAN HAIR VS 9 µM OPTICAL FIBRE CORE (99% OF TRANSOCEANIC INTERNET TRAFFIC)", "detail": "Inked scale & bandwidth bar comparing a 100-micrometre human hair to a 9-micrometre optical fibre core carrying terabits of laser data per second across 99% of transoceanic internet routes", "scale": "the glass core guiding this video across the ocean floor is just nine micrometres wide — ten times thinner than a single strand of your hair", "hold_s": 3.8}),
            ("07_table_three_props_gould_notebook_maiman_ruby_cylinder_kao_silica_spool", 39.0, 5.5, "C", False, "1917 TO 1970", "Fast",
             "Fast: daylight prop table (callback source for Part 05: Gordon Gould's notarised leather notebook, Theodore Maiman's 1 cm by 2 cm pink ruby cylinder inside an unlit quartz coil, and Charles Kao's spool of ultra-pure silica glass fibre). Nothing emissive.",
             STYLE + "On an oak laboratory bench in soft window light sit three objects side by side: a leather-bound notebook with an embossed brass seal, a small pink ruby cylinder beside a coiled quartz tube, and a brass spool wound with clear glass thread." + FAST_TAIL,
             None),
            ("08_explorer_sliding_silvered_pink_ruby_in_front_of_torch_into_glass_rod", 62.0, 5.5, "A", True, None, "Quality",
             "Quality: Explorer beat 1 (locked character reference, after 1:00).",
             STYLE + "Standing at a wooden optics bench where a brass lamp scatters wide rays, the Explorer slides a tiny silver-ended pink ruby cylinder in front of the lamp and smiles in delight as a single narrow red beam shoots straight into a curved glass rod." + EXP_TAIL,
             None),
            ("09_charles_kao_january_1966_harlow_measuring_fused_quartz_attenuation", 67.5, 5.5, "B", False, "HARLOW, JANUARY 1966", "Quality",
             "Quality: readable face (in Harlow, England, in January 1966, 32-year-old electrical engineer Charles Kao peers into a spectrophotometer measuring light loss through a thin rod of fused quartz glass).",
             STYLE + "Inside a 1966 British telecommunications laboratory in Harlow, thirty-two-year-old engineer Charles Kao in a white lab coat over a tie adjusts a brass optical bench holding a clear fused-quartz rod." + QUAL_TAIL,
             None),
        ],
    ),
    (
        2,
        "Part 02 — Einstein's 1917 Twin Photon & the Candy-Store Notebook That Named the 'LASER'",
        [
            ("01_einstein_1917_berlin_study_and_gould_13_nov_1957_bronx_candy_store_notary", 73.0, 6.5, "A", False, "NOTARISED IN A CANDY STORE", "Quality",
             "Quality: readable faces (Albert Einstein writing quantum radiation equations in Berlin in 1916–1917, dissolving to 37-year-old Columbia graduate student Gordon Gould having his notebook page titled 'LASER' stamped by a notary in a Bronx candy store on 13 November 1957 alongside Charles Townes's 1954 ammonia maser).",
             STYLE + "Split period scene: on the left in a 1917 Berlin study, physicist Albert Einstein writes equations with a fountain pen; on the right in a 1957 New York candy shop, graduate student Gordon Gould watches a shopkeeper press a brass notary seal onto his open notebook." + QUAL_TAIL,
             {"kind": "WHO", "label": "Charles Townes (1915–2015) — American physicist · Gordon Gould (1920–2005) — American physics graduate student", "fact_card": "Notarised in a candy store", "when_stamp": "1916 · 1917 · 1954 · 13 November 1957 · December 1958", "timeline_step": "2/6 · 1917 (Albert Einstein predicts stimulated emission) & 3/6 · 13 Nov 1957–1958 (Gordon Gould coins 'LASER' in a notarised notebook; Townes & Schawlow publish optical maser theory)", "hold_s": 3.8}),
            ("02_einstein_1917_stimulated_emission_2_to_n_cascade_and_mirror_cavity_chart", 79.5, 8.0, "E", False, "1917 STIMULATED EMISSION (1 → 2 → 4 → 2^N PHOTONS IN LOCKSTEP) + PARALLEL-MIRROR CAVITY", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked quantum cascade diagram shows Einstein's 1917 stimulated emission (1 photon → 2 → 4 → 8 → 2^n coherent photons in phase) inside a parallel-mirror optical cavity once population inversion (>50% of atoms in excited state) is reached.",
             {"kind": "DATA", "label": "1917 STIMULATED EMISSION: 1 PHOTON → 2 → 4 → 8 → 2^70 COHERENT WAVES IN PARALLEL-MIRROR CAVITY", "detail": "Inked quantum cascade diagram on period paper showing Einstein's 1917 stimulated emission (1 photon → 2 → 4 → 8 → 2^n coherent photons in phase) inside a parallel-mirror optical cavity once population inversion (>50% of atoms in excited state) is reached", "scale": "bounce a single photon back and forth between two mirrors just seventy times while triggering stimulated emission, and one particle of light multiplies into more than a sextillion identical waves marching in step", "hold_s": 3.8}),
            ("03_gould_13_nov_1957_notarised_notebook_and_brass_notary_embosser_closeup", 87.5, 6.5, "B", False, "13 NOVEMBER 1957 — 'LASER'", "Fast",
             "Fast: daylight macro shot of Gordon Gould's open leather laboratory notebook beside a heavy cast-iron notary seal press and a fountain pen on a wooden counter. Nothing emissive, no face.",
             STYLE + "In crisp daylight on a wooden counter, an open ruled notebook with a raised circular paper seal sits beside a cast-iron notary embosser and a black fountain pen." + FAST_TAIL,
             None),
            ("04_townes_1954_brass_ammonia_maser_cavity_and_parallel_optical_mirrors_pan", 94.0, 5.5, "C", False, "1954 MASER TO 1958 OPTICAL CAVITY", "Fast",
             "Fast: daylight close-up of a cylindrical brass microwave maser cavity beside a pair of parallel silvered optical mirrors mounted on a steel rail. Nothing emissive, no face.",
             STYLE + "In bright window light on a physics bench, a polished brass cylindrical chamber sits beside two round silvered glass mirrors mounted facing each other on a steel rail." + FAST_TAIL,
             None),
        ],
    ),
    (
        3,
        "Part 03 — 16 May 1960: Why Experts Said Pink Ruby Would Fail & How Theodore Maiman Won the Race — Midpoint Twist",
        [
            ("01_maiman_16_may_1960_firing_first_ruby_laser_and_schawlow_skepticism", 99.5, 6.5, "A", False, "PAPER REJECTED BY TOP JOURNAL", "Quality",
             "Quality: readable faces (32-year-old physicist Theodore Maiman on 16 May 1960 at Hughes Research Laboratories in Malibu firing the first 694.3 nm synthetic pink ruby laser while Arthur Schawlow shakes his head at a blackboard).",
             STYLE + "Inside the 1960 Malibu optics laboratory, physicist Theodore Maiman watches a deep-red laser beam shoot from a compact aluminium lamp housing onto a white target card while colleague Irnee D'Haenens checks an oscilloscope." + QUAL_TAIL,
             {"kind": "WHO", "label": "Arthur Schawlow (1921–1999) — American physicist", "fact_card": "Paper rejected by top journal", "when_stamp": "16 May 1960 · 6 August 1960 · 21 July 1969", "timeline_step": "4/6 · 16 May 1960 (Theodore Maiman fires the first laser using a flashlamp-pumped synthetic pink ruby at Hughes Labs in Malibu)", "hold_s": 3.8}),
            ("02_maiman_1960_ruby_70_percent_efficiency_and_694_3nm_spectral_narrowing_chart", 106.0, 8.0, "E", False, "16 MAY 1960 PINK RUBY (1×2 CM, ~70% EFFICIENCY VS 1% MYTH) → 694.3 NM LASER SPIKE", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked ruby-cavity and spectrum chart from Maiman (16 May 1960 / Nature 6 Aug 1960) shows the 1 cm × 2 cm pink ruby rod (0.05% Cr2O3 in Al2O3, ~70% fluorescence efficiency vs the mistaken 1% estimate) pumped above threshold (>950 V xenon flash) collapsing its red glow into a narrow, intense 694.3-nanometre laser spike.",
             {"kind": "DATA", "label": "16 MAY 1960 RUBY LASER: 1×2 CM ROD (~70% EFFICIENCY VS 1% MYTH) → 694.3 NM COHERENT SPIKE", "detail": "Inked ruby-cavity & spectrum chart on period paper from Maiman (16 May 1960 / Nature 6 Aug 1960) showing the 1 cm × 2 cm pink ruby rod (0.05% Cr2O3 in Al2O3, ~70% fluorescence efficiency vs the mistaken 1% estimate) pumped above threshold (>950 V xenon flash) collapsing its red glow into a narrow, intense 694.3-nanometre laser spike", "scale": "inside a pink ruby crystal no bigger than the tip of your little finger, Maiman unleashed a pulse of red light brighter than the surface of the Sun", "hold_s": 3.8}),
            ("03_apollo_11_21_july_1969_lunar_laser_retroreflector_mirror_array_on_moon", 114.0, 6.5, "B", False, "21 JULY 1969 — MOON MIRROR", "Quality",
             "Quality: complex period scene (on 21 July 1969 at Tranquility Base on the Moon, an Apollo 11 astronaut positions the suitcase-sized lunar laser ranging retroreflector array of 100 fused-silica corner-cube prisms aimed toward Earth).",
             STYLE + "On the grey lunar surface under a black sky, an Apollo astronaut in a white spacesuit tilts open a square panel studded with one hundred recessed glass corner prisms aimed toward a distant blue Earth." + QUAL_TAIL,
             None),
            ("04_disassembled_maiman_laser_parts_ruby_rod_xenon_helix_and_calipers_pan", 120.5, 5.5, "C", False, "1 CM × 2 CM PINK RUBY", "Fast",
             "Fast: daylight close-up of Theodore Maiman's disassembled laser components on velvet: the 1 cm by 2 cm silver-tipped pink ruby rod, brass vernier calipers, and the unlit helical quartz flashlamp. Nothing emissive, no face.",
             STYLE + "In crisp daylight on a dark velvet cloth, brass vernier calipers measure a small pink ruby cylinder beside a polished aluminium sleeve and an unlit helical quartz tube." + FAST_TAIL,
             None),
        ],
    ),
    (
        4,
        "Part 04 — Daniel Colladon's 1842 Glowing Water Fountain & Charles Kao's 1966 Pure-Glass Breakthrough",
        [
            ("01_colladon_1842_geneva_water_jet_and_kao_1966_harlow_silica_fibre_breakthrough", 126.0, 6.5, "A", False, "GUIDED LIGHT INSIDE A FOUNTAIN", "Quality",
             "Quality: readable faces (Swiss physicist Daniel Colladon in October 1842 in Geneva shining a sunbeam into a curving jet of pouring water, dissolving to 32-year-old engineer Charles Kao in January–July 1966 in Harlow measuring attenuation in fused silica glass rods).",
             STYLE + "Split period scene: on the left in an 1842 Geneva lecture hall, physicist Daniel Colladon directs a beam of sunlight through a lens into a curving stream of water; on the right in 1966 in England, engineer Charles Kao inspects a glowing glass fibre coil." + QUAL_TAIL,
             {"kind": "WHO", "label": "Daniel Colladon (1802–1893) — Swiss physicist and engineer", "fact_card": "Guided light inside a fountain", "when_stamp": "1842 · July 1966 · 2009", "timeline_step": "1/6 · 1842 (Daniel Colladon guides sunlight inside a curving water fountain in Geneva) & 5/6 · Jan–Jul 1966 (Charles Kao & George Hockham prove <20 dB/km purified silica glass fibres can carry laser communications)", "hold_s": 3.8}),
            ("02_kao_1966_and_corning_1970_1979_attenuation_drop_1000_to_0_2_db_km_chart", 132.5, 8.0, "E", False, "GLASS ATTENUATION: 1,000 DB/KM (1960) → 20 DB/KM (KAO 1966) → 17 DB/KM (1970) → 0.2 DB/KM (1979)", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked attenuation-drop chart from Kao & Hockham (1966) and Corning (1970–1979) shows 1960s optical glass (1,000 dB/km loss — 99% lost in 20 m) vs Charles Kao's 1966 target threshold (20 dB/km — 1% surviving 1,000 m), Corning's August 1970 titanium-doped silica fibre (17 dB/km), and modern 1,550 nm silica fibre (0.2 dB/km — >95% surviving 1 km).",
             {"kind": "DATA", "label": "OPTICAL FIBRE LOSS: 1,000 DB/KM (1960) → 20 DB/KM TARGET (KAO 1966) → 17 DB/KM (1970) → 0.2 DB/KM", "detail": "Inked attenuation-drop chart on period paper from Kao & Hockham (1966) and Corning (1970–1979) showing 1960s optical glass (1,000 dB/km loss — 99% lost in 20 m) vs Charles Kao's 1966 target threshold (20 dB/km — 1% surviving 1,000 m), Corning's August 1970 titanium-doped silica fibre (17 dB/km), and modern 1,550 nm silica fibre (0.2 dB/km — >95% surviving 1 km)", "scale": "purifying just a few parts per billion of iron out of melted quartz made glass five thousand times clearer than a camera lens — clear enough that a window pane a hundred kilometres thick would still let you see the light on the other side", "hold_s": 3.8}),
            ("03_green_iron_tinted_glass_block_vs_crystal_clear_fused_silica_preform_rod", 140.5, 6.5, "B", False, "JULY 1966 — 20 DECIBELS PER KILOMETRE", "Fast",
             "Fast: daylight macro comparison of a thick green-tinted ordinary window glass block beside a crystal-clear cylindrical fused-silica optical preform rod and a spool of glass thread on a workbench. Nothing emissive, no face.",
             STYLE + "In bright daylight on a laboratory bench, a thick greenish slab of ordinary glass sits beside a crystal-clear fused-quartz cylinder and a brass spool of fine glass fibre." + FAST_TAIL,
             None),
            ("04_explorer_plucking_rusty_iron_specks_from_glass_rod_with_magnet_wand", 147.0, 5.5, "B", True, None, "Quality",
             "Quality: Explorer beat 2 (locked character reference).",
             STYLE + "Peering at a green-tinted glass cylinder speckled with tiny dark rust motes that block a red beam, the Explorer sweeps a small brass magnet wand above the cylinder to lift the specks away so the glass turns crystal clear." + EXP_TAIL,
             None),
        ],
    ),
    (
        5,
        "Part 05 — Corning's 1970 Miracle Fibre, the Undersea Internet & the 1854 London Map That Saved Millions",
        [
            ("01_timeline_1842_1987_and_1_4_million_km_undersea_fibre_99_percent_chart", 152.5, 8.5, "E", False, "1842–1987 TIMELINE · 17 TO 0.2 DB/KM FIBRE · >1.4 MILLION KM SUBMARINE CABLES (99% INTERNET)", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, the 6-date timeline completes: 1842 (Daniel Colladon guides sunlight inside a curving water fountain in Geneva by total internal reflection) · 1917 (Albert Einstein predicts stimulated emission of radiation in Berlin) · 13 Nov 1957–1958 (Gordon Gould coins 'LASER' in a notarised notebook; Townes & Schawlow publish optical maser theory) · 16 May 1960 (Theodore Maiman fires the first laser using a flashlamp-pumped synthetic pink ruby at Hughes Labs in Malibu) · Jan–Jul 1966 (Charles Kao & George Hockham in Harlow prove <20 dB/km purified silica glass fibres can carry laser communications) · Aug 1970–1987 (Maurer, Keck & Schultz at Corning achieve 17 dB/km fibre, refined to 0.2 dB/km and paired with erbium optical amplifiers to carry 99% of global undersea internet traffic).",
             {"kind": "DATA", "label": "1842–1987 TIMELINE & >1.4 MILLION KM UNDERSEA FIBRE CABLES (99% OF INTERCONTINENTAL INTERNET)", "detail": "Animated 6-date timeline (1842 → Aug 1970–1987) alongside Corning's 17 dB/km → 0.2 dB/km silica fibre and >1.4 million kilometres of submarine optical cables carrying 99% of intercontinental internet traffic", "scale": "over one point four million kilometres of hair-thin glass fibres now lie across the ocean floor — enough to wrap around the Earth thirty-five times", "fact_card": "99% of ocean internet is glass", "when_stamp": "August 1970 · 1979 · 1987 · 1842–1987", "timeline_step": "6/6 · Aug 1970–1987 (Maurer, Keck & Schultz at Corning achieve 17 dB/km fibre, refined to 0.2 dB/km and paired with erbium optical amplifiers to carry 99% of global undersea internet traffic)", "hold_s": 3.8}),
            ("02_armoured_undersea_fibre_optic_cable_cutaway_and_corning_notebook_closeup", 161.0, 5.5, "A", False, "1.4 MILLION KM UNDER THE SEA", "Fast",
             "Fast: daylight cutaway specimen of an armoured submarine telecommunication cable showing steel strength wires, copper tube, and hair-thin glass fibres beside an open 1970 laboratory notebook. Nothing emissive, no face.",
             STYLE + "In crisp daylight on an engineering desk, a cutaway section of deep-sea cable reveals steel armour wires surrounding fine clear glass fibres beside an open laboratory notebook." + FAST_TAIL,
             None),
            ("03_john_snow_and_whitehead_september_1854_soho_broad_street_pump_handoff", 166.5, 6.5, "C", False, "THE BROAD STREET PUMP, 1854", "Quality",
             "Quality: readable faces (on the cobblestone corner of Broad Street in Soho, London, in September 1854, physician John Snow and Reverend Henry Whitehead hold a street map covered in black mortality bars beside the Broad Street water pump with its iron handle unbolted — handoff to 043 Broad Street Cholera Map).",
             STYLE + "On a Victorian cobblestone street corner in Soho in 1854, physician John Snow in a dark frock coat and clergyman Henry Whitehead inspect an inked street map beside a cast-iron street water pump with its handle removed." + QUAL_TAIL,
             {"kind": "WHEN", "label": "SEPTEMBER 1854", "hold_s": 3.5}),
            ("04_table_three_callback", 173.0, 2.4, "C", False, None, "reuse",
             "Reuse: verified unused moving window [5.50s..7.90s] of P1:07_table_three_props_gould_notebook_maiman_ruby_cylinder_kao_silica_spool (callback, £0).",
             "Reuse P1:07_table_three_props_gould_notebook_maiman_ruby_cylinder_kao_silica_spool [5.50s..7.90s] (2.40s distinct non-overlapping tail window from 8.00s source clip).",
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
                row["reuse_of"] = "P1:07_table_three_props_gould_notebook_maiman_ruby_cylinder_kao_silica_spool"
                row["reuse_window_s"] = [5.5, 7.9]
                row["reuse_audit"] = {
                    "source_row": "P1:07_table_three_props_gould_notebook_maiman_ruby_cylinder_kao_silica_spool",
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
            "film": "042_Maiman-Kao-Einstein-Laser-Fibre-Optics",
            "part": p_idx,
            "title": p_title,
            "version": "v01",
            "timing_status": "pre_vo_script_clock (built from laser_script_master_v01.md; retimes onto Scribe STT once VO locks)",
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
        "film": "042_Maiman-Kao-Einstein-Laser-Fibre-Optics",
        "version": "v01",
        "date": "2026-10-18",
        "owner": "gemini (J0540)",
        "status": "PRE_VO_BOARDS_V01_NO_MINT",
        "generation_authorized": False,
        "script": "00_Brand/Channel-Setup/ideas/042_Maiman-Kao-Einstein-Laser-Fibre-Optics/laser_script_master_v01.md",
        "script_review_score": 91.2,
        "sources": "00_Brand/Channel-Setup/ideas/042_Maiman-Kao-Einstein-Laser-Fibre-Optics/SOURCES_v01.md",
        "credit_snapshot": {
            "flow_balance": 23740,
            "flow_floor": 0,
            "flow_read_at": "2026-10-15T21:42:22Z",
            "vertex_promo_gbp": 71.02,
            "vertex_usable_gbp": 70.02,
        },
        "totals": totals,
        "per_part": per_part_summary,
        "mint_order": "006 > 007 > 008 > 009 > 010 > 011 > 012 > 013 > 014 > 015 > 016 > 017 > 018 > 019 > 020 > 021 > 022 > 023 > 024 > 025 > 026 > 027 > 028 > 029 > 030 > 031 > 032 > 033 > 034 > 035 > 036 > 037 > 038 > 039 > 040 > 041 > 042. Nothing in 042 is generation_authorized.",
    }
    (EDIT / "PICTURE_PLAN_v01.json").write_text(json.dumps(plan, indent=2) + "\n")

    sl = [
        "# 042 Lasers & Fibre Optics: The Pink Ruby That Built the Internet — Shot list & plate boards v01 (pre-VO)",
        "",
        "Gemini, 18 Oct 2026, J0540. Built from `laser_script_master_v01.md` (`91.2 PASS`) and `SOURCES_v01.md`.",
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
        "# 042 price review v01 (pre-VO plate boards)",
        "",
        "Gemini, 18 Oct 2026, J0540. Boards only. **No mint. No spend. No merge.**",
        "Prepared from `laser_script_master_v01.md` (`91.2 PASS`) and `SOURCES_v01.md` so 042's full plate board rows, non-emissive Fast prompts, £0 code graphics, and Teach-on-Screen overlays are ready to re-time the moment long VO locks. Parked for Chief.",
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
        f"- **Quality ({totals['Quality']} rows):** readable faces (Theodore Maiman, Irnee D'Haenens, Charles Kao, Albert Einstein, Gordon Gould, Arthur Schawlow, Daniel Colladon, John Snow, Henry Whitehead), 1960 Malibu Hughes Research Laboratories scenes, 1969 Apollo 11 lunar retroreflector deployment, 1842 Geneva fountain lecture, and the 2 Explorer beats.",
        f"- **Fast ({totals['Fast']} rows, non-emissive):** daylight prop and laboratory shots (pink synthetic ruby boule, silvered cylinder & unlit quartz coil pan, 3-object callback bench, Gordon Gould's 1957 notarised notebook & cast-iron seal press, Townes's 1954 brass maser chamber & parallel mirrors, disassembled Maiman ruby rod & brass vernier calipers, green iron-tinted glass block vs crystal-clear fused-silica preform rod, armoured undersea fibre-optic cable cutaway). Zero candles, flames, sparks, or glowing elements on Fast.",
        f"- **£0 code graphics ({totals['code_graphic']} rows):**",
        "  1. `P1:04_einstein_1917_maiman_694nm_ruby_and_kao_1000_to_0_2_db_km_fibre_chart` — Einstein's 1917 stimulated emission, Maiman's 16 May 1960 694.3 nm ruby laser, and optical glass loss dropping from 1,000 dB/km (1960) to <20 dB/km (Kao 1966) and 0.2 dB/km (`SCALE: ordinary glass in nineteen sixty swallowed ninety-nine percent of a light beam in just twenty metres — the length of a cricket pitch — whereas today's purified glass fibres carry a laser pulse a hundred kilometres without losing the signal`)",
        "  2. `P1:06_human_hair_100um_vs_single_mode_optical_fibre_9um_core_99_percent_internet_chart` — 100 µm human hair vs 9 µm single-mode optical fibre core carrying 99% of transoceanic internet traffic (`SCALE: the glass core guiding this video across the ocean floor is just nine micrometres wide — ten times thinner than a single strand of your hair`)",
        "  3. `P2:02_einstein_1917_stimulated_emission_2_to_n_cascade_and_mirror_cavity_chart` — Einstein's 1917 stimulated emission cascade (1 → 2 → 4 → 2^n coherent photons in phase) inside a parallel-mirror optical cavity (`SCALE: bounce a single photon back and forth between two mirrors just seventy times while triggering stimulated emission, and one particle of light multiplies into more than a sextillion identical waves marching in step`)",
        "  4. `P3:02_maiman_1960_ruby_70_percent_efficiency_and_694_3nm_spectral_narrowing_chart` — Maiman's 16 May 1960 1 cm × 2 cm synthetic pink ruby rod (~70% fluorescence efficiency vs 1% textbook myth) collapsing into a 694.3 nm laser spike (`SCALE: inside a pink ruby crystal no bigger than the tip of your little finger, Maiman unleashed a pulse of red light brighter than the surface of the Sun`)",
        "  5. `P4:02_kao_1966_and_corning_1970_1979_attenuation_drop_1000_to_0_2_db_km_chart` — Kao & Hockham (1966) and Corning (1970–1979) glass attenuation drop from 1,000 dB/km to 20 dB/km target, 17 dB/km (Aug 1970), and 0.2 dB/km (`SCALE: purifying just a few parts per billion of iron out of melted quartz made glass five thousand times clearer than a camera lens — clear enough that a window pane a hundred kilometres thick would still let you see the light on the other side`)",
        "  6. `P5:01_timeline_1842_1987_and_1_4_million_km_undersea_fibre_99_percent_chart` — completed 6-date timeline (1842 → 1987) + >1.4 million km of submarine optical cables carrying 99% of intercontinental internet traffic (`SCALE: over one point four million kilometres of hair-thin glass fibres now lie across the ocean floor — enough to wrap around the Earth thirty-five times`)",
        f"- **£0 verified reuse ({totals['reuse']} row):** `P5:04_table_three_callback` uses the 2.40 s unused moving tail `[5.50s..7.90s]` of `P1:07_table_three_props_gould_notebook_maiman_ruby_cylinder_kao_silica_spool`.",
        "",
        "## Mint order",
        "",
        "006 > 007 > 008 > 009 > 010 > 011 > 012 > 013 > 014 > 015 > 016 > 017 > 018 > 019 > 020 > 021 > 022 > 023 > 024 > 025 > 026 > 027 > 028 > 029 > 030 > 031 > 032 > 033 > 034 > 035 > 036 > 037 > 038 > 039 > 040 > 041 > 042. `generation_authorized` is `false` on every row.",
    ])
    (EDIT / "PRICE_REVIEW_v01.md").write_text("\n".join(pr_lines) + "\n")
    print(f"042 v01 boards written: {totals['rows']} rows, Flow expected={totals['flow_credits_expected']}")


if __name__ == "__main__":
    main()
