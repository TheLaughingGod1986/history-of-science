#!/usr/bin/env python3
"""Scaffold a vidIQ title-score checklist for an Orbit episode.

Does not call vidIQ (login / extension required). Writes a score sheet you fill
while scoring ABC titles in app.vidiq.com (Title Analyzer / Keyword Research /
Thumbnail Preview).

Examples:
  python3 vidiq_title_score_sheet.py \\
    --project-dir ../../02_Video-Projects/004_JWST-Discoveries-That-Change-Everything

  python3 vidiq_title_score_sheet.py --project-dir … --titles-file …/Titles/jwst_title_abc_v01.txt
"""
from __future__ import annotations

import argparse
import json
import re
from datetime import date
from pathlib import Path

BRAND_SUFFIX = "Orbit's Cosmic Journey"


def clean_title(raw: str) -> str | None:
    t = " ".join(raw.split()).strip()
    t = re.sub(r"\*+", "", t)
    t = t.replace("\\|", "|").replace("\\ |", " |")
    t = re.sub(r"\s*\\\s*\|\s*", " | ", t)
    t = re.sub(r"\s*\|\s*", " | ", t)
    t = re.sub(r"\s{2,}", " ", t).strip(" |-\\")
    # Drop legend / meta prefixes
    t = re.sub(
        r"^(?:locked title(?:\s*\([^)]*\))?|primary title|working title|seo title|"
        r"title\s*\(vidiq[^)]*\)|alt titles?)\s*[:—\-]\s*",
        "",
        t,
        flags=re.I,
    ).strip()
    t = re.sub(r"\s*\*\([^)]*\)\*", "", t).strip()
    t = re.sub(r"\s*\((?:Short/?thumb|thumb|alt|lock[^)]*)\)\s*$", "", t, flags=re.I).strip()
    if len(t) < 20 or len(t) > 140:
        return None
    if t.lower() in {"a", "b", "c"}:
        return None
    if not re.search(r"[A-Za-z]{4,}", t):
        return None
    if BRAND_SUFFIX.lower() not in t.lower() and "orbit" not in t.lower():
        t = f"{t} | {BRAND_SUFFIX}"
    # Collapse duplicate brand suffixes
    t = re.sub(
        rf"(\s*\|\s*{re.escape(BRAND_SUFFIX)})+$",
        f" | {BRAND_SUFFIX}",
        t,
        flags=re.I,
    )
    return t


def titles_from_abc_file(path: Path) -> list[str]:
    """Parse A/B/C blocks like jwst_title_abc_v01.txt."""
    text = path.read_text(encoding="utf-8", errors="ignore").replace("\\|", "|")
    found: list[str] = []
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if re.match(r"^[ABC]\s*[—\-–:]", line, re.I) or re.match(r"^[ABC]\s*$", line, re.I):
            same = re.sub(r"^[ABC]\s*[—\-–:]\s*", "", line, flags=re.I).strip()
            same = re.sub(
                r"^(?:LOCK(?:\s*\([^)]*\))?|thumb.*|alt.*|production.*)$",
                "",
                same,
                flags=re.I,
            ).strip()
            candidate = same
            if not candidate or len(candidate) < 20:
                j = i + 1
                while j < len(lines) and not lines[j].strip():
                    j += 1
                if j < len(lines):
                    nxt = lines[j].strip()
                    if not re.match(r"^(?:Rejected|##|#)", nxt, re.I):
                        candidate = nxt
                        i = j
            ct = clean_title(candidate)
            if ct:
                found.append(ct)
        i += 1
    return found


