#!/usr/bin/env python3
"""HOS 007 en-GB captions for master v04.

Sentence text and film times come from VO_RETIME_v01.json. v04's PCM matches
master v03 (md5 d76ce95dd28e8d8cf1d6c9235d1cad51), and only three picture
windows changed, so those film times carry. No cue runs across a chapter-card
in-point. The closing hand-off may sit on the end card; none runs past the master.
"""
from __future__ import annotations

import hashlib
import json
import textwrap
from pathlib import Path

PROJ = Path(__file__).resolve().parents[1]
RETIME = PROJ / "07_Edit-Project/VO_RETIME_v01.json"
MASTER = Path(
    "/Volumes/data/mac-mini-archive/hos-007-vaccine/master_v04_J0925/hos_007_master_v04.mp4"
)
OUT = PROJ / "11_Upload-Package/Captions/hos_007_master_v04.en.srt"
META = PROJ / "11_Upload-Package/Captions/hos_007_master_v04_captions_meta.json"
MASTER_SHA = "c7f62adbb241bf3fbfaa3a17929f05768eedcf89044cb2cc5ebd2971c163e810"
MASTER_DUR = 531.083
# Chapter-card in-points from VO_RETIME_v01, which land on the v04 timeline.
CARDS = [100.83, 232.37, 313.03, 407.69]
MAX_CHARS = 42
MAX_LINES = 2
MIN_CUE_S = 0.8


def ts(s: float) -> str:
    ms = int(round(max(0.0, s) * 1000))
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
    windows: list[list] = []
    for part in retime["parts"]:
        for s in part["sentences"]:
            a = float(s["film_s"])
            b = a + (float(s["end_s"]) - float(s["start_s"]))
            windows.append([a, b, s["text"]])
    for i, w in enumerate(windows[:-1]):
        if w[1] - w[0] >= 0.15:
            continue
        nxt = windows[i + 1]
        if abs(nxt[0] - w[0]) > 0.05:
            continue
        span = nxt[1] - nxt[0]
        take = min(1.6, max(1.0, span * 0.2))
        w[1] = w[0] + take
        nxt[0] = w[1] + 0.04

    cues: list[tuple[float, float, str]] = []
    for a, b, text in windows:
        pieces = chunks(text)
        total = sum(len(p) for p in pieces) or 1
        t = a
        for p in pieces:
            d = (b - a) * len(p) / total
            cues.append((t, t + d, p))
            t += d

    fixed: list[tuple[float, float, str]] = []
    for i, (a, b, text) in enumerate(cues):
        nxt = cues[i + 1][0] if i + 1 < len(cues) else MASTER_DUR
        stop = min(nxt - 0.04, MASTER_DUR - 0.05)
        for c in CARDS:
            if a < c < stop:
                stop = min(stop, c - 0.04)
        if stop - a >= MIN_CUE_S and b - a < MIN_CUE_S:
            b = a + MIN_CUE_S
        b = min(b, stop)
        if b <= a + 0.05:
            raise SystemExit(f"cue collapsed: {text!r} at {a:.2f} stop={stop:.2f}")
        for c in CARDS:
            if a < c < b:
                raise SystemExit(f"cue still over chapter card {c}: {text!r}")
        fixed.append((a, b, text))

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
        "language": "en-GB",
        "master": str(MASTER),
        "master_sha256": MASTER_SHA,
        "audio_pcm_md5": "d76ce95dd28e8d8cf1d6c9235d1cad51",
        "audio_note": "v04 PCM md5 matches master v03, so VO_RETIME_v01 film times carry",
        "source_text": "01_Script via 07_Edit-Project/VO_RETIME_v01.json",
        "cues": len(fixed),
        "first": ts(fixed[0][0]),
        "last_end": ts(fixed[-1][1]),
        "chapter_cards_s": CARDS,
    }, indent=2) + "\n")
    print(f"PASS  {OUT.name}  cues={len(fixed)}  {ts(fixed[0][0])} → {ts(fixed[-1][1])}  sha256={srt_sha}")


if __name__ == "__main__":
    main()
