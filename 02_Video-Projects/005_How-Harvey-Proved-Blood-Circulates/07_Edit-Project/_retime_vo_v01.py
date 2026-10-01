#!/usr/bin/env python3
"""HOS 005: re-time every sentence from the recorded VO v01 (word timestamps).

Run with the faster-whisper venv:
  ~/.venvs/hos-vo/bin/python 07_Edit-Project/_retime_vo_v01.py

Writes 07_Edit-Project/VO_RETIME_v01.json: per part, each script sentence with
its start/end inside the part take and on the film timeline.

Film timeline: Part 01 VO starts at 0:00. Before Parts 02-05 the chapter card
fades in CARD_BREATH_S after the last word of the previous part, holds, and the
next part's VO starts CARD_TO_VO_S after the card comes in.
"""
from __future__ import annotations

import difflib
import json
import re
from pathlib import Path

from faster_whisper import WhisperModel

PROJ = Path(__file__).resolve().parents[1]
VO = PROJ / "02_Voiceover"
OUT = PROJ / "07_Edit-Project/VO_RETIME_v01.json"
FINISH = json.loads((VO / "VO_FINISH_v01.json").read_text())

CARD_BREATH_S = 0.6
CARD_TO_VO_S = 1.9
CHAPTERS = {
    2: "The Liver That Made Blood",
    3: "The Sum That Broke the Old Idea",
    4: "The Tied Arm",
    5: "The Vessels He Never Saw",
}

NUM = {"sixteen-sixteen": "sixteen sixteen"}


def norm_tokens(text: str) -> list[str]:
    t = text.lower()
    for k, v in NUM.items():
        t = t.replace(k, v)
    t = re.sub(r"[^a-z0-9' ]+", " ", t.replace("-", " "))
    return [w.strip("'") for w in t.split() if w.strip("'")]


def sentences(text: str) -> list[str]:
    out: list[str] = []
    for para in [p.strip() for p in text.split("\n") if p.strip()]:
        out += [s.strip() for s in re.split(r"(?<=[.?!])\s+(?=[A-Z\"])", para) if s.strip()]
    return out


def fmt(s: float) -> str:
    m, sec = divmod(s, 60)
    return f"{int(m)}:{sec:05.2f}"


def main() -> None:
    model = WhisperModel("small.en", device="cpu", compute_type="int8")
    parts_out = []
    film_cursor = 0.0
    for p in FINISH["parts"]:
        n = p["part"]
        take = VO / p["file"]
        txt = (VO / p["file"].replace(".mp3", ".txt")).read_text()
        sents = sentences(txt)
        segs, _ = model.transcribe(str(take), word_timestamps=True)
        words = [w for s in segs for w in (s.words or [])]
        heard = [norm_tokens(w.word) for w in words]
        heard_flat: list[str] = []
        heard_idx: list[int] = []
        for i, toks in enumerate(heard):
            for t in toks:
                heard_flat.append(t)
                heard_idx.append(i)

        script_flat: list[str] = []
        sent_first: list[int] = []
        sent_last: list[int] = []
        for s in sents:
            toks = norm_tokens(s)
            sent_first.append(len(script_flat))
            script_flat += toks
            sent_last.append(len(script_flat) - 1)

        sm = difflib.SequenceMatcher(a=script_flat, b=heard_flat, autojunk=False)
        a2b: dict[int, int] = {}
        for blk in sm.get_matching_blocks():
            for k in range(blk.size):
                a2b[blk.a + k] = blk.b + k

        def map_fwd(ai: int) -> int:
            for j in range(ai, len(script_flat)):
                if j in a2b:
                    return a2b[j]
            return len(heard_flat) - 1

        def map_back(ai: int) -> int:
            for j in range(ai, -1, -1):
                if j in a2b:
                    return a2b[j]
            return 0

        if n > 1:
            card_in = film_cursor + CARD_BREATH_S
            vo_film_start = card_in + CARD_TO_VO_S
        else:
            card_in = None
            vo_film_start = 0.0

        rows = []
        for i, s in enumerate(sents):
            w0 = words[heard_idx[map_fwd(sent_first[i])]]
            w1 = words[heard_idx[map_back(sent_last[i])]]
            rows.append({
                "i": i + 1,
                "text": s,
                "start_s": round(w0.start, 2),
                "end_s": round(w1.end, 2),
                "film_s": round(vo_film_start + w0.start, 2),
                "film": fmt(vo_film_start + w0.start),
            })
        last_word_end = rows[-1]["end_s"]
        film_end = vo_film_start + p["duration_s"]
        parts_out.append({
            "part": n,
            "file": p["file"],
            "sha256": p["sha256"],
            "duration_s": p["duration_s"],
            "chapter_card": CHAPTERS.get(n),
            "card_in_film_s": round(card_in, 2) if card_in is not None else None,
            "card_in_film": fmt(card_in) if card_in is not None else None,
            "vo_film_start_s": round(vo_film_start, 2),
            "vo_film_start": fmt(vo_film_start),
            "vo_film_end_s": round(film_end, 2),
            "vo_film_end": fmt(film_end),
            "last_word_s": last_word_end,
            "sentences": rows,
        })
        film_cursor = film_end
        print(f"part {n:02d}: card {fmt(card_in) if card_in else '—'}  vo {fmt(vo_film_start)}–{fmt(film_end)}  {len(rows)} sentences", flush=True)

    out = {
        "film": "005_How-Harvey-Proved-Blood-Circulates",
        "source": "VO v01 part takes (VO_FINISH_v01.json), faster-whisper small.en word timestamps",
        "card_breath_s": CARD_BREATH_S,
        "card_to_vo_s": CARD_TO_VO_S,
        "vo_film_total_s": round(film_cursor, 2),
        "vo_film_total": fmt(film_cursor),
        "parts": parts_out,
    }
    OUT.write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n")
    print(f"wrote {OUT} total {fmt(film_cursor)}", flush=True)


if __name__ == "__main__":
    main()
