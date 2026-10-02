#!/usr/bin/env python3
"""HOS 005 Shorts VO v01 — Ben Orbit Narrator, settings_for_part(1) (speed 1.04). Never prints the API key.

Text = the "**Script (N words):**" paragraph of each Short in SHORTS_SCRIPTS_v01.md (signed off by Ben,
1 Oct 2026), word for word. Writes vo_v01/sNN_<slug>.txt (the vo_check script), .mp3, .wav, _align.json
and VO_SHORTS_v01.json.

  python3 _generate_shorts_vo_v01.py [--only s01 s02] [--take b]
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

SCRIPTS = HERE / "SHORTS_SCRIPTS_v01.md"
OUT = HERE / "vo_v01"
GERMS_ENV = Path("/Users/benjaminoats/YouTube/History Of Science/02_Video-Projects/"
                 "001_How-Did-We-Discover-Germs/07_Edit-Project/.env")
SHORTS = [("s01", "the_sum", "Short A"), ("s02", "the_tied_arm", "Short B"), ("s03", "never_saw", "Short C")]


def script_text(label: str) -> str:
    md = SCRIPTS.read_text(encoding="utf-8")
    sec = re.split(r"^## ", md, flags=re.M)
    body = next(s for s in sec if s.startswith(label))
    m = re.search(r"\*\*Script \((\d+) words\):\*\*\s*\n\s*\n(.+?)\n\s*\n", body, flags=re.S)
    if not m:
        raise SystemExit(f"no Script paragraph in {label}")
    text = " ".join(m.group(2).split())
    n = len(text.split())
    if n != int(m.group(1)):
        raise SystemExit(f"{label}: {n} words, script says {m.group(1)}")
    return text


def sha256(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def loud(p: Path) -> tuple[float, float]:
    err = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(p), "-af", "volumedetect", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    return (float(re.search(r"mean_volume: (-?[\d.]+)", err).group(1)),
            float(re.search(r"max_volume: (-?[\d.]+)", err).group(1)))


def dur(p: Path) -> float:
    return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                          "-of", "csv=p=0", str(p)], text=True))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", nargs="*")
    ap.add_argument("--take", default="a")
    ns = ap.parse_args()
    if GERMS_ENV.exists():
        load_dotenv(GERMS_ENV)
    token, mode = load_token(prefer_api_key=True)
    vs = settings_for_part(1)
    print(f"auth={mode} voice={VOICE_ID} model={MODEL_ID} speed={vs['speed']}", flush=True)
    OUT.mkdir(parents=True, exist_ok=True)
    meta_p = OUT / "VO_SHORTS_v01.json"
    meta = json.loads(meta_p.read_text()) if meta_p.exists() else {
        "film": PROJ.name, "scripts": SCRIPTS.name, "voice": "Ben Orbit Narrator", "voice_id": VOICE_ID,
        "model_id": MODEL_ID, "voice_settings": vs, "takes": []}
    for sid, slug, label in SHORTS:
        if ns.only and sid not in ns.only:
            continue
        text = script_text(label)
        txt = OUT / f"{sid}_{slug}.txt"
        txt.write_text(text + "\n", encoding="utf-8")
        stem = f"hos_005_{sid}_{slug}_vo_v01{ns.take}"
        mp3, wav, align = OUT / f"{stem}.mp3", OUT / f"{stem}.wav", OUT / f"{stem}_align.json"
        code, body, _ = request("POST", f"/v1/text-to-speech/{VOICE_ID}/with-timestamps", token, mode,
                                data={"text": text, "model_id": MODEL_ID, "voice_settings": vs},
                                query="output_format=mp3_44100_128", accept="application/json", timeout=300)
        if code != 200:
            raise SystemExit(f"TTS failed {sid} {code}: {body[:300]!r}")
        payload = json.loads(body.decode())
        mp3.write_bytes(base64.b64decode(payload["audio_base64"]))
        align.write_text(json.dumps(payload.get("alignment") or payload.get("normalized_alignment") or {}, indent=1))
        subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", str(mp3),
                        "-c:a", "pcm_s16le", "-ar", "48000", "-ac", "2", str(wav)], check=True)
        mean, peak = loud(wav)
        rec = {"id": sid, "take": ns.take, "txt": txt.name, "words": len(text.split()), "mp3": mp3.name,
               "mp3_sha256": sha256(mp3), "wav": wav.name, "align": align.name, "duration_s": round(dur(wav), 3),
               "mean_db": mean, "peak_db": peak}
        meta["takes"].append(rec)
        print(f"SAVED {stem} {rec['duration_s']}s mean {mean} peak {peak}", flush=True)
    meta_p.write_text(json.dumps(meta, indent=2) + "\n")


if __name__ == "__main__":
    main()
