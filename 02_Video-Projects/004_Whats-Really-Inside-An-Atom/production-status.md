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
| Plate boards (Step 4) | **`part-0N_plates_v02.json`.** Parts 01–04 `mint: false` (04 rough v01 pending Ben) · 05 `mint: false` · Explorer used ×2 (P02 + P04 stadium pea); remaining P05 · no Explorer in Part 03 |
| Picture | **Part 01–05 PASS.** **Full join v03 PASS (Ben, 29 Sep 2026)** sha `f88cb9d4…65244`. Finishing: final music bed + captions → `hos_004_full_v01` (UAT). |
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
| 04 The Shell That Bounced Back | 4:05–5:54 | 4:05 · ~1.5 s | **22** (4–6 s splits) | false (rough v01) |
| 05 Counting With X-rays | 5:54–8:18 | 5:54 · ~1.5 s | 11 | false |

**Next:** STOP for Ben — listen to music on `hos_004_full_v01`. Captions ready. STEP 3 title not started.

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

## Part 04 rough UAT (27 Sep 2026) — PENDING Ben

| Cut | Duration | sha256 | Notes |
|---|---|---|---|
| `hos_004_part04_rough_v01.mp4` | **109.033 s** | `49efa91a197aa74dd67d686a5d2df1b6d48eeac4cfc2d898d82e03c314e7f9fa` | 22 board windows · v04 VO · TEMP bed −20 dB sidechain · Flow Veo 3.1 scenery_only CDP |

**Mint:** credits **1162 → 162** (spent **1000**). Plate KEEP **22**/22. All path=`flow-cdp` (Gemini fallback armed but not needed — stayed above ~150 buffer). Quality on glow plates. Explorer once: `16_explorer_stadium_pea` (film-wide 2/3). Unnamed physicists in prompts.

**Log:** `07_Edit-Project/PART04_MINT_LOG_v01.json`

iCloud: `HOS UAT/004_Whats-Really-Inside-An-Atom/09_Final-Export/hos_004_part04_rough_v01.mp4`

**STOP for Ben.** Do not start Part 05. Do not label the rough KEEP/LOCKED — plate-level KEEP only in the mint log.


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

## Part 04 rough v02 — awaiting Ben UAT (v01 was FAIL)

- **Cut:** `hos_004_part04_rough_v02.mp4`
- **sha256:** `157feaef7bd21236aeafc3e953fe461fe2ee95896bb868d57357c9c1c2c1e1f5`
- **Duration:** 109.033 s · VO v04 KEEP · TEMP bed −20 dB sidechain
- **Audit:** `07_Edit-Project/PART04_V01_AUDIT.md` (KEEP 4 · FIX 18)
- **Mint log:** `07_Edit-Project/PART04_MINT_LOG_v02.json`
- **Paths:** Gemini API Veo 3.1 for most FIX plates; Flow Fast for tail after Gemini 429; Flow credits ~162→~92
- **iCloud:** `HOS UAT/004_Whats-Really-Inside-An-Atom/09_Final-Export/hos_004_part04_rough_v02.mp4`
- **SUPERSEDED:** Ben PASS on v02 (28 Sep). Land PR #154. Part 05 unlocked.

## Part 04 PASS (Ben 28 Sep 2026)

- **Passed cut:** `hos_004_part04_rough_v02.mp4`
- **sha256:** `157feaef7bd21236aeafc3e953fe461fe2ee95896bb868d57357c9c1c2c1e1f5`
- **Duration:** 109.033 s · VO v04 KEEP · TEMP bed −20 dB sidechain
- **Polish check:** `PART04_V02_POLISH_CHECK.md` — `09` HOLD; `05`/`12` would improve but Gemini 429 + Flow credits=3 (buffer 150) blocked remint → **v02 stays the passed cut** (no v03).
- iCloud: `HOS UAT/004_Whats-Really-Inside-An-Atom/09_Final-Export/hos_004_part04_rough_v02.mp4`
- Land PR #154. Next: Part 05.

## Part 05 — mint blocked (28 Sep 2026)

- Pre-mint VO audit: `PART05_PRE_MINT_AUDIT.md` · board `part-05_plates_v02.json` (27 Veo @ ~5.2s + end card)
- Stills ready under `04_Generated-Clips/part05/refs/v01_stills/`
- **Mint blocked (superseded):** Flow credits were low / Gemini 429 — Ben waived buffer; mint completed via Flow → Gemini → Vertex.
- PR #155 carried Part 05 tooling + roughs.

## Part 05 PASS (Ben 29 Sep 2026)

- **Passed cut:** `hos_004_part05_rough_v03.mp4`
- **sha256:** `b391bff0dbe8a8ae0130adef4f7f3d7b79aca2cb34a934d9cf42d76e1d03363f`
- **Duration:** 144.516 s · VO v04 · TEMP bed −20 dB sidechain
- **Path:** Flow CDP → Gemini API → Vertex for last plates; remints 14 / 22 / 26 (stadium purge)
- **Mint log:** `07_Edit-Project/PART05_MINT_LOG_v01.json` (`PART05_PASSED_V03`)
- **iCloud:** `HOS UAT/004_Whats-Really-Inside-An-Atom/09_Final-Export/hos_004_part05_rough_v03.mp4`
- Do **not** label KEEP/LOCKED. Land PR #155. **Next:** full-film join `hos_004_full_join_v01` for Thu 15 Oct 18:00.

