#!/usr/bin/env python3
"""HARD DELETE leftovers on @HistoryOfScienceYT ONLY.

Channel: UCXp7HkBIl1LgaznXuZHJyRg — never Orbit.
Allowlist NEVER deleted. Everything else (twins / drafts / private junk) goes.
If Studio signed out → write BLOCKED_AUTH and stop (never paste passwords).
"""
from __future__ import annotations

import json
import re
import subprocess
import time
import traceback
import urllib.request
from datetime import datetime
from pathlib import Path

from playwright.sync_api import sync_playwright

PORT = 9460
CDP = f"http://127.0.0.1:{PORT}"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
PROFILE = str(Path.home() / ".hos-chrome-youtube-studio")
CHANNEL = "UCXp7HkBIl1LgaznXuZHJyRg"
ALLOWLIST = {
    "_C92tIJCk8A",  # premiere / live long
    "H1y0DXFVmw8",  # live short
    "iqToagXnjX0",  # live short
    "8_Edn_HCi1s",  # live short
    "sILtQxgYQk8",  # scheduled Mon
    "93fPUG-hW0A",  # scheduled Tue
}
TWINS = [
    "8uBR-9oxeWs",
    "YX2UR1u-JCQ",
    "Fnb3p81u-wY",
    "vpuRgKXtFlY",
    "Lcmh5y2KMQM",
]

EV = Path(
    "/Users/benjaminoats/YouTube/History Of Science/02_Video-Projects/"
    "001_How-Did-We-Discover-Germs/11_Upload-Package/Schedule/"
    "evidence_2026-09-07_hard_delete"
)
LOG = EV / "run.log"


def log(msg: str) -> None:
    EV.mkdir(parents=True, exist_ok=True)
    line = f"{datetime.now().isoformat(timespec='seconds')} {msg}"
    print(line, flush=True)
    with LOG.open("a") as f:
        f.write(line + "\n")


def dump(name: str, obj) -> None:
    EV.mkdir(parents=True, exist_ok=True)
    (EV / name).write_text(json.dumps(obj, indent=2) + "\n")


def shot(page, name: str) -> str:
    EV.mkdir(parents=True, exist_ok=True)
    dest = EV / name
    try:
        page.screenshot(path=str(dest), full_page=False)
        return str(dest)
    except Exception as e:
        log(f"shot_err {name}: {e}")
        return ""


def chrome_up() -> bool:
    try:
        urllib.request.urlopen(f"{CDP}/json/version", timeout=2).read()
        return True
    except Exception:
        return False


def kill_port_chrome() -> None:
    """Kill only the Chrome process listening on our CDP port (by PID)."""
    try:
        out = subprocess.check_output(["lsof", "-ti", f":{PORT}"], text=True).strip()
    except subprocess.CalledProcessError:
        return
    for pid in out.split():
        if pid.isdigit():
            log(f"kill_pid={pid}")
            subprocess.call(["kill", pid])
    time.sleep(1.5)
    try:
        out2 = subprocess.check_output(["lsof", "-ti", f":{PORT}"], text=True).strip()
    except subprocess.CalledProcessError:
        return
    for pid in out2.split():
        if pid.isdigit():
            log(f"kill_9_pid={pid}")
            subprocess.call(["kill", "-9", pid])
    time.sleep(1)


def ensure_chrome() -> None:
    if chrome_up():
        log("chrome_already_up")
        return
    kill_port_chrome()
    p = Path(PROFILE)
    for name in ("SingletonLock", "SingletonSocket", "SingletonCookie", "DevToolsActivePort"):
        try:
            (p / name).unlink()
        except FileNotFoundError:
            pass
    log("starting_chrome")
    subprocess.Popen(
        [
            CHROME,
            f"--remote-debugging-port={PORT}",
            "--remote-allow-origins=*",
            f"--user-data-dir={PROFILE}",
            "--no-first-run",
            "--no-default-browser-check",
            "--disable-background-timer-throttling",
            "--disable-renderer-backgrounding",
            "--disable-backgrounding-occluded-windows",
            f"https://studio.youtube.com/channel/{CHANNEL}",
        ],
        stdout=open("/tmp/hos_chrome_9460_hard_delete.log", "a"),
        stderr=subprocess.STDOUT,
        start_new_session=True,
    )
    for i in range(90):
        if chrome_up():
            log(f"chrome_up_{i}")
            return
        time.sleep(0.5)
    raise RuntimeError("chrome_failed_to_start")


