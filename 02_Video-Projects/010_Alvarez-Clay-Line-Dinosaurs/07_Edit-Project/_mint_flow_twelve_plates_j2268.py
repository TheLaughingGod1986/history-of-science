#!/usr/bin/env python3
"""HOS 010 Alvarez clay line twelve-plate Flow adapter (J2268).

Consumes ONLY the bounded 12-plate scope in
`02_Video-Projects/010_Alvarez-Clay-Line-Dinosaurs/10_Shorts/TWELVE_PLATE_SCOPE_J2267.json`
(12 Quality parent plates for Short A and Short C, 10 shared with the long film
plus 2 Shorts-only bird plates `P5:09a_pigeon_pavement` and `P5:13a_gull_seaside`).

Built on the J2200 shared Flow accounting guards and the repaired HOS 009 / 013
runners (history-of-science #445, #468, #470, #477, #480). Never imports, modifies,
or delegates to any legacy auto-KEEP runner. Every generated take is recorded as
`file_state="GENERATED"`, `status="PENDING_REVIEW"`, `review="PENDING_REVIEW"`,
`keep=False` — never `KEEP`.

Default commands (`plan`, `dry-run`, `detach-command`) never open Chrome/CDP,
never click Create, never modify NAS media, and spend 0 credits (£0).
`submit` is interlocked behind BOTH:
  1. `HOS010_TWELVE_PLATES_SUBMIT=1` in the environment, AND
  2. Explicit elected-Chief spend authorization (J2269 after HOS 009 J2033 DONE),
     verified via `generation_authorized: true` in `TWELVE_PLATE_SCOPE_J2267.json`
     or a signed-off `--authorization-file` pinning the exact scope SHA-256 and
     authorized credit cap (`<= 3600`). Self-authorization is refused.

Core J2267 / J2268 / J2200 guards:
- Exact 12-row allowlist (`TWELVE_PLATE_SCOPE_J2267.json`), cross-checked against
  `02_Shot-List/PICTURE_PLAN_v04.json`, `10_Shorts/SHORTS_PICTURE_PLAN_v03.json`,
  `10_Shorts/J2267_BUDGET_RECONCILIATION.json`, and all 5 part boards
  (`part-01..04_plates_v03.json`, `part-05_plates_v04.json`).
- Accepted Short A / Short C VO hashes (`hos_010_short_A_v02.{mp3,wav}`,
  `hos_010_short_C_v02.{mp3,wav}`), locked long VO (`VO_TAKES_KEEP.json`), and
  J1004 Option A1 assembly audio recipe (`6` silence removals totaling `0.260s`,
  hook `1.06`, body `1.0`, `body_shift_s = -0.431`, `vo_duration_s = 22.289`,
  `hook_sentence_end_s = 2.849`, `rendered = false`) verified before any run.
- Explorer character reference (`01_Character/05_Generation-References/hos-explorer-reference-v01.jpg`)
  decoded and SHA-256-verified, attached ONLY on `P5:10_explorer_robin`, and
  refused on any frame-0 plate. Canonical house `_style_refs` verified 16:9 HD
  before any 0-credit `Nano Banana 2.1` start still.
- Studio Ultra account verified on `flow.google.com` by SHA-256 digest (no
  personal email address stored in code or receipts) + `ULTRA` entitlement.
- Exact model & price per take: `Veo 3.1 - Quality`, `8s`, `16:9`, `x1`,
  `100` credits/take (`Nano Banana 2.1`, `16:9`, `x1`, `0` credits for missing
  start stills). No Omni, no `x2`, no Fast substitution, no paid overage.
- Caps: max `3` takes/row, max `3600` total credits (or lower J2269 authorized
  cap), `<= 5` rows and `<= 1500` credits per batch, and `3000`-credit minimum
  headroom floor after reserving the full remaining cap, pending/unposted
  charges, and non-overlapping external reservations (never double-counting
  own reservations or stale `reserved_flow_expected` planning estimates).
- Exclusive shared Flow writer lock (`~/_desk/state/flow/shared/writer.lock`),
  durable `account.jsonl` reservation/intent/resolution/reconciliation,
  duplicate-process PID + flock refusal, `cdp_tabs.reuse_page`, silent 8s 16:9
  decode check, and SHA-256-verified immutable NAS archive copies + receipts.
- A take Flow refuses under its content policy is closed with
  `reconcile-policy-refusal`: `FAILED_POLICY`, `0` credits, no output. It still
  uses one of the row's `3` takes and its number is never used again. The row is
  set aside until its prompt changes: a refused prompt is not sent twice.
"""
from __future__ import annotations

import argparse
import fcntl
import hashlib
import inspect
import json
import math
import os
import re
import shlex
import subprocess
import sys
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

# Account verification reads STUDIO_FLOW_ACCOUNT outside the repo (no email address stored in repo or receipts).
ACCOUNT_ENV = "STUDIO_FLOW_ACCOUNT"
FORBIDDEN_ACCOUNT_ENV = "STUDIO_FLOW_FORBIDDEN_ACCOUNT"
REQUIRED_ACCOUNT_SHA256: str | None = None
FORBIDDEN_ACCOUNT_SHA256 = "93b0f97ef00986fa90ead10a83be910d43707ddc8023daa2018ed1d95cbbb9d4"

FILM_ID = "HOS:010"
FILM_NUM = "010"
FILM_FOLDER = "010_Alvarez-Clay-Line-Dinosaurs"
JOB_ID = "J2268"
SCOPE_JOB_ID = "J2267"
AUTH_JOB_ID = "J2269"
PRODUCER_JOB_ID = "J2270"
PRIOR_HOS009_JOB_ID = "J2033"

EXPECTED_ROW_COUNT = 12
EXPECTED_SHARED_LONG_COUNT = 10
EXPECTED_SHORTS_ONLY_COUNT = 2
EXPECTED_EXPLORER_ROW_ID = "P5:10_explorer_robin"
EXPECTED_SHORTS_ONLY_IDS = ("P5:09a_pigeon_pavement", "P5:13a_gull_seaside")
EXPECTED_ROW_IDS = (
    "P1:01_clay_line",
    "P2:01_walter_hammer",
    "P2:03_tiny_shells",
    "P2:05_almost_none",
    "P3:08_asaro_michel",
    "P4:06_dust_veil",
    "P5:08_all_at_once",
    "P5:09_robin",
    "P5:10_explorer_robin",
    "P5:12_clay_callback",
    "P5:09a_pigeon_pavement",
    "P5:13a_gull_seaside",
)

REQUIRED_QUALITY = "Quality"
REQUIRED_MODEL = "Veo 3.1 - Quality"
REQUIRED_STILL_MODEL = "Nano Banana 2.1"
REQUIRED_OUTPUTS = "x1"
REQUIRED_ASPECT = "16:9"
REQUIRED_DURATION = "8s"
REQUIRED_CLIP_S = 8
MAX_CREDITS_PER_TAKE = 100
MAX_TAKES_PER_ROW = 3
TRY1_TOTAL_CREDITS = 1200
MAX_TOTAL_CREDITS = 3600
MAX_BATCH_ROWS = 5
MAX_BATCH_CREDITS = 1500
HEADROOM_FLOOR = 3000

SUBMIT_ENV = "HOS010_TWELVE_PLATES_SUBMIT"
# A take Flow refused under its content policy: no output and no credits (Chief rulings on J2033,
# desk 6784299215, 6785508086 and 6785808071; for 010, desk 6786709657 item 2). It uses one of
# the row's takes. The row is set aside until its prompt changes, then goes on at the next take.
POLICY_REFUSED = "FAILED_POLICY"
DEFAULT_RESERVATION = "HOS010_TWELVE_PLATES_J2270"
FLOW_HOST = "flow.google.com"
GENERATE_LINE_RE = re.compile(r"^Generating will use (\d+) credits$")

FILM_REL = Path("02_Video-Projects/010_Alvarez-Clay-Line-Dinosaurs")
EDIT_REL = FILM_REL / "07_Edit-Project"
SHORTS_REL = FILM_REL / "10_Shorts"
SCOPE_REL = SHORTS_REL / "TWELVE_PLATE_SCOPE_J2267.json"
RECONCILIATION_REL = SHORTS_REL / "J2267_BUDGET_RECONCILIATION.json"
SHORTS_PLAN_REL = SHORTS_REL / "SHORTS_PICTURE_PLAN_v03.json"
LONG_PLAN_REL = FILM_REL / "02_Shot-List/PICTURE_PLAN_v04.json"
VO_KEEP_REL = FILM_REL / "02_Voiceover/VO_TAKES_KEEP.json"
EXPLORER_REF_REL = Path("01_Character/05_Generation-References/hos-explorer-reference-v01.jpg")
EXPLORER_REF_SHA256 = "24659dc1d761e9371de9411ca8b56cd5ad3e2587674a8cbdf66a3b84e451476d"

CANONICAL_HOUSE_STYLE_REFS = (
    (
        "04_Generated-Clips/_style_refs/04_sunny_window_v01.jpg",
        "cdb8b421fa121454bb62d9b6dfc1c782c7c95b1634d80c856bb95555cfdc4b45",
    ),
    (
        "04_Generated-Clips/_style_refs/10_mint_jar_v01.jpg",
        "311fe7b886f391eaabe32aabc0be1b1989e483dd814237c7095e3a118d423720",
    ),
)

EXPECTED_VO_KEEP_SHA256 = "e0640417c27b88d0221d325d0dfe13304e8dd69f738b0bcfaeeb90f263092f39"
EXPECTED_SHORT_A_MP3_SHA256 = "68d88b5b5883f2376bcec29c26d77efea7634d5c7705693f41202ca587b927fb"
EXPECTED_SHORT_A_WAV_SHA256 = "2488aa8b49beb3a642597e08f30ca53e723fbee00cd21ad8bdc581a9293ff228"
EXPECTED_SHORT_C_MP3_SHA256 = "20432ecd645b28e9fdc051578a284cb2845bd09f3040170b192089b256055b87"
EXPECTED_SHORT_C_WAV_SHA256 = "ca814ab01ad72fde015b4e157638b5e346d592e5df54cefe97e38969340fcb0c"

EXPECTED_OPTION_A1_SILENCES = (
    (0.0, 0.08),
    (0.64, 0.68),
    (1.08, 1.1),
    (1.44, 1.5),
    (1.98, 2.0),
    (2.42, 2.46),
)
EXPECTED_OPTION_A1_SILENCE_SUM_S = 0.26
EXPECTED_OPTION_A1_HOOK_SPEED = 1.06
EXPECTED_OPTION_A1_BODY_SPEED = 1.0
EXPECTED_OPTION_A1_BODY_SHIFT_S = -0.431
EXPECTED_SHORT_A_VO_DUR_S = 22.289
EXPECTED_SHORT_A_HOOK_END_S = 2.849
EXPECTED_SHORT_C_VO_DUR_S = 22.56
EXPECTED_SHORT_C_HOOK_END_S = 1.78

DEFAULT_NAS_MEDIA = Path(
    "/Volumes/data/studio-live/History Of Science/02_Video-Projects/010_Alvarez-Clay-Line-Dinosaurs"
)

EXPLORER_LOCK = (
    "Exactly ONE Explorer: young boy, messy brown hair, round thin gold glasses, "
    "teal long coat, tan vest, brown bow tie, satchel. Acts then leaves."
)


class GuardError(RuntimeError):
    """A credit, scope, authorization, lock, style-ref, VO, account or status rule refused the run."""


@dataclass(frozen=True)
class Row:
    index: int
    row_id: str
    part: int
    plate_id: str
    board: str
    board_sha256: str
    quality: str
    flow_model: str
    max_takes: int
    try1_credits: int
    planning_cap: int
    flow_clip_s: int
    t_s: float | None
    long_use_s: float
    max_short_use_s: float
    required_decode_s: float
    shorts_only: bool
    explorer: bool
    reference: str
    uses: tuple[dict, ...]
    prompt: str
    prompt_sha256: str
    normalized_prompt_sha256: str

    @property
    def key(self) -> tuple[int, str]:
        return (self.part, self.plate_id)


@dataclass(frozen=True)
class PriceEvidence:
    quality: str
    model: str
    outputs: str
    aspect: str
    duration: str
    credits: int
    generate_line: str
    read_at: str


@dataclass(frozen=True)
class GenerationAuthorization:
    job: str
    film: str
    scope_sha256: str
    authorized_cap_credits: int
    minimum_headroom_floor: int
    j2033_done: bool
    source: str


def repo_root_from(start: Path | None = None) -> Path:
    here = start or Path(__file__).resolve()
    for parent in [here, *here.parents]:
        if (parent / "AGENTS.md").exists() and (parent / EDIT_REL).exists():
            return parent
    env = os.environ.get("HOS_REPO")
    if env:
        return Path(env)
    return Path(__file__).resolve().parents[3]


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def account_sha256(account: str | None) -> str:
    if not isinstance(account, str) or not account.strip():
        return ""
    return sha256_bytes(account.strip().lower().encode("utf-8"))


def forbidden_account_sha256() -> str:
    raw = os.environ.get(FORBIDDEN_ACCOUNT_ENV, "").strip().lower()
    if raw:
        return account_sha256(raw)
    return (FORBIDDEN_ACCOUNT_SHA256 or "").strip().lower()


def required_account_sha256() -> str:
    if isinstance(REQUIRED_ACCOUNT_SHA256, str) and REQUIRED_ACCOUNT_SHA256.strip():
        digest = REQUIRED_ACCOUNT_SHA256.strip().lower()
    else:
        raw = os.environ.get(ACCOUNT_ENV, "").strip().lower()
        if not raw:
            raise GuardError(
                f"missing required setting {ACCOUNT_ENV} (set {ACCOUNT_ENV} outside the repo)"
            )
        digest = account_sha256(raw)
    forbidden = forbidden_account_sha256()
    if digest == FORBIDDEN_ACCOUNT_SHA256 or (forbidden and digest == forbidden):
        raise GuardError("Flow account is not the studio Ultra account")
    return digest


def verify_account_list(accounts: object) -> str:
    expected = required_account_sha256()
    forbidden = forbidden_account_sha256()
    if not isinstance(accounts, list) or len(accounts) != 1 or not isinstance(accounts[0], str):
        raise GuardError("live Flow account is missing or ambiguous")
    digest = account_sha256(accounts[0])
    if digest == FORBIDDEN_ACCOUNT_SHA256 or (forbidden and digest == forbidden) or digest != expected:
        raise GuardError("Flow account is not the studio Ultra account")
    return expected


def expected_model_for(row_or_quality: Row | str) -> str:
    quality = row_or_quality.quality if isinstance(row_or_quality, Row) else str(row_or_quality)
    if quality != REQUIRED_QUALITY:
        raise GuardError(f"unsupported row quality {quality!r}; HOS 010 twelve-plate scope is Quality only")
    return REQUIRED_MODEL


def expected_credits_for(row_or_quality: Row | str) -> int:
    expected_model_for(row_or_quality)
    return MAX_CREDITS_PER_TAKE


