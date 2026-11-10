# 017 script v01: notes for review (J0412)

Script: `oxygen_script_master_v01.md` (with `opening_and_outline_v00.md`, `SOURCES_v00.md` and `SOURCES_v01.md`).

**Draft only (J0412, Gemini Argon, 16 Oct 2026).** Built from `017_Priestley-Lavoisier-Oxygen/opening_and_outline_v00.md` and the neighbour and search evidence in `IDEAS_2026-10-16_J0388.md` (`evidence_2026-10-16_J0388/n_oxygen2.md` PASS — 3 big education videos ≥ 1M views led by **TED-Ed ★ *Oxygen's surprisingly complex journey through your body* 3.52M**, **TED-Ed ★ *The law of conservation of mass - Todd Ramsey* 2.42M** featuring Antoine Lavoisier, and Khan Academy *Conservation of energy* 1.17M — plus `public_search.md` & `public_search_titles.md` showing all 5 top GB slots under 370k views on `"who discovered oxygen priestley lavoisier"` and `"law of conservation of mass lavoisier"`). The topic isn't locked yet: Chief locks `017` and the working title pair first, then reviews/signs off this script and queues the Gemini facts pass (`--kind facts`) on `SOURCES_v01.md` (rows 1–15) before VO.

Structure (*Reference lessons* §1, scripts from 011 on): every chapter opens cold and ends on a question the next one answers; the midpoint twist ("Case closed? Wrong." — Carl Wilhelm Scheele isolating "fire air" in Sweden in 1771–1772 two full years before Priestley and mailing a French letter to Lavoisier on 30 September 1774 that remained hidden until 1890) lands in Part 04; the popular misconception ("When you diet and lose ten kilograms of fat, most people — and even many doctors — think that weight turns into heat or energy. Is that true?") is raised and explained away in Part 05 with Lavoisier's Law of Conservation of Mass and the 2014 *BMJ* mass-balance study (8.4 kg / 84% exhaled as $\text{CO}_2$, 1.6 kg / 16% as water); the ending hands off directly to `018` (*Invisible Light: William Herschel's Thermometer Past the Rainbow & Ritter's Ultraviolet*), with no goodbye and no subscribe ask. Five VO parts, matching 009–016.

## Marker count (v01)

Run on `oxygen_script_master_v01.md`: `grep -o "DATA:" … | wc -l`, and the same for each marker.

| Marker | Count | Where | Rule |
|---|---:|---|---|
| `DATA` | **5** | 1) inked comparison of ordinary air (21% oxygen, 15-minute mouse survival) vs Priestley's bell-jar gas (100% oxygen, 30-minute survival) and Lavoisier's balance precision (1/400th of a grain) (0:34); 2) inked daily-breath comparison showing 17,000 breaths/day and 550 litres of pure oxygen consumed per person every day (0:52); 3) inked pneumatic-trough diagram showing a 12-inch lens heating red mercuric oxide over liquid mercury to release 4–5× its volume in pure oxygen gas (1:56); 4) inked mass-balance diagram of Lavoisier's 12-day swan-neck retort: 50 cubic inches of air loses 8–9 cubic inches (~1/5th) as 45 grains of red oxide gain 3.5 grains, then heating yields 41.5 grains mercury + 3.5 grains (8–9 in³) oxygen (4:08); 5) animated timeline building 1703 · 1772 · 1 Aug 1774 · Oct 1774 · 1777 · 1789 · 8 May 1794 alongside an inked 10 kg fat mass-balance chart (8.4 kg CO2 exhaled vs 1.6 kg H2O) (6:43) | 3 or more per long, including the animated timeline |
| `SCALE` | **5** | 1) 1/400th of a grain — sensitive enough to weigh a single eyelash (0:34); 2) 550 litres of oxygen a day — enough to fill three bathtubs (0:52); 3) 12-inch lens focusing sunlight to over 600°C — hot enough to split solid red powder into liquid metal and gas (1:56); 4) 8 to 9 cubic inches out of 50 — roughly 1/5th of every breath you take is oxygen (4:08); 5) 8.4 kilograms out of every 10 kilograms of fat you lose is breathed out as invisible gas (6:43) | Every `DATA` number gets a `SCALE:` comparison (`grep -c "SCALE:"` ≥ `DATA:` count) |
| `WHO` | **7** | Joseph Priestley (0:34), Antoine Lavoisier (0:34), Georg Ernst Stahl (2:48), Marie-Anne Paulze Lavoisier (3:08), Carl Wilhelm Scheele (4:58), Pierre-Simon Laplace (5:30), Joseph-Louis Lagrange (7:15) | First mention only, role right for the scene's year (4 words or fewer) |
| `WHEN` | **22** | Wiltshire 1 August 1774 (0:00), 1770s (0:21), 1 August 1774 (0:34), Leeds 1767 (1:28), 30 November 1773 (1:28), 1 August 1774 (1:56), 8 March 1775 (2:25), 1703 (2:48), Paris October 1774 (3:08), 26 April 1775 (3:38), 1777 (4:08), Sweden 1771–1772 (4:58), 30 September 1774 (4:58), 1890 (4:58), 1780–1783 (5:30), Paris 1789 (5:58), 2014 (6:43), 1703–1794 (6:43), July 1791 (7:15), 8 May 1794 (7:15), 6 February 1804 (7:15), February 1800 (7:45) | Every spoken date or era; later dates drop onto the timeline |
| `FACT` | **4** | Invented fizzy soda water (1:28); Tried to claim sole credit (3:38); Scheele made oxygen first (1772) (4:58); Exhale 84% of lost fat (6:43) | 2–4 per long (4 words or fewer per card) |

