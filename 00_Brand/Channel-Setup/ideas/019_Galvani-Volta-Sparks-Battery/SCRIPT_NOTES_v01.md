# 019 script v01: notes for review (J0429)

Script: `galvani_script_master_v01.md` (with `opening_and_outline_v00.md`, `SOURCES_v00.md` and `SOURCES_v01.md`).

**Draft only (J0429, Gemini Argon, 17 Oct 2026).** Built from `019_Galvani-Volta-Sparks-Battery/opening_and_outline_v00.md` and the neighbour and search evidence in `IDEAS_2026-10-16_J0404.md` (`evidence_2026-10-16_J0404/n_galvani.md` PASS — 4 strictly on-topic education videos ≥ 1M views led by **CrashCourse *The Nervous System, Part 1* 11.16M**, **CrashCourse *The Nervous System, Part 2 - Action! Potential!* 8.17M**, **CrashCourse *Central Nervous System* 5.49M**, and **Amoeba Sisters *Nervous System* 4.16M**, plus `public_search.md` showing all 5 top GB slots under 92k views on `"luigi galvani frog legs"` and all 5 under 166k views on `"alessandro volta battery"`). The topic isn't locked yet: Chief locks `019` and the working title pair first, then reviews/signs off this script and queues the Gemini facts pass (`--kind facts`) on `SOURCES_v01.md` (rows 1–10) before VO.

Structure (*Reference lessons* §1, scripts from 011 on): every chapter opens cold and ends on a question the next one answers; the midpoint twist ("Case closed? Wrong." — after Alessandro Volta's 1792–1800 metallic electricity experiments and silver-zinc Voltaic pile seemingly crushed "animal electricity," Luigi Galvani and Giovanni Aldini dissected frog legs with a glass knife in 1794 and 1797 and triggered violent contractions by touching bare sciatic nerve directly to muscle with zero metal of any kind, before Emil du Bois-Reymond's 1848 galvanometer measured the -70 mV to +40 mV nerve action potential and proved both rivals right) lands in Part 04; the popular misconception ("Many people picture the nerves in your arms and brain as tiny insulated wires carrying electricity like a lamp cord in a wall") is raised and explained away in Part 05 with active sodium/potassium ion domino channels regenerating a 110 mV pulse at up to 120 m/s (270 mph); the ending hands off directly to `021` (*Electromagnetism: Hans Christian Ørsted's Twitching Compass & Michael Faraday's Cup of Mercury*, 21 April 1820), with no goodbye and no subscribe ask. Five VO parts, matching 009–018.

## Marker count (v01)

Run on `galvani_script_master_v01.md`: `grep -o "DATA:" … | wc -l`, and the same for each marker.

| Marker | Count | Where | Rule |
|---|---:|---|---|
| `DATA` | **6** | 1) inked comparison of Volta's 1800 silver-zinc pile (~1 V per cell pair, 30 pairs continuous current) vs the nerve action potential inside living muscle and brain cells (-70 mV resting to +40 mV peak, 110 mV swing) (0:34); 2) inked human nervous-system scale showing 86 billion neurons firing at up to 120 m/s (270 mph) on 20 watts of total power (0:52); 3) inked comparison diagram of Galvani's 1791 biological Leyden jar model and frog sciatic nerve conduction at 30 metres per second (2:28); 4) inked cutaway diagram of Volta's March 1800 Voltaic pile of 30 alternating silver (Ag) and zinc (Zn) pairs separated by brine-soaked cardboard, producing ~0.76 to 1.1 volts per pair (~30 volts continuous current) (4:18); 5) inked nerve-membrane diagram showing sodium (Na+) and potassium (K+) ions rushing across a neuron membrane to flip the voltage from -70 mV to +40 mV (the action potential measured by du Bois-Reymond in 1848) (6:00); 6) animated timeline building 6 Nov 1780 · 20 Sep 1786 · 1791 · 1794 · 20 Mar 1800 · 17 Jan 1803 · 1848 alongside an inked axon domino diagram showing Na+/K+ ion gates regenerating a 110 mV pulse at up to 120 metres per second (270 mph) (6:43) | 3 or more per long, including the animated timeline |
| `SCALE` | **6** | 1) 70 millivolts across a nerve membrane — a tiny voltage, yet across a cell wall so thin that its electric field is stronger than a lightning bolt (0:34); 2) 86 billion neurons running on 20 watts — less power than the dim bulb inside your refrigerator (0:52); 3) 30 metres per second in a frog nerve — crossing the entire leg in less than two-thousandths of a second (2:28); 4) 1 volt per silver-zinc pair — stack 30 pairs and you feel a sharp electric shock in wet hands that flows continuously instead of vanishing in one spark (4:18); 5) -70 millivolts to +40 millivolts in one millisecond — firing up to 1,000 times a second along your nerves (6:00); 6) 120 metres per second (270 mph) — a nerve signal races from your toe to your brain in less than a fiftieth of a second (6:43) | Every `DATA` number gets a `SCALE:` comparison (`grep -c "SCALE:"` ≥ `DATA:` count) |
| `WHO` | **7** | Luigi Galvani (0:34), Lucia Galeazzi Galvani (0:34), Alessandro Volta (0:34), Joseph Banks (3:42), Giovanni Aldini (4:58), Mary Shelley (5:30), Emil du Bois-Reymond (6:00) | First mention only, role right for the scene's year (4 words or fewer) |
| `WHEN` | **18** | Bologna 20 September 1786 (0:00), 1780s (0:21), 20 September 1786 (0:34), 20 March 1800 (0:34), Bologna 6 November 1780 (1:28), 20 September 1786 (1:58), 1791 (2:28), Pavia 1792 (3:08), 20 March 1800 (3:42), 26 June 1800 (3:42), Bologna 1794 (4:58), 1797 (4:58), London 17 January 1803 (5:30), 1818 (5:30), 1848 (6:00), 1780–1848 (6:43), May 1800 (7:18), 21 April 1820 (7:45) | Every spoken date or era; later dates drop onto the timeline |
| `FACT` | **4** | Lucia spotted the first spark (1:28); Tested coins on his tongue (3:08); Kicked with zero metal (4:58); Nerves fire like dominoes (6:43) | 2–4 per long (4 words or fewer per card) |

