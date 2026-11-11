#!/usr/bin/env python3
"""Check every film's status file, and build the status page from them.

One table Ben can read on his phone: every film, how far through it is (%),
what is being worked on now, what is next, and when it should be ready.

  python3 00_Brand/Channel-Setup/tools/status_board.py --check   # CI and before a commit: are the status files right?
  python3 00_Brand/Channel-Setup/tools/status_board.py           # build STATUS.md and the Kanban page here, to read

Each film keeps its own `02_Video-Projects/<NNN_Name>/status.json` (J2622, the studio's standard for every channel:
one status file per film). What is the channel's and no film's, the stages with their weights and owners, the
next-steps lines and the credit lines, is in `00_Brand/Channel-Setup/BOARD.json`. The two pages are built from those
on demand and are not kept in the repo, so a pull request that moves one film changes one small file and cannot
clash with another film's. Rules for agents: AGENTS.md -> "Status board".
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
from pathlib import Path
from zoneinfo import ZoneInfo

sys.path.insert(0, str(Path(__file__).resolve().parent))
import film_status  # noqa: E402

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "STATUS.md"
KANBAN_TEMPLATE = ROOT / "00_Brand/Channel-Setup/kanban/template.html"
KANBAN_OUT = ROOT / "00_Brand/Channel-Setup/kanban/index.html"

STATUSES = {"done", "doing", "todo", "blocked", "skip"}
ICON = {"done": "✅", "doing": "🔄", "todo": "⬜", "blocked": "⛔", "skip": "➖"}
WORD = {"done": "done", "doing": "in progress", "todo": "to do", "blocked": "blocked", "skip": "not needed"}


def parse_date(s: str | None) -> dt.date | None:
    return dt.date.fromisoformat(s) if s else None


def fmt_date(d: dt.date | None) -> str:
    return d.strftime("%a %-d %b") if d else "—"


def parse_when(s: str) -> dt.datetime:
    """'2026-10-05' or '2026-10-05T17:02' (London time, as agents write it)."""
    return dt.datetime.fromisoformat(s)


def fmt_when(s: str | None) -> str:
    if not s:
        return ""
    w = parse_when(s)
    return fmt_date(w.date()) + (w.strftime(" %H:%M") if "T" in s else "")


def owner_of(s: dict, st: dict) -> str:
    """Who has the stage now: the film's own owner, else the stage's default owner."""
    return st.get("owner") or s.get("owner") or "—"


def activity(st: dict) -> str:
    """Is anyone actually on it right now? 'underway', 'waiting: …', 'blocked: …' or 'queued'."""
    status = st["status"]
    why = st.get("waiting")
    if status == "doing":
        if st.get("underway") is True:
            return "▶️ underway"
        if st.get("underway") is False:
            return "⏸ waiting" + (f": {why}" if why else "")
        return "in progress"
    if status == "blocked":
        return "⛔ blocked" + (f": {why}" if why else "")
    if status == "todo":
        return "queued" + (f" ({why})" if why else "")
    return WORD[status]


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
    for s in stages:
        if not s.get("owner"):
            errors.append(f"stage '{s['key']}': give it a default owner")
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
            steps = st.get("steps")
            if steps is not None and not (isinstance(steps, list) and len(steps) == 2 and 0 <= steps[0] <= steps[1]):
                errors.append(f"{fid}/{key}: steps must be [done, total]")
            if "underway" in st and not isinstance(st["underway"], bool):
                errors.append(f"{fid}/{key}: underway must be true or false")
            if st.get("underway") and st.get("status") != "doing":
                errors.append(f"{fid}/{key}: only a stage in progress (doing) can be underway")
            if st.get("since"):
                try:
                    parse_when(st["since"])
                except ValueError:
                    errors.append(f"{fid}/{key}: since must be YYYY-MM-DD or YYYY-MM-DDTHH:MM")
            for k in ("due", "eta"):
                if st.get(k):
                    try:
                        parse_date(st[k][:10])
                    except ValueError:
                        errors.append(f"{fid}/{key}: {k} must be YYYY-MM-DD")
        for k in keys:
            if k not in film.get("stages", {}):
                errors.append(f"{fid}: missing stage '{k}'")
    return errors


def stage_progress(st: dict) -> float:
    """progress if given, else steps done / total, else 0."""
    if st.get("progress") is not None:
        return float(st["progress"])
    steps = st.get("steps")
    if steps and steps[1]:
        return steps[0] / steps[1]
    return 0.0


def countdown(d: dt.date | None, today: dt.date) -> str:
    if not d:
        return ""
    n = (d - today).days
    if n > 1:
        return f"in {n} d"
    if n == 1:
        return "tomorrow"
    if n == 0:
        return "today"
    return f"{-n} d late"


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
            earned += s["weight"] * stage_progress(st)
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


def time_left(st: dict, today: dt.date) -> str:
    """'2/5 parts · about 2 h left · ETA Tue 6 Oct' for a stage in progress."""
    bits = []
    steps = st.get("steps")
    if steps:
        bits.append(f"{steps[0]}/{steps[1]} {st.get('steps_unit', 'steps')}")
    if st.get("left"):
        bits.append(f"{st['left']} left")
    if st.get("eta"):
        eta = parse_date(st["eta"][:10])
        bits.append(f"ETA {fmt_date(eta)} ({countdown(eta, today)})")
    return " · ".join(bits)


def stage_line(s: dict, st: dict, today: dt.date) -> str:
    status = st["status"]
    label = s["label"]
    extra = []
    if status in ("doing", "blocked"):
        extra.append(f"{round(100 * stage_progress(st))}%")
        tl = time_left(st, today)
        if tl:
            extra.append(tl)
    if status not in ("done", "skip"):
        who = owner_of(s, st)
        if st.get("since"):
            who += f" since {fmt_when(st['since'])}"
        if status in ("doing", "blocked"):
            who += f", {activity(st)}"
        extra.append(f"with {who}")
    if st.get("due") and status not in ("done", "skip"):
        due = parse_date(st["due"])
        extra.append(f"due {fmt_date(due)} ({countdown(due, today)})")
    head = f"{ICON[status]} **{label}** — {WORD[status]}"
    if extra:
        head += " (" + ", ".join(extra) + ")"
    note = st.get("note")
    return f"- {head}" + (f": {note}" if note else "")


def agents_view(data: dict, today: dt.date) -> dict[str, list[str]]:
    """Per agent: what is underway, what is waiting, and what is next in their queue."""
    stages, films = data["stages"], data["films"]
    names: list[str] = []
    for s in stages:
        if s["owner"] not in names:
            names.append(s["owner"])
    for f in films:
        for s in stages:
            o = f["stages"][s["key"]].get("owner")
            if o and o not in names:
                names.append(o)
    out: dict[str, list[str]] = {}
    for who in names:
        now, waiting, queue = [], [], []
        for f in films:
            queued = False  # one "next up" per film: its first to-do stage for this agent
            for s in stages:
                st = f["stages"][s["key"]]
                if owner_of(s, st) != who:
                    continue
                tag = f"{f['id']} {s['label']}"
                if st["status"] == "doing" and st.get("underway") is not False:
                    since = f", since {fmt_when(st['since'])}" if st.get("since") else ""
                    tl = time_left(st, today)
                    now.append(tag + since + (f" ({tl})" if tl else ""))
                elif st["status"] in ("doing", "blocked"):
                    waiting.append(tag + (f": {st['waiting']}" if st.get("waiting") else ""))
                elif st["status"] == "todo" and not queued:
                    queued = True
                    queue.append((st.get("due") or "9999", tag + (f", due {fmt_date(parse_date(st['due']))}" if st.get("due") else "")))
        queue.sort()
        rows = []
        rows.append("- ▶️ Underway: " + ("; ".join(now) if now else "nothing right now"))
        if waiting:
            rows.append("- ⏸ Waiting: " + "; ".join(waiting))
        if queue:
            rows.append("- ⏭ Next up: " + "; ".join(t for _, t in queue[:3]))
        out[who] = rows
    return out


def render(data: dict) -> str:
    stages = data["stages"]
    today = parse_date(data["updated"])
    films = data["films"]
    lines: list[str] = []
    lines.append("# HOS status board")
    lines.append("")
    lines.append(
        f"**Built {fmt_date(today)} {today.year}** from each film's `status.json` and "
        "`00_Brand/Channel-Setup/BOARD.json` by `00_Brand/Channel-Setup/tools/status_board.py`. "
        "This page is not kept in the repo: run the tool to build it. The studio's board shows the same films live."
    )
    lines.append("")
    lines.append("## At a glance")
    lines.append("")
    lines.append("| Film | Airs | Done | Now | With · underway? | Time left on it | Ready for Ben's OK | Health |")
    lines.append("|---|---|---:|---|---|---|---|---|")
    for f in films:
        pct = film_percent(f, stages)
        cur = current_stage(f, stages)
        now = "all stages done" if cur is None else f"{cur[0]['label']} ({WORD[cur[1]['status']]})"
        holder = "—" if cur is None else f"**{owner_of(*cur)}** · {activity(cur[1])}"
        air = parse_date(f.get("air"))
        air_txt = fmt_date(air) + (f" ({(air - today).days} d)" if air else "")
        left = "—"
        if cur is not None and cur[1]["status"] in ("doing", "blocked"):
            left = time_left(cur[1], today) or "not estimated"
        elif cur is not None and cur[1].get("due"):
            left = f"starts later; due {countdown(parse_date(cur[1]['due']), today)}"
        rb = parse_date(f.get("ready_by"))
        rb_txt = fmt_date(rb) + (f" ({countdown(rb, today)})" if rb and rb >= today else "")
        lines.append(
            f"| **{f['id']}** {f['title']} | {air_txt} | {pct}% | {now} | {holder} | {left} | "
            f"{rb_txt} | {health(f, stages, today)} |"
        )
    lines.append("")

    lines.append("## Who's on what")
    lines.append("")
    for who, lines_for in agents_view(data, today).items():
        lines.append(f"**{who}**")
        lines.extend(lines_for)
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
        lines.append(f"- **{f['id']}** · {stage_line(s, st, today)[2:]}")
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
            lines.append(stage_line(s, f["stages"][s["key"]], today))
    lines.append("")
    lines.append("## How the % works")
    lines.append("")
    lines.append(
        "**With** is who has the stage now (the film's `owner`, else the stage's default owner). "
        "**Underway** means someone is working on it at this moment; **waiting** says what it is waiting on. "
        "**Time left** comes from the stage's `steps` (done/total), `left` (the owner's estimate) and `eta`; "
        "\"due in N d\" counts from the date at the top. "
        "Each stage carries a weight by how much work it is; a film's % is the weight done, "
        "plus part of any stage in progress. Weights: "
        + ", ".join(f"{s['label']} {s['weight']}" for s in stages)
        + "."
    )
    lines.append("")
    return "\n".join(lines)


def render_kanban(data: dict) -> str:
    """The Kanban page with the whole board built in as its snapshot."""
    snapshot = json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    return KANBAN_TEMPLATE.read_text().replace("/*SNAPSHOT*/null", snapshot, 1)


def load(today: dt.date | None = None) -> dict:
    """Every film's status file and the channel's own part, as the one document the pages are drawn from. `updated`
    is the day the page is built (London): nothing built is kept in the repo, so dates count from today."""
    data = film_status.read()
    data["updated"] = (today or dt.datetime.now(ZoneInfo("Europe/London")).date()).isoformat()
    return data


def kept_pages(root: Path = ROOT) -> list[str]:
    """The built pages, if someone has committed one again: they are made on demand and must stay out of the repo."""
    import subprocess
    r = subprocess.run(["git", "-C", str(root), "ls-files", "--", str(OUT.relative_to(ROOT)), str(KANBAN_OUT.relative_to(ROOT))],
                       capture_output=True, text=True)
    return r.stdout.split() if r.returncode == 0 else []


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--check", action="store_true", help="check the status files and write nothing")
    args = ap.parse_args(argv)
    try:
        data = load()
    except (OSError, ValueError, KeyError) as e:
        print(f"status files: {e}", file=sys.stderr)
        return 1
    errors = validate(data) + [f"{p} is committed: it is built on demand, remove it from the repo" for p in kept_pages()]
    if errors:
        for e in errors:
            print(f"status files: {e}", file=sys.stderr)
        return 1
    if args.check:
        print(f"{len(data['films'])} status files and BOARD.json are in order")
        return 0
    for p, text in {OUT: render(data), KANBAN_OUT: render_kanban(data)}.items():
        p.write_text(text)
        print(f"built {p.relative_to(ROOT)} (not kept in the repo)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
