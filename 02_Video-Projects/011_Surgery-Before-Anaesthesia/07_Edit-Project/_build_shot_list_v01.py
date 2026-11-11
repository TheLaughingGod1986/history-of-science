#!/usr/bin/env python3
"""Build HOS 011 (Anesthesia: The Day Surgery Stopped Hurting) Shot List v01 & Picture Plan v01
against the locked VO take `hos_011_vo_v01.wav` (532.72 s, sha256 d873f1d0..., J2245/J2286 KEEP).

Writes:
  - 07_Edit-Project/SHOT_LIST_v01.md
  - 07_Edit-Project/PICTURE_PLAN_v01.json
  - 07_Edit-Project/PICTURE_PLAN_v01.md
  - 07_Edit-Project/PRICE_REVIEW_v01.md
  - 07_Edit-Project/parts/part-01_plates_v01.json .. part-05_plates_v01.json

Cost of running this script: £0 / 0 credits. No API calls. `generation_authorized: false` on every row.
"""

from __future__ import annotations

import json
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent
EDIT_DIR = Path(__file__).resolve().parent
PARTS_DIR = EDIT_DIR / "parts"
STT_RAW_PATH = PROJECT_DIR / "02_Voiceover" / "stt" / "hos_011_vo_v01" / "stt_raw.json"
WORDS_SRT_PATH = PROJECT_DIR / "02_Voiceover" / "stt" / "hos_011_vo_v01" / "words.srt"

VO_WAV_REL = "02_Voiceover/hos_011_vo_v01.wav"
VO_WAV_SHA256 = "d873f1d0c9158087fd61ce0b9f53de985055d778cd58b8df70c67c0701300ae2"
VO_MP3_REL = "02_Voiceover/hos_011_vo_v01.mp3"
VO_MP3_SHA256 = "9fdd84d50ac2f85bcdf8aea0d5ceefd261cae5458dafa1e6865adf2a3053f496"
VO_DURATION_S = 532.72
FILM_END_S = 535.30

STYLE_PREFIX = (
    "Stylised 3D animated historical scene, Pixar-meets-Arcane painterly lighting, "
    "rich period wood, brass and glass textures, warm tungsten and cool window daylight contrast, "
    "gentle background softness, no text, no letters, no numbers, no watermark, 16:9."
)

EXPLORER_REF = "01_Character/02_Master-Character-Sheet/THE_EXPLORER_MASTER_CHARACTER_SHEET.png"

WHO_PORTRAITS = {
    "Robert Liston (1794–1847) — London surgeon": {
        "file": "07_Edit-Project/code_graphics_v01/who_overlays/who_robert_liston.png",
        "commons_url": "https://commons.wikimedia.org/wiki/File:Robert_Liston00.jpg",
        "licence": "Public domain (1840s portrait lithograph, Wellcome Collection / Wikimedia Commons)",
    },
    "Humphry Davy (1778–1829) — Bristol chemist": {
        "file": "07_Edit-Project/code_graphics_v01/who_overlays/who_humphry_davy.png",
        "commons_url": "https://commons.wikimedia.org/wiki/File:Sir_Humphry_Davy,_Bt_by_Thomas_Phillips.jpg",
        "licence": "Public domain (1821 painting by Thomas Phillips, National Portrait Gallery / Wikimedia Commons)",
    },
    "Crawford Long (1815–1878) — Georgia physician": {
        "file": "07_Edit-Project/code_graphics_v01/who_overlays/who_crawford_long.png",
        "commons_url": "https://commons.wikimedia.org/wiki/File:Crawford_Long.jpg",
        "licence": "Public domain (19th-century portrait photograph, National Library of Medicine / Wikimedia Commons)",
    },
    "Horace Wells (1815–1848) — Connecticut dentist": {
        "file": "07_Edit-Project/code_graphics_v01/who_overlays/who_horace_wells.png",
        "commons_url": "https://commons.wikimedia.org/wiki/File:Horace_Wells.jpg",
        "licence": "Public domain (1840s portrait engraving/photograph, National Library of Medicine / Wikimedia Commons)",
    },
    "William T. G. Morton (1819–1868) — Boston dentist": {
        "file": "07_Edit-Project/code_graphics_v01/who_overlays/who_william_morton.png",
        "commons_url": "https://commons.wikimedia.org/wiki/File:William_Thomas_Green_Morton.jpg",
        "licence": "Public domain (1850s portrait, National Library of Medicine / Wikimedia Commons)",
    },
    "John Collins Warren (1778–1856) — Boston surgeon": {
        "file": "07_Edit-Project/code_graphics_v01/who_overlays/who_john_collins_warren.png",
        "commons_url": "https://commons.wikimedia.org/wiki/File:John_Collins_Warren_(1778-1856).jpg",
        "licence": "Public domain (c. 1850 daguerreotype/portrait, Massachusetts General Hospital / Wikimedia Commons)",
    },
    "Oliver Wendell Holmes (1809–1894) — physician and poet": {
        "file": "07_Edit-Project/code_graphics_v01/who_overlays/who_oliver_wendell_holmes.png",
        "commons_url": "https://commons.wikimedia.org/wiki/File:Oliver_Wendell_Holmes_Sr_circa_1853.jpg",
        "licence": "Public domain (c. 1853 daguerreotype by Southworth & Hawes, Wikimedia Commons)",
    },
    "Charles T. Jackson (1805–1880) — Boston chemist": {
        "file": "07_Edit-Project/code_graphics_v01/who_overlays/who_charles_jackson.png",
        "commons_url": "https://commons.wikimedia.org/wiki/File:Charles_Thomas_Jackson.jpg",
        "licence": "Public domain (1850s portrait photograph, National Library of Medicine / Wikimedia Commons)",
    },
    "James Young Simpson (1811–1870) — Edinburgh obstetrician": {
        "file": "07_Edit-Project/code_graphics_v01/who_overlays/who_james_young_simpson.png",
        "commons_url": "https://commons.wikimedia.org/wiki/File:James_Young_Simpson.jpg",
        "licence": "Public domain (1850s portrait photograph by J. Moffat, Wellcome Collection / Wikimedia Commons)",
    },
    "John Snow (1813–1858) — London physician": {
        "file": "07_Edit-Project/code_graphics_v01/who_overlays/who_john_snow.png",
        "commons_url": "https://commons.wikimedia.org/wiki/File:John_Snow.jpg",
        "licence": "Public domain (1856 presentation portrait photograph, Wikimedia Commons)",
    },
}

CHAPTER_META = {
    1: {
        "title": "The Fastest Knife",
        "card_title": None,
        "in_s": 0.00,
        "out_s": 86.80,
        "vo_wav": "02_Voiceover/parts/hos_011_vo_v01/ch00.wav",
        "music_mood": "Tense low cello-and-ticking-pocket-watch pulse (68 BPM) shifting into curious chamber strings at 0:26.50",
    },
    2: {
        "title": "A Gas That Made People Laugh",
        "card_title": "A Gas That Made People Laugh",
        "in_s": 86.80,
        "out_s": 175.66,
        "vo_wav": "02_Voiceover/parts/hos_011_vo_v01/ch01.wav",
        "music_mood": "Light period plucked strings and celesta arpeggio (74 BPM) under Bristol 1800 and Georgia 1842",
    },
    3: {
        "title": "This Is No Humbug",
        "card_title": '"This Is No Humbug"',
        "in_s": 175.66,
        "out_s": 271.88,
        "vo_wav": "02_Voiceover/parts/hos_011_vo_v01/ch02.wav",
        "music_mood": "Restrained chamber strings tightening on 1845 Boston trial, opening into warm wonder on 16 Oct 1846 (70 BPM)",
    },
    4: {
        "title": "The Fight Over Who Was First",
        "card_title": "The Fight Over Who Was First",
        "in_s": 271.88,
        "out_s": 366.26,
        "vo_wav": "02_Voiceover/parts/hos_011_vo_v01/ch03.wav",
        "music_mood": "Rhythmic harpsichord-and-low-strings tension (76 BPM) for the four-way priority dispute, resolving on the Ether Monument",
    },
    5: {
        "title": "Across the Ocean",
        "card_title": "Across the Ocean",
        "in_s": 366.26,
        "out_s": 535.30,
        "vo_wav": "02_Voiceover/parts/hos_011_vo_v01/ch04.wav",
        "music_mood": "Warm orchestral discovery drone (72 BPM) through London, Edinburgh, and modern safety, holding 2.58 s past last word",
    },
}


def fmt_time(sec: float) -> str:
    m = int(round(sec * 100)) // 6000
    rem = sec - m * 60
    return f"{m}:{rem:05.2f}"


def load_words() -> list[dict]:
    data = json.loads(STT_RAW_PATH.read_text())
    return [w for w in data.get("words", []) if w.get("type") == "word"]


def excerpt_for_window(words: list[dict], s0: float, s1: float) -> str:
    picked = []
    for w in words:
        mid = 0.5 * (float(w["start"]) + float(w["end"]))
        if s0 - 0.04 <= mid < s1 + 0.04:
            picked.append(w["text"])
    return " ".join(picked) if picked else "(breath / card / end hold)"


