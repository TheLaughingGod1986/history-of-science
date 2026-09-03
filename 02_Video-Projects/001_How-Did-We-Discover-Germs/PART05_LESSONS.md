# Part 05 lessons — Clean Hands, Clean Cuts

**Date:** 2026-09-02  
**Status:** **LOCKED.** `09_Final-Export/hos_001_part05_rough_v03.mp4` (also **HOS UAT**).  
sha256 `7aec17d498f65aaa3312f0d8f04e4411fa5debeff5eb646b5effa61d3f54e194`  
**PARK.** Do not remint. Do not recut. Do not start Part 06. Do not unlock. Do not start 002. Full join `hos_001_germs_full_v02.mp4` is UAT PASS (live cut). Long Premiere `_C92tIJCk8A` Thu 3 Sep 18:00 London. Shorts stay on disk for UAT — do not upload.

Part 04 official: `hos_001_part04_rough_v23.mp4`  
sha256 `afe44645ddcfbc649baca52a7720e083d48125d5fd6ca32606b3fb2c951fe763` (unchanged)

## Cut on disk (v01 — FAIL)

- File: `hos_001_part05_rough_v01.mp4`
- sha256 `e9097e0fca460a04ec3b4f5203d946384e9f227436e97b5e9c4a0ec0a5230572`
- Dur **46.500s** · VO 45.680s (`part05_clean_hands_v01.wav`) · bytes 34801158
- Title: Clean Hands, Clean Cuts
- Chapter: “A surgical theatre” 1.50–5.00 left (after moving picture)
- Labels: LISTER 0.20–1.40 · SPRAY 8.13–12.33 · PROTOCOL 20.84–25.04 · SOAP 31.06–34.50 · A MAP 34.70–38.90 · INVISIBLE 44.35–46.28
- Bed: ward-family, lift at SOAP 31.056. FX: cloth / water / spray / wood. No metal tray.

## Ben UAT FAIL (v01)

| Plate | Time | Kid | Gate |
|---|---|---|---|
| **06 soap_hands** | ~0:39–0:40 | cartoon bugs | no cartoon germ sprites, no purple blobs, no germ-macro hero |
| 04 explorer_scrubs | ~0:21 | grey balls in the air | no sprites; Explorer garnish once then leaves |
| 05 theatre_wins | ~0:24–0:29 | identical nurses + metal tray | living ward; nurses not twins; **NO metal tray** |

## KEEP as-is (do not remint)

| Plate | File |
|---|---|
| 01 old_theatre | `01_old_theatre_v01b.mp4` |
| 02 spray_scrub | `02_spray_scrub_v01c.mp4` |
| 03 protocol | `03_protocol_v01b.mp4` (Lister mutton chops + goatee, not VECTOR) |
| 07 a_map | `07_a_map_v01.mp4` |
| 08 last_light | `08_last_light_v01d.mp4` (one S-curve Pasteur) |

## v02 remint (once) — 04/06 FAIL, 05 KEEP

Scripts: `_mint_part05_flow_v02.py` · `_mint_part05_flow_v02b.py`  
Builder ready, not run: `_build_part05_rough_v02.py`

Create stayed alive (false `status=failed` banner still downloaded).

| Plate | File | Motion | Walk | Call |
|---|---|---|---|---|
| 04 | v02 then `v02b` | 7.52 / 2.72 | grey spheres t000 / t100 / t400 / t720 (CLIP_USE 6.20) | **FAIL** |
| 05 | `05_theatre_wins_v02.mp4` | 11.77 / 29.31 | three distinct nurses (older grey / younger brown curls / darker skin); wooden bowls; no sprites; metal basin only t720 outside CLIP_USE | **KEEP** |
| 06 | v02 then `v02b` | 8.12 / 23.02 | t000 cleaner; blue/pink orbs on wrists t100 + t400 (in CLIP_USE); white pill sprites in water t720 | **FAIL** |

Archived: `_rejected_spheres_04_explorer_scrubs_v02.mp4` · `_rejected_orbs_06_soap_hands_v02.mp4` · `_rejected_spheres_04_explorer_scrubs_v02b.mp4` · `_rejected_orbs_06_soap_hands_v02b.mp4`

**Did not assemble** `hos_001_part05_rough_v02.mp4`.

## v02c remint (once) — 04/06 FAIL again

Script: `_mint_part05_flow_v02c.py`  
Fast T2V. No I2V. Positive prompts only (no germ / fever / microbe / purple / bacteria / bug / orbs / “no X”). Create stayed alive.

