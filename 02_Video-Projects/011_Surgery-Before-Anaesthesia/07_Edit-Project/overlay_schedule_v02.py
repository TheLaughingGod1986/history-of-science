"""Word-accurate overlay cue schedule for the Anaesthesia rough.

A card starts when the last word of its spoken phrase starts, so the full
phrase is not shown early. A card that would sit on another card is held.
Unspoken dates, prices and comparisons stay held. Narration is not changed.
"""
import hashlib
import json
import pathlib
import re

HERE = pathlib.Path(__file__).resolve().parent
WHO_S = 3.2
CARD_S = 2.0


def norm(text):
    return re.sub(r"[^a-z0-9]+", "", text.lower())


def load():
    plan = json.loads((HERE / "PICTURE_PLAN_v03.json").read_text())
    raw_path = HERE.parent / plan["vo_lock"]["stt_raw"]
    stt = json.loads(raw_path.read_text())
    words = [
        dict(word, raw_index=index)
        for index, word in enumerate(stt["words"])
        if word["type"] == "word"
    ]
    manifest = json.loads((HERE / "ASSEMBLY_SOURCES_v01.json").read_text())
    return plan, words, raw_path, manifest


def find_phrase(words, tokens, phrase):
    target = [norm(part) for part in phrase.split()]
    hits = [
        index
        for index in range(len(tokens) - len(target) + 1)
        if tokens[index : index + len(target)] == target
    ]
    return target, hits


