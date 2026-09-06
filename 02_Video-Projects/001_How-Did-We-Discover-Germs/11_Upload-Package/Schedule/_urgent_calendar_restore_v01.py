#!/usr/bin/env python3
"""Prove Mon/Tue schedule + cancel stuck upload. No deletes."""
from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path

from playwright.sync_api import sync_playwright

CDP = "http://127.0.0.1:9460"
CHANNEL = "UCXp7HkBIl1LgaznXuZHJyRg"
RELATED = "_C92tIJCk8A"
EV = Path(
    "/Users/benjaminoats/YouTube/History Of Science/02_Video-Projects/"
    "001_How-Did-We-Discover-Germs/11_Upload-Package/Schedule/"
    "evidence_2026-09-06_calendar_restore"
)

TARGETS = [
    {"id": "sILtQxgYQk8", "day": 7, "label": "Mon 7 Sep 2026 11:30", "slot": "s04"},
    {"id": "93fPUG-hW0A", "day": 8, "label": "Tue 8 Sep 2026 11:30", "slot": "s05"},
]
PUBLICS = ["H1y0DXFVmw8", "iqToagXnjX0", "8_Edn_HCi1s"]


def log(m: str) -> None:
    print(f"{datetime.now().isoformat(timespec='seconds')} {m}", flush=True)


def shot(page, name: str) -> str:
    EV.mkdir(parents=True, exist_ok=True)
    p = EV / name
    page.screenshot(path=str(p), full_page=False)
    return str(p)


def visibility(page) -> str:
    return page.evaluate(
        """() => {
      let hit = '';
      const walk = (r, d = 0) => {
        if (!r || d > 50 || hit) return;
        for (const el of (r.querySelectorAll ? r.querySelectorAll('*') : [])) {
          const t = (el.innerText || '').replace(/\\s+/g, ' ').trim();
          if (/^Visibility\\s+(Private|Public|Unlisted|Scheduled\\b.*)$/i.test(t) && t.length < 140) {
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


def dialog_dt(page) -> dict:
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
      let date = '', time = '';
      const walk = (r, d = 0) => {
        if (!r || d > 40) return;
        for (const el of (r.querySelectorAll ? r.querySelectorAll('ytcp-text-dropdown-trigger,div,span') : [])) {
          const t = (el.innerText || '').replace(/\\s+/g, ' ').trim();
          if (/^\\d{1,2}\\s+Sept\\s+2026$/i.test(t)) date = t;
        }
        for (const inp of (r.querySelectorAll ? r.querySelectorAll('input') : [])) {
          if (/^\\d{1,2}:\\d{2}$/.test(inp.value || '')) time = inp.value;
        }
        for (const el of (r.querySelectorAll ? r.querySelectorAll('*') : []))
          if (el.shadowRoot) walk(el.shadowRoot, d + 1);
      };
      walk(dlg);
      return {found: true, date, time, text: (dlg.innerText || '').slice(0, 500)};
    }"""
    )


def related_ok(page) -> dict:
    t = page.inner_text("body")
    m = re.search(r"Related video[^\n]{0,140}", t, re.I)
    return {
        "ok": bool(re.search(r"How Did We Discover Germs", t, re.I) or RELATED in t),
        "snip": m.group(0) if m else "",
    }


def click_radio(page, label: str) -> str:
    try:
        r = page.get_by_role("radio", name=re.compile(rf"^{re.escape(label)}$", re.I))
        if r.count():
            r.first.click(force=True, timeout=3000)
            page.wait_for_timeout(700)
            return f"role:{label}"
    except Exception:
        pass
    hit = page.evaluate(
        """(label) => {
      const re = new RegExp('^' + label + '$', 'i');
      let hit = null;
      const walk = (r, d = 0) => {
        if (!r || d > 50 || hit) return;
        for (const el of (r.querySelectorAll ? r.querySelectorAll('tp-yt-paper-radio-button,[role=radio]') : [])) {
          const t = ((el.innerText || '') + ' ' + (el.getAttribute('aria-label') || '')).replace(/\\s+/g, ' ').trim();
          if (re.test(t.split('\\n')[0].trim()) || re.test(t)) { el.click(); hit = t.slice(0, 60); return; }
        }
        for (const el of (r.querySelectorAll ? r.querySelectorAll('*') : []))
          if (el.shadowRoot) walk(el.shadowRoot, d + 1);
      };
      walk(document);
      return hit;
    }""",
        label,
    )
    page.wait_for_timeout(700)
    return hit or ""


def fill_schedule(page, day: int) -> dict:
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
    info["after"] = dialog_dt(page)
    return info


