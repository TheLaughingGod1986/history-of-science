#!/usr/bin/env python3
"""Offline zero-socket tests for J3171 non-spend methods and GET bodies.

Follows owner-authored HOS Chief ruling 7022847995 after PR 680
(7b87f15ebf6b1a74e7c1eb5df1c5b26fa9e74321, merged at f13cb7ae).
Fixture desks and tokens only. urlopen is mocked and asserted unused on
every refused call.
"""
from __future__ import annotations

import importlib.util
import os
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[3]
spec = importlib.util.spec_from_file_location(
    "flight_fixture_j3171", ROOT / "jobs/reviews/J3150/test_score_flight.py"
)
suite = importlib.util.module_from_spec(spec)
spec.loader.exec_module(suite)

NON_SPEND = (
    "/v1/user/subscription",
    "/v1/user/subscription?unused=1",
    "/v1/history",
    "/v1/history/item",
)
NON_GET = ("PATCH", "PUT", "POST", "DELETE", "HEAD", "OPTIONS", "patch", "post", "delete")


class FakeResponse:
    status = 200
    headers = {"content-type": "application/json"}

    def read(self) -> bytes:
        return b'{"character_limit":100000,"character_count":0}'

    def __enter__(self):
        return self

    def __exit__(self, *_args) -> bool:
        return False


class NonSpendGetOnlyTest(unittest.TestCase):
    def setUp(self) -> None:
        self.desk = suite.Desk()
        self.addCleanup(self.desk.close)
        self.desk.pause.write_text("fixture pause", encoding="utf-8")
        self.assertIs(suite.flight.ACTIVATION_AUTHORIZED, False)

    def _env(self, guard_off: bool) -> dict[str, str]:
        env = {"HOS_DESK_DIR": str(self.desk.root)}
        if guard_off:
            env["EL_GUARD_OFF"] = "1"
        return env

    def assert_refused(
        self,
        entry: str,
        path: str,
        *,
        method: str = "POST",
        data: object = None,
        query: str = "",
        guard_off: bool = True,
    ) -> None:
        with (
            patch.dict(os.environ, self._env(guard_off)),
            patch("urllib.request.urlopen") as transport,
            patch.object(suite.el_guard, "before_spend") as legacy_guard,
            patch.object(suite.flight, "from_client") as flight_client,
            patch.object(suite.flight, "from_multipart") as flight_multipart,
        ):
            if not guard_off:
                os.environ.pop("EL_GUARD_OFF", None)
            with self.assertRaises(suite.flight.guard.GuardRefused) as caught:
                if entry == "request":
                    suite.el_client.request(
                        method,
                        path,
                        "fixture",
                        "api_key",
                        data=data,
                        query=query,
                    )
                else:
                    suite.el_client.multipart_post(
                        path, "fixture", "api_key", fields={}, files=[]
                    )
            self.assertEqual(caught.exception.code, "malformed_request")
            transport.assert_not_called()
            legacy_guard.assert_not_called()
            flight_client.assert_not_called()
            flight_multipart.assert_not_called()
        self.assertTrue(self.desk.pause.is_file())
        self.assertFalse(self.desk.store.exists())

    def test_non_get_on_subscription_and_history_is_refused(self) -> None:
        for path in NON_SPEND:
            for method in NON_GET:
                for data in (None, {}):
                    for guard_off in (True, False):
                        with self.subTest(
                            path=path, method=method, data=data, guard_off=guard_off
                        ):
                            self.assert_refused(
                                "request",
                                path,
                                method=method,
                                data=data,
                                guard_off=guard_off,
                            )
            for guard_off in (True, False):
                with self.subTest(entry="multipart", path=path, guard_off=guard_off):
                    self.assert_refused(
                        "multipart", path, guard_off=guard_off
                    )

    def test_post_subscription_with_query_is_refused(self) -> None:
        self.assert_refused(
            "request",
            "/v1/user/subscription",
            method="POST",
            query="output_format=mp3_44100_128",
        )

    def test_get_with_a_body_is_refused_on_every_path(self) -> None:
        paths = (
            "/v1/user/subscription",
            "/v1/history",
            "/v1/history/item",
            "/v1/music",
            "/v1/text-to-speech/voice",
            "/v1/speech-to-text",
            "/v1/sound-generation",
        )
        bodies = ({}, {"text": "Hi"})
        for path in paths:
            for body in bodies:
                for method in ("GET", "get"):
                    for guard_off in (True, False):
                        with self.subTest(
                            path=path, method=method, guard_off=guard_off
                        ):
                            self.assert_refused(
                                "request",
                                path,
                                method=method,
                                data=body,
                                guard_off=guard_off,
                            )

    def test_bodyless_get_and_guarded_speech_still_behave(self) -> None:
        seen: list[tuple[str, str]] = []

        def fake_open(req, timeout=0):
            seen.append((req.get_method(), req.selector))
            return FakeResponse()

        with (
            patch.dict(os.environ, self._env(True)),
            patch("urllib.request.urlopen", side_effect=fake_open),
        ):
            suite.el_client.request("GET", "/v1/user/subscription", "fixture", "api_key")
            suite.el_client.request("get", "/v1/history", "fixture", "api_key")
            suite.el_client.request(
                "GET",
                "/v1/user/subscription",
                "fixture",
                "api_key",
                query="unused=1",
            )
            suite.el_client.request(
                "POST",
                "/v1/text-to-speech/voice",
                "fixture",
                "api_key",
                data={"text": "Hi"},
            )
        self.assertEqual(
            seen,
            [
                ("GET", "/v1/user/subscription"),
                ("GET", "/v1/history"),
                ("GET", "/v1/user/subscription?unused=1"),
                ("POST", "/v1/text-to-speech/voice"),
            ],
        )

        with (
            patch.dict(os.environ, self._env(False)),
            patch("urllib.request.urlopen") as transport,
        ):
            os.environ.pop("EL_GUARD_OFF", None)
            with self.assertRaises(suite.el_guard.SpendRefused):
                suite.el_client.request(
                    "POST",
                    "/v1/text-to-speech/voice",
                    "fixture",
                    "api_key",
                    data={"text": "Hi"},
                )
            transport.assert_not_called()

        with (
            patch.dict(os.environ, self._env(True)),
            patch("urllib.request.urlopen") as transport,
            patch.object(suite.el_guard, "before_spend") as legacy_guard,
        ):
            with self.assertRaises(suite.flight.guard.GuardRefused) as caught:
                suite.el_client.request(
                    "POST",
                    "/v1/music",
                    "fixture",
                    "api_key",
                    data={
                        "prompt": suite.PROMPT,
                        "music_length_ms": 180_000,
                        "model_id": "music_v2",
                        "force_instrumental": True,
                    },
                )
            self.assertEqual(caught.exception.code, "activation_closed")
            transport.assert_not_called()
            legacy_guard.assert_not_called()
        self.assertFalse(self.desk.store.exists())


if __name__ == "__main__":
    unittest.main()
