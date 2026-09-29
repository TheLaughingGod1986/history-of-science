#!/usr/bin/env python3
"""HOS 004 Shorts VO v03 — Ben Orbit Narrator at 1.04. Do not print the API key.

Speaks SHORTS_PUNCH_SCRIPTS_v03.md (Ben PASS edits). HOS channel only.
"""
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
MASTER = HERE / "vo_v03"
GERMS_ENV = Path(
    "/Users/benjaminoats/YouTube/History Of Science/"
    "02_Video-Projects/001_How-Did-We-Discover-Germs/07_Edit-Project/.env"
)
LOCAL_ENV = PROJ / "07_Edit-Project" / ".env"
CONTENT_OPS_ENV = REPO / "07_Content-Ops" / ".env"

SHORTS = [
    ("s01", "how_small", "s01_how_small.txt", 1.04),
    ("s02", "every_eighth", "s02_every_eighth.txt", 1.04),
    ("s03", "her_ring", "s03_her_ring.txt", 1.04),
]


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
        [
            "ffmpeg", "-hide_banner", "-i", str(path),
            "-af", "volumedetect", "-f", "null", "-",
        ],
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


def settings_for_speed(speed: float) -> dict:
    s = dict(VOICE_SETTINGS)
    s["speed"] = speed
    return s


def gen_one(sid: str, slug: str, txt_name: str, speed: float, token: str, mode: str) -> dict:
    txt = MASTER / txt_name
    stem = f"hos_004_{sid}_{slug}_vo_v03"
    mp3 = MASTER / f"{stem}.mp3"
    wav = MASTER / f"{stem}.wav"
    align = MASTER / f"{stem}_align.json"
    if not txt.exists():
        raise SystemExit(f"STOP: missing {txt}")
    text = txt.read_text(encoding="utf-8").strip()
    vs = settings_for_speed(speed)
    print(f"{sid} speed={speed} chars={len(text)} words={len(text.split())}", flush=True)
    code, body, _hdrs = request(
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
        raise SystemExit(f"TTS failed {sid} {code}: {body[:400]!r}")
    payload = json.loads(body.decode())
    audio_b64 = payload.get("audio_base64") or payload.get("audio")
    if not audio_b64:
        raise SystemExit(f"TTS JSON missing audio_base64 {sid}")
    MASTER.mkdir(parents=True, exist_ok=True)
    mp3.write_bytes(base64.b64decode(audio_b64))
    align_payload = payload.get("alignment") or payload.get("normalized_alignment") or {}
    align.write_text(json.dumps(align_payload, indent=2))
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
        "id": sid,
        "slug": slug,
        "txt": str(txt.relative_to(PROJ)),
        "txt_sha256": sha256_file(txt),
        "speed": speed,
        "mp3": str(mp3),
        "wav": str(wav),
        "align": str(align),
        "mp3_sha256": sha256_file(mp3),
        "wav_sha256": sha256_file(wav),
        "duration_s": round(dur, 3),
        "mean_db": mdb,
        "peak_db": peak,
        "voice_id": VOICE_ID,
        "model_id": MODEL_ID,
        "voice_settings": vs,
    }
    print(
        f"SAVED {sid} dur={dur:.3f}s mean_db={mdb} peak_db={peak} "
        f"wav_sha={rec['wav_sha256'][:16]}…",
        flush=True,
    )
    return rec


def main() -> None:
    for env in (LOCAL_ENV, GERMS_ENV, CONTENT_OPS_ENV):
        if env.exists():
            load_dotenv(env)
    # Prefer ~/.config/elevenlabs/api_key via el_auth — never Orbit .env
    token, mode = load_token(prefer_api_key=True)
    print(f"auth={mode} voice={VOICE_ID} model={MODEL_ID} speed=1.04", flush=True)
    records = []
    for sid, slug, txt_name, speed in SHORTS:
        records.append(gen_one(sid, slug, txt_name, speed, token, mode))
    meta = {
        "film": "004_Whats-Really-Inside-An-Atom",
        "scripts": "SHORTS_PUNCH_SCRIPTS_v03.md",
        "version": "v03",
        "voice": "Ben Orbit Narrator",
        "voice_id": VOICE_ID,
        "speed": 1.04,
        "shorts": records,
    }
    out = MASTER / "VO_SHORTS_v03.json"
    out.write_text(json.dumps(meta, indent=2) + "\n")
    print(f"meta={out}", flush=True)


if __name__ == "__main__":
    main()
