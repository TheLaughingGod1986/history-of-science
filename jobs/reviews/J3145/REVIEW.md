# J3145 — Independent Adversarial Review of Repaired HOS 009 Score Billing Guard (HOS PR #667, `c0c1848f`)

- **Reviewer:** `gemini` (`gemini-argon`, specialist worker on the Mac mini; not the implementer `cursor` of `J3144` and not the elected Chief)
- **Date:** 19 November 2026
- **Reviewed Target:** HOS PR #667 (`cursor/J3141-score-guard`), exact commit `c0c1848f89d99bcc656d1aa862428b605bd678c9`
- **Upstream References:** `J3142` independent review (`18c281b046f74c94aa2ebb101ecfaeec5ee10a5f`, `desk 7013983650`), Chief rulings `desk 7013542642`, `desk 7014134135`, and `desk 7014651936`, `J3144` implementation (`desk 7014517404`), and unmerged offline mapping HOS PR #651 commit `d047b06440591466d494a7377b9142cb1f4b0692`
- **Authority & Scope:** Independent reviewer recommendation only. This review performs **no account calls, no HTTP requests, no generation, no production integration, no deployment, no billing change, and no allowance authorization**. `J3047` permanent closure of the unused `J3043`/`J3045` allowance, `J2808` rejection of `v01`/`v02`, and the `J2035`/`J2171` holds remain intact. Elected Chief decides in `J3146`.

---

## 1. Verdict: **FIX** (J3142 Findings 1, 2, 3, 4, 6, 7 and Chief Desk 7013542642 Points a, d, e Resolved; 3 High-Severity Enforcement/Binding Gaps + 1 Medium Ledger-Boundary Gap Remain)

Commit `c0c1848f89d99bcc656d1aa862428b605bd678c9` remains offline, stdlib-only, free of network/environment imports, and unimported by production tools (`04_Audio/tools/el_guard.py`, `el_client.py`, `generate_music_bed.py`). All 17 of `J3144`'s synthetic unit tests pass (`0.357s`), and independent adversarial testing (`jobs/reviews/J3145/probe_j3145.py`, 11 test suites) confirms that `c0c1848f` resolves six of the seven `J3142` findings and three of the five Chief desk `7013542642` points (`a`, `d`, `e`).

However, independent adversarial probes prove **three high-severity enforcement/binding gaps and one medium ledger-resolution gap** (`Unresolved Findings A–D` below, also aligned with `desk 7014547460` and `desk 7014651936` Gaps 1–3) that **must be fixed offline before any production integration (`J3146`)**:

1. **Unresolved Finding A (HIGH — Caller-chosen `store_path`, `lock_path`, `pause_path`, and `ledger_path` bypass durable single-use, `TTS_PAUSE`, and pending-ledger checks):**
   `MeterBoard.decide()` accepts `store_path`, `lock_path`, `pause_path`, and `ledger_path` as caller arguments and `_named_file()` checks only `type(path) is type(Path("."))` and `path.name == name`. Passing the exact same raw subscription body and request twice with two different `store_path` directories returns `pass_once` both times (`test_08`). Similarly, when `TTS_PAUSE` exists and `ledger.jsonl` has an unposted spend in the real desk directory, pointing `pause_path` and `ledger_path` at a second directory ignores both and returns `pass_once`.
2. **Unresolved Finding B (HIGH — `_lock()` contradicts live `el_guard.acquire_lock()`, refuses when pre-flocked by the same process, and releases its flock before `decide()` returns):**
   Live `04_Audio/tools/el_guard.py` (`acquire_lock()`) creates `<desk>/locks/elevenlabs.lock` with `O_CREAT | O_EXCL | O_WRONLY`, writes the 4-key PID JSON, closes the descriptor without `fcntl.flock`, and holds the lock file until `atexit` (`release_lock()`). In `score_billing_guard.py`, `_lock()` opens a new file descriptor to `elevenlabs.lock`, calls `fcntl.flock(fd, LOCK_EX | LOCK_NB)`, and unlocks/closes `fd` in `finally:` before `decide()` returns. Consequently: (a) if the current process actually holds an exclusive `fcntl.flock(LOCK_EX)` on its own descriptor to `elevenlabs.lock`, `_lock()` gets `BlockingIOError` on the new file description and **refuses its own process with `GuardRefused("shared_meter")`** (`test_09`); and (b) when not pre-flocked, `_lock()` accepts any plain unlocked file containing `os.getpid()` and leaves `elevenlabs.lock` completely unlocked when `decide()` returns.
