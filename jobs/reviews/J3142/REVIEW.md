# J3142 — Independent Adversarial Review of HOS 009 Proposed Score Billing Guard (HOS PR #667, `c9ef1e0a`)

- **Reviewer:** `gemini` (`gemini-argon`, specialist worker on the Mac mini; not the implementer `cursor` of `J3141` and not the elected Chief)
- **Date:** 19 November 2026
- **Reviewed Target:** HOS PR #667 (`cursor/J3141-score-guard`), exact commit `c9ef1e0aa51a363971f5de1f5648ece6826eec12`
- **Upstream References:** `J3139` (`desk 7013186649`), `J3141` (`desk 7013482621`), Chief field comparison `desk 7005927729`, `J3059` (`desk 6984412310`), and unmerged offline mapping HOS PR #651 commit `d047b06440591466d494a7377b9142cb1f4b0692`
- **Authority & Scope:** Independent reviewer recommendation only. This review performs **no account calls, no HTTP requests, no generation, no production integration, no deployment, no billing change, and no allowance authorization**. `J3047` closure of the unused `J3043`/`J3045` allowance, `J2808` rejection of `v01`/`v02`, and the `J2035`/`J2171` holds remain intact. Elected Chief decides in `J3143`.

---

## 1. Verdict: **FIX** (2 Production Self-Lock Blockers, 3 High-Severity Enforcement/Tampering Gaps, 2 Medium/Low Hardening Items)

The proposed module (`jobs/reviews/J3141/score_billing_guard.py`, SHA-256 `d6a87058662335da0285f1c609cdfbe3285554236fceda6aa8d2aed36b9b3be5`) is offline, stdlib-only, free of network/environment imports, unimported by production tools, and correctly implements the nested `current_overage.amount` / `current_overage.currency` validation from `d047b06440591466d494a7377b9142cb1f4b0692`. All 17 of `J3141`'s synthetic unit tests pass.

However, independent adversarial review and synthetic testing (`jobs/reviews/J3142/probe_j3142.py`, 13 test suites / >110 synthetic probes) establish that **the guard as written at `c9ef1e0aa51a363971f5de1f5648ece6826eec12` cannot be used for production integration without correction**:

1. **It would refuse 100% of real healthy `GET /v1/user/subscription` responses on the studio's active Creator plan** for two independent reasons:
   - `_keys()` requires the raw JSON response to have *only* 16 top-level keys (`present == REQUIRED_KEYS`), refusing the actual 34-key `GET /v1/user/subscription` payload documented in `EAR_REVIEW_J3046.md` and Chief `desk 7005927729` with `GuardRefused("unknown_field")`, while `PROPOSAL.md` rightly forbids pre-filtering the raw bytes before `decide()`.
   - `_invoices()` requires `payload["next_invoice"] is None`, whereas on an active monthly Creator subscription (`tier == "creator"`, `status == "active"`, `billing_period == "monthly_period"`), `next_invoice` is a non-null scheduled renewal invoice object (verified against `_desk/006/elevenlabs_subscription_snapshot_20261004.json`), causing every real active monthly subscription read to fail with `GuardRefused("invoices")`.
2. **It has three high-severity enforcement and integration-boundary gaps**:
   - `MeterBoard.consume()` validates only 4 fields (`id`, `outcome`, `authorizes_generation`, `body_sha256`) and echoes `dict(token)` back, allowing a caller to mutate `estimated_credits`, `cash_gbp`, `would_allow_posts`, `retries`, `integrated`, `proposal_only`, `music_length_ms`, or `current_overage` between `decide()` and `consume()`.
   - `_request()` hardcodes `music_length_ms == 180_000` (180 s `music_v2`, ~2,475–2,970 credits) but permits `estimated_credits` as low as `1` (or prompt character length `~684` from `el_guard.characters_in`), allowing a pass when remaining subscription capacity is only `1` credit.
   - `MeterBoard` is ephemeral per-instance in memory only (instantiating a second `MeterBoard()` bypasses the one-request latch), omits `TTS_PAUSE` (`pause_file_present`) and `pending_unposted_credits` checks, and `PROPOSAL.md` §Integration path step 6 conflicts with `el_client.request("POST", "/v1/music", ...)`, which automatically fires a **second** unguarded `GET /v1/user/subscription` inside `el_guard.before_spend`.

