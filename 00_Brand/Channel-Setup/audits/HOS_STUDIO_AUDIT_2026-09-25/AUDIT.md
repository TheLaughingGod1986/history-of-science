# History of Science — studio audit (25 Sep 2026)

What is working, what isn't, and what changes. Written from the live public channel (read 25 Sep 2026, `PUBLIC_SNAPSHOT.json` next to this file), `main`, the 131 unmerged branches, and a side-by-side read of the Orbit With Ben studio (`orbit-with-ben`, cleaned up 25 Sep).

Studio numbers (stayed-to-watch, CTR, traffic sources) were not available for this audit. The first Studio read goes in the week-one log (`IMPROVEMENTS_BACKLOG.md` §1).

## 1. The channel today

Three weeks public. Three longs, eleven Shorts, **433 views in total**. Subscriber count is hidden on the public page.

| Film | Long | Length | Went out as | Views | Its Shorts | Short views |
|---|---|---:|---|---:|---:|---:|
| 001 Germs | `_C92tIJCk8A` | 6:05 | Premiere, Thu 3 Sep 18:00 | **4** | 5 | 244 |
| 002 Periodic Table | `AL_-qlWko_g` | 9:01 | Premiere, Thu 17 Sep 19:00 | **84** | 5 | 95 |
| 003 X-rays | `frP_YrNShsU` | 7:06 | Premiere, Thu 24 Sep 18:00 | 0 (1 day) | 1 public, 2 scheduled | 6 |

Shorts, best to worst:

| Views | Short | Frame 0 |
|---:|---|---|
| **110** | Microbes in a drop of pond water | microscope and lamp on a desk |
| **78** | Germs don't cast a shadow | germs moving through a ward |
| 32 | He predicted a metal before it was found | |
| 26 | Germs hitch a ride on you | |
| 25 | The periodic table's empty chairs | |
| 24 | A flask that proved germs come from outside | a still flask |
| 19 | Why tellurium sat before iodine | |
| 15 | Gallium sat where the table said | |
| 6 | Invisible life is still everywhere | a tap and basin |
| 6 | How X-rays Were Discovered by Accident | (1 day) |
| 4 | What other table has empty chairs? | a flat grid of blank cards |

## 2. What's working

1. **The look.** Every frame 0 checked is finished, warm, premium 3D cartoon. It does not look like the glowing-nebula AI channels Orbit competes with. The UAT bible and plate-library process did their job: the picture bar is high and consistent.
2. **The pipeline ships.** Three finished films in three and a half weeks (002 slipped one week, from 10 to 17 Sep), all on the right channel, with Related set on the Shorts.
3. **Scripts that pass.** 001 and 002 masters score 90.4 on the reviewer. The house VO/teach lock (name the thing, say why it mattered) is the right bar for a teaching channel.
4. **The Shorts that win show one concrete, familiar thing, already happening.** *Pond water* (110) and *Germs don't cast a shadow* (78) are the two best, and both open on the thing the title names. The abstract ones lose: *What other table has empty chairs?* (4) opens on a flat grid of blank cards; *Invisible life is still everywhere* (6) is a caption, not a promise. This is the same pattern Orbit measured across 48 Shorts (world or object at frame 0: median 86.5 views; dark or text card: 16.5).
5. **The channel is set up cleanly.** Right handle (`@HistoryOfScienceYT`), wrong-channel guards in `CHANNEL_META.json`, TikTok paused, no `/go/` on Shorts.

## 3. What isn't working

### 3a. On the channel

