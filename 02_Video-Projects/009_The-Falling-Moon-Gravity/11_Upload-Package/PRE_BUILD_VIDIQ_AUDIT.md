# Pre-build audit — 009 Gravity (the falling Moon)

Filled 4 Oct 2026 by write lane (Grok) from public signals: `evidence_2026-10-04_public_search.json` (YouTube GB autocomplete and top results, signed out) and `evidence_2026-10-04_neighbours.json` (`neighbours.py`, gate PASS: 5 education videos at 1M+, TED-Ed present). **vidIQ is waived by Ben's standing rule** (desk PR #180, comment 5949981415), so there are no vidIQ scores.

**UNSIGNED for Claude** — desk claim 5982314076: Claude signs this audit before production proceeds.

## Episode

| Field | Value |
|-------|-------|
| ID / slug | 009 · `009_The-Falling-Moon-Gravity` |
| Working title | *Why Doesn't the Moon Fall to Earth?* |
| Date pulled | 2026-10-04 |
| Credits used (approx) | 0 (vidIQ waived) |
| Brand guardrails | Wonder over fearbait · Moon falling first, apple second · apple never hits head · no "Newton invented gravity" · orbit = continuous miss · spray-paint = teaching only · HOS lane (same pull for apple and Moon) |

## 1. Success targets

| Metric | Target |
|--------|--------|
| Title score | vidIQ waived; title checked against `THUMBNAIL_AND_TITLE_RULES.md` §1 instead |
| Primary keyword | neighbour phrases *gravity* / *newton* / *moon*; search phrase *why doesn't the moon fall to earth* (autocomplete) |
| Hook promise | "Right now, as you watch this, the Moon is falling towards the Earth." Same promise on the thumbnail (falling Moon / orbit curve) and in the opening VO |
| Retention design | Five acts: falling Moon → apple in a plague year → cannon on the mountain → Moon test / Principia → falling around the world (comet, tides, ISS) |
| Packaging | One object per thumbnail: the Moon on its falling curve, or apple + Moon in one frame |

## 2. Keyword research

**Public signals only.** "Autocomplete" means YouTube suggests the phrase as you type.

| Keyword | Autocomplete? | Competition read | Role | Keep? |
|---|---|---|---|---|
| why doesn't the moon fall to earth | **yes** | NASA Night Sky Network ~2.2M; BYJU'S ~1.0M; mostly short explainers | main title | yes |
| the moon is falling | soft | Unowned story-led wording | T&C title | yes |
| newton gravity moon | weak suggest | Crash Course Newtonian Gravity ~1.4M; TED-Ed Newton laws | description, tags | yes |
| newton apple | soft | Folklore-heavy; keep as garnish not hero | tags only | soft |
| gravity / moon / newton (neighbour phrases) | n/a | TED-Ed three-body ~9.9M · Veritasium gravity ~15.5M · TED-Ed Newton laws ~2.9M · Crash Course ~1.4M | title, description opening, tags | yes |

**Decision:** *Moon* and *fall* lead the title; *gravity*, *Moon* and *Newton* go in the description's first line; *Principia* / Halley / orbit in tags.
**Description first 100 characters must include:** *gravity*, *moon*, *Newton* (`Descriptions/moon_long_description_v01.txt`, line 1).

## 3. Title ABC

| | Title | vidIQ score | Rules check | Keep? |
|---|-------|------:|-------|-------|
| A | Why Doesn't the Moon Fall to Earth? | waived | Pass: familiar mystery, one real object (Moon), searched wording, 37 chars | **Main (proposed)** |
| B | The Moon Is Falling Right Now | waived | Pass: present-tense hook matching cold open; 29 chars | **Test & Compare (proposed)** |
| C | Newton's Apple and the Moon | waived | Weak: apple-first fights house lock (Moon first) | **Reject** |

**Locked title:** proposed, not locked. Claude reviews; Ben's final OK covers the package.

## 3b. Script reviewer

```bash
cd 07_Content-Ops && npm run review:script -- --file ../02_Video-Projects/009_The-Falling-Moon-Gravity/01_Script/moon_script_master_v01.md
```

- [x] Script reviewer ≥ 90: **91.3** on v01 (Claude, 4 Oct 2026 / PR #208), structure PASS ~8.6 min.

## 4. Outlier / competitive patterns

| Outlier / pattern | Views | Steal (structure) | Do **not** copy |
|---|---|---|---|
| NASA Night Sky Network *Why Doesn't the Moon Fall to Earth?* | ~2.2M | Clear orbit-as-fall teach | classroom dryness |
| Veritasium *What Everyone Gets Wrong About Gravity* | ~15.5M | Myth-flip energy | presenter format / length |
| Crash Course *Newtonian Gravity* | ~1.4M | Inverse-square + Moon test beat | series tone |
| TED-Ed Newton three-body / 3 Laws | ~2.9–9.9M | Clean diagram teach | animation style copy |

**Patterns we will use:** myth-flip (Moon is falling / never hits); one clear scale (60 Earth radii); body-scale anchor (apple + ISS free-fall); Halley comet payoff date (Christmas 1758).

## 5. Incorporate into the build

| Data finding | Change |
|---|---|
| Neighbour phrases *gravity* / *newton* / *moon* | In the title, the description's first line and the tags; *falling Moon* spoken by 0:04 |
| *why doesn't the moon fall to earth* is searched | It's the main title and the cold-open question |
| Apple folklore dominates weak "newton apple" results | Keep apple as plague-year anecdote; Moon thought-experiment leads |
| NASA / BYJU'S own short explainers | Differentiate with Newton story + Principia / Halley / ISS arc |

**Chapter list after audit:**

1. Cold open: The Falling Moon (no card)
2. An Apple in a Plague Year
3. The Cannon on the Mountain
4. The Moon Test
5. Falling Around the World

## 6. Retention plan

| Minute zone | Job | Picture / VO |
|---|---|---|
| 0–0:05 | Curiosity spike | Moon falling on its curve (answer image) |
| ~0:15 | Stakes | apple, cannon, sum on the table |
| ~0:30 | Journey clear | two sets of rules (Earth vs heavens) |
| Chapter starts | Re-hook | each act ends on a question (how far does the pull reach? could he prove it?) |
| Mid | Teach while the story moves | cannon (03), 60 radii / 3600× / 1 min = 1 s (04), Halley + Principia (04–05) |
| Final chapter | Payoff + bigger question | comet 1758 · tides · ISS free-fall; hand-off to 010 clay / Alvarez |

## 7. Sign-off (block production until checked)

- [x] Keywords pulled and primary locked: public signals done (§2); vidIQ waived by Ben (standing rule)
- [x] Title proposed: *Why Doesn't the Moon Fall to Earth?*, T&C *The Moon Is Falling Right Now*
- [x] Script reviewer ≥ 90: 91.3 on v01 (Claude / PR #208)
- [x] Outlier patterns mapped into the chapter arc
- [ ] Thumb concepts match the title promise (one object · one emotion) — **await Claude**
- [x] Chapter teach-points listed (5 acts)
- [x] Cold-open clock (5 / 15 / 30 s) written
- [x] Retention plan filled
- [x] Production checklist path noted: `11_Upload-Package/PRODUCTION_CHECKLIST_V2.md`

**Signed off by:** **UNSIGNED — Claude** (desk claim 5982314076). Write lane filled public-signal sections; Claude signs before VO / picture.
**Date:** 4 Oct 2026 (draft)

**Only then:** Claude PASS on FACT_NOTES → VO (Ben Orbit Narrator) → plates → edit, each stage to Claude on the desk. **No picture mint from this PR.**
