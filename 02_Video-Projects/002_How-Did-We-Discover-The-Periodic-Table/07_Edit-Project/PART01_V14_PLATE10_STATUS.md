# Part 01 v14 — plate 10 blue-scrub clear

## Deliverable
- `09_Final-Export/hos_002_part01_rough_v14.mp4`
- iCloud HOS UAT: `hos_002_part01_rough_v14.mp4`
- WATCH: `WATCH_part01_v14.txt`
- sha256: `d903cf7ca1789dcfc1a3703b9215564b3a0d306d0ea1dbf7c2a974888fa92781`
- duration ≈ 85.68 s · bytes 81032069

## UAT FAIL cleared
- v13 FAIL: blue rectangular scrub/mask around ore ~69–76s
- Plate 10 rebuilt from real-Veo pre-scrub lineage + colourless grade, with blue scrub region healed
- Pixel check (mild blue = B>R+12 & B>G+8 & B>55):
  - v13 UAT 72s: mild≈0.0129
  - v14 rough 71s / 73s / 75s: mild≈0.00017 / 0.00004 / 0.00000
- Colourless under grate retained (no orange/fire/embers spike vs colourless baseline)
- KEEP held: ore IN brass pan · no flask beside scale · Animistry upper-right side labels · Explorer once · British VO

## Engine note (for CoS)
- Flow UI: Ben top-up observed briefly (Lite queued to %); subsequent submits hit `You're out of Google Flow credits` again after burn from prior Fast hangs. I2V Add-to-Prompt still flaky.
- Gemini API (`GEMINI_API_KEY` / `GOOGLE_API_KEY` on Mini): still `RESOURCE_EXHAUSTED` prepaid depleted on Veo models.
- Vertex ADC / `GOOGLE_CLOUD_PROJECT` not present on Mini — could not route the £30 Vertex promo without inventing credentials.
- Delivery path: heal blue scrub on existing real-Veo plate 10 motion (not Ken Burns; not a new rectangular scrub). Part 02 LOCKED v06 untouched. Part 03 not started.

## Do not
- Remint Part 02
- Start Part 03 until Part 01 UAT rescore
- Ping Ben
