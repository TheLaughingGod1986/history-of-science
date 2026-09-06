# Part 03 status — A Ruler for Atoms

**Updated:** 6 Sep 2026 22:22 Europe/London (Showrunner LOCK re-attempt · HOS Local Mini)

## Ben / Showrunner locks

| Cut | Status |
|---|---|
| `hos_002_part01_rough_v14.mp4` | **LOCKED PASS.** Do **not** remint / overwrite. |
| `hos_002_part02_rough_v06.mp4` | **LOCKED.** Do **not** remint / overwrite. |
| Part 03 | **BLOCKED (credits)** — Showrunner LOCK obeyed; no Ken Burns |
| Part 04 | Do **not** start |

## Target rough (not landed)

`/Users/benjaminoats/YouTube/History Of Science/02_Video-Projects/002_How-Did-We-Discover-The-Periodic-Table/09_Final-Export/hos_002_part03_rough_v01.mp4`

## Board (locked)

12 plates × ~8s · one Karlsruhe hall DNA · VO ~89.7s

| # | id | notes |
|---|---|---|
| 01 | `01_hall_open_side_label` | side: A RULER FOR ATOMS |
| 02 | `02_hall_argument` | |
| 03 | `03_method_pamphlet` | |
| 04 | `04_zoo_gets_ruler` | |
| 05 | `05_explorer_ruler` | Explorer ONCE · Germs younger-boy · I2V |
| 06 | `06_cards_snap_line` | |
| 07 | `07_light_to_heavy` | |
| 08 | `08_property_waves` | |
| 09 | `09_empty_chair_claim` | |
| 10 | `10_city_plan_lots` | |
| 11 | `11_fix_weights` | side: FIX THE WEIGHTS |
| 12 | `12_pattern_risks_public` | side: CHAOS HAS ADDRESS |

Inputs ready: script · VO · `parts/part-03_plates_v01.json` · `_mint_part03_flow_v01.py` · `_assemble_part03_rough_v01.py`

## BLOCKED — reconfirmed 6 Sep 22:13–22:20

Hard rule: real **Veo 3.1 Fast** every plate. Create dies / credits dry → **STOP**. No fake motion.

### Gemini API
Live probe: `429 RESOURCE_EXHAUSTED` — prepayment credits depleted (AI Studio).

### Flow UI (Veo 3.1 - Fast)
Smoke log: `logs/mint_part03_flow_smoke_plate01_20260906_221306.log`

- Model locked: **Veo 3.1 - Fast**
- Create submitted → immediate fail
- Page: *You're out of Google Flow credits…*
- Agent: *reached your credit or daily limit for the Veo 3.1 - Fast model*
- Suggested Omni Flash — **rejected** (Showrunner requires real Veo Fast, not Omni)
- Stall PNG refreshed under `04_Generated-Clips/part03/raw/v01_fast/`
- **Zero** landscape Veo mp4s on disk for Part 03

## When credits recover

1. `_mint_part03_flow_v01.py` (all 12 · Fast only)
2. QA: 16:9 · real motion · opaque vessels · no clear liquid glass · no vessel fire · Explorer once on 05
3. `_assemble_part03_rough_v01.py` → print path + bytes + sha256 + duration
4. Hand to HOS UAT. **Do not** ping Ben.

## Do not

- Remint Part 01 / 02
- Ship Ken Burns / still-push / freeze-pad
- Use Omni Flash as a substitute for Veo Fast
- Start Part 04
- Ping Ben
