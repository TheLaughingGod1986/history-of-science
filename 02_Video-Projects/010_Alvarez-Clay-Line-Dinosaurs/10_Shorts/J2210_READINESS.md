# J2210 readiness repair — 5 November 2026

Codex covering, £0. Based on PR #424 (ad3c0f4d), current main, and the Mini's existing J0365 v03 boards. This PR includes those local-only JSON parent boards so its v04 inputs are inspectable. No media is committed. No generation, VO edit, render, publication or schedule change occurred.

## Repairs

- SHORTS_PICTURE_PLAN_v03 preserves both accepted MP3/WAV hashes. Short A describes J1004 Option A1 as an assembly recipe, not newly rendered VO: six silence removals total 0.260s; sentence 1 at 1.06x, body at 1.00x. Hook 2.849s, planned VO 22.289s, total 23.289s.
- Full opening sentence stays in S01. Removed obsolete promoted-title fields and the duplicate iridium overlay; S07 retains its built-in graphic label.
- Short C opens directly on the robin; robin used only at opening and loop tail. Pigeon/pavement and gull/seaside have separate named parent plates, with explicit Quality prompts and 8s duration. Existing long VO timing stays unchanged; the two new rows are Shorts-only parents.
- Part 05 v04 adds 200 try-one / 518 expected Flow credits, and £2.56 try-one / £6.78 expected Vertex estimates to the inherited board. These are historical-rate estimates, not spend authority. Every generation flag remains false; live balance/rates and separate Chief HOS 010 mint authorization required after HOS 009 J2033.
- Both existing code graphics were read on the Mini and their SHA256 hashes match J2210 exactly. ffprobe measured their durations; exact paths/hashes are in the Shorts plan. Resolver now checks the exact film/part/row code_graphics_v01 filename before searching generated clips.

## Unresolved timing defect: do not assemble

Applying the requested Option A1 hook and shifting the original S02..S08 endpoints by -0.431s makes S02 run 2.849–4.749s = **1.900s**, below the **2.500s** body-cut floor. This is explicitly recorded as FAIL, with no waiver. The inherited final word gap is also 0.120s, above the 0.100s maximum.

A word-boundary search using the accepted Scribe transcript found no eight-shot arrangement (S01 plus seven body shots) satisfying all 2.50–3.80s body lengths with this fixed hook and total runtime. Review must choose a different cut count/plate segmentation while preserving every spoken word, or separately scope another lawful timing treatment. Do not remint VO or alter signed-off words from this job. J2172 remains held; a passing repository check is not an audiovisual KEEP or assembly approval.

## Validation

- Required check_all.sh for HOS 010: **ALL CHECKS PASS**, including contract tests, package lint, board sync, script 92.1 and episode gate. Full output: J2210_CHECK_ALL.txt. The first invocation hit sandbox npm cache permissions; rerunning with existing checkout dependencies passed.
- Exact-file resolver regression test: PASS (correct graphic resolves; wrong part and missing row return None).
- JSON assertions: contiguous timing, full S01 sentence, no promoted-title fields, only two robin appearances, two verified graphic files: PASS.
- Separate body-cut check: **FAIL S02 1.900s**. No moving-video or audio perception was demonstrated in this session; no motion/listening judgment is claimed.
