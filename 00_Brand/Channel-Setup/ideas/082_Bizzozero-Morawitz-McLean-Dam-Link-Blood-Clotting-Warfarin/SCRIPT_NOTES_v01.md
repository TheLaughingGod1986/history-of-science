# 082 script v01: notes for review (J0736)

Script: `blood_clotting_script_master_v01.md` (with `opening_and_outline_v00.md`, `SOURCES_v00.md` and `SOURCES_v01.md`).

**Draft only (J0736, Gemini Argon, 20 Oct 2026).** Built from `082_Bizzozero-Morawitz-McLean-Dam-Link-Blood-Clotting-Warfarin/opening_and_outline_v00.md` and the neighbour and search evidence in `IDEAS_2026-10-20_J0728.md` (`evidence_2026-10-20_J0728/n_blood_clotting_warfarin.md` PASS — 8 education videos ≥ 1M views, with 6 strictly on wound healing, blood clotting, platelets & blood: **TED-Ed ★ *How blood pressure works - Wilfred Manzano* (`Ab9OZsDECZw`, 17.98M)**, **TED-Ed ★ *Why do blood types matter? - Natalie S. Hodge* (`xfZhb6lmxjk`, 6.75M)**, **TED-Ed ★ *How a wound heals itself - Sarthak Sinha* (`TLVwELDMDWs`, 6.54M — exact platelets, fibrin clot & wound healing match!)**, **TED-Ed ★ *How the heart actually pumps blood - Edmond Hui* (`ruM4Xxhx32U`, 4.47M)**, **TED-Ed ★ *What happens if you're injected with the wrong blood type? - Bill Schutt* (`qcZKbjYyOfE`, 1.42M)**, and **FuseSchool *Platelets & Blood Clotting | Biology | FuseSchool* (`gExUCrpAKyQ`, 1.08M — exact platelets & fibrin coagulation match!)**, plus **TED ★ *A teen scientist's invention to help wounds heal* (`r-YXvkWLy-g`, 254.9k)** and **TED ★ *How we could teach our bodies to heal faster* (`2ch5FJAqLMk`, 170.7k)**, alongside `public_search.md` & `public_search_titles.md` showing `"how does blood clot"` is an exact YouTube autocomplete match (`yes`), all 5 top GB search results for `"jay mclean heparin karl paul link warfarin"` under 400k views, and all 5 top GB slots for *How Spoiled Clover Hay Turned Rat Poison Into a Life-Saving Blood Thinner* under 600 views). The topic isn't locked yet: Chief locks `082` and the working title pair first, then reviews/signs off this script and queues the Gemini facts pass (`--kind facts`) on `SOURCES_v01.md` (rows 1–4) before VO.

