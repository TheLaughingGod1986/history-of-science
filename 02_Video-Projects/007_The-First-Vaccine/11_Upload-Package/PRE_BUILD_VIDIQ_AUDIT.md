# Pre-build audit — 007 The First Vaccine (Jenner, cowpox, 1796)

Filled 4 Oct 2026 by Claude from public signals: `evidence_2026-10-03_public_search.json` (YouTube GB autocomplete and top results, signed out) and `evidence_2026-10-03_neighbours.json` (`neighbours.py`, gate PASS: 7 education videos at 1M+). **vidIQ is waived by Ben's standing rule** (desk PR #180, comment 5949981415), so there are no vidIQ scores.

## Episode

| Field | Value |
|-------|-------|
| ID / slug | 007 · `007_The-First-Vaccine` |
| Working title | *Why Vaccines Are Named After a Cow* |
| Date pulled | 2026-10-03 |
| Credits used (approx) | 0 (vidIQ waived) |
| Brand guardrails | Wonder over fearbait · no gore (the 005 red rules; cowpox only as soft healing marks) · the boy's test in one calm line · no present-day vaccine politics · HOS lane (the jab in your arm, and the moment we proved it works) |

## 1. Success targets

| Metric | Target |
|--------|--------|
| Title score | vidIQ waived; title checked against `THUMBNAIL_AND_TITLE_RULES.md` §1 instead |
| Primary keyword | neighbour phrases *vaccine* / *smallpox*; search phrase *how was the first vaccine made* (autocomplete) |
| Hook promise | "Every vaccine in the world is named after a cow." The same promise on the thumbnail (a cow, the word VACCA → VACCINE) and in the opening VO |
| Retention design | Five acts, each a cause-and-effect step: the speckled monster → the milkmaids' secret → a pail, a lancet and a boy → the test → the word that saved millions |
| Packaging | One object per thumbnail: the cow, or the milkmaid's hand beside a lancet |

## 2. Keyword research

**Public signals only.** "Autocomplete" means YouTube suggests the phrase as you type.

| Keyword | Autocomplete? | Top results (GB) | Competition read | Role | Keep? |
|---|---|---|---|---|---|
| how was the first vaccine made | **yes** (+ *who invented the first vaccine*) | SciShow 221K · WHO Europe 207K · Grunge 12K · TED-Ed *How do vaccines work?* 3.53M | Thin. Only SciShow tells the story at length | T&C title, description line 1 | yes |
| how did edward jenner discover the vaccine | **yes** (*edward jenner vaccine story*) | BBC Bitesize 306K · WHO Europe 207K · small channels ≤1.1K · TED-Ed smallpox 9.14M | Thin; Bitesize is a classroom dramatisation | description, tags, Part 02 | yes |
| first vaccine smallpox cowpox | related | TED-Ed smallpox 9.14M · Bitesize 306K · small channels | Low | tags | yes |
| why vaccines are named after a cow | no | small channels ≤858 views | **Very low.** Nobody owns the wording | main title | yes |
| vaccine / smallpox (neighbour phrases) | n/a | TED-Ed *How we conquered the deadly smallpox virus* 9.14M · TED-Ed *How do vaccines work?* 3.53M · Kurzgesagt vaccines 17.9M · Amoeba Sisters 1.38M · Be Smart 1.12M | These are the neighbours we want to be suggested beside | title, description opening, tags | yes |

**Decision:** neighbour phrase **vaccine** leads the title. *Smallpox*, *Edward Jenner* and *cowpox* go in the description's first two lines and the tags.
**Description first 100 characters must include:** *vaccine*, *smallpox* (`Descriptions/vaccine_long_description_v01.txt`, line 1–2).

## 3. Title ABC

