#!/usr/bin/env python3
"""HOS 006: build parts/part-0N_plates_v01.json and the priced plan from VO_RETIME_v02.json.

Claude desk task (PR #180 comment 5951184558, 2 Oct 2026): re-time the boards from VO v02,
as 005 v02, and price them: Quality vs Fast, Flow's 62 credits vs Vertex, first-take cost,
a retake allowance at 005's average rate, and which plates fall beyond the £0 floor.

Engine per plate (STUDIO_PLAYBOOK §5, Claude's steer): Quality only where a named person's
readable face is the hero, on every Explorer plate (UAT hard fail 4), and where a flame,
furnace, glow or sunbeam is the hero light. Everything else is Fast and its prompt keeps
flames, lamps and glows out of frame. Reason per plate in `engine_reason`.

Cheaper picture without losing quality:
- reuse: a later plate cuts a different window of an earlier KEEP clip (a callback), at no cost.
  The source plate is minted long enough to hold every window cut from it.
- Vertex clip length 4, 6 or 8 s (Veo 3.1 `duration_seconds`), the shortest that holds the
  plate's window plus REUSE_PAD_S; Flow clips are always 8 s.
- held establishing shots go on Flow Fast (10 credits a take).

Each plate names the sentence it starts on (`s`, 1-based inside the part) and an offset into
it (`off`, seconds). A plate runs to the next plate's start (or the part's end).

  python3 07_Edit-Project/_build_plate_boards_v01.py
"""
from __future__ import annotations

import json
import math
from pathlib import Path

PROJ = Path(__file__).resolve().parents[1]
EDIT = PROJ / "07_Edit-Project"
RETIME = json.loads((EDIT / "VO_RETIME_v02.json").read_text())
CREDIT_LOG = json.loads((EDIT / "VERTEX_CREDIT_LOG_v01.json").read_text())
OUT = EDIT / "parts"
PLAN = EDIT / "PICTURE_PLAN_v01.json"
SCRIPT = "01_Script/trees_script_master_v02.md"

CLIP_USE_S = 7.9
MIN_PLATE_S = 2.4
TAIL_S = 0.6
REUSE_PAD_S = 0.5  # cross-fade 0.35 s plus a little head room
VERTEX_LENGTHS = (4, 6, 8)

# Flow (read on the Mini's CDP Chrome, 2 Oct 2026, "Generating will use N credits")
FLOW_CREDITS_LEFT = 62
FLOW_COST = {"Lite [Lower Priority]": 0, "Lite": 5, "Fast": 10, "Quality": 100, "Nano Banana 2 still": 0}
FLOW_TAKES_PER_PLATE = 2  # 3 plates x 2 takes x 10 = 60 of the 62 credits
# Vertex list prices, video only 1080p, as 005's minter; GBP at the minter's conservative 0.80.
# 005 really cost £143.80 for $193.87 logged (209.53 -> 65.73), i.e. 0.742.
USD_PER_S = {"Quality": 0.20, "Fast": 0.10}
USD_PER_STILL = 0.039
GBP_PER_USD = 0.80
GBP_PER_USD_005_ACTUAL = round((209.53 - 65.73) / 193.87, 3)
# 005 v02 averages (PART01-05_MINT_LOG_v01.json): 70 Quality takes / 27 kept, 94 Fast / 48, 171 stills / 75 plates
TAKES_PER_KEEP = {"Quality": round(70 / 27, 2), "Fast": round(94 / 48, 2)}
STILLS_PER_PLATE = round(171 / 75, 2)

VAN_HELMONT = ("Jan Baptist van Helmont, a Flemish doctor of about forty, long dark wavy hair to the "
               "shoulders, moustache and small pointed beard, black coat with a plain white falling collar")
ARISTOTLE = "Aristotle, a Greek thinker of about fifty, short grey curly hair and a neat grey beard, cream Greek robe"
HALES = ("Stephen Hales, a round-faced, clean-shaven English parson of about fifty, short white wig, "
         "black clergyman's coat with white bands")
PRIESTLEY = "Joseph Priestley, a man of about thirty-eight, long face, strong nose, short grey wig, plain dark coat"
INGENHOUSZ = "Jan Ingenhousz, a Dutch doctor of about fifty, clean-shaven, round cheeks, powdered grey wig, brown coat"
SENEBIER = "Jean Senebier, a thin Genevan pastor of about forty, short dark hair, dark clerical coat with white bands at the neck"
SAUSSURE = "Nicolas-Théodore de Saussure, a young man of about thirty-five, dark hair, high white collar, dark coat"
EXPLORER = (
    "Exactly ONE Explorer, on model: a young boy, messy wavy brown hair (full crown), "
    "round thin gold glasses, long teal coat, tan waistcoat, brown bow tie, satchel. "
    "He acts, then leaves."
)
NOFLAME = " Daylight from out of frame; no candle, flame, lantern, lamp or fire in shot."

