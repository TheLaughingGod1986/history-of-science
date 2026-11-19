#!/usr/bin/env python3
"""J3142 independent adversarial synthetic test suite for HOS 009 score_billing_guard.py.

Offline only: zero account calls, zero network calls, zero production mutations.
Usage:
    python3 jobs/reviews/J3142/probe_j3142.py /path/to/jobs/reviews/J3141
"""

from __future__ import annotations

import ast
import hashlib
import json
import sys
import threading
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

TARGET_DIR = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else None
if TARGET_DIR is not None:
    sys.path.insert(0, str(TARGET_DIR))

import score_billing_guard as sbg  # noqa: E402
from score_billing_guard import GuardRefused, MeterBoard  # noqa: E402

EXPECTED_GUARD_SHA256 = "d6a87058662335da0285f1c609cdfbe3285554236fceda6aa8d2aed36b9b3be5"
FETCHED = datetime(2026, 11, 19, 15, 0, 0, tzinfo=timezone.utc)
RESET = 1_796_035_831

# The 34 top-level keys recorded from the live 17 Nov 2026 GET /v1/user/subscription
# in EAR_REVIEW_J3046.md (lines 78-91) and Chief desk 7005927729.
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
        "tier": "creator",
        "status": "active",
        "billing_period": "monthly_period",
        "character_count": 62_352,
        "character_limit": 121_114,
        "max_character_limit_extension": 0,
        "max_credit_limit_extension": 0,
        "can_extend_character_limit": False,
        "allowed_to_extend_character_limit": False,
        "next_character_count_reset_unix": RESET,
        "currency": "usd",
        "current_overage": {"amount": "0", "currency": "usd"},
        "has_open_invoices": False,
        "open_invoices": [],
        "next_invoice": None,
        "pending_change": None,
    }
    base.update(overrides)
    return base


def make_raw(**overrides) -> bytes:
    return json.dumps(make_sub(**overrides)).encode("utf-8")


def make_lease(**overrides) -> dict:
    base = {
        "exclusive": True,
        "holder": "hos009-score",
        "peers": 0,
        "hosts": ["hos009-score"],
        "observed_character_count": 62_352,
        "acquired_at": FETCHED,
    }
    base.update(overrides)
    return base


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


class StrSub(str):
    pass


class IntSub(int):
    pass


class DictSub(dict):
    pass


class BytesSub(bytes):
    pass


