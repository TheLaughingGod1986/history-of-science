#!/usr/bin/env python3
"""Mint ONE Flow IMAGE still (Nano Banana) for HOS 002 thumb C via Mini CDP :9222.

Same image route as `_mint_flow_image_still_v01.py` (Image mode / Nano Banana),
but connects to the shared benoats@googlemail.com CDP Chrome.

HARD: open a NEW tab only. Never navigate/close other Flow tabs (004 mint).
Record credits before/after. Max 2 tries (caller changes framing on FAIL).
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO / "04_Audio" / "tools"))
import orbit_flow_veo_ui as flow  # noqa: E402

CDP = os.environ.get("ORBIT_FLOW_CDP", "http://127.0.0.1:9222")
REQUIRED = "benoats@googlemail.com"
CREDIT_RE = re.compile(r"([\d,]{1,7})\s*(?:Google\s+Flow\s+)?credits", re.I)

# Compose-ready framing: slot ~1/4 frame width, a little right of centre,
# calm clean space top-left for LEFT / EMPTY / ON PURPOSE.
PROMPT_TRY1 = """Premium Animistry-class 3D cartoon still, 16:9 widescreen, native high resolution.
Warm library: dark polished wood wall grid of blank cream rectangular tiles (NO element symbols,
NO letters, NO numbers, NO readable text on tiles). Soft warm library lamp light, rich wood grain,
finished feature-animation polish — not photoreal, not flat cel.

HERO: one empty dark rectangular slot with a bright warm yellow-orange glowing rim.
The empty slot plus its glow fills about one quarter of the frame width, placed a little
RIGHT of centre. Surrounding tiles stay blank cream. Calm clean negative space in the
UPPER-LEFT third for later title text (no objects or bright glow there).

