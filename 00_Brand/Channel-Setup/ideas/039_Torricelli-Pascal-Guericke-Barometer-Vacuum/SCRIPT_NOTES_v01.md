# 039 script v01: notes for review (J0523)

Script: `barometer_script_master_v01.md` (with `opening_and_outline_v00.md`, `SOURCES_v00.md` and `SOURCES_v01.md`).

**Draft only (J0523, Gemini Argon, 18 Oct 2026).** Built from `039_Torricelli-Pascal-Guericke-Barometer-Vacuum/opening_and_outline_v00.md` and the neighbour and search evidence in `IDEAS_2026-10-18_J0515.md` (`evidence_2026-10-18_J0515/n_barometer.md` PASS — 3 TED-Ed videos ≥ 1M views: **TED-Ed ★ *How blood pressure works - Wilfred Manzano* (`Ab9OZsDECZw`, 17.98M)**, **TED-Ed ★ *The history of the barometer (and how it works) - Asaf Bar-Yosef* (`EkDhlzA-lwI`, 2.43M — exact Torricelli & Pascal barometer match!)**, and **TED-Ed ★ *Is it possible to create a perfect vacuum? - Rolf Landua and Anais Rassat* (`_rJOSDgDG0A`, 1.11M)**, plus **The Action Lab (`1.33M` on Magdeburg hemispheres)**, **TED-Ed ★ *The effects of underwater pressure on the body* (`_cj8AtODiHc`, 670.7k)**, and **Cognito *GCSE Physics - Atmospheric Pressure* (`s8C2RktZtbM`, 344.5k)**, alongside `public_search.md` showing 4 of the top 5 GB search results for `"evangelista torricelli barometer vacuum"` under 62k views and all 5 top GB slots for *How a Tube of Mercury and Sixteen Horses Proved Air Has Weight* under 643k views). The topic isn't locked yet: Chief locks `039` and the working title pair first, then reviews/signs off this script and queues the Gemini facts pass (`--kind facts`) on `SOURCES_v01.md` (rows 1–4) before VO.

