# J3141 — fail-closed score billing guard (proposal only)

19 November 2026. This is a proposed change for independent review. It is not
integrated, not deployed, and not an allowance.

No account call, no POST, no generation, no billing change, and no edit to the
live ElevenLabs guard were made while writing it. Tests use synthetic fixtures
only.

## Where it starts

The nested overage rule is copied from the reviewed offline mapping, HOS PR651
commit `d047b06440591466d494a7377b9142cb1f4b0692`. J3059 kept that commit
unmerged and unintegrated. This proposal does not import it and does not merge
it.

Desk 7005927729 is the field comparison this guard is built to survive:

- A fresh subscription GET is the only overage evidence that can be considered.
- The value that has to be kept is nested `current_overage.amount` and
  `current_overage.currency`.
- A flattened `current_overage_amount` is not raw evidence. A saved preflight
  that dropped the nested object cannot stand in for zero.
- Unknown billing evidence means no POST.
- The J3043/J3045 allowance stays closed unused under J3047. This module does
  not read it, renew it, or pool it.
- v01 and v02 stay rejected. J2035 and J2171 stay held.

## What a pass means

`MeterBoard.decide` returns `outcome: pass_once` only when every check below
passes. The returned token always has:

- `authorizes_generation: false`
- `opens_allowance: false`
- `integrated: false`
- `network_calls: 0`
- `would_allow_posts: 1`
- `retries: 0`

`consume` burns that one token. It still does not perform a POST. A second
`decide` or `consume` on the same board raises `retry_or_shared_meter` or
`retry`. A refusal burns the board too, so a caller cannot probe until a later
call passes.

There is no environment switch that turns the guard off.

## Checks, in order

1. Any extra argument, including a transport or fetch callback, is
   `network_forbidden`.
2. The board accepts one `decide`. The second is `retry_or_shared_meter`,
   including when two callers race.
3. HTTP status must be the integer 200.
4. `fetched_at` and `now` must be timezone-aware UTC. A negative gap is
   `inconsistent_clock`. A gap above 60 seconds, or a naive time, is `stale`.
   Exactly 60 seconds still passes.
5. The body must be raw bytes. The parser rejects duplicate keys at every
   object. A dict, a string, or a non-object is `malformed_body`.
6. The key set is exactly the sixteen fields listed in
   `score_billing_guard.REQUIRED_KEYS`. An extra key is `unknown_field`.
   Either flattened overage key is `overage`, even beside a valid nested
   object.
7. Entitlement must be tier `creator`, status `active`, billing period
   `monthly_period`. Anything else is `unknown_entitlement`.
8. Both extension limits must be integer 0 and both extension flags must be
   false. Otherwise `extensions`.
9. `has_open_invoices` must be false, `open_invoices` must be an empty list,
   and `next_invoice` must be null. Otherwise `invoices`. `pending_change`
   must be null.
10. Nested `current_overage` must be exactly `amount` and `currency`. The
    amount must be the canonical zero string accepted by the reviewed mapping
    (`0`, `0.0`, `0.00`, …). Integer zero, a blank, a sign, a non-zero, and a
    non-canonical string such as `00` or `0e0` are `overage`. The currency
    must be one of `usd`, `eur`, `inr`, `pln`, `gbp`, and the top-level
    `currency` must be the same string. The original amount string is kept on
    the token.
11. `character_count` and `character_limit` must be non-negative integers,
    with the limit at least the count. The reset unix time must fall after
    the freshness window. Remaining capacity is `character_limit -
    character_count`.
12. The request must be holder `hos009-score`, attempt integer 1, endpoint
    `/v1/music`, model `music_v2`, `force_instrumental` true, length exactly
    180000 ms, and query `output_format=mp3_44100_128`. Estimated credits must
    be an integer from 1 to 3000 inclusive. Cash must be the string `0`.
    Above 3000 credits is `budget`. Any other cash value is `cash`.
