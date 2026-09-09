# PART04 v17 — PUBLISH THE GAPS sharp remint

**Status:** LANDED FOR UAT — do **not** declare PASS · scores → CoS · no Ben ping

## Parent KEEP

| Field | Value |
|---|---|
| Cut | `hos_002_part04_rough_v16.mp4` |
| sha256 | `7e083fc440879209bbc69459fbaf21dc29dbfc1f77b370ec92ee931bec82cb3c` |
| duration | 127.760 s |
| Bible main | `25bdefd` |
| Single blocker | LATE SHOTS SHARP — PUBLISH THE GAPS ~120–126 still ghost doubles |

## UAT HARD FAIL stills (parent)

- PUBLISH THE GAPS ~121: full-scene ghost doubles (`fail_t121`)
- PUBLISH ~125: grid/flask/lamp ghost doubles (`fail_t125`)

## CLEARED — not reminted

- plate `10_family_before_weight` KEEP (keep_t110 — H/C/N/O sharp)
- Explorer `06` crown+glasses KEEP
- CLEAN LIGHT `09` / `09b` ~105 KEEP
- Written cards ~40 KEEP

## Reminted plates

| Plate | Method | Notes |
|---|---|---|
| `11_publish_gaps` | Fresh painted sharp continuous motion from procedural single-exposure start | NOT v01 restore · NOT temporal-median |
| `11b_wait_and_hunt` | Fresh painted sharp continuous motion from procedural single-exposure start | NOT v01 restore · NOT temporal-median |

### Engine notes

1. Flow Ultra (`benoats@googlemail.com`) create started (projects `8b761966-…`, `7aed7e87-…`). Gallery harvest still broken (play response timeout). Edit-download salvage returned an 8s mp4, but frame-diff MAD ~23–26 (heavy Veo motion) vs plate-10 KEEP MAD ~4–5 — rejected for motion-ghost risk.
2. Gemini API Veo: current Python 3.14 env missing `google.genai`; prior prepaid path was `429 RESOURCE_EXHAUSTED` on v16. No usable Gemini clip this run.
3. Therefore publish remint used: **opaque per-frame painted continuous motion** from fresh sharp starts (same class of fallback that cleared plate 10 in v16) — explicitly **not** restoring ghosty `v01` DNA and **not** temporal-median deghost.
4. Later Flow harvest for `11b` only (project `f4df706a-…`, sha `5c0da6e9…`) is archived as `11b_wait_and_hunt_v17.FLOW_TRY_5c0da6e9.mp4`. **Not swapped into rough_v17** — CoS should score mid-plate stills first; wrong burned `FAMILY FIRST` label on that clip vs SIDE_LABELS PUBLISH; ghost risk not cleared. Canonical dest stays painted `315394ce…`.

## HARD locks enforced

1. LATE SHOTS SHARP: one solid lamp, one solid flask set, one solid grid — reject ghost doubles / double-exposure
2. No left-half pixel mush
3. Soft rectangular Empty Chairs glow kept; clean warm lamp; no lava
4. Do **not** remint plate 10

## Landed cut

| Field | Value |
|---|---|
| Cut | `hos_002_part04_rough_v17.mp4` |
| Final-Export | `09_Final-Export/hos_002_part04_rough_v17.mp4` |
| HOS UAT (iCloud) | `HOS UAT/hos_002_part04_rough_v17.mp4` |
| sha256 | `e4cc41d8cf050f6726e6b3d5cbbbff10285656c588f3a758b4a29e1ec1f998fd` |
| bytes | 79090423 |
| duration | 127.760 s |
| Watch | `WATCH_part04_v17.txt` |
| Land meta | `part04_rough_v17_land_meta.json` |

## Plate sha256

| Plate | sha256 |
|---|---|
| `11_publish_gaps` | `6e2b0e821ec53291db03c54c4e55adc678ac549fa3f651bb0e705b26f2f43b1f` |
| `11b_wait_and_hunt` | `315394ce2d8944eff6e457d1166da57959bd125f7d5744923b30ae57e3d62569` |
| `10_family_before_weight` (KEEP) | `6ee17990e49aede89b166b84ee306b04cd2b6e134cee902c1a1bf8a08330fe1a` |
| `06_explorer_leaves_gap` (KEEP) | `f294b87b2387c2a10d7aa343db349e10e0fd5576c82a767d08f8fa211e4920c3` |

## Timeline map (SIDE_LABELS)

| Window | Side label | Picture plates |
|---|---|---|
| ~101–118.5 | FAMILY FIRST | `09b` KEEP · `10` KEEP |
| ~119–127.5 | PUBLISH THE GAPS | `11` · `11b` remint |

Fail spots: ~121/~125 → plates `11`/`11b` (note ~121 sits near 11→11b xfade).

## QA stills

`07_Edit-Project/_qa_part04_v17_cut/cut_t{105,110,117,121,124.5,125,126}.jpg`

- ~105 CLEAN LIGHT KEEP
- ~110 family KEEP (H/C/N/O sharp)
- ~121 / ~125 publish desks single-exposure (edge-doubling peak 0.50 / 0.47 vs fail125 0.90)

## Residual risk

Publish plates are sharp painted continuous-motion fallback (style more graphic than Flow Veo). Flow harvest + Gemini env/prepaid blocked preferred Veo path. Do **not** PASS from this agent.

## Next

Merge only after UAT PASS + Ben KEEP. Scores → CoS. No Ben ping.

Flow account for any follow-up I2V: `benoats@googlemail.com`.
