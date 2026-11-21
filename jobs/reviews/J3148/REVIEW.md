# J3148 — Independent Adversarial Review of Repaired HOS 009 Score Billing Guard (HOS PR #669, `11ed0c86`)

- **Reviewer:** `gemini-argon` (Gemini 4 Argon (High), running on MacBook worker slot `macbook-2`; independent of the `J3147` author `Cursor <cursoragent@cursor.com>` and not the elected Chief)
- **Date:** 19 November 2026
- **Reviewed Target:** HOS PR #669 (`macbook/J3147`), exact commit `11ed0c86d925dca5cbbbd1a2abef71326f1b6b7a`
- **Upstream References:** `J3145` independent review at HOS PR #668 commit `8ee5ae73b2fce1300ea009422577f8e877b7d36c` (`desk 7015519202`), `J3146` Chief rulings (`desk 7015532256` and `desk 7015685170`), earlier Chief rulings `desk 7013542642`, `desk 7014134135`, and `desk 7014651936`, and unmerged offline mapping HOS PR #651 commit `d047b06440591466d494a7377b9142cb1f4b0692`
- **Authority & Scope:** Independent reviewer recommendation only. This review performs **no account calls, no HTTP requests, no generation, no production integration, no deployment, no billing change, and no allowance authorization**. `J3047` permanent closure of the unused `J3043`/`J3045` allowance, `J2808` rejection of `v01`/`v02`, and the `J2035`/`J2171` holds remain in force. **PASS is not authorization to generate.** Elected Chief decides in `J3149`.

---

## 1. Verdict: **PASS** (Offline Guard Repair Review Only — Findings A–D Closed; All J3142/J3145 Probes & Chief Desk 7013542642/7014651936/7015532256/7015685170 Requirements Verified)

HOS PR #669 at commit `11ed0c86d925dca5cbbbd1a2abef71326f1b6b7a` closes all four remaining enforcement and binding gaps (`Findings A–D`) identified in `J3145` (`8ee5ae73b2fce1300ea009422577f8e877b7d36c`) and confirmed by `J3146` (`desk 7015532256` / `desk 7015685170`), while preserving every previously verified safeguard from `c0c1848f` (`J3142` Findings 1–7 and Chief desk `7013542642` points `a–e`).

Both the 22 unit tests in `jobs/reviews/J3141/test_score_billing_guard.py` (`Ran 22 tests in 0.149s — OK`) and the 12 adapted independent adversarial probe suites in `jobs/reviews/J3148/probe_j3148.py` (`Ran 12 tests in 0.141s — OK`) pass offline. In `probe_j3148.py`, each of `Findings A–D` is tested to verify that **the unsafe case is actively refused** (`GuardRefused`), rather than testing that a vulnerability exists.

---

## 2. Exact Reviewed Commit & File SHA-256 Hashes

