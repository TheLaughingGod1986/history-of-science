# Part 03 status — A Ruler for Atoms

**Updated:** 6 Sep 2026 22:52 Europe/London (HOS Local Mini · Showrunner GO resume probe)

## Ben / Showrunner locks

| Cut | Status |
|---|---|
| `hos_002_part01_rough_v14.mp4` | **LOCKED PASS.** Do **not** remint / overwrite. |
| `hos_002_part02_rough_v06.mp4` | **LOCKED.** Do **not** remint / overwrite. |
| Part 03 | **BLOCKED_AUTH** — Mini Flow still on wrong Google account |
| Part 04 | Do **not** start |

## Target rough (not landed)

`/Users/benjaminoats/YouTube/History Of Science/02_Video-Projects/002_How-Did-We-Discover-The-Periodic-Table/09_Final-Export/hos_002_part03_rough_v01.mp4`

## BLOCKED_AUTH — Showrunner GO resume probe (22:52)

Showrunner GO received. Auth probe ran **before** any mint.

| Check | Result |
|---|---|
| Required account | `benoats@googlemail.com` (Ben proof: 10,050 Flow credits) |
| Mini profile | `~/.playwright-hos-flow-profile` |
| Signed-in now | **`benoats86@gmail.com`** |
| Credits on that account | **0 Google Flow credits** |
| Mint | **not started** |
| Ken Burns | not used |
| P01 / P02 | untouched |

Evidence:

- `logs/flow_auth_probe_resume_20260906.json`
- Aria: `Google Account: Benjamin Oats (benoats86@gmail.com)`
- Credits chip: `0 Google Flow credits` · `Credits refresh daily` · Upgrade

**Hard stop.** Ben must sign Mini Flow as `benoats@googlemail.com` himself (never paste passwords), then re-issue GO.

## When Mini shows benoats@googlemail.com + credits

1. Confirm account chip + credits
2. `_mint_part03_flow_v01.py` (12 × Veo 3.1 Fast only)
3. QA gate → `_assemble_part03_rough_v01.py` → print path + bytes + sha256 + duration
4. Hand to HOS UAT. Do not ping Ben.

## Do not

- Remint Part 01 / 02
- Ship Ken Burns / still-push / freeze-pad
- Use Omni Flash instead of Veo Fast
- Mint as `benoats86@gmail.com`
- Paste passwords / switch accounts for Ben
- Start Part 04
