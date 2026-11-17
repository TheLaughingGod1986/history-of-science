# J2230 Vaccine Shorts v05 checks (14 Nov 2026)

Worker: cursor. Spend: £0. No upload, no schedule, no awaits.

Files (desk renders, not in git):

- Variolation v05: `/Users/benjaminoats/_desk/renders/J2230/vaccine_v05/hos_007_variolation_v05.mp4`
  sha256 `c7ae95379e11a355916f2087ffb04efe81bf458069195b729ee280786b1ebbc2`, 23.33 s
- Eradication v05: `/Users/benjaminoats/_desk/renders/J2230/vaccine_v05/hos_007_eradication_v05.mp4`
  sha256 `3482c23f30bcd4abf1bbd2031a7d55c6e2c7a44fda48481b5e0ce236378bb505`, 21.23 s

What v05 changed from the previous cuts:

- Variolation keeps the full words. The alignment has "variolation" at 79.12–80.06 s and "but" at 80.06–80.96 s. v04 ended those windows at 79.70 s and 80.35 s, and the voice check heard "varialitin" with "but" missing. v05 uses 78.28–80.96 s for that line. Voice check now PASS, with one sounds-alike warn ("on to" / "onto").
- The card tick is a 50 ms tone at −12 dB. v04's −28 dB tick never crossed the hit floor. `sfx_kit.py level` PASS on both stems (one hit, SFX about 24 LU under the voice).

Checks that PASS:

- Variolation and Eradication: voice check, SFX level, polish gate, picture QA (one low-detail warn on a hold frame in each).
- Music gate on the film's own `vaccine_score_bed_v01.mp3` (sha256 matches the plan): PASS, 60 BPM, brief Pace 58–64. Two unreadable comparison files warned.
- Eradication open gate: PASS, with a duration warning at 21.23 s.

Checks that do not pass:

- Variolation open gate FAIL: `Orbit in frame at 0 s (visor 0.0103 ≥ 0.003)`. The frame is the lancet in the red case, not Orbit. The same plate without the hook scores visor 0.0078. A sweep of portrait crops from x=400 to x=1040 stayed at or above 0.009. The child plate at 67.7 s scores visor 0.0003, and the earlier build found that plate too still for the moving-open check.
- Eradication cannot reach 22 s inside the approved pauses. Speech is 19.37 s. The approved breaths top out near 0.20 + 0.40 + 0.40 + 0.99 s, about 21.4 s. v05 is 21.23 s.

Willow stays the two scheduled Shorts. Harvey v04 is unchanged. No watch card.
