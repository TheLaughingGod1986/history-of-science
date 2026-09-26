# Pre-build vidIQ audit — HOS 004 Why Is the Periodic Table in This Order?

Template: `00_Brand/Channel-Setup/PRE_BUILD_VIDIQ_AUDIT_TEMPLATE.md`. Drafted 26 Sep 2026 from **public YouTube data** (GB search results and YouTube autocomplete, fetched the same day; raw pull in `evidence_2026-09-26_public_search.json`). **vidIQ scores are not in this draft:** vidIQ needs Ben's login (there's no API connection here), so every score cell reads *pending vidIQ*. Ben fills those in app.vidiq.com and signs off at the end.

## Episode

| Field | Value |
|-------|-------|
| ID / slug | `004_Whats-Really-Inside-An-Atom` |
| Working title | Why Is the Periodic Table in This Order? (Test & Compare: What's Really Inside an Atom? · How Small Can You Cut Gold?) |
| Date pulled | 26 Sep 2026 (public search + autocomplete); vidIQ pending |
| Credits used (approx) | 0 so far |
| Brand guardrails | Wonder over fearbait · no conspiracy · HOS lane (a familiar thing, and the moment we found out) · no bomb or fission |

## 1. Success targets

| Metric | Target |
|--------|--------|
| Title score | ≥ 90 in vidIQ (aim 95+): *pending vidIQ* |
| Primary keyword overall | *pending vidIQ* (see §2 for the public signals) |
| Hook promise | "By the end of this film you'll know why the periodic table is in the order it is, and how we proved it." Matches the open VO; the thumb must promise the same thing. |
| Retention design | 5 parts, each ends on a question the next answers (weight rule breaks → atoms have parts → mostly empty → counting fixes the table) |
| Packaging | One object (the gold coin halves / the glowing atom), 2–4 words, readable at 168×94 |

## 2. Keyword research

**Public signals only** (Overall / Est./mo / Comp are vidIQ numbers and are *pending*). "Autocomplete" means YouTube suggests the phrase as you type, so people really search it. "Top results" is who you'd compete with in GB search.

| Keyword | Autocomplete? | Top results (GB) | Competition read | Role | Keep? |
|---|---|---|---|---|---|
| what is inside an atom | **yes** (and "class 9" / "class 8" student variants) | Tidlybit 1.66M · minutephysics 5.7M · History of the Universe 3.5M · Arvin Ash 562K · Physics Explained 528K | **Very high.** Big channels hold the top five; much of the demand is homework | umbrella; description, not title lead | yes (desc) |
| what's really inside an atom | **no** | same set as above; also a 2-hour sleep video with this exact title (776 views) | Same wall; the exact phrase isn't searched | main title (Ben's pick) | see §3 |
| how small can you cut gold | **no** | only gold-bar cutting Shorts (jewellery) | No science competition, but search intent is jewellery | Test & Compare title B, thumbnail, lead Short | yes (T&C, Short) |
| how was the atom discovered | **yes** | TED-Ed 3.35M · Professor Dave 1.1M · Tracing Science 624K · Matt Parker 50K · Science Retold 2K (1 day old) | High, but older videos | secondary; description + chapter | yes (desc) |
| why is the periodic table in that order | no (but "periodic table order explained" is suggested) | songs dominate; the on-topic answers are small: ScienceABC 7.8K · LLNL 14.8K | **Low** for the real question | **our unique angle**; title C, description line 1 | yes |
| henry moseley / how moseley discovered atomic number | **yes** (8 variants incl. "henry moseley death", "x ray experiment") | Rational Thinker 98K · Evrim Ağacı 191K · KayScience 25K · rest under 20K | **Low** | chapter 5 + a Short + tags | yes |
| rutherford gold foil experiment | **yes** (8 variants, incl. "animation", "in real life") | BackstageScience 3.4M · Tyler DeWitt 946K · STFC 795K; mostly 8–18 years old | High but dated, and no 3D cartoon version | chapter 4 + a Short | yes |
| atoms are mostly empty space | **yes** ("the experiment that proved atoms are mostly empty space") | The Action Lab 1.08M · Kyle Hill 565K · Physics Explained 378K | Medium–high | stadium-and-pea Short | yes |
| who discovered the electron | **yes** | Tyler DeWitt 1.5M · STFC 550K · Rational Thinker 118K | Medium | chapter 3 + tags | yes |

**Decision (draft):** primary keyword for the description lead = **"what is inside an atom"**, with the unique angle said in the same line ("…and why the periodic table is in this order").
**Description first 100 characters must include:** *inside an atom*, *periodic table*, *order*. Suggested: "What's really inside an atom, and why is the periodic table in this order? Four discoveries, one century…"

## 3. Title ABC

The signed-out competition check (`STUDIO_PLAYBOOK.md` §2) is a **warning** for the main title: all top five results for "inside an atom" are channels with millions of subscribers. The playbook says narrow the angle when that happens. The film already has a narrow angle; the titles below put it forward to different degrees.

| | Title | vidIQ score | Rules check | Keep? |
|---|---|---:|---|---|
| A | What's Really Inside an Atom? | *pending* | Pass: familiar noun, one promise, 29 chars. Competes with minutephysics / Kurzgesagt / TED-Ed | **Main (Ben's pick)** |
| B | How Small Can You Cut Gold? | *pending* | Pass: familiar object first, curiosity, 27 chars. Search intent is jewellery, so this wins on browse/CTR, not search | **Test & Compare** |
| C | Why Is the Periodic Table in This Order? | *pending* | Pass: familiar noun first, the question the film actually answers, low competition, follows on from 002 | **Proposed third T&C variant** |
| Reject | How Did We Discover the Atom? | — | Retired formula (THUMBNAIL_AND_TITLE_RULES §1) | **Reject** |
| Reject | Anything with "atomic bomb" / "deadly" | — | Off-lane, fear framing | **Reject** |

**Locked title (26 Sep 2026):** *Why Is the Periodic Table in This Order?*, chosen for traction after this audit. Test & Compare runs all three: C (main), A and B.
**Why C:**
- **It can be found.** A small channel gets most of its early long-form views from search, not the home feed. The top results for C's question have 8K–15K views; for A's phrase they're minutephysics, Kurzgesagt and TED-Ed at millions.
- **It's the film's real payoff,** promised in the open ("why the periodic table is in the order it is") and answered in Part 05, so title, open and ending make the same promise.
- **It follows the channel's best long.** *How Did We Discover the Periodic Table?* has the most long views on the channel; C reads as the sequel, and End screen / Related can pair them. It is a different subject (the atom's inside, not the table's discovery), so it isn't a second long on the same subject.
- **The rules:** familiar noun first, one concrete promise, a yes/why question, 40 characters, no hedge.
- **A and B still get tested.** B keeps the gold coin as the strongest thumbnail and the lead Short; A covers the broad "inside an atom" search.

## 3b. Script reviewer

```bash
cd 07_Content-Ops && npm run review:script -- --file ../02_Video-Projects/004_Whats-Really-Inside-An-Atom/01_Script/atom_script_master_v02.md
```

- [ ] Score ≥ 90 / 100: **88.5 today.** The gap is mostly a reviewer counting bug (escalation and science words are counted once at most); 91.8 with the bug fixed. Ben decides: merge the reviewer fix, or pass this script by hand.

## 4. Outlier / competitive patterns (on-brand only)

| Outlier / pattern | Views | Steal (structure) | Do **not** copy |
|---|---|---|---|
| TED-Ed *The 2,400-year search for the atom* (5:23) | 3.35M | the idea → Dalton → Thomson → Rutherford journey | the flat 2D lecture look; 5-minute length |
| The Action Lab *The Experiment That Proved Atoms Are Mostly Empty Space* | 1.08M | one experiment, one surprising result, shown | a home-lab demo format |
| Kurzgesagt *How Small Is An Atom?* | 10.1M | a body/everyday scale anchor | the space-animation look |
| Evrim Ağacı *How a Physicist Shot by a Turkish Sniper at Çanakkale Changed Chemistry* | 191K | Moseley's story as the emotional turn | the war-first framing and sniper detail (HOS: no war framing, wonder not dread) |
| Kyle Hill *The "Empty Atom" Myth* | 565K | "what you were taught is not the whole story" | a myth-busting / contrarian frame |

**Patterns in the script:**

- [x] Assumption-flip / open-loop title (the table "breaks its own rule")
- [x] Chapter journey (idea → weight → electron → nucleus → number)
- [x] Body-scale anchor (the stadium and the pea, "you" framing)
- [x] Slow reveal / delayed answer (why Te comes before I is answered in Part 05)
- [ ] Engineering roadmap (doesn't fit)
- [x] Other: a person to follow at each step, and the loss of Moseley as the emotional turn

## 5. Incorporate into the build

| Data finding | Change to script / chapters / visuals / packaging |
|---|---|
| "what is inside an atom" is the umbrella, but held by big channels | Description line 1 + tags; title A keeps "inside an atom"; don't try to out-rank minutephysics on the phrase alone |
| "why is the periodic table in this order" has low competition and is our payoff | Title C as a Test & Compare variant; description line 1 names it; the open VO already promises it |
| "rutherford gold foil experiment" has strong student demand and dated results | A Short built from Part 04 (the flash in the dark room), title shaped as a question, e.g. *Why Did a Bullet Bounce Off Gold Foil?* |
| "henry moseley" searches include his death and the X-ray experiment | Part 05 keeps the Gallipoli line short and respectful (already); tags + a Short on the counting ladder |
| "atoms are mostly empty space" has demand | The stadium-and-pea Short |
| Weak competition angle | A 3D-cartoon, one-room-per-discovery story, which none of the top results are |
| Thumb pattern that works (Kurzgesagt / TED-Ed scale thumbs) | One object big (gold coin halves or the atom), 2–4 words: **HOW SMALL?** / **MOSTLY EMPTY** |

**Chapter list after audit** (matches script v02):

1. Cold open: cut the coin; the table's secret problem (no chapter card)
2. The Table That Broke Its Own Rule: Dalton's weights, Mendeleev's swap (Te before I)
3. The Crumb Inside the Atom: Thomson finds the electron (atoms have parts)
4. The Shell That Bounced Back: Rutherford finds the nucleus (mostly empty space)
5. Counting With X-rays: Moseley's atomic number fixes the table

**Shorts from the audit** (one a day at most, each promoting one film; this film's lead Short is the gold coin on Fri 16 Oct, per `LAUNCH_PLAN.md`):
- *How Small Can You Cut Gold?* (lead, 004)
- *Why Did a Bullet Bounce Off Gold Foil?* (004, later week)
- *An Atom Is Mostly Empty. Here's the Proof.* / stadium and pea (004, later week)

## 6. Retention plan

| Minute zone | Job | Picture / VO note |
|---|---|---|
| 0–0:05 | Curiosity spike | Knife halves the coin; push into the atom (answer image by 0:05) |
| ~0:15 | Stakes | Te and I wobble out of order: "the table had a secret problem" |
| ~0:30 | Journey clear | Scroll → tube → foil → 1913 lab, one labelled flash each |
| Chapter starts | Re-hook + chapter card | Each part opens on a place and year and ends on a question |
| Mid | Teach while the story continues | The bending beam, the flash in the dark, the stadium: proof on screen; the Explorer reacts at most |
| Final chapter | Payoff + bigger question | The table re-sorts itself by number; "some nuclei don't sit still" opens the radioactivity film |
| Outro | Hand-off | Cream end card, then the Studio end screen (X-rays, Periodic Table, Subscribe) |

- [x] No 30 s+ stretch without a new teach or turn (picture changes every ≤6 s in the open; each part has 2–4 labelled beats)
- [x] Every chapter earns the next one (each part ends on the question the next answers)
- [x] Runtime target 7–9 min (about 1,280 spoken words, likely about 8:25 of VO)

## 7. Sign-off (block production until checked)

- [x] Keywords pulled and primary locked: public signals (§2). **vidIQ waived by Ben, 26 Sep 2026.**
- [x] Title locked: *Why Is the Periodic Table in This Order?* (C), Test & Compare A and B. **vidIQ title scores waived by Ben.**
- [x] Script reviewer: **88.9, passed by hand by Ben (26 Sep 2026)**; the shortfall is the reviewer's counting bug (§3b).
- [x] Outlier patterns mapped into the chapter arc
- [x] Thumb concepts match the title promise (one object · one emotion)
- [x] Chapter teach-points listed (5 acts)
- [x] Cold-open clock (5 / 15 / 30 s) written
- [x] Retention plan filled
- [x] Production checklist path noted: `00_Brand/Channel-Setup/templates/PRODUCTION_CHECKLIST_V2.md`

**Signed off by:** Ben (vidIQ waived; script passed by hand at 88.9)
**Date:** 26 Sep 2026

**Only then:** VO (Ben Orbit Narrator) → Flow Veo plates → edit.
