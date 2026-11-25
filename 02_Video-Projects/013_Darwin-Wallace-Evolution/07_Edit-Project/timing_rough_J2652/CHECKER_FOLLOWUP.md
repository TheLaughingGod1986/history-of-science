# J2652: separate checker correction submitted

12 November 2026, Codex. Continues `REVIEW_v03c.md`; no plan, audio, render or prior evidence was overwritten.

The narrated-card breath defect is now reproduced by a small CLI regression: the production checker reports -2.40 seconds for a true 0.60-second lead-in. The isolated fix captures the preceding spoken end before matching the current card's words; those words still advance the transcript and determine final end hold.

Proposed fix: [OWB PR #871](https://github.com/TheLaughingGod1986/orbit-with-ben/pull/871), commit `231a20e7fd`. Six regression tests pass, including genuine short-breath, unfinished-sentence and short-end-hold failures. Email/network tests and shared-core integrity pass. The original-checker regression fails as expected. No threshold or film gate is waived.

`proposed_checker_readback_v03c.json` records the unmodified 106-row v03c CSV under that proposed checker: passed=true, zero errors, the existing Linnean-reading warning retained. **This is experimental evidence, not acceptance under the production checker.** The original failing `clip_check_v03c.json` remains untouched.

## Seven requested checks, current state

1. No in-word cuts: PASS at plan level, unchanged.
2. Qualifying cuts / sentence preference / seven-second ceiling: FIX overall. Qualifying cuts and ceiling pass; sentence preference and three brief beats still need editorial resolution.
3. Graphics and overlays at most eight seconds: PASS at plan level; new media unbuilt.
4. Locked WAV and hash: unchanged; prior v03c hash verification retained, no audio write or new listening claim.
5. Callback at most 4.20 seconds: PASS in scope (3.56 seconds, trim-only unused tail); media acceptance outstanding.
6. Word-level onsets: PASS in scope; 43 preserved cue schedules, no title overlap.
7. Optional own-code replacements: none adopted; no unbuilt composition claims a phone-sheet pass.

Overall **FIX**, progress **2/3**. No new rough or render is running. PR #551 remains diagnostic and unmerged.

## Next action

J2739 owns the separate review: adopt or correct PR #871, then rerun the production checker on the unchanged truthful CSV. Complete the editorial and source-mapping items in `REVIEW_v03c.md`, render the zero-credit free assets into new versions, and produce a new rough with current contact and 390 px phone sheets. Retain the audio, v02 and all earlier roughs. No generation credits, money, YouTube changes or Ben watch requested.
