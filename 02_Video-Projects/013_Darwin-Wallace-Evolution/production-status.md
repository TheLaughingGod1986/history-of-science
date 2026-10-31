# Production status — Evolution (Darwin's 20-year secret and Wallace's letter)

| Field | Value |
|---|---|
| Slug | `013_Darwin-Wallace-Evolution` |
| Channel | `@HistoryOfScienceYT` only |
| Topic | **Evolution** — Darwin's 20-year secret (*Notebook B* 1837 → 1844 essay → Wallace's 1858 letter → *Origin* 1859 → Jenkin/Mendel/Spencer) |
| Stage | **VO v02 recorded, parked for Chief review** (`J0807`, 31 Oct 2026). Script v02 Chief PASS `J0307`. |
| Neighbour gate | **PASS** (15 Oct 2026, `J0295`): 13 education ≥1M; TED-Ed/TED yes. Evidence `00_Brand/Channel-Setup/ideas/evidence_2026-10-15_J0295/n_darwin.json` |
| Script review | `01_Script/darwin_script_master_v02.md` (**92.6/100 PASS**, 1,227 spoken words, 8/8 structure gates) |
| FACT_NOTES | `01_Script/FACT_NOTES_v02.md` (`30 OK · 0 PARTIAL · 0 FLAG`, following `J0304` Gemini quote pass + `J0307` chronology/age updates) |
| VO | **v02 recorded, not locked.** Listen file `02_Voiceover/hos_013_vo_v02.wav` (512.48 s). v01 kept. See `02_Voiceover/VO_STATUS.md`. |
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

## STOP

- No Vertex/Veo/Flow minting on this film.
- No further ElevenLabs on this film until Chief reviews `hos_013_vo_v02`.
- Do not merge or close desk PR #180 from this work.
