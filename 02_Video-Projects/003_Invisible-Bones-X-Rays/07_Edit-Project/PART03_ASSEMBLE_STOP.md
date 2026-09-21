# HOS 003 Part 03 — ASSEMBLE STOP

**Status:** **STOPPED** — plate remint BATCH PASS is not enough; CoS blocked assemble for **missing VO audio masters**.

**Dated:** 21 Sep 2026 ~18:35 London / BST (docs); VO mint owned by parent on Mini

## Why stopped
CoS will not open Mini Cursor assemble for `hos_003_part03_rough_v01.mp4` until Orbit Narrator masters exist under `02_Voiceover/05_Master/`:
- `hos_003_part03_vo_v02_draft.wav` (or locked v01 if VO_LOCK says so)
- matching `.mp3`
- matching `_align.json`

## Who owns the mint
**Parent / Showrunner on Mini** (`machineId` `1e756e4d-88c1-4572-8ef7-e7984cce785f`) — writing `PART03_VO_LOCK.md` + `_generate_part03_vo_v02.py` and running TTS.  
**This agent:** do **not** start a second ElevenLabs mint (avoid double spend).

## When masters land
1. Confirm sha256 of wav (+ mp3/align) on Mini.
2. Flip this sheet / `PART03_ACCEPTANCE.md` / cues to **ASSEMBLE OPEN**.
3. Point cues VO section at the new master paths (not txt-only).
4. Ping CoS to reopen assemble — do **not** declare Ben PASS; do **not** run ffmpeg assemble unless CoS asks.

## Plate board (ready; not the blocker)
Remint 8 + KEEP 01/03/07 per `BATCH_A_REMINT_LAND_INDEX.json`. Cue draft (parked): `PART03_ASSEMBLE_V01_CUES.md` — treat as draft until VO masters land and OPEN is re-stamped.
