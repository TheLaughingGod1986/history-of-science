# J2236 — Code Cleanup Audit: `history-of-science` Tools, `07_Content-Ops`, and Per-Film Build Scripts

**Date:** 7 November 2026  
**Job:** `J2236` (`Cleanup audit: history-of-science tools and per-film scripts (dead code, duplicates, bugs)`)  
**Worker:** `macbook` (read-only audit; no production code or NAS/shipped film outputs modified)  
**Scope:**
1. `00_Brand/Channel-Setup/tools` (22 files, 5,336 lines) + `00_Brand/Channel-Setup/audits/start_studio_chrome_cdp.sh`
2. `07_Content-Ops` (`src/lib/hos-contract/`, CLI scripts, tests, and legacy Next.js/Prisma app — 184 files, ~24,800 lines)
3. `04_Audio/tools` (22 files, 5,863 lines)
4. `scripts/`, `tests/`, and `.github/workflows/` (13 files, 1,115 lines)
5. `02_Video-Projects/` per-film scripts (754 scripts across 12 film folders, **261,112 lines**)

---

## Executive Summary & Top 5 Findings (Ranked by Value × Risk)

1. **[P0 — High Value / Low Risk] Archive the retired Next.js / Prisma / PostgreSQL / Direct-Social-Adapter web app in `07_Content-Ops/` (119 files, 15,835 lines) and fix the broken `vitest` suite (`tests/autopublish.test.ts` fails with exit 1):**
   - `orbit-with-ben` retired and archived its hosted ops dashboard and Prisma database on 27 Sep 2026 (`_archive/07_Content-Ops/`), and `history-of-science/AGENTS.md` locks social posting to Buffer only (`BUFFER_HOS_API_KEY`). Yet `history-of-science/07_Content-Ops/` still carries `prisma/`, `src/app/`, `src/components/`, `src/workers/publishing-worker.ts`, `src/lib/publishing/`, `src/lib/oauth/`, `src/lib/security/`, `src/lib/storage/`, and `docs/` (15,835 lines total). Running `npx vitest run` in `07_Content-Ops/` currently **FAILS** (4 failed tests in `tests/autopublish.test.ts` because `DATABASE_URL` is undefined). CI only stays green because `.github/workflows/hos-contract.yml` runs 1 of the 18 test files (`tests/hos-contract.test.ts`).
2. **[P0 — High Value / Low Risk] Fix three active bugs in `00_Brand/Channel-Setup/tools/` (`hos_desk.py`, `hos_build_rule_v02.py`, `vo_check_py312.sh`):**
   - **`hos_desk.py` (lines 50–51):** omits `"gemini"` from `PARTIES` and `WRITERS`, causing `python3 00_Brand/Channel-Setup/tools/hos_desk.py inbox --as gemini` to crash with `invalid choice: 'gemini'`, directly breaking the `AGENTS.md` Chief failover chain (`Grok → Claude → Codex → Gemini`).
   - **`hos_build_rule_v02.py` (lines 32–38, 578–595):** crashes with `FileNotFoundError` on `--check` and `--test-negatives` on any clean checkout, CI runner, or MacBook because `lift_words_006()` reads gitignored `02_Video-Projects/006_Trees-Are-Made-Of-Air/10_Shorts/_work_s04_photosynthesis_v01/timeline.json` with a hardcoded fallback to `/Users/benjaminoats/YouTube/History Of Science`. It also embeds ~1,350 lines of episode-specific dictionaries inside the checker.
   - **`vo_check_py312.sh` (lines 4–6):** hardcodes `ROOT="/Users/benjaminoats/YouTube/History Of Science"`, so running it inside a Mini worktree silently executes `main`'s `vo_check.py` instead of the worktree's, and fails on the MacBook.
3. **[P0 — High Value / Low Risk] Remove Never-list-violating & dead tools in `04_Audio/tools/` and `00_Brand/Channel-Setup/audits/` (`orbit_gemini_omni.py`, `orbit_gemini_veo.py`, `fix_published_playback_lag.py`, `vidiq_title_score_sheet.py`, `start_studio_chrome_cdp.sh`, and Orbit robot branches in `orbit_flow_veo_ui.py`):**
   - Four standalone tools in `04_Audio/tools/` (840 lines total, 0 call sites in HOS) plus ~250 lines of `orbit_flow_veo_ui.py` and `start_studio_chrome_cdp.sh` implement actions explicitly forbidden by `AGENTS.md`: the Orbit robot in HOS (`orbit_gemini_omni.py`, `orbit_gemini_veo.py`, `orbit_flow_veo_ui.py`), AI Studio `GEMINI_API_KEY` spend (`orbit_gemini_veo.py`), overwriting masters in place + YouTube Studio Replace (`fix_published_playback_lag.py`, `start_studio_chrome_cdp.sh`), hijacking Flow CDP port `:9222` (`start_studio_chrome_cdp.sh`), and appending `" | History of Science"` series suffixes to titles (`vidiq_title_score_sheet.py`).
4. **[P1 — High Value / Medium Risk] Replace per-film copy-paste across `02_Video-Projects/` (754 scripts, 261,112 lines) with 3 shared library modules (`hos_media.py`, `hos_cards.py`, `hos_short_builder.py`) and archive 518 unreferenced/superseded draft scripts (159,038 lines):**
   - Across `02_Video-Projects/`, **754 scripts total 261,112 lines** (`002` alone has 267 scripts / 81,806 lines, including 26 versions of `_assemble_part04_rough_v01..v26.py`).
   - Exactly **236 scripts (102,074 lines)** are referenced by provenance receipts (`PACKAGE_MANIFEST.json`, `SHORTS_RELEASE.json`, `SHORT_*.json`, `production-status.md`, etc.); **518 scripts (159,038 lines, 60.9%)** have zero receipt references (including 197 superseded `_vNN` drafts across 64 versioned families and 65 one-off `_probe_*`/`_harvest_*`/`_fix_*` scripts).
   - Identical helper functions are copy-pasted hundreds of times: `def sha256`/`sha256_file` (**278 scripts**), `def probe_dur`/`probe` (**266 scripts**), `def ff`/`run` (**178 scripts**), `def render_card`/`render_hook`/`render_side_label` (**142 scripts**), `def chunk_words`/`lifted_vo`/`caption_check` (**44–50 scripts**). Extracting three shared modules under `00_Brand/Channel-Setup/tools/` will cut ~85% of per-film code for films `011+`.
5. **[P1 — Medium Value / Low Risk] Close CI / `check_all.sh` coverage gaps and wire ElevenLabs spend into `ai_spend_hook.py`:**
   - `00_Brand/Channel-Setup/tools/check_all.sh` omits 4 checks that run in GitHub Actions (`core_sync.py check`, `sync_rules.py --check`, `test_weekly_public_audit.py`, `test_vo_take.py`), while 4 existing test files (`test_gate_stayed.py`, `test_orbit_cfr_delivery.py`, `tests/test_flow_page_reuse.py`, `tests/test_hos_code_graphic_resolution.py` — 25 tests total) and 16 passing `07_Content-Ops/tests/*.test.ts` suites run in **neither** `check_all.sh` **nor** `.github/workflows/`.
   - `04_Audio/tools/ai_spend_hook.py` is called by Flow/Vertex video minters but is **never called** by `el_guard.py`, `el_client.py`, or `vo_take.py`, leaving HOS ElevenLabs spend unrecorded in `orbit-with-ben/scripts/ai_spend.py`.

---

## Ranked Master Table of All Findings