def titles_from_script_header(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8", errors="ignore").replace("\\|", "|")
    head = text.split("\n---\n", 1)[0]
    found: list[str] = []
    for m in re.finditer(r"^[-*]\s*[ABC]\s*:\s*(.+)$", head, re.I | re.M):
        ct = clean_title(m.group(1))
        if ct:
            found.append(ct)
    for m in re.finditer(
        r"\*\*(?:Working title|SEO title|Primary title)[^*]*\*\*\s*:\s*(.+)$",
        head,
        re.I | re.M,
    ):
        ct = clean_title(m.group(1))
        if ct:
            found.insert(0, ct)
    return found


def titles_from_ranking(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8", errors="ignore").replace("\\|", "|")
    found: list[str] = []
    for m in re.finditer(
        r"\|\s*\*\*[ABC][^*]*\*\*\s*\|\s*([^|]+)\|", text
    ):
        ct = clean_title(m.group(1))
        if ct:
            found.append(ct)
    return found


def discover_titles(project: Path, titles_file: Path | None) -> list[str]:
    ordered: list[str] = []
    seen: set[str] = set()

    def add_many(items: list[str]) -> None:
        for t in items:
            key = t.lower()
            if key in seen:
                continue
            seen.add(key)
            ordered.append(t)

    if titles_file and titles_file.is_file():
        add_many(titles_from_abc_file(titles_file))

    titles_dir = project / "11_Upload-Package" / "Titles"
    if titles_dir.is_dir():
        for path in sorted(titles_dir.glob("*")):
            if path.name.startswith("VIDIQ_"):
                continue
            if path.suffix.lower() in {".txt", ".md"}:
                add_many(titles_from_abc_file(path))

    for path in sorted((project / "11_Upload-Package").glob("RANKING*.md")):
        add_many(titles_from_ranking(path))

    for path in sorted((project / "01_Script").glob("*script_master*.md")):
        add_many(titles_from_script_header(path))

    return ordered[:5]


def project_slug(project: Path) -> str:
    name = project.name
    m = re.match(r"\d+_(.+)", name)
    return (m.group(1) if m else name).lower().replace("_", "-")


def render_sheet(project: Path, titles: list[str]) -> str:
    slug = project_slug(project)
    today = date.today().isoformat()
    rows = []
    letters = "ABCDE"
    for i, t in enumerate(titles):
        letter = letters[i] if i < len(letters) else str(i + 1)
        rows.append(f"| **{letter}** | {t} |  |  |  |  |")

    if not rows:
        rows = [
            f"| **A** |  |  |  |  |  |",
            f"| **B** |  |  |  |  |  |",
            f"| **C** |  |  |  |  |  |",
        ]

    return f"""# vidIQ title score sheet — {project.name}

**Date:** {today}  
**Project:** `{project}`  
**Gate:** Do **not** lock VO until one title scores **≥90** (target **95+** like V001/V003).  
**Session:** Log into [app.vidiq.com](https://app.vidiq.com) on the **automation / research** profile (not the login wall).

## Score ABC

| | Title | vidIQ score | Search vol note | Competition | Keep? |
|---|-------|-------------|-----------------|-------------|-------|
{chr(10).join(rows)}

## Checklist (run in order)

- [ ] **Keyword Research** — confirm primary keyword volume + related terms for description/tags
- [ ] **Title Analyzer** — score A/B/C (paste full title including `| {BRAND_SUFFIX}`)
- [ ] **Thumbnail Preview** — pair top title with thumb ABC; check mobile + suggested feed
- [ ] **Outliers / Daily Ideas** *(optional)* — note 1–2 competing angles to avoid
- [ ] Lock winner into `11_Upload-Package/Titles/` + `RANKING_STRATEGY` / production-status
- [ ] Update `VIDEO_BACKLOG.json` title if changed

## Keyword stack (fill from vidIQ)

| Keyword | Role (title / desc / tags / Shorts) | Volume | Comp |
|---------|--------------------------------------|--------|------|
|  | primary |  |  |
|  | secondary |  |  |
|  | umbrella |  |  |

## Decision

**Locked title:**  
**vidIQ score:**  
**Why it wins:**  

## Tools reference

- Title Analyzer / Generator: https://app.vidiq.com/tools/title-generator  
- Keyword Research: https://app.vidiq.com/keyword  
- Free toolkit: https://vidiq.com/free-youtube-tools/  

Regen this sheet:

```bash
python3 04_Audio/tools/vidiq_title_score_sheet.py --project-dir {project}
```

Slug hint: `{slug}`
"""


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--project-dir", type=Path, required=True)
    ap.add_argument("--titles-file", type=Path, default=None)
    ap.add_argument(
        "--out",
        type=Path,
        default=None,
        help="Default: <project>/11_Upload-Package/Titles/VIDIQ_TITLE_SCORE_SHEET.md",
    )
    args = ap.parse_args()

    project = args.project_dir.expanduser().resolve()
    if not project.is_dir():
        raise SystemExit(f"Project dir not found: {project}")

    titles = discover_titles(
        project,
        args.titles_file.expanduser().resolve() if args.titles_file else None,
    )
    sheet = render_sheet(project, titles)

    out = (
        args.out.expanduser().resolve()
        if args.out
        else project / "11_Upload-Package" / "Titles" / "VIDIQ_TITLE_SCORE_SHEET.md"
    )
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(sheet, encoding="utf-8")

    meta = {
        "project": str(project),
        "titles_discovered": titles,
        "out": str(out),
    }
    meta_path = out.with_suffix(".json")
    meta_path.write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {out}")
    print(f"Discovered {len(titles)} title candidates")
    for t in titles:
        print(f"  - {t}")


if __name__ == "__main__":
    main()
