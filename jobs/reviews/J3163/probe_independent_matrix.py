#!/usr/bin/env python3
"""Independent offline verification of J3162 routing type repair at faa8f75731a91d50b9ce999a4b80c4fa4562fce9."""
from __future__ import annotations

import hashlib
import importlib.util
import os
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[3]
spec = importlib.util.spec_from_file_location(
    "flight_fixture", ROOT / "jobs/reviews/J3150/test_score_flight.py"
)
assert spec is not None and spec.loader is not None
suite = importlib.util.module_from_spec(spec)
spec.loader.exec_module(suite)


def sha256_file(rel: str) -> str:
    return hashlib.sha256((ROOT / rel).read_bytes()).hexdigest()


EXPECTED_HASHES = {
    "04_Audio/tools/el_client.py": "aabdc7502bf6edcedb735e32427a89046d9794c0cea6c90eabb8d793b9692bb5",
    "04_Audio/tools/hos009_score_flight.py": "43e71321756bc56812264afd64b2946a8222f38c6bea6987376a83a8eafc922d",
    "04_Audio/tools/generate_music_bed.py": "a59f8496a8f285c830468d6dbb4333a9e2f1a12d5808fc6621341f62c62fc597",
    "jobs/reviews/J3150/pinned/score_billing_guard.py": "930d987783055d1f73e80fd9ae770f1ecde63d79b397706df74e9492b4029308",
    "jobs/reviews/J3150/pinned/subscription_shape.json": "ba290b64740c96c3407af17da80d043be3bf840d1863518bfb011e047f9e647e",
}


class SubStr(str):
    pass


class DerivedSubStr(SubStr):
    pass


def main() -> None:
    for rel, expected in EXPECTED_HASHES.items():
        actual = sha256_file(rel)
        assert actual == expected, f"hash mismatch for {rel}: {actual} != {expected}"
    assert suite.flight.ACTIVATION_AUTHORIZED is False
    assert suite.flight.GUARD_SHA256 == EXPECTED_HASHES["jobs/reviews/J3150/pinned/score_billing_guard.py"]
    assert suite.flight.SHAPE_SHA256 == EXPECTED_HASHES["jobs/reviews/J3150/pinned/subscription_shape.json"]

    desk = suite.Desk()
    desk.pause.write_text("fixture pause", encoding="utf-8")
    try:
        non_str_paths = [
            SubStr("/v1/music"),
            SubStr("/v1/music#fragment"),
            SubStr("/v1/music?output_format=mp3_44100_128"),
            SubStr("/v1/text-to-speech/voice"),
            DerivedSubStr("/v1/music"),
            b"/v1/music",
            b"/v1/music#fragment",
            bytearray(b"/v1/music"),
            None,
            0,
            1,
            False,
            True,
            [],
            {},
            Path("/v1/music"),
        ]
        non_str_queries = [
            SubStr(""),
            SubStr("output_format=mp3_44100_128"),
            DerivedSubStr(""),
            b"",
            b"output_format=mp3_44100_128",
            bytearray(b""),
            None,
            0,
            1,
            False,
            True,
            [],
            {},
        ]

        path_refusals = 0
        with patch.dict(
            os.environ, {"EL_GUARD_OFF": "1", "HOS_DESK_DIR": str(desk.root)}
        ), patch("urllib.request.urlopen") as transport, patch.object(
            suite.el_guard, "before_spend"
        ) as legacy:
            for entry in ("request", "multipart_post"):
                for bad_path in non_str_paths:
                    assert suite.el_client._music_route(bad_path) == "reject"
                    try:
                        if entry == "request":
                            suite.el_client.request(
                                "POST", bad_path, "fixture", "api_key", data={}
                            )
                        else:
                            suite.el_client.multipart_post(
                                bad_path, "fixture", "api_key", fields={}, files=[]
                            )
                    except suite.flight.guard.GuardRefused as exc:
                        assert exc.code == "malformed_request", exc.code
                        path_refusals += 1
                    else:
                        raise AssertionError(f"{entry} did not refuse path {bad_path!r}")

            query_refusals = 0
            for base_path in (
                "/v1/music",
                "/v1/music#fragment",
                "/v1/text-to-speech/voice",
                SubStr("/v1/music"),
            ):
                for bad_query in non_str_queries:
                    assert suite.el_client._music_route(base_path, bad_query) == "reject"
                    try:
                        suite.el_client.request(
                            "POST",
                            base_path,
                            "fixture",
                            "api_key",
                            query=bad_query,
                            data={},
                        )
                    except suite.flight.guard.GuardRefused as exc:
                        assert exc.code == "malformed_request", exc.code
                        query_refusals += 1
                    else:
                        raise AssertionError(
                            f"request did not refuse path={base_path!r} query={bad_query!r}"
                        )

            assert transport.call_count == 0
            assert legacy.call_count == 0
            assert not desk.store.exists()
            assert not (desk.root / "elevenlabs" / suite.flight.READ_ONCE_NAME).exists()

        print(f"verified_hashes={len(EXPECTED_HASHES)}")
        print(f"activation_authorized={suite.flight.ACTIVATION_AUTHORIZED}")
        print(f"path_refusals={path_refusals} (entries=2 x paths={len(non_str_paths)})")
        print(f"query_refusals={query_refusals} (base_paths=4 x queries={len(non_str_queries)})")
        print("transport_calls=0 legacy_before_spend_calls=0 live_or_fixture_stores_written=0")
    finally:
        suite.el_guard.release_lock()
        suite.el_guard._last.clear()
        desk.close()


if __name__ == "__main__":
    main()
