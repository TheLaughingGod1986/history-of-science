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
   browser exercising the real adapter with zero submits on drift. The original environment reader was replaced at the fourth checkpoint below;
   production wiring and live DOM validation are still unfinished.
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


Continuation checkpoint (fourth bounded run, 7 November 2026):

- Replaced the environment-based selected-control reader with strict DOM evidence
  for selected model, output count, aspect and duration; account control identity;
  explicit ULTRA entitlement; unique exact price and unambiguous AI-credit balance.
  Menu option text and environment variables cannot establish selection. Missing,
  changed or unknown layouts fail closed. No live browser was opened or inspected.
- Added `guarded_create`, an actual page adapter requiring ownership of the shared
  account lock. It preserves immutable UI evidence and fsyncs the shared charge
  intent before attempting Create. Its synchronous DOM operation rereads all
  evidence and clicks the same unique enabled control only if unchanged. It has
  no coordinate fallback or automatic retry. An explicit no-click drift resolves
  NOT_SUBMITTED; a disconnect or unknown response leaves PENDING and blocks both
  channels. A known click resolves CHARGED without assuming billing has posted.
- Six additional tests cover each rejected evidence field with zero clicks,
  intent/evidence-before-click ordering, duplicate identities, last-moment drift,
  disconnect recovery blocking the other channel, lock ownership, and execution
  of the production JavaScript against a Node DOM fixture. These use fake pages
  and DOM nodes only, never a real Create or Flow browser.

Validation: 57 runner regressions OK; `check_all.sh` ALL CHECKS PASS. The installed
HOS node_modules was used via an ignored symlink. No credits, media, scope, trim,
VO, upload, schedule or privacy changed. This is still step 1 of 3, not completion
of finding 2/3 and not a request for production review.

Required continuation: connect the new guard to the actual configured Create
boundary (the current `live_video_submit` still calls the legacy helper), validate
its strict selectors against a read-only real DOM fixture, integrate the shared
reservation/charge protocol into execute_batch and every active cross-channel
Flow writer, and provide idempotent ai_spend receipts. Preserve the production
interlock until all of that, parent inventory verification and independent J2200
re-review are complete. Do not merely call the guard before generate_clip: that
helper changes settings and can retry later; the guard belongs at its exact click
boundary. Any legacy spend/confirmation paths also need the shared lock/account
protocol. The core helper's current version must be changed in OWB first if it is
a registered shared core file, then synchronized under the studio core rules.

Resume PR445 branch `codex/J2275-runner-safety`; this worktree is
`/private/tmp/codex-j2275-live` (the previous /private/tmp continuation was gone).
Remaining multi-writer integration exceeds a bounded 20-minute run, so the claim
is released at this tested checkpoint. J2200 remains FIX, J2033 remains held;
nothing is waiting on Ben. No production interlock was removed.


Continuation checkpoint (fifth bounded run, 7 November 2026):

- Connected `live_video_submit` to the actual HOS helper's configured Create
  boundary, using a callback passed through `generate_clip` and
  `_generate_clip_once` into `submit_create`. The callback reserves the complete
  6000-credit liability from live UI evidence under the shared lock, then invokes
  the strict atomic evidence/intent/click guard. No pre-helper guard is used.
- Guarded helper calls require exactly one attempt, refuse an existing output,
  refuse a missing frame rather than using context Animate, and propagate mode
  setup failure. They bypass legacy spend hooks and all post-Create confirmation,
  retry, re-submit and agent-status requests. A separate passive downloader only
  reads media IDs and responses, writes a new file exclusively, and times out
  without another UI action. Unsupported gallery layouts remain a recovery task.
- Added `execute_shared_batch`, which holds shared account ownership from parent
  preparation through per-Create evidence, charge verification, technical check,
  NAS archive and immutable receipts. It accepts no caller-provided balance or
  price. Missing outputs preserve a local unresolved intent; uncertain clicks
  preserve the shared pending charge; either prevents retries. Failed technical
  outputs stop the batch and cannot become valid parents. This entry point is
  tested but is **not wired through the still-disabled production command**.
- Added integration tests executing the real live adapter and actual helper
  functions against fake Playwright/browser objects and the real accounting
  guard. Price/output/account/entitlement drift and the 8900-credit full-cap
  boundary produce zero fake clicks. A valid fake click has durable shared
  intent and immutable evidence first. Batch tests cover two receipts, failed
  output, missing output, disconnect recovery and required pre-spend archive.
