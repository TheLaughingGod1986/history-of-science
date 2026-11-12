#!/usr/bin/env python3
"""HOS desk — Claude (cloud) and Grok (the Mac Mini) talk in one GitHub PR, Ben is pinged for approvals.

Written 1 Oct 2026 so Ben stops copying prompts, reports and thumbnails between the two agents.
Rules: STUDIO_PLAYBOOK.md §15. Runs on the Mini with the `gh` CLI (logged in as Ben) and Pillow.

The desk is one draft PR from the branch `hos-desk`, titled "HOS desk — never merge". Every
message is a PR comment that starts with a hidden header:

  <!-- hos-desk v1 from=grok to=claude film=005 stage=thumbnails status=review -->

  from/to:  claude | grok | cursor | codex | ben | gemini | chief
  status: task | review | question | blocked | approval | done
  `to=chief` is the elected Chief (Grok, else Claude, Codex, Gemini), never Cursor.
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
import hashlib
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
PARTIES = ("claude", "grok", "cursor", "codex", "ben", "chief", "gemini")
WRITERS = ("grok", "cursor", "codex", "claude", "gemini")  # who may post and read an inbox; not the role name
SENDERS = ("claude", "grok", "cursor", "codex", "ben", "gemini")  # never post as chief; that would impersonate the role
CHIEF_DESK_IDS = ("grok", "claude", "codex", "gemini")  # Cursor is outside the succession (Ben, 26 Oct 2026)
CODE = "j2324-safe-role-routing"
LOADED_SHA256 = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
STATUSES = ("task", "review", "question", "blocked", "approval", "done")
MEDIA = re.compile(r"\.(mp4|mov|m4v|webm|wav|mp3|m4a|aac|aif|aiff|flac)$", re.I)
HEADER = re.compile(r"<!--\s*hos-desk v1 (.*?)-->", re.S)


# ---------- message format (pure, tested) ----------

def recipient_list(to: str) -> list[str]:
    """Comma-separated recipients, in order, with duplicates removed."""
    seen = []
    for part in str(to or "").split(","):
        name = part.strip().lower()
        if name and name not in seen:
            seen.append(name)
    return seen


def desk_id_for(agent: str | None) -> str | None:
    """Map a relay id onto a desk id. `chief` is Grok's desk id. Cursor is never a Chief."""
    if not agent:
        return None
    name = str(agent).strip().lower()
    if name in ("", "none", "cursor"):
        return None
    if name == "chief":
        return "grok"
    if name in CHIEF_DESK_IDS:
        return name
    return None


def header(**kv: str) -> str:
    parts = []
    for k, v in kv.items():
        if not v:
            continue
        if k == "to":
            cleaned = ",".join(recipient_list(str(v)))
        else:
            cleaned = re.sub(r"[^A-Za-z0-9_.-]+", "-", str(v))
        parts.append(f"{k}={cleaned}")
    return "<!-- hos-desk v1 " + " ".join(parts) + " -->"


def parse(body: str) -> dict | None:
    """The header of a desk comment (it must open the comment), or None for a plain (Ben) comment."""
    m = HEADER.match((body or "").lstrip())
    if not m:
        return None
    return dict(re.findall(r"(\w+)=(\S+)", m.group(1)))


def compose(frm: str, to: str, film: str, stage: str, status: str, body: str, images: list[str], reply_to: str = "", supersedes: str = "") -> str:
    title = f"### {frm.title()} → {to.title()} · {film or '—'} · {stage or '—'} · {status}"
    parts = [header(**{"from": frm, "to": to, "film": film, "stage": stage, "status": status, "reply_to": str(reply_to) if reply_to else "", "supersedes": str(supersedes) if supersedes else ""}), title, "", body.strip()]
    if images:
        parts += ["", *[f"![{Path(u.split('?')[0]).name}]({u})" for u in images]]
    return "\n".join(parts) + "\n"


