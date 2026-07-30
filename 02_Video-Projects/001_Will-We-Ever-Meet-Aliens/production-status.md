# Video 001 — production status

## Approved look reference
- **v06 (timing/audio/Orbit):** `09_Final-Export/aliens_BOLD_EXPLAINER_v06_FINAL_POLISHED_MASTER.mp4`
- Loved: timestamp, Orbit mascot, illustrated art.
- Problem: beds were **still PNGs** driven with shaky `zoompan` Ken Burns — not Seedance video.

## Current animated rebuild
- **Export:** `09_Final-Export/aliens_BOLD_EXPLAINER_v07_ANIMATED_BEDS_MASTER.mp4`
- **90s proof:** `09_Final-Export/aliens_v07_ANIMATED_BEDS_PROOF_90s.mp4`
- **30s Seedance hook proof:** `09_Final-Export/aliens_v07_ANIMATED_HOOK_PROOF_30s.mp4`
- Same v06 audio mix remuxed; same v06 Orbit Overlay-Rig choreography.
- **9/96** boards are real Seedance Mini i2v clips (opening + early boards).
- **87/96** use smooth locked pan (no zoompan shake) until fal balance is topped up.

## Blocker for full Seedance beds
fal.ai balance exhausted mid-batch (`User is locked. Reason: Exhausted balance`).
Resume with:
```bash
cd 07_Edit-Project
python3 -u _animate_bold_scenes_seedance_v07.py
python3 -u _build_bold_explainer_v07_animated.py
```
