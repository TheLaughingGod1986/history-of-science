# 009 Shorts scripts v02

**v02 (Claude, 9 Oct 2026): test B, Ben said yes.** Two Shorts per film, not three. Each is titled as the question people type, checked against YouTube autocomplete (signed out, en-GB) on 9 Oct. Short C of v01 is dropped (kept in v01 for a later slot). The on-screen long title at 9–14 s and everything else in the format line below still apply. Test plan and readouts: orbit-with-ben `05_Analytics/tests/SHORTS_TESTS.md`.

**Status: written by Claude, 4 Oct 2026.** Script PASS by Claude is the VO gate (Ben, 4 Oct 16:52, relayed on desk PR #180, comment 5981814178). Ben's final OK comes on the finished Shorts.

Rules: `HOS_STRATEGY.md` → *Short hook* and *The first two seconds*; `STUDIO_PLAYBOOK.md` §3 (Short) and §7. Voice: Ben Orbit Narrator, same settings as the long. Picture is cut from the long's own plates wherever possible.

Every Short: 22–27 s; the named thing at frame 0, already moving; the first words are the claim; a visible change by 1 s; a 2–4 word hook caption on frame 0 (yellow on the hook word); the Explorer never at frame 0; captions throughout; the promoted long's **exact live title** on screen at 9–14 s, never spoken; the last 4 s return to the opening picture so it loops; `gate_shorts_open.py check` PASS; Studio Related → the 009 long; no `/go/`, no pinned comment.

**Promoted long (title on screen at 9–14 s):** *Why Doesn't the Moon Fall to Earth?* (proposed; re-read the live title before export).

**Repeat check (4 Oct 2026):** `SHORTS_LOG.md` and the live Shorts list (16 public) have no HOS Short about gravity, Newton, the Moon, orbits or comets. The two below don't repeat each other.

**The week:** the first Short below is the lead on the Friday after the long airs (11:30 UK); the second goes to the following Sun or Tue slot. One Short a day, never before the long is public.

Word counts are spoken words. At 150–155 wpm, 57–63 words run about 23–25 s.

---

## Short A — the Moon is falling (lead, the Friday after the long airs, 11:30 UK)

**YouTube title (test B, search-worded, autocomplete-checked 9 Oct):** *Why Doesn't the Moon Crash Into the Earth?*


- **Frame 0:** the full Moon already sliding along its curve, a glowing line showing each small drop (long Part 01 plate `moon_falling`).
- **Hook caption:** IT'S **FALLING**
- **Change by 1 s:** the line drops, then swings sideways.

| s | Picture | Spoken |
|---|---|---|
| 0–2 | Moon on its falling curve | The Moon is falling towards the Earth right now. |
| 2–7 | teach diagram: sideways arrow and small drop | Every second, it moves sideways about a kilometre, and drops a tiny bit towards us. |
| 7–12 | Newton's cannonball falls all the way round | But the Earth curves away beneath it, so it keeps on missing. |
| 9–14 | **title on screen:** *Why Doesn't the Moon Fall to Earth?* |  |
| 12–18 | young Newton in the orchard looking up | Isaac Newton worked this out, more than three hundred years ago. |
| 18–24 | back to the Moon (loop) | An orbit isn't floating at all. It's falling, and missing, for ever. |

**Script (59 words):**

The Moon is falling towards the Earth right now. Every second, it moves sideways about a kilometre, and drops a tiny bit towards us. But the Earth curves away beneath it, so it keeps on missing. Isaac Newton worked this out, more than three hundred years ago. An orbit isn't floating at all. It's falling, and missing, for ever.

*Fact check:* NASA Moon fact sheet (about 1.02 km/s); *Principia* III Prop. IV; Newton's cannon (*System of the World*). The long's FACT_NOTES rows.

---

## Short B — one minute, one second (second, the following Sun or Tue slot)

**YouTube title (test B, search-worded, autocomplete-checked 9 Oct):** *How Did Newton Discover Gravity?*


- **Frame 0:** split screen already running: an apple dropping beside a ruler, the Moon sliding on its curve (long Part 04 plate `minute_second`).
- **Hook caption:** 1 MINUTE = **1 SECOND**
- **Change by 1 s:** both drops land at the same mark.

| s | Picture | Spoken |
|---|---|---|
| 0–2 | split screen | In one minute, the Moon falls about as far as an apple falls in one second. |
| 2–5 | Newton at his desk with the sum | Isaac Newton worked out why. |
| 5–11 | sixty Earths in a line to the Moon | The Moon is sixty times further from the Earth's centre than we are, |
| 9–14 | **title on screen:** *Why Doesn't the Moon Fall to Earth?* |  |
| 11–18 | 60 × 60 dot square shrinks the pull arrow | so the pull on it is sixty times sixty weaker. Three thousand six hundred times. |
| 18–24 | back to the split screen (loop) | And the numbers matched. One pull, for apples and Moons. |

**Script (59 words):**

In one minute, the Moon falls about as far as an apple falls in one second. Isaac Newton worked out why. The Moon is sixty times further from the Earth's centre than we are, so the pull on it is sixty times sixty weaker. Three thousand six hundred times. And the numbers matched. One pull, for apples and Moons.

*Fact check:* *Principia* III Prop. IV (15 1/12 Paris feet in one minute vs one second); Add. MS 3968 ("answer pretty nearly"). The long's FACT_NOTES rows.

---

