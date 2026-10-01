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
