# Open pull requests: a decision table (J2495)

Read on 10 Nov 2026 against `main` at `34c6f379`. Table only: nothing was merged, closed or pushed to another branch.

**27 pull requests: 17 to close, 6 to carry, 4 for the Chief to read.** #180 (the desk) is never merged or closed and is not in the table.

How to read the columns:
- **Files**: of the files the pull request adds or changes, how many are *missing* from main / already on main *byte for byte* / on main but *different*.
- **Replaced by**: the later work on main that covers it. A commit hash is on main.
- **Shared code**: anything under `00_Brand/Channel-Setup/tools`, `07_Content-Ops`, `.github`, `studio-core`, `.cursor/rules` or `AGENTS.md`.
- **Email**: does an added line hold a personal email address. The address is never copied here.

| PR | Opened | Base | Files: missing / same / differs | Replaced by | Shared code | Email | Recommend |
|---|---|---|---|---|---|---|---|
| #457 | 7 Nov, draft | main | 1 / 0 / 3 | #468 and #470: the 009 tranche-2 runner was repaired and reviewed on 10 Nov. Main's runner has 67 functions, this one 50. | no (a film's own runner and its test) | yes, 2 lines; the same 2 lines are already in main's copy | **CLOSE** |
| #454 | 7 Nov, draft | main | 1 / 0 / 3 | As #457, which contains this one's two commits. | no | yes, the same 2 lines | **CLOSE** |
| #437 | 6 Nov, draft | main | 1 / 0 / 1 | #464 (J2461: the later pin attempt and its read-back). J0958 is open again for one more try. | no | no | **CLOSE** |
| #434 | 5 Nov | main | 0 / 0 / 7 | Nothing. Main does not have experiment E2. | yes: `AGENTS.md`, three Cursor rules | no | **REVIEW** |
| #433 | 5 Nov | main | 0 / 0 / 6 | Its gate change only: #461 synced `gate_shorts_open.py` from the studio on 10 Nov. | yes: one Cursor rule, `gate_shorts_open.py`, `studio-core/CORE_FILES.json` | no | **REVIEW** |
| #431 | 5 Nov | main | 6 / 13 / 7 | Its first commit only (#430 merged it). | no | no | **CARRY** |
| #427 | 5 Nov | main | 0 / 1 / 1 | `b78dbe19` (J2217) rewrote the same file, and Ben's 5 Nov notes file is on main. | no | no | **CLOSE** |
| #405 | 4 Nov, draft | main | 0 / 0 / 8 | LEARNINGS rule 26 (9 Nov): search phrase first, 70 characters. These are 50-character rewrites under the older rule 15. | no | no | **CLOSE** |
| #403 | 3 Nov | main | 3 / 0 / 4 | `J1880_SOURCE_INVENTORY_v04.json`, the J2163 correction manifest and J2217, all on main. | no | no | **CLOSE** |
| #401 | 3 Nov | main | 1 / 0 / 3 | Ben's 5 Nov notes reopened the 008 master (J1868, J2217). The 3 differing files are generated. | no | no | **CLOSE** |
| #382 | 30 Oct | **#380's branch**, not main | 141 / 7 / 9 | Not replaced. Roughs v06 to v09 on main name `code_graphics_v02`, `v03` and `v04`; their build scripts and manifests exist only in this stack. | no | no | **CARRY** (top of the stack) |
| #380 | 30 Oct | main | 81 / 7 / 9 | Contained in #382. | no | no | **CLOSE** once #382 is carried |
| #379 | 30 Oct | main | 34 / 7 / 9 | Contained in #380. | no | no | **CLOSE** once #382 is carried |
| #378 | 30 Oct | main | 0 / 0 / 2 | Its review file has a later version in #382. Not part of the stack. | no | no | **CLOSE** once #382 is carried |
| #376 | 29 Oct | main | 16 / 7 / 6 | Contained in #379. | no | no | **CLOSE** once #382 is carried |
| #359 | 23 Oct, draft | main | 7 / 0 / 6 | Master v05 was built on main at 0 credits (`7196b52a`), beside this work, not after it. | no | no | **CARRY** (records) |
| #357 | 23 Oct | main | 0 / 0 / 2 | The opening gate (LEARNINGS rules 8 and 24) now enforces what this checklist asks a writer to tick. | yes: one Cursor rule | no | **REVIEW** |
| #355 | 22 Oct, draft | main | 21 / 52 / 1 | `master_v03_pack` and `master_v04_pack` are on main (52 files identical). | no | no | **CARRY** |
| #353 | 22 Oct | main | 0 / 37 / 25 | `786e631e` (J0827, the full join) rewrote the same 25 files. | no | no | **CLOSE** |
| #349 | 20 Oct, draft | main | 3 / 0 / 1 | Three later B thumbnails for 001 on main: boiled clear broth v04, sterile liquid flask v06, curved dust bend v08. | no | no | **CLOSE** |
| #348 | 16 Oct | main | 742 / 5 / 16 | Mostly. Plans are now built on the locked voice-over (013: #473); Shorts plans v02 and v03 are on main. | no | no | **CARRY** six files, close the rest |
| #347 | 16 Oct | main | 9 / 0 / 8 | The Short was uploaded again as `xzKoHg0E0_U`; the register on main already says so. | no | no | **CARRY** (9 upload records) |
| #345 | 16 Oct | main | 3 / 0 / 5 | `46d59506` (22 Oct): all 73 rows minted and logged. The recovered clip's two hashes are in main's log. | no | no | **CLOSE** |
| #334 | 15 Oct, draft | main | 3 / 0 / 1 | The pinned-comment milestones are on main (`update-pinned-comment.ts`). | yes: two scripts under `07_Content-Ops/scripts` | no | **REVIEW** |
| #325 | 15 Oct | main | 9 / 10 / 1 | Master v05 (`7196b52a`) and the film's Studio finish (`47de9a4e`). 006 is public. | no | no | **CLOSE** |
| #200 | 4 Oct | main | 6 / 0 / 1 | The Vertex hold was lifted and 006 shipped. Main's credit log is later (`0462e902`). | no | no | **CLOSE** |
| #195 | 2 Oct | main | 2 / 4 / 5 | `747a8347` (15 Oct keep sweep, Parts 01 to 05) and the later Flow driver (`825ad027`). | yes: `04_Audio/tools/orbit_flow_veo_ui.py` | yes: its two new files each hold an address | **CLOSE** |