HARD REJECT: people, Explorer, boy, hands, Orbit robot, readable text, element symbols,
periodic-table letters, UI, watermark, photoreal photo, jar of soup of symbols.
Silent still. Single frame."""

PROMPT_TRY2 = """Premium Animistry 3D cartoon 16:9 still. Close-medium on a wooden library
periodic-table wall of blank cream tiles only (no symbols). One glowing empty slot is the
clear hero — dark void, bright gold rim bloom — sized about 25% of frame width, sitting
slightly right of centre. Soft warm lamp light from the left, but the upper-left stays
calm and empty for text. No people, no text, no element soup. Finished CGI polish."""


def page_text(page, n: int = 12000) -> str:
    try:
        return page.locator("body").inner_text(timeout=8000)[:n]
    except Exception:
        return ""


def open_account_menu(page) -> None:
    for sel in (
        '[aria-label*="Account details" i]',
        '[aria-label*="Google Account" i]',
        'button:has-text("ULTRA")',
        "text=ULTRA",
    ):
        try:
            loc = page.locator(sel).first
            if loc.count() == 0:
                continue
            loc.click(timeout=2500)
            time.sleep(1.4)
            return
        except Exception:
            continue


def close_overlays(page) -> None:
    """Close account menu / dialogs that steal the Create click."""
    for _ in range(4):
        try:
            page.keyboard.press("Escape")
        except Exception:
            pass
        page.wait_for_timeout(150)
    try:
        # Click empty canvas (not the prompt bar)
        page.mouse.click(640, 280)
    except Exception:
        pass
    page.wait_for_timeout(200)


def read_credits(page) -> tuple[int | None, str | None]:
    def parse(text: str) -> tuple[int | None, str | None]:
        emails = set(re.findall(r"[A-Za-z0-9._%+-]+@(?:gmail|googlemail)\.com", text, flags=re.I))
        active = None
        if REQUIRED.lower() in {e.lower() for e in emails}:
            active = REQUIRED.lower()
        elif emails:
            active = sorted(emails)[0].lower()
        hits = [int(m.group(1).replace(",", "")) for m in CREDIT_RE.finditer(text)]
        credits = None
        if hits:
            near = [c for c in hits if 100 <= c <= 20000]
            credits = near[0] if near else max(hits)
        return credits, active

    credits, active = parse(page_text(page))
    if credits is None or active is None:
        open_account_menu(page)
        credits2, active2 = parse(page_text(page))
        credits = credits if credits is not None else credits2
        active = active or active2
        close_overlays(page)
    else:
        close_overlays(page)
    return credits, active


def pill_text(page) -> str:
    return page.evaluate(
        """() => {
          for (const b of document.querySelectorAll('button')) {
            const t = (b.innerText || '').trim().replace(/\\n/g, ' ');
            if (/Nano Banana|Video ·|Omni Flash|Omni 1|Veo 3|crop_16_9|\\bImage\\b/i.test(t)) {
              const r = b.getBoundingClientRect();
              if (r.width > 40 && r.height > 16) return t.slice(0, 120);
            }
          }
          return '';
        }"""
    ) or ""


def _pill_is_image_16x9(pill: str) -> bool:
    if not pill:
        return False
    image_ok = bool(re.search(r"Nano Banana|Banana|\bImage\b", pill, re.I))
    # Reject Video-mode pills even if they mention 16:9
    if re.search(r"\bVideo\b|Veo\s*3|Omni", pill, re.I) and not re.search(
        r"Banana|Nano", pill, re.I
    ):
        return False
    ratio_ok = bool(re.search(r"16:9|crop_16_9|16\s*[:×x]\s*9", pill, re.I))
    return image_ok and ratio_ok


def select_image_tab(page) -> None:
    # Wait briefly for the settings pill to hydrate (empty pill → false settings open).
    pill0 = ""
    for _ in range(8):
        pill0 = pill_text(page)
        if pill0:
            break
        page.wait_for_timeout(500)
    print(f"  pill before={pill0!r}", flush=True)
    # Already on Nano Banana / Image + 16:9 — nothing to switch.
    if _pill_is_image_16x9(pill0):
        print("  already Image/Nano Banana 16:9 — skip settings", flush=True)
        return
    flow._open_prompt_settings_pill(page)
    page.wait_for_timeout(900)
    # Re-check pill after opening (some UIs already show Banana in the pill only).
    pill1 = pill_text(page)
    if _pill_is_image_16x9(pill1):
        print("  pill ok after open — skip radio hunt", flush=True)
        try:
            page.keyboard.press("Escape")
        except Exception:
            pass
        return
    box = page.evaluate(
        """() => {
          const nodes = document.querySelectorAll(
            'button[role=radio],button[role=tab],[role=radio],button,[role=option]'
          );
          for (const b of nodes) {
            const t = ((b.innerText||'')+' '+(b.getAttribute('aria-label')||'')
                       +' '+(b.getAttribute('data-value')||'')).trim();
            // Flow labels: "image Image" / "videocam Video" / "🍌 Nano Banana"
            if ((/\\bimage\\b/i.test(t) || /banana/i.test(t)) && !/video|veo|omni/i.test(t)) {
              const r = b.getBoundingClientRect();
              if (r.width > 20 && r.height > 16)
                return {x:r.x+r.width/2,y:r.y+r.height/2,t:t.slice(0,80),
                        sel:b.getAttribute('aria-checked')||b.getAttribute('aria-selected')};
            }
          }
          return null;
        }"""
    )
    if not box:
        qa = Path(
            "/Users/benjaminoats/YouTube/hos-002-ab/02_Video-Projects/"
            "002_How-Did-We-Discover-The-Periodic-Table/08_Thumbnail/"
            "_stills_v05/_qa_mint/image_radio_missing.png"
        )
        qa.parent.mkdir(parents=True, exist_ok=True)
        page.screenshot(path=str(qa), full_page=False)
        # Last chance: if pill already reads Banana+16:9, proceed anyway.
        pill2 = pill_text(page)
        if _pill_is_image_16x9(pill2):
            print(f"  radio missing but pill ok={pill2!r} — proceed", flush=True)
            try:
                page.keyboard.press("Escape")
            except Exception:
                pass
            return
        raise RuntimeError(f"Image radio not found in settings popover (pill={pill2!r})")
    if box.get("sel") not in {"true", "True"}:
        page.mouse.click(box["x"], box["y"])
        page.wait_for_timeout(700)
    page.evaluate(
        """() => {
          for (const b of document.querySelectorAll('button,[role=radio],[role=option]')) {
            const t = ((b.innerText||'')+' '+(b.getAttribute('aria-label')||'')).trim();
            if (/crop_16_9|\\b16:9\\b/.test(t)) { b.click(); return true; }
          }
          return false;
        }"""
    )
    page.wait_for_timeout(400)
    try:
        page.keyboard.press("Escape")
    except Exception:
        pass
    page.wait_for_timeout(400)
    pill = pill_text(page)
    print(f"  image-mode pill={pill!r}", flush=True)
    if pill and re.search(r"\bVideo\b", pill) and not re.search(r"Banana|Image", pill, re.I):
        raise RuntimeError(f"Failed to switch to Image mode: {pill!r}")


def download_newest_image(page, dest: Path, timeout_s: float = 240) -> Path:
    dest.parent.mkdir(parents=True, exist_ok=True)
    qa_dir = dest.parent / "_qa_mint"
    qa_dir.mkdir(parents=True, exist_ok=True)
    t0 = time.time()
    while time.time() - t0 < timeout_s:
        # Keep confirming spend dialogs if they appear late.
        try:
            flow.dismiss_soft_prompts(page)
        except Exception:
            pass
        hit = page.evaluate(
            """() => {
              const imgs=[...document.querySelectorAll('img')].map(i=>{
                const r=i.getBoundingClientRect();
                return {x:r.x+r.width/2,y:r.y+r.height/2,w:r.width,h:r.height,y0:r.y,
                        src:i.currentSrc||i.src||''};
              }).filter(i=>i.w>120&&i.h>70&&i.y0>60);
              imgs.sort((a,b)=>b.y0-a.y0 || b.w*b.h-a.w*a.h);
              return imgs[0]||null;
            }"""
        )
        body_snip = page_text(page, 2500)
        gen_hint = bool(
            re.search(
                r"\b\d{1,3}%\b|in the queue|generat(?:ing|e)|rendering",
                body_snip,
                re.I,
            )
        ) and "Start creating or drop media" not in body_snip
        print(
            f"  image poll hit={'yes' if hit else 'no'} "
            f"gen_hint={gen_hint} elapsed={int(time.time()-t0)}s",
            flush=True,
        )
        if hit:
            page.mouse.click(hit["x"], hit["y"])
            page.wait_for_timeout(1200)
            for label in ("Download", "download", "Save"):
                btn = page.get_by_role("button", name=re.compile(label, re.I))
                if btn.count():
                    try:
                        with page.expect_download(timeout=20000) as dl:
                            btn.first.click(timeout=4000)
                        d = dl.value
                        d.save_as(str(dest))
                        if dest.exists() and dest.stat().st_size > 40000:
                            return dest
                    except Exception as e:
                        print(f"  download via {label} failed: {e}", flush=True)
            src = hit.get("src") or page.evaluate(
                """() => {
                  const imgs=[...document.querySelectorAll('img')].map(i=>{
                    const r=i.getBoundingClientRect();
                    return {src:i.currentSrc||i.src,w:r.width,h:r.height};
                  }).filter(i=>i.w>300&&i.h>160&&i.src);
                  imgs.sort((a,b)=>b.w*b.h-a.w*a.h);
                  return imgs[0]?.src||null;
                }"""
            )
            if src and str(src).startswith("http"):
                data = page.evaluate(
                    """async (url) => {
                      const r = await fetch(url); const b = await r.arrayBuffer();
                      const u = new Uint8Array(b); let s='';
                      for (let i=0;i<u.length;i++) s+=String.fromCharCode(u[i]);
                      return btoa(s);
                    }""",
                    src,
                )
                import base64

                dest.write_bytes(base64.b64decode(data))
                if dest.stat().st_size > 40000:
                    return dest
            # blob: / data: URLs
            if src and str(src).startswith("data:image"):
                import base64

                b64 = str(src).split(",", 1)[-1]
                dest.write_bytes(base64.b64decode(b64))
                if dest.stat().st_size > 40000:
                    return dest
        page.wait_for_timeout(4000)
    try:
        page.screenshot(path=str(qa_dir / "download_timeout.png"), full_page=False)
    except Exception:
        pass
    raise RuntimeError(f"Timed out waiting for Flow image still → {dest}")


def qa_still(path: Path) -> tuple[str, str]:
    from PIL import Image

    im = Image.open(path).convert("RGB")
    w, h = im.size
    if w < 1000 or h < 560:
        return "FAIL", f"too small {w}x{h}"
    ratio = w / h
    if abs(ratio - 16 / 9) > 0.12:
        return "FAIL", f"not 16:9 ratio={ratio:.3f}"
    # Reject if mostly text-like bright UI (heuristic: too much near-white)
    px = im.resize((64, 36)).getdata()
    whiteish = sum(1 for r, g, b in px if r > 240 and g > 240 and b > 240)
    if whiteish > 0.45 * 64 * 36:
        return "FAIL", "too much white / UI"
    return "KEEP", f"{w}x{h} ratio={ratio:.3f}"


def append_004_mint_note(credits_before: int | None, credits_after: int | None, used: int | None) -> None:
    """One-line note so Part 02 balance check still reconciles."""
    log = Path(
        "/Users/benjaminoats/YouTube/History Of Science/02_Video-Projects/"
        "004_Whats-Really-Inside-An-Atom/07_Edit-Project/PART02_MINT_LOG_v01.json"
    )
    note = (
        f"{datetime.now(timezone.utc).isoformat()} HOS002_AB_THUMB_C_STILL "
        f"Image/NanoBanana via CDP new-tab only; "
        f"credits_before={credits_before} used={used} after={credits_after} "
        f"(shared :9222; 002 A/B pack — do not treat as Part 02 spend)"
    )
    note_path = log.with_name("PART02_MINT_LOG_SHARED_CREDIT_NOTES.txt")
    with note_path.open("a") as f:
        f.write(note + "\n")
    # Also append into the JSON as a side field if readable
    try:
        data = json.loads(log.read_text())
        notes = data.setdefault("shared_cdp_credit_notes", [])
        notes.append(note)
        data["updated_at_shared_note"] = datetime.now(timezone.utc).isoformat()
        log.write_text(json.dumps(data, indent=2) + "\n")
    except Exception as e:
        print(f"  warn: could not patch PART02_MINT_LOG json: {e}", flush=True)
    print(f"  appended 004 credit note → {note_path}", flush=True)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--try", dest="try_n", type=int, default=1, choices=(1, 2))
    ap.add_argument(
        "--project-home",
        default=os.environ.get("HOS_FLOW_HOME", "https://flow.google.com/"),
        help="Open NEW project from Flow home (do not reuse 004 project URL)",
    )
    args = ap.parse_args()
    prompt = PROMPT_TRY1 if args.try_n == 1 else PROMPT_TRY2

    from playwright.sync_api import sync_playwright

    print(f"IMAGE_STILL_CDP try={args.try_n} out={args.out} cdp={CDP}", flush=True)
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(CDP)
        ctx = browser.contexts[0] if browser.contexts else browser.new_context()
        # NEW tab only — never touch existing Flow pages
        page = ctx.new_page()
        our_page = page
        qa_dir = args.out.parent / "_qa_mint"
        qa_dir.mkdir(parents=True, exist_ok=True)
        try:
            # Prefer a dedicated HOS image project (002 pinned), never the 004 project tab.
            pinned = os.environ.get(
                "HOS_FLOW_PROJECT_URL",
                "https://flow.google.com/project/30a34afb-8d9c-4eac-83ba-012d97f6b1b5",
            )
            page.goto(pinned, wait_until="domcontentloaded", timeout=120_000)
            page.wait_for_timeout(2800)
            flow.dismiss_banners(page)
            if "/project/" not in (page.url or ""):
                page.goto(args.project_home, wait_until="domcontentloaded", timeout=120_000)
                page.wait_for_timeout(2000)
                flow.dismiss_banners(page)
                for label in (r"New project", r"Create with Flow", r"^New$"):
                    try:
                        btn = page.get_by_role("button", name=re.compile(label, re.I))
                        if btn.count():
                            btn.first.click(timeout=3000)
                            page.wait_for_timeout(2500)
                            break
                    except Exception:
                        continue
            flow.dismiss_banners(page)
            page.screenshot(path=str(qa_dir / f"gate_try{args.try_n}.png"), full_page=False)
            credits_before, active = read_credits(page)
            print(
                f"  GATE account={active} credits_before={credits_before} url={page.url}",
                flush=True,
            )
            if active and active not in {REQUIRED.lower(), "benoats@gmail.com"}:
                raise SystemExit(f"STOP wrong account: {active}")
            if credits_before is not None and credits_before < 50:
                raise SystemExit(f"STOP low credits={credits_before}")

            select_image_tab(page)
            try:
                flow.force_outputs_x1(page)
            except Exception as e:
                print(f"  force_outputs_x1 warn: {e}", flush=True)
            try:
                flow._ensure_create_prompt_mode(page)
            except Exception as e:
                print(f"  create-mode warn: {e}", flush=True)
            # Robust prompt fill — Flow Slate sometimes drops the first insert_text.
            armed = False
            last_err: Exception | None = None
            for attempt in range(1, 4):
                try:
                    flow.ensure_agent_session(page)
                    flow.set_prompt(page, prompt)
                    armed = True
                    break
                except Exception as e:
                    last_err = e
                    print(f"  set_prompt attempt {attempt}/3 failed: {e}", flush=True)
                    page.wait_for_timeout(800)
                    try:
                        box = flow.editor_box(page)
                        if box:
                            page.mouse.click(
                                box["x"] + min(box["w"] - 40, 200),
                                box["y"] + max(8, box["h"] / 2),
                            )
                            page.wait_for_timeout(200)
                            page.keyboard.insert_text(prompt)
                            page.wait_for_timeout(400)
                            got = flow._editor_prompt_text(page)
                            if got and len(got) >= 24 and not got.lower().startswith(
                                "what do you want"
                            ):
                                print(
                                    f"  set_prompt fallback ok head={got[:60]!r}",
                                    flush=True,
                                )
                                armed = True
                                break
                    except Exception as e2:
                        print(f"  set_prompt fallback err: {e2}", flush=True)
            if not armed:
                raise RuntimeError(f"Could not arm Flow prompt editor: {last_err}")
            # Account / overlay menus block the send click (seen in live_02 QA).
            for _ in range(3):
                try:
                    page.keyboard.press("Escape")
                except Exception:
                    pass
                page.wait_for_timeout(200)
            print("  submitting Image Create…", flush=True)
            # Prefer direct JS click on prompt-bar arrow (mouse coords flake when
            # the expanded prompt modal reflows).
            clicked = page.evaluate(
                """() => {
                  const ranked = [];
                  for (const b of document.querySelectorAll('button')) {
                    const t = (b.innerText || '').trim().replace(/\\n/g, ' ');
                    if (!/arrow_forward/i.test(t)) continue;
                    if (b.disabled || b.getAttribute('aria-disabled') === 'true') continue;
                    const r = b.getBoundingClientRect();
                    if (r.width < 8 || r.height < 8) continue;
                    ranked.push({b, y: r.y, t});
                  }
                  if (!ranked.length) return null;
                  ranked.sort((a, c) => c.y - a.y);
                  ranked[0].b.click();
                  return ranked[0].t;
                }"""
            )
            if not clicked:
                flow.submit_create(page)
            else:
                print(f"  js-clicked send ({clicked!r})", flush=True)
            page.wait_for_timeout(800)
            # Keyboard fallback if prompt still sitting idle
            got_after = flow._editor_prompt_text(page)
            body_head = page_text(page, 3000)
            started = bool(
                re.search(
                    r"generat|in the queue|rendering|Creating your|high demand",
                    body_head,
                    re.I,
                )
            ) and not re.search(r"Start creating or drop media", body_head)
            if not started and got_after and len(got_after) > 40:
                print("  send may have missed — trying Enter / submit_create", flush=True)
                try:
                    box = flow.editor_box(page)
                    if box:
                        page.mouse.click(
                            box["x"] + min(box["w"] - 40, 200),
                            box["y"] + max(8, box["h"] / 2),
                        )
                        page.wait_for_timeout(150)
                    page.keyboard.press("Enter")
                    page.wait_for_timeout(600)
                except Exception as e:
                    print(f"  Enter fallback warn: {e}", flush=True)
                try:
                    flow.submit_create(page)
                except Exception as e:
                    print(f"  submit_create fallback warn: {e}", flush=True)
            confirmed = flow.confirm_generation_spend(page, timeout_s=20.0)
            print(f"  confirm_spend={confirmed}", flush=True)
            # Soft-prompt pass for image-specific confirm labels
            flow.dismiss_soft_prompts(page)
            page.wait_for_timeout(4000)
            # Early abort if credits unchanged AND still empty after short wait —
            # download_newest_image will still poll.
            path = download_newest_image(page, args.out, timeout_s=200)
            credits_after, _ = read_credits(page)
            used = None
            if credits_before is not None and credits_after is not None:
                used = max(0, credits_before - credits_after)
            verdict, reason = qa_still(path)
            meta = {
                "out": str(path),
                "bytes": path.stat().st_size,
                "try": args.try_n,
                "account": active,
                "credits_before": credits_before,
                "credits_after": credits_after,
                "credits_used": used,
                "qa": verdict,
                "qa_reason": reason,
                "url": page.url,
                "pulled": datetime.now(timezone.utc).isoformat(),
            }
            meta_path = args.out.with_suffix(".meta.json")
            meta_path.write_text(json.dumps(meta, indent=2) + "\n")
            append_004_mint_note(credits_before, credits_after, used)
            print(f"OK {verdict} {reason} meta={meta_path}", flush=True)
            print(json.dumps(meta), flush=True)
            return 0 if verdict == "KEEP" else 2
        finally:
            # Close ONLY our tab
            try:
                our_page.close()
            except Exception:
                pass
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