def body(page, n: int = 8000) -> str:
    try:
        return page.inner_text("body")[:n]
    except Exception as e:
        return str(e)


def dismiss(page) -> None:
    for name in ["Got it", "Dismiss", "Not now", "No thanks", "Skip", "Close"]:
        try:
            b = page.get_by_role("button", name=re.compile(rf"^{name}$", re.I))
            if b.count() and b.first.is_visible():
                b.first.click(timeout=500, force=True)
        except Exception:
            pass


def auth_probe(page) -> dict:
    page.goto(
        f"https://studio.youtube.com/channel/{CHANNEL}",
        wait_until="domcontentloaded",
        timeout=120000,
    )
    page.wait_for_timeout(3500)
    t = body(page, 3500)
    shot(page, "00_auth_probe.png")
    signed_out = bool(
        re.search(r"Choose an account|Signed out|Sign in", t, re.I)
        and "History of Science" not in t
    )
    ok = (not signed_out) and (
        "History of Science" in t or "UCXp7HkBIl1LgaznXuZHJyRg" in (page.url or "")
    )
    orbitish = bool(re.search(r"Orbit With Ben|@OrbitWithBen|Oppti", t, re.I))
    info = {
        "ok": ok and not orbitish,
        "signed_out": signed_out,
        "orbitish": orbitish,
        "url": page.url,
        "snip": t[:800],
        "channelId": CHANNEL,
        "account_hint": "benoats86@gmail.com expected for HOS Studio",
    }
    dump("00_AUTH.json", info)
    if signed_out or not ok or orbitish:
        dump(
            "BLOCKED_AUTH.json",
            {
                "status": "BLOCKED_AUTH",
                "reason": (
                    "Studio signed out or wrong channel — Ben must sign in as "
                    "benoats86@gmail.com. Never paste passwords."
                ),
                "channelId": CHANNEL,
                "probe": info,
                "at": datetime.now().isoformat(timespec="seconds"),
            },
        )
        shot(page, "00_BLOCKED_AUTH.png")
    return info


def list_rows(page) -> list[dict]:
    return page.evaluate(
        """()=>{
      const out=[];
      const walk=(r,d=0)=>{
        if(!r||d>50) return;
        for(const a of (r.querySelectorAll?r.querySelectorAll('a[href*="/video/"]'):[])){
          const m=(a.getAttribute('href')||'').match(/\\/video\\/([A-Za-z0-9_-]{11})/);
          if(!m) continue;
          let row=a;
          for(let i=0;i<12&&row;i++){
            if((row.innerText||'').length>40) break;
            row=row.parentElement;
          }
          out.push({id:m[1], text:((row&&row.innerText)||'').replace(/\\s+/g,' ').trim().slice(0,280)});
        }
        for(const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
          if(el.shadowRoot) walk(el.shadowRoot,d+1);
      };
      walk(document);
      const map={};
      for(const o of out){
        if(!map[o.id] || o.text.length>(map[o.id].text||'').length) map[o.id]=o;
      }
      return Object.values(map);
    }"""
    )


def scroll_content(page, rounds: int = 8) -> None:
    for _ in range(rounds):
        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        page.wait_for_timeout(700)
        page.mouse.wheel(0, 2400)
        page.wait_for_timeout(500)


