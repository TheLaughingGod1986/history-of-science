# Pre-build audit — 005 Blood (Harvey)

Filled 1 Oct 2026 from public signals: `evidence_2026-10-01_public_search.json` (YouTube GB autocomplete + top results, signed out) and `evidence_2026-10-01_neighbours.json` (`neighbours.py`). **vidIQ numbers need Ben's login: pending Ben.**

## Episode

| Field | Value |
|-------|-------|
| ID / slug | 005 · `005_How-Harvey-Proved-Blood-Circulates` |
| Working title | *The Tied Arm That Proved Your Blood Circulates* |
| Date pulled | 2026-10-01 |
| Credits used (approx) | 0 (no vidIQ yet) |
| Brand guardrails | Wonder over fearbait · no gore, no live-animal cruelty on screen · HOS lane (the pulse in your wrist, and the moment we found out the blood goes round) |

## 1. Success targets

| Metric | Target |
|--------|--------|
| Title score | vidIQ ≥ 90: **pending Ben** |
| Primary keyword | *william harvey* (in autocomplete); neighbour phrase *blood* / *heart* |
| Hook promise | "Your heart pumps more blood in half an hour than your whole body holds." Same promise on the thumb (the band / the jugs) and in the open VO |
| Retention design | Five acts, each a cause-and-effect step: old belief → valves → the sum → the tied arm → the missing capillaries |
| Packaging | One object per thumb (the tied arm; the flask-scale hero is the arm and band, or the tower of jugs) |

## 2. Keyword research

**Public signals only.** "Autocomplete" means YouTube suggests the phrase as you type. vidIQ Overall / Est./mo / Comp: *pending Ben*.

| Keyword | Autocomplete? | Top results (GB) | Competition read | Role | Keep? |
|---|---|---|---|---|---|
| how did harvey prove blood circulates | no | Few Minutes Knowledge 11.5K · HomeschoolingresourcesUK 48 · The Field Notebook 2 (posted 30 Sep) · Royal College of Physicians 46K · Scientists to Sleep 7 | **Very low.** No big channel owns the Harvey story | the film's question; description line 1 | yes |
| william harvey | **yes** | Royal College of Physicians 46K · East Kent Hospitals 4K · de Nicola Center 1.8K · BBC Bitesize for Teachers 320K · World Science Festival 126K | Low–medium; small or institutional channels | tags, description, chapter 3 | yes |
| blood circulation discovery | related: "william harvey blood circulation discovery" | Royal College of Physicians 46K · OpenMind 888K · Few Minutes Knowledge 11.5K · Mayo Clinic 8.2M · Learn Bright 3.4M | Medium (the big ones are explainers, not the discovery story) | description | yes |
| blood / heart (neighbour phrases) | n/a | TED-Ed *How the heart actually pumps blood* 4.46M · CrashCourse *The Heart, Part 1* 8.07M · Amoeba Sisters *Circulatory System…* 7.39M · TED-Ed *How blood pressure works* 17.96M | These are the neighbours we want to be suggested beside | title, description opening, tags | yes |

**Decision (draft):** neighbour phrase **blood** leads the title; *william harvey* and *blood circulation* go in the description's first two lines and the tags.
**Description first 100 characters must include:** *heart*, *blood*. Draft line 1: "Your heart pumps more blood in half an hour than your whole body holds…"

## 3. Title ABC

| | Title | vidIQ score | Rules check | Keep? |
|---|-------|------:|-------|-------|
| A | The Tied Arm That Proved Your Blood Circulates | *pending Ben* | Pass: familiar noun first (*arm*), one real object, holds *blood*, 46 chars, no formula | **Main (proposed)** |
| B | Why Doctors Thought Your Blood Was Used Up | *pending Ben* | Pass: the old belief as a question, holds *blood*, 42 chars | **Test & Compare (proposed)** |
| C | Your Heart Pumps More Blood Than You Have | *pending Ben* | Holds *heart* and *blood*; reads as a body fact, but "than you have" drops the half hour, so the claim is loose | park |
| Reject | Your Blood Goes Round in a Circle… | — | Too close to The Field Notebook's live title | **Reject** |
| Reject | How Did We Discover Blood Circulation? | — | Retired formula | **Reject** |

