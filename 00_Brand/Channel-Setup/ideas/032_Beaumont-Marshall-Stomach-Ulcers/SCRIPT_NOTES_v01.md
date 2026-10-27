# 032 script v01: notes for review (J0493)

Script: `ulcers_script_master_v01.md` (with `opening_and_outline_v00.md`, `SOURCES_v00.md` and `SOURCES_v01.md`).

**Draft only (J0493, Gemini Argon, 17 Oct 2026).** Built from `032_Beaumont-Marshall-Stomach-Ulcers/opening_and_outline_v00.md` and the neighbour and search evidence in `IDEAS_2026-10-17_J0470.md` (`evidence_2026-10-17_J0470/n_stomach.md` PASS — 16 education videos ≥ 1M views, including 7 strictly on digestion, stomach ulcers, stomach acid & gut microbes ≥ 1M: **TED-Ed ★ *How your digestive system works - Emma Bryce* (`Og5xAdC8EUI`, 13.91M)**, **TED-Ed ★ *How the food you eat affects your gut - Shilpa Ravella* (`1sISguPDlhY`, 7.25M)**, **TED-Ed ★ *The surprising cause of stomach ulcers - Rusha Modi* (`V_U6czbDHLE`, 4.04M — exact Barry Marshall & Robin Warren *H. pylori* match)**, **TED-Ed ★ *How does your body know you're full? - Hilary Coller* (`YVfyYrEmzgM`, 2.99M)**, **TEDx Talks ★ *Your Gut Microbiome* (`B9RruLkAUm8`, 2.44M)**, **TED-Ed ★ *You are your microbes* (`1X8p0vhsWRE`, 2.04M)**, and **TED-Ed ★ *Vultures: The acid-puking, plague-busting heroes of the ecosystem* (`1WIUuGCIfcc`, 1.62M)**, alongside `public_search.md` showing `"barry marshall stomach ulcer"` triggering autocomplete with all 5 top GB slots under 325k views and `"william beaumont alexis st martin"` having all 5 top GB slots under 93k views). The topic isn't locked yet: Chief locks `032` and the working title pair first, then reviews/signs off this script and queues the Gemini facts pass (`--kind facts`) on `SOURCES_v01.md` (rows 1–4) before VO.

Structure (*Reference lessons* §1, scripts from 011 on): every chapter opens cold and ends on a question the next one answers; the midpoint twist ("Case closed? Wrong." — after animal models failed and gastroenterologists rejected bacterial causation following their June 1984 *Lancet* paper, 32-year-old Barry Marshall underwent a clean baseline biopsy at Fremantle Hospital and in July 1984 drank a beef-broth beaker teeming with $10^9$ live *Helicobacter pylori* bacteria, developed achlorhydric vomiting and acute gastritis by Day 5–8, proved heavy *H. pylori* colonisation by endoscopy on Day 10, and cured himself on Day 14 with tinidazole and bismuth) lands in Part 04; the popular misconception ("Many people still think a spicy curry or a stressful week at work burns an ulcer straight into your stomach — or wonder why pH 1.5 acid doesn't digest your own stomach wall") is raised and explained away in Part 05 via the 1-millimetre mucus-bicarbonate shield keeping the stomach wall at neutral pH 7.0 against pH 1.5 lumen acid; the ending hands off directly to `033` (*Sparks & Synapses: Santiago Ramón y Cajal's 1887–1888 Kitchen Silver Stain in Barcelona & Otto Loewi's March 1921 3:00 a.m. Easter Dream of Two Frog Hearts*), with no goodbye and no subscribe ask. Five VO parts, matching 009–031.

## Marker count (v01)

Run on `ulcers_script_master_v01.md`: `grep -o "DATA:" … | wc -l`, and the same for each marker.

| Marker | Count | Where | Rule |
|---|---:|---|---|
| `DATA` | **6** | 1) inked pH and ulcer-cause chart on period paper showing human stomach acid at pH 1.5–2.0 (nearly as acidic as car battery acid at pH 0.8 and a million times more acidic than pure water at pH 7.0) and H. pylori causing ~80% of gastric ulcers and ~90% of duodenal ulcers (0:34); 2) inked pH scale bar (pH 7.0 water vs pH 1.5 gastric hydrochloric acid = ~300,000–1,000,000× higher H⁺ concentration) (0:52); 3) inked digestion-time chart on period paper from Beaumont's 1833 book comparing boiled tripe & whipped eggs (~1 hour), boiled beef (~2 hours 45 minutes), and roast pork (~5 hours 15 minutes) alongside in-vitro hydrochloric acid + pepsin digestion at 37.8 °C (1:58); 4) inked biopsy & incubation chart on period paper from Warren & Marshall's 100-patient Perth study (1982–1984) showing 0 colonies at 48 hours vs 1 mm H. pylori colonies at 5 days (120 hours), present in 100% of duodenal ulcer patients (13/13) and 82% of gastric ulcer patients (18/22) (3:42); 5) inked timeline and mechanism diagram on period paper of Barry Marshall's July 1984 self-experiment (Day 0: baseline clean biopsy + drinks 10⁹ H. pylori; Day 5–8: achlorhydric vomiting & gastritis; Day 10: biopsy proves heavy H. pylori colonisation; Day 14: cured by antibiotic + bismuth) alongside H. pylori's urease enzyme splitting urea into alkaline ammonia (NH₃) to neutralise pH 1.5 acid (5:28); 6) animated timeline building 6 Jun 1822 & Dec 1823 · May 1825–Dec 1833 · 11 Jun 1979 & 13 Apr 1982 · Jul 1984 · 2005 alongside an inked cross-section of the 1-millimetre mucus-bicarbonate shield keeping the stomach wall at neutral pH 7.0 against pH 1.5 lumen acid (6:43) | 3 or more per long, including the animated timeline |
| `SCALE` | **6** | 1) human stomach acid sits near pH 1.5 — strong enough to dissolve a zinc nail and a million times more acidic than pure water, yet H. pylori wraps itself in an ammonia bubble to survive inside it (0:34); 2) stomach acid is nearly a million times more acidic than drinking water — so harsh that doctors assumed the stomach was as sterile as a bottle of bleach (0:52); 3) by pulling a silk thread in and out of a living stomach 238 times, Beaumont timed digestion to the minute — from one hour for eggs to over five hours for roast pork (1:58); 4) throwing Petri dishes away after two days blinded doctors for decades — three extra days over the Easter weekend revealed the germ in nearly every duodenal ulcer patient (3:42); 5) one billion spiral bacteria in a single glass of broth — using an enzyme shield to turn lethal stomach acid into a cosy neutral home in just five days (5:28); 6) a mucus-and-bicarbonate shield just one millimetre thick separates pH 1.5 acid strong enough to dissolve metal from the delicate pH 7.0 cells of your stomach wall (6:43) | Every `DATA` number gets a `SCALE:` comparison (`grep -c "SCALE:"` ≥ `DATA:` count) |
| `WHO` | **5** | William Beaumont (0:34), Alexis St. Martin (0:34), Robin Warren (0:34), Barry Marshall (0:34), William Prout (1:28) | First mention only, role right for the scene's year (4 words or fewer) |
| `WHEN` | **19** | Mackinac Island May 1825 (0:00), Perth July 1984 (0:00), Mackinac Island 6 June 1822 (0:21), May 1825 (0:34), April 1982 (0:34), July 1984 (0:34), 23 December 1823 (1:28), May 1825 (1:28), August 1825 (1:28), December 1833 (1:28), 11 June 1979 (3:08), July 1981 (3:08), 13 April 1982 (3:08), 16 June 1984 (4:53), July 1984 (4:53), 2005 (4:53), 1822–2005 (6:43), 1887 (7:45), March 1921 (7:45) | Every spoken date or era; later dates drop onto the timeline |
| `FACT` | **4** | 238 silk-string tests (1:28); Left over 5-day Easter (3:08); Drank a billion bacteria (4:53); 1 mm mucus shield saves gut (6:43) | 2–4 per long (4 words or fewer per card) |

