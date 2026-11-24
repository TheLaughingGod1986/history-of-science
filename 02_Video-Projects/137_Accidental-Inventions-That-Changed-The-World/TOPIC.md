# Topic Brief — `137_Accidental-Inventions-That-Changed-The-World` (`HOS:137` · Search-Led Plan Film 3)

> **STATUS (`J3503` Rule-E Review GO, `2026-11-24`):**
> - **Plan & Approval:** **Film 3** of the Ben-approved History of Science search-led plan (`hos-search-2027-01`, Ben OK 24 Nov 2026; brought into December by Ben/Claude 24 Nov 2026). **Cluster 3 — Accidental & World-Changing Inventions.**
> - **Rule-E Verdict (`J3503`, `2026-11-24`):** **GO (`95.8 / 100` · `9.58 / 10` Opportunity Score · `10 / 10` gates PASS after `J3503` fixes)** — retired colliding PR `#743` Title A (`5 Accidental Inventions That Changed the World`, 5 exact live collisions), fixed Thumbnail Concept A/B copy & composition (`NEARLY TRASHED` / `WRONG RESISTOR`), locked **Laminated Safety Glass (1903)** as Beat 3 (excluding Microwave to preserve zero overlap with `HOS:129` GO `96.4/100`), audited neighbours strictly, verified `0` Short collisions, and queued follow-on script job **`J3513`** (`kind: script`, draft due **Mon 30 Nov 18:00 London**).
> - **WIP & Rule G:** Placed second in `jobs/WIP.json` `next_hos` (`["HOS:136", "HOS:137", "HOS:127", "HOS:011", ...]`). Enters active production as soon as the second of `008`/`009` leaves `active` after Ben's watch this week. `£0.00` spent.
> - **Production Dates (24 Nov accelerated calendar):**
>   - **Rule-E topic review:** **DONE (`J3503` GO, 24 Nov 2026)**
>   - **Package-first + script draft due (`J3513`):** Mon 30 Nov 2026 18:00 London
>   - **Script lock due:** Tue 8 Dec 2026
>   - **Ben's watch by:** Mon 21 Dec 2026
>   - **Target air date:** Thu 24 Dec 2026, 18:00 London (7–9 min, normal publish, no Premiere; slides one week if not ready and a finished older film `010`/`011`/`013` takes the slot; never rushed; nothing airs without Ben's watch).
> - **14-Day Test Bar (vs HOS best long of 162 views):** **500+ views** = keep Cluster 3 · **162–499** = one more film · **under 162** = drop or change (always reported with impressions, CTR, and US+UK+CA+AU share).
> - **Strict Unverified Claims Guard:** Every historical and scientific note in this brief is **UNVERIFIED** working text. Before any script is locked, VO is recorded, or picture credit is spent, every spoken and visual claim, date, inventor detail, and quote must be backed by verbatim primary-source quotes in `SOURCES.md` and verified through the `facts` lane (`gemini-agy`).

---

## 1. Search-Led Evidence (`05_Analytics/hos/search_research/2026-11-20.md` · `J3224`)

### 1a. Demand, Value & Competition (Steps 1–2)
| Query | Est. Monthly Searches | Comp | Growth | Top Markets / US Share | Adult / Evergreen | Status |
|---|---:|---:|---|---|---|---|
| `inventions that changed the world` | **35,881** | 54 | steady | **US 23%** (`8,280` US/mo), VN 15%, RU 15% | Adult · Evergreen | **Primary umbrella** |
| `accidental discoveries` | **9,367** | **39** | **+93.0%** | Parent `amazing discoveries` `25.7k` (**AU 20%, US 20% = 40%**) | Adult · Evergreen | **Primary low-comp** |
| `accidental inventions that changed the world` | **8,092** | 54 | **+73.9%** | US-led (`inventions that changed…` US 23%) | Adult · Evergreen | **Primary exact** |
| `inventions that shook the world` | **8,001** | **32** | **+69.5%** | US-led | Adult · Evergreen | Secondary |
| `pacemaker` / `pacemaker invention` | 23,807 | 45 | -32% | US/UK adult medical-tech curiosity | Adult · Evergreen | Beat / Short hook |
| `history of inventions` *(REJECTED)* | 68,676 | 31 | — | **PK 25%**, NL 10%, US 10% | Low-RPM trap | **DO NOT TARGET** |

- **US Education RPM proxy (`vidiq_earnings_calculate`, US long-form Education):** `$2.05` low / **`$3.42` mid** / `$5.47` high USD per 1,000 views.
- **Zero school-exam trap:** Universal adult Anglosphere curiosity (`US 23%` + `AU 20% / US 20%` on parent terms) with fast rising search interest (`+73.9%` to `+93.0%`).

### 1b. Signed-Out US Top-10 Gap (Step 3)
- **Gap score:** **9/10 to 10/10** weak, old, small, or slideshow listicle results (`inventions that changed the world`: **10/10**, 6 old, 8 `<50k` subs, `#1` old TV upload; `accidental inventions that changed the world`: **10/10**, 5 old, 5 `<50k` subs, 6 `<50k` views; `accidental discoveries`: **9/10**, 6 old 3+ yr, listicle clutter).

### 1c. Small-Channel Outlier Proof (`<50k` subs, `≥5×`, last 12 months — Step 4)
| Channel | Subs | Country | Video Title | Views | Breakout | Length |
|---|---:|---|---|---:|---:|---:|
| `Invention Flex` | 6.2K | US | *Top 10 Nikola Tesla Inventions That Changed The World* | 9.6K | **8.3×** | 7:42 |
| `Industrial Case Files` | 138 | US | *10 Forgotten Tesla Inventions That Could've Changed Everything* | 4.7K | **8.6×** | 31:39 |
| `Counter Facts Lab` | 1.4K | — | Accidental-discoveries breakout | 1.5K | **22×** | — |
| `TheOriginLens` | 246 | — | Accidental-invention breakout | 1.6K | **8×** | — |

### 1d. Live 2026-11-24 Free Verification (`public_search.py` & `neighbours.py` tie-breaker)
- **`public_search.py` (`11_Upload-Package/evidence_2026-11-24_public_search.json`, `13` queries after `J3503`):**
  - `"accidental inventions that changed the world"` → **`autocomplete = yes`**
  - `"accidental discoveries"` → **`autocomplete = yes`**
  - `"inventions that changed the world"` → **`autocomplete = yes`** (search results populated in `J3503`)
  - `"accidental inventions"` → **`autocomplete = yes`**
  - `"inventions that shook the world"` → **`autocomplete = yes`** (added in `J3503`)
  - **0 exact title collisions** across updated Long Titles A (`45c`), B (`69c`), C (`56c`), alternate (`48c`), and Short Titles S01 (`61c` & `48c`) and S02 (`54c`). *(PR `#743`'s original Title A `5 Accidental Inventions That Changed the World` had 5 exact live collisions — incl. `Arun Surya Teja` `nLbBtuydgZo` 251,692 views — and was retired in `J3503`.)*
- **`neighbours.py` tie-breaker (`11_Upload-Package/evidence_2026-11-24_neighbours.json`):**
  - **PASS** (`4` raw / **`3` strictly on-topic** education videos `≥1,000,000` views, `2` `TED-Ed` ★ `≥1M`, `TED-Ed/TED: yes`): `Thoughty2` `1,594,081` (*10 Inventions That Changed the World*, `Zaez9eM8wTs`), `TED-Ed` ★ `1,486,538` (*The accident that changed the world*, `CNbnLgetqHs`), `TED-Ed` ★ `1,041,862` (*How inventions change history (for better and for worse)*, `0SMNYivhGsc`). *(1 raw `≥1M` row — `TED-Ed` `RzkD_rTEBYs` *How will AI change the world?* `2,323,113` — transparently excluded in `J3503` as future-AI off-topic; reinforced by **`SciShow`** `YYyfioO50fM` *6 Incredible Discoveries Made on Accident* `1,484,724` saved in `evidence_2026-11-24_public_search.json`.)*
  - Subject words to reuse in description/tags (never channel names): `accidental inventions`, `inventions that changed the world`, `accidental discoveries`, `scientific mistakes`, `pacemaker`, `vulcanized rubber`, `safety glass`, `penicillin`, `post-it notes`.

---

## 2. Overlap & Lane Separation Check (Verified 2026-11-24 · `J3503` Ruling)

- **Zero overlap with public HOS longs (`001–007`):** none of the 5 laboratory mistakes duplicates Germs, Periodic Table, X-rays, Atom, Blood Circulation, Trees/Air, or Smallpox Vaccine.
- **Locked 5-Beat Shortlist Ruling (`J3503` — Zero Overlap With `HOS:129`):** **Laminated Safety Glass (Édouard Bénédictus, 1903) is locked as Beat 3; Microwave (1945) is excluded** because `HOS:129` (*How Was the Microwave Invented? (A Radar Accident)*, PR `#724`/`#727`) already passed Rule-E GO (`96.4/100`) in `next_hos` as its own standalone 8-minute film. `HOS:137` serves as the **Cluster 3 anthology hub** (~75–90 s per invention, united by the "prepared mind" laboratory slip) that launches the Cluster 3 playlist and hands off to `HOS:129` and future single-subject deep dives (`ideas/020` Penicillin, `ideas/076` Pacemaker, Goodyear, Post-it Notes).
- **Zero overlap with `HOS:130` (nuclear reactor), `HOS:136` (Trinity test), Field Order History (`WW2:001–010`, no combat), or Orbit With Ben (`001–087`, no space).**

---

## 3. Package First (Method Step 5 — Updated in `J3503` Before Any Script)

### 3a. Three Zero-Collision Query-First Title Candidates (Scored Against Cluster 3 Outliers)
All three open with exact high-growth query phrasing, exclude low-RPM `history of inventions`, and have **0 exact collisions** in `evidence_2026-11-24_public_search.json`:

| Variant | Title | Chars | ≤50 Chars? | Why / Fit vs Outliers |
|---|---|---:|---|---|
| **Title A (Recommended Primary · `J3503` Fix)** | `Accidental Inventions: 5 Mistakes That Worked` | **45** | **YES (≤50)** | Starts with exact autocomplete query `Accidental Inventions`, echoes Ben-approved hook `5 Mistakes That Worked`, clean under 50 chars on mobile, **`0` live collisions** (replaces colliding PR `#743` `5 Accidental Inventions That Changed the World`). |
| **Title B (Plan Title / T&C Arm 2)** | `Accidental Inventions That Changed the World (5 Mistakes That Worked)` | 69 | ≤70 | Verbatim title from Ben-approved `hos-search-2027-01`; leads with exact `+73.9%` query `Accidental Inventions That Changed the World` + Rule 26 parenthetical hook. Ideal T&C Arm 2 against Title A (`0` collisions). |
| **Title C (T&C Arm 3)** | `Accidental Inventions: 5 Mistakes That Changed the World` | 56 | ≤70 | Starts with exact `Accidental Inventions`, puts `5 Mistakes` + `That Changed the World` up front (`0` collisions). |
| *Backup (≤50c alt)* | `5 Accidental Lab Mistakes That Changed the World` | 48 | YES (≤50) | Alternate `≤50c` phrasing keeping `Changed the World` (`0` collisions). |
| *Retired (`J3503`)* | `5 Accidental Inventions That Changed the World` | 46 | — | **REJECTED** — 5 exact live YouTube collisions (`Arun Surya Teja` `nLbBtuydgZo` 251.7K views et al.; Never list §1.7). |

### 3b. Two Single-Hero Thumbnail Concepts (HOS 3D Cartoon House Style · `J3503` §2.2/§2.5/§2.B Fixes)
Painted 3D cartoon key art, warm period workshop/lab light, **one giant hero object (~2/3 right frame)** readable at `168×94`, Explorer small lower left, 2–3 words in clear top-left band, one gold word, **never repeating any title words**:
- **Concept A (One Hero Lab Mistake — `J3503` §2.2 & §2.5 Fix):** Giant warm-lit 3D cartoon 1903 cracked-yet-intact glass flask holding together in a glowing spiderweb (OR giant glowing emerald *Penicillium* Petri dish) filling 2/3 of the right frame on a warm period lab bench (subtle secondary props out of focus, never a 3-object collage); Explorer small at lower left lifting a magnifying glass. Band text: **`NEARLY TRASHED`** (gold on `TRASHED` — replaces title-repeating `5 MISTAKES`).
- **Concept B (One Wrong Resistor — `J3503` §2.B.1 Fix):** Close-up 3D cartoon 1956 workbench with one oversized warm-glowing wrong resistor plugged into a transistor circuit, pulsing a steady golden heartbeat line on a small period oscilloscope beside a crossed-out notebook; Explorer small lower-left. Band text: **`WRONG RESISTOR`** (gold on `WRONG` — names the exact physical object on screen).

---

## 4. Story Angle, 5-Part Structure Sketch & `J3503` Script Guardrails (UNVERIFIED Working Outline)

- **Lane:** Five familiar everyday objects (pacemakers, tyres, windscreens, antibiotics, sticky notes), each told as a tight ~75–90 s cause-and-effect lab beat: *what the inventor was actually trying to make → the mistake → why a prepared mind noticed instead of throwing it away → what changed.*
- **First 30 seconds (proof-first):** Open on Wilson Greatbatch grabbing a resistor 100× too strong out of a parts box in 1956 — and hearing his recording circuit pulse like a human heart (`0:05` proof apparatus). Answer the search premise at once: five real lab mistakes that reshaped everyday modern life.
- **5 Parts (7–9 min, ~1,200–1,300 words, Teach on Screen: ≥3 DATA+SCALE incl. 1839–1974 timeline, WHO cards, WHEN stamps, 2–4 FACT beats; all claims UNVERIFIED until `SOURCES.md` + `facts` lane):**
  1. **Part 1 — The Wrong Resistor (Wilson Greatbatch, 1956 · Implantable Pacemaker):** Building a heart-sound recording oscillator, reaches for a 10 kΩ resistor and grabs a 1 MΩ resistor by mistake — circuit pulses at ~1.8 ms every second, matching a human heartbeat. *(Guardrail: credit William Chardack & Andrew Gage for 1958 animal / 1960 Buffalo human implant; distinguish from Elmqvist & Senning's 1958 Swedish implant.)*
  2. **Part 2 — The Hot Stove Spill (Charles Goodyear, 1839 · Vulcanised Rubber):** After years of obsessive sulfur-and-lead trials in debt, dropping treated rubber onto a hot stove in Woburn, MA turns brittle gum into weatherproof elastic rubber. *(Guardrail: frame as a prepared mind, not a lazy fluke; verify 1844 patent, 1860 death in debt, and that Goodyear Tire was named after him in 1898.)*
  3. **Part 3 — The Dropped Glass Flask (Édouard Bénédictus, 1903 · Laminated Safety Glass · LOCKED):** A flask lined with evaporated cellulose-nitrate (collodion) film falls in a Paris lab and cracks into a spiderweb without shattering — later patented as Triplex (**1909**) for motoring windscreens. *(Guardrail: keep 1903 discovery and 1909 patent distinct; no Microwave beat so `HOS:129` stays 100% separate.)*
  4. **Part 4 — The Unwashed Petri Dish (Alexander Fleming & the Oxford Team, 1928–1941 · Penicillin):** Returning in Sept 1928 to a contaminated *Staphylococcus* plate with a bacteria-free halo around *Penicillium* mould — and why turning it into usable medicine took another decade of purification by Howard Florey, Ernst Chain, and Norman Heatley. *(Guardrail: credit the Oxford team explicitly; zero vaccine or medical-advice claims.)*
  5. **Part 5 — The Repositionable Glue (Spencer Silver & Art Fry, 1968–1974 · Post-it Notes):** Trying for a strong aerospace adhesive, Silver makes low-tack, pressure-sensitive acrylate microspheres instead; in 1974 Art Fry uses them to stop his church choir hymnal bookmarks from falling out (national launch 1980 after 1978 Boise sample test) — closing hand-off to Cluster 3 single-subject deep dives (including `HOS:129` Microwave). *(Guardrail: do not oversimplify microspheres as "glue that didn't stick at all".)*

---

## 5. Shorts Plan (16–19 s, Ben 19 Nov House Rules + Search-Led Rotation · `0` Collisions Verified in `J3503`)

- **Fri & Sat (promote `HOS:137` long, Related → `HOS:137`):**
  1. **Sat 11:30 (Go-public-day Short):** *How Did One Wrong Resistor Accidentally Invent the Pacemaker?* (`61` chars, `0` collisions; tight `48c` variant *How Did One Wrong Resistor Invent the Pacemaker?* also verified `0` collisions; 3D cartoon pulsing resistor on 1956 workbench at frame 0; concrete-fact caption line 1; seamless loop).
  2. **Fri 11:30 (Support Short):** *How Did Failed Glue Accidentally Invent Post-it Notes?* (`54` chars, `0` collisions; 3D cartoon peeling yellow adhesive note off a hymnal/lab bench at frame 0).
- **Sun & Tue 11:30:** Rotate a Cluster 1–3 winner or test next month's Cluster 3 candidate topic before scripting (e.g. *How Did a Dropped Flask Invent Shatterproof Glass?* / *How Did Charles Goodyear's Stove Accident Invent Rubber?*). Every Short title is a search phrase or question.