## The six to carry

Carry means: copy the named files onto a fresh branch from main, never merge the old branch. For `STATUS.md` and `00_Brand/Channel-Setup/kanban/index.html` the answer is always "regenerate with `status_board.py`". For `PIPELINE.json`, `VIDEO_BACKLOG.json`, `UPLOADS.json` and `library.json`, keep main's: each has moved on since.

**#431, HOS 011 Shorts scripts v02 and the upload package.** The board says J2239 is done, but its files are not on main. Carry the 6 missing files: `10_Shorts/SHORTS_SCRIPTS_v02.md`, and under `11_Upload-Package/` the long description, the tags, `PACKAGE_MANIFEST.json`, `PRODUCTION_CHECKLIST_V2.md` and the Shorts search evidence. `SCRIPT_NOTES_v01.md`: compare and keep the later wording. Both `production-status.md` files: keep main's and add one line for J2239 to 011's.

**#382, the HOS 008 graphics and rough-cut stack (it carries #380, #379 and #376).** Main's rough builds v06 to v09 read `code_graphics_v02` to `v04`, yet main holds only v01 and v05. Carry every missing file (141; 14 MB, mostly review stills): `_build_code_graphics_v02.py` to `v04.py`, `_assemble_rough_v01.py` to `v03.py`, `_swap_rough_v04.py`, `_swap_rough_v05.py`, the `code_graphics_v03/` and `code_graphics_v04/` folders, and the evidence under `_desk/008/`. `CODE_GRAPHICS_v01_REVIEW.md`, `part-04_plates_v03.json` and `part-05_plates_v03.json`: take this pull request's versions; main's date from 15 and 16 Oct and nothing touched them since. `production-status.md`: keep main's. Then close #380, #379, #376 and #378.

