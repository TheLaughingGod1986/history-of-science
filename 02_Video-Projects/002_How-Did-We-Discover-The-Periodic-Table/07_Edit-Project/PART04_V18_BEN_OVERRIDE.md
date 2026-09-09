# PART04 v18 — Ben OVERRIDE FAIL remint

**Status:** LANDED FOR UAT — do **not** declare PASS · scores → CoS · no Ben ping

## Why

UAT PASSed `hos_002_part04_rough_v17` sha `e4cc41d8cf050f6726e6b3d5cbbbff10285656c588f3a758b4a29e1ec1f998fd`.
**Ben REJECTED with stills** — CoS overrides PASS.

### Ben FAIL stills

1. `ben_fail_publish_ghost.png` — PUBLISH desk: horizontal ghost doubles (lamp, flasks, grid, magnifier, cards)
2. `ben_fail_explorer_face.png` — Explorer: face-cloud blot, black hole dots in hair, garbled cards, stepped lamp
3. `ben_fail_family_cards.png` + `ben_fail_family_lamp.png` — FAMILY FIRST: lamp jagged/blown, soft panel double edge
4. `ben_fail_player_chair.png` — empty-chair soft panel reference (ignore QuickTime chrome)

## Parent FAIL

| Field | Value |
|---|---|
| Cut | `hos_002_part04_rough_v17.mp4` |
| sha256 | `e4cc41d8cf050f6726e6b3d5cbbbff10285656c588f3a758b4a29e1ec1f998fd` |
| duration | 127.760 s |
| Bible main | `25bdefd` |

## CLEARED — not reminted

- Written cards ~40 KEEP
- CLEAN LIGHT `09` / `09b` KEEP (unless later FAIL)

## Reminted plates

| Plate | Method | sha256 |
|---|---|---|
| `06_explorer_leaves_gap` | Painted single-exposure · finished crown · profile/back · gold glasses rim · clean cards | `d0cff4a1aa1d3afeda35e7a91561673f0de818cbda6d35f2436302934b1f00de` |
| `10_family_before_weight` | Painted single-exposure · sharp H/C/N/O · clean lamp · ONE soft Empty Chairs panel | `d40a2cb1a9002731f67f22da9da82a6d2eff523ab52f0cdc05d1daa2f1916905` |
| `11_publish_gaps` | Painted single-exposure · opaque props · no crop-settle · no grain · mid-frame ghost QA | `3ea3401a357b00150976ea5ffbb6fc39bf17c506d3debe69ad0ec09f9816b600` |
| `11b_wait_and_hunt` | Painted single-exposure · grid holes · mid-frame ghost QA | `2cf249a0954d8ce8e161d84230f8d4734ae03f198126b6ed7fb45f9816e2390b` |

Exact plate sha256 also in `part04_rough_v18_land_meta.json` / `part04_build_v18_painted_meta.json`.

### Engine notes (credit blockers → CoS)

1. **Gemini API Veo** (`veo-3.1-generate-preview` / lite / fast): `429 RESOURCE_EXHAUSTED` — prepaid credits depleted (`ai.studio` billing). Stopped; did not retry burn.
2. **Flow Ultra** (`benoats@googlemail.com`): create reached project then stalled (Agent settings / harvest empty). No accepted gallery mp4 this run.
3. Therefore remint used **opaque per-frame painted continuous motion** from fresh procedural single-exposure v18 starts (harden pass after first land):
   - ONE soft Empty Chairs glow via heavy mask-blur (no nested concentric rects)
   - No crop-settle · no grain blend · no sharpen on publish/family/explorer
   - Card stacks vertical-only (horizontal card offsets read as Ben doubles)
   - Opaque flask / magnifier / mortar (no translucent nested outlines)
   - Mid-plate frames extracted (≥3) and self-checked before assemble

## HARD locks enforced

1. LATE SHOTS SHARP: one lamp, one flask set, one grid — reject horizontal ghost/double
2. Explorer: finished wavy crown; no face blot; no scalp black holes; readable cards
3. Clean warm lamp — no lava, no blown jagged white patches
4. Soft Empty Chairs panel = single soft rectangle (mask-blur), not double edge
5. Extract ≥3 mid-plate frames per reminted plate before assemble

## Landed cut

| Field | Value |
|---|---|
| Cut | `hos_002_part04_rough_v18.mp4` |
| Final-Export | `09_Final-Export/hos_002_part04_rough_v18.mp4` |
| HOS UAT (iCloud) | `HOS UAT/hos_002_part04_rough_v18.mp4` |
| sha256 | `05fb0a2b34dba1a8347ab74b2abc987fd406bef356b82b55f1a0e8ddb88cc6b5` |
| bytes | 71888783 |
| duration | 127.76 s |
| Watch | `WATCH_part04_v18.txt` |
| Land meta | `part04_rough_v18_land_meta.json` |

## Timeline map (SIDE_LABELS)

| Window | Side label | Picture plates |
|---|---|---|
| ~45–53 | EMPTY SEATS / EKA-ALUMINIUM | `06` remint |
| ~101–118.5 | FAMILY FIRST | `09b` KEEP · `10` remint |
| ~119–127.5 | PUBLISH THE GAPS | `11` · `11b` remint |

## QA stills

`07_Edit-Project/_qa_part04_v18_cut/cut_t{48,51,105,110,117,121,124.5,125,126}.jpg`

Also mid-plate: `_qa_part04_v18_final_mid/` (≥3 frames per reminted plate).

Note: cut `t≈121` sits inside the 11→11b xfade (0.35s) — dissolve blend can look soft there. Prefer mid-plate stills (`t2`/`t4`/`t6` of plate mp4s) and cut `t124.5`/`t125`/`t126` for LATE SHOTS SHARP scoring.

## Residual risk

Plates are sharp painted continuous-motion fallback (more graphic than Flow Veo). Prefer Flow/Veo when credits + harvest work. Style jump vs earlier Veo plates possible. Do **not** PASS from this agent.

## Next

Merge only after UAT PASS + Ben KEEP. Scores → CoS. No Ben ping.

Flow account for follow-up I2V: `benoats@googlemail.com`.
