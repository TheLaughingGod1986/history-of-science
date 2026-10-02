# Production status — 005 The Tied Arm That Proved Your Blood Circulates

| Field | Value |
|---|---|
| Slug | `005_How-Harvey-Proved-Blood-Circulates` |
| Channel | `@HistoryOfScienceYT` only |
| Topic | Ben picked: **Blood (Harvey)**, 1 Oct 2026 (chat with Claude) |
| Neighbour gate | PASS: 8 education videos with 1M+ views, TED-Ed yes (`11_Upload-Package/evidence_2026-10-01_neighbours.json`) |
| Pre-build vidIQ audit | filled from public signals; **vidIQ waived by Ben, 1 Oct 2026**; signed |
| Script sign-off | **Script v02 signed off by Ben, 1 Oct 2026** ("1–5 yes, 29 Oct", in chat with Claude; relayed on desk PR #180) |
| Script review | 89.8 with the fixed reviewer (#185). v02 signed off by Ben, 1 Oct 2026 (gate override, STUDIO_PLAYBOOK §2) |
| Episode gate | Every line OK except `script_review` 89.8 (Ben's recorded override, as on 004), 1 Oct 2026 |
| lint:package | PASS, 1 Oct 2026, schedule 29 Oct (captions warning) |
| VO | **Voice v01 (listen file sha `a19569f4…`, 8:15.33) OK'd by Ben, 1 Oct 2026** ("waive vidIQ, merge #186 and voice OK", in chat with Claude; relayed on desk PR #180). All `vo_check.py` PASS |
| Picture | **Part 01 rough v01 passed by Ben, 1 Oct 2026** ("Part 1 OK", in chat with Claude; relayed on desk PR #180 comment 5942662028), as it is, including the ECG-style pulse and the quill: `09_Final-Export/hos_005_part01_rough_v01.mp4`, sha256 `7661b6cf1897c6dabe60e09592b297f9ed21b253cb7c2946cc12f58732a9d098`. Parts 02–05 on Vertex AI Veo 3.1 in progress (boards v02 + Fast-plate light fix). Ben's moving-picture sign-off for the film is the full join |
| Runtime target | 7–9 min, 5 parts. Film VO timeline 8:21.33 with the four chapter cards (`07_Edit-Project/VO_RETIME_v01.json`), + 3–4 s end card ≈ 8:25 |
| Air | **Thu 29 Oct 2026 18:00 UK = 18:00 UTC** (`2026-10-29T18:00:00.000Z`; clocks go back 25 Oct), normal publish (no Premiere). Ben, 1 Oct. Not yet uploaded |
| Shorts | 3 planned (Fri 30 Oct, Sun 1 Nov, Tue 3 Nov, 11:30 UK = 11:30 UTC), one a day, none before the long is public, Related → this long. **Shorts A–C signed off by Ben, 1 Oct 2026** (`10_Shorts/SHORTS_SCRIPTS_v01.md`). Not built yet: cut from the long's plates once those exist |

## STOP

- **Picture:** Ben's moving-picture sign-off (5) for the film is on the full join v01, after Parts 02–05 pass Claude's still review and my UAT. Spend stops if the projected Vertex Free Trial credit would fall below £60.
- Resolved: Part 01 rough v01 passed by Ben, 1 Oct 2026 ("Part 1 OK").
- Resolved: the Flow-credits STOP (1 Oct 23:45) is replaced by Vertex AI Veo for 005 with Ben's OK. Shorts scripts signed off by Ben, 1 Oct 2026.

**Rule record:** Vertex AI Veo used for 005 with Ben's OK, 1 Oct 2026 (Flow at 62 credits, Gemini 402). Vertex isn't in `STUDIO_PLAYBOOK.md` §5's engine table yet; Claude adds it in its own docs PR.

## 1 Oct 2026 — topic, script v01, gates (Grok)

`npm run review:script -- --file ../02_Video-Projects/005_How-Harvey-Proved-Blood-Circulates/01_Script/blood_script_master_v01.md`

```
**Decision:** REJECT · **Score:** 84.4 / 100

| hook | 7.5 | curiosity | 7.5 | storytelling | 8 | scientificAccuracy | 7.6 | emotion | 9.6 |
| escalation | 7 | retentionPotential | 9 | searchPotential | 9.1 | visualOpportunities | 9.5 | narrationFlow | 9.6 |

Words: 1356 · Est. min: 9 · Chapters: 4
- [warn] hook: No question mark in the first spoken window — consider an immediate unanswered question.
- [info] overall: Structure gates 8/8 — applied +1.05 completeness boost to supporting dimensions.
- [fail] overall: Total 84.4/100 is below pass threshold 90. Rewrite before VO or picture gen.
```

`npm run gate:episode -- --project ../02_Video-Projects/005_How-Harvey-Proved-Blood-Circulates`

```
**Decision:** BLOCK — VO / Gemini Veo blocked
| project_dir | OK |
| prebuild_vidiq | FAIL | Pre-build vidIQ audit exists but sign-off incomplete (tick keywords/title/script reviewer + Signed off by). |
| script_file | OK | Script: 01_Script/blood_script_master_v01.md |
| script_review | FAIL | Script reviewer REJECT 84.4/90 (need ≥90). |
| explorer_acts | OK | [EXPLORER ACTS] beats 3 (need ≥1). |
| visual_must | OK | [VISUAL MUST] count 45 (need ≥4). |
| teach | OK | [TEACH] count 4 (need ≥4). |
| chapters | OK | [CHAPTER CARD] count 4 (aim 4–6 film acts). |
| production_checklist | OK |
```

`neighbours.py "blood circulation" "william harvey" "how the heart pumps blood" --phrase blood --phrase heart --manifest …`: gate PASS, 8 big neighbours, TED-Ed yes; block written to `PACKAGE_MANIFEST.json`.

`npm run lint:package -- --film 005`

```
PASS  02_Video-Projects/005_How-Harvey-Proved-Blood-Circulates/11_Upload-Package/PACKAGE_MANIFEST.json
   warn  [captions] no captionsFile (captions from the script)
```

Note: the gate first read the audit as signed because its "Signed off by" pattern accepted the words "pending Ben" as a name. The line is now an em dash, so the gate reports it honestly. The gate's pattern itself is unchanged; any fix to it needs its own PR with Ben's OK.

## 1 Oct 2026 — script v02 (Grok, from Claude's desk review)

`01_Script/blood_script_master_v02.md` is live; v01 renamed to `01_Script/blood_script_v01.md`.

- Part 01 now has its `## PART 01` header and a `[TEACH]`. No chapter card and no Explorer in Part 01: `STUDIO_PLAYBOOK.md` §3 says part 01 has no chapter card and the Explorer is never in the first minute, and Part 01 now ends at 0:56. 004 v02 does the same.
- Cut from 1,301 to 1,257 spoken words. The stove image lives only in Part 02 (Galen); Part 03 keeps the cold room and hard bench and drops the re-introduction (and the St Bartholomew's cue); two small repeats trimmed in Parts 04–05.
- The first three lines are unchanged.
- Part 04: "more than nine years at the College" now leads into the tied arm; the 1628 book and Aubrey follow the experiment.
- Cue times re-estimated at 150 wpm (0:00–0:56 · 0:56–2:35 · 2:35–4:20 · 4:20–6:32 · 6:32–8:28). Re-time from the recorded VO before plate boards. `part-01_plates_v01.json` was built on v01 and is stale.
- Stakes line now at ~0:28 (was 0:35); rule is by 0:25.

`npm run review:script -- --file ../02_Video-Projects/005_How-Harvey-Proved-Blood-Circulates/01_Script/blood_script_master_v02.md`

```
# blood_script_master_v02.md

**Decision:** REJECT · **Score:** 84.4 / 100

| Dimension | Score |
|---|---:|
| hook | 7.5 |
| curiosity | 7.5 |
| storytelling | 8 |
| scientificAccuracy | 7.6 |
| emotion | 9.6 |
| escalation | 7 |
| retentionPotential | 9 |
| searchPotential | 9.1 |
| visualOpportunities | 9.5 |
| narrationFlow | 9.6 |

Words: 1325 · Est. min: 8.8 · Chapters: 4

## Cold open excerpt

> The Tied Arm That Proved Your Blood Circulates (script master v02) PART 01: The Used-Up Blood (0:00–0:56). No chapter card. Your heart pumps more blood in half an hour than your whole body holds. For fourteen hundred years, doctors taught that blood was made fresh from food and u

## Findings

- **[warn] hook:** No question mark in the first spoken window — consider an immediate unanswered question.
- **[info] overall:** Structure gates 8/8 — applied +1.05 completeness boost to supporting dimensions.
- **[fail] overall:** Total 84.4/100 is below pass threshold 90. Rewrite before VO or picture gen.

Pass threshold: 90
```

`npm run gate:episode -- --project ../02_Video-Projects/005_How-Harvey-Proved-Blood-Circulates`

```
# Episode gate — 005_How-Harvey-Proved-Blood-Circulates

**Decision:** BLOCK — VO / Gemini Veo blocked

| Check | Status | Detail |
|---|---|---|
| project_dir | OK | Project: /Users/benjaminoats/YouTube/hos-005-blood/02_Video-Projects/005_How-Harvey-Proved-Blood-Circulates |
| prebuild_vidiq | FAIL | Pre-build vidIQ audit exists but sign-off incomplete (tick keywords/title/script reviewer + Signed off by). |
| script_file | OK | Script: 01_Script/blood_script_master_v02.md |
| script_review | FAIL | Script reviewer REJECT 84.4/90 (need ≥90). |
| explorer_acts | OK | [EXPLORER ACTS] beats 3 (need ≥1). |
| visual_must | OK | [VISUAL MUST] count 45 (need ≥4). |
| teach | OK | [TEACH] count 5 (need ≥4). |
| chapters | OK | [CHAPTER CARD] count 4 (aim 4–6 film acts). |
| production_checklist | OK | Checklist present: 11_Upload-Package/PRODUCTION_CHECKLIST_V2.md |

Script score: **84.4/100** · REJECT

Cold open: The Tied Arm That Proved Your Blood Circulates (script master v02) PART 01: The Used-Up Blood (0:00–0:56). No chapter card. Your heart pumps more blood in half an hour than your whole body holds. For …

## Next actions

- Fix **prebuild_vidiq**: Pre-build vidIQ audit exists but sign-off incomplete (tick keywords/title/script reviewer + Signed off by).
- Fix **script_review**: Script reviewer REJECT 84.4/90 (need ≥90).
```

## 1 Oct 2026 — schedule 29 Oct + VO v01 (Grok, desk task from Claude, comment 5941493885)

### Schedule

Ben, 1 Oct, in chat with Claude: "1–5 yes, 29 Oct". Script v02 signed off by Ben, 1 Oct 2026. `PACKAGE_MANIFEST.json` `schedule` = `2026-10-29T18:00:00.000Z` (Thu 18:00 UK; UK = UTC after 25 Oct). Shorts drafted for Fri 30 Oct, Sun 1 Nov and Tue 3 Nov at 11:30 UK = 11:30 UTC (`11_Upload-Package/LAUNCH_PLAN.md`). Nothing uploaded or scheduled on YouTube.

`npm run lint:package -- --film 005`

```
PASS  02_Video-Projects/005_How-Harvey-Proved-Blood-Circulates/11_Upload-Package/PACKAGE_MANIFEST.json
   warn  [captions] no captionsFile (captions from the script)
```

### VO v01

- **Voice:** Ben Orbit Narrator (`kDch6ACCIpqgQ0NsU9kk`, `eleven_v3`), `settings_for_part(n)`, speed 1.04 on every part. Text = `blood_script_master_v02.md` word for word, using the same line filter as `vo_check.py` (`02_Voiceover/partNN_*_v01.txt`). Generator `02_Voiceover/_generate_all_vo_v01.py`, finish `02_Voiceover/_finish_vo_v01.py`, records `VO_TAKES_v01.json` and `VO_FINISH_v01.json`.
- **First takes:** Part 01 PASS. Parts 02 and 04 peaked at −0.9 / −0.5 dB, Part 05 had a 1.63 s pause, and Part 03 transcribed "Picture yourself" as "pitch yourself" and "what he saw" as "what you saw".
- **Fixes (sentence alone, same words):** `_qa_what_he_saw_v01a` and `_qa_picture_yourself_v01b` spliced into Part 03 at the silences around each sentence. `_qa_picture_yourself_v01a` was clean on its own but still read "pitch" in the full-part transcription, so v01b–d were made and v01b was the take that read correctly in context (v01c and v01d unused).
- **Length:** raw total 8:34.56 (over target). Step 1 only: pauses over 0.6 s trimmed to 0.6 s inside each part (23.4 s removed in total). **No `atempo`.** Peak set to −2 dB (uniform gain). Part joins 1.0 s in the listen file.
- **Listen file:** `02_Voiceover/hos_005_vo_all_parts_listen_v01.mp3`, **8:15.33**, sha256 `a19569f46d9556a21fa0e1aea4427b5841f78d2e8d2d2bc1f4ddb30f08e53b9b`. On the Mini: `/Users/benjaminoats/YouTube/hos-005-blood/02_Video-Projects/005_How-Harvey-Proved-Blood-Circulates/02_Voiceover/`.
- **First minute (from the take):** title question "So how did a band…" 0:12.0 (line 3 of the script, as early as the text allows), promise 0:15.9, stakes "Every university…" 0:27.2 (rule is by 0:25: a text matter, not VO). `vo_check` labels "Where does all that blood go?" (0:49.5) as the title question because it takes the second question line.
- **Stumbles and repeats:** no inserted words in any diff (a double or restart would show as an insert). The remaining warnings are the transcriber's spelling of Fabricius, round/around, crack-brained, and believed/believe; "believed" re-checked on a 10 s window and heard correctly.

| Part | File | Start in listen file | Duration | Pause trim | sha256 |
|---|---|---|---|---|---|
| 01 | `part01_the_used_up_blood_v01.mp3` | 0:00.00 | 0:57.02 | 3.78 s | `17ef3c420ba0239e7df30cddfa33f61fb480b72661c43ea81effadefd17f4c15` |
| 02 | `part02_the_liver_that_made_blood_v01.mp3` | 0:58.02 | 1:37.58 | 4.74 s | `c99d1e5fbd0a0ab7cbd95bce2f796d5050be507c9358483b4900b34cb60436dd` |
| 03 | `part03_the_sum_that_broke_the_old_idea_v01.mp3` | 2:36.60 | 1:36.20 | 3.39 s | `480a3d57070c24e73b60f3a1ec8974c394d75033ad69eab59fdd381e2603e743` |
| 04 | `part04_the_tied_arm_v01.mp3` | 4:13.80 | 2:06.24 | 3.84 s | `51b0ffcaeea3ac1b0269744cf77d5294e0545987b25e8378f44c1bda568a391e` |
| 05 | `part05_the_vessels_he_never_saw_v01.mp3` | 6:21.04 | 1:54.29 | 7.63 s | `e848049790b84710abe40b4a375662ec23a4ec9dfd370891c1f1fee9fcf6253b` |
| All | `hos_005_vo_all_parts_listen_v01.mp3` | — | 8:15.33 | — | `a19569f46d9556a21fa0e1aea4427b5841f78d2e8d2d2bc1f4ddb30f08e53b9b` |

Raw takes (`partNN_*_v01_raw.mp3`) sha256: 01 `66330a1e98d6e199a9d893d49d48beb108a0ba03880c3baef6b720d8bba96769` · 02 `a1afe99111361b4a89d75daa6c483379eb7819294e3087ab2ca3923329a9da5d` · 03 `0c1f5c5467a01ccc3d21dc59183c069ade6c6ec100138491617692eb86cf4e89` · 04 `4fb91ae612d7f3fa02ff6b6b4f965a9b024f22f0d9a8f2f4d24cf61c5c604281` · 05 `49445e57c79b48bcf55775be901aca509236298b160f8543640227c4a75f252d`. Fixes: `_qa_what_he_saw_v01a.mp3` `2153070b921d411a452e6ec7ec413681c878978b26c7e1f2e4e5b64719c2ab37` · `_qa_picture_yourself_v01b.mp3` `9547de40f078fef7868df6e7a77dbcd0f9ae392fc922c12bb659c262c9470241`.

`vo_check.py <take> --script 01_Script/blood_script_master_v02.md --part N` (parts) and without `--part` (listen file), run with faster-whisper 1.2.1 (`~/.venvs/hos-vo`):

```
PASS  part01_the_used_up_blood_v01.mp3  0:57.02  mean -21.4 dB  peak -2.3 dB  147 wpm
   first minute: title_question 49.5s  promise 15.94s
PASS  part02_the_liver_that_made_blood_v01.mp3  1:37.58  mean -21.1 dB  peak -2.3 dB  151 wpm
   warn  replace at ~0:42.62: script 'those holes doctors believed they had to' / heard 'those holes doctors believe they had to' — sounds alike (likely the transcriber); listen
   warn  replace at ~1:09.90: script 'old professor called fabricius fabricius had found something' / heard 'old professor called fabrizius fabrizius had found something' — sounds alike (likely the transcriber); listen
   warn  replace at ~1:22.84: script 'vein need doors fabricius thought they slowed' / heard 'vein need doors fabrizius thought they slowed' — sounds alike (likely the transcriber); listen
PASS  part03_the_sum_that_broke_the_old_idea_v01.mp3  1:36.20  mean -21.3 dB  peak -2.3 dB  161 wpm
PASS  part04_the_tied_arm_v01.mp3  2:06.24  mean -21.9 dB  peak -2.3 dB  155 wpm
   warn  replace at ~0:52.34: script 'valve the flaps fabricius found harvey presses' / heard 'valve the flaps fabriceus found harvey presses' — sounds alike (likely the transcriber); listen
   warn  replace at ~1:22.58: script 'towards the heart fabricius thought they slowed' / heard 'towards the heart fabriceus thought they slowed' — sounds alike (likely the transcriber); listen
PASS  part05_the_vessels_he_never_saw_v01.mp3  1:54.29  mean -21.6 dB  peak -2.3 dB  150 wpm
   warn  replace at ~1:16.08: script 'wraps a cuff round your arm think' / heard 'wraps a cuff around your arm think' — sounds alike (likely the transcriber); listen
PASS  hos_005_vo_all_parts_listen_v01.mp3  8:15.33  mean -21.5 dB  peak -2.3 dB  152 wpm
   first minute: title_question 49.52s  promise 15.96s
   warn  replace at ~2:05.90: script 'old professor called fabricius fabricius had found something' / heard 'old professor called fabrizius fabrizius had found something' — sounds alike (likely the transcriber); listen
   warn  replace at ~2:18.74: script 'vein need doors fabricius thought they slowed' / heard 'vein need doors fabrizius thought they slowed' — sounds alike (likely the transcriber); listen
   warn  replace at ~5:01.70: script 'valve the flaps fabricius found harvey presses' / heard 'valve the flaps fabriceus found harvey presses' — sounds alike (likely the transcriber); listen
   warn  replace at ~5:30.70: script 'towards the heart fabricius thought they slowed' / heard 'towards the heart fabriceus thought they slowed' — sounds alike (likely the transcriber); listen
   warn  replace at ~6:07.88: script 'thought he was crack brained and gap was' / heard 'thought he was crackbrained and gap was' — sounds alike (likely the transcriber); listen
   warn  replace at ~7:28.36: script 'wraps a cuff round your arm think' / heard 'wraps a cuff around your arm think' — sounds alike (likely the transcriber); listen
```

Part and chapter times in the script are estimates; re-time every part and chapter card from these starts before plate boards.

## 1 Oct 2026 — script v02 with the fixed reviewer (Grok, desk task from Claude)

Reviewer from `main` after #185 merged; script text unchanged. `npm run review:script -- --file ../02_Video-Projects/005_How-Harvey-Proved-Blood-Circulates/01_Script/blood_script_master_v02.md`:

```
**Decision:** REJECT · **Score:** 89.8 / 100
hook 7.5 · curiosity 7.5 · storytelling 8 · scientificAccuracy 10 · emotion 9.6 · escalation 10 · retentionPotential 9 · searchPotential 9.1 · visualOpportunities 9.5 · narrationFlow 9.6
Words: 1257 · Est. min: 8.4 · Chapters: 4
- [warn] hook: No question mark in the first spoken window — consider an immediate unanswered question.
- [info] overall: Structure gates 8/8 — applied +1.05 completeness boost to supporting dimensions.
- [fail] overall: Total 89.8/100 is below pass threshold 90. Rewrite before VO or picture gen.
```

The first question ("So how did a band tied round an arm prove them wrong?") lands just after the opening window. Ben signed off v02 on 1 Oct 2026, so 89.8 stands as a gate override (STUDIO_PLAYBOOK §2).

## 1 Oct 2026 — voice OK, gate, re-time, plate boards, Part 01 mint STOP, Shorts scripts (Grok, desk task from Claude, comment 5942013813)

Ben, 1 Oct, in chat with Claude: "waive vidIQ, merge #186 and voice OK".

- **vidIQ:** `PRE_BUILD_VIDIQ_AUDIT.md` signed "vidIQ waived by Ben, 1 Oct 2026"; title ticked as locked with the v02 sign-off; the script-reviewer box stays unticked at 89.8 (override).
- **Voice:** Voice v01 (listen file sha `a19569f4…`, 8:15.33) OK'd by Ben, 1 Oct 2026. Part table (duration, start, sha256) is in the VO v01 section above.
- **Branch:** merged `origin/main` (with #185's reviewer) into `grok/hos-005-blood-script`, merge commit, no rebase.

`npm run gate:episode -- --project ../02_Video-Projects/005_How-Harvey-Proved-Blood-Circulates` (after the re-time; script score is Ben's recorded override, as on 004):

```
**Decision:** BLOCK — VO / Gemini Veo blocked

| Check | Status | Detail |
|---|---|---|
| project_dir | OK | Project: /Users/benjaminoats/YouTube/hos-005-blood/02_Video-Projects/005_How-Harvey-Proved-Blood-Circulates |
| prebuild_vidiq | OK | Pre-build vidIQ audit present and looks signed off. |
| script_file | OK | Script: 01_Script/blood_script_master_v02.md |
| script_review | FAIL | Script reviewer REJECT 89.8/90 (need ≥90). |
| explorer_acts | OK | [EXPLORER ACTS] beats 3 (need ≥1). |
| visual_must | OK | [VISUAL MUST] count 45 (need ≥4). |
| teach | OK | [TEACH] count 5 (need ≥4). |
| chapters | OK | [CHAPTER CARD] count 4 (aim 4–6 film acts). |
| production_checklist | OK | Checklist present: 11_Upload-Package/PRODUCTION_CHECKLIST_V2.md |

Script score: **89.8/100** · REJECT
```

### Re-time from the real VO

`~/.venvs/hos-vo/bin/python 07_Edit-Project/_retime_vo_v01.py` (faster-whisper small.en word timestamps on the five part takes) → `07_Edit-Project/VO_RETIME_v01.json`, every sentence's start in its take and on the film timeline. Each chapter card fades in 0.6 s after the previous part's last word, holds 1.5 s, and the next part's VO starts 1.9 s after the card comes in (2.5 s per join, replacing the listen file's 1.0 s joins).

| Part | Chapter card in | VO on the film timeline | Plates |
|---|---|---|---:|
| 01 The Used-Up Blood | — (no card) | 0:00.00–0:57.02 | 12 |
| 02 The Liver That Made Blood | 0:57.62 | 0:59.52–2:37.10 | 18 |
| 03 The Sum That Broke the Old Idea | 2:37.70 | 2:39.60–4:15.80 | 19 |
| 04 The Tied Arm | 4:16.40 | 4:18.30–6:24.54 | 27 |
| 05 The Vessels He Never Saw | 6:25.14 | 6:27.04–8:21.33 | 21 |

The film's VO ends at 8:21.33; with the 3–4 s end card it runs about 8:25. First minute from the take: title question 0:12.02, promise 0:15.94, stakes 0:27.22, Harvey named about 0:41. The script's part headers, chapter-card times and all 45 `[VISUAL MUST]` cue times now follow the VO. No spoken word changed; `review:script` still reads 89.8, 1,257 words.

### Plate boards v01 (all five parts)

`python3 07_Edit-Project/_build_plate_boards_v01.py` writes `07_Edit-Project/parts/part-0N_plates_v01.json` from the re-time: one plate per VO beat with `t_s`, `use_s` (every plate 2.4–7.9 s), `vo_land`, `prompt`, `quality`, `explorer`, `side_label`, plus each part's `forbidden` and `always_fails` (gore, faces in the first two seconds and wrong sums added for 005). The template `part-01_plates_v01.json` is kept as `parts/_replaced/part-01_plates_v01_template_REPLACED.json`.

- **Part 01:** 12 plates, no Explorer, no face before plate 07 (0:27); frame 0 is the wrist and pulse, moving. 11 Quality, 1 Fast (`06_vein_press`).
- **Explorer:** Part 02 plate 13 (Padua rail and Fabricius's drawing), Part 03 plate 11 (the jugs), Part 05 plate 06 (Malpighi's microscope). Three beats, all on model.
- **Wonder, not gore:** the arm plates are arm and hand only on clean skin; animal hearts appear only as ink drawings (Part 03 plate 03); the transfusion is tools only (Part 05 plate 13).
- **Readable writing:** the sums plates (Part 01 `04_sum_page`, Part 03 `08`–`10`) ask for large *2 oz*, *1/8*, *1000*, to be checked by hand on every take. *De Motu Cordis* is a text overlay on Part 04 `23_press_1628` (plate title page left plain).
- **Labels:** white Didot italic, 1–4 words, one at a time, on the plate's first beat (added in the edit).
- **Spend for the whole film:** 84 Quality + 13 Fast plates on try 1, roughly 8,700 Flow credits before any remints.

### Part 01 mint: STOPPED before any spend

- Flow gate on the Mini (`benoats@googlemail.com`, CDP :9222): `GATE PASS account=benoats@googlemail.com credits=62`. The page shows "You're running low on Google Flow credits. Your credits will reset monthly, or top up to get more now."
- 62 credits won't buy one Quality plate (about 100). Part 01's light plates must be Quality, and the playbook says to wait for the reset rather than drop to Fast or Ken Burns. Nothing was minted.
- Start-frame stills (`07_Edit-Project/_gen_part01_stills_v01.py`, Gemini Flash Image) also failed: `HTTP 402 … Your prepayment credits are depleted`. No stills were made.
- The mint is ready to run as soon as credits exist: board `mint: true`, one plate at a time from `01_pulse_wrist` until the first KEEP.

### Shorts scripts v01

`10_Shorts/SHORTS_SCRIPTS_v01.md`: A, the sum (63 words, lead Short for Fri 30 Oct); B, the tied arm (63); C, the capillaries Harvey never saw (57). Each one has the named thing at frame 0, moving, with the claim first, the long's title at 9–14 s, and a loop back to the opening. Checked against the live Shorts page (13 public, 1 Oct 23:55) and `SHORTS_LOG.md`: no blood, heart or vein Short exists. Waiting for Ben (sign-off 3).

## 1 Oct 2026 — plate boards v02: 97 → 75 plates, Quality only on emissive light (Grok, desk task from Claude, comment 5942132122)

No minting and no spend. `python3 07_Edit-Project/_build_plate_boards_v02.py` writes `parts/part-0N_plates_v02.json`; the v01 boards are in `parts/_replaced/part-0N_plates_v01_REPLACED.json` (`mint: false`). `_gen_part01_stills_v01.py` now reads the v02 board.

```
part 01: 9 plates (3 Quality, 6 Fast, Explorer 0) try-1 420 credits → part-01_plates_v02.json
part 02: 15 plates (4 Quality, 11 Fast, Explorer 1) try-1 620 credits → part-02_plates_v02.json
part 03: 14 plates (6 Quality, 8 Fast, Explorer 1) try-1 760 credits → part-03_plates_v02.json
part 04: 19 plates (6 Quality, 13 Fast, Explorer 0) try-1 860 credits → part-04_plates_v02.json
part 05: 18 plates (7 Quality, 11 Fast, Explorer 1) try-1 920 credits → part-05_plates_v02.json
film: 75 plates (26 Quality, 49 Fast) try-1 3580 credits
```

(The builder asserts every plate is 2.4–7.9 s, i.e. one Veo clip.)

- **Merges (22):** two or three neighbouring beats become one plate when they share one location and one action, and the plate's action carries every VO line in its window (`vo_land` now lists them; `merged_from_v01` names the old plates). Examples: the promise is now one desk glide across the sums page, the linen band and Fabricius's vein drawing, in the order the VO names them; the London lane and Harvey's introduction are one plate (Harvey walks up to the lantern-lit College door); the Padua theatre rises to the Explorer on the top rail; the tied arm's push-and-stop and empty-and-refill pairs are one plate each.
- **Kept separate (mute test, §5):** every place the picture must change on a word: Vesalius, the "why believe" turn, Fabricius and his little doors, each sum number, the jugs, the scale, the loop and the one-minute lap, each step of the arm experiment, Aubrey and the open gap, Malpighi, the eyepiece, the cuff, the Delft lens.
- **Why 75 and not 65–70:** with every plate at most 7.9 s, the film's five parts need at least 8 + 13 + 13 + 17 + 15 = 66 plates even if cuts could fall anywhere. Cuts have to land on the words, so 75 is the lowest count without a plate arriving 2 s or more away from its line. Apart from Aubrey, every cut is within about 2 s of its line: the biggest moves are the whispers plate 1.9 s early and `01/08_quill_question` 1.3 s early. The Aubrey plate lands 3.9 s into his sentence (v01 was 4.2 s).
- **Engine:** Quality only where the hero is emissive or fragile light: glowing cutaways, streams and loops; the stove heart; the lantern-lit College door (01/07); the cold room whose line names the lit candles (03/01); the glowing pond life. Everything else is Fast, and every Fast prompt in a candlelit set ends "Warm candlelight falls from out of frame; no candle, flame, lantern or lamp in shot." A Fast take with a flame or lamp in frame is now in `always_fails` (reframe or remint on Quality). Reason per plate in `engine_reason`.
- **Explorer plates (02/11, 03/08, 05/05) are Fast** under that rule (no light in frame). Putting them on Quality for face and hair fidelity would add 240 credits; flagged to Claude.
- **Readable-number plates** (01/04, 03/06, 03/07) are Fast; check '2 oz', '1/8', '1000' by hand on every take.
- **Credits on try 1:** Part 01 **420** (was 1,120); whole film **3,580** (was about 8,700). Remints come on top: 004's Parts 02 and 03 each cost about 1,000 credits including remints.
- Part 01 stays `mint: true` from `01_pulse_wrist` (Quality, ≈100), so the mint starts as soon as Flow has at least 100 credits.

## 1 Oct 2026 — Explorer plates to Quality (Grok, desk task from Claude, comment 5942202586)

Claude accepted boards v02 and moved the three Explorer plates (02/11 `11_padua_explorer`, 03/08 `08_explorer_jugs`, 05/05 `05_explorer_scope`) to Quality, `engine_reason: Quality: explorer fidelity…` (face and hair are UAT hard fail 4; a Fast remint would likely cost more than the +240). Readable-number plates stay Fast with the hand check on every take. No minting and no spend; Part 01 is unchanged and still starts at `01_pulse_wrist` once Flow shows at least 100 credits. `python3 07_Edit-Project/_build_plate_boards_v02.py`:

```
part 01: 9 plates (3 Quality, 6 Fast, Explorer 0) try-1 420 credits → part-01_plates_v02.json
part 02: 15 plates (5 Quality, 10 Fast, Explorer 1) try-1 700 credits → part-02_plates_v02.json
part 03: 14 plates (7 Quality, 7 Fast, Explorer 1) try-1 840 credits → part-03_plates_v02.json
part 04: 19 plates (6 Quality, 13 Fast, Explorer 0) try-1 860 credits → part-04_plates_v02.json
part 05: 18 plates (8 Quality, 10 Fast, Explorer 1) try-1 1000 credits → part-05_plates_v02.json
film: 75 plates (29 Quality, 46 Fast) try-1 3820 credits
```

## 2 Oct 2026 — Part 01 minted on Vertex AI Veo, rough v01 (Grok, desk task from Claude, comment 5942235177)

Ben, 1 Oct, in chat with Claude: "Orbit used Vertex I believe and we have credit; if this doesn't work for us I'll top up credit Monday. Shorts A–C OK."

### Setup and credit check

- **Project** `gen-lang-client-0538779324` ("History of Science"), `us-central1`, ADC as `benoats@googlemail.com` (checked by token info; gcloud CLI itself has no login). Never an Orbit project. Vertex AI API enabled; Cloud Billing API is off in the project, so the credit was read in the console.
- **Credit before the mint** (Cloud Billing → Credits, billing account `0124D1-E6EFD6-40F6DA`, 1 Oct 23:05 UK): **Free Trial £209.53 remaining of £225.63** (93%, ends 11 Nov 2026). The Google Developer Program monthly credits are used (0%). Part 01 try 1 estimated $9.60, so clearly enough. Screenshot: `07_Edit-Project/_evidence/vertex_credits_2026-10-01.png` (local, gitignored).
- **Credit after** (2 Oct ~00:45 UK): still shows £209.53; Cloud usage posts with a delay of hours. Expected after posting ≈ £190 (the $25.58 below).
- **Models:** Quality → `veo-3.1-generate-001`, Fast → `veo-3.1-fast-generate-001`, image-to-video from the start frame, 8 s, 1080p, `generate_audio=False` (video-only SKU, $0.20/s Quality, $0.10/s Fast at list), audio stream removed again on download. No Quality plate was dropped to Fast.
- **Start frames:** Gemini API still 402. Vertex Imagen 4 is not available in the project (404); `gemini-2.5-flash-image` on Vertex in the same project works, so start frames were made there with the live look (001 ward still and the 004 live thumbnail) as style references and the previous KEEP still as a seed in the same set ($0.039 each, 21 frames). One frame (`05_chained_book_v04`) is a centre crop of v02 to keep two wall sconces out of shot.
- **Tool:** `07_Edit-Project/_mint_part01_vertex_v01.py` (`still`, `mint`, `resume`, `verdict`, `total`) on `~/.venvs/hos-vertex`. It saves the Vertex operation name at submit and writes the log under a file lock.

### What happened

- `01_pulse_wrist` was minted alone first (Quality, KEEP on take 1), then the rest in parallel.
- **Lost takes ($5.60):** the first parallel batch (02, 03, 04, 05, 07) was submitted from background jobs that died when the agent's shell call returned. The operation names weren't saved, so those five clips can't be fetched; they're logged `LOST` and counted as billed. The tool now saves the operation name at submit and has `resume`.
- **Candles on Fast plates:** the style line in the first prompts said "warm cinematic candlelight", and the board's Fast prompts end "Warm candlelight falls from out of frame…". Veo Fast painted lit candles into 6 of 6 Fast takes (always_fails). Fix for remints: style line now "warm cinematic light", and `--daylight` swaps the board's candlelight sentence for "Soft warm daylight from a window out of frame…" (recorded per take). Every Fast KEEP is a daylight take. **For Parts 02–05 boards:** the Fast candlelight sentence should change the same way.
- **Lettering:** 07's board prompt names "(the Royal College of Physicians)", and Quality wrote that on the lintel twice. The KEEP take drops the name (`--replace`, logged) and reframes to a medium shot at the door.
- **Framing changes after two FAILs:** 04 (glide → top-down), 06 (hall with desks → chart alone in an empty room), 07 (lane → medium shot at the door).

### Takes (`07_Edit-Project/PART01_MINT_LOG_v01.json`, path `vertex`, 8 s each)

| Plate | Take | Engine | Model | Status | Cost | Why |
|---|---|---|---|---|---:|---|
| `01_pulse_wrist` | t1 | Quality | `veo-3.1-generate-001` | KEEP | $1.60 | Moving wrist and glowing artery at frame 0, hands only; camera rides up to a clean cartoon heart. Watch: heartbeat-trace spike glyph on the wrist ~1–3 s; arms cross ~3 s. Cut starts 1.0 s in |
| `02_bread_liver` | t1 | Quality | `veo-3.1-generate-001` | LOST | $1.60 | Job killed, op name not saved |
| `04_sum_band_doors` | t1 | Fast | `veo-3.1-fast-generate-001` | LOST | $0.80 | Job killed, op name not saved |
| `07_harvey_college_door` | t1 | Quality | `veo-3.1-generate-001` | LOST | $1.60 | Job killed, op name not saved |
| `03_band_tightens` | t1 | Fast | `veo-3.1-fast-generate-001` | LOST | $0.80 | Job killed, op name not saved |
| `05_chained_book` | t1 | Fast | `veo-3.1-fast-generate-001` | LOST | $0.80 | Job killed, op name not saved |
| `02_bread_liver` | t2 | Quality | `veo-3.1-generate-001` | KEEP | $1.60 | Food → glowing stream → liver → red streams to the limbs, then soak away |
| `04_sum_band_doors` | t2 | Fast | `veo-3.1-fast-generate-001` | FAIL | $0.80 | Lit candle from ~3 s |
| `07_harvey_college_door` | t2 | Quality | `veo-3.1-generate-001` | FAIL | $1.60 | "Royal College of Physicians" lettering on the lintel; Harvey shrinks at the door |
| `03_band_tightens` | t2 | Fast | `veo-3.1-fast-generate-001` | FAIL | $0.80 | Lit candle from ~1 s |
| `05_chained_book` | t2 | Fast | `veo-3.1-fast-generate-001` | FAIL | $0.80 | Lit candles inside the window (~3.6 s) |
| `06_body_backwards` | t1 | Fast | `veo-3.1-fast-generate-001` | FAIL | $0.80 | Lit candles ~2.7 s; smoke puff |
| `08_quill_question` | t1 | Fast | `veo-3.1-fast-generate-001` | FAIL | $0.80 | Lit candle ~4.4 s |
| `09_heart_clock` | t1 | Fast | `veo-3.1-fast-generate-001` | FAIL | $0.80 | Lit candle ~3.5 s |
| `03_band_tightens` | t3 | Fast | `veo-3.1-fast-generate-001` | KEEP | $0.80 | Band pulled tight, veins swell blue (daylight) |
| `04_sum_band_doors` | t3 | Fast | `veo-3.1-fast-generate-001` | FAIL | $0.80 | Linen folds the vein drawing shut as "inside your veins" lands (2nd FAIL → new framing) |
| `05_chained_book` | t3 | Fast | `veo-3.1-fast-generate-001` | KEEP | $0.80 | Glide down the aisle to the chained book (daylight) |
| `06_body_backwards` | t2 | Fast | `veo-3.1-fast-generate-001` | FAIL | $0.80 | Desk candles ~2.6 s (2nd FAIL → new framing) |
| `08_quill_question` | t2 | Fast | `veo-3.1-fast-generate-001` | KEEP | $0.80 | One upright "?" written and dotted; no face (daylight) |
| `09_heart_clock` | t2 | Fast | `veo-3.1-fast-generate-001` | KEEP | $0.80 | Painted heart, brass clock, fingertip counting (daylight) |
| `07_harvey_college_door` | t3 | Quality | `veo-3.1-generate-001` | ERROR | $0.00 | Vertex "Deadline exceeded", no clip |
| `07_harvey_college_door` | t4 | Quality | `veo-3.1-generate-001` | FAIL | $1.60 | Lettering again, smoke banks, scale shift (2nd FAIL → new framing) |
| `04_sum_band_doors` | t4 | Fast | `veo-3.1-fast-generate-001` | KEEP | $0.80 | Top-down: 2 oz / 1/8 / 1000 on "a sum", band on "a band", doors open on "tiny doors" |
| `06_body_backwards` | t3 | Fast | `veo-3.1-fast-generate-001` | KEEP | $0.80 | Chart alone swings and turns right round (not upside down as boarded; flagged) |
| `07_harvey_college_door` | t5 | Quality | `veo-3.1-generate-001` | KEEP | $1.60 | Harvey on the lantern-lit step, looks back, goes in; no lettering |

**Running total: $25.58** (Veo $24.80: 7 Quality × $1.60 + 17 Fast × $0.80, of which $5.60 lost; start frames $0.78). 9/9 KEEP.

### Rough cut v01

`~/.venvs/hos-vertex/bin/python 07_Edit-Project/_assemble_part01_rough_v01.py` → **`09_Final-Export/hos_005_part01_rough_v01.mp4`**, sha256 `7661b6cf1897c6dabe60e09592b297f9ed21b253cb7c2946cc12f58732a9d098`, 59.53 s. On the Mini: `/Users/benjaminoats/YouTube/hos-005-blood/02_Video-Projects/005_How-Harvey-Proved-Blood-Circulates/09_Final-Export/hos_005_part01_rough_v01.mp4`; phone copy in iCloud `HOS UAT/005_How-Harvey-Proved-Blood-Circulates/09_Final-Export/`. Meta: `07_Edit-Project/part01_rough_v01_meta.json`.

- Picture: the 9 KEEP plates on the board v02 times, hard cuts (the board's 0.35 s crossfade would need freeze-pad on the 7.9 s plates), 1920×1080, 30 fps CFR (1,786 frames), no freeze (freezedetect 0 events). The last plate runs 2.5 s past the last VO word, then picture and music fade over the final second.
- VO: `part01_the_used_up_blood_v01.mp3` locked (sha `17ef3c42…` checked by the script), unchanged; mono to both channels at full level.
- Bed: TEMP ElevenLabs Music v2 bed `05_Music/hos005-part01-temp_score_bed_v01.mp3` (66 s, "warm curious 17th-century documentary underscore… heartbeat-like pulse"), set to VO mean −20 dB (gain −17.5 dB) for the whole runtime: music the whole way, bed alone −38.6 dB in the tail.
- Labels: white Didot italic, top right, one at a time, on the VO word: *Your pulse* · *Made, then used up* · *One band* · *A sum* · *A band* · *Tiny doors* · *London, 1616* · *William Harvey*.

`vo_check.py hos_005_part01_rough_v01.mp4 --script 01_Script/blood_script_master_v02.md --part 1` (VO intact in the mix):

```
PASS  hos_005_part01_rough_v01.mp4  0:59.53  mean -21.6 dB  peak -2.3 dB  141 wpm
   first minute: title_question 49.6s  promise 15.94s
   warn  pace 141 wpm (< 145); expect a long film — see STUDIO_PLAYBOOK.md §4 speed
```

(The pace warning counts the 2.5 s picture tail; the take itself is 147 wpm.)

### My UAT against the 11 hard fails (plate playback start/middle/end plus the cut's frames; Ben judges on the real file)

| # | Hard fail | Part 01 rough v01 |
|---|---|---|
| 1 | Consistency | One 3D cartoon style throughout; Harvey's black sleeve and white cuff match in 07, 08 and 09. Harvey reads younger than "about forty", with collar-length hair |
| 2 | Picture explains the VO | Every plate lands its line (table above). Two watch items: 06 turns round rather than upside down; 01 has a heartbeat-trace glyph on the wrist |
| 3 | Explorer glasses | No Explorer in Part 01 (board, §3) |
| 4 | Explorer face and hair | No Explorer; Harvey's face is finished in 07 |
| 5 | Lamps | No lamp in any shot. Lanterns in 07 (Quality) are calm; a small clean candle shows in the background of 01's last second (Quality) |
| 6 | Readable cards | 2 oz / 1/8 / 1000 correct; the "?" is upright; no lettering on the College door |
| 7 | Late shots sharp | Sharp to the end, no ghosting |
| 8 | Finished quality | Finished throughout |
| 9 | No DNA helix | None |
| 10 | Microbes | None in Part 01 |
| 11 | No Orbit robot | None |

005 always_fails: no gore (the heart in 01 is a clean cartoon heart under a translucent chest); no face in the first two seconds; no flame on any Fast plate inside its window.

## 2 Oct 2026 — Part 01 passed; Parts 02–05 on Vertex (Grok, desk task from Claude, comment 5942662028)

**Ben, 1 Oct, in chat with Claude: "Part 1 OK".** Part 01 rough v01 is passed as it is, including the ECG-style pulse and the quill: `09_Final-Export/hos_005_part01_rough_v01.mp4`, sha256 `7661b6cf1897c6dabe60e09592b297f9ed21b253cb7c2946cc12f58732a9d098`.

### Setup for Parts 02–05

- **Boards:** v02 with the approved Fast-plate light fix (`python3 07_Edit-Project/_board_v02_light_fix.py`): on every Fast plate the candlelight/lamplight sentence is now "Soft warm daylight from a window out of frame. There are no candles, candlesticks, lamps or lanterns anywhere in the room." Two Fast plates set at dusk/evening that the VO doesn't put at night (04/19 `19_gap_open`, 05/03 `03_old_harvey`) move to afternoon daylight. The one plate the VO puts in candlelight (03/01 `01_cold_lecture_room`, "the candles are lit") was already Quality and keeps its light. The old text stays in each plate's `prompt_v02_before_light_fix`. Changed prompts: Part 02 8, Part 03 5, Part 04 12, Part 05 4.
- **Harvey:** the same man as Part 01. Plates with Harvey on screen carry `harvey_ref: true` (02/15, 03/01, 03/05, 03/14, 04/01, 04/02, 04/17, 04/19, 05/03) and their start frames attach `04_Generated-Clips/refs/harvey_ref_v01.jpg` (a crop of Part 01's `07_harvey_college_door_v02.jpg` start frame: readable face, black gown, small pointed beard). The young Harvey on the ship (02/15) now asks for the same face, collar-length black hair, small pointed beard and a black gown.
- **Explorer:** his three plates (02/11, 03/08, 05/05) attach the Explorer sheet (`01_Character/01_Master-References/hos-explorer-character-sheet-v01.jpg`) and the generation reference.
- **Tool:** `07_Edit-Project/_mint_vertex_v02.py --part N` (Part 01's tool per part: `still`, `mint`, `auto`, `resume`, `verdict`, `total`). Same project, models, prices and op-name-at-submit logging; the full Veo prompt is now saved with each take. Logs `07_Edit-Project/PART0N_MINT_LOG_v01.json`.
- **Credit guard:** every still and take is refused if the projected Free Trial credit would fall below £60. Projected = the lower of (£209.53 before any 005 spend − all 005 logged spend × 0.80 £/$) and the latest console reading. Console readings: `07_Edit-Project/_vertex_credit_v01.py <label>` (Cloud Billing → Credits via the Mini's Chrome, screenshot in `_evidence/`, log `07_Edit-Project/VERTEX_CREDIT_LOG_v01.json`).

### Credit before Part 02

`~/.venvs/hos-vertex/bin/python 07_Edit-Project/_vertex_credit_v01.py before_part02_2026-10-02`

```
CREDIT free_trial_remaining_gbp=209.53 status=Available floor=60
```

The console hasn't posted Part 01's spend yet. `_mint_vertex_v02.py --part 2 total`:

```
part 02: takes=0 stills=0 keep=0/15 cost_usd=$0.00 (lost $0.00)
film 005 Vertex spend $25.58 · projected Free Trial £189.07 (floor £60, £/$ 0.8)
```

### Part 02: 15/15 KEEP, rough v02

- **Cut:** `09_Final-Export/hos_005_part02_rough_v02.mp4`, sha256 `d813f553b4d9d6217f00291e1ccc2715d1fb6b71ebacc05bd028b0d2ac3c0b22`, 98.233 s, freezedetect 0, bed −17.70 dB. Phone copy in iCloud `HOS UAT/005_How-Harvey-Proved-Blood-Circulates/09_Final-Export/`. Built by `07_Edit-Project/_assemble_part_rough_v02.py --part 2 --version v02`.
- **v01** (`c4ccab76…`) was replaced the same hour: in my UAT, plate 14 had glyph marks on its little doors (hard fail 6), so it was reminted to take 3 with plain cup valves.
- **Takes:** 23 takes and 30 start frames, $25.17, nothing lost. Log: `07_Edit-Project/PART02_MINT_LOG_v01.json`. Failed takes: 01 t1 (candle and lamp), 09 t1 and 10 t1 (garbled lettering), 11 t1 and t2 (scroll lettering, then a new framing), 14 t1 and t2 (glyph doors, blobs), 15 t1 (modern warship).
- **Tool changes from Part 02:**
  - Style references are Part 01's passed frames only.
  - Fast plates carry the no-flame line.
  - "No letters…" goes wherever text could appear.
  - Every start frame is checked before a take.
  - After two FAILs on one framing, the framing changes.
- **Report and my 11-hard-fail UAT:** `07_Edit-Project/_desk/part02_report_2026-10-02.md` (posted to the desk).

`vo_check.py` (hos-vo venv):

```
PASS  hos_005_part02_rough_v02.mp4  1:38.23  mean -21.1 dB  peak -2.3 dB  150 wpm
   warn  replace at ~0:42.62: 'believed' / 'believe' — sounds alike (likely the transcriber); listen
   warn  replace at ~1:09.90: 'fabricius' / 'fabrizius' — sounds alike (likely the transcriber); listen
   warn  replace at ~1:22.84: 'fabricius' / 'fabrizius' — sounds alike (likely the transcriber); listen
```

### Credit after Part 02 (= before Part 03)

```
CREDIT free_trial_remaining_gbp=208.06 status=Available floor=60
part 02: takes=23 stills=30 keep=15/15 cost_usd=$25.17 (lost $0.00)
film 005 Vertex spend $51.65 · projected Free Trial £168.21 (floor £60, £/$ 0.8)
```

## Parts

| Part | Plate board | Latest cut | Status |
|---|---|---|---|
| 01 | `07_Edit-Project/parts/part-01_plates_v02.json` (9 plates: 3 Q, 6 F) | `09_Final-Export/hos_005_part01_rough_v01.mp4` (`7661b6cf…`, 59.53 s) | 9/9 KEEP on Vertex ($25.58); **passed by Ben, 1 Oct 2026** |
| 02 | `07_Edit-Project/parts/part-02_plates_v02.json` (15: 5 Q, 10 F, ≈700) | `09_Final-Export/hos_005_part02_rough_v02.mp4` (`d813f553…`, 98.23 s) | 15/15 KEEP on Vertex ($25.17); my UAT done; Claude reviewing stills |
| 03 | `07_Edit-Project/parts/part-03_plates_v02.json` (14: 7 Q, 7 F, ≈840) | — | start frames checked; minting on Vertex |
| 04 | `07_Edit-Project/parts/part-04_plates_v02.json` (19: 6 Q, 13 F, ≈860) | — | board v02 |
| 05 | `07_Edit-Project/parts/part-05_plates_v02.json` (18: 8 Q, 10 F, ≈1000) | — | board v02 |

Keep this file current on `main`. A STOP (quota, auth, missing VO) is a line here, not an open branch.
