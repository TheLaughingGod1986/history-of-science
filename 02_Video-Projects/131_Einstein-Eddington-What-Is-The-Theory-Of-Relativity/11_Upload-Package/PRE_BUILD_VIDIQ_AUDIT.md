# Pre-build vidIQ audit — History of Science (`HOS:131`)

> **Status (`2026-11-22`, `J3348`):** Pre-filled from zero-spend signed-out YouTube evidence (`evidence_2026-11-22_public_search.json`, `evidence_2026-11-22_neighbours.json`) and merged `J3224` vidIQ research (`orbit-with-ben` `05_Analytics/hos/search_research/2026-11-20.md`). Live per-title vidIQ scoring waits until Rule-E GO and an active HOS WIP slot opens under Rule G.

---

## Episode

| Field | Value |
|-------|-------|
| ID / slug | `131_Einstein-Eddington-What-Is-The-Theory-Of-Relativity` |
| Working title | *What Is the Theory of Relativity? (1919 Eclipse)* |
| Date pulled | `2026-11-22` (plus `J3224` vidIQ pull `2026-11-20`) |
| Credits used (approx) | `0` (`J3348` spent £0 / 0 credits) |
| Brand guardrails | Wonder over fearbait · zero overlap with `025` photoelectric effect · natural end-screen sequel to `009` Newton's Gravity |

---

## 1. Success targets (this episode)

| Metric | Target |
|--------|--------|
| Title score | ≥ **90** (aim **95+**, live vidIQ check at WIP entry) |
| Primary keyword overall | `theory of relativity` `29,476/mo` (`+84.4%`, comp `49`); `albert einstein documentary` `6,141/mo` (`+88.7%`, comp `38`, `9/10` US SERP gap) |
| Hook promise | How Arthur Eddington's 29 May 1919 solar eclipse photographs proved Einstein's curved spacetime beat Newton's gravity — and why your phone's GPS would drift 11 km/day without it. |
| Retention design | 4–5 cause-and-effect acts with DATA+SCALE graphics and WHO/WHEN cards (`Teach on screen`, `Rule 30`) |
| Packaging | One giant 3D painted hero object (1919 eclipse glass photographic plate + bent golden starlight ray), Explorer lower-left, 2-word cream/gold serif hook (`STARLIGHT BENT`) |

---

## 2. Keyword research (`J3224` vidIQ + `2026-11-22` signed-out autocomplete)

| Keyword | Autocomplete | Est./mo (`J3224`) | Comp | Role (title / desc / chapter / Shorts) | Keep? |
|---------|--------------|------------------:|-----:|----------------------------------------|-------|
| `what is the theory of relativity` | yes | 29,476 (`theory of relativity`, `+84.4%`) | 49 | primary title lead + desc line 1 | **Yes** |
| `theory of relativity explained` | yes | — (public search) | — | Title C + description + tags | **Yes** |
| `how did einstein prove relativity` | yes | 6,141 (`albert einstein documentary`, `+88.7%`) | 38 | chapter + Short S01 | **Yes** |
| `1919 solar eclipse einstein` | related | — (public search) | — | title tail + Act III + Short S01 | **Yes** |
| `why does gps need relativity` | — | — (public search, `minutephysics` 998K) | — | Act IV payoff + Short S02 | **Yes** |

**Decision:** Primary keyword for title lead = `What Is the Theory of Relativity?`  
**Description first 100 chars must include:** `What is the theory of relativity? On 29 May 1919, a total solar eclipse proved Albert Einstein...`

---

## 3. Title ABC (score before VO)

| | Title | Chars | Exact Collisions | Keep? |
|---|---|---:|---:|-------|
| A | `What Is the Theory of Relativity? (1919 Eclipse)` | 48 | 0 | **Primary (`Rule 15 ≤50` + `Rule 26`)** |
| B | `How a 1919 Solar Eclipse Proved Einstein Beat Isaac Newton` | 58 | 0 | **T&C Arm 2 (`Rule 23`)** |
| C | `Theory of Relativity Explained: The 1919 Eclipse That Proved It` | 63 | 0 | **Search-explainer backup** |
| Reject | `How Did We Discover Relativity? | History of Science` | 52 | — | **Reject** (formulaic + series suffix) |

---

## 4. Outlier & Neighbour Patterns (`2026-11-22` + `J3224`)

| Channel / Video | Views / Breakout | Steal (structure) | Do **not** copy |
|-----------------|------------------|-------------------|-----------------|
| `Veritasium` `eyZEqSPeMwg` *Relativity is so much weirder than we thought...* | `8,545,878` | Counter-intuitive physical intuition first | 30-minute lecture pacing |
| `TED-Ed` ★ `h8GqaAp3cGs` *Einstein's twin paradox explained* | `5,919,102` | Crystal-clear animated clock comparisons | Abstract blackboard without historical stakes |
| `TED-Ed` ★ `91XI7M9l3no` *Einstein's miracle year* | `2,733,278` | Grounding 1905 physics in the Bern patent desk | Skipping the 1919 eclipse proof |
| `Vox` `HLxvq_M4218` *The eclipse photo that made Einstein famous* | `2,196,555` | Glass-plate starlight measurement as the dramatic proof | Flat 2D newspaper collage look |
| `Quantara Explains` (3.1K US, `J3224`) / `Think Like Feynman` (12.1K US) | `7.6K` (`8.9×`) / `6.0K` (`7.7×`) | Adult US physics storytelling | Multi-hour slow pacing |

---

## 5. Sign-off (block production until checked)

- [x] `neighbours.py` gate PASS (`7` raw / `5` strictly on-topic `≥1M`, `TED-Ed/TED: yes`)
- [x] `public_search.py` autocomplete & `0` collision check saved
- [ ] Rule-E topic go/no-go review PASS
- [ ] Active HOS WIP slot open (Rule G)
- [ ] Live vidIQ Title Analyzer ≥ 90 locked
- [ ] `SOURCES.md` verbatim quotes + `facts` lane verified (`gemini-agy`)
- [ ] Script reviewer ≥ 90 + Episode gate PASS

**Signed off by:** pending Rule-E review & Chief lock  
**Date:** `2026-11-22` (backlog brief)
