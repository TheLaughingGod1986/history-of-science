#!/usr/bin/env python3
"""Soft final verify after Ben 22:26 — no ABORT exits.

Confirm Content list A, Audience not-kids, Altered YES, T&C state.
Undo any unsaved staged T&C. Do NOT re-arm T&C (already retried once; trouble saving).
"""
from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path
import importlib.util

from playwright.sync_api import sync_playwright

PORT = 9460
CHANNEL = "UCXp7HkBIl1LgaznXuZHJyRg"
VID = "GHZDsiH7L7A"
PROJ = Path(__file__).resolve().parents[2]
EV = PROJ / "11_Upload-Package/Schedule/evidence_2026-09-29_studio"
ART = Path.home() / ".local/share/cursor-mac-mini-hos-worker/artifacts/hos004_thumb_A_2226"
BEN = Path.home() / ".local/share/cursor-mac-mini-hos-worker/artifacts"

_SPEC = importlib.util.spec_from_file_location(
    "cos2102", Path(__file__).resolve().parent / "_cos_checkin_2102_growth_fix_v01.py"
)
cos = importlib.util.module_from_spec(_SPEC)
assert _SPEC.loader
_SPEC.loader.exec_module(cos)


def log(m: str) -> None:
    EV.mkdir(parents=True, exist_ok=True)
    ART.mkdir(parents=True, exist_ok=True)
    line = f"{datetime.now().isoformat(timespec='seconds')} {m}"
    print(line, flush=True)
    with (EV / "soft_verify_2226.log").open("a") as f:
        f.write(line + "\n")


def dump(n, o):
    t = json.dumps(o, indent=2) + "\n"
    (EV / n).write_text(t)
    (ART / n).write_text(t)


def shot(page, n: str) -> Path:
    p = EV / n
    page.screenshot(path=str(p), full_page=False)
    (ART / n).write_bytes(p.read_bytes())
    (BEN / n).write_bytes(p.read_bytes())
    return p


def open_edit(page) -> None:
    page.goto(
        f"https://studio.youtube.com/video/{VID}/edit",
        wait_until="commit",
        timeout=90000,
    )
    page.wait_for_timeout(4000)
    cos.dismiss(page)


def scroll_to(page, pattern: str, max_pages: int = 35) -> bool:
    page.keyboard.press("Home")
    page.wait_for_timeout(200)
    for _ in range(max_pages):
        if re.search(pattern, page.inner_text("body"), re.I):
            return True
        page.keyboard.press("PageDown")
        page.wait_for_timeout(120)
    return bool(re.search(pattern, page.inner_text("body"), re.I))


def main():
    ART.mkdir(parents=True, exist_ok=True)
    EV.mkdir(parents=True, exist_ok=True)
    result = {
        "at": datetime.now().isoformat(timespec="seconds"),
        "order": "Ben 22:26 soft verify — thumb A primary done; T&C not re-looped",
        "videoId": VID,
    }
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{PORT}")
        ctx = browser.contexts[0]
        page = ctx.pages[0] if ctx.pages else ctx.new_page()
        cos.channel_ok(page)

        # Content list
        page.goto(
            f"https://studio.youtube.com/channel/{CHANNEL}/videos/upload",
            wait_until="commit",
            timeout=90000,
        )
        page.wait_for_timeout(3500)
        cos.dismiss(page)
        try:
            page.get_by_role("textbox", name=re.compile(r"Search", re.I)).first.fill(
                "What's Really Inside an Atom"
            )
            page.keyboard.press("Enter")
            page.wait_for_timeout(2500)
        except Exception:
            pass
        shot(page, "SOFT_2226_content.png")
        body = page.inner_text("body")
        result["content"] = {
            "has_title": "What's Really Inside an Atom" in body,
            "mentions_hidden_number": bool(re.search(r"HIDDEN NUMBER", body)),
            "ab_test_running_on_004": bool(
                re.search(
                    r"What.?s Really Inside an Atom[\s\S]{0,120}A/B test running",
                    body,
                    re.I,
                )
            ),
        }

        open_edit(page)
        # Undo unsaved staged test if any
        try:
            page.get_by_role("button", name=re.compile(r"^Undo changes$", re.I)).first.click(
                timeout=1000
            )
            page.wait_for_timeout(800)
            result["undid_unsaved"] = True
        except Exception:
            result["undid_unsaved"] = False

        body = page.inner_text("body")
        if re.search(r"A/B testing titles|title test has been set up", body, re.I):
            result["staged_titles"] = True
            try:
                page.get_by_role("button", name=re.compile(r"^A/B Testing$", re.I)).first.click(
                    timeout=2000
                )
                page.wait_for_timeout(1000)
                body2 = page.inner_text("body")
                if re.search(r"current test will be deleted|Run a new test", body2, re.I):
                    page.get_by_role("button", name=re.compile(r"^Continue$", re.I)).first.click(
                        timeout=1500
                    )
                    page.wait_for_timeout(1500)
                    for pat in (r"^Cancel$", r"^Close$"):
                        try:
                            page.get_by_role("button", name=re.compile(pat, re.I)).first.click(
                                timeout=1000
                            )
                            break
                        except Exception:
                            pass
                    page.keyboard.press("Escape")
                    result["cleared_staged"] = True
                else:
                    page.keyboard.press("Escape")
            except Exception as e:
                result["clear_err"] = type(e).__name__
            open_edit(page)
        else:
            result["staged_titles"] = False

        shot(page, "SOFT_2226_edit.png")
        result["tc"] = cos.read_tc_state(page)

        scroll_to(page, r"Made for Kids|Audience")
        page.wait_for_timeout(400)
        result["audience"] = cos.read_audience(page)
        shot(page, "SOFT_2226_audience.png")

        cos.show_more(page)
        scroll_to(page, r"AI wasn|AI was used|Altered content|AI use")
        page.wait_for_timeout(400)
        result["altered"] = cos.read_ai_altered(page)
        shot(page, "SOFT_2226_altered.png")

        # Visibility snip
        scroll_to(page, r"Visibility|Scheduled|Premiere")
        body = page.inner_text("body")
        result["visibility_snip"] = {
            "scheduled": bool(re.search(r"Scheduled|15 Oct|Oct 15", body, re.I)),
            "premiere_off_guess": not bool(re.search(r"Premiere\s*on|Set as Premiere.*checked", body, re.I)),
        }
        shot(page, "SOFT_2226_final.png")

        result["summary"] = {
            "main_thumb_content_ok": result["content"].get("has_title")
            and not result["content"].get("mentions_hidden_number"),
            "audience_not_kids": result["audience"].get("ok_not_kids"),
            "altered_yes": result["altered"].get("yes") is True,
            "tc_two_slot": result["tc"].get("two_slot_title_test"),
            "tc_ineligible": result["tc"].get("ineligible"),
            "titles": result["tc"].get("titles_present"),
            "staged_cleared": result.get("cleared_staged") or not result.get("staged_titles"),
            "tc_rearm": "blocked_studio_trouble_saving_after_one_retry — re-arm after 15 Oct public (3 pairs or Thumbnail-only)",
        }
        dump("SOFT_2226_RESULT.json", result)
        log(f"SUMMARY {result['summary']}")
        return result


if __name__ == "__main__":
    main()