def verify_vo_and_option_a1(repo: Path, media: Path | None = None, *, require_audio_files: bool = False) -> dict:
    """Verify locked long VO, accepted Short A/C VO hashes, and J1004 Option A1 recipe."""
    vo_keep_path = repo / VO_KEEP_REL
    if not vo_keep_path.is_file():
        raise GuardError(f"missing locked long VO manifest: {vo_keep_path}")
    vo_keep_sha = sha256_file(vo_keep_path)
    if vo_keep_sha != EXPECTED_VO_KEEP_SHA256:
        raise GuardError(f"VO_TAKES_KEEP.json sha256 drift: {vo_keep_sha} != {EXPECTED_VO_KEEP_SHA256}")
    vo_keep = json.loads(vo_keep_path.read_text())
    if vo_keep.get("film") != FILM_NUM or not str(vo_keep.get("status") or "").startswith("LOCKED v01"):
        raise GuardError("VO_TAKES_KEEP.json is not LOCKED v01 for film 010")
    if abs(float(vo_keep.get("total_speech_s") or 0.0) - 499.84) > 1e-6:
        raise GuardError("VO_TAKES_KEEP.json total_speech_s drifted from 499.84")
    locked_parts = vo_keep.get("locked") or {}
    if set(locked_parts.keys()) != {"01", "02", "03", "04", "05"}:
        raise GuardError("VO_TAKES_KEEP.json must lock parts 01..05")
    for pkey, meta in locked_parts.items():
        if not re.fullmatch(r"[0-9a-f]{64}", str((meta or {}).get("sha256") or "")):
            raise GuardError(f"VO_TAKES_KEEP.json part {pkey} missing sha256")

    shorts_plan_path = repo / SHORTS_PLAN_REL
    if not shorts_plan_path.is_file():
        raise GuardError(f"missing SHORTS_PICTURE_PLAN_v03.json: {shorts_plan_path}")
    shorts_plan = json.loads(shorts_plan_path.read_text())
    shorts_by_id = {str(s.get("id")): s for s in (shorts_plan.get("shorts") or [])}
    if set(shorts_by_id.keys()) != {"Short_A", "Short_C"}:
        raise GuardError("SHORTS_PICTURE_PLAN_v03.json must define Short_A and Short_C")

    short_a = shorts_by_id["Short_A"]
    short_c = shorts_by_id["Short_C"]
    if (
        short_a.get("vo_sha256_mp3") != EXPECTED_SHORT_A_MP3_SHA256
        or short_a.get("vo_sha256_wav") != EXPECTED_SHORT_A_WAV_SHA256
        or abs(float(short_a.get("vo_duration_s") or 0.0) - EXPECTED_SHORT_A_VO_DUR_S) > 1e-6
        or abs(float(short_a.get("hook_sentence_end_s") or 0.0) - EXPECTED_SHORT_A_HOOK_END_S) > 1e-6
        or abs(float(short_a.get("loop_tail_s") or 0.0) - 1.0) > 1e-6
        or short_a.get("frame0_plate") != "P1:01_clay_line"
        or short_a.get("hook_complete_in_s01") is not True
    ):
        raise GuardError("Short_A VO or timing metadata drifted in SHORTS_PICTURE_PLAN_v03.json")

    if (
        short_c.get("vo_sha256_mp3") != EXPECTED_SHORT_C_MP3_SHA256
        or short_c.get("vo_sha256_wav") != EXPECTED_SHORT_C_WAV_SHA256
        or abs(float(short_c.get("vo_duration_s") or 0.0) - EXPECTED_SHORT_C_VO_DUR_S) > 1e-6
        or abs(float(short_c.get("hook_sentence_end_s") or 0.0) - EXPECTED_SHORT_C_HOOK_END_S) > 1e-6
        or abs(float(short_c.get("loop_tail_s") or 0.0) - 1.0) > 1e-6
        or short_c.get("frame0_plate") != "P5:09_robin"
        or short_c.get("hook_complete_in_s01") is not True
    ):
        raise GuardError("Short_C VO or timing metadata drifted in SHORTS_PICTURE_PLAN_v03.json")

    recipe = short_a.get("assembly_audio_recipe")
    if not isinstance(recipe, dict):
        raise GuardError("Short_A is missing J1004 Option A1 assembly_audio_recipe")
    if (
        recipe.get("source_sha256_mp3") != EXPECTED_SHORT_A_MP3_SHA256
        or recipe.get("source_sha256_wav") != EXPECTED_SHORT_A_WAV_SHA256
        or abs(float(recipe.get("source_duration_s") or 0.0) - 22.72) > 1e-6
        or abs(float(recipe.get("source_hook_end_s") or 0.0) - 3.28) > 1e-6
        or abs(float(recipe.get("hook_atempo") or 0.0) - EXPECTED_OPTION_A1_HOOK_SPEED) > 1e-9
        or abs(float(recipe.get("body_atempo") or 0.0) - EXPECTED_OPTION_A1_BODY_SPEED) > 1e-9
        or abs(float(recipe.get("body_shift_s") or 0.0) - EXPECTED_OPTION_A1_BODY_SHIFT_S) > 1e-6
        or recipe.get("rendered") is not False
    ):
        raise GuardError("Short_A Option A1 assembly_audio_recipe drifted from J1004 parameters")

    raw_silences = recipe.get("silence_removals_s")
    if not isinstance(raw_silences, list) or len(raw_silences) != len(EXPECTED_OPTION_A1_SILENCES):
        raise GuardError("Short_A Option A1 silence_removals_s count drifted")
    parsed_silences: list[tuple[float, float]] = []
    for pair, expected_pair in zip(raw_silences, EXPECTED_OPTION_A1_SILENCES):
        if not isinstance(pair, list) or len(pair) != 2:
            raise GuardError("malformed interval in Short_A silence_removals_s")
        start_s, end_s = float(pair[0]), float(pair[1])
        if (
            start_s < 0.0
            or end_s <= start_s
            or end_s > 3.28 + 1e-6
            or abs(start_s - expected_pair[0]) > 1e-6
            or abs(end_s - expected_pair[1]) > 1e-6
        ):
            raise GuardError("Short_A Option A1 silence interval drifted")
        parsed_silences.append((start_s, end_s))
    silence_sum = round(sum(b - a for a, b in parsed_silences), 6)
    if abs(silence_sum - EXPECTED_OPTION_A1_SILENCE_SUM_S) > 1e-6:
        raise GuardError(f"Short_A Option A1 silence sum {silence_sum} != {EXPECTED_OPTION_A1_SILENCE_SUM_S}")

    # Verify on-disk Short A / Short C VO files whenever present (or strictly when required).
    expected_audio_files = (
        ("Short_A_mp3", "10_Shorts/vo_v02/hos_010_short_A_v02.mp3", EXPECTED_SHORT_A_MP3_SHA256),
        ("Short_A_wav", "10_Shorts/vo_v02/hos_010_short_A_v02.wav", EXPECTED_SHORT_A_WAV_SHA256),
        ("Short_C_mp3", "10_Shorts/vo_v02/hos_010_short_C_v02.mp3", EXPECTED_SHORT_C_MP3_SHA256),
        ("Short_C_wav", "10_Shorts/vo_v02/hos_010_short_C_v02.wav", EXPECTED_SHORT_C_WAV_SHA256),
    )
    search_roots: list[Path] = []
    if media is not None:
        search_roots.append(Path(media))
    search_roots.append(repo / FILM_REL)

    verified_audio: dict[str, dict] = {}
    for label, rel_str, expected_sha in expected_audio_files:
        found: Path | None = None
        for root in search_roots:
            candidate = root / rel_str
            if candidate.is_file():
                found = candidate
                break
        if found is None:
            if require_audio_files:
                raise GuardError(f"missing required accepted Short VO file {rel_str}")
            verified_audio[label] = {"present": False, "expected_sha256": expected_sha}
            continue
        actual_sha = sha256_file(found)
        if actual_sha != expected_sha:
            raise GuardError(f"accepted Short VO sha256 mismatch on {found}: {actual_sha} != {expected_sha}")
        verified_audio[label] = {
            "present": True,
            "path": str(found),
            "sha256": actual_sha,
        }

    return {
        "vo_takes_keep_sha256": vo_keep_sha,
        "short_a_mp3_sha256": EXPECTED_SHORT_A_MP3_SHA256,
        "short_a_wav_sha256": EXPECTED_SHORT_A_WAV_SHA256,
        "short_c_mp3_sha256": EXPECTED_SHORT_C_MP3_SHA256,
        "short_c_wav_sha256": EXPECTED_SHORT_C_WAV_SHA256,
        "option_a1_verified": True,
        "option_a1_silence_sum_s": silence_sum,
        "audio_files": verified_audio,
    }


def load_scope(repo: Path) -> list[Row]:
    """Load and cross-verify the exact 12 Quality rows of TWELVE_PLATE_SCOPE_J2267.json."""
    scope_path = repo / SCOPE_REL
    recon_path = repo / RECONCILIATION_REL
    shorts_plan_path = repo / SHORTS_PLAN_REL
    long_plan_path = repo / LONG_PLAN_REL
    for required_path, label in (
        (scope_path, "twelve-plate scope"),
        (recon_path, "J2267 budget reconciliation"),
        (shorts_plan_path, "Shorts picture plan v03"),
        (long_plan_path, "long picture plan v04"),
    ):
        if not required_path.is_file():
            raise GuardError(f"missing {label}: {required_path}")

    recon = json.loads(recon_path.read_text())
    if recon.get("job") != SCOPE_JOB_ID:
        raise GuardError(f"unexpected reconciliation job {recon.get('job')!r}")
    if sha256_file(long_plan_path) != recon.get("picture_plan_sha256"):
        raise GuardError("scope drift: PICTURE_PLAN_v04.json sha256 does not match J2267 reconciliation")
    if sha256_file(shorts_plan_path) != recon.get("shorts_plan_sha256"):
        raise GuardError("scope drift: SHORTS_PICTURE_PLAN_v03.json sha256 does not match J2267 reconciliation")

    long_plan = json.loads(long_plan_path.read_text())
    ltotals = long_plan.get("totals") or {}
    if (
        int(ltotals.get("rows") or 0) != 75
        or int(ltotals.get("Quality") or 0) != 49
        or int(ltotals.get("Fast") or 0) != 11
        or int(ltotals.get("code_graphic") or 0) != 13
        or int(ltotals.get("flow_credits_try1") or 0) != 5010
    ):
        raise GuardError("scope drift: PICTURE_PLAN_v04.json totals do not match reconciled 75 rows / 5010 try1")

    shorts_plan = json.loads(shorts_plan_path.read_text())
    stotals = shorts_plan.get("totals") or {}
    if (
        int(stotals.get("missing_unique_moving_plates") or 0) != EXPECTED_ROW_COUNT
        or int(stotals.get("available_unique_plates") or 0) != 2
    ):
        raise GuardError("scope drift: SHORTS_PICTURE_PLAN_v03.json missing/available unique plate counts drifted")

    verify_vo_and_option_a1(repo)

    # Index all missing Short uses by source_long_plate from SHORTS_PICTURE_PLAN_v03.json.
    shorts_uses_by_plate: dict[str, list[dict]] = {}
    available_code_plates: set[str] = set()
    for short_entry in shorts_plan.get("shorts") or []:
        short_id = str(short_entry.get("id") or "")
        for srow in short_entry.get("rows") or []:
            src_plate = str(srow.get("source_long_plate") or "")
            if srow.get("plate_on_disk") is True:
                available_code_plates.add(src_plate)
                continue
            merged = {"short": short_id, **srow}
            shorts_uses_by_plate.setdefault(src_plate, []).append(merged)
    if available_code_plates != {"P4:01_iridium_spike", "P5:11_why_survive"}:
        raise GuardError(f"unexpected on-disk code graphics set in Shorts plan: {sorted(available_code_plates)}")
    if set(shorts_uses_by_plate.keys()) != set(EXPECTED_ROW_IDS):
        raise GuardError("scope drift: Shorts plan missing-plate set differs from the 12 J2267 parent identities")

    # Verify all 5 part boards against J2267_BUDGET_RECONCILIATION.json.
    recon_parts = recon.get("parts") or []
    if [int(p.get("part") or 0) for p in recon_parts] != [1, 2, 3, 4, 5]:
        raise GuardError("reconciliation must pin parts 1..5 in order")
    boards_by_part: dict[int, tuple[str, str, dict[str, dict]]] = {}
    for pmeta in recon_parts:
        part = int(pmeta["part"])
        rel_from_film = str(pmeta.get("path") or "")
        expected_board_name = "part-05_plates_v04.json" if part == 5 else f"part-0{part}_plates_v03.json"
        if rel_from_film != f"07_Edit-Project/parts/{expected_board_name}":
            raise GuardError(f"unexpected board path for part {part}: {rel_from_film}")
        board_path = repo / FILM_REL / rel_from_film
        if not board_path.is_file():
            raise GuardError(f"missing part board: {board_path}")
        digest = sha256_file(board_path)
        if digest != pmeta.get("sha256"):
            raise GuardError(f"scope drift: board sha256 mismatch on {rel_from_film}")
        board = json.loads(board_path.read_text())
        plates = board.get("plates") or []
        if len(plates) != int(pmeta.get("rows") or 0):
            raise GuardError(f"scope drift: board row count mismatch on {rel_from_film}")
        by_id: dict[str, dict] = {}
        for pl in plates:
            pid = str(pl.get("id") or "")
            if not pid or pid in by_id:
                raise GuardError(f"invalid or duplicate plate id {pid!r} on {rel_from_film}")
            by_id[pid] = pl
        boards_by_part[part] = (rel_from_film, digest, by_id)

    scope = json.loads(scope_path.read_text())
    if scope.get("job") != SCOPE_JOB_ID:
        raise GuardError(f"scope job {scope.get('job')!r} != {SCOPE_JOB_ID}")
    if scope.get("required_prior_production") != PRIOR_HOS009_JOB_ID:
        raise GuardError("scope must retain required_prior_production=J2033")

    hplan = scope.get("historical_planning") or {}
    if (
        int(hplan.get("try_one") or 0) != TRY1_TOTAL_CREDITS
        or int(hplan.get("hard_cap_proposed") or 0) != MAX_TOTAL_CREDITS
        or int(hplan.get("minimum_balance_after_remaining_cap_and_other_reservations") or 0) != HEADROOM_FLOOR
        or int(hplan.get("max_rows_per_batch") or 0) != MAX_BATCH_ROWS
        or int(hplan.get("max_credits_per_batch") or 0) != MAX_BATCH_CREDITS
    ):
        raise GuardError("scope historical_planning caps do not match J2267/J2268 constants")

    raw_rows = scope.get("rows") or []
    if len(raw_rows) != EXPECTED_ROW_COUNT:
        raise GuardError(f"scope drift: scope has {len(raw_rows)} rows, expected {EXPECTED_ROW_COUNT}")

    rows: list[Row] = []
    seen_ids: set[str] = set()
    for index, raw in enumerate(raw_rows, start=1):
        row_id = str(raw.get("identity") or "")
        match = re.fullmatch(r"P([1-5]):([A-Za-z0-9_]+)", row_id)
        if not match:
            raise GuardError(f"scope drift: malformed row identity {row_id!r}")
        part = int(match.group(1))
        plate_id = match.group(2)
        if row_id in seen_ids:
            raise GuardError(f"scope drift: duplicate row identity {row_id}")
        seen_ids.add(row_id)
        if row_id in available_code_plates:
            raise GuardError(f"scope drift: code graphic {row_id} must not be in Flow scope")

        board_rel, board_digest, by_id = boards_by_part[part]
        if raw.get("source_board") != board_rel or raw.get("source_board_sha256") != board_digest:
            raise GuardError(f"scope drift: source_board or sha256 mismatch on {row_id}")

        plate = by_id.get(plate_id)
        if plate is None:
            raise GuardError(f"scope drift: {row_id} missing from {board_rel}")
        if plate.get("route") != "flow-first":
            raise GuardError(f"scope drift: {row_id} route {plate.get('route')!r} is not flow-first")
        if plate.get("quality") != REQUIRED_QUALITY or raw.get("quality") != REQUIRED_QUALITY:
            raise GuardError(f"scope drift: {row_id} quality must be {REQUIRED_QUALITY}")

        board_model = str(plate.get("flow_model") or "")
        scope_model = str(raw.get("model") or "")
        if "Veo 3.1" not in board_model or "Quality" not in board_model:
            raise GuardError(f"scope drift: {row_id} board flow_model {board_model!r} invalid")
        if "Veo 3.1" not in scope_model or "Quality" not in scope_model:
            raise GuardError(f"scope drift: {row_id} scope model {scope_model!r} invalid")

        if (
            int(plate.get("flow_clip_s") or 0) != REQUIRED_CLIP_S
            or int(raw.get("clip_s") or 0) != REQUIRED_CLIP_S
            or raw.get("aspect") != REQUIRED_ASPECT
            or int(raw.get("outputs_per_take") or 0) != 1
            or int(raw.get("max_takes") or 0) != MAX_TAKES_PER_ROW
            or int(plate.get("flow_credits_try1") or 0) != MAX_CREDITS_PER_TAKE
            or int(raw.get("planning_credits_per_take") or 0) != MAX_CREDITS_PER_TAKE
            or int(raw.get("planning_cap") or 0) != MAX_CREDITS_PER_TAKE * MAX_TAKES_PER_ROW
        ):
            raise GuardError(f"scope drift: clip/aspect/outputs/takes/credits mismatch on {row_id}")

        prompt = str(plate.get("prompt") or "")
        if not prompt.strip() or raw.get("prompt") != prompt:
            raise GuardError(f"scope drift: prompt mismatch between scope and board on {row_id}")
        prompt_sha = sha256_bytes(prompt.encode("utf-8"))
        norm_sha = sha256_bytes(" ".join(prompt.split()).encode("utf-8"))

        explorer = bool(plate.get("explorer", False))
        expected_explorer = row_id == EXPECTED_EXPLORER_ROW_ID
        if explorer is not expected_explorer:
            raise GuardError(f"scope drift: Explorer allowed ONLY on {EXPECTED_EXPLORER_ROW_ID}, got {row_id}={explorer}")
        ref = str(raw.get("reference") or "")
        if ref != str(plate.get("reference") or ""):
            raise GuardError(f"scope drift: reference mismatch on {row_id}")
        if explorer and ref != str(EXPLORER_REF_REL):
            raise GuardError(f"scope drift: {row_id} must pin {EXPLORER_REF_REL}")
        if not explorer and "explorer" in ref.lower():
            raise GuardError(f"scope drift: non-Explorer row {row_id} references Explorer")

        shorts_only = bool(raw.get("shorts_only", False))
        expected_shorts_only = row_id in EXPECTED_SHORTS_ONLY_IDS
        if shorts_only is not expected_shorts_only:
            raise GuardError(f"scope drift: shorts_only mismatch on {row_id}")
        if shorts_only:
            if "t_s" in plate or "local_s" in plate or "duration_s" in plate:
                raise GuardError(f"scope drift: Shorts-only row {row_id} must not carry long timeline fields")
            t_s_val: float | None = None
        else:
            if "t_s" not in plate or plate.get("t_s") is None:
                raise GuardError(f"scope drift: shared long row {row_id} missing long timeline t_s")
            t_s_val = float(plate["t_s"])

        long_use_s = float(plate.get("use_s") or 0.0)
        if long_use_s <= 0.0 or long_use_s > float(REQUIRED_CLIP_S):
            raise GuardError(f"scope drift: invalid board use_s {long_use_s} on {row_id}")

        raw_uses = raw.get("uses") or []
        expected_uses = shorts_uses_by_plate.get(row_id) or []
        if not raw_uses or raw_uses != expected_uses:
            raise GuardError(f"scope drift: Short uses mismatch between scope and SHORTS_PICTURE_PLAN_v03 on {row_id}")

        max_short_use_s = 0.0
        total_short_alloc_s = 0.0
        for use in raw_uses:
            u_s = float(use.get("use_s") or 0.0)
            if u_s <= 0.0 or u_s > float(REQUIRED_CLIP_S):
                raise GuardError(f"scope drift: invalid Short use_s {u_s} on {row_id}")
            max_short_use_s = max(max_short_use_s, u_s)
            total_short_alloc_s += u_s
            if explorer and (use.get("id") == "S01" or float(use.get("t_start_s") or 0.0) <= 0.0):
                raise GuardError(f"Explorer hard fail: {row_id} cannot be used as a Short frame 0")
            if use.get("id") == "loop_tail" and abs(u_s - 1.0) > 1e-6:
                raise GuardError(f"Short loop_tail on {row_id} must be 1.0s, got {u_s}s")
        # Even when a frame-0 plate also supplies a distinct 1.0s loop_tail window, 8.0s easily covers both.
        if total_short_alloc_s > float(REQUIRED_CLIP_S) - 0.1:
            raise GuardError(f"Short distinct-window allocation {total_short_alloc_s}s exceeds 8s plate on {row_id}")

        rows.append(
            Row(
                index=index,
                row_id=row_id,
                part=part,
                plate_id=plate_id,
                board=str(FILM_REL / board_rel),
                board_sha256=board_digest,
                quality=REQUIRED_QUALITY,
                flow_model=REQUIRED_MODEL,
                max_takes=MAX_TAKES_PER_ROW,
                try1_credits=MAX_CREDITS_PER_TAKE,
                planning_cap=MAX_CREDITS_PER_TAKE * MAX_TAKES_PER_ROW,
                flow_clip_s=REQUIRED_CLIP_S,
                t_s=t_s_val,
                long_use_s=long_use_s,
                max_short_use_s=max_short_use_s,
                required_decode_s=float(REQUIRED_CLIP_S),
                shorts_only=shorts_only,
                explorer=explorer,
                reference=ref,
                uses=tuple(raw_uses),
                prompt=prompt,
                prompt_sha256=prompt_sha,
                normalized_prompt_sha256=norm_sha,
            )
        )

    if tuple(r.row_id for r in rows) != EXPECTED_ROW_IDS:
        raise GuardError(f"scope drift: 12-plate identity order {[r.row_id for r in rows]} != expected J2267 order")
    if sum(1 for r in rows if not r.shorts_only) != EXPECTED_SHARED_LONG_COUNT:
        raise GuardError("scope drift: expected 10 shared long+Shorts rows")
    if sum(1 for r in rows if r.shorts_only) != EXPECTED_SHORTS_ONLY_COUNT:
        raise GuardError("scope drift: expected 2 Shorts-only rows")
    # Callback plate must have a distinct prompt and identity from opening clay line plate.
    p1_open = rows[0]
    p5_cb = next(r for r in rows if r.row_id == "P5:12_clay_callback")
    if p1_open.prompt_sha256 == p5_cb.prompt_sha256:
        raise GuardError("P5:12_clay_callback must not duplicate P1:01_clay_line prompt")
    return rows


