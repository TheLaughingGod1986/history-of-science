# 027 script v01: notes for review (J0462)

Script: `turing_script_master_v01.md` (with `opening_and_outline_v00.md`, `SOURCES_v00.md` and `SOURCES_v01.md`).

**Draft only (J0462, Gemini Argon, 17 Oct 2026).** Built from `027_Lovelace-Turing-Computer-Enigma/opening_and_outline_v00.md` and the neighbour and search evidence in `IDEAS_2026-10-17_J0454.md` (`evidence_2026-10-17_J0454/n_turing.md` PASS — 4 education videos ≥ 1M views including 3 strictly on-topic ≥ 1M led by **Veritasium *The Insane Real Engineering of the Nazi Enigma Machine* (`JsBZOcqZerk`, 20.03M — #1 competitor upload of the last 30 days in `HOS_2026-10-17.md`)**, **TED-Ed ★ *The Turing test: Can a computer pass for a human? - Alex Gendler* (`3wLqsRLvV-c`, 1.87M)**, and **TED-Ed ★ *The greatest machine that never was - John Graham-Cumming* (`FlfChYGv3Z4`, 1.78M — Babbage & Ada Lovelace's Analytical Engine)**, alongside `public_search.md` showing `"alan turing enigma machine"` autocompleting in GB search and all 5 top GB slots for `"ada lovelace analytical engine"` under 741k views). The topic isn't locked yet: Chief locks `027` and the working title pair first, then reviews/signs off this script and queues the Gemini facts pass (`--kind facts`) on `SOURCES_v01.md` (rows 1–5) before VO.

Structure (*Reference lessons* §1, scripts from 011 on): every chapter opens cold and ends on a question the next one answers; the midpoint twist ("Case closed? Wrong." — when the German military trusted the portable Enigma machine's 158,962,555,217,826,360,000 daily settings, building on Marian Rejewski's 1932–1939 Polish breakthroughs, Alan Turing and Gordon Welchman at Bletchley Park exploited stereotyped morning "cribs" and Enigma's fatal reflector flaw that a letter could never encrypt to itself, building the electromechanical Bombe installed on 18 March 1940 to test 36 Enigma-equivalents in closed electrical loops and crack the daily key in under 20 minutes) lands in Part 04; the popular misconception ("Many people assume Turing's wartime codebreaking made him a celebrated hero in his own lifetime") is raised and explained away in Part 05 via the 1945–1974 Official Secrets Act classification of Bletchley Park, Turing's 1946 ACE design and October 1950 Turing Test paper, his March 1952 conviction and 7 June 1954 death, and his 24 December 2013 Royal Pardon; the ending hands off directly to `028` (*Blood Types & Safe Transfusions: Karl Landsteiner's February 1900 Vienna Blood-Mixing Experiment & Richard Lewisohn's January 1915 Sodium Citrate*), with no goodbye and no subscribe ask. Five VO parts, matching 009–026.

## Marker count (v01)

Run on `turing_script_master_v01.md`: `grep -o "DATA:" … | wc -l`, and the same for each marker.

| Marker | Count | Where | Rule |
|---|---:|---|---|
| `DATA` | **6** | 1) inked architecture comparison on period paper showing Babbage & Lovelace's 1843 Analytical Engine (Punched Cards → "Store" memory of 1,000 fifty-digit numbers ↔ "Mill" processor with conditional branching) and Turing's 1936 Universal Machine (stored-program tape of 0s and 1s) (0:34); 2) inked scale chart of 158,962,555,217,826,360,000 (159 quintillion) Enigma settings vs Turing's 20-minute Bombe sieve (0:52); 3) inked trace table on period paper of Ada Lovelace's August 1843 Note G algorithm calculating the Bernoulli number B₇ using variables V₁–V₁₃ and two nested branching loops (1:58); 4) inked diagram on period paper of Turing's 1936 Universal Machine tape (Instruction bits + Data bits on the same strip of 0s and 1s) alongside the self-referential Halting Problem contradiction matrix (3:42); 5) inked electrical-loop diagram on period paper showing how matching a 16-letter "WETTERVORHERSAGE" crib against ciphertext (where no letter can equal itself) forms a closed electrical loop across 36 spinning Bombe drum triplets, eliminating 99.9999% of plugboard/rotor possibilities at the speed of light (5:28); 6) animated timeline building Aug 1843 · 28 May 1936 · 25 Jul 1939 · 18 Mar 1940 · Oct 1950 · 7 Jun 1954 & 24 Dec 2013 alongside an inked Bletchley Park impact chart (~84,000 Enigma messages decoded/month, shortening WWII in Europe by an estimated 2–4 years and saving ~14 million lives) (6:48) | 3 or more per long, including the animated timeline |
| `SCALE` | **6** | 1) Lovelace wrote a working computer program with nested loops a full 100 years before the first electronic computer was ever switched on (0:34); 2) 159 quintillion possible keys — twenty million times more combinations than there are grains of sand on all the beaches of Earth (0:52); 3) 41 pages of visionary notes written in 1843 — programming nested loops for a machine whose brass gears still hadn't been built (1:58); 4) one rule-table small enough to write on a postcard can simulate every piece of software humanity will ever write (3:42); 5) what would take a human clerk millions of years by hand flashed through Welchman's diagonal board in milliseconds (5:28); 6) ~84,000 intercepted Enigma messages decoded every month at Bletchley Park — shortening World War II in Europe by an estimated 2 to 4 years and saving ~14 million lives (6:48) | Every `DATA` number gets a `SCALE:` comparison (`grep -c "SCALE:"` ≥ `DATA:` count) |
| `WHO` | **9** | Charles Babbage (0:21), John Herschel (0:21), Ada Lovelace (0:34), Alan Turing (0:34), Joseph Marie Jacquard (1:28), Luigi Menabrea (1:58), David Hilbert (3:08), Marian Rejewski (4:53), Gordon Welchman (5:28) | First mention only, role right for the scene's year (4 words or fewer) |
| `WHEN` | **25** | London August 1843 (0:00), Bletchley Park 18 March 1940 (0:00), London 1821 (0:21), August 1843 (0:34), 28 May 1936 (0:34), 5 June 1833 (1:28), 1804 (1:28), 1834 (1:28), October 1842 (1:58), August 1843 (1:58), 1928 (3:08), Cambridge 28 May 1936 (3:08), December 1932 (4:53), 25 July 1939 (4:53), 18 March 1940 (5:28), August 1940 (5:28), February 1946 (6:48), October 1950 (6:48), March 1952 (6:48), 7 June 1954 (6:48), 1974 (6:48), 24 December 2013 (6:48), 1843–2013 (6:48), February 1900 (7:45), January 1915 (7:45) | Every spoken date or era; later dates drop onto the timeline |
| `FACT` | **4** | Notes 3× longer than paper (1:58); Proved some maths unsolvable (3:08); A letter never became itself (5:28); Kept secret until 1974 (6:48) | 2–4 per long (4 words or fewer per card) |

