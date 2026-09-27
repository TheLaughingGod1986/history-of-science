# Production status — 004 Why Is the Periodic Table in This Order?

| Field | Value |
|---|---|
| Slug | `004_Whats-Really-Inside-An-Atom` |
| Channel | `@HistoryOfScienceYT` only |
| Topic | Ben picked 26 Sep 2026 (the atom; why the periodic table has its order) |
| Title | *Why Is the Periodic Table in This Order?* (main); Test & Compare *What's Really Inside an Atom?* and *How Small Can You Cut Gold?* |
| Script | `01_Script/atom_script_master_v02.md`. **Spoken words LOCKED.** VISUAL MUST **re-timed from VO v04** (27 Sep). |
| Script review | 88.9. Passed by hand by Ben, 26 Sep 2026 |
| Pre-build vidIQ audit | Signed off by Ben, 26 Sep 2026 (vidIQ waived) |
| Episode gate | Passed by Ben (manual), 26 Sep 2026 |
| VO | **v04 KEEP** (Ben, 27 Sep 2026, after listening at 3:38, 6:06 and 7:39; the three `vo_check` word FAILs there are the transcriber, not the take). Masters in `02_Voiceover/05_Master/`. |
| Re-time (Step 3) | **DONE from v04.** `07_Edit-Project/VO_RETIME_v02.json` · script VISUAL MUST + chapter cards updated |
| Plate boards (Step 4) | **`part-0N_plates_v02.json`.** Parts 01–03 `mint: false` (03 rough v01 pending Ben) · 04/05 `mint: false` · Explorer used ×1 (P02); remaining P04/P05 · no Explorer in Part 03 |
| Picture | **Part 01 rough v05 PASS** · **Part 02 rough v01 PASS** (“best yet”) · **Part 03 rough v01 PASS** (Ben: “fine”). **Part 04 minting** next. |
| Runtime (VO v04) | **498.285 s = 8:18** |
| Air | Thu 15 Oct 2026 18:00 UK, normal publish. Fallback Thu 22 Oct |

---

## VO v04 — KEEP (Ben, 27 Sep 2026)

**Route:** `ffmpeg -af atempo=1.03` on each v03 part master (pitch-safe). v01–v03 kept.

| Part | Start | Duration | Mean dB (mp3) | Peak dB | WAV sha256 |
|---|---|---|---|---|---|
| 01 | 0:00 | 69.813 s (1:10) | -23.8 | -4.2 | `9bd187b1dfb7dfd7e95071d10db34a020d7f3bfe99feb66040fab47eda36d44e` |
| 02 | 1:10 | 91.204 s (1:31) | -22.0 | -4.1 | `683aa97018b1acadc2beccffdc975441a60e21f2b11ed96e0c6b98d684bc85a2` |
| 03 | 2:41 | 83.730 s (1:24) | -23.4 | -4.1 | `74fcf8c2278ba170b46f132998067ce0e9a56ed8883e2b92442ebd49471eec36` |
| 04 | 4:05 | 109.022 s (1:49) | -24.7 | -4.1 | `461f384a6a4c7b6c7ff100587113f63541dd5f6dd68e8da2a765daec20fecf0a` |
| 05 | 5:54 | 144.516 s (2:25) | -24.3 | -4.4 | `191d07c4c7f1430ac8d1da465a40793ab898d935d9b4e9571623df7e69953ca8` |
| **Total** | — | **498.285 s (8:18)** | spread 2.7 dB | — | meta `02_Voiceover/05_Master/VO_MASTERS_v04.json` |

| Check | Result |
|---|---|
| Title question | **0:08.78** |
| Dalton “each kind a weight” | **PASS** |
| “It's a count.” | **PASS** |
| `vo_check.py` | **Rerun 27 Sep** with faster-whisper + PR #141. Parts 01–04 **PASS** (word check ran). Part 05 **FAIL** + listen **FAIL** at Ben holds 3:38 / 6:06 / 7:39 — see `VO_CHECK_v04_RERUN.md`. Ben listened at all three: **KEEP**. |
| Loudness | means −22.0…−24.7; peaks −4.1…−4.4; no in-part silence >1.5 s |

