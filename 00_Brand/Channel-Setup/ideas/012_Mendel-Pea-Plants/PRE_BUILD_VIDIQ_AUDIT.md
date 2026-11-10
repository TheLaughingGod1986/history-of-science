# Pre-build audit — 012 Genetics (Gregor Mendel's 28,000 pea plants, 1856–1900)

Prepared 7 Nov 2026 (`J2328`) from public signals in `00_Brand/Channel-Setup/ideas/evidence_2026-10-15_J0252/` and refreshed in `00_Brand/Channel-Setup/ideas/012_Mendel-Pea-Plants/evidence_2026-11-07_neighbours.json` / `evidence_2026-11-07_public_search.json` (`neighbours.py`, gate PASS: 8 education videos at 1M+, TED-Ed/TED present). **vidIQ is waived by Ben's standing rule** (desk PR #180, comment 5949981415), so there are no vidIQ scores. Ready to copy to `02_Video-Projects/012_Mendel-Pea-Plants/11_Upload-Package/PRE_BUILD_VIDIQ_AUDIT.md` when `HOS:012` enters `active`.

## Episode

| Field | Value |
|---|---|
| ID / slug | 012 · `012_Mendel-Pea-Plants` |
| Proposed air date | **Thu 24 Dec 2026** 18:00 UK (`2026-12-24T18:00:00.000Z`, `next_hos` #2) |
| Working title | *Genetics: The Monk Who Counted 28,000 Pea Plants* (T&C B: *How a Monk and 28,000 Pea Plants Solved Genetics*) |
| Date pulled | 2026-10-15 / refreshed 2026-11-07 |
| Credits used (approx) | 0 (vidIQ waived) |
| Brand guardrails | Abbey mice anecdote hedged as "Rumour says" · "My time will come" hedged as "he is said to have told a friend" · 28,000 plants / 7,324 seeds (5,474 : 1,850 = 2.96:1) / 8,023 seeds (6,022 : 2,001 = 3.01:1) sourced to Mendel (1866) · hawkweed apomixis (1903) explains Part 04 failure · 33 rows in `SOURCES_v01.md` must pass Gemini facts & primary-source quote check before VO |

## 1. Success targets

| Metric | Target |
|---|---|
| Title score | vidIQ waived; title checked against `THUMBNAIL_AND_TITLE_RULES.md` §1 instead |
| Primary keyword | neighbour phrases *genetics* / *heredity* / *gregor mendel* / *pea plants*; search phrases *gregor mendel pea plants* / *how mendel discovered genetics* |
| Hook promise | "Why can you have your grandfather's red hair, or your grandmother's green eyes, when neither of your parents has them — and how did one quiet friar with a paintbrush and 28,000 pea plants discover the hidden rules of heredity?" |
| Retention design | Five acts: The Trait That Skipped a Generation (cold) → The Friar Who Failed Twice → The Trait That Vanished → The Hawkweed Trap → Three Letters in the Spring of 1900 |
| Packaging | One object per thumbnail: open green pea pod showing 3 smooth golden peas and 1 wrinkled green pea beside Mendel's fine paintbrush and tweezers in warm abbey sunlight |

## 2. Keyword research

**Public signals only.** "Autocomplete" means YouTube suggests the phrase as you type.

| Keyword | Autocomplete? | Competition read | Role | Keep? |
|---|---|---|---|---|
| gregor mendel pea plants | **yes** | TED-Ed 5.05M #1; 3 of top 5 GB slots under 280k (`188k · 278k · 167k`) | primary / description line 1, tags | yes |
| how mendel discovered genetics | **related** | Autocompletes `how did gregor mendel discover genetics`; Cognito 188k & Interactive Biology 216k in top 5 | cold open / search intent | yes |
| Genetics: The Monk Who Counted 28,000 Pea Plants | **no** | TED-Ed 5.05M #1; slots #2–#5 under 190k (`2 · 188k · 183 · 1`) | Title A (Main) | yes |
| How a Monk and 28,000 Pea Plants Solved Genetics | **no** | TED-Ed 5.05M #1; slots #2–#5 under 190k (`666 · 188k · 141 · 6.5k`) | Title B (Test & Compare) | yes |
| How Mendel's Pea Plants Solved Heredity | **no** | Shares TED-Ed's exact words; 3 of top 5 under 280k (`188k · 216k · 278k`) | Title C (Alt) | yes |

**Decision:** *Genetics* leads Title A with *The Monk Who Counted 28,000 Pea Plants*; Title B tests the `How` search promise with the same concrete hook. Description line 1 carries *genetics*, *heredity*, *Gregor Mendel*, and *pea plants*.

## 3. Title ABC

| | Title | vidIQ score | Rules check | Keep? |
|---|---|---:|---|---|
| A | Genetics: The Monk Who Counted 28,000 Pea Plants | waived | Pass: big subject (*Genetics*) + concrete hook (*The Monk Who Counted 28,000 Pea Plants*), 49 chars | **Main** |
| B | How a Monk and 28,000 Pea Plants Solved Genetics | waived | Pass: search promise + exact number, 49 chars | **Test & Compare** |
| C | How Mendel's Pea Plants Solved Heredity | waived | Pass: shares TED-Ed 5.05M neighbour phrasing, 39 chars | **Alt** |

## 3b. Script reviewer

```bash
cd 07_Content-Ops && npm run review:script -- --file ../00_Brand/Channel-Setup/ideas/012_Mendel-Pea-Plants/mendel_script_master_v01.md
```

- [x] Script reviewer ≥ 90: **93.5** on v01 (`mendel_script_master_v01.md`, `J0260`), 8/8 structure gates, 1,311 words (~1,240 spoken).

## 4. Outlier / competitive patterns

| Outlier / pattern | Views | Steal (structure) | Do **not** copy |
|---|---|---|---|
| TED-Ed ★ *How Mendel's pea plants helped us understand genetics - Hortensia Jiménez Díaz* | ~5.05M | Clear visual 3:1 smooth/wrinkled & yellow/green pea pod reveal | 3-minute classroom summary without the 1850 exam failures or 1866 hawkweed tragedy |
| Amoeba Sisters *DNA, Chromosomes, Genes, and Traits: An Intro to Heredity* | ~6.84M | Everyday family-trait curiosity hook | flat 2D textbook cartoon |
| CrashCourse *Heredity: Crash Course Biology #9* | ~5.58M | Blending-paint myth-bust before Particulate Inheritance | fast host monologue |
| TED-Ed ★ *What is epigenetics? - Carlos Guerrero-Bosagna* | ~2.47M | Nuance on why traits aren't just a simple single switch | modern molecular focus |
| SciShow *The Man Who Discovered Dominant & Recessive Genes: Meet Gregor Mendel* | ~1.05M | Human biography of Mendel in Brünn | talking-head studio format |

**Patterns we will use:** Blending-paint myth vs whole pea packets; failing the Vienna teacher exam twice and learning statistical physics from Christian Doppler; forceps + paintbrush + calico bag artificial pollination on 253 flowers; 5,474 : 1,850 (2.96:1) and 6,022 : 2,001 (3.01:1) seed counts; Carl von Nägeli's hawkweed (*Hieracium*) apomixis trap; 35-year gap to the spring 1900 three-way rediscovery (de Vries, Correns, Tschermak); polygenic sliders explaining why human height looks blended.

## 5. Incorporate into the build

| Data finding | Change |
|---|---|
| Neighbour phrases *genetics* / *heredity* / *gregor mendel* / *pea plants* | In Title A/B, description line 1, and tags |
| Primary-source verification required (`SOURCES_v01.md`, 33 rows) | Queue `--kind facts` pass on entry into `active` before locking script v02 / VO |
| Why human traits don't look like a 3:1 box | Part 05 answers with polygenic brass-slider diagram (many genes adding small steps vs one pea switch) |

**Chapter list after audit:**

1. Cold open: The Trait That Skipped a Generation (no card)
2. The Friar Who Failed Twice
3. The Trait That Vanished
4. The Hawkweed Trap
5. Three Letters in the Spring of 1900

## 6. Retention plan

| Minute zone | Job | Picture / VO |
|---|---|---|
| 0–0:05 | Curiosity spike | Friar's hand splitting a green pea pod to show 6 smooth golden and 2 wrinkled green peas in Brünn, 1856 (answer image by 0:03, question by 0:07) |
| ~0:15 | Promise & stakes | Paintbrush dusting pollen + calico bag (0:15); red and white ink swirling into pink vs two whole peas (0:25) |
| ~0:34 | First real fact | Gregor Mendel in St Thomas's Abbey (1856–1863) + 28,000 pea plants counter & 35×7 m garden plan DATA/SCALE (before 0:45) |
| Chapter starts | Re-hook | Each part opens cold and ends on a question the next part answers |
| Midpoint (~5:00) | Twist | "Case closed? Wrong." Silent 1865 hall + Carl von Nägeli's hawkweed apomixis trap |
| Final chapter | Payoff + hand-off | 35-year timeline gap to spring 1900 (de Vries, Correns, Tschermak), Bateson 1905 *genetics*, polygenic sliders, hand-off to Darwin (`013`) or Anning (`014`) |

## 7. Sign-off (block production until checked)

- [x] Keywords pulled and primary locked: public signals done (§2); vidIQ waived by Ben (standing rule)
- [x] Title proposed: *Genetics: The Monk Who Counted 28,000 Pea Plants*, T&C *How a Monk and 28,000 Pea Plants Solved Genetics*
- [x] Script reviewer ≥ 90: 93.5 on v01 (`mendel_script_master_v01.md`)
- [x] Outlier patterns mapped into the chapter arc
- [x] Thumb concepts match the title promise (one object · one emotion)
- [x] Chapter teach-points listed (5 acts)
- [x] Cold-open clock (5 / 15 / 30 s) written
- [x] Retention plan filled
- [x] Production checklist path noted: `11_Upload-Package/PRODUCTION_CHECKLIST_V2.md`

**Prepared by:** `macbook-2` (`J2328` topic go/no-go prep, building on `J0252` & `J0260`).  
**Date:** 7 Nov 2026  

**When a HOS active slot frees:** Enter `active` via Rule-E topic go/no-go → Gemini facts pass (`SOURCES_v01.md` rows 1–33) & quote check → VO (Ben Orbit Narrator) → Shorts scripts v02 → plates → edit.
