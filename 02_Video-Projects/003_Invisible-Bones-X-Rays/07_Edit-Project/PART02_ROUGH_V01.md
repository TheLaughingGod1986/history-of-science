# HOS 003 Part 02 rough v01 — assemble notes

**For:** CoS soft check. Do not ping Ben. Do not declare PASS.  
**Cut:** `09_Final-Export/hos_003_part02_rough_v01.mp4`  
**sha256:** `53d09b8d87c24a01903f5e77474bb8bb7a2ba7ccf08c904c370e1ccdd8e350e0`  
**bytes:** 47864380 · **duration:** 69.208s  
**iCloud:** `~/Library/Mobile Documents/com~apple~CloudDocs/HOS UAT/hos_003_part02_rough_v01.mp4` (same sha)

## What landed

- VO: `02_Voiceover/05_Master/hos_003_part02_vo_v01_draft.wav` from `part02_the_cardboard_v02.txt` (sha `f3454130…`, do not fork). Same Ben Orbit Narrator lock as Part 01.
- Align: `hos_003_part02_vo_v01_draft_align.json`
- Bed: Germs `hos_001_part01_ominous_ward_v14_norm.wav` at 0.34, fade-out on the last ~2.3s (holds, not a dead cut).
- Teaching density: Didot italic side labels one-at-a-time + four teach cards, timed from VO alignment (Part 01 v03 house).
- Plates: KEEP only. Parked `01_chapter_cardboard` and `03_cardboard_waiting` skipped.

## A/V

Nine unique 8s plates + 0.35s xfade ≈ **69.2s** picture. VO draft is longer (~105s). v01 trims VO to picture — same pattern as Part 01 rough v01. No freeze / Ken Burns / loop. Full wav stays on disk for a later part if CoS unlocks more unique plates.

## Self-check vs `PART02_ACCEPTANCE.md` hard rejects

| Reject | v01 |
|---|---|
| Orbit | None in KEEP stills |
| Germs ward reuse | Lab / cardboard / door only — ward bed is audio cousin, not picture |
| Periodic desk | No cream-card desk / empty chairs |
| Photoreal | 3D cartoon |
| Gore | None |
| Lava | None |
| Underside bulb | None spotted on KEEP stills |
| Unfinished Explorer hair | No Explorer this part |
| Ken Burns ship | Real Veo motion, no still-pad |

## Soft risks (do not remint this cycle)

- Some KEEP glow plates read **TV-shaped** cardboard (05 / 09 / 10). 04 + 11 are flatter. House prefers flat cardboard; CoS can FAIL with stills if Ben hates the CRT silhouette.
- `07_names_it_x` draws the **X** late in the take (circle first).
- VO overhang means late lines (metal / pattern / first detector) are on the wav but not in this mix.

## Scripts

- `02_Voiceover/_generate_part02_vo_v01.py`
- `07_Edit-Project/_assemble_part02_rough_v01.py`
