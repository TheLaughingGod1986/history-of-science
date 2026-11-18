# HOS 106 — Topic brief and data learnings (`J2835` & `J2836`, 14 Nov 2026)

| Field | Value |
|---|---|
| **Film** | `HOS:106`, `02_Video-Projects/106_Aristotle-Freud-Schmidt-Eels-Sargasso` |
| **Working title (`0` collisions, Rule 15 & Rule 26)** | **Where Do Eels Come From? (The Sargasso Sea Hunt)** (`48` characters, `0` exact title collisions in `public_search.py`) |
| **Original `J2835` working title** | *Where Do Eels Come From? (The 2,000-Year Mystery)* (`49` characters; punctuation-only collision with `Creature Code` `mgRlVeTSSMA` `8` views *Where Do Eels Come From? The 2,000-Year Mystery* — disambiguated above to `(The Sargasso Sea Hunt)`) |
| **Other titles to test (`0` collisions)** | **Title B (`Rule 26 + Rule 23`, `51` chars):** *How Do Eels Reproduce? (The 1922 Sargasso Sea Hunt)* (disambiguated from *How Do Eels Reproduce? (Nobody Has Ever Seen It)* which collided with `CuriosityFact` `_BWQLJJ3GcM` `2` views) · **Title C (Story T&C arm, `39` chars):** *The Fish That Freud Dissected 400 Times* (`0` collisions) |
| **Search phrases (rule 26)** | `"where do eels come from"` (`autocomplete = yes`, `5` suggestions), `"how do eels reproduce"` (`autocomplete = yes`, `7` suggestions), `"eel migration"` (`autocomplete = yes`, `9` suggestions), `"sargasso sea eels"` (`autocomplete = yes`, `1` suggestion) |
| **Hook (UNVERIFIED working note)** | For two thousand years nobody could find a baby eel or an eel's eggs; the hunt ran from Aristotle's mud, through a 19-year-old Sigmund Freud cutting open hundreds of eels in Trieste, to a Danish research ship towing nets across the Atlantic to the Sargasso Sea, and no one has yet watched them breed in the wild. |
| **Rule-E Review Verdict (`J2836`)** | **GO (`94 / 100` · `9.40 / 10` Opportunity Score)** — Pre-cleared in `jobs/WIP.json` `next_hos` under Rule G (`4/4` active HOS slots full). |
| **Status & Claim Guard** | Proposal only in `jobs/WIP.json` `next_hos` (Rule G). **Every name, date, and number in Section 2 is UNVERIFIED (`written from memory`) and needs an exact primary-source quote in `SOURCES.md` verified by the `facts` lane (`gemini-agy`) before any script lock, VO, or picture spend.** No script, voice, picture, or Studio work started. |
| **Spend** | `£0.00` |

## 1. What our own data says (snapshot 14 Nov 2026; Studio CTR read 12 Nov 2026)

Channel: 6 subscribers, 3,888 views, 36 videos. Last 28 days: Shorts get 77% of their views from the Shorts feed and 22% from YouTube search; longs get 45% from Suggested and 25% from search (55 views).

**Longs, by views per day since publish**

