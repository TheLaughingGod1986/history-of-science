#!/usr/bin/env python3
"""J2476: HOS 013 Darwin & Wallace picture plan v01 on the locked VO (hos_013_vo_v03a.wav).

Builds at £0:
1. 07_Edit-Project/parts/part-01_plates_v01.json .. part-06_plates_v01.json
2. 07_Edit-Project/PICTURE_PLAN_v01.json
3. 07_Edit-Project/PICTURE_PLAN_v01.md
4. 07_Edit-Project/PRICE_REVIEW_v01.md
5. 10_Shorts/SHORTS_PICTURE_PLAN_v01.json

Applies HOS-2026-11-E2 proof-first first 30 seconds (9 cuts <= 4.5s, 0:05-0:15 physical
proof/apparatus, first DATA+SCALE graphic on screen at 0:39.40 <= 0:40.00), splits all
>8.0s rows onto word boundaries so 0 minted Veo clips exceed 8.0s, and maps every row
to its exact source (built £0 code graphic, built £0 public-domain archive composite,
£0 reuse, or parked Flow Veo 3.1 Quality/Fast mint with generation_authorized: false).
"""
from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path

EDIT = Path(__file__).resolve().parent
FILM = EDIT.parent
NAS_EDIT = Path("/Volumes/data/studio-live/History Of Science/02_Video-Projects/013_Darwin-Wallace-Evolution/07_Edit-Project")
WORDS_PATH = FILM / "02_Voiceover/stt/hos_013_vo_v03a/words_fw_small_en.json"
VO_WAV = FILM / "02_Voiceover/hos_013_vo_v03a.wav"
VO_SHA256 = "f8ef433b3b5b5571284e6f12ef339a2b2c0d39eb9978753e86a4d0efeb5e1a03"


