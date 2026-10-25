# HOS 006 — Master v06 Desk Report (`J0924` — Gemini covering)

- **Film:** `006_Trees-Are-Made-Of-Air` (*The Willow Tree That Was Made of Air*)
- **Stage:** `edit` (`master_v06`)
- **Authority:** Chief ruling (`#180` `6384888711`, Grok, 24 Oct 14:38 London) on Ben's change tick (`#180` `6375549934`, Fri 23 Oct 22:57 London).
- **Master MP4:** `/Users/benjaminoats/YouTube/History Of Science/02_Video-Projects/006_Trees-Are-Made-Of-Air/07_Edit-Project/master_v06/hos_006_master_v06.mp4` (`531.833 s`, `12,764` frames @ 24 fps, `1920×1080` H.264 + AAC 48 kHz stereo at `-14.0 LUFS` / `-1.4 dBTP`, sha256 `36c54e684b8a947c65298231268f9f031899df5a0d72ec38506f5e17b3d215ef`, video stream sha256 `30619688edb8d23d6cf32179b9ea1bc4b61074e0849821933eb1fc895a6f903e`)
- **Phone MP4 (`<120 MB`):** `/Users/benjaminoats/YouTube/History Of Science/02_Video-Projects/006_Trees-Are-Made-Of-Air/07_Edit-Project/master_v06/hos_006_master_v06_PHONE.mp4` (`109.83 MB`, `115,162,637` B, sha256 `9b3dde01a243eee0118ebba96f4bd387070c81208beb7ee3ea224e18d237b887`)
- **Check sheet (12 full-size 1920×1080 frames inspected):** `/Users/benjaminoats/YouTube/History Of Science/02_Video-Projects/006_Trees-Are-Made-Of-Air/07_Edit-Project/master_v06/hos_006_master_v06_ben_check_sheet.jpg` (`sha256: 3bf61b39d1d2a9e857d89451c1fe0d9876c57bbe3cf7effe46a2a05167ec8eb0`)
- **All-cards in-points proof sheet (`sf-1, sf, sf+1, ef-1, ef` across all 28 overlays):** `/Users/benjaminoats/YouTube/History Of Science/02_Video-Projects/006_Trees-Are-Made-Of-Air/07_Edit-Project/master_v06/hos_006_master_v06_card_inpoints_sheet.jpg` (`sha256: 2442e2047023582cb72e5b6e605e96c55383234c42e61954d63a5ff662878f16`)
- **Contact sheet:** `/Users/benjaminoats/YouTube/History Of Science/02_Video-Projects/006_Trees-Are-Made-Of-Air/07_Edit-Project/master_v06/hos_006_master_v06_contact_sheet.jpg` (`sha256: b79e5cef23746511c55d54a97dbb10de0659cd54fd06fb47896b7ac11e974299`)
- **iCloud HOS UAT copies:**
  - `/Users/benjaminoats/Library/Mobile Documents/com~apple~CloudDocs/HOS UAT/006_Trees_master_v06.mp4`
  - `/Users/benjaminoats/Library/Mobile Documents/com~apple~CloudDocs/HOS UAT/006_Trees_master_v06_PHONE.mp4`
  - `/Users/benjaminoats/Library/Mobile Documents/com~apple~CloudDocs/HOS UAT/006_Trees-Are-Made-Of-Air/hos_006_master_v06.mp4`
  - `/Users/benjaminoats/Library/Mobile Documents/com~apple~CloudDocs/HOS UAT/006_Trees-Are-Made-Of-Air/hos_006_master_v06_PHONE.mp4`
  - `/Users/benjaminoats/Library/Mobile Documents/com~apple~CloudDocs/HOS UAT/006_Trees-Are-Made-Of-Air/hos_006_master_v06_ben_check_sheet.jpg`
  - `/Users/benjaminoats/Library/Mobile Documents/com~apple~CloudDocs/HOS UAT/006_Trees-Are-Made-Of-Air/hos_006_master_v06_card_inpoints_sheet.jpg`
  - `/Users/benjaminoats/Library/Mobile Documents/com~apple~CloudDocs/HOS UAT/006_Trees-Are-Made-Of-Air/hos_006_master_v06_contact_sheet.jpg`