FORBIDDEN = (
    "HARD REJECT: Orbit robot; photoreal; Ken Burns or still push; a mouse or any animal hurt, "
    "dying or still (Priestley's mouse is only ever alive and lively); lava drip / molten bead; "
    "underside lamp bulb or shade cup; unfinished flat cards; garbled writing; unfinished Explorer "
    "hair; DNA helix; readable text or logos baked into the plate (labels, numbers and dates are "
    "added in the edit unless the plate says a quill writes them); twin Explorer; faces in the "
    "first two seconds of the film; a flame, lamp, furnace glow or glowing cutaway on a Fast plate. "
    "Never say 'same DNA' or 'lab DNA' in a Veo prompt."
)
ALWAYS_FAILS = [
    "lava drip / molten bead",
    "underside lamp bulb / shade cup",
    "unfinished flat cards",
    "garbled card text or wrong numbers (200, 5, 169, 62 checked by hand)",
    "unfinished Explorer hair or melted face",
    "Explorer without glasses",
    "horizontal ghosting in late shots",
    "DNA helix",
    "Orbit robot",
    "Ken Burns ship",
    "an animal hurt, dying or limp",
    "a face in the first two seconds of the film",
    "a flame, lamp or glow in frame on a Fast plate (remint on Quality or reframe)",
]
SET_LANGUAGE = (
    "Warm, sunlit natural-history world: oak, red brick, clay pots, glass jars, brass balances, "
    "green willow leaves. Van Helmont's walled garden at Vilvoorde (grey Flemish light, 1600s); "
    "Georgian English rooms (1700s); Geneva by the lake (1780s-1800s). Leaf cutaways are clean "
    "illustrated cross-sections. Say 'same Vilvoorde garden', 'same Priestley room' or 'same "
    "Ingenhousz sill' for continuity; never 'same DNA'."
)

Q_FACE = "Quality: a named person's readable face is the hero (first appearance)."
Q_EXP = ("Quality: explorer fidelity. Face and hair are UAT hard fail 4 (glasses, full hair, one Explorer); "
         "a Fast remint would cost more than the difference.")
Q_FLAME = "Quality: a candle flame, furnace or fire is in frame as the hero light (fragile light)."
Q_GLOW = "Quality: glowing threads of air, a lit cutaway or a glowing atom is the hero (emissive light)."
Q_SUN = "Quality: sunbeam glints on bubbles or a leaf are the hero (fragile light)."
F_HELD = "Fast: held establishing shot, slow push, no readable faces, nothing emissive."
F_DAY = "Fast: daylight or window light; nothing emissive in frame."
F_HANDS = "Fast: hands and props only, no face, nothing emissive."
F_WIDE = "Fast: wide shot, figures small and faces not readable, nothing emissive."
F_INK = "Fast: ink, paper, props or a flat illustrated diagram; nothing emissive."
F_CUT = "Fast: clean illustrated cutaway in soft daylight colours; nothing glows."

# Held establishing shots on Flow Fast (2 takes each on the 62 credits)
FLOW_PLATES = {"P1:09_vilvoorde", "P3:06_leeds_brewery", "P5:01_geneva_lake"}

R = "reuse"  # quality slot for a reuse row

