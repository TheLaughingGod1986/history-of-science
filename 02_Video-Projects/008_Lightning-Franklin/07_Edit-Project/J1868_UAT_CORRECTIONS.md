# J1868 — Franklin v03 UAT correction intake

Codex, elected acting Chief, 3 November 2026. **Triage only; all six notes remain unresolved.**

## Original review and evidence

Live `/api/checks` read confirmed HOS-008, v03, verdict `change`, at `2026-11-03T16:08:33.439Z`, original watch job J1297. Exact review saved in `J1868_BEN_REVIEW_v03.json`; no newer review or duplicate correction job was found. No media was reviewed or changed in this triage.

- [Chief h22 picture lock](https://github.com/TheLaughingGod1986/history-of-science/pull/180#issuecomment-6533306017): rough v12; not a finished-film approval.
- [Chief h35 master approval](https://github.com/TheLaughingGod1986/history-of-science/pull/180#issuecomment-6537320070): master v03, SHA256 `cf1561c218bace7bc14ed3d625b0790a457027a90f392262f45ca7172723099b`, 393139693 bytes, 539.626 seconds. These historical approvals are preserved; they do not resolve the new notes.
- J1297 completed UAT delivery; HOS PR391 is merged. Main pipeline still carried older picture/edit labels. Undocumented milestones are not made complete from the existence of the master.
- J1755 remains blocked at 2/3: restored UAT hash verified previously, browser playback media returned 403. Automatic approval review rejected replacement watch-object publication under its no-upload brief. PR401 is still open. Its delivery scope and restrictions remain separate from this correction intake. This record supersedes its pending-watch wording for the current six-note review; it does not dispose of PR401 or authorize publication.

## Correction scope

| Ben time (unchanged) | Ben note (verbatim) | Required outcome / acceptance |
|---|---|---|
| 00:20 | text on screen in readable needs maybe background colour | Readable white Didot italic with compliant contrast/background over moving picture, clear of the subject; check at phone size. |
| 0:30 | flash the next scene | Locate the unintended adjacent-scene flash and specify a clean boundary; no clipped spoken word, frozen filler or timing drift. |
| 1:49 | strange behaviour as hair flies out the tube | Locate the hair/tube artefact; select approved native motion supporting the locked line, or identify a missing asset for separately scoped generation. |
| 2:20 | strange behaviour with the silver foil | Locate the foil artefact and specify physically coherent approved motion supporting the line; no misleading composite or still workaround. |
| 3:31 | the diagram/ map is not easy to understand | Simplify our own animated map/diagram to one idea matching the spoken line; sourced geometry/labels and HOS styling, readable without sound. |
| 7:58 | the rods fall down for some reason | Locate the falling-rod artefact; retain believable anchored rods through the full interval and transitions, using approved motion or a separately scoped asset. |

These are Ben’s observations. Exact source rows, intervals, spoken lines and independently reproduced failures are for J1880 to establish; this intake does not invent those findings.

## Actionable handoffs

- **J1880 — assembly capability chain:** Cursor/Grok, Cursor Auto, Codex, Gemini according to availability. Ready now; due 4 Nov 12:00 London (deadline, not a delayed start). Map all six notes to master/cuts/source/VO and prepare an exact new-version edit recipe or code diff plus six acceptance checks. No replacement render, generation or credit spend. Inspect approved alternative native motion first; bound any missing-input search to 20 active minutes / three candidates, shared across retries. Preserve original files and locked VO/music/sync.
- **J1881 — elected Chief, after J1880:** due 4 Nov 14:00 London. Review the concrete recipe and missing-input evidence; queue separately scoped correction assembly and capable media QA jobs, or record a specific input hold. Any generation requires an explicit bounded HOS route/takes/cap and fresh balance checks. No authority to render or publish is conferred by this planning job.
- **J1755 — separate delivery owner:** existing hold and publication rejection stay in force. No R2 upload, YouTube action, schedule change or bypass here.

Intake acknowledgment through the existing checks API may mark the request handled **only as tracked** after these queue jobs and records exist. Retain original version/verdict/notes/timestamp. No note is marked resolved; no media PASS or Ben approval is claimed. Corrected media still requires all original gates, capable review and Ben’s finished-film watch.

## Validation

Record-only change. Repository check output is recorded in production-status.md.

---

## Current correction: J2163 supersedes the J1880 proposal below

See `J2163_REPAIR.md`, `J2163_CORRECTION_MANIFEST.json` and measured `J2163_MASTER_FRAME_PTS.json`. J1880 material below is preserved historical evidence, not the active recipe. Its inferred zero frame delta/sync, global CFR renderer, native Option A and overlay banner are rejected. All six notes remain unresolved; J1881 reviews this repair before separately scoping production. No media approval.

## J1880 — Source mapping, bounded correction recipe & six acceptance checks (Gemini worker, 4 November 2026)

- **Authority & scope:** Queue job `J1880` (`HOS-008:v03:2026-11-03T16:08:33.439Z / J1868`), HOS `008` `edit` claimed by `gemini`. Correction preparation only: **£0 spend, 0 Flow/ElevenLabs credits spent, 0 media files modified or rendered, 0 watch-object/R2/YouTube actions.** All six Ben notes remain unresolved pending `J1881` elected-Chief scope review, correction execution, capable QA, and Ben's watch.
- **Checks API reconciliation (`2026-11-04T22:03:30Z`):** `HOS-008` `v03` remains `status: "change"` at `2026-11-03T16:08:33.439Z` (not superseded). `J1755` / PR `#401` browser delivery repair and automatic-publication rejection remain separate and untouched.
- **Demonstrated media-input capability (`chief_relay.py capabilities`):** `gemini` demonstrated both `audio_input` and `moving_video_input` via native `read_file` perception on the 6 extracted moving-video + synchronized-audio segments (`01_00m20s.mp4`..`06_07m58s.mp4`) and candidate clips (`01_salon_tube_t1.mp4`, `03_audience_shock_t1.mp4`, `11_jar_crack_t1.mp4`, `21_roofs_golden_t1.mp4`, `01_house_rod_t1.mp4`), cross-checked against packet/PTS/frame boundaries of `hos_008_master_v03.mp4` (`sha256: cf1561c218bace7bc14ed3d625b0790a457027a90f392262f45ca7172723099b`, `393,139,693` bytes, `12,923` video packets @ 24 fps, `539.626 s`) and `hos_008_rough_v12.mp4` (`sha256: 02db759e1c4a0fa3fbcf5b19037d8c52527c93750df4d80aa9a6c8e0c9bf7745`). Uncertainty note: Ben's final watch on phone/desktop remains the sole authority to clear UAT after `J1881`.
- **Deliverables in `07_Edit-Project/`:**
  1. `J1880_SOURCE_INVENTORY_v04.json`: full source inventory, SHA-256 hashes, display frame / PTS / timeline / pre-trim intervals, adjacent cuts, spoken VO word timestamps, missing-footage search log (`9.5` cumulative active minutes across `1:49`, `2:20`, `7:58`; `<= 20 min` / `<= 3 candidates` per input), and Option A (£0 native) vs Option B (scoped Flow retake) specs.
  2. `_build_rough_v13_recipe.py`: exact new-version (`rough_v13 -> master_v04`) Python edit recipe (`--dry-run` default verified: `6` patched intervals, `919` patched frames, `12,004` unchanged frames, `12,923` total packets, `0` frame delta, `0.000 ms` `h35` VO sync lag).

### 1. Exact timestamp-to-source mapping and bounded corrections

| # | Ben time (verbatim) | Ben note (verbatim) | `v12` Cut & Row | Source clip & SHA-256 | `master_v03` display frames & PTS (`24 fps`) | Spoken VO line & word window | Independently reproduced finding in moving video + audio | Bounded correction in `_build_rough_v13_recipe.py` (`0` frame delta) |
|---|---|---|---|---|---|---|---|---|
| 1 | `00:20` | `text on screen in readable needs maybe background colour` | Cut `[3]` · `P1:03_table_three` (prev: `[2] P1:02_tower_tilt` `273..426`; next: `[4] P1:03_table_three_c1` `545..662`) | `03_table_three_t1.mp4` (`482a254d7f7b...`) | Frames `427..544` (`118f`, PTS `17.917–22.792 s`, timeline `17.764–22.681 s`) | *"By the end of this film, you'll know how a kite, a key, and a glass jar"* (`17.88–22.66 s`) | `draw_side_label()` rendered `A KITE · A KEY · A JAR` in warm gold `(242,208,122)` at `(960, 940)` directly over the sunlit warm-tan wooden tabletop and brass ring without a backing pill, losing luminance/hue contrast. | **£0 re-render of Cut `[3]` (`118f`, `427..544`):** render `A KITE · A KEY · A JAR` in HOS house Didot italic `58 px` cream-white `(252,248,240)` + `5 px` dark-umber stroke `(28,16,8)` inside a soft rounded dark-umber translucent pill `rgba(36,22,12,205)` with warm gold border `rgba(211,167,88,170)`, radius `18 px`, padding `28×14 px` at `y=940` (clear of kite, key, and jar), `0.35 s` fade in/out. |
| 2 | `0:30` | `flash the next scene` | Cut `[5]` · `P1:03b_town_safe` -> Cut `[6]` · `P1:04_storm_mystery` | `03b_town_safe_t1.mp4` (`f89bec2a38ae...`) -> `04_storm_mystery_t1.mp4` (`e1b2de5d8cd4...`) | Cut `[5]`: `663..747` (`85f`, clean `663..743`, flash `744..747` at PTS `31.167–31.292 s`); Cut `[6]`: `748..839` (`92f`, PTS `31.333–35.125 s`) | *"...simple idea stopped it burning our towns down."* (ends `30.70 s`) · pause `30.70–31.24 s` · *"For thousands of years, lightning was a mystery."* (`31.24–34.48 s`) | `PAUSE_TRIM_v03.json` cut pre-trim `32.269–32.990 s` inside the tail of `P1:03b_town_safe`, leaving a `4-frame` (`0.167 s`) residual fragment at display frames `744..747` (`31.167–31.292 s`) where a lightning bolt flashes over the town street just before Cut `[6]` starts at frame `748`. | **£0 boundary shift across `663..839` (`177f` total):** end `P1:03b_town_safe` cleanly at frame `743` (`81f`, `0.42 s` after *"down."* ends at `30.70 s`) and start `P1:04_storm_mystery` `4` frames earlier at frame `744` (`96f`, `0.000–4.000 s` of `04_storm_mystery_t1.mp4`, `0.07 s` before *"For"* at `31.24 s`). Zero VO clip, zero freeze, exact `177f` preserved. |
| 3 | `1:49` | `strange behaviour as hair flies out the tube` | Cut `[23]` · `P2:02_salon_spark` (prev: `[22] P2:01_salon_tube` `2407..2505`; next: `[24] P2:03_audience_shock` `2666..2717`) | `02_salon_spark_t1.mp4` (`4b61312e9416...`) | Frames `2506..2665` (`160f`, PTS `104.667–111.292 s`, timeline `104.376–111.043 s`) | *"Traveling lecturers rubbed glass tubes with silk and made sparks fly from people's fingers and hair."* (`104.25–110.19 s`) | Across `t=1.5–6.5 s` of `02_salon_spark_t1.mp4` (film `105.9–110.9 s`, peaking at `1:49`), cotton-like puffs float in mid-air and white powdered hair streams/extrudes out of the open tip of the glass tube onto the seated woman's head before detaching into floating blobs. Only `0.0–1.125 s` (`27f`) is clean. | **Option A (£0 native in recipe, `2506..2717` = `212f`):** `2506..2585` (`80f`, *"Traveling lecturers rubbed glass tubes with silk"*) uses unused `4.125–7.458 s` of `01_salon_tube_t1.mp4` (`1.12×` crop, upscale `1.68 <= 2.35`); `2586..2665` (`80f`, *"and made sparks fly from people's fingers and hair"*) uses `0.000–3.333 s` of `03_audience_shock_t1.mp4` (spark jumps to guest's finger, curls bounce); Cut `[24]` (`2666..2717`, `52f`) advances to `3.333–5.500 s` (`1.12×` crop). **Option B (Chief J1881 choice):** scoped Flow retake of `P2:02_salon_spark` from `02_salon_spark_t1.png` (`aefd6338...`). |
| 4 | `2:20` | `strange behaviour with the silver foil` | Cut `[28]` · `P2:07_foil_jar` (prev: `[27] P2:06_leyden_jar` `3049..3167`; next: `[29] P2:08_jar_spark` `3344..3407`) | `07_foil_jar_t1.mp4` (`8e28cc24ed74...`) | Frames `3168..3343` (`176f`, PTS `132.292–139.583 s`, timeline `131.906–139.239 s`) | *"It was a glass jar lined with metal foil, and it could store electricity, then let it all go at once in a"* (`132.09–139.21 s`) | Frames `0..91` (`0.000–3.833 s`, display `3168..3259`, film `132.29–136.08 s`) show clean hands pressing silver foil around the glass jar. Across frames `92..175` (`3.833–7.333 s`, display `3260..3343`, peaking at `2:19–2:20`), foil peels off in his left hand, teleports onto the jar rim like a cap, and the jar levitates above his open palm. | **£0 native fix (`3168..3343` = `176f`):** keep safe frames `3168..3259` (`92f = 3.833 s`, `0.000–3.833 s` of `07_foil_jar_t1.mp4`, *"It was a glass jar lined with metal foil, and it could store"*) and replace defective frames `3260..3343` (`84f = 3.500 s`, *"electricity, then let it all go at once in a"*) with unused `4.000–7.500 s` of approved KEEP plate `11_jar_crack_t1.mp4` (`7629a5df...`, foil-lined Leyden jars linked by brass rod on workshop bench, `>11.0 s` before Cut `[32]`). |
| 5 | `3:31` | `the diagram/ map is not easy to understand` | Cut `[44]` · `P3:04_letter_crosses` (prev: `[43] P3:03_book_pages` `4858..4976`; next: `[45] P3:05_king_hears` `5078..5176`) | `overlay_04_letter_crosses.mp4` (`3d827e7f7433...`) over `07_slow_news_t1.mp4` (`775e6d72eeb9...`) | Frames `4977..5077` (`101f`: `v06` card `4977..5068`, orphaned `v04` map flash `5069..5077` at PTS `211.750–212.083 s`) | *"He published the idea, and it crossed the ocean."* (`207.97–210.71 s`) | Two compounding defects: (1) frames `4977..5068` (`92f`) show two blank brown rounded rectangles (`WEST_BOX`, `EAST_BOX`) in a top-left inset card `(60,60,540,420)` that do not read as an ocean map; (2) frames `5069..5077` (`9f` right at `3:31`) flash the superseded `v04` vector shoreline diagram over the ship's sails. | **£0 code-overlay re-render across all `101f` (`4977..5077`):** render `overlay_04_letter_crosses_v04.mp4` over `0.000–4.208 s` of moving packet-ship plate `07_slow_news_t1.mp4` with a single upper-sky HOS cream-on-umber translucent trajectory banner (`x=200..1720, y=62..214`, `0.0%` ship occlusion above highest mast `y=248`): `PHILADELPHIA` -> animated golden dotted Atlantic arc + inked letter badge (`0.50–2.85 s`) -> `PARIS · 1752` (`3,600 MILES ACROSS THE ATLANTIC`). Eliminates both the brown boxes and the 9-frame flash. |
| 6 | `7:58` | `the rods fall down for some reason` | Cut `[100]` · `P5:13_rods_spread` (prev: `[99] P5:12_no_patent` `11246..11357`; next: `[101] P5:14_safe_towers` `11493..11611`) | `13_rods_spread_t1.mp4` (`d9fa5f1329ad...`) | Frames `11358..11492` (`135f`, PTS `474.375–479.958 s`, timeline `473.462–479.087 s`) | *"Within a few years, rods were going up on churches, houses, and ships' masts,"* (`473.44–478.52 s`) | After `t=1.50 s` (display frame `11394`, film `475.88–479.96 s`, peaking at `7:58`), the lightning rods on the church steeple and brick town house sprout jagged lightning-bolt kinks, detach from the roofs, tilt `60°` sideways, and fall/float across the sky. Only `0.0–1.50 s` (`36f`) is clean. | **Option A (£0 native in recipe, `11358..11492` = `135f`):** use `135` continuous frames (`1.500–7.125 s`, `5.625 s`) of approved KEEP plate `21_roofs_golden_t1.mp4` (`0bc82892...`) with a `1.08×` reframe (`upscale 1.62 <= 2.35`), showing straight vertical rods on a church steeple and row of houses in calm daylight (`43.5 s` before Cut `[109]`; caveat: no ship's mast). **Option B (Chief J1881 choice):** scoped Flow retake of `P5:13_rods_spread` from `13_rods_spread_t1.png` (`84a92bf6...`). |

### 2. Six acceptance checks for `master_v04` (post-`J1881` execution & capable QA)

1. **Check 1 (`00:20` · `P1:03_table_three` · frames `427..544`):** `A KITE · A KEY · A JAR` renders in HOS house Didot italic cream-white `(252,248,240)` over the dark-umber translucent pill `rgba(36,22,12,205)` at `y=940` with Weber/WCAG contrast ratio `>= 7.0:1`, readable at `168×94` phone preview size, fading in/out over `0.35 s` over moving picture, and `0%` overlap with the kite, key, or jar.
2. **Check 2 (`0:30` · `P1:03b_town_safe -> P1:04_storm_mystery` · frames `663..839`):** Single clean cut at display frame `744` (`31.167 s`, during the `30.70–31.24 s` inter-sentence pause); `0` residual frames from the lightning-flash tail of `03b_town_safe_t1.mp4`; `0` clipped spoken words; combined interval remains `177` frames.
3. **Check 3 (`1:49` · `P2:02_salon_spark` · frames `2506..2665`):** `0` frames of hair, smoke, or cotton extruding from or detaching near the glass tube across frames `2506..2717`; continuous native motion (`0` freeze events `>= 0.8 s`, upscale `<= 2.35×`) matching *"Traveling lecturers rubbed glass tubes with silk and made sparks fly from people's fingers and hair."*
4. **Check 4 (`2:20` · `P2:07_foil_jar` · frames `3168..3343`):** `07_foil_jar_t1.mp4` cuts out at frame `3259` (`3.833 s`) before any foil peels or jar levitates; frames `3260..3343` (`84f`) show physically coherent Leyden jars (`11_jar_crack_t1.mp4` `4.000–7.500 s`, `>11.0 s` before Cut `[32]`), passing `picture_qa.py` (`0` fails).
5. **Check 5 (`3:31` · `P3:04_letter_crosses` · frames `4977..5077`):** All `101` frames (`4977..5077`) carry the single upper-sky `PHILADELPHIA ──────► PARIS · 1752` (`3,600 MILES ACROSS THE ATLANTIC`) trajectory banner (`y=62..214`, `0.0%` ship mast/sail occlusion); `0` frames of the `v06` brown rectangles (`4977..5068`) and `0` frames of the orphaned `v04` vector shoreline flash (`5069..5077`); understands with sound off.
6. **Check 6 (`7:58` · `P5:13_rods_spread` · frames `11358..11492`):** Across all `135` frames (`11358..11492`), every lightning rod remains straight, rigid, vertical, and firmly anchored to its structure (`0` lightning kinks, `0` tilting/detaching/falling rods), with continuous motion (`0` freeze events `>= 0.8 s`) and exact `12,923`-packet / `0.000 ms` `h35` VO sync preserved across the full master.

### 3. Missing-asset / retake decision table for elected Chief (`J1881`)

- **Option A (`£0` / `0` Flow credits, ready immediately in `_build_rough_v13_recipe.py`):** Uses approved KEEP plates for all 6 notes (`01_salon_tube_t1.mp4` + `03_audience_shock_t1.mp4` at `1:49`; `21_roofs_golden_t1.mp4` at `7:58`). Caveats for Chief: at `1:49`, `03_audience_shock_t1.mp4` shows a spark from a table globe machine rather than close-up hair attraction to a glass rod; at `7:58`, `21_roofs_golden_t1.mp4` shows church and house rods clearly in calm daylight, but no ship's mast.
- **Option B (bounded Flow Veo 3.1 retakes on CDP `9222`, AI Ultra subscription credit, `£0` cash, live balance `15,430` credits vs `0` floor):**
  - `P2:02_salon_spark` (`1:49`): start frame `04_Generated-Clips/part02/refs/v03_flow_stills/02_salon_spark_t1.png` (`sha256: aefd6338...`), bounded `<= 3` takes (`30 cr` Fast cap or `300 cr` Quality cap), prompt & acceptance in `J1880_SOURCE_INVENTORY_v04.json`.
  - `P5:13_rods_spread` (`7:58`): start frame `04_Generated-Clips/part05/refs/v03_flow_stills/13_rods_spread_t1.png` (`sha256: 84a92bf6...`), bounded `<= 3` takes (`30 cr` Fast cap or `300 cr` Quality cap), prompt & acceptance in `J1880_SOURCE_INVENTORY_v04.json`.
  - Combined 2-plate cap: `60 cr` (Fast) or `600 cr` (Quality). No generation started in `J1880`.

## Ben second v03 review (5 Nov 2026)

See **[J1868_BEN_NOTES_2026-11-05.md](./J1868_BEN_NOTES_2026-11-05.md)** for the full record (Ben comment `6658371896`, Claude advisory `6658387533`). Ben's wording stays the record. No note is marked resolved.

> [Ben] changes 008 v03:
> 1. 0:51 still have hair flying out the tube, this needs rebuilt
> 2. Also the bottom text needs a background colour it’s hard to read over a moving video
> 3. 2:18 the jar flips upside down like magic
> 4. 3:13 strange behaviour as paper seems to roll out the globe
> 5. 7:59 the rods on the church’s seem to fall right

Net scope before any splice: eight defect items = the original six 3 Nov notes (unchanged, still unresolved) plus new **0:51 hair rebuild** plus new **3:13 paper/globe**, with a film-wide bottom-caption background over every bottom on-screen text on moving footage. No production splice on the old six-only list.

## J2217 amend (5 Nov 2026) — measured, not executed

Active plan is `eight_rows` in `J2163_CORRECTION_MANIFEST.json` (`schema` `hos.uat_correction_plan.v3`). `six_rows` is unchanged historical evidence. `_build_rough_v13_recipe.py` plans those eight rows and refuses `--execute` until J1881 re-reviews. GBP0. No render, spend, upload, or YouTube change. h22/h35, J1297, and the J1755/PR401 publication rejection stay as they were.

Master `cf1561c218bace7bc14ed3d625b0790a457027a90f392262f45ca7172723099b`, timebase `1/12288`, from `J2163_MASTER_FRAME_PTS.json`:

| Clock | Master frame | PTS | Plate | Row |
|---|---|---|---|---|
| 0:51 | 1220 | 51.000 s | `07_hot_night_t1.mp4` frames 1129–1232 | New row. Not the same source as 1:49. |
| 1:49 | 2506–2665 | 104.667–111.333 s | `02_salon_spark_t1.mp4` | Original hair/tube row, still unresolved. |
| 2:18 | 3305 | 138.000 s | `07_foil_jar_t1.mp4` | Outside keep 3168–3259. Inside replace 3260–3343. Not a new row. |
| 3:13 | 4621 | 193.000 s | `01_points_desk_t1.mp4` frames 4513–4672 | New row. Distinct from the 3:31 map. 13-frame residual before the map cut is unresolved. |
| 7:59 | 11469 | 479.000 s | `13_rods_spread_t1.mp4` | Inside the existing 11358–11492 rods row. |

0:51 stays on the hot-night plate because that is where the clock lands. The hair-and-tube picture is the salon plate already listed at 1:49. The row is not dropped and not retargeted. J1881 chooses which rebuild to scope. 27 rough-v12 bottom labels get an unbordered background panel. That inventory is not a splice list. Details: `J2217_AMEND.md`.
