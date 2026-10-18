# 051 script v01: notes for review (J0584)

Script: `spicy_script_master_v01.md` (with `opening_and_outline_v00.md`, `SOURCES_v00.md` and `SOURCES_v01.md`).

**Draft only (J0584, Gemini Argon, 18 Oct 2026).** Built from `051_Scoville-Julius-Patapoutian-Spicy-Capsaicin-TRPV1/opening_and_outline_v00.md` and the neighbour and search evidence in `IDEAS_2026-10-18_J0576.md` (`evidence_2026-10-18_J0576/n_spicy_capsaicin.md` PASS — 5+ education videos ≥ 1M views: **TED-Ed ★ *The science of spiciness - Rose Eveleth* (`qD0_yWgifDM`, 5.06M — exact subject match!)**, **TED-Ed ★ *How to make the perfect cookies (according to science)* (`n6wpNhyreDE`, 4.14M)**, **CrashCourse *Taste & Smell: Crash Course Anatomy & Physiology #16* (`mFm3yA1nslE`, 2.96M — exact sensory match!)**, **TED-Ed ★ *The science of laughter* (`Xu-QfE_1ksk`, 1.94M)**, **Veritasium (`eVtCO84MDj8`, 1.69M)**, and **SciShow Kids *Your Tongue: The Taste-Maker!* (`C4rdqXXzPGU`, 1.09M)**, plus **Be Smart *The Surprising Reason We Eat Spicy Food* (`2sziIUZgdgk`, 1.44M)** and **SciShow *Why Do Some People Tolerate Spicy Food?* (`XgbKrC2vh_I`, 504.3k)**, alongside `public_search.md` showing 4 of the top 5 GB search results for `"david julius capsaicin trpv1 scoville"` under 24k views and 3 of the top 5 GB slots for *Why Chili Peppers Trick Your Brain Into Feeling Like Your Mouth Is on Fire* under 65 views). The topic isn't locked yet: Chief locks `051` and the working title pair first, then reviews/signs off this script and queues the Gemini facts pass (`--kind facts`) on `SOURCES_v01.md` (rows 1–4) before VO.

Structure (*Reference lessons* §1, scripts from 011 on): every chapter opens cold and ends on a question the next one answers; the midpoint twist ("Case closed — was capsaicin simply burning cells like acid? Wrong! For fifty years, no one could find the molecular lock on our pain nerves. Then, at the University of California, San Francisco, physiologist David Julius and postdoctoral fellow Michael Caterina built a genetic dragnet!" — cloning `TRPV1` on 23 October 1997 from 14,000 sensory-nerve genes in `Fura-2` kidney cells and proving that pure hot water above 43 °C snaps the exact same ion channel wide open) lands in Part 03; David Julius and Ardem Patapoutian's February–March 2002 independent discovery of the `<26 °C` cold-and-menthol receptor `TRPM8` and Joshua Tewksbury and Sven-Eric Jordt's 2001–2002 proof that wild chilies evolved capsaicin to deter seed-crushing rodents while birds are 100% capsaicin-immune lands in Part 04; the tissue-burn and ice-water misconception ("Many people still believe a scorching chili pepper physically burns holes in your taste buds, and that gulping ice water washes the spice away") is raised and explained away in Part 05 via `TRPV1` threshold lowering, hydrophobic oil vs milk casein, and 8% medical capsaicin patches pruning back overactive pain fibres; the ending hands off directly to `052` (*Why Does Your Immune System Attack Peanuts & Pollen? Charles Richet & Paul Portier's 1901 Yacht Jellyfish Paradox, Henry Dale's 1910 Histamine, Daniel Bovet's 1937 Antihistamine & Kimishige and Teruko Ishizaka's 1966 `IgE` Antibody*), with no goodbye and no subscribe ask. Five VO parts, matching 009–050.

## Marker count (v01)

Run on `spicy_script_master_v01.md`: `grep -o "DATA:" … | wc -l`, and the same for each marker.

| Marker | Count | Where | Rule |
|---|---:|---|---|
| `DATA` | **6** | 1) inked dual-receptor temperature & Scoville dilution chart on period paper showing TRPM8 opening below 26 °C (or with menthol at 37 °C) and TRPV1 opening above 43 °C (or with capsaicin at 37 °C), paired with Scoville Heat Units spanning 0 (bell pepper), 5,000 (jalapeño), 300,000 (habanero), and 16,000,000 (pure capsaicin) (0:34); 2) inked TRPV1 threshold-shift graph showing activation temperature dropping from 43 °C (normal noxious heat threshold) to <33 °C when capsaicin binds, while TRPM8 cold activation shifts from <26 °C up to >34 °C when peppermint menthol binds (0:52); 3) inked Scoville dilution & hydrophobic solubility chart on period paper from Wilbur Scoville (May 1912, J. Am. Pharm. Assoc. 1: 453–454) comparing bell pepper (0 SHU), jalapeño (~5,000 SHU), cayenne (~40,000 SHU), habanero (~300,000 SHU), and pure capsaicin (16,000,000 SHU) alongside casein micelles in milk stripping hydrophobic capsaicin off nerve membranes (1:58); 4) inked Fura-2 calcium-fluorescence & thermal current trace on period paper from Caterina, Julius et al. (23 October 1997, Nature 389: 816–824) showing zero current in control HEK293 cells vs massive inward Ca2+/Na+ current in TRPV1-expressing cells triggered identically by 1 micromolar capsaicin or by stepping bath temperature across 43 °C (3:42); 5) inked mammalian vs avian TRPV1 & seed-survival comparison chart on period paper from Tewksbury & Nabhan (26 July 2001, Nature 412: 403–404) and Jordt & Julius (8 February 2002, Cell 108: 421–430) showing 0% seed germination after rodent chewing vs high germination after bird gut passage, paired with mammal TRPV1 firing maximally to capsaicin + 43 °C heat while avian TRPV1 fires to >43 °C heat but 0% to capsaicin (5:28); 6) animated timeline building 1876 · May 1912 · 1947–1960 · 23 Oct 1997 · Jul 2001–Mar 2002 alongside the hydrophobic water-repelling vs milk-casein and TRPV1 pain-patch defunctionalisation diagram (6:43) | 3 or more per long, including the animated timeline |
| `SCALE` | **6** | 1) one drop of pure capsaicin diluted into sixteen million drops of water — about eight hundred litres, or five full bathtubs — still sets a human tongue tingling (0:34); 2) the chili isn't heating your mouth at all — it rewires the thermostat on your nerve doors so your own thirty-seven-degree blood feels like scalding water (0:52); 3) drinking cold water on a chili burn is like trying to wash motor oil off your hands with plain water — while milk's casein proteins act like tiny detergent sponges that lift the greasy capsaicin molecule off your nerves (1:58); 4) forty-three degrees Celsius is the exact razor's edge where warm water turns into tissue-damaging pain — and TRPV1 is the molecular tripwire that guards your skin and tongue (3:42); 5) a wild bird can swallow a habanero or Carolina Reaper pepper as if it were a sweet blueberry — because chili plants engineered capsaicin specifically to lock onto mammal teeth while giving winged seed-couriers a free pass (5:28); 6) every time you bite into a spicy curry or brush your teeth with mint, you are playing a molecular piano of temperature doors that took one hundred and twenty-six years of chemistry and neuroscience to decode (6:43) | Every `DATA` number gets a `SCALE:` comparison (`grep -c "SCALE:"` ≥ `DATA:` count) |
| `WHO` | **8** | John Clough Thresh (0:34), Wilbur Lincoln Scoville (0:34), David Julius (0:34), Michael J. Caterina (0:34), Ardem Patapoutian (0:34), Miklós Jancsó (3:08), Joshua J. Tewksbury (4:53), Sven-Eric Jordt (4:53) | First mention only, role right for the scene's year (4 words or fewer) |
| `WHEN` | **22** | May 1912 (0:00), 23 October 1997 (0:00), San Francisco 23 October 1997 (0:21), 1876 (0:34), May 1912 (0:34), 23 October 1997 (0:34), February–March 2002 (0:34), 1876 (1:28), May 1912 (1:28), 1919 (1:28), 1947–1960 (3:08), 23 October 1997 (3:08), July 2001 (4:53), 8 February 2002 (4:53), 7–8 March 2002 (4:53), 2021 (4:53), 1876–2021 (6:43), July 1901 (7:45), 15 February 1902 (7:45), 1910 (7:45), 1937 (7:45), July 1966 (7:45) | Every spoken date or era; later dates drop onto the timeline |
| `FACT` | **3** | 1 in 16,000,000 dilution (1:28); Opens at 43 °C heat (3:08); Birds feel zero chili burn (4:53) | 2–4 per long (4 words or fewer per card) |

