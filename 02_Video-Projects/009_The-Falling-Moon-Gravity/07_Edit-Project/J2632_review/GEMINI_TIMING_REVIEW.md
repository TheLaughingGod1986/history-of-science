**Advisory Timing Review — J2632 (`183.94s`–`189.20s`, local `0.00s`–`5.26s`)**

### 1. Alignment & Motion Verification

* **Cut Boundaries & Source Duration (`0.00s` to `5.26s`):**
  * **In-point (`183.94s` / `local_s = 0.00s`):** Preceding sentence 2 (*"The Moon isn't held up at all."*) has its final word onset (`"all,"`) at `183.70s` (`local_s = -0.24s`) and sentence end at `184.10s` (`local_s = +0.16s`, ~5 frames into the clip), leaving a `0.42s` pause before sentence 3 begins at `local_s = 0.58s`.
  * **Out-point (`189.20s` / `local_s = 5.26s`):** Sentence 5 (*"To explain it..."*) begins cleanly at `189.20s` (`local_s = 5.26s`), matching the nominal `5.26s` edit duration. The 158-frame source at 30 fps (`5.2667s`, last sampled frame at `5.2333s`) covers the full `5.26s` span without requiring a freeze-pad.

* **Check 1 — Visible separation grows during *"It really is falling."* (`local_s = 0.58s` to `1.92s`):**
  * `"it"` onset (`0.58s`): Moon centre at `(656.70, 166.52)`, vertical drop below the `y = 160` tangent is **`6.52 px`**.
  * `"falling,"` onset (`1.40s`): Moon centre at `(790.02, 197.73)`, vertical drop below the tangent is **`37.73 px`**.
  * Phrase end (`1.92s`): Moon centre at `(870.55, 230.42)`, vertical drop below the tangent is **`70.42 px`**.
  * **Note on disc vs. centre separation:** Because the Moon radius is `57 px`, the Moon's top edge (`y - 57`) still overlaps the `y = 160` tangent line at `"it"` (`0.58s`) and at `"falling,"` onset (`1.40s`, overlapping by `19.27 px`), achieving full top-edge clearance (`gap > 57 px`) mid-word during `"falling,"` and reaching `13.42 px` of full-disc clearance by phrase end (`1.92s`). Centre-to-tangent vertical deflection grows continuously throughout (`6.52 px → 37.73 px → 70.42 px`).

* **Check 2 — Moon remains clear on *"It just never lands."* (`local_s = 2.56s` to `3.88s`, holding to `5.26s`):**
  * `"it"` onset (`2.56s`): Moon centre at `(963.33, 283.57)`, tangent drop **`123.57 px`** (top edge clear of tangent by `66.57 px`).
  * `"lands."` onset (`3.38s`): Moon centre at `(1068.95, 370.71)`, tangent drop **`210.71 px`** (top edge clear by `153.71 px`).
  * Phrase end (`3.88s`): Moon centre at `(1124.53, 433.12)`, tangent drop **`273.12 px`** (top edge clear by `216.12 px`).
  * Clip end (`5.233s`): Moon centre at `(1235.04, 629.56)`, tangent drop **`469.56 px`** (top edge clear by `412.56 px`).
  * **Earth & frame clearance:** On the circular arc of radius `720 px` around Earth `(560, 880)`, surface-to-surface clearance between the Moon (`r = 57 px`) and Earth (`r = 150 px`) remains a constant **`513 px`** (`720 - 150 - 57`), and the Moon stays well within standard `1920×1080` bounds (max `x + 57 ≈ 1292 px`, max `y + 57 ≈ 687 px`) with no labels to collide with.

---

### 2. Concrete Timing Conflicts

* **None critical.**
* **Minor geometric note (non-blocking):** Sentence 2's final word (`"all,"`) trails `0.16s` into the start of the clip (`local_s = 0.00s` to `0.16s`), and the Moon's upper limb (`r = 57 px`) does not fully detach below the `y = 160` horizontal tangent line until the middle of the word `"falling,"` (between `1.40s` and `1.92s`), although the centreline drop (`gap_below_tangent_px`) is already visibly increasing across the entire sentence (`6.52 px → 70.42 px`).

---

### 3. Limits & Advisory Verdict

* **Limits:** This review is strictly a numerical check of the supplied `VO_RETIME_v01.json` faster-whisper timestamps and coordinate samples; no audio listening, frame viewing, or motion perception was performed, and no tools or files were accessed.
* **Advisory Verdict:** **PASS (Advisory)** — Narration onsets and sentence windows align cleanly with the `183.94s–189.20s` (`5.26s` / 158-frame) candidate window, separation from the `y = 160` tangent grows continuously across *"It really is falling."*, and the Moon remains completely clear of both the tangent line and Earth across *"It just never lands."* through the `189.20s` cut. **Grok must approve the sheet before KEEP or splice.**
