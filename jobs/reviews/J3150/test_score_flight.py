#!/usr/bin/env python3
"""Offline adversarial checks for the disabled HOS 009 music flight.

No account call. The socket is patched or asserted unused. Fixtures bind a
temporary desk through the guard's own test seam. The production functions
do not take that desk, a transport, or a path.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import time
import unittest
import urllib.request
from datetime import datetime, timezone
from email.utils import formatdate, parsedate_to_datetime
from pathlib import Path

TOOLS = Path(__file__).resolve().parents[3] / "04_Audio" / "tools"
sys.path.insert(0, str(TOOLS))

import el_client  # noqa: E402
import el_guard  # noqa: E402
import generate_music_bed  # noqa: E402
import hos009_score_flight as flight  # noqa: E402

RESET = 1_893_456_000
PROMPT = "Continuous overlapping gut-string lute and bowed viols, no rests."


def subscription(**overrides) -> bytes:
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
        "character_limit": 100_000,
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
    return json.dumps(payload).encode("utf-8")


def fresh_header(seconds_ago: int = 1) -> str:
    return formatdate(time.time() - seconds_ago, usegmt=True)


def lock_header() -> str:
    """Date at the lock's own second, so the lease is not newer than the response."""
    started = datetime.fromisoformat(flight.guard._held_started)
    return formatdate(started.timestamp(), usegmt=True)


class Desk:
    def __init__(self) -> None:
        flight.guard.release_test_holder()
        self.root = Path(tempfile.mkdtemp(prefix="hos009-flight-"))
        (self.root / "locks").mkdir()
        eleven = self.root / "elevenlabs"
        eleven.mkdir()
        self.ledger = eleven / "ledger.jsonl"
        self.ledger.write_text("", encoding="utf-8")
        self.pause = eleven / "TTS_PAUSE"
        self.store = eleven / "hos009-score-single-use.json"
        flight.guard.bind_desk(self.root)

    def close(self) -> None:
        flight.guard.release_test_holder()


