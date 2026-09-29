#!/usr/bin/env python3
"""URGENT Ben 20:00 — Made for Kids audit + fix 004 Audience NO.

1) Channel check @HistoryOfScienceYT
2) GHZDsiH7L7A Audience → No, not Made for Kids (+ screenshot)
3) Studio Settings → Channel → Advanced: channel audience default (STOP if Yes)
4) Audience on 001/002/003 longs + their Shorts
CDP :9460 only. Never change channel settings.
"""
from __future__ import annotations

import json
import re
import urllib.request
from datetime import datetime
from pathlib import Path

from playwright.sync_api import sync_playwright

PORT = 9460
CHANNEL = "UCXp7HkBIl1LgaznXuZHJyRg"
HANDLE = "@HistoryOfScienceYT"
VID_004 = "GHZDsiH7L7A"
VIDEOS = {
    "004_long": VID_004,
    "001_long": "_C92tIJCk8A",
    "001_shorts": ["8uBR-9oxeWs", "YX2UR1u-JCQ", "Fnb3p81u-wY", "vpuRgKXtFlY", "Lcmh5y2KMQM"],
    "002_long": "AL_-qlWko_g",
    "002_shorts": ["uU12JA5rMWg", "nFQRWmpulTQ", "CnHwX1L9XHg", "nba0-f7PPeU", "LanTHJckYx8"],
    "003_long": "frP_YrNShsU",
    "003_shorts": ["oowAOWTBoq0", "xvanpsLeADE", "zI_eD3vFWmE"],
}
PROJ = Path(__file__).resolve().parents[2]
EV = PROJ / "11_Upload-Package/Schedule/evidence_2026-09-29_studio"
ART = Path.home() / ".local/share/cursor-mac-mini-hos-worker/artifacts/hos004_studio_phone_uat"


def log(m: str) -> None:
    EV.mkdir(parents=True, exist_ok=True)
    ART.mkdir(parents=True, exist_ok=True)
    line = f"{datetime.now().isoformat(timespec='seconds')} {m}"
    print(line, flush=True)
    with (EV / "urgent_kids_v01.log").open("a") as f:
        f.write(line + "\n")


def dump(n: str, o) -> None:
    text = json.dumps(o, indent=2) + "\n"
    (EV / n).write_text(text)
    (ART / n).write_text(text)


def shot(page, n: str) -> Path:
    p = EV / n
    page.screenshot(path=str(p), full_page=False)
    (ART / n).write_bytes(p.read_bytes())
    return p


def dismiss(page) -> None:
    for _ in range(3):
        page.keyboard.press("Escape")
        page.wait_for_timeout(100)
        try:
            page.get_by_role(
                "button",
                name=re.compile(r"^(OK, got it|Got it|Close|Dismiss|Not now|Continue)$", re.I),
            ).first.click(timeout=300)
        except Exception:
            pass


def channel_ok(page) -> dict:
    page.goto(
        f"https://studio.youtube.com/channel/{CHANNEL}/videos/upload",
        wait_until="domcontentloaded",
        timeout=90000,
    )
    page.wait_for_timeout(4000)
    dismiss(page)
    shot(page, "urgent_kids_00_channel.png")
    t = page.inner_text("body")
    return {
        "ok": HANDLE in t or "History of Science" in t,
        "has_orbit": bool(re.search(r"Orbit With Ben|OpptiAI", t, re.I)),
        "snip": t[:400],
    }


