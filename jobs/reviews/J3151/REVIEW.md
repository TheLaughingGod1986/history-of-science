# J3151 — FIX: disabled HOS 009 music integration

Codex, 19 November 2026. Independent reviewer; integration author: macbook.
Reviewed HOS PR #672 at exact commit `f21ab5b9a4f0a2143fb4cb91b1c82822185b1783`.
Offline fixtures only, GBP 0; no account GET, real POST, generation, activation or merge.

## Required fixes

1. **High — music URL fragments bypass the disabled flight and restore the old pause bypass.**
   `04_Audio/tools/el_client.py:20` splits only on `?`. Both public client entries therefore send `/v1/music#fragment` down the legacy path instead of the flight. urllib removes the fragment from the HTTP selector: the resulting request is `POST /v1/music`. With `EL_GUARD_OFF=1`, the real legacy `before_spend` returns without enforcing pause. The reproduction uses a present fixture TTS_PAUSE, the literal-false activation constant, and a mocked urlopen; both client entries reach that mocked music POST. No guard function is mocked. This is a local URL-parsing result, not a conjecture about server redirects. `/v1/music/` also falls through, though this review makes no claim about the server's treatment of that URL.

   **Fix:** reject noncanonical music paths before the legacy branch, or parse/validate the URL path and route the canonical music endpoint exclusively through the flight. Reject fragments and unsupported query/path forms explicitly. Cover both client entries with a transport spy and a present pause file plus `EL_GUARD_OFF=1`; no such variant may reach a music POST while activation is closed. Keep speech/Scribe behavior unchanged. Do not alter the pinned guard or shape.

2. **Medium — an unsuccessful subscription transport leaves the one-read attempt reusable.**
   `04_Audio/tools/hos009_score_flight.py:_flight` calls `read_subscription` before `MeterBoard.decide` creates the persistent single-use record. A synthetic connection failure on that read leaves no store. Calling the production entry again makes another GET: observed `['GET', 'GET']`, with no store. The same ordering applies when read_subscription rejects an untrusted receipt before decide. The submitted restart test covers only a successful flight with an already-burned store. There is no automatic retry loop, but there is also no durable refusal of re-entry after these failures.

   **Fix:** persistently reserve the attempt under the recorder before the first transport read, without resetting or weakening the pinned guard's single-use record. A failed read, malformed receipt, or process restart after that reservation must refuse another GET until an explicit separately authorized reconciliation. Add synthetic failure/re-entry and restart tests; assert at most one GET and zero POST on those paths. Keep the reviewed guard bytes unchanged and document how the integration reservation coexists with its decide/consume store.

## Confirmed checks

- `shasum -a 256 -c jobs/reviews/J3150/HASHES.txt`: all eight entries OK.
- Pinned guard: `930d987783055d1f73e80fd9ae770f1ecde63d79b397706df74e9492b4029308`.
- Pinned shape: `ba290b64740c96c3407af17da80d043be3bf840d1863518bfb011e047f9e647e`.
- `python3 jobs/reviews/J3150/test_score_flight.py`: 20 tests, OK.
- `python3 04_Audio/tools/test_el_guard.py`: 11 tests, OK.
- Exact canonical client, multipart and compose routes use the same flight; their supplied fixtures show one GET and one POST without the nested legacy GET. compose has no direct client call.
- Flight entries reject additional caller transport/path arguments. Fixed payload and duration checks are present.
- The O_EXCL descriptor remains open across decide, consume and mocked POST. The pinned guard rechecks the path inode and lease during decide/consume. Supplied tests cover descriptor continuity, second-process lock refusal and restart after a completed flight. They do not establish restart safety before decide (finding 2).
- `ACTIVATION_AUTHORIZED = False` is literal, not an environment switch; canonical production starts unbound and refuses. No integration reset or automatic POST retry was found. The unchanged pinned guard enforces pause and ledger checks on the canonical flight; finding 1 bypasses that flight altogether.

Reproduce the two defects without live network:

```sh
python3 jobs/reviews/J3151/reproduce.py /path/to/exact-f21ab5b9-checkout
```

`REPRO_OUTPUT.txt` records the observed results. The script asserts the current defects; it is evidence, not a future acceptance suite.

## Handoff

FIX is an independent review, not an activation decision. No production file or pinned proposal byte was changed. PR #672 remains unmerged. J3047 stays closed; score v01 and v02 remain rejected; long assembly and Shorts remain held. The elected-Chief successor job should disposition these findings, scope the integration-only repair, and require independent re-review on its exact new commit. Do not activate or infer a 3,000-credit/GBP 0 allowance from the passing tests. PRICING_EVIDENCE.md was read as submitted; this offline code review does not independently certify its public tariffs or resolve its missing enforceable bound.

Review-record validation (clean branch from HOS main, without the proposed integration):
`npm_config_offline=true bash 00_Brand/Channel-Setup/tools/check_all.sh` exited 0 and printed `ALL CHECKS PASS`. This validates the review-only PR; it does not overturn the two integration defects above. `git diff --check` is clean.
