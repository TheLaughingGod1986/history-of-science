#!/usr/bin/env python3
"""Shared ElevenLabs auth for Orbit audio tooling.

Prefers ELEVENLABS_API_KEY, then Firebase bearer from known cache paths /
Playwright IndexedDB (same pattern as per-project VO generators).
"""
from __future__ import annotations

import base64
import json
import os
import re
import time
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]


def _jwt_exp(tok: str) -> float:
    try:
        payload = tok.split(".")[1]
        pad = "=" * (-len(payload) % 4)
        pl = json.loads(base64.urlsafe_b64decode(payload + pad))
        return float(pl.get("exp", 0))
    except Exception:
        return 0.0


def _bearer_candidates(extra: list[Path] | None = None) -> list[Path]:
    paths = [
        Path("/tmp/elevenlabs_bearer.txt"),
        REPO
        / "02_Video-Projects/003_Exoplanets-Strangest-Alien-Worlds/02_Voiceover/.elevenlabs_bearer",
        REPO
        / "02_Video-Projects/004_JWST-Discoveries-That-Change-Everything/02_Voiceover/.elevenlabs_bearer",
        REPO
        / "02_Video-Projects/002_What-Happens-If-You-Fall-Into-A-Black-Hole/02_Voiceover/.elevenlabs_bearer",
    ]
    if extra:
        paths = list(extra) + paths
    return paths


def _from_indexeddb() -> str | None:
    sources = [
        Path(
            "/Users/ben/code/youtube/.playwright-elevenlabs-profile/Default/IndexedDB/"
            "https_elevenlabs.io_0.indexeddb.leveldb"
        ),
        Path.home()
        / "Library/Application Support/Google/Chrome/Default/IndexedDB/"
        / "https_elevenlabs.io_0.indexeddb.leveldb",
    ]
    now = time.time()
    best: tuple[float, str] | None = None
    for p in sources:
        if not p.exists():
            continue
        blob = b"".join(f.read_bytes() for f in p.glob("*") if f.is_file())
        for raw in set(
            re.findall(
                rb"eyJ[A-Za-z0-9_\-]{20,}\.[A-Za-z0-9_\-]{20,}\.[A-Za-z0-9_\-]{10,}",
                blob,
            )
        ):
            tok = raw.decode()
            exp = _jwt_exp(tok)
            if exp > now + 30 and (best is None or exp > best[0]):
                best = (exp, tok)
    if best:
        Path("/tmp/elevenlabs_bearer.txt").write_text(best[1] + "\n")
        return best[1]
    return None


def load_token(
    *,
    extra_bearer_paths: list[Path] | None = None,
    prefer_api_key: bool = False,
) -> tuple[str, str]:
    """Return (token, mode) where mode is 'api_key' or 'bearer'."""
    env_key = os.environ.get("ELEVENLABS_API_KEY", "").strip()
    key_file = Path(
        os.environ.get(
            "ELEVENLABS_API_KEY_FILE",
            str(Path.home() / ".config/elevenlabs/api_key"),
        )
    ).expanduser()
    file_key = ""
    if key_file.exists():
        file_key = key_file.read_text(encoding="utf-8").strip()

    api_key = env_key or file_key
    if api_key and (prefer_api_key or not _looks_like_jwt(api_key)):
        if api_key.startswith("sk_"):
            return api_key, "api_key"

    if prefer_api_key and not (api_key and api_key.startswith("sk_")):
        raise SystemExit(
            "ELEVENLABS_API_KEY required (same key as ElevenLabs MCP). "
            f"Set env or write sk_… to {key_file}"
        )

    if env_key and env_key.startswith("sk_"):
        return env_key, "api_key"
    if file_key and file_key.startswith("sk_"):
        return file_key, "api_key"

    now = time.time()
    for f in _bearer_candidates(extra_bearer_paths):
        if not f.exists():
            continue
        tok = f.read_text().strip()
        if tok and _jwt_exp(tok) > now + 30:
            return tok, "bearer"

    tok = _from_indexeddb()
    if tok:
        return tok, "bearer"

    raise SystemExit(
        "No ElevenLabs credentials — set ELEVENLABS_API_KEY / "
        f"{key_file} (MCP key) or refresh elevenlabs.io session."
    )


def _looks_like_jwt(tok: str) -> bool:
    return tok.count(".") >= 2 and tok.startswith("eyJ")


def auth_headers(token: str, mode: str, *, accept: str = "application/json") -> dict[str, str]:
    headers = {"Accept": accept}
    if mode == "api_key":
        headers["xi-api-key"] = token
    else:
        headers["Authorization"] = f"Bearer {token}"
    return headers