# Exact spoken phrases for markers that already had a word anchor.
ANCHORS = {
    ("P1:01a", "when"): "Before 1846",
    ("P1:01b", "label"): "fastest",
    ("P1:02a", "when"): "Europe and America",
    ("P1:03a", "who"): "Robert Liston",
    ("P1:04a", "when"): "autumn of 1846",
    ("P1:05a", "label"): "glass globe",
    ("P1:08a", "when"): "1840",
    ("P1:09c", "when"): "nearly fifty years earlier",
    ("P2:02a", "who"): "Humphry Davy",
    ("P2:02a", "when"): "1800 in Bristol",
    ("P2:02b", "label"): "nitrous oxide",
    ("P2:06a", "when"): "next morning",
    ("P2:07a", "who"): "Crawford Long",
    ("P2:09b_arch_long_1849", "when"): "another seven years",
    ("P3:02a", "who"): "Horace Wells",
    ("P3:02a", "when"): "December 1844",
    ("P3:03a", "when"): "The next day",
    ("P3:05a", "who"): "William Morton",
    ("P3:05b", "label"): "ether",
    ("P3:08a", "who"): "John Collins Warren",
    ("P4:04a", "who"): "Oliver Wendell Holmes",
    ("P4:04c_cg_anesthesia_etymology", "label"): "anesthesia",
    ("P4:05b", "who"): "Charles Jackson",
    ("P4:09a", "fact"): "doesn't name a single one of them",
    ("P5:02a", "when"): "21st of December 1846 in London",
    ("P5:04b", "who"): "James Young Simpson",
    ("P5:05a", "label"): "chloroform",
    ("P5:06b", "who"): "John Snow",
    ("P5:09a", "when"): "Today",
    ("P5:11a", "label"): "anesthetist",
}
TEXT = {
    ("P1:01a", "when"): "Before 1846",
    ("P1:01b", "label"): "FASTEST",
    ("P1:02a", "when"): "Europe & America",
    ("P1:04a", "when"): "Autumn 1846",
    ("P1:05a", "label"): "GLASS GLOBE",
    ("P1:09c", "when"): "Nearly fifty years earlier",
    ("P2:06a", "when"): "The next morning",
    ("P2:09b_arch_long_1849", "when"): "Seven years later",
    ("P3:02a", "when"): "December 1844",
    ("P3:03a", "when"): "The next day",
    ("P4:09a", "fact"): "No claimant named",
    ("P5:02a", "when"): "London, 21 December 1846",
}
# Spoken replacements for planned lines that add a date, price or place the
# narration does not say in one phrase. The card uses only the spoken part.
EXTRAS = {
    ("P3:02a", "when"): [
        {
            "phrase": "Hartford",
            "text": "Hartford",
            "part": "place",
            "replaces_anchor": True,
            "note": "Hartford is spoken. December 1844 is spoken during the Wells name card, so that date stays off this card.",
            "remainder": "December 1844 is spoken while the Horace Wells name card is up, so it is not a second card.",
        }
    ],
    ("P3:06a", "when"): [
        {
            "phrase": "sixteenth of October 1846",
            "text": "16 October 1846",
            "note": "The date is spoken here. The opening Boston line is earlier and does not say this date. Boston in this sentence comes after the year, so it is not on the card.",
        }
    ],
    ("P4:02b", "fact"): [
        {
            "phrase": "patent",
            "text": "Patent",
            "note": "The word patent is spoken. Patent number 4,848 is not spoken.",
            "remainder": "Patent number 4,848 is not spoken.",
        }
    ],
    ("P4:04a", "when"): [
        {
            "phrase": "a month after",
            "text": "A month after",
            "note": "The narration says a month after the operation. 21 November 1846 is not spoken.",
        }
    ],
    ("P4:06a_cg_master_timeline", "data"): [
        {
            "phrase": "two years earlier",
            "text": "Two years earlier",
            "note": "The timeline may repeat only dates already spoken before this line: 1800, March 1842, December 1844 and 16 October 1846. It must not add an unspoken span such as four years or 42 years.",
            "recap_spoken_at_s": [87.72, 149.00, 182.60, 225.14],
        }
    ],
    ("P4:08a", "when"): [
        {
            "phrase": "public garden",
            "text": "Public garden",
            "note": "Public garden is spoken in the next row. 1868 is not spoken.",
        }
    ],
    ("P5:04b", "when"): [
        {
            "phrase": "next year in Edinburgh",
            "text": "Next year, Edinburgh",
            "note": "4 November 1847 is not spoken.",
        }
    ],
    ("P5:06b", "when"): [
        {
            "phrase": "1853",
            "text": "1853",
            "note": "7 April is not spoken. London is the next sentence, so it is not on this card.",
        }
    ],
    ("P5:09b_cg_safety_stadium", "data"): [
        {
            "phrase": "one in every hundred thousand",
            "text": "1 in 100,000",
            "part": "rate",
            "note": "The digits are the spoken rate. Wembley is not spoken.",
        },
        {
            "phrase": "stadium full of 90,000 people",
            "text": "90,000 people",
            "part": "stadium",
            "note": "Spoken scale is a stadium of 90,000 people. Wembley is not spoken.",
        },
    ],
}
HOLDS = {
    ("P1:03b", "fact"): "The narration says a few minutes. It does not say under 3 minutes, so that number stays off the card.",
    ("P1:04b_cg_stopwatch_scale", "data"): "The stopwatch line is not spoken. Three minutes and the egg comparison are not in the narration.",
    ("P1:05a", "when"): "Boston is spoken here, but 16 October 1846 is not. That date is scheduled when it is spoken later. Showing it on this line would be early.",
    ("P2:05a_arch_laughing_gas_broadside", "when"): "Early 1800s is not spoken in this row.",
    ("P2:07b_cg_timeline_42yr", "when"): "Jefferson and 30 March are not spoken. March 1842 is spoken while the Crawford Long name card is still up, so the date is held instead of covering the name.",
    ("P2:07b_cg_timeline_42yr", "data"): "The 42-year span and the working-lifetime comparison are not spoken.",
    ("P2:08a", "fact"): "The two-dollar price is not spoken.",
    ("P3:04a", "when"): "January 1845 is not spoken. Boston alone is not this date.",
    ("P4:02b", "when"): "12 November 1846 is not spoken. The patent word is scheduled on its own.",
}
SCALE_HELD = {
    "P1:04b_cg_stopwatch_scale": "Boiling an egg is not spoken.",
    "P2:07b_cg_timeline_42yr": "A working lifetime is not spoken.",
    "P4:06a_cg_master_timeline": "Four years from the Georgia towel to the Ether Dome is not spoken.",
    "P5:09b_cg_safety_stadium": "Wembley is not spoken. The spoken comparison is a stadium full of 90,000 people, and that is a scheduled card.",
}


