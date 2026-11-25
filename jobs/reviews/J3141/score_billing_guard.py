"""Proposed fail-closed billing guard for one HOS 009 replacement score.

Proposal only. Nothing in production imports this module. It does not call
an account, open a network connection, read the environment, POST, generate,
deploy, change billing, relax the live ElevenLabs guard, or open an allowance.

A pass means the synthetic evidence would satisfy this guard once. It still
has authorizes_generation false. J3145 reviews this revision. J3146 is the
decision that could authorize a later, separate integration. J3047 stays closed.

The nested overage rule is the reviewed offline mapping at
d047b06440591466d494a7377b9142cb1f4b0692 (HOS PR651, unmerged). This file
copies that rule for a fresh raw body. It does not import the unmerged
proposal, and it does not accept historical or flattened evidence.
"""

from __future__ import annotations

import copy
import fcntl
import hashlib
import json
import os
import re
import threading
from datetime import datetime, timedelta, timezone
from decimal import Decimal, InvalidOperation
from email.utils import parsedate_to_datetime
from pathlib import Path

MAPPING_COMMIT = "d047b06440591466d494a7377b9142cb1f4b0692"
PROPOSAL_ONLY = True
AUTHORIZES_GENERATION = False
OPENS_ALLOWANCE = False

# J2806_PROVENANCE.json preflight_tariff_and_guards, one music_v2 take.
# 2,475 is the account-measured reference (13.75 credits/s x 180s) and the
# character-meter delta on that take (43,725 - 41,250). It is not used as a
# lower declaration: the published 180s price is 2,700 and the recorded
# worst case is 2,970. The declaration floor is that higher evidenced figure.
MEASURED_CHARACTER_BEFORE = 41_250
MEASURED_CHARACTER_AFTER = 43_725
MEASURED_CREDITS = 2_475
PUBLISHED_CREDITS_PER_MIN = 900
PUBLISHED_180S_CREDITS = 2_700
WORST_CASE_180S_CREDITS = 2_970
MIN_ESTIMATED_CREDITS = WORST_CASE_180S_CREDITS
MAX_CREDITS = 3_000
MAX_MUSIC_LENGTH_MS = 180_000
FRESH_FOR = timedelta(seconds=60)
ENDPOINT = "/v1/music"
MODEL_ID = "music_v2"
QUERY = "output_format=mp3_44100_128"
HOLDER = "hos009-score"
CASH_GBP = "0"
CURRENCIES = ("usd", "eur", "inr", "pln", "gbp")
AMOUNT_RE = re.compile(r"0(?:\.0+)?")
LOCK_NAME = "elevenlabs.lock"
PAUSE_NAME = "TTS_PAUSE"
LEDGER_NAME = "ledger.jsonl"
STORE_NAME = "hos009-score-single-use.json"
TARIFF_EVIDENCE = "J2806_PROVENANCE.json"

