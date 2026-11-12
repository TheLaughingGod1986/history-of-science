# J2652: evidence-backed timing candidate, still FIX

12 November 2026, Codex. Continuation of PR #551 and ruling 6808560760.
This is an internal timing scope, not an approved edit, render or UAT cut.
No credits, money, generation, audio changes or YouTube changes.

## What changed

`_retime_picture_plan_v03c.py` produces `PICTURE_PLAN_v03c.json` from the
unchanged v03b plan and its qualified boundary evidence. It searches 50 fps
word-gap positions, retains the source-group start in each search state, and
caps cumulative use of every planned eight-second Quality source. The first
source still ends at 3.82 s, preserving the callback's unused tail.

- **106 beats; zero unsupported cuts and zero in-word cuts.** All nine rejected
  v03b boundaries are gone. Each cut has its script/pause evidence inline.
- **Zero planned Quality-source overruns; longest beat 7.00 s.** This fixes all
  four previously reported overruns. Actual KEEP source windows still need
  checking against the final files; an eight-second planning cap is not KEEP.
- Removed redundant packet close-up, drawer-unlock, second Wallace split-view,
  Lyell-warning and second worried-shelf views. This does not cancel or change
  the separate generation job or claim a credit saving.
- Expanded the joint-reading archive into **two newly scoped compositions**,
  wide then detail, covering the actual reading/extracts passage. These need
  separate free renders; an old short source must not be stretched or looped.
- **All 43 existing cues retain their word indices, onsets and display times.**
  Host-row references were recomputed. Chapter titles now each have an explicit
  2.50 s visibility interval, starting 0.5–0.8 s after a supported sentence end.
  They do not overlap any other cue. The chapter background is distinct from
  its title: the Part 6 title clears at 450.16 s, before Jenkin at 450.20 s;
  the moving background continues to 453.00 s beneath the WHO overlay.
  This is a render specification, not a claim of visual acceptance.
- Callback: **504.22–507.78 s (3.56 s)**, source **3.82–7.38 s**. Trim only.
  The unused 4.18 s source budget is not an obligation to fill the full tail.
- v02, v03, v03b, their existing media and the locked WAV are unchanged.
  No new part files replace the old v03 parts: v03c's consolidated rows are the
  candidate source of truth for the next scope review.

## Seven requested checks

| Check | Result | Evidence / limit |
|---|---|---|
| 1. No in-word cuts | PASS, plan | Strict independent word-interval check on all 105 internal boundaries. |
| 2. Qualifying cuts, sentence preference, 7 s maximum | FAIL overall | Qualifying cuts and ceiling PASS. Sentence preference remains a solver penalty, not independently accepted editorial compliance. Three short beats below need resolving/review. |
| 3. Graphics and overlays at most 8 s | PASS, plan | Every beat at most 7 s; cues at most 4 s; title windows 2.5 s. New compositions remain unbuilt. |
| 4. Locked WAV and hash | PASS | Re-read NAS WAV: 837178125a72fb250d255f1039c5cb7f8630bbb313cf23801a1155f257d796e0. No audio writes. |
| 5. Callback at most 4.20 s, no stretch/loop | PASS, scope | 3.56 s of unused source, disjoint from the opener. Media acceptance still outstanding. |
| 6. Word-level onset audit | PASS, scope | All 43 anchors/display schedules preserved; no cue/title overlap. |
| 7. Three optional code replacements | PASS, not adopted | None adopted; original Quality choices retained. No unbuilt replacement is claimed to pass 390 px. |

**Required clip_check: FAIL (exit 1). Overall FIX. No gate changed or bypassed.**
The exact output is `clip_check_v03c.json`, with five negative breath errors
and one mid-sentence warning. This is not replaced by the independent tests.

## Exact gate discrepancy

The CSV truthfully includes words spoken during chapter-background shots.
`clip_check.py` first updates `last_spoken_word_end` using the current row's
`vo_text`, then computes that same CARD row's pre-card breath from it. It
therefore measures from words *during* the card rather than from the preceding
sentence. Example: Part 2 starts at 75.40 s after sentence end 74.60 s (0.80 s
breath), but the tool subtracts the card's last spoken word ending 78.14 s and
reports **−2.74 s**. All five errors reproduce this ordering.

Do not empty the card's truthful VO text, relabel CARD as ordinary picture to
hide the error, edit the report to pass, or waive the gate. A correction to the
shared checker needs its own reviewed PR under the standing check-change rule.
It must capture the preceding spoken end before consuming the current row,
retain the current row's words for following checks, and test both genuine
insufficient breath and chapter rows with narration. This job makes no such
checker change and grants no gate exception.

## Remaining editorial/render work

1. Review sentence preference and the three brief beats: cabin tail
   **74.60–75.40 (0.80 s)**, bagging detail **90.82–92.22 (1.40 s)**, paint mix
   **458.14–459.64 (1.50 s)**. They are honest flagged candidates, not polished
   cadence PASSes. A reframe must be a real distinct edit, never a duplicate
   frame run. The cabin sentence has no supported internal boundary from
   67.68 to 74.60; the following 0.80 s is the required chapter breath.
2. Resolve the shared-checker discrepancy through its own reviewed change,
   then rerun the unmodified truthfully populated CSV through that checker.
3. Review the newly allocated imagery against the spoken words, particularly
   the joint-reading archive and the case-file background under Jenkin. Scope
   the source for every moving-background graphic; v03's inherited generic
   `overlay_on_moving_plate` instruction alone does not name sufficient media.
4. Build the five missing free sources plus newly timed graphics/chapters and
   the two archive compositions, each as new versioned files at zero credits.
   Do not reuse the old baked chapter titles for their longer background shots.
5. Build a new-version diagnostic rough and new 390 px phone/contact sheets
   after the outstanding checks. The existing v03 rough is unchanged and is
   not evidence for v03c. No new render is running from this checkpoint.

## Verification

```text
Ran 8 tests in 0.017s — OK
unsupported_cuts: []
in_word_cuts: []
native_source_overruns: []
chapter_title_cue_overlaps: []
LOCKED WAV HASH PASS
ALL CHECKS PASS (repository check_all.sh only; not film acceptance)
clip_check exit 1; passed=false (5 errors, 1 warning)
```

Tests independently cover full coverage and word boundaries, cumulative source
windows, callback disjointness, cue identity, chapter breath/visibility, input
hashes and disabled generation/render authorization. No audio listening or
moving-video perception is claimed. This checkpoint leaves J2652 at **2/3**;
continuation requires the work above, not Ben's watch or a credit purchase.
