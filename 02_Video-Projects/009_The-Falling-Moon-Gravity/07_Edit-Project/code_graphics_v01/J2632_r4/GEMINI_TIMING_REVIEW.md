### J2632 r4 Independent Timing Advisory (Text-Only)

**Status:** R3 `0.175 s` head/cut and fade contradictions are **resolved** within Chief ruling `6807936928` (`< 10 ms` nearest-frame snap tolerance). **No assembled join exists.** **KEEP and splice remain prohibited** pending Claude sheet read and Chief KEEP/splice authorization.

---

### 1. Core Timing & Reconciliation Calculations

* **Frame & Duration Accounting (30 fps graphic):**
  * Total frames: $190\text{ unique frames}$ ($f_0\text{–}f_{189}$) $= \frac{190}{30} = 6.333333\text{ s}$ encoded duration.
  * Prepended head: $32\text{ frames}$ ($f_0\text{–}f_{31}$) $= \frac{32}{30} = 1.066667\text{ s}$.
  * Preserved motion: $190 - 32 = 158\text{ frames}$ ($f_{32}\text{–}f_{189}$) $= \frac{158}{30} = 5.266667\text{ s}$.
* **Film Timeline Pinning:**
  * Motion start ($f_{32}$, original motion $f_0$): pinned at $183.94\text{ s}$ (`render_local_s` $= 1.066667\text{ s}$).
  * Graphic start ($f_0$): $183.94 - 1.066667 = 182.873333\text{ s}$.
  * Fade window ($f_0\text{–}f_5$, 6 frame durations at 30 fps):
    $$\Delta t_{\text{fade}} = \frac{6}{30} = 0.200\text{ s} \implies 182.873333\text{ s} \text{ to } 183.073333\text{ s}$$
  * Graphic-only head lead ($f_6\text{–}f_{31}$, 26 frame durations at 30 fps):
    $$\Delta t_{\text{lead}} = \frac{26}{30} = 0.866667\text{ s} \implies 183.073333\text{ s} \text{ to } 183.94\text{ s}$$
  * Graphic last frame onset ($f_{189}$, `render_local_s` $= \frac{189}{30} = 6.300\text{ s}$):
    $$182.873333 + 6.300 = 189.173333\text{ s}$$
  * Nominal vs. encoded end:
    * Nominal edit end: $189.20\text{ s}$ ($\text{duration} = 189.20 - 182.873333 = 6.326667\text{ s}$).
    * Encoded end ($f_{189}$ end): $182.873333 + 6.333333 = 189.206667\text{ s}$ ($+6.67\text{ ms}$ past $189.20\text{ s}$, within $< 10\text{ ms}$ snap).
* **Parent Cut & R3 Contradiction Resolution (24 fps parent vs. 30 fps graphic):**
  * Parent pullback ($f_{125} \to f_{104}$ at 24 fps):
    $$\Delta t_{\text{parent}} = \frac{125 - 104}{24} = \frac{21}{24} = 0.875\text{ s} \quad (5.208333\text{ s} \to 4.333333\text{ s}\text{ source time})$$
  * Target parent out on film timeline:
    $$183.94 - 0.875 = 183.065\text{ s}$$
  * Residual between 30 fps fade end and 24 fps parent out target:
    $$183.073333\text{ s} - 183.065\text{ s} = +0.008333\text{ s} \text{ } (8.33\text{ ms} = \tfrac{1}{120}\text{ s})$$
  * **Assessment:** Because $1.066667\text{ s}\text{ (head)} = 0.200\text{ s}\text{ (fade)} + 0.866667\text{ s}\text{ (lead)}$, the prior r3 $0.175\text{ s}$ mismatch between the parent pullback and graphic head/fade is eliminated, leaving an $8.33\text{ ms}$ cross-rate grid residual that is $< 10\text{ ms}$ as permitted by Chief ruling `6807936928`.

---