def role_holder(state: dict | None, message_id: int, elected: str | None) -> str | None:
    """Who holds a chief-role message. An existing assignment stays put until handback."""
    assignment = ((state or {}).get("assignments") or {}).get(str(message_id)) or {}
    holder = assignment.get("holder")
    if holder in CHIEF_DESK_IDS:
        return holder
    return desk_id_for(elected)


def addressed(header: dict, me: str, elected: str | None = None, state: dict | None = None, message_id: int | None = None) -> bool:
    """Literal recipients match once. `chief` matches only the elected desk id, never Cursor.
    The literal inbox (elected is None) does not take role mail; deliver_role owns that copy."""
    recips = recipient_list(header.get("to", ""))
    if "chief" in recips:
        if elected is None or me not in CHIEF_DESK_IDS:
            return False
        return role_holder(state, message_id if message_id is not None else -1, elected) == me
    return me in recips


def for_agent(comments: list[dict], after_id: int, trusted: str, me: str = "grok", elected: str | None = None, state: dict | None = None) -> list[dict]:
    out = []
    seen = set()
    for c in comments:
        if c["id"] <= after_id or c["user"]["login"].lower() != trusted.lower() or c["id"] in seen:
            continue
        h = parse(c["body"])
        if not h or not addressed(h, me, elected, state, c["id"]):
            continue
        seen.add(c["id"])
        role = "chief" in recipient_list(h.get("to", "")) and role_holder(state, c["id"], elected) == me
        out.append({**c, "header": h, "role": role})
    return out


def worker_may_run(header: dict, me: str) -> bool:
    """A message addressed to the Chief role must not start the Cursor worker."""
    if "chief" in recipient_list(header.get("to", "")):
        return False
    return me != "chief"


def resolve_elected() -> str | None:
    """Desk id recorded by the Chief relay, unless HOS_DESK_ELECTED overrides it. Cursor never comes back."""
    raw = os.environ.get("HOS_DESK_ELECTED")
    if raw is not None:
        return desk_id_for(raw)
    path = Path(os.environ.get("CHIEF_CURRENT", str(Path.home() / "_desk/state/chief/current.json")))
    try:
        agent = json.loads(path.read_text()).get("agent")
    except (OSError, ValueError):
        return None
    return desk_id_for(agent)


def select_role_messages(comments: list[dict], state: dict, me: str, elected: str | None, trusted: str, recover_id: int | None = None) -> list[dict]:
    """New chief-role mail for the elected holder.

    The first call seeds last_role to the current max id and delivers nothing older.
    A single recover_id is the only older id that may be admitted. The watermark only moves forward.
    """
    if me != desk_id_for(elected) or me not in CHIEF_DESK_IDS:
        return []
    ids = [c.get("id", 0) for c in comments]
    if "last_role" not in state:
        state["last_role"] = max(ids) if ids else 0
        state["role_seeded"] = True
        if recover_id is None:
            return []
    acked = set()
    for bucket in (state.get("acknowledged") or {}).values():
        acked.update(str(item) for item in bucket)
    chosen = []
    seen = set()
    for c in comments:
        if c["id"] in seen or str(c.get("user", {}).get("login", "")).lower() != trusted.lower():
            continue
        h = parse(c.get("body") or "")
        if not h or h.get("status") == "done" or "chief" not in recipient_list(h.get("to", "")):
            continue
        if role_holder(state, c["id"], elected) != me or str(c["id"]) in acked:
            continue
        if c["id"] == recover_id or c["id"] > state.get("last_role", 0):
            seen.add(c["id"])
            chosen.append({**c, "header": h, "role": True})
    if chosen:
        state["last_role"] = max(state.get("last_role", 0), max(c["id"] for c in chosen))
    return chosen


