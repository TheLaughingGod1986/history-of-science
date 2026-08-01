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
    headers = auth_headers(token, mode, accept=accept)
    body = None
    if data is not None:
        headers["Content-Type"] = "application/json"
        body = json.dumps(data).encode()
    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status, r.read(), {k.lower(): v for k, v in r.headers.items()}
    except urllib.error.HTTPError as e:
        return e.code, e.read(), {k.lower(): v for k, v in e.headers.items()}


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
    headers = auth_headers(token, mode, accept="application/json")
    headers["Content-Type"] = f"multipart/form-data; boundary={boundary}"
    req = urllib.request.Request(
        f"{API}{path}", data=body, headers=headers, method="POST"
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status, r.read()
    except urllib.error.HTTPError as e:
        return e.code, e.read()


def slugify(text: str, *, max_len: int = 48) -> str:
    out = re.sub(r"[^a-zA-Z0-9]+", "-", text.strip().lower()).strip("-")
    return (out or "clip")[:max_len]
