# History of Science — strategy

What to make, the week, the hooks, packaging and how we measure. Set 25 Sep 2026 from `audits/HOS_STUDIO_AUDIT_2026-09-25/AUDIT.md`. It replaces the channel vision, the Shorts cadence lock, the open/out lock (its rules are in `STUDIO_PLAYBOOK.md` §7) and the Animistry and HeyHistorically inspiration locks. Those are in `_archive/` for history.

How to build and ship is `STUDIO_PLAYBOOK.md`. Titles and thumbnails are `THUMBNAIL_AND_TITLE_RULES.md`.

## The channel

| | |
|---|---|
| Name | **History of Science** · `@HistoryOfScienceYT` · `UCXp7HkBIl1LgaznXuZHJyRg` |
| Brand line | How we discovered what we know. |
| Tagline | Discovery. Wonder. Proof. |
| Look | Premium **3D cartoon** (Animistry-class): warm cinematic light, period labs, wards and studies |
| Voice | Ben Orbit Narrator (British), upbeat and clear |
| Side character | **The Explorer**, every 3–5 scenes, never the star (`01_Character/CHARACTER_BIBLE.md`) |
| Audience | Curious people of any age, on a phone. Child-obvious, never childish. |
| Not | Orbit With Ben, the Orbit robot, war or politics history, dread essays, 15-minute lectures |

## The lane

**A familiar thing, and the moment we found out the truth about it.** Germs on your hands. The bones inside you. The table on every classroom wall. The viewer already knows the thing; the film shows the person, the room and the proof that changed what everyone believed.

Every film answers three things by the end: what people believed before, the moment it was proved, and what became possible after.

Inspiration: [Animistry](https://www.youtube.com/@ytAnimistry) for the look and long-form immersion. [HeyHistorically](https://www.youtube.com/@heyhistorically) for Shorts as standalone hooks that feed one long through the Related pill. Steal the craft, not the war topics or the runtimes.

## The week

One long and three Shorts. Never more than one Short a day.

| Day (UK) | Type | Job |
|---|---|---|
| Thu 18:00 | Long, 7–9 min | The new film, **normal publish, not a Premiere** |
| Fri 11:30 | Short | Promotes the new long (now public, so Related can point at it) |
| Sun 11:30 | Short | Promotes a different film already out |
| Tue 11:30 | Short | Promotes a third film |

- A Short never goes out before the long it promotes is public.
- Each Short points at the film it is about, through Studio Related. The week is spread across films, not five Shorts on one film in five days.
- Films that already won stay in the rotation.
- No Premieres until subscribers are in the hundreds. All three HOS longs premiered; Germs has 4 views after three weeks. Orbit saw 0 views in a Premiere's first hour.
- A finished film beats a rushed one. If a film isn't ready by Thursday, the week runs on three back-catalogue Shorts.

## Short hook (22–27 s)

Two lines, then one hard fact. No greeting, no build-up.

**Line 1 (5–7 words)** is the surprising truth about a familiar thing, spoken in the first second: *"Your hands were killing patients."* *"You can see through your own hand."*

**Line 2** is the stay line: the person or moment that proved it. *"One doctor washed them, and the dying stopped."*

### The first two seconds

Your two best Shorts already do this: *Microbes in a drop of pond water* (110 views) and *Germs don't cast a shadow* (78) open on the thing itself, moving. The two worst open on blank cards and a caption.

1. **Start mid-action.** Trim the first 0.5–1 s of every Veo clip so frame 0 is already at the peak.
2. **The thing the title names is on screen at frame 0, moving.** The pond drop under the lens, the hand glowing on the plate. Never a blank desk, a flat card grid or an empty room.
3. **The first words are the claim.** Never "Imagine…" or "In 1895…".
4. **Something visibly changes by about 1 s:** a flash, a zoom, a hand moving in. A short sound on frame 0.
5. **A hook caption on frame 0:** 2–4 words, the promise, cap height about 8–10% of frame, yellow on the hook word.
6. **The Explorer is never at frame 0.** He can arrive from about 1 s, reacting to the thing.

Then one hard fact. The promoted film's exact live title is on screen at 9–14 s. The last 4 s return to the opening picture so the Short loops. Captions all the way through.

## Long hook

- **The first 3 s of picture are the story itself.** No logo, no title card, no bumper.
- **Sentence one is the promise.** Name the payoff within 30 s: the belief, the moment it broke, and what it made possible.
- **5 acts, cause and effect.** This happened, but, therefore. Each act teaches one idea a newcomer can say out loud afterwards.
- **The out is the cream end card** (`STUDIO_PLAYBOOK.md` §7). The last spoken line hands off to the next film. No "thanks for watching".

## Packaging

- **The title is one concrete promise about a familiar thing.** Not the *How Did We Discover X?* formula every week (`THUMBNAIL_AND_TITLE_RULES.md` §1).
- The thumbnail adds to the title, never repeats it. 2–4 words.
- The description opens on the real subject, then chapters, then sources.
- No hashtags in titles. Never reuse the title of a live video.

## Picking the next film

1. Read the latest `audits/weekly/<date>/REPORT.md`. Which Shorts and topics held?
2. Choose a familiar thing with a clear moment of proof, a person to follow, and one room to set it in.
3. Competition check: search the exact title signed out. If the top five are all channels with millions of subscribers, narrow the angle.
4. Fill the vidIQ pre-build audit and the topic score. **Ben picks.**

Candidates are in `VIDEO_BACKLOG.json`.

## Measure

- **Every Monday**, `tools/weekly_public_audit.py` writes `audits/weekly/<date>/REPORT.md`.
- **Every Short at 48 hours:** read stayed-to-watch in Studio and log it with its frame 0 in `audits/SHORTS_LOG.md`. The first Studio read sets the baseline. Aim for 45%, then 60%.
- **Every long at 7 days:** impressions, CTR (judge only past about 500 impressions), average percentage viewed, and views from Shorts (Related).
- **A weak upload is a result, not a re-upload.** Nothing public is remade or replaced.
- Change one thing at a time across a week's Shorts, and keep what beats the previous week by 3 points or more.
- Hold this strategy for four weeks (to 22 Oct). The only weekly question is whether stayed-to-watch went up. No new "locked" doc before then.
