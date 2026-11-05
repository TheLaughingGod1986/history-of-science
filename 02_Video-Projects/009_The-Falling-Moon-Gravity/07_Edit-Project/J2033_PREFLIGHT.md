# J2033 worker preflight — 4 November 2026

Worker: codex. Generation: 0/20. New KEEP decisions: 0. Credits spent: 0.

All 20 TRANCHE2_SCOPE_J2026.json rows exist in their v05 boards; all five board SHA-256 values match the scope. Accepted VO and media were not changed. No publishing actions were taken.

The existing HOS009 `_mint_flow_v04_tranche1.py` is not a tranche-2 runner: `boards()` selects v04 tranche 1; `finalize_video()` sets status KEEP automatically and writes a perceptual UAT assertion. Do not run it unchanged or merely override its constants. It also imports HOS006 `flow_page()`, whose fallback opened a duplicate tab when Flow was on `/about`.

This tooling PR replaces that caller's page selection with OWB `cdp_tabs.reuse_page`. An existing project remains untouched; an existing about/blank tab is navigated to Flow home; closed tabs are ignored; unrelated tabs remain untouched. Requires the existing OWB checkout (or OWB_REPO) for the shared helper. This PR does not make the old tranche-1 runner suitable for tranche 2.

Validation:
- `python3 -m unittest discover -s tests -p test_flow_page_reuse.py -v`: 5 tests OK (actual shared helper, fake browser, zero submissions).
- `bash 00_Brand/Channel-Setup/tools/check_all.sh`: ALL CHECKS PASS (using installed HOS node_modules via an untracked ignored symlink and temporary npm cache).
- `git diff --check`: clean.

Chief handoff: review/merge the tab-reuse fix, then provide a separately tested scoped tranche-2 runner before releasing J2033. It must consume only the approved v05 rows, mint P02:10_how_high and P03:07_ball_to_moon first, extract continuation references from their named parent clips, preserve versioned files, and write GENERATED/PENDING_REVIEW rather than KEEP. It must enforce writer locking, fresh account/balance and exact Quality x1 price evidence, pending-charge accounting, full remaining-cap reservation and the 3000-credit floor, batches <=5 rows/1500 credits, <=3 takes/row and 6000 total; preserve receipts/spend/technical checks and hash-verified NAS copies. No new date hold or capability hold is needed. J2034 owns picture review.

Disk prerequisite: the prescribed `nas_offload.py --apply` was started because free space was about 16 GiB. Do not start a second copy while that process runs. See the worker handoff for its process/monitor state; generation did not start.
