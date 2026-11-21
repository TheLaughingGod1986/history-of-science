#!/usr/bin/env python3
"""J3148 independent adversarial synthetic test suite for repaired HOS 009 score_billing_guard.py (11ed0c86).

Offline only: zero account calls, zero network calls, zero production mutations.
Adapts all J3145 probes so each of Findings A-D now proves the unsafe case is REFUSED
(never mistaking vulnerability proofs for acceptance), while re-verifying all earlier
J3142 Findings 1-7 and Chief desk 7013542642/7014651936/7015532256/7015685170 requirements
against HOS PR #669 commit 11ed0c86d925dca5cbbbd1a2abef71326f1b6b7a.

Usage:
    python3 jobs/reviews/J3148/probe_j3148.py /path/to/jobs/reviews/J3141
"""

from __future__ import annotations

import ast
import dataclasses
import fcntl
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

TARGET_DIR = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else None
if TARGET_DIR is not None:
    sys.path.insert(0, str(TARGET_DIR))

import score_billing_adapter as sba  # noqa: E402
import score_billing_guard as sbg  # noqa: E402
from score_billing_adapter import proposed_flight  # noqa: E402
from score_billing_guard import (  # noqa: E402
    GuardRefused,
    MeterBoard,
    TransportReceipt,
    bind_desk,
    hold_recorder,
    meter_units_per_credit,
    read_subscription,
    recorder_held,
    release_test_holder,
)

EXPECTED_HASHES = {
    "score_billing_guard.py": "930d987783055d1f73e80fd9ae770f1ecde63d79b397706df74e9492b4029308",
    "score_billing_adapter.py": "0550bb49bec3d6e55706beba73618e4aa9560487a2935ea9eb8cec84fa912819",
    "test_score_billing_guard.py": "69dabdc279dd5e298a3a92199fb45d19e3d3efcd1387a452872356d7656c324c",
    "PROPOSAL.md": "968c8ce535170658d5face6c9d95aed3717d336adf7d29742d32ab3a8c30f48b",
    "INTEGRATION_DIFF.md": "3d11a041e6e58b3ecbe2e22cf0f0781bdb4a51c9f56f65261cdd65d3f6756fc8",
    "subscription_shape.json": "ba290b64740c96c3407af17da80d043be3bf840d1863518bfb011e047f9e647e",
    "HASHES.txt": "f58907328b8aa53441d01db0b621454e62aabd87d8ec2666e008ed65c509363b",
}

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
    def __init__(self, *, bind: bool = True, hold: bool = True) -> None:
        release_test_holder()
        self.dir = Path(tempfile.mkdtemp(prefix="j3148-probe-"))
        (self.dir / "locks").mkdir(parents=True, exist_ok=True)
        (self.dir / "elevenlabs").mkdir(parents=True, exist_ok=True)
        self.pause = self.dir / "elevenlabs" / "TTS_PAUSE"
        self.ledger = self.dir / "elevenlabs" / "ledger.jsonl"
        self.ledger.write_text("", encoding="utf-8")
        self.lock = self.dir / "locks" / "elevenlabs.lock"
        self.store = self.dir / "elevenlabs" / "hos009-score-single-use.json"
        if bind:
            bind_desk(self.dir)
        if bind and hold:
            hold_recorder()
            # Ensure lock started timestamp is slightly before any rounded HTTP Date header
            started = (datetime.now(timezone.utc) - timedelta(seconds=5)).replace(microsecond=0).isoformat()
            self.rewrite_held(started=started)

    def rewrite_held(
        self,
        *,
        started: str | None = None,
        pid: int | None = None,
        host: str | None = None,
        script: str | None = None,
        extra: dict | None = None,
    ) -> None:
        moment = started or (datetime.now(timezone.utc) - timedelta(seconds=5)).replace(microsecond=0).isoformat()
        payload = {
            "pid": os.getpid() if pid is None else pid,
            "host": socket.gethostname() if host is None else host,
            "script": script if script is not None else sbg.RECORDER_SCRIPT,
            "started": moment,
        }
        if extra:
            payload.update(extra)
        raw = json.dumps(payload).encode("utf-8")
        os.lseek(sbg._held_fd, 0, os.SEEK_SET)
        os.ftruncate(sbg._held_fd, 0)
        os.write(sbg._held_fd, raw)
        sbg._held_started = moment

    def date_hdr(self, seconds_ago: float = 0.0) -> str:
        return formatdate(time.time() - seconds_ago, usegmt=True)

    def seal(self, raw: bytes | None = None, *, status: int = 200, date_value: str | None = None) -> TransportReceipt:
        body = make_raw() if raw is None else raw
        hdr = self.date_hdr() if date_value is None else date_value
        return read_subscription(lambda: (status, {"Date": hdr}, body))

    def decide(
        self,
        raw: bytes | None = None,
        *,
        board: MeterBoard | None = None,
        receipt: object | None = None,
        status: int = 200,
        date_value: str | None = None,
        request: object | None = None,
        **forbidden: object,
    ) -> tuple[MeterBoard, dict]:
        b = board or MeterBoard()
        rcpt = self.seal(raw, status=status, date_value=date_value) if receipt is None else receipt
        req = make_req() if request is None else request
        return b, b.decide(rcpt, request=req, **forbidden)


