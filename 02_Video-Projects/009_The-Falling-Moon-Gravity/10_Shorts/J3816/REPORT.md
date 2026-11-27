# J3816 — HOS 009 additional apple Short: failed-gate draft

Codex covering. Internal draft only. No Short PASS, no UAT handoff, upload, schedule, privacy change, Buffer change or credit spend.

## Selection and deliverable

004 has at least six identified built concepts; 005 has eight; 006 has five; 007 has its three original cuts and two search cuts; 008 has A/B/C and the no-patent cut. 009 and 010 have two built Shorts each. Selected the older locked long, 009. This is an additional cut, not a replacement of either approved 009 Short.

Title draft: **Did Newton’s Apple Hit His Head?** (not packaging approved). Promotes **How Isaac Newton Proved Gravity Using the Moon**, `wiyfRnsTfTY`.

Draft v02: **17.100 s**, 952×1692, 30 fps. SHA-256: `fe38f08f178fe09f5bef6ceaa2ee357e8956fed01c569b933ad10d050bc75d8a`.

NAS internal draft: `/Volumes/data/studio-live/History Of Science/02_Video-Projects/009_The-Falling-Moon-Gravity/10_Shorts/J3816/hos_009_s03_apple_head_v02.mp4`. NAS copy SHA-256 verified in this session; BUILD.json records the path and matching hash.

Whole sentences lifted from the hash-verified locked Part 02 narration; no added spoken words, no time stretch. Captions use the existing STT word timings. Opening states the apple-head rebuttal; the final sentence returns to the falling apple. The clean archive pictures replace v01’s long-master crops, which exposed clipped baked labels. The Newton card (1642–1727) fades at 5–8 seconds; the promoted long’s exact current title appears at 9–13.8 seconds. Existing 009 score only. Clean source paths, hashes, crop coordinates, source windows and voice alignment are in v02/BUILD.json.

## Actual checks on v02

```text
PASS  vo.wav  0:17.10  mean -23.1 dB  peak -4.1 dB  179 wpm
polish gate PASS: 0 of 6 rows failed, 1 to look at
music gate PASS: hos_009_score_v04_synth.wav, 535.3 s, about 52.2 BPM, brief Pace: 60-68 BPM
FAIL  hos_009_s03_apple_head_v02.mp4  dur=17.1s  motion=6.41  f0diff=1.14  cut1=2.4s  vo_onset=0.07s  tail_gap=1.33s
FAIL  pushed still at frame 0 (mean 0–1.5 s frame diff 1.14 < 1.50)
picture QA FAIL: 1 of 6 cuts fail, 5 to look at
FAIL  0:16 row apple_6: reuse: same stretch as 0:01
```

Full-bleed check: 0/18 padded frames at one per second, 0/35 at two per second. Loudness and first-cut failures from v01 were repaired. The VO PASS is a word-check receipt, not a claim of hearing it. Inspected the full portrait sheets of both versions and the clean source sheet; v02 removes the clipped long labels. The one low-detail frame is a deliberately soft room background around Newton. Actual moving-video perception and audio perception are unavailable in this session: watched=false, heard=false. No media KEEP was issued.

## Remaining repair (agents, not Ben’s watch)

1. Recut the opening from existing approved native moving picture. A scene change before one second can avoid the apple settling during the 0–1.5 s sustained-motion window; preserve the named apple/Newton subject and exact words. Run the unmodified opening gate again. Do not waive the 1.14 failure.
2. Resolve the terminal return against the actual picture gate. Its reuse check rejects this return. The optional `scripts/terminal_loop.py` contract currently admits 22–27 s only and a return of at most 1 s, so it cannot validate this new 16–19 s cut with its 1.2 s tail. Do not relabel source IDs or invent offsets to make it pass. A supported conforming edit or separately authorised gate correction is needed; current checks are unchanged.
3. Re-run all changed-output gates, add the house sound cue on the person-card reveal and level its stem, then obtain capable audio/motion/phone review and Chief Short PASS. Only then can a watch handoff be considered. No schedule is proposed.

v01 and its failed receipts are retained as evidence; v02 is the repair starting point. Draft construction and gate evaluation completed; gate evaluation returned failures. Ordinary Chief authority was rechecked: Codex remains elected. No failed gate was waived.

Repository verification: `check_all.sh 02_Video-Projects/009_The-Falling-Moon-Gravity` printed `ALL CHECKS PASS` using the existing shared node_modules and pinned Python environment. This verifies repository checks only; the Short gates above remain FAIL. `status_board.py --check`: `37 status files and BOARD.json are in order`. JPG review sheets and MP4 media remain outside git; text/metadata only is committed.
