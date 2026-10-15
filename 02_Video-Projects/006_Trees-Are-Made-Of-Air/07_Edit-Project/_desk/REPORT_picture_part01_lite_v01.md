**006 picture: Part 01 is minted (12 of 12 KEEP) and the Flow Lite test fails (0 of 2).** I recommend we don't make Lite the route for no-face Fast plates. Task: desk comment 5951520953. Grok, 2 Oct 2026.

## 1. Flow Lite [Lower Priority] vs Vertex Fast (same start frame, same scene)

| Plate | Flow Lite (0 credits, 720p) | Vertex Fast control ($0.80, 1080p) |
|---|---|---|
| P2 `06_garden_years` | **FAIL**, hard fail 1. The pot and the seasons hold, but the willow turns into a generic broadleaf tree from autumn on and never comes back as a willow. The flagstone path drifts to lawn. | **FAIL**, hard fail 1. The seasons read well, but the pot vanishes at about 4.8 s. |
| P5 `18_forest_sea` | **FAIL**, hard fails 2 and 8. By about 5 s the camera has left the forest for open sea, so "forest and sea" is lost, and the oxygen bubbles become giant soap bubbles floating in the air. | **KEEP**. The slow aerial drift holds forest and sea, with small bubbles over algae beds. |

**Verdict: Lite does not hold up.**
- Its finish looks like Fast, but it lost the hero prop on one plate and the idea on the other. Vertex kept 1 of 2.
- Lite also downloads at 720p, and twice the scripted submit stalled until the prompt was re-set by hand.
- It cost 0 credits, as advertised (62 before, 62 after both takes; screenshots in `07_Edit-Project/_evidence/`).
- With only two samples, I'd keep no-face Fast plates on Vertex Fast and use Lite only for throwaway pre-viz. Your call.

**Tool bug found and fixed (`04_Audio/tools/orbit_flow_veo_ui.py`).** `attach_image_to_prompt` re-locked "Veo 3.1 - Quality" during the start-frame step, whatever model was requested.
- The first forest Lite run was switched to Quality this way and Flow refused it for lack of credits, so nothing was spent.
- Any earlier Flow "Fast" start-frame mint made by this tool may have been billed as Quality.
- The fix passes the requested model through. Lower Priority is also matched exactly, and the selected label is checked after picking.
- Proof: `09_vilvoorde` on Flow Fast cost exactly 10 credits (62 → 52).

## 2. Part 01 on Vertex: 12 of 12 KEEP

I followed 005's process: `01_willow_air` alone to its first KEEP, then batches. The Explorer appears in no Part 01 row, so he stays out of the first minute.

| Plate | Engine | Kept take | Res | Clip / board use | Freeze ≥0.5 s | sha256 (16) |
|---|---|---|---|---|---|---|
| 01_willow_air | Vertex Quality | t1 (still v02) | 1920x1080 | 8 / 4.28 s | 0 | 19b78371f472bef6 |
| 02_balance_trunk | Vertex Fast | t1 | 1920x1080 | 4 / 3.08 s | 0 | 41e811d22fe80080 |
| 03_pot_jar_leaf | Vertex Fast | t1 | 1920x1080 | 8 / 7.5 s | 0 | b1aaba6dbb366593 |
| 04_years_pass | Vertex Fast | t3 | 1920x1080 | 6 / 5.48 s | 0 | 778765c8a0b23e52 |
| 05_olive_grove | Vertex Fast | t1 | 1920x1080 | 6 / 4.2 s | 0 | c7bd73390291ee77 |
| 06_aristotle | Vertex Quality | t1 | 1920x1080 | 8 / 6.24 s | 0 | ad1aae4cecd1a6e3 |
| 07_roots_mouths | Vertex Fast | t1 (still v03) | 1920x1080 | 6 / 4.74 s | 0 | d1690730c0975b97 |
| 08_wood_food_air | Vertex Fast | t3 (still v02) | 1920x1080 | 6 / 4.22 s | 0 | 8af6d144ce9741bf |
| 09_vilvoorde | **Flow Fast** (boarded route, 10 credits) | t1 | **1280x720** | 8 / 5.0 s | 0 | a8353fba020c7126 |
| 10_van_helmont_sack | Vertex Quality | t1 | 1920x1080 | 8 / 6.44 s | 0 | 092c9919758ca77e |
| 11_shoot_in_pot | Vertex Fast | t1 | 1920x1080 | 6 / 4.8 s | 0 | 6e1066306155bdb4 |
| 12_garden_sky | Vertex Fast | t2 | 1920x1080 | 8 / 5.67 s | 0 | 1713f3c33e3482f0 |

