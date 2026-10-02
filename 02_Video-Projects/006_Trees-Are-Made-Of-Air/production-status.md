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
| VO | **v02 finish for Claude's review** (listen file `02_Voiceover/hos_006_vo_all_parts_listen_v02.mp3`, 8:29.35, sha `304f83b4…`). Loudness, peak and pauses PASS on every part; `vo_check` word diff FAILs only on spelled-out numbers (check bug, see 2 Oct VO section) |
| Picture | pending. Flow shows **62 credits** (not reset) on 2 Oct; boards after Claude's VO review, Flow first, Vertex top-up only, stop at £0 |
| Runtime target | 7–9 min, 5 parts. Script 1,284 spoken words ≈ 8:34 at 150 wpm (nearer 8:15 at the channel's VO pace) |
| Air | proposed **Thu 5 Nov 2026 18:00 UK = 18:00 UTC**, normal publish (no Premiere); not signed off |
| Shorts | 3 planned (lead Fri 6 Nov proposed), one a day at most, Related → this long; dates around the 005 and back-catalogue Shorts set by Claude |

## STOP

- **VO v02 waits for Claude's review on the desk** (in Ben's place). No boards or picture spend until he accepts it. Credit can run to £0, never onto paid billing.

## Parts

| Part | Plate board | Latest cut | Status |
|---|---|---|---|
| 01 Plants Eat Soil | `07_Edit-Project/parts/part-01_plates_v01.json` (template) | — | script v02 · VO v02 |
| 02 Five Years and Two Ounces | | | script v02 · VO v02 |
| 03 The Air That Mint Repaired | | | script v02 · VO v02 |
| 04 Bubbles in the Sunlight | | | script v02 · VO v02 |
| 05 Carbon From the Sky | | | script v02 · VO v02 |

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

Keep this file current on `main`. A STOP (quota, auth, missing VO) is a line here, not an open branch.
