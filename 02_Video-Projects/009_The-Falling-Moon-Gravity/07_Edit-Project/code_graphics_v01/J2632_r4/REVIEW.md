# J2632 r4 — review candidate, not KEEP

Chief ruling: https://github.com/TheLaughingGod1986/history-of-science/pull/180#issuecomment-6807936928

Timing-only revision on PR #543. Added 32 tangent-draw head frames at 30 fps; the Moon stays at its start through f32. All accepted geometry and artwork remain unchanged. Motion starts at film 183.94 (f32). Graphic starts 182.873333; 190 encoded frames end 189.206667, with nominal film out 189.20 unchanged.

Fade specification: graphic f0–f5 occupies six frame durations, 0.200 s, ending 183.073333. Parent 99–104 supplies the outgoing side, with 104 the last parent frame; 108 and 125 are excluded. Relative to the parent out target 183.065, residual is +0.008333 s, inside Chief's nearest-frame tolerance. No join has been assembled and no later row or narration changed.

New SHA-256: `23c832b09e70f78d8eeece657dac11d6148e2a5f5c701f2ad88b868845b5f3b3`.
Superseded r3: `cb8051bb9d6b46d014be46977522d089e19262fa7fd7fd90dfee3099fb13c2f7`. Earlier evidence and media retained.
NAS safety copy hash verified; full paths in MANIFEST.json.

Evidence: CONTACT_SHEET.jpg includes f0/f5/f31/f32; PHONE_390.jpg contains f10/f137/f188 at native 390 px width; CUT_BOUNDARIES.jpg includes parent99–104 and excluded108/125, graphic first/last and cannon first. Codex inspected these still sheets: the two open rings remain visible at phone size. This is still-image review, not listening or motion perception.

Tool result: `J2632 geometry, stream, silence, 190 unique decoded frames and full decode checks passed; r4 timing residual under 10 ms; review pending.`
Repository result: `ALL CHECKS PASS` (full output CHECK_ALL.txt).

Gemini timing advisory: prior head/cut and fade contradictions resolved within the Chief tolerance (see GEMINI_TIMING_REVIEW.md, unedited output from agy gemini-4-argon-high). Assembly must use a 0.200 s fade, not six full 24 fps parent durations (0.250 s), exclude parent105+, and snap the tail to189.20. This is a text/ASR arithmetic review, not an assembled-join review. Tranche runner: 80 tests OK; private-network guard: 5 tests OK.

Pending: Claude's f0/f5/f31/f32 sheet read; Chief KEEP. `splice_authorized` remains false. No merge, splice, Flow spend or YouTube change.