| Rank | ID | Area | File(s) | Lines | `CORE_FILES.json` | Category | Value | Risk | Proposed Action |
|---|---|---|---|---:|---|---|---|---|---|
| 1 | **F-01** | `07_Content-Ops` | `prisma/`, `src/app/`, `src/components/`, `src/workers/`, `src/lib/{publishing,oauth,security,storage}/`, `docs/`, `src/lib/env.ts`, `tests/{autopublish,operator-auth}.test.ts` | 16,371 | `hos-only` | Dead legacy app + Failing test suite | High | Low | Archive retired web app/Prisma/direct adapters & obsolete tests to `_archive/07_Content-Ops/`; drop `DATABASE_URL` from `src/lib/env.ts`; run all 16 remaining `vitest` suites in CI & `check_all.sh`. |
| 2 | **F-02** | `00_Brand/tools` | `00_Brand/Channel-Setup/tools/hos_desk.py` (`L50-51`, `L358-376`) | 387 | `hos-only` | Bug (blocks Chief failover) | High | Low | Fix bug: add `"gemini"` to `PARTIES` and `WRITERS` so `hos_desk.py inbox --as gemini` and `post --from gemini` work per `AGENTS.md` line 273; add test in `scripts/test_hos_desk_handoffs.py`. |
| 3 | **F-03** | `00_Brand/tools` | `00_Brand/Channel-Setup/tools/hos_build_rule_v02.py` (`L32-38`, `L578-595`, `L600-1722`) | 1,722 | `hos-only` | Bug (`FileNotFoundError`) + Architecture | High | Low | Fix bug: guard `lift_words_006()` when gitignored `_work_s04_photosynthesis_v01/timeline.json` is absent; replace hardcoded `/Users/benjaminoats/...` paths with env overrides; split episode data (`PLATES_*`, `plan_*`) from the generic Shorts rule checker. |
| 4 | **F-04** | `04_Audio/tools` | `orbit_gemini_omni.py` (107L), `orbit_gemini_veo.py` (259L), `fix_published_playback_lag.py` (200L), `vidiq_title_score_sheet.py` (274L) | 840 | `hos-only` | Dead code + Never-list violations | High | Low | Archive all 4 zero-reference legacy scripts to `_archive/04_Audio/tools/`. |
| 5 | **F-05** | `04_Audio/tools` | `04_Audio/tools/orbit_flow_veo_ui.py` (`L38-159`, `L532-691`, `L748-873`, `L2751-2805`) | 3,230 | `hos-only` | Dead branch (Orbit robot) + CDP tab rule + duplicate `strip_audio` | High | Medium | Delete dead Orbit-robot branches (~250L), require `--start-frame` or `--scenery-only`, replace `veo.strip_audio` import with CORE `strip_cg_native_audio.py`, and connect to CDP `:9222` with `reuse_page` instead of launching a separate browser context. |
| 6 | **F-06** | `00_Brand/audits` | `00_Brand/Channel-Setup/audits/start_studio_chrome_cdp.sh` (`L1-37`) | 37 | **CORE** | Dangerous legacy script (port `:9222` collision + Studio Replace) | High | Low | Remove from `studio-core/CORE_FILES.json` in `orbit-with-ben`, sync via `scripts/core_sync.py`, and archive to `_archive/00_Brand/Channel-Setup/audits/` (`cdp_browsers.sh` is canonical). |
| 7 | **F-07** | `02_Video-Projects` | 754 per-film scripts across `02_Video-Projects/000..013` (518 unreferenced, 197 superseded `_vNN`, 65 debug/probe/harvest) | 261,112 | `hos-only` | Massive copy-paste + superseded drafts | High | Medium | Create shared helpers (`hos_media.py`, `hos_cards.py`, `hos_short_builder.py`) for films `011+`; archive the 518 unreferenced/superseded scripts (159,038L) + retired `SHORT_*.json` receipts to `_archive/02_Video-Projects/<film>/`, keeping all 236 receipt-backed provenance scripts untouched. |
| 8 | **F-08** | `00_Brand/tools` | `00_Brand/Channel-Setup/tools/vo_check_py312.sh` (`L4-11`) | 12 | `hos-only` | Bug (hardcoded Mini path breaks worktrees & MacBook) | Medium | Low | Fix bug: resolve `SCRIPT_DIR` relative to `$0` so worktrees run their own `vo_check.py`, and fall back cleanly from repo `.venv_vo_check_py312` to Mini `.venv_vo_check_py312` or `python3.12`/`python3`. |
| 9 | **F-09** | `00_Brand/tools` & `.github/workflows` | `00_Brand/Channel-Setup/tools/check_all.sh` (`L1-58`) & `.github/workflows/*.yml` | 58 | `hos-only` | CI / local gate drift (25 Python tests + 16 TS test suites skipped) | Medium | Low | Add missing checks (`core_sync.py check`, `sync_rules.py --check`, `test_weekly_public_audit.py`, `test_vo_take.py`, `test_gate_stayed.py`, `test_orbit_cfr_delivery.py`, `tests/test_*.py`, and full `vitest run`) to both `check_all.sh` and `.github/workflows/`. |
| 10 | **F-10** | `04_Audio/tools` & `00_Brand/tools` | `04_Audio/tools/vo_take.py` (`L65-168`), `00_Brand/Channel-Setup/tools/vo_check.py` (`L29-145`), `04_Audio/tools/ai_spend_hook.py` (`L1-40`), `04_Audio/tools/el_guard.py` (`L1-196`) | 790 | `hos-only` | Duplicate text/loudness logic + missing ElevenLabs `ai_spend.py` hook | Medium | Low | Merge word-normalisation (`UK_US`, `DROP_NUMBERS`, ordinals) and `ffprobe`/`ebur128` loudness helpers into one shared module; call `ai_spend_hook.record_spend("elevenlabs", ...)` from `el_guard.py`; support sibling checkout path in `ai_spend_hook.py`. |
| 11 | **F-11** | `07_Content-Ops` | `07_Content-Ops/scripts/{_j0946_*,_j0948_*,_j0952_*,j0188-*,hos-004-*,affiliate-*,apply-amazon-*,wire-topic-*}.ts` (12 files) | 1,688 | `hos-only` | One-off job & retired affiliate scripts | Medium | Low | Archive all 12 one-off `_j09*` / `j0188` / `hos-004` / affiliate scripts to `_archive/07_Content-Ops/scripts/`. |
| 12 | **F-12** | `00_Brand/tools` | `00_Brand/Channel-Setup/tools/atempo_known_over_cap.json` (`L1-28`) | 28 | `hos-only` | Stale exception allowlist (19 of 23 entries superseded or never uploaded) | Low | Low | Archive the 19 retired/superseded/never-uploaded Short build scripts & `SHORT_*.json` files to `_archive/02_Video-Projects/...` and prune `atempo_known_over_cap.json` down to the 4 aired `002` `backcat_four_elements` entries (`qW2OsD4mujc`). |
| 13 | **F-13** | `04_Audio/tools` | `04_Audio/tools/el_auth.py` (`L20-26`, `L65-115`), `04_Audio/tools/orbit_voice.py` (`L1-55`) | 192 | `el_auth.py` is **CORE**; `orbit_voice.py` is `hos-only` | Legacy dead branches & hardcoded OWB paths | Low | Low | In `orbit_with_ben`, remove dead `002/003/004` project bearer paths and Chrome IndexedDB scraper from `el_auth.py` and sync via `core_sync.py`; clean up `VOICE_ID_LOCK` warning in `orbit_voice.py`. |
| 14 | **F-14** | `07_Content-Ops` | `07_Content-Ops/src/lib/hos-contract/rules.ts` (`L356-380`) & `07_Content-Ops/scripts/package-lint.ts` (`L58-82`) | 704 | `hos-only` | Minor edge-case gap in `lintShortsRelease` | Low | Low | In `package-lint.ts` / `rules.ts`, check `atempo` / duration bounds and verify `video` file path existence when `status === "scheduled"` or `"uploaded"` in `SHORTS_RELEASE.json`. |

---

## Detailed Findings by Coverage Area

---

### Area 1: `00_Brand/Channel-Setup/tools/` & `00_Brand/Channel-Setup/audits/`

#### Finding F-02: `hos_desk.py` rejects `gemini` in `PARTIES` and `WRITERS`, breaking the Chief failover rule
- **File & Lines:** `00_Brand/Channel-Setup/tools/hos_desk.py`, lines 50–51 and 358–376 (387 lines total)
- **`CORE_FILES.json` Status:** `hos-only` (not locked in `CORE_FILES.json`)
- **Last Commit:** `ddefc98` (`2026-11-03 Keep desk tasks pending until linked outcome acknowledgement (#399)`)
- **Evidence:**
  - `AGENTS.md` line 273 states:
    > **Chief failover (Ben, 26 Oct):** Grok → Claude → Codex → Gemini. The elected Chief takes desk decisions under the same channel rules, using its own id (`hos_desk.py inbox --as codex|gemini`, or the Claude session).
  - In `00_Brand/Channel-Setup/tools/hos_desk.py` lines 50–51:
    ```python
    PARTIES = ("claude", "grok", "cursor", "codex", "ben")
    WRITERS = ("grok", "cursor", "codex")
    ```
  - Running `python3 00_Brand/Channel-Setup/tools/hos_desk.py inbox --as gemini` fails immediately with `argparse` error: `argument --as: invalid choice: 'gemini' (choose from 'claude', 'grok', 'cursor', 'codex', 'ben')`.
  - Note: Open PR `#450` (`cursor/j1809-desk-role`) is also touching desk role routing; coordinate when landing.