Structure (*Reference lessons* §1, scripts from 011 on): every chapter opens cold and ends on a question the next one answers; Giulio Bizzozero's 1882 living-vessel discovery of `platelets` and Paul Morawitz's 1905 `thrombin-fibrin` coagulation cascade land in Part 02; the midpoint twist ("Case closed — to help wounded soldiers in World War One stop bleeding, a twenty-five-year-old medical student at Johns Hopkins in nineteen sixteen was assigned to purify a powerful *clotting* chemical from dog liver! Wrong! Instead of clotting faster, his test tubes of blood refused to clot at all — because he had accidentally discovered `heparin`, the body's natural blood thinner!" — alongside Henrik Dam's 1929–1935 discovery of `Vitamin K`) lands in Part 03; farmer Ed Carlson's February 1933 Wisconsin blizzard milk can, Harold Campbell & Karl Paul Link's 28 June 1939 `dicoumarol` and 1948 `Warfarin`, the April 1951 Navy recruit, and President Eisenhower's September 1955 recovery land in Part 04; the ending hands off directly to `083` (*How Do Your Eyes Focus Light & How Do Glasses Cure Blurry Vision — and How Did a Darkened Room in Cairo Prove Your Eyes See the World Upside Down?*), with no goodbye and no subscribe ask. Five VO parts, matching 009–081.

## Marker count (v01)

Run on `blood_clotting_script_master_v01.md`: `grep -o "DATA:" … | wc -l`, and the same for each marker.

| Marker | Count | Where | Rule |
|---|---:|---|---|
| `DATA` | **6** | 1) inked Morawitz (1905) 4-factor coagulation cascade (`Thromboplastin + Ca²⁺ → Prothrombin → Thrombin → Fibrinogen to Fibrin`) & Vitamin K vs Warfarin liver cycle chart (0:34); 2) inked Karl Paul Link (1940–1948) dicoumarol/Warfarin plasma prothrombin activity curve & reversal by Vitamin K administration (0:52); 3) inked Giulio Bizzozero (1882 *Virchows Archiv*) living-vessel platelet plug formation & Paul Morawitz (1905 *Ergebnisse der Physiologie*) 4-factor enzymatic amplification cascade (1:58); 4) inked Jay McLean (1916 *Am. J. Physiol.*) heparphosphatide/heparin coagulation time curve + Henrik Dam (27 Apr 1935 *Nature*) Vitamin K prothrombin restoration chart (3:47); 5) inked Karl Paul Link, Harold Campbell, Mark Stahmann & Charles Huebner (1940–1948) sweet clover coumarin → mould-oxidized dicoumarol → compound #42 Warfarin structure & Vitamin K epoxide reductase inhibition chart (5:32); 6) animated timeline 1872–1955 (6:48) | ≥ 3 per long, including the timeline |
| `SCALE` | **6** | 1) 15 million platelet discs in a single drop of blood inflating spiky arms like life rafts and piling into a sandbag dam locked by fibrin cables (0:34); 2) Warfarin and Vitamin K as molecular lookalikes where Warfarin jams the liver's lock and real Vitamin K pops the counterfeit key back out (0:52); 3) clotting cascade working like a mountainside avalanche (1 → 10 → 100) weaving millions of fibrin threads in 2 minutes (1:58); 4) Jay McLean hunting for the accelerator pedal of clotting and accidentally finding the emergency brake that boosts our anti-clotting shield 1,000-fold (3:47); 5) mould in a damp barn welding two vanilla-scented coumarin molecules into a counterfeit Vitamin K key (5:32); 6) from a medical student's unclotted liver extract and bleeding chicks in Copenhagen to a milk can of cow's blood in a Wisconsin blizzard (6:48) | `SCALE:` on every `DATA:` (`grep -c` matches) |
| `WHO` | **9** | Giulio Bizzozero (1846–1901) — Italian histologist and pathologist; Paul Morawitz (1879–1936) — German physician and physiologist; Jay McLean (1890–1957) — American medical student and surgeon; William Henry Howell (1860–1945) — American physiologist; Henrik Dam (1895–1976) — Danish biochemist; Karl Paul Link (1901–1978) — American biochemist; Alexander Schmidt (1831–1894) — Baltic German physiologist; Edward Adelbert Doisy (1893–1986) — American biochemist; Harold A. Campbell (born 1913) — American biochemist | Every named person at first mention, role right for the scene's year |
| `WHEN` | **27** | Madison, Wisconsin, February 1933 (0:00); 1882, 1905, 1916, 1929, February 1933, 1935, 1948 (0:34); 1872, 1882, 1905 (1:28); 1916, 1918, 1929, 27 April 1935, 1943 (3:13); February 1933, 28 June 1939, 1941, 1948, April 1951, September 1955 (4:58); 1882–1955 timeline marker (6:48); 1011 AD, 1604, 1801, 1862 (7:45) | Every spoken date or era |
| `FACT` | **3** | `15 million platelets per drop` (1:28); `Clot hunt found blood thinner` (3:13); `Rat poison saved a President` (4:58) | 2–4 per long, ≤ 4 words per card |

## Craft lessons check (*Reference lessons* §1)

