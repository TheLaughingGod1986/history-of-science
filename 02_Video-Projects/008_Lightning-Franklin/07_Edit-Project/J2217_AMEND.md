# J2217 — eight-item Franklin recipe amend

Cursor worker, 5 November 2026. Code and evidence only. GBP0. No production approval. No note is marked resolved. This amends J2163 (`50620e40`) and does not replace its measured PTS file or its historical `six_rows`.

The planner in `_build_rough_v13_recipe.py` reads `eight_rows` and refuses `--execute` until J1881 re-reviews this amend. Caption labels are a panel policy, not splice intervals. h22/h35, J1297, and the J1755/PR401 publication rejection are unchanged. PR #411 and desk PR #180 are not merged here.

## Master clock map

Source: `J2163_MASTER_FRAME_PTS.json`. Master SHA256 `cf1561c218bace7bc14ed3d625b0790a457027a90f392262f45ca7172723099b`. Timebase `1/12288`. This session did not watch the picture or hear the soundtrack. Frame numbers come from the stored PTS list.

| Ben clock | Decoded frame | PTS | What the cut list puts there | Planner row |
|---|---|---|---|---|
| 0:51 | 1220 | 51.000 s (`626688` ticks) | `07_hot_night_t1.mp4`, rough window 47.0017–51.3187 s, closed GOP master frames 1129–1231 (`103` frames). SHA256 `30da07fe8860c3640fdb99a4439b858cfbd2460b94510e5e20d23da6b1b728c3`, rechecked this session. | New row. Rebuild, not trim. |
| 1:49 | 2506–2665 | 104.667–111.333 s | `02_salon_spark_t1.mp4`. SHA256 `4b61312e9416b68853409b7d67683643934b44cc2d56e48623b8b0c4e8c58a92`, rechecked this session. | Original row, still unresolved. |
| 2:18 | 3305 | 138.000 s (`1695744` ticks) | `07_foil_jar_t1.mp4` | Evidence on the 2:20 row. Not a ninth splice. |
| 3:13 | 4621 | 193.000 s (`2371584` ticks) | `01_points_desk_t1.mp4`, rough window 187.952–194.6187 s, closed GOP master frames 4511–4670 (`160` frames: clean `4511–4606`, paper unroll `4607–4670`). SHA256 `a9a32aa475424a973ea6e75ad1b9e260897f554723b57e6a5fc3a946980cbf15`, rechecked this session. | New row. |
| 7:59 | 11469 | 479.000 s | `13_rods_spread_t1.mp4` | Inside existing frames 11358–11492. |

## Cut bounds

Hot-night frames 1129–1231 (`103` decoded frames) are the exact closed GOP in `J2163_MASTER_FRAME_PTS.json` (`frame 1129` `key_frame=1` at PTS `580096` = `47.208333 s` through `frame 1231` at PTS `632832` = `51.500000 s`, end `633344` = `51.541667 s`; `frame 1232` `key_frame=1` starts `08_sky_flash`).

Points-desk frames 4511–4670 (`160` decoded frames) are the exact closed GOP in `J2163_MASTER_FRAME_PTS.json` (`frame 4511` `key_frame=1` at PTS `2315264` = `188.416667 s` through `frame 4670` at PTS `2396672` = `195.041667 s`, end `2397184` = `195.083333 s`; `frame 4671` `key_frame=1` starts `02_sentry_box`). Zero residual: the 13-frame difference vs nominal `timeline_in*24` comes from 13 earlier inter-cut `1024`-tick steps in `J2163_MASTER_FRAME_PTS.json`. All 27 `caption_treatment.labels` use their exact closed-GOP `[kf_in, kf_out - 1]` intervals (`[0, 141]` through `[12297, 12461]`).

## 0:51 is not the 1:49 source

`same_source_as_1_49` is false. The clock lands on the night-street plate. The hair-and-tube plate is `02_salon_spark`, already the unresolved 1:49 row. Those frames are not copied onto the 0:51 row, because the planner rejects overlapping splices. The 0:51 row stays, with no generation authorized. J1881 chooses a distinct hot-night rebuild or a clock that points at the salon rebuild.

## 2:18 is outside the kept jar frames

J1880 keep is display frames 3168–3259 (132.291667–136.125 s). The replace zone is 3260–3343 (136.125–139.625 s). Frame 3305 is inside the replace zone and outside the keep. `inside_keep_3168_3259` is false. `inside_replace_3260_3343` is true.

## Film-wide captions

Ben's line is that bottom text needs a background colour over moving video. The active treatment is a soft unbordered umber panel on every rough-v12 `side_label` (27 cuts). No border, no gold rule, no pill chrome. The 00:20 row (frames 427–544) is the exemplar only. `inventory_is_splice_list` is false, so those 27 windows are not passed to `build_plan`.

## Checks

`python3 -m unittest test_j2163_recipe.py` — 14 tests, OK. `--execute` exits 2 with the J1881 refusal. No output file was written. Frame identity, VO sync, and loudness remain unmeasured.