- **Spend:** `£0.00` cash, **`0` Flow credits**.

---

## Root-Cause Fixes & Frame-by-Frame Verification (`hos_006_master_v06_card_inpoints_sheet.jpg` & `hos_006_master_v06_ben_check_sheet.jpg`)

1. **Changes #1 (`1:03`, `#13 ch_five_years`, `sf=1480`) & #3 (`4:30`, `#52 ch_bubbles`, `sf=6564`) + All 28 Card In-Points Checked Frame-by-Frame:**
   - **Root cause in `v04`/`v05`:** The base concat join had slight container timebase rounding drift while overlays were shifted via floating-point seconds (`setpts=PTS-STARTPTS+{start_s:.6f}/TB` without normalizing `[0:v]` to `N/(24*TB)`). As a result, when `enable='between(n,sf,ef-1)'` opened on exact frame `n=sf`, ffmpeg's `overlay` filter saw the overlay stream's first frame PTS slightly after the base frame's PTS and passed the uncovered underlying cut frame `n=sf` through for 1 frame before compositing the card on `n=sf+1`.
   - **Fix in `master_v06` (`_build_master_v06.py`):** Locked both the base stream (`[0:v]fps=24,setpts=N/(24*TB),format=yuv420p`) and all 28 overlay streams (`[k:v]fps=24,setpts=(N+{sf})/(24*TB),format=yuv420p`) to exact integer frame numbers, and re-composited all 28 overlays (also restoring Part 5 overlays `#22..#27`: `ch_carbon`, `when_geneva_1782`, `timeline_d5`, `who_senebier`, `who_saussure`, `timeline_d6`).
   - **Frame-by-frame verification across every full-screen card in `hos_006_master_v06.mp4` (`hos_006_master_v06_card_inpoints_sheet.jpg`):**
     - `timeline_d1` (`0:39.75`, `#09`, `sf=954`): `f=953` = `#08` Explorer horizon; `f=954 [IN]` = parchment timeline card (diff `954->955 = 0.0`, **0-frame leak**).
     - `ch_five_years` (`1:01.67` / Ben `1:03`, `#13`, `sf=1480`): `f=1479` = `#12` willow pot; `f=1480 [IN]` = chapter card 100% cover (diff `1480->1481 = 0.0`, **0-frame furnace leak**); `f=1498` = *Five Years and Two Ounces* full title; `f=1518` = `#13` furnace soil.
     - `ch_mint` (`2:58.67`, `#34`, `sf=4288`): `f=4287` = `#33` willow; `f=4288 [IN]` = chapter card 100% cover (diff `4288->4289 = 0.0`, **0-frame sapling leak**); `f=4306` = *The Air That Mint Repaired* full title.
     - `timeline_d2` (`3:03.71`, `#35`, `sf=4409`): `f=4408` = `#34` sapling; `f=4409 [IN]` = parchment timeline card (diff `4409->4410 = 0.0`, **0-frame Hales leak**); `f=4486` = clean handoff to `who_hales` (`Stephen Hales`).
     - `timeline_d3` (`3:25.79`, `#39`, `sf=4939`): `f=4938` = `#38` book; `f=4939 [IN]` = parchment timeline card (diff `4939->4940 = 0.0`, **0-frame Leeds leak**).
     - `ch_bubbles` (`4:33.50` / Ben `4:30`, `#52`, `sf=6564`): `f=6563` = `#51` dark room; `f=6564 [IN]` = chapter card 100% cover (diff `6564->6565 = 0.0`, **0-frame villa leak**); `f=6582` = *Bubbles in the Sunlight* full title.
     - `timeline_d4` (`4:36.29`, `#52`, `sf=6631`): `f=6630` = `#52` villa; `f=6631 [IN]` = parchment timeline card (diff `6631->6632 = 0.0`, **0-frame leak**).
     - `ch_carbon` (`6:05.42`, `#68`, `sf=8770`): `f=8769` = `#67` leaf bubbles; `f=8770 [IN]` = chapter card 100% cover (diff `8770->8771 = 0.0`, **0-frame lake leak**); `f=8788` = *Carbon From the Sky* full title; `f=8808` = clean handoff to `when_geneva_1782` (`Geneva, 1782`).
     - `timeline_d5` (`6:09.92`, `#69`, `sf=8878`): `f=8877` = `#68` Geneva lake; `f=8878 [IN]` = parchment timeline card (diff `8878->8879 = 0.0`, **0-frame leak**).
     - `timeline_d6` (`6:20.21`, `#70`, `sf=9125`): `f=9124` = `#70` Saussure; `f=9125 [IN]` = parchment timeline card (diff `9125->9126 = 0.0`, **0-frame leak**).
     - All 18 lower-third / closing cards (`who_aristotle`, `who_helmont`, `wt_5lb`, `num_169`, `fact_leaves`, `wt_2oz`, `wt_164lb`, `wt_62lb`, `wt_1lb`, `fact_gas`, `who_hales`, `who_priestley`, `who_ingenhousz`, `num_500`, `when_geneva_1782`, `who_senebier`, `who_saussure`, `closing_next_film`) also start and end on their exact target frames with zero plate discontinuity (`hos_006_master_v06_card_inpoints_sheet.jpg`).

