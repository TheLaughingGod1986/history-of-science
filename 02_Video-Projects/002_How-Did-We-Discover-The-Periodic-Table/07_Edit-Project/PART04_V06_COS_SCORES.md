# HOS 002 Part 04 — v06 CoS scores (scrub 02b window roofs) — **STOP**

**Cut:** `hos_002_part04_rough_v06.mp4` — **NOT LANDED**  
**Sheet:** `PART04_V06_SCRUB_02B_WINDOW_ROOFS.md`  
**Parent v05:** sha `a7c9741c32f9689c019d5c8695b36a8e8d2bbbebfb19b93ee53b6d584b8a43fc` · 76043650 B · 127.760s  
**Do not declare PASS here.** Scores → CoS only. No P05 until KEEP/LOCK. Do not ping Ben.

## Parents (untouched)

| Cut | Status |
|---|---|
| P01 | LOCKED — FROZEN |
| P02 | LOCKED — FROZEN |
| P03 v09 | LOCKED sha `30060612a00d628998008c9946b8e25319b56f3b9e5613b537c5d2be989bbe4e` — FROZEN |

## UAT FAIL addressed (v05 → v06)

| Clock | Label | Blocker | v06 action |
|-------|-------|---------|------------|
| **~18–21s** | ATOMIC WEIGHT | In-camera peaked roofs + chimneys through 02b window | **FULL Veo 3.1 Fast remint** of `02b_cards_sixty_three` only — **no hard fills** |
| ~91–97s | A BET | — | KEEP v04 cleared `09` / `09b` |
| ~38–44s / ~40 | PERIODIC TABLE | — | KEEP v02 `05` / `06` night-sky |
| ~49 | EMPTY SEATS | — | KEEP Explorer teal |
| Brown scrub | books | CLEARED on v05 | KEEP — do not regress |

## Remint / method trail — **STOP after 2 Creates**

1. Flow account **`benoats@googlemail.com`** (Ultra `/u/1/`). Credits ULTRA throughout.
2. Prompt lock (in every Create): window = night sky + moon + clouds + stars ONLY; **NO** buildings / houses / peaked roofs / chimneys / town silhouette / skyline.
3. **No hard fills / brown panels / flat sky rectangles** used.
4. Still-check every second ~0–8 of plate; visual review + heuristic.

| Create | Project | Result |
|--------|---------|--------|
| **1** | `https://flow.google.com/u/1/project/ea1943c7-80f4-4800-9702-fa9858fefc0f` | Harvest OK · **REJECT** — peaked roofs + chimneys readable on stills t0–t7 → `_rejected/02b_cards_sixty_three_v06_try1_roofs.mp4` |
| **2** | `https://flow.google.com/u/1/project/46215d4f-a524-473d-992f-b62a340050b0` | Harvest OK · stronger sky-first prompt · **REJECT** — town/roof/chimney silhouette still readable on stills t0–t8 → `_rejected/02b_cards_sixty_three_v06_try2_roofs.mp4` |

5. Sheet gate: **max 2 Creates** → still roofs → **STOP**. Do not hard-fill. Do not assemble v06 rough.

## Land stats

| Field | Value |
|------|-------|
| path | — **not exported** (STOP) |
| bytes | — |
| duration | — |
| sha256 | — |
| reminted | attempted `02b_cards_sixty_three` only · **0 accepted** |
| method | Veo 3.1 Fast T2V — **no hard fill** |
| tries | **2** (both roofs) |
| Flow | `benoats@googlemail.com` |
| P03 untouched | `30060612a00d628998008c9946b8e25319b56f3b9e5613b537c5d2be989bbe4e` |
| roof n≈0 ~18–21 | **FAIL** — roofs readable on both Creates |
| KEEP confirm | Parent v05 KEEP zones untouched (no assemble) · brown scrub KEEP on parent |

## Spot QA (objective — Create stills)

- Create 1 / Create 2 plate stills: night sky + moon + clouds + stars present, **AND** dark town/roof/chimney silhouette still readable along lower panes.
- Brown panel: not reintroduced on either try (books / cards continuous).
- No hard-fill heal applied (forbidden by sheet).

## Evidence paths

- Rejected plates: `04_Generated-Clips/part04/raw/v06_fast/_rejected/`
- Still-checks: `07_Edit-Project/_qa_part04_v06_plate/`
- Mint meta: `07_Edit-Project/part04_mint_flow_v06_meta.json`
- Parent remains watch file: `hos_002_part04_rough_v05.mp4` + `WATCH_part04_v05.txt`

## CoS scores

_(CoS fills)_

**Agent note for CoS:** Veo Fast T2V is baking in-camera town silhouettes into 02b despite explicit sky-only negatives (2/2). Sheet forbids hard fills. Options for CoS only: (a) authorize Create budget beyond 2, (b) authorize a different gen path CoS names, (c) hold on v05 with known window-roof FAIL until a clean Veo take lands. Do **not** declare PASS. Do **not** ping Ben.
