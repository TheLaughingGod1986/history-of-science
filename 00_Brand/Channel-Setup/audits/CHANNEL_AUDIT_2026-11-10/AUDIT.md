# History of Science — full channel audit and action plan (10 Nov 2026)

Asked by Ben, 10 Nov 2026: *"History of Science has been performing quite badly lately… do a full audit, understand what's worked and what hasn't, put together an action plan."*

**Sources.**
- Public view counts for all 6 public longs and 28 public Shorts, read 10 Nov 2026 through vidIQ's public channel data.
- Owner analytics from the 7 Nov weekly audit (`02_Video-Projects/_analytics/HOS_2026-11-07.md` and its evidence file): Studio CTR, impressions, stayed-to-watch, traffic sources.
- The live thumbnails.
- `HOS_STRATEGY.md`, `docs/RETENTION_LEARNINGS.md` and the desk.

**Limits.** vidIQ is authorised only for Orbit With Ben, so I could not pull HOS owner analytics (CTR, impressions, retention) for after 7 Nov. Every owner figure here comes from the 7 Nov audit. Nothing was changed on YouTube.

---

## 1. The short version

1. **The long films are the problem, not the Shorts.** The six public longs have about 211 views between them, and 76% of those are one film (002, Periodic Table, 161). The two newest longs have 5 views (005, 12 days old) and 2 views (006, 5 days old). YouTube is barely showing them: 004 had 811 impressions in three weeks at 1.1% CTR.
2. **The newest long titles hide the subject.** *The Tied Arm That Proved Your Blood Circulates* and *The Willow Tree That Was Made of Air* are story titles. Nobody searches for them, and YouTube can't match them to the big videos on blood circulation or photosynthesis. The only long that works, 002, has a plain searchable title and earns its views as a suggested video next to TED-Ed's Mendeleev video.
3. **The Shorts that work are plain-English curiosity, not history.** The channel's best video by far is *What happens if you keep cutting gold in half?* (1,226 views, more than all six longs together, five times over). No name, no date, no "discovered". The worst Shorts are insider statements: *What other table has empty chairs?* (4), *The first X-ray showed a wedding ring* (9), *Gallium sat where the table said* (16).
4. **"Lately" is mostly one outlier wearing off, plus two weak longs.** October was 4.7× September (2,769 vs 588 views), but the gold Short alone was about 40% of that. Take it out and the channel is flat at roughly 50–80 views a day. The 7 days to 4 Nov were down 15% on the week before.
5. **Shorts don't feed the longs.** Shorts were 98% of views over 28 days, and Shorts-to-long Related clicks were **2**. The funnel the strategy relies on isn't working at this size, so the longs have to find viewers on their own, through search and suggested.
6. **All thumbnails look alike.** Every long thumbnail is the same library, the same boy at lower left, the same gold serif and one glowing object. Side by side they read as one video. At 1–3% CTR, that sameness costs clicks. The cartoon child may also make browsers think the channel is for kids.
7. **Most of the effort goes into process, not reach.** In the last week the desk spent days on runner safety, capability rechecks (one loop ran 5+ times with nothing changing) and gate reviews. Almost none went on titles, thumbnails or topic choice, which are the levers that move views at 6 subscribers.

---

## 2. What has worked (do more of this)

| Video | Views | Why it worked |
|---|---:|---|
| Short *What happens if you keep cutting gold in half?* (`29bpGAI0wb8`) | 1,226 | A thought experiment anyone can picture. No person, no date. The title is the question everybody has. Fed by the Shorts feed. |
| Short *Are Marie Curie's Notebooks Still Radioactive?* (`AMSriTQ-lcQ`) | 274 | A creepy, true, present-tense fact about a famous name. 78.6% average viewed. Stayed-to-watch was only 21.7% because frame 0 showed a dark lab, not the notebooks. |
| Short *How Did John Snow Stop Cholera?* (`OnJ8MFu0Mi0`) | 231 | A famous name plus a mystery, and 8 likes, the best like rate. |
| Short *One Tight Band Proved Your Blood Goes Round* (`PFj6172YU4Q`) | 214 in 2 days | About 4 views an hour, the fastest start since the gold Short. A body you own plus a visible action (the tourniquet). |
| Short *How Was Phosphorus Discovered?* (`oKqmnJNGiHg`) | 182 | A search title, and the story (a man boiling urine) is gross and memorable. |
| Short *What Is the Pasteur Swan Neck Flask Experiment?* (`-3L6HzJ_d_4`) | 117 | 91% of views from search, and the channel's best stayed-to-watch (73%). Exactly the words a student types. |
| Long *How Did We Discover the Periodic Table?* (`AL_-qlWko_g`) | 161 | A plain searchable subject, sitting beside TED-Ed's Mendeleev video (55.6% suggested). 3.4% CTR, the best of the longs. |

