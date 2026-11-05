# J2217 — eight-item Franklin recipe amend

Cursor worker, 5 November 2026, revised the same day for the J1881 elected-Chief FIX. Code and evidence only. GBP0. No production approval. No note is marked resolved. This amends J2163 (`50620e40`) and does not replace its measured PTS file or its historical `six_rows`. `J2163_DRY_RUN.json` stays the earlier six-row run.

The planner in `_build_rough_v13_recipe.py` reads `eight_rows` and refuses `--execute` until J1881 re-reviews this amend. h22/h35, J1297, and the J1755/PR401 publication rejection are unchanged. PR #411 and desk PR #180 are not merged here. This session did not watch the picture or hear the soundtrack.

## Evidence level

Keyframe flags and an aligned `[kf_in, kf_out-1]` span are a **candidate keyframe envelope**. They do not prove a closed GOP. `build_plan` now records `candidate_keyframe_envelope`, `gop_closure_proven: false`, and `dependency_validation: OUTSTANDING`. Original PTS values and durations stay on the patch. Unchanged decoded frames and audio still have to match. J2242 has to prove dependencies and that preservation before its output can be accepted. The splicer is not implemented here.

Hot-night frames 1129–1231 and points-desk frames 4511–4670 are those candidate envelopes from `J2163_MASTER_FRAME_PTS.json`. The 27 caption windows are the same kind of envelope (`[0, 141]` through `[12297, 12461]`).

## Master clock map

Source: `J2163_MASTER_FRAME_PTS.json`. Master SHA256 `cf1561c218bace7bc14ed3d625b0790a457027a90f392262f45ca7172723099b`. Timebase `1/12288`.

| Ben clock | Decoded frame | PTS | What the cut list puts there | Planner row |
|---|---|---|---|---|
| 0:51 | 1220 | 51.000 s (`626688` ticks) | `07_hot_night_t1.mp4`, candidate envelope 1129–1231 (`103` frames). SHA256 `30da07fe8860c3640fdb99a4439b858cfbd2460b94510e5e20d23da6b1b728c3`. | Tracked. Not a splice. |
| 1:49 | 2506–2665 | 104.667–111.333 s | `02_salon_spark_t1.mp4`. SHA256 `4b61312e9416b68853409b7d67683643934b44cc2d56e48623b8b0c4e8c58a92`. | Original row, still unresolved. |
| 2:18 | 3305 | 138.000 s (`1695744` ticks) | `07_foil_jar_t1.mp4` | Inside replace 3260–3343. Outside keep 3168–3259. |
| 2:20 | 3353 | 140.000 s (`1720320` ticks) | Next keyframe is 3344. Candidate envelope 3344–3404. | Distinct from the jar replace, which ends at 139.625 s. |
| 3:13 | 4621 | 193.000 s (`2371584` ticks) | `01_points_desk_t1.mp4`, candidate envelope 4511–4670 (`160` frames). SHA256 `a9a32aa475424a973ea6e75ad1b9e260897f554723b57e6a5fc3a946980cbf15`. | New row. `--retake-p3-01` accepts a future plate. |
| 7:59 | 11469 | 479.000 s | `13_rods_spread_t1.mp4` | Inside existing frames 11358–11492. |

## 0:51 disposition

Ben's words stay: "still have hair flying out the tube, this needs rebuilt".

The source map, which is not a watched picture, puts clock 0:51 on the night-street plate. That plate is left untouched. `splice` is false, and `distinct_hot_night_rebuild` is false, so `build_plan` does not emit a night-street patch.

The hair-and-tube file in the cut list is `02_salon_spark`, already the unresolved 1:49 row, near 1:51 (frame 2658). Reading the 0:51 note as that salon rebuild is an **inference pending capable in-context confirmation**. It is not marked resolved, and no generation is authorized.

## 2:18 and 2:20 are different checks

J1880 keep is frames 3168–3259 (132.291667–136.125 s). The jar replacement proposal is 3260–3343 and ends at 139.625 s. Frame 3305 (2:18, the jar flip) is inside that replacement and outside the keep.

Frame 3353 (2:20, the silver foil) is past that end. Replacing 3260–3343 does not cover it. The foil check stays unresolved and is not a splice in this amend.

## Film-wide captions

`plan_captions()` turns the 27 `side_label` inventory into 32 planned cards. Each card is at most four words, held at most 4 seconds, one at a time, on an unbordered umber panel over the moving plate. Timing is the master PTS of those frames. Words are the existing label, split in order where the line was longer than four words:

| Existing label | Planned cards |
|---|---|
| THE ANSWER IS ON THE ROOF | THE ANSWER IS / ON THE ROOF |
| A KITE · A KEY · A JAR | A KITE / A KEY / A JAR |
| LET THE EXPERIMENT BE MADE | LET THE EXPERIMENT / BE MADE |
| PENNSYLVANIA GAZETTE · 19 OCTOBER 1752 | PENNSYLVANIA GAZETTE / 19 OCTOBER 1752 |

A window longer than 4 seconds keeps the card to 4 seconds. The rest of that window is recorded as remainder ticks and is not a static hold. Nineteen windows have a remainder. Years on the cards already appear in `FACT_NOTES_v01.md`. No new date, number, or claim is added. Nothing is rendered.

The 27 side labels match `cuts_rough_v12.json`. That match does **not** prove every bottom text is covered. The same cut list has code-graphic and overlay rows whose internal words are not in `side_label`, plus `11_safe_path`, whose disposition names the title SAFE PATH DOWN. That title is a separate planned card (3 words, hold 10/3 s, frame 11038), still unresolved, still not rendered.

## Retake argument

`--retake-p3-01` and `--retake-p3-01-sha256` are accepted. A missing file, a bad hash, or fewer than 160 frames is refused. The same path still refuses `--execute`. The splicer remains J2242.

## Spend preflight

`ai_spend.py check` is not a command. The CLI is `record`, `spend`, `report`, and `doc`. A future take has to read the live Flow balance with `read_account()` in `_mint_flow_cdp_v01.py` (CDP `ORBIT_FLOW_CDP`, account `benoats@googlemail.com`, the route `_mint_flow_v03.py` already uses) and the Quality price shown on the Flow confirm dialog. Log the reading with `record` and any later take with `spend`. Subtract spends logged since the reading. Caps stay 3 takes and 300 subscription credits per plate, 900 in total, GBP0, no top-up and no overage. `authorized` is false. This FIX does not open Flow.

## Checks

`python3 -m unittest test_j2163_recipe.py` — 18 tests, OK. `--execute` exits 2 with the J1881 refusal. No output file was written. Frame identity, VO sync, and loudness remain unmeasured.
