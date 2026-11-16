# HOS 010 Shorts A & C — J2172 Inventory & £0 Assembly Report

- **Job:** `J2172` (`ref: J2023`)
- **Assembler:** `gemini` (`gemini-agy`, £0 / 0 credits)
- **Date:** `2026-11-16`
- **Scope:** £0 preparation and assembly only. Zero generation, zero credit spend, zero YouTube upload/schedule/privacy/retitle changes, zero Buffer writes.

## 1. Pre-Work Re-Inventory

### 1.1 Duplicate Public / Scheduled Ideas Check
- **Snapshot checked:** `05_Analytics/hos/snapshots/2026-11-16.json` (`64` HOS videos) plus `00_Brand/Channel-Setup/audits/shorts_open_library/library.json` (`air-date` checks for `2026-12-04`, `2026-12-06`, and `2026-12-07`).
- **Result:** `0` public or scheduled HOS videos or Shorts cover dinosaurs, the Alvarez Gubbio clay line / iridium anomaly, asteroid extinction, or living birds as avian dinosaurs.
- **Parent long readiness:** HOS `010` (*What Killed the Dinosaurs Was Hidden in a Line of Clay*, planned Thu `2026-12-03T18:00:00Z`) is **not uploaded yet** (`status.json` `picture` 12/65 plates). Under channel rules, **neither Short may air before HOS 010 long is public**. Also note `2026-12-07` is a Monday, whereas locked HOS Short weekdays (`AGENTS.md`, 7 Nov 2026) are Saturday, Friday, Sunday, and Tuesday (`2026-12-04` Fri and `2026-12-06` Sun or `2026-12-08` Tue).

### 1.2 Accepted VO & J0862 / J1004 Disposition
- **Short A (`What Killed the Dinosaurs?`):**
  - Source MP3: `10_Shorts/vo_v02/hos_010_short_A_v02.mp3` (`68d88b5b5883f2376bcec29c26d77efea7634d5c7705693f41202ca587b927fb`)
  - Source WAV: `10_Shorts/vo_v02/hos_010_short_A_v02.wav` (`2488aa8b49beb3a642597e08f30ca53e723fbee00cd21ad8bdc581a9293ff228`)
  - Disposition (`J0862` / `J2279` / `J2281` + `J1004` Option A1): accepted word-preserving pause-trimmed v02 take with `S1` `atempo=1.06` (`<= 1.06` house cap), `S2..S4` `1.00x`, VO onset `0.038 s`, hook sentence end `2.849 s` (`<= 3.0 s`), speech end `22.169 s`, `1.000 s` visual loop tail -> `23.289 s` (`23.3 s` container). `vo_check_py312.sh` PASS (`59/59` words, `159 wpm`).
- **Short C (`Are Birds Really Dinosaurs?`):**
  - Source MP3: `10_Shorts/vo_v02/hos_010_short_C_v02.mp3` (`20432ecd645b28e9fdc051578a284cb2845bd09f3040170b192089b256055b87`)
  - Source WAV: `10_Shorts/vo_v02/hos_010_short_C_v02.wav` (`ca814ab01ad72fde015b4e157638b5e346d592e5df54cefe97e38969340fcb0c`)
  - Disposition (`J0862` / `J2279` / `J2281`): accepted `1.00x` v02 take, VO onset `0.100 s`, hook sentence end `1.880 s` (`<= 3.0 s`), speech end `22.500 s`, `1.000 s` visual loop tail -> `23.560 s` (`23.6 s` container). `vo_check_py312.sh` PASS (`57/57` words, `154 wpm`).

### 1.3 Approved 12/12 Moving Plates & £0 Code Graphics
All 12 moving plates were minted by `cursor` on Flow Veo 3.1 (`J2269`), reviewed KEEP by non-producer `claude` (`desk #180` comments `6905894181` & `6907453362`), and locked KEEP with `keep=true` in `J2271` / `J2928`:

