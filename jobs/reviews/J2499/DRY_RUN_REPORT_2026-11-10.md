# HOS 013 Darwin & Wallace — Pass-1 Flow Mint Runner Dry-Run Report (J2499)

- **Date:** 2026-11-10
- **Film:** `HOS:013` (`013_Darwin-Wallace-Evolution`)
- **Job:** `J2499` (runner build, guard tests, and zero-spend dry-run; **0 submissions, 0 Create clicks, 0 credits spent, £0**)
- **Runner:** `02_Video-Projects/013_Darwin-Wallace-Evolution/07_Edit-Project/_mint_flow_v01_pass1.py`
- **Pinned scope:** `02_Video-Projects/013_Darwin-Wallace-Evolution/07_Edit-Project/PASS1_SCOPE_J2499.json`
- **Mint plan:** `02_Video-Projects/013_Darwin-Wallace-Evolution/07_Edit-Project/PASS1_MINT_PLAN_J2499.json`
- **Machine dry-run output:** `jobs/reviews/J2499/DRY_RUN_2026-11-10.json`
- **Unit test suite:** `tests/test_hos013_pass1_runner.py` (`21/21 PASS`)

---

## 1. Scope & Ordering Summary

- **Exact pass-1 row count:** **71** `flow-first` rows of `PICTURE_PLAN_v01.json` (out of 94 total rows; the 23 free rows — 16 code-graphic, 6 archive, 1 reuse — are excluded).
  - **Quality (`Veo 3.1 - Quality`, 8s, 16:9, x1 @ 100 credits):** **48** rows (`4,800` credits)
  - **Fast (`Veo 3.1 - Fast`, 8s, 16:9, x1 @ 10 credits):** **23** rows (`230` credits)
  - **Explorer rows:** **2** (`P1:11_beagle_cabin_explorer`, `P2:10a_explorer_shipmates`)
  - **First-pass total credit cap:** **`5,030` credits** (`MAX_TOTAL_CREDITS = 5030`, `MAX_TAKES_PER_ROW = 1`)