## Full join v01 (29 Sep 2026) — STOP for Ben

- **Cut:** `hos_004_full_join_v01.mp4`
- **sha256:** `70622869f9bc52c0599564bc4f2338f7dec3b547e141d084f59fcd3a199cd605`
- **Duration:** 516.685 s (8:36.69) · video 516.600 / audio 516.685 (Δ ~85 ms)
- **Parents:** 01 v05 · 02 v01 · 03 v01 · 04 v02 · 05 v03 (hash-checked, not reminted) · VO v04
- **Seams (xfade 0.40s):** 01→02 **1:09.41** · 02→03 **2:40.22** · 03→04 **4:03.55** · 04→05 **5:52.18**
- **Cream card (in P05):** **8:12.68** · **20s Studio hold from 8:16.70**
- **iCloud:** `HOS UAT/004_Whats-Really-Inside-An-Atom/09_Final-Export/hos_004_full_join_v01.mp4`
- Builder: `07_Edit-Project/_join_hos_004_full_v01.py` · notes `09_Final-Export/FULL_JOIN_V01_NOTES.md`
- Do **not** label KEEP/LOCKED. No remint. **STOP for Ben.**

## Full join v02 (29 Sep 2026) — Ben OVERRIDE · superseded (quiet mix)

- **Cut:** `hos_004_full_join_v02.mp4` · sha `02cf4a107caff44f08093a4231ef9dacafdde868483680df3bdc28ad8194b90a` · 524.700 s
- Picture/cards/seams/end OK, but `amix` without `normalize=0` halved VO+bed (~−6 dB): mean **−29.7** / peak **−9.7**. Superseded by v03.

## Full join v03 (29 Sep 2026) — **PASS** (Ben) · mix restore

Same picture, cards, seams and end as override v02. **Only** fix: `amix=inputs=2:weights=1 1:normalize=0` (same as part assemblers).

- **Cut:** `hos_004_full_join_v03.mp4`
- **sha256:** `f88cb9d47e910425519a40a6af7649626c47afbcdddf1f0f3293564c59f65244`
- **Duration:** **524.700 s** (8:44.70) · A/V delta **0.000** s
- **Levels:** full `vo_check` mean **−23.7 dB** / peak **−3.7 dB** (peak ≤ −1 OK) · film `ffmpeg -t 500.69` mean **−23.5 dB** / max **−3.7 dB** (matches parts ~−22…−24)
- **Word flags (full):** FAIL ~6:07.34 `a living`→`the living` · FAIL ~6:31.88 `sort`→`sought` · (v02 `wrong`→`rock` at ~3:59 **gone**)
- **wrong window:** Ben 3:55–4:03 ends on “pudding”; “wrong” ~**4:05.64**. Wider STT: **both** v03 and Part 03 rough hear **“wrong”** (not rock).
- **Ben PASS (29 Sep 2026)** on full join v03 (sha `f88cb9d4…65244`). Picture LOCKED for finishing.
- Finishing STEP 1–2 done: `hos_004_full_v01.mp4` (music UAT) + captions. **STOP for Ben music listen.** Steps 3–6 not started.
- **iCloud:** `HOS UAT/004_Whats-Really-Inside-An-Atom/09_Final-Export/hos_004_full_join_v03.mp4`
- Builder: `07_Edit-Project/_join_hos_004_full_v03.py` · notes `09_Final-Export/FULL_JOIN_V03_NOTES.md`

## Full_v01 (29 Sep 2026) — final continuous bed · STOP for Ben music

Replaces the five TEMP part beds. Picture = locked v03. VO v04 untouched.

- **Cut:** `hos_004_full_v01.mp4`
- **sha256:** `058e1ba7a4a986de0dec4fe1a6e0e6f47a47449ad314f979e8224a8a5ef1b4d5`
- **Duration:** **524.700 s** · A/V Δ **0.000** s · 1920×1080 30 fps CFR
- **Bed:** `05_Music/hos004-full_score_bed_v01.mp3` (−20 dB, sidechain, fade across cream, silent under hold). EL returned ~390.8 s for 506 s request → looped through cream.
- **amix:** `inputs=2:weights=1 1:normalize=0`
- **Levels:** `vo_check` mean **−23.6** / peak **−3.8** dB · film `−t 500.69` mean **−23.4** / max **−3.8** dB
- **Word flags:** known ~6:08 `a living`→`the living` · ~6:33 `sort`→`sought` · also transcriber `van den`→`van der` Broek · `a weight`→`of weight`
- **Captions (STEP 2):** `11_Upload-Package/Captions/hos_004_full_v01.en.srt` (script-locked, 90 cues, no cream/hold)
- **iCloud:** `HOS UAT/004_Whats-Really-Inside-An-Atom/09_Final-Export/hos_004_full_v01.mp4` (+ `WATCH_full_v01.txt`)
- Do **not** mark KEEP until Ben says so. No upload. **STOP for Ben** (music listen). Steps 3–6 not started.

