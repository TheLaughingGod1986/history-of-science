**Scope Note:** Text-only timing review of the supplied brief and Scribe SRT. **No audio/motion review** was performed (and no exact word timestamps are invented from grouped subtitles).

---

### 1. Timebase Conversion (`Part04 start = 262.06 s`, `Graphic start = 319.63 s`)

| Scribe SRT (Part04) | Film Time (s) | Graphic Local (s) | Subtitle Text |
| :--- | :--- | :--- | :--- |
| `49.240–53.080` | `311.30–315.14` | `-8.33 to -4.49` | *"beautiful part. In one second, an apple"* (in KEEP parent) |
| `53.220–56.420` | `315.28–318.48` | `-4.35 to -1.15` | *"falls about five meters. If the pull on"* (in KEEP parent) |
| `56.460–60.820` | `318.52–322.88` | `-1.11 to +3.25` | *"the moon is 3,600 times weaker, then in"* (graphic enters at `319.63 s` / `0.00 s` local) |
| `60.880–63.460` | `322.94–325.52` | `+3.31 to +5.89` | *"one minute, the moon should fall about the"* |
| `63.560–66.620` | `325.62–328.68` | `+5.99 to +9.05` | *"same distance, five meters, along its"* (**straddles `326.39 s` / `+6.76 s` local row cut**) |
| `66.680–67.140` | `328.74–329.20` | `+9.11 to +9.57` | *"curve."* |
| `68.020–70.340` | `330.08–332.40` | `+10.45 to +12.77` | *"Newton checked it against the real moon."* (graphic ends `333.14 s` / `+13.51 s` local) |

---

### 2. Does the Candidate Match Narration?

**No.** While the candidate satisfies the mechanical constraints (order `1 SECOND` → `1 MINUTE` → `5 m` → `TWO STOREYS HIGH`, `0.4 s` fades, no overlap, and all labels off at `6.40 s` local / `326.03 s` film before `326.39 s`), cramming all four labels into the first `6.40 s` causes every label after the recap anchor to fire **one cue early**:

1. **`1 SECOND` (`0.05–1.50 s` local / `319.68–321.13 s` film) + Left dot drop (`0.45–1.45 s` local / `320.08–321.08 s` film):**
   - Plays during *"the moon is 3,600 times weaker, then in"* (`318.52–322.88 s`). Because the spoken *"In one second, an apple falls about five meters"* (`311.30–318.48 s`) is carried by the preceding KEEP parent, this works only as an opening visual recap/baseline before `"one minute"` arrives.
2. **`1 MINUTE` (`1.60–3.10 s` local / `321.23–322.73 s` film) — Early Conflict:**
   - Plays and **fades completely out (`322.73 s`) before** the subtitle cue containing *"one minute, the moon should fall about the"* (`322.94–325.52 s` film / `3.31–5.89 s` local) even begins.
3. **`5 m` (`3.20–4.70 s` local / `322.83–324.33 s` film) + 300px brackets (`3.20–3.60 s` local / `322.83–323.23 s` film) — Early Conflict:**
   - Enters at `322.83 s` just as *"one minute, the moon should fall about the"* (`322.94–325.52 s`) starts, and **fades completely out (`324.33 s`) `1.29 s` before** the cue containing *"same distance, five meters, along its"* (`325.62–328.68 s` film / `5.99–9.05 s` local) begins.
4. **`TWO STOREYS HIGH` (`4.80–6.40 s` local / `324.43–326.03 s` film) — Early / Structural Conflict:**
   - Runs across the tail of *"one minute, the moon should fall about the"* and only the first `0.41 s` of *"same distance, five meters, along its"*, disappearing at `326.03 s` (`6.40 s` local) and leaving the entire second row (`326.39–333.14 s` / `6.76–13.51 s` local) bare.

---

### 3. Required Chief Clarification