**#359, HOS 006 motion checkpoint (records of credits spent).** `FLOW_MOTION_LOG_v05.json` records one charged Veo take (10 credits, 20,830 to 20,820) and a second marked "submitting, do not retry". Main has neither. Carry the 7 missing files under `master_v05/`. `FLOW_STILLS_LOG_v05.json`: add this pull request's take entries to main's log; lose none. The two scripts: keep main's. The studio's spend ledger has one line for J0886: check the second take is in it.

**#355, HOS 007 master records.** The v03 and v04 packs are on main; the v01 pack, the bed brief, the sound-effects kit manifest, `J0830_CONTINUE.md` and `_master_audio_v01.py` are not. 007 airs on Thu 12 Nov, and the script that mastered its audio should be in the repo. Carry the 21 missing files. `production-status.md`: keep main's.

**#348, six files out of 763.** Carry: for 009, `PICTURE_PLAN_v05.json`, `PRICE_REVIEW_v05.md` and `_build_plate_boards_v05.py` (main has the v05 plates, and four files name them, but not the plan, price or build script). For 010, `PICTURE_PLAN_v03.json`, `PRICE_REVIEW_v03.md` and `_build_plate_boards_v03.py` (main's v04 plan names v03, which is missing). Do not carry: the 702 plate boards for 78 future films, written before any voice-over (each is rebuilt on its locked voice-over when its turn comes, as 013 was); the 007 v03 and 008 v04 boards (nothing on main names them); the Shorts picture plans v01 (v02 and v03 are on main); the 013 files (its "v02" is older than main's v01 from #473, so it would muddle the numbering).

**#347, the first Dalton Short upload.** `-sa2t7dAtCk` was really uploaded on 16 Oct and later replaced by `xzKoHg0E0_U`. Carry the 9 record files under `004_.../10_Shorts/11_Upload-Package/s05_dalton/`. Everything that differs: keep main's.

## The four to read

**#434, experiment E2 (proof-first first 30 seconds, longs 008 to 010).** It adds 72 lines across `AGENTS.md`, the playbook, the strategy, three Cursor rules and the retention learnings: cuts under 4.5 s in the first 30 s, at least 7 moving plates, the apparatus on screen from 0:05 to 0:15, the first data graphic between 0:25 and 0:40. It merges cleanly today. The studio's LEARNINGS already lists E2 as an approved test (row 30) and 013's picture plan follows it, so the channel's own rules are behind. Recommendation: merge after a read.

**#433, experiment E1 (anomaly-first Short opening, 008 to 010).** Two parts. The rule text (16 lines in the Shorts Cursor rule, 4 in the strategy, the template and the learnings) can be carried as it stands. The other part adds 261 lines to `gate_shorts_open.py`, which is a copied studio tool: #461 replaced it on 10 Nov with the studio's first-second checks, so this change conflicts and must not be merged here. If the anomaly check is still wanted it goes into the studio's gate and is synced. Recommendation: carry the rule text, drop the gate change, and ask whether the studio gate already covers it.

**#357, a tick-list of Learnings 1 to 5 for Shorts briefs.** It adds a checklist to the Shorts Cursor rule and the brief template (12 and 10 lines). It was written on 23 Oct against five learnings; there are now 30, and the opening gate enforces the important ones by machine. Recommendation: close. A tick-list that restates the gate will drift from it.

**#334, HOS 004 launch-day helpers.** Two one-off scripts under `07_Content-Ops/scripts` that set the playlist order and pin for 15 Oct, a result note, and wording in `PINNED_COMMENTS.json`. The launch is done and main already has the milestone logic. One-off scripts do not belong in the shared tools. Recommendation: close; carry `LAUNCH_DAY_15_OCT_RESULT.md` alone if the record is wanted.

## One thing these pull requests did not cause

Main itself already holds an account email address in tracked files: 2 lines in the 009 tranche-2 runner and lines in four HOS 006 mint logs and scripts. Both repos are public. That needs its own job: read the account from an untracked setting and write "the studio Ultra account" in records.
