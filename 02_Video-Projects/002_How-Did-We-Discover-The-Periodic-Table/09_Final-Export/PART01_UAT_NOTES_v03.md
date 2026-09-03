# Part 01 UAT — hos_002_part01_rough_v03

**File:** `09_Final-Export/hos_002_part01_rough_v03.mp4`  
**sha256:** `96e94430e125520f6b683ac425983a6d4a19a3ccf5a6826919160ba6c8105952`  
**Duration:** 85.67s (VO lock 85.68s)  
**Engine:** Flow Veo 3.1 Fast T2V · 12 unique plates · remint 01/05/09 (v02) + plate09 v03 · no freeze-pad  
**Status:** STOP for Ben UAT — do not start Part 02

## What changed from v01 → v03

| Plate | v01 issue | v03 result |
|---|---|---|
| `01_empty_chairs_open` | Chalkboard readable marks | **Improved** — blank walls, glowing empty chairs |
| `05_explorer_ore_gas` | Off-model Explorer + smiley rock | **Improved** — teal coat, glasses, ore; no smiley rock |
| `09_seating_plan_gap` | Hologram flask / not seating plan | **Still fail** — Flow keeps rendering natural-history museum + dinosaur (v02 + v03 T2V). Needs still-frame I2V pass on mini |

## Spot-check stills

`09_Final-Export/_uat_part01_v02/` (00, 05, 09_v03, 12)

1. **Open** — PASS candidate.  
2. **Explorer** — PASS candidate.  
3. **Seating plan** — REGEN recommended (museum drift). Next pass: Gemini still → Flow I2V from start frame.  
4. No Orbit robot. Style OK for first rough.

## Ask Ben

- **PASS** with plate 09 museum drift and move to Part 02?  
- **REGEN** only `09_seating_plan_gap` (recommended)?  
- Anything else on 01 or 05?