**Locked title:** *The Tied Arm That Proved Your Blood Circulates* (Ben, 1 Oct 2026, with the script v02). T&C: *Why Doctors Thought Your Blood Was Used Up*.

## 3b. Script reviewer

```bash
cd 07_Content-Ops && npm run review:script -- --file ../02_Video-Projects/005_How-Harvey-Proved-Blood-Circulates/01_Script/blood_script_master_v01.md
```

- [ ] Score ≥ 90: **84.4** on v01 (1 Oct 2026). Not passed. See the desk report for where the points go.

## 4. Outlier / competitive patterns

| Outlier / pattern | Views | Steal (structure) | Do **not** copy |
|---|---|---|---|
| TED-Ed *How the heart actually pumps blood* | 4.46M | Explains *what* the heart does; we start where it stops: *how we found out* | its wording or title |
| Royal College of Physicians *Ceaseless motion* | 46K, 8 yr | The real room and the real experiments, told plainly | a lecture tone |
| The Field Notebook (posted 30 Sep) | 2 | — | its title wording ("goes round in a circle", "without seeing it") |

**Patterns we will use:** assumption-flip (the blood is used up → it goes round); one real number (more in half an hour than the body holds); slow reveal (the capillaries, after Harvey's death); body-scale anchor (the pulse in your wrist, the veins on your hand, a blood pressure cuff).

## 5. Incorporate into the build

| Data finding | Change |
|---|---|
| Neighbour phrase *blood* / *heart* | In the title, the description's first line and the tags |
| *william harvey* is searched | Named by 0:45, in the tags and the description |
| No big channel owns the Harvey story | Our hook: the room, the band, the sum, shown in 3D cartoon |
| TED-Ed *How blood pressure works* (17.96M) | Part 05 ends on the blood pressure cuff as Harvey's band |

**Chapter list after audit:**

1. Cold open: where does all that blood go? (no card)
2. The Liver That Made Blood
3. The Sum That Broke the Old Idea
4. The Tied Arm
5. The Vessels He Never Saw

## 6. Retention plan

| Minute zone | Job | Picture / VO |
|---|---|---|
| 0–0:05 | Curiosity spike | the pulse in a wrist, the red stream racing to the heart |
| ~0:15 | Stakes | "If it was wrong, medicine had the human body backwards" (0:35) |
| ~0:30 | Journey clear | a sum, a band, little doors |
| Chapter starts | Re-hook | each act opens on a question (why believe it? why doors? why does the hand go pale?) |
| Mid | Teach while the story moves | the jugs (the sum), the tied arm (the valves) |
| Final chapter | Payoff + bigger question | capillaries close the circle; the cuff; hand-off to germs |

## 7. Sign-off (block production until checked)

- [x] Keywords pulled and primary locked: public signals done (§2); **vidIQ waived by Ben, 1 Oct 2026**
- [x] Title locked: *The Tied Arm That Proved Your Blood Circulates*, with the script v02 sign-off (Ben, 1 Oct 2026, "1–5 yes, 29 Oct")
- [ ] Script reviewer ≥ 90: **89.8** on v02 with the fixed reviewer (#185). Not ≥ 90; Ben signed off v02 on 1 Oct 2026 (gate override, STUDIO_PLAYBOOK §2)
- [x] Outlier patterns mapped into the chapter arc
- [x] Thumb concepts match the title promise (one object · one emotion)
- [x] Chapter teach-points listed (5 acts)
- [x] Cold-open clock (5 / 15 / 30 s) written
- [x] Retention plan filled
- [x] Production checklist path noted: `11_Upload-Package/PRODUCTION_CHECKLIST_V2.md`

**Signed off by:** vidIQ waived by Ben, 1 Oct 2026 (in chat with Claude: "waive vidIQ, merge #186 and voice OK"; relayed on desk PR #180)
**Date:** 1 Oct 2026

The script score stays 89.8 on Ben's recorded override (as on 004).

**Only then:** VO (Ben Orbit Narrator) → Flow Veo plates → edit.