## Full_v02 music — **PASS** (Ben, 29 Sep 2026)

Ben: “music is a pass, lets go.”

- **Ship cut:** `hos_004_full_v02.mp4`
- **sha256:** `ed870939f476d326197cdaf1403ce7064850d4286ff63aa81bc5a7584761e98e`
- **Duration:** **524.700 s** · A/V Δ **0.000** s
- **Bed (no loop):** sect1 → card05 **5:55.48** ×fade 1.5 s → `hos004-full-sect2_score_bed_v01.mp3` → cream
- Do **not** regenerate sect2. Do **not** build another mix for music. No KEEP/LOCKED label. No upload until Ben says yes to the package dry-run.
- Notes: `FULL_V02_NOTES.md` · `WATCH_full_v02.txt`
- iCloud: `HOS UAT/004_Whats-Really-Inside-An-Atom/09_Final-Export/hos_004_full_v02.mp4`

## Full_v03 — **UNUSED / PARKED**

- **Cut:** `hos_004_full_v03.mp4` · sha `503e228745d4cf87fe6f504522cbad99f6af0f9c8b038c1ed8c52da493428157`
- Built earlier (no-choir sect2 experiment). Ben PASSed **v02**, not v03. Keep aside; do not upload; do not regenerate.

## Long thumbs — **A/B v04 PASS · C v06 STOP look**

C lander: `_land_hos_004_thumb_C_live_v06.py`. Index: `THUMBS_INDEX_v06.json`.

| Variant | File | Status | Notes |
|---|---|---|---|
| **A (main)** | `hos_004_thumb_A_atom_live_v04.jpg` | **Ben PASS** | Giant glowing 3D atom |
| **B** | `hos_004_thumb_B_cut_gold_live_v04.jpg` | **Ben PASS** | Giant gold coin mid-cut |
| **C** | `hos_004_thumb_C_hidden_number_live_v06.jpg` | **STOP look** | Painted Georgia **52**/**53** top-left; **Te**/**I** fill tiles; clear BR |

T&C: 1 Atom+A · 2 Periodic+C v06 · 3 Gold+B. Family: `hos_004_thumbs_v06_family_vs_002_live.jpg`.

## STEP 5 package — **UPLOADED via Studio** (29 Sep 2026)

Ben (29 Sep 18:33): skip API/`.env` — upload through YouTube Studio CDP on Mini (HOS Chrome profile). Never Orbit.

| Field | Value |
|---|---|
| Method | Playwright CDP `:9460` · `~/.hos-chrome-youtube-studio` |
| Channel | **@HistoryOfScienceYT** · `UCXp7HkBIl1LgaznXuZHJyRg` (checked first) |
| Cut | `hos_004_full_v02.mp4` sha `ed870939…e98e` · 524.7 s |
| Title | What's Really Inside an Atom? |
| Thumb | A v04 |
| Video id | **`GHZDsiH7L7A`** · https://youtu.be/GHZDsiH7L7A |
| Visibility | **Scheduled** · private until then · **not Premiere** |
| Air | **Thu 15 Oct 2026 18:00 Europe/London** (`2026-10-15T17:00:00.000Z`) |
| Made for kids | No |
| Proof | `11_Upload-Package/Schedule/evidence_2026-09-29_studio/689_schedule_proof.png` (tooltip: public 15 October 2026 at 18:00) |
| Result JSON | `11_Upload-Package/Schedule/PACKAGE_UPLOAD_RESULT_2026-09-29.json` |

### Studio finish — phone UAT (29 Sep 18:51 → CDP v20–v25) · FINISH order 20:00

Ben app check: auto thumb · no Altered · date looked like 30 Sep. CDP finish on Mini (`:9460`, HOS Chrome). FINISH result: `11_Upload-Package/Schedule/evidence_2026-09-29_studio/FINISH_V01C_RESULT.json`.

