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
3. Gemini quota blocked v03 Veo regen mid-run.
4. **Interim rough v03:** microbe beats use push-in on the faceless still (no smiles) until Veo quota recovers for true motion plates.

## Next

- Resume `_build_part01_rough_v01.py` when quota resets → real v03 Veo from `MICROBE_REF`.
- Replace still-bridges; Ben re-UAT before Part 02.