---

## 2. Exact Commit & Artifact Hashes Verified

Checked in an isolated detached worktree at `c9ef1e0aa51a363971f5de1f5648ece6826eec12`:

| File | SHA-256 | Status |
|---|---|---|
| `jobs/reviews/J3141/score_billing_guard.py` | `d6a87058662335da0285f1c609cdfbe3285554236fceda6aa8d2aed36b9b3be5` | Matches `HASHES.txt` |
| `jobs/reviews/J3141/HASHES.txt` | `946251b1b9670617a28d5534021d24d03c3ac39282b94a3bc29b7db92f813e9b` | Verified |
| `jobs/reviews/J3141/PROPOSAL.md` | `e434dcdab05af8de9c3aa462e2a28bc3a44d8ede6978c15ae52f3e2c16a7c54c` | Verified |
| `jobs/reviews/J3141/test_score_billing_guard.py` | `5222b9a9157bf140164b36e4051e38bcd488d4e932eae8650becf8655ffc7f28` | 17/17 tests PASS (`0.003s`) |
| `jobs/reviews/J3142/probe_j3142.py` | Independent adversarial probe suite (this review) | 13/13 suites PASS (`0.006s`) |

---

## 3. Requirement-by-Requirement Audit Matrix

| Requirement (`J3142` Brief) | What Holds in `c9ef1e0a` | What Fails / Needs Correction | Verdict |
|---|---|---|---|
| **1. Nested `current_overage.amount` & `currency`** | Requires nested `current_overage` dict with exact keys `{"amount", "currency"}`. Retains exact canonical zero string (`"0"`, `"0.0"`, `"0.00"`, ...) and currency (`usd`, `eur`, `inr`, `pln`, `gbp`) on token. Requires top-level `currency == current_overage.currency`. Refuses flattened `current_overage_amount` / `current_overage_currency` alone or alongside valid nested `current_overage`. | None in `_overage()` itself. In `_keys()`, if `current_overage` is missing alongside another missing or extra key, `_keys()` misclassifies the refusal as `unknown_field` or `malformed_body` instead of `overage` (Finding 7a). | **PASS (with Finding 7a key-order tweak)** |
| **2. Missing / null / malformed / negative / non-zero values** | Refuses `None`, `0` (int), `0.0` (float), `True`/`False`, `""`, `"00"`, `"000.000"`, `"-0"`, `"-0.00"`, `"+0"`, `"0."`, `".0"`, `"0e0"`, `"0.01"`, `"-0.01"`, `"1"`, `"-1"`, `"NaN"`, `"Infinity"`, whitespace/newline/null-byte padded strings, non-ASCII digits (`"０"`, `"٠"`), `str` subclasses, non-bytes bodies, invalid UTF-8, UTF-8 BOM, and duplicate JSON keys at any nesting depth (`object_pairs_hook=_pairs`). | `loads_strict()` does not pass `parse_constant` to `json.loads()`, so bare JSON `NaN`/`Infinity` are parsed by `json.loads` rather than rejected at the JSON parser boundary (Finding 7b). | **PASS (with Finding 7b parser hook)** |
| **3. Freshness & clock consistency** | Requires timezone-aware UTC ` datetime` (not subclass) with `utcoffset() == timedelta(0)` for `fetched_at` and `now`. Refuses `now < fetched_at` (`inconsistent_clock`) and `now - fetched_at > 60s` (`stale`); exact `60s` passes. Requires `next_character_count_reset_unix > int(fetched_at.timestamp()) + 60`. | `_lease()` does not call `_utc(acquired_at)`, allowing non-UTC timezone offsets (`+01:00`) on `lease["acquired_at"]`, and requires `acquired_at == fetched_at` exact microsecond equality even though lock acquisition precedes the HTTP GET (Finding 6). | **FIX (Finding 6)** |
| **4. Concurrency / shared-meter races** | Thread-safe `threading.Lock()` in `MeterBoard` ensures concurrent threads racing on the same `MeterBoard` instance get at most 1 `pass_once` and `N-1` `retry_or_shared_meter` (verified with 8 threads). Checks `exclusive is True`, `peers == 0`, `hosts == ["hos009-score"]`, `observed_character_count == character_count`. | `MeterBoard` has no process-wide or persistent latch across instances. `observed_character_count` is built from the same body in `PROPOSAL.md` step 5 (a tautology). `TTS_PAUSE` (`pause_file_present`) and `pending_unposted_credits` are not checked (Findings 5 & 6). | **FIX (Findings 5 & 6)** |
| **5. Insufficient credits & capacity** | Checks `character_count >= 0`, `character_limit > 0`, `character_limit >= character_count`, and `remaining = character_limit - character_count >= estimated_credits` (3,000 remaining vs 3,000 estimated passes; 2,999 remaining refuses as `insufficient_capacity`). | Allows `estimated_credits = 1` (or prompt length `684`) for a hardcoded `180,000 ms` `music_v2` request, passing when only `1` credit remains on the subscription (Finding 4). | **FIX (Finding 4)** |
| **6. Entitlement, extensions & invoices** | Checks `tier == "creator"`, `status == "active"`, `billing_period == "monthly_period"`, both extension limits `== 0`, both extension flags `is False`, `has_open_invoices is False`, `open_invoices == []`, `pending_change is None`. | **Blockers 1 & 2:** `_keys()` refuses all 18 standard non-billing top-level keys in a real 34-key `GET /v1/user/subscription` response (`unknown_field`), and `_invoices()` requires `next_invoice is None`, refusing the non-null scheduled renewal `next_invoice` object always present on an active monthly Creator plan (`invoices`). | **FIX (Findings 1 & 2 — Blockers)** |
| **7. One-request / no-retry enforcement & £0 / 3,000-credit cap** | Enforces `attempt == 1`, `estimated_credits <= 3000`, `cash_gbp == "0"`, `music_length_ms == 180000`, `endpoint == "/v1/music"`, `model_id == "music_v2"`, `force_instrumental is True`, `query == "output_format=mp3_44100_128"`, `holder == "hos009-score"`. Refusal burns that `MeterBoard` instance. | `MeterBoard.consume()` does not verify full token equality and echoes caller-tampered fields (`estimated_credits`, `cash_gbp`, `would_allow_posts`, `retries`, `current_overage`, etc.) into the consumed receipt (Finding 3); instantiating a new `MeterBoard()` resets `_used` (Finding 5). | **FIX (Findings 3 & 5)** |
| **8. Integration cannot bypass guard, evidence provenance & fail-closed paths** | Zero production files import `score_billing_guard.py`; no `EL_GUARD_OFF` or `os.getenv` in proposal; `authorizes_generation: False`, `opens_allowance: False`, `integrated: False`. | `PROPOSAL.md` leaves `generate_music_bed.py --generate` and `el_client.request` unguarded, and step 6 triggers a **second** unguarded `GET /v1/user/subscription` inside `el_client.request` -> `el_guard.before_spend` (Finding 5b). Token provenance omits `evaluated_at`, `tier`, `status`, `billing_period`, `next_character_count_reset_unix`, and extension fields (Finding 7c). | **FIX (Findings 5b & 7c)** |

