#!/usr/bin/env python3
"""Remind agents before shell commands that look like VO/picture generation spend."""
from __future__ import annotations

import json
import re
import sys

GEN_RE = re.compile(
    r"(veo|omni|_generate_|elevenlabs|orbit_voice|orbit_gemini_veo|text_to_speech|"
    r"seedance|kling|generate_vo|vidiq_score|ultra.?credit|generate_videos|flow_veo)",
    re.I,
)


def main() -> None:
    try:
        data = json.load(sys.stdin)
    except Exception:
        data = {}
    command = str(data.get("command") or data.get("tool_input", {}).get("command") or "")
    if not command and isinstance(data.get("arguments"), dict):
        command = str(data["arguments"].get("command") or "")

    if GEN_RE.search(command):
        msg = (
            "HOS spend gate: before ElevenLabs VO or Flow Veo spend, confirm "
            "(1) Ben picked the topic, (2) pre-build vidIQ audit signed, (3) script reviewer ≥90 and "
            "gate:episode PASS. Picture = Flow Veo 3.1 (Quality for lamps/flasks/glows), one plate at a "
            "time until the first KEEP, plate UAT on continuous playback; never Omni, Seedance or Kling; "
            "never 'same DNA' in a prompt; strip Veo audio; VO = Ben Orbit Narrator only. "
            "See STUDIO_PLAYBOOK.md §3–§6."
        )
        sys.stdout.write(
            json.dumps(
                {
                    "permission": "allow",
                    "agent_message": msg,
                }
            )
        )
    else:
        sys.stdout.write(json.dumps({"permission": "allow"}))
    sys.stdout.flush()


if __name__ == "__main__":
    main()
