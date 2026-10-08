"""One `ai_spend.py spend` line per take, for the AI spend month (Ben, 8 Oct 2026; OWB AGENTS.md "AI spend month").

The ledger and its CLI live in orbit-with-ben (`scripts/ai_spend.py`, `05_Analytics/ai_spend/ledger.jsonl`).
Measurement only: a failed write is printed and never stops a mint.

    from ai_spend_hook import spend
    spend("vertex", 5.12, "HOS:006", "P3:04 Quality take 1 (veo-3.1, 8 s)", by="cursor")
"""
from __future__ import annotations

import os
import re
import subprocess
import sys
from pathlib import Path

OWB = Path(os.environ.get("OWB_REPO", Path.home() / "YouTube" / "orbit-with-ben"))
AI_SPEND = OWB / "scripts" / "ai_spend.py"
GBP_PER_USD = 0.80  # the HOS minters' conservative rate; the Vertex credit is in GBP


def film_of(path: Path) -> str:
    m = re.search(r"02_Video-Projects/(\d{3})_", str(Path(path).resolve()))
    return f"HOS:{m.group(1)}" if m else ""


def spend(pool: str, amount: float, film: str, what: str, by: str | None = None) -> None:
    by = by or os.environ.get("OWB_AGENT") or "hos-minter"
    if not AI_SPEND.exists():
        print(f"  ai_spend: {AI_SPEND} missing; spend not recorded ({pool} {amount} {what})", flush=True)
        return
    r = subprocess.run([sys.executable, str(AI_SPEND), "spend", "--pool", pool, "--amount", f"{amount:g}",
                        "--film", film, "--what", what, "--by", by.lower()],
                       cwd=OWB, capture_output=True, text=True)
    if r.returncode != 0:
        print(f"  ai_spend: not recorded ({(r.stderr or r.stdout).strip()[:200]})", flush=True)