def handback(state: dict, holder: str, message_id: int, restored: str) -> None:
    """The stand-in returns one unacked role message to the restored Chief. Cursor cannot hold or receive it."""
    restored_id = desk_id_for(restored)
    if holder not in CHIEF_DESK_IDS or restored_id is None:
        raise ValueError("Only a Chief-chain holder can hand a role message back, and never to Cursor")
    pending = (state.get("pending") or {}).get(holder, {})
    comment = pending.get(str(message_id))
    assignment = (state.get("assignments") or {}).get(str(message_id)) or {}
    if not comment or assignment.get("holder") != holder or assignment.get("role") != "chief":
        raise ValueError("No chief-role assignment is held by this agent")
    del pending[str(message_id)]
    state.setdefault("pending", {}).setdefault(restored_id, {})[str(message_id)] = comment
    assignment["holder"] = restored_id
    assignment["handed_back_by"] = holder


def classify_message(comment: dict, later: list[dict], state: dict) -> str:
    """Label one candidate. This does not deliver it or move a watermark."""
    mid = str(comment.get("id"))
    for bucket in (state.get("acknowledged") or {}).values():
        if mid in {str(item) for item in bucket}:
            return "acknowledged"
    header = parse(comment.get("body") or "") or comment.get("header") or {}
    if header.get("status") in ("done", "approval"):
        return "terminal"
    for other in later:
        other_header = parse(other.get("body") or "") or {}
        if other_header.get("reply_to") == mid and other_header.get("status") in ("review", "approval", "done", "blocked"):
            return "later-outcome"
    return "unresolved"


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


def refuse_stale_reply(message: dict, snapshot: list[dict], trusted: str) -> None:
    """A Chief-chain reply must explicitly supersede the newest intervening post."""
    if message.get("from") not in CHIEF_DESK_IDS or not message.get("reply_to"):
        return
    reply_to = int(message["reply_to"])
    newer = []
    for comment in snapshot:
        if comment.get("user", {}).get("login", "").lower() != trusted.lower():
            continue
        other = parse(comment.get("body", "")) or {}
        if (other.get("from") in CHIEF_DESK_IDS
                and other.get("film", "") == message.get("film", "")
                and other.get("stage", "") == message.get("stage", "")
                and int(comment["id"]) > reply_to):
            newer.append(int(comment["id"]))
    if newer and message.get("supersedes") != str(max(newer)):
        raise ValueError(f"Stale desk reply to {reply_to}: newest Chief-chain post on this film/stage "
                         f"is {max(newer)}. Read it, then use --supersedes {max(newer)} to override explicitly.")


def cmd_post(ns) -> None:
    r = repo()
    pr = desk_pr(r)
    body = Path(ns.body_file).read_text() if ns.body_file else (ns.body or "")
    if not body.strip():
        sys.exit("Empty message: pass --body or --body-file")
    reply_to = getattr(ns, "reply_to", "")
    supersedes = getattr(ns, "supersedes", "")
    message = parse(header(**{"from": ns.frm, "film": ns.film, "stage": ns.stage,
                              "reply_to": reply_to, "supersedes": supersedes}))
    if ns.frm in CHIEF_DESK_IDS and reply_to:
        trusted = os.environ.get("HOS_DESK_TRUSTED") or r.split("/")[0]
        try:
            refuse_stale_reply(message, comments(r, pr), trusted)
        except ValueError as error:
            sys.exit(str(error))
    urls = push_images(r, ns.film, ns.stage, ns.image) if ns.image else []
    text = compose(ns.frm, ns.to, ns.film, ns.stage, ns.status, body, urls, reply_to, supersedes)
    f = HOME / "outbox.md"
    HOME.mkdir(parents=True, exist_ok=True)
    f.write_text(text)
    print(sh("gh", "pr", "comment", str(pr), "-R", r, "--body-file", str(f)))
    if ns.to == "ben" or ns.status == "approval":
        sh("gh", "pr", "edit", str(pr), "-R", r, "--add-label", NEEDS_BEN)


def load_state() -> dict:
    try:
        return json.loads((HOME / "state.json").read_text())
    except FileNotFoundError:
        return {"last": 0}


def save_state(s: dict) -> None:
    HOME.mkdir(parents=True, exist_ok=True)
    temporary = HOME / "state.json.tmp"
    temporary.write_text(json.dumps(s))
    temporary.replace(HOME / "state.json")


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


from contextlib import contextmanager
import fcntl

