#!/usr/bin/env python3
"""HOS 007 long-film VO v01 — Ben Orbit Narrator, settings_for_part, from origin/main script."""
from __future__ import annotations

import argparse
import base64
import hashlib
import json
import re
import subprocess
import sys
import time
from pathlib import Path

REPO = Path("/Users/benjaminoats/YouTube/History Of Science")
sys.path.insert(0, str(REPO / "04_Audio" / "tools"))

from el_auth import load_token  # noqa: E402
from el_client import request  # noqa: E402
from orbit_gemini_veo import load_dotenv  # noqa: E402
from orbit_voice import MODEL_ID, VOICE_ID, VOICE_NAME, settings_for_part  # noqa: E402

HERE = Path(__file__).resolve().parent
DESK = HERE.parent
SCRIPT = DESK / "vaccine_script_master_v01.md"
CONTENT_OPS_ENV = REPO / "07_Content-Ops" / ".env"
GERMS_ENV = (
    REPO
    / "02_Video-Projects"
    / "001_How-Did-We-Discover-Germs"
    / "07_Edit-Project"
    / ".env"
)

SLUGS = {
    1: "the_speckled_monster",
    2: "the_milkmaids_secret",
    3: "a_pail_a_lancet_and_a_boy",
    4: "the_test",
    5: "the_word_that_saved_millions",
}

# Leave headroom for other films (~50k remaining floor)
REMAINING_ABORT_FLOOR = 50_000


def part_text(part: int) -> str:
    """Spoken prose only: drop # / [ / | / <!-- lines; stop at first ---."""
    raw = SCRIPT.read_text(encoding="utf-8")
    cut = []
    for line in raw.splitlines():
        if line.strip() == "---":
            break
        cut.append(line)
    body = "\n".join(cut)
    chunks = re.split(r"^## PART \d+.*$", body, flags=re.M)
    if part >= len(chunks):
        raise SystemExit(f"STOP: part {part} not in script (chunks={len(chunks)})")
    lines = [
        l.strip()
        for l in chunks[part].splitlines()
        if l.strip() and not re.match(r"^(#|\[|\||<!--)", l.strip())
    ]
    return "\n\n".join(lines)


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def probe_dur(path: Path) -> float:
    out = subprocess.check_output(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "csv=p=0",
            str(path),
        ],
        text=True,
    ).strip()
    return float(out)


def user_info(token: str, mode: str) -> dict:
    code, body, _ = request("GET", "/v1/user", token, mode, timeout=60)
    if code != 200:
        return {"error": f"{code}: {body[:300]!r}"}
    return json.loads(body.decode())


def credits_snapshot(info: dict) -> dict:
    sub = (info.get("subscription") or {}) if isinstance(info, dict) else {}
    used = sub.get("character_count")
    limit = sub.get("character_limit")
    remaining = None
    if isinstance(used, int) and isinstance(limit, int):
        remaining = limit - used
    return {
        "used": used,
        "limit": limit,
        "remaining": remaining,
        "tier": sub.get("tier"),
        "raw_keys": sorted(sub.keys()) if isinstance(sub, dict) else [],
    }