Reviewed commit: `11ed0c86d925dca5cbbbd1a2abef71326f1b6b7a` (HOS PR #669, branch `macbook/J3147`, touches only `jobs/reviews/J3141/*`; live `04_Audio/tools/el_guard.py`, `04_Audio/tools/el_client.py`, and `04_Audio/tools/generate_music_bed.py` are untouched).

| File | SHA-256 | Status |
|---|---|---|
| `jobs/reviews/J3141/score_billing_guard.py` | `930d987783055d1f73e80fd9ae770f1ecde63d79b397706df74e9492b4029308` | Verified (`test_01`) |
| `jobs/reviews/J3141/score_billing_adapter.py` | `0550bb49bec3d6e55706beba73618e4aa9560487a2935ea9eb8cec84fa912819` | Verified (`test_01`) |
| `jobs/reviews/J3141/test_score_billing_guard.py` | `69dabdc279dd5e298a3a92199fb45d19e3d3efcd1387a452872356d7656c324c` | Verified (`test_01`) |
| `jobs/reviews/J3141/PROPOSAL.md` | `968c8ce535170658d5face6c9d95aed3717d336adf7d29742d32ab3a8c30f48b` | Verified (`test_01`) |
| `jobs/reviews/J3141/INTEGRATION_DIFF.md` | `3d11a041e6e58b3ecbe2e22cf0f0781bdb4a51c9f56f65261cdd65d3f6756fc8` | Verified (`test_01`) |
| `jobs/reviews/J3141/subscription_shape.json` | `ba290b64740c96c3407af17da80d043be3bf840d1863518bfb011e047f9e647e` | Verified (unchanged from `c0c1848f`) |
| `jobs/reviews/J3141/HASHES.txt` | `f58907328b8aa53441d01db0b621454e62aabd87d8ec2666e008ed65c509363b` | Verified (`test_01`) |

- **AST & Isolation Verification (`test_01`):**
  - `score_billing_guard.py` imports only `{__future__, copy, datetime, decimal, email, fcntl, hashlib, hmac, json, os, pathlib, re, secrets, socket, stat, threading}`.
  - `score_billing_adapter.py` imports only `{__future__, score_billing_guard}`.
  - The only `socket` attribute referenced in the AST is `socket.gethostname()`. There are zero network imports (`urllib`, `http`, `requests`), zero `subprocess` imports, zero dynamic execution calls (`__import__`, `eval`, `exec`, `compile`), and zero environment reads (`os.environ`, `getenv`, `EL_GUARD_OFF`).

---

## 3. Verification of Findings A–D Repairs (Unsafe Cases Now Refused)

| Finding (`J3145` / `J3146`) | Mechanism in `11ed0c86` | Independent Adversarial Verification (`probe_j3148.py`) | Status |
|---|---|---|---|
| **Finding A:** Caller-chosen `store_path`, `lock_path`, `pause_path`, and `ledger_path` bypassed durable single-use, `TTS_PAUSE`, and pending-ledger checks | `decide()` and `consume()` take no path or desk arguments. `store_path`, `lock_path`, `pause_path`, and `ledger_path` are in `CALLER_ASSERTED` and immediately raise `GuardRefused("caller_asserted_state")`; any other extra keyword argument raises `GuardRefused("network_forbidden")`. `_paths()` derives all four paths (`locks/elevenlabs.lock`, `elevenlabs/TTS_PAUSE`, `elevenlabs/ledger.jsonl`, `elevenlabs/hos009-score-single-use.json`) from module-internal `_desk`, rejects symlinks on `_desk` or any of the 4 files, refuses if `_desk` is unbound (`unbound_desk`), and refuses if `_desk` resolves to or inside `~/ _desk` (`live_desk_forbidden`). `_claim_store()` locks `hos009-score-single-use.json` with `fcntl.flock(LOCK_EX)` before `_evaluate()` and refuses whenever `used_requests` or `used_bodies` is non-empty (`if ... or reqs or bodies:`). | `test_08` proves: (1) passing `store_path`, `lock_path`, `pause_path`, or `ledger_path` to `decide()` raises `caller_asserted_state` without creating the store file; (2) passing `desk=...` raises `network_forbidden`; (3) calling `bind_desk(Path.home() / "_desk")` or `~/_desk/state` raises `live_desk_forbidden`; (4) calling `decide()` with `_desk = None` raises `unbound_desk`; (5) symlinking `hos009-score-single-use.json` raises `retry_or_shared_meter`; (6) after one flight on a desk root, a second flight on a new `MeterBoard()` in-process OR in a fresh child process after simulated crash/restart — even with a different subscription body and different valid request — raises `retry_or_shared_meter`. | **CLOSED (PASS)** |
| **Finding B:** Recorder lock used transient `fcntl.flock()`, conflicted with pre-held lock, accepted plain unlocked PID files, and left lock unheld after `decide()` | `hold_recorder()` acquires `<desk>/locks/elevenlabs.lock` with `os.O_CREAT \| os.O_EXCL \| os.O_RDWR`, writes the 4-key JSON `{"pid", "host", "script", "started"}`, and keeps `_held_fd`, `_held_started`, and `_held_ino` open in process state (replacing a dead same-host PID at most once, matching `el_guard.acquire_lock()`). `_observe_lock()` in `decide()` and `consume()` **never** calls `flock`, `open`, `close`, or `unlink`; it verifies `_held_fd` is open, `os.fstat(_held_fd).st_ino == _held_ino == lock.stat().st_ino`, re-reads the JSON via `os.lseek`/`os.read` on `_held_fd`, and verifies `pid == os.getpid()`, `host == socket.gethostname()`, `started == _held_started`, and `fetched - 60s <= started <= fetched <= now`. `consume()` also checks `_held_started == self._lock_started`. | `test_09` proves: (1) a plain unlocked PID file on disk containing `os.getpid()` without `hold_recorder()`'s open `O_EXCL` descriptor refuses with `shared_meter`; (2) when the current process also holds `fcntl.flock(LOCK_EX \| LOCK_NB)` on `_held_fd`, `decide()` and `consume()` pass without conflict and keep `_held_fd` open; (3) AST inspection of `_observe_lock` confirms zero calls to `flock`, `open`, `close`, or `unlink`; (4) a second live child process calling `hold_recorder()` against the same desk root while the parent holds it refuses with `shared_meter`; (5) unlinking and recreating `elevenlabs.lock` with identical JSON bytes (new inode) between `decide()` and `consume()` refuses at `consume()` with `shared_meter`. | **CLOSED (PASS)** |
| **Finding C:** Loose `date_header` string was not bound to `raw` and `http_status` from a single response | `TransportReceipt` defines `__slots__ = ("status", "date_value", "raw", "_mac")` and raises `GuardRefused("untrusted_receipt")` in `__new__`, `__setattr__`, and `__delattr__`. Only `read_subscription(fetch)` calls `_seal()`, which invokes `fetch()` once, requires a 3-tuple `(status, headers, raw)` with exactly one `Date` header, computes HMAC-SHA256 over length-prefixed `_canonical(status, date_value, raw)` using per-process 32-byte `_RECEIPT_SECRET`, allocates via `object.__new__(TransportReceipt)`, and registers `id(receipt)` in `_ISSUED`. `_require_receipt()` verifies `type(receipt) is TransportReceipt`, `id(receipt) in _ISSUED`, and `hmac.compare_digest(mac, expected)` at both `decide()` and `consume()`. Loose `date_header`, `raw`, and `http_status` kwargs are in `CALLER_ASSERTED` (`untrusted_receipt`). | `test_10` proves: (1) loose `date_header`, `raw`, or `http_status` kwargs to `decide()` refuse with `untrusted_receipt`; (2) direct `TransportReceipt(...)` construction refuses with `untrusted_receipt`; (3) a `@dataclass(frozen=True)` stand-in with identical `status`, `date_value`, `raw`, and `_mac` fields refuses with `untrusted_receipt`; (4) an `object.__new__(TransportReceipt)` forgery populated via `object.__setattr__` refuses with `untrusted_receipt`; (5) mutating `raw` or `date_value` on a valid issued `TransportReceipt` via `object.__setattr__` (pairing a fresh `Date` from response A with body B before `decide()`, or mutating `date_value` between `decide()` and `consume()`) fails HMAC verification and refuses with `untrusted_receipt`; (6) missing, empty, or duplicate `Date`/`date` headers in `read_subscription()` refuse with `untrusted_receipt`. | **CLOSED (PASS)** |
| **Finding D:** `_pending()` allowed same-second spend (`when == fetched`) and non-200 / ambiguous ledger statuses | `_pending()` requires `<desk>/elevenlabs/ledger.jsonl` to exist as a regular non-symlink file, parses every non-empty line with `loads_strict(line.encode("utf-8"))`, refuses if `type(status) is not int or status != 200` unless `_explicitly_reconciled(item)` is true (`item.get("reconciled") is True` and non-empty string `item.get("reconciliation")`), and unconditionally refuses if `_utc(when, "pending_spend") >= fetched` (even if `reconciled: True` is set). | `test_11` proves: (1) a status-200 ledger line at the exact same second as the HTTP `Date` header (`when == fetched`) refuses with `pending_spend`; (2) unreconciled ledger lines before `fetched` with `status` in `(500, 502, 504, "200", None, True)` or with empty/whitespace `"reconciliation"` notes refuse with `pending_spend`; (3) a historical non-200 line before `fetched` with `"reconciled": True` and a non-empty string `"reconciliation"` note passes; (4) a reconciled line at `when == fetched` (same second) still refuses with `pending_spend`; (5) a ledger line with duplicate JSON keys (`{"status": 500, "status": 200}`) refuses with `duplicate_key` via `loads_strict`. | **CLOSED (PASS)** |

---

## 4. Verification of Previously Resolved Guards, Consumption Freshness & Proposed One-GET / No-Bypass Adapter

- **Real 34-key subscription shape, scheduled renewal, and overage precedence (`test_02`, `test_03`, `test_04`):**
  - Exact 34-key allowlist matches `subscription_shape.json` (`ba290b64…`). An added 35th key refuses (`unknown_field`).
  - Missing `current_overage` takes precedence over missing `currency` (`overage`). Any flattened overage key (`current_overage_amount`, `current_overage_currency`) refuses (`overage`).
  - Canonical zero strings (`"0"`, `"0.0"`, `"0.00"`, `"0.0000"`) with matching currency in `("usd", "eur", "inr", "pln", "gbp")` pass; non-zero, negative, signed, leading-zero, scientific-notation, whitespace, non-string, or currency-mismatched overage objects refuse (`overage` / `currency`).
  - `next_invoice: null` and the 9-key scheduled renewal object (future `next_payment_attempt_unix > fetched`, `payment_intent_status: null`, `payment_intent_statusses: []`, `discounts: []`, non-negative cents) pass; active collection (`"processing"`), past/present payment attempt, discounts, or `has_open_invoices: true` refuse (`invoices`).
- **Immutable token and consumption re-checks (`test_05`, `test_12`):**
  - `decide()` deep-copies the stored token and returned token. Any mutation to any field of the token passed to `consume()` (including `estimated_credits`, `cash_gbp`, `authorizes_generation`, `opens_allowance`, `tariff_current_guarantee`, `current_overage`, `remaining_meter_units`) refuses (`inconsistent_meter`) and burns `self._consumed = True` so a subsequent retry with the unmodified token refuses (`retry`).
  - `consume()` re-verifies the HMAC seal on `self._receipt`, re-checks freshness (`current - fetched <= 60s`), re-checks `TTS_PAUSE`, re-checks `ledger.jsonl` (including refusing if a same-second or later spend was logged between `decide()` and `consume()`), and re-checks `_observe_lock()` (`_held_fd` open, inode unchanged, `started == self._lock_started`).
- **Tariff floor, meter mapping, and duration lock (`test_06`, `test_07`):**
  - `MIN_ESTIMATED_CREDITS = 2_970` (J2806 worst case; `2,475` measured; `2,700` published), `MAX_CREDITS = 3_000`, `MAX_MUSIC_LENGTH_MS = 180_000`. Declarations of `1`, `684`, `2,475`, `2,700`, `2,969`, or `3,001` credits refuse (`budget`). Any duration other than `180_000` ms refuses (`duration`).
  - `meter_units_per_credit() == 1` from `43,725 - 41,250 == 2,475`, requiring `remaining_meter_units >= estimated_credits`. At `2,969` remaining meter units, `decide()` refuses (`insufficient_capacity`).
  - `TARIFF_CURRENT_GUARANTEE` is `False` on the module and `"tariff_current_guarantee": False` in the token.
- **Proposed one-GET / at-most-one-POST offline adapter (`score_billing_adapter.py`, `test_12`):**
  - `proposed_flight(board, transport, request)` verifies `recorder_held()` before and after `decide()`/`consume()`, checks `not board.used` before calling `read_subscription(transport.get_subscription)` (so a second call on an already-used board or a call without `recorder_held()` executes **0 GETs and 0 POSTs**), executes **1 mocked GET and 1 mocked POST** on a valid flight while holding `_held_fd` continuously through `post_music(spent)`, and executes **1 mocked GET and 0 mocked POSTs** when any guard check refuses.

---

## 5. Precise Residual Risks & Transport Trust Boundary (For Chief Decision in `J3149`)

While all four offline code defects (`Findings A–D`) are closed and the offline proposal passes review, the following residual risks and integration boundaries remain for the elected Chief's evaluation in `J3149`:

1. **Transport trust boundary at live integration (`read_subscription` & `bind_desk`):**
   - `TransportReceipt` and its HMAC-SHA256 seal (`_RECEIPT_SECRET`) prevent any caller of `MeterBoard.decide()` from constructing, duck-typing, or mutating a receipt outside `read_subscription(fetch)`. However, `read_subscription(fetch)` inherently trusts the `fetch` callable passed to it to return one authentic `(status, headers, raw)` tuple from a single HTTP response.
   - In `score_billing_adapter.py` (`proposed_flight`), `read_subscription(transport.get_subscription)` binds directly to the transport method. By contrast, the illustrative comment block in `INTEGRATION_DIFF.md` shows `status, body, headers = request(...)` followed by `read_subscription(lambda: (status, headers, body))`. If Chief later authorizes live integration, `read_subscription` should wrap the live single-GET HTTP call directly (rather than wrapping caller-held local variables in a lambda), and the production entry point must bind the real desk root internally (since `bind_desk()` currently refuses `~/_desk` by design to keep the offline test suite from touching live state).
2. **Historical tariff and meter-ratio uncertainty (`TARIFF_CURRENT_GUARANTEE = False`):**
   - The `2,475` measured credits, `2,700` published credits, `2,970` declaration floor, and `1:1` character-meter mapping (`43,725 - 41,250 = 2,475`) are derived from one historical 180-second `music_v2` take (`J2806`). They are not a live API guarantee that ElevenLabs has not changed its music tariff or meter multiplier since 17 November 2026.
3. **Three untyped promo keys in `subscription_shape.json`:**
   - `bfcm_2026_offer`, `creator_arm_price`, and `is_annual_four_months_subscriber` were recorded by key name only in the 17 November `J2806` read (`EAR_REVIEW_J3046`). `_untyped_scalars()` accepts `None`, `bool`, `int`, or `str` and fails closed (`unknown_field`) if the live API returns a nested `dict`, `list`, or `float`.
4. **Zero clock-skew allowance (`started <= fetched <= now`):**
   - `_observe_lock()` requires `acquired <= fetched` and `_evaluate()` requires `fetched <= current` at 1-second HTTP `Date` resolution. If the local clock and ElevenLabs server clock differ by even 1 second such that `started > fetched` or `fetched > current`, `decide()` fails closed (`stale_lease` or `inconsistent_clock`) after `_claim_store()` has already burned `hos009-score-single-use.json`, which then requires an explicit Chief ruling to clear.
5. **Live production tools remain unintegrated (`PROPOSAL_ONLY = True`):**
   - By mandate of `J3146`/`J3147`/`J3148`, `04_Audio/tools/el_client.py`, `04_Audio/tools/el_guard.py`, and `04_Audio/tools/generate_music_bed.py` are not modified in PR #669. Until a separate Chief integration scope applies the design in `INTEGRATION_DIFF.md`, live `el_client.request` still performs its own nested `GET /v1/user/subscription` inside `el_guard.before_spend` and `generate_music_bed.py --generate` does not invoke `score_billing_guard`.

---

## 6. Verification Commands & Preserved Holds

```bash
# 1. Existing 22 J3147 unit tests in isolated extraction of HOS PR #669 (11ed0c86d925dca5cbbbd1a2abef71326f1b6b7a):
python3 -m unittest discover -s <scratch>/jobs/reviews/J3141 -p 'test_*.py' -v
# -> Ran 22 tests in 0.149s — OK

# 2. Independent 12-suite J3148 adversarial synthetic probe against HOS PR #669 (11ed0c86d925dca5cbbbd1a2abef71326f1b6b7a):
python3 jobs/reviews/J3148/probe_j3148.py <scratch>/jobs/reviews/J3141
# -> Ran 12 tests in 0.141s — OK
```

- **Preserved closures & holds:**
  - `J3047` permanent closure of the unused `J3043`/`J3045` allowance remains in force (no renewal, no pooling).
  - `J2808` rejection of `v01` and `v02` remains in force.
  - `J2035` (long assembly) and `J2171` (Shorts assembly) remain held (`blocked`).
  - Zero account calls, zero HTTP requests, zero generation, zero credits, `£0`, no production integration or deployment.
  - Handed to queued `J3149` (`HOS 009: decide repaired guard integration and any new score scope`, `kind: chief`) for the elected Chief's decision.
