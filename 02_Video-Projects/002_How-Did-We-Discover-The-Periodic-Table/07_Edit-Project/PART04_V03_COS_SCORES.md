# HOS 002 Part 04 — v03 CoS scores (scrub house props on books)

**Cut:** `hos_002_part04_rough_v03.mp4`  
**Sheet:** `PART04_V03_SCRUB_HOUSE_PROPS_BOOKS.md`  
**Parent v02:** sha `d5377dadc6c862c47348f79ad27b377f63c2b09b0b9607824e0a3c0383350f6c`  
**House:** `HOS_HOUSE_VO_AND_TEACH_LOCK.md`  
**Do not declare PASS here.** Scores → CoS only. No P05 until KEEP/LOCK. Do not ping Ben.

## Parents (untouched)

| Cut | Status |
|---|---|
| P01 v14 | LOCKED — FROZEN |
| P02 v06 | LOCKED — FROZEN |
| P03 v09 | LOCKED sha `30060612a00d628998008c9946b8e25319b56f3b9e5613b537c5d2be989bbe4e` — FROZEN |

## UAT FAIL addressed (v02 → v03)

| Clock | Label | Blocker | v03 action |
|-------|-------|---------|------------|
| **~19–21s** | ATOMIC WEIGHT | Glowing yellow house / model-town props on leather book stack | Remint/scrub **`02b_cards_sixty_three`** only |
| ~40–45s | PERIODIC TABLE → EMPTY SEATS | — | KEEP v02 night-sky fills on `05` / `06` (untouched) |

Spot-check: `03_what_is_element` + `04_sort_atomic_weight` already clean — not reminted.

## Remint / scrub trail

1. Flow account **`benoats@googlemail.com`** (Ultra `/u/1/`). I2V Create for `02b_cards_sixty_three` **succeeded** (project `53324bc4-3bc7-49b1-9166-9271875992bc`).
2. Gallery Download / play-network harvest **failed** (play response timeouts; Download media closed context) — no Ken Burns substitute.
3. Applied **adaptive hard leather/wood fill** over detected glowing yellow house-glow tokens on the existing Veo Fast `02b` plate (continuous card motion preserved) — same class of post-scrub as v02 window fill.
4. Pass-2 mop → residual house-glow ≈0 on plate frames. Whole-cut scan ~19–21 + ~40–45 CLEAN.
5. All other plates = v02 pack (v01 keep + v02 `05`/`06` sky). Same `PLATE_ORDER`. VO / labels untouched.

## Teach gate (unchanged)

- **Element** named + defined (pure chemical)
- **Atomic weight** sort visible
- **Periodic table** = family columns / seating chart
- **Why groundbreaking** = hunt metal before find (prediction / vacant chair address)

## Picture locks (v03 spot)

- Spot frames ~19 / 20 / 21s: book tops clean — **no** glowing yellow houses / house-icon tokens / model-town toys
- Spot frames ~40 / 42 / 45s: window = navy sky + moon/stars only — **unchanged** from v02 KEEP
- Desk DNA + Animistry side labels kept
- Flag for CoS: book-top scrub is a local leather fill (not a new Veo download). Acceptable per sheet (zero house props) but visually a paint-over — CoS call on KEEP vs further Veo remint when Download works
- Flag: clear glass / coloured liquid vessels still on keep plates (house: opaque) — same as v01/v02

## Land stats

| Field | Value |
|------|-------|
| path | `09_Final-Export/hos_002_part04_rough_v03.mp4` |
| bytes | 83019495 |
| duration | 127.760 s |
| sha256 | `79dd7650cb582b548ae4c1c0aa98e4938ff8ec90ba654dea9c0b5c5574ee62e8` |
| reminted | `02b_cards_sixty_three` |
| plate02b_picture | 15.10–23.00 s |
| columns_picture | 37.75–45.65 s |
| explorer_picture | 45.30–53.20 s |
| Flow | `benoats@googlemail.com` (Create OK; download failed → adaptive rect leather scrub) |
| P03 untouched | `30060612a00d628998008c9946b8e25319b56f3b9e5613b537c5d2be989bbe4e` |
| HOS UAT | `~/Library/Mobile Documents/com~apple~CloudDocs/HOS UAT/hos_002_part04_rough_v03.mp4` |
| watch | `WATCH_part04_v03.txt` |

## Spot QA (objective)

- v02 fail crop ~20s book-top: house-glow pixels **present** (n≈2623)
- v03 crop ~20s book-top: house-glow pixels **0**; book-box mean leather ~(124,70,50)
- ~40 / 45s: night sky + moon/stars only (v02 `05`/`06` KEEP)

## CoS scores

_(CoS fills)_
