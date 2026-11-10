# HOS 007 — `full_join_v01` Review & Gate Report (`REVIEW_v01.md` · J0827)

- **Master (`full_join_v01`):** `/Users/benjaminoats/YouTube/hos-007-vaccine/02_Video-Projects/007_The-First-Vaccine/07_Edit-Project/_precheck/full_join_v01/hos_007_full_join_v01.mp4`
- **UAT 540p proxy:** `/Users/benjaminoats/YouTube/hos-007-vaccine/02_Video-Projects/007_The-First-Vaccine/07_Edit-Project/_precheck/full_join_v01/hos_007_full_join_v01_uat_proxy.mp4` (sha256 `5ea31960b224`)
- **iCloud HOS UAT copy:** `~/Library/Mobile Documents/com~apple~CloudDocs/HOS UAT/007_full_join_v01/hos_007_full_join_v01.mp4`
- **Contact sheet (all 97 cuts):** `02_Video-Projects/007_The-First-Vaccine/07_Edit-Project/_desk/007/full_join_v01/hos_007_full_join_v01_contact_sheet.jpg`
- **SHA-256:** `7cfd6a594b23fc6fc0e57309b69067584f03f29fe23d5e72af745e36f56682ff`
- **Runtime / frames:** `505.147 s` (`8:25.15`), `12123` frames @ `24 fps`, `1920×1080` (`510.1 MB`)
- **Audio:** Locked 007 VO across Parts 01–05 (no music bed per ElevenLabs credit hold until 30 Oct; no new bed without Chief OK).
- **Spend:** `£0` (zero new Flow/Vertex mints; zero ElevenLabs spend).
- **Gates:** `picture_qa.py` **PASS** (`0 of 97 cuts fail, 5 WARNs to look at`), `polish_gate.py` **PASS** (`0 of 97 cuts failed`), `freezedetect` **PASS** (`0` freeze events >= 0.8 s). **Parked for Chief** (not a film PASS until Chief final OK).

---

## 1. J0827 £0 Repeat-Shot Fixes Applied (`2 / 2` Done)

| # | Cut(s) & Film Time | J0827 Brief Requirement | Action Taken in `full_join_v01` | Status |
|---|---|---|---|---|
| **1** | **#87–#88** `P5:06c_assembly_again` (`7:27.50–7:31.62`, `4.125 s`) + `P5:06d_assembly_front_row` (`7:31.62–7:34.54`, `2.917 s`) | `P5 06c_assembly_again` showed `06_assembly_1980_t1` `0.86–7.90 s`, overlapping `5.3 s` of what `06_assembly_1980` (`7:17.17–7:23.33`) showed `10 s` earlier with an almost identical wide frame. Use the plate's unused tail and make up the rest from another moving P5 plate, and/or use a clearly different framing of the tail (`1.3x` push-in on the clapping front row), never the same wide shot. | Split the `7.0417 s` (`169` frames) slot cleanly at the `1.12 s` VO sentence pause (`49.67 s` in Part 05, between *"…ended by humans."* and *"Why was this so groundbreaking?"*):<br>1) **#87 `06c_assembly_again`** (`4.125 s` = `99` frames): uses the **strictly unused back half (`3.833–7.958 s`, `0.00 s` overlap with `#82 04_health_workers` `0.000–3.833 s`)** of `04_health_workers_t1.mp4` at `1.18×` framing (`scale=2266:1274,crop=1920:1080:173:97`), showing the village families and health workers waving and clapping in golden sunlight.<br>2) **#88 `06d_assembly_front_row`** (`2.917 s` = `70` frames): uses the tail (`5.083–8.000 s`) of `06_assembly_1980_t1.mp4` with a **`1.38×` push-in crop on the clapping front row** (`scale=2650:1490,crop=1920:1080:320:260`), never showing the wide shot. Both sub-cuts are listed separately in `cuts_full_join_v01.json` so both midpoints and contact-sheet thumbnails are checked. | **DONE** |
| **2** | **#14** `P1:09c_case_again` (`1:03.38–1:07.71`, `4.333 s`) | `P1 09c_case_again` (`1:03`) repeated the `02_doctor_case` wide frame from `0:04` (overlap `3.56–7.38 s`). Reframe it so it reads as a new shot: a tight crop on the lancet, or a slow push. Keep the VO timing. | Reframed `02_doctor_case_t1.mp4` (`1.20–5.53 s`, where Veo's 3D camera pushes toward the open case) with a **tight `1.88×` macro crop centered on the silver lancet in the crimson velvet tray** (`scale=3610:2030:flags=lanczos,crop=1920:1080:220:670`, `upscale = 1.88 < 2.00` WARN limit). Reads as a dedicated close-up of the lancet while preserving exact VO timing (`104` frames = `4.333 s`). | **DONE** |

### 0.5-Second Luma / Edge / Seam Sweep on Fixed Cuts

