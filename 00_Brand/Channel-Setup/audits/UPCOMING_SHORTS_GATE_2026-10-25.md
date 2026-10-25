# Upcoming HOS Shorts: gate check (`--report-only`)

Run with `gate_shorts_open.py check --report-only` over the 13 scheduled private HOS Shorts on 2026-10-25 (J0918).

| Airs (London) | Short | In library | Gate (`--report-only`) | Would fail 60% stayed gate? | `f0diff` | `cut1` | `vo_onset` | `tail_gap` | `vo_src` |
|---|---|---|---|---|---:|---:|---:|---:|---|
| 2026-10-26 11:30 | [How Did John Snow Stop Cholera?](https://youtu.be/OnJ8MFu0Mi0) `OnJ8MFu0Mi0` | no | **PASS** | YES (pushed still at frame 0 (mean 0–1.5 s frame diff 0.47 < 1.50) — use moving footage; first cut at 4.67s > 3.0s (scene-change detect)) | 0.47 | 4.67s | 0.06s | 0.57s | `hos_sa_s3_snow_pump_vo_v02.wav` |
| 2026-10-27 11:30 | [What Is the Pasteur Swan Neck Flask Experiment?](https://youtu.be/1-BZaFIMwYU) `1-BZaFIMwYU` | yes | **PASS** | YES (pushed still at frame 0 (mean 0–1.5 s frame diff 1.22 < 1.50) — use moving footage) | 1.22 | 2.70s | 0.17s | 0.22s | `mix` |
| 2026-10-28 11:30 | [Are Marie Curie's Notebooks Still Radioactive?](https://youtu.be/vEg_tLIm0Co) `vEg_tLIm0Co` | no | **PASS** | YES (pushed still at frame 0 (mean 0–1.5 s frame diff 0.27 < 1.50) — use moving footage; first cut at 3.30s > 3.0s (scene-change detect)) | 0.27 | 3.30s | 0.10s | 0.00s | `hos_sa_s4_curie_notebooks_vo_v01.wav` |
| 2026-10-30 11:30 | [Why Does Your Heart Pump More Blood Than You Have?](https://youtu.be/1lszTrYRp-8) `1lszTrYRp-8` | no | **PASS** | NO (PASS strict) | 5.61 | 2.20s | 0.06s | 0.59s | `mix` |
| 2026-10-31 11:30 | [Is the Heart a Pump?](https://youtu.be/5n7xFQRBUvI) `5n7xFQRBUvI` | yes | **PASS** | NO (PASS strict) | 3.85 | 2.17s | 0.67s | 0.63s | `mix` |
| 2026-11-01 11:30 | [Why Did Gold Foil Bounce Rutherford's Particles Back?](https://youtu.be/JyRjM-9Yc8g) `JyRjM-9Yc8g` | no | **PASS** | YES (first cut at 3.20s > 3.0s (scene-change detect)) | 8.64 | 3.20s | 0.05s | 0.25s | `mix` |
| 2026-11-03 11:30 | [Why Were the Four Elements Wrong?](https://youtu.be/Pp5LmjsduI4) `Pp5LmjsduI4` | no | **PASS** | YES (first cut at 3.40s > 3.0s (scene-change detect)) | 6.29 | 3.40s | 0.05s | 0.17s | `mix` |
| 2026-11-05 11:30 | [Why Do Veins Have Valves?](https://youtu.be/PlihWC5uA2E) `PlihWC5uA2E` | no | **PASS** | NO (PASS strict) | 4.62 | 2.30s | 0.58s | 0.59s | `mix` |
| 2026-11-08 11:30 | [How Did One Tight Band Prove Your Blood Goes Round?](https://youtu.be/mTY67qet7cM) `mTY67qet7cM` | no | **PASS** | NO (PASS strict) | 4.09 | 2.70s | 0.06s | 0.55s | `mix` |
| 2026-11-13 11:30 | [What Was the Edward Jenner Experiment?](https://youtu.be/-I_GHK-GcFs) `-I_GHK-GcFs` | yes | **PASS** | NO (PASS strict) | 3.01 | 2.20s | 0.10s | 0.37s | `mix` |
| 2026-11-15 11:30 | [What Are the Blood Vessels Finer Than a Hair?](https://youtu.be/x_3L_IdYgEc) `x_3L_IdYgEc` | no | **PASS** | YES (pushed still at frame 0 (mean 0–1.5 s frame diff 0.94 < 1.50) — use moving footage) | 0.94 | 2.07s | 0.06s | 0.58s | `mix` |
| 2026-11-16 11:30 | [What Is Dalton's Atomic Theory?](https://youtu.be/-sa2t7dAtCk) `-sa2t7dAtCk` | no | **PASS** | YES (first cut at 4.80s > 3.0s (scene-change detect)) | 1.91 | 4.80s | 0.00s | 0.57s | `mix` |
| 2026-11-17 11:30 | [Why Is It Called a Vaccine?](https://youtu.be/4WUs0beKn0A) `4WUs0beKn0A` | yes | **PASS** | NO (PASS strict) | 3.98 | 2.53s | 0.44s | 0.38s | `mix` |

## Details

### `OnJ8MFu0Mi0` — How Did John Snow Stop Cholera? (`hos_sa_s3_snow_pump_v02.mp4`)

- report-only (would fail 60% stayed gate): pushed still at frame 0 (mean 0–1.5 s frame diff 0.47 < 1.50) — use moving footage
- report-only (would fail 60% stayed gate): first cut at 4.67s > 3.0s (scene-change detect)

### `1-BZaFIMwYU` — What Is the Pasteur Swan Neck Flask Experiment? (`hos_001_s11_curved_flask_v02.mp4`)

- report-only (would fail 60% stayed gate): pushed still at frame 0 (mean 0–1.5 s frame diff 1.22 < 1.50) — use moving footage
- warn: first VO word starts at 0.17s > 0.15s — trim leading silence

### `vEg_tLIm0Co` — Are Marie Curie's Notebooks Still Radioactive? (`hos_sa_s4_curie_notebooks_v04.mp4`)

- report-only (would fail 60% stayed gate): pushed still at frame 0 (mean 0–1.5 s frame diff 0.27 < 1.50) — use moving footage
- report-only (would fail 60% stayed gate): first cut at 3.30s > 3.0s (scene-change detect)

### `5n7xFQRBUvI` — Is the Heart a Pump? (`hos_005_s04_galen_stove_v01.mp4`)

- warn: first VO word starts at 0.67s > 0.15s — trim leading silence

### `JyRjM-9Yc8g` — Why Did Gold Foil Bounce Rutherford's Particles Back? (`hos_004_backcat_gold_foil_v01.mp4`)

- report-only (would fail 60% stayed gate): first cut at 3.20s > 3.0s (scene-change detect)

### `Pp5LmjsduI4` — Why Were the Four Elements Wrong? (`hos_002_backcat_four_elements_v01.mp4`)

- report-only (would fail 60% stayed gate): first cut at 3.40s > 3.0s (scene-change detect)

### `PlihWC5uA2E` — Why Do Veins Have Valves? (`hos_005_s05_valves_v01.mp4`)

- warn: first VO word starts at 0.58s > 0.15s — trim leading silence

### `x_3L_IdYgEc` — What Are the Blood Vessels Finer Than a Hair? (`hos_005_s03_never_saw_v02.mp4`)

- report-only (would fail 60% stayed gate): pushed still at frame 0 (mean 0–1.5 s frame diff 0.94 < 1.50) — use moving footage

### `-sa2t7dAtCk` — What Is Dalton's Atomic Theory? (`hos_004_s05_dalton_v02.mp4`)

- report-only (would fail 60% stayed gate): first cut at 4.80s > 3.0s (scene-change detect)

### `4WUs0beKn0A` — Why Is It Called a Vaccine? (`hos_007_s05_vacca_jesty_v02.mp4`)

- warn: first VO word starts at 0.44s > 0.15s — trim leading silence
