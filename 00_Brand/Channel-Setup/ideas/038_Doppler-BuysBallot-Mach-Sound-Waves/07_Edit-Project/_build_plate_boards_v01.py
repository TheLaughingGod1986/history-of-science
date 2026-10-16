#!/usr/bin/env python3
"""HOS 038 (The Doppler Effect: The 1845 Train of Trumpets That Proved It) pre-VO plate boards v01. J0524. No mint, no spend.

Built from 00_Brand/Channel-Setup/ideas/038_Doppler-BuysBallot-Mach-Sound-Waves/doppler_script_master_v01.md
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
        "Part 01 — The Lecture Hall in Prague and the Steam Train of Trumpets in Holland",
        [
            ("01_buys_ballot_3_june_1845_utrecht_train_trumpets_and_mach_1887_bullet_cone", 0.0, 5.5, "A", False, "THE TRAIN FULL OF TRUMPETS", "Quality",
             "Quality: Short frame 0 / answer image (0:03) + along the Utrecht–Maarssen railway line in the Netherlands on 3 June 1845, a steam locomotive roars past at 40 mph pulling an open wooden flatbed car where brass horn players blast a sustained G note while 27-year-old Dutch scientist Christophorus Buys Ballot listens beside the tracks, dissolving to Ernst Mach's 1887 shadowgraph of the V-shaped shockwave cone around a supersonic rifle bullet.",
             STYLE + "Along the Utrecht railway line on 3 June 1845, a green-and-brass steam locomotive speeds past pulling an open wooden flatbed wagon where three horn players blow polished brass trumpets while young Dutch scientist Christophorus Buys Ballot listens on the embankment, dissolving to a crisp shadowgraph plate showing a V-shaped shockwave cone trailing a speeding rifle bullet." + QUAL_TAIL,
             {"kind": "WHEN", "label": "UTRECHT, 3 JUNE 1845 · PRAGUE, 1887", "timeline_step": "3/5 · 3–5 Jun 1845 (Buys Ballot's Utrecht steam-train horn experiment) & 5/5 · 1887 (Mach & Salcher photograph the supersonic bullet shockwave cone)", "hold_s": 3.5}),
            ("02_doppler_1842_wave_diagram_1845_train_horns_and_1887_mach_cone_split", 5.5, 6.0, "B", False, "WAVE SHIFT, TRAIN HORNS, MACH CONE", "Quality",
             "Quality: complex three-part split composition (Christian Doppler's 25 May 1842 wave-crest diagram in Prague on the left; Buys Ballot's June 1845 Utrecht steam train of horn players in the centre; Ernst Mach and Peter Salcher's 1887 shadowgraph photograph of a supersonic bullet shockwave cone on the right).",
             STYLE + "Three-panel period composition: on the left, concentric wave circles chalked on a dark slate beside a brass tuning fork; in the centre, a brass post horn and music score resting on a railway timber; on the right, a glass photographic plate showing a sharp V-shaped shockwave cone around a brass bullet." + QUAL_TAIL,
             None),
            ("03_doppler_25_may_1842_prague_lecture_to_six_scholars", 11.5, 6.0, "C", False, "BARELY SIX LISTENERS", "Quality",
             "Quality: readable faces (inside a small hall of the Royal Bohemian Society of Sciences in Prague on 25 May 1842, 38-year-old Christian Doppler chalks concentric wave circles on a slate before six seated scholars).",
             STYLE + "Inside a quiet 1842 lecture room in Prague, thirty-eight-year-old Austrian professor Christian Doppler in a dark frock coat draws off-centre concentric wave circles on a wooden chalkboard before six seated scholars." + QUAL_TAIL,
             {"kind": "WHEN", "label": "PRAGUE, 25 MAY 1842", "timeline_step": "2/5 · 25 May 1842 (Christian Doppler presents his wave-shift equation in Prague)", "hold_s": 3.5}),
            ("04_doppler_1842_wave_bunching_343_ms_and_40_mph_train_pitch_shift_chart", 17.5, 8.0, "E", False, "SOUND SPEED 343 M/S (767 MPH) · 40 MPH TRAIN SHIFTS HORN PITCH BY ~1 WHOLE TONE", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked wave-frequency and pitch chart shows sound travelling at 343 m/s (767 mph at 20 °C) and a train moving at ~18 m/s (40 mph) bunching wave crests ahead (shorter wavelength λ, higher frequency) and stretching them behind (longer wavelength λ, lower frequency), shifting a sustained horn note by ~10% (~1 musical whole tone from approach to recession).",
             {"kind": "DATA", "label": "SOUND AT 343 M/S (767 MPH) & 40 MPH (18 M/S) TRAIN SHIFTING HORN PITCH BY ~10% (~1 WHOLE TONE)", "detail": "Inked wave-frequency & pitch chart on period paper showing sound travelling at 343 m/s (767 mph at 20 °C) and a train moving at ~18 m/s (40 mph) shifting a horn note by ~10% in frequency (~a musical whole tone from approaching to receding)", "scale": "a steam train chugging at just forty miles an hour — barely one-twentieth the speed of sound — squashes and stretches the sound waves enough to drop a trumpet's note by nearly a full piano key as it passes your ear", "who_card": "Christian Doppler (1803–1853) — Austrian physicist · Christophorus Buys Ballot (1817–1890) — Dutch meteorologist · Ernst Mach (1838–1916) — Austrian physicist", "when_stamp": "25 May 1842 · 3 June 1845 · 1887", "hold_s": 3.8}),
            ("05_brass_valved_post_horn_tuning_fork_and_stopwatch_bench_pan", 25.5, 5.5, "A", False, "UTRECHT RAILWAY, 1845", "Fast",
             "Fast: daylight macro pan across a polished 1840s brass valved Königstiger horn, a steel tuning fork on a wooden resonance box, and a silver pocket stopwatch on an oak bench between code graphics so two full-frame graphics never run back to back. Nothing emissive, no face.",
             STYLE + "In crisp daylight on a wooden workbench, the camera pans across a coiled brass valved post horn, a steel tuning fork mounted on a wooden sound box, and a silver pocket stopwatch." + FAST_TAIL,
             None),
            ("06_speed_scale_bar_40mph_train_vs_343ms_mach1_vs_500ms_rifle_bullet_card", 31.0, 8.0, "E", False, "343 METRES PER SECOND", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period parchment, an inked speed-scale bar compares Buys Ballot's June 1845 steam locomotive (~18 m/s / 40 mph = Mach 0.05) against the speed of sound in air at 20 °C (343 m/s / 767 mph = Mach 1.0) and Mach & Salcher's 1887 rifle bullet + whip tip (~440–530 m/s = Mach 1.3–1.5).",
             {"kind": "DATA", "label": "1845 TRAIN (18 M/S = MACH 0.05) VS SPEED OF SOUND (343 M/S = MACH 1.0) VS BULLET (485 M/S = MACH 1.4)", "detail": "Inked speed bar comparing Buys Ballot's June 1845 steam train (~18 m/s / 40 mph = Mach 0.05) vs the speed of sound in air at 20 °C (343 m/s / 767 mph = Mach 1.0) vs Mach & Salcher's 1887 rifle bullet (~440–530 m/s = Mach 1.3–1.5)", "scale": "sound races through mild air at 343 metres per second — the length of three and a half football pitches every single second", "hold_s": 3.8}),
            ("07_table_three_props_doppler_treatise_brass_horn_mach_shadowgraph_plate", 39.0, 5.5, "C", False, "1842 TO 1887", "Fast",
             "Fast: daylight prop table (callback source for Part 05: Christian Doppler's 1842 Prague paper beside a tuning fork, Buys Ballot's coiled brass horn, and Ernst Mach's glass photographic plate showing a bullet shockwave cone). Nothing emissive.",
             STYLE + "On an oak workbench in soft window light sit three objects side by side: a bound nineteenth-century pamphlet beside a steel tuning fork, a polished brass valved horn, and a framed glass photographic plate showing a V-shaped wave cone around a bullet." + FAST_TAIL,
             None),
            ("08_explorer_riding_miniature_steam_locomotive_blowing_horn_wave_rings", 62.0, 5.5, "A", True, None, "Quality",
             "Quality: Explorer beat 1 (locked character reference, after 1:00).",
             STYLE + "Riding on the front of a miniature brass steam locomotive while blowing a golden French horn, the Explorer watches concentric brass sound-wave rings bunch tightly together ahead of the train and stretch wide apart behind it as a tuning fork by the track vibrates." + EXP_TAIL,
             None),
            ("09_buys_ballot_5_june_1845_utrecht_platform_musicians_recording_pitch_drop", 67.5, 5.5, "B", False, "UTRECHT, JUNE 1845", "Quality",
             "Quality: readable faces (beside the Utrecht railway track on 5 June 1845, Christophorus Buys Ballot and three Dutch musicians on the station platform write down the exact pitch drop in their notebooks as the horn train recedes).",
             STYLE + "On a wooden railway platform near Utrecht on 5 June 1845, young scientist Christophorus Buys Ballot and three musicians in frock coats compare their musical note pads with astonished smiles as a steam train recedes down the track." + QUAL_TAIL,
             None),
        ],
    ),
    (
        2,
        "Part 02 — Cannon Flashes, Ripples in a Pond & Doppler's 1842 Prague Paper",
        [
            ("01_french_academy_1738_hilltop_cannon_timing_and_doppler_1842_prague", 73.0, 6.5, "A", False, "SPOKE TO JUST 6 PEOPLE", "Quality",
             "Quality: readable faces (French Academy scientists in 1738 on a hilltop near Paris timing a distant cannon with a pendulum pocket watch, contrasted with Christian Doppler on 25 May 1842 lecturing to six listeners in Prague).",
             STYLE + "Split period scene: on the left on a French hilltop in 1738, two astronomers in tricorn hats hold a brass telescope and pocket timer toward a distant puff of white cannon smoke; on the right in Prague in May 1842, Christian Doppler points to wave circles before six listeners." + QUAL_TAIL,
             {"kind": "FACT", "label": "Spoke to just 6 people", "when_stamp": "1630s · 1738 · 25 May 1842", "timeline_step": "1/5 · 1738 (French Academy cannon experiments clock sound at 331 m/s at 0 °C)", "hold_s": 3.8}),
            ("02_1738_french_academy_cannon_29km_331ms_and_doppler_1842_formula_diagram", 79.5, 8.0, "E", False, "1738 CANNON TIMING (29 KM = 331 M/S AT 0 °C) & DOPPLER'S 1842 WAVE FORMULA", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked cannon-timing and wave diagram shows the 1738 French Academy cannon experiment (instantaneous muzzle-flash sightline vs 88-second acoustic boom across ~29 km = 331 m/s at 0 °C / 343 m/s at 20 °C) alongside Christian Doppler's 25 May 1842 wave-bunching formula f_obs = f_src × v / (v ∓ v_s).",
             {"kind": "DATA", "label": "1738 FRENCH ACADEMY CANNON TIMING (29 KM IN 88 S = 331 M/S AT 0 °C) & DOPPLER 1842 EQUATION", "detail": "Inked cannon-timing & wave diagram on period paper showing the 1738 French Academy cannon experiment (muzzle flash vs acoustic boom across ~29 km = 331 m/s at 0 °C / 343 m/s at 20 °C) alongside Christian Doppler's 25 May 1842 wave-bunching formula f_obs = f_src × v / (v ∓ v_s)", "scale": "light crosses twenty-nine kilometres in less than a ten-thousandth of a second — whereas the cannon's sound wave takes a full eighty-eight seconds to march across the same valley", "hold_s": 3.8}),
            ("03_compression_and_rarefaction_brass_spring_wave_model_closeup", 87.5, 6.5, "B", False, "COMPRESSION & RAREFACTION", "Fast",
             "Fast: daylight macro shot of a long brass helical spring on a wooden demonstration track showing a tightly bunched compression pulse and a stretched rarefaction gap travelling along the coils without the spring itself moving across the table. Nothing emissive, no face.",
             STYLE + "In crisp daylight on a physics lecture bench, a polished brass coil spring mounted on wooden guides shows a tightly bunched compression wave travelling cleanly down the coils." + FAST_TAIL,
             None),
            ("04_doppler_1842_manuscript_and_ship_waves_diagram_prague", 94.0, 5.5, "C", False, "25 MAY 1842 — PRAGUE", "Fast",
             "Fast: daylight close-up of Christian Doppler's 25 May 1842 Prague manuscript 'Über das farbige Licht der Doppelsterne' beside an inked wooden model of a sailing ship steering into water ripples. Nothing emissive, no face.",
             STYLE + "In bright daylight on a Prague desk, a brass pointer moves across a shallow glass water tray beside an open nineteenth-century leather notebook and a miniature wooden sailing ship meeting closely spaced water ripples." + FAST_TAIL,
             {"kind": "WHEN", "label": "25 MAY 1842 — PRAGUE", "hold_s": 3.5}),
        ],
    ),
    (
        3,
        "Part 03 — Buys Ballot's June 1845 Steam Train of Horn Players — Midpoint Twist",
        [
            ("01_buys_ballot_june_1845_horn_train_and_huggins_1868_sirius_redshift", 99.5, 6.5, "A", False, "HIRED A TRAIN TO DEBUNK HIM", "Quality",
             "Quality: readable faces (27-year-old Christophorus Buys Ballot riding the open Utrecht–Maarssen flatbed car with brass horn players on 3 June 1845, alongside English astronomer William Huggins at his spectroscope in London in 1868 measuring the Doppler redshift of Sirius).",
             STYLE + "Split period scene: on the left on 3 June 1845, young Dutch scientist Christophorus Buys Ballot rides an open wooden railcar beside brass horn players blowing a steady note; on the right in 1868, bearded English astronomer William Huggins peers through a brass spectroscope mounted on a telescope." + QUAL_TAIL,
             {"kind": "WHO", "label": "William Huggins (1824–1910) — English astronomer", "fact_card": "Hired a train to debunk him", "when_stamp": "February 1845 · 3 June 1845 · 5 June 1845 · 1848 · 1868", "timeline_step": "4/5 · 1868 (William Huggins measures the first stellar Doppler shift in the spectral lines of Sirius)", "hold_s": 3.8}),
            ("02_buys_ballot_1845_g4_horn_392hz_to_414hz_and_372hz_pitch_chart", 106.0, 8.0, "E", False, "JUNE 1845 TRAIN HORN (G4 = 392 HZ): APPROACH 414 HZ (+1 SEMITONE) → RECEDE 372 HZ (−1 SEMITONE)", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked musical-pitch and wavelength chart from Buys Ballot's June 1845 Utrecht–Maarssen train experiments shows a sustained G4 horn note (~392 Hz): approaching at ~18 m/s (~40 mph) shifts pitch up to ~414 Hz (~G#4, +1 semitone), then drops on passing to ~372 Hz (~F#4, −1 semitone), alongside Fizeau (1848) & Huggins (1868) spectral-line redshift.",
             {"kind": "DATA", "label": "JUNE 1845 UTRECHT TRAIN: G4 HORN (392 HZ) SHIFTS TO ~414 HZ APPROACHING & ~372 HZ RECEDING", "detail": "Inked musical-pitch & wavelength chart on period paper from Buys Ballot's June 1845 Utrecht–Maarssen train experiments showing a sustained G4 horn note (~392 Hz): approaching at ~18 m/s (~40 mph) shifts pitch up to ~414 Hz (~G#4, +1 semitone), then drops on passing to ~372 Hz (~F#4, −1 semitone)", "scale": "as the locomotive passed the station platform at forty miles an hour, the horn's note plunged by nearly a full piano step in a fraction of a second", "hold_s": 3.8}),
            ("03_utrecht_maarssen_3_june_1845_flatbed_car_horn_players_passing_post", 114.0, 6.5, "B", False, "ALMOST A FULL TONE DROP", "Quality",
             "Quality: readable faces (three Dutch brass horn players on the open flatbed wagon holding a sustained G note as the steam locomotive thunders past Buys Ballot's trackside listening post on 3 June 1845).",
             STYLE + "On an open wooden flatbed railcar pulled by a steaming 1845 locomotive, three Dutch musicians in dark coats hold polished brass horns to their lips as they speed past a trackside wooden shelter where listeners take notes." + QUAL_TAIL,
             None),
            ("04_fraunhofer_stellar_spectrum_absorption_lines_redshift_plate", 120.5, 5.5, "C", False, "STELLAR REDSHIFT, 1868", "Fast",
             "Fast: daylight close-up of a brass spectroscope prism and a painted glass spectral plate showing dark vertical Fraunhofer absorption lines shifted slightly toward the red end of the rainbow band. Nothing emissive, no face.",
             STYLE + "In crisp daylight on an observatory desk, a heavy brass prism sits beside a painted glass reference strip showing a rainbow spectrum crossed by sharp dark vertical lines." + FAST_TAIL,
             None),
        ],
    ),
    (
        4,
        "Part 04 — Cracking the Whip & Ernst Mach's 1887 Supersonic Bullet Photo",
        [
            ("01_mach_and_salcher_1887_fiume_supersonic_bullet_shadowgraph", 126.0, 6.5, "A", False, "A WHIP CRACK IS A SONIC BOOM", "Quality",
             "Quality: readable faces (Austrian physicists Ernst Mach and Peter Salcher in 1887 inspecting their wet glass photographic plate showing the sharp V-shaped Mach shockwave cone around a supersonic rifle bullet).",
             STYLE + "Inside a 1887 physics laboratory, bearded Austrian physicist Ernst Mach and colleague Peter Salcher hold a glass photographic plate up to the window light, revealing the crisp V-shaped shockwave cone around a rifle bullet." + QUAL_TAIL,
             {"kind": "WHO", "label": "Peter Salcher (1848–1928) — Austrian physicist", "fact_card": "A whip crack is a sonic boom", "when_stamp": "1887 · 1929 · 14 October 1947", "hold_s": 3.8}),
            ("02_mach_salcher_1887_subsonic_transonic_mach1_and_supersonic_cone_diagram", 132.5, 8.0, "E", False, "1887 MACH & SALCHER: SUBSONIC (<343 M/S) VS MACH 1 BARRIER (343 M/S) VS SUPERSONIC CONE (485 M/S = MACH 1.4)", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked three-stage wave-front and Mach-cone diagram from Mach and Salcher's 1887 spark photographs compares subsonic motion (v < 343 m/s, nested circles), the transonic sound barrier (v = 343 m/s = Mach 1.0, wave fronts piling up at the nose), and supersonic flight (v = 485 m/s = Mach 1.4, V-shaped Mach cone with sin θ = 1 / M).",
             {"kind": "DATA", "label": "SUBSONIC (V < 343 M/S) VS SOUND BARRIER (MACH 1.0) VS SUPERSONIC MACH CONE (485 M/S = MACH 1.4)", "detail": "Inked three-stage wave-front & Mach-cone diagram on period paper from Mach & Salcher's 1887 spark photographs comparing subsonic motion (v < 343 m/s, nested circles), transonic sound barrier (v = 343 m/s = Mach 1.0, wave fronts pile up into a single wall of pressure), and supersonic flight (v = 485 m/s = Mach 1.4, V-shaped Mach cone with sin θ = 1 / M)", "scale": "a Leyden-jar spark lasting less than one-millionth of a second froze a rifle bullet moving at five hundred metres per second into a crystal-clear shadow on glass", "hold_s": 3.8}),
            ("03_tapered_leather_bullwhip_loop_uncoiling_in_daylight_closeup", 140.5, 6.5, "B", False, "FIUME, 1887 — THE MACH CONE", "Fast",
             "Fast: daylight slow-motion view of a braided leather bullwhip uncoiling through the air as the tapered cracker tip snaps cleanly past a framed 1887 glass negative of the Mach cone. Nothing emissive, no face.",
             STYLE + "In bright outdoor daylight against a clear sky, a braided brown leather bullwhip uncoils in a smooth loop as its narrow tip snaps sharply forward." + FAST_TAIL,
             None),
            ("04_explorer_schlieren_camera_freezing_supersonic_bullet_mach_cone", 147.0, 5.5, "B", True, None, "Quality",
             "Quality: Explorer beat 2 (locked character reference).",
             STYLE + "Standing beside a brass optical schlieren mirror and glass photographic plate holder, the Explorer pulls a shutter cord just as a brass bullet streaks through a wire frame, revealing a crisp V-shaped cone of compressed air ripples frozen in the frame." + EXP_TAIL,
             None),
        ],
    ),
    (
        5,
        "Part 05 — The Sonic Boom Myth, Medical Ultrasound & the 16 Horses That Couldn't Pull Two Bowls Apart",
        [
            ("01_timeline_1738_1887_and_continuous_sonic_boom_carpet_ultrasound_chart", 152.5, 8.5, "E", False, "1738–1887 TIMELINE · CONTINUOUS SONIC-BOOM WAKE (MACH 2 = 686 M/S) · DOPPLER ULTRASOUND", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, the 5-date timeline completes: 1738 (French Academy cannon-flash experiments clock sound at 331 m/s at 0 °C) · 25 May 1842 (Christian Doppler presents his wave-shift equation in Prague) · 3–5 Jun 1845 (Buys Ballot's Utrecht steam-train horn experiment) · 1868 (William Huggins measures the first stellar Doppler shift in Sirius) · 1887 (Ernst Mach & Peter Salcher photograph the supersonic bullet shockwave cone), alongside an inked diagram of a supersonic aircraft dragging a continuous Mach shockwave wake across the ground and 1957 Doppler medical ultrasound.",
             {"kind": "DATA", "label": "1738–1887 TIMELINE & CONTINUOUS MACH SHOCKWAVE CONE (MACH 2 = 686 M/S) + DOPPLER ULTRASOUND", "detail": "Animated 5-date timeline (1738 → 1887) alongside an inked diagram showing a supersonic jet dragging a continuous conical Mach shockwave wake across the ground (v = 686 m/s = Mach 2.0) and medical Doppler ultrasound measuring blood flow", "scale": "a supersonic jet at Mach 2 drags a continuous cone of compressed air across the ground at nearly seven hundred metres per second — twice as fast as a rifle shot", "fact_card": "Sonic booms never stop in flight", "when_stamp": "1957 · 1738–1887", "timeline_step": "5/5 · 1887 (Ernst Mach & Peter Salcher photograph the supersonic bullet shockwave cone)", "hold_s": 3.8}),
            ("02_speedboat_v_wake_and_supersonic_cone_model_comparison", 161.0, 5.5, "A", False, "A CONTINUOUS SHOCKWAVE WAKE", "Fast",
             "Fast: daylight side-by-side tabletop model comparing a wooden speedboat hull carving a continuous V-shaped bow wake in water with a sleek brass aircraft model mounted inside a translucent V-shaped Mach cone sweeping across a map. Nothing emissive, no face.",
             STYLE + "In crisp daylight on a demonstration table, a wooden boat model in a glass water channel carving a V-shaped wake sits beside a polished brass aircraft model surrounded by a translucent V-shaped cone sweeping over a relief map." + FAST_TAIL,
             None),
            ("03_torricelli_1643_mercury_barometer_and_guericke_1654_magdeburg_horses_handoff", 166.5, 6.5, "C", False, "SIXTEEN HORSES AND NO BOLTS", "Quality",
             "Quality: readable faces (Evangelista Torricelli and Vincenzo Viviani in Florence in June 1644 inverting a four-foot glass tube of mercury into a dish to create the first barometer and vacuum, beside Otto von Guericke in Regensburg on 8 May 1654 as sixteen horses strain in vain to pull two evacuated copper Magdeburg hemispheres apart — handoff to 039 Atmospheric Pressure & Vacuum).",
             STYLE + "Split period scene: on the left in Florence in 1644, Italian physicist Evangelista Torricelli holds an inverted four-foot glass tube of silvery mercury in a porcelain basin; on the right in Regensburg on 8 May 1654, Otto von Guericke watches two teams of eight horses strain against ropes tied to two joined copper hemispheres." + QUAL_TAIL,
             {"kind": "WHEN", "label": "1643 · 19 SEPTEMBER 1648 · 8 MAY 1654", "hold_s": 3.5}),
            ("04_table_three_callback", 173.0, 2.4, "C", False, None, "reuse",
             "Reuse: verified unused moving window [5.50s..7.90s] of P1:07_table_three_props_doppler_treatise_brass_horn_mach_shadowgraph_plate (callback, £0).",
             "Reuse P1:07_table_three_props_doppler_treatise_brass_horn_mach_shadowgraph_plate [5.50s..7.90s] (2.40s distinct non-overlapping tail window from 8.00s source clip).",
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
                row["reuse_of"] = "P1:07_table_three_props_doppler_treatise_brass_horn_mach_shadowgraph_plate"
                row["reuse_window_s"] = [5.5, 7.9]
                row["reuse_audit"] = {
                    "source_row": "P1:07_table_three_props_doppler_treatise_brass_horn_mach_shadowgraph_plate",
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
            "film": "038_Doppler-BuysBallot-Mach-Sound-Waves",
            "part": p_idx,
            "title": p_title,
            "version": "v01",
            "timing_status": "pre_vo_script_clock (built from doppler_script_master_v01.md; retimes onto Scribe STT once VO locks)",
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
        "film": "038_Doppler-BuysBallot-Mach-Sound-Waves",
        "version": "v01",
        "date": "2026-10-18",
        "owner": "gemini (J0524)",
        "status": "PRE_VO_BOARDS_V01_NO_MINT",
        "generation_authorized": False,
        "script": "00_Brand/Channel-Setup/ideas/038_Doppler-BuysBallot-Mach-Sound-Waves/doppler_script_master_v01.md",
        "sources": "00_Brand/Channel-Setup/ideas/038_Doppler-BuysBallot-Mach-Sound-Waves/SOURCES_v01.md",
        "credit_snapshot": {
            "flow_balance": 23740,
            "flow_floor": 0,
            "flow_read_at": "2026-10-15T21:42:22Z",
            "vertex_promo_gbp": 71.02,
            "vertex_usable_gbp": 70.02,
        },
        "totals": totals,
        "per_part": per_part_summary,
        "mint_order": "006 > 007 > 008 > 009 > 010 > 011 > 012 > 013 > 014 > 015 > 016 > 017 > 018 > 019 > 020 > 021 > 022 > 023 > 024 > 025 > 026 > 027 > 028 > 029 > 030 > 031 > 032 > 033 > 034 > 035 > 036 > 037 > 038. Nothing in 038 is generation_authorized.",
    }
    (EDIT / "PICTURE_PLAN_v01.json").write_text(json.dumps(plan, indent=2) + "\n")

    sl = [
        "# 038 The Doppler Effect: The 1845 Train of Trumpets That Proved It — Shot list & plate boards v01 (pre-VO)",
        "",
        "Gemini, 18 Oct 2026, J0524. Built from `doppler_script_master_v01.md` (`94.1 PASS`) and `SOURCES_v01.md`.",
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
        "# 038 price review v01 (pre-VO plate boards)",
        "",
        "Gemini, 18 Oct 2026, J0524. Boards only. **No mint. No spend. No merge.**",
        "Prepared from `doppler_script_master_v01.md` (`94.1 PASS`) and `SOURCES_v01.md` so 038's full plate board rows, non-emissive Fast prompts, £0 code graphics, and Teach-on-Screen overlays are ready to re-time the moment long VO locks. Parked for Chief.",
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
        f"- **Quality ({totals['Quality']} rows):** readable faces (Christian Doppler, Christophorus Buys Ballot, Ernst Mach, Peter Salcher, William Huggins, Evangelista Torricelli, Otto von Guericke), 1738 hilltop cannon observers, 1845 Utrecht horn-train scenes, and the 2 Explorer beats.",
        f"- **Fast ({totals['Fast']} rows, non-emissive):** daylight prop and laboratory shots (coiled brass valved post horn, tuning fork & pocket stopwatch pan, 3-object callback bench, brass helical spring compression/rarefaction wave model, Doppler's 1842 Prague manuscript & sailing-ship wave tray, brass spectroscope prism & Fraunhofer redshift plate, braided leather bullwhip loop in daylight, speedboat wake vs Mach cone model). Zero candles, flames, sparks, or glowing elements on Fast.",
        f"- **£0 code graphics ({totals['code_graphic']} rows):**",
        "  1. `P1:04_doppler_1842_wave_bunching_343_ms_and_40_mph_train_pitch_shift_chart` — sound at 343 m/s (767 mph at 20 °C) and a 40 mph (~18 m/s) train shifting a horn note by ~10% (~1 musical whole tone) (`SCALE: a steam train chugging at just forty miles an hour — barely one-twentieth the speed of sound — squashes and stretches the sound waves enough to drop a trumpet's note by nearly a full piano key as it passes your ear`)",
        "  2. `P1:06_speed_scale_bar_40mph_train_vs_343ms_mach1_vs_500ms_rifle_bullet_card` — 1845 steam train (~18 m/s = Mach 0.05) vs speed of sound in air at 20 °C (343 m/s = Mach 1.0) vs 1887 rifle bullet (~440–530 m/s = Mach 1.3–1.5) (`SCALE: sound races through mild air at 343 metres per second — the length of three and a half football pitches every single second`)",
        "  3. `P2:02_1738_french_academy_cannon_29km_331ms_and_doppler_1842_formula_diagram` — 1738 French Academy cannon flash-vs-boom timing across ~29 km (88 s = 331 m/s at 0 °C) + Christian Doppler's 25 May 1842 wave formula (`SCALE: light crosses twenty-nine kilometres in less than a ten-thousandth of a second — whereas the cannon's sound wave takes a full eighty-eight seconds to march across the same valley`)",
        "  4. `P3:02_buys_ballot_1845_g4_horn_392hz_to_414hz_and_372hz_pitch_chart` — Buys Ballot's June 1845 Utrecht train G4 horn note (~392 Hz) shifting to ~414 Hz approaching (+1 semitone) and ~372 Hz receding (−1 semitone) (`SCALE: as the locomotive passed the station platform at forty miles an hour, the horn's note plunged by nearly a full piano step in a fraction of a second`)",
        "  5. `P4:02_mach_salcher_1887_subsonic_transonic_mach1_and_supersonic_cone_diagram` — Mach & Salcher's 1887 subsonic (<343 m/s) vs Mach 1 sound barrier (343 m/s) vs Mach 1.4 supersonic bullet cone (`sin θ = 1 / M`) (`SCALE: a Leyden-jar spark lasting less than one-millionth of a second froze a rifle bullet moving at five hundred metres per second into a crystal-clear shadow on glass`)",
        "  6. `P5:01_timeline_1738_1887_and_continuous_sonic_boom_carpet_ultrasound_chart` — completed 5-date timeline (1738 → 1887) + continuous Mach shockwave wake (Mach 2 = 686 m/s) & Doppler medical ultrasound (`SCALE: a supersonic jet at Mach 2 drags a continuous cone of compressed air across the ground at nearly seven hundred metres per second — twice as fast as a rifle shot`)",
        f"- **£0 verified reuse ({totals['reuse']} row):** `P5:04_table_three_callback` uses the 2.40 s unused moving tail `[5.50s..7.90s]` of `P1:07_table_three_props_doppler_treatise_brass_horn_mach_shadowgraph_plate`.",
        "",
        "## Mint order",
        "",
        "006 > 007 > 008 > 009 > 010 > 011 > 012 > 013 > 014 > 015 > 016 > 017 > 018 > 019 > 020 > 021 > 022 > 023 > 024 > 025 > 026 > 027 > 028 > 029 > 030 > 031 > 032 > 033 > 034 > 035 > 036 > 037 > 038. `generation_authorized` is `false` on every row.",
    ])
    (EDIT / "PRICE_REVIEW_v01.md").write_text("\n".join(pr_lines) + "\n")
    print(f"038 v01 boards written: {totals['rows']} rows, Flow expected={totals['flow_credits_expected']}")


if __name__ == "__main__":
    main()