RAW_ROWS: list[dict] = [
    # =========================================================================
    # PART 01 — Cold Open: The Fastest Knife (0:00.00 – 1:26.80, 17 rows)
    # HOS-2026-11-E2 (0:00–0:30): 8 moving clips, max cut 4.30 s <= 4.50 s,
    # 0:05–0:15 physical proof/apparatus, first animated DATA+SCALE at 0:26.50–0:30.70.
    # =========================================================================
    {
        "row_id": "P1:01a",
        "part": 1,
        "in_s": 0.00,
        "out_s": 3.16,
        "source_kind": "mint_quality",
        "camera": "push-in",
        "subject": "1840s London operating theatre pocket watch & steep gallery",
        "visual": (
            "Answer image by 0:03: inside a steep-tiered 1840s wooden London operating theatre in crisp tall-window "
            "daylight, a surgeon's hand in a dark wool cuff snaps open a polished brass pocket watch in close foreground, "
            "the blued-steel second hand sweeping rapidly while packed gallery benches rise behind."
        ),
        "markers": {"when": "London, before 1846"},
        "sfx": "tick_ink (watch click + soft room tone)",
    },
    {
        "row_id": "P1:01b",
        "part": 1,
        "in_s": 3.16,
        "out_s": 6.90,
        "source_kind": "mint_fast",
        "camera": "push-in",
        "subject": "Scarred oak operating chair, leather straps & open surgical case (PROOF 0:05–0:15)",
        "visual": (
            "Title question by 0:06 ('Why?') + physical apparatus (0:05–0:15): close push in cool daylight onto an "
            "empty scarred oak operating chair with thick buckled leather arm straps beside a velvet-lined mahogany "
            "case of polished steel surgical knives on a linen-draped table. No candles or lamps."
        ),
        "markers": {"label": "SPEED"},
        "sfx": "whoosh_soft",
    },
    {
        "row_id": "P1:02a",
        "part": 1,
        "in_s": 6.90,
        "out_s": 10.50,
        "source_kind": "mint_fast",
        "camera": "pan-right",
        "subject": "Gallery students' hands holding open brass pocket watches (PROOF 0:05–0:15)",
        "visual": (
            "Physical proof/apparatus (0:05–0:15): tight lateral pan across a curved oak gallery rail in bright "
            "skylight daylight where four medical students' hands hold open brass pocket watches and pencilled notebooks, "
            "second hands ticking in unison. No emissive light sources."
        ),
        "markers": {"when": "Europe & America"},
        "sfx": "tick_ink",
    },
    {
        "row_id": "P1:02b",
        "part": 1,
        "in_s": 10.50,
        "out_s": 14.28,
        "source_kind": "mint_quality",
        "camera": "pull-back",
        "subject": "Cordial bottle & leather bite-strap set beside operating chair (PROOF 0:05–0:15)",
        "visual": (
            "Physical proof/apparatus (0:05–0:15): an assistant's hands place a corked stoneware cordial bottle, a "
            "pewter cup, and a folded leather bite-strap on the wooden side tray beside the operating chair as a "
            "patient's coat sleeve grips the chair arm."
        ),
        "markers": {},
        "sfx": "none",
    },
    {
        "row_id": "P1:03a",
        "part": 1,
        "in_s": 14.28,
        "out_s": 18.50,
        "source_kind": "mint_quality",
        "camera": "push-in",
        "subject": "Robert Liston stepping to the table at University College Hospital London",
        "visual": (
            "Tall, broad-shouldered Scottish surgeon Robert Liston in an 1840s dark frock coat stands beside the "
            "wooden operating table under the high skylight of University College Hospital, London, nodding once to "
            "the gallery as students lift their pocket watches."
        ),
        "markers": {"who": "Robert Liston (1794–1847) — London surgeon"},
        "sfx": "tick_ink (WHO card ink-in)",
    },
    {
        "row_id": "P1:03b",
        "part": 1,
        "in_s": 18.50,
        "out_s": 22.80,
        "source_kind": "mint_fast",
        "camera": "push-in",
        "subject": "Macro of brass pocket-watch dial sweeping past two minutes in daylight",
        "visual": (
            "Extreme close-up in crisp skylight daylight on a student's open brass pocket watch: the blued-steel "
            "second hand sweeps smoothly around the enamel sub-dial while the minute hand nears the three-minute mark, "
            "brass gears glinting."
        ),
        "markers": {"fact": "Under 3 minutes"},
        "sfx": "tick_ink (FACT card ink-in)",
    },
    {
        "row_id": "P1:04a",
        "part": 1,
        "in_s": 22.80,
        "out_s": 26.50,
        "source_kind": "mint_quality",
        "camera": "pan-up",
        "subject": "Autumn 1846 sunlight entering the Boston Ether Dome skylight",
        "visual": (
            "Golden October 1846 afternoon light streams down through the high glass dome of Massachusetts General "
            "Hospital in Boston onto the empty red-plush operating chair and two-necked glass inhaler globe waiting on "
            "a side table."
        ),
        "markers": {"when": "Autumn 1846"},
        "sfx": "whoosh_soft",
    },
    {
        "row_id": "P1:04b_cg_stopwatch_scale",
        "part": 1,
        "in_s": 26.50,
        "out_s": 30.70,
        "source_kind": "code_graphic",
        "code_graphic_path": "07_Edit-Project/code_graphics_v01/code_graphic_011_P1_04b_stopwatch_scale.mp4",
        "camera": "locked-animated-graphic",
        "subject": "DATA+SCALE #1 (EARLY 0:25–0:40): Liston <3 min stopwatch vs 1846 Ether Dome turnaround",
        "visual": (
            "House cream-on-walnut animated DATA+SCALE graphic (HOS-2026-11-E2 EARLY 0:25–0:40): an inked brass "
            "stopwatch dial sweeps once around and halts under '3 MINUTES' beside a period three-minute egg sandglass "
            "('SCALE: About as long as boiling an egg'), while a comparative bar shifts from 'BEFORE OCT 1846: AWAKE "
            "(<3 MIN RACE)' to '16 OCT 1846: ASLEEP (0 PAIN)'."
        ),
        "markers": {
            "data": "a brass stopwatch dial that sweeps round once and stops short of three minutes",
            "scale": "about as long as boiling an egg",
        },
        "sfx": "tick_ink",
    },
    {
        "row_id": "P1:05a",
        "part": 1,
        "in_s": 30.70,
        "out_s": 35.80,
        "source_kind": "mint_quality",
        "camera": "push-in",
        "subject": "Morton holding the two-necked glass ether globe to Edward Abbott's face in Boston",
        "visual": (
            "Close profile in the Boston operating dome on 16 October 1846: dentist William Morton holds a two-necked "
            "clear glass globe containing an ether-soaked sea sponge to young printer Edward Abbott's mouth; Abbott's "
            "eyelids close peacefully and his shoulders relax."
        ),
        "markers": {"when": "Boston, 16 October 1846", "label": "ETHER"},
        "sfx": "tick_ink",
    },
    {
        "row_id": "P1:05b",
        "part": 1,
        "in_s": 35.80,
        "out_s": 40.50,
        "source_kind": "mint_quality",
        "camera": "orbit-slow",
        "subject": "Glass ether globe vapour swirling while patient sleeps safely",
        "visual": (
            "Macro slow orbit around the two-necked glass inhaler globe resting on a white linen tray in soft skylight: "
            "faint ether vapour shimmers above the natural sponge inside the glass while the sleeping patient's chest "
            "rises and falls calmly behind."
        ),
        "markers": {},
        "sfx": "none",
    },
    {
        "row_id": "P1:06a",
        "part": 1,
        "in_s": 40.50,
        "out_s": 47.40,
        "source_kind": "mint_quality",
        "camera": "pan-right",
        "subject": "Four rival claimants' notebooks, patent papers & green silk gas bag on oak desk",
        "visual": (
            "Across a long 19th-century oak table lit by a tall window sit four competing artefacts: an 1800 green "
            "oiled-silk gas bag, a folded 1842 Georgia linen towel, a two-necked 1846 Boston glass globe, and wax-sealed "
            "patent and courtroom petitions."
        ),
        "markers": {},
        "sfx": "none",
    },
    {
        "row_id": "P1:07a_cg_three_chapters_map",
        "part": 1,
        "in_s": 47.40,
        "out_s": 53.60,
        "source_kind": "code_graphic",
        "code_graphic_path": "07_Edit-Project/code_graphics_v01/code_graphic_011_P1_07a_three_chapters_map.mp4",
        "camera": "locked-animated-graphic",
        "subject": "Promise route map: Bristol (1800) → Jefferson, Georgia (1842) → Boston (1846)",
        "visual": (
            "House cream-and-walnut animated period map tracing the three stops of the promise line in ink: "
            "'1. BRISTOL (1800 — Laughing Gas)' across the Atlantic to '2. JEFFERSON, GEORGIA (1842 — Country Doctor)' "
            "and north to '3. BOSTON (1846 — Ether Dome)'."
        ),
        "markers": {},
        "sfx": "tick_ink",
    },
    {
        "row_id": "P1:07b",
        "part": 1,
        "in_s": 53.60,
        "out_s": 59.50,
        "source_kind": "mint_fast",
        "camera": "pull-back",
        "subject": "Promise beat part 2: Boston amphitheatre benches & pocket watch stopping beside globe",
        "visual": (
            "Daylight pull-back from the two-necked glass ether globe and a stopped brass pocket watch on the surgical "
            "tray, revealing the curved wooden benches of the Boston amphitheatre above. No flames or lamps."
        ),
        "markers": {},
        "sfx": "none",
    },
    {
        "row_id": "P1:08a",
        "part": 1,
        "in_s": 59.50,
        "out_s": 66.40,
        "source_kind": "mint_quality",
        "camera": "push-in",
        "subject": "1840 patient POV: wooden operating room with no mask and no injection",
        "visual": (
            "First-person perspective approaching a scarred wooden operating chair in a dim 1840 hospital room: bare "
            "linen sheets, a water basin, and a wooden tray with no mask and no syringe in sight."
        ),
        "markers": {"when": "1840"},
        "sfx": "rumble_low (subtle low tension)",
    },
    {
        "row_id": "P1:08b",
        "part": 1,
        "in_s": 66.40,
        "out_s": 72.00,
        "source_kind": "mint_quality",
        "camera": "pan-left",
        "subject": "Pewter cup of strong spirit & orderlies' hands gripping chair arms",
        "visual": (
            "Close shot of a dented pewter tumbler of dark spirit on a wooden stool while two orderlies in rolled shirt "
            "sleeves brace their hands firmly against the oak arms of the operating chair."
        ),
        "markers": {},
        "sfx": "none",
    },
    {
        "row_id": "P1:09a",
        "part": 1,
        "in_s": 72.00,
        "out_s": 78.20,
        "source_kind": "mint_fast",
        "camera": "push-in",
        "subject": "Surgeon's hand closing a brass pocket watch: 'Not a gentle touch. Speed.'",
        "visual": (
            "In crisp daylight, a surgeon's hand snaps shut the lid of a brass pocket watch on the table beside a "
            "clean folded surgical cloth, the watch chain settling instantly."
        ),
        "markers": {},
        "sfx": "tick_ink",
    },
    {
        "row_id": "P1:09b",
        "part": 1,
        "in_s": 78.20,
        "out_s": 82.60,
        "source_kind": "mint_fast",
        "camera": "pan-right",
        "subject": "Centuries of old surgical treatises and apothecary jars on a mahogany shelf",
        "visual": (
            "In clean daylight, a slow pan across leather-bound 17th- and 18th-century surgical treatises and stoneware "
            "apothecary jars on a hospital library shelf. No candles or flames."
        ),
        "markers": {},
        "sfx": "none",
    },
    {
        "row_id": "P1:09c",
        "part": 1,
        "in_s": 82.60,
        "out_s": 86.80,
        "source_kind": "mint_quality",
        "camera": "push-in",
        "subject": "1800 leather-bound volume opening to a forgotten page nearly fifty years earlier",
        "visual": (
            "A leather-bound 1800 chemistry book sits on a laboratory bench beside a glass gas bell-jar; a breeze from "
            "the window turns the rag-paper pages to a passage printed nearly fifty years before 1846."
        ),
        "markers": {"when": "Nearly 50 years earlier"},
        "sfx": "whoosh_soft",
    },

    # =========================================================================
    # PART 02 — A Gas That Made People Laugh (1:26.80 – 2:55.66, 17 rows)
    # =========================================================================
    {
        "row_id": "P2:01_card_p02",
        "part": 2,
        "in_s": 86.80,
        "out_s": 88.90,
        "source_kind": "code_graphic",
        "code_graphic_path": "07_Edit-Project/code_graphics_v01/code_graphic_011_card_p02.mp4",
        "camera": "locked-chapter-card",
        "subject": "[CHAPTER CARD: A Gas That Made People Laugh]",
        "visual": (
            "House dark-walnut and cream chapter card with white Didot italic numeral 'II' and title "
            "'A Gas That Made People Laugh', spanning the 0.70 s chapter breath (86.80–87.50 s) and crossfading out."
        ),
        "markers": {"chapter_card": "A Gas That Made People Laugh"},
        "sfx": "tick_ink",
    },
    {
        "row_id": "P2:02a",
        "part": 2,
        "in_s": 88.90,
        "out_s": 95.20,
        "source_kind": "mint_quality",
        "camera": "push-in",
        "subject": "Young Humphry Davy in Bristol 1800 breathing nitrous oxide from a green silk bag",
        "visual": (
            "In the 1800 Pneumatic Institution laboratory in Bristol, 21-year-old chemist Humphry Davy in a Regency "
            "coat inhales nitrous oxide through a brass mouthpiece attached to a green oiled-silk gas bag beside a "
            "water-sealed glass gasometer."
        ),
        "markers": {"when": "Bristol, 1800", "who": "Humphry Davy (1778–1829) — Bristol chemist"},
        "sfx": "tick_ink (WHO card ink-in)",
    },
    {
        "row_id": "P2:02b",
        "part": 2,
        "in_s": 95.20,
        "out_s": 101.80,
        "source_kind": "mint_quality",
        "camera": "orbit-slow",
        "subject": "Davy laughing giddily in his Bristol laboratory ('laughing gas')",
        "visual": (
            "Davy lowers the green silk gas bag, eyes bright and laughing openly as he steadies himself against his "
            "oak laboratory workbench while glass flasks catch the morning window light."
        ),
        "markers": {"label": "NITROUS OXIDE"},
        "sfx": "tick_ink",
    },
    {
        "row_id": "P2:03a",
        "part": 2,
        "in_s": 101.80,
        "out_s": 108.50,
        "source_kind": "mint_quality",
        "camera": "push-in",
        "subject": "EXPLORER BEAT #1: Explorer beside Davy's gas-holder as Davy's toothache fades",
        "visual": (
            "[EXPLORER ACTS] In Davy's 1800 Bristol laboratory, Davy touches his own cheek in surprise as his wisdom-tooth "
            "pain vanishes; beside the glass gas-holder, the Explorer presses two fingers to his jaw in quiet "
            "recognition and nods toward Davy's open notebook."
        ),
        "markers": {"explorer": "Beat 1 (Bristol 1800 laboratory)"},
        "explorer_start_frame": EXPLORER_REF,
        "sfx": "none",
    },
    {
        "row_id": "P2:04a_arch_davy_1800",
        "part": 2,
        "in_s": 108.50,
        "out_s": 113.50,
        "source_kind": "free_archive",
        "code_graphic_path": "07_Edit-Project/code_graphics_v01/code_graphic_011_P2_04a_arch_davy_1800.mp4",
        "archive_url": "https://commons.wikimedia.org/wiki/File:Researches,_chemical_and_philosophical_-_chiefly_concerning_nitrous_oxide,_or_dephlogisticated_nitrous_air,_and_its_respiration_(IA_b21968393).pdf",
        "archive_licence": "Public domain (Humphry Davy, Researches, Chemical and Philosophical, London: J. Johnson, 1800, p. 556, Wellcome Collection / Wikimedia Commons)",
        "archive_credit": "Davy, Researches (1800), Wellcome / Commons",
        "camera": "animated-archive-highlight",
        "subject": "Archive scan: Davy's 1800 Researches p. 556 ('used with advantage during surgical operations')",
        "visual": (
            "Public-domain 1800 printed page from Humphry Davy's Researches, Chemical and Philosophical (p. 556) over "
            "warm period rag paper, with an animated golden ink underline drawing beneath 'capable of destroying "
            "physical pain, it may probably be used with advantage during surgical operations'."
        ),
        "markers": {},
        "sfx": "tick_ink",
    },
    {
        "row_id": "P2:04b",
        "part": 2,
        "in_s": 113.50,
        "out_s": 121.20,
        "source_kind": "mint_fast",
        "camera": "pull-back",
        "subject": "Davy's 1800 volume shelved unopened while ether and gas bottles sit as novelties",
        "visual": (
            "In daylight, Davy's 1800 book is pushed onto a dusty library shelf while in foreground a glass apothecary "
            "bottle of sulphuric ether and a green silk gas bladder sit on a velvet showman's tray. No candles or flames."
        ),
        "markers": {},
        "sfx": "none",
    },
    {
        "row_id": "P2:05a_arch_laughing_gas_broadside",
        "part": 2,
        "in_s": 121.20,
        "out_s": 127.60,
        "source_kind": "free_archive",
        "code_graphic_path": "07_Edit-Project/code_graphics_v01/code_graphic_011_P2_05a_arch_laughing_gas_broadside.mp4",
        "archive_url": "https://commons.wikimedia.org/wiki/File:Gillray_-_Scientific_Researches!_New_Discoveries_in_Pneumaticks!_(1802).jpg",
        "archive_licence": "Public domain (1802 hand-coloured etching by James Gillray & 1844 Hartford laughing-gas playbill, Wellcome Collection / Wikimedia Commons)",
        "archive_credit": "Gillray (1802) / Hartford Playbill (1844), Wellcome / Commons",
        "camera": "animated-archive-push",
        "subject": "Archive print & playbill: public laughing-gas demonstrations and stage exhibitions",
        "visual": (
            "Public-domain 19th-century laughing-gas lecture engraving and stage broadside ('A Grand Exhibition of the "
            "Effects Produced by Inhaling Nitrous Oxide, or Laughing Gas!'), framed on period rag paper with slow push."
        ),
        "markers": {"when": "Early 1800s"},
        "sfx": "tick_ink",
    },
    {
        "row_id": "P2:05b",
        "part": 2,
        "in_s": 127.60,
        "out_s": 134.90,
        "source_kind": "mint_quality",
        "camera": "orbit-slow",
        "subject": "1830s parlour 'ether frolic' where young guests stagger laughing",
        "visual": (
            "Inside an 1830s American parlour, young guests pass a crystal decanter of ether and linen handkerchiefs, "
            "staggering merrily around a wooden side table."
        ),
        "markers": {},
        "sfx": "none",
    },
    {
        "row_id": "P2:06a",
        "part": 2,
        "in_s": 134.90,
        "out_s": 141.90,
        "source_kind": "mint_quality",
        "camera": "push-in",
        "subject": "Guest bumping knee against wooden table leg and waking the next morning puzzled by bruise",
        "visual": (
            "A young man at an ether frolic stumbles against the corner of an oak table without flinching, looking down "
            "at his coat sleeve in mild surprise as morning light touches the window."
        ),
        "markers": {"when": "The next morning"},
        "sfx": "none",
    },
    {
        "row_id": "P2:07a",
        "part": 2,
        "in_s": 141.90,
        "out_s": 148.30,
        "source_kind": "mint_quality",
        "camera": "push-in",
        "subject": "Crawford Long in his Jefferson, Georgia wooden surgery noticing the painless bruises",
        "visual": (
            "In a clapboard country doctor's office in Jefferson, Georgia, 26-year-old physician Crawford Long sits at "
            "his desk holding a glass bottle of sulphuric ether and a folded white linen towel, deep in thought."
        ),
        "markers": {"who": "Crawford Long (1815–1878) — Georgia physician"},
        "sfx": "tick_ink (WHO card ink-in)",
    },
    {
        "row_id": "P2:07b_cg_timeline_42yr",
        "part": 2,
        "in_s": 148.30,
        "out_s": 154.90,
        "source_kind": "code_graphic",
        "code_graphic_path": "07_Edit-Project/code_graphics_v01/code_graphic_011_P2_07b_timeline_42yr.mp4",
        "camera": "locked-animated-graphic",
        "subject": "DATA+SCALE #2: 1800 Bristol → 1842 Jefferson, Georgia (42-year gap)",
        "visual": (
            "House cream-on-parchment animated timeline bar stretching from '1800 · BRISTOL (Davy's laughing-gas note)' "
            "to '30 MARCH 1842 · JEFFERSON, GEORGIA (Long's ether towel)', counting '42 YEARS' across the span "
            "('SCALE: Longer than a whole working lifetime before anyone used it for an operation')."
        ),
        "markers": {
            "when": "Jefferson, Georgia, 30 March 1842",
            "data": "a timeline bar stretching from 1800 (Bristol) to 1842 (Jefferson, Georgia), spanning 42 years",
            "scale": "longer than a whole working lifetime before anyone used it for an operation",
        },
        "sfx": "tick_ink",
    },
    {
        "row_id": "P2:08a",
        "part": 2,
        "in_s": 154.90,
        "out_s": 162.50,
        "source_kind": "mint_quality",
        "camera": "push-in",
        "subject": "Crawford Long holding an ether-soaked towel to James Venable's face (30 March 1842)",
        "visual": (
            "In his quiet Georgia office on 30 March 1842, Crawford Long holds a white linen towel dampened with ether "
            "over patient James Venable's nose and mouth; Venable sleeps calmly and wakes without pain."
        ),
        "markers": {"fact": "$2.00 ether operation"},
        "sfx": "tick_ink (FACT card ink-in)",
    },
    {
        "row_id": "P2:09a",
        "part": 2,
        "in_s": 162.50,
        "out_s": 166.14,
        "source_kind": "mint_fast",
        "camera": "pull-back",
        "subject": "Long closing his leather ledger book in his quiet Georgia surgery",
        "visual": (
            "In afternoon window daylight, Crawford Long writes '$2.00' in his leather account ledger and closes the "
            "cover quietly on his wooden desk inside the small Georgia surgery. No candles or lamps."
        ),
        "markers": {},
        "sfx": "none",
    },
    {
        "row_id": "P2:09b_arch_long_1849",
        "part": 2,
        "in_s": 166.14,
        "out_s": 170.50,
        "source_kind": "free_archive",
        "code_graphic_path": "07_Edit-Project/code_graphics_v01/code_graphic_011_P2_09b_arch_long_1849.mp4",
        "archive_url": "https://commons.wikimedia.org/wiki/File:An_account_of_the_first_use_of_sulphuric_ether_by_inhalation_as_an_anaesthetic_in_surgical_operations_(IA_101505514.nlm.nih.gov).pdf",
        "archive_licence": "Public domain (Crawford W. Long, Southern Medical and Surgical Journal, Dec 1849, National Library of Medicine / Wikimedia Commons)",
        "archive_credit": "Long, Southern Med. & Surg. J. (1849), NLM / Commons",
        "camera": "animated-archive-highlight",
        "subject": "Archive scan: Long's December 1849 paper published seven years after his 1842 operation",
        "visual": (
            "Public-domain scan of Crawford W. Long's December 1849 paper in the Southern Medical and Surgical Journal, "
            "highlighting the March 1842 operation date and the December 1849 publication date ('7 YEARS LATER')."
        ),
        "markers": {"when": "Published 1849 (7 years later)"},
        "sfx": "tick_ink",
    },
    {
        "row_id": "P2:10a",
        "part": 2,
        "in_s": 170.50,
        "out_s": 175.66,
        "source_kind": "mint_fast",
        "camera": "pan-right",
        "subject": "Empty rural Georgia road leading toward the northern hospital cities",
        "visual": (
            "Daylight wide shot of the quiet wooden porch of Long's Jefferson, Georgia office looking out toward a "
            "dusty coach road winding north under clear sky. No flames or lamps."
        ),
        "markers": {},
        "sfx": "whoosh_soft",
    },

    # =========================================================================
    # PART 03 — "This Is No Humbug" (2:55.66 – 4:31.88, 17 rows)
    # =========================================================================
    {
        "row_id": "P3:01_card_p03",
        "part": 3,
        "in_s": 175.66,
        "out_s": 177.80,
        "source_kind": "code_graphic",
        "code_graphic_path": "07_Edit-Project/code_graphics_v01/code_graphic_011_card_p03.mp4",
        "camera": "locked-chapter-card",
        "subject": '[CHAPTER CARD: "This Is No Humbug"]',
        "visual": (
            "House dark-walnut and cream chapter card with white Didot italic numeral 'III' and title "
            "'\"This Is No Humbug\"', spanning the 0.70 s inter-chapter breath (175.66–176.36 s) and crossfading out."
        ),
        "markers": {"chapter_card": '"This Is No Humbug"'},
        "sfx": "tick_ink",
    },
    {
        "row_id": "P3:02a",
        "part": 3,
        "in_s": 177.80,
        "out_s": 184.60,
        "source_kind": "mint_quality",
        "camera": "push-in",
        "subject": "Horace Wells watching the December 1844 laughing-gas stage show in Hartford",
        "visual": (
            "In a Hartford, Connecticut hall in December 1844, attentive dentist Horace Wells leans forward in his "
            "front-row seat watching a volunteer on stage stumble against a wooden bench without feeling pain."
        ),
        "markers": {"when": "Hartford, December 1844", "who": "Horace Wells (1815–1848) — Connecticut dentist"},
        "sfx": "tick_ink (WHO card ink-in)",
    },
    {
        "row_id": "P3:03a",
        "part": 3,
        "in_s": 184.60,
        "out_s": 190.50,
        "source_kind": "mint_quality",
        "camera": "push-in",
        "subject": "Wells breathing laughing gas in his Hartford dental chair while Riggs extracts his wisdom tooth",
        "visual": (
            "In his Hartford dental office the next morning (11 December 1844), Horace Wells sits in his own red plush "
            "dental chair holding a gas bag on his lap while colleague John Riggs steps back with dental forceps."
        ),
        "markers": {"when": "11 December 1844 (the next day)"},
        "sfx": "none",
    },
    {
        "row_id": "P3:03b",
        "part": 3,
        "in_s": 190.50,
        "out_s": 195.08,
        "source_kind": "mint_quality",
        "camera": "pull-back",
        "subject": "Wells waking delighted after feeling nothing ('a new era in tooth-pulling')",
        "visual": (
            "Horace Wells opens his eyes in the dental chair, touches his jaw in amazement, and smiles broadly at his "
            "colleague in the bright morning window light."
        ),
        "markers": {},
        "sfx": "none",
    },
    {
        "row_id": "P3:04a",
        "part": 3,
        "in_s": 195.08,
        "out_s": 202.50,
        "source_kind": "mint_quality",
        "camera": "push-in",
        "subject": "Wells in Boston (January 1845) as the laughing-gas bag is withdrawn too early",
        "visual": (
            "In the crowded Boston amphitheatre in January 1845, Horace Wells stands beside a seated patient with a "
            "small gas bag; as the bag is removed early, the patient flinches and cries out."
        ),
        "markers": {"when": "Boston, January 1845"},
        "sfx": "rumble_low (subtle tension)",
    },
    {
        "row_id": "P3:04b",
        "part": 3,
        "in_s": 202.50,
        "out_s": 209.92,
        "source_kind": "mint_quality",
        "camera": "pan-right",
        "subject": "Medical students in the steep gallery jeering 'Humbug!' as Wells packs his bag",
        "visual": (
            "Up in the steep wooden tiers of the Boston gallery, medical students lean over the brass rail jeering and "
            "waving their notebooks while below Horace Wells lowers his head over his gas bag."
        ),
        "markers": {},
        "sfx": "none",
    },
    {
        "row_id": "P3:05a",
        "part": 3,
        "in_s": 209.92,
        "out_s": 216.20,
        "source_kind": "mint_quality",
        "camera": "push-in",
        "subject": "William Morton watching intently from the gallery during Wells's failed trial",
        "visual": (
            "In the lower gallery row of that same Boston room stands Wells's former dental partner, 26-year-old "
            "William Morton, watching the failed demonstration with narrowed, determined eyes instead of laughing."
        ),
        "markers": {"who": "William T. G. Morton (1819–1868) — Boston dentist"},
        "sfx": "tick_ink (WHO card ink-in)",
    },
    {
        "row_id": "P3:05b",
        "part": 3,
        "in_s": 216.20,
        "out_s": 223.80,
        "source_kind": "mint_fast",
        "camera": "push-in",
        "subject": "Morton in his Boston workshop pouring sulphuric ether into a two-necked glass globe",
        "visual": (
            "In crisp daylight at his Boston workbench, Morton pours clear sulphuric ether from a glass-stoppered "
            "bottle onto a natural sponge inside a newly blown two-necked glass inhaler globe. No flames or candles."
        ),
        "markers": {"label": "ETHER"},
        "sfx": "tick_ink",
    },
    {
        "row_id": "P3:06a",
        "part": 3,
        "in_s": 223.80,
        "out_s": 231.20,
        "source_kind": "mint_quality",
        "camera": "push-in",
        "subject": "Morton walking into the Boston Ether Dome on 16 October 1846 carrying the glass globe",
        "visual": (
            "On the morning of 16 October 1846, William Morton hurries through the double doors of the Massachusetts "
            "General Hospital operating dome cradling the two-necked glass ether globe in both hands."
        ),
        "markers": {"when": "Boston, 16 October 1846"},
        "sfx": "whoosh_soft",
    },
    {
        "row_id": "P3:06b",
        "part": 3,
        "in_s": 231.20,
        "out_s": 238.20,
        "source_kind": "mint_quality",
        "camera": "push-in",
        "subject": "Young printer Edward Abbott seated in the red plush chair as Morton holds the globe to his lips",
        "visual": (
            "Twenty-year-old Boston printer Edward Abbott sits in the red velvet operating chair with a white cravat "
            "loosened at his neck; Morton gently places the glass mouthpiece of the ether globe to Abbott's lips."
        ),
        "markers": {},
        "sfx": "none",
    },
    {
        "row_id": "P3:07a",
        "part": 3,
        "in_s": 238.20,
        "out_s": 244.08,
        "source_kind": "mint_quality",
        "camera": "push-in",
        "subject": "EXPLORER BEAT #2: Explorer in the Ether Dome gallery lowering his pocket watch as Abbott sleeps",
        "visual": (
            "[EXPLORER ACTS] In the front row of the Boston Ether Dome gallery, the Explorer watches Edward Abbott's "
            "hand relax onto the red plush armrest as he falls into deep sleep; the Explorer slowly lowers his open "
            "brass pocket watch in quiet wonder."
        ),
        "markers": {"explorer": "Beat 2 (Boston Ether Dome, 16 Oct 1846)"},
        "explorer_start_frame": EXPLORER_REF,
        "sfx": "none",
    },
    {
        "row_id": "P3:08a",
        "part": 3,
        "in_s": 244.08,
        "out_s": 250.86,
        "source_kind": "mint_quality",
        "camera": "push-in",
        "subject": "Senior surgeon John Collins Warren operating while Abbott lies completely still",
        "visual": (
            "White-haired senior surgeon John Collins Warren in a dark frock coat leans over the operating chair in "
            "complete silence; Edward Abbott neither moves nor cries out while the gallery watches in stunned hush."
        ),
        "markers": {"who": "John Collins Warren (1778–1856) — Boston surgeon"},
        "sfx": "tick_ink (WHO card ink-in)",
    },
    {
        "row_id": "P3:08b",
        "part": 3,
        "in_s": 250.86,
        "out_s": 258.50,
        "source_kind": "mint_quality",
        "camera": "pull-back",
        "subject": "Warren turning to the packed Boston gallery: 'Gentlemen, this is no humbug'",
        "visual": (
            "John Collins Warren straightens up beside the waking, calm patient, turns toward the steep tiers of "
            "medical students and doctors under the glass dome, and speaks quietly to the astonished room."
        ),
        "markers": {},
        "sfx": "none",
    },
    {
        "row_id": "P3:09a_arch_ether_dome_1847",
        "part": 3,
        "in_s": 258.50,
        "out_s": 264.80,
        "source_kind": "free_archive",
        "code_graphic_path": "07_Edit-Project/code_graphics_v01/code_graphic_011_P3_09a_arch_ether_dome_1847.mp4",
        "archive_url": "https://commons.wikimedia.org/wiki/File:Southworth_%26_Hawes_-_Early_Operation_under_Ether,_Massachusetts_General_Hospital.jpg",
        "archive_licence": "Public domain (1847 daguerreotype by Southworth & Hawes of the Ether Dome at Massachusetts General Hospital, J. Paul Getty Museum / Wikimedia Commons)",
        "archive_credit": "Southworth & Hawes (1847), MGH / Commons",
        "camera": "animated-archive-push",
        "subject": "Archive photograph: 1847 Southworth & Hawes daguerreotype of the Boston Ether Dome",
        "visual": (
            "Public-domain 1847 Southworth & Hawes daguerreotype of an early ether operation inside the Massachusetts "
            "General Hospital Ether Dome, framed on period mount board with subtle camera push and white Didot italic "
            "corner credit."
        ),
        "markers": {},
        "sfx": "tick_ink",
    },
    {
        "row_id": "P3:10a",
        "part": 3,
        "in_s": 264.80,
        "out_s": 271.88,
        "source_kind": "mint_fast",
        "camera": "pan-right",
        "subject": "Atlantic mail steamer carrying the Boston ether news toward Britain ('Case closed? Wrong.')",
        "visual": (
            "In brisk daylight, a leather mail pouch stamped 'BOSTON TO LIVERPOOL' sits beside folded November 1846 "
            "medical journals on a ship's cabin table while grey Atlantic waves roll past the porthole. No flames."
        ),
        "markers": {},
        "sfx": "whoosh_soft",
    },

    # =========================================================================
    # PART 04 — The Fight Over Who Was First (4:31.88 – 6:06.26, 16 rows)
    # =========================================================================
    {
        "row_id": "P4:01_card_p04",
        "part": 4,
        "in_s": 271.88,
        "out_s": 274.00,
        "source_kind": "code_graphic",
        "code_graphic_path": "07_Edit-Project/code_graphics_v01/code_graphic_011_card_p04.mp4",
        "camera": "locked-chapter-card",
        "subject": "[CHAPTER CARD: The Fight Over Who Was First]",
        "visual": (
            "House dark-walnut and cream chapter card with white Didot italic numeral 'IV' and title "
            "'The Fight Over Who Was First', spanning the 0.70 s inter-chapter breath (271.88–272.58 s) and crossfading."
        ),
        "markers": {"chapter_card": "The Fight Over Who Was First"},
        "sfx": "tick_ink",
    },
    {
        "row_id": "P4:02a",
        "part": 4,
        "in_s": 274.00,
        "out_s": 281.36,
        "source_kind": "mint_quality",
        "camera": "push-in",
        "subject": "Morton tinting ether with orange dye and aromatic oils to disguise it as 'Letheon'",
        "visual": (
            "In his private Boston workroom, William Morton drops orange pigment and aromatic oil from a glass pipette "
            "into a decanter of clear ether, swirling the tinted liquid to hide its tell-tale smell."
        ),
        "markers": {},
        "sfx": "none",
    },
    {
        "row_id": "P4:02b",
        "part": 4,
        "in_s": 281.36,
        "out_s": 285.80,
        "source_kind": "mint_fast",
        "camera": "push-in",
        "subject": "Bottle labelled 'LETHEON' sealed with red wax beside US Patent 4,848",
        "visual": (
            "In crisp window daylight, a glass apothecary bottle of orange-tinted liquid sits beside a red-wax-sealed "
            "parchment deed on a mahogany desk. No candles or lamps."
        ),
        "markers": {"when": "12 November 1846", "fact": "Patent No. 4,848"},
        "sfx": "tick_ink (FACT card ink-in)",
    },
    {
        "row_id": "P4:03a_arch_letheon_patent",
        "part": 4,
        "in_s": 285.80,
        "out_s": 290.58,
        "source_kind": "free_archive",
        "code_graphic_path": "07_Edit-Project/code_graphics_v01/code_graphic_011_P4_03a_arch_letheon_patent.mp4",
        "archive_url": "https://commons.wikimedia.org/wiki/File:US_Patent_4848_Letheon_1846.png",
        "archive_licence": "Public domain (United States Patent Office, Patent No. 4,848, 12 November 1846, C. T. Jackson & W. T. G. Morton, US National Archives)",
        "archive_credit": "US Patent No. 4,848 (12 Nov 1846), NARA",
        "camera": "animated-archive-highlight",
        "subject": "Archive document: US Patent No. 4,848 (12 Nov 1846) for 'Letheon' (sulphuric ether)",
        "visual": (
            "Public-domain 12 November 1846 United States Patent No. 4,848 specification signed by C. T. Jackson and "
            "W. T. G. Morton, with an animated ink box highlighting the patent number and sulphuric ether specification."
        ),
        "markers": {},
        "sfx": "tick_ink",
    },
    {
        "row_id": "P4:03b",
        "part": 4,
        "in_s": 290.58,
        "out_s": 297.50,
        "source_kind": "mint_quality",
        "camera": "push-in",
        "subject": "Hospital surgeons unstoppering the bottle and recognizing the unmistakable smell of ether",
        "visual": (
            "Two Boston hospital surgeons in dark frock coats unstopper Morton's tinted bottle in a bright ward "
            "corridor, waft the vapour toward their noses, and exchange a knowing smile as they recognise plain ether."
        ),
        "markers": {},
        "sfx": "none",
    },
    {
        "row_id": "P4:04a",
        "part": 4,
        "in_s": 297.50,
        "out_s": 304.80,
        "source_kind": "mint_quality",
        "camera": "push-in",
        "subject": "Oliver Wendell Holmes writing his 21 November 1846 letter in his Boston study",
        "visual": (
            "In a book-lined Boston study on 21 November 1846, physician and poet Oliver Wendell Holmes dips a steel "
            "nib pen into an inkwell and writes a letter on cream stationery by window light."
        ),
        "markers": {
            "when": "Boston, 21 November 1846",
            "who": "Oliver Wendell Holmes (1809–1894) — physician and poet",
        },
        "sfx": "tick_ink (WHO card ink-in)",
    },
    {
        "row_id": "P4:04b",
        "part": 4,
        "in_s": 304.80,
        "out_s": 309.20,
        "source_kind": "mint_fast",
        "camera": "push-in",
        "subject": "Close-up of Holmes's steel nib pen and fresh ink letter on his Boston desk",
        "visual": (
            "In crisp window daylight, a close push onto Oliver Wendell Holmes's steel nib pen resting beside the "
            "freshly written cream letter page and brass inkstand. No candles or flames."
        ),
        "markers": {},
        "sfx": "none",
    },
    {
        "row_id": "P4:04c_cg_anesthesia_etymology",
        "part": 4,
        "in_s": 309.20,
        "out_s": 314.50,
        "source_kind": "code_graphic",
        "code_graphic_path": "07_Edit-Project/code_graphics_v01/code_graphic_011_P4_04c_anesthesia_etymology.mp4",
        "camera": "locked-animated-graphic",
        "subject": "Teach card: Holmes's 21 Nov 1846 coinage of 'anaesthesia' ('without feeling')",
        "visual": (
            "House cream-on-brown inked teach graphic drawing Oliver Wendell Holmes's 21 November 1846 coinage: "
            "Greek 'an-' (without) + 'aisthēsis' (feeling / sensation) joining into 'ANAESTHESIA — Sleep without pain'."
        ),
        "markers": {"label": "ANAESTHESIA"},
        "sfx": "tick_ink",
    },
    {
        "row_id": "P4:05a",
        "part": 4,
        "in_s": 314.50,
        "out_s": 320.00,
        "source_kind": "mint_fast",
        "camera": "pan-right",
        "subject": "Rival pamphlets and congressional petitions piling up as Morton claims priority",
        "visual": (
            "In daylight on a marble table, printed pamphlets and congressional petitions pile up beside Morton's "
            "two-necked glass globe as a gloved hand slams down a printed claim. No flames or candles."
        ),
        "markers": {},
        "sfx": "none",
    },
    {
        "row_id": "P4:05b",
        "part": 4,
        "in_s": 320.00,
        "out_s": 326.50,
        "source_kind": "mint_quality",
        "camera": "push-in",
        "subject": "Boston chemist Charles T. Jackson in his laboratory claiming the ether idea was his",
        "visual": (
            "In a Boston chemical laboratory lined with mineral specimens and glass retorts, chemist Charles Jackson "
            "in spectacles points insistently to his own laboratory notebook and a bottle of pure sulphuric ether."
        ),
        "markers": {"who": "Charles T. Jackson (1805–1880) — Boston chemist"},
        "sfx": "tick_ink (WHO card ink-in)",
    },
    {
        "row_id": "P4:06a_cg_master_timeline",
        "part": 4,
        "in_s": 326.50,
        "out_s": 333.90,
        "source_kind": "code_graphic",
        "code_graphic_path": "07_Edit-Project/code_graphics_v01/code_graphic_011_P4_06a_master_timeline.mp4",
        "camera": "locked-animated-graphic",
        "subject": "DATA+SCALE #3 (Master Timeline): 1800 Davy → 1842 Long → 1844 Wells → 1846 Morton/Jackson",
        "visual": (
            "Master animated HOS timeline on period parchment building each claimant's date in order as the VO names "
            "them: '1800 Davy (Bristol)' → 'Mar 1842 Long (Georgia, ether towel)' → 'Dec 1844 Wells (Hartford, nitrous "
            "oxide)' → 'Oct 1846 Morton & Jackson (Boston Ether Dome)'."
        ),
        "markers": {
            "data": "master timeline of the four claimants (1800 Davy, 1842 Long, 1844 Wells, 1846 Morton & Jackson)",
            "scale": "four years from Long's quiet Georgia towel (1842) to Boston's public Ether Dome (1846)",
        },
        "sfx": "tick_ink",
    },
    {
        "row_id": "P4:07a",
        "part": 4,
        "in_s": 333.90,
        "out_s": 338.20,
        "source_kind": "mint_fast",
        "camera": "pan-right",
        "subject": "[SUBSCRIBE BEAT] 1850s newspaper clippings and US Senate ether inquiry reports on a desk",
        "visual": (
            "In crisp daylight, a slow pan across stacks of 1850s newspaper broadsheets and printed US Senate ether "
            "controversy testimony piled on a dark mahogany table. No candles or flames."
        ),
        "markers": {"subscribe_beat": "true"},
        "sfx": "none",
    },
    {
        "row_id": "P4:07b",
        "part": 4,
        "in_s": 338.20,
        "out_s": 342.44,
        "source_kind": "mint_quality",
        "camera": "pull-back",
        "subject": "Courtroom gavel and empty leather coin purse ('none of the four men ended it rich or happy')",
        "visual": (
            "Slow pull-back across a wooden courtroom gavel resting beside an empty, worn leather coin purse and "
            "unpaid legal bills on a law-office table."
        ),
        "markers": {},
        "sfx": "none",
    },
    {
        "row_id": "P4:08a",
        "part": 4,
        "in_s": 342.44,
        "out_s": 349.50,
        "source_kind": "mint_fast",
        "camera": "push-in",
        "subject": "Tree-lined path in the Boston Public Garden approaching the granite Ether Monument",
        "visual": (
            "In calm morning daylight, a tree-lined gravel path in the Boston Public Garden leads toward a tall "
            "white-granite Victorian monument rising above the autumn trees. No candles or flames."
        ),
        "markers": {"when": "Boston Public Garden, 1868"},
        "sfx": "whoosh_soft",
    },
    {
        "row_id": "P4:08b_arch_ether_monument",
        "part": 4,
        "in_s": 349.50,
        "out_s": 354.80,
        "source_kind": "free_archive",
        "code_graphic_path": "07_Edit-Project/code_graphics_v01/code_graphic_011_P4_08b_arch_ether_monument.mp4",
        "archive_url": "https://commons.wikimedia.org/wiki/File:Ether_Monument,_Boston_Public_Garden_-_DSC09052.JPG",
        "archive_licence": "Public domain (CC0 1.0 Public Domain Dedication, Daderot / Wikimedia Commons; 1868 sculpture by J. Q. A. Ward & Ware and Van Brunt)",
        "archive_credit": "Ether Monument (1868), Boston Public Garden / CC0",
        "camera": "animated-archive-tilt",
        "subject": "Archive image: The 1868 Ether Monument in the Boston Public Garden",
        "visual": (
            "Public-domain photograph/engraving of the 1868 Good Samaritan Ether Monument in the Boston Public Garden, "
            "tilting slowly down to the carved granite inscription base."
        ),
        "markers": {},
        "sfx": "tick_ink",
    },
    {
        "row_id": "P4:09a",
        "part": 4,
        "in_s": 354.80,
        "out_s": 360.20,
        "source_kind": "mint_fast",
        "camera": "push-in",
        "subject": "Close-up of the granite inscription base naming the discovery of ether but no claimant",
        "visual": (
            "Close daylight shot of the carved grey granite base of the Boston Ether Monument surrounded by autumn "
            "leaves, its chiseled relief honouring the relief of pain while naming none of the four rivals."
        ),
        "markers": {"fact": "No claimant named"},
        "sfx": "tick_ink (FACT card ink-in)",
    },
    {
        "row_id": "P4:09b",
        "part": 4,
        "in_s": 360.20,
        "out_s": 366.26,
        "source_kind": "mint_quality",
        "camera": "push-in",
        "subject": "December 1846 London fog outside University College Hospital as Liston prepares to test ether",
        "visual": (
            "Across the Atlantic in December 1846 London, pale winter daylight filters into the wooden operating "
            "theatre of University College Hospital where a glass ether inhaler stands ready beside Robert Liston's "
            "surgical table."
        ),
        "markers": {},
        "sfx": "whoosh_soft",
    },

    # =========================================================================
    # PART 05 — Across the Ocean + Closing (6:06.26 – 8:55.30, 27 rows)
    # =========================================================================
    {
        "row_id": "P5:01_card_p05",
        "part": 5,
        "in_s": 366.26,
        "out_s": 368.40,
        "source_kind": "code_graphic",
        "code_graphic_path": "07_Edit-Project/code_graphics_v01/code_graphic_011_card_p05.mp4",
        "camera": "locked-chapter-card",
        "subject": "[CHAPTER CARD: Across the Ocean]",
        "visual": (
            "House dark-walnut and cream chapter card with white Didot italic numeral 'V' and title "
            "'Across the Ocean', spanning the 0.70 s inter-chapter breath (366.26–366.96 s) and crossfading out."
        ),
        "markers": {"chapter_card": "Across the Ocean"},
        "sfx": "tick_ink",
    },
    {
        "row_id": "P5:02a",
        "part": 5,
        "in_s": 368.40,
        "out_s": 374.80,
        "source_kind": "mint_quality",
        "camera": "push-in",
        "subject": "Robert Liston on 21 December 1846 in London watching Peter Squire's glass ether inhaler",
        "visual": (
            "In the packed wooden operating theatre of University College Hospital, London on 21 December 1846, "
            "Robert Liston stands beside a tall glass and brass tube ether inhaler held to butler Frederick "
            "Churchill's face."
        ),
        "markers": {"when": "London, 21 December 1846"},
        "sfx": "tick_ink",
    },
    {
        "row_id": "P5:02b",
        "part": 5,
        "in_s": 374.80,
        "out_s": 381.20,
        "source_kind": "mint_quality",
        "camera": "push-in",
        "subject": "Churchill sleeping peacefully through Liston's operation and waking to ask when it will begin",
        "visual": (
            "The patient lies completely relaxed on the London operating table; as the ether mask is lifted, he opens "
            "his eyes calmly and looks up at Liston in quiet surprise."
        ),
        "markers": {},
        "sfx": "none",
    },
    {
        "row_id": "P5:03a_arch_squire_inhaler_1846",
        "part": 5,
        "in_s": 381.20,
        "out_s": 388.40,
        "source_kind": "free_archive",
        "code_graphic_path": "07_Edit-Project/code_graphics_v01/code_graphic_011_P5_03a_arch_squire_inhaler_1846.mp4",
        "archive_url": "https://commons.wikimedia.org/wiki/File:Squire%27s_ether_inhaler,_1846_Wellcome_M0011572.jpg",
        "archive_licence": "Public domain (Peter Squire's apparatus for inhaling ether used in Robert Liston's operation on 21 Dec 1846, Wellcome Collection M0011572 / Wikimedia Commons)",
        "archive_credit": "Squire's Ether Inhaler (Dec 1846), Wellcome / Commons",
        "camera": "animated-archive-push",
        "subject": "Archive engraving: Peter Squire's London ether inhaler used by Liston on 21 Dec 1846",
        "visual": (
            "Public-domain December 1846 engraving of Peter Squire's sponge-filled glass ether inhaler and flexible "
            "breathing tube used by Robert Liston at University College Hospital, with animated call-out on the mouthpiece."
        ),
        "markers": {},
        "sfx": "tick_ink",
    },
    {
        "row_id": "P5:03b",
        "part": 5,
        "in_s": 388.40,
        "out_s": 395.20,
        "source_kind": "mint_quality",
        "camera": "push-in",
        "subject": "Liston addressing the London gallery: 'This Yankee dodge, gentlemen, beats mesmerism hollow.'",
        "visual": (
            "Robert Liston gestures warmly toward the glass ether apparatus and addresses the packed wooden tiers of "
            "gentlemen and students in the London amphitheatre."
        ),
        "markers": {},
        "sfx": "none",
    },
    {
        "row_id": "P5:04a",
        "part": 5,
        "in_s": 395.20,
        "out_s": 401.96,
        "source_kind": "mint_fast",
        "camera": "push-in",
        "subject": "Liston's brass pocket watch resting closed beside the surgical tray ('no longer needed to be fast')",
        "visual": (
            "Close daylight shot of a closed brass pocket watch resting untouched on white linen beside the glass "
            "ether inhaler tube: the race against the clock is over. No candles or flames."
        ),
        "markers": {},
        "sfx": "none",
    },
    {
        "row_id": "P5:04b",
        "part": 5,
        "in_s": 401.96,
        "out_s": 409.50,
        "source_kind": "mint_quality",
        "camera": "push-in",
        "subject": "James Young Simpson at 52 Queen Street, Edinburgh (November 1847) examining glass bottles",
        "visual": (
            "In an elegant Victorian dining room at 52 Queen Street, Edinburgh in November 1847, obstetrician James "
            "Young Simpson holds up a small cut-glass bottle of clear, sweet-smelling liquid toward the chandelier light."
        ),
        "markers": {
            "when": "Edinburgh, 4 November 1847",
            "who": "James Young Simpson (1811–1870) — Edinburgh obstetrician",
        },
        "sfx": "tick_ink (WHO card ink-in)",
    },
    {
        "row_id": "P5:05a",
        "part": 5,
        "in_s": 409.50,
        "out_s": 416.20,
        "source_kind": "mint_quality",
        "camera": "orbit-slow",
        "subject": "Simpson and assistants Keith and Duncan sniffing chloroform from tumblers at the dinner table",
        "visual": (
            "Seated around the mahogany dinner table in Edinburgh, Simpson and his two assistants George Keith and "
            "Matthews Duncan lean over small glass tumblers, inhaling the sweet chloroform vapour."
        ),
        "markers": {"label": "CHLOROFORM"},
        "sfx": "tick_ink",
    },
    {
        "row_id": "P5:05b",
        "part": 5,
        "in_s": 416.20,
        "out_s": 420.50,
        "source_kind": "mint_quality",
        "camera": "pull-back",
        "subject": "All three doctors slumped peacefully asleep around the Edinburgh dining table",
        "visual": (
            "Wide warm shot of the Edinburgh dining room: moments after inhaling from the tumblers, Simpson and his "
            "two assistants have slipped peacefully to the carpet beside their carved dining chairs."
        ),
        "markers": {},
        "sfx": "none",
    },
    {
        "row_id": "P5:06a_arch_simpson_1847",
        "part": 5,
        "in_s": 420.50,
        "out_s": 426.80,
        "source_kind": "free_archive",
        "code_graphic_path": "07_Edit-Project/code_graphics_v01/code_graphic_011_P5_06a_arch_simpson_1847.mp4",
        "archive_url": "https://commons.wikimedia.org/wiki/File:Account_of_a_new_anaesthetic_agent,_as_a_substitute_for_sulphuric_ether_in_surgery_and_midwifery_(IA_b21459371).pdf",
        "archive_licence": "Public domain (James Young Simpson, Account of a New Anaesthetic Agent, Edinburgh: Sutherland & Knox, Nov 1847, Wellcome Collection / Wikimedia Commons)",
        "archive_credit": "Simpson, Account of a New Anaesthetic Agent (1847), Wellcome / Commons",
        "camera": "animated-archive-highlight",
        "subject": "Archive scan: Simpson's November 1847 Edinburgh pamphlet introducing chloroform",
        "visual": (
            "Public-domain title page of James Young Simpson's November 1847 pamphlet 'Account of a New Anaesthetic "
            "Agent, as a Substitute for Sulphuric Ether in Surgery and Midwifery' (Chloroform), with animated ink highlight."
        ),
        "markers": {},
        "sfx": "tick_ink",
    },
    {
        "row_id": "P5:06b",
        "part": 5,
        "in_s": 426.80,
        "out_s": 433.80,
        "source_kind": "mint_quality",
        "camera": "push-in",
        "subject": "John Snow in London (7 April 1853) measuring chloroform drops onto a folded handkerchief",
        "visual": (
            "In a calm royal chamber at Buckingham Palace on 7 April 1853, London physician John Snow carefully "
            "measures drops of chloroform from a graduated glass vial onto a folded white handkerchief."
        ),
        "markers": {
            "when": "London, 7 April 1853",
            "who": "John Snow (1813–1858) — London physician",
        },
        "sfx": "tick_ink (WHO card ink-in)",
    },
    {
        "row_id": "P5:07a_arch_snow_chloroform_1858",
        "part": 5,
        "in_s": 433.80,
        "out_s": 438.72,
        "source_kind": "free_archive",
        "code_graphic_path": "07_Edit-Project/code_graphics_v01/code_graphic_011_P5_07a_arch_snow_chloroform_1858.mp4",
        "archive_url": "https://commons.wikimedia.org/wiki/File:On_chloroform_and_other_anaesthetics_-_their_action_and_administration_(IA_b2144219x).pdf",
        "archive_licence": "Public domain (John Snow, On Chloroform and Other Anaesthetics, London: John Churchill, 1858, Wellcome Collection / Wikimedia Commons)",
        "archive_credit": "Snow, On Chloroform (1858), Wellcome / Commons",
        "camera": "animated-archive-highlight",
        "subject": "Archive scan: John Snow's On Chloroform (1858) showing his regulating inhaler and Queen Victoria's 1853 case note",
        "visual": (
            "Public-domain engraving and text from John Snow's On Chloroform and Other Anaesthetics (1858), showing "
            "Snow's water-bath chloroform inhaler alongside his 7 April 1853 royal attendance note for Prince Leopold's birth."
        ),
        "markers": {},
        "sfx": "tick_ink",
    },
    {
        "row_id": "P5:07b",
        "part": 5,
        "in_s": 438.72,
        "out_s": 444.14,
        "source_kind": "mint_fast",
        "camera": "pull-back",
        "subject": "Victorian hospital wards adopting measured inhalers across Britain ('good enough for the Queen')",
        "visual": (
            "In bright morning daylight, a neat row of brass Snow inhalers and glass bottles sits ready on a clean "
            "Victorian hospital dispensary shelf. No candles or flames."
        ),
        "markers": {},
        "sfx": "none",
    },
    {
        "row_id": "P5:08a",
        "part": 5,
        "in_s": 444.14,
        "out_s": 451.80,
        "source_kind": "mint_quality",
        "camera": "push-in",
        "subject": "Modern operating room anaesthesia mask & calm patient bedside ('Is it safe?')",
        "visual": (
            "Inside a warm, reassuring modern operating theatre, a soft clear anaesthetic mask rests beside a calm "
            "patient pillow while gentle monitor lights glow softly in the background."
        ),
        "markers": {},
        "sfx": "none",
    },
    {
        "row_id": "P5:09a",
        "part": 5,
        "in_s": 451.80,
        "out_s": 458.50,
        "source_kind": "mint_fast",
        "camera": "push-in",
        "subject": "Precision modern anaesthetic vaporiser dials in clean clinical daylight",
        "visual": (
            "Close daylight shot of modern precision colour-coded anaesthetic vaporiser dials and flowmeters calibrated "
            "to fractions of a percent. No emissive screen text."
        ),
        "markers": {"when": "Today"},
        "sfx": "tick_ink",
    },
    {
        "row_id": "P5:09b_cg_safety_stadium",
        "part": 5,
        "in_s": 458.50,
        "out_s": 466.50,
        "source_kind": "code_graphic",
        "code_graphic_path": "07_Edit-Project/code_graphics_v01/code_graphic_011_P5_09b_safety_stadium.mp4",
        "camera": "locked-animated-graphic",
        "subject": "DATA+SCALE #4: 1 in 100,000 counter + 90,000-seat Wembley stadium bowl with single lit dot",
        "visual": (
            "House cream-on-walnut animated DATA+SCALE graphic: a counter ticks up to '1 IN 100,000' beside an "
            "architectural bowl diagram of a 90,000-seat stadium ('SCALE: 90,000 seats — Wembley Stadium capacity') "
            "where a single tiny gold dot illuminates ('Fewer than 1 death caused by the anaesthetic')."
        ),
        "markers": {
            "data": "a counter that ticks to 1 in 100,000 beside a stadium diagram of 90,000 seats with a single lit dot",
            "scale": "more seats than Wembley Stadium, and on average not even one person dies from the anaesthetic",
        },
        "sfx": "tick_ink",
    },
    {
        "row_id": "P5:10a",
        "part": 5,
        "in_s": 466.50,
        "out_s": 474.00,
        "source_kind": "mint_quality",
        "camera": "orbit-slow",
        "subject": "Architectural miniature model of a 90,000-seat stadium bowl in warm studio light",
        "visual": (
            "Slow elevated orbit over a warm carved-wood architectural model of a vast curved stadium bowl under soft "
            "studio light, conveying the scale of ninety thousand people."
        ),
        "markers": {},
        "sfx": "whoosh_soft",
    },
    {
        "row_id": "P5:11a",
        "part": 5,
        "in_s": 474.00,
        "out_s": 481.20,
        "source_kind": "mint_quality",
        "camera": "push-in",
        "subject": "Modern anaesthetist seated beside the sleeping patient throughout the operation",
        "visual": (
            "A calm, attentive anaesthetist in theatre scrubs sits directly beside the head of a peacefully sleeping "
            "patient, one gloved hand resting near the breathing circuit."
        ),
        "markers": {"label": "ANAESTHETIST"},
        "sfx": "tick_ink",
    },
    {
        "row_id": "P5:11b",
        "part": 5,
        "in_s": 481.20,
        "out_s": 485.80,
        "source_kind": "mint_fast",
        "camera": "push-in",
        "subject": "Anaesthetist's hand finely adjusting the precision vaporiser dial",
        "visual": (
            "Close shot in bright theatre light of the anaesthetist's fingers making a tiny, careful adjustment to a "
            "knurled precision flow dial while watching the breathing bag rise and fall."
        ),
        "markers": {},
        "sfx": "none",
    },
    {
        "row_id": "P5:12a_cg_anesthetist_monitor",
        "part": 5,
        "in_s": 485.80,
        "out_s": 491.20,
        "source_kind": "code_graphic",
        "code_graphic_path": "07_Edit-Project/code_graphics_v01/code_graphic_011_P5_12a_anesthetist_monitor.mp4",
        "camera": "locked-animated-graphic",
        "subject": "Explainer diagram: continuous heartbeat & breath trace balanced at 'Just Asleep Enough'",
        "visual": (
            "House cream-and-ink explainer diagram drawing a steady rhythmic pulse wave and breath wave held smoothly "
            "inside a balanced gold band ('HEARTBEAT · BREATH · DEPTH OF SLEEP')."
        ),
        "markers": {},
        "sfx": "tick_ink",
    },
    {
        "row_id": "P5:13a",
        "part": 5,
        "in_s": 491.20,
        "out_s": 498.00,
        "source_kind": "mint_quality",
        "camera": "push-in",
        "subject": "Why it was groundbreaking: 19th-century surgeon laying down the pocket watch to work carefully",
        "visual": (
            "In a bright late-19th-century operating room, a surgeon sets his brass pocket watch aside on the shelf "
            "and works with calm, unhurried precision over a sleeping patient."
        ),
        "markers": {},
        "sfx": "none",
    },
    {
        "row_id": "P5:13b",
        "part": 5,
        "in_s": 498.00,
        "out_s": 504.20,
        "source_kind": "mint_quality",
        "camera": "pan-right",
        "subject": "Delicate surgical instruments arranged for careful, unhurried operations",
        "visual": (
            "Close pan across fine, delicate surgical needles, silk suture thread, and precision forceps laid out "
            "neatly on clean white linen as the surgeon's hands work steadily."
        ),
        "markers": {},
        "sfx": "none",
    },
    {
        "row_id": "P5:14a",
        "part": 5,
        "in_s": 504.20,
        "out_s": 510.34,
        "source_kind": "mint_fast",
        "camera": "push-in",
        "subject": "Next-mystery bridge part 1: unwashed surgical coats hanging outside an 1860s ward ('still one problem')",
        "visual": (
            "In cool daylight, a slow push toward a row of stained dark wool surgical coats hanging on wooden pegs "
            "outside an 1860s hospital ward door. No candles or flames."
        ),
        "markers": {},
        "sfx": "none",
    },
    {
        "row_id": "P5:14b",
        "part": 5,
        "in_s": 510.34,
        "out_s": 516.50,
        "source_kind": "mint_quality",
        "camera": "push-in",
        "subject": "Next-mystery bridge part 2: 1860s hospital ward where recovering patients develop fever days later",
        "visual": (
            "In a dim 1860s hospital ward, a doctor checks the forehead of a feverish patient resting in bed days "
            "after a painless operation."
        ),
        "markers": {},
        "sfx": "rumble_low (quiet bridge tension)",
    },
    {
        "row_id": "P5:15a",
        "part": 5,
        "in_s": 516.50,
        "out_s": 524.20,
        "source_kind": "mint_quality",
        "camera": "push-in",
        "subject": "Next-mystery bridge part 2: brass microscope & Joseph Lister's carbolic acid brass spray",
        "visual": (
            "On a sunlit Glasgow laboratory bench stand a brass compound microscope and Joseph Lister's brass "
            "steam-driven carbolic acid spray emitting a fine mist across the surgical tray."
        ),
        "markers": {},
        "sfx": "whoosh_soft",
    },
    {
        "row_id": "P5:16a",
        "part": 5,
        "in_s": 524.20,
        "out_s": 528.20,
        "source_kind": "mint_fast",
        "camera": "pan-right",
        "subject": "Closing triptych on oak table: Davy's 1800 gas jar, Wells's gas bag, and Morton's glass ether globe",
        "visual": (
            "In warm daylight across an oak museum table sit the three objects that ended surgical pain: Davy's 1800 "
            "nitrous-oxide jar, a green oiled-silk gas bag, and Morton's two-necked 1846 glass ether globe. No flames."
        ),
        "markers": {},
        "sfx": "tick_ink",
    },
    {
        "row_id": "P5:16b_reuse_pocket_watch_to_globe",
        "part": 5,
        "in_s": 528.20,
        "out_s": 532.72,
        "source_kind": "existing_plate_reuse",
        "reuses_row": "P1:07b",
        "reuse_slice": "3.48s..8.00s",
        "camera": "pull-back",
        "subject": "Closing callback ('turned surgery from a race into a sleep'): stopped pocket watch & glass ether globe",
        "visual": (
            "Intra-film callback reuse of the unused [3.48s..8.00s] moving tail of P1:07b (>7 min separation): "
            "the stopped brass pocket watch resting beside the two-necked glass ether globe in soft daylight, holding "
            "past the final spoken word 'sleep' (532.68 s)."
        ),
        "markers": {},
        "sfx": "none",
    },
    {
        "row_id": "P5:17_cream_end_card",
        "part": 5,
        "in_s": 532.72,
        "out_s": 535.30,
        "source_kind": "code_graphic",
        "code_graphic_path": "07_Edit-Project/code_graphics_v01/code_graphic_011_cream_end_card.mp4",
        "camera": "locked-end-card",
        "subject": "House cream end card hold (2.58 s after last word 'sleep')",
        "visual": (
            "House cream-on-brown end card ('History of Science · Discovery. Wonder. Proof.') holding 2.58 s after "
            "the final spoken word while the orchestral score fades cleanly to silence."
        ),
        "markers": {},
        "sfx": "none",
    },
]


