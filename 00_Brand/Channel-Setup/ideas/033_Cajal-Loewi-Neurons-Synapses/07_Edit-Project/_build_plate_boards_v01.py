#!/usr/bin/env python3
"""HOS 033 (Neurons & Synapses: The 3 AM Dream That Solved How Brains Work) pre-VO plate boards v01. J0494. No mint, no spend.

Built from 00_Brand/Channel-Setup/ideas/033_Cajal-Loewi-Neurons-Synapses/neurons_script_master_v01.md
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
        "Part 01 — The Kitchen Table in Barcelona and the 3:00 a.m. Dream in Austria",
        [
            ("01_cajal_1888_barcelona_microscope_and_loewi_1921_graz_frog_hearts", 0.0, 5.5, "A", False, "WHY BRAIN CELLS NEVER TOUCH", "Quality",
             "Quality: Short frame 0 / answer image (0:03) + at a candlelit kitchen table in Barcelona in May 1888, 36-year-old Spanish anatomist Santiago Ramón y Cajal peers through a brass microscope at a slice of chick brain stained with silver nitrate where a single Purkinje neuron stands out jet-black, dissolving to Graz, Austria, at 3:00 a.m. in March 1921 as Otto Loewi transfers clear saline drops between two beating frog hearts in glass chambers.",
             STYLE + "At a candlelit kitchen table in Barcelona in May 1888, bearded Spanish anatomist Santiago Ramón y Cajal peers through a brass microscope at a jet-black branching neuron on a glass slide, dissolving to a midnight laboratory in Graz in March 1921 as pharmacologist Otto Loewi transfers clear drops with a pipette between two glass frog-heart chambers." + QUAL_TAIL,
             {"kind": "WHEN", "label": "BARCELONA, MAY 1888 · GRAZ, MARCH 1921", "timeline_step": "2/5 · May 1888–1891 (Cajal proves Neuron Doctrine) & 4/5 · Mar 1921 & 1936 (Loewi's 3:00 a.m. Vagusstoff frog-heart experiment)", "hold_s": 3.5}),
            ("02_golgi_silver_bottle_cajal_1906_nobel_clash_loewi_chambers_split", 5.5, 6.0, "B", False, "SILVER, GAPS, CHEMICAL SPARKS", "Quality",
             "Quality: complex three-part split composition (Camillo Golgi's 1873 silver chromate bottle and Cajal's 1888 pen-and-ink neuron drawings on the left; Golgi and Cajal clashing on the Stockholm Nobel stage in December 1906 in the centre; Otto Loewi's two glass frog-heart chambers in March 1921 on the right).",
             STYLE + "Three-panel period composition: on the left, an amber glass bottle of silver nitrate beside an India-ink drawing of a branching neuron; in the centre, two bearded scientists arguing before neuron wall charts on a grand podium; on the right, two glass chambers connected to a smoked kymograph drum." + QUAL_TAIL,
             None),
            ("03_cajal_barcelona_1888_lifting_silver_slide_and_sketching_neuron", 11.5, 6.0, "C", False, "ONE CELL IN A HUNDRED", "Quality",
             "Quality: readable face (in his home kitchen laboratory in Barcelona in May 1888, Santiago Ramón y Cajal lifts a glass slide from an amber silver-nitrate dish and sketches the tree-like branches of a single black neuron in India ink).",
             STYLE + "In a warm Barcelona kitchen laboratory in May 1888, thirty-six-year-old Santiago Ramón y Cajal lifts a stained glass slide with brass forceps, peers through his microscope, and draws a tree-like black nerve cell with a fine dip pen." + QUAL_TAIL,
             {"kind": "WHEN", "label": "BARCELONA, 1888", "hold_s": 3.5}),
            ("04_86_billion_neurons_20nm_synaptic_cleft_and_acetylcholine_diagram", 17.5, 8.0, "E", False, "86 BILLION NEURONS · 20 NM SYNAPTIC CLEFT", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked scale and brain-network diagram shows 86 billion separate silver-stained neurons connected by ~100 trillion synapses (named 'neuron' by Waldeyer in 1891 and 'synapse' by Sherrington in 1897), each separated by a 20-nanometre synaptic cleft (5,000× thinner than a 100,000 nm human hair) where an electrical impulse arriving at up to 100 m/s triggers chemical neurotransmitter release (acetylcholine, discovered by Otto Loewi in March 1921).",
             {"kind": "DATA", "label": "86 BILLION NEURONS · 100 TRILLION SYNAPSES · 20 NM CLEFT (5,000× THINNER THAN HAIR)", "detail": "Inked scale & brain-network diagram on period paper showing 86 billion neurons connected by ~100 trillion synapses, each separated by a 20-nanometre synaptic cleft (5,000× thinner than a 100,000 nm human hair)", "scale": "a synaptic gap is just 20 nanometres wide — five thousand times thinner than a single human hair, yet wide enough that no two brain cells fuse together", "who_card": "Camillo Golgi (1843–1926) — Italian physician and histologist · Santiago Ramón y Cajal (1852–1934) — Spanish neuroanatomist · Otto Loewi (1873–1961) — German-Austrian pharmacologist", "when_stamp": "1873 · May 1888 · March 1921", "hold_s": 3.8}),
            ("05_cajal_brass_microscope_micrometer_and_india_ink_drawings_pan", 25.5, 5.5, "A", False, "BARCELONA, 1888", "Fast",
             "Fast: daylight macro pan across Cajal's brass monocular microscope, glass slides stained golden-amber, and his hand-drawn India-ink sheets of cerebellar Purkinje neurons between code graphics so two full-frame graphics never run back to back. Nothing emissive, no face.",
             STYLE + "In crisp daylight on a wooden table, the camera pans across a gleaming brass microscope, amber-stained glass slides, and intricate black India-ink drawings of branching nerve cells." + FAST_TAIL,
             None),
            ("06_human_hair_100000nm_vs_rbc_7500nm_vs_20nm_synaptic_cleft_card", 31.0, 8.0, "E", False, "20 NANOMETRE GAP", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period parchment, an inked size-scale bar compares the thickness of a human hair (100,000 nm), a red blood cell (7,500 nm), and the 20–40 nanometre synaptic cleft between an axon terminal button and a dendritic spine.",
             {"kind": "DATA", "label": "HUMAN HAIR (100,000 NM) VS RED BLOOD CELL (7,500 NM) VS SYNAPSE (20 NM)", "detail": "Inked size-scale bar comparing a human hair (100,000 nm) vs a red blood cell (7,500 nm) vs the synaptic cleft (20–40 nm)", "scale": "five thousand synaptic gaps laid side by side would barely span the width of one human hair", "hold_s": 3.8}),
            ("07_table_three_props_silver_nitrate_cajal_drawing_frog_heart_chambers", 39.0, 5.5, "C", False, "1873 TO 1921", "Fast",
             "Fast: daylight prop table (callback source for Part 05: Golgi's amber silver-nitrate bottle and glass slide dish, Cajal's brass microscope with an India-ink Purkinje cell drawing, and Loewi's twin glass chambers with a smoked kymograph drum). Nothing emissive.",
             STYLE + "On a wooden laboratory bench in soft window light sit three objects side by side: an amber reagent bottle beside a glass staining dish, a brass microscope resting on an ink neuron drawing, and two clear glass organ chambers beside a smoked recording drum." + FAST_TAIL,
             None),
            ("08_explorer_axon_cliff_tossing_chemical_vial_across_20nm_canyon", 62.0, 5.5, "A", True, None, "Quality",
             "Quality: Explorer beat 1 (locked character reference, after 1:00).",
             STYLE + "Standing on the tip of a giant silver-stained axon terminal like a cliff edge, the Explorer peers through a brass spyglass across a narrow canyon at the neighbouring dendrite, tosses a tiny glass vial of amber chemical messenger droplets across the gap, and beams as the far cliff ripples with wave rings." + EXP_TAIL,
             None),
            ("09_cajal_holding_purkinje_neuron_ink_drawing_beside_microscope", 67.5, 5.5, "B", False, "PURKINJE CELL · 1888", "Quality",
             "Quality: readable face (Santiago Ramón y Cajal holding his India-ink drawing of a cerebellar Purkinje cell up beside his brass microscope).",
             STYLE + "In his Barcelona study in 1888, bearded Santiago Ramón y Cajal holds up a finely detailed India-ink drawing of a tree-like Purkinje brain cell beside his brass microscope." + QUAL_TAIL,
             None),
        ],
    ),
    (
        2,
        "Part 02 — The Tangle in the Microscope & Golgi's 1873 'Black Reaction'",
        [
            ("01_golgi_1873_abbiategrasso_kitchen_silver_nitrate_black_reaction", 73.0, 6.5, "A", False, "ABBIATEGRASSO · 2 AUGUST 1873", "Quality",
             "Quality: candlelit scene + readable face (30-year-old Italian physician Camillo Golgi on 2 August 1873 in his apartment kitchen at the Abbiategrasso hospital near Milan dropping a potassium-dichromate-hardened brain slice into silver nitrate).",
             STYLE + "In a quiet candlelit apartment kitchen in Abbiategrasso in August 1873, thirty-year-old Italian physician Camillo Golgi uses brass forceps to lower an orange potassium-dichromate-hardened tissue slice into a glass dish of silver nitrate." + QUAL_TAIL,
             {"kind": "FACT", "label": "Stained just 1 in 100 cells", "when_stamp": "2 August 1873", "timeline_step": "1/5 · 2 Aug 1873 (Camillo Golgi discovers la reazione nera silver stain in Abbiategrasso)", "hold_s": 3.8}),
            ("02_carmine_100_percent_tangle_vs_golgi_1_to_5_percent_black_stain_chart", 79.5, 8.0, "E", False, "100% CARMINE TANGLE VS 1%–5% GOLGI BLACK REACTION", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked comparison diagram contrasts conventional carmine dye (100% of neurons stained at once = an unreadable solid tangled mat) against Camillo Golgi's 2 August 1873 silver chromate 'black reaction' (1%–5% of neurons stained stark black on a transparent yellow background).",
             {"kind": "DATA", "label": "100% DYE (UNREADABLE TANGLE) VS GOLGI'S 1%–5% BLACK SILVER STAIN", "detail": "Inked comparison diagram on period paper showing conventional carmine stain (100% of neurons stained = unreadable tangled mat) vs Camillo Golgi's 1873 silver chromate 'black reaction' (1%–5% of neurons stained stark black on a clear yellow background)", "scale": "by staining only one to five cells out of every hundred, Golgi's silver reaction made single trees visible inside the densest forest in nature", "hold_s": 3.8}),
            ("03_golgi_microscope_view_single_black_pyramidal_neuron_on_amber", 87.5, 6.5, "B", False, "LA REAZIONE NERA, 1873", "Fast",
             "Fast: daylight circular microscope field showing a single jet-black silver-chromate-stained pyramidal neuron and its delicate branching dendrites standing out sharply against a clear golden-yellow background. Nothing emissive, no face.",
             STYLE + "Through a circular microscope lens in bright transmitted light, a single jet-black branching pyramidal nerve cell stands out like fine ink against a clear golden-amber background." + FAST_TAIL,
             None),
            ("04_potassium_dichromate_and_silver_nitrate_glass_dishes_bench", 94.0, 5.5, "C", False, "SILVER CHROMATE CRYSTALS", "Fast",
             "Fast: daylight close-up of two glass staining dishes containing orange potassium dichromate and clear silver nitrate beside mounted microscope slides on a wooden bench. Nothing emissive, no face.",
             STYLE + "In soft daylight on a wooden bench sit two glass dishes — one holding amber dichromate solution, the other clear silver solution — beside mounted glass microscope slides." + FAST_TAIL,
             None),
        ],
    ),
    (
        3,
        "Part 03 — The Painter in Barcelona & the 1906 Nobel Stage Fight",
        [
            ("01_cajal_1888_embryonic_stain_sherrington_1897_and_1906_nobel_clash", 99.5, 6.5, "A", False, "CLASHED ON THE NOBEL STAGE", "Quality",
             "Quality: readable faces (Santiago Ramón y Cajal in Barcelona in May 1888 drawing embryonic chick neurons alongside English physiologist Charles Scott Sherrington in 1897 and Golgi and Cajal clashing on the Stockholm Nobel podium on 11–12 December 1906).",
             STYLE + "Split period scene: on the left, English physiologist Charles Sherrington in spectacles examines a reflex chart in 1897; on the right in Stockholm in December 1906, Camillo Golgi and Santiago Ramón y Cajal gesture toward rival neuron diagrams on the Nobel lecture stage." + QUAL_TAIL,
             {"kind": "WHO", "label": "Charles Scott Sherrington (1857–1952) — English neurophysiologist", "fact_card": "Clashed on the Nobel stage", "when_stamp": "1887 · 1891 · 1897 · 11 December 1906 · 12 December 1906 · 1954", "timeline_step": "3/5 · 1897 & Dec 1906 (Sherrington coins 'synapse'; Golgi & Cajal clash at Nobel lectures)", "hold_s": 3.8}),
            ("02_cajal_dynamic_polarization_and_1954_electron_microscope_20nm_chart", 106.0, 8.0, "E", False, "ONE-WAY POLARIZATION & 1954 ELECTRON MICROSCOPE (0.2 NM VS 200 NM)", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked schematic of Cajal's Law of Dynamic Polarization (dendrites → soma → axon → 20 nm synaptic cleft → next dendrite) sits alongside a resolution chart comparing 19th-century light microscopes (200 nm blur limit) against 1954–1955 electron microscopy (0.2 nm resolution directly photographing the 20 nm synaptic cleft and vesicles).",
             {"kind": "DATA", "label": "DYNAMIC POLARIZATION & 1954 ELECTRON MICROSCOPE (20 NM CLEFT VS 200 NM LIGHT LIMIT)", "detail": "Inked diagram on period paper of Cajal's Law of Dynamic Polarization (dendrites → soma → axon → 20 nm synaptic cleft → next dendrite) alongside 1954–1955 electron microscopy resolution (0.2 nm resolving the 20 nm cleft vs 200 nm light limit)", "scale": "nineteenth-century light microscopes blurred anything smaller than 200 nanometres — ten times wider than the 20-nanometre synaptic gap, which is why only Cajal's embryonic silver stains and 1950s electron microscopes could prove the gap was real", "hold_s": 3.8}),
            ("03_stockholm_december_1906_golgi_and_cajal_nobel_lectures", 114.0, 6.5, "B", False, "STOCKHOLM, DECEMBER 1906", "Quality",
             "Quality: readable faces (Stockholm, 11–12 December 1906: Camillo Golgi and Santiago Ramón y Cajal standing before large wall charts of silver-stained neurons on the Nobel lecture stage, arguing opposite theories of the human brain).",
             STYLE + "In a grand Stockholm lecture hall in December 1906, Camillo Golgi and Santiago Ramón y Cajal in formal evening dress stand beside large hung wall charts of black-stained nerve cells, debating before an attentive academy audience." + QUAL_TAIL,
             None),
            ("04_cajal_india_ink_arrows_showing_one_way_dendrite_to_axon_flow", 120.5, 5.5, "C", False, "ONE-WAY STREET", "Fast",
             "Fast: daylight close-up of Cajal's original pen-and-ink botanical-style drawing of an embryonic neuron where small inked arrows trace the one-way signal path from bushy dendrites through the cell body and out along the axon terminal. Nothing emissive, no face.",
             STYLE + "In crisp daylight, a brass pointer traces fine ink arrows along a vintage sepia anatomical drawing of a branching nerve cell from its feathery top branches down its single long trunk." + FAST_TAIL,
             None),
        ],
    ),
    (
        4,
        "Part 04 — The War of the Soups and the Sparks & Otto Loewi's 3:00 a.m. Easter Dream — Midpoint Twist",
        [
            ("01_loewi_march_1921_graz_3am_dream_and_dale_acetylcholine", 126.0, 6.5, "A", False, "GRAZ · MARCH 1921 · 3:00 A.M.", "Quality",
             "Quality: readable faces (at Graz, Austria, on Easter weekend in March 1921, 47-year-old pharmacologist Otto Loewi wakes at 3:00 a.m., hurries to his university lab, and connects two beating frog hearts in glass saline chambers alongside English collaborator Henry Hallett Dale).",
             STYLE + "In a dimly lit laboratory in Graz in March 1921 at three in the morning, pharmacologist Otto Loewi in a waistcoat leans over two glass organ baths holding beating frog hearts while English scientist Henry Dale examines a kymograph trace." + QUAL_TAIL,
             {"kind": "WHO", "label": "Henry Hallett Dale (1875–1968) — English pharmacologist and physiologist", "fact_card": "Dreamed the experiment twice", "when_stamp": "1903 · March 1921 · 1936", "timeline_step": "4/5 · Mar 1921 & 1936 (Loewi's 3:00 a.m. two-heart Vagusstoff experiment; 1936 Nobel Prize with Dale)", "hold_s": 3.8}),
            ("02_loewi_two_frog_hearts_vagusstoff_kymograph_40_to_12_bpm_diagram", 132.5, 8.0, "E", False, "HEART #1 (VAGUS STIMULATED) → PIPETTE → NERVE-FREE HEART #2 SLOWS", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, an inked kymograph and two-heart diagram of Otto Loewi's March 1921 Graz experiment shows Heart #1 (with vagus nerve stimulated) slowing from ~40 bpm to ~10–15 bpm, and transferring a pipette of Vagusstoff (acetylcholine) saline to nerve-free Heart #2 slowing Heart #2 identically without electrical contact.",
             {"kind": "DATA", "label": "LOEWI'S TWO-HEART EXPERIMENT: VAGUSSTOFF (ACETYLCHOLINE) SLOWS HEART #2 (~40 → 12 BPM)", "detail": "Inked kymograph & two-heart diagram on period paper of Otto Loewi's March 1921 Graz experiment (Heart #1 slows from ~40 bpm to ~10–15 bpm; transferring Vagusstoff / acetylcholine saline to denervated Heart #2 slows Heart #2 identically without electrical contact)", "scale": "a few drops of clear salt water pipetted from one frog heart to another at three in the morning proved that every human thought, memory, and heartbeat relies on microscopic chemical messengers crossing a 20-nanometre gap", "hold_s": 3.8}),
            ("03_loewi_pipetting_vagusstoff_saline_into_heart_2_kymograph_trace", 140.5, 6.5, "B", False, "GRAZ, 3:00 A.M. — VAGUSSTOFF", "Quality",
             "Quality: readable face and hands (Otto Loewi at 3:30 a.m. in March 1921 squeezing a glass pipette of clear saline from Heart #1 into the chamber of nerve-free Heart #2 and watching the smoked-drum needle trace slow down at once).",
             STYLE + "In his Graz laboratory at night in March 1921, Otto Loewi carefully squeezes three clear drops from a glass pipette into a second glass chamber and smiles as a brass stylus slows its white wave trace on a revolving smoked drum." + QUAL_TAIL,
             None),
            ("04_explorer_crumpled_note_pipetting_three_amber_drops_between_chambers", 147.0, 5.5, "B", True, None, "Quality",
             "Quality: Explorer beat 2 (locked character reference).",
             STYLE + "Peering at a crumpled bedside note covered in unreadable squiggles, the Explorer shrugs, then uses a tiny glass pipette to transfer three amber droplets from one pulsing glass chamber into a second chamber and beams as the second drum trace slows in step." + EXP_TAIL,
             None),
        ],
    ),
    (
        5,
        "Part 05 — Why Both 'Soups' and 'Sparks' Were Right — and the Invisible Blanket Around Earth",
        [
            ("01_timeline_1873_1955_and_electrochemical_100ms_20nm_relay_chart", 152.5, 8.5, "E", False, "100 M/S ELECTRICAL SPARK → <1 MS CHEMICAL PUFF ACROSS 20 NM", "code_graphic",
             "Flow-first: a teach diagram, chart, counter or timeline is a £0 code graphic. No Flow mint.",
             "Own code graphic: on period paper, the 5-date timeline completes: 2 Aug 1873 (Golgi's black silver stain) · May 1888–1891 (Cajal proves Neuron Doctrine; Waldeyer coins 'neuron') · 1897 & Dec 1906 (Sherrington coins 'synapse'; 1906 Nobel clash) · Mar 1921 & 1936 (Loewi's 3:00 a.m. Vagusstoff frog-heart experiment; 1936 Nobel with Dale) · 1954–1955 (Palade & Palay electron microscope resolves 20 nm synaptic cleft), alongside an inked electrochemical relay diagram (100 m/s action potential → <1 ms chemical diffusion across 20 nm).",
             {"kind": "DATA", "label": "1873–1955 TIMELINE & ELECTROCHEMICAL RELAY (100 M/S SPARK → <1 MS 20 NM PUFF)", "detail": "Animated 5-date timeline (1873 → 1955) alongside an inked electrochemical relay diagram showing an electrical spike racing down an axon at 100 m/s and releasing chemical vesicles across the 20 nm cleft in <1 ms", "scale": "an electrical impulse racing at 100 metres per second converts into a chemical puff that crosses a 20-nanometre gap in less than one millisecond — firing across 100 trillion synapses inside a three-pound brain", "fact_card": "100 trillion chemical gaps", "when_stamp": "1873–1955", "timeline_step": "5/5 · 1954–1955 (Palade & Palay photograph the 20 nm synaptic cleft by electron microscopy)", "hold_s": 3.8}),
            ("02_synaptic_vesicles_releasing_neurotransmitters_across_20nm_gap", 161.0, 5.5, "A", False, "SPARK TO SOUP TO SPARK", "Fast",
             "Fast: daylight matte painted anatomical cross-section of a synaptic terminal showing tiny spherical vesicles opening at the membrane to release chemical messenger spheres across a narrow 20-nanometre cleft into receptor cups on the neighbouring dendrite. Nothing emissive, no face.",
             STYLE + "In crisp daylight, a detailed anatomical model shows tiny round vesicles at the tip of a nerve fibre opening to release small messenger spheres across a narrow gap into matching receptor cups on the next cell." + FAST_TAIL,
             None),
            ("03_foote_1856_sunlit_cylinders_and_tyndall_1859_rock_salt_tube_handoff", 166.5, 6.5, "C", False, "EARTH'S INVISIBLE BLANKET", "Quality",
             "Quality: readable faces (Eunice Newton Foote in Seneca Falls, New York, in August 1856 placing two 30-inch glass cylinders with thermometers in the summer sunlight, beside John Tyndall in May 1859 in London adjusting his brass rock-salt infrared tube — handoff to 034 The Greenhouse Effect).",
             STYLE + "Seneca Falls, New York, August 1856, and London, May 1859: scientist Eunice Newton Foote inspects two tall sunlit glass cylinders fitted with mercury thermometers in a garden, while physicist John Tyndall adjusts a four-foot brass tube fitted with rock-salt windows." + QUAL_TAIL,
             {"kind": "WHEN", "label": "AUGUST 1856 · 1859 · 1896", "hold_s": 3.5}),
            ("04_table_three_callback", 173.0, 2.4, "C", False, None, "reuse",
             "Reuse: verified unused moving window [5.50s..7.90s] of P1:07_table_three_props_silver_nitrate_cajal_drawing_frog_heart_chambers (callback, £0).",
             "Reuse P1:07_table_three_props_silver_nitrate_cajal_drawing_frog_heart_chambers [5.50s..7.90s] (2.40s distinct non-overlapping tail window from 8.00s source clip).",
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
                row["reuse_of"] = "P1:07_table_three_props_silver_nitrate_cajal_drawing_frog_heart_chambers"
                row["reuse_window_s"] = [5.5, 7.9]
                row["reuse_audit"] = {
                    "source_row": "P1:07_table_three_props_silver_nitrate_cajal_drawing_frog_heart_chambers",
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
            "film": "033_Cajal-Loewi-Neurons-Synapses",
            "part": p_idx,
            "title": p_title,
            "version": "v01",
            "timing_status": "pre_vo_script_clock (built from neurons_script_master_v01.md; retimes onto Scribe STT once VO locks)",
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
        "film": "033_Cajal-Loewi-Neurons-Synapses",
        "version": "v01",
        "date": "2026-10-17",
        "owner": "gemini (J0494)",
        "status": "PRE_VO_BOARDS_V01_NO_MINT",
        "generation_authorized": False,
        "script": "00_Brand/Channel-Setup/ideas/033_Cajal-Loewi-Neurons-Synapses/neurons_script_master_v01.md",
        "sources": "00_Brand/Channel-Setup/ideas/033_Cajal-Loewi-Neurons-Synapses/SOURCES_v01.md",
        "credit_snapshot": {
            "flow_Balance": 23740,
            "flow_floor": 0,
            "flow_read_at": "2026-10-15T21:42:22Z",
            "vertex_promo_gbp": 71.02,
            "vertex_usable_gbp": 70.02,
        },
        "totals": totals,
        "per_part": per_part_summary,
        "mint_order": "006 > 007 > 008 > 009 > 010 > 011 > 012 > 013 > 014 > 015 > 016 > 017 > 018 > 019 > 020 > 021 > 022 > 023 > 024 > 025 > 026 > 027 > 028 > 029 > 030 > 031 > 032 > 033. Nothing in 033 is generation_authorized.",
    }
    (EDIT / "PICTURE_PLAN_v01.json").write_text(json.dumps(plan, indent=2) + "\n")

    sl = [
        "# 033 Neurons & Synapses: The 3 AM Dream That Solved How Brains Work — Shot list & plate boards v01 (pre-VO)",
        "",
        "Gemini, 17 Oct 2026, J0494. Built from `neurons_script_master_v01.md` (93.7 PASS) and `SOURCES_v01.md`.",
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
        "# 033 price review v01 (pre-VO plate boards)",
        "",
        "Gemini, 17 Oct 2026, J0494. Boards only. **No mint. No spend. No merge.**",
        "Prepared from `neurons_script_master_v01.md` (93.7 PASS) and `SOURCES_v01.md` so 033's full plate board rows, non-emissive Fast prompts, £0 code graphics, and Teach-on-Screen overlays are ready to re-time the moment long VO locks. Parked for Chief.",
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
        f"- **Quality ({totals['Quality']} rows):** readable faces (Santiago Ramón y Cajal, Camillo Golgi, Charles Scott Sherrington, Otto Loewi, Henry Hallett Dale, Eunice Newton Foote, John Tyndall), candlelit kitchen microscope scenes, and the 2 Explorer beats.",
        f"- **Fast ({totals['Fast']} rows, non-emissive):** daylight prop and laboratory shots (Cajal's brass microscope & India-ink drawings pan, 3-object callback bench, Golgi's single black pyramidal neuron microscope view, dichromate & silver nitrate dishes, Cajal's one-way arrow drawing, synaptic vesicles releasing messenger molecules across the 20 nm cleft). Zero candles, flames, sparks, or glowing elements on Fast.",
        f"- **£0 code graphics ({totals['code_graphic']} rows):**",
        "  1. `P1:04_86_billion_neurons_20nm_synaptic_cleft_and_acetylcholine_diagram` — 86 billion neurons & ~100 trillion synapses separated by a 20 nm synaptic cleft (5,000× thinner than hair) (`SCALE: a synaptic gap is just 20 nanometres wide — five thousand times thinner than a single human hair, yet wide enough that no two brain cells fuse together`)",
        "  2. `P1:06_human_hair_100000nm_vs_rbc_7500nm_vs_20nm_synaptic_cleft_card` — human hair (100,000 nm) vs red blood cell (7,500 nm) vs synaptic cleft (20–40 nm) (`SCALE: five thousand synaptic gaps laid side by side would barely span the width of one human hair`)",
        "  3. `P2:02_carmine_100_percent_tangle_vs_golgi_1_to_5_percent_black_stain_chart` — 100% carmine dye (unreadable tangled mat) vs Camillo Golgi's 1873 silver chromate 'black reaction' (1%–5% stained black on clear yellow) (`SCALE: by staining only one to five cells out of every hundred, Golgi's silver reaction made single trees visible inside the densest forest in nature`)",
        "  4. `P3:02_cajal_dynamic_polarization_and_1954_electron_microscope_20nm_chart` — Cajal's Law of Dynamic Polarization (dendrites → soma → axon → 20 nm synapse) + 1954 electron microscopy (0.2 nm resolving the 20 nm cleft vs 200 nm light limit) (`SCALE: nineteenth-century light microscopes blurred anything smaller than 200 nanometres — ten times wider than the 20-nanometre synaptic gap, which is why only Cajal's embryonic silver stains and 1950s electron microscopes could prove the gap was real`)",
        "  5. `P4:02_loewi_two_frog_hearts_vagusstoff_kymograph_40_to_12_bpm_diagram` — Otto Loewi's March 1921 two-frog-heart Graz experiment: Heart #1 (~40 → 10–15 bpm) + pipette transfer of Vagusstoff (acetylcholine) slowing nerve-free Heart #2 (`SCALE: a few drops of clear salt water pipetted from one frog heart to another at three in the morning proved that every human thought, memory, and heartbeat relies on microscopic chemical messengers crossing a 20-nanometre gap`)",
        "  6. `P5:01_timeline_1873_1955_and_electrochemical_100ms_20nm_relay_chart` — completed 5-date timeline (1873 → 1955) + electrochemical relay (100 m/s action potential → <1 ms chemical diffusion across 20 nm) (`SCALE: an electrical impulse racing at 100 metres per second converts into a chemical puff that crosses a 20-nanometre gap in less than one millisecond — firing across 100 trillion synapses inside a three-pound brain`)",
        f"- **£0 verified reuse ({totals['reuse']} row):** `P5:04_table_three_callback` uses the 2.40 s unused moving tail `[5.50s..7.90s]` of `P1:07_table_three_props_silver_nitrate_cajal_drawing_frog_heart_chambers`.",
        "",
        "## Mint order",
        "",
        "006 > 007 > 008 > 009 > 010 > 011 > 012 > 013 > 014 > 015 > 016 > 017 > 018 > 019 > 020 > 021 > 022 > 023 > 024 > 025 > 026 > 027 > 028 > 029 > 030 > 031 > 032 > 033. `generation_authorized` is `false` on every row.",
    ])
    (EDIT / "PRICE_REVIEW_v01.md").write_text("\n".join(pr_lines) + "\n")
    print(f"033 v01 boards written: {totals['rows']} rows, Flow expected={totals['flow_credits_expected']}")


if __name__ == "__main__":
    main()