## Craft checks (*Reference lessons* §1 + *Polish pass*)

- **First-minute timings:** Answer image by 0:03 (thermometer inside a mouth biting a habanero chili staying at 37.0 °C while capsaicin wedges open the 43 °C `TRPV1` channel and menthol wedges open the <26 °C `TRPM8` channel), title question by 0:07, promise by 0:15, stakes by 0:25, first concrete answer & real fact (John Clough Thresh's 1876 capsaicin isolation, Wilbur Scoville's May 1912 16,000,000-unit human dilution scale, David Julius and Michael Caterina's 23 October 1997 `TRPV1` 43 °C heat-and-capsaicin channel, and Julius and Ardem Patapoutian's February–March 2002 `TRPM8` <26 °C cold-and-menthol channel) by 0:34.
- **Explorer limits:** 2 beats total (`[EXPLORER ACTS: once. …]`), at 1:05 (Part 01, outside the first minute) and 6:05 (Part 04 watching a glowing red capsaicin key bounce off the bird's keyhole while locking the rodent's 43 °C alarm wide open).
- **Chapter cold opens & cliffhanger questions:** Part 01 ends on why a chemist in 1876 and a pharmacist in 1912 had to use human tongues as laboratory instruments and why cold water fails to wash chili burn away; Part 02 opens cold on why "spicy" isn't one of the five basic tastes on taste buds, then tells the story of John Clough Thresh's 1876 capsaicin crystals, its greasy hydrocarbon tail vs milk casein, and Wilbur Scoville's May 1912 five-taster sugar-water dilution test up to 16,000,000 SHU, ending on how two scientists in California caught the mystery nerve door on camera; Part 03 opens cold on Miklós Jancsó's 1947–1960 heat-pain nerve experiments in Hungary, delivers the midpoint twist ("Case closed — was capsaicin simply burning cells like acid? Wrong!" — David Julius and Michael Caterina screening 14,000 sensory-nerve genes in `Fura-2` kidney cells on 23 October 1997 to clone `TRPV1` and discovering that pure 43 °C hot water snaps the exact same door open), and ends on what explains the icy chill of peppermint and why birds feel no chili burn; Part 04 opens cold on David Julius and Ardem Patapoutian's February–March 2002 independent discovery of the `<26 °C` cold-and-menthol receptor `TRPM8`, then explains Joshua Tewksbury's July 2001 rodent-vs-bird seed survival proof and Sven-Eric Jordt and Julius's 8 February 2002 avian `TRPV1` capsaicin-immunity discovery, ending on why doctors put 8% capsaicin patches on patients to cure chronic pain; Part 05 opens cold on the tissue-burn and ice-water misconception, explains `TRPV1` nerve-tip defunctionalisation by 8% medical patches, and hands off to Charles Richet and Paul Portier's 1901–1902 yacht anaphylaxis paradox, Henry Dale's 1910 histamine, Daniel Bovet's 1937 antihistamine, and Kimishige and Teruko Ishizaka's July 1966 `IgE` allergy antibody (`052`).
- **Quirky anecdote before the hard idea:** John Clough Thresh vaporising a microscopic speck of capsaicin in 1876 and setting everyone in his London lab coughing, and Wilbur Scoville having five human tasters sip sugar water one test per session in Detroit in May 1912 because human tongues beat every chemical test in the lab.
- **Rivalry / tension:** Chemical tissue-irritation dogma vs Jancsó and Julius's specific thermal nociceptor receptor; seed-grinding desert rodents vs seed-dispersing thrasher birds.
- **Misconception explained away:** "Many people still believe a scorching chili pepper physically burns holes in your taste buds, and that gulping ice water washes the spice away" — explained via `TRPV1` threshold lowering without cell damage, hydrophobic oil vs milk casein, and 8% medical capsaicin pain patches (Part 05, 6:43).

