#!/usr/bin/env python3
"""Tests for el_guard (no network). Run: python3 04_Audio/tools/test_el_guard.py"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import el_guard  # noqa: E402


def sub(left: int, limit: int = 209_536):
    body = json.dumps({"character_limit": limit, "character_count": limit - left}).encode()
    return lambda: (200, body)


class GuardTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        os.environ["HOS_DESK_DIR"] = self.tmp.name
        os.environ.pop("EL_GUARD_OFF", None)
        os.environ.pop("EL_CREDIT_FLOOR", None)
        el_guard.release_lock()
        el_guard._held = False
        el_guard._last.clear()

    def tearDown(self):
        el_guard.release_lock()
        self.tmp.cleanup()

    def test_spend_paths(self):
        self.assertTrue(el_guard.is_spend("POST", "/v1/text-to-speech/abc/with-timestamps"))
        self.assertFalse(el_guard.is_spend("GET", "/v1/user/subscription"))
        self.assertTrue(el_guard.is_spend("POST", "/v1/speech-to-text"))  # Scribe bills the pool too
        self.assertFalse(el_guard.is_spend("GET", "/v1/history"))

    def test_spend_logs_to_ledger_and_holds_lock(self):
        el_guard.before_spend("/v1/text-to-speech/x", {"text": "hello world"}, sub(90_000))
        self.assertTrue(el_guard.lock_path().exists())
        el_guard.after_spend(200)
        rows = [json.loads(l) for l in el_guard.ledger_path().read_text().splitlines()]
        self.assertEqual(rows[0]["chars"], 11)
        self.assertEqual(rows[0]["left_before"], 90_000)
        self.assertEqual(rows[0]["status"], 200)

    def test_floor_refuses(self):
        with self.assertRaises(el_guard.SpendRefused):
            el_guard.before_spend("/v1/text-to-speech/x", {"text": "a" * 2000}, sub(51_000))

    def test_floor_override(self):
        os.environ["EL_CREDIT_FLOOR"] = "1000"
        el_guard.before_spend("/v1/text-to-speech/x", {"text": "a" * 2000}, sub(51_000))

    def test_pause_file_refuses(self):
        el_guard.pause_path().parent.mkdir(parents=True, exist_ok=True)
        el_guard.pause_path().write_text("paused")
        with self.assertRaises(el_guard.SpendRefused):
            el_guard.before_spend("/v1/text-to-speech/x", {"text": "hi"}, sub(90_000))

    def test_unreadable_balance_refuses(self):
        with self.assertRaises(el_guard.SpendRefused):
            el_guard.before_spend("/v1/text-to-speech/x", {"text": "hi"}, lambda: (500, b""))

    def test_second_live_recorder_refused(self):
        # A live process on this host holds the lock.
        holder = subprocess.Popen([sys.executable, "-c", "import time; time.sleep(30)"])
        try:
            p = el_guard.lock_path()
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(json.dumps({"pid": holder.pid, "host": __import__("socket").gethostname(),
                                     "script": "other.py", "started": "now"}))
            with self.assertRaises(el_guard.SpendRefused) as cm:
                el_guard.before_spend("/v1/text-to-speech/x", {"text": "hi"}, sub(90_000))
            self.assertIn("other.py", str(cm.exception))
        finally:
            holder.kill()
            holder.wait()

    def test_stale_lock_taken_over(self):
        dead = subprocess.Popen([sys.executable, "-c", "pass"])
        dead.wait()
        p = el_guard.lock_path()
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps({"pid": dead.pid, "host": __import__("socket").gethostname()}))
        el_guard.before_spend("/v1/text-to-speech/x", {"text": "hi"}, sub(90_000))
        self.assertEqual(json.loads(p.read_text())["pid"], os.getpid())

    def test_release_removes_own_lock(self):
        el_guard.acquire_lock()
        el_guard.release_lock()
        self.assertFalse(el_guard.lock_path().exists())



class MultipartGuardTest(unittest.TestCase):
    def test_scribe_upload_goes_through_the_guard(self):
        import el_client

        seen = []

        def refuse(path, data, fetch):
            seen.append(path)
            raise el_guard.SpendRefused("test")

        real = el_guard.before_spend
        el_guard.before_spend = refuse
        try:
            with tempfile.NamedTemporaryFile(suffix=".mp3") as f:
                with self.assertRaises(el_guard.SpendRefused):
                    el_client.multipart_post("/v1/speech-to-text", "tok", "api_key", fields={}, files=[("file", Path(f.name))])
        finally:
            el_guard.before_spend = real
        self.assertEqual(seen, ["/v1/speech-to-text"])


if __name__ == "__main__":
    unittest.main()
