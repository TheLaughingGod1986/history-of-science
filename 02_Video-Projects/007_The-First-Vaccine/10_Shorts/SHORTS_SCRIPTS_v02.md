# 007 Shorts scripts v02

**v02 (Claude, 9 Oct 2026): test B, Ben said yes.** Two Shorts per film, not three. Each is titled as the question people type, checked against YouTube autocomplete (signed out, en-GB) on 9 Oct. Short A of v01 is dropped (kept in v01 for a later slot). The on-screen long title at 9–14 s and everything else in the format line below still apply. Test plan and readouts: orbit-with-ben `05_Analytics/tests/SHORTS_TESTS.md`.

**Status: written by Claude, 4 Oct 2026.** Script PASS by Claude is the VO gate (Ben, 4 Oct 16:52, relayed on desk PR #180, comment 5981814178). Ben's final OK comes on the finished Shorts.

Rules: `HOS_STRATEGY.md` → *Short hook* and *The first two seconds*; `STUDIO_PLAYBOOK.md` §3 (Short) and §7. Voice: Ben Orbit Narrator, same settings as the long. Picture is cut from the long's own plates wherever possible.

Every Short: 22–27 s; the named thing at frame 0, already moving; the first words are the claim; a visible change by 1 s; a 2–4 word hook caption on frame 0 (yellow on the hook word); the Explorer never at frame 0; captions throughout; the promoted long's **exact live title** on screen at 9–14 s, never spoken; the last 4 s return to the opening picture so it loops; `gate_shorts_open.py check` PASS; Studio Related → the 007 long; no `/go/`, no pinned comment.

**Promoted long (title on screen at 9–14 s):** *Why Vaccines Are Named After a Cow* (proposed; re-read the live title before export).

**Repeat check (4 Oct 2026):** `SHORTS_LOG.md` has no HOS Short about vaccines, smallpox, cowpox, milkmaids or Jenner. The two below don't repeat each other.

**The week:** the first Short below is the lead on the Friday after the long airs (11:30 UK); the second goes to the following Sun or Tue slot. One Short a day, never before the long is public.

Word counts are spoken words. At 150–155 wpm, 57–63 words run about 23–25 s.

---

## Short B — the milkmaids' secret (lead, the Friday after the long airs, 11:30 UK)

**YouTube title (test B, search-worded, autocomplete-checked 9 Oct):** *Who Invented the First Vaccine?*


- **Frame 0:** a milkmaid's hand on the pail handle, already walking past a shuttered house (long Part 02 plate `03_market_day`).
- **Hook caption:** THEY NEVER **CAUGHT IT**
- **Change by 1 s:** a shutter behind her swings closed.

| s | Picture | Spoken |
|---|---|---|
| 0–2 | milkmaid walks past the shuttered house | The first vaccine began with milkmaids, who never caught smallpox. |
| 2–7 | a cow's udder, then the milkmaid's healed hand | They caught cowpox from the cows instead, a few sore spots and nothing more. |
| 7–12 | the quiet village street, shutters closed | And farmers swore that anyone who'd had it was safe from smallpox for life. |
| 9–14 | **title on screen:** *Why Vaccines Are Named After a Cow* | |
| 12–19 | Jenner writing cases at his window | One country doctor, Edward Jenner, took the rumour seriously, and tested it. |
| 19–24 | back to the milkmaid on the street (loop) | He was right, and it became the first vaccine. |

**Script (59 words, about 24 s):**

The first vaccine began with milkmaids, who never caught smallpox. They caught cowpox from the cows instead, a few sore spots and nothing more. And farmers swore that anyone who'd had it was safe from smallpox for life. One country doctor, Edward Jenner, took the rumour seriously, and tested it. He was right, and it became the first vaccine.

*Fact check:* the dairy belief and cowpox's mildness are in FACT_NOTES and the long (Part 02). "Never" is the rumour as stated, not a medical claim; the next line says it had to be tested.

---

## Short C — gone for good (second, the following Sun or Tue slot)

**YouTube title (test B, search-worded, autocomplete-checked 9 Oct):** *How Was Smallpox Eradicated?*


- **Frame 0:** a turning globe with small lights going out one by one (long Part 05 plate `02_globe_lights`).
- **Hook caption:** GONE FOR **GOOD**
- **Change by 1 s:** the last light on one continent winks out.

| s | Picture | Spoken |
|---|---|---|
| 0–2 | globe, lights going out | Smallpox is gone. Forever. |
| 2–7 | the quiet village street, shutters closed | For centuries it killed about three in every ten people it caught. |
| 7–12 | the boy running in the garden; the case-book NO DISEASE FOLLOWED | Then, in 1796, one test showed that cowpox could protect you from it. |
| 9–14 | **title on screen:** *Why Vaccines Are Named After a Cow* | |
| 12–19 | health workers travel village to village | Health workers spread that idea to every country, until smallpox had nowhere left to hide. |
| 19–24 | 8 MAY 1980, then back to the globe (loop) | In 1980, it was declared gone. The first disease humans ever wiped out. |

**Script (61 words):**

Smallpox is gone. Forever. For centuries it killed about three in every ten people it caught. Then, in 1796, one test showed that cowpox could protect you from it. Health workers spread that idea to every country, until smallpox had nowhere left to hide. In 1980, it was declared gone. The first disease humans ever wiped out.

*Fact check:* about 30% case fatality (variola major; WHO); *Inquiry* Case XVII (1796); WHO declaration 8 May 1980. Both lines must be in FACT_NOTES before VO (they're on the long's new-claims list).
