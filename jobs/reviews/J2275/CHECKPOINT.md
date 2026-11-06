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
- Detached launch now forwards validated absolute repo/media/archive paths,
  other reservations, ledger/writer/PID state and per-run log/done paths. Missing
  inputs, negative reservations, aliased state paths and existing log/done files
  are rejected. The printed recipe never arms generation. The real launch entry
  owns a canonical cross-worktree runner flock for the child's whole lifetime;
  it records the child PID before signalling an execution gate. A killed owner
  leaves durable child PID evidence, preventing another start while that child
  lives. Missing/torn PID evidence fails closed. A stale done file cannot hide
  either a live runner lock or a live child. Logs and completion files are created
  exclusively and preserved. State defaults now live under
  `~/_desk/state/flow/hos009-tranche2`, not the worktree. These path defaults do
  not implement cross-channel spend reconciliation (finding 3 below).
- `cmd_submit` explicitly refuses even when armed until the remaining repairs
  below are implemented. It cannot reach the old unsafe live adapter.

Remaining required work, still on J2275:

1. Finding 2: actual selected-control/model/output/price/account/Ultra/balance UI
   evidence under the writer lock immediately before every Create, plus a fake
   browser exercising the real adapter with zero submits on drift. Existing
   `read_live_evidence` still reads environment strings and is NOT repaired.
2. Finding 3: canonical cross-channel writer lock plus durable shared reservation,
   pending and spend accounting, reconciliation and concurrency/crash tests.
   Defaults are now canonical for this runner, but other channel writers do not
   yet share its reservation ledger or generation lock. Do not arm them.
3. Expand integration tests for findings 2/3 and re-run all checks; verify real
   parent-still inventory before a later production release. The zero-price
   still preparation route is still unavailable and fails closed.
4. Request fresh elected-Chief re-review of J2200 only after all six findings are
   repaired. Worker completion is never authorisation to start J2033.

The original exact20 v05 scope, board hashes, locked narration, accepted trims,
old media and tranche-1 script are unchanged.

Validation from this isolated worktree:

```
python3 -m unittest tests.test_hos009_tranche2_runner -q
Ran 42 tests — OK
bash 00_Brand/Channel-Setup/tools/check_all.sh
ALL CHECKS PASS
```

The repository checks used an ignored symlink to the existing HOS node_modules.
Passing these checks does not complete the outstanding safety work.

Continuation checkpoint (second bounded run): launcher finding 6 is implemented.
The new tests execute the printed command through a fake final submit function,
start two competing owner processes, kill an owner while its child is live,
simulate PID-persistence failure, and verify exclusive immutable log/completion
handling. All fixtures use local temporary files and fake children; no browser,
Flow credit or NAS operation is involved. Production interlock remains unchanged.

Continue from branch `codex/J2275-runner-safety`, linked repair PR445. This
isolated continuation worktree is `/private/tmp/codex-j2275`. J2275 is released
for continuation, not complete; J2200 remains FIX and J2033 remains held. No
Chief re-review is requested until findings 2/3 and inventory checks are ready.

Continuation checkpoint (third bounded run, 6 November 2026):

- Added `SharedFlowAccounting`, a no-browser account protocol with canonical
  default `~/_desk/state/flow/shared` for both channels and every worktree.
  Exclusive writer ownership covers the context. JSONL reservation, pre-Create
  intent, resolution and explicit posted-charge events fsync the file and its
  directory. A torn, malformed or unknown event fails closed.
- Full unused reservation capacity plus all unposted charges remain liabilities.
  Releasing a reservation never releases an unposted charge. Pending intents
  block both channels, survive a SIGKILL, and require an evidence-bearing
  resolution. No balance heuristic assumes that a delayed charge has posted.
  Reservation identity collisions and duplicate take identities are rejected.
- Nine new regressions cover the exact floor, cross-channel reservations,
  idempotency/collisions, delayed deductions, non-submission recovery, released
  reservations with unposted charges, corrupt ledgers, real competing processes,
  fsync, and a writer killed after persisting its intent.

This is a tested accounting component, **not completion of finding 3**. The
existing Flow writers do not yet consume it; the live adapter and execute_batch
still use the old evidence/accounting interfaces. Production's explicit
`cmd_submit` interlock remains in place. The next continuation must integrate
this protocol into the real per-Create adapter (including idempotent ai_spend
receipts), make other channel writers use the same lock/account state, replace
the environment-based selected-control reader with live UI evidence, and test
that actual adapter against a fake browser. Only then verify parent-still
inventory and request the new J2200 system review. Do not remove the interlock
or mark J2275 done on the strength of these component tests.

Validation for this continuation: 51 zero-submit runner tests pass; full
`check_all.sh` reports ALL CHECKS PASS (existing installed node_modules used via
an ignored symlink). No real browser, Create, Flow credit, NAS media, narration,
accepted trim, scope, upload or publishing change occurred.

Resume from PR445 branch `codex/J2275-runner-safety`; this run's isolated
worktree is `/private/tmp/codex-j2275-resume`. The HOS shared checkout pull was
retried after the explicitly authorised mini repair and reports up to date.
Repair preserved unpushed/dirty work and reclaimed about 346 MB. The disk is
still below 20 GB; nas_offload reports that moves wait for 01:00–06:00 (above
the under-8-GB emergency exception), so no out-of-window bulk transfer ran.
