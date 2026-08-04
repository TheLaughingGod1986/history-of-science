#!/usr/bin/env python3
"""Remind agents before shell commands that look like VO/picture generation spend."""
from __future__ import annotations

import json
import re
import sys

GEN_RE = re.compile(
    r"(veo|omni|_generate_|elevenlabs|orbit_voice|text_to_speech|seedance|"
    r"generate_vo|vidiq_score|ultra.?credit)",
    re.I,
)


def main() -> None:
    try:
        data = json.load(sys.stdin)
    except Exception:
        data = {}
    command = str(data.get("command") or data.get("tool_input", {}).get("command") or "")
    # Cursor may nest differently; also check raw
    if not command and isinstance(data.get("arguments"), dict):
        command = str(data["arguments"].get("command") or "")

    if GEN_RE.search(command):
        msg = (
            "Orbit gate: before VO/Veo/Omni/gen spend, confirm pre-build vidIQ audit "
            "is signed off and VO–picture / retention rules apply "
            "(RETENTION_AND_GROWTH_LOCKED.md · PRE_BUILD_VIDIQ_AUDIT_TEMPLATE.md)."
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