# (id, s, off, quality, engine_reason, explorer, side_label, prompt or reuse(source_key, clip_in_s))
P = {
    1: dict(
        title="Plants Eat Soil (cold open, no chapter card)",
        explorer_lock="NONE this part (STUDIO_PLAYBOOK §3: never in the first minute). No face before 0:24 (Aristotle).",
        open_stamp=None,
        plates=[
            ("01_willow_air", 1, 0, "Quality", Q_GLOW, False, "MADE OF AIR",
             "Frame 0, already moving: a huge willow on a riverbank at golden hour. Fine glittering threads of air stream in through its leaves from every side and run down along the branches into the trunk, which glows faintly from within. Slow continuous push towards the trunk. No people."),
            ("02_balance_trunk", 2, 0, "Fast", F_DAY, False, "NOT THE SOIL",
             "A giant brass balance in a sunny field: a whole tree trunk lies on one pan and sinks; on the other pan a small heap of dark soil flies up, far too light. The camera drifts along the beam."),
            ("03_pot_jar_leaf", 3, 0, "Fast", F_DAY, False, "A POT · A JAR · THE SUN (one at a time)",
             "A sunlit oak table by a window. Three things appear one after another: a clay pot with a thin willow shoot, a glass jar turned over a green sprig of mint, and a green leaf in a jar of water beaded with tiny silver bubbles. The camera eases along them in that order." + NOFLAME),
            ("04_years_pass", 3, 7.5, "Fast", F_DAY, False, None,
             "Same sunlit table seen from above as time races: patches of sunlight sweep across it day after day, leaves outside the window flicker green, gold, bare and green again; the pot, the jar and the leaf stay put." + NOFLAME),
            ("05_olive_grove", 4, 0, "Fast", F_WIDE, False, None,
             "An ancient Greek olive grove on a hillside in hot sun: small farmers at a distance pile dark soil round the roots of young olive trees with their hands, as if feeding them. Slow drift between the trees."),
            ("06_aristotle", 5, 0, "Quality", Q_FACE, False, "ARISTOTLE",
             f"A sunny stone courtyard in ancient Athens: {ARISTOTLE}, stands beside a young olive tree and points down at its roots while explaining to two listening students. Readable, finished face. Camera eases in."),
            ("07_roots_mouths", 6, 0, "Fast", F_CUT, False, "ROOTS AS MOUTHS",
             "Cutaway below the young olive tree: its roots in dark earth open little round mouths and drink the soil, gulping as the camera sinks slowly down through the layers. Friendly, not creepy."),
            ("08_wood_food_air", 7, 3.0, "Fast", F_DAY, False, None,
             "A stack of split logs, a round loaf of bread and a man's misty breath on a cold morning in the same shot; each one drifts slowly in turn into focus as the camera pans. No faces." + NOFLAME),
            ("09_vilvoorde", 8, 0, "Fast", F_HELD, False, "VILVOORDE, NEAR BRUSSELS · EARLY 1600s",
             "Early 1600s, grey Flemish light: a red-brick town house with stepped gables and a walled garden behind it. Held wide shot, slow push towards the garden gate. No people in shot." + NOFLAME),
            ("10_van_helmont_sack", 8, 5.0, "Quality", Q_FACE, False, "JAN BAPTIST VAN HELMONT",
             f"Same Vilvoorde garden: {VAN_HELMONT}, heaves a sack of dark soil onto the pan of a big brass balance standing on the flagstones, and watches the beam settle. Readable, finished face."),
            ("11_shoot_in_pot", 11, 0, "Fast", F_HANDS, False, None,
             "Close on van Helmont's hands in black sleeves pressing a thin willow shoot into a big clay pot of dark soil and firming it in. Grey daylight." + NOFLAME),
            ("12_garden_sky", 12, 0, "Fast", F_DAY, False, None,
             "Same Vilvoorde garden: the clay pot with its little willow shoot alone on the flagstones while clouds race across the sky above in time-lapse and shadows swing round the walls." + NOFLAME),
        ],
    ),
    2: dict(
        title="Five Years and Two Ounces",
        explorer_lock="ONE beat (plate 07): in the snowy garden the Explorer lifts a corner of the pierced lid, rubs a pinch of soil, looks up the tall willow, scratches his head and walks off through the gate. Attach 01_Character/05_Generation-References/hos-explorer-reference-v01.jpg.",
        open_stamp={"after_s": 1.5, "text": "Vilvoorde", "treatment": "Didot italic side label in the edit"},
        plates=[
            ("01_furnace_soil", 1, 0, "Quality", Q_FLAME, False, "DRIED SOIL",
             f"A brick furnace in a Flemish workroom glows orange; {VAN_HELMONT}, slides out an iron tray of steaming dark soil with tongs and tips it into a big clay pot."),
            ("02_balance_200", 2, 3.5, "Fast", F_DAY, False, "200 POUNDS OF SOIL",
             "Same workroom by a grey window: the big clay pot of soil on one pan of a brass balance, iron weights stacked on the other until the beam is level; a quill writes a large clear '200' in a ledger. The number stays sharp." + NOFLAME),
            ("03_willow_shoot_scale", 3, 0, "Fast", F_DAY, False, "A 5-POUND WILLOW",
             "Same balance: a young willow shoot with bare roots lies alone on the pan, balanced by one small iron weight; the beam steadies." + NOFLAME),
            ("04_lid_rain", 4, 0, "Fast", F_DAY, False, "WATER IN, DUST OUT",
             "Same Vilvoorde garden: a round metal lid pierced with many tiny holes slides over the clay pot round the willow's stem; rain patters through the holes, while a puff of dust blown by the wind bounces off the lid."),
            ("05_pure_water", 5, 0, "Fast", F_DAY, False, None,
             "Close on the pierced lid of the pot: a copper watering can pours clear water that sparkles softly as it runs through the tiny holes into the soil." + NOFLAME),
            ("06_garden_years", 6, 0, "Fast", F_DAY, False, "FIVE YEARS",
             "Same Vilvoorde garden in one continuous time-lapse: spring leaves burst out on the willow in the clay pot, autumn leaves fall, snow settles, spring again; the willow climbs past the garden wall while the pot never changes." + NOFLAME),
            ("07_explorer_snow", 9, 0, "Quality", Q_EXP, True, None,
             f"Same Vilvoorde garden in snow, the willow now tall in its clay pot. {EXPLORER} He lifts a corner of the pierced lid, rubs a pinch of soil between finger and thumb, looks up and up the tall willow, scratches his head and walks off through the garden gate." + NOFLAME),
            ("08_haul_tree", 10, 0, "Fast", F_WIDE, False, None,
             "Same garden, wide: van Helmont and two helpers, small in frame, haul the tall dripping willow, roots and all, out of the clay pot and onto the big brass balance; iron weights pile up on the other pan." + NOFLAME),
            ("09_weights_169", 11, 0, "Fast", F_DAY, False, "169 POUNDS",
             "Close on the balance: one more iron weight lands and the beam levels; a quill writes a large clear '169' in the ledger. The number stays sharp." + NOFLAME),
            ("10_fallen_leaves", 12, 0, "Fast", F_DAY, False, None,
             "Same garden corner: four little heaps of dry willow leaves from four autumns, swept against the wall; a breeze lifts a few and lets them fall." + NOFLAME),
            ("11_furnace_again", 13, 0, R, None, False, None, ("P2:01_furnace_soil", 2.0)),
            ("12_pointer_short", 14, 1.5, "Fast", F_DAY, False, "SOIL LOST: ABOUT 2 OUNCES",
             "Close on the brass balance's pointer as the dried soil goes back on: it swings, slows and stops a hair short of its old mark. The camera pushes in on the tiny gap." + NOFLAME),
            ("13_tree_vs_pinch", 16, 0, "Fast", F_DAY, False, None,
             "The tall willow lies across a long oak table; at the far end a tiny pinch of dark soil sits in a silver spoon. The camera glides from the huge tree to the tiny pinch." + NOFLAME),
            ("14_why_grown", 17, 0, "Fast", F_WIDE, False, None,
             "Same garden, wide: van Helmont, small in frame with his back to us, stands beside the empty clay pot and looks up at the willow towering over the wall." + NOFLAME),
            ("15_desk_candle", 19, 0, "Quality", Q_FLAME, False, None,
             f"Van Helmont's study at night: {VAN_HELMONT}, writes by a single candle; its flame flickers on the page and on his thoughtful face."),
            ("16_water_drawing", 21, 0, "Fast", F_INK, False, '"FROM WATER ALONE"',
             "Close on a page with a brown-ink drawing of a tree; an inked stream of water pours into its roots and fills the trunk, the bark and the branches with blue. Ink and paper only, no readable text." + NOFLAME),
            ("17_mostly_wrong", 22, 0, "Fast", F_DAY, False, None,
             "Low angle up the tall willow from the empty clay pot; the wind shakes the leaves and a single leaf spins down onto the open ledger on the garden bench." + NOFLAME),
            ("18_charcoal_hearth", 23, 0, "Quality", Q_FLAME, False, None,
             f"A wide brick hearth: {VAN_HELMONT}, tips a heap of black charcoal onto it from a scoop; it catches and burns brightly, then sinks down and down."),
            ("19_ash_mound", 24, 3.6, "Fast", F_DAY, False, "62 POUNDS → 1 POUND OF ASH",
             "Close on the cold hearth: one small mound of pale grey ash where the great heap of charcoal had been; a brush sweeps it into a little dish on a balance." + NOFLAME),
            ("20_shimmer_coals", 25, 0, "Fast", F_DAY, False, None,
             "Same hearth, the fire out: a clear, invisible shimmer like heat haze rises off the grey coals and curls upward. Nothing glows; the shimmer only bends the bricks behind it." + NOFLAME),
            ("21_gas_window", 26, 0, "Fast", F_DAY, False, "GAS",
             "Same study by day: the clear shimmer drifts past van Helmont, small at his desk with his back to us, and slips out of the open window." + NOFLAME),
            ("22_shimmer_willow", 28, 0, "Fast", F_DAY, False, None,
             "The clear shimmer drifts across the Vilvoorde garden and into the willow's leaves, which tremble as it arrives; nobody notices." + NOFLAME),
        ],
    ),
    3: dict(
        title="The Air That Mint Repaired",
        explorer_lock="NONE this part.",
        open_stamp={"after_s": 1.5, "text": "Teddington", "treatment": "Didot italic side label in the edit"},
        plates=[
            ("01_soil_to_sky", 1, 0, "Fast", F_DAY, False, None,
             "Close on dark garden soil; the camera rises slowly up a plant stem, through leaves and out into a wide blue sky with drifting clouds." + NOFLAME),
            ("02_hales_branch", 2, 0, "Quality", Q_FACE, False, "STEPHEN HALES · 1727",
             f"A riverside churchyard garden at Teddington in the 1720s: {HALES}, seals a glass tube over the cut end of a leafy branch with wax and peers at the water level inside. Readable, finished face." + NOFLAME),
            ("03_water_level", 2, 6.5, "Fast", F_HANDS, False, None,
             "Close on the glass tube: the water level inside creeps down as the leafy branch drinks; Hales's finger marks the level with a little scratch." + NOFLAME),
            ("04_leaf_mist", 3, 0, "Fast", F_CUT, False, "FOOD FROM THE AIR?",
             "A clean illustrated cutaway of a leaf on its stem: water rises up the stem and drifts out of the leaf as fine mist, while a faint pale arrow of air drifts in towards it. Soft daylight colours; nothing glows."),
            ("05_guess", 5, 0, "Fast", F_INK, False, None,
             "Close on a page: a quill draws one large question mark beside a sketch of a leaf; a draught lifts the page's corner." + NOFLAME),
            ("06_leeds_brewery", 6, 0, "Fast", F_HELD, False, "LEEDS · 1771",
             "Leeds, 1771: a plain stone house beside a busy brewery, white steam rising from the vats into a grey sky. Held wide shot, slow push. No readable faces." + NOFLAME),
            ("07_priestley", 7, 4.5, "Quality", Q_FACE, False, "JOSEPH PRIESTLEY",
             f"Inside the brewery beside a great steaming vat: {PRIESTLEY}, holds a glass jar up into the rising air and studies it with delight. Readable, finished face." + NOFLAME),
            ("08_candles_out", 8, 2.0, "Quality", Q_FLAME, False, None,
             "Priestley's room: his hand lowers a lit candle on a wire into a tall glass jar standing in a bowl of water; the flame shrinks and goes out; a second lit candle lowered into the same jar goes out at once."),
            ("09_injured_air", 9, 0, "Fast", F_DAY, False, '"INJURED" AIR',
             "Close on the sealed glass jar in its bowl of water: a thin wisp of smoke curls from a dead wick inside and hangs, trapped." + NOFLAME),
            ("10_mint_jar", 10, 0, "Fast", F_HANDS, False, "ONE SPRIG OF MINT · 17 AUGUST",
             "Same jar: Priestley's hands slide a bright green sprig of mint in a little pot under it and seal it; beside it a small blank calendar card stands on the table (the date is added in the edit)." + NOFLAME),
            ("11_candle_tall", 11, 0, "Quality", Q_FLAME, False, "TEN DAYS LATER → THE AIR IS BACK",
             "Same jar, the mint now fuller: Priestley's hand lowers a lit candle on a wire into it and the flame burns tall and steady; the camera eases in on the flame."),
            ("12_mouse_mint", 13, 0, "Fast", F_DAY, False, "THE MOUSE LIVED",
             "Two glass jars side by side on Priestley's table: in the one with the mint, a small brown mouse sniffs about, lively and well, washing its whiskers. Wonder, not cruelty: the mouse is bright-eyed and busy." + NOFLAME),
            ("13_fires_breath", 15, -0.25, "Fast", F_WIDE, False, None,
             "A wide 1770s town at morning: chimneys smoking, people and cows breathing misty breath in the cold, carts moving. Small figures, no readable faces. The smoke stays in the chimney tops; no flames in shot."),
            ("14_trees_breathe", 17, 0, "Fast", F_DAY, False, None,
             "The camera pans from the smoky town to green countryside: woods and hedges gently breathing a faint clear shimmer back into the air." + NOFLAME),
            ("15_quill_vegetable", 18, 0, "Fast", F_HANDS, False, None,
             "Close on Priestley's hand writing with a quill in a notebook, the mint jar blurred beside it; no readable text." + NOFLAME),
            ("16_repair_reuse", 18, 4.5, R, None, False, "PLANTS REPAIR THE AIR", ("P3:14_trees_breathe", 3.0)),
            ("17_notebook_tick", 19, 0, "Fast", F_INK, False, "WHY ONLY SOMETIMES?",
             "Close on Priestley's notebook: one line gets a firm tick, the next line is crossed out; the quill hesitates. Marks only, no readable words." + NOFLAME),
            ("18_dark_window", 21, 0, "Fast", F_DAY, False, None,
             "The mint jar on the sill beside a dark evening window, the mint a little limp; the room grows dim and blue." + NOFLAME),
        ],
    ),
    4: dict(
        title="Bubbles in the Sunlight",
        explorer_lock="ONE beat (plate 08): the Explorer lifts a fizzing jar from the sunny sill, carries it into the shadow where the bubbles stop, steps back into the sunbeam where they start again, grins and sets it down. Attach the Explorer reference.",
        open_stamp={"after_s": 1.5, "text": "Summer 1779", "treatment": "Didot italic side label in the edit"},
        plates=[
            ("01_villa", 1, 0, "Fast", F_HELD, False, "A VILLA NEAR LONDON · 1779",
             "Summer 1779: a Georgian country house with tall windows in green fields; glass jars of water and leaves crowd every windowsill and glint in the sun. Held wide shot, slow push. No people." + NOFLAME),
            ("02_ingenhousz_jars", 2, 5.6, "Quality", Q_FACE, False, "JAN INGENHOUSZ",
             f"Inside the sunny house, jars of leaves on every sill and table: {INGENHOUSZ}, moves briskly along the rows, peering into each jar and noting it down. Readable, finished face." + NOFLAME),
            ("03_plunge_leaf", 3, 0, "Fast", F_HANDS, False, None,
             "Close on Ingenhousz's hands plunging a fresh green leaf into a clear jar of water on a sunny sill." + NOFLAME),
            ("04_sunny_window", 4, 0, "Fast", F_DAY, False, None,
             "Point of view at the tall sunny window: a row of jars with green leaves on the sill, warm sunlight falling across them, the summer fields beyond." + NOFLAME),
            ("05_bubbles_macro", 5, 2.5, "Quality", Q_SUN, False, "BUBBLES",
             "Macro: tiny silver bubbles bead on a green leaf under water in a sunbeam, swell, let go and rise to the top, glinting."),
            ("06_collect_blaze", 6, 0, "Quality", Q_FLAME, False, "OXYGEN (on the blaze)",
             "Ingenhousz's hands hold a small upside-down glass tube over the leaf jar to collect the rising bubbles; then a small candle flame lowered into the tube blazes up bright and tall."),
            ("07_priestley_callback", 8, 0, R, None, False, None, ("P3:11_candle_tall", 0.0)),
            ("08_explorer_shade", 9, 0, "Quality", Q_EXP, True, "NO LIGHT, NO BUBBLES",
             f"Same sunny room. {EXPLORER} He lifts a fizzing jar of leaves from the sunny sill and carries it into the shadow, where the bubbles stop; he steps back into the sunbeam where they start again, grins and sets it down." + NOFLAME),
            ("09_bubbles_again", 11, 0, R, None, False, None, ("P4:05_bubbles_macro", 4.2)),
            ("10_only_green", 12, 0, "Fast", F_DAY, False, "ONLY THE GREEN PARTS",
             "Three jars of water on the sunny sill: a pale root, a red flower and a green leaf; only the green leaf fizzes with bubbles." + NOFLAME),
            ("11_night_jars", 14, 0, "Quality", Q_FLAME, False, "AT NIGHT, LIKE US",
             "The same room at night, moonlight on the jars; a small candle burning inside a sealed plant jar slowly dims and shrinks."),
            ("12_shutters_open", 15, -0.1, "Fast", F_DAY, False, None,
             "Morning: a hand swings open a wooden shutter and daylight floods across the jars on the sill; the leaves lift a little." + NOFLAME),
            ("13_sun_canopy", 17, 0, "Fast", F_DAY, False, None,
             "Looking straight up through a sunny tree canopy, leaves fluttering, light dappling between them." + NOFLAME),
            ("14_leaf_glow", 19, 0, "Quality", Q_GLOW, False, "PHOTOSYNTHESIS (on the word, +4.6 s)",
             "A sunbeam pours into a clean illustrated cutaway of a leaf; the green cells inside glow as they catch the light, and tiny golden specks gather and join together."),
            ("15_leaf_turns_sun", 20, 3.3, "Fast", F_DAY, False, None,
             "A potted plant on the sunny sill slowly turns its leaves towards the window." + NOFLAME),
            ("16_pores_question", 21, 0, "Fast", F_DAY, False, "WHAT GOES IN?",
             "Close-up of the underside of a green leaf: tiny pores open and close like little mouths; a faint drift of clear air hangs just outside them." + NOFLAME),
        ],
    ),
    5: dict(
        title="Carbon From the Sky",
        explorer_lock="ONE beat (plate 20): under a great willow by a river the Explorer holds up an open hand in a sunbeam as if feeling invisible threads of air, watches a leaf turn to the light, smiles and walks away along the bank. Attach the Explorer reference.",
        open_stamp={"after_s": 1.5, "text": "Geneva, 1782", "treatment": "Didot italic side label in the edit"},
        plates=[
            ("01_geneva_lake", 1, 0, "Fast", F_HELD, False, "GENEVA · 1782",
             "Geneva in the 1780s: the old town above the blue lake with snowy mountains beyond, boats with white sails. Held wide shot, slow push. No readable faces." + NOFLAME),
            ("02_senebier_jars", 1, 4.5, "Quality", Q_FACE, False, "JEAN SENEBIER → FIXED AIR = CARBON DIOXIDE (+4.5 s)",
             f"A bright room above the lake: {SENEBIER}, bubbles gas from a bellows tube into one of two jars of water with leaves in the sun; that jar fizzes with bubbles while the other stays still. Readable, finished face." + NOFLAME),
            ("03_de_saussure", 2, 0, "Quality", Q_FACE, False, "DE SAUSSURE · 1804",
             f"A neat Geneva laboratory: {SAUSSURE}, lowers a glass bell over a small potted plant and seals its rim. Readable, finished face." + NOFLAME),
            ("04_fine_scales", 2, 6.0, "Fast", F_HANDS, False, None,
             "Close on fine brass scales: de Saussure's hands weigh the sealed plant, a flask of water and a glass globe of air in turn, adding tiny weights with tweezers." + NOFLAME),
            ("05_sums_add_up", 4, 0, "Fast", F_INK, False, None,
             "Close on a ledger: a quill draws a firm line under two columns of marks that balance exactly; no readable numbers." + NOFLAME),
            ("06_leaf_in", 5, 0.6, "Fast", F_CUT, False, None,
             "A clean illustrated cutaway of a willow leaf: little pale bubbles of carbon dioxide drift in through tiny pores on its underside, and water rises up from the stem. Soft daylight colours; nothing glows."),
            ("07_sugar_oxygen", 7, 0, "Quality", Q_GLOW, False, "AIR + WATER + LIGHT → SUGAR + OXYGEN",
             "Same leaf cutaway: sunlight pours in and the leaf glows warm green; the carbon dioxide and water join into tiny golden grains of sugar, and small clear bubbles of oxygen float out of the pores."),
            ("08_sugar_wood", 8, 0, "Fast", F_DAY, False, "SUGAR BECOMES WOOD",
             "A cutaway willow in a riverside meadow: honey-coloured sap flows down from the leaves through the branches and trunk and lays down new rings of wood, bark and roots. Nothing glows." + NOFLAME),
            ("09_helmont_willow", 9, 0, R, None, False, None, ("P2:06_garden_years", 4.0)),
            ("10_air_threads", 10, 0, R, None, False, "HALF IS CARBON · FROM THE AIR", ("P1:01_willow_air", 0.5)),
            ("11_trunk_pie", 11, 0, "Fast", F_INK, False, None,
             "A clean cross-section slice of a willow trunk on a plain cream background: the rings divide into wedges like a pie chart, one half dark, most of the rest two lighter wedges, and a thin sliver. No letters (labels added in the edit)."),
            ("12_scales_barely", 12, 0, R, None, False, None, ("P2:12_pointer_short", 1.0)),
            ("13_water_in_tree", 13, 0, R, None, False, None, ("P2:05_pure_water", 0.0)),
            ("14_built_from_sky", 15, 0, "Fast", F_DAY, False, None,
             "The camera rises slowly up a great willow's trunk from its roots into the leaves against a bright open sky." + NOFLAME),
            ("15_food_glow", 17, 0, "Quality", Q_GLOW, False, "YOUR FOOD BEGAN AS AIR",
             "A loaf of bread, a bowl of rice and a red apple on a wooden table, each with a little warm sunbeam glowing softly inside it; the camera glides along them."),
            ("16_cow_grass", 17, 6.5, "Fast", F_DAY, False, None,
             "A brown cow grazing on bright green grass in a sunny meadow, chewing contentedly; the camera drifts past." + NOFLAME),
            ("17_wind_air", 18, 4.0, "Fast", F_DAY, False, None,
             "Wind ripples across a wheat field towards a wood; birds lift and wheel in the clear air." + NOFLAME),
            ("18_forest_sea", 20, 0, "Fast", F_DAY, False, "EVERY BREATH",
             "A green forest running down to a sunlit sea full of drifting green algae; tiny clear oxygen bubbles rise from the leaves and the water. Slow aerial drift." + NOFLAME),
            ("19_dots_crowd", 21, 0, "Fast", F_INK, False, "4 IN 10,000",
             "A flat cream field filled with a crowd of ten thousand tiny pale dots jostling gently; four of them turn a solid bright gold colour. Flat illustration, nothing glows."),
            ("20_explorer_willow", 21, 4.0, "Quality", Q_EXP, True, None,
             f"Under a great willow by a river in warm sun. {EXPLORER} He holds up an open hand in a sunbeam as if feeling invisible threads of air, watches a willow leaf turn towards the light, smiles and walks away along the bank." + NOFLAME),
            ("21_three_objects", 23, 0, R, None, False, None, ("P1:03_pot_jar_leaf", 2.3)),
            ("22_pulled_down", 24, 0, "Fast", F_DAY, False, None,
             "Low angle from the soil at the foot of a great willow: the camera rises up the trunk into the canopy, the leaves rippling against a bright sky." + NOFLAME),
            ("23_carbon_atom", 26, 0, "Quality", Q_GLOW, False, None,
             "Extreme close-up of a green willow leaf: one tiny carbon atom inside it glows softly gold; the camera zooms in and in until the atom fills the frame, a soft glowing ball."),
            ("24_gold_foil", 28, 0, R, None, False, None, ("004:part01/11_gold_foil_bounce", 0.0)),
        ],
    ),
}