- Read-only live DOM probe (`LIVE_DOM_PROBE.json`): reused the one existing Flow
  tab under the shared account lock, without navigation or any click. The account
  matched and ULTRA was visible, but selected model/output/aspect/duration, exact
  price, balance and enabled Create were absent from that page. The reader
  correctly returned FAIL CLOSED. This does not validate the configured UI schema
  and is not permission to relax it or submit. No account address is in the probe.

Validation:

```
python3 -m unittest tests.test_flow_guard_boundary tests.test_hos009_tranche2_runner tests.test_hos009_shared_batch -q
Ran 71 tests in 3.754s
OK
bash 00_Brand/Channel-Setup/tools/check_all.sh
ALL CHECKS PASS
```

The check used the existing installed HOS node_modules through an ignored symlink.
No registered studio-core file changed; the pre-existing HOS-specific Flow helper
is not in CORE_FILES.json. No actual Create, credit spend, NAS media write,
narration/scope/trim change, media approval or publishing action occurred.

Next continuation must adopt the same canonical account protocol in every active
cross-channel Flow writer, add idempotent ai_spend reading/spend receipts and
explicit charge reconciliation, validate the configured live UI schema without
spending, and verify the real parent-still inventory. Then connect cmd_submit to
the shared path, test the full launch, and request independent elected-Chief
J2200 re-review. The old execute_batch remains a legacy test interface and must
not be selected for production. Keep the explicit cmd_submit interlock until
these requirements and J2200 review are satisfied. J2033 stays held.

Resume branch `codex/J2275-runner-safety`, draft PR445, isolated worktree
`/private/tmp/codex-j2275`. J2275 remains step 0 of the original 3-step plan:
implementation is unfinished. Released at a tested clean checkpoint because the
remaining multi-writer integration exceeds one bounded run. Nothing is on Ben.

Continuation checkpoint (sixth bounded run, 7 November 2026):

- Restored the existing PR445 branch at df064017 into /private/tmp/J2275-cont;
  do not restart from PR439 or the separate, older PR454 repair branch.
- Added export_ai_spend(target, by=...) on the shared account protocol. It exports
  confirmed charge events into the existing ai_spend record/spend schema with
  stable receipt IDs. It records the configured balance and per-film spend,
  excludes account addresses, preserves the original recorder across recovery,
  and never reduces pending/reserved/unposted liability or infers billing posted.
- Export retains account ownership and an exclusive destination lock. It rejects
  torn/corrupt destinations, duplicate IDs, identity collisions and aliasing the
  account ledger before any append. Appends and the destination directory fsync.
  A crash after the complete append is idempotent on replay; a torn append fails
  closed for explicit reconciliation. Historical report rows without IDs remain.
- execute_shared_batch accepts an explicit spend_ledger/recorder, replays known
  charges before local recovery holds, and exports in finally after the submitter
  so a confirmed click followed by download failure still records the charge.
  Unknown clicks remain PENDING and are never represented as confirmed spend.
- Six new tests cover exact-once replay/reopen, a changed recovery recorder,
  retained liabilities, private account omission, pending/not-submitted exclusion,
  append crash, corrupt/colliding destinations, lock contention, and actual batch
  download failure followed by a refused retry without duplicate spend.

Validation: 77 zero-submit tests OK (test_hos009_spend_export,
 test_flow_guard_boundary, test_hos009_tranche2_runner,
 test_hos009_shared_batch); check_all.sh ALL CHECKS PASS.
Only temporary fixture ledgers were written. No actual ai_spend ledger, Flow
browser, Create, credits, media, NAS, narration, scope, trims or publishing changed.
The required NAS offload invocation found the relay already owns the offload lock;
no duplicate offload was started.

Still unfinished: adopt the protocol in all active cross-channel writers and
make their reporting use the same destination lock; supply the canonical OWB
ai_spend destination at production entry (tests use explicit temporary paths);
validate real configured UI controls without spend; verify parent-still inventory;
connect and exercise the full production launch only after those safeguards.
The exporter is integrated only when spend_ledger is explicitly passed. It is not
blanket cross-writer adoption or a finding-3 PASS. Production cmd_submit remains
interlocked, J2200 remains FIX, J2033 remains held. Do not request final runner
review until all remaining work is complete. Remaining multi-writer integration
exceeds the bounded run; release for immediate continuation, nothing on Ben.

