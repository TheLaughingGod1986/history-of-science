"""Proposed fail-closed billing guard for one HOS 009 replacement score.

Proposal only. Nothing in production imports this module. It does not call
an account, open a network connection, read the environment, POST, generate,
deploy, change billing, relax the live ElevenLabs guard, or open an allowance.

J3147 repairs the four gaps J3145 proved and J3146 left unresolved. A pass
still has authorizes_generation false. J3148 reviews this revision. J3146's
NOT YET stands until that review. J3047 stays closed.

The tariff figures below are one historical J2806 take. They are not a
guarantee of what a later request would be charged. A future price change is
unknown_mapping or budget, not a silent pass.

A stale Date burns the single-use file. That burn is fail-closed. Clearing
the file takes an explicit Chief ruling. This module never deletes it, and
it refuses to bind the live desk.

The nested overage rule is the reviewed offline mapping at
d047b06440591466d494a7377b9142cb1f4b0692 (HOS PR651, unmerged). This file
copies that rule for a fresh raw body. It does not import the unmerged
proposal, and it does not accept historical or flattened evidence.
"""

from __future__ import annotations

import copy
import hashlib
import hmac
import json
import os
import re
import secrets
import socket
import stat
import threading
from datetime import datetime, timedelta, timezone
from decimal import Decimal, InvalidOperation
from email.utils import parsedate_to_datetime
from pathlib import Path

MAPPING_COMMIT = "d047b06440591466d494a7377b9142cb1f4b0692"
PROPOSAL_ONLY = True
AUTHORIZES_GENERATION = False
OPENS_ALLOWANCE = False
TARIFF_CURRENT_GUARANTEE = False

# J2806_PROVENANCE.json preflight_tariff_and_guards, one music_v2 take.
# 2,475 is the account-measured reference (13.75 credits/s x 180s) and the
# character-meter delta on that take (43,725 - 41,250). It is not used as a
# lower declaration: the published 180s price is 2,700 and the recorded
# worst case is 2,970. The declaration floor is that higher evidenced figure.
# Those three numbers describe that one take. They do not guarantee a later bill.
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
RECORDER_SCRIPT = "hos009-score-proposal"

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
# Names and codes from the previous proposal stay. Path arguments join the
# same state refusal. Loose response fields are not evidence either.
CALLER_ASSERTED = {
    "fetched_at": "caller_asserted_clock",
    "now": "caller_asserted_clock",
    "lease": "caller_asserted_lease",
    "acquired_at": "caller_asserted_lease",
    "pause_file_present": "caller_asserted_state",
    "pending_unposted_credits": "caller_asserted_state",
    "observed_character_count": "caller_asserted_state",
    "store_path": "caller_asserted_state",
    "lock_path": "caller_asserted_state",
    "pause_path": "caller_asserted_state",
    "ledger_path": "caller_asserted_state",
    "date_header": "untrusted_receipt",
    "raw": "untrusted_receipt",
    "http_status": "untrusted_receipt",
}


class GuardRefused(Exception):
    """The evidence does not permit a score request. No retry is implied."""

    def __init__(self, code: str):
        super().__init__(code)
        self.code = code


# Process-local desk and recorder ownership. decide() never receives these.
_desk: Path | None = None
_held_fd: int | None = None
_held_started: str | None = None
_held_ino: int | None = None

# Receipts are sealed only inside read_subscription. The constructor refuses.
_RECEIPT_SECRET = secrets.token_bytes(32)
_ISSUED: set[int] = set()


class TransportReceipt:
    """One subscription response. Status, Date and raw bytes share one seal.

    A caller cannot build one of these. A frozen stand-in with the same
    fields is refused. The seal is checked again at consume.
    """

    __slots__ = ("status", "date_value", "raw", "_mac")

    def __new__(cls, *args: object, **kwargs: object) -> TransportReceipt:
        raise GuardRefused("untrusted_receipt")

    def __setattr__(self, name: str, value: object) -> None:
        raise GuardRefused("untrusted_receipt")

    def __delattr__(self, name: str) -> None:
        raise GuardRefused("untrusted_receipt")


def meter_units_per_credit() -> int:
    """Units of character_count per music credit, from the one measured take.

    Unknown or non-integral mappings refuse. This does not treat a prompt
    length as a music price, it does not apply to any other duration, and it
    does not claim the next request will move the meter by the same amount.
    """
    if TARIFF_CURRENT_GUARANTEE:
        raise GuardRefused("unknown_mapping")
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
    """Parse one JSON object. Duplicate keys and bare NaN or Infinity fail closed."""
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
    """Freshness comes from the sealed response Date, not a caller datetime."""
    if type(value) is not str or value.strip() == "":
        raise GuardRefused("stale")
    try:
        parsed = parsedate_to_datetime(value)
    except (TypeError, ValueError, IndexError, OverflowError):
        raise GuardRefused("stale") from None
    if parsed is None:
        raise GuardRefused("stale")
    return _utc(parsed, "stale")


