# Part 02 lessons — Seeing the Tiny World

**Date:** 2026-08-27  
**Status:** **STOP for Ben UAT** is not ready — **9/10** real Flow Veo clips exist; plate **10** blocked on Flow credits. No Ken Burns. No Part 03.

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

## Real motion progress (`raw/v01_flow/`)

| Plate | Status |
|---|---|
| 01_chapter_lab_scope | **DONE** Veo 3.1 Lite (~2.2MB, 8s) |
| 02_lens_flare_eye | **DONE** Veo 3.1 Lite (~1.8MB, 8s) |
| 03_drop_of_water | **DONE** Veo 3.1 Lite (~1.0MB, 8s) |
| 04_plunge_into_drop | **DONE** Veo 3.1 Lite (~4.8MB, 8s) |
| 05_microbial_city | **DONE** Veo 3.1 Fast (~3.8MB, 8s) |
| 06_explorer_eyepiece | **DONE** Veo 3.1 Lite (~2.1MB, 8s) |
| 07_tiny_world_hold | **DONE** Veo 3.1 Lite (~3.5MB, 8s) |
| 08_ward_vs_lens | **DONE** Veo 3.1 Lite (~1.5MB, 8s) |
| 09_faceless_swarm_detail | **DONE** Veo 3.1 Lite (~3.1MB, 8s) |
| 10_pullback_to_lab | **BLOCKED** — Create send missing; Flow exact error below |

Did **not** assemble `hos_001_part02_rough_v01.mp4` (need all 10 mp4s). No Ken Burns fill for plate 10.

## Exact Flow error (plate 10, 27 Aug ~21:34 UTC)

Hovering the prompt-bar **info** chip / empty Create slot:

> **error**  
> **Not enough Google Flow and AI credits to perform this action. Try other settings or get more AI credits.**  
> Settings · Get more AI credits

Create/arrow is absent; orange send is gone. Model stayed **Veo 3.1 - Lite** (did not switch to Fast).

## Flow workflow that works (locked)

1. Upload start still → right-click **Animate**
2. Model **Veo 3.1 - Lite** (5 credits Ultra; Fast OK if needed) · 16:9 · x1 — never Omni Flash / Nano Banana
3. Prompt + Create → **approve credit confirmation**
4. Wait ~2 min → download mp4 from player
5. Playwright helper: `try_context_animate` + `confirm_generation_spend` in `orbit_flow_veo_ui.py`
6. Current Flow prompt bar may show **`add_2 Create`** (plus) instead of `arrow_forward`; the real send is the orange circle — it disappears when credits are exhausted.

## Do not

- Assemble or UAT still-push as the Part 02 rough
- Assemble a 9-plate cut and call it the animated rough
- Start Part 03 until a real animated Part 02 rough exists and Ben passes it
- Fall back to zoompan / sine-pan and call it animation

## Next

When Flow credits reopen: generate **10_pullback_to_lab** on **Veo 3.1 Lite** → assemble `_build_part02_flow_v01.py` (RAW=`v01_flow`) → `hos_001_part02_rough_v01.mp4` → Ben UAT.
