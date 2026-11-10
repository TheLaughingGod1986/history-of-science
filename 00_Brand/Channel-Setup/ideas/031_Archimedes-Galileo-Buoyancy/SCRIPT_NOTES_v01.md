# 031 script v01: notes for review (J0478)

Script: `archimedes_script_master_v01.md` (with `opening_and_outline_v00.md`, `SOURCES_v00.md` and `SOURCES_v01.md`).

**Draft only (J0478, Gemini Argon, 17 Oct 2026).** Built from `031_Archimedes-Galileo-Buoyancy/opening_and_outline_v00.md` and the neighbour and search evidence in `IDEAS_2026-10-17_J0470.md` (`evidence_2026-10-17_J0470/n_archimedes.md` PASS — 5 education videos ≥ 1M views, led by 2 exact TED-Ed Archimedes films ≥ 1M: **TED-Ed ★ *The real story behind Archimedes’ Eureka! - Armand D'Angour* (`0v86Yk14rf8`, 4.39M — exact Galileo underwater balance & *Syracusia* match)**, **TED-Ed ★ *How taking a bath led to Archimedes' principle - Mark Salata* (`ijj58xD5fDI`, 1.88M)**, **Khan Academy *Probability density functions* (`Fvi9A_tEmXQ`, 2.60M)**, **CrashCourse *Fluids in Motion: Crash Course Physics #15* (`fJefjG3xhW0`, 1.40M)**, and **CrashCourse *Fluids at Rest: Crash Course Physics #14* (`b5SqYuWT4-4`, 1.16M)**, alongside `public_search.md` showing `"archimedes principle buoyancy"` autocompleting in GB search with 3 of the top 5 GB slots under 926k views). The topic isn't locked yet: Chief locks `031` and the working title pair first, then reviews/signs off this script and queues the Gemini facts pass (`--kind facts`) on `SOURCES_v01.md` (rows 1–4) before VO.

Structure (*Reference lessons* §1, scripts from 011 on): every chapter opens cold and ends on a question the next one answers; the midpoint twist ("Case closed? Wrong." — Archimedes used the exact same law of buoyancy to design the ~4,000-tonne ancient palace ship *Syracusia* around 240 BC, and after his death in 212 BC his only surviving Greek manuscript of *On Floating Bodies* and *The Method* was scraped off parchment and overwritten into an Easter prayer book by scribe Johannes Myronas in April 1229, rediscovered under a magnifying glass in Constantinople by Johan Ludvig Heiberg in 1906, and finally recovered in May 2005 – 2008 when Stanford synchrotron X-rays excited the iron atoms in Archimedes' erased ink) lands in Part 04; the popular misconception ("Many people think buoyancy only works on things that float at the surface, or that deep water crushes a sinking rock downward faster") is raised and explained away in Part 05 via depth-dependent fluid pressure ($P = \rho g h$) pushing upward harder on the bottom of every submerged object than downward on its top ($F_b = \rho V g$); the ending hands off directly to `032` (*Stomach Acid & the Ulcer Myth: William Beaumont's May 1825 Silk-String Stomach Window on Mackinac Island & Barry Marshall Drinking a Beaker of H. pylori in July 1984*), with no goodbye and no subscribe ask. Five VO parts, matching 009–030.

## Marker count (v01)

Run on `archimedes_script_master_v01.md`: `grep -o "DATA:" … | wc -l`, and the same for each marker.

| Marker | Count | Where | Rule |
|---|---:|---|---|
| `DATA` | **6** | 1) inked comparison diagram on period paper showing a 1,000 g pure gold block (51.8 cm³) vs a 1,000 g crown with 30% silver (64.8 cm³): a 13.1 cm³ volume difference (<1 tablespoon) that raises a 30 cm tub by only 0.18 mm, but creates a 13.1-gram upward buoyant force imbalance when weighed underwater (0:34); 2) inked scale comparison of 0.18 mm water-level rise in a 30 cm basin vs 13.1 g buoyant lift on a submerged hydrostatic balance (0:52); 3) inked atomic density and volume comparison on period paper showing 1,000 g of pure gold (density 19.32 g/cm³, volume 51.76 cm³) vs 1,000 g of a 70% gold / 30% silver crown (silver density 10.49 g/cm³, total volume 64.83 cm³) — identical 1,000 g weight in air, 13.07 cm³ extra volume (1:58); 4) inked schematic of Archimedes' Proposition 7 underwater balance and Galileo's 1586 wire-wrapped La Bilancetta showing 1,000 g gold (51.8 cm³ → −51.8 g buoyancy = 948.2 g apparent weight in water) vs 1,000 g 70/30 crown (64.8 cm³ → −64.8 g buoyancy = 935.2 g in water), tipping by 13.1 g (3:42); 5) inked diagram on period paper showing (1) buoyancy of the 4,000-tonne ship Syracusia displacing 4,000 m³ of seawater vs a sinking solid metal bolt, and (2) Stanford's 2005–2008 synchrotron X-ray fluorescence beam exciting iron atoms in Archimedes' erased 10th-century ink beneath Johannes Myronas's April 1229 prayer text (5:28); 6) animated timeline building ~250 BC · ~240 BC · ~25 BC · April 1229 · 1586 · 1906 & May 2005–2008 alongside an inked hydrostatic pressure diagram showing water pressure increasing with depth (P = ρ g h) so upward pressure on the bottom exceeds downward pressure on the top by F_b = ρ V g (6:43) | 3 or more per long, including the animated timeline |
| `SCALE` | **6** | 1) 13 cubic centimetres of extra volume is less than one tablespoon of water — raising a wide bowl by less than two sheets of paper, yet tipping an underwater scale by 13 full grams (0:34); 2) a water-level rise thinner than two sheets of paper becomes a 13-gram push on an underwater balance (0:52); 3) pure gold is almost twice as dense as silver — so hiding 30% silver inside a one-kilogram crown swells its volume by 13 cubic centimetres, less than a single tablespoon (1:58); 4) instead of trying to spot a 0.18-millimetre water rise swamped by 3 millimetres of surface tension, dunking the balance turns that tiny volume difference into a 13-gram weight difference any scale can feel (3:42); 5) a 4,000-tonne palace ship floats effortlessly because its hollow hull pushes aside 4,000 tonnes of seawater — while a solid one-ounce bolt sinks because it pushes aside only a thimbleful (5:28); 6) whether it is a 1-kilogram crown in a bowl, a 100,000-tonne steel ship in the ocean, or a continent floating on the mantle, every submerged object is lifted by the exact weight of the fluid it pushes aside (6:43) | Every `DATA` number gets a `SCALE:` comparison (`grep -c "SCALE:"` ≥ `DATA:` count) |
| `WHO` | **6** | Archimedes of Syracuse (0:34), King Hiero II (0:34), Galileo Galilei (0:34), Vitruvius (1:28), Johannes Myronas (4:53), Johan Ludvig Heiberg (4:53) | First mention only, role right for the scene's year (4 words or fewer) |
| `WHEN` | **15** | Syracuse ~250 BC (0:00), Florence 1586 (0:00), ~250 BC (0:34), 1586 (0:34), ~250 BC (1:28), ~25 BC (1:28), 1586 (3:08), ~240 BC (4:53), 212 BC (4:53), April 1229 (4:53), 1906 (4:53), May 2005 (5:28), ~250 BC–2008 (6:43), May 1825 (7:45), July 1984 (7:45) | Every spoken date or era; later dates drop onto the timeline |
| `FACT` | **4** | Written 200 years later (1:28); Meniscus hides 0.18 mm rise (3:08); Scraped into a prayer book (4:53); Deeper water pushes up harder (6:43) | 2–4 per long (4 words or fewer per card) |

