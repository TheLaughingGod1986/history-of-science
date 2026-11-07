# 013 Shorts scripts v02

**v02 (5 Nov 2026, `J2240`): test B, Ben said yes.** Two Shorts per film, not three. Each is titled as the question people type, checked against YouTube autocomplete (signed out, en-GB, `10_Shorts/evidence_2026-11-05_shorts_search.json`). The on-screen long title at 9–14 s and everything else in the format line below still apply. Test plan and readouts: orbit-with-ben `05_Analytics/tests/SHORTS_TESTS.md`.

**Status: written 5 Nov 2026 (`J2240`).** Built directly from the Chief-locked long script `01_Script/darwin_script_master_v02.md` (`92.6 PASS`, `J0307`) and `01_Script/FACT_NOTES_v02.md` (`30 OK · 0 PARTIAL · 0 FLAG`, `J0304`/`J0307`). Shorts VO queued (`--kind vo`). Ben's final OK comes on the finished Shorts.

Rules: `HOS_STRATEGY.md` → *Short hook* and *The first two seconds*; `STUDIO_PLAYBOOK.md` §3 (Short) and §7; `AGENTS.md` → *Teach on screen* (at most one overlay in the 16:9 centre band, clear of 0–2 s and 9–14 s) and *Reference lessons* §3 (myth-bust opener allowed, no straight trailers); `LEARNINGS.md` #1–#2 (`J0899`/`J0909` positive question titles + payoff withheld past 15 s). Voice: Ben Orbit Narrator, same settings as the long (`eleven_v3`, speed 1.04). Picture is cut from the long's own plates wherever possible.

Every Short: 22–27 s; the named thing at frame 0, already moving; the first words are the question/claim; a visible change by 1 s; a 2–4 word hook caption on frame 0 (yellow on the hook word); the Explorer never at frame 0; captions throughout; the promoted long's **exact live title** on screen at 9–14 s, never spoken; the last 4 s return to the opening picture so it loops; `gate_shorts_open.py check` PASS; Studio Related → the 013 long; no `/go/`, no pinned comment.

**Promoted long (title on screen at 9–14 s):** *Evolution: The Letter That Forced Darwin to Publish* (proposed; 2-way Title T&C on launch with *Why Darwin Kept Natural Selection Secret for 20 Years*; re-read the live title before export).

