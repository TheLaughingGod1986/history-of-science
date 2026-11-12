# 011 Shorts scripts v02

**v02 (5 Nov 2026, `J2239`): Test B, search-titled Shorts.** Two Shorts per film, not three. Each is titled as the question people type, checked against YouTube autocomplete (signed out, en-GB) on 5 Nov 2026 (`11_Upload-Package/evidence_2026-11-05_shorts_public_search.json`). The on-screen long title at 9–14 s and everything else in the format line below still apply. Test plan and readouts: orbit-with-ben `05_Analytics/tests/SHORTS_TESTS.md`.

**Status: written 5 Nov 2026 (`J2239`).** Every spoken claim is sourced from the locked long script `01_Script/surgery_script_master_v02.md` and `01_Script/FACT_NOTES_v01.md` (`J0198` Gemini facts PASS + `J0224` Claude primary-source quote check PASS). Ben's final OK comes on the finished Shorts.

Rules: `HOS_STRATEGY.md` → *Short hook* and *The first two seconds*; `STUDIO_PLAYBOOK.md` §3 (Short) and §7; `AGENTS.md` → *Teach on screen* (Shorts: at most one overlay inside the 16:9 centre band, clear of 0–2 s and the 9–14 s title). Voice: Ben Orbit Narrator, same settings as the long. Picture is cut from the long's own plates wherever possible.

Every Short: 22–27 s; the named thing at frame 0, already moving; the first words are the claim; a visible change by 1 s; a 2–4 word hook caption on frame 0 (yellow on the hook word); the Explorer never at frame 0; captions throughout; the promoted long's **exact live title** on screen at 9–14 s, never spoken; the last 4 s return to the opening picture so it loops; `gate_shorts_open.py check` PASS; Studio Related → the 011 long; no `/go/`, no pinned comment.

**Promoted long (title on screen at 9–14 s):** *Anesthesia: The Day Surgery Stopped Hurting* (proposed; 2-way Title T&C on launch with *What Surgery Was Like Before Anesthesia* per `J0180`; re-read the live title before export).

