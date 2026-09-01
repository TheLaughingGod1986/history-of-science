# Production status — 001 How Did We Discover Germs?

**Queue:** Finish this film, then one more HOS long, then compare Veo vs Omni. `hos-finish-then-compare-omni.mdc`

| Step | Status |
|---|---|
| Topic / cluster / VidIQ pre-build | DONE |
| Master script | `germs_script_master_v01.md` · **PASS 90.4** |
| Part 01 picture | **LOCKED** `hos_001_part01_rough_v21.mp4` |
| Part 02 picture | **LOCKED** `hos_001_part02_rough_v12.mp4` |
| Part 03 picture | **LOCKED** `hos_001_part03_LOCKED_v08.mp4` · UAT remint `hos_001_part03_rough_v10.mp4` |
| Part 04 | **STOP for UAT** on `hos_001_part04_rough_v10.mp4` |
| Part 05 | Parked until Part 04 PASS |
| Broadcast + Shorts | Later (Shorts only after the long is public; zero `/go/` on Shorts) |

## Locked artifacts

- Part 01: `09_Final-Export/hos_001_part01_rough_v21.mp4`
- Part 02: `09_Final-Export/hos_001_part02_rough_v12.mp4`
- Part 03: `09_Final-Export/hos_001_part03_LOCKED_v08.mp4`  
  sha256 `7e7ce4d5dd909888a222983b58972dc08612442c51a65e6bf619f33f3e08b368`  
  Dur 71.292s · VO `part03_childbirth_ward_v01`  
  Superseded: `hos_001_part03_LOCKED_v05.mp4`

## Part 03 UAT remint (not locked)

- Parent v09 stays: `hos_001_part03_rough_v09.mp4` sha256 `3fe17eefb51553ebb4a58c442fe78812c2b943d9a34d8a4f5d0188fc563173fe`
- Cut: `09_Final-Export/hos_001_part03_rough_v10.mp4` (also **HOS UAT**)
- sha256 `cd84798f72d4096512ff80644686ddacc22780499b17e246a22d9e13e44b1608`
- Dur **71.292s** · VO 70.480s (`part03_childbirth_ward_v01`)
- `07_mocked_v10` Fast T2V (backs/sides, no portrait two-shot). mean 14.63 / first 35.99
- 06 HOLDS. Did not remint 01–06 or 08–10. Chapter “A childbirth ward, 1840s”. THE VECTOR stays.
- Do **not** overwrite `LOCKED_v08` or rough_v09

## Part 04 UAT remint (not locked)

- Parent v09 stays: `hos_001_part04_rough_v09.mp4` sha256 `abd8e969e761c0b8e10714f0fa1eb272c57c3550b52c7a49d89b600454524c86`
- Cut: `09_Final-Export/hos_001_part04_rough_v10.mp4` (also **HOS UAT**)
- sha256 `73e2e209b4cc3737ebf9955c1ecc83cb491fd33fa6d37bda7883f449d9801724`
- Dur **82.560s** · VO 81.760s (`part04_proof_in_a_flask_v01`)
- `07_bloom_cloud_v10` Fast T2V — no still, no harvest. Broth clouds, room is frame, glass intact. mean 10.89 / first 16.02
- Did not remint 01–06 or 08–12.

## Next

1. Part 03 `hos_001_part03_rough_v10.mp4` and Part 04 `hos_001_part04_rough_v10.mp4` in **HOS UAT** — neither locked. Parent v09 files stay.
2. Do not start Part 05 until Part 04 PASS.
3. Do not remint Part 01 v21 or Part 02 v12. Do not spend Omni on Neutron Star.