- **Order inside pass 1:** strictly **Part 01 first** (`P1:01_study_beaks` .. `P1:11_beagle_cabin_explorer`, covering the first 30s and the Shorts' opening frames), then **Parts 02 -> 06** in timeline order (`P6:08b_darwin_mendel_synthesis` last).
- **Batching (`MAX_BATCH_ROWS = 5`, `MAX_BATCH_CREDITS = 1000`):** **15 batches** (`14 × 5 rows + 1 × 1 row`; per-batch credits range from `100` to `500`, never exceeding `5` rows or `1,000` credits).

| Part | Mint rows | Quality (100) | Fast (10) | Explorer | Pass-1 credits |
|---|---:|---:|---:|---:|---:|
| Part 01 | 12 | 7 | 5 | 1 | 750 |
| Part 02 | 12 | 9 | 3 | 1 | 930 |
| Part 03 | 15 | 10 | 5 | 0 | 1,050 |
| Part 04 | 13 | 9 | 4 | 0 | 940 |
| Part 05 | 11 | 7 | 4 | 0 | 740 |
| Part 06 | 8 | 6 | 2 | 0 | 620 |
| **Total** | **71** | **48** | **23** | **2** | **5,030** |

---

## 2. Guards Built & Tested Offline (Zero Submissions)

Built on the J2200 `SharedFlowAccounting` protocol (`~/_desk/state/flow/shared`) and the repaired HOS 009 tranche-2 runner (`#468` 10 Nov DOM readers + plan `style_refs`, `#470` `Nano Banana 2.1` @ 0 credits, `#477` trusted CDP `page.mouse.click` + immutable still retry evidence paths):

1. **Right account & plan:** verifies `flow.google.com`, `ULTRA`, and the studio Ultra account via SHA-256 digest (`REQUIRED_ACCOUNT_SHA256`, `FORBIDDEN_ACCOUNT_SHA256`) so personal email addresses are never stored in code, tests, dry-run reports, or receipts.
2. **Right model & length per row:**
   - Quality rows require `Veo 3.1 - Quality`, `8s`, `16:9`, `x1`, `Generating will use 100 credits`.
   - Fast rows require `Veo 3.1 - Fast`, `8s`, `16:9`, `x1`, `Generating will use 10 credits`.
   - Missing start stills require `Nano Banana 2.1`, `16:9`, `x1`, `Generating will use 0 credits` (and post-take balance re-read confirms 0 credit drop).
3. **Live price read before each batch + atomic per-row recheck:** `read_live_batch_prices_on_page` / `accept_batch_prices` verifies both `100` (Quality) and `10` (Fast) on Flow before any row in a batch runs; `guarded_create` re-verifies the row's exact selected controls and price synchronously right before dispatching a trusted CDP `page.mouse.click(x, y)`.
4. **Live balance, pending charges, and cross-film reservations:** reads `~/_desk/state/flow/shared/account.jsonl` under exclusive `WriterLock`. Counts unposted charges, pending `SUBMITTING`/`PENDING` intents, and other films' active reservations (`J2033` `HOS:009` = `6,000` credits). At the latest recorded Flow balance (`14,890` at `2026-11-10T08:30:20Z`), projected headroom after reserving both `HOS:009` (`6,000`) and `HOS:013` (`5,030`) is **`3,860` credits** (`>= 0` floor).
5. **Pass-1 cap (`5,030`) & 1 take/row (`MAX_TAKES_PER_ROW = 1`):** enforced in `load_scope`, `ledger_totals`, `can_take`, `next_version`, `execute_shared_batch`, and `SharedFlowAccounting.reserve`.
6. **Batch cap (`<= 5` rows and `<= 1,000` credits):** enforced in `batch_rows` and `assert_batch_limits`.
7. **Shared writer lock & second-process refusal:** `WriterLock` (`flock` `LOCK_EX | LOCK_NB`) on both runner state and `~/_desk/state/flow/shared/writer.lock`; `refuse_duplicate` + `launch_once` PID gate blocks any second process even if an owner crashes or a stale `.done` exists.
8. **Missing/corrupt/drifted style reference refusal:** `verify_style_references` ffprobe/ffmpeg-decodes and SHA-256-verifies both house style refs on `studio-live` (`04_sunny_window_v01.jpg`, `10_mint_jar_v01.jpg`, `1920x1080` 16:9) and the repo Explorer sheet (`hos-explorer-reference-v01.jpg`, `1122x1402`) before opening Flow.
9. **Scope & prompt drift refusal:** `load_scope` cross-checks `PICTURE_PLAN_v01.json` sha256, all 6 `part-01..06_plates_v01.json` board sha256s, exact row membership/order, and per-row `prompt_sha256` + `normalized_prompt_sha256`.
10. **`GENERATED` / `PENDING_REVIEW` only (never `KEEP`) + NAS sha256 archive & receipts:** every output is written with `file_state="GENERATED"`, `status="PENDING_REVIEW"`, `review="PENDING_REVIEW"`, `keep=False`; `append_ledger`, `ledger_totals`, and `write_receipt` reject `KEEP`. Mounted NAS archive (`/Volumes/data/studio-live/History Of Science/02_Video-Projects/013_Darwin-Wallace-Evolution/04_Generated-Clips/archive_v01_pass1`) is verified mounted and receives sha256-verified `.mp4`, `.mp4.sha256.json`, per-take `.receipt.json`, and `batch-*.receipt.json`.
11. **Unarmed by default:** `plan` and `dry-run` never import Playwright or connect to CDP; `submit` exits non-zero unless `HOS013_PASS1_SUBMIT=1` after Chief review.

---

## 3. Verification Commands & Results

- `python3 -m unittest tests/test_hos013_pass1_runner.py -v` -> **Ran 21 tests, OK**
- `python3 02_Video-Projects/013_Darwin-Wallace-Evolution/07_Edit-Project/_mint_flow_v01_pass1.py dry-run --repo . --out jobs/reviews/J2499/DRY_RUN_2026-11-10.json` -> **PASS** (`submissions: 0`, `create_clicks: 0`, `credits_spent: 0`, `submit_armed: false`, `would_allow_reserve_at_recorded_balance: true`, `projected_headroom_after_013_cap: 3860`)
