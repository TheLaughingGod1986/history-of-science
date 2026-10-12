#!/usr/bin/env python3
"""Studio board: where every film is, who is working on what, and which jobs have stalled.

PIPELINE.json is the only status source; every write regenerates STATUS.md.
Stages come from PIPELINE.json, and statuses are done, doing, todo, blocked, skip.

  python3 scripts/studio.py board
  python3 scripts/studio.py claim 008 vo --by chief --eta 60 --note "recording"
  python3 scripts/studio.py release 008 vo --by chief --state doing
  python3 scripts/studio.py stale

Add --git to claim/release/set to pull, change PIPELINE.json and STATUS.md only,
commit and push to main. The push is the lock. Another live holder of the same
film+stage returns 75; expired claims can be taken over. stale uses the real
clock; STATUS.md uses the persisted as_of timestamp for deterministic CI.
"""
import argparse, datetime as dt, json, pathlib, subprocess, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
PIPELINE = ROOT / "00_Brand/Channel-Setup/PIPELINE.json"
STATUS = ROOT / "STATUS.md"
sys.path.insert(0, str(ROOT / "00_Brand/Channel-Setup/tools"))
import status_board
STATES = sorted(status_board.STATUSES)
MARK = {"todo": ".", "doing": ">", "done": "+", "skip": "-", "blocked": "!"}
EX_HELD = 75


def now():
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0)


def iso(t):
    return t.strftime("%Y-%m-%dT%H:%MZ")


def parse(s):
    return status_board.parse_timestamp(s)


def load(path):
    return json.loads(path.read_text())


def save(path, data, out):
    errors = status_board.validate(data)
    if errors:
        raise ValueError("; ".join(errors))
    text = status_board.render(data)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")
    out.write_text(text)


def film(data, key):
    return next(f for f in data["films"] if f["id"] == key)


def target_error(data, key, stage):
    if key not in {f["id"] for f in data["films"]}:
        return f"unknown film '{key}' in PIPELINE.json films"
    if stage not in {s["key"] for s in data["stages"]}:
        return f"unknown stage '{stage}' in PIPELINE.json stages"
    return None


def stalled(claim, at):
    return parse(claim["eta"]) < at


def do_claim(data, key, stage, by, eta_min, note, at):
    err = target_error(data, key, stage)
    if err:
        return err
    for c in data["claims"]:
        if c["film"] == key and c["stage"] == stage and c["by"] != by:
            if not stalled(c, at):
                return f"held by {c['by']} since {c['at']} (ETA {c['eta']})"
            note = f"{note} (took over stalled claim by {c['by']}, ETA {c['eta']})".strip()
    data["claims"] = [c for c in data["claims"] if (c["film"], c["stage"]) != (key, stage)]
    data["claims"].append({"film": key, "stage": stage, "by": by, "at": iso(at), "eta": iso(at + dt.timedelta(minutes=eta_min)),
                           "note": note})
    st = film(data, key)["stages"][stage]
    st.update(status="doing", owner=by, note=note)
    return None


def do_release(data, key, stage, by, state, ref):
    err = target_error(data, key, stage)
    if err:
        return err
    mine = [c for c in data["claims"] if c["film"] == key and c["stage"] == stage and c["by"] == by]
    if not mine:
        return f"no claim on {stage} by {by}"
    data["claims"] = [c for c in data["claims"] if c not in mine]
    do_set(data, key, stage, state, ref, None)
    return None


def do_set(data, key, stage, state, ref, nxt):
    err = target_error(data, key, stage)
    if err:
        return err
    s = film(data, key)["stages"][stage]
    s["status"] = state
    s.pop("progress", None)
    if ref:
        s["ref"] = ref
    if nxt is not None:
        data["next_steps"] = [nxt]


def board(data, at):
    stages = [s["key"] for s in data["stages"]]
    rows = ["film  air        " + " ".join(stages)]
    for f in data["films"]:
        cells = " ".join(MARK[f["stages"][s]["status"]] for s in stages)
        rows.append(f"{f['id']:<5} {f.get('air', ''):<10} {cells}  {f['title']}")
    rows.append("key: + done  > doing  . todo  - skip  ! blocked")
    rows.append("claims:" if data["claims"] else "claims: none")
    for c in data["claims"]:
        flag = "STALLED" if stalled(c, at) else "live"
        rows.append(f"{c['film']} {c['stage']} {c['by']} since {c['at']} ETA {c['eta']} {flag} {c['note']}")
    return "\n".join(rows)


