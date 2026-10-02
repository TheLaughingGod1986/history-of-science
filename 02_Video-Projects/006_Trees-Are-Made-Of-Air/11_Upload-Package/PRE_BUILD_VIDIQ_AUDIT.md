# Pre-build audit — 006 Trees are made of air (van Helmont → photosynthesis)

Filled 2 Oct 2026 from public signals: `evidence_2026-10-02_public_search.json` (YouTube GB autocomplete + top results, signed out), `evidence_2026-10-02_neighbours.json` and `evidence_2026-10-02_neighbours_manifest.json` (`neighbours.py`), and the title check in `00_Brand/Channel-Setup/audits/topic_packs_2026-10-02_006/titles_public_search.txt` (#190). **vidIQ is waived by Ben's standing rule** (relayed by Claude on desk PR #180, comment 5949981415), so there are no vidIQ scores.

## Episode

| Field | Value |
|-------|-------|
| ID / slug | 006 · `006_Trees-Are-Made-Of-Air` |
| Working title | *The Willow Tree That Was Made of Air* |
| Date pulled | 2026-10-02 |
| Credits used (approx) | 0 (vidIQ waived) |
| Brand guardrails | Wonder over fearbait · no animal harm on screen (Priestley's mouse only alive and well) · HOS lane (the tree outside your window, and the moment we found out it's made of air) |

## 1. Success targets

| Metric | Target |
|--------|--------|
| Title score | vidIQ waived; title checked against `THUMBNAIL_AND_TITLE_RULES.md` §1 instead |
| Primary keyword | neighbour phrases *tree* / *photosynthesis*; search phrase *where do trees get their mass* (autocomplete) |
| Hook promise | "A fully grown tree is built almost entirely out of thin air." Same promise on the thumb (the willow on the scales, MADE OF AIR) and in the open VO |
| Retention design | Five acts, each a cause-and-effect step: plants eat soil → the willow and the wrong answer → mint repairs the air → only in light → carbon from the sky |
| Packaging | One object per thumb: the willow in its pot on a brass balance against a pinch of soil |

## 2. Keyword research

**Public signals only.** "Autocomplete" means YouTube suggests the phrase as you type.

| Keyword | Autocomplete? | Top results (GB) | Competition read | Role | Keep? |
|---|---|---|---|---|---|
| where do trees get their mass | **yes** | Veritasium 2.54M · Seriously Dave? 3K · Scientia 29K · ScienceChannel9000 49K · AskaBiologist 74K | Low apart from Veritasium (who asks it as a physics puzzle, not as the history) | T&C title, description line 1 | yes |
| van helmont willow tree experiment | **yes** | Treasure Of World 881 · VIS PHILO. 894 / 3.7K · Homework Clinic 67K · LSGScience 43K | **Very low.** Nobody tells the story in full | description, tags, chapter 2 | yes |
| where does a tree's weight come from | related only | Veritasium 2.54M · Friends of the Earth 1.7K · Physics Daily 1.23M | Low | T&C title | yes |
| the willow tree that was made of air | related: *the willow tree experiment* | the song *The Willow Tree* (Topic, Trojan Records 719K) · Treasure Of World 881 | Low; the song owns the bare phrase, *made of air* separates us | main title | yes |
| tree / photosynthesis (neighbour phrases) | n/a | CrashCourse *Photosynthesis* 9.24M · Kurzgesagt *Trees Are So Weird* 6.71M · Amoeba Sisters *Photosynthesis* 6.18M · TED-Ed *The simple story of photosynthesis and food* 2.22M · Khan Academy *Photosynthesis* 2.18M · TED-Ed *How tall can a tree grow?* 1.41M | These are the neighbours we want to be suggested beside | title, description opening, tags | yes |

**Decision:** neighbour phrase **tree** leads the title; *photosynthesis*, *van helmont* and *where do trees get their mass* go in the description's first two lines and the tags.
**Description first 100 characters must include:** *tree*, *photosynthesis*. Draft line 1: "A fully grown tree is built almost entirely out of thin air. This is how we found out, from van Helmont's willow to photosynthesis."

## 3. Title ABC

| | Title | vidIQ score | Rules check | Keep? |
|---|-------|------:|-------|-------|
| A | The Willow Tree That Was Made of Air | waived | Pass: familiar noun in the first four words (*Willow Tree*), one real object, the familiar thing turned strange, holds *tree*, 36 chars, no formula | **Main (proposed)** |
| B | Where Does a Tree's Weight Come From? | waived | Pass: the searched question, holds *tree*, 37 chars; not Veritasium's wording | **Test & Compare (proposed)** |
| C | Trees Are Made of Air, Not Soil | waived | Holds *tree*; reads as a fact, but loses the willow and the story | park |
| Reject | Where Do Trees Get Their Mass? | — | Veritasium's live title | **Reject** |
| Reject | How Did We Discover Photosynthesis? | — | Retired formula | **Reject** |

**Locked title:** proposed, not locked. Claude reviews the script and titles; Ben's final OK covers the package.

## 3b. Script reviewer

```bash
cd 07_Content-Ops && npm run review:script -- --file ../02_Video-Projects/006_Trees-Are-Made-Of-Air/01_Script/trees_script_master_v01.md
```

- [x] Script reviewer ≥ 90: **93.8** on v01 (2 Oct 2026); output pasted in `production-status.md`.

## 4. Outlier / competitive patterns

| Outlier / pattern | Views | Steal (structure) | Do **not** copy |
|---|---|---|---|
| Veritasium *Where Do Trees Get Their Mass?* | 2.54M | The street-interview surprise: people say "the soil". We open on that wrong answer and follow the 180 years it took to fix | its title or its interview format |
| TED-Ed *The simple story of photosynthesis and food* | 2.22M | Explains *what* photosynthesis is; we start where it stops: *how we found out* | its wording |
| Homework Clinic *van Helmont's experiment* | 67K | The willow numbers told plainly | a worksheet tone |

**Patterns we will use:** assumption-flip (trees eat soil → trees are made of air); one real number (169 pounds of tree, two ounces of soil); slow reveal (the gas he named, the light, then the carbon); body-scale anchor (your food, your breath).

## 5. Incorporate into the build

| Data finding | Change |
|---|---|
| Neighbour phrases *tree* / *photosynthesis* | In the title, the description's first line and the tags; *photosynthesis* named in Part 04 |
| *where do trees get their mass* is searched | Spoken as the title question by 0:08 ("So where does a tree's weight really come from?"); T&C title |
| *van helmont willow* is searched and thin | Named by 0:45; Part 02 is the experiment, step by step |
| Veritasium owns the bare question | Our hook is the history: the room, the pot, the scales, shown in 3D cartoon |

**Chapter list after audit:**

1. Cold open: plants eat soil? (no card)
2. Five Years and Two Ounces
3. The Air That Mint Repaired
4. Bubbles in the Sunlight
5. Carbon From the Sky

## 6. Retention plan

| Minute zone | Job | Picture / VO |
|---|---|---|
| 0–0:05 | Curiosity spike | the willow drinking threads of air (answer image) |
| ~0:15 | Stakes | "if it was wrong, nobody really knew where wood, or food, or even the air we breathe came from" (0:22) |
| ~0:30 | Journey clear | a pot, a jar, the sun |
| Chapter starts | Re-hook | each act ends on a question (so why had it grown? why only sometimes? what was it taking in?) |
| Mid | Teach while the story moves | the scales (Part 02), the candle and mint (03), the bubbles (04) |
| Final chapter | Payoff + bigger question | carbon from the air; your food and breath; hand-off to the atom |

## 7. Sign-off (block production until checked)

- [x] Keywords pulled and primary locked: public signals done (§2); vidIQ waived by Ben (standing rule)
- [x] Title proposed: *The Willow Tree That Was Made of Air*, T&C *Where Does a Tree's Weight Come From?* (rules check passed; Claude reviews, Ben's final OK covers it)
- [x] Script reviewer ≥ 90: 93.8 on v01
- [x] Outlier patterns mapped into the chapter arc
- [x] Thumb concepts match the title promise (one object · one emotion)
- [x] Chapter teach-points listed (5 acts)
- [x] Cold-open clock (5 / 15 / 30 s) written
- [x] Retention plan filled
- [x] Production checklist path noted: `11_Upload-Package/PRODUCTION_CHECKLIST_V2.md`

**Signed off by:** vidIQ waived by Ben, standing rule (relayed by Claude on desk PR #180, comment 5949981415, 2 Oct 2026)
**Date:** 2 Oct 2026

**Only then:** VO (Ben Orbit Narrator) → Veo plates → edit, each stage to Claude on the desk.