def tts(text: str, part: int, token: str, mode: str, out: Path) -> dict:
    if out.exists():
        raise SystemExit(f"STOP: {out.name} exists; versions only go up")
    vs = settings_for_part(part)
    print(
        f"[part{part:02d}] TTS chars={len(text)} words={len(text.split())} "
        f"voice={VOICE_ID} model={MODEL_ID} vs={vs}",
        flush=True,
    )
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
        raise SystemExit(f"TTS failed part {part} {code}: {body[:400]!r}")
    payload = json.loads(body.decode())
    audio_b64 = payload.get("audio_base64") or payload.get("audio")
    if not audio_b64:
        raise SystemExit(f"TTS missing audio_base64 part {part}")
    out.write_bytes(base64.b64decode(audio_b64))
    align = out.with_name(out.stem + "_align.json")
    align.write_text(
        json.dumps(
            payload.get("alignment") or payload.get("normalized_alignment") or {},
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    dur = probe_dur(out)
    sha = sha256_file(out)
    rec = {
        "part": part,
        "slug": SLUGS[part],
        "file": str(out),
        "align": str(align),
        "duration_s": round(dur, 3),
        "sha256": sha,
        "bytes": out.stat().st_size,
        "chars": len(text),
        "words": len(text.split()),
        "voice_id": VOICE_ID,
        "voice_name": VOICE_NAME,
        "model_id": MODEL_ID,
        "voice_settings": vs,
    }
    print(f"[part{part:02d}] SAVED {out.name} {dur:.2f}s sha256 {sha}", flush=True)
    return rec


def extract_only() -> None:
    total_chars = 0
    total_words = 0
    for p, slug in SLUGS.items():
        text = part_text(p)
        txt_path = HERE / f"part{p:02d}_{slug}.txt"
        txt_path.write_text(text + "\n", encoding="utf-8")
        w = len(text.split())
        c = len(text)
        total_chars += c
        total_words += w
        print(f"part{p:02d} {slug}: {w} words / {c} chars → {txt_path.name}", flush=True)
        # Verify Phipps line in part 3
        if p == 3 and "healthy boy, about eight years old" not in text:
            raise SystemExit("STOP: Phipps line missing from part 03 spoken text")
    print(f"TOTAL spoken: {total_words} words / {total_chars} chars", flush=True)
    (HERE / "EXTRACT_META.json").write_text(
        json.dumps(
            {
                "total_chars": total_chars,
                "total_words": total_words,
                "parts": {
                    str(p): {
                        "slug": slug,
                        "chars": len(part_text(p)),
                        "words": len(part_text(p).split()),
                    }
                    for p, slug in SLUGS.items()
                },
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--extract-only", action="store_true")
    ap.add_argument("--parts", type=int, nargs="*", default=[1, 2, 3, 4, 5])
    ap.add_argument("--version", default="v01")
    ap.add_argument("--credits-only", action="store_true")
    ns = ap.parse_args()

    if ns.extract_only:
        extract_only()
        return 0

    for env in (GERMS_ENV, CONTENT_OPS_ENV):
        if env.exists():
            load_dotenv(env)
            print(f"loaded dotenv {env}", flush=True)

    token, mode = load_token(prefer_api_key=True)
    print(f"auth={mode} voice={VOICE_ID} model={MODEL_ID}", flush=True)

    before_raw = user_info(token, mode)
    before = credits_snapshot(before_raw)
    print(
        f"credits_before used={before['used']} limit={before['limit']} "
        f"remaining={before['remaining']} tier={before.get('tier')}",
        flush=True,
    )
    (DESK / "credits_before.json").write_text(
        json.dumps({"snapshot": before, "ts": time.time()}, indent=2) + "\n"
    )

    if ns.credits_only:
        print(json.dumps(before, indent=2))
        return 0

    # Ensure texts exist
    extract_only()
    need = sum(len(part_text(p)) for p in ns.parts)
    if before["remaining"] is not None and before["remaining"] - need < REMAINING_ABORT_FLOOR:
        raise SystemExit(
            f"Abort: remaining {before['remaining']} − need {need} "
            f"= {before['remaining'] - need} would breach {REMAINING_ABORT_FLOOR} floor"
        )

    recs = []
    for p in ns.parts:
        text = part_text(p)
        out = HERE / f"part{p:02d}_{SLUGS[p]}_{ns.version}.mp3"
        recs.append(tts(text, p, token, mode, out))

    after_raw = user_info(token, mode)
    after = credits_snapshot(after_raw)
    print(
        f"credits_after used={after['used']} limit={after['limit']} "
        f"remaining={after['remaining']}",
        flush=True,
    )
    # Refresh once if lag (used unchanged despite spend)
    chars_sent = sum(r["chars"] for r in recs)
    if (
        isinstance(before["used"], int)
        and isinstance(after["used"], int)
        and after["used"] == before["used"]
        and chars_sent > 0
    ):
        print("character_count lagged; sleeping 8s and refreshing…", flush=True)
        time.sleep(8)
        after_raw = user_info(token, mode)
        after = credits_snapshot(after_raw)
        print(
            f"credits_after_refreshed used={after['used']} remaining={after['remaining']}",
            flush=True,
        )

    (DESK / "credits_after.json").write_text(
        json.dumps({"snapshot": after, "ts": time.time(), "chars_sent": chars_sent}, indent=2)
        + "\n"
    )
    meta = {
        "film": "007",
        "version": ns.version,
        "parts": recs,
        "chars_sent_total": chars_sent,
        "auth_mode": mode,
        "credits_before": before,
        "credits_after": after,
        "voice_id": VOICE_ID,
        "voice_name": VOICE_NAME,
        "model_id": MODEL_ID,
        "no_video": True,
        "no_picture_spend": True,
        "no_plan_upgrade": True,
        "script": str(SCRIPT),
    }
    meta_path = HERE / f"VO_TAKES_{ns.version}.json"
    meta_path.write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {meta_path}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
