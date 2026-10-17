# HOS 003 Invisible Bones — production status

## Live (checked 25 Sep 2026 on the public channel)

| Asset | Id | State |
|---|---|---|
| Long *How Did We Discover X-rays?* (7:06) | `frP_YrNShsU` | Public. Premiered Thu 24 Sep 2026 18:00 London |
| S1 *How X-rays Were Discovered by Accident* | `oowAOWTBoq0` | Public (Fri 25 Sep 11:30) |
| S2 *How did Röntgen see bones without cutting* | `xvanpsLeADE` | Scheduled Sat 26 Sep 11:30 |
| S3 *The first X-ray showed a wedding ring* | `zI_eD3vFWmE` | Scheduled Sun 27 Sep 11:30 |

Schedule and upload records: `11_Upload-Package/Schedule/HOS_003_STUDIO_SCHEDULE.md`. Do not remint or re-upload. Per `HOS_STRATEGY.md`, the next long goes out as a normal publish, not a Premiere.

The part notes below are the build history (last updated 21 Sep).

**Updated:** 21 Sep 2026 (assemble land)
**Premiere title:** How Did We Discover X-rays?

| Part | Status |
|---|---|
| 01 | KEEP/LOCK v03 |
| 02 | KEEP/LOCK `hos_003_part02_rough_v03.mp4` ~61.6s — no remint |
| 03 | **LANDED** `hos_003_part03_rough_v01.mp4` · 83.417s · sha `c2b09230…541615d` — VO v02 lock · no Ben ping yet |
| 04–05 | Density + silent-read house for later |

## Part 03 rough

- Path: `09_Final-Export/hos_003_part03_rough_v01.mp4`
- Land: `07_Edit-Project/ASSEMBLE_LAND.json` status `LANDED`
- VO: `part03_bones_without_a_knife_v02` masters (~101.68s; mix trims ~18.3s to picture)
- Bed: `hos_001_part01_ominous_ward_v14_norm.wav`
- Assemble: `07_Edit-Project/_assemble_part03_rough_v01.py`

## New house

`00_Brand/Brand-Guidelines/HOS_HOUSE_SILENT_READABLE_PICTURE_LOCK.md` — Part 03+ only (not P02 remint).


## Ben 14:47 whole-channel Studio §9 (recorded 2026-09-30T17:58:08+01:00)

Channel: `@HistoryOfScienceYT` only. Evidence: `004_…/evidence_2026-09-30_whole_channel_1447/` · `BEN_1447_whole_channel/`.

### 003 videos
| id | kind | notes |
|---|---|---|
| `frP_YrNShsU` | long | Core §9; tags cut from 25+ down to 5 subject tags; playlist How We Found Out missing |
| `oowAOWTBoq0` `xvanpsLeADE` `zI_eD3vFWmE` | Shorts | Core §9 + Related → 003; tags fixed |
| `CUu8k38iAMc` | Short (private dup) | **Left Private** (CoS). Settings only. Tags fixed. |

Academic UK / GCSE Physics / Level won't-save (taxonomy). Visibility unchanged.


## 1 Oct 2026 — Studio: description opening + tags (Grok, desk task on PR #180)

Ben approved in chat with Claude on 1 Oct ("Blood, approve 001/003"). Approved text: `00_Brand/Channel-Setup/audits/NEIGHBOUR_PROPOSALS_2026-10-01.md` (commit 3577b81). Desktop Studio over CDP (port 9460), channel `@HistoryOfScienceYT` only. One setting per save. Title, thumbnail, schedule and file untouched. Test & Compare not touched (two T&C thumbnails made for review on the desk, **not added to Studio**).

`frP_YrNShsU`: new description opening (rest kept):

> X-rays let us see through skin. This is how Röntgen found them: a tube wrapped in black cardboard, a screen across a dark room that glowed when it shouldn't have, and a wedding ring on the first plate.
>
> In a Würzburg lab in 1895, Wilhelm Röntgen chased a glow that had no business being there, and named the unknown ray X.

Tags: x-rays, röntgen, roentgen, wilhelm röntgen, history of physics, history of science

