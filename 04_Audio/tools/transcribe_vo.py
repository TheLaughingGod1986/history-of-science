#!/usr/bin/env python3
"""Transcribe an Orbit VO master with ElevenLabs Scribe → SRT + JSON + plain text.

Useful for captions, chapter timestamps, and Shorts cut planning.

Examples:
  python3 transcribe_vo.py \\
    --audio …/02_Voiceover/05_Master/exoplanets_vo_master_v01.mp3 \\
    --out-dir …/02_Voiceover/06_Captions

  python3 transcribe_vo.py --audio … --out-dir … --dry-run
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

from el_auth import load_token  # noqa: E402
from el_client import multipart_post, slugify  # noqa: E402


def fmt_ts(seconds: float) -> str:
    if seconds < 0:
        seconds = 0.0
    ms = int(round(seconds * 1000))
    h, rem = divmod(ms, 3_600_000)
    m, rem = divmod(rem, 60_000)
    s, milli = divmod(rem, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{milli:03d}"


def words_to_srt(words: list[dict], *, max_chars: int = 42, max_gap: float = 0.85) -> str:
    """Pack word timestamps into readable caption cues."""
    cues: list[tuple[float, float, str]] = []
    buf: list[str] = []
    start: float | None = None
    last_end: float | None = None

    def flush() -> None:
        nonlocal buf, start, last_end
        if not buf or start is None or last_end is None:
            buf, start, last_end = [], None, None
            return
        cues.append((start, last_end, " ".join(buf)))
        buf, start, last_end = [], None, None

    for w in words:
        if w.get("type") and w.get("type") != "word":
            continue
        text = (w.get("text") or "").strip()
        if not text:
            continue
        ws = float(w.get("start", 0))
        we = float(w.get("end", ws))
        if start is None:
            start, last_end, buf = ws, we, [text]
            continue
        gap = ws - (last_end or ws)
        trial = " ".join(buf + [text])
        if gap > max_gap or len(trial) > max_chars:
            flush()
            start, last_end, buf = ws, we, [text]
        else:
            buf.append(text)
            last_end = we
    flush()

    lines: list[str] = []
    for i, (a, b, text) in enumerate(cues, 1):
        lines.append(str(i))
        lines.append(f"{fmt_ts(a)} --> {fmt_ts(b)}")
        lines.append(text)
        lines.append("")
    return "\n".join(lines)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--audio", type=Path, required=True)
    ap.add_argument("--out-dir", type=Path, required=True)
    ap.add_argument("--language", default="eng", help="ISO 639-3 (default eng)")
    ap.add_argument(
        "--dry-run",
        action="store_true",
        help="Validate paths / write stub plan only (no API call).",
    )
    args = ap.parse_args()

    audio = args.audio.expanduser().resolve()
    if not audio.exists():
        raise SystemExit(f"Audio not found: {audio}")
    out_dir = args.out_dir.expanduser().resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    stem = slugify(audio.stem)

    plan = {
        "created_at": datetime.now(timezone.utc).isoformat(),
        "audio": str(audio),
        "model_id": "scribe_v2",
        "language_code": args.language,
        "status": "planned",
    }

    if args.dry_run:
        plan_path = out_dir / f"{stem}_stt_plan.json"
        plan_path.write_text(json.dumps(plan, indent=2) + "\n", encoding="utf-8")
        print(f"DRY-RUN wrote {plan_path}")
        return

    token, mode = load_token()
    print(f"Transcribing {audio.name} …")
    code, body = multipart_post(
        "/v1/speech-to-text",
        token,
        mode,
        fields={
            "model_id": "scribe_v2",
            "language_code": args.language,
            "timestamps_granularity": "word",
            "diarize": "false",
        },
        files=[("file", audio)],
        timeout=900,
    )
    if code != 200:
        raise SystemExit(f"STT failed {code}: {body[:800]!r}")

    data = json.loads(body.decode())
    raw_path = out_dir / f"{stem}_stt_raw.json"
    raw_path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")

    text = (data.get("text") or "").strip()
    txt_path = out_dir / f"{stem}_transcript.txt"
    txt_path.write_text(text + ("\n" if text else ""), encoding="utf-8")

    words = data.get("words") or []
    srt = words_to_srt(words)
    srt_path = out_dir / f"{stem}.srt"
    srt_path.write_text(srt, encoding="utf-8")

    plan["status"] = "generated"
    plan["files"] = {
        "raw_json": raw_path.name,
        "transcript": txt_path.name,
        "srt": srt_path.name,
    }
    plan["duration_seconds"] = data.get("audio_duration_secs") or data.get(
        "audio_duration_seconds"
    )
    plan["word_count"] = len([w for w in words if (w.get("type") or "word") == "word"])
    meta_path = out_dir / f"{stem}_stt_meta.json"
    meta_path.write_text(json.dumps(plan, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {srt_path.name}, {txt_path.name}, {raw_path.name}")


if __name__ == "__main__":
    main()
