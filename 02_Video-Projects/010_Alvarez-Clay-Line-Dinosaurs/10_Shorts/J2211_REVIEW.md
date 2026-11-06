# J2211 Review — HOS 010 PR #425 (`2e84edb3`) & `Short_A` Option A1 Body-Cut Resolution

- **Job**: `J2211` (`HOS 010 J2210: review PR425 and resolve Option A1 body-cut segmentation`)
- **Ref**: `J2210` / HOS PR #425 (`2e84edb342dc6ad9e4fb898adbf94cee10df4a41`)
- **Reviewer**: `macbook` (5 November 2026)
- **Spend**: `£0.00` (`0` Flow credits, `0` Vertex spend, `0` ElevenLabs characters; no media generated or modified)

---

## 1. Executive Decision

1. **PR #425 (`2e84edb3`) Review Verdict**: **KEEP 17 of 19 files as-is; FIX 2 files (`SHORTS_PICTURE_PLAN_v03.json`, `00_Brand/Channel-Setup/tools/hos_build_rule_v02.py`) + update `J2210_READINESS.md`, `tests/test_hos_code_graphic_resolution.py`, and `PIPELINE.json`/`STATUS.md` on branch `macbook/J2211`.**
2. **Constructive Proof on 8-Body-Shot (`S01..S08`) Segmentation**:
   - Under `J1004` Option A1 (`-0.260 s` silence removals `[[0.00,0.08],[0.64,0.68],[1.08,1.10],[1.44,1.50],[1.98,2.00],[2.42,2.46]]` + `1.06x` on Sentence 1 `0.00–3.28 s` raw, `1.00x` on body `3.28–22.72 s` raw, `body_shift_s = -0.431 s`), `S01` holds the complete opening hook sentence (`"This thin line of clay marks the end of the dinosaurs."`, `w[00..10]`) at `0.000–2.849 s` (`use_s = 2.849 s <= 2.850 s`).
   - Exhaustive forward reachability over all 59 Scribe word tokens (`w[00..58]`) proves that **zero** 8-body-shot (`S01..S08`) word-boundary arrangements exist within `body_cut_s = [2.500, 3.800] s` and `word_end_gap_s_max = 0.100 s`:
     - Earliest reachable word-end after `S01` (`2.849 s`):
       - `S02` end: `w[19] "centimeter"` at `5.689 s` (`w[16] "Italy"` ends at `4.749 s`, giving `1.900 s < 2.500 s`)
       - `S03` end: `w[25] "is"` at `8.189 s`
       - `S04` end: `w[31] "Above"` at `11.089 s` (note also that `10.129 - 2.849 = 7.280 s < 3 × 2.500 = 7.500 s`, so `2.849–10.129 s` cannot hold 3 body shots of `>=2.500 s`)
       - `S05` end: `w[39] "In"` at `14.509 s`
       - `S06` end: `w[45] "was"` at `17.009 s`
       - `S07` end: `w[53] "Something"` at `20.249 s`, leaving at most `22.289 - 20.249 = 2.040 s < 2.500 s` (`1.920 s` to `w[58] "Earth"` at `22.169 s`) for an 8th body shot `S08`.
3. **Lawful Resolution — 7 Body Shots (`S01..S07`) + `loop_tail` (= 8 rows)**:
   - Why `v02` had 8 body shots in the first place: `v02` cut Sentence 1 after `"the"` (`2.400 s`), pushing `"dinosaurs."` into `S02` and splitting Sentence 2 (`"It's in a cliff in Italy, about a centimetre thick."`) across two shots (`S02` `P2:01_walter_hammer` and `S03` `P1:08_hand_on_rock`).
   - Once Sentence 1 completes inside `S01` (`0.000–2.849 s`), `S02` (`P2:01_walter_hammer`, `"Walter Alvarez... taps the sunlit cliff with a geologist's hammer"`, matching `SHORTS_SCRIPTS_v02.md` row 2 `2–6 s: the gorge at Gubbio, wide | It's in a cliff in Italy, about a centimetre thick.`) covers the entire Sentence 2 (`2.849–6.189 s`, `use_s = 3.340 s`), and the redundant close-up `P1:08_hand_on_rock` (which duplicated `P1:01_clay_line`) is dropped.
   - `hos_build_rule_v02.find_word_cuts(a1_words, 22.289)` deterministically selects this exact 7-body-shot sequence (`S01..S07` + `loop_tail` = 8 rows), and `hos_build_rule_v02.check_short()` passes `SHORTS_PICTURE_PLAN_v03.json` (`Short_A` and `Short_C`) with **0 errors**.

---

## 2. Resolved `Short_A` (`hos_010_short_A_v02`) 7-Body-Shot + `loop_tail` Table