---

## 4. Detailed Adversarial Findings & Precise Corrections

### Finding 1 (BLOCKER): `_keys()` rejects the real 34-key `GET /v1/user/subscription` raw response (`unknown_field`)
- **Location:** `score_billing_guard.py` lines 250–269 (`REQUIRED_KEYS`) and 377–385 (`_keys`), `PROPOSAL.md` lines 88–91, 150–151, 168–171.
- **Proof (`test_06_adversarial_finding_1_real_34_key_subscription_always_refuses`):**
  `PROPOSAL.md` §Integration path step 4 requires passing the raw bytes of `GET /v1/user/subscription` to `MeterBoard.decide(raw, ...)` without pre-filtering so `body_sha256` pins the actual raw HTTP response. However, tracked studio evidence (`EAR_REVIEW_J3046.md` lines 78–91 from `J2806` on 17 Nov 2026, Chief `desk 7005927729`, and `_desk/006/elevenlabs_subscription_snapshot_20261004.json`) proves that `GET /v1/user/subscription` on the studio's Creator account returns **34 top-level keys** (the 16 keys in `REQUIRED_KEYS` plus 18 standard account/voice/promo keys: `bfcm_2026_offer`, `can_extend_voice_limit`, `can_use_instant_voice_cloning`, `can_use_professional_voice_cloning`, `cancels_immediately`, `character_refresh_period`, `creator_arm_price`, `has_used_creator_coupon_on_account`, `has_used_starter_coupon_on_account`, `is_annual_four_months_subscriber`, `is_eligible_for_starter_promo`, `max_voice_add_edits`, `professional_voice_limit`, `professional_voice_slots_used`, `professional_voice_slots_used_in_workspace`, `voice_add_edit_counter`, `voice_limit`, `voice_slots_used`). Because `_keys()` raises `GuardRefused("unknown_field")` whenever `set(payload) - REQUIRED_KEYS` is non-empty, **every real raw `GET /v1/user/subscription` response will fail closed and burn the board**.
