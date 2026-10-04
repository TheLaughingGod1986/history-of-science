# Pre-build audit — 008 Lightning (Franklin's kite, 1752)

Filled 4 Oct 2026 by Claude from public signals: `evidence_2026-10-04_public_search.json` (YouTube GB autocomplete and top results, signed out) and `evidence_2026-10-04_neighbours.json` (`neighbours.py`, gate PASS: 6 education videos at 1M+, TED-Ed present). **vidIQ is waived by Ben's standing rule** (desk PR #180, comment 5949981415), so there are no vidIQ scores.

## Episode

| Field | Value |
|-------|-------|
| ID / slug | 008 · `008_Lightning-Franklin` |
| Working title | *Why Did Franklin Fly a Kite in a Storm?* |
| Date pulled | 2026-10-04 |
| Credits used (approx) | 0 (vidIQ waived) |
| Brand guardrails | Wonder over fearbait · no electrocution spectacle (Richmann told in one calm line, nothing shown) · the kite is never struck · priority care (Marly, May 1752, before the kite) · William is an adult · HOS lane (the rod on the roof you can see today) |

## 1. Success targets

| Metric | Target |
|--------|--------|
| Title score | vidIQ waived; title checked against `THUMBNAIL_AND_TITLE_RULES.md` §1 instead |
| Primary keyword | neighbour phrases *lightning* / *franklin* / *kite*; search phrase *how does a lightning rod work* (autocomplete) |
| Hook promise | "A grown man flew a kite into a thunderstorm, on purpose." The same promise on the thumbnail (the kite, the key, the spark) and in the opening VO |
| Retention design | Five acts, each a cause-and-effect step: fire from the sky → the sparks in a jar → a kite in the storm → the spark from the key → the rod on every roof |
| Packaging | One object per thumbnail: the kite in the storm cloud, or the knuckle and the key with a spark between |

## 2. Keyword research

**Public signals only.** "Autocomplete" means YouTube suggests the phrase as you type.

| Keyword | Autocomplete? | Competition read | Role | Keep? |
|---|---|---|---|---|
| why did franklin fly a kite | no | Nobody owns the wording | main title | yes |
| how does a lightning rod work | **yes** | How-it-works interest; no story-led answer | T&C title, Part 05, description | yes |
| franklin kite experiment | **yes** | Be Smart *The TRUE Story of Ben Franklin & His Kite* ~691K is the closest; little else tells it at length | description, tags, Parts 03–04 | yes |
| benjamin franklin lightning | **yes** | Competition present, mostly short or classroom | description line 1, tags | yes |
| who invented the lightning rod | **yes** | Priority myth risk | taught in Part 03 (Marly) | tags only |
| lightning / electricity (neighbour phrases) | n/a | SciShow Kids thunder/lightning ~5.6M · MinuteEarth lightning ~4.0M · TED-Ed static electricity ~3.6M · Kurzgesagt lightning ~2.1M | title, description opening, tags | yes |

**Decision:** *Franklin* and *kite* lead the title; *lightning* and *Benjamin Franklin* go in the description's first line; *lightning rod* in line 2 and the tags. Name collisions in the neighbour pool (Rosalind Franklin, a lightning myth) are ignored.
**Description first 100 characters must include:** *lightning*, *Franklin* (`Descriptions/lightning_long_description_v01.txt`, line 1).

## 3. Title ABC

| | Title | vidIQ score | Rules check | Keep? |
|---|-------|------:|-------|-------|
| A | Why Did Franklin Fly a Kite in a Storm? | waived | Pass: a familiar action (*fly a kite*) in a strange place (*a storm*), one real object, unowned wording, 39 chars | **Main (proposed)** |
| B | How Does a Lightning Rod Work? | waived | Pass: the searched question (autocomplete), the object on every tall roof, 30 chars | **Test & Compare (proposed)** |
| C | The Kite That Caught Lightning | waived | Fails the facts: the kite was never struck | **Reject** |

**Locked title:** proposed, not locked. Claude reviews; Ben's final OK covers the package.

## 3b. Script reviewer

```bash
cd 07_Content-Ops && npm run review:script -- --file ../02_Video-Projects/008_Lightning-Franklin/01_Script/lightning_script_master_v01.md
```

- [x] Script reviewer ≥ 90: **92.1** on v01 (4 Oct 2026), 8/8 structure gates.

## 4. Outlier / competitive patterns

| Outlier / pattern | Views | Steal (structure) | Do **not** copy |
|---|---|---|---|
| SciShow Kids *What Causes Thunder and Lightning?* | ~5.6M | One clear picture of charge building in a cloud | the kids' tone |
| MinuteEarth lightning | ~4.0M | Fast hand-drawn teach of the path to ground | its survival framing |
| Be Smart *The TRUE Story of Ben Franklin & His Kite* | ~691K | Myth-busting (the kite was never struck) | its wording or presenter format |

**Patterns we will use:** myth-flip (the kite was never hit); one real date (19 October 1752, the *Gazette*); proof you can see (threads stand up, then a spark from the key); body-scale anchor (the rod on the tallest building you can see).

## 5. Incorporate into the build

| Data finding | Change |
|---|---|
| Neighbour phrases *lightning* / *franklin* / *kite* | In the title, the description's first line and the tags; *lightning* spoken by 0:20 |
| *how does a lightning rod work* is searched | Answered plainly in Part 05 and teased at 0:07 ("the answer on its roof"); T&C title |
| *who invented the lightning rod* is searched with a myth attached | Part 03 tells Marly first, then the kite |
| "why did franklin fly a kite" is unowned | It's the main title and the cold-open question |

**Chapter list after audit:**

1. Cold open: fire from the sky (no card)
2. The Sparks in a Jar
3. A Kite in the Storm
4. The Spark From the Key
5. The Rod on Every Roof

## 6. Retention plan

| Minute zone | Job | Picture / VO |
|---|---|---|
| 0–0:05 | Curiosity spike | the kite in the storm, spark from the key (answer image) |
| ~0:15 | Stakes | steeples on fire; "what would you…" the burning barn |
| ~0:30 | Journey clear | a kite, a key, a jar |
| Chapter starts | Re-hook | each act ends on a question (how do you catch lightning without it killing you? could it protect homes?) |
| Mid | Teach while the story moves | the Leyden jar (02), the sentry-box and Marly (03), charge not a bolt (04), the safe path to ground (05) |
| Final chapter | Payoff + bigger question | the rod on the tallest building you can see; hand-off to 009 (the falling Moon) |

## 7. Sign-off (block production until checked)

- [x] Keywords pulled and primary locked: public signals done (§2); vidIQ waived by Ben (standing rule)
- [x] Title proposed: *Why Did Franklin Fly a Kite in a Storm?*, T&C *How Does a Lightning Rod Work?*
- [x] Script reviewer ≥ 90: 92.1 on v01
- [x] Outlier patterns mapped into the chapter arc
- [x] Thumb concepts match the title promise (one object · one emotion)
- [x] Chapter teach-points listed (5 acts)
- [x] Cold-open clock (5 / 15 / 30 s) written
- [x] Retention plan filled
- [x] Production checklist path noted: `11_Upload-Package/PRODUCTION_CHECKLIST_V2.md`

**Signed off by:** Claude (desk reviewer); vidIQ waived by Ben, standing rule (desk PR #180, comment 5949981415)
**Date:** 4 Oct 2026

**Only then:** FACT_NOTES for the script's new claims → VO (Ben Orbit Narrator) → plates → edit, each stage to Claude on the desk.
