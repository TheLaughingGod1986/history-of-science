# HOS 011 — Chief Price Pass Review v02 (`PRICE_REVIEW_v02.md`, `J2475`)

- **Film:** `011_Surgery-Before-Anaesthesia` (*Anesthesia: The Day Surgery Stopped Hurting*)
- **Chief ruling addressed:** `history-of-science#180` comment `6786715647` (Grok, 11 Nov 2026 04:06Z).
- **Slotted air date:** **Thu 10 Dec 2026** 18:00 UK (`2026-12-10T18:00:00.000Z`, `J2231`; ready for Ben's OK **Sun 6 Dec 2026**)
- **Queue position:** First in the HOS waiting line (`jobs/WIP.json` `next_hos`). Preparation only; no active production slot claimed and **0 credits / £0 spent**.
- **Locked VO:** `02_Voiceover/hos_011_vo_v01.wav` (`532.720 s` = `8:52.72`, `sha256: d873f1d0c9158087fd61ce0b9f53de985055d778cd58b8df70c67c0701300ae2`), `J2286` **KEEP** on all 5 chapters, `J2245` closed 10 Nov 2026.

## 1. Mint Cost Summary (66 Mint Rows + 27 Free Rows = 93 Total Rows)

| Part | Chapter title | Time (`in–out`) | Rows | Quality (`100`) | Fast (`10`) | Code graphic (`0`) | Free archive (`0`) | Reuse (`0`) | Mint rows | Free rows | Flow credits (try-1) | Flow credits (expected) | Vertex try-1 (£) | Vertex expected (£) |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Part 01 | The Fastest Knife | `0:00.00–1:26.80` | 18 | 15 | 0 | 2 | 1 | 0 | 15 | 3 | 1,500 | 3,885 | £24.00 | £62.10 |
| Part 02 | A Gas That Made People Laugh | `1:26.80–2:55.66` | 15 | 10 | 0 | 2 | 3 | 0 | 10 | 5 | 1,000 | 2,590 | £16.00 | £41.40 |
| Part 03 | This Is No Humbug | `2:55.66–4:31.88` | 15 | 12 | 0 | 1 | 2 | 0 | 12 | 3 | 1,200 | 3,108 | £19.20 | £49.68 |
| Part 04 | The Fight Over Who Was First | `4:31.88–6:06.26` | 17 | 12 | 0 | 3 | 2 | 0 | 12 | 5 | 1,200 | 3,108 | £19.20 | £49.68 |
| Part 05 | Across the Ocean | `6:06.26–8:55.30` | 28 | 17 | 0 | 5 | 5 | 1 | 17 | 11 | 1,700 | 4,403 | £27.20 | £70.38 |
| **Total** | **Full film (`8:55.30`)** | `0:00.00–8:55.30` | **93** | **66** | **0** | **13** | **13** | **1** | **66** | **27** | **6,600** | **17,094** | **£105.60** | **£273.24** |

## 2. v01 → v02 Changes (Chief Ruling `#6786715647`)

1. **Point 1 — All 23 `mint_fast` rows eliminated (`0` Fast rows in `v02`):**
   - **5 `mint_fast` rows swapped to `£0` / `0`-credit free rows** (every single Fast row whose neighbours are moving 3D plates, preserving the zero back-to-back full-frame graphics lock and `HOS-2026-11-E2`): `P1:09b` (`free_archive` Paré 1585 surgical treatise), `P3:05b` (`free_archive` 1846 two-necked glass ether inhaler engraving), `P5:04a` (`free_archive` UCH London 21 Dec 1846 operation illustration), `P5:14a` (`free_archive` Victorian surgical ward & spray engraving), and `P5:16a` (`code_graphic` closing triptych `'1800: A GAS · 1844: A BAG · 1846: A GLOBE'`).
   - **18 `mint_fast` rows upgraded to `mint_quality` (`Veo 3.1 Quality`):** `P1:01b`, `P1:02a`, `P1:03b`, `P1:07b`, `P1:09a`, `P2:04b`, `P2:09a`, `P2:10a`, `P3:10a`, `P4:02b`, `P4:04b`, `P4:05a`, `P4:07a`, `P4:08a`, `P4:09a`, `P5:07b`, `P5:09a`, `P5:11b` (each is either inside the `0:00–0:30` `HOS-2026-11-E2` open or immediately adjacent to an existing `code_graphic` / `free_archive` row, so it must be a moving 3D plate).
   - **Savings vs upgrading all 23 to Quality:** Upgrading all 23 would cost `7,100` Flow credits try-1 (`18,389` expected); the 5 free swaps reduce `v02` to **`6,600` Flow credits try-1** (**`17,094` expected**), saving **500 try-1 / 1,295 expected Flow credits** (`£8.00` try-1 / `£20.70` expected on Vertex).
2. **Point 2 — All 36 named-person rows (+ 3 additional = 39 rows) reworded so `0` mint prompts name a real person:**
   - Every Flow prompt now describes the historical figure by age, period role, and historically verified appearance for that scene's year (e.g., 52-year-old tall clean-shaven Scottish surgeon with short greying side whiskers in 1846 London; 21-year-old clean-shaven Regency chemist in 1800 Bristol; 26-year-old clean-shaven Georgia country physician in 1842; 29-year-old Connecticut dentist in 1844; 27-year-old Boston dentist with dark parted hair and neat moustache in 1846; 68-year-old white-haired senior Boston surgeon in 1846; 37-year-old Boston physician and man of letters in 1846; 41-year-old spectacled Boston chemist in 1846; 36-year-old Scottish obstetrician with long wavy brown hair in 1847 Edinburgh; 40-year-old London physician with dark side whiskers in 1853).
   - Enforced by `FORBIDDEN_NAME_RE` in `_build_shot_list_v01.py` and logged row-by-row in `07_Edit-Project/PROMPT_AND_FAST_CHANGE_v02.json`.
3. **Authorization gate:** Every row in `PICTURE_PLAN_v02.json`, `PICTURE_PLAN_v01.json`, and `parts/part-01_plates_v01.json`..`part-05_plates_v01.json` carries `"generation_authorized": false`. Minting waits for Chief's price-pass sign-off.