def require_generation_authorization(
    repo: Path,
    authorization_file: Path | None = None,
) -> GenerationAuthorization:
    """Verify explicit Chief spend authorization (J2269 after HOS 009 J2033 DONE)."""
    scope_path = repo / SCOPE_REL
    if not scope_path.is_file():
        raise GuardError(f"missing scope file: {scope_path}")
    live_scope_sha = sha256_file(scope_path)
    scope = json.loads(scope_path.read_text())

    if authorization_file is not None:
        auth_path = Path(authorization_file)
        if not auth_path.is_file():
            raise GuardError(f"missing Chief authorization file: {auth_path}")
        payload = json.loads(auth_path.read_text())
        if not isinstance(payload, dict):
            raise GuardError("authorization file must contain a JSON object")
        if payload.get("job") != AUTH_JOB_ID or payload.get("film") != FILM_ID:
            raise GuardError(f"authorization file must be issued by {AUTH_JOB_ID} for {FILM_ID}")
        if payload.get("generation_authorized") is not True:
            raise GuardError("authorization file has generation_authorized != true")
        if payload.get("j2033_done") is not True:
            raise GuardError("authorization file must confirm prior HOS 009 J2033 is DONE")
        if payload.get("scope_sha256") != live_scope_sha:
            raise GuardError("authorization file scope_sha256 does not match live TWELVE_PLATE_SCOPE_J2267.json")
        cap = payload.get("authorized_cap_credits")
        floor = payload.get("minimum_headroom_floor", HEADROOM_FLOOR)
        if type(cap) is not int or cap <= 0 or cap > MAX_TOTAL_CREDITS:
            raise GuardError(f"authorized_cap_credits {cap!r} must be an integer in 1..{MAX_TOTAL_CREDITS}")
        if type(floor) is not int or floor < HEADROOM_FLOOR:
            raise GuardError(f"minimum_headroom_floor {floor!r} cannot be below {HEADROOM_FLOOR}")
        return GenerationAuthorization(
            job=AUTH_JOB_ID,
            film=FILM_ID,
            scope_sha256=live_scope_sha,
            authorized_cap_credits=cap,
            minimum_headroom_floor=floor,
            j2033_done=True,
            source=str(auth_path.resolve()),
        )

    row_flags = [bool(r.get("generation_authorized", False)) for r in (scope.get("rows") or [])]
    if scope.get("generation_authorized") is True and row_flags and all(row_flags):
        if scope.get("j2033_done") is not True:
            raise GuardError("scope generation_authorized=true requires j2033_done=true from J2269")
        cap = int((scope.get("historical_planning") or {}).get("authorized_cap_credits") or MAX_TOTAL_CREDITS)
        if cap <= 0 or cap > MAX_TOTAL_CREDITS:
            raise GuardError(f"scope authorized_cap_credits {cap} outside 1..{MAX_TOTAL_CREDITS}")
        return GenerationAuthorization(
            job=str(scope.get("authorized_by_job") or AUTH_JOB_ID),
            film=FILM_ID,
            scope_sha256=live_scope_sha,
            authorized_cap_credits=cap,
            minimum_headroom_floor=HEADROOM_FLOOR,
            j2033_done=True,
            source=str(scope_path.resolve()),
        )

    raise GuardError(
        "generation is NOT authorized: TWELVE_PLATE_SCOPE_J2267.json has generation_authorized=false "
        f"(awaiting {AUTH_JOB_ID} preflight and elected-Chief ruling after {PRIOR_HOS009_JOB_ID} DONE)"
    )


def _row_sort_key(row: Row) -> tuple[int, int, float, int]:
    # Shared long plates first within each part by timeline t_s, then Shorts-only plates by scope index.
    return (row.part, 1 if row.shorts_only else 0, row.t_s if row.t_s is not None else float("inf"), row.index)


def order_rows(rows: list[Row], *, require_part1_first: bool = True) -> list[Row]:
    """Order strictly Part 01 first (Short A frame 0), then Parts 02..05, then Part 05 Shorts-only parents."""
    if not rows:
        raise GuardError("cannot order empty row list")
    ordered = sorted(rows, key=_row_sort_key)
    if require_part1_first and (ordered[0].part != 1 or ordered[0].row_id != "P1:01_clay_line"):
        raise GuardError("twelve-plate pass must start with Part 01 P1:01_clay_line")
    seen_keys: set[tuple[int, str]] = set()
    prev_key = (0, 0, -1.0, 0)
    for row in ordered:
        if row.key in seen_keys:
            raise GuardError(f"duplicate row in order: {row.row_id}")
        seen_keys.add(row.key)
        cur = _row_sort_key(row)
        if cur < prev_key:
            raise GuardError(f"out-of-order row {row.row_id}")
        prev_key = cur
    return ordered


def assert_batch_limits(batch: list[Row], *, max_credits: int = MAX_BATCH_CREDITS) -> int:
    """Enforce <= 5 rows and <= 1500 credits per batch (including worst-case 3-take exposure)."""
    if not batch:
        raise GuardError("empty batch is not allowed")
    if len(batch) > MAX_BATCH_ROWS:
        raise GuardError(f"batch of {len(batch)} rows exceeds MAX_BATCH_ROWS={MAX_BATCH_ROWS}")
    seen: set[str] = set()
    prev_order = (0, 0, -1.0, 0)
    try1_credits = 0
    worst_case_credits = 0
    for row in batch:
        if row.row_id in seen:
            raise GuardError(f"duplicate row in batch: {row.row_id}")
        seen.add(row.row_id)
        cur_order = _row_sort_key(row)
        if cur_order < prev_order:
            raise GuardError(f"batch violates canonical row order at {row.row_id}")
        prev_order = cur_order
        expected_cost = expected_credits_for(row)
        if row.try1_credits != expected_cost or row.max_takes != MAX_TAKES_PER_ROW:
            raise GuardError(f"invalid row cost or max_takes on {row.row_id}")
        try1_credits += row.try1_credits
        worst_case_credits += row.try1_credits * row.max_takes
    if try1_credits > max_credits or worst_case_credits > MAX_BATCH_CREDITS:
        raise GuardError(
            f"batch of {len(batch)} rows ({try1_credits} try1 / {worst_case_credits} max credits) "
            f"exceeds {min(max_credits, MAX_BATCH_CREDITS)} batch cap"
        )
    return try1_credits


def batch_rows(rows: list[Row], *, require_part1_first: bool = True) -> list[list[Row]]:
    """Pack ordered rows into batches of <= 5 rows and <= 1,500 worst-case credits (5 + 5 + 2)."""
    if not rows:
        return []
    ordered = order_rows(rows, require_part1_first=require_part1_first)
    batches: list[list[Row]] = []
    idx = 0
    while idx < len(ordered):
        batch: list[Row] = []
        worst_credits = 0
        while (
            idx < len(ordered)
            and len(batch) < MAX_BATCH_ROWS
            and worst_credits + ordered[idx].try1_credits * ordered[idx].max_takes <= MAX_BATCH_CREDITS
        ):
            batch.append(ordered[idx])
            worst_credits += ordered[idx].try1_credits * ordered[idx].max_takes
            idx += 1
        if not batch:
            raise GuardError(f"row {ordered[idx].row_id} alone exceeds batch limits")
        assert_batch_limits(batch)
        batches.append(batch)
    return batches


def accept_price(
    price: PriceEvidence,
    *,
    quality: str = REQUIRED_QUALITY,
    now: datetime | None = None,
    max_age_s: int = 900,
) -> int:
    expected_model = expected_model_for(quality)
    expected_cost = expected_credits_for(quality)
    if price.quality != quality:
        raise GuardError(f"price quality {price.quality!r} != {quality!r}")
    if price.model != expected_model:
        raise GuardError(f"model {price.model!r} is not {expected_model!r}")
    if price.outputs != REQUIRED_OUTPUTS:
        raise GuardError(f"outputs {price.outputs!r} are not {REQUIRED_OUTPUTS}")
    if price.aspect != REQUIRED_ASPECT:
        raise GuardError(f"aspect {price.aspect!r} is not {REQUIRED_ASPECT}")
    if price.duration != REQUIRED_DURATION:
        raise GuardError(f"duration {price.duration!r} is not {REQUIRED_DURATION}")
    if type(price.credits) is not int or price.credits != expected_cost:
        raise GuardError(f"price {price.credits!r} is not {expected_cost} for {quality}")
    match = GENERATE_LINE_RE.match((price.generate_line or "").strip())
    if not match or int(match.group(1)) != expected_cost:
        raise GuardError(f"generate line is not an exact {expected_cost}-credit charge")
    if not price.read_at:
        raise GuardError("price evidence has no read time")
    stamp = datetime.fromisoformat(price.read_at)
    if stamp.tzinfo is None:
        stamp = stamp.replace(tzinfo=timezone.utc)
    if now is not None:
        age = (now - stamp).total_seconds()
        if age < 0 or age > max_age_s:
            raise GuardError(f"price read is not fresh ({int(age)}s)")
    return expected_cost


def accept_batch_prices(
    prices_by_quality: dict[str, PriceEvidence] | None,
    *,
    now: datetime | None = None,
    max_age_s: int = 900,
) -> dict[str, int]:
    """Require a fresh live Quality (100-credit) price reading before each batch."""
    if not isinstance(prices_by_quality, dict):
        raise GuardError("missing pre-batch live price readings")
    extra = set(prices_by_quality.keys()) - {REQUIRED_QUALITY}
    if extra:
        raise GuardError(f"unexpected non-Quality model price entry in twelve-plate batch: {sorted(extra)}")
    ev = prices_by_quality.get(REQUIRED_QUALITY)
    if not isinstance(ev, PriceEvidence):
        raise GuardError("missing pre-batch live price reading for Quality")
    return {REQUIRED_QUALITY: accept_price(ev, quality=REQUIRED_QUALITY, now=now, max_age_s=max_age_s)}


def accept_zero_still_price(still_price: dict | None, *, now: datetime | None = None, max_age_s: int = 900) -> int:
    if not isinstance(still_price, dict):
        raise GuardError("Nano Banana 2.1 still price is missing")
    if still_price.get("model") not in (None, REQUIRED_STILL_MODEL):
        raise GuardError(f"still model {still_price.get('model')!r} is not {REQUIRED_STILL_MODEL!r}")
    if still_price.get("outputs") not in (None, REQUIRED_OUTPUTS):
        raise GuardError(f"still outputs {still_price.get('outputs')!r} are not {REQUIRED_OUTPUTS}")
    if still_price.get("aspect") not in (None, REQUIRED_ASPECT):
        raise GuardError(f"still aspect {still_price.get('aspect')!r} is not {REQUIRED_ASPECT}")
    displayed = still_price.get("displayed_credits")
    if type(displayed) is not int or displayed != 0:
        raise GuardError("Nano Banana 2.1 still price is not a verified 0")
    if now is not None and still_price.get("read_at"):
        stamp = datetime.fromisoformat(str(still_price["read_at"]))
        if stamp.tzinfo is None:
            stamp = stamp.replace(tzinfo=timezone.utc)
        age = (now - stamp).total_seconds()
        if age < 0 or age > max_age_s:
            raise GuardError(f"still price read is not fresh ({int(age)}s)")
    return 0


def accept_account(
    account_or_sha256: str | None,
    read_at: str | None,
    *,
    now: datetime,
    max_age_s: int = 900,
) -> str:
    expected = required_account_sha256()
    forbidden = forbidden_account_sha256()
    if not read_at:
        raise GuardError("balance read timestamp is missing")
    stamp = datetime.fromisoformat(read_at)
    if stamp.tzinfo is None:
        stamp = stamp.replace(tzinfo=timezone.utc)
    age = (now - stamp).total_seconds()
    if age < 0 or age > max_age_s:
        raise GuardError(f"balance read is not fresh ({int(age)}s)")
    if not isinstance(account_or_sha256, str) or not account_or_sha256.strip():
        raise GuardError("Flow account is missing")
    candidate = account_or_sha256.strip().lower()
    digest = candidate if re.fullmatch(r"[0-9a-f]{64}", candidate) else account_sha256(candidate)
    if digest == FORBIDDEN_ACCOUNT_SHA256 or (forbidden and digest == forbidden) or digest != expected:
        raise GuardError("Flow account is not the studio Ultra account")
    return expected


def _probe_image_16x9_or_valid(path: Path, *, require_16x9: bool = False) -> tuple[int, int, str]:
    if not path.is_file() or path.stat().st_size == 0:
        raise GuardError(f"missing or empty reference image: {path}")
    digest = sha256_file(path)
    try:
        probe = subprocess.run(
            ["ffprobe", "-v", "error", "-show_streams", "-of", "json", str(path)],
            check=True,
            capture_output=True,
            text=True,
        )
        streams = json.loads(probe.stdout).get("streams") or []
        if len(streams) != 1 or streams[0].get("codec_type") != "video":
            raise GuardError(f"reference image needs one image stream: {path}")
        width, height = int(streams[0]["width"]), int(streams[0]["height"])
        subprocess.run(
            ["ffmpeg", "-v", "error", "-xerror", "-i", str(path), "-frames:v", "1", "-f", "null", "-"],
            check=True,
            capture_output=True,
        )
    except GuardError:
        raise
    except Exception as exc:
        raise GuardError(f"corrupt or unreadable reference image: {path}") from exc
    if width < 640 or height < 360:
        raise GuardError(f"reference image resolution too small ({width}x{height}): {path}")
    if require_16x9 and abs(width / height - 16 / 9) > 0.02:
        raise GuardError(f"reference image is not 16:9 ({width}x{height}): {path}")
    return width, height, digest


def verify_explorer_reference(repo: Path, rows: list[Row] | None = None, *, check_hash: bool = True) -> dict | None:
    """Verify Explorer reference sheet exists, decodes, matches SHA-256, and is used only on P5:10."""
    if rows is not None:
        exp_rows = [r for r in rows if r.explorer]
        if [r.row_id for r in exp_rows] not in ([], [EXPECTED_EXPLORER_ROW_ID]):
            raise GuardError(
                f"Explorer reference allowed ONLY on {EXPECTED_EXPLORER_ROW_ID}, got {[r.row_id for r in exp_rows]}"
            )
        for r in exp_rows:
            for use in r.uses:
                if use.get("id") == "S01" or float(use.get("t_start_s") or 0.0) <= 0.0:
                    raise GuardError(f"Explorer hard fail: {r.row_id} is on a Short frame 0")
        if not exp_rows:
            return None

    exp_path = (repo / EXPLORER_REF_REL).resolve()
    if repo.resolve() not in exp_path.parents or not exp_path.is_file():
        raise GuardError(f"missing Explorer style reference: {exp_path}")
    width, height, digest = _probe_image_16x9_or_valid(exp_path, require_16x9=False)
    if check_hash and digest != EXPLORER_REF_SHA256:
        raise GuardError(f"Explorer reference sha256 drift: {digest} != {EXPLORER_REF_SHA256}")
    return {
        "rel": str(EXPLORER_REF_REL),
        "path": str(exp_path),
        "sha256": digest,
        "width": width,
        "height": height,
    }


def verify_style_references(
    repo: Path,
    media: Path,
    rows: list[Row] | None = None,
    *,
    check_hashes: bool = True,
) -> dict:
    """Verify house `_style_refs` (under media) and Explorer reference (under repo) before any Flow call."""
    media_root = Path(media)
    if not media_root.is_dir():
        raise GuardError(f"missing film media directory: {media_root}")
    house_verified = []
    for rel, expected_sha in CANONICAL_HOUSE_STYLE_REFS:
        candidate = (media_root / rel).resolve()
        if media_root.resolve() not in candidate.parents or not candidate.is_file() or candidate.stat().st_size == 0:
            raise GuardError(f"missing style reference image: {candidate}")
        width, height, digest = _probe_image_16x9_or_valid(candidate, require_16x9=True)
        if check_hashes and digest != expected_sha:
            raise GuardError(f"style reference sha256 drift on {rel}: {digest} != {expected_sha}")
        house_verified.append(
            {
                "rel": rel,
                "path": str(candidate),
                "sha256": digest,
                "width": width,
                "height": height,
            }
        )
    explorer_verified = verify_explorer_reference(repo, rows, check_hash=check_hashes)
    return {"house": house_verified, "explorer": explorer_verified}


def resolve_external_reservations(
    shared_snapshot: dict,
    external: int | dict[str, int] | None = 0,
    *,
    own_reservation: str = DEFAULT_RESERVATION,
    own_film: str = FILM_ID,
) -> int:
    """Deduplicate/reject double-counted or stale `expected` reservation inputs."""
    if external is None:
        return 0
    if isinstance(external, bool):
        raise GuardError("invalid external reservations value")
    if isinstance(external, int):
        if external < 0:
            raise GuardError("negative external reservations are invalid")
        return external
    if not isinstance(external, dict):
        raise GuardError("external reservations must be an int or dict of live caps")

    active = {
        key: val
        for key, val in (shared_snapshot.get("reservations") or {}).items()
        if isinstance(val, dict) and val.get("active")
    }
    active_films = {str(val.get("film")) for val in active.values() if val.get("film")}

    extra_sum = 0
    for raw_key, amount in external.items():
        key = str(raw_key)
        low = key.lower()
        if "expected" in low or low in ("006", "007", "008", "009 tranche 1", "028"):
            raise GuardError(
                f"stale expected reservation estimate {key!r} refused; use live cap reservations only"
            )
        if isinstance(amount, bool) or not isinstance(amount, int) or amount < 0:
            raise GuardError(f"invalid reservation amount {amount!r} for {key!r}")
        if key == own_reservation or key == own_film:
            raise GuardError(f"cannot double-count own {own_film} reservation {key!r} in external reservations")
        if key in active:
            recorded_cap = int(active[key]["cap"])
            if amount > recorded_cap:
                raise GuardError(
                    f"external reservation {key!r}={amount} exceeds active shared ledger cap {recorded_cap}"
                )
            # Already accounted in shared_snapshot['liability']; never double-count.
            continue
        if key in active_films:
            raise GuardError(
                f"film {key!r} already has an active reservation in shared Flow accounting; refusing double count"
            )
        extra_sum += amount
    return extra_sum


