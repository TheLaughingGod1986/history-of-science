# Part 02 lessons — Seeing the Tiny World

**Date:** 2026-08-26  
**Status:** BLOCKED — need real Veo animation (Ben rejected still-push)

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

## Real motion progress

| Plate | Status |
|---|---|
| 01_chapter_lab_scope | **DONE** Flow Veo 3.1 **Lite** (27 Aug PM) |
| 05_microbial_city | **DONE** Flow Veo 3.1 Fast |
| 02–04, 06–10 | **BLOCKED** — daily gen limit again after plate 01 Lite |

Prefer **Lite (5 credits)** for remaining plates when daily gens reopen.

## Flow workflow that works (locked)

1. Upload start still → right-click **Animate**
2. Model **Veo 3.1 - Lite** (5 credits Ultra; Fast OK if needed) · 16:9 · x1 — never Omni Flash / Nano Banana
3. Prompt + Create → **approve credit confirmation**
4. Wait ~2 min → download mp4 from player
5. Playwright helper: `try_context_animate` + `confirm_generation_spend` in `orbit_flow_veo_ui.py`

## Do not

- Assemble or UAT still-push as the Part 02 rough
- Start Part 03 until a real animated Part 02 rough exists and Ben passes it
- Fall back to zoompan / sine-pan and call it animation

## Next

When Flow daily gens reopen: finish **8** remaining plates on **Lite** (~40 credits) → assemble `hos_001_part02_rough_v01.mp4` → Ben UAT.