- **Proposed Action (`fix bug`):**
  - Add `"gemini"` to `PARTIES` and `WRITERS` in `00_Brand/Channel-Setup/tools/hos_desk.py` (`L50-51`), and add a unit test in `scripts/test_hos_desk_handoffs.py` verifying `--from gemini` and `inbox --as gemini`.

---

#### Finding F-03: `hos_build_rule_v02.py` crashes with `FileNotFoundError` on `--check` and `--test-negatives` on any clean checkout / CI / MacBook, and mixes 1,350 lines of episode data into the rule engine
- **File & Lines:** `00_Brand/Channel-Setup/tools/hos_build_rule_v02.py`, lines 32–38 (`MAIN_CHECKOUT`, `LOCAL_007_ROOT`), lines 578–595 (`lift_words_006`), and lines 600–1722 (hardcoded episode plans) (1,722 lines total)
- **`CORE_FILES.json` Status:** `hos-only`
- **Last Commit:** `0a92506` (`2026-11-05 Resolve J2211 HOS 010 Short A Option A1 7-shot segmentation and review PR 425`)
- **Evidence:**
  - Live test output on this checkout:
    ```
    $ python3 00_Brand/Channel-Setup/tools/hos_build_rule_v02.py --check
    Traceback (most recent call last):
      File ".../00_Brand/Channel-Setup/tools/hos_build_rule_v02.py", line 1718, in <module>
        sys.exit(main())
      File ".../00_Brand/Channel-Setup/tools/hos_build_rule_v02.py", line 1617, in main
        all_plans.extend(plan_006_lifts())
      File ".../00_Brand/Channel-Setup/tools/hos_build_rule_v02.py", line 752, in plan_006_lifts
        words, dur, note = lift_words_006(s["id"], s["t0"], s["t1"], s["vo_rel"])
      File ".../00_Brand/Channel-Setup/tools/hos_build_rule_v02.py", line 584, in lift_words_006
        tl = load(tl_path)
    FileNotFoundError: [Errno 2] No such file or directory: '.../02_Video-Projects/006_Trees-Are-Made-Of-Air/10_Shorts/_work_s04_photosynthesis_v01/timeline.json'
    ```
  - `_work_*` directories are gitignored (`.gitignore` line 32), and `resolve_repo_file()` (lines 32–49) falls back to hardcoded Mini directories `MAIN_CHECKOUT = Path("/Users/benjaminoats/YouTube/History Of Science")` and `LOCAL_007_ROOT = Path("/Users/benjaminoats/YouTube/hos-007-vaccine/02_Video-Projects/007_The-First-Vaccine")`.
  - Lines 70–390 (`HOOK_CONFLICT_PROPOSALS`, `PLATES_006`, `PLATES_FILMS`, `PLATES_S7`) and lines 578–1590 (`plan_006_abc`, `plan_006_lifts`, `plan_films`, `plan_standalone`) hardcode per-episode word maps and plate paths inside the tool.
- **Proposed Action (`fix bug` + `refactor`):**
  1. In `lift_words_006()` (`L578-595`), if `tl_path` does not exist on disk, fall back to `mapped` (from `words_006_vo()`) or the committed `00_Brand/Channel-Setup/audits/BUILD_RULE_v02.json` so `--check` and `--test-negatives` pass on any clean checkout, MacBook, or GitHub Actions runner.
  2. Replace hardcoded `/Users/benjaminoats/...` constants with `os.environ.get("HOS_MAIN_CHECKOUT")` fallbacks.
  3. Move episode-specific plan dictionaries (`PLATES_*`, `plan_*`) into a separate data file (`00_Brand/Channel-Setup/audits/build_rule_plans_v02.py` or per-film JSON manifests) and keep `hos_build_rule_v02.py` as a pure reusable checker (`find_word_cuts`, `build_rows`, `check_short`, `run_negative_self_tests`) and run `--test-negatives` in `check_all.sh`.

---

#### Finding F-06: `00_Brand/Channel-Setup/audits/start_studio_chrome_cdp.sh` hijacks Flow port `:9222` and promotes banned Studio Replace
- **File & Lines:** `00_Brand/Channel-Setup/audits/start_studio_chrome_cdp.sh`, lines 1–37 (37 lines total)
- **`CORE_FILES.json` Status:** **LOCKED in `studio-core/CORE_FILES.json`** (`sha256: d23cf346f85c6b0bc754695294270fd0c92c17e9ff4fa21e6c9ba570e100a214`)
- **Last Commit:** `c2e7996` (`2026-10-31`)
- **Evidence:**
  - Zero active code references in `history-of-science` (only mentioned in historical doc table in `AGENTS.md`).
  - Line 2: `# Open logged-in YouTube Studio with CDP :9222 for in-place Replace.`
  - Lines 4–6:
    ```bash
    PORT="${1:-9222}"
    SRC="${HOME}/.orbit-chrome-flow"
    DST="${HOME}/.orbit-chrome-youtube-studio"
    ```
  - This conflicts with three studio locks:
    1. In-place Studio Replace is on the **Never** list (`AGENTS.md` line 343: *"Never: Studio's in-place Replace or editor blur/trim on a Short"*).
    2. Port `9222` is reserved for Google Flow (`~/.hos-chrome-flow-benoats-googlemail-cdp`), while Orbit Studio is `9223` and HOS Studio is `9460`, managed by `00_Brand/Channel-Setup/tools/cdp_browsers.sh` (`com.hos.cdp-browsers.plist`).
- **Proposed Action (`archive to _archive/` via `core_sync.py`):**
  - In `orbit-with-ben`, remove `00_Brand/Channel-Setup/audits/start_studio_chrome_cdp.sh` from `studio-core/CORE_FILES.json`, move the file to `_archive/00_Brand/Channel-Setup/audits/start_studio_chrome_cdp.sh` in both repos, and run `python3 scripts/core_sync.py push`.

---

#### Finding F-08: `00_Brand/Channel-Setup/tools/vo_check_py312.sh` hardcodes `/Users/benjaminoats/YouTube/History Of Science`
- **File & Lines:** `00_Brand/Channel-Setup/tools/vo_check_py312.sh`, lines 4–11 (12 lines total)
- **`CORE_FILES.json` Status:** `hos-only`
- **Last Commit:** `c2e7996` (`2026-10-31`)
- **Evidence:**
  ```bash
  ROOT="/Users/benjaminoats/YouTube/History Of Science"
  PY="$ROOT/.venv_vo_check_py312/bin/python"
  TOOL="$ROOT/00_Brand/Channel-Setup/tools/vo_check.py"
  ```
  - When invoked from a Mini job worktree (`/tmp/hos-jNNNN-wt`), `vo_check_py312.sh` executes `vo_check.py` from the main checkout instead of the worktree's branch, and fails completely on `/Users/ben/_desk/worker/history-of-science` (MacBook).
- **Proposed Action (`fix bug`):**
  - Resolve `SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"`, `REPO_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"`, and `TOOL="$SCRIPT_DIR/vo_check.py"`. Look for `.venv_vo_check_py312/bin/python` in `$REPO_ROOT`, then `/Users/benjaminoats/YouTube/History Of Science/.venv_vo_check_py312/bin/python`, then `python3.12` / `python3`.

---

#### Finding F-09: `check_all.sh` and `.github/workflows/` omit 25 existing Python unit tests and 16 passing TypeScript test suites
- **Files & Lines:**
  - `00_Brand/Channel-Setup/tools/check_all.sh` (lines 1–58)
  - `.github/workflows/{audio-tools,channel-audit,core-check,desk-handoffs,hos-contract,rules-check,status-board,vo-check}.yml`
