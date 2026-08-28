#!/usr/bin/env python3
"""Generate Video 003 VO from exoplanets_narration_only_v01.txt via ElevenLabs.

Voice: Ben Orbit Narrator (IVC) kDch6ACCIpqgQ0NsU9kk — same locked settings as V002 v04.
Auth: Firebase Bearer from /tmp/elevenlabs_bearer.txt or Playwright profile IndexedDB.
"""
from __future__ import annotations

import base64
import json
import re
import subprocess
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(
    "/Users/ben/code/Orbit-YouTube/02_Video-Projects/"
    "003_Exoplanets-Strangest-Alien-Worlds"
)
NARR = ROOT / "01_Script/exoplanets_narration_only_v01.txt"
SEC_DIR = ROOT / "02_Voiceover/04_Section-Exports"
SEC_TXT = SEC_DIR / "_section_texts"
MASTER = ROOT / "02_Voiceover/05_Master"
VOICE_MODEL = ROOT / "02_Voiceover/02_Voice-Model"
REPORT = ROOT / "02_Voiceover/vo_generation_report_v01.json"

VOICE_ID = "kDch6ACCIpqgQ0NsU9kk"
MODEL = "eleven_v3"
VO_VERSION = "v01"
SETTINGS = {
    "stability": 0.34,
    "similarity_boost": 0.78,
    "style": 0.42,
    "speed": 1.04,
    "use_speaker_boost": True,
}

# Scene-aligned bundles matching script 01–11
SECTION_BREAKS = [
    ("01_hook-exoplanet", "Scenes 01–02 · hook + what is an exoplanet"),
    ("02_detection", "Scene 03 · how we find them"),
    ("03_diamond-glass", "Scenes 04–05 · diamond + glass rain"),
    ("04_suns-jupiter", "Scenes 06–07 · three suns + hot Jupiter"),
    ("05_eyeball-close", "Scenes 08–11 · eyeball + habitability + recap + CTA"),
]


def load_token() -> tuple[str, str]:
    for f in [
        Path("/tmp/elevenlabs_bearer.txt"),
        ROOT / "02_Voiceover/.elevenlabs_bearer",
        Path(
            "/Users/ben/code/Orbit-YouTube/02_Video-Projects/"
            "002_What-Happens-If-You-Fall-Into-A-Black-Hole/"
            "02_Voiceover/.elevenlabs_bearer"
        ),
    ]:
        if f.exists() and f.read_text().strip():
            tok = f.read_text().strip()
            try:
                payload = tok.split(".")[1]
                pad = "=" * (-len(payload) % 4)
                pl = json.loads(base64.urlsafe_b64decode(payload + pad))
                if pl.get("exp", 0) > time.time() + 30:
                    return tok, "bearer"
            except Exception:
                pass

    sources = [
        Path(
            "/Users/ben/code/youtube/.playwright-elevenlabs-profile/Default/IndexedDB/"
            "https_elevenlabs.io_0.indexeddb.leveldb"
        ),
        Path.home()
        / "Library/Application Support/Google/Chrome/Default/IndexedDB/"
        / "https_elevenlabs.io_0.indexeddb.leveldb",
    ]
    now = time.time()
    best = None
    for p in sources:
        if not p.exists():
            continue
        blob = b"".join(f.read_bytes() for f in p.glob("*") if f.is_file())
        for raw in set(
            re.findall(
                rb"eyJ[A-Za-z0-9_\-]{20,}\.[A-Za-z0-9_\-]{20,}\.[A-Za-z0-9_\-]{10,}",
                blob,
            )
        ):
            tok = raw.decode()
            try:
                payload = tok.split(".")[1]
                pad = "=" * (-len(payload) % 4)
                pl = json.loads(base64.urlsafe_b64decode(payload + pad))
            except Exception:
                continue
            exp = pl.get("exp", 0)
            if exp > now + 30 and (best is None or exp > best[0]):
                best = (exp, tok)
    if best:
        Path("/tmp/elevenlabs_bearer.txt").write_text(best[1] + "\n")
        return best[1], "bearer"
    raise SystemExit("No valid ElevenLabs bearer — refresh elevenlabs.io session")