def ledger_totals(
    entries: list[dict],
    *,
    max_takes: int = MAX_TAKES_PER_ROW,
    max_total_credits: int = MAX_TOTAL_CREDITS,
) -> tuple[int, int, bool, dict[str, int]]:
    """Sum spent/pending credits and per-row take counts. Reject KEEP, unknown status, or cap breaches."""
    latest: dict[tuple[str, int], dict] = {}
    for entry in entries:
        status = entry.get("status")
        if status == "KEEP" or entry.get("keep") is True or entry.get("review") == "KEEP":
            raise GuardError("ledger contains KEEP; twelve-plate runner never auto-KEEPs")
        if status not in ("SUBMITTING", "PENDING_REVIEW", "GENERATED", "FAILED", "REJECTED_REVIEW", POLICY_REFUSED):
            raise GuardError(f"unknown ledger status {status!r}")
        if status == POLICY_REFUSED and (entry.get("credits_used") != 0 or type(entry.get("credits_used")) is not int
                                         or not str(entry.get("reason") or "").strip()):
            raise GuardError(f"{POLICY_REFUSED} needs credits_used 0 and a reason")
        row_id = str(entry.get("row_id") or "")
        if not row_id:
            part = entry.get("part")
            plate_id = entry.get("plate_id")
            if part is not None and plate_id:
                row_id = f"P{int(part)}:{plate_id}"
        take = int(entry.get("take") or 0)
        if not row_id or take < 1:
            raise GuardError(f"invalid ledger row/take identity in {entry!r}")
        latest[(row_id, take)] = entry

    spent = 0
    pending = 0
    unknown = False
    takes: dict[str, int] = {}
    for (row_id, _take), entry in latest.items():
        takes[row_id] = takes.get(row_id, 0) + 1
        status = entry.get("status")
        if status == "SUBMITTING":
            reserved = entry.get("credits_reserved")
            if type(reserved) is not int or reserved <= 0:
                unknown = True
            else:
                pending += reserved
        elif status == POLICY_REFUSED:
            pass  # refused by Flow, 0 credits; it still used one of the row's takes
        else:
            amount = entry.get("credits_used")
            if amount is None:
                amount = entry.get("credits_reserved")
            if type(amount) is not int or amount <= 0:
                unknown = True
            else:
                spent += amount
    if any(count > max_takes for count in takes.values()):
        raise GuardError(f"a row already exceeds MAX_TAKES_PER_ROW={max_takes}")
    if spent + pending > max_total_credits:
        raise GuardError(f"ledger {spent}+{pending} exceeds authorized cap {max_total_credits}")
    return spent, pending, unknown, takes


def headroom(
    live: int | None,
    spent: int,
    pending: int,
    other: int,
    *,
    posted: int = 0,
    cap: int = MAX_TOTAL_CREDITS,
    floor: int = HEADROOM_FLOOR,
) -> int:
    """Verify full remaining cap + unposted + other preserves >= 3,000 credits without double-counting."""
    if (
        type(live) is not int
        or live < 0
        or type(other) is not int
        or other < 0
        or type(cap) is not int
        or cap <= 0
        or cap > MAX_TOTAL_CREDITS
        or type(floor) is not int
        or floor < 0
    ):
        raise GuardError("unknown or invalid balance, cap, floor, or other reservations")
    if min(spent, pending, posted) < 0 or posted > spent:
        raise GuardError("invalid posted/unposted accounting")
    remaining_cap = cap - spent - pending
    if remaining_cap < 0 or spent + pending > cap:
        raise GuardError(f"spend {spent}+{pending} exceeds the {cap} credit cap")
    unposted = spent - posted + pending
    # Note: unposted + remaining_cap == cap - posted, so pending/unposted takes inside `cap`
    # are counted exactly once against `live` (never `cap + pending`).
    left = live - unposted - remaining_cap - other
    if left < floor:
        raise GuardError(
            f"headroom {left} < {floor} after reserving remaining cap {remaining_cap}, "
            f"unposted {unposted}, and other {other}"
        )
    return left


def can_take(
    *,
    row: Row,
    live: int | None,
    spent: int,
    pending: int,
    other: int,
    takes_done: int,
    unknown_pending: bool,
    cost: int,
    posted: int = 0,
    cap: int = MAX_TOTAL_CREDITS,
    floor: int = HEADROOM_FLOOR,
) -> int:
    if unknown_pending:
        raise GuardError("unknown outstanding charges")
    if takes_done >= row.max_takes or takes_done >= MAX_TAKES_PER_ROW:
        raise GuardError(f"{row.row_id} already has {takes_done} take(s); cap is {MAX_TAKES_PER_ROW}")
    expected_cost = expected_credits_for(row)
    if type(cost) is not int or cost != expected_cost or cost != row.try1_credits:
        raise GuardError(f"refusing cost {cost!r} for {row.row_id} (expects {expected_cost})")
    if spent + pending + cost > cap:
        raise GuardError(f"cap {cap}: spent {spent} pending {pending} cost {cost}")
    return headroom(live, spent, pending + cost, other, posted=posted, cap=cap, floor=floor)


def build_plan(rows: list[Row], *, repo: Path | None = None) -> dict:
    root = repo or repo_root_from()
    vo_report = verify_vo_and_option_a1(root)
    explorer_info = verify_explorer_reference(root, rows)
    ordered = order_rows(rows)
    batches = batch_rows(ordered)
    per_part: dict[str, dict] = {}
    for part in range(1, 6):
        prows = [r for r in ordered if r.part == part]
        per_part[f"part_{part:02d}"] = {
            "rows": len(prows),
            "shared_long_rows": sum(1 for r in prows if not r.shorts_only),
            "shorts_only_rows": sum(1 for r in prows if r.shorts_only),
            "explorer": sum(1 for r in prows if r.explorer),
            "credits_try1": sum(r.try1_credits for r in prows),
            "credits_max_3_takes": sum(r.planning_cap for r in prows),
        }
    scope_payload = json.loads((root / SCOPE_REL).read_text())
    return {
        "job": JOB_ID,
        "scope_job": SCOPE_JOB_ID,
        "authorization_job": AUTH_JOB_ID,
        "producer_job": PRODUCER_JOB_ID,
        "prior_hos009_job": PRIOR_HOS009_JOB_ID,
        "film": FILM_ID,
        "scope_file": str(SCOPE_REL),
        "scope_sha256": sha256_file(root / SCOPE_REL),
        "generation_authorized": bool(scope_payload.get("generation_authorized", False)),
        "submissions": 0,
        "create_clicks": 0,
        "credits_spent": 0,
        "keep": False,
        "review": "PENDING_REVIEW",
        "file_state_when_written": "GENERATED",
        "row_count": len(ordered),
        "shared_long_row_count": sum(1 for r in ordered if not r.shorts_only),
        "shorts_only_row_count": sum(1 for r in ordered if r.shorts_only),
        "explorer_row_id": EXPECTED_EXPLORER_ROW_ID,
        "house_style_refs": [rel for rel, _sha in CANONICAL_HOUSE_STYLE_REFS],
        "explorer_ref": explorer_info["rel"] if explorer_info else str(EXPLORER_REF_REL),
        "vo_and_option_a1": vo_report,
        "caps": {
            "prices": {REQUIRED_QUALITY: MAX_CREDITS_PER_TAKE, "Still": 0},
            "models": {REQUIRED_QUALITY: REQUIRED_MODEL, "Still": REQUIRED_STILL_MODEL},
            "duration": REQUIRED_DURATION,
            "aspect": REQUIRED_ASPECT,
            "outputs": REQUIRED_OUTPUTS,
            "takes_per_row": MAX_TAKES_PER_ROW,
            "try1_credits": TRY1_TOTAL_CREDITS,
            "total_credits_proposed": MAX_TOTAL_CREDITS,
            "batch_rows": MAX_BATCH_ROWS,
            "batch_credits": MAX_BATCH_CREDITS,
            "floor": HEADROOM_FLOOR,
        },
        "per_part": per_part,
        "order": [
            {
                "index": row.index,
                "row_id": row.row_id,
                "part": row.part,
                "id": row.plate_id,
                "quality": row.quality,
                "flow_model": row.flow_model,
                "flow_clip_s": row.flow_clip_s,
                "try1_credits": row.try1_credits,
                "planning_cap": row.planning_cap,
                "shorts_only": row.shorts_only,
                "explorer": row.explorer,
                "prompt_sha256": row.prompt_sha256,
            }
            for row in ordered
        ],
        "batches": [
            {
                "batch_index": idx,
                "rows": [row.row_id for row in batch],
                "row_count": len(batch),
                "try1_credits": sum(row.try1_credits for row in batch),
                "worst_case_credits": sum(row.planning_cap for row in batch),
            }
            for idx, batch in enumerate(batches, start=1)
        ],
    }


def versioned_output(media: Path, part: int, plate_id: str, take: int = 1) -> Path:
    return (
        media
        / "04_Generated-Clips"
        / f"part{part:02d}"
        / "raw"
        / "v01_twelve_plates"
        / f"P{part:02d}_{plate_id}_t{take}.mp4"
    )


def next_version(
    media: Path, part: int, plate_id: str, *, max_takes: int = MAX_TAKES_PER_ROW, used=()
) -> tuple[int, Path]:
    """The first take number with no file and no ledger line. `used` holds the take numbers the
    ledger already has for this row: a take Flow refused leaves no file, and numbering the next
    take the same would put a new SUBMITTING line over the FAILED_POLICY one and then collide
    with the refused take's shared charge."""
    for take in range(1, max_takes + 1):
        dest = versioned_output(media, part, plate_id, take)
        if take not in used and not dest.exists():
            return take, dest
    raise GuardError(
        f"P{part}:{plate_id} already has {max_takes} versioned file(s); cap refuses take {max_takes + 1}"
    )


def still_path(media: Path, part: int, plate_id: str) -> Path:
    return (
        media
        / "04_Generated-Clips"
        / f"part{part:02d}"
        / "refs"
        / "v01_twelve_plates_stills"
        / f"P{part:02d}_{plate_id}_t1.png"
    )


def verify_still_inventory(rows: list[Row], media: Path) -> list[dict]:
    """Validate every start still before paid video batch spending starts."""
    inventory = []
    for row in rows:
        path = still_path(media, row.part, row.plate_id)
        if not path.is_file():
            raise GuardError(f"missing inventory start still for {row.row_id}: {path}")
        width, height, digest = _probe_image_16x9_or_valid(path, require_16x9=True)
        if width < 1280 or height < 720:
            raise GuardError(f"inventory still below 1280x720 HD ({width}x{height}): {path}")
        if digest != sha256_file(path):
            raise GuardError(f"inventory still changed while reading: {path}")
        pin = path.with_suffix(".sha256")
        if pin.exists() and pin.read_text().strip() != digest:
            raise GuardError(f"inventory differs from pinned start still: {path}")
        inventory.append(
            {
                "row_id": row.row_id,
                "part": row.part,
                "plate_id": row.plate_id,
                "path": str(path.resolve()),
                "sha256": digest,
                "width": width,
                "height": height,
            }
        )
    return inventory


