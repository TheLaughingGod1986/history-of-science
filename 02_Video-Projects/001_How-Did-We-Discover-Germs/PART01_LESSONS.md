# Part 01 lessons — Germs

**Date:** 2026-08-26

## Ben UAT

- **Reject:** smiling / winking / cute-faced cartoon germs.
- Germs = invisible **enemy** — stylised rods/spheres OK, **no faces**.
- Locked: `.cursor/rules/hos-microbe-visual-lock.mdc`
- Reject proof: `00_Brand/Channel-Setup/inspiration/REJECT_smiling_germs_part01_example.png`

## What we tried

1. Text-only prompt lock → Veo **still invented smiles** (v02 frames).
2. Built **faceless start-frame** (`refs/faceless_microbes_ref_v01.jpg`) for I2V.
3. Gemini Veo quota blocked v03/v04 motion regen.
4. **Interim rough v03:** microbe beats = push-in on faceless still (no smiles).
5. **Interim rough v04:** ward-first stillbridges (Flash Image stills) + corridor/hands motion.

## Ben UAT (round 2)

- Too many germs in the first minutes → **human ward first**.
- Mascot (**Explorer**) should **walk past beds** with a couple of **sick/ill patients**.
- Germs: faceless + **sparse**, late in the minute.

## Fix path (v04)

| Beat | Picture |
|---|---|
| Open | Ward with ~2 sick patients (no germs) |
| Mid | Explorer walks past beds / ill patients |
| Late | Sparse faceless microbes only when VO names the invisible enemy |

- Plate plan locked in `_build_part01_rough_v01.py` (Veo motion path).
- Interim assemble: `_build_part01_v04_still_interim.py` → `hos_001_part01_rough_v04.mp4`
- Stills under `04_Generated-Clips/part01/refs/*_v04.jpg`
- Artifact: `/opt/cursor/artifacts/hos_001_part01_rough_v04.mp4`

## Ben UAT (round 3) — jumpy / frozen

- v04 stillbridges read as **images**, not video.
- **v05b polish** (Veo still quota-blocked): multi-angle chains with **near-full-length dissolves** (~5.2s overlap on ~6.5s takes) so the picture is almost always morphing + continuous Ken Burns + lamp flicker.
- Builder: `_build_part01_v05_motion_polish.py` → `hos_001_part01_rough_v05.mp4` (~70s)
- Corridor + doctor-hands remain true Veo motion from earlier gens.
- Artifact: `/opt/cursor/artifacts/hos_001_part01_rough_v05.mp4`
- Honest limit: without Veo I2V, Explorer/patients cannot truly walk/breathe — only camera + morph. Real motion resumes when Gemini Veo quota is topped up.
- Quarantined old germy corridor plate: `part01/_rejected_germ_corridor_v01/` (swarm in the aisle). Clean corridor stills: `corridor_*_v05.jpg`.

## Still blocked

- Full **Veo character/patient motion** (429 RESOURCE_EXHAUSTED).
- When quota returns: I2V from v05 stills → true walk/breathe plates; keep ward-first narrative.