class FlightTest(unittest.TestCase):
    def setUp(self) -> None:
        self.desk = Desk()
        self.calls: list[tuple[str, bytes | None]] = []
        self.real_exchange = flight._read_one_response
        self.real_urlopen = urllib.request.urlopen
        os.environ.pop("EL_GUARD_OFF", None)

    def tearDown(self) -> None:
        flight._read_one_response = self.real_exchange
        urllib.request.urlopen = self.real_urlopen
        self.desk.close()
        os.environ.pop("EL_GUARD_OFF", None)

    def exchange(self, method: str, body: bytes | None, *, header: str | None = None, payload: bytes | None = None, post: bytes = b"audio"):
        payload = subscription() if payload is None else payload

        def fake(got_method: str, got_body: bytes | None):
            self.calls.append((got_method, got_body))
            used = lock_header() if header is None else header
            if got_method == "GET":
                return 200, used, payload
            return 200, used, post

        flight._read_one_response = fake

    def test_activation_constant_and_source_locks(self) -> None:
        self.assertIs(flight.ACTIVATION_AUTHORIZED, False)
        source = Path(flight.__file__).read_text(encoding="utf-8")
        self.assertIn("ACTIVATION_AUTHORIZED = False", source)
        self.assertNotIn('environ.get("EL_GUARD_OFF")', source)
        self.assertNotIn("unlink(", source)
        self.assertNotIn("os.environ", source)
        self.assertEqual(flight._sha(flight._PINNED / "score_billing_guard.py"), flight.GUARD_SHA256)

    def test_closed_activation_makes_no_socket(self) -> None:
        opened: list[str] = []

        def boom(*_args, **_kwargs):
            opened.append("open")
            raise AssertionError("socket opened")

        urllib.request.urlopen = boom
        with self.assertRaises(flight.guard.GuardRefused) as caught:
            flight.from_generator(prompt=PROMPT, length_ms=180_000)
        self.assertEqual(caught.exception.code, "activation_closed")
        self.assertEqual(opened, [])
        self.assertFalse(self.desk.store.exists())

    def test_unbound_desk_refuses_before_socket(self) -> None:
        flight.guard.release_test_holder()
        flight.guard._desk = None
        opened: list[str] = []
        urllib.request.urlopen = lambda *_a, **_k: opened.append("open")
        with self.assertRaises(flight.guard.GuardRefused) as caught:
            flight.from_generator(prompt=PROMPT, length_ms=180_000)
        self.assertEqual(caught.exception.code, "unbound_desk")
        self.assertEqual(opened, [])

    def test_one_get_and_one_post_holds_the_lock(self) -> None:
        self.exchange("GET", None)
        status, body, headers = flight.from_generator(prompt=PROMPT, length_ms=180_000)
        self.assertEqual(status, 200)
        self.assertEqual(body, b"audio")
        self.assertEqual([item[0] for item in self.calls], ["GET", "POST"])
        posted = json.loads(self.calls[1][1].decode("utf-8"))
        self.assertEqual(posted["music_length_ms"], 180_000)
        self.assertEqual(posted["model_id"], "music_v2")
        self.assertIs(posted["force_instrumental"], True)
        self.assertNotIn("estimated_credits", posted)
        fd = flight.guard._held_fd
        self.assertIsInstance(fd, int)
        self.assertEqual(os.fstat(fd).st_ino, flight.guard._held_ino)
        self.assertTrue(flight.guard.recorder_held())
        self.assertIn("date", headers)
        self.assertTrue(self.desk.store.is_file())
        self.assertGreater(self.desk.store.stat().st_size, 2)
        reserved = self._reservation()
        self.assertTrue(reserved.is_file())
        record = json.loads(reserved.read_text(encoding="utf-8"))
        self.assertIs(record["reserved"], True)
        self.assertEqual(record["recorder_ino"], flight.guard._held_ino)
        self.assertEqual(record["pinned_store"], "hos009-score-single-use.json")

    def test_client_and_multipart_use_the_same_single_flight(self) -> None:
        self.exchange("GET", None)
        before = []
        real = el_guard.before_spend

        def spy(*args, **kwargs):
            before.append(args)
            return real(*args, **kwargs)

        el_guard.before_spend = spy
        try:
            el_client.request(
                "POST",
                "/v1/music",
                "fixture-token",
                "api_key",
                data={
                    "prompt": PROMPT,
                    "music_length_ms": 180_000,
                    "model_id": "music_v2",
                    "force_instrumental": True,
                },
                query="output_format=mp3_44100_128",
            )
        finally:
            el_guard.before_spend = real
        self.assertEqual(before, [])
        self.assertEqual([item[0] for item in self.calls], ["GET", "POST"])

    def test_multipart_does_not_read_or_post_the_file(self) -> None:
        self.exchange("GET", None, post=b"from-flight")
        missing = self.desk.root / "no-such-upload.mp3"
        status, body = el_client.multipart_post(
            "/v1/music",
            "fixture-token",
            "api_key",
            fields={
                "prompt": PROMPT,
                "music_length_ms": "180000",
                "model_id": "music_v2",
                "force_instrumental": "true",
            },
            files=[("file", missing)],
        )
        self.assertEqual(status, 200)
        self.assertEqual(body, b"from-flight")
        self.assertFalse(missing.exists())
        self.assertEqual([item[0] for item in self.calls], ["GET", "POST"])
        self.assertTrue(self.calls[1][1].startswith(b"{"))

    def test_generator_does_not_call_the_old_client(self) -> None:
        self.exchange("GET", None)

        def banned(*_args, **_kwargs):
            raise AssertionError("generator bypassed the flight")

        real = el_client.request
        el_client.request = banned
        try:
            out = self.desk.root / "bed.mp3"
            meta = generate_music_bed.compose(PROMPT, out, length_ms=180_000)
        finally:
            el_client.request = real
        self.assertEqual(out.read_bytes(), b"audio")
        self.assertEqual(meta["bytes"], len(b"audio"))
        self.assertEqual([item[0] for item in self.calls], ["GET", "POST"])
        source = Path(generate_music_bed.__file__).read_text(encoding="utf-8")
        compose = source.split("def compose", 1)[1].split("def main", 1)[0]
        self.assertNotIn("request(", compose)
        self.assertNotIn("load_token", source)

    def test_refusal_is_one_get_and_no_post(self) -> None:
        self.exchange("GET", None)
        self.desk.pause.write_text("paused", encoding="utf-8")
        with self.assertRaises(flight.guard.GuardRefused) as caught:
            flight.from_client(
                data={
                    "prompt": PROMPT,
                    "music_length_ms": 180_000,
                    "model_id": "music_v2",
                    "force_instrumental": True,
                }
            )
        self.assertEqual(caught.exception.code, "paused")
        self.assertEqual([item[0] for item in self.calls], ["GET"])
        burned = self.desk.store.read_bytes()
        self.assertIn(b"used_requests", burned)
        with self.assertRaises(flight.guard.GuardRefused) as again:
            flight.from_generator(prompt=PROMPT, length_ms=180_000)
        self.assertEqual(again.exception.code, "retry_or_shared_meter")
        self.assertEqual([item[0] for item in self.calls], ["GET"])
        self.assertEqual(self.desk.store.read_bytes(), burned)

    def test_caller_transport_and_paths_are_refused(self) -> None:
        self.exchange("GET", None)
        for kwargs in (
            {"transport": object()},
            {"fetch": lambda: None},
            {"store_path": str(self.desk.store)},
            {"lock_path": str(self.desk.root / "locks" / "elevenlabs.lock")},
            {"desk": str(self.desk.root)},
        ):
            with self.assertRaises(flight.guard.GuardRefused) as caught:
                flight.from_generator(prompt=PROMPT, length_ms=180_000, **kwargs)
            self.assertEqual(caught.exception.code, "caller_supplied_transport")
        with self.assertRaises(flight.guard.GuardRefused):
            flight.from_client(
                data={"prompt": PROMPT, "music_length_ms": 180_000, "model_id": "music_v2", "force_instrumental": True},
                query="output_format=wav",
            )
        self.assertEqual(self.calls, [])

    def test_budget_cannot_be_substituted(self) -> None:
        self.exchange("GET", None)
        with self.assertRaises(flight.guard.GuardRefused) as caught:
            flight.from_client(
                data={
                    "prompt": PROMPT,
                    "music_length_ms": 180_000,
                    "model_id": "music_v2",
                    "force_instrumental": True,
                    "estimated_credits": 1,
                    "cash_gbp": "0",
                }
            )
        self.assertEqual(caught.exception.code, "caller_supplied_transport")
        self.assertEqual(self.calls, [])

    def test_el_guard_off_does_not_weaken_pause_or_open_activation(self) -> None:
        os.environ["EL_GUARD_OFF"] = "1"
        self.assertIs(flight.ACTIVATION_AUTHORIZED, False)
        self.exchange("GET", None)
        self.desk.pause.write_text("paused", encoding="utf-8")
        with self.assertRaises(flight.guard.GuardRefused) as caught:
            flight.from_generator(prompt=PROMPT, length_ms=180_000)
        self.assertEqual(caught.exception.code, "paused")
        self.assertEqual([item[0] for item in self.calls], ["GET"])

    def test_unknown_promo_object_refuses_without_reset(self) -> None:
        self.exchange("GET", None, payload=subscription(bfcm_2026_offer={"nested": True}))
        with self.assertRaises(flight.guard.GuardRefused) as caught:
            flight.from_generator(prompt=PROMPT, length_ms=180_000)
        self.assertEqual(caught.exception.code, "unknown_field")
        self.assertEqual([item[0] for item in self.calls], ["GET"])
        self.assertTrue(self.desk.store.is_file())
        burned = self.desk.store.read_bytes()
        with self.assertRaises(flight.guard.GuardRefused) as again:
            flight.from_generator(prompt=PROMPT, length_ms=180_000)
        self.assertEqual(again.exception.code, "retry_or_shared_meter")
        self.assertEqual(self.desk.store.read_bytes(), burned)

    def test_future_date_refuses_and_does_not_clear_the_store(self) -> None:
        header = formatdate(time.time() + 30, usegmt=True)
        self.exchange("GET", None, header=header)
        with self.assertRaises(flight.guard.GuardRefused) as caught:
            flight.from_generator(prompt=PROMPT, length_ms=180_000)
        self.assertEqual(caught.exception.code, "inconsistent_clock")
        self.assertEqual([item[0] for item in self.calls], ["GET"])
        burned = self.desk.store.read_bytes()
        self.assertGreater(len(burned), 2)
        with self.assertRaises(flight.guard.GuardRefused):
            flight.from_generator(prompt=PROMPT, length_ms=180_000)
        self.assertEqual(self.desk.store.read_bytes(), burned)
        self.assertEqual(len(self.calls), 1)

    def test_same_second_ledger_line_refuses(self) -> None:
        header = fresh_header()
        stamp = parsedate_to_datetime(header).astimezone(timezone.utc).replace(microsecond=0)
        self.desk.ledger.write_text(
            json.dumps({"time": stamp.isoformat(), "status": 200}) + "\n",
            encoding="utf-8",
        )
        self.exchange("GET", None, header=header)
        with self.assertRaises(flight.guard.GuardRefused) as caught:
            flight.from_generator(prompt=PROMPT, length_ms=180_000)
        self.assertEqual(caught.exception.code, "pending_spend")
        self.assertEqual([item[0] for item in self.calls], ["GET"])

    def test_retry_after_success_does_not_get_again(self) -> None:
        self.exchange("GET", None)
        flight.from_generator(prompt=PROMPT, length_ms=180_000)
        with self.assertRaises(flight.guard.GuardRefused) as caught:
            flight.from_generator(prompt=PROMPT, length_ms=180_000)
        self.assertEqual(caught.exception.code, "retry_or_shared_meter")
        self.assertEqual([item[0] for item in self.calls], ["GET", "POST"])

    def test_inode_stays_through_the_post(self) -> None:
        seen: dict[str, int] = {}

        def fake(method: str, body: bytes | None):
            self.calls.append((method, body))
            if method == "POST":
                seen["fd"] = flight.guard._held_fd
                seen["ino"] = os.fstat(flight.guard._held_fd).st_ino
            return 200, lock_header(), subscription() if method == "GET" else b"audio"

        flight._read_one_response = fake
        flight.from_generator(prompt=PROMPT, length_ms=180_000)
        self.assertEqual(seen["ino"], flight.guard._held_ino)
        self.assertEqual(os.fstat(seen["fd"]).st_ino, seen["ino"])
        self.assertEqual(flight.guard._held_fd, seen["fd"])

    def test_second_process_cannot_take_the_lock(self) -> None:
        flight.guard.hold_recorder()
        ino = flight.guard._held_ino
        code = self._child()
        self.assertEqual(code, "shared_meter")
        self.assertEqual(os.fstat(flight.guard._held_fd).st_ino, ino)

    def test_restart_sees_the_burned_store(self) -> None:
        self.exchange("GET", None)
        flight.from_generator(prompt=PROMPT, length_ms=180_000)
        ino = os.fstat(flight.guard._held_fd).st_ino
        code = self._child()
        self.assertEqual(code, "retry_or_shared_meter")
        self.assertEqual(os.fstat(flight.guard._held_fd).st_ino, ino)
        self.assertTrue(self.desk.store.is_file())

    def test_socket_binder_returns_one_response_and_stays_off(self) -> None:
        self.assertIs(flight.ACTIVATION_AUTHORIZED, False)
        seen: list[str] = []

        class Response:
            status = 200
            headers = {"Date": fresh_header()}

            def read(self) -> bytes:
                return b'{"ok":true}'

            def __enter__(self):
                return self

            def __exit__(self, *_args) -> bool:
                return False

        def fake_open(req, timeout=0):
            seen.append(req.full_url)
            self.assertEqual(timeout, 60)
            return Response()

        urllib.request.urlopen = fake_open
        real_token = sys.modules["el_auth"].load_token if "el_auth" in sys.modules else None
        import el_auth

        el_auth.load_token = lambda **_kwargs: ("fixture-key", "api_key")
        try:
            flight.ACTIVATION_AUTHORIZED = True
            status, date, raw = flight._read_one_response("GET", None)
        finally:
            flight.ACTIVATION_AUTHORIZED = False
            if real_token is not None:
                el_auth.load_token = real_token
        self.assertEqual(status, 200)
        self.assertIsInstance(date, str)
        self.assertEqual(raw, b'{"ok":true}')
        self.assertEqual(seen, [flight.SUBSCRIPTION_URL])
        self.assertIs(flight.ACTIVATION_AUTHORIZED, False)

    def test_speech_path_still_uses_the_old_guard(self) -> None:
        seen: list[str] = []

        class Response:
            status = 200
            headers = {"content-type": "application/json"}

            def read(self) -> bytes:
                return b'{"character_limit":1000,"character_count":1}'

            def __enter__(self):
                return self

            def __exit__(self, *_args) -> bool:
                return False

        urllib.request.urlopen = lambda *_a, **_k: Response()
        real = el_guard.before_spend

        def spy(path, data, fetch):
            seen.append(path)
            return real(path, data, fetch)

        el_guard.before_spend = spy
        os.environ["HOS_DESK_DIR"] = str(self.desk.root)
        el_guard.release_lock()
        el_guard._held = False
        el_guard._last.clear()
        try:
            el_client.request("POST", "/v1/text-to-speech/voice", "fixture-token", "api_key", data={"text": "Hi"})
        finally:
            el_guard.before_spend = real
            el_guard.release_lock()
        self.assertEqual(seen, ["/v1/text-to-speech/voice"])

    def test_fragment_and_noncanonical_music_make_no_post(self) -> None:
        """Legacy entries must not POST music variants while the pause bypass is on."""
        os.environ["EL_GUARD_OFF"] = "1"
        previous_desk = os.environ.get("HOS_DESK_DIR")
        os.environ["HOS_DESK_DIR"] = str(self.desk.root)
        self.desk.pause.write_text("paused", encoding="utf-8")
        self.assertIs(flight.ACTIVATION_AUTHORIZED, False)
        posts: list[tuple[str, str]] = []
        spends: list[str] = []

        class Response:
            status = 200
            headers = {}

            def read(self) -> bytes:
                return b"{}"

            def __enter__(self):
                return self

            def __exit__(self, *_args) -> bool:
                return False

        def spy_open(req, **_kwargs):
            posts.append((req.get_method(), req.selector.split("?", 1)[0]))
            return Response()

        real_spend = el_guard.before_spend

        def spy_spend(path, data, fetch):
            spends.append(path)
            return real_spend(path, data, fetch)

        urllib.request.urlopen = spy_open
        el_guard.before_spend = spy_spend
        variants = (
            "/v1/music#fragment",
            "/v1/music#",
            "/v1/music/",
            "/v1/music/extra",
            "/v1/music?other=1",
            "/v1/music?output_format=mp3_44100_128#frag",
            "/v1/music?",
            "/v1/music%23fragment",
            "https://api.elevenlabs.io/v1/music#fragment",
        )
        try:
            for path in variants:
                for entry in ("request", "multipart_post"):
                    before_posts = len(posts)
                    before_spends = len(spends)
                    with self.assertRaises(flight.guard.GuardRefused) as caught:
                        if entry == "request":
                            el_client.request(
                                "POST", path, "fixture", "api_key", data={}, query=""
                            )
                        else:
                            el_client.multipart_post(
                                path, "fixture", "api_key", fields={}, files=[]
                            )
                    self.assertEqual(caught.exception.code, "malformed_request")
                    self.assertEqual(posts[before_posts:], [])
                    self.assertEqual(spends[before_spends:], [])
            with self.assertRaises(flight.guard.GuardRefused) as caught:
                el_client.request(
                    "POST",
                    "/v1/music",
                    "fixture",
                    "api_key",
                    data={},
                    query="output_format=wav",
                )
            self.assertEqual(caught.exception.code, "malformed_request")
            self.assertFalse(any(selector == "/v1/music" for _method, selector in posts))
            self.assertEqual(spends, [])

            el_client.request(
                "POST",
                "/v1/text-to-speech/voice",
                "fixture",
                "api_key",
                data={"text": "Hi"},
            )
            self.assertIn(("POST", "/v1/text-to-speech/voice"), posts)
            self.assertEqual(spends, ["/v1/text-to-speech/voice"])
            upload = self.desk.root / "note.mp3"
            upload.write_bytes(b"fixture")
            el_client.multipart_post(
                "/v1/speech-to-text",
                "fixture",
                "api_key",
                fields={},
                files=[("file", upload)],
            )
            self.assertIn(("POST", "/v1/speech-to-text"), posts)
            self.assertIn("/v1/speech-to-text", spends)
            self.assertFalse(any(selector == "/v1/music" for _method, selector in posts))
        finally:
            el_guard.before_spend = real_spend
            el_guard.release_lock()
            el_guard._last.clear()
            if previous_desk is None:
                os.environ.pop("HOS_DESK_DIR", None)
            else:
                os.environ["HOS_DESK_DIR"] = previous_desk

    def test_failed_transport_reserves_one_read(self) -> None:
        def failed(method: str, body: bytes | None):
            self.calls.append((method, body))
            self.assertEqual(os.fstat(flight.guard._held_fd).st_ino, flight.guard._held_ino)
            raise OSError("synthetic connection failure")

        flight._read_one_response = failed
        with self.assertRaises(OSError):
            flight.from_generator(prompt=PROMPT, length_ms=180_000)
        reserved = self._reservation()
        self.assertTrue(reserved.is_file())
        kept = reserved.read_bytes()
        record = json.loads(kept.decode("utf-8"))
        self.assertEqual(record["recorder_ino"], flight.guard._held_ino)
        self.assertEqual(record["method"], "GET")
        self.assertFalse(self.desk.store.exists())
        self.assertEqual([item[0] for item in self.calls], ["GET"])
        held = flight.guard._held_fd
        ino = flight.guard._held_ino
        with self.assertRaises(flight.guard.GuardRefused) as again:
            flight.from_generator(prompt=PROMPT, length_ms=180_000)
        self.assertEqual(again.exception.code, "read_reserved")
        self.assertEqual([item[0] for item in self.calls], ["GET"])
        self.assertEqual(reserved.read_bytes(), kept)
        self.assertEqual(flight.guard._held_fd, held)
        self.assertEqual(os.fstat(held).st_ino, ino)
        self.assertEqual(self._child(), "read_reserved")
        self.assertEqual([item[0] for item in self.calls], ["GET"])
        self.assertEqual(reserved.read_bytes(), kept)
        self.assertFalse(self.desk.store.exists())

    def test_untrusted_receipt_reserves_one_read(self) -> None:
        def bad(method: str, body: bytes | None):
            self.calls.append((method, body))
            if method != "GET":
                raise AssertionError("music POST")
            return 200, None, b""

        flight._read_one_response = bad
        with self.assertRaises(flight.guard.GuardRefused) as caught:
            flight.from_generator(prompt=PROMPT, length_ms=180_000)
        self.assertEqual(caught.exception.code, "untrusted_receipt")
        kept = self._reservation().read_bytes()
        self.assertFalse(self.desk.store.exists())
        self.assertEqual([item[0] for item in self.calls], ["GET"])
        with self.assertRaises(flight.guard.GuardRefused) as again:
            flight.from_generator(prompt=PROMPT, length_ms=180_000)
        self.assertEqual(again.exception.code, "read_reserved")
        self.assertEqual([item[0] for item in self.calls], ["GET"])
        self.assertEqual(self._reservation().read_bytes(), kept)
        self.assertEqual(self._child(), "read_reserved")
        self.assertEqual([item[0] for item in self.calls], ["GET"])

    def _reservation(self):
        return self.desk.root / "elevenlabs" / flight.READ_ONCE_NAME

    def _child(self) -> str:
        script = (
            "import sys\n"
            "from pathlib import Path\n"
            "sys.path.insert(0, sys.argv[1])\n"
            "import hos009_score_flight as flight\n"
            "flight.guard.bind_desk(Path(sys.argv[2]))\n"
            "try:\n"
            "    flight.from_generator(prompt='lute', length_ms=180000)\n"
            "except flight.guard.GuardRefused as exc:\n"
            "    print(exc.code)\n"
        )
        ran = subprocess.run(
            [sys.executable, "-c", script, str(TOOLS), str(self.desk.root)],
            check=False,
            capture_output=True,
            text=True,
            env={**os.environ, "PYTHONPATH": str(TOOLS)},
        )
        self.assertEqual(ran.returncode, 0, ran.stderr)
        return ran.stdout.strip().splitlines()[-1]


if __name__ == "__main__":
    unittest.main()
