# Part 01 UAT — hos_002_part01_rough_v07

**File:** `09_Final-Export/hos_002_part01_rough_v07.mp4`  
**iCloud:** `HOS UAT/hos_002_part01_rough_v07.mp4` (same folder as Germs UAT)  
**sha256:** `5a49e103307d1417771bde5624ee90f3ea52f50821af1e7740024134ad66c951`  
**Duration:** 85.67s (VO lock 85.68s)  
**Status:** STOP for Ben UAT — do not start Part 02 picture/VO

## Why v07 (Ben notes on v05)

v05 looked quite good. Three fixes:

1. **Glassware** — vials/flasks were liquid in some plates and packed solids in others. Lock: **clear colored liquid in glass**; ores/rocks on wood only.
2. **Explorer** — must be the same boy as Germs 001 (teal coat, gold glasses, atom pin, satchel + compass). v06 I2V from the Germs still kept him in the **hospital ward**. v07 I2V from the workshop still puts him **in this chemistry workshop**, holding ore + a blue liquid jar.
3. **Music** — Part 01 had no underscore. v07 mixes a curious G-major flute + strings + harp bed under VO (vol 0.14, same sit-under as Germs). Wonder/workshop, not the death-ward D-minor.

## Spot-check

| Plate | v05 / v06 fail | v07 |
|---|---|---|
| `02_workshop_jars` | Mixed solids-in-glass | PASS candidate — colored liquids; ores on wood |
| `05_explorer_ore_gas` | Off-model, then ward | PASS candidate — Germs identity **in the workshop**; ore + blue liquid jar |
| `07_shelf_names_grow` | Gold flask with solid mass | PASS candidate — bubbling colored liquids; ores on shelves |
| `11_chemists_more_names` | Beads/spheres inside flasks | PASS candidate — clear liquids; ores on wood; blank cards |
| `09_seating_plan_gap` | Ghost chairs (fixed v06) | Kept opaque banquet chairs |

Stills: `09_Final-Export/_uat_part01_v07/`

## Ask Ben

**PASS** Part 01 → unlock Part 02 VO + picture?  
**REGEN** if Explorer still drifts from Germs, if any flask still reads as stuffing, or if the bed sits too loud/quiet under VO.
