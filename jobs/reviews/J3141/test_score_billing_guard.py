"""Synthetic fixtures only. No account access and no production-guard imports."""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import tempfile
import textwrap
import threading
import time
import unittest
from datetime import datetime, timedelta, timezone
from email.utils import formatdate
from pathlib import Path

from score_billing_guard import (
    AUTHORIZES_GENERATION,
    MIN_ESTIMATED_CREDITS,
    PROPOSAL_ONLY,
    REQUIRED_KEYS,
    GuardRefused,
    MeterBoard,
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


class World:
    def __init__(self):
        self.dir = Path(tempfile.mkdtemp(prefix="hos009-guard-"))
        self.pause = self.dir / "TTS_PAUSE"
        self.ledger = self.dir / "ledger.jsonl"
        self.ledger.write_text("", encoding="utf-8")
        self.lock = self.dir / "elevenlabs.lock"
        self.store = self.dir / "hos009-score-single-use.json"
        self.rewrite_lock()

    def rewrite_lock(self, pid=None, started=None):
        moment = started or (datetime.now(timezone.utc) - timedelta(seconds=5))
        self.lock.write_text(
            json.dumps(
                {
                    "pid": os_pid() if pid is None else pid,
                    "host": "holder",
                    "script": "proposal",
                    "started": moment.replace(microsecond=0).isoformat(),
                }
            ),
            encoding="utf-8",
        )

    def date_header(self, seconds_ago=2):
        return formatdate(time.time() - seconds_ago, usegmt=True)


def os_pid() -> int:
    import os

    return os.getpid()


def decide(world=None, body=None, **kwargs):
    world = world or World()
    board = kwargs.pop("board", None) or MeterBoard()
    payload = json.dumps(subscription()).encode() if body is None else body
    args = {
        "http_status": 200,
        "date_header": world.date_header(),
        "request": request(),
        "lock_path": world.lock,
        "pause_path": world.pause,
        "ledger_path": world.ledger,
        "store_path": world.store,
    }
    args.update(kwargs)
    return world, board, board.decide(payload, **args)


class ScoreBillingGuard(unittest.TestCase):
    def test_one_pass_does_not_authorize_generation(self):
        self.assertTrue(PROPOSAL_ONLY)
        self.assertFalse(AUTHORIZES_GENERATION)
        self.assertEqual(meter_units_per_credit(), 1)
        self.assertEqual(MIN_ESTIMATED_CREDITS, 2_970)
        _world, board, token = decide()
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
        self.assertEqual(token["network_calls"], 0)
        self.assertEqual(token["tier"], "creator")
        self.assertEqual(token["status"], "active")
        self.assertEqual(token["billing_period"], "monthly_period")
        spent = board.consume(token, body_sha256=token["body_sha256"])
        self.assertTrue(spent["consumed"])
        self.assertFalse(spent["authorizes_generation"])

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

    def test_same_body_refuses_on_a_new_board_and_a_fresh_process(self):
        world, board, token = decide()
        self.assertEqual(token["outcome"], "pass_once")
        with self.assertRaises(GuardRefused) as caught:
            decide(world, board=MeterBoard())
        self.assertEqual(caught.exception.code, "retry_or_shared_meter")
        child = textwrap.dedent(
            """
            import json, sys
            from pathlib import Path
            sys.path.insert(0, sys.argv[1])
            from test_score_billing_guard import World, decide
            world = World()
            world.store = Path(sys.argv[2])
            try:
                decide(world)
            except Exception as exc:
                print(getattr(exc, "code", type(exc).__name__))
            else:
                print("pass")
            """
        )
        completed = subprocess.run(
            [sys.executable, "-c", child, str(Path(__file__).parent), str(world.store)],
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertEqual(completed.stdout.strip(), "retry_or_shared_meter")
        board.consume(token, body_sha256=token["body_sha256"])

    def test_caller_clock_lease_and_state_are_refused(self):
        now = datetime.now(timezone.utc)
        cases = [
            ({"fetched_at": now}, "caller_asserted_clock"),
            ({"now": now}, "caller_asserted_clock"),
            ({"lease": {"exclusive": True}}, "caller_asserted_lease"),
            ({"pause_file_present": False}, "caller_asserted_state"),
            ({"pending_unposted_credits": 0}, "caller_asserted_state"),
        ]
        for extra, code in cases:
            with self.subTest(extra=sorted(extra)), self.assertRaises(GuardRefused) as caught:
                decide(**extra)
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

    def test_lock_must_be_this_process(self):
        world = World()
        world.rewrite_lock(pid=os_pid() + 1)
        with self.assertRaises(GuardRefused) as caught:
            decide(world)
        self.assertEqual(caught.exception.code, "shared_meter")
        stale = World()
        stale.rewrite_lock(started=datetime.now(timezone.utc) - timedelta(seconds=120))
        with self.assertRaises(GuardRefused) as caught:
            decide(stale)
        self.assertEqual(caught.exception.code, "stale_lease")

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
            decide(world, date_header=world.date_header(seconds_ago=61))
        self.assertEqual(caught.exception.code, "stale")
        with self.assertRaises(GuardRefused) as caught:
            decide(date_header="not-a-date")
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
        with self.assertRaises(GuardRefused) as caught:
            board.decide(
                json.dumps(subscription()).encode(),
                http_status=200,
                date_header=world.date_header(),
                request=request(),
                lock_path=world.lock,
                pause_path=world.pause,
                ledger_path=world.ledger,
                store_path=world.store,
            )
        self.assertEqual(caught.exception.code, "retry_or_shared_meter")
        board.consume(token, body_sha256=token["body_sha256"])
        with self.assertRaises(GuardRefused) as caught:
            board.consume(token, body_sha256=token["body_sha256"])
        self.assertEqual(caught.exception.code, "retry")

    def test_refusal_burns_the_flight(self):
        world = World()
        world.rewrite_lock(pid=os_pid() + 1)
        board = MeterBoard()
        with self.assertRaises(GuardRefused):
            decide(world, board=board)
        world.rewrite_lock()
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

    def test_production_files_are_unchanged_and_still_double_get(self):
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
        source = Path(__file__).with_name("score_billing_guard.py").read_text(encoding="utf-8")
        imports = "\n".join(
            line
            for line in source.splitlines()
            if line.startswith("import ") or line.startswith("from ")
        )
        for banned in ("socket", "urllib", "requests", "subprocess", "http"):
            self.assertNotIn(banned, imports)
        self.assertNotIn("getenv", source)
        self.assertNotIn("os.environ", source)
        self.assertNotIn("EL_GUARD_OFF", source)
        self.assertNotIn("urlopen", source)

    def test_module_hash_pin(self):
        module = Path(__file__).with_name("score_billing_guard.py").read_bytes()
        pinned = Path(__file__).with_name("HASHES.txt").read_text(encoding="utf-8")
        self.assertIn(hashlib.sha256(module).hexdigest(), pinned)


if __name__ == "__main__":
    unittest.main()