**`J0899` / `J0909` Shorts title + payoff-past-15s lock (Chief PASS, 24 Oct 2026):**
- **Positive question titles (`LEARNINGS.md` #1):** Both `v02` Shorts carry positive search-question titles naming the concrete subject: Short A ***How Was Surgery Done Before Anesthesia?*** and Short B ***Who Invented Anesthesia?*** (alt: ***How Was Anesthesia Discovered?***).
- **Payoff withheld past `15 s` (`≥70%` runtime, clear of the `9.0–14.0 s` promoted-long title banner, `LEARNINGS.md` #2):** Neither Short answers its title question's climax during the `9.0–14.0 s` banner window:
  - **Short A (`~24.0 s`):** `8–14 s` sets up that speed was the only mercy while the `9–14 s` banner runs; the Robert Liston pocket-watch amputation payoff (*"In London, students timed Robert Liston with their pocket watches as he took off a leg in just a few minutes."*) lands at **`14.5–23.8 s` (`60%–99%` runtime)**.
  - **Short B (`~23.8 s`):** `8–14 s` sets up the 1846 Boston glass-globe demonstration while the `9–14 s` banner runs; the four-way feud and nameless monument payoff (*"All four fought for decades over the credit, so Boston's stone monument to ether names not a single one of them."*) lands at **`14.5–23.6 s` (`61%–99%` runtime)**.

**Repeat check (5 Nov 2026):** `SHORTS_LOG.md` has 0 HOS Shorts about anaesthesia/anesthesia, ether, laughing gas, Robert Liston, Crawford Long, William Morton, or the Boston Ether Monument (the 001 Short `clV6E10NLPw` *The spray that stopped surgery killing patients* is about Joseph Lister's post-operative carbolic acid antiseptic spray in the 1860s, not anaesthesia). The two below don't repeat each other.

**The week:** the first Short below is the lead on the Friday after the long airs (Fri 11 Dec 2026, 11:30 UK); the second goes to the following Sun 13 Dec or Tue 15 Dec 2026 slot (11:30 UK). One Short a day, never before the long is public.

Word counts are spoken words. At 150–155 wpm, 60–61 words run about 23.5–24.5 s.

---

## Short A — timed with a pocket watch (lead, Fri 11 Dec 2026, 11:30 UK)

**YouTube title (Test B, search-worded, autocomplete-checked 5 Nov):** *How Was Surgery Done Before Anesthesia?*

- **Frame 0:** a surgeon's brass pocket watch already open and sweeping in a steep wooden London operating theatre lit by tall windows (long Part 01 plate `watch_sweep`).
- **Hook caption:** TIMED BY **WATCH**
- **Change by 1 s:** a second student's pocket watch clicks open beside the rail as the second hand sweeps.
- **Single Short overlay (15.5–19.0 s, inside 16:9 centre band, clear of 0–2 s and 9–14 s):** `DATA` brass stopwatch dial sweeping round and stopping short of three minutes (`UNDER 3 MINUTES`).

| s | Picture | Spoken |
|---|---|---|
| 0–2 | open brass pocket watch sweeping in the steep wooden theatre | Before eighteen forty-six, a patient was wide awake for every second of an operation. |
| 2–8 | wooden operating chair in window light; leather straps hanging from the arms | There was no mask and no sleep, just a strong drink and people to hold you still. |
| 8–14 | surgeon in dark frock coat at the wooden table looking up at the gallery rail | So the best surgeon was simply the fastest one. |
| 9–14 | **title on screen:** *Anesthesia: The Day Surgery Stopped Hurting* |  |
| 14–20 | row of students' pocket watches clicking open + `DATA` stopwatch dial overlay (`UNDER 3 MINUTES`, 15.5–19.0 s) | In London, students timed Robert Liston with their pocket watches |
| 20–24 | Liston closing his pocket watch; return to the open brass watch at frame 0 (loop) | as he took off a leg in just a few minutes. |

**Script (61 words):**

Before eighteen forty-six, a patient was wide awake for every second of an operation. There was no mask and no sleep, just a strong drink and people to hold you still. So the best surgeon was simply the fastest one. In London, students timed Robert Liston with their pocket watches as he took off a leg in just a few minutes.

*Fact check:* `FACT_NOTES_v01.md` rows 14, 16, 21, 22 (Science Museum Group on alcohol/opium and restraint before anaesthesia; Russell Museum / Ether Dome history on pre-1846 surgical speed and pocket-watch timing; keeps speed soft at "just a few minutes" / under three minutes, avoiding the unverified "28 seconds" legend). No gore shown.

---

## Short B — four claimants, zero names on the monument (second, Sun 13 Dec or Tue 15 Dec 2026, 11:30 UK)

**YouTube title (Test B, search-worded, autocomplete-checked 5 Nov):** *Who Invented Anesthesia?* (alt: *How Was Anesthesia Discovered?*)

- **Frame 0:** the tall carved stone Ether Monument in Boston Public Garden already tilting up through autumn trees, four portrait frames glinting in shadow beside it (long Part 04 plate `ether_monument`).
- **Hook caption:** WHO WAS **FIRST?**
- **Change by 1 s:** the four portrait frames light up one after another (Long, Wells, Morton, Jackson).
- **Single Short overlay (16.0–19.5 s, inside 16:9 centre band, clear of 0–2 s and 9–14 s):** cream-on-brown teach card `FACT: The monument names nobody`.

| s | Picture | Spoken |
|---|---|---|
| 0–2 | stone Ether Monument tilting up; four portrait frames lighting up | Four different men claimed they invented anesthesia. |
| 2–8 | Crawford Long in his quiet Georgia surgery holding a folded towel | In eighteen forty-two, a country doctor in Georgia used ether on a towel, but didn't publish it. |
| 8–14 | William Morton under the skylight of the Boston Ether Dome holding the two-necked glass globe | In eighteen forty-six, a Boston dentist put a patient to sleep with a glass globe. |
| 9–14 | **title on screen:** *Anesthesia: The Day Surgery Stopped Hurting* |  |
| 14–19 | quick back-and-forth cuts between the four lit portrait frames (Long, Wells, Morton, Jackson) + `FACT: The monument names nobody` (16.0–19.5 s) | All four fought for decades over the credit, |
| 19–24 | close on the carved stone inscription with no claimant names; return to the monument at frame 0 (loop) | so Boston's stone monument to ether names not a single one of them. |

**Script (60 words):**

Four different men claimed they invented anesthesia. In eighteen forty-two, a country doctor in Georgia used ether on a towel, but didn't publish it. In eighteen forty-six, a Boston dentist put a patient to sleep with a glass globe. All four fought for decades over the credit, so Boston's stone monument to ether names not a single one of them.

*Fact check:* `FACT_NOTES_v01.md` rows 3, 4, 7, 12, 13, 25, 30, 32 (Crawford Long's 30 March 1842 ether towel operation and Dec 1849 publication in *Southern Medical and Surgical Journal*; William Morton's 16 Oct 1846 Ether Dome demonstration in Bigelow 1846; 20-year priority controversy among Long, Wells, Morton and Jackson; Boston Public Garden 1868 Ether Monument inscription naming none of the four claimants).