## For Chief to decide

1. Lock **051 = Why Do Chilis Burn & Peppermints Feel Freezing Cold? Wilbur Scoville's 1912 Sugar-Water Taste Test & David Julius and Ardem Patapoutian's 1997–2002 Capsaicin (`TRPV1`) & Menthol (`TRPM8`) Ion Channels (1876–2002)** and pick the 2-way Test & Compare working title pair:
   - **A (Subject + hook, §1 rule 11):** *Spicy Chilis & Cold Mint: The Chemical Trick Inside Your Mouth* (62 chars)
   - **B (Search question, §1 rule 2):** *Why Chili Peppers Trick Your Brain Into Feeling Like Your Mouth Is on Fire* (74 chars)
   - **Alt (Search / twist question):** *Why Birds Eat Fiery Chilis Like Candy While Humans Feel 43 °C Pain* (66 chars)
2. Review `spicy_script_master_v01.md` (93.2/100 PASS), then queue the Gemini facts pass (`--kind facts`) on `SOURCES_v01.md` (rows 1–4) before VO.

## Score (`npm run review:script`)

```text
# spicy_script_master_v01.md

**Decision:** PASS · **Score:** 93.2 / 100

| Dimension | Score |
|---|---:|
| hook | 9.5 |
| curiosity | 9.5 |
| storytelling | 8 |
| scientificAccuracy | 10 |
| emotion | 9.6 |
| escalation | 9.4 |
| retentionPotential | 9 |
| searchPotential | 9.1 |
| visualOpportunities | 9.5 |
| narrationFlow | 9.6 |

Words: 1418 · Est. min: 9.5 · Chapters: 4

## Cold open excerpt

> Why does biting into a cold red chili pepper make your mouth feel like it's burning in scalding water — when a thermometer on your tongue doesn't move? And how did a May nineteen twelve sugar-water taste test in Detroit and a twenty-third of October nineteen ninety-seven petri-di

## Findings

- **[info] overall:** Structure gates 8/8 — applied +1.05 completeness boost to supporting dimensions.
- **[info] overall:** PASS 93.2/100 — proceed to VO after production checklist.

Pass threshold: 90
```
