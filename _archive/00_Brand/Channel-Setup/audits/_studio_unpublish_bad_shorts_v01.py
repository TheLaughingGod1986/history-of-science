#!/usr/bin/env python3
"""Unpublish bad Last Star dump Shorts + fix/unpublish off-cluster fillers (Studio CDP).

Orbit with Ben · channel UC_esArsDKd3GJvOkeO0DUog (@OrbitWithBen)

Actions (never delete):
  1. Set PRIVATE: KX-XU_AODoI, CkSECfUfH2Y (1 Sep dump — audit fail)
  2. Leave public: 9lLZMy8rBJo (only keeper from dump)
  3. Filler Related fix (Studio-only UI) — if still points at Last Star and
     cannot be retargeted, set PRIVATE:
       Q16DKNvq2OY — Earth, Seen From the Dark
       QptlHs1HuYI — The Galaxy Should Be Crowded — It's Silent (Fermi)

Related pill is **Studio-only** (ytcp-shorts-content-links-picker). There is no
YouTube Data API field for Shorts Related → parent long. This script attempts
Studio automation; on failure it documents the gap and unpublishes fillers.

Profiles tried in order (first existing wins):
  ~/.playwright-hos-flow-profile
  ~/code/youtube/.playwright-youtube-profile
  ~/.playwright-youtube-profile

Usage:
  python3 00_Brand/Channel-Setup/audits/_studio_unpublish_bad_shorts_v01.py
  python3 ... --dry-run          # list actions only
  python3 ... --profile PATH     # force one profile
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

from playwright.sync_api import sync_playwright

CHANNEL = "UC_esArsDKd3GJvOkeO0DUog"
LAST_STAR_ID = "REXYxuLOBoI"
LAST_STAR_TITLE = "What Happens When the Last Star Dies?"
FERMI_LONG_ID = "Mo93x0fxB1Q"
FERMI_LONG_TITLE = "Why Haven't We Found Aliens Yet? The Fermi Paradox Explained"

PROFILE_CANDIDATES = [
    Path.home() / ".playwright-hos-flow-profile",
    Path.home() / "code/youtube/.playwright-youtube-profile",
    Path.home() / ".playwright-youtube-profile",
]

HERE = Path(__file__).resolve().parent
OUT = HERE / "studio_unpublish_bad_shorts_v01_result.json"
AUDIT = HERE / "_studio_unpublish_bad_shorts_v01"

# (video_id, action, note)
UNPUBLISH_TARGETS = [
    ("KX-XU_AODoI", "private", "0 views · long-title VO open · audit FAIL"),
    ("CkSECfUfH2Y", "private", "eyeball-planet mute-test fail · audit FAIL"),
]

KEEP_PUBLIC = {"9lLZMy8rBJo"}

# Off-cluster fillers — Related must NOT be Last Star; unpublish if fix fails
FILLER_RELATED = {
    "QptlHs1HuYI": {
        "title_hint": "Galaxy Should Be Crowded",
        "long_id": FERMI_LONG_ID,
        "long_title": FERMI_LONG_TITLE,
        "unpublish_if_fail": True,
    },
    "Q16DKNvq2OY": {
        "title_hint": "Earth, Seen From the Dark",
        # Parent long unknown / off-cluster; do not leave Related → Last Star
        "long_id": None,
        "long_title": None,
        "unpublish_if_fail": True,
    },
}


def pick_profile(forced: str | None) -> Path | None:
    if forced:
        p = Path(forced).expanduser()
        return p if p.is_dir() else None
    for p in PROFILE_CANDIDATES:
        if p.is_dir():
            return p
    return None


def skip(page) -> None:
    try:
        page.get_by_role("link", name=re.compile(r"Skip", re.I)).click(timeout=1000)
    except Exception:
        pass


def dismiss(page) -> None:
    page.evaluate(
        "() => document.querySelectorAll('tp-yt-iron-overlay-backdrop').forEach(e => e.remove())"
    )
    for name in ("Got it", "Dismiss", "Close", "Not now"):
        try:
            b = page.get_by_role("button", name=name, exact=True)
            if b.count() and b.first.is_visible():
                b.first.click(force=True, timeout=600)
        except Exception:
            pass
    page.keyboard.press("Escape")
    page.wait_for_timeout(200)


def login_wall(page) -> bool:
    body = page.locator("body").inner_text()
    url = page.url or ""
    if "accounts.google.com" in url:
        return True
    if "Sign in" in body and ("Email or phone" in body or "Create account" in body):
        return True
    if "studio.youtube.com" not in url and "youtube.com" in url and "Sign in" in body:
        return True
    return False


def studio_edit_ready(page) -> bool:
    """True when the video edit page loaded with Studio chrome (not wrong account)."""
    if login_wall(page):
        return False
    url = page.url or ""
    if "/video/" not in url or "studio.youtube.com" not in url:
        return False
    body = page.locator("body").inner_text()
    if "You don't have permission" in body or "Content not found" in body:
        return False
    return page.locator("ytcp-video-metadata-visibility").count() > 0


def open_visibility(page) -> None:
    page.locator("ytcp-video-metadata-visibility").first.scroll_into_view_if_needed()
    page.wait_for_timeout(300)
    page.locator("ytcp-video-metadata-visibility").first.click(force=True)
    page.wait_for_timeout(1400)


def click_done(page) -> None:
    try:
        btn = page.get_by_role("button", name="Done", exact=True)
        if btn.count():
            target = btn.last if btn.count() > 1 else btn.first
            if target.is_visible():
                target.click(force=True, timeout=3000)
                page.wait_for_timeout(1500)
                return
    except Exception:
        pass
    coords = page.evaluate(
        """() => {
          const cands=[];
          const walk=(root)=>{
            for (const b of root.querySelectorAll('button, ytcp-button, [role=button]')) {
              const t=(b.innerText||b.textContent||'').replace(/\\s+/g,' ').trim();
              if (t!=='Done') continue;
              const r=b.getBoundingClientRect();
              if (r.width>20 && r.height>10 && r.y>300) {
                cands.push({x:r.x+r.width/2,y:r.y+r.height/2,yPos:r.y,
                  dis:!!(b.disabled||b.getAttribute('aria-disabled')==='true')});
              }
            }
            for (const el of root.querySelectorAll('*')) if (el.shadowRoot) walk(el.shadowRoot);
          };
          const dlg=document.querySelector('tp-yt-paper-dialog[aria-label="Select video privacy"]')
            || document.querySelector('tp-yt-paper-dialog');
          walk(dlg||document);
          if (!cands.length) walk(document);
          cands.sort((a,b)=>b.yPos-a.yPos);
          return cands.find(c=>!c.dis)||cands[0]||null;
        }"""
    )
    if coords:
        page.mouse.click(coords["x"], coords["y"])
        page.wait_for_timeout(1500)


def save_edit(page) -> bool:
    try:
        b = page.get_by_role("button", name="Save", exact=True)
        if b.count() and b.first.is_enabled():
            b.first.click(force=True)
            page.wait_for_timeout(3000)
            return True
    except Exception:
        pass
    return False


def click_private_radio(page) -> dict | None:
    return page.evaluate(
        """() => {
          const dlg=document.querySelector('tp-yt-paper-dialog[aria-label="Select video privacy"]')
            || document.querySelector('tp-yt-paper-dialog') || document;
          const walk=(root)=>{
            for (const el of root.querySelectorAll('tp-yt-paper-radio-button,[role=radio],label,div')) {
              const t=(el.innerText||'').replace(/\\s+/g,' ').trim();
              const al=el.getAttribute('aria-label')||'';
              const n=(el.getAttribute('name')||'').toUpperCase();
              if (n==='PRIVATE' || t==='Private' || /^Private\\b/i.test(al)) {
                const r=el.getBoundingClientRect();
                if (r.width>20 && r.height>5) {
                  el.scrollIntoView({block:'center'});
                  el.click();
                  return {ok:true, t:t.slice(0,40), al:al.slice(0,60)};
                }
              }
            }
            for (const el of root.querySelectorAll('*')) {
              if (el.shadowRoot) {
                const x=walk(el.shadowRoot);
                if (x) return x;
              }
            }
            return null;
          };
          return walk(dlg);
        }"""
    )


def collapse_schedule_panel(page) -> dict | None:
    """When Schedule is expanded, Private radio may be hidden."""
    return page.evaluate(
        """() => {
          const dlg=document.querySelector('tp-yt-paper-dialog[aria-label="Select video privacy"]')
            || document.querySelector('tp-yt-paper-dialog');
          let hasPrivate=false;
          const find=(root)=>{
            for (const el of root.querySelectorAll('tp-yt-paper-radio-button,[role=radio]')) {
              const n=(el.getAttribute('name')||'').toUpperCase();
              const t=(el.innerText||'').trim();
              const r=el.getBoundingClientRect();
              if ((n==='PRIVATE' || t==='Private') && r.width>10 && r.height>5) hasPrivate=true;
            }
            for (const el of root.querySelectorAll('*')) if (el.shadowRoot) find(el.shadowRoot);
          };
          find(dlg||document);
          if (hasPrivate) return {already:true};
          const walk=(root)=>{
            for (const el of root.querySelectorAll('*')) {
              const al=(el.getAttribute('aria-label')||'');
              const id=el.id||'';
              if (id==='first-container-expand-button' || /click to (expand|collapse)/i.test(al)) {
                const r=el.getBoundingClientRect();
                if (r.width>5) { el.click(); return {collapsed:true, al}; }
              }
              if (el.shadowRoot) {
                const x=walk(el.shadowRoot);
                if (x) return x;
              }
            }
            return null;
          };
          return walk(dlg||document);
        }"""
    )


def visibility_chip(page) -> str:
    try:
        return (
            page.locator("ytcp-video-metadata-visibility")
            .first.inner_text(timeout=2500)
            .replace("\n", " ")
        )
    except Exception:
        return ""


def read_related_chunk(page) -> str:
    body = page.locator("body").inner_text()
    if "Related video" not in body:
        return ""
    return body.split("Related video", 1)[-1][:320]


def related_points_at_last_star(chunk: str) -> bool:
    if not chunk or chunk.strip().startswith("None"):
        return False
    low = chunk.lower()
    return (
        LAST_STAR_ID.lower() in low
        or "last star" in low
        or "last star dies" in low
        or LAST_STAR_TITLE.lower()[:30] in low
    )


def set_private(page, video_id: str, note: str = "") -> dict:
    r: dict = {"video_id": video_id, "action": "private", "note": note, "ok": False}
    page.goto(
        f"https://studio.youtube.com/video/{video_id}/edit",
        wait_until="domcontentloaded",
        timeout=120000,
    )
    page.wait_for_timeout(4000)
    skip(page)
    dismiss(page)
    if login_wall(page):
        r["error"] = "login_wall"
        return r
    if not studio_edit_ready(page):
        r["error"] = "studio_not_ready"
        r["url"] = page.url
        r["hint"] = (
            "Profile lacks Orbit Studio access — use ~/.playwright-youtube-profile "
            "or log Chrome into @OrbitWithBen Studio once."
        )
        return r

    chip_before = visibility_chip(page)
    r["chip_before"] = chip_before
    if re.search(r"\bPrivate\b", chip_before) and not re.search(r"\bPublic\b", chip_before):
        r["ok"] = True
        r["already_private"] = True
        return r

    try:
        open_visibility(page)
    except Exception as e:
        r["open_err"] = str(e)[:160]
        try:
            page.get_by_text(
                re.compile(r"Visibility|Public|Private|Scheduled", re.I)
            ).first.click(force=True, timeout=3000)
            page.wait_for_timeout(1200)
        except Exception:
            pass

    r["collapse"] = collapse_schedule_panel(page)
    page.wait_for_timeout(400)
    r["private_click"] = click_private_radio(page)
    click_done(page)
    page.wait_for_timeout(600)
    r["saved"] = save_edit(page)
    if not r["saved"]:
        page.evaluate(
            """() => {
              for (const b of document.querySelectorAll('button, ytcp-button')) {
                const t=(b.innerText||'').trim();
                if (/^Save$/i.test(t) && !b.disabled) { b.click(); return true; }
              }
              return false;
            }"""
        )
        page.wait_for_timeout(2500)

    page.goto(
        f"https://studio.youtube.com/video/{video_id}/edit",
        wait_until="domcontentloaded",
        timeout=120000,
    )
    page.wait_for_timeout(3000)
    chip_after = visibility_chip(page)
    r["chip_after"] = chip_after
    r["ok"] = bool(re.search(r"\bPrivate\b", chip_after)) and not re.search(
        r"\bPublic\b", chip_after
    )
    try:
        page.screenshot(path=str(AUDIT / f"priv_{video_id}.png"))
    except Exception:
        pass
    return r


def set_related(page, video_id: str, long_id: str, long_title: str) -> dict:
    """Studio-only Related picker. Returns ok=False if UI unavailable."""
    r: dict = {
        "video_id": video_id,
        "action": "set_related",
        "target_long_id": long_id,
        "ok": False,
        "studio_only": True,
    }
    page.goto(
        f"https://studio.youtube.com/video/{video_id}/edit",
        wait_until="domcontentloaded",
        timeout=120000,
    )
    page.wait_for_timeout(3500)
    skip(page)
    dismiss(page)
    if login_wall(page):
        r["error"] = "login_wall"
        return r

    chunk_before = read_related_chunk(page)
    r["related_before"] = chunk_before[:200]
    if long_id and long_id in chunk_before and not related_points_at_last_star(chunk_before):
        r["ok"] = True
        r["already_correct"] = True
        return r

    picker = page.locator("ytcp-shorts-content-links-picker")
    if picker.count():
        picker.first.scroll_into_view_if_needed()
        picker.first.click(force=True)
    else:
        try:
            page.get_by_text("Related video", exact=True).first.click(force=True)
        except Exception:
            r["error"] = "no_related_picker"
            r["note"] = (
                "Shorts Related pill has no Data API — Studio UI only "
                "(ytcp-shorts-content-links-picker)."
            )
            return r

    page.wait_for_timeout(1500)
    try:
        page.locator("ytcp-video-pick-dialog").wait_for(timeout=15000)
    except Exception:
        r["error"] = "no_pick_dialog"
        return r

    search = page.locator("ytcp-video-pick-dialog #search-yours")
    if not search.count():
        search = page.get_by_placeholder(re.compile(r"Search your videos", re.I))
    if not search.count():
        r["error"] = "no_search_box"
        page.keyboard.press("Escape")
        return r

    picked = False
    for q in (long_title, long_id):
        if not q:
            continue
        search.first.fill(q)
        page.wait_for_timeout(2500)
        body = page.locator("ytcp-video-pick-dialog").inner_text()
        if "No matching results" in body:
            continue
        cells = page.locator("ytcp-video-pick-dialog ytcp-video-list-cell-video")
        if not cells.count():
            cells = page.locator("ytcp-video-pick-dialog ytcp-entity-card")
        for i in range(cells.count()):
            t = cells.nth(i).inner_text()
            is_short = bool(re.search(r"\b0:\d{2}\b", t)) and not re.search(
                r"\b1[0-9]:\d{2}\b", t
            )
            if (long_id in t or long_title[:20] in t) and not is_short:
                cells.nth(i).click(force=True)
                r["picked"] = t[:180]
                picked = True
                break
        if picked:
            break

    if not picked:
        r["error"] = "long_not_found_in_picker"
        page.keyboard.press("Escape")
        return r

    page.wait_for_timeout(800)
    for name in ("Done", "Select", "Save"):
        b = page.get_by_role("button", name=name, exact=True)
        if b.count() and b.first.is_visible() and b.first.is_enabled():
            b.first.click(force=True)
            page.wait_for_timeout(800)
            break

    r["saved"] = save_edit(page)
    page.goto(
        f"https://studio.youtube.com/video/{video_id}/edit",
        wait_until="domcontentloaded",
        timeout=120000,
    )
    page.wait_for_timeout(3000)
    chunk_after = read_related_chunk(page)
    r["related_after"] = chunk_after[:200]
    r["ok"] = bool(long_id in chunk_after or long_title[:15] in chunk_after) and (
        not related_points_at_last_star(chunk_after) or long_id == LAST_STAR_ID
    )
    try:
        page.screenshot(path=str(AUDIT / f"rel_{video_id}.png"))
    except Exception:
        pass
    return r


def verify_public_unchanged(page, video_id: str) -> dict:
    r: dict = {"video_id": video_id, "action": "verify_public", "ok": False}
    page.goto(
        f"https://studio.youtube.com/video/{video_id}/edit",
        wait_until="domcontentloaded",
        timeout=120000,
    )
    page.wait_for_timeout(3500)
    skip(page)
    dismiss(page)
    if login_wall(page):
        r["error"] = "login_wall"
        return r
    chip = visibility_chip(page)
    r["chip"] = chip
    r["ok"] = bool(re.search(r"\bPublic\b", chip)) and not re.search(
        r"\bPrivate\b", chip
    )
    return r


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--profile", help="Force a Playwright profile directory")
    args = parser.parse_args()

    profile = pick_profile(args.profile)
    plan = {
        "channel": CHANNEL,
        "profile": str(profile) if profile else None,
        "dry_run": args.dry_run,
        "unpublish": [{"id": v, "note": n} for v, _, n in UNPUBLISH_TARGETS],
        "keep_public": sorted(KEEP_PUBLIC),
        "fillers": FILLER_RELATED,
        "related_studio_only_note": (
            "Shorts Related → parent long is Studio UI only "
            "(ytcp-shorts-content-links-picker). No YouTube Data API v3 field."
        ),
        "started": datetime.now(timezone.utc).isoformat(),
        "results": {},
    }

    if args.dry_run:
        print(json.dumps(plan, indent=2))
        OUT.write_text(json.dumps(plan, indent=2) + "\n")
        return 0

    if not profile:
        plan["error"] = "no_profile"
        plan["profile_candidates"] = [str(p) for p in PROFILE_CANDIDATES]
        OUT.write_text(json.dumps(plan, indent=2) + "\n")
        print("ERROR: no Playwright profile found.", file=sys.stderr)
        print(json.dumps(plan, indent=2))
        return 2

    AUDIT.mkdir(parents=True, exist_ok=True)
    results: dict = {
        "unpublish": [],
        "keep_public": [],
        "fillers": [],
        "login_wall": False,
    }

    with sync_playwright() as p:
        ctx = p.chromium.launch_persistent_context(
            str(profile),
            headless=False,
            channel="chrome",
            args=["--disable-blink-features=AutomationControlled"],
            viewport={"width": 1440, "height": 1000},
        )
        page = ctx.pages[0] if ctx.pages else ctx.new_page()

        # Smoke: Studio home
        page.goto(
            f"https://studio.youtube.com/channel/{CHANNEL}/videos",
            wait_until="domcontentloaded",
            timeout=120000,
        )
        page.wait_for_timeout(4000)
        skip(page)
        dismiss(page)
        if login_wall(page):
            results["login_wall"] = True
            plan["results"] = results
            plan["error"] = "login_wall"
            OUT.write_text(json.dumps(plan, indent=2) + "\n")
            ctx.close()
            print("LOGIN WALL — script ready; run locally with a logged-in profile.")
            print(f"Result: {OUT}")
            return 3

        # Quick probe: can this profile open a video edit page?
        probe_id = UNPUBLISH_TARGETS[0][0]
        page.goto(
            f"https://studio.youtube.com/video/{probe_id}/edit",
            wait_until="domcontentloaded",
            timeout=120000,
        )
        page.wait_for_timeout(4000)
        skip(page)
        dismiss(page)
        if not studio_edit_ready(page):
            results["studio_not_ready"] = True
            plan["results"] = results
            plan["error"] = "studio_not_ready"
            plan["probe_url"] = page.url
            OUT.write_text(json.dumps(plan, indent=2) + "\n")
            ctx.close()
            print(
                "STUDIO NOT READY — Flow profile has no @OrbitWithBen edit access. "
                "Run with a YouTube Studio profile (see --profile)."
            )
            print(f"Result: {OUT}")
            return 4

        for video_id, _action, note in UNPUBLISH_TARGETS:
            print(f"PRIVATE {video_id} …", flush=True)
            try:
                ur = set_private(page, video_id, note)
            except Exception as e:
                ur = {"video_id": video_id, "ok": False, "error": str(e)[:300]}
            results["unpublish"].append(ur)
            print(f"  ok={ur.get('ok')} chip={ur.get('chip_after','')[:60]}", flush=True)
            OUT.write_text(json.dumps({**plan, "results": results}, indent=2) + "\n")

        for video_id in sorted(KEEP_PUBLIC):
            print(f"VERIFY PUBLIC {video_id} …", flush=True)
            try:
                vr = verify_public_unchanged(page, video_id)
            except Exception as e:
                vr = {"video_id": video_id, "ok": False, "error": str(e)[:300]}
            results["keep_public"].append(vr)
            print(f"  ok={vr.get('ok')} chip={vr.get('chip','')[:60]}", flush=True)

        for fid, cfg in FILLER_RELATED.items():
            print(f"FILLER {fid} …", flush=True)
            fr: dict = {"video_id": fid, "config": cfg}
            page.goto(
                f"https://studio.youtube.com/video/{fid}/edit",
                wait_until="domcontentloaded",
                timeout=120000,
            )
            page.wait_for_timeout(3500)
            skip(page)
            dismiss(page)
            chunk = read_related_chunk(page)
            fr["related_chunk"] = chunk[:200]
            fr["points_at_last_star"] = related_points_at_last_star(chunk)

            if not fr["points_at_last_star"]:
                fr["ok"] = True
                fr["action"] = "no_change_needed"
                results["fillers"].append(fr)
                print("  Related not Last Star — skip", flush=True)
                continue

            long_id = cfg.get("long_id")
            long_title = cfg.get("long_title") or ""
            if long_id:
                try:
                    rr = set_related(page, fid, long_id, long_title)
                except Exception as e:
                    rr = {"video_id": fid, "ok": False, "error": str(e)[:300]}
                fr["related_attempt"] = rr
                if rr.get("ok"):
                    fr["ok"] = True
                    fr["action"] = "related_fixed"
                    results["fillers"].append(fr)
                    print(f"  Related fixed → {long_id}", flush=True)
                    continue

            if cfg.get("unpublish_if_fail"):
                print(f"  Related fix failed — PRIVATE {fid}", flush=True)
                try:
                    pr = set_private(page, fid, "off-cluster filler · wrong Related pill")
                except Exception as e:
                    pr = {"video_id": fid, "ok": False, "error": str(e)[:300]}
                fr["unpublish"] = pr
                fr["ok"] = pr.get("ok", False)
                fr["action"] = "unpublished_filler"
                fr["studio_only_note"] = (
                    "Could not set Related via automation; unpublish fallback. "
                    "Manual Studio fix: video edit → Related video."
                )
            else:
                fr["ok"] = False
                fr["action"] = "manual_studio_required"
                fr["studio_only_note"] = (
                    "Related pill is Studio-only — set manually in Studio."
                )
            results["fillers"].append(fr)

        ctx.close()

    plan["results"] = results
    plan["finished"] = datetime.now(timezone.utc).isoformat()
    plan["ok"] = (
        not results.get("login_wall")
        and all(u.get("ok") for u in results["unpublish"])
        and all(k.get("ok") for k in results["keep_public"])
        and all(f.get("ok") for f in results["fillers"])
    )
    OUT.write_text(json.dumps(plan, indent=2) + "\n")
    print(f"\nRESULT → {OUT}")
    print(f"ok={plan['ok']}")
    return 0 if plan["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
