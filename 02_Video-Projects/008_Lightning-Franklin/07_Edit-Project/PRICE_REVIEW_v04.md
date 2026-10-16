# 008 price review v04 (Teach/Polish edit-overlay sync on Chief-PASSed v03)

Gemini, 16 Oct 2026, J0397. Boards only. **No mint. No spend. No merge.**
Preserves the exact Chief-PASSed v03 row counts, qualities, prices, and Flow totals (112 rows: 15 Quality / 86 non-emissive Fast / 11 £0 code graphics / 0 reuse; Flow try-1 **2,360**, Flow expected **5,605**).
Attaches 17 explicit `teach_overlay` specs (`WHO`, `WHEN`, `DATA + SCALE`, `FACT`, `TIMELINE`) sourced from `01_Script/FACT_NOTES_v01.md` for the edit (`AGENTS.md`: *"Cards and timeline added in the edit: 006, 007 and 008"*), with zero back-to-back full-frame graphics.

---

# J0240 — HOS 008 v03 plate boards & price review (15 Oct 2026)

Gemini covering (`J0240`, follow-on from `J0184` / HOS #317 `520cbe7`). Boards only: **no mint, no spend**.

## 1. Totals: v01 vs v02 vs v03

All 112 timed rows, VO hashes, sentence anchors, durations, spoken lines, and Explorer references are unchanged from `v01`/`v02`. Run `python3 02_Video-Projects/008_Lightning-Franklin/07_Edit-Project/_build_plate_boards_v03.py` to reproduce `part-01_plates_v03.json`–`part-05_plates_v03.json` and `PICTURE_PLAN_v03.json`.

| Metric | v01 | v02 (conditional) | **v03 (resolved)** |
|---|---:|---:|---:|
| Total rows | 112 | 112 | **112** |
| Quality hero/cover mints | 63 | 15 | **15** |
| Fast mints (non-emissive) | 46 | 82 *(flagged)* | **86** *(0 flagged)* |
| Code graphics (£0 / 0 cr) | 0 | 0 *(11 flagged)* | **11** |
| Reuse rows | 3 *(overlapping)* | 15 *(unmeasured)* | **0** *(all 15 measured)* |
| Total Veo mints | 109 | 97 | **101** |
| **Flow try-1 credits** | 6,850 cr | 2,320 cr | **2,360 cr** |
| **Flow expected credits** | 17,476 cr | 5,525 cr | **5,605 cr** |
| Vertex try-1 (fallback) | £88.96 | £58.08 | **£59.20** |
| Vertex expected (fallback) | £223.64 | £130.95 | **£133.38** |

### Per-part v03 breakdown

| Part | Rows | Mints | Quality | Fast | Code Graphic (£0) | Reuse | Flow try-1 | **Flow expected** | Vertex try-1 | Vertex expected |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Part 01 | 22 | 22 | 3 | 19 | 0 | 0 | 490 cr | **1,157 cr** | £12.64 | £28.36 |
| Part 02 | 19 | 17 | 2 | 15 | 2 | 0 | 350 cr | **818 cr** | £8.96 | £19.80 |
| Part 03 | 28 | 25 | 2 | 23 | 3 | 0 | 430 cr | **978 cr** | £13.76 | £30.17 |
| Part 04 | 18 | 16 | 4 | 12 | 2 | 0 | 520 cr | **1,276 cr** | £10.24 | £23.85 |
| Part 05 | 25 | 21 | 4 | 17 | 4 | 0 | 570 cr | **1,376 cr** | £13.60 | £31.20 |
| **Total** | **112** | **101** | **15** | **86** | **11** | **0** | **2,360 cr** | **5,605 cr** | **£59.20** | **£133.38** |

---

## 2. Condition (a): Emissive Fast prompts rewritten & 15-Quality hero swap

- **Hero swap (holding Quality = 15):**
  - Promoted to **Quality hero**: `P5:07_giant_spark` (`"Here's how it works. Lightning is a giant spark, hotter than the surface of the Sun"`, label `HOTTER THAN THE SUN`), where the giant branching bolt across the sky is the story.
  - Dropped to **Fast**: `P3:25_fibres_rise` (`"They were standing up on end, and pushing away from each other"`), which is a macro shot of wet hemp twine fibres lifting in grey storm daylight with no flame, spark, candle or face in shot.
- **All 86 Fast rows verified non-emissive (`review_required: []`):**
  - Every Fast row previously mentioning candles, sparks, flashes, bolts, or cloud flickers (`P1:02`, `P1:04`, `P1:05`, `P1:06`, `P1:08`, `P1:09`, `P1:11`, `P1:12`, `P2:01`, `P2:02`, `P2:03`, `P2:04`, `P2:05`, `P2:06`, `P2:09`, `P2:10`, `P2:11`, `P3:01`, `P3:02`, `P3:11`, `P3:12`, `P3:13`, `P3:16`, `P3:18`, `P3:20`, `P3:21`, `P3:22`, `P3:24`, `P3:25`, `P4:01`, `P4:07`, `P4:10`, `P4:11`, `P4:14`, `P4:15`, `P5:01`, `P5:03`, `P5:15`, `P5:18`, `P5:22`, plus the 15 former-reuse rows) has been rewritten into non-emissive framing: daylight/window light, or off-screen storm/room light shown only by its indirect reflection on walls, glass, faces, or wet slate without any flame, spark, or bolt in shot.

---

## 3. Condition (b): 11 flat-card and diagram rows → £0 code graphics

All 11 rows flagged in `v02` for flat-card/diagram prompts are now `quality: "code_graphic"` (`route: "code-graphic"`, `0` Flow credits, `£0.00` Vertex) with per-row `code_graphic_spec` definitions for our Python/Pillow/ffmpeg house explainer renderer. Where code-graphic rows sit adjacent (`P2:14`–`15`, `P3:03`–`04`, `P5:08`–`11`), they alternate `full_frame_period_paper` with `moving_plate_overlay` so two full-frame teach graphics never run back to back.

| Row | Duration | File | Layout Mode | Label |
|---|---:|---|---|---|
| `P2:14_likeness_pairs` | 5.08 s | `code_graphic_008_p2_14_likeness_pairs.mp4` | `full_frame_period_paper` | `SAME COLOUR · CROOKED LINES` |
| `P2:15_likeness_fire` | 5.28 s | `code_graphic_008_p2_15_likeness_fire.mp4` | `moving_plate_overlay` | `CRACK · FIRE · SHOCK` |
| `P3:03_rod_cloud` | 6.50 s | `code_graphic_008_p3_03_rod_cloud.mp4` | `full_frame_period_paper` | `DRAWING CHARGE FROM CLOUD` |
| `P3:04_letter_crosses` | 3.76 s | `code_graphic_008_p3_04_letter_crosses.mp4` | `moving_plate_overlay` | `PHILADELPHIA TO PARIS` |
| `P3:15_wet_dry` | 5.30 s | `code_graphic_008_p3_15_wet_dry.mp4` | `full_frame_period_paper` | `WET TWINE · DRY SILK` |
| `P4:06_same_thing` | 7.30 s | `code_graphic_008_p4_06_same_thing.mp4` | `moving_plate_overlay` | `ELECTRICITY` |
| `P4:08_teach_charge` | 7.10 s | `code_graphic_008_p4_08_teach_charge.mp4` | `full_frame_period_paper` | `NO BOLT, JUST CHARGE` |
| `P5:08_looking_path` | 3.16 s | `code_graphic_008_p5_08_looking_path.mp4` | `moving_plate_overlay` | `EASIEST PATH DOWN` |
| `P5:09_wood_vs_metal` | 6.86 s | `code_graphic_008_p5_09_wood_vs_metal.mp4` | `full_frame_period_paper` | `WOOD AND STONE RESIST` |
| `P5:10_metal_easy` | 2.98 s | `code_graphic_008_p5_10_metal_easy.mp4` | `moving_plate_overlay` | `METAL CONDUCTS` |
| `P5:11_safe_path` | 6.98 s | `code_graphic_008_p5_11_safe_path.mp4` | `full_frame_period_paper` | `A SAFE PATH TO THE GROUND` |

---

## 4. Condition (c): Measured unused footage on all 15 v02 reuse rows

Each Veo clip is `8.00 s` raw (`7.90 s` usable `clip_use_s` after cross-fade pad). Measuring `unused_raw_s = 8.00 - source_used_s` and `unused_usable_s = 7.90 - source_used_s` for every one of the 15 `v02` reuse rows shows that **0 of 15** can supply a distinct non-overlapping window of the row's full `use_s` length (every continuation pair in `v01` was created only when the span exceeded `7.90 s`, and all three `v01` callbacks exceeded `8.00 s` combined):

| Reuse Row (`v02`) | Needed `use_s` | Source Row (`reuse_of`) | Source `use_s` | Unused in 8.00 s (`7.90 s` usable) | Shortfall raw (`usable`) | Resolution in `v03` |
|---|---:|---|---:|---:|---:|---|
| `P1:01_kite_open_c1` | 5.92 s | `P1:01_kite_open` | 5.92 s | 2.08 s (1.98 s) | 3.84 s (3.94 s) | Priced Fast mint (8 s) |
| `P1:03_table_three_c1` | 4.92 s | `P1:03_table_three` | 4.92 s | 3.08 s (2.98 s) | 1.84 s (1.94 s) | Priced Fast mint (6 s) |
| `P1:13_ring_the_bells_c1` | 5.05 s | `P1:13_ring_the_bells` | 5.05 s | 2.95 s (2.85 s) | 2.10 s (2.20 s) | Priced Fast mint (6 s) |
| `P1:15_bell_count_c1` | 4.18 s | `P1:15_bell_count` | 4.18 s | 3.82 s (3.72 s) | 0.36 s (0.46 s) | Priced Fast mint (6 s) |
| `P2:17_page_bottom_c1` | 4.45 s | `P2:17_page_bottom` | 4.45 s | 3.55 s (3.45 s) | 0.90 s (1.00 s) | Priced Fast mint (6 s) |
| `P3:05_marly_garden_c1` | 5.12 s | `P3:05_marly_garden` | 5.12 s | 2.88 s (2.78 s) | 2.24 s (2.34 s) | Priced Fast mint (6 s) |
| `P3:07_slow_news` | 4.50 s | `P3:04_letter_crosses` | 3.76 s | 4.24 s (4.14 s) | 0.26 s (0.36 s) | Priced Fast mint (6 s; `P3:04` is code graphic) |
| `P3:13_key_ribbon_c1` | 4.27 s | `P3:13_key_ribbon` | 4.27 s | 3.73 s (3.63 s) | 0.54 s (0.64 s) | Priced Fast mint (6 s) |
| `P3:21_doorway_pov_c1` | 4.04 s | `P3:21_doorway_pov` | 4.04 s | 3.96 s (3.86 s) | 0.08 s (0.18 s) | Priced Fast mint (6 s) |
| `P4:03_room_memory` | 5.26 s | `P1:17_globe_spark` | 4.45 s | 3.55 s (3.45 s) | 1.71 s (1.81 s) | Priced Fast mint (6 s) |
| `P4:09_charge_string_c1` | 5.29 s | `P4:09_charge_string` | 5.29 s | 2.71 s (2.61 s) | 2.58 s (2.68 s) | Priced Fast mint (6 s) |
| `P5:06_rod_fitting_c1` | 4.39 s | `P5:06_rod_fitting` | 4.39 s | 3.61 s (3.51 s) | 0.78 s (0.88 s) | Priced Fast mint (6 s) |
| `P5:15_why_card_c1` | 5.96 s | `P5:15_why_card` | 5.96 s | 2.04 s (1.94 s) | 3.92 s (4.02 s) | Priced Fast mint (8 s) |
| `P5:20_table_three_again` | 3.10 s | `P1:03_table_three` | 4.92 s | 3.08 s (2.98 s) | 0.02 s (0.12 s) | Priced Fast mint (4 s) |
| `P5:22_newton_handoff_c1` | 5.46 s | `P5:22_newton_handoff` | 5.46 s | 2.54 s (2.44 s) | 2.92 s (3.02 s) | Priced Fast mint (6 s) |

**Status:** Parked for Chief (`parked for Chief: 008 v03 boards`). No mint, no spend.