REQUIRED_KEYS = frozenset(
    {
        "allowed_to_extend_character_limit",
        "bfcm_2026_offer",
        "billing_period",
        "can_extend_character_limit",
        "can_extend_voice_limit",
        "can_use_instant_voice_cloning",
        "can_use_professional_voice_cloning",
        "cancels_immediately",
        "character_count",
        "character_limit",
        "character_refresh_period",
        "creator_arm_price",
        "currency",
        "current_overage",
        "has_open_invoices",
        "has_used_creator_coupon_on_account",
        "has_used_starter_coupon_on_account",
        "is_annual_four_months_subscriber",
        "is_eligible_for_starter_promo",
        "max_character_limit_extension",
        "max_credit_limit_extension",
        "max_voice_add_edits",
        "next_character_count_reset_unix",
        "next_invoice",
        "open_invoices",
        "pending_change",
        "professional_voice_limit",
        "professional_voice_slots_used",
        "professional_voice_slots_used_in_workspace",
        "status",
        "tier",
        "voice_add_edit_counter",
        "voice_limit",
        "voice_slots_used",
    }
)
EXTENSION_KEYS = frozenset(
    {
        "max_character_limit_extension",
        "max_credit_limit_extension",
        "can_extend_character_limit",
        "allowed_to_extend_character_limit",
    }
)
UNTYPED_SCALAR_KEYS = frozenset(
    {
        "bfcm_2026_offer",
        "creator_arm_price",
        "is_annual_four_months_subscriber",
    }
)
BOOL_KEYS = frozenset(
    {
        "can_extend_voice_limit",
        "can_use_instant_voice_cloning",
        "can_use_professional_voice_cloning",
        "cancels_immediately",
        "has_open_invoices",
        "has_used_creator_coupon_on_account",
        "has_used_starter_coupon_on_account",
        "is_eligible_for_starter_promo",
    }
)
INT_KEYS = frozenset(
    {
        "max_voice_add_edits",
        "professional_voice_limit",
        "professional_voice_slots_used",
        "professional_voice_slots_used_in_workspace",
        "voice_add_edit_counter",
        "voice_limit",
        "voice_slots_used",
    }
)
INVOICE_KEYS = frozenset(
    {
        "amount_due_cents",
        "discount_amount_off",
        "discount_percent_off",
        "discounts",
        "next_payment_attempt_unix",
        "payment_intent_status",
        "payment_intent_statusses",
        "subtotal_cents",
        "tax_cents",
    }
)
FLAT_OVERAGE_KEYS = frozenset(
    {"current_overage_amount", "current_overage_currency"}
)
REQUEST_KEYS = frozenset(
    {
        "holder",
        "attempt",
        "endpoint",
        "model_id",
        "force_instrumental",
        "music_length_ms",
        "query",
        "estimated_credits",
        "cash_gbp",
    }
)
CALLER_ASSERTED = {
    "fetched_at": "caller_asserted_clock",
    "now": "caller_asserted_clock",
    "lease": "caller_asserted_lease",
    "acquired_at": "caller_asserted_lease",
    "pause_file_present": "caller_asserted_state",
    "pending_unposted_credits": "caller_asserted_state",
    "observed_character_count": "caller_asserted_state",
}


class GuardRefused(Exception):
    """The evidence does not permit a score request. No retry is implied."""

    def __init__(self, code: str):
        super().__init__(code)
        self.code = code


def meter_units_per_credit() -> int:
    """Units of character_count per music credit, from the one measured take.

    Unknown or non-integral mappings refuse. This does not treat a prompt
    length as a music price, and it does not apply to any other duration.
    """
    delta = MEASURED_CHARACTER_AFTER - MEASURED_CHARACTER_BEFORE
    if (
        delta != MEASURED_CREDITS
        or MEASURED_CREDITS != 2_475
        or PUBLISHED_CREDITS_PER_MIN * 3 != PUBLISHED_180S_CREDITS
        or WORST_CASE_180S_CREDITS != 2_970
        or MIN_ESTIMATED_CREDITS != WORST_CASE_180S_CREDITS
        or delta <= 0
        or delta % MEASURED_CREDITS != 0
        or WORST_CASE_180S_CREDITS < PUBLISHED_180S_CREDITS
        or WORST_CASE_180S_CREDITS < MEASURED_CREDITS
    ):
        raise GuardRefused("unknown_mapping")
    return delta // MEASURED_CREDITS


def _pairs(pairs: list[tuple[object, object]]) -> dict:
    out: dict = {}
    for key, value in pairs:
        if key in out:
            raise GuardRefused("duplicate_key")
        out[key] = value
    return out


def _reject_constant(_value: str) -> None:
    raise GuardRefused("malformed_body")


def loads_strict(raw: object) -> dict:
    """Parse one raw subscription body. Duplicate keys at any object fail closed."""
    if type(raw) is not bytes or raw == b"":
        raise GuardRefused("malformed_body")
    try:
        text = raw.decode("utf-8")
        value = json.loads(
            text,
            object_pairs_hook=_pairs,
            parse_constant=_reject_constant,
        )
    except GuardRefused:
        raise
    except (UnicodeError, json.JSONDecodeError, RecursionError, ValueError):
        raise GuardRefused("malformed_body") from None
    if type(value) is not dict:
        raise GuardRefused("malformed_body")
    return value


def _now() -> datetime:
    """The guard's own clock. Callers cannot pass a substitute."""
    return datetime.now(timezone.utc)


