# J1218 — HOS 008 diagnostic rough v03

**Worker:** cursor. **No Ben Ready-for-OK.** Park for elected-Chief graphics/composite review.

## Master

| Field | Value |
|---|---|
| Version | `rough_v03` (v01 + v02 preserved) |
| Duration | **540.02 s** container (pause-trim −17.792 s from 557.81 s) |
| SHA256 | `0da87a8272ad5849abccf5d86acbf352cedf30d3189ef9ac8127efd24fc2934d` |
| WORK | `/Volumes/data/mac-mini-archive/tmp-render-scratch/j1218-hos008-rough-v03/full_join_v03/` |
| Desk | `07_Edit-Project/_desk/008/rough_v03/` |
| NAS | `/Volumes/data/mac-mini-archive/YouTube/History Of Science/02_Video-Projects/008_Lightning-Franklin/07_Edit-Project/rough_v03/` |
| Assembler | `_assemble_rough_v03.py` |
| Graphics | `code_graphics_v02` (£0; J1193 ten-FIX + P5:11 KEEP) |
| PR | https://github.com/TheLaughingGod1986/history-of-science/pull/379 |

## Chief FIX items addressed (29–30 Oct rulings)

1. **Teach MOTION:** P5 `10_metal_easy` is cleaned alpha over KEEP `06_rod_fitting` (between full-frame `09_wood_vs_metal` and `11_safe_path`).
2. **NAS safety:** fresh WORK/run dirs; no unlink/rmtree of prior NAS deliverables; local `/tmp` mux then rsync.
3. **Contact-sheet labels:** mid-interval sampled master time (not stale `film_t`).
4. **P4 `06_same_thing`:** sequential full-frame moving plates (no split); CG label from graphics v02.
5. **J1193:** ten FIX rows rebuilt in `code_graphics_v02`; Bellin coords corrected as **UNVERIFIED PROPOSALS** (`CODE_GRAPHICS_v01_REVIEW_SOURCE_CORRECTION.md`). Formal graphics PASS still Chief.
6. **Runtime ≤9:00:** 540.02 s; VO wording locked; no music generation.

## Automated gates (full join)

| Gate | Result |
|---|---|
| picture_qa | **PASS** — 0 FAIL / 6 low-detail WARN |
| polish_gate | **PASS** — 0 FAIL / 6 WARN |
| music_gate | **SKIPPED_NO_BED** — NOT PASS (credit hold / Chief OK) |
| episode gate | see `episode_gate_rough_v03.txt` (this pack) |

## Six WARN rows (picture_qa)

| t | Row | Note |
|---|---|---|
| 1:19 | `13_ring_the_bells_c1` | soft rain/steeple plate |
| 4:28 | `15_wet_dry` | code graphic |
| 4:51 | `19_kite_climb` | moving plate |
| 5:46 | `06_same_thing` | sequential overlay |
| 6:58 | `02_wire_bells` | moving plate |
| 8:31 | `18_rod_closeup` | moving plate |

Motion/phone/Teach beyond these automated WARNs: Chief review of contact sheet + master. No freeze FAILs claimed cleared solely from contact sheet.

## Outstanding (not PASS)

- Elected-Chief graphics/composite PASS on the eleven rows + v03 cut
- Music / SFX finishing (`SKIPPED_NO_BED`)
- No Ben watch / upload / privacy change
- £0 spend under this job; no new Flow mint

## Detached run record

- tmux: `j1218-asm-v03`
- log: `~/_desk/logs/j1218-asm-v03.log`
- done: `~/_desk/logs/j1218-asm-v03.done`

## Delivery follow-up (Cursor, 30 Oct ~03:28 UTC)

Assembler deliver hit `rsync` exit 20 into the NAS film folder. Same-volume `cp` later completed: film-folder `rough_v03/hos_008_rough_v03.mp4` is **990399088** bytes (matches WORK). UAT sha256 verified `0da87a82…`. Container **540.021321 s** (21 ms mux padding; not extra speech). Sidecars + SHA256SUMS written beside the NAS master.
