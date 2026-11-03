# J1880 — Franklin v03 partial correction recipe

**Preparation incomplete; all six notes remain unresolved. No media PASS. GBP0.**

Current checks API was read and matches the original six-note v03 change request; snapshot is `J1880_CURRENT_CHECK.json`. NAS master was read and SHA-256 verified against cf1561c2…3099b (393139693 bytes). Historical h22/h35 approvals, J1297 and J1755 remain separate and unchanged.

Only stills were inspected. Local evidence is `/private/tmp/j1880-evidence/sheet.jpg` (not committed media). This establishes subject/layout at the sampled instants, not defects at normal speed. No audio/moving-video perception is available in this session. Exact JSON mapping, original notes, expected source hashes and adjacent cuts are in `J1880_SOURCE_MAPPING.json`. Source hashes in cut records are inherited provenance, not rehashed this session.

## Clock and source limitations

Use `timeline_in/out` for master seeking. `film_t` drifts away from the actual edited clock (for example rods-spread has film_t 481.579 but timeline 473.4623–479.0873). All six sampled subjects agree with timeline mapping. The video starts at 0.125s and is 24fps. Rounded cut times are not exact decoded frame boundaries. The original precheck rough-v04 pause removal file referenced by `_build_rough_v08.py` is absent at its recorded local path. Recover it from archive or derive verified source/master correspondence before defining source substitutions. Never use a nominal row offset as a proven safe interval.

## 00:20 — text on screen in readable needs maybe background colour

P1 `03_table_three`; proposed changed window [17.7643, 22.681)s. Source `03_table_three_t1.mp4`, SHA-256 `482a254d7f7b195241eea96511a736d212c971988decb33c38b183347639a9bb`. Adjacent rows: 02_tower_tilt, 03_table_three, 03_table_three_c1.

**Locked script context (text, not a listening/word-alignment result):** By the end of this film, you'll know how a kite, a key and a glass jar proved what lightning really is, and how one simple idea stopped it burning our towns down.

Rebuild only this row from its clean moving source. Replace the existing burnt-in label rather than layering a second label over it. White Didot italic, fitted to <=1500 px, start font 76 px at 1920x1080; short text: KITE · KEY · JAR (existing spoken nouns, no new claim). Centre at (960,940), keep off key/jar. Use a fitted soft cream-on-brown backing with 32px horizontal/18px vertical padding, 16px feather and 85% maximum opacity; no full-width slab. Fade 0.35s in/out; visible from row+0.15s to min(row+3.75s,row_out-0.25s). Check full-size and phone readability before finalising dimensions. Duration unchanged.

**Acceptance:** text on screen in readable needs maybe background colour — verify corrected result at normal speed, phone size, and adjacent transitions; retain all unchanged gates and sync

## 0:30 — flash the next scene

P1 `03b_town_safe`; proposed changed window [27.5977, 31.1267)s. Source `03b_town_safe_t1.mp4`, SHA-256 `f89bec2a38ae7707881637aad9ee3e0e7408febd85ebb1b6f31e88e6c735e9a0`. Adjacent rows: 03_table_three_c1, 03b_town_safe, 04_storm_mystery.

**Locked script context (text, not a listening/word-alignment result):** For thousands of years, lightning was a mystery. It fell without warning, split trees, killed animals in the fields and set roofs alight.

Inspect every frame of the town-safe row plus both adjacent cuts at normal speed and frame-step. Do not assume the intended 31.1267s boundary is the reported flash. Once exact anomalous frame(s) are identified, substitute the same count of chronologically contiguous clean native source frames; retain row boundary and audio samples. No deletion from timeline, duplicated frame, freeze, optical-flow invention or VO cut. Exact bad-frame index and safe source interval remain unestablished.

**Acceptance:** flash the next scene — verify corrected result at normal speed, phone size, and adjacent transitions; retain all unchanged gates and sync

## 1:49 — strange behaviour as hair flies out the tube

P2 `02_salon_spark`; proposed changed window [104.376, 111.0427)s. Source `02_salon_spark_t1.mp4`, SHA-256 `4b61312e9416b68853409b7d67683643934b44cc2d56e48623b8b0c4e8c58a92`. Adjacent rows: 01_salon_tube, 02_salon_spark, 03_audience_shock.

**Locked script context (text, not a listening/word-alignment result):** Travelling lecturers rubbed glass tubes with silk and made sparks fly from people's fingers and hair. Audiences paid to feel the shock.

Inspect full salon-spark row and preceding salon-tube source. Prefer a continuous native interval showing silk rubbed on tube or restrained hair attraction that stays attached to the guest; no loose hair emerging from tube. Preserve locked line and target duration. No safe alternative interval is approved by this session; current take is not cleared merely because J1191 previously KEEP-ed it.

