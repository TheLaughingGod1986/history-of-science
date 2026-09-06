# Part 03 status — A Ruler for Atoms

**Updated:** 6 Sep 2026 22:45 Europe/London (HOS Local Mini · auth probe)

## Ben / Showrunner locks

| Cut | Status |
|---|---|
| `hos_002_part01_rough_v14.mp4` | **LOCKED PASS.** Do **not** remint / overwrite. |
| `hos_002_part02_rough_v06.mp4` | **LOCKED.** Do **not** remint / overwrite. |
| Part 03 | **BLOCKED_AUTH** — wrong Google account on Mini Flow profile |
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

## BLOCKED_AUTH — 6 Sep 22:45 (Mini live probe)

Ben phone proof: Flow signed in as **benoats@googlemail.com** with **10,050 Google Flow credits**.

Mini Playwright profile `~/.playwright-hos-flow-profile` is signed in as **benoats86@gmail.com** (different account).

Live probe evidence:

- `logs/flow_auth_probe_20260906.json` → `verdict: BLOCKED_AUTH`, `active_email: benoats86@gmail.com`
- Aria label: `Google Account: Benjamin Oats (benoats86@gmail.com)`
- Screens: `logs/flow_auth_probe_20260906_account.png`, `logs/flow_auth_probe_20260906_credits_menu.png`
- Prior Create-die / “out of credits” on Fast was this wrong account — not the credited mailbox

**Hard stop.** No mint. No Ken Burns. No password paste. Ben must switch Mini Flow to `benoats@googlemail.com` himself, then re-run mint.

Mint script now hard-gates on account (`require_flow_account`) and will refuse `benoats86@gmail.com`.

## When Mini is on benoats@googlemail.com

1. Confirm Flow account chip + credits visible
2. `_mint_part03_flow_v01.py` (all 12 · Veo 3.1 Fast only)
3. QA: 16:9 · real motion · opaque vessels · no clear liquid glass · no vessel fire · Explorer once on 05
4. `_assemble_part03_rough_v01.py` → print path + bytes + sha256 + duration
5. Hand to HOS UAT. **Do not** ping Ben.

## Do not

- Remint Part 01 / 02
- Ship Ken Burns / still-push / freeze-pad
- Use Omni Flash as a substitute for Veo Fast
- Mint while signed in as `benoats86@gmail.com`
- Paste passwords / switch accounts for Ben
- Start Part 04
- Ping Ben