def cue_from_phrase(plan, words, tokens, row, kind, phrase, text, note, extra):
    target, hits = find_phrase(words, tokens, phrase)
    if not hits:
        return None, {
            "row_id": row["row_id"],
            "kind": kind,
            "planned_text": row["markers"].get(kind, text),
            "status": "held",
            "reason": f"Exact spoken phrase not found: {phrase}",
        }
    if kind == "who":
        start_at = hits[0]
    else:
        start_at = min(hits, key=lambda index: abs(words[index]["start"] - row["in_s"]))
    chosen = words[start_at : start_at + len(target)]
    reveal = chosen[-1]
    item = {
        "row_id": row["row_id"],
        "kind": kind,
        "planned_text": row["markers"].get(kind, text),
        "text": text,
        "anchor_text": " ".join(word["text"] for word in chosen),
        "word_indices": list(range(start_at, start_at + len(target))),
        "raw_stt_indices": [word["raw_index"] for word in chosen],
        "in_s": reveal["start"],
        "evidence_end_s": reveal["end"],
        "row_window_s": [row["in_s"], row["out_s"]],
        "status": "scheduled",
        "note": note,
    }
    if extra.get("part"):
        item["part"] = extra["part"]
    if extra.get("recap_spoken_at_s"):
        item["recap_spoken_at_s"] = extra["recap_spoken_at_s"]
    item["actual_row_id"] = next(
        other["row_id"]
        for other in plan["rows"]
        if other["in_s"] <= item["in_s"] < other["out_s"]
    )
    if item["actual_row_id"] != row["row_id"]:
        item["reconciliation"] = "The card follows the spoken words. The picture plan is unchanged."
    return item, None


