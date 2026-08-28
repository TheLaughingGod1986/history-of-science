# Part 02 lessons — Seeing the Tiny World

**Date:** 2026-08-28  
**Status:** **STOP for Ben UAT** — animated rough is ready. Do **not** start Part 03 until Ben passes this cut.

## Ben UAT (locked)

- Interim rough was **shaky** (sine pan) **and not animated** (Ken Burns / still-push).
- **Reject:** any still-zoom / sine-pan / overlay-drift cut shipped as Part 02 picture.
- **Require:** real Flow/API Veo I2V motion on every plate (same bar as Part 01 early Veo plates).

## Style parent

Must match Part 01 **v08 PASS**. Faceless microbes only. Sparse germs.

## Assets ready

- Script: `01_Script/part02_seeing_tiny_world_v01.md`
- VO: `02_Voiceover/part02_seeing_tiny_world_v01.mp3` (~87s)
- Stills: `04_Generated-Clips/part02/refs/*_v01.jpg` (10/10)
- Rejected still-push: `09_Final-Export/hos_001_part02_rough_v01_STILLPUSH_REJECT.mp4`
- **Animated rough:** `09_Final-Export/hos_001_part02_rough_v01.mp4` (~76.4s picture; VO trimmed to picture)

## VO–picture polish (2026-08-28)

Ben: camera-in-drop at ~25s did not follow the narration.

- Root cause: prompt said “camera plunges” + start still already contained a photographic camera. Veo literalised it.
- Fix: I2V from `03_drop_of_water` still; prompt forbids cameras; assemble order is now **lab → pond drop → eyepiece/spectrum → dive**.
- Do **not** put the word “camera” in HOS plunge prompts unless you mean a photographic object.


## Real motion inventory (`raw/v01_flow/`)

| Plate | Status |
|---|---|
| 01_chapter_lab_scope | **DONE** Veo 3.1 Lite (~2.2MB, 8s) |
| 02_lens_flare_eye | **DONE** Veo 3.1 Lite (~1.8MB, 8s) |
| 03_drop_of_water | **DONE** Veo 3.1 Lite — **subtle** motion (low frame-diff); watch in UAT |
| 04_plunge_into_drop | **DONE v02** Veo 3.1 Lite from pond-water still — dive into faceless microbes. **v01 CAMERA REJECT** quarantined |
| 05_microbial_city | **DONE** Veo 3.1 Fast (~3.8MB, 8s) |
| 06_explorer_eyepiece | **DONE** Veo 3.1 Lite — camera moves; Explorer acting may look stiff (UAT) |
| 07_tiny_world_hold | **DONE** Veo 3.1 Lite (~3.5MB, 8s) |
| 08_ward_vs_lens | **DONE** Veo 3.1 Lite (~1.5MB, 8s) |
| 09_faceless_swarm_detail | **DONE** Veo 3.1 Lite (~3.1MB, 8s) |
| 10_pullback_to_lab | **DONE** Veo 3.1 Lite (~2.1MB, 8s, real motion; Flow flashed “failed” then mp4 arrived) |

## Flow send bug (2026-08-28)

`submit_create` was matching **`add_2 Create`** (plus / asset picker) before **`arrow_forward Create`** (orange send). That left an empty Uploads modal (“No results found”) and `gen=False` forever. Fix: dismiss the picker, click **arrow_forward only**. Never click `add_2` to start a gen.

Plate 10 landed in ~72s after that fix (Lite, start-frame Animate path).

## Flow workflow that works (locked)

1. Upload start still → right-click **Animate**
2. Model **Veo 3.1 - Lite** (5 credits Ultra; Fast OK if needed) · 16:9 · x1 — never Omni Flash / Nano Banana
3. Prompt + **arrow_forward** Create → **approve credit confirmation**
4. Wait ~1–3 min → download mp4 from player (ignore a brief “failed” flash if video/mp4 arrives)
5. Playwright helper: `try_context_animate` + `confirm_generation_spend` + arrow-only `submit_create`

## Do not

- Treat the still-push file as the Part 02 rough
- Start Part 03 until Ben passes this animated cut
- Fall back to zoompan / sine-pan and call it animation

## Next

Ben UAT `hos_001_part02_rough_v01.mp4`. Pass / regen notes. Then Part 03 only.
