# J0175 audio continuation — 13 Oct 2026, Codex

Resumed at step 4/6 from a clean job worktree. Fixed the segment assembler to duck the existing 004 music bed from the actual normalized, delayed VO (threshold 0.003, ratio 20:1, 5 ms attack, 300 ms release). The delivered bed stem is the ducked bed used in the mix. No VO or picture changes, generation, spend or upload.

Applied the same filter to the already rendered stems and remuxed Bridges 3/4/5 and closing without re-encoding picture. Original files remain. Paths, SHA-256, measured loudness and raw gate findings are in `COMPILATION_AUDIO_DUCK_v02.json`. All four compressed video bitstream hashes match their v01 originals exactly; the prior picture review and polish findings therefore apply to unchanged picture. The new mix measurements are -15.94 to -16.65 LUFS, true peak -1.87 to -2.00 dBTP. Final whole-film loudness remains outstanding.

Gate command: `python3 <OWB>/scripts/sfx_kit.py level --vo <name>_vo_stem.wav --sfx <name>_sfx_stem.wav --bed <name>_bed_ducked_v02.wav --out sfx_level_v02.json`.

Exact tool output:

```text
SFX level PASS: VO -15.7 LUFS, SFX -49.1 LUFS, 2 hits
SFX level FAIL: VO -15.3 LUFS, SFX -70.0 LUFS, 0 hits
FAIL present: no SFX hit anywhere in the stem
SFX level PASS: VO -16.3 LUFS, SFX -49.1 LUFS, 2 hits
SFX level PASS: VO -16.1 LUFS, SFX -49.1 LUFS, 1 hits
```

Those lines refer to Bridges 3, 4, 5 and closing, respectively. The bed-level failures have cleared in all four; Bridge 4 still fails the mandatory SFX-presence check. It has no graphic or fast move requiring a hit. No fabricated effect or gate override was added: Chief must rule on the appropriate shot-specific sound or route a separate gate issue. This is tool evidence, not Chief approval or final PASS. Chief should listen to the revised mixes for musical fit.

Next: use `hos_comp_<name>_ducked_v02.mp4` in `/private/tmp/hos_comp_v01/segments/<name>/` when assembly resumes. Still need 006 moving plates/master (J0140), the closing end-card graphic, intro and Bridges 1–2, complete assembly and full-cut QA. J0204 timelines are already wired into B3/B5/closing. Keep step 4/6 until all segment assembly is complete.

HOS main pull was blocked by pre-existing local standalone-Short changes and untracked concat records; these were left untouched. Changes made and committed only in the clean `/private/tmp/j0175-wt` job worktree. Syntax compilation and `git diff --check` succeeded. No protected calls made.

Repository pre-push check: `check_all.sh` printed `ALL CHECKS PASS` (20 contract tests; package lint, board sync, media guard and Python checks). Used the installed HOS node_modules through an ignored worktree symlink and a /private/tmp npm cache after the sandbox blocked the home cache.