- **Precise correction:**
  1. Define `ALLOWED_OPTIONAL_KEYS` containing the documented non-billing top-level keys from the 34-key live response (`voice_limit`, `voice_slots_used`, `professional_voice_limit`, `professional_voice_slots_used`, `professional_voice_slots_used_in_workspace`, `max_voice_add_edits`, `voice_add_edit_counter`, `can_extend_voice_limit`, `can_use_instant_voice_cloning`, `can_use_professional_voice_cloning`, `character_refresh_period`, `cancels_immediately`, `creator_arm_price`, `has_used_creator_coupon_on_account`, `has_used_starter_coupon_on_account`, `is_annual_four_months_subscriber`, `is_eligible_for_starter_promo`, `bfcm_2026_offer`).
  2. In `_keys(payload)`: check `FLAT_OVERAGE_KEYS & present` first (`raise GuardRefused("overage")`), then check `missing = REQUIRED_KEYS - present` (checking `"current_overage" in missing` -> `overage`, `missing & EXTENSION_KEYS` -> `extensions`, `"currency" in missing` -> `currency`, any other missing required key -> `malformed_body`), and then check `extra = present - REQUIRED_KEYS - ALLOWED_OPTIONAL_KEYS` (`if extra: raise GuardRefused("unknown_field")`).
  3. If `character_refresh_period` is present, require `payload["character_refresh_period"] == "monthly_period"`; if `cancels_immediately` is present, require `payload["cancels_immediately"] is False`. Keep exact two-key validation (`set(nested) == {"amount", "currency"}`) on `current_overage`.