def _utc(value: object, code: str) -> datetime:
    if type(value) is not datetime or value.tzinfo is None:
        raise GuardRefused(code)
    if value.utcoffset() != timedelta(0):
        raise GuardRefused(code)
    return value.astimezone(timezone.utc)


def _exact_int(value: object, code: str) -> int:
    if type(value) is not int:
        raise GuardRefused(code)
    return value


def _date_header(value: object) -> datetime:
    """Freshness comes from the response Date header, not a caller datetime."""
    if type(value) is not str or value.strip() == "":
        raise GuardRefused("stale")
    try:
        parsed = parsedate_to_datetime(value)
    except (TypeError, ValueError, IndexError, OverflowError):
        raise GuardRefused("stale") from None
    if parsed is None:
        raise GuardRefused("stale")
    return _utc(parsed, "stale")


def _overage(payload: dict) -> tuple[str, str]:
    """Reviewed raw-API rule from the offline mapping. Historical evidence is not accepted."""
    if any(key in payload for key in FLAT_OVERAGE_KEYS):
        raise GuardRefused("overage")
    nested = payload.get("current_overage", None)
    if type(nested) is not dict or set(nested) != {"amount", "currency"}:
        raise GuardRefused("overage")
    amount = nested["amount"]
    currency = nested["currency"]
    if type(amount) is not str or AMOUNT_RE.fullmatch(amount) is None:
        raise GuardRefused("overage")
    try:
        parsed = Decimal(amount)
    except (InvalidOperation, ValueError):
        raise GuardRefused("overage") from None
    if not parsed.is_finite() or parsed.is_signed() or parsed != 0:
        raise GuardRefused("overage")
    if type(currency) is not str or currency not in CURRENCIES:
        raise GuardRefused("currency")
    if type(payload.get("currency")) is not str or payload["currency"] != currency:
        raise GuardRefused("currency")
    return amount, currency


def _keys(payload: dict) -> None:
    present = set(payload)
    extra = present - REQUIRED_KEYS
    missing = REQUIRED_KEYS - present
    if extra & FLAT_OVERAGE_KEYS:
        raise GuardRefused("overage")
    if extra:
        raise GuardRefused("unknown_field")
    if "current_overage" in missing:
        raise GuardRefused("overage")
    if missing & EXTENSION_KEYS:
        raise GuardRefused("extensions")
    if "currency" in missing:
        raise GuardRefused("currency")
    if missing:
        raise GuardRefused("malformed_body")


def _untyped_scalars(payload: dict) -> None:
    for key in UNTYPED_SCALAR_KEYS:
        value = payload[key]
        if value is None or type(value) is bool or type(value) is int or type(value) is str:
            continue
        raise GuardRefused("unknown_field")


def _entitlement(payload: dict) -> None:
    if (
        payload["tier"] != "creator"
        or payload["status"] != "active"
        or payload["billing_period"] != "monthly_period"
        or payload["character_refresh_period"] != "monthly_period"
        or type(payload["tier"]) is not str
        or type(payload["status"]) is not str
        or type(payload["billing_period"]) is not str
        or type(payload["character_refresh_period"]) is not str
    ):
        raise GuardRefused("unknown_entitlement")
    for key in BOOL_KEYS:
        if type(payload[key]) is not bool:
            raise GuardRefused("malformed_body")
    for key in INT_KEYS:
        if _exact_int(payload[key], "malformed_body") < 0:
            raise GuardRefused("malformed_body")
    if payload["cancels_immediately"] is not False:
        raise GuardRefused("invoices")


def _extensions(payload: dict) -> None:
    if (
        _exact_int(payload["max_character_limit_extension"], "extensions") != 0
        or _exact_int(payload["max_credit_limit_extension"], "extensions") != 0
        or payload["can_extend_character_limit"] is not False
        or payload["allowed_to_extend_character_limit"] is not False
    ):
        raise GuardRefused("extensions")