**`J0899` / `J0909` Shorts title + payoff-past-15s lock:**
- **Positive question titles (`LEARNINGS.md` #1, autocomplete-checked 5 Nov 2026):**
  - Short A: ***How Did Darwin Discover Evolution?*** (YouTube GB autocomplete: **yes**, `how did darwin discover evolution`).
  - Short B: ***What Is Survival of the Fittest?*** (YouTube GB autocomplete: **yes**, `what is survival of the fittest`).
- **Payoff withheld past `15 s` (`≥60–70%` runtime, clear of the `9.0–14.0 s` promoted-long title banner, `LEARNINGS.md` #2):**
  - **Short A (60 words, ~24 s):** `0–14 s` busts the Galápagos beach myth and explains that Darwin thought the birds were blackbirds and wrens and forgot to label their islands while the `9–14 s` banner runs; the payoff (*"Only back in London did John Gould show him they were all finches, with different beaks. Months later, Darwin drew a branching tree, and wrote: I think."*) lands at **`14.5–24.0 s`**.
  - **Short B (61 words, ~24 s):** `0–14 s` reveals Darwin didn't coin the phrase and tells how Herbert Spencer (1864) and Alfred Russel Wallace persuaded him to add it while the `9–14 s` banner runs; the definition payoff (*"And fittest never meant the strongest animal. It means the one that fits its world best, like a key in a lock."*) lands at **`15.0–24.0 s`**.

**Repeat check (5 Nov 2026):** `SHORTS_LOG.md` and `LIVE_VIDEOS.json` have no HOS Short about Darwin, Wallace, Galápagos finches, evolution, natural selection, or Herbert Spencer. The two below don't repeat each other.

**The week:** Short A is the lead on the Friday after the long airs (**Fri 18 Dec 2026**, 11:30 UK); Short B goes to the following Sunday or Tuesday slot (**Sun 20 Dec 2026**, 11:30 UK). One Short a day, never before the long is public.

Word counts are spoken words. At 146–155 wpm, 60–61 words run about 23.5–25.0 s.

---

## Short A — the birds he forgot to label (lead, Fri 18 Dec 2026, 11:30 UK)

**YouTube title (test B, search-worded, autocomplete-checked 5 Nov: `yes`):** *How Did Darwin Discover Evolution?*

- **Frame 0:** four Galápagos finch specimens with very different beaks laid out on a candlelit wooden table beside an open notebook; a hand reaches for an unlabelled skin (long Part 01 plate `study_beaks`).
- **Hook caption:** FORGOT THE **LABELS**
- **Change by 1 s:** the hand turns the bird skin over to reveal a blank paper tag.
- **Single overlay (16:9 centre band, 15–18 s, clear of 0–2 s and 9–14 s):** `LONDON · 1837` (WHEN stamp in white Didot italic).

| s | Picture | Spoken |
|---|---|---|
| 0–4 | finch skins on the table; blank tag turned over | How did Charles Darwin discover evolution? Not on a Galápagos beach. |
| 4–14 | young Darwin on the black lava shore bagging small dark birds without island labels | In eighteen thirty-five, he thought the birds there were blackbirds and wrens, and mostly forgot to label which island each came from. |
| 9–14 | **title on screen:** *Evolution: The Letter That Forced Darwin to Publish* |  |
| 14–19 | London, 1837: John Gould sorts the skins by beak shape (`WHEN: LONDON · 1837` at 15–18 s) | Only back in London did John Gould show him they were all finches, with different beaks. |
| 19–24 | Darwin's 1837 "I think" branching tree draws itself in candle-gold ink, then back to the four finch beaks on the table (loop) | Months later, Darwin drew a branching tree, and wrote: I think. |

**Script (60 words, `10_Shorts/vo_v02/hos_013_short_A_v02.txt`):**

How did Charles Darwin discover evolution? Not on a Galápagos beach. In eighteen thirty-five, he thought the birds there were blackbirds and wrens, and mostly forgot to label which island each came from. Only back in London did John Gould show him they were all finches, with different beaks. Months later, Darwin drew a branching tree, and wrote: I think.

*Fact check:* `01_Script/FACT_NOTES_v02.md` rows 1 (Notebook B p. 36, `"36 I think"`, July 1837), 4 (*Journal of Researches* 1845 p. 395 & *Ornithological Notes* pp. 262–264), and 6 (Gould in London, 1837). No species count spoken.

---

## Short B — survival of the fittest (second, Sun 20 Dec 2026, 11:30 UK)

**YouTube title (test B, search-worded, autocomplete-checked 5 Nov: `yes`):** *What Is Survival of the Fittest?*

- **Frame 0:** a brass key already sliding toward an iron lock on a Victorian desk beside a green copy of *On the Origin of Species* (long Part 06 plate `key_in_lock`).
- **Hook caption:** NOT THE **STRONGEST**
- **Change by 1 s:** the key slides into the lock and engages the wards.
- **Single overlay (16:9 centre band, 16–19 s, clear of 0–2 s and 9–14 s):** `FIT = FITS` (fact card in white Didot italic).

| s | Picture | Spoken |
|---|---|---|
| 0–5 | brass key sliding into the lock beside *Origin* | What is survival of the fittest? Charles Darwin didn't even coin the famous phrase. |
| 5–14 | Herbert Spencer writing at his desk (1864); Wallace's 1866 letter arriving at Down House | The writer Herbert Spencer came up with it in eighteen sixty-four, and Alfred Russel Wallace persuaded Darwin to add it to his book years later. |
| 9–14 | **title on screen:** *Evolution: The Letter That Forced Darwin to Publish* |  |
| 14–19 | finch beaks matched to hard seeds vs cactus flowers (`FACT: FIT = FITS` at 16–19 s) | And fittest never meant the strongest animal. |
| 19–24 | the brass key turns cleanly in the lock, then back to the key sliding in (loop) | It means the one that fits its world best, like a key in a lock. |

**Script (61 words, `10_Shorts/vo_v02/hos_013_short_B_v02.txt`):**

What is survival of the fittest? Charles Darwin didn't even coin the famous phrase. The writer Herbert Spencer came up with it in eighteen sixty-four, and Alfred Russel Wallace persuaded Darwin to add it to his book years later. And fittest never meant the strongest animal. It means the one that fits its world best, like a key in a lock.

*Fact check:* `01_Script/FACT_NOTES_v02.md` row 30 (Herbert Spencer, *Principles of Biology*, 1864; A. R. Wallace to C. R. Darwin, 2 July 1866, DCP Letter 5140; C. R. Darwin, *On the Origin of Species*, 5th ed., 1869, Ch. 4, p. 72).