- **`CORE_FILES.json` Status:** `check_all.sh` is `hos-only`; `.github/workflows/core-check.yml` is **CORE**
- **Evidence:**
  - `check_all.sh` header states: *"Run every fast repo check locally before opening or updating a PR. Mirrors the GitHub Actions workflows so a PR with a red check here will be red in CI"*, but:
    1. **In GitHub Actions, missing from `check_all.sh`:**
       - `python3 scripts/core_sync.py check` (in `core-check.yml`)
       - `python3 scripts/sync_rules.py --check` (in `rules-check.yml`)
       - `python3 00_Brand/Channel-Setup/tools/test_weekly_public_audit.py` (3 tests, in `core-check.yml`)
       - `python3 04_Audio/tools/test_vo_take.py` (9 tests, in `audio-tools.yml`)
    2. **In the repo (all PASS), missing from BOTH `check_all.sh` and `.github/workflows/`:**
       - `00_Brand/Channel-Setup/tools/test_gate_stayed.py` (173 lines, 7 unit tests — `OK`)
       - `04_Audio/tools/test_orbit_cfr_delivery.py` (220 lines, 11 unit tests — `OK`)
       - `tests/test_flow_page_reuse.py` (104 lines, 5 unit tests — `OK`)
       - `tests/test_hos_code_graphic_resolution.py` (33 lines, 2 unit tests — `OK`)
       - 15 passing Vitest suites in `07_Content-Ops/tests/` (`script-scorecard.test.ts`, `episode-readiness.test.ts`, `package-readiness.test.ts`, `youtube-package-publish.test.ts`, `youtube-captions-sync.test.ts`, `youtube-SubscriberThankYou.test.ts`, `script-RetentionHooks.test.ts`, etc.) — `hos-contract.yml` only runs `npx vitest run tests/hos-contract.test.ts`.
- **Proposed Action (`fix bug` / CI alignment):**
  - Add all 8 missing Python checks/test suites to `00_Brand/Channel-Setup/tools/check_all.sh` and the corresponding `.github/workflows/*.yml` files, and once Finding F-01 is resolved, change `npx vitest run tests/hos-contract.test.ts` to `npx vitest run` in both `check_all.sh` (`L35`) and `.github/workflows/hos-contract.yml` (`L142`).

---

#### Finding F-12: `atempo_known_over_cap.json` retains 19 retired, superseded, or never-uploaded files out of 23 entries
- **File & Lines:** `00_Brand/Channel-Setup/tools/atempo_known_over_cap.json`, lines 1–28 (28 lines total), read by `00_Brand/Channel-Setup/tools/atempo_check.py` (133 lines)
- **`CORE_FILES.json` Status:** `hos-only`
- **Last Commit:** `af600f2` (`2026-11-04 tools: fail any build that speeds the voice above atempo 1.06 (#369)`)
- **Evidence:**
  - Line 2 of `atempo_known_over_cap.json`: `"note": "... Remove an entry once its build is retired or rebuilt."`
  - Out of 23 entries in `"files"` (`L4-26`):
    - **13 entries are explicitly marked superseded and/or private & unscheduled:**
      - `001` `SHORT_s11_curved_flask_v01.{json,py}` (`"superseded by v07 (-3L6HzJ_d_4, public 27 Oct)"`) and `SHORT_s11_curved_flask_v02.{json,py}` (`"was 1-BZaFIMwYU, now private and unscheduled; v07 aired instead"`)
      - `007` `SHORT_s04_smallpox_test_v01.{json,py}` (`"was -I_GHK-GcFs, now private and unscheduled; J1219 swapped the 13 Nov slot to v04 (1.05) as cLKDiYP55J8 on 29 Oct"`) and `SHORT_s04_smallpox_test_v02.{json,py}` (`"superseded local cut, never uploaded"`)
      - `007` `SHORT_s05_vacca_jesty_v01.{json,py}`, `v02.json`, and `v03.{json,py}` (`"J1222 swapped the 17 Nov slot to v05 (1.03) as xgx2lYHhYZM on 30 Oct"` / `"superseded local cut, never uploaded"`)
    - **6 entries are `"built, never uploaded: rebuild at <=1.06 before any upload"`:**
      - `001` `SHORT_s07_semmelweis_hands_v01.{json,py}`, `001` `SHORT_s09_lister_antiseptic_v01.{json,py}`, `005` `SHORT_s08_capillaries_v01.{json,py}`
    - Only **4 entries** correspond to an aired cut (`002` `_build_backcat_four_elements_v02.py`, `_v03.py`, and their `*_meta.json` receipts for `qW2OsD4mujc`, aired Tue 3 Nov).
- **Proposed Action (`archive to _archive/` + prune allowlist):**
  - Archive the 19 superseded/never-uploaded `_build_short_*.py` and `SHORT_*.json` files to `_archive/02_Video-Projects/<film>/10_Shorts/` and remove those 19 lines from `00_Brand/Channel-Setup/tools/atempo_known_over_cap.json`.

---

#### Summary of Clean / Active Tools in `00_Brand/Channel-Setup/tools/` (No Cleanup Needed)
- `atempo_check.py` (133L) & `test_atempo_check.py` (52L, 5 tests PASS)
- `cdp_browsers.sh` (127L) & `com.hos.cdp-browsers.plist` (38L)
- `channel_profile.py` (13L)
- `gate_shorts_open.py` (976L, **CORE**) & `test_gate_stayed.py` (173L, 7 tests PASS)
- `neighbours.py` (226L), `public_search.py` (103L), `status_board.py` (417L), `style_sheet.py` (63L), `thumb_preview.py` (75L)
- `vo_check.py` (312L) & `test_vo_check.py` (88L, 4 tests PASS)
- `weekly_public_audit.py` (271L, **CORE**) & `test_weekly_public_audit.py` (58L, **CORE**, 3 tests PASS)

---

### Area 2: `07_Content-Ops/` (Release Contract, CLI Scripts, and Retired Web App)

#### Finding F-01: Retired Next.js / Prisma / PostgreSQL / Direct-Social-Adapter web app (119 files, 15,835 lines) is still in `07_Content-Ops/` and breaks `npx vitest run`
- **Files & Lines:**
  - `07_Content-Ops/prisma/` (4 files: `schema.prisma`, `seed.ts`, 2 migrations — **2,053 lines**)
  - `07_Content-Ops/src/app/` (53 Next.js route/page files: `/affiliate`, `/analytics`, `/calendar`, `/clips`, `/login`, `/api/oauth`, `/api/posts`, `/api/connections`, `/go/[slug]` — **5,701 lines**)
  - `07_Content-Ops/src/components/` (20 React UI components — **1,801 lines**)
  - `07_Content-Ops/src/workers/publishing-worker.ts` (**357 lines**)
  - `07_Content-Ops/src/lib/publishing/` (22 files including direct `meta.ts`, `threads.ts`, `tiktok.ts`, `x.ts`, `jobs.ts`, `idempotency.ts`, `duplicates.ts`, `status.ts`, `schedule.ts` — **4,171 lines**)
  - `07_Content-Ops/src/lib/oauth/state.ts` (**52 lines**), `07_Content-Ops/src/lib/security/{operator-auth,token-crypto}.ts` (**239 lines**), `07_Content-Ops/src/lib/storage/prisma.ts` (**15 lines**)
  - `07_Content-Ops/docs/` (15 docs for Meta/TikTok/X/Threads OAuth & local publishing worker — **1,446 lines**)
  - `07_Content-Ops/scripts/{reconcile-publishing-jobs.ts,validate-connections.ts,with-direct-url.mjs}` (**263 lines**)
  - `07_Content-Ops/src/lib/env.ts` (`L12`: `DATABASE_URL: z.string().min(1)` — **97 lines**)
  - `07_Content-Ops/tests/autopublish.test.ts` (**371 lines**) & `07_Content-Ops/tests/operator-auth.test.ts` (**68 lines**)
- **`CORE_FILES.json` Status:** All `hos-only` (none of `07_Content-Ops` is in `CORE_FILES.json`)
- **Evidence:**
  1. In `orbit-with-ben`, this entire hosted ops dashboard, Prisma schema, and direct social publishing stack was retired on 27 Sep 2026 and moved to `_archive/07_Content-Ops/` (`orbit-with-ben/AGENTS.md` line 34).
  2. In `history-of-science/AGENTS.md` line 45: *"Social posts go through Buffer only (HOS org, `BUFFER_HOS_API_KEY`)... Old Meta/Threads/TikTok CDP auto-post trees are under `_archive/00_Brand/Channel-Setup/`."*
  3. `.github/workflows/hos-contract.yml` line 140 explicitly runs `npm ci --ignore-scripts` with the comment: `# --ignore-scripts: the contract needs no database or Prisma client`.
  4. Running `npx vitest run` in `07_Content-Ops/` **FAILS** (exit code 1):
     ```
     FAIL  tests/autopublish.test.ts (10 tests | 4 failed)
       × maps transient and permanent adapter failures into retry vs failed states
         → Invalid `prisma.socialConnection.upsert()` invocation in src/lib/publishing/jobs.ts:449:29
           error: Environment variable not found: DATABASE_URL.
       × blocks enqueue when local file path is missing for live mode (tests/autopublish.test.ts:134)
       × blocks enqueue when local media path is not an existing file in live mode (tests/autopublish.test.ts:243)
       × fails job when live mode has no connected destination account (tests/autopublish.test.ts:313)
         → Error: Invalid environment configuration: DATABASE_URL: Invalid input: expected string, received undefined (src/lib/env.ts:56:11)
     Test Files  1 failed | 17 passed (18)
     ```