3. **Unresolved Finding C (HIGH — `date_header` is a loose caller-supplied string unbound to `raw` and `http_status`; live `el_client` double-GET remains unwired):**
   `MeterBoard.decide()` refuses `fetched_at` and `now` kwargs, but takes `date_header` as a standalone `str` separate from `raw` and `http_status`. A caller can pair an invented fresh `Date` string (or a `Date` header from another response) with a stale or different response's `raw` body and pass `decide()` (`test_10`). The header, status, and body bytes must be fields of a single response object/envelope. (In live `04_Audio/tools/el_client.py`, `before_spend` still issues its own `GET /v1/user/subscription`; per Chief `desk 7014651936`, live `el_client.py`/`el_guard.py` must not be modified until a later Chief integration scope after the offline guard passes review.)
4. **Unresolved Finding D (LOW/MEDIUM — `_pending()` 1-second timestamp equality race and non-200 status acceptance):**
   Both HTTP `Date` headers and `el_guard.after_spend()` (`timespec="seconds"`, `04_Audio/tools/el_guard.py` line 183) have 1-second timestamp resolution. Because `_pending()` checks only `if _utc(when, "pending_spend") > fetched:` (strictly greater) and `type(item.get("status")) is int`, a spend logged in `ledger.jsonl` during the exact same second as `fetched` (`when == fetched`), or a line with a failed/ambiguous HTTP status (e.g. `500` or `504`), passes `_pending()` (`test_11`).

---

## 2. Exact Commit & Artifact Hashes Verified

Checked in an isolated detached worktree (`/Volumes/MiniWork/scratch/J3145-target`) at `c0c1848f89d99bcc656d1aa862428b605bd678c9`:

| File | SHA-256 | Status |
|---|---|---|
| `jobs/reviews/J3141/score_billing_guard.py` | `7361cef3fb0742bb55477146a4faf6734d87201012760547ab53ac791e3350fa` | Matches `HASHES.txt` & `J3144` report |
| `jobs/reviews/J3141/test_score_billing_guard.py` | `f54c021960e44aefacb921584f470823437b443ca4f3e6a7fac632d4c6b526fa` | 17/17 tests PASS (`0.357s`) |
| `jobs/reviews/J3141/PROPOSAL.md` | `99a0004e7a4ff827d1bf202486f678793f68bd40dee58ec4d2449e45cfd64051` | Verified |
| `jobs/reviews/J3141/subscription_shape.json` | `ba290b64740c96c3407af17da80d043be3bf840d1863518bfb011e047f9e647e` | Verified (34 key names & types, no account values) |
| `jobs/reviews/J3141/HASHES.txt` | `b0c97e74da75a37e9f4bd9fd18dd7068269966a2e1d0b5946bd94c275b6213ec` | Verified |
| `jobs/reviews/J3145/probe_j3145.py` | Independent adversarial probe suite (this review) | 11/11 suites PASS (`0.050s`) |

---

## 3. Verification Matrix: `J3142` Findings (1–7) and Chief Desk `7013542642` Points (`a–e`)

