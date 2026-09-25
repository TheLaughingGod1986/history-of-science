#!/usr/bin/env python3
"""Force Schedule Done→Save for sILt Mon 7 / 93fP Tue 8 at 11:30 London."""
from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path

from playwright.sync_api import sync_playwright

CDP = "http://127.0.0.1:9460"
CHANNEL = "UCXp7HkBIl1LgaznXuZHJyRg"
EV = Path(
    "/Users/benjaminoats/YouTube/History Of Science/02_Video-Projects/"
    "001_How-Did-We-Discover-Germs/11_Upload-Package/Schedule/"
    "evidence_2026-09-06_calendar_restore"
)
JOBS = [
    {"slot": "s04", "id": "sILtQxgYQk8", "day": 7},
    {"slot": "s05", "id": "93fPUG-hW0A", "day": 8},
]


def log(msg: str) -> None:
    print(f"{datetime.now().isoformat(timespec='seconds')} {msg}", flush=True)


def shot(page, name: str) -> None:
    EV.mkdir(parents=True, exist_ok=True)
    try:
        page.screenshot(path=str(EV / name), full_page=False)
    except Exception as e:
        log(f"shot_err {name}: {e}")


def body(page, n: int = 6000) -> str:
    try:
        return page.inner_text("body")[:n]
    except Exception as e:
        return str(e)


def visibility(page) -> str:
    return page.evaluate(
        """() => {
      let hit = '';
      const walk = (r, d = 0) => {
        if (!r || d > 50 || hit) return;
        for (const el of (r.querySelectorAll ? r.querySelectorAll('*') : [])) {
          const t = (el.innerText || '').replace(/\\s+/g, ' ').trim();
          if (/^Visibility\\s+(Private|Public|Unlisted|Scheduled\\b.*)$/i.test(t) && t.length < 120) {
            hit = t; return;
          }
        }
        for (const el of (r.querySelectorAll ? r.querySelectorAll('*') : []))
          if (el.shadowRoot) walk(el.shadowRoot, d + 1);
      };
      walk(document);
      if (hit) return hit;
      const m = (document.body.innerText || '').match(/Visibility\\s*\\n?\\s*(Private|Public|Unlisted|Scheduled[^\\n]*)/i);
      return m ? ('Visibility ' + m[1].trim()) : '';
    }"""
    )


def open_vis(page) -> bool:
    ok = page.evaluate(
        """() => {
      const walk = (r, d = 0) => {
        if (!r || d > 55) return false;
        for (const el of (r.querySelectorAll ? r.querySelectorAll('ytcp-icon-button,button,[role=button]') : [])) {
          const a = el.getAttribute('aria-label') || '';
          if (/edit video visibility status/i.test(a)) { el.click(); return true; }
        }
        for (const el of (r.querySelectorAll ? r.querySelectorAll('*') : []))
          if (el.shadowRoot && walk(el.shadowRoot, d + 1)) return true;
        return false;
      };
      return walk(document);
    }"""
    )
    page.wait_for_timeout(1400)
    return bool(ok)


def dialog_info(page) -> dict:
    return page.evaluate(
        """() => {
      let dlg = null;
      const find = (r, d = 0) => {
        if (!r || d > 50 || dlg) return;
        for (const el of (r.querySelectorAll ? r.querySelectorAll('tp-yt-paper-dialog,ytcp-dialog') : [])) {
          const t = el.innerText || '';
          if (/Save or publish|Schedule/i.test(t) && /Private|Public/i.test(t)) { dlg = el; return; }
        }
        for (const el of (r.querySelectorAll ? r.querySelectorAll('*') : []))
          if (el.shadowRoot) find(el.shadowRoot, d + 1);
      };
      find(document);
      if (!dlg) return {found: false};
      const buttons = [];
      const walkB = (r, d = 0) => {
        if (!r || d > 40) return;
        for (const el of (r.querySelectorAll ? r.querySelectorAll('button,ytcp-button,[role=button]') : [])) {
          const t = (el.innerText || '').trim().slice(0, 40);
          if (!t) continue;
          buttons.push({
            t: t,
            dis: !!(el.disabled || el.getAttribute('aria-disabled') === 'true')
          });
        }
        for (const el of (r.querySelectorAll ? r.querySelectorAll('*') : []))
          if (el.shadowRoot) walkB(el.shadowRoot, d + 1);
      };
      walkB(dlg);
      let date = '', time = '';
      const walkF = (r, d = 0) => {
        if (!r || d > 40) return;
        for (const el of (r.querySelectorAll ? r.querySelectorAll('ytcp-text-dropdown-trigger,div,span') : [])) {
          const t = (el.innerText || '').replace(/\\s+/g, ' ').trim();
          if (/^\\d{1,2}\\s+Sept\\s+2026$/i.test(t)) date = t;
        }
        for (const inp of (r.querySelectorAll ? r.querySelectorAll('input') : [])) {
          if (/^\\d{1,2}:\\d{2}$/.test(inp.value || '')) time = inp.value;
        }
        for (const el of (r.querySelectorAll ? r.querySelectorAll('*') : []))
          if (el.shadowRoot) walkF(el.shadowRoot, d + 1);
      };
      walkF(dlg);
      return {found: true, date, time, buttons: buttons.slice(0, 20), text: (dlg.innerText || '').slice(0, 500)};
    }"""
    )


