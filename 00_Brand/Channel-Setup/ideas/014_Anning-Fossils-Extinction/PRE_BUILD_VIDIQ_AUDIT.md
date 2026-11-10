# Pre-build audit — 014 Extinction & Fossils (Mary Anning's Lyme Regis sea dragons, 1811–1824)

Prepared 7 Nov 2026 (`J2328`) from public signals in `00_Brand/Channel-Setup/ideas/evidence_2026-10-15_J0295/` and refreshed in `00_Brand/Channel-Setup/ideas/014_Anning-Fossils-Extinction/evidence_2026-11-07_neighbours.json` / `evidence_2026-11-07_public_search.json` (`neighbours.py`, gate PASS: 3–4 education videos at 1M+, TED-Ed/TED present). **vidIQ is waived by Ben's standing rule** (desk PR #180, comment 5949981415), so there are no vidIQ scores. Ready to copy to `02_Video-Projects/014_Anning-Fossils-Extinction/11_Upload-Package/PRE_BUILD_VIDIQ_AUDIT.md` when `HOS:014` enters `active`.

## Episode

| Field | Value |
|---|---|
| ID / slug | 014 · `014_Anning-Fossils-Extinction` |
| Proposed air date | **Thu 31 Dec 2026** 18:00 UK (`2026-12-31T18:00:00.000Z`, `next_hos` #3) |
| Working title | *Extinction: The 12-Year-Old Who Dug Up a Sea Dragon* (T&C B: *How a 12-Year-Old Girl Proved Extinction Is Real*) |
| Date pulled | 2026-10-15 / refreshed 2026-11-07 |
| Credits used (approx) | 0 (vidIQ waived) |
| Brand guardrails | 1811–1812 *Ichthyosaurus* (~17 ft / 5.2 m, 4-foot skull found by brother Joseph Anning, excavated by 12-year-old Mary Anning) · 10 Dec 1823 *Plesiosaurus* (~9 ft, 35 cervical vertebrae vs 7 in giraffes) · Cuvier forgery suspicion resolved 20 Feb 1824 at Geological Society · Geological Society barred women until 1919 · ichthyosaurs & plesiosaurs explained clearly as marine reptiles, not dinosaurs · 28 rows in `SOURCES_v01.md` must pass Gemini facts & primary-source quote check before VO |

## 1. Success targets

| Metric | Target |
|---|---|
| Title score | vidIQ waived; title checked against `THUMBNAIL_AND_TITLE_RULES.md` §1 instead |
| Primary keyword | neighbour phrases *extinction* / *fossils* / *mary anning*; search phrases *mary anning fossils* / *how fossils proved extinction* |
| Hook promise | "Why did scientists two hundred years ago believe it was impossible for any kind of animal to go extinct — and how did a twelve-year-old girl on a crumbling English beach prove whole worlds of creatures had vanished forever?" |
| Retention design | Five acts: The Monster in the Cliff (cold) → Curiosities on the Beach → The Seventeen-Foot Fish-Lizard → The Fake That Proved Extinction → Stones That Were Ancient Meals |
| Packaging | One object per thumbnail: 4-foot stone *Ichthyosaurus* skull with its dinner-plate bony eye ring in dark wet Blue Lias shale as Mary Anning's hammer chips it free |

## 2. Keyword research

**Public signals only.** "Autocomplete" means YouTube suggests the phrase as you type.

| Keyword | Autocomplete? | Competition read | Role | Keep? |
|---|---|---|---|---|
| mary anning fossils | **yes** | All 5 top GB results under 1M views (`906k · 164k · 282k · 612k · 16k`) | primary / description line 1, tags | yes |
| Extinction: The 12-Year-Old Who Dug Up a Sea Dragon | **no** | All 5 top GB results under 580k views (`575k · 429 · 76k · 113k · 1.1k`) | Title A (Main) | yes |
| How a 12-Year-Old Girl Proved Extinction Is Real | **no** | Related phrase autocompletes (`mary anning the girl who cracked open the world`); 3 results in top slot | Title B (Test & Compare) | yes |
| how fossils proved extinction | **no** | 3 of top 5 GB slots under 320k views (`44k · 5.23M · 315k · 1.62M · 535`) | cold open / search intent | yes |
| Fossils: The Sea Monsters That Proved Extinction Is Real | **no** | Shares NHM 5.23M *fossils* noun + *extinction* | Title C (Alt) | yes |

**Decision:** *Extinction* leads Title A with *The 12-Year-Old Who Dug Up a Sea Dragon*; Title B tests the `How` discovery promise *How a 12-Year-Old Girl Proved Extinction Is Real*. Description line 1 carries *extinction*, *fossils*, *Mary Anning*, *Ichthyosaurus*, and *Plesiosaurus*.

## 3. Title ABC

| | Title | vidIQ score | Rules check | Keep? |
|---|---|---:|---|---|
| A | Extinction: The 12-Year-Old Who Dug Up a Sea Dragon | waived | Pass: big subject (*Extinction*) + concrete hook (*The 12-Year-Old Who Dug Up a Sea Dragon*), 51 chars | **Main** |
| B | How a 12-Year-Old Girl Proved Extinction Is Real | waived | Pass: search promise + concrete age hook, 48 chars | **Test & Compare** |
| C | Fossils: The Sea Monsters That Proved Extinction Is Real | waived | Pass: big subject (*Fossils*) + discovery payoff, 56 chars | **Alt** |

## 3b. Script reviewer

```bash
cd 07_Content-Ops && npm run review:script -- --file ../00_Brand/Channel-Setup/ideas/014_Anning-Fossils-Extinction/anning_script_master_v01.md
```

- [x] Script reviewer ≥ 90: **93.8** on v01 (`anning_script_master_v01.md`, `J0364`), 8/8 structure gates, 1,301 words (~1,230 spoken).

## 4. Outlier / competitive patterns

| Outlier / pattern | Views | Steal (structure) | Do **not** copy |
|---|---|---|---|
| Natural History Museum *How do dinosaur fossils form?* | ~5.23M | Tactile step-by-step clarity of rock strata and shale preservation | mechanism-only overview |
| Be Smart *Are We Living In the Sixth Extinction?* | ~4.42M | High-stakes framing of what it means for a species to vanish forever | modern ecology essay |
| SciShow *The 10 Oldest Fossils Ever Discovered* | ~1.80M | Concrete physical scale and age comparisons for ancient fossils | listicle format |
| TED-Ed ★ *When will the next mass extinction occur?* | ~1.78M | Deep-time timeline of extinctions vs surviving lineages | broad geological survey |
| Extra History *Mary Anning - Princess of Paleontology* | ~1.17M | Human drama of Anning's poverty, the 1820 Birch auction, and the 1824 Geological Society triumph | 2D comic-panel lecture |

**Patterns we will use:** Pre-1800 belief that no species could go extinct (Cuvier's 1796 mammoth paper vs sceptics claiming sea monsters still hid in deep oceans); baby Mary surviving the 19 August 1800 lightning strike; Joseph and 12-year-old Mary uncovering the 17-foot *Ichthyosaurus* (1811–1812), sold for £23 and published by Sir Everard Home in 1814 without naming them; Col. Thomas Birch's 15 May 1820 £400 auction; the 10 December 1823 *Plesiosaurus* (35 neck vertebrae vs 7 in a giraffe) that Cuvier suspected was a fake until 20 February 1824; coprolites (1824–1829) and 200-million-year-old belemnite ink; marine reptiles vs land dinosaurs.

## 5. Incorporate into the build

| Data finding | Change |
|---|---|
| Neighbour phrases *extinction* / *fossils* / *mary anning* | In Title A/B, description line 1, and tags |
| Primary-source verification required (`SOURCES_v01.md`, 28 rows) | Queue `--kind facts` pass on entry into `active` before locking script v02 / VO |
| Common misconception ("Were they swimming dinosaurs?") | Part 05 busts the myth with an inked hip-and-limb comparison (erect pillar legs vs marine flippers) |

**Chapter list after audit:**

1. Cold open: The Monster in the Cliff (no card)
2. Curiosities on the Beach
3. The Seventeen-Foot Fish-Lizard
4. The Fake That Proved Extinction
5. Stones That Were Ancient Meals

## 6. Retention plan

| Minute zone | Job | Picture / VO |
|---|---|---|
| 0–0:05 | Curiosity spike | Twelve-year-old Mary Anning brushing wet Blue Lias clay off a 4-foot stone jawbone and huge bony eye ring at Lyme Regis, 1811–1812 (answer image by 0:03, question by 0:07) |
| ~0:15 | Promise & stakes | Small fossil hammer splitting shale (0:15); mammoth tusk beside globe with UNKNOWN oceans (0:25) |
| ~0:34 | First real fact | Mary and Joseph Anning at Lyme Regis (1811–1812) + 17-foot *Ichthyosaurus* skeleton vs 15-foot rowing boat DATA/SCALE (before 0:45) |
| Chapter starts | Re-hook | Each part opens cold and ends on a question the next part answers |
| Midpoint (~5:00) | Twist | "Case closed? Wrong." Cuvier suspects the 35-vertebra *Plesiosaurus* is a stitched-together forgery; verified 20 Feb 1824 at the Geological Society while Anning is barred from the room |
| Final chapter | Payoff + hand-off | Cracking open coprolites (1824–1829), drawing with 200-million-year-old fossil ink, marine reptiles vs dinosaurs, 1848 Presidential Address tribute, hand-off to `010` (*What Killed the Dinosaurs Was Hidden in a Line of Clay*) |

## 7. Sign-off (block production until checked)

- [x] Keywords pulled and primary locked: public signals done (§2); vidIQ waived by Ben (standing rule)
- [x] Title proposed: *Extinction: The 12-Year-Old Who Dug Up a Sea Dragon*, T&C *How a 12-Year-Old Girl Proved Extinction Is Real*
- [x] Script reviewer ≥ 90: 93.8 on v01 (`anning_script_master_v01.md`)
- [x] Outlier patterns mapped into the chapter arc
- [x] Thumb concepts match the title promise (one object · one emotion)
- [x] Chapter teach-points listed (5 acts)
- [x] Cold-open clock (5 / 15 / 30 s) written
- [x] Retention plan filled
- [x] Production checklist path noted: `11_Upload-Package/PRODUCTION_CHECKLIST_V2.md`

**Prepared by:** `macbook-2` (`J2328` topic go/no-go prep, building on `J0295` & `J0364`).  
**Date:** 7 Nov 2026  

**When a HOS active slot frees:** Enter `active` via Rule-E topic go/no-go → Gemini facts pass (`SOURCES_v01.md` rows 1–28) & quote check → VO (Ben Orbit Narrator) → Shorts scripts v02 → plates → edit.
