# Offline integration design — not applied

19 November 2026. J3147. This file is a design note for a later Chief scope. It is not a patch. Do not apply it. `04_Audio/tools/el_client.py`, `04_Audio/tools/el_guard.py` and `04_Audio/tools/generate_music_bed.py` are unchanged.

The guard in this directory stays offline. Nothing here authorizes a score, a GET, a POST, or a credit spend.

## What is open today

`el_client.request` treats a music POST as a spend and calls `el_guard.before_spend` with a nested subscription GET:

```python
el_guard.before_spend(
    path,
    data,
    lambda: request("GET", "/v1/user/subscription", token, mode)[:2],
)
```

That GET returns only `(status, body)`. The Date header is discarded. `before_spend` can then call `fetch_subscription()` itself, which is a second read of the same route when the caller had already read it. `multipart_post` repeats the same nested GET.

`generate_music_bed.py --generate` calls `compose`, which calls `request("POST", "/v1/music", ...)`. That path never consults this proposal. A dry run does not spend. A real `--generate` would. That is the bypass.

## What a later diff has to do

One flight, after this proposal has passed an independent review and a separate Chief scope:

1. Take the live recorder lock with the existing `O_EXCL` owner, and keep that descriptor until the process exits. Do not flock it inside the guard check, and do not pass a lease dict.
2. Perform one `GET /v1/user/subscription`. Keep the status, the Date header and the raw body from that single response object. Seal them with `read_subscription`. Do not pass a caller clock, and do not pass the three fields as separate arguments.
3. Bind the desk root once, inside the process, to the real desk. Read `locks/elevenlabs.lock`, `elevenlabs/TTS_PAUSE`, `elevenlabs/ledger.jsonl` and `elevenlabs/hos009-score-single-use.json` from that root. Do not accept those paths as `decide` arguments.
4. On `pass_once`, `consume` the unmodified token. `consume` checks the seal, the Date, the lock, the pause file and the ledger again.
5. Only then, one `POST /v1/music`. `el_guard.before_spend` must accept the already-fetched response and must not issue a second GET. A POST without a consumed receipt refuses.
6. On any refusal, stop. No second GET and no POST.
7. `generate_music_bed.py --generate` must refuse unless that consumed receipt matches the request it is about to send. The dry run stays a dry run. There is still no retry.

`el_guard.py` stays at least as strict as it is now. This design does not turn `EL_GUARD_OFF` on, does not raise the credit floor's allowance, and does not renew or pool the closed J3043/J3045 allowance.

## Sketch, not a patch

```
# el_client.request, spend branch, later scope only
# fetch once, keep status, headers and body
# do not call request("GET", "/v1/user/subscription") a second time from before_spend
status, body, headers = request("GET", "/v1/user/subscription", token, mode)
receipt = read_subscription(lambda: (status, headers, body))  # seals this tuple; fetch already done
token = board.decide(receipt, request=music_request)
spent = board.consume(token, body_sha256=token["body_sha256"])
# POST /v1/music once, using `spent`
# before_spend(path, data, fetch) is not given a new GET
```

The lambda above is only valid if `request` was already called once and the lambda does not call it again. A later implementation has to pass the tuple through without a second round trip. The sketch is here so the double GET is visible. It is not wired in.

`generate_music_bed.compose` would stop calling `request` directly. It would call the same flight. Until that change is applied, `--generate` remains a bypass. This commit does not block a manual run, and it does not open one.
