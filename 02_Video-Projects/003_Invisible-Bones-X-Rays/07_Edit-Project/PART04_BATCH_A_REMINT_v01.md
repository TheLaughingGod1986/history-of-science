# HOS 003 Part 04 — Batch A REMINT v01

**Status:** **UAT BATCH FAIL → REMINT OPEN (8 plates)**  
**Film:** *Invisible Bones / X-rays*  
**Part:** 04 — *Bertha’s Ring*  
**Dated:** 22 Sep 2026 · Europe/London (BST)  
**Board:** `parts/part-04_plates_v01.json` (helix + mute/label HARD FAIL baked)  
**Quality:** Veo 3.1 **Quality** / CLEAN LIGHT  
**Flow:** CoS Flow (`benoats@googlemail.com` ULTRA /u/1/) — remint already in flight  
**Assembly:** **CLOSED** until remint batch lands + plate-first UAT PASS  
**P01 / P02 / P03:** **LOCK / untouched** — do not remint  
**Do not mint from this sheet alone** — CoS owns Create remint.

This sheet does **not** pass/fail cuts as Ben PASS.

## KEEP (do not remint)

| # | Plate ID | Note |
|---:|---|---|
| 1 | `01_chapter_bertha` | KEEP — chapter open / empty proof plate reads clean |
| 5 | `05_letters_fly` | KEEP — letters travel from lab |
| 6 | `06_labs_copy_tube` | KEEP — labs copy cathode-tube shape |

Shared top-level `forbidden` / `quality_note` / `uat_root_fail` now include helix + mute/label HARD FAILs so KEEP plates never regress if re-prompted.

## REMINT (8) — Create order

| # | Plate ID | Root fail | Mute / VO-literal note |
|---:|---|---|---|
| 2 | `02_hand_on_plate` | Mute miss + helix risk | **MUTE:** hand rests for exposure **ON the proof plate** — not a glowing disk, not helix-in-palm |
| 3 | `03_bones_and_ring` | Helix/spiral risk on proof palm | Bones + ring both clear; ring denser; **no glowing yellow helix in palm** |
| 4 | `04_haunted_becomes_fact` | Explorer / face-hero + PROOF miss | **No Explorer / no face-hero scientist**; **PROOF** label present when VO needs it; plate held = fact |
| 7 | `07_doctors_lean_in` | Helix + mute/label risk | Faceless doctors lean to plate; MEDICINE sparse; no Explorer |
| 8 | `08_bullet_break_map` | Helix/spiral risk | Bullet/break map educational; no blood; no DNA prop |
| 9 | `09_body_as_map` | Helix/spiral risk | Body as map while whole; no helix-as-map; no cut-open horror |
| 10 | `10_why_groundbreaking` | Wall-of-text / garbled floats | **One** sparse `A NEW EYE` only — **no wall-of-text / garbled float labels** |
| 11 | `11_proof_hold` | Helix-in-palm risk | Bones+ring hold; continuous settle; no yellow helix in palm |

## HARD FAIL — bake into every Create prompt

1. **HARD FAIL — any DNA helix / spiral / prop** (includes double helix, Periodic DNA desk, yellow/purple garnish, **glowing yellow helix in X-ray palm**, DNA model, orrery-helix bleed).
2. **Never open Create with** `Same DNA soft background`. Prefer `Same Würzburg lab`.
3. **Plate 02:** mute = hand rest-for-exposure **on proof plate** (not glowing disk).
4. **Plate 04:** no Explorer / no face-hero scientist; **PROOF** label present when VO needs it.
5. **Plate 10:** no wall-of-text / garbled float labels — one sparse `A NEW EYE` only.

Root cause from Batch A UAT (22 Sep 2026). Negatives live in:

- top-level JSON `forbidden` + `quality_note` + `uat_root_fail`
- every remint plate `prompt` (and KEEP prompts for regression guard)
- this remint sheet + `PRODUCTION_BRIEF_PART04_v01.md`
- house bible `HOS_HOUSE_NO_DNA_HELIX_LOCK.md` (palm spiral note reinforced)

## Gate

- **Quality:** CLEAN LIGHT for proof / bone+ring / beam.
- **Assemble:** CLOSED until all 8 remints land and plate-first UAT passes.
- **P01 + P02 + P03:** LOCK — untouched.
- One plate per FAIL cycle; if Create dies, STOP; no Ken Burns fallback.
- Scores → CoS. Do not declare Ben PASS. Do not ping Ben.

## Related

- Prior mint green (superseded for remint ops): `PART04_BATCH_A_MINT_GREEN.md`
- Brief: `PRODUCTION_BRIEF_PART04_v01.md`
- Land index: `_qa_part04_batch_a/BATCH_A_LAND_INDEX.json` (11/11 landed; UAT FAIL)
