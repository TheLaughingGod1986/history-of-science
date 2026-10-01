# Production status — 005 The Tied Arm That Proved Your Blood Circulates

| Field | Value |
|---|---|
| Slug | `005_How-Harvey-Proved-Blood-Circulates` |
| Channel | `@HistoryOfScienceYT` only |
| Topic | Ben picked: **Blood (Harvey)**, 1 Oct 2026 (chat with Claude) |
| Neighbour gate | PASS: 8 education videos with 1M+ views, TED-Ed yes (`11_Upload-Package/evidence_2026-10-01_neighbours.json`) |
| Pre-build vidIQ audit | filled from public signals; **vidIQ pending Ben**; not signed |
| Script sign-off | **Script v02 signed off by Ben, 1 Oct 2026** ("1–5 yes, 29 Oct", in chat with Claude; relayed on desk PR #180) |
| Script review | 89.8 with the fixed reviewer (#185). v02 signed off by Ben, 1 Oct 2026 (gate override, STUDIO_PLAYBOOK §2) |
| Episode gate | **BLOCK** on the old reviewer score and the unsigned vidIQ audit; VO went ahead on Ben's script sign-off (desk task, 1 Oct) |
| lint:package | PASS, 1 Oct 2026, schedule 29 Oct (captions warning) |
| VO | **v01 done, all `vo_check.py` PASS, 8:15.33, waiting for Ben to listen** (`02_Voiceover/hos_005_vo_all_parts_listen_v01.mp3`) |
| Picture | pending (Flow Veo 3.1, plate library). **No picture until Ben OKs the voice** |
| Runtime target | 7–9 min, 5 parts (v02: 1,250 spoken words; VO v01 8:15.33 with 1 s part joins) |
| Air | **Thu 29 Oct 2026 18:00 UK = 18:00 UTC** (`2026-10-29T18:00:00.000Z`; clocks go back 25 Oct), normal publish (no Premiere). Ben, 1 Oct. Not yet uploaded |
| Shorts | 3 planned (Fri 30 Oct, Sun 1 Nov, Tue 3 Nov, 11:30 UK = 11:30 UTC), one a day, none before the long is public, Related → this long. Scripts pending (sign-off 3) |

## STOP

- **Voice: waiting for Ben to listen** to `hos_005_vo_all_parts_listen_v01.mp3` (sign-off point 4). No picture spend until he OKs it.
- **vidIQ audit** still unsigned (gate:episode BLOCK on it).

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

## Parts

| Part | Plate board | Latest cut | Status |
|---|---|---|---|
| 01 | `07_Edit-Project/parts/part-01_plates_v01.json` | — | stale (built on script v01); VO v01 0:57.02 |
| 02 | | | script v02 |
| 03 | | | script v02 |
| 04 | | | script v02 |
| 05 | | | script v02 |

Keep this file current on `main`. A STOP (quota, auth, missing VO) is a line here, not an open branch.
