# HOS 009 Tranche 2 — Half-Second Still Sheets & Stated-Rule Verdicts (J2582)

- **Job:** `J2582` (ref `J2034`)
- **Reviewer:** `gemini` (specialist worker)
- **Date:** `2026-11-11`
- **Rulings in force:**
  - Acting Chief ruling: [PR #180 comment 6792271903](https://github.com/TheLaughingGod1986/history-of-science/pull/180#issuecomment-6792271903)
  - Chief (Grok) ruling: [PR #180 comment 6792304982](https://github.com/TheLaughingGod1986/history-of-science/pull/180#issuecomment-6792304982)
  - Chief (Grok) amended `P02:08_the_apple_c1` ruling: [PR #180 comment 6792364829](https://github.com/TheLaughingGod1986/history-of-science/pull/180#issuecomment-6792364829)
- **Machine-readable evidence:** `02_Video-Projects/009_The-Falling-Moon-Gravity/07_Edit-Project/J2582_TRANCHE2_STILL_SHEETS_EVIDENCE_2026-11-11.json`
- **Sheets directory:** `02_Video-Projects/009_The-Falling-Moon-Gravity/07_Edit-Project/review_J2582_sheets/`

---

## 1. Dedicated Ruling Lines (`P02:08_the_apple_c1` and `P02:11_explorer_apple_c1`)

### A. `P02:08_the_apple_c1` (`take 1`, `sha256=838c28b3d4f5add8c12b0242275c833bc05fb7e751a4dc2af28ff140c845ffc1`, needed `use_s = 4.99 s`)
- **Full-clip half-second sheet (`0.00–7.88 s`, 18 frames):** `02_Video-Projects/009_The-Falling-Moon-Gravity/07_Edit-Project/review_J2582_sheets/P02_08_the_apple_c1_sheet.jpg`
- **Does the apple move upward at any point?** **YES.** At `t=0.00s–1.00s` (`f000–f024`) the green apple with a red flush lies still in the grass in front of the orchard bench (matching the last frame of parent `P02:08_the_apple`). From **`t=1.50s` to `t=2.50s` (`f036–f060`)**, the apple lifts off the grass and **rises upward** all the way into the upper tree branches, then hangs/drops from `t=3.00s` (`f072`), falls through `t=3.50s–4.99s` (`f084–f120`), and settles in the grass at `t=5.00s–7.88s` (`f120–f189`).
- **Continuous `4.99 s` window check:** None exists without upward motion and without a jump (`3.00–7.917 s` is `4.917 s < 4.99 s` and cutting in at `3.00 s` jumps the apple from the grass in the parent's last frame up to the tree branch).
- **Written outcome (per 6792364829):** **`retake`** (**FIX** — already covered by `J2583`).

### B. `P02:11_explorer_apple_c1` (`take 1`, `sha256=628cc70fa66e8733b6cd87759becf9d0cd1a31ea64b462875d73f6b43a8df183`, `use_s = 4.94 s`)
- **Used-window half-second sheet (`0.00–4.94 s`, 11 frames):** `02_Video-Projects/009_The-Falling-Moon-Gravity/07_Edit-Project/review_J2582_sheets/P02_11_explorer_apple_c1_sheet.jpg`
- **Quarter-second sheet (`3.00–5.00 s`, 9 frames at `0.25 s` steps):** `02_Video-Projects/009_The-Falling-Moon-Gravity/07_Edit-Project/review_J2582_sheets/P02_11_explorer_apple_c1_qsec_3to5s_sheet.jpg`
- **Stated-rule test (`>= 3` consecutive frames = camera move `KEEP`; `2` neighbouring frames = jump `FIX`):** Across all **9 consecutive quarter-second frames** (`3.00, 3.25, 3.50, 3.75, 4.00, 4.25, 4.50, 4.75, 5.00 s`) — and across all **49 consecutive 24fps frames `f072–f120`** (`MAD = 4.51–18.63`, smooth progression with zero 2-frame spike) — the framing changes continuously as a smooth camera push-in and tilt-up while the Explorer stands up from crouched to medium shot, tosses the red apple as prompted (`3.75–4.50 s`), catches it (`4.75 s`), and holds it up (`4.94–5.00 s`) beside the pale crescent Moon at upper left. Red apple and round gold glasses are settled (inherited from approved parent).
- **Verdict:** **`KEEP`** (`0.00–4.94 s`; camera move, no retake needed).

---

## 2. Newly Surfaced `FIX` Rows (Parked for Chief per Item 5)

Cutting half-second sheets across the full used window surfaced the **same upward-apple continuation defect** on the two Part 4 split-screen continuations (`P04:05_minute_second_c1` and `P04:05_minute_second_c2`), which was hidden in the earlier 4-frame still check (`f002, f063, f125, f187`):

1. **`P04:05_minute_second_c1`** (`take 1`, `sha256=4d69871bc14ebc9b7077be19ea24e44fa11c96c55e756a5c8483b6220087ca39`, window `0.00–6.76 s`) — **`FIX`**
   - **Sheet:** `02_Video-Projects/009_The-Falling-Moon-Gravity/07_Edit-Project/review_J2582_sheets/P04_05_minute_second_c1_sheet.jpg`
   - **Defect & frames:** Parent `P04:05_minute_second` ended with the green apple resting on the table at the foot of the blank wooden ruler. Because `c1` repeated `"on the left a green apple with a red flush falls for a moment beside a blank ruler"`, the apple on the left side of the split screen starts on the table at `t=0.00s–0.50s` (`f000–f012`), **rises upward up the ruler three times** — at **`t=1.00s–1.50s` (`f024–f036`)**, **`t=3.00s–3.50s` (`f072–f084`)**, and **`t=5.00s–5.50s` (`f120–f132`)** — alternating with downward drops at `t=2.00s–2.50s` (`f048–f060`), `t=4.00s–4.50s` (`f096–f108`), and `t=6.00s–6.76s` (`f144–f162`). No clean `6.76 s` window exists. Violates *"nothing falls upward"*.

2. **`P04:05_minute_second_c2`** (`take 1`, `sha256=c2f862ad7f39143ee5ec1309d031e75bef6001b8a1f0317a28825c9658d1511d`, window `0.00–6.75 s`) — **`FIX`**
   - **Sheet:** `02_Video-Projects/009_The-Falling-Moon-Gravity/07_Edit-Project/review_J2582_sheets/P04_05_minute_second_c2_sheet.jpg`
   - **Defect & frames:** On the left side of the split screen, the apple rests on the table at `t=0.00s–1.50s` (`f000–f036`), **rises upward from the table to the top of the wooden ruler across `t=2.00s–3.50s` (`f048–f084`)**, and falls back down across `t=4.00s–6.00s` (`f096–f144`). On the right side, the Moon **slides upward along its curve across `t=0.50s–2.00s` (`f012–f048`)** before drifting slightly down, and a second bright arc forms across the Earth at `t=4.00s–6.75s` (`f096–f162`). No clean `6.75 s` window exists. Violates *"nothing falls upward"*.

---

## 3. All 20 Tranche-2 Rows — Verdict, Window, Hash & Sheet Table

| Row | Take | SHA-256 | Used Window (`use_s`) | Upward Motion? | Verdict / Outcome | Sheet (`review_J2582_sheets/`) | Notes / Frame Findings |
|---|---:|---|---|---|---:|---|---|
| `P01:05_heavens_map_c1` | 1 | `bf781ede9d6524375ed13b4ac02549c76bc4bf9b1750dddaba33e05d9236ac5e` | `0.00–4.58 s` | No | **KEEP** | `P01_05_heavens_map_c1_sheet.jpg` | 11 frames: spheres and planets turn smoothly around central Earth; no vanishing/morphing; forbidden list clear. |
| `P01:07_night_field_c1` | 1 | `3161b6e6993ef2e930c779187ccc3eea507c5041526e1f73ae1d8b07c51df093` | `0.00–4.65 s` | No | **KEEP** | `P01_07_night_field_c1_sheet.jpg` | 11 frames: young man from behind with lantern in night field looking at Moon on horizon as curved arc draws smoothly. |
| `P02:01_cambridge_closes_c1` | 1 | `666c40de800f4f68b09a1668692dbe483ff4e6edfa1cbf2e20bd9a799be26329` | `0.00–4.19 s` | No | **KEEP** | `P02_01_cambridge_closes_c1_sheet.jpg` | 10 frames: gates swing, students load trunks to carts; hats settled (from parent); no gate notice or plague horror. |
| `P02:03_christmas_birth_c1` | 1 | `3a5d884e2e03145328369fae461f34760fb86602c2ac1772ca4bfd7dc9eddcfb` | `0.00–5.02 s` | No | **KEEP** | `P02_03_christmas_birth_c1_sheet.jpg` | 11 frames: winter timber farmhouse (settled from parent) with single candle in window; no baby shown; forbidden list clear. |
| `P02:05_working_alone_c1` | 1 | `02f3ccbe6346518230f6ad5d7c78da8781e9518bceec0120071f0177c04362f2` | `0.00–5.16 s` | No | **KEEP** | `P02_05_working_alone_c1_sheet.jpg` | 12 frames: young Newton at table with candle and prism rainbow on wall; reaches hand smoothly to prism `2.50–5.16 s`. |
| `P02:08_the_apple_c1` | 1 | `838c28b3d4f5add8c12b0242275c833bc05fb7e751a4dc2af28ff140c845ffc1` | `0.00–4.99 s` (full `0.00–7.88 s`) | **Yes (`1.50–2.50 s`)** | **FIX (`retake`)** | `P02_08_the_apple_c1_sheet.jpg` | 18 frames across full clip: apple in grass `0.00–1.00 s`, **rises to branch `1.50–2.50 s` (`f036–f060`)**, falls `3.00–4.99 s`. Outcome: **retake** (in `J2583`). |
| `P02:10_how_high` | 1 | `540cb3667bbd315aa7db42d1cf989fb1c46f6e3557670ee4f5281e1b4d2d8f05` | `0.00–2.58 s` (hard out `2.58 s`) | No | **KEEP** | `P02_10_how_high_sheet.jpg` | 7 frames (`0.00–2.58 s`): young Newton looks from fallen apple up to high daytime Moon; clean inside `0.00–2.58 s` lock. |
| `P02:11_explorer_apple_c1` | 1 | `628cc70fa66e8733b6cd87759becf9d0cd1a31ea64b462875d73f6b43a8df183` | `0.00–4.94 s` (+ `3.00–5.00 s` qsec) | No (prompted hand toss) | **KEEP** | `P02_11_explorer_apple_c1_sheet.jpg` + `P02_11_explorer_apple_c1_qsec_3to5s_sheet.jpg` | Framing changes smoothly across all 9 quarter-second frames `3.00–5.00 s` (and all 49 frames `f072–f120`, MAD `4.51–18.63`): camera move, not a jump. |
| `P03:01_really_falling_c1` | 1 | `9e6fa8d1beee098fd4e2f322981e218bd103154e5a98d7574969db3fe9e84e8c` | `0.00–5.26 s` | No | **FIX (`retake`)** | *(excluded per brief item 1; already remaking in `J2583`)* | Already ruled for 1 retake in 6792271903 / 6792292834 (Moon fades ~3.5 s and dark ball rides curve). |
| `P03:05_shot_orbit_c1` | 1 | `556bc9f79425e1101212efde11d397c8019c18f66a5555ae4282379129329c19` | `0.00–6.42 s` | No | **KEEP** | `P03_05_shot_orbit_c1_sheet.jpg` | 14 frames: silver cannonball curves around Earth on golden orbital trail as camera pulls back above mountain peak. |
| `P03:05_shot_orbit_c2` | 1 | `f62b975a10a7a68c2f519132aee430ae657f3b2f0918b0d963d8913ebc147f93` | `0.00–6.42 s` | No | **KEEP** | `P03_05_shot_orbit_c2_sheet.jpg` | 14 frames: continues from `c1`; silver cannonball sweeps around golden orbital loop past snow-capped mountain peak. |
| `P03:07_ball_to_moon` | 1 | `fba484bb8b37055948991f701cf788e8b02015f6e230c866c83f0106e838b95d` | `0.00–2.84 s` | No | **KEEP** | `P03_07_ball_to_moon_sheet.jpg` | 7 frames: dark cannonball orbits counter-clockwise along inner ring around Earth while Moon orbits on outer golden ring. |
| `P04:05_minute_second_c1` | 1 | `4d69871bc14ebc9b7077be19ea24e44fa11c96c55e756a5c8483b6220087ca39` | `0.00–6.76 s` | **Yes (`1.00–1.50 s`, `3.00–3.50 s`, `5.00–5.50 s`)** | **FIX (parked for Chief)** | `P04_05_minute_second_c1_sheet.jpg` | 15 frames: apple on left starts on table (`0.00–0.50 s`) and **rises upward up the ruler 3 times** (`1.00–1.50 s / f024–f036`, `3.00–3.50 s / f072–f084`, `5.00–5.50 s / f120–f132`). |
| `P04:05_minute_second_c2` | 1 | `c2f862ad7f39143ee5ec1309d031e75bef6001b8a1f0317a28825c9658d1511d` | `0.00–6.75 s` | **Yes (`2.00–3.50 s` apple; `0.50–2.00 s` Moon)** | **FIX (parked for Chief)** | `P04_05_minute_second_c2_sheet.jpg` | 15 frames: apple rests on table `0.00–1.50 s`, **rises upward to top of ruler `2.00–3.50 s` (`f048–f084`)**, falls `4.00–6.00 s`; Moon slides upward `0.50–2.00 s` (`f012–f048`). |
| `P04:08_halley_visit_c1` | 2 | `519bbb3da322a3f2d9e4b5463cf2bf267fb7f8734b755ce40b9237ae0d41f496` | `0.00–5.88 s` | No | **KEEP** | `P04_08_halley_visit_c1_sheet.jpg` | 13 frames: Halley and Newton converse across book-piled table in Trinity room; natural dark hair, no wigs, no readable text. |
| `P04:08_halley_visit_c2` | 1 | `d7e9d2748eee0e9b8d475fa0acda8f7caf777cfa4c5eeffc464433f89e3dbbbb` | `0.00–5.88 s` | No | **KEEP** | `P04_08_halley_visit_c2_sheet.jpg` | 13 frames: continues from `c1`; Halley and Newton converse across table; no wigs, no readable text, no vanishing/morphing. |
| `P05:04_comet_1758_c1` | 1 | `655cc16e317aaa8303e0dcfae2a8a49c697d344049374f4f1d68bdb3d086ec19` | `0.00–4.49 s` | No | **KEEP** | `P05_04_comet_1758_c1_sheet.jpg` | 10 frames: farmer-astronomer at wooden telescope beside Saxon farmhouse at night with faint comet above; frost settled. |
| `P05:05_iss_orbit_c1` | 1 | `fb8873d899c9abcbc1642a91cd58b6b3248ebd72914b828e76344617493158b2` | `0.00–7.70 s` | No | **KEEP** | `P05_05_iss_orbit_c1_sheet.jpg` | 17 frames: space station glides in orbit over blue Earth; shape settled; no flags, logos or letters anywhere. |
| `P05:05_iss_orbit_c2` | 1 | `07b94285af0c3f2898e6f8f9e6f2c8bfee5d57d4d2c9f96435b3e8d7ce21b8e4` | `0.00–7.71 s` | No | **KEEP** | `P05_05_iss_orbit_c2_sheet.jpg` | 17 frames: continues from `c1`; space station glides in orbit over blue Earth; no flags, logos or letters anywhere. |
| `P05:06_iss_apple_c1` | 1 | `7eda8b737ff43c906ae358c2d7076131104c50002e53e19bd3610667babcc133` | `0.00–4.59 s` | No (zero-g cabin drift) | **KEEP** | `P05_06_iss_apple_c1_sheet.jpg` | 11 frames: two generic astronauts with gold visors and green-and-red-flushed apple drift and rotate slowly in station cabin. |