**The pattern:** say the familiar thing in plain words (gold, blood, notebooks, cholera, a flask), and either ask the question a curious person or a student already has, or state a true fact that sounds impossible. Show that thing at frame 0.

## 3. What hasn't worked (stop doing this)

| Pattern | Examples (views) | Why |
|---|---|---|
| Insider statements that need context | *What other table has empty chairs?* (4) · *Gallium sat where the table said* (16) · *Why tellurium sat before iodine* (32) · *He said every eighth element repeats* (62) | You have to already know the story to care. Nothing to search, nothing to wonder about. |
| Runs of 4–6 Shorts on one film's niche | Periodic table, 18–22 Sep: 4–34 each · X-rays, 25–27 Sep: 9–40 each | The same topic on back-to-back days, and each one less interesting than the last. |
| Story titles on longs | 005 *The Tied Arm That Proved Your Blood Circulates* (5) · 006 *The Willow Tree That Was Made of Air* (2) | No searchable subject noun, so neither search nor suggested can place them. |
| Generic "How Did We Discover X?" on crowded topics | 001 Germs (7) · 003 X-rays (5) | Searchable, but the big channels own those exact searches. A sharper angle does better (the swan-neck Short got 91% of its views from search). |
| Vague hook words | *The Four Elements Were Wrong* (34) · *One Tight Band* as a long thumbnail | "Wrong" about what? "Band" of what? Fine as a story beat, weak as packaging. |
| Look-alike thumbnails | All 6 longs | Same room, same boy, same palette. Nothing tells you this film is different from the last one. |

---

## 4. Action plan

The order is by impact for the effort. Every live change below needs Ben's OK first: thumbnails are his under AGENTS.md, and so is the call to stop a running Test & Compare. Titles go through `07_Content-Ops/scripts/retitle-videos.ts --dry-run` and the `public_search.py` / `neighbours.py` evidence first.

### A. This week: repackage the live longs (no spend)

Proposed retitles. Each puts the searchable subject first and keeps the story in the thumbnail:

| Film | Now | Proposed title | Why |
|---|---|---|---|
| 006 `VbPubYd6Fbs` | The Willow Tree That Was Made of Air | **Where Does a Tree's Mass Come From?** | One of science's best-known questions, with millions-view neighbours. It matches the film's own pinned comment. |
| 005 `wwcjcFfC-5M` | The Tied Arm That Proved Your Blood Circulates | **How Did William Harvey Discover Blood Circulation?** | The exact school-search phrase, plus the name. |
| 001 `_C92tIJCk8A` | How Did We Discover Germs? | **Pasteur's Swan Neck Flask: How We Discovered Germs** | Reuses the phrase that gets the swan-neck Short 91% of its views from search. |
| 003 `frP_YrNShsU` | How Did We Discover X-rays? | **How Röntgen Discovered X-Rays by Accident** | Name plus "by accident" is the stronger hook. Leaves the generic search to the big channels. |
| 002 `AL_-qlWko_g` | (keep) | — | It works. Don't touch it. |
| 004 `GHZDsiH7L7A` | (keep for now) | — | Its Test & Compare is still running. Revisit at 1,000 test impressions. |