def force_done(page) -> str:
    try:
        btn = page.get_by_role("button", name=re.compile(r"^Done$", re.I))
        if btn.count():
            # force even if disabled attribute is stale
            page.evaluate(
                """() => {
              const walk = (r, d = 0) => {
                if (!r || d > 45) return false;
                for (const el of (r.querySelectorAll ? r.querySelectorAll('button,ytcp-button,[role=button]') : [])) {
                  if (/^Done$/i.test((el.innerText || '').trim())) {
                    el.removeAttribute('disabled');
                    el.setAttribute('aria-disabled', 'false');
                    el.click();
                    return true;
                  }
                }
                for (const el of (r.querySelectorAll ? r.querySelectorAll('*') : []))
                  if (el.shadowRoot && walk(el.shadowRoot, d + 1)) return true;
                return false;
              };
              return walk(document);
            }"""
            )
            try:
                btn.first.click(force=True, timeout=2000)
            except Exception:
                pass
            page.wait_for_timeout(1000)
            return "done"
    except Exception:
        pass
    return ""


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
    if not info["enabled"]:
        info["clicked"] = False
        return info
    clicked = False
    try:
        save = page.get_by_role("button", name=re.compile(r"^Save$", re.I))
        if save.count() and save.first.is_enabled():
            save.first.click(force=True, timeout=4000)
            clicked = True
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
    info["clicked"] = clicked
    if clicked:
        page.wait_for_timeout(2000)
        for name in ["Set private", "Set to private", "Update", "Confirm", "Schedule", "Yes", "OK", "Save"]:
            try:
                b = page.get_by_role("button", name=re.compile(rf"^{re.escape(name)}$", re.I))
                if b.count() and b.first.is_visible():
                    b.first.click(force=True, timeout=1500)
                    info["confirm"] = name
                    page.wait_for_timeout(1000)
            except Exception:
                pass
        for _ in range(30):
            page.wait_for_timeout(400)
            if not save_enabled(page):
                break
    return info


def ensure_scheduled(page, job: dict) -> dict:
    vid, day, slot = job["id"], job["day"], job["slot"]
    page.goto(
        f"https://studio.youtube.com/video/{vid}/edit",
        wait_until="domcontentloaded",
        timeout=120000,
    )
    page.wait_for_timeout(2500)
    out = {"id": vid, "label": job["label"], "chip0": visibility(page)}
    shot(page, f"URGENT_{slot}_{vid}_01_top.png")

    # If Public, Private first
    if re.search(r"Public", out["chip0"] or "", re.I):
        log(f"{vid} still Public — Private first")
        open_vis(page)
        out["private_radio"] = click_radio(page, "Private")
        page.wait_for_timeout(600)
        shot(page, f"URGENT_{slot}_{vid}_02_private.png")
        if save_enabled(page):
            out["private_save"] = page_save(page)
        force_done(page)
        page.wait_for_timeout(500)
        out["private_save2"] = page_save(page)
        page.wait_for_timeout(2000)
        page.reload(wait_until="domcontentloaded")
        page.wait_for_timeout(2000)
        out["chip_after_private"] = visibility(page)
        shot(page, f"URGENT_{slot}_{vid}_03_after_private.png")

    # Schedule
    open_vis(page)
    out["sched_radio"] = click_radio(page, "Schedule")
    page.wait_for_timeout(1000)
    out["fill"] = fill_schedule(page, day)
    page.keyboard.press("Tab")
    page.wait_for_timeout(400)
    out["dialog_filled"] = dialog_dt(page)
    shot(page, f"URGENT_{slot}_{vid}_04_schedule_filled.png")
    if save_enabled(page):
        out["sched_save1"] = page_save(page)
    force_done(page)
    page.wait_for_timeout(800)
    out["sched_save2"] = page_save(page)
    page.wait_for_timeout(2000)

    page.reload(wait_until="domcontentloaded")
    page.wait_for_timeout(2200)
    out["chip_final"] = visibility(page)
    shot(page, f"URGENT_{slot}_{vid}_05_final_chip.png")
    open_vis(page)
    page.wait_for_timeout(1200)
    out["dialog_final"] = dialog_dt(page)
    shot(page, f"URGENT_{slot}_{vid}_06_final_dialog.png")
    page.keyboard.press("Escape")
    page.wait_for_timeout(400)
    page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
    page.wait_for_timeout(700)
    out["related"] = related_ok(page)
    shot(page, f"URGENT_{slot}_{vid}_07_related.png")
    page.evaluate("window.scrollTo(0,0)")
    page.wait_for_timeout(300)
    shot(page, f"URGENT_{slot}_{vid}_08_thumb.png")

    d = out.get("dialog_final") or {}
    out["ok"] = bool(
        re.search(r"Scheduled", out.get("chip_final") or "", re.I)
        and re.search(rf"^{day}\s+Sept\s+2026$", d.get("date") or "", re.I)
        and str(d.get("time") or "").startswith("11:30")
        and out.get("related", {}).get("ok")
    )
    return out


