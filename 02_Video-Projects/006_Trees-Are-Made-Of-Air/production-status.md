# Production status — 006 The Willow Tree That Was Made of Air

| Field | Value |
|---|---|
| Slug | `006_Trees-Are-Made-Of-Air` |
| Channel | `@HistoryOfScienceYT` only |
| Topic | **Trees are made of air** (van Helmont's willow → photosynthesis). Grok's pick from the 006 shortlist (#190); agreed by Claude on desk PR #180 comment 5949981415, 2 Oct 2026. Ben's one final OK per film comes at the end (#188) |
| Neighbour gate | PASS: 11 education videos with 1M+ views, TED-Ed yes, 7 on-topic (`11_Upload-Package/evidence_2026-10-02_neighbours.json`). Manifest block written 2 Oct, phrases `tree`, `photosynthesis` (`evidence_2026-10-02_neighbours_manifest.*`) |
| Pre-build vidIQ audit | filled from public signals; **vidIQ waived by Ben's standing rule** (relayed by Claude, 5949981415); signed |
| Script review | **93.8 / 90 PASS**, v01, 2 Oct 2026 (output below) |
| Episode gate | **PASS**, 2 Oct 2026 (output below) |
| lint:package | PASS on the draft package (captions warning only), 2 Oct 2026. Title, description v01, tags v01 and schedule are proposals |
| Script sign-off | Claude reviews v01 on the desk (Ben doesn't see the script) |
| VO | pending (Ben Orbit Narrator), after Claude accepts the script |
| Picture | pending (Veo 3.1 plate library; Quality for every candle, sunbeam and bubble) |
| Runtime target | 7–9 min, 5 parts. Script 1,284 spoken words ≈ 8:34 at 150 wpm (nearer 8:15 at the channel's VO pace) |
| Air | proposed **Thu 5 Nov 2026 18:00 UK = 18:00 UTC**, normal publish (no Premiere); not signed off |
| Shorts | 3 planned (lead Fri 6 Nov proposed), one a day at most, Related → this long; dates around the 005 and back-catalogue Shorts set by Claude |

## STOP

- **Script v01 waits for Claude's review on the desk.** No VO, boards or picture until he accepts it. Credit can run to £0, never onto paid billing.

## Parts

| Part | Plate board | Latest cut | Status |
|---|---|---|---|
| 01 Plants Eat Soil | `07_Edit-Project/parts/part-01_plates_v01.json` (template) | — | script v01 |
| 02 Five Years and Two Ounces | | | script v01 |
| 03 The Air That Mint Repaired | | | script v01 |
| 04 Bubbles in the Sunlight | | | script v01 |
| 05 Carbon From the Sky | | | script v01 |

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

Keep this file current on `main`. A STOP (quota, auth, missing VO) is a line here, not an open branch.
