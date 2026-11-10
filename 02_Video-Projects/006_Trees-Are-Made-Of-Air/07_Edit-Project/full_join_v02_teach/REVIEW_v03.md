# HOS 006 — `full_join_v03_teach` Delta & Re-Gate Report (`REVIEW_v03.md` · J0826)

- **Master (`full_join_v03_teach` / updated `full_join_v02_teach`):** `02_Video-Projects/006_Trees-Are-Made-Of-Air/07_Edit-Project/full_join_v02_teach/hos_006_full_join_v03_teach.mp4` (and `hos_006_full_join_v02_teach.mp4`)
- **iCloud HOS UAT copy:** `~/Library/Mobile Documents/com~apple~CloudDocs/HOS UAT/hos_006_full_join_v03_teach.mp4` (and `hos_006_full_join_v02_teach.mp4`)
- **NAS archive copy:** `/Volumes/data/mac-mini-archive/YouTube/History Of Science/02_Video-Projects/006_Trees-Are-Made-Of-Air/07_Edit-Project/full_join_v02_teach/hos_006_full_join_v03_teach.mp4` (and `hos_006_full_join_v02_teach.mp4`)
- **SHA-256:** `d24a08ee94489379dd8e550700b9e31ec2fd4636c35158d037949248ecf8eb34`
- **Runtime / frames:** `507.833333 s` (`8:27.83`), `12,188` frames @ `24 fps`, `1920×1080`
- **Audio:** Byte-identical copy of `full_join_v01_teach` VO (no music bed per ElevenLabs credit hold until 30 Oct).
- **Spend:** `£0` (zero new Vertex/Flow mints; zero ElevenLabs spend).
- **Gate status:** `picture_qa.py` **PASS** (`0 of 91 cuts fail`), `polish_gate.py` **PASS** (`0 of 91 rows failed`), `npm run gate:episode` **PASS** (`93.7/100`).

---

## 1. J0826 & J0829 Delta Table — Chief FIX on `REVIEW_v02.md` (`4 / 4` Done)

| # | Item | Chief Ruling (J0826 / J0829) | `v03` Action Taken | Status |
|---|---|---|---|---|
| **1** | **#33** `P2 22_shimmer_willow_v02` (`2:53.29–2:58.67`) | Ended on `15_desk_candle_t1_above_desk_v03` `0.00–2.54 s` (repeating `#26` at `2:15.25`, `38 s` earlier, and a desk candle doesn't fit *"the very thing his tree was made of"*). Fill the `2.54 s` from an unused window of `22_shimmer_willow_t1` (`2.63–5.17 s` if clean) so `#33` stays all willow. | Re-built `22_shimmer_willow_v02.mp4` (`129` frames = `5.375 s`, sha256 `d318244121999faf78b53cea3162191282c2f1e848cd3c0cffa57b831633deff`) purely from `22_shimmer_willow_t1.mp4` frames `63..192` (`2.625–8.000 s`), so `#33` is 100% shimmering willow in the pot with zero `15_desk_candle` repeat (`edge_density 0.1612`, `luma_std 52.2`, `0` fail/warn). | **DONE** |
| **2** | **#62** `P4 11_night_jars_v02` (`5:30.46–5:38.29`) | Start `11_night_jars_t1` at `>= 4.30 s` after the `2.3–4.3 s` silhouette, played at `0.635x` speed (`3.70 s -> 5.83 s`, `140` frames, frame-blended) + `18_dark_window_t1` `4.00–6.00 s` (`48` frames) = `188` frames. Check luma and edge density at every `0.5 s` (`min_mean_luma >= 28`, no frame under `edge_density 0.02`). | Re-built `11_night_jars_v02.mp4` (`188` frames = `7.833 s`, sha256 `98c7d31f7c15de783a6dd04d5e27d20e1471786d18203a845f8ef96382739bec`): `11_night_jars_t1.mp4` `4.30–8.00 s` (`89` frames = `3.70 s` played at `0.635x` speed → `140` frames = `5.833 s`, frame-blended) + `18_dark_window_t1.mp4` `4.000–6.000 s` (frames `96..144` = `48` frames = `2.000 s`, the exact tail `#51` `0.00–4.00 s` never shows). The joined master matches that clip (mean squared error `0.65` across all `188` frames). Every `0.5 s` sample and all `188` frames pass: `min_mean_luma = 40.81 >= 28.0`, `min_edge_density = 0.0217 >= 0.0200` (table in §2.D). | **DONE** |
| **3** | **#86** `P5 19_dots_crowd` (`7:50.46–7:54.46`) | Label `"4 in 10,000 · Carbon Dioxide"` was 5 words (house rule is `≤ 4` words). Change to `"CO2: 4 in 10,000"`. | Updated `_build_part05_code_graphics_v01.py` (`txt = "CO2: 4 in 10,000"`, 4 words in house Didot italic on walnut/gold lower-third pill) and re-rendered `19_dots_crowd_cg_v01.mp4` (sha256 `a75baed0b9f0745b474dbc4c17555715dea0b04a5edc2ba54dcb2d32e752616d`, `0` fail/warn). | **DONE** |
| **4** | **`REVIEW_v02.md` §4 note** | Correct the §4 note: `15_desk_candle` at `2:18` is our own crop (`15_desk_candle_t1_above_desk_v03.mp4`), not a Veo Chief-KEEP plate. | Corrected in `REVIEW_v02.md` §4.B and §2 below: `#26` (`15_desk_candle` at `2:18`) is explicitly documented as our own crop (`15_desk_candle_t1_above_desk_v03.mp4`, not a Veo Chief-KEEP plate), while the other 4 `p5` WARNs (`#34`, `#60`, `#72`, `#90`) are Veo Chief-KEEP plates. | **DONE** |

