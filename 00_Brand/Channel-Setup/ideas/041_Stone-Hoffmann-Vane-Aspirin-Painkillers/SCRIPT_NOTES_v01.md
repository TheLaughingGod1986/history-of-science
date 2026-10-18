# 041 script v01: notes for review (J0539)

Script: `aspirin_script_master_v01.md` (with `opening_and_outline_v00.md`, `SOURCES_v00.md` and `SOURCES_v01.md`).

**Draft only (J0539, Gemini Argon, 18 Oct 2026).** Built from `041_Stone-Hoffmann-Vane-Aspirin-Painkillers/opening_and_outline_v00.md` and the neighbour and search evidence in `IDEAS_2026-10-18_J0515.md` (`evidence_2026-10-18_J0515/n_aspirin.md` PASS — 5 education videos ≥ 1M views: **TED-Ed ★ *How Do Pain Relievers Work? - George Zaidan* (`9mcuIc5O-DE`, 4.25M)**, **TED-Ed ★ *How aspirin was discovered - Krishna Sudhir* (`uRhkDN2WjzI`, 3.08M — exact historical match!)**, **TED-Ed ★ *How does your brain respond to pain? - Karen D. Davis* (`I7wfDenj6CQ`, 2.96M)**, **TED-Ed ★ *The mysterious science of pain - Joshua W. Pate* (`eakyDiXX6Uc`, 2.06M)**, and **SciShow *Why We Feel Pain, and How We Kill it | A Look at Pain & Painkillers* (`GmHGUTNoL-I`, 1.41M)**, plus **TED ★ *How to Hack Your Brain When You're in Pain* (`5SpaXqAQ4Wo`, 803.7k)**, alongside `public_search.md` showing all 5 top GB search results for `"felix hoffmann aspirin willow bark"` under 336k views and all 5 top GB slots for *How Tree Bark and a Chemist's Father Gave the World Aspirin* under 336k views). The topic isn't locked yet: Chief locks `041` and the working title pair first, then reviews/signs off this script and queues the Gemini facts pass (`--kind facts`) on `SOURCES_v01.md` (rows 1–4) before VO.

