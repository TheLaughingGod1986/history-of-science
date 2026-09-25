#!/usr/bin/env python3
"""HOS Germs Shorts — classic TYPE remint (mint NEW ids), then Private old ids.

Ben unlocked classic remint for TYPE PASS. YouTube cannot replace the file on the same id.

Channel: @HistoryOfScienceYT only (UCXp7HkBIl1LgaznXuZHJyRg). Never Orbit. Zero /go/.
Related on every new Short: _C92tIJCk8A
Do not touch HOS 002 remint bc-7f53df3e.

Usage (Google session must already be signed into HOS Studio on the CDP Chrome):
  /tmp/hos-studio-pw-venv/bin/python \\
    02_Video-Projects/001_How-Did-We-Discover-Germs/11_Upload-Package/Schedule/_remint_germs_shorts_type_classic_v01.py \\
    --cdp http://127.0.0.1:9460
"""
from __future__ import annotations

import argparse
import json
import re
from datetime import datetime
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(
    "/Users/benjaminoats/YouTube/History Of Science/02_Video-Projects/"
    "001_How-Did-We-Discover-Germs"
)
EV = ROOT / "11_Upload-Package/Schedule/evidence_2026-09-05_type_classic_remint"
JOBS_PATH = EV / "REMINT_JOBS.json"
HOS = "UCXp7HkBIl1LgaznXuZHJyRg"
LONG = "_C92tIJCk8A"
HANDLE = "@HistoryOfScienceYT"


def snip(page, n: int = 2500) -> str:
    try:
        return page.inner_text("body")[:n]
    except Exception as e:
        return f"<snip err {e}>"


def dismiss(page) -> None:
    for name in ["Got it", "Dismiss", "Not now", "Close", "No thanks", "Skip", "Done"]:
        try:
            b = page.get_by_role("button", name=re.compile(rf"^{name}$", re.I))
            if b.count() and b.first.is_visible():
                b.first.click(timeout=700, force=True)
        except Exception:
            pass


def is_glue(page) -> bool:
    t = page.title() + "\n" + snip(page, 1200)
    return bool(
        re.search(
            r"Error\s*9|something went wrong|don.?t have permission|"
            r"phone.?verif|confirm you.?re not a bot|unusual traffic",
            t,
            re.I,
        )
    )


def ensure_hos(page) -> dict:
    page.goto(
        f"https://studio.youtube.com/channel/{HOS}",
        wait_until="domcontentloaded",
        timeout=120000,
    )
    page.wait_for_timeout(4500)
    dismiss(page)
    body = snip(page, 2000)
    if re.search(r"signin|accountchooser|Signed out", page.url + "\n" + body, re.I):
        return {"ok": False, "reason": "SIGNED_OUT", "url": page.url, "snip": body[:500]}
    if re.search(r"\bOrbit\b|\bOppti\b", body, re.I) and "History of Science" not in body:
        return {"ok": False, "reason": "WRONG_CHANNEL", "url": page.url, "snip": body[:500]}
    ok = ("History of Science" in body) or (HOS in page.url)
    return {"ok": ok, "url": page.url, "title": page.title(), "snip": body[:500]}


def extract_new_id(page) -> str | None:
    m = re.search(r"/video/([A-Za-z0-9_-]{6,})/", page.url)
    if m:
        return m.group(1)
    body = snip(page, 8000)
    for pat in (
        r"https://youtu\.be/([A-Za-z0-9_-]{6,})",
        r"youtube\.com/shorts/([A-Za-z0-9_-]{6,})",
        r"watch\?v=([A-Za-z0-9_-]{6,})",
    ):
        m = re.search(pat, body)
        if m and m.group(1) != LONG:
            return m.group(1)
    return None


def next_until_visibility(page) -> None:
    for _ in range(16):
        dismiss(page)
        text = snip(page, 2500)
        try:
            dlg = page.locator("ytcp-uploads-dialog")
            if dlg.count():
                text = dlg.inner_text()
        except Exception:
            pass
        if re.search(r"Visibility|Save or publish|Schedule", text, re.I) and re.search(
            r"Private|Public|Unlisted", text, re.I
        ):
            return
        nxt = page.get_by_role("button", name=re.compile(r"^Next$", re.I))
        if nxt.count() and nxt.first.is_enabled():
            nxt.first.click(force=True)
            page.wait_for_timeout(1400)
        else:
            break


