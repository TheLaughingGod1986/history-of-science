# HOS 009 Shorts A & B — J2171 Inventory & £0 Assembly Report

- **Job:** `J2171` (`ref: J2023`)
- **Assembler:** `gemini` (`gemini-agy`, £0 / 0 credits)
- **Date:** `2026-11-21`
- **Scope:** £0 preparation and assembly only. Zero generation, zero credit spend, zero YouTube upload/schedule/privacy/retitle changes, zero Buffer writes.

## 1. Pre-Work Re-Inventory

### 1.1 Duplicate Public / Scheduled Ideas Check
- **Snapshot checked:** `05_Analytics/hos/snapshots/2026-11-20.json` (`69` HOS videos) plus `00_Brand/Channel-Setup/audits/shorts_open_library/library.json` (`air-date` checks for `2026-11-27` and `2026-11-30`).
- **Result:** `0` public or scheduled HOS videos or Shorts cover gravity, Newton, the Moon, orbits, or falling (`moon`, `gravity`, `newton`, `apple`, `orbit`, `falling`).
- **Parent long (`009` *Why Doesn't the Moon Fall to Earth?*):** Not yet uploaded or scheduled (`J3261` built long master v02, currently in `J2036` review; planned Thu `2026-11-26T18:00:00Z`). Neither Short may air before the parent long is Public.
- **Pairwise Frame-0 uniqueness (Short A vs Short B):** `hamming = 28 bits` (fail `<= 10`, warn `<= 16`), `background_match = 0.069` (fail `>= 0.40`, warn `>= 0.30`) — **PASS**.

### 1.2 Locked VO & Score Verification (100% SHA-256 Match, £0)
- **Short A VO (`hos_009_short_A_v02`):** J0862 / J2281 PASS (HOS PR #423). `24.320 s` speech (`1.00x`, `atempo = 1.0`), `vo_onset = 0.12 s <= 0.15 s`, hook ends `2.800 s <= 2.85 s`.
  - MP3 SHA-256: `c2fd407d3aafbe57030b29b213ed128ee4887b785272a2192b4c0809796a1ce6`
  - WAV SHA-256: `48847b15feda51804a0f6afae1a79aacc74b9bac43ef3eeadda8a7503b745571`
- **Short B VO (`hos_009_short_B_v04`):** J0862 / J2195 / J2279 / J2281 PASS (HOS PR #423). `24.480 s` speech (`1.00x`, `atempo = 1.0`), `vo_onset = 0.06 s <= 0.15 s`, hook ends `2.820 s <= 2.85 s`. Preserves both *"In one minute"* and *"in one second"* comparison intervals and all `J1004`/`J1894` restrictions.
  - MP3 SHA-256: `0c9c4c6ffdb1337dc11acaf57af909f8d8be91d77210bca2e13af80715b87498`
  - WAV SHA-256: `a6666fd27c9a90e781369ea07e4888d87a2d5edb1624a0090ae98fa39504686b`
- **Score (`hos_009_score_v04_synth.wav`):** Accepted by Acting Chief in `J3241` (`SCORE_DISPOSITION_v04_synth.json`). SHA-256 `151ba46acdf7d4395b34e105530bd077c26f6eb92832f9a1f00e1551ca88f58d` (`535.33 s`). Short A slices Part 1 awe/wonder (`t=2.0 s`, 62 BPM); Short B slices Part 4 explain pulse (`t=262.0 s`, 67 BPM).
- **House SFX kit (`06_Sound-Effects/kit_v01`):** Synthesised at £0 via `sfx_kit.py make --house hos` on NAS (`whoosh_soft`, `tick_ink`, `rumble_low`).

### 1.3 Verified Locked Plates (13/13 Local & NAS Exact SHA-256 Match)
| Row ID | File | SHA-256 | Authority | Used In |
|---|---|---|---|---|
| `P1:01_moon_falling` | `part01/raw/v01/01_moon_falling_t1.mp4` | `3e0774a7dd510b5ee32358c188f5efe4903aaf45aafab8870df662bcc1cd4c1f` | J1192/J1237 | Short A S01 (`2.00..4.80s`, `x=260->360`) + loop (`1.00..2.00s`, `x=225->260`) |
| `P1:02_apple_and_moon` | `part01/raw/v01/02_apple_and_moon_t1.mp4` | `bc3ad225b09a2fc090c4cbe694eb3aeeb0cf5999cd6c6d6262be81a1adcc90e6` | J1192/J1237 | Short B S02 (`0.80..3.54s`, `x=437->480`) |
| `P2:07_orchard_bench` | `part02/raw/v01/07_orchard_bench_t1.mp4` | `028ee06be5e3fb76cbc58265837633993c4834c961735c191c36379c5e7afa02` | J1192/J1237 | Short A S05 (`1.20..4.48s`, `x=540->560`) |
| `P2:08_the_apple` | `part02/raw/v01/08_the_apple_t1.mp4` | `357e8de3e9c771ef212fb01ee0a6052ebfedbc0de0ad9794270f5ff2128a5b44` | J1192/J1237 | Short A S06 (`0.40..3.60s`, `x=450->460`) |
| `P3:05_shot_orbit` | `part03/raw/v01/05_shot_orbit_t1.mp4` | `0878c30646fa8b7158044a5e3d52a584a1cf4fda8accc76f6aa747fca8405f1b` | J1192/J1237 | Short A S04 (`1.00..4.16s`, `x=420->560`) |
| `P3:07_ball_to_moon` | `part03/raw/v05_tranche2/07_ball_to_moon_t1.mp4` | `fba484bb8b370559...` (exact hash in `DELIVERY_MANIFEST.json`) | J2033/J2034 | Short A S03 (`0.50..3.74s`, `x=320->680`) |
| `P4:02_spray_paint` | `part04/raw/v01/02_spray_paint_t1.mp4` | `8a7b7d907240f959e7db25d3c9108439c5df79ae1b8261cde7079ac23342b092` | J1192/J1237 | Short B S05 (`1.20..4.26s`, `x=360->440`, moving-plate alternation) |
| `P4:02_spray_paint_c2` | `part04/raw/v01/02_spray_paint_c2_t1.mp4` | `0a6279c069fae36a0df291a33d25cce35d0a3aefd4965ebf21ef3e4281bb0f85` | J1192/J1237 | Short B S06 moving-plate background under `dots_square` |
| `P4:05_minute_second` | `part04/raw/v01/05_minute_second_t1.mp4` | `7f56f05930cefc854aabde17cd204510771dfbaaa5faa2f6b410facebbd3cd66` | J1192/J1237 | Short B S01 (`2.00..4.82s`, `x=720->875`) + loop (`1.00..2.00s`, `x=680->720`) |
| `P4:06_pretty_nearly` | `part04/raw/v01/06_pretty_nearly_t1.mp4` | `af487165258059d44e1f3ad9682d80d50c2239882f5495c82d7907a3e98d47ad` | J1192/J1237 | Short B S03 (`1.00..3.86s`, `x=437->460`) |
| `P4:06_pretty_nearly_c1` | `part04/raw/v01/06_pretty_nearly_c1_t1.mp4` | `eb3f5d5030b9b18a545ce0922377771c10f499f14f08d1b64239adca975078cf` | J1192/J1237 | Short B S07 (`1.00..4.17s`, `x=437->460`) |
| `P5:01_one_law` | `part05/raw/v01/01_one_law_t1.mp4` | `ed89eb1e5c519f18984284d144ae924616f6d08560179fc6b2e4c3942e6053a0` | J1192/J1237 | Short B S08 (`1.00..4.66s`, `x=437->450`) |
| `P5:09_orchard_dusk` | `part05/raw/v01/09_orchard_dusk_t1.mp4` | `1266d61a73ccb6854051836495df72e9f0d0cbd71dd83698d981d887b9a5a41f` | J1192/J1237 | Short A S08 (`0.50..3.54s`, `x=360->480`) |

Four £0 native `936x1664` (`1.00x`, full-bleed) portrait house code graphics derived from the parent 16:9 `code_graphics_v01` (leaving all 16:9 Long assets untouched) and staged on NAS `07_Edit-Project/code_graphics_v01/`:
- `code_graphic_009_short_A_s02_km_a_second_9x16.mp4` (`819e453dced47e4ad7ef8f6b014699f0e15bfe5334f807f18b25790503c79218`, `2.933 s`, single Short DATA label `SIDEWAYS AND DOWN`)
- `code_graphic_009_short_A_s07_orbit_teach_9x16.mp4` (`18b4dbf94c142f0fe9e5f4ed9b3f7006784fadeee6ca06a6b17cf53e5bfd98ef`, `2.667 s`, pure falling-sideways orbit diagram)
- `code_graphic_009_short_B_s04_sixty_earths_9x16.mp4` (`4f63cdac24b871242f3c73226f6a0d38dfd3a81cfadbec54d4401c02c33007c6`, `3.033 s`, pure 60-Earths chain diagram, no label clash with 9–14 s title)
- `code_graphic_009_short_B_s06_dots_square_9x16.mp4` (`45fe23301fe4044076e66623b445e02863230f0db3c8cedda2ea9f6265afa58f`, `3.133 s`, moving-plate composite over `P4:02_spray_paint_c2` with single Short DATA label `SIXTY TIMES SIXTY`)

## 2. Delivered Masters (`936x1664`, `2.311x <= 2.35x`, `30 fps`, CFR)

### 2.1 Short A — `hos_009_short_A_v01.mp4` (*What Would Happen If the Moon Stopped Moving?*)
- **Master SHA-256:** `43dbeb3ae42ed682814af56cec2bde0a3626a758c949174145af2db243278332` (`11,851,675` bytes)
- **NAS path:** `/Volumes/data/studio-live/History Of Science/02_Video-Projects/009_The-Falling-Moon-Gravity/10_Shorts/J2171/short_A/hos_009_short_A_v01.mp4`
- **iCloud HOS UAT path:** `HOS UAT/009_The-Falling-Moon-Gravity/10_Shorts/hos_009_short_A_v01.mp4` (verified identical SHA-256)
- **Metrics:** `25.4 s` (`24.32 s` VO-locked v02 + `1.00 s` loop tail; VO-locked Shorts exempt from 19 Nov 16–19 s rework per `studio/RULES.md`), hook `"IT'S FALLING"` (`0.0–2.0 s`, `#FFE000` on `FALLING`, clear of Moon and Newton), promoted-long title `"Why Doesn't the Moon Fall to Earth?"` at `9.0–14.0 s`, payoff `"An orbit isn't floating at all..."` starting at `19.64 s` (`77.6% >= 70%`), `-14.0 LUFS` / `-1.9 dBTP`, full `ffmpeg` decode `0` errors.
- **Gates (6/6 exit 0, 0 waivers):** `polish_gate` PASS (`0/9` fail), `picture_qa` PASS (`0/9` fail), `music_gate` PASS (`hos_009_score_v04_synth.wav`), `sfx_kit level` PASS (`VO -19.4 LUFS, SFX -46.1 LUFS`), `vo_check_py312` PASS, `gate_shorts_open.py --air-date 2026-11-27` PASS (`motion=17.47`, `f0diff=3.86`, `cut1=2.8s`, `vo_onset=0.10s`, `tail_gap=1.16s`, `0/26` padded at 1/s, `0/51` at 2/s).

### 2.2 Short B — `hos_009_short_B_v01.mp4` (*How Did Newton Discover Gravity?*)
- **Master SHA-256:** `e6e5ae3ff3be4856cc0a45af78f17f6b410974784a67fd3e6bba8222bc48037a` (`10,725,616` bytes)
- **NAS path:** `/Volumes/data/studio-live/History Of Science/02_Video-Projects/009_The-Falling-Moon-Gravity/10_Shorts/J2171/short_B/hos_009_short_B_v01.mp4`
- **iCloud HOS UAT path:** `HOS UAT/009_The-Falling-Moon-Gravity/10_Shorts/hos_009_short_B_v01.mp4` (verified identical SHA-256)
- **Metrics:** `25.5 s` (`24.48 s` VO-locked v04 + `1.00 s` loop tail), preserves both `"In one minute"` and `"in one second"` intervals, hook `"1 MINUTE = 1 SECOND"` (`0.0–2.0 s`, `#FFE000` on `1 SECOND`, clear of Moon), promoted-long title `"Why Doesn't the Moon Fall to Earth?"` at `9.0–14.0 s`, payoff `"And the numbers matched. One pull, for apples and Moons."` starting at `19.88 s` (`78.0% >= 70%`), `-14.3 LUFS` / `-1.8 dBTP`, full `ffmpeg` decode `0` errors.
- **Gates (6/6 exit 0, 0 waivers):** `polish_gate` PASS (`0/9` fail; right-half crop avoids split-panel seam completely), `picture_qa` PASS (`0/9` fail), `music_gate` PASS (`hos_009_score_v04_synth.wav`), `sfx_kit level` PASS (`VO -24.1 LUFS, SFX -54.1 LUFS`), `vo_check_py312` PASS (`0` fails, `0` warnings), `gate_shorts_open.py --air-date 2026-11-30` PASS (`motion=11.29`, `f0diff=2.99`, `cut1=2.83s`, `vo_onset=0.00s`, `tail_gap=1.12s`, `0/26` padded at 1/s, `1/51` no-edge soft-sky warn at 2–3 s verified full-bleed on `open_sheet.jpg`).

## 3. Perceptual Scope & Immediate Handoff
- All 4 contact sheets (`open_sheet.jpg` and `rows_sheet.jpg` for both Short A and Short B) were inspected directly via `image_input`; NAS copies live under `10_Shorts/qa_short_A_v01/` and `10_Shorts/qa_short_B_v01/` alongside all 4 code-graphic hero stills.
- Under `AGENTS.md` (4 Nov 2026 order), automated gates and frame sheets are verified here without claiming continuous audio/moving-video perception; actual watching/listening is Ben's final UAT watch once a non-producer reviewer verifies this PR, checks NAS/UAT SHA-256 parity, confirms unique working Play links, and sets `awaits_ben` (`due: 2026-11-24T18:00Z`).
- Conditional scheduling reminder: HOS 009 long (planned `2026-11-26T18:00:00Z`, not yet uploaded) MUST be Public before either Short airs; also note Mon `2026-11-30` is the brief's conditional target while the 7 Nov HOS week rule uses Sat/Fri/Sun/Tue `11:30` slots (e.g., Fri `27 Nov` / Sun `29 Nov` or Sat `28 Nov` / Tue `1 Dec`).