def read_audience(page, video_id: str, tag: str) -> dict:
    info = {"videoId": video_id, "tag": tag}
    page.goto(
        f"https://studio.youtube.com/video/{video_id}/edit",
        wait_until="domcontentloaded",
        timeout=90000,
    )
    page.wait_for_timeout(4500)
    dismiss(page)
    # Scroll to Audience
    for _ in range(28):
        body = page.inner_text("body")
        if re.search(r"Audience|Made for Kids", body, re.I):
            break
        page.evaluate(
            """() => {
              const walk=(r,d=0)=>{
                if(!r||d>55)return false;
                for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
                  if ((el.innerText||'').trim()==='Show more') { el.click(); return true; }
                }
                for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
                  if (el.shadowRoot && walk(el.shadowRoot,d+1)) return true;
                }
                return false;
              }; return walk(document);
            }"""
        )
        page.mouse.wheel(0, 600)
        page.wait_for_timeout(120)
    page.evaluate(
        """() => {
          const walk=(r,d=0)=>{
            if(!r||d>55)return false;
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
              const t=(el.innerText||'').trim();
              if (/^Audience$/i.test(t) || /Made for Kids/i.test(t)) {
                el.scrollIntoView({block:'center'}); return t;
              }
              if (el.shadowRoot && walk(el.shadowRoot,d+1)) return true;
            }
            return false;
          }; return walk(document);
        }"""
    )
    page.wait_for_timeout(400)
    shot(page, f"urgent_kids_{tag}.png")
    body = page.inner_text("body")
    info["set_to_not"] = bool(re.search(r"set to not ['\"]?Made for Kids", body, re.I))
    info["set_to_yes"] = bool(re.search(r"set to ['\"]?Made for Kids['\"]?(?!.*not)", body, re.I)) or bool(
        re.search(r"This video is set to 'Made for Kids'", body, re.I)
    )
    # Radio states
    radios = page.evaluate(
        """() => {
          let audY=null;
          const find=(r,d=0)=>{
            if(!r||d>55)return;
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
              if (/^Audience$/i.test((el.innerText||'').trim()) || /Made for Kids/i.test((el.innerText||'').trim()) && (el.innerText||'').trim().length<40) {
                const rect=el.getBoundingClientRect(); if(rect.y>80) audY=audY??rect.y;
              }
              if (el.shadowRoot) find(el.shadowRoot,d+1);
            }
          }; find(document);
          const out=[];
          const walk=(r,d=0)=>{
            if(!r||d>55)return;
            for (const el of (r.querySelectorAll?r.querySelectorAll('[role=radio],input[type=radio]'):[])) {
              const t=((el.getAttribute('aria-label')||'')+' '+(el.innerText||'')).trim();
              const rect=el.getBoundingClientRect();
              if (audY!=null && rect.y>audY-20 && rect.y<audY+500) {
                out.push({t:t.slice(0,80), checked: el.getAttribute('aria-checked')==='true' || el.checked===true, y:rect.y});
              }
            }
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
              if (el.shadowRoot) walk(el.shadowRoot,d+1);
            }
          }; walk(document);
          return {audY, radios: out};
        }"""
    )
    info["radios"] = radios
    no_checked = False
    yes_checked = False
    for r in radios.get("radios") or []:
        t = r.get("t") or ""
        if r.get("checked") and re.search(r"No.*not.*Made for Kids|not.?Made for Kids", t, re.I):
            no_checked = True
        if r.get("checked") and re.search(r"Yes.*Made for Kids|^Yes,", t, re.I) and not re.search(r"not", t, re.I):
            yes_checked = True
    info["no_checked"] = no_checked or info["set_to_not"]
    info["yes_checked"] = yes_checked or (info["set_to_yes"] and not info["set_to_not"])
    info["ok_not_kids"] = bool(info["no_checked"] and not info["yes_checked"])
    info["made_for_kids"] = bool(info["yes_checked"] and not info["no_checked"])
    return info


