# HOS 011 — Chief Price Pass Review v04 (`PRICE_REVIEW_v04.md`, `J3736`)

- **Film:** `011_Surgery-Before-Anaesthesia` (*Anesthesia: The Day Surgery Stopped Hurting*)
- **Authorising queue job:** `J3736` (queued by Acting Chief `gemini` in `J3734`, 25 Nov 2026)
- **Slotted air date:** **Thu 17 Dec 2026 18:00 London** (Ben watch **Mon 14 Dec 2026 18:00 London**; unified J3734 line-up)
- **Locked VO:** `02_Voiceover/hos_011_vo_v01.wav` (`532.720 s`, SHA-256 `d873f1d0c9158087fd61ce0b9f53de985055d778cd58b8df70c67c0701300ae2`; 0 new long VO credits needed)
- **Already built (£0):** All **26 free rows** (`13` code graphics + `13` archive composites) and timing rough `v11` (`hos_011_timing_rough_v11.mp4`) are built on `studio-live` (`J2563` / PR `#650`).
- **Authorization state:** `generation_authorized: false` across `PICTURE_PLAN_v04.json`, `parts/part-01_plates_v04.json`..`part-05_plates_v04.json`, and `PASS1_SCOPE_J3736.json`. **£0 / 0 credits spent in J3736.**

---

## 1. Live Flow Credit Balance & Shared Accounting (as of 25 Nov 2026)

| Metric | Value | Source |
|---|---:|---|
| Latest recorded Flow balance (studio Ultra account, CDP `:9222`) | **23,450 cr** | `orbit-with-ben/05_Analytics/ai_spend/ledger.jsonl` (`2026-11-24T08:30:22Z`, `mini-daily`) |
| Shared Flow active reservations remaining (`HOS013_PASS1`: 6,600 / 6,600 used) | **0 cr** | `~/_desk/state/flow/shared/account.jsonl` |
| Shared Flow unposted charges | **800 cr** | `~/_desk/state/flow/shared/account.jsonl` (`pending: false`) |
| Total shared Flow liability | **800 cr** | `unposted + remaining_reservations` |
| Spendable balance before 011 (`23,450 - 800`) | **22,650 cr** | — |
| Required headroom floor (`--floor 3000`) | **3,000 cr** | Matches HOS 013 guard (`J2643` / `J2643b`) |
| **Available headroom above `--floor 3000`** | **19,650 cr** | `22,650 - 3,000` |

---

## 2. Google Flow 5 Dec 2026 Model Transition & Route Comparison (67 Plates)

Google Flow retires **`Veo 3.1 - Quality` (100 cr)**, **`Veo 3.1 - Fast` (10 cr, already banned on HOS)**, and **`Omni 1.1 Flash`** on **Sat 5 Dec 2026** (`J3691`, verified on `support.google.com/flow/answer/16526234` and CDP `:9222`). Both post-cutover models — **`Veo 3.1 - Lite`** (5 cr standard / 0 cr Lower Priority on Ultra 20x) and **`Omni 1.2 Flash`** (720p, 3 cr/s = 24 cr for 8 s, 0 cr 1080p upscale, silent/audio-stripped, `--allow-omni`) — are already live in the Flow UI and supported in `04_Audio/tools/orbit_flow_veo_ui.py` (`J3691`), subject to a **bounded first-use style UAT** (`studio/RULES.md`).

All 67 Flow plates in `PICTURE_PLAN_v04.json` (66 original + dedicated closing plate `P5:16b_closing_watch_and_globe`) are audited and classified into:
- **2 Explorer rows:** `P2:03a`, `P3:07a` (character consistency → `Omni 1.2 Flash` post-5-Dec)
- **27 Fragile-light / glass-refraction / vapour / mist / lamp rows:** `P1:02b`, `P1:04a`, `P1:05a`, `P1:05b`, `P1:06a`, `P1:07b`, `P1:08b`, `P1:09c`, `P2:02b`, `P2:04b`, `P2:07a`, `P3:06a`, `P3:06b`, `P4:02b`, `P4:03b`, `P4:05a`, `P4:05b`, `P4:09b`, `P5:02a`, `P5:04b`, `P5:05a`, `P5:05b`, `P5:06b`, `P5:07b`, `P5:08a`, `P5:15a`, `P5:16b_closing_watch_and_globe` (→ `Omni 1.2 Flash` post-5-Dec)
- **38 Standard daylight period rows:** → `Veo 3.1 - Lite` (5 cr) or `Veo 3.1 - Lite [Lower Priority]` (0 cr) post-5-Dec

