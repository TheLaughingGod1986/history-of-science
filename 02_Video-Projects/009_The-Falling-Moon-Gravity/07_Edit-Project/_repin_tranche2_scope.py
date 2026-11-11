#!/usr/bin/env python3
"""Keep TRANCHE2_SCOPE_J2026.json in step with the v05 boards (J2636).

The picture tool (`_mint_flow_v05_tranche2.py`) pins each board by its sha256, so any change to a board makes the
tool refuse until the scope is pinned to the board as it now is. This does that, and nothing else:

  python3 _repin_tranche2_scope.py            # say what is out of step; exit 1 if anything is
  python3 _repin_tranche2_scope.py --write    # pin the scope to the boards as they are

Run it in the same pull request that changes a board (a KEEP record, a splice flag, a shot that becomes a drawn
diagram), so the board change and the new pin are reviewed together. The repo's tests fail until it has been run.

What it changes:
- `board_sha256` of every row whose board changed.
- `replaced_by` on a row whose board now routes it to a drawn diagram (`route: code-graphic`). The job, the Chief's
  ruling that scoped the diagram and the file are read from the board row itself (`engine_reason`,
  `code_graphic_spec.approval_ref`, `code_graphic_spec.file`). Nothing is typed by hand, and a diagram row that
  does not record all three stops the run. The picture tool never makes a row marked this way.

What it never does: add or remove a row, change a price or a take cap, unmark a row, or touch a board. A row that is
marked `replaced_by` while its board has gone back to a mint is an error to be ruled on, not repaired.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

EDIT_REL = Path("02_Video-Projects/009_The-Falling-Moon-Gravity/07_Edit-Project")
SCOPE_NAME = "TRANCHE2_SCOPE_J2026.json"
DESK_REF = re.compile(r"/pull/180#issuecomment-(\d+)$")


class RepinError(RuntimeError):
    """The scope and a board disagree in a way this tool will not settle."""


def diagram_note(name: str, plate: dict) -> dict:
    """The `replaced_by` mark for a row its board routes to a drawn diagram, from what that board row records."""
    spec = plate.get("code_graphic_spec") or {}
    job = re.match(r"(J\d{4}):", str(plate.get("engine_reason") or ""))
    ref = DESK_REF.search(str(spec.get("approval_ref") or ""))
    if not job or not ref or not spec.get("file"):
        raise RepinError(f"{name} is a drawn diagram on its board, but the board row does not name its job, "
                         "the Chief's ruling and the file")
    return {"route": "code-graphic", "job": job.group(1),
            "ruling": f"history-of-science#180 comment {ref.group(1)}", "file": spec["file"]}


def repin(repo: Path) -> tuple[dict, list[str]]:
    """(the scope pinned to the boards as they are, what changed). Writes nothing."""
    scope = json.loads((repo / EDIT_REL / SCOPE_NAME).read_text())
    changed = []
    for row in scope["rows"]:
        board_path = repo / row["board"]
        digest = hashlib.sha256(board_path.read_bytes()).hexdigest()
        plate = next((p for p in json.loads(board_path.read_text()).get("plates") or [] if p.get("id") == row["id"]), None)
        name = f"P{int(row['part']):02d}:{row['id']}"
        if plate is None:
            raise RepinError(f"{name} is not on {row['board']}")
        if digest != row["board_sha256"]:
            changed.append(f"{name}: pin {row['board_sha256'][:12]} -> {digest[:12]}")
            row["board_sha256"] = digest
        if plate.get("route") == "code-graphic":
            note = diagram_note(name, plate)
            if row.get("replaced_by") != note:
                changed.append(f"{name}: marked replaced by {note['job']} ({note['ruling']})")
                row["replaced_by"] = note
        elif "replaced_by" in row:
            raise RepinError(f"{name} is marked replaced, but its board routes it to {plate.get('route')!r} again")
    return scope, changed


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--write", action="store_true", help="write the scope (default: only say what is out of step)")
    ap.add_argument("--repo", default=str(Path(__file__).resolve().parents[3]))
    args = ap.parse_args(argv)
    try:
        scope, changed = repin(Path(args.repo))
    except RepinError as stop:
        print(f"STOP {stop}", file=sys.stderr)
        return 2
    if not changed:
        print("the scope pins every board as it is")
        return 0
    print("\n".join(changed))
    if not args.write:
        print("out of step: run again with --write, in the same pull request as the board change", file=sys.stderr)
        return 1
    (Path(args.repo) / EDIT_REL / SCOPE_NAME).write_text(json.dumps(scope, indent=2) + "\n")
    print("written")
    return 0


if __name__ == "__main__":
    sys.exit(main())
