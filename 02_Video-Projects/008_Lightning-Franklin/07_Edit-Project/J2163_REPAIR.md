# J2163 — Franklin recipe repair for J1881

Codex specialist worker, 4 November 2026. Code/evidence only, GBP0. No production approval. All six Ben notes remain unresolved. PR409 evidence at `bd5302494c7337058426b2d8714fa4cf4c90efa9` and its original inventory are preserved; the new manifest supersedes that inventory's proposed recipe, not its historical evidence.

Live read of `/api/checks` at 23:55:09Z confirms `HOS-008`, `v03`, `change`, original review `2026-11-03T16:08:33.439Z`, all six original notes. Saved in `J2163_CHECKS_READ.json`. No API mutation. J1297/h22/h35 remain historical; J1755/PR401 publication rejection stays separate.

## Measured input evidence

Read-only master SHA256 matches `cf1561c218bace7bc14ed3d625b0790a457027a90f392262f45ca7172723099b`, 393139693 bytes. Complete ffprobe decoded-frame traversal emitted no decoder diagnostics. 12,923 frames, timebase 1/12288, start1536 ticks=0.125s, end6630912 ticks=539.625s, duration539.500s. No replacement movie was produced.

`J2163_MASTER_FRAME_PTS.json` preserves every frame's integer PTS, reported duration and keyframe flag. There are 23 PTS steps of1024 ticks and one of1536; ordinary steps are512 ticks. Thus frame_index/24 loses25 frame periods (1.041667s) across the source. Forty differences between a frame's reported duration and the next PTS are retained as signed metadata, not smoothed: these are not all missing-image gaps. Future splicing must preserve both original timestamp and duration metadata and resolve presentation semantics, never fill or collapse them.

| Ben note | Conditional changed frames | Measured PTS start–end, seconds | Preservation |
|---|---|---|---|
|00:20|427–544|17.916667–22.833333|Sequential <=4-word white Didot italic labels over moving plate; soft cream/umber treatment, no pill/border. Master-derived word alignment and phone evidence still required.|
|0:30|744–839|31.166667–35.166667|663–743 remain unchanged. Proposed sentence30.70 / next31.24 require master-derived alignment; no claim that stored part offsets prove a safe cut.|
|1:49|2506–2665|104.666667–111.333333|160 candidate frames; adjacent2666–2717 unchanged. Exact glass-tube/hair asset missing; no table-globe fallback selected.|
|2:20|3260–3343|136.125000–139.625000|3168–3259 remain decoded-identical, following spark3344–3407 retained. Conditional jar source4.000–7.500s, KEEP/repeat checks outstanding.|
|3:31|4977–5077|207.833333–212.125000|One animated ink letter crossing over moving ship plate; no city/date/distance claim or bordered banner. Actual candidate duration4.291667s, not101/24.|
|7:58|11358–11492|474.375000–480.000000|135 candidate frames; exact ship-mast asset missing; roofs fallback not selected.|

Four proposed native inputs were independently SHA256-checked and decoded, with actual availability at requested intervals checked (`J2163_DRY_RUN.json`). Reference/retake media are not selected inputs: future generation must hash the named reference and verify every resulting take. Missing or short explicitly requested retakes fail, with no fallback.

h22 rough-v12 evidence (`ROUGH_V12_SUMMARY.json`, Chief review RULING) identifies `d032e5fb7ae89f492f1d4df59070ce13a419c23287834780f8996999d17520b4`. J1880's `02db759e...` is a different claimed byte identity, not relabelled as h22. This repair uses only the independently hash-verified h35 master for timeline/picture. Any alternate rough requires independent hash and elementary-video/decoded-frame/PTS comparison. h35 mix is -14.129 LUFS / -1.2 dBTP per J1881, consistent with existing rounded master review (-14.1/-1.2); J1880's -15.32/-1.00 is superseded. No new loudness/sync measurement is claimed.

## Code boundary and execution contract

The unsafe whole-film renderer, global CFR reconstruction, lossy unchanged-range extraction, repeated-last-frame/blank fallback, automatic native Option A selection, and unsupported overlay claims have been removed from the active recipe. Original implementation remains in the recorded Git parent. The repaired script is intentionally a **read-only planner**, with unconditional execution refusal from CLI and callable API. This is the safest concrete code result within this no-render repair scope; it is not a production splicer ready to run after toggling a flag.

Actual keyframes bound candidate GOP envelopes: note1 423–544; note2 744–839; note3 2506–2665; note4 3168–3343; note5 4977–5077; note6 11358–11492. They are not approved re-encoding windows. In particular note4 may require boundary handling of92 safe frames, and note1 four leading frames; preserve those decoded frames exactly using a tested lossless boundary encode, or another proven packet-preserving method. Keyframe flags alone do not prove closed GOPs; inspect dependencies before approving any window. Copy untouched closed GOP compressed packets; encode only explicitly recorded/approved boundary windows, preserving actual PTS/durations and source start. No global CFR or global re-encode. The separately authorized production job must implement and test this splicer, then prove exact unchanged decoded-frame hashes at source PTS. No identity claim from interval arithmetic.

Copy original h35 audio packets without shift. Compare payload hash, PTS, DTS, duration, timebase, side data/edit lists and packet/sample counts over the full output. Measure VO sync at each patch and historical checkpoints. Output frame delta, VO lag, unchanged-frame identity and audio identity remain **UNMEASURED** until execution and comparison. Hashes and source availability are input checks, not film QA.

## Missing assets and Chief handoff

Search budgets are already exhausted at three candidates each; no new search performed. J1881 retains the decision and must separately scope production/generation:

- 1:49: exact glass-tube/spark/hair interaction. Named reference `02_salon_spark_t1.png`, SHA256 `aefd6338aded1037c11306a99fc580d1a62a66d9367409f01e0edd993cc8cc58`. Proposed Flow/Veo3.1 **Quality only**, fragile spark, maximum3 takes/300 subscription credits; fresh live balance required. No spend authorized here.
- 7:58: exact church/house/ship-mast rods. Named reference `13_rods_spread_t1.png`, SHA256 `84a92bf6ce1abd1a5780c37ac2e8ae50ea6099f5cff5c7f728a70060b394819c`. Proposed Flow/Veo3.1 maximum3 takes; current rate, credit cap and fresh live balance must be recorded in separate scope. No spend or native fallback authorized here.

Future QA covers all six corrections and full cut/transitions, phone readability, picture_qa, polish_gate, episode gate, package lint, music_gate, SFX levels and measured VO sync, followed by elected Chief and Ben's final watch/listen. No lower gate is waived. This session has no demonstrated native audio/moving-video perception; decode and still evidence never count as hearing or watching.

## Validation and limits

Eleven targeted tests pass; final test evidence is `J2163_TESTS.txt`. Synthetic timestamp fixtures cover nonzero start/gaps, short/truncated decode, invalid timestamps, decoder failure/diagnostics, hash/size mismatch, missing retake, overwrite refusal, safe windows and execution refusal. Read-only real-input dry-run status is `PLANNED_NOT_EXECUTABLE`; full raw per-frame probe output is compacted without removing source timestamp data. No render, spend, upload, watch publication or YouTube changes.

Disk free space was8.2GB. Authorized `nas_offload.py --apply` reported it waits for the01:00–06:00 NAS window and moved nothing. This small text-only repair creates no render scratch.
