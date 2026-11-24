# Production status — 127 Wright Brothers First Flight: The 1901 Wind Tunnel

| Field | Value |
|---|---|
| Slug | `127_Wright-Brothers-How-Do-Airplanes-Fly-Wind-Tunnel` |
| Channel | `@HistoryOfScienceYT` only |
| Topic | **Rule-E GO (`97.2 / 100`, `J3264`, `2026-11-21`)** — Cluster 4 Lead Film 4 of Ben's approved `hos-search-2027-01` accelerated December test cohort (`J3495` / PR `#1239`). Waits behind `HOS:136` and `HOS:137` under Rule G before any VO or picture spend (`£0.00` spent). |
| Primary Title (Arm A) | *Wright Brothers First Flight: The 1901 Wind Tunnel* (`50 chars ≤ 50`, `0` exact collisions; exact `J3224` Cluster 4 Lead Film query `"wright brothers first flight"`) |
| Title B (T&C · Plan Title) | *Wright Brothers First Flight: The 1901 Wind Tunnel That Solved Lift* (`67 chars ≤ 70`, `0` exact collisions verified `2026-11-24`) |
| Title C (T&C · Physics Lead) | *How Do Airplanes Fly? (The 1901 Wind Tunnel)* (`44 chars ≤ 50`, `0` exact collisions) |
| Thumbnails (Draft Concepts) | **Thumb A (Primary):** `50% TOO HIGH` (gold on `50%`, 1901 wooden wind-tunnel cutaway + tiny curved steel wing on hacksaw-blade balance, Explorer small lower-left) · **Thumb B (T&C):** `200 TINY WINGS` (gold on `200`, Dayton bench rows of miniature curved steel test wings beside tunnel mouth, Explorer small lower-left) — unrendered; `style_sheet.py` & `thumb_preview.py` required before Ben's watch |
| Neighbour gate | **PASS (`2026-11-21`)** — `8` raw / `6` aviation / **`5` strictly on-topic** education videos `≥1M` views (`TED-Ed/TED: yes`, led by `TED-Ed` ★ `2.57M` `p4VHMsIuPmk`, `minutephysics` `2.48M` `Gg0TXNXgz-w`, `SciShow Kids` `1.75M` `VLpSxHwfU04`, `Veritasium` `1.66M` `aFO4PBolwFg`, `Simple History` `1.41M` `YDlk4Ky_ahs`, plus `Real Engineering` `384,056` and `SciShow` `293,525`) |
| Public search & collisions | **PASS (`2026-11-21` & `2026-11-24`)** — `11_Upload-Package/evidence_2026-11-21_public_search.json` + `evidence_2026-11-24_plan_title_search.json` (`4/4` core search phrases autocomplete `yes`; `0` exact title collisions across Titles A/B/C and Shorts S01/S02) |
| Pre-build vidIQ audit | `11_Upload-Package/PRE_BUILD_VIDIQ_AUDIT.md` & `PACKAGE_FIRST_SCORING_v01.md` completed (`J3504`, `2026-11-24`; per-title vidIQ app numeric scores pending active WIP) |
| Facts / `SOURCES.md` | **DRAFTED (`J3504`, `2026-11-24`) — PENDING INDEPENDENT `facts` LANE (`gemini-agy`)** (`01_Script/SOURCES.md` + `01_Script/FACT_NOTES_v01.md`: 17 claim rows backed by live NASA GRC, Smithsonian NASM, and NPS institutional quotes + honestly labelled secondary lifespans) |
| Script review | **PASS (`93.6 / 100`, `J3504`, `2026-11-24`)** — `01_Script/wright_brothers_wind_tunnel_script_master_v01.md` (`1,239` spoken words, `8.3` min, 5 parts, `8/8` structure gates, `7 DATA+SCALE`, `5 WHO`, `12 WHEN`, `4 FACT`, `2 EXPLORER ACTS`, `0` labels/facts over 4 words; pending independent `facts` audit & Chief lock) |
| Episode gate | **PASS (`9 / 9 OK`, `J3504`, `2026-11-24`)** — mechanical gate pass only; Chief lock & Rule G WIP slot required before any VO or picture spend |
| VO | pending (Ben Orbit Narrator; `£0.00` spent) |
| Picture | pending (Flow Veo 3.1, plate library; `£0.00` spent) |
| Runtime target | 7–9 min, 5 parts |
| Air | Target **Thu 31 Dec 2026, 18:00 London** (normal publish, no Premiere; slides one week if not ready; Ben's watch by Mon 28 Dec) |
| Shorts | 2 standalone `16–19 s` search-question Shorts drafted in `10_Shorts/SHORTS_SCRIPTS_v01.md` (Ben 19 Nov 3D cartoon house rules): **S01** *Why Did the Wright Brothers Build a Wind Tunnel?* (`48c`, `42w` ≈ `17.6 s`, Sat 2 Jan 11:30), **S02** *How Did the Wright Brothers Steer the First Plane?* (`50c`, `42w` ≈ `17.6 s`, Fri 1 Jan 11:30) — `0` collisions, pending `facts` & Chief lock |

## `J3504` Package-First & Script Draft Gate Outputs (`2026-11-24`)

- `npm run review:script -- --file ../02_Video-Projects/127_Wright-Brothers-How-Do-Airplanes-Fly-Wind-Tunnel/01_Script/wright_brothers_wind_tunnel_script_master_v01.md`:
  ```text
  # wright_brothers_wind_tunnel_script_master_v01.md

  **Decision:** PASS · **Score:** 93.6 / 100

  | Dimension | Score |
  |---|---:|
  | hook | 9.5 |
  | curiosity | 9.5 |
  | storytelling | 9 |
  | scientificAccuracy | 10 |
  | emotion | 9.6 |
  | escalation | 8.8 |
  | retentionPotential | 9 |
  | searchPotential | 9.1 |
  | visualOpportunities | 9.5 |
  | narrationFlow | 9.6 |

  Words: 1239 · Est. min: 8.3 · Chapters: 4

  - [info] overall: Structure gates 8/8 — applied +1.05 completeness boost to supporting dimensions.
  - [info] overall: PASS 93.6/100 — proceed to VO after production checklist.
  ```
- `npm run gate:episode -- --project ../02_Video-Projects/127_Wright-Brothers-How-Do-Airplanes-Fly-Wind-Tunnel --script ../02_Video-Projects/127_Wright-Brothers-How-Do-Airplanes-Fly-Wind-Tunnel/01_Script/wright_brothers_wind_tunnel_script_master_v01.md`:
  ```text
  # Episode gate — 127_Wright-Brothers-How-Do-Airplanes-Fly-Wind-Tunnel

  **Decision:** PASS — VO / Gemini Veo allowed

  project_dir OK | prebuild_vidiq OK | script_file OK | script_review OK (93.6/90) |
  explorer_acts OK (2) | visual_must OK (29) | teach OK (5) | chapters OK (4) |
  production_checklist OK
  ```
- `bash 00_Brand/Channel-Setup/tools/check_all.sh 02_Video-Projects/127_Wright-Brothers-How-Do-Airplanes-Fly-Wind-Tunnel`:
  ```text
  -- durable desk handoffs: PASS
  -- email ratchet: PASS
  -- no media: PASS
  -- status board in sync: PASS
  -- ElevenLabs guard tests: PASS
  -- vo_check word tests: PASS
  -- atempo check tests: PASS
  -- voice speed (atempo <= 1.06): PASS
  -- contract tests: PASS
  -- package-lint: PASS
  -- review:script wright_brothers_wind_tunnel_script_master_v01.md: PASS
  -- gate:episode: PASS
  ALL CHECKS PASS
  ```

## Rule-E Audit Evidence (`J3264`, `2026-11-21`)

- `neighbours.py` output (`11_Upload-Package/evidence_2026-11-21_neighbours.json`):
  ```text
  Words the top neighbours share: wright brothers, how do, do airplanes, airplanes fly, the wright
  TED-Ed/TED neighbour: yes
  Big neighbours (≥ 1,000,000 views): 8 (need 3)
  Neighbour gate (≥ 3 education videos with 1,000,000+ views): PASS
  Raw pull: 02_Video-Projects/127_Wright-Brothers-How-Do-Airplanes-Fly-Wind-Tunnel/11_Upload-Package/evidence_2026-11-21_neighbours.json
  ```
  *(Transparent filter: excluding `2` airplane-keyword false positives `dzrwnwOx0fw` riddle `7.65M` & `iKYHf22qVdM` airplane mode `4.21M`, and noting broader aviation `hd8tYiLSmn0` `2.52M`, leaves **`5` strictly on-topic `≥1M` education videos**, with `TED-Ed` ★ `#1` at `2,568,211` views.)*
- `public_search.py` outputs (`11_Upload-Package/evidence_2026-11-21_public_search.json` + `evidence_2026-11-24_plan_title_search.json`): `4/4` core search phrases autocomplete `yes`, `0` exact title collisions across Titles A/B/C and Shorts S01/S02.
- `J3264` script-stage guardrails resolved in `J3504` v01:
  1. Smeaton coefficient percentage fixed (`0.005` vs `0.0033` = `51.5%` / ~`50% TOO HIGH`, never `40%`; NASA modern derivation `0.00327`).
  2. Accurate aerodynamic lift physics (pressure difference + downward airflow deflection; explicitly debunks equal-transit-time myth via NASA GRC).
  3. 5-part (`7–9 min`, `1,239` words, `8.3` min) HOS structure with midpoint twist in Part 04.
  4. **Kill Devil Hills** distinguished from **Kitty Hawk**; all 5 `WHO` cards carry sourced lifespans and year-accurate roles.
  5. Primary Title Arm A (`50c`, `Wright Brothers First Flight: The 1901 Wind Tunnel`) paired with T&C Arm B (`67c`, verbatim plan title) and T&C Arm C (`44c`, `How Do Airplanes Fly? (The 1901 Wind Tunnel)`).

## Parts

| Part | Plate board | Latest cut | Status |
|---|---|---|---|
| 01 | `07_Edit-Project/parts/part-01_plates_v01.json` (template) | — | todo |
| 02 | — | — | todo |
| 03 | — | — | todo |
| 04 | — | — | todo |
| 05 | — | — | todo |

Keep this file current on `main`. A STOP (quota, auth, missing VO) is a line here, not an open branch.
