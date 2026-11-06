# Pre-build audit — 011 Anesthesia (Ether Day, 1846 and surgery before anesthesia)

Filled 5 Nov 2026 from public signals collected in `00_Brand/Channel-Setup/ideas/evidence_2026-10-12_J0180/` (`n_anaesthesia2.json`, `public_search.json`, `public_search2.json`) and `11_Upload-Package/evidence_2026-11-05_neighbours.json` / `evidence_2026-11-05_public_search.json` (`neighbours.py`, gate PASS: 5 education videos at 1M+, TED-Ed/TED present). **vidIQ is waived by Ben's standing rule** (desk PR #180, comment 5949981415), so there are no vidIQ scores.

## Episode

| Field | Value |
|-------|-------|
| ID / slug | 011 · `011_Surgery-Before-Anaesthesia` |
| Air date | **Thu 10 Dec 2026** 18:00 UK (`2026-12-10T18:00:00.000Z`) |
| Working title | *Anesthesia: The Day Surgery Stopped Hurting* (T&C B: *What Surgery Was Like Before Anesthesia*) |
| Date pulled | 2026-10-12 / 2026-11-05 |
| Credits used (approx) | 0 (vidIQ waived) |
| Brand guardrails | US spelling *Anesthesia* in title/tags (matches 19.7M & 2.65M TED-Ed neighbours, Chief lock J0180), UK *anaesthesia* allowed in description/VO · no gore (pain told through speed, stopwatch, straps) · Liston "Yankee dodge", Warren "no humbug" and Liston patient wakeup hedged as "is said to have" (`J0198` / `J0224`) · Simpson dinner party "out cold on the floor" · RCoA 1-in-100,000 stadium safety maths verified (`J0224`) |

## 1. Success targets

| Metric | Target |
|--------|--------|
| Title score | vidIQ waived; title checked against `THUMBNAIL_AND_TITLE_RULES.md` §1 instead |
| Primary keyword | neighbour phrases *anesthesia* / *surgery before anesthesia* / *how anesthesia was discovered*; search phrases *who invented anesthesia* / *ether day 1846* |
| Hook promise | "Before eighteen forty-six, the best surgeon in the world was simply the fastest one — until a Boston dentist walked into an operating theatre with a glass globe of clear liquid." |
| Retention design | Five acts: The Fastest Knife in London (cold) → The Party Gas Nobody Used → The Dentist in the Dome → Who Gets the Credit? → Across the Ocean |
| Packaging | One object per thumbnail: Robert Liston's brass pocket watch beside William Morton's two-necked glass ether inhaler in the Boston Ether Dome |

## 2. Keyword research

**Public signals only.** "Autocomplete" means YouTube suggests the phrase as you type.

| Keyword | Autocomplete? | Competition read | Role | Keep? |
|---|---|---|---|---|
| surgery before anesthesia | **yes** | TED-Ed 2.65M #1; open slots under 30k in GB top 5 (`28k · 4k`) | Title B (Test & Compare) / search intent | yes |
| who invented anesthesia | **yes** | TED-Ed 19.7M & 2.65M + small channels (`144k · 261k · 991`) | cold open / description line 1, tags | yes |
| ether day 1846 | **no** | All 5 top GB slots under 150k views (`756 · 11.9k · 144k · 22 · 20`) | Part 03, description, tags | yes |
| first operation under anaesthetic | **related** | Autocompletes `operation before anesthesia`; clinical clips dominate | description, tags | yes |
| how aspirin was discovered | **yes** | TED-Ed 3.08M medicine-history neighbour | suggested-traffic neighbour | yes |

**Decision:** *Anesthesia* leads Title A with *The Day Surgery Stopped Hurting*; Title B tests the exact autocomplete phrase *What Surgery Was Like Before Anesthesia*. Description line 1 carries *anesthesia* (*anaesthesia*), *surgery*, *ether*, *William Morton*, and *Robert Liston*.

## 3. Title ABC

| | Title | vidIQ score | Rules check | Keep? |
|---|-------|------:|-------|-------|
| A | Anesthesia: The Day Surgery Stopped Hurting | waived | Pass: big subject (*Anesthesia*) + concrete hook (*The Day Surgery Stopped Hurting*), 43 chars | **Main (J0180 lock)** |
| B | What Surgery Was Like Before Anesthesia | waived | Pass: search question + neighbour phrase *surgery before anesthesia*, 39 chars | **Test & Compare (J0180 lock)** |
| C | How a Dentist Ended the Terror of Surgery | waived | Pass: concrete story hook, 41 chars | **Alt** |

**Locked title:** J0180 Chief topic & spelling lock (6128594677); final package subject to Ben's watch.

## 3b. Script reviewer

```bash
cd 07_Content-Ops && npm run review:script -- --file ../02_Video-Projects/011_Surgery-Before-Anaesthesia/01_Script/surgery_script_master_v02.md
```

