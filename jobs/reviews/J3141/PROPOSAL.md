# J3147 — repaired fail-closed score billing guard (proposal only)

19 November 2026. This repairs the offline proposal at `c0c1848f89d99bcc656d1aa862428b605bd678c9`. J3145 (HOS PR 668, `8ee5ae73b2fce1300ea009422577f8e877b7d36c`) recorded FIX. J3146 confirmed that FIX and left findings A–D unresolved. This commit answers those four findings. It does not authorize a score.

No account call, no POST, no generation, no billing change, and no edit to the live ElevenLabs tools were made while writing it. Tests use synthetic fixtures and the existing redacted key names only. The live desk is refused, and no live single-use file is cleared.

## What a pass means

`MeterBoard.decide` returns `outcome: pass_once` only when every check below passes. The returned token always has `authorizes_generation: false`, `opens_allowance: false`, `integrated: false`, `network_calls: 0`, and `tariff_current_guarantee: false`. `consume` returns that same token with `consumed: true` only when every field still matches the copy the guard stored, the sealed response is still fresh, and the recorder lock, pause file and ledger still pass. A changed estimate, cash figure, overage object, or authorization flag refuses.

A stale Date burns `elevenlabs/hos009-score-single-use.json`. That burn is fail-closed. Clearing the file takes an explicit Chief ruling. This module does not delete it.

## Evidence used

- Subscription key names: the 34 names logged by the 17 Nov J2806 read and copied in `EAR_REVIEW_J3046`. `subscription_shape.json` records those names and types. It has no account values. Its hash is unchanged from `c0c1848f`.
- Types for 31 of those keys: the 4 Oct redacted snapshot's structure, plus the public subscription schema for `cancels_immediately` (boolean). The healthy snapshot's `next_invoice` is a scheduled renewal object, not null, with a null payment status and an empty discount list.
- Three names were logged only as names: `bfcm_2026_offer`, `creator_arm_price`, `is_annual_four_months_subscriber`. A null, boolean, integer, or string is accepted and ignored. A nested object or list refuses. Their real types are an unresolved risk.
- Duration tariff, from the historical `J2806` take: measured 2,475 credits for one 180s `music_v2` take; published 900 credits/minute, so 2,700 for 180s; recorded worst case 2,970. The declaration floor is 2,970, the higher evidenced figure. 2,475 remains the measured reference and is not a price the caller may declare.
- That take is not a current tariff guarantee. `TARIFF_CURRENT_GUARANTEE` is false. A later price change is not covered, and the token says so.
- Capacity mapping: on that same historical take the character meter moved 43,725 − 41,250 = 2,475, equal to the credits spent. The guard computes the ratio from those three numbers. It is 1 for this one take and this duration only. Any other ratio, or a broken equality, refuses `unknown_mapping`. A prompt length is not a music price. The ratio is not evidence that the next request will move the meter by the same amount.

## Findings A–D

A. The four paths are derived from one desk root: `locks/elevenlabs.lock`, `elevenlabs/TTS_PAUSE`, `elevenlabs/ledger.jsonl`, and `elevenlabs/hos009-score-single-use.json`. `decide` does not take `store_path`, `lock_path`, `pause_path`, or `ledger_path`. Those names stay on `CALLER_ASSERTED` and still refuse as `caller_asserted_state`. The older clock, lease, and state names are unchanged. `bind_desk` is the fixture seam. It is not a `decide` argument, and it refuses the live desk.

B. The recorder lock is the live shape: `O_CREAT | O_EXCL`, the four keys `pid`, `host`, `script`, `started`, descriptor kept open. The descriptor is read-write so the check can re-read those bytes without opening a second file. `hold_recorder` does that. `decide` and `consume` only observe it. They do not flock, close, or unlink it. A file that merely contains this pid, or an advisory lock this process also holds, is not ownership. `consume` checks the same descriptor and the same `started` value again, after the decision and before a mocked POST. A second live process cannot create the file. A dead same-host holder can be replaced only inside `hold_recorder`, once, the way the live recorder does. The check never unlinks. The single-use file has its own advisory lock around the read-modify-write. That lock is not the recorder lock.

