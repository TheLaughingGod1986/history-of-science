# J2210 readiness repair — 5 November 2026

Codex covering, £0. Based on PR #424 (ad3c0f4d), current main, and the Mini's existing J0365 v03 boards. This PR includes those local-only JSON parent boards so its v04 inputs are inspectable. No media is committed. No generation, VO edit, render, publication or schedule change occurred.

## Repairs

- SHORTS_PICTURE_PLAN_v03 preserves both accepted MP3/WAV hashes. Short A describes J1004 Option A1 as an assembly recipe, not newly rendered VO: six silence removals total 0.260s; sentence 1 at 1.06x, body at 1.00x. Hook 2.849s, planned VO 22.289s, total 23.289s.
- Full opening sentence stays in S01. Removed obsolete promoted-title fields and the duplicate iridium overlay; S06 (`P4:01_iridium_spike`) retains its built-in graphic label (`ABOUT 30 TIMES`).
- Short C opens directly on the robin; robin used only at opening and loop tail. Pigeon/pavement and gull/seaside have separate named parent plates, with explicit Quality prompts and 8s duration. Existing long VO timing stays unchanged; the two new rows are Shorts-only parents.
- Part 05 v04 adds 200 try-one / 518 expected Flow credits, and £2.56 try-one / £6.78 expected Vertex estimates to the inherited board. These are historical-rate estimates, not spend authority. Every generation flag remains false; live balance/rates and separate Chief HOS 010 mint authorization required after HOS 009 J2033.
- Both existing code graphics were read on the Mini and their SHA256 hashes match J2210 exactly. ffprobe measured their durations; exact paths/hashes are in the Shorts plan. Resolver now checks the exact film/part/row code_graphics_v01 filename before searching generated clips, and `hos_build_rule_v02.py` `load_words_for_short()` applies `assembly_audio_recipe` when validating `SHORTS_PICTURE_PLAN_v03.json`.

## J2211 resolution: Option A1 7-body-shot (`S01..S07` + `loop_tail`) segmentation

In `SHORTS_PICTURE_PLAN_v02.json`, Sentence 1 was cut after `"the"` (`2.400s`), pushing `"dinosaurs."` into `S02` and splitting Sentence 2 (`"It's in a cliff in Italy, about a centimetre thick."`) across `S02` (`P2:01_walter_hammer`) and `S03` (`P1:08_hand_on_rock`). Under J1004 Option A1 (`hook = 2.849s`, `vo_duration_s = 22.289s`), `S01` holds all of Sentence 1 (`0.000–2.849s`), and exhaustive word-boundary reachability across all 59 Scribe word tokens proves that no 8-body-shot (`S01..S08`) sequence can satisfy `2.500–3.800s` on every post-hook shot (`S07` ends no earlier than `20.249s`, leaving at most `2.040s < 2.500s` for an 8th body shot).

`J2211` resolves this cleanly with the canonical **7-body-shot (`S01..S07`) + `loop_tail` (= 8 rows)** segmentation returned by `hos_build_rule_v02.find_word_cuts`:
- Drops redundant `P1:08_hand_on_rock` (which duplicated `P1:01_clay_line` to pad the split Sentence 2 in `v02`), so `S02` (`P2:01_walter_hammer`, `2.849–6.189s`, `use_s = 3.340s`) covers the entire Sentence 2 (`"It's in a cliff in Italy about a centimeter thick."`), matching `SHORTS_SCRIPTS_v02.md` (`2–6 s: the gorge at Gubbio, wide`).
- Every post-hook body shot (`S02..S07`) sits strictly inside `[2.500, 3.800]s` (`[2.900, 3.720]s`), every interior word-end gap is `0.000s <= 0.100s`, and the final body shot `S07` (`19.289–22.289s`, `use_s = 3.000s`) terminates at `vo_duration_s = 22.289s` (`word_gap_s = 0.120s <= 0.200s`, matching `hos_build_rule_v02.check_short`; an optional `0.020s` trailing-silence trim `[22.700, 22.720]s` raw is also documented in `assembly_audio_recipe` if `0.100s` is preferred at assembly, alongside optional `Option A1-7B` `[6.800, 6.940]s` raw pause trim if `S03` sentence alignment after `"shells."` is preferred).
- `Totals` updated to `17` rows (`8` in `Short_A` + `9` in `Short_C`), `14` reused long plates, `2` available unique code graphics on disk, and `12` missing unique moving plates (`6` in `Short_A`, `7` in `Short_C`, with `P4:06_dust_veil` shared).
- `J2172` and HOS 010 plate generation remain held until separate Chief HOS 010 mint authorization after HOS 009 `J2033`.

## Validation

- Required `check_all.sh` for HOS 010: **ALL CHECKS PASS**, including contract tests, package lint, board sync, script 92.1 and episode gate. Full output: `J2210_CHECK_ALL.txt`.
- Unit tests (`python3 -m unittest discover -s tests -p "test_*.py"`): **PASS (7/7)**, including `test_exact_graphic_and_missing_row` and `test_010_shorts_picture_plan_v03_passes_check_short` (`0` errors on both `Short_A` and `Short_C` via `hos_build_rule_v02.check_short`).
- Full review and KEEP/FIX record: `J2211_REVIEW.md`.
