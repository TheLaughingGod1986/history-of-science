# Part 02 lessons — Seeing the Tiny World

**Date:** 2026-08-29  
**Status:** **STOP for Ben UAT** — ward beat reminted as **v04**. Do **not** start Part 03 until Ben passes this cut. Do **not** treat agent output as PASS.

## Ben UAT (locked)

- Interim rough was **shaky** (sine pan) **and not animated** (Ken Burns / still-push).
- **Reject:** any still-zoom / sine-pan / overlay-drift cut shipped as Part 02 picture.
- **Require:** real Flow/API Veo I2V motion on every plate (same bar as Part 01 early Veo plates).
- **Watch 0:53–1:01 hard:** nurses/steam/cloth must move with camera locked. v01–v03 failed that beat.

## Style parent

Must match Part 01 **v08 PASS**. Faceless microbes only. Sparse germs. Prefer Animistry **3D cartoon** over photoreal ward.

## Assets ready

- Script: `01_Script/part02_seeing_tiny_world_v01.md`
- VO: `02_Voiceover/part02_seeing_tiny_world_v01.mp3` (~87s)
- Stills: `04_Generated-Clips/part02/refs/*_v01.jpg` (10/10) + ward start `08_ward_vs_lens_v03.jpg`
- Rejected still-push: `09_Final-Export/hos_001_part02_rough_v01_STILLPUSH_REJECT.mp4`
- Rejected ward plates: `raw/v01_flow/08_ward_vs_lens_v02.mp4`, `raw/v03_flow/08_ward_vs_lens_v03.mp4` — **do not splice again**
- **UAT cut (ward remint):** `09_Final-Export/hos_001_part02_rough_v04.mp4` (~76.4s; v01 audio; plate 08 = v04 I2V at 0:53–1:01)
- Ward plate: `04_Generated-Clips/part02/raw/v04_flow/08_ward_vs_lens_v04.mp4`

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
| 08_ward_vs_lens | **v04 remint** Veo 3.1 Lite I2V (~1.6MB, 8s). Scope bbox locked across 0.2→7.5s (no Ken Burns). MAE ~30 — steam/glow/particles move; nurse lean may read subtle. Style leans cinematic — Ben UAT. Helpers: `_mint_part02_ward_v04.py`, `_splice_part02_v04_ward.py`. |
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

## Ward v04 remint notes (2026-08-29, Mini)

- Hypothesis: Flow Ingredients + “continuous camera motion” wrapper invented zoom on a locked still → Ken Burns fail on v02/v03.
- v04 path: locked-camera prompt · animate people/cloth only · splice only 0:53–1:01 of v01 · keep v01 audio.
- Local metrics: plate↔rough MAE ≈1.3 (splice OK). Microscope bbox stable (camera lock OK). Not a PASS — Ben watches acting + style.

## Next

Ben UAT `hos_001_part02_rough_v04.mp4` (especially **0:53–1:01**). Pass / regen notes. Then Part 03 only.
