# Production status — 004 What's Really Inside an Atom?

| Field | Value |
|---|---|
| Slug | `004_Whats-Really-Inside-An-Atom` |
| Channel | `@HistoryOfScienceYT` only |
| Topic | Ben picked 26 Sep 2026 (the atom; why the periodic table has its order) |
| Title | **What's Really Inside an Atom?** (main — Ben pick STEP 3, 29 Sep 2026); Test & Compare *Why Is the Periodic Table in This Order?* and *How Small Can You Cut Gold?* |
| Script | `01_Script/atom_script_master_v02.md`. **Spoken words LOCKED.** VISUAL MUST **re-timed from VO v04** (27 Sep). |
| Script review | 88.9. Passed by hand by Ben, 26 Sep 2026 |
| Pre-build vidIQ audit | Signed off by Ben, 26 Sep 2026 (vidIQ waived) |
| Episode gate | Passed by Ben (manual), 26 Sep 2026 |
| VO | **v04 KEEP** (Ben, 27 Sep 2026, after listening at 3:38, 6:06 and 7:39; the three `vo_check` word FAILs there are the transcriber, not the take). Masters in `02_Voiceover/05_Master/`. |
| Re-time (Step 3) | **DONE from v04.** `07_Edit-Project/VO_RETIME_v02.json` · script VISUAL MUST + chapter cards updated |
| Plate boards (Step 4) | **`part-0N_plates_v02.json`.** Parts 01–04 `mint: false` (04 rough v01 pending Ben) · 05 `mint: false` · Explorer used ×2 (P02 + P04 stadium pea); remaining P05 · no Explorer in Part 03 |
| Picture | **Part 01–05 PASS.** **Full join v03 PASS** sha `f88cb9d4…65244`. Finishing UAT: `hos_004_full_v02` (two-section bed) + thumbs A/B/C. |
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

**Next:** STOP for Ben — music on `hos_004_full_v02` (two-section bed, no loop) **and** long thumbs A/B/C together. Captions ready. Title locked. Do **not** start STEP 5 or STEP 6 until Ben signs off.

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
- Finishing STEP 1–2 done: `hos_004_full_v01.mp4` (music UAT) + captions. Picture LOCKED for finishing.
- **iCloud:** `HOS UAT/004_Whats-Really-Inside-An-Atom/09_Final-Export/hos_004_full_join_v03.mp4`
- Builder: `07_Edit-Project/_join_hos_004_full_v03.py` · notes `09_Final-Export/FULL_JOIN_V03_NOTES.md`

## Full_v01 (29 Sep 2026) — continuous bed with loop (superseded for music UAT by v02)

Picture = locked v03. VO v04 untouched. **Music join used a loop** (EL bed ~390.8 s) — Ben rejected the loop → v02.

| Field | Value |
|---|---|
| Cut | `hos_004_full_v01.mp4` |
| sha256 | `058e1ba7a4a986de0dec4fe1a6e0e6f47a47449ad314f979e8224a8a5ef1b4d5` |
| Duration | **524.700 s** · A/V Δ **0.000** s · 1920×1080 30 fps CFR |
| Bed | `05_Music/hos004-full_score_bed_v01.mp3` (−20 dB, sidechain, fade across cream, silent under hold). EL ~390.8 s → **looped** through cream |
| amix | `inputs=2:weights=1 1:normalize=0` |
| Levels | `vo_check` mean **−23.6** / peak **−3.8** dB · film `−t 500.69` mean **−23.4** / max **−3.8** dB |
| Captions | `11_Upload-Package/Captions/hos_004_full_v01.en.srt` (still valid for picture; reuse until regen) |
| iCloud | `HOS UAT/004_Whats-Really-Inside-An-Atom/09_Final-Export/hos_004_full_v01.mp4` |
| Status | **Superseded for music listen by full_v02.** Not KEEP. No upload. |

## Full_v02 (29 Sep 2026) — two-section bed, no loop · **STOP for Ben music**

Same picture/cards/end as v01. VO untouched. Music join at the Part 05 chapter card.

