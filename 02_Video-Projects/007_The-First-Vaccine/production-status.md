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
| Edit | **Full join v01 (`hos_007_full_join_v01.mp4`, 505.15 s / 12,123 frames, 97 cuts, sha256 `7cfd6a59`) assembled (J0827, 22 Oct 2026, £0)** across Parts 01–05 (Chief PASS J0820) on locked VO with house Didot teaching cards and both £0 repeat-shot fixes (`P1:09c_case_again` 1.88× lancet crop; `P5:06c/06d` split into strictly unused `04_health_workers` back half `3.833–7.958 s` + `06_assembly_1980` tail `5.083–8.000 s` 1.38× front-row push-in). Parts: P1 `61a5c039` (100.83 s, 20 cuts) · P2 `6ab2fb1f` (129.62 s, 22 cuts) · P3 `62a14a08` (78.75 s, 15 cuts) · P4 `e6a005cd` (92.75 s, 20 cuts) · P5 `14206aeb` (103.17 s, 20 cuts). Full join PASS `polish_gate.py` (`0 of 97 rows failed, 5 to look at`) and `picture_qa.py` (`0 of 97 cuts fail, 5 to look at`), 0 freeze events (`>= 0.8 s`). UAT proxy (`5ea31960`) in `~/Library/Mobile Documents/com~apple~CloudDocs/HOS UAT/007_full_join_v01/`. Parked for Chief review (`REVIEW_v01.md`). |
| Air | proposed **Thu 12 Nov 2026 18:00 UK = 18:00 UTC** (GMT); privacy private; madeForKids false; proposals only |
| Shorts | `s04_smallpox_test_v01` uploaded Private `-I_GHK-GcFs` for Fri 13 Nov 2026 11:30 UK (`2026-11-13T11:30:00Z`, J0873); `s05_vacca_jesty_v01` built (J0898, 24.167 s, sha256 `c3eece7477de`, parked for Chief: Short PASS + title + slot); Related → 007 long once uploaded |
| Backup | Neighbour gate PASSED — Lightning backup not needed |

## STOP

- No Vertex/Veo/Flow minting on this film.
- No spending.
- Do not merge or touch desk PR #180 from this scaffold PR.

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



