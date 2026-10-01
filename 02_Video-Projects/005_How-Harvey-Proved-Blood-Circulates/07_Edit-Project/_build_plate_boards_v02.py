#!/usr/bin/env python3
"""HOS 005: build parts/part-0N_plates_v02.json from VO_RETIME_v01.json.

v02 (Claude desk task, 1 Oct 2026): 97 plates -> 75. Neighbouring beats that share
one location and one action are one plate whose action carries every VO line in
its window; a plate stays separate wherever the picture must change to match the
words (STUDIO_PLAYBOOK §5 mute test). Every plate is <= 7.9 s (one Veo clip).

Engine per plate: Quality only where the hero of the plate is an emissive or
fragile light (candle flame in frame, glowing loop or cutaway, stove heart,
lanterns). Where candlelight is only the room's ambience the plate is Fast and
its prompt keeps every flame, lantern and lamp out of frame. Reason in
`engine_reason`.

Each plate names the sentence it starts on (`s`, 1-based inside the part) and an
offset into it (`off`, seconds; negative = that much before the sentence).

  python3 07_Edit-Project/_build_plate_boards_v02.py
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
CREDITS = {"Quality": 100, "Fast": 20}

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
AMBIENT = " Warm candlelight falls from out of frame; no candle, flame, lantern or lamp in shot."

FORBIDDEN = (
    "HARD REJECT: Orbit robot; photoreal; Ken Burns or still push; gore, wounds, blood on "
    "skin, cut flesh or real animal organs (animal hearts only as Harvey's ink drawings); "
    "live or dead animals on a table; lava drip / molten bead; underside lamp bulb or "
    "shade cup; unfinished flat cards; garbled writing; unfinished Explorer hair; DNA "
    "helix; readable text or logos baked into the plate (labels and the De Motu Cordis "
    "title are added in the edit); twin Explorer; faces in the first two seconds of the "
    "film; a flame, lantern or lamp in frame on a Fast plate. Never say 'same DNA' or "
    "'lab DNA' in a Veo prompt."
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
    "a flame, lantern or lamp in frame on a Fast plate (remint on Quality or reframe)",
]
SET_LANGUAGE = (
    "Warm candlelit 17th-century world: dark oak, cream linen, brass, leather books, "
    "London fog. Body cutaways are clean, glowing illustrations (warm red arteries, cool "
    "blue veins), never anatomical gore. Say 'same 1616 London lecture room' or 'same "
    "Harvey study' for continuity; never 'same DNA'."
)

Q_GLOW = "Quality: the glowing cutaway, stream or loop is the hero (emissive light)."
Q_STOVE = "Quality: the glowing stove heart is the hero (emissive light)."
Q_FLAME = "Quality: candle flames or lanterns are in frame as the hero light."
F_AMB = "Fast: candlelight is room ambience only; prompt keeps every flame, lantern and lamp out of frame."
F_DAY = "Fast: daylight or window light; nothing emissive in frame."
F_INK = "Fast: ink, paper and props; nothing emissive in frame."
F_ARM = "Fast: real arm and hand on clean skin; nothing emissive in frame."
F_EXP = "Fast: no flame or lamp in frame. Explorer hard fails (glasses, full hair, one Explorer) checked on UAT; remint if off-model."

# (id, s, off, quality, engine_reason, explorer, side_label, merged_from_v01, prompt)
P = {
    1: dict(
        title="The Used-Up Blood (cold open, no chapter card)",
        explorer_lock="NONE this part (STUDIO_PLAYBOOK §3: never in the first minute). Hands only, no faces before 0:27.",
        open_stamp=None,
        plates=[
            ("01_pulse_wrist", 1, 0, "Quality", Q_GLOW, False, "YOUR PULSE", ["01_pulse_wrist"],
             "Frame 0: extreme close-up of a relaxed human wrist resting palm-up on dark oak, two fingertips pressed on the pulse, already moving. The skin is softly translucent cartoon skin: a warm glowing red stream races up the forearm in time with each beat; the camera follows it up the arm to a softly glowing beating cartoon heart. Hand and arm only, no face. No wound, no blood on skin."),
            ("02_bread_liver", 2, 0, "Quality", Q_GLOW, False, "MADE, THEN USED UP", ["02_bread_liver"],
             "An old oak table with a round loaf of bread and a pewter cup. They melt into a milky white glowing stream that flows into a smooth stylised glowing cartoon liver, which pours out bright warm red streams that spread into a faint outline of arms and legs and soak away like water into sand."),
            ("03_band_tightens", 3, 0, "Fast", F_ARM, False, "ONE BAND", ["03_band_tightens"],
             "A bare upper arm resting on an oak table, arm and hand only, no face. Two hands wrap a strip of cream linen round the upper arm and pull it tight; below the band the veins on the forearm slowly swell into soft blue cords; the camera eases along the forearm. Clean skin, no wound, no blood." + AMBIENT),
            ("04_sum_band_doors", 4, 3.98, "Fast", F_INK, False, "A SUM → A BAND → TINY DOORS (one at a time, on each word)", ["04_sum_page", "05_linen_band", "06_vein_press"],
             "Dark oak desk. One slow continuous camera glide from left to right across three things, in this order: a cream paper page with three short lines of large, clear brown-ink handwriting, '2 oz', '1/8', '1000'; a coiled strip of cream linen that slowly uncoils as if gently tugged; an ink drawing of a vein opened along its length, with pairs of tiny flaps inside like little doors that gently swing open. The numbers stay sharp and correct." + AMBIENT),
            ("05_chained_book", 5, 0, "Fast", F_AMB, False, None, ["07_chained_book"],
             "A university lecture hall around 1600: a thick leather book chained to a carved oak lectern; rows of students in dark robes copy from it, quills moving. The camera glides slowly along the benches towards the book." + AMBIENT),
            ("06_body_backwards", 7, 0, "Fast", F_AMB, False, None, ["08_body_backwards"],
             "Same lecture hall. A large painted anatomy chart of a stylised human figure, with the liver painted big and gold at its centre, hangs on a cord; a draught makes the chart swing and slowly turn upside down." + AMBIENT),
            ("07_harvey_college_door", 8, 0, "Quality", Q_FLAME, False, "LONDON · 1616 → WILLIAM HARVEY (+1.6 s)", ["09_amen_corner", "10_harvey_chart"],
             f"London, 1616, at dusk. A narrow foggy lane of timber-framed houses; a carved stone doorway lit by two candle lanterns (the Royal College of Physicians). The camera pushes slowly through the fog; {HARVEY}, walks into frame, climbs the step to the lantern-lit door, pauses and turns with a keen look before going in. Readable, finished face. No readable signs."),
            ("08_quill_question", 10, -1.28, "Fast", F_AMB, False, None, ["11_quill_question"],
             "Close on Harvey's hand in a black sleeve dipping a quill and writing one large question mark on a blank cream page; the wet ink glints; the camera eases in. Only the question mark on the page." + AMBIENT),
            ("09_heart_clock", 12, 0, "Fast", F_AMB, False, None, ["12_heart_clock"],
             "Panelled lecture room. A painted heart on a chart pulses, and its beat dissolves into the face of a brass table clock, ticking; Harvey's fingers tap the oak table once for each tick, counting." + AMBIENT),
        ],
    ),
    2: dict(
        title="The Liver That Made Blood",
        explorer_lock="ONE beat (plate 11): the camera rises up the empty Padua anatomy theatre to the Explorer on the top rail; he traces the little doors on Fabricius's drawing, then slips away. Attach 01_Character/05_Generation-References/hos-explorer-reference-v01.jpg.",
        open_stamp={"after_s": 1.5, "text": "Rome, c. AD 170", "treatment": "Didot italic side label in the edit"},
        plates=[
            ("01_galen_scrolls", 1, 0, "Fast", F_AMB, False, "GALEN · ROME, c. AD 170", ["01_galen_scrolls"],
             f"Rome around AD 170, a study full of scroll racks: {GALEN}, writes on a scroll with a reed pen. Camera drifts in." + AMBIENT.replace("candlelight", "lamplight")),
            ("02_galen_centuries", 2, 0, "Fast", F_AMB, False, None, ["02_galen_centuries"],
             "Galen's scrolls become heavy leather books down the centuries: shelves fill with copies, monks and then gowned doctors bow over them. A continuous slow pan through time." + AMBIENT),
            ("03_eat_to_liver", 4, 0, "Quality", Q_GLOW, False, "FOOD → LIVER → BLOOD (on 'liver')", ["03_you_eat", "04_milky_liver"],
             "A warm, clean cartoon cutaway of a seated person, simple glowing outline of the body: they take a bite of bread and a soft milky glow travels down into the belly, flows into a smooth stylised liver, which glows and turns it warm red. Friendly, clear, no anatomy gore."),
            ("04_veins_soak", 6, 0, "Quality", Q_GLOW, False, None, ["05_veins_soak"],
             "Same cutaway body. Warm red streams flow out along the veins into the arms and legs and fade away into the flesh like water into sand."),
            ("05_heart_stove", 7, 0, "Quality", Q_STOVE, False, "A STOVE, NOT A PUMP", ["06_heart_stove"],
             "Same cutaway body. The heart glows like a little iron stove with a soft warm fire inside, warming the red blood that seeps slowly past it. Clean warm glow, no flames spitting."),
            ("06_septum_holes", 9, 0, "Quality", Q_STOVE, False, "INVISIBLE HOLES?", ["07_septum_holes"],
             "Close on the same glowing stove heart in the cutaway: a few red drops creep from the right side to the left through tiny imagined pores in the wall between the two sides; the pores flicker as if not really there."),
            ("07_doctors_believe", 10, 0, "Fast", F_AMB, False, None, ["08_doctors_believe"],
             "A room of gowned doctors around a chart of the heart with dotted holes drawn in its wall; they nod and point confidently at the holes nobody has seen." + AMBIENT),
            ("08_vesalius_book", 12, 0, "Fast", F_INK, False, "ANDREAS VESALIUS · 1555", ["09_vesalius_book"],
             "A great anatomy book lies open on a woodcut-style drawing of the heart (no readable text); a brass magnifying glass slides across the wall between its two sides." + AMBIENT),
            ("09_vesalius_nothing", 12, 6.5, "Fast", F_INK, False, None, ["10_vesalius_nothing"],
             "Same open book. Through the magnifying glass the heart wall is solid and smooth: a single tiny drop of red ink beads against it and cannot pass." + AMBIENT),
            ("10_why_believe", 13, 0, "Fast", F_AMB, False, None, ["11_why_believe"],
             "Galen's thick book on a lectern; students keep copying from it and the stack of finished copies beside them grows taller. Camera drifts." + AMBIENT),
            ("11_padua_explorer", 15, 0, "Fast", F_EXP, True, "PADUA · c. 1600", ["12_padua_theatre", "13_explorer_padua"],
             f"Padua around 1600: the steep wooden oval anatomy theatre, rings of carved rails rising around a small empty table. The camera rises slowly up the rails to the top rail, where {EXPLORER} He unrolls a drawing of a vein on the rail, traces its tiny paired flaps with one finger, then slips away into the shadows." + AMBIENT),
            ("12_fabricius", 15, 7.9, "Fast", F_AMB, False, "FABRICIUS", ["14_fabricius"],
             f"Same Padua theatre. {FABRICIUS}, holds up a large drawing of a vein opened along its length and points to the pairs of tiny flaps inside it." + AMBIENT),
            ("13_little_doors", 17, -0.12, "Fast", F_INK, False, "LITTLE DOORS (VALVES)", ["15_little_doors"],
             "Fabricius's drawing comes alive: a vein opened along its length, pairs of tiny flaps inside like little doors gently swinging. Warm parchment and ink look, no readable text."),
            ("14_pool_feet", 19, 0, "Fast", F_INK, False, None, ["16_pool_feet"],
             "Same living drawing: a faint red trickle runs down a leg vein and the little doors catch it, holding it back from pooling in the foot, as Fabricius imagined."),
            ("15_harvey_ship", 20, 0.2, "Fast", F_DAY, False, None, ["17_young_harvey", "18_ship_england"],
             f"Deck of a wooden sailing ship at a misty dawn harbour: {HARVEY_YOUNG}, studies Fabricius's vein drawing closely, frowns, rolls it up carefully under his arm and looks out as the sails fill and the ship moves off towards England."),
        ],
    ),
    3: dict(
        title="The Sum That Broke the Old Idea",
        explorer_lock="ONE beat (plate 08): in Harvey's study the Explorer sets out a tiny jug for every heartbeat; the jugs fill the desk, spill onto the floor and march out of the door; he turns wide-eyed to the single loaf. Attach the Explorer reference.",
        open_stamp={"after_s": 1.5, "text": "London", "treatment": "Didot italic side label in the edit"},
        plates=[
            ("01_cold_lecture_room", 1, 0, "Quality", Q_FLAME, False, None, ["01_lecture_room", "02_back_bench"],
             f"Point of view from a hard back bench of the same 1616 London lecture room, cold and candlelit, oak panels: breath mists in the cold, candle flames shiver in the foreground; at the front {HARVEY}, moves his pointer across a huge painted heart chart."),
            ("02_slow_hearts", 3, -0.05, "Fast", F_INK, False, "SLOW HEARTS", ["03_slow_hearts", "04_ink_heart_beats"],
             "Harvey's notebook on his desk: brown-ink drawings of the slow hearts of a frog and an eel with little sketch arrows; pages turn gently, and on the last page the ink drawing of the heart slowly squeezes and relaxes on the paper. Ink drawings only, no live animal, no readable text." + AMBIENT),
            ("03_stove_to_muscle", 4, -0.17, "Quality", Q_STOVE, False, "A MUSCLE (on 'muscle', +4.2 s)", ["05_stove_to_muscle"],
             "The little glowing stove-heart from the cutaway cools and turns into a strong, clean cartoon heart muscle that squeezes firmly, again and again."),
            ("04_squeeze_pulse", 7, 0, "Quality", Q_GLOW, False, "SQUEEZE = PULSE", ["06_squeeze_pulse"],
             "Clean glowing cutaway: the cartoon heart squeezes and with each squeeze a ripple of warm red races down an artery in the arm to the wrist, where two fingertips feel it beat."),
            ("05_how_much", 8, 0, "Fast", F_AMB, False, None, ["07_how_much"],
             f"Same Harvey study: {HARVEY}, dips his quill and looks from a drawing of the heart to a blank page, thinking." + AMBIENT),
            ("06_two_ounces_eighth", 10, 0, "Fast", F_INK, False, "2 OUNCES → ONE EIGHTH (+3.7 s)", ["08_two_ounces", "09_one_eighth"],
             "Close on a cream page: Harvey's quill writes '2 oz' in large clear brown ink, then writes '1/8' underneath it. The numbers stay sharp and correct." + AMBIENT),
            ("07_thousand_beats", 12, 0, "Fast", F_INK, False, "1,000 BEATS", ["10_thousand_beats"],
             "Same page: the quill writes '1000' under '2 oz' and '1/8' in large clear brown ink; a brass clock ticks beside the page. The numbers stay sharp and correct." + AMBIENT),
            ("08_explorer_jugs", 13, 0, "Fast", F_EXP, True, None, ["11_explorer_jugs"],
             f"Same Harvey study. {EXPLORER} He sets out a tiny pewter jug for every heartbeat; the jugs fill the desk, spill onto the floor and march in a line out of the door; he turns, wide-eyed, to a single loaf of bread on the table." + AMBIENT),
            ("09_jug_tower", 15, 0, "Fast", F_INK, False, "MORE THAN YOUR WHOLE BODY", ["12_jug_tower"],
             "A tower of tiny red pewter jugs rises beside a plain pale outline of a human body that holds far less; the tower keeps growing past it. Soft daylight, nothing glowing."),
            ("10_eat_weight", 16, 3.5, "Fast", F_DAY, False, None, ["13_eat_weight"],
             "A brass balance scale: on one pan a mountain of bread and food, on the other a simple wooden figure of a person; the food pan sinks and keeps sinking."),
            ("11_where_go", 18, 0, "Quality", Q_GLOW, False, None, ["14_where_go", "15_one_answer"],
             "A glowing outline of a body: red drains out of its limbs and vanishes into nothing; then the last of the drained glow stops in the air, hangs, and begins to drift back towards the body (no letters)."),
            ("12_glowing_loop", 21, 0, "Quality", Q_GLOW, False, "THE SAME BLOOD → IT CIRCULATES (+6.5 s)", ["16_glowing_loop", "17_circulates"],
             "Clean glowing cutaway: the same red stream leaves the heart through the arteries and comes back to it through blue veins, round and round; the camera pulls back to see the whole glowing loop on a simple body outline as the stream runs steadily round."),
            ("13_one_minute", 23, -0.56, "Quality", Q_GLOW, False, "ONE LAP · ONE MINUTE", ["18_one_minute"],
             "Same glowing loop with a brass clock hand sweeping once round the circle as a single glowing drop completes one lap."),
            ("14_not_proof", 24, -0.44, "Fast", F_AMB, False, None, ["19_not_proof"],
             f"Same Harvey study: {HARVEY}, looks from his page of sums to a strip of cream linen on the desk and picks it up." + AMBIENT),
        ],
    ),
    4: dict(
        title="The Tied Arm",
        explorer_lock="NONE this part.",
        open_stamp={"after_s": 1.5, "text": "Royal College of Physicians", "treatment": "Didot italic side label in the edit"},
        plates=[
            ("01_college_demo", 1, 0, "Fast", F_AMB, False, "NINE YEARS", ["01_college_demo"],
             f"Same 1616 London lecture room: {HARVEY}, demonstrates to rows of gowned physicians while the seasons pass at the tall window, snow to blossom to autumn leaves." + AMBIENT),
            ("02_linen_tie", 2, 0, "Fast", F_ARM, False, "A TIGHT BAND (+3.5 s)", ["02_linen_strip", "03_tie_band"],
             "Same lecture room: Harvey holds up a plain strip of cream linen, then ties it round a man's bare upper arm resting on the oak table and pulls it tight. Arm, hand and Harvey's hands only, no face of the man. Clean skin, nothing gory." + AMBIENT),
            ("03_hand_pale", 4, -0.02, "Fast", F_ARM, False, "NO BLOOD IN", ["04_hand_pale"],
             "Same arm: below the band the hand slowly turns pale and cool; above the band a soft pulse throbs under the skin. Arm only, clean skin." + AMBIENT),
            ("04_stopped_loosen", 6, 0, "Quality", Q_GLOW, False, None, ["05_stopped", "06_loosen"],
             "Clean glowing cutaway of the same arm: the tight band squeezes every vessel shut and the warm red stream stops dead at the band; then the band eases open just a little."),
            ("05_arteries_veins_shut", 9, 0, "Quality", Q_GLOW, False, "DEEP ARTERIES", ["07_deep_arteries", "08_veins_shut"],
             "Same glowing cutaway: deep arteries inside the arm push warm red under the loosened band towards the hand, while the blue veins near the skin stay pinched shut under the band and blood piles up below it."),
            ("06_veins_swell", 10, 1.98, "Fast", F_ARM, False, None, ["09_veins_swell"],
             "The real arm again, band still on: the hand flushes pink and the veins below the band swell into soft blue cords like ropes. Clean skin." + AMBIENT),
            ("07_in_out_doors", 12, 0, "Quality", Q_GLOW, False, "IN: ARTERIES · OUT: VEINS", ["10_in_out"],
             "Clean glowing cutaway of the arm: red flows in deep down, blue flows back out near the skin, a simple loop; the camera then glides along a blue vein towards a pair of little doors inside it."),
            ("08_knots_valve", 14, 0, "Quality", Q_GLOW, False, "A VALVE (+3.6 s)", ["11_knots", "12_valve"],
             "Close on the swollen blue vein on the forearm: small knots stand out along it. The camera pushes into one knot and the skin becomes a clean glowing cutaway: a pair of Fabricius's little doors inside the vein."),
            ("09_push_stops", 16, -0.28, "Fast", F_ARM, False, None, ["13_push_hand", "14_stops_dead"],
             "Close on the forearm: a fingertip presses the vein and pushes the blood towards the hand; it stops dead at the next knot, which bulges. Clean skin." + AMBIENT),
            ("10_slides_heart", 18, 0, "Fast", F_ARM, False, None, ["15_slides_heart"],
             "Same vein: the fingertip strokes the other way, towards the heart, and the blood slides through easily; the bulging knot flattens. Clean skin." + AMBIENT),
            ("11_two_fingers", 19, 0, "Fast", F_ARM, False, None, ["16_two_fingers"],
             "Two fingertips press a short stretch of the vein and slide apart, emptying it. Clean skin." + AMBIENT),
            ("12_stays_fills", 20, 0, "Fast", F_ARM, False, None, ["17_stays_empty", "18_fills_below"],
             "Same stretch of vein stays flat and empty between the two fingertips; then the finger nearer the hand lifts and the stretch refills from below, from the hand side, in one smooth wave. Clean skin." + AMBIENT),
            ("13_one_way", 22, 0, "Quality", Q_GLOW, False, "ONE WAY: TO THE HEART", ["19_one_way"],
             "Clean glowing cutaway: a long vein with many pairs of little doors, all opening the same way towards the heart as the blood flows home."),
            ("14_steering_home", 23, 0, "Fast", F_INK, False, None, ["20_steering_home"],
             "Fabricius's old ink drawing beside Harvey's new one on an oak desk: in Harvey's, the little ink doors turn like lock gates and a red ink stream flows through them home to the heart. Ink and parchment, nothing glowing." + AMBIENT),
            ("15_your_hand_glow", 25, 0.78, "Quality", Q_GLOW, False, None, ["21_your_hand", "22_glow_home"],
             "The back of a relaxed hand and inside of a wrist in soft daylight, no face, veins faintly blue under clean skin; a soft warm glow moves along the veins from the hand up the wrist towards the arm, on its way home."),
            ("16_press_book", 28, 0, "Fast", F_AMB, False, "FRANKFURT · 1628 (De Motu Cordis title overlay on the book)", ["23_press_1628", "24_book_pages"],
             "A wooden printing press in Frankfurt: a small sheet comes off the press and is folded into a small book with a plain title page; hands open it and turn to woodcut-style plates of a forearm with a band tied round it and the veins marked. No readable text (title added in the edit)." + AMBIENT),
            ("17_whispers", 29, -1.86, "Fast", F_DAY, False, None, ["25_whispers"],
             f"A London street by day: people point and whisper as {HARVEY}, walks past in his gown."),
            ("18_aubrey", 30, 3.94, "Fast", F_AMB, False, "JOHN AUBREY", ["26_aubrey"],
             "John Aubrey, a man in a long brown wig, writes in a notebook; through the window, Harvey's door with patients walking away." + AMBIENT),
            ("19_gap_open", 31, 0, "Fast", F_DAY, False, None, ["27_gap_open"],
             f"{HARVEY}, at a window at dusk looks at a drawing of the blood's loop with one part left blank."),
        ],
    ),
    5: dict(
        title="The Vessels He Never Saw",
        explorer_lock="ONE beat (plate 05): the Explorer leans in to Malpighi's microscope, adjusts his round glasses, looks, then pulls back with a gasp. Attach the Explorer reference.",
        open_stamp=None,
        plates=[
            ("01_loop_gap", 1, 0, "Quality", Q_GLOW, False, "HOW DOES IT CROSS?", ["01_loop_gap"],
             "The glowing loop from Part 03: at the far end, where the red arteries should meet the blue veins, there is a dark gap and the glow fades."),
            ("02_tiny_gaps", 3, 0, "Fast", F_DAY, False, None, ["02_tiny_gaps"],
             "A soft, warm magnified view of flesh: red seeps through tiny unseen gaps, blurred and uncertain, as Harvey guessed. Nothing glowing."),
            ("03_old_harvey", 4, 0, "Fast", F_DAY, False, "WILLIAM HARVEY · 1578–1657", ["03_old_harvey"],
             f"London in the 1650s, soft evening window light: {HARVEY_OLD}, at a window with his book; he closes it gently. No candle or lamp in shot."),
            ("04_malpighi_slide", 6, 0, "Fast", F_DAY, False, "MARCELLO MALPIGHI · BOLOGNA 1661", ["04_bologna", "05_slide"],
             f"Bologna, 1661: {MALPIGHI}, at a brass microscope by a bright window, places a thin glass slide with a pale pink film under the lens and adjusts the focus. No animal on screen."),
            ("05_explorer_scope", 7, -0.8, "Fast", F_EXP, True, None, ["06_explorer_scope"],
             f"Same Bologna study by the bright window. {EXPLORER} He leans in to the brass microscope, adjusts his round glasses, looks, then pulls back with a gasp."),
            ("06_eyepiece_mesh", 8, 2.7, "Fast", F_DAY, False, None, ["07_eyepiece_mesh"],
             "Through the eyepiece in a soft round vignette: a mesh of tiny vessels finer than hairs joins a red artery to a blue vein; blood creeps through. Soft daylight look, nothing glowing."),
            ("07_capillaries_loop", 9, 0, "Quality", Q_GLOW, False, "CAPILLARIES", ["08_capillaries", "09_loop_closes"],
             "The mesh of tiny vessels beside a single hair for scale; they light up with a soft glow as the blood creeps through, then the camera pulls back and the glowing mesh becomes the missing link in the glowing loop: heart, arteries, capillaries, veins, and the loop closes."),
            ("08_your_blood", 11, 1.8, "Quality", Q_GLOW, False, None, ["10_your_blood"],
             "A simple glowing body outline with the full circuit lit: out through the arteries, across the capillaries, home through the veins."),
            ("09_question", 12, 0, "Quality", Q_GLOW, False, None, ["11_question"],
             "Close on the heart of the same glowing circuit, pulsing steadily as the stream runs out and back."),
            ("10_one_vein", 13, 0, "Quality", Q_GLOW, False, "ONE VEIN REACHES ALL", ["12_one_vein"],
             "A single soft blue glow enters one vein of the glowing body outline and spreads round the whole circuit."),
            ("11_transfusion", 14, 0, "Fast", F_AMB, False, "FIRST TRANSFUSIONS · 1660s", ["13_transfusion"],
             "1660s: two physicians in wigs bend over a table with a slender silver tube, a quill and a pewter bowl. Tools only: no animal, no patient, no blood." + AMBIENT),
            ("12_tools", 14, 5.5, "Fast", F_AMB, False, None, ["14_tools"],
             "Close on the silver tube and quills laid out on linen; a hand writes in a ledger (no readable text)." + AMBIENT),
            ("13_cuff", 16, 0, "Fast", F_DAY, False, "HARVEY'S BAND, TODAY", ["15_cuff"],
             "A modern blood pressure cuff tightens round a bare upper arm, arm only, no face, in a bright clean room."),
            ("14_cuff_release", 18, 0, "Fast", F_DAY, False, None, ["16_cuff_release"],
             "Same cuff eases off; a stethoscope disc listens at the inside of the elbow. Arm only, no face."),
            ("15_band_table", 19, 0, "Fast", F_AMB, False, None, ["17_band_table"],
             "Harvey's linen band on the old oak table, beside the page of sums and Fabricius's vein drawing." + AMBIENT),
            ("16_proved_last_link", 20, 0, "Quality", Q_GLOW, False, None, ["18_harvey_proved", "19_last_link"],
             "Harvey's painted heart chart; a glowing loop draws itself over it and runs round, and at the far end the last link, a fine glowing mesh of tiny vessels, lights up softly to close it."),
            ("17_dutch_lens", 21, -0.2, "Fast", F_DAY, False, "DELFT · 1674", ["20_dutch_lens"],
             "A cloth merchant's hand holds a tiny brass lens up to a window; a drop of pond water on a glass sliver beside it."),
            ("18_pond_life", 21, 4.8, "Quality", Q_GLOW, False, None, ["21_pond_life"],
             "Through the lens: a drop of pond water full of tiny faceless moving shapes (rods, spheres, spirals), soft glow, always moving."),
        ],
    ),
}


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    parts = {p["part"]: p for p in RETIME["parts"]}
    nparts = len(parts)
    totals = {"plates": 0, "Quality": 0, "Fast": 0, "credits": 0}
    for n, spec in P.items():
        part = parts[n]
        sents = part["sentences"]
        if n < nparts:
            part_end = parts[n + 1]["card_in_film_s"]
        else:
            part_end = part["vo_film_end_s"] + TAIL_S
        rows = []
        for pid, s, off, q, reason, exp, label, merged, prompt in spec["plates"]:
            t = sents[s - 1]["film_s"] + off
            rows.append({
                "id": pid,
                "t_s": round(t, 2),
                "t": f"{int(t // 60)}:{t % 60:05.2f}",
                "explorer": exp,
                "quality": q,
                "engine_reason": reason,
                "side_label": label,
                "merged_from_v01": merged,
                "prompt": "Premium Animistry-class 3D cartoon. " + prompt + " Silent. Continuous motion through the final frame."
                + ("" if exp else " No Explorer."),
            })
        for i, r in enumerate(rows):
            end = rows[i + 1]["t_s"] if i + 1 < len(rows) else part_end
            r["use_s"] = round(end - r["t_s"], 2)
            assert MIN_PLATE_S <= r["use_s"] <= CLIP_USE_S, (n, r["id"], r["use_s"])
            lines = [x["text"] for x in sents if r["t_s"] - 0.05 <= x["film_s"] < end - 0.05]
            first = max((x for x in sents if x["film_s"] <= r["t_s"] + 0.05), key=lambda x: x["film_s"], default=None)
            if first is not None and (not lines or first["text"] != lines[0]):
                lines.insert(0, f"(continues) {first['text']}")
            r["vo_land"] = lines
        n_exp = sum(r["explorer"] for r in rows)
        nq = sum(r["quality"] == "Quality" for r in rows)
        credits = sum(CREDITS[r["quality"]] for r in rows)
        board = {
            "film": "005_How-Harvey-Proved-Blood-Circulates",
            "working_title": "The Tied Arm That Proved Your Blood Circulates",
            "part": f"{n:02d}",
            "title": spec["title"],
            "status": "BOARD_V02",
            "mint": n == 1,
            "house": "STUDIO_PLAYBOOK.md §5 · re-timed from VO v01 (VO_RETIME_v01.json) · v02 merges (Claude desk task, 1 Oct 2026)",
            "script": SCRIPT,
            "vo_file": f"02_Voiceover/{part['file']}",
            "vo_sha256": part["sha256"],
            "vo_duration_s": part["duration_s"],
            "chapter_card": None if n == 1 else {
                "text": part["chapter_card"], "in_s": part["card_in_film_s"], "hold_s": 1.5,
                "treatment": "soft cross-fade after the last word + 0.6 s breath; music continues",
            },
            "vo_film_start_s": part["vo_film_start_s"],
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
            "quality_note": "Flow Veo 3.1 on the Mac Mini CDP worker, benoats@googlemail.com only. Quality only where the hero is an emissive or fragile light (flame in frame, glowing cutaway or loop, stove heart, lanterns); Fast where candlelight is room ambience and no flame, lantern or lamp is in frame. Reason per plate in engine_reason. A Fast take with a flame or lamp in frame fails: reframe or remint on Quality. One plate at a time until the first KEEP; after 2 same-framing FAILs change the framing.",
            "labels": "White Didot italic side label, 1-4 words, one at a time, on the plate's first beat (or at the stated offset); added in the edit. Never two at once.",
            "credits_try1": {"Quality": nq, "Fast": len(rows) - nq, "credits": credits,
                             "rate": "Quality ~100, Fast ~20 Flow credits per clip"},
            "plates": rows,
        }
        path = OUT / f"part-{n:02d}_plates_v02.json"
        path.write_text(json.dumps(board, indent=2, ensure_ascii=False) + "\n")
        totals["plates"] += len(rows)
        totals["Quality"] += nq
        totals["Fast"] += len(rows) - nq
        totals["credits"] += credits
        print(f"part {n:02d}: {len(rows)} plates ({nq} Quality, {len(rows)-nq} Fast, Explorer {n_exp}) "
              f"try-1 {credits} credits → {path.name}")
    print(f"film: {totals['plates']} plates ({totals['Quality']} Quality, {totals['Fast']} Fast) "
          f"try-1 {totals['credits']} credits")


if __name__ == "__main__":
    main()
