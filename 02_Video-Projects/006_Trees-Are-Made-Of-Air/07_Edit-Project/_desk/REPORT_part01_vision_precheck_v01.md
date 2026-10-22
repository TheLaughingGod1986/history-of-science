# HOS 006 Part 01 · local vision precheck pilot v01

- **When:** 2026-10-04 00:19:11 BST
- **Model:** `mlx-community/Qwen2.5-VL-3B-Instruct-4bit`
- **Install footprint:** venv 0.78 GB + model 3.02 GB = **3.79 GB** (<20 GB)
- **Rough:** `/Users/benjaminoats/YouTube/hos-006-trees/02_Video-Projects/006_Trees-Are-Made-Of-Air/07_Edit-Project/_precheck/hos_006_part01_precheck_rough_v01.mp4`
  - sha256 `25fb1f20a9b547044e309df7000f0d3fadbe3420679512a104e40da5b47b4e47`
  - duration **61.05 s**, size 75.9 MB
- **Runtime:** wall 18.9s · VL load 0.0s · VL calls 0
- **Peak RSS (VL process):** **573 MB**

## Scope
Advisory only — never a gate. Part 01 KEEP plates already accepted (12/12). Local Mini only; no cloud vision.

## Flags on KEEP rough
_None._

## Positive controls (known-bad takes)
### `04_years_pass_t1`
- **freeze** @ 0.20s — ffmpeg freeze 0.54s
### `08_wood_food_air_t2`
- _No flags raised._
### `12_garden_sky_t1`
- _No flags raised._

## Scoring vs mint review notes
- **Hits:** 1
  - HIT `04_years_pass_t1` expect=freeze — first 0.54s freeze
- **Misses:** 2
  - MISS `08_wood_food_air_t2` expect=other — campfire flame
  - MISS `12_garden_sky_t1` expect=other — smoke/clouds at pot height
- **False alarms (on KEEP rough):** 0

## Recommendation
**Keep as standing pre-UAT advisory step** on the Mini overnight (outside Tdarr 01:00–05:00). 3B caught 1 known issue(s) with 0 false alarm(s) on the KEEP rough. Do not gate ship on it; human/UAT remains the sign-off. Note: 2 known-bad miss(es) — useful as a net, not a sieve.

## Method notes
- Freeze: ffmpeg `freezedetect` (n=0.003, d=0.5s) then VL confirm on mid-freeze still.
- Repeat: phash every 1.0s; flag if Hamming distance ≤ 6 and |Δt| ≥ 8s.
- Garbled text: VL OCR on mid-plate stills that have board `side_label`.
- Bad controls run the same detectors on raw known-bad takes.
