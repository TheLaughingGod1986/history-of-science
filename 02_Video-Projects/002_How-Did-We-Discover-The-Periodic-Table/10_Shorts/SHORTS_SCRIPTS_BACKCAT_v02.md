# 002 back-catalogue Short — the four elements (Tue 3 Nov 2026 11:30 UK) · scripts v02

**Status: v02, approved by Claude** (desk PR #180 comment 5950150517, 2 Oct 2026): title, hook, cover and script as written. This is the **fallback** for Tue 3 Nov: the 003 idea ("He called it X, for unknown") failed the live-page check (below). Ben sees the built Short, cover and title in the second final-OK package. Nothing is uploaded or scheduled.

**What changed from v01:** the Lavoisier beat takes Claude's option 2, one Vertex AI Veo 3.1 **Quality** mint of an 8 s plate (at most 2 takes; `07_Edit-Project/_mint_backcat_lavoisier_vertex_v01.py`, log `BACKCAT_LAVOISIER_MINT_LOG_v01.json`), in place of the labelled-jars plate. The word count in the header is corrected from 60 to 59 (v01 miscounted; not a word of the script changed). Built by `004_…/10_Shorts/_build_backcat_nov_v01.py` (index `SHORTS_INDEX_BACKCAT_v01.json`).

Rules: `HOS_STRATEGY.md` → *Short hook* and *The first two seconds*; `STUDIO_PLAYBOOK.md` §3 and §7; `THUMBNAIL_AND_TITLE_RULES.md` §3.3 (frame-0 caption 8–10% cap height, centred) and §4 (cover 85–90% width, across the top). Voice: Ben Orbit Narrator, speed 1.04. Picture: **002 KEEP plates** (Part 01 `raw/v01_fast/*_v01.mp4`, the plates in the locked `hos_002_part01_rough_v14.mp4`) plus the one approved Lavoisier mint.

Every Short: 22–27 s; the named thing at frame 0, already moving; the first words are the claim; a visible change by 1 s; the Explorer never at frame 0 (none of these plates has him); captions throughout; the promoted long's **exact live title** on screen at 9–14 s; the last ~3 s loop to the opening picture; `gate_shorts_open.py check --air-date 2026-11-03` PASS; `vo_check` PASS; Studio Related → `AL_-qlWko_g`; no `/go/`, no pinned comment.

**Promoted long:** *How Did We Discover the Periodic Table?* (`AL_-qlWko_g`, public). Live title read 2 Oct (`LIVE_VIDEOS.json` and the public page); re-read before export.

## Why not 003 "X, for unknown" (live-page check, 2 Oct 2026)

The live Shorts page lists three X-ray Shorts, all public and all promoting `frP_YrNShsU`. I transcribed the three uploaded files:

- *How X-rays Were Discovered by Accident* (`oowAOWTBoq0`), from `hos_003_s1_cardboard_glow_v01.mp4`: "…A soft glow blooms where no ordinary light is shining. Something left the tube… Something that passes paper, wood and soft things more easily than metal."
- *How did Röntgen see bones without cutting* (`xvanpsLeADE`): "X-rays pass soft tissue more than bone…"
- *The first X-ray showed a wedding ring* (`zI_eD3vFWmE`): "…Different materials stop the unknown ray differently."

"X, for unknown" sits in the same Part 02 scene as the accident Short, and its proof (the locked-door tests: a book, a hand, metal) is the claim the accident Short already makes ("passes paper, wood and soft things more easily than metal") and the ring Short ends on. It **repeats**, so per your call this slot takes the 002/001 fallback.

## Why 002, and why this beat

- **001 is mined out.** Its live and scheduled Shorts already cover bad air (shadow), the first microbes (pond water), Semmelweis's handwashing (*Germs hitch a ride on you*, `hos_001_s03_vector`), Pasteur's flask and Lister's spray (20 Oct).
- **002's live Shorts** cover the empty chairs (×2), gallium (×2), tellurium before iodine, and Newlands' octaves (18 Oct). Unused in 002: the four elements and Lavoisier (Part 01–02), Döbereiner's triads and Karlsruhe (Part 02–03), and the noble gases (Part 05).
- **Rejected inside 002:**
  - **Noble gases:** the only plate (`07b_noble_gas_column`) is a wall of cards with made-up symbols ("Pa", "My", "Uh", "Dg"). That breaks "no AI-made text" and looks like the live empty-chairs Shorts.
  - **Triads / Newlands:** Part 02's plates are Ken Burns stills (`v0N_kenburns`), which aren't allowed. Newlands also aired 18 Oct.
- **The four elements** have real-motion Part 01 plates, a familiar thing everyone has heard of, and a hard fact people don't know.

**The week of 29 Oct:** Fri 30 Oct → 005, Sun 1 Nov → 004, **Tue 3 Nov → 002 (this)**. Three different films. The last 002 Short (every eighth, 18 Oct) is 16 days before.

---

## Short — the four elements were wrong

- **Title:** *The Four Elements Were Wrong* (28 characters; "four elements" is the familiar noun; a yes/no on what everyone believed; not a copy of any live title).
- **Frame 0:** the four carved element shapes on the workbench bursting into dust and swirls, already moving (Part 01 plate `03_four_elements_crumble_v01`, trimmed to start at about 1.8 s).
- **Hook caption (frame 0):** NOT **ELEMENTS** (yellow on ELEMENTS; cap height 8–10%, centred).
- **Change by 1 s:** the shapes break apart into dust.
- **Cover (live style, across the top, 85–90% width):** FOUR / *elements were* / WRONG (teal middle line), on a painted scene of four carved shapes (a rock, a flame, a water drop, a wisp of air) cracking apart on an old workbench, the Explorer small, lower left, holding a list.

| s | Picture (002 KEEP plate) | Spoken |
|---|---|---|
| 0–2.5 | `03_four_elements_crumble_v01` from 1.8 s: the four shapes burst apart | Earth, air, fire and water aren't elements. |
| 2.5–6 | `04_iron_salt_flame_air_v01`: a nail, a heap of salt and a candle flame | For two thousand years, people said everything was made of those four. |
| 6–9 | `10_rock_not_fire_v01`: a dark rock on a balance, heat shimmering off it | But heat a rock, and it doesn't turn into fire. |
| 9–14 | **title on screen:** *How Did We Discover the Periodic Table?* | |
| 9–12 | `02_workshop_jars_v01`: shelves of jars, smoke drifting through the room | Air is a mixture, not one thing. |
| 13–15.7 | **`lavoisier_list` t1 (Vertex Quality mint), 0.1–2.77 s only:** Lavoisier in wig, dark coat and cravat at a bench with retorts and a brass balance, writing a list (page unreadable). Both takes put a lit candle on the back shelf from ~3 s, so only the clean head is used | Antoine Lavoisier threw out the four, |
| 15.7–18.7 | `08_labelled_zoo_v01`: labelled jars along the shelf | and listed only what couldn't be broken down. |
| 18–22.5 | `07_shelf_names_grow_v01`: the shelf of named jars keeps growing | His list had thirty-three. Two were light and heat. |
| 22.5–25 | back to `03_four_elements_crumble_v01` from 1.8 s (loop) | |

**Script (59 words):**

Earth, air, fire and water aren't elements. For two thousand years, people said everything was made of those four. But heat a rock, and it doesn't turn into fire. Air is a mixture, not one thing. Antoine Lavoisier threw out the four, and listed only what couldn't be broken down. His list had thirty-three. Two were light and heat.

At 150–155 wpm, 59 words run about 23 s, then the loop tail.

*Fact check:*
- The four elements: Empedocles (5th century BC), then Aristotle. They were the standard account until the 1700s, so "two thousand years" is honest rounding.
- "Heat a rock and it does not become fire" and "the atmosphere in the room is not one element. It is a mixture" are the film's own lines (Part 01).
- Lavoisier showed air is a mixture (oxygen and "azote", nitrogen) in the 1770s. In his *Traité élémentaire de chimie* (1789) he lists 33 "simple substances", things that couldn't be broken down with the tools of the day. *Light* (lumière) and *caloric* (heat) are on the list. The film says he "threw out the four-element comfort and wrote a list of simple substances"; the 33 and "light and heat" are the hard fact the film doesn't give.

**Plates (Part 01 locked in `hos_002_part01_rough_v14.mp4`, plus the Lavoisier mint):**

| Plate | File (`04_Generated-Clips/part01/raw/v01_fast/`) | sha256 |
|---|---|---|
| 03_four_elements_crumble | `03_four_elements_crumble_v01.mp4` | `57618639…` |
| 04_iron_salt_flame_air | `04_iron_salt_flame_air_v01.mp4` | `a0bc722b…` |
| 10_rock_not_fire | `10_rock_not_fire_v01.mp4` (the v14 soft-grade) | `053c5999…` |
| 02_workshop_jars | `02_workshop_jars_v01.mp4` | `52689953…` |
| lavoisier_list | `04_Generated-Clips/shorts_backcat/raw/lavoisier_list_tN.mp4` (Vertex `veo-3.1-generate-001`) | in the mint log and the index |
| 07_shelf_names_grow | `07_shelf_names_grow_v01.mp4` | `9817941e…` |

**Weak spot (resolved in v02, Claude took option 2):** there is no real-motion plate of Lavoisier himself; Part 02's Lavoisier plate is Ken Burns. The picture shows a labelled shelf while the VO names him, so his name rides on the caption only. If that's not good enough, the options are a Vertex Quality mint of one Lavoisier plate (about 8 s; credit allowed to £0) or a different fallback.