13. Remaining capacity must be at least the estimate, or the result is
    `insufficient_capacity`. The boundary 3000 remaining and 3000 estimated
    passes. 2999 remaining does not.
14. The lease must be exclusive, peers integer 0, hosts exactly
    `["hos009-score"]`, acquired at the same `fetched_at`, and
    `observed_character_count` equal to the body. Anything else is
    `shared_meter`, `stale_lease`, or `inconsistent_meter`.

The token stores `body_sha256` of the raw bytes. `consume` accepts only that
digest and a token whose `authorizes_generation` is still false. A mismatch
burns the token.

## Integration path

Do not wire this in on the strength of this proposal.

Live path today, unchanged by this commit:

1. `04_Audio/tools/generate_music_bed.py` `compose` can POST `/v1/music` for
   3000–600000 ms when someone passes `--generate`.
2. `el_client.request` calls `el_guard.before_spend`.
3. That live guard estimates cost as the prompt's character length, subtracts
   `character_count` from `character_limit`, and does not read nested overage,
   entitlement, extensions, invoices, freshness, or a cash cap.
4. `EL_GUARD_OFF=1` skips that live guard. This proposal has no such switch,
   and this commit does not add one to the live guard.

A later integration is a separate diff, and only after J3142 records a pass
on this exact commit and J3143 writes an explicit scope. That diff would:

1. Leave `el_guard.py` at least as strict as it is now. Do not add a bypass
   and do not lower its checks to match this proposal.
2. Add a score-only entry point that imports this module. Do not point the
   existing `--generate` path at it.
3. Take the live one-recorder lock first. If it is held, stop.
4. Perform one GET `/v1/user/subscription`. Store the raw bytes, the status,
   and the UTC time. Do not keep a flattened projection in place of the body.
5. Build the lease from that same body and from the lock (peers 0 only when
   this flight holds it). Call `decide`. On any refusal, release the lock,
   record the code, and stop. Do not GET again.
6. On `pass_once`, `consume` with the same body digest, then one POST
   `/v1/music` for exactly 180000 ms, `music_v2`, `force_instrumental` true.
   The live guard still has to pass that POST. If the two guards disagree,
   do not send it.
7. On any non-200, timeout, or exception, stop. The board stays burned. No
   second POST and no second GET.

Until that diff exists, `generate_music_bed.py --generate` must not be used
for this HOS 009 score. This commit does not change that script, so it also
does not itself block a manual run.

## Risks

- A real subscription body has more than these sixteen keys. Those extra keys
  fail closed as `unknown_field`. That is intentional. Widening the allowlist
  needs a separate review against a redacted raw schema. This proposal does
  not capture or require a live body.
- The credit estimate is declared by the caller. This guard refuses an
  estimate above 3000 or a cash figure other than `0`. It does not know the
  live music tariff. A declared 3000 can still be wrong. J3143 has to name
  the estimate before any POST. Guessing a tariff is not a pass.
- The shared subscription can move on another machine between the GET and the
  POST. The in-process board does not see that. Binding
  `observed_character_count` to the body catches a stale projection. It does
  not catch a spend that happens after the GET. The one-request rule is the
  control this proposal can actually enforce.
- `json.loads` without the duplicate-key hook would hide a repeated field.
  Callers must pass the raw bytes. A pre-parsed dict is `malformed_body`.
- The 60-second window will refuse a slow caller. That is the stale check,
  not a reason to lengthen it here.
- Historical flattened provenance remains evidence only inside the unmerged
  mapping. This guard refuses it.

## Holds this commit leaves in place

- J3047 closure of the unused J3043/J3045 allowance.
- J2808 rejection of score v01 and v02.
- J2035 and J2171 blocked.
- No public schedule change and no new ready-by promise.

## Review

```bash
python3 -m unittest discover -s jobs/reviews/J3141 -p 'test_*.py' -v
```

`HASHES.txt` pins `score_billing_guard.py`. The review commit is the pin for
the whole proposal, including this note and the tests.
