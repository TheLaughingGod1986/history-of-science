#!/usr/bin/env python3
"""J3145 independent adversarial synthetic test suite for revised HOS 009 score_billing_guard.py (c0c1848f).

Offline only: zero account calls, zero network calls, zero production mutations.
Reruns all J3142 baseline and adversarial probes against the revised API at
commit c0c1848f89d99bcc656d1aa862428b605bd678c9, verifies J3142 Findings 1-7
and Chief desk 7013542642 points a-e, and proves the remaining unresolved gaps
(Findings A-D).

Usage:
    python3 jobs/reviews/J3145/probe_j3145.py /path/to/jobs/reviews/J3141
"""

from __future__ import annotations

import ast
import fcntl
import hashlib
import json
import os
import subprocess
import sys
import tempfile
import threading
import time
import unittest
from datetime import datetime, timedelta, timezone
from email.utils import formatdate
from pathlib import Path

TARGET_DIR = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else None
if TARGET_DIR is not None:
    sys.path.insert(0, str(TARGET_DIR))

import score_billing_guard as sbg  # noqa: E402
from score_billing_guard import GuardRefused, MeterBoard  # noqa: E402

EXPECTED_GUARD_SHA256 = "7361cef3fb0742bb55477146a4faf6734d87201012760547ab53ac791e3350fa"
EXPECTED_TEST_SHA256 = "f54c021960e44aefacb921584f470823437b443ca4f3e6a7fac632d4c6b526fa"
EXPECTED_PROPOSAL_SHA256 = "99a0004e7a4ff827d1bf202486f678793f68bd40dee58ec4d2449e45cfd64051"
EXPECTED_SHAPE_SHA256 = "ba290b64740c96c3407af17da80d043be3bf840d1863518bfb011e047f9e647e"
EXPECTED_HASHES_SHA256 = "b0c97e74da75a37e9f4bd9fd18dd7068269966a2e1d0b5946bd94c275b6213ec"

RESET = 1_893_456_000

LIVE_17NOV_34_KEYS = (
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
)


def make_sub(**overrides) -> dict:
    base = {
        "allowed_to_extend_character_limit": False,
        "bfcm_2026_offer": None,
        "billing_period": "monthly_period",
        "can_extend_character_limit": False,
        "can_extend_voice_limit": False,
        "can_use_instant_voice_cloning": False,
        "can_use_professional_voice_cloning": False,
        "cancels_immediately": False,
        "character_count": 62_352,
        "character_limit": 121_114,
        "character_refresh_period": "monthly_period",
        "creator_arm_price": None,
        "currency": "usd",
        "current_overage": {"amount": "0", "currency": "usd"},
        "has_open_invoices": False,
        "has_used_creator_coupon_on_account": False,
        "has_used_starter_coupon_on_account": False,
        "is_annual_four_months_subscriber": None,
        "is_eligible_for_starter_promo": False,
        "max_character_limit_extension": 0,
        "max_credit_limit_extension": 0,
        "max_voice_add_edits": 5,
        "next_character_count_reset_unix": RESET,
        "next_invoice": {
            "amount_due_cents": 2200,
            "discount_amount_off": None,
            "discount_percent_off": None,
            "discounts": [],
            "next_payment_attempt_unix": RESET,
            "payment_intent_status": None,
            "payment_intent_statusses": [],
            "subtotal_cents": 2200,
            "tax_cents": 0,
        },
        "open_invoices": [],
        "pending_change": None,
        "professional_voice_limit": 1,
        "professional_voice_slots_used": 1,
        "professional_voice_slots_used_in_workspace": 1,
        "status": "active",
        "tier": "creator",
        "voice_add_edit_counter": 0,
        "voice_limit": 30,
        "voice_slots_used": 12,
    }
    base.update(overrides)
    return base


def make_raw(**overrides) -> bytes:
    return json.dumps(make_sub(**overrides)).encode("utf-8")


def make_req(**overrides) -> dict:
    base = {
        "holder": "hos009-score",
        "attempt": 1,
        "endpoint": "/v1/music",
        "model_id": "music_v2",
        "force_instrumental": True,
        "music_length_ms": 180_000,
        "query": "output_format=mp3_44100_128",
        "estimated_credits": 2_970,
        "cash_gbp": "0",
    }
    base.update(overrides)
    return base