def inventory_shelf(page) -> dict:
    tabs = {
        "videos": f"https://studio.youtube.com/channel/{CHANNEL}/videos/upload",
        "shorts": f"https://studio.youtube.com/channel/{CHANNEL}/videos/short",
        "live": f"https://studio.youtube.com/channel/{CHANNEL}/videos/live",
    }
    by_tab: dict[str, list[dict]] = {}
    all_map: dict[str, dict] = {}
    for key, url in tabs.items():
        page.goto(url, wait_until="domcontentloaded", timeout=120000)
        page.wait_for_timeout(2800)
        dismiss(page)
        scroll_content(page, 10)
        rows = list_rows(page)
        by_tab[key] = rows
        shot(page, f"10_inventory_{key}.png")
        for r in rows:
            prev = all_map.get(r["id"])
            if not prev or len(r.get("text", "")) > len(prev.get("text", "")):
                all_map[r["id"]] = {**r, "tab": key}
        log(f"inventory_{key} n={len(rows)} ids={[r['id'] for r in rows]}")
    items = list(all_map.values())
    keep = []
    delete = []
    for it in items:
        vid = it["id"]
        entry = {
            "id": vid,
            "tab": it.get("tab"),
            "text": it.get("text", ""),
            "allowlisted": vid in ALLOWLIST,
            "named_twin": vid in TWINS,
        }
        if vid in ALLOWLIST:
            keep.append(entry)
        else:
            delete.append(entry)
    seen = {d["id"] for d in delete}
    for twin in TWINS:
        if twin not in seen and twin not in ALLOWLIST:
            delete.append(
                {
                    "id": twin,
                    "tab": "forced_twin",
                    "text": "named twin (force probe)",
                    "allowlisted": False,
                    "named_twin": True,
                }
            )
    out = {
        "at": datetime.now().isoformat(timespec="seconds"),
        "channelId": CHANNEL,
        "allowlist": sorted(ALLOWLIST),
        "by_tab_counts": {k: len(v) for k, v in by_tab.items()},
        "shelf_count": len(items),
        "keep": keep,
        "delete_candidates": delete,
        "by_tab": by_tab,
    }
    dump("10_INVENTORY.json", out)
    return out


def click_named(page, name: str) -> bool:
    try:
        loc = page.get_by_role("button", name=re.compile(rf"^{re.escape(name)}$", re.I))
        if loc.count() and loc.last.is_visible():
            loc.last.click(force=True, timeout=2500)
            return True
    except Exception:
        pass
    try:
        loc = page.get_by_text(re.compile(rf"^{re.escape(name)}$", re.I))
        if loc.count():
            loc.last.click(force=True, timeout=2500)
            return True
    except Exception:
        pass
    return bool(
        page.evaluate(
            """(name)=>{
          const re=new RegExp('^'+name.replace(/[.*+?^${}()|[\\]\\\\]/g,'\\\\$&')+'$','i');
          const walk=(r,d=0)=>{
            if(!r||d>50) return false;
            for(const el of (r.querySelectorAll?r.querySelectorAll('button,ytcp-button,[role=button],tp-yt-paper-item,[role=menuitem],span,div'):[])){
              const t=(el.innerText||'').trim();
              if(re.test(t)){
                const box=el.getBoundingClientRect();
                if(box.width>8 && box.height>8){ el.click(); return true; }
              }
            }
            for(const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
              if(el.shadowRoot && walk(el.shadowRoot,d+1)) return true;
            return false;
          };
          return walk(document);
        }""",
            name,
        )
    )


def open_options_menu(page) -> str | None:
    return page.evaluate(
        """()=>{
      const walk=(r,d=0)=>{
        if(!r||d>50) return null;
        for(const el of (r.querySelectorAll?r.querySelectorAll('ytcp-icon-button,button,[role=button]'):[])){
          const a=(el.getAttribute('aria-label')||'');
          if(/options|more actions|more options|^More$/i.test(a)){
            const box=el.getBoundingClientRect();
            if(box.width>8){ el.click(); return a; }
          }
        }
        for(const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
          if(el.shadowRoot){ const x=walk(el.shadowRoot,d+1); if(x) return x; }
        return null;
      };
      return walk(document);
    }"""
    )