| Item | Status |
|---|---|
| Audience (Made for Kids) | **OK — No, not Made for Kids** (checked after every save). See Made for Kids section. Proof: `URGENT_audience_004_not_made_for_kids.png` |
| Visibility | **OK — leave alone** — Scheduled **15 Oct 2026 18:00 UK**, **Set as Premiere OFF** (`aria-checked=false`, input `18:00`), title *What's Really Inside an Atom?*, private until then. Proof: `FINISH_visibility_15oct_1800_premiere_off.png` · `finish_v01c_91_visibility_final.png` |
| Altered / AI use | **OK — YES** (Ben **21:49 CHANGE OF ORDER** — overrides 20:03 No / CoS 21:02 No). “Yes, AI was used” — AI visuals + AI clone of Ben's voice. Audience re-checked not-kids after save. Proof: `ALTERED_YES_004_long_VERIFY.png` · `ALTERED_YES_2149_RESULT.json` |
| Custom thumb A v04 | **OK — LIVE** (Ben **22:26**). Ended scrambled 2-slot T&C first → uploaded `hos_004_thumb_A_atom_live_v04.jpg` via Thumbnail image input → one Save → **Changes saved** → Content list shows **A (atom)**. Audience not-kids + Altered YES re-checked. Proof: `THUMB_A_2226_08_content_list.png` · `THUMB_A_2226_07_after_save.png` · `THUMB_A_2226_RESULT.json` · artifacts `BEN_2226_thumb_A_content_list.png` |
| Test & Compare | **Cleared 2-slot** (Ben 22:26). Title+thumb / Thumbnail-only re-arm hit Studio **trouble saving** (one wait+retry, stop). No active 2-slot left; single title Atom. **Re-arm after 15 Oct public:** 3 pairs (A+Atom · C v06+Periodic · B v04+Gold) or Thumbnail-only A/B/C. Proof: `FORCE_2226_RESULT.json` · `FINISH_2226_tc_after_save.png` |
| Description + chapters | **OK** — package description + chapters, no `/go/` links. |
| Captions | **OK** — `hos_004_full_v02.en.srt` uploaded (toast “English subtitles uploaded”). Proof: `FINISH_captions.png` (`finish_v01e_13_captions_after.png`) |
| End screen | **Still blocked by Studio processing** (CoS 21:02). Modal opens; template **1 video, 1 subscribe** applies; Specific `AL_-qlWko_g` not persisted — Save → **“problem in processing… edits were not saved”** + NaN times; element left **Best for viewer** + Subscribe. **Re-set Specific 002 after processing settles / launch day.** Proof: `COS2102ES4_06_saved.png` · `COS_CHECKIN_2102_ENDSCREEN_V04.json` |
| Pinned comment | **Blocked while Private/Scheduled** — Studio: “This account doesn't have permission to create comments.” Textarea disabled. Package text ready, no links. **Pin on launch day 15 Oct** after Public. Proof: `BEN_004_pin_blocked_permission.png` · `COMMENTS_V09_PIN.json` |
| Shorts | **s01/s03 v05 Ben PASS** (29 Sep 20:48). **s02 v05 FAIL** (shaky) → **s02 punch v06** rebuilt · `gate_shorts_open.py check` **PASS** · iCloud `HOS UAT/004_…/10_Shorts/hos_004_s02_every_eighth_punch_v06.mp4` · `WATCH_shorts_s02_v06.txt`. **STOP — Ben phone watch s02 v06. Schedule nothing until he OKs s02.** |
| `.env` / API | **Not used.** Orbit never touched. |

## Made for Kids — URGENT audit (Ben 29 Sep 20:00)

Package says `madeForKids: false`. Studio had shown “Made for Kids” on `GHZDsiH7L7A` — audited via CDP `:9460` HOS Chrome.

| Check | Result | Proof |
|---|---|---|
| **004 `GHZDsiH7L7A` Audience** | **No, it's not 'Made for Kids'** (radio checked; banner “set to not Made for Kids”). Already OK when opened — Ben may have fixed on phone. | `11_Upload-Package/Schedule/evidence_2026-09-29_studio/URGENT_audience_004_not_made_for_kids.png` · `urgent_kids_004_force_after.png` · artifacts `~/.local/share/cursor-mac-mini-hos-worker/artifacts/hos004_studio_phone_uat/URGENT_audience_004_not_made_for_kids.png` |
| **Channel → Settings → Channel → Advanced → Audience default** | **No, set this channel as not Made for Kids** (checked). Yes unchecked. **Did not STOP** — not “Yes, made for kids”. Channel settings **not changed**. | `URGENT_channel_advanced_audience.png` · `URGENT_CHANNEL_ADVANCED_V03.json` |
| **001 long `_C92tIJCk8A`** | Not Made for Kids | `urgent_kids_001_long.png` |
| **001 Shorts** (`8uBR-9oxeWs` · `YX2UR1u-JCQ` · `Fnb3p81u-wY` · `vpuRgKXtFlY` · `Lcmh5y2KMQM`) | Edit URLs returned Studio “Oops” — **not verified via edit pages**. Content list showed no Made-for-Kids badge on those Shorts. | `urgent_kids_001_short_*.png` · `URGENT_KIDS_FIX_V02.json` |
| **002 long `AL_-qlWko_g` + 5 Shorts** | All **Not Made for Kids** | `urgent_kids_002_*.png` |
| **003 long `frP_YrNShsU` + 3 Shorts** | All **Not Made for Kids** | `urgent_kids_003_*.png` |
| **Made-for-Kids hits** | **None** among verified videos | `URGENT_KIDS_AUDIT_V01.json` |

**Policy (every upload from now on):**
1. **Altered / synthetic content = YES** (“Yes, AI was used”) — Ben 21:49 (AI visuals + AI voice clone). One setting per save.
2. After **every** Studio save, re-check Audience = **“No, it's not made for kids”** (named selectors only — never broad “first Yes”).
End screens and pinned comments do not work on kids’ videos — Audience first.

## Altered / AI use = YES — Ben 21:49 CHANGE OF ORDER

