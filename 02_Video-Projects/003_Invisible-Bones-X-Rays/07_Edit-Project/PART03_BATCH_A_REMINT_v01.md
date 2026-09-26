# HOS 003 Part 03 — Batch A REMINT v01

**Status:** **UAT BATCH FAIL → REMINT OPEN (8 plates)**  
**Film:** *Invisible Bones / X-rays*  
**Part:** 03 — *Bones Without a Knife*  
**Dated:** 21 Sep 2026 · Europe/London (BST)  
**Board:** `parts/part-03_plates_v01.json` (helix HARD FAIL + mute-miss baked)  
**Quality:** Veo 3.1 **Quality** / CLEAN LIGHT  
**Flow:** Mini only (`benoats@googlemail.com`); no cloud Flow  
**Assembly:** **CLOSED** until remint batch lands + plate-first UAT PASS  
**P01 / P02:** **LOCK / untouched** — do not remint  
**Do not mint from this sheet alone** — CoS already launched Mini remint; Picture/CoS owns Create.

This sheet does **not** pass/fail cuts as Ben PASS.

## KEEP (do not remint)

| # | Plate ID | Note |
|---:|---|---|
| 1 | `01_chapter_bones` | KEEP — Würzburg beam→cardboard chapter read clean |
| 3 | `03_soft_fades` | KEEP — soft tissue fade + SOFT TISSUE |
| 7 | `07_explorer_hand_beam` | **SUPERSEDED 21 Sep evening** — rough_v01 full-cut HARD FAIL purple helix behind Explorer; remint 07 only — see `PART03_PLATE07_REMINT_v01.md` |

Shared top-level `forbidden` / `quality_note` now include the helix HARD FAIL so KEEP plates never regress if re-prompted.

## REMINT (8) — Create order

| # | Plate ID | Root fail | Mute / VO-literal note |
|---:|---|---|---|
| 2 | `02_hand_enters_path` | HARD Periodic-desk DNA helix bleed (yellow helix / desk prop) | Hand enters beam OK — remint for helix wipe |
| 4 | `04_bones_hold` | HARD DNA helix dominating palm | Bones hold OK — remint for helix wipe |
| 5 | `05_ring_darker` | HARD purple helix + **mute miss** | **MUTE-MISS:** denser ring must be visibly darker on hand silhouette (silent-readable) |
| 6 | `06_living_skeleton_read` | HARD DNA helix dominating desk | Living skeleton / NO KNIFE OK — remint for helix wipe |
| 8 | `08_medicine_question` | HARD DNA helix + **mute miss** | **MUTE-MISS:** empty beam + cardboard = medicine-question energy only (no people, silent-readable) |
| 9 | `09_wonder` | HARD DNA helix + **mute miss** | **MUTE-MISS:** calm glowing **bone silhouette** must dominate (wonder, not helix) |
| 10 | `10_caution_burn` | HARD blue DNA helix center | CAUTION + heat shimmer OK — remint for helix wipe |
| 11 | `11_hold_beam` | HARD DNA helix + **mute miss** | **MUTE-MISS:** clean **beam + cardboard** hold — both must read (silent-readable) |

## HARD FAIL — bake into every Create prompt

**HARD FAIL — no DNA helix, no double helix, no Periodic-table DNA desk prop on X-ray plates**  
(includes yellow/purple double-helix garnish, DNA model, orrery-helix desk bleed).

Root cause from Batch A UAT: Periodic-desk DNA helix bleed on X-ray plates. This negative is in:

- top-level JSON `forbidden` + `quality_note` + `uat_root_fail`
- every remint plate `prompt` (and KEEP prompts for regression guard)
- this remint sheet + `PRODUCTION_BRIEF_PART03_v01.md`

## Gate

- **Quality:** CLEAN LIGHT for beam / bone silhouette.
- **Assemble:** CLOSED until all remints land and plate-first UAT passes.
- **P01 + P02:** LOCK — untouched.
- One plate per FAIL cycle; if Create dies, STOP; no Ken Burns fallback.
- Scores → CoS. Do not declare Ben PASS. Do not ping Ben.

## Related

- Prior mint green (superseded for remint ops): `PART03_BATCH_A_MINT_GREEN.md`
- Brief: `PRODUCTION_BRIEF_PART03_v01.md`
- UAT score note (box): `/workspace/hos003/p03_batch_a/docs/UAT_SCORE_NOTE.md`

---

**KEEP/LOCK stamp (21 Sep evening):** `hos_003_part03_rough_v02.mp4` sha `572d498f…` — Ben KEEP. Soft notes non-blocking. No further remint this part.
