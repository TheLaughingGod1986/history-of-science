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
