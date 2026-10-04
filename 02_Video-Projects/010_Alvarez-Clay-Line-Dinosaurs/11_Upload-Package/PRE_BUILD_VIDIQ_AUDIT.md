# Pre-build audit — 010 Dinosaurs (Alvarez and the clay line)

Filled 4 Oct 2026 by write lane from public signals: `evidence_2026-10-04_public_search.json` (YouTube GB autocomplete and top results, signed out) and `evidence_2026-10-04_neighbours.json` (`neighbours.py`, gate PASS: 10 education videos at 1M+, TED-Ed/TED present). **vidIQ is waived by Ben's standing rule** (desk PR #180, comment 5949981415), so there are no vidIQ scores.

## Episode

| Field | Value |
|-------|-------|
| ID / slug | 010 · `010_Alvarez-Clay-Line-Dinosaurs` |
| Working title | *What Killed the Dinosaurs Was Hidden in a Line of Clay* |
| Date pulled | 2026-10-04 |
| Credits used (approx) | 0 (vidIQ waived) |
| Brand guardrails | Clay / iridium first · no CGI extinction trailer as hero · Chicxulub is after-act · birds as living dinosaurs soft · HOS lane (the paper and the line in the rock) |

## 1. Success targets

| Metric | Target |
|--------|--------|
| Title score | vidIQ waived; title checked against `THUMBNAIL_AND_TITLE_RULES.md` §1 instead |
| Primary keyword | neighbour phrases *dinosaur extinction* / *asteroid alvarez iridium* / *alvarez dinosaurs*; search phrase *what killed the dinosaurs* (autocomplete, crowded) |
| Hook promise | "The answer was hidden in a line of rock as thin as a pencil." Same promise on the thumbnail (clay line / fingertip) and in the opening VO |
| Retention design | Five acts: the line in the rock → Gubbio → clock of stardust → too much iridium → crater and the birds |
| Packaging | One object per thumbnail: the clay line in limestone, or the iridium spike graph |

## 2. Keyword research

**Public signals only.** "Autocomplete" means YouTube suggests the phrase as you type.

| Keyword | Autocomplete? | Competition read | Role | Keep? |
|---|---|---|---|---|
| what killed the dinosaurs | **yes** | Extremely crowded (Kurzgesagt, BBC, Discovery CGI explainers) | cold open question; **not** unique title alone | yes (hook only) |
| alvarez asteroid iridium | **no** | Opportunity — underused vs bare extinction | description, tags, Parts 03–04 | yes |
| dinosaur extinction | **yes** | Heavy competition | neighbour phrase, tags | yes |
| chicxulub | mixed | After-act; crater explainers exist | Part 05, tags | yes |
| iridium dinosaurs / clay line | weak | Owns the HOS angle | title, description line 1 | yes |

**Decision:** *clay* and *dinosaurs* lead the title; *asteroid* and *iridium* go in the description's first line; *Alvarez* / *Chicxulub* in tags and later chapters. Do not fight bare "what killed the dinosaurs" as the only title — own the clay/iridium paper angle.
**Description first 100 characters must include:** *dinosaurs*, *asteroid*, *iridium* (`Descriptions/clay_long_description_v01.txt`, line 1).

## 3. Title ABC

| | Title | vidIQ score | Rules check | Keep? |
|---|-------|------:|-------|-------|
| A | What Killed the Dinosaurs Was Hidden in a Line of Clay | waived | Pass: familiar question + unexpected answer (*line of clay*), one real object, unowned clay angle, ~58 chars | **Main (proposed)** |
| B | The Line of Clay That Ended the Dinosaurs | waived | Pass: object-first, clay owned, 42 chars | **Test & Compare (proposed)** |
| C | How an Asteroid Killed the Dinosaurs | waived | Fails differentiation — already owned by giants | **Reject** |

**Locked title:** proposed, not locked. Claude reviews; Ben's final OK covers the package.

## 3b. Script reviewer

```bash
cd 07_Content-Ops && npm run review:script -- --file ../02_Video-Projects/010_Alvarez-Clay-Line-Dinosaurs/01_Script/clay_script_master_v01.md
```

- [x] Script reviewer ≥ 90: **92.1** on v01 (4 Oct 2026, PR #208 merged), 8/8 structure gates.

## 4. Outlier / competitive patterns

| Outlier / pattern | Views | Steal (structure) | Do **not** copy |
|---|---|---|---|
| Kurzgesagt *The Day the Dinosaurs Died* | ~23M | Minute-by-minute stakes pacing | CGI impact trailer as hero |
| Kurzgesagt *How The Dinosaurs Actually Died* | ~8.8M | Clear cause chain | its exact framing |
| SciShow *How the Dinosaurs Actually Went Extinct* | ~3.1M | Myth vs evidence teach | presenter format |
| Be Smart *Did Dinosaurs Really Go Extinct?* | ~3.9M | Birds-as-dinosaurs twist | its wording |

**Patterns we will use:** clay-line proof object; one real date (6 June 1980, *Science*); iridium spike graph; crater after-act; birds still here.

## 5. Incorporate into the build

| Data finding | Change |
|---|---|
| Neighbour phrases *dinosaur extinction* / *asteroid alvarez iridium* | In the title (dinosaurs + clay), description line 1 (*dinosaurs*, *asteroid*, *iridium*), and tags |
| *what killed the dinosaurs* is searched and crowded | Cold-open question only; title owns clay answer |
| *alvarez asteroid iridium* autocomplete empty | Opportunity phrase in tags/description |
| Birds / surviving dinosaurs in Be Smart | Part 05 payoff soft |

**Chapter list after audit:**

1. Cold open: The Line in the Rock (no card)
2. The Gorge at Gubbio
3. A Clock Made of Stardust
4. Too Much Iridium
5. The Crater and the Birds

## 6. Retention plan

| Minute zone | Job | Picture / VO |
|---|---|---|
| 0–0:05 | Curiosity spike | clay line + fingertip (answer image) |
| ~0:15 | Stakes | vial · hammer · paper |
| ~0:30 | Journey clear | more than 160 Myr → gone |
| Chapter starts | Re-hook | each act ends on a question (how do you clock mud? where is the hole?) |
| Mid | Teach while the story moves | forams (02), iridium clock (03), spike + supernova drop (04), Chicxulub + birds (05) |
| Final chapter | Payoff + bigger question | robin / living dinosaur; clay line again |

## 7. Sign-off (block production until checked)

- [x] Keywords pulled and primary locked: public signals done (§2); vidIQ waived by Ben (standing rule)
- [x] Title proposed: *What Killed the Dinosaurs Was Hidden in a Line of Clay*, T&C *The Line of Clay That Ended the Dinosaurs*
- [x] Script reviewer ≥ 90: 92.1 on v01 (#208)
- [x] Outlier patterns mapped into the chapter arc
- [x] Thumb concepts match the title promise (one object · one emotion)
- [x] Chapter teach-points listed (5 acts)
- [x] Cold-open clock (5 / 15 / 30 s) written
- [x] Retention plan filled
- [x] Production checklist path noted: `11_Upload-Package/PRODUCTION_CHECKLIST_V2.md`

**Signed off by:** write lane (Grok Bot) scaffold; vidIQ waived by Ben, standing rule (desk PR #180, comment 5949981415). Claude still confirms FACT_NOTES / hard-checks before VO.
**Date:** 4 Oct 2026

**Only then:** Claude PASS on FACT_NOTES + HARD_CHECKS → VO (Ben Orbit Narrator) → plates → edit, each stage to Claude on the desk.