def fmt_t(sec: float) -> str:
    m = int(sec // 60)
    s = sec - m * 60
    return f"{m}:{s:05.2f}"


def load_vo_words() -> list[dict]:
    data = json.loads(WORDS_PATH.read_text())
    return data["words"]


# Archive metadata lookup from ARCHIVE_PULLS_RAW_v01.json
ARCHIVE_META = {
    item["id"]: item
    for item in json.loads((EDIT / "archive_pulls_v01/ARCHIVE_PULLS_RAW_v01.json").read_text())
}


# Part metadata
PART_META = {
    1: {
        "title": "Part 01 — The Twenty-Year Secret",
        "chapter_card": None,
        "vo_start_s": 0.00,
        "vo_end_s": 75.50,
    },
    2: {
        "title": "Part 02 — The Birds He Forgot to Label",
        "chapter_card": "The Birds He Forgot to Label",
        "vo_start_s": 75.50,
        "vo_end_s": 171.08,
    },
    3: {
        "title": "Part 03 — The Engine and the Barnacles",
        "chapter_card": "The Engine and the Barnacles",
        "vo_start_s": 171.08,
        "vo_end_s": 276.26,
    },
    4: {
        "title": "Part 04 — Fever in the Islands",
        "chapter_card": "Fever in the Islands",
        "vo_start_s": 276.26,
        "vo_end_s": 366.34,
    },
    5: {
        "title": "Part 05 — The Night Nobody Noticed",
        "chapter_card": "The Night Nobody Noticed",
        "vo_start_s": 366.34,
        "vo_end_s": 448.16,
    },
    6: {
        "title": "Part 06 — The Missing Piece",
        "chapter_card": "The Missing Piece",
        "vo_start_s": 448.16,
        "vo_end_s": 515.00,
    },
}


# All 81 rows across Parts 01-06:
# (part, id, t_in, t_out, set_id, eng, side_label, teach_overlay, who_portrait, archive_id, shot_desc, prompt)
ROWS_SPEC = [
    # === PART 01: The Twenty-Year Secret (0:00.00 - 1:15.50, HOS-2026-11-E2 proof-first open) ===
    (
        1, "01_study_beaks", 0.00, 3.80, "A", "Q", "LOCKED AWAY",
        {"kind": "LABEL", "label": "LOCKED AWAY", "hold_s": 3.0, "sfx": "tick_ink"},
        None, None,
        "Warm candlelit study at Down House: four Galápagos finch specimens with contrasting beaks (heavy nutcracker to thin needle) lie beside an open red-leather notebook showing a small inked branching tree (Answer image by 0:03; Short A frame 0)",
        "Premium Animistry-class 3D cartoon. Down House study in warm candle glow: four Galápagos finch specimens with contrasting beak shapes lie on a mahogany desk beside an open red-leather notebook showing an unlettered inked branching tree sketch. Short A frame 0 and the answer image. No readable words or numbers anywhere. Silent. Continuous motion through the final frame. No Explorer. No Orbit."
    ),
    (
        1, "02_drawer_lock", 3.80, 7.90, "A", "Q", None,
        {"kind": "MILESTONE", "label": "TITLE QUESTION BY 0:07", "note": "Physical proof (0:05-0:15 part 1)"},
        None, None,
        "Darwin's hands close the red-leather notebook, place it inside a mahogany desk drawer, and turn a brass key to lock it shut (Title question by 0:07; HOS-2026-11-E2 physical proof 0:05–0:15)",
        "Premium Animistry-class 3D cartoon. Close on a Victorian naturalist's hands closing the red-leather notebook, sliding it into a mahogany desk drawer, and turning a brass key in the lock under warm study light. No readable words or numbers anywhere. Silent. Continuous motion through the final frame. No Explorer. No Orbit."
    ),
    (
        1, "03a_unlabelled_birds", 7.90, 11.90, "A", "F", None,
        {"kind": "MILESTONE", "label": "PROOF 0:05-0:15", "note": "Physical proof (0:05-0:15 part 2): unlabelled bird skins"},
        None, None,
        "On the wooden study table in grey window light, hands lay down three dark Galápagos finch skins with blank parchment tags tied to their legs (HOS-2026-11-E2 physical proof 0:05–0:15)",
        "Premium Animistry-class 3D cartoon. On a wooden study table in grey window light, a naturalist's hands set down three small dark finch skins with blank unlettered paper tags tied to their legs. Daylight, window light or matte painted ink only. No candle, flame, glow, spark, fireball or lightning. No readable words or numbers anywhere. Silent. Continuous motion through the final frame. No Explorer. No Orbit."
    ),
    (
        1, "03b_malay_packet", 11.90, 16.02, "A", "Q", "ONE LETTER",
        {"kind": "LABEL", "label": "ONE LETTER", "hold_s": 3.2, "sfx": "tick_ink", "note": "Promise by 0:15 + physical proof (0:05-0:15 part 3)"},
        None, None,
        "Beside a glass jar of preserved barnacles and a brass dissecting microscope, a twine-tied foreign paper packet lands on Darwin's desk (Promise by 0:15; HOS-2026-11-E2 physical proof 0:05–0:15)",
        "Premium Animistry-class 3D cartoon. On a Victorian naturalist's mahogany desk beside a glass specimen jar of barnacles and a brass dissecting microscope, a sealed foreign paper packet tied with twine lands in warm study light. No readable words or numbers anywhere. Silent. Continuous motion through the final frame. No Explorer. No Orbit."
    ),
    (
        1, "04a_packet_seal", 16.02, 19.00, "A", "F", None,
        {"kind": "SFX", "sfx": "whoosh_soft"},
        None, None,
        "Close push-in on the red wax seal and brass magnifying glass beside the twine-tied packet in grey window light (HOS-2026-11-E2 cut < 4.5 s)",
        "Premium Animistry-class 3D cartoon. Slow push-in on a red wax seal and a brass magnifying glass resting beside a twine-tied paper packet on a wooden desk in grey window light. Daylight, window light or matte painted ink only. No candle, flame, glow, spark, fireball or lightning. No readable words or numbers anywhere. Silent. Continuous motion through the final frame. No Explorer. No Orbit."
    ),
    (
        1, "04b_drawer_unlock", 19.00, 21.64, "A", "F", None,
        None,
        None, None,
        "Close on a hand turning the brass key in the mahogany desk drawer and sliding the locked red-leather notebook back into the open in grey window light (HOS-2026-11-E2 cut < 4.5 s)",
        "Premium Animistry-class 3D cartoon. Close on a hand turning a brass key in a mahogany desk drawer and sliding the closed red-leather notebook out into grey window light. Daylight, window light or matte painted ink only. No candle, flame, glow, spark, fireball or lightning. No readable words or numbers anywhere. Silent. Continuous motion through the final frame. No Explorer. No Orbit."
    ),
    (
        1, "05a_museum_cases", 21.64, 25.64, "B", "Q", "LONDON · 1830S",
        {"kind": "WHEN", "label": "LONDON · 1830S", "hold_s": 3.4, "sfx": "tick_ink", "note": "Stakes by 0:25"},
        None, None,
        "Wood-panelled London museum hall: rows of tall glass cases hold animal skeletons under blank brass plaques (Stakes by 0:25; HOS-2026-11-E2 cut <= 4.5 s)",
        "Premium Animistry-class 3D cartoon. A wood-panelled Victorian museum hall in London, 1830s: tall locked glass cases hold animal skeletons under blank brass plaques as dust motes drift in high window shafts. No readable words or numbers anywhere. Silent. Continuous motion through the final frame. No Explorer. No Orbit."
    ),
    (
        1, "05b_museum_plaques", 25.64, 29.22, "B", "F", None,
        None,
        None, None,
        "Close tracking shot along a locked glass museum case of preserved birds and skeletons in grey window light, brass lock bolts fixed shut (HOS-2026-11-E2 cut < 4.5 s)",
        "Premium Animistry-class 3D cartoon. Close tracking shot along a locked glass museum case of preserved bird and reptile specimens in grey window light, brass lock bolts fixed shut. Daylight, window light or matte painted ink only. No candle, flame, glow, spark, fireball or lightning. No readable words or numbers anywhere. Silent. Continuous motion through the final frame. No Explorer. No Orbit."
    ),
    (
        1, "06_padlock_shut", 29.22, 33.44, "A", "F", "FIXED FOREVER?",
        {"kind": "LABEL", "label": "FIXED FOREVER?", "hold_s": 3.4, "sfx": "tick_ink"},
        None, None,
        "Close-up in grey window light: a heavy iron padlock clicks shut on a wooden specimen box (9th moving plate overlapping 0:00–0:30, cut 4.22 s <= 4.5 s)",
        "Premium Animistry-class 3D cartoon. Close-up in grey window light: a heavy iron padlock clicks shut on a wooden specimen chest. Daylight, window light or matte painted ink only. No candle, flame, glow, spark, fireball or lightning. No readable words or numbers anywhere. Silent. Continuous motion through the final frame. No Explorer. No Orbit."
    ),
    (
        1, "07_darwin_1837_desk", 33.44, 39.40, "A", "Q", "JULY 1837",
        {
            "kind": "WHO",
            "line_1": "Charles Darwin",
            "line_2": "(1809–1882) — naturalist",
            "when_stamp": "JULY 1837",
            "timeline_step": "2/7 · July 1837 (Notebook B)",
            "hold_s": 3.8,
            "sfx": "tick_ink"
        },
        "who_charles_darwin", None,
        "Summer 1837: 28-year-old Charles Darwin (clean-shaven with sideburns, dark coat) dips a steel pen at his study desk (First real fact before 0:45)",
        "Premium Animistry-class 3D cartoon. Summer 1837: a 28-year-old English naturalist, clean-shaven with dark sideburns and a dark frock coat, dips a steel pen in an inkwell at his study desk by warm lamplight. No readable words or numbers anywhere. Silent. Continuous motion through the final frame. No Explorer. No Orbit."
    ),
    (
        1, "08_cg_i_think_tree", 39.40, 54.30, "G", "CG", "TWENTY YEARS IN A DRAWER",
        {
            "kind": "DATA",
            "label": "TWENTY YEARS IN A DRAWER",
            "detail": "\"I think\" tree (Notebook B p. 36) + 20-year secrecy bar (1838 → 1858)",
            "scale": "20 years in a drawer — longer than a child takes to grow up",
            "hold_s": 3.6,
            "sfx": "tick_ink",
            "note": "HOS-2026-11-E2 Early DATA+SCALE graphic on screen at 0:39.40 (inside 0:25-0:40)"
        },
        None, "darwin_tree_1837",
        "Code graphic #1 (starts at 0:39.40 inside 0:25–0:40 HOS-2026-11-E2 window): scanned trace of Darwin's 1837 Notebook B p. 36 branching tree drawing itself in candle-gold ink beneath \"I think\", then a 20-year secrecy bar filling from 1838 to 1858",
        "Own £0 code graphic (code_graphic_013_p1_08_cg_i_think_tree.mp4) incorporating public-domain Cambridge MS DAR 121:36 scan: Notebook B p. 36 branching tree traces in gold ink, then 20-year bar fills 1838 → 1858."
    ),
    (
        1, "09_wallace_hut_split", 54.30, 62.08, "A/D", "Q", "JUNE 1858",
        {
            "kind": "WHO",
            "line_1": "Alfred Russel Wallace",
            "line_2": "(1823–1913) — naturalist",
            "when_stamp": "JUNE 1858",
            "timeline_step": "5/7 · June 1858 (Wallace letter)",
            "hold_s": 3.8,
            "sfx": "tick_ink"
        },
        "who_alfred_russel_wallace", None,
        "Split scene: on the left, bearded Darwin (aged 49) reads handwritten pages in his Kent study; on the right, Alfred Russel Wallace (aged 35, bearded, round glasses) writes by oil lamp in a rain-lashed bamboo hut",
        "Premium Animistry-class 3D cartoon. Split composition: on the left, a 49-year-old bearded English naturalist in his Kent study reads a foreign manuscript; on the right, a 35-year-old bearded field naturalist wearing round wire-rimmed spectacles writes by oil lamp in a rain-lashed bamboo hut. No readable words or numbers anywhere. Silent. Continuous motion through the final frame. No Explorer. No Orbit."
    ),
    (
        1, "10_cg_globe_arc", 62.08, 67.68, "G", "CG", "OTHER SIDE OF WORLD",
        {
            "kind": "DATA",
            "label": "OTHER SIDE OF WORLD",
            "detail": "Inked globe arc from Malay Archipelago to Kent + 230-page 1844 essay vs short 1858 paper",
            "scale": "the other side of the world",
            "hold_s": 3.6,
            "sfx": "tick_ink"
        },
        None, None,
        "Code graphic #2: inked globe arc sweeping from the Malay Archipelago to Down House, Kent, with Darwin's 230-page 1844 essay stack beside Wallace's short 1858 paper",
        "Own £0 code graphic (code_graphic_013_p1_10_cg_globe_arc.mp4): inked world map arc from Malay Archipelago to Kent beside 230-page stack vs 20-page essay."
    ),
    (
        1, "11_beagle_cabin_explorer", 67.68, 75.50, "C", "Q", None,
        {"kind": "EXPLORER", "beat": 1, "note": "Outside first minute (1:07.68)"},
        None, None,
        "HMS Beagle chart cabin rocks gently; unlabelled bird skins slide beside a brass compass as the Explorer (1st beat, outside first minute) peers over the chart table at a giant tortoise shell",
        "Premium Animistry-class 3D cartoon. Inside the timber chart cabin of HMS Beagle, unlabelled dark bird skins rest beside a brass compass as the Explorer peers curiously over the chart table at a giant tortoise shell. Exactly one Explorer, on model: round gold glasses, teal long coat, finished hair. No readable words or numbers anywhere. Silent. Continuous motion through the final frame. No Orbit."
    ),

    # === PART 02: The Birds He Forgot to Label (1:15.50 - 2:51.08) ===
    (
        2, "01_card_p02", 75.50, 77.00, "A", "CG", "THE BIRDS HE FORGOT",
        {"kind": "CHAPTER", "chapter": 2, "title": "The Birds He Forgot to Label", "sfx": "rumble_low"},
        None, None,
        "3D case-file desk chapter card: The Birds He Forgot to Label",
        "Own £0 chapter card graphic (code_graphic_013_p2_01_card_p02.mp4): case-file desk chapter card II."
    ),
    (
        2, "02_galapagos_beach_myth", 77.00, 84.22, "C", "Q", None,
        None,
        None, None,
        "Sunlit Galápagos black lava beach with surf and cactus; young Darwin (aged 26, wide-brimmed hat) walks past shore birds without looking up",
        "Premium Animistry-class 3D cartoon. Sunlit Galápagos black volcanic lava beach with white surf and prickly-pear cactus: a 26-year-old English naturalist in a wide-brimmed hat walks past dark finches on the rocks without looking down. No readable words or numbers anywhere. Silent. Continuous motion through the final frame. No Explorer. No Orbit."
    ),
    (
        2, "03_unlabelled_bagging", 84.22, 92.18, "C", "Q", "NO LABELS",
        {
            "kind": "WHEN",
            "label": "GALÁPAGOS · SEPTEMBER 1835",
            "side_label": "NO LABELS",
            "timeline_step": "1/7 · Sept 1835 (Galápagos)",
            "hold_s": 3.6,
            "sfx": "tick_ink"
        },
        None, None,
        "Young Darwin places small dark bird skins into a canvas collecting bag on the lava rocks, tying blank paper tags with no island written on them",
        "Premium Animistry-class 3D cartoon. Galápagos shore, September 1835: a 26-year-old English naturalist places small dark bird skins into a canvas collecting bag on black lava rock, tying blank paper tags with no writing on them. No readable words or numbers anywhere. Silent. Continuous motion through the final frame. No Explorer. No Orbit."
    ),
    (
        2, "04_blank_tags_row", 92.18, 97.40, "C", "F", "FORGOT TO LABEL FINCHES",
        {"kind": "FACT", "label": "FORGOT TO LABEL FINCHES", "hold_s": 3.5, "sfx": "tick_ink"},
        None, None,
        "Close-up on the Beagle cabin table in daylight: three dark bird skins (blackbird-like, wren-like, finch-like) with blank parchment tags fluttering in the sea breeze",
        "Premium Animistry-class 3D cartoon. Close-up on a wooden cabin table in daylight: three small dark bird skins lie in a row with blank unlettered parchment tags fluttering gently. Daylight, window light or matte painted ink only. No candle, flame, glow, spark, fireball or lightning. No readable words or numbers anywhere. Silent. Continuous motion through the final frame. No Explorer. No Orbit."
    ),
    (
        2, "05_tortoise_overboard", 97.40, 104.56, "C", "Q", None,
        None,
        None, None,
        "Beagle timber deck at sea: sailors stack giant domed tortoise shells; one crewman tips an empty shell over the wooden rail into the waves",
        "Premium Animistry-class 3D cartoon. On the sunlit timber deck of HMS Beagle at sea, sailors stack giant tortoise shells; one sailor tips an empty shell over the rail into the blue ocean swell. No readable words or numbers anywhere. Silent. Continuous motion through the final frame. No Explorer. No Orbit."
    ),
    (
        2, "06a_lawson_jetty", 104.56, 110.00, "C", "Q", None,
        {
            "kind": "WHO",
            "line_1": "Nicholas Lawson",
            "line_2": "Galápagos vice-governor",
            "hold_s": 3.6,
            "sfx": "tick_ink"
        },
        None, None,
        "On a stone jetty in the Galápagos, vice-governor Nicholas Lawson speaks to young Darwin beside two giant tortoise shells",
        "Premium Animistry-class 3D cartoon. On a stone jetty in the Galápagos Islands, the islands' vice-governor gestures toward two giant tortoise shells while a 26-year-old English naturalist listens intently. No readable words or numbers anywhere. Silent. Continuous motion through the final frame. No Explorer. No Orbit."
    ),
    (
        2, "06b_cg_tortoise_shells", 110.00, 114.86, "G", "CG", "ONE SHELL PER ISLAND",
        {"kind": "EXPLAINER", "label": "ONE SHELL PER ISLAND", "hold_s": 3.5, "sfx": "tick_ink"},
        None, None,
        "Inked anatomical explainer diagram on period paper: side-by-side profile of a dome-shelled tortoise and a high saddle-backed tortoise front arch matched to different islands",
        "Own £0 code graphic (code_graphic_013_p2_06b_cg_tortoise_shells.mp4): inked side-by-side dome shell vs saddle-backed shell arch diagram."
    ),
    (
        2, "07_darwin_notebook_wait", 114.86, 120.88, "C", "Q", None,
        None,
        None, None,
        "Young Darwin leans on the Beagle's stern rail at dusk as the volcanic islands recede on the horizon",
        "Premium Animistry-class 3D cartoon. A young 26-year-old English naturalist leans on the wooden stern rail of HMS Beagle at dusk as volcanic islands recede across the ocean horizon. No readable words or numbers anywhere. Silent. Continuous motion through the final frame. No Explorer. No Orbit."
    ),
    (
        2, "08a_gould_sorting", 120.88, 127.10, "B", "Q", "LONDON · 1837",
        {
            "kind": "WHO",
            "line_1": "John Gould",
            "line_2": "(1804–1881) — bird expert",
            "when_stamp": "LONDON · 1837",
            "hold_s": 3.8,
            "sfx": "tick_ink"
        },
        "who_john_gould", None,
        "London, 1837: ornithologist John Gould stands at a long mahogany table examining Darwin's bird skins and looking up in surprise",
        "Premium Animistry-class 3D cartoon. London, 1837: a museum ornithologist stands at a long mahogany museum table examining a collection of Galápagos bird skins and looking up in surprise. No readable words or numbers anywhere. Silent. Continuous motion through the final frame. No Explorer. No Orbit."
    ),
    (
        2, "08b_gould_skins_closeup", 127.10, 131.40, "B", "F", None,
        None,
        None, None,
        "Close dolly in grey window light across the row of Galápagos finch skins laid out by beak depth on Gould's mahogany table",
        "Premium Animistry-class 3D cartoon. Close tracking shot in grey window light across a neat row of Galápagos finch skins arranged from heavy stout beak to slender probing beak on a mahogany table. Daylight, window light or matte painted ink only. No candle, flame, glow, spark, fireball or lightning. No readable words or numbers anywhere. Silent. Continuous motion through the final frame. No Explorer. No Orbit."
    ),
    (
        2, "09_cg_finch_toolbox", 131.40, 143.72, "G", "CG", "WHOLE TOOLBOX OF BEAKS",
        {
            "kind": "DATA",
            "label": "WHOLE TOOLBOX OF BEAKS",
            "detail": "Inked chart of 4 Galápagos finch beak profiles (with Gould 1845 lithograph inset) grouped by tool shape",
            "scale": "one family of birds, a whole toolbox of beaks",
            "hold_s": 3.6,
            "sfx": "tick_ink"
        },
        None, "gould_finches_1845",
        "Code graphic #3: inked anatomical chart on period paper (with Gould's 1845 Darwin's finches lithograph) grouping the finch beaks next to four matching tools — heavy nutcracker, stout pliers, fine tweezers, and long probe",
        "Own £0 code graphic (code_graphic_013_p2_09_cg_finch_toolbox.mp4) incorporating public-domain Gould 1845 lithograph: four beak profiles matched to nutcracker, pliers, tweezers, and probe."
    ),
    (
        2, "10a_explorer_shipmates", 143.72, 149.90, "C", "Q", None,
        {"kind": "EXPLORER", "beat": 2, "note": "Outside first minute (2:23.72)"},
        None, None,
        "The Explorer (2nd beat) on the Beagle's deck turns a Darwin bird skin over looking for an island label, finds it blank, shrugs at the camera, then points to a shipmate's neatly tagged specimen",
        "Premium Animistry-class 3D cartoon. On the sunlit deck of HMS Beagle, the Explorer turns a bird skin tag over, finds it blank, shrugs gently, and points to a shipmate's neatly tagged specimen tray. Exactly one Explorer, on model: round gold glasses, teal long coat, finished hair. No readable words or numbers anywhere. Silent. Continuous motion through the final frame. No Orbit."
    ),
    (
        2, "10b_shipmate_tagged_tray", 149.90, 153.20, "C", "F", None,
        None,
        None, None,
        "Close on two neatly tagged shipmates' bird skins beside a brass dividers and island chart on the cabin table in daylight",
        "Premium Animistry-class 3D cartoon. Close on two neatly tagged bird specimens resting beside brass dividers on a wooden chart table in daylight. Daylight, window light or matte painted ink only. No candle, flame, glow, spark, fireball or lightning. No readable words or numbers anywhere. Silent. Continuous motion through the final frame. No Explorer. No Orbit."
    ),
    (
        2, "11_island_split_vision", 153.20, 161.20, "C", "Q", None,
        {"kind": "SFX", "sfx": "whoosh_soft"},
        None, None,
        "Aerial sweep over three volcanic Galápagos islands separated by blue ocean currents, each island highlighting a different seed or cactus flower",
        "Premium Animistry-class 3D cartoon. Sweeping aerial view over three volcanic Galápagos islands separated by deep blue ocean currents in warm sunlight. No readable words or numbers anywhere. Silent. Continuous motion through the final frame. No Explorer. No Orbit."
    ),
    (
        2, "12a_arch_notebook_tree_zoom", 161.20, 166.60, "A/G", "ARCH", None,
        {"kind": "ARCHIVE", "credit": "Cambridge Univ. Library MS DAR 121:36 (PD)"},
        None, "darwin_tree_1837",
        "Free archive composite: Cambridge University Library MS DAR 121:36 (Notebook B p. 36, Public Domain) on a 3D desk surface as animated gold ink traces the single ancestral trunk splitting into multiple branches",
        "Own £0 archive composite (code_graphic_013_p2_12a_arch_notebook_tree_zoom.mp4): public-domain MS DAR 121:36 scan on period desk with animated gold branch highlights and credit line."
    ),
    (
        2, "12b_tree_question", 166.60, 171.08, "A", "Q", None,
        None,
        None, None,
        "Back in the candlelit London study, Darwin gazes at the inked branching tree in Notebook B, tapping his pen tip against the blank space beside the branches",
        "Premium Animistry-class 3D cartoon. In a warm candlelit London study, a young English naturalist gazes at his open red-leather notebook, tapping his steel pen thoughtfully beside the sketched branches. No readable words or numbers anywhere. Silent. Continuous motion through the final frame. No Explorer. No Orbit."
    ),

    # === PART 03: The Engine and the Barnacles (2:51.08 - 4:36.26) ===
    (
        3, "01_card_p03", 171.08, 172.58, "A", "CG", "ENGINE AND BARNACLES",
        {"kind": "CHAPTER", "chapter": 3, "title": "The Engine and the Barnacles", "sfx": "rumble_low"},
        None, None,
        "3D case-file desk chapter card: The Engine and the Barnacles",
        "Own £0 chapter card graphic (code_graphic_013_p3_01_card_p03.mp4): case-file desk chapter card III."
    ),
    (
        3, "02a_malthus_lamplight", 172.58, 178.80, "A", "Q", "28 SEPTEMBER 1838",
        {
            "kind": "WHO",
            "line_1": "Thomas Malthus",
            "line_2": "(1766–1834) — economist",
            "when_stamp": "28 SEPTEMBER 1838",
            "timeline_step": "3/7 · Sept 1838 (Malthus read)",
            "hold_s": 3.8,
            "sfx": "tick_ink"
        },
        "who_thomas_malthus", None,
        "London, 28 September 1838: Darwin reads Malthus's open octavo book by oil lamp",
        "Premium Animistry-class 3D cartoon. London study, 28 September 1838: a young English naturalist reads an open octavo book by warm oil lamp light. No readable words or numbers anywhere. Silent. Continuous motion through the final frame. No Explorer. No Orbit."
    ),
    (
        3, "02b_notebook_d_open", 178.80, 182.70, "A", "Q", "THE MISSING PIECE",
        {"kind": "LABEL", "label": "THE MISSING PIECE", "hold_s": 3.2, "sfx": "tick_ink"},
        None, None,
        "Darwin's eyes widen by lamplight as he pulls Notebook D toward him and opens a fresh page",
        "Premium Animistry-class 3D cartoon. By warm oil lamp light, a young English naturalist's eyes widen with realization as he pulls a leather notebook toward him across the desk. No readable words or numbers anywhere. Silent. Continuous motion through the final frame. No Explorer. No Orbit."
    ),
    (
        3, "03_cg_malthus_curve", 182.70, 192.10, "G", "CG", "MOST NEVER SURVIVE",
        {
            "kind": "DATA",
            "label": "MOST NEVER SURVIVE",
            "detail": "Inked exponential curve (offspring born) vs flat horizontal line (food supply)",
            "scale": "far more born than can ever live",
            "hold_s": 3.6,
            "sfx": "tick_ink"
        },
        None, None,
        "Code graphic #4a: inked curve climbing steeply on period paper (offspring born) while a flat horizontal line stays low (food available); the gap fills with faded bird silhouettes",
        "Own £0 code graphic (code_graphic_013_p3_03_cg_malthus_curve.mp4): Malthusian exponential birth curve vs linear food line on period parchment."
    ),
    (
        3, "04a_drought_island_seeds", 192.10, 197.30, "C", "F", None,
        None,
        None, None,
        "Sun-baked Galápagos island in a drought year in daylight: cracked dry earth with only large, thick-shelled woody seeds left on the ground",
        "Premium Animistry-class 3D cartoon. Sun-baked Galápagos earth in daylight: cracked dry soil scattered with large, thick-shelled woody seeds under a pale dry sky. Daylight, window light or matte painted ink only. No candle, flame, glow, spark, fireball or lightning. No readable words or numbers anywhere. Silent. Continuous motion through the final frame. No Explorer. No Orbit."
    ),
    (
        3, "04b_finch_cracks_seed", 197.30, 201.96, "C", "Q", None,
        None,
        None, None,
        "A deep-beaked Galápagos finch cracks open a thick woody seed on the dry ground",
        "Premium Animistry-class 3D cartoon. On dry Galápagos volcanic ground, a finch with a deep stout beak cracks open a hard woody seed. No readable words or numbers anywhere. Silent. Continuous motion through the final frame. No Explorer. No Orbit."
    ),
    (
        3, "05a_chicks_deep_beaks", 201.96, 206.50, "C", "Q", None,
        None,
        None, None,
        "In a cactus nest, the deep-beaked parent feeds chicks whose beaks are visibly deep like the parent's",
        "Premium Animistry-class 3D cartoon. In a Galápagos cactus nest, a deep-beaked parent finch feeds chicks whose beaks are stout and deep like the parent's. No readable words or numbers anywhere. Silent. Continuous motion through the final frame. No Explorer. No Orbit."
    ),
    (
        3, "05b_finches_next_generation", 206.50, 211.76, "C", "Q", None,
        None,
        None, None,
        "Across sunlit Galápagos cactus branches, a thriving flock of deep-beaked finches perches and feeds in the next generation",
        "Premium Animistry-class 3D cartoon. Sunlit Galápagos cactus branches where a thriving flock of deep-beaked finches perches and cracks seeds across the island. No readable words or numbers anywhere. Silent. Continuous motion through the final frame. No Explorer. No Orbit."
    ),
    (
        3, "06_nature_keeps_fit", 211.76, 219.32, "G", "CG", "NATURAL SELECTION",
        {"kind": "EXPLAINER", "label": "NATURAL SELECTION", "hold_s": 3.6, "sfx": "tick_ink"},
        None, None,
        "Inked diagram on period paper: three beak profiles pass through a natural sieve of hard drought seeds, leaving the deepest beak gleaming in gold ink",
        "Own £0 code graphic (code_graphic_013_p3_06_nature_keeps_fit.mp4): inked natural-selection sieve diagram selecting the deep beak profile."
    ),
    (
        3, "07a_darwin_afraid_window", 219.32, 223.90, "A", "Q", None,
        None,
        None, None,
        "Down House study at night, January 1844: Darwin pauses by the study window with a troubled expression",
        "Premium Animistry-class 3D cartoon. Down House study at night, January 1844: an English naturalist in his mid-thirties pauses beside the darkened window with a troubled, hesitant expression. No readable words or numbers anywhere. Silent. Continuous motion through the final frame. No Explorer. No Orbit."
    ),
    (
        3, "07b_confessing_murder_letter", 223.90, 229.34, "A", "F", "CONFESSING A MURDER",
        {"kind": "LABEL", "label": "CONFESSING A MURDER", "hold_s": 3.6, "sfx": "tick_ink"},
        None, None,
        "Close in grey window light on Darwin's hand writing a letter to Joseph Hooker with a steel pen, pausing in hesitation",
        "Premium Animistry-class 3D cartoon. Close in grey window light on a man's hand writing a letter with a steel pen on cream paper, pausing in hesitation. Daylight, window light or matte painted ink only. No candle, flame, glow, spark, fireball or lightning. No readable words or numbers anywhere. Silent. Continuous motion through the final frame. No Explorer. No Orbit."
    ),
    (
        3, "08_emma_study", 229.34, 234.20, "A", "Q", None,
        {
            "kind": "WHO",
            "line_1": "Emma Darwin",
            "line_2": "(1808–1896) — Darwin's wife",
            "hold_s": 3.6,
            "sfx": "tick_ink"
        },
        "who_emma_darwin", None,
        "Through the half-open parlour doorway, Emma Darwin sits by lamplight with an open prayer book; Charles watches quietly with affection and worry",
        "Premium Animistry-class 3D cartoon. Through a half-open Victorian parlour doorway, a Victorian wife sits peacefully by warm lamplight while her husband watches quietly from the study. No readable words or numbers anywhere. Silent. Continuous motion through the final frame. No Explorer. No Orbit."
    ),
    (
        3, "09a_essay_1844_sealed", 234.20, 240.64, "A", "F", "JULY 1844",
        {
            "kind": "WHEN",
            "label": "JULY 1844",
            "timeline_step": "4/7 · July 1844 (230-page essay)",
            "hold_s": 3.5,
            "sfx": "tick_ink"
        },
        None, None,
        "July 1844 (before Vestiges, J0307 fix #1): in grey window light, Darwin's hands tie a thick 230-page fair-copy manuscript with red tape",
        "Premium Animistry-class 3D cartoon. Close in grey window light on hands tying a thick 230-page handwritten manuscript stack with red ribbon on a mahogany desk. Daylight, window light or matte painted ink only. No candle, flame, glow, spark, fireball or lightning. No readable words or numbers anywhere. Silent. Continuous motion through the final frame. No Explorer. No Orbit."
    ),
    (
        3, "09b_emma_letter_cupboard", 240.64, 246.00, "A", "Q", "230 PAGES · IF I DIE",
        {"kind": "LABEL", "label": "230 PAGES · IF I DIE", "hold_s": 3.5, "sfx": "tick_ink"},
        None, None,
        "Darwin places a sealed covering letter to Emma beside the 230-page manuscript inside the study cupboard and locks the door",
        "Premium Animistry-class 3D cartoon. In his Down House study, an English naturalist places a wax-sealed letter beside the thick bound manuscript inside a wooden cupboard and turns the key. No readable words or numbers anywhere. Silent. Continuous motion through the final frame. No Explorer. No Orbit."
    ),
    (
        3, "10a_arch_vestiges_1844", 246.00, 250.20, "B/G", "ARCH", "OCTOBER 1844",
        {"kind": "ARCHIVE", "label": "OCTOBER 1844", "credit": "Chambers, Vestiges 1st ed. (Oct 1844, PD)"},
        None, "vestiges_1844_title",
        "Free archive composite (chronology lock: Oct 1844 after July 1844 essay): 1st edition title page of Vestiges of the Natural History of Creation (Public Domain) on a Victorian reading table with animated ink stamp",
        "Own £0 archive composite (code_graphic_013_p3_10a_arch_vestiges_1844.mp4): public-domain Vestiges 1844 title page on period reading desk with October 1844 stamp and credit line."
    ),
    (
        3, "10b_vestiges_torn_apart", 250.20, 254.76, "B", "Q", None,
        None,
        None, None,
        "October 1844: in a Victorian reading room, stern naturalists slam critical reviews down onto the anonymous octavo volume",
        "Premium Animistry-class 3D cartoon. In a Victorian wood-panelled reading room in autumn 1844, stern gentlemen in dark frock coats slam critical pamphlets down beside an octavo book. No readable words or numbers anywhere. Silent. Continuous motion through the final frame. No Explorer. No Orbit."
    ),
    (
        3, "11_barnacles_microscope", 254.76, 261.50, "A", "Q", "EIGHT YEARS ON BARNACLES",
        {
            "kind": "FACT",
            "label": "EIGHT YEARS ON BARNACLES",
            "when_stamp": "1846–1854",
            "hold_s": 3.6,
            "sfx": "tick_ink"
        },
        None, None,
        "Down House study table crowded with dozens of glass jars of preserved barnacles; Darwin bends over a brass dissecting microscope",
        "Premium Animistry-class 3D cartoon. Down House study table crowded with glass specimen jars of marine barnacles as an English naturalist bends closely over a brass dissecting microscope. No readable words or numbers anywhere. Silent. Continuous motion through the final frame. No Explorer. No Orbit."
    ),
    (
        3, "12_cg_barnacle_counter", 261.50, 267.48, "A/G", "CG", "EIGHT YEARS AT MICROSCOPE",
        {
            "kind": "DATA",
            "label": "EIGHT YEARS AT MICROSCOPE",
            "detail": "Eight-year barnacle counter ticking from 1846 to 1854 beside four monograph volumes",
            "scale": "eight years at one microscope",
            "hold_s": 3.6,
            "sfx": "tick_ink"
        },
        None, None,
        "Code graphic #4b: brass-and-ink year counter ticking from 1846 to 1854 beside four monograph volumes and dissecting microscope silhouette",
        "Own £0 code graphic (code_graphic_013_p3_12_cg_barnacle_counter.mp4): 1846 → 1854 eight-year barnacle counter and 4 monograph volumes."
    ),
    (
        3, "13a_lyell_warning", 267.48, 273.10, "A", "F", None,
        None,
        None, None,
        "At Down House in grey window light, a visiting geologist gestures urgently toward Darwin's locked manuscript cupboard",
        "Premium Animistry-class 3D cartoon. In a sunlit study at Down House, a visiting gentleman geologist gestures urgently toward a locked wooden manuscript cupboard. Daylight, window light or matte painted ink only. No candle, flame, glow, spark, fireball or lightning. No readable words or numbers anywhere. Silent. Continuous motion through the final frame. No Explorer. No Orbit."
    ),
    (
        3, "13b_brass_globe_turn", 273.10, 276.26, "A", "F", None,
        None,
        None, None,
        "Close on a brass desktop globe in grey window light spinning toward the islands of the Malay Archipelago",
        "Premium Animistry-class 3D cartoon. Close on a period brass-mounted desktop globe in grey window light spinning smoothly toward the islands of Southeast Asia. Daylight, window light or matte painted ink only. No candle, flame, glow, spark, fireball or lightning. No readable words or numbers anywhere. Silent. Continuous motion through the final frame. No Explorer. No Orbit."
    ),

    # === PART 04: Fever in the Islands (4:36.26 - 6:06.34) ===
    (
        4, "01_card_p04", 276.26, 277.76, "A", "CG", "FEVER IN THE ISLANDS",
        {"kind": "CHAPTER", "chapter": 4, "title": "Fever in the Islands", "sfx": "rumble_low"},
        None, None,
        "3D case-file desk chapter card: Fever in the Islands",
        "Own £0 chapter card graphic (code_graphic_013_p4_01_card_p04.mp4): case-file desk chapter card IV."
    ),
    (
        4, "02_wallace_collector", 277.76, 283.70, "D", "Q", None,
        None,
        None, None,
        "Alfred Russel Wallace (aged 29, bearded, simple cotton shirt, round spectacles) packs wooden crates of pinned Amazon beetles and bird skins on a river dock",
        "Premium Animistry-class 3D cartoon. A bearded naturalist in his late twenties wearing round wire-rimmed spectacles and a simple cotton field shirt packs wooden crates of pinned beetles on a river dock. No readable words or numbers anywhere. Silent. Continuous motion through the final frame. No Explorer. No Orbit."
    ),
    (
        4, "03a_helen_burning", 283.70, 289.90, "D", "Q", "AUGUST 1852",
        {"kind": "WHEN", "label": "AUGUST 1852", "hold_s": 3.5, "sfx": "rumble_low"},
        None, None,
        "August 1852, open Atlantic at night: the sailing ship Helen burns on the dark water as smoke billows into the sky",
        "Premium Animistry-class 3D cartoon. Open Atlantic Ocean at night, August 1852: the wooden brig Helen burns on the dark waves as orange firelight reflects on the swell. No readable words or numbers anywhere. Silent. Continuous motion through the final frame. No Explorer. No Orbit."
    ),
    (
        4, "03b_crates_sinking", 289.90, 292.88, "D", "Q", "HIS COLLECTION SANK",
        {"kind": "FACT", "label": "HIS COLLECTION SANK", "hold_s": 2.6, "sfx": "tick_ink"},
        None, None,
        "Wooden specimen crates slip beneath the dark Atlantic waves as firelight fades on the water",
        "Premium Animistry-class 3D cartoon. Dark Atlantic water at night as wooden specimen crates sink beneath the waves. No readable words or numbers anywhere. Silent. Continuous motion through the final frame. No Explorer. No Orbit."
    ),
    (
        4, "04_open_boat_ten_days", 292.88, 298.12, "D", "Q", None,
        None,
        None, None,
        "Dawn on the open Atlantic: Wallace sits huddled with survivors in a small wooden ship's boat tossing on the swell, watching the horizon",
        "Premium Animistry-class 3D cartoon. Dawn on the open Atlantic: a bearded naturalist in round spectacles sits huddled with sailors in a small wooden open boat tossing on the ocean swell. No readable words or numbers anywhere. Silent. Continuous motion through the final frame. No Explorer. No Orbit."
    ),
    (
        4, "05_cg_wallace_counter", 298.12, 308.62, "D/G", "CG", "125,660 SPECIMENS",
        {
            "kind": "DATA",
            "label": "125,660 SPECIMENS",
            "when_stamp": "MALAY ARCHIPELAGO · 1854–1862",
            "detail": "Painted map of the Malay Archipelago with Wallace's specimen counter climbing 0 → 125,660",
            "scale": "a whole museum, collected by one man",
            "hold_s": 3.6,
            "sfx": "tick_ink"
        },
        None, None,
        "Code graphic #4c: painted map of the Malay Archipelago (1854–1862) with an inked specimen counter climbing from 0 to 125,660",
        "Own £0 code graphic (code_graphic_013_p4_05_cg_wallace_counter.mp4): Malay Archipelago map + 0 → 125,660 specimen counter."
    ),
    (
        4, "06a_wallace_fever", 308.62, 315.30, "D", "Q", "FEBRUARY 1858",
        {"kind": "WHEN", "label": "FEBRUARY 1858", "hold_s": 3.5, "sfx": "tick_ink"},
        None, None,
        "Night, February 1858: in a rain-lashed bamboo hut, Wallace (aged 35, mid-thirties, bearded) lies shivering under a blanket with malarial fever by oil lamp",
        "Premium Animistry-class 3D cartoon. Night, February 1858, in a rain-lashed bamboo hut: a 35-year-old bearded field naturalist lies shivering under a blanket with fever by warm oil lamp light. No readable words or numbers anywhere. Silent. Continuous motion through the final frame. No Explorer. No Orbit."
    ),
    (
        4, "06b_arch_malthus_1798", 315.30, 321.36, "D/G", "ARCH", "THE SAME IDEA",
        {"kind": "ARCHIVE", "label": "THE SAME IDEA", "credit": "Malthus, Principle of Population (1798, PD)", "hold_s": 3.5, "sfx": "tick_ink"},
        None, "malthus_1798_title",
        "Free archive composite: Malthus's 1798 An Essay on the Principle of Population title page (Public Domain) glowing over the bamboo desk surface with animated gold ink highlight (\"the ones that fit survive\")",
        "Own £0 archive composite (code_graphic_013_p4_06b_arch_malthus_1798.mp4): public-domain Malthus 1798 title page composite with animated ink highlight and credit line."
    ),
    (
        4, "07a_wallace_writes_hut", 321.36, 326.00, "D", "Q", None,
        None,
        None, None,
        "Wallace (aged 35) sits up by oil lamp in the bamboo hut and writes rapidly on thin paper sheets",
        "Premium Animistry-class 3D cartoon. Inside the bamboo hut by oil lamp light, a 35-year-old bearded field naturalist in round wire-rimmed spectacles sits up at a wooden table and writes rapidly on thin paper sheets. No readable words or numbers anywhere. Silent. Continuous motion through the final frame. No Explorer. No Orbit."
    ),
    (
        4, "07b_packet_to_mailbag", 326.00, 330.68, "D", "F", None,
        None,
        None, None,
        "In daylight on a tropical jetty, hands tie the twine-wrapped paper packet and place it into a canvas mail steamer bag",
        "Premium Animistry-class 3D cartoon. In daylight on a wooden jetty, hands tie a twine-wrapped paper packet sealed with red wax and drop it into a canvas mailbag. Daylight, window light or matte painted ink only. No candle, flame, glow, spark, fireball or lightning. No readable words or numbers anywhere. Silent. Continuous motion through the final frame. No Explorer. No Orbit."
    ),
    (
        4, "08_midpoint_twist_packet", 330.68, 337.30, "A", "Q", None,
        None,
        None, None,
        "Midpoint twist (~65% runtime): Down House study fireplace burning low; Darwin holds Wallace's opened packet near the grate — then pulls it back to his desk",
        "Premium Animistry-class 3D cartoon. Down House study with a low hearth glow: a 49-year-old bearded English naturalist holds the opened foreign packet near the fireplace grate, pauses, and pulls it firmly back to his desk. No readable words or numbers anywhere. Silent. Continuous motion through the final frame. No Explorer. No Orbit."
    ),
    (
        4, "09a_darwin_reads_wallace", 337.30, 344.20, "A", "Q", "18 JUNE 1858",
        {
            "kind": "WHO",
            "line_1": "Charles Lyell",
            "line_2": "(1797–1875) — geologist",
            "when_stamp": "18 JUNE 1858",
            "hold_s": 3.8,
            "sfx": "tick_ink"
        },
        "who_charles_lyell", None,
        "18 June 1858: Darwin (aged 49, full beard) lowers Wallace's pages in shock at his Down House study window",
        "Premium Animistry-class 3D cartoon. Down House study, 18 June 1858: a 49-year-old bearded English naturalist stands by the window lowering the foreign manuscript pages in shock. No readable words or numbers anywhere. Silent. Continuous motion through the final frame. No Explorer. No Orbit."
    ),
    (
        4, "09b_smashed_letter_pen", 344.20, 349.50, "A", "F", "ORIGINALITY SMASHED",
        {"kind": "LABEL", "label": "ORIGINALITY SMASHED", "hold_s": 3.6, "sfx": "tick_ink"},
        None, None,
        "Close in grey window light on Darwin's hand writing urgently to Charles Lyell (\"All my originality... will be smashed\", DCP-LETT-2285)",
        "Premium Animistry-class 3D cartoon. Close in grey window light on a man's hand writing urgently with a steel pen across letter paper on a mahogany desk. Daylight, window light or matte painted ink only. No candle, flame, glow, spark, fireball or lightning. No readable words or numbers anywhere. Silent. Continuous motion through the final frame. No Explorer. No Orbit."
    ),
    (
        4, "10_fairness_25_june", 349.50, 355.58, "A", "F", None,
        None,
        None, None,
        "25 June 1858 (J0307 fix #2 — before 28 June death): in grey window light, Darwin places his own 1844 sketch beside Wallace's paper and seals a second letter to Lyell offering to give up priority",
        "Premium Animistry-class 3D cartoon. In grey window light at Down House, hands place the thick 1844 manuscript beside the thin foreign paper packet and fold a second letter. Daylight, window light or matte painted ink only. No candle, flame, glow, spark, fireball or lightning. No readable words or numbers anywhere. Silent. Continuous motion through the final frame. No Explorer. No Orbit."
    ),
    (
        4, "11_down_house_grief", 355.58, 360.98, "A", "Q", None,
        None,
        None, None,
        "Evening, 28 June 1858 (\"Three days later...\"): exterior of Down House at dusk with curtains drawn and a single dim candle in the study window (respectful restraint, no child shown)",
        "Premium Animistry-class 3D cartoon. Exterior of Down House in Kent at dusk, 28 June 1858: curtains drawn across the tall windows with a single gentle candle glow in the study window. No readable words or numbers anywhere. Silent. Continuous motion through the final frame. No Explorer. No Orbit."
    ),
    (
        4, "12_lyell_hooker_bundle", 360.98, 366.34, "B", "F", None,
        None,
        None, None,
        "In London in daylight, two naturalists tie Wallace's essay and Darwin's 1844/1857 extracts into one bundle with ribbon and carry it up stone steps",
        "Premium Animistry-class 3D cartoon. In London daylight, two Victorian gentlemen tie two manuscript bundles together with ribbon and carry them up stone steps. Daylight, window light or matte painted ink only. No candle, flame, glow, spark, fireball or lightning. No readable words or numbers anywhere. Silent. Continuous motion through the final frame. No Explorer. No Orbit."
    ),

    # === PART 05: The Night Nobody Noticed (6:06.34 - 7:28.16) ===
    (
        5, "01_card_p05", 366.34, 368.56, "A", "CG", "NIGHT NOBODY NOTICED",
        {"kind": "CHAPTER", "chapter": 5, "title": "The Night Nobody Noticed", "sfx": "rumble_low"},
        None, None,
        "3D case-file desk chapter card: The Night Nobody Noticed",
        "Own £0 chapter card graphic (code_graphic_013_p5_01_card_p05.mp4): case-file desk chapter card V."
    ),
    (
        5, "02a_linnean_reading", 368.56, 376.56, "B", "Q", "1 JULY 1858",
        {
            "kind": "WHO",
            "line_1": "Joseph Hooker",
            "line_2": "(1817–1911) — botanist",
            "when_stamp": "LONDON · 1 JULY 1858",
            "hold_s": 3.8,
            "sfx": "tick_ink"
        },
        "who_joseph_hooker", None,
        "London, 1 July 1858: a warm evening in the wood-panelled meeting room of the Linnean Society; the secretary reads papers aloud while Charles Lyell and Joseph Hooker sit near the front",
        "Premium Animistry-class 3D cartoon. London, 1 July 1858: inside the wood-panelled meeting room of the Linnean Society, the secretary reads aloud at a lectern while two senior Victorian men of science listen from the front bench. No readable words or numbers anywhere. Silent. Continuous motion through the final frame. No Explorer. No Orbit."
    ),
    (
        5, "02b_joint_papers_lectern", 376.56, 382.34, "B", "F", None,
        None,
        None, None,
        "Close in grey window light on the wooden lectern as the secretary's hands turn Wallace's paper beside Darwin's older 1844/1857 extracts",
        "Premium Animistry-class 3D cartoon. Close in grey window light on a wooden lectern as hands turn two bundled handwritten manuscripts side by side. Daylight, window light or matte painted ink only. No candle, flame, glow, spark, fireball or lightning. No readable words or numbers anywhere. Silent. Continuous motion through the final frame. No Explorer. No Orbit."
    ),
    (
        5, "03a_two_empty_chairs", 382.34, 388.20, "B", "Q", "TWO EMPTY CHAIRS",
        {"kind": "LABEL", "label": "TWO EMPTY CHAIRS", "hold_s": 3.6, "sfx": "tick_ink"},
        None, None,
        "Slow push-in on two empty velvet chairs at the front of the Linnean Society hall (J0307 fix #3: neither man was in the room)",
        "Premium Animistry-class 3D cartoon. Slow push-in on two empty red-velvet chairs at the front of the wood-panelled Linnean Society meeting room. No readable words or numbers anywhere. Silent. Continuous motion through the final frame. No Explorer. No Orbit."
    ),
    (
        5, "03b_wallace_jungle_clearing", 388.20, 394.06, "D", "Q", None,
        None,
        None, None,
        "In a sunlit Malay jungle clearing, Wallace (aged 35) examines a butterfly net, unaware of the London reading (\"Wallace hadn't even been asked\")",
        "Premium Animistry-class 3D cartoon. In a sunlit tropical clearing in the Malay Archipelago, a 35-year-old bearded field naturalist in round wire-rimmed spectacles examines a specimen net, unaware of London. No readable words or numbers anywhere. Silent. Continuous motion through the final frame. No Explorer. No Orbit."
    ),
    (
        5, "04a_empty_linnean_hall", 394.06, 398.00, "B", "F", None,
        None,
        None, None,
        "The quiet Linnean Society hall after the meeting as benches stand empty in grey window light (\"And the reaction? Almost nothing.\")",
        "Premium Animistry-class 3D cartoon. The wood-panelled Linnean Society meeting room standing quiet and empty in grey window light after the session. Daylight, window light or matte painted ink only. No candle, flame, glow, spark, fireball or lightning. No readable words or numbers anywhere. Silent. Continuous motion through the final frame. No Explorer. No Orbit."
    ),
    (
        5, "04b_bell_report_1859", 398.00, 404.66, "B", "F", "NO STRIKING DISCOVERY",
        {
            "kind": "FACT",
            "label": "NO STRIKING DISCOVERY",
            "when_stamp": "MAY 1859",
            "hold_s": 3.6,
            "sfx": "tick_ink"
        },
        None, None,
        "May 1859: in grey window light, the Linnean Society's annual report opens on a wooden lectern as a pen underlines a single sentence",
        "Premium Animistry-class 3D cartoon. May 1859: in grey window light, a printed report lies open on a wooden lectern as a steel pen underlines a single unlettered line. Daylight, window light or matte painted ink only. No candle, flame, glow, spark, fireball or lightning. No readable words or numbers anywhere. Silent. Continuous motion through the final frame. No Explorer. No Orbit."
    ),
    (
        5, "05a_darwin_writes_origin", 404.66, 411.56, "A", "Q", None,
        None,
        None, None,
        "Down House, 1858–1859: Darwin writes page after page at his desk as daylight and candlelight cycle past the study window, stacking a finished green-bound manuscript",
        "Premium Animistry-class 3D cartoon. Down House study, 1858–1859: a bearded English naturalist writes page after page at his mahogany desk as light shifts across the window, stacking a thick manuscript. No readable words or numbers anywhere. Silent. Continuous motion through the final frame. No Explorer. No Orbit."
    ),
    (
        5, "05b_arch_origin_1859_title", 411.56, 414.44, "A/G", "ARCH", None,
        {"kind": "ARCHIVE", "credit": "Darwin, Origin of Species 1st ed. (John Murray, 1859, PD)"},
        None, "origin_1859_title",
        "Free archive composite: John Murray's 1st edition title page of On the Origin of Species (24 Nov 1859, Public Domain) on the study desk with animated gold ink highlight",
        "Own £0 archive composite (code_graphic_013_p5_05b_arch_origin_1859_title.mp4): public-domain 1859 Origin of Species 1st ed. title page composite with credit line."
    ),
    (
        5, "06_murray_bookshop", 414.44, 419.00, "E", "Q", "24 NOVEMBER 1859",
        {
            "kind": "WHEN",
            "label": "24 NOVEMBER 1859",
            "timeline_step": "6/7 · 24 Nov 1859 (Origin published)",
            "hold_s": 3.5,
            "sfx": "tick_ink"
        },
        None, None,
        "London, November 1859: John Murray's Albemarle Street bookshop window stacked with green cloth copies of On the Origin of Species; booksellers' clerks carry stacks out before opening day (J0307 fix #4)",
        "Premium Animistry-class 3D cartoon. Albemarle Street, London, November 1859: a publisher's bow-windowed bookshop stacked with green cloth-bound books as clerks carry stacks out into the morning street. No readable words or numbers anywhere. Silent. Continuous motion through the final frame. No Explorer. No Orbit."
    ),
    (
        5, "07_cg_timeline_origin", 419.00, 424.58, "G", "CG", "1,250 COPIES PRE-SOLD",
        {
            "kind": "DATA",
            "label": "1,250 COPIES PRE-SOLD",
            "detail": "Master timeline (1835 · 1837 · 1838 · 1844 · 1858 · 1859 · 1889) + ~1,250 copies ordered before publication day",
            "scale": "every copy ordered before the book even went on sale",
            "hold_s": 3.6,
            "sfx": "tick_ink"
        },
        None, None,
        "Code graphic #5: animated master timeline (1835 · 1837 · 1838 · 1844 · 1858 · 1859 · 1889) completing beside a stack of ~1,250 green books stamped PRE-SOLD",
        "Own £0 code graphic (code_graphic_013_p5_07_cg_timeline_origin.mp4): 7-date master timeline 1835 → 1889 + 1,250 copies ordered at Murray's pre-publication sale."
    ),
    (
        5, "08a_wallace_opens_origin", 424.58, 428.00, "D", "F", None,
        None,
        None, None,
        "In daylight on a bamboo veranda in the Malay Archipelago, Wallace's hands unwrap a green cloth copy of On the Origin of Species",
        "Premium Animistry-class 3D cartoon. Close in daylight on a bamboo veranda table as hands unwrap twine from a green cloth-bound octavo book. Daylight, window light or matte painted ink only. No candle, flame, glow, spark, fireball or lightning. No readable words or numbers anywhere. Silent. Continuous motion through the final frame. No Explorer. No Orbit."
    ),
    (
        5, "08b_wallace_reads_origin", 428.00, 434.24, "D", "Q", None,
        None,
        None, None,
        "Back in the Malay Archipelago (1860), Wallace sits on his bamboo veranda reading the green copy of On the Origin of Species, smiling warmly and nodding",
        "Premium Animistry-class 3D cartoon. Malay Archipelago, 1860: a 37-year-old bearded field naturalist sits on a sunlit bamboo veranda reading a green cloth-bound book, smiling warmly and nodding in admiration. No readable words or numbers anywhere. Silent. Continuous motion through the final frame. No Explorer. No Orbit."
    ),
    (
        5, "09_arch_darwinism_1889", 434.24, 440.50, "A/G", "ARCH", "DARWINISM · 1889",
        {
            "kind": "ARCHIVE",
            "label": "DARWINISM · 1889",
            "when_stamp": "1889",
            "timeline_step": "7/7 · 1889 (Wallace's Darwinism)",
            "credit": "Wallace, Darwinism 1st ed. (Macmillan, 1889, PD)",
            "hold_s": 3.6,
            "sfx": "tick_ink"
        },
        None, "darwinism_1889_title",
        "Free archive composite: 1st edition title page of Alfred Russel Wallace's 1889 book Darwinism (Macmillan, Public Domain) on a Victorian study desk with animated gold ink highlight",
        "Own £0 archive composite (code_graphic_013_p5_09_arch_darwinism_1889.mp4): public-domain 1889 Wallace Darwinism title page composite with credit line."
    ),
    (
        5, "10_darwin_worried_shelf", 440.50, 448.16, "A", "Q", None,
        None,
        None, None,
        "At Down House, an older Darwin furrows his brow over a notebook page while the camera pans to an uncut German journal sitting unread on a high shelf",
        "Premium Animistry-class 3D cartoon. At Down House, an older bearded English naturalist furrows his brow over a study notebook while the camera pans up to an uncut paper-bound journal resting on a high bookshelf. No readable words or numbers anywhere. Silent. Continuous motion through the final frame. No Explorer. No Orbit."
    ),

    # === PART 06: The Missing Piece (7:28.16 - 8:35.00) ===
    (
        6, "01_card_p06", 448.16, 449.66, "A", "CG", "THE MISSING PIECE",
        {"kind": "CHAPTER", "chapter": 6, "title": "The Missing Piece", "sfx": "rumble_low"},
        None, None,
        "3D case-file desk chapter card: The Missing Piece",
        "Own £0 chapter card graphic (code_graphic_013_p6_01_card_p06.mp4): case-file desk chapter card VI."
    ),
    (
        6, "02a_jenkin_study", 449.66, 453.50, "F", "Q", "JUNE 1867",
        {
            "kind": "WHO",
            "line_1": "Fleeming Jenkin",
            "line_2": "(1833–1885) — engineer",
            "when_stamp": "JUNE 1867",
            "hold_s": 3.4,
            "sfx": "tick_ink"
        },
        "who_fleeming_jenkin", None,
        "Edinburgh, June 1867: engineer Fleeming Jenkin stands at his study table beside two ceramic paint pots",
        "Premium Animistry-class 3D cartoon. Edinburgh, June 1867: a Scottish engineer stands at a wooden study table beside a pot of crimson paint and a pot of white paint. No readable words or numbers anywhere. Silent. Continuous motion through the final frame. No Explorer. No Orbit."
    ),
    (
        6, "02b_paint_pots_mix", 453.50, 458.78, "F", "F", "BLENDED AWAY?",
        {"kind": "LABEL", "label": "BLENDED AWAY?", "hold_s": 3.5, "sfx": "tick_ink"},
        None, None,
        "Close in grey window light as hands pour crimson paint and white paint together into a glass bowl, stirring them to a dull mid-grey",
        "Premium Animistry-class 3D cartoon. Close in grey window light on a wooden table as hands pour crimson paint and white paint into a glass bowl and stir them into a uniform dull grey. Daylight, window light or matte painted ink only. No candle, flame, glow, spark, fireball or lightning. No readable words or numbers anywhere. Silent. Continuous motion through the final frame. No Explorer. No Orbit."
    ),
    (
        6, "03_cg_blending_beaks", 458.78, 471.06, "G", "CG", "WASHED AWAY BY BLENDING",
        {"kind": "EXPLAINER", "label": "WASHED AWAY BY BLENDING", "hold_s": 3.6, "sfx": "tick_ink"},
        None, None,
        "Explainer diagram (inked on period paper): a deep gold finch beak blends with a small pale beak to make a 1/2 beak, then 1/4, fading into grey wash",
        "Own £0 code graphic (code_graphic_013_p6_03_cg_blending_beaks.mp4): inked blending-inheritance diagram showing deep gold beak diluting across generations 1, 1/2, 1/4, 1/8."
    ),
    (
        6, "04a_mendel_pea_garden", 471.06, 476.56, "F", "Q", "BRNO · 1866",
        {
            "kind": "WHO",
            "line_1": "Gregor Mendel",
            "line_2": "(1822–1884) — friar",
            "when_stamp": "BRNO · 1866",
            "hold_s": 3.8,
            "sfx": "tick_ink"
        },
        "who_gregor_mendel", None,
        "Brno, 1866: in a sunlit walled monastery garden, friar Gregor Mendel in his Augustinian habit examines purple and white pea blossoms with a small notebook",
        "Premium Animistry-class 3D cartoon. Brno, 1866: in a sunlit walled monastery garden, a friar in his black-and-white Augustinian habit and spectacles gently examines purple and white pea blossoms on a trellis. No readable words or numbers anywhere. Silent. Continuous motion through the final frame. No Explorer. No Orbit."
    ),
    (
        6, "04b_arch_mendel_1866_paper", 476.56, 479.92, "F/G", "ARCH", None,
        {"kind": "ARCHIVE", "credit": "Mendel, Versuche über Pflanzen-Hybriden (Brünn, 1866, PD)"},
        None, "mendel_1866_paper",
        "Free archive composite: first page of Gregor Mendel's 1866 paper Versuche über Pflanzen-Hybriden (Public Domain) on a monastery table with animated gold ink highlight",
        "Own £0 archive composite (code_graphic_013_p6_04b_arch_mendel_1866_paper.mp4): public-domain Mendel 1866 paper scan composite with credit line."
    ),
    (
        6, "05_beads_not_paint", 479.92, 485.64, "F", "Q", "WHOLE LIKE BEADS",
        {"kind": "LABEL", "label": "WHOLE LIKE BEADS", "hold_s": 3.5, "sfx": "tick_ink"},
        None, None,
        "Close-up on a wooden table: the grey paint bowl fades away as whole green and yellow glass beads roll together into a jar without changing colour",
        "Premium Animistry-class 3D cartoon. Close-up on a sunlit wooden table: whole green and yellow glass beads roll together into a clear glass jar, each bead keeping its bright distinct colour. No readable words or numbers anywhere. Silent. Continuous motion through the final frame. No Explorer. No Orbit."
    ),
    (
        6, "06a_origin_fifth_edition", 485.64, 490.60, "A", "F", None,
        None,
        None, None,
        "In grey window light at Down House, a green-cloth copy of On the Origin of Species opens on the desk beside a folded letter from Wallace",
        "Premium Animistry-class 3D cartoon. Close in grey window light on a mahogany desk as a green cloth-bound book opens beside a folded handwritten letter. Daylight, window light or matte painted ink only. No candle, flame, glow, spark, fireball or lightning. No readable words or numbers anywhere. Silent. Continuous motion through the final frame. No Explorer. No Orbit."
    ),
    (
        6, "06b_spencer_coined", 490.60, 496.54, "A", "Q", "1864",
        {
            "kind": "WHO",
            "line_1": "Herbert Spencer",
            "line_2": "(1820–1903) — philosopher",
            "when_stamp": "1864",
            "hold_s": 3.8,
            "sfx": "tick_ink"
        },
        "who_herbert_spencer", None,
        "London, 1864: philosopher Herbert Spencer writes at his study desk",
        "Premium Animistry-class 3D cartoon. London, 1864: Victorian philosopher Herbert Spencer with side whiskers writes at a wooden study desk in warm light. No readable words or numbers anywhere. Silent. Continuous motion through the final frame. No Explorer. No Orbit."
    ),
    (
        6, "07_key_in_lock", 496.54, 504.08, "A", "Q", "FIT MEANS FITS",
        {"kind": "LABEL", "label": "FIT MEANS FITS", "hold_s": 3.5, "sfx": "tick_ink", "note": "Short B frame 0"},
        None, None,
        "Close-up on a Victorian desk: a finely cut brass key slides smoothly into an iron lock and turns the bolt cleanly (Short B frame 0)",
        "Premium Animistry-class 3D cartoon. Close-up on a Victorian wooden desk: a finely cut brass key slides smoothly into an iron lock and turns the bolt cleanly. Short B frame 0. No readable words or numbers anywhere. Silent. Continuous motion through the final frame. No Explorer. No Orbit."
    ),
    (
        6, "08a_reuse_study_beaks_callback", 504.08, 508.48, "A", "REUSE", None,
        {"kind": "REUSE", "source_row": "P1:01_study_beaks", "window_s": [3.80, 8.00]},
        None, None,
        "Callback to Part 01 row 01 (study_beaks unused [3.80s..8.00s] tail): Darwin's open Notebook B and the four Galápagos finch beaks on the Down House desk",
        "Reuse of P1:01_study_beaks [3.80s..8.00s] unused moving tail (4.40 s required out of 4.20 s + 0.20 s xfade; £0, 0 credits)."
    ),
    (
        6, "08b_darwin_mendel_synthesis", 508.48, 512.48, "A", "Q", None,
        None,
        None, None,
        "Final synthesis shot: Darwin's red-leather Notebook B (\"I think\" tree) and a dish of Mendel's green and yellow peas sit side by side in warm golden sunlight at Down House",
        "Premium Animistry-class 3D cartoon. Warm golden sunlight in the Down House study: an open red-leather notebook and a porcelain dish of bright green and yellow garden peas sit side by side on the mahogany desk. No readable words or numbers anywhere. Silent. Continuous motion through the final frame. No Explorer. No Orbit."
    ),
    (
        6, "09_cream_end_card", 512.48, 515.00, "G", "CG", None,
        {"kind": "END_CARD", "hold_s": 2.52},
        None, None,
        "House cream end card (STUDIO_PLAYBOOK.md §7): music holds 2.5 s past the last word (8:32.24), then fades cleanly. No goodbye, no subscribe ask",
        "Own £0 house cream end card (code_graphic_013_p6_09_cream_end_card.mp4)."
    ),
]


def build_boards() -> None:
    words = load_vo_words()
    parts_dir = EDIT / "parts"
    parts_dir.mkdir(parents=True, exist_ok=True)

    # Verify contiguity, HOS-2026-11-E2, <= 8.0s mint rule, and non-adjacent full-frame CG/ARCH rule
    prev_out = 0.0
    for idx, r in enumerate(ROWS_SPEC):
        part, rid, t_in, t_out, set_id, eng, side_label, teach, who_p, arch_id, desc, prompt = r
        assert abs(t_in - prev_out) < 1e-6, f"Gap at {rid}: {t_in} != {prev_out}"
        dur = round(t_out - t_in, 2)
        assert dur > 0, f"Non-positive dur at {rid}"
        if t_in < 30.0:
            assert dur <= 4.50 + 1e-6, f"HOS-2026-11-E2 violation: {rid} in first 30s has dur {dur}s > 4.5s"
        if eng in ("Q", "F"):
            assert dur <= 8.00 + 1e-6, f"Minted row {rid} exceeds 8.0s Veo clip: {dur}s"
        if eng == "F":
            low_p = prompt.lower()
            for bad in ("candlelit", "oil lamp", "firelight", "burns on"):
                assert bad not in low_p, f"Emissive word {bad!r} in Fast row {rid}"
        if idx > 0 and eng in ("CG", "ARCH") and not rid.startswith("01_card_"):
            prev_eng = ROWS_SPEC[idx - 1][5]
            prev_id = ROWS_SPEC[idx - 1][1]
            if not prev_id.startswith("01_card_"):
                assert prev_eng not in ("CG", "ARCH"), f"Back-to-back full-frame graphics: {prev_id} ({prev_eng}) -> {rid} ({eng})"
        prev_out = t_out
    assert abs(prev_out - 515.00) < 1e-6

    # Group by part and write part-0N_plates_v01.json
    cum_flow_try1 = 0
    cum_flow_exp = 0
    cum_vertex_try1 = 0.0
    cum_vertex_exp = 0.0

    per_part_summaries = []
    all_part_objs = []

    for pnum in range(1, 7):
        pmeta = PART_META[pnum]
        prows = [r for r in ROWS_SPEC if r[0] == pnum]
        plates = []
        p_q = p_f = p_cg = p_arch = p_reuse = 0
        p_flow_try1 = p_flow_exp = 0
        p_vert_try1 = p_vert_exp = 0.0
        p_explorer = 0

        for r in prows:
            _, rid, t_in, t_out, set_id, eng, side_label, teach, who_p, arch_id, desc, prompt = r
            dur = round(t_out - t_in, 2)
            row_words = [
                w["word"] for w in words
                if (w["start"] + w["end"]) / 2.0 >= t_in and (w["start"] + w["end"]) / 2.0 < t_out
            ]
            vo_land_text = " ".join(row_words)
            is_explorer = bool(teach and teach.get("kind") == "EXPLORER")
            if is_explorer:
                p_explorer += 1

            if eng == "Q":
                p_q += 1
                quality = "Quality"
                route = "flow-first"
                flow_model = "Veo 3.1 Quality"
                flow_clip_s = 8
                f_try1, f_exp = 100, 259
                v_model = "veo-3.1-generate-001"
                v_clip_s = 8 if dur > 6.0 else 6
                v_try1 = 1.28 if v_clip_s == 8 else 0.96
                v_exp = 3.39 if v_clip_s == 8 else 2.56
                src_kind = "new_mint_quality"
                src_note = f"New plate, needs minting · Flow Veo 3.1 Quality · 100 credits"
            elif eng == "F":
                p_f += 1
                quality = "Fast"
                route = "flow-first"
                flow_model = "Veo 3.1 Fast"
                flow_clip_s = 8
                f_try1, f_exp = 10, 20
                v_model = "veo-3.1-fast-generate-001"
                v_clip_s = 8 if dur > 6.0 else 6
                v_try1 = 0.64 if v_clip_s == 8 else 0.48
                v_exp = 1.34 if v_clip_s == 8 else 1.01
                src_kind = "new_mint_fast"
                src_note = f"New plate, needs minting · Flow Veo 3.1 Fast (non-emissive) · 10 credits"
            elif eng == "CG":
                p_cg += 1
                quality = "code_graphic"
                route = "code-graphic"
                flow_model = None
                flow_clip_s = 0
                f_try1, f_exp = 0, 0
                v_model = None
                v_clip_s = 0
                v_try1, v_exp = 0.0, 0.0
                cg_file = f"code_graphic_013_p{pnum}_{rid}.mp4"
                src_kind = "code_graphic"
                src_note = f"Built £0 code graphic (`07_Edit-Project/code_graphics_v01/{cg_file}`) · 0 credits"
                if arch_id:
                    am = ARCHIVE_META[arch_id]
                    src_note += f" · embeds public-domain scan `{am['local_raw']}` ({am['commons_page']}, {am['licence']})"
            elif eng == "ARCH":
                p_arch += 1
                quality = "archive"
                route = "archive"
                flow_model = None
                flow_clip_s = 0
                f_try1, f_exp = 0, 0
                v_model = None
                v_clip_s = 0
                v_try1, v_exp = 0.0, 0.0
                cg_file = f"code_graphic_013_p{pnum}_{rid}.mp4"
                am = ARCHIVE_META[arch_id]
                src_kind = "free_archive"
                src_note = (
                    f"Built £0 archive composite (`07_Edit-Project/code_graphics_v01/{cg_file}`) from "
                    f"`{am['local_raw']}` ({am['commons_page']}, **{am['licence']}**) · 0 credits"
                )
            elif eng == "REUSE":
                p_reuse += 1
                quality = "reuse"
                route = "reuse"
                flow_model = None
                flow_clip_s = 0
                f_try1, f_exp = 0, 0
                v_model = None
                v_clip_s = 0
                v_try1, v_exp = 0.0, 0.0
                src_kind = "existing_plate_reuse"
                src_note = "Intra-film reuse of `P1:01_study_beaks` unused tail `[3.80s..8.00s]` (minted once in Part 01) · 0 credits"
            else:
                raise ValueError(eng)

            if who_p:
                am = ARCHIVE_META[who_p]
                src_note += (
                    f" · WHO portrait cut-out overlay built at `07_Edit-Project/code_graphics_v01/who_overlays/{who_p}_overlay.png` "
                    f"from `{am['local_raw']}` ({am['commons_page']}, **{am['licence']}**)"
                )

            p_flow_try1 += f_try1
            p_flow_exp += f_exp
            p_vert_try1 = round(p_vert_try1 + v_try1, 2)
            p_vert_exp = round(p_vert_exp + v_exp, 2)

            cum_flow_try1 += f_try1
            cum_flow_exp += f_exp
            cum_vertex_try1 = round(cum_vertex_try1 + v_try1, 2)
            cum_vertex_exp = round(cum_vertex_exp + v_exp, 2)

            plate_obj = {
                "id": rid,
                "t_s": round(t_in, 2),
                "t_end_s": round(t_out, 2),
                "t": fmt_t(t_in),
                "t_end": fmt_t(t_out),
                "local_s": round(t_in - pmeta["vo_start_s"], 2),
                "use_s": dur,
                "set": set_id,
                "explorer": is_explorer,
                "side_label": side_label,
                "quality": quality,
                "route": route,
                "source_kind": src_kind,
                "source_detail": src_note,
                "shot_description": desc,
                "prompt": prompt,
                "vo_land": [vo_land_text] if vo_land_text else [],
                "generation_authorized": False,
                "flow_model": flow_model,
                "flow_clip_s": flow_clip_s,
                "flow_credits_try1": f_try1,
                "flow_credits_expected": f_exp,
                "vertex_model": v_model,
                "vertex_clip_s": v_clip_s,
                "vertex_try1_gbp": v_try1,
                "vertex_expected_gbp": v_exp,
                "cum_flow_credits_try1": cum_flow_try1,
                "cum_flow_credits_expected": cum_flow_exp,
                "cum_vertex_try1_gbp": cum_vertex_try1,
                "cum_vertex_expected_gbp": cum_vertex_exp,
            }
            if teach:
                plate_obj["teach_overlay"] = teach
            if who_p:
                am = ARCHIVE_META[who_p]
                plate_obj["who_portrait_archive"] = {
                    "id": who_p,
                    "local_raw": am["local_raw"],
                    "overlay_png": f"07_Edit-Project/code_graphics_v01/who_overlays/{who_p}_overlay.png",
                    "commons_page": am["commons_page"],
                    "licence": am["licence"],
                    "sha256": am["sha256"],
                }
            if arch_id:
                am = ARCHIVE_META[arch_id]
                plate_obj["archive_source"] = {
                    "id": arch_id,
                    "local_raw": am["local_raw"],
                    "commons_page": am["commons_page"],
                    "licence": am["licence"],
                    "description": am["description"],
                    "sha256": am["sha256"],
                }
            if eng in ("CG", "ARCH"):
                cg_file = f"code_graphic_013_p{pnum}_{rid}.mp4"
                plate_obj["code_graphic_spec"] = {
                    "file": cg_file,
                    "path": f"07_Edit-Project/code_graphics_v01/{cg_file}",
                    "shows": desc,
                    "spend": "£0",
                }
            plates.append(plate_obj)

        part_summary = {
            "part": pnum,
            "title": pmeta["title"],
            "vo_start_s": pmeta["vo_start_s"],
            "vo_end_s": pmeta["vo_end_s"],
            "duration_s": round(pmeta["vo_end_s"] - pmeta["vo_start_s"], 2),
            "rows": len(plates),
            "Quality": p_q,
            "Fast": p_f,
            "code_graphic": p_cg,
            "archive": p_arch,
            "reuse": p_reuse,
            "mint_rows": p_q + p_f,
            "free_rows": p_cg + p_arch + p_reuse,
            "explorer": p_explorer,
            "flow_credits_try1": p_flow_try1,
            "flow_credits_expected": p_flow_exp,
            "vertex_try1_gbp": p_vert_try1,
            "vertex_expected_gbp": p_vert_exp,
        }
        per_part_summaries.append(part_summary)

        part_doc = {
            "part": f"{pnum:02d}",
            "title": pmeta["title"],
            "film": "013_Darwin-Wallace-Evolution",
            "working_title": "Evolution: The Letter That Forced Darwin to Publish",
            "version": "v01",
            "task": "J2476: HOS 013 picture plan v01 on locked VO hos_013_vo_v03a.wav + free picture built + priced and parked for Chief.",
            "mint": False,
            "status": "BOARD_V01_PARKED_FOR_CHIEF",
            "vo_file": "02_Voiceover/hos_013_vo_v03a.wav",
            "vo_sha256": VO_SHA256,
            "vo_duration_s": 512.48,
            "vo_film_start_s": pmeta["vo_start_s"],
            "part_end_film_s": pmeta["vo_end_s"],
            "chapter_card": pmeta["chapter_card"],
            "summary": part_summary,
            "plates": plates,
        }
        all_part_objs.append(part_doc)
        out_p = parts_dir / f"part-{pnum:02d}_plates_v01.json"
        out_p.write_text(json.dumps(part_doc, indent=2) + "\n")
        if NAS_EDIT.exists():
            (NAS_EDIT / "parts").mkdir(parents=True, exist_ok=True)
            shutil.copy2(out_p, NAS_EDIT / "parts" / out_p.name)

    totals = {
        "rows": sum(p["rows"] for p in per_part_summaries),
        "Quality": sum(p["Quality"] for p in per_part_summaries),
        "Fast": sum(p["Fast"] for p in per_part_summaries),
        "code_graphic": sum(p["code_graphic"] for p in per_part_summaries),
        "archive": sum(p["archive"] for p in per_part_summaries),
        "reuse": sum(p["reuse"] for p in per_part_summaries),
        "mint_rows": sum(p["mint_rows"] for p in per_part_summaries),
        "free_rows": sum(p["free_rows"] for p in per_part_summaries),
        "explorer": sum(p["explorer"] for p in per_part_summaries),
        "flow_credits_try1": cum_flow_try1,
        "flow_credits_expected": cum_flow_exp,
        "vertex_try1_gbp": cum_vertex_try1,
        "vertex_expected_gbp": cum_vertex_exp,
    }

    plan_v01 = {
        "film": "013_Darwin-Wallace-Evolution",
        "working_title": "Evolution: The Letter That Forced Darwin to Publish",
        "air_date": "2026-12-17",
        "version": "v01",
        "written": "2026-11-10",
        "task": "J2476: HOS 013 picture plan v01 on locked VO hos_013_vo_v03a.wav, free picture built and QA'd, paid mint rows priced and parked for Chief behind HOS 009 and 010.",
        "script": "01_Script/darwin_script_master_v02.md (92.6 PASS, J0307)",
        "facts_pass": "01_Script/FACT_NOTES_v02.md + 01_Script/GEMINI_QUOTE_PASS_J0304.md (30 OK, 0 PARTIAL, 0 FLAG)",
        "vo_file": "02_Voiceover/hos_013_vo_v03a.wav",
        "vo_sha256": VO_SHA256,
        "vo_duration_s": 512.48,
        "master_duration_s": 515.00,
        "shorts_vo": {
            "Short_A": "10_Shorts/vo_v02/hos_013_short_A_v02.wav (26.64 s, J2288 KEEP, PR #444)",
            "Short_B": "10_Shorts/vo_v02/hos_013_short_B_v02.wav (26.00 s, J2288 KEEP, PR #444)",
        },
        "hos_2026_11_e2_open": {
            "window_s": [0.00, 30.00],
            "cuts_overlapping_0_30": 9,
            "max_cut_s_in_0_30": 4.22,
            "all_cuts_under_4p5s": True,
            "physical_proof_0_05_to_0_15": [
                "P1:02_drawer_lock (0:03.80-0:07.90): Darwin's hands lock the red-leather notebook in the desk drawer",
                "P1:03a_unlabelled_birds (0:07.90-0:11.90): unlabelled Galápagos finch skins with blank parchment tags on the study table",
                "P1:03b_malay_packet (0:11.90-0:16.02): barnacle specimen jar, brass dissecting microscope, and Wallace's twine-tied packet landing on the desk",
            ],
            "early_data_scale": {
                "row": "P1:08_cg_i_think_tree",
                "t_in_s": 39.40,
                "t_out_s": 54.30,
                "lands_in_0_25_to_0_40": True,
                "data": "\"I think\" tree (Notebook B p. 36) + 20-year secrecy bar (1838 → 1858)",
                "scale": "20 years in a drawer — longer than a child takes to grow up",
            },
        },
        "totals": totals,
        "per_part": per_part_summaries,
        "mint_order": "HOS 009 > HOS 010 > HOS 013. Nothing in 013 is generation_authorized. Paid picture parks for the Chief's price pass.",
    }

    (EDIT / "PICTURE_PLAN_v01.json").write_text(json.dumps(plan_v01, indent=2) + "\n")
    if NAS_EDIT.exists():
        shutil.copy2(EDIT / "PICTURE_PLAN_v01.json", NAS_EDIT / "PICTURE_PLAN_v01.json")

    # Write PICTURE_PLAN_v01.md and PRICE_REVIEW_v01.md
    write_markdown_docs(plan_v01, all_part_objs)
    build_shorts_plan()
    print("Built PICTURE_PLAN_v01:", json.dumps(totals))


def write_markdown_docs(plan: dict, all_parts: list[dict]) -> None:
    tot = plan["totals"]
    md = [
        "# 013 picture plan v01: *Evolution: The Letter That Forced Darwin to Publish*",
        "",
        "**Written 10 Nov 2026 (`J2476`). Spend: `£0` / `0` Flow credits.**",
        "",
        "Timed directly to the Chief-locked long voiceover **`02_Voiceover/hos_013_vo_v03a.wav`** (`512.480 s` = `8:32.48`, `sha256: f8ef433b3b5b5571284e6f12ef339a2b2c0d39eb9978753e86a4d0efeb5e1a03`, `J1310`) and word timestamps (`02_Voiceover/stt/hos_013_vo_v03a/words_fw_small_en.json`), with the two accepted Shorts voiceovers (`hos_013_short_A_v02.wav` and `hos_013_short_B_v02.wav`, `J2288` KEEP, PR #444) mapped in `10_Shorts/SHORTS_PICTURE_PLAN_v01.json`.",
        "",
        "## 1. HOS-2026-11-E2 proof-first first 30 seconds (`0:00.00–0:40.00`)",
        "",
        "| Gate | Requirement | In `PICTURE_PLAN_v01` | Status |",
        "|---|---|---|---|",
        "| **CUTS (`0:00–0:30`)** | Every visual cut `≤ 4.5 s`, `≥ 7` distinct moving plates, no hold `> 4.5 s` | **9 distinct moving plates** overlapping `0:00–0:30` (`P1:01` `3.80 s`, `P1:02` `4.10 s`, `P1:03a` `4.00 s`, `P1:03b` `4.12 s`, `P1:04a` `2.98 s`, `P1:04b` `2.64 s`, `P1:05a` `4.00 s`, `P1:05b` `3.58 s`, `P1:06` `4.22 s`); max cut **`4.22 s`** | **PASS** |",
        "| **PROOF (`0:05–0:15`)** | Physical proof or apparatus already moving (no exterior establishing shot) | `P1:02` (`0:03.80–0:07.90`: hands locking *Notebook B* in drawer), `P1:03a` (`0:07.90–0:11.90`: unlabelled Galápagos finch skins with blank tags), `P1:03b` (`0:11.90–0:16.02`: barnacle specimen jar, brass dissecting microscope, and Wallace's packet landing on desk) | **PASS** |",
        "| **EARLY (`0:25–0:40`)** | First animated `DATA + SCALE` graphic on screen between `0:25` and `0:40`, matching `FACT_NOTES` | `P1:08_cg_i_think_tree` starts at **`0:39.40`** (`0:39.40–0:54.30`, `14.90 s`) as Darwin says *\"in a private notebook — one kind of animal at the bottom, branching into many at the top\"*: traces the public-domain 1837 *Notebook B* p. 36 tree (`MS DAR 121:36`) + 20-year secrecy bar (`1838 → 1858`, `SCALE: 20 years in a drawer — longer than a child takes to grow up`) | **PASS** |",
        "",
        "## 2. Cost table (nothing minted in `J2476`; parked behind HOS 009 and 010)",
        "",
        "| Part | Chapter title | Time (`in–out`) | Rows | Quality (`100`) | Fast (`10`) | Code graphic (`0`) | Free archive (`0`) | Reuse (`0`) | Mint rows | Free rows | Flow credits (try-1) | Flow credits (expected) | Vertex try-1 (£) | Vertex expected (£) |",
        "|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for p in plan["per_part"]:
        md.append(
            f"| Part {p['part']:02d} | {p['title'].split('—')[1].strip()} | `{fmt_t(p['vo_start_s'])}–{fmt_t(p['vo_end_s'])}` | "
            f"{p['rows']} | {p['Quality']} | {p['Fast']} | {p['code_graphic']} | {p['archive']} | {p['reuse']} | "
            f"{p['mint_rows']} | {p['free_rows']} | {p['flow_credits_try1']:,} | {p['flow_credits_expected']:,} | "
            f"£{p['vertex_try1_gbp']:.2f} | £{p['vertex_expected_gbp']:.2f} |"
        )
    md.append(
        f"| **Total** | **Full film (`8:35.00`)** | `0:00.00–8:35.00` | **{tot['rows']}** | **{tot['Quality']}** | **{tot['Fast']}** | "
        f"**{tot['code_graphic']}** | **{tot['archive']}** | **{tot['reuse']}** | **{tot['mint_rows']}** | **{tot['free_rows']}** | "
        f"**{tot['flow_credits_try1']:,}** | **{tot['flow_credits_expected']:,}** | **£{tot['vertex_try1_gbp']:.2f}** | **£{tot['vertex_expected_gbp']:.2f}** |"
    )
    md += [
        "",
        f"- **{tot['rows']} rows** across `515.00 s` (`512.48 s` VO + `2.52 s` cream end card). Every minted row (`Q` or `F`) is **`≤ 8.00 s`**, so 0 rows exceed the 8 s length of a single Veo 3.1 clip.",
        f"- **{tot['free_rows']} free (`£0` / `0` credit) rows are built and QA'd on disk/NAS now:** {tot['code_graphic']} animated code graphics/maps/diagrams/cards + {tot['archive']} public-domain archive composites + {tot['reuse']} intra-film callback reuse (`P6:08a` reusing the `[3.80s..8.00s]` tail of `P1:01_study_beaks`).",
        f"- **{tot['mint_rows']} rows need minting:** **{tot['Quality']} Quality** (`{tot['Quality']*100:,}` credits try-1) and **{tot['Fast']} Fast** (`{tot['Fast']*10:,}` credits try-1, all non-emissive daylight/window-light) = **`{tot['flow_credits_try1']:,}` Flow credits first-try** (`{tot['flow_credits_expected']:,}` expected with the standard `2.59×` Q / `2.0×` F retry allowance). `generation_authorized` is `false` on every row; parked for the Chief's price pass behind **HOS 009** and **HOS 010**.",
        "",
        "## 3. Free picture built and QA'd in `J2476` (`£0`)",
        "",
        "- **22 rendered `1920×1080` 30 fps H.264 `.mp4` clips + `.jpg` hero stills** in `07_Edit-Project/code_graphics_v01/` (mirrored to `/Volumes/data/studio-live/History Of Science/02_Video-Projects/013_Darwin-Wallace-Evolution/07_Edit-Project/code_graphics_v01/`):",
        "  - 6 chapter & end cards: `P2:01_card_p02`, `P3:01_card_p03`, `P4:01_card_p04`, `P5:01_card_p05`, `P6:01_card_p06`, `P6:09_cream_end_card`",
        "  - 10 animated data charts, maps & inked explainer diagrams: `P1:08_cg_i_think_tree`, `P1:10_cg_globe_arc`, `P2:06b_cg_tortoise_shells`, `P2:09_cg_finch_toolbox`, `P3:03_cg_malthus_curve`, `P3:06_nature_keeps_fit`, `P3:12_cg_barnacle_counter`, `P4:05_cg_wallace_counter`, `P5:07_cg_timeline_origin`, `P6:03_cg_blending_beaks`",
        "  - 6 public-domain archive composites (2.5D layered desk + animated ink callouts + corner credit in white Didot italic): `P2:12a_arch_notebook_tree_zoom` (`MS DAR 121:36`), `P3:10a_arch_vestiges_1844` (*Vestiges* 1844), `P4:06b_arch_malthus_1798` (Malthus 1798), `P5:05b_arch_origin_1859_title` (*Origin* 1859 1st ed.), `P5:09_arch_darwinism_1889` (*Darwinism* 1889 1st ed.), `P6:04b_arch_mendel_1866_paper` (Mendel 1866)",
        "- **17 verified Public Domain Wikimedia Commons scans & portraits** downloaded in `07_Edit-Project/archive_pulls_v01/ARCHIVE_PULLS_RAW_v01.json` (7 document/lithograph scans + 10 historical portraits for the `WHO` lower-third cards, rendered as framed cut-out overlays in `07_Edit-Project/code_graphics_v01/who_overlays/`).",
        "- **QA (`picture_qa.py` + `polish_gate.py`):** recorded in `07_Edit-Project/code_graphics_v01/picture_qa_v01.txt` (`0` fails, `0` warnings) and `07_Edit-Project/code_graphics_v01/polish_gate_v01.txt` (`0` fails).",
        "",
        "---",
        "",
        "## 4. Row-by-row picture plan v01 (timed to `hos_013_vo_v03a.wav`)",
        "",
    ]

    for pdoc in all_parts:
        s = pdoc["summary"]
        md.append(f"### {pdoc['title']} · `{fmt_t(s['vo_start_s'])}–{fmt_t(s['vo_end_s'])}` (`{s['duration_s']:.2f} s`) · {s['rows']} rows")
        md.append("")
        md.append("| Row | In (`t_s`) | Out (`t_end_s`) | Dur | Route | Teach / Overlay | Shot & Spoken VO | Picture source, path / link & licence, and mint cost |")
        md.append("|---|---:|---:|---:|---|---|---|---|")
        for r in pdoc["plates"]:
            rid = f"`P{s['part']}:{r['id']}`"
            tin = f"`{r['t']}` (`{r['t_s']:.2f}s`)"
            tout = f"`{r['t_end']}` (`{r['t_end_s']:.2f}s`)"
            dur = f"`{r['use_s']:.2f}s`"
            rt = r["flow_model"] or r["route"]
            ov = r.get("side_label") or "—"
            if "teach_overlay" in r and r["teach_overlay"].get("kind"):
                tk = r["teach_overlay"]["kind"]
                if tk == "WHO":
                    ov = f"`WHO: {r['teach_overlay']['line_1']} {r['teach_overlay']['line_2']}`"
                    if r["teach_overlay"].get("when_stamp"):
                        ov += f" + `WHEN: {r['teach_overlay']['when_stamp']}`"
                elif tk in ("DATA", "WHEN", "FACT", "LABEL", "EXPLAINER"):
                    ov = f"`{tk}: {r['teach_overlay'].get('label', ov)}`"
                    if r["teach_overlay"].get("scale"):
                        ov += f" · `SCALE: {r['teach_overlay']['scale']}`"
            vo_snip = r["vo_land"][0] if r["vo_land"] else "*(hold)*"
            if len(vo_snip) > 90:
                vo_snip = vo_snip[:87] + "..."
            shot_col = f"{r['shot_description']} — *\"{vo_snip}\"*"
            md.append(f"| {rid} | {tin} | {tout} | {dur} | {rt} | {ov} | {shot_col} | {r['source_detail']} |")
        md.append("")

    (EDIT / "PICTURE_PLAN_v01.md").write_text("\n".join(md) + "\n")
    (EDIT / "PRICE_REVIEW_v01.md").write_text("\n".join(md[:58]) + "\n")
    if NAS_EDIT.exists():
        shutil.copy2(EDIT / "PICTURE_PLAN_v01.md", NAS_EDIT / "PICTURE_PLAN_v01.md")
        shutil.copy2(EDIT / "PRICE_REVIEW_v01.md", NAS_EDIT / "PRICE_REVIEW_v01.md")


def build_shorts_plan() -> None:
    import sys
    sys.path.insert(0, str(FILM.parents[1] / "00_Brand/Channel-Setup/tools"))
    import hos_build_rule_v02 as R

    shorts_dir = FILM / "10_Shorts"
    stt_base = shorts_dir / "vo_v02/stt"

    short_specs = [
        {
            "id": "Short_A",
            "title": "How Did Darwin Discover Evolution?",
            "air_date": "2026-12-18",
            "vo_file": "10_Shorts/vo_v02/hos_013_short_A_v02.wav",
            "vo_sha256": "9f80fa1c22951b5f7d25b2365fa5d62a58e848898262e6d5365bb2e68047bef8",
            "vo_dur_s": 26.20,
            "hook_caption": "FORGOT THE **LABELS**",
            "single_overlay": {"kind": "WHEN", "text": "LONDON · 1837", "t_in_s": 15.0, "t_out_s": 18.0},
            "promoted_long_banner": {"text": "Evolution: The Letter That Forced Darwin to Publish", "t_in_s": 9.0, "t_out_s": 14.0},
            "plates": [
                "P1:01_study_beaks",
                "P2:02_galapagos_beach_myth",
                "P2:03_unlabelled_bagging",
                "P2:04_blank_tags_row",
                "P1:03a_unlabelled_birds",
                "P2:08a_gould_sorting",
                "P2:09_cg_finch_toolbox",
                "P1:07_darwin_1837_desk",
                "P1:08_cg_i_think_tree",
            ],
        },
        {
            "id": "Short_B",
            "title": "What Is Survival of the Fittest?",
            "air_date": "2026-12-20",
            "vo_file": "10_Shorts/vo_v02/hos_013_short_B_v02.wav",
            "vo_sha256": "6745bd813bd390bdf5091460bd9b5425eca568e4dbb3cf37f2c0a53f70ad47c0",
            "vo_dur_s": 26.00,
            "hook_caption": "NOT THE **STRONGEST**",
            "single_overlay": {"kind": "FACT", "text": "FIT = FITS", "t_in_s": 16.0, "t_out_s": 19.0},
            "promoted_long_banner": {"text": "Evolution: The Letter That Forced Darwin to Publish", "t_in_s": 9.0, "t_out_s": 14.0},
            "plates": [
                "P6:07_key_in_lock",
                "P6:06a_origin_fifth_edition",
                "P6:06b_spencer_coined",
                "P1:09_wallace_hut_split",
                "P5:08b_wallace_reads_origin",
                "P5:05b_arch_origin_1859_title",
                "P3:04b_finch_cracks_seed",
                "P2:09_cg_finch_toolbox",
                "P3:06_nature_keeps_fit",
            ],
        },
    ]

    out_shorts = []
    for sp in short_specs:
        stem = Path(sp["vo_file"]).stem
        wdata = json.loads((stt_base / stem / "words.json").read_text())
        words = [(w["text"], round(float(w["start"]), 3), round(float(w["end"]), 3)) for w in wdata]
        cuts = R.find_word_cuts(words, sp["vo_dur_s"])
        rows = []
        for c, pl in zip(cuts, sp["plates"]):
            is_built_cg = any(
                pl.endswith(x) for x in (
                    "08_cg_i_think_tree", "09_cg_finch_toolbox", "05b_arch_origin_1859_title", "06_nature_keeps_fit"
                )
            )
            pnum = pl.split(":")[0][1:]
            pid = pl.split(":")[1]
            cg_rel = f"07_Edit-Project/code_graphics_v01/code_graphic_013_p{pnum}_{pid}.mp4" if is_built_cg else None
            rows.append({
                **c,
                "source_long_plate": pl,
                "free_built_path": cg_rel,
                "plate_on_disk": is_built_cg,
                "status": "planned_free_built" if is_built_cg else "blocked_missing_plate_parked_for_mint",
                "flow_credits_expected": 0,
            })
        rows.append({
            "id": "loop_tail",
            "t_start_s": sp["vo_dur_s"],
            "t_end_s": round(sp["vo_dur_s"] + 0.60, 3),
            "use_s": 0.60,
            "role": "loop_tail",
            "source_long_plate": sp["plates"][0],
            "plate_on_disk": False,
            "status": "blocked_missing_plate_parked_for_mint",
            "spoken": "",
            "note": "Matched frame-0 plate loop tail (<= 1.0 s, keeps total Short duration <= 27.0 s). Zero extra Flow credits (cut from long's plates).",
        })
        out_shorts.append({
            "id": sp["id"],
            "title": sp["title"],
            "air_date": sp["air_date"],
            "vo_file": sp["vo_file"],
            "vo_sha256": sp["vo_sha256"],
            "vo_dur_s": sp["vo_dur_s"],
            "total_dur_s": round(sp["vo_dur_s"] + 0.60, 2),
            "hook_complete_in_s01": True,
            "hook_sentence_end_s": rows[0]["word_end_s"],
            "hook_caption": sp["hook_caption"],
            "single_overlay": sp["single_overlay"],
            "promoted_long_banner": sp["promoted_long_banner"],
            "flow_credits_try1": 0,
            "flow_credits_expected": 0,
            "rows": rows,
        })

    doc = {
        "film": "013_Darwin-Wallace-Evolution",
        "version": "v01",
        "task": "J2476: HOS 013 Shorts picture plan v01 timed to accepted J2288 Shorts VOs (PR #444). Cut 100% from long plates (0 extra Flow credits).",
        "shorts": out_shorts,
    }
    (shorts_dir / "SHORTS_PICTURE_PLAN_v01.json").write_text(json.dumps(doc, indent=2) + "\n")


if __name__ == "__main__":
    build_boards()