Structure (*Reference lessons* §1, scripts from 011 on): every chapter opens cold and ends on a question the next one answers; the midpoint twist ("Case closed? Wrong! When Hoffmann and Arthur Eichengrün handed their gentle new painkiller to pharmacology chief Heinrich Dreser, Dreser refused to test or sell it!" — after Felix Hoffmann on 10 August 1897 acetylated salicylic acid to spare his arthritis-stricken father's bleeding stomach, pharmacology boss Heinrich Dreser rejected acetylsalicylic acid as "poison for the heart" while promoting diacetylmorphine/Heroin, synthesised 11 days later on 21 August 1897, until Arthur Eichengrün secretly tested it on himself and Berlin patients, forcing Bayer to register Aspirin on 6 March 1899) lands in Part 03; John Vane's 23 June 1971 Royal College of Surgeons discovery solving the 74-year mystery of how aspirin works (blocking cyclooxygenase / COX enzymes from producing pain, fever, and inflammation prostaglandins, and Roth & Majerus's 1975 proof of permanent Serine-530 acetylation) lands in Part 04; the medical irony ("In eighteen ninety-seven, Bayer's chief pharmacologist Heinrich Dreser tried to block Aspirin because he claimed it was bad for the heart") is raised and explained away in Part 05 via irreversible 8–10 day platelet thromboxane A2 blockade and the 1988 ISIS-2 trial of 17,187 heart-attack patients showing a 23% reduction in vascular deaths; the ending hands off directly to `042` (*How Do Lasers & Fibre Optics Work? Albert Einstein's 1917 Stimulated Emission, Theodore Maiman's 16 May 1960 Flashlamp Ruby Laser in Malibu & Charles Kao's 1966 Pure Glass Fibre in Harlow*), with no goodbye and no subscribe ask. Five VO parts, matching 009–040.

## Marker count (v01)

Run on `aspirin_script_master_v01.md`: `grep -o "DATA:" … | wc -l`, and the same for each marker.

| Marker | Count | Where | Rule |
|---|---:|---|---|
| `DATA` | **6** | 1) inked clinical & chemical chart on period paper showing Edward Stone's 1763 trial (50 of 50 ague/fever patients relieved with 20 grains / ~1.3 g of dried willow bark every 4 hours), Felix Hoffmann's 10 August 1897 acetylation (salicylic acid + acetic anhydride → acetylsalicylic acid, 100% pure crystals), and global consumption (~40,000 tonnes / ~100 billion tablets per year) (0:34); 2) inked 74-year mystery bar comparing 10 August 1897 (acetylsalicylic acid synthesised at Bayer) to 23 June 1971 (John Vane proves aspirin irreversibly inhibits prostaglandin synthesis via the COX enzyme) (0:52); 3) inked extraction & dose diagram on period paper showing 1 pound of dried white willow bark (Edward Stone 1763, 50 fever patients cured with 20 grains / 1.3 g) yielding salicin (1828) and salicylic acid (Piria 1838), where arthritis patients required 4–6 grams per day of corrosive acid (1:58); 4) inked molecular & gastric-irritation comparison chart on period paper from Hoffmann's 10 August 1897 notebook showing salicylic acid (exposed phenolic −OH group irritating stomach mucosa) vs acetylsalicylic acid (acetyl group −COCH3 shielding the stomach before releasing active salicylate in the bloodstream) (3:42); 5) inked enzyme-lock diagram on period paper from John Vane (1971) and Roth & Majerus (1975) showing arachidonic acid entering the cyclooxygenase (COX) enzyme channel to produce pain/fever prostaglandins and clotting thromboxane A2 vs acetylsalicylic acid permanently acetylating Serine-530 to block the channel by >95% (5:28); 6) animated timeline building 25 Apr 1763 · 1828–1838 · 10 Aug 1897 · 23 Jun 1971 · 1975–1988 alongside the 8–10 day irreversible platelet thromboxane blockade and 23% reduction in vascular deaths in the 17,187-patient ISIS-2 trial (6:43) | 3 or more per long, including the animated timeline |
| `SCALE` | **6** | 1) humans swallow roughly forty thousand tonnes of aspirin every single year — more than a hundred billion little white tablets, enough to stretch to the Moon and back (0:34); 2) for nearly three-quarters of a century, doctors prescribed the world's most popular medicine completely blind to what it did inside a human cell (0:52); 3) to calm swollen joints in the eighteen seventies, arthritis patients had to swallow up to six grams of raw salicylic acid every single day — a dose so caustic it stripped the lining of their stomachs (1:58); 4) swapping a single hydrogen atom for an acetyl group turned a corrosive crystal that burned the throat into a gentle tablet that passed safely through the stomach (3:42); 5) a single three-hundred-milligram aspirin tablet — weighing less than five grains of rice — floods your bloodstream with a quintillion molecules that silence pain factories from head to toe (5:28); 6) one tiny seventy-five-milligram aspirin tablet disables a blood platelet's clotting factory for its entire ten-day life — cutting heart-attack deaths by nearly a quarter (6:43) | Every `DATA` number gets a `SCALE:` comparison (`grep -c "SCALE:"` ≥ `DATA:` count) |
| `WHO` | **6** | Edward Stone (0:34), Felix Hoffmann (0:34), John Vane (0:34), Raffaele Piria (1:28), Arthur Eichengrün (3:08), Heinrich Dreser (3:08) | First mention only, role right for the scene's year (4 words or fewer) |
| `WHEN` | **24** | Elberfeld 10 August 1897 (0:00), Oxfordshire 25 April 1763 (0:00), Elberfeld 10 August 1897 (0:21), 25 April 1763 (0:34), 10 August 1897 (0:34), 23 June 1971 (0:34), 1550 BC (1:28), 1758 (1:28), 25 April 1763 (1:28), 1828 (1:28), 1838 (1:28), 1876 (1:28), 1853 (3:08), 10 August 1897 (3:08), 21 August 1897 (3:08), 6 March 1899 (3:08), 23 June 1971 (4:53), 1975 (4:53), 1982 (4:53), 1988 (6:43), 1763–1988 (6:43), 1917 (7:45), 16 May 1960 (7:45), 1966 (7:45) | Every spoken date or era; later dates drop onto the timeline |
| `FACT` | **4** | Baked bark in a bread oven (1:28); Boss feared it hurt the heart (3:08); Plugs the pain enzyme tunnel (4:53); Cuts heart-attack deaths 23% (6:43) | 2–4 per long (4 words or fewer per card) |

## Craft checks (*Reference lessons* §1 + *Polish pass*)