def _invoices(payload: dict, fetched: datetime) -> None:
    if payload["has_open_invoices"] is not False:
        raise GuardRefused("invoices")
    if type(payload["open_invoices"]) is not list or payload["open_invoices"] != []:
        raise GuardRefused("invoices")
    if payload["pending_change"] is not None:
        raise GuardRefused("pending_change")
    nxt = payload["next_invoice"]
    if nxt is None:
        return
    if type(nxt) is not dict or set(nxt) != INVOICE_KEYS:
        raise GuardRefused("invoices")
    if _exact_int(nxt["amount_due_cents"], "invoices") < 0:
        raise GuardRefused("invoices")
    if _exact_int(nxt["subtotal_cents"], "invoices") < 0:
        raise GuardRefused("invoices")
    when = _exact_int(nxt["next_payment_attempt_unix"], "invoices")
    if when <= int(fetched.timestamp()):
        raise GuardRefused("invoices")
    if nxt["payment_intent_status"] is not None or nxt["payment_intent_statusses"] != []:
        raise GuardRefused("invoices")
    if nxt["discounts"] != []:
        raise GuardRefused("invoices")
    if nxt["discount_amount_off"] is not None or nxt["discount_percent_off"] is not None:
        raise GuardRefused("invoices")
    tax = nxt["tax_cents"]
    if tax is not None and (type(tax) is not int or tax < 0):
        raise GuardRefused("invoices")


def _capacity(payload: dict, fetched: datetime, credits: int) -> tuple[int, int, int]:
    count = _exact_int(payload["character_count"], "malformed_body")
    limit = _exact_int(payload["character_limit"], "malformed_body")
    reset = _exact_int(payload["next_character_count_reset_unix"], "reset_inconsistent")
    if limit < count:
        raise GuardRefused("inconsistent_meter")
    if count < 0 or limit <= 0:
        raise GuardRefused("malformed_body")
    if reset <= int(fetched.timestamp()) + int(FRESH_FOR.total_seconds()):
        raise GuardRefused("reset_inconsistent")
    ratio = meter_units_per_credit()
    if type(ratio) is not int or ratio < 1:
        raise GuardRefused("unknown_mapping")
    remaining = limit - count
    needed = credits * ratio
    if remaining < needed:
        raise GuardRefused("insufficient_capacity")
    return count, limit, remaining


def _request(request: object) -> dict:
    if type(request) is not dict or set(request) != REQUEST_KEYS:
        raise GuardRefused("malformed_request")
    if request["holder"] != HOLDER or type(request["holder"]) is not str:
        raise GuardRefused("scope")
    attempt = request["attempt"]
    if type(attempt) is not int or attempt != 1:
        raise GuardRefused("retry")
    if request["endpoint"] != ENDPOINT or type(request["endpoint"]) is not str:
        raise GuardRefused("endpoint")
    if request["model_id"] != MODEL_ID or type(request["model_id"]) is not str:
        raise GuardRefused("model")
    if request["force_instrumental"] is not True:
        raise GuardRefused("not_instrumental")
    length = request["music_length_ms"]
    if type(length) is not int or length != MAX_MUSIC_LENGTH_MS:
        raise GuardRefused("duration")
    if request["query"] != QUERY or type(request["query"]) is not str:
        raise GuardRefused("malformed_request")
    credits = request["estimated_credits"]
    if (
        type(credits) is not int
        or credits < MIN_ESTIMATED_CREDITS
        or credits > MAX_CREDITS
    ):
        raise GuardRefused("budget")
    cash = request["cash_gbp"]
    if type(cash) is not str or cash != CASH_GBP:
        raise GuardRefused("cash")
    return request


def _named_file(path: object, name: str, code: str) -> Path:
    # PosixPath is the concrete type of Path("."). A str or a Path subclass refuses.
    if type(path) is not type(Path(".")) or path.name != name:
        raise GuardRefused(code)
    return path


def _pause(path: object) -> None:
    pause = _named_file(path, PAUSE_NAME, "paused")
    if not pause.parent.is_dir() or pause.exists():
        raise GuardRefused("paused")


def _pending(path: object, fetched: datetime) -> None:
    """A missing ledger is unknown, not zero. A line after the Date header is unposted."""
    ledger = _named_file(path, LEDGER_NAME, "pending_spend")
    if not ledger.is_file():
        raise GuardRefused("pending_spend")
    try:
        text = ledger.read_text(encoding="utf-8")
    except OSError:
        raise GuardRefused("pending_spend") from None
    for line in text.splitlines():
        if line.strip() == "":
            continue
        try:
            item = json.loads(line)
        except json.JSONDecodeError:
            raise GuardRefused("pending_spend") from None
        if type(item) is not dict or type(item.get("status")) is not int:
            raise GuardRefused("pending_spend")
        stamp = item.get("time")
        if type(stamp) is not str:
            raise GuardRefused("pending_spend")
        try:
            when = datetime.fromisoformat(stamp)
        except ValueError:
            raise GuardRefused("pending_spend") from None
        if _utc(when, "pending_spend") > fetched:
            raise GuardRefused("pending_spend")


