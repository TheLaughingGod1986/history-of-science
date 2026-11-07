# J2171 — HOS 009 Shorts A & B GBP0 Inventory, SHA-256 Media Reconciliation & Assembly Plan v03 (7 Nov 2026)

- **Worker:** `gemini` (specialist worker under Acting-Chief Codex `J2023`, 5 Nov 2026)
- **Scope:** `£0` / `0` credits. No generation, no credit spend, no upload, no scheduling, no privacy/retitle or Buffer writes. Clean worktree from `origin/main` (`a7183325`). All existing `v02`/`v03`/`v04` VO files and `SHORTS_PICTURE_PLAN_v02.json` preserved untouched.
- **Direct `audio_input` audition:** Both accepted VO masters (`hos_009_short_A_v02.mp3` and `hos_009_short_B_v04.mp3`) were directly auditioned in-session via `read_file` (`audio/mpeg`), confirming clean British narration, zero spoken repeats, intact `"Isaac Newton"` onset at `6.74 s` in Short B `v04`, and completed hooks within `<= 2.850 s`.

---

## 1. Duplicate Idea & Channel State Check (`2026-11-07` Snapshot)

- **Snapshot:** `orbit-with-ben/05_Analytics/hos/snapshots/2026-11-07.json` (`64` HOS videos) + `00_Brand/Channel-Setup/audits/SHORTS_LOG.md`.
- **Gravity / Newton / Moon / Orbit overlap:** **`0` matches** across all public, scheduled, and private HOS videos.
- **Promoted 009 Long (`Why Doesn't the Moon Fall to Earth?`):** Not yet uploaded or scheduled on YouTube (planned target `Thu 26 Nov 2026 18:00 UTC`; long assembly `J2035` -> QA `J2036` -> Ben watch `J2037`). Per `J2171` and `STUDIO_PLAYBOOK.md`, the 009 long must be public before either HOS 009 Short airs (conditional planning targets: Short A `Fri 27 Nov 2026 11:30 UK`, Short B `Mon 30 Nov 2026 11:30 UK`; watch-ready target `Tue 24 Nov 2026 18:00 UTC`).

---

## 2. Dependency Status (`J0862` Complete; `J2033` / `J2034` / `J2035` Incomplete)