| Cut | `film_t_s` | `mean_luma` | `luma_std` | `edge_density` | `coarse_std` | `seams` |
|---|---:|---:|---:|---:|---:|---|
| `P1:09c_case_again` | `63.62` | `57.62` | `41.59` | `0.0475` | `40.25` | `[]` |
| `P1:09c_case_again` | `64.12` | `59.35` | `42.45` | `0.0449` | `41.18` | `[]` |
| `P1:09c_case_again` | `64.62` | `62.57` | `43.24` | `0.0413` | `42.05` | `[]` |
| `P1:09c_case_again` | `65.12` | `65.47` | `44.42` | `0.0372` | `43.34` | `[]` |
| `P1:09c_case_again` | `65.62` | `68.54` | `45.68` | `0.0344` | `44.67` | `[]` |
| `P1:09c_case_again` | `66.12` | `69.76` | `46.93` | `0.0319` | `46.01` | `[]` |
| `P1:09c_case_again` | `66.62` | `70.56` | `47.32` | `0.0295` | `46.46` | `[]` |
| `P1:09c_case_again` | `67.12` | `70.89` | `47.39` | `0.0252` | `46.64` | `[]` |
| `P5:06c_assembly_again` | `447.75` | `108.34` | `49.78` | `0.1358` | `47.15` | `[]` |
| `P5:06c_assembly_again` | `448.25` | `110.52` | `50.34` | `0.1429` | `47.70` | `[]` |
| `P5:06c_assembly_again` | `448.75` | `110.47` | `50.20` | `0.1432` | `47.61` | `[]` |
| `P5:06c_assembly_again` | `449.25` | `111.56` | `51.20` | `0.1317` | `48.89` | `[]` |
| `P5:06c_assembly_again` | `449.75` | `110.79` | `50.23` | `0.1289` | `47.95` | `[]` |
| `P5:06c_assembly_again` | `450.25` | `116.66` | `51.96` | `0.1212` | `49.79` | `[]` |
| `P5:06c_assembly_again` | `450.75` | `119.85` | `54.50` | `0.1233` | `52.43` | `[]` |
| `P5:06c_assembly_again` | `451.25` | `120.76` | `55.70` | `0.1184` | `53.74` | `[]` |
| `P5:06d_assembly_front_row` | `451.87` | `95.24` | `37.84` | `0.0721` | `35.85` | `[]` |
| `P5:06d_assembly_front_row` | `452.37` | `95.89` | `38.00` | `0.0768` | `35.89` | `[]` |
| `P5:06d_assembly_front_row` | `452.87` | `95.70` | `37.83` | `0.0676` | `35.91` | `[]` |
| `P5:06d_assembly_front_row` | `453.37` | `95.72` | `39.28` | `0.0730` | `37.31` | `[]` |
| `P5:06d_assembly_front_row` | `453.87` | `96.35` | `41.43` | `0.0653` | `39.69` | `[]` |
| `P5:06d_assembly_front_row` | `454.37` | `97.08` | `41.55` | `0.0723` | `39.63` | `[]` |

---

## 2. Part Summary (`Parts 01–05`)

| Part | Rough Slug | Offset (`s`) | Duration (`s`) | Frames | Cuts | SHA-256 |
|---:|---|---:|---:|---:|---:|---|
| `01` | `part01_rough_v01` | `0.000` | `100.833` | `2420` | `20` | `61a5c039c96aa1b222aae686d391e2d949ffc53685d86561b8343bbce7288c6d` |
| `02` | `part02_rough_v01` | `100.833` | `129.625` | `3111` | `22` | `6ab2fb1f2e317ea526c627588c542dc514d517cf50b52901e6b542d8f5e9875a` |
| `03` | `part03_rough_v01` | `230.458` | `78.750` | `1890` | `15` | `62a14a089f2e8c62dc7a711f9fe439c667e21472341e4478336a23743f03169e` |
| `04` | `part04_rough_v01` | `309.208` | `92.750` | `2226` | `20` | `e6a005cd7661b7d4c07c0fc8a19da30a6b45e6c44d9cc3ac9d7edc40621c2ca6` |
| `05` | `part05_rough_v01` | `401.958` | `103.167` | `2476` | `20` | `14206aeb1be19af42f4149e95b068a00d5f0c1cfd17cc216c3c0bbfea1f438de` |

---

## 3. Complete Cut List (`97` Cuts Across Parts 01–05)