### Finding 2 (BLOCKER): `_invoices()` requires `next_invoice is None`, which is impossible on an active monthly Creator subscription (`invoices`)
- **Location:** `score_billing_guard.py` lines 418–428 (`_invoices`), `PROPOSAL.md` lines 96–98.
- **Proof (`test_07_adversarial_finding_2_active_subscription_next_invoice_always_refuses`):**
  `_entitlement()` requires `tier == "creator"`, `status == "active"`, and `billing_period == "monthly_period"`, while `_invoices()` requires `payload["next_invoice"] is None`. On an active recurring monthly Creator subscription, ElevenLabs `GET /v1/user/subscription` populates `next_invoice` with the upcoming monthly renewal invoice dict (e.g. `{"amount_due_cents": 2640, "subtotal_cents": 2200, "tax_cents": null, "discount_percent_off": null, "discount_amount_off": null, "discounts": [], "next_payment_attempt_unix": 1793361031, "payment_intent_status": null, "payment_intent_statusses": []}`, verified in `_desk/006/elevenlabs_subscription_snapshot_20261004.json` lines 29–39). Requiring `next_invoice is None` causes every healthy active Creator subscription response to fail closed with `GuardRefused("invoices")`.
- **Precise correction:**
  In `_invoices(payload)`:
  - Keep `payload["has_open_invoices"] is False`, `type(payload["open_invoices"]) is list`, `payload["open_invoices"] == []`, and `payload["pending_change"] is None`.
  - Allow `next_invoice` to be `None` **or** a `dict` where:
    - `amount_due_cents` and `subtotal_cents` are non-negative integers (`_exact_int(..., "invoices") >= 0`),
    - `next_payment_attempt_unix` is an integer `> int(fetched_at.timestamp())`,
    - `payment_intent_status` (if present) is `None` (no failed or open payment collection attempt), and
    - `payment_intent_statusses` (if present) is `[]`.

### Finding 3 (HIGH): `MeterBoard.consume()` accepts and echoes caller-tampered token fields
- **Location:** `score_billing_guard.py` lines 586–611 (`MeterBoard.decide` and `MeterBoard.consume`).
- **Proof (`test_08_adversarial_finding_3_consume_accepts_tampered_token_fields`):**
  `decide()` stores only `self._token_id` and `self._body_sha256`. `consume()` checks only `id`, `outcome`, `authorizes_generation`, and `body_sha256`, and then returns `out = dict(token)`. Mutating `token["would_allow_posts"] = 99`, `token["retries"] = 5`, `token["integrated"] = True`, `token["proposal_only"] = False`, `token["estimated_credits"] = 999_999`, `token["cash_gbp"] = "250.00"`, `token["music_length_ms"] = 600_000`, or `token["current_overage"] = {"amount": "42.00", "currency": "usd"}` after `decide()` succeeds in `consume()` and returns the forged values in the consumed receipt.
- **Precise correction:**
  In `MeterBoard`: store a deep copy of the issued token (`self._token = copy.deepcopy(token)`). In `consume(self, token, *, body_sha256)`: require `type(token) is dict`, `type(body_sha256) is str`, `body_sha256 == self._body_sha256`, and `token == self._token` (exact deep equality across all fields and nested `current_overage`), else raise `GuardRefused("inconsistent_meter")`. Construct the returned consumed receipt from `copy.deepcopy(self._token)` with `"consumed": True`.

### Finding 4 (HIGH): `_request()` allows `estimated_credits = 1` for a fixed 180,000 ms `music_v2` generation
- **Location:** `score_billing_guard.py` lines 239–240, 457–465 (`_request`), `test_score_billing_guard.py` lines 881–882.
- **Proof (`test_09_adversarial_finding_4_underestimated_credits_for_180s_music_passes`):**
  `_request()` hardcodes `music_length_ms == 180_000` (180 seconds), yet accepts any `estimated_credits` integer from `1` to `3000`. In `04_Audio/tools/el_guard.py` line 137, `characters_in(data)` estimates `/v1/music` cost as `len(prompt)` (~684 credits). With `estimated_credits = 1` (or `684`), `decide()` returns `pass_once` when `remaining_credits` is only `1` (or `684`), even though 180 s of ElevenLabs Music v2 bills ~2,475 credits (account-measured in `J2664`/`J2806`), 2,700 credits (published 900 credits/min), or 2,970 credits (with the 10% worst-case safety margin in `SCORE_SCOPE_J3042.json`).