EXTERNAL = {
    "004:part01/11_gold_foil_bounce": {
        "quality": "KEEP (live in 004)",
        "file": "02_Video-Projects/004_Whats-Really-Inside-An-Atom/04_Generated-Clips/part01/raw/v01/11_gold_foil_bounce_v01.mp4",
        "sha256": "5436abd10fa19bdd0f48f69d1c6d56a02ae25de30598d8ae739ef309c3e9f437",
        "duration_s": 8.0,
        "note": "The hand-off line to the atom film: 004's live gold-foil plate. Alternative if Claude wants new picture: one Quality plate (+1 Quality mint).",
    },
}


def fmt(t: float) -> str:
    return f"{int(t // 60)}:{t % 60:05.2f}"


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    parts = {p["part"]: p for p in RETIME["parts"]}
    nparts = len(parts)
    rows_by_key: dict[str, dict] = {}
    boards = {}
    for n, spec in P.items():
        part = parts[n]
        sents = part["sentences"]
        part_end = parts[n + 1]["card_in_film_s"] if n < nparts else part["vo_film_end_s"] + TAIL_S
        rows = []
        for pid, s, off, q, reason, exp, label, body in spec["plates"]:
            t = sents[s - 1]["film_s"] + off
            row = {"id": pid, "t_s": round(t, 2), "t": fmt(t), "explorer": exp, "side_label": label}
            if q == R:
                src, clip_in = body
                row.update({"quality": "reuse", "reuse_of": src, "clip_in_s": clip_in,
                            "engine_reason": "Reuse: a later window of a KEEP clip (callback), no new mint."})
            else:
                row.update({"quality": q, "engine_reason": reason,
                            "prompt": "Premium Animistry-class 3D cartoon. " + body
                            + " Silent. Continuous motion through the final frame." + ("" if exp else " No Explorer.")})
            rows.append(row)
        for i, r in enumerate(rows):
            end = rows[i + 1]["t_s"] if i + 1 < len(rows) else part_end
            r["use_s"] = round(end - r["t_s"], 2)
            assert MIN_PLATE_S <= r["use_s"] <= CLIP_USE_S, (n, r["id"], r["use_s"])
            lines = [x["text"] for x in sents if r["t_s"] - 0.05 <= x["film_s"] < end - 0.05]
            first = max((x for x in sents if x["film_s"] <= r["t_s"] + 0.05), key=lambda x: x["film_s"], default=None)
            if first is not None and (not lines or first["text"] != lines[0]):
                lines.insert(0, f"(continues) {first['text']}")
            r["vo_land"] = lines
            rows_by_key[f"P{n}:{r['id']}"] = r
        boards[n] = (spec, part, part_end, rows)

    # clip length: own window, and every reuse window cut from it
    need: dict[str, float] = {k: min(r["use_s"] + REUSE_PAD_S, 8.0) for k, r in rows_by_key.items() if r["quality"] != "reuse"}
    for k, r in rows_by_key.items():
        if r["quality"] == "reuse":
            src = r["reuse_of"]
            end = r["clip_in_s"] + r["use_s"]
            if src in EXTERNAL:
                assert end <= EXTERNAL[src]["duration_s"], (k, end)
                continue
            assert src in need, (k, src)
            assert end <= 8.0 - 0.1, (k, end)
            need[src] = max(need[src], min(end + REUSE_PAD_S, 8.0))
            r["reuse_window"] = f"{r['clip_in_s']:.2f}-{end:.2f} s of {src}"

    floor_gbp = CREDIT_LOG["readings"][-1]["free_trial_remaining_gbp"]
    cum = 0.0
    flow_credits = 0
    for k, r in rows_by_key.items():
        if r["quality"] == "reuse":
            r.update({"route": "reuse", "clip_s": 0, "cost_try1_gbp": 0.0, "cost_expected_gbp": 0.0})
            continue
        q = r["quality"]
        if k in FLOW_PLATES:
            assert q == "Fast" and need[k] <= 8, k
            flow_credits += FLOW_COST["Fast"] * FLOW_TAKES_PER_PLATE
            r.update({"route": "flow", "clip_s": 8, "flow_credits": FLOW_COST["Fast"] * FLOW_TAKES_PER_PLATE,
                      "cost_try1_gbp": 0.0, "cost_expected_gbp": 0.0,
                      "route_note": f"Flow Veo 3.1 Fast, {FLOW_TAKES_PER_PLATE} takes x {FLOW_COST['Fast']} credits; a third take moves to Vertex Fast"})
            continue
        clip = next(L for L in VERTEX_LENGTHS if L >= need[k] - 1e-6) if need[k] <= 8 + 1e-6 else None
        assert clip, (k, need[k])
        try1 = USD_PER_S[q] * clip * GBP_PER_USD
        stills = STILLS_PER_PLATE * USD_PER_STILL * GBP_PER_USD
        exp = try1 * TAKES_PER_KEEP[q] + stills
        cum += exp
        r.update({"route": "vertex", "clip_s": clip, "cost_try1_gbp": round(try1, 2),
                  "cost_expected_gbp": round(exp, 2), "cum_expected_gbp": round(cum, 2),
                  "beyond_floor": cum > floor_gbp})
    assert flow_credits <= FLOW_CREDITS_LEFT, flow_credits

    totals = {"rows": 0, "mints": 0, "Quality": 0, "Fast": 0, "reuse": 0, "flow": 0,
              "vertex_s": {"Quality": 0, "Fast": 0}, "try1_gbp": 0.0, "expected_gbp": 0.0}
    per_part = []
    for n, (spec, part, part_end, rows) in boards.items():
        nq = sum(r["quality"] == "Quality" for r in rows)
        nf = sum(r["quality"] == "Fast" for r in rows)
        nr = sum(r["quality"] == "reuse" for r in rows)
        board = {
            "film": "006_Trees-Are-Made-Of-Air",
            "working_title": "The Willow Tree That Was Made of Air",
            "part": f"{n:02d}",
            "title": spec["title"],
            "status": "BOARD_V01",
            "mint": False,
            "house": "STUDIO_PLAYBOOK.md §5 · re-timed from VO v02 (VO_RETIME_v02.json) · priced (Claude desk task 5951184558, 2 Oct 2026)",
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
            "explorer_plates": sum(r["explorer"] for r in rows),
            "forbidden": FORBIDDEN,
            "always_fails": ALWAYS_FAILS,
            "motion_lock": "Real Veo camera and object motion on every plate. No freeze-pad, no loop, no Ken Burns. A reuse row cuts a different window of a KEEP clip; never a still.",
            "quality_note": "Flow Veo 3.1 Fast on the Mini's CDP worker (benoats@googlemail.com) for the held establishing shots; Vertex AI Veo 3.1 (gen-lang-client-0538779324) for the rest: veo-3.1-generate-001 for Quality, veo-3.1-fast-generate-001 for Fast, 4/6/8 s clips. Quality only for a named person's face, the Explorer, or a flame/furnace/glow/sunbeam hero. A Fast take with a flame, lamp or glow in frame fails: reframe or remint on Quality. One plate at a time until the first KEEP; after 2 same-framing FAILs change the framing.",
            "labels": "White Didot italic side label, 1-4 words, one at a time, on the plate's first beat (or at the stated offset); added in the edit. Never two at once.",
            "counts": {"rows": len(rows), "mints": nq + nf, "Quality": nq, "Fast": nf, "reuse": nr},
            "plates": rows,
        }
        path = OUT / f"part-{n:02d}_plates_v01.json"
        path.write_text(json.dumps(board, indent=2, ensure_ascii=False) + "\n")
        t1 = sum(r["cost_try1_gbp"] for r in rows)
        ex = sum(r["cost_expected_gbp"] for r in rows)
        per_part.append({"part": n, "rows": len(rows), "Quality": nq, "Fast": nf, "reuse": nr,
                         "flow": sum(r["route"] == "flow" for r in rows),
                         "try1_gbp": round(t1, 2), "expected_gbp": round(ex, 2)})
        totals["rows"] += len(rows)
        totals["mints"] += nq + nf
        totals["Quality"] += nq
        totals["Fast"] += nf
        totals["reuse"] += nr
        totals["flow"] += sum(r["route"] == "flow" for r in rows)
        for r in rows:
            if r["route"] == "vertex":
                totals["vertex_s"][r["quality"]] += r["clip_s"]
        totals["try1_gbp"] += t1
        totals["expected_gbp"] += ex
        print(f"part {n:02d}: {len(rows)} rows = {nq} Quality + {nf} Fast + {nr} reuse; "
              f"try-1 £{t1:.2f}, expected £{ex:.2f} → {path.name}")

    beyond = [{"key": k, "quality": r["quality"], "clip_s": r["clip_s"], "expected_gbp": r["cost_expected_gbp"],
               "cum_expected_gbp": r["cum_expected_gbp"]}
              for k, r in rows_by_key.items() if r.get("beyond_floor")]
    lite_candidates = [k for k, r in rows_by_key.items()
                       if r["route"] == "vertex" and r["quality"] == "Fast"]
    lite_saving = sum(rows_by_key[k]["cost_expected_gbp"] for k in lite_candidates)
    stills_saving = sum(STILLS_PER_PLATE * USD_PER_STILL * GBP_PER_USD for r in rows_by_key.values() if r["route"] == "vertex")
    plan = {
        "film": "006_Trees-Are-Made-Of-Air",
        "written": "2026-10-02",
        "task": "Claude desk PR #180 comment 5951184558",
        "vertex_balance_before_boards": CREDIT_LOG["readings"][-1],
        "floor_gbp": 0.0,
        "flow": {"credits_left": FLOW_CREDITS_LEFT, "cost_per_clip": FLOW_COST, "plates": sorted(FLOW_PLATES),
                 "credits_planned": flow_credits},
        "rates": {"vertex_usd_per_s": USD_PER_S, "usd_per_still": USD_PER_STILL, "gbp_per_usd_planning": GBP_PER_USD,
                  "gbp_per_usd_005_actual": GBP_PER_USD_005_ACTUAL, "takes_per_keep_005": TAKES_PER_KEEP,
                  "stills_per_plate_005": STILLS_PER_PLATE},
        "totals": {**totals, "try1_gbp": round(totals["try1_gbp"], 2), "expected_gbp": round(totals["expected_gbp"], 2)},
        "per_part": per_part,
        "top_up_needed_gbp": round(max(0.0, totals["expected_gbp"] - floor_gbp), 2),
        "beyond_floor": beyond,
        "options_not_in_plan": {
            "flow_lite_lower_priority": {"credits": 0, "plates": len(lite_candidates),
                                         "would_save_gbp": round(lite_saving, 2),
                                         "note": "Flow shows 'Veo 3.1 - Lite [Lower Priority]' at 0 credits. Not in the playbook's model table; needs Claude/Ben's OK and a one-plate trial judged on continuous playback."},
            "flow_nano_banana_stills": {"credits": 0, "would_save_gbp": round(stills_saving, 2),
                                        "note": "Start frames from Flow's Nano Banana 2 (0 credits) instead of Vertex gemini-2.5-flash-image."},
        },
        "external_reuse": EXTERNAL,
    }
    PLAN.write_text(json.dumps(plan, indent=2, ensure_ascii=False) + "\n")
    print(f"film: {totals['rows']} rows = {totals['Quality']} Quality + {totals['Fast']} Fast + {totals['reuse']} reuse "
          f"({totals['flow']} Fast on Flow, {flow_credits} credits); Vertex seconds {totals['vertex_s']}")
    print(f"try-1 £{totals['try1_gbp']:.2f} · expected with 005 retakes + stills £{totals['expected_gbp']:.2f} · "
          f"Vertex £{floor_gbp:.2f} → top-up £{plan['top_up_needed_gbp']:.2f} · beyond floor: {len(beyond)} plates")
    print(f"options: Flow Lite LP on {len(lite_candidates)} Fast plates saves £{lite_saving:.2f}; Flow stills save £{stills_saving:.2f}")


if __name__ == "__main__":
    main()
