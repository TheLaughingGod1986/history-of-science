# HOS 004 full join v03 — restore mix level (UAT)

**Cut:** `hos_004_full_join_v03.mp4`  
**sha256:** `f88cb9d47e910425519a40a6af7649626c47afbcdddf1f0f3293564c59f65244`  
**Duration:** 524.700 s (8:44.70) · **Size:** 381929742 B  
**A/V delta:** `0.000` s  
**Status:** UAT for Ben. Do **not** label KEEP/LOCKED. Do **not** upload.

Same picture, chapter cards, seams and end as override v02. **Only** change: part mix uses `amix=inputs=2:weights=1 1:normalize=0` (v02 omitted `normalize=0`, so ffmpeg halved VO+bed ≈ −6 dB).

## Levels

| Measure | Value |
|---|---|
| Full `vo_check` mean / peak | **−23.7 dB** / **−3.7 dB** (peak ≤ −1 OK) |
| Film only `ffmpeg -t 500.69` mean / max | **−23.5 dB** / **−3.7 dB** (matches parts ~−22…−24) |

## vo_check word flags (full audio)

```
FAIL  hos_004_full_join_v03_audio.wav  8:44.70  mean -23.7 dB  peak -3.7 dB  147 wpm
   FAIL  replace at ~6:07.34: a living → the living
   FAIL  replace at ~6:31.88: sort → sought
   warn  silence 21.0s at 8:23.70
   warn  cambridge jj / rontgen / moseley (transcriber)
```

v02’s ~3:59.50 `wrong`→`rock` is **gone** on v03 (louder mix).

## “wrong” window (Ben 3:55–4:03)

That 8 s cut ends on “pudding”; “It was also wrong” lands ~**4:05.64** (full) / ~**83.25 s** into Part 03 rough.  
STT on a wider span: **both** v03 and `hos_004_part03_rough_v01.mp4` hear **“wrong”** (not “rock”).

Builder: `07_Edit-Project/_join_hos_004_full_v03.py`  
iCloud: `HOS UAT/004_Whats-Really-Inside-An-Atom/09_Final-Export/hos_004_full_join_v03.mp4`