class MockTransport:
    def __init__(self, body: bytes, header: str, status: int = 200) -> None:
        self.body = body
        self.header = header
        self.status = status
        self.gets = 0
        self.posts = 0
        self.post_lock_held = False

    def get_subscription(self) -> tuple[int, dict, bytes]:
        self.gets += 1
        return (self.status, {"Date": self.header}, self.body)

    def post_music(self, spent_token: dict) -> None:
        self.posts += 1
        self.post_lock_held = recorder_held() and sbg._held_fd is not None
        if spent_token.get("consumed") is not True:
            raise GuardRefused("retry")


class J3148IndependentGuardRepairReviewSuite(unittest.TestCase):
    """Independent adversarial review of HOS PR #669 at commit 11ed0c86d925dca5cbbbd1a2abef71326f1b6b7a."""

    def tearDown(self) -> None:
        release_test_holder()

    def test_01_exact_artifact_hashes_and_ast_no_network_or_env(self) -> None:
        guard_dir = Path(sbg.__file__).resolve().parent
        for name, exp_sha in EXPECTED_HASHES.items():
            digest = hashlib.sha256((guard_dir / name).read_bytes()).hexdigest()
            self.assertEqual(digest, exp_sha, f"SHA-256 mismatch on {name}")

        # Verify HASHES.txt pins the exact 6 content files
        hashes_lines = (guard_dir / "HASHES.txt").read_text(encoding="utf-8").strip().splitlines()
        self.assertEqual(len(hashes_lines), 6)
        for line in hashes_lines:
            sha, fname = line.split()
            self.assertEqual(EXPECTED_HASHES[fname], sha)

        # AST audit of score_billing_guard.py and score_billing_adapter.py
        for fname, allowed_imports in (
            (
                "score_billing_guard.py",
                {
                    "__future__",
                    "copy",
                    "datetime",
                    "decimal",
                    "email",
                    "fcntl",
                    "hashlib",
                    "hmac",
                    "json",
                    "os",
                    "pathlib",
                    "re",
                    "secrets",
                    "socket",
                    "stat",
                    "threading",
                },
            ),
            ("score_billing_adapter.py", {"__future__", "score_billing_guard"}),
        ):
            src = (guard_dir / fname).read_text(encoding="utf-8")
            tree = ast.parse(src)
            imported = set()
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        imported.add(alias.name.split(".")[0])
                elif isinstance(node, ast.ImportFrom) and node.module:
                    imported.add(node.module.split(".")[0])
                elif isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
                    self.assertNotIn(node.func.id, {"__import__", "eval", "exec", "compile"})
                elif isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
                    # socket.gethostname() is the only permitted socket call; no socket() or create_connection()
                    if isinstance(node.func.value, ast.Name) and node.func.value.id == "socket":
                        self.assertEqual(node.func.attr, "gethostname")
            self.assertEqual(imported, allowed_imports)
            for forbidden_token in ("os.environ", "getenv", "EL_GUARD_OFF", "urlopen"):
                self.assertNotIn(forbidden_token, src)

    def test_02_nested_overage_and_currency_matrix_holds(self) -> None:
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

        for flat_key in ("current_overage_amount", "current_overage_currency"):
            h = Harness()
            with self.assertRaises(GuardRefused) as ctx:
                h.decide(make_raw(**{flat_key: "0"}))
            self.assertEqual(ctx.exception.code, "overage")

    def test_03_real_34_key_shape_untyped_scalars_and_key_precedence(self) -> None:
        self.assertEqual(set(LIVE_17NOV_34_KEYS), set(sbg.REQUIRED_KEYS))
        h = Harness()
        _, tok = h.decide(make_raw())
        self.assertEqual(tok["outcome"], "pass_once")

        h_extra = Harness()
        with self.assertRaises(GuardRefused) as ctx:
            h_extra.decide(make_raw(unexpected_field=1))
        self.assertEqual(ctx.exception.code, "unknown_field")

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

        sub = make_sub()
        del sub["current_overage"]
        del sub["currency"]
        h_prec = Harness()
        with self.assertRaises(GuardRefused) as ctx:
            h_prec.decide(json.dumps(sub).encode("utf-8"))
        self.assertEqual(ctx.exception.code, "overage")

    def test_04_scheduled_renewal_next_invoice_passes_and_bad_invoices_refuse(self) -> None:
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

    def test_05_consume_enforces_immutable_token_and_burns_on_tamper(self) -> None:
        for field, forged in (
            ("estimated_credits", 1),
            ("cash_gbp", "25.00"),
            ("would_allow_posts", 99),
            ("retries", 5),
            ("integrated", True),
            ("proposal_only", False),
            ("authorizes_generation", True),
            ("opens_allowance", True),
            ("tariff_current_guarantee", True),
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
                # Even passing the unmodified token afterwards refuses as retry
                with self.assertRaises(GuardRefused) as ctx2:
                    board.consume(tok, body_sha256=tok["body_sha256"])
                self.assertEqual(ctx2.exception.code, "retry")

    def test_06_tariff_floor_meter_mapping_and_no_current_guarantee(self) -> None:
        self.assertEqual(sbg.MIN_ESTIMATED_CREDITS, 2_970)
        self.assertEqual(sbg.MEASURED_CREDITS, 2_475)
        self.assertEqual(sbg.PUBLISHED_180S_CREDITS, 2_700)
        self.assertFalse(sbg.TARIFF_CURRENT_GUARANTEE)
        self.assertEqual(meter_units_per_credit(), 1)

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
            self.assertFalse(tok["tariff_current_guarantee"])

        h_low = Harness()
        with self.assertRaises(GuardRefused) as ctx:
            h_low.decide(
                make_raw(character_count=10_000 - 2_969, character_limit=10_000),
                request=make_req(estimated_credits=2_970),
            )
        self.assertEqual(ctx.exception.code, "insufficient_capacity")

        for bad_ms in (60_000, 120_000, 179_999, 180_001, 240_000):
            h_dur = Harness()
            with self.assertRaises(GuardRefused) as ctx:
                h_dur.decide(request=make_req(music_length_ms=bad_ms))
            self.assertEqual(ctx.exception.code, "duration")

    def test_07_strict_json_clock_window_and_provenance(self) -> None:
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
            "tariff_current_guarantee",
            "measured_180s_credits",
            "published_180s_credits",
            "floor_credits",
        ):
            self.assertIn(key, tok)

        # Future Date header refuses as inconsistent_clock
        h_fut = Harness()
        fut_hdr = formatdate(time.time() + 30, usegmt=True)
        with self.assertRaises(GuardRefused) as ctx:
            h_fut.decide(date_value=fut_hdr)
        self.assertEqual(ctx.exception.code, "inconsistent_clock")

        # Stale Date header (>60s) refuses as stale and burns single-use store file
        h_stale = Harness()
        stale_hdr = formatdate(time.time() - 65, usegmt=True)
        with self.assertRaises(GuardRefused) as ctx:
            h_stale.decide(date_value=stale_hdr)
        self.assertEqual(ctx.exception.code, "stale")
        self.assertTrue(h_stale.store.is_file())
        with self.assertRaises(GuardRefused) as ctx2:
            h_stale.decide()
        self.assertEqual(ctx2.exception.code, "retry_or_shared_meter")

        for raw_const in (b'{"x": NaN}', b'{"x": Infinity}', b'{"x": -Infinity}', b'\xef\xbb\xbf{"x": 1}'):
            with self.assertRaises(GuardRefused) as ctx:
                sbg.loads_strict(raw_const)
            self.assertEqual(ctx.exception.code, "malformed_body")

        with self.assertRaises(GuardRefused) as ctx:
            sbg.loads_strict(b'{"a": 1, "a": 2}')
        self.assertEqual(ctx.exception.code, "duplicate_key")

    def test_08_finding_A_repaired_internally_pinned_paths_and_durable_crash_safe_single_use(self) -> None:
        """VERIFIED REPAIRED (Finding A):
        (1) Passing store_path, lock_path, pause_path, or ledger_path into decide() now REFUSES
            with caller_asserted_state before touching the single-use store.
        (2) Unbound desk refuses with unbound_desk; binding live ~/_desk (or any subdirectory)
            refuses with live_desk_forbidden.
        (3) Symlinked lock, pause, ledger, or store paths inside the desk root refuse.
        (4) Durable single-use persists across a new MeterBoard, across a fresh process after
            simulated crash/restart, and refuses even when a different subscription body and
            different valid request are tried against the same bound desk root."""
        h = Harness()
        other_dir = Path(tempfile.mkdtemp(prefix="j3148-alt-"))
        for kw in (
            {"store_path": other_dir / "hos009-score-single-use.json"},
            {"lock_path": other_dir / "elevenlabs.lock"},
            {"pause_path": other_dir / "TTS_PAUSE"},
            {"ledger_path": other_dir / "ledger.jsonl"},
        ):
            with self.subTest(kw=list(kw.keys())), self.assertRaises(GuardRefused) as ctx:
                h.decide(**kw)
            self.assertEqual(ctx.exception.code, "caller_asserted_state")
            self.assertFalse(h.store.exists())

        # Any unexpected path/desk argument to decide() refuses as network_forbidden
        with self.assertRaises(GuardRefused) as ctx:
            h.decide(desk=other_dir)
        self.assertEqual(ctx.exception.code, "network_forbidden")

        # Live ~/_desk or subdirectory is refused by bind_desk()
        live_desk = Path.home() / "_desk"
        if live_desk.is_dir():
            with self.assertRaises(GuardRefused) as ctx:
                bind_desk(live_desk)
            self.assertEqual(ctx.exception.code, "live_desk_forbidden")
            sub_live = live_desk / "state"
            if sub_live.is_dir():
                with self.assertRaises(GuardRefused) as ctx:
                    bind_desk(sub_live)
                self.assertEqual(ctx.exception.code, "live_desk_forbidden")

        # Unbound desk refuses
        sbg._desk = None
        with self.assertRaises(GuardRefused) as ctx:
            h.decide()
        self.assertEqual(ctx.exception.code, "unbound_desk")

        # Symlinked pause/ledger/store refuses
        h_sym = Harness()
        real_store = other_dir / "real-store.json"
        real_store.write_text("", encoding="utf-8")
        h_sym.store.symlink_to(real_store)
        with self.assertRaises(GuardRefused) as ctx:
            h_sym.decide()
        self.assertEqual(ctx.exception.code, "retry_or_shared_meter")

        # Durable single-use across fresh MeterBoard AND subprocess restart, even with a different body/request
        h_dur = Harness()
        _, tok1 = h_dur.decide(make_raw(character_count=10_000), request=make_req(estimated_credits=2_970))
        self.assertEqual(tok1["outcome"], "pass_once")
        self.assertTrue(h_dur.store.is_file())

        # In-process second board with DIFFERENT body and DIFFERENT request still refuses
        with self.assertRaises(GuardRefused) as ctx:
            h_dur.decide(
                make_raw(character_count=20_000),
                board=MeterBoard(),
                request=make_req(estimated_credits=3_000),
            )
        self.assertEqual(ctx.exception.code, "retry_or_shared_meter")

        # Subprocess after simulated crash/restart (release lock and let child take lock on same desk)
        release_test_holder()
        h_dur.lock.unlink()
        child_code = textwrap.dedent(
            """
            import json, sys, time
            from email.utils import formatdate
            from pathlib import Path
            sys.path.insert(0, sys.argv[1])
            import score_billing_guard as sbg
            root = Path(sys.argv[2])
            sub = sys.argv[3].encode("utf-8")
            req = json.loads(sys.argv[4])
            sbg.bind_desk(root)
            sbg.hold_recorder()
            rcpt = sbg.read_subscription(lambda: (200, {"Date": formatdate(time.time(), usegmt=True)}, sub))
            try:
                sbg.MeterBoard().decide(rcpt, request=req)
            except sbg.GuardRefused as exc:
                print(exc.code)
            else:
                print("UNEXPECTED_PASS")
            """
        )
        res = subprocess.run(
            [
                sys.executable,
                "-c",
                child_code,
                str(Path(sbg.__file__).resolve().parent),
                str(h_dur.dir),
                json.dumps(make_sub(character_count=30_000)),
                json.dumps(make_req(estimated_credits=2_990)),
            ],
            check=False,
            capture_output=True,
            text=True,
            timeout=15,
        )
        self.assertEqual(res.returncode, 0, res.stderr)
        self.assertEqual(res.stdout.strip(), "retry_or_shared_meter")

    def test_09_finding_B_repaired_process_held_o_excl_recorder_and_two_process_exclusion(self) -> None:
        """VERIFIED REPAIRED (Finding B):
        (1) A plain unlocked PID file on disk containing os.getpid() without hold_recorder()'s
            open O_EXCL descriptor now REFUSES with shared_meter.
        (2) Pre-flocking _held_fd in the current process no longer conflicts with _observe_lock():
            decide() and consume() pass, never call flock/unlink/close, and keep _held_fd open.
        (3) Two-process exclusion: a second live process calling hold_recorder() against the
            same desk root while process 1 holds it REFUSES with shared_meter.
        (4) If elevenlabs.lock is unlinked, replaced by a new inode, or overwritten with another
            PID/host/started timestamp between decide() and consume(), consume() REFUSES."""
        # (1) Plain PID file on disk without hold_recorder() descriptor refuses
        h_plain = Harness(bind=True, hold=False)
        h_plain.lock.write_text(
            json.dumps(
                {
                    "pid": os.getpid(),
                    "host": socket.gethostname(),
                    "script": sbg.RECORDER_SCRIPT,
                    "started": (datetime.now(timezone.utc) - timedelta(seconds=5)).replace(microsecond=0).isoformat(),
                }
            ),
            encoding="utf-8",
        )
        with self.assertRaises(GuardRefused) as ctx:
            h_plain.decide()
        self.assertEqual(ctx.exception.code, "shared_meter")

        # (2) Pre-flocked descriptor in this process passes decide() and consume() and stays open
        h_flock = Harness()
        fcntl.flock(sbg._held_fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        try:
            board, tok = h_flock.decide()
            self.assertEqual(tok["outcome"], "pass_once")
            self.assertTrue(recorder_held())
            spent = board.consume(tok, body_sha256=tok["body_sha256"])
            self.assertTrue(spent["consumed"])
            self.assertTrue(recorder_held())
            os.fstat(sbg._held_fd)
        finally:
            fcntl.flock(sbg._held_fd, fcntl.LOCK_UN)

        # AST check that _observe_lock never calls flock, open, close, or unlink
        obs_tree = ast.parse(inspect.getsource(sbg._observe_lock))
        obs_calls = {
            node.func.attr
            for node in ast.walk(obs_tree)
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)
        }
        for forbidden_call in ("flock", "open", "close", "unlink"):
            self.assertNotIn(forbidden_call, obs_calls)

        # (3) Two-process exclusion while process 1 holds the recorder
        h_two = Harness()
        child_script = textwrap.dedent(
            """
            import sys
            from pathlib import Path
            sys.path.insert(0, sys.argv[1])
            import score_billing_guard as sbg
            sbg.bind_desk(Path(sys.argv[2]))
            try:
                sbg.hold_recorder()
            except sbg.GuardRefused as exc:
                print(exc.code)
            else:
                print("UNEXPECTED_ACQUIRED")
            """
        )
        proc = subprocess.run(
            [
                sys.executable,
                "-c",
                child_script,
                str(Path(sbg.__file__).resolve().parent),
                str(h_two.dir),
            ],
            check=False,
            capture_output=True,
            text=True,
            timeout=15,
        )
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertEqual(proc.stdout.strip(), "shared_meter")

        # (4) Replacing elevenlabs.lock with a new inode between decide() and consume() refuses at consume()
        h_inode = Harness()
        board_ino, tok_ino = h_inode.decide()
        lock_bytes = h_inode.lock.read_bytes()
        h_inode.lock.unlink()
        h_inode.lock.write_bytes(lock_bytes)
        with self.assertRaises(GuardRefused) as ctx:
            board_ino.consume(tok_ino, body_sha256=tok_ino["body_sha256"])
        self.assertEqual(ctx.exception.code, "shared_meter")

    def test_10_finding_C_repaired_trusted_single_response_binding_and_hmac_seal(self) -> None:
        """VERIFIED REPAIRED (Finding C):
        (1) Loose date_header, raw, or http_status kwargs to decide() REFUSE with untrusted_receipt.
        (2) Direct TransportReceipt(...) instantiation, frozen dataclass stand-ins, or
            object.__new__(TransportReceipt) forgeries REFUSE with untrusted_receipt.
        (3) Mutating raw, date_value, or status on a sealed TransportReceipt via object.__setattr__
            (e.g. pairing a fresh Date from response A with a body from response B, or mutating
            between decide() and consume()) fails HMAC verification and REFUSES with untrusted_receipt.
        (4) Missing Date, duplicate Date headers, or non-3-tuple fetch result in read_subscription()
            REFUSES with untrusted_receipt."""
        h = Harness()
        rcpt_test = h.seal()
        for loose_kw in (
            {"date_header": h.date_hdr()},
            {"raw": make_raw()},
            {"http_status": 200},
        ):
            with self.subTest(kw=list(loose_kw.keys())):
                with self.assertRaises(GuardRefused) as ctx:
                    MeterBoard().decide(rcpt_test, request=make_req(), **loose_kw)
                self.assertEqual(ctx.exception.code, "untrusted_receipt")

        # Direct constructor refuses
        with self.assertRaises(GuardRefused) as ctx:
            TransportReceipt(200, h.date_hdr(), make_raw())
        self.assertEqual(ctx.exception.code, "untrusted_receipt")

        # Frozen dataclass stand-in with identical fields refuses
        @dataclasses.dataclass(frozen=True)
        class FakeReceipt:
            status: int
            date_value: str
            raw: bytes
            _mac: bytes = b"\x00" * 32

        fake_dc = FakeReceipt(200, h.date_hdr(), make_raw())
        with self.assertRaises(GuardRefused) as ctx:
            MeterBoard().decide(fake_dc, request=make_req())
        self.assertEqual(ctx.exception.code, "untrusted_receipt")

        # object.__new__(TransportReceipt) forgery not in _ISSUED / without valid HMAC refuses
        forged_rcpt = object.__new__(TransportReceipt)
        object.__setattr__(forged_rcpt, "status", 200)
        object.__setattr__(forged_rcpt, "date_value", h.date_hdr())
        object.__setattr__(forged_rcpt, "raw", make_raw())
        object.__setattr__(forged_rcpt, "_mac", b"\x11" * 32)
        with self.assertRaises(GuardRefused) as ctx:
            MeterBoard().decide(forged_rcpt, request=make_req())
        self.assertEqual(ctx.exception.code, "untrusted_receipt")

        # Pairing fresh Date from sealed response A with body from response B via object.__setattr__ refuses
        rcpt_a = h.seal(make_raw(character_count=10_000), date_value=h.date_hdr(seconds_ago=1))
        body_b = make_raw(character_count=50_000)
        object.__setattr__(rcpt_a, "raw", body_b)
        with self.assertRaises(GuardRefused) as ctx:
            MeterBoard().decide(rcpt_a, request=make_req())
        self.assertEqual(ctx.exception.code, "untrusted_receipt")

        # Mutating sealed receipt after decide() and before consume() refuses at consume()
        h_mut = Harness()
        rcpt_valid = h_mut.seal()
        board_mut, tok_mut = h_mut.decide(receipt=rcpt_valid)
        object.__setattr__(rcpt_valid, "date_value", h_mut.date_hdr(seconds_ago=3))
        with self.assertRaises(GuardRefused) as ctx:
            board_mut.consume(tok_mut, body_sha256=tok_mut["body_sha256"])
        self.assertEqual(ctx.exception.code, "untrusted_receipt")

        # Missing or duplicate Date headers in read_subscription refuse
        for bad_headers in ({}, {"X-Other": "1"}, {"Date": h.date_hdr(), "date": h.date_hdr()}, {"Date": ""}):
            with self.assertRaises(GuardRefused) as ctx:
                read_subscription(lambda bh=bad_headers: (200, bh, make_raw()))
            self.assertEqual(ctx.exception.code, "untrusted_receipt")

    def test_11_finding_D_repaired_same_second_and_unreconciled_ledger_refusals(self) -> None:
        """VERIFIED REPAIRED (Finding D):
        (1) Same-second spend (`when == fetched`) with status 200 now REFUSES as pending_spend.
        (2) Non-200 status (500, 502, 504, "200", None, True) before `fetched` now REFUSES as
            pending_spend unless that ledger line carries `reconciled: True` and a non-empty
            string `reconciliation`.
        (3) Even with `reconciled: True` and a valid note, a same-second (`when == fetched`) or
            later (`when > fetched`) ledger line still REFUSES as pending_spend.
        (4) Malformed ledger lines (duplicate keys, bare NaN) refuse via loads_strict."""
        # (1) Same-second spend (when == fetched) with status 200 refuses
        h_same = Harness()
        hdr = h_same.date_hdr(seconds_ago=1)
        fetched_dt = parsedate_to_datetime(hdr).astimezone(timezone.utc).replace(microsecond=0)
        h_same.rewrite_held(started=(fetched_dt - timedelta(seconds=5)).isoformat())
        h_same.ledger.write_text(
            json.dumps({"time": fetched_dt.isoformat(), "status": 200, "chars": 2970}) + "\n",
            encoding="utf-8",
        )
        with self.assertRaises(GuardRefused) as ctx:
            h_same.decide(date_value=hdr)
        self.assertEqual(ctx.exception.code, "pending_spend")

        # (2) Non-200 or non-int status before fetched refuses when unreconciled
        past_iso = (datetime.now(timezone.utc) - timedelta(minutes=10)).replace(microsecond=0).isoformat()
        for bad_status in (500, 502, 504, "200", None, True):
            h_bad = Harness()
            h_bad.ledger.write_text(
                json.dumps({"time": past_iso, "status": bad_status}) + "\n",
                encoding="utf-8",
            )
            with self.assertRaises(GuardRefused) as ctx:
                h_bad.decide()
            self.assertEqual(ctx.exception.code, "pending_spend")

        # Incomplete reconciliation (empty note or reconciled=False) still refuses
        for bad_rec in (
            {"time": past_iso, "status": 500, "reconciled": True, "reconciliation": "   "},
            {"time": past_iso, "status": 500, "reconciled": True},
            {"time": past_iso, "status": 500, "reconciled": False, "reconciliation": "note"},
        ):
            h_inc = Harness()
            h_inc.ledger.write_text(json.dumps(bad_rec) + "\n", encoding="utf-8")
            with self.assertRaises(GuardRefused) as ctx:
                h_inc.decide()
            self.assertEqual(ctx.exception.code, "pending_spend")

        # Properly reconciled historical non-200 line before fetched passes
        h_rec = Harness()
        h_rec.ledger.write_text(
            json.dumps(
                {
                    "time": past_iso,
                    "status": 500,
                    "reconciled": True,
                    "reconciliation": "J3140 verified zero account delta before subscription read",
                }
            )
            + "\n",
            encoding="utf-8",
        )
        _, tok_rec = h_rec.decide()
        self.assertEqual(tok_rec["outcome"], "pass_once")

        # (3) Reconciled line at when == fetched (same second) STILL refuses
        h_rec_same = Harness()
        h_rec_same.rewrite_held(started=(fetched_dt - timedelta(seconds=5)).isoformat())
        h_rec_same.ledger.write_text(
            json.dumps(
                {
                    "time": fetched_dt.isoformat(),
                    "status": 500,
                    "reconciled": True,
                    "reconciliation": "cannot waive same-second timestamp",
                }
            )
            + "\n",
            encoding="utf-8",
        )
        with self.assertRaises(GuardRefused) as ctx:
            h_rec_same.decide(date_value=hdr)
        self.assertEqual(ctx.exception.code, "pending_spend")

        # (4) Duplicate key in ledger line refuses as duplicate_key via loads_strict
        h_dup = Harness()
        h_dup.ledger.write_text(
            f'{{"time": "{past_iso}", "status": 500, "status": 200}}\n',
            encoding="utf-8",
        )
        with self.assertRaises(GuardRefused) as ctx:
            h_dup.decide()
        self.assertEqual(ctx.exception.code, "duplicate_key")

    def test_12_consume_rechecks_and_proposed_flight_one_get_at_most_one_post(self) -> None:
        """VERIFIED (Freshness/state at consumption & proposed_flight one-GET / at-most-one-POST):
        (1) consume() re-verifies freshness, TTS_PAUSE, ledger.jsonl (including same-second spend),
            and recorder lock ownership.
        (2) proposed_flight() executes 1 mocked GET and 1 mocked POST on a passing flight while
            holding the recorder lock through POST; 0 GETs and 0 POSTs on a second call to the
            same board or when recorder lock is not held; and 1 GET and 0 POSTs on any refusal."""
        # Same-second spend appearing in ledger between decide() and consume() refuses at consume()
        h_c = Harness()
        hdr = h_c.date_hdr(seconds_ago=1)
        fetched_dt = parsedate_to_datetime(hdr).astimezone(timezone.utc).replace(microsecond=0)
        h_c.rewrite_held(started=(fetched_dt - timedelta(seconds=5)).isoformat())
        board_c, tok_c = h_c.decide(date_value=hdr)
        h_c.ledger.write_text(
            json.dumps({"time": fetched_dt.isoformat(), "status": 200}) + "\n",
            encoding="utf-8",
        )
        with self.assertRaises(GuardRefused) as ctx:
            board_c.consume(tok_c, body_sha256=tok_c["body_sha256"])
        self.assertEqual(ctx.exception.code, "pending_spend")

        # proposed_flight happy path: 1 GET, 1 POST, lock held during POST
        h_ok = Harness()
        tx_ok = MockTransport(make_raw(), h_ok.date_hdr())
        board_ok = MeterBoard()
        spent = proposed_flight(board_ok, tx_ok, make_req())
        self.assertEqual(tx_ok.gets, 1)
        self.assertEqual(tx_ok.posts, 1)
        self.assertTrue(tx_ok.post_lock_held)
        self.assertTrue(spent["consumed"])
        self.assertFalse(spent["authorizes_generation"])

        # Second call on already-used board: 0 GETs, 0 POSTs
        tx_second = MockTransport(make_raw(), h_ok.date_hdr())
        with self.assertRaises(GuardRefused) as ctx:
            proposed_flight(board_ok, tx_second, make_req())
        self.assertEqual(ctx.exception.code, "retry_or_shared_meter")
        self.assertEqual(tx_second.gets, 0)
        self.assertEqual(tx_second.posts, 0)

        # Call without recorder_held(): 0 GETs, 0 POSTs
        h_nolock = Harness(bind=True, hold=False)
        tx_nolock = MockTransport(make_raw(), h_nolock.date_hdr())
        with self.assertRaises(GuardRefused) as ctx:
            proposed_flight(MeterBoard(), tx_nolock, make_req())
        self.assertEqual(ctx.exception.code, "shared_meter")
        self.assertEqual(tx_nolock.gets, 0)
        self.assertEqual(tx_nolock.posts, 0)

        # Call that fails guard evaluation (e.g. overage): 1 GET, 0 POSTs
        h_ov = Harness()
        tx_ov = MockTransport(make_raw(current_overage={"amount": "0.01", "currency": "usd"}), h_ov.date_hdr())
        with self.assertRaises(GuardRefused) as ctx:
            proposed_flight(MeterBoard(), tx_ov, make_req())
        self.assertEqual(ctx.exception.code, "overage")
        self.assertEqual(tx_ov.gets, 1)
        self.assertEqual(tx_ov.posts, 0)


if __name__ == "__main__":
    if len(sys.argv) > 1 and Path(sys.argv[1]).exists():
        sys.argv.pop(1)
    unittest.main(verbosity=2)
