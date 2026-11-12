**Mode & Scope Declaration:** This is a **text-only check** based solely on the supplied render manifest, Chief ruling `6801512032`, and Scribe word timestamps (`a5a07a83...`). It involves **no audio listening and no visual/motion perception**. This review is **advisory only**; **Grok decides KEEP**, and no Chief approval is issued here.

---

### 1. Boundary & Edit Safety Analysis

* **Part & Timeline Alignment (`PASS`):**
  * **Local `0.00s` = Film `319.63s`** (`57.57s` into `part04` starting at `262.06s`). Matches manifest `film_start_s: 319.63`.
  * **Internal Cut (`6.76s` local = Film `326.39s`):** Matches manifest `internal_cut_s: 326.39`.
  * **Edit Exit (`13.51s` local = Film `333.14s`):** Matches manifest `film_end_s: 333.14` and `nominal_edit_duration_s: 13.51`.
  * **Frame & Duration Pad (`PASS`):** `406` source frames at `30 fps` (`0..405`) yield `13.5333s`, covering the `13.51s` edit cleanly with a `+0.0233s` (`~0.7` frame) safety pad at the tail.
* **Entry Boundary (`0.00s` local) (`PASS`):**
  * Preceding word `"is"` ends at `-0.13s`; first in-graphic word `"3,600"` starts at `+0.13s`.
  * Local zero lands in the exact center of a `0.26s` silence gap (`-0.13s` to `+0.13s`). Zero word clipping.
* **Internal Cut Boundary (`6.76s` local) (`PASS with note`):**
  * Visually, `6.76s` sits in the `1.00s` label-free gap between `"1 MINUTE"` (`end_s: 5.85`) and `"5 m"` / bracket draw (`start_s: 6.85`), with `no_splice: true` preserving continuous motion.
  * Acoustically, `6.76s` falls mid-word inside `"distance,"` (`6.35s–6.949s`). Because `no_splice: true` means the graphic does not hard-cut visually at `6.76s`, this mid-word timestamp causes no visual/audio clash, and the `6.85s` bracket/label onset initiates `0.099s` before `"distance,"` finishes (`6.949s`).
* **Exit Boundary (`13.51s` local) (`PASS`):**
  * Final spoken word `"moon."` ends at `12.77s`, leaving `0.74s` of clean tail hold before the `13.51s` edit cut (and `0.763s` before `13.5333s` file EOF).

---

### 2. Label Windows, Fades, Action & Scribe Correspondence

All four labels obey the **one-label-at-a-time** rule (`geometry_checks.one_label_at_a_time: true`) and clear at `10.40s`. With `0.40s` fade-in and `0.40s` fade-out inside each window:

| Element / Label | Local Window (s) | Fade-In / Full Hold / Fade-Out (s) | Gap to Next (s) | Scribe Words in Window & Correspondence |
| :--- | :--- | :--- | :--- | :--- |
| **Dot Drop** | `0.45 – 1.45` | *(Motion: `1.00s` drop)* | — | Runs across `"3,600"` (`0.13–1.45s`), landing at `1.45s` right at the end of `"3,600"`. |
| **`1 SECOND`** | `0.40 – 2.80` | `0.40–0.80` / `0.80–2.40` (`1.60s`) / `2.40–2.80` | `0.30s` (`2.80–3.10`) | **Anaphoric Reference (`PASS`):** Names the apple drop already spoken in the parent shot (*"In one second, an apple falls about five meters"*, `-6.57s` to `-2.51s`) while narration bridges via *"3,600 times weaker"* (`0.13–2.37s`). Clears at `2.80s` before `"then"` (`2.91s`). |
| **`1 MINUTE`** | `3.10 – 5.85` | `3.10–3.50` / `3.50–5.45` (`1.95s`) / `5.45–5.85` | `1.00s` (`5.85–6.85`) | **Direct Spoken Match (`PASS`):** Fades in during `"in"` (`3.05–3.25s`) and `"one"` (`3.31–3.55s`), reaches full opacity (`3.50s`) just before `"minute,"` (`3.65–4.05s`), holds through *"the moon should fall about"* (`4.41–5.75s`), and finishes fading out at `5.85s` during `"the"` (`5.77–5.89s`). |
| **Brackets Draw** | `6.85 – 7.25` *(stays)* | *(Draws `0.40s`, locks at `7.25s`)* | — | Draws across the tail of `"distance,"` (`6.35–6.949s`) and the subsequent pause, locking at `7.25s` (`0.059s` before `"five"` at `7.309s`). |
| **`5 m`** | `6.85 – 8.85` | `6.85–7.25` / `7.25–8.45` (`1.20s`) / `8.45–8.85` | `0.15s` (`8.85–9.00`) | **Direct Spoken Match (`PASS`):** Fades in with the brackets (`6.85–7.25s`), reaching full opacity `0.059s` before `"five"` (`7.309–7.57s`) and holding through `"meters,"` (`7.69–8.15s`). Fades out (`8.45–8.85s`) over `"along"` (`8.57–8.79s`). |
| **`TWO STOREYS HIGH`** | `9.00 – 10.40` | `9.00–9.40` / `9.40–10.00` (`0.60s`) / `10.00–10.40` | `3.11s` to exit (`10.40–13.51`) | **Chief-Approved Scale Label (`PASS`):** Runs over `"its"` (`8.85–9.05s`), `"curve."` (`9.11–9.57s`), and the `0.88s` sentence pause (`9.57–10.45s`). Clears at `10.40s`, `0.05s` before `"Newton"` (`10.45s`). *(See Section 3).* |
| **Post-Label Hold** | `10.40 – 13.51` | *(Brackets stay; Moon continues)* | — | Covers *"Newton checked it against the real moon."* (`10.45–12.77s`) plus `0.74s` silent pad to `13.51s`. |

