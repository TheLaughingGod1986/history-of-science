#!/usr/bin/env python3
"""HOS 049 (Colour Vision: Why John Dalton Had His Own Eyes Cut Open) pre-VO plate boards v01. J0570. No mint, no spend.

Built from 00_Brand/Channel-Setup/ideas/049_Dalton-Young-Helmholtz-Wald-Colour-Vision/colour_vision_script_master_v01.md (92.4 PASS)
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
        "Part 01 — The Pink Flower That Looked Sky-Blue and the 150-Year-Old Pickled Eyeball",
        [
            ("01_john_dalton_31_oct_1794_manchester_pink_geranium_and_rgb_screen_subpixels", 0.0, 5.5, "A", False, "SKY-BLUE OR PINK?", "Quality",
             "Quality: Short frame 0 / answer image (0:03) + split composition: on the left, in Manchester on 31 October 1794, 28-year-old Quaker chemist John Dalton holds a pink crane's-bill geranium flower between a sunlit window (where it looks sky-blue to him) and a flickering candle (where it turns red); on the right, a macro zoom into a modern screen shows only tiny Red, Green, and Blue sub-pixels tricking the human eye into seeing yellow light.",
             STYLE + "Split period and optical scene: on the left in 1794 Manchester, twenty-eight-year-old Quaker chemist John Dalton in a plain dark coat holds a potted pink geranium flower between a sunlit window and a brass candlestick; on the right, a close-up grid of red, green, and blue sub-pixel bars blends into the illusion of a bright yellow lemon." + QUAL_TAIL,
             {"kind": "WHEN", "label": "MANCHESTER, 31 OCTOBER 1794", "timeline_step": "1/5 · 31 Oct 1794 (John Dalton in Manchester reads the first scientific study of colour blindness)", "hold_s": 3.5}),
            ("02_dalton_1794_geranium_1844_eye_jar_young_helmholtz_cones_wald_retinal_1995_dna_split", 5.5, 6.0, "B", False, "GERANIUM, CONES, RETINAL, DNA", "Quality",
             "Quality: complex four-part composition (Dalton's 1794 geranium and 28 July 1844 preserved eyeball jar in Manchester; Young 1802 and Helmholtz's 1852 overlapping Red, Green, and Blue cone sensitivity curves; George Wald's 11-cis-retinal Vitamin A switch snapping straight; and Hunt and Mollon's 1995 X-chromosome DNA gel from Dalton's retina).",
             STYLE + "Four-panel period composition: on the left, a pink geranium beside a glass specimen jar holding preserved eye tissue; second, three overlapping blue, green, and red optical prisms; third, a bent Vitamin A retinal molecular model snapping straight; on the right, a 1995 genetics pipette over a DNA gel dish." + QUAL_TAIL,
             None),
            ("03_joseph_ransome_28_jul_1844_manchester_peering_through_daltons_clear_dissected_eye", 11.5, 6.0, "C", False, "28 JULY 1844", "Quality",
             "Quality: readable face (on 28 July 1844 in Manchester, physician Joseph Ransome peers through the rear window of John Dalton's dissected eye at scarlet and green ribbons and sees both colours pass through unaltered because the vitreous humour is completely colourless).",
             STYLE + "In a quiet 1844 Manchester study, physician Joseph Ransome in a dark waistcoat holds a watch glass of crystal-clear fluid and peers through a dissected eye specimen toward scarlet and green silk ribbons by a sunny window." + QUAL_TAIL,
             {"kind": "WHEN", "label": "MANCHESTER, 28 JULY 1844", "timeline_step": "3/5 · 28 Jul 1844 (Joseph Ransome dissects Dalton's eyes and proves the vitreous humour is clear)", "hold_s": 3.5}),
            ("04_young_helmholtz_420_534_564nm_three_cones_1m_hues_and_1_in_12_men_x_linked_chart", 17.5, 8.0, "E", False, "3 CONES (420, 534, 564 NM = 1,000,000 HUES) · DALTON MISSING 534 NM GREEN CONE · 1 IN 12 MEN (8%) VS 1 IN 200 WOMEN (0.5%)", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked cone-wavelength sensitivity and X-linked prevalence chart from Young (1802), Helmholtz (1852), and Hunt & Mollon (17 February 1995 Science 267: 984–988) shows S-cones (420 nm), M-cones (534 nm, absent in John Dalton's deuteranopia), and L-cones (564 nm) combining to distinguish ~1,000,000 hues, and contrasts male (~8% = 1 in 12) vs female (~0.5% = 1 in 200) red-green colour blindness.",
             {"kind": "DATA", "label": "3 CONES (420, 534, 564 NM = 1M SHADES) · DALTON MISSING M-CONE · 1 IN 12 MEN (8%) VS 1 IN 200 WOMEN (0.5%)", "detail": "Inked cone-wavelength sensitivity & X-linked prevalence chart on period paper from Young (1802), Helmholtz (1852), and Hunt & Mollon (17 February 1995 Science 267: 984–988) showing S-cones (420 nm), M-cones (534 nm, absent in Dalton), and L-cones (564 nm) combining to distinguish ~1,000,000 hues, and contrasting male (~8% = 1 in 12) vs female (~0.5% = 1 in 200) red-green colour blindness", "scale": "because each of your three cone types can distinguish about one hundred steps of brightness, three cones multiplying one hundred by one hundred by one hundred let your brain see roughly one million different shades", "who_card": "John Dalton (1766–1844) — English chemist and physicist · Joseph Ransome (1809–1893) — Manchester surgeon and physician · Thomas Young (1773–1829) — English physician and physicist · Hermann von Helmholtz (1821–1894) — German physician and physicist · George Wald (1906–1997) — American biochemist · David M. Hunt (born 1943) — British molecular geneticist · John D. Mollon (born 1945) — British visual neuroscientist", "when_stamp": "31 October 1794 · 28 July 1844 · 1802 · 1852 · 1933–1958 · 17 February 1995", "hold_s": 3.8}),
            ("05_pink_geranium_flower_scarlet_stockings_glass_prism_and_retinal_model_pan", 25.5, 5.5, "A", False, "31 OCTOBER 1794", "Fast",
             "Fast: daylight macro pan across a potted pink crane's-bill geranium flower, folded scarlet silk stockings, a cut-glass optical prism, and a bent ball-and-stick retinal model on an oak table between code graphics so two full-frame graphics never run back to back. Nothing emissive, no face.",
             STYLE + "In crisp daylight on an oak laboratory bench, the camera pans smoothly across a potted pink crane's-bill geranium flower, folded scarlet silk stockings, a triangular glass prism, and a ball-and-stick Vitamin A molecular model." + FAST_TAIL,
             None),
            ("06_wald_11_cis_retinal_200_femtosecond_photoisomerization_vs_blink_speed_chart", 31.0, 8.0, "E", False, "1 IN 12 MEN", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period parchment, an inked photoisomerization speed chart compares a human eye blink (300 milliseconds = 3 × 10⁻¹ s) and a camera flash (1 millisecond) against the 200-femtosecond (2 × 10⁻¹³ s) cis-to-trans snap of George Wald's 11-cis-retinal Vitamin A switch inside the eye.",
             {"kind": "DATA", "label": "GEORGE WALD RETINAL SWITCH: 200 FEMTOSECONDS (2 × 10⁻¹³ S) CIS-TO-TRANS SNAP VS 300 MS BLINK", "detail": "Inked photoisomerization speed chart comparing a human blink (300 milliseconds = 3 × 10⁻¹ s) and a camera flash (1 millisecond) against the 200-femtosecond (2 × 10⁻¹³ s) cis-to-trans snap of retinal inside the eye", "scale": "the Vitamin A switch inside your retina snaps straight in two hundred femtoseconds — more than a trillion times faster than the blink of an eye", "hold_s": 3.8}),
            ("07_table_three_props_pink_geranium_helmholtz_brass_spectroscope_and_1844_eye_jar", 39.0, 5.5, "C", False, "1794 TO 1995", "Fast",
             "Fast: daylight prop table (callback source for Part 05: Dalton's potted pink crane's-bill geranium beside his 1794 manuscript, Helmholtz's brass colour-mixing spectroscope, and the 1844 glass specimen jar with a 1995 DNA tube). Nothing emissive.",
             STYLE + "On an oak workbench in soft window light sit three objects side by side: a potted pink geranium flower beside a handwritten 1794 manuscript, a brass three-slit optical spectroscope, and a sealed glass specimen jar beside a small DNA test tube." + FAST_TAIL,
             None),
            ("08_explorer_overlapping_red_and_green_spotlights_to_reveal_yellow_lemon", 62.0, 5.5, "A", True, None, "Quality",
             "Quality: Explorer beat 1 (locked character reference, after 1:00).",
             STYLE + "Standing before a dark theatre wall, the Explorer switches on two focused spotlights — one pure red and one pure green — and where the two beams overlap in the centre, a bright golden-yellow lemon appears in the circle of light." + EXP_TAIL,
             None),
            ("09_john_dalton_31_oct_1794_manchester_comparing_scarlet_academic_gown_and_green_leaf", 67.5, 5.5, "B", False, "MANCHESTER, 31 OCTOBER 1794", "Quality",
             "Quality: readable face (in Manchester on 31 October 1794, John Dalton stands before the Literary and Philosophical Society holding his scarlet academic gown next to a green laurel leaf).",
             STYLE + "In a 1794 Manchester lecture room, twenty-eight-year-old Quaker chemist John Dalton stands before wooden benches holding up a bright scarlet academic robe sleeve right beside a green laurel branch." + QUAL_TAIL,
             None),
        ],
    ),
    (
        2,
        "Part 02 — 31 October 1794 & 28 July 1844: John Dalton's Pink Geranium, the Scarlet Gown & His Dissected Eyeballs",
        [
            ("01_dalton_31_oct_1794_manchester_geranium_and_ransome_28_jul_1844_clear_eye_autopsy", 73.0, 6.5, "A", False, "DISSECTED HIS OWN EYES", "Quality",
             "Quality: readable faces (28-year-old Quaker chemist John Dalton on 31 October 1794 in Manchester comparing a pink geranium flower in daylight and candlelight, dissolving to physician Joseph Ransome on 28 July 1844 draining clear vitreous humour from Dalton's eye into a watch glass).",
             STYLE + "Split period scene: on the left in 1794 Manchester, John Dalton examines a pink geranium flower by a window and a candle; on the right on 28 July 1844, physician Joseph Ransome pours crystal-clear vitreous fluid from Dalton's dissected eye into a glass dish." + QUAL_TAIL,
             {"kind": "FACT", "label": "Dissected his own eyes", "when_stamp": "1792 · 31 October 1794 · 27 July 1844 · 28 July 1844", "timeline_step": "1/5 · 31 Oct 1794 (John Dalton reads the first scientific study of colour blindness) & 3/5 · 28 Jul 1844 (Joseph Ransome dissects Dalton's eyes and proves the vitreous humour is clear)", "hold_s": 3.8}),
            ("02_dalton_1794_daylight_vs_candlelight_geranium_spectrum_and_1844_clear_vitreous_chart", 79.5, 8.0, "E", False, "31 OCT 1794 & 28 JUL 1844 DALTON AUTOPSY: PINK GERANIUM (450 NM BLUE + 650 NM RED) & 100% CLEAR VITREOUS HUMOUR", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked daylight vs candlelight spectral transmission diagram from John Dalton (31 October 1794 / 1798 Manchester Memoirs 5: 28–45) shows why a pink geranium (reflecting both short-wavelength blue ~450 nm and long-wavelength red ~650 nm) looked sky-blue to Dalton in blue-rich daylight but reddish in red-rich candlelight, alongside Joseph Ransome's 28 July 1844 autopsy finding of 100% clear vitreous humour.",
             {"kind": "DATA", "label": "1794 GERANIUM SPECTRUM & 28 JUL 1844 AUTOPSY: 100% CLEAR EYE JELLY DISPROVES DALTON'S BLUE-FILTER HYPOTHESIS", "detail": "Inked daylight vs candlelight spectral transmission diagram on period paper from John Dalton (31 October 1794 / 1798 Manchester Memoirs 5: 28–45) showing why a pink geranium (reflecting both short-wavelength blue ~450 nm and long-wavelength red ~650 nm) looked sky-blue to Dalton in blue-rich daylight but reddish in red-rich candlelight, alongside Joseph Ransome's 28 July 1844 autopsy finding of 100% clear vitreous humour", "scale": "John Dalton waited fifty years — from his seventeen ninety-four lecture to the day after his death in eighteen forty-four — so his doctor could look through the back of his own eyeball and prove his blue-jelly theory wrong", "hold_s": 3.8}),
            ("03_dalton_1844_preserved_eye_specimen_jar_watch_glass_and_1798_manchester_memoirs", 87.5, 6.5, "B", False, "28 JULY 1844 — CLEAR EYE JELLY", "Fast",
             "Fast: daylight macro shot of John Dalton's 1844 glass specimen jar, a clear glass watch dish beside scarlet and green silk ribbons, and Dalton's 1798 printed Manchester Memoirs paper on an oak table. Nothing emissive, no face.",
             STYLE + "In crisp daylight on a wooden specimen table, a sealed glass museum jar sits beside a clear watch glass, scarlet and green silk ribbons, and an open 1798 scientific journal." + FAST_TAIL,
             None),
            ("04_scarlet_silk_stockings_red_sealing_wax_green_leaf_and_pink_geranium_pan", 94.0, 5.5, "C", False, "31 OCTOBER 1794 — DALTONISM", "Fast",
             "Fast: daylight close-up pan across a pair of scarlet silk stockings, a stick of red sealing wax beside green grass blades, and a pink crane's-bill geranium on a Manchester study desk. Nothing emissive, no face.",
             STYLE + "In bright window light on an oak desk, a pair of scarlet silk stockings lies beside red sealing wax, a green leaf, and a potted pink geranium flower." + FAST_TAIL,
             None),
        ],
    ),
    (
        3,
        "Part 03 — 1802, 1852 & 17 February 1995: Young and Helmholtz's Three Cones & Sequencing Dalton's 150-Year-Old Eye — Midpoint Twist",
        [
            ("01_young_1802_helmholtz_1852_three_cones_and_hunt_mollon_17_feb_1995_dalton_dna", 99.5, 6.5, "A", False, "DNA FROM 150-YEAR-OLD EYE", "Quality",
             "Quality: readable faces (Thomas Young in 1802 London and Hermann von Helmholtz in 1852 Königsberg with colour-matching optical instruments, alongside Ewald Hering in 1878, Jeremy Nathans in 1986, and David Hunt and John Mollon on 17 February 1995 extracting DNA from John Dalton's 150-year-old preserved retina).",
             STYLE + "Split period scene: on the left in an 1852 German physics lab, Hermann von Helmholtz and Thomas Young adjust a brass three-slit colour-mixing apparatus; on the right in a 1995 British genetics laboratory, David Hunt and John Mollon sample a tiny tissue crumb from John Dalton's 1844 Manchester eye jar." + QUAL_TAIL,
             {"kind": "WHO", "label": "Ewald Hering (1834–1918) — German physiologist · Jeremy Nathans (born 1958) — American molecular geneticist", "fact_card": "DNA from 150-year-old eye", "when_stamp": "1666 · 1802 · 1852 · 1878 · 1986 · 17 February 1995", "timeline_step": "2/5 · 1802 & 1852 (Thomas Young and Hermann von Helmholtz establish three-cone trichromacy) & 5/5 · 17 Feb 1995 (David Hunt and John Mollon extract DNA from Dalton's 150-year-old eye and prove he lacked the middle-wavelength green-cone gene)", "hold_s": 3.8}),
            ("02_helmholtz_rgb_metamer_yellow_illusion_and_1995_dalton_m_cone_deletion_chart", 106.0, 8.0, "E", False, "1852 HELMHOLTZ RGB METAMERS (RED 630 NM + GREEN 530 NM = 580 NM YELLOW) & 1995 DALTON DNA (MISSING 534 NM M-CONE GENE)", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked RGB screen metamers and Dalton X-chromosome DNA chart from Helmholtz (1852), Nathans (1986 Science 232: 193–202), and Hunt & Mollon (17 February 1995 Science 267: 984–988) shows how 580 nm monochromatic yellow light and a 630 nm Red + 530 nm Green LED pair produce identical L/M cone excitation ratios (~150,000 cones/mm² in the fovea), and how Dalton's X chromosome carried the L-cone (red) gene but lacked the M-cone (green) gene.",
             {"kind": "DATA", "label": "RGB METAMERS & 17 FEB 1995 DALTON DNA: 150,000 CONES/MM² IN FOVEA · MISSING 534 NM M-CONE GENE (DEUTERANOPIA)", "detail": "Inked RGB screen metamers & Dalton X-chromosome DNA chart on period paper from Helmholtz (1852), Nathans (1986 Science 232: 193–202), and Hunt & Mollon (17 February 1995 Science 267: 984–988) showing how 580 nm monochromatic yellow light and a 630 nm Red + 530 nm Green LED pair produce identical L/M cone excitation ratios, and how Dalton's X chromosome carried the L-cone (red) gene but lacked the M-cone (green) gene", "scale": "a single square millimetre at the centre of your retina packs roughly one hundred and fifty thousand cone cells — yet every colour you have ever seen is mixed from just three cone types", "hold_s": 3.8}),
            ("03_dalton_1844_eye_jar_micropipette_dna_tubes_and_1995_science_paper", 114.0, 6.5, "B", False, "17 FEBRUARY 1995 — DALTON'S DNA", "Fast",
             "Fast: daylight macro shot of John Dalton's 1844 preserved eye jar beside a laboratory micropipette, PCR microcentrifuge tubes, and the 17 February 1995 Science journal on a genetics bench. Nothing emissive, no face.",
             STYLE + "In crisp daylight on a genetics laboratory bench, an antique 1844 glass specimen jar sits beside a precision micropipette, rack of tiny DNA tubes, and an open 1995 scientific journal." + FAST_TAIL,
             None),
            ("04_newton_1666_glass_prism_and_helmholtz_1852_brass_colour_mixer_pan", 120.5, 5.5, "C", False, "1802 & 1852 — TRICHROMACY", "Fast",
             "Fast: daylight close-up pan across an antique 1666 glass prism, Thomas Young's 1802 Philosophical Transactions offprint, and Hermann von Helmholtz's 1852 brass colour-mixing spectroscope on an oak desk. Nothing emissive, no face.",
             STYLE + "In bright window light on an oak desk, a triangular glass prism rests beside an open 1802 Royal Society volume and a polished brass Helmholtz spectroscope." + FAST_TAIL,
             None),
        ],
    ),
    (
        4,
        "Part 04 — 1933–1958: Franz Boll's Bleaching Frog Retina, George Wald's Vitamin A Switch & the 200-Femtosecond Snap",
        [
            ("01_boll_1876_kuhne_1878_visual_purple_and_wald_hubbard_1952_retinal_vitamin_a_switch", 126.0, 6.5, "A", False, "SNAPS IN 200 FEMTOSECONDS", "Quality",
             "Quality: readable faces (Franz Boll in 1876 and Willy Kühne in 1878 observing reddish-purple frog rhodopsin bleaching yellow in sunlight, dissolving to American biochemist George Wald and Ruth Hubbard at Harvard in 1933–1958 holding a molecular model of bent 11-cis-retinal straightening into all-trans-retinal).",
             STYLE + "Split period scene: on the left in an 1876 German physiology lab, Franz Boll and Willy Kühne hold a glass dish by a window as a purple retinal sample bleaches pale yellow; on the right in a 1952 Harvard laboratory, George Wald and Ruth Hubbard examine a large molecular model of bent 11-cis-retinal snapping straight." + QUAL_TAIL,
             {"kind": "WHO", "label": "Franz Boll (1849–1879) — German physiologist · Willy Kühne (1837–1900) — German physiologist · Ruth Hubbard (1924–2016) — Austrian-American biochemist", "fact_card": "Snaps in 200 femtoseconds", "when_stamp": "1876 · 1878 · 1933 · 1952–1958 · 1967", "timeline_step": "4/5 · 1933–1958 (George Wald and Ruth Hubbard prove light snaps Vitamin A's 11-cis-retinal straight into all-trans-retinal)", "hold_s": 3.8}),
            ("02_wald_hubbard_1952_11_cis_retinal_200fs_isomerization_and_100k_sodium_channel_chart", 132.5, 8.0, "E", False, "1952–1958 WALD & HUBBARD: 1 PHOTON → 11-CIS TO ALL-TRANS RETINAL IN 200 FS → CLOSES ~100,000 SODIUM CHANNELS", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked rhodopsin photoisomerization and amplification diagram from George Wald & Ruth Hubbard (1952 J. Gen. Physiol. 36: 269–315 & 1967 Nobel Lecture) shows 1 photon straightening kinked 11-cis-retinal into all-trans-retinal in 200 femtoseconds inside the opsin pocket (tuned to 420, 534, or 564 nm by subtle amino-acid shifts) and closing ~10⁵ sodium channels per photon.",
             {"kind": "DATA", "label": "1 PHOTON → 200 FS 11-CIS-RETINAL SNAP → CLOSES >100,000 SODIUM CHANNELS IN THE CONE/ROD CELL", "detail": "Inked rhodopsin photoisomerization & amplification diagram on period paper from George Wald & Ruth Hubbard (1952 J. Gen. Physiol. 36: 269–315 & 1967 Nobel Lecture) showing 1 photon straightening kinked 11-cis-retinal into all-trans-retinal in 200 fs inside the opsin pocket (tuned to 420, 534, or 564 nm by subtle amino-acid shifts) and closing ~10⁵ sodium channels per photon", "scale": "one single photon of starlight — the smallest possible packet of energy in the universe — snaps one Vitamin A molecule straight and blocks over a hundred thousand sodium ions to fire a signal to your brain", "hold_s": 3.8}),
            ("03_harvard_1958_amber_vitamin_a_vials_and_bent_11_cis_vs_straight_all_trans_models", 140.5, 6.5, "B", False, "1952–1958 — THE RETINAL SWITCH", "Fast",
             "Fast: daylight macro shot of amber glass vials of Vitamin A retinaldehyde beside two ball-and-stick molecular models — kinked 11-cis-retinal and straight all-trans-retinal — on a Harvard biochemistry bench. Nothing emissive, no face.",
             STYLE + "In crisp daylight on a laboratory bench, amber glass vials of Vitamin A sit beside two contrasting ball-and-stick molecular models: one bent at a sharp angle and the other snapped straight." + FAST_TAIL,
             None),
            ("04_explorer_catching_photon_to_snap_bent_retinal_lever_and_shut_sodium_gates", 147.0, 5.5, "B", True, None, "Quality",
             "Quality: Explorer beat 2 (locked character reference).",
             STYLE + "Standing inside a cutaway cone cell beside a cocked spring-trap shaped like a bent Vitamin A retinal molecule, the Explorer catches a single incoming photon sphere, snapping the molecular lever straight and slamming shut a row of mechanical sodium gates." + EXP_TAIL,
             None),
        ],
    ),
    (
        5,
        "Part 05 — Why Bulls Can't See a Red Cape & How a Man Who Forgot Every 30 Seconds Revealed How Memories Form",
        [
            ("01_timeline_1794_1995_and_mammal_2_cone_human_3_cone_bird_4_cone_spectrum_chart", 152.5, 8.5, "E", False, "1794–1995 TIMELINE · 201 YEARS FROM DALTON'S GERANIUM TO HIS RETINAL DNA · 2-CONE BULL VS 3-CONE HUMAN", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, the 5-date timeline completes: 31 Oct 1794 (John Dalton in Manchester reads the first scientific study of colour blindness) · 1802 & 1852 (Thomas Young and Hermann von Helmholtz establish three-cone trichromacy) · 28 Jul 1844 (Joseph Ransome dissects Dalton's eyes and proves the vitreous humour is clear) · 1933–1958 (George Wald and Ruth Hubbard prove light snaps Vitamin A's 11-cis-retinal straight into all-trans-retinal) · 17 Feb 1995 (David Hunt and John Mollon extract DNA from Dalton's 150-year-old eye and prove he lacked the middle-wavelength green-cone gene) alongside the mammal 2-cone vs human 3-cone vs bird 4-cone spectrum comparison.",
             {"kind": "DATA", "label": "1794–1995 TIMELINE · 201 YEARS FROM DALTON'S GERANIUM TO HIS RETINAL DNA · 2-CONE DICHROMAT VS 3-CONE TRICHROMAT", "detail": "Animated 5-date timeline (31 Oct 1794 → 17 Feb 1995) alongside the mammal 2-cone vs human 3-cone vs bird 4-cone UV spectrum comparison", "scale": "two hundred and one years after John Dalton held a pink geranium up to a candle in seventeen ninety-four, DNA from his own preserved retina finally solved the mystery of how he saw the world", "when_stamp": "1794–1995 · 2009", "timeline_step": "5/5 · 1794–1995 timeline complete", "hold_s": 3.8}),
            ("02_red_matador_cape_and_three_optical_colour_filters_on_museum_plinth_pan", 161.0, 5.5, "A", False, "TWO CONES VS THREE CONES", "Fast",
             "Fast: daylight close-up of a folded red matador cape beside two-cone dichromat and three-cone trichromat optical filter lenses and ripe red fruit among green leaves on a wooden museum plinth. Nothing emissive, no face.",
             STYLE + "In crisp daylight on a wooden museum plinth, a folded red cloth cape sits beside two brass optical filter lenses and a bowl of ripe red apples nestled in green leaves." + FAST_TAIL,
             None),
            ("03_ebbinghaus_1885_nonsense_syllables_and_brenda_milner_1957_patient_hm_mirror_star_handoff", 166.5, 6.5, "C", False, "THE MIRROR-STAR MEMORY TEST", "Quality",
             "Quality: readable faces (German psychologist Hermann Ebbinghaus in Berlin in 1885 memorising 2,300 nonsense syllables by metronome, alongside Brenda Milner in 1953–1957 watching Patient H.M. Henry Molaison trace a five-pointed star in a mirror — handoff to 050 Memory & Patient H.M.).",
             STYLE + "Split period scene: on the left in an 1885 Berlin study, Hermann Ebbinghaus flips three-letter syllable cards beside a ticking brass metronome; on the right in 1957 Connecticut, neuropsychologist Brenda Milner watches Henry Molaison trace a five-pointed star reflected in a tabletop mirror." + QUAL_TAIL,
             {"kind": "WHEN", "label": "1885 · 1953–1957", "hold_s": 3.5}),
            ("04_table_three_callback", 173.0, 2.4, "C", False, None, "reuse",
             "Reuse: verified unused moving window [5.50s..7.90s] of P1:07_table_three_props_pink_geranium_helmholtz_brass_spectroscope_and_1844_eye_jar (callback, £0).",
             "Reuse P1:07_table_three_props_pink_geranium_helmholtz_brass_spectroscope_and_1844_eye_jar [5.50s..7.90s] (2.40s distinct non-overlapping tail window from 8.00s source clip).",
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
                row["reuse_of"] = "P1:07_table_three_props_pink_geranium_helmholtz_brass_spectroscope_and_1844_eye_jar"
                row["reuse_window_s"] = [5.5, 7.9]
                row["reuse_audit"] = {
                    "source_row": "P1:07_table_three_props_pink_geranium_helmholtz_brass_spectroscope_and_1844_eye_jar",
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
            "film": "049_Dalton-Young-Helmholtz-Wald-Colour-Vision",
            "part": p_idx,
            "title": p_title,
            "version": "v01",
            "timing_status": "pre_vo_script_clock (built from colour_vision_script_master_v01.md; retimes onto Scribe STT once VO locks)",
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
        "film": "049_Dalton-Young-Helmholtz-Wald-Colour-Vision",
        "version": "v01",
        "date": "2026-10-18",
        "owner": "gemini (J0570)",
        "status": "PRE_VO_BOARDS_V01_NO_MINT",
        "generation_authorized": False,
        "script": "00_Brand/Channel-Setup/ideas/049_Dalton-Young-Helmholtz-Wald-Colour-Vision/colour_vision_script_master_v01.md",
        "sources": "00_Brand/Channel-Setup/ideas/049_Dalton-Young-Helmholtz-Wald-Colour-Vision/SOURCES_v01.md",
        "credit_snapshot": {
            "flow_balance": 23740,
            "flow_floor": 0,
            "flow_read_at": "2026-10-15T21:42:22Z",
            "vertex_promo_gbp": 71.02,
            "vertex_usable_gbp": 70.02,
        },
        "totals": totals,
        "per_part": per_part_summary,
        "mint_order": "006 > 007 > 008 > 009 > 010 > 011 > 012 > 013 > 014 > 015 > 016 > 017 > 018 > 019 > 020 > 021 > 022 > 023 > 024 > 025 > 026 > 027 > 028 > 029 > 030 > 031 > 032 > 033 > 034 > 035 > 036 > 037 > 038 > 039 > 040 > 041 > 042 > 043 > 044 > 045 > 046 > 047 > 048 > 049 > 050. Nothing in 049 is generation_authorized.",
    }
    (EDIT / "PICTURE_PLAN_v01.json").write_text(json.dumps(plan, indent=2) + "\n")

    sl = [
        "# 049 Colour Vision: Why John Dalton Had His Own Eyes Cut Open — Shot list & plate boards v01 (pre-VO)",
        "",
        "Gemini, 18 Oct 2026, J0570. Built from `colour_vision_script_master_v01.md` (`92.4 PASS`) and `SOURCES_v01.md`.",
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
        "# 049 price review v01 (pre-VO plate boards)",
        "",
        "Gemini, 18 Oct 2026, J0570. Boards only. **No mint. No spend. No merge.**",
        "Prepared from `colour_vision_script_master_v01.md` (`92.4 PASS`) and `SOURCES_v01.md` so 049's full plate board rows, non-emissive Fast prompts, £0 code graphics, and Teach-on-Screen overlays are ready to re-time the moment long VO locks. Parked for Chief.",
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
        f"- **Quality ({totals['Quality']} rows):** readable faces (John Dalton, Joseph Ransome, Thomas Young, Hermann von Helmholtz, David Hunt, John Mollon, Franz Boll, Willy Kühne, George Wald, Ruth Hubbard, Hermann Ebbinghaus, Brenda Milner, Henry Molaison), 1794 Manchester pink geranium lecture, 1844 Manchester eye dissection, 1852 colour-mixing lab, 1995 Dalton retinal DNA extraction, 1952 Harvard retinal switch, and the 2 Explorer beats.",
        f"- **Fast ({totals['Fast']} rows, non-emissive):** daylight prop and laboratory shots (pink crane's-bill geranium, scarlet silk stockings, glass prism & retinal model pan, 3-object callback bench, Dalton's 1844 specimen jar & 1798 Manchester Memoirs paper, scarlet stockings & sealing wax, 1995 micropipette & PCR tubes, 1666 Newton prism & Helmholtz brass spectroscope, Harvard Vitamin A vials & bent/straight retinal models, folded red matador cape & dichromat/trichromat lenses). Zero candles, flames, sparks, or glowing elements on Fast.",
        f"- **£0 code graphics ({totals['code_graphic']} rows):**",
        "  1. `P1:04_young_helmholtz_420_534_564nm_three_cones_1m_hues_and_1_in_12_men_x_linked_chart` — S-cones (420 nm), M-cones (534 nm, absent in Dalton), and L-cones (564 nm) distinguishing ~1,000,000 hues + X-linked red-green colour blindness (1 in 12 men = 8% vs 1 in 200 women = 0.5%) (`SCALE: because each of your three cone types can distinguish about one hundred steps of brightness, three cones multiplying one hundred by one hundred by one hundred let your brain see roughly one million different shades`)",
        "  2. `P1:06_wald_11_cis_retinal_200_femtosecond_photoisomerization_vs_blink_speed_chart` — George Wald's 200-femtosecond (2 × 10⁻¹³ s) 11-cis to all-trans retinal photoisomerization snap vs a 300 ms human blink (`SCALE: the Vitamin A switch inside your retina snaps straight in two hundred femtoseconds — more than a trillion times faster than the blink of an eye`)",
        "  3. `P2:02_dalton_1794_daylight_vs_candlelight_geranium_spectrum_and_1844_clear_vitreous_chart` — Dalton's 1794 pink geranium daylight vs candlelight spectrum & Joseph Ransome's 28 July 1844 autopsy finding of 100% colourless vitreous humour (`SCALE: John Dalton waited fifty years — from his seventeen ninety-four lecture to the day after his death in eighteen forty-four — so his doctor could look through the back of his own eyeball and prove his blue-jelly theory wrong`)",
        "  4. `P3:02_helmholtz_rgb_metamer_yellow_illusion_and_1995_dalton_m_cone_deletion_chart` — Helmholtz's 1852 RGB metamers (Red 630 nm + Green 530 nm = 580 nm yellow across ~150,000 cones/mm² in the fovea) & Hunt and Mollon's 17 February 1995 Science DNA proof of Dalton's missing M-cone gene (`SCALE: a single square millimetre at the centre of your retina packs roughly one hundred and fifty thousand cone cells — yet every colour you have ever seen is mixed from just three cone types`)",
        "  5. `P4:02_wald_hubbard_1952_11_cis_retinal_200fs_isomerization_and_100k_sodium_channel_chart` — Wald & Hubbard's (1952–1958) 1-photon 11-cis-retinal isomerization closing >100,000 sodium ion channels (`SCALE: one single photon of starlight — the smallest possible packet of energy in the universe — snaps one Vitamin A molecule straight and blocks over a hundred thousand sodium ions to fire a signal to your brain`)",
        "  6. `P5:01_timeline_1794_1995_and_mammal_2_cone_human_3_cone_bird_4_cone_spectrum_chart` — completed 5-date timeline (31 Oct 1794 → 17 Feb 1995) + 2-cone mammal vs 3-cone human vs 4-cone bird spectrum (`SCALE: two hundred and one years after John Dalton held a pink geranium up to a candle in seventeen ninety-four, DNA from his own preserved retina finally solved the mystery of how he saw the world`)",
        f"- **£0 verified reuse ({totals['reuse']} row):** `P5:04_table_three_callback` uses the 2.40 s unused moving tail `[5.50s..7.90s]` of `P1:07_table_three_props_pink_geranium_helmholtz_brass_spectroscope_and_1844_eye_jar`.",
        "",
        "## Mint order",
        "",
        "006 > 007 > 008 > 009 > 010 > 011 > 012 > 013 > 014 > 015 > 016 > 017 > 018 > 019 > 020 > 021 > 022 > 023 > 024 > 025 > 026 > 027 > 028 > 029 > 030 > 031 > 032 > 033 > 034 > 035 > 036 > 037 > 038 > 039 > 040 > 041 > 042 > 043 > 044 > 045 > 046 > 047 > 048 > 049 > 050. `generation_authorized` is `false` on every row.",
    ])
    (EDIT / "PRICE_REVIEW_v01.md").write_text("\n".join(pr_lines) + "\n")
    print(f"049 v01 boards written: {totals['rows']} rows, Flow expected={totals['flow_credits_expected']}")


if __name__ == "__main__":
    main()
