"""Synthetic fixtures only. No account access and no production-guard imports."""

from __future__ import annotations

import ast
import hashlib
import inspect
import json
import os
import socket
import subprocess
import sys
import tempfile
import textwrap
import threading
import time
import unittest
from datetime import datetime, timedelta, timezone
from email.utils import formatdate, parsedate_to_datetime
from pathlib import Path

import score_billing_guard as sbg
from score_billing_adapter import proposed_flight
from score_billing_guard import (
    AUTHORIZES_GENERATION,
    MIN_ESTIMATED_CREDITS,
    PROPOSAL_ONLY,
    REQUIRED_KEYS,
    TARIFF_CURRENT_GUARANTEE,
    GuardRefused,
    MeterBoard,
    TransportReceipt,
    meter_units_per_credit,
)


RESET = 1_893_456_000
ROOT = Path(__file__).resolve().parents[3]


def subscription(**overrides) -> dict:
    payload = {
        "allowed_to_extend_character_limit": False,
        "bfcm_2026_offer": None,
        "billing_period": "monthly_period",
        "can_extend_character_limit": False,
        "can_extend_voice_limit": False,
        "can_use_instant_voice_cloning": False,
        "can_use_professional_voice_cloning": False,
        "cancels_immediately": False,
        "character_count": 0,
        "character_limit": 10_000,
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
        "max_voice_add_edits": 0,
        "next_character_count_reset_unix": RESET,
        "next_invoice": {
            "amount_due_cents": 0,
            "discount_amount_off": None,
            "discount_percent_off": None,
            "discounts": [],
            "next_payment_attempt_unix": RESET,
            "payment_intent_status": None,
            "payment_intent_statusses": [],
            "subtotal_cents": 0,
            "tax_cents": None,
        },
        "open_invoices": [],
        "pending_change": None,
        "professional_voice_limit": 0,
        "professional_voice_slots_used": 0,
        "professional_voice_slots_used_in_workspace": 0,
        "status": "active",
        "tier": "creator",
        "voice_add_edit_counter": 0,
        "voice_limit": 0,
        "voice_slots_used": 0,
    }
    payload.update(overrides)
    return payload


def request(**overrides):
    base = {
        "holder": "hos009-score",
        "attempt": 1,
        "endpoint": "/v1/music",
        "model_id": "music_v2",
        "force_instrumental": True,
        "music_length_ms": 180_000,
        "query": "output_format=mp3_44100_128",
        "estimated_credits": MIN_ESTIMATED_CREDITS,
        "cash_gbp": "0",
    }
    base.update(overrides)
    return base


def prepare(root: Path) -> None:
    """Create the pinned layout. Does not take the recorder lock or delete a store."""
    (root / "locks").mkdir(parents=True, exist_ok=True)
    eleven = root / "elevenlabs"
    eleven.mkdir(parents=True, exist_ok=True)
    ledger = eleven / "ledger.jsonl"
    if not ledger.exists():
        ledger.write_text("", encoding="utf-8")


def date_header(seconds_ago=0):
    return formatdate(time.time() - seconds_ago, usegmt=True)


class World:
    def __init__(self):
        sbg.release_test_holder()
        self.root = Path(tempfile.mkdtemp(prefix="hos009-guard-"))
        prepare(self.root)
        self.pause = self.root / "elevenlabs" / "TTS_PAUSE"
        self.ledger = self.root / "elevenlabs" / "ledger.jsonl"
        self.store = self.root / "elevenlabs" / "hos009-score-single-use.json"
        self.lock = self.root / "locks" / "elevenlabs.lock"
        sbg.bind_desk(self.root)
        sbg.hold_recorder()

    def rewrite_held(self, started: str, pid=None, host=None, script=None):
        payload = {
            "pid": os.getpid() if pid is None else pid,
            "host": socket.gethostname() if host is None else host,
            "script": script or sbg.RECORDER_SCRIPT,
            "started": started,
        }
        raw = json.dumps(payload).encode("utf-8")
        os.lseek(sbg._held_fd, 0, os.SEEK_SET)
        os.ftruncate(sbg._held_fd, 0)
        os.write(sbg._held_fd, raw)
        sbg._held_started = started