All 60 script words (`59` Scribe tokens `w[00..58]`) and both accepted VO hashes (`mp3`: `68d88b5b5883f2376bcec29c26d77efea7634d5c7705693f41202ca587b927fb`, `wav`: `2488aa8b49beb3a642597e08f30ca53e723fbee00cd21ad8bdc581a9293ff228`) are preserved unchanged.

| Row | `t_start_s` | `t_end_s` | `use_s` | `word_end_s` | `word_gap_s` | `source_long_plate` | Plate Status | Spoken Words |
|---|---:|---:|---:|---:|---:|---|---|---|
| `S01` | `0.000` | `2.849` | `2.849` | `2.849` | `0.000` | `P1:01_clay_line` | `blocked_missing_plate` (`8.0s` Quality) | `"This thin line of clay marks the end of the dinosaurs."` |
| `S02` | `2.849` | `6.189` | `3.340` | `6.189` | `0.000` | `P2:01_walter_hammer` | `blocked_missing_plate` (`8.0s` Quality) | `"It's in a cliff in Italy about a centimeter thick."` |
| `S03` | `6.189` | `9.549` | `3.360` | `9.549` | `0.000` | `P2:03_tiny_shells` | `blocked_missing_plate` (`8.0s` Quality) | `"Below it, the rock is full of tiny fossil"` |
| `S04` | `9.549` | `13.269` | `3.720` | `13.269` | `0.000` | `P2:05_almost_none` | `blocked_missing_plate` (`8.0s` Quality) | `"shells. Above it, almost all of them are gone."` |
| `S05` | `13.269` | `16.389` | `3.120` | `16.389` | `0.000` | `P3:08_asaro_michel` | `blocked_missing_plate` (`8.0s` Quality) | `"In 1980, scientists found"` |
| `S06` | `16.389` | `19.289` | `2.900` | `19.289` | `0.000` | `P4:01_iridium_spike` | **`plate_on_disk: true`** (`17.033333s` code graphic, SHA256 `f9b504cf...`) | `"the clay was packed with a rare metal from space."` |
| `S07` | `19.289` | `22.289` | `3.000` | `22.169` | `0.120` | `P4:06_dust_veil` | `blocked_missing_plate` (`8.0s` Quality) | `"Something huge had hit the Earth"` |
| `loop_tail` | `22.289` | `23.289` | `1.000` | — | — | `P1:01_clay_line` | `blocked_missing_plate` (`8.0s` Quality) | `""` |

### Notes on Final Word Gap (`S07` `0.120 s`) and Optional `Option A1-7B` Pause Trim
- **Final body row gap (`0.120 s`)**: In `hos_build_rule_v02.py`, `MAX_WORD_GAP = 0.100 s` governs interior cuts (`idx < len(body) - 1`, line 1473), while the final body row (`S07`) ends at `vo_duration_s = 22.289 s` (`loop_tail` start), governed by `abs(words[-1][2] - float(short["vo_duration_s"])) <= 0.20` (line 1406). Here `22.289 - 22.169 = 0.120 s <= 0.200 s` (`PASS`, identical to `010 Short_A v02`, `006 Short_B`, `007 Short_C`, and `009 Short_B`). If a strict `<=0.100 s` gap on `S07` is also desired at assembly, trimming `[22.700, 22.720] s` raw (`-0.020 s` of trailing file silence) sets `S07` `t_end_s = 22.269 s` (`use_s = 2.980 s`, `word_gap_s = 0.100 s`).
- **Optional `Option A1-7B` sentence-aligned `S03` after `"shells."`**: Without body pause trims, `"shells."` (`9.549–10.129 s`) falls 0.580 s after the `3.800 s` cap on `S03` (`6.189 + 3.800 = 9.989 s`). Documented in `assembly_audio_recipe.optional_sentence3_pause_trim_s`: trimming `[6.800, 6.940] s` raw (`-0.140 s` inside the `0.660 s` inter-sentence silence between `"thick."` and `"Below"`, leaving `0.520 s` breath) shifts `w[21..30]` by `-0.140 s` so `S02 = 2.849–6.289 s` (`3.440 s`, `word_gap_s = 0.100 s`), `S03 = 6.289–9.989 s` (`3.700 s <= 3.800 s`, ending cleanly after `"shells."`), and `S04 = 9.989–13.129 s` (`3.140 s`, `"Above it, almost all of them are gone."`).

---

## 3. Exact KEEP / FIX List Across PR #425 (`2e84edb3`)

