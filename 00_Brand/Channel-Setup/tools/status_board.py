#!/usr/bin/env python3
"""Render STATUS.md (repo root) from 00_Brand/Channel-Setup/PIPELINE.json.

One table Ben can read on his phone: every film, how far through it is (%),
what is being worked on now, what is next, and when it should be ready.

  python3 00_Brand/Channel-Setup/tools/status_board.py           # write STATUS.md
  python3 00_Brand/Channel-Setup/tools/status_board.py --check   # CI: fail if STATUS.md is stale

Rules for agents (AGENTS.md -> "Status board"): whoever finishes or starts a
stage edits PIPELINE.json and re-runs this in the same PR. Never edit STATUS.md
by hand. Dates are counted from PIPELINE.json "updated", never from today's
clock, so the file only changes when the data does.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
DATA = ROOT / "00_Brand/Channel-Setup/PIPELINE.json"
OUT = ROOT / "STATUS.md"

STATUSES = {"done", "doing", "todo", "blocked", "skip"}
ICON = {"done": "✅", "doing": "🔄", "todo": "⬜", "blocked": "⛔", "skip": "➖"}
WORD = {"done": "done", "doing": "in progress", "todo": "to do", "blocked": "blocked", "skip": "not needed"}


def parse_date(s: str | None) -> dt.date | None:
    return dt.date.fromisoformat(s) if s else None


def fmt_date(d: dt.date | None) -> str:
    return d.strftime("%a %-d %b") if d else "—"


def bar(pct: int, width: int = 20) -> str:
    filled = round(pct / 100 * width)
    return "█" * filled + "░" * (width - filled)


def validate(data: dict) -> list[str]:
    errors: list[str] = []
    stages = data.get("stages", [])
    keys = [s["key"] for s in stages]
    total = sum(s["weight"] for s in stages)
    if total != 100:
        errors.append(f"stage weights add up to {total}, not 100")
    for film in data.get("films", []):
        fid = film.get("id", "?")
        for key, st in film.get("stages", {}).items():
            if key not in keys:
                errors.append(f"{fid}: unknown stage '{key}'")
            if st.get("status") not in STATUSES:
                errors.append(f"{fid}/{key}: status must be one of {sorted(STATUSES)}")
            p = st.get("progress")
            if p is not None and not (0 <= p <= 1):
                errors.append(f"{fid}/{key}: progress must be between 0 and 1")
        for k in keys:
            if k not in film.get("stages", {}):
                errors.append(f"{fid}: missing stage '{k}'")
    return errors


def film_percent(film: dict, stages: list[dict]) -> int:
    weight_total = 0.0
    earned = 0.0
    for s in stages:
        st = film["stages"][s["key"]]
        if st["status"] == "skip":
            continue
        weight_total += s["weight"]
        if st["status"] == "done":
            earned += s["weight"]
        elif st["status"] in ("doing", "blocked"):
            earned += s["weight"] * float(st.get("progress", 0))
    return round(100 * earned / weight_total) if weight_total else 100


def current_stage(film: dict, stages: list[dict]) -> tuple[dict, dict] | None:
    """The first stage that isn't done or skipped, in pipeline order."""
    for s in stages:
        st = film["stages"][s["key"]]
        if st["status"] not in ("done", "skip"):
            return s, st
    return None


def health(film: dict, stages: list[dict], today: dt.date) -> str:
    if any(film["stages"][s["key"]]["status"] == "blocked" for s in stages):
        return "⛔ blocked"
    late = [
        s for s in stages
        if film["stages"][s["key"]]["status"] not in ("done", "skip")
        and parse_date(film["stages"][s["key"]].get("due"))
        and parse_date(film["stages"][s["key"]]["due"]) < today
    ]
    if late:
        return "🟠 behind"
    return "🟢 on track"


def stage_line(s: dict, st: dict) -> str:
    status = st["status"]
    label = s["label"]
    extra = []
    if status in ("doing", "blocked") and st.get("progress") is not None:
        extra.append(f"{round(100 * st['progress'])}%")
    if st.get("owner") and status != "done":
        extra.append(st["owner"])
    if st.get("due") and status not in ("done", "skip"):
        extra.append(f"due {fmt_date(parse_date(st['due']))}")
    head = f"{ICON[status]} **{label}** — {WORD[status]}"
    if extra:
        head += " (" + ", ".join(extra) + ")"
    note = st.get("note")
    return f"- {head}" + (f": {note}" if note else "")


