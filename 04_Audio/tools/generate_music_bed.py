#!/usr/bin/env python3
"""Generate an instrumental cinematic music bed via ElevenLabs Music v2.

Default: dry-run (writes plan JSON only). Pass --generate to call the API.

Examples:
  python3 generate_music_bed.py \\
    --project exoplanets \\
    --prompt "Low curious cinematic space documentary bed, warm pads, no vocals" \\
    --out-dir ../../02_Video-Projects/003_…/05_Music \\
    --length-ms 120000

  # From [MUSIC: …] cues in a script (joined into one prompt):
  python3 generate_music_bed.py --script …/script_master_v01.md --out-dir …/05_Music --generate
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

from el_auth import load_token  # noqa: E402
from el_client import request, slugify  # noqa: E402

MUSIC_RE = re.compile(r"\[MUSIC:\s*([^\]]+)\]", re.I)

DEFAULT_NEGATIVE = (
    "vocals, lyrics, singing, pop drums, trap beat, cartoon, comedy sting, "
    "loud riser, EDM drop, phone ringtone"
)

DEFAULT_ORBIT_BED = (
    "Instrumental cinematic space documentary underscore for History of Science. "
    "Warm curious pads, soft low strings, gentle cosmic shimmer, sparse piano "
    "motifs. Builds subtly under narration; leaves room for voice. No vocals."
)


def _is_placeholder(text: str) -> bool:
    t = text.strip().lower()
    if not t or t in {"…", "...", "sfx", "music"}:
        return True
    if re.fullmatch(r"[.\u2026/ ]+", t):
        return True
    return False


def cues_from_script(text: str) -> list[str]:
    out: list[str] = []
    for m in MUSIC_RE.finditer(text):
        cue = " ".join(m.group(1).split()).strip()
        if _is_placeholder(cue):
            continue
        out.append(cue)
    return out


def build_prompt(base: str, cues: list[str]) -> str:
    parts = [base.strip()]
    if cues:
        parts.append("Mood progression from script cues:")
        for i, c in enumerate(cues, 1):
            parts.append(f"{i}. {c}")
    parts.append(f"Avoid: {DEFAULT_NEGATIVE}.")
    return "\n".join(parts)


def compose(
    token: str,
    mode: str,
    prompt: str,
    out: Path,
    *,
    length_ms: int,
) -> dict:
    payload = {
        "prompt": prompt,
        "music_length_ms": length_ms,
        "model_id": "music_v2",
        "force_instrumental": True,
    }
    code, body, headers = request(
        "POST",
        "/v1/music",
        token,
        mode,
        data=payload,
        query="output_format=mp3_44100_128",
        accept="audio/mpeg",
        timeout=600,
    )
    if code != 200:
        raise SystemExit(f"Music compose failed {code}: {body[:800]!r}")
    out.write_bytes(body)
    return {
        "bytes": out.stat().st_size,
        "song_id": headers.get("song-id") or headers.get("x-song-id"),
    }


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--out-dir", type=Path, required=True)
    ap.add_argument("--project", default="orbit", help="Filename prefix slug")
    ap.add_argument("--prompt", default="", help="Override full music prompt")
    ap.add_argument("--script", type=Path, help="Optional script master for [MUSIC:] cues")
    ap.add_argument("--length-ms", type=int, default=120_000, help="3s–600s")
    ap.add_argument("--version", default="v01")
    ap.add_argument(
        "--generate",
        action="store_true",
        help="Call ElevenLabs (costs credits). Default dry-run.",
    )
    args = ap.parse_args()

    if not (3_000 <= args.length_ms <= 600_000):
        raise SystemExit("--length-ms must be between 3000 and 600000")

    cues: list[str] = []
    if args.script:
        script = args.script.expanduser().resolve()
        if not script.exists():
            raise SystemExit(f"Script not found: {script}")
        cues = cues_from_script(script.read_text(encoding="utf-8"))

    prompt = args.prompt.strip() or build_prompt(DEFAULT_ORBIT_BED, cues)
    out_dir = args.out_dir.expanduser().resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    stem = f"{slugify(args.project)}_score_bed_{args.version}"
    audio_path = out_dir / f"{stem}.mp3"
    plan_path = out_dir / f"{stem}_plan.json"

    plan = {
        "created_at": datetime.now(timezone.utc).isoformat(),
        "project": args.project,
        "script": str(args.script) if args.script else None,
        "music_cues": cues,
        "prompt": prompt,
        "length_ms": args.length_ms,
        "model_id": "music_v2",
        "force_instrumental": True,
        "generate": bool(args.generate),
        "audio_file": audio_path.name,
        "status": "planned",
    }

    if args.generate:
        token, mode = load_token()
        print(f"Composing {args.length_ms}ms bed → {audio_path.name}")
        meta = compose(token, mode, prompt, audio_path, length_ms=args.length_ms)
        plan["status"] = "generated"
        plan.update(meta)
    else:
        print("DRY-RUN music plan")
        print(prompt[:500])
        if len(prompt) > 500:
            print("…")

    plan_path.write_text(json.dumps(plan, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {plan_path}")


if __name__ == "__main__":
    main()