Overrides Ben 20:03 “Altered content: No” and CoS 21:02 note to set No. Reason: AI-generated visuals and an AI clone of Ben's voice.

| Video | Result | Audience after |
|---|---|---|
| **004 long `GHZDsiH7L7A`** | **YES** (“Yes, AI was used”) | not Made for Kids |
| **001 long `_C92tIJCk8A`** | **YES** (already Yes) | not Made for Kids |
| **002 long `AL_-qlWko_g`** | **YES** | not Made for Kids |
| **003 long `frP_YrNShsU`** | **YES** | not Made for Kids |
| **002 Shorts** (5) | **YES** ×5 | not Made for Kids |
| **003 Shorts** (3) | **YES** ×3 | not Made for Kids |
| **001 Shorts** (5) | **Studio Oops** on all edit URLs — **not settable via Details** (same as kids audit). Retry after Studio fixes edit pages. | n/a |

CDP `:9460` · named radio `Yes, AI was used` · one save · Audience re-read. JSON: `ALTERED_YES_2149_RESULT.json` · `ALTERED_YES_2149_001SHORTS_RETRY.json`. Script: `_ben_2149_altered_yes_v01.py`.

JSON: `11_Upload-Package/Schedule/evidence_2026-09-29_studio/URGENT_KIDS_AUDIT_V01.json` · `URGENT_KIDS_FIX_V02.json` · `URGENT_CHANNEL_ADVANCED_V03.json`

## Comments — Ben 20:03 (29 Sep)

Kids-locked comments theory confirmed for 004 earlier blank UI; after Audience **No**, Comments section is editable.

| Check | Result | Proof |
|---|---|---|
| **004 `GHZDsiH7L7A` Comments** | **On** · Moderation **Basic** · Who can comment **Anyone** · Sort **Top** · likes checkbox on | `BEN_004_comments_on.png` · `comments_v06_004_comments_on.png` · `COMMENTS_V06_RESULT.json` |
| **001 long `_C92tIJCk8A`** | Comments **On** | `comments_v06_audit_001_long.png` |
| **002 long `AL_-qlWko_g`** | Comments **On** | `comments_v06_audit_002_long.png` |
| **003 long `frP_YrNShsU`** | Comments **On** | `comments_v06_audit_003_long.png` |
| **002 Shorts** (5) | All Comments **On** | `comments_v06_audit_002_short_*.png` |
| **003 Shorts** (3) | All Comments **On** | `comments_v06_audit_003_short_*.png` |
| **001 Shorts** (5) | Edit “Oops” — **not audited** via Details (same as kids audit) | `comments_v06_audit_001_short_*_oops.png` |
| **Comments OFF list** | **None** among auditable longs + 002/003 Shorts | `COMMENTS_BEN_2003_SUMMARY.json` |
| **Pinned comment** | **Not posted** — Studio permission banner while Private/Scheduled. Do on launch day. | `BEN_004_pin_blocked_permission.png` · `COMMENTS_V09_PIN.json` |

Summary: `11_Upload-Package/Schedule/evidence_2026-09-29_studio/COMMENTS_BEN_2003_SUMMARY.json`

## Studio growth settings — Ben 20:03 (29 Sep) · full order

Ben’s full growth-settings list. Overrides: **(a) Altered/AI use = NO** (not Yes); **(b) channel Audience change authorised** (record before). CDP `:9460` HOS only. Summary JSON: `GROWTH_ALL_RESULT.json` · `CHANNEL_META.json` key `studio_growth_settings_2026-09-29`.

### CoS check-in 21:02 (30 Sep) — live re-verify

Ben re-sent the growth order unchanged. Live CDP pass with **named selectors only** (no “first Yes”); Audience re-read after every save.

| Check | Result | Proof |
|---|---|---|
| **Audience** | **No, it's not 'Made for Kids'** (checked) + banner | `COS2102_B1_audience.png` · `COS_CHECKIN_2102_RESULT.json` |
| **AI use / Altered** | Was No at 21:02 — **superseded by Ben 21:49 → YES** (see Altered section) | `ALTERED_YES_004_long_VERIFY.png` |
| **Visibility** | Scheduled **15 Oct**; Premiere **OFF** | `COS2102_B2_visibility.png` |
| **T&C** | Was Ineligible 2-slot — **cleared Ben 22:26**; re-arm blocked by Studio trouble saving (retry once). Re-arm after public | `FORCE_2226_RESULT.json` · `THUMB_A_2226_RESULT.json` |
| **End screen Specific 002** | **Blocked** — processing error + NaN (template Subscribe ok; video stuck Best for viewer) | `COS2102ES4_06_saved.png` |
| **Selector policy** | aria-label / exact own-text for kids + AI radios; one control per save | `_cos_checkin_2102_growth_fix_v01.py` |
| **Short s02 v06** | Already delivered — gate PASS · iCloud · STOP phone watch | `SHORTS_PUNCH_INDEX_s02_v06.json` |

### A — Channel settings

