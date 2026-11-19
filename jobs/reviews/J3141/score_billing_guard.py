"""Proposed fail-closed billing guard for one HOS 009 replacement score.

Proposal only. Nothing in production imports this module. It does not call
an account, open a network connection, read the environment, POST, generate, deploy,
change billing, relax the live ElevenLabs guard, or open an allowance.

A pass means the synthetic evidence would satisfy this guard once. It still
has authorizes_generation false. J3142 reviews it. J3143 is the decision that
could authorize a later, separate integration. J3047 stays closed.

The nested overage rule is the reviewed offline mapping at
d047b06440591466d494a7377b9142cb1f4b0692 (HOS PR651, unmerged). This file
copies that rule for a fresh raw body. It does not import the unmerged
proposal, and it does not accept historical or flattened evidence.
"""

from __future__ import annotations

import hashlib
import json
import re
import threading
from datetime import datetime, timedelta, timezone
from decimal import Decimal, InvalidOperation

MAPPING_COMMIT = "d047b06440591466d494a7377b9142cb1f4b0692"
PROPOSAL_ONLY = True
AUTHORIZES_GENERATION = False
OPENS_ALLOWANCE = False

MAX_CREDITS = 3000
MAX_MUSIC_LENGTH_MS = 180_000
FRESH_FOR = timedelta(seconds=60)
ENDPOINT = "/v1/music"
MODEL_ID = "music_v2"
QUERY = "output_format=mp3_44100_128"
HOLDER = "hos009-score"
CASH_GBP = "0"
CURRENCIES = ("usd", "eur", "inr", "pln", "gbp")
AMOUNT_RE = re.compile(r"0(?:\.0+)?")

