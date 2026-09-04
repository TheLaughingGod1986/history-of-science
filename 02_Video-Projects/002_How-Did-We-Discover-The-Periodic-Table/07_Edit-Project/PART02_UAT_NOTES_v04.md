# Part 02 UAT notes — v04 (4 Sep 2026)

## Ben FAIL on v03 (confirmed)
1. Pots/jars still on fire
2. Rest of scenery looks unfinished (local Pillow desks)

## Root causes
- v03 scenery was unfinished local Pillow Ken Burns desks (not finished Flow).
- Flow T2V ignores “no jars / no fire” and invents alchemy shelves with vessel flames.
- Attaching a start frame flipped Create onto **Nano Banana (Image)**; early remints were stills/wrong mode until Video/Veo re-lock.

## Fixes landed
- Prompt-pill **Video + Veo 3.1 Fast** lock after attach; **refuse Create** if still on Nano Banana.
- Do not auto-attach unfinished Pillow stills.
- Working path: **Flow Image still** (jar-free writing study, candle OK) → **Veo I2V** with Video re-lock.

## Evidence so far
- Finished jar-free Flow stills for plates 02–11 under `04_Generated-Clips/part02/refs/v04_flow_stills/` (Image mode; ~0 AI credit).
- Plate `02_lavoisier_list` Veo I2V harvested (`…/raw/v01_fast/02_lavoisier_list_v01.mp4`, ~6.9MB):
  - Finished look (not Pillow flat)
  - No vessel fire (candle only)
  - Mid-clip Veo still drifts jars into frame — reject if jars must stay zero; acceptable vs flaming pots pending Ben call

## Blocker
- AI credits ≈ **8** left (each Veo Fast I2V ≈ **10**). Need ~80 more to I2V remaining scenery plates.
- Stopped before burning the last credits on a doomed remint.

## Next (when credits topped up)
1. QA/replace weak stills (`06`, `09` look thin).
2. I2V remint scenery 03,05–11 from Flow stills with Video re-lock.
3. Keep `01_chapter_card` + local `04_triad_cards`.
4. Assemble `hos_002_part02_rough_v04.mp4` → iCloud `HOS UAT/` + `WATCH_part02_v04.txt`.
5. **STOP for Ben UAT — no Part 03.**
