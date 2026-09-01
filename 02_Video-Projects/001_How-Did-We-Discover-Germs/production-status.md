# Production status — 001 How Did We Discover Germs?

**Queue:** Finish this film, then one more HOS long, then compare Veo vs Omni. `hos-finish-then-compare-omni.mdc`

| Step | Status |
|---|---|
| Topic / cluster / VidIQ pre-build | DONE |
| Master script | `germs_script_master_v01.md` · **PASS 90.4** |
| Part 01 picture | **LOCKED** `hos_001_part01_rough_v21.mp4` |
| Part 02 picture | **LOCKED** `hos_001_part02_rough_v12.mp4` |
| Part 03 picture | **LOCKED** `hos_001_part03_LOCKED_v08.mp4` · UAT remint `hos_001_part03_rough_v09.mp4` |
| Part 04 | Harvest/rebuild `07_bloom_cloud` → `hos_001_part04_rough_v09.mp4` |
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

- Cut: `09_Final-Export/hos_001_part03_rough_v09.mp4` (also **HOS UAT**)
- sha256 `3fe17eefb51553ebb4a58c442fe78812c2b943d9a34d8a4f5d0188fc563173fe`
- Dur **71.292s** · VO 70.480s (`part03_childbirth_ward_v01`)
- Reminted `06_explorer_crosses_v09` Fast I2V (OTS walk, no palm germ)
- Do **not** overwrite `LOCKED_v08` or rough_v01/v02

## Part 04 watch

- Parent FAIL: `hos_001_part04_rough_v08.mp4` sha256 `89bfe1ecdfba3a12…` Dur **82.560s**
- Next export: `hos_001_part04_rough_v09.mp4` after harvest of `07_bloom_cloud`
- VO stays `part04_proof_in_a_flask_v01` — do not remint
- Do not remint 01, 06, 08, 09

## Next

1. Part 03 `hos_001_part03_rough_v09.mp4` in **HOS UAT** — not locked.
2. Part 04 harvest flask-grid takes, then assemble v09. Do not start Part 05.
3. Do not remint Part 01 v21 or Part 02 v12. Do not spend Omni on Neutron Star.
