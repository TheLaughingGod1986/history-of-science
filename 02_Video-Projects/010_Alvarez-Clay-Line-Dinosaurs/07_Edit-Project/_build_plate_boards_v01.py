#!/usr/bin/env python3
"""HOS 010: plate boards v01 from the locked VO. Flow-first prices. No mint, no spend.

J0314. Same price table as 009 J0261 after the Flow-first pass: teach diagrams are
£0 code graphics, Fast continuations that cannot take a distinct window are edit-holds,
faces / fragile light / Short frame-0 plates stay Quality.

Reads Scribe word times from HOS_STT_DIR (the takes' stt_raw.json). Writes boards here.
"""
from __future__ import annotations

import json
import math
import os
import re
from pathlib import Path

PROJ = Path(__file__).resolve().parents[1]
EDIT = PROJ / "07_Edit-Project"
OUT = EDIT / "parts"
STT = Path(os.environ.get(
    "HOS_STT_DIR",
    PROJ / "02_Voiceover/stt",
))
KEEP = json.loads((PROJ / "02_Voiceover/VO_TAKES_KEEP.json").read_text())

CLIP_USE_S = 7.9
MIN_PLATE_S = 2.4
TAIL_S = 0.6
CARD_BREATH_S = 0.6
CARD_TO_VO_S = 1.9
VERTEX_LENGTHS = (4, 6, 8)

FLOW_CREDITS_LEFT = 23740
FLOW_READ_AT = "2026-10-15T21:42:22Z"
VERTEX_BALANCE_GBP = 71.02
VERTEX_READ_AT = "2026-10-15T07:30:31Z"
VERTEX_MARGIN_GBP = 1.00
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
FAST_SAFE = " Daylight, window light or matte painted ink only. No candle, flame, glow, spark, fireball or lightning."
NO_IMPACT = " No impact, no fireball, no burning animals, no dying dinosaurs."
EXPLORER_REF = "01_Character/05_Generation-References/hos-explorer-reference-v01.jpg"

Q_FACE = "Quality: a readable face."
Q_LIGHT = "Quality: fragile light, water, glow, space dust or sunlit rock (never Fast)."
Q_HERO = "Quality: Short frame 0 or the answer image."
Q_ANIMAL = "Quality: an animal the line is about."
F_DAY = "Fast: daylight or matte ink. Nothing emissive, so Veo Fast is allowed."
CODE_REASON = "Flow-first, as the 009 J0261 price pass: a teach diagram is a £0 code graphic. No Flow mint."
REUSE_REASON = "Reuse: a window of a KEEP clip (callback), no new mint."
CONT_REASON = "Continuation: same shot carried past one clip."

STEMS = {
    1: "hos_010_part01_the_line_in_the_rock_v01",
    2: "hos_010_part02_the_gorge_at_gubbio_v01",
    3: "hos_010_part03_a_clock_made_of_stardust_v01",
    4: "hos_010_part04_too_much_iridium_v01",
    5: "hos_010_part05_the_crater_and_the_birds_v01",
}
TITLES = {
    1: "The Line in the Rock",
    2: "The Gorge at Gubbio",
    3: "A Clock Made of Stardust",
    4: "Too Much Iridium",
    5: "The Crater and the Birds",
}