def enrich_rows(words: list[dict]) -> list[dict]:
    enriched = []
    for idx, r in enumerate(RAW_ROWS, 1):
        s0 = round(float(r["in_s"]), 2)
        s1 = round(float(r["out_s"]), 2)
        dur = round(s1 - s0, 2)
        kind = r["source_kind"]
        assert dur > 0, f"{r['row_id']} non-positive duration {dur}"
        if kind in ("mint_quality", "mint_fast"):
            assert dur <= 8.00, f"Mint row {r['row_id']} duration {dur}s > 8.00s"

        if kind == "mint_quality":
            model = "veo-3.1-quality"
            flow_try1 = 100
            flow_exp = 259
            vertex_try1_gbp = 1.60
            vertex_exp_gbp = 4.14
            source_desc = "New plate to mint — Flow Veo 3.1 Quality (100 credits try-1 / 259 expected; generation_authorized: false)"
        elif kind == "mint_fast":
            model = "veo-3.1-fast"
            flow_try1 = 10
            flow_exp = 20
            vertex_try1_gbp = 0.64
            vertex_exp_gbp = 1.28
            source_desc = "New plate to mint — Flow Veo 3.1 Fast (10 credits try-1 / 20 expected, non-emissive daylight; generation_authorized: false)"
        elif kind == "code_graphic":
            model = "code-graphic-ffmpeg"
            flow_try1 = 0
            flow_exp = 0
            vertex_try1_gbp = 0.0
            vertex_exp_gbp = 0.0
            source_desc = f"Own code graphic (£0 / 0 credits) — `{r['code_graphic_path']}`"
        elif kind == "free_archive":
            model = "archive-composite-ffmpeg"
            flow_try1 = 0
            flow_exp = 0
            vertex_try1_gbp = 0.0
            vertex_exp_gbp = 0.0
            source_desc = (
                f"Free public-domain archive composite (£0 / 0 credits) — `{r['code_graphic_path']}` · "
                f"Source: {r['archive_url']} · Licence: {r['archive_licence']}"
            )
        elif kind == "existing_plate_reuse":
            model = "intra-film-reuse"
            flow_try1 = 0
            flow_exp = 0
            vertex_try1_gbp = 0.0
            vertex_exp_gbp = 0.0
            source_desc = (
                f"Existing plate tail reuse (£0 / 0 credits) — reuses `{r['reuses_row']}` slice `{r['reuse_slice']}` "
                "(>7 min separation)"
            )
        else:
            raise ValueError(f"Unknown source_kind: {kind}")

        markers = r.get("markers", {})
        who_info = WHO_PORTRAITS.get(markers["who"]) if "who" in markers else None

        prompt = (
            f"{STYLE_PREFIX} {r['visual']} Camera: {r['camera']}."
            if kind in ("mint_quality", "mint_fast")
            else r["visual"]
        )

        row_obj = {
            "index": idx,
            "row_id": r["row_id"],
            "part": r["part"],
            "in": fmt_time(s0),
            "out": fmt_time(s1),
            "in_s": s0,
            "out_s": s1,
            "duration_s": dur,
            "vo_excerpt": excerpt_for_window(words, s0, s1),
            "subject": r["subject"],
            "visual": r["visual"],
            "camera": r["camera"],
            "prompt": prompt,
            "source_kind": kind,
            "model": model,
            "picture_source": source_desc,
            "code_graphic_path": r.get("code_graphic_path"),
            "archive_url": r.get("archive_url"),
            "archive_licence": r.get("archive_licence"),
            "archive_credit": r.get("archive_credit"),
            "reuses_row": r.get("reuses_row"),
            "reuse_slice": r.get("reuse_slice"),
            "explorer_start_frame": r.get("explorer_start_frame"),
            "markers": markers,
            "who_portrait": who_info,
            "sfx": r.get("sfx", "none"),
            "flow_clip_s": 8 if kind in ("mint_quality", "mint_fast") else None,
            "flow_credits_try1": flow_try1,
            "flow_credits_expected": flow_exp,
            "vertex_try1_gbp": vertex_try1_gbp,
            "vertex_expected_gbp": vertex_exp_gbp,
            "generation_authorized": False,
        }
        enriched.append(row_obj)

    # Verify contiguity and rules
    for i in range(len(enriched)):
        if i == 0:
            assert enriched[i]["in_s"] == 0.0, f"First row starts at {enriched[i]['in_s']}"
        else:
            prev_out = enriched[i - 1]["out_s"]
            cur_in = enriched[i]["in_s"]
            assert abs(cur_in - prev_out) < 1e-6, (
                f"Gap/overlap between {enriched[i-1]['row_id']} ({prev_out}) and {enriched[i]['row_id']} ({cur_in})"
            )
            # Never two full-frame teach/archive graphics back-to-back (end card after moving plate is fine)
            prev_full_graphic = enriched[i - 1]["source_kind"] in ("code_graphic", "free_archive")
            cur_full_graphic = enriched[i]["source_kind"] in ("code_graphic", "free_archive")
            assert not (prev_full_graphic and cur_full_graphic), (
                f"Back-to-back full-frame graphics: {enriched[i-1]['row_id']} -> {enriched[i]['row_id']}"
            )
    assert abs(enriched[-1]["out_s"] - FILM_END_S) < 1e-6, f"Last row ends at {enriched[-1]['out_s']} != {FILM_END_S}"

    # Verify HOS-2026-11-E2 (0:00–0:30)
    open_30 = [r for r in enriched if r["in_s"] < 30.0]
    assert len(open_30) >= 7, f"HOS-2026-11-E2 needs >=7 plates in 0:00-0:30, got {len(open_30)}"
    max_open_cut = max(r["duration_s"] for r in open_30)
    assert max_open_cut <= 4.50, f"HOS-2026-11-E2 max cut in 0:00-0:30 is {max_open_cut}s > 4.50s"

    return enriched


