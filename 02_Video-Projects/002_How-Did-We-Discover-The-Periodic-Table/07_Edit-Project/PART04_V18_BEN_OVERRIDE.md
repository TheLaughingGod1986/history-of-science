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
| `06_explorer_leaves_gap` | Painted single-exposure · finished crown · profile/back · gold glasses rim · clean cards | `286c4c0244098ac283e428d7de8e46929e6540cc430ac19c226c1dad675799af` |
| `10_family_before_weight` | Painted single-exposure · sharp H/C/N/O · clean lamp · ONE soft Empty Chairs panel | `4496c73f9bba7157d50b685c2e427daba12d22b245d73ee7a646a76cb50ef13c` |
| `11_publish_gaps` | Painted single-exposure · opaque props · no crop-settle · mid-frame ghost QA | `9863fb4844151b95343e12301a1b2c410cfe051edf134f11e1be8f6574506c49` |
| `11b_wait_and_hunt` | Painted single-exposure · grid holes · mid-frame ghost QA | `dc119f7757938da2ae99e9a02a86d04dfcb1a60cea8086867256737f1b1fbcfa` |

Exact plate sha256 also in `part04_rough_v18_land_meta.json` / `part04_build_v18_painted_meta.json`.

### Engine notes (credit blockers → CoS)

1. **Gemini API Veo** (`veo-3.1-generate-preview` / lite / fast): `429 RESOURCE_EXHAUSTED` — prepaid credits depleted (`ai.studio` billing). Stopped; did not retry burn.
2. **Flow Ultra** (`benoats@googlemail.com`): create reached project `f98399b2-df65-41b0-821c-2c28844828d1` then stalled — Agent settings (tune) button not found; no accepted gallery mp4 this run. Prior v17 harvest also empty/MAD-heavy.
3. Therefore remint used **opaque per-frame painted continuous motion** from fresh procedural single-exposure v18 starts:
   - ONE soft Empty Chairs glow via mask-blur (no nested concentric rects)
   - No crop-settle (v17 crop+sharpen rang as ghost doubles for Ben)
   - No temporal-median · not v01 restore
   - Mid-plate frames extracted and self-checked before assemble

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
| sha256 | `b4ab99efa40a281bf59a325c443b2c28f29a3db4c5760b046cb290ba3f779fd3` |
| bytes | 73195893 |
| duration | 127.760 s |
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

### Edge-pair frac (lower = fewer parallel ghost edges; Ben fail publish ≈ 0.597)

See `part04_rough_v18_land_meta.json` → `edge_pair_frac`.

Note: cut `t≈121` sits inside the 11→11b xfade (0.35s) — edge-pair spikes there are expected from dissolve blend, not plate DNA. Prefer mid-plate stills (`t124.5`/`t125`/`t126`) for LATE SHOTS SHARP scoring.

## Residual risk

Plates are sharp painted continuous-motion fallback (more graphic than Flow Veo). Prefer Flow/Veo when credits + harvest work. Style jump vs earlier Veo plates possible. Do **not** PASS from this agent.

## Next

Merge only after UAT PASS + Ben KEEP. Scores → CoS. No Ben ping.

Flow account for follow-up I2V: `benoats@googlemail.com`.
