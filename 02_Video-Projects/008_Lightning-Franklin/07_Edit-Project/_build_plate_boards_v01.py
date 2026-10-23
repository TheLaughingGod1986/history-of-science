#!/usr/bin/env python3
"""HOS 008: build and price parts/part-0N_plates_v01.json from the locked VO (no spend, mint nothing).

Backlog job J0184 (OWB queue, 12 Oct 2026): plate board rows (prompt, reference, Flow quality, price)
from the locked VO, drafted from SHOT_LIST_v01.md (Claude, 6 Oct) and VO_RETIME_v01.json.

Each plate starts on a sentence (`s`, 1-based inside the part) or on a named word inside it, and runs
to the next plate's start (the next chapter card, or the last word + TAIL_S at the end of the film).
The locked VO runs 9:24.8 against the shot list's ~8:35, so some spans run past one clip (CLIP_USE_S).
Those get `added` continuation rows: the same shot carried on by start-frame I2V from the last frame
of the row before (SHOT_LIST continuity lock). At the price pass, Chief/Claude may swap any of them
for a reuse of a KEEP clip (SHOT_LIST §Size: cut Fast cutaways to reuses first, never 04 proof beats).

Engine and price: Flow Veo 3.1 first (HOS AGENTS.md "Who does what": Fast 10 credits a take, Quality
100, from 006's plan), Vertex Veo as the fallback at list prices (as 006/007: video only, 1080p, GBP at
0.80, 005's takes-per-KEEP and stills-per-plate). Both routes are priced for every mint so the plan
shows the Flow/Vertex split before any spend (SHOT_LIST §Size).

  python3 07_Edit-Project/_build_plate_boards_v01.py
"""
from __future__ import annotations

import json
import math
import re
from pathlib import Path

PROJ = Path(__file__).resolve().parents[1]
EDIT = PROJ / "07_Edit-Project"
RETIME = json.loads((EDIT / "VO_RETIME_v01.json").read_text())
OUT = EDIT / "parts"
PLAN = EDIT / "PICTURE_PLAN_v01.json"
TEMPLATE = json.loads((OUT / "part-01_plates_v01.json").read_text()) if (OUT / "part-01_plates_v01.json").exists() else {}

CLIP_USE_S = 7.9
MIN_PLATE_S = 2.4
TAIL_S = 0.6
REUSE_PAD_S = 0.5
VERTEX_LENGTHS = (4, 6, 8)

# Readings 12 Oct 2026 (ai_spend ledger): Flow 52 credits (14:47Z-15:47Z, AI Ultra refill not landed),
# Vertex Free Trial £4.93 (14:26Z, after HOS 006 J0160 batch B). Vertex stops at £0.10 (HOS AGENTS.md).
FLOW_CREDITS_LEFT = 52
VERTEX_BALANCE_GBP = 4.93
VERTEX_MARGIN_GBP = 0.10
FLOW_CREDITS = {"Quality": 100, "Fast": 10}
USD_PER_S = {"Quality": 0.20, "Fast": 0.10}
USD_PER_STILL = 0.039
GBP_PER_USD = 0.80
TAKES_PER_KEEP = {"Quality": round(70 / 27, 2), "Fast": round(94 / 48, 2)}
STILLS_PER_PLATE = round(171 / 75, 2)

STYLE = "Premium Animistry-class 3D cartoon. "
TAIL = " No readable words or numbers anywhere. Silent. Continuous motion through the final frame. No Explorer. No Orbit."
EXPLORER_TAIL = (" Exactly one Explorer, on model: round gold glasses, teal long coat, finished hair. "
                 "No readable words or numbers anywhere. Silent. Continuous motion through the final frame. No Orbit.")
NOSTRIKE = " The kite and string are never struck; no bolt touches them."
SAFE = " Nobody is struck, burned or hurt."
FRANKLIN = "Benjamin Franklin in his mid-forties, plain short wig, no spectacles, brown 1750s coat"
WILLIAM = "William Franklin, a young man of about twenty-one in a tricorn hat (an adult, never a child)"
JAR = "a glass jar lined with metal foil, a cork stopper with a thick wire through it bent into a ring at the top"
F_HELD = "Fast: held establishing shot, slow push, no readable faces, nothing emissive."
F_DAY = "Fast: daylight or window light; nothing emissive in frame."
F_HANDS = "Fast: hands and props only, no face, nothing emissive."
F_WIDE = "Fast: wide shot, figures small and faces not readable, no lightning."
F_INK = "Fast: ink, paper, props or a flat painted-parchment card; no sparks or glow."
Q_LIGHT = "Quality: lightning, sparks, glow or candlelight (SHOT_LIST: never Fast on fragile light)."
Q_FACE = "Quality: readable face or crowd."
REUSE_REASON = "Reuse: a window of a KEEP clip (callback), no new mint."
CONT_REASON = "Continuation: same shot carried on by start-frame I2V from the last frame of the row before (span > one clip)."