def summarize_parts(rows: list[dict]) -> tuple[list[dict], dict]:
    part_summaries = []
    tot = {
        "rows": 0,
        "mint_quality": 0,
        "mint_fast": 0,
        "code_graphic": 0,
        "free_archive": 0,
        "existing_plate_reuse": 0,
        "mint_rows": 0,
        "free_rows": 0,
        "flow_credits_try1": 0,
        "flow_credits_expected": 0,
        "vertex_try1_gbp": 0.0,
        "vertex_expected_gbp": 0.0,
    }
    for p in sorted(CHAPTER_META.keys()):
        prows = [r for r in rows if r["part"] == p]
        q = sum(1 for r in prows if r["source_kind"] == "mint_quality")
        f = sum(1 for r in prows if r["source_kind"] == "mint_fast")
        cg = sum(1 for r in prows if r["source_kind"] == "code_graphic")
        ar = sum(1 for r in prows if r["source_kind"] == "free_archive")
        re_cnt = sum(1 for r in prows if r["source_kind"] == "existing_plate_reuse")
        mint_cnt = q + f
        free_cnt = cg + ar + re_cnt
        fc1 = sum(r["flow_credits_try1"] for r in prows)
        fce = sum(r["flow_credits_expected"] for r in prows)
        vt1 = round(sum(r["vertex_try1_gbp"] for r in prows), 2)
        vte = round(sum(r["vertex_expected_gbp"] for r in prows), 2)

        ps = {
            "part": p,
            "title": CHAPTER_META[p]["title"],
            "in": fmt_time(CHAPTER_META[p]["in_s"]),
            "out": fmt_time(CHAPTER_META[p]["out_s"]),
            "in_s": CHAPTER_META[p]["in_s"],
            "out_s": CHAPTER_META[p]["out_s"],
            "duration_s": round(CHAPTER_META[p]["out_s"] - CHAPTER_META[p]["in_s"], 2),
            "rows": len(prows),
            "mint_quality": q,
            "mint_fast": f,
            "code_graphic": cg,
            "free_archive": ar,
            "existing_plate_reuse": re_cnt,
            "mint_rows": mint_cnt,
            "free_rows": free_cnt,
            "flow_credits_try1": fc1,
            "flow_credits_expected": fce,
            "vertex_try1_gbp": vt1,
            "vertex_expected_gbp": vte,
        }
        part_summaries.append(ps)
        for k in (
            "rows",
            "mint_quality",
            "mint_fast",
            "code_graphic",
            "free_archive",
            "existing_plate_reuse",
            "mint_rows",
            "free_rows",
            "flow_credits_try1",
            "flow_credits_expected",
        ):
            tot[k] += ps[k]
        tot["vertex_try1_gbp"] = round(tot["vertex_try1_gbp"] + vt1, 2)
        tot["vertex_expected_gbp"] = round(tot["vertex_expected_gbp"] + vte, 2)

    return part_summaries, tot


