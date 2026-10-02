# 004 back-catalogue Short — gold foil (Sun 1 Nov 2026 11:30 UK) · scripts v02

**Status: v02, approved by Claude with one accuracy fix** (desk PR #180 comment 5950150517, 2 Oct 2026). v01 said the foil "threw a bullet back": nobody fired a bullet (they fired alpha particles) and the shell is Rutherford's comparison, so the title and first line are changed. Everything else is v01. Under Ben's 2 Oct rule Claude reviews Short scripts; Ben sees the built Short, cover and title in the second final-OK package. Nothing is uploaded or scheduled.

**What changed from v01:** title *The Gold Foil That Threw a Bullet Back* → **_Why Gold Foil Bounced Rutherford's Particles Back_**; first line "Gold foil threw a bullet back." → **"Tiny particles bounced back off gold foil."** Frame 0, hook and cover (GOLD / *threw it* / BACK) are unchanged, per Claude. Picture plan and plates are unchanged; the in-points as built are in the index. Built by `_build_backcat_nov_v01.py` (index `SHORTS_INDEX_BACKCAT_v01.json`).

Rules: `HOS_STRATEGY.md` → *Short hook* and *The first two seconds*; `STUDIO_PLAYBOOK.md` §3 and §7; `THUMBNAIL_AND_TITLE_RULES.md` §3.3 (frame-0 caption 8–10% cap height, centred) and §4 (cover 85–90% width, across the top). Voice: Ben Orbit Narrator, speed 1.04. Picture: **004 Part 04 KEEP plates only** (`07_Edit-Project/part04_rough_v02_land_meta.json`), no new mint.

Every Short: 22–27 s; the named thing at frame 0, already moving; the first words are the claim; a visible change by 1 s; the Explorer never at frame 0 (he is in none of these plates); captions throughout; the promoted long's **exact live title** on screen at 9–14 s; the last ~3 s return to the opening picture so it loops; `gate_shorts_open.py check --air-date 2026-11-01` PASS; `vo_check` PASS; Studio Related → `GHZDsiH7L7A`; no `/go/`, no pinned comment.

**Promoted long:** *What's Really Inside an Atom?* (`GHZDsiH7L7A`, public Thu 15 Oct 18:00). Live title read 2 Oct from `audits/LIVE_VIDEOS.json`; re-read it after 15 Oct, before export.

**Repeat check (2 Oct 2026, 10:30 UK).** The live Shorts page (`yt-dlp --flat-playlist …/@HistoryOfScienceYT/shorts`) lists 13 public Shorts: germs ×5, periodic table ×5, X-rays ×3. `SHORTS_LOG.md` adds three scheduled: gold halves (16 Oct, 004), every eighth element (18 Oct, 002), carbolic spray (20 Oct, 001). None is about Rutherford, the gold-foil bounce or the shell and tissue paper. The 16 Oct gold-halves Short already says "a pea in a stadium", so this one leaves the stadium out and its plates.

**The week of 29 Oct:** Fri 30 Oct → 005 (Short A), **Sun 1 Nov → 004 (this)**, Tue 3 Nov → 002. Three different films.

---

## Short — the shell that came back

- **Title:** *Why Gold Foil Bounced Rutherford's Particles Back* (49 characters; familiar noun "gold foil" up front; not a copy of any live title).
- **Frame 0:** the brass shell striking a sheet of tissue paper in an ornate frame, already moving (Part 04 plate `12_shell_comes_back_v02`, trimmed to start at about 1.5 s).
- **Hook caption (frame 0):** IT CAME **BACK** (yellow on BACK; cap height 8–10%, centred).
- **Change by 1 s:** the shell recoils off the tissue and flies back at the camera.
- **Cover (live style, across the top, 85–90% width):** GOLD / *threw it* / BACK (teal middle line), on a painted scene of a gleaming shell bouncing back off a sheet of tissue paper over a gold-foil frame, the Explorer small, ducking, lower left.

| s | Picture (Part 04 KEEP plate) | Spoken |
|---|---|---|
| 0–2.5 | `12_shell_comes_back_v02` from 1.5 s: shell hits the tissue and bounces back | Tiny particles bounced back off gold foil. |
| 2.5–7 | `03_fire_at_gold_v01`: Rutherford's team fires the beam at the foil | In nineteen-oh-nine, Rutherford's team fired tiny particles at gold thinner than paper. |
| 7–9.5 | `09_almost_all_pass_v02` from 4 s: the stream pours through the foil | Almost all went straight through. |
| 9–14 | **title on screen:** *What's Really Inside an Atom?* | |
| 9.5–12.5 | `07_green_flash_count_v02`: green flashes counted through the eyepiece | About one in eight thousand bounced back. |
| 12.5–18.5 | `11_shell_tissue_v02` from 2 s: the shell driving into the tissue | Rutherford said it was like firing a shell at tissue paper, and it came back and hit you. |
| 18.5–22.5 | `13_mass_packed_v02` from 3 s: the atom opens to a tiny bright centre | An atom's mass sits almost all in one tiny centre: the nucleus. |
| 22.5–25 | back to `12_shell_comes_back_v02` from 1.5 s (loop) | |

**Script (61 words):**

Tiny particles bounced back off gold foil. In nineteen-oh-nine, Rutherford's team fired tiny particles at gold thinner than paper. Almost all went straight through. About one in eight thousand bounced back. Rutherford said it was like firing a shell at tissue paper, and it came back and hit you. An atom's mass sits almost all in one tiny centre: the nucleus.

At the narrator's 150–155 wpm, 61 words run about 23–24 s, then the loop tail.

*Fact check:*
- Geiger and Marsden, Manchester, 1909, alpha particles on gold foil; about 1 in 8,000 turned back through more than 90° (Geiger & Marsden, *Proc. R. Soc. A* 82, 1909). The film's Part 04 says the same ("about one in eight thousand bounces back").
- "Tiny particles", not "bullet": they fired alpha particles. The shell and tissue paper are Rutherford's comparison, and the VO frames them that way ("Rutherford said it was like…").
- Rutherford's line: "as if you fired a 15-inch shell at a piece of tissue paper and it came back and hit you" (Rutherford, 1936 lecture, *Background to Modern Science*, 1938), his later recollection of 1909, so the VO keeps "Rutherford said". Quoted in the film's Part 04.
- Nucleus, 1911 (Rutherford, *Phil. Mag.* 21). "Mass", not "all of the atom": the film says "nearly all of an atom's mass is packed into a tiny, positive centre".

**Plates (all from `part04_rough_v02_land_meta.json`, no new mint):**

| Plate | File | sha256 | Mode |
|---|---|---|---|
| 12_shell_comes_back | `04_Generated-Clips/part04/raw/v01/12_shell_comes_back_v02.mp4` | `3764483d…` | Fast |
| 03_fire_at_gold | `…/03_fire_at_gold_v01.mp4` | `d64e1b33…` | Fast |
| 09_almost_all_pass | `…/09_almost_all_pass_v02.mp4` | `c73023c9…` | Fast |
| 07_green_flash_count | `…/07_green_flash_count_v02.mp4` | `3c388ef1…` | Quality |
| 11_shell_tissue | `…/11_shell_tissue_v02.mp4` | `78ee7164…` | Fast |
| 13_mass_packed | `…/13_mass_packed_v02.mp4` | `a770491d…` | Quality |

The build script copies each sha from the land meta into `SHORTS_INDEX_BACKCAT_v01.json` and refuses a plate whose sha doesn't match.