# (id, sentence, word or None, quality | ("reuse", source key), set, side_label, prompt body, explorer)
ROWS = {
    1: [
        ("01_kite_open", 1, None, "Quality", "A", "PHILADELPHIA · 1752",
         "Summer dusk over a green field with a wooden fence and a small open shed: a silk kite climbs into rolling dark storm clouds; the camera slides down the wet string to an iron key, where a tiny blue spark jumps to a knuckle." + NOSTRIKE, False),
        ("02_tower_tilt", 3, None, "Quality", "I", "THE ANSWER IS ON THE ROOF",
         "Night storm over a modern city: a slow tilt up a tall generic glass tower to the thin metal rod at its very top as clouds gather and flicker. No real or recognisable building.", False),
        ("03_table_three", 4, None, "Fast", "D", "A KITE · A KEY · A JAR",
         f"A wooden table in daylight: a silk kite, an iron key and {JAR} arrive one after another, set down by unseen hands; slow push in.", False),
        ("03b_town_safe", 4, "idea", "Fast", "B", None,
         "An 18th-century town of stone and timber houses under a passing grey storm: thin iron rods on the roofs, wet cobbles, people safe behind their doors. Held wide shot, slow push, no lightning.", False),
        ("04_storm_mystery", 5, None, "Quality", "B-style countryside", None,
         "Ancient dark countryside at night: enormous storm clouds roll in, lit from within by silent flickers of lightning far away. Slow push.", False),
        ("05_split_tree", 6, None, "Quality", "B-style countryside", None,
         "A lone tree on a hillside at night is lit white by a flash; afterwards the trunk stands cracked and smoking gently in the rain. No animals shown hurt.", False),
        ("06_heavens", 7, None, "Quality", "B", None,
         "Townsfolk in 18th-century clothes at their windows and doorways look up at a flashing sky, hands clasped, faces small and lit by the flicker." + SAFE, False),
        ("07_hot_night", 8, None, "Fast", "B", None,
         "A town street on a hot summer evening: people sit on doorsteps fanning themselves as heavy clouds slide over the rooftops. Wide shot, faces small, no lightning.", False),
        ("08_sky_flash", 9, None, "Quality", "B", None,
         "A summer night sky over 18th-century rooftops flashes white, again and again, rain beginning to fall.", False),
        ("09_barn_smoke", 9, "smell", "Fast", "B", None,
         "At the edge of town, grey smoke rises from a barn roof into the night rain; seen from a distance, no flames close up, no people or animals in danger.", False),
        ("10_wait_shutter", 10, None, "Fast", "B", None,
         "Inside a cottage, a family waits behind closed wooden shutters, seen from behind; rain streaks the gaps in the shutters. No faces readable, nothing emissive.", False),
        ("11_tall_spire", 11, None, "Quality", "B", None,
         "A church's wooden spire rises high above the low roofs of a town at night; storm clouds churn right over its tip, lit by flickers.", False),
        ("12_steeple_fire", 12, None, "Quality", "B", "LIGHTNING",
         "A bolt hits a church's wooden spire and a small fire catches at the top; townspeople below run with buckets, small in frame." + SAFE, False),
        ("13_ring_the_bells", 13, None, "Quality", "C", "RING THE BELLS",
         "Inside a stone bell tower: two ringers haul on the ropes as rain lashes the louvred openings; a flash lights the tower white through the louvres. Short B frame 0." + SAFE, False),
        ("14_steeple_rain", 14, None, "Fast", "B", None,
         "The steeple from outside in the rain, its bells swinging in the louvred openings; slow push, no lightning in this shot.", False),
        ("15_bell_count", 15, None, "Fast", "C", None,
         "An empty bell tower in grey storm light: the bell ropes sway slowly by themselves, rain dripping from the louvres. No people.", False),
        ("16_question_sky", 16, None, "Fast", "B", None,
         "Clouds churn over a dark sleeping town; a slow pull back from the rooftops. No lightning.", False),
        ("17_globe_spark", 19, None, "Quality", "D", None,
         "A candlelit back room in Philadelphia: a glass globe on a wooden frame spins and crackles with small blue sparks; Leyden jars on a shelf behind.", False),
    ],
    2: [
        ("01_salon_tube", 1, None, "Quality", "F", "ELECTRICITY · A PARTY TRICK",
         "A panelled 1740s salon lit by candles: a travelling lecturer rubs a glass tube with silk before well-dressed guests.", False),
        ("02_salon_spark", 2, None, "Quality", "F", None,
         "In the candlelit salon, a guest's hair lifts towards the glass tube and a small spark jumps from her fingertip; the audience gasps and laughs." + SAFE, False),
        ("03_audience_shock", 3, None, "Quality", "F", None,
         "A row of well-dressed guests holding hands jolts and laughs together as a tiny shock passes along the line; candlelit salon.", False),
        ("04_franklin_watches", 4, None, "Quality", "F", "BENJAMIN FRANKLIN · PHILADELPHIA",
         f"{FRANKLIN}, in the salon audience, leans forward, fascinated, his face lit by the candles.", False),
        ("05_print_shop", 5, None, "Quality", "E", None,
         f"A Philadelphia printing shop in morning light, wooden hand press and type cases: {FRANKLIN} hands his apron to a younger partner and carries a glass tube into the back room.", False),
        ("06_leyden_jar", 6, None, "Quality", "D", "THE LEYDEN JAR",
         f"In the candlelit back room, Franklin's hands lift {JAR} from a shelf of jars and set it on the bench.", False),
        ("07_foil_jar", 7, None, "Fast", "D", None,
         "Close on hands pressing thin metal foil smooth around the outside of a glass jar on a wooden bench; daylight from a window, no candles.", False),
        ("08_jar_spark", 7, "bright", "Quality", "D", None,
         f"Close on {JAR}: a bright blue spark snaps from the ring to a fingertip in the dim back room." + SAFE, False),
        ("09_window_storm", 8, None, "Quality", "D", None,
         f"{FRANKLIN} at the back-room window, a storm far off over the roofs flickering; he turns his head slowly from the jar to the sky.", False),
        ("10_flash_crack_smell", 9, None, "Quality", "D", None,
         "In the dim back room, a spark flashes between two jars; Franklin's hand recoils, and a thin curl of smoke drifts up from the bench.", False),
        ("11_jar_crack", 12, None, "Quality", "D", None,
         "A bigger spark cracks between two foil-lined jars, a white flash in the dark room, like a tiny thunderstorm on the bench.", False),
        ("12_notebook_list", 13, None, "Fast", "D", "7 NOVEMBER 1749",
         "Franklin's open notebook on the bench in window light: a quill writes a numbered column down the page; no legible words (the list is an overlay in the edit).", False),
        ("13_explorer_jar", 14, None, "Quality", "D", None,
         f"In the candlelit back room, the Explorer reaches a cautious finger to {JAR}, flinches at the small snap of a spark, shakes his hand, then grins and does it again.", True),
        ("14_likeness_pairs", 15, None, "Fast", "J", None,
         "A soft painted-parchment card in two halves: a crooked little spark on one side, a crooked lightning bolt on the other, drawn in gentle animated lines. No words.", False),
        ("15_likeness_fire", 17, None, "Fast", "J", None,
         "A soft painted-parchment card in two halves: a candle wick lit by a tiny spark, a thatched roof lit by lightning, animated gently. No people, no words.", False),
        ("16_not_proof", 18, None, "Fast", "D", None,
         "Close on Franklin's hand tapping his quill against the notebook page, thinking; window light, no face, no candles.", False),
        ("17_page_bottom", 19, None, "Fast", "D", "LET THE EXPERIMENT BE MADE",
         "The quill writes five words at the bottom of the notebook page; no legible words (the line is an overlay in the edit). Window light.", False),
        ("18_quill_down", 21, None, "Fast", "D", None,
         "Franklin puts the quill down and looks up at the stormy window, seen from behind; grey daylight, nothing emissive.", False),
    ],
    3: [
        ("01_points_desk", 1, None, "Quality", "D", None,
         f"{FRANKLIN} at his bench holds a needle point near a charged brass ball; a faint blue glow gathers at the point.", False),
        ("02_sentry_box", 3, None, "Fast", "D", "THE SENTRY-BOX",
         "A drawing on Franklin's desk: a small sentry-box on a tall tower with a pointed iron rod rising into cloud; the drawing's clouds drift. No legible text on the sheet.", False),
        ("03_rod_cloud", 4, None, "Quality", "J", None,
         "A soft painted-parchment card: a tall pointed rod on a tower beneath a storm cloud; small sparks are drawn gently from the cloud to the tip. No words.", False),
        ("04_letter_crosses", 5, None, "Fast", "K", None,
         "A letter is sealed with wax; then a painted-parchment map of the Atlantic where a small sailing ship crosses under drifting cloud shadows. No words on the map.", False),
        ("05_marly_garden", 6, None, "Fast", "G", "MARLY, FRANCE · MAY 1752",
         "A French formal garden near Paris in May under a grey storm sky: a 40-foot iron rod held by silk cords between three tall poles, its foot in a small sentry box on a stool over wine bottles. Held wide shot, slow push, no lightning.", False),
        ("06_marly_spark", 7, None, "Quality", "G", None,
         "In the Marly garden as a storm cloud passes, an old soldier brings a brass wire in a long glass handle near the rod's foot and a spark jumps." + SAFE, False),
        ("07_slow_news", 9, None, ("reuse", "P3:04_letter_crosses"), "K", None, None, False),
        ("08_no_tower", 11, None, "Fast", "A-style town", None,
         "1750s Philadelphia rooftops, low and even brick and timber, no tall spire anywhere; slow pan in grey daylight.", False),
        ("09_kite_idea", 12, None, "Fast", "D", None,
         "From Franklin's window, a child's kite bobs high above the rooftops in the wind; he watches from inside, seen from behind. Daylight.", False),
        ("10_kite_over_steeple", 13, None, "Fast", "A-style town", None,
         "A kite rises higher and higher until it floats above a church steeple; wide shot, grey sky, no lightning.", False),
        ("11_kite_build", 14, None, "Quality", "D", "SILK · CEDAR · WIRE",
         f"{FRANKLIN} at his desk making a kite: a silk handkerchief stretched over two crossed cedar sticks, a tail tied on; warm candlelight.", False),
        ("12_wire_top", 15, None, "Quality", "D", None,
         "Close on Franklin's hands fixing a sharp wire to the top of the kite, standing a foot or more above the wooden frame; candlelight.", False),
        ("13_key_ribbon", 16, None, "Quality", "D", None,
         "Close on Franklin's hands tying an iron key where rough twine meets a ribbon of silk; candlelight.", False),
        ("14_silk_clever", 17, None, "Fast", "D", None,
         "Close on a dry silk ribbon running through Franklin's fingers; window light, no face.", False),
        ("15_wet_dry", 18, None, "Fast", "J", None,
         "A soft painted-parchment card: a wet twine string with gentle lines of charge running down it that stop where it meets a dry silk ribbon. No words.", False),
        ("16_keep_silk_dry", 19, None, "Quality", "A", "KEEP THE SILK DRY",
         "Inside a small open-fronted wooden shed at the edge of a field, rain outside: the bottom of the kite string, rough twine, the iron key and a dry silk ribbon held in Franklin's hand.", False),
        ("17_secret_walk", 20, None, "Fast", "A", None,
         "Two men slip out of town at dusk across a wet field, one carrying a kite wrapped in cloth; wide shot, figures small, no lightning.", False),
        ("18_william_runs", 22, None, "Quality", "A", "JUNE 1752",
         f"Field under a dark sky: {WILLIAM} runs and lifts the kite into the wind; Franklin watches from the shed." + NOSTRIKE, False),
        ("19_kite_climb", 23, None, "Quality", "A", None,
         "The silk kite climbs into the dark storm cloud; the wet string glints. Short A frame 0." + NOSTRIKE, False),
        ("20_waiting", 24, None, "Quality", "A", None,
         "Father and son in the shed doorway, looking up at the storm overhead, waiting; rain falling past them.", False),
        ("21_doorway_pov", 25, None, "Quality", "A", None,
         "From inside the shed doorway: a string runs up from a hand into the storm sky, rain sweeping across the field, clouds flickering far off." + NOSTRIKE, False),
        ("22_william_face", 26, None, "Quality", "A", None,
         f"{WILLIAM} beside his father in the shed doorway, looking up, rain dripping from his hat brim.", False),
        ("23_nothing_yet", 27, None, "Fast", "A", None,
         "The kite holds steady in the grey cloud; nothing happens; wind moves the grass. No lightning.", False),
        ("24_eyes_drop", 28, None, "Quality", "A", None,
         "Franklin's eyes drop from the sky to the string in his hand; close, his face lit by the grey storm light.", False),
        ("25_fibres_rise", 29, None, "Quality", "A", "THE THREADS STAND UP",
         "Extreme close-up: loose fibres on the wet twine lift and spread apart from each other, like hairs on an arm." + NOSTRIKE, False),
    ],
    4: [
        ("01_knuckle_close", 1, None, "Quality", "A", None,
         "In the shed, Franklin slowly brings his knuckle close to the iron key hanging on the string; rain behind.", False),
        ("02_knuckle_spark", 2, None, "Quality", "A", "A SPARK",
         "A small blue spark leaps from the iron key to Franklin's knuckle with a snap; small spark only." + SAFE, False),
        ("03_room_memory", 3, None, ("reuse", "P1:17_globe_spark"), "D", None, None, False),
        ("04_fill_the_jar", 4, None, "Quality", "A", "LIGHTNING IN A JAR",
         f"In the shed, Franklin touches the iron key to the wire of {JAR}; a faint glow gathers in the jar." + NOSTRIKE, False),
        ("05_jar_spark_field", 5, None, "Quality", "A", None,
         "A second hand brings a wire near the charged jar in the shed and the same small spark jumps out." + SAFE, False),
        ("06_same_thing", 6, None, "Fast", "D + A", "ELECTRICITY",
         "Split frame: on one side a spark from a jar in a back room, on the other a spark from a key in a rainy field, side by side and identical.", False),
        ("07_kite_cloud_wide", 8, None, "Quality", "A", None,
         "Wide: the kite steady in the dark storm cloud over the field, flickers far off in the cloud." + NOSTRIKE, False),
        ("08_teach_charge", 9, None, "Fast", "J", "NO BOLT, JUST CHARGE",
         "A soft painted-parchment card: a storm cloud, the kite well below it, gentle lines of charge running down the wet string; no bolt touches the kite. No words.", False),
        ("09_charge_string", 11, None, "Quality", "A", None,
         "Close along the wet twine: a faint soft glow of charge runs quietly down the string to the iron key." + NOSTRIKE, False),
        ("10_richmann_rod", 13, None, "Quality", "room", "ST PETERSBURG · 1753",
         "St Petersburg in a summer storm, 1753: an iron rod rises through the roof of a stone house; clouds flicker overhead.", False),
        ("11_richmann_room", 13, "during", "Quality", "room", None,
         "The empty room below: an iron rod through the ceiling, an electrometer on a stand; the window flashes white, cut away. No body, no injury, no people.", False),
        ("12_careful_lucky", 14, None, "Fast", "D", None,
         "Close on Franklin's hands turning the iron key over in window light; no face, nothing emissive.", False),
        ("13_gazette_page", 15, None, "Fast", "E", "PENNSYLVANIA GAZETTE · 19 OCTOBER 1752",
         "An inside page of a printed newspaper lifted from a wooden press in daylight; no legible words.", False),
        ("14_royal_society", 16, None, "Quality", "room", "THE ROYAL SOCIETY",
         "A candlelit London meeting room: a letter is read aloud to a row of listening fellows in wigs.", False),
        ("15_copley_medal", 16, "award", "Quality", "room", "THE COPLEY MEDAL · 1753",
         "A medal is lifted from a velvet case and catches the light; no legible lettering.", False),
        ("16_rod_idea", 17, None, "Fast", "D", None,
         "Franklin looks from the jar to the window, then up at the roofs; seen from behind, grey daylight, nothing emissive.", False),
        ("17_roofs_storm", 19, None, "Fast", "A-style town", None,
         "1750s Philadelphia roofs under a gathering storm, families going indoors, small in frame; no lightning.", False),
    ],
    5: [
        ("01_house_rod", 1, None, "Quality", "H", "SEPTEMBER 1752",
         "Franklin's brick town house on Market Street, 1752: an iron rod fixed to the top of the chimney, about nine feet above it, as a storm rolls in.", False),
        ("02_wire_bells", 2, None, "Fast", "H", None,
         "Inside the house in daylight: a wire runs down the staircase wall to two small bells hung about six inches apart opposite a chamber door; hands finish hanging a brass ball on a silk thread between them.", False),
        ("03_bells_ring", 3, None, "Quality", "H", "THE BELLS THAT RING",
         "On the dim staircase as a storm passes, the two small bells begin to ring on their own as the brass ball swings between them; a tiny spark.", False),
        ("04_tell_everyone", 4, None, "Fast", "E", None,
         "In the printing shop in morning light, fresh printed sheets are stacked and handed across the counter to customers, faces small.", False),
        ("05_almanac_page", 5, None, "Fast", "D", "POOR RICHARD · 1753",
         "An almanac page turned by a hand in window light; no legible words, no drawing.", False),
        ("06_rod_fitting", 6, None, "Fast", "H-style street", None,
         "A workman fixes an iron rod up the outside wall of a brick house: the point above the roof, the foot pushed into damp earth. Daylight.", False),
        ("07_giant_spark", 7, None, "Quality", "B", "HOTTER THAN THE SUN",
         "A single giant lightning bolt over a dark town, slowed down, branching across the sky.", False),
        ("08_looking_path", 9, None, "Quality", "J", None,
         "A soft painted-parchment card: a lightning bolt forks and feels its way downward towards a town's roofs, choosing a path. No words.", False),
        ("09_wood_vs_metal", 10, None, "Fast", "J", None,
         "A soft painted-parchment card: a wooden roof and a stone steeple, drawn in gentle lines, flare and crack apart; no people. No words.", False),
        ("10_metal_easy", 11, None, "Quality", "J", None,
         "A soft painted-parchment card: a metal rod glows and passes the charge smoothly down. No words.", False),
        ("11_safe_path", 12, None, "Quality", "J", "A SAFE PATH TO THE GROUND",
         "A cutaway painted-parchment diagram: a bolt hits the tip of a rod on a steeple, runs down the outside wall and into the earth; the wooden spire stays dark and safe. No words.", False),
        ("12_no_patent", 13, None, "Fast", "D", None,
         "Franklin at his desk pushes a folded paper aside and smiles, seen from the side at a distance; window light, nothing emissive.", False),
        ("13_rods_spread", 15, None, "Fast", "B, H, sea", None,
         "Iron rods rise one after another on a church tower, a town house and a ship's mast; daylight, no lightning.", False),
        ("14_safe_towers", 16, None, "Quality", "B", None,
         "A church tower with a rod on top stands calm in a storm; a flash runs down the rod into the ground while the tower is untouched." + SAFE, False),
        ("15_why_card", 17, None, "Quality", "B", None,
         "A calm 18th-century town under a passing storm, rods on the roofs, people indoors and safe, warm windows; slow push.", False),
        ("16_explorer_rooftop", 19, None, "Quality", "H", None,
         "On a rooftop at golden hour after the storm, the Explorer taps the base of the iron rod, follows it down the wall to the ground with his eyes, nods and gives it a small salute.", True),
        ("17_look_up", 20, None, "Fast", "I", None,
         "Today: a child at a window, seen from behind, looks up at a tall building with a thin rod on top; grey daylight, no lightning.", False),
        ("18_rod_closeup", 21, None, "Quality", "I", None,
         "The thin metal rod at the very top of a tall modern tower against a dark storm sky, clouds flickering. No real or recognisable building.", False),
        ("19_skyline_strike", 22, None, "Quality", "I", "20+ STRIKES A YEAR",
         "A modern city skyline at night; lightning strikes the rod on a tall tower again and again, and the tower stands calm. Short C frame 0.", False),
        ("20_table_three_again", 23, None, ("reuse", "P1:03_table_three"), "D", None, None, False),
        ("21_roofs_golden", 24, None, "Fast", "B", None,
         "A town at golden hour after a storm, a thin rod on every roof, wet tiles shining; slow drift over the rooftops.", False),
        ("22_newton_handoff", 25, None, "Quality", "—", None,
         "An English garden at dusk: an apple falls from a tree; the Moon hangs above it. Slow push.", False),
    ],
}