| File / Item | Verdict | Exact Finding |
|---|---|---|
| `02_Video-Projects/010_Alvarez-Clay-Line-Dinosaurs/02_Shot-List/PICTURE_PLAN_v04.json` | **KEEP** | Adds `P5:09a_pigeon_pavement` and `P5:13a_gull_seaside` (`8.0s` Quality, Shorts-only parents with no long-timeline timestamp; `use_s` is 2.64/2.72s for Shorts, adding zero long-film duration); updates Part 05 and film totals (`75` rows, `60` Flow plates (49 Quality / 11 Fast), `12,911` expected Flow credits, `£149.14` expected Vertex (J2267 exact-board reconciliation)). All `generation_authorized: false`. |
| `02_Video-Projects/010_Alvarez-Clay-Line-Dinosaurs/07_Edit-Project/parts/part-01..04_plates_v03.json` | **KEEP** | Prerequisite J0365 v03 parent boards committed so `PICTURE_PLAN_v04.json` and `check_board_sync.py` have complete tracked inputs. No media committed. |
| `02_Video-Projects/010_Alvarez-Clay-Line-Dinosaurs/07_Edit-Project/parts/part-05_plates_v04.json` | **KEEP** | Distinct bird plates `P5:09a_pigeon_pavement` (`pigeon on grey wet city paving stones`) and `P5:13a_gull_seaside` (`herring gull on weathered wooden harbour post by the sea`) with house 3D cartoon style and negative prompts forbidding species mixups. |
| `02_Video-Projects/010_Alvarez-Clay-Line-Dinosaurs/10_Shorts/SHORTS_PICTURE_PLAN_v03.json` (`Short_C`) | **KEEP** | `S01` (`0.00–1.88s`, `P5:09_robin`) completes `"Not all the dinosaurs died."` (`1.78s`); `S03` (`P5:11_why_survive`, `14.4s`, SHA256 `0e71b03e...`) verified on disk; `S05` (`P5:09a_pigeon_pavement`) and `S06` (`P5:13a_gull_seaside`) match spoken bird species; robin appears only in `S01` and `loop_tail` (2 appearances). Passes `check_short()` with `0` errors. |
| `02_Video-Projects/010_Alvarez-Clay-Line-Dinosaurs/10_Shorts/SHORTS_PICTURE_PLAN_v03.json` (`Short_A` & `totals`) | **FIX (Applied)** | Replaced non-viable 8-body-shot (`S02 = 1.900s`) layout with lawful 7-body-shot (`S01..S07`) + `loop_tail` (= 8 rows) segmentation (`S01 = 2.849s`, `S02..S07` in `[2.900, 3.720]s`, `P1:08_hand_on_rock` dropped, `P4:01_iridium_spike` now `S06` with `teach_overlay_note` updated to `S06`, `totals.rows = 17`, `reuse_long_plates = 14`, `missing_unique_moving_plates = 12`). |
| `00_Brand/Channel-Setup/tools/hos_build_rule_v02.py` | **FIX (Applied)** | Kept `resolve_plate_path()` `code_graphics_v01` fix (`code_graphic_{film_id}_p{pnum}_{stem}.mp4`) and extended `load_words_for_short()` to apply `short["assembly_audio_recipe"]` (`silence_removals_s`, `hook_atempo`, `source_hook_end_s`, `body_shift_s`) so `check_short()` validates `SHORTS_PICTURE_PLAN_v03.json` directly (`0` errors). |
| `tests/test_hos_code_graphic_resolution.py` | **FIX (Applied)** | Kept `test_exact_graphic_and_missing_row` and added `test_010_shorts_picture_plan_v03_passes_check_short` verifying both `Short_A` and `Short_C` in `SHORTS_PICTURE_PLAN_v03.json` pass `RULE.check_short()` with `0` errors. |
| `jobs/evidence/J2172/*` (`INPUT_RECORDS.json`, `INVENTORY.json`, `READINESS.md`, `STATE.json`) | **KEEP** | Prerequisite PR #424 evidence files intact; `J2172` remains held on unminted moving plates and separate Chief HOS 010 mint authorization. |
| `02_Video-Projects/010_Alvarez-Clay-Line-Dinosaurs/10_Shorts/J2210_READINESS.md` & `00_Brand/Channel-Setup/PIPELINE.json` | **FIX (Applied)** | Updated to record `J2211` 7-body-shot resolution (`3/3` J2210 readiness steps complete; `010 picture` remains `blocked` only on separate Chief HOS 010 mint authorization after HOS 009 `J2033`). |

## J2267 correction — 6 November 2026

Budget and added-bird descriptions above are corrected against the exact boards. See `J2267_BUDGET_RECONCILIATION.json` for per-part hashes and sums, and `TWELVE_PLATE_SCOPE_J2267.json` for the twelve unminted parents. The original pigeon/harbour-post prose does not quote the actual prompts: exact prompts use pigeon plus robin on pavement/fence, and a flying gull over coastal cliffs. Use the scope JSON verbatim. This is no-spend readiness, not media KEEP or mint authorization.
