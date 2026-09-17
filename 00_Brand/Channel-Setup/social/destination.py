"""HOS social destinations — never Orbit, never Wellesley.

Live HOS handles:
  Instagram / Threads  @historyofscienceyt
  Facebook Page        61593586420124
  YouTube              @HistoryOfScienceYT

Forbidden:
  Orbit IG/Threads @orbitwithben
  Wellesley IG/Threads @historyofscience
  Orbit Facebook Page 61592833318203
  TikTok (paused)
"""
from __future__ import annotations

HOS_IG_HANDLE = "historyofscienceyt"
HOS_THREADS_HANDLE = "historyofscienceyt"
HOS_FACEBOOK_PAGE_ID = "61593586420124"
HOS_YOUTUBE_HANDLE = "@HistoryOfScienceYT"

ORBIT_FACEBOOK_PAGE_ID = "61592833318203"
ORBIT_SUITE_ASSET_ID = "1285932871266399"
ORBIT_BUSINESS_ID = "1352434763139246"

FORBIDDEN_HANDLES = frozenset(
    {
        "orbitwithben",
        "orbit.with.ben",
        "historyofscience",  # Wellesley Science Center
    }
)
FORBIDDEN_FACEBOOK_PAGE_IDS = frozenset({ORBIT_FACEBOOK_PAGE_ID})
FORBIDDEN_SUITE_ASSET_IDS = frozenset({ORBIT_SUITE_ASSET_ID})


def _norm_handle(value: object) -> str:
    return str(value or "").strip().lstrip("@").lower()


def refuse_meta_publish(creds: dict | None) -> dict:
    """Abort Meta Reels if creds would post to Orbit / Wellesley."""
    creds = creds or {}
    page_id = str(creds.get("page_id") or "").strip()
    asset = str(creds.get("business_suite_asset_id") or "").strip()
    ig = _norm_handle(creds.get("instagram_username"))
    reasons: list[str] = []
    if page_id in FORBIDDEN_FACEBOOK_PAGE_IDS:
        reasons.append(f"facebook page_id is Orbit ({ORBIT_FACEBOOK_PAGE_ID})")
    if asset in FORBIDDEN_SUITE_ASSET_IDS:
        reasons.append(f"business_suite_asset_id is Orbit ({ORBIT_SUITE_ASSET_ID})")
    if ig in FORBIDDEN_HANDLES:
        reasons.append(f"instagram_username is forbidden ({ig})")
    if ig and ig != HOS_IG_HANDLE:
        reasons.append(f"instagram_username must be {HOS_IG_HANDLE}, got {ig}")
    if page_id and page_id != HOS_FACEBOOK_PAGE_ID:
        reasons.append(
            f"facebook page_id must be HOS {HOS_FACEBOOK_PAGE_ID}, got {page_id}"
        )
    if not str(creds.get("business_suite_asset_id") or "").strip():
        reasons.append(
            "HOS Facebook has no Business Suite asset yet — do not open the Orbit composer"
        )
    if reasons:
        return {
            "ok": False,
            "error": "refusing_non_hos_destination: " + "; ".join(reasons),
            "reasons": reasons,
        }
    return {"ok": True, "error": "", "reasons": []}


def refuse_threads_publish(*, username: str, page_url: str = "", body_text: str = "") -> dict:
    """Abort Threads if the logged-in session is not @historyofscienceyt."""
    handle = _norm_handle(username) or HOS_THREADS_HANDLE
    blob = f"{page_url} {body_text}".lower()
    reasons: list[str] = []
    if handle in FORBIDDEN_HANDLES:
        reasons.append(f"threads username is forbidden ({handle})")
    if handle != HOS_THREADS_HANDLE:
        reasons.append(f"threads username must be {HOS_THREADS_HANDLE}, got {handle}")
    if "orbitwithben" in blob and "edit profile" in blob:
        reasons.append("logged-in Threads profile is @orbitwithben")
    if reasons:
        return {
            "ok": False,
            "error": "refusing_non_hos_threads: " + "; ".join(reasons),
            "reasons": reasons,
        }
    return {"ok": True, "error": "", "reasons": []}