| Plate | File | Motion | Walk | Call |
|---|---|---|---|---|
| 04 | v02c | 9.21 / 14.96 | t000 blue spheres in the wash; t100 bright-blue lather; t400/t720 air clear, Explorer left. Pith helmet. | **FAIL** |
| 05 | `05_theatre_wins_v02.mp4` | — | unchanged | **KEEP** |
| 06 | v02c | 17.48 / 50.03 | t000 / t100 / t400 light-blue spheres on wrists + basin rim; t720 blue spheres on the stone | **FAIL** |

Archived: `_rejected_blue_04_explorer_scrubs_v02c.mp4` · `_rejected_orbs_06_soap_hands_v02c.mp4`

**Did not assemble** then.

## v02d remint — 04/06 KEEP, assembled v02

Script: `_mint_part05_flow_v02d.py` · Builder: `_build_part05_rough_v02.py`  
Composition change: 04 = aisle walk-out (no wash). 06 = medium basin still life (no hands). Fast T2V. Create stayed alive.

| Plate | File | Motion | Walk | Call |
|---|---|---|---|---|
| 04 | `04_explorer_scrubs_v02d.mp4` | 10.32 / 24.40 | teal coat, no hat; walks aisle; gone t720; lamp steam only | **KEEP** |
| 05 | `05_theatre_wins_v02.mp4` | — | unchanged | **KEEP** |
| 06 | `06_soap_hands_v02d.mp4` | 3.49 / 6.88 | medium basin, brass tap, white soap on cloth, foam in bowl; no hands | **KEEP** |

Cut: `hos_001_part05_rough_v02.mp4`  
sha256 `8d04bf6954a39296157da9c27806ea311d657aac14ce22e76cb9cef1cdf5266c`  
Dur **46.500s** · VO 45.680s · bytes 34435429

## Lessons that held

- Veo Fast stamps purple/grey/coloured sprites when the prompt says germ / fever / microbe / purple / bacteria / bug. Drop those words.
- **Negation also stamps.** “No grey balls / no orbs / no pink / no blue” still paints orbs.
- **Positive-only still stamped blue on wrist CUs.** v02c named only theatre / teal coat / wet hands / white soap foam — Veo still painted light-blue spheres on 04 wash + 06 wrists/rim.
- **Composition change fixed it.** Stop minting wrist CUs. 04 = Explorer leaving the aisle. 06 = medium basin still life, no skin.
- Do **not** I2V 04 from `explorer_sheet.jpg`.
- t72 raw still has a second straight-neck on the right. Use `t72_pasteur_lock_one_flask.jpg`.
- Create false `status=failed` banner can still download. Real die = no media after ~190s.
- 05 clone-nurse FAIL was identical faces + metal tray. v02 KEEP used three different faces/ages and wooden bowls.

## Continuity

- One classic Pasteur: t72 S-curve, round-bottom on wood, small on “what else is still invisible”.
- Lister ≠ VECTOR mustache. Explorer garnish once then leaves.
- No cartoon germ sprites, no matching-coat twins, no top hats, no metal tray, no Ken Burns.

## v03 recut — pull 07 tail CU (no mint)

Builder: `_build_part05_rough_v03.py`  
`07_a_map_v01` prompt trucks ward → theatre → washed hands. After ~3s it becomes the rejected soap_hands germ-macro. v02 used 6.20s of it, so ~0:39–0:40 was that leftover.

Uses: 01–05 = 6.20 · 06 SOAP v02d = 8.00 · 07 = **2.50** (empty theatre only) · 08d = 8.00.

Cut: `hos_001_part05_rough_v03.mp4`  
sha256 `7aec17d498f65aaa3312f0d8f04e4411fa5debeff5eb646b5effa61d3f54e194`  
Dur **46.500s** · VO 45.680s · bytes 32942895

Walk: 0:32 SOAP basin · 0:36 SOAP · 0:37–0:38 empty theatre · 0:39–0:44 one S-curve Pasteur. No wrist CU. No cartoon orbs.

## Next

**PARK.** Parts 01–05 LOCKED. Full join `hos_001_germs_full_v02.mp4` **UAT PASS**. Long Premiere `_C92tIJCk8A` Thu 3 Sep 18:00 London. Shorts stay on disk for UAT. Do not remint. Do not upload Shorts. Do not start 002. CoS pinged Ben.
