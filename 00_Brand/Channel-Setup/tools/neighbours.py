#!/usr/bin/env python3
"""Neighbour check — which big education videos should YouTube suggest our film next to?

Written 1 Oct 2026 from HOS 002's analytics: 108 of its 126 views came from "suggested",
55.6% of them from TED-Ed's "The genius of Mendeleev's periodic table", the rest from school
lessons (Khan Academy, Grade 7 Science). A film gets daily views when it sits next to a big,
evergreen lesson on the same subject and uses the same words. This finds those lessons.

For a topic it searches YouTube GB (signed out, no login) for the phrases, plus TED-Ed, TED
and Khan Academy versions of them, keeps only videos from known education channels, and
ranks TED-Ed/TED first, then views.

Usage
  python3 neighbours.py "periodic table" "mendeleev" \
      --out 02_Video-Projects/<NNN_Slug>/11_Upload-Package/evidence_<date>_neighbours.json
  # write the contract block into the film's manifest (phrases = the words the title,
  # description and tags must share with the neighbours):
  python3 neighbours.py "atom" "rutherford gold foil" --phrase atom --phrase atomic \
      --manifest 02_Video-Projects/004_*/11_Upload-Package/PACKAGE_MANIFEST.json

The topic gate (STUDIO_PLAYBOOK.md §2): at least one neighbour with 1M+ views, TED-Ed or TED
preferred. `npm run lint:package` then checks the manifest's `neighbours` block.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import time
from collections import Counter
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from public_search import search, suggest  # noqa: E402

# Tier 1 is what Ben wants us next to; tier 2 is the school-lesson layer that also feeds 002.
TIER1 = {"TED-Ed", "TED", "TEDx Talks"}
TIER2 = {
    "Khan Academy", "CrashCourse", "SciShow", "Veritasium", "Kurzgesagt – In a Nutshell",
    "Kurzgesagt - In a Nutshell", "FuseSchool - Global Education", "Free Science Lessons", "Cognito",
    "Amoeba Sisters", "The Royal Institution", "BBC Ideas", "BBC Teach", "Science History Institute",
    "Periodic Videos", "minutephysics", "MinuteEarth", "PBS Space Time", "Be Smart", "SmarterEveryDay",
    "Real Engineering", "Tom Scott", "Vsauce", "Primer", "3Blue1Brown", "Sabine Hossenfelder", "SciShow Kids",
    "National Geographic", "Natural History Museum", "Science Museum", "Royal Society of Chemistry",
    "The Science Asylum", "Lessons from the Past", "History of Everything", "Tibees", "Up and Atom",
    "Physics Girl", "Thoughty2", "Kings and Generals", "Oversimplified", "Extra History", "Simple History",
}
MIN_NEIGHBOUR_VIEWS = 1_000_000


def views(s: str) -> int:
    s = s.replace(",", "").lower()
    m = re.search(r"([\d.]+)\s*([km]?)", s)
    if not m:
        return 0
    n = float(m.group(1))
    return int(n * {"k": 1e3, "m": 1e6}.get(m.group(2), 1) if "bn" not in s else n * 1e9)


def tier(channel: str) -> int:
    return 1 if channel in TIER1 else 2 if channel in TIER2 else 0


STOP = {"the", "and", "how", "did", "what", "why", "who", "inside", "really", "discover", "discovery", "history", "theory"}


def relevant(title: str, phrases: list[str]) -> bool:
    """On the subject: the title holds a topic phrase or one of its key words (4+ letters)."""
    t = title.lower()
    keys = {w for p in phrases for w in re.findall(r"[a-z]{4,}", p.lower()) if w not in STOP}
    return any(p.lower() in t for p in phrases) or any(re.search(rf"\b{re.escape(k)}", t) for k in keys)


def queries(phrases: list[str]) -> list[str]:
    out = []
    for p in phrases:
        out += [p, f"ted-ed {p}", f"{p} ted", f"khan academy {p}"]
    return out


def search_retry(q: str, top: int, tries: int = 3) -> list[dict]:
    for i in range(tries):
        try:
            return search(q, top)
        except Exception:
            if i == tries - 1:
                raise
            time.sleep(2 * (i + 1))
    return []


def find(phrases: list[str], top: int = 20) -> dict:
    seen: dict[str, dict] = {}
    failed: list[str] = []
    for q in queries(phrases):
        try:
            results = search_retry(q, top)
        except Exception:
            failed.append(q)
            continue
        for r in results:
            t = tier(r["channel"])
            if not r.get("id") or not t or r["id"] in seen:
                continue
            seen[r["id"]] = {**r, "tier": t, "viewCount": views(r["views"]), "foundBy": q,
                             "onTopic": relevant(r["title"], phrases)}
    ranked = sorted((r for r in seen.values() if r["onTopic"]), key=lambda r: (0 if r["tier"] == 1 and r["viewCount"] >= 100_000 else 1, -r["viewCount"]))
    words = Counter()
    for r in ranked[:10]:
        toks = re.findall(r"[a-z']+", r["title"].lower())
        words.update(" ".join(toks[i:i + 2]) for i in range(len(toks) - 1))
    shared = [w for w, n in words.most_common(10) if n >= 2]
    return {
        "pulled": date.today().isoformat(),
        "source": "YouTube GB search (signed out) filtered to education channels; not vidIQ.",
        "phrases": phrases,
        "autocomplete": {p: suggest(p) for p in phrases},
        "sharedTitleWords": shared,
        "neighbours": ranked,
        "gate": "PASS" if any(r["viewCount"] >= MIN_NEIGHBOUR_VIEWS for r in ranked) else "FAIL",
        "hasTed": any(r["tier"] == 1 for r in ranked),
        "failedQueries": failed,
    }


def write_manifest(path: Path, pull: dict, phrases: list[str], n: int = 5) -> None:
    m = json.loads(path.read_text())
    m["neighbours"] = {
        "phrases": phrases,
        "checked": pull["pulled"],
        "videos": [
            {"id": r["id"], "channel": r["channel"], "title": r["title"], "views": r["viewCount"]}
            for r in pull["neighbours"][:n]
        ],
    }
    path.write_text(json.dumps(m, indent=2, ensure_ascii=False) + "\n")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("topics", nargs="+", help="subject phrases, e.g. 'periodic table' 'mendeleev'")
    ap.add_argument("--phrase", action="append", default=[],
                    help="contract phrase the title/description/tags must contain (repeatable)")
    ap.add_argument("--top", type=int, default=20)
    ap.add_argument("--out", type=Path)
    ap.add_argument("--manifest", type=Path, help="write the neighbours block into this PACKAGE_MANIFEST.json")
    ns = ap.parse_args()

    pull = find(ns.topics, ns.top)
    print("| # | Channel | Views | Title | Found by |")
    print("|---|---|---|---|---|")
    for i, r in enumerate(pull["neighbours"][:12], 1):
        star = " ★" if r["tier"] == 1 else ""
        print(f"| {i} | {r['channel']}{star} | {r['views']} | [{r['title']}](https://youtu.be/{r['id']}) | {r['foundBy']} |")
    print(f"\nWords the top neighbours share: {', '.join(pull['sharedTitleWords']) or '—'}")
    print(f"TED-Ed/TED neighbour: {'yes' if pull['hasTed'] else 'NO'}")
    if pull["failedQueries"]:
        print(f"Queries YouTube refused (re-run later): {'; '.join(pull['failedQueries'])}")
    print(f"Neighbour gate (one education video ≥ {MIN_NEIGHBOUR_VIEWS:,} views): {pull['gate']}")
    if ns.out:
        ns.out.parent.mkdir(parents=True, exist_ok=True)
        ns.out.write_text(json.dumps(pull, indent=1, ensure_ascii=False) + "\n")
        print(f"Raw pull: {ns.out}")
    if ns.manifest:
        if not ns.phrase:
            ap.error("--manifest needs at least one --phrase (the words the title must share)")
        write_manifest(ns.manifest, pull, ns.phrase)
        print(f"Wrote neighbours block to {ns.manifest}")
    return 0 if pull["gate"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
