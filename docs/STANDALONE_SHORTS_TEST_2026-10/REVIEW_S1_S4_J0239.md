# HOS Standalone Shorts S1–S4 — Gates, Contact Sheets & Cover Previews (J0239)

Worker: `gemini` (`gemini-agy`), 15 October 2026. Prepared for J0172 (Chief's PASS before scheduling). No upload, schedule, re-render, or spend.

## 1. Shorts Open Gate (`gate_shorts_open.py check`)

```text
PASS  hos_sa_s1_herschel_infrared_v01.mp4  dur=22.43s  audio=-18.1dB  motion=11.94  dhash=532b2b7beb7b1b03
PASS  hos_sa_s2_brand_phosphorus_v01.mp4  dur=22.97s  audio=-18.0dB  motion=13.4  dhash=53572b8f0e0f1e03
PASS  hos_sa_s3_snow_pump_v02.mp4  dur=22.17s  audio=-18.8dB  motion=18.7  dhash=6c8a563231333373
PASS  hos_sa_s4_curie_notebooks_v04.mp4  dur=22.63s  audio=-18.0dB  motion=16.72  dhash=7c0f8db3b70f1168
```

## 2. Polish-Pass SFX Level Gate (`sfx_kit.py level`)

```text
s1_herschel_infrared: SFX level PASS: VO -20.8 LUFS, SFX -34.9 LUFS, 1 hits
s2_brand_phosphorus:  SFX level PASS: VO -20.0 LUFS, SFX -34.9 LUFS, 1 hits
s3_snow_pump:         SFX level PASS: VO -19.7 LUFS, SFX -34.9 LUFS, 1 hits
s4_curie_notebooks:   SFX level PASS: VO -19.6 LUFS, SFX -34.9 LUFS, 1 hits
```

## 3. Contact Sheets & Cover 168 px Previews (`thumb_preview.py short`)

All images are JPEG (< 600 KB each, under the 1.5 MB limit) and force-added to `review/standalone-s1-s4`:

### Contact Sheets (frame 0, 1.0s, 12× 2s marks `0.0s..22.0s`, and last frame)
- **S1 (`hos_sa_s1_herschel_infrared_v01.mp4`):** `docs/STANDALONE_SHORTS_TEST_2026-10/shorts_v01/hos_sa_s1_herschel_infrared_v01_contact_sheet.jpg`
- **S2 (`hos_sa_s2_brand_phosphorus_v01.mp4`):** `docs/STANDALONE_SHORTS_TEST_2026-10/shorts_v01/hos_sa_s2_brand_phosphorus_v01_contact_sheet.jpg`
- **S3 (`hos_sa_s3_snow_pump_v02.mp4`):** `docs/STANDALONE_SHORTS_TEST_2026-10/shorts_v01/hos_sa_s3_snow_pump_v02_contact_sheet.jpg`
- **S4 (`hos_sa_s4_curie_notebooks_v04.mp4`):** `docs/STANDALONE_SHORTS_TEST_2026-10/shorts_v01/hos_sa_s4_curie_notebooks_v04_contact_sheet.jpg`

### Cover Previews (`thumb_preview.py short` — 110×196 tile + 168×94 centre 16:9 crop, rendered at 2×)
- **S1 (`hos_sa_s1_cover_v01.png` — HEAT beyond RED):** `docs/STANDALONE_SHORTS_TEST_2026-10/covers_j0209_v01/hos_sa_s1_cover_v01_preview.jpg` (also `_phone.jpg`, `_style.jpg`)
- **S2 (`hos_sa_s2_cover_v01.png` — GLOW not GOLD):** `docs/STANDALONE_SHORTS_TEST_2026-10/covers_j0209_v01/hos_sa_s2_cover_v01_preview.jpg` (also `_phone.jpg`, `_style.jpg`)
- **S3 (`hos_sa_s3_cover_v01.png` — REMOVE the HANDLE):** `docs/STANDALONE_SHORTS_TEST_2026-10/covers_j0209_v01/hos_sa_s3_cover_v01_preview.jpg` (also `_phone.jpg`, `_style.jpg`)
- **S4 (`hos_sa_s4_cover_v01.png` — BOOKS behind LEAD):** `docs/STANDALONE_SHORTS_TEST_2026-10/covers_j0209_v01/hos_sa_s4_cover_v01_preview.jpg` (also `_phone.jpg`, `_style.jpg`)
- **Combined 4-cover preview sheet:** `docs/STANDALONE_SHORTS_TEST_2026-10/covers_j0209_v01/hos_sa_s1_s4_covers_preview.jpg`