@contextmanager
def state_transaction():
    HOME.mkdir(parents=True, exist_ok=True)
    with (HOME / "state.lock").open("a") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        state = load_state()
        yield state
        save_state(state)


def pending_messages(state, incoming, agent):
    pending = state.setdefault("pending", {}).setdefault(agent, {})
    acked = state.get("acknowledged", {}).get(agent, {})
    for comment in incoming:
        if comment.get("header", {}).get("status") == "done":
            continue  # terminal notifications must not create an acknowledgement ping-pong
        if comment.get("role") and agent not in CHIEF_DESK_IDS:
            continue  # Cursor does not take a chief-role copy
        if str(comment["id"]) not in acked:
            pending.setdefault(str(comment["id"]), comment)
            if comment.get("role"):
                state.setdefault("assignments", {}).setdefault(str(comment["id"]), {"role": "chief", "holder": agent})
    return sorted(pending.values(), key=lambda c: c["id"])


def acknowledge(state, agent, message_id, reply, trusted):
    pending = state.get("pending", {}).get(agent, {})
    original = pending.get(str(message_id))
    h = parse(reply.get("body", "")) or {}
    if not original:
        raise ValueError("No pending message for this agent/id")
    source = original["header"]
    if (reply.get("user", {}).get("login", "").lower() != trusted.lower()
            or reply.get("id", 0) <= message_id or h.get("from") != agent
            or h.get("status") not in ("review", "approval", "done", "blocked")
            or h.get("reply_to") != str(message_id)
            or any(h.get(k, "") != source.get(k, "") for k in ("film", "stage"))):
        raise ValueError("Acknowledgement requires a trusted later outcome on the same film/stage, from this agent, with reply_to=<original id>")
    state.setdefault("acknowledged", {}).setdefault(agent, {})[str(message_id)] = reply["id"]
    del pending[str(message_id)]
    (state.get("assignments") or {}).pop(str(message_id), None)


def cmd_ack(ns):
    r = repo()
    replies = comments(r, desk_pr(r))
    reply = next((c for c in replies if c["id"] == ns.ref), None)
    if not reply:
        raise ValueError("Outcome comment is not on the current desk thread")
    with state_transaction() as state:
        acknowledge(state, ns.agent, ns.id, reply, os.environ.get("HOS_DESK_TRUSTED") or r.split("/")[0])
    print(f"Acknowledged {ns.id} with outcome {ns.ref}")


def check_inbox(ns) -> int:
    HOME.mkdir(parents=True, exist_ok=True)
    with (HOME / f"dispatch-{ns.agent}.lock").open("a") as lock:
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            print("Inbox delivery already running for this agent")
            return 0
        return deliver_inbox(ns)