| Row ID | NAS File (`04_Generated-Clips/...`) | SHA-256 | Producer | Crop / Window Used |
|---|---|---|---|---|
| `P1:01_clay_line` | `part01/P01_01_clay_line_t1.mp4` | `dc7329d38a035b1d54c8f0da8068419d1261a7eb00348d886416cc5f2f5ab0dc` | `cursor` | `Short A S01` `t=1.000..3.849s` (`x=437`), `loop_tail` `t=0.000..1.000s` (`x=437`, seamless wrap into `t=1.000s`) |
| `P2:01_walter_hammer` | `part02/P02_01_walter_hammer_r1_t1.mp4` | `eda11284e733b5b1172a76524e879964f0003c3252431d98c4698de4a35cb4e6` | `cursor` | `Short A S02` `t=0.000..3.340s` (`x=620`) |
| `P2:03_tiny_shells` | `part02/P02_03_tiny_shells_r1_t1.mp4` | `1898afb649bf891169571df454731eb0c154a9ac5af4d82ba30092a346e04d54` | `cursor` | `Short A S03` `t=0.000..3.360s` (`x=437`) |
| `P2:05_almost_none` | `part02/P02_05_almost_none_t1.mp4` | `ba9bc1dc6924b4b53eb01297be7767cd6a6a5e446670d88b45c7d090425ef871` | `cursor` | `Short A S04` `t=0.000..3.720s` (`x=380->460`) |
| `P3:08_asaro_michel` | `part03/P03_08_asaro_michel_t1.mp4` | `7cd3ad8a6f867a8a3ac0f07780b7c2aa3307b4212a34c2150ed930c18da6e314` | `cursor` | `Short A S05` `t=0.000..3.120s` (`x=180`) |
| `P4:06_dust_veil` | `part04/P04_06_dust_veil_t2.mp4` | `a2bf9d295f3c8623d651ad9e4bc691b9d72b90c64042e28397a5e8f8b237da71` | `cursor` | `Short A S07` `t=2.000..5.000s` (`x=540`); `Short C S02` `t=1.750..5.070s` (`x=540`) |
| `P5:08_all_at_once` | `part05/P05_08_all_at_once_t2.mp4` | `db377bd25cb147967a796e908be774c8a6b01564a81463506ec894fd275657f3` | `cursor` | `Short C S04` `t=1.250..3.750s` (`x=380`) |
| `P5:09_robin` | `part05/P05_09_robin_t2.mp4` | `c509ba1152414e87951ba324943568aa1a866886a33571a76e204ab0c07877cc` | `cursor` | `Short C S01` (`R6c`) `t=4.250..6.130s` (`x=521.944->535`), `loop_tail` `t=3.250..4.250s` (`x=515->521.944`, seamless wrap into `t=4.250s`) |
| `P5:09a_pigeon_pavement` | `part05/P05_09a_pigeon_pavement_t1.mp4` | `d1807ac9577041664ed8c7fa355bd08475a76fb02255bc5a3ba587209446e0df` | `cursor` | `Short C S05` `t=1.100..3.740s` (`x=360->530`) |
| `P5:13a_gull_seaside` | `part05/P05_13a_gull_seaside_t1.mp4` | `e404e79514046d1f70a2395629a77e12e0b4e2444d010a630a8bd6f5e0c216e7` | `cursor` | `Short C S06` (`12d` Claude KEEP tracked crop) `t=4.300..7.020s` (`x=605->520`) |
| `P5:10_explorer_robin` | `part05/P05_10_explorer_robin_t2.mp4` | `b4024f56b4d7c12dc586684aa0918445f2c4a6b016380a08498e7b1c5d6390b3` | `cursor` | `Short C S07` `t=2.050..5.650s` (`x=375->410`) |
| `P5:12_clay_callback` | `part05/P05_12_clay_callback_t2.mp4` | `781f95958a511e5c4a1241c0a372f2ccba4b3d4a02145520c9fd60b9afab2684` | `cursor` | `Short C S08` (`R4b`) `t=1.050..4.230s` (`x=437`) |

Full-bleed `936x1664` (`9:16`, `1.00x` native portrait, zero bars/padding) house-parchment code graphics built at £0 in `_build_j2172_shorts_v01.py` from the parent `16:9` graphics (`code_graphic_010_p4_01_iridium_spike.mp4` `f9b504cf...` and `code_graphic_010_p5_11_why_survive.mp4` `0e71b03e...`) and staged on the NAS:
- `07_Edit-Project/code_graphics_v01/code_graphic_010_short_A_s06_iridium_spike_9x16.mp4` (`3352a3d42164aa4e967cebdfdbc9fc7ebd60c299d7eb589d1c51a46d984338e6`, `2.900 s`)
- `07_Edit-Project/code_graphics_v01/code_graphic_010_short_C_s03_why_survive_9x16.mp4` (`03716128fb6792563e34c1dfdaa50e47cea1e092afdf9ba121e8537f8d48867d`, `2.733 s`)