def _live_desk(root: Path) -> bool:
    live = (Path.home() / "_desk").resolve()
    try:
        root.resolve().relative_to(live)
    except ValueError:
        return False
    return True


def bind_desk(root: object) -> None:
    """Point the proposal at one desk root. Not a decide() argument.

    Tests pass a temporary directory. The live desk is refused so this
    module cannot read or clear a real single-use file.
    """
    if type(root) is not type(Path(".")) or root.is_symlink() or not root.is_dir():
        raise GuardRefused("unbound_desk")
    if _live_desk(root):
        raise GuardRefused("live_desk_forbidden")
    global _desk
    _desk = root


def release_test_holder() -> None:
    """Close this process's recorder descriptor. Does not delete any file.

    Tests call this between fixtures. decide() and consume() do not.
    """
    global _held_fd, _held_started, _held_ino
    fd = _held_fd
    _held_fd = None
    _held_started = None
    _held_ino = None
    if fd is not None:
        os.close(fd)


def _paths() -> dict[str, Path]:
    root = _desk
    if type(root) is not type(Path(".")) or root.is_symlink() or not root.is_dir():
        raise GuardRefused("unbound_desk")
    if _live_desk(root):
        raise GuardRefused("live_desk_forbidden")
    lock = root / "locks" / LOCK_NAME
    pause = root / "elevenlabs" / PAUSE_NAME
    ledger = root / "elevenlabs" / LEDGER_NAME
    store = root / "elevenlabs" / STORE_NAME
    for path in (lock, pause, ledger, store):
        if path.is_symlink():
            raise GuardRefused("retry_or_shared_meter")
    return {"lock": lock, "pause": pause, "ledger": ledger, "store": store}


def _pid_alive(pid: int) -> bool:
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        return True
    return True


def _dead_holder(lock: Path) -> bool:
    """True only when the lock names a dead pid on this host. Does not unlink."""
    try:
        holder = json.loads(lock.read_text(encoding="utf-8") or "{}")
    except (OSError, json.JSONDecodeError, UnicodeError):
        return False
    if type(holder) is not dict:
        return False
    if holder.get("host") != socket.gethostname():
        return False
    pid = holder.get("pid")
    if type(pid) is not int or pid <= 0:
        return False
    return not _pid_alive(pid)


def hold_recorder() -> None:
    """Take the recorder lock the way el_guard does: O_EXCL, then keep it.

    This is not called from decide() or consume(). Those only observe the
    descriptor this function left open. The descriptor is read-write so the
    check can re-read the bytes without opening a second file or flocking.
    Creation is still O_EXCL. The check never flocks, closes, or unlinks.
    A dead same-host holder is replaced once, here, matching el_guard.
    A live holder is shared_meter.
    """
    global _held_fd, _held_started, _held_ino
    if _held_fd is not None:
        return
    lock = _paths()["lock"]
    if lock.parent.is_symlink():
        raise GuardRefused("shared_meter")
    lock.parent.mkdir(parents=True, exist_ok=True)
    started = _now().replace(microsecond=0).isoformat()
    me = {
        "pid": os.getpid(),
        "host": socket.gethostname(),
        "script": RECORDER_SCRIPT,
        "started": started,
    }
    encoded = json.dumps(me).encode("utf-8")
    for attempt in range(2):
        try:
            fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_RDWR, 0o644)
        except FileExistsError:
            if attempt == 1 or not _dead_holder(lock):
                raise GuardRefused("shared_meter") from None
            try:
                lock.unlink()
            except OSError:
                raise GuardRefused("shared_meter") from None
            continue
        try:
            os.write(fd, encoded)
            info = os.fstat(fd)
        except OSError:
            os.close(fd)
            raise GuardRefused("shared_meter") from None
        if not stat.S_ISREG(info.st_mode):
            os.close(fd)
            raise GuardRefused("shared_meter")
        _held_fd = fd
        _held_started = started
        _held_ino = info.st_ino
        return
    raise GuardRefused("shared_meter")


def recorder_held() -> bool:
    """True when this process still has the O_EXCL descriptor open."""
    return _held_fd is not None and _held_started is not None