2. **Change #2 (`4:02`, `#45 P3 12_mouse_mint`, `3:59.50–4:07.38`, `sf=5748..5937`, frames `04_01_50_mouse_mint_f5796.png` & `04_03_50_mouse_mint_f5844.png`):**
   - **Root cause in `v05`:** In `12_mouse_mint_t1.mp4`, the bottom tip of the mint sprig's stem ended in mid-air inside the lower third of the bell jar (`y ≈ 880..930` as the camera pushed out), reading as a floating twig.
   - **Fix in `master_v06` (`clips/12_mouse_mint_v06.mp4`, `£0 / 0 credits`):** Applied a smooth 1.38× bottom-anchored crop (`upscale: 1.38 <= 2.35x` limit) that tracks the mint stem base so the green mint stem extends cleanly down through the bottom frame border (`y=1080`) on every single frame (`f=5748..5936`), while keeping the mouse and leafy mint sprig well-framed inside the glass bell jar.

---

## Machine Checks (Pasted Outputs)

```text
SFX level PASS: VO -16.1 LUFS, SFX -34.0 LUFS, 31 hits
music gate PASS: trees006_score_bed_v01.mp3, 531.8 s, about 66.7 BPM, brief Pace: 60-72 BPM
WARN   2:18 row 15_desk_candle 15_desk_candle_t1_above_desk_v03.mp4: low detail: edge density 0.0269 < film p5 0.0270
WARN   3:01 row 01_soil_to_sky 01_soil_to_sky_t1.mp4: low detail: edge density 0.0219 < film p5 0.0270
WARN   5:24 row 09_bubbles_again 05_bubbles_macro_t1_from4.500.mp4: low detail: edge density 0.0244 < film p5 0.0270
WARN   6:32 row 05_sums_add_up 05_sums_add_up_t1.mp4: low detail: edge density 0.0246 < film p5 0.0270
WARN   8:17 row 23_carbon_atom 23_carbon_atom_t1.mp4: low detail: edge density 0.0237 < film p5 0.0270
picture QA PASS: 0 of 96 cuts fail, 5 to look at -> /Users/benjaminoats/YouTube/History Of Science/02_Video-Projects/006_Trees-Are-Made-Of-Air/07_Edit-Project/master_v06/PICTURE_QA.md, /Users/benjaminoats/YouTube/History Of Science/02_Video-Projects/006_Trees-Are-Made-Of-Air/07_Edit-Project/master_v06/picture_qa_review.jpg
polish gate PASS: 0 of 96 rows failed, 5 to look at -> /Users/benjaminoats/YouTube/History Of Science/02_Video-Projects/006_Trees-Are-Made-Of-Air/07_Edit-Project/master_v06/polish_gate.json
**Decision:** PASS — VO / Gemini Veo allowed
Script score: **93.7/100** · PASS
Integrated loudness: I: -14.0 LUFS, LRA: 3.3 LU, True peak: -1.4 dBFS
Built hos_006_master_v06_PHONE.mp4: 109.83 MB (< 120 MB)
```