| # | Part | Row | Film In–Out | Dur (`s`) | Frames | Source | Offset (`s`) | Upscale | Overlays | Disposition |
|---:|---:|---|---|---:|---:|---|---:|---:|---|---|
| **#01** | P1 | `01_cow_meadow` | `0:00.00–0:04.25` | `4.25` | `102` | `01_cow_meadow_t1.mp4` | `0.00` | `1.00×` | `p1_vacca` | KEEP Flow Quality t1 (J0352 Chief KEEP) |
| **#02** | P1 | `02_doctor_case` | `0:04.25–0:11.62` | `7.38` | `177` | `02_doctor_case_t1.mp4` | `0.00` | `1.00×` | `—` | KEEP Flow Quality t1 (J0352 Chief KEEP) |
| **#03** | P1 | `03_table_three` | `0:11.62–0:19.08` | `7.46` | `179` | `03_table_three_t1.mp4` | `0.00` | `1.50×` | `p1_three` | KEEP Flow Fast t1 (J0352 Chief KEEP) |
| **#04** | P1 | `03b_globe_tease` | `0:19.08–0:23.21` | `4.12` | `99` | `03_globe_lights_t1.mp4` | `3.80` | `1.00×` | `—` | REUSE window 3.80-7.90 s of P5:03_globe_lights |
| **#05** | P1 | `04_church_dusk` | `0:23.21–0:29.21` | `6.00` | `144` | `04_church_dusk_t1.mp4` | `0.00` | `1.50×` | `p1_when_1700s` | KEEP Flow Fast t1 (J0352 Chief KEEP) |
| **#06** | P1 | `07_map_shadows` | `0:29.21–0:35.17` | `5.96` | `143` | `code_graphic_007_p1_07_map_shadows.mp4` | `0.00` | `1.00×` | `p1_monster` | Code graphic v01 (£0, code_graphic_007_p1_07_map_shadows.mp4) |
| **#07** | P1 | `07b_three_in_ten` | `0:35.17–0:38.96` | `3.79` | `91` | `07b_three_in_ten_t1.mp4` | `0.00` | `1.50×` | `p1_data_3in10` | KEEP Flow Fast t1 (J0352 Chief KEEP) |
| **#08** | P1 | `07c_scarred` | `0:38.96–0:44.25` | `5.29` | `127` | `07c_scarred_t1.mp4` | `0.00` | `1.50×` | `—` | KEEP Flow Fast t1 (J0352 Chief KEEP) |
| **#09** | P1 | `05_quiet_lane` | `0:44.25–0:47.67` | `3.42` | `82` | `05_quiet_lane_t1.mp4` | `0.00` | `1.50×` | `—` | KEEP Flow Fast t1 (J0352 Chief KEEP) |
| **#10** | P1 | `06_shuttered_house` | `0:47.67–0:52.33` | `4.67` | `112` | `06_shuttered_house_t1.mp4` | `0.00` | `1.00×` | `—` | KEEP Flow Quality t1 (J0352 Chief KEEP) |
| **#11** | P1 | `08_bell_tower` | `0:52.33–0:55.67` | `3.33` | `80` | `08_bell_tower_t1.mp4` | `0.00` | `1.50×` | `—` | KEEP Flow Fast t1 (J0352 Chief KEEP) |
| **#12** | P1 | `09_churchyard` | `0:55.67–0:59.38` | `3.71` | `89` | `09_churchyard_t1.mp4` | `0.00` | `1.50×` | `—` | KEEP Flow Fast t1 (J0352 Chief KEEP) |
| **#13** | P1 | `09b_counted` | `0:59.38–1:03.38` | `4.00` | `96` | `09b_counted_t1.mp4` | `0.00` | `1.50×` | `—` | KEEP Flow Fast t1 (J0352 Chief KEEP) |
| **#14** | P1 | `09c_case_again` | `1:03.38–1:07.71` | `4.33` | `104` | `02_doctor_case_t1.mp4` | `1.20` | `1.88×` | `—` | REUSE window 1.20-5.53 s of P1:02_doctor_case with tight 1.88x crop on lancet in velvet (J0827 £0 fix) |
| **#15** | P1 | `10_variolation` | `1:07.71–1:14.08` | `6.38` | `153` | `10_variolation_t1.mp4` | `0.00` | `1.00×` | `—` | KEEP Flow Quality t1 (J0352 Chief KEEP) |
| **#16** | P1 | `10b_milder` | `1:14.08–1:20.04` | `5.96` | `143` | `10b_milder_t1.mp4` | `0.00` | `1.50×` | `p1_variolation` | KEEP Flow Fast t1 (J0352 Chief KEEP) |
| **#17** | P1 | `10c_doors_close` | `1:20.04–1:26.25` | `6.21` | `149` | `10c_doors_close_t1.mp4` | `0.00` | `1.50×` | `—` | KEEP Flow Fast t1 (J0352 Chief KEEP) |
| **#18** | P1 | `11_mother_window` | `1:26.25–1:32.92` | `6.67` | `160` | `11_mother_window_t1.mp4` | `0.00` | `1.61×` | `—` | KEEP Flow Fast t1 (J0352 Chief KEEP) |
| **#19** | P1 | `11b_child_cot` | `1:32.92–1:36.46` | `3.54` | `85` | `11b_child_cot_t1.mp4` | `0.00` | `1.50×` | `—` | KEEP Flow Fast t1 (J0352 Chief KEEP) |
| **#20** | P1 | `12_farm_gate` | `1:36.46–1:40.83` | `4.38` | `105` | `12_farm_gate_t1.mp4` | `0.00` | `1.50×` | `—` | KEEP Flow Fast t1 (J0352 Chief KEEP) |
| **#21** | P2 | `01_milking_dawn` | `1:40.83–1:48.08` | `7.25` | `174` | `01_milking_dawn_t1.mp4` | `0.00` | `1.00×` | `p2_ch, p2_cowpox` | KEEP Flow Quality t1 (J0352 Chief KEEP) |
| **#22** | P2 | `02_healed_hand` | `1:48.08–1:54.87` | `6.79` | `163` | `02_healed_hand_t1.mp4` | `0.00` | `1.00×` | `p2_mild` | KEEP Flow Quality t1 (J0352 Chief KEEP) |
| **#23** | P2 | `02b_well_again` | `1:54.87–2:00.33` | `5.46` | `131` | `02b_well_again_t1.mp4` | `0.00` | `1.50×` | `—` | KEEP Flow Fast t1 (J0352 Chief KEEP) |
| **#24** | P2 | `04_village_a` | `2:00.33–2:04.83` | `4.50` | `108` | `04_village_a_t1.mp4` | `0.00` | `1.50×` | `—` | KEEP Flow Fast t1 (J0352 Chief KEEP) |
| **#25** | P2 | `02c_laughs` | `2:04.83–2:10.08` | `5.25` | `126` | `02c_laughs_t1.mp4` | `0.00` | `1.50×` | `—` | KEEP Flow Fast t1 (J0352 Chief KEEP) |
| **#26** | P2 | `03a_cap_and_pail` | `2:10.08–2:16.33` | `6.25` | `150` | `03a_cap_and_pail_t1.mp4` | `0.00` | `1.50×` | `—` | KEEP Flow Fast t1 (J0352 Chief KEEP) |
| **#27** | P2 | `03_market_walk` | `2:16.33–2:22.54` | `6.21` | `149` | `03_market_walk_t1.mp4` | `0.00` | `1.50×` | `p2_never` | KEEP Flow Fast t1 (J0352 Chief KEEP) |
| **#28** | P2 | `05_village_b` | `2:22.54–2:27.58` | `5.04` | `121` | `05_village_b_t1.mp4` | `0.00` | `1.50×` | `—` | KEEP Flow Fast t1 (J0352 Chief KEEP) |
| **#29** | P2 | `05b_gate_again` | `2:27.58–2:30.67` | `3.08` | `74` | `12_farm_gate_t1.mp4` | `4.84` | `1.00×` | `—` | REUSE window 4.84-7.90 s of P1:12_farm_gate |
| **#30** | P2 | `06_jesty_family` | `2:30.67–2:35.42` | `4.75` | `114` | `06_jesty_family_t1.mp4` | `0.00` | `1.00×` | `p2_who_jesty` | KEEP Flow Quality t1 (J0352 Chief KEEP) |
| **#31** | P2 | `06b_jesty_hands` | `2:35.42–2:41.75` | `6.33` | `152` | `06b_jesty_hands_t1.mp4` | `0.00` | `1.50×` | `p2_when_1774` | KEEP Flow Fast t1 (J0352 Chief KEEP) |
| **#32** | P2 | `07_jesty_table` | `2:41.75–2:48.71` | `6.96` | `167` | `07_jesty_table_t1.mp4` | `0.00` | `1.50×` | `—` | KEEP Flow Fast t1 (J0352 Chief KEEP) |
| **#33** | P2 | `08a_berkeley` | `2:48.71–2:53.75` | `5.04` | `121` | `08a_berkeley_t1.mp4` | `0.00` | `1.50×` | `p2_when_berkeley` | KEEP Flow Fast t1 (J0352 Chief KEEP) |
| **#34** | P2 | `08_jenner_window` | `2:53.75–3:00.87` | `7.12` | `171` | `08_jenner_window_t1.mp4` | `0.00` | `1.00×` | `p2_who_jenner` | KEEP Flow Quality t1 (J0352 Chief KEEP) |
| **#35** | P2 | `09_cuckoo` | `3:00.87–3:03.50` | `2.62` | `63` | `09_cuckoo_t1.mp4` | `0.00` | `1.50×` | `—` | KEEP Flow Fast t1 (J0352 Chief KEEP) |
| **#36** | P2 | `10_balloon` | `3:03.50–3:10.21` | `6.71` | `161` | `10_balloon_t1.mp4` | `0.00` | `1.00×` | `—` | KEEP Flow Quality t1 (J0352 Chief KEEP) |
| **#37** | P2 | `10b_pail_on_desk` | `3:10.21–3:15.21` | `5.00` | `120` | `10b_pail_on_desk_t1.mp4` | `0.00` | `1.50×` | `—` | KEEP Flow Fast t1 (J0352 Chief KEEP) |
| **#38** | P2 | `11_young_jenner` | `3:15.21–3:22.75` | `7.54` | `181` | `11_young_jenner_t1.mp4` | `0.00` | `1.50×` | `—` | KEEP Flow Fast t1 (J0352 Chief KEEP) |
| **#39** | P2 | `12_hunter_letter` | `3:22.75–3:29.96` | `7.21` | `173` | `12_hunter_letter_t1.mp4` | `0.00` | `1.50×` | `p2_who_hunter` | KEEP Flow Fast t1 (J0352 Chief KEEP) |
| **#40** | P2 | `12b_try_it` | `3:29.96–3:37.37` | `7.42` | `178` | `12b_try_it_t1.mp4` | `0.00` | `1.50×` | `p2_try_exp` | KEEP Flow Fast t1 (J0352 Chief KEEP) |
| **#41** | P2 | `13_casebook` | `3:37.37–3:44.79` | `7.42` | `178` | `13_casebook_t1.mp4` | `0.00` | `1.50×` | `—` | KEEP Flow Fast t1 (J0352 Chief KEEP) |
| **#42** | P2 | `14_explorer_stool` | `3:44.79–3:50.46` | `5.67` | `136` | `14_explorer_stool_t1.mp4` | `0.00` | `1.00×` | `—` | KEEP Flow Quality t1 (J0352 Chief KEEP) |
| **#43** | P3 | `01a_garden_path` | `3:50.46–3:54.79` | `4.33` | `104` | `01a_garden_path_t1.mp4` | `0.00` | `1.50×` | `p3_ch` | KEEP Flow Fast t1 (J0352 Chief KEEP) |
| **#44** | P3 | `01_sarah_nelmes` | `3:54.79–3:59.96` | `5.17` | `124` | `01_sarah_nelmes_t1.mp4` | `0.00` | `1.00×` | `p3_who_sarah` | KEEP Flow Quality t1 (J0352 Chief KEEP) |
| **#45** | P3 | `02_cow_from_lane` | `3:59.96–4:07.67` | `7.71` | `185` | `02_cow_from_lane_t1.mp4` | `0.00` | `1.50×` | `p3_blossom` | KEEP Flow Fast t1 (J0352 Chief KEEP) |
| **#46** | P3 | `03_phipps_stool` | `4:07.67–4:12.08` | `4.42` | `106` | `03_phipps_stool_t1.mp4` | `0.00` | `1.00×` | `—` | KEEP Flow Quality t1 (J0352 Chief KEEP) |
| **#47** | P3 | `03b_lancet_case` | `4:12.08–4:15.83` | `3.75` | `90` | `03b_lancet_case_t1.mp4` | `0.00` | `1.50×` | `p3_when_may14` | KEEP Flow Fast t1 (J0352 Chief KEEP) |
| **#48** | P3 | `04_lancet_touch` | `4:15.83–4:22.42` | `6.58` | `158` | `04_lancet_touch_t1.mp4` | `0.00` | `1.00×` | `p3_who_phipps` | KEEP Flow Quality t1 (J0352 Chief KEEP) |
| **#49** | P3 | `05_quill_writes` | `4:22.42–4:29.79` | `7.38` | `177` | `05_quill_writes_t1.mp4` | `0.00` | `1.50×` | `p3_quill_date` | KEEP Flow Fast t1 (J0352 Chief KEEP) |
| **#50** | P3 | `05b_week_passes` | `4:29.79–4:33.12` | `3.33` | `80` | `05b_week_passes_t1.mp4` | `0.00` | `1.50×` | `—` | KEEP Flow Fast t1 (J0352 Chief KEEP) |
| **#51** | P3 | `06_mild_fever` | `4:33.12–4:38.04` | `4.92` | `118` | `06_mild_fever_t1.mp4` | `0.00` | `1.50×` | `p3_mild_fever` | KEEP Flow Fast t1 (J0352 Chief KEEP) |
| **#52** | P3 | `07_playing_garden` | `4:38.04–4:43.58` | `5.54` | `133` | `07_playing_garden_t1.mp4` | `0.00` | `1.50×` | `—` | KEEP Flow Fast t1 (J0352 Chief KEEP) |
| **#53** | P3 | `08_jenner_thinks` | `4:43.58–4:48.17` | `4.58` | `110` | `08_jenner_thinks_t1.mp4` | `0.00` | `1.50×` | `—` | KEEP Flow Fast t1 (J0352 Chief KEEP) |
| **#54** | P3 | `08b_uneasy_hand` | `4:48.17–4:53.37` | `5.21` | `125` | `08b_uneasy_hand_t1.mp4` | `0.00` | `1.50×` | `—` | KEEP Flow Fast t1 (J0352 Chief KEEP) |
| **#55** | P3 | `08c_map_again` | `4:53.37–5:00.33` | `6.96` | `167` | `code_graphic_007_p3_08c_map_again.mp4` | `0.00` | `1.00×` | `—` | Dedicated £0 code graphic reuse render of P1:07_map_shadows |
| **#56** | P3 | `09_casebook_open` | `5:00.33–5:06.00` | `5.67` | `136` | `13_casebook_t1.mp4` | `1.10` | `1.00×` | `—` | REUSE window 1.10-6.76 s of P2:13_casebook |
| **#57** | P3 | `09b_phipps_again` | `5:06.00–5:09.21` | `3.21` | `77` | `03_phipps_stool_t1.mp4` | `4.68` | `1.00×` | `—` | REUSE window 4.68-7.90 s of P3:03_phipps_stool |
| **#58** | P4 | `01_page_turns` | `5:09.21–5:12.08` | `2.88` | `69` | `05_quill_writes_t1.mp4` | `2.00` | `1.00×` | `p4_ch, p4_when_july1` | REUSE window 2.00-4.88 s of P3:05_quill_writes |
| **#59** | P4 | `02_variolation_calm` | `5:12.08–5:18.21` | `6.12` | `147` | `02_variolation_calm_t1.mp4` | `0.00` | `1.00×` | `—` | KEEP Flow Quality t1 (J0352 Chief KEEP) |
| **#60** | P4 | `03_waiting` | `5:18.21–5:23.33` | `5.12` | `123` | `03_waiting_t1.mp4` | `0.00` | `1.00×` | `p4_waiting` | KEEP Flow Quality t1 (J0352 Chief KEEP) |
| **#61** | P4 | `04_day_one` | `5:23.33–5:25.92` | `2.58` | `62` | `04_day_one_t1.mp4` | `0.00` | `1.50×` | `p4_day_one` | KEEP Flow Fast t1 (J0352 Chief KEEP) |
| **#62** | P4 | `05_days_pass` | `5:25.92–5:29.17` | `3.25` | `78` | `05_days_pass_t1.mp4` | `4.50` | `1.50×` | `p4_one_week` | KEEP Flow Fast t1 trimmed to clean back half 4.50-7.76 s per J0820 brief |
| **#63** | P4 | `06_line_underlined` | `5:29.17–5:32.75` | `3.58` | `86` | `06_line_underlined_t1.mp4` | `0.00` | `1.50×` | `p4_no_disease` | KEEP Flow Fast t1 (J0352 Chief KEEP) |
| **#64** | P4 | `06b_still_nothing` | `5:32.75–5:38.00` | `5.25` | `126` | `06b_still_nothing_t1.mp4` | `0.00` | `1.50×` | `—` | KEEP Flow Fast t1 (J0352 Chief KEEP) |
| **#65** | P4 | `07_jesty_again` | `5:38.00–5:44.75` | `6.75` | `162` | `06_jesty_family_t1.mp4` | `1.14` | `1.00×` | `p4_22_years` | REUSE window 1.14-7.90 s of P2:06_jesty_family |
| **#66** | P4 | `07b_quill_again` | `5:44.75–5:48.54` | `3.79` | `91` | `05_quill_writes_t1.mp4` | `4.14` | `1.00×` | `—` | REUSE window 4.14-7.90 s of P3:05_quill_writes |
| **#67** | P4 | `07c_cases_again` | `5:48.54–5:54.21` | `5.67` | `136` | `13_casebook_t1.mp4` | `2.22` | `1.00×` | `—` | REUSE window 2.22-7.90 s of P2:13_casebook |
| **#68** | P4 | `08_soho_press` | `5:54.21–5:59.54` | `5.33` | `128` | `08_soho_press_t1.mp4` | `0.00` | `1.50×` | `p4_soho_1798` | KEEP Flow Fast t1 (J0352 Chief KEEP) |
| **#69** | P4 | `08b_title_page` | `5:59.54–6:04.29` | `4.75` | `114` | `archive_007_p4_08b_title_page_v01.mp4` | `0.00` | `1.00×` | `p4_inquiry_credit` | Public domain archive scan (£0, archive_007_p4_08b_title_page_v01.mp4) |
| **#70** | P4 | `08c_cow_again` | `6:04.29–6:07.58` | `3.29` | `79` | `01_cow_meadow_t1.mp4` | `4.60` | `1.00×` | `—` | REUSE window 4.60-7.90 s of P1:01_cow_meadow |
| **#71** | P4 | `12_explorer_press` | `6:07.58–6:14.04` | `6.46` | `155` | `12_explorer_press_t1.mp4` | `0.00` | `1.00×` | `—` | KEEP Flow Quality t1 (J0352 Chief KEEP) |
| **#72** | P4 | `08d_doctors_scoff` | `6:14.04–6:18.21` | `4.17` | `100` | `08d_doctors_scoff_t1.mp4` | `0.00` | `1.50×` | `—` | KEEP Flow Fast t1 (J0352 Chief KEEP) |
| **#73** | P4 | `09_satire` | `6:18.21–6:22.67` | `4.46` | `107` | `archive_007_p4_09_satire_v01.mp4` | `0.00` | `1.00×` | `p4_gillray_credit` | Public domain archive scan (£0, archive_007_p4_09_satire_v01.mp4) |
| **#74** | P4 | `09b_boy_well` | `6:22.67–6:25.87` | `3.21` | `77` | `07_playing_garden_t1.mp4` | `4.68` | `1.00×` | `—` | REUSE window 4.68-7.90 s of P3:07_playing_garden |
| **#75** | P4 | `10a_packets` | `6:25.87–6:29.37` | `3.50` | `84` | `10a_packets_t1.mp4` | `0.00` | `1.50×` | `—` | KEEP Flow Fast t1 (J0352 Chief KEEP) |
| **#76** | P4 | `10_garden_hut` | `6:29.37–6:35.54` | `6.17` | `148` | `10_garden_hut_t1.mp4` | `0.00` | `1.50×` | `p4_temple` | KEEP Flow Fast t1 (J0352 Chief KEEP) |
| **#77** | P4 | `11_news_spreads` | `6:35.54–6:41.96` | `6.42` | `154` | `code_graphic_007_p4_11_news_spreads.mp4` | `0.00` | `1.00×` | `p4_news_spreads` | Code graphic v01 (£0, code_graphic_007_p4_11_news_spreads.mp4) |
| **#78** | P5 | `01_pasteur_1881` | `6:41.96–6:49.87` | `7.92` | `190` | `01_pasteur_1881_t1.mp4` | `0.00` | `1.00×` | `p5_ch, p5_who_pasteur, p5_vaccine_board` | KEEP Flow Quality t1 (J0352 Chief KEEP) |
| **#79** | P5 | `02_cow_again` | `6:49.87–6:56.92` | `7.04` | `169` | `01_cow_meadow_t1.mp4` | `0.84` | `1.00×` | `—` | REUSE window 0.84-7.90 s of P1:01_cow_meadow |
| **#80** | P5 | `09_meadow_golden` | `6:56.92–7:02.50` | `5.58` | `134` | `09_meadow_golden_t1.mp4` | `0.00` | `1.00×` | `p5_vacca_glow` | KEEP Flow Quality t1 (J0352 Chief KEEP) |
| **#81** | P5 | `02b_news_again` | `7:02.50–7:05.71` | `3.21` | `77` | `code_graphic_007_p5_02b_news_again.mp4` | `0.00` | `1.00×` | `—` | Dedicated £0 code graphic reuse render of P4:11_news_spreads |
| **#82** | P5 | `04_health_workers` | `7:05.71–7:09.54` | `3.83` | `92` | `04_health_workers_t1.mp4` | `0.00` | `1.00×` | `—` | KEEP Flow Quality t1 (J0352 Chief KEEP) |
| **#83** | P5 | `05_kit_opens` | `7:09.54–7:13.67` | `4.12` | `99` | `05_kit_opens_t1.mp4` | `0.00` | `1.50×` | `—` | KEEP Flow Fast t1 (J0352 Chief KEEP) |
| **#84** | P5 | `03_globe_lights` | `7:13.67–7:17.17` | `3.50` | `84` | `03_globe_lights_t1.mp4` | `0.00` | `1.00×` | `p5_last_cases` | KEEP Flow Quality t1 (J0352 Chief KEEP) |
| **#85** | P5 | `06_assembly_1980` | `7:17.17–7:23.33` | `6.17` | `148` | `06_assembly_1980_t1.mp4` | `0.00` | `1.00×` | `p5_may_1980, p5_smallpox_gone` | KEEP Flow Quality t1 (J0352 Chief KEEP) |
| **#86** | P5 | `06b_churchyard_again` | `7:23.33–7:27.50` | `4.17` | `100` | `09_churchyard_t1.mp4` | `3.74` | `1.00×` | `p5_300m` | REUSE window 3.74-7.90 s of P1:09_churchyard |
| **#87** | P5 | `06c_assembly_again` | `7:27.50–7:31.62` | `4.12` | `99` | `04_health_workers_t1.mp4` | `3.83` | `1.18×` | `—` | REUSE strictly unused tail 3.833-7.958 s of P5:04_health_workers (0.00 s overlap, 1.18x framing, J0827 £0 fix) |
| **#88** | P5 | `06d_assembly_front_row` | `7:31.62–7:34.54` | `2.92` | `70` | `06_assembly_1980_t1.mp4` | `5.08` | `1.38×` | `—` | REUSE tail 5.083-8.000 s of P5:06_assembly_1980 with 1.38x push-in crop on clapping front row (J0827 £0 fix) |
| **#89** | P5 | `08_body_learns` | `7:34.54–7:40.62` | `6.08` | `146` | `code_graphic_007_p5_08_body_learns.mp4` | `0.00` | `1.00×` | `—` | Code graphic v01 (£0, code_graphic_007_p5_08_body_learns.mp4) |
| **#90** | P5 | `07_childs_arm` | `7:40.62–7:46.79` | `6.17` | `148` | `07_childs_arm_t1.mp4` | `0.00` | `1.00×` | `—` | KEEP Flow Quality t1 (J0352 Chief KEEP) |
| **#91** | P5 | `07b_kit_again` | `7:46.79–7:52.00` | `5.21` | `125` | `05_kit_opens_t1.mp4` | `2.68` | `1.00×` | `—` | REUSE window 2.68-7.90 s of P5:05_kit_opens |
| **#92** | P5 | `07c_playground` | `7:52.00–7:58.25` | `6.25` | `150` | `07c_playground_t1.mp4` | `0.00` | `1.50×` | `—` | KEEP Flow Fast t1 (J0352 Chief KEEP) |
| **#93** | P5 | `10_history_book` | `7:58.25–8:02.87` | `4.62` | `111` | `10_history_book_t1.mp4` | `0.00` | `1.50×` | `—` | KEEP Flow Fast t1 (J0352 Chief KEEP) |
| **#94** | P5 | `11_table_three_again` | `8:02.87–8:08.58` | `5.71` | `137` | `03_table_three_t1.mp4` | `2.18` | `1.00×` | `—` | REUSE window 2.18-7.90 s of P1:03_table_three |
| **#95** | P5 | `13_explorer_meadow` | `8:08.58–8:15.33` | `6.75` | `162` | `13_explorer_meadow_t1.mp4` | `0.00` | `1.00×` | `—` | KEEP Flow Quality t1 (J0352 Chief KEEP) |
| **#96** | P5 | `11b_storm_builds` | `8:15.33–8:20.08` | `4.75` | `114` | `11b_storm_builds_t1.mp4` | `0.00` | `1.50×` | `—` | KEEP Flow Fast t1 (J0352 Chief KEEP) |
| **#97** | P5 | `12_kite_storm` | `8:20.08–8:25.12` | `5.04` | `121` | `12_kite_storm_t1.mp4` | `0.00` | `1.00×` | `—` | KEEP Flow Quality t1 (J0352 Chief KEEP) |

