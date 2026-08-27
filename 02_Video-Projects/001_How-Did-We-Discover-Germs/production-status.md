# Production status — 001 How Did We Discover Germs?

| Step | Status |
|---|---|
| Topic score | DONE |
| Cluster plan | DONE |
| Pre-build VidIQ audit | SIGNED (live VidIQ re-score before upload) |
| Master script | `germs_script_master_v01.md` |
| Script / gate | **PASS 90.4** |
| Shorts cadence | Cluster 4–6 · **not daily** |
| Part 01 VO | DONE · Ben Orbit Narrator |
| Part 01 picture | **PASS — `hos_001_part01_rough_v08.mp4`** |
| Style / microbe / motion locks | **LOCKED** |
| Part 02 VO + stills | DONE |
| Part 02 picture | **9/10 Flow I2V done** (01–09). Plate **10** blocked on Flow credits. **No assemble. No Ken Burns. STOP — not Ben UAT yet.** |
| Parts 03–05 | Blocked on real animated Part 02 + Ben UAT |
| Broadcast + Shorts | Later (Shorts only after long is public; zero `/go/` on Shorts) |

## Artifacts

- Part 01 locked: `/opt/cursor/artifacts/hos_001_part01_LOCKED_v08.mp4`
- Part 02 real plates: `04_Generated-Clips/part02/raw/v01_flow/` (**01–09**; **10 missing**)
- Part 02 still-push (REJECT): `09_Final-Export/hos_001_part02_rough_v01_STILLPUSH_REJECT.mp4`
- Part 02 animated rough: **not built** (waiting on plate 10)

## Quota (2026-08-27 night)

- **Gemini Veo API:** prepaid depleted (separate from Free Trial / GDP).
- **Flow Ultra:** Veo **3.1 Lite** generated plates **02–04, 06–09** this session after 01+05 already existed. Plate **10** then failed with exact UI copy:
  **`Not enough Google Flow and AI credits to perform this action. Try other settings or get more AI credits.`**
- Create/send control gone (info chip only). Did not switch model. Did not Ken Burns.

## Next

1. When Flow credits exist: Lite I2V **10_pullback_to_lab** only (`_gen_part02_remaining_lite.py` skip-existing).
2. Assemble `hos_001_part02_rough_v01.mp4` via `_build_part02_flow_v01.py` (RAW `v01_flow`) → copy to `/opt/cursor/artifacts` + demo.
3. Ben UAT Part 02 (animated). Then Part 03.
