# J3144 — revised fail-closed score billing guard (proposal only)

19 November 2026. This revises the offline proposal at `c9ef1e0aa51a363971f5de1f5648ece6826eec12`. It is not integrated, not deployed, and not an allowance.

No account call, no POST, no generation, no billing change, and no edit to the live ElevenLabs guard were made while writing it. Tests use synthetic fixtures and redacted key names only.

J3142 (HOS PR 668, `18c281b046f74c94aa2ebb101ecfaeec5ee10a5f`) recorded FIX. Chief desk 7013542642 ruled NOT YET. This commit answers that review and desk points a–e. It does not authorize a score.

## What a pass means

`MeterBoard.decide` returns `outcome: pass_once` only when every check below passes. The returned token always has `authorizes_generation: false`, `opens_allowance: false`, `integrated: false`, and `network_calls: 0`. `consume` returns that same token with `consumed: true` only when every field still matches the copy the guard stored. A changed estimate, cash figure, overage object, or authorization flag refuses.

## Evidence used

- Subscription key names: the 34 names logged by the 17 Nov J2806 read and copied in `EAR_REVIEW_J3046`. `subscription_shape.json` records those names and types. It has no account values.
- Types for 31 of those keys: the 4 Oct redacted snapshot's structure, plus the public subscription schema for `cancels_immediately` (boolean). The healthy snapshot's `next_invoice` is a scheduled renewal object, not null, with a null payment status and an empty discount list.
- Three names were logged only as names: `bfcm_2026_offer`, `creator_arm_price`, `is_annual_four_months_subscriber`. A null, boolean, integer, or string is accepted and ignored. A nested object or list refuses. Their real types are an unresolved risk.
- Duration tariff, from `J2806_PROVENANCE.json`: measured 2,475 credits for one 180s `music_v2` take; published 900 credits/minute, so 2,700 for 180s; recorded worst case 2,970. The declaration floor is 2,970, the higher evidenced figure. 2,475 remains the measured reference and is not a price the caller may declare.
- Capacity mapping: on that same take the character meter moved 43,725 − 41,250 = 2,475, equal to the credits spent. The guard computes the ratio from those three numbers. It is 1 for this one take and this duration only. Any other ratio, or a broken equality, refuses `unknown_mapping`. A prompt length is not a music price.

## Checks, in order

1. `fetched_at`, `now`, `lease`, `pause_file_present`, and `pending_unposted_credits` are refused. They are not evidence.
2. The in-memory board accepts one `decide`. The durable record is `hos009-score-single-use.json`, flocked, keyed by the request-body hash and the raw subscription hash. A new `MeterBoard`, including in a new process, refuses when given the same file.
3. HTTP status must be the integer 200.
4. `date_header` must be the response Date header. `now` is the guard's own clock. A negative gap is `inconsistent_clock`. A gap above 60 seconds is `stale`.
5. The body must be raw bytes. Duplicate keys and bare `NaN` or `Infinity` refuse.
6. The key set must be the 34 names in `subscription_shape.json`. One added key is `unknown_field`. A missing `current_overage` is `overage` even when `currency` is missing too. Flattened overage keys are `overage`.
7. Entitlement must be tier `creator`, status `active`, and both periods `monthly_period`. `cancels_immediately` must be false.
8. Both extension limits must be integer 0 and both extension flags false.
9. Open invoices must be empty and `has_open_invoices` false. `pending_change` must be null. `next_invoice` may be null or the nine-field renewal object from the redacted snapshot: non-negative cent fields, a payment time after the Date header, null payment status, and no discounts. A processing payment refuses.
10. Nested `current_overage` keeps the reviewed canonical-zero rule.
11. The request must be holder `hos009-score`, attempt 1, `/v1/music`, `music_v2`, instrumental, exactly 180000 ms. Estimated credits must be an integer from 2,970 to 3,000. One credit refuses. Cash must be the string `0`.
12. Remaining meter units must cover `estimated_credits` times the evidenced ratio.
13. `TTS_PAUSE` must be absent on disk. A caller flag does not override the file.
14. `ledger.jsonl` must exist. A line without an integer status, or a line timestamped after the Date header, is `pending_spend`. A missing file is unknown, not zero.
15. `elevenlabs.lock` must be flocked by this process, in the live recorder's four-field shape, with `started` at or before the Date header and inside the 60-second window. A dict lease is refused.

The token stores the raw-body hash, the request hash, the Date-derived fetch time, the guard clock, the tariff figures, and the entitlement fields that were checked.

## Proposed integration

Do not wire this in on the strength of this proposal. This commit does not change `el_client.py`, `el_guard.py`, or `generate_music_bed.py`.

`el_client.request` still calls `el_guard.before_spend`, and that call still performs its own GET `/v1/user/subscription`. A future diff, only after an independent pass and a separate Chief scope, would have to do all of the following:

1. Leave `el_guard.py` at least as strict as it is now.
2. Take the live one-recorder lock first, then pass that `elevenlabs.lock` path. Do not pass a lease dict.
3. Perform one GET. Keep the raw bytes and the Date header from that response. Pass those in. Do not pass a caller clock.
4. Read `TTS_PAUSE` and `ledger.jsonl` from the desk. Do not pass booleans or a pending total.
5. Pin the single-use file to one directory for `hos009-score`. A caller-chosen directory is not a pin.
6. On `pass_once`, `consume` the unmodified token, then one POST. `el_guard.before_spend` must take the already-fetched raw response and does not issue a second GET. A POST without a consumed receipt refuses.
7. On any refusal, stop. No second GET and no second POST.

Until that diff exists, `generate_music_bed.py --generate` remains a bypass. This commit does not itself block a manual run, and it does not open one.

## Unresolved risks

- The three promo keys can still refuse a real body if the live value is an object. No account call was made to learn the type.
- The single-use directory is an argument so the synthetic tests do not touch the live desk. A new empty directory would admit another flight. Integration has to pin the directory first.
- The lock check reads a file and flocks it. It does not call `acquire_lock`, because a synthetic test must not take the studio recorder lock. A process that writes its own pid into a file of the right name satisfies the check.
- The Date header is trusted only because this module cannot see the socket. A separate `fetched_at` is refused, which stops the old requirement that the caller copy one timestamp onto another. It does not detect a header the caller invented.
- The meter ratio is one measured take. A later price change is not covered.
- Server time after the local lock time refuses. There is no skew allowance.
- `el_client.request` still double-GETs. Nothing in this commit closes that path.

## Holds this commit leaves in place

- J3047 closure of the unused J3043/J3045 allowance.
- J2808 rejection of score v01 and v02.
- J2035 and J2171 blocked.
- No public schedule change and no new ready-by promise.

## Review

```bash
python3 -m unittest discover -s jobs/reviews/J3141 -p 'test_*.py' -v
```

`HASHES.txt` pins `score_billing_guard.py`. The review commit is the pin for the whole proposal.