| Item | Requirement | Status in `c0c1848f` | Independent Probe Verification |
|---|---|---|---|
| **Desk 7013542642 (a) / J3142 Finding 4** | Evidence-based 180s duration tariff floor (`MIN_ESTIMATED_CREDITS = 2,970` from `J2806` worst case; `2,475` measured reference; `2,700` published); refuse `1` credit or `< 2,970` | **RESOLVED** | `test_06`: `0`, `1`, `684`, `2475`, `2700`, `2969`, `3001`, `-2970`, `True` all refuse as `budget`; `2970..3000` pass when capacity suffices |
| **Desk 7013542642 (b) / J3142 Finding 5** | Durable single-use across `MeterBoard` instances and process restarts | **PARTIAL -> FIX (`Finding A`)** | Same `store_path` refuses across instances and subprocesses, **but** `store_path` is caller-chosen: passing a second directory passes the identical body and request a second time (`test_08`) |
| **Desk 7013542642 (c) / J3142 Finding 5 & 6** | No caller-asserted freshness or lease; trusted response `Date`, guard clock `_now()`, real recorder lock, disk `TTS_PAUSE` and `ledger.jsonl` | **PARTIAL -> FIX (`Findings A, B, C, D`)** | `fetched_at`/`now`/`lease` kwargs refuse, **but**: (1) `lock_path`/`pause_path`/`ledger_path` are caller-chosen (`test_08`); (2) `_lock()` fails with `shared_meter` when pre-flocked by the same process and releases its flock before returning (`test_09`); (3) `date_header` is a loose string not bound to a response object (`test_10`) |
| **Desk 7013542642 (d) / J3142 Finding 1 & 2** | Redacted real 34-key subscription fixture (`subscription_shape.json`), scheduled renewal `next_invoice`, fail closed on added key or collection activity | **RESOLVED** | `test_03` & `test_04`: 34-key payload + 9-key scheduled renewal `next_invoice` pass; 35th key refuses as `unknown_field`; non-scalar on 3 untyped promo keys refuses as `unknown_field`; processing payment/discounts/past invoice date refuse as `invoices` |
| **Desk 7013542642 (e)** | Explicit credits-to-character-meter mapping (`meter_units_per_credit() == 1` from `43,725 - 41,250 == 2,475` for 180s only; refuse any other duration or unknown mapping) | **RESOLVED** | `test_06`: `meter_units_per_credit() == 1`; any `music_length_ms != 180_000` refuses as `duration`; `remaining < estimated_credits * ratio` refuses as `insufficient_capacity` |
| **J3142 Finding 3** | Immutable receipt in `MeterBoard.consume()` | **RESOLVED** | `test_05`: deep copy stored in `self._token`; mutating any field (`estimated_credits`, `cash_gbp`, `current_overage`, `would_allow_posts`, `retries`, `integrated`, `proposal_only`, `music_length_ms`, `remaining_meter_units`) refuses as `inconsistent_meter` |
| **J3142 Finding 6** | Lock `started <= fetched_at` within 60s window and strict UTC offset check | **RESOLVED** | `test_07`: lock acquired 5s before `Date` in UTC passes; non-UTC offset (`+01:00`) refuses as `stale_lease` |
| **J3142 Finding 7** | `_keys()` `current_overage` precedence, `loads_strict()` `parse_constant` rejecting bare `NaN`/`Infinity`, and full token provenance fields | **RESOLVED** | `test_03` & `test_07`: missing `current_overage` + missing `currency` raises `overage`; bare `NaN`/`Infinity`/`-Infinity` raise `malformed_body`; all 16 provenance fields present on token |

---

## 4. Detailed Unresolved Findings & Required Corrections