Structure (*Reference lessons* §1, scripts from 011 on): every chapter opens cold and ends on a question the next one answers; the midpoint twist ("Case closed? Not until Pascal thought of the ultimate experiment!" — after testing 46-foot tubes of water and red wine lashed to a ship's mast in Rouen in late 1646, Blaise Pascal had his brother-in-law Florin Périer carry a mercury barometer 1,000 metres up the volcanic mountain Puy-de-Dôme on 19 September 1648, watching the mercury fall by 84 millimetres as the weight of overlying air decreased) lands in Part 03; Otto von Guericke's 8 May 1654 16-horse Magdeburg hemispheres demonstration at Regensburg and Robert Boyle & Robert Hooke's 1660–1662 evacuated glass-globe watch and J-tube experiments land in Part 04; the popular misconception ("Most people think the first steam engines worked by using high-pressure steam to push a heavy piston") is raised and explained away in Part 05 via Denis Papin (1690) and Thomas Newcomen's (1712) atmospheric vacuum engine, where condensing steam with cold water created a vacuum so outside air weight slammed the piston down with >5 tonnes of force; the ending hands off directly to `040` (*How Old Is the Earth? Radiometric Dating, Lead-Poisoned Gasoline & Clair Patterson's Ultra-Clean Room*), with no goodbye and no subscribe ask. Five VO parts, matching 009–038.

## Marker count (v01)

Run on `barometer_script_master_v01.md`: `grep -o "DATA:" … | wc -l`, and the same for each marker.

| Marker | Count | Where | Rule |
|---|---:|---|---|
| `DATA` | **6** | 1) inked height-and-density balance chart on period paper comparing 10.3 metres (32 feet) of water (density 1.0 g/cm³) against 760 millimetres (30 inches) of liquid mercury (density 13.6 g/cm³), both exerting 101.3 kPa (14.7 lb/in²) at sea level (0:34); 2) inked atmospheric-load scale bar showing 14.7 pounds per square inch (1.03 kg/cm² = 101,325 Pa) summing to ~10,000 kg (10 metric tonnes) over the ~1.7 m² surface area of a human body (0:52); 3) inked pump-and-barometer diagram on period paper showing a Florentine suction pump failing above 18 braccia (32 feet / 10.3 m of water) beside Torricelli & Viviani's 1644 mercury tube stopping at 1.25 braccia (30 inches / 760 mm of mercury) with a vacuum above (1:58); 4) inked altitude-vs-pressure chart on period paper from Florin Périer's 19 September 1648 Puy-de-Dôme climb showing mercury falling from 711 mm (26 pouces 3.5 lignes) at the Clermont monastery garden (~395 m elevation) to 627 mm (23 pouces 2 lignes) at the Puy-de-Dôme summit (1,465 m, a drop of 84 mm across ~1,000 m of altitude) (3:42); 5) inked force-and-volume diagram on period paper showing Otto von Guericke's 50 cm Magdeburg hemispheres clamped by ~20,000 N (~2 tonnes) of outside air pressure alongside Robert Boyle's 1662 J-tube showing gas volume halving when mercury pressure doubles (29.75 → 59.5 inches Hg, P × V = constant) (5:28); 6) animated timeline building 1638 · Jun 1644 · 19 Sep 1648 · 8 May 1654 · 1660–1662 · 1712 alongside Thomas Newcomen's 1712 atmospheric engine cylinder (21-inch bore, 14.7 psi outside air driving the piston down with >5 tonnes of force at 12 strokes per minute) (6:43) | 3 or more per long, including the animated timeline |
| `SCALE` | **6** | 1) because liquid mercury is nearly fourteen times heavier than water, a thirty-inch tube of mercury on your desk weighs the exact same per square inch as a thirty-two-foot tower of water three storeys high (0:34); 2) the air pressing inward on your skin right now weighs around ten tonnes — as heavy as a double-decker London bus, balanced only because the fluids inside your body push back out with the exact same force (0:52); 3) if you tried to sip water through a vertical straw thirty-five feet tall, even the strongest vacuum pump on Earth could never lift the water to your lips (1:58); 4) climbing just one kilometre up the mountain left roughly ten percent of Earth's atmosphere below their boots — dropping the mercury column by the length of a human thumb (3:42); 5) on a fifty-centimetre copper sphere, the ordinary air of a spring afternoon clamps the two halves together with two tonnes of force — the weight of a full-grown rhinoceros sitting on the seam (5:28); 6) when cold water condensed the steam inside Newcomen's cylinder, the outside atmosphere slammed the piston down with over five tonnes of force twelve times a minute (6:43) | Every `DATA` number gets a `SCALE:` comparison (`grep -c "SCALE:"` ≥ `DATA:` count) |
| `WHO` | **7** | Evangelista Torricelli (0:34), Blaise Pascal (0:34), Otto von Guericke (0:34), Vincenzo Viviani (1:28), Florin Périer (3:08), Robert Boyle (4:53), Thomas Newcomen (6:43) | First mention only, role right for the scene's year (4 words or fewer) |
| `WHEN` | **21** | Regensburg 8 May 1654 (0:00), Florence 1644 (0:00), Florence 11 June 1644 (0:21), 1643 (0:34), 19 September 1648 (0:34), 8 May 1654 (0:34), 1638 (1:28), 11 June 1644 (1:28), 1646 (3:08), 15 November 1647 (3:08), 19 September 1648 (3:08), 1650 (4:53), 8 May 1654 (4:53), 1660 (4:53), 1662 (4:53), 1690 (6:43), 1712 (6:43), 1638–1712 (6:43), 20 May 1904 (7:45), 1953 (7:45), 1965 (7:45) | Every spoken date or era; later dates drop onto the timeline |
| `FACT` | **4** | Straws push, never suck (1:28); Tested with a 46-foot wine tube (3:08); 16 horses couldn't open it (4:53); Steam engines ran on air weight (6:43) | 2–4 per long (4 words or fewer per card) |

## Craft checks (*Reference lessons* §1 + *Polish pass*)

