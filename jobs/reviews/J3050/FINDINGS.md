# J3050 — billing evidence proposal, 18 November 2026

Proposal only, not a deployed guard or generation authorization. Zero API requests,
zero POSTs, zero credit or cash spend in this investigation. All tests are synthetic.

## Contract and evidence

Primary source, retrieved 18 November 2026:
https://elevenlabs.io/docs/api-reference/user/subscription/get
The documented GET response uses a nested Price object, `current_overage`, with
`amount` (example decimal string `"0"`) and `currency` (example `"usd"`). It does
not document `current_overage_amount` as a raw response property. The endpoint
separately documents extension limits, entitlement flags and subscription status;
zero overage alone is not proof that billing extension is disabled.

Sanitized captured projection (not an entire raw response):

```json
{"current_overage":{"amount":"0","currency":"usd"}}
```

This pair was independently inspected in J2806's local execution transcript,
step_index 69, created 2026-11-17T16:12:03Z. The capture also lists the raw
subscription keys, including `current_overage`. No credentials or account
identifiers are included here. Local source: the J2806 session transcript cited
in EAR_REVIEW_J3046.md (HOS PR648). That transcript is local evidence, not a
portable raw-response archive. The reviewed projection has the API's documented
shape, while J2806_PROVENANCE.json's subscription_before/after use the flattened
pair `current_overage_amount/current_overage_currency`, both `"0"/"usd"`.
J2664_PROVENANCE.json is local/unverified: no such file is tracked in the
repository. That citation is not relied on as portable evidence.

J3045's local PREFLIGHT.json (checked_at 2026-11-18T11:57:43.078008+00:00;
HOS PR647 outcome) retained eight selected subscription fields and a failed
literal-name search for `current_overage_amount`, with no matches. It did NOT
retain `current_overage.amount/currency`. Thus absence of the flattened key
establishes a mapping mistake in that search, NOT absence of the documented
nested evidence. Conversely, the 17 November zero cannot prove the 18 November
nested amount. PR648's diagnosis is supported as a key-path explanation, but any
claim of unchanged account state across the two dates exceeds retained evidence.

| Field | J2806 retained provenance | J3045 retained preflight |
|---|---|---|
| tier / status | creator / active | creator / active |
| character_count / limit | 41250 before, 43725 after / 121114 | 62352 / 121114 |
| both extension limits | 0 | 0 |
| both extension flags | false | false |
| overage | flattened zero / usd, nested prior capture | nested value not retained |
| billing period / reset | retained | not retained |
| pending reconciliation | recorded complete then | explicitly not completed |

These are observations at separate times, not evidence of continuous state.
No fresh account GET was needed or made for this bounded proposal.

## Proposed evidence rule

The standalone offline normalizer requires explicit source classification.
Raw API evidence requires the documented nested object and refuses either
flattened key even alongside valid nested evidence. Historical flattened
provenance is accepted only as labelled historical evidence; it never substitutes
for a current response. Only historical_provenance permits both representations;
when both exist, both must be complete,
valid and agree. Malformed nested evidence cannot fall back to a flattened zero.
No recursive name search, `.get(..., 0)`, null-to-zero conversion or inferred zero.
Reject absent/null/non-numeric, negative (including signed zero), nonzero,
nonfinite, integer/boolean/float amounts, non-canonical zero strings such as
`"00"` or `"000.000"`, missing/unknown currencies, extra nested Price
fields, contradictory or incomplete dual representations, and unknown sources.
Extra subscription fields remain outside this narrow parser, not silently
validated. A valid pair returns evidence with `authorizes_generation: false` and
`freshness_assessed: false`. A caller-supplied source label proves no freshness.

Before integration review, the raw-body JSON loader must reject duplicate keys
at every object level (including subscription and Price). This dictionary-only
function cannot recover duplicates discarded by a default JSON loader and is
not a raw-body validator. Exact two-field Price validation deliberately fails
closed on future extra fields. Live subscription responses already contain
some undocumented top-level fields; schema drift requires separate review.

The proposal is under jobs/reviews/J3050, unimported by production tools.
It cannot assess freshness, account identity, HTTP success, active plan/tier,
extension flags/limits, pending charges/reconciliation, live tariff and margin,
remaining credit, recorder lock, pause, or scope validity. Other billing fields
`open_invoices`, `has_open_invoices`, `next_invoice`, `pending_change` and
top-level `currency` are out of scope too. Zero current overage does not cover
previously invoiced overage; account/Price currency consistency needs its own check.
Each remains mandatory
in any separately reviewed future integration. Unknown at ANY such gate means
no POST. No tariff quoted historically is authority for future production.

## Unresolved and handoff

The nested pair at the J3045 instant cannot be recovered from its retained
preflight alone. No statement that the account stayed unchanged is justified.
Claude must review the evidence rule independently, especially source separation,
strict type choices and refusal behavior. The elected Chief then decides the
proposal; there is no automatic retry timer or permission to deploy it here.
J3043/J3045 allowance remains permanently closed, unused (0 POSTs); neither that
allowance nor earlier ones may be pooled or renewed. J2808 rejection and J2035 /
J2171 holds stay intact. Future production requires a separate explicit scope and
decision, not completion or merger of this proposal.

Validation: `python3 -m unittest discover -s jobs/reviews/J3050 -p 'test_*.py' -v`
— updated tests, reviewer probes and repository checks are recorded in VALIDATION.md.

## J3057 correction handoff

All three required changes and recommendations 4–9 from J3052 REVIEW.md
(PR653, 80dc8fe0) are addressed within this offline proposal. Original Claude
request: desk6978888233. J3053 request changes at desk6983820915 supersedes
earlier desk6980094321 acceptance. No documentation recommendation is deferred.
Duplicate-key rejection in a future raw-body loader, freshness/account checks
and all billing checks listed above remain mandatory prerequisites for any
separate integration review; this function does not implement or verify them.
A separate independent Claude review of the updated exact commit followed by
an elected-Chief decision is required; the author must not merge this correction.
