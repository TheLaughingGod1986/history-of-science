#!/usr/bin/env python3
"""HOS 007: time every sentence and word of the locked VO (VO_TAKES_KEEP.json).

Run with the faster-whisper venv:
  ~/.venvs/hos-vo/bin/python 07_Edit-Project/_retime_vo_v01.py

Writes 07_Edit-Project/VO_RETIME_v01.json, as 006's VO_RETIME_v02.json, plus each part's
word starts (`words`) so a plate can start on a word boundary inside a sentence.

Film timeline (as 005/006): Part 01 VO starts at 0:00. Before Parts 02-05 the chapter card
fades in CARD_BREATH_S after the end of the previous part, holds, and the next part's VO
starts CARD_TO_VO_S after the card comes in.
"""
from __future__ import annotations

import difflib
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

from faster_whisper import WhisperModel

PROJ = Path(__file__).resolve().parents[1]
REPO = PROJ.parents[1]
sys.path.insert(0, str(REPO / "00_Brand/Channel-Setup/tools"))
from vo_check import norm  # noqa: E402

VO = PROJ / "02_Voiceover"
OUT = PROJ / "07_Edit-Project/VO_RETIME_v01.json"
KEEP = json.loads((VO / "VO_TAKES_KEEP.json").read_text())

CARD_BREATH_S = 0.6
CARD_TO_VO_S = 1.9
TEXT = {
    1: "part01_the_speckled_monster.txt",
    2: "part02_the_milkmaids_secret.txt",
    3: "part03_a_pail_a_lancet_and_a_boy.txt",
    4: "part04_the_test.txt",
    5: "part05_the_word_that_saved_millions.txt",
}
CHAPTERS = {
    2: "The Milkmaids' Secret",
    3: "A Pail, a Lancet and a Boy",
    4: "The Test",
    5: "The Word That Saved Millions",
}


def sentences(text: str) -> list[str]:
    out: list[str] = []
    for para in [p.strip() for p in text.split("\n") if p.strip()]:
        out += [s.strip() for s in re.split(r"(?<=[.?!])\s+(?=[A-Z\"“])", para) if s.strip()]
    return out


def fmt(s: float) -> str:
    m, sec = divmod(s, 60)
    return f"{int(m)}:{sec:05.2f}"


def duration(path: Path) -> float:
    return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                          "-of", "default=noprint_wrappers=1:nokey=1", str(path)], text=True))


def main() -> None:
    model = WhisperModel("small.en", device="cpu", compute_type="int8")
    parts_out = []
    film_cursor = 0.0
    for n in range(1, 6):
        take = VO / KEEP["locked"][f"{n:02d}"]["file"]
        sha = hashlib.sha256(take.read_bytes()).hexdigest()
        dur = round(duration(take), 2)
        sents = sentences((VO / TEXT[n]).read_text())
        segs, _ = model.transcribe(str(take), word_timestamps=True)
        words = [w for s in segs for w in (s.words or [])]
        heard_flat: list[str] = []
        heard_idx: list[int] = []
        for i, w in enumerate(words):
            for t in norm(w.word):
                heard_flat.append(t)
                heard_idx.append(i)

        script_flat: list[str] = []
        sent_first: list[int] = []
        sent_last: list[int] = []
        for s in sents:
            toks = norm(s)
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
        prev_last_word = -1
        for i, s in enumerate(sents):
            last_word = heard_idx[map_back(sent_last[i])]
            first_word = prev_last_word + 1 if i else heard_idx[map_fwd(sent_first[i])]
            first_word = min(first_word, last_word)
            w0, w1 = words[first_word], words[last_word]
            prev_last_word = last_word
            rows.append({
                "i": i + 1,
                "text": s,
                "start_s": round(w0.start, 2),
                "end_s": round(w1.end, 2),
                "film_s": round(vo_film_start + w0.start, 2),
                "film": fmt(vo_film_start + w0.start),
            })
        film_end = vo_film_start + dur
        parts_out.append({
            "part": n,
            "file": take.name,
            "sha256": sha,
            "duration_s": dur,
            "match_rate_pct": round(100 * len(a2b) / max(1, len(script_flat)), 1),
            "chapter_card": CHAPTERS.get(n),
            "card_in_film_s": round(card_in, 2) if card_in is not None else None,
            "card_in_film": fmt(card_in) if card_in is not None else None,
            "vo_film_start_s": round(vo_film_start, 2),
            "vo_film_start": fmt(vo_film_start),
            "vo_film_end_s": round(film_end, 2),
            "vo_film_end": fmt(film_end),
            "last_word_s": rows[-1]["end_s"],
            "sentences": rows,
            "words": [[round(w.start, 2), w.word.strip()] for w in words],
        })
        film_cursor = film_end
        print(f"part {n:02d}: card {fmt(card_in) if card_in else '—'}  vo {fmt(vo_film_start)}–{fmt(film_end)}  "
              f"{len(rows)} sentences, match {parts_out[-1]['match_rate_pct']}%", flush=True)

    out = {
        "film": "007_The-First-Vaccine",
        "source": "Locked VO (VO_TAKES_KEEP.json), faster-whisper small.en word timestamps, vo_check.norm()",
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
