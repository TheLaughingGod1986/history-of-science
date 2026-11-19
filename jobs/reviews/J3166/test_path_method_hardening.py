#!/usr/bin/env python3
"""Offline fixture zero-transport tests for J3166 path and method hardening.

Follows owner-authored HOS Chief ruling 7022139984 after PR 675 (d1f9e545).
Fixture desks and tokens only; urlopen is mocked and asserted unused on all
rejected and disabled-flight paths.
"""
from __future__ import annotations

import importlib.util
import os
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[3]
spec = importlib.util.spec_from_file_location(
    "flight_fixture_j3166", ROOT / "jobs/reviews/J3150/test_score_flight.py"
)
suite = importlib.util.module_from_spec(spec)
spec.loader.exec_module(suite)


class ClientString(str):
    pass


class FakeResponse:
    status = 200
    headers = {"content-type": "application/json"}

    def read(self) -> bytes:
        return b'{"character_limit":100000,"character_count":0}'

    def __enter__(self):
        return self

    def __exit__(self, *_args) -> bool:
        return False


class PathAndMethodHardeningTest(unittest.TestCase):
    def setUp(self) -> None:
        self.desk = suite.Desk()
        self.addCleanup(self.desk.close)
        self.desk.pause.write_text("fixture pause", encoding="utf-8")
        self.assertIs(suite.flight.ACTIVATION_AUTHORIZED, False)

    def assert_refused_zero_transport(
        self,
        entry: str,
        path: object,
        *,
        method: object = "POST",
        guard_off: bool = True,
        query: str = "",
    ) -> None:
        env = {"HOS_DESK_DIR": str(self.desk.root)}
        if guard_off:
            env["EL_GUARD_OFF"] = "1"
        with (
            patch.dict(os.environ, env),
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
                        method, path, "fixture", "api_key", data={}, query=query
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

    def test_semicolon_paths_rejected_with_zero_transport(self) -> None:
        paths = (
            "/v1/text-to-speech/..;/music",
            "/v1/text-to-speech/..;/music?output_format=mp3_44100_128",
            "/v1/music;param",
            "/v1/text-to-speech/voice;param",
            "/v1/speech-to-text;foo",
        )
        for path in paths:
            self.assertTrue(suite.el_guard.path_is_unsafe(path), path)
            self.assertEqual(suite.el_client._music_route(path), "reject", path)
            self.assertTrue(suite.el_guard.is_spend("POST", path), path)
            self.assertTrue(suite.el_guard.is_spend("PUT", path), path)
            self.assertFalse(suite.el_guard.is_spend("GET", path), path)
            for guard_off in (True, False):
                for entry in ("request", "multipart_post"):
                    with self.subTest(entry=entry, path=path, guard_off=guard_off):
                        self.assert_refused_zero_transport(
                            entry, path, guard_off=guard_off
                        )

    def test_noncanonical_music_methods_rejected_before_flight_guard_and_urlopen(
        self,
    ) -> None:
        methods = (
            "PUT",
            "PATCH",
            "DELETE",
            "HEAD",
            "OPTIONS",
            "put",
            "patch",
            "delete",
            " POST",
            "POST ",
            "\tPOST",
            "POST\n",
            " post",
            "PO ST",
            " PUT",
            " GET",
            "GET ",
            "",
            "   ",
            None,
            b"POST",
            ClientString("POST"),
            ClientString("GET"),
        )
        paths_and_queries = (
            ("/v1/music", ""),
            ("/v1/music", "output_format=mp3_44100_128"),
            ("/V1/MUSIC", ""),
            ("/v1/music/extra", ""),
            ("/v1/text-to-speech/..;/music", ""),
        )
        for method in methods:
            self.assertTrue(
                suite.el_guard.is_spend(method, "/v1/music"), repr(method)
            )
            for path, query in paths_and_queries:
                for guard_off in (True, False):
                    with self.subTest(
                        method=repr(method),
                        path=path,
                        query=query,
                        guard_off=guard_off,
                    ):
                        self.assert_refused_zero_transport(
                            "request",
                            path,
                            method=method,
                            guard_off=guard_off,
                            query=query,
                        )

    def test_canonical_post_music_stays_on_disabled_guarded_flight(self) -> None:
        payload = {
            "prompt": suite.PROMPT,
            "music_length_ms": 180_000,
            "model_id": "music_v2",
            "force_instrumental": True,
        }
        for method in ("POST", "post"):
            for query in ("", "output_format=mp3_44100_128"):
                with self.subTest(method=method, query=query):
                    fresh_desk = suite.Desk()
                    try:
                        fresh_desk.pause.write_text("fixture pause", encoding="utf-8")
                        env = {
                            "HOS_DESK_DIR": str(fresh_desk.root),
                            "EL_GUARD_OFF": "1",
                        }
                        with (
                            patch.dict(os.environ, env),
                            patch("urllib.request.urlopen") as transport,
                            patch.object(suite.el_guard, "before_spend") as legacy_guard,
                        ):
                            with self.assertRaises(suite.flight.guard.GuardRefused) as caught:
                                suite.el_client.request(
                                    method,
                                    "/v1/music",
                                    "fixture",
                                    "api_key",
                                    data=payload,
                                    query=query,
                                )
                            self.assertEqual(caught.exception.code, "activation_closed")
                            transport.assert_not_called()
                            legacy_guard.assert_not_called()
                        self.assertFalse(fresh_desk.store.exists())
                    finally:
                        fresh_desk.close()

    def test_clean_non_music_requests_and_get_behavior_preserved(self) -> None:
        seen: list[tuple[str, str]] = []

        def fake_open(req, timeout=0):
            seen.append((req.get_method(), req.selector))
            return FakeResponse()

        env = {"HOS_DESK_DIR": str(self.desk.root), "EL_GUARD_OFF": "1"}
        with patch.dict(os.environ, env), patch("urllib.request.urlopen", side_effect=fake_open):
            suite.el_client.request("GET", "/v1/user/subscription", "fixture", "api_key")
            suite.el_client.request("get", "/v1/user/subscription", "fixture", "api_key")
            suite.el_client.request(
                "POST", "/v1/text-to-speech/voice", "fixture", "api_key", data={"text": "Hi"}
            )
            suite.el_client.request("GET", "/v1/music", "fixture", "api_key")
        self.assertEqual(
            seen,
            [
                ("GET", "/v1/user/subscription"),
                ("GET", "/v1/user/subscription"),
                ("POST", "/v1/text-to-speech/voice"),
                ("GET", "/v1/music"),
            ],
        )
        self.assertFalse(suite.el_guard.is_spend("GET", "/v1/music"))
        self.assertFalse(suite.el_guard.is_spend("GET", "/v1/user/subscription"))


if __name__ == "__main__":
    unittest.main()
