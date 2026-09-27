#!/usr/bin/env python3
"""Public competition check — YouTube autocomplete + top search results, no login.

Written 27 Sep 2026 from the HOS 004 audit (STUDIO_PLAYBOOK.md §2). Use it for the
signed-out competition check on every title, and as the keyword section of the pre-build
audit when vidIQ is waived. It does not give search volumes; vidIQ does.

For each phrase it records:
  - whether YouTube autocomplete suggests it (people really type it), and the suggestions;
  - the top results in GB search: title, channel, views, age, length.

Usage
  python3 public_search.py "why is the periodic table in this order" "henry moseley" \
      --out 02_Video-Projects/<NNN_Slug>/11_Upload-Package/evidence_<date>_public_search.json

Prints a markdown table (paste into the audit) and writes the raw pull to --out.
Read it like the playbook: if the top five for the exact title are all channels with
millions of subscribers, narrow the angle.
"""
from __future__ import annotations

import argparse
import json
import re
import urllib.parse
import urllib.request
from datetime import date
from pathlib import Path

UA = {"User-Agent": "Mozilla/5.0", "Accept-Language": "en-GB"}


def get(url: str) -> str:
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60) as r:
        return r.read().decode("utf-8", "replace")


def walk(o, key):
    if isinstance(o, dict):
        if key in o:
            yield o[key]
        for v in o.values():
            yield from walk(v, key)
    elif isinstance(o, list):
        for v in o:
            yield from walk(v, key)


def suggest(q: str) -> list[str]:
    url = ("https://suggestqueries.google.com/complete/search?client=firefox&ds=yt&hl=en-GB&gl=GB&q="
           + urllib.parse.quote(q))
    try:
        return json.loads(get(url))[1]
    except Exception:
        return []


def text(o) -> str:
    return o.get("simpleText") or "".join(r.get("text", "") for r in o.get("runs", []))


def search(q: str, n: int) -> list[dict]:
    html = get("https://www.youtube.com/results?hl=en-GB&gl=GB&search_query=" + urllib.parse.quote(q))
    m = re.search(r"var ytInitialData = (\{.*?\});</script>", html, re.S)
    if not m:
        raise RuntimeError("ytInitialData not found — YouTube page layout changed")
    out = []
    for v in walk(json.loads(m.group(1)), "videoRenderer"):
        out.append({"id": v.get("videoId"), "title": text(v.get("title", {})), "channel": text(v.get("ownerText", {})),
                    "views": text(v.get("viewCountText", {})), "age": text(v.get("publishedTimeText", {})),
                    "length": text(v.get("lengthText", {}))})
        if len(out) >= n:
            break
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("phrases", nargs="+")
    ap.add_argument("--top", type=int, default=8)
    ap.add_argument("--out", type=Path, default=None)
    ns = ap.parse_args()

    pull = {"pulled": date.today().isoformat(),
            "source": "YouTube GB search results and autocomplete; public, no login. Not vidIQ.", "queries": {}}
    print("| Phrase | Autocomplete? | Top results (GB) |")
    print("|---|---|---|")
    for q in ns.phrases:
        sug = suggest(q)
        res = search(q, ns.top)
        pull["queries"][q] = {"suggest": sug, "search": res}
        typed = "yes" if any(s.lower() == q.lower() for s in sug) else ("related: " + "; ".join(sug[:3]) if sug else "no")
        top = " · ".join(f"{r['channel']} {r['views'].replace(' views', '')}" for r in res[:5])
        print(f"| {q} | {typed} | {top} |")
    if ns.out:
        ns.out.parent.mkdir(parents=True, exist_ok=True)
        ns.out.write_text(json.dumps(pull, indent=1, ensure_ascii=False) + "\n")
        print(f"\nRaw pull: {ns.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