def _observe_lock(fetched: datetime, now: datetime) -> None:
    """Confirm this process still owns the recorder lock. Never takes it.

    No flock, no O_EXCL, no close, no unlink. The descriptor hold_recorder
    kept open has to match the path inode, the pid, the host, and the same
    started timestamp, inside the freshness window.
    """
    fd = _held_fd
    started_held = _held_started
    ino = _held_ino
    if fd is None or type(started_held) is not str or type(ino) is not int:
        raise GuardRefused("shared_meter")
    lock = _paths()["lock"]
    if lock.is_symlink() or not lock.is_file():
        raise GuardRefused("shared_meter")
    try:
        st_fd = os.fstat(fd)
        st_path = lock.stat()
    except OSError:
        raise GuardRefused("shared_meter") from None
    if (
        not stat.S_ISREG(st_fd.st_mode)
        or st_fd.st_ino != ino
        or st_path.st_ino != st_fd.st_ino
    ):
        raise GuardRefused("shared_meter")
    try:
        os.lseek(fd, 0, os.SEEK_SET)
        raw = os.read(fd, 4096)
        lease = json.loads(raw.decode("utf-8"))
    except (OSError, json.JSONDecodeError, UnicodeError):
        raise GuardRefused("malformed_lease") from None
    if type(lease) is not dict or set(lease) != {"pid", "host", "script", "started"}:
        raise GuardRefused("malformed_lease")
    if type(lease["pid"]) is not int or lease["pid"] != os.getpid():
        raise GuardRefused("shared_meter")
    if lease["host"] != socket.gethostname() or type(lease["host"]) is not str:
        raise GuardRefused("shared_meter")
    if type(lease["script"]) is not str or lease["script"] == "":
        raise GuardRefused("malformed_lease")
    if lease["started"] != started_held or type(lease["started"]) is not str:
        raise GuardRefused("stale_lease")
    try:
        acquired = _utc(datetime.fromisoformat(lease["started"]), "stale_lease")
    except ValueError:
        raise GuardRefused("stale_lease") from None
    if acquired > fetched or acquired > now or fetched - acquired > FRESH_FOR:
        raise GuardRefused("stale_lease")


def _canonical(status: int, date_value: str, raw: bytes) -> bytes:
    date_b = date_value.encode("utf-8")
    return (
        status.to_bytes(8, "big", signed=True)
        + len(date_b).to_bytes(8, "big")
        + date_b
        + len(raw).to_bytes(8, "big")
        + raw
    )


def _seal(status: int, date_value: str, raw: bytes) -> TransportReceipt:
    if type(status) is not int or type(date_value) is not str or type(raw) is not bytes:
        raise GuardRefused("untrusted_receipt")
    if date_value.strip() == "" or raw == b"":
        raise GuardRefused("untrusted_receipt")
    mac = hmac.new(_RECEIPT_SECRET, _canonical(status, date_value, raw), hashlib.sha256).digest()
    receipt = object.__new__(TransportReceipt)
    object.__setattr__(receipt, "status", status)
    object.__setattr__(receipt, "date_value", date_value)
    object.__setattr__(receipt, "raw", raw)
    object.__setattr__(receipt, "_mac", mac)
    _ISSUED.add(id(receipt))
    return receipt


def read_subscription(fetch: object) -> TransportReceipt:
    """Seal one transport result. fetch is called once and returns (status, headers, body).

    Date is taken from that headers object. A later swap of the body fails
    the seal. This is the only sealer. decide() does not call fetch.
    """
    if not callable(fetch):
        raise GuardRefused("untrusted_receipt")
    got = fetch()
    if type(got) is not tuple or len(got) != 3:
        raise GuardRefused("untrusted_receipt")
    status, headers, raw = got
    if type(status) is not int or type(headers) is not dict or type(raw) is not bytes:
        raise GuardRefused("untrusted_receipt")
    dates = [value for key, value in headers.items() if type(key) is str and key.lower() == "date"]
    if len(dates) != 1 or type(dates[0]) is not str:
        raise GuardRefused("untrusted_receipt")
    return _seal(status, dates[0], raw)


def _require_receipt(receipt: object) -> TransportReceipt:
    if type(receipt) is not TransportReceipt or id(receipt) not in _ISSUED:
        raise GuardRefused("untrusted_receipt")
    status = receipt.status
    date_value = receipt.date_value
    raw = receipt.raw
    mac = receipt._mac
    if (
        type(status) is not int
        or type(date_value) is not str
        or type(raw) is not bytes
        or type(mac) is not bytes
    ):
        raise GuardRefused("untrusted_receipt")
    expected = hmac.new(
        _RECEIPT_SECRET, _canonical(status, date_value, raw), hashlib.sha256
    ).digest()
    if not hmac.compare_digest(mac, expected):
        raise GuardRefused("untrusted_receipt")
    return receipt


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


def _pause(path: Path) -> None:
    if path.is_symlink() or not path.parent.is_dir() or path.exists():
        raise GuardRefused("paused")


def _explicitly_reconciled(item: dict) -> bool:
    """A ledger line is reconciled only when the line itself says so.

    This is not a decide() argument. Both the flag and a non-empty note
    have to be present. A status-200 spend at or after the subscription
    Date still refuses: reconciliation does not move the clock.
    """
    note = item.get("reconciliation")
    return item.get("reconciled") is True and type(note) is str and note.strip() != ""


