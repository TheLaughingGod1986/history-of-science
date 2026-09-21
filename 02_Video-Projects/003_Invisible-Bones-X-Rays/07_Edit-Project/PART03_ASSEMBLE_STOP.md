# HOS 003 Part 03 — ASSEMBLE STOP (VO missing)

**Status:** **STOPPED** — plate-first Batch A UAT PASS plate set is on Mini, but assemble cannot run.  
**Dated:** 21 Sep 2026 · Europe/London  
**Do not:** mint Veo · remint plates · invent VO · ping Ben · Public upload

## Blocking missing paths

Expected house VO masters (P01/P02 pattern) are **absent**:

1. `02_Voiceover/05_Master/hos_003_part03_vo_*_draft.wav`
2. `02_Voiceover/05_Master/hos_003_part03_vo_*_draft.mp3`
3. `02_Voiceover/05_Master/hos_003_part03_vo_*_draft_align.json`
4. `02_Voiceover/_generate_part03_vo_*.py` (no generator script yet)

`05_Master/` currently has only Part 01 + Part 02 drafts.

## Present (not blocking alone)

| Asset | Path | Note |
|---|---|---|
| VO text v01 | `02_Voiceover/part03_bones_without_a_knife_v01.txt` | board `vo_file`; sha `aa4ec877…` · 615 B |
| VO text v02 | `02_Voiceover/part03_bones_without_a_knife_v02.txt` | densified; sha `b8e165cc…` · 1203 B — **no audio yet** |
| Music bed | `02_Video-Projects/001_How-Did-We-Discover-Germs/05_Music/hos_001_part01_ominous_ward_v14_norm.wav` | same ominous ward bed as P01/P02 |
| Timing board | `07_Edit-Project/parts/part-03_plates_v01.json` | `clip_use_s` 7.9 · `xfade_s` 0.35 · side labels |
| Cue sheet | *(none)* | no `PART03_ASSEMBLE*_CUES.md`; labels live on plates JSON |

## Plate sha verify (clips dir)

Dir: `04_Generated-Clips/part03/`

| Plate | On-disk sha256 | vs handoff |
|---|---|---|
| `01_chapter_bones_v01.mp4` | `ebb64736279d6455d062e740d154d272ead839662eca7865ef4eb0e0a61a6926` | **handoff typo** — CoS wrote `…a61aafc6`; Mini land index + mint JSON match `…a61a6926` (KEEP file OK) |
| `02_hand_enters_path_v03.mp4` | `8df82c6eee13158a9866b356323f59d3080deb2910f40c99443dbe9eeba94a14` | OK |
| `03_soft_fades_v01.mp4` | `5278f40d88f7c65949c773dbdf31633d94200d8badd67a6fe77a712a1e275b1a` | OK |
| `04_bones_hold_v03.mp4` | `d1b54bb9cf7bf5ca2621bbd4cef959b9d2f23b09a84178f7a68110557279db25` | OK |
| `05_ring_darker_v05.mp4` | `a57705df6eaca9c42bdd3a94e7f8f3aa0633c492cc0659c0f57988c89349cf93` | OK |
| `06_living_skeleton_read_v02.mp4` | `c2ebf454c382e4fa866e35eba023f312cba60ff8cb5e5326e557a8fabdb7263b` | OK |
| `07_explorer_hand_beam_v01.mp4` | `2c938277d3f743fe459ae5bd935adb5dd1bdad80538951a56b08a76e0599617a` | OK |
| `08_medicine_question_v02.mp4` | `e770f6783382d6ebad9eaedbc0b57e3fcbf32192d0a48891a2b3670f3671a36a` | OK |
| `09_wonder_v02.mp4` | `efcf9c67d62b40b10ece57ea5c6ebc52e7616ca8579880d5fa666bac30938e18` | OK |
| `10_caution_burn_v02.mp4` | `366a6e5b6a2107ebf9f3d95d9ed30ca0aa740b7ec55e99725a155772b5329da2` | OK |
| `11_hold_beam_v02.mp4` | `d9bbd16b12a964c479ced75d397e44cb1abd25e4545a82f32aeb33c1241e8fe8` | OK |

## Unblock (CoS / Showrunner)

1. Lock VO text (v01 board vs densified v02 — P02 used densified).
2. Generate Ben Orbit Narrator masters into `02_Voiceover/05_Master/` (wav + mp3 + align), matching P01/P02 house.
3. Re-open assemble → write `hos_003_part03_rough_v01.mp4` + `ASSEMBLE_LAND.json`.

No rough mp4 written. No Veo spend. No Ben ping.
