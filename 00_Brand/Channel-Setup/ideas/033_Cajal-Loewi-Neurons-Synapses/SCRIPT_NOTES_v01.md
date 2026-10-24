# 033 script v01: notes for review (J0493)

Script: `neurons_script_master_v01.md` (with `opening_and_outline_v00.md`, `SOURCES_v00.md` and `SOURCES_v01.md`).

**Draft only (J0493, Gemini Argon, 17 Oct 2026).** Built from `033_Cajal-Loewi-Neurons-Synapses/opening_and_outline_v00.md` and the neighbour and search evidence in `IDEAS_2026-10-17_J0485.md` (`evidence_2026-10-17_J0485/n_neurons.md` & `n_neurons_synapse.md` PASS — 5 strictly on-topic neuron/synapse/nervous-system videos ≥ 1M views: **CrashCourse *The Nervous System, Part 1* (`qPix_X-9t7E`, 11.16M)**, **CrashCourse *The Nervous System, Part 2 - Action! Potential!* (`OZG8M_ldA1M`, 8.17M)**, **CrashCourse *Central Nervous System* (`q8NtmDrb_qo`, 5.49M)**, **CrashCourse *The Nervous System, Part 3 - Synapses!* (`VitFvNvRIIY`, 5.42M — exact Otto Loewi frog-heart match)**, and **Amoeba Sisters *Nervous System* (`RNLceVI8jcc`, 4.17M)**, plus **30+ TED-Ed/TED brain videos ≥ 1M led by `xyQY8a-ng6g` `21.78M` and `lEXBxijQREo` `19.25M`**, alongside `public_search.md` showing `"otto loewi frog heart"` triggering autocomplete with all 5 top GB slots under 16k views and `"santiago ramon y cajal neuron"` triggering autocomplete with all 5 top GB slots under 48k views). The topic isn't locked yet: Chief locks `033` and the working title pair first, then reviews/signs off this script and queues the Gemini facts pass (`--kind facts`) on `SOURCES_v01.md` (rows 1–4) before VO.

Structure (*Reference lessons* §1, scripts from 011 on): every chapter opens cold and ends on a question the next one answers; the midpoint twist ("Case closed? Not quite." — during the 20-year War of the Soups and the Sparks, Otto Loewi in Graz woke on Easter Saturday night in March 1921 with an experimental design he couldn't decipher the next morning, woke at 3:00 a.m. the following night from the exact same dream, hurried to his laboratory, and transferred saline from a vagus-stimulated frog heart to a denervated frog heart to prove chemical synaptic transmission via *Vagusstoff* / acetylcholine, sharing the 1936 Nobel Prize with Henry Dale) lands in Part 04; the popular misconception ("People often say the human brain runs on pure electricity like a copper computer chip — or repeat the old myth that you only use ten percent of your brain") is raised and explained away in Part 05 via the electrochemical relay (action potentials at up to 100 m/s triggering <1 ms chemical neurotransmitter release across 100 trillion 20-nanometre synapses); the ending hands off directly to `034` (*The Greenhouse Effect & Ice Ages: Eunice Newton Foote's August 1856 Sunlit Glass Cylinders, John Tyndall's May 1859 Spectrophotometer & Svante Arrhenius's April 1896 Calculation*), with no goodbye and no subscribe ask. Five VO parts, matching 009–032.

## Marker count (v01)

Run on `neurons_script_master_v01.md`: `grep -o "DATA:" … | wc -l`, and the same for each marker.

