# Topic Brief — `136_Oppenheimer-Teller-Bethe-Trinity-Test-Explained` (`HOS:136` · Search-Led Plan Film 2)

> **STATUS (`J3495`, `2026-11-24`):**
> - **Plan & Approval:** **Film 2** of the Ben-approved History of Science search-led plan (`hos-search-2027-01`, Ben OK 24 Nov 2026; brought into December by Ben/Claude 24 Nov 2026). **Cluster 2 — Nuclear, Quantum & Modern Physics Breakthroughs.**
> - **WIP & Rule G:** Placed first in `jobs/WIP.json` `next_hos` (`["HOS:136", "HOS:137", "HOS:127", "HOS:011", ...]`). Enters active production as soon as `008` or `009` leaves `active` after Ben's watch this week. `£0.00` spent.
> - **Production Dates (24 Nov accelerated calendar):**
>   - **Rule-E topic review due:** Thu 26 Nov 2026
>   - **Package-first + script draft due:** Sat 28 Nov 2026
>   - **Script lock due:** Fri 4 Dec 2026
>   - **Ben's watch by:** Mon 14 Dec 2026
>   - **Target air date:** Thu 17 Dec 2026, 18:00 London (7–9 min, normal publish, no Premiere; slides one week if not ready and a finished older film `010`/`011`/`013` takes the slot; never rushed; nothing airs without Ben's watch).
> - **14-Day Test Bar (vs HOS best long of 162 views):** **500+ views** = keep Cluster 2 · **162–499** = one more film · **under 162** = drop or change (always reported with impressions, CTR, and US+UK+CA+AU share).
> - **Strict Unverified Claims Guard:** Every historical and scientific note in this brief is **UNVERIFIED** working text. Before any script is locked, VO is recorded, or picture credit is spent, every spoken and visual claim, date, calculation, and quote must be backed by verbatim primary-source quotes in `SOURCES.md` and verified through the `facts` lane (`gemini-agy`).

---

## 1. Search-Led Evidence (`05_Analytics/hos/search_research/2026-11-20.md` · `J3224`)

### 1a. Demand, Value & Competition (Steps 1–2)
| Query | Est. Monthly Searches | Comp | Growth | Top Markets / US Share | Adult / Evergreen | Status |
|---|---:|---:|---|---|---|---|
| `trinity test` | **21,494** | **38** | steady | Parent `manhattan project` `35,203`/mo (**US 18%, GB 9%** = 27% US+GB) | Adult · Evergreen | **Primary** |
| `manhattan project` | **35,203** | mid | steady | **US 18%, GB 9%** | Adult · Evergreen | **Secondary / Context** |
| `enrico fermi` | 9,601 | 35 | steady | Parent `manhattan project` US 18%, GB 9% | Adult · Evergreen | Cluster 2 bridge |
| `nuclear bomb` *(REJECTED)* | 279,797 | 50 | — | **IN 26%, BD 17%**, US 6% | Low-RPM trap | **DO NOT TARGET** |

- **US Education RPM proxy (`vidiq_earnings_calculate`, US long-form Education):** `$2.05` low / **`$3.42` mid** / `$5.47` high USD per 1,000 views.
- **Channel fit (`J3223` audit):** HOS audience is already `78.8%` aged 25–54 (`70.2%` male), but US share is only `2.5%` (`109` lifetime views). Targeting `trinity test` + `manhattan project` directly serves adult US/UK/CA/AU viewers instead of school-cram traffic.

### 1b. Signed-Out US Top-10 Gap (Step 3)
- **Gap score:** **9 / 10 weak, old, small, or off-target results** (`#1` is a 1:44 movie clip; `#2`, `#4`, `#5` are raw archival clips with no explanation; `7` results are 3+ years old; `6` are from channels `<50k` subscribers; virtually no clear 3D animated physics-history explainer answering the atmospheric-ignition calculation).

### 1c. Small-Channel Outlier Proof (`<50k` subs, `≥5×`, last 12 months — Step 4)
| Channel | Subs | Country | Video Title | Views | Breakout | Length |
|---|---:|---|---|---:|---:|---:|
| `Unifying Lens` | 1.5K | US | *How America Really Got the Bomb (And Started the Nuclear Age)* | 1.7K | **15×** | 9:55 |
| `Untold WWII` | 84 | US | *The Secret of Calutron: Engineers Used 14,700 Tons of Silver* | 5.8K | **172×** | 24:01 |
| `Science Retold` *(Cluster 2)* | 3.4K | US | *The Origin Of Planck's Constant* | 61.9K | **13×** | 24:02 |
| `Science Retold` *(Cluster 2)* | 3.4K | US | *How Scientists First Split the Atom* | 28.5K | **6.1×** | 20:18 |
| `Math Everywhere` *(Cluster 2)* | 10.3K | US | *MAX PLANCK: The Tragic Story of the Father of Quantum Physics!* | 36.5K | **10×** | 47:04 |

### 1d. Live 2026-11-24 Free Verification (`public_search.py` & `neighbours.py` tie-breaker)
- **`public_search.py` (`11_Upload-Package/evidence_2026-11-24_public_search.json`):**
  - `"trinity test"` → `autocomplete = yes`
  - `"manhattan project"` → `autocomplete = yes`
  - **0 exact title collisions** across Titles A, B, and C.
- **`neighbours.py` tie-breaker (`11_Upload-Package/evidence_2026-11-24_neighbours.json`):**
  - **PASS** (`8` education videos `≥1,000,000` views, `TED-Ed/TED: yes`): `Veritasium` `19,956,652` (*The Man Who Gave us the Power To Destroy Ourselves (Oppenheimer)*), `TEDx Talks` ★ `9,215,188`, `Kurzgesagt` `8,226,886`, `TED-Ed` ★ `3,332,906`, `TEDx Talks` ★ `2,322,133`, `TED-Ed` ★ `2,149,453`, `TED` ★ `1,243,770` (plus `SciShow` `1,671,802` *The Manhattan Project* & `CrashCourse` `944,463` *The Atomic Bomb: Crash Course History of Science #33* on initial pull).
  - Subject words to reuse in description/tags (never channel names): `trinity test`, `manhattan project`, `nuclear fission`, `oppenheimer`, `atmosphere ignition`, `implosion`, `atomic physics`.

---

## 2. Overlap & Lane Separation Check (Verified 2026-11-24)

- **Zero overlap with `HOS:130` (`130_Fermi-Szilard-Woods-How-Does-A-Nuclear-Reactor-Work`, PR #726/#728):** `HOS:130` is Chicago Pile-1 (Dec 1942 — how a controlled self-sustaining nuclear reactor works under Stagg Field). `HOS:136` is July 1945 Trinity Test theoretical physics (the atmospheric-ignition calculation by Edward Teller, Hans Bethe & Emil Konopinski, the implosion sphere test, and Fermi's paper-slip blast measurement).
- **Zero overlap with `ideas/022_Meitner-Hahn-Nuclear-Fission`:** `022` ends with the 1938 discovery of nuclear fission.
- **Zero overlap with Field Order History (`WW2:001–011`):** `WW2:003` covers the $3.0B B-29 Superfortress programme (Manhattan Project mentioned only as a cost benchmark). `HOS:136` stays **100% inside HOS's 3D cartoon laboratory-physics discovery lane** — equations, chalkboards, implosion geometry, and scientific measurement. **No combat, no military strategy, no wartime bombing or casualty footage.**
- **Zero overlap with Orbit With Ben (`001–087`):** Zero space overlap.
- **Zero overlap with HOS `000–135`, `ideas/011–095`, or `VIDEO_BACKLOG.json`.**

---

## 3. Package First (Method Step 5 — Before Any Script)

### 3a. Three Query-First Title Candidates (Scored Against Cluster 2 Outliers)
All three open with the exact search query `Trinity Test`, add one concrete physics hook, avoid low-RPM `nuclear bomb`, and have **0 exact collisions** in `evidence_2026-11-24_public_search.json`:

| Variant | Title | Chars | ≤50 Chars? | Why / Fit vs Outliers |
|---|---|---:|---|---|
| **Title A (Recommended Primary)** | `Trinity Test Explained: Could It Ignite the Sky?` | **48** | **YES (≤50)** | Leads with exact query (`Trinity Test Explained`), puts the visceral stakes question in plain English inside 50 chars for mobile, matches curiosity framing of `Science Retold` (13×) and `Unifying Lens` (15×). |
| **Title B (Plan Title / T&C Arm 2)** | `Trinity Test Explained: The Calculation That Nearly Stopped the Bomb` | 68 | ≤70 | Verbatim title from Ben-approved `hos-search-2027-01`; highlights the specific calculation hook (`LA-602`). Strong A/B test arm against Title A. |
| **Title C (T&C Arm 3)** | `Trinity Test: The Calculation That Nearly Stopped It` | 52 | Near 50 | Tighter calculation variant keeping exact `Trinity Test` lead. |

*Note for package-first script job:* Final choice locks Title A (≤50 chars) as primary or tests Title A vs Title B in Test & Compare once impressions justify it.

### 3b. Two Thumbnail Concepts (HOS 3D Cartoon House Style)
Painted 3D cartoon key art, warm period light, Explorer small at lower left, 2–3 words in clear top-left band, one gold word, **never repeating the title**:
- **Concept A (Chalkboard & Pre-Dawn Tower):** Warm 1945 Los Alamos physics chalkboard covered in glowing nitrogen-fusion equations on the left opening out to the steel Trinity tower against a pre-dawn desert sky on the right; Explorer small at lower left holding a notebook. Band text: `IGNITE THE SKY?` (gold on `SKY?`).
- **Concept B (Fermi's Paper Slips):** Close-up 3D cartoon hand releasing torn paper scraps into a warm pre-dawn flash outside an observation shelter, measuring tape/scale subtly visible; Explorer small at lower left. Band text: `ZERO MARGIN` (gold on `ZERO`).

---

## 4. Story Angle & 5-Part Structure Sketch (UNVERIFIED Working Outline)

- **Lane:** A familiar historical turning point (`Trinity Test`), told through the physicists, the room (Los Alamos chalkboard & Jornada del Muerto desert shelter), and the calculation that proved the atmosphere would not burn.
- **First 30 seconds (proof-first):** Open on the pre-dawn desert tower and a physicist's chalk equation stopping cold — answer the search question immediately: *Before the first atomic test in July 1945, physicists had to prove mathematically that it would not set Earth's entire atmosphere on fire.*
- **5 Parts (7–9 min, ~1,200–1,300 words, Teach on Screen: ≥3 DATA+SCALE incl. timeline, WHO cards, WHEN stamps, 2–4 FACT beats):**
  1. **Part 1 — The Chalkboard Scare (1942):** Edward Teller's question at Berkeley — could nuclear temperatures fuse nitrogen nuclei in Earth's air?
  2. **Part 2 — Checking the Sky (LA-602):** Hans Bethe, Emil Konopinski, Cloyd Marvin, and Teller calculate radiative energy loss (Bremsstrahlung) vs nitrogen-nitrogen fusion rates (`DATA+SCALE` comparison of ignition energy vs heat loss).
  3. **Part 3 — The Implosion Puzzle:** Why plutonium could not use a simple gun design and required exact explosive lenses focusing inward to microsecond precision (`DATA` timing scale).
  4. **Part 4 — Dawn in the Desert (16 July 1945):** The storm delay, the countdown, and Enrico Fermi's side bet — dropping tiny paper scraps to measure the shockwave displacement (`FACT` beat + `DATA` yield estimate vs official measurement).
  5. **Part 5 — What the Calculation Proved:** Why the atmosphere stayed intact, what nuclear physics unlocked (and changed forever), and handoff to Cluster 2 next film (`HOS:130` Chicago Pile-1 / nuclear reactors).

---

## 5. Shorts Plan (16–19 s, Ben 19 Nov House Rules + Search-Led Rotation)

- **Fri & Sat (promote `HOS:136` long, Related → `HOS:136`):**
  1. **Sat 11:30 (Go-public-day Short):** *Why Did Physicists Think the Trinity Test Could Ignite the Sky?* (64 chars; 3D cartoon glowing chalkboard + desert tower at frame 0; concrete-fact caption line 1; loops last line into line 1).
  2. **Fri 11:30 (Support Short):** *How Did Enrico Fermi Measure the Trinity Blast With Paper?* (58 chars; 3D cartoon hand dropping torn paper scraps in desert wind at frame 0).
- **Sun & Tue 11:30:** Rotate Cluster 1/2 winner or test next month's Cluster 2 candidate topic before scripting (e.g. *What Is the God Particle?* / *Why Did Fermi Build a Reactor Under a Stadium?*). Every Short title is a search phrase or question.
