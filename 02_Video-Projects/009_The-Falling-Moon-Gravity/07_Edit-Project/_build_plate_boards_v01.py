#!/usr/bin/env python3
"""HOS 009: build and price parts/part-0N_plates_v01.json from the locked VO (no spend, mint nothing).

Backlog job J0261 (OWB queue, repo hos): plate board rows (prompt, reference, Flow quality, price)
from the locked VO, drafted from SHOT_LIST_v01.md (Claude, 6 Oct) and VO_RETIME_v01.json.

Plates follow narration order. Two shot-list beats move to where the words are said:
the old-Newton telling is before the orchard (Part 02 sentences 9 then 10), and
"still up there, night after night" closes Part 02. The Part 02 cart cutaway (shot-list
02-02, a named cut-first cutaway) is folded into the arrival. Fast prompts stay
non-emissive. The quart pot is Quality because the shot is candlelit (HOS Never:
no Veo Fast on fragile light).

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
REVIEW = EDIT / "PRICE_REVIEW_v01.md"

CLIP_USE_S = 7.9
MIN_PLATE_S = 2.4
TAIL_S = 0.6
REUSE_PAD_S = 0.5
VERTEX_LENGTHS = (4, 6, 8)

# Readings 15 Oct 2026 (orbit-with-ben ai_spend ledger). No spend logged after either reading.
FLOW_CREDITS_LEFT = 23730
FLOW_READ_AT = "2026-10-15T12:58:32Z"
VERTEX_BALANCE_GBP = 71.02
VERTEX_READ_AT = "2026-10-15T07:30:31Z"
VERTEX_MARGIN_GBP = 1.00  # that reading: jobs stop at a £1 margin
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
CURVE = " The Moon, ball or path slides sideways and down along a smooth curve. Nothing plummets straight at the Earth."
FAST_SAFE = " Daylight, window light or matte painted ink only. No candle, flame, glow, spark, comet or lightning."
NO_HORROR = " No sick people, no crosses on doors, no carts of bodies."
APPLE = "a green apple with a red flush"
HOUSE = "a two-storey limestone farmhouse with mullioned windows and a stone-slate roof, and no plaque on the door"
NEWTON_YOUNG = ("Isaac Newton at about twenty-three, no wig, his own shoulder-length dark hair, "
                "a plain dark coat and a simple white band collar")
NEWTON_OLD = "Isaac Newton as an old man with long white hair and a dark coat"
NEWTON_41 = "Isaac Newton at about forty-one, his own dark hair, no wig, a plain dark coat"
HALLEY = "Edmond Halley at about twenty-eight, long dark natural hair, no wig, and a travelling coat"
EXPLORER_REF = "01_Character/05_Generation-References/hos-explorer-reference-v01.jpg"

F_DAY = "Fast: daylight, window light or matte ink. Nothing emissive, so Veo Fast is allowed."
Q_LIGHT = "Quality: Moon, night sky, candle, fire, glow, water or space (never Fast on fragile light)."
Q_FACE = "Quality: a readable face."
Q_HERO = "Quality: Short frame 0 or the answer image."
Q_FORCE = "Quality: shot list said Fast, but the picture is candlelit (HOS Never: no Fast on fragile light)."
REUSE_REASON = "Reuse: a window of a KEEP clip (callback), no new mint."
CONT_REASON = "Continuation: same shot carried on by start-frame I2V from the last frame of the row before (span > one clip)."

# (id, sentence, word or None, quality, set, side_label, prompt body or None, explorer, reason)
ROWS = {
    1: [
        ("01_moon_falling", 1, None, "Quality", "A", "THE MOON IS FALLING",
         "A full Moon over a dark English field at night. A thin line traces its path as it drops a little and slides sideways, again and again, drawing its curve. Short A frame 0. The answer image." + CURVE,
         False, Q_HERO),
        ("02_apple_and_moon", 2, None, "Quality", "A", "THE SAME PULL?",
         f"In one frame, {APPLE} drops slowly from a branch and the Moon hangs in the night sky behind the same tree." + CURVE,
         False, Q_LIGHT),
        ("03_table_three", 4, None, "Fast", "C", "AN APPLE · A CANNON · A SUM",
         f"On a wooden table in grey window light, {APPLE}, a small brass cannon and a sheet of unreadable marks arrive one after another, set down by unseen hands. The marks are scribbles, not numbers.",
         False, F_DAY),
        ("04_things_fall", 6, None, "Fast", "C", None,
         "Quick everyday falls in daylight: a stone drops to the flagstones, then a cup tips off a wooden table. No faces.",
         False, F_DAY),
        ("05_heavens_map", 8, None, "Quality", "K", "TWO SETS OF RULES",
         "An old painted chart of the heavens: the Earth at the centre, crystal spheres turning, the Moon and planets fixed on gleaming rings.",
         False, Q_LIGHT),
        ("06_perfect_circles", 9, None, "Fast", "K", None,
         "Close on those painted rings, turning in perfect circles. Matte paint, no glow, no readable marks.",
         False, F_DAY),
        ("07_night_field", 11, None, "Quality", "A", "1665",
         f"A clear night in a dark Lincolnshire field: a young man seen mostly from behind, face kept in shadow, drops a pebble and looks up as the Moon rises. Not yet named." + CURVE,
         False, Q_LIGHT),
        ("08_cold_ground", 13, None, "Fast", "A", None,
         "Close on boots in frosty grass as a pebble lands with a soft thud. The Moon stays out of frame. No face.",
         False, F_DAY),
        ("09_stone_and_moon", 15, None, "Fast", "A", None,
         "A soft split made of two moving pictures side by side: the pebble falling onto grass, and the Moon sliding along its curve. Matte, no glow added, no words." + CURVE,
         False, F_DAY),
        ("10_farmhouse_dawn", 16, None, "Quality", "C", None,
         f"Dawn on {HOUSE}, with an apple orchard beside it. Slow push. Hard cut ready for the next chapter.",
         False, Q_LIGHT),
    ],
    2: [
        ("01_cambridge_closes", 1, None, "Quality", "B", "CAMBRIDGE CLOSES",
         "Cambridge in the summer of 1665: college gates swing shut and students carry trunks out to waiting carts. No notice on the gate." + NO_HORROR,
         False, Q_FACE),
        ("02_newton_arrives", 3, None, "Quality", "C", "ISAAC NEWTON · WOOLSTHORPE",
         f"A cart rolls along a country road, then {NEWTON_YOUNG} carries a stack of books through the low door of {HOUSE}.",
         False, Q_FACE),
        ("03_christmas_birth", 4, None, "Quality", "C", "25 DECEMBER 1642",
         f"The same farmhouse in winter, a single candle in one window. No baby shown.",
         False, Q_LIGHT),
        ("04_quart_pot", 6, None, "Quality", "C", None,
         "A small pewter quart pot on a wooden table in warm candlelight. No baby, no face. Gentle and quiet.",
         False, Q_FORCE),
        ("05_working_alone", 7, None, "Quality", "C", None,
         f"{NEWTON_YOUNG} alone at a table: a glass prism throws a rainbow on the stone wall, and pages of curves lie beside a candle.",
         False, Q_LIGHT),
        ("06_old_newton_tells", 9, None, "Quality", "room", None,
         f"Many years later: {NEWTON_OLD} sits by a fire and tells a friend, whose face stays soft and unrecognisable. The telling comes before the garden, as the voice says it.",
         False, Q_FACE),
        ("07_orchard_bench", 10, None, "Quality", "A", None,
         f"The Woolsthorpe orchard in late summer. {NEWTON_YOUNG} sits on a bench under an apple tree, thinking. No apple has fallen yet.",
         False, Q_FACE),
        ("08_the_apple", 11, None, "Quality", "A", "THE APPLE",
         f"{APPLE} falls from the tree and lands in the grass a few feet from the bench. It never touches his head.",
         False, Q_LIGHT),
        ("09_pull_heights", 15, None, "Fast", "E", None,
         "A soft painted-parchment card: a gentle ink line of pull at the top of a tree, then a tower, then a mountain. Matte ink, no glow, no words.",
         False, F_DAY),
        ("10_how_high", 17, None, "Quality", "A", "HOW HIGH DOES IT REACH?",
         f"{NEWTON_YOUNG} looks from the fallen apple up to the pale daytime Moon. A faint line of pull stretches up towards it." + CURVE,
         False, Q_LIGHT),
        ("11_explorer_apple", 18, None, "Quality", "A", None,
         f"The Explorer picks up the fallen apple, tosses it, catches it, holds it up beside the pale Moon and squints at the two. Never a Short frame 0." + CURVE,
         True, Q_FACE),
        ("12_still_up_there", 21, None, "Quality", "A", None,
         "The Moon high over the same orchard at night, still up there. Slow push." + CURVE,
         False, Q_LIGHT),
    ],
    3: [
        ("01_really_falling", 1, None, "Quality", "A", None,
         "The same Moon over the orchard. A curve draws under it: it is falling, and it never lands." + CURVE,
         False, Q_LIGHT),
        ("02_cannon_world", 5, None, "Quality", "D", "NEWTON'S CANNON",
         "A stylised small round Earth with a giant mountain poking above a thin band of air, and a brass cannon on top pointing sideways. Dark sky. The cannon and the mountain come into view together.",
         False, Q_LIGHT),
        ("03_shot_slow", 6, None, "Fast", "D", "SLOW",
         "The brass cannon fires gently. The ball curves down and lands near the foot of the mountain. Matte daylight on the model, no muzzle flash, no glow." + CURVE,
         False, F_DAY),
        ("04_shot_faster", 7, None, "Fast", "D", "FASTER",
         "A faster shot from the same cannon: the ball curves further and lands far around the small globe. No flash, no glow." + CURVE,
         False, F_DAY),
        ("05_shot_orbit", 8, None, "Quality", "D", "FALLING ALL THE WAY ROUND",
         "The fastest shot curves down as the round Earth curves away beneath it. The ball sweeps all the way round on a glowing trail and comes back past the mountain." + CURVE,
         False, Q_LIGHT),
        ("06_orbit_teach", 12, None, "Fast", "E", None,
         "A soft painted-parchment card: two small ink arrows on a ball, one sideways and one down, repeating around a circle. Matte ink, no glow, no words.",
         False, F_DAY),
        ("07_ball_to_moon", 14, None, "Quality", "D", "AN ORBIT",
         "The cannonball's circle fades into the Moon's much larger orbit around the Earth." + CURVE,
         False, Q_LIGHT),
        ("08_km_a_second", 15, None, "Fast", "E", None,
         "A painted-parchment card of the Moon on its curve: a short sideways ink arrow and a tiny downward ink tick, repeating. No glow, no numbers (the distance is an overlay)." + CURVE,
         False, F_DAY),
        ("09_can_he_calculate", 17, None, "Fast", "C", None,
         "At the table, the apple beside the paper and a pen poised. Seen from behind, no readable face, window light, no candle.",
         False, F_DAY),
    ],
    4: [
        ("01_weaker_far", 1, None, "Fast", "E", None,
         "A painted-parchment card: a pull arrow shrinks as a ball moves away from a painted Earth, at two distances and then three. Matte ink, no glow, no numbers.",
         False, F_DAY),
        ("02_spray_paint", 5, None, "Quality", "E", "TWICE AS FAR, A QUARTER AS STRONG",
         "A hand sprays paint at a wall from close up, a small dark spot, then from twice as far, a patch four times as big and paler. Teaching picture only. No words on the wall.",
         False, Q_FACE),
        ("03_sixty_earths", 9, None, "Fast", "E", "60 TIMES FURTHER",
         "A calm painted diagram: one Earth, then a line of many Earths laid end to end out towards a small Moon. Matte, no glow, no digits.",
         False, F_DAY),
        ("04_dots_square", 10, None, "Fast", "E", "3,600 TIMES WEAKER",
         "A square of many small ink dots fills the card, then a pull arrow beside the Moon shrinks to one tiny dot. No digits (the count is an overlay).",
         False, F_DAY),
        ("05_minute_second", 13, None, "Quality", "E", "1 MINUTE = 1 SECOND",
         f"Split picture: on the left {APPLE} falls for a moment beside a blank ruler; on the right the Moon falls along its curve. Both drop the same distance. No digits. Short B frame 0." + CURVE,
         False, Q_HERO),
        ("06_pretty_nearly", 16, None, "Fast", "C", None,
         "Newton's page in window light: two short columns of unreadable marks that end level with each other. No digits. A hand rests the page flat.",
         False, F_DAY),
        ("07_put_aside", 19, None, "Fast", "C", None,
         "The papers slide into a drawer. At the window the light changes from summer green to winter grey to spring. No face, no candle.",
         False, F_DAY),
        ("08_halley_visit", 20, None, "Quality", "F", "EDMOND HALLEY · 1684",
         f"A panelled room at Trinity, books piled on every surface. {HALLEY} sits across from {NEWTON_41}. Window light.",
         False, Q_FACE),
        ("09_ellipse_answer", 23, None, "Quality", "F", None,
         f"{NEWTON_41} draws an ellipse in the air with one finger. A soft glowing ellipse appears between him and Halley.",
         False, Q_LIGHT),
        ("10_write_it_down", 25, None, "Fast", "F", None,
         "A man writing late, seen from behind, stacks of pages growing on the desk. No readable face, window light only, nothing emissive.",
         False, F_DAY),
        ("11_principia_press", 27, None, "Quality", "G", "PRINCIPIA · 1687",
         "A 1680s London hand-press shop in lamplight: a thick book comes off a wooden press onto a stack of sheets. No readable title (the title is an overlay).",
         False, Q_LIGHT),
        ("12_fish_book", 28, None, "Fast", "G", None,
         "A lavish book of fish illustrations lies open on a shelf, pictures only, no readable title. Unseen hands count coins onto the counter in window light. No readable face.",
         False, F_DAY),
    ],
    5: [
        ("01_one_law", 1, None, "Quality", "E", "ONE LAW EVERYWHERE",
         "A painted solar system: the same faint lines of pull reach from the Sun to each planet and from Jupiter to its moons. Soft glow on the lines.",
         False, Q_LIGHT),
        ("02_tides_harbour", 3, None, "Quality", "I", "THE MOON PULLS BACK",
         "A stone harbour at night. The tide slowly rises up the wall as the Moon hangs overhead. Boats shift on calm water." + CURVE,
         False, Q_LIGHT),
        ("03_halley_comet_path", 4, None, "Fast", "E", None,
         "A painted-parchment card: a long ink ellipse around a painted Sun, and a small ink marker on the far side of the loop. Matte ink, no glow, no digits, no tail.",
         False, F_DAY),
        ("04_comet_1758", 7, None, "Quality", "H", "HALLEY'S COMET · 1758",
         "Christmas night beside a Saxon farmhouse: a farmer-astronomer at an eight-foot wooden reflecting telescope under a cold clear sky. A faint comet with a short soft tail drifts into the eyepiece and holds as a soft smudge among the stars. No snow. Short C frame 0.",
         False, Q_HERO),
        ("05_iss_orbit", 9, None, "Quality", "J", "FALLING, TOGETHER",
         "A generic space station, a simple silhouette with no flags, logos or letters, glides over a blue Earth." + CURVE,
         False, Q_LIGHT),
        ("06_iss_apple", 14, None, "Quality", "J", None,
         f"Inside a plain station cabin with handrails, two generic astronauts in plain suits and {APPLE} drift together. The apple turns slowly. No real likeness, no readable patches.",
         False, Q_LIGHT),
        ("07_station_curve", 17, None, "Fast", "E", None,
         "A painted-parchment card: the station's path drawn as the cannonball's circle, one ink arrow sideways and one down. Matte, no glow, no words." + CURVE,
         False, F_DAY),
        ("08_cup_and_planets", 18, None, "Quality", "C", None,
         "A cup tips off a wooden table, and the view pulls out to planets sliding on their curves around the Sun." + CURVE,
         False, Q_LIGHT),
        ("09_orchard_dusk", 22, None, "Quality", "A", "THE SAME PULL",
         f"The Woolsthorpe orchard at dusk. {APPLE} falls into the grass and the camera tilts up past the tree to the rising Moon." + CURVE,
         False, Q_LIGHT),
        ("10_explorer_bench", 23, None, "Quality", "A", None,
         "At dusk the Explorer sets the apple down on the bench, looks up at the Moon and gives it a small nod. Never a Short frame 0." + CURVE,
         True, Q_FACE),
        ("11_table_three_again", 25, None, ("reuse", "P1:03_table_three"), "C", None, None, False, REUSE_REASON),
        ("12_clay_handoff", 27, None, "Quality", "—", None,
         "A dark sky over a green prehistoric landscape. A bright point grows in the sky, then the picture cuts to a thin pale band of clay in a rock face. No impact, no fire, no creatures hurt. May later share a 010 plate.",
         False, Q_LIGHT),
    ],
}

SHOT_LIST_REF = "07_Edit-Project/SHOT_LIST_v01.md"


def fmt(t: float) -> str:
    return f"{int(t // 60)}:{t % 60:05.2f}"


def main() -> None:
    parts = {p["part"]: p for p in RETIME["parts"]}
    rows_by_key: dict[str, dict] = {}
    boards = {}
    short: list[tuple] = []
    for n, part in parts.items():
        part_end = parts[n + 1]["card_in_film_s"] if n < len(parts) else part["vo_film_end_s"] + TAIL_S
        anchored = []
        for pid, s, word, q, set_, label, body, explorer, reason in ROWS[n]:
            if word is not None:
                raise SystemExit("word anchors are unused on 009; retime words were not needed")
            sent = part["sentences"][s - 1]
            t = sent["film_s"]
            row = {"id": pid, "t_s": round(t, 2), "t": fmt(t), "set": set_, "explorer": explorer,
                   "side_label": label, "sentence": s}
            if isinstance(q, tuple):
                row.update({"quality": "reuse", "reuse_of": q[1], "engine_reason": reason,
                            "reference": q[1], "prompt": None})
            else:
                row.update({"quality": q, "engine_reason": reason,
                            "prompt": STYLE + body + (EXPLORER_TAIL if explorer else TAIL),
                            "reference": EXPLORER_REF if explorer else f"set {set_} continuity; no still reference"})
            if explorer:
                row["reference"] = EXPLORER_REF
            anchored.append(row)
        anchored.sort(key=lambda r: (r["t_s"], r["id"]))
        if anchored[0]["sentence"] != 1:
            raise SystemExit(f"part {n} does not open on sentence 1")
        rows = []
        for i, r in enumerate(anchored):
            end = anchored[i + 1]["t_s"] if i + 1 < len(anchored) else part_end
            span = round(end - r["t_s"], 2)
            if span < MIN_PLATE_S - 1e-6:
                short.append((n, r["id"], r["t"], span, r["sentence"]))
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
                           "side_label": None, "added": True, "sentence": r["sentence"]}
                    if r["quality"] == "reuse":
                        row.update({"quality": "reuse", "reuse_of": r["reuse_of"], "engine_reason": REUSE_REASON,
                                    "reference": r["reuse_of"], "prompt": None})
                    else:
                        body = r["prompt"][len(STYLE):]
                        for mark in (" Short A frame 0.", " Short B frame 0.", " Short C frame 0.", " The answer image."):
                            body = body.replace(mark, "")
                        row.update({"quality": r["quality"], "engine_reason": CONT_REASON,
                                    "i2v_from": f"P{n}:{prev['id']} last frame",
                                    "reference": f"P{n}:{prev['id']} last frame",
                                    "prompt": STYLE + f"Same shot continues from the last frame of {prev['id']}, camera keeps moving: " + body})
                        if r["explorer"]:
                            row["prompt"] = row["prompt"].replace(EXPLORER_TAIL, TAIL).replace("the Explorer", "the empty set")
                            row["explorer"] = False
                row["use_s"] = round(t1 - t0, 2)
                sents = part["sentences"]
                lines = [x["text"] for x in sents if t0 - 0.05 <= x["film_s"] < t1 - 0.05]
                first = max((x for x in sents if x["film_s"] <= t0 + 0.05), key=lambda x: x["film_s"], default=None)
                if first is not None and (not lines or first["text"] != lines[0]):
                    lines.insert(0, f"(continues) {first['text']}")
                row["vo_land"] = lines
                row["generation_authorized"] = False
                rows.append(row)
        for r in rows:
            rows_by_key[f"P{n}:{r['id']}"] = r
        boards[n] = (part, part_end, rows)
    if short:
        raise SystemExit("plates under %.1f s:\n" % MIN_PLATE_S + "\n".join(
            f"  part {n} {pid} sentence {s} at {t}: {u} s" for n, pid, t, u, s in short))

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

    titles = {
        1: "The Falling Moon",
        2: "An Apple in a Plague Year",
        3: "The Cannon on the Mountain",
        4: "The Moon Test",
        5: "Falling Around the World",
    }
    totals = {"rows": 0, "mints": 0, "Quality": 0, "Fast": 0, "reuse": 0, "added": 0, "explorer": 0,
              "flow_credits_try1": 0, "flow_credits_expected": 0, "vertex_try1_gbp": 0.0, "vertex_expected_gbp": 0.0}
    per_part = []
    OUT.mkdir(exist_ok=True)
    for n, (part, part_end, rows) in boards.items():
        nq = sum(r["quality"] == "Quality" for r in rows)
        nf = sum(r["quality"] == "Fast" for r in rows)
        nr = sum(r["quality"] == "reuse" for r in rows)
        na = sum(bool(r.get("added")) for r in rows)
        ne = sum(bool(r["explorer"]) for r in rows)
        assert ne <= 1, (n, ne)
        board = {
            "part": f"{n:02d}",
            "title": f"Part {n:02d} — {titles[n]}",
            "film": "009_The-Falling-Moon-Gravity",
            "working_title": "Why Doesn't the Moon Fall to Earth?",
            "mint": False,
            "status": "BOARD_V01_PARKED_FOR_CHIEF",
            "house": ("STUDIO_PLAYBOOK.md §5 · rows from 07_Edit-Project/SHOT_LIST_v01.md (Claude, 6 Oct 2026), "
                      "timed from the locked VO (VO_RETIME_v01.json) and priced by Cursor, 15 Oct 2026 "
                      "(_build_plate_boards_v01.py, J0261). Rows marked added carry a shot past one clip. "
                      "Chief's price pass before any mint. Nothing here is generation_authorized."),
            "vo_file": f"02_Voiceover/{part['file']}",
            "vo_sha256": part["sha256"],
            "vo_duration_s": part["duration_s"],
            "chapter_card": None if n == 1 else {
                "text": part["chapter_card"], "in_s": part["card_in_film_s"], "hold_s": 1.5,
                "treatment": "soft cross-fade after the part's end + 0.6 s breath; music continues",
            },
            "set_language": "Sets A-K as SHOT_LIST_v01.md §Sets. Say 'same Woolsthorpe orchard' for continuity. Never 'same DNA' in a prompt.",
            "explorer_lock": "At most one plate in this part. On model: round gold glasses, teal long coat, finished hair. Attach the Explorer reference. Never a Short frame 0.",
            "forbidden": "Orbit robot. Photoreal. Ken Burns. Readable words or numbers. The apple hitting Newton's head. Plague horror. A straight drop onto the Earth. Agency logos or real astronaut likenesses. Snow on the 1758 comet. A gate notice at Cambridge.",
            "motion_lock": "Real camera and object motion on every plate. No freeze-pad, no loop.",
            "rules": [
                "The apple lands in the grass a few feet away. It never hits Newton's head.",
                "The Moon and every cannonball move sideways and down on a curve. Nothing plummets straight at the Earth.",
                "Plague is gates, carts and trunks. No sick people, no crosses, no carts of bodies.",
                "No readable text in any plate. Every LABEL, date and number is an overlay in the edit.",
                "Newton at 23 and at 41 wears his own hair, no wig. Halley has long dark natural hair, no wig. The old Newton has white hair.",
                "The station is generic: no flags, logos or real likenesses. The comet is a faint smudge, no snow.",
                "Fast plates are non-emissive. Candle, prism, fire, Moon-night, comet, water and space stay on Quality.",
                "WHO and WHEN cards (Newton, Halley, 1642, 1665, 1684, 1687, 1758) are edit overlays. The VO is already locked.",
            ],
            "vo_film_start_s": part["vo_film_start_s"],
            "part_end_film_s": round(part_end, 2),
            "clip_use_s": CLIP_USE_S,
            "xfade_s": 0.35,
            "explorer_plates": ne,
            "counts": {"rows": len(rows), "mints": nq + nf, "Quality": nq, "Fast": nf, "reuse": nr, "added": na},
            "plates": rows,
        }
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
        "film": "009_The-Falling-Moon-Gravity",
        "written": "2026-10-15",
        "task": "J0261 (OWB queue, repo hos): plate boards from the locked VO; mint nothing; parked for Chief's price pass",
        "shot_list": SHOT_LIST_REF,
        "vo": "02_Voiceover/VO_TAKES_KEEP.json status LOCKED v01 (Chief KEEP, desk #180 comment 6101629662, 11 Oct)",
        "readings": {
            "flow_credits_left": FLOW_CREDITS_LEFT,
            "flow_read_at": FLOW_READ_AT,
            "flow_note": "ai_spend record by cursor, J0279 Germs thumb still. No Flow spend logged after this reading.",
            "vertex_promo_gbp": VERTEX_BALANCE_GBP,
            "vertex_read_at": VERTEX_READ_AT,
            "vertex_margin_gbp": VERTEX_MARGIN_GBP,
            "vertex_usable_gbp": usable_vx,
            "vertex_note": "Google Developer Program monthly credit, all Available. Free Trial is £0. Jobs stop at a £1 margin on this reading. No Vertex spend logged after it.",
        },
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
        "departures_from_shot_list": [
            "Part 02 cart_road (shot-list 02-02, a named cut-first cutaway) is inside 02_newton_arrives: the sentence is one journey, not two plates.",
            "06_old_newton_tells sits before the orchard, because the locked VO tells the story that way.",
            "12_still_up_there closes Part 02, where 'still up there, night after night' is said. Part 03 opens on 01_really_falling.",
            "04_quart_pot is Quality. The shot list said Fast, and the picture is candlelit.",
            "Fast prompts are non-emissive, including the cannon shots (no muzzle flash) and the parchment cards (matte ink).",
            "The eyepiece beat (shot-list 05_right_on_time) stays inside 04_comet_1758. 'It has carried his name ever since' is 1.56 s, under a plate.",
            "02_apple_and_moon opens on 'So why doesn't it ever hit us?' so the apple line (2.31 s) is not its own plate.",
            "10_explorer_bench is its own plate on 'it is falling towards you', after the dusk orchard and before the table reuse.",
        ],
        "price_pass_questions": [
            "All-Flow expected credits against the 15 Oct reading, and whether Quality stays on Flow.",
            "Which added continuation rows become reuses of a KEEP clip instead of a second mint. Do not loop or freeze.",
            "Which non-hero Quality rows can move to Fast: farmhouse dawn, the cannon-world reveal, the spray-paint wall, the one-law diagram, the cup-to-planets pull-out, the clay hand-off. Faces, candles, the Moon at night, the comet, water, space, the glowing orbit trail and the three Short frame-0 plates stay Quality.",
            "Whether the parchment teach rows (pull heights, orbit arrows, weaker-with-distance, sixty Earths, the dot square, the station curve) become £0 code graphics instead of Fast mints, as on 008 v03.",
            "Vertex does not fit the whole film on the usable promo balance. Flow-first is the split this reading supports, if the price pass agrees.",
        ],
    }
    PLAN.write_text(json.dumps(plan, indent=2, ensure_ascii=False) + "\n")
    lines = [
        "# 009 price review v01",
        "",
        "Cursor, 15 Oct 2026, J0261. Boards and prompts only. **No mint. No spend.** Parked for Chief's price pass.",
        "",
        f"Locked VO: Chief KEEP, desk #180 comment 6101629662. Retime match "
        + ", ".join(f"part {p['part']} {p['match_rate_pct']}%" for p in RETIME["parts"])
        + f". Film {RETIME['vo_film_total']}.",
        "",
        "## Readings",
        "",
        f"- Flow: **{FLOW_CREDITS_LEFT}** credits at {FLOW_READ_AT}. No spend logged after that.",
        f"- Vertex promo: **£{VERTEX_BALANCE_GBP:.2f}** at {VERTEX_READ_AT}. Usable **£{usable_vx:.2f}** after the £1 margin on that reading. No spend logged after it. Free Trial is £0.",
        "",
        "## Totals",
        "",
        f"| | rows | Quality | Fast | reuse | added | Flow try-1 | Flow expected | Vertex try-1 | Vertex expected |",
        f"|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for pp in per_part:
        lines.append(
            f"| Part {pp['part']:02d} | {pp['rows']} | {pp['Quality']} | {pp['Fast']} | {pp['reuse']} | {pp['added']} | "
            f"{pp['flow_credits_try1']} | {pp['flow_credits_expected']} | £{pp['vertex_try1_gbp']:.2f} | £{pp['vertex_expected_gbp']:.2f} |"
        )
    lines.append(
        f"| **Film** | **{totals['rows']}** | **{totals['Quality']}** | **{totals['Fast']}** | **{totals['reuse']}** | **{totals['added']}** | "
        f"**{totals['flow_credits_try1']}** | **{totals['flow_credits_expected']}** | **£{totals['vertex_try1_gbp']:.2f}** | **£{totals['vertex_expected_gbp']:.2f}** |"
    )
    lines += [
        "",
        f"All on Flow: {'FITS' if plan['fits_now']['flow'] else 'DOES NOT FIT'} ({totals['flow_credits_expected']} expected vs {FLOW_CREDITS_LEFT} left).",
        f"All on Vertex: {'FITS' if plan['fits_now']['vertex'] else 'DOES NOT FIT'} (£{totals['vertex_expected_gbp']:.2f} expected vs £{usable_vx:.2f} usable).",
        "",
        "Rates are 006/008's: Flow Fast 10 / Quality 100 a take; expected uses 005's takes-per-KEEP (Quality 2.59, Fast 1.96) plus stills. Vertex is list price, 1080p, £0.80 per dollar, clip length 4/6/8 s.",
        "",
        "## What changed against the shot list",
        "",
    ]
    for item in plan["departures_from_shot_list"]:
        lines.append(f"- {item}")
    lines += ["", "## For the price pass", ""]
    for item in plan["price_pass_questions"]:
        lines.append(f"- {item}")
    lines.append("")
    REVIEW.write_text("\n".join(lines))
    print(f"film: {totals['rows']} rows ({totals['added']} added) = {totals['Quality']} Quality + {totals['Fast']} Fast + "
          f"{totals['reuse']} reuse, {totals['explorer']} Explorer")
    print(f"all on Flow: {totals['flow_credits_try1']} cr try-1 · {totals['flow_credits_expected']} cr expected (have {FLOW_CREDITS_LEFT}) "
          f"{'FIT' if plan['fits_now']['flow'] else 'OVER'}")
    print(f"all on Vertex: £{totals['vertex_try1_gbp']:.2f} try-1 · £{totals['vertex_expected_gbp']:.2f} expected (usable £{usable_vx:.2f}) "
          f"{'FIT' if plan['fits_now']['vertex'] else 'OVER'}")


if __name__ == "__main__":
    main()
