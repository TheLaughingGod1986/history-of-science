# HOS 136 — `v02` Fix Verification & Acting Chief `KEEP` / Script Lock Ruling (`J3677`)

- **Job:** `J3677` (`kind: review`, ref `J3553`)
- **Acting Chief:** `gemini` (elected Acting Chief under `Claude -> Codex -> Gemini -> Grok` per Ben's 24 Nov 2026 order; verified via live `chief_relay.py status` = `Chief: Gemini` at `06:20Z`, `06:24Z`, and `06:25Z`; `claude` down until `07:50Z`, `codex` down on usage limit until Nov 27)
- **Date:** `2026-11-25` (UTC)
- **Film:** `HOS:136` — *Trinity Test Explained: Could It Ignite the Sky?* (Cluster 2 Film 2, target air Thu 17 Dec 2026 18:00 London; Ben's watch Mon 14 Dec; script lock due Fri 4 Dec)
- **Audited PRs:**
  - HOS PR `#766` (`macbook/J3675`, head `fff4addb`, `7/7` CI green) — `v02` script, `SOURCES.md`, `FACT_NOTES_v02.md`, `SHORTS_SCRIPTS_v02.md`, `LAUNCH_PLAN.md`, `PRE_BUILD_VIDIQ_AUDIT.md`
  - HOS PR `#767` (`gemini/J3676-hos136-facts-v02`, head `dd52bd1e96a46547a1f4f3a85349ddce05840ad2`, stacked cleanly on PR `#766`, `MERGEABLE`, `7/7` GitHub CI checks green) — independent `v02` facts audit (`01_Script/GEMINI_FACTS_CHECK_v02.md`, `0` blocking `FLAG`s)
- **Ruling:** **`KEEP` & SCRIPT LOCKED**
- **Protected Actions Executed by Elected Acting Chief (`gemini`):**
  - Merged HOS PR `#767` into `main` as **`ab25f2de`** (automatically superseding/merging PRs `#746`, `#753`, `#764`, and `#766`).
  - Merged HOS PR `#765` (`jobs/reviews/J3553/REVIEW.md`, historical `v01` FIX ruling) into `main` as **`fc86aa62`**.
  - Updated `status.json` and `production-status.md` (`script`: `done`, `facts`: `done`, `shorts_scripts`: `done`, `vo` & `shorts_vo`: `todo` referencing queued VO jobs `J3678` & `J3679`).
  - Rotated completely finished, Ben-OK'd, and scheduled `HOS:008` (`J3500`, `ben_ok: done`, `scheduled: done`) out of `orbit-with-ben/jobs/WIP.json` `active` and promoted newly script-locked `HOS:136` (#1 in Ben's 24 Nov `hos-search-2027-01` order) into active HOS WIP (**OWB PR `#1306`**, merged as `90613b82ca`: `5/5` HOS active, `9/10` total).
  - Queued `HOS:136` 5-part long VO (**`J3678`**, due Mon 7 Dec 18:00 London) and Shorts `S01`/`S02` VO (**`J3679`**, due Tue 8 Dec 18:00 London) under normal Mac-mini ElevenLabs credit rules (floor `0`, live balance check first, never buy/top up, `vo_check_py312.sh` required; `HOS:128` `J3670`/`J3671` takes credit priority if tight due to earlier Thu 10 Dec air date).
  - Reopened and closed original **`J3553`** as `done` (script lock achieved).
  - **Spend / Scheduling:** **£0.00 / 0 credits spent**; nothing uploaded, scheduled, or altered on YouTube.
  - **Target & contingency preserved:** **Thu 17 Dec 2026, 18:00 London** target (normal publish, no Premiere; Ben's watch by Mon 14 Dec; Shorts `S02` Fri 18 Dec & `S01` Sat 19 Dec 11:30 London; slides one week if not ready).
  - **Packaging caveat preserved:** Draft thumbnail concepts (`AIR ON FIRE?` / `MEASURED BY PAPER`, with §2.6 hand-verified chalkboard ink & §2.9 3-way T&C note at `thumbnails` stage) remain **unrendered drafts (NOT rendered packaging PASS)**; picture and thumbnail generation wait for Chief VO PASS.

---

## 1. Exact Locked `v02` SHA-256 Hashes (Independently Verified on `dd52bd1e` / Merged `ab25f2de`)

All 8 hashes independently recomputed on a clean detached worktree at `dd52bd1e96a46547a1f4f3a85349ddce05840ad2` — **8/8 EXACT MATCH**:

```text
85fb1286610264f5692a1e1dfe766fc0dfb90231016fd27f012dc079499047b2  02_Video-Projects/136_Oppenheimer-Teller-Bethe-Trinity-Test-Explained/01_Script/trinity_test_explained_script_master_v02.md
060acf45825759934812f8a12833f298c2d5de68a236e9a237d215961a69311a  02_Video-Projects/136_Oppenheimer-Teller-Bethe-Trinity-Test-Explained/01_Script/SOURCES.md
899156a368a5f22e554b3d267f073e3c69ff7eded609e2aa07f5db2e5c8126a6  02_Video-Projects/136_Oppenheimer-Teller-Bethe-Trinity-Test-Explained/01_Script/FACT_NOTES_v02.md
0dede3091c363d229d3c4e779519f512ddb44f605a7c207099cb44ef92da1b6a  02_Video-Projects/136_Oppenheimer-Teller-Bethe-Trinity-Test-Explained/01_Script/GEMINI_FACTS_CHECK_v02.md
e1df5d81baffca83c559b78a2a87df97df0fe8be15fb8de96a761445906941fe  02_Video-Projects/136_Oppenheimer-Teller-Bethe-Trinity-Test-Explained/10_Shorts/SHORTS_SCRIPTS_v02.md
bcf98849bb6d4258070965a4add4e0b30580afd27e7cc9604d93a4ceea71ed96  02_Video-Projects/136_Oppenheimer-Teller-Bethe-Trinity-Test-Explained/11_Upload-Package/PACKAGE_FIRST_SCORING_v01.md
6d602b11f3e9bbc62bc326c3ba30fcd892ee6302a4e72299cfc7668511839b1a  02_Video-Projects/136_Oppenheimer-Teller-Bethe-Trinity-Test-Explained/11_Upload-Package/LAUNCH_PLAN.md
65489bdc4e2b9f8d4ee19337f6de4bbc0863f050cdc4e25437a10aa6bf1b55aa  02_Video-Projects/136_Oppenheimer-Teller-Bethe-Trinity-Test-Explained/11_Upload-Package/PRE_BUILD_VIDIQ_AUDIT.md
```

---

## 2. Independent Verification Matrix — All 8 `J3552` `FLAG`s + 2 `R20` Polishes + 6 `J3553` `ADD` Items

| Item | Requirement (`J3552` / `J3553`) | Independent Chief Audit Result (`2026-11-25`) | Status |
|---|---|---|---|
| **`FLAG-1`** | Remove bogus OSTI `4036390` (1964 Misra) & WAF-blocked `sgp.fas.org`; cite verified Wayback `LA-602` PDF (`14 Aug 1946`) + DOE OpenNet `trinity_safety.htm` + LANL/OSTI `1836991`; clean draft description `Sources:` | Completely removed from all active citations (`SOURCES.md`, `FACT_NOTES_v02.md`, `LAUNCH_PLAN.md`); verified 22-page Wayback `LA-602` PDF (`14 August 1946`, declassified `2-2-73`) + DOE OpenNet + OSTI `1836991` live. | **PASS** |
| **`FLAG-2`** | Remove unsourced `"a thousand times faster"` cooling ratio in Part 02 (`SCALE:` & spoken) | Removed cleanly (`L57`: `"radiation drained energy faster than nitrogen fusion could replace it, keeping a safety factor above one even under the worst assumptions"` + frozen-lake spark analogy). Matches `LA-602` pp. 3, 12, 16 (`~1.6` floor / `7.4` with inverse Compton). | **PASS** |
| **`FLAG-3`** | Upgrade `FACT_NOTES` Rows 3 (NASA), 8 (`LA-602` pp. 10 & 15–16), and 9 (CrossRef Bethe 1976 DOI + opened verbatim quotes; drop non-matching Wikipedia links) | Directly spot-checked live HTTP `200`: NASA Goddard (`78.08%`, `20.95%`), CrossRef `10.1080/00963402.1976.11455623` (`"Ultimate catastrophe?"`, *BAS*, pp. `36-37`), Stanford PH241 `chung1` (`three in one million`, `No chance whatever...`, `This claim is nonsense.`), plus `J3676` visual verification of `LA-602` PDF pp. `1, 2, 3, 10, 12, 15, 16`. | **PASS** |
| **`FLAG-4`** | Fix Part 04 Bainbridge bunker (`S-10000`, `~5.7 mi / 9.1 km` south of Ground Zero, NOT `"ten miles away"`); keep Base Camp (`~10 mi`) clearly pre-shot | Fixed cleanly in `L116` (`S-10000`, `~5.7 miles / 9.1 km`) and `L119`/`L121–122` (Base Camp pre-shot wager separated from `S-10000` countdown and post-flash paper drop). Confirmed verbatim against live DOE OpenNet `trinity.htm`. | **PASS** |
| **`FLAG-5`** | Fix Short `S02` `"silent shockwave"` | Replaced with `"in silence for the blast wave"` in both table row (`L56`) and spoken paragraph (`L62`). | **PASS** |
| **`FLAG-6`** | Fix inverted light-speed analogy in Part 03 (`1 µs` = `~300 m`, ~3 football fields) | Fixed in spoken `L98` and `SCALE:` `L100` (`"In one microsecond, light itself travels barely three hundred metres, about three football fields"`). Exact SI arithmetic: $299{,}792{,}458\text{ m/s} \times 1\,\mu\text{s} = 299.79\text{ m}$. Conceptual physics only; zero blueprints. | **PASS** |
| **`FLAG-7`** | Trim Shorts `S01` (`55w`) & `S02` (`65w`) to `40–44w` (`16.0–19.0 s` house rule) | Programmatically verified in `SHORTS_SCRIPTS_v02.md`: **`S01 = 42w`** (`16.36–16.80 s` speech) and **`S02 = 42w`** (`16.36–16.80 s` speech), cleanly inside `16.0–19.0 s` with natural pauses, Frame 0 3D cartoon moving plates, concrete-fact line 1, single Teach overlay, and seamless loops. | **PASS** |
| **`FLAG-8`** | Replace spliced `FACT_NOTES` Row 10 Wikipedia quote with DOE OpenNet `hans-bethe.html` verbatim | Directly verified verbatim live on DOE OpenNet `hans-bethe.html` (`HTTP 200`, `EXACT PASS`). | **PASS** |
| **`R20` (a & b)** | Unify Part 05 timeline span (`1942–1946`) and tighten CP-1 interval (`2 yr 7.5 mo`) | Unified to `1942–1946` (`four years`, `L154`) and tightened to `"Nearly three years before that desert dawn"` (`L157`). | **PASS** |
| **`ADD-1`** | `WHO:` Cloyd Marvin resolution + Arthur Compton moved to Part 01 first mention | Spoken `L69` reads `"Konopinski, Teller, and a colleague"` (full `E. J. Konopinski, C. Marvin, E. Teller` preserved in `SOURCES.md`/`FACT_NOTES_v02.md`). Compton `WHO:` moved to Part 01 `L39` (first mention `L37`). All `8/8` named people carded at first spoken mention (`role ≤ 3w`). | **PASS** |
| **`ADD-2`** | Add `WHEN: 1959` (Part 02) and `WHEN: Los Alamos, 1943` (Part 03) | Added at `L66` and `L83` (`7` total `WHEN:` stamps aligned 1-to-1 with `FACT_NOTES_v02.md`). | **PASS** |
| **`ADD-3`** | One card/label at a time & interleaved `[VISUAL MUST]` | Programmatically verified **`36` `[VISUAL MUST]` blocks**, **`0` stacked `WHO`/`WHEN`/`FACT`/`LABEL` cards**. All `16` `LABEL:` and `4` `FACT:` markers `≤4w`. | **PASS** |
| **`ADD-4`** | Part 01 first-minute milestones (`<=0:08`, `<=0:15`, `<=0:25`, `0:25–0:40`, `<0:45`) | Programmatically verified: `L5` (`13w`) `5.1–5.2 s`; `L9` (`34w`) `13.2–13.6 s`; `L13` (`55w`) `21.4–22.0 s`; `L17` (`73w`) `21.4–29.2 s` (`~23–31 s` w/ pauses); `L21` (`98w`) `28.4–39.2 s`. | **PASS** |
| **`ADD-5`** | Short `S02` overlay `≤4` words + §2.6 hand-verified edit-ink note | Overlay `2.5m SHIFT ≈ 10KT` (`4` tokens `≤4w`); `10,000 TONS TNT` cream pad marked hand-verified edit ink (§2.6). | **PASS** |
| **`ADD-6`** | Single `master` filename in `01_Script/` & `LAUNCH_PLAN.md` archive-credit match | Sole master is `trinity_test_explained_script_master_v02.md`; default `gate:episode` (no `--script`) selects `v02` and PASSes (`9/9`); `LAUNCH_PLAN.md` aligns archive credits & production line at package lock. | **PASS** |
| **Spoken Diff** | Direct audit of every `v01 → v02` spoken change | Audited every changed spoken line (`L5, L9, L13, L21, L57, L64, L69, L98, L107, L113, L119, L150, L157` + `S01`/`S02`) — **zero unverified new spoken claims**. | **PASS** |

*Non-blocking `J3676` quote-hygiene notes acknowledged (`R04` Wikipedia-only Berkeley/Oppenheimer, `R13` omitted `...`, `R15` Wikipedia `"planned"` paired beside primary DOE OpenNet `"scheduled"` verbatim) — zero factual, spoken, or primary-backing defects.*

---

## 3. Packaging Draft Lock Candidates Confirmed (Unrendered Drafts Only)

- **Primary Title (Arm A):** *Trinity Test Explained: Could It Ignite the Sky?* (`48c ≤ 50`, `96/100`, `0` collisions)
- **T&C Arm B (Plan Title):** *Trinity Test Explained: The Calculation That Nearly Stopped the Bomb* (`68c ≤ 70`, `92/100`, `0` collisions)
- **T&C Arm C (Backup):** *Trinity Test: The Calculation That Nearly Stopped It* (`52c`, `88/100`, `0` collisions)
- **Thumbnails (Unrendered Drafts — NOT rendered packaging PASS):** Thumb A (`AIR ON FIRE?`, gold on `FIRE?`, `96/100`) & Thumb B (`MEASURED BY PAPER`, gold on `PAPER`, `93/100`), preserving **§2.6 hand-verified chalkboard ink** (never AI-rendered math/text) and **§2.9 3-way T&C note** at `thumbnails` stage (waits for VO PASS).
- **Shorts Titles (Test B, `0` collisions):** `S01` *Could the Trinity Test Have Ignited the Sky?* (`44c`, Sat 19 Dec 11:30 London) & `S02` *How Did Enrico Fermi Measure the Trinity Blast With Paper?* (`58c`, Fri 18 Dec 11:30 London).

---

## 4. Fresh Independent Gate Outputs (`dd52bd1e` / `ab25f2de`, `2026-11-25`)

- **Direct live HTTP exact-quote spot-checks (`8/8` primary hosts):** `EXACT PASS` across NASA Goddard Earth Fact Sheet, DOE OpenNet (`hans-bethe.html`, `trinity.htm`, `trinity_safety.htm`), CrossRef `10.1080/00963402.1976.11455623`, Stanford PH241 `chung1`, OSTI `1836991` (Katz 2021), and Enrico Fermi memo (`dannen.com/decision/fermi.html`).
- **Teach / Polish / Craft markers on `trinity_test_explained_script_master_v02.md`:** `DATA: 5` · `SCALE: 5` · `WHO: 8` · `WHEN: 7` · `FACT: 4` · `LABEL: 16` · `VISUAL MUST: 36` (`0` stacked) · `TEACH: 5` · `CHAPTER CARD: 4` · `EXPLORER ACTS: 2` (outside first minute).
- **`npm run review:script -- --file ../02_Video-Projects/136_Oppenheimer-Teller-Bethe-Trinity-Test-Explained/01_Script/trinity_test_explained_script_master_v02.md`:** **PASS · 93.4 / 100** (`Words: 1260 · Est. min: 8.4 · Chapters: 4 · Structure gates 8/8`).
- **Default `npm run gate:episode -- --project ../02_Video-Projects/136_Oppenheimer-Teller-Bethe-Trinity-Test-Explained` (WITHOUT `--script`):** **PASS — VO / Gemini Veo allowed**, selecting `01_Script/trinity_test_explained_script_master_v02.md` (`9/9 OK`).
- **`bash 00_Brand/Channel-Setup/tools/check_all.sh 02_Video-Projects/136_Oppenheimer-Teller-Bethe-Trinity-Test-Explained`:** **ALL CHECKS PASS** (`12/12 PASS`).
- **`python3 -m unittest tests/test_no_private_network.py`:** **OK (`5` tests)**.
- **GitHub CI on PR `#767`:** **7/7 checks green** (`atempo`, `check`, `contract`, `no-desk-close`, `no-media`, `status-board`, `tests`).

---

## 5. Next Production Steps (Queued under Rule G WIP)

1. **`J3678`** — `HOS:136` long VO (5 parts from locked `trinity_test_explained_script_master_v02.md`, `85fb1286...`, due Mon 7 Dec 18:00 London; Mac mini `el_client.py`/`vo_take.py`, `vo_check_py312.sh`; `HOS:128` `J3670`/`J3671` takes credit priority if tight due to earlier Thu 10 Dec air date).
2. **`J3679`** — `HOS:136` Shorts `S01` & `S02` VO (from locked `SHORTS_SCRIPTS_v02.md`, `e1df5d81...`, `16.0–19.0 s` band, due Tue 8 Dec 18:00 London; Mac mini `el_client.py`/`vo_take.py`, `vo_check_py312.sh`).
3. Picture generation (`Flow Veo 3.1`) and rendered thumbnail design/panel remain **strictly blocked until Chief VO PASS**.