- **Precise correction:**
  Define `MIN_ESTIMATED_CREDITS = 2970` (or require `2970 <= credits <= MAX_CREDITS` for the fixed `180_000 ms` duration, corresponding to published 900 credits/min × 3 min + 10% margin) and refuse any lower estimate (`1..2969`, including prompt-character estimates) with `GuardRefused("budget")`. Update `test_budget_edges` in `test_score_billing_guard.py` so `estimated_credits=1` and `2969` are tested as `budget` refusals and `2970..3000` pass.

### Finding 5 (HIGH): Ephemeral per-instance `MeterBoard`, missing `TTS_PAUSE` / unposted-spend lease fields, and integration double-GET / bypass conflict
- **Location:** `score_billing_guard.py` lines 294–303 (`LEASE_KEYS`), 554–590 (`MeterBoard`), `PROPOSAL.md` lines 131–164.
- **Proof (`test_10_adversarial_finding_5_new_meterboard_instance_bypasses_one_request_latch`):**
  1. `MeterBoard` tracks `_used` only on `self`. Creating a second `MeterBoard()` instance in the same process after a failed or consumed flight succeeds (`pass_once`), so a retry helper that instantiates `MeterBoard()` per call is not stopped by `MeterBoard`.
  2. `LEASE_KEYS` does not check `pause_file_present` (`TTS_PAUSE`) or `pending_unposted_credits` (unreconciled charges from local ledgers).
  3. In `PROPOSAL.md` §Integration path:
     - Step 2 says *"Do not point the existing `--generate` path at it"*, which leaves `generate_music_bed.py --generate` and `el_client.request("POST", "/v1/music", ...)` able to bypass `score_billing_guard` completely.
     - Step 4 performs one `GET /v1/user/subscription` and Step 6 requires `el_guard.before_spend` to run on the subsequent `POST /v1/music`. In `04_Audio/tools/el_client.py` line 40, `el_guard.before_spend` unconditionally calls `lambda: request("GET", "/v1/user/subscription", token, mode)[:2]`, which performs a **second** `GET /v1/user/subscription` (violating the single-GET rule in `J3141`/`J3143`) and discards the raw bytes.
- **Precise correction:**
  1. Add a module-level process latch `_PROCESS_FLIGHT_USED = False` guarded by a module-level `threading.Lock()` in `score_billing_guard.py` so that `MeterBoard.decide()` can only run **once per process lifetime** by default (with an explicit test-only reset helper or keyword forbidden in production, or a single-flight token registry that refuses a second `MeterBoard` for `holder == "hos009-score"`).
  2. Add `"pause_file_present"` (must be `False`, else `GuardRefused("paused")`) and `"pending_unposted_credits"` (must be exact integer `0`, else `GuardRefused("pending_spend")`) to `LEASE_KEYS` and `_lease()`.
  3. Update `PROPOSAL.md` §Integration path so that when a future integration is separately authorized by `J3143`: (a) `el_client.request` / `el_guard.before_spend` reuses the single fresh raw `GET /v1/user/subscription` response from the guard rather than issuing a second GET, and (b) `el_client.request` refuses any `POST /v1/music` that does not carry a consumed guard receipt when the guard is integrated.

### Finding 6 (MEDIUM): `_lease()` requires `acquired_at == fetched_at` microsecond equality and skips `_utc(acquired_at)`
- **Location:** `score_billing_guard.py` lines 486–488 (`_lease`).
- **Proof (`test_11_adversarial_finding_6_lease_timestamp_paradox_and_non_utc_offset`):**
  1. `PROPOSAL.md` step 3 acquires the one-recorder lock *before* step 4 performs `GET /v1/user/subscription`, so a real lock's `acquired_at` is earlier than `fetched_at` (`acquired_at <= fetched_at`). Yet `_lease()` checks `acquired != fetched_at` and refuses `acquired_at = fetched_at - 1ms` with `stale_lease`, forcing the caller to falsify `acquired_at = fetched_at`.
  2. `_lease()` checks `type(acquired) is not datetime` without calling `_utc(acquired, "stale_lease")`, so a non-UTC `datetime` (e.g. `+01:00`) equal to the same instant passes.
