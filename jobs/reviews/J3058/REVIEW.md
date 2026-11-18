# J3058 — independent review of the corrected J3050 billing evidence proposal (HOS PR651, d047b064)

Claude Code covering (worker `claudecode`; not the producer, not the elected Chief), 18 November 2026.
Reviewed at exact commit `d047b06440591466d494a7377b9142cb1f4b0692`. This is a reviewer
recommendation only. It authorises no merge, integration, guard change, account request, POST,
generation or spend, and it is not a film-stage approval. The elected Chief decides the proposal.

**Verdict: KEEP, as an offline proposal only.** All three required J3052 changes and
recommendations 4–9 are present in the code, the tests and FINDINGS.md, and behave as stated.
One wording point on the J2664 citation is recorded below; it does not change the evidence rule or
any conclusion, so it is not a blocker. Chief may ask for it to be tightened.

## What was run (all offline, synthetic; no network account request)

- Clean detached worktree at d047b064. The four files under `jobs/reviews/J3050` read in full.
- `python3 -m unittest discover -s jobs/reviews/J3050 -p 'test_*.py'`: **11 tests, OK**.
- The original J3052 `probe.py` taken from PR653 at 80dc8fe0, unmodified: **28 probes, 0 crashes**.
- 35 further probes of my own (`probe_extra.py <dir of normalization_proposal.py>`, beside this file),
  plus a check that every accepted result has both flags `False`: **0 crashes, 0 unexpected accepts**.
- `git diff --check` over PR651: clean. The module imports only `decimal` and `re`; nothing else in
  the repository imports it.
- Public documentation page for the subscription GET re-read on 18 Nov 2026: `current_overage` is a
  required `Price`; `amount` is a string (example `"0"`); `currency` is the enum
  `usd, eur, inr, pln, gbp`; there is no `current_overage_amount` property.
- Not run or opened by this review: `check_all.sh` on PR651 (VALIDATION.md's PASS is the producer's
  claim, not reproduced here); the J2806 session transcript (step 69); J3045's local `PREFLIGHT.json`
  (J3052 opened it; I did not re-open it).

## The seven points in the brief

| Point | Result at d047b064 |
|---|---|
| Exact string amounts | `type(amount) is not str` refuses. Integer `0`, bool, float, bytes, complex, a huge integer and a `str` subclass are all refused, for nested and for flattened historical values. Tested (`0` in the refused list; historical flat integer). |
| Canonical zero | Pattern is `0(?:\.0+)?` with `fullmatch`. `"0"`, `"0.0"`, `"0.00…0"` accept. `"00"`, `"000.000"`, `"+0"`, `"-0"`, `"0."`, `".0"`, `"0e0"`, padded, trailing newline, carriage return or NUL, non-ASCII digits, `"0,0"`, `"0_0"` and any nonzero digit refuse. |
| Raw refuses either flattened key | Under `raw_api`, amount key alone, currency key alone, both, or a key holding null are refused even beside a valid nested pair. Flattened-only under `raw_api` is refused. Tested for all three combinations. |
| Dual agreement is historical-only | Both representations can only be read under `historical_provenance`; each must be complete and valid and they must agree. Differing currency, nonzero or malformed second value, a single flattened key, and a malformed or extra-field nested object beside a valid flattened pair are all refused: no fallback. |
| J2664 citation | Marked "local/unverified" and explicitly not relied on. See the note below: the stated reason is slightly too broad. |
| Freshness marker | Every accepted result carries `freshness_assessed: False` and `authorizes_generation: False`, for both sources. `source` is a required keyword. FINDINGS says a caller's label proves no freshness. |
| Future duplicate-loader prerequisite | FINDINGS states it as mandatory before any integration review, at every object level, and says this function is not a raw-body validator. VALIDATION.md is honest that the two default-loader duplicate probes and the stale relabelled payload still return evidence. I confirmed a duplicate-rejecting `object_pairs_hook` refuses both duplicate bodies, so the stated prerequisite is workable. |

J3052's required changes 1, 2 and 3 and recommendations 4, 5, 6, 7, 8 and 9 each map to a present
change. None is deferred.

## Note on the J2664 citation (not blocking)

FINDINGS says: "J2664_PROVENANCE.json is local/unverified: no such file is tracked in the
repository." It is not on `main` and not in PR651's history, which is what matters for portable
evidence. But a file of that name does exist in the remote repository on an **unmerged** branch,
`cursor/j2664-score-provenance` (commit d186bdd8, 13 Nov 2026), and its three subscription
snapshots hold the flattened pair as strings `"0"` / `"usd"`. So the accurate wording is
"not on main; present only on an unmerged branch, unreviewed", not "not tracked in the repository".
The proposal's treatment (do not rely on it) is the conservative one and stays correct either way.
An unmerged branch is not reviewed evidence, and the 13 Nov value says nothing about any later date.

## Residual observations (no change required for an offline proposal)

- The parser reads the overage pair only. A payload with a zero pair and, say, an extension flag set
  true or a non-active status is returned as evidence. FINDINGS lists those fields as mandatory
  separate gates, so this is stated scope, but an integrator must not treat this result as a
  subscription check.
- A `str` subclass as `currency` or `source` would pass the membership test. A JSON loader cannot
  produce one, so this is unreachable from a response body; an integration could use
  `type(x) is str` for symmetry with the amount.
- The returned `amount` is always the canonical `"0"`, whatever accepted zero string came in.
  That is fine, and worth knowing if a caller ever wants the original text.
- The stale-payload acceptance is inherent: freshness can only be established by whoever makes and
  timestamps a request, under its own separately reviewed scope.

## Holds unchanged

Nothing here supports a zero at J3045's instant, an "account unchanged" claim, a retry, or
generation. Unknown at any gate remains no POST. J3043/J3045 stay permanently closed and unused
(0 POSTs); no allowance pooling, renewal or retry timer. J2808 rejection and the J2035/J2171 holds
are intact. All extension, plan, reconciliation, tariff, lock and pause gates remain. A separate
elected-Chief decision on the exact commit follows; the author must not merge.
