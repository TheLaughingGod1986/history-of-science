#!/usr/bin/env python3
"""FORCE-upload house yellow/gold custom thumbs on 5 Public Germs Shorts.

Studio ONLY. No remint. No drafts. @HistoryOfScienceYT CDP :9460.
"""
from __future__ import annotations

import hashlib
import json
import re
import time
import traceback
from datetime import datetime, timezone
from pathlib import Path

from playwright.sync_api import sync_playwright

EV = Path(
    "/Users/benjaminoats/YouTube/History Of Science/02_Video-Projects/"
    "001_How-Did-We-Discover-Germs/11_Upload-Package/Schedule/"
    "evidence_2026-09-06_shorts_thumb_house"
)
THUMBS = Path(
    "/Users/benjaminoats/YouTube/History Of Science/02_Video-Projects/"
    "001_How-Did-We-Discover-Germs/08_Thumbnail/Shorts"
)
ART = Path.home() / ".local/share/cursor-mac-mini-hos-worker/artifacts"
CDP = "http://127.0.0.1:9460"
CHANNEL = "UCXp7HkBIl1LgaznXuZHJyRg"
HANDLE = "@HistoryOfScienceYT"

JOBS = [
    {
        "slot": "s01",
        "id": "H1y0DXFVmw8",
        "title": "Germs don't cast a shadow",
        "file": "hos_001_s01_shadow_cover_animistry_v02.jpg",
        "png": "hos_001_s01_shadow_cover_animistry_v02.png",
    },
    {
        "slot": "s02",
        "id": "iqToagXnjX0",
        "title": "Microbes in a drop of pond water",
        "file": "hos_001_s02_pond_cover_animistry_v03.jpg",
        "png": "hos_001_s02_pond_cover_animistry_v03.png",
    },
    {
        "slot": "s03",
        "id": "8_Edn_HCi1s",
        "title": "Germs hitch a ride on you",
        "file": "hos_001_s03_vector_cover_animistry_v02.jpg",
        "png": "hos_001_s03_vector_cover_animistry_v02.png",
    },
    {
        "slot": "s04",
        "id": "sILtQxgYQk8",
        "title": "A flask that proved germs come from outside",
        "file": "hos_001_s04_flask_cover_animistry_v03.jpg",
        "png": "hos_001_s04_flask_cover_animistry_v03.png",
    },
    {
        "slot": "s05",
        "id": "93fPUG-hW0A",
        "title": "Invisible life is still everywhere",
        "file": "hos_001_s05_soap_cover_animistry_v02.jpg",
        "png": "hos_001_s05_soap_cover_animistry_v02.png",
    },
]


