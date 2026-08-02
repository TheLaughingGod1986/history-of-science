#!/usr/bin/env python3
"""Publish V001 Short #01 as Public now (catch-up — long already live)."""
from __future__ import annotations

import json
import re
from pathlib import Path

from playwright.sync_api import sync_playwright

PROFILE = "/Users/ben/code/youtube/.playwright-youtube-profile"
ROOT = Path(
    "/Users/ben/code/Orbit-YouTube/02_Video-Projects/001_Will-We-Ever-Meet-Aliens"
)
INDEX_PATH = ROOT / "10_Shorts/SHORTS_UPLOAD_INDEX.json"
INDEX = json.loads(INDEX_PATH.read_text())
AUDIT = ROOT / "11_Upload-Package/Schedule/_studio_audit_shorts_v001"
OUT = ROOT / "11_Upload-Package/Schedule/aliens_short01_publish_now_v01.json"
TARGET_ID = "01"
ORBIT = "UC_esArsDKd3GJvOkeO0DUog"


def skip(page):
    try:
        page.get_by_role("link", name=re.compile(r"Skip", re.I)).click(timeout=800)
    except Exception:
        pass


def visibility_chip(page) -> str:
    try:
        return page.locator("ytcp-video-metadata-visibility").first.inner_text(
            timeout=2500
        ).replace("\n", " ")
    except Exception:
        return ""


def is_public(chip: str) -> bool:
    return bool(re.search(r"\bPublic\b", chip)) and not re.search(
        r"\bScheduled\b", chip, re.I
    )


def open_visibility(page) -> None:
    page.locator("ytcp-video-metadata-visibility").first.scroll_into_view_if_needed()
    page.wait_for_timeout(250)
    page.locator("ytcp-video-metadata-visibility").first.click(force=True)
    page.wait_for_timeout(1600)


def collapse_schedule_panel(page) -> dict | None:
    return page.evaluate(
        """() => {
          const dlg=document.querySelector('tp-yt-paper-dialog[aria-label="Select video privacy"]')
            || document.querySelector('tp-yt-paper-dialog');
          const walk=(root)=>{
            for (const el of root.querySelectorAll('*')) {
              const al=(el.getAttribute('aria-label')||'');
              const id=el.id||'';
              if (id==='first-container-expand-button' || /click to (expand|collapse)/i.test(al)) {
                const r=el.getBoundingClientRect();
                if (r.width>5) { el.click(); return {al,id,x:r.x,y:r.y}; }
              }
              if (el.shadowRoot) {
                const x=walk(el.shadowRoot);
                if (x) return x;
              }
            }
            return null;
          };
          let hasPublic=false;
          const find=(root)=>{
            for (const el of root.querySelectorAll('tp-yt-paper-radio-button,[role=radio]')) {
              const n=(el.getAttribute('name')||'').toUpperCase();
              const t=(el.innerText||'').trim();
              const r=el.getBoundingClientRect();
              if ((n==='PUBLIC' || t==='Public') && r.width>10 && r.height>5) hasPublic=true;
            }
            for (const el of root.querySelectorAll('*')) if (el.shadowRoot) find(el.shadowRoot);
          };
          find(dlg||document);
          if (hasPublic) return {already:true};
          return walk(dlg||document);
        }"""
    )


def click_public_radio(page) -> dict | None:
    return page.evaluate(
        """() => {
          const dlg=document.querySelector('tp-yt-paper-dialog[aria-label="Select video privacy"]')
            || document.querySelector('tp-yt-paper-dialog');
          const walk=(root)=>{
            for (const el of root.querySelectorAll('tp-yt-paper-radio-button,[role=radio]')) {
              const n=(el.getAttribute('name')||'').toUpperCase();
              const t=(el.innerText||'').replace(/\\s+/g,' ').trim();
              if (n==='PUBLIC' || t==='Public') {
                el.scrollIntoView({block:'center'});
                el.click();
                return {ok:true, name:n, t:t.slice(0,40)};
              }
            }
            for (const el of root.querySelectorAll('*')) {
              if (!el.shadowRoot) continue;
              const x=walk(el.shadowRoot);
              if (x) return x;
            }
            return null;
          };
          return walk(dlg||document);
        }"""
    )


def click_done(page) -> bool:
    try:
        btn = page.get_by_role("button", name="Done", exact=True)
        if btn.count():
            (btn.last if btn.count() > 1 else btn.first).click(force=True, timeout=3000)
            page.wait_for_timeout(1500)
            return True
    except Exception:
        pass
    return False


def save(page) -> bool:
    try:
        b = page.get_by_role("button", name="Save", exact=True)
        if b.count() and b.first.is_enabled():
            b.first.click(force=True)
            page.wait_for_timeout(4000)
            return True
    except Exception:
        pass
    return False


