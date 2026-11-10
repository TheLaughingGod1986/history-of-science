# Pre-build audit — 013 Evolution (Darwin's 20-year secret and Wallace's letter)

Filled 19 Oct 2026 from public signals collected in `00_Brand/Channel-Setup/ideas/evidence_2026-10-15_J0295/public_search.json`, `public_search_titles.json` (YouTube GB autocomplete and top results, signed out) and `n_darwin.json` (`neighbours.py`, gate PASS: 13 education videos at 1M+, TED-Ed/TED present). **vidIQ is waived by Ben's standing rule** (desk PR #180, comment 5949981415), so there are no vidIQ scores.

## Episode

| Field | Value |
|-------|-------|
| ID / slug | 013 · `013_Darwin-Wallace-Evolution` |
| Working title | *Evolution: The Letter That Forced Darwin to Publish* (T&C B: *Why Darwin Kept Natural Selection Secret for 20 Years*) |
| Date pulled | 2026-10-15 |
| Credits used (approx) | 0 (vidIQ waived) |
| Brand guardrails | Notebook B "I think" tree + Wallace's June 1858 letter first · no Ternate receipt-date overclaim · no unhedged finch/barnacle counts · 1844 essay before *Vestiges* · 25 June fairness letter before 28 June death · 22 Nov 1859 Murray trade sale before 24 Nov publication |

## 1. Success targets

| Metric | Target |
|--------|--------|
| Title score | vidIQ waived; title checked against `THUMBNAIL_AND_TITLE_RULES.md` §1 instead |
| Primary keyword | neighbour phrases *evolution* / *natural selection* / *charles darwin*; search phrases *how darwin discovered evolution* / *alfred russel wallace darwin* |
| Hook promise | "Why did Charles Darwin work out how life changes over time, and then lock it in a drawer for twenty years?" |
| Retention design | Six acts: The Twenty-Year Secret (cold) → The Birds He Forgot to Label → The Engine and the Barnacles → Fever in the Islands → The Night Nobody Noticed → The Missing Piece |
| Packaging | One object per thumbnail: Darwin's locked red-leather *Notebook B* "I think" tree or the sealed 1858 packet beside finch beaks |

## 2. Keyword research

**Public signals only.** "Autocomplete" means YouTube suggests the phrase as you type.

| Keyword | Autocomplete? | Competition read | Role | Keep? |
|---|---|---|---|---|
| how darwin discovered evolution | **yes** | Moderate; open slots under 1M in GB top 5 | cold open / search intent | yes |
| charles darwin natural selection | **yes** | Heavy textbook competition | neighbour phrase, description line 1, tags | yes |
| alfred russel wallace darwin | **related** | Opportunity — underused vs bare Darwin biography | Part 04–05, description, tags | yes |
| evolution the letter that forced darwin to publish | **no** | All 5 top GB slots under 1,000 views (`754 · 17 · 145 · 212 · 40`) | Title A | yes |
| why darwin kept natural selection secret for 20 years | **related** | 3 of top 4 GB slots under 120k views (`8,774 · 252 · 1.70M · 110k`) | Title B (Test & Compare) | yes |

**Decision:** *Evolution* and *Darwin* lead Title A with the *letter* hook; Title B tests the 20-year secret question. Description line 1 carries *evolution*, *natural selection*, *Charles Darwin*, and *Alfred Russel Wallace*.

## 3. Title ABC

| | Title | vidIQ score | Rules check | Keep? |
|---|-------|------:|-------|-------|
| A | Evolution: The Letter That Forced Darwin to Publish | waived | Pass: big subject (*Evolution*) + concrete hook (*The Letter That Forced Darwin to Publish*), 51 chars | **Main (J0295 lock)** |
| B | Why Darwin Kept Natural Selection Secret for 20 Years | waived | Pass: search question + exact 20-year span, 53 chars | **Test & Compare (J0295 lock)** |
| C | How a Letter From the Jungle Forced Darwin to Publish | waived | Pass: concrete story hook, 53 chars | **Alt** |

**Locked title:** J0295 Chief topic lock (6196336541); final package subject to Ben's watch.

## 3b. Script reviewer

```bash
cd 07_Content-Ops && npm run review:script -- --file ../02_Video-Projects/013_Darwin-Wallace-Evolution/01_Script/darwin_script_master_v02.md
```

- [x] Script reviewer ≥ 90: **92.6** on v01 (`9db5a267`) and **92.6** on v02 (`darwin_script_master_v02.md`), 8/8 structure gates, 1,227 spoken words.

