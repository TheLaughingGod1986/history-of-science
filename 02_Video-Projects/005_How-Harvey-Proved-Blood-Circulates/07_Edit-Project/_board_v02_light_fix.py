#!/usr/bin/env python3
"""Boards v02, Parts 02–05: the Fast-plate light fix approved on the desk (Claude, comment 5942662028).

- Fast plates: the candlelight/lamplight sentence becomes soft warm daylight from a window out of
  frame (Veo Fast painted lit candles into 6 of 6 candlelight takes in Part 01). Plates the VO puts
  at night are Quality already and keep their light.
- Fast plates set at dusk or evening that the VO doesn't put at night move to daylight too.
- `harvey_ref: true` on plates with Harvey on screen: start frames attach the Part 01 Harvey
  reference (04_Generated-Clips/refs/harvey_ref_v01.jpg) for the same face, gown and beard.

The original prompt stays in `prompt_v02_before_light_fix`. Idempotent.

  python3 07_Edit-Project/_board_v02_light_fix.py
"""
from __future__ import annotations

import json
import re
from pathlib import Path

PARTS = Path(__file__).resolve().parent / "parts"
DAYLIGHT = ("Soft warm daylight from a window out of frame. There are no candles, candlesticks, "
            "lamps or lanterns anywhere in the room.")
CANDLE_RE = re.compile(r"Warm (?:candle|lamp)light falls from out of frame; no candle, flame, lantern or lamp in shot\.")
EVENING = {
    "19_gap_open": ("at a window at dusk", "at a window in late-afternoon daylight"),
    "03_old_harvey": ("soft evening window light", "soft warm afternoon window light"),
}
YOUNG_HARVEY = ("young William Harvey, about twenty-two, olive skin, black hair, first thin beard, "
                "dark keen eyes, dark student's gown")
YOUNG_HARVEY_FIX = ("young William Harvey, about twenty-two, the same face as the older Harvey: olive "
                    "skin, black hair to the collar, small pointed black beard, dark keen eyes, black "
                    "student's gown with a white collar")
HARVEY_ON_SCREEN = re.compile(r"(?:young |old )?William Harvey, (?:a short man|about)")
HARVEY_SHORT_NAME = {"02_linen_tie"}
NOTE = "2026-10-02 light fix (desk 5942662028): Fast plates in daylight, no candle sentence"


def main() -> None:
    for n in range(2, 6):
        f = PARTS / f"part-0{n}_plates_v02.json"
        b = json.loads(f.read_text())
        changed = []
        for p in b["plates"]:
            before = p.get("prompt_v02_before_light_fix", p["prompt"])
            pr = before
            if p["quality"] == "Fast":
                pr = CANDLE_RE.sub(DAYLIGHT, pr)
                if p["id"] in EVENING:
                    old, new = EVENING[p["id"]]
                    pr = pr.replace(old, new)
                    if DAYLIGHT not in pr:
                        pr = pr.replace(" Silent.", f" {DAYLIGHT} Silent.", 1)
            pr = pr.replace(YOUNG_HARVEY, YOUNG_HARVEY_FIX)
            p["harvey_ref"] = bool(HARVEY_ON_SCREEN.search(pr)) or p["id"] in HARVEY_SHORT_NAME
            if pr != before:
                p["prompt_v02_before_light_fix"] = before
                p["prompt"] = pr
                p["light_fix"] = NOTE
                changed.append(p["id"])
        assert not any(CANDLE_RE.search(p["prompt"]) for p in b["plates"] if p["quality"] == "Fast")
        b["light_fix"] = NOTE
        b["quality_note"] = (b["quality_note"].replace("Flow Veo 3.1 on the Mac Mini CDP worker, benoats@googlemail.com only.",
                                                       "Vertex AI Veo 3.1 for 005 (Ben's OK, 1 Oct 2026), project gen-lang-client-0538779324.")
                             + " Fast plates are lit by daylight from a window out of frame (2 Oct light fix).")
        f.write_text(json.dumps(b, indent=2, ensure_ascii=False) + "\n")
        hv = [p["id"] for p in b["plates"] if p["harvey_ref"]]
        print(f"part 0{n}: {len(changed)} prompts changed; harvey_ref {hv}")


if __name__ == "__main__":
    main()