## Craft checks (*Reference lessons* §1 + *Polish pass*)

- **First-minute timings:** Answer image by 0:03 (Archimedes in Syracuse around 250 BC lowering a balanced golden wreath crown and pure gold block underwater as the silver-doped crown rises and 22-year-old Galileo in 1586 winds brass wire along the balance arm), title question by 0:07, promise by 0:15, stakes by 0:25, first concrete answer & real fact (Archimedes' Principle of upward buoyant force equal to displaced water weight and Galileo's 1586 underwater balance tipping by 13 grams where a 30 cm bowl rises by only 0.18 mm) by 0:34.
- **Explorer limits:** 2 beats total (`[EXPLORER ACTS: once. …]`), at 1:05 (Part 01, outside the first minute) and 6:05 (Part 04 shining an X-ray lantern on the medieval prayer book so Archimedes' erased Greek geometric spirals and balance diagrams glow through the prayers).
- **Chapter cold opens & cliffhanger questions:** Part 01 ends on where the famous story of the overflowing bathtub came from and how 22-year-old Galileo caught the mistake 1,600 years later; Part 02 opens cold on Roman architect Vitruvius writing *De Architectura* around 25 BC (more than 200 years after Archimedes), King Hiero II's votive wreath, gold (19.32 g/cm³) vs silver (10.49 g/cm³) density, and Vitruvius's overflowing-pot assumption, ending on why broke 22-year-old medical dropout Galileo Galilei proved in 1586 that Vitruvius's method could never have worked; Part 03 opens cold on Galileo's 1586 *La Bilancetta*, the 0.18 mm water rise in a 30 cm bowl swamped by a 2–3 mm surface-tension meniscus, Archimedes' Proposition 7 in *On Floating Bodies*, and Galileo's wire-wrapped underwater balance counting coils by fingernail, ending on how Archimedes used that exact law to float a 4,000-tonne ancient palace ship and how his book was nearly erased forever by a 13th-century monk; Part 04 opens cold on the midpoint twist ("Case closed? Wrong." — King Hiero's 4,000-tonne *Syracusia* drained by Archimedes' screw, Johannes Myronas scraping the 10th-century Archimedes parchment into an Easter prayer book in April 1229, Johan Ludvig Heiberg's 1906 magnifying-glass discovery, and Stanford's May 2005 synchrotron X-ray beam making the iron in Archimedes' erased ink glow), ending on why a heavy rock weighs less underwater even when it sinks to the bottom; Part 05 opens cold on the surface-floating misconception, explains depth-pressure buoyancy ($F_b = \rho V g$), and hands off to William Beaumont's May 1825 silk-string stomach window and Barry Marshall drinking *H. pylori* in July 1984 (`032`).
- **Quirky anecdote before the hard idea:** Twenty-two-year-old Galileo winding fine brass wire along the arm of his hydrostatic balance and running his thumbnail across the coils to count the turns by ear; a thirteenth-century monk scraping Archimedes' priceless treatises off goatskin parchment to write an Easter prayer book, only for particle-accelerator X-rays to light up the iron atoms in the erased ink 776 years later.
- **Rivalry / tension:** King Hiero II suspecting his royal goldsmith of theft without allowing a single gold leaf to be scratched; Galileo overturning 1,600 years of uncritical belief in Vitruvius's spilled-bathwater tale.
- **Misconception explained away:** "Many people think buoyancy only works on things that float at the surface, or that deep water crushes a sinking rock downward faster" — explained via water pressure increasing with depth so the upward push on the bottom always beats the downward push on the top by the weight of displaced fluid (Part 05, 6:43).

## For Chief to decide

1. Lock **031 = Archimedes' Bathtub, the Golden Crown & Buoyancy: Archimedes of Syracuse (~250 BC) & Galileo's 1586 Hydrostatic Balance (~250 BC–1586)** and pick the 2-way Test & Compare working title pair:
   - **A (Subject + hook, §1 rule 11):** *Archimedes' Eureka: Why the Overflowing Bathtub Story Is Wrong* (62 chars)
   - **B (Search question, §1 rule 2):** *How Archimedes Actually Proved the Golden Crown Was Fake* (56 chars)
   - **Alt (Search / twist question):** *Why Galileo Proved Archimedes Couldn't Use Spilled Bathwater* (60 chars)
2. Review `archimedes_script_master_v01.md` (92.4/100 PASS), then queue the Gemini facts pass (`--kind facts`) on `SOURCES_v01.md` (rows 1–4) before VO.

## Score (`npm run review:script`)

```text
# archimedes_script_master_v01.md

**Decision:** PASS · **Score:** 92.4 / 100

| Dimension | Score |
|---|---:|
| hook | 9.5 |
| curiosity | 9.5 |
| storytelling | 8 |
| scientificAccuracy | 10 |
| emotion | 9.6 |
| escalation | 8.6 |
| retentionPotential | 9 |
| searchPotential | 9.1 |
| visualOpportunities | 9.5 |
| narrationFlow | 9.6 |

Words: 1670 · Est. min: 11.1 · Chapters: 4

## Cold open excerpt

> Why did young Galileo prove that Archimedes could never have caught a royal thief with spilled bathwater — and how did he really test the golden crown underwater? By the end of this film, you'll see why a crown mixed with silver raises the water in a basin by less than the thickn

## Findings

- **[info] overall:** Structure gates 8/8 — applied +1.05 completeness boost to supporting dimensions.
- **[info] overall:** PASS 92.4/100 — proceed to VO after production checklist.

Pass threshold: 90
```
