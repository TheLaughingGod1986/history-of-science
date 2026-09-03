# Part 01 lessons — Germs (LOCKED PASS)

**Date:** 2026-08-26  
**Status:** **PASS** — Ben locked style on `hos_001_part01_rough_v08.mp4` (cut now `hos_001_part01_rough_v21.mp4`)

**Film-wide doctor continuity (2 Sep 2026):** any two-doctor plate in this film must match KEEP 0:48 (`07_mocked_v12` — mustache younger + grey 1840s beard). Do **not** remint this locked cut unless CoS sends a UAT FAIL with stills. Finish 03 v14 first. Rule: `.cursor/rules/hos-part03-doctor-continuity.mdc`.

## Locked look

Animistry-class 3D cartoon · Victorian ward · Explorer garnish · faceless germs · continuous motion through the close.

Canonical docs:
- `00_Brand/Channel-Setup/HOS_PART01_STYLE_BASELINE_LOCKED.md`
- `.cursor/rules/hos-part01-style-baseline.mdc`
- `.cursor/rules/hos-microbe-visual-lock.mdc`
- Open/out: this death-ward picture **is** the film open (no branded intro) — `00_Brand/Channel-Setup/HOS_OPEN_OUT_LOCKED.md` · `.cursor/rules/hos-open-out-lock.mdc`

Artifact: `/opt/cursor/artifacts/hos_001_part01_rough_v08.mp4`

## What Ben approved (v08)

| Rule | Detail |
|---|---|
| Style | Keep the v01 cartoon world (not v03–v07 redesigns) |
| Germs | Faceless only — no smiles / winks |
| Density | Fewer germ-float scenes; story world leads |
| Motion | Last stretch must stay animated (not still-zoom) |

## What failed (do not repeat)

| Cut | Fail |
|---|---|
| v01 | Smiling germs (style otherwise good) |
| v03–v06 | Ward-first / stillbridge / modern hospital |
| v07 | Photoreal Flow drift |
| early v08 end | Still-zoom after ~1:10 — fixed with motion beds + drifting faceless overlays |

## Build helpers to copy forward

- Faceless micro assets: `04_Generated-Clips/part01/refs/v08_micro_assets/`
- End-motion repair: `07_Edit-Project/_fix_v08_end_motion.py`
- Part builder pattern: `07_Edit-Project/_build_part01_v08_faceless.py`

## Next

**Part 02 — Seeing the Tiny World** (microscope / microbial city). Match this lock. Stop for Ben UAT after Part 02 rough.
