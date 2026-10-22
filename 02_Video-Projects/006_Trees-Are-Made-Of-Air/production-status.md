# Production status — 006 The Willow Tree That Was Made of Air

| Field | Value |
|---|---|
| Slug | `006_Trees-Are-Made-Of-Air` |
| Channel | `@HistoryOfScienceYT` only |
| Topic | **Trees are made of air** (van Helmont's willow → photosynthesis). Grok's pick from the 006 shortlist (#190); agreed by Claude on desk PR #180 comment 5949981415, 2 Oct 2026. Ben's one final OK per film comes at the end (#188) |
| Neighbour gate | PASS: 11 education videos with 1M+ views, TED-Ed yes, 7 on-topic (`11_Upload-Package/evidence_2026-10-02_neighbours.json`). Manifest block written 2 Oct, phrases `tree`, `photosynthesis` (`evidence_2026-10-02_neighbours_manifest.*`) |
| Pre-build vidIQ audit | filled from public signals; **vidIQ waived by Ben's standing rule** (relayed by Claude, 5949981415); signed |
| Script review | **93.7 / 90 PASS**, v02, 2 Oct 2026 (v01 93.8; output below) |
| Episode gate | **PASS** on v02, 2 Oct 2026 (output below) |
| lint:package | PASS on the draft package after the neighbours block edit (captions warning only), 2 Oct 2026. Title, description v01, tags v01 and schedule are proposals |
| Script sign-off | v01 approved by Claude on the desk with 3 accuracy fixes (#180 comment 5950401504); **v02** = those fixes, `01_Script/trees_script_master_v02.md` |
| VO | **v02 accepted** by Claude (#180 comment 5951184558) on the fixed `vo_check` (`358d9c7`, PR #188): **PASS** on all five parts and the listen file, 2 Oct (output below). "Genevan" confirmed in the take (whisper large-v3, 0.98) |
| Picture | **All 5 parts (92 rows) KEEP and rough cuts assembled** (Chief KEEP sweep 15 Oct 2026, `#180 IC_kwDOUEPCF88AAAABcNg8Bw`, PR `#310 → 85e16bbb`). Part 01: 12/12 KEEP + `hos_006_part01_rough_v01.mp4` (`picture_qa` PASS); Part 02: UAT applied (`#180 5981378493`) + `hos_006_part02_rough_v02.mp4`; Part 03: 18/18 KEEP/reuse (with top-cropped `P3:06`) + `hos_006_part03_rough_v02.mp4` KEEP; Part 04: 16/16 KEEP/reuse (`P4:06 t3`, `P4:08 t2`, `P4:13–16 t1` KEEP) + `hos_006_part04_rough_v01.mp4` KEEP; Part 05: 24/24 KEEP/reuse/code-graphics (`P5:02` cover, `P5:11/19` code graphics KEEP) + `hos_006_part05_rough_v01.mp4` KEEP (`picture_qa` PASS). Flow balance **23,730**; no top-up needed |
| Runtime target | 7–9 min, 5 parts. Script 1,284 spoken words ≈ 8:34 at 150 wpm (nearer 8:15 at the channel's VO pace) |
| Air | proposed **Thu 5 Nov 2026 18:00 UK = 18:00 UTC**, normal publish (no Premiere); not signed off |
| Shorts | 3 planned (lead Fri 6 Nov proposed), one a day at most, Related → this long; dates around the 005 and back-catalogue Shorts set by Claude |

## Next

- **Full join v01 (J0312, 15 Oct):** the five QA-passed roughs are joined (`hos_006_full_join_v01.mp4`, stream copy, VO already in each part). No music bed yet (none on disk; credit hold until 30 Oct, Chief's OK before a new bed). Teach overlay list for Codex: `07_Edit-Project/_desk/006/full_join_v01/TEACH_OVERLAYS_v01.md`. Parked for Chief. Not a film PASS.

## Parts

| Part | Plate board | Latest cut | Status |
|---|---|---|---|
| 01 Plants Eat Soil | `07_Edit-Project/parts/part-01_plates_v01.json` (12 rows: 3 Q, 9 F) | `hos_006_part01_rough_v01.mp4` (61.67 s, `69974f305a34…`) | script v02 · VO v02 PASS · board v01 · **plates 12/12 KEEP · rough v01 PASS** |
| 02 Five Years and Two Ounces | `part-02_plates_v01.json` (22: 4 Q, 17 F, 1 reuse) | `hos_006_part02_rough_v02.mp4` (117.00 s, `da02be4f9100…`) | script v02 · VO v02 PASS · board v01 · **UAT applied (#180 5981378493) · rough v02 KEEP** |
| 03 The Air That Mint Repaired | `part-03_plates_v01.json` (18: 4 Q, 13 F, 1 reuse) | `hos_006_part03_rough_v02.mp4` (94.83 s, `ff80e9fdf802…`) | script v02 · VO v02 PASS · board v01 · **plates 18/18 KEEP/reuse (with P3:06) · rough v02 KEEP** |
| 04 Bubbles in the Sunlight | `part-04_plates_v01.json` (16: 6 Q, 8 F, 2 reuse) | `hos_006_part04_rough_v01.mp4` (91.92 s, `fcdcce5fc5ce…`) | script v02 · VO v02 PASS · board v01 · **plates 16/16 KEEP/reuse · rough v01 KEEP** |
| 05 Carbon From the Sky | `part-05_plates_v01.json` (24: 6 Q, 12 F, 6 reuse) | `hos_006_part05_rough_v01.mp4` (142.38 s, `b3ca1afb9cd9…`) | script v02 · VO v02 PASS · board v01 · **plates 24/24 KEEP/reuse/CG · rough v01 KEEP (PASS)** |

## 2 Oct 2026 — scaffold, script v01, gates (Grok)

`python3 00_Brand/Channel-Setup/tools/neighbours.py "photosynthesis" "where do trees get their mass" "van helmont willow tree" --phrase tree --phrase photosynthesis --out …/evidence_2026-10-02_neighbours_manifest.json --manifest …/PACKAGE_MANIFEST.json`

```
| # | Channel | Views | Title | Found by |
|---|---|---|---|---|
| 1 | TED-Ed ★ | 4,797,252 views | [What if there were 1 trillion more trees? - Jean-François Bastin](https://youtu.be/3hxE7Af98AI) | ted-ed photosynthesis |
| 2 | TED-Ed ★ | 3,118,737 views | [What happens if you cut down all of a city's trees? - Stefan Al](https://youtu.be/zarll9bx6FI) | ted-ed where do trees get their mass |
| 3 | TED-Ed ★ | 2,218,164 views | [The simple story of photosynthesis and food - Amanda Ooten](https://youtu.be/eo5XndJaz-Y) | photosynthesis |
| 4 | TED-Ed ★ | 1,407,041 views | [How tall can a tree grow? - Valentin Hammoudi](https://youtu.be/vvtPJKWUb2g) | ted-ed where do trees get their mass |
| 5 | TED-Ed ★ | 856,874 views | [The secret language of trees - Camille Defrenne and Suzanne Simard](https://youtu.be/V4m9SefyRjg) | ted-ed where do trees get their mass |
| 6 | TED-Ed ★ | 619,296 views | [Does planting trees actually cool the planet? - Carolyn Beans](https://youtu.be/bbxmH_Kj7fk) | ted-ed where do trees get their mass |
| 7 | TED-Ed ★ | 526,380 views | [No one really knows what a tree is - Max G. Levy](https://youtu.be/j1EXBeBA89w) | ted-ed where do trees get their mass |
| 8 | TED-Ed ★ | 357,552 views | [Let’s plant 20 million trees together! #TeamTrees](https://youtu.be/TRIBbTo5Svc) | ted-ed where do trees get their mass |
| 9 | CrashCourse | 9,237,499 views | [Photosynthesis: Crash Course Biology #8](https://youtu.be/sQK3Yr4Sc_k) | photosynthesis |
| 10 | Kurzgesagt – In a Nutshell | 6,713,007 views | [Trees Are So Weird](https://youtu.be/ZSch_NgZpQs) | where do trees get their mass |
| 11 | Amoeba Sisters | 6,179,145 views | [Photosynthesis (UPDATED)](https://youtu.be/CMiPYHNNg28) | photosynthesis |
| 12 | Veritasium | 2,537,739 views | [Where Do Trees Get Their Mass?](https://youtu.be/2KZb2_vcNTg) | where do trees get their mass |

Words the top neighbours share: a tree
TED-Ed/TED neighbour: yes
Big neighbours (≥ 1,000,000 views): 11 (need 3)
Neighbour gate (≥ 3 education videos with 1,000,000+ views): PASS
Raw pull: 02_Video-Projects/006_Trees-Are-Made-Of-Air/11_Upload-Package/evidence_2026-10-02_neighbours_manifest.json
Wrote neighbours block to 02_Video-Projects/006_Trees-Are-Made-Of-Air/11_Upload-Package/PACKAGE_MANIFEST.json
```

`npm run review:script -- --file ../02_Video-Projects/006_Trees-Are-Made-Of-Air/01_Script/trees_script_master_v01.md`

```
# trees_script_master_v01.md

**Decision:** PASS · **Score:** 93.8 / 100

| Dimension | Score |
|---|---:|
| hook | 9.5 |
| curiosity | 9.5 |
| storytelling | 8 |
| scientificAccuracy | 10 |
| emotion | 9.6 |
| escalation | 10 |
| retentionPotential | 9 |
| searchPotential | 9.1 |
| visualOpportunities | 9.5 |
| narrationFlow | 9.6 |

Words: 1284 · Est. min: 8.6 · Chapters: 4

## Cold open excerpt

> A fully grown tree is built almost entirely out of thin air. So where does a tree's weight really come from? By the end of this film, you'll know how a willow in a pot, a sprig of mint and a sunny window cracked one of nature's oldest secrets, and why it took more than a hundred 

## Findings

- **[info] overall:** Structure gates 8/8 — applied +1.05 completeness boost to supporting dimensions.
- **[info] overall:** PASS 93.8/100 — proceed to VO after production checklist.

Pass threshold: 90
```

`npm run gate:episode -- --project ../02_Video-Projects/006_Trees-Are-Made-Of-Air`

```
# Episode gate — 006_Trees-Are-Made-Of-Air

**Decision:** PASS — VO / Gemini Veo allowed

| Check | Status | Detail |
|---|---|---|
| project_dir | OK | Project: 02_Video-Projects/006_Trees-Are-Made-Of-Air |
| prebuild_vidiq | OK | Pre-build vidIQ audit present and looks signed off. |
| script_file | OK | Script: 01_Script/trees_script_master_v01.md |
| script_review | OK | Script reviewer PASS 93.8/90 (need ≥90). |
| explorer_acts | OK | [EXPLORER ACTS] beats 3 (need ≥1). |
| visual_must | OK | [VISUAL MUST] count 49 (need ≥4). |
| teach | OK | [TEACH] count 5 (need ≥4). |
| chapters | OK | [CHAPTER CARD] count 4 (aim 4–6 film acts). |
| production_checklist | OK | Checklist present: 11_Upload-Package/PRODUCTION_CHECKLIST_V2.md |

Script score: **93.8/100** · PASS

Cold open: A fully grown tree is built almost entirely out of thin air. So where does a tree's weight really come from? By the end of this film, you'll know how a willow in a pot, a sprig of mint and a sunny win…
```

`npm run lint:package -- --film 006`

```
PASS  02_Video-Projects/006_Trees-Are-Made-Of-Air/11_Upload-Package/PACKAGE_MANIFEST.json
   warn  [captions] no captionsFile (captions from the script)
```

## 2 Oct 2026 — script v02, neighbours block, VO v02 (Grok, desk task from Claude, comment 5950401504)

### Script v02

Claude approved v01 on the desk with three accuracy fixes. v02 changes those three sentences and nothing else (v01 kept as `01_Script/trees_script_v01.md`):

| # | v01 | v02 |
|---|---|---|
| 1 | A fully grown tree is built almost entirely out of thin air. | The wood of a tree is built mostly out of thin air. |
| 2 | Out of that thin trace, a willow builds a hundred and sixty-nine pounds of tree. | Out of that thin trace, a willow builds its wood. |
| 3 | It was the gas Priestley had discovered a few years earlier, which we now call oxygen. | It was the gas Priestley had found in seventeen seventy-four, which we now call oxygen. |

The 0:00 visual and the MADE OF AIR label are unchanged.

`npm run review:script -- --file ../02_Video-Projects/006_Trees-Are-Made-Of-Air/01_Script/trees_script_master_v02.md`

```
**Decision:** PASS · **Score:** 93.7 / 100
| hook | 9.5 | curiosity | 9.5 | storytelling | 8 | scientificAccuracy | 9.9 | emotion | 9.6 |
| escalation | 10 | retentionPotential | 9 | searchPotential | 9.1 | visualOpportunities | 9.5 | narrationFlow | 9.6 |
Words: 1278 · Est. min: 8.5 · Chapters: 4
- [info] overall: Structure gates 8/8 — applied +1.05 completeness boost to supporting dimensions.
- [info] overall: PASS 93.7/100 — proceed to VO after production checklist.
Pass threshold: 90
```

`npm run gate:episode -- --project ../02_Video-Projects/006_Trees-Are-Made-Of-Air`

```
**Decision:** PASS — VO / Gemini Veo allowed
| prebuild_vidiq | OK | Pre-build vidIQ audit present and looks signed off. |
| script_file | OK | Script: 01_Script/trees_script_master_v02.md |
| script_review | OK | Script reviewer PASS 93.7/90 (need ≥90). |
| explorer_acts | OK | [EXPLORER ACTS] beats 3 (need ≥1). |
| visual_must | OK | [VISUAL MUST] count 49 (need ≥4). |
| teach | OK | [TEACH] count 5 (need ≥4). |
| chapters | OK | [CHAPTER CARD] count 4 (aim 4–6 film acts). |
| production_checklist | OK | Checklist present: 11_Upload-Package/PRODUCTION_CHECKLIST_V2.md |
Script score: **93.7/100** · PASS
```

### Neighbours block (hand-edited)

`PACKAGE_MANIFEST.json` `neighbours.videos` now holds the three exact-question lessons and the two TED-Ed lessons Claude kept. Views are from `evidence_2026-10-02_neighbours_manifest.json`: Veritasium *Where Do Trees Get Their Mass?* (2,537,739), CrashCourse *Photosynthesis: Crash Course Biology #8* (9,237,499), Kurzgesagt *Trees Are So Weird* (6,713,007), TED-Ed *The simple story of photosynthesis and food* (2,218,164) and TED-Ed *What if there were 1 trillion more trees?* (4,797,252). Removed: *The secret language of trees* (0.86M), *What happens if you cut down all of a city's trees?* and *How tall can a tree grow?* (not in Claude's keep list). Phrases unchanged (`tree`, `photosynthesis`).

`npm run lint:package -- --film 006`

```
PASS  02_Video-Projects/006_Trees-Are-Made-Of-Air/11_Upload-Package/PACKAGE_MANIFEST.json
   warn  [captions] no captionsFile (captions from the script)
```

### VO v02

- **Voice:** Ben Orbit Narrator (`kDch6ACCIpqgQ0NsU9kk`, `eleven_v3`), `settings_for_part(n)`, speed 1.04, the same as 005. Text = `trees_script_master_v02.md` word for word, using `vo_check.py`'s line filter (`02_Voiceover/partNN_*_v01.txt`). Generator `02_Voiceover/_generate_all_vo_v01.py`, finish `_finish_vo_v02.py` (the v01 finish missed one fix and is superseded), records `VO_TAKES_v01.json` and `VO_FINISH_v02.json`.
- **Raw takes:** 8:51.8 in total. Peaks −0.7 to −0.9 dB on four parts (the finish fixes this).
- **Sentences regenerated alone, same words:**
  - Part 02 "…the roots had come from water alone." The raw take said "have come" (both whisper small.en and medium.en agree), fixed with `_qa_had_come_v01b`.
  - Part 02 "Picture yourself in that garden." This was heard as "pitch yourself" in context, the same issue 005 had; fixed with `_qa_picture_yourself_v01c`.
  - Part 03 "Then he tried air that mice had made stale with their breathing." The raw take and retakes a and b read as "have made"; take d reads "had" (0.99 medium, 0.98 small).
- **Length:** step 1 only. Pauses over 0.6 s were trimmed to 0.6 s (24.4 s in total). **No `atempo`.** Peak set to −2 dB, with 1.0 s joins. **Listen file 8:29.35**, inside the 8:15–8:30 target.
- **First minute:** title question "So where does a tree's weight really come from?" at 0:04.3, promise at 0:07.4, Aristotle at about 0:24 and van Helmont named at about 0:44.
- **Doubles and stumbles:** no inserted words in any diff, so no doubles or restarts were found. Each flagged window was re-heard with whisper medium.en (below).

| Part | File | Start in listen file | Duration | Pause trim | sha256 |
|---|---|---|---|---|---|
| 01 | `part01_plants_eat_soil_v02.mp3` | 0:00.00 | 1:01.05 | 3.43 s | `f8d12e8e3fc2dae08abff1b9445681115a06fb0268142438569f8762566e47c1` |
| 02 | `part02_five_years_and_two_ounces_v02.mp3` | 1:02.05 | 1:57.00 | 4.56 s | `ddd904b749ae2c30af92b89950e377c7ebb85aec4538858ae21f4ce4928b1a11` |
| 03 | `part03_the_air_that_mint_repaired_v02.mp3` | 3:00.05 | 1:34.23 | 4.42 s | `6696a9b8bcd0295139a75d59e1d2900189a4c9ed7d4609a592d9959e4a094bd7` |
| 04 | `part04_bubbles_in_the_sunlight_v02.mp3` | 4:35.27 | 1:31.32 | 6.28 s | `64dea1c0dd63d3fdbbccedef86ee6d8bcf91911f3ca02f4e9665883f32e32ed2` |
| 05 | `part05_carbon_from_the_sky_v02.mp3` | 6:07.59 | 2:21.76 | 5.68 s | `d8f5a499b548252756d39d467134515de2b6ab66ad0e3ba84de6179bd6233eba` |
| All | `hos_006_vo_all_parts_listen_v02.mp3` | — | 8:29.35 | — | `304f83b49d0a73b66dca3493f46dccaf98dc16c4fc1b55486e2b5fe3af4bd4f9` |

Raw sha256: 01 `330c95ce…3d7e` · 02 `532c7b86…b558` · 03 `a0478376…ecf0` · 04 `ae3b37c9…eeea` · 05 `c96b74de…40a8` (full values in `VO_FINISH_v02.json`). Fixes: `_qa_had_come_v01b` `7d821b3427aefadd026fbea27555cc590844dc989e2e0f1faee95a484b41e989` · `_qa_picture_yourself_v01c` `b7c869a9ffc65afd650e34d19152521cc6b626a6766a124d73d845514cb6f2d5` · `_qa_mice_had_made_v01d` `b095aaccb75eee47a0a1bc6d86d91208c67b849e578c9239bd65fac3ae912f31`. Files are on the Mini: `/Users/benjaminoats/YouTube/hos-006-trees/02_Video-Projects/006_Trees-Are-Made-Of-Air/02_Voiceover/`.

`vo_check.py <take> --script 01_Script/trees_script_master_v02.md --part N` (and without `--part` for the listen file), faster-whisper (`~/.venvs/hos-vo`):

```
FAIL  part01_plants_eat_soil_v02.mp3  1:01.05  mean -21.3 dB  peak -2.3 dB  160 wpm
   first minute: title_question 4.28s  promise 7.36s
   FAIL  delete at ~0:17.94: script 'took more than a and years for years' / heard 'took more than years for years' — listen, then regenerate that sentence alone if real
   FAIL  replace at ~0:41.12: script 'half of the hundreds a doctor called' / heard 'half of the 1600s a doctor called' — listen, then regenerate that sentence alone if real
FAIL  part02_five_years_and_two_ounces_v02.mp3  1:57.00  mean -21.5 dB  peak -2.3 dB  158 wpm
   FAIL  delete at ~0:42.28: script 'and weighed it a and pounds about the' / heard 'and weighed it pounds about the' — listen, then regenerate that sentence alone if real
   FAIL  delete at ~0:58.18: script 'less about ounces a and pounds of new' / heard 'less about ounces pounds of new' — listen, then regenerate that sentence alone if real
FAIL  part03_the_air_that_mint_repaired_v02.mp3  1:34.23  mean -21.7 dB  peak -2.3 dB  150 wpm
   FAIL  replace at ~0:48.60: script 'so on the seventeenth of august he' / heard 'so on the 17th of august he' — listen, then regenerate that sentence alone if real
   warn  replace at ~0:21.22: script 'he wrote probably take some of their' / heard 'he wrote probably takes some of their' — sounds alike (likely the transcriber); listen
PASS  part04_bubbles_in_the_sunlight_v02.mp3  1:31.32  mean -22.9 dB  peak -2.3 dB  142 wpm
   warn  pace 142 wpm (< 145); expect a long film — see STUDIO_PLAYBOOK.md §4 speed
   warn  replace at ~0:04.04: script 'doctor called jan ingenhousz took a house' / heard 'doctor called jan ingenhaus took a house' — sounds alike (likely the transcriber); listen
PASS  part05_carbon_from_the_sky_v02.mp3  2:21.76  mean -22.1 dB  peak -2.2 dB  151 wpm
   warn  replace at ~0:12.66: script 'then in another genevan nicolas theodore de' / heard 'then in another geneva nicolas theodor de' — sounds alike (likely the transcriber); listen
   warn  replace at ~0:14.20: script 'another genevan nicolas theodore de saussure did' / heard 'another geneva nicolas theodor de saussure did' — sounds alike (likely the transcriber); listen
   warn  replace at ~1:59.06: script 'sun together they proved that a tree' / heard 'sun together they prove that a tree' — sounds alike (likely the transcriber); listen
FAIL  hos_006_vo_all_parts_listen_v02.mp3  8:29.35  mean -21.9 dB  peak -2.2 dB  151 wpm
   first minute: title_question 133.48s  promise 7.34s
   FAIL  delete at ~0:17.94: script 'took more than a and years for years' / heard 'took more than years for years' — listen, then regenerate that sentence alone if real
   FAIL  replace at ~0:41.12: script 'half of the hundreds a doctor called' / heard 'half of the 1600s a doctor called' — listen, then regenerate that sentence alone if real
   FAIL  delete at ~1:42.02: script 'and weighed it a and pounds about the' / heard 'and weighed it pounds about the' — listen, then regenerate that sentence alone if real
   FAIL  delete at ~1:58.44: script 'less about ounces a and pounds of new' / heard 'less about ounces pounds of new' — listen, then regenerate that sentence alone if real
   FAIL  replace at ~3:39.68: script 'so on the seventeenth of august he' / heard 'so on the 17th of august he' — listen, then regenerate that sentence alone if real
   warn  replace at ~4:27.00: script 'doctor called jan ingenhousz took a house' / heard 'doctor called jan ingenhaus took a house' — sounds alike (likely the transcriber); listen
   warn  replace at ~6:09.24: script 'then in another genevan nicolas theodore de' / heard 'then in another geneva nicolas theodore de' — sounds alike (likely the transcriber); listen
   warn  replace at ~7:55.60: script 'sun together they proved that a tree' / heard 'sun together they prove that a tree' — sounds alike (likely the transcriber); listen
```

**The `vo_check` FAILs that remain are a bug in the check, not in the voice.** `norm()` drops number words and digits on both sides, but:

- "a hundred and fifty / sixty-nine / sixty-four" keeps the "a … and" between them, which the transcriber's "150 / 169 / 164" doesn't have;
- "1600s" and "17th" are not `isdigit()`, and "hundreds" and "seventeenth" are not in `NUMBER_WORDS`.

Each window re-heard with whisper medium.en on the v02 takes:

```
part01_plants_eat_soil_v02.mp3 14-20s: cracked one of nature's oldest secrets and why it took more than 150 years.
part01_plants_eat_soil_v02.mp3 38-44s: wreath came from. Near Brussels, in the first half of the 1600s, a doctor
part02_five_years_and_two_ounces_v02.mp3 24-30s: that tree nothing but pure water. Picture yourself in that garden.
part02_five_years_and_two_ounces_v02.mp3 40-46s: After five years he pulled the tree out and weighed it. £169.
part02_five_years_and_two_ounces_v02.mp3 55-62s: he dried the soil again and put it back on the scales 200 pounds less about
part03_the_air_that_mint_repaired_v02.mp3 18-25s: bold guess. Plants, he wrote, probably take some of their food from the air, but a guess
part03_the_air_that_mint_repaired_v02.mp3 46-52s: that air injured so on the 17th of august he slipped a sprig of mint
part02_five_years_and_two_ounces_v02.mp3 57-66s: and put it back on the scales 200 pounds less about two ounces 164 pounds of new
```

The audio says the script's words. The check is unchanged: per AGENTS.md, a fix to `vo_check.py` goes in its own PR with Ben's OK.

### Flow credits (before boards)

The Flow page on the Mini's CDP Chrome (`benoats@googlemail.com`, ULTRA tier) reads **"62 Google Flow credits"** with the banner "You're running low on Google Flow credits. Your credits will reset monthly". So the monthly credits **have not reset** as of 2 Oct, about 12:30 UK. Vertex Free Trial remaining: still to read before boarding.

## 2 Oct 2026 — VO accepted on the fixed vo_check, boards v01 and priced plan (Grok, desk task 5951184558)

Branch `grok/hos-006-trees-script` (worktree on the Mini, `/Users/benjaminoats/YouTube/hos-006-trees`). Nothing has been minted. Film records are in `02_Video-Projects/006_Trees-Are-Made-Of-Air/production-status.md`.

### 1. VO v02: `vo_check` PASS

I ran `git checkout origin/claude/hos-repo-access-qdfmrk -- 00_Brand/Channel-Setup/tools/vo_check.py` (`358d9c7`). Then `vo_check.py <take> --script 01_Script/trees_script_master_v02.md --part N`, and the same without `--part` for the listen file (faster-whisper, `~/.venvs/hos-vo`). I didn't commit the file on the 006 branch, so it stays in #188.

```
PASS  part01_plants_eat_soil_v02.mp3  1:01.05  mean -21.3 dB  peak -2.3 dB  160 wpm
   first minute: title_question 4.28s  promise 7.36s
PASS  part02_five_years_and_two_ounces_v02.mp3  1:57.00  mean -21.5 dB  peak -2.3 dB  158 wpm
PASS  part03_the_air_that_mint_repaired_v02.mp3  1:34.23  mean -21.7 dB  peak -2.3 dB  150 wpm
   warn  replace at ~0:21.22: script 'he wrote probably take some of their' / heard 'he wrote probably takes some of their' — sounds alike (likely the transcriber); listen
PASS  part04_bubbles_in_the_sunlight_v02.mp3  1:31.32  mean -22.9 dB  peak -2.3 dB  142 wpm
   warn  pace 142 wpm (< 145); expect a long film — see STUDIO_PLAYBOOK.md §4 speed
   warn  replace at ~0:04.04: script 'doctor called jan ingenhousz took a house' / heard 'doctor called jan ingenhaus took a house' — sounds alike (likely the transcriber); listen
PASS  part05_carbon_from_the_sky_v02.mp3  2:21.76  mean -22.1 dB  peak -2.2 dB  151 wpm
   warn  replace at ~0:12.66: script 'then in another genevan nicolas theodore de' / heard 'then in another geneva nicolas theodor de' — sounds alike (likely the transcriber); listen
   warn  replace at ~0:14.20: script 'another genevan nicolas theodore de saussure did' / heard 'another geneva nicolas theodor de saussure did' — sounds alike (likely the transcriber); listen
   warn  replace at ~1:59.06: script 'sun together they proved that a tree' / heard 'sun together they prove that a tree' — sounds alike (likely the transcriber); listen
PASS  hos_006_vo_all_parts_listen_v02.mp3  8:29.35  mean -21.9 dB  peak -2.2 dB  151 wpm
   first minute: title_question 133.48s  promise 7.34s
   warn  replace at ~4:26.68: script 'doctor called jan ingenhousz took a house' / heard 'doctor called jan ingenhaus took a house' — sounds alike (likely the transcriber); listen
   warn  replace at ~6:07.76: script 'then in another genevan nicolas theodore de' / heard 'then in another geneva nicolas theodore de' — sounds alike (likely the transcriber); listen
   warn  replace at ~7:55.04: script 'sun together they proved that a tree' / heard 'sun together they prove that a tree' — sounds alike (likely the transcriber); listen
```

The listen file's `title_question 133.48s` is the whole-film search finding a later question. Part 01 puts the title question at 4.28 s.

**"Genevan" (Part 05, about 0:12).** I cut 0:09–0:18 out of the Part 05 take and re-transcribed it on its own with word timings. Both models hear the "-n":

```
large-v3  plain   … Then, in 1804, another Genevan, Nicolas Theodore de Saussure, did what   ('Genevan,' 14.02–14.68 s, p=0.98)
large-v3  prompt  … another Genevan, Nicolas Theodore de Saussure, did                      ('Genevan,' p=0.98)
medium.en plain   … another Genevan, Nicolas Théodore de Saussure, did what he called …    ('Genevan,' 14.20–14.88 s, p=0.79)
```

A short pause follows "Genevan" ("Nicolas" starts at 14.84 s), so the "-n" isn't swallowed by the next word. The small model's "Geneva" comes from the full-take context, so I didn't regenerate anything. I can't listen myself; this is the transcriber evidence. Ben's ear on that one word at about 6:09 in the listen file would settle it.

### 2. Boards v01, re-timed from VO v02

- `07_Edit-Project/_retime_vo_v02.py` writes `VO_RETIME_v02.json`, timing every sentence from the v02 takes with the same method as 005. It uses `vo_check.norm()`, so spoken numbers don't shift sentence starts.
  - **Film timeline:** VO runs 0:00–8:35.36. Chapter cards come in at 1:01.65, 3:01.15, 4:37.88 and 6:11.70; each part's VO starts 1.9 s after its card.
- `07_Edit-Project/_build_plate_boards_v01.py` writes `parts/part-0N_plates_v01.json` and `PICTURE_PLAN_v01.json`.
  - **Each plate records:** its start time, the VO lines it lands on, a side label, and Quality or Fast with the reason.
  - **Pricing per plate:** route, clip length, first-take cost, expected cost and the running total.
  - **Limits:** every plate is 2.4–7.9 s, and the Explorer appears in 3 beats (Part 02 snow garden, Part 04 shade jar, Part 05 willow). None is in the first minute, and there are no faces before Aristotle at 0:24.
- **Quality only for faces and fragile light.** That means:
  - each named person's first readable face: Aristotle, van Helmont, Hales, Priestley, Ingenhousz, Senebier and de Saussure;
  - the 3 Explorer plates;
  - flames or fire as the hero light: furnace, desk candle, charcoal fire, Priestley's candles, the oxygen blaze and the night candle;
  - glows: the air threads at 0:00, the bubbles in a sunbeam, the leaf glow, sugar and oxygen, the glowing food and the carbon atom.
  - **Made Fast instead:** the leaf cutaways, the shimmer off the cold coals and the closing "pulled down" rise. Their prompts keep every glow, flame and lamp out of frame.
- **10 free reuse rows.** Each cuts a later window of a KEEP clip as a callback, and the source is minted long enough to hold both windows:
  - Part 02's `11_furnace_again` reuses `01_furnace_soil`.
  - Part 03's "PLANTS REPAIR THE AIR" reuses `14_trees_breathe`.
  - Part 04: "the gas Priestley had found" reuses his candle burning tall from Part 03, and "back into the sun" reuses the bubbles macro.
  - Part 05 reuses the garden willow, the air threads from 0:00, the scale pointer, the watering, and the pot, jar and leaf table from Part 01.
  - The last line, "fired tiny particles at gold…", uses **004's live KEEP `11_gold_foil_bounce_v01.mp4`** (sha `5436abd1…`). It hands off to the atom film for free; if you'd rather have new picture there, that's one more Quality mint.
- **Shorter clips on Vertex.** Each plate is minted as the shortest 4, 6 or 8 s Veo clip that holds its window plus 0.5 s. That's 180 s of Quality and 370 s of Fast in total.

| Part | Rows | Quality | Fast | Reuse | On Flow | First take | Expected |
|---|---:|---:|---:|---:|---:|---:|---:|
| 01 Plants Eat Soil | 12 | 3 | 9 | 0 | 1 | £7.84 | £18.58 |
| 02 Five Years and Two Ounces | 22 | 4 | 17 | 1 | 0 | £13.76 | £31.31 |
| 03 The Air That Mint Repaired | 18 | 4 | 13 | 1 | 1 | £11.36 | £26.66 |
| 04 Bubbles in the Sunlight | 16 | 6 | 8 | 2 | 0 | £11.52 | £28.44 |
| 05 Carbon From the Sky | 24 | 6 | 12 | 6 | 1 | £13.92 | £33.38 |
| **Film** | **92** | **23** | **59** | **10** | **3** | **£58.40** | **£138.37** |

### 3. Priced plan

**Vertex balance before boarding:** Free Trial **£65.73**, Available. I read it with `_vertex_credit_v01.py before_boards_006_2026-10-02` at about 12:30 UK and logged it in `VERTEX_CREDIT_LOG_v01.json`; the screenshot is on the Mini and gitignored. The balance was £209.53 before 005 Part 02, so **005 really cost £143.80** against \$193.87 logged, about £0.742 per dollar.

**Flow, read from the picker today on the Mini's Chrome:** the account shows **62 credits**. A clip costs 5 credits on Veo 3.1 Lite, 10 on Fast and 100 on Quality; **Lite [Lower Priority] costs 0**, and **Nano Banana 2 stills cost 0**. Flow doesn't show the reset date, only "resets monthly".

- **On Flow's 62 credits:** the three held establishing shots, on Fast with 2 takes each (60 credits): `P1:09_vilvoorde`, `P3:06_leeds_brewery` and `P5:01_geneva_lake`. A third take on any of them moves to Vertex Fast. Quality isn't possible on Flow at 100 credits.
- **On Vertex:** the other 79 mints. Quality uses `veo-3.1-generate-001`, Fast uses `veo-3.1-fast-generate-001`, with start frames from `gemini-2.5-flash-image`.
- **Rates:** \$0.20 a second for Quality, \$0.10 for Fast and \$0.039 a still. I converted at the minter's conservative £0.80 per dollar; at 005's real rate everything is about 7% lower.
- **First-take cost: £58.40.** Every plate's first take fits under £65.73.
- **Retake allowance at 005's average rate:** 2.59 takes per kept Quality plate and 1.96 per kept Fast plate, plus 2.28 stills per plate. That gives **£138.37 expected, £72.64 over the £0 floor**. At 005's real exchange rate it's about £128, or £63 over.

**Plates beyond the floor,** taken in minting order (Part 01 → 05) with expected cost: 39 plates, £73.56 expected. Reuse rows and Flow plates cost nothing and aren't in this list.

- **Part 03 (8):** `10_mint_jar` F, `11_candle_tall` Q, `12_mouse_mint` F, `13_fires_breath` F, `14_trees_breathe` F, `15_quill_vegetable` F, `17_notebook_tick` F, `18_dark_window` F
- **Part 04 (14):** `01_villa` F, `02_ingenhousz_jars` Q, `03_plunge_leaf` F, `04_sunny_window` F, `05_bubbles_macro` Q, `06_collect_blaze` Q, `08_explorer_shade` Q, `10_only_green` F, `11_night_jars` Q, `12_shutters_open` F, `13_sun_canopy` F, `14_leaf_glow` Q, `15_leaf_turns_sun` F, `16_pores_question` F
- **Part 05 (17):** `02_senebier_jars` Q, `03_de_saussure` Q, `04_fine_scales` F, `05_sums_add_up` F, `06_leaf_in` F, `07_sugar_oxygen` Q, `08_sugar_wood` F, `11_trunk_pie` F, `14_built_from_sky` F, `15_food_glow` Q, `16_cow_grass` F, `17_wind_air` F, `18_forest_sea` F, `19_dots_crowd` F, `20_explorer_willow` Q, `22_pulled_down` F, `23_carbon_atom` Q

**Top-up for Ben: £73** (to cover the 005 retake rate at the conservative exchange rate).

### 4. Cheaper options that need your OK (not in the plan)

1. **Flow "Veo 3.1 Lite [Lower Priority]" at 0 credits** for the 56 Fast plates now on Vertex. This would save £62.06 expected. Lite isn't in the playbook's model table, so it needs your OK (and Ben's, if it's a rule change). I'd test one plate first and judge it on continuous playback, keeping Lite off anything with a face, a hand action or fine detail.
2. **Start frames from Flow's Nano Banana 2 at 0 credits** instead of Vertex stills. This saves £5.62.

With both, the expected cost is about **£70.69, around £5 over** (or about £65.6 at 005's real rate, right at the floor). A smaller top-up of about £10 would then cover the retake risk.

Next on your word: mint Part 01 (Vertex, from `01_willow_air`) and read the credit after each part, as with 005. I'll do any merges you want in the boards first.

Keep this file current on `main`. A STOP (quota, auth, missing VO) is a line here, not an open branch.


## 13 Oct 2026 — J0140 Senebier recovery (Codex covering)

Chief desk rulings 6140112141 / 6140142639 authorize a fresh zero-credit Nano Banana still and one Fast i2v attempt for P5:02. P5:03 uses the Chief-reassigned P5:11 clip. Runner `_probe_senebier_fast_v01.py` uses a fresh t3 filename and refuses another submitted attempt.

Initial run stopped before Create because neither uploaded style reference was attached. Flow remained 23,690 credits (0 spent). `_flow_still_v01.py` now waits for each exact completed upload tile and verifies prompt chips. No-spend live check output:

```text
attach via library 04_sunny_window_v01.jpg: True (chips=1)
attach via library 10_mint_jar_v01.jpg: True (chips=2)
No-spend style-ref attachment check: 2 chips
```

Both changed Python files compile. `status_board.py --check`: `STATUS.md and kanban/index.html match PIPELINE.json`. These are tool checks only, no creative PASS.

Resumed detached in tmux `j0140-senebier-fast-v02`, under the `flow-cdp-9222` writer lock. Log `/Users/benjaminoats/_desk/logs/j0140-senebier-fast-v02.log`; exit marker same stem `.done`. Read it before continuing; missing marker means still running. No duplicate or further paid retry. P4:08 t2 remains for Chief KEEP; missing paid P4:06 t2 remains for Chief decision. PR #310 records code and board, media stays outside git. Shared checkout changes were preserved; its pull was blocked by them.

## 14 Oct 2026 — J0140 Acting-Chief ruling executed: P4:06 t3 Fast, P5:11/19 code graphics, review/j0140 sheets, and Part 03 v02 + Part 04 v01 + Part 05 v01 roughs (Gemini covering)

Executed the 4-point Acting-Chief ruling (Claude, 14 Oct 20:50Z) on Flow (CDP 9222) and assembled all three roughs:

1. **P4:06 t2 probe & t3 Fast mint (`_probe_collect_blaze_fast_v01.py`):**
   - Fixed `harvest()` in `_mint_flow_cdp_v01.py` with top-row fallback (`y > 20`) and inspected Flow project `5c3e36ef-deef-4d70-965f-a350ca8376ab` (`f269dd3e` held `P4:10 t2`, already harvested). Confirmed `06_collect_blaze_t2` had failed server-side with no video tile in the project (Flow had refunded 50 credits: balance `23,740`).
   - Minted and harvested one authorized Fast take `06_collect_blaze_t3.mp4` (`1280x720`, 8.0 s, 24 fps, 0 freezes, sha256 `61e303bc25bd5b415a6703d3c053f390077b471485da3faaa44ac53c48668989`, 10 credits: `23,740 -> 23,730`, logged via `ai_spend.py spend --pool flow`).
2. **Part 05 0-credit house-style code graphics (`_build_part05_code_graphics_v01.py`) & P5:02 cover fallback:**
   - `11_trunk_pie_cg_v01.mp4` (6.0 s, 1920x1080 @ 24 fps, 0 freezes, sha256 `60e63c5e5e1d960fa41bc8bfba18ac58f936818666a90e0e0da244cb94b98d98`, `polish_gate` std `53.74`, edge `0.041`, seams `[]`): animated willow cross-section dividing into 50% dark walnut, 42% warm wood, 6% lighter wood, and 2% pale mineral-ash sliver on cream parchment, no letters.
   - `19_dots_crowd_cg_v01.mp4` (6.0 s, 1920x1080 @ 24 fps, 0 freezes, sha256 `1931f67210cd1436e4214aa9e0dd076b3b36621cb84b58f986fdcfbc3bd18691`, `polish_gate` std `28.64`, edge `0.1178`, seams `[]`): 10,000 jostling pale dots inside a circular walnut-and-brass specimen lens bezel, with 4 dots swelling into solid bright gold, no letters.
   - `02_senebier_jars_cover_v01.mp4` (7.46 s, 1920x1080 @ 24 fps, 0 freezes, sha256 `f667a4556aa66fd6da0c2c9798718d3540a5036b9921210366c96ff478a22731`): 0-credit cover from KEEP `P4:04_sunny_window_t1` (`1.50–5.25 s`) + KEEP `P4:05_bubbles_macro_t1` (`3.75–7.46 s`).
3. **Contact sheets pushed to `review/j0140` and `cursor/j0140-006-flow-mint`:**
   - Added all 9 pending UAT contact sheets + composite (`J0140_ALL_9_REVIEW_SHEETS.jpg`) under `02_Video-Projects/006_Trees-Are-Made-Of-Air/07_Edit-Project/_desk/006/j0140_review_sheets/`.
4. **Rough cuts assembled (`_assemble_part03_04_05_roughs_v01.py`, 0 spend, copied to iCloud `HOS UAT`):**
   - **Part 03 rough v02** (`hos_006_part03_rough_v02.mp4`, 94.833 s, VO 94.228 s, sha256 `ff80e9fdf802…`, 0 freezes): drops top-cropped `P3:06_leeds_brewery_nofire_crop_v01.mp4` (1.33x, vat fireboxes excluded per Chief #180 6131279209 / 6133444306) into Part 03. `picture_qa.py` flags only the board's locked `16_repair_reuse` window of `14_trees_breathe_t1.mp4` (same as v01).
   - **Part 04 rough v01** (`hos_006_part04_rough_v01.mp4`, 91.917 s, VO 91.320 s, sha256 `fcdcce5fc5ce…`, 0 freezes): all 16 board plates on the locked v02 VO (`02_ingenhousz_jars_t1` top-cropped 1.10x per Chief #180 6131279209; `06_collect_blaze_t3` bottom-trimmed 1.60x to exclude bottom-edge seam). `picture_qa.py` flags only the board's locked `09_bubbles_again` reuse of `05_bubbles_macro_t1` and the Chief-KEEP night candle shot `11_night_jars_t1` (`mean 19.95, p95 118.0`).
   - **Part 05 rough v01** (`hos_006_part05_rough_v01.mp4`, 142.375 s, VO 141.760 s, sha256 `b3ca1afb9cd9…`, 0 freezes): all 24 board plates on the locked v02 VO (`02` cover fallback, `03` reassigned `11_trunk_pie_t1`, `05` trimmed to 5.00–7.93 s ledger tail, `11` and `19` code graphics, `24` HOS 004 KEEP `11_gold_foil_bounce_v01.mp4`). **`picture_qa.py` verdict: PASS (0 fails).**
5. **PR #310 conflicts resolved:** merged `main`, regenerated `STATUS.md` and `00_Brand/Channel-Setup/kanban/index.html` via `status_board.py`, and verified `check_all.sh`.

## 15 Oct 2026 — J0140 Chief KEEP sweep applied, Part 01 rough v01 assembled, and Parts 01–05 picture logs consolidated on `main` (Gemini covering)

- **Chief KEEP sweep (`#180 IC_kwDOUEPCF88AAAABcNg8Bw`, 15 Oct 2026 08:47Z; `#310 → 85e16bbb`):**
  - Applied Chief's `KEEP` rulings across `PART03_MINT_LOG_v01.json`, `PART04_MINT_LOG_v01.json`, `PART04_FLOW_MINT_LOG_v01.json`, `PART05_FLOW_MINT_LOG_v01.json`, `parts/part-01..05_plates_v01.json`, and `ROUGH_META_part03_v02.json` / `ROUGH_META_part04_v01.json` / `ROUGH_META_part05_v01.json` (`P3:06 t1` top-cropped 1.33x, `P4:01–04 t1`, `P4:06 t3` Fast, `P4:08 t2` Quality, `P4:13–16 t1`, `P5:02` cover fallback, `P5:11/19` code graphics, and `Part 03 v02 / Part 04 v01 / Part 05 v01` roughs). Zero `PENDING_UAT` entries remain in any mint log (`0/6` logs have pending UAT).
- **Consolidated Part 01 and Part 02 logs onto `main` & assembled Part 01 24fps rough v01 (0 spend):**
  - Brought `PART01_MINT_LOG_v01.json`, `FLOW_FAST_v01.json`, `LITE_TEST_v01.json`, `PART02_MINT_LOG_v01.json`, `PART02_UAT_APPLIED_20261004.md`, `ROUGH_META_part02_v02.json`, and the UAT-applied `parts/part-02_plates_v01.json` from the Mini's `hos-006-trees` worktree onto `main`.
  - Assembled 24 fps 1080p `hos_006_part01_rough_v01.mp4` (`61.667 s`, VO `61.050 s`, sha256 `69974f305a34…`, 0 freezes, **`picture_qa.py` PASS**, `rc=0`) and wrote its metadata, cut/pool lists, contact sheet and `picture_qa` report to `07_Edit-Project/_desk/006/part01_rough_v01/` (copied to iCloud `HOS UAT`).
- **Next stage (`006 edit`):** `J0266` is queued for the zero-spend `picture_qa` / `polish_gate` fixes on Part 03 rough v02 (`16_repair_reuse` non-overlapping window) and Part 04 rough v01 (`09_bubbles_again` non-overlapping window + `11_night_jars` gentle shadow lift), followed by full fine cut assembly and thumbnails.

## 16 Oct 2026 — Short `s04_photosynthesis_v01` (Test B, search-titled lift from Part 05, OWB J0373)

- **Selection:** HOS 004 and 005 each have 2 search-titled Shorts (`s04` and `s05`); HOS 006 is the next locked long with 0 search-titled Shorts built so far.
- **VO (0 spend):** `02_Voiceover/part05_carbon_from_the_sky_v01_raw.mp3` claim-first lift (word indices `70..113` + `125..142`, dropping the `"We now know that"` lead-in and `"So here is what van Helmont's willow was really made of."` bridge): *"A leaf takes in carbon dioxide through tiny pores. It draws up water through its roots. Then, with the energy of sunlight, it joins them together into sugar, and lets the spare oxygen go. That sugar becomes everything else: leaves, roots, bark and wood. About half of dry wood is carbon, and every bit of that carbon came out of the air."* 62 words, pauses capped at 0.45 s, `atempo=1.02`, 24.977 s VO + 0.55 s tail = 25.533 s total.
- **Picture & bed (0 spend):** Chief-KEPT plates `P5:06_leaf_in_t1` (frame 0 and 3.2 s loop), `P2:05_pure_water_t1`, `P5:07_sugar_oxygen_t1`, `P4:05_bubbles_macro_t1`, `P5:08_sugar_wood_t1`, `P5:14_built_from_sky_t1`, `P1:01_willow_air_t1`. Own-synthesis warm harmonic pad (`hos006_s04_synth_pad_v01.wav`) at −20 dB under VO. Hook **AIR TO WOOD** (WOOD in yellow). Person/date card **DE SAUSSURE · Geneva, 1804** at 18.5–22.1 s (3.6 s, lower third of 16:9 centre band, 0.35 s fade in/out); the long's exact title *The Willow Tree That Was Made of Air* at 9.0–14.0 s; word captions throughout; CTA `watch the full film →` at 22.33–25.45 s.
- **Title draft:** *How Does Photosynthesis Work?* (signed-out GB YouTube autocomplete exact hit, 16 Oct 2026; alts *How Do Leaves Make Food for the Plant?*, *What Is Wood Made Of?*).
- **File:** `10_Shorts/hos_006_s04_photosynthesis_v01.mp4`, 25.533 s, sha256 `1198f5671f2960e2bfe49755578f90eb07c5c4ff6124a665bb0d056b1799b524` (J0399: feathered bottom of WHO card shade so alpha ramps smoothly to 0 instead of dropping 140 → 0 at `BAND_TOP + BAND_H`); phone copy iCloud `HOS UAT/006_Trees-Are-Made-Of-Air/10_Shorts/hos_006_s04_photosynthesis_v01.mp4`.

```
PASS  hos_006_s04_photosynthesis_v01.mp4  dur=25.53s  audio=-23.9dB  motion=10.73  dhash=202051d11e804ea6
   sheet /var/folders/1z/ymtxygjd7cnfrxjv7sqgmww40000gn/T/hos_shorts_gate/hos_006_s04_photosynthesis_v01_open_sheet.jpg
PASS  hos_006_s04_photosynthesis_v01.mp4  0:25.53  mean -23.9 dB  peak -4.0 dB  146 wpm
polish gate PASS: 0 of 8 rows failed, 1 to look at -> 02_Video-Projects/006_Trees-Are-Made-Of-Air/10_Shorts/qa_s04_photosynthesis_v01/polish_gate_s04_photosynthesis_v01.json
picture QA PASS: 0 of 8 cuts fail, 1 to look at -> 02_Video-Projects/006_Trees-Are-Made-Of-Air/10_Shorts/qa_s04_photosynthesis_v01/picture_qa_s04_photosynthesis_v01/PICTURE_QA.md, 02_Video-Projects/006_Trees-Are-Made-Of-Air/10_Shorts/qa_s04_photosynthesis_v01/picture_qa_s04_photosynthesis_v01/picture_qa_review.jpg
```

Gate run with `--air-date 2026-11-19` (gate only). Caption check: 18 changes, ratio 1.0. Freezedetect: 0 events.

**STOP:** parked for Chief: Short PASS, title and slot. Nothing uploaded.

## 16 Oct 2026 — Short `s05_charcoal_gas_v01` (Test B, second search-titled lift from Part 02, OWB J0390)

- **Selection:** HOS 004 and 005 each have 2 search-titled Shorts (`s04` and `s05`); HOS 006 had 1 search-titled Short (`s04_photosynthesis_v01`), so `s05_charcoal_gas_v01` completes 006's pair of Test B search-titled Shorts.
- **VO (0 spend):** `02_Voiceover/part02_five_years_and_two_ounces_v01_raw.mp3` contiguous lift (word indices `243..304`): *"Van Helmont also burned sixty-two pounds of charcoal and found just one pound of ash left behind. The rest had vanished into the air, as a wild, invisible spirit. He gave it a new name: gas. We now know that gas was mostly carbon dioxide. He had discovered the very thing his tree was made of. He never put the two together."* 62 words, pauses capped at 0.40 s, `atempo=1.03`, 25.581 s VO + 0.55 s tail = 26.133 s total.
- **Picture & bed (0 spend):** Chief-KEPT plates `P2:18_charcoal_hearth_t1` (frame 0 and 3.0 s loop), `P2:19_ash_mound_t1` (`0.15–3.45 s` < `4.0 s` trim), `P2:20_shimmer_coals_t1`, `P2:stretches_v03/15_desk_candle_t1_above_desk_v03`, `P5:06_leaf_in_t1`, `P2:06_garden_years_t2`. Own-synthesis warm harmonic pad (`hos006_s05_synth_pad_v01.wav`) at −20 dB under VO. Hook **WOOD TO GAS** (GAS in yellow). Person/date card **VAN HELMONT · Near Brussels, early 1600s** at 2.15–5.75 s (3.6 s, lower third of 16:9 centre band, 0.35 s fade in/out); the long's exact title *The Willow Tree That Was Made of Air* at 9.0–14.0 s; word captions throughout; CTA `watch the full film →` at 23.13–26.05 s.
- **Title draft:** *Who Discovered Carbon Dioxide?* (signed-out GB YouTube autocomplete exact hit, 16 Oct 2026; alts *What Happens When Wood Burns?*, *Why Does Wood Turn to Ashes?*).
- **File:** `10_Shorts/hos_006_s05_charcoal_gas_v01.mp4`, 26.133 s, sha256 `06fbeceda4944be5f75101e99166033b419ab0d7becc9d27328209f8961aa9b6`; phone copy iCloud `HOS UAT/006_Trees-Are-Made-Of-Air/10_Shorts/hos_006_s05_charcoal_gas_v01.mp4`.

```
PASS  hos_006_s05_charcoal_gas_v01.mp4  dur=26.13s  audio=-23.8dB  motion=10.72  dhash=98c06b227e7bfdf0
   sheet /var/folders/1z/ymtxygjd7cnfrxjv7sqgmww40000gn/T/hos_shorts_gate/hos_006_s05_charcoal_gas_v01_open_sheet.jpg
PASS  hos_006_s05_charcoal_gas_v01.mp4  0:26.13  mean -23.8 dB  peak -4.4 dB  145 wpm
```

Gate run with `--air-date 2026-11-26` (gate only). Caption check: 20 changes, ratio 1.0. Freezedetect: 0 events.

**STOP:** parked for Chief: Short PASS, title and slot. Nothing uploaded.

## 18 Oct 2026 — Short `s06_ingenhousz_oxygen_v01` (Test B, third search-titled lift from Part 04, OWB J0533)

- **Selection:** HOS 004 and 005 each have 3 search-titled Shorts (`s04`, `s05`, `s06`); HOS 006 had 2 search-titled Shorts (`s04_photosynthesis_v01`, `s05_charcoal_gas_v01`), making 006 the locked HOS long with the fewest built Shorts (007+ do not have minted picture yet).
- **VO (0 spend):** `02_Voiceover/part04_bubbles_in_the_sunlight_v01_raw.mp3` claim-first lift (word indices `50..81` + `105..134`, dropping the `"It was the gas Priestley had found in seventeen seventy-four, which we now call oxygen. Then came the clue that solved Priestley's puzzle."` bridge): *"Tiny silver bubbles appear on the green leaf and rise to the top. He collected the bubbles and tested the gas. A candle flame burned brighter in it than in ordinary air. Move the jar into the shade, and the bubbles stop. Move it back into the sun, and they start again. Only the green parts made bubbles. Roots and flowers didn't."* 62 words, pauses capped at 0.28 s, `atempo=1.05`, 24.756 s VO + 0.55 s tail = 25.333 s total.
- **Picture & bed (0 spend):** Chief-KEPT plates `P4:05_bubbles_macro_t1` (frame 0 and 3.0 s loop), `P4:03_plunge_leaf_t1`, `P4:06_collect_blaze_t3` (with Chief's bottom-6% seam trim `scale=2048:1152,crop=1920:1080:64:0`), `P3:11_candle_tall_t1`, `P3:18_dark_window_t1`, `P4:12_shutters_open_t1`, `P4:10_only_green_t2`. Own-synthesis warm harmonic pad (`hos006_s06_synth_pad_v01.wav`) at −20 dB under VO. Hook **LEAF IN SUN** (SUN in yellow). Person/date card **JAN INGENHOUSZ · Near London, 1779** at 4.6–8.2 s (3.6 s, lower third of 16:9 centre band, feathered shade, 0.35 s fade in/out); the long's exact title *The Willow Tree That Was Made of Air* at 9.0–14.0 s; word captions throughout; CTA `watch the full film →` at 22.33–25.25 s.
- **Title draft:** *How Do Plants Make Oxygen?* (signed-out GB YouTube autocomplete exact hit, 18 Oct 2026; alts *How Do Plants Produce Oxygen?*, *Where Does Oxygen Come From?*, *Who Discovered Photosynthesis?*).
- **File:** `10_Shorts/hos_006_s06_ingenhousz_oxygen_v01.mp4`, 25.333 s, sha256 `3daf38e7f3f5becb5e63c838fba6dfdf1d662ef3f6782cd55961d8b992cd11ae`; phone copy iCloud `HOS UAT/006_Trees-Are-Made-Of-Air/10_Shorts/hos_006_s06_ingenhousz_oxygen_v01.mp4`.

```
PASS  hos_006_s06_ingenhousz_oxygen_v01.mp4  dur=25.33s  audio=-24.8dB  motion=15.38  dhash=9296173351587f6c
   sheet /var/folders/1z/ymtxygjd7cnfrxjv7sqgmww40000gn/T/hos_shorts_gate/hos_006_s06_ingenhousz_oxygen_v01_open_sheet.jpg
PASS  hos_006_s06_ingenhousz_oxygen_v01.mp4  0:25.33  mean -24.8 dB  peak -4.9 dB  147 wpm
polish gate PASS: 0 of 8 rows failed, 0 to look at -> 02_Video-Projects/006_Trees-Are-Made-Of-Air/10_Shorts/qa_s06_ingenhousz_oxygen_v01/polish_gate_s06_ingenhousz_oxygen_v01.json
picture QA PASS: 0 of 8 cuts fail, 0 to look at -> 02_Video-Projects/006_Trees-Are-Made-Of-Air/10_Shorts/qa_s06_ingenhousz_oxygen_v01/picture_qa_s06_ingenhousz_oxygen_v01/PICTURE_QA.md
```

Gate run with `--air-date 2026-12-22` (gate only). Caption check: 19 changes, ratio 1.0. Freezedetect: 0 events.

**STOP:** parked for Chief: Short PASS, title and slot. Nothing uploaded.

## 19 Oct 2026 — Short `s07_priestley_mint_v01` (Test B, fourth search-titled lift from Part 03, OWB J0623)

- **Selection:** HOS 004 and 005 each have 4 search-titled Shorts (`s04`–`s07`); HOS 006 had 3 search-titled Shorts (`s04_photosynthesis_v01`, `s05_charcoal_gas_v01`, `s06_ingenhousz_oxygen_v01`), making 006 the locked HOS long with the fewest built Shorts (007+ do not have minted picture yet).
- **VO (0 spend):** `02_Voiceover/part03_the_air_that_mint_repaired_v01_raw.mp3` claim-first lift (word indices `85..108`, `120..146`, `187..193`, `210..213`): *"If you burn a candle inside a sealed glass jar, the flame soon dies, and the air left behind won't let another candle burn. He slipped a sprig of mint into a jar of that injured air, and waited. Ten days later, he lowered in another candle. It burned perfectly well. Something had to be putting it back. Plants repair the air."* 62 words, pauses capped at 0.30 s, `atempo=1.02`, 23.184 s VO + 0.55 s tail = 23.767 s total.
- **Picture & bed (0 spend):** Chief-KEPT plates `P3:11_candle_tall_t1` (frame 0 and 3.0 s loop), `P3:08_candles_out_t1`, `P3:07_priestley_t1`, `P3:10_mint_jar_t1`, `P4:06_collect_blaze_t3` (with Chief's bottom-6% seam trim), `P3:15_quill_vegetable_t1`, `P3:14_trees_breathe_t1`. Own-synthesis warm harmonic pad (`hos006_s07_synth_pad_v01.wav`) at −23.3 dB under VO. Hook **MINT IN GLASS** (GLASS in yellow). Person/date card **JOSEPH PRIESTLEY · Leeds, 1771** at 4.8–8.4 s (3.6 s, lower third of 16:9 centre band, cosine-feathered shade, 0.35 s fade in/out); the long's exact title *The Willow Tree That Was Made of Air* at 9.0–14.0 s; word captions throughout (17/17 changes); CTA `watch the full film →` at 20.73–23.68 s.
- **Title draft:** *How Do Plants Clean the Air?* (signed-out GB YouTube autocomplete exact hit, 19 Oct 2026; alts *Why Do We Need Plants?*, *What Was Joseph Priestley's Bell Jar Experiment?*).
- **File:** `10_Shorts/hos_006_s07_priestley_mint_v01.mp4`, 23.767 s, sha256 `253b56176b878c153a7198e650f51c848dd8bba5b4d164248cabdcef6f70ce44`; phone copy iCloud `HOS UAT/006_Trees-Are-Made-Of-Air/10_Shorts/hos_006_s07_priestley_mint_v01.mp4`.

```
PASS  hos_006_s07_priestley_mint_v01.mp4  dur=23.77s  audio=-23.8dB  motion=12.03  dhash=2f2f6e7e3d2dccfc
   sheet /var/folders/1z/ymtxygjd7cnfrxjv7sqgmww40000gn/T/hos_shorts_gate/hos_006_s07_priestley_mint_v01_open_sheet.jpg
PASS  hos_006_s07_priestley_mint_v01.mp4  0:23.77  mean -23.8 dB  peak -4.1 dB  157 wpm
polish gate PASS: 0 of 8 rows failed, 1 to look at -> 02_Video-Projects/006_Trees-Are-Made-Of-Air/10_Shorts/qa_s07_priestley_mint_v01/polish_gate_s07_priestley_mint_v01.json
picture QA PASS: 0 of 8 cuts fail, 1 to look at -> 02_Video-Projects/006_Trees-Are-Made-Of-Air/10_Shorts/qa_s07_priestley_mint_v01/picture_qa_s07_priestley_mint_v01/PICTURE_QA.md, 02_Video-Projects/006_Trees-Are-Made-Of-Air/10_Shorts/qa_s07_priestley_mint_v01/picture_qa_s07_priestley_mint_v01/picture_qa_review.jpg
```

Gate run with `--air-date 2026-12-29` (gate only). Caption check: 17 changes, ratio 1.0. Freezedetect: 0 events.

**STOP:** parked for Chief: Short PASS, title and slot. Nothing uploaded.

## 21 Oct 2026 — Short `s08_willow_pot_v01` (Test B, fifth search-titled lift from Part 02, OWB J0760)

- **Selection:** HOS 004 and 005 each have 5 search-titled Shorts (`s04`–`s08`); HOS 006 had 4 search-titled Shorts (`s04_photosynthesis_v01`, `s05_charcoal_gas_v01`, `s06_ingenhousz_oxygen_v01`, `s07_priestley_mint_v01`), making 006 the locked HOS long with the fewest built Shorts (007+ do not have minted picture yet).
- **VO (0 spend):** `02_Voiceover/part02_five_years_and_two_ounces_v01_raw.mp3` claim-first lift (word indices `6..20`, `34..43`, `106..117`, `168..194`): *"He took a big clay pot and filled it with two hundred pounds of soil, Then he planted a young willow that weighed five pounds. Then, after five years, he pulled the tree out and weighed it. A hundred and sixty-four pounds of new tree, and only two ounces of soil gone. The tree had not eaten the soil. So why had it grown?"* 64 words, pauses capped at 0.30 s, `atempo=1.02`, 23.874 s VO + 0.55 s tail = 24.433 s total. Zero VO overlap with `s05_charcoal_gas_v01` (words `243..304`).
- **Picture & bed (0 spend):** Chief-KEPT plates `P1:11_shoot_in_pot_t1` (frame 0 and 3.0 s loop), `P1:10_van_helmont_sack_t1`, `P2:03_willow_shoot_scale_t1`, `P2:04_lid_rain_t1`, `P2:08_haul_tree_t1_trim_0to4p8`, `P2:13_tree_vs_pinch_t1`, `P2:12_pointer_short_t1`, `P1:02_balance_trunk_t1`. Own-synthesis warm harmonic pad (`hos006_s08_synth_pad_v01.wav`) at −23.0 dB under VO. Hook **TREE IN POT** (POT in yellow). Person/date card **VAN HELMONT · Vilvoorde, 1600s** at 2.4–6.0 s (3.6 s, lower third of 16:9 centre band, cosine-feathered shade, 0.35 s fade in/out); the long's exact title *The Willow Tree That Was Made of Air* at 9.0–14.0 s; word captions throughout (16/16 changes); CTA `watch the full film →` at 21.43–24.35 s.
- **Title draft:** *Do Plants Eat Soil?* (signed-out GB YouTube autocomplete exact hit, 21 Oct 2026; alts *Where Do Trees Get Their Mass?*, *What Was Van Helmont's Willow Tree Experiment?*).
- **File:** `10_Shorts/hos_006_s08_willow_pot_v01.mp4`, 24.433 s, sha256 `8bce695efab2a54fa3c04a11c13c487b38c04589fc28d3a64f4f58a0f7a73441`; phone copy iCloud `HOS UAT/006_Trees-Are-Made-Of-Air/10_Shorts/hos_006_s08_willow_pot_v01.mp4`.

```
PASS  hos_006_s08_willow_pot_v01.mp4  dur=24.43s  audio=-23.5dB  motion=10.37  dhash=fdffd68d9f3fbc9f
   sheet /var/folders/1z/ymtxygjd7cnfrxjv7sqgmww40000gn/T/hos_shorts_gate/hos_006_s08_willow_pot_v01_open_sheet.jpg
PASS  hos_006_s08_willow_pot_v01.mp4  0:24.43  mean -23.5 dB  peak -4.6 dB  160 wpm
   first minute: title_question 22.6s
polish gate PASS: 0 of 9 rows failed, 1 to look at -> 02_Video-Projects/006_Trees-Are-Made-Of-Air/10_Shorts/qa_s08_willow_pot_v01/polish_gate_s08_willow_pot_v01.json
picture QA PASS: 0 of 9 cuts fail, 1 to look at -> 02_Video-Projects/006_Trees-Are-Made-Of-Air/10_Shorts/qa_s08_willow_pot_v01/picture_qa_s08_willow_pot_v01/PICTURE_QA.md, 02_Video-Projects/006_Trees-Are-Made-Of-Air/10_Shorts/qa_s08_willow_pot_v01/picture_qa_s08_willow_pot_v01/picture_qa_review.jpg
```

Gate run with `--air-date 2027-01-05` (gate only). Caption check: 16 changes, ratio 1.0. Freezedetect: 0 events.

**STOP:** parked for Chief: Short PASS, title and slot. Nothing uploaded.

## 22 Oct 2026 — Long `full_join_v02_teach` (21 £0 fixes from `REVIEW_v01.md` applied, OWB J0809)

- **Master:** `07_Edit-Project/full_join_v02_teach/hos_006_full_join_v02_teach.mp4` (`507.833 s`, `12,188` frames @ 24 fps, sha256 `09c1364b1954ba4a69a287586d036b6610e9cd7c05ab97b255f2b2ac8b3824f0`). Also copied to iCloud `HOS UAT/hos_006_full_join_v02_teach.mp4` and NAS `/Volumes/data/mac-mini-archive/YouTube/History Of Science/02_Video-Projects/006_Trees-Are-Made-Of-Air/07_Edit-Project/full_join_v02_teach/hos_006_full_join_v02_teach.mp4`.
- **Fixes applied (£0, zero mints, no music bed):**
  1. **Part 02 sync drift (`+5.46 s`):** inserted already-minted `06_garden_years_t1.mp4` (`0.00–5.46 s`, `131` frames) after `#18` (`06_garden_years_t2.mp4`), restoring `#19`–`#32` to exact alignment with `VO_RETIME_v02.json` and returning `#33` (`22_shimmer_willow`) from `10.83 s` back to `5.38 s` (`2:53.29–2:58.67`).
  2. **House-style & low-detail replacements (`#14`, `#20`, `#24`, `#33`, `#62`):** replaced flat UI card in `#14` with top-cropped `02_balance_200_t1` + house Didot lower-third counter (`0 → 200 pounds of dried soil`); cropped `#20` (`09_weights_169_t1` `1920×788`) to hide bottom-right Veo `"169"` numerals and quill; trimmed/cropped bare tabletop pan in `#24` (`13_tree_vs_pinch_t1`); removed flat UI filler card from `#33` (`22_shimmer_willow`); replaced daytime/silhouette opening of `#62` (`11_night_jars`) with moonlit jar (`4.50–8.00 s`) + moonlit plant window (`18_dark_window_t1`).
  3. **Part 05 DATA code-graphic labels (`#78`, `#86`):** re-rendered `11_trunk_pie_cg_v01.mp4` (`50% Carbon (from air)` / `44% Oxygen · 6% Hydrogen`) and `19_dots_crowd_cg_v01.mp4` (`4 in 10,000 · Carbon Dioxide`) in house Didot italic.
  4. **Overlay re-timing (`LAY_TIMES_v02.json`):** aligned all 21 teach overlays to exact frame boundaries (`REVIEW_v02.md`), sequencing `timeline_d2` before `who_hales` in `#35`, separating `ch_bubbles` and `timeline_d4` with `1.21 s` of moving `01_villa_t1` in `#52`, and moving `num_500` into `#53`.

```
polish gate PASS: 0 of 91 rows failed, 5 to look at -> /Users/benjaminoats/YouTube/History Of Science/02_Video-Projects/006_Trees-Are-Made-Of-Air/07_Edit-Project/full_join_v02_teach/polish_gate.json
picture QA PASS: 0 of 91 cuts fail, 5 to look at -> /Users/benjaminoats/YouTube/History Of Science/02_Video-Projects/006_Trees-Are-Made-Of-Air/07_Edit-Project/full_join_v02_teach/PICTURE_QA.md, /Users/benjaminoats/YouTube/History Of Science/02_Video-Projects/006_Trees-Are-Made-Of-Air/07_Edit-Project/full_join_v02_teach/picture_qa_review.jpg
Script score: 93.7/100 · PASS (Decision: PASS — VO / Gemini Veo allowed)
```

**STOP:** parked for Chief: `full_join_v02_teach` review & final OK. Nothing uploaded or scheduled.

## 22 Oct 2026 — Long `full_join_v03_teach` (3 £0 Chief FIX items from J0809 applied, OWB J0826)

- **Master:** `07_Edit-Project/full_join_v02_teach/hos_006_full_join_v03_teach.mp4` (and `hos_006_full_join_v02_teach.mp4`, `507.833 s`, `12,188` frames @ 24 fps, sha256 `9a8efcefd7a82f2c2128882e00e17ae0aa2d749891dc762a1f6addf80969f140`). Copied to iCloud `HOS UAT/hos_006_full_join_v03_teach.mp4` (and `hos_006_full_join_v02_teach.mp4`) and NAS `/Volumes/data/mac-mini-archive/YouTube/History Of Science/02_Video-Projects/006_Trees-Are-Made-Of-Air/07_Edit-Project/full_join_v02_teach/`.
- **Fixes applied (£0, zero mints, no music bed, `REVIEW_v03.md`):**
  1. **#33 (`22_shimmer_willow_v02`, `2:53.29–2:58.67`):** replaced `15_desk_candle_t1_above_desk_v03` tail repeat with unused window `2.625–8.000 s` (frames `63..192` = `129` frames) of `22_shimmer_willow_t1.mp4`, so `#33` stays 100% willow (`edge_density 0.1612`, `0` fail/warn).
  2. **#62 (`11_night_jars_v02`, `5:30.46–5:38.29`):** replaced overlapping `18_dark_window_t1` `0.67–5.00 s` with `11_night_jars_t1.mp4` `2.75–8.00 s` (`140` frames, opening moonlit after the `0.0–2.3 s` bright-sun stretch) + `18_dark_window_t1.mp4` `4.00–6.00 s` (`48` frames, the stretch `#51` `0.00–4.00 s` does not show), keeping `#62` at `188` frames (`edge_density 0.0350`, `min_mean_luma 32.9 >= 28.0`, `0` fail/warn).
  3. **#86 (`19_dots_crowd_cg_v01`, `7:50.46–7:54.46`):** shortened 5-word label `"4 in 10,000 · Carbon Dioxide"` to 4-word `"CO2: 4 in 10,000"` in house Didot italic.
  4. **`REVIEW_v02.md` §4 note:** corrected `#26` (`15_desk_candle` at `2:18`) note to record that `15_desk_candle_t1_above_desk_v03.mp4` is our own crop, not a Veo Chief-KEEP plate.

```
polish gate PASS: 0 of 91 rows failed, 5 to look at -> /Users/benjaminoats/YouTube/History Of Science/02_Video-Projects/006_Trees-Are-Made-Of-Air/07_Edit-Project/full_join_v02_teach/polish_gate.json
picture QA PASS: 0 of 91 cuts fail, 5 to look at -> /Users/benjaminoats/YouTube/History Of Science/02_Video-Projects/006_Trees-Are-Made-Of-Air/07_Edit-Project/full_join_v02_teach/PICTURE_QA.md, /Users/benjaminoats/YouTube/History Of Science/02_Video-Projects/006_Trees-Are-Made-Of-Air/07_Edit-Project/full_join_v02_teach/picture_qa_review.jpg
Script score: 93.7/100 · PASS (Decision: PASS — VO / Gemini Veo allowed)
```

**STOP:** parked for Chief: `full_join_v03_teach` (`REVIEW_v03.md`) review & merge of PR #352. Nothing uploaded or scheduled.




## 22 Oct 2026 — J0835 master v01 (£0 original score and house SFX)



- Master: `/Users/benjaminoats/YouTube/History Of Science/02_Video-Projects/006_Trees-Are-Made-Of-Air/07_Edit-Project/master_v01/hos_006_master_v01.mp4`
- NAS (copied, SHA-256 verified): `/Volumes/data/mac-mini-archive/YouTube/History Of Science/02_Video-Projects/006_Trees-Are-Made-Of-Air/09_Final-Export/master_v01/hos_006_master_v01.mp4`
- SHA-256 (both copies): `0e8f4c5990802dc15333d43b4f86c5595e84271e58acc8b11cfe72ecc98cd8cf`
- Video: 1920×1080 H264, 24 fps, 12,188 frames, 507.833333 s. Container/audio: 508.000 s (0.167 s AAC audio tail).
- Source: full_join_v03_teach, SHA-256 `d24a08ee94489379dd8e550700b9e31ec2fd4636c35158d037949248ecf8eb34`.
- Source and master compressed video SHA-256: `a67d3735f75f8763d77b063342c68e6b3946f27617555c7ec03802f051399abe` — byte-identical picture; no recut or new picture generation.
- Separate stems: `/Users/benjaminoats/YouTube/History Of Science/02_Video-Projects/006_Trees-Are-Made-Of-Air/07_Edit-Project/master_v01/stem_vo_v01.wav`; `/Users/benjaminoats/YouTube/History Of Science/02_Video-Projects/006_Trees-Are-Made-Of-Air/05_Music/trees006_score_bed_v01.mp3`; `/Users/benjaminoats/YouTube/History Of Science/02_Video-Projects/006_Trees-Are-Made-Of-Air/06_Sound-Effects/stem_sfx_v01.wav`. Mix: `/Users/benjaminoats/YouTube/History Of Science/02_Video-Projects/006_Trees-Are-Made-Of-Air/07_Edit-Project/master_v01/audio_master_v01.m4a`.
- New original HOS score: G-major/E-minor/C/D family, warm sustained viol-like harmonics, soft harp notes every 60/66 s; 3 s transitions at chapter cards (61.667 / 178.667 / 273.500 / 365.417 s). Explain chapters lift the harp; wonder chapters soften it. Full-runtime bed; no loops of an earlier film's music.
- House HOS ink ticks on teach reveals and restrained soft chapter whooshes: 21 cues. No rumbles on this quiet experiment story. Cues/levels in `sfx_cues_v01.json` and `sfx_level_v01.json`.
- Two-pass loudnorm target -14 LUFS/-1.5 dBTP (headroom below the -1 dBTP ceiling); no speech retiming or script changes.

## Machine checks (pasted outputs)

### music_gate.txt

```text
WARN pace: measured about 171.4 BPM against the brief's 60-72; Claude listens
music gate PASS: trees006_score_bed_v01.mp3, 507.8 s, about 171.4 BPM, brief Pace: 60-72 BPM
```

### picture_qa.txt

```text
WARN   2:18 row 15_desk_candle 15_desk_candle_t1_above_desk_v03.mp4: low detail: edge density 0.0271 < film p5 0.0272
WARN   3:01 row 01_soil_to_sky 01_soil_to_sky_t1.mp4: low detail: edge density 0.0219 < film p5 0.0272
WARN   5:24 row 09_bubbles_again 05_bubbles_macro_t1_from4.500.mp4: low detail: edge density 0.0245 < film p5 0.0272
WARN   6:32 row 05_sums_add_up 05_sums_add_up_t1.mp4: low detail: edge density 0.0248 < film p5 0.0272
WARN   8:17 row 23_carbon_atom 23_carbon_atom_t1.mp4: low detail: edge density 0.0238 < film p5 0.0272
picture QA PASS: 0 of 91 cuts fail, 5 to look at -> /Users/benjaminoats/YouTube/History Of Science/02_Video-Projects/006_Trees-Are-Made-Of-Air/07_Edit-Project/master_v01/PICTURE_QA.md, /Users/benjaminoats/YouTube/History Of Science/02_Video-Projects/006_Trees-Are-Made-Of-Air/07_Edit-Project/master_v01/picture_qa_review.jpg
```

### polish_gate.txt

```text
15_desk_candle   138.0s 15_desk_candle_t1_above_desk WARN low detail: edge density 0.0271 < film p5 0.0272
01_soil_to_sky   181.2s 01_soil_to_sky_t1.mp4        WARN low detail: edge density 0.0219 < film p5 0.0272
09_bubbles_again   324.2s 05_bubbles_macro_t1_from4.50 WARN low detail: edge density 0.0245 < film p5 0.0272
05_sums_add_up   392.4s 05_sums_add_up_t1.mp4        WARN low detail: edge density 0.0248 < film p5 0.0272
23_carbon_atom   497.5s 23_carbon_atom_t1.mp4        WARN low detail: edge density 0.0238 < film p5 0.0272
polish gate PASS: 0 of 91 rows failed, 5 to look at -> /Users/benjaminoats/YouTube/History Of Science/02_Video-Projects/006_Trees-Are-Made-Of-Air/07_Edit-Project/master_v01/polish_gate.json
```

### episode_gate.txt

```text
**Decision:** PASS — VO / Gemini Veo allowed
Script score: **93.7/100** · PASS
```

```text
{
  "verdict": "PASS",
  "vo_integrated": -16.1,
  "sfx_integrated": -33.3,
  "hits": 21,
  "fails": [],
  "warns": []
}
ALL CHECKS PASS (repository check_all.sh 006)
```

Final mux measurement:

```text
Summary:

  Integrated loudness:
    I:         -14.0 LUFS
    Threshold: -24.6 LUFS

  Loudness range:
    LRA:         3.0 LU
    Threshold: -34.6 LUFS
    LRA low:   -16.1 LUFS
    LRA high:  -13.1 LUFS

  True peak:
    Peak:       -1.5 dBFS
[out#0/null @ 0xbe1044300] video:5047KiB audio:95239KiB subtitle:0KiB other streams:0KiB global headers:0KiB muxing overhead: unknown
frame=12188 fps=493 q=-0.0 Lsize=N/A time=00:08:28.00 bitrate=N/A speed=20.6x elapsed=0:00:24.70
```

## Chief review still required

- Listen to the complete film for musical fit, mix comfort, repeated/stumbled VO and chapter transitions. Worker has not made an aesthetic PASS.
- Tempo WARN: gate estimates 171.4 BPM against Pace 60–72; the composer's note trigger is exactly 66 BPM with no faster arpeggio. The warning is retained for Chief to judge by ear; the checker was not changed or waived.
- Picture/polish use the unchanged `full_join_v02_teach/picture_qa_reviewed_ok_v02_teach.json` already used for v03: prior Chief reuse rulings and teach-card-edge seam rulings. No new waiver. First raw run without those rulings is preserved as `picture_qa_without_prior_rulings.txt`.
- Five existing low-detail WARNs remain at 2:18, 3:01, 5:24, 6:32 and 8:17. Review sheet remains in the local master pack (`picture_qa_review.jpg`); see v03 review for Chief's earlier inspection.
- No upload, scheduling or YouTube state change. £0 spend. Next: Chief listens/reviews, decides final PASS and Ben watch; Ben final check remains due 1 Nov.