def seal(world, body, header):
    calls = {"get": 0}

    def fetch():
        calls["get"] += 1
        return (200, {"Date": header}, body)

    receipt = sbg.read_subscription(fetch)
    return receipt, calls["get"]


def decide(world=None, body=None, header=None, **kwargs):
    world = world or World()
    board = kwargs.pop("board", None) or MeterBoard()
    payload = json.dumps(subscription()).encode() if body is None else body
    if "receipt" in kwargs:
        receipt = kwargs.pop("receipt")
    else:
        receipt, _gets = seal(world, payload, header or date_header())
    asked = kwargs.pop("request", None) or request()
    return world, board, board.decide(receipt, request=asked, **kwargs)


class CountingTransport:
    def __init__(self, body: bytes, header: str, status: int = 200):
        self.body = body
        self.header = header
        self.status = status
        self.gets = 0
        self.posts = 0

    def get_subscription(self):
        self.gets += 1
        return (self.status, {"Date": self.header}, self.body)

    def post_music(self, token):
        self.posts += 1
        if token.get("consumed") is not True:
            raise GuardRefused("retry")


class ScoreBillingGuard(unittest.TestCase):
    def test_one_pass_does_not_authorize_generation(self):
        self.assertTrue(PROPOSAL_ONLY)
        self.assertFalse(AUTHORIZES_GENERATION)
        self.assertFalse(TARIFF_CURRENT_GUARANTEE)
        self.assertEqual(meter_units_per_credit(), 1)
        self.assertEqual(MIN_ESTIMATED_CREDITS, 2_970)
        world, board, token = decide()
        self.assertEqual(token["outcome"], "pass_once")
        self.assertEqual(token["current_overage"], {"amount": "0", "currency": "usd"})
        self.assertEqual(token["estimated_credits"], 2_970)
        self.assertEqual(token["floor_credits"], 2_970)
        self.assertEqual(token["measured_180s_credits"], 2_475)
        self.assertEqual(token["meter_units_per_credit"], 1)
        self.assertEqual(token["remaining_meter_units"], 10_000)
        self.assertFalse(token["authorizes_generation"])
        self.assertFalse(token["opens_allowance"])
        self.assertFalse(token["integrated"])
        self.assertFalse(token["tariff_current_guarantee"])
        self.assertEqual(token["network_calls"], 0)
        self.assertEqual(token["tier"], "creator")
        self.assertEqual(token["status"], "active")
        self.assertEqual(token["billing_period"], "monthly_period")
        self.assertTrue(sbg.recorder_held())
        spent = board.consume(token, body_sha256=token["body_sha256"])
        self.assertTrue(spent["consumed"])
        self.assertFalse(spent["authorizes_generation"])
        self.assertTrue(sbg.recorder_held())
        os.fstat(sbg._held_fd)
        self.assertTrue(world.store.is_file())

    def test_documented_shape_passes_and_an_added_key_fails(self):
        shape = json.loads(
            (Path(__file__).with_name("subscription_shape.json")).read_text(encoding="utf-8")
        )
        self.assertEqual(set(shape["keys"]), set(REQUIRED_KEYS))
        self.assertEqual(len(REQUIRED_KEYS), 34)
        _world, _board, token = decide()
        self.assertEqual(token["outcome"], "pass_once")
        extra = subscription(voice_extra=1)
        world = World()
        with self.assertRaises(GuardRefused) as caught:
            decide(world, body=json.dumps(extra).encode())
        self.assertEqual(caught.exception.code, "unknown_field")
        nested = subscription(bfcm_2026_offer={"offer": True})
        with self.assertRaises(GuardRefused) as caught:
            decide(body=json.dumps(nested).encode())
        self.assertEqual(caught.exception.code, "unknown_field")

    def test_scheduled_renewal_passes_and_collection_refuses(self):
        _world, _board, token = decide()
        self.assertEqual(token["outcome"], "pass_once")
        absent = subscription(next_invoice=None)
        _world, _board, token = decide(body=json.dumps(absent).encode())
        self.assertEqual(token["outcome"], "pass_once")
        invoice = subscription()["next_invoice"]
        invoice["payment_intent_status"] = "processing"
        with self.assertRaises(GuardRefused) as caught:
            decide(body=json.dumps(subscription(next_invoice=invoice)).encode())
        self.assertEqual(caught.exception.code, "invoices")
        with self.assertRaises(GuardRefused) as caught:
            decide(body=json.dumps(subscription(next_invoice={})).encode())
        self.assertEqual(caught.exception.code, "invoices")
        with self.assertRaises(GuardRefused) as caught:
            decide(body=json.dumps(subscription(has_open_invoices=True)).encode())
        self.assertEqual(caught.exception.code, "invoices")

    def test_declared_one_credit_and_under_floor_refuse(self):
        for credits in (1, 684, 2_475, 2_969, 3_001, 0, -1, True, "2970"):
            with self.subTest(credits=credits), self.assertRaises(GuardRefused) as caught:
                decide(request=request(estimated_credits=credits))
            self.assertEqual(caught.exception.code, "budget")
        _world, _board, token = decide(request=request(estimated_credits=2_970))
        self.assertEqual(token["estimated_credits"], 2_970)
        _world, _board, token = decide(request=request(estimated_credits=3_000))
        self.assertEqual(token["estimated_credits"], 3_000)
        short = subscription(character_count=7_031, character_limit=10_000)
        with self.assertRaises(GuardRefused) as caught:
            decide(body=json.dumps(short).encode(), request=request(estimated_credits=2_970))
        self.assertEqual(caught.exception.code, "insufficient_capacity")

    def test_same_body_refuses_on_a_new_board_and_after_restart(self):
        world, board, token = decide()
        self.assertEqual(token["outcome"], "pass_once")
        with self.assertRaises(GuardRefused) as caught:
            decide(world, board=MeterBoard())
        self.assertEqual(caught.exception.code, "retry_or_shared_meter")
        board.consume(token, body_sha256=token["body_sha256"])
        root = Path(tempfile.mkdtemp(prefix="hos009-restart-"))
        prepare(root)
        script = textwrap.dedent(
            """
            import json, sys, time
            from email.utils import formatdate
            from pathlib import Path
            sys.path.insert(0, sys.argv[1])
            import score_billing_guard as guard
            from test_score_billing_guard import prepare, request, subscription
            root = Path(sys.argv[2])
            role = sys.argv[3]
            prepare(root)
            guard.release_test_holder()
            guard.bind_desk(root)
            guard.hold_recorder()
            body = json.dumps(subscription()).encode()
            header = formatdate(time.time(), usegmt=True)
            receipt = guard.read_subscription(lambda: (200, {"Date": header}, body))
            board = guard.MeterBoard()
            try:
                token = board.decide(receipt, request=request())
            except guard.GuardRefused as exc:
                print(exc.code)
            else:
                print(token["outcome"])
            """
        )
        first = subprocess.run(
            [sys.executable, "-c", script, str(Path(__file__).parent), str(root), "first"],
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(first.returncode, 0, first.stderr)
        self.assertEqual(first.stdout.strip(), "pass_once")
        second = subprocess.run(
            [sys.executable, "-c", script, str(Path(__file__).parent), str(root), "second"],
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(second.returncode, 0, second.stderr)
        self.assertEqual(second.stdout.strip(), "retry_or_shared_meter")

    def test_two_processes_cannot_both_hold_the_recorder(self):
        world = World()
        ready = world.root / "ready"
        script = textwrap.dedent(
            """
            import sys, time
            from pathlib import Path
            sys.path.insert(0, sys.argv[1])
            import score_billing_guard as guard
            root = Path(sys.argv[2])
            ready = Path(sys.argv[3])
            guard.bind_desk(root)
            try:
                guard.hold_recorder()
            except guard.GuardRefused as exc:
                ready.write_text(exc.code, encoding="utf-8")
            else:
                ready.write_text("acquired", encoding="utf-8")
            """
        )
        completed = subprocess.run(
            [sys.executable, "-c", script, str(Path(__file__).parent), str(world.root), str(ready)],
            check=False,
            capture_output=True,
            text=True,
            timeout=15,
        )
        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertEqual(ready.read_text(encoding="utf-8"), "shared_meter")
        self.assertTrue(sbg.recorder_held())

    def test_caller_clock_lease_and_state_are_refused(self):
        now = datetime.now(timezone.utc)
        world = World()
        cases = [
            ({"fetched_at": now}, "caller_asserted_clock"),
            ({"now": now}, "caller_asserted_clock"),
            ({"lease": {"exclusive": True}}, "caller_asserted_lease"),
            ({"pause_file_present": False}, "caller_asserted_state"),
            ({"pending_unposted_credits": 0}, "caller_asserted_state"),
            ({"store_path": world.store}, "caller_asserted_state"),
            ({"lock_path": world.lock}, "caller_asserted_state"),
            ({"pause_path": world.pause}, "caller_asserted_state"),
            ({"ledger_path": world.ledger}, "caller_asserted_state"),
            ({"date_header": date_header()}, "untrusted_receipt"),
            ({"http_status": 200}, "untrusted_receipt"),
            ({"raw": b"{}"}, "untrusted_receipt"),
        ]
        for extra, code in cases:
            with self.subTest(extra=sorted(extra)), self.assertRaises(GuardRefused) as caught:
                decide(world, **extra)
            self.assertEqual(caught.exception.code, code)

    def test_pause_file_and_pending_ledger_are_read_not_declared(self):
        world = World()
        world.pause.write_text("pause", encoding="utf-8")
        with self.assertRaises(GuardRefused) as caught:
            decide(world)
        self.assertEqual(caught.exception.code, "paused")
        world = World()
        world.ledger.write_text("{}\n", encoding="utf-8")
        with self.assertRaises(GuardRefused) as caught:
            decide(world)
        self.assertEqual(caught.exception.code, "pending_spend")
        world = World()
        later = (datetime.now(timezone.utc) + timedelta(seconds=30)).isoformat()
        world.ledger.write_text(
            json.dumps({"status": 200, "time": later}) + "\n",
            encoding="utf-8",
        )
        with self.assertRaises(GuardRefused) as caught:
            decide(world)
        self.assertEqual(caught.exception.code, "pending_spend")

    def test_same_second_and_failed_ledger_lines_refuse_unless_reconciled(self):
        world = World()
        header = date_header()
        fetched = parsedate_to_datetime(header).astimezone(timezone.utc).replace(microsecond=0)
        world.rewrite_held((fetched - timedelta(seconds=5)).isoformat())
        world.ledger.write_text(
            json.dumps({"status": 200, "time": fetched.isoformat()}) + "\n",
            encoding="utf-8",
        )
        with self.assertRaises(GuardRefused) as caught:
            decide(world, header=header)
        self.assertEqual(caught.exception.code, "pending_spend")

        world = World()
        past = (datetime.now(timezone.utc) - timedelta(hours=1)).replace(microsecond=0).isoformat()
        world.ledger.write_text(
            json.dumps({"status": 500, "time": past}) + "\n",
            encoding="utf-8",
        )
        with self.assertRaises(GuardRefused) as caught:
            decide(world)
        self.assertEqual(caught.exception.code, "pending_spend")

        world = World()
        world.ledger.write_text(
            json.dumps({"status": "504", "time": past}) + "\n",
            encoding="utf-8",
        )
        with self.assertRaises(GuardRefused) as caught:
            decide(world)
        self.assertEqual(caught.exception.code, "pending_spend")

        world = World()
        world.ledger.write_text(
            json.dumps(
                {
                    "status": 500,
                    "time": past,
                    "reconciled": True,
                    "reconciliation": "synthetic-fixture",
                }
            )
            + "\n",
            encoding="utf-8",
        )
        _world, _board, token = decide(world)
        self.assertEqual(token["outcome"], "pass_once")

        world = World()
        header = date_header()
        fetched = parsedate_to_datetime(header).astimezone(timezone.utc).replace(microsecond=0)
        world.rewrite_held((fetched - timedelta(seconds=5)).isoformat())
        world.ledger.write_text(
            json.dumps(
                {
                    "status": 500,
                    "time": fetched.isoformat(),
                    "reconciled": True,
                    "reconciliation": "synthetic-fixture",
                }
            )
            + "\n",
            encoding="utf-8",
        )
        with self.assertRaises(GuardRefused) as caught:
            decide(world, header=header)
        self.assertEqual(caught.exception.code, "pending_spend")

    def test_lock_must_be_this_process_and_is_not_flocked_by_the_check(self):
        world = World()
        started = (datetime.now(timezone.utc) - timedelta(seconds=5)).replace(microsecond=0).isoformat()
        world.rewrite_held(started, pid=os.getpid() + 1)
        with self.assertRaises(GuardRefused) as caught:
            decide(world)
        self.assertEqual(caught.exception.code, "shared_meter")

        stale = World()
        old = (datetime.now(timezone.utc) - timedelta(seconds=120)).replace(microsecond=0).isoformat()
        stale.rewrite_held(old)
        with self.assertRaises(GuardRefused) as caught:
            decide(stale)
        self.assertEqual(caught.exception.code, "stale_lease")

        held = World()
        # A pid file written without the open descriptor is not ownership.
        sbg.release_test_holder()
        held.lock.write_text(
            json.dumps(
                {
                    "pid": os.getpid(),
                    "host": socket.gethostname(),
                    "script": sbg.RECORDER_SCRIPT,
                    "started": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
                }
            ),
            encoding="utf-8",
        )
        with self.assertRaises(GuardRefused) as caught:
            decide(held)
        self.assertEqual(caught.exception.code, "shared_meter")

        owned = World()
        import fcntl

        fcntl.flock(sbg._held_fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        _world, board, token = decide(owned)
        self.assertEqual(token["outcome"], "pass_once")
        self.assertTrue(sbg.recorder_held())
        board.consume(token, body_sha256=token["body_sha256"])
        os.fstat(sbg._held_fd)
        observe = ast.parse(inspect.getsource(sbg._observe_lock))
        called = {
            node.func.attr
            for node in ast.walk(observe)
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)
        }
        self.assertNotIn("flock", called)
        self.assertNotIn("unlink", called)

    def test_receipt_substitution_refuses(self):
        with self.assertRaises(GuardRefused) as caught:
            TransportReceipt(200, date_header(), b"{}")
        self.assertEqual(caught.exception.code, "untrusted_receipt")

        class Frozen:
            def __init__(self, status, date_value, raw):
                self.status = status
                self.date_value = date_value
                self.raw = raw

        world = World()
        body_a = json.dumps(subscription()).encode()
        body_b = json.dumps(subscription(character_count=10)).encode()
        header = date_header()
        receipt, gets = seal(world, body_a, header)
        self.assertEqual(gets, 1)
        stand_in = Frozen(200, header, body_b)
        board = MeterBoard()
        with self.assertRaises(GuardRefused) as caught:
            board.decide(stand_in, request=request())
        self.assertEqual(caught.exception.code, "untrusted_receipt")
        object.__setattr__(receipt, "raw", body_b)
        with self.assertRaises(GuardRefused) as caught:
            board.decide(receipt, request=request())
        self.assertEqual(caught.exception.code, "untrusted_receipt")
        self.assertFalse(board.used)

    def test_consume_rechecks_freshness_pause_and_ledger(self):
        world, board, token = decide()
        real_now = sbg._now
        sbg._now = lambda: real_now() + timedelta(seconds=90)
        try:
            with self.assertRaises(GuardRefused) as caught:
                board.consume(token, body_sha256=token["body_sha256"])
            self.assertEqual(caught.exception.code, "stale")
        finally:
            sbg._now = real_now

        world, board, token = decide()
        world.pause.write_text("pause", encoding="utf-8")
        with self.assertRaises(GuardRefused) as caught:
            board.consume(token, body_sha256=token["body_sha256"])
        self.assertEqual(caught.exception.code, "paused")

        world, board, token = decide()
        later = (datetime.now(timezone.utc) + timedelta(seconds=30)).isoformat()
        world.ledger.write_text(
            json.dumps({"status": 200, "time": later}) + "\n",
            encoding="utf-8",
        )
        with self.assertRaises(GuardRefused) as caught:
            board.consume(token, body_sha256=token["body_sha256"])
        self.assertEqual(caught.exception.code, "pending_spend")

    def test_proposed_flight_uses_one_get_and_at_most_one_post(self):
        world = World()
        body = json.dumps(subscription()).encode()
        transport = CountingTransport(body, date_header())
        board = MeterBoard()
        spent = proposed_flight(board, transport, request())
        self.assertEqual(transport.gets, 1)
        self.assertEqual(transport.posts, 1)
        self.assertTrue(spent["consumed"])
        self.assertFalse(spent["authorizes_generation"])
        self.assertTrue(sbg.recorder_held())
        again = CountingTransport(body, date_header())
        with self.assertRaises(GuardRefused) as caught:
            proposed_flight(board, again, request())
        self.assertEqual(caught.exception.code, "retry_or_shared_meter")
        self.assertEqual(again.gets, 0)
        self.assertEqual(again.posts, 0)

        refused = World()
        refused.pause.write_text("pause", encoding="utf-8")
        transport = CountingTransport(body, date_header())
        with self.assertRaises(GuardRefused) as caught:
            proposed_flight(MeterBoard(), transport, request())
        self.assertEqual(caught.exception.code, "paused")
        self.assertEqual(transport.gets, 1)
        self.assertEqual(transport.posts, 0)
        self.assertIs(world.root.exists(), True)

    def test_consume_rejects_tampered_fields(self):
        mutations = (
            ("estimated_credits", 1),
            ("cash_gbp", "250.00"),
            ("would_allow_posts", 99),
            ("retries", 5),
            ("integrated", True),
            ("proposal_only", False),
            ("music_length_ms", 600_000),
            ("current_overage", {"amount": "42.00", "currency": "usd"}),
            ("authorizes_generation", True),
        )
        for key, value in mutations:
            _world, board, token = decide()
            forged = dict(token)
            forged[key] = value
            with self.subTest(key=key), self.assertRaises(GuardRefused) as caught:
                board.consume(forged, body_sha256=token["body_sha256"])
            self.assertEqual(caught.exception.code, "inconsistent_meter")
            with self.assertRaises(GuardRefused) as caught:
                board.consume(token, body_sha256=token["body_sha256"])
            self.assertEqual(caught.exception.code, "retry")
        _world, board, token = decide()
        with self.assertRaises(GuardRefused) as caught:
            board.consume(token, body_sha256="0" * 64)
        self.assertEqual(caught.exception.code, "inconsistent_meter")

    def test_parser_provenance_and_overage_precedence(self):
        with self.assertRaises(GuardRefused) as caught:
            decide(body=b'{"tier": NaN}')
        self.assertEqual(caught.exception.code, "malformed_body")
        missing = subscription()
        del missing["current_overage"]
        del missing["currency"]
        with self.assertRaises(GuardRefused) as caught:
            decide(body=json.dumps(missing).encode())
        self.assertEqual(caught.exception.code, "overage")
        flat = subscription()
        del flat["current_overage"]
        flat["current_overage_amount"] = "0"
        with self.assertRaises(GuardRefused) as caught:
            decide(body=json.dumps(flat).encode())
        self.assertEqual(caught.exception.code, "overage")
        text = json.dumps(subscription())
        doubled = text.replace('"tier": "creator"', '"tier": "creator", "tier": "creator"', 1)
        with self.assertRaises(GuardRefused) as caught:
            decide(body=doubled.encode())
        self.assertEqual(caught.exception.code, "duplicate_key")

    def test_canonical_zero_and_clock_window(self):
        for amount in ("0", "0.0", "0.00", "0.000"):
            body = json.dumps(
                subscription(currency="gbp", current_overage={"amount": amount, "currency": "gbp"})
            ).encode()
            _world, _board, token = decide(body=body)
            self.assertEqual(token["current_overage"]["amount"], amount)
        world = World()
        with self.assertRaises(GuardRefused) as caught:
            decide(world, header=date_header(seconds_ago=61))
        self.assertEqual(caught.exception.code, "stale")
        with self.assertRaises(GuardRefused) as caught:
            decide(world)
        self.assertEqual(caught.exception.code, "retry_or_shared_meter")
        self.assertTrue(world.store.is_file())
        with self.assertRaises(GuardRefused) as caught:
            decide(header="not-a-date")
        self.assertEqual(caught.exception.code, "stale")

    def test_request_shape_and_no_second_decide(self):
        refusals = [
            (dict(attempt=2), "retry"),
            (dict(endpoint="/v1/sound-generation"), "endpoint"),
            (dict(model_id="music_v1"), "model"),
            (dict(force_instrumental=False), "not_instrumental"),
            (dict(music_length_ms=179_000), "duration"),
            (dict(holder="other-score"), "scope"),
            (dict(cash_gbp="0.00"), "cash"),
        ]
        for overrides, code in refusals:
            with self.subTest(overrides=overrides), self.assertRaises(GuardRefused) as caught:
                decide(request=request(**overrides))
            self.assertEqual(caught.exception.code, code)
        world, board, token = decide()
        body = json.dumps(subscription()).encode()
        header = date_header()
        receipt, _gets = seal(world, body, header)
        with self.assertRaises(GuardRefused) as caught:
            board.decide(receipt, request=request())
        self.assertEqual(caught.exception.code, "retry_or_shared_meter")
        board.consume(token, body_sha256=token["body_sha256"])
        with self.assertRaises(GuardRefused) as caught:
            board.consume(token, body_sha256=token["body_sha256"])
        self.assertEqual(caught.exception.code, "retry")

    def test_refusal_burns_the_flight(self):
        world = World()
        started = (datetime.now(timezone.utc) - timedelta(seconds=5)).replace(microsecond=0).isoformat()
        world.rewrite_held(started, pid=os.getpid() + 1)
        board = MeterBoard()
        with self.assertRaises(GuardRefused):
            decide(world, board=board)
        world.rewrite_held(started)
        with self.assertRaises(GuardRefused) as caught:
            decide(world, board=board)
        self.assertEqual(caught.exception.code, "retry_or_shared_meter")

    def test_transport_argument_is_refused(self):
        with self.assertRaises(GuardRefused) as caught:
            decide(transport=object())
        self.assertEqual(caught.exception.code, "network_forbidden")

    def test_concurrent_callers_get_one_decision(self):
        world = World()
        board = MeterBoard()
        barrier = threading.Barrier(2)
        results = []

        def run():
            barrier.wait()
            try:
                _world, _board, token = decide(world, board=board)
                results.append(("pass", token["outcome"]))
            except GuardRefused as exc:
                results.append(("refuse", exc.code))

        threads = [threading.Thread(target=run) for _ in range(2)]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
        self.assertEqual(sorted(kind for kind, _value in results), ["pass", "refuse"])
        self.assertIn("retry_or_shared_meter", [value for kind, value in results if kind == "refuse"])

    def test_live_desk_and_production_files_stay_untouched(self):
        live = Path.home() / "_desk"
        if live.is_dir():
            with self.assertRaises(GuardRefused) as caught:
                sbg.bind_desk(live)
            self.assertEqual(caught.exception.code, "live_desk_forbidden")
        for relative in (
            "04_Audio/tools/el_guard.py",
            "04_Audio/tools/generate_music_bed.py",
            "04_Audio/tools/el_client.py",
        ):
            text = (ROOT / relative).read_text(encoding="utf-8")
            self.assertNotIn("score_billing_guard", text)
        client = (ROOT / "04_Audio/tools/el_client.py").read_text(encoding="utf-8")
        self.assertIn('request("GET", "/v1/user/subscription"', client)
        proposal = Path(__file__).with_name("PROPOSAL.md").read_text(encoding="utf-8")
        self.assertIn("does not issue a second GET", proposal)
        design = Path(__file__).with_name("INTEGRATION_DIFF.md").read_text(encoding="utf-8")
        self.assertIn("not applied", design.lower())
        self.assertIn("generate_music_bed", design)
        source = Path(__file__).with_name("score_billing_guard.py").read_text(encoding="utf-8")
        imports = "\n".join(
            line
            for line in source.splitlines()
            if line.startswith("import ") or line.startswith("from ")
        )
        for banned in ("urllib", "requests", "subprocess", "http"):
            self.assertNotIn(banned, imports)
        self.assertNotIn("getenv", source)
        self.assertNotIn("os.environ", source)
        self.assertNotIn("EL_GUARD_OFF", source)
        self.assertNotIn("urlopen", source)
        self.assertNotIn("socket.socket", source)

    def test_module_hash_pin(self):
        module = Path(__file__).with_name("score_billing_guard.py").read_bytes()
        pinned = Path(__file__).with_name("HASHES.txt").read_text(encoding="utf-8")
        self.assertIn(hashlib.sha256(module).hexdigest(), pinned)


if __name__ == "__main__":
    unittest.main()
