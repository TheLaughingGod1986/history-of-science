#!/usr/bin/env python3
"""Generate Video 002 VO from blackhole_narration_only_v01.txt via ElevenLabs.

Voice: Ben Orbit Narrator (IVC) kDch6ACCIpqgQ0NsU9kk — Documentary v02 settings.
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
    "002_What-Happens-If-You-Fall-Into-A-Black-Hole"
)
NARR = ROOT / "01_Script/blackhole_narration_performance_v02.txt"
SEC_DIR = ROOT / "02_Voiceover/04_Section-Exports"
SEC_TXT = SEC_DIR / "_section_texts"
MASTER = ROOT / "02_Voiceover/05_Master"
VOICE_MODEL = ROOT / "02_Voiceover/02_Voice-Model"
REPORT = ROOT / "02_Voiceover/vo_generation_report_v01.json"

VOICE_ID = "kDch6ACCIpqgQ0NsU9kk"  # Ben Orbit Narrator
# v04 — polish: keep HOTU energy, reduce drawl/elongation, nudge speed up
MODEL = "eleven_v3"
VO_VERSION = "v04"
SETTINGS = {
    # Slightly higher than v03 creative (0.20) → less word-stretch, still expressive
    "stability": 0.34,
    "similarity_boost": 0.78,
    "style": 0.42,
    "speed": 1.04,  # v03 felt a touch slow at 0.98
    "use_speaker_boost": True,
}

# Scene-aligned section bundles (script scenes 01–15)
SECTION_BREAKS = [
    ("01_hook-context", "Scenes 01–03 · hook + what is + myths"),
    ("02_birth-horizon", "Scenes 04–05 · birth + event horizon"),
    ("03_approach-time", "Scenes 06–07 · approach + time dilation"),
    ("04_fall-crossing", "Scenes 08–10 · spaghetti + crossing + singularity"),
    ("05_mystery-close", "Scenes 11–15 · Hawking + spin + engines + reflect + CTA"),
]

# Paragraph index ranges into narration paragraphs (0-based, end exclusive)
# Filled at runtime after splitting, with fallback equal chunks.


def load_token() -> tuple[str, str]:
    for f in [
        Path("/tmp/elevenlabs_bearer.txt"),
        ROOT / "02_Voiceover/.elevenlabs_bearer",
    ]:
        if f.exists() and f.read_text().strip():
            tok = f.read_text().strip()
            # validate expiry
            try:
                payload = tok.split(".")[1]
                pad = "=" * (-len(payload) % 4)
                pl = json.loads(base64.urlsafe_b64decode(payload + pad))
                if pl.get("exp", 0) > time.time() + 30:
                    return tok, "bearer"
            except Exception:
                pass

    # IndexedDB scrape
    sources = [
        Path("/Users/ben/code/youtube/.playwright-elevenlabs-profile/Default/IndexedDB/"
             "https_elevenlabs.io_0.indexeddb.leveldb"),
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
    """Split narration into 5 story sections by paragraph targets."""
    paras = [p.strip() for p in re.split(r"\n\s*\n", text.strip()) if p.strip()]
    # Target cumulative word fractions matching SECTION_BREAKS weights
    weights = [0.12, 0.22, 0.22, 0.24, 0.20]
    total_w = sum(len(p.split()) for p in paras)
    targets = []
    acc = 0.0
    for w in weights[:-1]:
        acc += w
        targets.append(int(total_w * acc))

    sections = []
    start = 0
    ti = 0
    running = 0
    for i, p in enumerate(paras):
        running += len(p.split())
        if ti < len(targets) and running >= targets[ti]:
            slug, label = SECTION_BREAKS[ti]
            chunk = "\n\n".join(paras[start : i + 1]).strip()
            sections.append((slug, label, chunk))
            start = i + 1
            ti += 1
    slug, label = SECTION_BREAKS[-1]
    chunk = "\n\n".join(paras[start:]).strip()
    if chunk:
        sections.append((slug, label, chunk))
    # If split produced wrong count, equal-ish fallback
    if len(sections) != len(SECTION_BREAKS):
        sections = []
        n = len(SECTION_BREAKS)
        size = max(1, len(paras) // n)
        for i, (slug, label) in enumerate(SECTION_BREAKS):
            a = i * size
            b = len(paras) if i == n - 1 else (i + 1) * size
            sections.append((slug, label, "\n\n".join(paras[a:b]).strip()))
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
    lines = []
    for p in paths:
        lines.append(f"file '{p}'")
    lst.write_text("\n".join(lines) + "\n")
    # decode to wav master for edit flexibility
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
    # also mp3 convenience copy
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

    # quota check
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
    durations = {}
    meta_sections = []

    for slug, label, text in sections:
        txt_path = SEC_TXT / f"blackhole_vo_section-{slug}.txt"
        txt_path.write_text(text + "\n")
        out = SEC_DIR / f"blackhole_vo_section-{slug}_ivc_kDch_{VO_VERSION}.mp3"
        chars = len(text)
        words = len(text.split())
        print(f"\n=== TTS {slug} ({words}w / {chars}c) — {label} ===", flush=True)
        t0 = time.time()
        tts(token, mode, text, out)
        dur = probe_dur(out)
        durations[slug] = dur
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

    master_wav = MASTER / f"blackhole_voiceover_{VO_VERSION}_ivc_kDch_master.wav"
    master_mp3 = concat_master(paths, master_wav)
    master_dur = probe_dur(master_wav)
    print(f"\nMASTER {master_wav.name}  {master_dur/60:.2f} min", flush=True)
    print(f"MASTER mp3 {master_mp3}", flush=True)

    report_path = ROOT / f"02_Voiceover/vo_generation_report_{VO_VERSION}.json"
    report = {
        "generated_at": stamp,
        "voice_id": VOICE_ID,
        "voice_name": "Ben Orbit Narrator",
        "model": MODEL,
        "settings": SETTINGS,
        "vo_version": VO_VERSION,
        "notes": "v04 polish: eleven_v3 + tags; less drawl (stab 0.34, style 0.42, speed 1.04)",
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
    report_path.write_text(json.dumps(report, indent=2) + "\n")
    # keep canonical report pointer on latest
    REPORT.write_text(json.dumps(report, indent=2) + "\n")

    # voice settings card for this project
    (VOICE_MODEL / "ben_orbit_voice_settings_v002.md").write_text(
        f"""# Ben Orbit Narrator — Video 002 VO settings ({VO_VERSION})

**Voice ID:** `{VOICE_ID}`  
**Model:** `{MODEL}`  
**Profile:** Documentary · faster / more energetic  
**Master:** `{master_wav.name}` ({master_dur/60:.2f} min)

| Setting | Value | vs v01 |
|---------|-------|-------|
| Stability | {SETTINGS['stability']} | was 0.50 (less flat) |
| Similarity | {SETTINGS['similarity_boost']} | was 0.83 |
| Style | {SETTINGS['style']} | was 0.08 (more excitement) |
| Speed | {SETTINGS['speed']} | was 0.92 (faster) |
| Speaker boost | On | |

Generated: {stamp}
"""
    )
    print("REPORT", report_path, flush=True)


if __name__ == "__main__":
    main()
