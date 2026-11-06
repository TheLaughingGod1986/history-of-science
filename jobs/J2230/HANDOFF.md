# J2230 — six HOS Shorts gap-fill: preflight and continuation

Codex covering, acting Chief, 6 November 2026. GBP0. **Incomplete; step 1 of 4.**

## Selection and calendar ruling

`PREFLIGHT.json` is evidence for the existing J2230 queue record, not a second tracker. The permitted dates are 18, 20, 21, 23, 25, 27, 28, 30 November and 2, 4, 5 December. Both HOS and OWB HOS upload registries were read. Preserve 18/21 November Willow, 27/30 November Moon (J2171), 2 December Franklin C (J2170/J2255), 4 December Alvarez (J2172); retain Franklin A's own reservation pending its separate review. Do not infer scheduling permission from this list.

Chief selection decision: count the two already-finished Willow replacements under J2263 toward the required two Willow cuts. They have KEEP and existing awaits_ben cards J2263.1–2, with unique Play links; Ben has not approved them. Do not duplicate their work or cards, reuse superseded uploaded cuts, or change their YouTube/Buffer state. This preserves space for two Harvey candidates on 20/23 November and two Vaccine candidates on 25/28 November. All slots remain conditional on current gates, the long being public, Ben watch and a separate scheduling job.

## Actual media verification

Four unuploaded archive candidates were read and their entire MP4 SHA-256 matched the tracked metadata, using the NAS paths in PREFLIGHT.json. The iCloud Harvey s06 path exists but reading bytes raised `OSError: [Errno 11] Resource deadlock avoided`; use the verified NAS source, not a placeholder.

Fresh gate results are committed beside this note; these supersede old gate PASS claims:

- Harvey s06: **FAIL**, integrated loudness −20.0 LUFS; first VO onset warning 0.70s.
- Harvey s07: **FAIL**, integrated loudness −20.5 LUFS; first VO onset warning 0.51s.
- Willow s05: **FAIL**, integrated loudness −20.5 LUFS and first cut 3.97s.
- Willow s06: **FAIL**, integrated loudness −21.4 LUFS and first cut 3.07s.

Nothing newly passed. No failed-gate override, no Ben-watch card created for these failed candidates. Measurements do not demonstrate watching or hearing.

## Continue this same job

1. Retain the 1/4 queue progress and HOS:005, HOS:006, HOS:007 links. The selected 006 work remains with J2263; check its current review/Ben state rather than redoing it.
2. Verify the older Harvey ideas were not retired or already public against live Shorts and LEARNINGS rule 8 before adapting s06/s07. Rebuild as new versions from locked VO and plates, without overwriting archive originals. Correct mix from stems, onset, anomaly-first hook, current titles, timing of the 9–14s title, 4s terminal loop and word captions. A simple loudness/trim transcode is not sufficient evidence for these other requirements.
3. Build two distinct Vaccine extracts from locked long VO and picture. Candidate topics are variolation and smallpox eradication, distinct from scheduled s04 Jenner test and s05 vacca/Jesty. The existing variolation SRT blocks 16–20 span 67.700–85.220s and are too short alone; select additional existing words, using exact word alignment, to meet 55–65 words and 22–27s. Do not add a new spoken line or pad with silence. Eradication is in Part05 (SRT blocks 112–118); select a standalone coherent lift and verify all word boundaries. Titles in PREFLIGHT are drafts, requiring signed-out autocomplete and duplicate-topic checks.
4. Run current open gate for each actual target date, VO word check, picture/polish/music/SFX gates, phone/readability and caption/loop/decode checks. Paste real PASS output in the report and film production-status.md only on actual PASS. Use a capable reviewer for perceptual claims; this Codex session demonstrated neither audio_input nor moving_video_input.
5. Hash-verify durable final copies. Queue the immediate independent review successor when ready. Only KEEP cuts go on awaits with working unique Play links, retain Ben-watch and publication holds. No YouTube, Buffer or registry writes occurred in this run.

## Operational preflight

OWB divergent pull recovered after the prescribed safe mini_repair; retry pull succeeded. Repair recovered about 1.3GB, leaving about 6GB. Authorized under-8GB NAS offload found no eligible scratch, so moved nothing. HOS pull succeeded. One detached clean HOS worktree used: /private/tmp/J2230-codex-hos. No render is running for this job; gate logs/sheets are in /Users/benjaminoats/_desk/renders/J2230/preflight.
