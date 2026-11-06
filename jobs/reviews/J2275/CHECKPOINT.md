# J2275 repair checkpoint — 6 November 2026

Partial implementation, not a system PASS. Based on PR439 head
1772cd52e63e4060e36d3e2f0dfb321c16d37f12. J2200 remains FIX and J2033
remains held. No browser submission, credit spend, NAS media change, generated
picture approval, upload or publishing action was performed.

Implemented and covered by zero-submit regressions:

- Charge arithmetic reserves the full remaining 6000-credit liability, including
  the impending take and pending/unposted charges. Only an explicit reconciled
  `posted` amount can release already-deducted liabilities; production does not
  yet supply reconciliation. At 8900 and 8999 the first take is refused; 9000
  leaves exactly 3000. Delayed deductions, other reservations and invalid posted
  amounts are covered.
- Archive destinations and receipts use exclusive creation. Identical retries
  are idempotent, different bytes are refused, and hash-mismatch evidence is
  preserved. Production archive validation requires an existing directory on a
  mounted /Volumes share and a persisted write/read probe before any submit.
  Unit tests explicitly opt into temporary local archives. Each completed take
  carries archive path/hash and price/balance evidence. Ledger appends fsync.
- Technical validation requires a single 1280x720-or-larger 16:9 video stream,
  a full decode, silence and at least the scoped use duration / 8-second route.
  Failed files are recorded FAILED and stop the batch. Missing files preserve
  unresolved charges and stop. Only archived, technically valid, unchanged
  generated outputs advance. In-scope continuations select the latest verified
  parent take/hash rather than blindly using t1. Existing parent start stills
  must decode and get immutable hash evidence. No perceptual KEEP is inferred.
- A stale done file no longer hides a live PID.
- `cmd_submit` explicitly refuses even when armed until the remaining repairs
  below are implemented. It cannot reach the old unsafe live adapter.

Remaining required work, still on J2275:

1. Finding 2: actual selected-control/model/output/price/account/Ultra/balance UI
   evidence under the writer lock immediately before every Create, plus a fake
   browser exercising the real adapter with zero submits on drift. Existing
   `read_live_evidence` still reads environment strings and is NOT repaired.
2. Finding 3: canonical cross-channel writer lock plus durable shared reservation,
   pending and spend accounting, reconciliation and concurrency/crash tests.
   Current ledger/lock CLI defaults are still worktree-local. Do not arm them.
3. Finding 6: detached command must carry validated media/archive/reservation and
   canonical state/log/done paths with atomic runner ownership. Only the stale
   done-file bypass is fixed; detached argument propagation and atomic ownership
   are NOT fixed.
4. Expand integration tests for the above and re-run all checks; verify real
   parent-still inventory before a later production release. The zero-price
   still preparation route is still unavailable and fails closed.
5. Request fresh elected-Chief re-review of J2200 only after all six findings are
   repaired. Worker completion is never authorisation to start J2033.

The original exact20 v05 scope, board hashes, locked narration, accepted trims,
old media and tranche-1 script are unchanged.

Validation from this isolated worktree:

```
python3 -m unittest tests.test_hos009_tranche2_runner -q
Ran 33 tests — OK
bash 00_Brand/Channel-Setup/tools/check_all.sh
ALL CHECKS PASS
```

The repository checks used an ignored symlink to the existing HOS node_modules.
Passing these checks does not complete the outstanding safety work.
