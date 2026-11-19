#!/usr/bin/env python3
"""Thin ElevenLabs HTTP helpers (stdlib only)."""
from __future__ import annotations

import json
import mimetypes
import re
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any
from uuid import uuid4

import el_guard
from el_auth import auth_headers

API = "https://api.elevenlabs.io"
_CANONICAL_MUSIC_QUERY = "output_format=mp3_44100_128"
_MUSIC_PREFIX = "/v1/music"
# other is this allow-list only. Sound-generation is not on it.
_OTHER_PREFIXES = (
    "/v1/text-to-speech",
    "/v1/speech-to-speech",
    "/v1/speech-to-text",
    "/v1/user/subscription",
)


def _music_shaped(bare: str) -> bool:
    """True when the path is /v1/music, compared case-insensitively."""
    folded = bare.casefold()
    return folded == _MUSIC_PREFIX or folded.startswith(_MUSIC_PREFIX + "/") or (
        folded.startswith(_MUSIC_PREFIX)
        and len(folded) > len(_MUSIC_PREFIX)
        and not folded[len(_MUSIC_PREFIX)].isalnum()
    )


def _music_route(path: str, query: str = "") -> str:
    """Classify a client path as flight, reject, or other.

    flight is only the exact path /v1/music, with no fragment and with an
    empty query or output_format=mp3_44100_128. A fragment, a trailing slash,
    a suffix, an absolute URL, a case-shifted music path, or any other query
    is reject. other is only a clean speech, Scribe or subscription path.
    """
    # Reject non-built-in strings before legacy dispatch. In particular, a
    # str subclass must not bypass canonical/fragment checks via this branch.
    if type(path) is not str or type(query) is not str:
        return "reject"
    if el_guard.path_is_unsafe(path):
        return "reject"
    had_fragment = "#" in path
    bare = path.split("#", 1)[0]
    had_query = "?" in bare
    in_query = ""
    if had_query:
        bare, in_query = bare.split("?", 1)
    absolute = "://" in bare
    if absolute:
        after = bare.split("://", 1)[1]
        slash = after.find("/")
        bare = after[slash:] if slash >= 0 else "/"
    if not _music_shaped(bare):
        if absolute or not bare.startswith(_OTHER_PREFIXES):
            return "reject"
        return "other"
    if absolute or had_fragment or bare != "/v1/music":
        return "reject"
    if had_query and query:
        return "reject"
    if had_query and in_query == "":
        return "reject"
    effective = in_query if had_query else query
    if effective not in ("", _CANONICAL_MUSIC_QUERY):
        return "reject"
    return "flight"


def _music_flight_query(path: str, query: str = "") -> str | None:
    """Return the query to hand the disabled flight, or None if this is not music.

    A noncanonical music form raises before either legacy entry can send it.
    """
    route = _music_route(path, query)
    if route == "other":
        return None
    if route != "flight":
        from hos009_score_flight import guard

        raise guard.GuardRefused("malformed_request")
    head = path.split("#", 1)[0]
    if "?" in head:
        return head.split("?", 1)[1]
    return query


def request(
    method: str,
    path: str,
    token: str,
    mode: str,
    *,
    data: dict[str, Any] | None = None,
    query: str = "",
    accept: str = "application/json",
    timeout: int = 600,
) -> tuple[int, bytes, dict[str, str]]:
    if method.upper() == "POST":
        routed = _music_flight_query(path, query)
        if routed is not None:
            # Canonical music only. Fragments and other forms already raised.
            from hos009_score_flight import from_client

            return from_client(data=data, query=routed)
    url = f"{API}{path}"
    if query:
        url = f"{url}?{query}"
    spend = el_guard.is_spend(method, path)
    if spend:
        # Lock, pause file, credit floor and ledger (el_guard.py). Raises SpendRefused.
        el_guard.before_spend(
            path,
            data,
            lambda: request("GET", "/v1/user/subscription", token, mode)[:2],
        )
    headers = auth_headers(token, mode, accept=accept)
    body = None
    if data is not None:
        headers["Content-Type"] = "application/json"
        body = json.dumps(data).encode()
    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            result = r.status, r.read(), {k.lower(): v for k, v in r.headers.items()}
    except urllib.error.HTTPError as e:
        result = e.code, e.read(), {k.lower(): v for k, v in e.headers.items()}
    if spend:
        el_guard.after_spend(result[0])
    return result


def multipart_post(
    path: str,
    token: str,
    mode: str,
    *,
    fields: dict[str, str],
    files: list[tuple[str, Path]],
    timeout: int = 600,
) -> tuple[int, bytes]:
    routed = _music_flight_query(path)
    if routed is not None:
        # Do not read the uploaded file and do not nest a subscription GET.
        from hos009_score_flight import from_multipart

        return from_multipart(fields=fields, files=files)
    boundary = f"----orbit{uuid4().hex}"
    chunks: list[bytes] = []
    for name, value in fields.items():
        chunks.append(f"--{boundary}\r\n".encode())
        chunks.append(
            f'Content-Disposition: form-data; name="{name}"\r\n\r\n{value}\r\n'.encode()
        )
    for field_name, file_path in files:
        mime = mimetypes.guess_type(str(file_path))[0] or "application/octet-stream"
        chunks.append(f"--{boundary}\r\n".encode())
        chunks.append(
            (
                f'Content-Disposition: form-data; name="{field_name}"; '
                f'filename="{file_path.name}"\r\n'
                f"Content-Type: {mime}\r\n\r\n"
            ).encode()
        )
        chunks.append(file_path.read_bytes())
        chunks.append(b"\r\n")
    chunks.append(f"--{boundary}--\r\n".encode())
    body = b"".join(chunks)
    spend = el_guard.is_spend("POST", path)
    if spend:
        # Same lock, pause file, floor and ledger as request() (el_guard.py). Raises SpendRefused.
        el_guard.before_spend(
            path,
            None,
            lambda: request("GET", "/v1/user/subscription", token, mode)[:2],
        )
    headers = auth_headers(token, mode, accept="application/json")
    headers["Content-Type"] = f"multipart/form-data; boundary={boundary}"
    req = urllib.request.Request(
        f"{API}{path}", data=body, headers=headers, method="POST"
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            result = r.status, r.read()
    except urllib.error.HTTPError as e:
        result = e.code, e.read()
    if spend:
        el_guard.after_spend(result[0])
    return result


def slugify(text: str, *, max_len: int = 48) -> str:
    out = re.sub(r"[^a-zA-Z0-9]+", "-", text.strip().lower()).strip("-")
    return (out or "clip")[:max_len]
