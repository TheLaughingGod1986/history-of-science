# J1107 checkpoint — not complete, not a Chief approval

Worker: codex. Five-step plan; only step 1 complete. All image copies and collectors: `/Users/benjaminoats/_desk/j1107/`.

The 40 live/scheduled records comprise 8 longs and 32 Shorts. API Short images are not verified custom covers or first frames (see style/README.md); do not score those as the cover or opening. Long style scores are worker advice only. Phone sheets use the HOS thumb_preview.py; the separate `scores.json` contains OWB diagnostics only, not HOS thresholds.

Studio exact window: 30 Sep–27 Oct 2026, 25 rows. Long median CTR 2.3% (4 rows), Short median 1.6% (21 rows), unweighted and including displayed zeroes. No long reaches 1,000 impressions. One Short does: 29bpGAI0wb8, 1,121 and 0.9%; a one-item eligible set cannot support a meaningful bottom quartile. Missing records are UNKNOWN, not zero. Views from impressions were not present in this view; never substitute total views or calculate an exact count from rounded CTR. The API requests returned 400 and are retained for evidence.

Tests: Studio shows Running for Germs, X-rays AND Atom. Atom is absent from the HOS rows of the central ledger: inspect its report and reconcile the ledger before choosing Bs. X-rays is still Running, despite its old estimated end time. No test was ended, replaced or declared finished. Three scheduled longs show Ineligible; their armed variant setup needs inspection. Two longs have no badge; that alone does not prove no configured test.

Competitor collector runs in tmux `j1107-competitors`, log `/Users/benjaminoats/_desk/logs/j1107-competitors.log`, completion `/Users/benjaminoats/_desk/logs/j1107-competitors.done`. Missing .done means still running: do not start another. Uses saved public yt-dlp metadata, exact dates, separate long/Short tabs, then fastest/slowest cohorts and thumbnails. Ten tabs fetched (five requested reference channels); per-video exact-date collection ongoing. A capped 200-entry tab is marked capped: expand if it does not cover the full 90 days. Veritasium still needs history-piece eligibility coding. Search on all 8 long titles saved separately; classify genuinely relevant history-of-science channels before adding them, excluding unrelated music, nursery, veterinary and exercise results. Fast/slow comparison, visual coding, patterns and title Bs are unfinished.

Resume: confirm collector completion and errors; finish 90-day/competitor coverage; recover actual Short frame 0 and chosen covers; obtain views-from-impressions and inspect all test reports; complete style scores; only then select up to three eligible Bs, build in HOS style, run packaging panel, apply agreed feedback and queue Chief-gated Studio tasks. Preserve step count 5. No Bs or downstream Studio jobs created yet, no spend and no YouTube changes.

## Validation

HOS check_all.sh exit 0: `ALL CHECKS PASS`. Full output: checks.txt. Live `npm run channel:audit` exit 1: `58 videos, 4 errors.` All four reported errors are duplicate-live self-comparisons for uU12JA5rMWg, which appears twice in that tool output. The live API inventory here deduplicates IDs and contains it once. This audit does not change the checker or claim the live channel gate passed. Studio-only checklist beyond thumbnail test statuses remains outside this checkpoint.

## 19:20 UTC continuation — read this before rerunning collectors

The detached collector **finished exit 0**. There is no active render/collector. `competitors/cohorts.json`, `coverage.json`, `thumbnail_manifest.json`, `long_visual_coding.json`, `short_visual_coding.json` and `FINDINGS.md` now hold the five-channel result: 122 hashes verified, 68 long and 54 Short image observations. The 125 nonpublic details were deliberately excluded. See the history filter and overlapping-tail caveats.

The earlier HOS PR370 / commit 64a4c4c3 has been recovered selectively under `recovered/` with provenance: all six search-neighbour cohorts, their image manifest, search evidence, frame-zero manifest, exact-window metrics and relevant Studio text. Do not collect these again. Their contact sheets and images are already under `_desk/J1107/competitors/`. Next: code the six search-neighbour cohorts, verify Short covers/openings and current test setup, then create eligible designs/panel/handoff. Five-step progress stays 1/5; Short coverage prevents calling step 2 complete.

Recovered 28-day engaged views from impressions: Periodic Table 15, Atom 8, Germs 1, X-rays 0. These are supported by saved `studio_*_28days.txt`, not the separate lifetime Reach reads. Shorts unknown. Frame-zero sources: 11 hash matches, 2 mismatches (John Snow, infrared), 19 unavailable; still images alone do not verify motion/VO. Preserve J1113 changes.

Continue the same branches and PRs: HOS PR371 `codex/j1107-hos-thumb-assets`, OWB PR324 `codex/j1107-hos-thumb-audit`. Restored worktrees: `/private/tmp/j1107-hos-wt` and `/private/tmp/j1107-owb-wt`. Do not start another audit branch or duplicate the earlier PRs.

Continuation validation: `check_all.sh` exit 0, `ALL CHECKS PASS`; full output in HOS `checks_continuation.txt`. Initial sandbox npm-cache failure was resolved by using the existing checkout dependencies and a writable temporary cache, with no dependency change. All 122 selected IDs have visual records and matching image hashes; git diff whitespace check is clean. No new live Studio session occurred in this continuation.