**Failed takes and why:**
- `04` t1 froze for the first 0.54 s; t2 had snow falling inside the room.
- `08` t1 was LOST: the local process died before an operation name came back. I've counted its $0.60 as spent. t2 had a campfire flame on a Fast plate.
- `12` t1 had clouds at pot height that read as smoke.

**Watch points for assembly:**
- `11_shoot_in_pot`: a hand deforms after 5.0 s, and the board uses 4.8 s, so cut at or before 4.8 s.
- `09_vilvoorde` is 720p, from the Flow download. **Question:** accept an upscale for a 5 s establishing push, or remint it on Vertex Fast for about $0.80?

**Start frames:**
- All 16 Part 01 stills came from Vertex `gemini-2.5-flash-image` at $0.039 each, by-eye checked against the Part 01 style refs. Nano Banana 2 in Flow wasn't needed.
- Remakes: willow v02 (v01 was photoreal), 07 v03 (v01 creepy, v02 had eyes), 08 v02 (v01 showed breath like smoke in a warm room).

UAT method: a 24-frame dense tile across each clip, frames at 1280 px at start, middle and end, `freezedetect` at 0.5 s, and ffprobe. This is a frame read, not literal continuous playback; Ben's moving-picture sign-off is still the real watch.

UAT output, pasted:

```
| 01_willow_air_t1 | 1920x1080 | 8.00 s | audio=0 | freeze>0.5s=0 |
| 02_balance_trunk_t1 | 1920x1080 | 4.00 s | audio=0 | freeze>0.5s=0 |
| 03_pot_jar_leaf_t1 | 1920x1080 | 8.00 s | audio=0 | freeze>0.5s=0 |
| 04_years_pass_t3 | 1920x1080 | 6.00 s | audio=0 | freeze>0.5s=0 |
| 05_olive_grove_t1 | 1920x1080 | 6.00 s | audio=0 | freeze>0.5s=0 |
| 06_aristotle_t1 | 1920x1080 | 8.00 s | audio=0 | freeze>0.5s=0 |
| 07_roots_mouths_t1 | 1920x1080 | 6.00 s | audio=0 | freeze>0.5s=0 |
| 08_wood_food_air_t3 | 1920x1080 | 6.00 s | audio=0 | freeze>0.5s=0 |
| 09_vilvoorde_flowfast_t1 | 1280x720 | 8.00 s | audio=0 | freeze>0.5s=0 |
| 10_van_helmont_sack_t1 | 1920x1080 | 8.00 s | audio=0 | freeze>0.5s=0 |
| 11_shoot_in_pot_t1 | 1920x1080 | 6.00 s | audio=0 | freeze>0.5s=0 |
| 12_garden_sky_t2 | 1920x1080 | 8.00 s | audio=0 | freeze>0.5s=0 |
| 06_garden_years_t1 | 1920x1080 | 8.00 s | audio=0 | freeze>0.5s=0 |
| 06_garden_years_lite_t1 | 1280x720 | 8.00 s | audio=0 | freeze>0.5s=0 |
| 18_forest_sea_t1 | 1920x1080 | 8.00 s | audio=0 | freeze>0.5s=0 |
| 18_forest_sea_lite_t1 | 1280x720 | 8.00 s | audio=0 | freeze>0.5s=0 |
```

## 3. Credit

- **Vertex spend:** Part 01 is $13.62 (16 takes and 16 stills, including the lost $0.60). The Lite controls are $1.68. The film total is **$15.30**.
- **Console reading after Part 01: Free Trial £63.29, Available** (`_evidence/vertex_credits_after_part01_006_2026-10-02.png`). It was £65.73 before the boards.
  - Billing lags, so most of today's spend hasn't posted yet.
  - The projection is **£53.49** at the planning rate of £0.80 per dollar, nearer £54.4 at 005's real rate.
  - Either figure is far above the £0 floor, and paid billing was never touched.
- **Flow:** 62 → 52 credits. Lite cost 0; `09_vilvoorde` on Fast cost 10.

## 4. Records (no media in git)

- Logs:
  - `07_Edit-Project/PART01_MINT_LOG_v01.json`
  - `PART02_MINT_LOG_v01.json` (garden control)
  - `PART05_MINT_LOG_v01.json` (forest control)
  - `LITE_TEST_v01.json`
  - `FLOW_FAST_v01.json`
  - `VERTEX_CREDIT_LOG_v01.json`
- Scripts: `_mint_vertex_v01.py` and `_flow_lite_test_v01.py` (Lite, plus a `--fast` mode for boarded Flow rows).
- Every log entry has the path and full sha256 of its clip and start frame.

**Next, on your OK:** Part 02 on Vertex (22 rows), the same way. Flow is not the route except where the board names it. I also need your answer on the `09_vilvoorde` 720p question.

Images: the Lite-versus-Vertex dense sheets, and the 12 Part 01 keeps at 3 s.