def sha256(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def log(msg: str) -> None:
    EV.mkdir(parents=True, exist_ok=True)
    line = f"{datetime.now().isoformat(timespec='seconds')} {msg}"
    print(line, flush=True)
    with (EV / "run.log").open("a") as f:
        f.write(line + "\n")


def shot(page, name: str) -> str:
    EV.mkdir(parents=True, exist_ok=True)
    ART.mkdir(parents=True, exist_ok=True)
    dest = EV / name
    try:
        page.screenshot(path=str(dest), full_page=True)
        try:
            (ART / name).write_bytes(dest.read_bytes())
        except Exception:
            pass
        return str(dest)
    except Exception as e:
        log(f"shot_err {name}: {e}")
        return ""


def body(page, n: int = 6000) -> str:
    try:
        return page.inner_text("body")[:n]
    except Exception as e:
        return str(e)


def wait_studio(page, timeout_s: int = 60) -> bool:
    page.wait_for_load_state("domcontentloaded")
    for _ in range(timeout_s):
        t = body(page, 1500)
        if "Choose an account" in t or "Signed out" in t:
            return False
        if page.locator(
            "ytcp-navigation-drawer, ytcp-app, ytcp-video-metadata-editor"
        ).count():
            return True
        time.sleep(0.5)
    return False


def dismiss(page) -> None:
    for name in ["Close", "Got it", "Not now", "Dismiss", "No thanks"]:
        try:
            btn = page.get_by_role("button", name=re.compile(rf"^{name}$", re.I))
            if btn.count() and btn.first.is_visible():
                btn.first.click(force=True, timeout=800)
                page.wait_for_timeout(150)
        except Exception:
            pass
    try:
        page.keyboard.press("Escape")
    except Exception:
        pass


def ensure_hos(page) -> dict:
    page.goto(
        f"https://studio.youtube.com/channel/{CHANNEL}",
        wait_until="domcontentloaded",
        timeout=120000,
    )
    ok = wait_studio(page)
    dismiss(page)
    t = body(page, 2500)
    return {
        "ok": ok and ("History of Science" in t or HANDLE.lower() in t.lower()),
        "url": page.url,
        "snippet": t[:400],
    }


def click_save(page) -> str:
    for name in ["Save", "PUBLISH", "Publish"]:
        btn = page.get_by_role("button", name=re.compile(rf"^{name}$", re.I))
        if btn.count():
            try:
                if btn.first.is_enabled():
                    btn.first.click(force=True, timeout=4000)
                    page.wait_for_timeout(2500)
                    return f"clicked_{name}"
            except Exception as e:
                return f"click_err_{name}:{e}"
    ok = page.evaluate(
        """()=>{
      const walk=(r,d=0)=>{
        if(!r||d>50) return false;
        for(const el of (r.querySelectorAll?r.querySelectorAll('button,ytcp-button,[role=button]'):[])){
          const tx=(el.innerText||'').trim();
          if(/^Save$/i.test(tx) && !el.disabled){ el.click(); return true; }
        }
        for(const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
          if(el.shadowRoot && walk(el.shadowRoot,d+1)) return true;
        return false;
      };
      return walk(document);
    }"""
    )
    if ok:
        page.wait_for_timeout(2500)
        return "js_Save"
    return "save_not_found_or_grey"


def find_thumb_file_inputs(page):
    return page.evaluate(
        """()=>{
      const out=[];
      const walk=(r,d=0,path='')=>{
        if(!r||d>55) return;
        const nodes=r.querySelectorAll?r.querySelectorAll('input[type=file]'):[];
        for(const el of nodes){
          out.push({
            acc: el.accept||'',
            id: el.id||'',
            name: el.name||'',
            aria: el.getAttribute('aria-label')||'',
            near: (el.closest && (el.closest('ytcp-thumbnails,ytcp-video-thumbnail-editor,ytcp-thumbnail-uploader,ytcp-video-metadata-editor-basics')||{}).tagName)||'',
            path
          });
        }
        for(const el of (r.querySelectorAll?r.querySelectorAll('*'):[])){
          if(el.shadowRoot) walk(el.shadowRoot,d+1,path+'/'+(el.tagName||''));
        }
      };
      walk(document);
      return out;
    }"""
    )


def upload_thumb(page, path: Path) -> dict:
    notes = []
    try:
        page.get_by_text(
            re.compile(r"Thumbnail|Upload file|Custom thumbnail", re.I)
        ).first.scroll_into_view_if_needed(timeout=5000)
        page.wait_for_timeout(400)
    except Exception as e:
        notes.append(f"scroll:{e}")

    inputs_info = find_thumb_file_inputs(page)
    notes.append(f"file_inputs={len(inputs_info)}")
    notes.append({"inputs": inputs_info[:8]})

    loc = page.locator('input[type="file"]')
    n = loc.count()
    notes.append(f"light_inputs={n}")
    for i in range(n):
        try:
            acc = (loc.nth(i).get_attribute("accept") or "").lower()
            if (
                "image" in acc
                or "jpeg" in acc
                or "png" in acc
                or acc == ""
                or "*/*" in acc
            ):
                loc.nth(i).set_input_files(str(path))
                notes.append(f"set_input_files_i={i}_acc={acc}")
                page.wait_for_timeout(2500)
                return {"ok": True, "method": f"set_input_files:{i}", "notes": notes}
        except Exception as e:
            notes.append(f"set_err_{i}:{type(e).__name__}:{e}")

    for pat in [
        r"^Upload file$",
        r"Upload thumbnail",
        r"Custom thumbnail",
        r"Upload$",
        r"Change$",
        r"Replace$",
    ]:
        try:
            el = page.get_by_text(re.compile(pat, re.I))
            if not el.count():
                continue
            with page.expect_file_chooser(timeout=8000) as fc:
                el.first.click(force=True, timeout=4000)
            fc.value.set_files(str(path))
            notes.append(f"chooser={pat}")
            page.wait_for_timeout(2500)
            return {"ok": True, "method": f"chooser:{pat}", "notes": notes}
        except Exception as e:
            notes.append(f"chooser_err_{pat}:{type(e).__name__}")

    try:
        clicked = page.evaluate(
            """()=>{
          const walk=(r,d=0)=>{
            if(!r||d>55) return null;
            for(const el of (r.querySelectorAll?r.querySelectorAll('button,ytcp-button,[role=button],div,span,a'):[])){
              const t=(el.innerText||'').replace(/\\s+/g,' ').trim();
              if(/^(Upload file|Upload thumbnail|Custom thumbnail|Change|Replace)$/i.test(t)){
                el.click(); return t;
              }
            }
            for(const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
              if(el.shadowRoot){ const x=walk(el.shadowRoot,d+1); if(x) return x; }
            return null;
          };
          return walk(document);
        }"""
        )
        notes.append(f"js_click={clicked}")
        if clicked:
            with page.expect_file_chooser(timeout=8000) as fc:
                page.wait_for_timeout(200)
            fc.value.set_files(str(path))
            notes.append("js_chooser_ok")
            page.wait_for_timeout(2500)
            return {"ok": True, "method": f"js:{clicked}", "notes": notes}
    except Exception as e:
        notes.append(f"js_err:{type(e).__name__}:{e}")

    return {"ok": False, "method": None, "notes": notes}


def process_one(page, job: dict) -> dict:
    jpg = THUMBS / job["file"]
    png = THUMBS / job["png"]
    path = jpg if jpg.exists() else png
    if not path.exists():
        return {"id": job["id"], "slot": job["slot"], "status": "failed", "error": "file_missing"}

    item = {
        "slot": job["slot"],
        "id": job["id"],
        "title": job["title"],
        "path": str(path),
        "sha256": sha256(path),
        "bytes": path.stat().st_size,
        "status": "failed",
    }

    url = f"https://studio.youtube.com/video/{job['id']}/edit"
    log(f"==== {job['slot']} {job['id']} ====")
    page.goto(url, wait_until="domcontentloaded", timeout=120000)
    if not wait_studio(page):
        item["error"] = "studio_not_ready"
        shot(page, f"{job['slot']}_{job['id']}_blocked.png")
        return item
    dismiss(page)
    page.wait_for_timeout(1200)

    item["before"] = shot(page, f"{job['slot']}_{job['id']}_before.png")
    item["before_snippet"] = body(page, 800)

    t0 = body(page, 3000)
    if re.search(r"verify it.?s you|Confirm it.?s you|phone number", t0, re.I):
        item["status"] = "blocked"
        item["error"] = "verify_wall"
        return item

    up = upload_thumb(page, path)
    item["upload"] = up
    item["after_upload"] = shot(page, f"{job['slot']}_{job['id']}_after_upload.png")

    if not up.get("ok"):
        item["error"] = "upload_failed"
        return item

    save = click_save(page)
    item["save"] = save
    page.wait_for_timeout(2000)
    dismiss(page)
    item["after_save"] = shot(page, f"{job['slot']}_{job['id']}_after_save.png")
    item["after_snippet"] = body(page, 800)

    t1 = body(page, 2500)
    if re.search(r"error|couldn.?t upload|failed to upload|too large|invalid", t1, re.I):
        item["status"] = "failed"
        item["error"] = "upload_error_in_ui"
    else:
        item["status"] = "updated"
    return item


def dashboard_proof(page) -> str:
    page.goto(
        f"https://studio.youtube.com/channel/{CHANNEL}/videos/short",
        wait_until="domcontentloaded",
        timeout=120000,
    )
    wait_studio(page)
    page.wait_for_timeout(2500)
    dismiss(page)
    return shot(page, "99_content_shorts_after.png")


def main() -> int:
    EV.mkdir(parents=True, exist_ok=True)
    ART.mkdir(parents=True, exist_ok=True)
    result = {
        "started": datetime.now(timezone.utc).isoformat(),
        "channel": HANDLE,
        "channelId": CHANNEL,
        "cdp": CDP,
        "lock": "FORCE yellow/gold 3D house thumbs — no match/leave-as-is",
        "items": [],
        "ok": False,
    }

    with sync_playwright() as pw:
        browser = pw.chromium.connect_over_cdp(CDP, timeout=60000)
        ctx = browser.contexts[0]
        page = next(
            (p for p in ctx.pages if "studio.youtube.com" in (p.url or "")),
            None,
        )
        if page is None:
            page = ctx.new_page()

        hos = ensure_hos(page)
        result["hos"] = hos
        shot(page, "00_hos_boot.png")
        if not hos.get("ok"):
            log(f"HOS check weak: {hos}")
            if "studio.youtube.com" not in page.url:
                result["stopped"] = "HOS_NOT_READY"
                (EV / "RESULT.json").write_text(json.dumps(result, indent=2))
                return 2

        for job in JOBS:
            try:
                item = process_one(page, job)
            except Exception as e:
                item = {
                    "slot": job["slot"],
                    "id": job["id"],
                    "status": "failed",
                    "error": f"{type(e).__name__}:{e}",
                    "trace": traceback.format_exc()[-1500:],
                }
                shot(page, f"{job['slot']}_{job['id']}_exception.png")
            result["items"].append(item)
            (EV / "RESULT_PARTIAL.json").write_text(json.dumps(result, indent=2))
            log(f"DONE {job['slot']} {item.get('status')} {item.get('error', '')}")

        try:
            result["dashboard"] = dashboard_proof(page)
        except Exception as e:
            result["dashboard_err"] = str(e)

    updated = sum(1 for i in result["items"] if i.get("status") == "updated")
    failed = sum(1 for i in result["items"] if i.get("status") != "updated")
    result["summary"] = {
        "updated": updated,
        "failed": failed,
        "total": len(result["items"]),
    }
    result["ok"] = failed == 0 and updated == 5
    result["finished"] = datetime.now(timezone.utc).isoformat()
    (EV / "RESULT.json").write_text(json.dumps(result, indent=2))
    print(json.dumps(result, indent=2)[:5000])
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
