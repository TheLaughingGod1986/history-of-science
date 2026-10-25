# Production status — 007 The First Vaccine

| Field | Value |
|---|---|
| Slug | `007_The-First-Vaccine` |
| Channel | `@HistoryOfScienceYT` only |
| Topic | **The first vaccine** (Jenner, cowpox, 1796 → Inquiry 1798; after-act 1980 eradication + *vacca*) |
| Stage | **Script v01 on main** (review 92.3). FACT_NOTES confirmed by Claude 4 Oct 2026. **VO allowed** |
| VO | Locked set 01 **v03** · 02 v01 · 03 v02b · 04 v01b · 05 v01b. Part 01 v03 = v02 + one-paragraph chalk-cross pickup (Claude 5996011402, 5 Oct 2026): "a neighbour's house shut up and silent". 100.23 s, sha256 `3881da7b…5fb83`, vo_check PASS; Claude VO PASS (5996211914). Audio stays on the Mini (mp3 gitignored); evidence `~/_desk/007/vo_20261005_chalk/` |
| Neighbour gate | **PASS** (3 Oct 2026): 7 education ≥1M; TED-Ed yes. Evidence `11_Upload-Package/evidence_2026-10-03_neighbours.json` |
| Picture | **All 73/73 Flow rows minted (J0352 KEEP, 21 Oct 2026; HOS PR #351 merged):** P1 17/17 (530 cr) · P2 21/21 (750 cr) · P3 12/12 (390 cr) · P4 11/11 (380 cr) · P5 12/12 (840 cr) = **2,890 cr** vs 7,550 cap. Face lock `P2:08_jenner_window` KEEP applied to all later readable Jenner faces. 3 £0 code graphics (`7808f751`), 2 archive + 18 reuse (£0). |
| Edit | **Full join v01 (`hos_007_full_join_v01.mp4`, 505.15 s / 12,123 frames, 97 cuts, sha256 `7cfd6a59`) assembled (J0827, 22 Oct 2026, £0)** across Parts 01–05 (Chief PASS J0820) on locked VO with house Didot teaching cards and both £0 repeat-shot fixes (`P1:09c_case_again` 1.88× lancet crop; `P5:06c/06d` split into strictly unused `04_health_workers` back half `3.833–7.958 s` + `06_assembly_1980` tail `5.083–8.000 s` 1.38× front-row push-in). Parts: P1 `61a5c039` (100.83 s, 20 cuts) · P2 `6ab2fb1f` (129.62 s, 22 cuts) · P3 `62a14a08` (78.75 s, 15 cuts) · P4 `e6a005cd` (92.75 s, 20 cuts) · P5 `14206aeb` (103.17 s, 20 cuts). **Master v04 (`hos_007_master_v04.mp4`, 531.08 s / 12,746 frames, 102 cuts, sha256 `c7f62adb`, `_PHONE.mp4` 102.49 MB sha256 `58e89a6f`, J0925, £0 / 0 Flow cr)** with all 3 of Ben's changes on v03 (`0:38` 10 intact turned-wood peg dolls resting solidly on oak windowsill so nothing falls through shelf, `2:40` folding steel lancet held at shallow grazing angle scratching skin surface with no needle going in, `4:22` Jenner touching folding steel lancet at shallow angle to James Phipps's clean upper arm with zero AI artefact) + kept v03 fixes (`1:48` aligned milking hand, `3:50` Explorer at house scale, `8:25–8:51` closing card + 20 s moving end screen + 1.5 s fade) in NAS `master_v04_J0925/` and iCloud `HOS UAT/007_The-First-Vaccine/`, parked for Chief review (`07_Edit-Project/master_v04_pack/REVIEW_master_v04.md`). |
| Air | proposed **Thu 12 Nov 2026 18:00 UK = 18:00 UTC** (GMT); privacy private; madeForKids false; proposals only |
| Shorts | `s04_smallpox_test_v01` uploaded Private `-I_GHK-GcFs` for Fri 13 Nov 2026 11:30 UK (`2026-11-13T11:30:00Z`, J0873); `s05_vacca_jesty_v02` (`24.167 s`, sha256 `89a9a1668d74`) uploaded Private `4WUs0beKn0A` for Tue 17 Nov 2026 11:30 UK (`2026-11-17T11:30:00Z`, J0906); Related → 007 long once uploaded (`J0875`) |
| Backup | Neighbour gate PASSED — Lightning backup not needed |

## STOP

- No Vertex/Veo/Flow minting on this film.
- No spending.
- Do not merge or touch desk PR #180 from this scaffold PR.

## 23 Oct 2026 — J0856 candidate master v02 (Gemini, superseding J0830 v01)

