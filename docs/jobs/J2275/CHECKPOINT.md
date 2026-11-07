# J2275 repair checkpoint — 7 November 2026

Worker: codex. Scope: HOS PR439 (`1772cd52`) / J2200 findings. **INCOMPLETE. No merge, system PASS or generation release.**

This branch imports the reviewed PR439 commit onto current main and preserves the exact 20-row v05 scope, locked narration and existing trims. No browser, Flow submit, credit spend, NAS write or publishing action occurred. Test clips were synthetic temporary fixtures only; no audio or moving-video perception is claimed.

## Changes implemented and tested

- The next take no longer releases its own credit reservation. At live 8900 the full 6000 liability leaves 2900 and is refused; 9000 is the exact floor boundary. Pending and spent amounts remain conservatively liable until explicit reconciliation exists. Negative balances/spends/reservations fail closed. **This is deliberately conservative, not a complete posted/unposted reconciliation implementation.**
- An archive directory must pass write/read preflight before the batch can spend. Production additionally requires the mounted approved NAS root. Exclusive archive creation accepts identical retries and rejects different existing hashes without overwriting or deleting them. Part-specific paths prevent cross-part name collisions. Per-take receipts are immutable and include archive/input hashes plus the supplied balance/account/price evidence. Evidence is not yet live per-Create proof (see remaining work).
- Technical checks require a silent, single-video-stream, decodable 8-second 16:9 HD output (at least 1280×720). Invalid output is archived, recorded FAILED and cannot advance the batch. Missing output remains unresolved. In-scope parents are selected from a verified ledger version/hash with a matching archive, rather than blindly t1 or an older tranche. A technical PASS never means perceptual KEEP.
- Detached commands carry media, archive, ledger, writer lock, PID, repo and reservation arguments. Each command uses unique log/done names; live PIDs override stale done files, and the process lock covers the entire command. Existing outputs/receipts are preserved. Tests execute the emitted shell command against a fake entry point with spaces in paths.
- Production `submit` explicitly refuses this partial repair even when armed. Remove that refusal only after completing the remaining repairs and testing them; do not bypass J2200/J2033 gates.

## Remaining work — continue the same job

1. J2200 finding 2: read selected model/output controls, exact displayed price, balance, unique account and Ultra entitlement **under the canonical lock immediately before every actual Create**, including after the adapter configures a project. Environment strings are not evidence. Exercise the real adapter with a fake browser and prove zero clicks on all drift cases. Persist the live proof with each immutable receipt.
2. J2200 finding 3: implement the canonical cross-channel generation writer lock and durable shared reservation/pending/spend ledger. Current production state/locks remain worktree-local. Derive other reservations from shared state; integrate idempotent shared ai_spend receipts. Model explicit posted/unposted reconciliation rather than permanently conservative double-accounting. Test separate worktrees, competing processes, interrupted submits and crash recovery. Never automatically retry an uncertain Create.
3. Verify real start-still inventory paths/hashes before any spending, or implement and test the separately guarded displayed-zero preparation route. Existing `live_still_maker` still stops; no inventory has been checked in this session.
4. Revisit all six original findings after integration. Expand tests for actual adapter, cross-worktree concurrency and crash recovery; rerun the full checks. Request elected-Chief re-review of J2200 only when complete. J2033 remains blocked and J2034 still owns eventual picture review.

## Validation

`python3 -m unittest tests.test_hos009_tranche2_runner -v`: **34 tests PASS** (23 existing + 11 regression tests).

`bash 00_Brand/Channel-Setup/tools/check_all.sh`: **ALL CHECKS PASS**, using an ignored symlink to the existing HOS node_modules and a temporary npm cache. Existing package title/caption warnings remain warnings.

`git diff --check`: PASS.

Queue plan remains 1/3: brief reviewed; implementation and final integrated verification unfinished. Release to the queue, not review/approved. Nothing is required from Ben.

## Second checkpoint — 7 November 2026, Codex

**Still incomplete; production submit remains unconditionally disabled.** The remaining live-adapter/shared-writer integration and fake-browser coverage exceed this bounded run. This is a work checkpoint, not a request for J2200 PASS.

Added a durable `SharedFlowState` implementation with machine-wide defaults (`~/_desk/state/flow`, `~/_desk/locks/flow-generation.lock`), independent of worktree/channel environment. It uses the existing nonblocking `WriterLock` implementation, atomic replacement and file/directory fsync. Reservations for other owners are derived from the journal. An impending take retains its full reservation; unresolved Creates survive reopening and refuse both same-ID retries and new submits. Completed/failed charges stay unposted liabilities until explicit external-charge/balance evidence is recorded. Duplicate charge reconciliation is refused. Spend outbox payloads have stable IDs.

**Integration limitations:** the new shared state is tested in isolation and is not wired into `execute_batch` or the real adapter. Other Flow writers have not adopted this new machine-wide lock. The idempotent payload is not yet delivered to `ai_spend`; it is not a claim that spend reporting is implemented. No existing cross-channel Flow writer lock was found in the inspected Flow adapter/mint code; reconcile this contract with every actual writer before enabling production. The conservative legacy arithmetic remains in use for fake-batch tests.

Added `verify_still_inventory`: independent start stills need existing files, matching stable hashes, a decodable single image stream, and 16:9 HD dimensions. The disabled production path now calls it for the entire scope and archives an immutable inventory receipt before batch selection. Missing assets fail closed, with no automatic still generation. Real media inventory was not read or approved; extracted continuation frames still require the existing proven-parent path and further integration review.

Validation (synthetic local fixtures, no browser calls):

```text
python3 -m unittest tests.test_hos009_tranche2_runner -q
Ran 41 tests
OK
bash 00_Brand/Channel-Setup/tools/check_all.sh
ALL CHECKS PASS
git diff --check
PASS
```

Seven new tests cover floor/other-channel reservation boundaries, durable uncertain-Create recovery, delayed deduction reconciliation, competing processes sharing one lock, checkout-independent defaults, corrupt-journal fail-closed recovery, and missing/corrupt/small/valid start stills. Full checks reused the installed HOS node_modules via an ignored symlink and a temporary npm cache. No media, Flow credits, YouTube changes or film approvals.

Resume at 1/3. Next: integrate per-Create selected-control/account/Ultra/price/balance proof under the shared writer lock; wire reservations/charges and idempotent ai_spend delivery; test the actual adapter with a fake browser and crash/retry cases; revisit all six J2200 findings; then full validation and independent elected-Chief re-review. J2033 remains blocked; J2034 retains eventual perceptual picture review. Nothing needs Ben.