---

## 4. Gate Outputs (`picture_qa.py` & `polish_gate.py`)

### `picture_qa.py` Output

```text
WARN   0:15 row 03_table_three 03_table_three_t1.mp4: low detail: edge density 0.0154 < film p5 0.0224
WARN   4:26 row 05_quill_writes 05_quill_writes_t1.mp4: low detail: edge density 0.0184 < film p5 0.0224
WARN   4:51 row 08b_uneasy_hand 08b_uneasy_hand_t1.mp4: low detail: edge density 0.0223 < film p5 0.0224
WARN   5:11 row 01_page_turns 05_quill_writes_t1.mp4: low detail: edge density 0.0152 < film p5 0.0224
WARN   5:47 row 07b_quill_again 05_quill_writes_t1.mp4: low detail: edge density 0.0183 < film p5 0.0224
picture QA PASS: 0 of 97 cuts fail, 5 to look at -> /private/tmp/j0827-hos-wt/02_Video-Projects/007_The-First-Vaccine/07_Edit-Project/_desk/007/full_join_v01/PICTURE_QA.md, /private/tmp/j0827-hos-wt/02_Video-Projects/007_The-First-Vaccine/07_Edit-Project/_desk/007/full_join_v01/picture_qa_review.jpg
```

### `polish_gate.py` Output

