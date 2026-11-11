# HOS 011 — Chief Price Pass Review (`PRICE_REVIEW_v01.md`, `J2475`)

- **Film:** `011_Surgery-Before-Anaesthesia` (*Anesthesia: The Day Surgery Stopped Hurting*)
- **Slotted air date:** **Thu 10 Dec 2026** 18:00 UK (`2026-12-10T18:00:00.000Z`, `J2231`; ready for Ben's OK **Sun 6 Dec 2026**)
- **Queue position:** First in the HOS waiting line (`jobs/WIP.json` `next_hos`). Preparation only; no active production slot claimed and **0 credits / £0 spent**.
- **Locked VO:** `02_Voiceover/hos_011_vo_v01.wav` (`532.720 s` = `8:52.72`, `sha256: d873f1d0c9158087fd61ce0b9f53de985055d778cd58b8df70c67c0701300ae2`), `J2286` **KEEP** on all 5 chapters, `J2245` closed 10 Nov 2026.

## 1. Mint Cost Summary (71 Mint Rows + 22 Free Rows = 93 Total Rows)

| Part | Chapter title | Time (`in–out`) | Rows | Quality (`100`) | Fast (`10`) | Code graphic (`0`) | Free archive (`0`) | Reuse (`0`) | Mint rows | Free rows | Flow credits (try-1) | Flow credits (expected) | Vertex try-1 (£) | Vertex expected (£) |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Part 01 | The Fastest Knife | `0:00.00–1:26.80` | 18 | 10 | 6 | 2 | 0 | 0 | 16 | 2 | 1,060 | 2,710 | £19.84 | £49.08 |
| Part 02 | A Gas That Made People Laugh | `1:26.80–2:55.66` | 15 | 7 | 3 | 2 | 3 | 0 | 10 | 5 | 730 | 1,873 | £13.12 | £32.82 |
| Part 03 | This Is No Humbug | `2:55.66–4:31.88` | 15 | 11 | 2 | 1 | 1 | 0 | 13 | 2 | 1,120 | 2,889 | £18.88 | £48.10 |
| Part 04 | The Fight Over Who Was First | `4:31.88–6:06.26` | 17 | 6 | 6 | 3 | 2 | 0 | 12 | 5 | 660 | 1,674 | £13.44 | £32.52 |
| Part 05 | Across the Ocean | `6:06.26–8:55.30` | 28 | 14 | 6 | 4 | 3 | 1 | 20 | 8 | 1,460 | 3,746 | £26.24 | £65.64 |
| **Total** | **Full film (`8:55.30`)** | `0:00.00–8:55.30` | **93** | **48** | **23** | **12** | **9** | **1** | **71** | **22** | **5,030** | **12,892** | **£91.52** | **£228.16** |

## 2. Routing & Cost Notes for Chief's Price Pass

1. **Every minted row is `≤ 8.00 s` (`3.16 s – 7.70 s`):** Zero rows require a double-clip mint, so `71` mint rows = `71` Veo 3.1 clips (`48` Quality at `100` credits + `23` Fast at `10` credits = **`5,030` Flow credits try-1** / **`12,892` expected**).
2. **`23.7%` of rows (`22` of `93`) cost `0` credits / `£0`:** `12` house code graphics (4 chapter cards, 1 cream end card, 4 `DATA + SCALE` graphics, 2 teach diagrams), `9` verified public-domain primary-source archive composites, and `1` closing callback tail reuse.
3. **Strict `Fast` hygiene (`23` rows):** Every `veo-3.1-fast` row is a daylight or clean window-lit shot of surgical instruments, pocket watches, wooden benches, books, or monument stone with **zero candles, gas lamps, lanterns, or glowing filaments**.
4. **Both Shorts (`Short A` and `Short B`) cost `0` additional mint credits:** All 9:16 plates are centre-cropped from the long's Part 01–04 plates.
5. **Authorization gate:** Every row in `PICTURE_PLAN_v01.json` and `parts/part-01_plates_v01.json`..`part-05_plates_v01.json` carries `"generation_authorized": false`. Minting waits until HOS 011 enters active picture production and Chief flips `generation_authorized: true`.
