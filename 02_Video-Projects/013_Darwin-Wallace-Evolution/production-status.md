# Production status — Evolution (Darwin's 20-year secret and Wallace's letter)

| Field | Value |
|---|---|
| Slug | `013_Darwin-Wallace-Evolution` |
| Channel | `@HistoryOfScienceYT` only |
| Topic | **Evolution** — Darwin's 20-year secret (*Notebook B* 1837 → 1844 essay → Wallace's 1858 letter → *Origin* 1859 → Jenkin/Mendel/Spencer) |
| Air (slotted) | **Thu 17 Dec 2026** 18:00 UK (`2026-12-17T18:00:00.000Z`) — locked in `J2231` (ready for Ben's OK by **Sun 13 Dec 2026**) |
| Stage | **VO locked** `hos_013_vo_v03a` (`J1310`, Chief h39 on J1301, 31 Oct 2026). Script v02 Chief PASS `J0307`. Active in `jobs/WIP.json` (`#541`); Shorts scripts v02 + upload package + shot list queued (`J2240` from `J2231`). |
| Neighbour gate | **PASS** (15 Oct 2026, `J0295`): 13 education ≥1M; TED-Ed/TED yes. Evidence `00_Brand/Channel-Setup/ideas/evidence_2026-10-15_J0295/n_darwin.json` |
| Script review | `01_Script/darwin_script_master_v02.md` (**92.6/100 PASS**, 1,227 spoken words, 8/8 structure gates) |
| FACT_NOTES | `01_Script/FACT_NOTES_v02.md` (`30 OK · 0 PARTIAL · 0 FLAG`, following `J0304` Gemini quote pass + `J0307` chronology/age updates) |
| VO | **locked** `hos_013_vo_v03a` (512.480 s, 8:32.48). WAV sha256 `837178125a72fb250d255f1039c5cb7f8630bbb313cf23801a1155f257d796e0`. MP3 sha256 `ada7eaa775104ee5dea9e9be98155abfc0b1e9fda010097f42ca9fa25bed7f85`. v01, v02 and v03 kept. See `02_Voiceover/VO_STATUS.md`. |
| Shorts VO | **accepted** (`J2246`, 6 Nov 2026; `J2288` KEEP, PR #444 merged 10 Nov 2026). `hos_013_short_A_v02` 26.64 s and `hos_013_short_B_v02` 26.00 s. Both `vo_check` PASS. See `10_Shorts/vo_v02/VO_STATUS.md`. |
| Picture | **Picture plan v02 (`J2558`, 11 Nov 2026) beside v01 (`J2476`, 10 Nov 2026).** `0` `Veo 3.1 - Fast` rows (5 former Fast rows swapped to £0 free rows + 18 upgraded to `Veo 3.1 - Quality`; wording from `#496` and `#498` kept word for word): **66 Quality mint rows** (`6,600` Flow credits try-1 / `17,094` expected) + **28 free rows** (`19` code graphics, `8` public-domain archive composites, `1` reuse). Runner `_mint_flow_v01_pass1.py` refuses `Veo 3.1 - Fast`; `PASS1_SCOPE_J2499.json` and `PASS1_MINT_PLAN_J2499.json` re-pinned to `v02` (`MAX_TOTAL_CREDITS = 6600`, `generation_authorized: false`). |
| Runtime target | 7–9 min, 6 parts (1,227 spoken words) |

## 19 Oct 2026 — Script v02 & Episode Gate (`J0307`)

### `npm run review:script` output

```text
# darwin_script_master_v02.md

**Decision:** PASS · **Score:** 92.6 / 100

| Dimension | Score |
|---|---:|
| hook | 9.5 |
| curiosity | 8.7 |
| storytelling | 8 |
| scientificAccuracy | 9.6 |
| emotion | 9.6 |
| escalation | 10 |
| retentionPotential | 9 |
| searchPotential | 9.1 |
| visualOpportunities | 9.5 |
| narrationFlow | 9.6 |

Words: 1569 · Est. min: 10.5 · Chapters: 5

## Findings

- **[info] overall:** Structure gates 8/8 — applied +1.05 completeness boost to supporting dimensions.
- **[info] overall:** PASS 92.6/100 — proceed to VO after production checklist.

Pass threshold: 90
```

### `npm run gate:episode` output

```text
# Episode gate — 013_Darwin-Wallace-Evolution

**Decision:** PASS — VO / Gemini Veo allowed

| Check | Status | Detail |
|---|---|---|
| project_dir | OK | Project: /Users/benjaminoats/YouTube/History Of Science/02_Video-Projects/013_Darwin-Wallace-Evolution |
| prebuild_vidiq | OK | Pre-build vidIQ audit present and looks signed off. |
| script_file | OK | Script: 01_Script/darwin_script_master_v02.md |
| script_review | OK | Script reviewer PASS 92.6/90 (need ≥90). |
| explorer_acts | OK | [EXPLORER ACTS] beats 1 (need ≥1). |
| visual_must | OK | [VISUAL MUST] count 24 (need ≥4). |
| teach | OK | [TEACH] count 6 (need ≥4). |
| chapters | OK | [CHAPTER CARD] count 5 (aim 4–6 film acts). |
| production_checklist | WARN | No PRODUCTION_CHECKLIST_V2.md yet — add before publish. |

Script score: **92.6/100** · PASS
```

## 31 Oct 2026 — VO recorded (`J0807`)

House voice, `eleven_v3`. Full take `hos_013_vo_v01` (512.70 s, −19.5 LUFS). One sentence said "credits" where the locked script says "credit" (5:34). Pickup `hos_013_pickup_credit_v01` is spliced into `hos_013_vo_v02`. v01 is untouched. No picture, no upload. Parked for Chief. Detail: `02_Voiceover/VO_STATUS.md`.

## 31 Oct 2026 — VO locked (`J1310`)

Chief h39 on J1301 passed v03. `hos_013_vo_v03a` is the locked take: the same words with six measured chapter-end fades. No re-take and no ElevenLabs. Chapter starts on the VO clock: ch01 1:15.50, ch02 2:51.08, ch03 4:36.26, ch04 6:06.34, ch05 7:28.16. Film 8:32.48. The 1.69 s beat after "into the open." at 0:20.34 is accepted; the editor may tighten it to no less than 0.6 s if the hook needs it. Detail: `02_Voiceover/VO_STATUS.md`.

## 5 Nov 2026 — Shorts scripts v02, Upload Package & Shot List v01 (`J2240`)

- **Slotted:** **Thu 17 Dec 2026** 18:00 UK (`2026-12-17T18:00:00.000Z`, `J2231`; active in `jobs/WIP.json` `#541`).
- **Shorts scripts v02 (`10_Shorts/SHORTS_SCRIPTS_v02.md`):** Two search-titled Test B Shorts checked against signed-out YouTube GB autocomplete (`10_Shorts/evidence_2026-11-05_shorts_search.json`):
  - **Short A (`10_Shorts/vo_v02/hos_013_short_A_v02.txt`, 60 words):** *How Did Darwin Discover Evolution?* (autocomplete: **yes**; payoff withheld past `14.5 s`).
  - **Short B (`10_Shorts/vo_v02/hos_013_short_B_v02.txt`, 61 words):** *What Is Survival of the Fittest?* (autocomplete: **yes**; payoff withheld past `15.0 s`).
  - Queued Shorts VO as **`J2246`** (`--kind vo`, `--needs mini`).
- **Upload package (`11_Upload-Package/`):** Built `PACKAGE_MANIFEST.json`, `PRODUCTION_CHECKLIST_V2.md`, `Descriptions/darwin_long_description_v01.txt` (chapters timed to `hos_013_vo_v03a`: `0:00, 1:15, 2:51, 4:36, 6:06, 7:28`; primary sources from `FACT_NOTES_v02.md`), and `Tags/darwin_long_tags_v01.txt`.
- **Shot list (`07_Edit-Project/SHOT_LIST_v01.md`):** 62 rows across 6 parts timed to `hos_013_vo_v03a` (`512.48 s`), with all 5 `DATA + SCALE` graphics, 11 `WHO` cards, 19 `WHEN` stamps, 4 `FACT` cards, and 2 Explorer beats outside the first minute.

### `npm run lint:package -- --film 013` output

```text
PASS  02_Video-Projects/013_Darwin-Wallace-Evolution/11_Upload-Package/PACKAGE_MANIFEST.json
   warn  [captions] no captionsFile (captions from the script)
```

### `npm run gate:episode` output

```text
# Episode gate — 013_Darwin-Wallace-Evolution

**Decision:** PASS — VO / Gemini Veo allowed

| Check | Status | Detail |
|---|---|---|
| project_dir | OK | Project: /Users/ben/_desk/worker/history-of-science/02_Video-Projects/013_Darwin-Wallace-Evolution |
| prebuild_vidiq | OK | Pre-build vidIQ audit present and looks signed off. |
| script_file | OK | Script: 01_Script/darwin_script_master_v02.md |
| script_review | OK | Script reviewer PASS 92.6/90 (need ≥90). |
| explorer_acts | OK | [EXPLORER ACTS] beats 1 (need ≥1). |
| visual_must | OK | [VISUAL MUST] count 24 (need ≥4). |
| teach | OK | [TEACH] count 6 (need ≥4). |
| chapters | OK | [CHAPTER CARD] count 5 (aim 4–6 film acts). |
| production_checklist | OK | Checklist present: 11_Upload-Package/PRODUCTION_CHECKLIST_V2.md |

Script score: **92.6/100** · PASS
```

## 6 Nov 2026 — Shorts VO recorded (`J2246`)

House voice, `eleven_v3`, speed 1.04. Two takes, one each, from the v02 txt files. Not a lock.

| Stem | Duration | vo_check | WAV sha256 |
|---|---|---|---|
| `hos_013_short_A_v02` | 26.64 s | PASS (pace warn 140 wpm) | `9f80fa1c22951b5f7d25b2365fa5d62a58e848898262e6d5365bb2e68047bef8` |
| `hos_013_short_B_v02` | 26.00 s | PASS (pace warn 143 wpm; Russel/Russell sounds-alike at 0:11.42) | `6745bd813bd390bdf5091460bd9b5425eca568e4dbb3cf37f2c0a53f70ad47c0` |

Scribe mismatches are the years only (`1835`, `1864`). ElevenLabs 90,171 → 89,847 left (delta 324). Nothing bought. Detail: `10_Shorts/vo_v02/VO_STATUS.md`.

## 10 Nov 2026 — Picture Plan v01 on Locked VO, Free Picture Built & QA'd, Paid Mint Priced (`J2476`)

- **Picture plan v01 (`07_Edit-Project/PICTURE_PLAN_v01.json`, `07_Edit-Project/PICTURE_PLAN_v01.md`, `07_Edit-Project/PRICE_REVIEW_v01.md`, `07_Edit-Project/parts/part-01_plates_v01.json .. part-06_plates_v01.json`, `10_Shorts/SHORTS_PICTURE_PLAN_v01.json`):**
  - 94 contiguous rows across `515.00 s` (`512.480 s` locked `hos_013_vo_v03a.wav` + `2.52 s` house cream end card). Every minted row (`Q` or `F`) is **`≤ 8.00 s`**, so 0 rows exceed a single 8 s Veo 3.1 clip.
  - **HOS-2026-11-E2 proof-first first 30 seconds (`0:00.00–0:40.00`):**
    - **CUTS (`0:00–0:30`):** 9 distinct moving plates overlapping `0:00–0:30` (`P1:01` `3.80 s`, `P1:02` `4.10 s`, `P1:03a` `4.00 s`, `P1:03b` `4.12 s`, `P1:04a` `2.98 s`, `P1:04b` `2.64 s`, `P1:05a` `4.00 s`, `P1:05b` `3.58 s`, `P1:06` `4.22 s`), max cut **`4.22 s ≤ 4.50 s`** — **PASS**.
    - **PROOF (`0:05–0:15`):** `P1:02` (`0:03.80–0:07.90`: hands locking *Notebook B* in drawer), `P1:03a` (`0:07.90–0:11.90`: unlabelled Galápagos finch skins with blank parchment tags), `P1:03b` (`0:11.90–0:16.02`: barnacle specimen jar, brass dissecting microscope, and Wallace's packet landing on desk) — **PASS**.
    - **EARLY (`0:25–0:40`):** `P1:08_cg_i_think_tree` starts at **`0:39.40`** (`0:39.40–0:54.30`, inside `0:25–0:40`), tracing the public-domain 1837 *Notebook B* p. 36 branching tree (`MS DAR 121:36`) + 20-year secrecy bar (`1838 → 1858`, `SCALE: 20 years in a drawer — longer than a child takes to grow up`) — **PASS**.
- **Free (`£0` / `0` credit) picture built and QA'd (23 rows + 10 WHO overlays):**
  - **16 code graphics, maps, diagrams, chapter cards & end card** + **6 public-domain archive composites** = **22 rendered `1920×1080` 30 fps H.264 `.mp4` clips + `.jpg` stills** in `07_Edit-Project/code_graphics_v01/` (and mirrored to `/Volumes/data/studio-live/History Of Science/02_Video-Projects/013_Darwin-Wallace-Evolution/07_Edit-Project/code_graphics_v01/`).
  - **17 verified Public Domain Wikimedia Commons files** in `07_Edit-Project/archive_pulls_v01/ARCHIVE_PULLS_RAW_v01.json` (7 historical scans/lithographs + 10 portraits rendered into framed circular cut-out overlays in `07_Edit-Project/code_graphics_v01/who_overlays/`).
  - **1 intra-film reuse (`P6:08a_reuse_study_beaks_callback`):** reuses the `[3.80s..8.00s]` tail of `P1:01_study_beaks` (`0` extra credits).
- **Cost table (71 rows need minting; `generation_authorized: false` on every row; parked behind HOS 009 and 010):**

| Part | Chapter title | Time (`in–out`) | Rows | Quality (`100`) | Fast (`10`) | Code graphic (`0`) | Free archive (`0`) | Reuse (`0`) | Mint rows | Free rows | Flow credits (try-1) | Flow credits (expected) | Vertex try-1 (£) | Vertex expected (£) |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Part 01 | The Twenty-Year Secret | `0:00.00–1:15.50` | 13 | 6 | 5 | 2 | 0 | 0 | 11 | 2 | 650 | 1,654 | £8.32 | £21.40 |
| Part 02 | The Birds He Forgot to Label | `1:15.50–2:51.08` | 16 | 9 | 3 | 3 | 1 | 0 | 12 | 4 | 930 | 2,391 | £11.04 | £28.43 |
| Part 03 | The Engine and the Barnacles | `2:51.08–4:36.26` | 19 | 8 | 6 | 4 | 1 | 0 | 14 | 5 | 860 | 2,192 | £11.68 | £29.58 |
| Part 04 | Fever in the Islands | `4:36.26–6:06.34` | 16 | 10 | 3 | 2 | 1 | 0 | 13 | 3 | 1,030 | 2,650 | £12.00 | £30.99 |
| Part 05 | The Night Nobody Noticed | `6:06.34–7:28.16` | 15 | 7 | 4 | 2 | 2 | 0 | 11 | 4 | 740 | 1,893 | £9.76 | £24.85 |
| Part 06 | The Missing Piece | `7:28.16–8:35.00` | 15 | 8 | 2 | 3 | 1 | 1 | 10 | 5 | 820 | 2,112 | £11.20 | £28.45 |
| **Total** | **Full film (`8:35.00`)** | `0:00.00–8:35.00` | **94** | **48** | **23** | **16** | **6** | **1** | **71** | **23** | **5,030** | **12,892** | **£64.00** | **£163.70** |

### `polish_gate.py` & `picture_qa.py` output on the 22 built free clips

```text
polish gate PASS: 0 of 22 rows failed, 4 to look at -> 02_Video-Projects/013_Darwin-Wallace-Evolution/07_Edit-Project/code_graphics_v01/polish_gate_v01.json
picture QA PASS: 0 of 22 cuts fail, 4 to look at -> 02_Video-Projects/013_Darwin-Wallace-Evolution/07_Edit-Project/code_graphics_v01/picture_qa_v01/PICTURE_QA.md, 02_Video-Projects/013_Darwin-Wallace-Evolution/07_Edit-Project/code_graphics_v01/picture_qa_v01/picture_qa_review.jpg
```

## 11 Nov 2026 — Picture Plan v02 with Zero Fast Rows, Scope Re-pinned & Runner Fast Refusal (`J2558`)

- **Ruling:** Chief Grok (`#180` comments `6774289583` item 3 and `6787044973`), modeled after `011` (`PR #495`, comment `6788217207`).
- **23 former `Veo 3.1 - Fast` rows resolved (`07_Edit-Project/FAST_ROW_CHANGE_v02.json`):**
  - **5 rows swapped to `£0` / `0`-credit free rows** (each strictly between two moving `Veo 3.1 - Quality` plates; `0` back-to-back graphics):
    1. `P2:10b_shipmate_tagged_tray` (`2:29.90–2:33.20`, `3.30 s`) → **`archive`**: John Gould, *Darwin's finches* lithograph (*Journal of Researches*, 2nd ed., 1845, p. 379), `07_Edit-Project/archive_pulls_v01/raw/gould_finches_1845.jpg` (`https://commons.wikimedia.org/wiki/File%3ADarwin%27s_finches_by_Gould.jpg`, **Public domain**, `sha256: 031197cb402d34912f6337cccd335a0ec353ae6d9fe86070c5d5b5a2dfac2acc`).
    2. `P3:09a_essay_1844_sealed` (`3:54.20–4:00.64`, `6.44 s`) → **`code-graphic`**: house inked case-file & timeline beat (230-page fair-copy manuscript stack sealed with red tape + timeline step `4/7 · July 1844`).
    3. `P4:07b_packet_to_mailbag` (`5:26.00–5:30.68`, `4.68 s`) → **`code-graphic`**: house inked route map graphic of Wallace's wax-sealed packet travelling along a map line from Ternate (early 1858) to Down House (arrived 18 June 1858), with no unsourced duration.
    4. `P5:02b_joint_papers_lectern` (`6:16.56–6:22.34`, `5.78 s`) → **`archive`**: William Edward Kilburn daguerreotype of Sir Joseph Dalton Hooker (c. 1852), `07_Edit-Project/archive_pulls_v01/raw/who_joseph_hooker.jpg` (`https://commons.wikimedia.org/wiki/File%3AJoseph_Dalton_Hooker_by_William_Kilburn_c1852.jpg`, **Public domain**, `sha256: 05f012a4529fdbe3e29e623e671129cb50daab727a6d41fae7b57fb2956a97fa`), composited on the 1 July 1858 Linnean Society joint papers dossier.
    5. `P5:04b_bell_report_1859` (`6:38.00–6:44.66`, `6.66 s`) → **`code-graphic`**: house inked May 1859 Linnean Society presidential annual report page (`FACT: NO STRIKING DISCOVERY`).
  - **18 rows upgraded to `Veo 3.1 - Quality` (`100` credits each):** `P1:03a_unlabelled_birds`, `P1:04a_packet_seal`, `P1:04b_drawer_unlock`, `P1:05b_museum_plaques`, `P1:06_padlock_shut`, `P2:04_blank_tags_row`, `P2:08b_gould_skins_closeup`, `P3:04a_drought_island_seeds`, `P3:07b_confessing_murder_letter`, `P3:13a_lyell_warning`, `P3:13b_brass_globe_turn`, `P4:09b_smashed_letter_pen`, `P4:10_fairness_25_june`, `P4:12_lyell_hooker_bundle`, `P5:04a_empty_linnean_hall`, `P5:08a_wallace_opens_origin`, `P6:02b_paint_pots_mix`, `P6:06a_origin_fifth_edition`.
- **Picture plan `v02` written beside `v01` (`_build_picture_plan_v02.py`, `PICTURE_PLAN_v02.{json,md}`, `PRICE_REVIEW_v02.md`, `SHOT_LIST_v02.md`, `parts/part-01..06_plates_v02.json`):**
  - **94 rows:** **66 `Veo 3.1 - Quality`** (`6,600` try-1 / `17,094` expected Flow credits), **0 `Veo 3.1 - Fast`**, **28 free rows** (`19` code graphics, `8` public-domain archive composites, `1` reuse).
  - Every prompt names nobody: the wording merged in `#496` (`f859ac84`) and `#498` (`d7f4849c`) is kept word for word across all 66 Quality rows.
- **Pass-1 scope (`PASS1_SCOPE_J2499.json`), mint plan (`PASS1_MINT_PLAN_J2499.json`), and runner (`_mint_flow_v01_pass1.py`):**
  - Re-pinned to `PICTURE_PLAN_v02.json` and `part-01..06_plates_v02.json` (`EXPECTED_ROW_COUNT = 66`, `EXPECTED_QUALITY_COUNT = 66`, `EXPECTED_FAST_COUNT = 0`, `MAX_TOTAL_CREDITS = 6600`, `14` batches).
  - `Veo 3.1 - Fast` removed from `MODEL_BY_QUALITY` and `PRICE_BY_QUALITY` and actively refused across scope loading, price acceptance, and live UI checks.
  - `generation_authorized: false` on every row; `0` credits spent (`£0`).

## STOP

- No Vertex/Veo/Flow minting on this film.
- The long VO stays locked as `hos_013_vo_v03a`. Do not re-record it.
- The two Shorts takes above are waiting on review. No further ElevenLabs on them unless that review orders one pickup.
- Do not merge or close desk PR #180 from this work.

## J2498 — diagnostic timing rough, 11 Nov 2026

Internal working cut: `07_Edit-Project/timing_rough_J2498/hos_013_timing_rough_J2498_v01.mp4` on studio-live. 515.00 s; 22 verified existing renders and 72 labelled slates. No generation or spend. See `07_Edit-Project/timing_rough_J2498/ROUGH_MANIFEST_v01.json` for full NAS path and SHA-256.

`clip_check.py`: **FAIL**, exit 1, `passed: false`, nine errors (full pasted JSON in `timing_rough_J2498/clip_check_v01.json`). Independent word-timestamp audit: 14 cuts inside words, 23 cuts inside sentences, five graphics over 8 s. Overlay onset unresolved; no new overlays composited. No stage PASS claimed.

Parked for Chief: resolve sentence-boundary cuts versus picture cadence, scope corrected v03 edit/overlay timings and five missing v02 free renders. Callback source unminted and its requested 4.40 s exceeds its 4.20 s source tail. Existing v01/v02 plans and generation authorization untouched. `TIMING_REPORT_v01.md` names every issue; `COST_OPTIONS_v01.md` offers three free alternatives saving 300 first-take / 777 expected credits if adopted. No Ben-watch submission, upload or schedule action.

Repository verification for the J2498 evidence PR: `check_all.sh` → **ALL CHECKS PASS** (summary pasted in `timing_rough_J2498/VALIDATION_v01.md`). This does not override the failed media timing check.

## J2652 checkpoint — 12 Nov 2026

110-beat v03 scope and 515-second diagnostic rough delivered to NAS; 45 word onset records. `clip_check`: passed=true, errors=[], warnings=[]. Repository check_all.sh: ALL CHECKS PASS. **Overall FIX, not stage PASS**: unsupported phrase cuts, four source-length overruns, short chapter titles and seven cue overlaps remain. £0. v02 and J1310 audio untouched. See `07_Edit-Project/timing_rough_J2652/REVIEW_v03.md`; J2652 is released for continuation, not finished.

### J2652 continuation — 12 November 2026, Codex

Cue-scope revision only; edit remains **FIX**, not approved. Evidence:
`07_Edit-Project/timing_rough_J2652/REVIEW_v03b.md` on PR #551.
43 cue intervals now avoid all seven earlier collisions; every named person
keeps the original word onset and a 3–4 s hold. Measured pauses at −45 dB
supply additional cut candidates without changing the WAV or transcript.
Nine inherited cuts, four source overruns and five brief chapter cards still
need correction before a new rough. No spend or generation; v02/v03 preserved.

Validation output (technical checks, not a film-stage PASS):

```text
CUE SCHEDULE PASS: 43 cues, zero collisions; names remain at their word onset for 3–4 s.
TIMING FIX: 9 unsupported existing cuts; 0 spans exceed 7 s without a verified boundary.
Ran 4 tests ... OK
ALL CHECKS PASS
Independent inherited cuts, 7 s cap, unchanged VO hash, and no-render guard: PASS
```

The repository-wide ALL CHECKS PASS does not waive the timing FIX. J2652
continues at 2 of 3; the next run must revise shot allocation and chapter
presentation, carry the repaired cues forward, then render and inspect a new
version. Nothing is waiting on Ben.
