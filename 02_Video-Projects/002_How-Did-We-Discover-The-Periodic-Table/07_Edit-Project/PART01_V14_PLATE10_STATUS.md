# Part 01 plate 10 remint → v14 — BLOCKED

## Status
**BLOCKED** (no `hos_002_part01_rough_v14.mp4`)

Worker: history-of-science Mini (Cursor HOS Local)  
Scope: ONE remint of plate 10 only · mint/splice only · do not score UAT · do not start Part 02 · do not ping Ben

## UAT FAIL inputs folded into this remint
From v13 (`hos_002_part01_rough_v13.mp4`):
- Plate 10 ~69–76s: **blue RECTANGULAR scrub/mask** around ore (reject)
- Orange embers cleared in v13, but blue mask is reject
- **Flask beside scale** is back in v13 — must remove
- KEEP: colourless shimmer only · motion MAD · Animistry side labels · ore IN brass pan

## Attempt
- Engine: Google Flow Veo UI · model `Veo 3.1 - Lite`
- Mode: I2V from clean start still (pre-scrub source; no blue rect baked in)
- Start: `07_Edit-Project/_qa_v14_plate10_prep/p10_start_v14_clean.jpg`
- Script: `07_Edit-Project/_remint_part01_plate10_v14_i2v.py`
- Log: `07_Edit-Project/logs/remint_part01_plate10_v14_i2v.log`
- Meta: `07_Edit-Project/part01_remint_plate10_v14_meta.json`

## Exact Flow credit / UI error
Banner (verbatim from Flow UI body + screenshot):

> You're out of Google Flow credits. You can wait until they refresh or upgrade to get more Google Flow credits now.

Additional I2V UI failure while credits empty:

> Flow never enabled Add to Prompt after start-frame upload

Screenshot:
`04_Generated-Clips/part01/_rejected_uat_v14_plate10/10_rock_not_fire_v14_i2v_fail.png`

## What was NOT done (on purpose)
- **No local scrub/mask fallback** — would reintroduce a visible blue rectangular processing artifact (the v13 reject).
- **No `hos_002_part01_rough_v14.mp4` export** — do not hand a cut that still shows a processing artifact.
- **No PASS declaration.**

## Handoff for Picture / CoS
Need Google Flow credits refresh or upgrade on the HOS Ultra account, then re-run ONE plate-10 I2V remint + splice to v14.

STOP for HOS UAT.
