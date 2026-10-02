#!/usr/bin/env python3
"""HOS 005: build parts/part-0N_plates_v01.json from VO_RETIME_v01.json.

One plate per VO beat. Each plate names the sentence it lands on (`s`, 1-based
inside the part) plus an optional offset into that sentence (`off`, seconds).
Plate start/length come from the recorded VO, so re-running after a re-time
keeps the boards honest.

  python3 07_Edit-Project/_build_plate_boards_v01.py
"""
from __future__ import annotations

import json
from pathlib import Path

PROJ = Path(__file__).resolve().parents[1]
RETIME = json.loads((PROJ / "07_Edit-Project/VO_RETIME_v01.json").read_text())
OUT = PROJ / "07_Edit-Project/parts"
SCRIPT = "01_Script/blood_script_master_v02.md"

CLIP_USE_S = 7.9
MIN_PLATE_S = 2.4
TAIL_S = 0.6

HARVEY = (
    "William Harvey, a short man of about forty, olive skin, black hair to the collar, "
    "small pointed black beard and moustache, dark keen eyes, black physician's gown "
    "with a plain white falling collar"
)
HARVEY_YOUNG = (
    "young William Harvey, about twenty-two, olive skin, black hair, first thin beard, "
    "dark keen eyes, dark student's gown"
)
HARVEY_OLD = (
    "old William Harvey, about seventy-five, white hair and small white pointed beard, "
    "same olive skin and dark eyes, black gown"
)
GALEN = "Galen, a Greek doctor of about fifty, curly grey hair and beard, cream Greek robe"
FABRICIUS = (
    "Fabricius, an old Italian professor, long white beard, black scholar's cap and robe"
)
MALPIGHI = (
    "Marcello Malpighi, a doctor of about thirty-three, long dark curled wig, "
    "brown 1660s coat with white cravat"
)
EXPLORER = (
    "Exactly ONE Explorer, on model: a young boy, messy wavy brown hair (full crown), "
    "round thin gold glasses, long teal coat, tan waistcoat, brown bow tie, satchel. "
    "He acts, then leaves."
)

FORBIDDEN = (
    "HARD REJECT: Orbit robot; photoreal; Ken Burns or still push; gore, wounds, blood on "
    "skin, cut flesh or real animal organs (animal hearts only as Harvey's ink drawings); "
    "live or dead animals on a table; lava drip / molten bead; underside lamp bulb or "
    "shade cup; unfinished flat cards; garbled writing; unfinished Explorer hair; DNA "
    "helix; readable text or logos baked into the plate (labels and the De Motu Cordis "
    "title are added in the edit); twin Explorer; faces in the first two seconds of the "
    "film. Never say 'same DNA' or 'lab DNA' in a Veo prompt."
)
ALWAYS_FAILS = [
    "lava drip / molten bead",
    "underside lamp bulb / shade cup",
    "unfinished flat cards",
    "garbled card text or wrong sums (2 oz, 1/8, 1000 checked by hand)",
    "unfinished Explorer hair or melted face",
    "Explorer without glasses",
    "horizontal ghosting in late shots",
    "DNA helix",
    "Orbit robot",
    "Ken Burns ship",
    "gore: wound, blood on skin, cut flesh, real animal organs",
    "a face in the first two seconds of the film",
]
SET_LANGUAGE = (
    "Warm candlelit 17th-century world: dark oak, cream linen, brass, leather books, "
    "London fog. Body cutaways are clean, glowing illustrations (warm red arteries, cool "
    "blue veins), never anatomical gore. Say 'same 1616 London lecture room' or 'same "
    "Harvey study' for continuity; never 'same DNA'."
)