- **Precise correction:**
  In `_lease()`, validate `acquired = _utc(lease["acquired_at"], "stale_lease")` and require `fetched_at - FRESH_FOR <= acquired <= fetched_at` (lock acquired in UTC at or before `fetched_at`, within the 60-second freshness window).

### Finding 7 (LOW/MEDIUM): Key-error precedence in `_keys()`, bare JSON `NaN`/`Infinity` in `loads_strict()`, and provenance completeness on token
- **Location:** `score_billing_guard.py` lines 323–337 (`loads_strict`), 377–394 (`_keys`), 526–551 (`_evaluate`).
- **Proof (`test_12` and `test_13` in `probe_j3142.py`):**
  1. In `_keys()`, if `current_overage` is missing alongside `currency` (`missing == {"current_overage", "currency"}`), exact single-element set comparison `if missing == {"current_overage"}` is false and raises `malformed_body` instead of `overage`.
  2. In `loads_strict()`, `json.loads(text, object_pairs_hook=_pairs)` has no `parse_constant` hook, so bare non-standard JSON `NaN`/`Infinity` are accepted by `loads_strict()` itself.
  3. `_evaluate()` validates `now` (`current`), `tier`, `status`, `billing_period`, `next_character_count_reset_unix`, and the 4 extension fields, but omits them from the returned token dict.
- **Precise correction:**
  1. In `loads_strict()`, pass `parse_constant=lambda _: (_ for _ in ()).throw(GuardRefused("malformed_body"))` to `json.loads`.
  2. In `_keys()`, check `if "current_overage" in missing: raise GuardRefused("overage")`, `if missing & EXTENSION_KEYS: raise GuardRefused("extensions")`, `if "currency" in missing: raise GuardRefused("currency")`.
  3. Include `"evaluated_at": current.strftime("%Y-%m-%dT%H:%M:%SZ")`, `"tier": "creator"`, `"status": "active"`, `"billing_period": "monthly_period"`, `"next_character_count_reset_unix": reset`, `"max_character_limit_extension": 0`, `"max_credit_limit_extension": 0`, `"can_extend_character_limit": False`, and `"allowed_to_extend_character_limit": False` in the returned token so saved preflight provenance is self-contained.

---

## 5. Verification Commands & Preserved Holds

```bash
# 1. Existing J3141 unit tests in detached worktree at c9ef1e0aa51a363971f5de1f5648ece6826eec12:
python3 -m unittest discover -s /Volumes/MiniWork/scratch/J3141-target/jobs/reviews/J3141 -p 'test_*.py' -v
# -> Ran 17 tests in 0.003s — OK

# 2. Independent J3142 adversarial synthetic probe suite against c9ef1e0aa51a363971f5de1f5648ece6826eec12:
python3 jobs/reviews/J3142/probe_j3142.py /Volumes/MiniWork/scratch/J3141-target/jobs/reviews/J3141
# -> Ran 13 tests in 0.006s — OK
```

- **Preserved closures & holds:**
  - `J3047` permanent closure of the unused `J3043`/`J3045` allowance remains in force (no renewal, no pooling).
  - `J2808` rejection of `v01` and `v02` remains in force.
  - `J2035` (long assembly) and `J2171` (Shorts assembly) remain held (`blocked`).
  - Zero account calls, zero HTTP requests, zero generation, zero credits, `£0`, no production integration or deployment.
  - Handed to queued `J3143` (`HOS 009: decide reviewed guard and separate score scope`, `kind: chief`) for the elected Chief's decision.