def render(data: dict) -> str:
    stages = data["stages"]
    today = parse_date(data["updated"])
    films = data["films"]
    lines: list[str] = []
    lines.append("# HOS status board")
    lines.append("")
    lines.append(
        f"**As of {fmt_date(today)} {today.year}**, updated by {data['updated_by']}. "
        "Generated from `00_Brand/Channel-Setup/PIPELINE.json` by "
        "`00_Brand/Channel-Setup/tools/status_board.py`. Don't edit this file by hand."
    )
    lines.append("")
    lines.append("## At a glance")
    lines.append("")
    lines.append("| Film | Airs | Done | Now | Ready for Ben's OK | Health |")
    lines.append("|---|---|---:|---|---|---|")
    for f in films:
        pct = film_percent(f, stages)
        cur = current_stage(f, stages)
        now = "all stages done" if cur is None else f"{cur[0]['label']} ({WORD[cur[1]['status']]})"
        air = parse_date(f.get("air"))
        air_txt = fmt_date(air) + (f" ({(air - today).days} d)" if air else "")
        lines.append(
            f"| **{f['id']}** {f['title']} | {air_txt} | {pct}% | {now} | "
            f"{fmt_date(parse_date(f.get('ready_by')))} | {health(f, stages, today)} |"
        )
    lines.append("")

    lines.append("## Being worked on right now")
    lines.append("")
    doing = [
        (f, s, f["stages"][s["key"]]) for f in films for s in stages
        if f["stages"][s["key"]]["status"] in ("doing", "blocked")
    ]
    if not doing:
        lines.append("Nothing in progress.")
    for f, s, st in doing:
        lines.append(f"- **{f['id']}** · {stage_line(s, st)[2:]}")
    lines.append("")

    lines.append("## Next steps (in order)")
    lines.append("")
    for i, step in enumerate(data.get("next_steps", []), 1):
        lines.append(f"{i}. {step}")
    lines.append("")

    if data.get("credits"):
        lines.append("## Credit left")
        lines.append("")
        lines.append("| Pool | Left | Rule | Checked |")
        lines.append("|---|---|---|---|")
        for c in data["credits"]:
            lines.append(f"| {c['pool']} | {c['left']} | {c['rule']} | {c['checked']} |")
        lines.append("")

    lines.append("## Film by film")
    for f in films:
        pct = film_percent(f, stages)
        lines.append("")
        lines.append(f"### {f['id']} · {f['title']}")
        lines.append("")
        lines.append(f"`{bar(pct)}` **{pct}%**")
        lines.append("")
        air = parse_date(f.get("air"))
        lines.append(
            f"Airs **{fmt_date(air)}** · ready for Ben's OK by **{fmt_date(parse_date(f.get('ready_by')))}** · "
            f"{health(f, stages, today)}"
        )
        if f.get("summary"):
            lines.append("")
            lines.append(f["summary"])
        lines.append("")
        for s in stages:
            lines.append(stage_line(s, f["stages"][s["key"]]))
    lines.append("")
    lines.append("## How the % works")
    lines.append("")
    lines.append(
        "Each stage carries a weight by how much work it is; a film's % is the weight done, "
        "plus part of any stage in progress. Weights: "
        + ", ".join(f"{s['label']} {s['weight']}" for s in stages)
        + "."
    )
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--check", action="store_true", help="fail if STATUS.md doesn't match PIPELINE.json")
    args = ap.parse_args()
    data = json.loads(DATA.read_text())
    errors = validate(data)
    if errors:
        for e in errors:
            print(f"PIPELINE.json: {e}", file=sys.stderr)
        return 1
    text = render(data)
    if args.check:
        current = OUT.read_text() if OUT.exists() else ""
        if current != text:
            print("STATUS.md is stale: run python3 00_Brand/Channel-Setup/tools/status_board.py", file=sys.stderr)
            return 1
        print("STATUS.md matches PIPELINE.json")
        return 0
    OUT.write_text(text)
    print(f"wrote {OUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
