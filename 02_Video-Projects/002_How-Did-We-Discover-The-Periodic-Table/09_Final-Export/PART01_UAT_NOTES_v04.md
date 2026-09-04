# Part 01 UAT — hos_002_part01_rough_v04

**File:** `09_Final-Export/hos_002_part01_rough_v04.mp4`  
**sha256:** `575ac412e4ee5f54e727f48b5e6b54b8f4248ff741539eaa787cd0ef4424b0cb`  
**Duration:** 85.67s (VO lock 85.68s)  
**Status:** STOP for Ben UAT — do not start Part 02

## v04 fix (plate 09)

T2V kept drifting to natural-history museum. **I2V from approved open still** (`00_open_empty_chairs.jpg`) fixed it — glowing wooden chairs in period hall, no dinosaur.

| Plate | v03 | v04 |
|---|---|---|
| `01_empty_chairs_open` | PASS | unchanged |
| `05_explorer_ore_gas` | PASS | unchanged |
| `09_seating_plan_gap` | Museum drift | **PASS candidate** — chairs read; rhymes visually with open (same hall family) |

## Spot-check stills

`09_Final-Export/_uat_part01_v02/`

- `00_open_empty_chairs.jpg` — strange picture first  
- `05_explorer_ore_gas.jpg` — Explorer on-model  
- `09_seating_plan_gap_raw_v04.jpg` — plate 09 raw (chairs, not museum)  
- `09_seating_plan_gap_v04_correct.jpg` — in rough at ~62s  

## Ask Ben

- **PASS** Part 01 → Part 02?  
- **REGEN** if open + seating-plan rhyme too close (acceptable for rough?)  
- Anything on Explorer plate 05?