## Craft checks (*Reference lessons* §1 + *Polish pass*)

- **First-minute timings:** Answer image by 0:03 (William Beaumont at Fort Mackinac in May 1825 lowering boiled beef on a silk string into Alexis St. Martin's stomach fistula, dissolving to Barry Marshall at Royal Perth Hospital in July 1984 drinking a beaker of a billion *H. pylori* bacteria), title question by 0:07, promise by 0:15, stakes by 0:25, first concrete answer & real fact (Beaumont's 238 silk-string experiments proving hydrochloric acid digestion at pH 1.5 and Warren & Marshall's discovery that *H. pylori* survives that acid and causes 80–90% of peptic ulcers) by 0:34.
- **Explorer limits:** 2 beats total (`[EXPLORER ACTS: once. …]`), at 1:05 (Part 01, outside the first minute) and 6:05 (Part 04 watching *H. pylori* spin its flagella and spray an alkaline ammonia shield against falling hydrochloric acid drops).
- **Chapter cold opens & cliffhanger questions:** Part 01 ends on what doctors before 1825 thought happened to food after you swallowed it and how a fur trapper who ran away to Canada three times changed medicine; Part 02 opens cold on the mechanical millstone vs stewpot vs rotting vat debate, the 6 June 1822 accidental shotgun wound on Mackinac Island, Beaumont's 238 silk-string and 100 °F glass-vial experiments alongside William Prout's 23 December 1823 discovery of gastric hydrochloric acid, ending on how Beaumont's proof of pH 1.5 stomach acid created a 150-year medical blind spot; Part 03 opens cold on the "sterile stomach / stress causes ulcers" dogma, Robin Warren's 11 June 1979 birthday biopsy, Barry Marshall's July 1981 100-patient study, and plate #35 left in the incubator over the 5-day April 1982 Easter holiday, ending on why specialists still mocked them and what drove Marshall to drink a glass of bacteria himself; Part 04 opens cold on the midpoint twist ("Case closed? Wrong." — failed piglet infections, Marshall's June 1984 baseline biopsy, drinking $10^9$ *H. pylori* in July 1984, the urease ammonia shield, Day 5–8 vomiting, Day 10 biopsy proof, Day 14 antibiotic cure, and the 2005 Nobel Prize), ending on why your stomach doesn't digest itself every afternoon; Part 05 opens cold on the spicy-food and self-digestion misconception, explains the 1-millimetre mucus-bicarbonate shield, and hands off to Santiago Ramón y Cajal's 1887–1888 Barcelona silver-stained neurons and Otto Loewi's March 1921 3:00 a.m. Easter frog-heart experiment (`033`).
- **Quirky anecdote before the hard idea:** William Beaumont tying chunks of roast beef and cabbage to a silk string and chasing his homesick patient Alexis St. Martin whenever he paddled back to Canada; biopsy plate #35 only growing *H. pylori* because lab technicians left it in the incubator over a five-day Easter holiday weekend.
- **Rivalry / tension:** Robin Warren and young registrar Barry Marshall laughed off the stage by gastroenterologists protecting the stress-and-acid-blocker orthodoxy, driving Marshall to secretly infect himself before telling his wife.
- **Misconception explained away:** "Many people still think a spicy curry or a stressful week at work burns an ulcer straight into your stomach — or wonder why pH 1.5 acid doesn't digest your own stomach wall" — explained via the 1-millimetre mucus-and-bicarbonate barrier keeping the stomach wall at pH 7.0 unless breached by *H. pylori* or heavy painkiller use (Part 05, 6:43).