def set_visibility(page, job: dict) -> str:
    if job.get("visibilityPlan") == "schedule" and job.get("publishAt"):
        try:
            page.get_by_text(re.compile(r"^Schedule$", re.I)).first.click(timeout=4000)
            page.wait_for_timeout(800)
            return "schedule_attempted"
        except Exception as e:
            return f"schedule_err:{e}"
    try:
        page.evaluate(
            """() => {
              const walk=(r,d=0)=>{
                if(!r||d>25) return false;
                const nodes=[...(r.querySelectorAll
                  ? r.querySelectorAll('[role=radio],tp-yt-paper-radio-button,ytcp-radio')
                  : [])];
                for (const el of nodes) {
                  const t=((el.innerText||'')+' '+(el.getAttribute('aria-label')||'')).toLowerCase();
                  if (t.includes('public') && !t.includes('scheduled')) { el.click(); return true; }
                }
                for (const el of (r.querySelectorAll ? r.querySelectorAll('*') : [])) {
                  if (el.shadowRoot && walk(el.shadowRoot, d+1)) return true;
                }
                return false;
              };
              return walk(document.querySelector('ytcp-uploads-dialog') || document);
            }"""
        )
        return "public_clicked"
    except Exception as e:
        return f"public_err:{e}"


def set_related(page, new_id: str) -> str:
    page.goto(
        f"https://studio.youtube.com/video/{new_id}/edit",
        wait_until="domcontentloaded",
        timeout=120000,
    )
    page.wait_for_timeout(4000)
    dismiss(page)
    body = snip(page, 5000)
    if LONG in body or "How Did We Discover Germs" in body:
        return "already_set"
    try:
        for _ in range(10):
            page.mouse.wheel(0, 1200)
            page.wait_for_timeout(250)
        add = page.get_by_text(
            re.compile(r"Add (a )?related video|Select video|Add video", re.I)
        )
        if add.count():
            add.first.click(timeout=4000)
        else:
            page.get_by_text(re.compile(r"Related video", re.I)).first.click(timeout=4000)
        page.wait_for_timeout(1000)
        box = page.locator(
            "tp-yt-paper-input input, input[type='text'], input[aria-label*='Search' i]"
        ).first
        box.click(timeout=4000)
        box.fill(LONG)
        page.wait_for_timeout(2000)
        hit = page.get_by_text(
            re.compile(r"How Did We Discover Germs|" + re.escape(LONG), re.I)
        )
        if hit.count():
            hit.first.click(timeout=5000)
            page.wait_for_timeout(800)
        save = page.get_by_role("button", name=re.compile(r"^Save$", re.I))
        if save.count() and save.first.is_enabled():
            save.first.click(timeout=4000)
            page.wait_for_timeout(2500)
            return "set_saved"
        return "picked_save_grey"
    except Exception as e:
        return f"err:{type(e).__name__}:{e}"


def private_old(page, old_id: str) -> str:
    page.goto(
        f"https://studio.youtube.com/video/{old_id}/edit",
        wait_until="domcontentloaded",
        timeout=120000,
    )
    page.wait_for_timeout(3500)
    dismiss(page)
    if is_glue(page):
        return "glue"
    try:
        vis = page.get_by_text(re.compile(r"^Visibility$", re.I))
        if vis.count():
            vis.first.click(timeout=3000)
            page.wait_for_timeout(800)
        page.get_by_text(re.compile(r"^Private$", re.I)).first.click(timeout=4000)
        page.wait_for_timeout(600)
        save = page.get_by_role("button", name=re.compile(r"^Save$", re.I))
        if save.count() and save.first.is_enabled():
            save.first.click(timeout=4000)
            page.wait_for_timeout(2500)
            return "privated"
        return "private_selected_save_grey"
    except Exception as e:
        return f"err:{type(e).__name__}:{e}"