## 4. Outlier / competitive patterns

| Outlier / pattern | Views | Steal (structure) | Do **not** copy |
|---|---|---|---|
| Primer *Simulating Natural Selection* | ~15.7M | Visual cause-and-effect clarity for selection | simulation-only format |
| Kurzgesagt *How Evolution works* | ~11.4M | Simple everyday analogy for selection | flat vector style |
| Amoeba Sisters *Natural Selection* | ~4.6M | Clear distinction between variation and adaptation | classroom cartoon format |
| TED-Ed *Myths and misconceptions about evolution* | ~3.3M | Myth-busting ("survival of the fittest", Galápagos eureka myth) | anthology structure |
| TEDxNTU *How we found out evolution is true: John van Wyhe* | ~2.2M | Primary-source grounding on Darwin & Wallace | lecture format |

**Patterns we will use:** Galápagos unlabelled-finches myth-bust; 1837 "I think" notebook sketch; 5 July 1844 sealed essay and Emma letter before *Vestiges* (Oct 1844); Wallace's Feb 1858 malaria-fever letter arriving 18 June 1858; 1 July 1858 Linnean reading ("no striking discovery"); 22 Nov 1859 pre-publication sell-out; Jenkin's paint pot vs Mendel's beads.

## 5. Incorporate into the build

| Data finding | Change |
|---|---|
| Neighbour phrases *evolution* / *natural selection* / *charles darwin* | In Title A/B, description line 1, and tags |
| Galápagos eureka myth is widespread | Part 02 opens by busting the beach flash-of-genius myth with Darwin's unlabelled birds and Gould's 1837 London identification |
| Chronology traps (1844 *Vestiges*, June 1858 death, 22 Nov trade sale) | Fixed in `darwin_script_master_v02.md` and sourced in `FACT_NOTES_v02.md` (`30 OK · 0 PARTIAL · 0 FLAG`) |

**Chapter list after audit:**

1. Cold open: The Twenty-Year Secret (no card)
2. The Birds He Forgot to Label
3. The Engine and the Barnacles
4. Fever in the Islands
5. The Night Nobody Noticed
6. The Missing Piece

## 6. Retention plan

| Minute zone | Job | Picture / VO |
|---|---|---|
| 0–0:05 | Curiosity spike | Four finch beaks beside red-leather *Notebook B* "I think" tree locked in drawer (answer image by 0:03, question by 0:07) |
| ~0:15 | Promise & stakes | Malay Archipelago packet + barnacle jar (0:15); locked London museum cases (0:25) |
| ~0:34 | First real fact | Summer 1837 "I think" tree + 20-year secrecy bar (before 0:45) |
| Chapter starts | Re-hook | Each part opens cold and ends on a question the next part answers |
| Midpoint (~5:00) | Twist | "Case closed? Wrong." 18 June 1858 letter to Lyell + 25 June fairness letter + 28 June death |
| Final chapter | Payoff + hand-off | Jenkin's blending paint vs Mendel's whole beads + Spencer's "fittest = fits"; hand-off to 012 Mendel or 014 Mary Anning |

## 7. Sign-off (block production until checked)

- [x] Keywords pulled and primary locked: public signals done (§2); vidIQ waived by Ben (standing rule)
- [x] Title proposed: *Evolution: The Letter That Forced Darwin to Publish*, T&C *Why Darwin Kept Natural Selection Secret for 20 Years*
- [x] Script reviewer ≥ 90: 92.6 on v02 (`darwin_script_master_v02.md`)
- [x] Outlier patterns mapped into the chapter arc
- [x] Thumb concepts match the title promise (one object · one emotion)
- [x] Chapter teach-points listed (6 acts)
- [x] Cold-open clock (5 / 15 / 30 s) written
- [x] Retention plan filled
- [x] Production checklist path noted: `11_Upload-Package/PRODUCTION_CHECKLIST_V2.md`

**Signed off by:** Claude (J0299 v01) & Gemini (`gemini-argon`, J0304 / J0307 v02); topic locked by Chief in J0295 (`6196336541`); vidIQ waived by Ben, standing rule (desk PR #180, comment 5949981415).
**Date:** 19 Oct 2026

**Only then:** Chief PASS on `darwin_script_master_v02.md` + `FACT_NOTES_v02.md` → VO (Ben Orbit Narrator) → plates → edit.