# id, find-phrase, quality, set, side_label, body, explorer, reason
# quality "code" or ("reuse", source_id)
ROWS = {
    1: [
        ("01_clay_line", "What killed the dinosaurs", "Quality", "A", "THE CLAY LINE",
         "A sunlit limestone cliff in a narrow Italian gorge. The camera pushes in on a thin dark clay band between pale layers. A fingertip comes to rest on the band. Short A frame 0. The answer image.",
         False, Q_HERO),
        ("02_vial_turns", "So what happened", "Quality", "B", "ONE SMALL SAMPLE",
         "A small glass vial of grey clay turns slowly under a warm lamp on a wooden lab bench. No readable label.",
         False, Q_LIGHT),
        ("03_bench_three", "By the end of this film", "Fast", "B", "HAMMER, VIAL, PAPER",
         "On a wooden workbench in grey window light, a geologist's hammer, a vial of grey clay and a printed page arrive one after another. The page is a blur of marks, not words.",
         False, F_DAY),
        ("04_long_reign", "For more than", "Quality", "G", None,
         "A sunlit Cretaceous plain. Long-necked dinosaurs graze far off, calm. None are in distress." + NO_IMPACT,
         False, Q_ANIMAL),
        ("05_empty_plain", "In the seas", "Fast", "G", None,
         "The same plain, now empty and quiet. Only ferns move in the wind. No bones, no death, no animals.",
         False, F_DAY),
        ("06_museum_question", "For a long time", "Quality", "C", "WHAT HAPPENED?",
         "A painted museum hall, high windows, dust in the light. A great dinosaur skeleton stands in the hall. Soft question-mark shapes drift like dust and never become readable letters.",
         False, Q_LIGHT),
        ("07_many_ideas", "dozens of ideas", "Fast", "E", None,
         "Small matte vignettes drift past: a volcano seen from far away with no eruption, a plain thermometer, a tiny mammal beside an unbroken egg. No text, no distress.",
         False, F_DAY),
        ("08_hand_on_rock", "Picture yourself", "Quality", "A", None,
         "Close on a hand laid flat across the clay line in the sunlit gorge. The light shifts. No face.",
         False, Q_LIGHT),
        ("09_gubbio_road", "young American geologist", "Fast", "A", None,
         "A small nineteen-seventies rented car winds along a mountain road into a narrow limestone gorge. No readable plate. Daylight.",
         False, F_DAY),
    ],
    2: [
        ("01_walter_hammer", "Walter Alvarez was studying", "Quality", "A", "WALTER ALVAREZ",
         "Gubbio in the nineteen-seventies. Walter Alvarez, clean-shaven, fair hair, dark-rimmed glasses, a short-sleeved field shirt, taps the sunlit cliff with a geologist's hammer.",
         False, Q_FACE),
        ("02_layers_build", "The cliffs there", "code", "E", None,
         "Own code graphic: pale layers of an ancient sea floor settle one on another. Matte ink on a lifted navy field. No words.",
         False, CODE_REASON),
        ("03_tiny_shells", "When he looked through", "Quality", "A", "TINY SHELLS",
         "A hand lens over the pale limestone below the clay. The rock is crowded with tiny round fossil shells, each the size of a grain of sand.",
         False, Q_LIGHT),
        ("04_floating_sea", "They came from little", "Quality", "E", None,
         "The same tiny shelled creatures drift in a sunlit ancient sea. Calm water, no distress.",
         False, Q_LIGHT),
        ("05_almost_none", "But just above", "Quality", "A", "ALMOST NONE",
         "The hand lens moves above the clay line. The rock is almost empty, only a few very small shells.",
         False, Q_LIGHT),
        ("06_explorer_lens", "Only a few very small", "Quality", "A", None,
         "In the gorge the Explorer peers through a hand lens at the rock below the clay, raises his eyebrows at the tiny shells, moves the lens above the line, finds almost nothing, and looks back, puzzled. Never a Short frame 0.",
         True, Q_FACE),
        ("07_same_level", "Because they vanished", "Quality", "A", None,
         "A slow pull back from the lens to the whole cliff. The thin clay line runs level across the sunlit face.",
         False, Q_LIGHT),
        ("08_two_clocks", "A few years would", "code", "E", None,
         "Own code graphic: two hourglasses side by side, one emptying quickly, one barely dripping. Matte ink, no digits.",
         False, CODE_REASON),
        ("09_wrap_sample", "He took a piece", "Quality", "A", "TAKEN HOME",
         "Walter wraps a small piece of the rock, clay band and all, in cloth and puts it in his field bag.",
         False, Q_FACE),
    ],
    3: [
        ("01_luis_sample", "Walter's father was Luis", "Quality", "D", "LUIS ALVAREZ",
         "A desk at Berkeley, late nineteen-seventies. Luis Alvarez, late sixties, white thinning hair, glasses, a cardigan, turns the rock sample over in his hands. His son stands beside him. Window light.",
         False, Q_FACE),
        ("02_pyramid_muons", "hidden rooms inside", "code", "E", None,
         "Own code graphic: a cutaway of a pyramid. Faint particle tracks pass through the stone. No hidden chamber is revealed. No words.",
         False, CODE_REASON),
        ("03_space_dust", "gentle rain of dust", "Quality", "E", "RAIN FROM SPACE",
         "A soft steady rain of glittering space dust falls on the Earth from every direction. Short B frame 0.",
         False, Q_HERO),
        ("04_dust_sea_floor", "settling on land", "Quality", "E", None,
         "The same fine glitter settles, year after year, on a dark sea floor. Calm water.",
         False, Q_LIGHT),
        ("05_iridium_sinks", "young and molten", "Quality", "E", "SANK TO THE CORE",
         "A cutaway of a young Earth. Molten iron sinks to the centre and carries silvery iridium with it. The crust is left almost bare. No readable labels.",
         False, Q_LIGHT),
        ("06_meteorite_rich", "But in meteorites", "Quality", "B", None,
         "A meteorite rests on dark cloth. Soft silver glints in it. No words.",
         False, Q_LIGHT),
        ("07_clock_idea", "So here was the clock", "code", "E", None,
         "Own code graphic: two clay bands. One is thick with glitter, for a slow layer. One is almost bare, for a fast layer. Matte ink, no digits.",
         False, CODE_REASON),
        ("08_asaro_michel", "Frank Asaro", "Quality", "D", "ASARO AND MICHEL",
         "A late-nineteen-seventies Berkeley lab. Frank Asaro and Helen Michel, kind likenesses in lab coats, press powdered samples into small pills and set them by a detector rack. Tape reels turn. No reactor. No readable screens.",
         False, Q_FACE),
        ("09_waiting_result", "What came back", "Fast", "D", None,
         "A paper printout starts to feed from a machine in window light. The team leans in, faces turned away. No readable numbers.",
         False, F_DAY),
    ],
    4: [
        ("01_iridium_spike", "In the Gubbio clay", "code", "B", "THE IRIDIUM SPIKE",
         "Own code graphic: a hand-drawn line stays low through the rock layers, then jumps in one sharp spike at the clay. No digits (the thirty-times note is an overlay).",
         False, CODE_REASON),
        ("02_stevns_cliff", "white sea cliff", "Quality", "Denmark", "DENMARK",
         "A white chalk sea cliff in daylight, with one thin dark band through it. No text.",
         False, Q_LIGHT),
        ("03_world_pins", "all around the world", "code", "F", "ALL AROUND THE WORLD",
         "Own code graphic: a painted world map. A pin drops on Italy, then a white cliff, then New Zealand. Matte pins, no glow, no place names.",
         False, CODE_REASON),
        ("04_supernova_test", "exploding star nearby", "code", "E", None,
         "Own code graphic: a far star flares, a dotted line runs to a test tube, then a plain cross fades in. Matte ink. The supernova idea fails. No words.",
         False, CODE_REASON),
        ("05_ten_km", "A giant asteroid", "code", "E", None,
         "Own code graphic: a rock beside a city skyline, for scale only. The rock hangs far out in space and does not move toward the Earth. No impact. No digits.",
         False, CODE_REASON),
        ("06_dust_veil", "throw dust high", "Quality", "G", "DUST AROUND THE WORLD",
         "A quiet Cretaceous forest of ferns and conifers. A dark grey veil spreads high across the sky and the sunlight fades. No fire, no impact, no animals.",
         False, Q_LIGHT),
        ("07_food_chain", "Plants would stop", "code", "E", None,
         "Own code graphic: a fern fades, then a plant-eater icon, then a meat-eater icon. Icons only, gently dimming. No animals in distress, no words.",
         False, CODE_REASON),
        ("08_science_paper", "In June", "Fast", "D", "SCIENCE, 1980",
         "A journal lies open on a desk in window light. The pages are a blur, not a readable title. No lamp.",
         False, F_DAY),
        ("09_doubters", "It was bold", "Quality", "D", None,
         "A crowded seminar room. Arms folded, heads shaking. Readable faces, kind, not caricatured. Window light.",
         False, Q_FACE),
        ("10_where_hole", "because if an asteroid", "code", "F", None,
         "Own code graphic: the same painted world map, with a large question mark over the oceans. No place names.",
         False, CODE_REASON),
    ],
    5: [
        ("01_shocked_quartz", "tiny grains of quartz", "Quality", "H", "SHOCKED QUARTZ",
         "A round microscope field: one grain of quartz criss-crossed with fine straight cracks. No text.",
         False, Q_LIGHT),
        ("02_glass_beads", "tiny beads of glass", "Quality", "H", "GLASS BEADS",
         "Tiny glassy beads sit beside a coin for scale. Soft light, no place name.",
         False, Q_LIGHT),
        ("03_caribbean_hunt", "towards the Caribbean", "code", "F", None,
         "Own code graphic: the map narrows on the Caribbean. A soft search circle. No place names.",
         False, CODE_REASON),
        ("04_chicxulub_ring", "enormous crater", "Quality", "E", "CHICXULUB CRATER",
         "Our own stylised gravity map, not a published one. A huge buried ring in glowing colour straddles a coastline. No place names, no numbers.",
         False, Q_LIGHT),
        ("05_ring_scale", "It's called Chicxulub", "code", "E", "ABOUT 180 KM WIDE",
         "Own code graphic: the same ring laid over an outline of southern England, for size. No digits on the art (the width is an overlay).",
         False, CODE_REASON),
        ("06_same_moment", "the same moment", "Quality", "A", "THE SAME MOMENT",
         "The Gubbio clay line again, close up, matching the Part 01 cliff. A gentle glow shows the iridium in the band. A new plate, not a replay of the opening clip.",
         False, Q_LIGHT),
        ("07_deccan_note", "volcanoes in India", "Fast", "E", None,
         "A distant line of old lava flows under a hazy sky. No eruption, no fire, no animals. Daylight.",
         False, F_DAY),
        ("08_all_at_once", "everything changes at once", "Quality", "A", None,
         "The cliff's layers, slow and even, then one sudden dark line. Sunlit rock.",
         False, Q_LIGHT),
        ("09_robin", "the pigeon on the pavement", "Quality", "I", "STILL HERE",
         "A morning garden. A pigeon struts, then a robin hops along a fence and turns its head. A faint outline of a small feathered dinosaur fades in over the robin, then out. The robin is Short C frame 0. No distress.",
         False, Q_HERO),
        ("10_explorer_robin", "Every bird you have", "Quality", "I", None,
         "The Explorer crouches in the garden and holds out a few crumbs. A robin hops closer. He looks from the bird to the sky and smiles. Never a Short frame 0.",
         True, Q_FACE),
        ("11_why_survive", "Why did they survive", "code", "E", None,
         "Own code graphic: three icons build in turn, a small bird, a seed, a ground nest. The reason is still open. No dinosaurs in distress, no words.",
         False, CODE_REASON),
        ("12_clay_callback", "So next time", "Quality", "A", None,
         "The sunlit Gubbio clay line again, the thin dark band between pale layers. A new plate, not a replay of the opening clip.",
         False, Q_LIGHT),
        ("13_window_song", "one of them is singing", "Quality", "I", None,
         "A bird sings on a branch outside a window. Soft morning light.",
         False, Q_ANIMAL),
        ("14_bench_three_again", "A hammer, a vial", ("reuse", "P1:03_bench_three"), "B", None,
         None, False, REUSE_REASON),
    ],
}