| Marker | Count | Where | Rule |
|---|---:|---|---|
| `DATA` | **6** | 1) inked scale & brain-network diagram on period paper showing 86 billion neurons connected by ~100 trillion synapses, each separated by a 20-nanometre synaptic cleft (5,000× thinner than a 100,000 nm human hair) (0:34); 2) inked size-scale bar comparing a human hair (100,000 nm) vs a red blood cell (7,500 nm) vs the synaptic cleft (20–40 nm) (0:52); 3) inked comparison diagram on period paper showing conventional carmine stain (100% of neurons stained = unreadable tangled mat) vs Camillo Golgi's 1873 silver chromate "black reaction" (1%–5% of neurons stained completely black on a clear yellow background) (1:58); 4) inked diagram on period paper of Cajal's Law of Dynamic Polarization (dendrites → soma → axon → 20 nm synaptic cleft → next dendrite) alongside 1954–1955 electron microscopy resolution (0.2 nm electron microscope resolving the 20 nm synaptic cleft vs 200 nm limit of 19th-century light microscopes) (3:42); 5) inked kymograph & two-heart diagram on period paper of Otto Loewi's March 1921 Graz experiment (Heart #1 with vagus nerve stimulated at ~1–2 Hz slows from ~40 bpm to ~10–15 bpm; transferring Vagusstoff / acetylcholine saline to denervated Heart #2 slows Heart #2 identically without electrical contact; atropine blocks the effect) (5:32); 6) animated timeline building 2 Aug 1873 · May 1888–1891 · 1897 & Dec 1906 · Mar 1921 & 1936 · 1954–1955 alongside an inked electrochemical relay diagram showing an electrical spike racing down an axon at 100 m/s and releasing chemical vesicles across the 20 nm cleft in <1 ms (6:43) | 3 or more per long, including the animated timeline |
| `SCALE` | **6** | 1) a synaptic gap is just 20 nanometres wide — five thousand times thinner than a single human hair, yet wide enough that no two brain cells fuse together (0:34); 2) five thousand synaptic gaps laid side by side would barely span the width of one human hair (0:52); 3) by staining only one to five cells out of every hundred, Golgi's silver reaction made single trees visible inside the densest forest in nature (1:58); 4) nineteenth-century light microscopes blurred anything smaller than 200 nanometres — ten times wider than the 20-nanometre synaptic gap, which is why only Cajal's embryonic silver stains and 1950s electron microscopes could prove the gap was real (3:42); 5) a few drops of clear salt water pipetted from one frog heart to another at three in the morning proved that every human thought, memory, and heartbeat relies on microscopic chemical messengers crossing a 20-nanometre gap (5:32); 6) an electrical impulse racing at 100 metres per second converts into a chemical puff that crosses a 20-nanometre gap in less than one millisecond — firing across 100 trillion synapses inside a three-pound brain (6:43) | Every `DATA` number gets a `SCALE:` comparison (`grep -c "SCALE:"` ≥ `DATA:` count) |
| `WHO` | **5** | Camillo Golgi (0:34), Santiago Ramón y Cajal (0:34), Otto Loewi (0:34), Charles Scott Sherrington (3:08), Henry Hallett Dale (4:58) | First mention only, role right for the scene's year (4 words or fewer) |
| `WHEN` | **20** | Barcelona May 1888 (0:00), Graz March 1921 (0:00), Barcelona 1888 (0:21), 1873 (0:34), May 1888 (0:34), March 1921 (0:34), 2 August 1873 (1:28), 1887 (3:08), 1891 (3:08), 1897 (3:08), 11 December 1906 (3:08), 12 December 1906 (3:08), 1954 (3:08), 1903 (4:58), March 1921 (4:58), 1936 (4:58), 1873–1955 (6:43), August 1856 (7:45), 1859 (7:45), 1896 (7:45) | Every spoken date or era; later dates drop onto the timeline |
| `FACT` | **4** | Stained just 1 in 100 cells (1:28); Clashed on the Nobel stage (3:08); Dreamed the experiment twice (4:58); 100 trillion chemical gaps (6:43) | 2–4 per long (4 words or fewer per card) |

## Craft checks (*Reference lessons* §1 + *Polish pass*)

