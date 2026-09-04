# Part 01 UAT — hos_002_part01_rough_v02

**File:** `09_Final-Export/hos_002_part01_rough_v02.mp4`  
**sha256:** `719af156e49985b04da362fae708686b51bb421a22f37e778e6fdc9c600bc779`  
**Duration:** 85.67s (VO lock 85.68s)  
**Engine:** Flow Veo 3.1 Fast T2V · 12 unique plates · remint 01/05/09 (v02) · no freeze-pad  
**Status:** STOP for Ben UAT — do not start Part 02

## What changed from v01

| Plate | v01 issue | v02 result |
|---|---|---|
| `01_empty_chairs_open` | Chalkboard readable marks | **Improved** — blank walls, glowing empty chairs, strange picture first |
| `05_explorer_ore_gas` | Off-model Explorer + smiley rock | **Improved** — teal coat, glasses, ore; no smiley rock in spot-check still |
| `09_seating_plan_gap` | Hologram flask, not seating plan | **Still fail** — renders natural-history museum / dinosaur hall, not empty-chair seating plan |

## Spot-check stills

`09_Final-Export/_uat_part01_v02/`

1. **Open (empty chairs)** — PASS candidate. Glowing vacant chairs read; no chalkboard text.
2. **Explorer (05)** — PASS candidate. One boy, glasses, teal coat, satchel. Ore in hands; gas-jar beat weak in this frame but no mascot rock.
3. **Seating plan (09)** — **REGEN required.** VO says “seating plan nobody has dared to draw” — picture is a museum cabinet, not chairs at a table.
4. No Orbit orange robot spotted.
5. Style: Animistry-class 3D cartoon continuous motion — overall look OK for first rough.

## Ask Ben

- **PASS** Part 01 with plate 09 as-is (museum drift) and move to Part 02?  
- **REGEN** only `09_seating_plan_gap` (recommended)?  
- **REGEN** anything else on 01 or 05?

If REGEN 09: next pass should be I2V from a seating-plan still (long table + glowing empty chairs, no museum props).