def deliver_inbox(ns) -> int:
    r = repo()
    pr = desk_pr(r)
    trusted = os.environ.get("HOS_DESK_TRUSTED") or r.split("/")[0]
    me = ns.agent
    key = "last" if me == "grok" else f"last_{me}"
    with state_transaction() as state:
        snapshot = comments(r, pr)
        fence = state.setdefault("run_fence", {})
        # Seed EVERY recipient from the same upgrade snapshot, including literal
        # mail above an old watermark and recipients which have never polled.
        if not state.get("literal_snapshot_v2"):
            for recipient in WRITERS:
                historical = for_agent(snapshot, 0, trusted, recipient)
                old_pending = (state.get("pending") or {}).get(recipient, {})
                fence[recipient] = sorted(set(fence.get(recipient, [])) |
                    {str(c["id"]) for c in historical} |
                    {mid for mid, c in old_pending.items() if not c.get("role")})
                watermark = "last" if recipient == "grok" else f"last_{recipient}"
                state[watermark] = max(state.get(watermark, 0), max((c["id"] for c in snapshot), default=0))
            state.setdefault("last_role", max((c["id"] for c in snapshot), default=0))
            state["literal_snapshot_v2"] = True
        recover_id = getattr(ns, "recover_id", None)
        if getattr(ns, "recover_since_id", None) is not None:
            raise ValueError("Bulk recovery is disabled; classify and admit one reviewed --recover-id")
        incoming = for_agent(snapshot, state.get(key, 0), trusted, me)
        if recover_id is not None:
            incoming += [c for c in for_agent(snapshot, 0, trusted, me) if c["id"] == recover_id]
            fence[me] = [mid for mid in fence.get(me, []) if mid != str(recover_id)]
        new = pending_messages(state, incoming, me)
        state[key] = max(state.get(key, 0), max((c["id"] for c in snapshot), default=0))
        fenced = set(fence.get(me, []))
    inbox = HOME / "inbox"
    inbox.mkdir(parents=True, exist_ok=True)
    shown = 0
    for c in new:
        if c.get("role") or str(c["id"]) in fenced:
            continue
        shown += 1
        h = c["header"]
        f = inbox / f"{c['id']}_{h.get('film', 'x')}_{h.get('stage', 'msg')}.md"
        f.write_text(task_text(me, pr, c))
        print(f"\n=== {f}\n{c['body']}")
        if ns.run and worker_may_run(h, me):
            rc = run_agent(f)
            if rc == -1:
                notify(f"Task for {me.title()}: {h.get('film', '')} {h.get('stage', '')}")
            elif rc:
                print(f"agent exited {rc}; message left in {f}")
        # Successful process exit also requires an explicit outcome acknowledgement.
    if not shown:
        print(f"No new messages for {me.title()}.")
    return shown


def task_text(me: str, pr: int, comment: dict) -> str:
    h = comment["header"]
    authority = ""
    if comment.get("role") or "chief" in recipient_list(h.get("to", "")):
        authority = (
            f"This message is for the elected Chief ({me}). Use that identity on the desk. "
            "Cursor does not hold Chief authority and must not decide it.\n\n"
        )
    return (
        f"# Desk task for {me.title()} (PR #{pr}, comment {comment['id']})\n\n"
        + authority
        + "Follow AGENTS.md, then studio/RULES.md (this channel's own rules). When finished, reply on the desk with:\n"
        f"  python3 00_Brand/Channel-Setup/tools/hos_desk.py post --from {me} --to claude --film {h.get('film', '')} "
        f"--stage {h.get('stage', '')} --status review --body-file <report.md> [--image <png/jpg> …]\n\n"
        + comment["body"]
        + f"\n\nThis message remains pending until an outcome is posted. Post the outcome with --reply-to {comment['id']}, "
        f"then run: python3 00_Brand/Channel-Setup/tools/hos_desk.py ack {comment['id']} --as {me} --ref <outcome comment id>\n"
    )


def deliver_role(ns) -> int:
    """Persist chief-role mail for the elected desk id. Never starts the Cursor worker."""
    HOME.mkdir(parents=True, exist_ok=True)
    elected = desk_id_for(getattr(ns, "elected", None)) or resolve_elected()
    me = ns.agent
    if me != elected:
        return 0
    r = repo()
    pr = desk_pr(r)
    trusted = os.environ.get("HOS_DESK_TRUSTED") or r.split("/")[0]
    recover_id = getattr(ns, "recover_id", None)
    with (HOME / f"dispatch-{me}.lock").open("a") as lock:
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            print("Role delivery already running for this agent")
            return 0
        with state_transaction() as state:
            incoming = select_role_messages(comments(r, pr), state, me, elected, trusted, recover_id)
            new = pending_messages(state, incoming, me)
    inbox = HOME / "inbox"
    inbox.mkdir(parents=True, exist_ok=True)
    shown = 0
    for c in new:
        if not c.get("role"):
            continue
        shown += 1
        f = inbox / f"{c['id']}_{c['header'].get('film', 'x')}_{c['header'].get('stage', 'msg')}.md"
        f.write_text(task_text(me, pr, c))
        print(f"\n=== {f}\n{c['body']}")
    if not shown:
        print(f"No new chief-role messages for {me}.")
    return shown


