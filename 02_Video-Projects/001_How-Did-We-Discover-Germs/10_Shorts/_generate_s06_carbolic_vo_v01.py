#!/usr/bin/env python3
"""HOS 001 S06 Lister carbolic spray Short VO — Ben Orbit Narrator @ 1.04."""
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
MASTER = HERE / "vo_s06"
GERMS_ENV = HERE.parent / "07_Edit-Project" / ".env"
CONTENT_OPS_ENV = REPO / "07_Content-Ops" / ".env"
TXT = MASTER / "s06_carbolic_spray.txt"
STEM = "hos_001_s06_carbolic_spray_vo_v01"


def probe_dur(path: Path) -> float:
    out = subprocess.check_output(
        [
            "ffprobe", "-v", "error", "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1", str(path),
        ],
        text=True,
    ).strip()
    return float(out)


def mean_db(path: Path) -> tuple[float | None, float | None]:
    proc = subprocess.run(
        ["ffmpeg", "-hide_banner", "-i", str(path), "-af", "volumedetect", "-f", "null", "-"],
        capture_output=True,
        text=True,
    )
    mean = peak = None
    for line in (proc.stderr or "").splitlines():
        if "mean_volume:" in line:
            try:
                mean = float(line.split("mean_volume:")[1].split("dB")[0].strip())
            except ValueError:
                pass
        if "max_volume:" in line:
            try:
                peak = float(line.split("max_volume:")[1].split("dB")[0].strip())
            except ValueError:
                pass
    return mean, peak


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> int:
    for env in (GERMS_ENV, CONTENT_OPS_ENV):
        if env.exists():
            load_dotenv(env)
    token, mode = load_token(prefer_api_key=True)
    text = TXT.read_text(encoding="utf-8").strip()
    words = len(text.split())
    vs = dict(VOICE_SETTINGS)
    vs["speed"] = 1.04
    print(f"auth={mode} words={words} speed=1.04", flush=True)
    code, body, _ = request(
        "POST",
        f"/v1/text-to-speech/{VOICE_ID}/with-timestamps",
        token,
        mode,
        data={"text": text, "model_id": MODEL_ID, "voice_settings": vs},
        query="output_format=mp3_44100_128",
        accept="application/json",
        timeout=300,
    )
    if code != 200:
        raise SystemExit(f"TTS failed {code}: {body[:400]!r}")
    payload = json.loads(body.decode())
    audio_b64 = payload.get("audio_base64") or payload.get("audio")
    if not audio_b64:
        raise SystemExit("TTS missing audio_base64")
    MASTER.mkdir(parents=True, exist_ok=True)
    mp3 = MASTER / f"{STEM}.mp3"
    wav = MASTER / f"{STEM}.wav"
    align = MASTER / f"{STEM}_align.json"
    mp3.write_bytes(base64.b64decode(audio_b64))
    align.write_text(
        json.dumps(
            payload.get("alignment") or payload.get("normalized_alignment") or {},
            indent=2,
        )
        + "\n"
    )
    subprocess.run(
        [
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            "-i", str(mp3), "-c:a", "pcm_s16le", "-ar", "48000", "-ac", "2", str(wav),
        ],
        check=True,
    )
    dur = probe_dur(wav)
    mdb, peak = mean_db(wav)
    rec = {
        "id": "s06",
        "slug": "carbolic_spray",
        "words": words,
        "duration_s": round(dur, 3),
        "mean_db": mdb,
        "peak_db": peak,
        "mp3": str(mp3),
        "wav": str(wav),
        "align": str(align),
        "wav_sha256": sha256_file(wav),
        "speed": 1.04,
        "voice_id": VOICE_ID,
        "model_id": MODEL_ID,
        "under_22s": dur < 22.0,
        "added_line": "Antiseptic surgery began there.",
    }
    (MASTER / "VO_S06_v01.json").write_text(json.dumps(rec, indent=2) + "\n")
    print(
        f"SAVED dur={dur:.3f}s mean={mdb} peak={peak} under_22={dur < 22}",
        flush=True,
    )
    if dur < 22.0:
        print("WARN under 22s — Ben asked to add a short line; already added one. Re-gen if still short.", flush=True)
    if dur > 27.0:
        print("WARN over 27s", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
