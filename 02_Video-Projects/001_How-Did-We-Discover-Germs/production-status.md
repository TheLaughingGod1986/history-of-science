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
| Part 02 picture | **BLOCKED** — Ben: not animated. Still-push REJECT. 1/10 real Flow plate. Re-probe 27 Aug AM: Flow daily gen limit + API prepaid depleted |
| Parts 03–05 | Blocked on real animated Part 02 + Ben UAT |
| Broadcast + Shorts | Later (Shorts only after long is public) |

## Artifacts

- Part 01 locked: `/opt/cursor/artifacts/hos_001_part01_LOCKED_v08.mp4`
- Part 02 real plate sample: `04_Generated-Clips/part02/raw/v01_flow/05_microbial_city_v01.mp4`
- Part 02 still-push (REJECT): `09_Final-Export/hos_001_part02_rough_v01_STILLPUSH_REJECT.mp4`

## Quota (re-probe 2026-08-27 ~09:15 UTC)

- **Gemini Veo API:** 429 — prepaid credits **depleted** (not just RPD). Top up at AI Studio billing.
- **Flow Ultra:** ~57 Flow credits showing, but Create still fails: **daily generation limit**. Separate from credit balance.
- Need: Flow daily gen reset **and/or** buy AI credits / top up API prepaid — then burn remaining 9 Part 02 Veo Fast plates (~90 Flow credits at 10 each; may need AI credits top-up).

## Next

1. Unblock gens (Flow daily reset and/or AI credits / API prepaid).
2. Generate remaining 9 Part 02 Flow I2V plates → assemble real `hos_001_part02_rough_v01.mp4`.
3. Ben UAT Part 02 (animated). Then Part 03.
