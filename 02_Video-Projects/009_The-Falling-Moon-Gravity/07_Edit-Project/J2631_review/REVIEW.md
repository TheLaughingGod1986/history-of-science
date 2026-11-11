# J2631 — five-metre comparison, candidate for Chief review

Codex covering. Built the no-spend parchment diagram with the existing renderer and palette. One dot falls once and stays down; an inked Moon moves continuously sideways and down along one arc under a dashed tangent. Brackets span the same 300 pixels at y=330–630. Four sequential labels, 0.4-second fades. No credits spent, no film splice, no KEEP/PASS decision, no change to the parent or next shot.

## Blocking timing finding

Gemini (`agy --model gemini-4-argon-high`) reviewed the supplied subtitle timestamps, not audio or motion. Its complete unedited findings and input are adjacent. The literal all-labels-before-326.39 interpretation forces the current labels early: `1 MINUTE` is gone before its subtitle cue begins, and `5 m` is gone before its cue begins. Candidate must not be spliced.

Chief decision requested: interpret “off before each cut” as no label crossing either boundary, allowing `5 m` and `TWO STOREYS HIGH` after the internal cut, as Gemini recommends. Suggested local windows: `1 SECOND` 0.40–2.80; `1 MINUTE` 3.35–5.85; `5 m` 6.85–8.85; `TWO STOREYS HIGH` 9.00–10.40; brackets 6.85–7.25. These are recommendations only, not applied. The grouped SRT cannot establish exact word timings; a capable narration reviewer must verify the revised timing. Existing cut, VO and 13.51-second edit interval stay locked.

## Files and checks

- Film interval 319.63–333.14; internal board split 326.39. Proposed source windows 0–6.76 and 6.76–13.51; both rows remain unapproved.
- 1920×1080 H.264, 30 fps, 406 frames / 13.533333 seconds of source coverage for the nominal 13.51-second edit. Final frame starts at 13.5; frame quantisation is recorded, not a changed film duration. Silent graphic; existing VO supplies sound in assembly.
- `MANIFEST.json`: media paths and SHA-256; verified identical Mini and studio-live copies. MP4 stays out of git.
- `CONTACT_SHEET.jpg`: 15 decoded frames, including f202/f203 around the internal cut.
- `CUT_BOUNDARIES.jpg`: both sides of all three proposed boundaries, including neighbouring KEEP sources. Parent trim 0–6.75 and next source start 0 are explicit assumptions for Chief/assembler confirmation; no actual assembled cut exists yet.
- Per-frame coordinate checks across all 406 frames: one landing, no decreasing y, increasing Moon x, no overlapping labels, all text off after 6.40. Final intended centre drops both equal 300 pixels. Still sheets visually inspected; these are not moving-video or listening QA.
- Required repository `check_all.sh`: all checks passed (contract, packages, board consistency, voice guards, no media). Geometry assertions live in `_build_j2631_review.py`; output is guarded against overwrite.

Reproduce with the graphics Python environment, `_build_j2631_review.py --out <new-empty-output-dir> --review <review-dir>`. The renderer also supports `--only 05_minute_second`; use a fresh output directory, as its general manifest writer belongs to the existing builder.

Chief owns the sheet decision, timing clarification and eventual KEEP. J2035 remains held; J2586/J2587/J2630 are not closed by this worker. J2632 is separate.