C. Status, Date and raw bytes are sealed together by `read_subscription`, which calls the transport once. `TransportReceipt` cannot be constructed by the caller. A frozen stand-in, a loose `date_header`, or a body swapped after the seal refuses as `untrusted_receipt`. `consume` checks the seal again.

D. Each ledger line is parsed with `loads_strict`. A line timestamped at or after the Date refuses, including the same second. A status other than integer 200 refuses unless that line itself carries `reconciled: true` and a non-empty `reconciliation` note. The note is not a `decide` argument. Reconciliation does not waive a same-second or later timestamp.

## Checks, in order

1. `fetched_at`, `now`, `lease`, `acquired_at`, `pause_file_present`, `pending_unposted_credits`, `observed_character_count`, and the four path names are refused. They are not evidence.
2. The receipt must be one this process sealed. A dataclass with the same fields is not a receipt.
3. The in-memory board accepts one `decide`. The durable record is the pinned single-use file. A new `MeterBoard`, including after a restart, refuses when that file already holds a flight. A second directory passed into `decide` refuses before it can be used.
4. HTTP status must be the integer 200 on that same receipt.
5. The Date on that receipt must parse. `now` is the guard's own clock. A negative gap is `inconsistent_clock`. A gap above 60 seconds is `stale`, and the single-use file stays burned.
6. The body must be the raw bytes on that receipt. Duplicate keys and bare `NaN` or `Infinity` refuse.
7. The key set must be the 34 names in `subscription_shape.json`. One added key is `unknown_field`. A missing `current_overage` is `overage` even when `currency` is missing too. Flattened overage keys are `overage`.
8. Entitlement must be tier `creator`, status `active`, and both periods `monthly_period`. `cancels_immediately` must be false.
9. Both extension limits must be integer 0 and both extension flags false.
10. Open invoices must be empty and `has_open_invoices` false. `pending_change` must be null. `next_invoice` may be null or the nine-field renewal object from the redacted snapshot: non-negative cent fields, a payment time after the Date header, null payment status, and no discounts. A processing payment refuses.
11. Nested `current_overage` keeps the reviewed canonical-zero rule.
12. The request must be holder `hos009-score`, attempt 1, `/v1/music`, `music_v2`, instrumental, exactly 180000 ms. Estimated credits must be an integer from 2,970 to 3,000. One credit refuses. Cash must be the string `0`.
13. Remaining meter units must cover `estimated_credits` times the evidenced ratio. The ratio is historical.
14. `TTS_PAUSE` must be absent. A caller flag does not override the file. `consume` reads the file again.
15. `ledger.jsonl` must exist. The rules in finding D apply. A missing file is unknown, not zero. `consume` reads it again.
16. The open recorder descriptor must still be this process, with `started` at or before the Date and inside the 60-second window. `consume` checks it again. A dict lease is refused.

## Proposed integration

Do not wire this in on the strength of this proposal. This commit does not change `el_client.py`, `el_guard.py`, or `generate_music_bed.py`.

`el_client.request` still calls `el_guard.before_spend`, and that call still performs its own GET `/v1/user/subscription`. `generate_music_bed.py --generate` still reaches that POST without this guard. `INTEGRATION_DIFF.md` is the offline design that would close the double GET and that bypass. It is not applied. The adapter `proposed_flight` is the offline stand-in: one mocked GET, then `decide`, then `consume`, then at most one mocked POST, and no second GET when the board has already decided. On any refusal it does not issue a second GET and it does not post.

Until that diff is applied, `generate_music_bed.py --generate` remains a bypass. This commit does not itself block a manual run, and it does not open one.

## Unresolved risks

- The three promo keys can still refuse a real body if the live value is an object. No account call was made to learn the type.
- The meter ratio and the 2,970 floor come from one historical take. They are not a guarantee of the next charge.
- Server time after the local lock time refuses. There is no skew allowance.
- The receipt seal stops a caller of `decide` from pairing a fresh Date with a different body. It does not make a mocked transport a live socket. No live response was fetched.
- `bind_desk` can aim a fixture at a temporary root. The production entry point cannot. Integration still has to bind the real desk once, in a later scope.
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

`HASHES.txt` pins this proposal. The review commit is the pin for the whole proposal.