class Harness:
    def __init__(self) -> None:
        self.dir = Path(tempfile.mkdtemp(prefix="j3145-probe-"))
        self.pause = self.dir / "TTS_PAUSE"
        self.ledger = self.dir / "ledger.jsonl"
        self.ledger.write_text("", encoding="utf-8")
        self.lock = self.dir / "elevenlabs.lock"
        self.store = self.dir / "hos009-score-single-use.json"
        self.write_lock()

    def write_lock(self, *, pid: int | None = None, started: datetime | str | None = None, extra: dict | None = None) -> None:
        moment = started or (datetime.now(timezone.utc) - timedelta(seconds=5)).replace(microsecond=0).isoformat()
        if isinstance(moment, datetime):
            moment = moment.isoformat()
        payload = {
            "pid": os.getpid() if pid is None else pid,
            "host": "mac-mini",
            "script": "probe_j3145.py",
            "started": moment,
        }
        if extra:
            payload.update(extra)
        self.lock.write_text(json.dumps(payload), encoding="utf-8")

    def date_hdr(self, seconds_ago: float = 2.0) -> str:
        return formatdate(time.time() - seconds_ago, usegmt=True)

    def decide(self, raw: object | None = None, board: MeterBoard | None = None, **kwargs) -> tuple[MeterBoard, dict]:
        b = board or MeterBoard()
        body = make_raw() if raw is None else raw
        args = {
            "http_status": 200,
            "date_header": self.date_hdr(),
            "request": make_req(),
            "lock_path": self.lock,
            "pause_path": self.pause,
            "ledger_path": self.ledger,
            "store_path": self.store,
        }
        args.update(kwargs)
        return b, b.decide(body, **args)


class StrSub(str):
    pass


class IntSub(int):
    pass


class DictSub(dict):
    pass


class BytesSub(bytes):
    pass


