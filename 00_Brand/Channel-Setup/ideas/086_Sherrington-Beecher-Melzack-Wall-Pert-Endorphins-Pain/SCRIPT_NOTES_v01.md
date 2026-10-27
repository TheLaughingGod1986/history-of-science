# 086 script v01: notes for review (J0766)

Script: `pain_endorphins_script_master_v01.md` (with `opening_and_outline_v00.md`, `SOURCES_v00.md` and `SOURCES_v01.md`).

**Draft only (J0766, Gemini Argon, 21 Oct 2026).** Built from `086_Sherrington-Beecher-Melzack-Wall-Pert-Endorphins-Pain/opening_and_outline_v00.md` and the neighbour and search evidence in `IDEAS_2026-10-20_J0743.md` (`evidence_2026-10-20_J0743/n_pain_endorphins.md` PASS — 14 education videos ≥ 1M views, with 6 strictly on the neuroscience of pain: **TED-Ed ★ *How does anesthesia work? - Steven Zheng* (`B_tTymvDWXk`, 19.72M)**, **TED-Ed ★ *How Do Pain Relievers Work? - George Zaidan* (`9mcuIc5O-DE`, 4.25M — exact nociceptor & pain pathway match!)**, **TED-Ed ★ *How do animals experience pain? - Robyn J. Crook* (`5j9Syov0AAw`, 3.92M — exact nociception match!)**, **TED-Ed ★ *How does your brain respond to pain? - Karen D. Davis* (`I7wfDenj6CQ`, 2.96M — exact pain modulation & brain analgesia match!)**, **TED-Ed ★ *What does appendix pain feel like? - David R. Flum* (`8CUEPNcGtWs`, 2.72M)**, and **TED-Ed ★ *The mysterious science of pain - Joshua W. Pate* (`eakyDiXX6Uc`, 2.06M — exact subject match!)**, alongside `public_search.md` & `public_search_titles.md` showing `"how does pain work"` is an exact YouTube autocomplete match (`yes`), all 5 top GB search results for `"ronald melzack patrick wall gate control theory pain"` under 404k views, and 3 of the top 5 GB slots for *Why Rubbing a Stubbed Toe Stops Pain and How Your Brain Makes Its Own Morphine* under 1,500 views). The topic isn't locked yet: Chief locks `086` and the working title pair first, then reviews/signs off this script and queues the Gemini facts pass (`--kind facts`) on `SOURCES_v01.md` (rows 1–4) before VO.

Structure (*Reference lessons* §1, scripts from 011 on): every chapter opens cold and ends on a question the next one answers; René Descartes's 1664 bell-rope myth, Charles Sherrington's 1906 discovery of `nociceptors` (with Erlanger & Gasser's fast `A-delta` and slow `C` fibres), and Henry Knowles Beecher's February 1944 Anzio beachhead pain paradox and 1955 `placebo effect` land in Part 02; the midpoint twist ("Case closed — pain signals travel up a dedicated wire straight from your injured skin to a pain centre in your brain, and nothing in your skin or spine can stop them! Wrong!") with Ronald Melzack & Patrick Wall's 19 November 1965 `Gate Control Theory of Pain` and 1967 `TENS` lands in Part 03; Candace Pert & Solomon Snyder's 9 March 1973 discovery of `opioid receptors` and John Hughes & Hans Kosterlitz's 18 December 1975 isolation of `enkephalins` and `endorphins` land in Part 04; the ending hands off directly to `087` (*Why Can't Plain Water Wash Off Grease — and How Did a German Woman at Her Kitchen Sink Unlock How Soap Rips Apart Dirt and Viruses?*), with no goodbye and no subscribe ask. Five VO parts, matching 009–085.

## Marker count (v01)

Run on `pain_endorphins_script_master_v01.md`: `grep -o "DATA:" … | wc -l`, and the same for each marker.

