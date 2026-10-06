#!/usr/bin/env python3
"""HOS desk — Claude (cloud) and Grok (the Mac Mini) talk in one GitHub PR, Ben is pinged for approvals.

Written 1 Oct 2026 so Ben stops copying prompts, reports and thumbnails between the two agents.
Rules: STUDIO_PLAYBOOK.md §15. Runs on the Mini with the `gh` CLI (logged in as Ben) and Pillow.

The desk is one draft PR from the branch `hos-desk`, titled "HOS desk — never merge". Every
message is a PR comment that starts with a hidden header:

  <!-- hos-desk v1 from=grok to=claude film=005 stage=thumbnails status=review -->

  from/to:  claude | grok | ben     status: task | review | question | blocked | approval | done
A comment with no header is Ben talking. Claude reads every comment (GitHub wakes its session);
the Mini's watcher hands Grok every comment addressed to Grok. Images go on the `hos-desk`
branch under _desk/ (never on main); video and audio never go in git.

  python3 hos_desk.py init                                  # once: branch, label, draft PR
  python3 hos_desk.py post --to claude --film 005 --stage thumbnails --status review \\
      --body-file report.md --image sheet_long.jpg --image preview_168.jpg
  python3 hos_desk.py inbox                                 # print new messages for Grok
  python3 hos_desk.py inbox --watch 120 --run               # the Mini's watcher (launchd)
  python3 hos_desk.py thread --last 10                      # read the desk

`--run` starts Grok on each new task with $HOS_DESK_AGENT_CMD, where {file} is the message file,
e.g.  HOS_DESK_AGENT_CMD='cursor-agent -p --force "$(cat {file})"'.  Without it the watcher shows
a macOS notification and Grok picks the task up with `inbox` when Ben opens Cursor.
Only comments by $HOS_DESK_TRUSTED (default: the repo owner) are ever acted on.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shlex
import shutil
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

BRANCH = "hos-desk"
LABEL = "hos-desk"
NEEDS_BEN = "needs-ben"
TITLE = "HOS desk — Claude ↔ Grok (never merge)"
HOME = Path(os.environ.get("HOS_DESK_HOME", Path.home() / ".hos_desk"))
PARTIES = ("claude", "grok", "cursor", "ben")
WRITERS = ("grok", "cursor")  # the write lane: Grok, or Cursor while Grok is out (AGENTS.md)
STATUSES = ("task", "review", "question", "blocked", "approval", "done")
MEDIA = re.compile(r"\.(mp4|mov|m4v|webm|wav|mp3|m4a|aac|aif|aiff|flac)$", re.I)
HEADER = re.compile(r"<!--\s*hos-desk v1 (.*?)-->", re.S)


# ---------- message format (pure, tested) ----------

def header(**kv: str) -> str:
    return "<!-- hos-desk v1 " + " ".join(f"{k}={re.sub(r'[^A-Za-z0-9_.-]+', '-', v)}" for k, v in kv.items() if v) + " -->"


def parse(body: str) -> dict | None:
    """The header of a desk comment (it must open the comment), or None for a plain (Ben) comment."""
    m = HEADER.match((body or "").lstrip())
    if not m:
        return None
    return dict(re.findall(r"(\w+)=(\S+)", m.group(1)))


def compose(frm: str, to: str, film: str, stage: str, status: str, body: str, images: list[str]) -> str:
    title = f"### {frm.title()} → {to.title()} · {film or '—'} · {stage or '—'} · {status}"
    parts = [header(**{"from": frm, "to": to, "film": film, "stage": stage, "status": status}), title, "", body.strip()]
    if images:
        parts += ["", *[f"![{Path(u.split('?')[0]).name}]({u})" for u in images]]
    return "\n".join(parts) + "\n"


def for_agent(comments: list[dict], after_id: int, trusted: str, me: str = "grok") -> list[dict]:
    out = []
    for c in comments:
        if c["id"] <= after_id or c["user"]["login"].lower() != trusted.lower():
            continue
        h = parse(c["body"])
        if h and h.get("to") == me:
            out.append({**c, "header": h})
    return out


# ---------- GitHub via gh ----------

def sh(*cmd: str, cwd: Path | None = None, check: bool = True) -> str:
    r = subprocess.run(cmd, cwd=cwd, text=True, capture_output=True)
    if check and r.returncode:
        sys.exit(f"{' '.join(cmd[:3])}… failed: {r.stderr.strip()}")
    return r.stdout.strip()


def repo() -> str:
    return os.environ.get("HOS_DESK_REPO") or sh("gh", "repo", "view", "--json", "nameWithOwner", "-q", ".nameWithOwner")


def desk_pr(r: str) -> int:
    n = sh("gh", "pr", "list", "-R", r, "--head", BRANCH, "--state", "open", "--json", "number", "-q", ".[0].number")
    if not n:
        sys.exit("No open desk PR. Run: python3 hos_desk.py init")
    return int(n)


def comments(r: str, pr: int) -> list[dict]:
    out = sh("gh", "api", "--paginate", f"repos/{r}/issues/{pr}/comments?per_page=100", "--jq", ".[]")
    return [json.loads(line) for line in out.splitlines() if line.strip()]


def sparse_clone(r: str, dest: Path, branch: str | None = None) -> None:
    """Clone only `_desk/` (no other blobs): the Mini's disk can't hold a full second copy of the repo."""
    cmd = ["git", "clone", "--quiet", "--filter=blob:none", "--no-checkout", "--single-branch", "--depth", "1"]
    if branch:
        cmd += ["--branch", branch]
    sh(*cmd, f"https://github.com/{r}.git", str(dest))
    sh("git", "sparse-checkout", "set", "--no-cone", "/_desk/", cwd=dest)
    sh("git", "checkout", "--quiet", branch or "HEAD", cwd=dest)


def worktree(r: str) -> Path:
    wt = HOME / "worktree"
    if not (wt / ".git").exists():
        HOME.mkdir(parents=True, exist_ok=True)
        shutil.rmtree(wt, ignore_errors=True)
        sparse_clone(r, wt, BRANCH)
    sh("git", "pull", "--quiet", "--ff-only", cwd=wt)
    return wt


def push_images(r: str, film: str, stage: str, paths: list[str]) -> list[str]:
    from PIL import Image

    wt = worktree(r)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M")
    rel_dir = Path("_desk") / (film or "general") / f"{stamp}_{stage or 'msg'}"
    (wt / rel_dir).mkdir(parents=True, exist_ok=True)
    rels = []
    for p in map(Path, paths):
        if MEDIA.search(p.name):
            sys.exit(f"{p.name}: video/audio never goes in git. Post a still or contact sheet, and the file's path on the Mini.")
        im = Image.open(p).convert("RGB")
        im.thumbnail((1600, 1600))
        rel = rel_dir / (p.stem + ".jpg")
        im.save(wt / rel, "JPEG", quality=85)
        rels.append(rel)
    # .gitignore ignores **/*.jpg; desk stills are allowed (MEDIA above keeps video/audio out).
    sh("git", "add", "-f", *map(str, rels), cwd=wt)
    sh("git", "commit", "--quiet", "-m", f"desk: {film} {stage} images", cwd=wt)
    sh("git", "push", "--quiet", "origin", BRANCH, cwd=wt)
    sha = sh("git", "rev-parse", "HEAD", cwd=wt)
    return [f"https://github.com/{r}/blob/{sha}/{rel.as_posix()}?raw=true" for rel in rels]


# ---------- commands ----------

def cmd_init(ns) -> None:
    r = repo()
    existing = sh("gh", "pr", "list", "-R", r, "--head", BRANCH, "--state", "open", "--json", "number", "-q", ".[0].number")
    if existing:
        print(f"Desk already open: PR #{existing}")
        return
    for name, colour, desc in ((LABEL, "5319e7", "Claude ↔ Grok desk"), (NEEDS_BEN, "d93f0b", "Waiting on Ben")):
        sh("gh", "label", "create", name, "-R", r, "--color", colour, "--description", desc, "--force")
    tmp = HOME / "init"
    shutil.rmtree(tmp, ignore_errors=True)
    sparse_clone(r, tmp)
    sh("git", "checkout", "--quiet", "-b", BRANCH, cwd=tmp)
    (tmp / "_desk").mkdir(exist_ok=True)
    (tmp / "_desk" / "README.md").write_text(
        "# HOS desk\n\nReview images posted between Claude and Grok. This branch is never merged.\n"
        "Rules: `00_Brand/Channel-Setup/STUDIO_PLAYBOOK.md` §15.\n")
    sh("git", "add", "_desk", cwd=tmp)
    sh("git", "commit", "--quiet", "-m", "desk: open the HOS desk", cwd=tmp)
    sh("git", "push", "--quiet", "-u", "origin", BRANCH, cwd=tmp)
    body = ("Claude and Grok talk here; Ben is pinged when something needs his OK.\n\n"
            "**Never merge this PR.** Rules: `STUDIO_PLAYBOOK.md` §15. Tool: `00_Brand/Channel-Setup/tools/hos_desk.py`.\n\n"
            "Ben: reply in plain words (\"approved\", \"change X\"). Claude reads it and briefs Grok.")
    url = sh("gh", "pr", "create", "-R", r, "--draft", "--head", BRANCH, "--base", "main",
             "--title", TITLE, "--body", body, "--label", LABEL, cwd=tmp)
    shutil.rmtree(tmp, ignore_errors=True)
    print(f"Desk open: {url}")


def cmd_post(ns) -> None:
    r = repo()
    pr = desk_pr(r)
    body = Path(ns.body_file).read_text() if ns.body_file else (ns.body or "")
    if not body.strip():
        sys.exit("Empty message: pass --body or --body-file")
    urls = push_images(r, ns.film, ns.stage, ns.image) if ns.image else []
    text = compose(ns.frm, ns.to, ns.film, ns.stage, ns.status, body, urls)
    f = HOME / "outbox.md"
    HOME.mkdir(parents=True, exist_ok=True)
    f.write_text(text)
    print(sh("gh", "pr", "comment", str(pr), "-R", r, "--body-file", str(f)))
    if ns.to == "ben" or ns.status == "approval":
        sh("gh", "pr", "edit", str(pr), "-R", r, "--add-label", NEEDS_BEN)


def load_state() -> dict:
    try:
        return json.loads((HOME / "state.json").read_text())
    except Exception:
        return {"last": 0}


def save_state(s: dict) -> None:
    HOME.mkdir(parents=True, exist_ok=True)
    (HOME / "state.json").write_text(json.dumps(s))


def notify(msg: str) -> None:
    if shutil.which("osascript"):
        subprocess.run(["osascript", "-e", f'display notification {json.dumps(msg)} with title "HOS desk"'])


def run_agent(msg_file: Path) -> int:
    tpl = os.environ.get("HOS_DESK_AGENT_CMD")
    if not tpl:
        return -1
    cmd = tpl.replace("{file}", shlex.quote(str(msg_file)))
    print(f"→ starting Grok on {msg_file.name}")
    return subprocess.run(cmd, shell=True, cwd=os.environ.get("HOS_REPO_DIR") or None).returncode


def check_inbox(ns) -> int:
    r = repo()
    pr = desk_pr(r)
    trusted = os.environ.get("HOS_DESK_TRUSTED") or r.split("/")[0]
    me = ns.agent
    key = "last" if me == "grok" else f"last_{me}"
    state = load_state()
    new = for_agent(comments(r, pr), state.get(key, 0), trusted, me)
    inbox = HOME / "inbox"
    inbox.mkdir(parents=True, exist_ok=True)
    for c in new:
        h = c["header"]
        f = inbox / f"{c['id']}_{h.get('film', 'x')}_{h.get('stage', 'msg')}.md"
        f.write_text(
            f"# Desk task for {me.title()} (PR #{pr}, comment {c['id']})\n\n"
            "Follow AGENTS.md. When finished, reply on the desk with:\n"
            f"  python3 00_Brand/Channel-Setup/tools/hos_desk.py post --from {me} --to claude --film {h.get('film', '')} "
            f"--stage {h.get('stage', '')} --status review --body-file <report.md> [--image <png/jpg> …]\n\n"
            + c["body"])
        print(f"\n=== {f}\n{c['body']}")
        if ns.run:
            rc = run_agent(f)
            if rc == -1:
                notify(f"Task for {me.title()}: {h.get('film', '')} {h.get('stage', '')}")
            elif rc:
                print(f"agent exited {rc}; message left in {f}")
        state[key] = c["id"]
        save_state(state)
    if not new:
        print(f"No new messages for {me.title()}.")
    return len(new)


def cmd_inbox(ns) -> None:
    if not ns.watch:
        check_inbox(ns)
        return
    while True:
        try:
            check_inbox(ns)
        except SystemExit as e:
            print(e)
        except Exception as e:  # keep the watcher alive through network blips
            print(f"inbox error: {e}")
        time.sleep(ns.watch)


def cmd_thread(ns) -> None:
    r = repo()
    for c in comments(r, desk_pr(r))[-ns.last:]:
        h = parse(c["body"]) or {"from": "ben"}
        print(f"\n--- {c['created_at']} {h.get('from')}→{h.get('to', 'all')} {h.get('film', '')} {h.get('stage', '')}")
        print(HEADER.sub("", c["body"]).strip())


def main() -> None:
    # launchd writes stdout to a file; without line buffering watch.log stays empty.
    sys.stdout.reconfigure(line_buffering=True)
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("init").set_defaults(fn=cmd_init)
    p = sub.add_parser("post")
    p.add_argument("--from", dest="frm", choices=PARTIES, default="grok")
    p.add_argument("--to", choices=PARTIES, required=True)
    p.add_argument("--film", default="")
    p.add_argument("--stage", default="")
    p.add_argument("--status", choices=STATUSES, default="review")
    p.add_argument("--body")
    p.add_argument("--body-file")
    p.add_argument("--image", action="append", default=[])
    p.set_defaults(fn=cmd_post)
    p = sub.add_parser("inbox")
    p.add_argument("--watch", type=int, default=0, help="poll every N seconds")
    p.add_argument("--run", action="store_true", help="start the agent with $HOS_DESK_AGENT_CMD")
    p.add_argument("--as", dest="agent", choices=WRITERS, default="grok", help="whose inbox (cursor while Grok is out)")
    p.set_defaults(fn=cmd_inbox)
    p = sub.add_parser("thread")
    p.add_argument("--last", type=int, default=10)
    p.set_defaults(fn=cmd_thread)
    ns = ap.parse_args()
    ns.fn(ns)


if __name__ == "__main__":
    main()
