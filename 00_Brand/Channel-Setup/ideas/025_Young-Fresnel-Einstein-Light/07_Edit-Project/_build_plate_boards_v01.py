#!/usr/bin/env python3
"""HOS 025 (The Double-Slit Experiment: How a Playing Card Broke Physics) pre-VO plate boards v01. J0448. No mint, no spend.

Built from 00_Brand/Channel-Setup/ideas/025_Young-Fresnel-Einstein-Light/young_script_master_v01.md
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
        "Part 01 — The Card in the Sunbeam",
        [
            ("01_young_playing_card_sunbeam_fringes_1801", 0.0, 5.5, "A", False, "LIGHT + LIGHT = DARKNESS", "Quality",
             "Quality: Short frame 0 / answer image (0:03) + Thomas Young holding the thin edge of a playing card inside a narrow pinhole sunbeam on 24 November 1801 as the shadow on the wall breaks into glowing interference stripes with a bright central band.",
             STYLE + "In a darkened London room on 24 November 1801, physician Thomas Young holds the thin edge of a playing card inside a narrow pinhole sunbeam; on the wall behind the card, the shadow breaks into glowing rainbow-edged interference stripes with a bright white band right down the middle." + QUAL_TAIL,
             {"kind": "WHEN", "label": "LONDON · 24 NOVEMBER 1801", "timeline_step": "2/7 · 24 Nov 1801 & 1803 (Young's playing-card wave interference)", "hold_s": 3.5}),
            ("02_young_card_arago_bright_spot_einstein_uv_split", 5.5, 6.0, "B", False, "CARD, BRIGHT SPOT, PHOTON", "Quality",
             "Quality: readable faces (Thomas Young splitting a sunbeam in London, François Arago peering at the bright spot in Paris, and Albert Einstein in Bern watching UV light eject electrons).",
             STYLE + "Three-panel period composition: on the left, Thomas Young holds a playing card in a sunbeam; in the centre, François Arago peers at a bright star of light in the middle of a circular shadow; on the right, young Albert Einstein watches ultraviolet light strike a metal plate." + QUAL_TAIL,
             None),
            ("03_newton_opticks_and_two_slit_bullet_piles", 11.5, 6.0, "C", False, "TINY BULLETS OF LIGHT?", "Fast",
             "Fast: daylight wooden lectern holding a leather-bound seventeenth-century optics volume beside a brass two-slit screen where tiny silver bearings roll through in straight lines into two simple heaps. No readable text on plate, nothing emissive.",
             STYLE + "In crisp daylight on a wooden lectern, an open leather-bound optics volume sits beside a tabletop model where tiny silver ball bearings roll in straight lines through two slots to form two simple piles behind." + FAST_TAIL,
             {"kind": "WHEN", "label": "1704–1801", "timeline_step": "1/7 · 1704 (Newton's Opticks particle theory)", "hold_s": 3.5}),
            ("04_young_wavelength_1_36000_red_to_1_60000_violet_chart", 17.5, 8.0, "E", False, "1/36,000 IN RED · 1/60,000 IN VIOLET", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked wave-interference diagram shows two light waves meeting crest-to-crest (bright band) and crest-to-trough (dark band), alongside Young's 1801 wavelength table: Red light = 1/36,000 inch (~700 nm) to Violet light = 1/60,000 inch (~420 nm).",
             {"kind": "DATA", "label": "RED 1/36,000 IN (~700 NM) · VIOLET 1/60,000 IN (~420 NM)", "detail": "Inked wave-interference diagram and wavelength scale comparing Young's 1801 measurements of Red light (1/36,000 in = ~700 nm) and Violet light (1/60,000 in = ~420 nm) against a human hair (~75,000 nm)", "scale": "one fifty-thousandth of an inch from crest to crest — more than a hundred waves of light fit side by side across the width of a single human hair", "who_card": "Thomas Young (1773–1829) — English physician and polymath", "when_stamp": "24 November 1801", "hold_s": 3.8}),
            ("05_clamped_playing_card_and_shutter_pinhole_pan", 25.5, 5.5, "A", False, "1/30TH-INCH CARD SLIP", "Fast",
             "Fast: daylight pan across a brass clamp holding a thin slip of playing card (1/30th inch thick) and a fine needle beside a wooden window shutter between code graphics so two full-frame graphics never run back to back.",
             STYLE + "In soft window light, the camera tracks across a brass table clamp holding the thin edge of a playing card beside a fine sewing needle and a brass micrometer screw." + FAST_TAIL,
             None),
            ("06_150_light_waves_across_one_human_hair_scale_chart", 31.0, 8.0, "E", False, "150 WAVES IN A HAIR", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period parchment, an inked scale diagram compares a single human hair (75 micrometres wide) spanning ~150 wavelengths of green-yellow light (~500 nanometres each) against Young's 1/30th-inch (~0.85 mm) playing card.",
             {"kind": "DATA", "label": "~150 LIGHT WAVES (500 NM) ACROSS 1 HUMAN HAIR (75 µM)", "detail": "Inked size comparison showing ~150 visible light wavelengths (~500 nm each) fitting side by side across 1 human hair (75 µm wide)", "scale": "150 light waves across one strand of hair — no wonder shadows look sharp to the naked eye", "hold_s": 3.8}),
            ("07_table_three_props_playing_card_2mm_disc_photoelectric_plate", 39.0, 5.5, "C", False, "LONDON, NOVEMBER 1801", "Fast",
             "Fast: daylight prop table (callback source for Part 05: brass-clamped playing card slip, 2 mm brass disc mounted on glass plate, zinc photoelectric plate with quartz window). Nothing emissive.",
             STYLE + "On a wooden laboratory workbench in soft window light sit three objects side by side: a thin playing card held vertically in a brass clamp, a two-millimetre brass disc mounted on a clear glass square, and a polished zinc plate beside a brass electroscope." + FAST_TAIL,
             None),
            ("08_explorer_blocking_one_side_of_playing_card", 62.0, 5.5, "A", True, None, "Quality",
             "Quality: Explorer beat 1 (locked character reference, after 1:00).",
             STYLE + "Standing on the wooden table behind the clamped playing card, the Explorer slides a tiny brass screen to block the light passing on the left side of the card, gasps as the bright stripes inside the shadow on the wall vanish, and pulls the screen back to watch the stripes return." + EXP_TAIL,
             None),
            ("09_one_side_blocked_fringes_vanish_closeup", 67.5, 5.5, "B", False, "FRINGES VANISH", "Quality",
             "Quality: close-up of the glowing interference fringes inside the card's shadow instantly disappearing into a smooth dim edge the moment a small brass screen blocks one side of the sunbeam.",
             STYLE + "Close view of a wall screen where bright and dark interference stripes glow inside a narrow shadow; as a small brass blade slides in to block one side of the card, the internal stripes vanish immediately." + QUAL_TAIL,
             None),
        ],
    ),
    (
        2,
        "Part 02 — The Man Who Read the Rosetta Stone and Split a Sunbeam",
        [
            ("01_young_rosetta_stone_and_organ_pipes_huygens", 73.0, 6.5, "A", False, "LONDON · 1801 & 1814", "Quality",
             "Quality: readable face (twenty-eight-year-old Thomas Young examining royal cartouches on a plaster cast of the Rosetta Stone and comparing organ pipes with Christiaan Huygens's wave treatise).",
             STYLE + "London, 1801 and 1814: physician Thomas Young in a dark Georgian coat traces the carved oval cartouche on a plaster cast of the Rosetta Stone, then holds two brass organ pipes beside an open wave diagram." + QUAL_TAIL,
             {"kind": "WHO", "label": "Christiaan Huygens (1629–1695) — Dutch physicist and astronomer", "fact_card": "Also cracked Rosetta Stone", "when_stamp": "1690 · 1814", "hold_s": 3.8}),
            ("02_crest_plus_crest_vs_crest_plus_trough_diagram", 79.5, 8.0, "E", False, "CREST + TROUGH = DARKNESS", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked interference path-difference diagram shows crest + crest = 2× amplitude (bright fringe at path difference 0, 1λ, 2λ) and crest + trough = 0 (dark fringe at path difference 0.5λ, 1.5λ), alongside Young's 24 November 1803 single-side blocking test.",
             {"kind": "DATA", "label": "ΔL = 0, 1λ → BRIGHT · ΔL = 0.5λ, 1.5λ → DARK", "detail": "Inked interference path-difference diagram showing crest + crest = bright fringe (at path difference 0, 1λ, 2λ) and crest + trough = dark fringe (at path difference 0.5λ, 1.5λ)", "scale": "moving just one fifty-thousandth of an inch sideways on the wall turns bright sunlight into pitch darkness", "when_stamp": "24 November 1803", "hold_s": 3.8}),
            ("03_brougham_edinburgh_review_and_unsold_pamphlets_1804", 87.5, 6.5, "B", False, "1 COPY SOLD IN 1804", "Quality",
             "Quality: readable face (Henry Brougham writing his attack in Edinburgh while stacks of Thomas Young's 1804 reply pamphlet sit untouched on a London bookshop counter).",
             STYLE + "Split period scene: on the left, Scottish reviewer Henry Brougham scowls as he writes with a quill pen; on the right, tall tied stacks of printed pamphlets sit untouched on a quiet London bookshop counter." + QUAL_TAIL,
             {"kind": "WHO", "label": "Henry Brougham (1778–1868) — Scottish writer and politician", "fact_card": "Pamphlet sold just 1 copy", "when_stamp": "1803 · 1804", "hold_s": 3.8}),
            ("04_ripple_tank_water_waves_overlapping_bench", 94.0, 5.5, "C", False, "TWO WAVE SOURCES", "Fast",
             "Fast: daylight top-down view of a shallow glass water tray where two brass pins dip in step, sending concentric ripples overlapping into clear calm lanes and oscillating crests. Nothing emissive, no face.",
             STYLE + "In crisp daylight, two brass pins dip rhythmically into a shallow glass tray of water, sending overlapping circular ripples across the surface with clear calm radial lanes between moving wave crests." + FAST_TAIL,
             None),
        ],
    ),
    (
        3,
        "Part 03 — The Trap That Backfired — Poisson's Bright Spot",
        [
            ("01_fresnel_honey_drop_lens_and_1818_paris_committee", 99.5, 6.5, "A", False, "PARIS · 1818 GRAND PRIX", "Quality",
             "Quality: readable faces (thirty-year-old Augustin-Jean Fresnel focusing sunlight through a honey drop in 1815, then facing the 1818 French Academy committee of Laplace, Biot, Poisson, and Arago).",
             STYLE + "France, 1815 and Paris, 1818: young engineer Augustin-Jean Fresnel examines a golden drop of honey filling a tiny hole in a metal sheet, then stands before the French Academy committee of Pierre-Simon Laplace, Jean-Baptiste Biot, Siméon Denis Poisson and François Arago." + QUAL_TAIL,
             {"kind": "WHO", "label": "Augustin-Jean Fresnel (1788–1827) — French civil engineer · Pierre-Simon Laplace (1749–1827) — French mathematician · Jean-Baptiste Biot (1774–1862) — French physicist · Siméon Denis Poisson (1781–1840) — French mathematician · François Arago (1786–1853) — French astronomer", "fact_card": "Used honey drop as a lens", "when_stamp": "France, 1815 · Paris, 1818", "hold_s": 3.8}),
            ("02_poisson_2mm_disc_equal_path_bright_spot_diagram", 106.0, 8.0, "E", False, "2 MM DISC · ΔL = 0 AT SHADOW CENTRE", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked circular-diffraction geometry diagram shows a 2-millimetre opaque metal disc where every wave bending around the circular rim travels the exact same distance √(R² + L²) to the dead centre of the shadow (ΔL = 0), summing crest-to-crest to form Poisson's/Arago's bright spot.",
             {"kind": "DATA", "label": "2 MM DISC · EQUAL RIM PATH √(R² + L²) → BRIGHT SPOT", "detail": "Inked circular-diffraction geometry diagram showing a 2 mm opaque metal disc where every ray from the circular rim travels the exact same path length √(R² + L²) to the centre of the shadow (ΔL = 0)", "scale": "behind a solid 2-millimetre metal coin-like disc, every wave around the rim meets in step to light up the dead centre of the dark shadow", "hold_s": 3.8}),
            ("03_arago_observing_bright_spot_behind_2mm_disc_1819", 114.0, 6.5, "B", False, "THE BRIGHT SPOT IN THE SHADOW", "Quality",
             "Quality: readable face (François Arago in the Paris Observatory laboratory in March 1819 peering through a magnifying eyepiece at the unmistakable bright star of light in the dead centre of the 2 mm disc's circular shadow).",
             STYLE + "Paris Observatory, March 1819: astronomer François Arago glues a two-millimetre brass disc onto a clear glass plate with wax, illuminates it with a pinpoint beam, and gasps as a crisp bright star of light shines right at the dead centre of the dark circular shadow." + QUAL_TAIL,
             {"kind": "WHEN", "label": "15 MARCH 1819", "timeline_step": "3/7 · 15 Mar 1819 (Fresnel & Arago's 2 mm disc bright spot)", "hold_s": 3.5}),
            ("04_2mm_brass_disc_on_glass_plate_wax_closeup", 120.5, 5.5, "C", False, "2-MILLIMETRE BRASS DISC", "Fast",
             "Fast: daylight macro view of the tiny 2-millimetre circular brass disc fixed with a dab of beeswax to the middle of a square glass plate held in a brass stand. Nothing emissive, no face.",
             STYLE + "In crisp daylight, brass tweezers press a tiny two-millimetre circular brass disc onto a dab of beeswax at the centre of a clear glass plate mounted in a brass holder." + FAST_TAIL,
             None),
        ],
    ),
    (
        4,
        "Part 04 — The Ultraviolet Puzzle and Einstein's Heresy",
        [
            ("01_hertz_lenard_red_vs_ultraviolet_photoelectric", 126.0, 6.5, "A", False, "BRIGHT RED FAILS, DIM UV WORKS", "Quality",
             "Quality: readable faces (Heinrich Hertz and Philipp Lenard testing a clean metal plate where bright red light ejects zero electrons while dim violet/UV light deflects the electrometer immediately).",
             STYLE + "Karlsruhe and Kiel, 1887–1902: physicists Heinrich Hertz and Philipp Lenard shine an intense red beam onto a polished metal plate in a glass tube with zero effect on the gold-leaf electroscope, then switch to a dim violet-ultraviolet beam that makes the electroscope leaf spring wide immediately." + QUAL_TAIL,
             {"kind": "WHO", "label": "Heinrich Hertz (1857–1894) — German physicist · Philipp Lenard (1862–1947) — Hungarian-German physicist", "when_stamp": "1887 · 1902", "timeline_step": "4/7 · 1887–1902 (Hertz & Lenard photoelectric paradox)", "hold_s": 3.8}),
            ("02_einstein_1905_photoelectric_kmax_hf_threshold_chart", 132.5, 8.0, "E", False, "E = HF · K_MAX = HF - Φ", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked photoelectric threshold graph plots maximum electron kinetic energy K_max against light frequency f (K_max = hf - φ): below threshold f_0 (red light), 0 electrons emitted regardless of brightness; above f_0 (UV light), electron energy rises linearly with slope h = 6.626 × 10⁻³⁴ J·s.",
             {"kind": "DATA", "label": "K_MAX = HF - Φ (0 ELECTRONS BELOW THRESHOLD F_0)", "detail": "Inked photoelectric threshold graph plotting maximum electron kinetic energy K_max against light frequency f (K_max = hf - φ, slope h = 6.626 × 10⁻³⁴ J·s) from Albert Einstein's 17 March 1905 paper", "scale": "a billion red photons hit the metal like ping-pong balls and knock loose zero electrons — while a single ultraviolet photon hits like a cannonball and kicks an electron straight out", "who_card": "Albert Einstein (1879–1955) — Swiss patent clerk and physicist · Max Planck (1858–1947) — German theoretical physicist", "when_stamp": "December 1900 · Bern, 17 March 1905", "timeline_step": "5/7 · 17 Mar 1905 (Einstein's E = hf light quanta)", "hold_s": 3.8}),
            ("03_planck_1913_and_millikan_1916_confirming_einstein", 140.5, 6.5, "B", False, "1921 NOBEL FOR PHOTOELECTRIC", "Quality",
             "Quality: readable faces (Max Planck in Berlin in 1913 and American experimentalist Robert Millikan in his Chicago laboratory in 1916 confirming Einstein's photoelectric line and winning Einstein the 1921 Physics Nobel).",
             STYLE + "Split period portrait: on the left, Max Planck stands in Berlin holding a formal recommendation scroll; on the right, American physicist Robert Millikan in Chicago adjusts his vacuum photoelectric wheel and nods in astonished confirmation." + QUAL_TAIL,
             {"kind": "WHO", "label": "Robert Millikan (1868–1953) — American experimental physicist", "fact_card": "Nobel was for photoelectric, not E=mc²", "when_stamp": "1913 · 1916 · 1921", "hold_s": 3.8}),
            ("04_explorer_red_pingpong_balls_vs_violet_cannonball", 147.0, 5.5, "B", True, None, "Quality",
             "Quality: Explorer beat 2 (locked character reference).",
             STYLE + "Standing beside the metal photoelectric plate, the Explorer tosses a handful of small red wooden balls at a latched brass trapdoor without budging it, then rolls a single heavy violet sphere that pops the latch open on the first hit." + EXP_TAIL,
             None),
        ],
    ),
    (
        5,
        "Part 05 — Firing One Photon at a Time and How Your Camera Sees",
        [
            ("01_timeline_1704_1921_and_single_photon_dot_buildup", 152.5, 8.5, "E", False, "1 PHOTON AT A TIME → WAVE STRIPES", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, the 7-date timeline completes: 1704 (Newton's Opticks) · 24 Nov 1801 & 1803 (Young's card) · 15 Mar 1819 (Fresnel & Arago bright spot) · 1887–1902 (Photoelectric paradox) · 17 Mar 1905 (Einstein E=hf quanta) · 1909 (G. I. Taylor single-photon interference) · 1921 (Einstein Physics Nobel), alongside an inked single-photon accumulation chart (10 photons → 1,000 photons → 100,000 photons building Young's stripes dot by dot).",
             {"kind": "DATA", "label": "10 → 1,000 → 100,000 SINGLE PHOTONS BUILD WAVE STRIPES", "detail": "Animated 7-date timeline (1704 → 1921) alongside an inked single-photon detector accumulation chart showing individual particle hits summing into Thomas Young's interference bands", "scale": "firing one single photon at a time with kilometres of empty space between them — and they still build Young's exact wave stripes dot by dot", "who_card": "Geoffrey Ingram Taylor (1886–1975) — Cambridge physicist · Louis de Broglie (1892–1987) — French quantum physicist", "when_stamp": "1909 · 1924 · 1704–1921", "timeline_step": "6/7 · 1909 (G. I. Taylor single-photon test) & 7/7 · 1921 (Einstein Physics Nobel)", "hold_s": 3.8}),
            ("02_taylor_light_tight_box_and_camera_lens_sensor", 161.0, 5.5, "A", False, "WAVE IN FLIGHT, PARTICLE ON IMPACT", "Fast",
             "Fast: daylight close-up of a wooden light-tight diffraction box beside a glass camera lens focusing daylight onto a grid of metallic silicon sensor squares. Nothing emissive, no face.",
             STYLE + "In crisp daylight on a laboratory bench, a long light-tight mahogany box with smoked-glass filters sits beside a cutaway brass camera lens focusing light onto a fine grid of metallic sensor tiles." + FAST_TAIL,
             None),
            ("03_haber_200atm_ammonia_and_lovelace_note_g_handoff", 166.5, 6.5, "C", False, "TURNING AIR INTO BREAD", "Quality",
             "Quality: Fritz Haber and Robert Le Rossignol in Karlsruhe on 2 July 1909 watching silver drops of liquid ammonia condense inside a high-pressure steel reactor at 200 atmospheres, dissolving into Ada Lovelace's 1843 Note G table (handoff to 026 Haber-Bosch).",
             STYLE + "Karlsruhe, 2 July 1909: chemist Fritz Haber and engineer Robert Le Rossignol peer at a thick-walled steel high-pressure tube with a brass gauge at 200 atmospheres as clear drops of liquid ammonia drip into a cold glass receiver, dissolving into brass Analytical Engine gears." + QUAL_TAIL,
             {"kind": "WHEN", "label": "2 JULY 1909 · AUGUST 1843", "hold_s": 3.5}),
            ("04_table_three_callback", 173.0, 2.4, "C", False, None, "reuse",
             "Reuse: verified unused moving window [5.50s..7.90s] of P1:07_table_three_props_playing_card_2mm_disc_photoelectric_plate (callback, £0).",
             "Reuse P1:07_table_three_props_playing_card_2mm_disc_photoelectric_plate [5.50s..7.90s] (2.40s distinct non-overlapping tail window from 8.00s source clip).",
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
                row["reuse_of"] = "P1:07_table_three_props_playing_card_2mm_disc_photoelectric_plate"
                row["reuse_window_s"] = [5.5, 7.9]
                row["reuse_audit"] = {
                    "source_row": "P1:07_table_three_props_playing_card_2mm_disc_photoelectric_plate",
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
            "film": "025_Young-Fresnel-Einstein-Light",
            "part": p_idx,
            "title": p_title,
            "version": "v01",
            "timing_status": "pre_vo_script_clock (built from young_script_master_v01.md; retimes onto Scribe STT once VO locks)",
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
        "film": "025_Young-Fresnel-Einstein-Light",
        "version": "v01",
        "date": "2026-10-17",
        "owner": "gemini (J0448)",
        "status": "PRE_VO_BOARDS_V01_NO_MINT",
        "generation_authorized": False,
        "script": "00_Brand/Channel-Setup/ideas/025_Young-Fresnel-Einstein-Light/young_script_master_v01.md",
        "sources": "00_Brand/Channel-Setup/ideas/025_Young-Fresnel-Einstein-Light/SOURCES_v01.md",
        "credit_snapshot": {
            "flow_Balance": 23740,
            "flow_floor": 0,
            "flow_read_at": "2026-10-15T21:42:22Z",
            "vertex_promo_gbp": 71.02,
            "vertex_usable_gbp": 70.02,
        },
        "totals": totals,
        "per_part": per_part_summary,
        "mint_order": "006 > 007 > 008 > 009 > 010 > 011 > 012 > 013 > 014 > 015 > 016 > 017 > 018 > 019 > 020 > 021 > 022 > 023 > 024 > 025. Nothing in 025 is generation_authorized.",
    }
    (EDIT / "PICTURE_PLAN_v01.json").write_text(json.dumps(plan, indent=2) + "\n")

    sl = [
        "# 025 The Double-Slit Experiment: How a Playing Card Broke Physics — Shot list & plate boards v01 (pre-VO)",
        "",
        "Gemini, 17 Oct 2026, J0448. Built from `young_script_master_v01.md` (91.0 PASS) and `SOURCES_v01.md`.",
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
        "# 025 price review v01 (pre-VO plate boards)",
        "",
        "Gemini, 17 Oct 2026, J0448. Boards only. **No mint. No spend. No merge.**",
        "Prepared from `young_script_master_v01.md` (91.0 PASS) and `SOURCES_v01.md` so 025's full plate board rows, non-emissive Fast prompts, £0 code graphics, and Teach-on-Screen overlays are ready to re-time the moment long VO locks. Parked for Chief.",
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
        f"- **Quality ({totals['Quality']} rows):** readable faces (Thomas Young, Henry Brougham, Augustin-Jean Fresnel, Pierre-Simon Laplace, Jean-Baptiste Biot, Siméon Denis Poisson, François Arago, Heinrich Hertz, Philipp Lenard, Albert Einstein, Max Planck, Robert Millikan, Fritz Haber, Robert Le Rossignol), emissive/sunbeam scenes (24 Nov 1801 playing-card sunbeam answer image, vanishing interference fringes), and the 2 Explorer beats.",
        f"- **Fast ({totals['Fast']} rows, non-emissive):** daylight prop and laboratory shots (Newton Opticks & two-slit ball-bearing model, clamped 1/30th-inch playing card & micrometer pan, 3-object callback bench, ripple tank water waves, 2 mm brass disc mounted with beeswax on glass, G. I. Taylor light-tight diffraction box & cutaway camera lens/silicon sensor). Zero candles, flames, sparks, or glowing elements on Fast.",
        f"- **£0 code graphics ({totals['code_graphic']} rows):**",
        "  1. `P1:04_young_wavelength_1_36000_red_to_1_60000_violet_chart` — Young's 1801 wave interference and wavelength table from Red (1/36,000 in = ~700 nm) to Violet (1/60,000 in = ~420 nm) (`SCALE: one fifty-thousandth of an inch from crest to crest — more than a hundred waves of light fit side by side across the width of a single human hair`)",
        "  2. `P1:06_150_light_waves_across_one_human_hair_scale_chart` — ~150 visible light wavelengths (~500 nm each) fitting across 1 human hair (75 µm) (`SCALE: 150 light waves across one strand of hair — no wonder shadows look sharp to the naked eye`)",
        "  3. `P2:02_crest_plus_crest_vs_crest_plus_trough_diagram` — path-difference interference diagram (crest + crest = bright, crest + trough = dark) (`SCALE: moving just one fifty-thousandth of an inch sideways on the wall turns bright sunlight into pitch darkness`)",
        "  4. `P3:02_poisson_2mm_disc_equal_path_bright_spot_diagram` — circular diffraction geometry around a 2 mm opaque metal disc (ΔL = 0 at shadow centre) (`SCALE: behind a solid 2-millimetre metal coin-like disc, every wave around the rim meets in step to light up the dead centre of the dark shadow`)",
        "  5. `P4:02_einstein_1905_photoelectric_kmax_hf_threshold_chart` — Einstein's 17 March 1905 photoelectric threshold graph K_max = hf - φ (`SCALE: a billion red photons hit the metal like ping-pong balls and knock loose zero electrons — while a single ultraviolet photon hits like a cannonball and kicks an electron straight out`)",
        "  6. `P5:01_timeline_1704_1921_and_single_photon_dot_buildup` — completed 7-date timeline (1704 → 1921) + G. I. Taylor 1909 single-photon interference buildup (`SCALE: firing one single photon at a time with kilometres of empty space between them — and they still build Young's exact wave stripes dot by dot`)",
        f"- **£0 verified reuse ({totals['reuse']} row):** `P5:04_table_three_callback` uses the 2.40 s unused moving tail `[5.50s..7.90s]` of `P1:07_table_three_props_playing_card_2mm_disc_photoelectric_plate`.",
        "",
        "## Mint order",
        "",
        "006 > 007 > 008 > 009 > 010 > 011 > 012 > 013 > 014 > 015 > 016 > 017 > 018 > 019 > 020 > 021 > 022 > 023 > 024 > 025. `generation_authorized` is `false` on every row.",
    ])
    (EDIT / "PRICE_REVIEW_v01.md").write_text("\n".join(pr_lines) + "\n")
    print(f"025 v01 boards written: {totals['rows']} rows, Flow expected={totals['flow_credits_expected']}")


if __name__ == "__main__":
    main()