def api(method, url, token, mode, data=None, accept="application/json"):
    headers = {"Accept": accept}
    if mode == "api_key":
        headers["xi-api-key"] = token
    else:
        headers["Authorization"] = f"Bearer {token}"
    body = None
    if data is not None:
        headers["Content-Type"] = "application/json"
        body = json.dumps(data).encode()
    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=300) as r:
            return r.status, r.read()
    except urllib.error.HTTPError as e:
        return e.code, e.read()


def split_sections(text: str) -> list[tuple[str, str, str]]:
    """Split narration_only by SCENE headers into locked VO bundles."""
    parts = re.split(r"(?=^SCENE \d+)", text.strip(), flags=re.M)
    by_id: dict[int, str] = {}
    for p in parts:
        p = p.strip()
        if not p:
            continue
        m = re.match(r"SCENE (\d+)\s*[—\-]\s*.+", p)
        if not m:
            continue
        sid = int(m.group(1))
        body = re.sub(r"^SCENE \d+\s*[—\-].*\n?", "", p).strip()
        body = re.sub(r"\[.*?\]", "", body)
        body = re.sub(r"\n{3,}", "\n\n", body).strip()
        by_id[sid] = body

    bundles = [
        ("01_hook-exoplanet", "Scenes 01–02 · hook + what is an exoplanet", [1, 2]),
        ("02_detection", "Scene 03 · how we find them", [3]),
        ("03_diamond-glass", "Scenes 04–05 · diamond + glass rain", [4, 5]),
        ("04_suns-jupiter", "Scenes 06–07 · three suns + hot Jupiter", [6, 7]),
        ("05_eyeball-close", "Scenes 08–11 · eyeball + habitability + recap + CTA", [8, 9, 10, 11]),
    ]
    sections = []
    for slug, label, ids in bundles:
        chunk = "\n\n".join(by_id[i] for i in ids if i in by_id).strip()
        sections.append((slug, label, chunk))
    return sections


def tts(token, mode, text, out: Path):
    payload = {
        "text": text,
        "model_id": MODEL,
        "voice_settings": SETTINGS,
    }
    code, body = api(
        "POST",
        f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"
        f"?output_format=mp3_44100_128",
        token,
        mode,
        payload,
        accept="audio/mpeg",
    )
    if code != 200:
        raise SystemExit(f"TTS failed {code}: {body[:500]}")
    out.write_bytes(body)


def probe_dur(path: Path) -> float:
    out = subprocess.check_output(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "default=noprint_wrappers=1:nokey=1",
            str(path),
        ],
        text=True,
    ).strip()
    return float(out)


def concat_master(paths: list[Path], dest: Path):
    lst = SEC_DIR / f"_concat_list_{VO_VERSION}.txt"
    lines = [f"file '{p}'" for p in paths]
    lst.write_text("\n".join(lines) + "\n")
    dest.parent.mkdir(parents=True, exist_ok=True)
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
            str(lst),
            "-c:a",
            "pcm_s16le",
            "-ar",
            "48000",
            "-ac",
            "1",
            str(dest),
        ],
        check=True,
    )
    mp3 = dest.with_suffix(".mp3")
    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-hide_banner",
            "-loglevel",
            "error",
            "-i",
            str(dest),
            "-codec:a",
            "libmp3lame",
            "-q:a",
            "2",
            str(mp3),
        ],
        check=True,
    )
    return mp3