class WriterLock:
    """Exclusive non-blocking flock. Any concurrent second process raises GuardError."""

    def __init__(self, path: Path):
        self.path = Path(path)
        self.handle = None

    def __enter__(self):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.handle = self.path.open("a+")
        try:
            fcntl.flock(self.handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError as exc:
            self.handle.close()
            self.handle = None
            raise GuardError(f"writer lock held: {self.path}") from exc
        return self

    def __exit__(self, exc_type, exc, tb):
        if self.handle is not None:
            fcntl.flock(self.handle.fileno(), fcntl.LOCK_UN)
            self.handle.close()
            self.handle = None
        return False


def shared_flow_state_dir() -> Path:
    """Canonical cross-channel Flow accounting directory (~/_desk/state/flow/shared)."""
    return Path.home() / "_desk/state/flow/shared"


class SharedFlowAccounting:
    """Durable cross-channel Flow reservation & charge accounting (J2200 protocol)."""

    def __init__(self, state: Path | None = None):
        self.state = state if state is not None else shared_flow_state_dir()
        self.lock = WriterLock(self.state / "writer.lock")
        self.path = self.state / "account.jsonl"
        self.held = False

    def __enter__(self):
        self.lock.__enter__()
        self.held = True
        try:
            self.snapshot()
        except BaseException:
            self.__exit__(None, None, None)
            raise
        return self

    def __exit__(self, *args):
        self.held = False
        return self.lock.__exit__(*args)

    def _assert_held(self):
        if not self.held:
            raise GuardError("shared Flow writer lock is not held")

    @staticmethod
    def _amount(value):
        if type(value) is not int or value < 0:
            raise GuardError("invalid shared credit amount")
        return value

    @classmethod
    def _parse_ledger_bytes(cls, data: bytes) -> dict:
        reservations, charges = {}, {}
        try:
            if data and not data.endswith(b"\n"):
                raise GuardError("torn shared Flow ledger; reconcile before any Create")
            for line in data.splitlines():
                event = json.loads(line)
                if not isinstance(event, dict):
                    raise GuardError("shared Flow event is not an object")
                kind, key = event["kind"], event["id"]
                if not isinstance(key, str) or not key:
                    raise GuardError("invalid shared event identity")
                if kind == "reserve":
                    cap = cls._amount(event["cap"])
                    if not event.get("film") or key in reservations:
                        raise GuardError("duplicate or unowned reservation")
                    reservations[key] = dict(cap=cap, film=event["film"], active=True)
                elif kind == "release":
                    if key not in reservations or not reservations[key]["active"]:
                        raise GuardError("unknown/repeated reservation release")
                    if any(c["reservation"] == key and c["status"] == "PENDING" for c in charges.values()):
                        raise GuardError("cannot release unresolved pending charge")
                    reservations[key]["active"] = False
                elif kind == "intent":
                    reservation = event["reservation"]
                    if key in charges or reservation not in reservations or not reservations[reservation]["active"]:
                        raise GuardError("duplicate charge or inactive reservation")
                    amount = cls._amount(event["amount"])
                    used = sum(c["amount"] for c in charges.values() if c["reservation"] == reservation)
                    if amount <= 0 or used + amount > reservations[reservation]["cap"]:
                        raise GuardError("charge exceeds reservation cap")
                    charges[key] = dict(reservation=reservation, amount=amount, status="PENDING", posted=False)
                elif kind in ("charged", "not_submitted"):
                    charge = charges[key]
                    if charge["status"] != "PENDING" or not event.get("evidence"):
                        raise GuardError("invalid pending charge resolution")
                    charge["status"] = "CHARGED" if kind == "charged" else "NOT_SUBMITTED"
                    if kind == "not_submitted":
                        charge["amount"] = 0
                elif kind == "posted":
                    charge = charges[key]
                    if charge["status"] != "CHARGED" or charge["posted"] or not event.get("evidence"):
                        raise GuardError("invalid posted charge reconciliation")
                    charge["posted"] = True
                elif kind == "policy_refused":
                    # Flow refused the prompt under its content policy and charged
                    # nothing: a reversal event, appended, never a history rewrite.
                    charge = charges[key]
                    if charge["status"] != "CHARGED" or charge["posted"] or not event.get("evidence"):
                        raise GuardError("invalid policy-refusal reversal")
                    charge["status"] = "POLICY_REFUSED"
                    charge["amount"] = 0
                else:
                    raise GuardError(f"unknown shared Flow event {kind!r}")
        except GuardError:
            raise
        except (ValueError, KeyError, TypeError) as exc:
            raise GuardError("unreadable shared Flow ledger; no Create permitted") from exc

        # Active reservations cover only their unused capacity; unposted charges carry
        # the already-used portion until reconciled, so liability never double-counts.
        unposted = sum(c["amount"] for c in charges.values() if not c["posted"])
        remaining = sum(
            r["cap"] - sum(c["amount"] for c in charges.values() if c["reservation"] == key)
            for key, r in reservations.items()
            if r["active"]
        )
        return dict(
            reservations=reservations,
            charges=charges,
            unposted=unposted,
            remaining_reservations=remaining,
            liability=unposted + remaining,
            pending=any(c["status"] == "PENDING" for c in charges.values()),
        )

    def snapshot(self) -> dict:
        self._assert_held()
        data = self.path.read_bytes() if self.path.exists() else b""
        return self._parse_ledger_bytes(data)

    @classmethod
    def peek_readonly(cls, state: Path | None = None) -> dict:
        base = state if state is not None else shared_flow_state_dir()
        path = base / "account.jsonl"
        data = path.read_bytes() if path.exists() else b""
        return cls._parse_ledger_bytes(data)

    def _event(self, event: dict) -> None:
        self._assert_held()
        append_ledger(self.path, {**event, "at": now_iso()})
        directory = os.open(self.state, os.O_RDONLY)
        try:
            os.fsync(directory)
        finally:
            os.close(directory)

    def reserve(self, key: str, film: str, cap: int, *, live: int, floor: int = HEADROOM_FLOOR) -> None:
        state = self.snapshot()
        self._amount(cap)
        self._amount(live)
        self._amount(floor)
        if not isinstance(key, str) or not key or not isinstance(film, str) or not film or cap <= 0:
            raise GuardError("reservation needs an identity, film and positive cap")
        existing = state["reservations"].get(key)
        if existing:
            if existing != dict(cap=cap, film=film, active=True):
                raise GuardError("reservation identity collision")
            if state["pending"] or live - state["liability"] < floor:
                raise GuardError("pending charge or insufficient shared Flow headroom")
            return
        if state["pending"] or live - state["liability"] - cap < floor:
            raise GuardError("pending charge or insufficient shared Flow headroom")
        self._event(dict(kind="reserve", id=key, film=film, cap=cap))

    def intent(self, key: str, reservation: str, amount: int, *, live: int, floor: int = HEADROOM_FLOOR) -> None:
        state = self.snapshot()
        self._amount(amount)
        self._amount(live)
        self._amount(floor)
        if state["pending"] or live - state["liability"] < floor:
            raise GuardError("pending charge or insufficient shared Flow headroom")
        record = state["reservations"].get(reservation)
        if not isinstance(key, str) or not key or key in state["charges"] or not record or not record["active"]:
            raise GuardError("duplicate intent or inactive reservation")
        used = sum(c["amount"] for c in state["charges"].values() if c["reservation"] == reservation)
        if amount <= 0 or used + amount > record["cap"]:
            raise GuardError("charge exceeds reservation cap")
        self._event(dict(kind="intent", id=key, reservation=reservation, amount=amount))

    def resolve(self, key: str, *, submitted: bool, evidence: dict) -> None:
        charge = self.snapshot()["charges"].get(key)
        if type(submitted) is not bool or not charge or charge["status"] != "PENDING" or not evidence:
            raise GuardError("resolution needs a pending charge and evidence")
        self._event(dict(kind="charged" if submitted else "not_submitted", id=key, evidence=evidence))

    def reconcile_posted(self, key: str, *, evidence: dict) -> None:
        charge = self.snapshot()["charges"].get(key)
        if not charge or charge["status"] != "CHARGED" or charge["posted"] or not evidence:
            raise GuardError("posted reconciliation needs an unposted charge and evidence")
        self._event(dict(kind="posted", id=key, evidence=evidence))

    def release(self, key: str) -> None:
        state = self.snapshot()
        record = state["reservations"].get(key)
        if not record or not record["active"] or any(
            c["reservation"] == key and c["status"] == "PENDING" for c in state["charges"].values()
        ):
            raise GuardError("cannot release inactive reservation or pending charge")
        self._event(dict(kind="release", id=key))

    def reverse_policy_refusal(self, key: str, *, evidence: dict) -> bool:
        """Reverse an unposted CHARGED take that Flow refused under its content policy.

        Appends one ``policy_refused`` event (net charge 0). Re-running for an
        already reversed take is a no-op and returns False. A posted charge, a
        PENDING intent or a missing evidence record is refused.
        """
        charge = self.snapshot()["charges"].get(key)
        if charge and charge["status"] == "POLICY_REFUSED":
            return False
        if not charge or charge["status"] != "CHARGED" or charge["posted"] or not evidence:
            raise GuardError("policy-refusal reversal needs an unposted CHARGED take and evidence")
        self._event(dict(kind="policy_refused", id=key, evidence=evidence))
        return True

    def export_ai_spend(self, target: Path, *, by: str) -> int:
        """Idempotently export confirmed charges into the shared OWB ai_spend ledger."""
        self._assert_held()
        state = self.snapshot()
        if not isinstance(by, str) or not by.strip():
            raise GuardError("spend export needs a recorder identity")
        target = Path(target).resolve()
        if target == self.path.resolve():
            raise GuardError("spend destination aliases the account ledger")
        rows = []
        events = [json.loads(line) for line in self.path.read_text().splitlines()] if self.path.exists() else []
        for event in events:
            if event["kind"] != "charged":
                continue
            key = event["id"]
            charge = state["charges"][key]
            if charge["status"] == "POLICY_REFUSED":
                continue
            film = state["reservations"][charge["reservation"]]["film"]
            evidence = event["evidence"]
            balances = evidence.get("ui", {}).get("balances", [])
            base = dict(at=event["at"], pool="flow", by=by, source="shared-flow", charge=key)
            if balances:
                if len(balances) != 1 or type(balances[0]) is not int or balances[0] < 0:
                    raise GuardError("invalid confirmed charge balance evidence")
                rows.append(
                    dict(base, id="flow:read:" + key, kind="record", left=balances[0], note="Configured UI before Create")
                )
            rows.append(
                dict(base, id="flow:spend:" + key, kind="spend", amount=charge["amount"], film=film, what=key)
            )
        target.parent.mkdir(parents=True, exist_ok=True)
        with WriterLock(target.with_name(target.name + ".lock")):
            data = target.read_bytes() if target.exists() else b""
            if data and not data.endswith(b"\n"):
                raise GuardError("torn ai_spend ledger; reconcile before export")
            try:
                existing = [json.loads(line) for line in data.splitlines()]
                if any(not isinstance(row, dict) for row in existing):
                    raise ValueError("non-object row")
            except (ValueError, TypeError) as exc:
                raise GuardError("unreadable ai_spend ledger") from exc
            indexed = {}
            for row in existing:
                if "id" in row:
                    if row["id"] in indexed:
                        raise GuardError("duplicate ai_spend receipt identity")
                    indexed[row["id"]] = row
            # A refused take that reached the report before it was reversed is taken back
            # by one more receipt, for exactly the amount written, so the report nets to
            # zero. A refused take that never reached the report writes nothing. Nor does
            # one already taken back, by this receipt or by a correction entered by hand
            # with the ai_spend tool that names the charge.
            for event in events:
                if event["kind"] != "policy_refused":
                    continue
                key = event["id"]
                spent = indexed.get("flow:spend:" + key)
                taken_back = any(
                    row.get("kind") == "spend" and type(row.get("amount")) in (int, float)
                    and row["amount"] < 0 and key in f"{row.get('charge', '')} {row.get('what', '')}"
                    for row in existing)
                if spent is not None and not taken_back:
                    rows.append(dict(at=event["at"], pool="flow", by=by, source="shared-flow",
                                     charge=key, id="flow:reversal:" + key, kind="spend",
                                     amount=-spent["amount"], film=spent["film"],
                                     what=key + " refused by Flow policy, not charged"))
            missing = []
            for row in rows:
                previous = indexed.get(row["id"])
                if previous is not None:
                    if {k: v for k, v in previous.items() if k != "by"} != {k: v for k, v in row.items() if k != "by"}:
                        raise GuardError("ai_spend receipt identity collision")
                else:
                    missing.append(row)
            if missing:
                with target.open("ab") as handle:
                    handle.write(b"".join((json.dumps(row, sort_keys=True) + "\n").encode() for row in missing))
                    handle.flush()
                    os.fsync(handle.fileno())
                directory = os.open(target.parent, os.O_RDONLY)
                try:
                    os.fsync(directory)
                finally:
                    os.close(directory)
            return len(missing)


def process_alive(pid: int) -> bool:
    if pid <= 0:
        return False
    try:
        os.kill(pid, 0)
    except OSError:
        return False
    return True


def refuse_duplicate(pid_path: Path, done_path: Path) -> None:
    """Refuse a second runner process if a live PID is recorded, even if a stale .done exists."""
    if not pid_path.exists():
        return
    try:
        pid = int(pid_path.read_text().strip())
    except ValueError as exc:
        raise GuardError(f"unreadable pid file {pid_path}") from exc
    if process_alive(pid) and pid != os.getpid():
        raise GuardError(f"runner already live as pid {pid}; {done_path.name} will not override active owner")


def runner_state_dir() -> Path:
    return Path.home() / "_desk/state/flow/hos010-twelve-plates"


def detached_command(
    script: Path,
    log_path: Path,
    done_path: Path,
    *,
    repo: Path,
    media: Path,
    archive: Path,
    other: int,
    ledger: Path,
    lock: Path,
    pid: Path,
    authorization_file: Path | None = None,
    session: str = "hos010-twelve-plates",
) -> list[str]:
    """Print-only detached tmux command; never arms generation or overwrites logs."""
    paths = [script, repo, media, archive, ledger, lock, pid, log_path, done_path]
    if authorization_file is not None:
        paths.append(authorization_file)
    if not all(path.is_absolute() for path in paths):
        raise GuardError("detached inputs and state paths must be absolute")
    if not script.is_file() or not repo.is_dir() or not media.is_dir() or not archive.is_dir():
        raise GuardError("detached script/repo/media/archive must already exist")
    if authorization_file is not None and not authorization_file.is_file():
        raise GuardError("detached authorization file must already exist")
    if other < 0 or not re.fullmatch(r"[A-Za-z0-9_-]+", session):
        raise GuardError("invalid reservation or tmux session")
    resolved = [path.resolve() for path in (ledger, lock, pid, log_path, done_path)]
    if len(set(resolved)) != len(resolved):
        raise GuardError("detached state/log/done paths must be distinct")
    if log_path.exists() or done_path.exists():
        raise GuardError("use fresh per-run log and done paths; existing files are preserved")
    args = [
        sys.executable,
        str(script),
        "launch-worker",
        "--repo",
        str(repo),
        "--media",
        str(media),
        "--archive",
        str(archive),
        "--other-reservations",
        str(other),
        "--ledger",
        str(ledger),
        "--lock",
        str(lock),
        "--pid",
        str(pid),
        "--log",
        str(log_path),
        "--done",
        str(done_path),
    ]
    if authorization_file is not None:
        args.extend(["--authorization-file", str(authorization_file)])
    return ["tmux", "new", "-d", "-s", session, shlex.join(args)]


def claim_pid(pid_path: Path, pid: int | None = None) -> None:
    pid_path.parent.mkdir(parents=True, exist_ok=True)
    temporary = pid_path.with_name(pid_path.name + f".{os.getpid()}.tmp")
    immutable_bytes(temporary, (str(os.getpid() if pid is None else pid) + "\n").encode())
    os.replace(temporary, pid_path)


def launch_once(
    command: list[str],
    *,
    ownership: Path,
    pid: Path,
    log: Path,
    done: Path,
) -> int:
    """Exclusive detached runner owner: claims PID under flock before releasing gated child."""
    with WriterLock(ownership):
        refuse_duplicate(pid, done)
        if done.exists():
            raise GuardError("done file already exists; use a fresh run id")
        log.parent.mkdir(parents=True, exist_ok=True)
        done.parent.mkdir(parents=True, exist_ok=True)
        with log.open("xb") as handle:
            gate = (
                "import os,sys; token=os.read(0,1); "
                "sys.exit(125) if token != b'1' else None; "
                "os.execvp(sys.argv[1], sys.argv[1:])"
            )
            child = subprocess.Popen(
                [sys.executable, "-c", gate, *command],
                stdin=subprocess.PIPE,
                stdout=handle,
                stderr=subprocess.STDOUT,
            )
            signalled = False
            try:
                claim_pid(pid, child.pid)
                assert child.stdin is not None
                child.stdin.write(b"1")
                child.stdin.close()
                signalled = True
                code = child.wait()
            except BaseException:
                if child.stdin and not child.stdin.closed:
                    child.stdin.close()
                if not signalled:
                    child.wait(timeout=5)
                raise
        immutable_bytes(done, (str(code) + "\n").encode())
        return code


def append_ledger(path: Path, entry: dict) -> None:
    if entry.get("status") == "KEEP" or entry.get("keep") is True or entry.get("review") == "KEEP":
        raise GuardError("refusing to record KEEP")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a") as handle:
        handle.write(json.dumps(entry, sort_keys=True) + "\n")
        handle.flush()
        os.fsync(handle.fileno())


def read_ledger(path: Path) -> list[dict]:
    if not path.exists():
        return []
    rows = []
    for line in path.read_text().splitlines():
        if line.strip():
            rows.append(json.loads(line))
    return rows


def latest_entries(entries: list[dict]) -> list[dict]:
    latest = {}
    for entry in entries:
        row_id = entry.get("row_id") or f"P{int(entry.get('part') or 0)}:{entry.get('plate_id')}"
        latest[(row_id, int(entry.get("take") or 0))] = entry
    return list(latest.values())


def _entry_row_id(entry: dict) -> str:
    return entry.get("row_id") or f"P{int(entry.get('part') or 0)}:{entry.get('plate_id')}"


def takes_recorded(entries: list[dict], row_id: str) -> set[int]:
    return {int(e.get("take") or 0) for e in entries if _entry_row_id(e) == row_id}


def refused_takes(entries: list[dict]) -> list[dict]:
    """Takes Flow refused under its content policy, in ledger order."""
    return [e for e in latest_entries(entries) if e.get("status") == POLICY_REFUSED]


def rows_set_aside(rows: list[Row], entries: list[dict]) -> list[str]:
    """Rows whose prompt, as it stands in the scope, is one Flow has already refused.

    A refused prompt is not sent again unchanged. When the scope carries a new prompt for the
    row, its hash differs from the refused take's and the row comes back at the next take number.
    """
    refused = {(_entry_row_id(e), e.get("prompt_sha256")) for e in refused_takes(entries)}
    return [row.row_id for row in rows if (row.row_id, row.prompt_sha256) in refused]


def policy_refusal_record(submitting: dict, *, reason: str, evidence: dict) -> dict:
    """Close a SUBMITTING take that Flow refused under its content policy at 0 credits."""
    if not str(reason or "").strip() or not evidence:
        raise GuardError("a policy refusal needs a reason and evidence")
    if not submitting.get("prompt_sha256"):
        raise GuardError("the SUBMITTING take carries no prompt hash; refusing to close it blind")
    return {
        "row_id": _entry_row_id(submitting),
        "plate_id": submitting.get("plate_id"),
        "part": submitting.get("part"),
        "quality": submitting.get("quality"),
        "flow_model": submitting.get("flow_model"),
        "take": int(submitting.get("take") or 0),
        "status": POLICY_REFUSED,
        "file_state": "REFUSED",
        "generated": False,
        "review": "PENDING_REVIEW",
        "keep": False,
        "prompt_sha256": submitting["prompt_sha256"],
        "credits_used": 0,
        "reason": reason,
        "evidence": evidence,
        "at": now_iso(),
    }


def reconcile_policy_refusal(*, accounting_state: Path, ledger_path: Path, lock_path: Path,
                             key: str, plate_id: str, part: int, take: int,
                             reason: str, evidence: dict) -> dict:
    """Append the shared reversal and the twelve-plate ledger's FAILED_POLICY line; idempotent.

    Both ledgers only gain lines, and nothing is submitted. The local line is skipped when the
    take's latest entry is already FAILED_POLICY, so a second run changes nothing.
    """
    row_id = f"P{int(part)}:{plate_id}"
    if row_id not in EXPECTED_ROW_IDS:
        raise GuardError(f"{row_id} is not one of the twelve scoped rows")
    if key != f"{FILM_ID}:P{int(part):02d}:{plate_id}:t{int(take)}":
        raise GuardError("the shared charge id does not belong to this row and take")
    with WriterLock(lock_path), SharedFlowAccounting(accounting_state) as account:
        entries = read_ledger(ledger_path)
        latest = {(_entry_row_id(e), int(e.get("take") or 0)): e for e in entries}
        current = latest.get((row_id, int(take)))
        if current is None or current.get("status") not in ("SUBMITTING", POLICY_REFUSED):
            raise GuardError("policy refusal applies only to a SUBMITTING take")
        if current.get("status") == "SUBMITTING" and current.get("shared_charge") not in (None, key):
            raise GuardError("the twelve-plate ledger names a different shared charge for this take")
        local = current.get("status") != POLICY_REFUSED
        closed = policy_refusal_record(current, reason=reason, evidence=evidence) if local else None
        shared = account.reverse_policy_refusal(key, evidence=evidence)
        if local:
            closed["shared_charge"] = key
            append_ledger(ledger_path, closed)
            entries.append(closed)
        return {
            "shared_appended": shared,
            "local_appended": local,
            "refused_takes": [f"{_entry_row_id(e)}:t{int(e.get('take') or 0)}" for e in refused_takes(entries)],
        }


def submitting_record(row: Row, take: int, dest: Path) -> dict:
    return {
        "row_id": row.row_id,
        "plate_id": row.plate_id,
        "part": row.part,
        "quality": row.quality,
        "flow_model": row.flow_model,
        "take": take,
        "status": "SUBMITTING",
        "file_state": "SUBMITTING",
        "generated": False,
        "review": "PENDING_REVIEW",
        "keep": False,
        "file": str(dest),
        "prompt_sha256": row.prompt_sha256,
        "credits_reserved": row.try1_credits,
        "at": now_iso(),
    }


def review_record(row: Row, take: int, dest: Path, technical: dict) -> dict:
    """Saved as GENERATED / PENDING_REVIEW, never KEEP."""
    return {
        "row_id": row.row_id,
        "plate_id": row.plate_id,
        "part": row.part,
        "quality": row.quality,
        "flow_model": row.flow_model,
        "take": take,
        "status": "PENDING_REVIEW",
        "file_state": "GENERATED",
        "generated": True,
        "review": "PENDING_REVIEW",
        "keep": False,
        "file": str(dest),
        "sha256": technical.get("sha256"),
        "prompt_sha256": row.prompt_sha256,
        "technical": technical,
        "credits_reserved": row.try1_credits,
        "credits_used": row.try1_credits,
        "at": now_iso(),
    }


def technical_report(
    path: Path,
    *,
    required_s: float = 8.0,
    min_width: int = 1280,
    min_height: int = 720,
) -> dict:
    """Decode/format validation only; never implies perceptual KEEP."""
    report = {"ok": False, "review": "PENDING_REVIEW", "keep": False}
    if not path.is_file() or path.stat().st_size < 500:
        return report | {"reason": "missing or tiny"}
    report.update(sha256=sha256_file(path), bytes=path.stat().st_size)
    probe = subprocess.run(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration:stream=codec_type,width,height",
            "-of",
            "json",
            str(path),
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    try:
        payload = json.loads(probe.stdout)
        duration = float(payload["format"]["duration"])
        videos = [v for v in payload["streams"] if v["codec_type"] == "video"]
        audio = sum(v["codec_type"] == "audio" for v in payload["streams"])
        video = videos[0] if len(videos) == 1 else {}
        width, height = int(video.get("width", 0)), int(video.get("height", 0))
    except (ValueError, KeyError, TypeError):
        return report | {"reason": "invalid probe"}
    decode = subprocess.run(
        ["ffmpeg", "-v", "error", "-xerror", "-i", str(path), "-map", "0:v:0", "-f", "null", "-"],
        capture_output=True,
        check=False,
    )
    report.update(
        duration_s=duration,
        audio_streams=audio,
        width=width,
        height=height,
        decode_ok=decode.returncode == 0,
    )
    report["ok"] = bool(
        probe.returncode == 0
        and decode.returncode == 0
        and len(videos) == 1
        and audio == 0
        and duration >= required_s - 0.09
        and width >= min_width
        and height >= min_height
        and abs(width / max(height, 1) - 16 / 9) < 0.02
    )
    return report


def strip_audio(path: Path) -> None:
    silent = path.with_suffix(".silent.mp4")
    subprocess.run(
        ["ffmpeg", "-y", "-v", "error", "-i", str(path), "-c:v", "copy", "-an", str(silent)],
        check=True,
    )
    silent.replace(path)


def immutable_bytes(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        with path.open("xb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
    except FileExistsError:
        if path.read_bytes() != data:
            raise GuardError(f"immutable destination differs: {path}")


def archive_verified(src: Path, dest: Path) -> dict:
    src_hash = sha256_file(src)
    immutable_bytes(dest, src.read_bytes())
    dest_hash = sha256_file(dest)
    if src_hash != dest_hash:
        raise GuardError(f"hash mismatch for {dest}; archive preserved")
    evidence = {"sha256": dest_hash, "dest": str(dest), "verified": True}
    immutable_bytes(
        dest.with_suffix(dest.suffix + ".sha256.json"),
        (json.dumps(evidence, sort_keys=True) + "\n").encode(),
    )
    return evidence


def verify_nas_volume_mounted(target: Path) -> Path:
    resolved = target.resolve()
    volumes = Path("/Volumes")
    if volumes not in resolved.parents:
        raise GuardError(f"NAS path must live under /Volumes/...: {resolved}")
    mount = volumes / resolved.relative_to(volumes).parts[0]
    if not os.path.ismount(mount):
        raise GuardError(f"NAS volume is not mounted: {mount}")
    return resolved


def verify_nas_archive_mounted(archive_dir: Path) -> Path:
    archive = verify_nas_volume_mounted(archive_dir)
    if not archive.is_dir():
        raise GuardError(f"archive directory must already exist: {archive}")
    return archive


def require_archive(archive_dir: Path | None, *, nas: bool = True) -> Path:
    if archive_dir is None:
        raise GuardError("a verified NAS archive directory is mandatory before submit")
    archive = verify_nas_archive_mounted(archive_dir) if nas else archive_dir.resolve()
    if not archive.is_dir():
        raise GuardError("archive directory must already exist")
    probe = archive / (".hos010-twelve-plates-write-probe-" + uuid.uuid4().hex)
    immutable_bytes(probe, b"hos010 twelve-plate archive writable\n")
    if probe.read_bytes() != b"hos010 twelve-plate archive writable\n":
        raise GuardError("archive write verification failed")
    return archive


def write_receipt(path: Path, row_ids: list[str], entries: list[dict]) -> None:
    if any(e.get("keep") is True or e.get("status") == "KEEP" for e in entries):
        raise GuardError("refusing to write KEEP receipt")
    payload = {
        "film": FILM_ID,
        "job": JOB_ID,
        "rows": row_ids,
        "keep": False,
        "file_state": "GENERATED",
        "review": "PENDING_REVIEW",
        "entries": entries,
    }
    immutable_bytes(path, (json.dumps(payload, indent=2, sort_keys=True) + "\n").encode())


def canonical_spend_ledger() -> Path:
    return Path.home() / "YouTube/orbit-with-ben/05_Analytics/ai_spend/ledger.jsonl"


def production_batch_paths(
    *,
    repo: Path,
    accounting_state: Path | None,
    spend_ledger: Path | None,
    inventory_rows: list[Row] | None,
) -> tuple[Path, Path]:
    state = shared_flow_state_dir()
    target = canonical_spend_ledger()
    if accounting_state is not None and Path(accounting_state).resolve() != state.resolve():
        raise GuardError("production requires canonical shared Flow accounting")
    if spend_ledger is not None and Path(spend_ledger).resolve() != target.resolve():
        raise GuardError("production requires canonical OWB spend report")
    if inventory_rows is None:
        raise GuardError("production requires the full locked 12-row scope")
    locked = load_scope(repo)
    if inventory_rows != locked:
        raise GuardError("production inventory differs from the locked 12-row scope")
    return state, target


def next_still_evidence_path(archive_dir: Path, still_filename: str) -> Path:
    first = archive_dir / f"{still_filename}.still.create.json"
    if not first.exists():
        return first
    attempt = 2
    while True:
        candidate = archive_dir / f"{still_filename}.still.attempt{attempt}.create.json"
        if not candidate.exists():
            return candidate
        attempt += 1


def verified_output(entry: dict) -> bool:
    if not (
        entry.get("status") == "PENDING_REVIEW"
        and entry.get("file_state") == "GENERATED"
        and entry.get("generated") is True
        and entry.get("keep") is False
        and (entry.get("technical") or {}).get("ok") is True
        and (entry.get("archive") or {}).get("verified") is True
    ):
        return False
    path = Path(entry.get("file", ""))
    archive = Path(entry["archive"].get("dest", ""))
    return (
        path.is_file()
        and archive.is_file()
        and sha256_file(path) == entry.get("sha256") == sha256_file(archive) == entry["archive"].get("sha256")
    )


def next_batch(rows: list[Row], ledger: list[dict]) -> list[Row]:
    done = {
        entry.get("row_id") or f"P{int(entry.get('part') or 0)}:{entry.get('plate_id')}"
        for entry in latest_entries(ledger)
        if verified_output(entry)
    }
    # A refused prompt is not sent again unchanged. Left in, the row would burn its three takes
    # on the same refusal and then stop every later batch on the take cap.
    waiting = set(rows_set_aside(rows, ledger))
    remaining = [
        row
        for row in order_rows(rows, require_part1_first=True)
        if row.row_id not in done and row.row_id not in waiting
    ]
    if not remaining:
        return []
    return batch_rows(remaining, require_part1_first=False)[0]


def execute_shared_batch(
    batch: list[Row],
    *,
    repo: Path,
    media: Path,
    ledger_path: Path,
    archive_dir: Path,
    accounting_state: Path | None = None,
    spend_ledger: Path | None = None,
    recorder: str = "gemini",
    reservation: str = DEFAULT_RESERVATION,
    other: int | dict[str, int] = 0,
    cap: int = MAX_TOTAL_CREDITS,
    floor: int = HEADROOM_FLOOR,
    authorization_file: Path | None = None,
    batch_price_reader=None,
    submitter=None,
    still_maker=None,
    test_archive: bool = False,
    inventory_rows: list[Row] | None = None,
) -> list[dict]:
    """Execute one guarded twelve-plate batch under SharedFlowAccounting."""
    if type(cap) is not int or cap <= 0 or cap > MAX_TOTAL_CREDITS:
        raise GuardError(f"invalid total credit cap {cap!r}; must be in 1..{MAX_TOTAL_CREDITS}")
    if type(floor) is not int or floor < HEADROOM_FLOOR:
        raise GuardError(f"invalid headroom floor {floor!r}; minimum floor is {HEADROOM_FLOOR}")
    assert_batch_limits(batch)
    if not test_archive:
        auth = require_generation_authorization(repo, authorization_file)
        cap = min(cap, auth.authorized_cap_credits)
        floor = max(floor, auth.minimum_headroom_floor)
        accounting_state, spend_ledger = production_batch_paths(
            repo=repo,
            accounting_state=accounting_state,
            spend_ledger=spend_ledger,
            inventory_rows=inventory_rows,
        )
    if inventory_rows is not None and any(row not in inventory_rows for row in batch):
        raise GuardError("batch contains a row outside the locked 12-row scope")

    # Refuse VO/Option A1 drift or missing/corrupt style & Explorer references BEFORE opening Flow.
    vo_manifest = verify_vo_and_option_a1(repo, media, require_audio_files=not test_archive)
    style_manifest = verify_style_references(repo, media, inventory_rows or batch, check_hashes=not test_archive)
    archive_dir = require_archive(archive_dir, nas=not test_archive)
    submitter = submitter or live_video_submit
    batch_price_reader = batch_price_reader or live_batch_price_reader
    accepts_other = "other" in inspect.signature(submitter).parameters
    accepts_floor = "floor" in inspect.signature(submitter).parameters
    accepts_cap = "cap" in inspect.signature(submitter).parameters

    written: list[dict] = []
    with SharedFlowAccounting(accounting_state) as accounting:
        if spend_ledger is not None:
            accounting.export_ai_spend(spend_ledger, by=recorder)
        snap = accounting.snapshot()
        if snap["pending"]:
            raise GuardError("unresolved shared Create; refusing batch")
        resolved_other = resolve_external_reservations(
            snap, other, own_reservation=reservation, own_film=FILM_ID
        )

        entries = read_ledger(ledger_path)
        if any(e.get("status") == "SUBMITTING" for e in latest_entries(entries)):
            raise GuardError("unresolved local SUBMITTING take; reconcile before batch")
        spent, pending, unknown, takes = ledger_totals(entries, max_total_credits=cap)
        if unknown:
            raise GuardError("unknown pending charge in local ledger")
        for row in batch:
            if takes.get(row.row_id, 0) >= MAX_TAKES_PER_ROW:
                raise GuardError(f"{row.row_id}: row take cap ({MAX_TAKES_PER_ROW}) already reached")
            if spent + pending + row.try1_credits > cap:
                raise GuardError(f"{row.row_id}: batch would exceed {cap} credit cap")
            pending += row.try1_credits

        batch_prices = batch_price_reader()
        verified_prices = accept_batch_prices(batch_prices, now=datetime.now(timezone.utc))

        if still_maker is not None:
            for srow in batch:
                spath = still_path(media, srow.part, srow.plate_id)
                if not spath.is_file():
                    made = Path(
                        still_maker(
                            srow,
                            spath,
                            repo=repo,
                            media=media,
                            accounting=accounting,
                            reservation=reservation,
                            evidence_path=next_still_evidence_path(archive_dir, spath.name),
                            other=resolved_other,
                            cap=cap,
                            floor=floor,
                        )
                    )
                    if not made.is_file():
                        raise GuardError(f"zero-price still for {srow.row_id} was not written")
                    archive_verified(made, archive_dir / made.name)

        inventory = verify_still_inventory(batch, media)
        inventory_payload = {
            "vo": vo_manifest,
            "style_refs": style_manifest,
            "batch_prices": verified_prices,
            "stills": inventory,
        }
        inventory_bytes = (json.dumps(inventory_payload, sort_keys=True) + "\n").encode()
        inventory_id = sha256_bytes(inventory_bytes)
        immutable_bytes(archive_dir / f"inventory-{inventory_id}.json", inventory_bytes)
        inventory_by_row = {item["row_id"]: item for item in inventory}

        for row in batch:
            frame = still_path(media, row.part, row.plate_id)
            expected_still = inventory_by_row.get(row.row_id)
            if (
                expected_still is None
                or Path(expected_still["path"]) != frame.resolve()
                or sha256_file(frame) != expected_still["sha256"]
            ):
                raise GuardError(f"start still changed after inventory on {row.row_id}; refusing Create")

            take, dest = next_version(media, row.part, row.plate_id, used=takes_recorded(entries, row.row_id))
            dest.parent.mkdir(parents=True, exist_ok=True)
            charge = f"{FILM_ID}:P{row.part:02d}:{row.plate_id}:t{take}"
            intent = submitting_record(row, take, dest)
            intent["shared_charge"] = charge
            intent["inventory"] = inventory_id
            intent["input"] = {"file": str(frame.resolve()), "sha256": expected_still["sha256"]}
            append_ledger(ledger_path, intent)

            submit_kwargs: dict = dict(
                accounting=accounting,
                reservation=reservation,
                charge=charge,
                evidence_path=archive_dir / (dest.name + ".create.json"),
            )
            if accepts_other:
                submit_kwargs["other"] = resolved_other
            if accepts_floor:
                submit_kwargs["floor"] = floor
            if accepts_cap:
                submit_kwargs["cap"] = cap

            try:
                evidence = submitter(row, dest, frame, **submit_kwargs)
            finally:
                if spend_ledger is not None:
                    accounting.export_ai_spend(spend_ledger, by=recorder)

            shared = accounting.snapshot()["charges"].get(charge)
            if not shared or shared["status"] != "CHARGED" or shared["amount"] != row.try1_credits:
                raise GuardError(f"submitter returned without exact {row.try1_credits}-credit shared charge")
            if not isinstance(evidence, dict) or evidence.get("charge") != charge:
                raise GuardError("submitter returned without matching per-Create evidence")
            if not dest.is_file():
                raise GuardError("charged output missing; reconcile before retry")

            strip_audio(dest)
            technical = technical_report(dest, required_s=row.required_decode_s)
            entry = review_record(row, take, dest, technical)
            entry.update(
                shared_charge=charge,
                create_evidence=evidence,
                batch_prices=verified_prices,
                inventory=inventory_id,
                input=intent["input"],
                archive=archive_verified(dest, archive_dir / dest.name),
            )
            if not technical["ok"]:
                entry["status"] = "FAILED"
                entry["file_state"] = "FAILED_TECHNICAL"
            write_receipt(archive_dir / (dest.name + ".receipt.json"), [row.row_id], [entry])
            append_ledger(ledger_path, entry)
            entries.append(entry)
            written.append(entry)
            if not technical["ok"]:
                raise GuardError(f"technical validation failed on {row.row_id}: {dest}; stopping batch")

    batch_ids = [r.row_id for r in batch]
    batch_tag = sha256_bytes(",".join(batch_ids).encode("utf-8"))[:12]
    write_receipt(archive_dir / f"batch-{batch_tag}.receipt.json", batch_ids, written)
    return written


def open_flow_page(browser, flow_home: str, goto):
    """Reuse the open Flow tab via cdp_tabs.reuse_page; never spawn duplicate Flow tabs."""
    owb = Path(os.environ.get("OWB_REPO", str(Path.home() / "YouTube/orbit-with-ben")))
    sys.path.insert(0, str(owb / "scripts"))
    from cdp_tabs import reuse_page

    page = reuse_page(browser.contexts[0], FLOW_HOST)
    url = page.url or ""
    if FLOW_HOST in url and "/about" not in url:
        return page
    goto(page, flow_home)
    return page


BALANCE_EVIDENCE_JS = r"""(expected) => {
  const visible = e => { const r = e.getBoundingClientRect();
    const s = getComputedStyle(e);
    return r.width > 0 && r.height > 0 && s.visibility !== 'hidden' && s.display !== 'none'; };
  const unique = a => [...new Set(a)];
  const body = document.body.innerText;
  const accounts = unique([...document.querySelectorAll('[aria-label]')].filter(visible)
    .map(e => e.getAttribute('aria-label')).filter(t => /Google Account|Account details/i.test(t))
    .flatMap(t => t.match(/[A-Z0-9._%+-]+\x40[A-Z0-9.-]+\.[A-Z]{2,}/ig) || [])
    .map(t => t.toLowerCase()));
  const balances = unique([...body.matchAll(/(?:^|\n)\s*([\d,]+)\s+(?:AI|Google Flow) credits\s*(?=\n|$)/g)]
    .map(m => Number(m[1].replace(/,/g, ''))));
  return {
    host: location.hostname,
    accounts,
    balances,
    ultra: body.split('\n').some(t => t.trim() === 'ULTRA')
  };
}"""


def _close_flow_overlays(page) -> None:
    try:
        page.evaluate(
            "() => { for (const b of document.querySelectorAll('.cdk-overlay-backdrop')) b.click(); }",
            None,
        )
    except Exception:
        pass
    try:
        page.keyboard.press("Escape")
    except Exception:
        pass
    try:
        page.wait_for_timeout(300)
    except Exception:
        pass


def read_live_balance(page, *, open_overlay: bool = True) -> int:
    """Read and validate the studio Ultra account + Flow credit balance in its own step."""
    evidence = page.evaluate(BALANCE_EVIDENCE_JS, None)
    opened = False
    if open_overlay and isinstance(evidence, dict) and not evidence.get("balances"):
        try:
            clicked = page.evaluate(
                """() => {
                  const e = document.querySelector('[aria-label="Account details"], [aria-label*="Account details" i], [aria-label*="Google Account" i]');
                  if (e) { e.click(); return true; }
                  return false;
                }""",
                None,
            )
        except Exception:
            clicked = False
        if clicked:
            opened = True
            try:
                page.wait_for_timeout(600)
            except Exception:
                pass
            evidence = page.evaluate(BALANCE_EVIDENCE_JS, None)
    try:
        if not isinstance(evidence, dict) or evidence.get("host") != FLOW_HOST or evidence.get("ultra") is not True:
            raise GuardError("live Flow host or ULTRA entitlement is missing or changed")
        verify_account_list(evidence.get("accounts"))
        balances = evidence.get("balances")
        if not isinstance(balances, list) or len(balances) != 1 or type(balances[0]) is not int or balances[0] < 0:
            raise GuardError("live Flow balance is missing or ambiguous")
        allowed_keys = {"host", "accounts", "ultra", "balances"}
        extra_keys = set(evidence) - allowed_keys
        if extra_keys and extra_keys not in (
            {"models", "outputs", "aspects", "durations", "prices", "create_count"},
            {"models", "outputs", "aspects", "prices", "create_count"},
        ):
            raise GuardError("unknown live Flow balance evidence schema")
        return balances[0]
    finally:
        if opened:
            _close_flow_overlays(page)


def _open_settings_trigger_if_needed(page) -> bool:
    try:
        clicked = page.evaluate(
            """() => {
              if (document.querySelector('button[aria-label="Select model family"]')) return false;
              const e = document.querySelector('button[aria-label="Settings trigger"]');
              if (e) { e.click(); return true; }
              return false;
            }""",
            None,
        )
    except Exception:
        return False
    if clicked:
        try:
            page.wait_for_timeout(600)
        except Exception:
            pass
    return bool(clicked)


CREATE_EVIDENCE_JS = r"""(expected) => {
  const visible = e => { const r = e.getBoundingClientRect();
    const s = getComputedStyle(e);
    return r.width > 0 && r.height > 0 && s.visibility !== 'hidden' && s.display !== 'none'; };
  const text = e => (e.innerText || e.getAttribute('aria-label') || '').trim().replace(/\s+/g, ' ');
  const unique = a => [...new Set(a)];
  const selected = [...document.querySelectorAll(
    '[aria-selected="true"],[aria-checked="true"],[aria-pressed="true"],select option:checked')]
    .filter(visible).map(text);
  const allButtons = [...document.querySelectorAll('button')].filter(visible);
  const modelButtons = allButtons
    .filter(e => e.getAttribute('aria-label') === 'Select model family' &&
      !e.disabled && e.getAttribute('aria-disabled') !== 'true')
    .map(e => (e.innerText || '').trim().replace(/\s+/g, ' ').replace(/\s+arrow_drop_down$/, ''));
  const knownVideoModels = new Set(['Veo 3.1 - Quality', 'Veo 3.1 - Fast', 'Veo 3.1 - Lite']);
  const models = modelButtons.some(t => !knownVideoModels.has(t))
    ? []
    : unique([...selected.filter(t => knownVideoModels.has(t)), ...modelButtons]);
  const aspectMap = {
    '16:9': '16:9', 'crop_16_9 16:9': '16:9',
    '9:16': '9:16', 'crop_9_16 9:16': '9:16',
    '4:3': '4:3', 'crop_landscape 4:3': '4:3',
    '1:1': '1:1', 'crop_square 1:1': '1:1',
    '3:4': '3:4', 'crop_portrait 3:4': '3:4'
  };
  const body = document.body.innerText;
  const accounts = unique([...document.querySelectorAll('[aria-label]')].filter(visible)
    .map(e => e.getAttribute('aria-label')).filter(t => /Google Account|Account details/i.test(t))
    .flatMap(t => t.match(/[A-Z0-9._%+-]+\x40[A-Z0-9.-]+\.[A-Z]{2,}/ig) || [])
    .map(t => t.toLowerCase()));
  const prices = unique(body.split('\n').map(t => t.trim())
    .filter(t => /^Generating will use \d+ credits$/.test(t)));
  const balances = unique([...body.matchAll(/(?:^|\n)\s*([\d,]+)\s+(?:AI|Google Flow) credits\s*(?=\n|$)/g)]
    .map(m => Number(m[1].replace(/,/g, ''))));
  const buttons = allButtons.filter(e => {
    const t = text(e); return (t === 'Create' || t === 'Start generation' || t === 'arrow_forward') &&
      !e.disabled && e.getAttribute('aria-disabled') !== 'true'; });
  const evidence = {
    host: location.hostname,
    models,
    outputs: unique(selected.filter(t => /^x[1234]$/.test(t))),
    aspects: unique(selected.map(t => aspectMap[t]).filter(Boolean)),
    durations: unique(selected.filter(t => /^\d+s$/.test(t))),
    accounts, prices, balances,
    ultra: body.split('\n').some(t => t.trim() === 'ULTRA'),
    create_count: buttons.length
  };
  if (expected === null) return evidence;
  if (JSON.stringify(evidence) !== JSON.stringify(expected))
    return {ready: false, reason: 'live UI changed', evidence};
  if (buttons.length !== 1) return {ready: false, reason: 'Create not unique', evidence};
  const rect = buttons[0].getBoundingClientRect();
  if (!Number.isFinite(rect.left) || !Number.isFinite(rect.top) || !(rect.width > 0 && rect.height > 0))
    return {ready: false, reason: 'Create geometry invalid', evidence};
  const cx = rect.left + rect.width / 2;
  const cy = rect.top + rect.height / 2;
  if (typeof innerWidth === 'number' && typeof innerHeight === 'number' &&
      (cx < 0 || cy < 0 || cx > innerWidth || cy > innerHeight))
    return {ready: false, reason: 'Create outside viewport', evidence};
  if (typeof document.elementFromPoint === 'function') {
    const hit = document.elementFromPoint(cx, cy);
    if (!hit || (hit !== buttons[0] && !(typeof buttons[0].contains === 'function' && buttons[0].contains(hit))))
      return {ready: false, reason: 'Create obstructed', evidence};
  }
  return {ready: true, target: {x: cx, y: cy}, evidence};
}"""


def _resolve_evidence_balances(raw: dict, balance: int | None) -> list[int]:
    balances = raw.get("balances")
    if not isinstance(balances, list):
        raise GuardError("live Flow balance is missing or ambiguous")
    if len(balances) == 0 and balance is not None:
        if type(balance) is not int or balance < 0:
            raise GuardError("live Flow balance is missing or ambiguous")
        return [balance]
    if len(balances) == 1 and type(balances[0]) is int and balances[0] >= 0:
        if balance is not None and (type(balance) is not int or balances[0] != balance):
            raise GuardError("live Flow balance is missing or ambiguous")
        return list(balances)
    raise GuardError("live Flow balance is missing or ambiguous")


def _scrub_evidence_accounts(raw: dict, balances: list[int], account_digest: str) -> dict:
    clean = {k: v for k, v in raw.items() if k != "accounts"}
    clean["balances"] = balances
    clean["account_sha256"] = account_digest
    clean["account_verified"] = True
    return clean


def _read_and_validate_live_evidence(
    page,
    *,
    quality: str = REQUIRED_QUALITY,
    balance: int | None = None,
    open_overlay: bool = False,
    require_enabled_create: bool = True,
) -> tuple[dict, dict]:
    expected_model = expected_model_for(quality)
    expected_cost = expected_credits_for(quality)
    raw = page.evaluate(CREATE_EVIDENCE_JS, None)
    if (
        open_overlay
        and isinstance(raw, dict)
        and not raw.get("models")
        and not raw.get("prices")
        and _open_settings_trigger_if_needed(page)
    ):
        raw = page.evaluate(CREATE_EVIDENCE_JS, None)
    if not isinstance(raw, dict):
        raise GuardError("live Flow evidence is not an object")
    expected_keys = {
        "host",
        "models",
        "outputs",
        "aspects",
        "durations",
        "accounts",
        "prices",
        "balances",
        "ultra",
        "create_count",
    }
    if set(raw) != expected_keys:
        raise GuardError("unknown live Flow evidence schema")
    account_digest = verify_account_list(raw.get("accounts"))
    required = dict(
        host=FLOW_HOST,
        models=[expected_model],
        outputs=[REQUIRED_OUTPUTS],
        aspects=[REQUIRED_ASPECT],
        durations=[REQUIRED_DURATION],
        prices=[f"Generating will use {expected_cost} credits"],
        ultra=True,
    )
    if any(raw.get(k) != v for k, v in required.items()):
        raise GuardError(
            f"live Flow selected controls/entitlement/price do not match {quality} ({expected_model}, {expected_cost} credits)"
        )
    if require_enabled_create and raw.get("create_count") != 1:
        raise GuardError("live Flow Create button is missing, disabled or ambiguous")
    balances = _resolve_evidence_balances(raw, balance)
    return raw, _scrub_evidence_accounts(raw, balances, account_digest)


def read_live_evidence(
    page,
    *,
    quality: str = REQUIRED_QUALITY,
    balance: int | None = None,
    open_overlay: bool = False,
) -> dict:
    _raw, evidence = _read_and_validate_live_evidence(
        page, quality=quality, balance=balance, open_overlay=open_overlay
    )
    return evidence


def _extract_trusted_click_target(target: object) -> tuple[float, float] | None:
    if not isinstance(target, dict):
        return None
    x, y = target.get("x"), target.get("y")
    if (
        isinstance(x, bool)
        or isinstance(y, bool)
        or not isinstance(x, (int, float))
        or not isinstance(y, (int, float))
        or not math.isfinite(x)
        or not math.isfinite(y)
    ):
        return None
    return float(x), float(y)


def guarded_create(
    page,
    accounting: SharedFlowAccounting,
    *,
    row: Row,
    reservation: str,
    charge: str,
    evidence_path: Path,
    floor: int = HEADROOM_FLOOR,
    balance: int | None = None,
) -> dict:
    """Atomic per-row Create guard: validates Veo 3.1 - Quality x1 8s 100-credit state, logs intent, clicks."""
    accounting._assert_held()
    expected_cost = expected_credits_for(row)
    if row.try1_credits != expected_cost:
        raise GuardError(f"row {row.row_id} cost {row.try1_credits} != {expected_cost}")
    raw, evidence = _read_and_validate_live_evidence(page, quality=row.quality, balance=balance)
    record = dict(
        read_at=now_iso(),
        row_id=row.row_id,
        quality=row.quality,
        credits=expected_cost,
        ui=evidence,
        charge=charge,
        reservation=reservation,
    )
    immutable_bytes(evidence_path, (json.dumps(record, sort_keys=True) + "\n").encode())
    accounting.intent(charge, reservation, expected_cost, live=evidence["balances"][0], floor=floor)
    outcome = page.evaluate(CREATE_EVIDENCE_JS, raw)
    if not isinstance(outcome, dict) or type(outcome.get("ready")) is not bool:
        raise GuardError("ambiguous Create precheck outcome; shared charge remains pending")
    if not outcome["ready"]:
        accounting.resolve(
            charge,
            submitted=False,
            evidence=dict(reason=outcome.get("reason"), read_at=record["read_at"]),
        )
        raise GuardError("live UI drift before Create; no submission")
    coords = _extract_trusted_click_target(outcome.get("target"))
    mouse = getattr(page, "mouse", None)
    if coords is None or mouse is None or not callable(getattr(mouse, "click", None)):
        accounting.resolve(
            charge,
            submitted=False,
            evidence=dict(reason="missing trusted click target or mouse adapter", read_at=record["read_at"]),
        )
        raise GuardError("missing trusted Create click target or mouse adapter; no submission")
    mouse.click(coords[0], coords[1])
    accounting.resolve(
        charge,
        submitted=True,
        evidence=dict(ui=evidence, target=dict(x=coords[0], y=coords[1]), read_at=record["read_at"]),
    )
    return record


STILL_EVIDENCE_JS = r"""(expected) => {
  const visible = e => { const r = e.getBoundingClientRect();
    const s = getComputedStyle(e);
    return r.width > 0 && r.height > 0 && s.visibility !== 'hidden' && s.display !== 'none'; };
  const text = e => (e.innerText || e.getAttribute('aria-label') || '').trim().replace(/\s+/g, ' ');
  const unique = a => [...new Set(a)];
  const selected = [...document.querySelectorAll(
    '[aria-selected="true"],[aria-checked="true"],[aria-pressed="true"],select option:checked')]
    .filter(visible).map(text);
  const allButtons = [...document.querySelectorAll('button')].filter(visible);
  const modelButtons = allButtons
    .filter(e => e.getAttribute('aria-label') === 'Select model family' &&
      !e.disabled && e.getAttribute('aria-disabled') !== 'true')
    .map(e => (e.innerText || '').trim().replace(/\s+/g, ' ')
      .replace(/\s+arrow_drop_down$/, '').replace(/^🍌\s+/, ''));
  const knownStillModels = new Set(['Nano Banana 2', 'Nano Banana 2.1']);
  const models = modelButtons.some(t => !knownStillModels.has(t))
    ? []
    : unique([...selected.map(t => t.replace(/^🍌\s+/, '')).filter(t => knownStillModels.has(t)), ...modelButtons]);
  const aspectMap = {
    '16:9': '16:9', 'crop_16_9 16:9': '16:9',
    '9:16': '9:16', 'crop_9_16 9:16': '9:16',
    '4:3': '4:3', 'crop_landscape 4:3': '4:3',
    '1:1': '1:1', 'crop_square 1:1': '1:1',
    '3:4': '3:4', 'crop_portrait 3:4': '3:4'
  };
  const body = document.body.innerText;
  const accounts = unique([...document.querySelectorAll('[aria-label]')].filter(visible)
    .map(e => e.getAttribute('aria-label')).filter(t => /Google Account|Account details/i.test(t))
    .flatMap(t => t.match(/[A-Z0-9._%+-]+\x40[A-Z0-9.-]+\.[A-Z]{2,}/ig) || [])
    .map(t => t.toLowerCase()));
  const prices = unique(body.split('\n').map(t => t.trim())
    .filter(t => /^Generating will use \d+ credits$/.test(t)));
  const balances = unique([...body.matchAll(/(?:^|\n)\s*([\d,]+)\s+(?:AI|Google Flow) credits\s*(?=\n|$)/g)]
    .map(m => Number(m[1].replace(/,/g, ''))));
  const buttons = allButtons.filter(e => {
    const t = text(e); return (t === 'Create' || t === 'Start generation' || t === 'arrow_forward') &&
      !e.disabled && e.getAttribute('aria-disabled') !== 'true'; });
  const evidence = {
    host: location.hostname,
    models,
    outputs: unique(selected.filter(t => /^x[1234]$/.test(t))),
    aspects: unique(selected.map(t => aspectMap[t]).filter(Boolean)),
    accounts, prices, balances,
    ultra: body.split('\n').some(t => t.trim() === 'ULTRA'),
    create_count: buttons.length
  };
  if (expected === null) return evidence;
  if (JSON.stringify(evidence) !== JSON.stringify(expected))
    return {ready: false, reason: 'live UI changed', evidence};
  if (buttons.length !== 1) return {ready: false, reason: 'Create not unique', evidence};
  const rect = buttons[0].getBoundingClientRect();
  if (!Number.isFinite(rect.left) || !Number.isFinite(rect.top) || !(rect.width > 0 && rect.height > 0))
    return {ready: false, reason: 'Create geometry invalid', evidence};
  const cx = rect.left + rect.width / 2;
  const cy = rect.top + rect.height / 2;
  if (typeof innerWidth === 'number' && typeof innerHeight === 'number' &&
      (cx < 0 || cy < 0 || cx > innerWidth || cy > innerHeight))
    return {ready: false, reason: 'Create outside viewport', evidence};
  if (typeof document.elementFromPoint === 'function') {
    const hit = document.elementFromPoint(cx, cy);
    if (!hit || (hit !== buttons[0] && !(typeof buttons[0].contains === 'function' && buttons[0].contains(hit))))
      return {ready: false, reason: 'Create obstructed', evidence};
  }
  return {ready: true, target: {x: cx, y: cy}, evidence};
}"""


def _read_and_validate_live_still_evidence(
    page,
    *,
    balance: int | None = None,
    open_overlay: bool = False,
) -> tuple[dict, dict]:
    raw = page.evaluate(STILL_EVIDENCE_JS, None)
    if (
        open_overlay
        and isinstance(raw, dict)
        and not raw.get("models")
        and not raw.get("prices")
        and _open_settings_trigger_if_needed(page)
    ):
        raw = page.evaluate(STILL_EVIDENCE_JS, None)
    if not isinstance(raw, dict):
        raise GuardError("live Flow still evidence is not an object")
    expected_keys = {
        "host",
        "models",
        "outputs",
        "aspects",
        "accounts",
        "prices",
        "balances",
        "ultra",
        "create_count",
    }
    if set(raw) != expected_keys:
        raise GuardError("unknown live Flow still evidence schema")
    account_digest = verify_account_list(raw.get("accounts"))
    required = dict(
        host=FLOW_HOST,
        models=[REQUIRED_STILL_MODEL],
        outputs=[REQUIRED_OUTPUTS],
        aspects=[REQUIRED_ASPECT],
        prices=["Generating will use 0 credits"],
        ultra=True,
        create_count=1,
    )
    if any(raw.get(k) != v for k, v in required.items()):
        raise GuardError("live Flow still selected controls/entitlement/zero-price are missing or changed")
    balances = _resolve_evidence_balances(raw, balance)
    return raw, _scrub_evidence_accounts(raw, balances, account_digest)


def read_live_still_evidence(page, *, balance: int | None = None, open_overlay: bool = False) -> dict:
    _raw, evidence = _read_and_validate_live_still_evidence(page, balance=balance, open_overlay=open_overlay)
    return evidence


def guarded_still_create(
    page,
    accounting: SharedFlowAccounting,
    *,
    reservation: str,
    row: Row,
    evidence_path: Path,
    floor: int = HEADROOM_FLOOR,
    balance: int | None = None,
) -> dict:
    accounting._assert_held()
    state = accounting.snapshot()
    raw, evidence = _read_and_validate_live_still_evidence(page, balance=balance)
    if state["pending"] or evidence["balances"][0] - state["liability"] < floor:
        raise GuardError("pending charge or insufficient shared Flow headroom for still")
    record = dict(
        read_at=now_iso(),
        row_id=row.row_id,
        plate_id=row.plate_id,
        ui=evidence,
        reservation=reservation,
        credits=0,
    )
    immutable_bytes(evidence_path, (json.dumps(record, sort_keys=True) + "\n").encode())
    outcome = page.evaluate(STILL_EVIDENCE_JS, raw)
    if not isinstance(outcome, dict) or type(outcome.get("ready")) is not bool:
        raise GuardError("ambiguous still Create precheck outcome; stopping before video generation")
    if not outcome["ready"]:
        raise GuardError("live UI drift before still Create; no submission")
    coords = _extract_trusted_click_target(outcome.get("target"))
    mouse = getattr(page, "mouse", None)
    if coords is None or mouse is None or not callable(getattr(mouse, "click", None)):
        raise GuardError("missing trusted still Create click target or mouse adapter; no submission")
    mouse.click(coords[0], coords[1])
    return record


def read_live_batch_prices_on_page(page, *, configure_model) -> dict[str, PriceEvidence]:
    """Read live Quality (100-credit) price on Flow without clicking Create."""
    live_balance = read_live_balance(page)
    configure_model(page, REQUIRED_MODEL)
    _raw, evidence = _read_and_validate_live_evidence(
        page,
        quality=REQUIRED_QUALITY,
        balance=live_balance,
        open_overlay=True,
        require_enabled_create=False,
    )
    _close_flow_overlays(page)
    price_line = evidence["prices"][0]
    credits = int(GENERATE_LINE_RE.match(price_line).group(1))
    out = {
        REQUIRED_QUALITY: PriceEvidence(
            quality=REQUIRED_QUALITY,
            model=evidence["models"][0],
            outputs=evidence["outputs"][0],
            aspect=evidence["aspects"][0],
            duration=evidence["durations"][0],
            credits=credits,
            generate_line=price_line,
            read_at=now_iso(),
        )
    }
    accept_batch_prices(out, now=datetime.now(timezone.utc))
    return out


def live_batch_price_reader() -> dict[str, PriceEvidence]:
    """Live pre-batch price reader via CDP :9222. Unreachable unless submit is armed."""
    if os.environ.get(SUBMIT_ENV) != "1":
        raise GuardError("live batch price reader is not armed")
    repo = repo_root_from()
    sys.path.insert(0, str(repo / "04_Audio/tools"))
    import orbit_flow_veo_ui as flow
    from playwright.sync_api import sync_playwright

    cdp = os.environ.get("ORBIT_FLOW_CDP", "http://127.0.0.1:9222")
    with sync_playwright() as playwright:
        browser = playwright.chromium.connect_over_cdp(cdp)
        page = open_flow_page(
            browser,
            flow.FLOW_HOME,
            lambda current, url: current.goto(url, wait_until="domcontentloaded", timeout=120_000),
        )
        if "/project/" not in (page.url or ""):
            flow.ensure_project(page)
        return read_live_batch_prices_on_page(
            page,
            configure_model=lambda p, m: flow.configure_veo_settings(
                p, model=m, frames_mode=True, ingredients_mode=False
            ),
        )


def still_prompt_for_row(still_tool, row: Row) -> str:
    core = " ".join(row.prompt.split())
    if row.explorer:
        core = core.replace("No Explorer.", "") + " " + EXPLORER_LOCK
    return still_tool.still_prompt(
        "History of Science locked look: premium Animistry-class 3D cartoon, finished materials, warm cinematic period light.",
        core + " Opening frame only. No readable words, numbers, letters or text anywhere.",
    )


def video_prompt_for_row(row: Row) -> str:
    core = " ".join(row.prompt.split())
    if row.explorer:
        core = core.replace("No Explorer.", "") + " " + EXPLORER_LOCK
    return (
        "Animate the attached start frame; keep its exact cartoon look, objects and light. "
        + core
        + " Silent picture only. Continuous real camera and subject motion through the final frame."
        + " No readable handwriting, letters or numbers anywhere."
    )


def live_still_maker(
    row: Row,
    dest: Path,
    *,
    repo: Path,
    media: Path,
    accounting: SharedFlowAccounting | None = None,
    reservation: str = DEFAULT_RESERVATION,
    evidence_path: Path | None = None,
    other: int = 0,
    cap: int = MAX_TOTAL_CREDITS,
    floor: int = HEADROOM_FLOOR,
) -> Path:
    """Zero-credit start still maker under SharedFlowAccounting."""
    if os.environ.get(SUBMIT_ENV) != "1":
        raise GuardError(f"live still generation is not armed for {row.row_id}")
    if type(other) is not int or other < 0 or type(floor) is not int or floor < HEADROOM_FLOOR:
        raise GuardError("invalid floor or other reservations")
    if accounting is None or evidence_path is None:
        raise GuardError(f"still generation for {row.row_id} requires SharedFlowAccounting and evidence_path")
    accounting._assert_held()

    verified_refs = verify_style_references(repo, media, [row])
    style_paths = [Path(item["path"]) for item in verified_refs["house"]]
    if row.explorer and verified_refs["explorer"] is not None:
        style_paths.append(Path(verified_refs["explorer"]["path"]))

    sys.path.insert(0, str(repo / "04_Audio/tools"))
    sys.path.insert(0, str(repo / "02_Video-Projects/006_Trees-Are-Made-Of-Air/07_Edit-Project"))
    import _flow_still_v01 as still_tool
    import orbit_flow_veo_ui as flow
    from playwright.sync_api import sync_playwright

    cdp = os.environ.get("ORBIT_FLOW_CDP", "http://127.0.0.1:9222")
    effective_floor = floor + other
    prompt = still_prompt_for_row(still_tool, row)

    with sync_playwright() as playwright:
        browser = playwright.chromium.connect_over_cdp(cdp)
        page = open_flow_page(
            browser,
            flow.FLOW_HOME,
            lambda current, url: current.goto(url, wait_until="domcontentloaded", timeout=120_000),
        )
        evidence = {}

        def create_guard(configured_page):
            live_balance = read_live_balance(configured_page)
            ui = read_live_still_evidence(configured_page, balance=live_balance, open_overlay=True)
            accounting.reserve(reservation, FILM_ID, cap, live=ui["balances"][0], floor=effective_floor)
            evidence.update(
                guarded_still_create(
                    configured_page,
                    accounting,
                    reservation=reservation,
                    row=row,
                    evidence_path=evidence_path,
                    floor=effective_floor,
                    balance=live_balance,
                )
            )

        still_tool.make_still(
            page,
            prompt,
            dest,
            timeout_s=300,
            create_guard=create_guard,
            style_refs=style_paths,
            media_root=media,
        )
        after_balance = read_live_balance(page)
        if after_balance < evidence["ui"]["balances"][0]:
            raise GuardError(f"zero-price still reduced Flow balance on {row.row_id}")

    if not dest.is_file():
        raise GuardError(f"zero-price still for {row.row_id} was not written")
    immutable_bytes(dest.with_suffix(".sha256"), (sha256_file(dest) + "\n").encode())
    return dest


def live_video_submit(
    row: Row,
    dest: Path,
    frame: Path,
    *,
    accounting: SharedFlowAccounting,
    reservation: str,
    charge: str,
    evidence_path: Path,
    other: int = 0,
    cap: int = MAX_TOTAL_CREDITS,
    floor: int = HEADROOM_FLOOR,
) -> dict:
    """Real Flow video submission. Unreachable unless HOS010_TWELVE_PLATES_SUBMIT=1."""
    if os.environ.get(SUBMIT_ENV) != "1":
        raise GuardError("live submit is not armed")
    if type(other) is not int or other < 0 or type(floor) is not int or floor < HEADROOM_FLOOR:
        raise GuardError("invalid floor or other reservations")
    accounting._assert_held()
    repo = repo_root_from()
    sys.path.insert(0, str(repo / "04_Audio/tools"))
    import orbit_flow_veo_ui as flow
    from playwright.sync_api import sync_playwright

    model = expected_model_for(row)
    os.environ["ORBIT_FLOW_VEO_MODEL"] = model
    prompt = video_prompt_for_row(row)
    cdp = os.environ.get("ORBIT_FLOW_CDP", "http://127.0.0.1:9222")
    effective_floor = floor + other

    with sync_playwright() as playwright:
        browser = playwright.chromium.connect_over_cdp(cdp)
        page = open_flow_page(
            browser,
            flow.FLOW_HOME,
            lambda current, url: current.goto(url, wait_until="domcontentloaded", timeout=120_000),
        )
        evidence = {}

        def create_guard(configured_page):
            live_balance = read_live_balance(configured_page)
            ui = read_live_evidence(configured_page, quality=row.quality, balance=live_balance, open_overlay=True)
            accounting.reserve(reservation, FILM_ID, cap, live=ui["balances"][0], floor=effective_floor)
            evidence.update(
                guarded_create(
                    configured_page,
                    accounting,
                    row=row,
                    reservation=reservation,
                    charge=charge,
                    evidence_path=evidence_path,
                    floor=effective_floor,
                    balance=live_balance,
                )
            )

        flow.generate_clip(
            page,
            prompt,
            dest,
            model=model,
            timeout_s=700,
            start_frame=frame,
            attempts=1,
            reuse_project=False,
            create_guard=create_guard,
        )
        before_balance = evidence["ui"]["balances"][0]
        after_balance = read_live_balance(page)
        delta = before_balance - after_balance
        expected_cost = expected_credits_for(row)
        if delta > expected_cost:
            raise GuardError(
                f"Flow balance dropped by {delta} credits (> expected {expected_cost}) on {row.row_id}"
            )
        if delta == expected_cost:
            accounting.reconcile_posted(
                charge,
                evidence=dict(
                    before=before_balance,
                    after=after_balance,
                    delta=delta,
                    reconciled_at=now_iso(),
                ),
            )
    return evidence


def latest_recorded_flow_balance(spend_ledger: Path | None = None) -> dict | None:
    target = spend_ledger or canonical_spend_ledger()
    if not target.is_file():
        return None
    latest = None
    for line in target.read_text().splitlines():
        if not line.strip():
            continue
        row = json.loads(line)
        left = row.get("left")
        if (
            row.get("pool") == "flow"
            and row.get("kind") == "record"
            and isinstance(left, (int, float))
            and not isinstance(left, bool)
            and float(left).is_integer()
        ):
            latest = {"left": int(left), "at": row.get("at"), "by": row.get("by", "")}
    return latest


def build_dry_run_report(
    repo: Path,
    *,
    media: Path,
    archive_dir: Path,
    other: int | dict[str, int] = 0,
    floor: int = HEADROOM_FLOOR,
    require_staged: bool = False,
    authorization_file: Path | None = None,
    accounting_state: Path | None = None,
    spend_ledger: Path | None = None,
) -> dict:
    """Zero-browser, zero-spend, zero-NAS-write readiness & guard verification."""
    if type(floor) is not int or floor < HEADROOM_FLOOR:
        raise GuardError(f"headroom floor cannot be below {HEADROOM_FLOOR}")
    rows = load_scope(repo)
    plan = build_plan(rows, repo=repo)
    vo_report = verify_vo_and_option_a1(repo, media, require_audio_files=require_staged)
    explorer_ref = verify_explorer_reference(repo, rows)

    staging_blockers: list[str] = []
    auth_info: dict | None = None
    try:
        auth = require_generation_authorization(repo, authorization_file)
        auth_info = {
            "authorized": True,
            "job": auth.job,
            "authorized_cap_credits": auth.authorized_cap_credits,
            "minimum_headroom_floor": auth.minimum_headroom_floor,
            "j2033_done": auth.j2033_done,
        }
    except GuardError as exc:
        if require_staged:
            raise
        auth_info = {"authorized": False, "reason": str(exc)}
        staging_blockers.append(str(exc))

    try:
        style_refs = verify_style_references(repo, media, rows)
    except GuardError as exc:
        if require_staged:
            raise
        style_refs = {"house": [], "explorer": explorer_ref, "staged": False, "reason": str(exc)}
        staging_blockers.append(str(exc))

    nas_media = verify_nas_volume_mounted(media)
    if not nas_media.is_dir():
        raise GuardError(f"NAS media directory missing: {nas_media}")
    if require_staged:
        archive_checked = verify_nas_archive_mounted(archive_dir)
        archive_status = {"path": str(archive_checked), "exists": True, "mounted_under_volumes": True}
    else:
        verify_nas_volume_mounted(archive_dir)
        archive_exists = archive_dir.is_dir()
        if not archive_exists:
            staging_blockers.append(f"NAS archive directory not yet created (created at J2270): {archive_dir}")
        archive_status = {"path": str(archive_dir), "exists": archive_exists, "mounted_under_volumes": True}

    shared = SharedFlowAccounting.peek_readonly(accounting_state)
    resolved_other = resolve_external_reservations(
        shared, other, own_reservation=DEFAULT_RESERVATION, own_film=FILM_ID
    )
    recorded = latest_recorded_flow_balance(spend_ledger)
    balance_left = recorded["left"] if recorded else None
    liability = shared["liability"]
    own_already_active = DEFAULT_RESERVATION in {
        k for k, v in shared["reservations"].items() if v.get("active")
    }
    own_additional = 0 if own_already_active else MAX_TOTAL_CREDITS
    projected_after_010 = (
        balance_left - liability - resolved_other - own_additional if balance_left is not None else None
    )
    active_reservations = {
        key: {"film": val["film"], "cap": val["cap"]}
        for key, val in shared["reservations"].items()
        if val["active"]
    }
    return {
        "job": JOB_ID,
        "film": FILM_ID,
        "generated_at": now_iso(),
        "mode": "dry-run (no browser, no Create click, no NAS writes, 0 submissions, 0 credits spent)",
        "submissions": 0,
        "create_clicks": 0,
        "credits_spent": 0,
        "keep": False,
        "submit_armed": submit_armed(),
        "authorization": auth_info,
        "scope_verified": {
            "rows": plan["row_count"],
            "shared_long_rows": plan["shared_long_row_count"],
            "shorts_only_rows": plan["shorts_only_row_count"],
            "explorer_row_id": plan["explorer_row_id"],
            "try1_credits": TRY1_TOTAL_CREDITS,
            "proposed_cap_credits": MAX_TOTAL_CREDITS,
            "max_takes_per_row": MAX_TAKES_PER_ROW,
            "batch_count": len(plan["batches"]),
            "max_batch_rows": MAX_BATCH_ROWS,
            "max_batch_credits": MAX_BATCH_CREDITS,
            "first_row": plan["order"][0]["row_id"],
            "last_row": plan["order"][-1]["row_id"],
        },
        "vo_and_option_a1_verified": vo_report,
        "style_refs_verified": style_refs,
        "nas_archive_status": archive_status,
        "staging_blockers": staging_blockers,
        "shared_accounting_readonly": {
            "active_reservations": active_reservations,
            "unposted_charges": shared["unposted"],
            "remaining_reservations": shared["remaining_reservations"],
            "total_liability": liability,
            "has_pending_charge": shared["pending"],
            "external_reservations_deduplicated": resolved_other,
            "floor": floor,
            "latest_recorded_flow_balance": recorded,
            "projected_headroom_after_3600_cap": projected_after_010,
            "would_allow_3600_reserve_at_recorded_balance": (
                bool(not shared["pending"] and projected_after_010 is not None and projected_after_010 >= floor)
            ),
        },
        "per_part": plan["per_part"],
        "batches": plan["batches"],
    }


def cmd_plan(repo: Path, out: Path | None) -> dict:
    plan = build_plan(load_scope(repo), repo=repo)
    if plan["submissions"] != 0 or plan["create_clicks"] != 0 or plan["keep"] is not False:
        raise GuardError("plan tried to submit or keep")
    text = json.dumps(plan, indent=2) + "\n"
    if out is not None:
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(text)
    else:
        sys.stdout.write(text)
    return plan


def cmd_dry_run(
    repo: Path,
    *,
    media: Path,
    archive_dir: Path,
    other: int,
    floor: int,
    require_staged: bool,
    authorization_file: Path | None,
    out: Path | None,
) -> dict:
    report = build_dry_run_report(
        repo,
        media=media,
        archive_dir=archive_dir,
        other=other,
        floor=floor,
        require_staged=require_staged,
        authorization_file=authorization_file,
    )
    if report["submissions"] != 0 or report["create_clicks"] != 0 or report["keep"] is not False:
        raise GuardError("dry-run tried to submit or keep")
    text = json.dumps(report, indent=2) + "\n"
    if out is not None:
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(text)
    else:
        sys.stdout.write(text)
    return report


def submit_armed(env: dict | None = None) -> bool:
    return (env if env is not None else os.environ).get(SUBMIT_ENV) == "1"


def cmd_submit(
    repo: Path,
    *,
    other: int | dict[str, int],
    floor: int = HEADROOM_FLOOR,
    cap: int = MAX_TOTAL_CREDITS,
    reservation: str = DEFAULT_RESERVATION,
    media: Path,
    ledger_path: Path,
    lock_path: Path,
    pid_path: Path,
    done_path: Path,
    archive_dir: Path | None,
    authorization_file: Path | None = None,
    accounting_state: Path | None = None,
    spend_ledger: Path | None = None,
    recorder: str = "gemini",
    batch_price_reader=None,
    submitter=None,
    still_maker=None,
    test_archive: bool = False,
) -> list[dict]:
    """Run one guarded twelve-plate batch ONLY when armed AND explicitly authorized by J2269."""
    if not submit_armed():
        raise SystemExit(
            "refusing submit: generation is not armed "
            f"({SUBMIT_ENV} is not 1). Plan / dry-run only until {AUTH_JOB_ID} / {PRODUCER_JOB_ID}."
        )
    auth = require_generation_authorization(repo, authorization_file)
    effective_cap = min(cap, auth.authorized_cap_credits)
    effective_floor = max(floor, auth.minimum_headroom_floor)
    refuse_duplicate(pid_path, done_path)
    with WriterLock(lock_path):
        claim_pid(pid_path)
        rows = load_scope(repo)
        entries = read_ledger(ledger_path)
        batch = next_batch(rows, entries)
        if not batch:
            return []
        return execute_shared_batch(
            batch,
            repo=repo,
            media=media,
            ledger_path=ledger_path,
            archive_dir=archive_dir,
            accounting_state=accounting_state,
            spend_ledger=spend_ledger,
            recorder=recorder,
            reservation=reservation,
            other=other,
            cap=effective_cap,
            floor=effective_floor,
            authorization_file=authorization_file,
            batch_price_reader=batch_price_reader,
            submitter=submitter,
            still_maker=still_maker or live_still_maker,
            test_archive=test_archive,
            inventory_rows=rows,
        )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="HOS 010 Alvarez clay line twelve-plate Flow adapter (J2268)"
    )
    sub = parser.add_subparsers(dest="cmd", required=True)

    plan_p = sub.add_parser("plan", help="verify 12-row J2267 scope, VO, Option A1, and 3 batches; submit nothing")
    plan_p.add_argument("--repo")
    plan_p.add_argument("--out")

    dry_p = sub.add_parser("dry-run", help="verify scope, VO, Explorer ref, NAS mount and shared ledger; submit nothing")
    dry_p.add_argument("--repo")
    dry_p.add_argument("--media", default=str(DEFAULT_NAS_MEDIA))
    dry_p.add_argument(
        "--archive",
        default=str(DEFAULT_NAS_MEDIA / "04_Generated-Clips/archive_v01_twelve_plates"),
    )
    dry_p.add_argument("--other-reservations", type=int, default=0)
    dry_p.add_argument("--floor", type=int, default=HEADROOM_FLOOR)
    dry_p.add_argument("--require-staged", action="store_true")
    dry_p.add_argument("--authorization-file")
    dry_p.add_argument("--out")

    submit_p = sub.add_parser("submit", help=f"refused unless {SUBMIT_ENV}=1 AND {AUTH_JOB_ID} authorization is present")
    submit_p.add_argument("--repo")
    submit_p.add_argument("--media", required=False)
    submit_p.add_argument("--archive", required=False)
    submit_p.add_argument("--other-reservations", type=int, required=False)
    submit_p.add_argument("--floor", type=int, default=HEADROOM_FLOOR)
    submit_p.add_argument("--cap", type=int, default=MAX_TOTAL_CREDITS)
    submit_p.add_argument("--reservation", default=DEFAULT_RESERVATION)
    submit_p.add_argument("--authorization-file")
    submit_p.add_argument("--recorder", default="gemini")
    submit_p.add_argument("--ledger", required=False)
    submit_p.add_argument("--lock", required=False)
    submit_p.add_argument("--pid", required=False)
    submit_p.add_argument("--done", required=False)

    state = runner_state_dir()
    for name, help_text in (
        ("detach-command", "print a tmux launch command; start nothing"),
        ("launch-worker", "exclusive detached process owner"),
    ):
        launch = sub.add_parser(name, help=help_text)
        launch.add_argument("--repo", required=True)
        launch.add_argument("--media", required=True)
        launch.add_argument("--archive", required=True)
        launch.add_argument("--other-reservations", type=int, required=True)
        launch.add_argument("--authorization-file")
        launch.add_argument("--ledger", default=str(state / "ledger.jsonl"))
        launch.add_argument("--lock", default=str(state / "writer.lock"))
        launch.add_argument("--pid", default=str(state / "runner.pid"))
        launch.add_argument("--log", required=True)
        launch.add_argument("--done", required=True)

    refusal = sub.add_parser(
        "reconcile-policy-refusal",
        help="close a take Flow refused under its content policy at 0 credits; submits nothing",
    )
    refusal.add_argument("--key", required=True, help="shared charge id, e.g. HOS:010:P02:01_walter_hammer:t1")
    refusal.add_argument("--plate", required=True)
    refusal.add_argument("--part", type=int, required=True)
    refusal.add_argument("--take", type=int, default=1)
    refusal.add_argument("--reason", required=True)
    refusal.add_argument("--evidence", required=True, help="JSON file: the Chief ruling and the balance arithmetic")
    refusal.add_argument("--accounting-state", default=None)
    refusal.add_argument("--ledger", default=None)
    refusal.add_argument("--lock", default=None)

    args = parser.parse_args(argv)
    if args.cmd == "reconcile-policy-refusal":
        evidence = json.loads(Path(args.evidence).read_text())
        result = reconcile_policy_refusal(
            accounting_state=Path(args.accounting_state) if args.accounting_state else shared_flow_state_dir(),
            ledger_path=Path(args.ledger) if args.ledger else state / "ledger.jsonl",
            lock_path=Path(args.lock) if args.lock else state / "writer.lock",
            key=args.key,
            plate_id=args.plate,
            part=args.part,
            take=args.take,
            reason=args.reason,
            evidence=evidence,
        )
        sys.stdout.write(json.dumps(result, sort_keys=True) + "\n")
        return 0
    if args.cmd == "plan":
        repo = Path(args.repo) if args.repo else repo_root_from()
        cmd_plan(repo, Path(args.out) if args.out else None)
        return 0
    if args.cmd == "dry-run":
        repo = Path(args.repo) if args.repo else repo_root_from()
        cmd_dry_run(
            repo,
            media=Path(args.media),
            archive_dir=Path(args.archive),
            other=args.other_reservations,
            floor=args.floor,
            require_staged=bool(args.require_staged),
            authorization_file=Path(args.authorization_file) if args.authorization_file else None,
            out=Path(args.out) if args.out else None,
        )
        return 0
    if args.cmd in ("detach-command", "launch-worker"):
        auth_file = Path(args.authorization_file) if args.authorization_file else None
        command = detached_command(
            Path(__file__).resolve(),
            Path(args.log),
            Path(args.done),
            repo=Path(args.repo),
            media=Path(args.media),
            archive=Path(args.archive),
            other=args.other_reservations,
            ledger=Path(args.ledger),
            lock=Path(args.lock),
            pid=Path(args.pid),
            authorization_file=auth_file,
        )
        load_scope(Path(args.repo))
        if args.cmd == "detach-command":
            sys.stdout.write(json.dumps(command) + "\n")
            return 0
        if Path(args.pid).resolve() != (state / "runner.pid").resolve():
            raise GuardError("launch-worker requires the canonical runner pid path")
        child_args = shlex.split(command[-1])
        child_args[2] = "submit"
        log_index = child_args.index("--log")
        del child_args[log_index : log_index + 2]
        return launch_once(
            child_args,
            ownership=state / "runner.lock",
            pid=Path(args.pid),
            log=Path(args.log),
            done=Path(args.done),
        )
    if not submit_armed():
        raise SystemExit(
            "refusing submit: generation is not armed "
            f"({SUBMIT_ENV} is not 1). Plan / dry-run only until {AUTH_JOB_ID} / {PRODUCER_JOB_ID}."
        )
    repo = Path(args.repo) if args.repo else repo_root_from()
    require_generation_authorization(
        repo, Path(args.authorization_file) if args.authorization_file else None
    )
    if args.other_reservations is None or not args.media:
        raise GuardError("armed submit needs --other-reservations and --media")
    cmd_submit(
        repo,
        other=args.other_reservations,
        floor=args.floor,
        cap=args.cap,
        reservation=args.reservation,
        media=Path(args.media),
        ledger_path=Path(args.ledger) if args.ledger else state / "ledger.jsonl",
        lock_path=Path(args.lock) if args.lock else state / "writer.lock",
        pid_path=Path(args.pid) if args.pid else state / "runner.pid",
        done_path=Path(args.done) if args.done else state / "runner.done",
        archive_dir=Path(args.archive) if args.archive else None,
        authorization_file=Path(args.authorization_file) if args.authorization_file else None,
        recorder=args.recorder,
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except GuardError as exc:
        print(f"STOP {exc}", file=sys.stderr)
        raise SystemExit(2)
