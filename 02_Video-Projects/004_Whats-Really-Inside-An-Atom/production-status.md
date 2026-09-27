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
| Plate boards (Step 4) | **`part-0N_plates_v02.json`.** Part 01 `mint: true` · Parts 02–05 `mint: false` · Explorer ×3 (P02/P04/P05) · no SEE labels · no Explorer in first minute |
| Picture | **Part 01 STOPPED** (Ben 27 Sep 14:10). Flow Ultra out of credits; Gemini Veo fallback: **10 KEEP / 7 FAIL**. VO now KEEP; picture restarts only on Ben's go (moving-picture sign-off, point 5). See `PART01_MINT_STOP_2026-09-27.md`. |
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
| 01 Cold open | 0:00–1:10 | none | 17 (split 07 at 0:32) | **true** |
| 02 The Table That Broke Its Own Rule | 1:10–2:41 | 1:10 · ~1.5 s | 10 | false |
| 03 The Crumb Inside the Atom | 2:41–4:05 | 2:41 · ~1.5 s | 8 | false |
| 04 The Shell That Bounced Back | 4:05–5:54 | 4:05 · ~1.5 s | 10 | false |
| 05 Counting With X-rays | 5:54–8:18 | 5:54 · ~1.5 s | 11 | false |

**Next:** VO v04 is KEEP (27 Sep). Before any more picture spend, Ben decides how to finish Part 01's 7 missing plates (Flow credits vs the Gemini API Veo fallback) and reviews the 10 kept plates in motion. Do not assemble rough. Do not start Part 02.
