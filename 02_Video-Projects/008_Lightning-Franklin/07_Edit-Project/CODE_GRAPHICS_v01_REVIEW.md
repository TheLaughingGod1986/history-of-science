# J0329 — Franklin code graphics v01, Chief review requested

16 October 2026 · builder: codex · no creative PASS or final OK issued.

**FIX, 16 Oct ~02:06 London (Cursor covering).** P5:11 only. Label is now **SAFE PATH DOWN** (3 words). Re-rendered `code_graphic_008_p5_11_safe_path.mp4` (210 frames, 1920×1080, 30 fps, no audio). The other ten MP4s and five alpha MOVs are the 00:37 renders, hashes unchanged. Frame at 2.5 s shows the new label. NAS mirror was not retried.

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
- P5:11 label is SAFE PATH DOWN (3 words), set by Chief on 16 Oct and re-rendered. The old seven-word line is gone.
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

## NAS handoff — blocked on mkdir

The first mirror attempt stopped on the downscaled-alpha test before any copy. The corrected run passed all decode/alpha checks (`TECHNICAL_CHECKS.json`, 11 rows), then blocked inside macOS `mkdir` while creating the new NAS destination (process sample: stuck in `mkdir`, empty log). Cursor covering stopped that session at 01:24 London on 16 Oct after 45 minutes with no copy started (exit marker `143`). It was not a second render.

The share is mounted (`192.168.1.119:/volume1/data` on `/Volumes/data`). Existing paths stat normally, including `.../History Of Science/02_Video-Projects`. Creating `008_Lightning-Franklin` under that folder, and creating `mini-tmp-scratch/2026-10-16`, did not return within 20–25 seconds. No verified NAS mirror exists. Do not start another mkdir against this share until a create returns; a hung `mkdir` wedges later listings.

Local media is intact at `02_Video-Projects/008_Lightning-Franklin/07_Edit-Project/code_graphics_v01/` in the History of Science checkout (untracked; mp4/mov are gitignored). A safety copy, not a NAS mirror, is at `~/_desk/j0329-code-graphics-v01/`.

Second probe, 16 Oct ~01:50 London (Cursor covering, no mkdir): `listdir` of `.../History Of Science/02_Video-Projects` did not return within 8 seconds. Local `shasum -a 256 -c SHA256SUMS.txt` is OK (11 mp4, 5 alpha mov, contact sheet, manifest, checks). PR #338 is MERGEABLE. No copy was started.

Parked for Chief: review the eleven graphics (holds in "Composite and review holds" above). The mint gate is unchanged. No files were deleted.
