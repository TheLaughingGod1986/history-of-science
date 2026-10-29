# J1218 — HOS 008 rough v02 repair notes (Cursor)

**Job:** J1218 (diagnostic rough v02 from J1213 FIX).  
**Worker:** cursor. **No Ben Ready-for-OK.** Park for Chief only.

## Master

| Field | Value |
|---|---|
| Version | `rough_v02` (v01 preserved) |
| Duration | **540.02 s** (≤9:00; pause-trim −17.493 s from 557.814 s) |
| SHA256 | `edebeaf7e71d29051135859d7ad7e87bb4ee73d7e52a37b8251ccfb951dcad06` |
| WORK | `/Volumes/data/mac-mini-archive/tmp-render-scratch/j1218-hos008-rough-v02/full_join_v01/` |
| Desk | `07_Edit-Project/_desk/008/rough_v02/` |
| NAS | `/Volumes/data/mac-mini-archive/YouTube/History Of Science/02_Video-Projects/008_Lightning-Franklin/07_Edit-Project/rough_v02/` |
| Assembler | `_assemble_rough_v02.py` (versioned; v01 preserved beside it) |

## Repairs applied (£0, locked VO, no new Flow/music)

1. **P4 `06_same_thing` (~6:01 v01):** removed hstack split; sequential full-frame jar_spark → knuckle_spark.
2. **P5 `10_metal_easy` (~7:58 v01):** full-frame period-paper CG (no white linework over worker/ladder).
3. **P2 `09_window_storm` (~2:30 v01):** left 5% crop reframe (natural mullion; not labelled a confirmed split).
4. **§4 pause-trim:** silences >0.6 s cut; target ≤540 s. Cuts JSON remapped through removals so gates seek inside the trimmed master (bugfix: reuse path previously dropped `prior_cuts` and remap no-oped).
5. **No music bed:** `SKIPPED_NO_BED` (credit hold / Chief OK required). **Not PASS.**
6. **No new Flow mint.** Any row that still needs a mint is parked with cost for Ben — none spent under this job.

## Gates (re-run on remapped cuts; local `/private/tmp/j1218_gates` then sync)

See `polish_gate_rough_v02.*`, `picture_qa_rough_v02/`, `music_gate_rough_v02.*`, `contact_rough_v02.jpg` in this folder after the detached gate job lands.

## Outstanding (Chief)

- **J1193** still open — code-graphic motion review is a required input to final graphics PASS. Not claimed in this dispatch (J1218-only).
- **Music / SFX finishing** still outstanding (`SKIPPED_NO_BED`; no SFX level PASS claimed).
- **Teach on screen / Polish** film review beyond automated gates — Chief.
- Original **J1213** remains held pending this repair + J1193.
- iCloud **HOS UAT** copy may fail with Errno 11 (deadlock); NAS + desk hold the durable master.

## Not done by this worker

- No upload, schedule, privacy change, or Ben Ready-for-OK card.
- No final OK / PASS / merge of AGENTS or Never-list changes.
