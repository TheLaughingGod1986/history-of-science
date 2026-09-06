# Part 03 status — A Ruler for Atoms

**Updated:** 4 Sep 2026 evening (after CoS Part 01 v11 watch notes)

## Locked keepers (do not remint)

| Cut | Status |
|---|---|
| `hos_002_part01_rough_v11.mp4` | **HOLD / locked.** Plate 10: clear flask gone; ore IN brass pan; shimmer only; no floating glass. |
| `hos_002_part02_rough_v06.mp4` | **PASS locked.** Do not UAT again unless Ben reopens. |

## CoS gate for Part 03 (from Part 01 v11 + Part 02 v06)

**KEEP:** 3D cartoon / Animistry · British VO · classical bed · Explorer once.

**FAIL — must not repeat:**

1. Heavy Ken Burns (stills + pans/zooms ~0:07, 0:45, 0:53, 1:08, 1:16, 1:23)
2. Animistry side labels missing (need side labels when VO names terms — not center stamps)
3. Continuity style jarring (real motion ↔ still-push cuts)

**Part 03 hard:** all real Veo motion every beat · side labels burned in assemble · Explorer once · one set language.

Canonical: `COS_LOCK_002.md` · `FILM002_QUALITY_GATE_FROM_PART02.md`

## Ready on disk

- Script + VO (~89.7s) + 12-plate board (`parts/part-03_plates_v01.json`)
- Mint: `_mint_part03_gemini_v01.py` (API) · `_mint_part03_flow_v01.py` (Flow UI)
- Assemble: `_assemble_part03_rough_v01.py` (upper-right side labels → HOS UAT)
- Flow UI helper updated for `flow.google.com` Agent settings → **Veo 3.1 - Fast**

## Blocker (now) — not shipping Ken Burns

1. **Gemini API:** prepaid credits depleted (`429 RESOURCE_EXHAUSTED` / prepayment).
2. **Flow UI (benoats86@gmail.com):** Agent Create path locks Veo 3.1 - Fast in settings, but generations fail with *“Failed to render response” / agent failed* (not charged). UI shows ~10 Flow credits; agent path still cannot mint usable landscape Veo. One harvest pulled a **Threads/Instagram portrait** CDN clip — **quarantined** under `04_Generated-Clips/part03/raw/_rejected_wrong_source/` (download filter now rejects those CDNs).

## When credits / Flow agent recover

1. Prefer Flow Veo 3.1 Fast via `_mint_part03_flow_v01.py` (or Gemini API if prepaid refilled).
2. QA: landscape 16:9 · continuous motion · no Ken Burns · Explorer once on plate 05.
3. Assemble → `HOS UAT` → report land. **Do not ping Ben.**

## Do not

- Remint Part 01 / 02
- Ship Ken Burns / freeze-pad as the Part 03 look
- Ping Ben
- Start Part 04 before Part 03 PASS
