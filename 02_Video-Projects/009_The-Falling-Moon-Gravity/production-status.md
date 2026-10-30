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

- Tranche 1 is complete (57/57 KEEP) and Chief J1237 picture PASS with locked assembly in/outs on the v05 board; tranche 2 (20 Quality rows, 5,180 expected) waits for the ~12 Nov AI Ultra renewal.
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
- **Next:** Chief J1237 closed tranche 1 PASS (see below). Tranche 2 (`20` Quality rows, `5,180` expected) waits for the ~12 Nov AI Ultra renewal.

## 30 Oct 2026 — J1237: Motion evidence for the 3 flagged windows of J1192 tranche 1 (Gemini covering)

- **Authority:** Acting Chief (Claude) queue job `J1237` (answering desk `#6511102950`). `£0` spend, no new mint, no retake, no upload.
- **Chief ruling (source of truth):** https://github.com/TheLaughingGod1986/history-of-science/pull/180#issuecomment-6516310345 — **J1237 PASS**; J1192 tranche 1 picture PASS with the locked in/outs below. Docs/records aligned to that ruling (v05 board + mint-log notes); no remint.
- **Exported evidence (`02_Video-Projects/009_The-Falling-Moon-Gravity/07_Edit-Project/review_J1192_motion/`):**
  - Full-size (`1280×720`) PNG frames across each `freezedetect=n=-50dB:d=0.8` flagged window `±0.5 s` (`P01_03_table_three/frames/` 50 frames, `P04_07_put_aside/frames/` 34 frames, `P04_10_write_it_down_c1/frames/` 38 frames), full-size PNG strips (`*_strip.png`), 1-row contact sheets (`*_contact_1row.png`), 6-column contact grids (`*_contact_grid.png`), and full-clip frame-difference plots (`*_frame_diff_plot.png` + `frame_diff_metrics.json`).
- **Per-clip Chief-locked in/out (assembly must use these):**
  1. **`P01:03_table_three` (`3.333–4.375 s`, `f080–f105`):** Low-motion beat, not a freeze (`0` duplicate frames, `MAD = 0.137–0.380`, `RMS = 0.552–2.750`; apple rocks/settles, centroid ~10 px). Camera essentially static across `f080–f105` (best-fit scale `1.000`); **no** push-in in that span — push-in only builds after ~`4.5 s`. Locked **`0.000–7.000 s` ONLY** (`use_s = 7.00`). **FORBIDDEN:** `1.000–8.000 s` (starts mid-settle).
  2. **`P04:07_put_aside` (`7.083–8.000 s`, `f170–f191`):** Brisk continuous motion `0.000–7.083 s` (`MAD` median `1.15`, papers slide into drawer + summer→autumn→winter→spring light shift) followed by a `0.917 s` tail settle; board `use_s = 3.76 s` avoids the tail at locked **`0.000–3.760 s`**. Hard limit **`out ≤ 7.042 s`**.
  3. **`P04:10_write_it_down_c1` (`0.000–1.042 s`, `f000–f025`):** Opening `1.042 s` (`MAD = 0.099–0.508`) is a low-motion pre-action hold; locked trimmed in/out **`1.083–6.423 s`** (`use_s = 5.34`). Hard limit **`in ≥ 1.083 s`**. Arm/figure note: **checked by Chief J1237, clean** (green sleeve = second standing figure correctly occluded; no arm-through-body or hand morph). `2.583–7.923 s` alt not required.
- **Next:** Tranche 1 picture PASS (Chief J1237). Tranche 2 (`20` Quality rows, `5,180` expected) waits for the ~12 Nov AI Ultra renewal; future 009 assembly brief carries the locked in/outs above.

## 30 Oct 2026 — J1266: Final Sources and provisional Chapters in `Descriptions/moon_long_description_v01.txt` (Chief h13 on J1261, £0, Gemini covering)

- **Authority:** Chief (Grok) ruling `h13` on `J1261` (30 Oct 2026, HOS `#180` re `6521114044`) and queue job `J1266`. Records only, `£0` spend, no YouTube/Studio change, no upload.
- **Provisional chapters status:** Chapters provisional from VO part timings (this job); the rough-cut and picture-lock jobs must re-time them against the master before upload.
- **Provisional `Chapters` block added to `11_Upload-Package/Descriptions/moon_long_description_v01.txt` from locked VO part takes in `02_Voiceover/VO_TAKES_KEEP.json` and part `.wav` durations (summed in film order, no picture yet):**

