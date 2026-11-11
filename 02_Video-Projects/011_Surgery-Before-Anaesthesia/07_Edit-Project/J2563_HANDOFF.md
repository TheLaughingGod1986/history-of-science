Codex covering J2563 — preflight findings; assembly incomplete, parked for Chief.

The approved v02 was read from current origin/main in an isolated worktree. The shared Mini HOS checkout is on an older Chief branch, so its absence of film 011 was not treated as permission to recreate the project or overwrite local work.

Concrete blockers:

- Every one of the 13 archive URLs in v02 returned HTTP 404 on a direct source check. J2563_PREFLIGHT.json records the exact URL, time and result for each. No archive image downloaded, licence accepted, or composite built. Source names in the plan alone are not evidence of permission.
- Locked hos_011_vo_v01.wav was not found in the shared checkout, the MacBook slot-2 checkout, or studio-live's film store. The 011 studio-live folder itself is absent. Additional bounded local searches found no WAV. Its expected SHA-256 remains d873f1d0c9158087fd61ce0b9f53de985055d778cd58b8df70c67c0701300ae2. The tracked word timings exist. No silence, replacement voice or newly generated narration substituted.
- The nominal free reuse row P5:16b requires the unused 3.48–8.00 s tail of P1:07b, which is itself an unmade mint_quality row. Thus this is 26 buildable free rows plus one dependency, not 27 independent available inputs.
- The timestamp audit flags 35 cuts inside punctuation-delimited sentences, including 18 inside word intervals. Eleven punctuation-delimited sentences last longer than 8 seconds, while no planned row exceeds 8 seconds. The literal “no sentence cut by a picture change” plus maximum 8-second row cannot both hold for those sentences. See J2563_TIMING_AUDIT.md for every boundary and sentence. Punctuation analysis is advisory; no audio perception or motion review is claimed.

Delivered: reproducible read-only preflight script, machine-readable source/timing findings, complete timing exception list, and nine conditional savings options (four strongest: 400 try-1 / 1,036 expected Flow credits). All savings use v02's budget rates; no row changed.

Not delivered: the 13 code graphics, 13 archive composites, reuse clip, timing rough, overlay cue schedule or v03 retime. No render gate PASS, film approval, or completed edit stage is claimed. No media was written to studio-live. The accepted P4:08a wording correction (“mid-1840s”) is recorded for the next plan version; v02 remains immutable.

Next: Chief resolves the sentence-cut versus 8-second conflict, locates/restores the locked WAV and approves a corrected archive-source brief (or separately scopes replacement source research). Then resume J2563 to build all free rows, render the rough, verify hashes/durations and request capable motion review. The missing reuse source stays a labelled dependency slate until P1:07b exists, unless Chief scopes another solution.

£0 / 0 credits used. No minting, uploads, schedules, privacy changes, or generation_authorized changes. Nothing sent to Ben for UAT.

Validation (repository checks, not a film-stage approval):

```text
-- durable desk handoffs: PASS
-- no media: PASS
-- status board in sync: PASS
-- ElevenLabs guard tests: PASS
-- vo_check word tests: PASS
-- atempo check tests: PASS
-- voice speed (atempo <= 1.06): PASS
-- contract tests: PASS
-- package-lint: PASS
ALL CHECKS PASS
```

The first check run could not use npm's protected cache. Reused the existing installed node_modules through an ignored worktree symlink and reran the full check successfully; no dependency changes.
