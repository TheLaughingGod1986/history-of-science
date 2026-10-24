# 081 script v01: notes for review (J0736)

Script: `plant_tropisms_script_master_v01.md` (with `opening_and_outline_v00.md`, `SOURCES_v00.md` and `SOURCES_v01.md`).

**Draft only (J0736, Gemini Argon, 20 Oct 2026).** Built from `081_Darwin-Went-Neljubow-Gane-Plant-Tropisms-Auxin/opening_and_outline_v00.md` and the neighbour and search evidence in `IDEAS_2026-10-20_J0728.md` (`evidence_2026-10-20_J0728/n_plant_hormones_auxin.md` PASS — 6 education videos ≥ 1M views: **SciShow Kids *How Does A Seed Become A Plant?* (`tkFPyue5X3Q`, 6.20M)**, **TED-Ed ★ *How Mendel's pea plants helped us understand genetics* (`Mehz7tCxjSE`, 5.03M)**, **TED-Ed ★ *The amazing ways plants defend themselves - Valentin Hammoudi* (`Hja0SLs2kus`, 4.44M)**, **TED ★ *Electrical experiments with plants that count and communicate | Greg Gage* (`pvBlSFVmoaw`, 3.30M — exact plant sensing & movement match!)**, **TED-Ed ★ *The wild world of carnivorous plants* (`ee7muQ_qKU0`, 2.36M)**, and **TED-Ed ★ *How tall can a tree grow? - Valentin Hammoudi* (`vvtPJKWUb2g`, 1.41M)**, plus **Cognito *GCSE Biology - Plant Hormones - Tropisms & Auxins* (`rKHIfsHX1aA`, 687.3k — exact Darwin & Went auxin phototropism match!)** and **TED-Ed ★ *How plants tell time - Dasha Savage* (`3jIW5wW2WC0`, 366.5k)**, alongside `public_search.md` & `public_search_titles.md` showing `"phototropism"` is an exact YouTube autocomplete match (`yes`), all 5 top GB search results for `"charles darwin frits went auxin phototropism"` under 688k views, and all 3 top GB slots for *How Darwin's Blindfolded Grass Tip Unlocked Why Plants Grow Toward Light* under 16k views). The topic isn't locked yet: Chief locks `081` and the working title pair first, then reviews/signs off this script and queues the Gemini facts pass (`--kind facts`) on `SOURCES_v01.md` (rows 1–4) before VO.

Structure (*Reference lessons* §1, scripts from 011 on): every chapter opens cold and ends on a question the next one answers; Charles & Francis Darwin's November 1880 blindfolded canary-grass coleoptile tips (`phototropism`) and Gottlieb Haberlandt & Bohumil Němec's 1900 falling-starch `statoliths` (`gravitropism`) land in Part 02; the midpoint twist ("Case closed — if a plant tip sends a message down the stem, it must be an electrical nerve impulse travelling through living tissue! Wrong! In nineteen thirteen in Copenhagen and at three o'clock in the morning on seventeen April nineteen twenty-six in Utrecht, scientists sliced the tip completely off, replaced it with a lifeless cube of jelly, and watched the headless plant bend in the dark!" — where Peter Boysen-Jensen, Árpád Paál, and Frits Warmolt Went isolated `auxin` in agar jelly) lands in Part 03; Dmitry Neljubow's 1901 leaking streetlamp gas and Richard Gane's 29 December 1934 56-kg apple proof of `ethylene` ripening gas land in Part 04; the ending hands off directly to `082` (*How Does a Cut Stop Bleeding Without Clotting All the Blood in Your Veins — and How Did Spoiled Clover Hay Turn Rat Poison Into a Life-Saving Blood Thinner?*), with no goodbye and no subscribe ask. Five VO parts, matching 009–080.

## Marker count (v01)

Run on `plant_tropisms_script_master_v01.md`: `grep -o "DATA:" … | wc -l`, and the same for each marker.