| Route | Model mix (67 plates) | Try-1 credits (66-plate baseline) | Expected w/ 1.5× retakes | Headroom after try-1 (`22,650 - cap`) | Margin over `--floor 3000` | Prerequisite & risk |
|---|---|---:|---:|---:|---:|---|
| **Route A (RECOMMENDED — fastest clean route)** | 67 × `Veo 3.1 - Quality` (pre-5-Dec) | **6,700 cr** *(6,600)* | ~10,050 cr *(legacy 2.59×: 17,353)* | **15,950 cr** | **+12,950 cr** | **0 new-model UAT delay.** Proven house look across 008/009/010/013. Must finish Quality mint before Sat 5 Dec (any late retake post-5-Dec uses `Omni 1.2 Flash` @ 24 cr or `Lite` @ 5 cr). |
| **Route B1 (Credit-saving hybrid)** | 29 × `Omni 1.2 Flash` (24 cr) + 38 × `Veo 3.1 - Lite` (5 cr) | **886 cr** *(862)* | ~1,329 cr | **21,764 cr** | **+18,764 cr** | **Saves 5,814 cr (86.8%).** Requires bounded first-use style UAT (e.g., 4-plate probe ~58 cr) before bulk mint (`studio/RULES.md`). |
| **Route B2 (Hybrid w/ Lower Priority)** | 29 × `Omni 1.2 Flash` (24 cr) + 38 × `Veo 3.1 - Lite [Lower Priority]` (0 cr) | **696 cr** *(672)* | ~1,044 cr | **21,954 cr** | **+18,954 cr** | **Saves 6,004 cr (89.6%).** Requires bounded first-use style UAT + slower Lower Priority queue throughput. |
| **Route C (All-Omni 1.2 Flash)** | 67 × `Omni 1.2 Flash` 720p (24 cr) | **1,608 cr** *(1,584)* | ~2,412 cr | **21,042 cr** | **+18,042 cr** | **Saves 5,092 cr (76.0%).** Requires bounded first-use style UAT; uniform 720p→1080p upscale pipeline. |
| **Route D (All-Lite)** | 67 × `Veo 3.1 - Lite` (5 cr / 0 cr LP) | **335 cr** *(0 cr LP)* | ~503 cr | **22,315 cr** | **+19,315 cr** | **Not recommended** for 2 Explorer + 27 fragile-light/glass rows without UAT proof. |

### Recommendation for Mon 14 Dec Ben Watch / Thu 17 Dec Air

1. **Primary recommendation — Route A (`Veo 3.1 - Quality`, 6,700 cr pass-1 cap, `--floor 3000`):**
   - **Fastest zero-risk path to Mon 14 Dec watch.** Today is Wed 25 Nov (10 days before the 5 Dec Quality retirement, 19 days before Mon 14 Dec watch).
   - `Veo 3.1 - Quality` requires **zero new-model style UAT**, has **15,950 cr headroom** after reserving the full 6,700 cr cap (**+12,950 cr** above `--floor 3000`), and does **not** starve December/January films (`128`, `136`, `137`, `127`), which will mint post-5-Dec at ~700–900 cr each on `Lite + Omni 1.2 Flash`.
   - **Target schedule under Route A:** Chief PASS/GO Thu 26 Nov → pass-1 mint (14 batches × ≤5 rows) Thu 26 Nov–Tue 1 Dec → frame review & retakes Wed 2–Fri 4 Dec (before 5 Dec cutover; any straggler retake post-5-Dec uses `Omni 1.2 Flash` / `Lite`) → edit, SFX, music & QA Sat 5–Wed 9 Dec → thumbnails Thu 10 Dec → **Ben watch Fri 11–Mon 14 Dec** (3–4 days ahead of deadline) → **Air Thu 17 Dec 18:00 London**.
2. **Optional Chief credit-saving pivot — Route B1 via 1-day bounded UAT probe:**
   - If Chief prefers to bank ~5,800 Flow credits immediately, run a **4-plate bounded first-use style UAT (~58 cr: 2 `Omni 1.2 Flash` + 2 `Veo 3.1 - Lite`)** on Thu 26 Nov. If UAT passes, lock a post-cutover scope for Route B1 (**886 cr** try-1) and finish pass-1 by Wed 3–Thu 4 Dec (still 10 days before Mon 14 Dec watch). If UAT fails, fall straight back to Route A while Quality is still live through 4 Dec.

---

## 3. Per-Part Cost & Row Breakdown (`PICTURE_PLAN_v04.json`, 93 Rows)

| Part | Chapter | In–out | Total rows | Built free (CG / Arch) | Mint rows | Explorer | Fragile light | Standard | Route A Quality (try-1) | Route B1 Hybrid (try-1) | Route B2 LP Hybrid (try-1) |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Part 01 | The Fastest Knife | `0:00.00–1:26.80` | 18 | 3 (2 / 1) | 15 | 0 | 8 | 7 | 1,500 | 227 | 192 |
| Part 02 | A Gas That Made People Laugh | `1:26.80–2:55.66` | 15 | 5 (2 / 3) | 10 | 1 | 3 | 6 | 1,000 | 126 | 96 |
| Part 03 | This Is No Humbug | `2:55.66–4:31.88` | 15 | 3 (1 / 2) | 12 | 1 | 2 | 9 | 1,200 | 117 | 72 |
| Part 04 | The Fight Over Who Was First | `4:31.88–6:06.26` | 17 | 5 (3 / 2) | 12 | 0 | 5 | 7 | 1,200 | 155 | 120 |
| Part 05 | Across the Ocean | `6:06.26–8:55.30` | 28 | 10 (5 / 5) | 18 | 0 | 9 | 9 | 1,800 | 261 | 216 |
| **Total** | **Full film (`8:55.30`)** | `0:00.00–8:55.30` | **93** | **26 (13 / 13)** | **67** | **2** | **27** | **38** | **6,700** | **886** | **696** |

