# 010 price review v03

Gemini, 16 Oct 2026, J0365. Boards only. **No mint. No spend. No merge.**
v03 closes the one remaining reuse shortfall in v02 (`P5:14_bench_three_again`, 8.16 s needed vs 2.65 s unused in `P1:03_bench_three`), alternates `P4:04_supernova_test` as a window overlay so no two full-frame teach graphics sit back to back, and attaches the 15 Teach-on-Screen edit-overlay specs (`WHO`, `WHEN`, `DATA`+`SCALE`, `FACT`, `TIMELINE`). Parked for Chief.

Locked VO: Chief KEEP, desk #180 comment 6101773293. Timings match v01/v02. Film picture 510.44s with the closing breath.

## Readings

- Flow: **23740** credits at 2026-10-15T21:42:22Z (J0313, CDP :9222). Not re-read. No spend in this job.
- Vertex promo: **£71.02** at 2026-10-15T07:30:31Z. Usable **£70.02** after the £1 margin. Not re-read. **Not authorised** for 010.

## Totals

| | rows | Quality | Fast | code | edit-hold | reuse | Flow try-1 | Flow expected | Vertex try-1 | Vertex expected |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Part 01 | 15 | 10 | 5 | 0 | 0 | 0 | 1050 | 2690 | £14.24 | £36.46 |
| Part 02 | 13 | 11 | 0 | 2 | 0 | 0 | 1100 | 2849 | £10.88 | £28.99 |
| Part 03 | 12 | 8 | 1 | 2 | 1 | 0 | 810 | 2092 | £8.64 | £22.84 |
| Part 04 | 12 | 5 | 1 | 6 | 0 | 0 | 510 | 1315 | £5.12 | £13.30 |
| Part 05 | 21 | 13 | 4 | 3 | 0 | 1 | 1340 | 3447 | £15.84 | £40.77 |
| **Film** | **73** | **47** | **11** | **13** | **1** | **1** | **4810** | **12393** | **£54.72** | **£142.36** |

v01 was 72 rows: 48 Quality, 7 Fast, 13 code, 3 edit-hold, 1 reuse; Flow expected 12,572, Vertex expected £146.88.
v02 was 72 rows: 47 Quality, 10 Fast, 13 code, 1 edit-hold, 1 reuse; Flow expected 12,373, Vertex expected £147.99.
v03 is **73 rows**: 47 Quality, 11 Fast, 13 code, 1 edit-hold, 1 verified reuse; Flow try-1 **4810**, Flow expected **12393** (+20 cr over v02), Vertex expected £142.36.

## What changed from v02 → v03

1. **`P5:14_bench_three_again` (8.16 s) reuse shortfall closed (+10 try-1 / +20 expected Flow credits):**
   - In v02, `P5:14_bench_three_again` (`use_s: 8.16 s`) was marked `reuse` of `P1:03_bench_three` (0 cr).
   - `P1:03_bench_three` is an 8.00 s (7.90 s usable) Fast clip that already uses 5.25 s in Part 01, leaving **2.65 s** unused moving footage (shortfall **5.51 s**, and even a full 7.90 s clip is 0.26 s short of 8.16 s).
   - v03 splits the beat into `P5:14_bench_three_again` (**5.51 s** own Fast mint, overhead track across the workbench, 10 try-1 / 20 expected Flow credits) + `P5:14_bench_three_again_c1` (**2.65 s** £0 reuse of the unused `[5.25s..7.90s]` tail of `P1:03_bench_three`, **0.00 s shortfall**).
2. **Back-to-back code-graphic alternation in Part 04 (`P4:03` → `P4:04` → `P4:05`):**
   - Marks `P4:04_supernova_test` with `code_graphic_layout: window_overlay` (composited over moving plate in edit) so two full-frame teach graphics never sit back to back (`AGENTS.md` *Teach on screen* Gate 6).
3. **Teach on Screen edit-overlay specs attached (`teach_overlay`, £0 / 0 Flow):**
   - 3 `WHO` cards at first mention (`Walter Alvarez (born 1940) — geologist`, `Luis Alvarez (1911–1988) — physicist`, `Frank Asaro & Helen Michel (1927–2014 · born 1932) — chemists`).
   - 6 `WHEN` stamps and 5-step animated `TIMELINE` (`66 Ma` → `1970s Gubbio` → `Late 1970s Berkeley` → `June 1980 Science` → `Early 1990s Chicxulub`).
   - 5 `DATA` + `SCALE` moments (`1 cm clay · thin as a pencil`, `Two-clock comparison`, `Iridium spike · 30× normal`, `10 km asteroid · city scale`, `180 km crater · wider than southern England`).
   - 3 `FACT` cards (`3 IN 4 SPECIES GONE`, `NO PLUTONIUM-244`, `LIVING DINOSAURS`).

## Mint order

006 (0 Flow) > 007 (7,196) > 008 (5,605) > 009 tranche 1 (7,354) > (~12 Nov AI Ultra renewal: 009 tranche 2 5,180, then 010 12,393). Every row has `generation_authorized: false`.

## For the Chief

Parked for Chief: 010 plate boards v03 (+20 expected Flow credits to eliminate the 5.51 s reuse shortfall on `P5:14_bench_three_again`). v02 files remain in place if Chief prefers v02 unchanged. No mint, no spend.
