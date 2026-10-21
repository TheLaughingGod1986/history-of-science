#!/usr/bin/env python3
"""HOS 055 (How Hearing Works: The Amplifier Inside Your Inner Ear) pre-VO plate boards v01. J0600. No mint, no spend.

Built from 00_Brand/Channel-Setup/ideas/055_Helmholtz-Bekesy-Kemp-Hearing-Cochlea/hearing_script_master_v01.md
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
        "Part 01 — How a Pea-Sized Snail Shell in Your Skull Detects Motions Smaller Than an Atom",
        [
            ("01_violin_wave_middle_ear_bones_bekesy_silver_dust_cochlea_and_kemp_1978_echo", 0.0, 5.5, "A", False, "SMALLER THAN AN ATOM", "Quality",
             "Quality: Short frame 0 / answer image (0:03) + a sound wave from a plucked violin string ripples into the human ear, vibrating the eardrum and three tiny middle-ear bones into a pea-sized spiral cochlea where silver dust glitters along Georg von Békésy's 1928–1947 travelling wave and David Kemp's July 1978 ear-canal microphone records an echo ringing back out from dancing outer hair cells.",
             STYLE + "Split period-and-anatomical scene: on the left, a plucked violin string sends ripples through the three tiny middle-ear bones into a translucent pea-sized spiral cochlea shimmering with silver dust; on the right in July 1978, physicist David Kemp records an acoustic echo from a miniature ear-canal probe." + QUAL_TAIL,
             {"kind": "WHEN", "label": "JULY 1978", "timeline_step": "3/4 · Jul 1978 (David Kemp records otoacoustic emissions proving Thomas Gold's 1948 active cochlear amplifier)", "hold_s": 3.5}),
            ("02_helmholtz_1863_bekesy_1928_hudspeth_tip_links_and_kemp_1978_ear_echo_split", 5.5, 6.0, "B", False, "COCHLEA, HAIR CELLS, EAR ECHOES", "Quality",
             "Quality: complex three-part composition (Hermann von Helmholtz in Heidelberg in 1863 beside a grand piano and Georg von Békésy in Budapest in 1928–1947 filming the basilar membrane under strobe light; Jim Hudspeth in 1977–1985 nudging hair-cell stereocilia tip links; and David Kemp in London in July 1978 recording otoacoustic emissions from a living human ear).",
             STYLE + "Three-panel period composition: on the left, Hermann von Helmholtz beside an open grand piano and Georg von Békésy inspecting a cochlear preparation; in the centre, a fine glass probe nudging a staircase bundle of hair-cell bristles; on the right, David Kemp in 1978 monitoring an ear-canal microphone waveform." + QUAL_TAIL,
             None),
            ("03_subatomic_01nm_stereocilia_tilt_vs_12000_dancing_outer_hair_cells_amplifying_100x", 11.5, 6.0, "C", False, "0.1 nm = 1 HYDROGEN ATOM", "Quality",
             "Quality: complex microscopic anatomical reveal (at the threshold of human hearing, 0 dB SPL, a hair-cell stereocilia bundle inside the cochlea tilts by just 0.1 nanometres alongside a 0.1 nm hydrogen atom model, while 12,000 cylindrical outer hair cells physically elongate and contract to amplify the fluid wave 100-fold).",
             STYLE + "Inside the fluid-filled cochlear canal, three neat rows of cylindrical outer hair cells rhythmically contract and elongate like miniature pistons, lifting a gentle membrane ripple into a tall wave that tilts a staircase of sensory bristles." + QUAL_TAIL,
             {"kind": "WHEN", "label": "1863 · 1928–1947 · 1948 · JULY 1978 · JANUARY 1985", "timeline_step": "1/4 · 1863 (Helmholtz) · 2/4 · 1928–1947 (Békésy) · 3/4 · Jul 1978 & Jan 1985 (Kemp & Brownell)", "hold_s": 3.5}),
            ("04_cochlear_35mm_tonotopic_map_20000hz_to_20hz_and_40db_outer_hair_cell_gain_chart", 17.5, 8.0, "E", False, "35-MM BASILAR MEMBRANE TONOTOPIC MAP (20,000 HZ BASE → 20 HZ APEX) & +40 DB (100×) OUTER HAIR CELL AMPLIFICATION", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked cochlear tonotopic frequency map & travelling-wave chart from Helmholtz (1863), Békésy (1928–1947 / 1960), and Kemp (July 1978 JASA) plots the 35-mm unrolled basilar membrane from the narrow, stiff base (0.1 mm, peaking at 20,000 Hz) to the wide, flexible apex (0.5 mm, peaking at 20 Hz), with active outer hair cell amplification boosting the wave peak by +40 dB (100×) down to ~0.1 nm displacement.",
             {"kind": "DATA", "label": "35-MM BASILAR MEMBRANE (20,000 HZ BASE TO 20 HZ APEX) & +40 DB (100×) OUTER HAIR CELL AMPLIFIER DOWN TO 0.1 NM", "detail": "Inked cochlear tonotopic map & active amplification chart on period paper showing the 35-mm basilar membrane sorting 20,000 Hz (stiff 0.1 mm base) to 20 Hz (flexible 0.5 mm apex) and outer hair cells providing +40 dB (100-fold) mechanical gain down to ~0.1 nm displacement", "scale": "if you scaled a hair cell's microscopic bristle up to the height of the Eiffel Tower, the whisper-quiet motion it detects at the threshold of hearing would be like tilting the top of the tower by just the width of your thumb", "who_card": "Hermann von Helmholtz (1821–1894) — German physicist and physician · Georg von Békésy (1899–1972) — Hungarian biophysicist · Thomas Gold (1920–2004) — Austrian-British astrophysicist · David T. Kemp (born 1945) — British auditory physicist · William E. Brownell (born 1945) — American biophysicist", "when_stamp": "1863 · 1928–1947 · 1948 · July 1978 · January 1985", "hold_s": 3.8}),
            ("05_brass_helmholtz_resonator_silver_dust_vial_ear_speculum_and_cochlea_model_pan", 25.5, 5.5, "A", False, "1,000× FASTER THAN VISION", "Fast",
             "Fast: daylight macro pan across a hollow brass Helmholtz resonator sphere, a glass vial of silver dust, an acoustic ear-canal probe tip, and a carved wooden spiral cochlea model on an oak laboratory bench between code graphics so two full-frame graphics never run back to back. Nothing emissive, no face.",
             STYLE + "In crisp daylight on an oak laboratory bench, the camera pans smoothly across a polished brass Helmholtz resonator sphere, a small glass vial of silver flakes, a rubber-tipped ear microphone probe, and a cross-section model of the spiral cochlea." + FAST_TAIL,
             None),
            ("06_retinal_phototransduction_20000us_vs_hair_cell_tip_link_10us_speed_chart", 31.0, 8.0, "E", False, "10 MICROSECONDS VS 20–50 MILLISECONDS", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period parchment, an inked sensory transduction speed chart compares retinal rod/cone chemical phototransduction (~20,000–50,000 microseconds) against cochlear hair-cell tip-link direct mechanical channel opening (~10 microseconds — more than 1,000 times faster, supporting frequencies up to 20,000 Hz).",
             {"kind": "DATA", "label": "VISION CHEMICAL CASCADE (20,000–50,000 µS) VS HAIR-CELL MECHANICAL TIP-LINK SPRING (~10 µS = >1,000× FASTER)", "detail": "Inked sensory transduction speed chart comparing retinal phototransduction (~20,000–50,000 µs chemical cascade) against cochlear hair-cell tip-link channel opening (~10 µs direct mechanical gating up to 20,000 Hz)", "scale": "your ear's mechanical trapdoors snap open in ten millionths of a second — more than a thousand times faster than the chemical sensors in your eye, which is why you can hear two drumsticks hit a millisecond apart when your eyes only see a blur", "hold_s": 3.8}),
            ("07_table_three_props_helmholtz_resonator_bekesy_wave_model_and_kemp_ear_probe", 39.0, 5.5, "C", False, "1863 TO 2000", "Fast",
             "Fast: daylight prop table (callback source for Part 05: Hermann von Helmholtz's 1863 brass resonator sphere, Georg von Békésy's 1947 brass-and-rubber cochlear wave model, and David Kemp's 1978 miniature ear-canal microphone probe). Nothing emissive.",
             STYLE + "On an oak workbench in soft window light sit three objects side by side: a hollow brass Helmholtz resonator sphere, a brass-and-rubber mechanical wave rack, and a coiled acoustic ear-canal microphone probe." + FAST_TAIL,
             None),
            ("08_explorer_surfing_35mm_cochlear_wave_boosted_by_outer_hair_cell_pogo_sticks", 62.0, 5.5, "A", True, None, "Quality",
             "Quality: Explorer beat 1 (locked character reference, after 1:00).",
             STYLE + "Surfing on a turquoise wave along an unrolled thirty-five-millimetre canal, the Explorer rides past a row of bouncing cylindrical pogo-stick columns that boost the wave crest high enough to tug a golden tip-link rope and ring a brass bell." + EXP_TAIL,
             None),
            ("09_georg_von_bekesy_1928_budapest_sprinkling_silver_dust_on_cochlea", 67.5, 5.5, "B", False, "BUDAPEST, 1928–1947", "Quality",
             "Quality: readable face (in Budapest in 1928, Hungarian biophysicist Georg von Békésy peers through a binocular microscope at silver flakes glittering on the exposed basilar membrane of a temporal bone preparation).",
             STYLE + "In a 1928 Budapest laboratory, Hungarian biophysicist Georg von Békésy in a white coat bends over a binocular microscope, using a fine brush to sprinkle tiny silver flakes onto a delicate inner-ear preparation." + QUAL_TAIL,
             {"kind": "WHEN", "label": "BUDAPEST, 1928–1947", "timeline_step": "2/4 · 1928–1947 (Georg von Békésy uses silver dust and strobe light to discover the cochlear travelling wave along the 35-mm basilar membrane)", "hold_s": 3.5}),
        ],
    ),
    (
        2,
        "Part 02 — 1863 & 1928–1947: Helmholtz's Piano Harp vs Georg von Békésy's Glittering Cochlear Wave",
        [
            ("01_helmholtz_1863_heidelberg_piano_and_bekesy_1928_1947_budapest_travelling_wave", 73.0, 6.5, "A", False, "35 MM SNAIL-SHELL WAVE", "Quality",
             "Quality: readable faces (German physicist Hermann von Helmholtz in Heidelberg in 1863 standing beside an open grand piano with brass resonators, dissolving to Hungarian biophysicist Georg von Békésy in Budapest in 1928–1947 drilling a microscopic window into a temporal bone under water and observing the 35-mm basilar membrane travelling wave).",
             STYLE + "Split period scene: on the left in 1863 Heidelberg, Hermann von Helmholtz holds a brass resonator sphere beside the open strings of a grand piano; on the right in 1930s Budapest, Georg von Békésy observes a rippling ribbon wave through a microscope." + QUAL_TAIL,
             {"kind": "FACT", "label": "35 mm snail-shell wave", "when_stamp": "1863 · 1928–1947 · 1961", "timeline_step": "1/4 · 1863 (Helmholtz) & 2/4 · 1928–1947 (Békésy travelling wave; 1961 Nobel Prize)", "hold_s": 3.8}),
            ("02_bekesy_1928_1960_basilar_membrane_01mm_to_05mm_width_and_10000x_stiffness_chart", 79.5, 8.0, "E", False, "1863 HELMHOLTZ RESONANCE VS 1928–1947 BÉKÉSY 35-MM TRAVELLING WAVE (0.1 MM STIFF BASE → 0.5 MM FLEXIBLE APEX, 10,000× STIFFNESS GRADIENT)", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked basilar membrane width, stiffness & travelling-wave envelope chart from Helmholtz (1863) and Békésy (1928–1947 / 1960 Experiments in Hearing) shows membrane width widening from ~0.1 mm at the base (20,000 Hz) to ~0.5 mm at the apex (20 Hz) while stiffness drops ~10,000-fold, causing each frequency's travelling wave to crest at a unique distance along the 35-mm ribbon.",
             {"kind": "DATA", "label": "35-MM BASILAR MEMBRANE: WIDTH WIDENS 5× (0.1 → 0.5 MM) & STIFFNESS DROPS 10,000× FROM 20,000 HZ BASE TO 20 HZ APEX", "detail": "Inked basilar membrane width, stiffness & travelling-wave envelope chart on period paper from Helmholtz (1863) and Békésy (1928–1947 / 1960 Experiments in Hearing) showing membrane width widening from ~0.1 mm at the base (20,000 Hz) to ~0.5 mm at the apex (20 Hz) while stiffness drops ~10,000-fold, causing each frequency's travelling wave to crest at a unique distance", "scale": "unrolled from its snail shell, your basilar membrane is just thirty-five millimetres long — the length of a paperclip, yet it sorts a thousand musical pitches from twenty hertz to twenty thousand hertz along its ribbon", "hold_s": 3.8}),
            ("03_bekesy_1947_brass_and_rubber_mechanical_cochlear_wave_model_closeup", 87.5, 6.5, "B", False, "1928–1947 — THE TRAVELLING WAVE", "Fast",
             "Fast: daylight macro shot of Georg von Békésy's 1947 brass-and-rubber mechanical cochlear model, a vial of silver dust, and a standard 35-mm metal paperclip for scale on a Budapest workbench. Nothing emissive, no face.",
             STYLE + "In crisp daylight on a wooden workbench, a brass-and-rubber mechanical wave model sits beside a small glass bottle of silver dust and a thirty-five-millimetre metal paperclip." + FAST_TAIL,
             None),
            ("04_heidelberg_1863_grand_piano_strings_tuning_forks_and_brass_resonators_pan", 94.0, 5.5, "C", False, "1863 — TUNED RESONATORS", "Fast",
             "Fast: daylight close-up pan across the open brass-strung harp of an 1863 grand piano, steel tuning forks, and graded brass Helmholtz resonator spheres on a study table. Nothing emissive, no face.",
             STYLE + "In bright window light in a nineteenth-century study, steel tuning forks and a graded set of hollow brass Helmholtz resonator spheres rest beside the open strings of a grand piano." + FAST_TAIL,
             None),
        ],
    ),
    (
        3,
        "Part 03 — 1948, July 1978 & January 1985: Thomas Gold's Rejected Amplifier, David Kemp's Echoing Ear (Otoacoustic Emissions) & Dancing Outer Hair Cells — Midpoint Twist",
        [
            ("01_gold_1948_cambridge_kemp_july_1978_ear_echo_and_brownell_dallos_dancing_outer_hair_cells", 99.5, 6.5, "A", False, "LIVING EARS EMIT SOUND", "Quality",
             "Quality: readable faces (young astrophysicist Thomas Gold in Cambridge in 1948 sketching an active cochlear feedback circuit, dissolving to British physicist David Kemp in London in July 1978 sealing a miniature microphone probe into a volunteer's ear canal to record otoacoustic emissions, and William Brownell and Peter Dallos watching cylindrical outer hair cells elongate and contract).",
             STYLE + "Split period scene: on the left in July 1978 London, physicist David Kemp fits a tiny acoustic probe into a seated volunteer's ear and watches an echo wave appear on a paper recorder; on the right in 1985, William Brownell and Peter Dallos observe cylindrical outer hair cells contracting under a microscope." + QUAL_TAIL,
             {"kind": "WHO", "label": "Peter Dallos (1934–2014) — Hungarian-American auditory neurobiologist", "fact_card": "Living ears emit sound", "when_stamp": "1948 · July 1978 · 11 January 1985 · 11 May 2000", "timeline_step": "3/4 · Jul 1978 (David Kemp records otoacoustic emissions proving Gold's 1948 amplifier, traced to outer hair cells by Brownell in Jan 1985 and prestin in May 2000)", "hold_s": 3.8}),
            ("02_gold_1948_kemp_1978_oae_and_brownell_1985_dallos_2000_prestin_40db_tuning_chart", 106.0, 8.0, "E", False, "PASSIVE DEAD WAVE VS ACTIVE LIVING +40 DB (100×) OUTER HAIR CELL AMPLIFIER & JULY 1978 KEMP OTOACOUSTIC ECHO", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked passive (dead) vs active (living +40 dB outer-hair-cell amplified) cochlear tuning curve & Kemp otoacoustic emission waveform from Gold (1948), Kemp (July 1978, JASA 64: 1386–1391), Brownell et al. (11 Jan 1985, Science 227: 194–196), and Zheng & Dallos (11 May 2000, Nature 405: 149–155) shows 12,000 prestin-driven outer hair cells sharpening frequency tuning and amplifying basilar-membrane motion 100-fold (+40 dB).",
             {"kind": "DATA", "label": "12,000 PRESTIN-DRIVEN OUTER HAIR CELLS BOOST WAVE 100× (+40 DB) & EMIT 5–15 MS OTOACOUSTIC ECHOES (KEMP, JULY 1978)", "detail": "Inked passive (dead) vs active (living +40 dB outer-hair-cell amplified) cochlear tuning curve & Kemp otoacoustic emission waveform on period paper from Gold (1948), Kemp (July 1978, JASA 64: 1386–1391), Brownell et al. (11 Jan 1985, Science 227: 194–196), and Zheng & Dallos (11 May 2000, Nature 405: 149–155) showing 12,000 prestin-driven outer hair cells sharpening frequency tuning and amplifying basilar-membrane motion 100-fold (+40 dB)", "scale": "twelve thousand outer hair cells in each ear dance up and down up to twenty thousand times a second — acting like microscopic pogo sticks that boost a whisper a hundred times louder before your nerve cells even measure it", "hold_s": 3.8}),
            ("03_london_1978_ear_canal_microphone_probe_and_paper_echo_trace_closeup", 114.0, 6.5, "B", False, "JULY 1978 — OTOACOUSTIC ECHOES", "Fast",
             "Fast: daylight macro shot of David Kemp's 1978 miniature ear-canal acoustic probe assembly, soft rubber ear tips, and a pen-chart waveform trace showing a click followed 10 ms later by an otoacoustic echo on an acoustics bench. Nothing emissive, no face.",
             STYLE + "In crisp daylight on an acoustics workbench, a miniature brushed-aluminium ear microphone probe and rubber ear tips rest beside a paper chart recording of an acoustic wave." + FAST_TAIL,
             None),
            ("04_outer_hair_cell_prestin_piston_model_and_microscope_stage_pan", 120.5, 5.5, "C", False, "11 JANUARY 1985 — DANCING HAIR CELLS", "Fast",
             "Fast: daylight close-up pan across a brass-and-wood anatomical model of cylindrical outer hair cells with spring-loaded walls beside a laboratory microscope stage. Nothing emissive, no face.",
             STYLE + "In bright window light on a laboratory bench, a detailed model of three cylindrical outer hair cells with coiled wall springs sits beside a brass microscope stage." + FAST_TAIL,
             None),
        ],
    ),
    (
        4,
        "Part 04 — 1977–1985: Jim Hudspeth's Microsecond Tip-Link Trapdoors & Why Loud Noise Causes Ringing (Tinnitus)",
        [
            ("01_hudspeth_corey_1977_1983_glass_probe_and_pickles_1984_tip_link_electron_micrograph", 126.0, 6.5, "A", False, "10-MICROSECOND TIP-LINK SPRING", "Quality",
             "Quality: readable faces (American biophysicists Jim Hudspeth and David Corey in 1977–1983 using a micromanipulator glass probe to nudge the staircase stereocilia bundle atop a single hair cell, dissolving to British physiologist James Pickles in Birmingham in 1984 examining an electron micrograph of the 150-nm tip-link filament connecting one bristle tip to its taller neighbour).",
             STYLE + "Split period scene: on the left in 1979, biophysicists Jim Hudspeth and David Corey adjust a micromanipulator glass probe nudging a microscopic hair-cell bundle; on the right in 1984 Birmingham, James Pickles inspects a high-magnification print of staircase bristles joined by fine tip-link threads." + QUAL_TAIL,
             {"kind": "WHO", "label": "A. James Hudspeth (born 1945) — American sensory biophysicist · David P. Corey (born 1951) — American neurobiologist · James O. Pickles (born 1946) — British auditory physiologist", "fact_card": "10-microsecond tip-link spring", "when_stamp": "1977–1983 · 1984", "timeline_step": "4/4 · 1979–1984 (Jim Hudspeth, David Corey & James Pickles reveal 10-microsecond tip-link mechanotransduction springs)", "hold_s": 3.8}),
            ("02_corey_hudspeth_1979_1983_and_pickles_1984_stereocilia_tip_link_10us_gating_chart", 132.5, 8.0, "E", False, "1979–1984 HUDSPETH/COREY/PICKLES 150-NM TIP-LINK GATING SPRING (~10 µS CHANNEL OPENING ACROSS 15,500 HAIR CELLS PER EAR)", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked hair-cell stereocilia staircase & tip-link gating-spring chart from Corey & Hudspeth (1979 PNAS / 1983 J. Neurosci.) and Pickles, Comis & Osborne (1984 Hearing Research 15: 103–112) shows a ~150-nm tip-link filament pulling open TMC1 mechanotransduction channels in ~10 µs across a 0.1–100 nm bundle deflection across the human ear's ~15,500 non-regenerating hair cells.",
             {"kind": "DATA", "label": "150-NM TIP-LINK FILAMENT YANKS OPEN ION TRAPDOORS IN ~10 µS ACROSS 15,500 NON-REGENERATING HAIR CELLS PER EAR", "detail": "Inked hair-cell stereocilia staircase & tip-link gating-spring chart on period paper from Corey & Hudspeth (1979 PNAS / 1983 J. Neurosci.) and Pickles, Comis & Osborne (1984 Hearing Research 15: 103–112) showing a ~150-nm tip-link filament pulling open TMC1 mechanotransduction channels in ~10 µs across a 0.1–100 nm bundle deflection", "scale": "each ear has only fifteen thousand five hundred hair cells to last your entire life — fewer than the seats in a single sports arena, compared with more than a hundred million light sensors in a single eye", "hold_s": 3.8}),
            ("03_stereocilia_staircase_model_with_tip_link_threads_and_micromanipulator_closeup", 140.5, 6.5, "B", False, "15,500 HAIR CELLS PER EAR", "Fast",
             "Fast: daylight macro shot of a V-shaped staircase model of hair-cell stereocilia connected by fine brass tip-link threads beside a precision micromanipulator dial on a bench. Nothing emissive, no face.",
             STYLE + "In crisp daylight on a physiology workbench, a V-shaped staircase model of graduated sensory bristles joined at their tips by fine brass spring threads sits beside a brass micromanipulator dial." + FAST_TAIL,
             None),
            ("04_explorer_tugging_golden_tip_link_rope_on_giant_stereocilia_staircase_trapdoor", 147.0, 5.5, "B", True, None, "Quality",
             "Quality: Explorer beat 2 (locked character reference).",
             STYLE + "Standing atop a giant staircase of cylindrical pillars, the Explorer pulls a taut golden rope linking a shorter pillar to a spring-loaded trapdoor on the taller pillar beside it, opening the hatch as a stream of brass spheres rolls inside." + EXP_TAIL,
             None),
        ],
    ),
    (
        5,
        "Part 05 — Why Newborn Babies' Ears Echo Back — & How Your Nose Smells 10,000 Scents",
        [
            ("01_timeline_1863_2000_and_tinnitus_central_gain_vs_newborn_oae_screening_chart", 152.5, 8.5, "E", False, "1863–2000 TIMELINE · HELMHOLTZ, BÉKÉSY 35-MM WAVE, KEMP 1978 OAE ECHO, BROWNELL/DALLOS PRESTIN & HUDSPETH/PICKLES 10-µS TIP LINKS", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, the 4-date timeline completes: 1863 (Hermann von Helmholtz publishes On the Sensations of Tone proposing cochlear frequency resonance) · 1928–1947 (Georg von Békésy uses silver dust and strobe light to discover the cochlear travelling wave along the 35-mm basilar membrane) · Jul 1978 (David Kemp records otoacoustic emissions proving Thomas Gold's 1948 active cochlear amplifier, traced to dancing outer hair cells by William Brownell in Jan 1985 and prestin in May 2000) · 1979–1984 (Jim Hudspeth, David Corey & James Pickles reveal 10-microsecond tip-link mechanotransduction springs).",
             {"kind": "DATA", "label": "1863–2000 HEARING TIMELINE · BÉKÉSY 35-MM WAVE, KEMP 1978 OAE ECHO, 12,000 OUTER HAIR CELLS & 10-µS TIP LINKS", "detail": "Animated 4-date timeline (1863 → 2000) alongside the central auditory gain tinnitus diagram and newborn otoacoustic emission screening chart", "scale": "every time you listen to a song or hear a friend's voice, twelve thousand microscopic hair motors in each ear are dancing in time with the music to amplify vibrations smaller than an atom", "when_stamp": "1863–2000", "timeline_step": "4/4 · 1863–2000 timeline complete", "hold_s": 3.8}),
            ("02_newborn_oae_ear_probe_cochlea_model_and_tuning_fork_on_plinth_pan", 161.0, 5.5, "A", False, "BRAIN GAIN & NEWBORN ECHO TEST", "Fast",
             "Fast: daylight close-up of a soft newborn otoacoustic screening ear probe beside a spiral cochlea model and a steel tuning fork on a wooden museum plinth. Nothing emissive, no face.",
             STYLE + "In crisp daylight on a wooden museum plinth, a soft-tipped newborn hearing microphone probe rests beside a translucent spiral cochlea model and a steel tuning fork." + FAST_TAIL,
             None),
            ("03_buck_and_axel_5_apr_1991_1000_olfactory_receptor_genes_and_1999_chord_code_handoff", 166.5, 6.5, "C", False, "400 KEYS, 10,000 SCENTS", "Quality",
             "Quality: readable faces (American biologists Linda Buck and Richard Axel at Columbia University on 5 April 1991 discovering the 1,000-gene olfactory receptor family, alongside Linda Buck and Bettina Malnic on 5 March 1999 proving the combinatorial piano-chord code of smell across 400 human nasal receptors — handoff to 056 Olfaction & Smell).",
             STYLE + "Split period scene: on the left in April 1991 at Columbia University, neurobiologist Linda Buck and molecular biologist Richard Axel inspect a multi-band DNA gel of olfactory receptor genes; on the right in March 1999, Linda Buck and Bettina Malnic map odour molecules onto a four-hundred-key receptor board." + QUAL_TAIL,
             {"kind": "WHEN", "label": "5 APRIL 1991 · 5 MARCH 1999", "hold_s": 3.5}),
            ("04_table_three_callback", 173.0, 2.4, "C", False, None, "reuse",
             "Reuse: verified unused moving window [5.50s..7.90s] of P1:07_table_three_props_helmholtz_resonator_bekesy_wave_model_and_kemp_ear_probe (callback, £0).",
             "Reuse P1:07_table_three_props_helmholtz_resonator_bekesy_wave_model_and_kemp_ear_probe [5.50s..7.90s] (2.40s distinct non-overlapping tail window from 8.00s source clip).",
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
                row["reuse_of"] = "P1:07_table_three_props_helmholtz_resonator_bekesy_wave_model_and_kemp_ear_probe"
                row["reuse_window_s"] = [5.5, 7.9]
                row["reuse_audit"] = {
                    "source_row": "P1:07_table_three_props_helmholtz_resonator_bekesy_wave_model_and_kemp_ear_probe",
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
            "film": "055_Helmholtz-Bekesy-Kemp-Hearing-Cochlea",
            "part": p_idx,
            "title": p_title,
            "version": "v01",
            "timing_status": "pre_vo_script_clock (built from hearing_script_master_v01.md; retimes onto Scribe STT once VO locks)",
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
        "film": "055_Helmholtz-Bekesy-Kemp-Hearing-Cochlea",
        "version": "v01",
        "date": "2026-10-18",
        "owner": "gemini (J0600)",
        "status": "PRE_VO_BOARDS_V01_NO_MINT",
        "generation_authorized": False,
        "script": "00_Brand/Channel-Setup/ideas/055_Helmholtz-Bekesy-Kemp-Hearing-Cochlea/hearing_script_master_v01.md",
        "sources": "00_Brand/Channel-Setup/ideas/055_Helmholtz-Bekesy-Kemp-Hearing-Cochlea/SOURCES_v01.md",
        "credit_snapshot": {
            "flow_balance": 23740,
            "flow_floor": 0,
            "flow_read_at": "2026-10-15T21:42:22Z",
            "vertex_promo_gbp": 71.02,
            "vertex_usable_gbp": 70.02,
        },
        "totals": totals,
        "per_part": per_part_summary,
        "mint_order": "006 > 007 > 008 > 009 > 010 > 011 > 012 > 013 > 014 > 015 > 016 > 017 > 018 > 019 > 020 > 021 > 022 > 023 > 024 > 025 > 026 > 027 > 028 > 029 > 030 > 031 > 032 > 033 > 034 > 035 > 036 > 037 > 038 > 039 > 040 > 041 > 042 > 043 > 044 > 045 > 046 > 047 > 048 > 049 > 050 > 051 > 052 > 053 > 054 > 055 > 056. Nothing in 055 is generation_authorized.",
    }
    (EDIT / "PICTURE_PLAN_v01.json").write_text(json.dumps(plan, indent=2) + "\n")

    sl = [
        "# 055 How Hearing Works: The Amplifier Inside Your Inner Ear — Shot list & plate boards v01 (pre-VO)",
        "",
        "Gemini, 18 Oct 2026, J0600. Built from `hearing_script_master_v01.md` (`91.4 PASS`) and `SOURCES_v01.md`.",
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
        "# 055 price review v01 (pre-VO plate boards)",
        "",
        "Gemini, 18 Oct 2026, J0600. Boards only. **No mint. No spend. No merge.**",
        "Prepared from `hearing_script_master_v01.md` (`91.4 PASS`) and `SOURCES_v01.md` so 055's full plate board rows, non-emissive Fast prompts, £0 code graphics, and Teach-on-Screen overlays are ready to re-time the moment long VO locks. Parked for Chief.",
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
        f"- **Quality ({totals['Quality']} rows):** readable faces (Hermann von Helmholtz, Georg von Békésy, Thomas Gold, David T. Kemp, William E. Brownell, Peter Dallos, A. James Hudspeth, David P. Corey, James O. Pickles, Linda B. Buck, Richard Axel, Bettina Malnic), 1863 Heidelberg piano resonance, 1928–1947 Budapest silver-dust cochlear travelling wave, July 1978 London otoacoustic emissions & 1985 dancing outer hair cells, 1977–1984 microsecond tip-link mechanotransduction, and the 2 Explorer beats.",
        f"- **Fast ({totals['Fast']} rows, non-emissive):** daylight prop and laboratory shots (Helmholtz brass resonator, silver-dust vial, ear probe & spiral cochlea model pan, 3-object callback bench, Békésy's 1947 brass-and-rubber wave model & 35-mm paperclip, Heidelberg 1863 grand piano strings & tuning forks, Kemp's 1978 ear-canal microphone probe & waveform trace, outer hair cell prestin piston model & microscope stage, stereocilia staircase model with tip-link threads & micromanipulator, newborn OAE probe & tuning fork on museum plinth). Zero candles, flames, sparks, or glowing elements on Fast.",
        f"- **£0 code graphics ({totals['code_graphic']} rows):**",
        "  1. `P1:04_cochlear_35mm_tonotopic_map_20000hz_to_20hz_and_40db_outer_hair_cell_gain_chart` — 35-mm basilar membrane tonotopic map (20,000 Hz stiff base to 20 Hz flexible apex) and +40 dB (100×) outer hair cell mechanical gain down to ~0.1 nm (`SCALE: if you scaled a hair cell's microscopic bristle up to the height of the Eiffel Tower, the whisper-quiet motion it detects at the threshold of hearing would be like tilting the top of the tower by just the width of your thumb`)",
        "  2. `P1:06_retinal_phototransduction_20000us_vs_hair_cell_tip_link_10us_speed_chart` — retinal chemical phototransduction (20,000–50,000 µs) vs cochlear hair-cell tip-link direct mechanical gating (~10 µs = >1,000× faster) (`SCALE: your ear's mechanical trapdoors snap open in ten millionths of a second — more than a thousand times faster than the chemical sensors in your eye, which is why you can hear two drumsticks hit a millisecond apart when your eyes only see a blur`)",
        "  3. `P2:02_bekesy_1928_1960_basilar_membrane_01mm_to_05mm_width_and_10000x_stiffness_chart` — Helmholtz (1863) vs Békésy (1928–1947) 35-mm basilar membrane width (0.1 → 0.5 mm) and 10,000-fold stiffness gradient sorting 20,000 Hz to 20 Hz (`SCALE: unrolled from its snail shell, your basilar membrane is just thirty-five millimetres long — the length of a paperclip, yet it sorts a thousand musical pitches from twenty hertz to twenty thousand hertz along its ribbon`)",
        "  4. `P3:02_gold_1948_kemp_1978_oae_and_brownell_1985_dallos_2000_prestin_40db_tuning_chart` — Gold (1948), Kemp (July 1978 OAE echo), Brownell (1985), and Dallos (2000 prestin) passive vs active +40 dB (100×) cochlear tuning curve across 12,000 outer hair cells (`SCALE: twelve thousand outer hair cells in each ear dance up and down up to twenty thousand times a second — acting like microscopic pogo sticks that boost a whisper a hundred times louder before your nerve cells even measure it`)",
        "  5. `P4:02_corey_hudspeth_1979_1983_and_pickles_1984_stereocilia_tip_link_10us_gating_chart` — Corey & Hudspeth (1979–1983) and Pickles (1984) 150-nm tip-link gating spring (~10 µs channel opening across 15,500 non-regenerating hair cells per human ear) (`SCALE: each ear has only fifteen thousand five hundred hair cells to last your entire life — fewer than the seats in a single sports arena, compared with more than a hundred million light sensors in a single eye`)",
        "  6. `P5:01_timeline_1863_2000_and_tinnitus_central_gain_vs_newborn_oae_screening_chart` — completed 4-date timeline (1863 → 2000) + central auditory gain tinnitus and newborn OAE screening chart (`SCALE: every time you listen to a song or hear a friend's voice, twelve thousand microscopic hair motors in each ear are dancing in time with the music to amplify vibrations smaller than an atom`)",
        f"- **£0 verified reuse ({totals['reuse']} row):** `P5:04_table_three_callback` uses the 2.40 s unused moving tail `[5.50s..7.90s]` of `P1:07_table_three_props_helmholtz_resonator_bekesy_wave_model_and_kemp_ear_probe`.",
        "",
        "## Mint order",
        "",
        "006 > 007 > 008 > 009 > 010 > 011 > 012 > 013 > 014 > 015 > 016 > 017 > 018 > 019 > 020 > 021 > 022 > 023 > 024 > 025 > 026 > 027 > 028 > 029 > 030 > 031 > 032 > 033 > 034 > 035 > 036 > 037 > 038 > 039 > 040 > 041 > 042 > 043 > 044 > 045 > 046 > 047 > 048 > 049 > 050 > 051 > 052 > 053 > 054 > 055 > 056. `generation_authorized` is `false` on every row.",
    ])
    (EDIT / "PRICE_REVIEW_v01.md").write_text("\n".join(pr_lines) + "\n")
    print(f"055 v01 boards written: {totals['rows']} rows, Flow expected={totals['flow_credits_expected']}")


if __name__ == "__main__":
    main()
