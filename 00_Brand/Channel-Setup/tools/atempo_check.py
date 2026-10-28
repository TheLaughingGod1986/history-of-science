#!/usr/bin/env python3
"""Fail any tracked build that speeds the voice above the house cap (atempo 1.06).

AGENTS.md Never list and STUDIO_PLAYBOOK section 4: `atempo` above 1.06 is never
allowed. No gate checked it, and by 28 Oct 2026 builds at 1.07, 1.08, 1.10,
1.11, 1.12 and 1.40 had all passed every gate (three of them scheduled to air).

Scans tracked files under 02_Video-Projects/ and docs/ (never _archive/):
  - JSON: any key containing "atempo" with a number above the cap
  - Python: a literal atempo=<n> in a filter string, a module-level
    NAME = <n> where NAME contains ATEMPO, and a NAME = <n> that is fed into
    an atempo={NAME} / atempo=%s filter in the same file

Builds that were already over the cap on 28 Oct are listed in
atempo_known_over_cap.json and are reported on every run, not hidden. A new
file over the cap fails. Never add a new file to that list to make this pass:
rebuild at 1.06 or below, or trim pauses instead.

  python3 00_Brand/Channel-Setup/tools/atempo_check.py           # check the repo
  python3 00_Brand/Channel-Setup/tools/atempo_check.py FILE ...  # check given files only
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

CAP = 1.06
ROOT = Path(__file__).resolve().parents[3]
KNOWN = Path(__file__).resolve().parent / "atempo_known_over_cap.json"
SCAN_DIRS = ("02_Video-Projects", "docs")

NUM = r"([0-9]+(?:\.[0-9]+)?)"
LITERAL = re.compile(r"\batempo\s*=\s*" + NUM)  # ffmpeg filter syntax is lower case
DICT_KEY = re.compile(r"""["'][A-Za-z_]*atempo[A-Za-z_]*["']\s*:\s*""" + NUM, re.I)
ASSIGN = re.compile(r"^([A-Za-z_][A-Za-z0-9_]*)\s*(?::[^=]+)?=\s*" + NUM + r"\s*(?:#.*)?$", re.M)
FED = re.compile(r"atempo\s*=\s*\{\s*([A-Za-z_][A-Za-z0-9_]*)", re.I)


def over(value: float) -> bool:
    return value > CAP + 1e-9


def scan_json(text: str) -> list[tuple[str, float]]:
    try:
        data = json.loads(text)
    except ValueError:
        return []
    hits: list[tuple[str, float]] = []

    def walk(node, path: str) -> None:
        if isinstance(node, dict):
            for key, val in node.items():
                here = f"{path}.{key}" if path else str(key)
                if "atempo" in str(key).lower() and isinstance(val, (int, float)) and not isinstance(val, bool):
                    if over(float(val)):
                        hits.append((here, float(val)))
                walk(val, here)
        elif isinstance(node, list):
            for i, val in enumerate(node):
                walk(val, f"{path}[{i}]")

    walk(data, "")
    return hits


def scan_py(text: str) -> list[tuple[str, float]]:
    hits: list[tuple[str, float]] = []
    for m in LITERAL.finditer(text):
        if over(float(m.group(1))):
            line = text.count("\n", 0, m.start()) + 1
            hits.append((f"line {line} atempo={m.group(1)}", float(m.group(1))))
    for m in DICT_KEY.finditer(text):
        if over(float(m.group(1))):
            line = text.count("\n", 0, m.start()) + 1
            hits.append((f"line {line} {m.group(0).split(':')[0].strip()} = {m.group(1)}", float(m.group(1))))
    fed = {name for name in FED.findall(text)}
    for m in ASSIGN.finditer(text):
        name, value = m.group(1), float(m.group(2))
        if ("ATEMPO" in name.upper() or name in fed) and over(value):
            line = text.count("\n", 0, m.start()) + 1
            hits.append((f"line {line} {name} = {m.group(2)}", value))
    return hits


def scan_file(path: Path) -> list[tuple[str, float]]:
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return []
    if path.suffix == ".json":
        return scan_json(text)
    if path.suffix == ".py":
        return scan_py(text)
    return []


def tracked_files() -> list[Path]:
    out = subprocess.run(["git", "ls-files", "--", *SCAN_DIRS], cwd=ROOT, capture_output=True, text=True, check=True)
    return [ROOT / p for p in out.stdout.splitlines()
            if p.endswith((".json", ".py")) and "_archive/" not in p]


def main(argv: list[str]) -> int:
    known = json.loads(KNOWN.read_text(encoding="utf-8"))["files"] if KNOWN.exists() else {}
    files = [Path(a).resolve() for a in argv] if argv else tracked_files()
    new, old = [], []
    for path in files:
        hits = scan_file(path)
        if not hits:
            continue
        rel = path.relative_to(ROOT).as_posix()
        (old if rel in known else new).append((rel, hits))

    for rel, hits in old:
        note = known[rel].get("note", "")
        print(f"KNOWN  {rel}: {', '.join(f'{w} ({v})' for w, v in hits)}" + (f"  [{note}]" if note else ""))
    for rel, hits in new:
        print(f"FAIL   {rel}: {', '.join(f'{w} ({v})' for w, v in hits)}  (cap {CAP})")
    if new:
        print(f"atempo check FAIL: {len(new)} file(s) speed the voice above {CAP}. Rebuild at <= {CAP} or trim pauses.")
        return 1
    print(f"atempo check PASS: no new build above {CAP} ({len(old)} known file(s) listed above).")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