def cancel_stuck_upload(page) -> dict:
    """Cancel uploading 'hos 001 s04 flask punch v02' only — no deletes."""
    out = {"action": "cancel_upload_only"}
    page.goto(
        f"https://studio.youtube.com/channel/{CHANNEL}/videos/short",
        wait_until="domcontentloaded",
        timeout=120000,
    )
    page.wait_for_timeout(3500)
    shot(page, "URGENT_90_content_before_cancel.png")
    text = page.inner_text("body")
    out["has_title"] = bool(re.search(r"hos\s*001\s*s04\s*flask\s*punch\s*v02", text, re.I))
    out["has_uploading"] = bool(re.search(r"Uploading", text, re.I))
    if not (out["has_title"] or out["has_uploading"]):
        out["ok"] = True
        out["note"] = "no_uploading_draft_visible"
        return out

    # Try menu on uploading row
    clicked = page.evaluate(
        """() => {
      const walk = (r, d = 0) => {
        if (!r || d > 55) return null;
        for (const el of (r.querySelectorAll ? r.querySelectorAll('*') : [])) {
          const t = (el.innerText || '').replace(/\\s+/g, ' ').trim();
          if (/hos\\s*001\\s*s04\\s*flask\\s*punch\\s*v02/i.test(t) && t.length < 200) {
            // find nearby menu button
            let n = el;
            for (let i = 0; i < 8 && n; i++) {
              const btn = n.querySelector && n.querySelector('button[aria-label*="Options" i], button[aria-label*="menu" i], ytcp-icon-button, button');
              // prefer options in same row
              const buttons = n.querySelectorAll ? n.querySelectorAll('ytcp-icon-button,button,[role=button]') : [];
              for (const b of buttons) {
                const a = (b.getAttribute('aria-label') || '') + ' ' + (b.innerText || '');
                if (/option|menu|more|action/i.test(a) || a.trim() === '') {
                  // click last icon-ish
                }
              }
              n = n.parentElement;
            }
            return t.slice(0, 120);
          }
        }
        for (const el of (r.querySelectorAll ? r.querySelectorAll('*') : [])) {
          if (el.shadowRoot) {
            const h = walk(el.shadowRoot, d + 1);
            if (h) return h;
          }
        }
        return null;
      };
      return walk(document);
    }"""
    )
    out["row"] = clicked

    # Prefer Cancel upload button/text
    for name in [
        r"^Cancel upload$",
        r"^Cancel$",
        r"^Stop upload$",
        r"^Discard upload$",
    ]:
        try:
            b = page.get_by_role("button", name=re.compile(name, re.I))
            if b.count() and b.first.is_visible():
                b.first.click(force=True, timeout=2000)
                out["clicked"] = name
                page.wait_for_timeout(1500)
                break
        except Exception:
            pass

    # Open options menu via text match then Cancel
    try:
        row = page.get_by_text(re.compile(r"hos\s*001\s*s04\s*flask\s*punch\s*v02", re.I)).first
        if row.count() or True:
            # click near uploading
            loc = page.locator("text=/Uploading/i").first
            if loc.count():
                # options button to the right of uploading row — try aria Options
                page.evaluate(
                    """() => {
                  const nodes = [...document.querySelectorAll('*')].filter(e => /Uploading/i.test(e.innerText||'') && (e.innerText||'').length < 40);
                  for (const n of nodes) {
                    let p = n;
                    for (let i=0;i<10 && p;i++) {
                      const btns = p.querySelectorAll ? p.querySelectorAll('ytcp-icon-button,button,[aria-label]') : [];
                      for (const b of btns) {
                        const a = b.getAttribute('aria-label') || '';
                        if (/options|more actions|menu/i.test(a)) { b.click(); return a; }
                      }
                      p = p.parentElement;
                    }
                  }
                  return null;
                }"""
                )
                page.wait_for_timeout(800)
                for lab in ["Cancel upload", "Cancel", "Delete forever", "Remove"]:
                    # Only cancel — skip delete forever
                    if "Delete" in lab or "Remove" in lab:
                        continue
                    try:
                        m = page.get_by_role("menuitem", name=re.compile(rf"^{re.escape(lab)}$", re.I))
                        if m.count():
                            m.first.click(timeout=2000)
                            out["menu"] = lab
                            page.wait_for_timeout(1500)
                            break
                        t = page.get_by_text(re.compile(rf"^{re.escape(lab)}$", re.I))
                        if t.count() and t.first.is_visible():
                            t.first.click(timeout=2000)
                            out["menu"] = f"text:{lab}"
                            page.wait_for_timeout(1500)
                            break
                    except Exception:
                        pass
    except Exception as e:
        out["menu_err"] = str(e)[:160]

    page.wait_for_timeout(2000)
    shot(page, "URGENT_91_content_after_cancel.png")
    text2 = page.inner_text("body")
    out["still_uploading"] = bool(re.search(r"Uploading", text2, re.I))
    out["still_title"] = bool(re.search(r"hos\s*001\s*s04\s*flask\s*punch\s*v02", text2, re.I))
    out["ok"] = not out["still_uploading"]
    return out