# (id, s, off, quality, explorer, side_label, prompt)
P = {
    1: dict(
        title="The Used-Up Blood (cold open, no chapter card)",
        explorer_lock="NONE this part (STUDIO_PLAYBOOK §3: never in the first minute). Hands only, no faces before plate 07.",
        open_stamp=None,
        plates=[
            ("01_pulse_wrist", 1, 0, "Quality", False, "YOUR PULSE",
             "Frame 0: extreme close-up of a relaxed human wrist resting palm-up on dark oak, two fingertips pressed on the pulse, already moving. The skin is softly translucent cartoon skin: a warm glowing red stream races up the forearm in time with each beat; the camera follows it up the arm to a softly glowing beating cartoon heart. Hand and arm only, no face. No wound, no blood on skin."),
            ("02_bread_liver", 2, 0, "Quality", False, "MADE, THEN USED UP",
             "An old oak table with a round loaf of bread and a pewter cup. They melt into a milky white glowing stream that flows into a smooth stylised glowing cartoon liver, which pours out bright warm red streams that spread into a faint outline of arms and legs and soak away like water into sand."),
            ("03_band_tightens", 3, 0, "Quality", False, "ONE BAND",
             "A bare upper arm resting on a candlelit oak table, arm and hand only, no face. Two hands wrap a strip of cream linen round the upper arm and pull it tight; below the band the veins on the forearm slowly swell into soft blue cords. Clean skin, no wound, no blood."),
            ("04_sum_page", 4, 0, "Quality", False, "A SUM",
             "Dark oak desk by candlelight. A cream paper page with three short lines of large, clear brown-ink handwriting: '2 oz', '1/8', '1000'. A quill rests beside it and the candle flame flickers softly; camera glides slowly across the page. The numbers stay sharp and correct."),
            ("05_linen_band", 4, 3.6, "Quality", False, "A BAND",
             "Same candlelit oak desk. A coiled strip of cream linen lies beside the page of sums; it slowly uncoils as if gently tugged from out of frame. Soft candle glow."),
            ("06_vein_press", 4, 7.0, "Fast", False, "A VEIN",
             "Close-up of the back of a relaxed hand on the same oak desk, no face. A fingertip of the other hand presses a faint blue vein and slides along it; a tiny soft glow inside the vein stops at a small bump (a valve). Clean skin, no blood."),
            ("07_chained_book", 5, 0, "Quality", False, None,
             "A university lecture hall around 1600: a thick leather book chained to a carved oak lectern; rows of students in dark robes copy from it by candlelight, quills moving. The camera glides slowly past the candles towards the book."),
            ("08_body_backwards", 7, 0, "Quality", False, None,
             "Same lecture hall. A large painted anatomy chart of a stylised human figure, with the liver painted big and glowing gold at its centre, hangs on a cord; a draught makes the chart swing and slowly turn upside down. Candles gutter."),
            ("09_amen_corner", 8, 0, "Quality", False, "LONDON · 1616",
             "London, 1616, at dusk. A narrow foggy lane of timber-framed houses; a carved stone doorway lit by candle lanterns (the Royal College of Physicians). The camera pushes slowly through the fog towards the door. No readable signs."),
            ("10_harvey_chart", 9, 2.7, "Quality", False, "WILLIAM HARVEY",
             f"Inside a panelled, candlelit lecture room: {HARVEY}, stands beside a large painted chart of the heart on an easel, lifts a long wooden pointer to it and turns to his audience with a keen look. Readable, finished face."),
            ("11_quill_question", 10, 0, "Quality", False, None,
             "Close on Harvey's hand in a black sleeve dipping a quill and writing one large question mark on a blank cream page; the wet ink glints in candlelight; the camera eases in. Only the question mark on the page."),
            ("12_heart_clock", 12, 0, "Quality", False, None,
             "Same lecture room. The painted heart on Harvey's chart pulses, and its beat dissolves into the face of a brass table clock, ticking; Harvey's fingers tap the oak table once for each tick, counting."),
        ],
    ),
    2: dict(
        title="The Liver That Made Blood",
        explorer_lock="ONE beat (plate 13): the Explorer on the top rail of the empty Padua anatomy theatre, traces the little doors on Fabricius's drawing, then slips away. Attach 01_Character/05_Generation-References/hos-explorer-reference-v01.jpg.",
        open_stamp={"after_s": 1.5, "text": "Rome, c. AD 170", "treatment": "Didot italic side label in the edit"},
        plates=[
            ("01_galen_scrolls", 1, 0, "Quality", False, "GALEN · ROME, c. AD 170",
             f"Rome around AD 170, a lamplit study full of scroll racks: {GALEN}, writes on a scroll with a reed pen; the oil lamp glows cleanly. Camera drifts in."),
            ("02_galen_centuries", 2, 0, "Quality", False, None,
             "Galen's scrolls become heavy leather books down the centuries: shelves fill with copies, monks and then gowned doctors bow over them by candlelight. A continuous slow pan through time."),
            ("03_you_eat", 3, 0, "Fast", False, None,
             "A warm, clean cartoon cutaway of a seated person, simple glowing outline of the body: they take a bite of bread and a soft milky glow travels down into the belly. Friendly, clear, no anatomy gore."),
            ("04_milky_liver", 5, 0, "Quality", False, "FOOD → LIVER → BLOOD",
             "Same cutaway body. The milky stream flows into a smooth stylised liver, which glows and turns it warm red."),
            ("05_veins_soak", 6, 0, "Quality", False, None,
             "Same cutaway body. Warm red streams flow out along the veins into the arms and legs and fade away into the flesh like water into sand."),
            ("06_heart_stove", 7, 0, "Quality", False, "A STOVE, NOT A PUMP",
             "Same cutaway body. The heart glows like a little iron stove with a soft warm fire inside, warming the red blood that seeps slowly past it. Clean warm glow, no flames spitting."),
            ("07_septum_holes", 9, 0, "Quality", False, "INVISIBLE HOLES?",
             "A cutaway cartoon heart: a few red drops creep from the right side to the left through tiny imagined pores in the wall between the two sides; the pores flicker as if not really there."),
            ("08_doctors_believe", 10, 0, "Quality", False, None,
             "A candlelit room of gowned doctors around a chart of the heart with dotted holes drawn in its wall; they nod and point confidently at the holes nobody has seen."),
            ("09_vesalius_book", 12, 0, "Quality", False, "ANDREAS VESALIUS · 1555",
             "A great anatomy book lies open on a woodcut-style drawing of the heart (no readable text); a brass magnifying glass slides across the wall between its two sides by candlelight."),
            ("10_vesalius_nothing", 12, 6.5, "Quality", False, None,
             "Same open book. Through the magnifying glass the heart wall is solid and smooth: a single tiny drop of red ink beads against it and cannot pass."),
            ("11_why_believe", 13, 0, "Quality", False, None,
             "Galen's thick book on a lectern; students keep copying from it by candlelight as the candle burns down. Camera drifts."),
            ("12_padua_theatre", 15, 0, "Quality", False, "PADUA · c. 1600",
             "Padua around 1600: the steep wooden oval anatomy theatre, rings of carved rails rising around a small table, candlelit and empty. Camera rises slowly up the rails."),
            ("13_explorer_padua", 15, 5.0, "Quality", True, None,
             f"Same Padua anatomy theatre. {EXPLORER} He climbs to the top rail, looks down at the candlelit table, unrolls a drawing of a vein on the rail and traces its tiny paired flaps with one finger, then slips away into the shadows."),
            ("14_fabricius", 16, 0, "Quality", False, "FABRICIUS",
             f"Same Padua theatre. {FABRICIUS}, holds up a large drawing of a vein opened along its length, candlelight on his face."),
            ("15_little_doors", 17, 0, "Fast", False, "LITTLE DOORS (VALVES)",
             "Fabricius's drawing comes alive: a vein opened along its length, pairs of tiny flaps inside like little doors gently swinging. Warm parchment and ink look, no readable text."),
            ("16_pool_feet", 19, 0, "Fast", False, None,
             "Same living drawing: a faint red trickle runs down a leg vein and the little doors catch it, holding it back from pooling in the foot, as Fabricius imagined."),
            ("17_young_harvey", 20, 0, "Quality", False, None,
             f"Padua study by candlelight: {HARVEY_YOUNG}, studies Fabricius's vein drawing closely, frowns, then rolls it up carefully."),
            ("18_ship_england", 21, 0, "Fast", False, None,
             "Young Harvey with the rolled drawing under his arm walks up the gangplank of a wooden sailing ship at a misty dawn harbour; sails fill."),
        ],
    ),
    3: dict(
        title="The Sum That Broke the Old Idea",
        explorer_lock="ONE beat (plate 11): in Harvey's study the Explorer sets out a tiny jug for every heartbeat; the jugs fill the desk, spill onto the floor and march out of the door; he turns wide-eyed to the single loaf. Attach the Explorer reference.",
        open_stamp={"after_s": 1.5, "text": "London", "treatment": "Didot italic side label in the edit"},
        plates=[
            ("01_lecture_room", 1, 0, "Quality", False, None,
             f"Same 1616 London lecture room, cold and candlelit, oak panels, physicians on hard wooden benches; {HARVEY}, at the front moves his pointer across a huge painted heart chart."),
            ("02_back_bench", 2, 0, "Quality", False, None,
             "Point of view from a back bench of the same lecture room: breath mists in the cold, candle flames shiver, Harvey small and bright at the front."),
            ("03_slow_hearts", 3, 0, "Fast", False, "SLOW HEARTS",
             "Harvey's notebook on his desk: brown-ink drawings of the slow hearts of a frog and an eel with little sketch arrows; pages turn gently. Ink drawings only, no live animal, no readable text."),
            ("04_ink_heart_beats", 3, 4.5, "Fast", False, None,
             "Same notebook page: the ink drawing of the heart gently squeezes and relaxes on the paper, slow and easy to see."),
            ("05_stove_to_muscle", 5, 0, "Quality", False, "A MUSCLE",
             "The little glowing stove-heart from the cutaway cools and turns into a strong, clean cartoon heart muscle that squeezes firmly."),
            ("06_squeeze_pulse", 7, 0, "Quality", False, "SQUEEZE = PULSE",
             "Clean glowing cutaway: the cartoon heart squeezes and with each squeeze a ripple of warm red races down an artery in the arm to the wrist, where two fingertips feel it beat."),
            ("07_how_much", 8, 0, "Quality", False, None,
             f"Same Harvey study by candlelight: {HARVEY}, dips his quill and looks from a drawing of the heart to a blank page, thinking."),
            ("08_two_ounces", 10, 0, "Quality", False, "2 OUNCES",
             "Close on the page: Harvey's quill writes '2 oz' in large clear brown ink. The numbers stay sharp and correct."),
            ("09_one_eighth", 11, 0, "Quality", False, "ONE EIGHTH",
             "Same page: the quill writes '1/8' under '2 oz' in large clear brown ink."),
            ("10_thousand_beats", 12, 0, "Quality", False, "1,000 BEATS",
             "Same page: the quill writes '1000' under the other numbers in large clear brown ink; a brass clock ticks beside the page."),
            ("11_explorer_jugs", 13, 0, "Quality", True, None,
             f"Same Harvey study. {EXPLORER} He sets out a tiny pewter jug for every heartbeat; the jugs fill the desk, spill onto the floor and march in a line out of the door; he turns, wide-eyed, to a single loaf of bread on the table."),
            ("12_jug_tower", 15, 0, "Quality", False, "MORE THAN YOUR WHOLE BODY",
             "A tower of tiny red jugs rises beside a simple glowing outline of a human body that holds far less; the tower keeps growing past it."),
            ("13_eat_weight", 16, 3.5, "Fast", False, None,
             "A brass balance scale: on one pan a mountain of bread and food, on the other a simple wooden figure of a person; the food pan sinks and keeps sinking."),
            ("14_where_go", 18, 0, "Quality", False, None,
             "A glowing outline of a body: red drains out of its limbs and vanishes into nothing, leaving a faint question in the air (no letters)."),
            ("15_one_answer", 19, 0, "Quality", False, None,
             f"Same Harvey study: {HARVEY}, lifts his quill, the candle brightens on his face as the idea lands."),
            ("16_glowing_loop", 21, 0, "Quality", False, "THE SAME BLOOD",
             "Clean glowing cutaway: the same red stream leaves the heart through the arteries and comes back to it through blue veins, round and round, a glowing loop."),
            ("17_circulates", 22, 0, "Quality", False, "IT CIRCULATES",
             "Same glowing loop, seen whole on a simple body outline; the stream speeds up and runs steadily round."),
            ("18_one_minute", 23, 3.7, "Quality", False, "ONE LAP · ONE MINUTE",
             "Same glowing loop with a brass clock hand sweeping once round the circle as a single glowing drop completes one lap."),
            ("19_not_proof", 24, 0, "Quality", False, None,
             f"Same Harvey study: {HARVEY}, looks from his page of sums to a strip of cream linen on the desk and picks it up."),
        ],
    ),
    4: dict(
        title="The Tied Arm",
        explorer_lock="NONE this part.",
        open_stamp={"after_s": 1.5, "text": "Royal College of Physicians", "treatment": "Didot italic side label in the edit"},
        plates=[
            ("01_college_demo", 1, 0, "Quality", False, "NINE YEARS",
             f"Same 1616 London lecture room: {HARVEY}, demonstrates to rows of gowned physicians; candles burn down and are replaced as the seasons pass at the window."),
            ("02_linen_strip", 2, 0, "Quality", False, None,
             "Same lecture room: Harvey holds up a plain strip of cream linen to the benches."),
            ("03_tie_band", 3, 0, "Quality", False, "A TIGHT BAND",
             "A man's bare arm rests on the oak table, arm and hand only, no face. Harvey's hands tie the linen band round the upper arm and pull it tight. Clean skin, nothing gory."),
            ("04_hand_pale", 4, 0, "Quality", False, "NO BLOOD IN",
             "Same arm: below the band the hand slowly turns pale and cool; above the band a soft pulse throbs under the skin. Arm only, clean skin."),
            ("05_stopped", 6, 0, "Quality", False, None,
             "Clean glowing cutaway of the same arm: the tight band squeezes every vessel shut and the warm red stream stops dead at the band."),
            ("06_loosen", 8, 0, "Quality", False, None,
             "Same arm: Harvey's fingers loosen the linen band just a little. Arm only."),
            ("07_deep_arteries", 9, 1.3, "Quality", False, "DEEP ARTERIES",
             "Clean glowing cutaway: deep arteries inside the arm push warm red under the loosened band towards the hand."),
            ("08_veins_shut", 10, 0, "Quality", False, None,
             "Same cutaway: the blue veins near the skin stay pinched shut under the band, and blood piles up below it."),
            ("09_veins_swell", 11, 0, "Quality", False, None,
             "The real arm again: the hand flushes pink and the veins below the band swell into soft blue cords like ropes. Clean skin."),
            ("10_in_out", 12, 0, "Quality", False, "IN: ARTERIES · OUT: VEINS",
             "Clean glowing cutaway of the arm: red flows in deep down, blue flows back out near the skin, a simple loop."),
            ("11_knots", 13, 0, "Quality", False, None,
             "Close on the swollen blue vein on the forearm: small knots stand out along it. Clean skin."),
            ("12_valve", 15, 0, "Quality", False, "A VALVE",
             "The camera pushes into one knot and the skin becomes a clean cutaway: a pair of Fabricius's little doors inside the vein."),
            ("13_push_hand", 16, 0, "Quality", False, None,
             "Close on the forearm: a fingertip presses the vein and pushes the blood towards the hand. Clean skin."),
            ("14_stops_dead", 17, 0, "Quality", False, None,
             "Same vein: the pushed blood stops dead at the next knot, which bulges; cutaway glimpse of the little doors shut tight."),
            ("15_slides_heart", 18, 0, "Quality", False, None,
             "Same vein: the fingertip strokes the other way, towards the heart, and the blood slides through easily; the little doors swing open."),
            ("16_two_fingers", 19, 0, "Quality", False, None,
             "Two fingertips press a short stretch of the vein and slide apart, emptying it. Clean skin."),
            ("17_stays_empty", 20, 0, "Quality", False, None,
             "Same stretch stays flat and empty; then the finger nearer the hand lifts."),
            ("18_fills_below", 21, 0, "Quality", False, None,
             "Same stretch refills from below, from the hand side, in one smooth wave."),
            ("19_one_way", 22, 0, "Quality", False, "ONE WAY: TO THE HEART",
             "Clean glowing cutaway: a long vein with many pairs of little doors, all opening the same way towards the heart as the blood flows home."),
            ("20_steering_home", 23, 0, "Quality", False, None,
             "Fabricius's old drawing beside Harvey's new one: in Harvey's, the little doors turn like lock gates steering a glowing stream home to the heart."),
            ("21_your_hand", 25, 0, "Fast", False, None,
             "The back of a relaxed hand and inside of a wrist, no face, veins faintly blue under clean skin, soft daylight."),
            ("22_glow_home", 27, 0, "Quality", False, None,
             "Same hand: a soft warm glow moves along the veins from the hand up the wrist towards the arm, on its way home."),
            ("23_press_1628", 28, 0, "Quality", False, "FRANKFURT · 1628",
             "A wooden printing press by candlelight in Frankfurt: a small sheet comes off the press and is folded into a small book. The title page is left plain (title added in the edit)."),
            ("24_book_pages", 28, 5.0, "Quality", False, None,
             "Hands turn the pages of the small book: woodcut-style plates of a forearm with a band tied round it and the veins marked. No readable text."),
            ("25_whispers", 29, 0, "Fast", False, None,
             f"A London street: people point and whisper as {HARVEY}, walks past in his gown."),
            ("26_aubrey", 30, 4.2, "Quality", False, "JOHN AUBREY",
             "John Aubrey, a man in a long brown wig, writes in a notebook by candlelight; through the window, Harvey's door with patients walking away."),
            ("27_gap_open", 31, 0, "Quality", False, None,
             f"{HARVEY}, at a window at dusk looks at a drawing of the blood's loop with one part left blank."),
        ],
    ),
    5: dict(
        title="The Vessels He Never Saw",
        explorer_lock="ONE beat (plate 06): the Explorer leans in to Malpighi's microscope, adjusts his round glasses, looks, then pulls back with a gasp. Attach the Explorer reference.",
        open_stamp=None,
        plates=[
            ("01_loop_gap", 1, 0, "Quality", False, "HOW DOES IT CROSS?",
             "The glowing loop from Part 03: at the far end, where the red arteries should meet the blue veins, there is a dark gap and the glow fades."),
            ("02_tiny_gaps", 3, 0, "Quality", False, None,
             "A soft, warm magnified view of flesh: red seeps through tiny unseen gaps, blurred and uncertain, as Harvey guessed."),
            ("03_old_harvey", 4, 0, "Quality", False, "WILLIAM HARVEY · 1578–1657",
             f"London in the 1650s: {HARVEY_OLD}, at a window, a candle by his book; he closes it gently."),
            ("04_bologna", 6, 0, "Quality", False, "MARCELLO MALPIGHI · BOLOGNA 1661",
             f"Bologna, 1661: {MALPIGHI}, at a brass microscope by a bright window, adjusting it."),
            ("05_slide", 6, 5.0, "Fast", False, None,
             "Close on Malpighi's hands placing a thin glass slide with a pale pink film on it under the brass lens. No animal on screen."),
            ("06_explorer_scope", 7, 0, "Quality", True, None,
             f"Same Bologna study. {EXPLORER} He leans in to the brass microscope, adjusts his round glasses, looks, then pulls back with a gasp."),
            ("07_eyepiece_mesh", 8, 2.7, "Quality", False, None,
             "Through the eyepiece in a soft round vignette: a mesh of tiny vessels finer than hairs joins a red artery to a blue vein; blood creeps through."),
            ("08_capillaries", 9, 0, "Quality", False, "CAPILLARIES",
             "Same mesh beside a single hair for scale; the tiny vessels glow as the blood creeps through them."),
            ("09_loop_closes", 10, 0, "Quality", False, None,
             "The glowing loop closes: heart, arteries, capillaries, veins and back to the heart, glowing all the way round."),
            ("10_your_blood", 11, 3.4, "Quality", False, None,
             "A simple glowing body outline with the full circuit lit: out through the arteries, across the capillaries, home through the veins."),
            ("11_question", 12, 0, "Quality", False, None,
             "Same glowing circuit pulses steadily."),
            ("12_one_vein", 13, 0, "Quality", False, "ONE VEIN REACHES ALL",
             "A single soft blue glow enters one vein of the glowing body outline and spreads round the whole circuit."),
            ("13_transfusion", 14, 0, "Quality", False, "FIRST TRANSFUSIONS · 1660s",
             "1660s, candlelit: two physicians in wigs bend over a table with a slender silver tube, a quill and a pewter bowl. Tools only: no animal, no patient, no blood."),
            ("14_tools", 14, 5.5, "Quality", False, None,
             "Close on the silver tube and quills laid out on linen by candlelight; a hand writes in a ledger (no readable text)."),
            ("15_cuff", 16, 0, "Fast", False, "HARVEY'S BAND, TODAY",
             "A modern blood pressure cuff tightens round a bare upper arm, arm only, no face, in a bright clean room."),
            ("16_cuff_release", 18, 0, "Fast", False, None,
             "Same cuff eases off; a stethoscope disc listens at the inside of the elbow. Arm only, no face."),
            ("17_band_table", 19, 0, "Quality", False, None,
             "Harvey's linen band on the old oak table in candlelight, beside the page of sums and Fabricius's vein drawing."),
            ("18_harvey_proved", 20, 0, "Quality", False, None,
             "Harvey's painted heart chart; the glowing loop draws itself over it and runs round."),
            ("19_last_link", 20, 4.4, "Quality", False, None,
             "Malpighi's brass microscope by the bright Bologna window, the last link, glowing softly."),
            ("20_dutch_lens", 21, 0, "Quality", False, "DELFT · 1674",
             "A cloth merchant's hand holds a tiny brass lens up to a window; a drop of pond water on a glass sliver beside it."),
            ("21_pond_life", 21, 4.8, "Quality", False, None,
             "Through the lens: a drop of pond water full of tiny faceless moving shapes (rods, spheres, spirals), soft glow, always moving."),
        ],
    ),
}


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    parts = {p["part"]: p for p in RETIME["parts"]}
    nparts = len(parts)
    for n, spec in P.items():
        part = parts[n]
        sents = part["sentences"]
        vo0 = part["vo_film_start_s"]
        if n < nparts:
            part_end = parts[n + 1]["card_in_film_s"]
        else:
            part_end = part["vo_film_end_s"] + TAIL_S
        rows = []
        for pid, s, off, q, exp, label, prompt in spec["plates"]:
            sent = sents[s - 1]
            t = sent["film_s"] + off
            rows.append({
                "id": pid,
                "t_s": round(t, 2),
                "t": f"{int(t // 60)}:{t % 60:05.2f}",
                "explorer": exp,
                "quality": q,
                "side_label": label,
                "vo_land": sent["text"] if off == 0 else f"(+{off:.1f} s into) {sent['text']}",
                "prompt": "Premium Animistry-class 3D cartoon. " + prompt + " Silent. Continuous motion through the final frame."
                + ("" if exp else " No Explorer."),
            })
        for i, r in enumerate(rows):
            end = rows[i + 1]["t_s"] if i + 1 < len(rows) else part_end
            r["use_s"] = round(end - r["t_s"], 2)
            assert MIN_PLATE_S <= r["use_s"] <= CLIP_USE_S, (n, r["id"], r["use_s"])
        n_exp = sum(r["explorer"] for r in rows)
        board = {
            "film": "005_How-Harvey-Proved-Blood-Circulates",
            "working_title": "The Tied Arm That Proved Your Blood Circulates",
            "part": f"{n:02d}",
            "title": spec["title"],
            "status": "BOARD_V01",
            "mint": n == 1,
            "house": "STUDIO_PLAYBOOK.md §5 · re-timed from VO v01 (VO_RETIME_v01.json)",
            "script": SCRIPT,
            "vo_file": f"02_Voiceover/{part['file']}",
            "vo_sha256": part["sha256"],
            "vo_duration_s": part["duration_s"],
            "chapter_card": None if n == 1 else {
                "text": part["chapter_card"], "in_s": part["card_in_film_s"], "hold_s": 1.5,
                "treatment": "soft cross-fade after the last word + 0.6 s breath; music continues",
            },
            "vo_film_start_s": vo0,
            "part_end_film_s": round(part_end, 2),
            "clip_use_s": CLIP_USE_S,
            "xfade_s": 0.35,
            "open_stamp": spec["open_stamp"],
            "set_language": SET_LANGUAGE,
            "explorer_lock": spec["explorer_lock"],
            "explorer_plates": n_exp,
            "forbidden": FORBIDDEN,
            "always_fails": ALWAYS_FAILS,
            "motion_lock": "Real Veo camera and object motion on every plate. No freeze-pad, no loop, no Ken Burns.",
            "quality_note": "Flow Veo 3.1 on the Mac Mini CDP worker, benoats@googlemail.com only. Quality for anything with light (candles, glowing loop, stove heart) and every hero plate; Fast only for low-risk garnish. One plate at a time until the first KEEP; after 2 same-framing FAILs change the framing.",
            "labels": "White Didot italic side label, 1-4 words, one at a time, on the plate's first beat; added in the edit.",
            "plates": rows,
        }
        path = OUT / f"part-{n:02d}_plates_v01.json"
        path.write_text(json.dumps(board, indent=2, ensure_ascii=False) + "\n")
        q = sum(r["quality"] == "Quality" for r in rows)
        print(f"part {n:02d}: {len(rows)} plates ({q} Quality, {len(rows)-q} Fast, Explorer {n_exp}) → {path.name}")


if __name__ == "__main__":
    main()