def set_not_kids(page, video_id: str) -> dict:
    info = {"videoId": video_id}
    page.goto(
        f"https://studio.youtube.com/video/{video_id}/edit",
        wait_until="domcontentloaded",
        timeout=90000,
    )
    page.wait_for_timeout(4500)
    dismiss(page)
    for _ in range(28):
        if re.search(r"Audience|Made for Kids", page.inner_text("body"), re.I):
            break
        page.evaluate(
            """() => {
              const walk=(r,d=0)=>{
                if(!r||d>55)return false;
                for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
                  if ((el.innerText||'').trim()==='Show more') { el.click(); return true; }
                }
                for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
                  if (el.shadowRoot && walk(el.shadowRoot,d+1)) return true;
                }
                return false;
              }; return walk(document);
            }"""
        )
        page.mouse.wheel(0, 600)
        page.wait_for_timeout(120)
    # Prefer role radio
    try:
        radio = page.get_by_role(
            "radio",
            name=re.compile(r"No,? it.?s not.?Made for Kids|Not made for kids", re.I),
        )
        if radio.count():
            radio.first.click(force=True, timeout=5000)
            info["via"] = "role_radio"
    except Exception as e:
        info["role_err"] = str(e)[:100]
    if not info.get("via"):
        hit = page.evaluate(
            """() => {
              const walk=(r,d=0)=>{
                if(!r||d>55)return false;
                for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
                  const t=(el.innerText||'').trim();
                  if (/No, it's not.?Made for Kids/i.test(t) && t.length<80) { el.click(); return t; }
                  if (el.shadowRoot) { const x=walk(el.shadowRoot,d+1); if(x) return x; }
                }
                return false;
              }; return walk(document);
            }"""
        )
        info["via"] = hit
    page.wait_for_timeout(600)
    try:
        btn = page.get_by_role("button", name=re.compile(r"^Save$", re.I))
        if btn.count() and btn.first.is_enabled():
            btn.first.click(force=True)
            info["saved"] = True
            page.wait_for_timeout(4500)
        else:
            info["saved"] = False
    except Exception as e:
        info["saved"] = str(e)[:80]
    # Reload verify
    verified = read_audience(page, video_id, "004_after_fix")
    info["after"] = verified
    # Canonical Audience screenshot name for Ben/CoS
    src = EV / "urgent_kids_004_after_fix.png"
    if src.exists():
        (EV / "URGENT_audience_004_not_made_for_kids.png").write_bytes(src.read_bytes())
        (ART / "URGENT_audience_004_not_made_for_kids.png").write_bytes(src.read_bytes())
    return info


