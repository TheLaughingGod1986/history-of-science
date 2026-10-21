#!/usr/bin/env python3
"""HOS 083 (Your Eyes: Why You See the World Upside Down) pre-VO plate boards v01. J0753. No mint, no spend.

Built from 00_Brand/Channel-Setup/ideas/083_Al-Haytham-Kepler-Young-Donders-Snellen-Eyes-Glasses-Optics/eyes_optics_script_master_v01.md
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
        "Part 01 — The Darkened Room in Cairo, the Peeled Ox Eye & Why 4 Billion People Wear Glasses",
        [
            ("01_ibn_al_haytham_1011_cairo_camera_obscura_inverted_lamps_and_human_eye_retina_spectacle_lens", 0.0, 5.5, "A", False, "WHY YOUR EYES SEE UPSIDE DOWN", "Quality",
             "Quality: Short frame 0 / answer image (0:03) + side by side, inside Ibn al-Haytham's darkened Cairo room (camera obscura) in 1011 AD five oil lamps outside a tiny shutter pinhole project five inverted flames onto the back wall, beside a cross-section of a human eye where the cornea and crystalline lens bend light rays to project an upside-down image onto the retina while a concave spectacle lens shifts a myopic focal point back onto the retina.",
             STYLE + "Split historical-and-anatomical scene: on the left in 1011 AD Cairo, five oil lamps outside a shuttered window pinhole cast five inverted flame images onto the wall of Ibn al-Haytham's darkened chamber; on the right, a cutaway human eye and concave spectacle lens focus light rays into a sharp upside-down image on the retina." + QUAL_TAIL,
             {"kind": "WHEN", "label": "CAIRO, 1011 AD", "timeline_step": "1/3 · 1011–1021 AD (Ibn al-Haytham in Cairo uses the pinhole camera obscura in his Book of Optics to refute Greek extramission eye-beams and prove light enters the eye)", "hold_s": 3.5}),
            ("02_ibn_al_haytham_1011_cairo_kepler_1604_scheiner_1619_ox_eye_and_young_1801_snellen_1862_split", 5.5, 6.0, "B", False, "CAIRO PINHOLE, INVERTED RETINA, 20/20 EYE CHART", "Quality",
             "Quality: complex three-part composition (Hasan Ibn al-Haytham in Cairo in 1011–1021 AD testing straight-line light rays in his pinhole camera obscura; Johannes Kepler in Prague in 1604 and Christoph Scheiner in 1619 holding up a peeled ox eye showing an inverted retinal image; and Thomas Young at the Royal Society in 1800–1801 with Franciscus Donders and Herman Snellen in Utrecht in 1862 unveiling the 20/20 Big E Eye Chart).",
             STYLE + "Three-panel period composition: on the left, Ibn al-Haytham in 1011 Cairo tracing pinhole light rays in his darkened room; in the centre, Johannes Kepler in 1604 Prague and Christoph Scheiner in 1619 holding a peeled ox eye with an upside-down flame on its retina; on the right, Thomas Young in 1801 London beside Franciscus Donders and Herman Snellen in 1862 Utrecht with the wall eye chart." + QUAL_TAIL,
             None),
            ("03_normal_24mm_eye_vs_myopic_25mm_eye_with_concave_lens_and_hyperopic_23mm_eye_with_convex_lens", 11.5, 6.0, "C", False, "1 MILLIMETRE OF BLUR", "Quality",
             "Quality: complex optical reveal (a split comparison of a normal 24-mm human eyeball focusing light sharply onto the retina vs a 25-mm myopic eyeball focusing 1 mm in front of the retina corrected by a concave minus lens and a 23-mm hyperopic eyeball corrected by a convex plus lens).",
             STYLE + "In a three-part optical cross-section, a normal twenty-four-millimetre eyeball focuses light cleanly on the retina, an elongated myopic eyeball is brought into focus by a concave spectacle lens, and a shortened hyperopic eyeball is brought into focus by a convex spectacle lens." + QUAL_TAIL,
             {"kind": "WHEN", "label": "1011 AD · 1021 AD · 1604 · 1619 · 1801 · 1862", "timeline_step": "1/3 · 1011–1021 AD (Ibn al-Haytham) · 2/3 · 1604 & 1619 (Johannes Kepler & Christoph Scheiner) · 3/3 · 1801 & 1862–1864 (Thomas Young, Franciscus Donders & Herman Snellen)", "hold_s": 3.5}),
            ("04_al_haytham_1011_kepler_1604_scheiner_1619_young_1801_and_snellen_1862_eye_optics_chart", 17.5, 8.0, "E", False, "KEPLER (1604) & DONDERS/SNELLEN (1862): CORNEA (~43 D) + LENS (~15–20 D) = ~58–60 D AT 24 MM AXIAL LENGTH (±1 MM = ∓3 DIOPTRES)", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked Optics of the Human Eye, Retinal Inversion, Accommodation & Refractive Correction chart from Ibn al-Haytham (1011–1021 AD Kitāb al-Manāẓir / Book of Optics), Johannes Kepler (1604 Ad Vitellionem Paralipomena), Christoph Scheiner (1619 Oculus), Thomas Young (1801 Phil. Trans. R. Soc. 91: 23–88), and Franciscus Donders & Herman Snellen (1862 Probebuchstaben zur Bestimmung der Sehschärfe) shows 1) Camera obscura intromission rays crossing at the pupil/lens to form an inverted retinal image; 2) Ciliary muscle accommodation flattening the lens for distance vs fattening it for near vision; and 3) Concave (myopia), convex (hyperopia/presbyopia), and cylindrical (astigmatism) spectacle lenses + Snellen's 5-arcminute 20/20 optotype geometry.",
             {"kind": "DATA", "label": "KEPLER (1604) & DONDERS/SNELLEN (1862) HUMAN EYE RAY-TRACING (~58–60 DIOPTRES AT 24 MM AXIAL LENGTH; ±1 MM = ∓3 D) CHART", "detail": "Inked Kepler (1604) & Donders/Snellen (1862) human eye ray-tracing diagram (cornea ~43 dioptres + crystalline lens ~15–20 dioptres = ~58–60 dioptres total refractive power focusing at 24 mm axial length; ±1 mm axial error = ∓3 dioptres of myopia/hyperopia) on period paper", "scale": "every single millimetre your eyeball grows too long throws your focus off by three dioptres — meaning a difference smaller than the thickness of a British pound coin turns a sharp street sign across the road into a blurry smudge", "who_card": "Ibn al-Haytham (c. 965–c. 1040) — Arab mathematician and physicist · Johannes Kepler (1571–1630) — German astronomer and mathematician · Christoph Scheiner (1573–1650) — German Jesuit physicist and astronomer · Thomas Young (1773–1829) — British physician and physicist · Franciscus Cornelis Donders (1818–1889) — Dutch ophthalmologist and physiologist · Herman Snellen (1834–1908) — Dutch ophthalmologist", "when_stamp": "1011 AD · 1021 AD · 1604 · 1619 · 1801 · 1862", "hold_s": 3.8}),
            ("05_kitab_al_manazir_manuscript_brass_trial_lens_case_and_spectacle_frames_pan", 25.5, 5.5, "A", False, "UPSIDE DOWN ON THE RETINA", "Fast",
             "Fast: daylight macro pan across Ibn al-Haytham's Arabic optical diagram manuscript, a velvet-lined wooden optician's trial-lens case of concave and convex glass lenses, and brass spectacles on an oak bench between code graphics so two full-frame graphics never run back to back. Nothing emissive, no face.",
             STYLE + "In crisp daylight on an oak optician's workbench, the camera pans smoothly across an open medieval optical geometry manuscript, a velvet-lined case of glass trial lenses, and brass spectacle frames." + FAST_TAIL,
             None),
            ("06_herman_snellen_1862_utrecht_5x5_grid_optotype_and_5_arcminute_20_20_visual_acuity_chart", 31.0, 8.0, "E", False, "UTRECHT, 1862", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period parchment, an inked Herman Snellen (1862 Probebuchstaben zur Bestimmung der Sehschärfe, Utrecht) 5×5 Grid Optotype & 5-Arcminute Visual Acuity Angle diagram shows the big 'E' at 20 feet (6 metres) subtending 5 minutes of arc (1/12th of 1 degree), with each stroke and gap subtending 1 minute of arc to match the spacing of cone photoreceptors in the human fovea.",
             {"kind": "DATA", "label": "1862 HERMAN SNELLEN (UTRECHT): 5×5 GRID OPTOTYPE & 5-ARCMINUTE (1 ARCMINUTE STROKE AT 20 FT / 6 M) 20/20 VISUAL ACUITY CHART", "detail": "Inked Herman Snellen (1862) 20/200 to 20/20 visual acuity chart geometry (5 arcminutes letter height, 1 arcminute stroke width at 20 feet / 6 metres) on period paper", "scale": "reading the 20/20 line on Snellen's eye chart from twenty feet away requires your eye to distinguish gaps of just one-sixtieth of a degree — like spotting the space between two fingers held up from the far end of a tennis court", "hold_s": 3.8}),
            ("07_table_three_props_1011_pinhole_brass_screen_1604_glass_eye_model_and_1862_trial_spectacle_set", 39.0, 5.5, "C", False, "1011 TO 1864", "Fast",
             "Fast: daylight prop table (callback source for Part 05: Ibn al-Haytham's 1011 brass pinhole aperture screen, Kepler and Scheiner's 1604–1619 glass-and-brass anatomical eyeball model, and Donders and Snellen's 1862 brass trial-frame spectacles). Nothing emissive.",
             STYLE + "On an oak workbench in soft window light sit three objects side by side: a carved brass pinhole aperture screen, a glass-and-brass anatomical eyeball model on a stand, and a pair of adjustable brass trial-frame spectacles." + FAST_TAIL,
             None),
            ("08_explorer_sliding_concave_spectacle_lens_in_front_of_giant_cutaway_eyeball_focusing_inverted_tree_on_retina", 62.0, 5.5, "A", True, None, "Quality",
             "Quality: Explorer beat 1 (locked character reference, after 1:00).",
             STYLE + "Standing beside a giant translucent cutaway eyeball model where an upside-down green tree projects slightly in front of the rear retina screen, the Explorer slides a curved glass spectacle lens in front of the cornea so the upside-down tree snaps into crisp focus on the retina." + EXP_TAIL,
             None),
            ("09_thomas_young_27_nov_1800_royal_society_london_optometer_and_calliper_accommodation_test", 67.5, 5.5, "B", False, "LONDON, 27 NOVEMBER 1800", "Quality",
             "Quality: readable face (in London on 27 November 1800, published 1801, 27-year-old British physician and physicist Thomas Young demonstrates his optometer and blunt calliper rings at the Royal Society to prove lens accommodation).",
             STYLE + "In a 1800 Royal Society lecture room in London, young British polymath Thomas Young holds a brass optometer bar and small blunt calliper ring beside a large anatomical drawing of the human crystalline lens." + QUAL_TAIL,
             {"kind": "WHEN", "label": "LONDON, 27 NOVEMBER 1800", "timeline_step": "3/3 · 27 Nov 1800 / 1801 & 1862 (Thomas Young proves crystalline-lens accommodation and discovers astigmatism, and Donders & Snellen standardize the 20/20 eye chart)", "hold_s": 3.5}),
        ],
    ),
    (
        2,
        "Part 02 — 1011–1021 AD: The Myth of Eye-Beams (Extramission) & Ibn al-Haytham's Darkened Room in Cairo (Camera Obscura)",
        [
            ("01_ibn_al_haytham_1011_1021_cairo_five_oil_lamps_camera_obscura_and_kitab_al_manazir", 73.0, 6.5, "A", False, "PINHOLE PROVED LIGHT ENTERS", "Quality",
             "Quality: readable face (Arab mathematician and physicist Hasan Ibn al-Haytham in Cairo between 1011 and 1021 AD inside his darkened camera obscura room watching five oil lamps outside a shutter pinhole project five inverted spots of light on the wall while an assistant blocks one lamp).",
             STYLE + "In a 1011 AD Cairo chamber, Arab physicist Ibn al-Haytham stands beside a wooden window shutter with a single pinhole as light rays from five outside oil lamps cross through the hole to form five inverted spots on the white wall." + QUAL_TAIL,
             {"kind": "FACT", "label": "Pinhole proved light enters", "when_stamp": "1011 AD · 1021 AD", "timeline_step": "1/3 · 1011–1021 AD (Ibn al-Haytham in Cairo uses the 5-lamp pinhole camera obscura in his Book of Optics to prove intromission)", "hold_s": 3.8}),
            ("02_ibn_al_haytham_1011_1021_kitab_al_manazir_five_lamp_camera_obscura_ray_crossing_chart", 79.5, 8.0, "E", False, "1011–1021 AD IBN AL-HAYTHAM (KITĀB AL-MANĀẒIR / BOOK OF OPTICS): 5-LAMP CAMERA OBSCURA STRAIGHT-LINE INTROMISSION RAY CROSSING", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked Ibn al-Haytham (1011–1021 AD Kitāb al-Manāẓir / Book of Optics) 5-lamp camera obscura straight-line ray crossing diagram refuting Euclidean extramission eye-beams.",
             {"kind": "DATA", "label": "1011–1021 AD IBN AL-HAYTHAM (BOOK OF OPTICS): 5-LAMP CAMERA OBSCURA STRAIGHT-LINE RAY CROSSING & INTROMISSION PROOF", "detail": "Inked Ibn al-Haytham (1011–1021 AD Kitāb al-Manāẓir / Book of Optics) 5-lamp camera obscura straight-line ray crossing diagram refuting Euclidean extramission eye-beams on period paper", "scale": "if vision worked by shooting rays out of your pupils the way Euclid and Ptolemy claimed, opening your eyes at midnight would light up a pitch-black bedroom like a pair of car headlights — and staring at the sun would never hurt your eyes", "hold_s": 3.8}),
            ("03_cairo_1021_kitab_al_manazir_arabic_eye_anatomy_manuscript_and_brass_sighting_tube_closeup", 87.5, 6.5, "B", False, "1011–1021 AD — IBN AL-HAYTHAM'S BOOK OF OPTICS", "Fast",
             "Fast: daylight macro shot of Ibn al-Haytham's Kitāb al-Manāẓir Arabic manuscript showing the twin-eye anatomy diagram beside brass sighting tubes, a wooden pinhole screen, and reed pens on a table. Nothing emissive, no face.",
             STYLE + "In crisp daylight on a carved wooden table in Cairo, an open Arabic optics manuscript with inked diagrams of the two eyes sits beside brass sighting tubes, a wooden pinhole screen, and a reed pen." + FAST_TAIL,
             None),
            ("04_wooden_camera_obscura_model_with_pinhole_aperture_and_translucent_ground_glass_screen_pan", 94.0, 5.5, "C", False, "AL-BAYT AL-MUZLIM — THE CAMERA OBSCURA", "Fast",
             "Fast: daylight close-up pan across a cutaway wooden camera obscura teaching box showing a brass pinhole aperture plate at the front and a frosted glass projection screen at the back on an oak bench. Nothing emissive, no face.",
             STYLE + "In bright window light on an oak bench, a cutaway wooden camera obscura box shows a front brass pinhole plate and a rear ground-glass viewing screen." + FAST_TAIL,
             None),
        ],
    ),
    (
        3,
        "Part 03 — 1604 & 1619: Johannes Kepler's Upside-Down Retina & Christoph Scheiner's Peeled Ox Eye — Midpoint Twist",
        [
            ("01_johannes_kepler_1604_prague_retinal_ray_tracing_and_christoph_scheiner_1619_peeled_ox_eye_flame", 99.5, 6.5, "A", False, "RETINA SEES WORLD UPSIDE DOWN", "Quality",
             "Quality: readable faces (German astronomer Johannes Kepler in Prague in 1604 tracing light refraction through the cornea and crystalline lens to an inverted retinal focus, dissolving to Swiss anatomist Felix Platter and German Jesuit physicist Christoph Scheiner in 1619 holding a peeled ox eye in a dark room to show a tiny upside-down candle flame on the translucent retina).",
             STYLE + "Split period scene: on the left in 1604 Prague, Johannes Kepler uses brass dividers to trace inverted light rays through a diagram of the eye lens onto the retina; on the right in 1619 Ingolstadt, Christoph Scheiner holds a prepared ox eye showing a tiny inverted candle flame on its translucent rear retina." + QUAL_TAIL,
             {"kind": "FACT", "label": "Retina sees world upside down", "who_card": "Felix Platter (1536–1614) — Swiss physician and anatomist", "when_stamp": "1286 · 1583 · 1604 · 1619", "timeline_step": "2/3 · 1604 & 1619 (Johannes Kepler proves the cornea and lens project an inverted image onto the retina and explains concave and convex spectacles, and Christoph Scheiner demonstrates the upside-down flame on a peeled ox eye)", "hold_s": 3.8}),
            ("02_johannes_kepler_1604_and_christoph_scheiner_1619_inverted_retinal_image_and_spectacle_ray_chart", 106.0, 8.0, "E", False, "1604 JOHANNES KEPLER (AD VITELLIONEM PARALIPOMENA) & 1619 CHRISTOPH SCHEINER (OCULUS): INVERTED RETINAL IMAGE & CONCAVE/CONVEX LENSES", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked Johannes Kepler (1604 Ad Vitellionem Paralipomena) & Christoph Scheiner (1619 Oculus) inverted retinal image & concave vs convex spectacle lens ray-tracing chart.",
             {"kind": "DATA", "label": "1604 KEPLER & 1619 SCHEINER (OCULUS): INVERTED RETINAL FOCUS & CONCAVE (MYOPIA) VS CONVEX (HYPEROPIA) SPECTACLE RAY CHART", "detail": "Inked Johannes Kepler (1604 Ad Vitellionem Paralipomena) & Christoph Scheiner (1619 Oculus) inverted retinal image & concave vs convex spectacle lens ray-tracing chart on period paper", "scale": "a pinhole camera needs no lens, so why does your eye have one? Because a pinhole tiny enough to make a sharp image lets in almost no light — your eye's lens lets your pupil open a hundred times wider in the dark while bending every spread-out ray back to a single pinpoint on your retina", "hold_s": 3.8}),
            ("03_prague_1604_ad_vitellionem_paralipomena_book_1619_oculus_and_medieval_rivet_spectacles_closeup", 114.0, 6.5, "B", False, "1604 & 1619 — KEPLER & SCHEINER'S INVERTED RETINA", "Fast",
             "Fast: daylight macro shot of Johannes Kepler's 1604 Ad Vitellionem Paralipomena and Christoph Scheiner's 1619 Oculus open to their eye-refraction plates beside wooden rivet spectacles and biconvex glass lenses on a bench. Nothing emissive, no face.",
             STYLE + "In crisp daylight on a 1619 study table, two open Latin optics volumes showing eye ray-tracing engravings sit beside wooden rivet spectacles and polished glass lenses." + FAST_TAIL,
             None),
            ("04_glass_globe_eye_lens_demonstrator_comparing_dim_pinhole_vs_bright_convex_lens_focus_pan", 120.5, 5.5, "C", False, "WHY THE EYE HAS A CONVERGING LENS", "Fast",
             "Fast: daylight close-up pan across a brass-and-glass optical bench model comparing a tiny pinhole aperture against a wide biconvex crystal lens focusing parallel rods of light onto a curved white retinal cup on an oak table. Nothing emissive, no face.",
             STYLE + "In bright window light on an oak table, a brass optical bench model shows a wide glass lens bending multiple rods into a single focal point on a curved white retinal cup." + FAST_TAIL,
             None),
        ],
    ),
    (
        4,
        "Part 04 — 1801 & 1862: Thomas Young's Calliper Test (Accommodation & Astigmatism) & Herman Snellen's 20/20 Eye Chart",
        [
            ("01_thomas_young_1801_accommodation_and_franciscus_donders_herman_snellen_1862_utrecht_eye_chart", 126.0, 6.5, "A", False, "IRON RING PROVED LENS FLEXES", "Quality",
             "Quality: readable faces (Benjamin Franklin in 1784 with bifocals and British polymath Thomas Young in 1800–1801 testing crystalline lens accommodation and astigmatism, dissolving to Dutch ophthalmologists Franciscus Cornelis Donders and Herman Snellen at the Utrecht Eye Hospital in 1862 testing a patient with trial lenses in front of the 20/20 Big E eye chart).",
             STYLE + "Split period scene: on the left in 1801 London, Thomas Young inspects his brass optometer and crystalline-lens accommodation diagrams beside Benjamin Franklin's split bifocal spectacles; on the right in 1862 Utrecht, Franciscus Donders and Herman Snellen fit trial lenses onto a patient looking at a wall eye chart." + QUAL_TAIL,
             {"kind": "FACT", "label": "Iron ring proved lens flexes", "who_card": "Benjamin Franklin (1706–1790) — American statesman and natural philosopher", "when_stamp": "May 1784 · 27 November 1800 · 1801 · 1825 · 1862 · 1864", "timeline_step": "3/3 · 1801 & 1862–1864 (Thomas Young proves lens accommodation and discovers astigmatism, and Franciscus Donders & Herman Snellen standardize refractive errors and the 20/20 eye chart)", "hold_s": 3.8}),
            ("02_thomas_young_1801_accommodation_astigmatism_and_donders_snellen_1862_1864_refractive_acuity_chart", 132.5, 8.0, "E", False, "1801 THOMAS YOUNG (PHIL. TRANS.: CILIARY LENS ACCOMMODATION & ASTIGMATISM) & 1862–1864 DONDERS & SNELLEN (DIOPTRE REFRACTION & 20/20 CHART)", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked Thomas Young (1801 Phil. Trans. R. Soc. 91: 23–88) ciliary-lens accommodation & astigmatism chart alongside Franciscus Donders & Herman Snellen's (1862–1864) emmetropia, myopia (− dioptre), hyperopia (+ dioptre) & 20/20 optotype acuity scale.",
             {"kind": "DATA", "label": "1801 THOMAS YOUNG (LENS ACCOMMODATION & ASTIGMATISM) & 1862–1864 DONDERS-SNELLEN (DIOPTRE REFRACTION & 20/20 ACUITY) CHART", "detail": "Inked Thomas Young (1801 Phil. Trans. R. Soc. 91: 23–88) ciliary-lens accommodation & astigmatism chart alongside Franciscus Donders & Herman Snellen's (1862–1864) emmetropia, myopia (− dioptre), hyperopia (+ dioptre) & 20/20 optotype acuity scale on period paper", "scale": "when you look up from your phone to a sign across the street, the living lens inside your eye flattens its curve by less than half a millimetre in a third of a second — faster and smoother than the autofocus motor in a modern digital camera", "hold_s": 3.8}),
            ("03_utrecht_1862_velvet_trial_lens_set_brass_trial_frames_and_young_1801_optometer_closeup", 140.5, 6.5, "B", False, "1801 & 1862 — ACCOMMODATION & THE 20/20 EYE CHART", "Fast",
             "Fast: daylight macro shot of Franciscus Donders and Herman Snellen's 1862 Utrecht mahogany trial-lens case, adjustable brass trial frames, and Thomas Young's 1801 brass optometer bar on a bench. Nothing emissive, no face.",
             STYLE + "In crisp daylight on an 1862 Utrecht ophthalmology bench, a mahogany case of concave, convex, and cylindrical glass trial lenses sits beside brass trial frames and a brass optometer bar." + FAST_TAIL,
             None),
            ("04_explorer_pulling_and_relaxing_ciliary_muscle_strings_on_elastic_crystal_lens_to_focus_near_and_far", 147.0, 5.5, "B", True, None, "Quality",
             "Quality: Explorer beat 2 (locked character reference).",
             STYLE + "Standing beside a giant suspended elastic crystal eye lens held in a brass ciliary-muscle ring, the Explorer relaxes the radial suspensory cords so the lens springs rounder for close focus, then pulls them taut to flatten the lens for distant focus." + EXP_TAIL,
             None),
        ],
    ),
    (
        5,
        "Part 05 — The Living Camera in Your Head — & Why Your Brain Gives You a Fever at 37 °C",
        [
            ("01_timeline_1011_1864_and_eye_optics_retinal_inversion_accommodation_snellen_chart", 152.5, 8.5, "E", False, "1011–1864 TIMELINE · IBN AL-HAYTHAM CAMERA OBSCURA, KEPLER & SCHEINER INVERTED RETINA, YOUNG ACCOMMODATION & DONDERS-SNELLEN 20/20", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, the 3-era timeline completes: 1011–1021 AD (Ibn al-Haytham in Cairo uses the pinhole camera obscura in his Book of Optics to refute Greek extramission eye-beams and prove light enters the eye) · 1604 & 1619 (Johannes Kepler proves the cornea and lens project an inverted image onto the retina and explains concave and convex spectacles, and Christoph Scheiner demonstrates the upside-down flame on a peeled ox eye) · 1801 & 1862–1864 (Thomas Young at the Royal Society proves lens accommodation and discovers astigmatism, and Franciscus Donders and Herman Snellen in Utrecht standardize refractive errors and the 20/20 eye chart).",
             {"kind": "DATA", "label": "1011–1864 OPTICS OF THE EYE & GLASSES TIMELINE · IBN AL-HAYTHAM, KEPLER, SCHEINER, THOMAS YOUNG, DONDERS & SNELLEN", "detail": "Animated timeline (1011 → 1864) alongside an inked summary of camera obscura intromission, inverted retinal refraction, ciliary lens accommodation, and 20/20 spectacle correction", "scale": "from five oil lamps outside a darkened room in medieval Cairo to a peeled ox eye and the big letter E on an optician's wall, scientists unlocked how two spheres of jelly let us see the universe", "when_stamp": "1011–1864", "timeline_step": "3/3 · 1011–1864 timeline complete", "hold_s": 3.8}),
            ("02_anatomical_eye_and_brass_spectacles_beside_clinical_glass_thermometer_on_plinth_pan", 161.0, 5.5, "A", False, "FOUR BILLION PEOPLE IN CLEAR FOCUS", "Fast",
             "Fast: daylight close-up of a cutaway anatomical eye model and brass spectacles beside an early clinical glass thermometer in a velvet case on a wooden museum plinth. Nothing emissive, no face.",
             STYLE + "In crisp daylight on a wooden museum plinth, a sculpted cutaway human eye model and brass spectacles sit beside a glass mercury thermometer in a velvet-lined wooden case." + FAST_TAIL,
             None),
            ("03_santorio_1612_thermometer_blagden_1775_heated_room_wunderlich_1868_37c_and_kluger_1975_fever_handoff", 166.5, 6.5, "C", False, "37 °C THERMOREGULATION & FEVER", "Quality",
             "Quality: readable faces (Santorio Santorio in 1612 with his mouth thermoscope, Charles Blagden on 23 January 1775 standing inside a 126 °C heated room beside a cooking beefsteak, Carl Wunderlich in 1868 recording 1,000,000 thermometer readings at 37 °C, and Matthew Kluger in 1975 — handoff to 084 Body Temperature, 37 °C & Fever).",
             STYLE + "Split period scene: on the left in 1775 London, Royal Society physician Charles Blagden stands calmly inside a heated chamber wiping sweat from his brow beside a thermometer and a cooked steak on a plate; on the right in 1868 Leipzig, Carl Wunderlich records patient thermometer charts." + QUAL_TAIL,
             {"kind": "WHEN", "label": "1612 · 23 JANUARY 1775 · 1868 · 1975", "hold_s": 3.5}),
            ("04_table_three_callback", 173.0, 2.4, "C", False, None, "reuse",
             "Reuse: verified unused moving window [5.50s..7.90s] of P1:07_table_three_props_1011_pinhole_brass_screen_1604_glass_eye_model_and_1862_trial_spectacle_set (callback, £0).",
             "Reuse P1:07_table_three_props_1011_pinhole_brass_screen_1604_glass_eye_model_and_1862_trial_spectacle_set [5.50s..7.90s] (2.40s distinct non-overlapping tail window from 8.00s source clip).",
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
                row["reuse_of"] = "P1:07_table_three_props_1011_pinhole_brass_screen_1604_glass_eye_model_and_1862_trial_spectacle_set"
                row["reuse_window_s"] = [5.5, 7.9]
                row["reuse_audit"] = {
                    "source_row": "P1:07_table_three_props_1011_pinhole_brass_screen_1604_glass_eye_model_and_1862_trial_spectacle_set",
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
            "film": "083_Al-Haytham-Kepler-Young-Donders-Snellen-Eyes-Glasses-Optics",
            "part": p_idx,
            "title": p_title,
            "version": "v01",
            "timing_status": "pre_vo_script_clock (built from eyes_optics_script_master_v01.md; retimes onto Scribe STT once VO locks)",
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
        "film": "083_Al-Haytham-Kepler-Young-Donders-Snellen-Eyes-Glasses-Optics",
        "version": "v01",
        "date": "2026-10-21",
        "owner": "gemini (J0753)",
        "status": "PRE_VO_BOARDS_V01_NO_MINT",
        "generation_authorized": False,
        "script": "00_Brand/Channel-Setup/ideas/083_Al-Haytham-Kepler-Young-Donders-Snellen-Eyes-Glasses-Optics/eyes_optics_script_master_v01.md",
        "sources": "00_Brand/Channel-Setup/ideas/083_Al-Haytham-Kepler-Young-Donders-Snellen-Eyes-Glasses-Optics/SOURCES_v01.md",
        "credit_snapshot": {
            "flow_balance": 23740,
            "flow_floor": 0,
            "flow_read_at": "2026-10-15T21:42:22Z",
            "vertex_promo_gbp": 71.02,
            "vertex_usable_gbp": 70.02,
        },
        "totals": totals,
        "per_part": per_part_summary,
        "mint_order": "006 > 007 > 008 > 009 > 010 > 011 > 012 > 013 > 014 > 015 > 016 > 017 > 018 > 019 > 020 > 021 > 022 > 023 > 024 > 025 > 026 > 027 > 028 > 029 > 030 > 031 > 032 > 033 > 034 > 035 > 036 > 037 > 038 > 039 > 040 > 041 > 042 > 043 > 044 > 045 > 046 > 047 > 048 > 049 > 050 > 051 > 052 > 053 > 054 > 055 > 056 > 057 > 058 > 059 > 060 > 061 > 062 > 063 > 064 > 065 > 066 > 067 > 068 > 069 > 070 > 071 > 072 > 073 > 074 > 075 > 076 > 077 > 078 > 079 > 080 > 081 > 082 > 083 > 084 > 085 > 086. Nothing in 083 is generation_authorized.",
    }
    (EDIT / "PICTURE_PLAN_v01.json").write_text(json.dumps(plan, indent=2) + "\n")

    sl = [
        "# 083 Your Eyes: Why You See the World Upside Down — Shot list & plate boards v01 (pre-VO)",
        "",
        "Gemini, 21 Oct 2026, J0753. Built from `eyes_optics_script_master_v01.md` (`91.1/100 PASS`) and `SOURCES_v01.md`.",
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
        "# 083 price review v01 (pre-VO plate boards)",
        "",
        "Gemini, 21 Oct 2026, J0753. Boards only. **No mint. No spend. No merge.**",
        "Prepared from `eyes_optics_script_master_v01.md` (`91.1/100 PASS`) and `SOURCES_v01.md` so 083's full plate board rows, non-emissive Fast prompts, £0 code graphics, and Teach-on-Screen overlays are ready to re-time the moment long VO locks. Parked for Chief.",
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
        f"- **Quality ({totals['Quality']} rows):** readable faces (Hasan Ibn al-Haytham, Johannes Kepler, Felix Platter, Christoph Scheiner, Benjamin Franklin, Thomas Young, Franciscus Cornelis Donders, Herman Snellen, Charles Blagden, Carl Wunderlich), 1011–1021 AD Cairo 5-lamp `camera obscura` intromission proof, 1604 Prague inverted retinal ray-tracing & 1619 peeled ox-eye flame demonstration, 27 November 1800 / 1801 London living-lens `accommodation` & 1862 Utrecht `20/20` eye chart, and the 2 Explorer beats.",
        f"- **Fast ({totals['Fast']} rows, non-emissive):** daylight prop and laboratory shots (*Kitāb al-Manāẓir* Arabic optics manuscript, velvet trial-lens case & brass spectacles pan, 3-object callback bench, 1021 Cairo twin-eye anatomy manuscript with brass sighting tubes & pinhole screen, cutaway wooden `camera obscura` teaching box, 1604 *Ad Vitellionem Paralipomena* & 1619 *Oculus* refraction plates with wooden rivet spectacles, brass-and-glass optical bench lens demonstrator, 1862 Utrecht mahogany trial-lens set with brass trial frames & Young's 1801 optometer bar, cutaway eye model and brass spectacles beside clinical glass thermometer on museum plinth). Zero candles, flames, sparks, or glowing elements on Fast.",
        f"- **£0 code graphics ({totals['code_graphic']} rows):**",
        "  1. `P1:04_al_haytham_1011_kepler_1604_scheiner_1619_young_1801_and_snellen_1862_eye_optics_chart` — Kepler (1604) & Donders/Snellen (1862) human eye ray-tracing (`~58–60 dioptres` at `24 mm` axial length; `±1 mm = ∓3 dioptres`) (`SCALE: every single millimetre your eyeball grows too long throws your focus off by three dioptres — meaning a difference smaller than the thickness of a British pound coin turns a sharp street sign across the road into a blurry smudge`)",
        "  2. `P1:06_herman_snellen_1862_utrecht_5x5_grid_optotype_and_5_arcminute_20_20_visual_acuity_chart` — Herman Snellen (1862, Utrecht) `5×5` grid optotype & `5-arcminute` (`1 arcminute` stroke at `20 ft / 6 m`) `20/20` visual acuity chart (`SCALE: reading the 20/20 line on Snellen's eye chart from twenty feet away requires your eye to distinguish gaps of just one-sixtieth of a degree — like spotting the space between two fingers held up from the far end of a tennis court`)",
        "  3. `P2:02_ibn_al_haytham_1011_1021_kitab_al_manazir_five_lamp_camera_obscura_ray_crossing_chart` — Ibn al-Haytham (1011–1021 AD *Kitāb al-Manāẓir / Book of Optics*) 5-lamp `camera obscura` straight-line ray crossing chart (`SCALE: if vision worked by shooting rays out of your pupils the way Euclid and Ptolemy claimed, opening your eyes at midnight would light up a pitch-black bedroom like a pair of car headlights — and staring at the sun would never hurt your eyes`)",
        "  4. `P3:02_johannes_kepler_1604_and_christoph_scheiner_1619_inverted_retinal_image_and_spectacle_ray_chart` — Johannes Kepler (1604 *Ad Vitellionem Paralipomena*) & Christoph Scheiner (1619 *Oculus*) inverted retinal image & concave vs convex spectacle lens ray-tracing chart (`SCALE: a pinhole camera needs no lens, so why does your eye have one? Because a pinhole tiny enough to make a sharp image lets in almost no light — your eye's lens lets your pupil open a hundred times wider in the dark while bending every spread-out ray back to a single pinpoint on your retina`)",
        "  5. `P4:02_thomas_young_1801_accommodation_astigmatism_and_donders_snellen_1862_1864_refractive_acuity_chart` — Thomas Young (1801 *Phil. Trans.*) ciliary-lens `accommodation` & `astigmatism` + Franciscus Donders & Herman Snellen (1862–1864) dioptre refractive scale & `20/20` chart (`SCALE: when you look up from your phone to a sign across the street, the living lens inside your eye flattens its curve by less than half a millimetre in a third of a second — faster and smoother than the autofocus motor in a modern digital camera`)",
        "  6. `P5:01_timeline_1011_1864_and_eye_optics_retinal_inversion_accommodation_snellen_chart` — completed timeline (1011 → 1864) + camera obscura, inverted retina, accommodation & 20/20 spectacles (`SCALE: from five oil lamps outside a darkened room in medieval Cairo to a peeled ox eye and the big letter E on an optician's wall, scientists unlocked how two spheres of jelly let us see the universe`)",
        f"- **£0 verified reuse ({totals['reuse']} row):** `P5:04_table_three_callback` uses the 2.40 s unused moving tail `[5.50s..7.90s]` of `P1:07_table_three_props_1011_pinhole_brass_screen_1604_glass_eye_model_and_1862_trial_spectacle_set`.",
        "",
        "## Mint order",
        "",
        "006 > 007 > 008 > 009 > 010 > 011 > 012 > 013 > 014 > 015 > 016 > 017 > 018 > 019 > 020 > 021 > 022 > 023 > 024 > 025 > 026 > 027 > 028 > 029 > 030 > 031 > 032 > 033 > 034 > 035 > 036 > 037 > 038 > 039 > 040 > 041 > 042 > 043 > 044 > 045 > 046 > 047 > 048 > 049 > 050 > 051 > 052 > 053 > 054 > 055 > 056 > 057 > 058 > 059 > 060 > 061 > 062 > 063 > 064 > 065 > 066 > 067 > 068 > 069 > 070 > 071 > 072 > 073 > 074 > 075 > 076 > 077 > 078 > 079 > 080 > 081 > 082 > 083 > 084 > 085 > 086. `generation_authorized` is `false` on every row.",
    ])
    (EDIT / "PRICE_REVIEW_v01.md").write_text("\n".join(pr_lines) + "\n")
    print(f"083 v01 boards written: {totals['rows']} rows, Flow expected={totals['flow_credits_expected']}")


if __name__ == "__main__":
    main()