def cmd_inbox(ns) -> None:
    if not ns.watch:
        check_inbox(ns)
        deliver_role(ns)
        return
    HOME.mkdir(parents=True, exist_ok=True)
    marker = HOME / "loaded.json"
    temporary = marker.with_suffix(".tmp")
    temporary.write_text(json.dumps({"pid": os.getpid(), "code": CODE, "sha256": LOADED_SHA256}))
    temporary.replace(marker)
    print(f"HOS desk watcher {CODE} pid={os.getpid()} sha256={LOADED_SHA256}")
    while True:
        try:
            check_inbox(ns)
            elected = resolve_elected()
            if elected:
                deliver_role(argparse.Namespace(agent=elected, elected=elected, run=False, recover_id=None))
        except SystemExit as e:
            print(e)
        except Exception as e:  # keep the watcher alive through network blips
            print(f"inbox error: {e}")
        time.sleep(ns.watch)


def cmd_handback(ns) -> None:
    with state_transaction() as state:
        handback(state, ns.agent, ns.id, ns.to)
    print(f"Handed {ns.id} from {ns.agent} back to {desk_id_for(ns.to)}")


def watcher_pid(target: str) -> int:
    output = subprocess.run(["launchctl", "print", target], text=True, capture_output=True, check=True).stdout
    match = re.search(r"^\s*pid = (\d+)\s*$", output, re.M)
    if not match or int(match[1]) <= 0:
        raise ValueError("Cannot identify running launchd watcher")
    return int(match[1])


def inspect_idle(target: str) -> int:
    pid = watcher_pid(target)
    output = subprocess.run(["ps", "-axo", "pid=,ppid="], text=True, capture_output=True, check=True).stdout
    processes = {}
    for line in output.splitlines():
        child, parent = map(int, line.split())
        processes[child] = parent
    if pid not in processes:
        raise ValueError("Watcher absent from process snapshot")
    descendants = {pid}
    while True:
        expanded = descendants | {child for child, parent in processes.items() if parent in descendants}
        if expanded == descendants:
            break
        descendants = expanded
    if descendants != {pid}:
        raise ValueError("Watcher has active descendants")
    lease = HOME / "execution.json"
    if lease.exists():
        value = json.loads(lease.read_text())
        if not isinstance(value, dict) or not isinstance(value.get("pid"), int) or value["pid"] <= 0:
            raise ValueError("Invalid desk execution lease")
        lease_pid = value["pid"]
        if lease_pid in processes:
            raise ValueError("Desk execution lease is active")
    return pid


def cmd_refresh(ns) -> None:
    """Inspect the OS boundary while holding every dispatch lock, or fail closed.

    Locks span kickstart and loaded-process confirmation, preventing a new
    dispatch in the inspection/restart gap (also for the pre-upgrade watcher).
    """
    from contextlib import ExitStack
    installed_path = Path(os.environ.get("HOS_DESK_INSTALLED",
        "/Users/benjaminoats/YouTube/History Of Science/00_Brand/Channel-Setup/tools/hos_desk.py"))
    target = f"gui/{os.getuid()}/com.hos.desk"
    HOME.mkdir(parents=True, exist_ok=True)
    try:
        if hashlib.sha256(installed_path.read_bytes()).hexdigest() != LOADED_SHA256:
            raise ValueError("Installed source differs from this loaded code")
        with ExitStack() as stack:
            # Serialise refreshers too; lock order is fixed across all callers.
            for name in ["refresh", *[f"dispatch-{agent}" for agent in sorted(WRITERS)]]:
                lock = stack.enter_context((HOME / f"{name}.lock").open("a"))
                fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
            old_pid = inspect_idle(target)
            print(f"decision=refresh code={CODE} pid={old_pid} sha256={LOADED_SHA256}")
            if not getattr(ns, "apply", False):
                return
            if inspect_idle(target) != old_pid:
                raise ValueError("Watcher changed during inspection")
            subprocess.run(["launchctl", "kickstart", "-k", target], check=True)
            for attempt in range(50):
                new_pid = watcher_pid(target)
                try:
                    loaded = json.loads((HOME / "loaded.json").read_text())
                except (OSError, ValueError):
                    loaded = {}
                if (new_pid != old_pid and loaded.get("pid") == new_pid
                        and loaded.get("code") == CODE and loaded.get("sha256") == LOADED_SHA256):
                    evidence = {"old_pid": old_pid, **loaded, "confirmed_at": datetime.now(timezone.utc).isoformat()}
                    (HOME / "refresh-result.json").write_text(json.dumps(evidence))
                    print(json.dumps(evidence))
                    return
                time.sleep(0.1)
            raise ValueError("Restart requested but loaded PID/version was not confirmed; inspect launchd before retry")
    except (OSError, ValueError, subprocess.SubprocessError) as error:
        raise SystemExit(f"Refresh refused or unconfirmed: {error}")


