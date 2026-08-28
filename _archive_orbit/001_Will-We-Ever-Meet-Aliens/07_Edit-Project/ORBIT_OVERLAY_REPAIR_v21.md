# Orbit Overlay Repair v21

## Problems found

- The broadcast enlarged 112 px proxy sprites, which made Orbit look soft.
- Generated expression sprites used mismatched crops and a distorted replacement visor.
- Orbit changed expression and apparent position too often.
- The live mascot appeared over text cards, while some cards also contained a baked mascot.
- The lower-left placement could cover card copy and felt detached from the composition.

## v21 treatment

- Built a clean cutout from the canonical neutral Orbit artwork.
- Removed disconnected stars, debris, and noisy alpha pixels without overwriting the master.
- Created a fixed 420 x 380 transparent ProRes 4444 overlay rig.
- Added a restrained six-second idle cycle: gentle tilt, slow hover, and one natural blink.
- Fixed Orbit to one lower-right home position with only a few pixels of drift.
- Increased readable on-screen size to roughly 22% of frame height.
- Added a subtle soft shadow for separation from bright and dark footage.
- Hid Orbit on text cards, chapter cards, brand plates, and the outro.
- Preserved all previous exports and created a separate v21 review and master export.

## Outputs

- Review: `09_Final-Export/aliens_v21_PROOF_stable_orbit_90s.mp4`
- Full: `09_Final-Export/aliens_broadcast_v21_stable_orbit.mp4`
- Selective-host review: `09_Final-Export/aliens_v22_PROOF_selective_orbit_90s.mp4`
- Recommended selective-host master: `09_Final-Export/aliens_broadcast_v22_selective_orbit.mp4`
- Reusable rig: `01_Orbit-Character/06_Animation-Exports/Overlay-Rig-v01/orbit_overlay_idle-blink_6s_v01.mov`
- Timeline record: `07_Edit-Project/SECTION_EDL_v21_stable_orbit.json`

## Selective-host refinement

The stable v21 treatment proved the placement and animation, but kept Orbit on
screen for about 64% of the film. The recommended v22 cut reduces this to nine
deliberate appearances, one per narrative section. Each appearance fades in
and out over 0.28 seconds, and the final YouTube end screen is left untouched
because it already includes Orbit artwork.

## Verified

- 1920 x 1080
- 30 fps
- H.264 video
- AAC stereo audio at 48 kHz
- 635.5 seconds
- Previous versions remain present
