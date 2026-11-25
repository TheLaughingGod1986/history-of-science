# Pre-build vidIQ audit — History of Science (`HOS:130`)

> **Status (`2026-11-22`, `J3348` → `J3350`):** Pre-filled from zero-spend signed-out YouTube evidence (`evidence_2026-11-22_public_search.json`, `11` queries / `80` rows; `evidence_2026-11-22_neighbours.json`) and merged `J3224` vidIQ research (`orbit-with-ben` `05_Analytics/hos/search_research/2026-11-20.md`). **Rule-E pre-cleared GO (`96.6 / 100`) by `J3350`** in `jobs/WIP.json` `next_hos` under Rule G. Live per-title vidIQ scoring waits until an active HOS WIP slot opens.

---

## Episode

| Field | Value |
|-------|-------|
| ID / slug | `130_Fermi-Szilard-Woods-How-Does-A-Nuclear-Reactor-Work` |
| Working title | *How Does a Nuclear Reactor Work? (Under a Stadium)* |
| Date pulled | `2026-11-22` (plus `J3224` vidIQ pull `2026-11-20`) |
| Credits used (approx) | `0` (`J3348` spent £0 / 0 credits) |
| Brand guardrails | Wonder over fearbait · no military/combat overlap with WW2 channel · HOS lane (a familiar thing, and the moment we found out) |

---

## 1. Success targets (this episode)

| Metric | Target |
|--------|--------|
| Title score | ≥ **90** (aim **95+**, live vidIQ check at WIP entry) |
| Primary keyword overall | `enrico fermi` `9,601/mo` comp `35` (`9/10` US SERP gap); `how does a nuclear reactor work` `autocomplete = yes` |
| Hook promise | How Enrico Fermi built and controlled the first nuclear reactor under a Chicago football stadium with no shielding — and why `0.65%` delayed neutrons keep every reactor from exploding. |
| Retention design | 4–5 cause-and-effect acts with DATA+SCALE graphics and WHO/WHEN cards (`Teach on screen`, `Rule 30`) |
| Packaging | One giant 3D painted hero object (graphite reactor dome + cadmium rod), Explorer lower-left, 2-word cream/gold serif hook (`NO SHIELDING`) |

---

## 2. Keyword research (`J3224` vidIQ + `2026-11-22` signed-out autocomplete)

| Keyword | Autocomplete | Est./mo (`J3224`) | Comp | Role (title / desc / chapter / Shorts) | Keep? |
|---------|--------------|------------------:|-----:|----------------------------------------|-------|
| `how does a nuclear reactor work` | yes | — (public search) | — | primary title lead + desc line 1 | **Yes** |
| `enrico fermi` / `enrico fermi nuclear reactor` | yes | 9,601 | 35 | secondary title / desc / Short S02 | **Yes** |
| `chicago pile 1` | yes | — (public search) | — | chapter + tags + Short S02 | **Yes** |
| `nuclear chain reaction` | yes | — (public search) | — | chapter + Short S01 | **Yes** |
| `manhattan project` (parent context) | — | 35,203 (US 18%, GB 9%) | — | umbrella context (lab physics only) | Context only |

**Decision:** Primary keyword for title lead = `How Does a Nuclear Reactor Work?`  
**Description first 100 chars must include:** `How does a nuclear reactor work? Beneath a Chicago football stadium in 1942, Enrico Fermi proved...`

---

## 3. Title ABC (score before VO)

| | Title | Chars | Exact Collisions | Keep? |
|---|---|---:|---:|-------|
| A | `How Does a Nuclear Reactor Work? (Under a Stadium)` | 50 | 0 | **Primary (`Rule 15 ≤50` + `Rule 26`)** |
| B | `The First Nuclear Reactor Was Built on a Squash Court (1942)` | 60 | 0 | **T&C Arm 2 (`Rule 23`)** |
| C | `Enrico Fermi: How Scientists Built the First Nuclear Reactor` | 60 | 0 | **Cluster 2 named-scientist backup** |
| Reject | `How Did We Discover Nuclear Power? | History of Science` | 55 | — | **Reject** (formulaic + series suffix) |

---

## 4. Outlier & Neighbour Patterns (`2026-11-22` + `J3224`)

| Channel / Video | Views / Breakout | Steal (structure) | Do **not** copy |
|-----------------|------------------|-------------------|-----------------|
| `Kurzgesagt` `rcOFV4y5z8c` *Nuclear Energy Explained: How does it work? 1/3* | `8,224,844` | Plain physical mechanism explained visually | Flat 2D vector style |
| `SmarterEveryDay` `JVROsxtjoCw` *I Explored the World's First Nuclear Power Plant* | `3,847,436` | Tactile curiosity about how real hardware works | Live-action vlog pacing |
| `TED-Ed` ★ `R7WPEYGr1Vs` *How do nuclear power plants work?* | `3,332,507` | Tight curriculum clarity + high suggested traffic | Textbook framing without a human story |
| `Science Retold` (3.4K US, `J3224`) *How Scientists First Split the Atom* | `28,500` (`6.1×`) | Adult US science-history storytelling | Long slow holds (`>4.5s`) |

---

## 5. Sign-off (block production until checked)

- [x] `neighbours.py` gate PASS (`12` raw / `9` strictly on-topic `≥1M`, `TED-Ed/TED: yes`)
- [x] `public_search.py` autocomplete & `0` collision check saved (`11` queries / `80` rows; refreshed in `J3350`)
- [x] Rule-E topic go/no-go review PASS (`J3350`, **GO `96.6 / 100`** — `TOPIC_GO_NO_GO_SHEET.md`, `TOPIC_OPPORTUNITY_SCORE.md`)
- [ ] Active HOS WIP slot open (Rule G)
- [ ] Live vidIQ Title Analyzer ≥ 90 locked
- [ ] `SOURCES.md` verbatim quotes + `facts` lane verified (`gemini-agy`)
- [ ] Script reviewer ≥ 90 + Episode gate PASS

**Signed off by:** `macbook` (`J3350` Rule-E GO `96.6/100` in `next_hos`; Chief merge & WIP entry pending)  
**Date:** `2026-11-22` (Rule-E pre-cleared backlog brief)
