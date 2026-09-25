# Incident: Eiffel Tower start frame (2026-07-27)

## What happened
Priority A clips were generated with the Explore-page **Eiffel Tower blueprint** as `start_frame`, not Orbit.

Confirmed asset IDs:
- Bad: `ip6374dwIHSvg6Mj26uR`, `0OK31NLICqegCGr3MNJF` (Eiffel blueprint, ~5.3MB)
- Good: `oaCGb79I7Rh3JDVKANKW` / `kw23OgO1bzq4slMsEKUg` (`orbit-seedance-reference-v01.png`, ~954KB)

## Root cause
Automation uploaded via `input[type=file]` while the UI still had the Explore Eiffel asset bound as start frame (or re-bound it). Prompt text said “Orbit” but Seedance image-conditioned from the wrong start frame.

## Actions
1. Quarantined bad clips → `_Rejected/eiffel-startframe-2026-07-27/`
2. Reverted those 7 rows in `animation-index.csv` to pending
3. Regenerating with verified Orbit start-frame asset only + explicit “no Eiffel/blueprints” prompt line

## Guardrail for future gens
Before Generate: confirm `start_frame` asset **name** is `orbit-seedance-reference-v01.png` (or size ~954KB). Abort if asset is the Eiffel explore IDs above.

## 2026-07-27 batch4 scene-027
B-roll cosmic-timeline submitted with start_frame MHJat0UJOfmZsyW4izJR (Eiffel Explore asset still in library). Two iterations generated. Aborted remaining batch. Quarantined; regenerating with request-body strip guard.

## 2026-07-27 — user request: remove Eiffel

All quarantined Eiffel-contaminated MP4s deleted from disk (Orbit `_Rejected/eiffel-startframe-2026-07-27/` and Video 001 `eiffel-startframe-027-20260727/`).

**Clarification:** The Eiffel Tower was never a creative choice. An ElevenLabs Explore blueprint asset was accidentally bound as Seedance `start_frame`. Video 001 does not use and must not use any Eiffel imagery.