## Craft checks (*Reference lessons* §1 + *Polish pass*)

- **First-minute timings:** Answer image by 0:03 (dissected frog leg on a brass hook kicking as a spark snaps against an iron balcony railing in Bologna on 20 September 1786, dissolving into Volta's stack of silver and zinc coins), title question by 0:07, promise by 0:15, stakes by 0:25, first concrete answer & real fact (Luigi and Lucia Galvani in 1786, Alessandro Volta's 30-pair silver-zinc battery on 20 March 1800, and the 70-millivolt nerve impulse) by 0:34.
- **Explorer limits:** 2 beats total (`[EXPLORER ACTS: once. …]`), at 1:05 (Part 01, outside the first minute) and 6:00 (Part 04 watching du Bois-Reymond's multi-thousand-turn coil galvanometer needle swing as a living nerve fires and saluting both rivals).
- **Chapter cold opens & cliffhanger questions:** Part 01 ends on why a doctor in Bologna had a spark machine and a plate of frogs on his table and why the legs kicked with no storm cloud in the sky; Part 02 opens cold on 6 November 1780 with Lucia Galeazzi spotting the scalpel-spark twitch and Galvani's 20 September 1786 brass-hook-on-iron-balcony breakthrough, ending on why Italy's greatest physicist applauded Galvani's 1791 paper at first and then decided the frog had nothing to do with making the electricity; Part 03 opens cold on Alessandro Volta in Pavia (1792) discovering the dissimilar-metals rule, testing tin and silver on his own tongue, and stacking 30 pairs of silver, zinc and brine-soaked cardboard on 20 March 1800, ending on what Galvani had quietly done in 1794 using zero metal at all; Part 04 opens cold on the midpoint twist ("Case closed? Wrong." — Galvani's 1794 glass-knife metal-free nerve-to-muscle contraction, Aldini's 17 January 1803 London battery demonstration that inspired Mary Shelley's *Frankenstein*, and du Bois-Reymond's 1848 galvanometer measurement of the -70 mV to +40 mV nerve impulse), ending on why human nerves aren't passive copper wires and what happened in 1820 when a professor held a compass next to Volta's battery wire; Part 05 opens cold on the "copper wires in a wall" misconception, explains the 120 m/s Na+/K+ domino wave and May 1800 water electrolysis, and hands off to Hans Christian Ørsted's 21 April 1820 twitching compass needle (`021`).
- **Quirky anecdote before the hard idea:** Lucia Galeazzi noticing a dead frog's leg jump across the room from a static spark machine on 6 November 1780, and Alessandro Volta putting a strip of tin and a silver spoon on his own tongue in 1792 to taste a continuous sour electric current.
- **Rivalry:** back-and-forth portrait cuts between Luigi Galvani in Bologna and Alessandro Volta in Pavia (3:08).
- **Misconception explained away:** "Many people picture the nerves in your arms and brain as tiny insulated wires carrying electricity like a lamp cord in a wall" — explained via salty-tissue leakage vs active Na+/K+ domino ion channels regenerating a 110 mV wave every millimetre at up to 120 m/s (Part 05, 6:43).

## For Chief to decide

1. Lock **019 = Sparks of Life & the First Battery: Luigi Galvani's Twitching Frog Legs & Alessandro Volta's Pile of Coins (1780–1800)** and pick the 2-way Test & Compare working title pair:
   - **A (Subject + hook, §1 rule 11):** *The First Battery: How a Twitching Frog Leg Changed the World* (61 chars)
   - **B (Search question, §1 rule 2):** *Why a Dead Frog's Leg Kicked and Invented the Electric Battery* (62 chars)
   - **Alt (Rivalry / action question):** *How an Argument Over a Frog's Leg Invented the Battery* (54 chars)
2. Review `galvani_script_master_v01.md` (91.9/100 PASS), then queue the Gemini facts pass (`--kind facts`) on `SOURCES_v01.md` (rows 1–10) before VO.

## Score (`npm run review:script`)

```text
# galvani_script_master_v01.md

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

Words: 1577 · Est. min: 10.5 · Chapters: 4

## Cold open excerpt

> Why did a dead frog's leg kick violently when hung from a brass hook on an iron balcony railing? And how did a furious argument over that single twitch give us both the battery inside your phone and the discovery that your own brain runs on electricity? By the end of this film, y

## Findings

- **[info] overall:** Structure gates 8/8 — applied +1.05 completeness boost to supporting dimensions.
- **[info] overall:** PASS 91.9/100 — proceed to VO after production checklist.

Pass threshold: 90
```