- **First-minute timings:** Answer image by 0:03 (Otto von Guericke's 8 May 1654 16-horse Magdeburg hemispheres in Regensburg dissolving to Evangelista Torricelli and Vincenzo Viviani inverting a 4-foot glass tube of mercury in Florence in 1644), title question by 0:07, promise by 0:15, stakes by 0:25, first concrete answer & real fact (Torricelli proving in 1643–1644 that outside air weight balances 32 feet of water or 30 inches of mercury, proved on Puy-de-Dôme on 19 September 1648 and before 16 horses on 8 May 1654) by 0:34.
- **Explorer limits:** 2 beats total (`[EXPLORER ACTS: once. …]`), at 1:05 (Part 01, outside the first minute) and 6:05 (Part 04 cranking a miniature vacuum pump as a pocket watch inside a glass bell jar fades to total silence).
- **Chapter cold opens & cliffhanger questions:** Part 01 ends on why scholars for two thousand years insisted empty space was impossible and how Florentine well-diggers broke Aristotle's law; Part 02 opens cold on how a drinking straw really works, Galileo's 1638 18-braccia (32-foot) suction-pump limit, and Torricelli and Viviani's 1643–1644 30-inch mercury barometer and vacuum (*"We live submerged at the bottom of an ocean of the element air"*), ending on why 23-year-old Blaise Pascal built a 46-foot glass tube of red wine and sent a barometer up a volcano; Part 03 opens cold on the midpoint twist ("Case closed? Not until Pascal thought of the ultimate experiment!" — Pascal's 1646 Rouen 46-foot red-wine tube and Florin Périer's 19 September 1648 1,000-metre ascent of Puy-de-Dôme where the mercury dropped by 84 mm), ending on what happens when you pump the air out of a hollow copper sphere and hitch 16 warhorses to pull it open; Part 04 opens cold on Otto von Guericke's 1650 vacuum pump crushing wooden barrels, his 8 May 1654 Regensburg 16-horse Magdeburg hemispheres demonstration before Emperor Ferdinand III, and Robert Boyle & Robert Hooke's 1660–1662 silent watch in a vacuum and Boyle's Law, ending on how engineers turned the two-tonne crush of the atmosphere into the steam engine; Part 05 opens cold on the steam-engine misconception, explains Denis Papin (1690) and Thomas Newcomen's (1712) atmospheric vacuum engine, and hands off to Ernest Rutherford's 20 May 1904 Royal Institution pitchblende lecture and Clair Patterson's 1953 ultra-clean room and 1965 Greenland ice cores (`040`).
- **Quirky anecdote before the hard idea:** Florentine well-diggers baffling Galileo with pumps that stopped at 32 feet; Blaise Pascal lashing 46-foot glass tubes of red wine to a ship's mast in Rouen; Otto von Guericke's evacuated wooden beer barrels smashing inward before he cast his copper hemispheres.
- **Rivalry / tension:** Aristotelian *horror vacui* professors claiming "spirits" inside the glass pushed the column down vs Pascal's red-wine tube and Puy-de-Dôme mountain ascent.
- **Misconception explained away:** "Most people think the first steam engines worked by using high-pressure steam to push a heavy piston" — explained via Thomas Newcomen's 1712 atmospheric vacuum engine condensing low-pressure steam with cold water so outside air weight slammed the piston down with >5 tonnes of force (Part 05, 6:43).

## For Chief to decide

1. Lock **039 = Atmospheric Pressure, the Barometer & the Vacuum — Evangelista Torricelli's 1643 Mercury Tube, Blaise Pascal's 19 September 1648 Puy-de-Dôme Mountain Climb & Otto von Guericke's 8 May 1654 16-Horse Magdeburg Hemispheres (1638–1712)** and pick the 2-way Test & Compare working title pair:
   - **A (Subject + hook, §1 rule 11):** *Atmospheric Pressure: Why 16 Horses Couldn't Pull Two Bowls Apart* (65 chars)
   - **B (Search question, §1 rule 2):** *How a Tube of Mercury and Sixteen Horses Proved Air Has Weight* (62 chars)
   - **Alt (Search / twist question):** *Why Can't Any Suction Pump on Earth Lift Water Past 32 Feet?* (60 chars)
2. Review `barometer_script_master_v01.md` (93.8/100 PASS), then queue the Gemini facts pass (`--kind facts`) on `SOURCES_v01.md` (rows 1–4) before VO.

## Score (`npm run review:script`)

```text
# barometer_script_master_v01.md

**Decision:** PASS · **Score:** 93.8 / 100

| Dimension | Score |
|---|---:|
| hook | 9.5 |
| curiosity | 9.5 |
| storytelling | 8 |
| scientificAccuracy | 10 |
| emotion | 9.6 |
| escalation | 10 |
| retentionPotential | 9 |
| searchPotential | 9.1 |
| visualOpportunities | 9.5 |
| narrationFlow | 9.6 |

Words: 1694 · Est. min: 11.3 · Chapters: 4

## Cold open excerpt

> Why couldn't any suction pump in Renaissance Florence ever lift water higher than thirty-two feet? And why couldn't sixteen straining warhorses in Germany pull two unbolted copper bowls apart until a single tiny valve was turned? By the end of this film, you'll see why a two-thou

## Findings

- **[info] overall:** Structure gates 8/8 — applied +1.05 completeness boost to supporting dimensions.
- **[info] overall:** PASS 93.8/100 — proceed to VO after production checklist.

Pass threshold: 90
```