def main():
    SEC_DIR.mkdir(parents=True, exist_ok=True)
    SEC_TXT.mkdir(parents=True, exist_ok=True)
    MASTER.mkdir(parents=True, exist_ok=True)
    VOICE_MODEL.mkdir(parents=True, exist_ok=True)

    token, mode = load_token()
    (ROOT / "02_Voiceover/.elevenlabs_bearer").write_text(token + "\n")

    code, body = api("GET", "https://api.elevenlabs.io/v1/user/subscription", token, mode)
    if code != 200:
        raise SystemExit(f"subscription check failed {code}: {body[:300]}")
    sub = json.loads(body)
    remaining = (sub.get("character_limit") or 0) - (sub.get("character_count") or 0)
    narr = NARR.read_text().strip()
    need = len(narr)
    print(f"quota remaining={remaining} need≈{need} tier={sub.get('tier')}", flush=True)
    if remaining < need + 500:
        raise SystemExit(f"Insufficient characters: remaining {remaining}, need {need}")

    sections = split_sections(narr)
    stamp = time.strftime("%Y%m%d_%H%M%S")
    paths = []
    meta_sections = []

    for slug, label, text in sections:
        txt_path = SEC_TXT / f"exoplanets_vo_section-{slug}.txt"
        txt_path.write_text(text + "\n")
        out = SEC_DIR / f"exoplanets_vo_section-{slug}_ivc_kDch_{VO_VERSION}.mp3"
        chars = len(text)
        words = len(text.split())
        print(f"\n=== TTS {slug} ({words}w / {chars}c) — {label} ===", flush=True)
        t0 = time.time()
        if out.exists() and out.stat().st_size > 10_000:
            print(f"  skip existing {out.name}", flush=True)
        else:
            tts(token, mode, text, out)
        dur = probe_dur(out)
        paths.append(out)
        meta_sections.append(
            {
                "slug": slug,
                "label": label,
                "words": words,
                "chars": chars,
                "duration_s": round(dur, 2),
                "file": str(out),
                "elapsed_s": round(time.time() - t0, 1),
            }
        )
        print(f"  → {out.name}  {dur:.1f}s  {out.stat().st_size} bytes", flush=True)
        time.sleep(0.4)

    master_wav = MASTER / f"exoplanets_voiceover_{VO_VERSION}_ivc_kDch_master.wav"
    master_mp3 = concat_master(paths, master_wav)
    master_dur = probe_dur(master_wav)
    print(f"\nMASTER {master_wav.name}  {master_dur/60:.2f} min", flush=True)

    report = {
        "generated_at": stamp,
        "voice_id": VOICE_ID,
        "voice_name": "Ben Orbit Narrator",
        "model": MODEL,
        "settings": SETTINGS,
        "vo_version": VO_VERSION,
        "notes": "V003 lock: same eleven_v3 settings as V002 v04; Orbit travelogue sync",
        "auth_mode": mode,
        "narration_source": str(NARR),
        "sections": meta_sections,
        "total_duration_s": round(master_dur, 2),
        "total_duration_min": round(master_dur / 60, 2),
        "master_wav": str(master_wav),
        "master_mp3": str(master_mp3),
        "quota_remaining_before": remaining,
        "chars_used_approx": need,
    }
    report_path = ROOT / f"02_Voiceover/vo_generation_report_{VO_VERSION}.json"
    report_path.write_text(json.dumps(report, indent=2) + "\n")
    REPORT.write_text(json.dumps(report, indent=2) + "\n")

    (VOICE_MODEL / "ben_orbit_voice_settings_v003.md").write_text(
        f"""# Ben Orbit Narrator — Video 003 VO settings ({VO_VERSION})

**Voice ID:** `{VOICE_ID}`  
**Model:** `{MODEL}`  
**Profile:** Documentary · travelogue energy (locked from V002 v04)  
**Master:** `{master_wav.name}` ({master_dur/60:.2f} min)

| Setting | Value |
|---------|-------|
| Stability | {SETTINGS['stability']} |
| Similarity | {SETTINGS['similarity_boost']} |
| Style | {SETTINGS['style']} |
| Speed | {SETTINGS['speed']} |
| Speaker boost | On |

Generated: {stamp}
"""
    )
    print("REPORT", report_path, flush=True)


if __name__ == "__main__":
    main()
