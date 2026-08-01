#!/usr/bin/env python3
"""Generate ElevenLabs SFX from [SFX: …] cues in an Orbit script master.

Default: dry-run (parse + write cue manifest only). Pass --generate to call the API.

Examples:
  python3 generate_sfx_from_script.py \\
    --script ../../02_Video-Projects/003_…/01_Script/exoplanets_script_master_v01.md \\
    --out-dir ../../02_Video-Projects/003_…/06_Sound-Effects/generated_v01

  python3 generate_sfx_from_script.py --script … --out-dir … --generate --duration 3
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

SFX_RE = re.compile(r"\[SFX:\s*([^\]]+)\]", re.I)
SCENE_RE = re.compile(r"^###\s+SCENE\s+(\d+)\b|^\[SCENE:\s*(\d+)", re.I | re.M)


def _is_placeholder(text: str) -> bool:
    t = text.strip().lower()
    if not t or t in {"…", "...", "…/", ".../", "sfx", "music"}:
        return True
    if re.fullmatch(r"[.\u2026/ ]+", t):
        return True
    return False


def parse_cues(script_text: str) -> list[dict]:
    """Return unique SFX cues with first scene context and occurrence count."""
    scenes: list[tuple[int, int]] = []  # (char_index, scene_num)
    for m in SCENE_RE.finditer(script_text):
        num = int(m.group(1) or m.group(2))
        scenes.append((m.start(), num))

    def scene_at(pos: int) -> int | None:
        cur = None
        for idx, num in scenes:
            if idx <= pos:
                cur = num
            else:
                break
        return cur

    seen: dict[str, dict] = {}
    for i, m in enumerate(SFX_RE.finditer(script_text), start=1):
        text = " ".join(m.group(1).split()).strip()
        if _is_placeholder(text):
            continue
        key = text.lower()
        if key in seen:
            seen[key]["occurrences"] += 1
            continue
        scene = scene_at(m.start())
        slug = f"{(scene or 0):02d}_{slugify(text)}" if scene else f"{i:02d}_{slugify(text)}"
        seen[key] = {
            "index": len(seen) + 1,
            "text": text,
            "scene": scene,
            "slug": slug,
            "occurrences": 1,
            "char_offset": m.start(),
        }
    return sorted(seen.values(), key=lambda c: c["index"])


def enrich_prompt(cue: str) -> str:
    """Orbit house style: cinematic, restrained, no cartoon whooshes."""
    base = cue.rstrip(".")
    return (
        f"{base}. Cinematic space documentary sound design, clean and restrained, "
        f"no cartoon whoosh, no comedy sting, subtle stereo bed suitable under narration."
    )


def generate_one(
    token: str,
    mode: str,
    text: str,
    out: Path,
    *,
    duration: float | None,
    loop: bool,
) -> None:
    payload: dict = {
        "text": text,
        "model_id": "eleven_text_to_sound_v2",
        "prompt_influence": 0.45,
        "loop": loop,
    }
    if duration is not None:
        payload["duration_seconds"] = duration
    code, body, _ = request(
        "POST",
        "/v1/sound-generation",
        token,
        mode,
        data=payload,
        query="output_format=mp3_44100_128",
        accept="audio/mpeg",
        timeout=180,
    )
    if code != 200:
        raise SystemExit(f"SFX failed {code}: {body[:500]!r}")
    out.write_bytes(body)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--script", type=Path, required=True, help="Script master .md")
    ap.add_argument("--out-dir", type=Path, required=True, help="SFX output directory")
    ap.add_argument(
        "--generate",
        action="store_true",
        help="Call ElevenLabs (costs credits). Default is dry-run manifest only.",
    )
    ap.add_argument(
        "--duration",
        type=float,
        default=None,
        help="SFX duration seconds (0.5–30). Default: API auto.",
    )
    ap.add_argument(
        "--loop",
        action="store_true",
        help="Request seamless loop (good for short ambience beds).",
    )
    ap.add_argument("--limit", type=int, default=0, help="Only first N unique cues")
    args = ap.parse_args()

    script = args.script.expanduser().resolve()
    if not script.exists():
        raise SystemExit(f"Script not found: {script}")
    cues = parse_cues(script.read_text(encoding="utf-8"))
    if args.limit:
        cues = cues[: args.limit]

    out_dir = args.out_dir.expanduser().resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    manifest = {
        "created_at": datetime.now(timezone.utc).isoformat(),
        "script": str(script),
        "generate": bool(args.generate),
        "duration_seconds": args.duration,
        "loop": bool(args.loop),
        "cues": [],
    }

    token = mode = None
    if args.generate:
        token, mode = load_token(prefer_api_key=True)

    for cue in cues:
        prompt = enrich_prompt(cue["text"])
        filename = f"sfx_{cue['slug']}_v01.mp3"
        path = out_dir / filename
        entry = {
            **cue,
            "prompt": prompt,
            "file": filename,
            "status": "planned",
        }
        if args.generate:
            print(f"Generating: {cue['text'][:80]}")
            generate_one(
                token,
                mode,
                prompt,
                path,
                duration=args.duration,
                loop=args.loop,
            )
            entry["status"] = "generated"
            entry["bytes"] = path.stat().st_size
        else:
            print(f"DRY-RUN [{cue['scene'] or '?'}] {cue['text']}")
        manifest["cues"].append(entry)

    report = out_dir / "sfx_generation_manifest.json"
    report.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {report} ({len(cues)} unique cues)")


if __name__ == "__main__":
    main()
