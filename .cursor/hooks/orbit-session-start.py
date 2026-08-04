#!/usr/bin/env python3
"""Orbit sessionStart — inject retention & growth checklist into new agent sessions."""
from __future__ import annotations

import json
import sys

CONTEXT = """
# Orbit session checklist (auto-injected)

Follow these standing rules for this channel:

1. **Pre-build vidIQ audit (blocking)** before script lock / VO / Veo gen → `00_Brand/Channel-Setup/PRE_BUILD_VIDIQ_AUDIT_TEMPLATE.md`
2. **Longs:** 10–12 min · 4–6 chapters · `[VISUAL MUST]` + `[TEACH]` every scene · VO–picture lock
3. **Shorts:** 22–30s punch-first (0–1.5s) · Related+pin when long is public · soft end CTA
4. **Success:** views + higher % watched · wonder over fearbait
5. Canonical: `00_Brand/Channel-Setup/RETENTION_AND_GROWTH_LOCKED.md`

Do not spend Ultra/Veo credits or lock VO until the pre-build audit is signed off for new episodes (V013+).
""".strip()


def main() -> None:
    try:
        json.load(sys.stdin)
    except Exception:
        pass
    out = {
        "env": {
            "ORBIT_RETENTION_GATE": "1",
            "ORBIT_PREBUILD_VIDIQ_REQUIRED": "1",
            "ORBIT_LONGFORM_MINUTES": "10-12",
        },
        "additional_context": CONTEXT,
    }
    sys.stdout.write(json.dumps(out))
    sys.stdout.flush()


if __name__ == "__main__":
    main()