## Craft checks (*Reference lessons* §1 + *Polish pass*)

- **First-minute timings:** Answer image by 0:03 (Ada Lovelace in London in August 1843 tracing a Jacquard punched card beside Babbage's brass gears, morphing into Turing's 1936 paper tape and the 1940 Bletchley Park Bombe drums), title question by 0:07, promise by 0:15, stakes by 0:25, first concrete answer & real fact (Ada Lovelace publishing the first computer algorithm in August 1843 and Alan Turing proving the Universal Computing Machine on 28 May 1936) by 0:34.
- **Explorer limits:** 2 beats total (`[EXPLORER ACTS: once. …]`), at 1:05 (Part 01, outside the first minute) and 6:05 (Part 04 plugging a diagonal cable into an alphabet lamp loop to watch 25 contradictory bulbs flash dark).
- **Chapter cold opens & cliffhanger questions:** Part 01 ends on how a silk-weaving loom inspired the first computer program in Victorian London and why Alan Turing invented the modern computer only while trying to prove a famous maths problem was impossible; Part 02 opens cold on human "computers", Babbage's 1834 Analytical Engine (Store, Mill, 1804 Jacquard cards), and Ada Lovelace's August 1843 Notes A–G (41 pages, Note G Bernoulli number algorithm with nested loops, and Note A symbol/music prophecy), ending on how a 23-year-old runner in Cambridge reinvented the universal computer 93 years later using an imaginary strip of paper tape; Part 03 opens cold on David Hilbert's 1928 *Entscheidungsproblem* and Turing's 28 May 1936 paper defining the Universal Computing Machine and proving the Halting Problem, ending on how Turing turned pure logic into a one-tonne cabinet of spinning bronze drums to crack Nazi Germany's Enigma cipher; Part 04 opens cold on the midpoint twist ("Case closed? Wrong." — 159 quintillion Enigma settings, Marian Rejewski's 1932–1939 Polish *bomba* and Pyry handover, and Turing & Welchman's 18 March 1940 Bombe using cribs and Enigma's self-encryption flaw to find daily keys in under 20 minutes), ending on why the British government burned the blueprints and prosecuted the man who helped save the free world; Part 05 opens cold on the "celebrated wartime hero in his lifetime" misconception, explains the 1945–1974 Official Secrets Act classification, Turing's 1946 ACE and 1950 Turing Test, his 1952 conviction, 1954 death and 2013 Royal Pardon, and hands off to Karl Landsteiner's February 1900 Vienna blood-type discovery and Richard Lewisohn's January 1915 sodium citrate breakthrough (`028`).
- **Quirky anecdote before the hard idea:** "Computer" meaning a human clerk making typos by hand until Babbage cried out *"I wish to God these calculations had been executed by steam!"*; Lady Byron schooling young Ada in mathematics to prevent "poetic madness" inherited from Lord Byron.
- **Rivalry / tension:** Hilbert's dream of complete mathematical decidability shattered by Turing's 1936 Halting Problem, and the battle of wits between Enigma's 159 quintillion daily keys and Rejewski, Turing and Welchman's mathematical sieve.
- **Misconception explained away:** "Many people assume Turing's wartime codebreaking made him a celebrated hero in his own lifetime" — explained via Britain's 30-year secrecy order until 1974 and Turing's 1952 prosecution (Part 05, 6:48).

