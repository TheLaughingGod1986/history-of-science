#!/usr/bin/env python3
"""HOS 030 (Continental Drift: The Woman Who Mapped the Hidden Ocean Rift) pre-VO plate boards v01. J0479. No mint, no spend.

Built from 00_Brand/Channel-Setup/ideas/030_Wegener-Tharp-Plate-Tectonics/tectonics_script_master_v01.md
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
        "Part 01 — The Torn Map and the Seam at the Bottom of the Sea",
        [
            ("01_wegener_1912_pangaea_globe_and_tharp_1952_atlantic_rift", 0.0, 5.5, "A", False, "THE HIDDEN OCEAN RIFT", "Quality",
             "Quality: Short frame 0 / answer image (0:03) + Alfred Wegener in Frankfurt on 6 January 1912 sliding the brass-edged coastlines of South America and Africa together on a period globe while Marie Tharp in New York in Autumn 1952 inks a 16,000-kilometre V-shaped rift valley splitting the Mid-Atlantic Ridge.",
             STYLE + "In Frankfurt on 6 January 1912, meteorologist Alfred Wegener slides the brass-edged coastlines of South America and Africa together on a period globe, dissolving into cartographer Marie Tharp in New York in Autumn 1952 inking a deep V-shaped rift valley down a broad Atlantic Ocean chart." + QUAL_TAIL,
             {"kind": "WHEN", "label": "FRANKFURT, 6 JANUARY 1912 · NEW YORK, AUTUMN 1952", "timeline_step": "1/6 · 6 Jan 1912 & 1915 (Alfred Wegener presents continental drift & Pangaea in Frankfurt)", "hold_s": 3.5}),
            ("02_pangaea_greenland_skis_tharp_rift_vine_matthews_stripes_split", 5.5, 6.0, "B", False, "PANGAEA, SONAR RIFT, SEAFLOOR SPREADING", "Quality",
             "Quality: readable faces & complex split composition (Alfred Wegener's 1915 Pangaea map and his 1930 skis buried in Greenland snow on the left; Marie Tharp's 1952 hand-drawn Atlantic cross-section overlaid with red earthquake dots in the centre; Fred Vine and Drummond Matthews's 1963 zebra-striped magnetic seafloor conveyor belt on the right).",
             STYLE + "Three-panel period composition: on the left, a parchment supercontinent map beside wooden skis standing upright in Arctic snow; in the centre, Marie Tharp drafting an underwater mountain profile; on the right, symmetrical black-and-white magnetic stripes spreading across an ocean ridge." + QUAL_TAIL,
             None),
            ("03_frankfurt_1912_geologists_shaking_heads_sunken_land_bridges", 11.5, 6.0, "C", False, "JANUARY 1912: FROZEN CONTINENTS?", "Quality",
             "Quality: readable faces (stern geologists in frock coats inside a wood-panelled Frankfurt lecture hall on 6 January 1912 shaking their heads and tapping heavy textbooks showing static continents).",
             STYLE + "Inside a wood-panelled Frankfurt lecture hall on 6 January 1912, three stern bearded geologists in dark frock coats shake their heads skeptically and tap open geology atlases on a wooden lectern." + QUAL_TAIL,
             None),
            ("04_wegener_1912_shelf_fit_and_tharp_1952_mid_atlantic_rift_chart", 17.5, 8.0, "E", False, "4,500 KM SHELF FIT & 16,000 KM RIFT", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period parchment, an inked diagram shows Alfred Wegener's 6 January 1912 Pangaea fit across the 200-metre continental shelves (matching Mesosaurus freshwater fossils and Appalachian–Caledonian mountains across 5,000 km of ocean) alongside Marie Tharp's 1952 Mid-Atlantic Ridge cross-section (a 16,000 km mountain chain split by a 1.5–3 km deep, 15–48 km wide V-shaped rift valley spreading at ~2.5 cm/year).",
             {"kind": "DATA", "label": "WEGENER 1912 SHELF FIT (4,500 KM) & THARP 1952 RIFT (16,000 KM, 2.5 CM/YR)", "detail": "Inked parchment map & cross-section comparing Wegener's 1912 continental-shelf jigsaw fit (Mesosaurus fossils across 5,000 km) and Marie Tharp's 1952 Mid-Atlantic Ridge rift valley (16,000 km long, 1.5–3 km deep, spreading at 2.5 cm/year)", "scale": "2.5 centimetres a year — the exact speed your fingernails grow, yet over 200 million years enough to open the 5,000-kilometre Atlantic Ocean", "who_card": "Alfred Wegener (1880–1930) — German meteorologist and polar explorer · Marie Tharp (1920–2006) — American geologist and oceanographic cartographer", "when_stamp": "6 January 1912 · Autumn 1952", "hold_s": 3.8}),
            ("05_sonar_echogram_paper_rolls_and_brass_dividers_pan", 25.5, 5.5, "A", False, "SONAR SOUNDINGS", "Fast",
             "Fast: daylight pan across unrolled paper sonar echogram rolls and brass drafting dividers on an oak table between code graphics so two full-frame graphics never run back to back. Nothing emissive.",
             STYLE + "In soft daylight on an oak drafting table, the camera pans across long unrolled paper sonar depth trace rolls beside a pair of brass proportional dividers and a bottle of black India ink." + FAST_TAIL,
             None),
            ("06_2_5_cm_per_year_fingernail_vs_5000_km_atlantic_scale_card", 31.0, 8.0, "E", False, "2.5 CM PER YEAR", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked scale card compares a human fingernail growing 2.5 cm/year against two tectonic plates diverging 2.5 cm/year to open 5,000 kilometres of ocean in 200 million years.",
             {"kind": "DATA", "label": "2.5 CM/YEAR × 200 MILLION YEARS = 5,000 KM ATLANTIC OCEAN", "detail": "Inked rate-and-time scale bar on period paper showing 2.5 cm/year (fingernail growth rate) × 200,000,000 years = 5,000 km (Width of the Atlantic Ocean)", "scale": "moving no faster than your fingernail grows, two continents drift 5,000 kilometres apart in 200 million years", "hold_s": 3.8}),
            ("07_table_three_props_pangaea_globe_mesosaurus_fossil_sonar_roll", 39.0, 5.5, "C", False, "PALISADES, NEW YORK, 1952", "Fast",
             "Fast: daylight prop table (callback source for Part 05: brass-mounted Pangaea globe, dark shale slab with a Mesosaurus skeleton impression, and Marie Tharp's inked Atlantic rift profile scroll with ruling pen). Nothing emissive.",
             STYLE + "On a wooden drafting bench in soft window light sit three objects side by side: a brass-mounted continental globe, a dark shale rock slab bearing a small reptile fossil impression, and a rolled ocean-floor profile chart beside a brass ruling pen." + FAST_TAIL,
             None),
            ("08_explorer_clicking_south_america_africa_puzzle_pieces_globe", 62.0, 5.5, "A", True, None, "Quality",
             "Quality: Explorer beat 1 (locked character reference, after 1:00).",
             STYLE + "Standing on the brass rim of Wegener's globe, the Explorer pushes the wooden puzzle pieces of South America and Africa together with a satisfying click, then peers through its magnifying glass into the deep V-shaped seam down the middle of the Atlantic Ocean." + EXP_TAIL,
             None),
            ("09_wegener_skiing_into_greenland_whiteout_november_1930", 67.5, 5.5, "B", False, "GREENLAND ICE CAP, 1930", "Quality",
             "Quality: readable figure in blowing snow (Alfred Wegener in a heavy fur parka trudging on wooden skis into a howling whiteout on the Greenland ice cap in November 1930).",
             STYLE + "On the frozen Greenland ice cap in November 1930, explorer Alfred Wegener in a heavy fur-hooded parka leans forward on wooden skis against swirling snow and wind." + QUAL_TAIL,
             None),
        ],
    ),
    (
        2,
        "Part 02 — Torn Newspaper, Freshwater Reptiles, and the Greenland Ice",
        [
            ("01_wegener_1910_torn_newspaper_and_1915_pangaea_map", 73.0, 6.5, "A", False, "MARBURG & FRANKFURT · 1910–1915", "Quality",
             "Quality: readable face (Alfred Wegener in Marburg and Frankfurt in December 1910 – 1915 holding two halves of a torn newspaper edge to edge beside his 1915 map of Pangaea).",
             STYLE + "In a German study in 1912, meteorologist Alfred Wegener holds two halves of a torn newspaper together so the lines align beside a large parchment map of the supercontinent Pangaea." + QUAL_TAIL,
             {"kind": "FACT", "label": "Died rescuing Arctic team", "when_stamp": "December 1910 · 6 January 1912 · 1915", "hold_s": 3.8}),
            ("02_torn_newspaper_four_proofs_and_jeffreys_10e10_tidal_chart", 79.5, 8.0, "E", False, "TORN NEWSPAPER PROOFS VS 10¹⁰× TIDAL GAP", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked four-line 'torn newspaper' proof diagram shows (1) the 200-metre continental shelf fit between Brazil and West Africa, (2) Appalachian and Caledonian mountain alignment, (3) freshwater Mesosaurus and Glossopteris fossil bands across 5,000 km, and (4) Harold Jeffreys's 1924 calculation that tidal forces are 10¹⁰× too weak to plough granite through solid basalt.",
             {"kind": "DATA", "label": "4 PANGAEA PROOFS VS JEFFREYS 1924 (TIDAL FORCE 10¹⁰× TOO WEAK)", "detail": "Inked four-line 'torn newspaper' diagram on period paper showing (1) 200 m shelf fit, (2) Appalachian–Caledonian mountains, (3) Mesosaurus & Glossopteris fossils across 5,000 km, and (4) Harold Jeffreys's 1924 calculation that tidal force is 10¹⁰× too weak", "scale": "the tidal push Wegener relied on was ten billion times too weak — like trying to push a brick wall through solid concrete by blowing on it", "who_card": "Harold Jeffreys (1891–1989) — British mathematician and geophysicist", "when_stamp": "1924", "hold_s": 3.8}),
            ("03_chamberlin_1926_symposium_and_wegener_1930_greenland_skis", 87.5, 6.5, "B", False, "BURIED IN GREENLAND ICE", "Quality",
             "Quality: readable face (Rollin T. Chamberlin denouncing Wegener at the 15 November 1926 New York petroleum geology symposium, dissolving into Wegener's pair of wooden skis standing upright in −54 °C Greenland snow in November 1930).",
             STYLE + "New York, 15 November 1926, dissolving to Greenland, November 1930: geologist Rollin Chamberlin gestures dismissively at a podium, fading into a pair of wooden skis planted upright in deep blue-white Arctic snow." + QUAL_TAIL,
             {"kind": "WHO", "label": "Rollin T. Chamberlin (1881–1948) — American geologist", "when_stamp": "15 November 1926 · November 1930", "timeline_step": "2/6 · 1924, 15 Nov 1926 & Nov 1930 (Jeffreys & NY symposium reject drift; Wegener dies in Greenland)", "hold_s": 3.8}),
            ("04_mesosaurus_and_glossopteris_shale_fossils_bench", 94.0, 5.5, "C", False, "5,000 KM APART", "Fast",
             "Fast: daylight macro view of two matching black shale fossil slabs — one showing a freshwater Mesosaurus skeleton and one showing a tongue-shaped Glossopteris fern leaf — resting beside a brass caliper. Nothing emissive, no face.",
             STYLE + "In crisp window light on a museum table, the camera tracks across two dark shale rock slabs showing a delicate fossil reptile skeleton and a fossil fern leaf beside a brass caliper." + FAST_TAIL,
             None),
        ],
    ),
    (
        3,
        "Part 03 — 'Girl Talk' and the 16,000-Kilometre Scar Under the Sea",
        [
            ("01_tharp_and_heezen_lamont_1952_drafting_atlantic_profiles", 99.5, 6.5, "A", False, "LAMONT OBSERVATORY · AUTUMN 1952", "Quality",
             "Quality: readable faces (cartographer Marie Tharp in a 1950s blouse at a wide drafting table at Columbia University's Lamont Geological Observatory in Autumn 1952 plotting sonar depth rolls with a compass and ruling pen while marine geologist Bruce Heezen looks over her shoulder).",
             STYLE + "Palisades, New York, Autumn 1952: cartographer Marie Tharp plots six sweeping North Atlantic depth profiles with a ruling pen at a wide drafting table while geologist Bruce Heezen looks over her shoulder." + QUAL_TAIL,
             {"kind": "WHO", "label": "Bruce Heezen (1924–1977) — American marine geologist", "fact_card": "Barred from research ships", "when_stamp": "Autumn 1952", "timeline_step": "3/6 · Autumn 1952 & 1953 (Marie Tharp discovers Mid-Atlantic rift valley; earthquake dots match)", "hold_s": 3.8}),
            ("02_tharp_mid_atlantic_rift_and_foster_1953_earthquake_overlay_chart", 106.0, 8.0, "E", False, "1.5–3 KM DEEP RIFT · 65,000 KM SEAM", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked cross-section and transparent overlay shows sonar echo depth (d = ½ v t) revealing the Mid-Atlantic Ridge with Marie Tharp's 1.5–3 km deep, 15–48 km wide V-shaped rift valley at its crest, matched 1-to-1 by Howard Foster's 1953 earthquake epicentre dots along a 65,000 km global seam.",
             {"kind": "DATA", "label": "THARP 1952 V-SHAPED RIFT (1.5–3 KM DEEP) & 65,000 KM EARTHQUAKE SEAM", "detail": "Inked cross-section and overlay on period paper showing sonar echo depth (d = ½ v t) revealing the Mid-Atlantic Ridge with Marie Tharp's 1.5–3 km deep V-shaped rift valley matched 1-to-1 by Howard Foster's 1953 earthquake epicentre dots along a 65,000 km seam", "scale": "a continuous underwater mountain chain and rift valley stretching 65,000 kilometres around the planet — long enough to wrap around Earth's equator more than one and a half times", "who_card": "Howard Foster (fl. 1953) — American geological draftsman", "when_stamp": "1953 · 1957", "hold_s": 3.8}),
            ("03_foster_transparent_earthquake_sheet_laid_over_tharp_rift_1953", 114.0, 6.5, "B", False, "EARTHQUAKES MATCH THE RIFT", "Quality",
             "Quality: readable hands and faces (Marie Tharp and Bruce Heezen in 1953 laying Howard Foster's transparent sheet of red earthquake epicentre dots directly over Tharp's inked V-shaped Mid-Atlantic rift valley).",
             STYLE + "Lamont drafting room, 1953: Marie Tharp and Bruce Heezen lay a transparent sheet of red earthquake dots directly over a hand-inked chart of the Mid-Atlantic Ridge as the dots line up down the central canyon." + QUAL_TAIL,
             None),
            ("04_six_inked_north_atlantic_sonar_profiles_closeup", 120.5, 5.5, "C", False, "SIX SONAR PROFILES", "Fast",
             "Fast: daylight close-up of six stacked hand-inked North Atlantic ocean-floor cross-section strips showing the sharp V-shaped notch at the crest of each ridge profile. Nothing emissive, no face.",
             STYLE + "In crisp daylight, the camera glides over six parallel hand-inked ocean-floor cross-section profiles pinned to a drafting board, each showing a deep V-shaped canyon at the summit of the ridge." + FAST_TAIL,
             None),
        ],
    ),
    (
        4,
        "Part 04 — The Magnetic Barcode on the Ocean Conveyor Belt — Midpoint Twist",
        [
            ("01_hess_1962_conveyor_sketch_and_vine_matthews_1963_cambridge", 126.0, 6.5, "A", False, "PRINCETON 1962 & CAMBRIDGE 1963", "Quality",
             "Quality: readable faces (Princeton geologist Harry Hess in November 1962 sketching mantle convection cells rising under Marie Tharp's mid-ocean rift, alongside 24-year-old Fred Vine and Drummond Matthews in Cambridge on 7 September 1963 examining symmetrical magnetometer paper traces).",
             STYLE + "Split period scene: on the left, Princeton geologist Harry Hess in November 1962 sketches rising mantle arrows beneath a mid-ocean ridge; on the right, Cambridge researchers Fred Vine and Drummond Matthews in September 1963 compare symmetrical magnetic paper traces." + QUAL_TAIL,
             {"kind": "WHO", "label": "Harry Hess (1906–1969) — American geologist and Navy officer · Arthur Holmes (1890–1965) — British geologist · Fred Vine (1939–1988) — British marine geophysicist · Drummond Matthews (1931–1997) — British marine geologist", "fact_card": "Magnetic field flips north-south", "when_stamp": "1929 · November 1962 · 7 September 1963", "timeline_step": "4/6 · Nov 1962 (Harry Hess seafloor spreading) & 5/6 · 7 Sep 1963 (Vine & Matthews magnetic stripes)", "hold_s": 3.8}),
            ("02_seafloor_conveyor_580c_curie_point_magnetic_barcode_diagram", 132.5, 8.0, "E", False, "580 °C CURIE LOCK · ≤200 MA OCEAN FLOOR", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked seafloor conveyor-belt and magnetic-barcode diagram shows hot mantle upwelling at the mid-ocean rift, basalt cooling below the ~580 °C magnetite Curie point to lock in Earth's flipping magnetic field in symmetrical zebra stripes on both sides of the ridge, and old ocean crust subducting into deep trenches so no ocean floor exceeds ~200 million years in age.",
             {"kind": "DATA", "label": "580 °C CURIE MAGNETIC BARCODE & ≤200 MA OCEAN FLOOR VS 4 GA CONTINENTS", "detail": "Inked seafloor conveyor-belt and magnetic-barcode diagram on period paper showing mantle upwelling, magnetite locking in Earth's magnetic field below ~580 °C in symmetrical zebra stripes, and oceanic crust age (≤200 Ma vs 4,000 Ma continents)", "scale": "while continental rocks are up to 4 billion years old, the entire ocean floor recycles itself like a conveyor belt every 200 million years", "hold_s": 3.8}),
            ("03_research_ship_towing_magnetometer_over_zebra_striped_ridge", 140.5, 6.5, "B", False, "THE MAGNETIC BARCODE", "Fast",
             "Fast: daylight cutaway view of an oceanographic research ship towing a streamlined brass magnetometer sensor above the Mid-Atlantic Ridge patterned with symmetrical black-and-white basalt stripes. Nothing emissive, no face.",
             STYLE + "In clear daylight, an oceanographic research vessel tows a streamlined brass magnetometer torpedo on a cable above a seabed ridge patterned with symmetrical black-and-white stone stripes." + FAST_TAIL,
             None),
            ("04_explorer_astride_mid_ocean_rift_compass_flipping_stripes", 147.0, 5.5, "B", True, None, "Quality",
             "Quality: Explorer beat 2 (locked character reference).",
             STYLE + "Standing astride Marie Tharp's mid-ocean rift with one foot on each conveyor-belt plate, the Explorer holds a brass compass whose needle flips north and south as matching black and white stripes paint themselves onto the moving rock under its boots." + EXP_TAIL,
             None),
        ],
    ),
    (
        5,
        "Part 05 — Solid Rock That Flows and How Continents Float",
        [
            ("01_timeline_1912_1963_and_crustal_buoyancy_density_chart", 152.5, 8.5, "E", False, "2.7 G/CM³ GRANITE FLOATS ON 3.3 G/CM³ MANTLE", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, the 6-date timeline completes: 6 Jan 1912 & 1915 (Wegener continental drift & Pangaea) · 1924, 15 Nov 1926 & Nov 1930 (Jeffreys & NY symposium reject Wegener; Greenland death) · Autumn 1952 & 1953 (Marie Tharp Mid-Atlantic rift & Foster earthquake overlay) · Nov 1962 (Harry Hess seafloor spreading) · 7 Sep 1963 (Vine & Matthews magnetic barcode) · Today (GPS tracks plates at 1.5–10 cm/year), alongside an inked density cross-section comparing continental granite (2.7 g/cm³) and oceanic basalt (3.0 g/cm³) floating on solid mantle rock (3.3 g/cm³).",
             {"kind": "DATA", "label": "GRANITE (2.7 G/CM³) & BASALT (3.0 G/CM³) FLOATING ON SOLID MANTLE (3.3 G/CM³)", "detail": "Animated 6-date timeline (1912 → Today) alongside an inked crustal buoyancy diagram comparing continental granite (2.7 g/cm³) and oceanic basalt (3.0 g/cm³) floating on solid mantle rock (3.3 g/cm³)", "scale": "granite continents (2.7 g/cm³) float high above basalt ocean crust (3.0 g/cm³) on the denser mantle (3.3 g/cm³) like tall wooden blocks floating beside thin iron plates", "fact_card": "Earth's mantle is solid rock", "when_stamp": "1912–1963", "timeline_step": "6/6 · Today (GPS satellites measure plates moving at 1.5–10 cm/year)", "hold_s": 3.8}),
            ("02_granite_and_basalt_rock_samples_on_balance_bench", 161.0, 5.5, "A", False, "SOLID MANTLE CREEP", "Fast",
             "Fast: daylight close-up of a tall pale pink continental granite block (2.7 g/cm³) and a thin dark oceanic basalt slab (3.0 g/cm³) resting on a brass geological scale beside a core sample of green peridotite mantle rock (3.3 g/cm³). Nothing emissive, no face.",
             STYLE + "In crisp daylight on a geology bench, a tall block of pale pink granite and a thin slab of dark grey basalt sit beside a dense green mantle rock cylinder and a brass scale." + FAST_TAIL,
             None),
            ("03_archimedes_syracuse_250bc_and_galileo_1586_underwater_crown_handoff", 166.5, 6.5, "C", False, "ARCHIMEDES' UNDERWATER SCALE", "Quality",
             "Quality: readable faces (Archimedes in Syracuse around 250 BC and 22-year-old Galileo Galilei in Florence in 1586 dipping a balanced golden wreath crown and a block of pure gold underwater — handoff to 031 Archimedes & Buoyancy).",
             STYLE + "Syracuse, 250 BC, and Florence, 1586: Greek mathematician Archimedes and young Galileo Galilei lower a brass balance scale holding a golden laurel wreath and a pure gold block into a glass tank of water as the wreath tips upward." + QUAL_TAIL,
             {"kind": "WHEN", "label": "~250 BC · 1586", "hold_s": 3.5}),
            ("04_table_three_callback", 173.0, 2.4, "C", False, None, "reuse",
             "Reuse: verified unused moving window [5.50s..7.90s] of P1:07_table_three_props_pangaea_globe_mesosaurus_fossil_sonar_roll (callback, £0).",
             "Reuse P1:07_table_three_props_pangaea_globe_mesosaurus_fossil_sonar_roll [5.50s..7.90s] (2.40s distinct non-overlapping tail window from 8.00s source clip).",
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
                row["reuse_of"] = "P1:07_table_three_props_pangaea_globe_mesosaurus_fossil_sonar_roll"
                row["reuse_window_s"] = [5.5, 7.9]
                row["reuse_audit"] = {
                    "source_row": "P1:07_table_three_props_pangaea_globe_mesosaurus_fossil_sonar_roll",
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
            "film": "030_Wegener-Tharp-Plate-Tectonics",
            "part": p_idx,
            "title": p_title,
            "version": "v01",
            "timing_status": "pre_vo_script_clock (built from tectonics_script_master_v01.md; retimes onto Scribe STT once VO locks)",
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
        "film": "030_Wegener-Tharp-Plate-Tectonics",
        "version": "v01",
        "date": "2026-10-17",
        "owner": "gemini (J0479)",
        "status": "PRE_VO_BOARDS_V01_NO_MINT",
        "generation_authorized": False,
        "script": "00_Brand/Channel-Setup/ideas/030_Wegener-Tharp-Plate-Tectonics/tectonics_script_master_v01.md",
        "sources": "00_Brand/Channel-Setup/ideas/030_Wegener-Tharp-Plate-Tectonics/SOURCES_v01.md",
        "credit_snapshot": {
            "flow_Balance": 23740,
            "flow_floor": 0,
            "flow_read_at": "2026-10-15T21:42:22Z",
            "vertex_promo_gbp": 71.02,
            "vertex_usable_gbp": 70.02,
        },
        "totals": totals,
        "per_part": per_part_summary,
        "mint_order": "006 > 007 > 008 > 009 > 010 > 011 > 012 > 013 > 014 > 015 > 016 > 017 > 018 > 019 > 020 > 021 > 022 > 023 > 024 > 025 > 026 > 027 > 028 > 029 > 030. Nothing in 030 is generation_authorized.",
    }
    (EDIT / "PICTURE_PLAN_v01.json").write_text(json.dumps(plan, indent=2) + "\n")

    sl = [
        "# 030 Continental Drift: The Woman Who Mapped the Hidden Ocean Rift — Shot list & plate boards v01 (pre-VO)",
        "",
        "Gemini, 17 Oct 2026, J0479. Built from `tectonics_script_master_v01.md` (92.0 PASS) and `SOURCES_v01.md`.",
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
        "# 030 price review v01 (pre-VO plate boards)",
        "",
        "Gemini, 17 Oct 2026, J0479. Boards only. **No mint. No spend. No merge.**",
        "Prepared from `tectonics_script_master_v01.md` (92.0 PASS) and `SOURCES_v01.md` so 030's full plate board rows, non-emissive Fast prompts, £0 code graphics, and Teach-on-Screen overlays are ready to re-time the moment long VO locks. Parked for Chief.",
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
        f"- **Quality ({totals['Quality']} rows):** readable faces (Alfred Wegener, Marie Tharp, Rollin T. Chamberlin, Bruce Heezen, Harry Hess, Fred Vine, Drummond Matthews, Archimedes, Galileo Galilei), Arctic whiteout scene, and the 2 Explorer beats.",
        f"- **Fast ({totals['Fast']} rows, non-emissive):** daylight prop and laboratory shots (sonar echogram paper rolls & brass dividers pan, 3-object callback bench, Mesosaurus & Glossopteris shale fossils, six stacked North Atlantic sonar profiles, research ship towing magnetometer over striped ridge, granite & basalt density blocks on brass scale). Zero candles, flames, sparks, or glowing elements on Fast.",
        f"- **£0 code graphics ({totals['code_graphic']} rows):**",
        "  1. `P1:04_wegener_1912_shelf_fit_and_tharp_1952_mid_atlantic_rift_chart` — Wegener's 6 Jan 1912 Pangaea fit across 200 m continental shelves and Marie Tharp's 1952 Mid-Atlantic Ridge V-shaped rift valley (`SCALE: 2.5 centimetres a year — the exact speed your fingernails grow, yet over 200 million years enough to open the 5,000-kilometre Atlantic Ocean`)",
        "  2. `P1:06_2_5_cm_per_year_fingernail_vs_5000_km_atlantic_scale_card` — 2.5 cm/year fingernail growth rate × 200 million years = 5,000 km Atlantic Ocean (`SCALE: moving no faster than your fingernail grows, two continents drift 5,000 kilometres apart in 200 million years`)",
        "  3. `P2:02_torn_newspaper_four_proofs_and_jeffreys_10e10_tidal_chart` — Wegener's 4 'torn newspaper' Pangaea proofs vs Harold Jeffreys's 1924 calculation that tidal force is 10¹⁰× too weak (`SCALE: the tidal push Wegener relied on was ten billion times too weak — like trying to push a brick wall through solid concrete by blowing on it`)",
        "  4. `P3:02_tharp_mid_atlantic_rift_and_foster_1953_earthquake_overlay_chart` — Marie Tharp's 1.5–3 km deep V-shaped rift valley matched 1-to-1 by Howard Foster's 1953 earthquake epicentre dots along a 65,000 km global seam (`SCALE: a continuous underwater mountain chain and rift valley stretching 65,000 kilometres around the planet — long enough to wrap around Earth's equator more than one and a half times`)",
        "  5. `P4:02_seafloor_conveyor_580c_curie_point_magnetic_barcode_diagram` — mantle upwelling, basalt locking in Earth's reversing magnetic field below ~580 °C in symmetrical zebra stripes, and ≤200 Ma ocean floor vs 4 Ga continents (`SCALE: while continental rocks are up to 4 billion years old, the entire ocean floor recycles itself like a conveyor belt every 200 million years`)",
        "  6. `P5:01_timeline_1912_1963_and_crustal_buoyancy_density_chart` — completed 6-date timeline (1912 → Today) + crustal density diagram comparing continental granite (2.7 g/cm³) and oceanic basalt (3.0 g/cm³) floating on solid mantle rock (3.3 g/cm³) (`SCALE: granite continents (2.7 g/cm³) float high above basalt ocean crust (3.0 g/cm³) on the denser mantle (3.3 g/cm³) like tall wooden blocks floating beside thin iron plates`)",
        f"- **£0 verified reuse ({totals['reuse']} row):** `P5:04_table_three_callback` uses the 2.40 s unused moving tail `[5.50s..7.90s]` of `P1:07_table_three_props_pangaea_globe_mesosaurus_fossil_sonar_roll`.",
        "",
        "## Mint order",
        "",
        "006 > 007 > 008 > 009 > 010 > 011 > 012 > 013 > 014 > 015 > 016 > 017 > 018 > 019 > 020 > 021 > 022 > 023 > 024 > 025 > 026 > 027 > 028 > 029 > 030. `generation_authorized` is `false` on every row.",
    ])
    (EDIT / "PRICE_REVIEW_v01.md").write_text("\n".join(pr_lines) + "\n")
    print(f"030 v01 boards written: {totals['rows']} rows, Flow expected={totals['flow_credits_expected']}")


if __name__ == "__main__":
    main()