def cmd_thread(ns) -> None:
    r = repo()
    for c in comments(r, desk_pr(r))[-ns.last:]:
        h = parse(c["body"]) or {"from": "ben"}
        print(f"\n--- {c['created_at']} {h.get('from')}→{h.get('to', 'all')} {h.get('film', '')} {h.get('stage', '')}")
        print(HEADER.sub("", c["body"]).strip())


def party_list(value: str) -> str:
    parts = recipient_list(value)
    bad = [p for p in parts if p not in PARTIES]
    if not parts or bad:
        raise argparse.ArgumentTypeError("unknown desk party: " + (", ".join(bad) or value))
    return ",".join(parts)


def main() -> None:
    # launchd writes stdout to a file; without line buffering watch.log stays empty.
    sys.stdout.reconfigure(line_buffering=True)
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("init").set_defaults(fn=cmd_init)
    p = sub.add_parser("post")
    p.add_argument("--from", dest="frm", choices=SENDERS, default="grok")
    p.add_argument("--to", type=party_list, required=True)
    p.add_argument("--film", default="")
    p.add_argument("--stage", default="")
    p.add_argument("--status", choices=STATUSES, default="review")
    p.add_argument("--body")
    p.add_argument("--body-file")
    p.add_argument("--image", action="append", default=[])
    p.add_argument("--reply-to", type=int, help="original desk message id this outcome resolves")
    p.add_argument("--supersedes", type=int, help="newest Chief-chain post explicitly superseded by this reply")
    p.set_defaults(fn=cmd_post)
    p = sub.add_parser("inbox")
    p.add_argument("--watch", type=int, default=0, help="poll every N seconds")
    p.add_argument("--run", action="store_true", help="start the agent with $HOS_DESK_AGENT_CMD")
    p.add_argument("--as", dest="agent", choices=WRITERS, default="grok", help="whose inbox (cursor or codex while Grok is out)")
    p.add_argument("--recover-since-id", type=int, help="disabled: bulk replay is unsafe; use reviewed --recover-id")
    p.add_argument("--recover-id", type=int, help="admit one reviewed unresolved message by id; never rewinds watermarks")
    p.set_defaults(fn=cmd_inbox)
    p = sub.add_parser("handback")
    p.add_argument("id", type=int)
    p.add_argument("--as", dest="agent", choices=CHIEF_DESK_IDS, required=True)
    p.add_argument("--to", dest="to", choices=CHIEF_DESK_IDS, required=True)
    p.set_defaults(fn=cmd_handback)
    p = sub.add_parser("refresh")
    p.add_argument("--apply", action="store_true", help="restart only after OS idle checks and dispatch locks; Chief authorisation required")
    p.set_defaults(fn=cmd_refresh)
    p = sub.add_parser("ack")
    p.add_argument("id", type=int)
    p.add_argument("--as", dest="agent", choices=WRITERS, required=True)
    p.add_argument("--ref", type=int, required=True, help="posted outcome comment id on this desk")
    p.set_defaults(fn=cmd_ack)
    p = sub.add_parser("thread")
    p.add_argument("--last", type=int, default=10)
    p.set_defaults(fn=cmd_thread)
    ns = ap.parse_args()
    ns.fn(ns)


if __name__ == "__main__":
    main()
