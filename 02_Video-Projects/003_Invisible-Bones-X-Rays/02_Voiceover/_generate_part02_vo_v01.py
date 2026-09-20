#!/usr/bin/env python3
"""HOS 003 Part 02 VO draft — Ben Orbit Narrator. Do not print the API key."""
from __future__ import annotations

import base64
import hashlib
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
TXT = HERE / "part02_the_cardboard_v02.txt"
VO_TXT_SHA = "f3454130086c42ea5545b2e149f193fe8d03ea2f0b7843155e48784ccb206975"
MP3 = HERE / "05_Master" / "hos_003_part02_vo_v01_draft.mp3"
WAV = HERE / "05_Master" / "hos_003_part02_vo_v01_draft.wav"
ALIGN = HERE / "05_Master" / "hos_003_part02_vo_v01_draft_align.json"


def probe_dur(path: Path) -> float:
    out = subprocess.check_output(
        [
            "ffprobe", "-v", "error", "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1", str(path),
        ],
        text=True,
    ).strip()
    return float(out)


def main() -> None:
    MP3.parent.mkdir(parents=True, exist_ok=True)
    load_dotenv(PROJ / "07_Edit-Project" / ".env")
    if GERMS_ENV.exists():
        load_dotenv(GERMS_ENV)
    if TXT.name != "part02_the_cardboard_v02.txt":
        raise SystemExit("STOP: VO lock is part02_the_cardboard_v02.txt — do not use v01")
    got = hashlib.sha256(TXT.read_bytes()).hexdigest()
    if got != VO_TXT_SHA:
        raise SystemExit(f"STOP: VO txt sha {got} != locked {VO_TXT_SHA}")
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
    print(f"SAVED {MP3.name} bytes={MP3.stat().st_size} dur={probe_dur(MP3):.3f}s", flush=True)
    print(f"SAVED {WAV.name} bytes={WAV.stat().st_size} dur={probe_dur(WAV):.3f}s", flush=True)
    print(f"ALIGN {ALIGN.name} keys={sorted(align.keys())}", flush=True)


if __name__ == "__main__":
    main()