def click_delete_menu_item(page) -> str | None:
    return page.evaluate(
        """()=>{
      const walk=(r,d=0)=>{
        if(!r||d>50) return null;
        for(const el of (r.querySelectorAll?r.querySelectorAll('tp-yt-paper-item,[role=menuitem],yt-formatted-string,span,div,ytcp-text-menu-item'):[])){
          const t=(el.innerText||'').trim();
          if(/^Delete(?: forever)?$/i.test(t) || /^Move to trash$/i.test(t)){
            const box=el.getBoundingClientRect();
            if(box.width>20 && box.height>10){ el.click(); return t; }
          }
        }
        for(const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
          if(el.shadowRoot){ const x=walk(el.shadowRoot,d+1); if(x) return x; }
        return null;
      };
      return walk(document);
    }"""
    )


def video_gone(page, vid: str) -> bool:
    page.goto(
        f"https://studio.youtube.com/video/{vid}/edit",
        wait_until="domcontentloaded",
        timeout=120000,
    )
    page.wait_for_timeout(2200)
    t = body(page, 3000)
    return bool(
        re.search(
            r"not found|doesn't exist|does not exist|unavailable|moved to trash|"
            r"couldn't find|no longer available",
            t,
            re.I,
        )
    )


def check_permanent_ack(page) -> bool:
    """Tick 'I understand that deleting this video is permanent…' in the dialog."""
    # Prefer role=checkbox / native input inside the permanent-delete dialog
    try:
        box = page.get_by_role(
            "checkbox",
            name=re.compile(r"I understand that deleting", re.I),
        )
        if box.count():
            if not box.first.is_checked():
                box.first.check(force=True, timeout=2500)
            notes_hit = True
            return True
    except Exception:
        notes_hit = False
    checked = page.evaluate(
        """()=>{
      const walk=(r,d=0)=>{
        if(!r||d>50) return false;
        for(const el of (r.querySelectorAll?r.querySelectorAll('tp-yt-paper-checkbox,ytcp-checkbox-lit,input[type=checkbox],[role=checkbox]'):[])){
          const t=((el.innerText||'')+' '+(el.getAttribute('aria-label')||'')+' '+(el.getAttribute('label')||'')).trim();
          const near=(el.closest && (el.closest('ytcp-confirmation-dialog,tp-yt-paper-dialog,ytcp-dialog')||el.parentElement));
          const nearT=near?((near.innerText||'').slice(0,500)):'';
          if(/I understand that deleting|deleting this video is permanent/i.test(t+nearT)){
            if(el.getAttribute('aria-checked')==='true' || el.checked) return 'already';
            el.click();
            return 'clicked';
          }
        }
        // also click label text
        for(const el of (r.querySelectorAll?r.querySelectorAll('yt-formatted-string,span,div,label'):[])){
          const t=(el.innerText||'').trim();
          if(/^I understand that deleting this video is permanent/i.test(t)){
            el.click(); return 'label';
          }
        }
        for(const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
          if(el.shadowRoot){ const x=walk(el.shadowRoot,d+1); if(x) return x; }
        return false;
      };
      return walk(document);
    }"""
    )
    return bool(checked)


def click_delete_forever_enabled(page) -> bool:
    """Click the enabled Delete forever button inside the confirmation dialog."""
    return bool(
        page.evaluate(
            """()=>{
      const walk=(r,d=0)=>{
        if(!r||d>50) return false;
        for(const el of (r.querySelectorAll?r.querySelectorAll('button,ytcp-button,[role=button]'):[])){
          const t=(el.innerText||'').trim();
          if(!/^Delete forever$/i.test(t)) continue;
          const dis=el.disabled || el.getAttribute('aria-disabled')==='true'
            || el.classList.contains('disabled') || el.getAttribute('disabled')!=null;
          const box=el.getBoundingClientRect();
          if(!dis && box.width>20){ el.click(); return true; }
        }
        for(const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
          if(el.shadowRoot && walk(el.shadowRoot,d+1)) return true;
        return false;
      };
      return walk(document);
    }"""
        )
    )


