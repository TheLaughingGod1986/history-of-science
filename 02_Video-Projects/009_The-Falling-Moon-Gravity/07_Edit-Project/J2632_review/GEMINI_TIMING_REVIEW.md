### J2632 Revised Render Timing Advisory (`01_really_falling_c1`)

**Verdict:** **BLOCKED / CONTRADICTION FLAGGED (Do Not Pass Join)** — Phrase-to-motion alignment at `183.94s–189.20s` and internal geometry checks pass, but the **21-frame (`30 fps`) graphic head cannot cover the 21-frame (`24 fps`) parent trim**, leaving an unresolved **`0.175s` clock mismatch** (or **`0.375s–0.425s`** if crossfaded over parent frames `99–104`) under the no-hold, no-retime, no-extra-frames, no-splice constraint. Chief owns `KEEP` and must reconcile the clocks.

---

### 1. Timing & Clock-Mismatch Calculations

* **Revised Graphic (`30 fps`):**
  * Total decoded frames: $179\text{ unique frames}$ ($\text{frames } 0\text{–}178$), encoded duration $= \frac{179}{30} = 5.966667\text{ s}$ (nominal edit duration $= 5.96\text{ s}$; last frame $178$ at $5.933333\text{ s}$).
  * Tangent-draw head (`frames 0–20`): $21\text{ frames at } 30\text{ fps} = \frac{21}{30} = \mathbf{0.700\text{ s}}$.
  * Orbital motion (`frames 21–178`, old `f0` $\rightarrow$ new `f21`): $158\text{ frames at } 30\text{ fps} = \frac{158}{30} = \mathbf{5.266667\text{ s}}$ (nominal $5.26\text{ s}$).
  * Locked timeline placement: Motion `[f21..f178]` spans $\mathbf{183.94\text{ s} \rightarrow 189.20\text{ s}}$; graphic start (`f0`) lands at $183.94 - 0.700 = \mathbf{183.240\text{ s}}$.

* **Parent Cut (`01_really_falling_t1.mp4` at `24 fps`):**
  * Planned out: $\text{frame } 125$ ($\frac{125}{24} = 5.208333\text{ s}$), aligned to film $\mathbf{183.940\text{ s}}$.
  * Chief required earlier out: $\text{frame } 104$ ($\frac{104}{24} = 4.333333\text{ s}$), excluding $\text{frames } 108, 112, 125$.
  * Parent cut delta: $125 - 104 = 21\text{ frames at } 24\text{ fps} = \frac{21}{24} = \mathbf{0.875\text{ s}}$ earlier, placing parent `f104` at $183.940 - 0.875 = \mathbf{183.065\text{ s}}$.

* **Explicit Contradictions:**
  1. **Butt-Join Clock Mismatch (`0.175s` shortfall):**
     $$\Delta t_{\text{parent}} - \Delta t_{\text{head}} = 0.875\text{ s} - 0.700\text{ s} = \mathbf{0.175\text{ s}} \quad (4.2\text{ frames at } 24\text{ fps} \text{ or } 5.25\text{ frames at } 30\text{ fps})$$
     * Holding motion at `183.94s` and end at `189.20s` leaves an uncovered **$0.175\text{ s}$ gap** (`183.065s` to `183.240s`).
     * Pulling the graphic back to `183.065s` shifts motion start $0.175\text{ s}$ early to `183.765s` (breaking narration lock) and ends the graphic at `189.025s` (leaving a $0.175\text{ s}$ gap before `189.20s`).
  2. **Crossfade Overlap Contradiction (`f99–f104` / `0.20s` fade):**
     * Parent frames `99–104` span $5\text{ intervals} = \frac{5}{24} = 0.208333\text{ s}$ ($f_{99}$ at $4.125\text{ s}$ to $f_{104}$ at $4.333333\text{ s}$) or $6\text{ inclusive frames} = \frac{6}{24} = 0.250\text{ s}$.
     * If executed as an overlapping **dissolve/crossfade** where the graphic begins fading in over parent `f99`, the overlap consumes an additional $0.200\text{–}0.250\text{ s}$ of graphic head frames, expanding the total shortfall between parent `f99` and motion start `183.94s` to:
       * **$0.875 + 0.200 - 0.700 = \mathbf{0.375\text{ s}}$** ($11.25\text{ graphic frames at } 30\text{ fps}$), or
       * **$\frac{26}{24} - 0.700 = \mathbf{0.3833\text{ s}}$** ($11.5\text{ frames at } 30\text{ fps}$) / **$\frac{27}{24} - 0.700 = \mathbf{0.425\text{ s}}$** ($12.75\text{ frames at } 30\text{ fps}$).
     * Even if `f99–f104` is a non-overlapping parent fade-out ending on `f104`, the **$0.175\text{ s}$** butt-join gap remains.

