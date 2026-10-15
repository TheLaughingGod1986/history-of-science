# J0329 — Franklin code graphics v01, Chief review requested

16 October 2026 · builder: codex · no creative PASS or final OK issued.

Eleven silent 1920×1080, 30 fps MP4s follow the v03 board's `use_s` and film/part VO placements. Five additional ProRes 4444 MOVs contain straight alpha. Full-frame rows have a cream/gold/blue ink drawing on brown period paper, Didot italic labels, and drawn mechanisms. The builder uses the existing Pillow/ffmpeg house approach, with no API calls, generated imagery or paid dependencies. No VO or source board was changed.

## Files and reproduction

Local pack: `/Users/benjaminoats/YouTube/History Of Science/02_Video-Projects/008_Lightning-Franklin/07_Edit-Project/code_graphics_v01/`.

NAS destination (copy pending; not yet verified): `/Volumes/data/mac-mini-archive/YouTube/History Of Science/02_Video-Projects/008_Lightning-Franklin/07_Edit-Project/code_graphics_v01/`.

The pack contains all clips, eleven sample stills, `CONTACT_SHEET.jpg`, `MANIFEST.json`, `TECHNICAL_CHECKS.json`, and `SHA256SUMS.txt`. Text-only copies of the manifest, checks and hashes accompany this note. Renders are excluded from git.

```sh
/Users/benjaminoats/_desk/venv-graphics/bin/python \
  02_Video-Projects/008_Lightning-Franklin/07_Edit-Project/_build_code_graphics_v01.py \
  --out <new-empty-output-directory>
```

`--stills-only` makes the sample stills first. The renderer refuses to overwrite existing videos. It streams frames into ffmpeg, avoiding large image-sequence scratch folders. Duration rounds up by less than one 30 fps frame: assembly trims to the manifest's exact `use_s`. Manifest records locked VO hash, source-board hash, spoken lines, film start, part-relative start and original `tick_ink_s`. Ticks are cues for the separate SFX stem, not embedded audio; their eventual mix requires the house level check.

## Composite and review holds

The brief mentions two overlays; the authoritative plan has **five**. All five are delivered as alpha plus clearly provisional paper-backed MP4 previews:

| Row | Required moving picture |
|---|---|
| P2:15 likeness_fire | P2:12 notebook_list, unused moving tail |
| P3:04 letter_crosses | P3:07 slow_news |
| P4:06 same_thing | P2:08 jar_spark and P4:02 knuckle_spark, left/right |
| P5:08 looking_path | P1:16 question_sky |
| P5:10 metal_easy | P5:06 rod_fitting |

No local picture KEEP record exists for 008 yet. In particular P4:06 is only its divider and label: it is **not a completed spark comparison**. Paper MP4s must never be substituted into these moving-plate slots in the finished film. After mint/KEEP, position overlays against the actual subjects and verify unused windows and continuous movement.

Chief should review each graphic against its VO in motion, not only the contact sheet. Outstanding judgment points:

- The Atlantic contour is a schematic ink coastline, not a verified historical 1752 map. Its geographical fidelity needs review or a sourced geometry revision before acceptance.
- P5:11 retains the exact approved seven-word label “A SAFE PATH TO THE GROUND”; this conflicts with the four-word house limit. Chief decides shortening or an explicit exception. No wording exception was assumed by the worker.
- Tick times and graphic events follow the boards; exact spoken-word alignment remains an assembly review against the locked audio. The builder does not replace the part VO or retime speech.
- Five rows still require moving plates; plate alignment, composite readability and final UAT cannot be judged from these standalone alpha files.

The mint gate remains unchanged: after 006 and 007, with a live Flow reading leaving at least 3,000 credits after 008's expected 5,605. No Flow, Vertex or ElevenLabs calls, no spend, no uploads, and no deletion.

## Validation evidence

Repository `check_all.sh` output:

```text
-- no media: PASS
-- status board in sync: PASS
-- ElevenLabs guard tests: PASS
-- vo_check word tests: PASS
-- contract tests: PASS
-- package-lint: PASS
ALL CHECKS PASS
```

These are automated repository results, not Chief's creative PASS. Status board regenerated and checked again after the review handoff update.

Native-resolution alpha verification is used: a first attempt downscaled alpha to 192×108 and failed an opacity threshold because it averaged thin ink strokes. The corrected check examines the actual full-resolution alpha, requiring both fully transparent pixels and opaque ink.

## NAS handoff — pending filesystem operation

The first mirror attempt stopped on the downscaled-alpha test before any copy. The corrected run passed all decode/alpha checks, then blocked inside macOS `mkdir` while creating the new NAS destination (confirmed by a process sample). The share is mounted as NFS, but no verified mirror exists yet. Local media is intact. Do not start a duplicate copy.

- Session: `j0329-mirror-v2`
- Log: `/Users/benjaminoats/_desk/logs/j0329-mirror-v2.log`
- Exit marker: `/Users/benjaminoats/_desk/logs/j0329-mirror-v2.done`
- Runner: `/Users/benjaminoats/_desk/jobs/j0329-verify-mirror.py`
- Missing exit marker means still running; once present, read it and the log. Exit 0 is only written after all files match SHA-256 on NAS.

J0329 remains at step 3/4 until the mirror is verified and the final review handoff is recorded. Then park it for Chief. No files were removed or duplicate render started.
