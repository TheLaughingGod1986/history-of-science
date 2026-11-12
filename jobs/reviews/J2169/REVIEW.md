# J2169 — pre-render blocker, 5 November 2026

Worker: codex. Inventory finished; assembly and rendered-cut verification remain unfinished (step 1/3). No film PASS, KEEP, UAT readiness or publishing approval is asserted. No generation, spend, render, upload, schedule, privacy, title or Buffer changes.

## Exact inputs

Canonical B is **mint**, not soil: `t2_mint_fixed_vo_v03b.mp3`, 23.200000 s, SHA-256 `0f1099262037b62ea2b2a003ce86e196458fa983e9ca97877afb5600e97c7479`. Its hash equals `VO_LOCK_CLAUDE_PASS_20261004.md` and its alignment's `mp3_sha256`; its stored transcript starts “A sprig of mint repaired the air.” The J1004 two-ounces label is not used. No new ASR or listening claim.

C: `t3_bubbles_sunlight_vo_v01.mp3`, 24.160000 s, SHA-256 `5b5d84e560d51ed9ad6f9bf5588f458802620f48f008b9409c532f8a1ea4e269`, matching that same lock. Stored character alignment starts “Leaves only make oxygen in the light.” Both actual files decode with ffmpeg exit 0 (`VO_DECODE.json`).

All 12 unique planned plates exist. `INPUT_INVENTORY.json` records exact NAS paths, hashes, sizes and ffprobe durations/resolutions for them and both VOs. The source rule hash is recorded too. No original is changed. Planned totals remain B 24.20 s / hook 2.24 s and C 25.16 s / hook 2.56 s; these are plan values, not measured finished-cut gates.

## Mandatory source-only picture QA: FAIL

Invoked the unmodified OWB `scripts/picture_qa.py` with each candidate's complete cut/pool files and no rendered video. `Short_B_source_qa` and `Short_C_source_qa` contain the actual machine reports. The baseline source offset is explicitly 0 because BUILD_RULE supplies no in-points. **This is not a finished render's cut list.** The failures are invariant under every legal offset of the implicated eight-second sources: no two source starts can be ten seconds apart.

```text
B: picture QA FAIL: 3 of 8 cuts fail
0:11 S04 10_mint_jar_t1: reuse: same stretch as 0:01
0:15 S05 11_candle_tall_t1: reuse: same stretch as 0:04
0:24 loop_tail 10_mint_jar_t1: reuse: same stretch as 0:01
C: picture QA FAIL: 2 of 9 cuts fail
0:13 S05 05_bubbles_macro_t1: reuse: same stretch as 0:01
0:25 loop_tail 05_bubbles_macro_t1: reuse: same stretch as 0:01
```

The gate compares **source offsets**, not elapsed film time. Waiting ten seconds between appearances or renaming/re-encoding a source does not fix it. A new render of unchanged footage would still replay the source. Do not disable reuse checks, omit loop rows, invent distinct source identities, or claim old KEEP waives this.

## Still inspection and bounded repair decision

`STILLS.json` records the durable, hash-verified source sheet in `_desk/handoff/J2169/SOURCE_STILLS_0_1_3s.jpg`. Samples at 0, 1 and 3 s are **stills only**, not motion review. They show:

- B S02 `11_candle_tall_t1` already has mint inside the jar while the narration introduces the candle before mint is added. Check whether a crop/other already-KEPT candle-only plate can preserve the sequence honestly.
- B S07 `14_trees_breathe_t1` shows a town street. It is weak support for “the little green plant had made the air good again.” A more literal already-KEPT plant shot is preferable.
- C's opening macro clearly depicts leaves and bubbles in these stills. This does not certify motion, the final crop, opening recognition or final phone readability.

**Next decision, no spend:** reconcile the prescribed matching-source loop with the mandatory reuse checker, and approve an exact alternative row-to-source/offset plan that passes the unchanged gate. For B replace S04/S05 repeats and review S02/S07 sequence; for C replace S05 repeat. A loop that uses the same short opening source is still a FAIL under the current checker. If that checker is wrong for the required Shorts loop, only Chief may scope the separate system-change PR and its review; this worker has neither edited it nor waived it. Otherwise specify a different existing source that gives a truthful visually matching loop. Keep canonical VO, all spoken words, <=1.06 atempo, duration, source provenance and current gates. If no existing-media fix exists, Chief must separately bound any generation; J2169 grants none.

Limit that decision to these five failing rows and two B picture concerns; do not repeat a generic timed wait or re-audit the same sources. Then reopen J2169 for assembly and all rendered checks. No rendered candidate exists yet, so no Ben-watch card or immediate finished-cut review is appropriate.

## Duplicate/state check

Read OWB `05_Analytics/hos/snapshots/2026-11-04.json` (`takenAt` 2026-11-04T06:40:33.216Z). No public/scheduled mint, Priestley, oxygen or sunlight Short is listed; this is a saved snapshot check, not a fresh live API read. Long `VbPubYd6Fbs` is Private for 5 November 18:00Z in that snapshot. Must re-read Public before any future Short release.

Standalone `docs/STANDALONE_SHORTS_TEST_2026-10/BUILD_RULE_S5_S8_v02.json` S7 remains `planned` and duplicates B's Priestley/mint experiment and frame-0 source. Do not build, promote or schedule S7 alongside B. Preserve the existing selection; Chief resolves any future release collision. Short A under22s, retired s04/s05/s06 and superseded s07/s08 remain excluded.

Targets 18/21 November 11:30 and watch pack by 15 November 18:00 remain conditional, not approvals. After repair: render, source and pixel picture QA, polish, music/SFX, captions, hook/open/loop and decode, durable hash-verified deliverables, then immediate review successor; reviewer owns awaits for Ben. No direct audio or moving-video input demonstrated in this session. Ben's final watch remains the actual watch/listen check.

## Workspace

Clean worktree `/private/tmp/J2169-hos`, branch `codex/J2169`. Both repository pulls were up to date. Mini free space approximately 9.8 GB; authorized `nas_offload.py --apply` found no old-enough scratch to move (9,811 -> 9,812 MB). No NAS files deleted. No render was started and no tmux process needs resuming.

Repository validation (unmodified `check_all.sh`, full output `REPO_CHECKS.txt`):

```text
ALL CHECKS PASS
```

These repository checks do not clear the two source picture-QA FAILs above. No rendered-cut gate was claimed or skipped as passed.