| Item | Result | Proof |
|---|---|---|
| **A1 Audience** | **BEFORE: already not_kids** (“No, set this channel as not Made for Kids” checked). **AFTER: same.** No change needed; re-confirmed. | `BEN_growth_A1_audience_BEFORE.png` · `BEN_growth_A1_audience_AFTER.png` |
| **A2 Upload defaults Basic** | Visibility **Private**; Category **Education**; Language **English (UK)**; Caption cert **never aired on US TV**; Licence **Standard YouTube**; title/desc templates empty | `BEN_growth_A2_basic_AFTER.png` · `BEN_growth_A2_advanced_fields_AFTER.png` |
| **A3 Upload defaults Advanced** | Comments **On**; Moderation **Basic** (Studio UI had no “Hold potentially inappropriate” option in this dropdown); automatic chapters **ON**; caption cert set | `BEN_growth_A3_advanced_AFTER.png` · `BEN_growth_A3_comments_menu.png` |
| **A4 Channel Basic info** | Country **United Kingdom**; keywords from `channel_keywords.txt`; description left (no Orbit) | `BEN_growth_A4_basic_AFTER.png` |
| **A5 Branding watermark** | **Not added** (no subscribe graphics) | `BEN_growth_A5_branding.png` |

### B — Long `GHZDsiH7L7A`

| Item | Result | Proof |
|---|---|---|
| **B1 Audience** | Not Made for Kids; Comments/Notifications disabled notices **gone** | `BEN_growth_B1_audience.png` |
| **B2 Visibility** | **Scheduled 15 Oct 2026 18:00**; **Set as Premiere OFF**; private until then | `BEN_growth_B2_visibility_PROOF.png` |
| **B3 Details** | Title Atom; package description+chapters (no `/go/`); **thumb A v04 LIVE** (Ben 22:26) | `THUMB_A_2226_08_content_list.png` · `BEN_growth_B3_details.png` |
| **B4 AI use / Altered** | **YES** (“Yes, AI was used”) — Ben **21:49** overrides 20:03/21:02 No; re-confirmed after thumb A | `FORCE_2226_RESULT.json` · `ALTERED_YES_004_long_VERIFY.png` |
| **B5 Subtitles** | English present / upload path used (`hos_004_full_v02.en.srt`) | `BEN_growth_B5_subtitles_AFTER.png` |
| **B6 End screen** | **Blocked** — processing error; Specific 002 not saved (Subscribe template only) | `COS2102ES4_06_saved.png` |
| **B7 Cards** | Attempted ~1:30→002 + ~6:00→003; verify in Studio | `BEN_growth_B7_cards_AFTER.png` |
| **B8 Playlist** | Create/add attempted for “History of Science: How We Found Out”; Studio **Oops** on playlist page after — **re-check manually** | `BEN_growth_B8_playlist_AFTER.png` |
| **B9 Test & Compare** | **2-slot cleared** (Ben 22:26). Re-arm blocked by Studio trouble saving after one retry. **After 15 Oct public:** 3 pairs or Thumbnail-only | `FORCE_2226_RESULT.json` |
| **B10 Pin** | **Blocked** while Private/Scheduled — do **15 Oct 18:05** | `BEN_growth_B10_pin.png` |

### C — Older films

| Item | Result |
|---|---|
| Made for Kids → No changes | **None changed** — all auditable already not_kids |
| Already not_kids | 001/002/003 longs + all 002/003 Shorts |
| 001 Shorts edit Oops | `8uBR-9oxeWs` · `YX2UR1u-JCQ` · `Fnb3p81u-wY` · `vpuRgKXtFlY` · `Lcmh5y2KMQM` — unverified via edit |
| C4 end screens → 004 | **Deferred** until after 15 Oct 18:05 |

### D — Shorts (Ben 30 Sep 10:45 fixes)

| Slot | Id | Status | Notes |
|---|---|---|---|
| Fri How Small v05 | **`29bpGAI0wb8`** | **Scheduled 16 Oct 2026 11:30 UK** (after 004 15 Oct 18:00) | Audience not kids · Altered YES · Related 004 **still deferred** → 15 Oct 18:05 · proof `BEN_1045_s01_1130.png` |
| Sun Every Eighth v06 | **`TbMMJSRKC3U`** | **Scheduled 18 Oct 2026 11:30 UK** | Audience not kids · Altered YES · Related **002 set** · proof `BEN_1045_s02_1130.png` |
| Tue (was Her Ring) | **`CUu8k38iAMc`** | **PRIVATE** (30 Sep 10:45) — not deleted | Duplicate of public `zI_eD3vFWmE` (27 Sep). Tue 20 Oct now → **001 Germs**. Script ideas STOP: `10_Shorts/SHORTS_TUE_001_GERMS_IDEAS_v01.md` |

**Covers live-v02 (STOP for Ben — not uploaded):** painted scenes + TOP chunky type (no text box), matching live 002 Short covers. Fri `HOW SMALL?` · Sun `EVERY EIGHTH?` · Tue provisional `THEY LAUGHED?` (Idea A). Eight-up sheet (5 live 002 + 3 new): `10_Shorts/covers_live_v02/hos_004_shorts_covers_live_v02_eight_up.jpg` · `thumb_preview.py short` sheet alongside. iCloud `HOS UAT/004_…/10_Shorts/`.