- **Proposed Action (`archive to _archive/` + `fix bug`):**
  1. Move `prisma/`, `src/app/`, `src/components/`, `src/workers/`, `src/lib/{publishing,oauth,security,storage}/`, `docs/`, `scripts/{reconcile-publishing-jobs.ts,validate-connections.ts,with-direct-url.mjs}`, and `tests/{autopublish,operator-auth}.test.ts` to `_archive/07_Content-Ops/`.
  2. Remove `DATABASE_URL` and retired OAuth/operator env vars from `07_Content-Ops/src/lib/env.ts` (or make them optional) and remove `@prisma/client` / `prisma` / `next` / `react` dependencies from `07_Content-Ops/package.json` so `07_Content-Ops` is a fast, lightweight TypeScript CLI + test package like `orbit-with-ben/07_Content-Ops`.
  3. Update `00_Brand/Channel-Setup/tools/check_all.sh` and `.github/workflows/hos-contract.yml` to run `npx vitest run` across all 16 active test suites.

---

#### Finding F-11: 12 one-off job scripts and retired affiliate scripts in `07_Content-Ops/scripts/`
- **Files & Lines:**
  - `07_Content-Ops/scripts/_j0946_captions_readback.ts` (64 lines)
  - `07_Content-Ops/scripts/_j0948_readback.ts` (71 lines)
  - `07_Content-Ops/scripts/_j0948_tags.ts` (76 lines)
  - `07_Content-Ops/scripts/_j0948_unschedule.ts` (80 lines)
  - `07_Content-Ops/scripts/_j0952_readback.ts` (75 lines)
  - `07_Content-Ops/scripts/_j0952_unschedule.ts` (58 lines)
  - `07_Content-Ops/scripts/j0188-language-repair.ts` (167 lines)
  - `07_Content-Ops/scripts/hos-004-package-dry-run-v02.ts` (166 lines)
  - `07_Content-Ops/scripts/affiliate-go-live.ts` (324 lines)
  - `07_Content-Ops/scripts/apply-amazon-live-urls.ts` (291 lines)
  - `07_Content-Ops/scripts/wire-topic-book-placements.ts` (316 lines)
- **`CORE_FILES.json` Status:** `hos-only`
- **Evidence:**
  - Zero references in `package.json`, `.github/workflows/`, or `AGENTS.md` commands.
  - All `_j0946*`, `_j0948*`, `_j0952*`, `j0188*`, and `hos-004*` scripts were single-use incident scripts from October 2026 jobs.
  - `AGENTS.md` line 213 (`Money & links`): *"HOS descriptions carry no book or affiliate links until Associate is approved and re-verified"* — and the Prisma-backed affiliate tables are retired (Finding F-01).
- **Proposed Action (`archive to _archive/`):**
  - Move these 11 files (plus the 3 publishing-worker scripts in F-01) to `_archive/07_Content-Ops/scripts/`.

---

#### Finding F-14: `07_Content-Ops/src/lib/hos-contract/rules.ts` and `scripts/package-lint.ts` audit
- **Files & Lines:**
  - `07_Content-Ops/src/lib/hos-contract/rules.ts` (502 lines, last commit `fab39c3` on `2026-11-04`)
  - `07_Content-Ops/scripts/package-lint.ts` (202 lines, last commit `c2e7996` on `2026-10-31`)
  - `07_Content-Ops/scripts/channel-audit.ts` (181 lines, last commit `a87cd56` on `2026-10-27`)
  - `07_Content-Ops/tests/hos-contract.test.ts` (365 lines, 20 tests — all PASS in 169 ms)
- **`CORE_FILES.json` Status:** `hos-only`
- **Audit Assessment:**
  - `rules.ts`, `package-lint.ts`, `channel-audit.ts`, and `hos-contract.test.ts` are **clean, well-structured, and actively enforced** in CI (`hos-contract.yml` and `channel-audit.yml`).
  - Recent fixes (`dedupeVideoIds` and `dedupeVideosById` for YouTube API playlist page boundaries, `containsSyntheticMedia` Data API omission warning vs explicit `false` error, draft long package chapter/sources 14-day window) are well-tested.
  - **Two minor improvement opportunities (`low risk`):**
    1. In `package-lint.ts` (`L58-82`), when linting `SHORTS_RELEASE.json`, each entry's `file` / `video` path on disk is not checked for existence or `atempo` compliance even when `status === "scheduled"`. Adding an optional `fileExists` check for scheduled Shorts when the file is tracked/present prevents stale paths in `SHORTS_RELEASE.json`.
    2. `STUDIO_ONLY_CHECKS` (`rules.ts` lines 494–495) lists `"AI disclosure = Yes (confirm by eye)"` and `"Every video: Altered / synthetic content = Yes (Data API videos.list omits this field)"` as two separate bullets for the same Studio checkbox; those two lines can be merged into one clear checklist line.

---

### Area 3: `04_Audio/tools/`

#### Finding F-04: Four zero-reference tools in `04_Audio/tools/` that violate the `AGENTS.md` Never list (840 lines)
- **Files & Lines:**
  1. `04_Audio/tools/orbit_gemini_omni.py` (107 lines, `hos-only`, last commit `c2e7996`)
     - **Evidence:** `git grep orbit_gemini_omni` returns **0 matches** outside `_archive/`. Hardcodes `ORBIT_REF = REPO / "01_Orbit-Character/05_Seedance-References/orbit-seedance-reference-16x9-v01.png"` (does not exist in HOS) and calls `gemini-omni-flash-preview`. Violates `AGENTS.md` line 336 (`Never: The Orbit robot in any HOS film. Omni, Seedance, Kling...`).
  2. `04_Audio/tools/orbit_gemini_veo.py` (259 lines, `hos-only`, last commit `c2e7996`)
     - **Evidence:** Only imported by `orbit_flow_veo_ui.py` (`import orbit_gemini_veo as veo`, line 38) for two trivial helpers (`veo.already_done`, `veo.strip_audio`) and dead Orbit constants (`veo.ORBIT_REF`, `veo.build_prompt`). Reads `GEMINI_API_KEY` (`aistudio.google.com/apikey`, violating `AGENTS.md` line 467 *"never AI Studio prepaid credit"*), and injects `IDENTITY_LOCK = "CRITICAL ORBIT IDENTITY — match the attached reference image exactly, full-CG Orbit in every frame: solid matte ORANGE rounded floating robot..."`.
  3. `04_Audio/tools/fix_published_playback_lag.py` (200 lines, `hos-only`, last commit `c2e7996`)
     - **Evidence:** `git grep fix_published_playback_lag` returns **0 code matches** (only `docs/PUBLISHED_PLAYBACK_LAG_FIX.md`). When run with `--apply`, it overwrites master `.mp4` files in place (`os.replace(tmp_path, src)`) and prints instructions to use YouTube **Studio Replace** on live video IDs — both explicitly banned by `AGENTS.md` lines 343 & 346 (`Never: Studio's in-place Replace`, `Never: Overwriting a previous cut`). Also references `SHORTS_UPLOAD_INDEX.json` (an Orbit-only file).
  4. `04_Audio/tools/vidiq_title_score_sheet.py` (274 lines, `hos-only`, last commit `c2e7996`)
     - **Evidence:** `git grep vidiq_title_score_sheet` returns **0 matches**. Lines 203–211 (`clean_title`) automatically append `" | History of Science"` (`SUFFIX = " | History of Science"`) to every title, which is an explicit hard fail under `AGENTS.md` line 345 (`Never: Titles: hashtags, series suffixes`) and `07_Content-Ops/src/lib/hos-contract/rules.ts`.
- **Proposed Action (`archive to _archive/`):**
  - Archive all four scripts (`orbit_gemini_omni.py`, `orbit_gemini_veo.py`, `fix_published_playback_lag.py`, `vidiq_title_score_sheet.py`) to `_archive/04_Audio/tools/` (after removing `import orbit_gemini_veo as veo` from `orbit_flow_veo_ui.py` in Finding F-05).

---