def build():
    plan, words, raw_path, manifest = load()
    tokens = [norm(word["text"]) for word in words]
    rows = {row["row_id"]: row for row in plan["rows"]}
    proposed = []
    held = []
    seen = set()
    for row in plan["rows"]:
        for kind, planned in row["markers"].items():
            if kind not in ("who", "when", "data", "fact", "label"):
                continue
            key = (row["row_id"], kind)
            seen.add(key)
            extras = EXTRAS.get(key)
            if extras:
                for extra in extras:
                    if extra.get("replaces_anchor"):
                        pass
                    item, missing = cue_from_phrase(
                        plan,
                        words,
                        tokens,
                        row,
                        kind,
                        extra["phrase"],
                        extra["text"],
                        extra["note"],
                        extra,
                    )
                    if missing:
                        held.append(missing)
                    else:
                        proposed.append(item)
                    if extra.get("remainder"):
                        held.append(
                            {
                                "row_id": row["row_id"],
                                "kind": kind,
                                "part": "remainder",
                                "planned_text": planned,
                                "status": "held",
                                "reason": extra["remainder"],
                            }
                        )
                continue
            phrase = ANCHORS.get(key)
            if phrase is None:
                held.append(
                    {
                        "row_id": row["row_id"],
                        "kind": kind,
                        "planned_text": planned,
                        "status": "held",
                        "reason": HOLDS.get(key, "No exact spoken phrase for this planned line."),
                    }
                )
                continue
            item, missing = cue_from_phrase(
                plan,
                words,
                tokens,
                row,
                kind,
                phrase,
                TEXT.get(key, planned),
                "Spoken phrase. The card starts on its last word.",
                {},
            )
            if missing:
                held.append(missing)
            else:
                proposed.append(item)
    for key, reason in HOLDS.items():
        if key not in seen:
            held.append(
                {
                    "row_id": key[0],
                    "kind": key[1],
                    "planned_text": rows[key[0]]["markers"].get(key[1], ""),
                    "status": "held",
                    "reason": reason,
                }
            )
    duration = plan["vo_lock"]["duration_s"]
    for item in proposed:
        length = WHO_S if item["kind"] == "who" else CARD_S
        item["out_s"] = round(min(item["in_s"] + length, duration), 3)
        item["in_s"] = round(item["in_s"], 3)
    proposed.sort(key=lambda item: (item["in_s"], 0 if item["kind"] == "who" else 1, item["row_id"]))
    scheduled = []
    for item in proposed:
        conflict = next(
            (
                other
                for other in scheduled
                if other["in_s"] < item["out_s"] and item["in_s"] < other["out_s"]
            ),
            None,
        )
        # A person's first name card keeps the frame. The card already on screen
        # ends as the surname starts, when that still leaves it readable.
        if conflict and item["kind"] == "who" and conflict["kind"] != "who":
            visible = round(item["in_s"] - conflict["in_s"], 3)
            if visible >= 0.8:
                conflict["out_s"] = round(item["in_s"], 3)
                conflict["note"] = (
                    conflict.get("note", "").rstrip()
                    + " It ends when the name card starts."
                ).strip()
                conflict = None
        if conflict:
            item["status"] = "held"
            item["reason"] = (
                f"One card at a time. This overlaps {conflict['row_id']}/{conflict['kind']} "
                f"({conflict['text']}), which is already using the frame."
            )
            held.append(item)
        else:
            scheduled.append(item)
    credits = []
    for asset in manifest["assets"]:
        if asset["role"] not in ("archive", "portrait"):
            continue
        row = rows[asset["row_id"]]
        credit = asset.get("credit")
        if not credit:
            credits.append(
                {
                    "row_id": row["row_id"],
                    "kind": asset["role"] + "_credit",
                    "status": "held",
                    "reason": "The source manifest has no approved credit line for this portrait.",
                    "source_asset": asset["asset_id"],
                }
            )
            continue
        who = next(
            (
                cue
                for cue in scheduled
                if cue["kind"] == "who" and cue["row_id"] == row["row_id"]
            ),
            None,
        )
        name_on_picture = [
            f"{cue['row_id']}/{cue['kind']}"
            for cue in scheduled
            if cue["kind"] == "who"
            and cue["in_s"] < row["out_s"]
            and row["in_s"] < cue["out_s"]
        ]
        # A portrait line rides on that person's name card, including when the
        # name is spoken in a later row. An archive credit stays in the corner
        # unless a name card crosses the picture.
        if asset["role"] == "portrait" and who:
            credit_in, credit_out = who["in_s"], who["out_s"]
            status = "scheduled_with_name_card"
            name_cards = [f"{who['row_id']}/who"]
        elif name_on_picture:
            credit_in, credit_out = row["in_s"], row["out_s"]
            status = "held_layout_conflict"
            name_cards = name_on_picture
        else:
            credit_in, credit_out = row["in_s"], row["out_s"]
            status = "scheduled_corner_credit"
            name_cards = []
        credits.append(
            {
                "row_id": row["row_id"],
                "kind": asset["role"] + "_credit",
                "text": credit,
                "in_s": credit_in,
                "out_s": credit_out,
                "source_asset": asset["asset_id"],
                "page_url": asset.get("page_url"),
                "status": status,
                "name_cards_on_row": name_cards,
                "word_indices": who["word_indices"]
                if who and asset["role"] == "portrait"
                else [
                    index
                    for index, word in enumerate(words)
                    if credit_in <= word["start"] < credit_out
                ],
            }
        )
    scales = []
    for row in plan["rows"]:
        if "scale" not in row["markers"]:
            continue
        scales.append(
            {
                "row_id": row["row_id"],
                "planned_text": row["markers"]["scale"],
                "status": "held" if row["row_id"] in SCALE_HELD else "scheduled",
                "reason": SCALE_HELD.get(row["row_id"], "Spoken with its data card."),
            }
        )
    return {
        "job": "J2563",
        "status": "cue_schedule_not_a_film_pass",
        "generation_authorized": False,
        "spend_gbp": 0,
        "credits_used": 0,
        "stt_sha256": hashlib.sha256(raw_path.read_bytes()).hexdigest(),
        "word_index_basis": "zero-based filtered type=word list; raw_stt_indices also recorded",
        "reveal_rule": "in_s is the start of the last anchor word",
        "downloads": "not attempted; Wikimedia hold until 2026-11-13T05:30:00Z",
        "scheduled": scheduled,
        "held": held,
        "credits": credits,
        "scales": scales,
        "checks": {
            "scheduled_overlaps": 0,
            "no_card_before_its_last_word": True,
            "max_card_s": 4,
            "unresolved_holds": len(held),
            "layout_review_required": True,
            "film_stage_pass": False,
            "moving_video_review": False,
            "audio_review": False,
        },
        "render_notes": [
            "Do not draw a held line.",
            "The 008-010 opening experiment is not approved for 011.",
            "P5:16b stays a slate. No unused tail was measured.",
            "This schedule does not approve the picture, the edit, or a watch copy.",
        ],
    }


def main():
    result = build()
    destination = HERE / "OVERLAY_CUE_SCHEDULE_v02.json"
    destination.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n")
    print(
        f"{len(result['scheduled'])} scheduled; {len(result['held'])} held; "
        f"{sum(item['status']=='scheduled_corner_credit' for item in result['credits'])} corner credits; "
        f"{sum(item['status']=='held_layout_conflict' for item in result['credits'])} credit conflicts."
    )
    for item in result["scheduled"]:
        print(
            f"  {item['in_s']:7.2f}-{item['out_s']:7.2f} {item['row_id']:28} {item['kind']:5} {item['text']}"
        )
    print("-- held --")
    for item in result["held"]:
        print(f"  {item['row_id']:28} {item['kind']:5} {item.get('reason','')[:140]}")


if __name__ == "__main__":
    main()
