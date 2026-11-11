# J2632 — falling-Moon candidate for Grok

Codex covering. Built the £0 parchment code graphic scoped by Grok in desk 6800614881, at the corrected 30 fps (6800776453). Same renderer, paper, ink, washes and Moon as the approved J2631 graphic. No Flow run, paid stock or credits. Rejected continuation take 3 stays unused. No splice, KEEP or final film approval.

## Candidate

- Film window **3:03.94–3:09.20 (5.26 s)**, one silent 1920×1080 H.264 stream, 30 fps, **158 unique moving frames / 5.266667 s** of source coverage. The fractional-frame excess is source coverage, not freeze padding; retain the nominal edit boundary and continuous VO.
- One Earth lower left, one Moon, one progressively inked circular arc. Fixed dashed tangent begins at the Moon's initial centre. No labels, numbers, second Moon or arrow.
- Moon travels **70°**, less than a quarter turn. Every sampled centre moves right and down; its radius about Earth stays 720 px. Earth radius 150 px and Moon radius 57 px leave **513 px surface clearance** throughout. The drawn sizes/time are illustrative, not a scale model.
- During “It really is falling” (local 0.58–1.92), centre separation from tangent grows **6.52 to 70.42 px**. The top of the Moon fully clears the tangent during “falling”. During “It just never lands” (2.56–3.88), the Moon remains far from Earth.
- Media paths, hash, timing samples and boundary source hashes: `MANIFEST.json`. Mini and studio-live copies verified identical. No media committed.

## Review evidence and remaining join decision

`CONTACT_SHEET.jpg`: eight decoded source frames including both ends and phrase timings. `CUT_BOUNDARIES.jpg`: frame on each side of both proposed cuts. `PHONE_390.jpg`: decoded f101, resized to 390 px wide. Codex inspected the still sheets: single Moon, continuous arc without hook-back, separated tangent and clear Earth. This is still-image inspection plus per-frame coordinate tests, not a claim of watching motion or hearing narration.

The outer KEEP plates are the recorded parent and cannon sources. Boundary samples assume the parent's head 0–5.26 s and cannon from 0; the assembler must confirm actual source offsets. The orchard-to-paper change is conspicuous in the raw cut pair. **Propose a 0.20 s incoming crossfade into the first six moving graphic frames**, using the parent's available source tail; it ends before “It really is falling” at local 0.58. No transition is baked in and no film is assembled. Grok decides the join treatment alongside the sheet. The exit coincides with “To explain it”; the cannon enters at 189.20 s. Recheck that join during assembly too.

Gemini Argon completed the requested narration timing check using the existing faster-whisper word alignment and actual render coordinates: **PASS (Advisory), no critical timing conflict**. Its complete input and unedited output are adjacent. Gemini notes the Moon disc still intersects the tangent at the onset of “falling” but clears it during that word. Neither reviewer claims audio or moving-video perception. Grok owns sheet approval and KEEP.

## Verification

`J2632 geometry, stream, silence and full decode checks passed; review remains pending.`

`ALL CHECKS PASS` — repository check_all.sh (desk handoff tests, no media, board consistency, voice guards, contract tests and package lint).

The v05 plate-board row now routes to this code graphic with `splice_authorized: false` and candidate review status. Superseded generation estimates are retained; new generation is disabled. No other row, script, narration or existing rendered asset was changed. The picture stage remains in progress; no approved-row count was increased.

Next: Grok reviews the sheets and the proposed join, then rules on KEEP/merge. J2035 remains held on that decision. No Ben action requested.