The rule **"every label off before 326.39 and 333.14"** is ambiguous in a way that prevents honest VO timing if read as *"all four labels must finish before `326.39 s` (`6.76 s` local)"*:
- The cue *"one minute, the moon should fall about the"* spans `322.94–325.52 s` (`3.31–5.89 s` local).
- The cue *"same distance, five meters, along its"* spans `325.62–328.68 s` (`5.99–9.05 s` local), leaving only **`0.77 s`** (`5.99–6.76 s` local) before the `326.39 s` internal row cut.
- Because each label requires `0.4 s` fade-in + `0.4 s` fade-out (`>= 0.8 s` per label) with no overlap, **two labels (`5 m` and `TWO STOREYS HIGH`) cannot both fit after `"one minute..."` (`3.31–5.89 s` local) and before the `326.39 s` (`6.76 s` local) cut.**

**Clarification needed from Chief:**
Does *"every label off before 326.39 and 333.14"* mean:
- **(A) Boundary-clean cuts (honest VO sync):** No label may be active *across* either cut (`326.39 s` or `333.14 s`) — i.e., Row 1 labels (`1 SECOND`, `1 MINUTE`) must be off before `326.39 s` (`6.76 s` local), and Row 2 labels (`5 m`, `TWO STOREYS HIGH`) appear after `326.39 s` and are off before `333.14 s` (`13.51 s` local)?
- **(B) Strict Row-1-only labels:** All four labels must finish before `326.39 s` (`6.76 s` local), accepting that `5 m` and `TWO STOREYS HIGH` will pre-empt the spoken *"same distance, five meters"* cue?

---

### 4. Concrete Review Recommendation

**HOLD candidate pending Chief clarification on the `326.39 s` boundary rule, and adjust local windows (without touching cut, VO, or locked duration):**

1. **Recommended (Option A — Split across `326.39 s` / `6.76 s` local so labels match narration cues):**
   - **`1 SECOND`:** `0.40–2.80 s` local (`320.03–322.43 s` film) — pairs with the `320.08–321.08 s` left dot drop as the recap baseline during *"the moon is 3,600 times weaker, then in"*.
   - **`1 MINUTE`:** `3.35–5.85 s` local (`322.98–325.48 s` film) — stays within the `"one minute, the moon should fall about the"` cue (`3.31–5.89 s` local) and is **fully off `0.91 s` before the `326.39 s` (`6.76 s` local) cut**.
   - **Equal 300px brackets:** Shift from `322.83–323.23 s` (`3.20–3.60 s` local) into the `"same distance, five meters, along its"` cue (`5.99–9.05 s` local), e.g., `6.05–6.45 s` local (`325.68–326.08 s` film, finishing before the `6.76 s` cut) or `6.85–7.25 s` local (`326.48–326.88 s` film, right after the cut).
   - **`5 m`:** `6.85–8.85 s` local (`326.48–328.48 s` film) — opens cleanly after the `326.39 s` (`6.76 s` local) cut inside the `"same distance, five meters, along its"` cue (`5.99–9.05 s` local).
   - **`TWO STOREYS HIGH`:** `9.00–10.40 s` local (`328.63–330.03 s` film) — follows `5 m` over `"curve."` (`9.11–9.57 s` local) and finishes before `"Newton checked it against the real moon."` (`10.45–12.77 s` local), well before `333.14 s` (`13.51 s` local).

2. **Fallback (Option B — If Chief mandates all 4 labels must end before `326.39 s` / `6.76 s` local):**
   - At minimum, delay `1 MINUTE` so it is not gone before `"one minute"` is even spoken, and push `5 m` into the start of the `"same distance, five meters"` cue (`5.99 s` local) — though note that fitting both `5 m` and `TWO STOREYS HIGH` before `6.76 s` local with `0.4 s` fades still forces `5 m` to run ahead of `5.99 s` local (`e.g., 1 SECOND 0.30–1.90; 1 MINUTE 2.80–4.10; 5 m 4.20–5.40; TWO STOREYS HIGH 5.50–6.70`), which remains out of sync with the VO. Option A is strongly preferred for honest timing.