def hard_delete_one(page, vid: str) -> dict:
    if vid in ALLOWLIST:
        return {"id": vid, "ok": False, "skipped": True, "reason": "ALLOWLIST"}
    notes: list[str] = []
    page.goto(
        f"https://studio.youtube.com/video/{vid}/edit",
        wait_until="domcontentloaded",
        timeout=120000,
    )
    page.wait_for_timeout(2500)
    dismiss(page)
    t0 = body(page, 2500)
    shot(page, f"20_before_{vid}.png")
    if re.search(r"not found|doesn't exist|unavailable|no longer available", t0, re.I):
        return {"id": vid, "ok": True, "already_gone": True, "notes": ["already_gone"]}

    menu = open_options_menu(page)
    notes.append(f"menu={menu}")
    page.wait_for_timeout(800)
    item = click_delete_menu_item(page)
    notes.append(f"item={item}")
    page.wait_for_timeout(1000)
    shot(page, f"20b_menu_{vid}.png")

    # First click may open "Permanently delete this video?" OR select Delete in menu
    # then open dialog. If dialog not open yet, click Delete / Delete forever once.
    dlg = body(page, 2000)
    if not re.search(r"Permanently delete this video|I understand that deleting", dlg, re.I):
        for label in ("Delete forever", "Delete", "Move to trash"):
            if click_named(page, label):
                notes.append(f"open_dlg={label}")
                page.wait_for_timeout(1000)
                break

    shot(page, f"20c_dialog_{vid}.png")
    ack = check_permanent_ack(page)
    notes.append(f"ack={ack}")
    page.wait_for_timeout(600)
    shot(page, f"20d_acked_{vid}.png")

    confirmed = False
    if click_delete_forever_enabled(page):
        notes.append("confirm=Delete forever (enabled)")
        confirmed = True
    else:
        for label in ("Delete forever", "Delete", "Confirm", "Yes"):
            if click_named(page, label):
                notes.append(f"confirm={label}")
                confirmed = True
                break
    page.wait_for_timeout(2800)
    shot(page, f"21_after_click_{vid}.png")

    # If still on dialog (ack failed first pass), retry ack + confirm
    t_mid = body(page, 2000)
    if re.search(r"Permanently delete this video|I understand that deleting", t_mid, re.I):
        notes.append("dialog_still_open_retry")
        ack2 = check_permanent_ack(page)
        notes.append(f"ack2={ack2}")
        page.wait_for_timeout(500)
        if click_delete_forever_enabled(page):
            notes.append("confirm2=Delete forever")
            confirmed = True
            page.wait_for_timeout(2800)
            shot(page, f"21b_retry_{vid}.png")

    gone = video_gone(page, vid)
    in_trash = False
    if not gone:
        t = body(page, 2500)
        in_trash = bool(re.search(r"trash|deleted|no longer available", t, re.I))
        notes.append(f"post_snip={t[:200]}")
    result = {
        "id": vid,
        "ok": bool(gone),
        "gone_from_edit": gone,
        "in_trash_hint": in_trash,
        "confirmed_click": confirmed,
        "notes": notes,
    }
    dump(f"22_delete_{vid}.json", result)
    log(f"delete {vid} ok={result['ok']} gone={gone} notes={notes}")
    return result


