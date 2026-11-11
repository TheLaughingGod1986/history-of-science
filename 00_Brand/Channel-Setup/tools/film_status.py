#!/usr/bin/env python3
"""One status file per film, and the way back to PIPELINE.json.

The studio's standard for every channel is one `status.json` in each film's folder (plan decision 2, 10 Nov 2026,
orbit-with-ben docs/MULTI_CHANNEL_PLAN.md). This channel kept every film in one file, `PIPELINE.json`, plus two pages
generated from it and committed. Every pull request that moved a film touched the same three files: on 10 Nov, 24 of
69 open pull requests conflicted on them.

  python3 00_Brand/Channel-Setup/tools/film_status.py check     # can the one file become the many, and come back unchanged?
  python3 00_Brand/Channel-Setup/tools/film_status.py split     # say what would be written, write nothing
  python3 00_Brand/Channel-Setup/tools/film_status.py split --write

What goes where:
  02_Video-Projects/<NNN_Name>/status.json   one film: its number, title, dates, summary and every stage
  studio/channel.json `stages`               the channel's stages in order, each with its label, weight and default
                                             owner, and the kind of job it is (the studio reads these too)
  00_Brand/Channel-Setup/BOARD.json          the rest that is the channel's and no film's: the next-steps lines, the
                                             credit lines, the board's address

A film's file is in the shape Orbit With Ben's films use (`film`, `title`, `air`, `stages` with a `state` for each,
`claims`, `next`), so one reader serves both channels. Everything this channel records beyond that (`ready_by`,
`summary`, and a stage's `note`, `owner`, `due`, `since`, `waiting`, `underway`, `jobs`, `steps`, `steps_unit`,
`left`, `eta`) is kept under the same names. Nothing is dropped: `join(split(x)) == x` for the whole document, and a
test holds it for the real file.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
PIPELINE = ROOT / "00_Brand/Channel-Setup/PIPELINE.json"
BOARD = ROOT / "00_Brand/Channel-Setup/BOARD.json"
CHANNEL = ROOT / "studio/channel.json"
# The kind of job each stage is. The studio routes a stage that is still to do, and that nobody has, to the worker
# for its kind. A stage with no kind here (Ben's OK) is nobody's to route.
KINDS = {"topic": "review", "script": "script", "facts": "facts", "package": "listing", "vo": "vo",
         "shorts_scripts": "script", "shorts_vo": "vo", "picture": "video", "edit": "assembly", "thumbnails": "chart",
         "scheduled": "studio"}
FILMS = ROOT / "02_Video-Projects"
IDEAS = ROOT / "00_Brand/Channel-Setup/ideas"
STATUS = "status.json"


# ---- one film ----

def to_status(film: dict) -> dict:
    """A PIPELINE.json film entry as its own status file."""
    out = {"film": film["id"]}
    out.update((k, v) for k, v in film.items() if k not in ("id", "stages"))
    out["stages"] = {key: _stage_out(st) for key, st in film["stages"].items()}
    out.setdefault("claims", [])
    out.setdefault("next", "")
    return out


def from_status(doc: dict) -> dict:
    """The way back: a status file as the PIPELINE.json entry it came from."""
    film = {"id": doc["film"]}
    for k, v in doc.items():
        if k in ("film", "stages") or (k == "claims" and v == []) or (k == "next" and v == ""):
            continue
        film[k] = v
    film["stages"] = {key: _stage_back(st) for key, st in doc["stages"].items()}
    return film


def _stage_out(st: dict) -> dict:
    if "state" in st:
        raise ValueError("a stage already has a `state`: it cannot also be given one from `status`")
    return {("state" if k == "status" else k): v for k, v in st.items()}


def _stage_back(st: dict) -> dict:
    return {("status" if k == "state" else k): v for k, v in st.items()}


# ---- the whole document ----

def split(data: dict) -> tuple[dict, dict]:
    """(the channel's own part, {film number: its status file})."""
    films = data.get("films") or []
    ids = [f["id"] for f in films]
    if len(set(ids)) != len(ids):
        raise ValueError("two films share a number: " + ", ".join(sorted(i for i in set(ids) if ids.count(i) > 1)))
    board = {k: v for k, v in data.items() if k != "films"}
    if ids != sorted(ids):                    # only kept when the order is not simply by number
        board["film_order"] = ids
    return board, {f["id"]: to_status(f) for f in films}


def join(board: dict, statuses: dict) -> dict:
    """The PIPELINE.json document those parts came from."""
    order = board.get("film_order") or sorted(statuses)
    if sorted(order) != sorted(statuses):
        raise ValueError("the film order and the status files do not name the same films")
    data = {k: v for k, v in board.items() if k != "film_order"}
    data["films"] = [from_status(statuses[i]) for i in order]
    return data


# ---- where a film's file lives ----

def slug(title: str) -> str:
    words = re.findall(r"[A-Za-z0-9]+", title)
    return "-".join(w if w.isupper() else w.capitalize() for w in words[:6]) or "Untitled"


def folder_for(film: dict, films: Path = FILMS, ideas: Path = IDEAS) -> Path:
    """The film's folder under 02_Video-Projects: the one that already carries its number, else the name its idea
    folder has, else a name made from its title. More than one folder with the number is an error, never a guess."""
    fid = film["id"]
    have = sorted(p for p in films.glob(f"{fid}_*") if p.is_dir())
    if len(have) > 1:
        raise ValueError(f"{fid}: more than one film folder carries this number: " + ", ".join(p.name for p in have))
    if have:
        return have[0]
    idea = sorted(p for p in ideas.glob(f"{fid}_*") if p.is_dir())
    return films / (idea[0].name if len(idea) == 1 else f"{fid}_{slug(film.get('title', ''))}")


def paths(data: dict, films: Path = FILMS, ideas: Path = IDEAS) -> dict:
    """{film number: where its status file goes}."""
    return {f["id"]: folder_for(f, films, ideas) / STATUS for f in data.get("films") or []}


def stages_out(stages: list, kinds: dict = KINDS) -> list:
    """The stage list as the channel's settings keep it: each stage as it was, plus the kind of job it is."""
    return [dict(s, **({"kind": kinds[s["key"]]} if s["key"] in kinds else {})) for s in stages]


def stages_back(stages: list) -> list:
    """The way back: the stage list without the kinds, as PIPELINE.json had it."""
    return [{k: v for k, v in s.items() if k != "kind"} for s in stages]


def write(data: dict, films: Path = FILMS, ideas: Path = IDEAS, board: Path = BOARD, channel: Path = CHANNEL) -> list:
    """Write every film's status file, the stage list into the channel's settings, and the rest into BOARD.json.
    Returns the paths written."""
    rest, statuses = split(data)
    written = []
    for fid, path in paths(data, films, ideas).items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(dump(statuses[fid]))
        written.append(path)
    settings = json.loads(channel.read_text())
    settings["stages"] = stages_out(rest.pop("stages"))
    settings["pipeline"] = {"kind": "film_status", "path": f"{films.name}/*/{STATUS}"}     # how the studio is told
    channel.write_text(json.dumps(settings, indent=2) + "\n")
    board.write_text(dump(rest))
    return written + [channel, board]


def read(films: Path = FILMS, board: Path = BOARD, channel: Path = CHANNEL) -> dict:
    """The whole document, put back together from the files on disk."""
    statuses = {}
    for p in sorted(films.glob(f"*/{STATUS}")):
        doc = json.loads(p.read_text())
        where = f"{p.parent.name}/{STATUS}"
        if not isinstance(doc, dict) or not doc.get("film") or not isinstance(doc.get("stages"), dict):
            raise ValueError(f"{where}: needs `film` (its number) and `stages`")
        if not p.parent.name.startswith(str(doc["film"]) + "_"):
            raise ValueError(f"{where}: says it is film {doc['film']}, but its folder carries another number")
        if doc["film"] in statuses:
            raise ValueError(f"two status files are for film {doc['film']}")
        for key, st in doc["stages"].items():
            if not isinstance(st, dict) or "status" in st or "state" not in st:
                raise ValueError(f"{where}: stage '{key}' must be written with `state` (a film's own file says "
                                 "`state`, not `status`)")
        statuses[doc["film"]] = doc
    stages = json.loads(channel.read_text()).get("stages")
    if not isinstance(stages, list) or not all(isinstance(s, dict) and s.get("key") for s in stages):
        raise ValueError(f"{channel.name}: `stages` must list each stage with its key, label, weight and owner")
    return join(dict(json.loads(board.read_text()), stages=stages_back(stages)), statuses)


def dump(doc: dict) -> str:
    return json.dumps(doc, indent=2, ensure_ascii=False) + "\n"


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("cmd", choices=["check", "split"])
    ap.add_argument("--write", action="store_true", help="split: write the files (default: only say what would be written)")
    a = ap.parse_args(argv)
    data = json.loads(PIPELINE.read_text())
    board, statuses = split(data)
    if join(board, statuses) != data:
        print("PIPELINE.json does not come back unchanged: nothing written", file=sys.stderr)
        return 1
    where = paths(data)
    if a.cmd == "check":
        print(f"PIPELINE.json comes back unchanged from {len(statuses)} status files and the channel's own part")
        return 0
    for fid, path in where.items():
        new = "" if path.parent.is_dir() else "  (new folder)"
        print(f"{'write' if a.write else 'would write'} {path.relative_to(ROOT)}{new}")
    for path in (CHANNEL, BOARD):
        print(f"{'write' if a.write else 'would write'} {path.relative_to(ROOT)}" + ("  (its `stages`)" if path == CHANNEL else ""))
    if a.write:
        write(data)
        if read() != data:
            print("the files on disk do not give PIPELINE.json back: check them before anything else changes", file=sys.stderr)
            return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