Continuation checkpoint (seventh bounded run, 7 November 2026):

- Resumed PR445 at 2660c8b4, preserving the original 0/3 plan and production
  interlock. Do not restart from PR439.
- Added the required reporting-writer lock adoption in canonical OWB tooling:
  https://github.com/TheLaughingGod1986/orbit-with-ben/pull/622
  (draft, commit 7197269164). ai_spend.append now resolves the destination and
  uses the exact ledger.jsonl.lock used by export_ai_spend, refuses torn/corrupt
  data and duplicate receipt IDs before append, and fsyncs file and directory.
  Recovery reports sort event timestamps so an old exported balance cannot
  supersede a newer balance reading merely because it was appended later.
- 26 OWB ai_spend regressions PASS, including actual separate-process contention
  through a symlink, unchanged corrupt ledgers, fsync and report chronology.
  A temporary-ledger integration using the actual PR445 exporter and modified
  OWB writer PASSed: two receipts plus one ordinary balance; replay added zero;
  held exporter destination lock refused the CLI append; liability stayed 6000.
- Existing 77 HOS zero-submit regressions PASS; check_all ALL CHECKS PASS. No
  real Flow browser/Create, credit, media/NAS write, narration/scope/trim or
  publishing change. The scratch-offload invocation detected another existing
  offload owner and exited without moving anything; log/done:
  ~/_desk/logs/J2275-disk.log and J2275-disk.done (exit 0).

Still unfinished: PR622 needs review/merge before its lock protects installed
report writers; active cross-channel generation writers must adopt the shared
account protocol; supply canonical report destination at production entry;
validate configured real UI, verify parent inventory and exercise the complete
launch. Production cmd_submit remains disabled. J2200 remains FIX; J2033 held.
This is a tested reporting increment, not completion or a request for final
runner PASS. Resume PR445 plus linked OWB PR622. Remaining integration exceeds
this run's bounded scope; release J2275 for immediate continuation, nothing on Ben.
Isolated worktrees: /private/tmp/codex-j2275 (HOS checkpoint) and
/private/tmp/codex-j2275-owb (OWB reporting repair).

Continuation checkpoint (7 November 2026, inventory integration):

- Resume **PR445**, branch `codex/J2275-runner-safety`, worktree
  `/private/tmp/j2275-integrate`. PR457/68680265 is a divergent partial branch;
  it lacks the actual guarded adapter, stronger launcher and spend exporter.
  Do not restart from PR439 or substitute PR457 for this continuation. No PR
  was merged or closed; Chief owns that decision.
- Ported PR457's independent-still decoder/dimension/hash inventory into the
  shared-account batch, rather than adding a second accounting implementation.
  The entire supplied inventory scope is checked under shared ownership and its
  content-addressed receipt is archived before any local intent or Create.
  Pinned hash mismatch, missing/corrupt/small images, or a frame changed after
  preparation stop before browser entry. Output receipts include inventory ID
  and actual input hash. `inventory_rows` must receive the full locked scope at
  eventual production entry; absent that, it checks the current batch.
- 81 zero-submit regressions pass, including real synthetic image decoding,
  missing later asset preventing the first submit, pinned-hash mismatch, and
  changed input after verification. Existing fake-browser tests remain intact.
  No real media inventory was read or approved, and no actual Flow Create ran.

Still incomplete at **1/3**: all active cross-channel generation writers must
adopt the same account protocol; production must use the canonical OWB spend
report destination (and PR622 lock contract), full inventory scope and shared
batch; configured live UI schema needs read-only validation; real parent/media
inventory remains unverified. Then test complete launch and obtain elected-Chief
J2200 re-review. Keep cmd_submit disabled and J2033 held. No Ben action needed.

Disk offload ran safely with the existing tool, detached session
`j2275-disk-1419`; log `~/_desk/logs/J2275-disk-1419.log`, completion file
`~/_desk/logs/J2275-disk-1419.done`. It found nothing old enough to move and
reported 7,924 MB free. It deleted nothing on the NAS. Three zero-byte untracked
OWB blockers were preserved in `~/_desk/rescue/j2275-1794061168964108000/`.

Validation for this checkpoint: 81 zero-submit tests OK; repository `check_all.sh` ALL CHECKS PASS (existing package warnings only); `git diff --check` clean. Existing installed node_modules reused via ignored symlink.