| Stamp | Chapter title | VO part (`02_Voiceover/`) | Part duration (`VO_TAKES_KEEP.json` & `.wav` `ffprobe`) | Summed part start (s) | First word in part (`stt_raw.json`) | First word in film order (s / `m:ss.ss`) |
|---|---|---|---:|---:|---|---:|
| `0:00` | `The falling Moon` | `hos_009_part01_the_falling_moon_v01` (`sha256: 81b6c45f…`) | `83.84 s` | `0.00 s` | `"Right"` at `+0.10 s` | `0.10 s` (`0:00.10`) → **`0:00`** |
| `1:24` | `An apple in a plague year` | `hos_009_part02_an_apple_in_a_plague_year_v01` (`sha256: 36855907…`) | `89.84 s` | `83.84 s` | `"In"` at `+0.14 s` | `83.98 s` (`1:23.98`) → **`1:24`** |
| `2:54` | `The cannon on the mountain` | `hos_009_part03_the_cannon_on_the_mountain_v01` (`sha256: 53235ab0…`) | `80.88 s` | `173.68 s` | `"Newton's"` at `+0.12 s` | `173.80 s` (`2:53.80`) → **`2:54`** |
| `4:15` | `The Moon test` | `hos_009_part04_the_moon_test_v01` (`sha256: 2d03f372…`) | `131.20 s` | `254.56 s` | `"Newton"` at `+0.10 s` | `254.66 s` (`4:14.66`) → **`4:15`** |
| `6:26` | `Falling around the world` | `hos_009_part05_falling_around_the_world_v01` (`sha256: 10ebaf45…`) | `122.64 s` | `385.76 s` | `"Newton's"` at `+0.16 s` | `385.92 s` (`6:25.92`) → **`6:26`** |

  - Total summed VO duration (`Parts 01–05`): `83.84 + 89.84 + 80.88 + 131.20 + 122.64 = 508.40 s` (`8:28.40`).
- **Final `Sources` block added under `Chapters` (8 plain citations strictly from `01_Script/FACT_NOTES_v01.md` source column; no URLs; honours row 33 "Do not attribute to Newton" on spray-paint analogy and row 41 "Not a Newton cite" on the 010 Alvarez hand-off):**
  - `Isaac Newton, Philosophiæ Naturalis Principia Mathematica (London, 1687), Book III, Prop. IV`
  - `Isaac Newton, A Treatise of the System of the World (London, 1728)`
  - `Isaac Newton, memorandum (c. 1714–18), Cambridge University Library Add. MS 3968`
  - `William Stukeley, Memoirs of Sir Isaac Newton's Life (1752), entry for 15 April 1726`
  - `John Conduitt, memoranda, Keynes MS 130 (Newton Project)`
  - `Edmond Halley, Synopsis of the Astronomy of Comets (1705)`
  - `Richard S. Westfall, Never at Rest (1980)`
  - `NASA NSSDC, "Moon Fact Sheet", and NASA, "ISS Facts and Figures"`
- **Rest of description (`moon_long_description_v01.txt`) and `PACKAGE_MANIFEST.json`:** opener, bullet list, and sign-off kept byte-identical to `#383`.
- **Repository check output (`00_Brand/Channel-Setup/tools/check_all.sh 02_Video-Projects/009_The-Falling-Moon-Gravity`):**
```text
-- no media: PASS
-- status board in sync: PASS
-- ElevenLabs guard tests: PASS
-- vo_check word tests: PASS
-- contract tests: PASS
-- package-lint: PASS
-- review:script moon_script_master_v01.md: PASS
-- gate:episode: PASS
ALL CHECKS PASS
```
- **Package lint on `main` and against PR `#387` (`origin/gemini/j1259-release-gate-chapters-sources` @ `592eaae7`, `checkChaptersAndSources`):**
```text
> content-ops@0.1.0 lint:package
> tsx scripts/package-lint.ts --film 009

PASS  02_Video-Projects/009_The-Falling-Moon-Gravity/11_Upload-Package/PACKAGE_MANIFEST.json
   warn  [captions] no captionsFile (captions from the script)
```