# Plates that must be Quality on Flow (fragile light) can still fall back to Vertex Quality.
SHOT_LIST_REF = "07_Edit-Project/SHOT_LIST_v01.md"


def fmt(t: float) -> str:
    return f"{int(t // 60)}:{t % 60:05.2f}"


def key(w: str) -> str:
    return re.sub(r"[^a-z']", "", w.lower().replace("’", "'"))


def at(part: dict, s: int, word: str | None) -> float:
    sent = part["sentences"][s - 1]
    if word is None:
        return sent["film_s"]
    for t, w in part["words"]:
        if sent["start_s"] - 0.01 <= t <= sent["end_s"] and key(w) == word:
            return round(part["vo_film_start_s"] + t, 2)
    raise SystemExit(f"part {part['part']}: word {word!r} not heard in sentence {s}: {sent['text']}")


def main() -> None:
    parts = {p["part"]: p for p in RETIME["parts"]}
    rows_by_key: dict[str, dict] = {}
    boards = {}
    short: list[tuple] = []
    for n, part in parts.items():
        part_end = parts[n + 1]["card_in_film_s"] if n < len(parts) else part["vo_film_end_s"] + TAIL_S
        anchored = []
        for pid, s, word, q, set_, label, body, explorer in ROWS[n]:
            t = at(part, s, word)
            row = {"id": pid, "t_s": round(t, 2), "t": fmt(t), "set": set_, "explorer": explorer,
                   "side_label": label}
            if isinstance(q, tuple):
                row.update({"quality": "reuse", "reuse_of": q[1], "engine_reason": REUSE_REASON})
            else:
                reason = (Q_FACE if "face" in body or "guests" in body or "fellows" in body else Q_LIGHT) if q == "Quality" else \
                    (F_HANDS if "hands" in body.lower() and "Close" in body else
                     F_INK if "parchment" in body or "page" in body or "drawing" in body else
                     F_WIDE if "wide" in body.lower() or "small" in body else
                     F_HELD if "Held" in body else F_DAY)
                row.update({"quality": q, "engine_reason": reason,
                            "prompt": STYLE + body + (EXPLORER_TAIL if explorer else TAIL)})
                if explorer:
                    row["reference"] = "01_Character/05_Generation-References/hos-explorer-reference-v01.jpg"
            anchored.append(row)
        anchored.sort(key=lambda r: r["t_s"])
        rows = []
        for i, r in enumerate(anchored):
            end = anchored[i + 1]["t_s"] if i + 1 < len(anchored) else part_end
            span = round(end - r["t_s"], 2)
            if span < MIN_PLATE_S - 1e-6:
                short.append((n, r["id"], r["t"], span))
            pieces = max(1, math.ceil(span / CLIP_USE_S - 1e-9))
            step = span / pieces
            for k in range(pieces):
                t0 = round(r["t_s"] + k * step, 2)
                t1 = round(r["t_s"] + (k + 1) * step, 2) if k + 1 < pieces else end
                if k == 0:
                    row = dict(r)
                else:
                    prev = rows[-1]
                    row = {"id": f"{r['id']}_c{k}", "t_s": t0, "t": fmt(t0), "set": r["set"], "explorer": False,
                           "side_label": None, "added": True}
                    if r["quality"] == "reuse":
                        row.update({"quality": "reuse", "reuse_of": r["reuse_of"], "engine_reason": REUSE_REASON})
                    else:
                        body = r["prompt"][len(STYLE):]
                        row.update({"quality": r["quality"], "engine_reason": CONT_REASON, "i2v_from": f"P{n}:{prev['id']} last frame",
                                    "prompt": STYLE + f"Same shot continues from the last frame of {prev['id']}, camera keeps moving: " + body.replace(" Short A frame 0.", "").replace(" Short B frame 0.", "").replace(" Short C frame 0.", "")})
                        if r["explorer"]:
                            row["prompt"] = row["prompt"].replace(EXPLORER_TAIL, TAIL).replace("the Explorer", "the empty set")
                row["use_s"] = round(t1 - t0, 2)
                sents = part["sentences"]
                lines = [x["text"] for x in sents if t0 - 0.05 <= x["film_s"] < t1 - 0.05]
                first = max((x for x in sents if x["film_s"] <= t0 + 0.05), key=lambda x: x["film_s"], default=None)
                if first is not None and (not lines or first["text"] != lines[0]):
                    lines.insert(0, f"(continues) {first['text']}")
                row["vo_land"] = lines
                rows.append(row)
        for r in rows:
            rows_by_key[f"P{n}:{r['id']}"] = r
        boards[n] = (part, part_end, rows)
    if short:
        raise SystemExit(f"plates under {MIN_PLATE_S} s:\n" + "\n".join(f"  part {n} {pid} at {t}: {u} s" for n, pid, t, u in short))

    need = {k: min(r["use_s"] + REUSE_PAD_S, 8.0) for k, r in rows_by_key.items() if r["quality"] != "reuse"}
    for k, r in rows_by_key.items():
        if r["quality"] != "reuse":
            continue
        src = r["reuse_of"]
        assert src in need, (k, src)
        own = rows_by_key[src]["use_s"]
        clip_in = own + 0.1 if own + 0.1 + r["use_s"] + REUSE_PAD_S <= 8.0 else max(0.0, CLIP_USE_S - r["use_s"])
        end = clip_in + r["use_s"]
        r["clip_in_s"] = round(clip_in, 2)
        r["reuse_window"] = f"{clip_in:.2f}-{end:.2f} s of {src}" + ("" if clip_in >= own else " (overlaps its own window)")
        need[src] = max(need[src], min(end + REUSE_PAD_S, 8.0))

    cum_flow = 0
    cum_vx = 0.0
    for k, r in rows_by_key.items():
        if r["quality"] == "reuse":
            r.update({"route": "reuse", "flow_credits_try1": 0, "flow_credits_expected": 0, "vertex_clip_s": 0,
                      "vertex_try1_gbp": 0.0, "vertex_expected_gbp": 0.0})
            continue
        q = r["quality"]
        clip = next(L for L in VERTEX_LENGTHS if L >= need[k] - 1e-6)
        try1 = USD_PER_S[q] * clip * GBP_PER_USD
        exp = try1 * TAKES_PER_KEEP[q] + STILLS_PER_PLATE * USD_PER_STILL * GBP_PER_USD
        fexp = math.ceil(FLOW_CREDITS[q] * TAKES_PER_KEEP[q])
        cum_flow += fexp
        cum_vx += exp
        r.update({"route": "flow-first", "flow_model": f"Veo 3.1 {q}", "flow_clip_s": 8,
                  "flow_credits_try1": FLOW_CREDITS[q], "flow_credits_expected": fexp,
                  "cum_flow_credits_expected": cum_flow,
                  "vertex_model": "veo-3.1-generate-001" if q == "Quality" else "veo-3.1-fast-generate-001",
                  "vertex_clip_s": clip, "vertex_try1_gbp": round(try1, 2), "vertex_expected_gbp": round(exp, 2),
                  "cum_vertex_expected_gbp": round(cum_vx, 2)})

    totals = {"rows": 0, "mints": 0, "Quality": 0, "Fast": 0, "reuse": 0, "added": 0, "explorer": 0,
              "flow_credits_try1": 0, "flow_credits_expected": 0, "vertex_try1_gbp": 0.0, "vertex_expected_gbp": 0.0}
    per_part = []
    for n, (part, part_end, rows) in boards.items():
        nq = sum(r["quality"] == "Quality" for r in rows)
        nf = sum(r["quality"] == "Fast" for r in rows)
        nr = sum(r["quality"] == "reuse" for r in rows)
        na = sum(bool(r.get("added")) for r in rows)
        ne = sum(bool(r["explorer"]) for r in rows)
        assert ne <= 1, (n, ne)
        board = {k: v for k, v in TEMPLATE.items() if k not in ("plates", "open_stamp", "vo_duration_s", "vo_file")}
        board.update({
            "part": f"{n:02d}",
            "title": f"Part {n:02d} — {part['chapter_card'] or 'Fire From the Sky'}",
            "film": "008_Lightning-Franklin",
            "working_title": "Why Did Franklin Fly a Kite in a Storm?",
            "mint": False,
            "status": "BOARD_V01",
            "house": ("STUDIO_PLAYBOOK.md §5 · rows from 07_Edit-Project/SHOT_LIST_v01.md (Claude, 6 Oct 2026), "
                      "timed from the locked VO (VO_RETIME_v01.json) and priced by Cursor, 12 Oct 2026 "
                      "(_build_plate_boards_v01.py, J0184). Rows marked `added` carry a shot past one clip. "
                      "Chief's price pass and Claude's review before any mint."),
            "vo_file": f"02_Voiceover/{part['file']}",
            "vo_sha256": part["sha256"],
            "vo_duration_s": part["duration_s"],
            "chapter_card": None if n == 1 else {
                "text": part["chapter_card"], "in_s": part["card_in_film_s"], "hold_s": 1.5,
                "treatment": "soft cross-fade after the part's end + 0.6 s breath; music continues",
            },
            "set_language": "Sets A-K as SHOT_LIST_v01.md §Sets; say 'same <place> 1752 set' for continuity; never 'same DNA' in a prompt.",
            "rules": [
                "No electrocution spectacle: sparks are small and blue; nobody is struck; Richmann's room only, then a flash and a cut.",
                "The kite is never struck; charge is a soft glow or fibres lifting, never a bolt down the string.",
                "William is about twenty-one, never a child; Franklin mid-forties, plain short wig, no spectacles (FACT_NOTES P1).",
                "No readable text in any plate; every LABEL, date and page text is an overlay in the edit (house type).",
                "WHO/WHEN cards for Franklin, William Franklin and Georg Richmann are edit overlays with years from FACT_NOTES (AGENTS.md Teach on screen: VO-locked film, overlays only).",
            ],
            "vo_film_start_s": part["vo_film_start_s"],
            "part_end_film_s": round(part_end, 2),
            "clip_use_s": CLIP_USE_S,
            "xfade_s": 0.35,
            "explorer_plates": ne,
            "counts": {"rows": len(rows), "mints": nq + nf, "Quality": nq, "Fast": nf, "reuse": nr, "added": na},
            "plates": rows,
        })
        (OUT / f"part-{n:02d}_plates_v01.json").write_text(json.dumps(board, indent=2, ensure_ascii=False) + "\n")
        pp = {"part": n, "rows": len(rows), "Quality": nq, "Fast": nf, "reuse": nr, "added": na,
              "flow_credits_try1": sum(r["flow_credits_try1"] for r in rows),
              "flow_credits_expected": sum(r["flow_credits_expected"] for r in rows),
              "vertex_try1_gbp": round(sum(r["vertex_try1_gbp"] for r in rows), 2),
              "vertex_expected_gbp": round(sum(r["vertex_expected_gbp"] for r in rows), 2)}
        per_part.append(pp)
        for f in ("rows", "Quality", "Fast", "reuse", "added", "flow_credits_try1", "flow_credits_expected",
                  "vertex_try1_gbp", "vertex_expected_gbp"):
            totals[f] += pp[f]
        totals["mints"] += nq + nf
        totals["explorer"] += ne
        print(f"part {n:02d}: {len(rows)} rows ({na} added) = {nq} Quality + {nf} Fast + {nr} reuse; "
              f"Flow {pp['flow_credits_expected']} cr expected · Vertex £{pp['vertex_expected_gbp']:.2f} expected")
    totals["vertex_try1_gbp"] = round(totals["vertex_try1_gbp"], 2)
    totals["vertex_expected_gbp"] = round(totals["vertex_expected_gbp"], 2)
    usable_vx = round(VERTEX_BALANCE_GBP - VERTEX_MARGIN_GBP, 2)
    plan = {
        "film": "008_Lightning-Franklin",
        "written": "2026-10-12",
        "task": "J0184 (OWB queue, repo hos): plate boards from the locked VO; mint nothing; parked for Chief's price pass",
        "shot_list": SHOT_LIST_REF,
        "readings": {"flow_credits_left": FLOW_CREDITS_LEFT, "flow_note": "AI Ultra refill not landed at 15:47Z 12 Oct",
                     "vertex_free_trial_gbp": VERTEX_BALANCE_GBP, "vertex_margin_gbp": VERTEX_MARGIN_GBP,
                     "vertex_usable_gbp": usable_vx,
                     "vertex_note": "HOS 006 (J0107/J0160) goes first on the Vertex trial; trial ends 11 Nov"},
        "rates": {"flow_credits_per_take": FLOW_CREDITS, "vertex_usd_per_s": USD_PER_S, "usd_per_still": USD_PER_STILL,
                  "gbp_per_usd_planning": GBP_PER_USD, "takes_per_keep_005": TAKES_PER_KEEP,
                  "stills_per_plate_005": STILLS_PER_PLATE},
        "vo_film_total_s": RETIME["vo_film_total_s"],
        "totals": totals,
        "per_part": per_part,
        "all_on_flow_credits_expected": totals["flow_credits_expected"],
        "all_on_vertex_gbp_expected": totals["vertex_expected_gbp"],
        "fits_now": {"flow": totals["flow_credits_expected"] <= FLOW_CREDITS_LEFT,
                     "vertex": totals["vertex_expected_gbp"] <= usable_vx},
        "price_pass_questions": [
            "Which `added` continuation rows become reuses of KEEP clips instead (SHOT_LIST §Size: Fast cutaways first, never Part 04 proof beats)?",
            "Flow/Vertex split once the Ultra refill lands: Quality on Flow is 100 credits a take, so the Quality share decides it.",
            "Picture waits for the VO-first batch and its credit; nothing here is minted.",
        ],
    }
    PLAN.write_text(json.dumps(plan, indent=2, ensure_ascii=False) + "\n")
    print(f"film: {totals['rows']} rows ({totals['added']} added) = {totals['Quality']} Quality + {totals['Fast']} Fast + "
          f"{totals['reuse']} reuse, {totals['explorer']} Explorer")
    print(f"all on Flow: {totals['flow_credits_try1']} cr try-1 · {totals['flow_credits_expected']} cr expected (have {FLOW_CREDITS_LEFT})")
    print(f"all on Vertex: £{totals['vertex_try1_gbp']:.2f} try-1 · £{totals['vertex_expected_gbp']:.2f} expected (usable £{usable_vx:.2f})")


if __name__ == "__main__":
    main()