### 2. ASR & Motion Sample Alignment Verification

All supplied `timing_samples` preserve the exact post-$183.94\text{ s}$ motion trajectory and ASR word-onset sync:
* **Head / Fade ($182.873333\text{ s–}183.94\text{ s}$):** Fade ($182.873333\text{ s–}183.073333\text{ s}$) lands between supplied ASR word onsets `"isn't"` ($182.76\text{ s}$) and `"held"` ($183.12\text{ s}$); tangent-draw head ($f_6\text{–}f_{31}$) spans `"held up at all,"` ($183.12\text{ s–}183.70\text{ s}$).
* **Motion Start ($f_{32}$):** `motion_local_s = 0` $\to$ `render_local_s = 1.066667 s` $\to$ `film_s = 183.94 s` (`gap = 0.0 px`).
* **Key Verbal Anchors:**
  * `"it"` ($184.52\text{ s}$): `motion_local_s = 0.58 s`, `render_local_s = 1.646667 s` (`gap = 6.52 px`).
  * `"falling,"` ($185.34\text{ s}$): `motion_local_s = 1.40 s`, `render_local_s = 2.466667 s` (`gap = 37.73 px`).
  * `"it"` ($186.50\text{ s}$): `motion_local_s = 2.56 s`, `render_local_s = 3.626667 s` (`gap = 123.57 px`).
  * `"lands."` ($187.32\text{ s}$): `motion_local_s = 3.38 s`, `render_local_s = 4.446667 s` (`gap = 210.71 px`).
  * `"To"` ($189.20\text{ s}$): $0.026667\text{ s}$ after $f_{189}$ onset ($189.173333\text{ s}$) and $-0.006667\text{ s}$ before encoded end ($189.206667\text{ s}$).

---

### 3. Concrete Assembly Nuances to Flag (Non-Blocking Under `< 10 ms` Snap)

1. **24 fps vs. 30 fps Six-Frame Fade Indexing (`f99–f104` vs. `f0–f5`):**
   * On the 30 fps graphic, 6 frame durations ($f_0\text{–}f_5$) equal $\frac{6}{30} = 0.200\text{ s}$.
   * On the 24 fps parent, the 6 frame indices $f_{99}\text{–}f_{104}$ span $\frac{104 - 99}{24} = \frac{5}{24} = 0.208333\text{ s}$ onset-to-onset ($4.125\text{ s}$ to $4.333333\text{ s}$, matching the $+8.33\text{ ms}$ residual), whereas 6 full 24 fps frame durations ($f_{99}$ onset to $f_{104}$ end at $4.375\text{ s}$) would equal $\frac{6}{24} = 0.250\text{ s}$ ($50\text{ ms}$ longer than $0.200\text{ s}$).
   * **Assembly requirement:** When an edit join is eventually authorized, the 30 fps fade ($182.873333\text{ s–}183.073333\text{ s}$) must map onto parent frames $f_{99}\text{–}f_{104}$ with $f_{104}$ as the final visible parent frame (snapping the $8.33\text{ ms}$ delta) and must not extend to $0.250\text{ s}$ or expose parent $f_{105+}$ ($f_{108}\text{–}f_{125}$ remain strictly excluded).
2. **Tail Trim at $189.20\text{ s}$:**
   * Encoded clip end is $189.206667\text{ s}$ ($+6.67\text{ ms}$ past nominal $189.20\text{ s}$); assembly must snap/cut cleanly at the $189.20\text{ s}$ boundary into `02_cannon_world_t1.mp4` $f_0$.

---

### 4. Limits of This Advisory

* Derived strictly from the supplied r4 manifest JSON and existing ASR text timestamps; no tools were run, no files were read or modified, and no audio or video motion was inspected.
* Source boundary entries in the manifest represent unjoined source frames only; **no assembled join exists**, and **KEEP / splice remain prohibited** until Chief issues approval.