def channel_advanced_audience(page) -> dict:
    """Settings → Channel → Advanced settings. Do NOT change anything."""
    info = {}
    # Try direct advanced settings URL patterns used by Studio
    urls = [
        f"https://studio.youtube.com/channel/{CHANNEL}/editing/sections",
        f"https://studio.youtube.com/channel/{CHANNEL}/editing/details",
        f"https://studio.youtube.com/",
    ]
    page.goto(f"https://studio.youtube.com/channel/{CHANNEL}", wait_until="domcontentloaded", timeout=90000)
    page.wait_for_timeout(3500)
    dismiss(page)
    # Click Settings in left rail
    page.evaluate(
        """() => {
          const walk=(r,d=0)=>{
            if(!r||d>55)return false;
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
              if ((el.innerText||'').trim()==='Settings') { el.click(); return true; }
              if (el.shadowRoot && walk(el.shadowRoot,d+1)) return true;
            }
            return false;
          }; return walk(document);
        }"""
    )
    page.wait_for_timeout(2500)
    shot(page, "urgent_kids_settings.png")
    # Channel tab
    page.evaluate(
        """() => {
          const walk=(r,d=0)=>{
            if(!r||d>55)return false;
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
              const t=(el.innerText||'').trim();
              if (t==='Channel' && t.length<=10) { el.click(); return true; }
              if (el.shadowRoot && walk(el.shadowRoot,d+1)) return true;
            }
            return false;
          }; return walk(document);
        }"""
    )
    page.wait_for_timeout(2000)
    shot(page, "urgent_kids_settings_channel.png")
    # Advanced settings
    page.evaluate(
        """() => {
          const walk=(r,d=0)=>{
            if(!r||d>55)return false;
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
              const t=(el.innerText||'').trim();
              if (/^Advanced settings$/i.test(t) || /^Advanced$/i.test(t)) { el.click(); return t; }
              if (el.shadowRoot && walk(el.shadowRoot,d+1)) return true;
            }
            return false;
          }; return walk(document);
        }"""
    )
    page.wait_for_timeout(2500)
    # Scroll for audience / made for kids
    for _ in range(15):
        body = page.inner_text("body")
        if re.search(r"Audience|Made for Kids|made for kids", body, re.I):
            break
        page.mouse.wheel(0, 500)
        page.wait_for_timeout(120)
    page.evaluate(
        """() => {
          const walk=(r,d=0)=>{
            if(!r||d>55)return false;
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
              const t=(el.innerText||'').trim();
              if (/Audience|Made for Kids/i.test(t) && t.length<60) {
                el.scrollIntoView({block:'center'}); return t;
              }
              if (el.shadowRoot && walk(el.shadowRoot,d+1)) return true;
            }
            return false;
          }; return walk(document);
        }"""
    )
    page.wait_for_timeout(500)
    shot(page, "urgent_kids_channel_advanced_audience.png")
    (EV / "URGENT_channel_advanced_audience.png").write_bytes(
        (EV / "urgent_kids_channel_advanced_audience.png").read_bytes()
    )
    (ART / "URGENT_channel_advanced_audience.png").write_bytes(
        (EV / "urgent_kids_channel_advanced_audience.png").read_bytes()
    )
    body = page.inner_text("body")
    info["snip"] = body[:2500]
    info["has_audience_section"] = bool(re.search(r"Audience|Made for Kids", body, re.I))
    # Channel default radios
    radios = page.evaluate(
        """() => {
          const out=[];
          const walk=(r,d=0)=>{
            if(!r||d>55)return;
            for (const el of (r.querySelectorAll?r.querySelectorAll('[role=radio],input[type=radio]'):[])) {
              const t=((el.getAttribute('aria-label')||'')+' '+(el.innerText||'')).trim();
              if (/Made for Kids|kids|Audience/i.test(t) || t==='Yes' || t==='No') {
                out.push({
                  t:t.slice(0,100),
                  checked: el.getAttribute('aria-checked')==='true' || el.checked===true,
                  y: el.getBoundingClientRect().y
                });
              }
            }
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
              if (el.shadowRoot) walk(el.shadowRoot,d+1);
            }
          }; walk(document);
          return out;
        }"""
    )
    info["radios"] = radios
    # Interpret
    default_yes = False
    default_no = False
    for r in radios:
        t = r.get("t") or ""
        if not r.get("checked"):
            continue
        if re.search(r"Yes.*Made for Kids|made for kids", t, re.I) and not re.search(r"not", t, re.I):
            default_yes = True
        if re.search(r"No.*not.*Made for Kids|not made for kids|No,", t, re.I):
            default_no = True
    # Also text banners
    if re.search(r"set to ['\"]?Made for Kids", body, re.I) and not re.search(r"set to not", body, re.I):
        default_yes = True
    if re.search(r"set to not ['\"]?Made for Kids", body, re.I):
        default_no = True
    info["channel_default_made_for_kids"] = default_yes and not default_no
    info["channel_default_not_for_kids"] = default_no and not default_yes
    info["stop_for_ben"] = bool(info["channel_default_made_for_kids"])
    info["note"] = (
        "STOP — channel default is Made for Kids; do not change without Ben"
        if info["stop_for_ben"]
        else "Channel default is not Made for Kids (or unclear — see screenshot/radios)"
    )
    return info


