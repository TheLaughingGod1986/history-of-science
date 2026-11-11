# J2632 — falling-Moon candidate, revised

**Revision, 11 Nov, after Claude's sheet read (desk 6805465664).** Same motion: one Moon, 70° circular arc, fixed tangent, no labels, 158 frames, 5.26 s. Two drawing changes, £0.

1. **Strokes.** Encoded f116 measures a 4 px tangent and a 6 px arc at 1080. Dashes are about 37 px on and 27 px off. The 640-wide sheet cells had shrunk the first candidate's 4 px lines to about 1.3 px, which read as hairlines. f116 is now on `CONTACT_SHEET.jpg` at 390 px wide, 1:1, and in `PHONE_390.jpg`. At that size the dashed tangent, the arc and the gap between them still read.
2. **Earth.** The inner ring and the two button arcs are gone on this graphic only. Four inked coastlines sit in the disc: North America, South America, Europe and Africa, same ink, 5 px. Other graphics still use the old Earth.
3. **Parent out.** Not a re-render. The KEEP parent is the whole 8 s clip (`01_really_falling_t1.mp4`, 24 fps, sha256 `ab4b40bc2e65`). The planned out, frame 125 (5.208 s), shows the golden trail curled down the Moon's right side. Frame 94 (3.917 s) is the last sampled frame where the trail still meets the Moon from above and points up. The hook is on screen by frame 96 (4.000 s). The difference is 1.30 s. The source can move: nothing locks the out at 5.26 s except the planned sentence length. Assembler cuts at frame 94, holds this graphic's first frame for that 1.30 s, and keeps the 0.20 s cross-fade. The cannon stays at 189.20 and the words stay on the moving gap. No splice in this revision.

Moon path, radius and the timing samples are unchanged, so Gemini's advisory on the first candidate still applies. New file sha256 `73e77846090c30cc3ae3b67c9df9a3f730dfecad42c1312691f511e13ec3889a` (916,763 bytes). The first candidate was `80ce9560d9dd6d0edbf4fa81e3d1619ccb0f1f8168bfa78c91901451a003ed8d`. Mini checkout and studio-live copies match. `splice_authorized` stays false.

---

# J2632 — first candidate, for the record

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

The revision at the top supersedes this candidate. J2035 stays held until the assembler uses parent frame 94. No Ben action requested.
