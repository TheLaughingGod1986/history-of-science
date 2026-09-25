# HOS 002 Part 04 — v06 CoS scores (desk-only 02b)

**Cut:** `hos_002_part04_rough_v06.mp4`  
**Sheet:** `PART04_V06_DESK_ONLY_02B.md`  
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
| **~18–21s** | ATOMIC WEIGHT | In-camera peaked roofs + chimneys through 02b window | **FULL Veo 3.1 Fast remint** of `02b_cards_sixty_three` only — **DESK-ONLY** (no window in frame) · **no hard fills** |
| ~91–97s | A BET | — | KEEP v04 cleared `09` / `09b` |
| ~38–44s / ~40 | PERIODIC TABLE | — | KEEP v02 `05` / `06` night-sky |
| ~49 | EMPTY SEATS | — | KEEP Explorer teal |
| Brown scrub | books | CLEARED on v05 | KEEP — do not regress |

## Remint / method trail

1. Flow account **`benoats@googlemail.com`** (Ultra `/u/1/`). Credits ULTRA.
2. Prompt lock: **DESK-ONLY** tight crop — cream cards, leather books, lamp, vessels. **NO WINDOW / panes / night sky / outdoor / roofs / chimneys / town.** Soft dark wood interior BG only.
3. **No hard fills / brown panels / flat sky rectangles** used.
4. Still-check full plate + visual review of stills.

| Create | Project | Result |
|--------|---------|--------|
| **1** | `https://flow.google.com/u/1/project/20dadd65-c532-4fbf-9928-82c658b0e03e` | Harvest OK · **ACCEPT** — tight desk, wood-panel BG, no window/roofs readable on stills t0–t7 |
| **2** | `https://flow.google.com/u/1/project/49213d26-9e7a-43f6-904d-11d0c996c64d` | Harvest OK · **REJECT** — curved window frame readable on right edge (mint process died mid-wait; accidental resubmit) |
| **3** | `https://flow.google.com/u/1/project/e1531365-457e-4b7e-b38b-e03bdefa9fdd` | Harvest OK · **REJECT** — window-edge tell (second crash resubmit; over sheet max-2; not used) |

5. Accepted Create **1** only. Creates 2–3 rejected after visual still-check. No hard-fill.

## Land stats

| Field | Value |
|------|-------|
| path | `09_Final-Export/hos_002_part04_rough_v06.mp4` |
| bytes | **76818977** |
| duration | **127.760 s** |
| sha256 | `5aea09bdc505beb4d887acdfcfc5c43b307ee0bb7c606bb287b4beeb56e5bbf2` |
| reminted | `02b_cards_sixty_three` only |
| method | Veo 3.1 Fast T2V desk-only — **no hard fill** |
| tries | **1 accepted** (Create 1). Creates 2–3 crash-resubmits rejected |
| Flow | `benoats@googlemail.com` |
| P03 untouched | `30060612a00d628998008c9946b8e25319b56f3b9e5613b537c5d2be989bbe4e` |
| window ~18–21 | **none readable** on accepted plate / assembled spot stills (desk + wood interior) |
| KEEP confirm | late window · night-sky ~40 · Explorer teal ~49 · Empty Chairs · brown scrub cleared |

## Spot QA (objective)

- ~18–21 (02b): continuous desk — cream cards in motion, leather books, lamp, vessels; wood interior BG; **no window panes / night sky / roofs / town**.
- Brown panel: not reintroduced (books continuous).
- KEEP night-sky ~40 present (v02 plates untouched).
- KEEP Explorer teal ~49 present.
- KEEP late window 09/09b from v04 untouched.
- No hard-fill heal applied.

## Evidence paths

- Accepted plate: `04_Generated-Clips/part04/raw/v06_fast/02b_cards_sixty_three_v06.mp4`
- Rejected: `04_Generated-Clips/part04/raw/v06_fast/_rejected/`
- Still-checks: `07_Edit-Project/_qa_part04_v06_plate/` · `_qa_part04_v06_spot/`
- Mint meta: `07_Edit-Project/part04_mint_flow_v06_meta.json`
- Land meta: `07_Edit-Project/part04_rough_v06_land_meta.json`
- iCloud HOS UAT: `hos_002_part04_rough_v06.mp4` + `WATCH_part04_v06.txt`

## CoS scores

_(CoS fills)_

**Agent note for CoS:** Desk-only Create 1 clears the roof-through-window FAIL without hard fills. Creates 2–3 were accidental resubmits after mint wait-loop process death; both show window-edge tells and were rejected. Do **not** declare PASS. Do **not** ping Ben.
