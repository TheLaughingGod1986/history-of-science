# Production status — 128 Why Do We Use AC Instead of DC? (Edison vs Tesla)

| Field | Value |
|---|---|
| Slug | `128_Edison-Tesla-Westinghouse-Why-Do-We-Use-AC-Instead-Of-DC` |
| Channel | `@HistoryOfScienceYT` only |
| Topic | **DONE — Rule-E GO (`J3346`, 22 Nov 2026 — `97.1 / 100` Opportunity Score) + Ben 24 Nov 2026 approval (`hos-search-2027-01`, OWB PR `#1238`).** Entered active production 24 Nov 2026. |
| Package-First Pick (Arm A) | *Why Do We Use AC Instead of DC? (Edison vs Tesla)* (`49 chars ≤ 50`, `0` exact collisions, scored `95/100` in [`11_Upload-Package/PACKAGE_FIRST_SCORING_v01.md`](11_Upload-Package/PACKAGE_FIRST_SCORING_v01.md)) |
| Test & Compare Arm B (Plan) | *Thomas Edison vs Nikola Tesla: How AC Won the War of Currents* (`61 chars`, `0` exact collisions, `93/100`) |
| Test & Compare Arm C | *Thomas Edison vs Nikola Tesla: Why AC Won the War of Currents* (`61 chars`, `0` exact collisions, `91/100`) |
| Thumbnails (Planned) | **Thumb A:** `1 MILE LIMIT` (1886 transformer vs overheating DC cable, `94/100`) · **Thumb B:** `22 MILES AWAY` (1896 Niagara Falls generator to Buffalo, `91/100`) · **Thumb C (3-way opt):** `HIGH VOLTAGE` (1893 Chicago White City) |
| Neighbour gate | **PASS (`2026-11-22`)** — `8` raw / `6` strictly on-topic education videos `≥1M` views in `neighbours.py` (`TED-Ed/TED: yes`; led by `Veritasium` `28.29M` & `12.84M`, `TED-Ed` ★ `3.62M` & `1.04M`, `Thoughty2` `1.97M`, `SciShow` `1.40M`). |
| Public search | Saved (`11_Upload-Package/evidence_2026-11-22_public_search.json`; `11` queries; 5 core phrases `autocomplete = yes`; `0` exact collisions). |
| Pre-build vidIQ audit | Updated in [`11_Upload-Package/PRE_BUILD_VIDIQ_AUDIT.md`](11_Upload-Package/PRE_BUILD_VIDIQ_AUDIT.md) (signed off for J3496 draft; awaits Chief lock). |
| Script draft & review | **Draft v01 (`J3496`, 24 Nov 2026):** `01_Script/edison_tesla_ac_dc_script_master_v01.md` — `review:script` **PASS** (exact pasted output below) · awaits HOS script review & Chief lock (`due 1 Dec`). |
| Facts & Sources | `01_Script/FACT_NOTES_v01.md` (`21 OK · 0 PARTIAL · 0 FLAG`) + `01_Script/SOURCES.md` — all J3346 guardrails resolved (Pearl Street 4 Sep 1882 / 110 V / 82 customers / 400 lamps / `<1 mi`; Great Barrington 20 Mar 1886 / `500 V → 3,000 V → 100 V` / `4,000 ft`; ZBD 1885 & Gaulard-Gibbs; Tesla 1 May 1888 & Ferraris March 1888 & Westinghouse July 1888; Chicago 1893 `$399k vs $554k` & stopper lamps; Niagara Falls `15–16 Nov 1896` `22 miles` to Buffalo; zero Topsy myth). |
| Episode gate | **PASS** (exact pasted output below; VO & Veo still held until Chief script lock — `£0.00` spent). |
| VO | pending (Ben Orbit Narrator — blocked until Chief script lock) |
| Picture | pending (Flow Veo 3.1, plate library — blocked until script + VO PASS) |
| Runtime target | 7–9 min, 6 parts (5 chapter cards) |
| Air | **Thu 10 Dec 2026, 18:00 London**, normal publish (no Premiere); slides to Thu 17 Dec if not ready for Ben's watch by Mon 7 Dec |
| Shorts | Draft v01 (`10_Shorts/SHORTS_SCRIPTS_v01.md`, 16–19 s Ben 19 Nov house rules): `S01` *Why Couldn't Thomas Edison's DC Power Cross a City?* (**Fri 11 Dec 11:30**) & `S02` *How Did Nikola Tesla's AC Beat Edison's DC?* (**Sat 12 Dec 11:30**) — awaiting review with long script. |