REQUIRED_KEYS = frozenset(
    {
        "tier",
        "status",
        "billing_period",
        "character_count",
        "character_limit",
        "max_character_limit_extension",
        "max_credit_limit_extension",
        "can_extend_character_limit",
        "allowed_to_extend_character_limit",
        "next_character_count_reset_unix",
        "currency",
        "current_overage",
        "has_open_invoices",
        "open_invoices",
        "next_invoice",
        "pending_change",
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
LEASE_KEYS = frozenset(
    {
        "exclusive",
        "holder",
        "peers",
        "hosts",
        "observed_character_count",
        "acquired_at",
    }
)


class GuardRefused(Exception):
    """The evidence does not permit a score request. No retry is implied."""

    def __init__(self, code: str):
        super().__init__(code)
        self.code = code


def _pairs(pairs: list[tuple[object, object]]) -> dict:
    out: dict = {}
    for key, value in pairs:
        if key in out:
            raise GuardRefused("duplicate_key")
        out[key] = value
    return out


def loads_strict(raw: object) -> dict:
    """Parse one raw subscription body. Duplicate keys at any object fail closed."""
    if type(raw) is not bytes or raw == b"":
        raise GuardRefused("malformed_body")
    try:
        text = raw.decode("utf-8")
        value = json.loads(text, object_pairs_hook=_pairs)
    except GuardRefused:
        raise
    except (UnicodeError, json.JSONDecodeError, RecursionError, ValueError):
        raise GuardRefused("malformed_body") from None
    if type(value) is not dict:
        raise GuardRefused("malformed_body")
    return value


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
    if not missing:
        return
    if missing == {"current_overage"}:
        raise GuardRefused("overage")
    if missing <= EXTENSION_KEYS:
        raise GuardRefused("extensions")
    if missing == {"currency"}:
        raise GuardRefused("currency")
    raise GuardRefused("malformed_body")


def _entitlement(payload: dict) -> None:
    if (
        payload["tier"] != "creator"
        or payload["status"] != "active"
        or payload["billing_period"] != "monthly_period"
        or type(payload["tier"]) is not str
        or type(payload["status"]) is not str
        or type(payload["billing_period"]) is not str
    ):
        raise GuardRefused("unknown_entitlement")


def _extensions(payload: dict) -> None:
    if (
        _exact_int(payload["max_character_limit_extension"], "extensions") != 0
        or _exact_int(payload["max_credit_limit_extension"], "extensions") != 0
        or payload["can_extend_character_limit"] is not False
        or payload["allowed_to_extend_character_limit"] is not False
    ):
        raise GuardRefused("extensions")


def _invoices(payload: dict) -> None:
    if (
        payload["has_open_invoices"] is not False
        or type(payload["open_invoices"]) is not list
        or payload["open_invoices"] != []
        or payload["next_invoice"] is not None
    ):
        raise GuardRefused("invoices")
    if payload["pending_change"] is not None:
        raise GuardRefused("pending_change")


def _capacity(payload: dict, fetched_at: datetime) -> tuple[int, int, int]:
    count = _exact_int(payload["character_count"], "malformed_body")
    limit = _exact_int(payload["character_limit"], "malformed_body")
    reset = _exact_int(payload["next_character_count_reset_unix"], "reset_inconsistent")
    if count < 0 or limit <= 0:
        raise GuardRefused("malformed_body")
    if limit < count:
        raise GuardRefused("inconsistent_meter")
    if reset <= int(fetched_at.timestamp()) + int(FRESH_FOR.total_seconds()):
        raise GuardRefused("reset_inconsistent")
    return count, limit, limit - count


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
    if type(credits) is not int or credits < 1 or credits > MAX_CREDITS:
        raise GuardRefused("budget")
    cash = request["cash_gbp"]
    if type(cash) is not str or cash != CASH_GBP:
        raise GuardRefused("cash")
    return request


def _lease(lease: object, *, holder: str, fetched_at: datetime, character_count: int) -> None:
    if type(lease) is not dict or set(lease) != LEASE_KEYS:
        raise GuardRefused("malformed_lease")
    if lease["exclusive"] is not True:
        raise GuardRefused("shared_meter")
    peers = lease["peers"]
    hosts = lease["hosts"]
    if (
        type(peers) is not int
        or peers != 0
        or type(hosts) is not list
        or hosts != [HOLDER]
        or lease["holder"] != holder
    ):
        raise GuardRefused("shared_meter")
    acquired = lease["acquired_at"]
    if type(acquired) is not datetime or acquired != fetched_at:
        raise GuardRefused("stale_lease")
    observed = lease["observed_character_count"]
    if type(observed) is not int or observed != character_count:
        raise GuardRefused("inconsistent_meter")


def _evaluate(
    raw: object,
    fetched_at: object,
    now: object,
    http_status: object,
    lease: object,
    request: object,
    forbidden: dict,
) -> dict:
    if forbidden:
        raise GuardRefused("network_forbidden")
    if type(http_status) is not int or http_status != 200:
        raise GuardRefused("http_status")
    fetched = _utc(fetched_at, "stale")
    current = _utc(now, "stale")
    if current < fetched:
        raise GuardRefused("inconsistent_clock")
    if current - fetched > FRESH_FOR:
        raise GuardRefused("stale")
    payload = loads_strict(raw)
    _keys(payload)
    _entitlement(payload)
    _extensions(payload)
    _invoices(payload)
    amount, currency = _overage(payload)
    count, limit, remaining = _capacity(payload, fetched)
    asked = _request(request)
    credits = asked["estimated_credits"]
    if remaining < credits:
        raise GuardRefused("insufficient_capacity")
    _lease(lease, holder=asked["holder"], fetched_at=fetched, character_count=count)
    body_sha = hashlib.sha256(raw).hexdigest()
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
        "http_status": 200,
        "fetched_at": fetched.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "fresh_for_seconds": int(FRESH_FOR.total_seconds()),
        "current_overage": {"amount": amount, "currency": currency},
        "character_count": count,
        "character_limit": limit,
        "remaining_credits": remaining,
        "estimated_credits": credits,
        "cash_gbp": CASH_GBP,
        "endpoint": ENDPOINT,
        "model_id": MODEL_ID,
        "music_length_ms": MAX_MUSIC_LENGTH_MS,
        "holder": HOLDER,
    }


class MeterBoard:
    """One in-process flight. The first decide burns it, pass or refusal.

    A second decide is a retry or a shared-meter collision. This is not the
    live recorder lock and it does not coordinate another machine.
    """

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._used = False
        self._consumed = False
        self._token_id: str | None = None
        self._body_sha256: str | None = None

    def decide(
        self,
        raw: object,
        *,
        fetched_at: object,
        now: object,
        http_status: object,
        lease: object,
        request: object,
        **forbidden: object,
    ) -> dict:
        with self._lock:
            if self._used:
                raise GuardRefused("retry_or_shared_meter")
            self._used = True
        token = _evaluate(
            raw, fetched_at, now, http_status, lease, request, forbidden
        )
        with self._lock:
            self._token_id = token["id"]
            self._body_sha256 = token["body_sha256"]
        return dict(token)

    def consume(self, token: object, *, body_sha256: object) -> dict:
        with self._lock:
            if self._token_id is None or self._consumed:
                raise GuardRefused("retry")
            self._consumed = True
            if (
                type(token) is not dict
                or token.get("id") != self._token_id
                or token.get("outcome") != "pass_once"
                or token.get("authorizes_generation") is not False
                or type(body_sha256) is not str
                or body_sha256 != self._body_sha256
                or token.get("body_sha256") != body_sha256
            ):
                raise GuardRefused("inconsistent_meter")
            out = dict(token)
            out["consumed"] = True
            out["network_calls"] = 0
            out["authorizes_generation"] = False
            out["opens_allowance"] = False
            return out