def empty_trash(page) -> dict:
    urls = [
        (
            f"https://studio.youtube.com/channel/{CHANNEL}/videos/restricted"
            "?filter=%5B%7B%22name%22%3A%22CONTENT_RESTRICTION%22%2C%22value%22%3A%22TRASHED%22%7D%5D"
        ),
        (
            f"https://studio.youtube.com/channel/{CHANNEL}/videos/short"
            "?filter=%5B%7B%22name%22%3A%22CONTENT_RESTRICTION%22%2C%22value%22%3A%22TRASHED%22%7D%5D"
        ),
    ]
    notes: list[str] = []
    deleted_from_trash: list[str] = []
    for url in urls:
        page.goto(url, wait_until="domcontentloaded", timeout=120000)
        page.wait_for_timeout(3000)
        dismiss(page)
        scroll_content(page, 6)
        shot(page, f"30_trash_{'short' if 'short' in url else 'videos'}.png")
        rows = list_rows(page)
        notes.append(f"trash_rows={len(rows)}")
        if click_named(page, "Empty trash"):
            notes.append("empty_trash_clicked")
            page.wait_for_timeout(800)
            for label in ("Empty trash", "Delete forever", "Delete", "Confirm", "Yes"):
                if click_named(page, label):
                    notes.append(f"empty_confirm={label}")
                    page.wait_for_timeout(1500)
            page.wait_for_timeout(2500)
            shot(page, "31_after_empty_trash.png")
        for r in list_rows(page):
            vid = r["id"]
            if vid in ALLOWLIST:
                notes.append(f"trash_skip_allowlist={vid}")
                continue
            page.goto(
                f"https://studio.youtube.com/video/{vid}/edit",
                wait_until="domcontentloaded",
                timeout=120000,
            )
            page.wait_for_timeout(1800)
            open_options_menu(page)
            page.wait_for_timeout(600)
            click_delete_menu_item(page)
            page.wait_for_timeout(700)
            for label in ("Delete forever", "Delete", "Confirm", "Yes"):
                if click_named(page, label):
                    notes.append(f"trash_del={vid}:{label}")
                    page.wait_for_timeout(1000)
                    break
            if video_gone(page, vid):
                deleted_from_trash.append(vid)
    out = {"notes": notes, "deleted_from_trash": deleted_from_trash}
    dump("30_TRASH.json", out)
    return out


def cancel_stuck_uploads(page) -> list[str]:
    notes: list[str] = []
    page.goto(
        f"https://studio.youtube.com/channel/{CHANNEL}/videos/short",
        wait_until="domcontentloaded",
        timeout=120000,
    )
    page.wait_for_timeout(2500)
    for i in range(10):
        clicked = False
        try:
            loc = page.get_by_text(re.compile(r"^Cancel upload$", re.I))
            if loc.count():
                loc.first.click(force=True, timeout=2500)
                clicked = True
                notes.append(f"cancel_{i}")
                page.wait_for_timeout(800)
                for name in ["Cancel upload", "Confirm", "Yes", "OK", "Done"]:
                    click_named(page, name)
                page.wait_for_timeout(1000)
        except Exception as e:
            notes.append(f"cancel_err_{i}={e}")
        if not clicked:
            break
    shot(page, "05_after_cancel_uploads.png")
    return notes


