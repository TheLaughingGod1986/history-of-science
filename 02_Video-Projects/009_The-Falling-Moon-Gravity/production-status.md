# Production status — Gravity (the falling Moon)

| Field | Value |
|---|---|
| Slug | `009_The-Falling-Moon-Gravity` |
| Stage | **Picture Tranche 1 KEEP (57/57 Flow rows + 12 code graphics + 1 reuse = 70/90 rows)** (29 Oct 2026, J1192) |
| Script | PR #208 v01 · review **91.3** (may still be off main) |
| FACT_NOTES | Sourced from script new-claims; **7/7 hard-checks PASS**; Claude UNSIGNED |
| Neighbour gate | **PASS — 5 education ≥1M; TED-Ed yes** |
| Upload package | Manifest / description / tags / PRE_BUILD (UNSIGNED) / checklist scaffolded |
| Picture | **Tranche 1 minted & KEEP** (J1192, 29 Oct: 57/57 Flow rows = 26 Quality + 31 Fast, 3,170 cr vs 7,354 expected / 7,585 cap; live Flow 15,380 >= 3,000 buffer) + 12 £0 code graphics (J0342/J0383) + 1 reuse = **70/90 rows**. Tranche 2 (20 Quality rows, 5,180 expected) waits for ~12 Nov renewal. |
| VO | **LOCKED v01** (Chief KEEP, desk #180 comment 6101629662, 11 Oct). Retime 8:38.4 in `07_Edit-Project/VO_RETIME_v01.json`. |

## STOP

- Tranche 1 is complete (57/57 KEEP); tranche 2 (20 Quality rows, 5,180 expected) waits for the ~12 Nov AI Ultra renewal.
- Do not merge or close desk PR #180 from this work.
- Does **not** close #180.

## 24 Oct 2026 — J0909 (`J0899` Change 4): Gravity-apparatus search terms in description lines 1–2 and tags + Shorts VO & `J0383` teach-graphic alternation notes (Gemini covering)

- **Authority:** Chief PASS on `J0899` (`02_Video-Projects/_analytics/HOS_2026-10-24.md` §4 #4) and queue job `J0909`. `£0` spend, no live YouTube changes.
- **Applied to `11_Upload-Package/` and `10_Shorts/SHORTS_SCRIPTS_v02.md`:**
  1. **Gravity-apparatus search terms in description lines 1–2 and tags (`Descriptions/moon_long_description_v01.txt`, `Tags/moon_long_tags_v01.txt`, `PACKAGE_MANIFEST.json`, `PRE_BUILD_VIDIQ_AUDIT.md`):** Wove `"theory of gravity"`, `"how Newton proved gravity"`, and `"Cavendish torsion balance"` (from breakout neighbour `eyZEqSPeMwg`, `1.14M` views in 6.8h on 23–24 Oct, zero channel names) into lines 1–2 of `moon_long_description_v01.txt` (retaining `Moon`, `Newton`, `gravity` in the first 100 chars) and into `moon_long_tags_v01.txt` (8 tags total). Added `eyZEqSPeMwg` to `PACKAGE_MANIFEST.json` `neighbours.videos`.
  2. **Search-titled `v02` Shorts VO & `J0383` teach-graphic alternation (`LAUNCH_PLAN.md`, `10_Shorts/SHORTS_SCRIPTS_v02.md`, `PACKAGE_MANIFEST.json`):** Documented positive-question Shorts VO titles (*What Would Happen If the Moon Stopped Moving?* / *Why Doesn't the Moon Crash Into the Earth?*, *How Did Newton Discover Gravity?*) and alternating every `J0383`-verified parchment teach graphic in `0:00–0:30` and `1:00–2:00` with a moving 3D plate.
- **Package lint (`npm run lint:package -- --film 009`):** `PASS  02_Video-Projects/009_The-Falling-Moon-Gravity/11_Upload-Package/PACKAGE_MANIFEST.json`.

## 29 Oct 2026 — J1192: HOS 009 picture tranche 1 minted and KEEP (57/57 Flow rows of boards v04) (Gemini covering)

- **Authority:** Acting Chief (Claude) price pass J0863 PASS and queue job `J1192`. £0 cash spend, no ElevenLabs, no upload.
- **Live Flow gate & spend:**
  - Start live Flow read: `18,550` credits (`benoats@googlemail.com`, after J1191 008 completion), logged via `ai_spend.py`.
  - Minted all **57/57 tranche-1 Flow rows** across Parts 01–05 (`26 Quality + 31 Fast`):
    - **Part 01 (`12/12` KEEP):** `01_moon_falling`, `02_apple_and_moon`, `03_table_three`, `03_table_three_c1`, `03_table_three_c2`, `04_things_fall`, `05_heavens_map`, `06_perfect_circles` (take 2, non-emissive matte brass armillary sphere), `07_night_field`, `08_three_questions`, `09_no_answer`, `10_farmhouse_dawn`.
    - **Part 02 (`10/10` KEEP):** `01_cambridge_closes`, `02_road_north`, `03_christmas_birth`, `04_sundial_pegs`, `05_working_alone`, `06_prism_spectrum`, `07_fluxions_desk`, `08_the_apple`, `11_explorer_apple`, `12_how_far_moon`.
    - **Part 03 (`7/7` KEEP):** `01_really_falling`, `02_cannon_world`, `03_shot_slow` (take 2 reusing `02_cannon_world` parent still), `04_shot_faster` (take 2 reusing `02_cannon_world` parent still), `05_shot_orbit`, `09_moon_curve`, `10_explorer_cannon`.
    - **Part 04 (`13/13` KEEP):** `01_two_numbers`, `02_spray_paint`, `02_spray_paint_c1` (take 2 reusing `02_spray_paint` parent still), `02_spray_paint_c2` (take 2 reusing `02_spray_paint` parent still), `05_minute_second`, `06_pretty_nearly`, `06_pretty_nearly_c1`, `07_put_aside`, `07_put_aside_c1`, `08_halley_visit`, `09_i_have_calculated`, `10_write_it_down`, `10_write_it_down_c1`.
    - **Part 05 (`15/15` KEEP):** `01_one_law`, `01_one_law_c1`, `02_principia_press`, `02_principia_press_c1`, `04_comet_1758`, `05_iss_orbit` (take 2 clean 3D cartoon station silhouette over blue Earth), `06_iss_apple` (take 2 two upright astronauts in station cabin with floating apple), `07_astronaut_float`, `08_cup_and_planets`, `08_cup_and_planets_c1` (take 2 reusing `08_cup_and_planets` parent still), `08_cup_and_planets_c2`, `09_orchard_dusk`, `10_explorer_bench` (closer), `12_clay_handoff`, `12_clay_handoff_c1`.
  - Total tranche-1 Flow spend: **`3,170` credits** (`2,920` first-pass + `250` across 7 targeted UAT retakes) vs `7,354` expected / `7,585` cap.
  - End live Flow balance: **`15,380` credits** (`>= 3,000` buffer; logged via `ai_spend.py`).
- **Evidence & NAS backup:**
  - Ledger: `02_Video-Projects/009_The-Falling-Moon-Gravity/07_Edit-Project/FLOW_MINT_LOG_v04_tranche1.json` (all 57/57 `KEEP` with sha256, duration, UAT sheet paths, and balance reads).
  - Local media: `/Users/benjaminoats/YouTube/hos-009-gravity/02_Video-Projects/009_The-Falling-Moon-Gravity/04_Generated-Clips/part01..05/` (silent `.mp4` clips, Nano Banana 2 `.png` start stills, UAT contact sheets).
  - NAS copy (copy-only verified, 57/57 matching sha256): `/Volumes/data/mac-mini-archive/YouTube/History Of Science/02_Video-Projects/009_The-Falling-Moon-Gravity/04_Generated-Clips/` and `07_Edit-Project/FLOW_MINT_LOG_v04_tranche1.json`.
- **Next:** Parked for Chief tranche 1 PASS (`J1192`); tranche 2 (`20` Quality rows, `5,180` expected) waits for the ~12 Nov AI Ultra renewal.