```text
01_cow_meadow     2.1s 01_cow_meadow_t1.mp4         ok
02_doctor_case     7.9s 02_doctor_case_t1.mp4        ok
03_table_three    15.3s 03_table_three_t1.mp4        WARN low detail: edge density 0.0154 < film p5 0.0224
03b_globe_tease    21.1s 03_globe_lights_t1.mp4       ok
04_church_dusk    26.2s 04_church_dusk_t1.mp4        ok
07_map_shadows    32.2s code_graphic_007_p1_07_map_s ok
07b_three_in_ten    37.1s 07b_three_in_ten_t1.mp4      ok
07c_scarred    41.6s 07c_scarred_t1.mp4           ok
05_quiet_lane    46.0s 05_quiet_lane_t1.mp4         ok
06_shuttered_house    50.0s 06_shuttered_house_t1.mp4    ok
08_bell_tower    54.0s 08_bell_tower_t1.mp4         ok
09_churchyard    57.5s 09_churchyard_t1.mp4         ok
09b_counted    61.4s 09b_counted_t1.mp4           ok
09c_case_again    65.5s 02_doctor_case_t1.mp4        ok
10_variolation    70.9s 10_variolation_t1.mp4        ok
10b_milder    77.1s 10b_milder_t1.mp4            ok
10c_doors_close    83.2s 10c_doors_close_t1.mp4       ok
11_mother_window    89.6s 11_mother_window_t1.mp4      ok (reviewed_ok: split panel: vertical seam at 0.536, vertical seam at 0.578, vertical seam at 0.601)
11b_child_cot    94.7s 11b_child_cot_t1.mp4         ok
12_farm_gate    98.7s 12_farm_gate_t1.mp4          ok
01_milking_dawn   104.5s 01_milking_dawn_t1.mp4       ok
02_healed_hand   111.5s 02_healed_hand_t1.mp4        ok
02b_well_again   117.6s 02b_well_again_t1.mp4        ok
04_village_a   122.6s 04_village_a_t1.mp4          ok
02c_laughs   127.5s 02c_laughs_t1.mp4            ok
03a_cap_and_pail   133.2s 03a_cap_and_pail_t1.mp4      ok
03_market_walk   139.4s 03_market_walk_t1.mp4        ok
05_village_b   145.1s 05_village_b_t1.mp4          ok
05b_gate_again   149.1s 12_farm_gate_t1.mp4          ok
06_jesty_family   153.0s 06_jesty_family_t1.mp4       ok
06b_jesty_hands   158.6s 06b_jesty_hands_t1.mp4       ok
07_jesty_table   165.2s 07_jesty_table_t1.mp4        ok
08a_berkeley   171.2s 08a_berkeley_t1.mp4          ok
08_jenner_window   177.3s 08_jenner_window_t1.mp4      ok
09_cuckoo   182.2s 09_cuckoo_t1.mp4             ok
10_balloon   186.8s 10_balloon_t1.mp4            ok
10b_pail_on_desk   192.7s 10b_pail_on_desk_t1.mp4      ok
11_young_jenner   199.0s 11_young_jenner_t1.mp4       ok
12_hunter_letter   206.3s 12_hunter_letter_t1.mp4      ok
12b_try_it   213.7s 12b_try_it_t1.mp4            ok
13_casebook   221.1s 13_casebook_t1.mp4           ok
14_explorer_stool   227.6s 14_explorer_stool_t1.mp4     ok
01a_garden_path   232.6s 01a_garden_path_t1.mp4       ok
01_sarah_nelmes   237.4s 01_sarah_nelmes_t1.mp4       ok
02_cow_from_lane   243.8s 02_cow_from_lane_t1.mp4      ok
03_phipps_stool   249.9s 03_phipps_stool_t1.mp4       ok
03b_lancet_case   254.0s 03b_lancet_case_t1.mp4       ok
04_lancet_touch   259.1s 04_lancet_touch_t1.mp4       ok
05_quill_writes   266.1s 05_quill_writes_t1.mp4       WARN low detail: edge density 0.0184 < film p5 0.0224
05b_week_passes   271.5s 05b_week_passes_t1.mp4       ok
06_mild_fever   275.6s 06_mild_fever_t1.mp4         ok
07_playing_garden   280.8s 07_playing_garden_t1.mp4     ok
08_jenner_thinks   285.9s 08_jenner_thinks_t1.mp4      ok
08b_uneasy_hand   290.8s 08b_uneasy_hand_t1.mp4       WARN low detail: edge density 0.0223 < film p5 0.0224
08c_map_again   296.9s code_graphic_007_p3_08c_map_ ok
09_casebook_open   303.2s 13_casebook_t1.mp4           ok
09b_phipps_again   307.6s 03_phipps_stool_t1.mp4       ok
01_page_turns   310.6s 05_quill_writes_t1.mp4       WARN low detail: edge density 0.0152 < film p5 0.0224
02_variolation_calm   315.1s 02_variolation_calm_t1.mp4   ok
03_waiting   320.8s 03_waiting_t1.mp4            ok
04_day_one   324.6s 04_day_one_t1.mp4            ok
05_days_pass   327.5s 05_days_pass_t1.mp4          ok
06_line_underlined   331.0s 06_line_underlined_t1.mp4    ok
06b_still_nothing   335.4s 06b_still_nothing_t1.mp4     ok
07_jesty_again   341.4s 06_jesty_family_t1.mp4       ok
07b_quill_again   346.6s 05_quill_writes_t1.mp4       WARN low detail: edge density 0.0183 < film p5 0.0224
07c_cases_again   351.4s 13_casebook_t1.mp4           ok
08_soho_press   356.9s 08_soho_press_t1.mp4         ok
08b_title_page   361.9s archive_007_p4_08b_title_pag ok
08c_cow_again   365.9s 01_cow_meadow_t1.mp4         ok
12_explorer_press   370.8s 12_explorer_press_t1.mp4     ok
08d_doctors_scoff   376.1s 08d_doctors_scoff_t1.mp4     ok
09_satire   380.4s archive_007_p4_09_satire_v01 ok
09b_boy_well   384.3s 07_playing_garden_t1.mp4     ok
10a_packets   387.6s 10a_packets_t1.mp4           ok
10_garden_hut   392.5s 10_garden_hut_t1.mp4         ok
11_news_spreads   398.8s code_graphic_007_p4_11_news_ ok
01_pasteur_1881   405.9s 01_pasteur_1881_t1.mp4       ok
02_cow_again   413.4s 01_cow_meadow_t1.mp4         ok
09_meadow_golden   419.7s 09_meadow_golden_t1.mp4      ok
02b_news_again   424.1s code_graphic_007_p5_02b_news ok
04_health_workers   427.6s 04_health_workers_t1.mp4     ok
05_kit_opens   431.6s 05_kit_opens_t1.mp4          ok
03_globe_lights   435.4s 03_globe_lights_t1.mp4       ok
06_assembly_1980   440.2s 06_assembly_1980_t1.mp4      ok
06b_churchyard_again   445.4s 09_churchyard_t1.mp4         ok
06c_assembly_again   449.6s 04_health_workers_t1.mp4     ok
06d_assembly_front_row   453.1s 06_assembly_1980_t1.mp4      ok
08_body_learns   457.6s code_graphic_007_p5_08_body_ ok
07_childs_arm   463.7s 07_childs_arm_t1.mp4         ok
07b_kit_again   469.4s 05_kit_opens_t1.mp4          ok
07c_playground   475.1s 07c_playground_t1.mp4        ok
10_history_book   480.6s 10_history_book_t1.mp4       ok
11_table_three_again   485.7s 03_table_three_t1.mp4        ok
13_explorer_meadow   492.0s 13_explorer_meadow_t1.mp4    ok
11b_storm_builds   497.7s 11b_storm_builds_t1.mp4      ok
12_kite_storm   502.6s 12_kite_storm_t1.mp4         ok
polish gate PASS: 0 of 97 rows failed, 5 to look at -> /private/tmp/j0827-hos-wt/02_Video-Projects/007_The-First-Vaccine/07_Edit-Project/_desk/007/full_join_v01/polish_gate.json
```