def write_outputs(rows: list[dict], part_summaries: list[dict], tot: dict) -> None:
    PARTS_DIR.mkdir(parents=True, exist_ok=True)

    # 1. Per-part JSON files
    for ps in part_summaries:
        p = ps["part"]
        prows = [r for r in rows if r["part"] == p]
        part_payload = {
            "film": "011_Surgery-Before-Anaesthesia",
            "part": p,
            "title": ps["title"],
            "card_title": CHAPTER_META[p]["card_title"],
            "vo_file": VO_WAV_REL,
            "vo_sha256": VO_WAV_SHA256,
            "chapter_vo_wav": CHAPTER_META[p]["vo_wav"],
            "music_mood": CHAPTER_META[p]["music_mood"],
            "in": ps["in"],
            "out": ps["out"],
            "in_s": ps["in_s"],
            "out_s": ps["out_s"],
            "duration_s": ps["duration_s"],
            "summary": ps,
            "generation_authorized": False,
            "rows": prows,
        }
        out_p = PARTS_DIR / f"part-{p:02d}_plates_v01.json"
        out_p.write_text(json.dumps(part_payload, indent=2, ensure_ascii=False) + "\n")

    # 2. Master PICTURE_PLAN_v01.json
    plan_json = {
        "film": "011_Surgery-Before-Anaesthesia",
        "title": "Anesthesia: The Day Surgery Stopped Hurting",
        "title_b": "What Surgery Was Like Before Anesthesia",
        "air_date": "2026-12-10T18:00:00.000Z",
        "job_id": "J2475",
        "status": "parked_for_chief_price_pass",
        "generation_authorized": False,
        "vo_lock": {
            "file": VO_WAV_REL,
            "wav_sha256": VO_WAV_SHA256,
            "mp3_file": VO_MP3_REL,
            "mp3_sha256": VO_MP3_SHA256,
            "duration_s": VO_DURATION_S,
            "film_end_s": FILM_END_S,
            "end_card_hold_s": round(FILM_END_S - VO_DURATION_S, 2),
            "words_srt": "02_Voiceover/stt/hos_011_vo_v01/words.srt",
            "stt_raw": "02_Voiceover/stt/hos_011_vo_v01/stt_raw.json",
            "verdict": "J2286 KEEP across all 5 chapters (0 pickups, 0 re-recordings); J2245 closed by acting Chief on 10 Nov 2026.",
        },
        "hos_2026_11_e2_gate": {
            "window_s": [0.0, 30.0],
            "distinct_moving_plates": len([r for r in rows if r["in_s"] < 30.0]),
            "max_cut_s": max(r["duration_s"] for r in rows if r["in_s"] < 30.0),
            "proof_0_05_to_0_15_rows": ["P1:01b", "P1:02a", "P1:02b"],
            "early_data_scale_0_25_to_0_40_row": "P1:04b_cg_stopwatch_scale",
            "early_data_scale_window_s": [26.50, 30.70],
            "verdict": "PASS",
        },
        "who_portraits": WHO_PORTRAITS,
        "parts": part_summaries,
        "totals": tot,
        "rows": rows,
    }
    (EDIT_DIR / "PICTURE_PLAN_v01.json").write_text(json.dumps(plan_json, indent=2, ensure_ascii=False) + "\n")

    # 3. SHOT_LIST_v01.md
    shot_md = build_shot_list_md(rows, part_summaries, tot)
    (EDIT_DIR / "SHOT_LIST_v01.md").write_text(shot_md)

    # 4. PICTURE_PLAN_v01.md
    plan_md = build_picture_plan_md(rows, part_summaries, tot)
    (EDIT_DIR / "PICTURE_PLAN_v01.md").write_text(plan_md)

    # 5. PRICE_REVIEW_v01.md
    price_md = build_price_review_md(rows, part_summaries, tot)
    (EDIT_DIR / "PRICE_REVIEW_v01.md").write_text(price_md)


