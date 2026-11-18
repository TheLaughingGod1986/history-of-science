# J3052 — independent review of the J3050 billing evidence proposal (HOS PR651, ff02370b)

Claude Code covering (worker `claudecode`, not the producer and not the elected Chief), 18 November 2026.
This is a reviewer recommendation only. It authorises no merge, integration, guard change, account
request, POST, generation or spend. The Chief decides the proposal.

**Verdict: FIX, three required changes, then acceptable as an offline proposal only.**
The evidence reasoning in FINDINGS.md holds. The code is stricter than its tests show in most
branches, but two accept-paths contradict the rule the proposal itself states.

## What was checked

- PR651's four files read in full; its 8 synthetic tests run in a clean worktree: 8 pass.
- 28 extra synthetic probes (`probe.py <dir of normalization_proposal.py>`; no network, no account).
- Official contract re-read on 18 Nov 2026 (public documentation page only):
  `current_overage` is a required `Price` object; `amount` is a **string** (example `"0"`);
  `currency` is an enum of exactly `usd, eur, inr, pln, gbp`; no `current_overage_amount` property
  exists. The proposal's currency list and nested shape match this exactly.
- Tracked evidence on main: `J2806_PROVENANCE.json` (both snapshots hold the flattened pair as
  strings `"0"` / `"usd"`), `EAR_REVIEW_J3046.md`, `J3045_evidence/OUTCOME.md`.
- J3045's local `PREFLIGHT.json` (the path OUTCOME.md names): it retains exactly eight subscription
  fields, `missing_required_fields: ["current_overage_amount"]`, an empty path list, and **no
  `current_overage` value of any shape**. FINDINGS' table matches it.
- Not checked: the J2806 session transcript (step 69) was not opened by this review; the nested
  capture is taken from PR648's written account of it.

## Evidence claims

| Claim in FINDINGS | Result |
|---|---|
| Official response is nested; the flattened name is not a raw property | Confirmed against the documentation |
| J3045's failure was a literal-name search, not proof the nested value was absent | Confirmed by PREFLIGHT.json |
| The nested pair at J3045's instant cannot be recovered | Confirmed: nothing was retained. No zero may be inferred for 11:57:43Z on 18 Nov |
| The 17 Nov zero says nothing about 18 Nov; no "unchanged account" claim | Agreed. Usage moved from 43,725 to 62,352 between the two readings, so the account demonstrably was not static |
| `J2664_PROVENANCE.json` uses the flattened convention | **Not verifiable from the repository**: no file of that name is tracked on main or in its history (see required change 3) |

One addition: PR648 records that the 13 and 17 Nov captures were made with
`sub.get("current_overage") or {}` and `.get("amount")`. That is the tolerant pattern this proposal
bans. The retained values are real strings, so the historical zero stands, but the flattened records
are a derived projection and should never be described as raw.

## Refusal branches (all exercised)

Refused, as the rule requires: payload not a plain dict; unknown, null, list or bytes source; no
overage key; nested null, list, empty, one-field or extra-field object; amount null, bool, float,
list, dict, str subclass, empty, words, NaN, Infinity, exponent, padded, trailing newline, `+0`,
`0.`, signed zero, negative, nonzero, non-ASCII digits, huge integer; currency null, empty, upper
case, unknown, number, list; one flattened key alone; flattened-only under `raw_api`; contradictory
or malformed second representation; error envelopes; a response wrapped under another key.
Every valid result carries `authorizes_generation: False`.

Accepted, and these are the findings:

| Probe | Result | Assessment |
|---|---|---|
| `raw_api`, nested amount integer `0` | ACCEPT | Contradicts the contract (string). Untested either way |
| `raw_api`, nested pair plus flattened keys | ACCEPT (tested as intended) | A documented raw response has no flattened keys, so this payload is a derived record labelled raw |
| `raw_api`, amount `"00"` or `"000.000"` | ACCEPT | Non-canonical zero |
| Duplicate JSON key, `"5"` then `"0"`, parsed by the default loader | ACCEPT | Outside the function, but nothing warns the integrator |
| A stale payload labelled `raw_api` | ACCEPT | The label is the caller's word; the result repeats it with no capture time |

## Required changes (exact)

1. **Amount must be `str`.** Replace `type(amount) not in (str, int)` with `type(amount) is not str`.
   The contract says string and no retained record holds an integer. Change the dual-representation
   test's flattened `0` to `"0"`, and add `0` to the refused amounts.
2. **`raw_api` refuses flattened keys.** If `source == 'raw_api'` and either flattened key is present,
   raise `EvidenceRefused`. The both-must-agree rule then applies to `historical_provenance` only.
   Move `test_matching_dual_representations` and the dual-contradiction cases to the historical source,
   and add one test that nested plus flattened under `raw_api` is refused. Reword the FINDINGS
   sentence "When both representations exist…" to say this.
3. **Correct the J2664 citation.** Name the tracked file that actually holds the 13 Nov flattened
   pair, or mark that record as local and unverified.

## Recommended (not blocking the offline proposal; mandatory before any integration review)

4. Canonical zero only: `0(?:\.0+)?` in place of the general decimal pattern.
5. Add tests: historical source with nested-only evidence; `"00"`; each new refusal above.
6. State in FINDINGS that the raw body must be parsed with duplicate keys rejected, at both levels.
7. Add `'freshness_assessed': False` to the result (or take and echo a caller-supplied capture time),
   so a `raw_api` label cannot be read downstream as "current".
8. Name the contract's other billing fields in the out-of-scope list: `open_invoices`,
   `has_open_invoices`, `next_invoice`, `pending_change` and the top-level `currency`. Zero current
   overage does not cover overage already invoiced, and the Price currency could be cross-checked
   against the account currency.
9. Note that the live response already carries top-level keys the documentation does not list, so the
   exact two-field check on `Price` may one day refuse a legitimate response. That fails closed and is
   the right default; it should be a stated, deliberate choice.

## Holds unchanged

J3043/J3045 allowance stays closed and unused (0 POSTs). J2808 rejection and the J2035/J2171 holds
are intact. Nothing here supports a zero value at J3045's instant, a retry, or generation.