1. **Longs get almost no views, and Premieres make it worse.** Germs has 4 views in three weeks. All three longs went out as Premieres. Orbit measured the same thing: 13 impressions and 0 views in a Premiere's first hour, and *Andromeda* on 0 after four hours. Orbit's rule is now **no Premieres until subscribers are in the hundreds**. HOS should take it.
2. **Shorts are not sending anyone to the long.** Germs Shorts got 244 views; the Germs long got 4. Related is set, so the pill is there. Studio's traffic sources will say more; from the public side, the likely causes are that each film's Shorts go out in one burst (five in five days) and then stop, and that a long called *How Did We Discover Germs?* is a weaker promise than the Short that sent the viewer.
3. **Every long title is the same formula:** *How Did We Discover X?* It reads as a series label, it is the phrase the biggest education channels already own in search, and it names the method (discovering), not the thing people want to see. Orbit's title audit found that a familiar noun first plus one concrete promise wins, and series-style titles lose.
4. **Runtime drifts from the lock.** The vision says 8–9 minutes; Germs is 6:05 and X-rays 7:06. That is fine if the story is done, but the doc and the films disagree.
5. **No frame-0 hook caption on any Short.** Orbit's rule (a 2–4 word promise on frame 0, about 8–10% cap height) is untried here.

### 3b. In the repo

1. **`main` is two weeks behind the channel.** Main stops at 13 Sep. The work for 002 Part 04–05, all of 003's picture, the 003 Premiere and the social mirror audit lives on unmerged branches. On main, 003 says "Mint closed" while the film is public. An agent starting from main is working from stale facts.
2. **131 branches with unmerged commits.** Many are one-commit records of a STOP (Flow quota, signed-out Flow, missing VO masters). Nobody can tell which are live.
3. **Rules that contradict each other, loaded into every session.** 34 Cursor rules, 32 always-on, about 1,400 lines. 21 are still named `orbit-*`. Examples:
   - `orbit-longform-vo-picture-gate` says "Orbit agency"; `hos-explorer-character` says Orbit is retired.
   - `orbit-next-production` still manages Orbit's Neutron Star queue.
   - The session-start hook injects "8–12 min longs", "Orbit experiences science" and "CG = Gemini Veo API" into every Cursor session, while `hos-flow-veo-primary` says Flow first.
   - Film-specific locks (Germs ship date, Part 03 doctor continuity, microbes) are always-on for every film.
4. **The gates were built for Orbit, so HOS worked around them.** `gate:episode` demanded at least four `[ORBIT ACTS]` markers, and the script reviewer took about 4 points off any script without one. 001 and 002 reached 90.4 by labelling the Explorer's beats `[ORBIT ACTS: Explorer …]`. 003 used the honest `[EXPLORER ACTS]` marker, scored 81.6 and was blocked. It shipped anyway, with no pre-build vidIQ audit on file on main, which says the gate had stopped being run. The episode template still told writers to put Orbit in four scenes. With the fix in this clean-up, 003's master scores 85.6: still under 90, now for real reasons.
5. **Stacked "locks".** The UAT bible was hardened five times in two days, each after one failed cut, and the house rules are split across nine lock docs, three of which (teaching density, silent-readable picture, no DNA helix) exist only on branches. The rules are good. Finding them is the problem.
6. **Orbit leftovers still in the live tree.** `VIDEO_BACKLOG.json` is Orbit's space backlog (Fermi, black holes, Moon); HOS has no topic backlog of its own. `ideas/` is Orbit's. `TikTok/` is Orbit's TikTok account, with `/Users/ben/code/Orbit-YouTube` paths. `audits/` is Orbit's August audits and Studio Replace scripts, which break the one-video-one-upload rule. `docs/` has Orbit's growth and monetisation plans. Plus 833 files in `_archive_orbit/`, which now lives in its own repo.
7. **Cost per film is high.** 002 Part 04 went to rough v26; Part 01 to v14. Many branches are STOPs on Flow quota. The picture is good, but the churn is the price. Most of it comes from one failed still at a time becoming a new always-on rule, rather than from a fixed plate list and a single UAT pass.

## 4. What Orbit learned that HOS should take