## Gate Outputs (`J3496`, `2026-11-24`)

### `npm run review:script -- --file ../02_Video-Projects/128_Edison-Tesla-Westinghouse-Why-Do-We-Use-AC-Instead-Of-DC/01_Script/edison_tesla_ac_dc_script_master_v01.md`

```text
# edison_tesla_ac_dc_script_master_v01.md

**Decision:** PASS · **Score:** 92 / 100

| Dimension | Score |
|---|---:|
| hook | 9.5 |
| curiosity | 7.5 |
| storytelling | 9.5 |
| scientificAccuracy | 9.9 |
| emotion | 9.6 |
| escalation | 8.8 |
| retentionPotential | 9 |
| searchPotential | 9.1 |
| visualOpportunities | 9.5 |
| narrationFlow | 9.6 |

Words: 1292 · Est. min: 8.6 · Chapters: 5

## Findings
- **[info] overall:** Structure gates 8/8 — applied +1.05 completeness boost to supporting dimensions.
- **[info] overall:** PASS 92/100 — proceed to VO after production checklist.
Pass threshold: 90
```

### `npm run gate:episode -- --project ../02_Video-Projects/128_Edison-Tesla-Westinghouse-Why-Do-We-Use-AC-Instead-Of-DC`

```text
# Episode gate — 128_Edison-Tesla-Westinghouse-Why-Do-We-Use-AC-Instead-Of-DC

**Decision:** PASS — VO / Gemini Veo allowed

| Check | Status | Detail |
|---|---|---|
| project_dir | OK | Project: .../02_Video-Projects/128_Edison-Tesla-Westinghouse-Why-Do-We-Use-AC-Instead-Of-DC |
| prebuild_vidiq | OK | Pre-build vidIQ audit present and looks signed off. |
| script_file | OK | Script: 01_Script/edison_tesla_ac_dc_script_master_v01.md |
| script_review | OK | Script reviewer PASS 92/90 (need ≥90). |
| explorer_acts | OK | [EXPLORER ACTS] beats 2 (need ≥1). |
| visual_must | OK | [VISUAL MUST] count 20 (need ≥4). |
| teach | OK | [TEACH] count 6 (need ≥4). |
| chapters | OK | [CHAPTER CARD] count 5 (aim 4–6 film acts). |
| production_checklist | OK | Checklist present: 11_Upload-Package/PRODUCTION_CHECKLIST_V2.md |

Script score: **92/100** · PASS
```

### `00_Brand/Channel-Setup/tools/check_all.sh 02_Video-Projects/128_Edison-Tesla-Westinghouse-Why-Do-We-Use-AC-Instead-Of-DC`

```text
-- durable desk handoffs: PASS
-- email ratchet: PASS
-- no media: PASS
-- status board in sync: PASS
-- ElevenLabs guard tests: PASS
-- vo_check word tests: PASS
-- atempo check tests: PASS
-- voice speed (atempo <= 1.06): PASS
-- contract tests: PASS
-- package-lint: PASS
-- review:script edison_tesla_ac_dc_script_master_v01.md: PASS
-- gate:episode: PASS

ALL CHECKS PASS
```

## Parts

| Part | Title | Plate board | Latest cut | Status |
|---|---|---|---|---|
| 01 | The One-Mile Trap (no chapter card) | `07_Edit-Project/parts/part-01_plates_v01.json` (scaffold) | — | Script v01 in review |
| 02 | The Trick That Shrank the Wire | pending VO lock | — | Script v01 in review |
| 03 | The Motor Without Sparks | pending VO lock | — | Script v01 in review |
| 04 | The War of the Currents | pending VO lock | — | Script v01 in review |
| 05 | The White City and Niagara | pending VO lock | — | Script v01 in review |
| 06 | Why Both Currents Won | pending VO lock | — | Script v01 in review |

Keep this file current on `main`. A STOP (quota, auth, missing VO) is a line here, not an open branch.
