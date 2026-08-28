# CapCut / Broadcast — Orbit 001

## Watch this (polished)

`09_Final-Export/aliens_broadcast_v01.mp4` — **legacy layout** (generic space-heavy).

### Remaster v02 (in progress)

VO-locked mystery remaster: alien cities, megastructures, fleets, artifacts, glimpses.  
See `remaster_v02/VISUAL_REMASTER_v02.md` + `VO_LOCKED_SHOTLIST_v02.json`.  
Target export: `09_Final-Export/aliens_broadcast_v02.mp4`.

Layout (v01):
- Full-frame **B-roll** matched to each VO section (2–4 unique clips, no reuse)
- **Orbit PiP** bottom-right (~18% width) — expressions only, not full screen
- Smoothed VO master (`aliens_voiceover_master_smooth_v01.wav`)

EDL: `SECTION_EDL_v01.json` (v01) · remaster shotlist `remaster_v02/VO_LOCKED_SHOTLIST_v02.json`

## CapCut project

`Orbit - 001 Will We Ever Meet Aliens` — rebuilt to the same section EDL (B-roll + PiP track).  
If PiP scale looks off in CapCut, use the MP4 export as the source of truth and nudge Orbit in CapCut.

## Rebuild

```bash
cd ~/code/Orbit-YouTube/02_Video-Projects/001_Will-We-Ever-Meet-Aliens/07_Edit-Project
python3 _build_polished_broadcast.py
python3 _build_capcut_pip_draft.py
```

## Still later

- Real CapCut title/graphic cards
- Dedicated Orbit intro/thinking takes
- Optional VO regen if you want a less TTS cadence