| Marker | Count | Where | Rule |
|---|---:|---|---|
| `DATA` | **6** | 1) inked Melzack & Wall (1965) nerve conduction velocity comparison (`A-beta 35–75 m/s` vs `A-delta 5–30 m/s` vs `C-fibre 0.5–2 m/s`) & spinal dorsal horn Gate Control circuit (0:34); 2) inked Beecher (1946) Anzio battlefield (`~25%`) vs civilian surgical (`>80%`) morphine demand & Pert/Snyder/Kosterlitz (1973–1975) opioid receptor / endorphin lock-and-key chart (0:52); 3) inked Sherrington (1906) & Erlanger/Gasser two-wave nociceptor conduction chart + Beecher (1946 & 1955) Anzio & 35% placebo analgesia chart (1:58); 4) inked Melzack & Wall (1965 *Science*) dorsal horn Gate Control circuit diagram (3:47); 5) inked Pert & Snyder (1973 *Science*) `[³H]naloxone` opioid receptor binding & Hughes/Kosterlitz (1975 *Nature*) Met/Leu-enkephalin & beta-endorphin chart (5:32); 6) animated timeline 1906–1975 (6:48) | ≥ 3 per long, including the timeline |
| `SCALE` | **6** | 1) touch nerves race up to your spine at 75 m/s — as fast as an express train — while throbbing pain nerves crawl at 1 m/s, a walking pace, so rubbing a bumped shin lets touch signals slam the spinal gate shut first (0:34); 2) molecule for molecule, your brain's own beta-endorphin is 18–30× more potent than hospital morphine (0:52); 3) if you are six feet tall and stub your toe, the sharp A-delta flash reaches your brain in <0.1 s, while the slow C-fibre ache takes nearly 2 full seconds to climb the same leg (1:58); 4) the dorsal horn works like a nightclub bouncer at a narrow doorway — slow pain signals open the door, but a crowd of fast touch signals from rubbing your toe bolts it shut (3:47); 5) Kosterlitz and Hughes hauled buckets of frozen pig brains from a Scottish slaughterhouse for two years to isolate a pinch of enkephalin crystals (5:32); 6) from a muddy medical tent on an Italian beach to a spinal gate at MIT and slaughterhouse pig brains in Scotland (6:48) | `SCALE:` on every `DATA:` (`grep -c` matches) |
| `WHO` | **12** | Charles Scott Sherrington (1857–1952) — British neurophysiologist; Henry Knowles Beecher (1904–1976) — American anaesthesiologist and researcher; Ronald Melzack (1929–2019) — Canadian psychologist; Patrick David Wall (1925–2001) — British neuroscientist; Candace Beebe Pert (1946–2013) — American neuroscientist and pharmacologist; Solomon Halbert Snyder (born 1938) — American neuroscientist; John Hughes (born 1942) — British pharmacologist; Hans Walter Kosterlitz (1903–1996) — German-British pharmacologist; René Descartes (1596–1650) — French philosopher and mathematician; Herbert Spencer Gasser (1888–1963) — American physiologist; Joseph Erlanger (1874–1965) — American physiologist; Friedrich Wilhelm Sertürner (1783–1841) — German pharmacist and chemist | Every named person at first mention, role right for the scene's year |
| `WHEN` | **24** | Anzio, Italy, February 1944 (0:00); 1906, 1944, 1955, 19 November 1965, 9 March 1973, 18 December 1975 (0:34); 1664, 1906, February 1944, 1946, 1955 (1:28); 19 November 1965, 1967 (3:13); 1804, 22 September 1972, 9 March 1973, 18 December 1975, 1978 (4:58); 1906–1975 timeline marker (6:48); 1823, 12 March 1891, 1913, 1917 (7:45) | Every spoken date or era |
| `FACT` | **3** | `75% refused Anzio morphine` (1:28); `Touch slams pain gate` (3:13); `Brain makes own morphine` (4:58) | 2–4 per long, ≤ 4 words per card |

## Craft lessons check (*Reference lessons* §1)