def _pending(path: Path, fetched: datetime) -> None:
    """A missing ledger is unknown, not zero. Same-second and later lines are unposted.

    Failed or non-integer statuses refuse unless that line is explicitly
    reconciled. Parsing uses loads_strict, so duplicate keys and bare
    NaN or Infinity refuse as well.
    """
    if path.is_symlink() or not path.is_file():
        raise GuardRefused("pending_spend")
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        raise GuardRefused("pending_spend") from None
    for line in text.splitlines():
        if line.strip() == "":
            continue
        item = loads_strict(line.encode("utf-8"))
        status = item.get("status")
        if type(status) is not int or status != 200:
            if not _explicitly_reconciled(item):
                raise GuardRefused("pending_spend")
        stamp = item.get("time")
        if type(stamp) is not str:
            raise GuardRefused("pending_spend")
        try:
            when = datetime.fromisoformat(stamp)
        except ValueError:
            raise GuardRefused("pending_spend") from None
        if _utc(when, "pending_spend") >= fetched:
            raise GuardRefused("pending_spend")


def _claim_store(request_sha: str, body_sha: str) -> None:
    """Record one flight at the pinned store. A second line, or a second path, refuses.

    The file is never deleted. A refusal after this write, including a stale
    Date, leaves the flight burned until a Chief ruling says otherwise.
    """
    store = _paths()["store"]
    store.parent.mkdir(parents=True, exist_ok=True)
    import fcntl

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
    receipt: TransportReceipt,
    now: datetime,
    request: object,
    body_sha: str,
    request_sha: str,
) -> dict:
    fetched = _date_header(receipt.date_value)
    current = _utc(now, "stale")
    if current < fetched:
        raise GuardRefused("inconsistent_clock")
    if current - fetched > FRESH_FOR:
        raise GuardRefused("stale")
    if type(receipt.status) is not int or receipt.status != 200:
        raise GuardRefused("http_status")
    payload = loads_strict(receipt.raw)
    _keys(payload)
    _untyped_scalars(payload)
    _entitlement(payload)
    _extensions(payload)
    _invoices(payload, fetched)
    amount, currency = _overage(payload)
    asked = _request(request)
    credits = asked["estimated_credits"]
    count, limit, remaining = _capacity(payload, fetched, credits)
    paths = _paths()
    _pause(paths["pause"])
    _pending(paths["ledger"], fetched)
    _observe_lock(fetched, current)
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
        "tariff_current_guarantee": TARIFF_CURRENT_GUARANTEE,
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
    """One flight. The pinned single-use file, not this object, survives a restart."""

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._used = False
        self._consumed = False
        self._token: dict | None = None
        self._body_sha256: str | None = None
        self._receipt: TransportReceipt | None = None
        self._lock_started: str | None = None

    @property
    def used(self) -> bool:
        return self._used

    def decide(self, receipt: object, *, request: object, **forbidden: object) -> dict:
        for key, code in CALLER_ASSERTED.items():
            if key in forbidden:
                raise GuardRefused(code)
        if forbidden:
            raise GuardRefused("network_forbidden")
        sealed = _require_receipt(receipt)
        with self._lock:
            if self._used:
                raise GuardRefused("retry_or_shared_meter")
            self._used = True
        body_sha, request_sha = _fingerprints(sealed.raw, request)
        _claim_store(request_sha, body_sha)
        token = _evaluate(sealed, _now(), request, body_sha, request_sha)
        with self._lock:
            self._token = copy.deepcopy(token)
            self._body_sha256 = body_sha
            self._receipt = sealed
            self._lock_started = _held_started
        return copy.deepcopy(token)

    def consume(self, token: object, *, body_sha256: object) -> dict:
        with self._lock:
            if self._token is None or self._consumed or self._receipt is None:
                raise GuardRefused("retry")
            self._consumed = True
            if (
                type(token) is not dict
                or type(body_sha256) is not str
                or body_sha256 != self._body_sha256
                or token != self._token
            ):
                raise GuardRefused("inconsistent_meter")
            sealed = _require_receipt(self._receipt)
            fetched = _date_header(sealed.date_value)
            current = _utc(_now(), "stale")
            if current < fetched or current - fetched > FRESH_FOR:
                raise GuardRefused("stale")
            if _held_started != self._lock_started or type(self._lock_started) is not str:
                raise GuardRefused("stale_lease")
            paths = _paths()
            _pause(paths["pause"])
            _pending(paths["ledger"], fetched)
            _observe_lock(fetched, current)
            out = copy.deepcopy(self._token)
            out["consumed"] = True
            out["network_calls"] = 0
            out["authorizes_generation"] = False
            out["opens_allowance"] = False
            return out