| Marker | Count | Where | Rule |
|---|---:|---|---|
| `DATA` | **6** | 1) inked Darwin (1880) & Frits Went (17 Apr 1926) coleoptile phototropism & agar-block curvature bioassay chart (0:34); 2) inked Frits Went (1926/1928) *Avena* curvature angle chart (0:52); 3) inked Charles & Francis Darwin (Nov 1880 *The Power of Movement in Plants*) 5-condition coleoptile tip experiment + Haberlandt & Němec (1900) root-cap statolith sedimentation diagram (1:58); 4) inked Boysen-Jensen (1913), Árpád Paál (1919) & Frits Went (17 Apr 1926) Cholodny–Went Auxin Redistribution diagram (3:47); 5) inked Dmitry Neljubow (1901) `0.1 ppm` ethylene triple-response threshold & Richard Gane (29 Dec 1934 *Nature*) climacteric apple ethylene burst chart (5:32); 6) animated timeline 1806–1934 (6:48) | ≥ 3 per long, including the timeline |
| `SCALE` | **6** | 1) shaded stem cells inflating with water and stretching longer like the outer rail of a curving train track (0:34); 2) one ten-millionth of a gram of auxin in a 2-mm cube of jelly bending thousands of oat shoots in darkness (0:52); 3) a 1.5-mm tin-foil cap on a grass tip as a blindfold on a runner's eyes while leaving their legs free (1:58); 4) auxin acting as an accelerator on the shady side of stems and a brake on the bottom side of roots (3:47); 5) one ripe banana in a paper bag broadcasting ethylene like a chemical radio transmitter (5:32); 6) tin-foil helmets at Down House to a 3 a.m. Utrecht jelly cube to 56 kg of Cambridge apples (6:48) | `SCALE:` on every `DATA:` (`grep -c` matches) |
| `WHO` | **12** | Charles Darwin (1809–1882) — English naturalist; Francis Darwin (1848–1925) — English botanist; Gottlieb Haberlandt (1854–1945) — Austrian botanist; Bohumil Němec (1873–1966) — Czech botanist; Peter Boysen-Jensen (1883–1959) — Danish plant physiologist; Frits Warmolt Went (1903–1990) — Dutch-American botanist; Dmitry Nikolayevich Neljubow (1876–1926) — Russian plant physiologist; Richard Gane (1904–1981) — British plant physiologist; Thomas Andrew Knight (1759–1838) — British horticulturist and botanist; Árpád Paál (1889–1943) — Hungarian botanist; Kenneth Vivian Thimann (1904–1997) — British-American plant physiologist; Frank Earl Denny (1883–1964) — American plant physiologist | Every named person at first mention, role right for the scene's year |
| `WHEN` | **23** | Down House, Kent, November 1880 (0:00); November 1880, 1900, 1901, 1913, 17 April 1926, 1934 (0:34); 1806, November 1880, 1900 (1:28); 1910, 1913, 1919, 17 April 1926, 1927 (3:13); 1901, 1924, 29 December 1934 (4:58); 1880–1934 timeline marker (6:48); 1882, 1905, 1916, February 1933 (7:45) | Every spoken date or era |
| `FACT` | **3** | `2mm foil cap blinded grass` (1:28); `Shady cells stretch longer` (3:13); `Apples breathe ripening gas` (4:58) | 2–4 per long, ≤ 4 words per card |

## Craft lessons check (*Reference lessons* §1)