- **Cold opens & cliffhanger hand-offs:** Part 01 opens cold on why you instinctively rub a stubbed toe and how wounded soldiers at Anzio in February 1944 felt almost no pain, and ends on how Beecher's Anzio observations shattered Descartes's 300-year bell-rope myth; Part 02 opens cold on Descartes (1664), Sherrington's `nociceptors` (1906), and Beecher's 215 Anzio soldiers (1944) and `placebo effect` (1955), and ends on how Melzack and Wall on 19 November 1965 found the physical pain switch in the spinal cord; Part 03 opens cold on the midpoint twist ("Case closed — pain signals travel up a dedicated wire straight from your injured skin to a pain centre in your brain, and nothing in your skin or spine can stop them! Wrong!"), explains Melzack & Wall's 1965 `Gate Control Theory of Pain` and 1967 `TENS`, and ends on why human brain cells have keyholes for opium poppy juice; Part 04 opens cold on Sertürner (1804), Pert & Snyder's 1973 `opioid receptors`, and Hughes & Kosterlitz's 1975 `enkephalins / endorphins`, and ends on why washing a cut with plain water can't remove grease whereas soap destroys grease and viruses; Part 05 opens cold on the spinal gate and the pharmacy in your head, and hands off to Chevreul (1823), Agnes Pockels (1891), McBain (1913), and Langmuir (1917) (`087`).
- **Quirky anecdote before the hard idea:** Rubbing a stubbed toe in the dark and feeling the sharp flash 1.9 seconds before the slow ache; wide-awake Anzio soldiers waving away morphine; 72-year-old Hans Kosterlitz and John Hughes hauling buckets of frozen pig brains from a Scottish slaughterhouse to find the brain's own morphine!
- **Rivalry / tension:** Descartes's 300-year fixed bell-rope dogma ("specificity theory") vs Beecher's Anzio paradox & Melzack and Wall's 1965 spinal gate; international race to find the endogenous opioid ligand (`Pert & Snyder` vs `Hughes & Kosterlitz`).
- **Misconception explained away:** "Is pain a fixed one-way wire where a bigger injury always causes bigger pain, and does rubbing a bump just distract you?" — refuted by Beecher, Melzack & Wall, and Pert/Snyder/Hughes/Kosterlitz (Parts 01–04).

## For Chief to decide

1. Lock **086 = Why Do We Feel Pain, Why Does Rubbing a Stubbed Toe Make It Hurt Less — and How Did Wounded Soldiers on an Italian Beach Reveal the Brain's Own Morphine (`Pain, Nociceptors, Gate Control Theory & Endorphins`)? Charles Sherrington's 1906 Discovery of `Nociceptors`, Henry Knowles Beecher's 1944 Anzio Beachhead Pain Paradox & 1955 `Placebo Effect`, Ronald Melzack & Patrick Wall's 19 November 1965 `Gate Control Theory of Pain`, and Candace Pert, Solomon Snyder, John Hughes & Hans Kosterlitz's 1973–1975 Discovery of `Opioid Receptors` & `Endorphins` (1664–1978)** and pick the 2-way Test & Compare working title pair:
   - **A (Subject + hook, §1 rule 11):** *Endorphins: How Your Brain Makes Its Own Morphine* (49 chars)
   - **B (Search question, §1 rule 2):** *Why Rubbing a Stubbed Toe Stops Pain and How Your Brain Makes Its Own Morphine* (78 chars)
   - **Alt (Search / twist question):** *Why Rubbing a Bump Stops Pain and How Soldiers Unlocked Endorphins* (66 chars)
2. Review `pain_endorphins_script_master_v01.md` (90.8/100 PASS), then queue the Gemini facts pass (`--kind facts`) on `SOURCES_v01.md` (rows 1–4) before VO.

## Score (`npm run review:script`)

```text
# pain_endorphins_script_master_v01.md

**Decision:** PASS · **Score:** 90.8 / 100

| Dimension | Score |
|---|---:|
| hook | 9.5 |
| curiosity | 9.5 |
| storytelling | 8 |
| scientificAccuracy | 10 |
| emotion | 9.6 |
| escalation | 7 |
| retentionPotential | 9 |
| searchPotential | 9.1 |
| visualOpportunities | 9.5 |
| narrationFlow | 9.6 |

Words: 1654 · Est. min: 11 · Chapters: 4

## Cold open excerpt

> Why, the very instant you stub your toe against a table leg , do you automatically grab your foot and rub the skin — and why does rubbing a bump actually make the pain fade ? Even stranger: how did wounded soldiers on a shell-torn Italian beach in February nineteen forty-four fee

## Findings

- **[info] overall:** Structure gates 8/8 — applied +1.05 completeness boost to supporting dimensions.
- **[info] overall:** PASS 90.8/100 — proceed to VO after production checklist.

Pass threshold: 90
```