1. **`J0862` / `J2279` / `J2281` (Shorts VO disposition) — COMPLETE (`PASS / KEEP`, HOS PR #423 `a7183325`):**
   - **Short A (`hos_009_short_A_v02`):** `24.320 s` VO (`25.320 s` with `1.000 s` loop tail), `59` words, `hook_end_s = 2.800 s <= 2.850 s` (*"The Moon is falling towards the Earth right now."*).
     - `.mp3` SHA-256: `c2fd407d3aafbe57030b29b213ed128ee4887b785272a2192b4c0809796a1ce6` (`390,188` bytes)
     - `.wav` SHA-256: `48847b15feda51804a0f6afae1a79aacc74b9bac43ef3eeadda8a7503b745571` (`4,669,518` bytes)
   - **Short B (`hos_009_short_B_v04`):** `24.480 s` VO (`25.480 s` with `1.000 s` loop tail), `59` words, `hook_end_s = 2.820 s <= 2.850 s` (*"In one minute, the Moon falls five metres. An apple falls that far in one second."* — preserves both `"In one minute"` and `"in one second"` intervals and all `J1004`/`J1894`/`J2195`/`J2279` rulings).
     - `.mp3` SHA-256: `0c9c4c6ffdb1337dc11acaf57af909f8d8be91d77210bca2e13af80715b87498` (`588,716` bytes)
     - `.wav` SHA-256: `a6666fd27c9a90e781369ea07e4888d87a2d5edb1624a0090ae98fa39504686b` (`2,350,158` bytes)
2. **`J2033` (Mint 20 Tranche 2 Quality rows) & `J2034` (Chief picture review & complete 009 picture acceptance) — INCOMPLETE:**
   - `J2033` is currently blocked on `J2275` / `J2200` runner repair (`0/20` Tranche 2 rows minted).
   - `J2034` (`after: J2033`) is open awaiting `J2033`.
   - **Short A row `S03` (`5.74–8.98 s`, `use_s = 3.24 s`, `P3:07_ball_to_moon`)** is one of the 20 unminted Tranche 2 Quality rows in `07_Edit-Project/TRANCHE2_SCOPE_J2026.json` (`Part 3, id: 07_ball_to_moon`).
   - **Short B row `S06` (`14.50–17.65 s`, `use_s = 3.15 s`, `P4:04_dots_square`)** is a `moving_plate_overlay` code graphic whose named background plate `02_spray_paint_c2` (`02_spray_paint_c2_t1.mp4`, `sha256: 0a6279c069fae36a...`) was minted in Tranche 1 (`J1192` KEEP / `J1237` PASS) and awaits moving-plate compositing & review under `J2034` / `J2035`.
3. **`J2035` (Long assembly & `05_Music/` score bed) — INCOMPLETE:**
   - HOS 009 does not yet have an `05_Music/` score bed on local disk or NAS (`J2035` owns checking/queuing the film's score bed after `J2034` PASS; Shorts A and B reuse the film's score bed at `£0` once available).
   - House SFX (`06_Sound-Effects/kit_v01`: `rumble_low.wav`, `whoosh_soft.wav`, `tick_ink.wav`) is synthesised at `£0` via `sfx_kit.py make --house hos` at assembly.

---

## 3. Exact Row-by-Row Media & SHA-256 Inventory (`SHORTS_PICTURE_PLAN_v03.json`)

### Short A — *What Would Happen If the Moon Stopped Moving?* (`hos_009_short_A_v02`, `25.32 s`)

- **Promoted long title at `9.0–14.0 s`:** *Why Doesn't the Moon Fall to Earth?*
- **Frame-0 hook caption:** `IT'S FALLING` (`FALLING` in yellow)

| Row | Window (s) | `use_s` | Source Plate | Kind | Probed Dur (s) | SHA-256 (verified local + NAS) | Status | Spoken |
|---|---|---:|---|---|---:|---|---|---|
| `S01` | `0.00–2.80` | `2.80` | `P1:01_moon_falling` | Flow Veo Quality (T1 KEEP, `J1237` PASS) | `8.000` | `3e0774a7dd510b5ee32358c188f5efe4903aaf45aafab8870df662bcc1cd4c1f` | Ready | *The moon is falling towards the Earth right now.* |
| `S02` | `2.80–5.74` | `2.94` | `P3:08_km_a_second` | `code_graphics_v01` (`SIDEWAYS AND DOWN`) | `4.950` | `b18c90bc720791f3b4e084db41ca2df4e573d791db74191032366ae9d42a6f58` | Ready | *Every second, it moves sideways about a* |
| `S03` | `5.74–8.98` | `3.24` | `P3:07_ball_to_moon` | Flow Veo Quality (Tranche 2 parent) | — | — | **Blocked (`J2033`/`J2034`)** | *kilometer and drops a tiny bit towards us.* |
| `S04` | `8.98–12.14` | `3.16` | `P3:05_shot_orbit` | Flow Veo Quality (T1 KEEP, `J1237` PASS) | `8.000` | `0878c30646fa8b7158044a5e3d52a584a1cf4fda8accc76f6aa747fca8405f1b` | Ready | *But the Earth curves away beneath it,* |
| `S05` | `12.14–15.42` | `3.28` | `P2:07_orchard_bench` | Flow Veo Fast (T1 KEEP, `J1237` PASS) | `8.000` | `028ee06be5e3fb76cbc58265837633993c4834c961735c191c36379c5e7afa02` | Ready | *so it keeps on missing. Isaac* |
| `S06` | `15.42–18.62` | `3.20` | `P2:08_the_apple` | Flow Veo Quality (T1 KEEP, `J1237` PASS) | `5.083` | `357e8de3e9c771ef212fb01ee0a6052ebfedbc0de0ad9794270f5ff2128a5b44` | Ready | *Newton worked this out more than three hundred years ago.* |
| `S07` | `18.62–21.28` | `2.66` | `P3:06_orbit_teach` | `code_graphics_v01` (`FALLING SIDEWAYS`) | `4.400` | `840706a32f1717c789317f13c0a4481e334c34f8a39c9393f78a660ea9d9a178` | Ready | *An orbit isn't floating at all.* |
| `S08` | `21.28–24.32` | `3.04` | `P5:09_orchard_dusk` | Flow Veo Quality (T1 KEEP, `J1237` PASS) | `8.000` | `1266d61a73ccb6854051836495df72e9f0d0cbd71dd836981d887b9a5a41f` | Ready | *It's falling and missing forever* |
| `loop_tail` | `24.32–25.32` | `1.00` | `P1:01_moon_falling` | Flow Veo Quality (T1 KEEP, `J1237` PASS) | `8.000` | `3e0774a7dd510b5ee32358c188f5efe4903aaf45aafab8870df662bcc1cd4c1f` | Ready | *(loop return)* |

### Short B — *How Did Newton Discover Gravity?* (`hos_009_short_B_v04`, `25.48 s`)

- **Promoted long title at `9.0–14.0 s`:** *Why Doesn't the Moon Fall to Earth?*
- **Frame-0 hook caption:** `1 MINUTE = 1 SECOND` (`1 SECOND` in yellow)
- **`v03` cut-plan improvements over legacy `v02` (`SHORTS_PICTURE_PLAN_v03.json`):**
  1. Updates `Short_B` top-level rows from legacy `hos_009_short_B_v02` (`23.13 s`, unresolved hook `4.27 s`) to the Chief-approved `hos_009_short_B_v04` (`24.48 s` VO / `25.48 s` total, `hook_end_s = 2.82 s <= 2.85 s`).
  2. Replaces `S05` (`11.44–14.50 s`) legacy `P4:01_weaker_far` (`full_frame_period_paper` code graphic) with Tranche 1 KEEP moving 3D plate `P4:02_spray_paint` (`02_spray_paint_t1.mp4`, `7.917 s`, `sha256: 8a7b7d907240f959...`) so `S04` (`P4:03_sixty_earths`, full-frame period paper) and `S06` (`P4:04_dots_square`) are separated by a moving 3D plate (`AGENTS.md` *Teach on screen* Gate #6 MOTION & `J0383` alternation).
  3. Uses Tranche 1 KEEP continuation `P4:06_pretty_nearly_c1` (`06_pretty_nearly_c1_t1.mp4`, `8.000 s`, `sha256: eb3f5d5030b9b18a...`) on `S07` (`17.65–20.82 s`) instead of repeating `S03` (`P4:06_pretty_nearly`), giving `Short_B` 8 distinct body clips across `S01..S08`.

| Row | Window (s) | `use_s` | Source Plate (`v03`) | Kind | Probed Dur (s) | SHA-256 (verified local + NAS) | Status | Spoken |
|---|---|---:|---|---|---:|---|---|---|
| `S01` | `0.00–2.82` | `2.82` | `P4:05_minute_second` | Flow Veo Quality (T1 KEEP, `J1237` PASS) | `8.000` | `7f56f05930cefc854aabde17cd204510771dfbaaa5faa2f6b410facebbd3cd66` | Ready | *In one minute, the moon falls five meters.* |
| `S02` | `2.82–5.56` | `2.74` | `P1:02_apple_and_moon` | Flow Veo Quality (T1 KEEP, `J1237` PASS) | `7.917` | `bc3ad225b09a2fc090c4cbe694eb3aeeb0cf5999cd6c6d6262be81a1adcc90e6` | Ready | *An apple falls that far in* |
| `S03` | `5.56–8.42` | `2.86` | `P4:06_pretty_nearly` | Flow Veo Quality (T1 KEEP, `J1237` PASS) | `8.000` | `af487165258059d44e1f3ad9682d80d50c2239882f5495c82d7907a3e98d47ad` | Ready | *one second Isaac Newton worked out why.* |
| `S04` | `8.42–11.44` | `3.02` | `P4:03_sixty_earths` | `code_graphics_v01` (`SIXTY EARTHS`) | `4.680` | `4de87bc274d984971dabea10403c42ccb45ef654279414d36c19f3c3fce1ac10` | Ready | *The moon is 60 times further* |
| `S05` | `11.44–14.50` | `3.06` | `P4:02_spray_paint` *(v02: `P4:01_weaker_far`)* | Flow Veo Fast (T1 KEEP, `J1237` PASS) | `7.917` | `8a7b7d907240f959e7db25d3c9108439c5df79ae1b8261cde7079ac23342b092` | Ready | *from the Earth's center than we are, so the pull on it is* |
| `S06` | `14.50–17.65` | `3.15` | `P4:04_dots_square` (over `02_spray_paint_c2`) | `code_graphics_v01` (`SIXTY TIMES SIXTY`) | `5.530` | `7c393d99592073b975adb3faf4196f1253c5c193fd9316b839bc367e32cad072` | **Pending `J2034`/`J2035` composite** | *60 times 60 weaker, Three thousand* |
| `S07` | `17.65–20.82` | `3.17` | `P4:06_pretty_nearly_c1` *(v02: `P4:06_pretty_nearly`)* | Flow Veo Quality (T1 KEEP, `J1237` PASS) | `8.000` | `eb3f5d5030b9b18a545ce0922377771c10f499f14f08d1b64239adca975078cf` | Ready | *six hundred times. And the numbers matched.* |
| `S08` | `20.82–24.48` | `3.66` | `P5:01_one_law` | Flow Veo Quality (T1 KEEP, `J1237` PASS) | `7.917` | `ed89eb1e5c519f18984284d144ae924616f6d08560179fc6b2e4c3942e6053a0` | Ready | *One pull for apples and moons* |
| `loop_tail` | `24.48–25.48` | `1.00` | `P4:05_minute_second` | Flow Veo Quality (T1 KEEP, `J1237` PASS) | `8.000` | `7f56f05930cefc854aabde17cd204510771dfbaaa5faa2f6b410facebbd3cd66` | Ready | *(loop return)* |

---

## 4. Next Action per `J2171` Brief

Per `J2171` (*"If J2034 incomplete do useful inventory only then attach dependency, not claim a ready master"*):
- Useful `£0` inventory, SHA-256 verification across Mini + NAS, duplicate check, and `SHORTS_PICTURE_PLAN_v03.json` (`Short_A` `v02` + `Short_B` `v04` with `J0383` moving-plate alternation) are complete and committed.
- Attach dependency hold on `J2034` (complete HOS 009 picture acceptance after `J2033` mints `P03:07_ball_to_moon` and `J2034` reviews Tranche 2 + moving-plate code-graphic composites, alongside `J2035` long score bed).
