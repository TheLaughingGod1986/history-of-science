# HOS status board

**As of Wed 14 Oct 2026**, updated by gemini (J0140). Generated from `00_Brand/Channel-Setup/PIPELINE.json` by `00_Brand/Channel-Setup/tools/status_board.py`. Don't edit this file by hand.

**Kanban board (live):** https://claude.ai/artifact/Hhk519dkbHMzeaZfp3efhc — reads this same file from `main` every 5 minutes. The first time you open it, allow GitHub when it asks.

## At a glance

| Film | Airs | Done | Now | With · underway? | Time left on it | Ready for Ben's OK | Health |
|---|---|---:|---|---|---|---|---|
| **004** What's Really Inside an Atom? | Thu 15 Oct (1 d) | 95% | Thumbnails (in progress) | **Cursor** · ⏸ waiting: J0106: C v07b file (don't touch the armed test), then the Chief's OK | not estimated | Tue 29 Sep | 🟠 behind |
| **005** The Tied Arm That Proved Your Blood Circulates | Thu 29 Oct (15 d) | 100% | all stages done | — | — | Fri 2 Oct | 🟢 on track |
| **006** The Willow Tree That Was Made of Air | Thu 5 Nov (22 d) | 57% | Picture (blocked) | **chief** · ⛔ blocked: Chief: P5:02 cover KEEP after guarded fresh-still failure; P4:08 t2 KEEP; missing paid P4:06 t2 decision. No further retry; detached batch ended. | 3/6 batches · about 2 weeks left · ETA Sun 25 Oct (in 11 d) | Sun 1 Nov (in 18 d) | ⛔ blocked |
| **007** Why Vaccines Are Named After a Cow | Thu 12 Nov (29 d) | 40% | Picture (to do) | **Claude** · queued (Claude's review of the boards; then the voiceover batch and picture credit) | starts later; due in 18 d | Sun 8 Nov (in 25 d) | 🟢 on track |
| **008** Why Did Franklin Fly a Kite in a Storm? | Thu 19 Nov (36 d) | 35% | Shorts voiceover (to do) | **Cursor** · queued (after 010 long VO) | starts later; due 6 d late | Sun 15 Nov (in 32 d) | 🟠 behind |
| **009** Why Doesn't the Moon Fall to Earth? | Thu 26 Nov (43 d) | 35% | Shorts voiceover (to do) | **Cursor** · queued (after 010 long VO) | starts later; due 6 d late | Sun 22 Nov (in 39 d) | 🟠 behind |
| **010** What Killed the Dinosaurs Was Hidden in a Line of Clay | Thu 3 Dec (50 d) | 35% | Shorts voiceover (to do) | **Cursor** · queued (after 010 long VO) | starts later; due 6 d late | Sun 29 Nov (in 46 d) | 🟠 behind |

## Who's on what

**Claude**
- ▶️ Underway: nothing right now
- ⏭ Next up: 007 Picture, due Sun 1 Nov

**Grok**
- ▶️ Underway: nothing right now
- ⏭ Next up: 006 Edit + master, due Thu 29 Oct; 007 Edit + master, due Thu 5 Nov; 008 Edit + master, due Thu 12 Nov

**Ben**
- ▶️ Underway: nothing right now
- ⏭ Next up: 006 Ben's final OK, due Sun 1 Nov; 007 Ben's final OK, due Sun 8 Nov; 008 Ben's final OK, due Sun 15 Nov

**Cursor**
- ▶️ Underway: nothing right now
- ⏸ Waiting: 004 Thumbnails: J0106: C v07b file (don't touch the armed test), then the Chief's OK
- ⏭ Next up: 008 Shorts voiceover, due Thu 8 Oct; 009 Shorts voiceover, due Thu 8 Oct; 010 Shorts voiceover, due Thu 8 Oct

**chief**
- ▶️ Underway: nothing right now
- ⏸ Waiting: 006 Picture: Chief: P5:02 cover KEEP after guarded fresh-still failure; P4:08 t2 KEEP; missing paid P4:06 t2 decision. No further retry; detached batch ended.

## Being worked on right now

- **004** · 🔄 **Thumbnails** — in progress (0%, with Cursor since Fri 9 Oct, ⏸ waiting: J0106: C v07b file (don't touch the armed test), then the Chief's OK, due Tue 13 Oct (1 d late)): A + B live in the armed test; C v07 armed but not OK'd. v07b re-letter (no spend) is J0106; Chief's OK by Wed 14 Oct 18:00, else pair 2 comes out
- **006** · ⛔ **Picture** — blocked (48%, 3/6 batches · about 2 weeks left · ETA Sun 25 Oct (in 11 d), with chief since Tue 13 Oct 11:20, ⛔ blocked: Chief: P5:02 cover KEEP after guarded fresh-still failure; P4:08 t2 KEEP; missing paid P4:06 t2 decision. No further retry; detached batch ended., due Sun 25 Oct (in 11 d)): Part 01 12/12 kept; Part 02 rough v02 held; Part 03: 16/16 Vertex first takes KEEP (J0107 10 Oct, about $14.82 / £11.86; Chief KEEP desk #180 comment 6102934743), 16_repair_reuse is a window of 14, P3:06 first take minted on Vertex by J0160 (12 Oct, pending UAT); Part 03 rough v01 built 12 Oct (J0137, desk #180 6116202964: 94.8 s on the locked v02 VO, P3:06 slot held by a plate board, no spend; picture_qa flags row 16 reuse of 14 for the Chief), awaiting the Chief's KEEP call on desk #180; Part 04 rows 01–04 have Vertex first takes from J0160 (pending UAT); the Flow refill landed (25,050) and J0138 priced the rest of Parts 04–05 at 1,270 credits for one take each (2,680 for two), on desk #180 for the Chief's price pass (J0139), then the Flow mints (J0140); Codex 13 Oct: detached remint exit 1. P4:08 t2 harvested; P4:06 t2, P5:02/03 MISS after 600 s. Chief reassigns P5:03 from P5:11. Stale-still guard committed 9fe9f3e; no spend this run. J0140 13 Oct 11:24 London: fresh P5:02 still + one Fast attempt started detached in tmux j0140-senebier-fast (runner d0fa55c, PR #310). Start balance 23,690, account verified and reading logged. No duplicate runs. Initial attempt stopped before Create: 0 style chips, 0 credits spent; completed-upload wait fixed fcbb7e8 and no-spend attachment check observed 2 chips. Resumed detached as j0140-senebier-fast-v02. Settled recovery 13 Oct: runner exit 0 but P5:02 per-plate FAIL before Create (incomplete style references); balance 23,690 to 23,680, cause/refund unverified. No live tmux, no usable recovery take. J0140 parked for Chief; evidence J0140_RECOVERY_SETTLED_2026-10-13.md.

## Next steps (in order)

1. 004 airs Thu 15 Oct 18:00: Test & Compare A/B/C armed 9 Oct (C = v07) but on hold — C has no OK. J0106 makes v07b (52/53 at about 2×, file only, due Tue 13 Oct); the Chief OKs it and swaps it in by Wed 14 Oct 18:00, or pair 2 comes out, leaving A and B (desk #180). No other Studio changes on 004 until then.
2. 005: the 2 Oct thumbnail/Test & Compare/end-screen settings went on a stray private copy; manifest now points at the scheduled long wwcjcFfC-5M (#262). Check and re-arm them on wwcjcFfC-5M before Thu 29 Oct (queue J0101).
3. 006 Part 03: all 16 Vertex first takes minted 10 Oct (J0107, about £11.86) and KEPT by the Chief (desk #180, 10 Oct 23:38). Next: Part 03 rough v01 on the Mini (J0137, no spend), with the P3:06 Flow slot held.
4. Shorts test B (Ben: yes, 9 Oct): two search-titled Shorts per film from 007, v02 scripts for 007–010 (titles autocomplete-checked). Shorts voiceover records the v02 pair.
5. Voice queue (ElevenLabs 18,653 until 30 Oct): 007 Shorts B + C (J0109), then 009 long (opening to the Chief J0108/J0110, VO J0111), then 010 long (J0112, J0113), then the 008–010 Shorts. Each job checks the balance first; no music beds without the Chief's OK.
6. Four a month on each channel (Ben, 9 Oct): the channel short of 4 gets work and credits first.
7. 006 picture: Mon 12 Oct after 09:00 read the Flow balance and price P3:06 + Parts 04–05 (J0138), the Chief passes the prices (J0139), then Flow mints and the Part 04/05 roughs (J0140); picture by Sun 25 Oct, edit and thumbnails by Thu 29 Oct, Ben's final OK Sun 1 Nov.
8. Mon 12 Oct: Flow credits refill (AI Ultra). J0138 reads the balance and re-prices 006 (P3:06, Parts 04–05), then 007, on Flow rates; the Chief passes before any mint (J0139).
9. 007 picture: plate boards priced (96 rows, 80 mints); spend starts after 006 and once the whole voiceover batch has passed.
10. 008 edit: narration runs 9:14.8, over the 7–9 min window; the §4 pause trim on the assembled film has to bring it in.
11. Thu 29 Oct 18:05: 005 post-air jobs (Related on its Shorts, cards, end screen, pinned comment).

## Credit left

| Pool | Left | Rule | Checked |
|---|---|---|---|
| ElevenLabs (voice) | 18,653 of 209,536 | voice and both channels' music (one account); resets Fri 30 Oct; eleven_v3 bills about 0.47 credits per char. Until the reset (Chief, 9 Oct): HOS voice first, in queue order: 007 Shorts B + C (J0109, ~700 credits), 009 long (J0111, ~3,400), 010 long (J0113, ~3,500). Each VO job reads the balance first and spends nothing if it's below what it needs. No music bed (OWB or HOS) without the Chief's OK. | 9 Oct |
| Vertex free trial (picture) | about £4.25 projected after 006 Part 03 (16 takes about £11.86; last console reading £16.11 at 10 Oct 22:03Z, console lags) | free trial, use it before it ends 10 Nov; spend down to £0, no £5 floor (Ben, 10 Oct 22:50); never onto real money or the card. 006 Part 03 is done (J0107). Each job reads the live Free Trial balance first; a job needing more than is left goes to Ben. | 10 Oct |
| Flow (picture) | 25,050 (AI Ultra refill landed; read 12 Oct 23:19 London). Priced by J0138: 006 needs 1,270 at 1 take (2,680 at 2), 007 needs 3,050 (6,100); all of it fits | Flow first for picture; AI Ultra active (renewed 12 Oct). Floor 0: never buy credits, top up or spill into billing. No spend until the Chief's price pass (J0139) | 12 Oct |

## Film by film

### 004 · What's Really Inside an Atom?

`███████████████████░` **95%**

Airs **Thu 15 Oct** · ready for Ben's OK by **Tue 29 Sep** · 🟠 behind

Finished and scheduled: long `GHZDsiH7L7A` airs Thu 15 Oct 18:00 (Premiere off). Test & Compare A/B/C armed 9 Oct but C (v07) has no OK; v07b (52/53 about 2x) is J0106, due Tue 13 Oct. The Chief OKs it and swaps it in by Wed 14 Oct 18:00, or pair 2 comes out, leaving A and B (desk #180). No other Studio changes on 004 until then; pin and Related at 18:05 on air day.

- ✅ **Topic** — done
- ✅ **Script** — done
- ✅ **Fact check** — done
- ✅ **Audit + upload package** — done
- ✅ **Voiceover (long)** — done
- ✅ **Shorts scripts** — done
- ✅ **Shorts voiceover** — done
- ✅ **Picture** — done
- ✅ **Edit + master** — done: master v02
- 🔄 **Thumbnails** — in progress (0%, with Cursor since Fri 9 Oct, ⏸ waiting: J0106: C v07b file (don't touch the armed test), then the Chief's OK, due Tue 13 Oct (1 d late)): A + B live in the armed test; C v07 armed but not OK'd. v07b re-letter (no spend) is J0106; Chief's OK by Wed 14 Oct 18:00, else pair 2 comes out
- ✅ **Ben's final OK** — done: long OK'd before upload (29 Sep); thumb C is the Chief's call now
- ✅ **Scheduled** — done: Thu 15 Oct 18:00; pin + Related at 18:05

### 005 · The Tied Arm That Proved Your Blood Circulates

`████████████████████` **100%**

Airs **Thu 29 Oct** · ready for Ben's OK by **Fri 2 Oct** · 🟢 on track

Finished and scheduled. Long `wwcjcFfC-5M` airs Thu 29 Oct 18:00; Shorts A (30 Oct), B `mTY67qet7cM` (8 Nov) and C `x_3L_IdYgEc` (15 Nov) are scheduled. s04 5n7xFQRBUvI scheduled 31 Oct 11:30 UK; cover/settings saved. J0188 3/4: Related after 29 Oct long airs; HOS Buffer credential unavailable.

- ✅ **Topic** — done
- ✅ **Script** — done
- ✅ **Fact check** — done
- ✅ **Audit + upload package** — done
- ✅ **Voiceover (long)** — done
- ✅ **Shorts scripts** — done
- ✅ **Shorts voiceover** — done
- ✅ **Picture** — done
- ✅ **Edit + master** — done: master v02
- ✅ **Thumbnails** — done: A/B/C made; Test & Compare to re-check on wwcjcFfC-5M (J0101)
- ✅ **Ben's final OK** — done: 2 Oct
- ✅ **Scheduled** — done: Thu 29 Oct 18:00; post-air jobs at 18:05

### 006 · The Willow Tree That Was Made of Air

`███████████░░░░░░░░░` **57%**

Airs **Thu 5 Nov** · ready for Ben's OK by **Sun 1 Nov** · ⛔ blocked

Voice is locked. Remaining picture work is recovery and review: Part 05 has Chief KEEP decisions, P5:03 uses reassigned P5:11, and P5:02 is running one authorized fresh-still/Fast attempt. Roughs follow the outstanding picture and graphics checks.

- ✅ **Topic** — done
- ✅ **Script** — done: v02, 93.7
- ✅ **Fact check** — done
- ✅ **Audit + upload package** — done
- ✅ **Voiceover (long)** — done: v02, all five parts PASS
- ✅ **Shorts scripts** — done
- ✅ **Shorts voiceover** — done: A v02 · B v03b · C v01 locked
- ⛔ **Picture** — blocked (48%, 3/6 batches · about 2 weeks left · ETA Sun 25 Oct (in 11 d), with chief since Tue 13 Oct 11:20, ⛔ blocked: Chief: P5:02 cover KEEP after guarded fresh-still failure; P4:08 t2 KEEP; missing paid P4:06 t2 decision. No further retry; detached batch ended., due Sun 25 Oct (in 11 d)): Part 01 12/12 kept; Part 02 rough v02 held; Part 03: 16/16 Vertex first takes KEEP (J0107 10 Oct, about $14.82 / £11.86; Chief KEEP desk #180 comment 6102934743), 16_repair_reuse is a window of 14, P3:06 first take minted on Vertex by J0160 (12 Oct, pending UAT); Part 03 rough v01 built 12 Oct (J0137, desk #180 6116202964: 94.8 s on the locked v02 VO, P3:06 slot held by a plate board, no spend; picture_qa flags row 16 reuse of 14 for the Chief), awaiting the Chief's KEEP call on desk #180; Part 04 rows 01–04 have Vertex first takes from J0160 (pending UAT); the Flow refill landed (25,050) and J0138 priced the rest of Parts 04–05 at 1,270 credits for one take each (2,680 for two), on desk #180 for the Chief's price pass (J0139), then the Flow mints (J0140); Codex 13 Oct: detached remint exit 1. P4:08 t2 harvested; P4:06 t2, P5:02/03 MISS after 600 s. Chief reassigns P5:03 from P5:11. Stale-still guard committed 9fe9f3e; no spend this run. J0140 13 Oct 11:24 London: fresh P5:02 still + one Fast attempt started detached in tmux j0140-senebier-fast (runner d0fa55c, PR #310). Start balance 23,690, account verified and reading logged. No duplicate runs. Initial attempt stopped before Create: 0 style chips, 0 credits spent; completed-upload wait fixed fcbb7e8 and no-spend attachment check observed 2 chips. Resumed detached as j0140-senebier-fast-v02. Settled recovery 13 Oct: runner exit 0 but P5:02 per-plate FAIL before Create (incomplete style references); balance 23,690 to 23,680, cause/refund unverified. No live tmux, no usable recovery take. J0140 parked for Chief; evidence J0140_RECOVERY_SETTLED_2026-10-13.md.
- ⬜ **Edit + master** — to do (with Grok, due Thu 29 Oct (in 15 d))
- ⬜ **Thumbnails** — to do (with Grok, due Thu 29 Oct (in 15 d))
- ⬜ **Ben's final OK** — to do (with Ben, due Sun 1 Nov (in 18 d))
- ⬜ **Scheduled** — to do (with Grok, due Mon 2 Nov (in 19 d))

### 007 · Why Vaccines Are Named After a Cow

`████████░░░░░░░░░░░░` **40%**

Airs **Thu 12 Nov** · ready for Ben's OK by **Sun 8 Nov** · 🟢 on track

Script, facts, long voiceover and both Shorts' voiceover (v02) are done; the Shorts takes wait for the Chief's keep call. Picture waits for Claude's board review and credit.

- ✅ **Topic** — done
- ✅ **Script** — done: v01, 92.3
- ✅ **Fact check** — done
- ✅ **Audit + upload package** — done
- ✅ **Voiceover (long)** — done: about 8.4 min; Part 01 v03 with the shut-up-house pickup
- ✅ **Shorts scripts** — done: v02 (test B): two search-titled Shorts, 9 Oct
- ✅ **Shorts voiceover** — done: B v02 25.5 s + C v02 24.8 s locked 12 Oct; Chief KEEP both (desk 6096257381, VO_LOCK_CHIEF_PASS_20261012.json)
- ⬜ **Picture** — to do (with Claude since Wed 7 Oct, due Sun 1 Nov (in 18 d)): plate boards BOARD_V01: re-timed from the locked VO (8:32) and priced 7 Oct (96 rows: 80 mints = 25 Quality + 55 Fast, 2 of them on Flow, 16 reuses; 36 rows added because the VO runs longer than the script's estimate). First takes about £58, about £139 with usual retakes, against £20.59 usable Vertex. Waits for Claude's review, the voiceover batch and credit; nothing minted
- ⬜ **Edit + master** — to do (with Grok, due Thu 5 Nov (in 22 d))
- ⬜ **Thumbnails** — to do (with Grok, due Thu 5 Nov (in 22 d))
- ⬜ **Ben's final OK** — to do (with Ben, due Sun 8 Nov (in 25 d))
- ⬜ **Scheduled** — to do (with Grok, due Mon 9 Nov (in 26 d))

### 008 · Why Did Franklin Fly a Kite in a Storm?

`███████░░░░░░░░░░░░░` **35%**

Airs **Thu 19 Nov** · ready for Ben's OK by **Sun 15 Nov** · 🟠 behind

Script, facts, package and the long voiceover are done (locked 7 Oct, 9:14.8). Shorts voiceover (v02 pair) comes after 009 and 010; picture waits for the whole voiceover batch.

- ✅ **Topic** — done
- ✅ **Script** — done: v01, 92.1
- ✅ **Fact check** — done
- ✅ **Audit + upload package** — done
- ✅ **Voiceover (long)** — done: long VO locked 7 Oct: 5 parts, 555 s (9:14.8), 7,497 chars; Part 01 pause trimmed, Part 05 one sentence re-recorded; Claude PASS each part (VO_TAKES_KEEP.json)
- ✅ **Shorts scripts** — done: v02 (test B): two search-titled Shorts, 9 Oct
- ⬜ **Shorts voiceover** — to do (with Cursor, due Thu 8 Oct (6 d late))
- ⬜ **Picture** — to do (with Cursor, due Sun 8 Nov (in 25 d)): shot list v01 ready (07_Edit-Project/SHOT_LIST_v01.md, about 58 plates; 8 period details P1–P8 to confirm first); plates start after the whole VO batch passes
- ⬜ **Edit + master** — to do (with Grok, due Thu 12 Nov (in 29 d))
- ⬜ **Thumbnails** — to do (with Grok, due Thu 12 Nov (in 29 d))
- ⬜ **Ben's final OK** — to do (with Ben, due Sun 15 Nov (in 32 d))
- ⬜ **Scheduled** — to do (with Grok, due Mon 16 Nov (in 33 d))

### 009 · Why Doesn't the Moon Fall to Earth?

`███████░░░░░░░░░░░░░` **35%**

Airs **Thu 26 Nov** · ready for Ben's OK by **Sun 22 Nov** · 🟠 behind

Long VO v01 locked (5 parts, 508 s speech); Chief KEEP all five, no pickups (desk 6101629662). Picture next after Claude's board review and credit.

- ✅ **Topic** — done
- ✅ **Script** — done: v01, 91.3
- ✅ **Fact check** — done
- ✅ **Audit + upload package** — done
- ✅ **Voiceover (long)** — done: long VO locked 11 Oct: 5 parts v01, 508 s speech; Chief KEEP all five, no pickups (VO_TAKES_KEEP.json, desk 6101629662)
- ✅ **Shorts scripts** — done: v02 (test B): two search-titled Shorts, 9 Oct
- ⬜ **Shorts voiceover** — to do (with Cursor, due Thu 8 Oct (6 d late))
- ⬜ **Picture** — to do (with Cursor, due Sun 15 Nov (in 32 d)): shot list v01 ready (07_Edit-Project/SHOT_LIST_v01.md, about 58 plates; 8 period details P1–P8 to confirm first); plates start after the whole VO batch passes
- ⬜ **Edit + master** — to do (with Grok, due Thu 19 Nov (in 36 d))
- ⬜ **Thumbnails** — to do (with Grok, due Thu 19 Nov (in 36 d))
- ⬜ **Ben's final OK** — to do (with Ben, due Sun 22 Nov (in 39 d))
- ⬜ **Scheduled** — to do (with Grok, due Mon 23 Nov (in 40 d))

### 010 · What Killed the Dinosaurs Was Hidden in a Line of Clay

`███████░░░░░░░░░░░░░` **35%**

Airs **Thu 3 Dec** · ready for Ben's OK by **Sun 29 Nov** · 🟠 behind

Long VO v01 locked (5 parts); Chief KEEP all five, no pickups (desk 6101773293). Picture next after Claude's board review and credit.

- ✅ **Topic** — done
- ✅ **Script** — done: v01, 92.1
- ✅ **Fact check** — done
- ✅ **Audit + upload package** — done
- ✅ **Voiceover (long)** — done: long VO locked 11 Oct: 5 parts v01, 500 s speech; Chief KEEP all five, no pickups (VO_TAKES_KEEP.json, desk 6101773293)
- ✅ **Shorts scripts** — done: v02 (test B): two search-titled Shorts, 9 Oct
- ⬜ **Shorts voiceover** — to do (with Cursor, due Thu 8 Oct (6 d late))
- ⬜ **Picture** — to do (with Cursor, due Sun 22 Nov (in 39 d)): shot list v01 ready (07_Edit-Project/SHOT_LIST_v01.md, about 55 plates; 8 period details P1–P8 to confirm first); plates start after the whole VO batch passes
- ⬜ **Edit + master** — to do (with Grok, due Thu 26 Nov (in 43 d))
- ⬜ **Thumbnails** — to do (with Grok, due Thu 26 Nov (in 43 d))
- ⬜ **Ben's final OK** — to do (with Ben, due Sun 29 Nov (in 46 d))
- ⬜ **Scheduled** — to do (with Grok, due Mon 30 Nov (in 47 d))

## How the % works

**With** is who has the stage now (the film's `owner`, else the stage's default owner). **Underway** means someone is working on it at this moment; **waiting** says what it is waiting on. **Time left** comes from the stage's `steps` (done/total), `left` (the owner's estimate) and `eta`; "due in N d" counts from the date at the top. Each stage carries a weight by how much work it is; a film's % is the weight done, plus part of any stage in progress. Weights: Topic 3, Script 10, Fact check 5, Audit + upload package 4, Voiceover (long) 10, Shorts scripts 3, Shorts voiceover 5, Picture 35, Edit + master 10, Thumbnails 5, Ben's final OK 5, Scheduled 5.