| | Title | vidIQ score | Rules check | Keep? |
|---|-------|------:|-------|-------|
| A | Why Vaccines Are Named After a Cow | waived | Pass: familiar noun first (*Vaccines*), one real object, the familiar thing turned strange, holds *vaccine*, 34 chars, no formula | **Main (proposed)** |
| B | How Was the First Vaccine Made? | waived | Pass: the searched question (autocomplete), holds *vaccine*, 31 chars | **Test & Compare (proposed)** |
| C | The Milkmaid's Hands That Made the First Vaccine | waived | No autocomplete, no edge (tested 3 Oct) | park |
| Reject | How Did We Discover Vaccines? | — | Retired formula | **Reject** |

**Locked title:** proposed, not locked. Claude reviews; Ben's final OK covers the package.

## 3b. Script reviewer

```bash
cd 07_Content-Ops && npm run review:script -- --file ../02_Video-Projects/007_The-First-Vaccine/01_Script/vaccine_script_master_v01.md
```

- [x] Script reviewer ≥ 90: **92.3** on v01 (4 Oct 2026).

## 4. Outlier / competitive patterns

| Outlier / pattern | Views | Steal (structure) | Do **not** copy |
|---|---|---|---|
| TED-Ed *How we conquered the deadly smallpox virus* | 9.14M | Explains how smallpox was beaten worldwide; we start earlier, with the one test that made it possible | its wording or its global-campaign focus |
| SciShow *The Untold Story of the First Vaccine* | 221K | Tells the precursors (variolation, Jesty) honestly; we do the same in one line | its talking-head format |
| BBC Bitesize *The life and work of Edward Jenner* | 306K | The village, the milkmaid, the boy, told as story | the classroom tone |

**Patterns we will use:** assumption-flip (milkmaids' rumour → proof); one real date (14 May and 1 July 1796); slow reveal (the cow's name inside the word); body-scale anchor (every jab you have ever had).

## 5. Incorporate into the build

| Data finding | Change |
|---|---|
| Neighbour phrases *vaccine* / *smallpox* | In the title, the description's first line and the tags; *smallpox* named by 0:20 |
| *how was the first vaccine made* is searched | Spoken by 0:05 ("So how did a cow end up inside the most important medicine ever made?"); T&C title |
| *edward jenner* searches are thin | Jenner named by about 2:30; Parts 03–04 are the case, step by step |
| "named after a cow" is unowned | It's the main title and the payoff (Pasteur, 1881) |

**Chapter list after audit:**

1. Cold open: the speckled monster (no card)
2. The Milkmaids' Secret
3. A Pail, a Lancet and a Boy
4. The Test
5. The Word That Saved Millions

## 6. Retention plan

| Minute zone | Job | Picture / VO |
|---|---|---|
| 0–0:05 | Curiosity spike | the cow and VACCA → VACCINE (answer image) |
| ~0:15 | Stakes | three in ten died; "which would you choose?" |
| ~0:30 | Journey clear | a pail, a lancet, a book |
| Chapter starts | Re-hook | each act ends on a question (a list of stories isn't proof; would it protect him?) |
| Mid | Teach while the story moves | cowpox (Part 02), the case (03), the test and the book (04) |
| Final chapter | Payoff + bigger question | the cow's name in every vaccine; smallpox gone in 1980; hand-off to the next film |

## 7. Sign-off (block production until checked)

- [x] Keywords pulled and primary locked: public signals done (§2); vidIQ waived by Ben (standing rule)
- [x] Title proposed: *Why Vaccines Are Named After a Cow*, T&C *How Was the First Vaccine Made?*
- [x] Script reviewer ≥ 90: 92.3 on v01
- [x] Outlier patterns mapped into the chapter arc
- [x] Thumb concepts match the title promise (one object · one emotion)
- [x] Chapter teach-points listed (5 acts)
- [x] Cold-open clock (5 / 15 / 30 s) written
- [x] Retention plan filled
- [x] Production checklist path noted: `11_Upload-Package/PRODUCTION_CHECKLIST_V2.md`

**Signed off by:** Claude (desk reviewer); vidIQ waived by Ben, standing rule (desk PR #180, comment 5949981415)
**Date:** 4 Oct 2026

**Only then:** VO (Ben Orbit Narrator) → plates → edit, each stage to Claude on the desk.