---

## 4. Prompt Hygiene Audit (`PROMPT_AUDIT_v04.json`)

All **67 Flow prompts** were audited against HOS 013 Flow lessons and `studio/RULES.md`:
- **Real person names:** **0 / 67** (every historical figure is described by age, period clothing, and historically verified appearance).
- **Forbidden words (`same DNA`, `lab DNA`):** **0 / 67**.
- **On-screen text requests:** **0 / 67**; **67 / 67** explicitly include `"no text, no letters, no numbers, no watermark, 16:9."`.
- **6 leaked stage-direction / bracket prefixes caught in `v03` and cleaned in `v04`:**
  - `P1:01a`: stripped `"Answer image by 0:03: "`
  - `P1:01b`: stripped `"Title question by 0:06 ('Why?') + physical apparatus (0:05–0:15): "` (removed quoted `'Why?'` so Flow never renders literal text!)
  - `P1:02a`: stripped `"Physical proof/apparatus (0:05–0:15): "`
  - `P1:02b`: stripped `"Physical proof/apparatus (0:05–0:15): "`
  - `P2:03a`: stripped `"[EXPLORER ACTS] "` (Explorer appearance lock is injected cleanly by the runner via `EXPLORER_LOCK` + canonical Explorer reference sheet)
  - `P3:07a`: stripped `"[EXPLORER ACTS] "`

---

## 5. `P5:16b` Overlap Resolution (93/93 Rows Zero Overlap)

- **Problem flagged in `J2563` / `J2659`:** `P1:07b` uses `6.61 s` of an `8.00 s` clip, leaving only `1.39 s` unused. Reusing `P1:07b` for `P5:16b` (`4.52 s`) would cause a **3.13 s overlap** (or require stretching/freezing, which is banned).
- **Why a £0 archive or code graphic is illegal here:** Row 91 (`P5:16a`, closing triptych) and Row 93 (`P5:17_cream_end_card`) are both **full-frame `code_graphic` rows**. `studio/RULES.md` forbids back-to-back full-frame teach graphics: *"a moving plate comes between them."*
- **Resolution in `PICTURE_PLAN_v04.json`:** Replaced `P5:16b_reuse_pocket_watch_to_globe` with **1 dedicated 8 s moving 3D cartoon Flow plate** (`P5:16b_closing_watch_and_globe`, `4.52 s` used): golden afternoon window light pulling back from a stopped brass pocket watch resting beside the clear two-necked glass ether globe in the quiet, empty Boston amphitheatre.
- **Result:** **93 / 93 rows have 0.00 s overlap**, `0` reuse rows, `0` consecutive full-frame graphics, and all 26 already-built free rows from `J2563` remain untouched.

---

## 6. Guarded Pass-1 Runner (`_mint_flow_v01_pass1.py`)

Mirrors `013_Darwin-Wallace-Evolution/07_Edit-Project/_mint_flow_v01_pass1.py`:
- Locks exact 67-row scope (`PASS1_SCOPE_J3736.json`, SHA-256 pinned to `PICTURE_PLAN_v04.json`, all 5 `parts/part-0N_plates_v04.json` boards, every prompt, both NAS house style refs, and the repo Explorer reference sheet).
- Live Flow account (SHA-256 digest only, zero personal email in code) + ULTRA + balance check (`read_live_balance`) + atomic per-Create price verification (`100 credits`, `Veo 3.1 - Quality`, `16:9`, `8s`, `x1`).
- Shared cross-channel Flow accounting (`~/_desk/state/flow/shared/account.jsonl`) with exclusive `WriterLock`, duplicate-process PID refusal, `--floor 3000` headroom enforcement (default on both `dry-run` and `submit`; `< 3000` refused on armed `submit`), `MAX_BATCH_ROWS = 5`, `MAX_BATCH_CREDITS = 1000`, `MAX_TAKES_PER_ROW = 1`, `MAX_TOTAL_CREDITS = 6700`, and `Veo 3.1 - Fast` refusal.
- Refuses retired `Veo 3.1 - Quality` submission on or after `2026-12-05` (`FLOW_CUTOVER_DATE`).
- Dual arming lock: `PASS1_SCOPE_J3736.json` ships with `"generation_authorized": false` AND `submit` refuses unless BOTH `HOS011_PASS1_SUBMIT=1` AND `generation_authorized: true` (after Chief price PASS / mint GO).
- Verified offline unit test suite: `tests/test_hos011_pass1_runner.py`.
