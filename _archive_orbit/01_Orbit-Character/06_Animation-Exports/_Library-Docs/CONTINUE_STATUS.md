# Continue status — 2026-07-27 (Eiffel incident)

## Confirmed bug
Priority A v1 used **Eiffel Tower Explore blueprint** as `start_frame` (not Orbit).
Quarantined in `_Rejected/eiffel-startframe-2026-07-27/`.

## Regen status
- **1 good:** `Hover/orbit_idle-hover_v01.mp4` — start asset `orbit-seedance-reference-v01.png`
- **Second regen batch:** still bound Explore Eiffel asset (`explore_asset_*`, ~5.3MB) — **do not use**
- Remaining Priority A still need correct Orbit-only regen

## Guardrail
Before Generate, start-frame asset **name must be** `orbit-seedance-reference-v01.png` (~954KB).  
Abort if name is `explore_asset_*` or size ~5.3MB.
