# P04 Empty Chairs — ASSEMBLE STAGED → `hos_002_part04_rough_v22`

**Showrunner 10 Sep 2026 evening burn:** stage now; Mini launches the moment plate **10** UAT KEEPs.  
**Rough version:** `hos_002_part04_rough_v22.mp4`  
**Parent picture pack:** v21 assemble map + swap in lava-desk remints below (`05` KEEP + `10` TBD).  
**VO:** `02_Voiceover/part04_empty_chairs_v01.wav`  
**Bed:** `05_Music/hos_002_part01_curious_workshop_v02_norm.wav` (curious, not death-ward)  
**Do not touch** P01–P03. Scores → CoS. Do **not** declare PASS / ping Ben from Picture.  
**P05** stays gated until Ben KEEP/LOCK on this cut.

---

## Why v22

Parent `hos_002_part04_rough_v21.mp4` sha `868a012c…` HARD FAIL lava drip:
- PERIODIC TABLE ~t38–43 → remint `05_columns_families`
- FAMILY FIRST ~t108 → remint `10_family_before_weight`

Master: `PART04_V22_LAVA_DESK_REMINT.md`

---

## Locked KEEP remints (must hash-match)

| Plate | File | sha256 | Status |
|---|---|---|---|
| `05_columns_families` | `04_Generated-Clips/part04/raw/v22_quality/05_columns_families_v22_try2B.mp4` | `49437e7e4004c224b021409e15ebb50fb06b74737adfe2b6c0bc0a61bfae8caa` | **KEEP** (try2B BOARDTOP Quality) |
| `10_family_before_weight` | `04_Generated-Clips/part04/raw/v22_quality/10_family_before_weight_v22_tryN.mp4` | **TBD — paste on plate UAT KEEP** | **IN FLIGHT** (Quality; prefer BOARDTOP DNA join) |
| `06_explorer_leaves_gap` | `04_Generated-Clips/part04/raw/v20_fast/06_explorer_leaves_gap_v20_try3.mp4` | `df9bb44fb123e1a737976517be0dc809470f1828f1dba0dc8f1178f59721978c` | KEEP hold |
| `09b_risk_hold` | `04_Generated-Clips/part04/raw/v20_quality/09b_risk_hold_v20_try14.mp4` | `47a6bdebed079d46e48950d3b544388a807c79258d1114b39ab596ebf6f44c38` | KEEP hold |
| `11_publish_gaps` | `04_Generated-Clips/part04/raw/v20_fast/11_publish_gaps_v20_try9.mp4` | `97d0c419fdf7720f366140a9fb2b024a29580a2db51a434e7afb425a19f8cc72` | KEEP hold |
| `11b_wait_and_hunt` | `04_Generated-Clips/part04/raw/v20_fast/11b_wait_and_hunt_v20_try1.mp4` | `5602762e82fd40eb654b25a5d3e5260e8baf79707fb19ecf8b58ede67cb3075e` | KEEP hold |

STOP if any sha mismatches. On 10 KEEP: fill path + full sha256 in this table before assemble runs (or CoS patches in-line).

---

## Assemble rules

1. Same `PLATE_ORDER` as `_assemble_part04_rough_v21.py` (01…11b).  
2. Fork `_assemble_part04_rough_v21.py` → `_assemble_part04_rough_v22.py`.  
3. Swap **`05`** + **`10`** to the KEEP remints above; keep all other v21 sources (including prior KEEP hold 06/09b/11/11b).  
4. Animistry side labels with spoken words (existing SIDE_LABELS cue sheet).  
5. Picture with VO — no lag regressions on PERIODIC TABLE / FAMILY FIRST / EMPTY SEATS / PUBLISH.  
6. **UAT scrub focus:** no lava drip / molten bead on PERIODIC TABLE (~t38–43) or FAMILY FIRST (~t108).  
7. Export: `09_Final-Export/hos_002_part04_rough_v22.mp4` + sha256 + duration + bytes.  
8. Copy to iCloud `HOS UAT/hos_002_part04_rough_v22.mp4` + `WATCH_part04_v22.txt`.  
9. Plate-library: assemble-last after plate UAT — do not remint during assemble.  
10. CoS owns Ben ping after UAT (PASS only).

---

## Gate

- **Do not assemble** until plate `10_family_before_weight` continuous-playback plate UAT = KEEP and sha is written above.  
- Create dies → STOP (no Ken Burns).  
- Flow: `benoats@googlemail.com` ULTRA.

---

## Brief paths

- **This assemble brief:** `07_Edit-Project/PART04_ASSEMBLE_V22.md`  
- Lava remint master: `PART04_V22_LAVA_DESK_REMINT.md`  
- Plate 05 KEEP note: `PART04_V22_PLATE_05_TRY2_COS.md`  
- Plate 10 brief: `PART04_NEXT_PLATE_10_FAMILY_NO_LAVA.md`  
- Script: `01_Script/part04_empty_chairs_v01.md`  
- Parent assemble script to fork: `_assemble_part04_rough_v21.py` → `_assemble_part04_rough_v22.py`
