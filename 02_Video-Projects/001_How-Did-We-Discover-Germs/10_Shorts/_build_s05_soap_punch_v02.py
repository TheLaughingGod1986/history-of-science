#!/usr/bin/env python3
"""s05 soap punch v02 only. UAT FAIL fix. Do not remint. Do not touch s01–s04 or the long.

Picture: SOAP basin CU only (no hands, no orbs).
Burned punch + on-screen hold: “What else is still invisible?”
Spoken soap line may remain. CTA only on last ~4s loop.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
VENV_DIR = HERE / "_venv"
VENV_PY = VENV_DIR / "bin" / "python"
if VENV_DIR.exists() and Path(sys.prefix) != VENV_DIR:
    os.execv(str(VENV_PY), [str(VENV_PY), *sys.argv])

import importlib.util

spec = importlib.util.spec_from_file_location(
    "punch_v01", HERE / "_build_germs_punch_shorts_v01.py"
)
mod = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(mod)

# Basin CU in v02: 343.20–350.00. Theatre after ~350.3 — do not use.
PIC_START = 343.20
PIC_END = 350.00
# Audio through last question (“what else is still invisible to us?”)
AUD_START = 343.20
AUD_END = 359.325
HOLD_Q = 3.6
LOOP = 4.0

ITEM = {
    "id": "s05_soap",
    "slot": "Tue 8 Sep 2026 11:30 Europe/London",
    "title": "What else is still invisible?",
    "line": "What else is still invisible?",
    "spoken_may": "Every time soap meets your hands.",
}
OUT_NAME = "hos_001_s05_soap_punch_v02.mp4"
PASS_FILES = (
    "hos_001_s01_shadow_punch_v01.mp4",
    "hos_001_s02_pond_punch_v01.mp4",
    "hos_001_s03_vector_punch_v01.mp4",
    "hos_001_s04_flask_punch_v01.mp4",
)


def main() -> None:
    if mod.sha256(mod.SRC) != mod.SHA:
        raise SystemExit("v02 long sha mismatch — abort, do not remint")
    for name in PASS_FILES:
        if not (HERE / name).exists():
            raise SystemExit(f"PASS file missing, abort: {name}")

    work = HERE / "_work" / "s05_soap_v02"
    work.mkdir(parents=True, exist_ok=True)

    pic_dur = PIC_END - PIC_START
    aud_dur = AUD_END - AUD_START
    if aud_dur < pic_dur:
        raise SystemExit("audio window shorter than basin motion")
    hold_under_vo = aud_dur - pic_dur
    total = aud_dur + HOLD_Q + LOOP
    if total < 22.0:
        extra = 22.0 - total
        hold_q = HOLD_Q + extra
        total = aud_dur + hold_q + LOOP
    else:
        hold_q = HOLD_Q
    if total > 27.0:
        raise SystemExit(f"s05 v02 duration {total:.2f} out of 22–27")

    motion = work / "basin_motion.mp4"
    mod.encode_916(mod.SRC, motion, PIC_START, pic_dur, silent=True)

    # Full VO (soap line spoken → last question) under basin picture + hold
    vo = work / "vo.wav"
    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-hide_banner",
            "-loglevel",
            "error",
            "-ss",
            f"{AUD_START:.3f}",
            "-t",
            f"{aud_dur:.3f}",
            "-i",
            str(mod.SRC),
            "-vn",
            "-ac",
            "2",
            "-ar",
            "48000",
            str(vo),
        ],
        check=True,
    )

    hold_vo = work / "hold_vo.mp4"
    mod.freeze_hold(motion, hold_vo, hold_under_vo)

    story = work / "story.mp4"
    concat1 = work / "story_concat.txt"
    concat1.write_text(f"file '{motion.name}'\nfile '{hold_vo.name}'\n")
    pic_only = work / "story_pic.mp4"
    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-hide_banner",
            "-loglevel",
            "error",
            "-f",
            "concat",
            "-safe",
            "0",
            "-i",
            str(concat1),
            "-c",
            "copy",
            str(pic_only),
        ],
        check=True,
        cwd=work,
    )
    mod.ff(
        "-i",
        str(pic_only),
        "-i",
        str(vo),
        "-c:v",
        "copy",
        "-c:a",
        "aac",
        "-b:a",
        "192k",
        "-shortest",
        str(story),
    )

    hold_q_mp4 = work / "hold_q.mp4"
    mod.freeze_hold(motion, hold_q_mp4, hold_q)
    loop_mp4 = work / "loop.mp4"
    mod.loop_open(motion, loop_mp4, LOOP)

    concat2 = work / "concat.txt"
    concat2.write_text(
        f"file '{story.name}'\nfile '{hold_q_mp4.name}'\nfile '{loop_mp4.name}'\n"
    )
    raw = work / "raw.mp4"
    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-hide_banner",
            "-loglevel",
            "error",
            "-f",
            "concat",
            "-safe",
            "0",
            "-i",
            str(concat2),
            "-c",
            "copy",
            str(raw),
        ],
        check=True,
        cwd=work,
    )

    out = HERE / OUT_NAME
    raw_dur = mod.probe(raw)
    if raw_dur < 22.0 or raw_dur >= 28.0:
        raise SystemExit(f"s05 v02 raw {raw_dur:.2f}s — abort")
    mod.overlay_captions(ITEM, raw, raw_dur, out)
    dur = mod.probe(out)
    if dur < 22.0 or dur >= 28.0:
        raise SystemExit(f"s05 v02 exported {dur:.2f}s — abort")

    dest = mod.ICLOUD / OUT_NAME
    dest.write_bytes(out.read_bytes())

    index_path = HERE / "SHORTS_PUNCH_INDEX_v01.json"
    index = json.loads(index_path.read_text())
    index["note"] = (
        "s01–s04 PASS. s05 v02 STOP for UAT. Not LOCKED. Do not upload. "
        "Related = _C92tIJCk8A only. Zero /go/. Do not remint. Do not touch the long."
    )
    for it in index["items"]:
        if it["id"] in ("s01_shadow", "s02_pond", "s03_vector", "s04_flask"):
            it["status"] = "PASS"
            it["locked"] = False
        if it["id"] == "s05_soap":
            it["line"] = "What else is still invisible?"
            it["spoken_may"] = ITEM["spoken_may"]
            it["start"] = PIC_START
            it["end"] = PIC_END
            it["audio_end"] = AUD_END
            it["hold"] = hold_q
            it["file"] = OUT_NAME
            it["duration"] = dur
            it["status"] = "UAT"
            it["locked"] = False
            it["uat"] = (
                "v01 FAIL — last question not held. "
                "v02 burns and holds What else is still invisible? on SOAP basin. "
                "CTA last ~4s loop only."
            )
    index_path.write_text(json.dumps(index, indent=2) + "\n")
    (mod.ICLOUD / index_path.name).write_text(index_path.read_text())
    print(f"OK s05 v02 {dur:.2f}s → {OUT_NAME} (planned {total:.2f})", flush=True)


if __name__ == "__main__":
    main()