def main() -> None:
    EV.mkdir(parents=True, exist_ok=True)
    ART.mkdir(parents=True, exist_ok=True)
    (EV / "urgent_kids_v01.log").write_text("")
    urllib.request.urlopen(f"http://127.0.0.1:{PORT}/json/version", timeout=3)
    result = {
        "at": datetime.now().isoformat(timespec="seconds"),
        "channel": HANDLE,
        "channelId": CHANNEL,
        "urgent": "Ben 20:00 Made for Kids",
    }

    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{PORT}", timeout=30000)
        page = browser.contexts[0].pages[0] if browser.contexts[0].pages else browser.contexts[0].new_page()
        page.set_default_timeout(45000)
        try:
            page.set_viewport_size({"width": 1680, "height": 1100})
        except Exception:
            pass
        try:
            page.bring_to_front()
        except Exception:
            pass

        log("urgent channel check")
        result["channelCheck"] = channel_ok(page)
        if result["channelCheck"].get("has_orbit") or not result["channelCheck"].get("ok"):
            dump("URGENT_KIDS_AUDIT_V01.json", result)
            log("STOP wrong channel")
            print(json.dumps(result, indent=2))
            return

        log("urgent 004 audience before")
        result["004_before"] = read_audience(page, VID_004, "004_before")
        dump("URGENT_004_BEFORE.json", result["004_before"])

        if not result["004_before"].get("ok_not_kids"):
            log("urgent 004 SET not Made for Kids")
            result["004_fix"] = set_not_kids(page, VID_004)
        else:
            log("urgent 004 already not Made for Kids — screenshot")
            src = EV / "urgent_kids_004_before.png"
            (EV / "URGENT_audience_004_not_made_for_kids.png").write_bytes(src.read_bytes())
            (ART / "URGENT_audience_004_not_made_for_kids.png").write_bytes(src.read_bytes())
            result["004_fix"] = {"already_ok": True, "after": result["004_before"]}

        log("urgent channel advanced audience (read-only)")
        result["channelAdvanced"] = channel_advanced_audience(page)
        dump("URGENT_CHANNEL_ADVANCED.json", result["channelAdvanced"])

        if result["channelAdvanced"].get("stop_for_ben"):
            result["STOP"] = True
            result["STOP_REASON"] = "Channel Advanced default is Made for Kids — tell Ben, do not change"
            dump("URGENT_KIDS_AUDIT_V01.json", result)
            log("STOP channel default Made for Kids")
            print(json.dumps(result, indent=2))
            return

        # Audit 001/002/003 longs + shorts
        audits = {}
        made_for_kids_hits = []

        log("urgent audit 001 long")
        audits["001_long"] = read_audience(page, VIDEOS["001_long"], "001_long")
        for sid in VIDEOS["001_shorts"]:
            log(f"urgent audit 001 short {sid}")
            audits[f"001_short_{sid}"] = read_audience(page, sid, f"001_short_{sid}")
        log("urgent audit 002 long")
        audits["002_long"] = read_audience(page, VIDEOS["002_long"], "002_long")
        for sid in VIDEOS["002_shorts"]:
            log(f"urgent audit 002 short {sid}")
            audits[f"002_short_{sid}"] = read_audience(page, sid, f"002_short_{sid}")
        log("urgent audit 003 long")
        audits["003_long"] = read_audience(page, VIDEOS["003_long"], "003_long")
        for sid in VIDEOS["003_shorts"]:
            log(f"urgent audit 003 short {sid}")
            audits[f"003_short_{sid}"] = read_audience(page, sid, f"003_short_{sid}")

        for k, v in audits.items():
            if v.get("made_for_kids") or (v.get("yes_checked") and not v.get("no_checked")):
                made_for_kids_hits.append({"key": k, "videoId": v.get("videoId"), "detail": v})

        result["audits"] = {
            k: {
                "videoId": v.get("videoId"),
                "ok_not_kids": v.get("ok_not_kids"),
                "made_for_kids": v.get("made_for_kids"),
                "no_checked": v.get("no_checked"),
                "yes_checked": v.get("yes_checked"),
                "set_to_not": v.get("set_to_not"),
                "set_to_yes": v.get("set_to_yes"),
            }
            for k, v in audits.items()
        }
        result["made_for_kids_hits"] = made_for_kids_hits
        result["004_ok"] = bool(
            (result.get("004_fix") or {}).get("after", {}).get("ok_not_kids")
            or result["004_before"].get("ok_not_kids")
        )

    dump("URGENT_KIDS_AUDIT_V01.json", result)
    log(
        "DONE "
        + json.dumps(
            {
                "004_ok": result.get("004_ok"),
                "channel_stop": result.get("channelAdvanced", {}).get("stop_for_ben"),
                "hits": result.get("made_for_kids_hits"),
            },
            default=str,
        )[:1500]
    )
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