class J3145IndependentGuardReviewSuite(unittest.TestCase):
    """Independent adversarial review of HOS PR #667 at commit c0c1848f89d99bcc656d1aa862428b605bd678c9."""

    def test_01_exact_artifact_hashes_and_ast_no_network_or_env(self):
        guard_dir = Path(sbg.__file__).resolve().parent
        expected = {
            "score_billing_guard.py": EXPECTED_GUARD_SHA256,
            "test_score_billing_guard.py": EXPECTED_TEST_SHA256,
            "PROPOSAL.md": EXPECTED_PROPOSAL_SHA256,
            "subscription_shape.json": EXPECTED_SHAPE_SHA256,
            "HASHES.txt": EXPECTED_HASHES_SHA256,
        }
        for name, exp_sha in expected.items():
            digest = hashlib.sha256((guard_dir / name).read_bytes()).hexdigest()
            self.assertEqual(digest, exp_sha, f"SHA-256 mismatch on {name}")

        guard_path = guard_dir / "score_billing_guard.py"
        tree = ast.parse(guard_path.read_text(encoding="utf-8"))
        imported = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imported.add(alias.name.split(".")[0])
            elif isinstance(node, ast.ImportFrom) and node.module:
                imported.add(node.module.split(".")[0])
            elif isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
                self.assertNotIn(node.func.id, {"__import__", "eval", "exec", "compile"})
        self.assertEqual(
            imported,
            {"__future__", "copy", "datetime", "decimal", "email", "fcntl", "hashlib", "json", "os", "pathlib", "re", "threading"},
        )

    def test_02_nested_overage_and_currency_matrix_holds(self):
        for zero_str, cur in (("0", "usd"), ("0.0", "eur"), ("0.00", "gbp"), ("0.0000", "inr"), ("0.0", "pln")):
            with self.subTest(zero=zero_str, cur=cur):
                h = Harness()
                _, tok = h.decide(make_raw(currency=cur, current_overage={"amount": zero_str, "currency": cur}))
                self.assertEqual(tok["outcome"], "pass_once")
                self.assertEqual(tok["current_overage"], {"amount": zero_str, "currency": cur})
                self.assertFalse(tok["authorizes_generation"])
                self.assertFalse(tok["opens_allowance"])
                self.assertFalse(tok["integrated"])
                self.assertTrue(tok["proposal_only"])

        bad_overages = [
            (None, "overage"),
            (0, "overage"),
            ("0", "overage"),
            ([], "overage"),
            ({}, "overage"),
            ({"amount": "0"}, "overage"),
            ({"currency": "usd"}, "overage"),
            ({"amount": "0", "currency": "usd", "extra": "0"}, "overage"),
            ({"amount": None, "currency": "usd"}, "overage"),
            ({"amount": 0, "currency": "usd"}, "overage"),
            ({"amount": 0.0, "currency": "usd"}, "overage"),
            ({"amount": False, "currency": "usd"}, "overage"),
            ({"amount": "", "currency": "usd"}, "overage"),
            ({"amount": "00", "currency": "usd"}, "overage"),
            ({"amount": "00.00", "currency": "usd"}, "overage"),
            ({"amount": ".0", "currency": "usd"}, "overage"),
            ({"amount": "0.", "currency": "usd"}, "overage"),
            ({"amount": "-0", "currency": "usd"}, "overage"),
            ({"amount": "-0.00", "currency": "usd"}, "overage"),
            ({"amount": "+0", "currency": "usd"}, "overage"),
            ({"amount": "0e0", "currency": "usd"}, "overage"),
            ({"amount": "0.01", "currency": "usd"}, "overage"),
            ({"amount": "-0.01", "currency": "usd"}, "overage"),
            ({"amount": " 0", "currency": "usd"}, "overage"),
            ({"amount": "0 ", "currency": "usd"}, "overage"),
            ({"amount": "0\n", "currency": "usd"}, "overage"),
            ({"amount": "0\x00", "currency": "usd"}, "overage"),
            ({"amount": "NaN", "currency": "usd"}, "overage"),
            ({"amount": "Infinity", "currency": "usd"}, "overage"),
            ({"amount": "0", "currency": "USD"}, "currency"),
            ({"amount": "0", "currency": "cad"}, "currency"),
            ({"amount": "0", "currency": "eur"}, "currency"),
        ]
        for ov, expected_code in bad_overages:
            with self.subTest(overage=ov):
                h = Harness()
                with self.assertRaises(GuardRefused) as ctx:
                    h.decide(make_raw(current_overage=ov))
                self.assertEqual(ctx.exception.code, expected_code)

        # Flattened overage keys alongside valid nested current_overage refuse as overage
        for flat_key in ("current_overage_amount", "current_overage_currency"):
            h = Harness()
            with self.assertRaises(GuardRefused) as ctx:
                h.decide(make_raw(**{flat_key: "0"}))
            self.assertEqual(ctx.exception.code, "overage")

    def test_03_resolved_finding_1_and_desk_d_real_34_key_shape_and_untyped_scalars(self):
        """VERIFIED RESOLVED (J3142 Finding 1 & Desk 7013542642 point d):
        The 34-key subscription shape passes; an added 35th key refuses as unknown_field;
        missing current_overage refuses as overage even when currency is also missing (J3142 Finding 7);
        and the 3 untyped promo keys accept scalars but refuse nested dict/list/float."""
        self.assertEqual(set(LIVE_17NOV_34_KEYS), set(sbg.REQUIRED_KEYS))
        h = Harness()
        _, tok = h.decide(make_raw())
        self.assertEqual(tok["outcome"], "pass_once")

        # Added 35th key refuses
        h_extra = Harness()
        with self.assertRaises(GuardRefused) as ctx:
            h_extra.decide(make_raw(unexpected_field=1))
        self.assertEqual(ctx.exception.code, "unknown_field")

        # Untyped promo scalars accept None/bool/int/str, refuse dict/list/float
        for promo_key in ("bfcm_2026_offer", "creator_arm_price", "is_annual_four_months_subscriber"):
            for ok_val in (None, False, True, 0, 42, "promo"):
                h_ok = Harness()
                _, tok_ok = h_ok.decide(make_raw(**{promo_key: ok_val}))
                self.assertEqual(tok_ok["outcome"], "pass_once")
            for bad_val in ({}, {"a": 1}, [], [1], 1.5):
                h_bad = Harness()
                with self.assertRaises(GuardRefused) as ctx:
                    h_bad.decide(make_raw(**{promo_key: bad_val}))
                self.assertEqual(ctx.exception.code, "unknown_field")

        # Key-error precedence (J3142 Finding 7): missing current_overage + missing currency -> overage
        sub = make_sub()
        del sub["current_overage"]
        del sub["currency"]
        h_prec = Harness()
        with self.assertRaises(GuardRefused) as ctx:
            h_prec.decide(json.dumps(sub).encode("utf-8"))
        self.assertEqual(ctx.exception.code, "overage")

    def test_04_resolved_finding_2_scheduled_renewal_next_invoice_passes_and_bad_invoices_refuse(self):
        """VERIFIED RESOLVED (J3142 Finding 2):
        Active monthly Creator subscription with non-null scheduled renewal next_invoice passes,
        while collection activity, past payment attempt, discounts, or extra invoice keys refuse."""
        h_none = Harness()
        _, tok_none = h_none.decide(make_raw(next_invoice=None))
        self.assertEqual(tok_none["outcome"], "pass_once")

        h_sched = Harness()
        _, tok_sched = h_sched.decide(make_raw())
        self.assertEqual(tok_sched["outcome"], "pass_once")

        base_inv = make_sub()["next_invoice"]
        bad_invoices = [
            {**base_inv, "payment_intent_status": "processing"},
            {**base_inv, "payment_intent_statusses": ["processing"]},
            {**base_inv, "amount_due_cents": -1},
            {**base_inv, "subtotal_cents": -1},
            {**base_inv, "tax_cents": -1},
            {**base_inv, "next_payment_attempt_unix": int(time.time()) - 10},
            {**base_inv, "discounts": [{"id": "d1"}]},
            {**base_inv, "discount_amount_off": 100},
            {**base_inv, "discount_percent_off": 10},
            {**base_inv, "extra_key": 1},
        ]
        for inv in bad_invoices:
            h_bad = Harness()
            with self.assertRaises(GuardRefused) as ctx:
                h_bad.decide(make_raw(next_invoice=inv))
            self.assertEqual(ctx.exception.code, "invoices")

    def test_05_resolved_finding_3_consume_enforces_immutable_token(self):
        """VERIFIED RESOLVED (J3142 Finding 3):
        MeterBoard.consume() deep-compares the full token against self._token and refuses
        any mutated field with inconsistent_meter."""
        for field, forged in (
            ("estimated_credits", 1),
            ("cash_gbp", "25.00"),
            ("would_allow_posts", 99),
            ("retries", 5),
            ("integrated", True),
            ("proposal_only", False),
            ("music_length_ms", 600_000),
            ("current_overage", {"amount": "14.20", "currency": "usd"}),
            ("remaining_meter_units", 999_999),
        ):
            with self.subTest(field=field):
                h = Harness()
                board, tok = h.decide()
                forged_tok = dict(tok)
                forged_tok[field] = forged
                with self.assertRaises(GuardRefused) as ctx:
                    board.consume(forged_tok, body_sha256=tok["body_sha256"])
                self.assertEqual(ctx.exception.code, "inconsistent_meter")

    def test_06_resolved_finding_4_and_desk_a_e_tariff_floor_and_meter_mapping(self):
        """VERIFIED RESOLVED (J3142 Finding 4 & Desk 7013542642 points a & e):
        Floor is pinned at 2,970 credits (J2806 worst case; 2,475 measured; 2,700 published);
        1, 684, 2,475, 2,700, 2,969, and 3,001 credits refuse as budget;
        meter_units_per_credit() == 1 for the fixed 180,000 ms duration only;
        any other music_length_ms refuses as duration."""
        self.assertEqual(sbg.MIN_ESTIMATED_CREDITS, 2_970)
        self.assertEqual(sbg.MEASURED_CREDITS, 2_475)
        self.assertEqual(sbg.PUBLISHED_180S_CREDITS, 2_700)
        self.assertEqual(sbg.meter_units_per_credit(), 1)

        for bad_credits in (0, 1, 684, 2_475, 2_700, 2_969, 3_001, -2_970, True):
            h = Harness()
            with self.assertRaises(GuardRefused) as ctx:
                h.decide(request=make_req(estimated_credits=bad_credits))
            self.assertEqual(ctx.exception.code, "budget")

        for ok_credits in (2_970, 2_985, 3_000):
            h = Harness()
            _, tok = h.decide(
                make_raw(character_count=10_000 - ok_credits, character_limit=10_000),
                request=make_req(estimated_credits=ok_credits),
            )
            self.assertEqual(tok["outcome"], "pass_once")
            self.assertEqual(tok["remaining_meter_units"], ok_credits)

        # Insufficient capacity when remaining_meter_units == estimated_credits - 1
        h_low = Harness()
        with self.assertRaises(GuardRefused) as ctx:
            h_low.decide(
                make_raw(character_count=10_000 - 2_969, character_limit=10_000),
                request=make_req(estimated_credits=2_970),
            )
        self.assertEqual(ctx.exception.code, "insufficient_capacity")

        # Any duration other than 180,000 ms refuses
        for bad_ms in (60_000, 120_000, 179_999, 180_001, 240_000):
            h_dur = Harness()
            with self.assertRaises(GuardRefused) as ctx:
                h_dur.decide(request=make_req(music_length_ms=bad_ms))
            self.assertEqual(ctx.exception.code, "duration")

    def test_07_resolved_finding_6_and_7_lock_window_strict_json_and_token_provenance(self):
        """VERIFIED RESOLVED (J3142 Findings 6 & 7):
        - Lock started 5s before Date header passes; non-UTC offset on lock started refuses;
        - Bare JSON NaN/Infinity/-Infinity, BOM, and duplicate keys refuse in loads_strict();
        - Returned token carries full entitlement, extension, tariff, and timestamp provenance."""
        h = Harness()
        _, tok = h.decide()
        for key in (
            "evaluated_at",
            "fetched_at",
            "tier",
            "status",
            "billing_period",
            "next_character_count_reset_unix",
            "max_character_limit_extension",
            "max_credit_limit_extension",
            "can_extend_character_limit",
            "allowed_to_extend_character_limit",
            "remaining_meter_units",
            "meter_units_per_credit",
            "tariff_evidence",
            "measured_180s_credits",
            "published_180s_credits",
            "floor_credits",
        ):
            self.assertIn(key, tok)

        # Non-UTC offset on lock started refuses as stale_lease
        plus_one = timezone(timedelta(hours=1))
        h_tz = Harness()
        h_tz.write_lock(started=(datetime.now(timezone.utc) - timedelta(seconds=5)).astimezone(plus_one).isoformat())
        with self.assertRaises(GuardRefused) as ctx:
            h_tz.decide()
        self.assertEqual(ctx.exception.code, "stale_lease")

        # Bare NaN / Infinity / -Infinity refuse in loads_strict()
        for raw_const in (b'{"x": NaN}', b'{"x": Infinity}', b'{"x": -Infinity}'):
            with self.assertRaises(GuardRefused) as ctx:
                sbg.loads_strict(raw_const)
            self.assertEqual(ctx.exception.code, "malformed_body")

        # Duplicate key at top level or nested refuses as duplicate_key
        with self.assertRaises(GuardRefused) as ctx:
            sbg.loads_strict(b'{"a": 1, "a": 2}')
        self.assertEqual(ctx.exception.code, "duplicate_key")
        with self.assertRaises(GuardRefused) as ctx:
            sbg.loads_strict(b'{"current_overage": {"amount": "0", "amount": "0", "currency": "usd"}}')
        self.assertEqual(ctx.exception.code, "duplicate_key")

    def test_08_unresolved_finding_A_caller_chosen_paths_bypass_single_use_pause_and_ledger(self):
        """UNRESOLVED FINDING A (HIGH — Desk 7013542642 points b & c / Desk 7014651936 Gap 1):
        decide() accepts caller-chosen store_path, lock_path, pause_path, and ledger_path,
        and _named_file() checks only Path type and basename.
        (1) Passing the exact same raw subscription body and request twice with two different
            store_path directories returns pass_once BOTH times.
        (2) When TTS_PAUSE exists and ledger.jsonl has an unposted line in dir_a, passing
            pause_path and ledger_path from dir_b ignores both and returns pass_once."""
        raw = make_raw()
        req = make_req()

        h1 = Harness()
        # Simulate active TTS_PAUSE and pending spend in h1's directory:
        h1.pause.write_text("paused\n", encoding="utf-8")
        future_line = json.dumps({"time": (datetime.now(timezone.utc) + timedelta(seconds=30)).isoformat(), "status": 200})
        h1.ledger.write_text(future_line + "\n", encoding="utf-8")

        # Second directory h2 has no TTS_PAUSE, empty ledger, and a fresh store_path:
        h2 = Harness()
        _, tok1 = h2.decide(raw=raw, request=req)
        self.assertEqual(tok1["outcome"], "pass_once")

        # Third directory h3 replays the EXACT SAME raw body and request and ALSO gets pass_once:
        h3 = Harness()
        _, tok2 = h3.decide(raw=raw, request=req)
        self.assertEqual(tok2["outcome"], "pass_once")
        self.assertEqual(tok1["body_sha256"], tok2["body_sha256"])
        self.assertEqual(tok1["request_sha256"], tok2["request_sha256"])

    def test_09_unresolved_finding_B_lock_check_fails_when_pre_flocked_and_leaves_lock_unheld(self):
        """UNRESOLVED FINDING B (HIGH — Desk 7013542642 point c / Desk 7014651936 Gap 2):
        (1) Live el_guard.acquire_lock() creates elevenlabs.lock with O_EXCL and writes PID JSON
            without flock. If a caller actually holds an exclusive fcntl.flock(LOCK_EX) on its
            own open file descriptor to elevenlabs.lock before decide(), _lock() opens a new
            file description, gets BlockingIOError on flock(LOCK_EX | LOCK_NB), and REFUSES
            its own process with shared_meter!
        (2) When not pre-flocked, _lock() takes LOCK_EX and immediately unlocks (LOCK_UN) and
            closes fd in finally: before decide() returns, so no lock is held after decide()."""
        h = Harness()
        holder_fd = os.open(h.lock, os.O_RDWR)
        try:
            fcntl.flock(holder_fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
            # While this process holds an exclusive flock on elevenlabs.lock, decide() refuses!
            with self.assertRaises(GuardRefused) as ctx:
                h.decide()
            self.assertEqual(ctx.exception.code, "shared_meter")
        finally:
            fcntl.flock(holder_fd, fcntl.LOCK_UN)
            os.close(holder_fd)

        # Conversely, with just a plain file on disk (no flock held), decide() passes and releases
        # its transient flock before returning, leaving the file unlocked afterward:
        h2 = Harness()
        _, tok = h2.decide()
        self.assertEqual(tok["outcome"], "pass_once")
        probe_fd = os.open(h2.lock, os.O_RDWR)
        try:
            # Succeeds immediately because _lock() unlocked in finally:
            fcntl.flock(probe_fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        finally:
            fcntl.flock(probe_fd, fcntl.LOCK_UN)
            os.close(probe_fd)

    def test_10_unresolved_finding_C_loose_date_header_string_not_bound_to_response_body(self):
        """UNRESOLVED FINDING C (HIGH — Desk 7013542642 point c / Desk 7014651936 Gap 3):
        date_header is passed as a loose caller-supplied string separate from raw and http_status.
        An invented fresh Date string paired with any raw body (or a body from a different response)
        passes decide()."""
        h = Harness()
        stale_or_other_response_body = make_raw(character_count=50_000)
        invented_fresh_date = formatdate(time.time() - 1, usegmt=True)
        _, tok = h.decide(raw=stale_or_other_response_body, date_header=invented_fresh_date)
        self.assertEqual(tok["outcome"], "pass_once")

    def test_11_unresolved_finding_D_ledger_same_second_race_and_non_200_status_accepted(self):
        """UNRESOLVED FINDING D (LOW/MEDIUM — _pending() ledger validation):
        (1) Both HTTP Date headers and el_guard.after_spend ('timespec=\"seconds\"') have 1-second
            resolution. Because _pending() checks `_utc(when) > fetched` (strictly greater), a
            ledger spend recorded in the same second as the Date header (`when == fetched`) passes.
        (2) _pending() checks only `type(item.get('status')) is int`, so a ledger line with a
            failed/ambiguous status (e.g. 500 or 504) at or before `fetched` passes."""
        h = Harness()
        fetched_dt = datetime.now(timezone.utc).replace(microsecond=0) - timedelta(seconds=2)
        date_hdr = formatdate(fetched_dt.timestamp(), usegmt=True)
        # Same-second spend with status 500 at `when == fetched_dt`:
        h.ledger.write_text(
            json.dumps({"time": fetched_dt.isoformat(), "status": 500, "chars": 2970}) + "\n",
            encoding="utf-8",
        )
        _, tok = h.decide(date_header=date_hdr)
        self.assertEqual(tok["outcome"], "pass_once")


if __name__ == "__main__":
    if len(sys.argv) > 1 and Path(sys.argv[1]).exists():
        sys.argv.pop(1)
    unittest.main(verbosity=2)