#### Finding F-05: `04_Audio/tools/orbit_flow_veo_ui.py` (3,230 lines) contains ~250 lines of dead Orbit-robot code, duplicates `strip_cg_native_audio.py`, and launches its own Chromium context instead of reusing CDP `:9222`
- **File & Lines:** `04_Audio/tools/orbit_flow_veo_ui.py`, lines 38–159 (`ORBIT_AGENT_INSTRUCTION`, `FLOW_I2V_PREFACE`), lines 532–691 (`launch_context`, `upload_orbit_ref`, `_assert_orbit_identity_ref`, `attach_orbit_to_prompt`, `ensure_orbit_agent_instruction`), lines 2751–2805 (`main` default mode) (3,230 lines total)
- **`CORE_FILES.json` Status:** `hos-only` (`tests/test_flow_page_reuse.py` imports `_acquire_flow_work_page` and `_close_extra_flow_tabs`)
- **Evidence:**
  1. **Orbit robot default mode:** When invoked without `--start-frame` or `--scenery-only`, `orbit_flow_veo_ui.py` defaults to uploading `veo.ORBIT_REF` (the orange robot) and injecting `ORBIT_AGENT_INSTRUCTION` (`"small rounded matte-orange floating space robot"`). In HOS, every Flow clip is either `--start-frame <still.jpg>` (image-to-video) or `--scenery-only` (text-to-video).
  2. **Duplicate audio stripper:** Calls `veo.strip_audio(raw)` from `orbit_gemini_veo.py` instead of the CORE-locked `04_Audio/tools/strip_cg_native_audio.py` (`strip_native_audio_to_silent_aac`).
  3. **Browser context management (`launch_context`, lines 532–554):** Launches `pw.chromium.launch_persistent_context(str(PROFILE_DIR), ...)` on `~/.orbit-chrome-flow` instead of connecting over CDP to the managed Flow browser on port `:9222` (`00_Brand/Channel-Setup/tools/cdp_browsers.sh`). While `_acquire_flow_work_page(ctx)` (lines 282–307, tested by `tests/test_flow_page_reuse.py`) properly reuses a single tab within `ctx`, `launch_context()` itself still opens a separate Chrome instance unless CDP `:9222` is used.
- **Proposed Action (`delete dead branch` + `refactor`):**
  1. Delete `ORBIT_AGENT_INSTRUCTION`, `FLOW_I2V_PREFACE`, `upload_orbit_ref`, `_assert_orbit_identity_ref`, `attach_orbit_to_prompt`, `ensure_orbit_agent_instruction`, and `import orbit_gemini_veo as veo`. Require either `--start-frame` or `--scenery-only` in `main()`.
  2. Import `strip_native_audio_to_silent_aac` from `strip_cg_native_audio` (and inline the 3-line `already_done(out)` check).
  3. In `launch_context()`, connect first to `http://127.0.0.1:9222` via `pw.chromium.connect_over_cdp("http://127.0.0.1:9222")` (keeping `_acquire_flow_work_page(ctx)` so `tests/test_flow_page_reuse.py` continues to pass) and never close the shared CDP browser on exit.

---

#### Finding F-10: Duplicate word-normalisation & loudness code between `vo_take.py` and `vo_check.py`, plus missing ElevenLabs spend hook in `el_guard.py` / `ai_spend_hook.py`
- **Files & Lines:**
  - `04_Audio/tools/vo_take.py` (lines 65–168, 242 lines total, `hos-only`)
  - `00_Brand/Channel-Setup/tools/vo_check.py` (lines 29–145, 312 lines total, `hos-only`)
  - `04_Audio/tools/el_guard.py` (lines 1–196, `hos-only`) & `04_Audio/tools/el_client.py` (lines 1–113, `hos-only`)
  - `04_Audio/tools/ai_spend_hook.py` (lines 1–40, `hos-only`)
- **Evidence:**
  1. **Duplicated & diverging word diff / loudness:**
     - Both `vo_take.py` and `vo_check.py` implement word normalisation, SequenceMatcher script diffing, `ffprobe` duration probing, and `ffmpeg` `volumedetect` loudness measurement.
     - However, `vo_check.py` (`L29-65`) has `UK_US` spelling canonicalisation (`recognise`/`recognize`, `colour`/`color`, `sulphur`/`sulfur`, `aluminium`/`aluminum`, etc.), `DROP_NUMBERS` (cardinals transcribed as digits by Scribe/Whisper), and ordinal suffix stripping (`1st` -> `st`), whereas `vo_take.py` (`L65-75`) only strips punctuation (`re.findall(r"[a-z0-9']+", ...)`). As a result, `vo_take.py`'s Scribe check (`scribe_check`) flags false mismatches on numbers and UK/US spellings that `vo_check.py` passes!
  2. **Missing ElevenLabs `ai_spend_hook.py` call:**
     - `AGENTS.md` line 490 mandates: *"for both channels, every credit reading and every spend goes into `scripts/ai_spend.py` in `orbit-with-ben`."*
     - `git grep ai_spend_hook` shows `ai_spend_hook.py` is called in `orbit_flow_veo_ui.py` (`L2264`) and Vertex minters, but **0 times** in `el_guard.py`, `el_client.py`, or `vo_take.py`.
     - Furthermore, `04_Audio/tools/ai_spend_hook.py` line 18 hardcodes `OWB_DEFAULT = Path.home() / "YouTube" / "orbit-with-ben"` without checking the sibling checkout `Path(__file__).resolve().parents[3] / "orbit-with-ben"` (which is where `orbit-with-ben` lives on the MacBook and in multi-slot setups).
- **Proposed Action (`merge duplicates into one shared helper` + `fix bug`):**
  1. Import `norm`, `loudness`, and `probe_duration` from `00_Brand/Channel-Setup/tools/vo_check.py` inside `04_Audio/tools/vo_take.py` so Scribe and Whisper use the exact same UK/US and number-aware normaliser.
  2. In `04_Audio/tools/el_guard.py` (`finish()` and `check_budget_and_reserve()`), call `ai_spend_hook.record_spend("elevenlabs", chars, ...)` and `ai_spend_hook.record_reading(...)`.
  3. In `04_Audio/tools/ai_spend_hook.py` (`_script()`), check `(Path(__file__).resolve().parents[3] / "orbit-with-ben" / "scripts" / "ai_spend.py")` before falling back to `Path.home() / "YouTube" / "orbit-with-ben"`.

---

#### Finding F-13: Legacy dead branches in `04_Audio/tools/el_auth.py` (CORE) and `orbit_voice.py`
- **Files & Lines:**
  - `04_Audio/tools/el_auth.py`, lines 20–26 (`_PROJECT_ENVS`) and lines 65–115 (`_from_indexeddb`) (137 lines, **CORE**)
  - `04_Audio/tools/orbit_voice.py`, lines 38–54 (`VOICE_ID_LOCK` fallback warning) (55 lines, `hos-only`)
- **Evidence:**
  - `el_auth.py` lines 20–26 search three non-existent Orbit episode paths (`02_Video-Projects/003_Exoplanets...`, `004_JWST...`, `002_What-Happens...`) for `.elevenlabs_bearer`, and lines 65–115 scrape Chrome IndexedDB (`~/.orbit-chrome-flow/Default/IndexedDB/...`) for firebase tokens when `ELEVENLABS_API_KEY` is now standard in `.env`.
- **Proposed Action (`delete dead branch`):**
  - Low priority: when touching `studio-core` in `orbit-with-ben`, remove `_PROJECT_ENVS` and `_from_indexeddb` from `04_Audio/tools/el_auth.py` and sync via `core_sync.py`.

---

#### Summary of Clean / Active Tools in `04_Audio/tools/` (No Cleanup Needed)
- `el_client.py` (113L) & `test_vo_take.py` (167L, 9 tests PASS)
- `generate_music_bed.py` (115L, **CORE**) & `generate_sfx_from_script.py` (175L, **CORE**)
- `make_ Hos_sfx_bed.py` / `make_hos_sfx_bed.py` (88L), `make_hos_music_bed.py` (226L), `make_music_bed.py` (194L), `make_sfx_bed.py` (191L)
- `narration_prep.py` (154L, **CORE**)
- `orbit_cfr_delivery.py` (338L, **CORE**) & `test_orbit_cfr_delivery.py` (220L, 11 tests PASS)
- `strip_cg_native_audio.py` (65L, **CORE**)
- `verify_veo_lip_sync.py` (467L, **CORE**)

---

### Area 4: `scripts/`, `tests/`, and `.github/workflows/`