- **First-minute timings:** Answer image by 0:03 (Santiago Ramón y Cajal at his Barcelona kitchen table in May 1888 peering through a brass microscope at a jet-black silver-stained Purkinje neuron, dissolving to Otto Loewi in Graz at 3:00 a.m. in March 1921 transferring saline between two beating frog hearts), title question by 0:07, promise by 0:15, stakes by 0:25, first concrete answer & real fact (Cajal's 1888 Neuron Doctrine proving separate cells across 20-nanometre synapses and Loewi's March 1921 chemical neurotransmitter proof) by 0:34.
- **Explorer limits:** 2 beats total (`[EXPLORER ACTS: once. …]`), at 1:05 (Part 01, outside the first minute) and 6:08 (Part 04 shrugging at an unreadable midnight note before pipetting glowing droplets from Heart #1 to Heart #2).
- **Chapter cold opens & cliffhanger questions:** Part 01 ends on why 19th-century scientists believed the brain was one giant fused plumbing pipe and how a midnight discovery in an Italian hospital kitchen let us see inside it; Part 02 opens cold on the brain as the one exception to Cell Theory, the Reticular Theory, and Camillo Golgi's 2 August 1873 discovery of *la reazione nera* in his Abbiategrasso apartment kitchen staining 1%–5% of neurons jet-black, ending on why Golgi himself still swore nerve fibres were fused until a 35-year-old Spanish artist saw the stain in 1887; Part 03 opens cold on Cajal's childhood as an artist, seeing Golgi's stain in Madrid in 1887, staining embryonic brains ("young saplings") in Barcelona in May 1888 to prove free nerve endings and the Law of Dynamic Polarization, Wilhelm Waldeyer's "neuron" (1891) and Charles Sherrington's "synapse" (1897), and the 11–12 December 1906 Stockholm Nobel stage fight settled by the 1954 electron microscope, ending on how a signal jumps the 20-nanometre canyon — by an electric spark or a chemical soup; Part 04 opens cold on the midpoint twist ("Case closed? Not quite." — the War of the Soups and the Sparks, Otto Loewi's illegible Easter Saturday night note in March 1921, waking at 3:00 a.m. Sunday night from the same dream, and the two-frog-heart *Vagusstoff* / acetylcholine experiment earning the 1936 Nobel Prize with Henry Dale), ending on how electrical sparks and chemical puffs team up inside your head every millisecond; Part 05 opens cold on the "pure electricity / 10% of your brain" misconception, explains the 100 m/s spike to <1 ms chemical puff relay, and hands off to Eunice Newton Foote's August 1856 sunlit glass cylinders, John Tyndall's 1859 infrared tube, and Svante Arrhenius's 1896 calculation (`034`).
- **Quirky anecdote before the hard idea:** Camillo Golgi setting up a microscope lab in his hospital apartment kitchen by candlelight; Otto Loewi scribbling a Nobel-winning experiment in the middle of the night, being unable to read his own handwriting at 6:00 a.m., and dreaming the exact same experiment again the next night at 3:00 a.m.
- **Rivalry / tension:** Camillo Golgi and Santiago Ramón y Cajal sharing the 1906 Nobel Prize stage in Stockholm and using their Nobel lectures on consecutive days (11–12 December 1906) to argue opposite theories of the human brain; the 20-year War of the Soups and the Sparks.
- **Misconception explained away:** "People often say the human brain runs on pure electricity like a copper computer chip — or repeat the old myth that you only use ten percent of your brain" — explained via both electrical action potentials (up to 100 m/s along the axon) and chemical neurotransmitter puffs (<1 ms across the 20 nm synaptic cleft) working together across 100% of the brain (Part 05, 6:43).

## For Chief to decide

1. Lock **033 = Sparks & Synapses: How the Brain Sends Messages — Santiago Ramón y Cajal's 1887 Kitchen Silver Stain & Otto Loewi's 1921 Easter Night Dream of Two Frog Hearts (1873–1921)** and pick the 2-way Test & Compare working title pair:
   - **A (Subject + hook, §1 rule 11):** *Neurons & Synapses: The 3 AM Dream That Solved How Brains Work* (62 chars)
   - **B (Search question, §1 rule 2):** *Why Your 86 Billion Brain Cells Never Actually Touch Each Other* (63 chars)
   - **Alt (Search / twist question):** *How a Kitchen Silver Stain and Two Frog Hearts Solved the Brain* (63 chars)
2. Review `neurons_script_master_v01.md` (93.7/100 PASS), then queue the Gemini facts pass (`--kind facts`) on `SOURCES_v01.md` (rows 1–4) before VO.

## Score (`npm run review:script`)

```text
# neurons_script_master_v01.md

**Decision:** PASS · **Score:** 93.7 / 100

| Dimension | Score |
|---|---:|
| hook | 9.5 |
| curiosity | 9.5 |
| storytelling | 9.5 |
| scientificAccuracy | 10 |
| emotion | 9.6 |
| escalation | 8.4 |
| retentionPotential | 9 |
| searchPotential | 9.1 |
| visualOpportunities | 9.5 |
| narrationFlow | 9.6 |

Words: 1618 · Est. min: 10.8 · Chapters: 4

## Cold open excerpt

> Why don't the eighty-six billion nerve cells inside your brain ever touch each other — and how did a three-in-the-morning dream prove how your thoughts cross the gap? By the end of this film, you'll see how an accidental spill of silver nitrate in an Italian hospital kitchen reve

## Findings

- **[info] overall:** Structure gates 8/8 — applied +1.05 completeness boost to supporting dimensions.
- **[info] overall:** PASS 93.7/100 — proceed to VO after production checklist.

Pass threshold: 90
```