## Craft checks (*Reference lessons* §1 + *Polish pass*)

- **First-minute timings:** Answer image by 0:03 (12-inch burning lens at Bowood House focusing sunlight onto red mercury powder over mercury as a candle erupts into dazzling flame beside a lively mouse), title question by 0:07, promise by 0:15, stakes by 0:25, first concrete answer & real fact (Joseph Priestley on 1 August 1774 and Antoine Lavoisier weighing oxygen to 1/400th of a grain, 21% of air) by 0:34.
- **Explorer limits:** 2 beats total (`[EXPLORER ACTS: once. …]`), at 1:05 (Part 01, outside the first minute) and 5:58 (Part 04 watching the needle of Lavoisier's giant brass balance hold at zero beside the foaming fermentation flask).
- **Chapter cold opens & cliffhanger questions:** Part 01 ends on why scientists were fooled for a century by phlogiston and how a Leeds brewery led Priestley to his bell jar; Part 02 opens cold on Priestley's 1767 fizzy soda-water discovery next door to the Leeds brewery before his 1 August 1774 burning-lens and 8 March 1775 mouse experiments, ending on why phlogiston collapsed on a pair of scales and what happened at the October 1774 Paris dinner; Part 03 opens cold on the metal-rusting mass paradox and the Lavoisiers' 12-day sealed swan-neck retort experiment, ending on why Swedish pharmacist Carl Wilhelm Scheele had reason to be furious with both of them; Part 04 opens cold on the midpoint twist ("Case closed? Wrong." — Scheele's 1771–1772 discovery and his 30 September 1774 letter to Lavoisier uncovered in 1890), followed by the guinea-pig ice calorimeter and the 1789 Law of Conservation of Mass, ending on where 10 kg of lost body fat goes; Part 05 opens cold on the weight-loss-turns-to-energy misconception (84% exhaled as $\text{CO}_2$), tells the tragic 1791–1794 endings of Priestley and Lavoisier, and hands off to William Herschel's February 1800 thermometer past the rainbow (`018`).
- **Quirky anecdote before the hard idea:** Priestley pouring water between two glasses in the carbon-dioxide cloud over fermenting beer vats at the Jopson brewery in Leeds in 1767 to invent fizzy soda water before his pneumatic trough and mercuric-oxide gas decomposition.
- **Rivalry / debate:** back-and-forth portrait cuts between Joseph Priestley in England and Antoine Lavoisier in Paris after Lavoisier's 26 April 1775 Easter Memoir (3:38).
- **Misconception explained away:** "When you diet and lose ten kilograms of fat, most people — and even many doctors — think that weight turns into heat or energy. Is that true?" — refuted by Lavoisier's conservation of mass and the 2014 *BMJ* calculation proving 8.4 kg (84%) is exhaled as carbon dioxide and 1.6 kg (16%) leaves as water (Part 05, 6:43).

## For Chief to decide

1. Lock **017 = Oxygen & the Phlogiston Myth: Priestley's Bell Jar & Lavoisier's Balance (1774–1789)** and pick the 2-way Test & Compare working title pair:
   - **A (Subject + hook, §1 rule 11):** *Oxygen: The Bell-Jar Experiment That Proved Air Has Weight* (58 chars)
   - **B (Search question, §1 rule 2):** *Why the Man Who Discovered Oxygen Insisted It Didn't Exist* (58 chars)
   - **Alt (Search / experiment hook):** *How a Burning Lens and a Mouse Revealed What You Breathe* (56 chars)
2. Review `oxygen_script_master_v01.md` (93.9/100 PASS), then queue the Gemini facts pass (`--kind facts`) on `SOURCES_v01.md` (rows 1–15) before VO.

## Score (`npm run review:script`)

```text
# oxygen_script_master_v01.md

**Decision:** PASS · **Score:** 93.9 / 100

| Dimension | Score |
|---|---:|
| hook | 9.5 |
| curiosity | 9.5 |
| storytelling | 9 |
| scientificAccuracy | 10 |
| emotion | 9.6 |
| escalation | 9.1 |
| retentionPotential | 9 |
| searchPotential | 9.1 |
| visualOpportunities | 9.5 |
| narrationFlow | 9.6 |

Words: 1564 · Est. min: 10.4 · Chapters: 4

## Cold open excerpt

> Why does a rusted iron nail weigh more than it did when it was shiny and new? And when an English experimenter first trapped pure oxygen under a glass bell jar with a magnifying lens and helped a trapped mouse survive twice as long, why did he go to his grave insisting that oxyge

## Findings

- **[info] overall:** Structure gates 8/8 — applied +1.05 completeness boost to supporting dimensions.
- **[info] overall:** PASS 93.9/100 — proceed to VO after production checklist.

Pass threshold: 90
```
