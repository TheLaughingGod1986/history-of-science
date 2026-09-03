# Last three Shorts — craft + distribution audit

**Date:** Tuesday 1 Sep 2026, ~15:45 UK  
**Live channel:** Orbit with Ben (`@OrbitWithBen` · `UC_esArsDKd3GJvOkeO0DUog`)  
**Not this:** `@HistoryOfScienceYT` is still empty. These three did **not** go to the new HOS Brand Account.

**What was audited:** the three Shorts that went public together today at **13:39–13:40 UTC** (14:39–14:40 UK). Downloaded the mp4s, pulled frames at 0.2s / 1s / 2.5s / 9s / 14s / last 4s / last frame, compared VO captions, listings, and cadence against the locked punch-first bar and against the two cluster leaders.

**Data this run**

| Source | What we got | Confidence |
|--------|-------------|------------|
| YouTube RSS + watch pages | views, likes, duration, publish time, description, tags | **HIGH** |
| Downloaded 9:16 mp4s + ffmpeg frames | open / mid / end picture, burn-in captions, CTA | **HIGH** |
| Auto captions of VO | spoken line vs on-screen vs title | **HIGH** |
| YouTube Analytics (impressions, 3s hooked, AVD %, swipe) | **not pulled** — no Studio/API analytics this run | — |
| vidIQ scores | **not pulled** — vidIQ MCP not in this environment | — |

Raw downloads: `/tmp/hos_shorts_audit/` (local only, not committed).

---

## Executive verdict

They are underperforming because **three near-duplicate Last Star teasers were dumped at the same second, five days late, on pictures that do not show the line.** That is a distribution and craft failure, not a “Shorts are dead” signal.

The same cluster already has a working Short: **The Universe Is Running Out of New Stars** (`DN4L1DkerMM`, **226 views**, 26 Aug). Three Suns (`MDvAKtmKauw`, **142 views**) is still the diamond-bar pattern. Today’s three violate that pattern on purpose-built checks the rules already name: **no batch-dump, one idea, VO-literal picture, punch in 0–1s, loop the open into the last 4s.**

Age caveat: these cuts are **~2 hours old**. 226 views on a 6-day Short is not a fair league table. **0 views on a public 26s Short after two hours** (`KX-XU_AODoI`) is still pathological. A healthy first-hour Short on this channel has historically found *some* Shorts-feed impressions. Dump + duplicate + long-title VO is enough to explain a dead start.

Do **not** recut the whole catalogue. Do **not** ship more Last Star Shorts this week. Fix ops so HOS Germs cannot repeat this.

---

## The three (live, 1 Sep 2026 ~15:45 UK)

