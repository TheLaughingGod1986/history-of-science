#!/usr/bin/env python3
"""HOS 005 VO v01 — Ben Orbit Narrator only, settings_for_part(n) (speed 1.04). Never prints the API key.

Spoken text is read from the signed-off script v02 with the same line filter as vo_check.py,
so the take is checked against exactly what was sent. Never overwrites an existing take.

  python3 _generate_all_vo_v01.py [--parts 1 2 3 4 5] [--version v01]
  python3 _generate_all_vo_v01.py --sentence "<exact sentence>" --out _qa_<what>_v01a.mp3 --part N
"""
from __future__ import annotations

import argparse
import base64
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
PROJ = HERE.parent
REPO = PROJ.parents[1]
sys.path.insert(0, str(REPO / "04_Audio" / "tools"))

from el_auth import load_token  # noqa: E402
from el_client import request  # noqa: E402
from orbit_gemini_veo import load_dotenv  # noqa: E402
from orbit_voice import MODEL_ID, VOICE_ID, settings_for_part  # noqa: E402

SCRIPT = PROJ / "01_Script" / "blood_script_master_v02.md"
GERMS_ENV = Path("/Users/benjaminoats/YouTube/History Of Science/02_Video-Projects/"
                 "001_How-Did-We-Discover-Germs/07_Edit-Project/.env")
SLUGS = {1: "the_used_up_blood", 2: "the_liver_that_made_blood", 3: "the_sum_that_broke_the_old_idea",
         4: "the_tied_arm", 5: "the_vessels_he_never_saw"}


def part_text(part: int) -> str:
    chunks = re.split(r"^## PART \d+.*$", SCRIPT.read_text(encoding="utf-8"), flags=re.M)
    lines = [l.strip() for l in chunks[part].splitlines() if l.strip() and not re.match(r"\s*(#|\[|<!--)", l)]
    return "\n\n".join(lines)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def tts(text: str, part: int, token: str, mode: str, out: Path) -> dict:
    if out.exists():
        raise SystemExit(f"STOP: {out.name} exists; versions only go up")
    vs = settings_for_part(part)
    code, body, _ = request("POST", f"/v1/text-to-speech/{VOICE_ID}/with-timestamps", token, mode,
                            data={"text": text, "model_id": MODEL_ID, "voice_settings": vs},
                            query="output_format=mp3_44100_128", accept="application/json", timeout=300)
    if code != 200:
        raise SystemExit(f"TTS failed part {part} {code}: {body[:300]!r}")
    payload = json.loads(body.decode())
    out.write_bytes(base64.b64decode(payload["audio_base64"]))
    out.with_name(out.stem + "_align.json").write_text(json.dumps(payload.get("alignment") or {}, indent=1))
    dur = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                         "-of", "csv=p=0", str(out)], text=True))
    rec = {"part": part, "file": str(out), "duration_s": round(dur, 3), "sha256": sha256(out),
           "chars": len(text), "words": len(text.split()), "voice_id": VOICE_ID, "model_id": MODEL_ID,
           "voice_settings": vs}
    print(f"SAVED {out.name} {dur:.2f}s sha256 {rec['sha256'][:16]}…", flush=True)
    return rec


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--parts", type=int, nargs="*", default=[1, 2, 3, 4, 5])
    ap.add_argument("--version", default="v01")
    ap.add_argument("--sentence")
    ap.add_argument("--part", type=int)
    ap.add_argument("--out")
    ns = ap.parse_args()
    if GERMS_ENV.exists():
        load_dotenv(GERMS_ENV)
    token, mode = load_token(prefer_api_key=True)
    print(f"auth={mode} voice={VOICE_ID} model={MODEL_ID}", flush=True)
    if ns.sentence:
        if ns.sentence not in part_text(ns.part):
            raise SystemExit("STOP: sentence is not word-for-word in that part of the script")
        tts(ns.sentence, ns.part, token, mode, HERE / ns.out)
        return
    recs = []
    for p in ns.parts:
        text = part_text(p)
        (HERE / f"part{p:02d}_{SLUGS[p]}_{ns.version}.txt").write_text(text + "\n", encoding="utf-8")
        recs.append(tts(text, p, token, mode, HERE / f"part{p:02d}_{SLUGS[p]}_{ns.version}.mp3"))
    meta = HERE / f"VO_TAKES_{ns.version}.json"
    old = json.loads(meta.read_text()) if meta.exists() else []
    meta.write_text(json.dumps(old + recs, indent=2) + "\n")


if __name__ == "__main__":
    main()
