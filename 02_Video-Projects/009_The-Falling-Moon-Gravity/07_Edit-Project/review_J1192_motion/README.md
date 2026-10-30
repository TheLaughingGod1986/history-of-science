# HOS 009 Tranche 1 — Motion Evidence for the 3 Flagged Windows (J1192 / J1237)

- **Film:** `009_The-Falling-Moon-Gravity`
- **PR:** `#377` (`gemini/j1192-009-tranche1-flow-mint`)
- **Desk reference:** `#6511102950` (`ffmpeg freezedetect=n=-50dB:d=0.8` detector flags on 3 of 57 KEEP clips in `FLOW_MINT_LOG_v04_tranche1.json`)
- **Job:** `J1237` (worker: `gemini`)

---

## 3-Line Read Per Clip

### 1. `P01:03_table_three` (`03_table_three_t1.mp4`, flagged `3.333–4.375 s` / `f080–f105`, exported `2.833–4.875 s` / `f068–f117`)
1. **Motion continuity:** Motion is continuous across `3.333–4.375 s` (`f080–f105`, 0 duplicate frames, `MAD = 0.137–0.380`, `RMS = 0.552–2.750`) with no freeze, pop, morph or warp of any object (no hands in shot; the parchment settles under the brass cannon by `1.67 s`, the green apple finishes its gentle roll by `3.33 s`, and the camera maintains a slow, uninterrupted push-in through `3.333–4.375 s` that accelerates smoothly through `8.000 s`).
2. **Board in/out hold:** Holds cleanly in the cut at the v04/v05 board's full `use_s = 7.00 s` duration (`0.000–7.000 s` default, or `1.000–8.000 s`), as the `-50 dB` detector flag reflects only the transition between object settle and the steady camera push-in rather than a freeze or defect.
3. **Trimmed in/out:** No defect to trim around; keep board in/out **`0.000–7.000 s`** (or **`1.000–8.000 s`** for stronger late camera push-in, both `7.000 s`).

### 2. `P04:07_put_aside` (`07_put_aside_t1.mp4`, flagged `7.083–8.000 s` / `f170–f191`, exported `6.583–7.958 s` / `f158–f191`)
1. **Motion continuity:** From `0.000–7.083 s` (`f000–f170`) motion is brisk and continuous (`MAD` median `1.15`, 0 duplicate frames, no pop, morph or warp: papers slide into the wooden drawer and the drawer closes while window light shifts summer → autumn → winter → spring blossom), whereas `7.083–8.000 s` (`f170–f191`, `MAD = 0.077–0.546`) is a near-still tail hold after the seasonal transition completes at `7.083 s`.
2. **Board in/out hold:** Holds cleanly in the cut at the v04/v05 board's `use_s = 3.76 s` because the board uses less than half of the `8.00 s` raw clip and does not reach the `7.083–8.000 s` tail.
3. **Trimmed in/out:** Use board in/out **`0.000–3.760 s`** (`f000–f090`, covering the papers sliding into the drawer and the summer-to-winter transition; or **`3.200–6.960 s`** / `f077–f167` for the winter-to-spring sunbeam sweep), keeping `out <= 7.042 s` (`f169`) to exclude the `7.083–8.000 s` tail completely.

### 3. `P04:10_write_it_down_c1` (`10_write_it_down_c1_t1.mp4`, flagged `0.000–1.042 s` / `f000–f025`, exported `0.000–1.542 s` / `f000–f037`)
1. **Motion continuity:** The flagged opening `0.000–1.042 s` (`f000–f025`, `MAD = 0.099–0.508`, 0 duplicate frames) is a near-still pre-action hold of Newton seated from behind before he turns his head and raises his arm at `1.042–1.542 s` (`f025–f037`, `MAD` rising to `1.184`), with no pop, morph or warp in `0.000–1.542 s` (note: later at `2.67–5.33 s` / `f064–f128`, the standing helper's green-sleeved arm handing in the stack of pages remains behind the seated figure's right shoulder before withdrawing cleanly at `5.50 s`).
2. **Board in/out hold:** An untrimmed `0.000–5.340 s` cut would start on the `1.042 s` pre-action hold, but the v04/v05 board requires only `use_s = 5.34 s` out of the `8.00 s` raw clip (`2.66 s` of trim margin), so the board's duration easily avoids the flagged opening.
3. **Trimmed in/out:** Trim to **`1.083–6.423 s`** (`f026–f154`, `5.340 s`, starting immediately after the `0.000–1.042 s` flag as Newton turns to receive the pages; or **`2.583–7.923 s`** / `f062–f190`, `5.340 s`, starting directly on the stack placement and running through the clean solo desk settle at `5.50–7.92 s`).

---

## Summary Table & Exported Evidence

| Clip | SHA-256 (prefix) | Flagged Window (`freezedetect`) | Exported Window (`±0.5 s`) | Board `use_s` | Trimmed In/Out | Full-Size PNG Frames (`1280×720`) | Full-Size PNG Strip | 1-Row Contact Sheet | Grid Contact Sheet | Frame-Diff Plot |
|---|---|---|---|---:|---|---|---|---|---|---|
| `P01:03_table_three` | `49f567480e50` | `3.333–4.375 s` (`f080–f105`) | `2.833–4.875 s` (`f068–f117`, 50 frames) | `7.00 s` | `0.000–7.000 s` (or `1.000–8.000 s`) | `P01_03_table_three/frames/` | `P01_03_table_three_strip.png` | `P01_03_table_three_contact_1row.png` | `P01_03_table_three_contact_grid.png` | `P01_03_table_three_frame_diff_plot.png` |
| `P04:07_put_aside` | `abfc25c1c875` | `7.083–8.000 s` (`f170–f191`) | `6.583–7.958 s` (`f158–f191`, 34 frames) | `3.76 s` | `0.000–3.760 s` (or `3.200–6.960 s`, `out <= 7.042 s`) | `P04_07_put_aside/frames/` | `P04_07_put_aside_strip.png` | `P04_07_put_aside_contact_1row.png` | `P04_07_put_aside_contact_grid.png` | `P04_07_put_aside_frame_diff_plot.png` |
| `P04:10_write_it_down_c1` | `364e616e730e` | `0.000–1.042 s` (`f000–f025`) | `0.000–1.542 s` (`f000–f037`, 38 frames) | `5.34 s` | `1.083–6.423 s` (or `2.583–7.923 s`, `in >= 1.083 s`) | `P04_10_write_it_down_c1/frames/` | `P04_10_write_it_down_c1_strip.png` | `P04_10_write_it_down_c1_contact_1row.png` | `P04_10_write_it_down_c1_contact_grid.png` | `P04_10_write_it_down_c1_frame_diff_plot.png` |
