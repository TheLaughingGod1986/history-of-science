# HOS 009 Tranche 2 — J2629 Full-Clip Half-Second Sheet Check on the Two Third Takes

- **Job:** `J2629` (after `J2628`, scope `J2626`, ref `J2034`)
- **Reviewer:** `gemini` (`gemini-argon`, specialist worker)
- **Date:** `2026-11-11`
- **Rulings in force:**
  - Chief (Grok) single ruling: [PR #180 comment 6799165375](https://github.com/TheLaughingGod1986/history-of-science/pull/180#issuecomment-6799165375) (`11 Nov 14:56Z`), replacing conflicting parts of [6798928858](https://github.com/TheLaughingGod1986/history-of-science/pull/180#issuecomment-6798928858) (`11 Nov 14:46Z`), plus [6799137892](https://github.com/TheLaughingGod1986/history-of-science/pull/180#issuecomment-6799137892) (`11 Nov 14:54Z`)
  - Queue/runner rulings: [6799526318](https://github.com/TheLaughingGod1986/history-of-science/pull/180#issuecomment-6799526318), [6799192880](https://github.com/TheLaughingGod1986/history-of-science/pull/180#issuecomment-6799192880), [6799192687](https://github.com/TheLaughingGod1986/history-of-science/pull/180#issuecomment-6799192687)
- **Machine-readable evidence:** `02_Video-Projects/009_The-Falling-Moon-Gravity/07_Edit-Project/J2629_THIRD_TAKES_SHEETS_EVIDENCE_2026-11-11.json`
- **Full-clip `0.5 s` sheets beside `START_FRAME`:** `02_Video-Projects/009_The-Falling-Moon-Gravity/07_Edit-Project/review_J2629_sheets/`

---

## 1. Summary Table

| Order | Shot | Take | Clip SHA-256 | Board Window | Q1 | Q2 | Q3 | Outcome |
|---:|---|---:|---|---|---|---|---|---|
| 1 | `P03:01_really_falling_c1` | 3 | `cef66d0f83a641ce7ff3c5c16f08d3daf6d67cc2e2f29d496fa74d70cd51b124` | `0.00–5.26 s` | **YES** (`f000–f189`) | **NO** (`f012–f189`: dark grey ball forms at curve tip `f012–f036`; golden curve bends back & loops overhead `f036–f189`) | **YES** (`f000–f189`) | **`FAIL / PARKED`** (no take 4; stretch of take 2's first second withdrawn per `6799165375`) |
| 2 | `P04:05_minute_second_c1` | 3 | `ae8f6dc6bd72bb6316b9ea67fedc69947261783ef17040a7f0cc22c240a8c05c` | `0.00–6.76 s` | **YES** (`f000–f189`) | **NO** (`f073–f102`: second apple bounces ~80 px back up at `f073–f084`, morphs green→red `f074–f078`, drops a second time `f084–f094`; 2 apples at end `f096–f189`) | **NO** (`f012–f189` Moon reverses backward along arc across whole clip; `f073–f084` & `f096–f101` second apple bounces upward) | **`FAIL / PARKED`** (no take 4; goes to edit-side option Chief brings Grok; `c2` not made) |

---

## 2. Per-Shot Yes/No Answers with Frames

### 1. `P03:01_really_falling_c1` (`take 3`, `01_really_falling_c1_t3.mp4`)
- **Clip SHA-256:** `cef66d0f83a641ce7ff3c5c16f08d3daf6d67cc2e2f29d496fa74d70cd51b124`
- **Start frame:** `01_really_falling_c1_from_01_really_falling.png` (`sha256: 977108833c437f925fe07778ab2efeaeb92b11c2f62e9446016a2617fb82a058`, identical to take 2)
- **Board window:** `0.00–5.26 s` (full clip `0.00–7.88 s` / `f000–f189`)
- **Sheet:** `02_Video-Projects/009_The-Falling-Moon-Gravity/07_Edit-Project/review_J2629_sheets/P03_01_really_falling_c1_t3_sheet.jpg` (`sha256: 193edd250fae602c87d3e7bf1c691becd58e26668fcd21a23ac6f3b13935e072`)
1. **(1) the same Moon is in the sky in every frame and never fades, changes size or colour, or leaves:**
   - **YES (`START_FRAME` and `t=00.00s (f000)` through `t=05.26s (f126) [USE_END]` and `t=07.88s (f189) [CLIP_END]`).** The original warm cream-gold full Moon with lunar maria remains in the sky above the orchard in every frame (`f000–f189`, centroid `x≈494.2–498.3, y≈267.6–268.7`) at constant size, brightness and colour; it never fades or leaves.
2. **(2) the single golden curve never bends back, loops, wraps around or crosses the Moon, and no second line or object appears:**
   - **NO (`t=00.50s–01.00s (f012–f024)` through `t=05.26s (f126) [USE_END]` and `t=07.88s (f189) [CLIP_END]`).**
     - **Second object appears (`f012–f189`):** a dark grey sphere/ball begins forming at the upper-right tip of the golden curve at `t=00.50s–00.75s (f012–f018, x≈841, y≈213–206)`, becomes a solid dark grey sphere by `t=01.00s–01.50s (f024–f036, x≈848–853, y≈194–161)`, and rides the tip of the curve through `t=05.26s (f126) [USE_END]` and `t=07.88s (f189) [CLIP_END]`.
     - **Golden curve bends back and loops (`f036–f189`):** starting at `t=01.50s–02.00s (f036–f048)`, the upper-right tip of the single golden curve hooks upward and bends backward (leftward) across the sky above the orchard in a wide overhead C-loop (`x≈853` at `f030` → `x≈833` at `f048` → `x≈728, y≈85` at `f096` → `x≈671, y≈111` at `f126 [USE_END]`), then loops downward toward the upper-right rim of the Moon across `t=05.50s–07.88s (f132–f189, reaching x≈613, y≈219 at f189)`.
3. **(3) the Moon's face carries no mark:**
   - **YES (`START_FRAME` and `t=00.00s (f000)` through `t=05.26s (f126) [USE_END]` and `t=07.88s (f189) [CLIP_END]`).** The bright cream-gold Moon's face carries only its natural lunar maria from `START_FRAME` across all frames `f000–f189`, with no mark or line crossing its disc.
- **Outcome:** **`FAIL / PARKED`** (per Chief Grok's single ruling `6799165375`: there is no take 4; `P03:01_really_falling_c1` is **parked**, and the stretch of take 2's first second is withdrawn).

---

### 2. `P04:05_minute_second_c1` (`take 3`, `05_minute_second_c1_t3.mp4`)
- **Clip SHA-256:** `ae8f6dc6bd72bb6316b9ea67fedc69947261783ef17040a7f0cc22c240a8c05c`
- **Start frame:** `05_minute_second_c1_from_05_minute_second.png` (`sha256: 973543d2e8129dfe3ba30a188b90237dd53a936fd5f3c5bc18d31a6137f9c342`, identical to take 2)
- **Board window:** `0.00–6.76 s` (full clip `0.00–7.88 s` / `f000–f189`)
- **Sheet:** `02_Video-Projects/009_The-Falling-Moon-Gravity/07_Edit-Project/review_J2629_sheets/P04_05_minute_second_c1_t3_sheet.jpg` (`sha256: c9ee75abd3aede6ba88c3e624855a30d19dec1f75c4d7a024c2a3b45892a4d06`)
1. **(1) on the left, the apple at the foot of the ruler never moves or rolls:**
   - **YES (`START_FRAME` and `t=00.00s (f000)` through `t=06.76s (f162) [USE_END]` and `t=07.88s (f189) [CLIP_END]`).** The original green apple sitting on the wooden table to the right of the ruler's base (`x≈529.5–532.2, y≈569.6–572.0`) stays in its spot across the entire clip (`f000–f189`) and never moves or rolls.
2. **(2) a second apple drops once from beside the top of the ruler, and there are exactly two apples on the left at the end:**
   - **NO (`t=03.04s–04.25s / f073–f102` for the upward bounce, green→red colour morph, and second drop; YES that there are two apples on the left at the end from `t=04.00s / f096` through `t=06.76s / f162 [USE_END]` and `t=07.88s / f189 [CLIP_END]`).** A second green apple enters beside the top of the ruler at `t=00.00s–00.50s (f000–f012)` and drops to touch the wooden base of the ruler at `t=02.88s–03.00s (f069–f072, y_mean≈560)`. Instead of dropping once and staying down, it **bounces ~80 px back up into the air** from `t=03.04s (f073)` to `t=03.46s–03.50s (f083–f084, y_mean≈480.6 — clearly suspended in mid-air on tile `t=03.50s (f084)`)` while morphing from green to **bright red** (`f074–f078`), then **drops a second time** onto the ruler's base (`t=03.50s–03.92s / f084–f094`) with a small second settle (`f096–f104`), leaving **two apples** on the left at the end (`f096–f189`: one red apple on the ruler's base, one green apple beside it on the table).
3. **(3) nothing moves upward, there is no apple on the right, the Moon keeps moving forward and never reverses, and no second bright arc appears over the Earth:**
   - **NO (`t=00.50s (f012)` through `t=06.76s (f162) [USE_END]` and `t=07.88s (f189) [CLIP_END]` for Moon reversal; `t=03.04s–03.50s (f073–f084)` and `t=04.00s–04.21s (f096–f101)` for upward apple bounce).**
     - **Nothing moves upward — NO (`f073–f084` and `f096–f101`):** after touching the ruler's base at `t=02.88s–03.00s (f069–f072)`, the second apple bounces upward ~80 px into the air through `t=03.46s–03.50s (f083–f084)` (while changing colour from green to red in `f074–f078`), plus a smaller upward rebound at `f096–f101`.
     - **There is no apple on the right — YES (`f000–f189`):** no apple appears on the right half of the split screen.
     - **The Moon keeps moving forward and never reverses — NO (`f012–f189`, including `f162 [USE_END]`):** in the parent shot (`05_minute_second_t1.mp4`), the Moon moved forward (up and rightward along the golden orbital curve from `x≈987, y≈269` at `f000` to `x≈1151, y≈211` at `START_FRAME`). In `c1` take 3, starting immediately at `t=00.50s (f012)` and continuing across the entire clip through `t=06.76s (f162) [USE_END]` and `t=07.88s (f189) [CLIP_END]`, the Moon **reverses direction** and slides backward (leftward and downward) along the golden curve (`x≈1151.1, y≈211.3` at `f000` → `x≈1118.1, y≈218.5` at `t=03.00s / f072` → `x≈1053.1, y≈225.8` at `t=06.76s / f162 [USE_END]` → `x≈996.8, y≈227.6` at `t=07.88s / f189 [CLIP_END]`), leaving the bare upper-right tip of the golden curve protruding past the Moon from `t=01.00s (f024)` onward.
     - **No second bright arc appears over the Earth — YES (`f000–f189`):** only the single golden orbital curve is present over the Earth.
- **Outcome:** **`FAIL / PARKED`** (per Chief Grok's single ruling `6799165375`: there is no take 4; `P04:05_minute_second_c1` goes to an edit-side option the Chief brings Grok, and `P04:05_minute_second_c2` is **not made**).