| # | ID | Title | Dur | Views | Likes | Published |
|---|----|-------|----:|------:|------:|-----------|
| 1 | [`CkSECfUfH2Y`](https://www.youtube.com/shorts/CkSECfUfH2Y) | The Sky Is Already Running Out of Light | 26s | **14** | 1 | 13:39:57 UTC |
| 2 | [`KX-XU_AODoI`](https://www.youtube.com/shorts/KX-XU_AODoI) | The Day the Last Star Goes Out | 26s | **0** | 0 | 13:40:03 UTC |
| 3 | [`9lLZMy8rBJo`](https://www.youtube.com/shorts/9lLZMy8rBJo) | What Remains After the Last Star Dies? | 26s | **28** | 3 | 13:40:14 UTC |

All three: 1080×1920, 26.0s, descriptions are **only** the long title + `REXYxuLOBoI` URL (no punch first line, no tags in the body). Each has one comment (the full-film pin).

Index still names **dead IDs** from an earlier upload generation:

| Live ID | Stale index ID | Planned air (never happened) |
|---------|----------------|------------------------------|
| `CkSECfUfH2Y` | `SdNXS1PD_Yk` | Thu 27 Aug 20:00 UK |
| `KX-XU_AODoI` | `IVbO9XkkDps` | Fri 28 Aug 11:30 UK |
| `9lLZMy8rBJo` | `xRxhb3vSru4` | Sat 29 Aug 11:30 UK |

They were meant to be **one per day** after Last Star went public (27 Aug 18:00). They went out **five days late, 17 seconds apart.** Locked rule they broke: *“One Short per day max — never dump the cluster.”*

---

## Same cluster, already live (the control group)

| ID | Title | Published | Views now | Why it is the control |
|----|-------|-----------|----------:|------------------------|
| `PV50PX-bE4g` | Most of the Universe Gives Off No Light | 20 Aug | **127** | Concrete image words. Punch in the description. |
| `DN4L1DkerMM` | The Universe Is Running Out of New Stars | 26 Aug | **226** | Best Last Star Short. Named process + hard fact. |
| `wIh3armF7_k` | The Last Star Will Be a Red Dwarf | 27 Aug | **54** | Named object. Open caption “die young” vs red-dwarf marathon. |

`CkSECfUfH2Y` is a **second pass of the same idea as `PV50PX-bE4g`** (index file: `last-star_punch-01_universe-almost-dark_v05_titlecta.mp4`). YouTube is being asked to re-find “the sky is running out of light” after the channel already has two public Shorts that say that.

---

## Why each one fails (watched, not guessed)

Diamond bar used: Three Suns `MDvAKtmKauw` (open = two suns + **“not one sun”**; ~9s = film title on a new shot; last 4s = **same two-sun picture**, still a content line, not a title card).

### 1. `CkSECfUfH2Y` — The Sky Is Already Running Out of Light — **FAIL**

**VO (first line):** “The universe is almost dark. One star is still burning.”  
**Picture (entire 26s):** one **eyeball planet** plate — tan iris storm, cyan “city” lights on the right. That is an Alien Worlds visual, not a last-star sky.

| Gate | Result |
|------|--------|
| Strange picture in 1s | Eyeball world — striking, **wrong film** |
| Punch 0–1.5s | Burn-in is **“almost dark”** — mood, not a fact |
| One VO idea → one literal image | **Mute test fail.** Mute it and it is an eyeball-planet Short |
| Hard fact | Never lands. Poetry: “lonely coal of light”, “night already won” |
| Loop last 4s | Same eyeball wallpaper + yellow film title + “watch the full film →” |
| Unique in the cluster | Duplicate of `PV50PX-bE4g` / `DN4L1DkerMM` |

This is the clearest craft miss of the three. The line names **darkness / one last star**. The picture names **a tidally locked eyeball world**.

### 2. `KX-XU_AODoI` — The Day the Last Star Goes Out — **FAIL (dead start)**

**VO (0:00):** “What happens when the last star dies?” — that is the **parent long’s title**, not a Short of its own.  
**Picture (entire 26s):** one nebula-eclipse plate (dark sphere, orange corona). Pretty. Not “fusion stops.”

| Gate | Result |
|------|--------|
| Punch 0–1.5s | Burn-in **“last star dies?”** = long title, not a new promise |
| Hard fact | “Fusion stops” arrives at **~17s** — past the swipe |
| Assess | “quieter and stranger”, “furnace runs out of options” — metaphor |
| Loop | Same eclipse for 26s; last 4s become a title card |
| Distribution | **0 public views, 0 likes**, 1 pinned comment |

A Short whose spoken first line is the long’s title reads as a **clip of the film**, not a standalone discovery item. Combined with a same-second dump, that is the likeliest reason this one has **no Shorts-feed start**.

### 3. `9lLZMy8rBJo` — What Remains After the Last Star Dies? — **weakest craft, best of a bad drop**

**VO:** “So what remains after the last star?” then remnants / radiation / “could anything ever start again?”  
**Picture (entire 26s):** one **ringed cratered moon** (Mimas-with-rings). That is not black dwarfs, not black holes, not deep time.

| Gate | Result |
|------|--------|
| Punch 0–1.5s | **“what remains”** — mid-sentence, not a drawable fact |
| Title | Question that restates the long. Soft. |
| Mute test | Ringed moon for 26s. Could sit under any cosmology VO |
| Film title | Present ~9s, but **parked in the bottom UI collision zone** |
| End | Correct CTA copy (“watch the full film →”) on the same still world |
| Signal | 28 views / 3 likes — people who *did* get it marked it, the open did not scale |

This is the only one of the three that found a handful of humans. It is still not the diamond bar. Do not treat 28 views as a format win.

---

## Shared failures (all three)

1. **Batch dump.** 13:39:57, 13:40:03, 13:40:14 UTC. YouTube splits first-hour impressions across siblings. Locked: never dump.
2. **Five days late.** Cluster spacing after the 27 Aug long was the whole point. Dumping on 1 Sep also sat on top of **same-day** filler Short `Q16DKNvq2OY` *Earth, Seen From the Dark* (10:30 UTC, **5 views**, wrong pillar).
3. **One plate per Short.** No cut when the line changes. Wallpaper under clever VO — the Neutron Star Part 02 miss, now on Shorts.
4. **Last 4s is a title card, not a loop.** Diamond bar: first ~3s and last ~4s are the **same strange picture**. These three spend the last 4s on “What Happens When the Last Star Dies?” + “watch the full film →”. That fights rewatch, which is how Shorts get a second pass in the feed.
5. **Descriptions stripped.** Winners lead with the punch sentence, then the film URL. These three are only `Title | Orbit's Cosmic Journey | URL`.
6. **Cannibal titles.** Sky / last star / what remains are three wordings of the parent long, not three different drawable facts (red dwarf vs star-birth ending vs diamond crust).
7. **Index lie.** `orbit-with-ben/.../SHORTS_UPLOAD_INDEX.json` still lists `SdNXS1PD_Yk` / `IVbO9XkkDps` / `xRxhb3vSru4` as scheduled. Mirrors and watchers will follow corpses.
8. **Related pill** on these three does point at Last Star (correct). Same-week fillers do **not**: `Q16DKNvq2OY` (Earth flyby) and `QptlHs1HuYI` (Fermi) scrape as related to Last Star. That is the “never fill a gap with a Short from another pillar” miss.

What they **did** get right (so we do not “fix” the wrong layer):

- Length **26s** (inside 22–27s). Not a 40s problem.
- Captions the whole way, yellow/white lowercase.
- End CTA copy is the locked line (the 226-view Short still burns the raw ID `REXYxuLOBoI` on screen — today’s three are cleaner there).
- Parent URL in the description. Zero `/go/`.
- No Orbit-in-frame-1 violation on these three (scenery first). The failure is **wrong scenery**, not “Orbit was in the open.”

---

## Last 7 days of Shorts (context, not the brief)

The last three are the dump. The week around them is also cold. Do not ignore that.

| Published | Title | Views | Note |
|-----------|-------|------:|------|
| 1 Sep 13:40 | What Remains… | 28 | dump |
| 1 Sep 13:40 | The Day the Last Star Goes Out | 0 | dump · dead |
| 1 Sep 13:39 | Sky Is Already Running Out of Light | 14 | dump · eyeball plate |
| 1 Sep 10:30 | Earth, Seen From the Dark | 5 | **other pillar** in a Last Star week |
| 31 Aug | The Galaxy Should Be Crowded — It's Silent | 4 | Fermi filler |
| 30 Aug | It Rains Glass Sideways… | 6 | Alien Worlds reissue vs 142-view Three Suns |
| 27 Aug | Last Star Will Be a Red Dwarf | 54 | in-cluster, named object |
| 26 Aug | Universe Is Running Out of New Stars | **226** | in-cluster, named process |

Pattern: **in-cluster, named-object Shorts still work.** Off-cluster fillers and same-idea remakes do not.

---

## Immediate actions (Orbit, this week)

**Addendum 1 Sep evening (Ben):** keep a Short a day at 11:30 UK. Thursday morning promotes that afternoon’s film; Fri–Wed Related → previous Thursday. See `ORBIT_DAILY_SHORTS_CADENCE_LOCKED.md`. Wednesday 2 Sep is a *new* Last Star idea (`Star Recycling Isn't Perfect`), not a fourth dump sibling.

Do these in order. Do not dump another Last Star teaser today.

1. **No second Short today.** Tomorrow 11:30 UK is the new Last Star punch (`Star Recycling Isn't Perfect`). Then Thursday morning is Europa’s premiere promo.
2. **Leave `9lLZMy8rBJo` public.** It has the only real engagement of the dump (3 likes). Recutting it now wastes the one signal.
3. **Unpublish `KX-XU_AODoI` after 24h if views stay ~0.** It is the long’s title with a nebula wallpaper. A recut (new ID) is allowed only if the open VO is a **new fact** (“Fusion stops. Gravity wins.”) on a picture of a star going dark — not the film title.
4. **Unpublish or recut `CkSECfUfH2Y`.** Do not leave an eyeball-planet Short in a last-star cluster. If recut: lonely coal of light = **one dim star in a near-black sky**, not a tidally locked world.
5. **Fix Studio Related** on `Q16DKNvq2OY` and `QptlHs1HuYI` to their actual parents (or unpublish them as off-cluster fillers). Last Star week is for Last Star.
6. **Rewrite live IDs** in `orbit-with-ben/02_Video-Projects/005_The-Last-Star-In-The-Universe/10_Shorts/SHORTS_UPLOAD_INDEX.json`. Put old IDs in `historicalDuplicateIds`. Social watchers still read this file.
7. **Do not recut `DN4L1DkerMM` / `PV50PX-bE4g` / `wIh3armF7_k`.** They are the control group.

Studio (Ben, 2 minutes): open each of the three → Analytics → **impressions vs views**, **3-second hooked**, **average percentage viewed**. If impressions are ~0, it is the dump. If impressions exist and hooked % is low, it is the open. Paste those three numbers into this file when you have them; this audit is incomplete without them.

---

## Future Shorts — ship gate (blocking)

Nothing goes public, scheduled, or “just this once” unless every line is **PASS**. This is the plan for Orbit leftovers **and** HOS Germs. Fail = rewrite / regen, not “ship and see.”

### A. Idea (before edit)

| # | Gate | Kill test |
|---|------|-----------|
| A1 | **One new drawable fact** | If you can swap this title with another Short in the cluster and nobody notices, kill it |
| A2 | **Not the long’s title** | First VO line ≠ parent film title |
| A3 | **Mute test written down** | One sentence: “If you mute this, you see ___.” If that sentence is “Orbit/Explorer in space/ward,” rewrite |
| A4 | **Not a remake** | Search the live shelf. Same idea already public → this stays **private reserve** |
| A5 | **Parent long is already public** | No teaser Shorts before the pillar |

### B. Picture + sound (before upload)

| # | Gate | Kill test |
|---|------|-----------|
| B1 | **22–27s** (never ≥40s) | `ffprobe` duration |
| B2 | **Punch in 0–1.5s** | First burn-in is the strongest concrete phrase (`not one sun`, `fusion stops`, `it rains glass`) — not “what remains” |
| B3 | **Picture is the line** | When VO names an object, that object is on screen. Wrong world = regen |
| B4 | **≥1 cut when the idea turns** | One 26s wallpaper plate is a fail unless the VO is one still image on purpose |
| B5 | **Captions the whole Short** | No holes. 1–3 words, yellow/white lowercase, centre — not a sentence covering the subject |
| B6 | **Film title on screen ~9–14s** | Exact live long title, **above** the Shorts UI collision zone (not the bottom 15%) |
| B7 | **Loop** | First ~3s picture **returns** in the last ~4s. CTA may sit small on that picture. Last 4s must not become a title card |
| B8 | **CTA** | Soft `watch the full film →` + description = punch line + parent URL. Zero `/go/` |

### C. Publish (before it leaves private)

| # | Gate | Kill test |
|---|------|-----------|
| C1 | **One Short per day** | Calendar has no sibling within 20 hours. Dump = abort |
| C2 | **Monster hook first** in the cluster | Day-1 evening after the long = strongest fact, not “part 4 of 6” |
| C3 | **Studio Related** → **this** week’s long, exact title | Click the Short in Studio. Pill must show the film, not the previous Short |
| C4 | **Pin** `Full film — {title}: https://www.youtube.com/watch?v={ID}` | |
| C5 | **Cover from a no-mascot frame** | Studio **desktop** custom cover. Never Data API `thumbnails.set`. Never a captioned Orbit/Explorer face |
| C6 | **Description punch-first** | Line 1 = the fact. Then film URL. Tags filled from VidIQ when credits exist |
| C7 | **Index the live ID the same hour** | `SHORTS_UPLOAD_INDEX.json` matches Studio. Old IDs in `historicalDuplicateIds` |
| C8 | **24h read** | If impressions ≈ 0, do not “post two more to help it.” Diagnose. If hooked % is bad, recut the **open** (new ID) |

### D. HOS-only extras (Germs 001 and after)

| # | Gate |
|---|------|
| D1 | Long is public first. Cluster 4–6 Shorts over 7–10 days (cadence lock). Not daily forever |
| D2 | Picture = Part 01 v08 / locked-part style: 3D cartoon, faceless germs, **Explorer every 3–5 scenes not every cut** |
| D3 | Titles: drawable + named subject + wrongness in the line. No series suffix, no `#Shorts` in the title |
| D4 | Do not start Germs Shorts until the long exists as a public ID |

---

## What we are not changing

- Punch-first **22–27s**. The 40s era stays dead.
- Wonder over dread. No fearbait titles even if VidIQ would score them higher.
- One long / week when production is ready. Shorts sell that long; they are not a second channel.
- Recut = **new YouTube ID**. Leave the old live until the remake is public, then unpublish. Do not delete.
- TikTok still paused.
- `@HistoryOfScienceYT` stays empty until Germs (or Ben says otherwise). Do not “rescue” Orbit’s dump by uploading the same files there.

---

## Next production implication

HOS **001 Germs** is still Part 04 UAT. Shorts for that film are **later**, after the long is public. When they are built, run section **A→D** on each file before any `publishAt`. The failure mode today was not “we forgot the rules existed.” It was shipping three reserves at once without the mute test.