### Unresolved Finding A (HIGH): Caller-Chosen `store_path`, `lock_path`, `pause_path`, and `ledger_path` Bypass Durable Single-Use, `TTS_PAUSE`, and Pending-Ledger Guards
- **Location:** `score_billing_guard.py` lines 444–461 (`_named_file`, `_pause`, `_pending`), 486–490 (`_lock`), 524–526 (`_claim_store`), 649–684 (`MeterBoard.decide`).
- **Proof (`test_08_unresolved_finding_A_caller_chosen_paths_bypass_single_use_pause_and_ledger`):**
  1. `_named_file(path, name, code)` checks only `type(path) is type(Path(".")) and path.name == name`.
  2. Calling `MeterBoard().decide(raw, ..., store_path=dir1 / "hos009-score-single-use.json")` and then `MeterBoard().decide(raw, ..., store_path=dir2 / "hos009-score-single-use.json")` with the **exact same `raw` bytes and `request`** returns `outcome: "pass_once"` both times.
  3. Creating `TTS_PAUSE` and a pending spend line in `dir1` and passing `pause_path=dir2 / "TTS_PAUSE"` and `ledger_path=dir2 / "ledger.jsonl"` completely bypasses the pause and pending-spend checks and returns `pass_once`.
- **Precise correction:**
  1. Derive all four paths (`<desk>/locks/elevenlabs.lock`, `<desk>/elevenlabs/TTS_PAUSE`, `<desk>/elevenlabs/ledger.jsonl`, and `<desk>/elevenlabs/hos009-score-single-use.json`) internally from one fixed desk root directory inside `score_billing_guard.py` (using a module-level desk root constant that tests may point at a temp desk root only via an internal/module attribute, never via `decide()` arguments).
  2. Remove `store_path`, `lock_path`, `pause_path`, and `ledger_path` from `MeterBoard.decide()` parameters and add them to `CALLER_ASSERTED` so passing any of those four path arguments to `decide()` raises `GuardRefused`.
  3. Add a test proving that calling `decide()` twice with the same body (even if the caller attempts to pass a `store_path` argument) refuses on the second call, and document in the module docstring that a stale-Date refusal burning the single-use file is fail-closed by design and clearing it requires an explicit Chief ruling on the desk.

### Unresolved Finding B (HIGH): `_lock()` Contradicts `el_guard.acquire_lock()`, Refuses When Pre-Flocked by This Process, and Releases Its Flock Before `decide()` Returns
- **Location:** `score_billing_guard.py` lines 486–521 (`_lock`) vs `04_Audio/tools/el_guard.py` lines 83–135 (`acquire_lock`, `release_lock`).
- **Proof (`test_09_unresolved_finding_B_lock_check_fails_when_pre_flocked_and_leaves_lock_unheld`):**
  1. In Unix/macOS, `fcntl.flock()` locks are per open file description (`os.open()`). When the current process opens `elevenlabs.lock` and holds `fcntl.flock(holder_fd, fcntl.LOCK_EX | fcntl.LOCK_NB)` before calling `decide()`, `_lock()` opens a second file descriptor (`fd = os.open(lock, os.O_RDWR)`), attempts `fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)`, catches `BlockingIOError`, and **refuses its own process with `GuardRefused("shared_meter")`**.
  2. Live `el_guard.acquire_lock()` does **not** use `fcntl.flock()`: it creates `<desk>/locks/elevenlabs.lock` atomically via `os.open(path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o644)`, writes `{"pid", "host", "script", "started"}`, closes the file descriptor, sets `el_guard._held = True`, and keeps the file until process exit (`release_lock()`).
  3. Because `_lock()` calls `fcntl.flock(fd, fcntl.LOCK_UN)` in `finally:` before returning, no flock is held after `decide()` returns, and any plain unlocked file on disk containing `pid == os.getpid()` passes `_lock()`.
- **Precise correction:**
  1. `_lock()` must **never** call `fcntl.flock()`, acquire the lock, or release the lock itself.
  2. Instead, `_lock()` must verify that **this process currently holds** the recorder lock from `decide()` through `consume()`/`POST`: check that `<desk>/locks/elevenlabs.lock` is a regular file (not a symlink), parses as the exact 4-key dict `{"pid", "host", "script", "started"}` with `pid == os.getpid()`, `host == socket.gethostname()`, non-empty `script`, UTC `started` satisfying `fetched - FRESH_FOR <= started <= fetched <= now`, and that the recorder lock-hold state for this process is active and unreleased (and re-verify the lock file still belongs to `os.getpid()` with the same `started` timestamp inside `consume()`). Add tests for both cases: held by this process passes, not held refuses.

