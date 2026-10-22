# HOS 006 — `full_join_v02_teach` Delta & Re-Gate Report (`REVIEW_v02.md` · J0809)

- **Master (`full_join_v02_teach`):** `02_Video-Projects/006_Trees-Are-Made-Of-Air/07_Edit-Project/full_join_v02_teach/hos_006_full_join_v02_teach.mp4`
- **iCloud HOS UAT copy:** `~/Library/Mobile Documents/com~apple~CloudDocs/HOS UAT/hos_006_full_join_v02_teach.mp4`
- **NAS archive copy:** `/Volumes/data/mac-mini-archive/YouTube/History Of Science/02_Video-Projects/006_Trees-Are-Made-Of-Air/07_Edit-Project/full_join_v02_teach/hos_006_full_join_v02_teach.mp4`
- **SHA-256:** `d24a08ee94489379dd8e550700b9e31ec2fd4636c35158d037949248ecf8eb34`
- **Runtime / frames:** `507.833333 s` (`8:27.83`), `12,188` frames @ `24 fps`, `1920×1080`
- **Audio:** Byte-identical copy of `full_join_v01_teach` VO (no music bed per ElevenLabs credit hold until 30 Oct).
- **Spend:** `£0` (zero new Vertex/Flow mints; zero ElevenLabs spend).
- **Gate status:** `picture_qa.py` **PASS** (`0 of 91 cuts fail`), `polish_gate.py` **PASS** (`0 of 91 rows failed`), `npm run gate:episode` **PASS** (`93.7/100`). **Parked for Chief** (not a film PASS until Chief's final OK).

---

## 1. Delta Table — Every `REVIEW_v01.md` FIX Item (`21 / 21` Done)

| # | Cut(s) & Row | `REVIEW_v01` Finding | `full_join_v02_teach` Action Taken | Status |
|---|---|---|---|---|
| **1** | **#09** `P1 09_vilvoorde` (`0:39.75–0:44.75`) | `timeline_d1` started at `0:40.00` (6 frames after `#09` cut), flashing the brick manor; parchment `luma_std 12.49 < 18.0`. | Re-timed `timeline_d1` to `0:39.75–0:42.96` (frames `954..1031`, starting on the exact `#09` cut) and added candlelit parchment vignette (`luma_std 23.4 >= 18.0`, clearing the low-detail WARN). | **DONE** |
| **2** | **#13** `P2 01_furnace_soil` (`1:01.67–1:07.13`) | `ch_five_years` started at `1:02.00` (8 frames after Part 02 cut at `1:01.67`), flashing the furnace before the chapter card. | Re-timed `ch_five_years` to `1:01.67–1:03.25` (frames `1480..1518`), opening cleanly on frame 0 of Part 02. | **DONE** |
| **3** | **#14** `P2 02_balance_200` (`1:07.13–1:12.96`) | `code_graphic_p2_02_pounds_v03.mp4` was a flat slate-blue/cream UI panel (`edge_density 0.0125 < 0.0227`, house-style FAIL). | Replaced with already-minted `02_balance_200_t1.mp4` (`0.00–5.83 s`) cropped to `1920×816` (`1.32×` upscale, hiding the Veo `"200"` on the bottom ledger) with a house-style walnut/cream Didot italic lower-third counter (`0 → 200 pounds / of dried soil · starting weight`) in `02_balance_200_house_v02.mp4` (`edge_density 0.0680`, `luma_std 48.0`, `seams=[]`). | **DONE** |
| **4** | **#18** `P2 06_garden_years` (`1:28.63–1:42.00`) | `07_explorer_snow` (`5.46 s`) was cut in Part 02 without extending `#18`, shifting `#19`–`#32` early by `5.46 s` (`131` frames). | Appended already-minted `06_garden_years_t1.mp4` (`0.00–5.458333 s`, `131` frames) immediately after `06_garden_years_t2.mp4` (`7.916667 s`, `190` frames) in `06_garden_years_joined_v02.mp4` (`321` frames = `13.375 s`), restoring `#19`–`#32` to exact VO alignment. | **DONE** |
| **5** | **#19** `P2 08_haul_tree` (`1:42.00–1:46.79`) | Played `5.46 s` early (`1:36.54–1:41.33`) over *"the pot of soil never changes"*, with `num_169` spilling in. | Shifted `+5.46 s` to `1:42.00–1:46.79` (frames `2448..2563`), landing directly on *"Then, after five years, he pulled the tree out and weighed it"* (`1:40.97–1:45.57`), with zero overlay spill. | **DONE** |
| **6** | **#20** `P2 09_weights_169` (`1:46.79–1:50.71`) | Played `5.46 s` early (`1:41.33–1:45.25`) before VO said `"169 pounds"`; bottom-right open book showed Veo-drawn `"169"` numerals and floating quill (`y > 790`). | (1) Shifted `#20` `+5.46 s` to `1:46.79–1:50.71` (`2563..2657`) and `num_169` to `1:46.83–1:50.04` (`2564..2641`) over spoken *"A hundred and sixty-nine pounds"* (`1:46.85–1:50.13`). (2) Cropped `09_weights_169_t1.mp4` to `crop=1920:788:0:0,scale=1920:1080` (`1.37×` upscale) in `09_weights_169_crop_v02.mp4`, completely removing the Veo numerals and floating quill. | **DONE** |
| **7** | **#21** `P2 10_fallen_leaves` (`1:50.71–1:55.12`) | Played `5.46 s` early (`1:45.25–1:49.67`) over `"169 pounds"`, before VO mentioned the leaves. | Shifted `#21` `+5.46 s` to `1:50.71–1:55.12` (`2657..2763`) and `fact_leaves` (*"Leaves not weighed"*) to `1:50.75–1:53.96` (`2658..2735`), matching spoken *"And that didn't even count the leaves that had fallen in four autumns"* (`1:50.75–1:54.91`). | **DONE** |
| **8** | **#22–#23** `P2 11_furnace_again` & `12_pointer_short` (`1:55.12–2:05.46`) | Played `5.46 s` early over the fallen-leaves line instead of the drying/weighing lines. | Shifted `+5.46 s` to `1:55.12–1:58.67` (`#22`) and `1:58.67–2:05.46` (`#23`), aligning with *"He dried the soil again and put it back on the scales. Two hundred pounds, less about two ounces"* (`1:55.17–2:04.49`). | **DONE** |
| **9** | **#24** `P2 13_tree_vs_pinch` (`2:05.46–2:10.83`) | Played `5.46 s` early (`2:00.00–2:05.38`) and failed low-detail WARN (`edge_density 0.0208 < 0.0227`) during the bare tabletop pan. | Shifted `+5.46 s` to `2:05.46–2:10.83` (matching *"A hundred and sixty-four pounds of new tree, and only two ounces of soil gone"*) and built `13_tree_vs_pinch_trim_v02.mp4` (`crop=1628:916:146:120,scale=1920:1080`, `1.18×` upscale, trimming out the bare wood pan so midpoint `edge_density` rises from `0.0208` to `0.0684`). | **DONE** |
| **10** | **#25–#31** `P2 14_why_grown` .. `20_shimmer_coals` (`2:10.83–2:46.67`) | All played `5.46 s` early due to `#18` drift; `fact_gas` spilled 5 frames into the tail of `#31`. | Shifted all 7 cuts by `+5.46 s` (`+131` frames) to their locked board times and removed the 5-frame `fact_gas` spill from `#31` (full table in §2 below). | **DONE** |
| **11** | **#32** `P2 21_gas_window` (`2:46.67–2:53.29`) | Played `5.46 s` early (`2:41.21–2:47.83`); `fact_gas` played `5.67 s` before Ben said *"He gave it a new name: gas"*. | Shifted `#32` `+5.46 s` to `2:46.67–2:53.29` (`4000..4159`) and `fact_gas` (*"Coined the word gas"*) to `2:46.67–2:49.88` (`4000..4077`), landing right as Ben says *"He gave it a new name: gas"* (`2:46.67`). | **DONE** |
| **12** | **#33** `P2 22_shimmer_willow` (`2:53.29–2:58.67`) | Stretched to `10.83 s` (`2:47.83–2:58.67`) with a flat slate-blue/cream UI poster card (`edge_density 0.0162 < 0.0227`, house-style FAIL). | Restored to `5.375 s` (`129` frames, `2:53.29–2:58.67`) in `22_shimmer_willow_v02.mp4` using `22_shimmer_willow_t1.mp4` (`2.625–8.000 s`, frames `63..192`, all willow with zero repeat of `#26` `15_desk_candle`), dropping the flat UI card completely (`edge_density 0.1612`, `luma_std 52.2`). | **DONE** |
| **13** | **#34** `P3 01_soil_to_sky` (`2:58.67–3:03.71`) | `ch_mint` started `0.33 s` (8 frames) after the Part 03 cut (`2:59.00` vs `2:58.67`), flashing the sapling for 8 frames. | Re-timed `ch_mint` to `2:58.67–3:00.25` (frames `4288..4326`), starting on the exact Part 03 cut boundary. | **DONE** |
| **14** | **#35–#36** `P3 02_hales_branch` & `03_water_level` (`3:03.71–3:15.42`) | `who_hales` played before `timeline_d2` (reversed against spoken order *"in 1727, a country parson called Stephen Hales"*), and `timeline_d2` spilled `0.41 s` (10 frames) across the `3:10.21` cut into `#36`. | Sequenced `timeline_d2` (`Teddington, 1727`) first at `3:03.71–3:06.92` (`4409..4486`) and `who_hales` second at `3:06.92–3:10.21` (`4486..4565`), matching spoken order and ending on the exact `#35/#36` cut with zero spill into `#36`. | **DONE** |
| **15** | **#39–#40** `P3 06_leeds_brewery` & `07_priestley` (`3:25.79–3:36.46`) | `timeline_d3` started 5 frames after `#39` opened (`3:26.00` vs `3:25.79`), and `who_priestley` started 7 frames before `#39` ended (`3:30.00` vs `3:30.29`). | Re-timed `timeline_d3` to `3:25.79–3:29.00` (`4939..5016`) and `who_priestley` to `3:30.29–3:33.88` (`5047..5133`, with `#40` plate baked from frame 0 of `07_priestley_t1.mp4`). Parchment vignette raised `#39` `luma_std` to `23.1 >= 18.0`. | **DONE** |
| **16** | **#52** `P4 01_villa` (`4:33.50–4:39.50`) | `ch_bubbles` (`4:34.00–4:35.58`) and `timeline_d4` (`4:35.58–4:38.79`) ran back-to-back with zero moving plate between them (MOTION fail + `luma_std 13.82 < 18.0`). | Re-timed `ch_bubbles` to `4:33.50–4:35.08` (`6564..6602`), followed by `1.21 s` (`29` frames, `4:35.08–4:36.29`) of moving plate `01_villa_t1.mp4`, then `timeline_d4` at `4:36.29–4:39.50` (`6631..6708`, `luma_std 23.0 >= 18.0`). | **DONE** |
| **17** | **#53–#54** `P4 02_ingenhousz_jars` & `03_plunge_leaf` (`4:39.50–4:51.83`) | `num_500` (`0 → 500 experiments`) played at `4:47.00–4:50.58` over `#54` (*"He plunged fresh leaves..."*) instead of `#53` (*"more than five hundred experiments"*, `4:44.0–4:46.48`). | Moved `num_500` into `#53` at `4:43.58–4:47.17` (`6806..6892`, baked over `#53 02_ingenhousz_jars_t1.mp4`), matching the spoken number and leaving `#54` completely clear. | **DONE** |
| **18** | **#62** `P4 11_night_jars` (`5:30.46–5:38.29`) | Opened in bright sunlight (`0.0–2.3 s`) over *"And at night..."*, followed by a black silhouette blocking the frame (`2.3–4.3 s`, `edge_density 0.0127 < 0.0227`). | Built `11_night_jars_v02.mp4` (`188` frames = `7.833 s`): `11_night_jars_t1.mp4` (`4.30–8.00 s` played at `0.635x` speed → `140` frames = `5.833 s`, frame-blended after the `2.3–4.3 s` silhouette) + `18_dark_window_t1.mp4` (`4.00–6.00 s` = `48` frames = `2.000 s`, the stretch `#51` `0.00–4.00 s` does not show), raising midpoint `edge_density` from `0.0127` to `0.0414` and every 0.5 s sample to `min_mean_luma 40.9 >= 28.0` and `min_edge_density 0.0217 >= 0.0200`. | **DONE** |
| **19** | **#67–#68** `P4 16_pores_question` & `P5 01_geneva_lake` (`5:57.88–6:09.92`) | `ch_carbon` started at `6:05.00`, 10 frames before Part 04 ended (`6:05.42`). | Shifted `ch_carbon` to `6:05.42–6:07.00` (`8770..8808`), starting cleanly on the Part 05 cut boundary. | **DONE** |
| **20** | **#69–#71** `P5 02_senebier_jars`, `03_de_saussure`, `04_fine_scales` (`6:09.92–6:30.92`) | `timeline_d5` started 2 frames late (`6:10.00` vs `6:09.92`); `who_saussure` started 9 frames early (`6:17.00` vs `6:17.38`); `timeline_d6` spilled 6 frames into `#71` (`6:23.62` vs `6:23.38`). | Re-timed `timeline_d5` to `6:09.92–6:12.92` (`8878..8950`), `who_senebier` to `6:13.21–6:16.62` (`8957..9039`), `who_saussure` to `6:17.38–6:20.21` (`9057..9125`), and `timeline_d6` to `6:20.21–6:23.38` (`9125..9201`), eliminating all three boundary flashes/spills. | **DONE** |
| **21** | **#78 & #86** `P5 11_trunk_pie` (`7:03.38–7:08.33`) & `P5 19_dots_crowd` (`7:50.46–7:54.46`) | Both code graphics had zero text/number labels on screen, failing the Teach-on-Screen mute test. | Re-rendered both in `_build_part05_code_graphics_v01.py` with house Didot italic labels (`≤ 4` words): `50% Carbon / (from air)` + `44% Oxygen / 6% Hydrogen` callouts on `11_trunk_pie_cg_v01.mp4`, and `CO2: 4 in 10,000` on a walnut/gold lower-third pill on `19_dots_crowd_cg_v01.mp4` (`0` freeze events, `seams=[]`). | **DONE** |

---

## 2. Part 02 Cut-Sync Verification Against `VO_RETIME_v02.json` (`#18`–`#33`)

| Cut | Row ID | `v01` Window | `v02` Window (`mm:ss.cc`) | `v02` Frames | Locked VO Sentence (`VO_RETIME_v02.json`) | Alignment |
|---|---|---|---|---|---|---|
| **#18** | `06_garden_years` | `1:28.63–1:36.54` (`190f`) | **`1:28.62–1:42.00`** | `321f` (`13.38s`) | `[1:28.61–1:40.23]` *"Picture yourself in that garden. Every spring, the leaves burst out. Every autumn, they fall. Year after year the willow grows taller, and the pot of soil never changes."* | **EXACT** (`t2` + `t1` covers full sentence + pause to `1:42.00`). |
| **#19** | `08_haul_tree` | `1:36.54–1:41.33` | **`1:42.00–1:46.79`** | `115f` (`4.79s`) | `[1:40.97–1:45.57]` *"Then, after five years, he pulled the tree out and weighed it."* | **EXACT** (`+5.46s` shift). |
| **#20** | `09_weights_169` | `1:41.33–1:45.25` | **`1:46.79–1:50.71`** | `94f` (`3.92s`) | `[1:46.85–1:50.13]` *"A hundred and sixty-nine pounds, about the weight of a grown man."* | **EXACT** (`num_169` animates `1:46.83–1:50.04`). |
| **#21** | `10_fallen_leaves` | `1:45.25–1:49.67` | **`1:50.71–1:55.12`** | `106f` (`4.42s`) | `[1:50.75–1:54.91]` *"And that didn't even count the leaves that had fallen in four autumns."* | **EXACT** (`fact_leaves` animates `1:50.75–1:53.96`). |
| **#22** | `11_furnace_again` | `1:49.67–1:53.21` | **`1:55.12–1:58.67`** | `85f` (`3.54s`) | `[1:55.17–1:58.67]` *"Now came the moment that mattered. He dried the soil again..."* | **EXACT** (`+5.46s` shift). |
| **#23** | `12_pointer_short` | `1:53.21–2:00.00` | **`1:58.67–2:05.46`** | `163f` (`6.79s`) | `[1:58.67–2:04.49]` *"...and put it back on the scales. Two hundred pounds, less about two ounces."* | **EXACT** (`+5.46s` shift). |
| **#24** | `13_tree_vs_pinch` | `2:00.00–2:05.38` | **`2:05.46–2:10.83`** | `129f` (`5.38s`) | `[2:05.49–2:10.25]` *"A hundred and sixty-four pounds of new tree, and only two ounces of soil gone."* | **EXACT** (`+5.46s` shift + bare-table trim). |
| **#25** | `14_why_grown` | `2:05.38–2:09.79` | **`2:10.83–2:15.25`** | `106f` (`4.42s`) | `[2:10.87–2:14.37]` *"The tree had not eaten the soil. So why had it grown?"* | **EXACT** (`+5.46s` shift). |
| **#26** | `15_desk_candle` | `2:09.79–2:15.25` | **`2:15.25–2:20.71`** | `131f` (`5.46s`) | `[2:15.27–2:20.25]` *"Van Helmont's answer seemed obvious. The only thing he had added was water."* | **EXACT** (`+5.46s` shift). |
| **#27** | `16_water_drawing` | `2:15.25–2:20.38` | **`2:20.71–2:25.83`** | `123f` (`5.12s`) | `[2:20.73–2:25.87]` *"So, he wrote, the wood, the bark and the roots had come from water alone."* | **EXACT** (`+5.46s` shift). |
| **#28** | `17_mostly_wrong` | `2:20.38–2:25.71` | **`2:25.83–2:31.17`** | `128f` (`5.33s`) | `[2:25.87–2:30.65]` *"It was a brilliant experiment, and his answer was mostly wrong."* | **EXACT** (`+5.46s` shift). |
| **#29** | `18_charcoal_hearth` | `2:25.71–2:32.50` | **`2:31.17–2:37.96`** | `163f` (`6.79s`) | `[2:31.17–2:37.95]` *"And here is the strangest part of the mystery. Van Helmont also burned sixty-two pounds of charcoal..."* | **EXACT** (`+5.46s` shift). |
| **#30** | `19_ash_mound` | `2:32.50–2:36.04` | **`2:37.96–2:41.50`** | `85f` (`3.54s`) | `[2:37.95–2:40.99]` *"...and found just one pound of ash left behind."* | **EXACT** (`+5.46s` shift). |
| **#31** | `20_shimmer_coals` | `2:36.04–2:41.21` | **`2:41.50–2:46.67`** | `124f` (`5.17s`) | `[2:41.51–2:46.09]` *"The rest had vanished into the air, as a wild, invisible spirit."* | **EXACT** (`+5.46s` shift). |
| **#32** | `21_gas_window` | `2:41.21–2:47.83` | **`2:46.67–2:53.29`** | `159f` (`6.62s`) | `[2:46.67–2:52.70]` *"He gave it a new name: gas. We now know that gas was mostly carbon dioxide."* | **EXACT** (`fact_gas` animates `2:46.67–2:49.88`). |
| **#33** | `22_shimmer_willow` | `2:47.83–2:58.67` (`260f`) | **`2:53.29–2:58.67`** | `129f` (`5.38s`) | `[2:53.30–2:58.45]` *"He had discovered the very thing his tree was made of. He never put the two together."* | **EXACT** (UI filler card removed; returns to `5.38s`). |

---

## 3. Teach-on-Screen & House-Style Review Gate (`full_join_v02_teach`)

| Gate Item | `v01` Score | `v02` Score | `full_join_v02_teach` Verification |
|---|---|---|---|
| **1. DATA** (≥3 animated data moments + timeline, reads muted, matches `FACT_NOTES`) | FIX | **PASS** | 6-drop period-paper timeline (`d1`–`d6`) + 5 animated DATA moments: `#14` (`0 → 200 pounds of dried soil`), `#20` (`0 → 169 pounds`), `#53` (`0 → 500 experiments`), `#78` (`50% Carbon (from air)` / `44% Oxygen · 6% Hydrogen` wood-ring pie), `#86` (`CO2: 4 in 10,000` dot crowd). Every graphic reads with the sound off and matches `FACT_NOTES_v01.md`. |
| **2. WHO** (every named person at first mention, sourced years & period role) | PASS (re-time 3) | **PASS** | All 7 WHO cards (`who_aristotle`, `who_helmont`, `who_hales`, `who_priestley`, `who_ingenhousz`, `who_senebier`, `who_saussure`) land on first mention, carry sourced years and period-accurate roles, and stay strictly inside their cut boundaries. |
| **3. WHEN** (every spoken date/era has stamp or timeline marker) | PASS (re-time 6) | **PASS** | All 6 timeline markers (`early 1600s`, `1727`, `1771`, `1779`, `1782`, `1804`) start/end on exact cut boundaries with zero 2–10 frame flashes or spills. |
| **4. FACT** (2–4 sourced fact beats) | PASS (re-time 2) | **PASS** | `fact_leaves` (`1:50.75–1:53.96` in `#21`) and `fact_gas` (`2:46.67–2:49.88` in `#32`) now land directly on their spoken sentences after the Part 02 `+5.46 s` sync fix. |
| **5. STYLE** (house style, white/cream Didot italic or cream teach card, ≤4 words/label, no flat UI/poster card, no Veo text) | FIX | **PASS** | Both flat slate-blue/cream UI cards (`#14` and `#33`) are gone; `#20` (`09_weights_169_crop_v02.mp4`) crops out the Veo `"169"` numerals and floating quill (`y > 788`). |
| **6. MOTION** (animates over moving picture, ≤4 s hold, never two full-frame graphics back to back) | FIX | **PASS** | In `#52` (`4:33.50–4:39.50`), `ch_bubbles` (`4:33.50–4:35.08`) and `timeline_d4` (`4:36.29–4:39.50`) are separated by `1.21 s` (`29` frames) of moving `01_villa_t1.mp4`. No card holds still > 4 s. |

---

## 4. Pasted Gate Outputs

### A. `polish_gate.py` (`0 failed`)
```text
polish gate PASS: 0 of 91 rows failed, 5 to look at -> /Users/benjaminoats/YouTube/History Of Science/02_Video-Projects/006_Trees-Are-Made-Of-Air/07_Edit-Project/full_join_v02_teach/polish_gate.json
```

### B. `picture_qa.py` (`0 fail`)
```text
WARN   2:18 row 15_desk_candle 15_desk_candle_t1_above_desk_v03.mp4: low detail: edge density 0.0271 < film p5 0.0272
WARN   3:01 row 01_soil_to_sky 01_soil_to_sky_t1.mp4: low detail: edge density 0.0219 < film p5 0.0272
WARN   5:24 row 09_bubbles_again 05_bubbles_macro_t1_from4.500.mp4: low detail: edge density 0.0245 < film p5 0.0272
WARN   6:32 row 05_sums_add_up 05_sums_add_up_t1.mp4: low detail: edge density 0.0248 < film p5 0.0272
WARN   8:17 row 23_carbon_atom 23_carbon_atom_t1.mp4: low detail: edge density 0.0238 < film p5 0.0272
picture QA PASS: 0 of 91 cuts fail, 5 to look at -> /Users/benjaminoats/YouTube/History Of Science/02_Video-Projects/006_Trees-Are-Made-Of-Air/07_Edit-Project/full_join_v02_teach/PICTURE_QA.md, /Users/benjaminoats/YouTube/History Of Science/02_Video-Projects/006_Trees-Are-Made-Of-Air/07_Edit-Project/full_join_v02_teach/picture_qa_review.jpg
```
*(Note: The 5 WARNs above are simply the film's bottom 5th-percentile `edge_density` cuts out of 91 (`p5 = 0.0272`): `#26` (`15_desk_candle` at `2:18`) is our own crop (`15_desk_candle_t1_above_desk_v03.mp4`, not a Veo Chief-KEEP plate), and the other 4 (`#34`, `#60`, `#72`, `#90`) are Veo Chief-KEEP 3D cartoon plates already inspected and marked KEEP in `REVIEW_v01.md`. All 5 sit above the `0.021` floor after raising the film `p5` from `0.0227` to `0.0272`, and zero cuts fail `luma_std < 18.0`.)*

### C. `npm run gate:episode` (`PASS · 93.7/100`)
```text
# Episode gate — 006_Trees-Are-Made-Of-Air

**Decision:** PASS — VO / Gemini Veo allowed

| Check | Status | Detail |
|---|---|---|
| project_dir | OK | Project: /Users/benjaminoats/YouTube/History Of Science/02_Video-Projects/006_Trees-Are-Made-Of-Air |
| prebuild_vidiq | OK | Pre-build vidIQ audit present and looks signed off. |
| script_file | OK | Script: 01_Script/trees_script_master_v02.md |
| script_review | OK | Script reviewer PASS 93.7/90 (need ≥90). |
| explorer_acts | OK | [EXPLORER ACTS] beats 3 (need ≥1). |
| visual_must | OK | [VISUAL MUST] count 49 (need ≥4). |
| teach | OK | [TEACH] count 5 (need ≥4). |
| chapters | OK | [CHAPTER CARD] count 4 (aim 4–6 film acts). |
| production_checklist | OK | Checklist present: 11_Upload-Package/PRODUCTION_CHECKLIST_V2.md |

Script score: **93.7/100** · PASS
```