**Acceptance:** strange behaviour as hair flies out the tube — verify corrected result at normal speed, phone size, and adjacent transitions; retain all unchanged gates and sync

## 2:20 — strange behaviour with the silver foil

P2 `08_jar_spark`; proposed changed window [139.2393, 141.921)s. Source `08_jar_spark_t1.mp4`, SHA-256 `6a24bb5487447e000f2041833f9ef8ef575f678a82ffc10c8ddbb513fa585b4c`. Adjacent rows: 07_foil_jar, 08_jar_spark, 09_window_storm.

**Locked script context (text, not a listening/word-alignment result):** It was a glass jar lined with metal foil, and it could store electricity, then let it all go at once, in a bright spark with a loud crack.

Inspect jar-spark plus preceding foil-jar source. Select continuous coherent jar/foil motion: lining remains attached, cork and ring-wire stable, no foil flying or morphing. Spark supports locked narration. Do not conceal artefact with still frame or misleading patch. Safe replacement interval remains missing.

**Acceptance:** strange behaviour with the silver foil — verify corrected result at normal speed, phone size, and adjacent transitions; retain all unchanged gates and sync

## 3:31 — the diagram/ map is not easy to understand

P3 `04_letter_crosses`; proposed changed window [207.827, 211.577)s. Source `overlay_04_letter_crosses.mp4`, SHA-256 `3d827e7f7433a5d1c50ff0278fc6b8e5ae49d1a4c25c8bb025eedde7cec6e32a`. Adjacent rows: 03_rod_cloud, 04_letter_crosses, 05_marly_garden.

**Locked script context (text, not a listening/word-alignment result):** He published the idea, and it crossed the ocean. In May seventeen fifty-two, in a garden at Marly, near Paris, French scientists put up a tall pointed rod and tried it.

Rebuild own alpha overlay over moving ship plate, removing existing composite map/text first. One idea: published letter crosses ocean. Use sequential PHILADELPHIA then PARIS, one label at a time, white Didot italic, <=4 words per label, >=76px at 1080p. A single letter icon moves between two named points across an unscaled schematic ocean band; no invented coastline, bearings, distance or travel-time metric. 0.4s ink/fade entry/exit, continuous animation within existing row. FACT_NOTES must support destinations; source-backed geometry required if any map outline is retained. Underlying clean plate provenance and source interval must be recovered from v06 compositor before executable recipe.

**Acceptance:** the diagram/ map is not easy to understand — verify corrected result at normal speed, phone size, and adjacent transitions; retain all unchanged gates and sync

## 7:58 — the rods fall down for some reason

P5 `13_rods_spread`; proposed changed window [473.4623, 479.0873)s. Source `13_rods_spread_t1.mp4`, SHA-256 `d9fa5f1329ad0e190ffd43c5b3d8cd47ab3c39b58402dc76eeb43c74290d9607`. Adjacent rows: 12_no_patent, 13_rods_spread, 14_safe_towers.

**Locked script context (text, not a listening/word-alignment result):** Within a few years, rods were going up on churches, houses and ships' masts. And one by one, church towers became safer places to stand.

Inspect rods-spread source and safe-towers native source, including full transitions. Rods must stay anchored to church/house/mast; no downward translation, detached floating hardware or unexplained falling. Prefer an approved continuous safe-towers interval if it supports the line and reuse limits. No safe interval selected here; do not approve from the single still.

**Acceptance:** the rods fall down for some reason — verify corrected result at normal speed, phone size, and adjacent transitions; retain all unchanged gates and sync

## Resume and validation

Steps: (1) intake/ownership/current review complete; (2) source and adjacent-motion/VO mapping incomplete; (3) exact executable recipe incomplete; (4) final validation/handoff incomplete. Do not mark J1880 done or unblock J1881. Resume the same four-step plan with a worker demonstrating moving_video_input. Recover original pause-trim map and exact spoken alignment, inspect approved native alternatives and record source intervals/hashes; audio listening, if required to establish spoken alignment, needs demonstrated audio_input too.

No generation is proposed for execution yet. If native options fail, J1881 must separately scope reference, Flow/Veo route (Quality for fragile spark/light), bounded takes, live-balance-based cap and capable acceptance reviewer; no invented price or generation authority. Search budget remains at most 20 active minutes / three in-depth candidates per missing input cumulatively.

For any later picture-only master, copy v03 audio unchanged, retain timing/frame count, verify untouched decoded picture outside approved intervals, then run unmodified picture/polish/music/episode/package and HOS required checks. Capability review and Ben’s corrected finished-film watch still required. J1755 publication rejection remains in force.
