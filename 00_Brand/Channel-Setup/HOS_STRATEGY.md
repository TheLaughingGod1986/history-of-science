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
- **Topic fatigue (5 Oct 2026, R2):** at most 6 Shorts in a row on one topic. Stop a topic after **2 not-fed Shorts in a row** (see *Measure*), then give it a 2-week break.
- No Premieres until subscribers are in the hundreds. All three HOS longs premiered; Germs has 4 views after three weeks. Orbit saw 0 views in a Premiere's first hour.
- A finished film beats a rushed one. If a film isn't ready by Thursday, the week runs on three back-catalogue Shorts.

## Short hook (22–27 s)

Two lines, then one hard fact. No greeting, no build-up.

**Line 1 (5–7 words)** is the surprising truth about a familiar thing, spoken in the first second: *"Your hands were killing patients."* *"You can see through your own hand."*

**Line 2** is the stay line: the person or moment that proved it. *"One doctor washed them, and the dying stopped."*

### The first two seconds

Your two best Shorts already do this: *Microbes in a drop of pond water* (110 views) and *Germs don't cast a shadow* (78) open on the thing itself, moving. The two worst open on blank cards and a caption.

1. **Start mid-action.** Trim the first 0.5–1 s of every Veo clip so frame 0 is already at the peak.
2. **The thing the title names is on screen at frame 0, moving.** The pond drop under the lens, the hand glowing on the plate. Never a blank desk, a flat card grid or an empty room. **Every Short gets its own open:** never reuse an opening background from the last 10 Shorts (5 Oct 2026, rule R3 below; `gate_shorts_open.py` checks frame 0 against them).
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
- **Every long sits beside big neighbours** (1 Oct 2026): at least 3 TED-Ed or education videos with 1M+ views on the same subject, and our title, description opening and tags use its subject noun. That is where 002's daily views come from (108 of 126 from suggested, 55.6% from TED-Ed's Mendeleev video). `STUDIO_PLAYBOOK.md` §2.
- The thumbnail adds to the title, never repeats it. 2–4 words.
- The description opens on the real subject, then chapters, then sources.
- No hashtags in titles. Never reuse the title of a live video.

## Picking the next film

1. Read the latest `audits/weekly/<date>/REPORT.md`. Which Shorts and topics held?
2. Choose a familiar thing with a clear moment of proof, a person to follow, and one room to set it in.
3. **Neighbour pool (1 Oct 2026):** every future film must be one YouTube can recommend next to big education videos. `neighbours.py` must PASS with **≥ 3 education videos at 1M+ views** on the topic before topic lock (`STUDIO_PLAYBOOK.md` §2). Use their subject words in title, description and tags, never their channel names.
4. Competition check: search the exact title signed out. If the top five are all channels with millions of subscribers, narrow the angle.
5. Fill the vidIQ pre-build audit and the topic score. **Claude and Grok pick on the desk** (Ben sees the finished film; `AGENTS.md`).

Candidates are in `VIDEO_BACKLOG.json`.

## Measure

- **Every Monday**, `tools/weekly_public_audit.py` writes `audits/weekly/<date>/REPORT.md`.
- **Every Short at 48 hours:** read stayed-to-watch in Studio and log it with its frame 0 in `audits/SHORTS_LOG.md`. The first Studio read sets the baseline. Aim for 45%, then 60%.
- **Every Short on day 1 (5 Oct 2026, R1 and R5):** read its **Shorts-feed share** in Analytics and log it in `audits/SHORTS_LOG.md`. 50% or more means YouTube fed it; under that, it wasn't fed. Under about 50 views, % viewed is noise, so never call a Short on it. Aim for a day-1 average viewed of 60% or more; that is a target, not a gate. These are reads after publishing, not ship gates.
- **Every long at 7 days:** impressions, CTR (judge only past about 500 impressions), average percentage viewed, and views from Shorts (Related).
- **A weak upload is a result, not a re-upload.** Nothing public is remade or replaced.
- Change one thing at a time across a week's Shorts, and keep what beats the previous week by 3 points or more.
- Hold this strategy for four weeks (to 22 Oct); the 5 Oct Shorts feed rules (R1–R5) are additions, not a new lock. The only weekly question is whether stayed-to-watch went up. No new "locked" doc before then.

### Shorts feed rules (Claude ruling, 5 Oct 2026)

Mirrored from Orbit With Ben (`orbit-with-ben` `a909731`: `AGENTS.md` standing lesson 5 and `docs/ORBIT_PLAYBOOK_LESSONS.md` §6). Evidence: a YouTube Analytics read of 60 public Orbit Shorts after the Moon Short `dQlOgsDGmtA` stalled. On day 1 a Short is either fed by the Shorts feed or it isn't: fed Shorts (40) had a median of 85.5 day-1 views, 85% from the feed; not-fed Shorts (20) a median of 13, 15.5% from the feed. Retention did not separate them. Orbit's Moon run was fed for six Shorts, then stopped being fed.

| Rule | HOS form |
|---|---|
| **R1 · Score by feed share** | Day-1 Shorts-feed share, 50% or more = fed. Ignore % viewed under ~50 views. A post-publish read, not a ship gate. |
| **R2 · Topic fatigue** | At most 6 in a row on one topic; stop after 2 not-fed in a row; then a 2-week break. |
| **R3 · Own open** | Frame 0 shows the subject the title names; no opening background from the last 10 Shorts. `gate_shorts_open.py check` compares frame 0 with the last 10 Shorts as well as ±14 days. |
| **R4 · Host never at frame 0** | Already HOS rule 6 above: the Explorer can arrive from about 1 s, never at frame 0. |
| **R5 · Retention target** | Day-1 average viewed 60% or more. A target, not a gate. |

R6 (re-uploads one at a time) is already covered: one Short a day, and a weak upload is a result, never a re-upload.
