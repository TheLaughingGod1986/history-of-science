# Part 03 status — A Ruler for Atoms

**Updated:** 6 Sep 2026 22:10 Europe/London (HOS Local Mini · Ben GO attempt)

## Ben GO (locks)

| Cut | Status |
|---|---|
| `hos_002_part01_rough_v14.mp4` | **LOCKED PASS.** Do **not** remint / overwrite. |
| `hos_002_part02_rough_v06.mp4` | **LOCKED.** Do **not** remint / overwrite. |
| Part 03 | **Mint attempted → BLOCKED (credits)** |
| Part 04 | Do **not** start |

## Target rough (not landed)

`/Users/benjaminoats/YouTube/History Of Science/02_Video-Projects/002_How-Did-We-Discover-The-Periodic-Table/09_Final-Export/hos_002_part03_rough_v01.mp4`

## Ready on disk (inputs)

- Board: `07_Edit-Project/parts/part-03_plates_v01.json` (12 plates; Explorer once on `05_explorer_ruler`)
- VO: `02_Voiceover/part03_ruler_for_atoms_v01.wav` + align
- Music bed: `05_Music/hos_002_part01_curious_workshop_v02_norm.wav`
- Mint: `_mint_part03_flow_v01.py` (prefer Flow Veo 3.1 Fast) · `_mint_part03_gemini_v01.py`
- Assemble: `_assemble_part03_rough_v01.py` (Animistry upper-right side labels)

## BLOCKED — credits dry (do not ship fake motion)

Hard rule obeyed: **STOP**. No Ken Burns / still-push / freeze-pad rough.

### Gemini API (prepaid)

Live probe 6 Sep 22:00:

`429 RESOURCE_EXHAUSTED` — *Your prepayment credits are depleted* (AI Studio prepay).

Prior full mint log (`logs/mint_part03_gemini_v01_full.log`): `ok=0` across all plates on same 429.

### Flow UI (benoats86@gmail.com / Ultra session)

Smoke 6 Sep 21:57 → `logs/mint_part03_flow_smoke_plate01_20260906_215711.log`:

1. Logged in; Create project opened; model locked **Veo 3.1 - Fast** via Agent settings.
2. Create submitted (scenery T2V plate `01_hall_open_side_label`).
3. Immediate fail — page text:

   > You're out of Google Flow credits. You can wait until they refresh or upgrade…

   > I wasn't able to start that generation because your account has reached its current credit limit.

4. Stall PNG: `04_Generated-Clips/part03/raw/v01_fast/01_hall_open_side_label_v01_flow_stall.png`
5. **Zero** usable landscape Veo mp4 written under `raw/v01_fast/` (only stall PNG).
6. Browser later drifted to Facebook cookie interstitial after fail (secondary noise; root cause = Flow credits).

## When credits recover

1. Flow Veo 3.1 Fast via `_mint_part03_flow_v01.py` (or Gemini Fast if prepaid refilled).
2. QA every plate: landscape 16:9 · continuous real motion · no Threads/portrait CDN · Explorer once on plate 05 on-model.
3. Assemble → `hos_002_part03_rough_v01.mp4` → HOS UAT. Print path + bytes + sha256 + duration.
4. **Do not** ping Ben. Parent hands to HOS UAT.

## Do not

- Remint Part 01 v14 or Part 02 v06
- Ship Ken Burns / freeze-pad as Part 03
- Start Part 04
- Ping Ben