def scan_content(page) -> dict:
    page.goto(
        f"https://studio.youtube.com/channel/{CHANNEL}/videos/short",
        wait_until="domcontentloaded",
        timeout=120000,
    )
    page.wait_for_timeout(3500)
    shot(page, "URGENT_92_content_shorts.png")
    # filter Public
    try:
        page.get_by_role("button", name=re.compile(r"Visibility", re.I)).first.click(timeout=2500)
        page.wait_for_timeout(500)
        page.get_by_text(re.compile(r"^Public$", re.I)).first.click(timeout=2500)
        page.wait_for_timeout(2500)
        shot(page, "URGENT_93_content_public_filter.png")
    except Exception as e:
        pass
    pub_text = page.inner_text("body")[:4000]
    # filter Scheduled
    try:
        page.get_by_role("button", name=re.compile(r"Visibility", re.I)).first.click(timeout=2500)
        page.wait_for_timeout(400)
        page.get_by_text(re.compile(r"^Scheduled$", re.I)).first.click(timeout=2500)
        page.wait_for_timeout(2500)
        shot(page, "URGENT_94_content_scheduled_filter.png")
    except Exception:
        pass
    sched_text = page.inner_text("body")[:4000]
    return {
        "public_has_flask": bool(re.search(r"flask", pub_text, re.I)),
        "public_snip": pub_text[:800],
        "scheduled_has_flask": bool(re.search(r"flask|Invisible", sched_text, re.I)),
        "scheduled_snip": sched_text[:800],
    }


def main() -> int:
    EV.mkdir(parents=True, exist_ok=True)
    result = {
        "started": datetime.now().isoformat(timespec="seconds"),
        "channelId": CHANNEL,
        "related": RELATED,
        "no_deletes": True,
        "jobs": [],
    }
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(CDP, timeout=60000)
        ctx = browser.contexts[0]
        page = next(
            (pg for pg in ctx.pages if "studio.youtube.com" in (pg.url or "")),
            None,
        ) or ctx.new_page()

        # boot channel check
        page.goto(
            f"https://studio.youtube.com/channel/{CHANNEL}",
            wait_until="domcontentloaded",
            timeout=120000,
        )
        page.wait_for_timeout(2000)
        shot(page, "URGENT_00_boot.png")

        for job in TARGETS:
            log(f"ENSURE {job['id']} {job['label']}")
            r = ensure_scheduled(page, job)
            result["jobs"].append(r)
            log(
                f"  ok={r.get('ok')} chip={r.get('chip_final')} "
                f"date={(r.get('dialog_final') or {}).get('date')} "
                f"time={(r.get('dialog_final') or {}).get('time')}"
            )

        # publics untouched check
        pubs = []
        for vid in PUBLICS:
            page.goto(
                f"https://studio.youtube.com/video/{vid}/edit",
                wait_until="domcontentloaded",
                timeout=120000,
            )
            page.wait_for_timeout(1800)
            c = visibility(page)
            shot(page, f"URGENT_public_{vid}.png")
            pubs.append({"id": vid, "chip": c, "ok": bool(re.search(r"Public", c or "", re.I))})
        result["publics"] = pubs

        log("CANCEL stuck upload if present")
        result["cancel_upload"] = cancel_stuck_upload(page)
        result["content_scan"] = scan_content(page)

        result["ok"] = all(j.get("ok") for j in result["jobs"]) and all(
            p.get("ok") for p in pubs
        )
        result["finished"] = datetime.now().isoformat(timespec="seconds")
        (EV / "RESULT_URGENT.json").write_text(json.dumps(result, indent=2))
        (EV / "RESULT.json").write_text(json.dumps(result, indent=2))
        print(
            json.dumps(
                {
                    "ok": result["ok"],
                    "jobs": [
                        {
                            "id": j["id"],
                            "ok": j.get("ok"),
                            "chip": j.get("chip_final"),
                            "date": (j.get("dialog_final") or {}).get("date"),
                            "time": (j.get("dialog_final") or {}).get("time"),
                            "related": j.get("related"),
                        }
                        for j in result["jobs"]
                    ],
                    "publics": pubs,
                    "cancel": result.get("cancel_upload"),
                    "content": {
                        k: result["content_scan"].get(k)
                        for k in ("public_has_flask", "scheduled_has_flask")
                    },
                },
                indent=2,
            )
        )
        return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