- **Stop the Test & Compare on 005 and 006.** At 7 impressions or fewer they will never reach a result, and they block the retitle. That's Ben's call.
- **Descriptions:** open on the answer in the searched words. For example: "Trees get almost all their mass from the air, not the soil. In 1648, Jan van Helmont…" Then chapters, then sources (the existing rule, kept).
- **Measure at 14 days:** impressions and CTR against the 7 Nov figures. Keep a change if impressions or CTR improve; roll it back if both fall.

### B. Next 2 weeks: thumbnails that don't look alike

- One thumbnail test (Ben approves). On 005 or 006, make a version with **no Explorer**: the hero object large, a bright accent colour unique to that film, 2–3 words. Run it as Test & Compare against the current one once the new title is live.
- If it wins, drop the Explorer from long thumbnails and keep him inside the films. If it loses, keep the house look and vary the background colour and setting per film, so the six stop looking like one video.

### C. Shorts: copy the winners

1. **One "What happens if…?" Short a week**, built on the gold-in-half template: a thought experiment shown, no name or date in the first 3 s, and the history arrives as the answer. Candidates from films already made: "What happens if you seal soup in a flask?" (001), "What happens if you put mint in a sealed jar?" (006), "What happens if you fly a kite in a lightning storm?" (008).
2. **Title every Short as either a plain question a student types** ("How was X discovered?", "What is the X experiment?") **or one impossible-sounding true fact** ("Marie Curie's notebooks are still radioactive"). Never an insider statement.
3. **Never more than 2 Shorts in a row on one film.** Spread them across films. This tightens the existing R2 rule from 6 to 2.
4. **Frame 0 shows the titled object.** This rule is already written and still being missed (the Curie notebooks, the wrist on the heart Short). Make it a hard gate.
5. **Cheap retitle test on 3 dead Shorts** (no re-upload, which is allowed):
   - `CnHwX1L9XHg` *Gallium sat where the table said* → **This Metal Melts in Your Hand**
   - `nFQRWmpulTQ` *He predicted a metal before it was found* → **How Mendeleev Predicted an Element Nobody Had Seen**
   - `zI_eD3vFWmE` *The first X-ray showed a wedding ring* → **The First X-Ray Ever Taken**

   Read them at 7 days. If any revives, retitle the rest of the September Shorts.

### D. Long-film topics and titles from 009 on

- **The title is the question people search, with the subject noun up front.** 009 *Why Doesn't the Moon Fall to Earth?* and 010 *What Killed the Dinosaurs?* already fit. Keep the story phrasing for the thumbnail and the opening line.
- **Check the title against search before the voiceover is locked,** not after. `public_search.py` and `neighbours.py` already exist. Add one test: the title contains the subject noun the neighbour videos use.
- Keep films 7–9 minutes, and keep the proof-first opening test (HOS-2026-11-E2).

### E. Process: spend the effort where the views are

- **Cut the recheck loops.** Ben's rule of 3 Nov ("no endless unchanged rechecks") should be enforced by the relay. A capability hold rechecks once a day at most, and after two unchanged checks it goes to Ben's watch.
- **A weekly 30-minute packaging review on the desk:** last week's titles, thumbnails, CTR and impressions; one change to test next week. This is the cheapest lever and it currently has no owner. Proposed owner: Claude (listings), with the Chief signing off.
- **Connect HOS to vidIQ** (Ben: vidIQ, then authorise the HOS channel). Then owner analytics such as CTR, impressions and retention can be read on demand instead of waiting for the weekly job.

---

## 5. What not to change

- The 22–27 s Shorts length, the loop ending, captions all the way through, and the 9–14 s title. The re-cuts already lifted average viewed to 78–115%.
- 002's title and thumbnail.
- Nothing public is re-uploaded or replaced. A weak upload is a result.
- The house look inside the films. Only the packaging changes.

## 6. How we'll know it's working (read on 24 Nov and 8 Dec)

| Measure | Now (7 Nov) | Target by 8 Dec |
|---|---|---|
| Long impressions, 7-day, all longs | about 50 (002 + 004; 005 and 006 near zero) | 500+ |
| Long CTR | 1.1–3.4% | 4%+ on the retitled films |
| Views per long, at 14 days | 2–31 | 100+ |
| Shorts over 150 views, per week | about 1 | 2+ |
| Subscribers | 6 | 25 |