---

### 3. Distinction: Chief-Approved Scale Label vs. Spoken Narration

* **`"TWO STOREYS HIGH"` (`9.00–10.40s`) is an approved visual scale gloss, not a missing spoken phrase:**
  * Scribe narration at `7.309–9.57s` says: *"...five meters, along its curve."*
  * While the `5 m` brackets (`[300, 690]` px) remain locked on screen, `"TWO STOREYS HIGH"` replaces `"5 m"` at `9.00s` to give the viewer a concrete physical scale equivalent during the completion of *"along its curve"* (`9.11–9.57s`) and the natural breath pause (`9.57–10.45s`) before *"Newton checked it against the real moon."*
  * **No narration rewrite is required or recommended.**

---

### 4. Conflicts & Limits

* **Conflicts:** **None (`0` blocking conflicts).** All manifest numbers, label windows, bracket draw timings, film/local offsets, and Scribe alignments match Chief ruling `6801512032`.
* **Minor Timing Notes (Non-blocking):**
  1. **`"TWO STOREYS HIGH"` Full-Opacity Hold (`0.60s`):** Within the `1.40s` window (`9.00–10.40s`), subtracting `0.40s` fade-in and `0.40s` fade-out leaves `0.60s` (`18` frames) at `100%` opacity (`9.40–10.00s`), though legibility spans `~1.0s+` across mid-fades and sits cleanly inside the `9.57–10.45s` speech pause.
  2. **Clearance Before `"Newton"` (`0.05s`):** `"TWO STOREYS HIGH"` ends at `10.40s` and `"Newton"` begins at `10.45s` (`1.5` frames margin)—tight but clean, with zero overlap.
  3. **Internal Cut Marker (`6.76s`) vs. `"distance,"` (`6.35–6.949s`):** Safe as long as `no_splice: true` holds (no visual cut at `6.76s`); if the edit were ever split into separate visual plates at `6.76s`, that cut would fall `0.19s` before the end of `"distance,"`.
* **Limits of This Check:**
  * Text-and-timestamp verification only. This check cannot verify rendered font rendering, actual alpha-fade curves in the `.mp4`, visual absence of an Earth limb on the canvas, dot drop trajectory (`0.45–1.45s`), or continuous down-and-right Moon motion except via the reported manifest flags (`all_406_frames_monotone: true`, `left_landed_once: true`, `one_label_at_a_time: true`).

---

### 5. Concrete Timing Verdict

* **Verdict:** **TIMING PASS (Advisory — Grok decides KEEP).**
* Entry (`0.00s`), internal cut (`6.76s` under `no_splice: true`), and exit (`13.51s` within `13.5333s` / `406f` source) are boundary-safe, all four label windows (`0.40–2.80`, `3.10–5.85`, `6.85–8.85`, `9.00–10.40`) and bracket draws (`6.85–7.25`) align cleanly with Scribe word timings, and `"TWO STOREYS HIGH"` functions properly as a Chief-approved scale label without narration changes.