---

## 2. Pasted Gate Outputs (`full_join_v03_teach`)

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
*(Note: The 5 WARNs above are the film's bottom 5th-percentile `edge_density` cuts out of 91 (`p5 = 0.0272`): `#26` (`15_desk_candle` at `2:18`) is our own crop (`15_desk_candle_t1_above_desk_v03.mp4`, not a Veo Chief-KEEP plate), and the other 4 (`#34`, `#60`, `#72`, `#90`) are Veo Chief-KEEP 3D cartoon plates already inspected and marked KEEP in `REVIEW_v01.md`. All 5 sit above the `0.021` floor, and zero cuts fail `luma_std < 18.0`.)*

### C. `npm run gate:episode` (`PASS · 93.7/100`)
```text
# Episode gate — 006_Trees-Are-Made-Of-Air

**Decision:** PASS — VO / Gemini Veo allowed

Script score: **93.7/100** · PASS
```

### D. `#62` luma and edge every `0.5 s` (J0829, measured on `hos_006_full_join_v03_teach.mp4` at `5:30.46`, `960×540`, `polish_gate.edge_density`)

All `188` frames: `min_mean_luma = 40.81`, `min_edge_density = 0.0217` (frame 0). Floor is `28` and `0.02`.

| t in shot | mean luma | edge density |
|---|---:|---:|
| 0.00 | 58.69 | 0.0217 |
| 0.50 | 44.75 | 0.0324 |
| 1.00 | 52.25 | 0.0363 |
| 1.50 | 56.16 | 0.0371 |
| 2.00 | 60.64 | 0.0386 |
| 2.50 | 64.98 | 0.0407 |
| 3.00 | 68.79 | 0.0411 |
| 3.50 | 70.00 | 0.0413 |
| 4.00 | 70.85 | 0.0414 |
| 4.50 | 71.27 | 0.0415 |
| 5.00 | 71.19 | 0.0416 |
| 5.50 | 71.09 | 0.0424 |
| 6.00 | 40.89 | 0.0273 |
| 6.50 | 41.12 | 0.0280 |
| 7.00 | 41.39 | 0.0282 |
| 7.50 | 41.19 | 0.0279 |

`6.00 s` is the cut onto `18_dark_window_t1` `4.00–6.00 s`. Midpoint polish (`t = 334.38 s`) is mean `70.84`, edge `0.0414`.