**SHORTS_LOG:** synced from live Studio Shorts scrape (`LIVE_SHORTS_LIST.json`) — added missing public `zI_eD3vFWmE` + `xvanpsLeADE`. From now: check live Shorts page before any new script.

## Channel split — HOS only (Ben reminder 29 Sep 2026)

- Channel: **@HistoryOfScienceYT**. Repo: **history-of-science**. UAT: **`HOS UAT/004_…`** only.
- Do **not** write 004 status, schedules, or deliverables into Orbit With Ben / OWB UAT / orbit agent stores.
- Shorts VO = HOS house voice (ElevenLabs Ben Orbit Narrator IVC) — voice reuse is intentional; **no** Orbit branding, links, or picture rules.

## STEP 6 Short scripts v02 — **STOP for Ben approve**

`10_Shorts/SHORTS_PUNCH_SCRIPTS_v02.md` — Fri 004 gold (~60 w) · Sun 002 Newlands octaves · Tue 003 Bertha’s hand only. Shorts **not** uploaded.

## Upload / Shorts status (29 Sep 2026 · FINISH 20:00)

- **Long upload:** **DONE via Studio** — id **`GHZDsiH7L7A`** · Scheduled **15 Oct 2026 18:00 UK** · **Premiere OFF** · Audience **not Made for Kids** · no `.env`. Records: `PACKAGE_UPLOAD_RESULT_2026-09-29.json` · `PACKAGE_MANIFEST.json` (`youtubeId`, `premiere: false`).
- **Superseded (kept):** `UPLOAD_BLOCKED_ENV_ABSENT_2026-09-29.json` · `DRY_RUN_NOT_CLEAN_ENV_ABSENT_2026-09-29.json` → status `SUPERSEDED`.
- **FINISH Studio:** Visibility + Audience + description/chapters + captions **OK**. **Thumb A LIVE** (Ben 22:26). T&C re-arm / end screen / pin still launch-day or after Studio save healthy.
- **Thumbs (files):** A v04 · B v04 · **C v06** — Ben PASS. **Live Studio main thumb = A (atom v04)** — Content list confirmed.
- **Shorts:** **SCHEDULED** (Ben 09:02). s01 `29bpGAI0wb8` Fri 16 Oct 11:30 · s02 `TbMMJSRKC3U` Sun 18 Oct 11:30 · s03 `CUu8k38iAMc` Tue 20 Oct 11:30. Related s01→004 deferred to 15 Oct 18:05.

### Ben 22:26 — main thumb A NOW (30 Sep)

| Step | Result | Proof |
|---|---|---|
| End 2-slot T&C holding thumb | **Ended** (Continue delete → Cancel new wizard); still_two=False | `THUMB_A_2226_01_before_tc.png` · `THUMB_A_2226_04_after_tc_clear.png` |
| Upload A + one Save | **Changes saved** (no trouble) | `THUMB_A_2226_07_after_save.png` |
| Content list shows A | **Confirmed** — atom / “WHAT'S REALLY INSIDE AN ATOM?” (not HIDDEN NUMBER) | `THUMB_A_2226_08_content_list.png` · `BEN_2226_thumb_A_content_list.png` |
| Audience + Altered | **not Made for Kids** · **Yes, AI was used** | `FORCE_2226_RESULT.json` |
| Re-arm T&C | **Blocked** — Title+thumb / Thumbnail-only → Studio trouble saving; waited 2–3 min, retried once, stopped. No 2-slot left. Re-arm after 15 Oct public | `FINISH_2226_tc_after_save.png` |

### Screenshots for Ben / CoS (exact paths)