Phone: `iCloud Drive/HOS UAT/004_Whats-Really-Inside-An-Atom/02_Voiceover/05_Master/`  
Listen: **`hos_004_vo_all_parts_listen_v04.mp3`**  
Listen sha256: `e9e47e32f4db1838794bc84e86ed37be882982c43ff8c4707862e29a54af1dbd`

### Re-time + plates (from v04)

| Part | Film window | Chapter card | Plates | mint |
|---|---|---|---|---|
| 01 Cold open | 0:00–1:10 | none | 17 (split 07 at 0:32) | false (PASS) |
| 02 The Table That Broke Its Own Rule | 1:10–2:41 | 1:10 · ~1.5 s | **20** (4–6 s splits) | false (PASS) |
| 03 The Crumb Inside the Atom | 2:41–4:05 | 2:41 · ~1.5 s | **19** (4–6 s splits) | false (PASS) |
| 04 The Shell That Bounced Back | 4:05–5:54 | 4:05 · ~1.5 s | 10 | false |
| 05 Counting With X-rays | 5:54–8:18 | 5:54 · ~1.5 s | 11 | false |

**Next:** Part 04 Flow mint → `hos_004_part04_rough_v01.mp4`. STOP for Ben after Part 04 rough. Do not start Part 05.

---

## Part 01 rough UAT (27 Sep 2026)

| Cut | Duration | Notes |
|---|---|---|
| `hos_004_part01_rough_v01.mp4` | 128.7 s | assembly bug (kept) — full Veo lengths |
| `hos_004_part01_rough_v02.mp4` | 69.813 s | board windows; silent plates + VO |
| `hos_004_part01_rough_v03.mp4` | 69.813 s | v02 picture + TEMP music bed |
| `hos_004_part01_rough_v04.mp4` | 69.813 s | Ben 3-scene remints + same TEMP bed as v03 |
| `hos_004_part01_rough_v05.mp4` | 69.813 s | plate 12 straight-beam remint + same TEMP bed |

**Ben PASS Part 01 rough v05** — Sun 27 Sep **17:11 UK**, judged **in motion** (not stills). Garbled background jar label **“lpod”** accepted as-is. Do not remint Part 01 unless CoS sends a later FAIL with stills. Locked cut for Part 01 UAT: `hos_004_part01_rough_v05.mp4` sha256 `71d7c70798c77ce2ecb02c37ad043fd98117a2209a84899236337fee8b952add`.

iCloud: `HOS UAT/004_Whats-Really-Inside-An-Atom/09_Final-Export/`

---

## Part 02 rough UAT (27 Sep 2026) — PASS

| Cut | Duration | sha256 | Notes |
|---|---|---|---|
| `hos_004_part02_rough_v01.mp4` | **91.204 s** | `620ce51250028495a588f25967dddfaa9c6136dc4172c7b0ce1ee609f103f1d2` | 20 board windows · v04 VO · TEMP bed · Flow Veo 3.1 scenery_only CDP |

**Ben PASS Part 02 rough v01** — judged “best yet”. Do not remint Part 02 unless CoS sends a later FAIL with stills.

**Mint record:** credits **2502 → 2162**. KEEP **20**/20. Explorer plate `16_explorer_te_before_i` used (film-wide 1 of 3). Named-Mendeleev Flow prompts silent-fail — describe people instead going forward.

**Log:** `07_Edit-Project/PART02_MINT_LOG_v01.json`

iCloud: `HOS UAT/004_Whats-Really-Inside-An-Atom/09_Final-Export/hos_004_part02_rough_v01.mp4`

## Part 03 rough UAT (27 Sep 2026) — PASS

| Cut | Duration | sha256 | Notes |
|---|---|---|---|
| `hos_004_part03_rough_v01.mp4` | **83.733 s** | `d62e0ed096ead8ec52666ca07476f973aeaae7635b70a16faaac45f14ec518e0` | 19 board windows · v04 VO · TEMP bed −20 dB sidechain · Flow Veo 3.1 scenery_only CDP |

**Mint:** credits **2162 → 1162** (spent **1000**). Plate KEEP **19**/19 (plate 19 explosion framing remint after near-still FAILs). Quality on tube-glow plates. No Explorer. Unnamed physicist in prompts.

**Log:** `07_Edit-Project/PART03_MINT_LOG_v01.json`

iCloud: `HOS UAT/004_Whats-Really-Inside-An-Atom/09_Final-Export/hos_004_part03_rough_v01.mp4`