## For Chief to decide

1. Lock **027 = The First Computer & Breaking Enigma: Ada Lovelace's 1843 Note G & Alan Turing's 1936 Universal Machine and 1940 Bombe (1843–1940)** and pick the 2-way Test & Compare working title pair:
   - **A (Subject + hook, §1 rule 11):** *Breaking Enigma: How a Paper Tape Invented the Computer* (55 chars)
   - **B (Search question, §1 rule 2):** *How a Victorian Countess and Alan Turing Invented Computing* (59 chars)
   - **Alt (Search / twist question):** *How One Flaw in the Enigma Machine Cracked 159 Quintillion Keys* (63 chars)
2. Review `turing_script_master_v01.md` (94.3/100 PASS), then queue the Gemini facts pass (`--kind facts`) on `SOURCES_v01.md` (rows 1–5) before VO.

## Score (`npm run review:script`)

```text
# turing_script_master_v01.md

**Decision:** PASS · **Score:** 94.3 / 100

| Dimension | Score |
|---|---:|
| hook | 9.5 |
| curiosity | 9.5 |
| storytelling | 9.5 |
| scientificAccuracy | 10 |
| emotion | 9.6 |
| escalation | 9 |
| retentionPotential | 9 |
| searchPotential | 9.1 |
| visualOpportunities | 9.5 |
| narrationFlow | 9.6 |

Words: 1490 · Est. min: 9.9 · Chapters: 4

## Cold open excerpt

> How did a Victorian countess writing punched-card tables — and a young mathematician imagining a strip of paper tape — invent the computer and crack an unbreakable cipher? By the end of this film, you'll see why a "computer" used to be a human clerk making fatal navigation mistak

## Findings

- **[info] overall:** Structure gates 8/8 — applied +1.05 completeness boost to supporting dimensions.
- **[info] overall:** PASS 94.3/100 — proceed to VO after production checklist.

Pass threshold: 90
```
