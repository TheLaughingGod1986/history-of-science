# Vertex credit lag fix (Grok, 4 Oct 2026)

Authority: Claude #180 **5981276239**.

## Formula (now in code)
```
usable_gbp = last_console_gbp
           − (Σ logged Vertex take+still $ since that reading) × GBP_PER_USD
           − FLOOR_GBP(5)
```
- **Never** the console figure alone.
- When consecutive readings share the same Free Trial £ (lag plateau), baseline = **first** of those equal readings.
- `GBP_PER_USD = 0.80` = `PICTURE_PLAN_v01.json` → `rates.gbp_per_usd_planning` (not the 0.742 `gbp_per_usd_005_actual`).
- Patched: `_vertex_credit_v01.py`, `_mint_vertex_v01.py` (`projected_gbp` / `usable_gbp` / `guard`).

## Current figure (no new mint; logs only)
| Input | Value |
|---|---|
| Lag plateau start | `before_part02_resume_2026-10-04` @ 2026-10-04T14:37:25Z |
| Console Free Trial | **£37.48** (same through `after_part02_remints`) |
| Spend since plateau | **$11.390** (Part 02 resume takes 12,14–22 + remints 02/07/08 t2 + stills) |
| Spend × 0.8 | £9.112 |
| est_remaining | 37.48 − 9.112 = **£28.368** |
| **usable** | 28.368 − 5 = **£23.37** |

Film-wide logged Vertex spend remains ~$36.88 (`PART02_TOTAL_after_strategy_a_20261004.txt`); that full total must **not** be subtracted from £37.48 (most of Part 02 was minted before this plateau). Claude’s hand £16 used full Part 02 $21.62 against the lagging console — that over-subtracts pre-plateau spend; code uses spend-since-plateau only.

**Nothing more mints until UAT is posted** (this review).
