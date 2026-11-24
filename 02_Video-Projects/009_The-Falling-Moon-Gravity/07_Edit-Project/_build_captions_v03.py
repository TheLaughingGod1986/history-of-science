#!/usr/bin/env python3
"""HOS 009 en-GB captions for master v03.

Sentence text and film times come from 07_Edit-Project/VO_RETIME_v01.json.
Every part vo_start (0.00, 86.34, 178.68, 262.06, 395.76 s) and chapter-card
in-point (84.44, 176.78, 260.16, 393.86 s) matches 09_Assembly/j2035_v03/SOURCE_MAP.json
exact to 0.00 s, so the VO_RETIME_v01 film times map directly onto v03 (519.000 s).
No cue runs across a chapter-card in-point or past the master duration.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import textwrap
from pathlib import Path

PROJ = Path(__file__).resolve().parents[1]
RETIME = PROJ / "07_Edit-Project/VO_RETIME_v01.json"
MASTER = Path(
    "/Volumes/data/studio-live/History Of Science/02_Video-Projects/"
    "009_The-Falling-Moon-Gravity/09_Assembly/j2035_v03/hos009_long_master_v03.mp4"
)
OUT = PROJ / "11_Upload-Package/Captions/hos_009_master_v03.en.srt"
META = PROJ / "11_Upload-Package/Captions/hos_009_master_v03_captions_meta.json"
MASTER_SHA = "744f32b7f2f95e75fabf039a345aee6c7c01ab6f304a932ebe7172bd3b3ede55"
MASTER_DUR = 519.000
# Chapter-card in-points from SOURCE_MAP.json & VO_RETIME_v01.json (v03 timeline).
CARDS = [84.44, 176.78, 260.16, 393.86]
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
    ap = argparse.ArgumentParser()
    ap.add_argument("--skip-master-hash", action="store_true",
                    help="Skip re-hashing the 898 MB NAS master if already verified in this run.")
    ns = ap.parse_args()

    if not ns.skip_master_hash:
        h = hashlib.sha256()
        with MASTER.open("rb") as f:
            for b in iter(lambda: f.read(1 << 20), b""):
                h.update(b)
        assert h.hexdigest() == MASTER_SHA, f"master sha mismatch: {h.hexdigest()}"

    retime = json.loads(RETIME.read_text(encoding="utf-8"))
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
        "master": "09_Assembly/j2035_v03/hos009_long_master_v03.mp4",
        "master_sha256": MASTER_SHA,
        "master_duration_s": MASTER_DUR,
        "timing_note": "Part vo_start (0.00, 86.34, 178.68, 262.06, 395.76 s) and chapter cards (84.44, 176.78, 260.16, 393.86 s) match SOURCE_MAP.json v03 exact to 0.00 s.",
        "source_text": "01_Script/moon_script_master_v01.md via 07_Edit-Project/VO_RETIME_v01.json",
        "cues": len(fixed),
        "first": ts(fixed[0][0]),
        "last_end": ts(fixed[-1][1]),
        "chapter_cards_s": CARDS,
    }, indent=2) + "\n", encoding="utf-8")
    print(f"PASS  {OUT.name}  cues={len(fixed)}  {ts(fixed[0][0])} -> {ts(fixed[-1][1])}  sha256={srt_sha}")


if __name__ == "__main__":
    main()