- **Cold opens & cliffhanger hand-offs:** Part 01 opens cold on how a windowsill plant sees sunlight (`phototropism`), feels gravity (`gravitropism`), and ripens fruit (`ethylene`) without eyes or a brain, and ends on why Charles and Francis Darwin fitted tiny tin-foil helmets onto grass seedlings in November 1880; Part 02 opens cold on the Darwins' 1880 Down House tin-foil cap experiment and Haberlandt & Němec's 1900 falling-starch `statoliths`, and ends on how Boysen-Jensen and Frits Went proved what Darwin's invisible messenger really was; Part 03 opens cold on the midpoint twist ("Case closed — if a plant tip sends a message down the stem, it must be an electrical nerve impulse travelling through living tissue! Wrong!"), tells the story of Boysen-Jensen's gelatin/mica tests and Went's 3:00 a.m. 17 April 1926 agar-jelly isolation of `auxin`, and ends on how one ripe apple or banana ripens every fruit around it through thin air; Part 04 opens cold on leaking coal-gas streetlamp pipes in European cities and Dmitry Neljubow's 1901 St Petersburg pea shoots, explains Frank Denny's 1924 lemon sheds and Richard Gane's 1934 56-kg apple proof of `ethylene`, and ends on how your own bloodstream turns liquid blood into a solid clot in seconds and how a milk can of cow's blood in a 1933 Wisconsin blizzard turned rat poison (`Warfarin`) into medicine; Part 05 opens cold on the chemical sensory world of plants, and hands off to Giulio Bizzozero (1882), Paul Morawitz (1905), Jay McLean (1916), Henrik Dam (1935), and Karl Paul Link (Feb 1933–1955) (`082`).
- **Quirky anecdote before the hard idea:** 71-year-old Charles Darwin crafting microscopic tin-foil top hats for grass shoots; 23-year-old Frits Went sneaking into his father's lab at night and waking his parents at 3:00 a.m. shouting *"Father, come and see, I have got it!"*; leaking streetlamp pipes stripping trees bare and kerosene heaters yellowing lemons!
- **Rivalry / tension:** Julius von Sachs mocking the Darwins' tip-signal discovery vs Boysen-Jensen and Frits Went's chemical proof of `auxin`.
- **Misconception explained away:** "Does sunlight warm or shrink the sunny side of a stem to make it bend?" — refuted by Darwin's 1880 tin-foil cap and Went's 1926 `auxin` proof that light drives `auxin` to the *shaded* side so shaded cells stretch longer (Parts 01–03).

## For Chief to decide

1. Lock **081 = How Do Plants See Light, Feel Gravity & Ripen Fruit Without Eyes, Nerves or Brains (`Plant Tropisms, Charles Darwin's 1880 Blindfolded Grass Tip, Frits Went's 1926 Auxin & Ethylene Gas`)? Charles & Francis Darwin's November 1880 Canary-Grass Tip Blindfold Experiment (`Phototropism`), Gottlieb Haberlandt & Bohumil Němec's 1900 Falling-Starch `Statoliths` (`Gravitropism`), Frits Warmolt Went's 17 April 1926 3:00 a.m. Agar-Jelly Isolation of `Auxin`, and Dmitry Neljubow & Richard Gane's 1901–1934 Discovery of `Ethylene` Ripening Gas (1880–1934)** and pick the 2-way Test & Compare working title pair:
   - **A (Subject + hook, §1 rule 11):** *Plant Hormones: How Darwin's Blindfolded Grass Sees Light* (57 chars)
   - **B (Search question, §1 rule 2):** *How Darwin's Blindfolded Grass Tip Unlocked Why Plants Grow Toward Light* (72 chars)
   - **Alt (Search / twist question):** *How Plants See Light, Feel Gravity and Ripen Fruit Without a Brain* (66 chars)
2. Review `plant_tropisms_script_master_v01.md` (91.0/100 PASS), then queue the Gemini facts pass (`--kind facts`) on `SOURCES_v01.md` (rows 1–4) before VO.

## Score (`npm run review:script`)

```text
# plant_tropisms_script_master_v01.md

**Decision:** PASS · **Score:** 91 / 100

| Dimension | Score |
|---|---:|
| hook | 9.5 |
| curiosity | 8.3 |
| storytelling | 8 |
| scientificAccuracy | 10 |
| emotion | 9.6 |
| escalation | 8.4 |
| retentionPotential | 9 |
| searchPotential | 9.1 |
| visualOpportunities | 9.5 |
| narrationFlow | 9.6 |

Words: 1654 · Est. min: 11 · Chapters: 4

## Cold open excerpt

> How does a green plant on your windowsill see sunlight ( phototropism ) without eyes? Right now, a houseplant bends its stem toward the window, feels which way is down ( gravitropism ) in pitch darkness, and whispers through the air to ripen every piece of fruit in a bowl ( ethyl

## Findings

- **[info] overall:** Structure gates 8/8 — applied +1.05 completeness boost to supporting dimensions.
- **[info] overall:** PASS 91/100 — proceed to VO after production checklist.

Pass threshold: 90
```
