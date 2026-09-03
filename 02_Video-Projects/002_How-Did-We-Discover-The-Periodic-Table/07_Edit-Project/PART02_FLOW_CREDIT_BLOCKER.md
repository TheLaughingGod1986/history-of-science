# Part 02 Flow Ultra — credit / usage blocker

**Date:** 2026-09-04  
**Status:** BLOCKED on Google Flow Ultra credits (not a script bug)

## What happened

1. Part 01 PASS is locked. Part 02 VO + 11 plates + assemble script are ready.
2. Flow UI automation works (`flow.google.com`, Veo 3.1 Fast, scenery-only).
3. Create submits, then Flow returns:
   - "You've reached your usage limit. Please try again later."
   - "I've tried starting that video again, but it was declined because your credit limit has been reached."
4. Soft-retry / refresh cannot mint new plates without credits.
5. Gemini API fallback is unavailable — `GEMINI_API_KEY` / `GOOGLE_API_KEY` are empty in project `.env`.

## Salvage

Two already-rendered gallery clips were UI-downloaded into:

`04_Generated-Clips/part02/raw/_salvage_gallery_v01/ui_download_01.mp4`  
`04_Generated-Clips/part02/raw/_salvage_gallery_v01/ui_download_03.mp4`

(Likely duplicates of the same successful scenery take — not enough for an 11-plate rough.)

## Unblock options (Ben)

1. **Wait** for Google One AI Ultra Flow credits / daily usage to refresh, then re-run:
   ```bash
   cd "/Users/benjaminoats/YouTube/History Of Science"
   ORBIT_FLOW_PROFILE="$HOME/.playwright-hos-flow-profile" ORBIT_FLOW_HEADED=1 \
     /tmp/hos-flow-venv/bin/python -u \
     02_Video-Projects/002_How-Did-We-Discover-The-Periodic-Table/07_Edit-Project/_mint_part02_flow_v01.py
   ```
2. **Top up / confirm Ultra** subscription credits in Google One / Flow.
3. Optionally put a real `GEMINI_API_KEY` in `07_Edit-Project/.env` for API Veo lite fallback (not preferred; Flow-first rule).

## After credits return

1. Mint 11 plates → `_assemble_part02_rough_v01.py`
2. Copy rough **only** to iCloud `HOS UAT/`
3. **STOP for Ben UAT** — no Part 03 until PASS
