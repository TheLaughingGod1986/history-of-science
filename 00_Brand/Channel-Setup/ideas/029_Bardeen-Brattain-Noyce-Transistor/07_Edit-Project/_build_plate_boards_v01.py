#!/usr/bin/env python3
"""HOS 029 (The First Transistor: How a Paperclip and Gold Foil Shrunk Computers) pre-VO plate boards v01. J0479. No mint, no spend.

Built from 00_Brand/Channel-Setup/ideas/029_Bardeen-Brattain-Noyce-Transistor/transistor_script_master_v01.md
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
        "Part 01 — The Paperclip, the Gold Wedge, and 15 Billion Switches",
        [
            ("01_bardeen_brattain_bell_labs_1947_gold_wedge_transistor", 0.0, 5.5, "A", False, "THE FIRST TRANSISTOR", "Quality",
             "Quality: Short frame 0 / answer image (0:03) + Walter Brattain and John Bardeen at Bell Telephone Laboratories in Murray Hill, New Jersey, on 16 December 1947 pressing a small plastic wedge wrapped in gold foil — slit at the tip with a razor blade — onto a germanium crystal as an oscilloscope wave jumps 100-fold.",
             STYLE + "At Bell Telephone Laboratories in Murray Hill, New Jersey, on 16 December 1947, physicist Walter Brattain and theorist John Bardeen press a small triangular plastic wedge wrapped in gold foil onto a shiny slab of germanium crystal with a bent paperclip spring as an oscilloscope wave leaps tall." + QUAL_TAIL,
             {"kind": "WHEN", "label": "MURRAY HILL, 16 DECEMBER 1947", "timeline_step": "1/6 · 16–23 Dec 1947 (Bardeen & Brattain's gold-foil point-contact transistor at Bell Labs)", "hold_s": 3.5}),
            ("02_eniac_tubes_bell_labs_wedge_kilby_noyce_microchip_split", 5.5, 6.0, "B", False, "TUBES, CRYSTAL, MICROCHIP", "Quality",
             "Quality: readable faces & glowing vacuum tubes (the 30-tonne 1946 ENIAC computer glowing with 17,468 glass vacuum tubes on the left; Bardeen and Brattain's December 1947 gold-foil transistor and Shockley's January 1948 Chicago notebook in the centre; Jack Kilby and Robert Noyce's 1958–1959 integrated circuits on the right).",
             STYLE + "Three-panel period composition: on the left, the 30-tonne 1946 ENIAC computer room glowing with racks of hot glass vacuum tubes; in the centre, a gold-foil plastic wedge pressed onto germanium beside an open leather notebook; on the right, a gleaming silicon wafer etched with flat microchips." + QUAL_TAIL,
             None),
            ("03_eniac_philadelphia_1946_17468_glass_vacuum_tubes", 11.5, 6.0, "C", False, "17,468 GLASS TUBES", "Quality",
             "Quality: glowing filaments + readable faces (inside the University of Pennsylvania in February 1946, technicians wheel a cart of replacement glass vacuum tubes past the 30-tonne, 150-kilowatt ENIAC computer as a hot glass tube pops and goes dark).",
             STYLE + "Inside a warm computer room at the University of Pennsylvania in February 1946, two technicians wheel a metal cart stacked with spare glass vacuum tubes past tall black racks of glowing bulbs as one glass tube flashes and goes dark." + QUAL_TAIL,
             {"kind": "WHEN", "label": "PHILADELPHIA, FEBRUARY 1946", "hold_s": 3.5}),
            ("04_point_contact_1947_vs_eniac_vs_15b_microchip_chart", 17.5, 8.0, "E", False, "0.005 CM GAP · 17,468 TUBES → 15B TRANSISTORS", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked schematic and scale comparison shows Walter Brattain and John Bardeen's 16 December 1947 point-contact transistor (two gold-foil contacts separated by 1/500th inch = ~0.005 cm on n-type germanium, amplifying power ~18× to 100×) alongside William Shockley's January 1948 three-layer junction transistor and Jack Kilby (12 September 1958) & Robert Noyce's (23 January 1959) monolithic integrated circuit vs 1946 ENIAC (17,468 tubes, 30 tonnes, 150 kW) and a modern chip (>15 billion switches).",
             {"kind": "DATA", "label": "1946 ENIAC (17,468 TUBES, 30 T) VS 1947 GERMPANIUM WEDGE VS >15B CHIP", "detail": "Inked schematic & scale chart on period paper comparing 1946 ENIAC (17,468 glass tubes, 30 tonnes, 150 kW), 16 Dec 1947 point-contact transistor (0.005 cm razor-slit gold gap on germanium), and a fingernail silicon chip (>15 billion transistors)", "scale": "17,468 glass tubes filling a room and gulping enough power for a hundred homes — replaced today by 15 billion crystal switches on a chip the size of your fingernail", "who_card": "Walter Brattain (1902–1987) — American experimental physicist · John Bardeen (1908–1991) — American theoretical physicist · William Shockley (1910–1989) — American physicist and manager · Jack Kilby (1923–2005) — American electrical engineer · Robert Noyce (1927–1990) — American physicist and co-founder", "when_stamp": "16 December 1947 · 12 September 1958 · 23 January 1959", "hold_s": 3.8}),
            ("05_germanium_slab_and_paperclip_spring_macro_pan", 25.5, 5.5, "A", False, "MURRAY HILL, DECEMBER 1947", "Fast",
             "Fast: daylight macro pan across a bent steel paperclip spring pressing a polystyrene plastic triangle wrapped in gold foil onto a grey metallic germanium crystal slab between code graphics so two full-frame graphics never run back to back. Nothing emissive.",
             STYLE + "In crisp daylight on a wooden lab bench, the camera tracks closely across a bent steel paperclip spring pressing a small plastic triangle wrapped in gold foil onto a polished grey germanium crystal slab." + FAST_TAIL,
             None),
            ("06_1_500th_inch_razor_slit_vs_10cm_vacuum_tube_scale_chart", 31.0, 8.0, "E", False, "1/500TH OF AN INCH", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period parchment, an inked size comparison compares a 10-centimetre glass vacuum tube against Walter Brattain's 1/500th-inch (~50 micrometre, thinner than tissue paper) razor slit in gold foil and modern 3-nanometre silicon transistor gates.",
             {"kind": "DATA", "label": "1/500TH INCH (~50 µM RAZOR SLIT) VS 10 CM GLASS VACUUM TUBE", "detail": "Inked gap comparison on period parchment showing 1/500th inch (~50 µm, thinner than tissue paper) between Brattain's two gold contacts vs a 10 cm glass vacuum tube and 3 nm modern silicon gates", "scale": "a gap one five-hundredth of an inch wide sliced by hand with a razor blade — thinner than a sheet of tissue paper", "hold_s": 3.8}),
            ("07_table_three_props_paperclip_wedge_razor_blade_silicon_wafer", 39.0, 5.5, "C", False, "BELL LABS, DECEMBER 1947", "Fast",
             "Fast: daylight prop table (callback source for Part 05: bent paperclip spring and gold-foil plastic wedge on germanium, steel razor blade, and a mirror-bright etched silicon microchip wafer). Nothing emissive.",
             STYLE + "On a laboratory workbench in soft window light sit three objects side by side: a bent paperclip spring holding a gold-tipped plastic triangle on a germanium crystal, a steel razor blade, and a round patterned silicon wafer." + FAST_TAIL,
             {"kind": "WHEN", "label": "23 DECEMBER 1947", "hold_s": 3.5}),
            ("08_explorer_hot_vacuum_tube_vs_cool_germanium_crystal_switch", 62.0, 5.5, "A", True, None, "Quality",
             "Quality: Explorer beat 1 (locked character reference, after 1:00).",
             STYLE + "Standing between a hot, flickering glass vacuum tube as tall as itself and Brattain's tiny gold-tipped plastic triangle, the Explorer fans itself from the vacuum tube's heat, then taps the cool germanium crystal and watches a small signal wave leap ten times taller." + EXP_TAIL,
             None),
            ("09_shockley_staring_at_bell_labs_point_contact_apparatus", 67.5, 5.5, "B", False, "SHOCKLEY'S RIVALRY", "Quality",
             "Quality: readable face (William Shockley staring tensely at Bardeen and Brattain's point-contact transistor apparatus at Bell Labs in late December 1947).",
             STYLE + "At Bell Telephone Laboratories in December 1947, physicist William Shockley in a dark suit stares tensely down at the small gold-foil wedge and germanium crystal on the laboratory bench." + QUAL_TAIL,
             None),
        ],
    ),
    (
        2,
        "Part 02 — Burning Glass Tubes and the Razor Slit in Gold Foil",
        [
            ("01_de_forest_1906_triode_and_bardeen_1946_surface_states", 73.0, 6.5, "A", False, "1906 TRIODE TO 1946 SURFACE STATES", "Quality",
             "Quality: glowing filament + readable faces (Lee De Forest's 1906 glowing glass triode vacuum tube boiling electrons across a wire grid beside William Shockley's failed April 1945 semiconductor cylinder and John Bardeen's March 1946 chalkboard diagram of surface-state electrons).",
             STYLE + "Murray Hill, New Jersey, March 1946: quiet theorist John Bardeen points to a chalkboard diagram of crystal surface electrons beside a glowing 1906 glass triode bulb and a silent copper-and-silicon test cylinder." + QUAL_TAIL,
             {"kind": "WHO", "label": "Lee De Forest (1873–1961) — American electrical inventor", "fact_card": "Gap cut with razor blade", "when_stamp": "1906 · April 1945 · March 1946", "hold_s": 3.8}),
            ("02_bardeen_surface_states_and_1_500th_inch_hole_injection_diagram", 79.5, 8.0, "E", False, "SURFACE STATES & 50 µM HOLE INJECTION", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked physics diagram shows John Bardeen's March 1946 surface-state electron trap on n-type germanium and Walter Brattain's 16 December 1947 gold-foil polystyrene wedge injecting positive minority 'holes' across a 1/500th-inch (50 µm) razor-cut gap to amplify output power ~18× and voltage ~100×.",
             {"kind": "DATA", "label": "16 DEC 1947 · 50 µM GOLD GAP INJECTS HOLES FOR ~100× GAIN", "detail": "Inked physics diagram on period paper showing Bardeen's March 1946 surface-state electron trap on n-type germanium and Brattain's 16 December 1947 gold-foil plastic wedge injecting minority 'holes' across a 1/500th-inch (50 µm) gap to amplify output ~100×", "scale": "instead of boiling electrons in a hot glass bulb the size of a fist, Bardeen and Brattain steered them through a solid crystal across a gap thinner than tissue paper", "when_stamp": "16 December 1947", "hold_s": 3.8}),
            ("03_brattain_slicing_gold_foil_wedge_with_razor_blade_1947", 87.5, 6.5, "B", False, "THE MIRACLE MONTH", "Quality",
             "Quality: readable faces (Walter Brattain in his Bell Labs coat on 16–23 December 1947 slicing a razor blade across gold foil wrapped on a plastic triangle and pressing it onto a germanium slab while John Bardeen watches).",
             STYLE + "Murray Hill, New Jersey, 16 December 1947: experimentalist Walter Brattain carefully slices a steel razor blade across the gold-foil tip of a small plastic triangle while John Bardeen leans over the germanium crystal bench." + QUAL_TAIL,
             {"kind": "WHEN", "label": "23 DECEMBER 1947", "hold_s": 3.5}),
            ("04_cart_of_spare_unlit_glass_vacuum_tubes_closeup", 94.0, 5.5, "C", False, "FRAGILE GLASS BULBS", "Fast",
             "Fast: daylight close-up of a metal utility cart stacked with dozens of unlit glass vacuum tubes and brass base pins in a 1940s computer hallway. Nothing emissive, no face.",
             STYLE + "In crisp window light, the camera pans across a wheeled metal cart loaded with neat rows of clear unlit glass vacuum tubes with brass contact pins." + FAST_TAIL,
             None),
        ],
    ),
    (
        3,
        "Part 03 — The Hotel Room Rivalry and the Man Who Won Two Physics Nobels",
        [
            ("01_shockley_chicago_hotel_room_new_years_eve_1947_notebook", 99.5, 6.5, "A", False, "CHICAGO HOTEL ROOM · JAN 1948", "Quality",
             "Quality: readable face (William Shockley in shirtsleeves in a Chicago hotel room over New Year's Eve, 31 December 1947 – 23 January 1948, filling notebook pages after learning Julius Edgar Lilienfeld's 1930 patent blocked his field-effect claim).",
             STYLE + "In a Chicago hotel room in January 1948, physicist William Shockley in white shirtsleeves leans intensely over a desk, sketching a three-layer crystal diagram in a leather notebook." + QUAL_TAIL,
             {"kind": "WHO", "label": "Julius Edgar Lilienfeld (1882–1963) — Austro-Hungarian physicist and inventor", "fact_card": "Only 2× Physics Nobel winner", "when_stamp": "1930 · 23 January 1948", "timeline_step": "2/6 · 23 Jan 1948 (Shockley's Chicago hotel-room junction transistor)", "hold_s": 3.8}),
            ("02_shockley_npn_junction_sandwich_and_teal_silicon_diagram", 106.0, 8.0, "E", False, "N-P-N CRYSTAL SANDWICH (100× RIVER)", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked three-layer n-p-n bipolar junction ('sandwich') transistor diagram shows William Shockley's 23 January 1948 design alongside Gordon Teal's May 1954 high-purity grown-junction silicon crystal, where a tiny positive voltage on the thin p-type base lowers the potential barrier and unleashes a 100× electron river from n-type emitter to collector.",
             {"kind": "DATA", "label": "23 JAN 1948 N-P-N JUNCTION SANDWICH & MAY 1954 SILICON CRYSTAL", "detail": "Inked three-layer n-p-n junction transistor diagram on period paper showing how a tiny positive voltage on the thin p-type base lowers the potential barrier and unleashes a 100× electron current from n-type emitter to collector", "scale": "a tiny trickle of electrons into the middle crystal layer opens the floodgate for a river of current a hundred times larger", "who_card": "Gordon Teal (1907–2003) — American physical chemist", "when_stamp": "May 1954", "hold_s": 3.8}),
            ("03_bardeen_1956_and_1972_two_physics_nobel_prizes_stockholm", 114.0, 6.5, "B", False, "TWO PHYSICS NOBEL PRIZES", "Quality",
             "Quality: readable faces (John Bardeen receiving the 1956 Nobel Prize in Physics in Stockholm on 10 December 1956 alongside Brattain and Shockley, and returning in 1972 for his 1957 BCS superconductivity theory).",
             STYLE + "Stockholm concert hall, 10 December 1956 and 1972: physicist John Bardeen in white tie holds two gold Nobel Prize medals with a quiet smile." + QUAL_TAIL,
             {"kind": "WHEN", "label": "10 DECEMBER 1956 · 1957 · 1972", "hold_s": 3.5}),
            ("04_grown_junction_silicon_boule_and_pocket_transistors_bench", 120.5, 5.5, "C", False, "MAY 1954 · SILICON", "Fast",
             "Fast: daylight macro shot of a gleaming cylindrical grown-junction silicon crystal boule beside three small metal-cased silicon transistors on a laboratory table. Nothing emissive, no face.",
             STYLE + "In crisp daylight, a cylindrical silver-grey silicon crystal rod rests on a velvet cloth beside three small three-legged metal transistors." + FAST_TAIL,
             None),
        ],
    ),
    (
        4,
        "Part 04 — The 'Traitorous Eight' and the Summer-Vacation Microchip — Midpoint Twist",
        [
            ("01_traitorous_eight_fairchild_1957_and_kilby_dallas_1958", 126.0, 6.5, "A", False, "FAIRCHILD 1957 & DALLAS 1958", "Quality",
             "Quality: readable faces (Robert Noyce, Gordon Moore, and Jean Hoerni walking out of Shockley Semiconductor Laboratory on 18 September 1957 to found Fairchild Semiconductor, alongside Jack Kilby sitting alone in an empty Texas Instruments lab in Dallas during the July – 12 September 1958 summer holiday).",
             STYLE + "Split period scene: on the left, young physicists Robert Noyce, Gordon Moore, and Jean Hoerni stride out of a California laboratory building in September 1957; on the right, engineer Jack Kilby sits alone at a long workbench in a quiet Dallas laboratory in July 1958." + QUAL_TAIL,
             {"kind": "WHO", "label": "Gordon Moore (1929–2023) — American chemist and co-founder · Jean Hoerni (1924–1997) — Swiss-American physicist", "fact_card": "Invented during summer holiday", "when_stamp": "18 September 1957 · July 1958 · Dallas, 12 September 1958", "timeline_step": "3/6 · 18 Sep 1957 ('Traitorous Eight' found Fairchild) & 4/6 · 12 Sep 1958 & 23 Jan 1959 (Kilby & Noyce microchips)", "hold_s": 3.8}),
            ("02_tyranny_of_numbers_vs_kilby_1958_and_noyce_1959_planar_ic_diagram", 132.5, 8.0, "E", False, "100,000 SOLDER JOINTS VS 1 PLANAR CHIP", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked comparison diagram contrasts the 'Tyranny of Numbers' (thousands of hand-soldered discrete transistors, resistors, and capacitors) against Jack Kilby's 12 September 1958 monolithic germanium oscillator chip and Jean Hoerni & Robert Noyce's 23 January 1959 planar silicon integrated circuit with photolithographically printed aluminium interconnects.",
             {"kind": "DATA", "label": "TYRANNY OF NUMBERS VS 12 SEP 1958 KILBY & 23 JAN 1959 NOYCE IC", "detail": "Inked comparison diagram on period paper of the 'Tyranny of Numbers' (thousands of hand-soldered discrete parts) vs Jack Kilby's 12 September 1958 monolithic germanium chip and Robert Noyce's 23 January 1959 planar silicon integrated circuit", "scale": "instead of soldering 100,000 separate parts together by hand, Noyce's planar chip printed the entire circuit flat onto a sliver of silicon like pages on a printing press", "when_stamp": "23 January 1959", "hold_s": 3.8}),
            ("03_noyce_january_1959_planar_silicon_wafer_mountain_view", 140.5, 6.5, "B", False, "THE SILICON MICROCHIP", "Quality",
             "Quality: readable face (Robert Noyce in Mountain View, California, on 23 January 1959 holding up a gleaming silicon wafer patterned with rows of flat, photolithographically etched microchips).",
             STYLE + "Mountain View, California, 23 January 1959: physicist Robert Noyce holds up a mirror-bright circular silicon wafer patterned with a grid of tiny flat microchips under a magnifying lens." + QUAL_TAIL,
             None),
            ("04_explorer_tangled_wires_to_planar_stencil_microchip", 147.0, 5.5, "B", True, None, "Quality",
             "Quality: Explorer beat 2 (locked character reference).",
             STYLE + "Tangled inside a giant bird's nest of hand-soldered wires and loose resistors, the Explorer sets the tangle aside, shines a beam of light through a stencil onto a flat silicon disc, and lifts up a gleaming microchip no bigger than a button." + EXP_TAIL,
             None),
        ],
    ),
    (
        5,
        "Part 05 — Moore's Law and the Moving Ground Beneath Silicon Valley",
        [
            ("01_timeline_1947_2000_and_moores_law_15_billion_chart", 152.5, 8.5, "E", False, "MOORE'S LAW · >15 BILLION TRANSISTORS", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, the 6-date timeline completes: 16–23 Dec 1947 (Bardeen & Brattain point-contact transistor) · 23 Jan 1948 (Shockley junction transistor) · 18 Sep 1957 ('Traitorous Eight' found Fairchild) · 12 Sep 1958 & 23 Jan 1959 (Kilby & Noyce integrated circuits) · 19 Apr 1965 & Jul 1968 (Gordon Moore's Law & Intel) · 2000–Today (Kilby Nobel; >15–100 billion transistors/chip), alongside an inked Moore's Law exponential curve.",
             {"kind": "DATA", "label": "MOORE'S LAW (1965): 1 TRANSISTOR (1947) → >15 BILLION ON A FINGERNAIL", "detail": "Animated 6-date timeline (1947 → Today) alongside an inked Moore's Law exponential chart rising from 1 transistor (1947) and 4 components (1958) to >15 billion transistors on a fingernail-sized silicon chip (15 atoms wide)", "scale": "from 1 hand-sliced transistor in 1947 to more than 15 billion transistors on a single phone chip today — with each gate just 15 silicon atoms wide", "fact_card": "Made from ordinary sand", "when_stamp": "19 April 1965 · July 1968 · 2000 · 1947–2000", "timeline_step": "5/6 · 19 Apr 1965 & Jul 1968 (Moore's Law & Intel) & 6/6 · 2000–Today (Kilby Nobel & >15B transistors/chip)", "hold_s": 3.8}),
            ("02_quartz_beach_sand_to_silicon_boule_and_wafer_bench", 161.0, 5.5, "A", False, "28% OF EARTH'S CRUST", "Fast",
             "Fast: daylight close-up of golden quartz beach sand (27.7% silicon in Earth's crust) beside a mirror-bright single-crystal silicon ingot boule and a patterned silicon microprocessor wafer. Nothing emissive, no face.",
             STYLE + "In crisp daylight on a laboratory table, a glass dish of golden quartz beach sand sits beside a polished silver-grey silicon crystal cylinder and a patterned microprocessor wafer." + FAST_TAIL,
             None),
            ("03_wegener_1912_pangaea_globe_and_tharp_1952_ocean_rift_handoff", 166.5, 6.5, "C", False, "THE MOVING CONTINENTS", "Quality",
             "Quality: readable faces (Alfred Wegener in Frankfurt on 6 January 1912 fitting South America and Africa together on a globe beside Marie Tharp in New York in 1952 inking the 16,000-kilometre Mid-Atlantic Ridge rift valley — handoff to 030 Continental Drift & Plate Tectonics).",
             STYLE + "Frankfurt, 6 January 1912 and New York, 1952: meteorologist Alfred Wegener fits the coastlines of South America and Africa together on a brass globe while cartographer Marie Tharp inks a deep V-shaped rift valley down a map of the Atlantic Ocean floor." + QUAL_TAIL,
             {"kind": "WHEN", "label": "6 JANUARY 1912 · 1952", "hold_s": 3.5}),
            ("04_table_three_callback", 173.0, 2.4, "C", False, None, "reuse",
             "Reuse: verified unused moving window [5.50s..7.90s] of P1:07_table_three_props_paperclip_wedge_razor_blade_silicon_wafer (callback, £0).",
             "Reuse P1:07_table_three_props_paperclip_wedge_razor_blade_silicon_wafer [5.50s..7.90s] (2.40s distinct non-overlapping tail window from 8.00s source clip).",
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
                row["reuse_of"] = "P1:07_table_three_props_paperclip_wedge_razor_blade_silicon_wafer"
                row["reuse_window_s"] = [5.5, 7.9]
                row["reuse_audit"] = {
                    "source_row": "P1:07_table_three_props_paperclip_wedge_razor_blade_silicon_wafer",
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
            "film": "029_Bardeen-Brattain-Noyce-Transistor",
            "part": p_idx,
            "title": p_title,
            "version": "v01",
            "timing_status": "pre_vo_script_clock (built from transistor_script_master_v01.md; retimes onto Scribe STT once VO locks)",
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
        "film": "029_Bardeen-Brattain-Noyce-Transistor",
        "version": "v01",
        "date": "2026-10-17",
        "owner": "gemini (J0479)",
        "status": "PRE_VO_BOARDS_V01_NO_MINT",
        "generation_authorized": False,
        "script": "00_Brand/Channel-Setup/ideas/029_Bardeen-Brattain-Noyce-Transistor/transistor_script_master_v01.md",
        "sources": "00_Brand/Channel-Setup/ideas/029_Bardeen-Brattain-Noyce-Transistor/SOURCES_v01.md",
        "credit_snapshot": {
            "flow_Balance": 23740,
            "flow_floor": 0,
            "flow_read_at": "2026-10-15T21:42:22Z",
            "vertex_promo_gbp": 71.02,
            "vertex_usable_gbp": 70.02,
        },
        "totals": totals,
        "per_part": per_part_summary,
        "mint_order": "006 > 007 > 008 > 009 > 010 > 011 > 012 > 013 > 014 > 015 > 016 > 017 > 018 > 019 > 020 > 021 > 022 > 023 > 024 > 025 > 026 > 027 > 028 > 029. Nothing in 029 is generation_authorized.",
    }
    (EDIT / "PICTURE_PLAN_v01.json").write_text(json.dumps(plan, indent=2) + "\n")

    sl = [
        "# 029 The First Transistor: How a Paperclip and Gold Foil Shrunk Computers — Shot list & plate boards v01 (pre-VO)",
        "",
        "Gemini, 17 Oct 2026, J0479. Built from `transistor_script_master_v01.md` (92.6 PASS) and `SOURCES_v01.md`.",
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
        "# 029 price review v01 (pre-VO plate boards)",
        "",
        "Gemini, 17 Oct 2026, J0479. Boards only. **No mint. No spend. No merge.**",
        "Prepared from `transistor_script_master_v01.md` (92.6 PASS) and `SOURCES_v01.md` so 029's full plate board rows, non-emissive Fast prompts, £0 code graphics, and Teach-on-Screen overlays are ready to re-time the moment long VO locks. Parked for Chief.",
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
        f"- **Quality ({totals['Quality']} rows):** readable faces (Walter Brattain, John Bardeen, William Shockley, Lee De Forest, Gordon Teal, Robert Noyce, Gordon Moore, Jean Hoerni, Jack Kilby, Alfred Wegener, Marie Tharp), glowing vacuum tubes (1946 ENIAC & 1906 triode), and the 2 Explorer beats.",
        f"- **Fast ({totals['Fast']} rows, non-emissive):** daylight prop and laboratory shots (germanium slab & paperclip spring pan, 3-object callback bench, cart of unlit spare glass tubes, grown-junction silicon boule & metal-cased transistors, quartz beach sand beside silicon ingot & patterned wafer). Zero candles, flames, sparks, or glowing elements on Fast.",
        f"- **£0 code graphics ({totals['code_graphic']} rows):**",
        "  1. `P1:04_point_contact_1947_vs_eniac_vs_15b_microchip_chart` — 16 Dec 1947 point-contact transistor (0.005 cm razor-slit gold gap on germanium) vs 1946 ENIAC (17,468 tubes, 30 tonnes, 150 kW) and a modern >15B transistor smartphone chip (`SCALE: 17,468 glass tubes filling a room and gulping enough power for a hundred homes — replaced today by 15 billion crystal switches on a chip the size of your fingernail`)",
        "  2. `P1:06_1_500th_inch_razor_slit_vs_10cm_vacuum_tube_scale_chart` — Brattain's 1/500th-inch (~50 µm) razor slit in gold foil vs a 10 cm glass vacuum tube and 3 nm silicon gates (`SCALE: a gap one five-hundredth of an inch wide sliced by hand with a razor blade — thinner than a sheet of tissue paper`)",
        "  3. `P2:02_bardeen_surface_states_and_1_500th_inch_hole_injection_diagram` — Bardeen's March 1946 surface-state electron trap on n-type germanium and Brattain's 16 Dec 1947 gold-foil wedge injecting minority 'holes' across a 50 µm gap (`SCALE: instead of boiling electrons in a hot glass bulb the size of a fist, Bardeen and Brattain steered them through a solid crystal across a gap thinner than tissue paper`)",
        "  4. `P3:02_shockley_npn_junction_sandwich_and_teal_silicon_diagram` — Shockley's 23 Jan 1948 n-p-n bipolar junction ('sandwich') transistor and Gordon Teal's May 1954 grown-junction silicon crystal (`SCALE: a tiny trickle of electrons into the middle crystal layer opens the floodgate for a river of current a hundred times larger`)",
        "  5. `P4:02_tyranny_of_numbers_vs_kilby_1958_and_noyce_1959_planar_ic_diagram` — 'Tyranny of Numbers' (hand-soldered discrete components) vs Jack Kilby's 12 Sep 1958 monolithic germanium oscillator chip and Robert Noyce's 23 Jan 1959 planar silicon integrated circuit (`SCALE: instead of soldering 100,000 separate parts together by hand, Noyce's planar chip printed the entire circuit flat onto a sliver of silicon like pages on a printing press`)",
        "  6. `P5:01_timeline_1947_2000_and_moores_law_15_billion_chart` — completed 6-date timeline (16 Dec 1947 → Today) + Moore's Law exponential curve rising from 1 transistor (1947) to >15 billion transistors on a fingernail-sized silicon chip (`SCALE: from 1 hand-sliced transistor in 1947 to more than 15 billion transistors on a single phone chip today — with each gate just 15 silicon atoms wide`)",
        f"- **£0 verified reuse ({totals['reuse']} row):** `P5:04_table_three_callback` uses the 2.40 s unused moving tail `[5.50s..7.90s]` of `P1:07_table_three_props_paperclip_wedge_razor_blade_silicon_wafer`.",
        "",
        "## Mint order",
        "",
        "006 > 007 > 008 > 009 > 010 > 011 > 012 > 013 > 014 > 015 > 016 > 017 > 018 > 019 > 020 > 021 > 022 > 023 > 024 > 025 > 026 > 027 > 028 > 029. `generation_authorized` is `false` on every row.",
    ])
    (EDIT / "PRICE_REVIEW_v01.md").write_text("\n".join(pr_lines) + "\n")
    print(f"029 v01 boards written: {totals['rows']} rows, Flow expected={totals['flow_credits_expected']}")


if __name__ == "__main__":
    main()