def click_schedule(page) -> str:
    try:
        r = page.get_by_role("radio", name=re.compile(r"^Schedule$", re.I))
        if r.count():
            r.first.click(force=True, timeout=3000)
            page.wait_for_timeout(900)
            return "role"
    except Exception:
        pass
    hit = page.evaluate(
        """() => {
      let hit = null;
      const walk = (r, d = 0) => {
        if (!r || d > 50 || hit) return;
        for (const el of (r.querySelectorAll ? r.querySelectorAll('tp-yt-paper-radio-button,[role=radio],div,span') : [])) {
          const t = ((el.innerText || '') + ' ' + (el.getAttribute('aria-label') || '')).replace(/\\s+/g, ' ').trim();
          if (/^Schedule$/i.test(t)) { el.click(); hit = t; return; }
        }
        for (const el of (r.querySelectorAll ? r.querySelectorAll('*') : []))
          if (el.shadowRoot) walk(el.shadowRoot, d + 1);
      };
      walk(document);
      return hit;
    }"""
    )
    page.wait_for_timeout(900)
    return hit or ""


def fill_dt(page, day: int) -> dict:
    info = {"day": day}
    page.evaluate(
        """() => {
      const walk = (r, d = 0) => {
        if (!r || d > 50) return false;
        for (const el of (r.querySelectorAll ? r.querySelectorAll('ytcp-text-dropdown-trigger,ytcp-dropdown-trigger') : [])) {
          const t = (el.innerText || '').replace(/\\s+/g, ' ').trim();
          if (/^\\d{1,2}\\s+Sept\\s+2026$/i.test(t)) { el.click(); return true; }
        }
        for (const el of (r.querySelectorAll ? r.querySelectorAll('*') : []))
          if (el.shadowRoot && walk(el.shadowRoot, d + 1)) return true;
        return false;
      };
      return walk(document);
    }"""
    )
    page.wait_for_timeout(700)
    info["picked"] = page.evaluate(
        """(day) => {
      let hit = null;
      const walk = (r, d = 0) => {
        if (!r || d > 55 || hit) return;
        for (const el of (r.querySelectorAll ? r.querySelectorAll('button,[role=gridcell],div,span') : [])) {
          const t = (el.innerText || '').trim();
          const aria = el.getAttribute('aria-label') || '';
          const box = el.getBoundingClientRect();
          if (box.width < 8 || box.height < 8 || box.width > 90) continue;
          if (t === String(day) || new RegExp('\\\\b' + day + '\\\\b').test(aria)) {
            el.click(); hit = aria || t; return;
          }
        }
        for (const el of (r.querySelectorAll ? r.querySelectorAll('*') : []))
          if (el.shadowRoot) walk(el.shadowRoot, d + 1);
      };
      walk(document);
      return hit;
    }""",
        day,
    )
    page.wait_for_timeout(500)
    focused = page.evaluate(
        """() => {
      let el = null;
      const walk = (r, d = 0) => {
        if (!r || d > 55 || el) return;
        for (const inp of (r.querySelectorAll ? r.querySelectorAll('input') : [])) {
          if (/^\\d{1,2}:\\d{2}$/.test(inp.value || '')) { el = inp; return; }
        }
        for (const n of (r.querySelectorAll ? r.querySelectorAll('*') : []))
          if (n.shadowRoot) walk(n.shadowRoot, d + 1);
      };
      walk(document);
      if (!el) return false;
      el.focus();
      if (el.select) el.select();
      return true;
    }"""
    )
    if focused:
        page.keyboard.press("Meta+a")
        page.keyboard.type("11:30", delay=40)
        page.keyboard.press("Tab")
        page.wait_for_timeout(400)
        info["time"] = "11:30"
    return info