def stale_list(data, at):
    return [f"{c['film']} {c['stage']} by {c['by']}: ETA {c['eta']} passed ({c['note']})"
            for c in data["claims"] if stalled(c, at)]


def apply_write(path, out, data, change, at):
    err = change(data)
    if not err:
        data["as_of"] = iso(at)
        data["updated"] = at.date().isoformat()
        save(path, data, out)
    return err


def git(*args):
    return subprocess.run(["git", "-C", str(ROOT), *args], capture_output=True, text=True)


def with_git(path, out, change, message, at, tries=3):
    """Push only the pipeline and regenerated board; retry racing claims from main."""
    if path.resolve() != PIPELINE.resolve() or out.resolve() != STATUS.resolve():
        return "--git requires the repository PIPELINE.json and STATUS.md"
    paths = (str(path), str(out))
    if git("diff", "--name-only", "HEAD", "--", *paths).stdout.strip():
        return "PIPELINE.json/STATUS.md have uncommitted changes; save them first"
    for _ in range(tries):
        if git("pull", "-q", "--rebase", "--autostash", "origin", "main").returncode != 0:
            return "git pull failed; resolve the working tree first"
        data = load(path)
        err = apply_write(path, out, data, change, now())
        if err:
            return err
        if git("add", "--", *paths).returncode != 0:
            return "git add failed"
        if git("commit", "-q", "-m", message, "--", *paths).returncode != 0:
            return "git commit failed"
        if git("push", "-q", "origin", "HEAD:main").returncode == 0:
            return None
        if git("reset", "--soft", "HEAD~1").returncode != 0:
            return "could not undo the racing claim commit"
        if git("reset", "-q", "--", *paths).returncode != 0:
            return "could not unstage the racing claim files"
        if git("checkout", "-q", "--", *paths).returncode != 0:
            return "could not restore the racing claim files"
    return "push kept racing; try again"


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--pipeline", default=str(PIPELINE), help="pipeline file (for isolated dry runs)")
    ap.add_argument("--status", default=str(STATUS), help="generated board path")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("board")
    sub.add_parser("stale")
    for name in ("claim", "release", "set"):
        p = sub.add_parser(name)
        p.add_argument("film")
        p.add_argument("stage")
        p.add_argument("--git", action="store_true")
        if name == "claim":
            p.add_argument("--by", required=True)
            p.add_argument("--eta", type=int, default=60, help="minutes until the claim counts as stalled")
            p.add_argument("--note", default="")
        if name == "release":
            p.add_argument("--by", required=True)
            p.add_argument("--state", choices=STATES, default="doing")
            p.add_argument("--ref")
        if name == "set":
            p.add_argument("state", choices=STATES)
            p.add_argument("--ref")
            p.add_argument("--next")
    a = ap.parse_args(argv)
    path, out = pathlib.Path(a.pipeline), pathlib.Path(a.status)
    data = load(path)
    errors = status_board.validate(data)
    if errors:
        print("; ".join(errors), file=sys.stderr)
        return 1
    at = now()
    if a.cmd == "board":
        print(board(data, at))
        return 0
    if a.cmd == "stale":
        hits = stale_list(data, at)
        print("\n".join(hits) if hits else "no stalled claims")
        return 1 if hits else 0
    err = target_error(data, a.film, a.stage)
    if err:
        print(f"studio: {err}", file=sys.stderr)
        return 1
    if a.cmd == "claim" and a.eta <= 0:
        print("studio: --eta must be positive", file=sys.stderr)
        return 1
    if a.cmd == "claim":
        change = lambda d: do_claim(d, a.film, a.stage, a.by, a.eta, a.note, now())
        msg = f"studio: {a.film} {a.stage} claimed by {a.by}"
    elif a.cmd == "release":
        change = lambda d: do_release(d, a.film, a.stage, a.by, a.state, a.ref)
        msg = f"studio: {a.film} {a.stage} {a.state} by {a.by}"
    else:
        change = lambda d: do_set(d, a.film, a.stage, a.state, a.ref, a.next)
        msg = f"studio: {a.film} {a.stage} {a.state}"
    if a.git:
        err = with_git(path, out, change, msg, at)
    else:
        err = apply_write(path, out, data, change, at)
    if err:
        print(f"studio: {err}", file=sys.stderr)
        return EX_HELD if a.cmd == "claim" and err.startswith("held") else 1
    print(msg)
    return 0


if __name__ == "__main__":
    sys.exit(main())