## For Chief to decide

1. Lock **032 = Stomach Acid & the Ulcer Myth: William Beaumont's 1825 Silk-String Stomach Window on Mackinac Island & Barry Marshall Drinking *H. pylori* in 1984 (1822–1984)** and pick the 2-way Test & Compare working title pair:
   - **A (Subject + hook, §1 rule 11):** *Stomach Ulcers: Why a Doctor Drank a Beaker of Bacteria* (55 chars)
   - **B (Search question, §1 rule 2):** *How a Silk String in a Stomach Wound Solved Digestion* (53 chars)
   - **Alt (Search / twist question):** *Why Doctors Blamed Stress for Ulcers Until One Drank Bacteria* (61 chars)
2. Review `ulcers_script_master_v01.md` (91.6/100 PASS), then queue the Gemini facts pass (`--kind facts`) on `SOURCES_v01.md` (rows 1–4) before VO.

## Score (`npm run review:script`)

```text
# ulcers_script_master_v01.md

**Decision:** PASS · **Score:** 91.6 / 100

| Dimension | Score |
|---|---:|
| hook | 9.5 |
| curiosity | 9.5 |
| storytelling | 8 |
| scientificAccuracy | 10 |
| emotion | 9.6 |
| escalation | 7.8 |
| retentionPotential | 9 |
| searchPotential | 9.1 |
| visualOpportunities | 9.5 |
| narrationFlow | 9.6 |

Words: 1666 · Est. min: 11.1 · Chapters: 4

## Cold open excerpt

> Why did doctors blame stress for stomach ulcers for a century — until a young physician mixed a billion bacteria into a beaker and drank it? By the end of this film, you'll see how a freak musket wound on the American frontier let a doctor watch human digestion through a living w

## Findings

- **[info] overall:** Structure gates 8/8 — applied +1.05 completeness boost to supporting dimensions.
- **[info] overall:** PASS 91.6/100 — proceed to VO after production checklist.

Pass threshold: 90
```