- **First-minute timings:** Answer image by 0:03 (Felix Hoffmann crystallising pure white acetylsalicylic acid at Bayer in Elberfeld on 10 August 1897 beside his father's letter, dissolving to Reverend Edward Stone tasting white willow bark in Oxfordshire in 1758–1763), title question by 0:07, promise by 0:15, stakes by 0:25, first concrete answer & real fact (Edward Stone's 25 April 1763 willow-bark fever cure, Felix Hoffmann's 10 August 1897 acetylation into Aspirin, and John Vane's June 1971 discovery of COX prostaglandin inhibition) by 0:34.
- **Explorer limits:** 2 beats total (`[EXPLORER ACTS: once. …]`), at 1:05 (Part 01, outside the first minute) and 6:05 (Part 04 sliding a silver "ACETYL" bolt across the COX enzyme tunnel to block red prostaglandin sparks).
- **Chapter cold opens & cliffhanger questions:** Part 01 ends on how ancient healers and an eighteenth-century Oxfordshire vicar discovered a fever cure inside a swamp tree and why the purified crystal burned stomachs raw; Part 02 opens cold on 3,500 years of willow bark, Edward Stone's 1758–1763 baker's-oven drying and 50-patient trial, and Buchner (1828), Piria (1838), and Maclagan (1876) isolating salicin and corrosive salicylic acid, ending on how 29-year-old Felix Hoffmann tamed the molecule on 10 August 1897 to spare his father; Part 03 opens cold on the midpoint twist ("Case closed? Wrong!" — Hoffmann's 10 August 1897 synthesis of 100% pure acetylsalicylic acid, Heinrich Dreser rejecting it as heart poison while promoting Heroin synthesised 11 days later on 21 August 1897, and Arthur Eichengrün's secret trials leading to the 6 March 1899 registration of Aspirin), ending on how doctors prescribed hundreds of billions of tablets over 74 years without knowing how it stops pain; Part 04 opens cold on how a swallowed pill "knows" where you hurt, explaining John Vane's 23 June 1971 prostaglandin discovery and Roth & Majerus's 1975 proof of permanent Serine-530 COX acetylation, ending on what blocking that same enzyme does inside blood platelets; Part 05 opens cold on Heinrich Dreser's 1897 fear that Aspirin hurt the heart, explains 8–10 day irreversible platelet thromboxane blockade and the 1988 ISIS-2 trial's 23% reduction in heart-attack mortality, and hands off to Albert Einstein's 1917 stimulated emission, Theodore Maiman's 16 May 1960 pink ruby laser, and Charles Kao's 1966 ultra-pure glass fibre (`042`).
- **Quirky anecdote before the hard idea:** Reverend Edward Stone drying a pound of willow bark in a paper bag on the outside of a baker's bread oven for three months; Heinrich Dreser rejecting Aspirin as dangerous while championing Heroin as a safe cough medicine eleven days later.
- **Rivalry / tension:** Arthur Eichengrün & Felix Hoffmann vs pharmacology boss Heinrich Dreser at Bayer; 74 years of blind clinical use vs John Vane's 1971 mechanistic proof.
- **Misconception explained away:** "When you swallow an aspirin tablet for a stubbed toe or a toothache, how does the pill in your stomach 'know' where the pain is? The secret is: it doesn't!" — explained via systemic COX blockade silencing prostaglandin production only where damaged cells are actively churning out alarm signals (Part 04, 4:53), plus Dreser's 1897 "bad for the heart" claim reversed by platelet thromboxane blockade in Part 05 (6:43).

## For Chief to decide

1. Lock **041 = Willow Bark to Aspirin & How Painkillers Work: Edward Stone's 25 April 1763 Royal Society Ague Trial, Felix Hoffmann's 10 August 1897 Acetylsalicylic Acid in Elberfeld & John Vane's 1971 Prostaglandin Proof (1763–1988)** and pick the 2-way Test & Compare working title pair:
   - **A (Subject + hook, §1 rule 11):** *Aspirin: The Bitter Tree Bark That Became the World's Pill* (58 chars)
   - **B (Search question, §1 rule 2):** *How Tree Bark and a Chemist's Father Gave the World Aspirin* (59 chars)
   - **Alt (Search / twist question):** *Why We Took Aspirin for 74 Years Before Knowing How It Works* (60 chars)
2. Review `aspirin_script_master_v01.md` (91.9/100 PASS), then queue the Gemini facts pass (`--kind facts`) on `SOURCES_v01.md` (rows 1–4) before VO.

## Score (`npm run review:script`)

```text
# aspirin_script_master_v01.md

**Decision:** PASS · **Score:** 91.9 / 100

| Dimension | Score |
|---|---:|
| hook | 9.5 |
| curiosity | 9.5 |
| storytelling | 8 |
| scientificAccuracy | 10 |
| emotion | 9.6 |
| escalation | 8.1 |
| retentionPotential | 9 |
| searchPotential | 9.1 |
| visualOpportunities | 9.5 |
| narrationFlow | 9.6 |

Words: 1653 · Est. min: 11 · Chapters: 4

## Cold open excerpt

> How does a tiny white aspirin tablet swallowed into your stomach know whether you have a throbbing headache in your temples or a sprained ankle? And why did a German dye-factory chemist in eighteen ninety-seven invent the world's most famous painkiller just to save his father's b

## Findings

- **[info] overall:** Structure gates 8/8 — applied +1.05 completeness boost to supporting dimensions.
- **[info] overall:** PASS 91.9/100 — proceed to VO after production checklist.

Pass threshold: 90
```
