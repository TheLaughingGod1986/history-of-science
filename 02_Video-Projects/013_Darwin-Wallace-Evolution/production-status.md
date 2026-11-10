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
| Shorts VO | **recorded, not locked** (`J2246`, 6 Nov 2026). `hos_013_short_A_v02` 26.64 s and `hos_013_short_B_v02` 26.00 s. Both `vo_check` PASS. See `10_Shorts/vo_v02/VO_STATUS.md`. |
| Picture | **pre-VO boards only, no mint** |
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

## STOP

- No Vertex/Veo/Flow minting on this film.
- The long VO stays locked as `hos_013_vo_v03a`. Do not re-record it.
- The two Shorts takes above are waiting on review. No further ElevenLabs on them unless that review orders one pickup.
- Do not merge or close desk PR #180 from this work.
