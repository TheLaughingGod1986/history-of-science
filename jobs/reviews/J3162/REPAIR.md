# J3162 offline routing repair

19 November 2026. Implementer: Codex. Base: PR675, owner TheLaughingGod1986,
branch macbook/J3154, c2dc9859c1c0242362fa7d611a7dc9de6dca5b12.

The sole production change is in el_client._music_route: unsupported path or
query types return reject instead of other. Both POST entry points therefore
raise malformed_request before legacy transport. This deliberately rejects
str subclasses as well as bytes, None, and other non-built-in strings. Plain
built-in speech/Scribe strings retain their existing controls.

Verification (fixture desks, synthetic tokens, patched transport only):
- Two new matrix tests cover 34 path/query cases across both entry points,
  with TTS_PAUSE present, EL_GUARD_OFF=1 and literal activation False.
  Every case refuses malformed_request, zero urlopen and zero legacy guard calls.
- Existing flight suite: 23 passed, including plain-string canonical/fragment/
  query checks, speech/Scribe and compose controls. Existing guard suite: 11 passed.
- J3158 normalization probe copied byte-for-byte from review commit e93bf01:
  the original exploit assertion now exits on malformed_request (NORMALIZATION.txt).
  verify_normalization.py changes its expected outcome only: all six original
  calls refuse, zero POSTs (NORMALIZATION_VERIFIED.txt).
- Independent reservation probe copied unchanged from J3158: all three failure/
  restart cases pass; reservation persists unchanged and restart performs no GET.
- All eight J3150 hashes verify; only the routing hash was updated there.
  Pinned guard remains 930d987783055d1f73e80fd9ae770f1ecde63d79b397706df74e9492b4029308;
  shape remains ba290b64740c96c3407af17da80d043be3bf840d1863518bfb011e047f9e647e.
- check_all.sh: every check passes except package-lint on the unchanged HOS008
  past schedule, the same baseline failure documented by J3158. HOS009 lint passes.
  git diff --check passes.

Flight, held O_EXCL descriptor/inode protections, one-read reservation and
activation constant are unchanged. No live lock/store, media or film status
was changed. GBP 0; no account calls, generation, activation, deployment, merge,
allowance, YouTube or Buffer change. No pricing rescan. J3047 stays closed unused;
v01/v02 remain rejected, J2035/J2171 held. No replacement delivery promise.

Next: independently review the exact new commit (Claude, Gemini backup;
Codex implementer excluded), then elected-Chief disposition within the same
no-activation/no-merge scope. PR678 stays review-only and unmerged.