| What | Repo evidence | Artifacts (Ben share) |
|---|---|---|
| Audience 004 not kids | `11_Upload-Package/Schedule/evidence_2026-09-29_studio/URGENT_audience_004_not_made_for_kids.png` | `/Users/benjaminoats/.local/share/cursor-mac-mini-hos-worker/artifacts/hos004_studio_phone_uat/URGENT_audience_004_not_made_for_kids.png` |
| Channel Advanced audience default No | `…/URGENT_channel_advanced_audience.png` | `…/artifacts/hos004_studio_phone_uat/URGENT_channel_advanced_audience.png` |
| Visibility 15 Oct 18:00 Premiere OFF | `…/FINISH_visibility_15oct_1800_premiere_off.png` | `…/artifacts/hos004_studio_phone_uat/FINISH_visibility_15oct_1800_premiere_off.png` |
| Test & Compare Ineligible | `…/FINISH_test_and_compare.png` | `…/artifacts/hos004_studio_phone_uat/FINISH_test_and_compare.png` |
| Comments On (004) | `…/BEN_004_comments_on.png` | `/Users/benjaminoats/.local/share/cursor-mac-mini-hos-worker/artifacts/BEN_004_comments_on.png` |
| Pin blocked (permission) | `…/BEN_004_pin_blocked_permission.png` | `/Users/benjaminoats/.local/share/cursor-mac-mini-hos-worker/artifacts/BEN_004_pin_blocked_permission.png` |
| Growth A1 channel Audience | `…/BEN_growth_A1_audience_AFTER.png` | `/Users/benjaminoats/.local/share/cursor-mac-mini-hos-worker/artifacts/BEN_growth_A1_audience_AFTER.png` |
| Growth A2 upload defaults | `…/BEN_growth_A2_basic_AFTER.png` | `/Users/benjaminoats/.local/share/cursor-mac-mini-hos-worker/artifacts/BEN_growth_A2_basic_AFTER.png` |
| Growth B2 Visibility 15 Oct 18:00 Premiere OFF | `…/BEN_growth_B2_visibility_PROOF.png` | `/Users/benjaminoats/.local/share/cursor-mac-mini-hos-worker/artifacts/BEN_growth_B2_visibility_PROOF.png` |
| Growth B1 Audience not kids | `…/BEN_growth_B1_audience.png` | `/Users/benjaminoats/.local/share/cursor-mac-mini-hos-worker/artifacts/BEN_growth_B1_audience.png` |
| Growth B4 AI use No | `…/BEN_growth_B4_altered_AFTER.png` | `/Users/benjaminoats/.local/share/cursor-mac-mini-hos-worker/artifacts/BEN_growth_B4_altered_AFTER.png` |
| Growth B9 T&C Ineligible | `…/BEN_growth_B9_tc_AFTER.png` | `/Users/benjaminoats/.local/share/cursor-mac-mini-hos-worker/artifacts/BEN_growth_B9_tc_AFTER.png` |
| Ben 22:26 thumb A Content list | `…/THUMB_A_2226_08_content_list.png` | `/Users/benjaminoats/.local/share/cursor-mac-mini-hos-worker/artifacts/BEN_2226_thumb_A_content_list.png` |
| Ben 22:26 thumb A Changes saved | `…/THUMB_A_2226_07_after_save.png` | `/Users/benjaminoats/.local/share/cursor-mac-mini-hos-worker/artifacts/BEN_2226_thumb_A_changes_saved.png` |
| Growth B6 end screen | `…/BEN_growth_B6_endscreen_AFTER.png` | `/Users/benjaminoats/.local/share/cursor-mac-mini-hos-worker/artifacts/BEN_growth_B6_endscreen_AFTER.png` |
| Growth B7 cards | `…/BEN_growth_B7_cards_AFTER.png` | `/Users/benjaminoats/.local/share/cursor-mac-mini-hos-worker/artifacts/BEN_growth_B7_cards_AFTER.png` |
| Growth B8 playlist | `…/BEN_growth_B8_playlist_AFTER.png` | `/Users/benjaminoats/.local/share/cursor-mac-mini-hos-worker/artifacts/BEN_growth_B8_playlist_AFTER.png` |


## Ben 14:47 whole-channel Studio §9 (recorded 2026-09-30T17:58:08+01:00)

Channel: `@HistoryOfScienceYT` only. Supersedes narrower Fri/Sun/language orders where they overlap. Evidence: `11_Upload-Package/Schedule/evidence_2026-09-30_whole_channel_1447/` · artifacts `BEN_1447_whole_channel/` · `CONTACT_final_states.jpg` · `SWEEP_RESULT.json` · `TAGS4_RESULT.json`.

### 004 videos
| id | kind | notes |
|---|---|---|
| `GHZDsiH7L7A` | long | Core §9; tags fixed; Test & Compare **not touched**; schedule 15 Oct unchanged; How We Found Out playlist missing |
| `29bpGAI0wb8` | Short (Fri) | Core §9; title already *What happens if you keep cutting gold in half?*; tags already OK; **Related deferred to 15 Oct 18:05** |
| (no other 004 Shorts live yet beyond Fri) | | |

**Would not save (channel-wide education taxonomy):** Academic system **United Kingdom** absent (England listed; left as UAE per “if listed”). GCSE Chemistry/Physics/Biology exams absent. Level “Secondary school” is a non-selectable header; Grade 10 leaf does not persist after reload. Playlist **History of Science: How We Found Out** does not exist; Studio “New playlist” submenu did not expose a title field — longs remain on *How Did We Discover…? | History of Science*.

**Was Made for Kids / AI=No before:** none in sweep lists. Tag concatenation bug from first pass **repaired** (22/22 verified after reload). STOP.


### Fri probe follow-up (2026-09-30T18:05:47+01:00)

[Studio dropdown probe Fri](bc-73025afe-d117-5442-9891-fb3cac39f1d3) found Academic **United Kingdom** is not listed (England/Scotland/Wales are). Fri `29bpGAI0wb8` set to **Academic England** + **English (United Kingdom)** languages + Type Concept overview. Whole-channel 14:47 pass had reverted Academic to UAE — **restored England** and verified after reload (Scheduled, not-kids). Level still None (Key stage picks do not persist). GCSE Chemistry still not in exam taxonomy. Evidence: `11_Upload-Package/Schedule/evidence_2026-09-30_studio_fixes/FRI_ENGLAND_RESTORE_RESULT.json`.