def main() -> int:
    if LOG.exists():
        LOG.unlink()
    EV.mkdir(parents=True, exist_ok=True)
    report: dict = {
        "started": datetime.now().isoformat(timespec="seconds"),
        "channelId": CHANNEL,
        "allowlist": sorted(ALLOWLIST),
        "twins": TWINS,
        "deleted": [],
        "failed": [],
        "skipped_allowlist": [],
        "ok": False,
    }
    dump(
        "ALLOWLIST.json",
        {"channelId": CHANNEL, "allowlist": sorted(ALLOWLIST), "twins": TWINS},
    )

    try:
        ensure_chrome()
    except Exception as e:
        report["error"] = f"chrome:{e}"
        dump("RESULT.json", report)
        log(f"CHROME_FAIL {e}")
        return 3

    with sync_playwright() as pw:
        browser = pw.chromium.connect_over_cdp(CDP)
        ctx = browser.contexts[0]
        page = next(
            (p for p in ctx.pages if "studio.youtube.com" in (p.url or "")),
            None,
        ) or ctx.new_page()

        def _dlg(d):
            try:
                if d.type == "beforeunload":
                    d.accept()
                else:
                    d.dismiss()
            except Exception:
                pass

        page.on("dialog", _dlg)

        auth = auth_probe(page)
        if not auth.get("ok"):
            report["stopped"] = "BLOCKED_AUTH"
            report["auth"] = auth
            dump("RESULT.json", report)
            log("BLOCKED_AUTH — stop. Ben must sign in.")
            return 2
        log("AUTH_OK")
        report["auth"] = {"ok": True, "url": auth.get("url")}

        report["cancel_uploads"] = cancel_stuck_uploads(page)

        inv = inventory_shelf(page)
        report["inventory_before"] = {
            "shelf_count": inv["shelf_count"],
            "keep_ids": [k["id"] for k in inv["keep"]],
            "delete_ids": [d["id"] for d in inv["delete_candidates"]],
        }

        for d in inv["delete_candidates"]:
            if d["id"] in ALLOWLIST:
                report["fatal"] = f"allowlist_in_delete_list:{d['id']}"
                dump("RESULT.json", report)
                log(report["fatal"])
                return 4

        for d in inv["delete_candidates"]:
            vid = d["id"]
            if vid in ALLOWLIST:
                report["skipped_allowlist"].append(vid)
                continue
            try:
                res = hard_delete_one(page, vid)
                if res.get("skipped"):
                    report["skipped_allowlist"].append(vid)
                elif res.get("ok") or res.get("already_gone"):
                    report["deleted"].append(res)
                else:
                    report["failed"].append(res)
            except Exception as e:
                report["failed"].append(
                    {
                        "id": vid,
                        "ok": False,
                        "error": str(e),
                        "tb": traceback.format_exc()[-400:],
                    }
                )

        report["trash"] = empty_trash(page)

        inv2 = inventory_shelf(page)
        report["inventory_after"] = {
            "shelf_count": inv2["shelf_count"],
            "keep_ids": [k["id"] for k in inv2["keep"]],
            "leftover_non_allowlist": [
                d["id"]
                for d in inv2["delete_candidates"]
                if d.get("tab") != "forced_twin"
            ],
            "items": inv2["keep"]
            + [d for d in inv2["delete_candidates"] if d.get("tab") != "forced_twin"],
        }

        allow_status = {}
        missing_allow = []
        for vid in sorted(ALLOWLIST):
            gone = video_gone(page, vid)
            allow_status[vid] = {"gone": gone}
            if gone:
                missing_allow.append(vid)
            shot(page, f"40_allowlist_{vid}.png")
        report["allowlist_status"] = allow_status
        report["missing_allowlist_alarm"] = sorted(set(missing_allow))

        twin_status = {}
        for vid in TWINS:
            twin_status[vid] = {"gone": video_gone(page, vid)}
            shot(page, f"41_twin_{vid}.png")
        report["twin_status"] = twin_status

        leftovers = [
            d["id"]
            for d in inv2["delete_candidates"]
            if d.get("tab") != "forced_twin" and d["id"] not in ALLOWLIST
        ]
        twins_left = [t for t, s in twin_status.items() if not s.get("gone")]
        report["leftovers"] = sorted(set(leftovers + twins_left))
        report["remaining_shelf_count"] = inv2["shelf_count"]
        report["deleted_ids"] = [d["id"] for d in report["deleted"]]
        report["ok"] = (
            not report["leftovers"]
            and not report["missing_allowlist_alarm"]
            and all(not allow_status[v]["gone"] for v in ALLOWLIST)
        )
        report["finished"] = datetime.now().isoformat(timespec="seconds")
        dump("RESULT.json", report)

        md = [
            "# HOS hard delete leftovers — 2026-09-07",
            "",
            f"Channel: `{CHANNEL}` (@HistoryOfScienceYT only)",
            "",
            "## Allowlist (kept)",
            "",
        ]
        for vid in sorted(ALLOWLIST):
            st = allow_status.get(vid, {})
            md.append(f"- `{vid}` gone={st.get('gone')}")
        md += ["", "## Deleted", ""]
        for vid in report["deleted_ids"]:
            md.append(f"- `{vid}`")
        if report["failed"]:
            md += ["", "## Failed", ""]
            for f in report["failed"]:
                md.append(f"- `{f.get('id')}` notes={f.get('notes') or f.get('error')}")
        md += [
            "",
            f"## Remaining shelf count: **{report['remaining_shelf_count']}**",
            "",
            f"Leftovers: {report['leftovers'] or 'none'}",
            "",
            f"OK: **{report['ok']}**",
            "",
        ]
        (EV / "REPORT.md").write_text("\n".join(md) + "\n")
        log(
            f"DONE ok={report['ok']} deleted={report['deleted_ids']} "
            f"shelf={report['remaining_shelf_count']}"
        )
        return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
