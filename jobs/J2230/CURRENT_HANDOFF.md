# J2230 — 6 Nov 2026, Codex worker continuation

**Incomplete, retain step 3/4. No final cut, KEEP, new Ben-watch card, scheduling, upload or spend.**

This note supersedes the timing assumptions in the older `HANDOFF.md` and
`VACCINE_ASSEMBLY_INPUTS_v01.json`. Older inputs and all Harvey/Willow files are untouched.

## Material timing correction

The old eradication MP4 does **not** contain its stated narration. Its original
intervals used Part 05's planned start **409.59 s** from `VO_RETIME_v01.json`.
The actual v04 cut list and master builder place Part 05 at frame 9647 / 24 =
**401.958333 s**. The original audio word check records large insertions and
replacements, including the body-learning section at the opening; see
`eradication_original_mix_check_v01.json`. Do not assemble from that old MP4.

`prepare_corrected_eradication_input.py` verifies the existing v04 master hash
and the exact final VO stem used by the v04 builder, maps through the actual
master offset, and creates new 16:9 reference video and separate VO inputs:

- `/Users/benjaminoats/_desk/renders/J2230/eradication_corrected_inputs_v02/eradication_assembly_input_v02.mp4`
- `/Users/benjaminoats/_desk/renders/J2230/eradication_corrected_inputs_v02/eradication_vo_from_master_v02.wav`
- Both fully decode, 22.46 s. Full source/output hashes and intervals are in
  `ERADICATION_CORRECTED_INPUT_v02.json`. These are assembly inputs, not Shorts.

The original raw trim also ended at Part 05 40.30 s, inside “gone” (start 40.24,
sentence end 40.60). New inputs preserve it through 40.72 s. The deletion flag
disappears in both v02 checks. There is no next sentence before 41.38 s.

## Actual VO checks and capability hold

`prepare_vaccine_stems.py` also prepares hash-verified separate raw VO inputs
and word-start maps in `_desk/renders/J2230/vaccine_stems_v01` and `_v02`.
These preserve the earlier proposed sentence order and have no new words.

- Variolation raw stem: `vo_check.py` **PASS**, exit 0, 24.50 s, mean −22.8 dB,
  peak −4.5 dB. Warning: “on to” / “onto” at about 0:16.70; listen. Exact output
  is in `variolation_stem_vo_check_v01.json`. This is a VO-input check only.
- Eradication corrected final-master VO stem: `vo_check.py` **FAIL**, exit 1,
  22.46 s, mean −25.6 dB, peak −11.5 dB. The remaining real failure flag is
  “had killed” / ASR “have killed” at about 0:00.98. There is also a warning at
  about 0:07.12, “humans” / “human health workers”. Exact output is in
  `eradication_corrected_vo_check_v02.json`. The same first failure occurs on
  the independent hash-verified raw Part 05 extract.

This session exposed command output and still-image viewing but demonstrated
neither audio_input nor moving_video_input. ASR is evidence of a flag, not a
listener. Do **not** rewrite the canonical text, claim this is a transcription
error, regenerate narration, or waive the failed check. A capable listener
must adjudicate those exact spans; if the spoken take is wrong, Chief owns
the recovery decision under this job's existing-VO/£0 scope.

## Next work

1. Listen to the corrected eradication WAV at 0:00–0:03 and 0:06–0:09, and the
   variolation WAV at 0:15–0:19. Also retain Harvey heart-pump's existing
   extra-“it circulates” listening flag and cuff music-pace flag.
2. Resolve both Vaccine openings before final assembly. The existing recipes
   still open “Doctors took…” and “A disease…”. No new opening is approved here.
   The job calls for anomaly-first openings; the earlier eradication opening
   FIX remains. Do not silently mint a new spoken line in this £0 lift job.
3. Build distinct final vertical edits with original moving picture, captions,
   exact long title, full bed/SFX and four-second loop; run all current gates
   and independent review. Existing masters contain teach labels: do not
   unknowingly inherit extra or mistimed overlays in a Short.
4. Hash-verify durable final copies; only reviewed finished cuts get unique
   Play links and `jobs.py awaits`. Keep the current conditional calendar:
   Harvey 20/23 Nov, Vaccine 25/28 Nov; Willow pair remains J2263 18/21 Nov.

The current HOS registry contains Vaccine s04/s05 originals and replacements,
not a registered eradication Short. An older scripted Short C covers the same
subject; the latest snapshot lists only the experiment and name-origin Shorts
for the Vaccine long. Preserve duplicate-topic review before publication.
The long `ETynHpIYLeY` remains private for 12 Nov 18:00Z in that snapshot;
recheck actual Public state before any scheduling. No YouTube/Buffer changes.

Operationally: both pulls succeeded after the initial sandbox-only OWB pull
was retried with authorized filesystem access. Required under-20GB offload
was attempted; it deferred to 01:00–06:00 because ~16 GiB remained. No files
were moved or deleted on the NAS. All extraction/check processes completed;
no render is running. One isolated HOS worktree, branch `codex/J2230-vaccine`.
