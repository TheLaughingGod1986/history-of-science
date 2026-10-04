# HOS 006 Part 02 — Strategy A run (Grok, 4 Oct 2026)

Authority: Claude #180 **5981112327** (Strategy A GO) + **5981064652** (£5 lag floor).

## Floor
- `FLOOR_GBP = 5.0` in `_mint_vertex_v01.py` + `_vertex_credit_v01.py`

## Credit (live CDP, account benoats@googlemail.com / gen-lang-client-0538779324)
| Label | Free Trial £ | Floor | Usable |
|---|---:|---:|---:|
| before_part02_resume_2026-10-04 | 37.48 | 5 | 32.48 |
| after_part02_batch2_2026-10-04 | 37.48 | 5 | 32.48 (lag) |
| after_part02_remints_2026-10-04 | 37.48 | 5 | 32.48 (lag) |

Projected after film spend (mint total): ~£36.22 (script). Live console still lagging at £37.48.

Part 02 mint log cost_usd_total ≈ **$21.62**. No card spend.

## Plates
| Plate | Result |
|---|---|
| 01_furnace_soil | KEEP t1 |
| 02_balance_200 | FAIL t1 + FAIL t2 (**twin stop**) — pot never on pan |
| 03_willow_shoot_scale | KEEP t1 |
| 04_lid_rain | KEEP t1 |
| 05_pure_water | KEEP t1 |
| 06_garden_years | FAIL t1 / **KEEP t2** (pot lock OK) |
| 07_explorer_snow | FAIL t1 + FAIL t2 (**twin stop**) — no real snow |
| 08_haul_tree | FAIL t1 + FAIL t2 (**twin stop**) — subject vanish |
| 09_weights_169 | KEEP t1 |
| 10_fallen_leaves | KEEP t1 |
| 11_furnace_again | **reuse** of 01 (board); not minted |
| 12_pointer_short | minted t1 PENDING_UAT |
| 13_tree_vs_pinch | KEEP t1 |
| 14–22 (ex 11) | minted t1 PENDING_UAT |

## Notes
- Batch 3 first try failed on **empty 0-byte seed stills** (v01 placeholders); quarantined; retried with v02/v03.
- Local Wan/LTX test queued (`LOCAL_WAN_LTX_TEST_QUEUE_20261004.md`); mint clear for ~22:19.
- Parts 03–05 parked. Remotion + 007 still queued.
- Do not merge #180.

## Desk follow-up (Claude 5981276239) — Grok same day
- Credit lag patch in `_vertex_credit_v01.py` (console − spend since plateau − £5).
- Twin-FAIL: see `TWIN_FAIL_DISPOSITION_20261004.md`.
- UAT quads 12+14–22: `uat_pending/` + `UAT_PENDING_12_14_22_20261004.md`.
- No new mints.