| Save | Result | After save | After reopen |
|---|---|---|---|
| description | saved, reopened and matched | Visibility Public · not made for kids: True | Visibility Public · not made for kids: True |
| tags | saved, reopened and matched | Visibility Public · not made for kids: True | Visibility Public · not made for kids: True |

Evidence: `11_Upload-Package/evidence_2026-10-01_studio/` (`RESULT_003.json`, `before_api.json`, `after_api.json`). Studio screenshots of the description and tags are on the desk (PR #180); originals on the Mini under `~/.local/share/cursor-mac-mini-hos-worker/artifacts/DESK_2026-10-01_001_003/`.

`npm run channel:audit` after the session:

```
PASS  long  frP_YrNShsU  public  How Did We Discover X-rays?
PASS  long  _C92tIJCk8A  public  How Did We Discover Germs?
22 videos, 0 errors.
```

Still Studio-only: Altered content = Yes (by eye; the Data API omits it).


## 1 Oct 2026 — duplicate description line removed + Test & Compare (Grok, desk task 5941493885)

Ben, 1 Oct, in chat with Claude: "1–5 yes" (the 003 duplicate line and the T&C thumbnails v02 approved). Desktop Studio over CDP (port 9460), `@HistoryOfScienceYT` only. One setting per save; Audience and Visibility re-read after each save and after reopening.

**1. Description (23:20 London):** deleted only the paragraph "Something invisible had left the tube. He called it X — for unknown." (it repeated "named the unknown ray X"). Opening, story paragraph, chapters and sign-off unchanged; reopened and matched (`evidence_2026-10-01_studio/DESC_DUP_RESULT_2026-10-01.json`).

**2. Test & Compare, title and thumbnail. Started Thu 1 Oct 2026, 23:27 London (22:27 UTC). Judge nothing before about 500 impressions per variant.**

| Variant | Title | Thumbnail |
|---|---|---|
| A (control) | How Did We Discover X-rays? | current live thumbnail (unchanged) |
| B | Why did a screen glow in a dark room? | `08_Thumbnail/Selected/hos_003_tc_thumb_v02.jpg` (1280×720, sha256 `75b8a7a951a5b5e33f71d3402bdd58ef65b73c4313b59bfdc82d21f23a5d0250`; jpgs are git-ignored) |

| Save | Result | After save | After reopen |
|---|---|---|---|
| description | saved, reopened and matched | Visibility Public · not made for kids: True | Visibility Public · not made for kids: True |
| Test & Compare (Title and thumbnail, 2 variants) | Set test + Save; reopened: "A/B testing titles · Running…" with both titles | Visibility Public · not made for kids: True | Visibility Public · not made for kids: True |

Evidence: `11_Upload-Package/evidence_2026-10-01_studio/TC_RESULT_2026-10-01.json`, `TC_VERIFY_2026-10-01.json`.

`npm run lint:package` before the session: PASS (001 and 003 are SKIP as already-public longs; 004 and 005 PASS).

`npm run channel:audit` after the session (full output on the Mini: `~/.local/share/cursor-mac-mini-hos-worker/artifacts/DESK_2026-10-01_tc/channel_audit_2026-10-01.txt`):

```
PASS  long  frP_YrNShsU  public  How Did We Discover X-rays?
   warn  [ai-disclosure] Data API omits altered/synthetic — confirm Yes in Studio (Altered content)
PASS  long  _C92tIJCk8A  public  How Did We Discover Germs?
   warn  [ai-disclosure] Data API omits altered/synthetic — confirm Yes in Studio (Altered content)

22 videos, 0 errors.
```

Screenshots on the Mini under `~/.local/share/cursor-mac-mini-hos-worker/artifacts/DESK_2026-10-01_tc/` (`VERIFY_<film>_01_details_top.png`, `<film>_tc_commit_04_filled.png`), and on the desk (PR #180). Altered content was not touched in this session (Yes since the 30 Sep sweep; by eye, the Data API omits it).


## 16 Oct 2026 — Short `s04_unknown_x_v01` (Test B, first search-titled lift from Part 02, OWB J0406)

- **Selection:** HOS 004, 005, and 006 each have 2 built search-titled Shorts (`s04` and `s05`); HOS 007+ do not yet have full-part picture. Among locked HOS longs with existing VO and picture, 003 had 0 built Test B search-titled Shorts (only its original 3 punch Shorts S1–S3), so `s04_unknown_x_v01` starts 003's pair of Test B search-titled Shorts.
- **VO (0 spend):** `02_Voiceover/05_Master/hos_003_part02_vo_v01_draft.wav` claim-first lift (word indices `105..118` + `130..184`, skipping question `119..129` so duration stays inside 22–27 s and 55–65 words): *"He calls it X — for unknown. An unknown ray that writes on cardboard. He does not rush the newspapers. He locks the door and tests. Block the path with a book — the glow weakens or shifts. With a hand — soft flesh and denser bone leave different marks. With metal — the shadow hardens. Move the object, move the shadow. The glow changes. Pattern, not ghost story."* 65 words, pauses capped at 0.25 s, `atempo=1.03`, 25.944 s VO + 0.55 s tail = 26.500 s total.
- **Picture & bed (0 spend):** Chief-KEPT plates `P2:07_names_it_x_v01` (`4.90 s` X-chalking window on frame 0 and 3.0 s loop), `P2:11_detector_hold_v01`, `P2:10_test_hand_metal_v01`, `P2:09_test_book_v01`, `P3:02_hand_enters_path_v03`, `P3:05_ring_darker_v05`, `P2:05_glow_blooms_v02`. Own-synthesis warm harmonic pad (`hos003_s04_synth_pad_v01.wav`, D-dorian voicing) at −20 dB under VO. Hook **NAMED IT X** (X in yellow). Person/date card **WILHELM RÖNTGEN · Würzburg, 1895** at 2.15–5.75 s (3.6 s, lower third of 16:9 centre band, feathered shade, 0.35 s fade in/out); the long's exact title *How Did We Discover X-rays?* at 9.0–14.0 s; word captions throughout; CTA `watch the full film →` at 23.49–26.41 s.
- **Title draft:** *What Are X-Rays?* (signed-out GB YouTube autocomplete exact hit, 16 Oct 2026; alts *How Do X-Rays Work?*, *Who Discovered X-Rays?*).
- **File:** `10_Shorts/hos_003_s04_unknown_x_v01.mp4`, 26.500 s, sha256 `3b50feaf513e30e685885ca5980edaae0beab4bafa04c23dbcb88cefe9804546`; phone copy iCloud `HOS UAT/003_Invisible-Bones-X-Rays/10_Shorts/hos_003_s04_unknown_x_v01.mp4`.

```
PASS  hos_003_s04_unknown_x_v01.mp4  dur=26.5s  audio=-22.8dB  motion=20.2  dhash=64c0640c2c284000
   sheet /var/folders/1z/ymtxygjd7cnfrxjv7sqgmww40000gn/T/hos_shorts_gate/hos_003_s04_unknown_x_v01_open_sheet.jpg
PASS  hos_003_s04_unknown_x_v01.mp4  0:26.50  mean -22.8 dB  peak -3.8 dB  147 wpm
polish gate PASS: 0 of 8 rows failed, 1 to look at -> 02_Video-Projects/003_Invisible-Bones-X-Rays/10_Shorts/qa_s04_unknown_x_v01/polish_gate_s04_unknown_x_v01.json
picture QA PASS: 0 of 8 cuts fail, 1 to look at -> 02_Video-Projects/003_Invisible-Bones-X-Rays/10_Shorts/qa_s04_unknown_x_v01/picture_qa_s04_unknown_x_v01/PICTURE_QA.md, 02_Video-Projects/003_Invisible-Bones-X-Rays/10_Shorts/qa_s04_unknown_x_v01/picture_qa_s04_unknown_x_v01/picture_qa_review.jpg
```

Gate run with `--air-date 2026-11-28` (gate only). Caption check: 21 changes, ratio 1.0. Freezedetect: 0 events.

**STOP:** parked for Chief: Short PASS, title and slot. Nothing uploaded.


## 17 Oct 2026 — Short `s05_first_xray_v01` (Test B, second search-titled lift from Part 04, OWB J0423)

- **Selection:** HOS 004, 005, and 006 each have 2 built search-titled Shorts (`s04` and `s05`); HOS 003 had only 1 built search-titled Short (`s04_unknown_x_v01`), so `s05_first_xray_v01` completes 003's pair of Test B search-titled Shorts.
- **VO (0 spend):** `02_Voiceover/05_Master/hos_003_part04_vo_v02_draft.wav` claim-first lift (`7.40–11.96 s` before S3 + `38.76–46.88 s`, `51.48–55.88 s`, `59.44–68.96 s` after S3, zero overlap with S1–S4): *"The photographic plate records bones and her wedding ring. Letters fly across Europe. Labs copy the tube. Doctors lean in. A bullet lodged where eyes cannot go. The body becomes a map you can read while the patient is still whole. Surgery is no longer the only way to look inside. Diagnosis gains a new eye, one that sees density, not blood and guesswork."* 64 words, pauses capped at 0.25 s, `atempo=1.02`, 24.383 s VO + 0.55 s tail = 24.933 s total.
- **Picture & bed (0 spend):** Chief-KEPT plates `P4:03_bones_and_ring_v02` (`2.80 s` hand-bones-and-ring plate window on frame 0 and 3.0 s loop), `P4:05_letters_fly_v01`, `P4:06_labs_copy_tube_v03` (`3.60 s` continuous dolly), `P4:08_bullet_break_map_v07`, `P1:01_skeleton_without_knife_open_v01`, `P5:07_why_groundbreaking_v08`. Own-synthesis warm harmonic pad (`hos003_s05_synth_pad_v01.wav`, A-aeolian/Fmaj7 voicing, distinct from `s04` D-dorian) at −20 dB under VO. Hook **THE FIRST X-RAY** (X-RAY in yellow). Person/date card **BERTHA RÖNTGEN · Würzburg, 1895** at 2.15–5.75 s (3.6 s, lower third of 16:9 centre band, feathered shade, 0.35 s fade in/out); the long's exact title *How Did We Discover X-rays?* at 9.0–14.0 s; word captions throughout; CTA `watch the full film →` at 21.93–24.85 s.
- **Title draft:** *What Was the First X-Ray Picture?* (signed-out GB YouTube autocomplete exact hit `first x ray picture` / `first x ray`, 17 Oct 2026; alts *Who Took the First X-Ray?*, *How Did X-Rays Change Medicine?*).
- **File:** `10_Shorts/hos_003_s05_first_xray_v01.mp4`, 24.933 s, sha256 `f667ee2aad8cbb724321abff7bd7590293d37524fd4a9fb8ff1b1fa148e5e931`; phone copy iCloud `HOS UAT/003_Invisible-Bones-X-Rays/10_Shorts/hos_003_s05_first_xray_v01.mp4`.

```
PASS  hos_003_s05_first_xray_v01.mp4  dur=24.93s  audio=-22.3dB  motion=67.64  dhash=eae5e2345868ec3e
   sheet /var/folders/1z/ymtxygjd7cnfrxjv7sqgmww40000gn/T/hos_shorts_gate/hos_003_s05_first_xray_v01_open_sheet.jpg
PASS  hos_003_s05_first_xray_v01.mp4  0:24.93  mean -22.3 dB  peak -3.6 dB  154 wpm
polish gate PASS: 0 of 7 rows failed, 1 to look at -> 02_Video-Projects/003_Invisible-Bones-X-Rays/10_Shorts/qa_s05_first_xray_v01/polish_gate_s05_first_xray_v01.json
picture QA PASS: 0 of 7 cuts fail, 1 to look at -> 02_Video-Projects/003_Invisible-Bones-X-Rays/10_Shorts/qa_s05_first_xray_v01/picture_qa_s05_first_xray_v01/PICTURE_QA.md, 02_Video-Projects/003_Invisible-Bones-X-Rays/10_Shorts/qa_s05_first_xray_v01/picture_qa_s05_first_xray_v01/picture_qa_review.jpg
```

Gate run with `--air-date 2026-12-01` (gate only). Caption check: 17 changes, ratio 1.0. Freezedetect: 0 events.

**STOP:** parked for Chief: Short PASS, title and slot. Nothing uploaded.