| Film | Title | Views | Views/day | Impressions | CTR | Avg % viewed |
|---|---|---:|---:|---:|---:|---:|
| 002 | How Did We Discover the Periodic Table? | 161 | 2.80 | 1,141 | 3.4% | 21.6% |
| 007 | How Was the First Vaccine Made? (And Why It's Named After a Cow) | 3 | 1.95 (1.5 days old) | not read yet | not read yet | not read yet (`UNKNOWN` at `<10` views) |
| 006 | The Willow Tree That Was Made of Air | 10 | 1.17 | 22 | 0% | 100% (one viewer, `UNKNOWN`) |
| 004 | What's Inside an Atom? Mostly Empty Space | 33 | 1.12 | 816 | 1.2% | 20.9% |
| 005 | The Tied Arm That Proved Your Blood Circulates | 5 | 0.32 | 14 | 21.4% (3 clicks) | 9.2% (`UNKNOWN` at `<10` views) |
| 003 | How Did We Discover X-rays? | 5 | 0.10 | 41 | 2.4% | 26.7% (`UNKNOWN` at `<10` views) |
| 001 | How Did We Discover Germs? | 7 | 0.10 | 44 | 6.8% | 48.1% (`UNKNOWN` at `<10` views) |

- **3 best longs:** 002 Periodic Table (161 views, 2.80/day, 1,141 impressions), 004 Atom (33 views, 816 impressions), 007 Vaccine (fastest start of any long, but only 1.5 days of data). What they share (hypothesis to test): a plain question a student types, about a subject that big school lessons already cover (002 gets most of its views as a Suggested video beside TED-Ed's Mendeleev film), 8:45 to 9:01 long.
- **3 worst longs:** 003 X-rays and 001 Germs (0.10/day each) and 005 Tied Arm (0.32/day, 9.2% viewed, 14 impressions). What they share: 005 and 006 carry story titles nobody searches for, so YouTube showed them 14 and 22 times; 001 and 003 are the two shortest (6:05, 7:06) and never found a neighbour.

**Shorts, by views per day (30 public)**

| Short | Views | Views/day | Avg % viewed | Stayed |
|---|---:|---:|---:|---:|
| What happens if you keep cutting gold in half? (`29bpGAI0wb8`) | 1,227 | 42.5 | 44.1% | 40.8% |
| One Tight Band Proved Your Blood Goes Round (`PFj6172YU4Q`) | 216 | 37.2 | 61.1% | 15.2% |
| Are Marie Curie's Notebooks Still Radioactive? (`AMSriTQ-lcQ`) | 274 | 16.3 | 76.9% | 22.7% |
| How Did John Snow Stop Cholera? (`OnJ8MFu0Mi0`) | 231 | 12.3 | 65.7% | 29.6% |
| ... | | | | |
| Gallium sat where the table said | 16 | 0.29 | 33.5% | 30.4% |
| The first X-ray showed a wedding ring | 9 | 0.19 | 64.0% | 50.0% |
| What other table has empty chairs? | 4 | 0.08 | 23.1% | 33.3% |

- **3 best Shorts** share: a question in the title that names an everyday thing or a famous person (gold, Curie, John Snow), and an answer you can picture. Best "stayed": *What Is the Pasteur Swan Neck Flask Experiment?* (`-3L6HzJ_d_4`) at 76.5%.
- **3 worst Shorts** share: a statement or teaser title that only makes sense after watching the long (0.08 to 0.29 views a day).

**What this means for a new topic:** a search-led question about something the viewer has seen or eaten (LEARNINGS rules 1, 26, 28, 31), with big education videos already on the subject (the neighbour rule), told through a person, a date and a twist.

## 2. The film (UNVERIFIED working notes — require `SOURCES.md` exact quotes before script lock)

- **People and dates (all to be sourced in `SOURCES.md` before any script lock; written from memory here, UNVERIFIED):** Aristotle (4th century BC, *Historia Animalium*) concluded eels grow spontaneously from mud ("earth's guts") because no eel he cut open held eggs or milt. In 1876 Sigmund Freud, a 19-year-old medical student at Carl Claus's zoological station in Trieste, dissected about 400 European eels looking for the male organs (testes of Syrski) and found nothing certain. In 1896 Giovanni Battista Grassi and Salvatore Calandruccio in Sicily showed in an aquarium that a transparent leaf-shaped marine creature (*Leptocephalus brevirostris*, previously classified as a separate species) metamorphosed into a glass eel. From 1904 to 1922 Danish biologist Johannes Schmidt towed fine plankton nets across the Atlantic (aboard the *Thor* and *Dana*), mapping ever smaller larvae (`45 mm → 25 mm → <10 mm`) westward until in 1922 he pinpointed the Sargasso Sea as the spawning ground.
- **Twist (UNVERIFIED):** Schmidt never saw an adult eel spawn in the Sargasso Sea or recovered fertilised eggs in the wild. Only in 2022 were adult European eels tracked all the way into the Sargasso Sea by satellite pop-up archival tags (Wright et al., *Scientific Reports* 2022), and still nobody has filmed eels spawning in the wild.

### Why it should work

- Resembles our best performers: a question title about a named everyday creature, like the gold Short (1,227 views, 42.5/day) and *How Did John Snow Stop Cholera?* (231 views, 12.3/day); a famous name in an unexpected place (Sigmund Freud dissecting 400 eels), like *Are Marie Curie's Notebooks Still Radioactive?* (274 views, 16.3/day, 76.9% viewed).
- Search-led title with a bracketed tail, the shape of our fastest-starting long, 007 Vaccine (1.95 views/day on day 2), and of 002 Periodic Table (161 views, 3.4% CTR).
- LEARNINGS rules followed: 1 (positive question naming the subject), 15 and 23 (stakes in a bracketed tail, `48` chars `≤50` chars), 26 (search phrase first), 28 (Shorts as curriculum/famous-scientist questions), 10 and 30 (concrete physical proof first: `0:05–0:15` Freud's Trieste dissection tray with a split eel showing zero eggs/testes, followed by Grassi's transparent leaf-larva tank and Schmidt's Sargasso plankton-net larval size map).

### Public search & autocomplete check (`public_search.py`, YouTube GB signed out, 14 Nov 2026; raw pull in `11_Upload-Package/evidence_2026-11-14_public_search.json`)

| Phrase / Candidate Title | Autocomplete? | Top results (GB, 14 Nov 2026) | Collision Check |
|---|---|---|---|
| `where do eels come from` | **yes** (`5` suggestions) | Bizarre Beasts `1,594,707` (`acEIGorImGs`) · Atomic Frontier `365,534` (`y0UIJekwyPY`) · TED-Ed `1,157,605` (`BR1enXROmgA`) · Auralis `1,629,143` (`LxNq8zOEbM8`) · MinuteEarth `569,775` (`DQVUuBQtb7w`) | Search phrase (Rule 26a) |
| `how do eels reproduce` | **yes** (`7` suggestions) | TED-Ed `2,751,342` (`RFi6ISTjkR4`) · Bizarre Beasts `1,594,707` (`acEIGorImGs`) · Thoughty2 `3,317,475` (`k61Bk63EvTM`) · Atomic Frontier `365,534` (`y0UIJekwyPY`) · TED-Ed `1,157,605` (`BR1enXROmgA`) | Search phrase (Rule 26a) |
| `eel migration` | **yes** (`9` suggestions) | TED-Ed `1,157,608` (`BR1enXROmgA`) · Auralis `1,629,141` (`LxNq8zOEbM8`) · Bizarre Beasts `1,594,707` (`acEIGorImGs`) · Discovery UK `114,189` (`RgHkWGX_9ZI`) · ZSL `93,645` (`WBRnNk_uo9Y`) | Search phrase (Rule 26a) |
| `sargasso sea eels` | **yes** (`1` suggestion) | acapellascience `175,206` · Discovery UK `114,189` · Auralis `1,629,143` · Bizarre Beasts `1,594,707` | Search phrase |
| `Where Do Eels Come From? (The Sargasso Sea Hunt)` | related (`eel migration sargasso sea`) | Bizarre Beasts `1,594,709` · WowScience `66` · Untamed Animal Facts `1,209` · MinuteEarth `569,777` · TED-Ed `1,157,611` | **`0` collisions (Primary Title A, `48` chars)** |
| `Where Do Eels Come From? (The 2,000-Year Mystery)` | related | Creature Code `8` (`mgRlVeTSSMA`: *Where Do Eels Come From? The 2,000-Year Mystery*) · Bizarre Beasts `1,594,707` · Riddle & Record `10` | **Punctuation collision (`mgRlVeTSSMA`) — disambiguated to Title A above** |
| `How Do Eels Reproduce? (The 1922 Sargasso Sea Hunt)` | related | Bizarre Beasts `1,594,709` · Thoughty2 `3,317,476` · The Earth and Alien `1` · OctoLab `1,365` · Deep Sea Lab `668` | **`0` collisions (Title B, `51` chars)** |
| `The Fish That Freud Dissected 400 Times` | no | calvintheninja `47,374` · VILEMasterShake `13,938` · Animal Oddballs `81` · The Origin Vault `66,928` · Fish Journeys `255` | **`0` collisions (Title C, `39` chars)** |
| `Why Did Sigmund Freud Dissect 400 Eels?` | related | calvintheninja `47,374` · VILEMasterShake `13,938` · Animal Oddballs `80` · showselectordog `3,451,018` · Hannah Fry `62,190` | **`0` collisions (Short `S01`, `39` chars)** |
| `Has Anyone Ever Seen an Eel Lay Eggs?` | no | Bizarre Beasts `1,594,707` · Never Filmed `57` · Pokato_1 `9` · TED-Ed `2,751,342` · Nescium `382` | **`0` collisions (Short `S02`, `37` chars)** |

### Neighbour pass (`neighbours.py`, YouTube GB signed out, 14 Nov 2026; raw pull in `11_Upload-Package/evidence_2026-11-14_neighbours.json`)

| Channel | Video | Views | Source |
|---|---|---:|---|
| TED-Ed ★ | No one can figure out how eels have sex - Lucy Cooke (`RFi6ISTjkR4`) | 2,751,342 | `neighbours.py` (Tier 1) + `public_search.py` |
| TED-Ed ★ | Eli the eel: A mysterious migration - James Prosek (`BR1enXROmgA`) | 1,157,611 | `neighbours.py` (Tier 1) + `public_search.py` |
| Thoughty2 | Why Nobody Knows How Eels Reproduce (`k61Bk63EvTM`) | 3,317,475 | `neighbours.py` (Tier 2) + `public_search.py` |
| Bizarre Beasts (Complexly / Hank Green) | We Finally Know Where Eels Come From (`acEIGorImGs`) | 1,594,707 | `public_search.py` (#1 result for `"where do eels come from"`) |
| Auralis | Eels Shouldn't Be Able To Exist... (`LxNq8zOEbM8`) | 1,629,143 | `public_search.py` |
| MinuteEarth | Why We Haven't Learned More In 101 Years Of Trying (`DQVUuBQtb7w`) | 569,775 | `public_search.py` (Tier 2) |

`neighbours.py` gate: **PASS** (`bigCount = 3` videos over 1M in `neighbours.py`, two of them Tier-1 `TED-Ed`, plus `Bizarre Beasts` `1.59M` and `Auralis` `1.63M` in `public_search.py`). Subject words to share: `"eels"`, `"how eels"`, `"the eel"`, `"reproduce"`, `"migration"`, `"sargasso"`.

### Two Short angles (`0` collisions)

1. **Why Did Sigmund Freud Dissect 400 Eels?** (`39` chars, `0` collisions) — The famous name, the 1876 Trieste laboratory dissection tray (`0.0 s` Frame-0 hero object), and the male organ he could not prove.
2. **Has Anyone Ever Seen an Eel Lay Eggs?** (`37` chars, `0` collisions) — Frame 0 on the transparent leaf-like *Leptocephalus* larva / Sargasso plankton net; the answer is no, with the 1922 larval size map and 2022 satellite tags as the payoff (`≥70%` runtime).

## 3. Rule-E Review Rulings (`J2836`, 14 Nov 2026)

- **Open point 1 — Does Thoughty2 count as the third education neighbour? YES (`PASS`).** `Thoughty2` (`k61Bk63EvTM`, `3,317,475` views) is explicitly in `00_Brand/Channel-Setup/tools/neighbours.py` `TIER2` (line 49), and `HOS:106` already has **two direct Tier-1 `TED-Ed` lessons over `1M` views** (`RFi6ISTjkR4` at `2.75M` and `BR1enXROmgA` at `1.16M`). Moreover, `public_search.py` confirms a fourth `≥1M` science-education video on the exact phrase `"where do eels come from"`: **Bizarre Beasts** (`acEIGorImGs`, *We Finally Know Where Eels Come From*, **`1,594,707` views**, Complexly's biology education channel alongside SciShow/CrashCourse), plus **MinuteEarth** (`DQVUuBQtb7w`, **`569,775` views**).
- **Open point 2 — `public_search.py` autocomplete & title-collision evidence:** Gathered and saved in `11_Upload-Package/evidence_2026-11-14_public_search.json`. Caught punctuation-only collisions on *Where Do Eels Come From? (The 2,000-Year Mystery)* (`mgRlVeTSSMA`, `8` views) and *How Do Eels Reproduce? (Nobody Has Ever Seen It)* (`_BWQLJJ3GcM`, `2` views) and disambiguated to `0`-collision primary Title A **`Where Do Eels Come From? (The Sargasso Sea Hunt)`** (`48` chars) and Title B **`How Do Eels Reproduce? (The 1922 Sargasso Sea Hunt)`** (`51` chars).
- **Open point 3 — Unverified claims guard:** Every name, date, and number in Section 2 remains marked **UNVERIFIED** until an active HOS WIP slot opens under Rule G and `SOURCES.md` + the `facts` lane verify every claim from primary sources (Aristotle *Historia Animalium* VI.16, Freud 1877 *Sitzungsber. Akad. Wiss. Wien*, Grassi & Calandruccio 1896/1897 *Proc. R. Soc. Lond.*, Schmidt 1922 *Phil. Trans. R. Soc. B*, Wright et al. 2022 *Sci. Rep.*).
- **Non-duplication:** Verified zero overlap across `02_Video-Projects/000–105`, `00_Brand/Channel-Setup/ideas/011–095` & `IDEAS_*.md`, `VIDEO_BACKLOG.json`, and `jobs/WIP.json`.
