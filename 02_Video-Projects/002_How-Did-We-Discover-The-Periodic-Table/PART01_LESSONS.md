# Part 01 lessons — Periodic Table (LOCKED PASS)

**Date:** 2026-09-03  
**Status:** **PASS** — Ben locked picture on `hos_002_part01_rough_v11.mp4`  
**sha256:** `48c55ac66f1e91ddcd1ea765b6a6e53336a5ba495a99377e5ef6bf14e88aa384`  
**VO:** `02_Voiceover/part01_zoo_of_stuff_v02.wav` · **85.680s**

Canonical cut: `09_Final-Export/hos_002_part01_rough_v11.mp4` · iCloud `HOS UAT/`  
Do **not** remint Part 01 unless Ben sends a UAT FAIL with stills from **v11**.

## Locked look

Animistry-class 3D cartoon · period chemistry workshop · Explorer garnish **once** · continuous motion · continuous curious-workshop music bed under VO.

Style parent: Germs Part 01 v08 / v21 cartoon world (warm wood, not photoreal, not modern lab).

## What Ben failed (do not repeat on Part 02+)

| Fail | Bad plate(s) | Lock going forward |
|---|---|---|
| Wrong Explorer (adult / satchel rummage / glowing chair) | 05 | Younger boy on Germs lock identity; **hold ore in hands**; empty scale pans; no glowing furniture as hero |
| Powder / pour **misses** flask mouth | 06 | Prefer **opaque ceramic tip + powder spill + smoke puff** — no live pour into a clear neck |
| Bubbles floating **in air** above liquid meniscus | 02 / 07 / 08 / 11 / 12 | **OPAQUE** ceramic jars + sealed metal canisters only. Ban clear glass liquids |
| Clear flask floating / sitting beside scale | 10 | Table around scale **empty of glassware**. Ore **flat inside** brass pan. Heat = colourless shimmer only (no flames / orange coals) |
| Watching superseded roughs | v07–v10 stills | Always UAT the **latest** rough filename only |

## Prompt physics lock (copy into every workshop plate)

```
Prefer OPAQUE ceramic jars / sealed metal canisters / solid cylinders.
ZERO clear glass flasks with liquid. ZERO bubbles in air. ZERO floating glassware.
Nothing hangs or floats above pans/stands — objects sit IN / ON contact surfaces.
Heat = colourless shimmer / haze only unless VO explicitly asks for fire.
Exactly ONE Explorer when called for — Germs Part 01 younger-boy lock. No twins. No Orbit.
No readable text / logos / UI. Silent picture. Continuous motion the whole clip.
```

## Process lessons

1. **Duration guard** — reject Flow downloads outside ~6–12s (contamination / wrong clip).
2. **Archive rejects** — `_rejected_uat_vNN/` before overwrite; bump rough version.
3. **Flow login** — `looks_logged_in` must accept `flow.google.com` (UI left labs.google).
4. **Assemble from current RAW** — never ship an iCloud cut that does not match reminted RAW.
5. **Explorer I2V** — attach a composition start frame (correct scale + props). Do not I2V the full-frame identity sheet as a wide hero.
6. **Mute test** — picture must tell the beat without VO (list → triads → broken pattern).

## Build helpers to copy forward

- Plates: `07_Edit-Project/parts/part-01_plates_v01.json`
- Remint pattern: `07_Edit-Project/_remint_part01_uat_v10_plate10.py` (duration guard + archive)
- Assemble: `07_Edit-Project/_assemble_part01_rough_v11.py`
- Explorer refs: `04_Generated-Clips/part01/refs/hos-explorer-character-sheet-v01.jpg` · `explorer_germs_part01_lock.jpg`
- Flow helper: `04_Audio/tools/orbit_flow_veo_ui.py`
- Profile: `~/.playwright-hos-flow-profile`

## Next

**Part 02 — First Patterns, Still Wrong** (Lavoisier list · Döbereiner triads · Newlands octave gag).  
Apply this physics lock on every plate. Explorer **once** on triad-break (05). Stop for Ben UAT after Part 02 rough.
