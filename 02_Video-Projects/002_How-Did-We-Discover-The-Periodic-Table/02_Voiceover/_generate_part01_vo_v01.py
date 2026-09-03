#!/usr/bin/env python3
"""Part 01 VO — Zoo of Stuff. Ben Orbit Narrator only. Do not print the API key."""
from __future__ import annotations

import base64
import json
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO / "04_Audio" / "tools"))

from el_auth import load_token  # noqa: E402
from el_client import request  # noqa: E402
from orbit_gemini_veo import load_dotenv  # noqa: E402
from orbit_voice import MODEL_ID, VOICE_ID, VOICE_SETTINGS  # noqa: E402

HERE = Path(__file__).resolve().parent
PROJ = HERE.parent
GERMS_ENV = REPO / "02_Video-Projects/001_How-Did-We-Discover-Germs/07_Edit-Project/.env"
TXT = HERE / "part01_zoo_of_stuff_v02.txt"
MP3 = HERE / "part01_zoo_of_stuff_v02.mp3"
WAV = HERE / "part01_zoo_of_stuff_v02.wav"
ALIGN = HERE / "part01_zoo_of_stuff_v02_align.json"


def probe_dur(path: Path) -> float:
    out = subprocess.check_output(
        [
            "ffprobe", "-v", "error", "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1", str(path),
        ],
        text=True,
    ).strip()
    return float(out)


def phrase_time(align: dict, needle: str) -> float | None:
    chars = align.get("characters") or []
    starts = align.get("character_start_times_seconds") or []
    if not chars or not starts or len(chars) != len(starts):
        return None
    blob = "".join(chars).lower()
    idx = blob.find(needle.lower())
    if idx < 0:
        return None
    return float(starts[idx])


def main() -> None:
    load_dotenv(PROJ / "07_Edit-Project" / ".env")
    if GERMS_ENV.exists():
        load_dotenv(GERMS_ENV)
    text = TXT.read_text().strip()
    token, mode = load_token(prefer_api_key=True)
    print(f"auth={mode} voice={VOICE_ID} model={MODEL_ID} chars={len(text)}", flush=True)
    code, body, _hdrs = request(
        "POST",
        f"/v1/text-to-speech/{VOICE_ID}/with-timestamps",
        token,
        mode,
        data={"text": text, "model_id": MODEL_ID, "voice_settings": VOICE_SETTINGS},
        query="output_format=mp3_44100_128",
        accept="application/json",
        timeout=300,
    )
    if code != 200:
        raise SystemExit(f"TTS failed {code}: {body[:400]!r}")
    payload = json.loads(body.decode())
    audio_b64 = payload.get("audio_base64") or payload.get("audio")
    if not audio_b64:
        raise SystemExit("TTS JSON missing audio_base64")
    MP3.write_bytes(base64.b64decode(audio_b64))
    align = payload.get("alignment") or payload.get("normalized_alignment") or {}
    ALIGN.write_text(json.dumps(align, indent=2))
    subprocess.run(
        [
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            "-i", str(MP3), "-c:a", "pcm_s16le", "-ar", "48000", "-ac", "2", str(WAV),
        ],
        check=True,
    )
    d = probe_dur(MP3)
    print(f"SAVED {MP3} bytes={MP3.stat().st_size} dur={d:.3f}", flush=True)
    for label, needle in [
        ("SEATING PLAN", "secret seating plan"),
        ("PERIODIC TABLE", "periodic table"),
        ("FOUR INGREDIENTS", "four ingredients"),
        ("TRAP", "also a trap"),
        ("ALCHEMISTS", "alchemists"),
        ("ZOO", "zoo with labels"),
    ]:
        t = phrase_time(align, needle)
        print(f"WORD {label} t={t}", flush=True)


if __name__ == "__main__":
    main()
