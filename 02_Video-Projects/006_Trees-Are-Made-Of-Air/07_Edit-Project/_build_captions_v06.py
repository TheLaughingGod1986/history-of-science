#!/usr/bin/env python3
"""HOS 006 captions for master v06.

Sentence text and film times come from VO_RETIME_v02.json (script v02, timed
on the VO v02 takes). v06's audio is the same PCM as v05, so those film times
carry. Long sentences split into cues by character share. No cue runs across
a chapter-card in-point. The closing hand-off is spoken over the end card, so
cues may sit on that card; none runs past the master.
"""
from __future__ import annotations

import hashlib
import json
import textwrap
from pathlib import Path

PROJ = Path(__file__).resolve().parents[1]
RETIME = PROJ / "07_Edit-Project/VO_RETIME_v02.json"
LAY = PROJ / "07_Edit-Project/master_v06/LAY_TIMES_v06.json"
MASTER = PROJ / "07_Edit-Project/master_v06/hos_006_master_v06.mp4"
OUT = PROJ / "11_Upload-Package/Captions/hos_006_master_v06.en.srt"
META = PROJ / "11_Upload-Package/Captions/hos_006_master_v06_captions_meta.json"
MASTER_SHA = "36c54e684b8a947c65298231268f9f031899df5a0d72ec38506f5e17b3d215ef"
MASTER_DUR = 531.833
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
    lay = json.loads(LAY.read_text())
    cards = sorted(
        r["start"] for r in lay["rows"] if r.get("kind") == "chapter"
    )

    windows: list[list] = []
    for part in retime["parts"]:
        for s in part["sentences"]:
            a = float(s["film_s"])
            b = a + (float(s["end_s"]) - float(s["start_s"]))
            windows.append([a, b, s["text"]])
    # A date line whisper timed at 0 s shares its start with the next sentence.
    # Give it the opening of that sentence; the words are spoken there.
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
        for c in cards:
            if a < c < stop:
                stop = min(stop, c - 0.04)
        if stop - a >= MIN_CUE_S and b - a < MIN_CUE_S:
            b = a + MIN_CUE_S
        b = min(b, stop)
        if b <= a + 0.05:
            raise SystemExit(f"cue collapsed: {text!r} at {a:.2f} stop={stop:.2f}")
        for c in cards:
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
        "master": str(MASTER.relative_to(PROJ)),
        "master_sha256": MASTER_SHA,
        "audio_pcm_md5": "f4f95e7101065bfab0158b71d7669f22",
        "audio_note": "v06 PCM md5 matches master v05, so VO_RETIME_v02 film times carry",
        "source_text": "01_Script via 07_Edit-Project/VO_RETIME_v02.json",
        "cues": len(fixed),
        "first": ts(fixed[0][0]),
        "last_end": ts(fixed[-1][1]),
        "chapter_cards_s": cards,
    }, indent=2) + "\n")
    print(f"PASS  {OUT.name}  cues={len(fixed)}  {ts(fixed[0][0])} → {ts(fixed[-1][1])}  sha256={srt_sha}")


if __name__ == "__main__":
    main()