## 2. Delivered Masters (`936x1664`, `2.311x <= 2.35x`, `30 fps`, CFR)

### 2.1 Short A — `hos_010_short_A_v01.mp4` (*What Killed the Dinosaurs?*)
- **Master SHA-256:** `ea29e26487d6631416449c9adf712f51b1b9508db06b7b6c29edc4236970fe59` (`12,952,218` bytes)
- **NAS path:** `/Volumes/data/studio-live/History Of Science/02_Video-Projects/010_Alvarez-Clay-Line-Dinosaurs/10_Shorts/J2172/short_A/hos_010_short_A_v01.mp4`
- **iCloud HOS UAT path:** `HOS UAT/010_Alvarez-Clay-Line-Dinosaurs/10_Shorts/hos_010_short_A_v01.mp4` (verified identical SHA-256)
- **Metrics:** `23.3 s` (`23.289 s`), hook `"THE LINE"` (`0.0–2.0 s`, off the clay seam), promoted-long title `9.0–14.0 s`, payoff `"packed with a rare metal from space"` at `17.069 s` (`73.3% >= 70%`), `-14.4 LUFS` / `-1.8 dBTP`, full `ffmpeg` decode `0` errors.
- **Gates (all exit 0):** `polish_gate` PASS (`0/8` fail), `picture_qa` PASS (`0/8` fail), `music_gate` PASS, `sfx_kit level` PASS (`3` events, bed `-26.3 dB`, SFX `-20.7 dB` vs VO), `vo_check_py312` PASS, `gate_shorts_open.py --air-date 2026-12-04` PASS (`motion=24.31`, `f0diff=4.16`, `0/47` padded frames).

### 2.2 Short C — `hos_010_short_C_v01.mp4` (*Are Birds Really Dinosaurs?*)
- **Master SHA-256:** `698db62789e1e6884ae15797dc51083c39bbc0ee3c0cc1ecf83f92e2e87a0359` (`13,612,892` bytes)
- **NAS path:** `/Volumes/data/studio-live/History Of Science/02_Video-Projects/010_Alvarez-Clay-Line-Dinosaurs/10_Shorts/J2172/short_C/hos_010_short_C_v01.mp4`
- **iCloud HOS UAT path:** `HOS UAT/010_Alvarez-Clay-Line-Dinosaurs/10_Shorts/hos_010_short_C_v01.mp4` (verified identical SHA-256)
- **Metrics:** `23.6 s` (`23.560 s`), hook `"STILL HERE"` (`0.0–1.88 s`, upper-band `5.5%–23.2% H` clear of the robin's head/eye), WHEN card `"66 MILLION YEARS AGO"` (`2.20–5.15 s` with `0.35 s` fades inside `16:9` band), promoted-long title `9.0–14.0 s`, payoff `"Every bird you have ever seen is a living dinosaur"` at `16.560 s` (`70.3% >= 70%`), `-14.1 LUFS` / `-1.8 dBTP`, full `ffmpeg` decode `0` errors.
- **Gates (all exit 0):** `polish_gate` PASS (`0/9` fail, `1` sky-detail warn on `s06` gull over open sea), `picture_qa` PASS (`0/9` fail), `music_gate` PASS, `sfx_kit level` PASS (`4` events, bed `-26.9 dB`, SFX `-21.2 dB` vs VO), `vo_check_py312` PASS, `gate_shorts_open.py --air-date 2026-12-07` (and `2026-12-06`) PASS (`motion=14.71`, `f0diff=1.99`, `0/48` padded frames).

## 3. Perceptual Scope & Immediate Handoff
- Contact sheets (`open_sheet.jpg`, `rows_sheet.jpg`, `picture_qa_review.jpg`, and both `9:16` code-graphic hero stills) were inspected directly via `image_input`.
- Under `AGENTS.md` ("Ben's final watch is the watch-and-listen check", 4 Nov 2026), automated gates and frame sheets are verified here without claiming continuous audio/moving-video perception; the actual watch-and-listen step is Ben's UAT watch once a non-producer reviewer (`claude` / `codex`) verifies the package and sets `awaits_ben` with working unique Play links.
