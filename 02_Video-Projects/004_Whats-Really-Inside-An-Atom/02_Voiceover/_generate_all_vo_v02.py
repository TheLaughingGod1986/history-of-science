#!/usr/bin/env python3
"""HOS 004 VO v02 — faster speeds. Ben Orbit Narrator only. Do not print the API key.

Does NOT edit shared VOICE_SETTINGS. Per-call speed overrides:
  Part 01: 1.15 · Parts 02–05: 1.12
Keeps v01 masters untouched.
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
MASTER = HERE / "05_Master"
GERMS_ENV = Path(
    "/Users/benjaminoats/YouTube/History Of Science/"
    "02_Video-Projects/001_How-Did-We-Discover-Germs/07_Edit-Project/.env"
)
LOCAL_ENV = PROJ / "07_Edit-Project" / ".env"

# Locked spoken text (identical to v01). Speeds per Ben work order.
PARTS = [
    ("01", "cold_open", "part01_cold_open_v02.txt", 1.15),
    ("02", "the_table_that_broke_its_own_rule", "part02_the_table_that_broke_its_own_rule_v02.txt", 1.12),
    ("03", "the_crumb_inside_the_atom", "part03_the_crumb_inside_the_atom_v02.txt", 1.12),
    ("04", "the_shell_that_bounced_back", "part04_the_shell_that_bounced_back_v02.txt", 1.12),
    ("05", "counting_with_x_rays", "part05_counting_with_x_rays_v02.txt", 1.12),
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


def mean_db(path: Path) -> float | None:
    proc = subprocess.run(
        [
            "ffmpeg", "-hide_banner", "-i", str(path),
            "-af", "volumedetect", "-f", "null", "-",
        ],
        capture_output=True,
        text=True,
    )
    mean = None
    peak = None
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
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def settings_for_speed(speed: float) -> dict:
    s = dict(VOICE_SETTINGS)
    s["speed"] = speed
    return s


def gen_one(num: str, slug: str, txt_name: str, speed: float, token: str, mode: str) -> dict:
    txt = HERE / txt_name
    stem = f"hos_004_part{num}_vo_v02"
    mp3 = MASTER / f"{stem}.mp3"
    wav = MASTER / f"{stem}.wav"
    align = MASTER / f"{stem}_align.json"
    if not txt.exists():
        raise SystemExit(f"STOP: missing {txt}")
    # Never overwrite v01
    for legacy in (MASTER / f"hos_004_part{num}_vo_v01.mp3", MASTER / f"hos_004_part{num}_vo_v01.wav"):
        if not legacy.exists():
            print(f"WARN: v01 missing {legacy.name}", flush=True)
    text = txt.read_text(encoding="utf-8").strip()
    vs = settings_for_speed(speed)
    print(f"PART {num} speed={speed} chars={len(text)} words={len(text.split())}", flush=True)
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
        raise SystemExit(f"TTS failed part {num} {code}: {body[:400]!r}")
    payload = json.loads(body.decode())
    audio_b64 = payload.get("audio_base64") or payload.get("audio")
    if not audio_b64:
        raise SystemExit(f"TTS JSON missing audio_base64 part {num}")
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
        "part": num,
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
        f"SAVED part{num} dur={dur:.3f}s mean_db={mdb} peak_db={peak} "
        f"wav_sha={rec['wav_sha256'][:16]}…",
        flush=True,
    )
    return rec


def main() -> None:
    if LOCAL_ENV.exists():
        load_dotenv(LOCAL_ENV)
    if GERMS_ENV.exists():
        load_dotenv(GERMS_ENV)
    token, mode = load_token(prefer_api_key=True)
    print(f"auth={mode} voice={VOICE_ID} model={MODEL_ID}", flush=True)
    print(f"shared_VOICE_SETTINGS_speed={VOICE_SETTINGS['speed']} (untouched)", flush=True)
    records = []
    for num, slug, txt_name, speed in PARTS:
        records.append(gen_one(num, slug, txt_name, speed, token, mode))
    total = sum(r["duration_s"] for r in records)
    meta = {
        "film": "004_Whats-Really-Inside-An-Atom",
        "title": "Why Is the Periodic Table in This Order?",
        "version": "v02",
        "route": "elevenlabs_speed_override",
        "voice": "Ben Orbit Narrator",
        "voice_id": VOICE_ID,
        "total_duration_s": round(total, 3),
        "speeds": {"01": 1.15, "02_05": 1.12},
        "parts": records,
    }
    out = MASTER / "VO_MASTERS_v02.json"
    out.write_text(json.dumps(meta, indent=2) + "\n")
    mm, ss = divmod(int(total), 60)
    print(f"TOTAL {total:.3f}s ({mm}:{ss:02d}) meta={out}", flush=True)
    v01_total = 536.16
    ratio = v01_total / total if total else 0
    print(f"vs v01 {v01_total:.2f}s → ratio {ratio:.3f} (expect ~1.10–1.12)", flush=True)


if __name__ == "__main__":
    main()
