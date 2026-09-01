# Production status — 001 How Did We Discover Germs?

**Queue:** Finish this film, then one more HOS long, then compare Veo vs Omni. `hos-finish-then-compare-omni.mdc`

| Step | Status |
|---|---|
| Topic / cluster / VidIQ pre-build | DONE |
| Master script | `germs_script_master_v01.md` · **PASS 90.4** |
| Part 01 picture | **LOCKED** `hos_001_part01_rough_v21.mp4` |
| Part 02 picture | **LOCKED** `hos_001_part02_rough_v12.mp4` |
| Part 03 picture | **LOCKED** `hos_001_part03_LOCKED_v08.mp4` · remint `hos_001_part03_rough_v11.mp4` (faces) |
| Part 04 | **STOP for UAT** on `hos_001_part04_rough_v14.mp4` — 07 HOLDS v13; 05/06 v14 motion pass, S-curve FAIL |
| Part 05 | Parked until Part 04 PASS |
| Broadcast + Shorts | Later (Shorts only after the long is public; zero `/go/` on Shorts) |

## Locked artifacts

- Part 01: `09_Final-Export/hos_001_part01_rough_v21.mp4`
- Part 02: `09_Final-Export/hos_001_part02_rough_v12.mp4`
- Part 03: `09_Final-Export/hos_001_part03_LOCKED_v08.mp4`  
  sha256 `7e7ce4d5dd909888a222983b58972dc08612442c51a65e6bf619f33f3e08b368`  
  Dur 71.292s · VO `part03_childbirth_ward_v01`  
  Superseded: `hos_001_part03_LOCKED_v05.mp4`

## Part 03 UAT remint — PASS

- Parent v09 stays: `hos_001_part03_rough_v09.mp4` sha256 `3fe17eefb51553ebb4a58c442fe78812c2b943d9a34d8a4f5d0188fc563173fe`
- Cut: `09_Final-Export/hos_001_part03_rough_v10.mp4` (also **HOS UAT**)
- sha256 `cd84798f72d4096512ff80644686ddacc22780499b17e246a22d9e13e44b1608`
- Dur **71.292s** · VO 70.480s (`part03_childbirth_ward_v01`)
- `07_mocked_v10` Fast T2V (backs/sides, no portrait two-shot). mean 14.63 / first 35.99
- 06 HOLDS. Did not remint 01–06 or 08–10. Chapter “A childbirth ward, 1840s”. THE VECTOR stays.
- Do **not** remint Part 03. Do **not** overwrite `LOCKED_v08` or rough_v09

## Part 04 v10 — FAIL (do not overwrite)

- Cut: `09_Final-Export/hos_001_part04_rough_v10.mp4` (also **HOS UAT**)
- sha256 `73e2e209b4cc3737ebf9955c1ecc83cb491fd33fa6d37bda7883f449d9801724`
- Dur **82.560s** · VO 81.760s (`part04_proof_in_a_flask_v01`)
- `07_bloom_cloud_v10` FAIL: round-bottom straight-neck flask + oversized worm-germs. Left in place.

## Part 04 v11 UAT remint (not locked)

- Cut: `09_Final-Export/hos_001_part04_rough_v11.mp4` (also **HOS UAT**, v10 not overwritten)
- sha256 `121ad804de63812bf6a29cb1a937325ad874194afc053a15fc1aff9d33ebc2b2`
- Dur **82.560s** · VO 81.760s (`part04_proof_in_a_flask_v01`)
- `07_bloom_cloud_v11` Fast T2V only (no still / Ingredients / harvest). One Create + one remint then STOP.
- First take archived `_rejected_flask_07_bloom_cloud_v11.mp4` (straight neck + worms).
- Remint motion pass: mean **4.34** / first **6.12**. Room is the frame. Glass intact. Broth clouds by t720.
- **07 QA FAIL (stop):** no swan-neck S-curve. Still a round-bottom straight-neck flask. Oversized worm/lump germs still hero-scale. Not Erlenmeyer as the only flask.
- KEEP 01–06 and 08–12 from the v10 plate set. Stack unchanged (chapter, labels, bed, FX). VO unchanged.

## Part 03 v11 remint (faces)

- Cut: `09_Final-Export/hos_001_part03_rough_v11.mp4` (also **HOS UAT**)
- sha256 `759308347e919cfbd75b89fc6b844cf623bef7e9b5846643dc3f89e420ea08c7`
- Dur **71.292s** · bytes **36798231** · VO 70.480s
- `07_mocked_v11` Fast T2V only (no still / Add to Prompt). Create alive. mean **4.84** / first **15.25**
- Faces finished (eyes/nose/mouth), dark-haired Semmelweis + grey-haired colleague, living ward. No remint.
- KEEP 01–06 (Explorer 06 HOLDS) and 08–10.
- Labels locked: SEMMELWEIS 26.54–28.15 · HANDWASHING 34.78–35.70 · THE VECTOR 44.82–49.02 · chapter 1.50–5.00

## Part 04 v14 remint (05 + 06 only)

- Cut: `09_Final-Export/hos_001_part04_rough_v14.mp4` (also **HOS UAT**; v13 not overwritten)
- sha256 `2d42a7d163defdfade13ef71cf53ef6a75e47b4bc9b0f909e00474f0305fa188`
- Dur **82.560s** · bytes **52289617** · VO 81.760s
- `06_explorer_watches_v14` then `05_tip_the_trap_v14` Fast T2V. Create alive. No remint (motion passed).
- 06 motion 11.50 / 34.54. Teal Explorer + one scientist + amber PASS. S-curve FAIL (straight neck).
- 05 motion 8.15 / 48.01. Upright, no pour PASS. S-curve FAIL. Late pills / steam-orb FAIL.
- `07_bloom_cloud_v13` HOLDS sha256 `fd5d4f7470386ae1bf2eba745cd2d695c402c549cd6fc061edd885fdb34d3604`

## Next

1. Part 03 `hos_001_part03_rough_v11.mp4` and Part 04 `hos_001_part04_rough_v14.mp4` in **HOS UAT**.
2. Do not start Part 05 until Part 04 PASS.
3. Do not remint Part 01 v21 or Part 02 v12. Do not touch 07 v13. Do not spend Omni on Neutron Star.
