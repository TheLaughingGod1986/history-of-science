"""The repo as film 009's picture tool saw it when its takes were made (J2636).

Twenty shots were approved and made from the five v05 boards. Since then the Chief has replaced some of them with
drawn diagrams, and each replacement changes a board. The tool pins its boards by hash, so every test that loaded the
live boards broke the day one changed (history-of-science #533, 11 Nov 2026: 77 tests red on main, unseen).

`tests/fixtures/hos009_as_minted/` holds the five boards and the scope file as they were at #528 (4d94db91), the last
change before any shot became a diagram. `then_repo()` is this repo with those in place of today's. Everything else
in it is a link to the real file, so the tool, the retake records and the other films' tools are today's.

The tests of how a take is guarded, priced, made and recorded run there. What is true of the boards as they are now
(the scope pins them, the replaced rows are never made again) is tested on the real repo, in
`tests/test_hos009_final_boards.py`.
"""
from __future__ import annotations

import atexit
import os
import shutil
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EDIT_REL = Path("02_Video-Projects/009_The-Falling-Moon-Gravity/07_Edit-Project")
FIXTURE = ROOT / "tests/fixtures/hos009_as_minted"
BOARDS = tuple(f"parts/part-0{n}_plates_v05.json" for n in range(1, 6))
FROZEN = ("TRANCHE2_SCOPE_J2026.json", *BOARDS)

_then: Path | None = None


def _mirror(src: Path, dest: Path, down: tuple) -> None:
    """Make `dest` a folder of links to what is in `src`. The entry named `down[0]` becomes a real folder, filled the
    same way, so the path down to the edit folder can hold files of its own."""
    for entry in sorted(src.iterdir()):
        if down and entry.name == down[0]:
            (dest / entry.name).mkdir()
            _mirror(entry, dest / entry.name, down[1:])
        elif entry.name != ".git":
            os.symlink(entry, dest / entry.name)


def then_repo() -> Path:
    """The repo with the 009 boards and scope as they were when the takes were made. Built once a run, in a temp folder."""
    global _then
    if _then is None:
        top = Path(tempfile.mkdtemp(prefix="hos009_then_")).resolve()
        atexit.register(shutil.rmtree, top, ignore_errors=True)
        _mirror(ROOT, top, EDIT_REL.parts + ("parts",))
        for rel in FROZEN:
            dest = top / EDIT_REL / rel
            dest.unlink()                                  # the link to today's file
            shutil.copyfile(FIXTURE / rel, dest)
        _then = top
    return _then


THEN = then_repo()
THEN_EDIT = THEN / EDIT_REL


def studio_checkout() -> Path:
    """Where the mint tools look for the studio's shared tab helper (orbit-with-ben scripts/cdp_tabs.py)."""
    return Path(os.environ.get("OWB_REPO", str(Path.home() / "YouTube/orbit-with-ben")))


# Six tests drive the tools' own call into that helper. It lives in the studio's repo, not this one, so they run on
# the Mini and wherever OWB_REPO names a checkout, and are skipped (not failed) where there is none, as in this
# repo's own checks.
NEEDS_STUDIO = "needs the studio's checkout for scripts/cdp_tabs.py (set OWB_REPO)"
HAS_STUDIO = (studio_checkout() / "scripts/cdp_tabs.py").is_file()