class J3142IndependentGuardReviewSuite(unittest.TestCase):
    """Independent verification of what holds and what fails in J3141 c9ef1e0a."""

    def test_01_pinned_hash_and_ast_no_network_or_env(self):
        guard_path = Path(sbg.__file__).resolve()
        digest = hashlib.sha256(guard_path.read_bytes()).hexdigest()
        self.assertEqual(digest, EXPECTED_GUARD_SHA256)

        tree = ast.parse(guard_path.read_text(encoding="utf-8"))
        imported = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imported.add(alias.name.split(".")[0])
            elif isinstance(node, ast.ImportFrom) and node.module:
                imported.add(node.module.split(".")[0])
            elif isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
                self.assertNotIn(node.func.id, {"__import__", "eval", "exec", "compile", "open"})
        self.assertEqual(
            imported,
            {"__future__", "hashlib", "json", "re", "threading", "datetime", "decimal"},
        )

    def test_02_nested_amount_and_currency_matrix(self):
        for curr in ("usd", "eur", "inr", "pln", "gbp"):
            for amt in ("0", "0.0", "0.00", "0.000", "0.000000"):
                board = MeterBoard()
                tok = board.decide(
                    make_raw(currency=curr, current_overage={"amount": amt, "currency": curr}),
                    fetched_at=FETCHED,
                    now=FETCHED,
                    http_status=200,
                    lease=make_lease(),
                    request=make_req(),
                )
                self.assertEqual(tok["current_overage"], {"amount": amt, "currency": curr})
                self.assertFalse(tok["authorizes_generation"])
                self.assertFalse(tok["opens_allowance"])
                self.assertFalse(tok["integrated"])
                self.assertEqual(tok["network_calls"], 0)

        bad_amounts = (
            None,
            0,
            0.0,
            1,
            -1,
            True,
            False,
            [],
            {},
            "",
            "00",
            "00.0",
            "000.000",
            "-0",
            "-0.0",
            "-0.00",
            "+0",
            "+0.00",
            "0.",
            ".0",
            "0.0.0",
            "0e0",
            "0E0",
            "0e-5",
            "0.0000000001",
            "-0.0000000001",
            "0.01",
            "-0.01",
            "1",
            "-1",
            "NaN",
            "Infinity",
            "-Infinity",
            "inf",
            "zero",
            "null",
            " 0",
            "0 ",
            "0\n",
            "0\r",
            "0\t",
            "0\x00",
            "\u00a00",
            "０",
            "٠",
            "0_0",
            "0,0",
            "0x0",
        )
        for amt in bad_amounts:
            with self.subTest(amt=amt), self.assertRaises(GuardRefused) as ctx:
                MeterBoard().decide(
                    make_raw(current_overage={"amount": amt, "currency": "usd"}),
                    fetched_at=FETCHED,
                    now=FETCHED,
                    http_status=200,
                    lease=make_lease(),
                    request=make_req(),
                )
            self.assertEqual(ctx.exception.code, "overage")

        bad_currencies = (
            None,
            "",
            "USD",
            "Gbp",
            "EUR",
            "cad",
            "aud",
            "jpy",
            "chf",
            " usd",
            "usd ",
            "usd\n",
            "usd\x00",
            0,
            True,
            False,
            [],
            {},
        )
        for curr in bad_currencies:
            with self.subTest(curr=curr), self.assertRaises(GuardRefused) as ctx:
                MeterBoard().decide(
                    make_raw(current_overage={"amount": "0", "currency": curr}),
                    fetched_at=FETCHED,
                    now=FETCHED,
                    http_status=200,
                    lease=make_lease(),
                    request=make_req(),
                )
            self.assertEqual(ctx.exception.code, "currency")

        # Top-level vs nested currency mismatch
        with self.assertRaises(GuardRefused) as ctx:
            MeterBoard().decide(
                make_raw(currency="gbp", current_overage={"amount": "0", "currency": "usd"}),
                fetched_at=FETCHED,
                now=FETCHED,
                http_status=200,
                lease=make_lease(),
                request=make_req(),
            )
        self.assertEqual(ctx.exception.code, "currency")

    def test_03_malformed_and_duplicate_key_bodies(self):
        bad_bodies = (
            b"",
            b"   ",
            b"{",
            b"}",
            b"[]",
            b"null",
            b"true",
            b"false",
            b"0",
            b'"0"',
            b"\xff\xfe{}",
            b"\xef\xbb\xbf" + make_raw(),
            None,
            "{}",
            make_sub(),
            bytearray(make_raw()),
            memoryview(make_raw()),
            BytesSub(make_raw()),
        )
        for raw in bad_bodies:
            with self.subTest(raw=type(raw).__name__), self.assertRaises(GuardRefused) as ctx:
                MeterBoard().decide(
                    raw,
                    fetched_at=FETCHED,
                    now=FETCHED,
                    http_status=200,
                    lease=make_lease(),
                    request=make_req(),
                )
            self.assertEqual(ctx.exception.code, "malformed_body")

        # Duplicate keys: shadow attack ("5.00" followed by "0")
        base_str = make_raw().decode("utf-8")
        dup_nested_amount = base_str.replace(
            '"amount": "0"',
            '"amount": "5.00", "amount": "0"',
            1,
        ).encode("utf-8")
        dup_outer_overage = base_str.replace(
            '"current_overage": {"amount": "0", "currency": "usd"}',
            '"current_overage": {"amount": "9.99", "currency": "usd"}, '
            '"current_overage": {"amount": "0", "currency": "usd"}',
            1,
        ).encode("utf-8")
        for dup in (dup_nested_amount, dup_outer_overage):
            with self.assertRaises(GuardRefused) as ctx:
                MeterBoard().decide(
                    dup,
                    fetched_at=FETCHED,
                    now=FETCHED,
                    http_status=200,
                    lease=make_lease(),
                    request=make_req(),
                )
            self.assertEqual(ctx.exception.code, "duplicate_key")

    def test_04_freshness_clocks_and_reset_boundaries(self):
        # Exact 60s boundary passes
        tok = MeterBoard().decide(
            make_raw(),
            fetched_at=FETCHED,
            now=FETCHED + timedelta(seconds=60),
            http_status=200,
            lease=make_lease(),
            request=make_req(),
        )
        self.assertEqual(tok["outcome"], "pass_once")

        # 1 microsecond past 60s refuses as stale
        with self.assertRaises(GuardRefused) as ctx:
            MeterBoard().decide(
                make_raw(),
                fetched_at=FETCHED,
                now=FETCHED + timedelta(seconds=60, microseconds=1),
                http_status=200,
                lease=make_lease(),
                request=make_req(),
            )
        self.assertEqual(ctx.exception.code, "stale")

        # 1 microsecond negative clock refuses as inconsistent_clock
        with self.assertRaises(GuardRefused) as ctx:
            MeterBoard().decide(
                make_raw(),
                fetched_at=FETCHED,
                now=FETCHED - timedelta(microseconds=1),
                http_status=200,
                lease=make_lease(),
                request=make_req(),
            )
        self.assertEqual(ctx.exception.code, "inconsistent_clock")

        # Non-UTC timezone offset on fetched_at or now refuses as stale
        plus_one = timezone(timedelta(hours=1))
        for kw in (
            {"fetched_at": FETCHED.astimezone(plus_one)},
            {"now": FETCHED.astimezone(plus_one)},
            {"fetched_at": FETCHED.replace(tzinfo=None)},
            {"now": FETCHED.replace(tzinfo=None)},
        ):
            with self.subTest(kw=kw), self.assertRaises(GuardRefused) as ctx:
                args = dict(
                    fetched_at=FETCHED,
                    now=FETCHED,
                    http_status=200,
                    lease=make_lease(),
                    request=make_req(),
                )
                args.update(kw)
                MeterBoard().decide(make_raw(), **args)
            self.assertEqual(ctx.exception.code, "stale")

        # Reset timestamp at or inside freshness window refuses
        boundary_reset = int(FETCHED.timestamp()) + 60
        with self.assertRaises(GuardRefused) as ctx:
            MeterBoard().decide(
                make_raw(next_character_count_reset_unix=boundary_reset),
                fetched_at=FETCHED,
                now=FETCHED,
                http_status=200,
                lease=make_lease(),
                request=make_req(),
            )
        self.assertEqual(ctx.exception.code, "reset_inconsistent")

    def test_05_concurrency_race_8_threads(self):
        board = MeterBoard()
        barrier = threading.Barrier(8)
        outcomes = []
        lock = threading.Lock()

        def worker():
            barrier.wait()
            try:
                tok = board.decide(
                    make_raw(),
                    fetched_at=FETCHED,
                    now=FETCHED,
                    http_status=200,
                    lease=make_lease(),
                    request=make_req(),
                )
                with lock:
                    outcomes.append(("pass", tok["outcome"]))
            except GuardRefused as exc:
                with lock:
                    outcomes.append(("refuse", exc.code))

        threads = [threading.Thread(target=worker) for _ in range(8)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        passes = [o for o in outcomes if o[0] == "pass"]
        refusals = [o for o in outcomes if o[0] == "refuse"]
        self.assertEqual(len(passes), 1)
        self.assertEqual(len(refusals), 7)
        self.assertTrue(all(code == "retry_or_shared_meter" for _, code in refusals))

    def test_06_adversarial_finding_1_real_34_key_subscription_always_refuses(self):
        """FINDING 1 (BLOCKER): A real raw GET /v1/user/subscription body has 34 top-level keys
        (EAR_REVIEW_J3046.md lines 78-91, desk 7005927729). Passing the raw bytes of a healthy
        34-key subscription body always fails closed with unknown_field."""
        live_shaped = make_sub()
        for key in LIVE_17NOV_34_KEYS:
            live_shaped.setdefault(key, None)
        raw_34 = json.dumps(live_shaped).encode("utf-8")
        with self.assertRaises(GuardRefused) as ctx:
            MeterBoard().decide(
                raw_34,
                fetched_at=FETCHED,
                now=FETCHED,
                http_status=200,
                lease=make_lease(),
                request=make_req(),
            )
        self.assertEqual(ctx.exception.code, "unknown_field")

    def test_07_adversarial_finding_2_active_subscription_next_invoice_always_refuses(self):
        """FINDING 2 (BLOCKER): On an active monthly Creator subscription, next_invoice is a
        scheduled renewal invoice object (e.g. amount_due_cents=2640, subtotal_cents=2200), not
        null (_desk/006/elevenlabs_subscription_snapshot_20261004.json). _invoices() requires
        next_invoice is None, refusing every real active monthly Creator subscription."""
        healthy_next_invoice = {
            "amount_due_cents": 2640,
            "subtotal_cents": 2200,
            "tax_cents": None,
            "discount_percent_off": None,
            "discount_amount_off": None,
            "discounts": [],
            "next_payment_attempt_unix": RESET + 3600,
            "payment_intent_status": None,
            "payment_intent_statusses": [],
        }
        with self.assertRaises(GuardRefused) as ctx:
            MeterBoard().decide(
                make_raw(next_invoice=healthy_next_invoice),
                fetched_at=FETCHED,
                now=FETCHED,
                http_status=200,
                lease=make_lease(),
                request=make_req(),
            )
        self.assertEqual(ctx.exception.code, "invoices")

    def test_08_adversarial_finding_3_consume_accepts_tampered_token_fields(self):
        """FINDING 3 (HIGH): MeterBoard.consume() checks only id, outcome,
        authorizes_generation, and body_sha256, then returns dict(token). Mutating other
        security-critical fields on the token before consume() succeeds and echoes the
        forged fields into the consumed receipt."""
        board = MeterBoard()
        tok = board.decide(
            make_raw(),
            fetched_at=FETCHED,
            now=FETCHED,
            http_status=200,
            lease=make_lease(),
            request=make_req(),
        )
        tampered = dict(tok)
        tampered["integrated"] = True
        tampered["proposal_only"] = False
        tampered["would_allow_posts"] = 99
        tampered["retries"] = 5
        tampered["estimated_credits"] = 999_999
        tampered["cash_gbp"] = "250.00"
        tampered["music_length_ms"] = 600_000
        tampered["current_overage"] = {"amount": "42.00", "currency": "usd"}

        consumed = board.consume(tampered, body_sha256=tok["body_sha256"])
        self.assertTrue(consumed["consumed"])
        self.assertEqual(consumed["would_allow_posts"], 99)
        self.assertEqual(consumed["estimated_credits"], 999_999)
        self.assertEqual(consumed["cash_gbp"], "250.00")
        self.assertEqual(consumed["current_overage"]["amount"], "42.00")

    def test_09_adversarial_finding_4_underestimated_credits_for_180s_music_passes(self):
        """FINDING 4 (HIGH): music_length_ms is fixed at 180_000 ms (180s Music v2, which
        bills ~2,475 credits measured / 2,700 published / 2,970 with 10% margin), but
        _request() accepts estimated_credits as low as 1 (or 684 prompt chars from
        el_guard.characters_in), allowing a pass when remaining capacity is only 1 credit."""
        board = MeterBoard()
        tok = board.decide(
            make_raw(character_count=121_113, character_limit=121_114),
            fetched_at=FETCHED,
            now=FETCHED,
            http_status=200,
            lease=make_lease(observed_character_count=121_113),
            request=make_req(estimated_credits=1),
        )
        self.assertEqual(tok["outcome"], "pass_once")
        self.assertEqual(tok["remaining_credits"], 1)
        self.assertEqual(tok["music_length_ms"], 180_000)

    def test_10_adversarial_finding_5_new_meterboard_instance_bypasses_one_request_latch(self):
        """FINDING 5 (HIGH): MeterBoard state is per-instance in memory only. Instantiating
        a second MeterBoard() in the same process after a refusal or consumed flight
        succeeds with no process-wide or file-backed one-request latch."""
        b1 = MeterBoard()
        with self.assertRaises(GuardRefused):
            b1.decide(
                make_raw(),
                fetched_at=FETCHED,
                now=FETCHED,
                http_status=500,
                lease=make_lease(),
                request=make_req(),
            )
        # Second instance in the same process is not blocked:
        b2 = MeterBoard()
        tok = b2.decide(
            make_raw(),
            fetched_at=FETCHED,
            now=FETCHED,
            http_status=200,
            lease=make_lease(),
            request=make_req(),
        )
        self.assertEqual(tok["outcome"], "pass_once")

    def test_11_adversarial_finding_6_lease_timestamp_paradox_and_non_utc_offset(self):
        """FINDING 6 (MEDIUM):
        (a)POSAL.md step 3 acquires the lock BEFORE step 4's GET /v1/user/subscription,
            so real lock acquired_at < fetched_at, yet _lease() requires acquired == fetched_at
            and refuses acquired_at = fetched_at - 1ms with stale_lease.
        (b) _lease() does not call _utc(acquired), so a non-UTC timezone offset (+01:00)
            equal to the same instant passes."""
        with self.assertRaises(GuardRefused) as ctx:
            MeterBoard().decide(
                make_raw(),
                fetched_at=FETCHED,
                now=FETCHED,
                http_status=200,
                lease=make_lease(acquired_at=FETCHED - timedelta(milliseconds=1)),
                request=make_req(),
            )
        self.assertEqual(ctx.exception.code, "stale_lease")

        plus_one = timezone(timedelta(hours=1))
        tok = MeterBoard().decide(
            make_raw(),
            fetched_at=FETCHED,
            now=FETCHED,
            http_status=200,
            lease=make_lease(acquired_at=FETCHED.astimezone(plus_one)),
            request=make_req(),
        )
        self.assertEqual(tok["outcome"], "pass_once")

    def test_12_adversarial_finding_7_missing_overage_masked_by_extra_or_co_missing_keys(self):
        """FINDING 7 (LOW/MEDIUM): In _keys(), extra keys are checked before missing
        current_overage, and missing == {'current_overage'} uses exact single-element set
        equality, so missing current_overage + missing currency raises malformed_body
        instead of overage."""
        sub = make_sub()
        del sub["current_overage"]
        del sub["currency"]
        with self.assertRaises(GuardRefused) as ctx:
            MeterBoard().decide(
                json.dumps(sub).encode("utf-8"),
                fetched_at=FETCHED,
                now=FETCHED,
                http_status=200,
                lease=make_lease(),
                request=make_req(),
            )
        self.assertEqual(ctx.exception.code, "malformed_body")

    def test_13_subclasses_bare_json_constants_and_consume_before_decide(self):
        # consume() before decide() refuses as retry
        with self.assertRaises(GuardRefused) as ctx:
            MeterBoard().consume({}, body_sha256="0" * 64)
        self.assertEqual(ctx.exception.code, "retry")

        # Subclasses in request/lease
        for bad_req, code in (
            (make_req(holder=StrSub("hos009-score")), "scope"),
            (make_req(attempt=IntSub(1)), "retry"),
            (make_req(endpoint=StrSub("/v1/music")), "endpoint"),
            (make_req(model_id=StrSub("music_v2")), "model"),
            (make_req(music_length_ms=IntSub(180_000)), "duration"),
            (make_req(query=StrSub("output_format=mp3_44100_128")), "malformed_request"),
            (make_req(estimated_credits=IntSub(2_970)), "budget"),
            (make_req(cash_gbp=StrSub("0")), "cash"),
            (DictSub(make_req()), "malformed_request"),
        ):
            with self.subTest(bad_req=code), self.assertRaises(GuardRefused) as ctx:
                MeterBoard().decide(
                    make_raw(),
                    fetched_at=FETCHED,
                    now=FETCHED,
                    http_status=200,
                    lease=make_lease(),
                    request=bad_req,
                )
            self.assertEqual(ctx.exception.code, code)

        # Bare JSON NaN / Infinity inside loads_strict: json.loads has no parse_constant hook,
        # so loads_strict() itself parses bare NaN/Infinity without raising malformed_body!
        raw_nan = b'{"x": NaN}'
        parsed_nan = sbg.loads_strict(raw_nan)
        self.assertTrue("x" in parsed_nan)


if __name__ == "__main__":
    # Remove sys.argv[1] before unittest parses CLI args
    if len(sys.argv) > 1 and Path(sys.argv[1]).exists():
        sys.argv.pop(1)
    unittest.main(verbosity=2)