**Ben PASS Part 03 rough v01** — “fine”. Do not remint Part 03 unless CoS sends a later FAIL with stills.

## Part 04 rough UAT — minting

Board: `part-04_plates_v02.json` (4–6 s splits). Explorer once (stadium pea). Credits start **1162** · Gemini Veo 3.1 API fallback if Flow would drop below ~150 buffer. STOP after `hos_004_part04_rough_v01.mp4` — do not start Part 05.


---

### Ben UAT fixes → v04 (27 Sep 16:00 UK) · Part 01 record

**Plate mapping (v03 screenshots → board):**

| Ben image | Plate | t_s |
|---|---|---|
| Image 1 — scientist + golden beam to head + ATOMOS plinths | `12_1913_targets` | 52.748 |
| Image 2 — helmeted blue-suit little man + fake wall tiles | `09_uncuttable_blur` | 36.091 |
| Image 3 — coin/knife + ATOM on table (open) | `01_coin_halves` (+ spine `15_knife_coin_return` @ 63.853) | 0.000 |

**Remints (Flow Ultra CDP `benoats@googlemail.com`, scenery_only, strip Veo audio):**

| Plate | Tries | Model | Change |
|---|---|---|---|
| `01_coin_halves` | 1 KEEP | Fast | Successive gold-coin halvings emphasised |
| `09_uncuttable_blur` | 2 KEEP (try2 framing) | Fast | No character; ECU magnifier blur (no Explorer) |
| `12_1913_targets` | 1 KEEP | **Quality** | Glow inside tube/apparatus; no laser-to-head; no ATOMOS |
| `15_knife_coin_return` | 1 KEEP | Fast | Knife + coin halves return (open spine) |

Credits: before **2692** → after **2602** (spent **~90**). Log: `PART01_MINT_LOG_v01.json` · `ben_fix_2026_09_27`.

v04 sha256: `63cc242eeeb2ce2cd38d69a7f0459f03ab8791c2d8892912a8971cd74e49927c`


### Plate 12 straight-beam remint → v05 (Ben 27 Sep 16:33 UK)

Problem: tube glow had an S-shaped wiggle. Real X-ray/cathode beams run straight.

| Field | Value |
|---|---|
| Plate | `12_1913_targets` @ 52.748 s |
| Tries | **1 KEEP** (Quality) |
| Credits | before **2602** → after **2502** (spent **100**) |
| Account | `benoats@googlemail.com` Flow Ultra CDP |
| Keep | brass+glass apparatus, targets on bench, no person in beam, no ATOMOS; prompt locks **straight beam, no curls, no wiggle, no squiggle** |
| v05 sha256 | `71d7c70798c77ce2ecb02c37ad043fd98117a2209a84899236337fee8b952add` |
| Log | `PART01_MINT_LOG_v01.json` · `ben_fix_12_straight_2026_09_27` |


### TEMP music bed (UAT only — final bed at full-film assembly)

| Field | Value |
|---|---|
| Status | **TEMP** |
| File | `05_Music/hos004-part01-temp_score_bed_v01.mp3` |
| sha256 | `dfcedde16055c3046ad45db7090f90466621d16e9b594b11edec61713ff08a97` |
| Generator | `04_Audio/tools/generate_music_bed.py --generate` (ElevenLabs `music_v2`, force_instrumental) |
| Prompt | `warm curious documentary underscore, soft strings, light piano, gentle wonder, no vocals, leaves room for voice` |
| Length | 75.05 s (requested 75000 ms) |
| Mix | bed **-20 dB** relative to VO (`volume=0.1`); `sidechaincompress` threshold=0.018 ratio=8 attack=20 release=500 under speech; **2.5 s** fade-out at part end; plates silent (no Veo audio); VO level unchanged |
| v03 sha256 | `a4902dacbd99c8411921ac8e60898d79697dcbeea09a5c50c9c61215286248df` |
| Levels (measured) | VO mean **-23.6 dB** / peak **-4.0 dB**; bed under speech mean **~-51.5 dB**; bed in gaps mean **~-40.8 dB**; mix peak **-4.0 dB** (below −1 dB) |

Meta: `07_Edit-Project/part01_rough_v03_land_meta.json` · `part01_rough_v04_land_meta.json` · assemblers `_assemble_part01_rough_v03_music.py` · `_assemble_part01_rough_v04.py`
