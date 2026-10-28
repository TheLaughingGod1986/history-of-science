# J1107 evidence checkpoint — 28 October 2026

Worker: codex. This is an unfinished audit, not Chief approval. No YouTube, thumbnail, title, test, schedule, privacy, or paid-credit changes were made.

The report lives in OWB `05_Analytics/weekly_thumb_audit/HOS/2026-10-28.md`.

## Evidence

- `inventory_api.json`: authenticated read-only Data API inventory, verified against HOS channel ID; 58 known uploads, 40 public/scheduled. Includes 26 public and 14 scheduled. Private unscheduled uploads excluded from the audit table.
- `thumbnail_manifest.json`: all 40 served thumbnail URLs, SHA256 and persistent local copies under `/Users/benjaminoats/_desk/J1107/2026-10-28/`. Media stays outside git.
- `assessment.json`: individual advisory cover-style scores for all 40, rule references, test state, date and metrics. PASS means that limited cover rubric, never a film-stage or Chief PASS. `briefQuestionTitle` separately records the job brief's question requirement; historic HOS examples permit statements, so these are review flags, not authority to retitle.
- `metrics_28days.json`: 30 September–27 October, Studio Advanced mode. Numeric rows for 25 videos; missing rows remain unavailable. Long median 2.3%, Short median 1.6%. Only one Short has 1,000+ impressions; zero longs. Do not infer a reliable bottom quartile from one video.
- `studio_advanced_28days.txt`: raw Studio table. Table rows sum to 4,784 impressions while channel total is 4,795; 11 impressions are not attributable from the visible rows. No allocation was invented.
- `studio_*_28days.txt`: individual page read-backs. Shorts redirect to their overview and do not expose the long-form Reach funnel. Long engaged views from impressions are recorded; the equivalent Shorts count is unavailable, not inferred from rounded CTR.
- `analytics_probe.json`: read-only Analytics API supports the views query but rejects these thumbnail-metric queries. Studio was the fallback. API period is 29 September–26 October; do not mix those views with the Studio 28-day table.
- `frame0_manifest.json`: 13 local registered opening frames extracted, 19 media paths missing/unregistered. Eleven source hashes match the registry; John Snow `OnJ8MFu0Mi0` and infrared `c2q7w0pgcn8` do not match, so their opening evidence is not accepted as the registered upload. These are local-file evidence, not proof of pixel identity with YouTube. Motion and first spoken line still need checking.
- `competitors.json`: five requested reference channels; 90-day public listings with separate long/Short fastest and slowest selections by views/day. Low-count cohorts necessarily overlap; never claim independent ten-video tails where fewer than 20 exist. Missing view counts excluded. The oldest fetched upload in every capped listing precedes the cutoff. Veritasium sample still needs history-piece filtering.
- `competitor_thumbnail_manifest.json`: selected competitor thumbnail copies and hashes. `competitor_coding.json` contains OCR and measured luma/contrast; manual text correction, subject, text size/colour, composition, curiosity gap and hook coding are explicitly pending.
- `search_neighbours.json`: five signed-out public search results for each of eight long titles. These reveal six additional relevant channels; the neighbour sample is separate and still needs analysis.

## Six-step continuation plan

1. Inventory and served thumbnail copies — done.
2. Performance collection and test-state checks — collected with explicit missing-data limitations above; scheduled test configuration and compilation state need final verification before design/arming.
3. Complete visual audit — cover scores drafted for all 40; finish opening motion/line checks, resolve unavailable local media, validate the served cover on Studio/mobile surfaces.
4. Complete competitor study — review/complete manual coding, separate history pieces, analyse newly found neighbours, and write supported contrasts with cohort/sample caveats.
5. Select eligible designs, make Bs/title proposals, run the packaging panel, apply agreed feedback. Check existing jobs first; no parallel replacement of already-queued thumbnail work. Never overwrite an active/prearmed test. Queue gated Studio jobs only after concrete assets exist; Chief approves before arming.
6. Verify deliverables, submit final report to Chief, record test ledger proposals, park for Chief review.

## Reproduction

Python: `/opt/homebrew/opt/python@3.14/bin/python3.14` (the HOS shell's default Python lacks Pillow).
`collect.py`, `competitors.py`, `search_neighbours.py`, `frame0.py`, `sheets.py`, `competitor_sheets.py`, `code_competitors.py`, `assess.py` are audit helpers. API helpers read the existing read-only HOS tracker token; never persist/print credentials. Their paths currently identify this Mac mini and audit date. Do not run collectors blindly over this fixed checkpoint; use a new date directory for a later audit.

Forty per-video house previews were made with HOS `thumb_preview.py`. All media, contact sheets and full metadata are retained under `_desk/J1107`, never under ephemeral `/tmp` alone.

J1113 changed ten scheduled HOS covers to frame-zero hooks today (OWB PR #320), awaiting Chief review. Those recent authorized changes override a routine suggestion to restore old custom covers; reconcile saved Studio state and cached served thumbnails first.