def _lock(path: object, fetched: datetime, now: datetime) -> None:
    """The recorder lock is the lock file, exclusively flocked, held by this process."""
    lock = _named_file(path, LOCK_NAME, "malformed_lease")
    if not lock.is_file():
        raise GuardRefused("shared_meter")
    fd = os.open(lock, os.O_RDWR)
    try:
        try:
            fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            raise GuardRefused("shared_meter")
        try:
            lease = json.loads(lock.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError, UnicodeError):
            raise GuardRefused("malformed_lease") from None
        if type(lease) is not dict or set(lease) != {"pid", "host", "script", "started"}:
            raise GuardRefused("malformed_lease")
        if type(lease["pid"]) is not int or lease["pid"] != os.getpid():
            raise GuardRefused("shared_meter")
        if (
            type(lease["host"]) is not str
            or lease["host"] == ""
            or type(lease["script"]) is not str
            or lease["script"] == ""
        ):
            raise GuardRefused("malformed_lease")
        try:
            started = datetime.fromisoformat(lease["started"])
        except ValueError:
            raise GuardRefused("stale_lease") from None
        acquired = _utc(started, "stale_lease")
        if acquired > fetched or acquired > now or fetched - acquired > FRESH_FOR:
            raise GuardRefused("stale_lease")
    finally:
        fcntl.flock(fd, fcntl.LOCK_UN)
        os.close(fd)


def _claim_store(path: object, request_sha: str, body_sha: str) -> None:
    store = _named_file(path, STORE_NAME, "retry_or_shared_meter")
    store.parent.mkdir(parents=True, exist_ok=True)
    fd = os.open(store, os.O_RDWR | os.O_CREAT, 0o644)
    try:
        fcntl.flock(fd, fcntl.LOCK_EX)
        raw = os.read(fd, 1_000_000)
        if raw.strip() == b"":
            state: dict = {"used_requests": [], "used_bodies": []}
        else:
            try:
                state = json.loads(raw.decode("utf-8"))
            except (UnicodeError, json.JSONDecodeError):
                raise GuardRefused("retry_or_shared_meter") from None
        reqs = state.get("used_requests") if type(state) is dict else None
        bodies = state.get("used_bodies") if type(state) is dict else None
        if type(reqs) is not list or type(bodies) is not list or reqs or bodies:
            raise GuardRefused("retry_or_shared_meter")
        if request_sha in reqs or body_sha in bodies:
            raise GuardRefused("retry_or_shared_meter")
        reqs.append(request_sha)
        bodies.append(body_sha)
        payload = json.dumps(state, separators=(",", ":")).encode("utf-8")
        os.lseek(fd, 0, os.SEEK_SET)
        os.ftruncate(fd, 0)
        os.write(fd, payload)
    finally:
        fcntl.flock(fd, fcntl.LOCK_UN)
        os.close(fd)


def _fingerprints(raw: object, request: object) -> tuple[str, str]:
    if type(raw) is not bytes or raw == b"":
        raise GuardRefused("malformed_body")
    if type(request) is not dict:
        raise GuardRefused("malformed_request")
    try:
        encoded = json.dumps(request, sort_keys=True, separators=(",", ":")).encode("utf-8")
    except (TypeError, ValueError):
        raise GuardRefused("malformed_request") from None
    return hashlib.sha256(raw).hexdigest(), hashlib.sha256(encoded).hexdigest()


