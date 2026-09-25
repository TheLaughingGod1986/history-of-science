#!/usr/bin/env python3
"""Part 04 v19 — Flow auth unblock probe (googlemail Ultra, not 86).

STOP_TO_COS BLOCKED_AUTH if passkey wall / wrong account / no credits UI.
"""
from __future__ import annotations

import json
import re
import time
from datetime import datetime, timezone
from pathlib import Path

from playwright.sync_api import sync_playwright

PROJ = Path(__file__).resolve().parents[1]
QA = Path(__file__).resolve().parent / "_qa_part04_v19_auth"
PROFILE = Path.home() / ".playwright-hos-flow-profile"
REQUIRED = "benoats@googlemail.com"
FORBIDDEN = "benoats86@gmail.com"
URLS = [
    "https://labs.google/fx/tools/flow",
    "https://flow.google.com/",
    "https://flow.google.com/u/0/",
    "https://flow.google.com/u/1/",
]


def body_text(page) -> str:
    try:
        return page.inner_text("body")
    except Exception:
        return page.content()


def classify(text: str, url: str, title: str) -> dict:
    low = text.lower()
    passkey = any(
        x in low
        for x in (
            "passkey",
            "verifying it's you",
            "verifying it’s you",
            "complete sign-in using your passkey",
            "use your passkey",
            "confirm it's you",
            "confirm it’s you",
        )
    )
    credits = None
    for m in re.finditer(r"([\d,]{3,6})\s*credits", text, re.I):
        try:
            credits = int(m.group(1).replace(",", ""))
            break
        except ValueError:
            pass
    return {
        "url": url,
        "final_url": url,
        "title": title,
        "googlemail": REQUIRED in low or "googlemail.com" in low,
        "forbidden86": FORBIDDEN in low or "benoats86" in low,
        "passkey": passkey,
        "sign_in": "sign in" in low or "choose an account" in low,
        "credits": credits,
        "credits_hint": "credit" in low,
        "body_snip": "\n".join(text.splitlines()[:40])[:1200],
    }


def main() -> None:
    QA.mkdir(parents=True, exist_ok=True)
    results = []
    blocked = False
    ok = False
    with sync_playwright() as p:
        ctx = p.chromium.launch_persistent_context(
            user_data_dir=str(PROFILE),
            headless=False,
            viewport={"width": 1400, "height": 900},
            accept_downloads=True,
        )
        page = ctx.pages[0] if ctx.pages else ctx.new_page()
        for i, url in enumerate(URLS):
            try:
                page.goto(url, wait_until="domcontentloaded", timeout=120000)
            except Exception as e:
                results.append({"tried": url, "error": str(e)})
                continue
            time.sleep(4)
            try:
                page.get_by_role("button", name=re.compile(r"Agree|Accept|I agree", re.I)).first.click(
                    timeout=2500
                )
            except Exception:
                pass
            text = body_text(page)
            title = page.title()
            final = page.url
            shot = QA / f"retry_probe_{i}_{re.sub(r'[^a-zA-Z0-9]+', '_', final)[:60]}.png"
            page.screenshot(path=str(shot), full_page=False)
            row = classify(text, final, title)
            row["tried"] = url
            row["shot"] = str(shot.relative_to(PROJ.parent.parent)) if False else str(shot)
            # try open account / credits chip
            for sel in (
                "text=Credits",
                "[aria-label*='credit' i]",
                "text=/\\d[\\d,]*\\s*credits/i",
                "img[alt*='profile' i]",
                "button:has-text('@')",
            ):
                try:
                    page.locator(sel).first.click(timeout=1500)
                    time.sleep(1.5)
                    text2 = body_text(page)
                    row2 = classify(text2, page.url, page.title())
                    if row2.get("credits") and not row.get("credits"):
                        row["credits"] = row2["credits"]
                    if row2["passkey"]:
                        row["passkey"] = True
                    if row2["googlemail"]:
                        row["googlemail"] = True
                    if row2["forbidden86"]:
                        row["forbidden86"] = True
                    shot2 = QA / f"retry_probe_{i}_after_click.png"
                    page.screenshot(path=str(shot2), full_page=False)
                    row["after_click_shot"] = str(shot2)
                    break
                except Exception:
                    continue
            results.append(row)
            if row["passkey"] and row.get("googlemail"):
                blocked = True
                break
            if (
                not row["passkey"]
                and row.get("credits")
                and row["credits"] >= 1000
                and not row["forbidden86"]
            ):
                ok = True
                break
            if (
                not row["passkey"]
                and "flow.google.com" in row["final_url"]
                and "/about" not in row["final_url"]
                and not row["sign_in"]
            ):
                # likely session live; keep probing for credits
                pass
        # Final home shot
        try:
            page.goto("https://labs.google/fx/tools/flow", wait_until="domcontentloaded", timeout=90000)
            time.sleep(3)
            final_shot = QA / "retry_flow_home_final.png"
            page.screenshot(path=str(final_shot), full_page=False)
            text = body_text(page)
            final_row = classify(text, page.url, page.title())
            final_row["shot"] = str(final_shot)
            results.append({"final_home": final_row})
            if final_row["passkey"]:
                blocked = True
            if final_row.get("credits") and final_row["credits"] >= 1000 and not final_row["passkey"]:
                ok = True
        except Exception as e:
            results.append({"final_home_error": str(e)})
        ctx.close()

    out = {
        "when": datetime.now(timezone.utc).astimezone().isoformat(),
        "required_account": REQUIRED,
        "forbidden_account": FORBIDDEN,
        "ok": ok,
        "blocked_auth": blocked,
        "results": results,
    }
    (QA / "auth_probe_v19_retry.json").write_text(json.dumps(out, indent=2) + "\n")
    if blocked or (not ok and any(r.get("passkey") for r in results if isinstance(r, dict))):
        stop = {
            "status": "STOP_TO_COS_BLOCKED_AUTH",
            "when": out["when"],
            "detail": "Passkey / auth wall still present for googlemail — no paint, no mint.",
            "evidence": str(QA / "auth_probe_v19_retry.json"),
        }
        (QA / "STOP_TO_COS_BLOCKED_AUTH.json").write_text(json.dumps(stop, indent=2) + "\n")
        print(json.dumps(stop, indent=2))
        raise SystemExit(2)
    print(json.dumps(out, indent=2))
    if not ok:
        raise SystemExit(3)
    print("AUTH_OK")


if __name__ == "__main__":
    main()