def tokens(text: str) -> list[str]:
    text = text.lower().replace("’", "'").replace("'", "")
    text = re.sub(r"[^a-z0-9 ]+", " ", text)
    return [t for t in text.split() if t]


def word_tokens(text: str) -> list[str]:
    raw = tokens(text)
    # Scribe writes 160, 66, 30, 10, 180, 1980, 1970s, 1990s. Script writes the words.
    # Matching uses the find-phrase, which is chosen to avoid the number.
    return raw


def fmt(t: float) -> str:
    return f"{int(t // 60)}:{t % 60:05.2f}"


def load_words(n: int) -> list[dict]:
    path = STT / STEMS[n] / "stt_raw.json"
    data = json.loads(path.read_text())
    out = []
    for w in data["words"]:
        if w.get("type") != "word":
            continue
        tok = word_tokens(w["text"])
        if not tok:
            continue
        out.append({"text": w["text"], "tok": tok[0], "start": float(w["start"]), "end": float(w["end"])})
    return out


def locate(words: list[dict], phrase: str, start_i: int) -> int:
    want = tokens(phrase)
    for n in (min(4, len(want)), min(3, len(want)), min(2, len(want))):
        if n < 2:
            continue
        w = want[:n]
        for i in range(start_i, len(words) - n + 1):
            if [words[i + k]["tok"] for k in range(n)] == w:
                return i
    raise SystemExit(f"phrase not found after word {start_i}: {phrase!r}")