| Orbit rule (evidence) | Take it? | Where it goes |
|---|---|---|
| One entry point (`AGENTS.md`), seven docs in force in order of precedence, six Cursor rules with one always-on, everything else in `_archive/` | **Yes** | This clean-up |
| No Premieres until subscribers are in the hundreds (0 views in a Premiere's first hour) | **Yes** (HOS: 4 views on Germs) | `HOS_STRATEGY.md`, playbook |
| Three Shorts a week, each promoting a *different* film, one teasing the new long; never more than one a day | **Yes**, replaces the 4–6-in-a-burst cluster | `HOS_STRATEGY.md` |
| The first two seconds: start mid-action, the named thing at frame 0 and moving, first words are the claim, a change by 1 s, a 2–4 word hook caption | **Yes** (HOS's own top two Shorts already do most of it) | `HOS_STRATEGY.md` |
| Title shapes: familiar noun first, one concrete promise, no hedges, no hashtags, no series formula, never repeat a live title | **Yes**, adapted to discovery stories | `THUMBNAIL_AND_TITLE_RULES.md` |
| Long thumbs: one subject, 2–4 words readable at 168×94, adds to the title rather than repeating it; Test & Compare with 3 | **Yes** | `THUMBNAIL_AND_TITLE_RULES.md` |
| Shorts ship gate (`gate_shorts_open.py`): narration audible, under 40 s, a fresh opening frame | **Yes**, without the Orbit detector (it misfires on HOS's warm lamp light; checked by eye on the three Germs Shorts it flagged) | `tools/gate_shorts_open.py` |
| Weekly public audit every Monday | **Yes** | `tools/weekly_public_audit.py` |
| Phone-size thumb preview | **Yes** | `tools/thumb_preview.py` |
| Title-only fixes by API, pinned-comment refresh by API | **Yes** | `07_Content-Ops/scripts/` |
| YouTube growth/policy basics, channel authority, frame sizes | **Yes** | docs 4–6 |
| A weak upload is a result, never a re-upload; one video = one upload | **Yes** (already HOS rule) | playbook |
| Mid-film subscribe beat | **Not yet.** HOS's open/out lock keeps subscribe in Studio. Revisit after Orbit's data is in (from 11 Oct). | backlog |
| *Familiar thing in danger* lane, Orbit character rules, AI Studio/Omni picture path | **No.** HOS's lane is discovery; its picture path is Flow Veo with the Explorer. | — |

## 5. What changed in this clean-up

- `AGENTS.md` (read first, any agent) and `CLAUDE.md`. Seven docs in force, in order.
- `HOS_STRATEGY.md`: what to make, the week, hooks, packaging, measure. Replaces the channel vision, cadence and inspiration locks.
- `STUDIO_PLAYBOOK.md`: how to build and ship. Folds in the UAT bible, the plate-library runbook, the VO/teach lock and the three branch-only house locks.
- `THUMBNAIL_AND_TITLE_RULES.md`, `YOUTUBE_GROWTH_AND_POLICY.md`, `CHANNEL_AUTHORITY.md`, `YOUTUBE_FRAME_SIZES.md`, `IMPROVEMENTS_BACKLOG.md`.
- Cursor: 34 rules down to 6 (one always-on). Hooks rewritten to point at `AGENTS.md`.
- `gate:episode` counts `[EXPLORER ACTS]` beats (at least 1, warns above 3) instead of four Orbit beats, and the script reviewer credits `[EXPLORER ACTS]` like the old marker and no longer counts it as spoken words. The old marker still counts, so earlier scripts keep their scores. The template script is HOS.
- Tools ported from Orbit: weekly public audit, Shorts ship gate, thumb preview, retitle and pinned-comment scripts.
- `_archive/` holds everything superseded (paths preserved), including `_archive_orbit/`.
- `VIDEO_BACKLOG.json` is HOS's: the three live films plus candidate topics for Ben to pick from.

The film folders (001–003) and anything code or automation reads were left in place.
