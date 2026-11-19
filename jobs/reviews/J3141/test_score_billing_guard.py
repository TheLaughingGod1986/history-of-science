"""Synthetic fixtures only. No account access and no production-guard imports."""

from __future__ import annotations

import hashlib
import json
import threading
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

from score_billing_guard import (
    AUTHORIZES_GENERATION,
    GuardRefused,
    MeterBoard,
    PROPOSAL_ONLY,
)


FETCHED = datetime(2026, 11, 19, 15, 0, tzinfo=timezone.utc)
RESET = 1_893_456_000  # well after the freshness window


def subscription(**overrides) -> dict:
    payload = {
        "tier": "creator",
        "status": "active",
        "billing_period": "monthly_period",
        "character_count": 118_114,
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
    payload.update(overrides)
    return payload


def raw_body(**overrides) -> bytes:
    return json.dumps(subscription(**overrides)).encode()


def lease(**overrides):
    base = {
        "exclusive": True,
        "holder": "hos009-score",
        "peers": 0,
        "hosts": ["hos009-score"],
        "observed_character_count": 118_114,
        "acquired_at": FETCHED,
    }
    base.update(overrides)
    return base


def request(**overrides):
    base = {
        "holder": "hos009-score",
        "attempt": 1,
        "endpoint": "/v1/music",
        "model_id": "music_v2",
        "force_instrumental": True,
        "music_length_ms": 180_000,
        "query": "output_format=mp3_44100_128",
        "estimated_credits": 3_000,
        "cash_gbp": "0",
    }
    base.update(overrides)
    return base


_MISSING = object()


def decide(board=None, body=_MISSING, **kwargs):
    board = board or MeterBoard()
    args = {
        "fetched_at": FETCHED,
        "now": FETCHED,
        "http_status": 200,
        "lease": lease(),
        "request": request(),
    }
    args.update(kwargs)
    payload = raw_body() if body is _MISSING else body
    return board, board.decide(payload, **args)


class ScoreBillingGuard(unittest.TestCase):
    def test_nested_zero_is_one_pass_and_does_not_authorize_generation(self):
        self.assertTrue(PROPOSAL_ONLY)
        self.assertFalse(AUTHORIZES_GENERATION)
        board, token = decide()
        self.assertEqual(token["outcome"], "pass_once")
        self.assertEqual(token["current_overage"], {"amount": "0", "currency": "usd"})
        self.assertEqual(token["estimated_credits"], 3_000)
        self.assertEqual(token["cash_gbp"], "0")
        self.assertEqual(token["music_length_ms"], 180_000)
        self.assertEqual(token["would_allow_posts"], 1)
        self.assertEqual(token["retries"], 0)
        self.assertEqual(token["network_calls"], 0)
        self.assertFalse(token["authorizes_generation"])
        self.assertFalse(token["opens_allowance"])
        self.assertFalse(token["integrated"])
        self.assertEqual(token["remaining_credits"], 3_000)
        spent = board.consume(token, body_sha256=token["body_sha256"])
        self.assertTrue(spent["consumed"])
        self.assertFalse(spent["authorizes_generation"])
        self.assertEqual(spent["network_calls"], 0)

    def test_canonical_zero_strings_are_retained(self):
        for amount in ("0", "0.0", "0.00", "0.000"):
            body = json.dumps(
                subscription(
                    currency="gbp",
                    current_overage={"amount": amount, "currency": "gbp"},
                )
            ).encode()
            _board, token = decide(body=body)
            self.assertEqual(token["current_overage"]["amount"], amount)
            self.assertEqual(token["current_overage"]["currency"], "gbp")

    def test_amount_and_currency_refusals(self):
        cases = []
        for amount in (
            None, 0, True, False, [], {}, "", "00", "000.000", "zero", "NaN",
            "Infinity", "-0", "-0.00", "-1", "0.01", 1, -1, 0.0, " 0", "0 ", "0e0",
        ):
            cases.append(({"amount": amount, "currency": "usd"}, "overage"))
        for currency in (None, "", "USD", "xxx", 0, [], {}):
            cases.append(({"amount": "0", "currency": currency}, "currency"))
        cases.append(({"amount": "0"}, "overage"))
        cases.append(({"currency": "usd"}, "overage"))
        cases.append((None, "overage"))
        cases.append(([], "overage"))
        cases.append(({"amount": "0", "currency": "usd", "extra": 1}, "overage"))
        for nested, code in cases:
            body = raw_body(current_overage=nested, currency="usd")
            with self.subTest(nested=nested), self.assertRaises(GuardRefused) as caught:
                decide(body=body)
            self.assertEqual(caught.exception.code, code)

    def test_missing_flat_and_unknown_shapes(self):
        missing = subscription()
        del missing["current_overage"]
        with self.assertRaises(GuardRefused) as caught:
            decide(body=json.dumps(missing).encode())
        self.assertEqual(caught.exception.code, "overage")

        flat = subscription()
        del flat["current_overage"]
        flat["current_overage_amount"] = "0"
        flat["current_overage_currency"] = "usd"
        with self.assertRaises(GuardRefused) as caught:
            decide(body=json.dumps(flat).encode())
        self.assertEqual(caught.exception.code, "overage")

        both = subscription()
        both["current_overage_amount"] = "0"
        with self.assertRaises(GuardRefused) as caught:
            decide(body=json.dumps(both).encode())
        self.assertEqual(caught.exception.code, "overage")

        extra = subscription()
        extra["voice_limit"] = 0
        with self.assertRaises(GuardRefused) as caught:
            decide(body=json.dumps(extra).encode())
        self.assertEqual(caught.exception.code, "unknown_field")

        for bad in (b"", b"{", b"[]", b"null", b'"0"', None, "{}"):
            with self.subTest(bad=bad), self.assertRaises(GuardRefused) as caught:
                decide(body=bad)
            self.assertEqual(caught.exception.code, "malformed_body")

    def test_duplicate_keys_refuse(self):
        text = json.dumps(subscription())
        outer = text.replace('"tier": "creator"', '"tier": "creator", "tier": "creator"', 1)
        nested = text.replace(
            '"amount": "0"', '"amount": "0", "amount": "0"', 1
        )
        for raw in (outer.encode(), nested.encode()):
            with self.subTest(raw=raw[:80]), self.assertRaises(GuardRefused) as caught:
                decide(body=raw)
            self.assertEqual(caught.exception.code, "duplicate_key")

    def test_entitlement_extensions_and_invoices(self):
        refusals = [
            (dict(tier="pro"), "unknown_entitlement"),
            (dict(status="past_due"), "unknown_entitlement"),
            (dict(billing_period="annual"), "unknown_entitlement"),
            (dict(max_credit_limit_extension=1), "extensions"),
            (dict(max_character_limit_extension=1), "extensions"),
            (dict(can_extend_character_limit=True), "extensions"),
            (dict(allowed_to_extend_character_limit=True), "extensions"),
            (dict(has_open_invoices=True), "invoices"),
            (dict(open_invoices=[{}]), "invoices"),
            (dict(next_invoice={}), "invoices"),
            (dict(pending_change={}), "pending_change"),
        ]
        for overrides, code in refusals:
            with self.subTest(overrides=overrides), self.assertRaises(GuardRefused) as caught:
                decide(body=raw_body(**overrides))
            self.assertEqual(caught.exception.code, code)

    def test_stale_and_inconsistent_clocks(self):
        with self.assertRaises(GuardRefused) as caught:
            decide(now=FETCHED + timedelta(seconds=61))
        self.assertEqual(caught.exception.code, "stale")
        _board, token = decide(now=FETCHED + timedelta(seconds=60))
        self.assertEqual(token["outcome"], "pass_once")
        with self.assertRaises(GuardRefused) as caught:
            decide(now=FETCHED - timedelta(seconds=1))
        self.assertEqual(caught.exception.code, "inconsistent_clock")
        naive = FETCHED.replace(tzinfo=None)
        with self.assertRaises(GuardRefused) as caught:
            decide(fetched_at=naive)
        self.assertEqual(caught.exception.code, "stale")
        with self.assertRaises(GuardRefused) as caught:
            decide(http_status=500)
        self.assertEqual(caught.exception.code, "http_status")
        with self.assertRaises(GuardRefused) as caught:
            decide(http_status=True)
        self.assertEqual(caught.exception.code, "http_status")

    def test_shared_meter_and_moved_count(self):
        cases = [
            (dict(peers=1), "shared_meter"),
            (dict(exclusive=False), "shared_meter"),
            (dict(hosts=["hos009-score", "other-flight"]), "shared_meter"),
            (dict(hosts=[]), "shared_meter"),
            (dict(acquired_at=FETCHED - timedelta(seconds=1)), "stale_lease"),
            (dict(observed_character_count=41_250), "inconsistent_meter"),
            (dict(holder="other-score"), "shared_meter"),
        ]
        for overrides, code in cases:
            with self.subTest(overrides=overrides), self.assertRaises(GuardRefused) as caught:
                decide(lease=lease(**overrides))
            self.assertEqual(caught.exception.code, code)

    def test_budget_edges(self):
        with self.assertRaises(GuardRefused) as caught:
            decide(
                body=raw_body(character_count=0),
                lease=lease(observed_character_count=0),
                request=request(estimated_credits=3_001),
            )
        self.assertEqual(caught.exception.code, "budget")
        for cash in ("0.00", "0.0", "1", "-0", "0 ", "", None, 0, True):
            with self.subTest(cash=cash), self.assertRaises(GuardRefused) as caught:
                decide(request=request(cash_gbp=cash))
            self.assertEqual(caught.exception.code, "cash")
        for credits in (0, -1, True, False, "3000", 3000.0, None):
            with self.subTest(credits=credits), self.assertRaises(GuardRefused) as caught:
                decide(request=request(estimated_credits=credits))
            self.assertEqual(caught.exception.code, "budget")
        _board, token = decide(request=request(estimated_credits=1))
        self.assertEqual(token["estimated_credits"], 1)
        with self.assertRaises(GuardRefused) as caught:
            decide(
                body=raw_body(character_count=118_115),
                lease=lease(observed_character_count=118_115),
                request=request(estimated_credits=3_000),
            )
        self.assertEqual(caught.exception.code, "insufficient_capacity")

    def test_one_request_shape_and_no_retry(self):
        refusals = [
            (dict(attempt=2), "retry"),
            (dict(attempt=0), "retry"),
            (dict(attempt=True), "retry"),
            (dict(endpoint="/v1/sound-generation"), "endpoint"),
            (dict(model_id="music_v1"), "model"),
            (dict(force_instrumental=False), "not_instrumental"),
            (dict(music_length_ms=179_000), "duration"),
            (dict(music_length_ms=180_001), "duration"),
            (dict(music_length_ms=True), "duration"),
            (dict(holder="other-score"), "scope"),
        ]
        for overrides, code in refusals:
            with self.subTest(overrides=overrides), self.assertRaises(GuardRefused) as caught:
                decide(request=request(**overrides))
            self.assertEqual(caught.exception.code, code)

        board, token = decide()
        with self.assertRaises(GuardRefused) as caught:
            board.decide(
                raw_body(),
                fetched_at=FETCHED,
                now=FETCHED,
                http_status=200,
                lease=lease(),
                request=request(),
            )
        self.assertEqual(caught.exception.code, "retry_or_shared_meter")
        board.consume(token, body_sha256=token["body_sha256"])
        with self.assertRaises(GuardRefused) as caught:
            board.consume(token, body_sha256=token["body_sha256"])
        self.assertEqual(caught.exception.code, "retry")

    def test_refusal_burns_the_flight(self):
        board = MeterBoard()
        with self.assertRaises(GuardRefused):
            board.decide(
                raw_body(),
                fetched_at=FETCHED,
                now=FETCHED,
                http_status=200,
                lease=lease(peers=1),
                request=request(),
            )
        with self.assertRaises(GuardRefused) as caught:
            board.decide(
                raw_body(),
                fetched_at=FETCHED,
                now=FETCHED,
                http_status=200,
                lease=lease(),
                request=request(),
            )
        self.assertEqual(caught.exception.code, "retry_or_shared_meter")

    def test_consume_is_bound_to_the_same_body(self):
        board, token = decide()
        forged = dict(token)
        forged["authorizes_generation"] = True
        with self.assertRaises(GuardRefused) as caught:
            board.consume(forged, body_sha256=token["body_sha256"])
        self.assertEqual(caught.exception.code, "inconsistent_meter")
        with self.assertRaises(GuardRefused) as caught:
            board.consume(token, body_sha256=token["body_sha256"])
        self.assertEqual(caught.exception.code, "retry")

        board, token = decide()
        with self.assertRaises(GuardRefused) as caught:
            board.consume(token, body_sha256="0" * 64)
        self.assertEqual(caught.exception.code, "inconsistent_meter")

    def test_transport_arguments_are_refused(self):
        board = MeterBoard()
        with self.assertRaises(GuardRefused) as caught:
            board.decide(
                raw_body(),
                fetched_at=FETCHED,
                now=FETCHED,
                http_status=200,
                lease=lease(),
                request=request(),
                transport=object(),
            )
        self.assertEqual(caught.exception.code, "network_forbidden")

    def test_concurrent_callers_get_one_decision(self):
        board = MeterBoard()
        barrier = threading.Barrier(2)
        results = []

        def run():
            barrier.wait()
            try:
                token = board.decide(
                    raw_body(),
                    fetched_at=FETCHED,
                    now=FETCHED,
                    http_status=200,
                    lease=lease(),
                    request=request(),
                )
                results.append(("pass", token["outcome"]))
            except GuardRefused as exc:
                results.append(("refuse", exc.code))

        threads = [threading.Thread(target=run) for _ in range(2)]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
        self.assertEqual(sorted(kind for kind, _value in results), ["pass", "refuse"])
        self.assertEqual(
            [value for kind, value in results if kind == "refuse"],
            ["retry_or_shared_meter"],
        )

    def test_pass_is_pinned_to_the_raw_bytes(self):
        body = raw_body()
        _board, token = decide(body=body)
        self.assertEqual(token["body_sha256"], hashlib.sha256(body).hexdigest())

    def test_production_files_do_not_import_the_proposal(self):
        root = Path(__file__).resolve().parents[3]
        for relative in (
            "04_Audio/tools/el_guard.py",
            "04_Audio/tools/generate_music_bed.py",
            "04_Audio/tools/el_client.py",
        ):
            text = (root / relative).read_text(encoding="utf-8")
            self.assertNotIn("score_billing_guard", text)
        source = Path(__file__).with_name("score_billing_guard.py").read_text(encoding="utf-8")
        imports = "\n".join(
            line
            for line in source.splitlines()
            if line.startswith("import ") or line.startswith("from ")
        )
        for banned in ("socket", "urllib", "requests", "os", "subprocess", "http"):
            self.assertNotIn(banned, imports)
        self.assertNotIn("EL_GUARD_OFF", source)
        self.assertNotIn("getenv", source)

    def test_module_hash_pin(self):
        module = Path(__file__).with_name("score_billing_guard.py").read_bytes()
        pinned = Path(__file__).with_name("HASHES.txt").read_text(encoding="utf-8")
        self.assertIn(hashlib.sha256(module).hexdigest(), pinned)


if __name__ == "__main__":
    unittest.main()
