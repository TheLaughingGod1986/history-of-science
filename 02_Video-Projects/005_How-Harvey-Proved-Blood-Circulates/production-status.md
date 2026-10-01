# Production status — 005 The Tied Arm That Proved Your Blood Circulates

| Field | Value |
|---|---|
| Slug | `005_How-Harvey-Proved-Blood-Circulates` |
| Channel | `@HistoryOfScienceYT` only |
| Topic | Ben picked: **Blood (Harvey)**, 1 Oct 2026 (chat with Claude) |
| Neighbour gate | PASS: 8 education videos with 1M+ views, TED-Ed yes (`11_Upload-Package/evidence_2026-10-01_neighbours.json`) |
| Pre-build vidIQ audit | filled from public signals; **vidIQ pending Ben**; not signed |
| Script review | **84.4 / 90, REJECT** (v02, 1 Oct 2026; v01 also 84.4) |
| Episode gate | **BLOCK** (script score; audit not signed) |
| lint:package | PASS (draft manifest; captions warning) |
| VO | pending (Ben Orbit Narrator), blocked by the gate |
| Picture | pending (Flow Veo 3.1, plate library), blocked by the gate |
| Runtime target | 7–9 min, 5 parts (v02: 1,257 spoken words, ~8:28 at 150 wpm) |
| Air | Proposed Thu 22 Oct 2026 18:00 UK, normal publish (no Premiere); pending Ben |
| Shorts | 3 planned (Fri 23, Sun 25, Tue 27 Oct, 11:30 UK), one a day at most, Related → this long |

## STOP

- **Script below 90.** v02 scores 84.4 (same as v01). Claude is asking Ben whether to fix the reviewer in its own PR or pass by hand (as for 004 at 88.9). No VO until then.
- **vidIQ audit and title** need Ben's login and OK.

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

## Parts

| Part | Plate board | Latest cut | Status |
|---|---|---|---|
| 01 | `07_Edit-Project/parts/part-01_plates_v01.json` | — | stale (built on script v01) |
| 02 | | | script v02 |
| 03 | | | script v02 |
| 04 | | | script v02 |
| 05 | | | script v02 |

Keep this file current on `main`. A STOP (quota, auth, missing VO) is a line here, not an open branch.