Original £0 warm chamber score at **60.0 BPM** (`ac[20]/ac[0] = 0.8926`) with envelope ducking (`18.12 dB` mean under VO in speech, `0` breaches, rising `+1.53 dB` in pauses) and **43 HOS house SFX cues** (39 ink ticks across all 6 WHO cards, all 12 date/place stamps & data pills, all 21 teach labels & code graphics + 4 page-turn whooshes on the chapter cards; never over the VO's first word). Approved join picture copied as a lossless video stream (`SHA256=0aa1cf6383b02034c5a7b6ded41ea24549e59b0bb4d7031445775d5ce9fd9915`).

Master v02: `/Volumes/data/mac-mini-archive/hos-007-vaccine/master_v02_J0856/hos_007_master_v02.mp4`  
SHA-256: `e55f680db246e12620a7827599415e6d9f513d614563bd213c0b2a42f9c69c97` · Duration: `505.147 s`  
Measured encoded master: **−14.0 LUFS, −1.4 dBTP**.

```text
SFX level PASS: VO -16.1 LUFS, SFX -35.0 LUFS, 43 hits
Bed vs VO PASS: bed -34.4 LUFS, 18.12 dB under VO in speech (p10 13.1, p50 18.6, p90 21.4, min 11.2, 0 breaches < 10 LU), rises +1.53 dB in pauses (-35.21 -> -33.68 LUFS)
music gate PASS: vaccine_score_bed_v01.mp3, 505.1 s, about 60.0 BPM, brief Pace: 58-64 BPM (onset ac[20]/ac[0] = 0.8926)
polish gate PASS: 0 of 97 rows failed, 5 to look at
picture QA PASS: 0 of 97 cuts fail, 5 to look at
Episode gate Decision: PASS; script 92.3/100
```

Full actual outputs and before/after table: `07_Edit-Project/master_v01_pack/REVIEW_master_v01.md`. Chief audio fit and final review pending. No approved edit stage claimed.

## 23 Oct 2026 — Short `s04_smallpox_test_v01` (Test B, first search-titled lift from Part 04, OWB J0865)

- **Selection:** HOS 004, 005, 006, and 001 each have 5 built search-titled Shorts (`s04`–`s08` / `s07`–`s11`); HOS 002 and 003 each have 4. HOS 007 now has VO locked + all 73/73 Flow plates KEEP (J0352) + master v02 Chief PASS (J0867) and had 0 built search-titled Shorts, making 007 the locked HOS long with the fewest built Shorts.
- **VO (0 spend):** `02_Voiceover/part04_the_test_v01b.mp3` contiguous 62-word lift (words `0..61`, zero overlap with 007 Short B in Part 02 and Short C in Part 05): *"On the first of July, Jenner did the test. He gave James a standard variolation, the old treatment that used real smallpox matter, which would normally cause at least a mild illness. Then he waited. One day. Three days. A week. Nothing happened. In Jenner's words, no disease followed. Months later, he tried again. Still nothing. The cowpox had protected the boy."* 62 words, pauses capped at 0.14 s, `atempo=1.08`, 25.779 s VO + 0.35 s tail = 26.133 s total.
- **Picture & bed (0 spend):** Chief-KEPT plates `P3:03b_lancet_case_t1` (in `2.00 s`, frame 0 and the 3.0 s loop, `crop_x=640`), `P4:02_variolation_calm_t1` (`crop_x=1050`), `P3:06_mild_fever_t1` (`crop_x=640`), `P3:05b_week_passes_t1` (`crop_x=640`), `P3:07_playing_garden_t1` (`crop_x=640`), `P2:13_casebook_t1` (`crop_x=640`), `P4:05_days_pass_t1` (in `4.50 s`, `crop_x=640`). Own-synthesis warm harmonic pad (`hos007_s04_synth_pad_v01.wav`, D-major voicing, 0 credits) at −23.7 dB under VO. Hook **THE FIRST TEST** (TEST in yellow). Person/date card **EDWARD JENNER · 1 July 1796 · Berkeley** at 2.20–5.80 s (3.6 s, lower third of 16:9 centre band, 0.35 s fade in/out); the long's exact title *Why Vaccines Are Named After a Cow* at 9.0–14.0 s; word captions throughout with exclusive `gte(t,s)*lt(t,e)` handovers (20 captions, 19/19 handovers verified single-caption); CTA `watch the full film →` on the last 3.0 s.
- **Title draft:** *What Was the Edward Jenner Experiment?* (signed-out GB YouTube autocomplete exact hits `edward jenner experiment` / `how was the first vaccine made` / `edward jenner smallpox vaccine story` / `edward jenner cowpox vaccine` / `how did jenner test work`, 23 Oct 2026; alts *How Was the First Vaccine Made?*, *How Did Edward Jenner Test the First Vaccine?*).
- **File:** `10_Shorts/hos_007_s04_smallpox_test_v01.mp4`, 26.133 s, sha256 `3daff43d04bcebf538cd4c405a8eeb723a7329f425bec536d876cb7c69d696af`; phone copy iCloud `HOS UAT/007_The-First-Vaccine/10_Shorts/hos_007_s04_smallpox_test_v01.mp4`. One picture_qa / polish look-at, not a fail: `06_mild_fever_t1` at 0:08, low detail (edge density 0.0171 < film p5 0.0218).

```
PASS  hos_007_s04_smallpox_test_v01.mp4  dur=26.13s  audio=-24.1dB  motion=18.05  dhash=86e766dfda1e867f
   sheet /var/folders/1z/ymtxygjd7cnfrxjv7sqgmww40000gn/T/hos_shorts_gate/hos_007_s04_smallpox_test_v01_open_sheet.jpg
PASS  hos_007_s04_smallpox_test_v01.mp4  0:26.13  mean -24.1 dB  peak -4.9 dB  142 wpm
   warn  pace 142 wpm (< 145); expect a long film — see STUDIO_PLAYBOOK.md §4 speed
polish gate PASS: 0 of 8 rows failed, 1 to look at -> 02_Video-Projects/007_The-First-Vaccine/10_Shorts/qa_s04_smallpox_test_v01/polish_gate_s04_smallpox_test_v01.json
picture QA PASS: 0 of 8 cuts fail, 1 to look at -> 02_Video-Projects/007_The-First-Vaccine/10_Shorts/qa_s04_smallpox_test_v01/picture_qa_s04_smallpox_test_v01/PICTURE_QA.md, 02_Video-Projects/007_The-First-Vaccine/10_Shorts/qa_s04_smallpox_test_v01/picture_qa_s04_smallpox_test_v01/picture_qa_review.jpg
```

Gate run with `--air-date 2027-01-24` (gate only). Caption check: 20 changes, ratio 1.0, 19/19 handovers verified single-caption. Freezedetect: 0 events.

**STOP:** parked for Chief: Short PASS, title and slot. Nothing uploaded.

## 23 Oct 2026 — Short `s04_smallpox_test_v01` packaged & uploaded Private (`-I_GHK-GcFs`, Fri 13 Nov 11:30 London, OWB J0873)

- **Authority:** Chief PASS on `J0865` (`hos_007_s04_smallpox_test_v01.mp4`, `26.133 s`, sha256 `3daff43d04bcebf538cd4c405a8eeb723a7329f425bec536d876cb7c69d696af`, HOS `994d5a7b`) and Chief-created `J0873`. `£0` spend.
- **Upload & schedule:** Packaged in `10_Shorts/11_Upload-Package/s04_smallpox_test/PACKAGE_MANIFEST.json` (`SHORTS_RELEASE.json` PASS) and uploaded Private via `npm run youtube:package` as **`-I_GHK-GcFs`** (`https://youtu.be/-I_GHK-GcFs`) for the first free HOS weekday Short slot on or after Fri 13 Nov: **Fri 13 Nov 2026 at 11:30 London (`2026-11-13T11:30:00Z`, GMT)** (after the 007 long airs Thu 12 Nov 18:00 London).
- **API readback (`API_READBACK_-I_GHK-GcFs.json`):** `privacyStatus=private`, `publishAt=2026-11-13T11:30:00Z`, `uploadStatus=processed`, `madeForKids=false`, `selfDeclaredMadeForKids=false`, `defaultLanguage=en-GB`, `defaultAudioLanguage=en-GB`, `categoryId=27`, `hasCustomThumbnail=true`, 6 tags.
- **Studio readback (`STUDIO_READBACK_-I_GHK-GcFs.json`, CDP `:9460`):** `No, it's not Made for Kids` checked (`true`), Altered content `Yes` checked (`true`); `Related video` → to be set to the 007 long once it is uploaded, before the Short goes public on Fri 13 Nov 11:30Z.
- **Records:** Registered in `SHORTS_UPLOAD_INDEX.json`, `SHORTS_RELEASE.json`, `00_Brand/Channel-Setup/audits/SHORTS_LOG.md`, `00_Brand/Channel-Setup/audits/shorts_open_library/library.json` (`status=scheduled`), and `00_Brand/Channel-Setup/social/UPLOADS.json` (Buffer held until public; ready for `buffer-mirror.ts register --channel hos` once OWB PR #260 merges and 007 long has an id).

```text
PASS  hos_007_s04_smallpox_test_v01.mp4  dur=26.13s  audio=-24.1dB  motion=18.05  dhash=86e766dfda1e867f
   sheet /var/folders/1z/ymtxygjd7cnfrxjv7sqgmww40000gn/T/hos_shorts_gate/hos_007_s04_smallpox_test_v01_open_sheet.jpg
PASS  02_Video-Projects/007_The-First-Vaccine/11_Upload-Package/PACKAGE_MANIFEST.json
   warn  [captions] no captionsFile (captions from the script)
PASS  02_Video-Projects/007_The-First-Vaccine/10_Shorts/SHORTS_RELEASE.json
   warn  [related] What Was the Edward Jenner Experiment?: Related video not set yet (set it to the 007 long once that long is public)
PASS  Short -I_GHK-GcFs  private 2026-11-13 11:30 UK  What Was the Edward Jenner Experiment?
45 videos, 0 errors.
ALL CHECKS PASS
```

## 24 Oct 2026 — Short `s05_vacca_jesty_v01` (Test B, second search-titled lift from Part 04, OWB J0898)

- **Selection:** HOS 004, 005, 006, and 001 each have 5 built search-titled Shorts (`s04`–`s08` / `s07`–`s11`); HOS 002 and 003 each have 4. HOS 007 had 1 built search-titled Short (`s04_smallpox_test_v01`), making 007 the locked HOS long with the fewest built Shorts (1 of its 2 Test B search-titled Shorts).
- **VO (0 spend):** `02_Voiceover/part04_the_test_v01b.mp3` 60-word sentence-aligned lift (words `62..76 + 103..147`, zero overlap with `s04_smallpox_test_v01` words `0..61`, 007 Short B in Part 02, and Short C in Part 05): *"Jenner wasn't the first to try cowpox. Benjamin Jesty had done it twenty-two years earlier. He tested more people, and in seventeen ninety-eight he paid to print a short book. He called the disease by a Latin name, variolae vaccinae, which means smallpox of the cow. From vacca, the Latin word for cow, came the name for the treatment: vaccination."* 60 words, pauses capped at 0.14 s, `atempo=1.07`, 23.817 s VO + 0.35 s tail = 24.167 s total (146 wpm).
- **Picture & bed (0 spend):** Chief-KEPT plates `P5:09_meadow_golden_t1` (in `2.20 s`, frame 0 and the 3.0 s loop, `crop_x=660`), `P2:06_jesty_family_t1` (`crop_x=660`), `P4:10_garden_hut_t1` (`crop_x=640`), `P4:08_soho_press_t1` (`crop_x=820`), `P5:10_history_book_t1` (`crop_x=640`), `P1:01_cow_meadow_t1` (`crop_x=660`), `P4:10a_packets_t1` (`crop_x=640`) — zero plate overlap with `s04_smallpox_test_v01`. Own-synthesis warm harmonic pad (`hos007_s05_synth_pad_v01.wav`, G-major pastoral voicing, 0 credits) at −20.0 dB under VO. Hook **NOT THE FIRST** (FIRST in yellow). Person/date card **BENJAMIN JESTY · Dorset · 1774** at 2.40–5.80 s (3.4 s, lower third of 16:9 centre band, 0.35 s fade in/out); the long's exact title *Why Vaccines Are Named After a Cow* at 9.0–14.0 s; word captions throughout with exclusive `gte(t,s)*lt(t,e)` handovers (18 captions, 17/17 handovers verified single-caption); CTA `watch the full film →` on the last 3.0 s.
- **Title draft:** *Why Is It Called a Vaccine?* (signed-out GB YouTube autocomplete exact hits `why is it called vaccines` / `vaccine latin words` / `benjamin jesty` / `who invented the first vaccine` / `edward jenner cowpox vaccine`, 24 Oct 2026; alts *Who Tried Cowpox Before Edward Jenner?*, *Where Does the Word Vaccine Come From?*).
- **File:** `10_Shorts/hos_007_s05_vacca_jesty_v01.mp4`, 24.167 s, sha256 `c3eece7477deeddaab4caebdfe801849384554e649c26867d90ae05f4fc99e3c`; phone copy iCloud `HOS UAT/007_The-First-Vaccine/10_Shorts/hos_007_s05_vacca_jesty_v01.mp4`. One picture_qa / polish look-at, not a fail: `10_history_book_t1` at 0:13, low detail (edge density 0.0340 < film p5 0.0375).

```
PASS  hos_007_s05_vacca_jesty_v01.mp4  dur=24.17s  audio=-24.1dB  motion=16.17  dhash=727d2edf57490736
   sheet /var/folders/1z/ymtxygjd7cnfrxjv7sqgmww40000gn/T/hos_shorts_gate/hos_007_s05_vacca_jesty_v01_open_sheet.jpg
PASS  hos_007_s05_vacca_jesty_v01.mp4  0:24.17  mean -24.1 dB  peak -4.7 dB  146 wpm
   warn  replace at ~0:12.04: script 'a latin name variolae vaccinae which means' / heard 'a latin name varioli vaccinae which means' — sounds alike (likely the transcriber); listen
   warn  replace at ~0:17.28: script 'the cow from vacca the latin word' / heard 'the cow from vaca the latin word' — sounds alike (likely the transcriber); listen
polish gate PASS: 0 of 8 rows failed, 1 to look at -> 02_Video-Projects/007_The-First-Vaccine/10_Shorts/qa_s05_vacca_jesty_v01/polish_gate_s05_vacca_jesty_v01.json
picture QA PASS: 0 of 8 cuts fail, 1 to look at -> 02_Video-Projects/007_The-First-Vaccine/10_Shorts/qa_s05_vacca_jesty_v01/picture_qa_s05_vacca_jesty_v01/PICTURE_QA.md, 02_Video-Projects/007_The-First-Vaccine/10_Shorts/qa_s05_vacca_jesty_v01/picture_qa_s05_vacca_jesty_v01/picture_qa_review.jpg
```

Gate run with `--air-date 2027-01-26` (gate only). Caption check: 18 changes, ratio 1.0, 17/17 handovers verified single-caption. Freezedetect: 0 events.

**STOP:** parked for Chief: Short PASS, title and slot. Nothing uploaded.

## 24 Oct 2026 — J0909 (`J0899` Change 2): 2-way Thumbnail T&C launch plan, neighbour search terms in description/tags & 12–15 s Short cut test plan (Gemini covering)

- **Authority:** Chief PASS on `J0899` (`02_Video-Projects/_analytics/HOS_2026-10-24.md` §4 #2) and queue job `J0909`. `£0` spend, no live YouTube changes.
- **Applied to `11_Upload-Package/` and `08_Thumbnail/README.md`:**
  1. **2-way Thumbnail Test & Compare plan on launch (`LAUNCH_PLAN.md`, `08_Thumbnail/README.md`, `PACKAGE_MANIFEST.json`):** Documented Variant A (**`THE MILKMAID'S / SECRET`**) vs Variant B (**`IMMUNE`**) for launch T&C alongside Title T&C (*Why Vaccines Are Named After a Cow* vs *How Was the First Vaccine Made?*) and `relatedVideoId: "_C92tIJCk8A"` (001 Germs end screen).
  2. **Neighbour search terms woven into description lines 1–2 and tags (`Descriptions/vaccine_long_description_v01.txt`, `Tags/vaccine_long_tags_v01.txt`):** Wove `"Edward Jenner cowpox vaccine"`, `"deadly smallpox virus"`, and `"why can't every shot be a pill"` into lines 1–2 of `vaccine_long_description_v01.txt` and added `edward jenner cowpox vaccine` + `deadly smallpox virus` to `vaccine_long_tags_v01.txt` (8 tags total, 0 channel names).
  3. **Second 12–15 s Short cut test (`LEARNINGS.md` #4) & payoff timing (`≥70%` runtime):** Documented in `LAUNCH_PLAN.md` and `PACKAGE_MANIFEST.json`.
- **Package lint (`npm run lint:package -- --film 007`):** `PASS  02_Video-Projects/007_The-First-Vaccine/11_Upload-Package/PACKAGE_MANIFEST.json` & `PASS  02_Video-Projects/007_The-First-Vaccine/10_Shorts/SHORTS_RELEASE.json`.

## 24 Oct 2026 — Short `s05_vacca_jesty_v02` built (title-safe banner re-wrap), packaged & uploaded Private (`4WUs0beKn0A`, Tue 17 Nov 11:30 London, OWB J0906)

- **Authority:** Chief PASS with one fix on `J0898` and Chief-created `J0906`. `£0` spend.
- **Fix in `_build_short_s05_vacca_jesty_v01.py` (`VER="v02"`):** Re-wrapped the 9–14 s title banner to two lines `'Why Vaccines Are'` (`508.9 px` wide, `x=285.6..794.4 px`) / `'Named After a Cow'` (`542.4 px` wide, `x=268.8..811.2 px`) inside title-safe; nothing else changed.
- **Build & QA (`hos_007_s05_vacca_jesty_v02.mp4`, `24.167 s`, 60 words, sha256 `89a9a1668d7470acb27e5a93a77641aaeeaf6aed053fa418d899c776f4d3b88e`):** Copied to iCloud `HOS UAT/007_The-First-Vaccine/10_Shorts/hos_007_s05_vacca_jesty_v02.mp4`. All gates PASS (`gate_shorts_open --air-date 2026-11-17`, `vo_check`, `polish_gate`, `picture_qa`, `freezedetect 0`, `handovers 10/17 ok=True`).
- **Upload & schedule:** Packaged in `10_Shorts/11_Upload-Package/s05_vacca_jesty/PACKAGE_MANIFEST.json` (`SHORTS_RELEASE.json` PASS) and uploaded Private via `npm run youtube:package` as **`4WUs0beKn0A`** (`https://youtu.be/4WUs0beKn0A`), title **`Why Is It Called a Vaccine?`**, for the first free HOS Short slot after `2026-11-13T11:30Z`: **Tue 17 Nov 2026 at 11:30 London (`2026-11-17T11:30:00Z`, GMT)** (since Fri 13 Nov is `-I_GHK-GcFs`, Sun 15 Nov is `x_3L_IdYgEc`, and Mon 16 Nov is `-sa2t7dAtCk`).
- **API readback (`API_READBACK_4WUs0beKn0A.json`):** `privacyStatus=private`, `publishAt=2026-11-17T11:30:00Z`, `uploadStatus=processed`, `madeForKids=false`, `selfDeclaredMadeForKids=false`, `defaultLanguage=en-GB`, `defaultAudioLanguage=en-GB`, `categoryId=27`, `hasCustomThumbnail=true`, 6 tags.
- **Studio readback (`STUDIO_READBACK_4WUs0beKn0A.json`, CDP `:9460`):** `No, it's not Made for Kids` checked (`true`), Altered content `Yes` checked (`true`); `Related video` → added to `J0875` to be set to the 007 long once it is uploaded, before the Short goes public on Tue 17 Nov 11:30Z.
- **Records:** Registered in `SHORTS_UPLOAD_INDEX.json`, `SHORTS_RELEASE.json`, `11_Upload-Package/LAUNCH_PLAN.md`, `00_Brand/Channel-Setup/audits/SHORTS_LOG.md`, `00_Brand/Channel-Setup/audits/shorts_open_library/library.json` (`status=scheduled`), and `00_Brand/Channel-Setup/social/UPLOADS.json`, and added to `J0875`.

```text
PASS  hos_007_s05_vacca_jesty_v02.mp4  dur=24.17s  audio=-24.1dB  motion=16.17  dhash=727d2edf57490736
   sheet /var/folders/1z/ymtxygjd7cnfrxjv7sqgmww40000gn/T/hos_shorts_gate/hos_007_s05_vacca_jesty_v02_open_sheet.jpg
PASS  hos_007_s05_vacca_jesty_v02.mp4  0:24.17  mean -24.1 dB  peak -4.7 dB  146 wpm
polish gate PASS: 0 of 8 rows failed, 1 to look at -> 02_Video-Projects/007_The-First-Vaccine/10_Shorts/qa_s05_vacca_jesty_v02/polish_gate_s05_vacca_jesty_v02.json
picture QA PASS: 0 of 8 cuts fail, 1 to look at -> 02_Video-Projects/007_The-First-Vaccine/10_Shorts/qa_s05_vacca_jesty_v02/picture_qa_s05_vacca_jesty_v02/PICTURE_QA.md, 02_Video-Projects/007_The-First-Vaccine/10_Shorts/qa_s05_vacca_jesty_v02/picture_qa_s05_vacca_jesty_v02/picture_qa_review.jpg
PASS  02_Video-Projects/007_The-First-Vaccine/11_Upload-Package/PACKAGE_MANIFEST.json
   warn  [captions] no captionsFile (captions from the script)
PASS  02_Video-Projects/007_The-First-Vaccine/10_Shorts/SHORTS_RELEASE.json
   warn  [related] What Was the Edward Jenner Experiment?: Related video not set yet (set it to the 007 long once that long is public)
   warn  [related] Why Is It Called a Vaccine?: Related video not set yet (set it to the 007 long once that long is public)
PASS  Short 4WUs0beKn0A  private 2026-11-17 11:30 UK  Why Is It Called a Vaccine?
48 videos, 0 errors.
```





## 23 Oct 2026 — J0887 candidate master v03 (Gemini, Ben's 3 changes on v02, £0 / 0 Flow credits)

- **Ben's 3 changes on `master_v02`:**
  1. **`1:48` (*"When she's milking the cow the hand is misaligned"*):** Replaced `#21 P2:01_milking_dawn` (`1:40.83–1:48.08`, `174` frames) with `01_milking_dawn_v03.mp4` rendered from clean `0`-credit Flow Nano Banana 2 still `01_milking_dawn_v03b.png` (zero paint-patching) with subpixel push-in, animated milk stream `(1014, 712) -> (1022, 825)`, sunbeam motes, and Part 2 overlays `p2_ch` + `p2_cowpox`. Both of the dairymaid's hands meet the centre of the cow's pink udder naturally right above the wooden bucket, with the milk stream flowing straight down from her hands into the bucket.
  2. **`3:50` (*"Mascot here is way to big"*):** Replaced `#42 P2:14_explorer_stool` (`3:44.79–3:50.46`, `136` frames) with `14_explorer_stool_v03.mp4` rendered from `0`-credit Flow Nano Banana 2 wide byre still `14_explorer_stool_v03.png` with subpixel push-in and sunbeam motes. The Explorer stands at child-sized house scale (~1/3 of frame height, clearly smaller than the seated adult dairymaid and cow, never dominating the frame).
  3. **`8:25` (*"Ends very promptly, maybe something like subscribe to be alerted when the new video is out"*):** Extended `#97 P5:12_kite_storm_v03` (`8:20.08–8:27.08`, `168` frames = `7.00 s`) so the last VO word at `8:24.67` breathes `2.41 s` while the music resolves; added `#98 P5:14_closing_card_v03` (`8:27.08–8:31.08`, `96` frames = `4.00 s`) with a house Didot closing card over moving storm clouds naming next week's film (*Why Did Franklin Fly a Kite in a Storm?*, `Next film · Thursday 19 November`) and `Subscribe to see it first · @HistoryOfScienceYT` (cued with house ink tick #44 at `507.18 s`); followed by `20.00 s` of moving 3D cartoon picture (`#99..#102`, `8:31.08–8:51.08`: golden meadow, Berkeley village & church, Temple of Vaccinia garden hut, leather history books) and a `1.50 s` picture & music fade to black (`8:49.58–8:51.08`). No new VO.
- **Files (NAS & iCloud `HOS UAT`):**
  - Master v03: `/Volumes/data/mac-mini-archive/hos-007-vaccine/master_v03_J0887/hos_007_master_v03.mp4` (`531.083333 s`, `12,746` frames, `102` cuts, `-14.0 LUFS / -1.4 dBTP`, sha256 `b4c329a057f4dd2e1b676cefa63adcd52d0be1b0346dd298295ad90159020dad`)
  - Phone copy (`<120 MB`): `/Volumes/data/mac-mini-archive/hos-007-vaccine/master_v03_J0887/hos_007_master_v03_PHONE.mp4` (`102.95 MB`, sha256 `db612314a3ed83e5a498d9bc6e8090e5212c21618f1084969efd51467be953e2`)
  - Check sheet: `/Volumes/data/mac-mini-archive/hos-007-vaccine/master_v03_J0887/ben_changes_check_sheet_v03.jpg` (`sha256: 22428d8607b0a1d7a30a28139e9a874edb0126323167f7be7831152867f5e4b9`)
  - Contact sheet: `/Volumes/data/mac-mini-archive/hos-007-vaccine/master_v03_J0887/hos_007_master_v03_contact_sheet.jpg` (`sha256: 4e23b27c032e876265b3bc64f94a41752ef0714c412f999c0d563f46102d9e78`)
  - iCloud UAT: `~/Library/Mobile Documents/com~apple~CloudDocs/HOS UAT/007_The-First-Vaccine/` (`hos_007_master_v03.mp4`, `hos_007_master_v03_PHONE.mp4`, `ben_changes_check_sheet_v03.jpg`, `hos_007_master_v03_contact_sheet.jpg`)

```text
SFX level PASS: VO -16.1 LUFS, SFX -35.4 LUFS, 44 hits
music gate PASS: vaccine_score_bed_v01.mp3, 531.1 s, about 60.0 BPM, brief Pace: 58-64 BPM
polish gate PASS: 0 of 102 rows failed, 6 to look at -> /private/tmp/j0887-hos007-v03-wt/02_Video-Projects/007_The-First-Vaccine/07_Edit-Project/master_v03_pack/polish_gate.json
picture QA PASS: 0 of 102 cuts fail, 6 to look at -> /private/tmp/j0887-hos007-v03-wt/02_Video-Projects/007_The-First-Vaccine/07_Edit-Project/master_v03_pack/PICTURE_QA.md, /private/tmp/j0887-hos007-v03-wt/02_Video-Projects/007_The-First-Vaccine/07_Edit-Project/master_v03_pack/picture_qa_review.jpg
Episode gate Decision: PASS — VO / Gemini Veo allowed; Script score: 92.3/100 · PASS
freezedetect: 0 events; encoded loudness: I: -14.0 LUFS, Peak: -1.4 dBFS
```

Full frame-by-frame evidence and gate outputs: `07_Edit-Project/master_v03_pack/REVIEW_master_v03.md`. Parked for Chief review (`J0887`). No approved edit stage claimed.

## 25 Oct 2026 — J0925 candidate master v04 (Gemini, Ben's 3 changes on v03, £0 / 0 Flow credits)

- **Ben's 3 changes on `master_v03` (HOS #180 `6376001097`, Chief ruling `6384888711`):**
  1. **`0:38` (*"the wooden figures look like they fall through the shelf and vanish. Replace or trim the plate so nothing passes through solid objects."*):** Replaced `#007 P1:07b_three_in_ten` (`0:35.17–0:38.96`, `91` frames) with `07b_three_in_ten_v04.mp4` rendered from `0`-credit Flow Nano Banana 2 16:9 still `07b_three_in_ten_v04.png` (`upscale: 1.0`) with smooth subpixel push-in, soft window motes, and Part 1 overlay `p1_data_3in10` (`3 in 10 died · Smallpox case fatality`). Ten intact one-piece turned-wood peg dolls (7 standing upright, 3 lying on their sides) rest solidly on top of the oak cottage windowsill through the final frame; nothing passes through or vanishes into the shelf.
  2. **`2:40` (*"it should be a scratch, not a needle going into the arm. Historically Jenner made two shallow cuts in James Phipps's skin with a lancet, so show a lancet scratching the surface, with no needle going in."*):** Replaced `#031 P2:06b_jesty_hands` (`2:35.42–2:41.75`, `152` frames) with `06b_jesty_hands_v04.mp4` rendered from `0`-credit Flow Nano Banana 2 16:9 still `06b_jesty_hands_v04.png` (`upscale: 1.0`) with smooth subpixel push-in, warm farmhouse daylight motes, and Part 2 overlay `p2_when_1774` (`Dorset, 1774`). Shows an authentic 18th-century folding tortoiseshell-and-steel medical lancet held at a shallow grazing angle scratching two shallow lines along the top of the forearm skin, with no needle going into the arm.
  3. **`4:22` (*"something odd comes off the boy's arm when the doctor places the matter on it (AI artefact). Replace the plate or cut around it."*):** Replaced `#048 P3:04_lancet_touch` (`4:15.83–4:22.42`, `158` frames) with `04_lancet_touch_v04.mp4` rendered from `0`-credit Flow Nano Banana 2 16:9 still `04_lancet_touch_v04.png` (`upscale: 1.0`) with smooth subpixel push-in, warm study window motes, and Part 3 overlay `p3_who_phipps` (`James Phipps · Age about 8`). Edward Jenner in his sunlit 1796 Berkeley study gently touches a folding steel lancet at a shallow grazing angle to 8-year-old James Phipps's clean upper arm; zero protruding object or AI artefact on the boy's arm.
- **Files (NAS & iCloud `HOS UAT`):**
  - Master v04: `/Volumes/data/mac-mini-archive/hos-007-vaccine/master_v04_J0925/hos_007_master_v04.mp4` (`531.083333 s`, `12,746` frames, `102` cuts, `-14.0 LUFS / -1.4 dBTP`, sha256 `c7f62adbb241bf3fbfaa3a17929f05768eedcf89044cb2cc5ebd2971c163e810`)
  - Phone copy (`<120 MB`): `/Volumes/data/mac-mini-archive/hos-007-vaccine/master_v04_J0925/hos_007_master_v04_PHONE.mp4` (`102.49 MB`, sha256 `58e89a6fb5d3698cd10885fbf763f7cf722d6deb64d950cb3e2ec3bb8dced8d3`)
  - Check sheet: `/Volumes/data/mac-mini-archive/hos-007-vaccine/master_v04_J0925/ben_changes_check_sheet_v04.jpg` (`sha256: 0f8f5d21fef5be277cb1b92b60e7068d7ee00d98936d34a8ad0825722bbecb8e`)
  - Contact sheet: `/Volumes/data/mac-mini-archive/hos-007-vaccine/master_v04_J0925/hos_007_master_v04_contact_sheet.jpg` (`sha256: 0ddfb02688bb698c69ae5aa315a17fe1e76d21e3d24256592647605f9635a861`)
  - iCloud UAT: `~/Library/Mobile Documents/com~apple~CloudDocs/HOS UAT/007_The-First-Vaccine/` (`hos_007_master_v04.mp4`, `hos_007_master_v04_PHONE.mp4`, `ben_changes_check_sheet_v04.jpg`, `hos_007_master_v04_contact_sheet.jpg`)

```text
SFX level PASS: VO -16.1 LUFS, SFX -35.4 LUFS, 44 hits
music gate PASS: vaccine_score_bed_v01.mp3, 531.1 s, about 60.0 BPM, brief Pace: 58-64 BPM
polish gate PASS: 0 of 102 rows failed, 6 to look at -> /private/tmp/j0925-hos007-v04-wt/02_Video-Projects/007_The-First-Vaccine/07_Edit-Project/master_v04_pack/polish_gate.json
picture QA PASS: 0 of 102 cuts fail, 6 to look at -> /private/tmp/j0925-hos007-v04-wt/02_Video-Projects/007_The-First-Vaccine/07_Edit-Project/master_v04_pack/PICTURE_QA.md, /private/tmp/j0925-hos007-v04-wt/02_Video-Projects/007_The-First-Vaccine/07_Edit-Project/master_v04_pack/picture_qa_review.jpg
Episode gate Decision: PASS — VO / Gemini Veo allowed; Script score: 92.3/100 · PASS
freezedetect: 0 events; encoded loudness: I: -14.0 LUFS, Peak: -1.4 dBFS
```

Full frame-by-frame evidence and gate outputs: `07_Edit-Project/master_v04_pack/REVIEW_master_v04.md`. Parked for Chief review (`J0925`). No approved edit stage claimed.