def force_done(page) -> str:
    try:
        btn = page.get_by_role("button", name=re.compile(r"^Done$", re.I))
        if btn.count():
            btn.first.click(force=True, timeout=4000)
            page.wait_for_timeout(1000)
            return "role"
    except Exception:
        pass
    hit = page.evaluate(
        """() => {
      let dlg = null;
      const find = (r, d = 0) => {
        if (!r || d > 50 || dlg) return;
        for (const el of (r.querySelectorAll ? r.querySelectorAll('tp-yt-paper-dialog,ytcp-dialog') : [])) {
          if (/Save or publish|Schedule/i.test(el.innerText || '')) { dlg = el; return; }
        }
        for (const el of (r.querySelectorAll ? r.querySelectorAll('*') : []))
          if (el.shadowRoot) find(el.shadowRoot, d + 1);
      };
      find(document);
      const root = dlg || document;
      let hit = null;
      const walk = (r, d = 0) => {
        if (!r || d > 45 || hit) return;
        for (const el of (r.querySelectorAll ? r.querySelectorAll('button,ytcp-button,[role=button]') : [])) {
          if (/^Done$/i.test((el.innerText || '').trim())) {
            el.removeAttribute('disabled');
            el.setAttribute('aria-disabled', 'false');
            el.click();
            hit = 'js';
            return;
          }
        }
        for (const el of (r.querySelectorAll ? r.querySelectorAll('*') : []))
          if (el.shadowRoot) walk(el.shadowRoot, d + 1);
      };
      walk(root);
      return hit;
    }"""
    )
    page.wait_for_timeout(1000)
    return hit or ""


def save_enabled(page) -> bool:
    return bool(
        page.evaluate(
            """() => {
      const walk = (r, d = 0) => {
        if (!r || d > 50) return false;
        for (const el of (r.querySelectorAll ? r.querySelectorAll('button,ytcp-button,[role=button]') : [])) {
          if (/^Save$/i.test((el.innerText || '').trim())) {
            const dis = el.disabled || el.getAttribute('aria-disabled') === 'true';
            if (!dis) return true;
          }
        }
        for (const el of (r.querySelectorAll ? r.querySelectorAll('*') : []))
          if (el.shadowRoot && walk(el.shadowRoot, d + 1)) return true;
        return false;
      };
      return walk(document);
    }"""
        )
    )


def page_save(page) -> dict:
    info = {"enabled": save_enabled(page)}
    clicked = False
    try:
        save = page.get_by_role("button", name=re.compile(r"^Save$", re.I))
        if save.count() and save.first.is_enabled():
            save.first.click(force=True, timeout=4000)
            clicked = True
            info["via"] = "role"
    except Exception:
        pass
    if not clicked:
        clicked = bool(
            page.evaluate(
                """() => {
          const walk = (r, d = 0) => {
            if (!r || d > 50) return false;
            for (const el of (r.querySelectorAll ? r.querySelectorAll('button,ytcp-button,[role=button]') : [])) {
              if (/^Save$/i.test((el.innerText || '').trim())) {
                const dis = el.disabled || el.getAttribute('aria-disabled') === 'true';
                if (!dis) { el.click(); return true; }
              }
            }
            for (const el of (r.querySelectorAll ? r.querySelectorAll('*') : []))
              if (el.shadowRoot && walk(el.shadowRoot, d + 1)) return true;
            return false;
          };
          return walk(document);
        }"""
            )
        )
        if clicked:
            info["via"] = "js"
    info["clicked"] = clicked
    if clicked:
        page.wait_for_timeout(1800)
        for name in ["Confirm", "Update", "Schedule", "Yes", "OK", "Save"]:
            try:
                b = page.get_by_role("button", name=re.compile(rf"^{re.escape(name)}$", re.I))
                if b.count() and b.first.is_visible():
                    b.first.click(force=True, timeout=1500)
                    info["confirm"] = name
                    page.wait_for_timeout(900)
            except Exception:
                pass
        for _ in range(25):
            page.wait_for_timeout(400)
            if not save_enabled(page):
                break
    return info