def price_mint(q: str, need_s: float) -> dict:
    clip = next(L for L in VERTEX_LENGTHS if L >= need_s - 1e-6)
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


def zero_route(route: str) -> dict:
    return {
        "route": route, "flow_model": None, "flow_clip_s": 0,
        "flow_credits_try1": 0, "flow_credits_expected": 0,
        "vertex_model": None, "vertex_clip_s": 0,
        "vertex_try1_gbp": 0.0, "vertex_expected_gbp": 0.0,
    }


def code_spec(part: int, pid: str, body: str) -> dict:
    return {
        "file": f"code_graphic_010_p{part}_{pid}.mp4",
        "renderer": "python-pillow-ffmpeg (house explainer renderer, £0)",
        "style": "HOS cream-on-navy explainer, matte, one idea, labels of 4 words or fewer as overlays",
        "shows": body,
    }


def main() -> None:
    parts_meta = []
    film_cursor = 0.0
    anchored_by_part = {}
    for n in range(1, 6):
        words = load_words(n)
        dur = round(KEEP["locked"][f"{n:02d}"]["duration_s"], 2)
        if n == 1:
            card_in = None
            vo_start = 0.0
        else:
            card_in = round(film_cursor + CARD_BREATH_S, 2)
            vo_start = round(card_in + CARD_TO_VO_S, 2)
        vo_end = round(vo_start + dur, 2)
        cursor = 0
        anchored = []
        for pid, phrase, q, set_, label, body, explorer, reason in ROWS[n]:
            i = locate(words, phrase, cursor)
            cursor = i + 1
            local = words[i]["start"]
            film_t = round(vo_start + local, 2)
            row = {
                "id": pid, "t_s": film_t, "t": fmt(film_t), "set": set_, "explorer": explorer,
                "side_label": label, "find": phrase, "local_s": round(local, 2),
            }
            if isinstance(q, tuple):
                row.update({"quality": "reuse", "reuse_of": q[1], "engine_reason": reason,
                            "reference": q[1], "prompt": None})
            elif q == "code":
                row.update({"quality": "code_graphic", "engine_reason": reason,
                            "prompt": body, "reference": "own code graphic; no still",
                            "code_graphic_spec": code_spec(n, pid, body)})
            else:
                row.update({"quality": q, "engine_reason": reason,
                            "prompt": STYLE + body + FAST_SAFE + (EXPLORER_TAIL if explorer else TAIL)
                            if q == "Fast" else STYLE + body + (EXPLORER_TAIL if explorer else TAIL),
                            "reference": EXPLORER_REF if explorer else f"set {set_} continuity; no still reference"})
            if explorer:
                row["reference"] = EXPLORER_REF
            anchored.append(row)
        anchored.sort(key=lambda r: (r["t_s"], r["id"]))
        part_end = vo_end + (TAIL_S if n == 5 else 0.0)
        # Next part's card is the end of this part's picture, except the last.
        parts_meta.append({
            "part": n, "file": KEEP["locked"][f"{n:02d}"]["file"],
            "sha256": KEEP["locked"][f"{n:02d}"]["sha256"], "duration_s": dur,
            "card_in_film_s": card_in, "vo_film_start_s": vo_start, "vo_film_end_s": vo_end,
            "chapter": TITLES[n],
        })
        anchored_by_part[n] = (anchored, part_end if n == 5 else None)
        film_cursor = vo_end

    # Part end is the next card, so a plate does not run under the next chapter card.
    for n in range(1, 5):
        anchored, _ = anchored_by_part[n]
        anchored_by_part[n] = (anchored, parts_meta[n]["card_in_film_s"])

    short = []
    rows_by_key = {}
    boards = {}
    for n in range(1, 6):
        anchored, part_end = anchored_by_part[n]
        rows = []
        for i, r in enumerate(anchored):
            end = anchored[i + 1]["t_s"] if i + 1 < len(anchored) else part_end
            span = round(end - r["t_s"], 2)
            if span < MIN_PLATE_S - 1e-6:
                short.append((n, r["id"], r["t"], span, r["find"]))
            q = r["quality"]
            pieces = 1 if q in ("code_graphic", "reuse") else max(1, math.ceil(span / CLIP_USE_S - 1e-9))
            step = span / pieces
            for k in range(pieces):
                t0 = round(r["t_s"] + k * step, 2)
                t1 = round(r["t_s"] + (k + 1) * step, 2) if k + 1 < pieces else end
                if k == 0:
                    row = dict(r)
                else:
                    prev = rows[-1]
                    row = {
                        "id": f"{r['id']}_c{k}", "t_s": t0, "t": fmt(t0), "set": r["set"],
                        "explorer": False, "side_label": None, "added": True, "find": r["find"],
                        "quality": r["quality"], "engine_reason": CONT_REASON,
                        "i2v_from": f"P{n}:{prev['id']} last frame",
                        "reference": f"P{n}:{prev['id']} last frame",
                    }
                    if r["quality"] == "Fast":
                        body = r["prompt"][len(STYLE):]
                        row["prompt"] = STYLE + f"Same shot continues from the last frame of {prev['id']}, camera keeps moving: " + body
                        row["v01_parent_quality"] = "Fast"
                    elif r["quality"] == "Quality":
                        body = r["prompt"][len(STYLE):]
                        for mark in (" Short A frame 0.", " Short B frame 0.", " Short C frame 0.", " The answer image."):
                            body = body.replace(mark, "")
                        row["prompt"] = STYLE + f"Same shot continues from the last frame of {prev['id']}, camera keeps moving: " + body
                        row["v01_parent_quality"] = "Quality"
                    else:
                        row["prompt"] = None
                row["use_s"] = round(t1 - t0, 2)
                row["generation_authorized"] = False
                # The line being said: words whose start falls in [t0, t1) on the film clock.
                vo0 = parts_meta[n - 1]["vo_film_start_s"]
                words = load_words(n)
                said = [w["text"] for w in words if t0 - vo0 - 0.05 <= w["start"] < t1 - vo0 - 0.05]
                row["vo_land"] = [" ".join(said).strip()]
                rows.append(row)
        # Fast continuations that lack a distinct window become edit-holds.
        by_id = {f"P{n}:{r['id']}": r for r in rows}
        for r in rows:
            if not r.get("added") or r.get("v01_parent_quality") != "Fast":
                continue
            parent_id = r["id"].rsplit("_c", 1)[0]
            parent = by_id[f"P{n}:{parent_id}"]
            unused = round(CLIP_USE_S - parent["use_s"], 2)
            shortfall = round(r["use_s"] - max(unused, 0), 2)
            r["reuse_measurement"] = {
                "source_row": f"P{n}:{parent_id}",
                "source_clip_usable_s": CLIP_USE_S,
                "source_used_s": parent["use_s"],
                "unused_usable_s": max(unused, 0),
                "required_use_s": r["use_s"],
                "shortfall_usable_s": max(shortfall, 0),
                "distinct_window": shortfall <= 0,
            }
            if shortfall > 0:
                r.update({
                    "quality": "reuse", "route_kind": "edit-hold", "prompt": None,
                    "reuse_of": f"P{n}:{parent_id}",
                    "engine_reason": (
                        "Flow-first, as the 009 J0261 price pass: a Fast continuation is an edit-hold "
                        f"of the parent KEEP. No second mint, no loop, no freeze. Unused usable footage "
                        f"is {max(unused, 0)} s against {r['use_s']} s needed."
                    ),
                    "reference": f"P{n}:{parent_id}",
                    "v01_quality": "Fast",
                })
        for r in rows:
            if r.get("added") and r.get("v01_parent_quality") == "Quality":
                parent_id = r["id"].rsplit("_c", 1)[0]
                parent = by_id[f"P{n}:{parent_id}"]
                unused = round(CLIP_USE_S - parent["use_s"], 2)
                r["quality_continuation"] = {
                    "source_row": f"P{n}:{parent_id}",
                    "unused_usable_s": max(unused, 0),
                    "required_use_s": r["use_s"],
                    "shortfall_usable_s": round(max(r["use_s"] - max(unused, 0), 0), 2),
                    "kept_as": "Quality mint. An edit-hold cannot cover it.",
                }
        for r in rows:
            rows_by_key[f"P{n}:{r['id']}"] = r
        boards[n] = rows

    if short:
        raise SystemExit("plates under %.1f s:\n" % MIN_PLATE_S + "\n".join(
            f"  part {n} {pid} at {t}: {u} s ({phrase})" for n, pid, t, u, phrase in short))

    cum_flow = 0
    cum_vx = 0.0
    for key, r in rows_by_key.items():
        q = r["quality"]
        if r.get("route_kind") == "edit-hold":
            priced = zero_route("edit-hold")
        elif q == "reuse":
            priced = zero_route("reuse")
        elif q == "code_graphic":
            priced = zero_route("code-graphic")
        else:
            need = min(r["use_s"] + 0.5, 8.0)
            priced = price_mint(q, need)
            cum_flow += priced["flow_credits_expected"]
            cum_vx += priced["vertex_expected_gbp"]
        r.update(priced)
        r["cum_flow_credits_expected"] = cum_flow
        r["cum_vertex_expected_gbp"] = round(cum_vx, 2)

    OUT.mkdir(exist_ok=True)
    totals = {k: 0 for k in (
        "rows", "Quality", "Fast", "code_graphic", "edit_hold", "reuse", "added", "explorer",
        "flow_credits_try1", "flow_credits_expected")}
    totals["vertex_try1_gbp"] = 0.0
    totals["vertex_expected_gbp"] = 0.0
    per_part = []
    for n, rows in boards.items():
        meta = parts_meta[n - 1]
        counts = {
            "rows": len(rows),
            "Quality": sum(r["quality"] == "Quality" for r in rows),
            "Fast": sum(r["quality"] == "Fast" for r in rows),
            "code_graphic": sum(r["quality"] == "code_graphic" for r in rows),
            "edit_hold": sum(r.get("route") == "edit-hold" for r in rows),
            "reuse": sum(r["quality"] == "reuse" and r.get("route") == "reuse" for r in rows),
            "added": sum(bool(r.get("added")) for r in rows),
        }
        ne = sum(bool(r["explorer"]) for r in rows)
        assert ne <= 1, (n, ne)
        board = {
            "part": f"{n:02d}",
            "title": f"Part {n:02d} — {TITLES[n]}",
            "film": "010_Alvarez-Clay-Line-Dinosaurs",
            "working_title": "What Killed the Dinosaurs Was Hidden in a Line of Clay",
            "mint": False,
            "status": "BOARD_V01_PARKED_FOR_CHIEF",
            "house": ("STUDIO_PLAYBOOK.md §5. Rows from SHOT_LIST_v01.md (Claude, 6 Oct 2026), "
                      "timed from the locked VO Scribe words and priced Flow-first by Cursor, 15 Oct 2026 "
                      "(J0314, _build_plate_boards_v01.py). Nothing here is generation_authorized."),
            "vo_file": f"02_Voiceover/{meta['file']}",
            "vo_sha256": meta["sha256"],
            "vo_duration_s": meta["duration_s"],
            "chapter_card": None if n == 1 else {
                "text": TITLES[n], "in_s": meta["card_in_film_s"], "hold_s": 1.5,
                "treatment": "soft cross-fade after the part's end + 0.6 s breath; music continues",
            },
            "explorer_lock": "At most one plate in this part. On model. Never a Short frame 0.",
            "forbidden": "Orbit. Photoreal. Ken Burns. Readable words or numbers. An impact, a fireball, burning animals, or a dinosaur in distress. A reactor. A published gravity map copied as a plate.",
            "motion_lock": "Real camera or object motion on every minted plate. No freeze-pad, no loop. An edit-hold is shorter than the line unless a later pass authorises a mint.",
            "rules": [
                "The asteroid strike is never shown hitting.",
                "Walter is clean-shaven, fair-haired, dark-rimmed glasses. Luis has white thinning hair and glasses. Asaro and Michel are kind likenesses in lab coats. No reactor.",
                "No readable text in any plate. Every label, date and number is an edit overlay.",
                "Fast plates are non-emissive. Lamps, glow, water, space dust, molten iron and sunlit rock stay Quality or move to a £0 code graphic.",
                "Teach diagrams, the iridium graph, the maps and the scale cards are £0 code graphics.",
                "Short frame 0: Part 01 clay line, Part 03 space dust, Part 05 robin.",
            ],
            "vo_film_start_s": meta["vo_film_start_s"],
            "part_end_film_s": round(anchored_by_part[n][1] if n < 5 else meta["vo_film_end_s"] + TAIL_S, 2),
            "clip_use_s": CLIP_USE_S,
            "xfade_s": 0.35,
            "explorer_plates": ne,
            "counts": counts,
            "plates": rows,
        }
        (OUT / f"part-{n:02d}_plates_v01.json").write_text(json.dumps(board, indent=2, ensure_ascii=False) + "\n")
        pp = dict(counts)
        pp["part"] = n
        pp["flow_credits_try1"] = sum(r["flow_credits_try1"] for r in rows)
        pp["flow_credits_expected"] = sum(r["flow_credits_expected"] for r in rows)
        pp["vertex_try1_gbp"] = round(sum(r["vertex_try1_gbp"] for r in rows), 2)
        pp["vertex_expected_gbp"] = round(sum(r["vertex_expected_gbp"] for r in rows), 2)
        per_part.append(pp)
        for f in ("rows", "Quality", "Fast", "code_graphic", "edit_hold", "reuse", "added",
                  "flow_credits_try1", "flow_credits_expected"):
            totals[f] += pp[f]
        totals["vertex_try1_gbp"] += pp["vertex_try1_gbp"]
        totals["vertex_expected_gbp"] += pp["vertex_expected_gbp"]
        totals["explorer"] += ne
        print(f"part {n:02d}: {pp['rows']} rows = {pp['Quality']} Q + {pp['Fast']} F + "
              f"{pp['code_graphic']} code + {pp['edit_hold']} hold + {pp['reuse']} reuse; "
              f"Flow {pp['flow_credits_expected']} · Vertex £{pp['vertex_expected_gbp']:.2f}")

    totals["vertex_try1_gbp"] = round(totals["vertex_try1_gbp"], 2)
    totals["vertex_expected_gbp"] = round(totals["vertex_expected_gbp"], 2)
    usable_vx = round(VERTEX_BALANCE_GBP - VERTEX_MARGIN_GBP, 2)
    holds = []
    qcont = []
    for key, r in rows_by_key.items():
        if r.get("route") == "edit-hold":
            m = r["reuse_measurement"]
            holds.append((key, r["use_s"], m["source_row"], m["source_used_s"], m["unused_usable_s"], m["shortfall_usable_s"]))
        if r.get("quality_continuation"):
            m = r["quality_continuation"]
            qcont.append((key, r["use_s"], m["source_row"], m["unused_usable_s"], m["shortfall_usable_s"]))

    plan = {
        "film": "010_Alvarez-Clay-Line-Dinosaurs",
        "written": "2026-10-15",
        "task": "J0314: plate boards v01 from the locked script and VO. Flow-first prices. Mint nothing. Parked for Chief.",
        "shot_list": "07_Edit-Project/SHOT_LIST_v01.md",
        "vo": "02_Voiceover/VO_TAKES_KEEP.json status LOCKED v01 (Chief KEEP, desk #180 comment 6101773293, 11 Oct)",
        "readings": {
            "flow_credits_left": FLOW_CREDITS_LEFT,
            "flow_read_at": FLOW_READ_AT,
            "flow_note": "J0313 fresh Flow read. No Flow spend logged after it. Not re-read for this no-spend job.",
            "vertex_promo_gbp": VERTEX_BALANCE_GBP,
            "vertex_read_at": VERTEX_READ_AT,
            "vertex_margin_gbp": VERTEX_MARGIN_GBP,
            "vertex_usable_gbp": usable_vx,
            "vertex_note": "Not re-read. The route stays Flow-first.",
        },
        "rates": {
            "flow_credits_per_take": FLOW_CREDITS,
            "vertex_usd_per_s": USD_PER_S,
            "usd_per_still": USD_PER_STILL,
            "gbp_per_usd_planning": GBP_PER_USD,
            "takes_per_keep_005": TAKES_PER_KEEP,
            "stills_per_plate_005": STILLS_PER_PLATE,
        },
        "vo_film_total_s": round(parts_meta[-1]["vo_film_end_s"] + TAIL_S, 2),
        "totals": totals,
        "per_part": per_part,
        "fits_now": {
            "flow": totals["flow_credits_expected"] <= FLOW_CREDITS_LEFT,
            "vertex": totals["vertex_expected_gbp"] <= usable_vx,
        },
        "departures_from_shot_list": [
            "Plates start where the locked VO says the line, not on the script's estimated clock.",
            "Denmark's cliff is shown when the white sea cliff is said. The world map follows, on 'all around the world'.",
            "The pigeon is inside the robin plate. Shot-list 05-10 was a named cut-first cutaway, and the two birds are one breath.",
            "The Italy-to-California map (shot-list 02-09, a named cut-first cutaway) is not its own plate. The wrap covers the trip home.",
            "Pyramid tracks, the iridium graph, both maps, the two clocks, the layer stack, the clock diagram, the supernova test, the 10 km scale, the food-chain icons, the crater scale and the question-mark map are £0 code graphics.",
            "The glowing Chicxulub ring stays Quality. It is a new stylised map, not a published one.",
            "Same-moment is a new Quality plate of the Gubbio cliff with a glow. It does not replay the opening clip.",
            "Part 02's Explorer sits on 'only a few very small ones', between the empty rock and the pull-back.",
            "Part 05's Explorer ends when the survival question starts. That question is a £0 icon card. The clay-line callback is its own Quality plate, then the bird at the window.",
            "Overlay 'A HAMMER · A VIAL · A PAPER' is shortened to HAMMER, VIAL, PAPER so the label stays at four words or fewer.",
        ],
    }
    (EDIT / "PICTURE_PLAN_v01.json").write_text(json.dumps(plan, indent=2, ensure_ascii=False) + "\n")
    (EDIT / "VO_RETIME_v01.json").write_text(json.dumps({
        "source": "Scribe stt_raw.json word starts, aligned on each plate's find-phrase. No new transcription.",
        "card_breath_s": CARD_BREATH_S,
        "card_to_vo_s": CARD_TO_VO_S,
        "parts": parts_meta,
        "plates": [{"part": n, "id": r["id"], "t_s": r["t_s"], "use_s": r["use_s"], "find": r.get("find")}
                   for n, rows in boards.items() for r in rows if not r.get("added")],
    }, indent=2) + "\n")

    lines = [
        "# 010 price review v01",
        "",
        "Cursor, 15 Oct 2026, J0314. Boards only. **No mint. No spend.**",
        "Flow-first from the start, on the same table as the 009 J0261 price pass. Parked for Chief.",
        "",
        "Locked VO: Chief KEEP, desk #180 comment 6101773293. "
        + ", ".join(f"part {p['part']} {p['duration_s']}s" for p in parts_meta)
        + f". Film picture {plan['vo_film_total_s']}s with the closing breath.",
        "",
        "## Readings",
        "",
        f"- Flow: **{FLOW_CREDITS_LEFT}** credits at {FLOW_READ_AT} (J0313, CDP :9222). No spend logged after it. Not re-read.",
        f"- Vertex promo: **£{VERTEX_BALANCE_GBP:.2f}** at {VERTEX_READ_AT}. Usable **£{usable_vx:.2f}** after the £1 margin. Not re-read. The route stays Flow-first.",
        "",
        "## Totals",
        "",
        "| | rows | Quality | Fast | code | edit-hold | reuse | Flow try-1 | Flow expected | Vertex try-1 | Vertex expected |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for pp in per_part:
        lines.append(
            f"| Part {pp['part']:02d} | {pp['rows']} | {pp['Quality']} | {pp['Fast']} | {pp['code_graphic']} | "
            f"{pp['edit_hold']} | {pp['reuse']} | {pp['flow_credits_try1']} | {pp['flow_credits_expected']} | "
            f"£{pp['vertex_try1_gbp']:.2f} | £{pp['vertex_expected_gbp']:.2f} |"
        )
    lines.append(
        f"| **Film** | **{totals['rows']}** | **{totals['Quality']}** | **{totals['Fast']}** | **{totals['code_graphic']}** | "
        f"**{totals['edit_hold']}** | **{totals['reuse']}** | **{totals['flow_credits_try1']}** | "
        f"**{totals['flow_credits_expected']}** | **£{totals['vertex_try1_gbp']:.2f}** | **£{totals['vertex_expected_gbp']:.2f}** |"
    )
    lines += [
        "",
        f"All on Flow: {'FITS' if plan['fits_now']['flow'] else 'DOES NOT FIT'} "
        f"({totals['flow_credits_expected']} expected vs {FLOW_CREDITS_LEFT} left).",
        f"All on Vertex: {'FITS' if plan['fits_now']['vertex'] else 'DOES NOT FIT'} "
        f"(£{totals['vertex_expected_gbp']:.2f} expected vs £{usable_vx:.2f} usable).",
        "",
        "006, 007, 008 and 009 still share this pot. 009 v02 expected 13,848, 008 v03 expected 5,605, "
        "and the 007 review expected about 7,550. Those three already add up past 23,740 if they all mint. "
        "010's figure is on top. Mint order stays the Chief's call. This board does not mint.",
        "",
        "Rates are 006/008/009's: Flow Fast 10 / Quality 100 a take; expected uses 005's takes-per-KEEP "
        "(Quality 2.59, Fast 1.96) plus stills. Vertex is list price, 1080p, £0.80 per dollar, clip length 4/6/8 s.",
        "",
        "## 1. Teach diagrams → £0 code graphics",
        "",
        f"{totals['code_graphic']} rows. Flow and Vertex are 0.",
        "",
        "## 2. Fast continuations → edit-hold",
        "",
        "No second mint. An 8.00 s clip (7.90 s usable) does not leave a distinct window.",
        "",
        "| Row | Needed s | Parent | Parent use s | Unused usable s | Shortfall s |",
        "|---|---:|---|---:|---:|---:|",
    ]
    if not holds:
        lines.append("| — | | | | | |")
    for key, need, parent, used, unused, gap in holds:
        lines.append(f"| {key} | {need} | {parent} | {used} | {unused} | {gap} |")
    lines += [
        "",
        "## 3. Quality continuations",
        "",
        "Each stays a second Quality mint. An edit-hold cannot cover it.",
        "",
        "| Row | Needed s | Parent | Unused usable s | Shortfall s |",
        "|---|---:|---|---:|---:|",
    ]
    if not qcont:
        lines.append("| — | | | | |")
    for key, need, parent, unused, gap in qcont:
        lines.append(f"| {key} | {need} | {parent} | {unused} | {gap} |")
    lines += ["", "## What changed against the shot list", ""]
    for item in plan["departures_from_shot_list"]:
        lines.append(f"- {item}")
    lines += [
        "",
        "## For the Chief",
        "",
        "Mint order, after 006, 007, 008 and 009, stays the Chief's call. No mint in this pass.",
        "",
    ]
    (EDIT / "PRICE_REVIEW_v01.md").write_text("\n".join(lines))
    print(f"film: {totals['rows']} rows = {totals['Quality']} Q + {totals['Fast']} F + "
          f"{totals['code_graphic']} code + {totals['edit_hold']} hold + {totals['reuse']} reuse")
    print(f"Flow {totals['flow_credits_expected']} expected vs {FLOW_CREDITS_LEFT} "
          f"{'FIT' if plan['fits_now']['flow'] else 'OVER'}")
    print(f"Vertex £{totals['vertex_expected_gbp']:.2f} expected vs £{usable_vx:.2f} "
          f"{'FIT' if plan['fits_now']['vertex'] else 'OVER'}")


if __name__ == "__main__":
    main()