def set_public(page, vid: str, num: str) -> dict:
    r: dict = {"id": num, "video_id": vid, "ok": False}
    page.goto(
        f"https://studio.youtube.com/video/{vid}/edit",
        wait_until="domcontentloaded",
        timeout=120000,
    )
    page.wait_for_timeout(4000)
    skip(page)

    chip0 = visibility_chip(page)
    r["before"] = chip0
    if is_public(chip0):
        r["ok"] = True
        r["already"] = True
        r["visibility_snip"] = chip0
        return r

    try:
        open_visibility(page)
    except Exception:
        page.get_by_text(re.compile(r"Visibility|Scheduled", re.I)).first.click(
            force=True
        )
        page.wait_for_timeout(1400)

    page.screenshot(path=str(AUDIT / f"short01_dlg.png"))
    r["collapse"] = collapse_schedule_panel(page)
    page.wait_for_timeout(1000)
    page.screenshot(path=str(AUDIT / f"short01_radios.png"))

    r["public_click"] = click_public_radio(page)
    if not (r["public_click"] and r["public_click"].get("ok")):
        collapse_schedule_panel(page)
        page.wait_for_timeout(900)
        r["public_click"] = click_public_radio(page)

    page.wait_for_timeout(600)
    r["done"] = click_done(page)
    r["saved"] = save(page)

    page.reload(wait_until="domcontentloaded")
    page.wait_for_timeout(3500)
    skip(page)
    chip = visibility_chip(page)
    r["visibility_snip"] = chip
    r["ok"] = is_public(chip)
    page.screenshot(path=str(AUDIT / f"short01_done.png"))
    return r


def main():
    AUDIT.mkdir(parents=True, exist_ok=True)
    target = next(s for s in INDEX["shorts"] if s["id"] == TARGET_ID)
    result = {"target": target["video_id"], "title": target["title"], "ok": False}

    with sync_playwright() as p:
        ctx = p.chromium.launch_persistent_context(
            PROFILE,
            headless=False,
            channel="chrome",
            args=["--disable-blink-features=AutomationControlled"],
            viewport={"width": 1440, "height": 1100},
        )
        page = ctx.pages[0] if ctx.pages else ctx.new_page()
        print(f"PUBLIC {target['id']} {target['video_id']}…", flush=True)
        try:
            rr = set_public(page, target["video_id"], target["id"])
        except Exception as e:
            rr = {
                "id": target["id"],
                "video_id": target["video_id"],
                "ok": False,
                "error": str(e)[:400],
            }
        result["publish"] = rr
        print(
            f"  → ok={rr.get('ok')} before={rr.get('before','')[:50]} "
            f"vis={rr.get('visibility_snip','')[:80]}",
            flush=True,
        )

        # Verify public watch page
        page.goto(
            f"https://www.youtube.com/watch?v={target['video_id']}",
            wait_until="domcontentloaded",
            timeout=90000,
        )
        page.wait_for_timeout(3500)
        watch = page.locator("body").inner_text()[:1200]
        result["watch_private"] = bool(
            re.search(r"private|Sign in to confirm", watch, re.I)
        )
        result["watch_has_title"] = "Where Is Everybody" in watch or "Fermi" in watch
        page.screenshot(path=str(AUDIT / "short01_watch.png"))

        page.goto(
            f"https://studio.youtube.com/channel/{ORBIT}/videos/short",
            wait_until="domcontentloaded",
        )
        page.wait_for_timeout(4000)
        skip(page)
        page.screenshot(path=str(AUDIT / "short01_shorts_tab.png"), full_page=True)

        result["ok"] = bool(rr.get("ok")) and not result["watch_private"]
        OUT.write_text(json.dumps(result, indent=2) + "\n")

        if rr.get("ok"):
            target["visibility"] = "public"
            target["published_now"] = True
            target["schedule_iso"] = "2026-07-31T17:50:00+01:00"
            target["note"] = "Published Public now via Studio (catch-up)"
            target.pop("action_required", None)
            INDEX_PATH.write_text(json.dumps(INDEX, indent=2) + "\n")

            # Mirror to TikTok + Meta (IG/FB) + Threads
            try:
                import importlib.util
                from pathlib import Path as _P

                def _load_notify(auto_dir: _P, mod_name: str):
                    path = auto_dir / "hooks.py"
                    spec = importlib.util.spec_from_file_location(mod_name, path)
                    mod = importlib.util.module_from_spec(spec)
                    assert spec and spec.loader
                    spec.loader.exec_module(mod)
                    return mod.notify_short_live

                _base = _P("/Users/ben/code/Orbit-YouTube/00_Brand/Channel-Setup")
                tr = _load_notify(_base / "TikTok" / "auto", "orbit_tiktok_hooks")(
                    ROOT, target
                )
                result["tiktok"] = tr
                print(f"tiktok → {tr.get('status')}", flush=True)
                mr = _load_notify(_base / "Meta" / "auto", "orbit_meta_hooks")(
                    ROOT, target
                )
                result["meta"] = mr
                print(f"meta → {mr.get('status')}", flush=True)
                thr = _load_notify(_base / "Threads" / "auto", "orbit_threads_hooks")(
                    ROOT, target
                )
                result["threads"] = thr
                print(f"threads → {thr.get('status')}", flush=True)
                OUT.write_text(json.dumps(result, indent=2) + "\n")
            except Exception as e:
                print("social mirror hooks skipped:", e, flush=True)

        ctx.close()
        print("RESULT ok=", result["ok"], flush=True)
        raise SystemExit(0 if result["ok"] else 1)


if __name__ == "__main__":
    main()
