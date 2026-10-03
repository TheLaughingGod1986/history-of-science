#!/usr/bin/env python3
"""HOS 005 captions: script-locked SRT for master v02.

Sentence text and in-take times come from VO_RETIME_v02.json (the signed-off
script v02, timed on the VO v01 takes); each part's offset in the master comes
from full_join_v02_meta.json. Long sentences split into cues by character share.
No cue spans a chapter card coming in (each card fades out under the next
part's first word), and none runs into the end card or the end-screen hold.
"""
from __future__ import annotations

import hashlib
import json
import textwrap
from pathlib import Path

PROJ = Path(__file__).resolve().parents[1]
RETIME = PROJ / "07_Edit-Project/VO_RETIME_v02.json"
JOIN = PROJ / "07_Edit-Project/full_join_v02_meta.json"
MASTER = PROJ / "09_Final-Export/hos_005_master_v02.mp4"
OUT = PROJ / "11_Upload-Package/Captions/hos_005_master_v02.en.srt"
META = PROJ / "11_Upload-Package/Captions/hos_005_master_v02_captions_meta.json"
MASTER_SHA = json.loads(JOIN.read_text())["sha256"]
MAX_CHARS = 42
MAX_LINES = 2
MIN_CUE_S = 1.0


def ts(s: float) -> str:
    ms = int(round(s * 1000))
    h, ms = divmod(ms, 3_600_000)
    m, ms = divmod(ms, 60_000)
    sec, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{sec:02d},{ms:03d}"


def chunks(text: str) -> list[str]:
    lines = textwrap.wrap(text, MAX_CHARS)
    return [" ".join(lines[i:i + MAX_LINES]) for i in range(0, len(lines), MAX_LINES)]


def main() -> None:
    h = hashlib.sha256()
    with MASTER.open("rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    assert h.hexdigest() == MASTER_SHA, "master sha mismatch"

    retime = json.loads(RETIME.read_text())
    join = json.loads(JOIN.read_text())
    offsets = {int(p["part"]): p["film_start_s"] for p in join["parts"]}
    end_card_in = join["end_card"]["in_s"]

    cues: list[tuple[float, float, str]] = []
    for part in retime["parts"]:
        off = offsets[part["part"]]
        for s in part["sentences"]:
            a, b = off + s["start_s"], off + s["end_s"]
            pieces = chunks(s["text"])
            total = sum(len(p) for p in pieces)
            t = a
            for p in pieces:
                d = (b - a) * len(p) / total
                cues.append((t, t + d, p))
                t += d

    fixed: list[tuple[float, float, str]] = []
    for i, (a, b, text) in enumerate(cues):
        nxt = cues[i + 1][0] if i + 1 < len(cues) else end_card_in
        b = min(max(b, a + MIN_CUE_S), nxt - 0.02, end_card_in)
        fixed.append((a, b, text))

    for c in join["cards"]:
        for a, b, _ in fixed:
            assert not (a <= c["in_s"] < b), f"cue over card {c['part']}"

    lines = []
    for i, (a, b, text) in enumerate(fixed, 1):
        wrapped = "\n".join(textwrap.wrap(text, MAX_CHARS))
        lines.append(f"{i}\n{ts(a)} --> {ts(b)}\n{wrapped}\n")
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(lines), encoding="utf-8")

    srt_sha = hashlib.sha256(OUT.read_bytes()).hexdigest()
    META.write_text(json.dumps({
        "srt": OUT.name,
        "sha256": srt_sha,
        "master": MASTER.name,
        "master_sha256": MASTER_SHA,
        "source_text": "01_Script/blood_script_master_v03.md via 07_Edit-Project/VO_RETIME_v02.json",
        "cues": len(fixed),
        "first": ts(fixed[0][0]),
        "last_end": ts(fixed[-1][1]),
        "end_card_in": ts(end_card_in),
    }, indent=2) + "\n")
    print(f"PASS  {OUT.name}  cues={len(fixed)}  {ts(fixed[0][0])} → {ts(fixed[-1][1])}  sha256={srt_sha}")


if __name__ == "__main__":
    main()
