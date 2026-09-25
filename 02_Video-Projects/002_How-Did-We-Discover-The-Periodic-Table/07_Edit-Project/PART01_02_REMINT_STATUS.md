# Parts 01+02 motion remint status — 5 Sep 2026

## Part 01 — landed for CoS watch

- Cut: `hos_002_part01_rough_v12.mp4` in **HOS UAT**
- Watch pointer: `WATCH_part01_v12.txt` / `ZZ_OPEN_PART01_V12.txt`
- vs v11: Animistry **side labels** (upper-right) when VO names terms; picture from existing real Veo plates (motion-scored — not Ken Burns still-push assemble).
- Plate 10 HOLD: ore IN brass pan + shimmer present. Spot QA still shows some **clear glass on background shelves** — Flow remint attempted; blocked by daily Veo Fast quota.

## Part 02 — blocked (cannot ship Ken Burns)

- Prior v06 = Ken Burns from stills. Must remint to real Veo.
- Mint script ready: `_mint_part02_flow_remint_v07.py`

## Engine blockers (report to CoS — do not ping Ben)

1. **Gemini API prepaid dry** — `429 RESOURCE_EXHAUSTED` / prepayment depleted.
2. **Flow Veo 3.1 Fast daily quota reached** (account `benoats86@gmail.com`) — UI: *"your account has reached its daily quota for the Veo 3.1 - Fast model"*. Create fails; not charged. Agent also suggests Omni Flash (forbidden for HOS CG).
3. Flow Agent Create path still flaky (navigation / Failed to render) when quota allows.

## Resume when

- Flow Veo Fast quota resets **or** Gemini prepaid topped up **or** CoS points to another Ultra login with Veo Fast headroom.
- Then: remint Part 01 plate 10 (opaque shelves) if CoS FAILs shelf glass → rebuild v12.1; mint all Part 02 scenery to `raw/v07_fast` → assemble v07 with side labels → HOS UAT.