- [x] Script reviewer ≥ 90: **91.1** on v01 (`J0183`) and **91.1** on v02 (`surgery_script_master_v02.md`, `J0224`), 8/8 structure gates, 1,259 words (~1,210 spoken).

## 4. Outlier / competitive patterns

| Outlier / pattern | Views | Steal (structure) | Do **not** copy |
|---|---|---|---|
| TED-Ed ★ *How does anesthesia work? - Steven Zheng* | ~19.7M | Everyday curiosity hook on how sleep without pain works | mechanism-only format |
| TED-Ed ★ *How does laser eye surgery work?* | ~6.8M | Clear step-by-step surgical clarity | modern clinical focus |
| TED-Ed ★ *How does heart transplant surgery work?* | ~4.5M | Stakes of operating-room timing | modern surgery focus |
| TED-Ed ★ *How aspirin was discovered - Krishna Sudhir* | ~3.1M | Period medicine-discovery arc | single-chemist focus |
| TED-Ed ★ *What did people do before anesthesia? - Sally Frampton* | ~2.6M | Pre-1846 surgical speed and early pain-relief attempts | broad survey without the 1846 Ether Dome climax |

**Patterns we will use:** Robert Liston's pocket-watch speed in pre-1846 London; Humphry Davy's 1799–1800 nitrous oxide wisdom-tooth note and "ether frolic" party bruises; Crawford Long's 1842 Georgia towel operation; Horace Wells's 1845 Boston laughing-gas failure ("Humbug!"); William Morton and John Collins Warren's 16 October 1846 Ether Dome triumph; the four-way credit battle and Boston's nameless Ether Monument; James Young Simpson's 1847 chloroform dinner-table crash and John Snow giving chloroform to Queen Victoria in 1853.

## 5. Incorporate into the build

| Data finding | Change |
|---|---|
| Neighbour phrase *anesthesia* / *surgery before anesthesia* | In Title A/B, description line 1, and tags |
| Primary-source quote verification (`J0198` + `J0224`) | Applied in `surgery_script_master_v02.md` and documented in `SOURCES_v01.md` + `CLAUDE_QUOTE_CHECK_v01.md` |
| Modern anaesthetic safety reassurance | Part 05 answers "Is it safe?" with the sourced RCoA 1-in-100,000 figure and 90,000-seat stadium scale |

**Chapter list after audit:**

1. Cold open: The Fastest Knife in London (no card)
2. The Party Gas Nobody Used
3. The Dentist in the Dome
4. Who Gets the Credit?
5. Across the Ocean

## 6. Retention plan

| Minute zone | Job | Picture / VO |
|---|---|---|
| 0–0:05 | Curiosity spike | Robert Liston's brass pocket watch ticking in a wooden operating theatre gallery before 1846 (answer image by 0:03, question by 0:07) |
| ~0:15 | Promise & stakes | Two-necked glass ether globe in Boston, 16 October 1846 (0:15); leather straps on the wooden table (0:25) |
| ~0:35 | First real fact | London surgeon Robert Liston timed at under three minutes + stopwatch dial DATA/SCALE (before 0:45) |
| Chapter starts | Re-hook | Each part opens cold and ends on a question the next part answers |
| Midpoint (~4:55) | Twist | "Case closed? Wrong." Morton's disguised "Letheon" patent and the four-way fight over credit |
| Final chapter | Payoff + hand-off | Liston's December 1846 London trial, Simpson's 1847 chloroform crash, Queen Victoria 1853, 1-in-100,000 safety scale; hand-off to 001 Germs / Lister |

## 7. Sign-off (block production until checked)

- [x] Keywords pulled and primary locked: public signals done (§2); vidIQ waived by Ben (standing rule)
- [x] Title proposed: *Anesthesia: The Day Surgery Stopped Hurting*, T&C *What Surgery Was Like Before Anesthesia*
- [x] Script reviewer ≥ 90: 91.1 on v02 (`surgery_script_master_v02.md`)
- [x] Outlier patterns mapped into the chapter arc
- [x] Thumb concepts match the title promise (one object · one emotion)
- [x] Chapter teach-points listed (5 acts)
- [x] Cold-open clock (5 / 15 / 30 s) written
- [x] Retention plan filled
- [x] Production checklist path noted: `11_Upload-Package/PRODUCTION_CHECKLIST_V2.md`

**Signed off by:** Chief topic lock (`J0180`, 6128594677), Cursor-on-Claude (`J0183` v01), Gemini (`J0198` facts pass) & Claude (`J0224` quote check & v02 lock, 6172862675); slotted Thu 10 Dec 2026 in `J2231`.
**Date:** 5 Nov 2026

**Only then:** VO (Ben Orbit Narrator) → Shorts scripts v02 → plates → edit.