### Unresolved Finding C (HIGH): Loose `date_header` String Is Not Bound to the Response Object Carrying `raw` and `http_status`
- **Location:** `score_billing_guard.py` lines 649–684 (`MeterBoard.decide`).
- **Proof (`test_10_unresolved_finding_C_loose_date_header_string_not_bound_to_response_body`):**
  `decide()` takes `raw`, `http_status`, and `date_header` as three separate arguments. A caller can supply an invented fresh `date_header` string (e.g. `formatdate(time.time() - 1, usegmt=True)`) alongside a stale raw body or a body from a different response and receive `pass_once`.
- **Precise correction:**
  1. Require `decide()` to accept a single immutable response object/envelope (e.g., an exact `SubscriptionResponse` dataclass/frozen object or verified response unit containing `status`, `headers` / `date`, and `body` from one fetch) and refuse any loose `date_header` or `raw` argument or any response whose header and body provenance do not belong to the same single response instance.
  2. Add a test proving that a loose `date_header` string or a fresh `Date` paired with a different response's body refuses.
  3. Keep this change strictly inside the unintegrated proposal (`jobs/reviews/J3141/`): do **not** edit live `04_Audio/tools/el_client.py` or `04_Audio/tools/el_guard.py` prior to the Chief's `J3146` integration scope.

### Unresolved Finding D (LOW/MEDIUM): `_pending()` 1-Second Timestamp Equality (`when == fetched`) and Non-200 Ledger Status
- **Location:** `score_billing_guard.py` lines 457–483 (`_pending`).
- **Proof (`test_11_unresolved_finding_D_ledger_same_second_race_and_non_200_status_accepted`):**
  Both HTTP `Date` headers and `el_guard.after_spend()` (`timespec="seconds"`) have 1-second precision. Because `_pending()` checks `if _utc(when, "pending_spend") > fetched:`, a ledger spend recorded in the same second as `fetched` (`when == fetched`), or a line with a non-200 status (`status != 200`, e.g., `500` or `504`), passes `_pending()`.
- **Precise correction:**
  In `_pending()`, parse each line with `loads_strict(line.encode("utf-8"))`, require `item.get("status") == 200` (or refuse non-200 / ambiguous ledger lines unless explicitly reconciled), and refuse `if _utc(when, "pending_spend") >= fetched:` so the subscription `GET` timestamp is strictly newer (`fetched > when`) than every logged spend.

---

## 5. Verification Commands & Preserved Holds

```bash
# 1. Existing J3144 unit tests in detached worktree at c0c1848f89d99bcc656d1aa862428b605bd678c9:
python3 -m unittest discover -s /Volumes/MiniWork/scratch/J3145-target/jobs/reviews/J3141 -p 'test_*.py' -v
# -> Ran 17 tests in 0.357s — OK

# 2. Independent J3145 adversarial synthetic probe suite against c0c1848f89d99bcc656d1aa862428b605bd678c9:
python3 /Volumes/MiniWork/scratch/J3142-review/jobs/reviews/J3145/probe_j3145.py /Volumes/MiniWork/scratch/J3145-target/jobs/reviews/J3141
# -> Ran 11 tests in 0.050s — OK
```

- **Preserved closures & holds:**
  - `J3047` permanent closure of the unused `J3043`/`J3045` allowance remains in force (no renewal, no pooling).
  - `J2808` rejection of `v01` and `v02` remains in force.
  - `J2035` (long assembly) and `J2171` (Shorts assembly) remain held (`blocked`).
  - Zero account calls, zero HTTP requests, zero generation, zero credits, `£0`, no production integration or deployment.
  - Handed to queued `J3146` (`HOS 009: decide the reviewed music guard and score scope`, `kind: chief`) for the elected Chief's decision.