- **Files Inspected:**
  - `scripts/core_sync.py` (127 lines, **CORE**) — `python3 scripts/core_sync.py check` PASSes (`core_sync: OK (56 core files match manifest)`).
  - `scripts/sync_rules.py` (104 lines, `hos-only`) — `python3 scripts/sync_rules.py --check` PASSes (`OK: CLAUDE.md and .cursor/rules/hos-studio.mdc match AGENTS.md`).
  - `scripts/test_hos_desk_handoffs.py` (57 lines, `hos-only`) — 2 unit tests PASS.
  - `tests/test_flow_page_reuse.py` (104 lines, `hos-only`) — 5 unit tests PASS.
  - `tests/test_hos_code_graphic_resolution.py` (33 lines, `hos-only`) — 2 unit tests PASS.
  - `.github/workflows/*.yml` (8 workflow files, 690 lines total).
- **Findings in Area 4:**
  - Covered in **Finding F-02** (add `gemini` test to `scripts/test_hos_desk_handoffs.py`) and **Finding F-09** (wire `tests/test_flow_page_reuse.py` and `tests/test_hos_code_graphic_resolution.py` into `check_all.sh` and GitHub Actions).
  - One minor portability improvement in `scripts/core_sync.py` (`L19`, **CORE**): `PEERS` hardcodes `Path.home() / "YouTube" / "orbit-with-ben"` and `Path.home() / "YouTube" / "History Of Science"`; adding `REPO.parent / "orbit-with-ben"` and `REPO.parent / "history-of-science"` allows `core_sync.py push` to work seamlessly on `/Users/ben/_desk/worker/*` checkouts as well.

---

### Area 5: The 754 Per-Film Build Scripts Under `02_Video-Projects/` (261,112 Lines)

#### Quantitative Inventory of `02_Video-Projects/` Scripts

Across `02_Video-Projects/`, there are **754 script files (`.py`, `.sh`, `.js`, `.ts`, `.mjs`) totaling 261,112 lines of code**:

| Film Folder | Status | Total Scripts | Total Lines | Referenced in Receipts | Unreferenced Scripts (Lines) | Versioned Families (`>1` `_vNN`) | Superseded `_vNN` Files |
|---|---|---:|---:|---:|---:|---:|---:|
| `000_Explorer-Style-Test` | Test | 1 | 328 | 1 | 0 (0L) | 0 | 0 |
| `001_How-Did-We-Discover-Germs` | Live | 140 | 40,858 | 36 | 104 (29,412L) | 10 | 25 |
| `002_How-Did-We-Discover-The-Periodic-Table` | Live | 267 | 81,806 | 48 | 219 (66,104L) | 28 | 108 |
| `003_Invisible-Bones-X-Rays` | Live | 16 | 9,253 | 11 | 5 (2,618L) | 2 | 2 |
| `004_Whats-Really-Inside-An-Atom` | Live | 139 | 66,334 | 49 | 90 (40,115L) | 14 | 42 |
| `005_How-Harvey-Proved-Blood-Circulates` | Live | 91 | 17,998 | 32 | 59 (10,840L) | 5 | 11 |
| `006_Trees-Are-Made-Of-Air` | Live / Shorts | 40 | 13,668 | 22 | 18 (5,412L) | 3 | 6 |
| `007_The-First-Vaccine` | In prod | 24 | 12,491 | 14 | 10 (3,190L) | 1 | 2 |
| `008_Lightning-Franklin` | In prod | 22 | 12,461 | 13 | 9 (1,120L) | 1 | 1 |
| `009_The-Falling-Moon-Gravity` | In prod | 8 | 3,992 | 6 | 2 (227L) | 0 | 0 |
| `010_Alvarez-Clay-Line-Dinosaurs` | In prod | 3 | 1,877 | 3 | 0 (0L) | 0 | 0 |
| `013_Darwin-Wallace-Evolution` | Pre-prod | 3 | 46 | 1 | 2 (0L) | 0 | 0 |
| **TOTAL** | | **754** | **261,112** | **236** | **518 (159,038L)** | **64** | **197** |

#### Breakdown by Functional Category

| Category | Script Count | Total Lines | Share of Lines |
|---|---:|---:|---:|
| Long plate / still minting (`_mint_*`, `_gen_part*`, Flow/Vertex drivers) | 240 | 69,669 | 26.7% |
| Long assembly / rough cut / master join (`_assemble_*`, `_build_part*`, `_join_*`) | 215 | 65,766 | 25.2% |
| Shorts build & render (`_build_short_*`) | 86 | 52,936 | 20.3% |
| One-off debug / probe / harvest / schedule helpers (`_harvest_*`, `_probe_*`, `other`) | 64 | 27,262 | 10.4% |
| Long thumbnail & Short cover builders (`_paint_*`, `_build_thumb*`, `_make_cover*`) | 45 | 14,194 | 5.4% |
| Long QA / UAT / frame inspection (`_qa_*`, `_verify_*`, `_check_*`) | 31 | 13,504 | 5.2% |
| Long teach cards & code graphics (`code_graphic_*`, `_render_cards*`, timelines) | 14 | 4,784 | 1.8% |
| Shorts plate minting | 9 | 3,651 | 1.4% |
| Long music & SFX mixing (`_mix_*`, `_build_sfx_*`) | 12 | 3,325 | 1.3% |
| Long VO generation & Scribe alignment (`_gen_vo_*`, `_align_*`) | 22 | 2,883 | 1.1% |
| Shorts frame-0 / thumbnail helpers | 12 | 2,608 | 1.0% |
| Shorts VO generation | 4 | 530 | 0.2% |

---

#### Finding F-07A: How Much of the 754 Per-Film Scripts Is Copy-Paste That Shared Helpers Can Replace?

An AST/regex scan across all 754 scripts shows that **~80–85% of every per-film build script is copy-pasted boilerplate**:

| Duplicated Boilerplate Pattern / Function | Scripts Defining It | % of All 754 Scripts | Where It Is Copy-Pasted |
|---|---:|---:|---|
| `ffmpeg` subprocess wrapper (`def ff()`, `def run()`) | **389** | 51.6% | Every `_build_part*`, `_assemble_part*`, `_join_*`, `_build_short_*` |
| `ffprobe` duration/stream probe (`def probe_dur()`, `def probe()`) | **309** | 41.0% | Every part assembler, Short builder, QA script |
| Flow Veo UI invocation / gallery harvest (`def assert_auth()`, `def dismiss()`, `def run_harvest()`, `def dest_for()`) | **268** | 35.5% | 240+ `_mint_part*_flow_vNN.py` and `_harvest_*` scripts in `001`–`008` |
| SHA-256 receipt hashing (`def sha256()`, `def sha256_file()`) | **244** | 32.4% | Every Short builder, joiner, and mint receipt writer |
| Hardcoded `/Users/benjaminoats/...` path constants | **242** | 32.1% | Breaks running per-film scripts in worktrees or on MacBook |
| Pillow text/card rendering (`ImageDraw`, `ImageFont`, `def render_card()`, `def render_hook()`, `def render_side_label()`) | **236** | 31.3% | Every Short builder (frame-0 yellow hook word, 9–14s title card, end card) and long chapter/WHO/WHEN/FACT cards |
| House font loader (`Didot.ttc` / `Georgia` fallback) | **198** | 26.3% | Re-implemented inline in 198 scripts |
| `ffmpeg` crossfade (`xfade` / `acrossfade`) filtergraph builder | **110** | 14.6% | Part assemblers and Short builders |
| Loudness measurement & normalisation (`ebur128` / `volumedetect` / `loudnorm`, `def mean_db()`) | **99** | 13.1% | Joiners, Short builders, SFX mixers |
| 24fps CFR delivery encode (`fps=24`, `-r 24`, `libx264 -crf 18 -preset slow`) | **86** | 11.4% | Re-implemented inline instead of calling `04_Audio/tools/orbit_cfr_delivery.py` |
| Vertex Veo / Imagen REST polling loop (`predictLongRunning`, `fetchPredictOperation`) | **86** | 11.4% | Per-part start-still and Vertex plate minters |
| Short VO lift + `atempo` + word alignment (`def chunk_words()`, `def lifted_vo()`, `def caption_check()`, `def words_from_align()`) | **50** | 6.6% (58% of all 86 Short builders) | Almost every `_build_short_sNN_*.py` (500–750 lines each) is 90% identical code with only a 40-line `SHOTS` / `HOOK` config block changed! |
| Direct ElevenLabs HTTP calls (pre-`vo_take.py`) | **33** | 4.4% | Already superseded for new films by `04_Audio/tools/vo_take.py` |

