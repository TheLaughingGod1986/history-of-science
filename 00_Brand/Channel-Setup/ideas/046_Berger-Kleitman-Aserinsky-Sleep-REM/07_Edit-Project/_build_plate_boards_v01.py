#!/usr/bin/env python3
"""HOS 046 (Sleep & Dreams: The Nighttime Wash That Saves Your Brain) pre-VO plate boards v01. J0555. No mint, no spend.

Built from 00_Brand/Channel-Setup/ideas/046_Berger-Kleitman-Aserinsky-Sleep-REM/sleep_script_master_v01.md
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
        "Part 01 — The Rusty Polygraph, the Eight-Year-Old Boy, and the Nighttime Dishwasher in Your Skull",
        [
            ("01_aserinsky_1952_chicago_sleeping_son_armond_polygraph_and_glymphatic_wash", 0.0, 5.5, "A", False, "THE NIGHTTIME BRAIN WASH", "Quality",
             "Quality: Short frame 0 / answer image (0:03) + in a University of Chicago sleep lab in 1952, 31-year-old graduate student Eugene Aserinsky watches his sleeping 8-year-old son Armond while the ink pens of an Offner Dynograph machine scribble fast zigzags across a paper roll and glial channels widen by 60% for cerebrospinal fluid to flush neural tissue.",
             STYLE + "In a 1952 University of Chicago sleep laboratory, thirty-one-year-old graduate student Eugene Aserinsky stands beside his sleeping eight-year-old son Armond on a cot while the ink pens of a vintage Offner Dynograph recorder trace fast zigzag waves across a paper strip." + QUAL_TAIL,
             {"kind": "WHEN", "label": "CHICAGO, 1952", "timeline_step": "3/4 · 1952–4 Sep 1953 (Eugene Aserinsky and Nathaniel Kleitman discover Rapid Eye Movement REM dreaming sleep on 8-year-old Armond Aserinsky in Chicago)", "hold_s": 3.5}),
            ("02_berger_1924_eeg_kleitman_1938_cave_aserinsky_1953_rem_and_nedergaard_2013_split", 5.5, 6.0, "B", False, "CLOCKS, DREAMS, BRAIN WASHING", "Quality",
             "Quality: complex three-part split composition (Hans Berger's 6 July 1924 first human EEG brainwave trace in Jena and Nathaniel Kleitman's 1938 underground beds in Mammoth Cave on the left; Eugene Aserinsky's 4 September 1953 REM sleep polygraph pens in the centre; Maiken Nedergaard's 18 October 2013 glymphatic fluid-flush model on the right).",
             STYLE + "Three-panel period composition: on the left, a 1924 string galvanometer and two iron beds inside a limestone cavern; in the centre, brass polygraph ink pens tracing rapid eye-movement waves; on the right, an anatomical brain model showing widened fluid channels." + QUAL_TAIL,
             None),
            ("03_aserinsky_1952_chicago_staring_at_berserk_offner_dynograph_pens", 11.5, 6.0, "C", False, "CHICAGO, 1952", "Quality",
             "Quality: readable faces (in Chicago in 1952, Eugene Aserinsky stares in disbelief as the Offner Dynograph ink pens jerk rapidly back and forth while 8-year-old Armond sleeps deeply beside the machine).",
             STYLE + "In a 1952 Chicago laboratory room, Eugene Aserinsky in rolled-up shirtsleeves leans over a vintage metal polygraph console as its ink pens oscillate rapidly while eight-year-old Armond sleeps peacefully on a cot." + QUAL_TAIL,
             {"kind": "WHEN", "label": "1952", "timeline_step": "3/4 · 1952–4 Sep 1953 (Eugene Aserinsky records REM sleep on his 8-year-old son Armond in Chicago)", "hold_s": 3.5}),
            ("04_90_min_sleep_cycle_eeg_delta_vs_rem_and_26_yr_sleep_6_yr_dream_chart", 17.5, 8.0, "E", False, "90-MIN NREM/REM CYCLES · DELTA (0.5–4 HZ, 60% WIDER CHANNELS) VS REM (74.1% DREAMS) · 26 YRS ASLEEP + 6 YRS DREAMING", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked 90-minute sleep-cycle and brainwave frequency chart compares waking beta/alpha EEG (8–30 Hz), deep slow-wave delta sleep (0.5–4 Hz, 60% interstitial space expansion & 10–20× metabolite clearance, Nedergaard 2013), and paradoxical REM dreaming sleep (fast low-voltage EEG, rapid eye movements, 20 of 27 awakenings reporting vivid dreams, Aserinsky & Kleitman 4 Sep 1953) across an 80-year human lifetime (~26 years spent asleep + ~6 years spent dreaming).",
             {"kind": "DATA", "label": "90-MIN SLEEP CYCLES · DEEP DELTA (0.5–4 HZ, 60% CHANNEL EXPANSION) VS REM · 26 YRS ASLEEP + 6 YRS DREAMING", "detail": "Inked 90-minute sleep-cycle & brainwave frequency chart on period paper comparing waking beta/alpha EEG (8–30 Hz), deep slow-wave delta sleep (0.5–4 Hz, 60% interstitial space expansion & 10–20× metabolite clearance), and paradoxical REM dreaming sleep (fast low-voltage EEG, rapid eye movements, 20 of 27 awakenings reporting vivid dreams) across a human lifetime (~26 years spent asleep + ~6 years spent dreaming)", "scale": "over an eighty-year lifetime, you spend roughly twenty-six years fast asleep — and more than six full years of your life inside vivid REM dreams while your body is temporarily paralysed", "who_card": "Hans Berger (1873–1941) — German psychiatrist in Jena · Nathaniel Kleitman (1895–1999) — American sleep physiologist · Eugene Aserinsky (1921–1998) — American physiology graduate student · Maiken Nedergaard (born 1957) — Danish neuroscientist", "when_stamp": "6 July 1924 · June 1938 · 4 September 1953 · 18 October 2013", "hold_s": 3.8}),
            ("05_offner_dynograph_ink_pens_eeg_paper_roll_and_brass_clock_pan", 25.5, 5.5, "A", False, "CHICAGO, 1952", "Fast",
             "Fast: daylight macro pan across vintage polygraph ink pens, a moving paper strip of alpha, delta, and REM wave traces, silver-foil scalp electrodes, and a brass laboratory clock on an oak bench between code graphics so two full-frame graphics never run back to back. Nothing emissive, no face.",
             STYLE + "In crisp daylight on an oak laboratory bench, the camera pans smoothly across brass ink-pen arms resting on a paper chart of wavy brainwave traces, silver-foil disc electrodes, and a mechanical laboratory clock." + FAST_TAIL,
             None),
            ("06_nedergaard_2013_glymphatic_14_pct_awake_vs_23_pct_asleep_2x_amyloid_chart", 31.0, 8.0, "E", False, "60% WIDER CHANNELS AT NIGHT", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period parchment, an inked glymphatic clearance comparison chart from Xie, Iliff & Nedergaard (18 October 2013, Science) contrasts the waking brain (interstitial fluid space = 14% of brain volume, slow trickle clearance) against the deep-sleeping brain (interstitial space expands by >60% to 23% of brain volume, convective cerebrospinal fluid flow increasing 10–20× and doubling beta-amyloid plaque clearance).",
             {"kind": "DATA", "label": "18 OCT 2013 GLYMPHATIC WASH: CHANNELS WIDEN >60% (14% AWAKE → 23% ASLEEP) · 2× BETA-AMYLOID CLEARANCE", "detail": "Inked waking vs sleeping brain-channel chart showing interstitial space jumping from 14% (awake) to 23% (asleep, a >60% increase) and toxic beta-amyloid plaque clearance doubling during deep slow-wave sleep", "scale": "when you fall into deep sleep, the cells of your brain pull back by sixty percent like parked cars clearing a narrow street so the nighttime street-sweeper trucks can rush through", "hold_s": 3.8}),
            ("07_table_three_props_berger_eeg_strip_kleitman_cave_thermometer_offner_polygraph_pen", 39.0, 5.5, "C", False, "1924 TO 2013", "Fast",
             "Fast: daylight prop table (callback source for Part 05: Hans Berger's 1924 wavy alpha-wave photographic strip, Nathaniel Kleitman's 1938 Mammoth Cave glass thermometer and notebook, and Eugene Aserinsky's 1952 Offner Dynograph ink pen assembly). Nothing emissive.",
             STYLE + "On an oak workbench in soft window light sit three objects side by side: a framed 1924 wavy brainwave strip, a vintage glass thermometer beside a leather cave notebook, and a brass polygraph ink-pen carriage." + FAST_TAIL,
             None),
            ("08_explorer_in_nightcap_with_broom_watching_brain_blocks_slide_apart_for_water_wash", 62.0, 5.5, "A", True, None, "Quality",
             "Quality: Explorer beat 1 (locked character reference, after 1:00).",
             STYLE + "Wearing a striped nightcap over finished hair and holding a tiny broom beside a tabletop model of brain blocks, the Explorer tries to sweep between tightly packed blocks until a bedside clock strikes twelve, the blocks slide apart by sixty percent, and clear water washes dust particles down a drain." + EXP_TAIL,
             None),
            ("09_hans_berger_6_july_1924_jena_recording_first_human_eeg_alpha_wave", 67.5, 5.5, "B", False, "JENA, 6 JULY 1924", "Quality",
             "Quality: readable faces (in Jena on 6 July 1924, German psychiatrist Hans Berger places silver-foil electrodes on a 17-year-old boy's scalp and records the first wavy 10 Hz alpha rhythm line).",
             STYLE + "In a 1924 Jena clinic room, German psychiatrist Hans Berger in a white medical coat carefully attaches small silver-foil electrodes to a teenage patient's head beside a brass string galvanometer." + QUAL_TAIL,
             None),
        ],
    ),
    (
        2,
        "Part 02 — 6 July 1924 & June 1938: Hans Berger's Brainwaves & Nathaniel Kleitman's 32 Days in Mammoth Cave",
        [
            ("01_berger_1924_jena_eeg_and_kleitman_richardson_june_1938_mammoth_cave_beds", 73.0, 6.5, "A", False, "HID EEG FIVE YEARS", "Quality",
             "Quality: readable faces (German psychiatrist Hans Berger on 6 July 1924 in Jena recording the first human EEG, dissolving to 43-year-old Nathaniel Kleitman and 23-year-old Bruce Richardson recording body temperatures 120 feet underground in Mammoth Cave from 4 June to 6 July 1938).",
             STYLE + "Split period scene: on the left in 1924 Jena, psychiatrist Hans Berger inspects a wavy 10 Hz alpha brainwave trace; on the right in June 1938 inside a vast Kentucky limestone cavern, Nathaniel Kleitman and Bruce Richardson sit beside two iron beds whose legs stand in tin cans." + QUAL_TAIL,
             {"kind": "WHO", "label": "Bruce Richardson (born 1915) — Chicago physiology researcher", "fact_card": "Hid EEG five years", "when_stamp": "6 July 1924 · 1929 · 4 June 1938 · 6 July 1938", "timeline_step": "1/4 · 6 Jul 1924 (Hans Berger in Jena records the first human EEG brainwaves, published 1929) & 2/4 · 4 Jun–6 Jul 1938 (Nathaniel Kleitman and Bruce Richardson live 32 days in Mammoth Cave, Kentucky, proving the endogenous ~24-hour human circadian rhythm)", "hold_s": 3.8}),
            ("02_kleitman_1938_mammoth_cave_28h_schedule_vs_24h_circadian_temperature_chart", 79.5, 8.0, "E", False, "JUNE 1938 MAMMOTH CAVE (32 DAYS AT 54 °F / 120 FT DOWN): 28-HOUR CAVE SCHEDULE VS PERSISTENT ~24-HOUR TEMPERATURE CLOCK", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked Mammoth Cave temperature and circadian rhythm chart from Nathaniel Kleitman (1939, Sleep and Wakefulness) compares the imposed 28-hour cave schedule (6 cycles per 7-day week at 54 °F / 12 °C in total darkness for 32 days) against Kleitman's persistent ~24-hour body-temperature oscillation (36.1–37.1 °C, peaking every 24 hours regardless of the cave clock).",
             {"kind": "DATA", "label": "1938 MAMMOTH CAVE (32 DAYS, 120 FT DOWN): IMPOSED 28-H DAY VS PERSISTENT 24-H BODY-TEMPERATURE RHYTHM", "detail": "Inked Mammoth Cave temperature & circadian rhythm chart on period paper from Nathaniel Kleitman (1939, Sleep and Wakefulness) comparing the imposed 28-hour cave schedule (6 cycles per 7-day week at 54 °F / 12 °C in total darkness for 32 days) against Kleitman's persistent ~24-hour body-temperature oscillation (36.1–37.1 °C, peaking every 24 hours regardless of the cave clock)", "scale": "locked a hundred and twenty feet underground in pitch darkness for thirty-two days, Nathaniel Kleitman's body temperature kept ticking on a twenty-four-hour rhythm like a wristwatch sealed inside a vault", "hold_s": 3.8}),
            ("03_mammoth_cave_iron_beds_in_tin_cans_and_temperature_chart_closeup", 87.5, 6.5, "B", False, "JUNE 1938 — MAMMOTH CAVE", "Fast",
             "Fast: daylight-lit museum reconstruction of Kleitman and Richardson's two tall iron beds with their legs standing in tin cans inside the 54 °F limestone cavern beside Kleitman's temperature chart. Nothing emissive, no face.",
             STYLE + "Inside a cool limestone cavern chamber in crisp even light, two tall iron camp beds stand with their legs placed inside tin cans beside a wooden table holding a glass thermometer and a plotted temperature chart." + FAST_TAIL,
             None),
            ("04_berger_1929_alpha_10hz_vs_delta_1_4hz_brainwave_strips_and_galvanometer_pan", 94.0, 5.5, "C", False, "10 HZ ALPHA VS 1–4 HZ DELTA", "Fast",
             "Fast: daylight close-up of Hans Berger's 1929 published EEG strips comparing 10 Hz waking alpha waves with tall 1–4 Hz deep delta sleep waves beside a brass galvanometer on an oak desk. Nothing emissive, no face.",
             STYLE + "In bright window light on an oak desk, two photographic paper strips showing rapid ten-cycle alpha waves and tall slow delta waves rest beside a brass string galvanometer." + FAST_TAIL,
             None),
        ],
    ),
    (
        3,
        "Part 03 — 1952 to 4 September 1953: Eugene Aserinsky Wires Up His 8-Year-Old Son Armond & Discovers REM Dreaming Sleep — Midpoint Twist",
        [
            ("01_aserinsky_1952_taping_electrodes_on_8yo_armond_with_kleitman_and_dement", 99.5, 6.5, "A", False, "THOUGHT MACHINE WAS BROKEN", "Quality",
             "Quality: readable faces (graduate student Eugene Aserinsky in 1952–1953 taping small surface electrodes near the eyes of his 8-year-old son Armond Aserinsky beside an Offner Dynograph pen recorder, joined by Nathaniel Kleitman and William C. Dement).",
             STYLE + "In a 1952 University of Chicago sleep lab, graduate student Eugene Aserinsky gently tapes small round electrodes beside the eyes of his smiling eight-year-old son Armond while professor Nathaniel Kleitman and William Dement watch beside an Offner Dynograph recorder." + QUAL_TAIL,
             {"kind": "WHO", "label": "Armond Aserinsky (1943–2012) — eight-year-old test subject · William C. Dement (1928–2020) — American sleep researcher", "fact_card": "Thought machine was broken", "when_stamp": "1951 · 1952 · 4 September 1953 · 1957", "timeline_step": "3/4 · 1952–4 Sep 1953 (Eugene Aserinsky and Nathaniel Kleitman discover Rapid Eye Movement REM dreaming sleep on 8-year-old Armond Aserinsky in Chicago; 90-minute cycle mapped with William Dement in 1957)", "hold_s": 3.8}),
            ("02_aserinsky_kleitman_4_sep_1953_rem_20_of_27_vs_nrem_4_of_23_dream_recall_chart", 106.0, 8.0, "E", False, "4 SEP 1953 SCIENCE: 20/27 REM AWAKENINGS (74.1%) YIELD VIVID DREAMS VS 4/23 NREM (17.4%) · 90-MIN CYCLE", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked polygraph and dream-recall bar chart from Eugene Aserinsky & Nathaniel Kleitman (4 September 1953, Science 118: 273–274) shows 20 of 27 awakenings during Rapid Eye Movement (REM) periods yielding vivid dream recall (74.1%) vs 4 of 23 awakenings during non-REM ocular quiescence (17.4%), recurring in ~20-minute bursts every ~90 minutes.",
             {"kind": "DATA", "label": "4 SEP 1953 SCIENCE: 20/27 REM AWAKENINGS (74.1%) = VIVID DREAMS VS 4/23 NREM (17.4%) · EVERY 90 MIN", "detail": "Inked polygraph & dream-recall bar chart on period paper from Eugene Aserinsky & Nathaniel Kleitman (4 September 1953, Science 118: 273–274) showing 20 of 27 awakenings during Rapid Eye Movement (REM) periods yielding vivid dream recall (74.1%) vs 4 of 23 awakenings during non-REM ocular quiescence (17.4%), recurring in ~20-minute bursts every ~90 minutes", "scale": "four or five times every single night, your brain switches into a dreaming state where it burns nearly as much oxygen and electricity as it does when you are wide awake solving a maths puzzle", "hold_s": 3.8}),
            ("03_offner_dynograph_conjugate_eye_movement_strip_and_1953_science_offprint_closeup", 114.0, 6.5, "B", False, "4 SEPTEMBER 1953 — REM SLEEP", "Fast",
             "Fast: daylight macro shot of the Offner Dynograph paper strip showing jagged conjugate eye movements alongside Aserinsky and Kleitman's 4 September 1953 Science offprint on an oak desk. Nothing emissive, no face.",
             STYLE + "In crisp daylight on a Chicago sleep-lab desk, a long paper polygraph strip inked with sharp conjugate eye-movement peaks lies beside a printed 1953 scientific journal and a brass stopwatch." + FAST_TAIL,
             None),
            ("04_vintage_offner_dynograph_console_dials_and_ink_wells_pan", 120.5, 5.5, "C", False, "1952 — THE OFFNER DYNOGRAPH", "Fast",
             "Fast: daylight close-up pan across the brushed-metal dials, glass ink wells, and brass pen arms of the 1952 Offner Dynograph polygraph recorder on a wooden bench. Nothing emissive, no face.",
             STYLE + "In bright window light on a wooden laboratory bench, the camera pans across the vintage metal control dials, glass ink reservoirs, and slender pen arms of an Offner Dynograph recorder." + FAST_TAIL,
             None),
        ],
    ),
    (
        4,
        "Part 04 — 18 October 2013: Maiken Nedergaard Discovers the Brain's Nighttime Dishwasher (The Glymphatic System)",
        [
            ("01_nedergaard_and_iliff_18_oct_2013_rochester_glymphatic_brain_wash_discovery", 126.0, 6.5, "A", False, "2% WEIGHT, 20% ENERGY", "Quality",
             "Quality: readable faces (Danish neuroscientist Maiken Nedergaard and American neuroscientist Jeff Iliff at the University of Rochester in 2012 – 18 October 2013 using a two-photon microscope to watch cerebrospinal fluid flush through a sleeping brain).",
             STYLE + "In a University of Rochester laboratory, Danish neuroscientist Maiken Nedergaard and colleague Jeff Iliff examine two-photon microscope images comparing narrow waking brain channels with wide-open sleeping glymphatic channels." + QUAL_TAIL,
             {"kind": "WHO", "label": "Jeff Iliff (born 1976) — American neuroscientist", "fact_card": "2% weight, 20% energy", "when_stamp": "2012 · 18 October 2013", "timeline_step": "4/4 · 2012–18 Oct 2013 (Maiken Nedergaard, Jeff Iliff, and Lulu Xie discover the glymphatic system and >60% sleep-driven expansion of brain interstitial channels in Science)", "hold_s": 3.8}),
            ("02_xie_iliff_nedergaard_18_oct_2013_science_14_to_23_pct_space_and_2x_amyloid_chart", 132.5, 8.0, "E", False, "18 OCT 2013 SCIENCE: INTERSTITIAL SPACE EXPANDS >60% (14% → 23%) · 10–20× CSF INFLUX · 2× BETA-AMYLOID CLEARANCE", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked two-photon tracer and beta-amyloid clearance chart from Xie, Kang, Xu, Iliff & Nedergaard (18 October 2013, Science 342: 373–377) shows interstitial fluid space rising >60% (from 14% awake to 23% in slow-wave sleep), CSF tracer influx increasing ~10–20×, and radiolabelled 125I-beta-amyloid clearance rate doubling during sleep vs wakefulness.",
             {"kind": "DATA", "label": "18 OCT 2013 SCIENCE: GLIAL CELLS SHRINK SO CHANNELS WIDEN >60% (14% → 23%) · 2× BETA-AMYLOID CLEARANCE", "detail": "Inked two-photon tracer & beta-amyloid clearance chart on period paper from Xie, Kang, Xu, Iliff & Nedergaard (18 October 2013, Science 342: 373–377) showing interstitial fluid space rising >60% (from 14% awake to 23% in slow-wave sleep), CSF tracer influx increasing ~10–20×, and radiolabelled 125I-beta-amyloid clearance rate doubling during sleep vs wakefulness", "scale": "your brain cannot think at full speed and power-wash its own hallways at the same time — so every night it shrinks its support cells by sixty percent and turns on a high-pressure dishwasher while you sleep", "hold_s": 3.8}),
            ("03_waking_14_pct_vs_sleeping_23_pct_brain_channel_models_and_2013_science_paper", 140.5, 6.5, "B", False, "18 OCTOBER 2013 — THE GLYMPHATIC WASH", "Fast",
             "Fast: daylight macro shot of two side-by-side anatomical cross-section models on a Rochester lab bench — tightly packed waking glial cells (14% channel volume) on the left and shrunken sleeping glial cells (23% channel volume) on the right — beside the October 2013 Science offprint. Nothing emissive, no face.",
             STYLE + "In crisp daylight on a laboratory bench, two sculpted anatomical cross-section models sit side by side: on the left, tightly packed cells with narrow alleys; on the right, shrunken cells with wide fluid channels beside a printed journal." + FAST_TAIL,
             None),
            ("04_explorer_pulling_slow_wave_sleep_lever_to_widen_pipe_and_flush_plaques", 147.0, 5.5, "B", True, None, "Quality",
             "Quality: Explorer beat 2 (locked character reference).",
             STYLE + "Standing beside two transparent glass pipes, one clogged with yellow beads between thick sponge walls and one wide open, the Explorer pulls a brass lever so the sponge walls shrink back by sixty percent and a stream of clear water flushes the yellow beads cleanly away." + EXP_TAIL,
             None),
        ],
    ),
    (
        5,
        "Part 05 — Why Every Hour of Sleep Counts & How a Frozen Gas Cylinder Created Teflon and Bulletproof Kevlar",
        [
            ("01_timeline_1924_2013_and_8h_vs_6h_front_loaded_nrem_back_loaded_rem_chart", 152.5, 8.5, "E", False, "1924–2013 TIMELINE · 8H VS 6H SLEEP ARCHITECTURE (CUTTING 2 HOURS CHOPS OFF UP TO 2/3 OF MORNING REM)", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, the 4-date timeline completes: 6 Jul 1924 (Hans Berger in Jena records the first human EEG brainwaves, published 1929) · 4 Jun–6 Jul 1938 (Nathaniel Kleitman and Bruce Richardson live 32 days in Mammoth Cave, Kentucky, proving the endogenous ~24-hour human circadian rhythm) · 1952–4 Sep 1953 (Eugene Aserinsky and Nathaniel Kleitman discover Rapid Eye Movement REM dreaming sleep on 8-year-old Armond Aserinsky in Chicago; 90-minute cycle mapped with William Dement in 1957) · 2012–18 Oct 2013 (Maiken Nedergaard, Jeff Iliff, and Lulu Xie discover the glymphatic system and >60% sleep-driven expansion of brain interstitial channels in Science) alongside the 8-hour vs 6-hour sleep architecture curve showing front-loaded deep slow-wave glymphatic wash and back-loaded morning REM dream cycles.",
             {"kind": "DATA", "label": "1924–2013 TIMELINE · 8H VS 6H SLEEP CURVE (LOSING 2 MORNING HOURS ROBS UP TO 2/3 OF REM DREAM SLEEP)", "detail": "Animated 4-date timeline (6 Jul 1924 → 2012–18 Oct 2013) alongside the 8-hour vs 6-hour sleep architecture curve showing front-loaded deep slow-wave glymphatic wash and back-loaded morning REM dream cycles", "scale": "cutting your sleep from eight hours to six doesn't just lose a quarter of the night — it chops off up to two-thirds of your richest morning REM dream cycles", "fact_card": "Morning holds most REM", "when_stamp": "1924–2013", "timeline_step": "4/4 · 1924–2013 timeline complete", "hold_s": 3.8}),
            ("02_two_shift_night_clock_model_deep_wash_first_half_rem_dreams_morning_pan", 161.0, 5.5, "A", False, "TWO NIGHTLY SHIFTS", "Fast",
             "Fast: daylight close-up of a brass eight-hour night-clock dial divided into two painted halves — deep slow-wave washing in the first half and morning REM dream synthesis in the final hours — on an oak desk. Nothing emissive, no face.",
             STYLE + "In crisp daylight on an oak study table, a brass eight-hour night clock dial with painted blue and gold sectors sits beside a fountain pen and a bound sleep-laboratory notebook." + FAST_TAIL,
             None),
            ("03_plunkett_6_apr_1938_sawed_teflon_cylinder_and_kwolek_1965_cloudy_kevlar_handoff", 166.5, 6.5, "C", False, "TEFLON AND BULLETPROOF KEVLAR", "Quality",
             "Quality: readable faces (27-year-old DuPont chemist Roy Plunkett on 6 April 1938 sawing open an 'empty' frozen steel gas cylinder coated inside with white Teflon powder, alongside Stephanie Kwolek in 1965 spinning a cloudy liquid-crystal polymer into golden bulletproof Kevlar fibre — handoff to 047 Plastics, Teflon & Kevlar).",
             STYLE + "Split period scene: on the left in 1938 New Jersey, young chemist Roy Plunkett inspects a sawed-open steel gas cylinder lined with waxy white Teflon powder; on the right in 1965 Delaware, chemist Stephanie Kwolek holds a beaker of cloudy opalescent liquid beside a spool of golden Kevlar fibre." + QUAL_TAIL,
             {"kind": "WHEN", "label": "6 APRIL 1938 · 1965", "hold_s": 3.5}),
            ("04_table_three_callback", 173.0, 2.4, "C", False, None, "reuse",
             "Reuse: verified unused moving window [5.50s..7.90s] of P1:07_table_three_props_berger_eeg_strip_kleitman_cave_thermometer_offner_polygraph_pen (callback, £0).",
             "Reuse P1:07_table_three_props_berger_eeg_strip_kleitman_cave_thermometer_offner_polygraph_pen [5.50s..7.90s] (2.40s distinct non-overlapping tail window from 8.00s source clip).",
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
                row["reuse_of"] = "P1:07_table_three_props_berger_eeg_strip_kleitman_cave_thermometer_offner_polygraph_pen"
                row["reuse_window_s"] = [5.5, 7.9]
                row["reuse_audit"] = {
                    "source_row": "P1:07_table_three_props_berger_eeg_strip_kleitman_cave_thermometer_offner_polygraph_pen",
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
            "film": "046_Berger-Kleitman-Aserinsky-Sleep-REM",
            "part": p_idx,
            "title": p_title,
            "version": "v01",
            "timing_status": "pre_vo_script_clock (built from sleep_script_master_v01.md; retimes onto Scribe STT once VO locks)",
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
        "film": "046_Berger-Kleitman-Aserinsky-Sleep-REM",
        "version": "v01",
        "date": "2026-10-18",
        "owner": "gemini (J0555)",
        "status": "PRE_VO_BOARDS_V01_NO_MINT",
        "generation_authorized": False,
        "script": "00_Brand/Channel-Setup/ideas/046_Berger-Kleitman-Aserinsky-Sleep-REM/sleep_script_master_v01.md",
        "sources": "00_Brand/Channel-Setup/ideas/046_Berger-Kleitman-Aserinsky-Sleep-REM/SOURCES_v01.md",
        "credit_snapshot": {
            "flow_balance": 23740,
            "flow_floor": 0,
            "flow_read_at": "2026-10-15T21:42:22Z",
            "vertex_promo_gbp": 71.02,
            "vertex_usable_gbp": 70.02,
        },
        "totals": totals,
        "per_part": per_part_summary,
        "mint_order": "006 > 007 > 008 > 009 > 010 > 011 > 012 > 013 > 014 > 015 > 016 > 017 > 018 > 019 > 020 > 021 > 022 > 023 > 024 > 025 > 026 > 027 > 028 > 029 > 030 > 031 > 032 > 033 > 034 > 035 > 036 > 037 > 038 > 039 > 040 > 041 > 042 > 043 > 044 > 045 > 046. Nothing in 046 is generation_authorized.",
    }
    (EDIT / "PICTURE_PLAN_v01.json").write_text(json.dumps(plan, indent=2) + "\n")

    sl = [
        "# 046 Sleep & Dreams: The Nighttime Wash That Saves Your Brain — Shot list & plate boards v01 (pre-VO)",
        "",
        "Gemini, 18 Oct 2026, J0555. Built from `sleep_script_master_v01.md` (`91.4 PASS`) and `SOURCES_v01.md`.",
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
        "# 046 price review v01 (pre-VO plate boards)",
        "",
        "Gemini, 18 Oct 2026, J0555. Boards only. **No mint. No spend. No merge.**",
        "Prepared from `sleep_script_master_v01.md` (`91.4 PASS`) and `SOURCES_v01.md` so 046's full plate board rows, non-emissive Fast prompts, £0 code graphics, and Teach-on-Screen overlays are ready to re-time the moment long VO locks. Parked for Chief.",
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
        f"- **Quality ({totals['Quality']} rows):** readable faces (Eugene Aserinsky, 8-year-old Armond Aserinsky, Hans Berger, Nathaniel Kleitman, Bruce Richardson, William C. Dement, Maiken Nedergaard, Jeff Iliff, Roy Plunkett, Stephanie Kwolek), 1952 Chicago sleep lab scenes, 1924 Jena EEG clinic, 1938 Mammoth Cave chamber, 2013 Rochester glymphatic lab, and the 2 Explorer beats.",
        f"- **Fast ({totals['Fast']} rows, non-emissive):** daylight prop and laboratory shots (Offner Dynograph ink pens & EEG paper roll pan, 3-object callback bench, Mammoth Cave iron beds in tin cans & temperature chart, Berger's 1929 10 Hz alpha vs 1–4 Hz delta strips & galvanometer, 4 September 1953 conjugate eye-movement strip & *Science* offprint, Offner Dynograph dials & ink wells, waking 14% vs sleeping 23% brain channel models, two-shift night clock dial). Zero candles, flames, sparks, or glowing elements on Fast.",
        f"- **£0 code graphics ({totals['code_graphic']} rows):**",
        "  1. `P1:04_90_min_sleep_cycle_eeg_delta_vs_rem_and_26_yr_sleep_6_yr_dream_chart` — 90-minute NREM/REM sleep cycles (0.5–4 Hz deep delta wash vs fast REM dreaming) & 80-year human lifetime totals (~26 years asleep + ~6 years dreaming) (`SCALE: over an eighty-year lifetime, you spend roughly twenty-six years fast asleep — and more than six full years of your life inside vivid REM dreams while your body is temporarily paralysed`)",
        "  2. `P1:06_nedergaard_2013_glymphatic_14_pct_awake_vs_23_pct_asleep_2x_amyloid_chart` — Xie, Iliff & Nedergaard (18 October 2013, *Science*) interstitial space expansion from 14% (awake) to 23% (asleep, >60% increase) and 2× beta-amyloid clearance (`SCALE: when you fall into deep sleep, the cells of your brain pull back by sixty percent like parked cars clearing a narrow street so the nighttime street-sweeper trucks can rush through`)",
        "  3. `P2:02_kleitman_1938_mammoth_cave_28h_schedule_vs_24h_circadian_temperature_chart` — Kleitman's 1938 Mammoth Cave experiment (32 days 120 ft underground at 54 °F on an imposed 28-hour day vs persistent ~24-hour body-temperature rhythm) (`SCALE: locked a hundred and twenty feet underground in pitch darkness for thirty-two days, Nathaniel Kleitman's body temperature kept ticking on a twenty-four-hour rhythm like a wristwatch sealed inside a vault`)",
        "  4. `P3:02_aserinsky_kleitman_4_sep_1953_rem_20_of_27_vs_nrem_4_of_23_dream_recall_chart` — Aserinsky & Kleitman (4 September 1953, *Science*) 20 of 27 REM awakenings (74.1%) yielding vivid dream recall vs 4 of 23 non-REM awakenings (17.4%) (`SCALE: four or five times every single night, your brain switches into a dreaming state where it burns nearly as much oxygen and electricity as it does when you are wide awake solving a maths puzzle`)",
        "  5. `P4:02_xie_iliff_nedergaard_18_oct_2013_science_14_to_23_pct_space_and_2x_amyloid_chart` — Xie, Iliff & Nedergaard (18 October 2013, *Science*) >60% channel expansion, 10–20× CSF tracer influx, and 2× radiolabelled beta-amyloid clearance (`SCALE: your brain cannot think at full speed and power-wash its own hallways at the same time — so every night it shrinks its support cells by sixty percent and turns on a high-pressure dishwasher while you sleep`)",
        "  6. `P5:01_timeline_1924_2013_and_8h_vs_6h_front_loaded_nrem_back_loaded_rem_chart` — completed 4-date timeline (1924 → 2013) + 8-hour vs 6-hour sleep architecture curve showing front-loaded deep slow-wave wash and back-loaded morning REM cycles (`SCALE: cutting your sleep from eight hours to six doesn't just lose a quarter of the night — it chops off up to two-thirds of your richest morning REM dream cycles`)",
        f"- **£0 verified reuse ({totals['reuse']} row):** `P5:04_table_three_callback` uses the 2.40 s unused moving tail `[5.50s..7.90s]` of `P1:07_table_three_props_berger_eeg_strip_kleitman_cave_thermometer_offner_polygraph_pen`.",
        "",
        "## Mint order",
        "",
        "006 > 007 > 008 > 009 > 010 > 011 > 012 > 013 > 014 > 015 > 016 > 017 > 018 > 019 > 020 > 021 > 022 > 023 > 024 > 025 > 026 > 027 > 028 > 029 > 030 > 031 > 032 > 033 > 034 > 035 > 036 > 037 > 038 > 039 > 040 > 041 > 042 > 043 > 044 > 045 > 046. `generation_authorized` is `false` on every row.",
    ])
    (EDIT / "PRICE_REVIEW_v01.md").write_text("\n".join(pr_lines) + "\n")
    print(f"046 v01 boards written: {totals['rows']} rows, Flow expected={totals['flow_credits_expected']}")


if __name__ == "__main__":
    main()
