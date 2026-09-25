# Improvements backlog

Written 25 Sep 2026 from `audits/HOS_STUDIO_AUDIT_2026-09-25/AUDIT.md`. Part 1 is to do now. Part 2 waits until the four-week hold in `HOS_STRATEGY.md` ends (22 Oct). Part 3 runs every week.

## 1. Do now (no new videos)

| # | Job | Why | Done when |
|---|---|---|---|
| 1 | **Land the unmerged film records on `main`.** At least: 002 P04–P05 desk locks, all 003 part branches that shipped, `hos-003-studio-schedule`, `hos-003-scout-optimize`, `hos-social-mirror-audit`. Then close every branch whose job is done. | Main stops at 13 Sep and says 003 "Mint closed" while it is live. 131 branches have unmerged commits. | `main` matches the channel; open branches are only live jobs |
| 2 | **Switch 003 X-rays' remaining Shorts and every future long to the new week:** no Premiere, one Short a day at most, Shorts spread across films. | All three longs premiered and have 88 views between them. | Next long goes out as a normal publish |
| 3 | **First Studio read.** For all 11 Shorts: stayed-to-watch, average view duration, traffic source. For the 3 longs: impressions, CTR, average percentage viewed, views from Shorts. Log in `audits/SHORTS_LOG.md`. | Public pages can't show retention or CTR. This is the baseline everything else is judged against. | Log filled |
| 4 | **Add an end screen and a pinned comment to each live long** if missing, pointing at the best of the other two. | A viewer who finishes a film should be sent somewhere. | All three in Studio |
| 5 | **Upload the script as captions (SRT) on 002 and 003** (001 already has clean captions). | Auto-captions mangle names like Mendeleev and Röntgen. | Captions show as "English", not auto-generated |
| 6 | **Retitle the two weakest Shorts** with `retitle-videos.ts` (title only, same id): *What other table has empty chairs?* and *Invisible life is still everywhere*. Keep the files. | Abstract titles; 4 and 6 views. | Dry run, Ben OK, applied |
| 7 | **Build a "How we found out" playlist** with all three longs, first on the channel home page. | The home page is where a viewer lands from a Short. | Playlist live |
| 8 | **Register the live Shorts in the ship gate's library** on the Mac: `gate_shorts_open.py fetch --id … --date … --title …` for each of the 11 (or `add --file` from the exports), so the 14-day repeat-opening check has something to compare against. | yt-dlp is blocked from the cloud; the library starts empty. | `gate_shorts_open.py list --all` shows 11 |
| 9 | **Set up the Monday audit routine** to run `tools/weekly_public_audit.py` and put the report on main. | Orbit runs the same job. | First report on main |

## 2. After the hold (from 23 Oct)

| # | Change | How to judge it |
|---|---|---|
| 10 | **Retire the *How Did We Discover X?* formula** for new longs; A/B the title of one live long with Test & Compare. | CTR and impressions past 500 against the formula titles |
| 11 | **Shorter Shorts, 15–20 s,** one fact and a clean loop. | Average % viewed and whether the graph ends above 100% |
| 12 | **Mid-film subscribe beat,** if Orbit's test (from 11 Oct) shows it doesn't cost retention. It would change the open/out lock, so Ben decides. | Orbit's retention at the beat, then ours |
| 13 | **Cut the cost per film.** Track remints per part (002 P04 reached v26). Aim for a fixed plate board and one UAT pass per plate. | Remints per finished minute, Flow credits per film |
| 14 | **Explorer on a long thumb,** as one Test & Compare variant. | CTR past 500 impressions |
| 15 | **Port the rest of Orbit's Content Ops changes** (subscribe-beat gate, synthetic-disclosure script, stale-Shorts supersede) only when the rule they enforce is adopted here. | — |

## 3. Every week

- **Monday:** weekly public audit → `audits/weekly/<date>/REPORT.md`. Refresh pinned comments.
- **48 h after each Short:** stayed-to-watch into `audits/SHORTS_LOG.md`.
- **7 days after each long:** impressions, CTR, average % viewed, views from Shorts.
- Change one thing across the week's Shorts, keep what wins by 3 points or more.

The first public baseline is `audits/HOS_STUDIO_AUDIT_2026-09-25/PUBLIC_SNAPSHOT.json`.
