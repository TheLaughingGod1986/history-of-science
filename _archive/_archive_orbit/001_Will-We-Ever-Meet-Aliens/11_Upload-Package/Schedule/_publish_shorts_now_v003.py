#!/usr/bin/env python3
"""Publish all V001 Shorts as Public (v03 — collapse Schedule, then Public radio)."""
from __future__ import annotations

import json
import re
from pathlib import Path

from playwright.sync_api import sync_playwright

PROFILE = "/Users/ben/code/youtube/.playwright-youtube-profile"
ROOT = Path(
    "/Users/ben/code/Orbit-YouTube/02_Video-Projects/001_Will-We-Ever-Meet-Aliens"
)
INDEX = json.loads((ROOT / "10_Shorts/SHORTS_UPLOAD_INDEX.json").read_text())
AUDIT = ROOT / "11_Upload-Package/Schedule/_studio_audit_shorts_v001"
OUT = ROOT / "11_Upload-Package/Schedule/aliens_shorts_publish_now_v03.json"


def skip(page):
    try:
        page.get_by_role("link", name=re.compile(r"Skip", re.I)).click(timeout=800)
    except Exception:
        pass


def dismiss(page):
    page.keyboard.press("Escape")
    page.wait_for_timeout(350)


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
    """When Schedule is expanded, Private/Unlisted/Public radios are hidden.
    Click the schedule expand/collapse control to reveal them."""
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
          // If PUBLIC radio already visible, no collapse needed
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
        body = page.locator("body").inner_text()
        rel = body.split("Related video", 1)[-1][:100] if "Related video" in body else ""
        r["related_ok"] = "Haven't" in rel or "Fermi" in rel or "Aliens" in rel
        return r

    try:
        open_visibility(page)
    except Exception:
        page.get_by_text(re.compile(r"Visibility|Scheduled", re.I)).first.click(force=True)
        page.wait_for_timeout(1400)

    page.screenshot(path=str(AUDIT / f"pub_v03_{num}_dlg.png"))
    r["collapse"] = collapse_schedule_panel(page)
    page.wait_for_timeout(1000)
    page.screenshot(path=str(AUDIT / f"pub_v03_{num}_radios.png"))

    r["public_click"] = click_public_radio(page)
    if not (r["public_click"] and r["public_click"].get("ok")):
        # one more collapse attempt then retry
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
    body = page.locator("body").inner_text()
    rel = body.split("Related video", 1)[-1][:120] if "Related video" in body else ""
    r["related_snip"] = rel.replace("\n", " ")
    r["related_ok"] = "None" not in rel[:40] and (
        "Haven't" in rel or "Fermi" in rel or "Aliens" in rel
    )
    page.screenshot(path=str(AUDIT / f"pub_v03_{num}_done.png"))
    return r


def main():
    AUDIT.mkdir(parents=True, exist_ok=True)
    result = {"shorts": [], "ok": False}
    with sync_playwright() as p:
        ctx = p.chromium.launch_persistent_context(
            PROFILE,
            headless=False,
            channel="chrome",
            args=["--disable-blink-features=AutomationControlled"],
            viewport={"width": 1440, "height": 1100},
        )
        page = ctx.pages[0] if ctx.pages else ctx.new_page()
        for s in INDEX["shorts"]:
            print(f"PUBLIC {s['id']} {s['video_id']}…", flush=True)
            try:
                rr = set_public(page, s["video_id"], s["id"])
            except Exception as e:
                rr = {
                    "id": s["id"],
                    "video_id": s["video_id"],
                    "ok": False,
                    "error": str(e)[:400],
                }
            result["shorts"].append(rr)
            print(
                f"  → ok={rr.get('ok')} vis={rr.get('visibility_snip','')[:60]} "
                f"related={rr.get('related_ok')}",
                flush=True,
            )
            OUT.write_text(json.dumps(result, indent=2) + "\n")

        page.goto(
            "https://studio.youtube.com/channel/TBD_CREATE_HISTORY_OF_SCIENCE_CHANNEL/videos/short",
            wait_until="domcontentloaded",
        )
        page.wait_for_timeout(4500)
        skip(page)
        page.screenshot(path=str(AUDIT / "pub_v03_shorts_tab.png"), full_page=True)
        body = page.locator("body").inner_text()
        result["tab_public_count"] = len(re.findall(r"\bPublic\b", body))
        result["tab_scheduled_count"] = len(re.findall(r"\bScheduled\b", body))
        result["tab_titles"] = [
            t
            for t in (
                "Where Is Everybody",
                "Space Is Rude",
                "Aliens Are Watching",
                "First Alien Clue",
            )
            if t in body
        ]
        result["ok"] = all(x.get("ok") for x in result["shorts"])
        OUT.write_text(json.dumps(result, indent=2) + "\n")

        for s, rr in zip(INDEX["shorts"], result["shorts"]):
            if rr.get("ok"):
                s["visibility"] = "public"
                s["published_now"] = True
                s["note"] = "Published Public immediately (was scheduled Aug 2026)"
        (ROOT / "10_Shorts/SHORTS_UPLOAD_INDEX.json").write_text(
            json.dumps(INDEX, indent=2) + "\n"
        )

        # Mirror each newly public short to TikTok + Meta (IG/FB) + Threads.
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
            notify_tiktok = _load_notify(_base / "TikTok" / "auto", "orbit_tiktok_hooks")
            notify_meta = _load_notify(_base / "Meta" / "auto", "orbit_meta_hooks")
            notify_threads = _load_notify(
                _base / "Threads" / "auto", "orbit_threads_hooks"
            )

            for s, rr in zip(INDEX["shorts"], result["shorts"]):
                if not rr.get("ok"):
                    continue
                tr = notify_tiktok(ROOT, s)
                print(f"tiktok {s.get('id')} → {tr.get('status')}", flush=True)
                rr["tiktok"] = tr
                mr = notify_meta(ROOT, s)
                print(f"meta {s.get('id')} → {mr.get('status')}", flush=True)
                rr["meta"] = mr
                thr = notify_threads(ROOT, s)
                print(f"threads {s.get('id')} → {thr.get('status')}", flush=True)
                rr["threads"] = thr
            OUT.write_text(json.dumps(result, indent=2) + "\n")
        except Exception as e:
            print("social mirror hooks skipped:", e, flush=True)

        ctx.close()
        print("RESULT ok=", result["ok"], "tab_public=", result.get("tab_public_count"), flush=True)
        raise SystemExit(0 if result["ok"] else 1)


if __name__ == "__main__":
    main()