def _evaluate(
    raw: object,
    date_header: object,
    now: datetime,
    http_status: object,
    request: object,
    lock_path: object,
    pause_path: object,
    ledger_path: object,
    body_sha: str,
    request_sha: str,
) -> dict:
    if type(http_status) is not int or http_status != 200:
        raise GuardRefused("http_status")
    fetched = _date_header(date_header)
    current = _utc(now, "stale")
    if current < fetched:
        raise GuardRefused("inconsistent_clock")
    if current - fetched > FRESH_FOR:
        raise GuardRefused("stale")
    payload = loads_strict(raw)
    _keys(payload)
    _untyped_scalars(payload)
    _entitlement(payload)
    _extensions(payload)
    _invoices(payload, fetched)
    amount, currency = _overage(payload)
    asked = _request(request)
    credits = asked["estimated_credits"]
    count, limit, remaining = _capacity(payload, fetched, credits)
    _pause(pause_path)
    _pending(ledger_path, fetched)
    _lock(lock_path, fetched, current)
    ratio = meter_units_per_credit()
    return {
        "id": body_sha[:32] + ":" + fetched.strftime("%Y%m%dT%H%M%SZ"),
        "outcome": "pass_once",
        "proposal_only": PROPOSAL_ONLY,
        "authorizes_generation": AUTHORIZES_GENERATION,
        "opens_allowance": OPENS_ALLOWANCE,
        "integrated": False,
        "network_calls": 0,
        "would_allow_posts": 1,
        "retries": 0,
        "mapping_commit": MAPPING_COMMIT,
        "body_sha256": body_sha,
        "request_sha256": request_sha,
        "http_status": 200,
        "fetched_at": fetched.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "evaluated_at": current.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "fresh_for_seconds": int(FRESH_FOR.total_seconds()),
        "current_overage": {"amount": amount, "currency": currency},
        "character_count": count,
        "character_limit": limit,
        "remaining_meter_units": remaining,
        "meter_units_per_credit": ratio,
        "tariff_evidence": TARIFF_EVIDENCE,
        "measured_180s_credits": MEASURED_CREDITS,
        "published_180s_credits": PUBLISHED_180S_CREDITS,
        "floor_credits": MIN_ESTIMATED_CREDITS,
        "estimated_credits": credits,
        "cash_gbp": CASH_GBP,
        "endpoint": ENDPOINT,
        "model_id": MODEL_ID,
        "music_length_ms": MAX_MUSIC_LENGTH_MS,
        "holder": HOLDER,
        "tier": "creator",
        "status": "active",
        "billing_period": "monthly_period",
        "next_character_count_reset_unix": payload["next_character_count_reset_unix"],
        "max_character_limit_extension": 0,
        "max_credit_limit_extension": 0,
        "can_extend_character_limit": False,
        "allowed_to_extend_character_limit": False,
        "consumed": False,
    }


class MeterBoard:
    """One flight. The single-use file, not this object, survives a restart."""

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._used = False
        self._consumed = False
        self._token: dict | None = None
        self._body_sha256: str | None = None

    def decide(
        self,
        raw: object,
        *,
        http_status: object,
        date_header: object,
        request: object,
        lock_path: object,
        pause_path: object,
        ledger_path: object,
        store_path: object,
        **forbidden: object,
    ) -> dict:
        for key, code in CALLER_ASSERTED.items():
            if key in forbidden:
                raise GuardRefused(code)
        if forbidden:
            raise GuardRefused("network_forbidden")
        with self._lock:
            if self._used:
                raise GuardRefused("retry_or_shared_meter")
            self._used = True
        body_sha, request_sha = _fingerprints(raw, request)
        _claim_store(store_path, request_sha, body_sha)
        token = _evaluate(
            raw,
            date_header,
            _now(),
            http_status,
            request,
            lock_path,
            pause_path,
            ledger_path,
            body_sha,
            request_sha,
        )
        with self._lock:
            self._token = copy.deepcopy(token)
            self._body_sha256 = body_sha
        return copy.deepcopy(token)

    def consume(self, token: object, *, body_sha256: object) -> dict:
        with self._lock:
            if self._token is None or self._consumed:
                raise GuardRefused("retry")
            self._consumed = True
            if (
                type(token) is not dict
                or type(body_sha256) is not str
                or body_sha256 != self._body_sha256
                or token != self._token
            ):
                raise GuardRefused("inconsistent_meter")
            out = copy.deepcopy(self._token)
            out["consumed"] = True
            out["network_calls"] = 0
            out["authorizes_generation"] = False
            out["opens_allowance"] = False
            return out