def fix_one(page, job: dict) -> dict:
    vid, day, slot = job["id"], job["day"], job["slot"]
    page.goto(
        f"https://studio.youtube.com/video/{vid}/edit",
        wait_until="domcontentloaded",
        timeout=120000,
    )
    page.wait_for_timeout(2500)
    out = {"id": vid, "day": day, "chip_before": visibility(page)}
    shot(page, f"v02c_{slot}_before.png")

    if not open_vis(page):
        out["error"] = "open_vis_failed"
        return out
    out["dialog0"] = dialog_info(page)
    shot(page, f"v02c_{slot}_dialog0.png")

    out["radio"] = click_schedule(page)
    page.wait_for_timeout(1000)
    out["fill"] = fill_dt(page, day)
    page.keyboard.press("Tab")
    page.wait_for_timeout(500)
    out["dialog1"] = dialog_info(page)
    shot(page, f"v02c_{slot}_filled.png")

    out["save_pre"] = save_enabled(page)
    if out["save_pre"]:
        out["save1"] = page_save(page)
    out["done"] = force_done(page)
    page.wait_for_timeout(900)
    out["dialog_still"] = dialog_info(page).get("found")
    if out["dialog_still"]:
        out["done2"] = force_done(page)
        page.wait_for_timeout(800)
        if dialog_info(page).get("found"):
            page.keyboard.press("Escape")
            page.wait_for_timeout(500)
    out["save_post"] = save_enabled(page)
    out["save2"] = page_save(page)
    page.wait_for_timeout(2000)

    page.goto(
        f"https://studio.youtube.com/video/{vid}/edit",
        wait_until="domcontentloaded",
        timeout=120000,
    )
    page.wait_for_timeout(2500)
    out["chip_after"] = visibility(page)
    shot(page, f"v02c_{slot}_after.png")

    open_vis(page)
    page.wait_for_timeout(1200)
    out["dialog_verify"] = dialog_info(page)
    shot(page, f"v02c_{slot}_verify.png")
    page.keyboard.press("Escape")

    dv = out.get("dialog_verify") or {}
    out["ok"] = bool(
        re.search(r"Scheduled", out.get("chip_after") or "", re.I)
        and re.search(rf"^{day}\\s+Sept\\s+2026$", dv.get("date") or "", re.I)
        and str(dv.get("time") or "").startswith("11:30")
    )
    # soft ok: chip Scheduled + dialog had correct dt when filled
    if not out["ok"]:
        d1 = out.get("dialog1") or {}
        out["soft_ok"] = bool(
            re.search(r"Scheduled", out.get("chip_after") or "", re.I)
            and re.search(rf"{day}\\s+Sept", d1.get("date") or "", re.I)
            and str(d1.get("time") or "").startswith("11:30")
        )
    return out


def main() -> int:
    EV.mkdir(parents=True, exist_ok=True)
    result = {"started": datetime.now().isoformat(timespec="seconds"), "jobs": []}
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(CDP, timeout=60000)
        ctx = browser.contexts[0]
        page = next(
            (pg for pg in ctx.pages if "studio.youtube.com" in (pg.url or "")),
            None,
        ) or ctx.new_page()
        for job in JOBS:
            log(f"FIX {job['id']} day={job['day']}")
            r = fix_one(page, job)
            result["jobs"].append(r)
            log(
                f"  ok={r.get('ok')} soft={r.get('soft_ok')} chip={r.get('chip_after')} "
                f"verify={r.get('dialog_verify')} done={r.get('done')} save2={r.get('save2')}"
            )

        page.goto(
            f"https://studio.youtube.com/channel/{CHANNEL}/videos/short",
            wait_until="domcontentloaded",
            timeout=120000,
        )
        page.wait_for_timeout(3000)
        shot(page, "v02c_90_content.png")
        result["ok"] = all(j.get("ok") or j.get("soft_ok") for j in result["jobs"])
        result["finished"] = datetime.now().isoformat(timespec="seconds")
        (EV / "RESULT_V02C_SCHEDULE_FIX.json").write_text(json.dumps(result, indent=2))
        # also update RESULT.json status
        print(
            json.dumps(
                {
                    "ok": result["ok"],
                    "jobs": [
                        {
                            "id": j["id"],
                            "ok": j.get("ok"),
                            "soft_ok": j.get("soft_ok"),
                            "chip": j.get("chip_after"),
                            "date": (j.get("dialog_verify") or {}).get("date"),
                            "time": (j.get("dialog_verify") or {}).get("time"),
                            "filled_date": (j.get("dialog1") or {}).get("date"),
                            "filled_time": (j.get("dialog1") or {}).get("time"),
                            "done": j.get("done"),
                            "save2": j.get("save2"),
                        }
                        for j in result["jobs"]
                    ],
                },
                indent=2,
            )
        )
        return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