##### Proposed Shared Helpers for Future Films (`011+`)
Creating **three shared library modules** in `00_Brand/Channel-Setup/tools/` will turn each future film's build scripts from ~3,000–15,000 lines of copy-pasted Python into declarative JSON/YAML manifests + thin CLI calls:

1. **`00_Brand/Channel-Setup/tools/hos_media.py` (~180 lines):**
   - Centralises `probe_dur(path)`, `probe_streams(path)`, `ff(args)`, `sha256_file(path)`, `mean_db(path)`, `extract_vo_lift(master_vo, t0, t1, atempo=1.0)`, `build_xfade_chain(clips, durations, fade_s)`, and delegates final encoding to `04_Audio/tools/orbit_cfr_delivery.py`.
   - Eliminates `def probe_dur`, `def ff`, `def sha256`, `def mean_db`, and inline CFR flags across all future long assemblers and Short builders.
2. **`00_Brand/Channel-Setup/tools/hos_cards.py` (~220 lines):**
   - Centralises house typography (`Didot.ttc` italic/bold loader), long chapter cards, *Teach on screen* overlays (`WHO`, `WHEN`, `FACT`, `DATA` cream-on-brown / white Didot italic cards with 0.3–0.6s ink/fade animation), and Shorts cards (`render_frame0_hook` with yellow hook word, `render_mid_title_card` at 9–14s, `render_end_card`, and `render_side_label`).
   - Eliminates the 236 duplicated Pillow `ImageDraw` card renderers.
3. **`00_Brand/Channel-Setup/tools/hos_short_builder.py` (~280 lines):**
   - Takes a declarative per-Short JSON spec (`10_Shorts/spec_s01_<slug>.json`: hook lines, yellow word,VO lift timestamps or standalone VO path, 6–7 plate paths + trim windows, mid-title text, music bed slice) and executes the entire build, caption check, `atempo <= 1.06` check, CFR encode, `SHORT_sNN_<slug>_vNN.json` receipt write, and `gate_shorts_open.py check`.
   - Replaces the 500–750 line `_build_short_sNN_vNN.py` scripts (86 scripts / 52,936 lines across `001`–`009`).

---

#### Finding F-07B: Archiving Strategy for Existing Per-Film Scripts in `02_Video-Projects/` (Respecting Provenance)

Per the job brief: *"Never touch shipped films' outputs or anything on the NAS; per-film build scripts of shipped films are provenance: propose archiving only with the receipts that point at them."*

1. **Keep in place (236 scripts, 102,074 lines):**
   - Every script in `001`–`010` whose filename is referenced by a live/canonical receipt (`PACKAGE_MANIFEST.json`, `SHORTS_RELEASE.json`, the active `SHORT_sNN_*_vNN.json` for each aired/scheduled Short, `production-status.md`, `JOIN_RECEIPT*.json`, `UAT_*.md`, or the 4 aired entries in `atempo_known_over_cap.json`) stays in its exact path in `02_Video-Projects/` as build provenance.
2. **Safe to archive to `_archive/02_Video-Projects/<NNN_Slug>/...` (518 scripts, 159,038 lines — 60.9% of all per-film script code):**
   - **Category 1 — 65 one-off debug, auth-probe, and gallery-harvest scripts (23,043 lines) with 0 receipt references:**
     - Examples in `001`: `_probe_flow_one_plate.py`, `_probe_part03_01_fast_v01.py`, `_harvest_part04_07_flow_v01.py`, `_harvest_part04_v19_still_clear.py`, `_gen_part04_fix_stills_v04.py`, `11_Upload-Package/Schedule/_calendar_restore_schedule_fix_v02c.py`, `11_Upload-Package/Schedule/_fix_related_s06_lister_v01.py`.
     - Examples in `002`: `_probe_flow_auth_part03_v02.py` through `_v09.py` (7 copies), `_harvest_force_download_v01.py` & `_v04.py`, `_harvest_newest_gallery_v01.py`, `_harvest_part03_v07..v09_force_download.py`, `_harvest_part04_v09..v10_edit_download.py`.
   - **Category 2 — 197 superseded `_v01.._v(N-1)` draft scripts across 64 versioned script families (~82,000 lines), archived together with their superseded `SHORT_*_v01..v(N-1).json` / rough-cut receipts:**
     - `001_How-Did-We-Discover-Germs`:
       - `_build_part04_rough_v01.py`, `_v20.py`, `_v21.py`, `_v22.py` (keep final `_v23.py`)
       - `_mint_part05_flow_v01.py`..`_v02c.py` (8 intermediate scripts; keep `_v02d.py`)
       - `10_Shorts/_build_short_s11_curved_flask_v01.py`..`_v06.py` + `SHORT_s11_curved_flask_v01..v06.json` (keep aired `_v07.py` + `_v07.json`)
       - `10_Shorts/_build_short_s01_childbed_hands_v01.py`..`_v06.py` + `SHORT_s01_childbed_hands_v01..v06.json` (keep aired `_v07.py` + `_v07.json`)
     - `002_How-Did-We-Discover-The-Periodic-Table`:
       - `_assemble_part01_rough_v01.py`..`_v13.py` (11 intermediate scripts; keep `_v14.py`)
       - `_assemble_part02_rough_v01.py`..`_v06.py` (4 intermediate scripts; keep `_v07.py`)
       - `_assemble_part03_rough_v01.py`..`_v08.py` (8 intermediate scripts; keep `_v09.py`)
       - `_assemble_part04_rough_v01.py`..`_v25.py` (25 intermediate scripts; keep `_v26.py`)
       - `_mint_part03_flow_v01.py`..`_v08.py` (8 intermediate scripts; keep `_v09.py`)
       - `_mint_part04_flow_v01.py`..`_v19.py` (14 intermediate scripts; keep `_v20.py`)
     - `004_Whats-Really-Inside-An-Atom` & `005_How-Harvey-Proved-Blood-Circulates`:
       - Intermediate `_assemble_part*_v01..v(N-1).py`, `_mint_part*_v01..v(N-1).py`, and superseded `_build_short_*_v01..v(N-1).py` + their matching `SHORT_*_v01..v(N-1).json` receipts.

---

## Recommended Implementation Sequence (PR Plan for Claude)

1. **PR 1 (Fast Bug Fixes & CI Alignment — Findings F-02, F-03, F-08, F-09):**
   - Add `"gemini"` to `hos_desk.py` `PARTIES`/`WRITERS` + test.
   - Guard `lift_words_006()` in `hos_build_rule_v02.py` when `_work_*` is absent so `--check` and `--test-negatives` pass everywhere.
   - Make `vo_check_py312.sh` worktree-relative.
   - Add the 8 missing Python test suites/checks to `check_all.sh` and `.github/workflows/`.
2. **PR 2 (Archive Retired `07_Content-Ops` Web App & Fix `vitest` — Findings F-01, F-11, F-14):**
   - Move `prisma/`, `src/app/`, `src/components/`, `src/workers/`, `src/lib/{publishing,oauth,security,storage}/`, `docs/`, one-off `scripts/_j09*`, and `tests/{autopublish,operator-auth}.test.ts` to `_archive/07_Content-Ops/`.
   - Drop `DATABASE_URL` requirement from `src/lib/env.ts` and switch `check_all.sh` + `hos-contract.yml` to run full `npx vitest run` (all 16 remaining test suites green).
3. **PR 3 (Clean `04_Audio/tools/` & `start_studio_chrome_cdp.sh` — Findings F-04, F-05, F-06, F-10):**
   - Archive `orbit_gemini_omni.py`, `orbit_gemini_veo.py`, `fix_published_playback_lag.py`, `vidiq_title_score_sheet.py` to `_archive/04_Audio/tools/`.
   - Remove Orbit-robot branches from `orbit_flow_veo_ui.py` and use `strip_cg_native_audio.py`.
   - Share `vo_check.py` normalisation with `vo_take.py` and wire `el_guard.py` into `ai_spend_hook.py`.
   - Remove `start_studio_chrome_cdp.sh` from `studio-core/CORE_FILES.json` in `orbit-with-ben` and archive it in both repos.
4. **PR 4 (Shared Film Build Helpers + Superseded Per-Film Script Archive — Findings F-07, F-12):**
   - Land `hos_media.py`, `hos_cards.py`, and `hos_short_builder.py` in `00_Brand/Channel-Setup/tools/` with unit tests.
   - Archive the 518 unreferenced/superseded per-film draft scripts + their superseded `SHORT_*_vNN.json` receipts to `_archive/02_Video-Projects/`, and prune the 18 retired entries from `atempo_known_over_cap.json`.
