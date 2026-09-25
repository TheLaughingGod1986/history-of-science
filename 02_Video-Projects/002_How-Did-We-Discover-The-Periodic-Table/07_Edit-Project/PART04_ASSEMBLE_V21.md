# P04 Empty Chairs — ASSEMBLE UNLOCK → `hos_002_part04_rough_v21`

**CoS 10 Sep 2026:** all reminted plates KEEP. Unlock assemble.  
**Rough version:** `hos_002_part04_rough_v21.mp4`  
**Parent picture pack:** v20 assemble map + swap in four KEEP remints below.  
**VO:** `02_Voiceover/part04_empty_chairs_v01.wav`  
**Bed:** `05_Music/hos_002_part01_curious_workshop_v02_norm.wav` (curious, not death-ward)  
**Do not touch** P01–P03. Scores → CoS. Do **not** declare PASS / ping Ben from Picture.

---

## Locked KEEP remints (must hash-match)

| Plate | File | sha256 |
|---|---|---|
| `06_explorer_leaves_gap` | `04_Generated-Clips/part04/raw/v20_fast/06_explorer_leaves_gap_v20_try3.mp4` | `df9bb44fb123e1a737976517be0dc809470f1828f1dba0dc8f1178f59721978c` |
| `09b_risk_hold` | `04_Generated-Clips/part04/raw/v20_quality/09b_risk_hold_v20_try14.mp4` | `47a6bdebed079d46e48950d3b544388a807c79258d1114b39ab596ebf6f44c38` |
| `11_publish_gaps` | `04_Generated-Clips/part04/raw/v20_fast/11_publish_gaps_v20_try9.mp4` | `97d0c419fdf7720f366140a9fb2b024a29580a2db51a434e7afb425a19f8cc72` |
| `11b_wait_and_hunt` | `04_Generated-Clips/part04/raw/v20_fast/11b_wait_and_hunt_v20_try1.mp4` | `5602762e82fd40eb654b25a5d3e5260e8baf79707fb19ecf8b58ede67cb3075e` |

STOP if any sha mismatches. Prefer canonical filenames above (or hardlink/copy into assemble inputs).

---

## Assemble rules

1. Same `PLATE_ORDER` as `_assemble_part04_rough_v20.py` (01…11b).  
2. Swap **only** the four KEEP remints; all other plates stay the v20 KEEP/prior sources map.  
3. Animistry side labels with spoken words (existing SIDE_LABELS cue sheet).  
4. Picture with VO — no 5–10s lag regressions on EMPTY SEATS / PUBLISH / A BET hold.  
5. Export: `09_Final-Export/hos_002_part04_rough_v21.mp4` + sha256 + duration + bytes.  
6. Copy to iCloud `HOS UAT/hos_002_part04_rough_v21.mp4` + `WATCH_part04_v21.txt`.  
7. Plate-library: this is assemble-last after plate UAT — do not remint during assemble.  
8. CoS owns Ben ping after UAT.

---

## Brief paths

- **This assemble brief:** `07_Edit-Project/PART04_ASSEMBLE_V21.md`  
- Board: `PART04_PLATE_BOARD_AFTER_11B.md`  
- Script: `01_Script/part04_empty_chairs_v01.md`  
- Parent assemble script to fork: `_assemble_part04_rough_v20.py` → `_assemble_part04_rough_v21.py`