def upload_one(page, job: dict) -> dict:
    path = Path(job["file"])
    page.goto(
        f"https://studio.youtube.com/channel/{HOS}/videos/upload?d=ud",
        wait_until="domcontentloaded",
        timeout=120000,
    )
    page.wait_for_timeout(2500)
    dismiss(page)
    if is_glue(page):
        job["ok"] = False
        job["glue"] = True
        return job

    inputs = page.locator('input[type="file"]')
    if inputs.count():
        inputs.first.set_input_files(str(path))
    else:
        with page.expect_file_chooser(timeout=20000) as fc:
            page.get_by_role("button", name=re.compile(r"Select files", re.I)).click(
                force=True
            )
        fc.value.set_files(str(path))

    title_box = page.get_by_role("textbox", name=re.compile(r"title|describe", re.I)).first
    title_box.wait_for(timeout=180000)
    try:
        title_box.fill(job["title"])
    except Exception:
        title_box.click()
        page.keyboard.press("Meta+A")
        page.keyboard.type(job["title"])

    try:
        desc = page.get_by_role(
            "textbox", name=re.compile(r"tell viewers|description", re.I)
        ).first
        desc.click(force=True)
        desc.fill(job["description"])
    except Exception:
        pass

    try:
        page.get_by_text(re.compile(r"No, it.?s not.?Made for Kids", re.I)).click(
            force=True
        )
    except Exception:
        pass

    try:
        up = page.get_by_text(
            re.compile(r"Upload file|Upload thumbnail|Custom thumbnail", re.I)
        )
        if up.count() and job.get("cover"):
            with page.expect_file_chooser(timeout=5000) as fc:
                up.first.click(force=True)
            fc.value.set_files(job["cover"])
            job["thumbAttempt"] = "chooser"
    except Exception as e:
        job["thumbAttempt"] = f"skip:{type(e).__name__}"

    next_until_visibility(page)
    job["visibilityResult"] = set_visibility(page, job)

    for name in ["Publish", "Schedule", "Save"]:
        btn = page.get_by_role("button", name=re.compile(rf"^{name}$", re.I))
        if btn.count() and btn.first.is_enabled():
            btn.first.click(force=True)
            page.wait_for_timeout(5000)
            break

    dismiss(page)
    page.wait_for_timeout(2000)
    new_id = extract_new_id(page)
    if not new_id:
        try:
            link = page.locator(
                "a[href*='/video/'], a[href*='youtu.be/'], a[href*='shorts/']"
            ).first
            href = link.get_attribute("href") or ""
            m = re.search(r"([A-Za-z0-9_-]{11})", href)
            if m:
                new_id = m.group(1)
        except Exception:
            pass

    job["newId"] = new_id
    job["uploaded"] = bool(new_id)
    job["uploadUrl"] = page.url
    job["ok"] = bool(new_id)
    if new_id:
        job["relatedStatus"] = set_related(page, new_id)
        job["relatedSet"] = job["relatedStatus"] in (
            "already_set",
            "set_saved",
            "picked_save_grey",
        )
    return job


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--cdp", default="http://127.0.0.1:9460")
    ap.add_argument("--only")
    args = ap.parse_args()
    EV.mkdir(parents=True, exist_ok=True)
    jobs = json.loads(JOBS_PATH.read_text())
    if args.only:
        jobs = [j for j in jobs if j["slot"] == args.only]

    result = {
        "started": datetime.now().isoformat(timespec="seconds"),
        "channel": HANDLE,
        "channelId": HOS,
        "long": LONG,
        "items": [],
        "stopped": None,
    }

    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(args.cdp)
        ctx = browser.contexts[0]
        page = ctx.pages[0] if ctx.pages else ctx.new_page()
        hos = ensure_hos(page)
        result["hos"] = hos
        page.screenshot(path=str(EV / "00_hos_boot.png"), full_page=True)
        if not hos.get("ok"):
            result["stopped"] = hos.get("reason") or "HOS_NOT_READY"
            (EV / "RESULT_PARTIAL.json").write_text(json.dumps(result, indent=2))
            print(json.dumps(result, indent=2)[:2500])
            return 2

        for job in jobs:
            print(f"==== upload {job['slot']} {job['oldId']} ====")
            if is_glue(page):
                result["stopped"] = "GLUE_BEFORE_UPLOAD"
                break
            try:
                item = upload_one(page, dict(job))
            except Exception as e:
                item = dict(job)
                item["ok"] = False
                item["error"] = f"{type(e).__name__}:{e}"
                result["items"].append(item)
                result["stopped"] = "UPLOAD_EXCEPTION"
                break
            page.screenshot(
                path=str(EV / f"{job['slot']}_after_upload.png"), full_page=True
            )
            if item.get("glue"):
                result["items"].append(item)
                result["stopped"] = "GLUE_DURING_UPLOAD"
                break
            if not item.get("newId"):
                result["items"].append(item)
                result["stopped"] = "NO_NEW_ID"
                break
            item["oldPrivateStatus"] = private_old(page, job["oldId"])
            item["oldPrivated"] = item["oldPrivateStatus"] in (
                "privated",
                "private_selected_save_grey",
            )
            result["items"].append(item)
            (EV / "RESULT_PARTIAL.json").write_text(json.dumps(result, indent=2))

    result["finished"] = datetime.now().isoformat(timespec="seconds")
    (EV / "RESULT_FINAL.json").write_text(json.dumps(result, indent=2))
    lines = [
        "| old id | new id | Related | Private old |",
        "|---|---|---|---|",
    ]
    for it in result["items"]:
        related = LONG if it.get("relatedSet") else it.get("relatedStatus")
        lines.append(
            f"| {it.get('oldId')} | {it.get('newId')} | {related} | {it.get('oldPrivated')} |"
        )
    (EV / "REPORT_TABLE.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))
    print("stopped=", result.get("stopped"))
    return 0 if not result.get("stopped") else 1


if __name__ == "__main__":
    raise SystemExit(main())
