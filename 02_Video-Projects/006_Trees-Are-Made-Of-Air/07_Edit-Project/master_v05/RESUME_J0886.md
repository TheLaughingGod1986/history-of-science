# J0886 — HOS 006 v05 worker checkpoint

Branch `codex/j0886-hos006-v05`, worktree `/private/tmp/j0886-hos-wt`.
Python: `/Users/benjaminoats/YouTube/History Of Science/.venv-hos/bin/python`.
All paths below are under this film's `07_Edit-Project/master_v05` unless absolute.

## Five queue steps (keep denominator 5)

1. Inspect v04 problem frames and v03 bubble frames, map replacements.
2. Mint and inspect four new zero-credit Flow start stills.
3. Generate and visually inspect continuous motion, then rebuild master v05.
4. Run every gate, inspect all required full-size master frames, produce phone copy <120 MB and SHA-verified HOS UAT/NAS copies.
5. Evidence PR and desk report; park for Chief. No worker final OK or PASS.

## Full-size before-frame observations (actually inspected)

Frames extracted with ffmpeg to `/private/tmp/j0886-frames`; all eight are in `BEFORE_CHECK_SHEET_J0886.jpg`.

- v04 **0:07** (#2, 4.291667–7.375): willow's exposed roots hover above/outside the pan. Replace the entire plate.
- v04 **1:26** (#17, 83.625–88.625): watering can pours over a pot lid, while the trunk is behind the pot, without a visible trunk-to-soil connection in the pot. Replace the entire plate.
- v04 **4:28** (#50, 265.291667–269.5): a quill is held by a detached hand floating above the notebook; no attached arm or body. Replace the entire plate.
- v04 **5:29** (#61, 325.875–330.458333): root, flower and green-leaf jars; bubbles from the right jar continue above the water and into open air. Replace the entire plate; do not paint-patch.
- v03 **4:54** (#55): bubbles rise above the water/jars into room air.
- v03 **5:21** (#59): Explorer beside jar; large bubbles continue well above the water/jar.
- v04 **4:54**: the replacement five-jar plate shows tiny bubbles within water; no obvious air plume at this sampled time. Preserve this shot.
- v04 **5:21**: Explorer walking away holding jar; no obvious air plume at this sampled time. Preserve this shot.

## Resume safely

Check `tmux list-sessions` and `~/_desk/logs/j0886-*.done` first. A missing `.done` for a live session means leave it running. Never duplicate a still or video submission. `FLOW_MOTION_LOG_v05.json` records each submission BEFORE Create; an uncertain failed submission must be recovered from the existing project, not reminted.

Motion batch script `_mint_motion_v05.py`: three Fast takes (10 credits each), one Quality bubble take (100), nominal 130 total; hard job cap 400, live account/balance guards, one attempt each. No cash/Vertex/ElevenLabs. Generated audio is stripped.

When motion is ready, inspect every clip at start/middle/end and intervening frames for contact, attached limbs, and bubbles below the surface. Write `MOTION_REVIEW_v05.json` keyed by clip stem, containing `accepted: true`, the exact `sha256`, and actual observations ONLY after inspecting it. This is worker evidence, not Chief's film PASS. `_build_master_v05.py` refuses to build without matching accepted hashes. It replaces only cuts 2,17,50,61, retains all timing and overlays elsewhere, and stream-copies v04 audio then verifies its encoded audio hash is identical.

Rebuild with `_build_master_v05.py` detached. Then run `picture_qa.py` and `polish_gate.py` using the new master/cuts/pool and only the inherited existing waivers, music gate, SFX level, loudness, and film `check_all.sh 006`. Do not invent any waiver. Existing v04 music/stems are in the shared HOS checkout's `master_v04`; audio is unchanged but the gates still run on v05.

Extract full-size v05 frames at 7,86,268,329,294,321 seconds; inspect each and combine with v03 294/321 reference frames. Report exactly what each now shows. Generate `_PHONE.mp4` under 120 MB (e.g. 960x540, video 1300k, audio 96k; verify measured size). Copy both next to one another in HOS UAT and archive master on NAS, verify SHA-256. UAT and NAS writes require the workspace's normal escalation. Never use a `/private/tmp` path as the final review master.

No upload, scheduling, metadata changes, or final approval is authorized by this checkpoint. Release when background work starts, carry the same queue progress, and finish parked for Chief only after the deliverables and reports exist.

## Disk handling

Mini initially had 10 GiB available. Older HOS006 test-render scratch `/private/tmp/hos006_s08_test` was copied to `/Volumes/data/mac-mini-archive/mini-tmp-scratch/2026-10-23/J0886/hos006_s08_test`, SHA-256 verified for all 14 files, then only its local copy removed. NAS AppleDouble `._` sidecars were excluded from manifest comparison; originals were verified unchanged. `MOVED_TO_NAS_hos006_s08_test.txt` and `j0886_archive_manifest.json` remain in `/private/tmp`. No NAS deletions. Archive log `~/_desk/logs/j0886-archive-retry.log`, completion code 0. The first attempt stopped safely on extra sidecars, before any deletion. Free space is still below 20 GB; avoid large local scratch. Current and previous master scratch retained.

## 23 Oct recovery run (Codex)

Recovered the existing scale-pan generation from its recorded Flow project without submitting a second take. Saved silent 8.0 s clip `clips/02_balance_trunk_v05.mp4`, SHA-256 `1240a36d895d3de41d2ac73f3e4024831ef645f25d96b514208621d198e05aa8`; zero freeze events at 0.8 s threshold. Six-frame contact sheet inspected: root ball remains inside the left pan across the sampled frames. Full-size/intervening-frame review still required before acceptance. Live balance after recovery: 20,820 Flow credits (first take used 10).

Remaining three takes started detached in tmux `j0886-motion-resume`. Log `/Users/benjaminoats/_desk/logs/j0886-motion-resume.log`; completion `/Users/benjaminoats/_desk/logs/j0886-motion-resume.done`. Missing completion with live tmux means leave running. No duplicate submissions. Old `j0886-motion.done` is the previous failed run, not this run. Queue remains 2/5: step 3 requires all motion inspection plus rebuild. No master v05, gates, phone or final acceptance yet.