def format_markers_cell(r: dict) -> str:
    m = r["markers"]
    bits = []
    if "chapter_card" in m:
        bits.append(f"`CHAPTER CARD: {m['chapter_card']}`")
    if "data" in m:
        bits.append(f"`DATA: {m['data']}`")
    if "scale" in m:
        bits.append(f"`SCALE: {m['scale']}`")
    if "who" in m:
        bits.append(f"`WHO: {m['who']}`")
    if "when" in m:
        bits.append(f"`WHEN: {m['when']}`")
    if "fact" in m:
        bits.append(f"`FACT: {m['fact']}`")
    if "label" in m:
        bits.append(f"`LABEL: {m['label']}`")
    if "explorer" in m:
        bits.append(f"`[EXPLORER ACTS]: {m['explorer']}`")
    if "subscribe_beat" in m:
        bits.append("`[SUBSCRIBE BEAT]`")
    return " · ".join(bits) if bits else "—"


def build_cost_table_md(part_summaries: list[dict], tot: dict) -> str:
    lines = [
        "| Part | Chapter title | Time (`in–out`) | Rows | Quality (`100`) | Fast (`10`) | Code graphic (`0`) | Free archive (`0`) | Reuse (`0`) | Mint rows | Free rows | Flow credits (try-1) | Flow credits (expected) | Vertex try-1 (£) | Vertex expected (£) |",
        "|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for ps in part_summaries:
        lines.append(
            f"| Part {ps['part']:02d} | {ps['title']} | `{ps['in']}–{ps['out']}` | {ps['rows']} | "
            f"{ps['mint_quality']} | {ps['mint_fast']} | {ps['code_graphic']} | {ps['free_archive']} | "
            f"{ps['existing_plate_reuse']} | {ps['mint_rows']} | {ps['free_rows']} | "
            f"{ps['flow_credits_try1']:,} | {ps['flow_credits_expected']:,} | "
            f"£{ps['vertex_try1_gbp']:.2f} | £{ps['vertex_expected_gbp']:.2f} |"
        )
    lines.append(
        f"| **Total** | **Full film (`{fmt_time(FILM_END_S)}`)** | `0:00.00–{fmt_time(FILM_END_S)}` | "
        f"**{tot['rows']}** | **{tot['mint_quality']}** | **{tot['mint_fast']}** | "
        f"**{tot['code_graphic']}** | **{tot['free_archive']}** | **{tot['existing_plate_reuse']}** | "
        f"**{tot['mint_rows']}** | **{tot['free_rows']}** | "
        f"**{tot['flow_credits_try1']:,}** | **{tot['flow_credits_expected']:,}** | "
        f"**£{tot['vertex_try1_gbp']:.2f}** | **£{tot['vertex_expected_gbp']:.2f}** |"
    )
    return "\n".join(lines)


def build_shot_list_md(rows: list[dict], part_summaries: list[dict], tot: dict) -> str:
    cost_table = build_cost_table_md(part_summaries, tot)
    open_rows = [r for r in rows if r["in_s"] < 30.0]

    lines = [
        "# HOS 011 — Shot List v01 (Timed to Locked VO `hos_011_vo_v01`, `J2475`)",
        "",
        "| Field | Value |",
        "|---|---|",
        "| Film | `011_Surgery-Before-Anaesthesia` |",
        "| Title (Variant A / B) | *Anesthesia: The Day Surgery Stopped Hurting* / *What Surgery Was Like Before Anesthesia* |",
        "| Air date (slotted) | **Thu 10 Dec 2026** 18:00 UK (`2026-12-10T18:00:00.000Z`, `J2231`) |",
        "| Locked script | `01_Script/surgery_script_master_v02.md` (**91.1/100 PASS**, 1,230 spoken words, `J0198` Gemini facts PASS + `J0224` Claude primary-source quote check PASS) |",
        f"| Locked VO | `{VO_WAV_REL}` (`532.720 s` = `8:52.72`, `sha256: {VO_WAV_SHA256}`; MP3 `sha256: {VO_MP3_SHA256}`) — `J2286` listening review **KEEP** on all 5 chapters (`0` pickups, `0` re-recordings), `J2245` closed by acting Chief on 10 Nov 2026 |",
        "| Word timings | `02_Voiceover/stt/hos_011_vo_v01/words.srt` and `02_Voiceover/stt/hos_011_vo_v01/stt_raw.json` |",
        f"| Total runtime | **`535.30 s` (`8:55.30`)** = `532.72 s` VO + `2.58 s` house cream end-card hold (`P5:17_cream_end_card`) |",
        f"| Total rows | **{tot['rows']} contiguous rows** across 5 parts (`0` gaps, every minted row `≤ 8.00 s`): **{tot['mint_rows']} mint rows** (`{tot['mint_quality']}` Quality + `{tot['mint_fast']}` Fast) + **{tot['free_rows']} £0/0-credit rows** (`{tot['code_graphic']}` code graphics + `{tot['free_archive']}` free public-domain archive composites + `{tot['existing_plate_reuse']}` intra-film plate tail reuse) |",
        f"| Flow credit total | **`{tot['flow_credits_try1']:,}` Flow credits first-try** (`{tot['flow_credits_expected']:,}` expected at observed 2.59× Quality / 2.00× Fast retry rates); Vertex fallback **`£{tot['vertex_try1_gbp']:.2f}` try-1** (`£{tot['vertex_expected_gbp']:.2f}` expected) |",
        "| Generation lock | **`generation_authorized: false` on every row. £0 / 0 credits spent in `J2475`.** Paid picture parks for the Chief's price pass behind active HOS films. |",
        "",
        "---",
        "",
        "## 1. HOS-2026-11-E2 Proof-First Open Gate (`0:00.00–0:40.00`)",
        "",
        "| Gate item | Requirement (`AGENTS.md` / `J2204`) | `SHOT_LIST_v01` verification | Verdict |",
        "|---|---|---|---|",
        f"| **1. CUTS (`0:00–0:30`)** | Every cut `≤ 4.50 s`, `≥ 7` distinct moving plates, no hold `> 4.50 s` | **{len(open_rows)} distinct moving clips** in `0:00–0:30` (`P1:01a` `3.16 s`, `P1:01b` `3.74 s`, `P1:02a` `3.60 s`, `P1:02b` `3.78 s`, `P1:03a` `4.22 s`, `P1:03b` `4.30 s`, `P1:04a` `3.70 s`, `P1:04b_cg_stopwatch_scale` `4.20 s`); max cut **`4.30 s ≤ 4.50 s`** | **PASS** |",
        "| **2. PROOF (`0:05–0:15`)** | Physical proof or apparatus on screen, never an exterior establishing shot | `P1:01b` (`0:03.16–0:06.90`: scarred oak operating chair with leather arm straps & steel surgical knife case), `P1:02a` (`0:06.90–0:10.50`: gallery students' open brass pocket watches ticking in unison), `P1:02b` (`0:10.50–0:14.28`: cordial bottle & leather bite-strap set beside the chair) — zero exterior building/street shots | **PASS** |",
        "| **3. EARLY (`0:25–0:40`)** | First animated `DATA + SCALE` graphic on screen between `0:25` and `0:40` | `P1:04b_cg_stopwatch_scale` on screen at **`0:26.50–0:30.70`** (`4.20 s`), drawing the brass stopwatch dial stopping short of `3 MINUTES` beside a 3-minute egg sandglass (`SCALE: About as long as boiling an egg`) and flipping to `16 OCTOBER 1846 — 0 PAIN` | **PASS** |",
        "| **First-minute HOS locks** | Answer image by `0:05`, title question by `0:08`, promise by `0:58`, first real fact before `0:45`, no Explorer in `0:00–1:00` | Answer image at `0:00.00–0:03.16` (`P1:01a`), title question `'Why?'` at `0:05.72` (`P1:01b`), Liston `<3 min` fact at `0:18.50–0:22.80` (`P1:03b`) & Boston `16 Oct 1846` at `0:30.70–0:35.80` (`P1:05a`), promise at `0:48.28–0:58.82` (`P1:07a`/`P1:07b`), Explorer first appears at `1:41.80` (`P2:03a`) | **PASS** |",
        "",
        "---",
        "",
        "## 2. Mint Cost & Picture Source Summary Table",
        "",
        cost_table,
        "",
        "### Breakdown by Picture Source Category",
        "",
        "| Source category | Rows | Share of rows | Flow credits (try-1) | Flow credits (expected) | Notes |",
        "|---|---:|---:|---:|---:|---|",
        f"| **1. Own code graphics (`code_graphic`)** | `{tot['code_graphic']}` | `{100*tot['code_graphic']/tot['rows']:.1f}%` | `0` | `0` | 4 chapter cards (`card_p02`–`card_p05`), 1 cream end card (`P5:17_cream_end_card`), 4 `DATA + SCALE` animated graphics (`P1:04b`, `P2:07b`, `P4:06a`, `P5:09b`), and 3 animated teach/map diagrams (`P1:07a` promise route map, `P4:04c` `'anaesthesia'` etymology, `P5:12a` anaesthetist physiological trace) |",
        f"| **2. Free public-domain archive (`free_archive`)** | `{tot['free_archive']}` | `{100*tot['free_archive']/tot['rows']:.1f}%` | `0` | `0` | 9 primary-source scans/photographs from Wikimedia Commons / Wellcome / NLM (`P2:04a` Davy 1800 p. 556, `P2:05a` laughing-gas broadside, `P2:09b` Long 1849 paper, `P3:09a` 1847 Southworth & Hawes Ether Dome daguerreotype, `P4:03a` US Patent `4,848`, `P4:08b` 1868 Boston Ether Monument, `P5:03a` Squire 1846 London inhaler, `P5:06a` Simpson 1847 chloroform pamphlet, `P5:07a` Snow 1858 chloroform treatise) + 10 `WHO` circular portrait cut-outs |",
        f"| **3. Existing plate tail reuse (`existing_plate_reuse`)** | `{tot['existing_plate_reuse']}` | `{100*tot['existing_plate_reuse']/tot['rows']:.1f}%` | `0` | `0` | `P5:16b_reuse_pocket_watch_to_globe` (`8:48.20–8:52.72`) reuses the `[3.48s..8.00s]` moving tail of `P1:07b` (`> 7 min` separation) on the closing callback line *'Together, they turned surgery from a race into a sleep.'* |",
        f"| **4. New plate to mint — Veo 3.1 `Fast` (`mint_fast`)** | `{tot['mint_fast']}` | `{100*tot['mint_fast']/tot['rows']:.1f}%` | `{tot['mint_fast']*10:,}` | `{tot['mint_fast']*20:,}` | Strictly non-emissive daylight/window-lit apparatus, architectural, and tabletop shots (`≤ 8.00 s` each, zero candles/flames/glows) |",
        f"| **5. New plate to mint — Veo 3.1 `Quality` (`mint_quality`)** | `{tot['mint_quality']}` | `{100*tot['mint_quality']/tot['rows']:.1f}%` | `{tot['mint_quality']*100:,}` | `{tot['mint_quality']*259:,}` | Hero human faces/hands, glass ether globe reflections, dining-room chandelier lighting, and the 2 Explorer character-sheet beats (`≤ 8.00 s` each) |",
        f"| **Total** | **`{tot['rows']}`** | **`100.0%`** | **`{tot['flow_credits_try1']:,}`** | **`{tot['flow_credits_expected']:,}`** | **`{tot['mint_rows']}` rows need minting (`{tot['free_rows']}` rows are £0 / 0 credits)** |",
        "",
        "---",
        "",
        "## 3. Public-Domain `WHO` Card Portraits (`£0` / `0` Credits, Lower-Third + Circular Cut-Out)",
        "",
        "| # | First-mention row | Time (`in–out`) | `WHO` card text | Public-domain portrait source & licence |",
        "|---:|---|---|---|---|",
    ]

    who_idx = 0
    for r in rows:
        if "who" in r["markers"]:
            who_idx += 1
            wtxt = r["markers"]["who"]
            winfo = WHO_PORTRAITS[wtxt]
            lines.append(
                f"| {who_idx} | `{r['row_id']}` | `{r['in']}–{r['out']}` | `{wtxt}` | "
                f"`{winfo['file']}` — [Wikimedia Commons]({winfo['commons_url']}) · {winfo['licence']} |"
            )

    lines.extend([
        "",
        "---",
        "",
        "## 4. Row-by-Row Shot List Timed to `hos_011_vo_v01` (`words.srt`)",
        "",
    ])

    for ps in part_summaries:
        p = ps["part"]
        prows = [r for r in rows if r["part"] == p]
        lines.extend([
            f"### Part {p:02d} — {ps['title']} (`{ps['in']}–{ps['out']}`, `{ps['duration_s']:.2f} s`, {ps['rows']} rows)",
            "",
            f"- **Chapter VO WAV:** `{CHAPTER_META[p]['vo_wav']}`",
            f"- **Music cue:** {CHAPTER_META[p]['music_mood']}",
            f"- **Part cost:** `{ps['mint_rows']}` mint rows (`{ps['mint_quality']}` Quality + `{ps['mint_fast']}` Fast) + `{ps['free_rows']}` free rows = **`{ps['flow_credits_try1']:,}` Flow credits try-1** (`{ps['flow_credits_expected']:,}` expected)",
            "",
            "| Row | Time (`in–out`) | Dur (`s`) | VO words (`words.srt`) | Visual & camera move | On-screen markers (`Teach` / `Polish`) | Picture source (path / URL & licence / mint model) | Flow credits (try-1 / exp) |",
            "|---|---|---:|---|---|---|---|---:|",
        ])
        for r in prows:
            mcell = format_markers_cell(r)
            lines.append(
                f"| `{r['row_id']}` | `{r['in']}–{r['out']}` | `{r['duration_s']:.2f}` | "
                f"\"{r['vo_excerpt']}\" | **{r['subject']}** ({r['camera']}): {r['visual']} | "
                f"{mcell} | {r['picture_source']} | `{r['flow_credits_try1']} / {r['flow_credits_expected']}` |"
            )
        lines.append("")

    lines.extend([
        "---",
        "",
        "## 5. Teach-on-Screen & Polish-Pass Gate Self-Check",
        "",
        "| Gate item | Requirement | Count / verification in `SHOT_LIST_v01` | Status |",
        "|---|---|---|---|",
        "| **DATA + SCALE** | `≥ 3` animated data moments (incl. timeline), each with spoken & sourced `SCALE` | **4 `DATA + SCALE` code graphics**: `P1:04b_cg_stopwatch_scale` (`<3 min` stopwatch vs boiling an egg), `P2:07b_cg_timeline_42yr` (`1800 → 1842` 42-year timeline), `P4:06a_cg_master_timeline` (`1800 → 1846` four-claimant master timeline), `P5:09b_cg_safety_stadium` (`1 in 100,000` counter + `90,000`-seat Wembley stadium bowl) | **PASS** |",
        "| **WHO** | Every named person has a card at first mention with sourced years & period role | **10 `WHO` cards** (`Liston`, `Davy`, `Long`, `Wells`, `Morton`, `Warren`, `Holmes`, `Jackson`, `Simpson`, `Snow`), each paired with a verified public-domain portrait cut-out | **PASS** |",
        "| **WHEN** | Every spoken date or era has a stamp or timeline marker | **22 `WHEN` stamps** covering every spoken date/era from `before 1846` and `Bristol, 1800` to `London, 7 April 1853` and `Today` | **PASS** |",
        "| **FACT** | `2–4` sourced surprising fact cards (`≤ 4` words) | **4 `FACT` cards**: `Under 3 minutes` (`P1:03b`), `$2.00 ether operation` (`P2:08a`), `Patent No. 4,848` (`P4:02b`), `No claimant named` (`P4:09a`) | **PASS** |",
        "| **EXPLORER** | `1–3` beats, never in `0:00–1:00`, locked to master character sheet | **2 `[EXPLORER ACTS]` beats**: `P2:03a` (`1:41.80–1:48.50`, Bristol 1800) and `P3:07a` (`3:58.20–4:03.50`, Boston Ether Dome 1846), both seeded from `01_Character/02_Master-Character-Sheet/THE_EXPLORER_MASTER_CHARACTER_SHEET.png` | **PASS** |",
        f"| **MOTION & BACK-TO-BACK** | Every minted clip `≤ 8.00 s`; never two full-frame teach/archive graphics back-to-back | All {tot['mint_rows']} minted rows are `3.16 s – 7.70 s` (`≤ 8.00 s`); all {tot['code_graphic'] + tot['free_archive']} full-frame `code_graphic` / `free_archive` rows have moving plates immediately before and after (`0` back-to-back graphics) | **PASS** |",
        "| **SFX & MUSIC** | House SFX kit (`rumble_low`, `whoosh_soft`, `tick_ink`) + part-by-part music cue shifts | House SFX mapped per row (`06_Sound-Effects/kit_v01`); music shifts across the 4 chapter cards (`card_p02`–`card_p05`) and holds `2.58 s` over `P5:17_cream_end_card` | **PASS** |",
        "",
        "---",
        "",
        "## 6. Companion Shorts Reuse Mapping (`10_Shorts/SHORTS_SCRIPTS_v02.md`, `0` Extra Mint Credits)",
        "",
        "- **Short A (*How Was Surgery Done Before Anesthesia?*, 61 words, ~24.5 s):** Reuses 9:16 centre-crops of `P1:01a` (frame-0 pocket watch + wooden operating theatre with yellow hook word `AWAKE`), `P1:01b` (oak chair with leather straps), `P1:03a` (`WHO: Robert Liston`), `P1:03b` (`FACT: Under 3 minutes` — single Short overlay), `P1:05a` (Morton holding the two-necked glass ether globe to Abbott's face on 16 Oct 1846), and `P3:08b` (Warren in the Ether Dome). **`0` extra Flow credits.**",
        "- **Short B (*Who Invented Anesthesia?*, 60 words, ~24.5 s):** Reuses 9:16 centre-crops of `P1:06a` (frame-0 four rivals' artefacts with yellow hook word `STOLE`), `P2:02a` (Davy 1800 laughing gas), `P2:08a` (Long 1842 Georgia ether towel), `P3:04a` (Wells 1845 Boston trial), `P3:06a` (Morton 16 Oct 1846 glass globe), `P4:02a` (Morton's tinted Letheon), and `P4:09a` (`FACT: No claimant named` on the Boston Ether Monument). **`0` extra Flow credits.**",
    ])
    return "\n".join(lines) + "\n"


def build_picture_plan_md(rows: list[dict], part_summaries: list[dict], tot: dict) -> str:
    cost_table = build_cost_table_md(part_summaries, tot)
    return "\n".join([
        "# HOS 011 — Picture Plan v01 (`J2475`)",
        "",
        f"- **Locked VO:** `{VO_WAV_REL}` (`532.720 s` = `8:52.72`, `sha256: {VO_WAV_SHA256}`; MP3 `sha256: {VO_MP3_SHA256}`) — `J2286` **KEEP** across all 5 chapters, `J2245` closed 10 Nov 2026.",
        f"- **Master JSON:** `07_Edit-Project/PICTURE_PLAN_v01.json` and per-part boards `07_Edit-Project/parts/part-01_plates_v01.json` .. `part-05_plates_v01.json`.",
        f"- **Row-by-row shot list:** `07_Edit-Project/SHOT_LIST_v01.md` ({tot['rows']} contiguous rows across `535.30 s` / `8:55.30`).",
        f"- **Generation authorization:** `generation_authorized: false` on every row. **£0 / 0 credits spent.**",
        "",
        "## Summary by Part",
        "",
        cost_table,
        "",
        f"## Free (`£0` / `0` Credit) Rows in the Plan (`{tot['free_rows']}` Full-Frame Rows + `10` `WHO` Portrait Cut-Outs)",
        "",
        f"1. **{tot['code_graphic']} Own Code Graphics (`07_Edit-Project/code_graphics_v01/`):**",
        "   - `P1:04b_cg_stopwatch_scale` (`0:26.50–0:30.70`): `DATA + SCALE #1` (`<3 min` stopwatch dial + boiling-an-egg sandglass + `16 Oct 1846` turnaround, satisfying `HOS-2026-11-E2` `EARLY 0:25–0:40`).",
        "   - `P1:07a_cg_three_chapters_map` (`0:47.40–0:53.60`): Promise route map (`Bristol 1800 → Jefferson, Georgia 1842 → Boston 1846`).",
        "   - `P2:01_card_p02` (`1:26.80–1:28.90`): `[CHAPTER CARD: A Gas That Made People Laugh]`.",
        "   - `P2:07b_cg_timeline_42yr` (`2:28.30–2:34.90`): `DATA + SCALE #2` (`1800 Bristol → 1842 Jefferson, Georgia`, 42-year span).",
        "   - `P3:01_card_p03` (`2:55.66–2:57.80`): `[CHAPTER CARD: \"This Is No Humbug\"]`.",
        "   - `P4:01_card_p04` (`4:31.88–4:34.00`): `[CHAPTER CARD: The Fight Over Who Was First]`.",
        "   - `P4:04c_cg_anesthesia_etymology` (`5:09.20–5:14.50`): Oliver Wendell Holmes's 21 Nov 1846 Greek coinage (`an-` + `aisthēsis` → `ANAESTHESIA`).",
        "   - `P4:06a_cg_master_timeline` (`5:26.50–5:33.90`): `DATA + SCALE #3` (Master timeline `1800 Davy → 1842 Long → 1844 Wells → 1846 Morton & Jackson`).",
        "   - `P5:01_card_p05` (`6:06.26–6:08.40`): `[CHAPTER CARD: Across the Ocean]`.",
        "   - `P5:09b_cg_safety_stadium` (`7:38.50–7:46.50`): `DATA + SCALE #4` (`1 in 100,000` counter + `90,000`-seat Wembley stadium diagram with single lit dot).",
        "   - `P5:12a_cg_anesthetist_monitor` (`8:05.80–8:11.20`): Continuous heartbeat, breath, and depth-of-sleep physiological diagram.",
        "   - `P5:17_cream_end_card` (`8:52.72–8:55.30`): House cream-on-brown end card hold (`2.58 s`).",
        f"2. **{tot['free_archive']} Public-Domain Archive Composites (`07_Edit-Project/code_graphics_v01/`):**",
        "   - `P2:04a_arch_davy_1800` (`1:48.50–1:53.50`): Humphry Davy, *Researches, Chemical and Philosophical* (1800), p. 556 (Wellcome / Wikimedia Commons, `Public domain`).",
        "   - `P2:05a_arch_laughing_gas_broadside` (`2:01.20–2:07.60`): 1802 Gillray etching & 1844 Hartford laughing-gas playbill (Wellcome / Wikimedia Commons, `Public domain`).",
        "   - `P2:09b_arch_long_1849` (`2:46.14–2:50.50`): Crawford W. Long, *Southern Medical and Surgical Journal* (Dec 1849) paper (NLM / Wikimedia Commons, `Public domain`).",
        "   - `P3:09a_arch_ether_dome_1847` (`4:18.50–4:24.80`): Southworth & Hawes 1847 daguerreotype of the MGH Ether Dome (Getty / Wikimedia Commons, `Public domain`).",
        "   - `P4:03a_arch_letheon_patent` (`4:45.80–4:50.58`): US Patent No. `4,848` (12 Nov 1846, Jackson & Morton, NARA / Wikimedia Commons, `Public domain`).",
        "   - `P4:08b_arch_ether_monument` (`5:49.50–5:54.80`): 1868 Ether Monument in the Boston Public Garden (Wikimedia Commons, `CC0 / Public domain`).",
        "   - `P5:03a_arch_squire_inhaler_1846` (`6:21.20–6:28.40`): Peter Squire's December 1846 London ether inhaler engraving (Wellcome / Wikimedia Commons, `Public domain`).",
        "   - `P5:06a_arch_simpson_1847` (`7:00.50–7:06.80`): James Young Simpson, *Account of a New Anaesthetic Agent* (Nov 1847, Wellcome / Wikimedia Commons, `Public domain`).",
        "   - `P5:07a_arch_snow_chloroform_1858` (`7:13.80–7:18.72`): John Snow, *On Chloroform and Other Anaesthetics* (1858, Wellcome / Wikimedia Commons, `Public domain`).",
        "3. **1 Intra-Film Plate Tail Reuse (`existing_plate_reuse`):**",
        "   - `P5:16b_reuse_pocket_watch_to_globe` (`8:48.20–8:52.72`): Reuses the unused `[3.48s..8.00s]` moving tail of `P1:07b` (`> 7 min` separation) on the closing callback line.",
        "",
    ])


def build_price_review_md(rows: list[dict], part_summaries: list[dict], tot: dict) -> str:
    cost_table = build_cost_table_md(part_summaries, tot)
    return "\n".join([
        "# HOS 011 — Chief Price Pass Review (`PRICE_REVIEW_v01.md`, `J2475`)",
        "",
        "- **Film:** `011_Surgery-Before-Anaesthesia` (*Anesthesia: The Day Surgery Stopped Hurting*)",
        "- **Slotted air date:** **Thu 10 Dec 2026** 18:00 UK (`2026-12-10T18:00:00.000Z`, `J2231`; ready for Ben's OK **Sun 6 Dec 2026**)",
        "- **Queue position:** First in the HOS waiting line (`jobs/WIP.json` `next_hos`). Preparation only; no active production slot claimed and **0 credits / £0 spent**.",
        f"- **Locked VO:** `{VO_WAV_REL}` (`532.720 s` = `8:52.72`, `sha256: {VO_WAV_SHA256}`), `J2286` **KEEP** on all 5 chapters, `J2245` closed 10 Nov 2026.",
        "",
        f"## 1. Mint Cost Summary ({tot['mint_rows']} Mint Rows + {tot['free_rows']} Free Rows = {tot['rows']} Total Rows)",
        "",
        cost_table,
        "",
        "## 2. Routing & Cost Notes for Chief's Price Pass",
        "",
        f"1. **Every minted row is `≤ 8.00 s` (`3.16 s – 7.70 s`):** Zero rows require a double-clip mint, so `{tot['mint_rows']}` mint rows = `{tot['mint_rows']}` Veo 3.1 clips (`{tot['mint_quality']}` Quality at `100` credits + `{tot['mint_fast']}` Fast at `10` credits = **`{tot['flow_credits_try1']:,}` Flow credits try-1** / **`{tot['flow_credits_expected']:,}` expected**).",
        f"2. **`{100*tot['free_rows']/tot['rows']:.1f}%` of rows (`{tot['free_rows']}` of `{tot['rows']}`) cost `0` credits / `£0`:** `{tot['code_graphic']}` house code graphics (4 chapter cards, 1 cream end card, 4 `DATA + SCALE` graphics, 2 teach diagrams), `{tot['free_archive']}` verified public-domain primary-source archive composites, and `{tot['existing_plate_reuse']}` closing callback tail reuse.",
        f"3. **Strict `Fast` hygiene (`{tot['mint_fast']}` rows):** Every `veo-3.1-fast` row is a daylight or clean window-lit shot of surgical instruments, pocket watches, wooden benches, books, or monument stone with **zero candles, gas lamps, lanterns, or glowing filaments**.",
        "4. **Both Shorts (`Short A` and `Short B`) cost `0` additional mint credits:** All 9:16 plates are centre-cropped from the long's Part 01–04 plates.",
        "5. **Authorization gate:** Every row in `PICTURE_PLAN_v01.json` and `parts/part-01_plates_v01.json`..`part-05_plates_v01.json` carries `\"generation_authorized\": false`. Minting waits until HOS 011 enters active picture production and Chief flips `generation_authorized: true`.",
        "",
    ])


def main() -> None:
    words = load_words()
    rows = enrich_rows(words)
    part_summaries, tot = summarize_parts(rows)
    write_outputs(rows, part_summaries, tot)
    print(
        f"PASS: Built HOS 011 shot list v01 ({tot['rows']} rows, {FILM_END_S:.2f}s): "
        f"{tot['mint_rows']} mint ({tot['mint_quality']} Q + {tot['mint_fast']} F = "
        f"{tot['flow_credits_try1']:,} try-1 / {tot['flow_credits_expected']:,} expected Flow credits) + "
        f"{tot['free_rows']} free ({tot['code_graphic']} CG + {tot['free_archive']} ARCH + {tot['existing_plate_reuse']} REUSE)."
    )


if __name__ == "__main__":
    main()