- **Cold opens & cliffhanger hand-offs:** Part 01 opens cold on how 5 litres of liquid blood seal a finger cut in seconds without clotting your veins and how a milk can of cow's blood in a 1933 Wisconsin blizzard turned rat poison (`Warfarin`) into medicine, and ends on how Giulio Bizzozero in 1882 spotted the tiny `platelet` discs everyone else dismissed as trash; Part 02 opens cold on the candle-wax cooling myth and Bizzozero's 1882 living-vessel `platelets` + Morawitz's 1905 `thrombin-fibrin` net, and ends on why all the blood in our veins doesn't clot into stone right now and how a 25-year-old Baltimore medical student in 1916 found the answer by accident; Part 03 opens cold on the midpoint twist ("Case closed — to help wounded soldiers in World War One stop bleeding, a twenty-five-year-old medical student at Johns Hopkins in nineteen sixteen was assigned to purify a powerful *clotting* chemical from dog liver! Wrong!"), tells the story of Jay McLean's accidental discovery of `heparin` and Henrik Dam's 1929–1935 `Vitamin K`, and ends on how a 1933 Wisconsin blizzard, rotten sweet clover hay, and rat poison gave humanity `Warfarin`; Part 04 opens cold on farmer Ed Carlson's 190-mile blizzard drive with a milk can of unclotted cow's blood, explains Harold Campbell & Karl Paul Link's 28 June 1939 `dicoumarol`, 1948 `Warfarin`, the April 1951 Navy recruit cured by Vitamin K, and President Eisenhower's September 1955 treatment, and ends on how our eyes focus light upside down on the retina and how glasses cure blurry vision; Part 05 opens cold on the clotting tightrope that saves millions, and hands off to Ibn al-Haytham (1011 AD), Johannes Kepler (1604), Thomas Young (1801), and Herman Snellen (1862) (`083`).
- **Quirky anecdote before the hard idea:** Medical student Jay McLean placing a beaker of cat blood on Professor Howell's desk and telling him to call when it clotted (it never did); farmer Ed Carlson driving 190 miles in a blizzard with a milk can of unclotted cow's blood; mould turning vanilla-scented grass coumarin into a blood thinner; rat poison saving US President Dwight D. Eisenhower!
- **Rivalry / tension:** William Howell's pro-clotting cephalin dogma vs Jay McLean's anticoagulant `heparin`; fear of `Warfarin` as a lethal rat poison vs its 1951–1955 proof as a reversible, life-saving oral blood thinner.
- **Misconception explained away:** "Does blood clot simply because it cools or dries when exposed to air, and does a blood thinner literally water down your blood?" — refuted by Bizzozero & Morawitz's platelet-fibrin cascade and Link & Dam's proof that `Warfarin` blocks `Vitamin K` recycling in the liver without diluting the blood (Parts 01–04).

## For Chief to decide

1. Lock **082 = How Does a Cut Stop Bleeding Without Clotting All the Blood in Your Veins — and How Did Spoiled Clover Hay Turn Rat Poison Into a Life-Saving Blood Thinner (`Blood Clotting, Platelets, Fibrin, Heparin, Vitamin K & Karl Paul Link's Warfarin`)? Giulio Bizzozero's 1882 Discovery of `Platelets` & Paul Morawitz's 1905 `Thrombin-Fibrin` Cascade, Medical Student Jay McLean & William Howell's 1916 Accidental Discovery of `Heparin`, Henrik Dam's 1929–1935 Discovery of `Vitamin K`, and Karl Paul Link's February 1933 Blizzard Milk-Can Discovery of `Dicoumarol` and `Warfarin` (1882–1955)** and pick the 2-way Test & Compare working title pair:
   - **A (Subject + hook, §1 rule 11):** *Warfarin: How Rat Poison Saved Millions of Lives* (48 chars)
   - **B (Search question, §1 rule 2):** *How Spoiled Clover Hay Turned Rat Poison Into a Life-Saving Blood Thinner* (73 chars)
   - **Alt (Search / twist question):** *How Your Blood Clots in Seconds and How Rat Poison Became Medicine* (66 chars)
2. Review `blood_clotting_script_master_v01.md` (91.0/100 PASS), then queue the Gemini facts pass (`--kind facts`) on `SOURCES_v01.md` (rows 1–4) before VO.

## Score (`npm run review:script`)

```text
# blood_clotting_script_master_v01.md

**Decision:** PASS · **Score:** 91 / 100

| Dimension | Score |
|---|---:|
| hook | 9.5 |
| curiosity | 9.1 |
| storytelling | 8 |
| scientificAccuracy | 10 |
| emotion | 9.6 |
| escalation | 7.6 |
| retentionPotential | 9 |
| searchPotential | 9.1 |
| visualOpportunities | 9.5 |
| narrationFlow | 9.6 |

Words: 1557 · Est. min: 10.4 · Chapters: 4

## Cold open excerpt

> How does a cut on your finger stop bleeding in seconds ( a blood clot ) without solidifying all the blood in your veins? Right now, your five litres of liquid blood race through sixty thousand miles of vessels without clogging, yet seal a paper cut in minutes — so how did a milk 

## Findings

- **[info] overall:** Structure gates 8/8 — applied +1.05 completeness boost to supporting dimensions.
- **[info] overall:** PASS 91/100 — proceed to VO after production checklist.

Pass threshold: 90
```