---

### 2. Narration-to-Motion Alignment Check (at `film_motion_start_s = 183.94s`)

Mapping `f21` (`render_local_s = 0.70s`, `motion_local_s = 0.00s`) to `183.94s` preserves the exact `film_s` coordinates of the original 158-frame motion curve:

| Film Time (`film_s`) | Render / Motion Local (`s`) | Narration Event (`VO_RETIME_v01.json`) | Moon Center `(x, y)` px | Gap Below `y=160` Tangent (`px`) | Fit Assessment |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **`183.24`** | `0.00` / `-0.70` | Mid-Sentence 2 (*"...held [183.12] **up** [183.34] at [183.56] all, [183.70]"*) | `(560.00, 160.00)` | `0.00` | Tangent draws in over 21 frames (`0.70s`) during sentence tail & pause |
| **`183.94`** | `0.70` / `0.00` | Pre-Sentence 3 pause (`0.58s` before *"It"*) | `(560.00, 160.00)` | `0.00` | Clockwise orbital motion begins (`f21`) |
| **`184.52`** | `1.28` / `0.58` | **"It"** onset (*"It really is falling."*) | `(656.70, 166.52)` | **`6.52`** | Exceeds `5px` arc / `4px` tangent strokes at phrase onset |
| **`185.34`** | `2.10` / `1.40` | **"falling,"** onset | `(790.02, 197.73)` | **`37.73`** | Clear downward deflection during key verb |
| **`185.86`** | `2.62` / `1.92` | End of *"It really is falling."* | `(870.55, 230.42)` | **`70.42`** | Gap grows $+63.90\text{ px}$ across phrase ($>1.23\times$ Moon radius $57\text{ px}$) |
| **`186.50`** | `3.26` / `2.56` | **"It"** onset (*"It just never lands."*) | `(963.33, 283.57)` | **`123.57`** | Large separation established at sentence start |
| **`187.32`** | `4.08` / `3.38` | **"lands."** onset | `(1068.95, 370.71)` | **`210.71`** | Constant surface clearance to Earth $= 513\text{ px}$ |
| **`187.82`** | `4.58` / `3.88` | End of *"It just never lands."* | `(1124.53, 433.12)` | **`273.12`** | Well clear of Earth and frame boundaries |
| **`189.173`** | `5.933` / `5.233` | Last frame `f178` (cut to Cannon `f0` at **"To"** `189.20s`) | `(1235.04, 629.56)` | **`469.56`** | $513\text{ px}$ from Earth; $627.96\text{ px}$ from right edge; $393.44\text{ px}$ from bottom |

* **Confirmation:** When mapped to `183.94s`, the original motion gap still fits both phrases cleanly.

---

### 3. Limitations

* **Text-only review:** Evaluated strictly from the supplied manifest, boundary metadata, and historical `faster-whisper` timestamps (`VO_RETIME_v01.json`); no files, audio, or video frames were accessed, listened to, or watched.
* **No assembled join:** Boundary entries are isolated source samples only; no rendered transition between parent `f99–f104`, graphic `f0–f178`, and `02_cannon_world_t1.mp4` exists yet.

---

### 4. Needed Chief Decision

To reconcile the `24 fps` parent cut at `f104` (`183.065s`) with the `30 fps` graphic while preserving motion lock at `183.94s–189.20s` and no holds/retimes, Chief must authorize **one** of the following:
1. **Re-render the `30 fps` graphic with a longer drawn tangent lead-in:**
   * **Butt join after parent fade-out on `f99–f104`:** Requires **$26\text{–}27\text{ head frames}$** at $30\text{ fps}$ ($0.8667\text{–}0.9000\text{ s}$ vs $0.875\text{ s}$ exact; total $184\text{–}185\text{ frames}$) so graphic `f0` starts at `183.065s` and motion `f_motion` still starts at `183.94s`.
   * **Overlapping crossfade across parent `f99–f104` (`0.20s` / `5–6 parent frames`):** Requires **$32\text{–}34\text{ head frames}$** at $30\text{ fps}$ ($1.0667\text{–}1.1333\text{ s}$; total $190\text{–}192\text{ frames}$) to cover both the $0.875\text{ s}$ earlier cut and the $0.200\text{–}0.250\text{ s}$ crossfade overlap before `183.94s`.
2. **Or adjust the parent out-point to match the existing 21-frame (`0.700s`) head:**
   * A $0.700\text{ s}$ trim at $24\text{ fps}$ is $16.8\text{ frames}$ (parent `f108` $= 0.7083\text{ s}$), **not** `f104` — which conflicts with Chief's exclusion of `f108`.
