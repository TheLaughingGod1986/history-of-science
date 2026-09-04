# HOS 001 Germs — full audit (4 Sep 2026 ~15:20 London)

**Channel:** History of Science (`UCXp7HkBIl1LgaznXuZHJyRg` · `@HistoryOfScienceYT`)  
**Scope:** long `_C92tIJCk8A` + Shorts cluster · SEO · technical · content · housekeeping  
**Do not:** remint · Data API `thumbnails.set` · `/go/` on Shorts · Orbit / Oppti

## Verdict

**Ship is healthy.** No critical content or SEO breaks on public assets. Remaining work is Studio-login-gated polish (pin funnel comment on live Short; confirm Scheduled Shorts in HOS Studio UI).

| Area | Status |
|---|---|
| Long public + playable | PASS |
| Short s01 public (Fri 11:30) | PASS |
| Shorts s02–s05 still scheduled (not missing) | PASS (private to cold clients until publishAt) |
| Zero `/go/` / Amazon on public listings | PASS |
| Parent funnel link on live Short | PASS |
| Chapters on long | PASS |
| Auto-captions EN present (long + s01) | PASS |
| Related / pin / cover confirm in Studio today | BLOCKED — Chrome session on Orbit With Ben; HOS Studio returns permission Oops |

## Live public snapshot (yt-dlp / watch page)

### Long `_C92tIJCk8A`
- **Title:** How Did We Discover Germs?
- **Visibility:** public · **Duration:** 365s · **Views at audit:** 1
- **Channel:** History of Science
- **Description:** cold-open hook · story beats · chapters · brand line · `#HistoryOfScience #GermTheory #Science`
- **Chapters:** 0:00 / 1:20 / 2:37 / 3:48 / 5:10 — present
- **Keywords meta:** germ theory, Pasteur, Lister, Semmelweis, swan neck flask, history of science, …
- **Affiliate:** none
- **Captions:** English auto present; spot-check reads clean (Semmelweis / Pasteur / Lister intact)

### Short s01 `8uBR-9oxeWs` (live today)
- **Title:** Germs don't cast a shadow
- **Visibility:** public · **Duration:** 26s · **Views at audit:** ~4–8
- **Description:** punch line · **Watch the full film** → `_C92tIJCk8A` · hashtags including `#Shorts`
- **Affiliate:** none · **Parent link:** yes
- **Captions:** EN auto present (sparse — music-heavy open; acceptable for punch Short)

### Shorts s02–s05

| ID | Slot | Expected London | Cold client |
|---|---|---|---|
| `YX2UR1u-JCQ` | s02 pond | Sat 5 Sep 11:30 | private until publishAt |
| `Fnb3p81u-wY` | s03 vector | Sun 6 Sep 11:30 | private until publishAt |
| `vpuRgKXtFlY` | s04 flask | Mon 7 Sep 11:30 | private until publishAt |
| `Lcmh5y2KMQM` | s05 soap | Tue 8 Sep 11:30 | private until publishAt |

Prior Studio checks (3 Sep evening) confirmed all five **Scheduled** on HOS Shorts tab with Related → long. They are not deleted.

## SEO checklist

| Check | Long | Live Short | Notes |
|---|---|---|---|
| Primary promise in title | PASS | PASS | Question title matches lock |
| Hook in first ~100 chars | PASS | PASS | |
| Chapters | PASS | n/a | |
| Hashtags | PASS | PASS | 3–5 |
| Tags / keywords dense | PASS | PASS | VidIQ pass logged 2 Sep |
| Exact parent title + URL on Short | n/a | PASS | |
| Zero `/go/` | PASS | PASS | |
| Category Education / EN-GB | PASS (2 Sep Studio) | PASS (2 Sep) | Re-confirm when HOS Studio opens |
| Thumbnail ABC | Running (3 Sep evening) | n/a | Title locked; Thumbnail only |
| Pin funnel comment | unknown | **TODO** | Studio pin once public — do on phone tonight |

## Content / technical

- **No remint needed.** Parents + full v02 stay locked.
- **No listing errors** on public long/Short (no Orbit branding, no affiliate, no wrong film URL).
- **Mobile Studio empty Shorts list** = Videos/Public filter (see prior note). Use Shorts tab or Visibility → Scheduled / All.
- **s01 auto-caption** is thin; optional later: upload a cleaned EN .srt if Ben wants tighter accessibility. Not blocking.

## Housekeeping applied in repo

- Refresh `production-status.md` (s01 public · ABC running · correct Short ids)
- Align `PACKAGE_MANIFEST.json` privacy with live Public long
- Align `RELEASE_WEEK_001.md` Short titles to locked listings
- Record this audit + public SEO scrape JSON

## Remaining (needs HOS Studio / phone)

1. **Pin** on `8uBR-9oxeWs`:
   ```
   Full film — How Did We Discover Germs?:
   https://www.youtube.com/watch?v=_C92tIJCk8A
   ```
2. After each later Short goes public (Sat–Tue 11:30): same pin.
3. In HOS Studio: glance Related still set on s02–s05; End screen on long → Subscribe + next film when one exists.
4. Optional: publish cleaned EN captions on long if auto-caption drifts.

## Evidence

- `PUBLIC_SEO_SCRAPE_2026-09-04.json`
- `STUDIO_AUDIT_SHORTS_2026-09-03_v02.json`