| Field | Value |
|---|---|
| Cut | `hos_004_full_v02.mp4` |
| sha256 | `ed870939f476d326197cdaf1403ce7064850d4286ff63aa81bc5a7584761e98e` |
| Duration | **524.700 s** · A/V Δ **0.000** s · 1920×1080 30 fps CFR |
| Bed §1 | `hos004-full_score_bed_v01.mp3` · 0:00 → card05 **5:55.48** (355.478 s) |
| Bed §2 | `hos004-full-sect2_score_bed_v01.mp3` (~160.0 s) · card05 → cream end · prompt + “gentle lift toward a quiet resolution” |
| Join | **1.5 s** crossfade under Part 05 chapter card · **no loop** |
| Duck | gap **−20 dB** · extra ~3 dB under speech (`threshold=0.012:ratio=12…`) · `amix normalize=0` |
| vo_check | mean **−23.6** / peak **−3.8** dB · 147 wpm |
| Mean 0:00–8:20.69 | mean **−23.4** / max **−3.8** dB |
| Word FAILs | ~**6:07** `a living`→`the living` · ~**7:40** `a weight`→`of weight` · ~**8:06** insert `you` · **no 6:31** this run · **no 5:34** on full |
| 7:40 window | full_v02 and plain P05 v04 VO hear the **same** (“kind of [a]…”); STT not a mix fault. Plain P04 still hears `van der` at local ~1:33 (5:34 film) but full_v02 did not flag it. |
| Builder | `07_Edit-Project/_mix_hos_004_full_v02_music.py` · notes `09_Final-Export/FULL_V02_NOTES.md` · check `FULL_V02_VO_CHECK.txt` |
| iCloud | `HOS UAT/004_Whats-Really-Inside-An-Atom/09_Final-Export/hos_004_full_v02.mp4` (+ `WATCH_full_v02.txt`) |
| Status | **UAT — STOP for Ben music listen.** Not KEEP. No upload. |

## Title (STEP 3) — Ben pick 29 Sep 2026

| Role | Title |
|---|---|
| **Main (listing)** | **What's Really Inside an Atom?** |
| Test & Compare alt 1 | *Why Is the Periodic Table in This Order?* |
| Test & Compare alt 2 | *How Small Can You Cut Gold?* |

Written into this file + `11_Upload-Package/LAUNCH_PLAN.md`.

## Long thumbs (STEP 4) — **v03 STOP for Ben pick** (nothing to Studio)

Composer: `08_Thumbnail/_compose_hos_004_thumbs_v03.py`. Index: `THUMBS_INDEX_v03.json`.

v03 restores the film’s **3D cartoon** look (v02 went flat/graphic). Keeps v02 fixes: correct Z, one clear idea, text off subject. Full-bleed only — no split panels, no flat vector tiles. v01 + v02 remain in Selected for side-by-side.

| Variant | File | Hook | Notes |
|---|---|---|---|
| **B (main)** | `hos_004_thumb_B_cut_gold_v03.jpg` | **CUT GOLD?** | Full-frame coin/knife from v01 plate; hook up/left, clear of blade; no side panel |
| A | `hos_004_thumb_A_hidden_number_v03.jpg` | **THE HIDDEN NUMBER** | Film 3D Te/I cubes; house-font **Te 52** / **I 53** only (I glowing); no other numbers |
| C | `hos_004_thumb_C_bounced_back_v03.jpg` | **IT BOUNCED BACK** | Part 04 foil plate · one bright rebound particle + short trail · no beds/constellations |

### Test & Compare pairs (as recorded — pending Ben pick)

| # | Title | Thumb |
|---|---|---|
| **1 main** | What's Really Inside an Atom? | B CUT GOLD? |
| 2 | Why Is the Periodic Table in This Order? | A THE HIDDEN NUMBER |
| 3 | How Small Can You Cut Gold? | C IT BOUNCED BACK |

**iCloud:** `HOS UAT/004_Whats-Really-Inside-An-Atom/08_Thumbnail/Selected/` (v01 · v02 · v03 side by side)

**STOP for Ben** — thumbnail pick (and music on `hos_004_full_v02`). Do **not** push to Studio. Do **not** start STEP 5/6 until Ben signs off. Do **not** label KEEP/LOCKED.

