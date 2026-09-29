# HOS 004 full_v01 — final continuous music (UAT)

**Cut:** `hos_004_full_v01.mp4`  
**sha256:** `058e1ba7a4a986de0dec4fe1a6e0e6f47a47449ad314f979e8224a8a5ef1b4d5`  
**Duration:** 524.700 s · **A/V Δ:** 0.000 s · **Size:** 417941859 B  
**Status:** UAT for Ben music listen. Do **not** label KEEP until Ben says so. No upload.

## Locked inputs

- Picture: `hos_004_full_join_v03.mp4` (Ben PASS 29 Sep, sha `f88cb9d4…65244`)
- VO: part masters v04, untouched level, placed at v03 part starts
- Chapter cards + 4 s cream + 20 s hold unchanged

## Bed

- File: `05_Music/hos004-full_score_bed_v01.mp3`
- Prompt: warm curious documentary underscore (soft strings, light piano, gentle wonder)
- Requested 506000 ms; ElevenLabs returned **~390.8 s** — looped to cover through cream (~504.7 s)
- Mix: −20 dB relative to VO · sidechain duck · continues under chapter cards · fades across cream · silent under 20 s hold
- `amix=inputs=2:weights=1 1:normalize=0` + alimiter
- Delivery: 1920×1080 30 fps CFR (`orbit_cfr_delivery.remaster_cfr`)

## Levels (paste)

| Check | Value |
|---|---|
| `vo_check` mean / peak | **−23.6 / −3.8 dB** (peak ≤ −1 OK) |
| `ffmpeg -t 500.69` mean / max | **−23.4 / −3.8 dB** |

## vo_check word flags

Known KEEP-VO transcriber flags (same as v03):
- ~6:08 `a living` → `the living`
- ~6:33 `sort` → `sought`

Also heard on this pass (transcriber, not remaster):
- ~5:34 / ~6:31 `van den Broek` → `van der broek`
- ~7:40 `a weight` → `of weight`
- warns: Röntgen / Moseley spellings

## Captions (STEP 2)

`11_Upload-Package/Captions/hos_004_full_v01.en.srt` — script-locked words, whisper timings, ≤42 chars / ≤2 lines, no cues during cream/hold.

Builder: `07_Edit-Project/_mix_hos_004_full_v01_music.py` · captions `_build_hos_004_full_v01_captions.py`  
iCloud: `HOS UAT/004_Whats-Really-Inside-An-Atom/09_Final-Export/hos_004_full_v01.mp4`
