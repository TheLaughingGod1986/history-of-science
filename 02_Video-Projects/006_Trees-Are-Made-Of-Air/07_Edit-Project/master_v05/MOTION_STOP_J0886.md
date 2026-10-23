# Motion batch stopped: recover existing take, do not resubmit

`j0886-motion` completed with exit **1**. The first Fast take was submitted, but Flow returned `needs_gallery_harvest: true` while still generating. No clip downloaded; the script stopped before submitting any other take. No active tmux session remains.

Existing project: https://flow.google.com/project/8f1b2c08-1f0d-4452-acdc-76a9ad26426d

Read `FLOW_MOTION_LOG_v05.json`. Recover that existing project's video with the existing helper `harvest(page, flow, project_url, dest, wait_s=360)` before any fresh submission. Its reserved spend is 10 credits (live after-balance still needs reading); other three takes were NOT submitted. Submitted spend was logged at Create by the shared Flow helper as codex.

After successful harvest, strip generated audio, hash the file, generate its motion sheet and set its entry to PENDING_VISUAL_REVIEW with actual observations still pending. The mint script now handles gallery-pending returns for subsequent takes, but deliberately stops on the existing uncertain entry so nobody silently resubmits it.

This supersedes the earlier checkpoint's statement that motion is running. There is no v05 master or media-gate PASS yet. Keep queue progress 2/5.
