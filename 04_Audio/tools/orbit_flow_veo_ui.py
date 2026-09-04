#!/usr/bin/env python3
"""Orbit CG via Google Flow Veo UI (Ultra plan — default picture path).

Uses Playwright against labs.google/fx/tools/flow so Google One → AI Ultra
Flow credits apply (**Veo 3.1** only — never Omni Flash / Nano Banana for Orbit CG).
Prefer this over AI Studio (needs billed API key) and over GEMINI_API_KEY (separate billing).

Channel VO stays on ElevenLabs TTS → Ben Orbit Narrator (see orbit_voice.py).

One-time auth (headed) — same Google profile as AI Studio works:
  python3 04_Audio/tools/orbit_flow_veo_ui.py --login

Generate:
  python3 04_Audio/tools/orbit_flow_veo_ui.py --probe
  python3 04_Audio/tools/orbit_flow_veo_ui.py \\
    --prompt "Orbit floats beside JWST…" --out /tmp/orbit_test.mp4

Fallbacks (only if Flow UI is broken):
  python3 04_Audio/tools/orbit_aistudio_veo_ui.py --probe
  python3 04_Audio/tools/orbit_gemini_veo.py --probe
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
from pathlib import Path
from urllib.parse import urljoin

REPO = Path(__file__).resolve().parents[2]
TOOLS = Path(__file__).resolve().parent
sys.path.insert(0, str(TOOLS))

import orbit_gemini_veo as veo  # noqa: E402 — shared prompt lock / strip_audio

# Google moved Flow off labs.google; prefer the live host (labs still redirects).
FLOW_HOME = "https://flow.google.com/"
# Ultra AI-credit account (benoats@googlemail.com) is typically /u/1/ in this profile.
FLOW_HOME_ULTRA = os.environ.get("ORBIT_FLOW_HOME", "https://flow.google.com/u/1/")
FLOW_HOME_LEGACY = "https://labs.google/fx/tools/flow"
DEFAULT_PROFILE = Path(
    os.environ.get(
        "ORBIT_FLOW_PROFILE",
        os.environ.get(
            "ORBIT_AISTUDIO_PROFILE",
            str(Path.home() / "code" / "youtube" / ".playwright-aistudio-profile"),
        ),
    )
)
DEFAULT_MODEL = os.environ.get("ORBIT_FLOW_VEO_MODEL", "Veo 3.1 - Quality")
# Flow video CG must stay on Veo 3.x — never Omni Flash / Nano Banana for Orbit motion.
VEO3_MODEL_RE = re.compile(r"^Veo\s*3(\.\d+)?\s*-\s*(Lite|Fast|Quality)$", re.I)
FORBIDDEN_VIDEO_MODELS = ("Omni Flash", "Nano Banana", "Nano Banana 2")
MEDIA_REDIRECT_RE = re.compile(r"media\.getMediaUrlRedirect\?name=([a-f0-9\-]+)", re.I)

# Flow Agent invents a near-miss redesign unless the Orbit identity still is
# attached IN the prompt. CG = Flow Veo (not Seedance). Never use plates under
# 05_Seedance-References/_Rejected/ (white-chest two-sphere fake "canonical").
ORBIT_AGENT_INSTRUCTION = (
    "ORBIT IDENTITY LOCK (always): Match the attached Orbit identity reference "
    "exactly. Orbit is ONE continuous matte orange sphere/egg body (head and torso "
    "are the same piece — no neck, no two stacked spheres), NO legs, soft orange "
    "underside glow only, large black curved visor with TWO cream/white circular "
    "eyes with dark pupils, integrated side nubs (not headphones), single thin "
    "antenna with glowing bulb tip, solid orange chest (tiny vents OK — NO large "
    "white chest disc). Short stubby orange arms with dark three-finger hands may "
    "appear in motion. HARD REJECTS — never generate: large white/pale chest disc, "
    "glowing white belly plate, separate head on neck, ear rings/headphones/side "
    "discs, white helmet, legs, slit eyes, blank visor, HUD text. For video: "
    "IMAGE-TO-VIDEO animate the attached Orbit reference exactly — do not invent "
    "a new robot species."
)

FLOW_I2V_PREFACE = (
    "IMAGE-TO-VIDEO of the attached Orbit identity reference. Animate THIS exact "
    "single continuous orange sphere character — black curved visor, cream circular "
    "eyes, integrated side nubs, single antenna, solid orange chest. Do NOT redesign. "
    "Reject white chest disc, ear rings/headphones, two-sphere head/body split."
)


def profile_path(override: Path | None = None) -> Path:
    p = override or DEFAULT_PROFILE
    p.mkdir(parents=True, exist_ok=True)
    return p


# HOS Ultra mint account — has AI credits when Flow credits are 0.
# Playwright often defaults to benoats86@gmail.com (Flow-only pool).
DEFAULT_FLOW_ACCOUNT = os.environ.get(
    "ORBIT_FLOW_ACCOUNT", "benoats@googlemail.com"
)
ACCOUNT_CHOOSER_URL = (
    "https://accounts.google.com/AccountChooser?"
    "continue=https%3A%2F%2Fflow.google.com%2F"
)


def ensure_flow_account(page, email: str | None = None) -> str:
    """Force the Flow session onto the Ultra account with AI-credit fallback.

    Returns the email string we attempted to select. Raises if the chooser
    cannot surface the account (manual login required once).
    """
    target = (email or DEFAULT_FLOW_ACCOUNT).strip().lower()
    print(f"  ensure Flow account → {target}", flush=True)
    page.goto(ACCOUNT_CHOOSER_URL, wait_until="domcontentloaded", timeout=120_000)
    page.wait_for_timeout(2500)
    dismiss_banners(page)
    body = ""
    try:
        body = page.locator("body").inner_text(timeout=8000)
    except Exception:
        pass
    if target not in body.lower():
        # Already on Flow with that session, or chooser skipped
        if "flow.google.com" in (page.url or ""):
            print(f"  chooser skipped — already on Flow url={page.url}", flush=True)
            return target
        raise RuntimeError(
            f"Flow account chooser does not list {target}. "
            "Sign in once with ORBIT_FLOW_PROFILE headed."
        )
    clicked = False
    loc = page.locator(f'[data-email="{target}"], [data-identifier="{target}"]')
    if loc.count():
        loc.first.click(timeout=15_000)
        clicked = True
    else:
        try:
            page.get_by_text(target, exact=False).first.click(timeout=15_000)
            clicked = True
        except Exception:
            hit = page.evaluate(
                """(email) => {
                  for (const n of document.querySelectorAll(
                    'div,li,button,a,[role="link"],[role="option"]'
                  )) {
                    const t = ((n.innerText || '') + ' ' +
                      (n.getAttribute('data-email') || '')).toLowerCase();
                    if (t.includes(email)) { n.click(); return true; }
                  }
                  return false;
                }""",
                target,
            )
            clicked = bool(hit)
    if not clicked:
        raise RuntimeError(f"Could not click Flow account {target}")
    try:
        page.wait_for_url("**/flow.google.com/**", timeout=90_000)
    except Exception:
        page.wait_for_timeout(5000)
    dismiss_banners(page)
    print(f"  Flow account ready url={page.url}", flush=True)
    # Best-effort credit readout from account panel
    try:
        page.locator('[aria-label*="Account" i]').first.click(timeout=4000)
        page.wait_for_timeout(800)
        panel = page.locator("body").inner_text(timeout=4000)
        for line in panel.splitlines():
            if re.search(r"credit|@gmail|@googlemail", line, re.I):
                print(f"  acct: {line.strip()[:160]}", flush=True)
        page.keyboard.press("Escape")
    except Exception as e:
        print(f"  account panel readout skipped: {e}", flush=True)
    return target


def launch_context(playwright, *, headed: bool, profile: Path, slow_mo: int = 0):
    args = [
        "--disable-blink-features=AutomationControlled",
        "--no-first-run",
        "--no-default-browser-check",
    ]
    kwargs = {
        "user_data_dir": str(profile),
        "headless": not headed,
        "viewport": {"width": 1440, "height": 900},
        "accept_downloads": True,
        "args": args,
        "slow_mo": slow_mo or 0,
        "permissions": ["clipboard-read", "clipboard-write"],
    }
    # Prefer installed Chrome (matches Ultra Google session better)
    try:
        ctx = playwright.chromium.launch_persistent_context(channel="chrome", **kwargs)
    except Exception:
        ctx = playwright.chromium.launch_persistent_context(**kwargs)
    page = ctx.pages[0] if ctx.pages else ctx.new_page()
    try:
        ctx.grant_permissions(
            ["clipboard-read", "clipboard-write"], origin="https://labs.google"
        )
    except Exception:
        pass
    # HOS mint must stay on Flow — Chrome profile can auto-open Orbit Facebook.
    def _abort_social(route):
        route.abort()

    for host in (
        "**/facebook.com/**",
        "**/www.facebook.com/**",
        "**/instagram.com/**",
        "**/www.instagram.com/**",
        "**/threads.com/**",
        "**/www.threads.com/**",
        "**/threads.net/**",
    ):
        try:
            ctx.route(host, _abort_social)
        except Exception:
            pass
    return ctx, page


# Playwright/Flow races that usually recover on a fresh project hop.
_TRANSIENT_UI_MARKERS = (
    "execution context was destroyed",
    "most likely because of a navigation",
    "target closed",
    "target page, context or browser has been closed",
    "frame was detached",
    "cannot find context with specified id",
    "page crashed",
    "net::err_",
    "err_internet_disconnected",
    "timeout",
    "could not find new project",
    "agent prompt editor not visible",
    "not in flow project",
    "settings save/back not found",
    "orbit prompt chip missing",
    "flow video not ready",
    "flow generation failed",
    "download too small",
)


def is_transient_ui_error(exc: BaseException) -> bool:
    msg = str(exc).lower()
    return any(m in msg for m in _TRANSIENT_UI_MARKERS)


def settle_after_nav(page, wait_ms: int = 1200) -> None:
    """Wait out Flow SPA navigations so page.evaluate won't race a destroy."""
    try:
        page.wait_for_load_state("domcontentloaded", timeout=20_000)
    except Exception:
        pass
    try:
        page.wait_for_load_state("networkidle", timeout=8_000)
    except Exception:
        pass
    page.wait_for_timeout(wait_ms)


def safe_evaluate(page, script: str, *args, retries: int = 4, pause_ms: int = 700):
    """page.evaluate with retries when Flow navigates mid-call."""
    last: BaseException | None = None
    for attempt in range(1, retries + 1):
        try:
            return page.evaluate(script, *args)
        except Exception as e:
            last = e
            if attempt >= retries or not is_transient_ui_error(e):
                raise
            print(
                f"  evaluate race (retry {attempt}/{retries}): {e}",
                flush=True,
            )
            settle_after_nav(page, wait_ms=pause_ms)
    assert last is not None
    raise last


def recover_flow_home(page) -> None:
    """Best-effort return to Flow home after a UI break."""
    try:
        page.goto(FLOW_HOME, wait_until="domcontentloaded", timeout=120_000)
        settle_after_nav(page, wait_ms=2000)
        dismiss_banners(page)
    except Exception as e:
        print(f"  recover_flow_home skipped: {e}", flush=True)


def dismiss_banners(page) -> None:
    try:
        hit = safe_evaluate(
            page,
            """() => {
              const want = [/^(Agree|I agree|Accept all|Accept)$/i, /^(No thanks|Reject|Decline)$/i, /^close$|^Dismiss$|^Got it$/i];
              for (const re of want) {
                for (const b of document.querySelectorAll('button')) {
                  const t = (b.innerText || '').trim().split('\\n')[0];
                  if (re.test(t)) {
                    try { b.click(); return t; } catch (e) {}
                  }
                }
              }
              return null;
            }""",
        )
        if hit:
            print(f"  dismissed banner via {hit!r}", flush=True)
    except Exception:
        pass
    page.wait_for_timeout(400)


def looks_logged_in(page) -> bool:
    url = (page.url or "").lower()
    if "accounts.google.com" in url and ("signin" in url or "servicelogin" in url):
        return False
    on_flow = ("labs.google" in url) or ("flow.google.com" in url)
    if not on_flow:
        return False
    if "/project/" in url:
        return True
    # Visible "New project" control on the modern home is enough.
    try:
        if page.get_by_text(re.compile(r"^\s*New project\s*$", re.I)).count() > 0:
            return True
        if page.get_by_role("button", name=re.compile(r"new project", re.I)).count() > 0:
            return True
    except Exception:
        pass
    try:
        body = page.locator("body").inner_text(timeout=5000)[:4000]
    except Exception:
        return False
    low = body.lower()
    if "sign in" in low[:500] and "new project" not in low:
        return False
    return any(
        m in low
        for m in (
            "new project",
            "flow tv",
            "ultra",
            "start creating",
            "all media",
            "create with flow",
        )
    )


def visible_button(page, *needles: str):
    """Return first visible button whose inner_text contains all needles."""
    needles_l = [n.lower() for n in needles]
    buttons = page.locator("button")
    for i in range(buttons.count()):
        b = buttons.nth(i)
        try:
            box = b.bounding_box()
            if not box or box["width"] < 2 or box["height"] < 2:
                continue
            text = (b.inner_text(timeout=400) or "").lower().replace("\n", " ")
            if all(n in text for n in needles_l):
                return b
        except Exception:
            continue
    return None


def click_visible(page, *needles: str, timeout: int = 8000) -> bool:
    b = visible_button(page, *needles)
    if not b:
        return False
    b.click(timeout=timeout)
    return True


# Flow 2026-09 UI: prompt is often a contenteditable ("What do you want to create?")
# not the older Slate `[data-slate-editor="true"]` node.
_PROMPT_EDITOR_JS = """() => {
  const score = (el) => {
    if (!el) return null;
    const r = el.getBoundingClientRect();
    if (r.width < 40 || r.height < 10) return null;
    if (r.bottom < 0 || r.top > (window.innerHeight || 900)) return null;
    const aria = (el.getAttribute('aria-label') || '').toLowerCase();
    const ph = (el.getAttribute('placeholder') || '').toLowerCase();
    const t = (el.innerText || el.textContent || '').toLowerCase();
    const cls = (el.className || '').toString();
    const hint = aria + ' ' + ph + ' ' + t.slice(0, 80);
    let s = r.width * Math.max(r.height, 24);
    // Prefer the agent composer on the right.
    if (r.x > 900) s += 20000;
    if (/what do you want|what would you like|create\\?|prompt|describe/i.test(hint)) s += 50000;
    if (cls.includes('ProseMirror')) s += 45000;
    if (el.getAttribute('data-slate-editor') === 'true') s += 40000;
    if (el.getAttribute('contenteditable') === 'true') s += 10000;
    if ((el.getAttribute('role') || '') === 'textbox') s += 8000;
    if (el.tagName === 'TEXTAREA') s += 6000;
    return {el, s, w: r.width, h: r.height, x: r.x, y: r.y};
  };
  const cands = [];
  for (const sel of [
    '.ProseMirror[contenteditable="true"]',
    '[data-slate-editor="true"]',
    '[contenteditable="true"]',
    'textarea',
    '[role="textbox"]',
  ]) {
    for (const el of document.querySelectorAll(sel)) {
      const hit = score(el);
      if (hit) cands.push(hit);
    }
  }
  cands.sort((a, b) => b.s - a.s);
  if (!cands.length) return null;
  const best = cands[0];
  return {w: best.w, h: best.h, x: best.x, y: best.y};
}"""

_FOCUS_PROMPT_EDITOR_JS = """() => {
  const score = (el) => {
    if (!el) return null;
    const r = el.getBoundingClientRect();
    if (r.width < 40 || r.height < 10) return null;
    const aria = (el.getAttribute('aria-label') || '').toLowerCase();
    const ph = (el.getAttribute('placeholder') || '').toLowerCase();
    const t = (el.innerText || el.textContent || '').toLowerCase();
    const cls = (el.className || '').toString();
    const hint = aria + ' ' + ph + ' ' + t.slice(0, 80);
    let s = r.width * Math.max(r.height, 24);
    if (r.x > 900) s += 20000;
    if (/what do you want|what would you like|create\\?|prompt|describe/i.test(hint)) s += 50000;
    if (cls.includes('ProseMirror')) s += 45000;
    if (el.getAttribute('data-slate-editor') === 'true') s += 40000;
    if (el.getAttribute('contenteditable') === 'true') s += 10000;
    if ((el.getAttribute('role') || '') === 'textbox') s += 8000;
    if (el.tagName === 'TEXTAREA') s += 6000;
    return {el, s};
  };
  const cands = [];
  for (const sel of [
    '.ProseMirror[contenteditable="true"]',
    '[data-slate-editor="true"]',
    '[contenteditable="true"]',
    'textarea',
    '[role="textbox"]',
  ]) {
    for (const el of document.querySelectorAll(sel)) {
      const hit = score(el);
      if (hit) cands.push(hit);
    }
  }
  cands.sort((a, b) => b.s - a.s);
  if (!cands.length) return false;
  const ed = cands[0].el;
  ed.focus();
  try {
    const sel = window.getSelection();
    if (sel) {
      const range = document.createRange();
      range.selectNodeContents(ed);
      sel.removeAllRanges();
      sel.addRange(range);
    }
  } catch (e) {}
  return true;
}"""


def editor_box(page) -> dict | None:
    try:
        return safe_evaluate(
            page,
            _PROMPT_EDITOR_JS,
            retries=3,
            pause_ms=500,
        )
    except Exception:
        return None


def editor_usable(page) -> bool:
    """True when the agent prompt editor is on-screen and wide enough to type."""
    box = editor_box(page)
    if not box or box["w"] < 40:
        return False
    # Closed session leaves a 0×0 or off-viewport editor node in the DOM
    try:
        vw = page.viewport_size["width"] if page.viewport_size else 1440
    except Exception:
        vw = 1440
    return 0 <= box["x"] < vw - 40 and box["y"] > -20


def ensure_agent_session(page) -> None:
    """Make sure the right-hand agent session + prompt bar are open."""
    if editor_usable(page):
        return
    # Prefer JS clicks — Playwright locator clicks often hang on Flow overlays.
    try:
        safe_evaluate(
            page,
            """() => {
              const clickMatch = (re) => {
                for (const el of document.querySelectorAll('button,div,[role="button"]')) {
                  const t = (el.innerText || '').trim().replace(/\\n/g, ' ');
                  if (re.test(t)) { el.click(); return t.slice(0, 60); }
                }
                return null;
              };
              clickMatch(/history/i);
              // session row — never match bare "orbit" (hits Orbit With Ben social cards)
              for (const el of document.querySelectorAll('button,div,[role="button"]')) {
                const t = (el.innerText || '').trim();
                const r = el.getBoundingClientRect();
                if (r.width > 120 && r.height > 24 && r.x > 900 &&
                    /untitled session|new session|^session\b|video session|cinematic/i.test(t) &&
                    t.length < 80 && !/facebook|instagram|orbit with ben/i.test(t)) {
                  el.click(); return;
                }
              }
              clickMatch(/new session|edit_square/i);
            }""",
        )
    except Exception as e:
        print(f"  ensure_agent_session race: {e}", flush=True)
        settle_after_nav(page, wait_ms=800)
    page.wait_for_timeout(1200)
    if editor_usable(page):
        return
    try:
        safe_evaluate(
            page,
            """() => {
              for (const b of document.querySelectorAll('button')) {
                const t = (b.innerText || '').trim().replace(/\\n/g, ' ');
                if (/new session|untitled session/i.test(t)) { b.click(); return; }
              }
            }""",
        )
    except Exception:
        pass
    page.wait_for_timeout(1200)


def _ensure_project_once(page) -> str:
    """Single attempt to land inside a Flow project editor."""
    force_new = os.environ.get("ORBIT_FLOW_FORCE_NEW_PROJECT", "1") not in {
        "0",
        "false",
        "False",
    }
    pinned = (os.environ.get("ORBIT_FLOW_PROJECT_URL") or "").strip()
    if pinned and "/project/" in pinned:
        if pinned.rstrip("/") not in (page.url or ""):
            print(f"  opening pinned project {pinned}", flush=True)
            page.goto(pinned, wait_until="domcontentloaded", timeout=120_000)
            settle_after_nav(page, wait_ms=2000)
            dismiss_banners(page)
        if "/project/" in (page.url or "") and editor_usable(page):
            print(f"  project ready (pinned): {page.url}", flush=True)
            return page.url
        # fall through to normal ensure if editor not ready yet
    home = FLOW_HOME_ULTRA if "u/1" in FLOW_HOME_ULTRA else FLOW_HOME
    if "/project/" not in (page.url or "") or (
        force_new and "/u/1/" not in (page.url or "")
    ):
        page.goto(home, wait_until="domcontentloaded", timeout=120_000)
        settle_after_nav(page, wait_ms=2000)
        dismiss_banners(page)
        if not looks_logged_in(page):
            raise RuntimeError(
                "Not logged into Google Flow.\n"
                "Run once with --login on the Ultra Google account:\n"
                "  python3 04_Audio/tools/orbit_flow_veo_ui.py --login"
            )
        opened = False
        if force_new and click_visible(page, "new project"):
            try:
                page.wait_for_url("**/project/**", timeout=60_000)
                opened = True
            except Exception:
                opened = "/project/" in (page.url or "")
        if not opened:
            # Prefer an existing project under /u/1/ only (AI-credit Ultra account).
            href = safe_evaluate(
                page,
                """() => {
                  const as = [...document.querySelectorAll('a[href*="/project/"]')];
                  const u1 = as.find(a => /\\/u\\/1\\/.*project\\//i.test(a.href));
                  if (u1) return u1.href;
                  const hit = as.find(a =>
                    /flow\\.google\\.com\\/.*project\\/|labs\\.google.*\\/project\\//i.test(a.href)
                  );
                  return hit ? hit.href : (as[0] ? as[0].href : null);
                }""",
            )
            if href:
                page.goto(href, wait_until="domcontentloaded", timeout=120_000)
            elif click_visible(page, "new project"):
                page.wait_for_url("**/project/**", timeout=60_000)
            else:
                raise RuntimeError("Could not find New project or existing Flow project")
        settle_after_nav(page, wait_ms=2000)
        if "flow.google.com" not in (page.url or "") and "labs.google" not in (page.url or ""):
            raise RuntimeError(f"Left Flow unexpectedly: {page.url}")
    else:
        page.wait_for_timeout(800)
    dismiss_banners(page)
    # Wait for agent prompt
    deadline = time.time() + 45
    while time.time() < deadline:
        try:
            ensure_agent_session(page)
        except Exception as e:
            if not is_transient_ui_error(e):
                raise
            settle_after_nav(page, wait_ms=800)
        if editor_usable(page):
            break
        page.wait_for_timeout(500)
    if "/project/" not in (page.url or ""):
        raise RuntimeError(f"Not in Flow project: {page.url}")
    if not editor_usable(page):
        raise RuntimeError(
            "Flow agent prompt editor not visible — open a session in the UI"
        )
    print(f"  project ready: {page.url}", flush=True)
    return page.url


def ensure_project(page, *, attempts: int = 3) -> str:
    """Land inside a Flow project editor. Retries transient SPA races."""
    last: BaseException | None = None
    for attempt in range(1, attempts + 1):
        try:
            return _ensure_project_once(page)
        except Exception as e:
            last = e
            if "not logged into google flow" in str(e).lower():
                raise
            if attempt >= attempts or not is_transient_ui_error(e):
                raise
            print(
                f"  ensure_project retry {attempt}/{attempts}: {e}",
                flush=True,
            )
            recover_flow_home(page)
    assert last is not None
    raise last


def assert_veo3_model(model: str) -> str:
    """Require a Flow Veo 3.x video model label (Lite / Fast / Quality)."""
    label = (model or "").strip()
    if any(bad.lower() in label.lower() for bad in FORBIDDEN_VIDEO_MODELS):
        raise RuntimeError(
            f"Refusing non-Veo video model {label!r}. Orbit CG must use Veo 3 "
            f"(e.g. 'Veo 3.1 - Quality'). Override: ORBIT_FLOW_VEO_MODEL=..."
        )
    if not VEO3_MODEL_RE.match(label):
        raise RuntimeError(
            f"Expected a Veo 3 model like 'Veo 3.1 - Quality', got {label!r}"
        )
    return label


def read_selected_video_model(page) -> str | None:
    """Read the currently selected Flow video-generation model label."""
    return page.evaluate(
        """() => {
          for (const b of document.querySelectorAll('button')) {
            const t = (b.innerText || '').trim().replace(/\\n/g, ' ');
            if (/Veo 3|Omni Flash/.test(t) && /arrow_drop_down/.test(t)) {
              return t.replace(/\\s*arrow_drop_down\\s*/i, '')
                .replace(/^volume_up\\s*/i, '')
                .trim();
            }
          }
          // Closed pill may show "Video · 720p · 8s" — open state is authoritative.
          return null;
        }"""
    )


def _ensure_create_prompt_mode(page) -> None:
    """Ensure we can configure video generation on the current Flow UI.

    Sep 2026 Flow (`flow.google.com`): generation defaults live under the Agent
    panel Settings (tune) sheet — there is no separate Create/Agent toggle or
    prompt-bar Veo pill. Opening Settings and seeing the video model dropdown
    is enough to proceed.
    """
    # Legacy prompt-bar pill still present on some sessions.
    has_pill = page.evaluate(
        """() => [...document.querySelectorAll('button')].some(b =>
          /Nano Banana|Video ·|Omni Flash|Omni 1|Veo 3|crop_16_9/.test(b.innerText || ''))"""
    )
    if has_pill:
        return
    # New Agent Settings sheet
    try:
        page.get_by_role("button", name="Settings", exact=True).click(timeout=4000)
        page.wait_for_timeout(900)
    except Exception:
        # Fallback: material "tune" icon button near the prompt
        page.evaluate(
            """() => {
              for (const b of document.querySelectorAll('button')) {
                const aria = (b.getAttribute('aria-label') || '').trim();
                const t = (b.innerText || '').trim();
                if (aria === 'Settings' || t === 'tune') { b.click(); return true; }
              }
              return false;
            }"""
        )
        page.wait_for_timeout(900)
    has_video_dd = page.evaluate(
        """() => [...document.querySelectorAll('button')].some(b => {
          const t = (b.innerText || '');
          return /arrow_drop_down/i.test(t) && /(Omni|Veo 3)/i.test(t);
        })"""
    )
    if has_video_dd:
        # Leave sheet open for configure_veo_settings; caller will Save/close.
        return
    # Close and fail clearly
    try:
        page.keyboard.press("Escape")
    except Exception:
        pass
    raise RuntimeError(
        "Flow video model settings not found. Open Agent Settings (tune) and "
        "confirm Video generation default shows Omni/Veo."
    )
def _open_prompt_settings_pill(page) -> None:
    """Click the prompt-bar settings pill (Nano Banana / Video · / Omni / Veo)."""
    box = page.evaluate(
        """() => {
          for (const b of document.querySelectorAll('button')) {
            const t = (b.innerText || '');
            if (/Nano Banana|Video ·|Omni Flash|Veo 3|crop_16_9/.test(t)) {
              const r = b.getBoundingClientRect();
              if (r.width > 40 && r.height > 16)
                return { x: r.x + r.width / 2, y: r.y + r.height / 2, t: t.trim().slice(0, 80) };
            }
          }
          return null;
        }"""
    )
    if not box:
        raise RuntimeError("Flow prompt settings pill not found")
    page.mouse.click(box["x"], box["y"])
    page.wait_for_timeout(900)


def _select_video_tab(page) -> None:
    """Select the Video tab inside the prompt settings popover (not Image/Nano Banana)."""
    tabs = page.evaluate(
        """() => [...document.querySelectorAll('button[role=tab]')].map(b => {
          const r = b.getBoundingClientRect();
          return {
            t: (b.innerText || '').trim(),
            sel: b.getAttribute('aria-selected'),
            x: r.x + r.width / 2,
            y: r.y + r.height / 2,
          };
        }).filter(b => /Image|Video/i.test(b.t))"""
    )
    video = next((t for t in (tabs or []) if "Video" in t["t"]), None)
    if not video:
        # Popover may already be on video-only chrome (Omni/Veo dropdown visible)
        if page.locator("button").filter(has_text="Omni Flash").count() or page.locator(
            "button"
        ).filter(has_text="Veo 3").count():
            return
        raise RuntimeError("Flow Image/Video tabs not found in settings popover")
    if video.get("sel") != "true":
        # JS click often fails to flip aria-selected — use mouse.
        page.mouse.click(video["x"], video["y"])
        page.wait_for_timeout(900)


def _select_veo_from_dropdown(page, model: str) -> str:
    """Open Omni/Veo dropdown and pick the requested Veo 3.x model."""
    dd = page.locator("button").filter(has_text="arrow_drop_down")
    # Prefer the video-model dropdown (Omni Flash / Veo 3.x)
    model_dd = page.locator("button").filter(has_text="Omni Flash").filter(
        has_text="arrow_drop_down"
    )
    if model_dd.count() == 0:
        model_dd = page.locator("button").filter(has_text="Veo 3").filter(
            has_text="arrow_drop_down"
        )
    if model_dd.count() == 0:
        model_dd = dd
    if model_dd.count() == 0:
        raise RuntimeError("Flow video model dropdown not found")

    current = (model_dd.last.inner_text() or "").replace("\n", " ")
    if model not in current:
        model_dd.last.click(timeout=5000, force=True)
        page.wait_for_timeout(800)
        item = page.get_by_role("menuitem", name=re.compile(re.escape(model), re.I))
        if item.count() == 0:
            item = page.locator(f'[role="menuitem"]:has-text("{model}")')
        if item.count() == 0:
            # Menuitem text may include a leading volume_up icon glyph
            clicked = page.evaluate(
                """(model) => {
                  const needle = String(model || '').toLowerCase();
                  for (const el of document.querySelectorAll('[role=menuitem],button')) {
                    const t = (el.innerText || '').trim().replace(/\\n/g, ' ');
                    if (t.length < 80 && t.toLowerCase().includes(needle)) {
                      el.click();
                      return t;
                    }
                  }
                  return null;
                }""",
                model,
            )
            if not clicked:
                raise RuntimeError(f"Veo 3 model menu item not found: {model}")
        else:
            item.first.click(timeout=5000, force=True)
        page.wait_for_timeout(500)

    selected = read_selected_video_model(page) or ""
    if "Veo 3" not in selected:
        selected = (model_dd.last.inner_text() or "").replace("\n", " ")
        selected = re.sub(r"\s*arrow_drop_down\s*", " ", selected, flags=re.I).strip()
        selected = re.sub(r"^volume_up\s*", "", selected, flags=re.I).strip()
    if "Veo 3" not in selected:
        raise RuntimeError(
            f"Flow video model is still {selected!r} — must be Veo 3.x "
            f"(not Omni Flash / Nano Banana)"
        )
    return selected


def _set_video_aspect_and_outputs(
    page, *, frames_mode: bool = False, ingredients_mode: bool = False
) -> None:
    """Prefer 16:9 and x1; Frames or Ingredients for I2V when requested.

    Mouse-click tabs — JS el.click() often fails to flip aria-selected here
    (same bug as the Image/Video tab).
    """

    def _mouse_click_match(kind: str) -> str | None:
        box = page.evaluate(
            """(kind) => {
              for (const b of document.querySelectorAll('button')) {
                const t = (b.innerText || '').trim().replace(/\\n/g, ' ');
                let ok = false;
                if (kind === 'frames') ok = /crop_free|\\bFrames\\b/i.test(t) && t.length < 40;
                else if (kind === 'ingredients') ok = /Ingredients|chrome_extension/i.test(t) && t.length < 50;
                else if (kind === '16:9') ok = /crop_16_9/.test(t) || /\\b16:9\\b/.test(t);
                else if (kind === '8s') ok = t === '8s';
                else if (kind === 'x1') ok = t === 'x1';
                if (!ok) continue;
                const r = b.getBoundingClientRect();
                if (r.width < 8 || r.height < 8) continue;
                return { x: r.x + r.width / 2, y: r.y + r.height / 2, t };
              }
              return null;
            }""",
            kind,
        )
        if not box:
            return None
        page.mouse.click(box["x"], box["y"])
        page.wait_for_timeout(350)
        return box.get("t")

    if frames_mode:
        _mouse_click_match("frames")
    elif ingredients_mode:
        _mouse_click_match("ingredients")

    _mouse_click_match("16:9")
    _mouse_click_match("8s")
    clicked_x1 = _mouse_click_match("x1")
    print(f"  outputs clicked x1={clicked_x1!r}", flush=True)


def configure_veo_settings(
    page,
    *,
    model: str = DEFAULT_MODEL,
    frames_mode: bool = False,
    ingredients_mode: bool = False,
) -> None:
    """Lock Flow video defaults to Veo 3.x · 16:9 · x1 via Agent Settings.

    Sep 2026 UI: Settings (tune) sheet → Video generation default → Save.
    Legacy prompt-bar pill path kept as fallback.
    """
    model = assert_veo3_model(model)
    dismiss_banners(page)

    def _open_agent_settings() -> bool:
        try:
            page.get_by_role("button", name="Settings", exact=True).click(timeout=4000)
            page.wait_for_timeout(900)
        except Exception:
            opened = page.evaluate(
                """() => {
                  for (const b of document.querySelectorAll('button')) {
                    const aria = (b.getAttribute('aria-label') || '').trim();
                    const t = (b.innerText || '').trim();
                    if (aria === 'Settings' || t === 'tune') { b.click(); return true; }
                  }
                  return false;
                }"""
            )
            if not opened:
                return False
            page.wait_for_timeout(900)
        return page.evaluate(
            r"""() => [...document.querySelectorAll('button')].some(b => {
              const t = (b.innerText || '');
              return /arrow_drop_down/i.test(t) && /(Omni|Veo 3)/i.test(t);
            })"""
        )

    def _agent_settings_path() -> str:
        if not _open_agent_settings():
            raise RuntimeError("Agent Settings sheet not available")
        # Prefer Never for confirm-before-generate so mint can run unattended.
        page.evaluate(
            r"""() => {
              for (const b of document.querySelectorAll('button,label,span,div')) {
                const t = (b.innerText || '').trim().replace(/\n/g, ' ');
                if (t === 'Never') { b.click(); return true; }
              }
              return false;
            }"""
        )
        page.wait_for_timeout(200)
        # Video section: 16:9 + x1 (lower controls). Avoid regex word-boundaries.
        page.evaluate(
            r"""() => {
              const btns = [...document.querySelectorAll('button')];
              for (const b of btns) {
                const t = (b.innerText || '').trim().replace(/\n/g, ' ');
                const r = b.getBoundingClientRect();
                if (r.y > 450 && (t.includes('crop_16_9') || t.includes('16:9'))) b.click();
              }
              const x1 = btns.filter((b) => (b.innerText || '').trim() === 'x1');
              if (x1.length >= 2) x1[x1.length - 1].click();
              else if (x1.length === 1) x1[0].click();
            }"""
        )
        page.wait_for_timeout(250)
        # Video model dropdown (lower Omni/Veo control)
        box = page.evaluate(
            r"""() => {
              const hits = [];
              for (const b of document.querySelectorAll('button')) {
                const t = (b.innerText || '').trim();
                const r = b.getBoundingClientRect();
                if (/arrow_drop_down/i.test(t) && /(Omni|Veo 3)/i.test(t) && r.width > 40)
                  hits.push({x: r.x + r.width / 2, y: r.y + r.height / 2, t: t.slice(0, 80), y0: r.y});
              }
              hits.sort((a, b) => b.y0 - a.y0);
              return hits[0] || null;
            }"""
        )
        if not box:
            raise RuntimeError("Video model dropdown not found in Agent Settings")
        page.mouse.click(box["x"], box["y"])
        page.wait_for_timeout(900)
        clicked = page.evaluate(
            r"""(model) => {
              const needle = String(model || '').toLowerCase();
              for (const el of document.querySelectorAll('[role=menuitem],button,mat-option,[role=option]')) {
                const t = (el.innerText || '').trim().replace(/\n/g, ' ');
                if (t.length < 80 && t.toLowerCase().includes(needle)) {
                  el.click();
                  return t;
                }
              }
              return null;
            }""",
            model,
        )
        if not clicked:
            raise RuntimeError(f"Veo model menu item not found: {model}")
        page.wait_for_timeout(400)
        saved = page.evaluate(
            """() => {
              for (const b of document.querySelectorAll('button')) {
                const t = (b.innerText || '').trim();
                if (t === 'Save' || t.startsWith('Save')) { b.click(); return 'save'; }
              }
              return null;
            }"""
        )
        if not saved:
            page.keyboard.press("Escape")
            saved = "escape"
        page.wait_for_timeout(700)
        print(f"  agent-settings video model locked: {clicked} ({saved})", flush=True)
        return clicked

    # Prefer Agent Settings (current Flow home UI).
    try:
        selected = _agent_settings_path()
        print(f"  video model locked: {selected}", flush=True)
        return
    except Exception as e:
        print(f"  agent-settings path failed ({e}); trying prompt pill…", flush=True)
        try:
            page.keyboard.press("Escape")
        except Exception:
            pass
        page.wait_for_timeout(400)

    # Agent UI (Sep 2026): skip slow legacy Image/Video tab lock — it hangs on
    # /u/1/ projects. Force x1 on the bottom Video pill and continue.
    if "/u/1/" in (page.url or "") or "flow.google.com" in (page.url or ""):
        print("  Agent UI: skip legacy settings lock; force x1 only", flush=True)
        force_outputs_x1(page)
        try:
            page.keyboard.press("Escape")
        except Exception:
            pass
        return

    # Legacy prompt-bar popover path — soft-fail on Sep 2026 Agent UI
    # (new /u/1/ projects expose "Video · 720p · 8s · xN" pill, not Image/Video tabs).
    try:
        _ensure_create_prompt_mode(page)
        _open_prompt_settings_pill(page)
        _select_video_tab(page)
        selected = _select_veo_from_dropdown(page, model)
        _set_video_aspect_and_outputs(
            page, frames_mode=frames_mode, ingredients_mode=ingredients_mode
        )
        print(f"  video model locked: {selected}", flush=True)
        page.keyboard.press("Escape")
        page.wait_for_timeout(500)
        print("  settings closed via escape (prompt pill)", flush=True)
        return
    except Exception as e:
        print(
            f"  WARN Veo settings lock soft-fail ({e}); continuing with UI defaults",
            flush=True,
        )
        try:
            page.keyboard.press("Escape")
        except Exception:
            pass
        # Best-effort: open bottom "Video · … · x2" pill and force x1 / 16:9.
        try:
            hit = page.evaluate(
                """() => {
                  const btns = [...document.querySelectorAll('button,[role="button"]')];
                  const pill = btns.find(b => /Video\\s*·|720p|1080p/i.test(b.innerText||''));
                  if (pill) { pill.click(); return (pill.innerText||'').slice(0,80); }
                  return null;
                }"""
            )
            if hit:
                print(f"  opened video pill: {hit!r}", flush=True)
                page.wait_for_timeout(700)
                page.evaluate(
                    """() => {
                      const clickExact = (label) => {
                        for (const b of document.querySelectorAll('button,[role="button"]')) {
                          const t = (b.innerText || '').trim();
                          if (t === label) { b.click(); return true; }
                        }
                        return false;
                      };
                      clickExact('x1');
                      clickExact('16:9');
                      clickExact('Landscape');
                    }"""
                )
                page.keyboard.press("Escape")
                page.wait_for_timeout(400)
        except Exception as e2:
            print(f"  video pill tweak skipped: {e2}", flush=True)



def upload_orbit_ref(page, ref: Path) -> bool:
    """Upload Orbit reference into the project media library (backup)."""
    if not ref.exists():
        raise FileNotFoundError(ref)
    if not click_visible(page, "add media"):
        raise RuntimeError("Add Media button not found")
    page.wait_for_timeout(600)
    up = page.locator('button:has-text("Upload media")')
    if up.count():
        with page.expect_file_chooser(timeout=10_000) as fc:
            up.first.click()
        fc.value.set_files(str(ref))
    else:
        fi = page.locator('input[type="file"]')
        if fi.count() == 0:
            raise RuntimeError("No Upload media control / file input")
        fi.first.set_input_files(str(ref))
    page.wait_for_timeout(3500)
    page.keyboard.press("Escape")
    page.wait_for_timeout(400)
    return True


def _prompt_attachment_count(page) -> int:
    """Count image chips near the agent prompt editor (not the whole page)."""
    return page.evaluate(
        """() => {
          const ed = document.querySelector('[data-slate-editor="true"]');
          if (!ed) return 0;
          const er = ed.getBoundingClientRect();
          // Attachment chips sit just above the slate editor in the composer.
          return [...document.querySelectorAll('img')].filter(i => {
            const r = i.getBoundingClientRect();
            if (r.width < 24 || r.height < 24 || r.width > 200) return false;
            // Exclude avatar / header chrome
            if (r.y < 60) return false;
            const nearY = r.y >= er.y - 280 && r.bottom <= er.bottom + 100;
            const nearX = r.x >= er.x - 60 && r.x <= er.right + 60;
            const src = i.currentSrc || i.src || '';
            const isMedia = /media\\.getMediaUrlRedirect|blob:|data:image/i.test(src);
            return nearY && nearX && isMedia;
          }).length;
        }"""
    )


def _assert_orbit_identity_ref(ref: Path) -> Path:
    """Refuse quarantine / redesign plates as Orbit identity refs."""
    p = ref.resolve()
    bad_markers = ("_rejected", "orbit-cg-canonical", "flow-ingredient-plain")
    low = str(p).lower()
    if any(m in low for m in bad_markers):
        raise RuntimeError(
            f"Refused off-model Orbit plate: {p}\n"
            "Use orbit-seedance-reference-16x9-v01.png (legacy filename — "
            "identity still only; CG engine is Flow Veo, not Seedance)."
        )
    if "seedance-reference" not in low and "orbit-seedance" not in low:
        print(
            f"  warn: unexpected Orbit identity ref name: {p.name}",
            flush=True,
        )
    return p

# Back-compat alias
_assert_seedance_ref = _assert_orbit_identity_ref


def _open_create_picker(page) -> None:
    """Open the prompt '+' / Create asset picker."""
    ensure_agent_session(page)
    clicked = page.evaluate(
        """() => {
          const ed = document.querySelector('[data-slate-editor="true"]');
          const er = ed ? ed.getBoundingClientRect() : {y: 700, bottom: 900};
          for (const i of document.querySelectorAll('i.google-symbols, span.google-symbols')) {
            const t = (i.textContent || '').trim();
            if (t !== 'add_2' && t !== 'add') continue;
            const b = i.closest('button');
            if (!b) continue;
            const r = b.getBoundingClientRect();
            if (r.y >= er.y - 160 && r.y <= er.bottom + 120) {
              b.click();
              return true;
            }
          }
          return false;
        }"""
    )
    if not clicked:
        btn = page.locator('button:has-text("add_2")')
        if btn.count():
            btn.first.click(timeout=5000)
    page.wait_for_timeout(700)


def _wait_add_to_prompt_enabled(page, *, timeout_s: float = 90) -> bool:
    """Wait until Flow finishes processing the upload and enables Add to Prompt."""
    t0 = time.time()
    while time.time() - t0 < timeout_s:
        st = page.evaluate(
            """() => {
              const btns = [...document.querySelectorAll('button')].filter(b =>
                /^Add to Prompt$/i.test((b.innerText || '').trim())
              );
              if (!btns.length) return {found: false};
              const b = btns[btns.length - 1];
              const disabled =
                b.disabled ||
                b.getAttribute('aria-disabled') === 'true' ||
                /disabled/i.test(b.className || '');
              return {found: true, disabled};
            }"""
        )
        if st.get("found") and not st.get("disabled"):
            return True
        page.wait_for_timeout(1500)
    return False


def attach_image_to_prompt(page, ref: Path) -> bool:
    """Attach an arbitrary still to the Flow agent prompt (HOS start-frame I2V).

    Same upload path as Orbit identity attach, without Orbit filename asserts.
    """
    ref = Path(ref).resolve()
    if not ref.exists():
        raise FileNotFoundError(ref)
    ensure_agent_session(page)
    before = _prompt_attachment_count(page)
    print(f"  attaching start frame: {ref.name}", flush=True)

    _open_create_picker(page)

    uploads_tab = page.locator('button:has-text("Uploads")')
    if uploads_tab.count():
        try:
            uploads_tab.first.click(timeout=3000)
            page.wait_for_timeout(400)
        except Exception:
            pass

    up = page.locator('button:has-text("Upload media")')
    if up.count() == 0:
        page.keyboard.press("Escape")
        page.wait_for_timeout(400)
        _open_create_picker(page)
        page.wait_for_timeout(600)
        up = page.locator('button:has-text("Upload media")')
    if up.count() == 0:
        up = page.locator('button:has-text("Upload")')
    if up.count() == 0:
        raise RuntimeError("Upload media not found in Create picker")

    try:
        with page.expect_file_chooser(timeout=12_000) as fc:
            up.last.click(force=True)
        fc.value.set_files(str(ref))
    except Exception:
        fi = page.locator('input[type="file"]')
        if fi.count() == 0:
            raise RuntimeError("Could not upload start frame to Create picker")
        fi.last.set_input_files(str(ref))

    print("  uploaded — waiting for Add to Prompt…", flush=True)
    if not _wait_add_to_prompt_enabled(page, timeout_s=90):
        raise RuntimeError(
            "Flow never enabled Add to Prompt after start-frame upload"
        )

    # Prefer selecting the just-uploaded asset by filename stem when possible
    stem = ref.stem.lower()[:24]
    page.evaluate(
        """(stem) => {
          for (const el of document.querySelectorAll('div,button,li,[role="option"]')) {
            const t = (el.innerText || '').trim().toLowerCase();
            if (stem && t.includes(stem) && t.length < 200) {
              try { el.click(); } catch (e) {}
              return true;
            }
          }
          return false;
        }""",
        stem,
    )
    page.wait_for_timeout(400)
    add = page.locator('button:has-text("Add to Prompt")')
    if add.count() == 0:
        raise RuntimeError("Add to Prompt button missing")
    add.last.click(force=True)
    page.wait_for_timeout(1500)

    for _ in range(2):
        body = ""
        try:
            body = page.locator("body").inner_text(timeout=2000)[:2500]
        except Exception:
            pass
        if "Add to Prompt" in body or "Search assets" in body or "Upload media" in body:
            page.keyboard.press("Escape")
            page.wait_for_timeout(500)
        else:
            break

    ensure_agent_session(page)
    attached = _prompt_attachment_count(page) > before
    if not attached:
        page.wait_for_timeout(2000)
        attached = _prompt_attachment_count(page) > before

    print(f"  prompt attachment visible={attached} (was {before})", flush=True)
    if not attached:
        raise RuntimeError(
            "Start frame did not attach to the Flow prompt — aborting."
        )
    return True


def attach_orbit_to_prompt(page, ref: Path) -> bool:
    """Attach Orbit identity still into the agent prompt (required for identity).

    CG engine is Google Flow Veo — not Seedance. The still file may still be
    named orbit-seedance-reference-*.png (legacy path only).

    Flow path that works (2026-08):
      + Create → Upload media → wait until thumbnail ready → **Add to Prompt**

    Library-only / header Add Media is not enough. Aborts if no prompt chip.
    """
    ref = _assert_orbit_identity_ref(ref)
    if not ref.exists():
        raise FileNotFoundError(ref)
    ensure_agent_session(page)
    before = _prompt_attachment_count(page)
    print(f"  attaching Orbit ref: {ref.name}", flush=True)

    _open_create_picker(page)

    uploads_tab = page.locator('button:has-text("Uploads")')
    if uploads_tab.count():
        try:
            uploads_tab.first.click(timeout=3000)
            page.wait_for_timeout(400)
        except Exception:
            pass

    up = page.locator('button:has-text("Upload media")')
    if up.count() == 0:
        # Picker may not have opened — retry once
        page.keyboard.press("Escape")
        page.wait_for_timeout(400)
        _open_create_picker(page)
        page.wait_for_timeout(600)
        up = page.locator('button:has-text("Upload media")')
    if up.count() == 0:
        up = page.locator('button:has-text("Upload")')
    if up.count() == 0:
        # Last resort: any visible file input after forcing Add Media header
        try:
            upload_orbit_ref(page, ref)
        except Exception:
            pass
        _open_create_picker(page)
        page.wait_for_timeout(800)
        up = page.locator('button:has-text("Upload media")')
    if up.count() == 0:
        raise RuntimeError("Upload media not found in Create picker")

    try:
        with page.expect_file_chooser(timeout=12_000) as fc:
            up.last.click(force=True)
        fc.value.set_files(str(ref))
    except Exception:
        fi = page.locator('input[type="file"]')
        if fi.count() == 0:
            raise RuntimeError("Could not upload Orbit to Create picker")
        fi.last.set_input_files(str(ref))

    print("  uploaded — waiting for Add to Prompt…", flush=True)
    if not _wait_add_to_prompt_enabled(page, timeout_s=90):
        raise RuntimeError(
            "Flow never enabled Add to Prompt after Orbit upload "
            "(thumbnail still processing?)"
        )

    page.evaluate(
        """() => {
          const name = 'orbit-seedance';
          for (const el of document.querySelectorAll('div,button,li,[role="option"]')) {
            const t = (el.innerText || '').trim();
            if (t.toLowerCase().includes(name) && t.length < 160) {
              try { el.click(); } catch (e) {}
              return true;
            }
          }
          return false;
        }"""
    )
    page.wait_for_timeout(400)
    add = page.locator('button:has-text("Add to Prompt")')
    if add.count() == 0:
        raise RuntimeError("Add to Prompt button missing")
    add.last.click(force=True)
    page.wait_for_timeout(1500)

    for _ in range(2):
        body = ""
        try:
            body = page.locator("body").inner_text(timeout=2000)[:2500]
        except Exception:
            pass
        if "Add to Prompt" in body or "Search assets" in body or "Upload media" in body:
            page.keyboard.press("Escape")
            page.wait_for_timeout(500)
        else:
            break

    ensure_agent_session(page)
    attached = _prompt_attachment_count(page) > before
    if not attached:
        page.wait_for_timeout(2000)
        attached = _prompt_attachment_count(page) > before

    print(f"  prompt attachment visible={attached} (was {before})", flush=True)
    if not attached:
        raise RuntimeError(
            "Orbit identity reference did not attach to the Flow prompt — aborting "
            "to avoid off-model mascot generation. Confirm Add to Prompt produced "
            "an image chip above the prompt before Create."
        )
    return True


def ensure_orbit_agent_instruction(page) -> None:
    """Install a persistent Agent Instruction for Orbit identity (once per session)."""
    ensure_agent_session(page)
    opened = page.evaluate(
        """() => {
          for (const b of document.querySelectorAll('button,[role="button"]')) {
            const t = (b.innerText || '').trim().replace(/\\n/g, ' ');
            if (/agent instructions|article_spark/i.test(t)) { b.click(); return t.slice(0,40); }
          }
          return null;
        }"""
    )
    if not opened:
        print("  warn: Agent Instructions not found", flush=True)
        return
    print(f"  agent instructions open ({opened!r})", flush=True)
    page.wait_for_timeout(800)
    body = ""
    try:
        body = page.locator("body").inner_text(timeout=3000)
    except Exception:
        pass
    if "ORBIT IDENTITY LOCK" in body:
        page.evaluate(
            """() => {
              for (const b of document.querySelectorAll('button')) {
                const t = (b.innerText || '').trim();
                if (/^Done$/i.test(t) || /^Close$/i.test(t)) { b.click(); return; }
              }
            }"""
        )
        page.wait_for_timeout(400)
        print("  Orbit Agent Instruction already present", flush=True)
        return

    added = page.evaluate(
        """() => {
          for (const b of document.querySelectorAll('button')) {
            const t = (b.innerText || '').trim().replace(/\\n/g, ' ');
            if (/add instruction/i.test(t)) { b.click(); return true; }
          }
          return false;
        }"""
    )
    if not added:
        print("  warn: Add Instruction not found", flush=True)
        page.keyboard.press("Escape")
        return
    page.wait_for_timeout(500)
    # Paste is much faster/safer than keyboard.type for long locks
    page.keyboard.insert_text(ORBIT_AGENT_INSTRUCTION)
    page.wait_for_timeout(300)
    page.evaluate(
        """() => {
          for (const b of document.querySelectorAll('button')) {
            const t = (b.innerText || '').trim();
            if (/^Done$/i.test(t)) { b.click(); return; }
          }
        }"""
    )
    page.wait_for_timeout(600)
    print("  Orbit Agent Instruction saved", flush=True)


def flow_prompt(
    scene_prompt: str,
    *,
    scenery_only: bool = False,
    start_frame_i2v: bool = False,
) -> str:
    """Wrap a scene prompt for Flow.

    Keep this short — Agent Instruction already holds the full identity lock.
    Long typed prompts stall Playwright and desync the Create picker.
    """
    body = scene_prompt.strip()
    if "IMAGE-TO-VIDEO" in body or "ORBIT IDENTITY LOCK" in body:
        return body
    if start_frame_i2v:
        return (
            f"IMAGE-TO-VIDEO of the attached start frame. Animate THIS exact scene — "
            f"keep composition, characters, and lighting. Continuous camera/subject "
            f"motion through the final frame. {body} Silent picture only. No text, no logos."
        )
    if scenery_only:
        return (
            f"{body} "
            "SCENERY ONLY — no characters, no robots, no mascots, no text. "
            "Silent picture only."
        )
    return (
        f"{FLOW_I2V_PREFACE} {body} "
        "Match the attached Orbit identity image exactly. Silent picture only."
    )


_PLACEHOLDER_RE = re.compile(
    r"^what do you want to create\??$|^what would you like to create\??$|"
    r"^hi\b.*create\??$|^describe|^enter a prompt|^prompt$|^start creating",
    re.I,
)

_EDITOR_TEXT_JS = """() => {
  const score = (el) => {
    if (!el) return null;
    const r = el.getBoundingClientRect();
    if (r.width < 40 || r.height < 10) return null;
    const aria = (el.getAttribute('aria-label') || '').toLowerCase();
    const ph = (el.getAttribute('placeholder') || '').toLowerCase();
    const t = (el.innerText || el.textContent || '').toLowerCase();
    const hint = aria + ' ' + ph + ' ' + t.slice(0, 80);
    let s = r.width * Math.max(r.height, 24);
    if (r.x > 900) s += 20000;
    if (/what do you want|what would you like|create\\?|prompt|describe/i.test(hint)) s += 50000;
    if ((el.className || '').toString().includes('ProseMirror')) s += 45000;
    if (el.getAttribute('data-slate-editor') === 'true') s += 40000;
    if (el.getAttribute('contenteditable') === 'true') s += 10000;
    if ((el.getAttribute('role') || '') === 'textbox') s += 8000;
    if (el.tagName === 'TEXTAREA') s += 6000;
    return {el, s};
  };
  const cands = [];
  for (const sel of [
    '.ProseMirror[contenteditable="true"]',
    '[data-slate-editor="true"]',
    '[contenteditable="true"]',
    'textarea',
    '[role="textbox"]',
  ]) {
    for (const el of document.querySelectorAll(sel)) {
      const hit = score(el);
      if (hit) cands.push(hit);
    }
  }
  cands.sort((a, b) => b.s - a.s);
  if (!cands.length) return '';
  const ed = cands[0].el;
  if (ed.tagName === 'TEXTAREA' || ed.tagName === 'INPUT') {
    return (ed.value || '').trim();
  }
  // Strip ProseMirror placeholder widgets so empty editors don't look filled.
  const clone = ed.cloneNode(true);
  clone.querySelectorAll(
    '.prosemirror-placeholder, .ProseMirror-placeholder, .ProseMirror-widget, [data-placeholder]'
  ).forEach((n) => n.remove());
  let out = (clone.innerText || clone.textContent || '').trim();
  // Placeholder decorations sometimes leave the question as plain text.
  const q = ['what do you want to create', 'what would you like to create'];
  const low = out.toLowerCase().replace(new RegExp('[?]+$'), '');
  if (q.includes(low)) return '';
  return out;
}"""


def _editor_prompt_text(page) -> str:
    """Return real editor text. Flow's placeholder must not count as a prompt."""
    raw = page.evaluate(_EDITOR_TEXT_JS) or ""
    stripped = raw.strip()
    if _PLACEHOLDER_RE.match(stripped):
        return ""
    if stripped.lower() in {
        "what do you want to create?",
        "what do you want to create",
        "what would you like to create?",
    }:
        return ""
    return stripped


def _clear_editor(page) -> None:
    """Wipe placeholder + leftover prompt text. Do not click the image chip."""
    for combo in (("Meta+A", "Backspace"), ("Control+A", "Backspace")):
        page.evaluate(_FOCUS_PROMPT_EDITOR_JS)
        page.keyboard.press(combo[0])
        page.keyboard.press(combo[1])
        page.wait_for_timeout(80)
    leftover = _editor_prompt_text(page)
    if leftover.lower().startswith("what do you want"):
        page.keyboard.press("Meta+A")
        page.keyboard.press("Backspace")
        page.wait_for_timeout(80)


def set_prompt(page, prompt: str) -> None:
    """Type into the Flow agent editor without wiping an attached image chip.

    ProseMirror/Slate only arm Create on real input events. DOM writes look
    filled but leave send disabled.
    """
    ensure_agent_session(page)
    box = editor_box(page)
    if not box or not editor_usable(page):
        raise RuntimeError("Flow prompt editor not visible (open agent session)")
    # Click toward the right of the editor so we don't focus/remove the chip
    page.mouse.click(box["x"] + min(box["w"] - 40, 180), box["y"] + max(6, box["h"] / 2))
    page.wait_for_timeout(150)
    page.evaluate(_FOCUS_PROMPT_EDITOR_JS)
    _clear_editor(page)
    page.evaluate(_FOCUS_PROMPT_EDITOR_JS)
    # Playwright insert_text fires beforeinput insertText — editor consumes this.
    page.keyboard.insert_text(prompt)
    page.wait_for_timeout(450)
    got = _editor_prompt_text(page)
    dirty = got.lower().startswith("what do you want")
    ok = bool(got and (not dirty) and len(got) >= min(24, max(12, len(prompt) // 8)))
    print(f"  set_prompt insert_text chars={len(got)} dirty={dirty} head={got[:40]!r}", flush=True)
    if not ok:
        page.evaluate(_FOCUS_PROMPT_EDITOR_JS)
        _clear_editor(page)
        page.evaluate(_FOCUS_PROMPT_EDITOR_JS)
        page.keyboard.type(prompt, delay=3)
        page.wait_for_timeout(300)
        got = _editor_prompt_text(page)
        dirty = got.lower().startswith("what do you want")
        ok = bool(got and (not dirty) and len(got) >= min(24, max(12, len(prompt) // 8)))
        print(f"  set_prompt type fallback chars={len(got)} dirty={dirty}", flush=True)
    if not ok:
        raise RuntimeError(
            f"Flow prompt editor not armed after input events head={got[:80]!r}"
        )
    print(f"  set_prompt ok head={got[:60]!r}", flush=True)


def _flow_info_tooltip(page) -> str:
    """Hover the orange info chip next to Create and return tooltip / title."""
    try:
        tip = page.evaluate(
            """() => {
              const btns = [...document.querySelectorAll('button,[role="button"],[aria-label]')];
              for (const b of btns) {
                const t = (b.innerText || b.getAttribute('aria-label') || '')
                  .trim().replace(/\\n/g, ' ');
                if (/^info$|priority_high|error/i.test(t) && t.length < 40) {
                  const r = b.getBoundingClientRect();
                  if (r.y > 500) {
                    return {
                      t,
                      title: b.getAttribute('title') || b.getAttribute('aria-label') || '',
                      x: r.x + r.width / 2,
                      y: r.y + r.height / 2,
                    };
                  }
                }
              }
              return null;
            }"""
        )
        if not tip:
            return ""
        page.mouse.move(tip["x"], tip["y"])
        page.wait_for_timeout(600)
        extra = page.evaluate(
            """() => {
              const els = [...document.querySelectorAll(
                '[role="tooltip"],[data-state="open"],div[class*="tooltip"]'
              )];
              return els.map(e => (e.innerText || '').trim()).filter(Boolean).join(' | ');
            }"""
        )
        return " | ".join(x for x in (tip.get("t"), tip.get("title"), extra) if x)
    except Exception as e:
        return f"tooltip-err {e}"


def _dismiss_asset_search_modal(page) -> None:
    """Close Flow's Search assets / empty Uploads overlay that steals Create."""
    for _ in range(10):
        body = ""
        try:
            body = page.locator("body").inner_text(timeout=1500)[:4000]
        except Exception:
            pass
        open_picker = any(
            s in body
            for s in (
                "Asset Search",
                "Search assets",
                "Add to Prompt",
                "No results found",
            )
        )
        if not open_picker:
            return
        closed = page.evaluate(
            """() => {
              const labels = /^(close|cancel|done|dismiss)$/i;
              for (const b of document.querySelectorAll('button,[aria-label]')) {
                const t = (b.innerText || b.getAttribute('aria-label') || '')
                  .trim().replace(/\\n/g, ' ');
                if (labels.test(t) && t.length < 24) {
                  try { b.click(); return t.slice(0, 24); } catch (e) {}
                }
              }
              return null;
            }"""
        )
        if closed:
            print(f"  closed asset picker via {closed!r}", flush=True)
        else:
            page.keyboard.press("Escape")
            # Click the canvas (not the prompt plus) so the overlay loses focus
            try:
                page.mouse.click(720, 220)
            except Exception:
                pass
        page.wait_for_timeout(350)


def submit_create(page) -> None:
    """Click the prompt-bar send (arrow_forward). Never click add_2 (asset picker)."""
    _dismiss_asset_search_modal(page)

    deadline = time.time() + 45
    while time.time() < deadline:
        _dismiss_asset_search_modal(page)
        state = page.evaluate(
            """() => {
              const pick = (preferArrow) => {
                const hits = [];
                for (const b of document.querySelectorAll('button')) {
                  const t = (b.innerText || '').trim().replace(/\\n/g, ' ');
                  if (/error|cancel|add_2|show thinking|arrow_forward_ios|expand_more/i.test(t)) continue;
                  const isArrow = /(^|\\s)arrow_forward(\\s|$)/i.test(t) && !/ios|thinking/i.test(t);
                  const isCreate = /^Create$/i.test(t);
                  if (preferArrow && !isArrow) continue;
                  if (!preferArrow && !isCreate) continue;
                  if (!isArrow && !isCreate) continue;
                  const disabled =
                    b.disabled || b.getAttribute('aria-disabled') === 'true';
                  const r = b.getBoundingClientRect();
                  if (r.width < 8 || r.height < 8) continue;
                  hits.push({
                    disabled,
                    x: r.x + r.width / 2,
                    y: r.y + r.height / 2,
                    t: t.slice(0, 40),
                    arrow: isArrow,
                  });
                }
                return hits.find(h => h.arrow) || hits[0] || null;
              };
              const send = pick(true) || pick(false);
              if (send) return send;
              for (const b of document.querySelectorAll('button')) {
                const t = (b.innerText || '').trim().replace(/\\n/g, ' ');
                if (/^info$|^error$|priority_high|error\\s*cancel/i.test(t) &&
                    b.getBoundingClientRect().y > 700) {
                  return { disabled: true, blocked: t.slice(0, 40) };
                }
              }
              return null;
            }"""
        )
        if state and state.get("blocked"):
            tip = _flow_info_tooltip(page)
            raise RuntimeError(
                f"Flow Create blocked ({state['blocked']!r} tooltip={tip!r})"
            )
        if state and not state.get("disabled"):
            print(f"  clicking Flow send ({state.get('t')!r})", flush=True)
            clicked = page.evaluate(
                """() => {
                  const ranked = [];
                  for (const b of document.querySelectorAll('button')) {
                    const t = (b.innerText || '').trim().replace(/\\n/g, ' ');
                    if (/error|cancel|add_2|new project/i.test(t)) continue;
                    if (!/(^|\\s)arrow_forward(\\s|$)/i.test(t) || /ios|show thinking/i.test(t)) continue;
                    if (b.disabled || b.getAttribute('aria-disabled') === 'true') continue;
                    ranked.push(b);
                  }
                  if (ranked.length) {
                    ranked[ranked.length - 1].click();
                    return 'arrow_forward';
                  }
                  return null;
                }"""
            )
            if clicked:
                page.wait_for_timeout(800)
                return
            page.mouse.click(state["x"], state["y"])
            page.wait_for_timeout(800)
            return
        page.wait_for_timeout(500)

    tip = _flow_info_tooltip(page)
    raise RuntimeError(
        f"Flow arrow_forward send not found or never enabled tooltip={tip!r}"
    )


def dismiss_soft_prompts(page) -> None:
    """Click safe confirmations (not blanket Yes).

    Flow Ultra often shows a post-Create approval card
    ("I'm going to generate… Veo 3.1… N credits") that must be confirmed
    before generation actually starts — without this, wait only sees the
    uploaded start-frame JPEG forever.
    """
    page.evaluate(
        """() => {
          const re = /Got it|I understand|Continue|Agree|Accept|Dismiss|^OK$|Generate (the )?video|Create video|Try again|Retry|Regenerate|^Confirm$|^Generate$|^Approve$|Use \\d+ credits|Spend credits|Yes,? generate/i;
          for (const b of document.querySelectorAll('button,[role="button"],[role="menuitem"]')) {
            const t = (b.innerText || b.getAttribute('aria-label') || '')
              .trim().replace(/\\n/g, ' ');
            if (
              re.test(t) &&
              t.length < 120 &&
              !/new project|settings|add media|ultra|agent instructions|view settings|save|close|never/i.test(t)
            ) {
              try { b.click(); } catch (e) {}
            }
          }
        }"""
    )


def confirm_generation_spend(page, *, timeout_s: float = 12.0) -> bool:
    """Click the post-Create Ultra credit / model confirmation if it appears.

    Do NOT treat ambient 'AI credits' chrome as a dialog — that used to re-click
    the main Create arrow_forward and stall/resubmit forever.
    """
    deadline = time.time() + timeout_s
    clicked = False
    while time.time() < deadline:
        hit = page.evaluate(
            """() => {
              // Only act when a real confirmation dialog/sheet is visible.
              const body = (document.body && document.body.innerText) || '';
              const dialogish = /going to generate|about to generate|use \\d+ credits|spend \\d+ credits|high demand|in the queue|confirm generation/i.test(body);
              if (!dialogish) return null;
              const labels = [
                /^Confirm$/i, /^Generate$/i, /^Approve$/i, /^Continue$/i,
                /Generate (the )?video/i, /Create video/i, /Use \\d+ credits/i,
                /Spend .*credits/i, /Yes,? generate/i, /^OK$/i,
              ];
              for (const b of document.querySelectorAll('button,[role="button"]')) {
                const t = (b.innerText || b.getAttribute('aria-label') || '')
                  .trim().replace(/\\n/g, ' ');
                if (!t || t.length > 80) continue;
                // Never re-fire the composer send control.
                if (/never|cancel|dismiss|close|settings|arrow_forward|send/i.test(t)) continue;
                for (const re of labels) {
                  if (re.test(t)) {
                    try { b.click(); return t.slice(0, 60); } catch (e) {}
                  }
                }
              }
              return null;
            }"""
        )
        if hit:
            print(f"  confirmed generation spend via {hit!r}", flush=True)
            clicked = True
            page.wait_for_timeout(600)
        else:
            page.wait_for_timeout(400)
            if clicked:
                break
    return clicked


def try_context_animate(page) -> bool:
    """Right-click the latest uploaded/project still and choose Animate (HOS Flow path)."""
    hit = page.evaluate(
        """() => {
          const imgs = [...document.querySelectorAll('img,video,canvas,[role="img"]')]
            .filter((el) => {
              const r = el.getBoundingClientRect();
              return r.width > 80 && r.height > 60 && r.y > 40 && r.y < 900;
            });
          if (!imgs.length) return null;
          const el = imgs[imgs.length - 1];
          const r = el.getBoundingClientRect();
          return { x: r.x + r.width / 2, y: r.y + r.height / 2 };
        }"""
    )
    if not hit:
        return False
    page.mouse.click(hit["x"], hit["y"], button="right")
    page.wait_for_timeout(500)
    animated = page.evaluate(
        """() => {
          for (const el of document.querySelectorAll(
            'button,[role="menuitem"],[role="option"],div,span,li'
          )) {
            const t = (el.innerText || el.getAttribute('aria-label') || '')
              .trim().replace(/\\n/g, ' ');
            if (/^Animate$/i.test(t) || /\\bAnimate\\b/i.test(t) && t.length < 40) {
              try { el.click(); return t.slice(0, 40); } catch (e) {}
            }
          }
          return null;
        }"""
    )
    if animated:
        print(f"  context Animate clicked ({animated!r})", flush=True)
        page.wait_for_timeout(800)
        return True
    page.keyboard.press("Escape")
    return False


def collect_media_ids(page) -> set[str]:
    html = page.content()
    return set(MEDIA_REDIRECT_RE.findall(html))


def collect_gallery_asb_srcs(page) -> list[str]:
    """Agent UI gallery thumbnails live at flow.google.com/asb/…"""
    try:
        return page.evaluate(
            """() => [...document.querySelectorAll('img')]
              .map(i => i.currentSrc || i.src || '')
              .filter(s => /\\/asb\\//i.test(s))"""
        ) or []
    except Exception:
        return []


def force_outputs_x1(page) -> bool:
    """Force Agent UI outputs pill off x2/x3/x4 onto x1 (saves AI credits)."""
    try:
        before = page.evaluate(
            """() => {
              const btns = [...document.querySelectorAll('button,[role="button"]')];
              const pill = btns.find(b => /Video\\s*[·•]|720p|1080p|\\bx[1-4]\\b/i.test(b.innerText||''));
              return pill ? (pill.innerText || '').replace(/\\s+/g,' ').trim().slice(0,80) : '';
            }"""
        )
        page.evaluate(
            """() => {
              const btns = [...document.querySelectorAll('button,[role="button"]')];
              const pill = btns.find(b => /Video\\s*[·•]|720p|1080p|\\bx[2-4]\\b/i.test(b.innerText||''));
              if (pill) pill.click();
            }"""
        )
        page.wait_for_timeout(600)
        clicked = page.evaluate(
            """() => {
              const clickExact = (label) => {
                for (const b of document.querySelectorAll('button,[role="button"],[role="option"],div[role="menuitem"]')) {
                  const t = (b.innerText || '').trim();
                  if (t === label) { b.click(); return true; }
                }
                return false;
              };
              // Prefer explicit x1; also click "1" variants some locales use.
              return clickExact('x1') || clickExact('1');
            }"""
        )
        page.wait_for_timeout(400)
        try:
            page.keyboard.press("Escape")
        except Exception:
            pass
        page.wait_for_timeout(300)
        after = page.evaluate(
            """() => {
              const btns = [...document.querySelectorAll('button,[role="button"]')];
              const pill = btns.find(b => /Video\\s*[·•]|720p|1080p|\\bx[1-4]\\b/i.test(b.innerText||''));
              return pill ? (pill.innerText || '').replace(/\\s+/g,' ').trim().slice(0,80) : '';
            }"""
        )
        ok = bool(clicked) and ("x2" not in (after or "").lower()) and (
            "x1" in (after or "").lower() or "x2" not in (before or "").lower()
        )
        print(
            f"  force x1: clicked={clicked!r} before={before!r} after={after!r} ok={ok}",
            flush=True,
        )
        return ok
    except Exception as e:
        print(f"  force x1 skipped: {e}", flush=True)
        return False


def harvest_agent_gallery_mp4(
    page,
    dest: Path,
    captured_videos: list[bytes],
    *,
    before_asb: set[str] | None = None,
) -> str | None:
    """Play newest Agent gallery card and save the googlevideo/mp4 body.

    New Flow Agent UI never emits getMediaUrlRedirect ids. Completed clips sit
    in All media as /asb/ thumbs; playing them fires googlevideo videoplayback
    which we capture from the network listener.
    """
    before_asb = before_asb or set()
    try:
        # Prefer All media tab so thumbs are visible.
        page.evaluate(
            """() => {
              for (const n of document.querySelectorAll('button,a,[role="button"],[role="tab"]')) {
                const t = ((n.innerText || '') + ' ' + (n.getAttribute('aria-label') || '')).trim();
                if (/^All media$/i.test(t) || t === 'All media') { n.click(); return; }
              }
            }"""
        )
        page.wait_for_timeout(500)
    except Exception:
        pass

    thumbs = collect_gallery_asb_srcs(page)
    new_thumbs = [s for s in thumbs if s not in before_asb] or list(thumbs)
    if not new_thumbs:
        return None
    print(f"  gallery harvest thumbs={len(thumbs)} new={len(new_thumbs)}", flush=True)

    # Prefer the newest card (last in DOM is usually latest).
    target_src = new_thumbs[-1]
    before_n = len(captured_videos)

    # Hover card → click play; capture googlevideo via expect_response (safe).
    def _play_and_capture() -> bytes | None:
        try:
            box = page.evaluate(
                """(src) => {
                  const img = [...document.querySelectorAll('img')].find(i =>
                    (i.currentSrc || i.src || '') === src
                  );
                  if (!img) return null;
                  const r = img.getBoundingClientRect();
                  return {x:r.x, y:r.y, w:r.width, h:r.height};
                }""",
                target_src,
            )
            if not box or box.get("w", 0) <= 40:
                return None
            cx = box["x"] + box["w"] / 2
            cy = box["y"] + box["h"] / 2
            page.mouse.move(cx, cy)
            page.wait_for_timeout(350)

            def _is_vid(resp) -> bool:
                u = (resp.url or "").lower()
                ct = (resp.headers.get("content-type") or "").lower()
                return resp.status == 200 and (
                    "googlevideo.com" in u
                    or "videoplayback" in u
                    or ("video" in ct and "mp4" in ct)
                )

            with page.expect_response(_is_vid, timeout=45_000) as ri:
                page.mouse.click(box["x"] + 28, box["y"] + 28)
                page.wait_for_timeout(400)
                page.mouse.click(cx, cy)
            resp = ri.value
            body = resp.body()
            if len(body) > 150_000 and b"ftyp" in body[:64]:
                return body
        except Exception as e:
            print(f"  gallery expect_response play err: {e}", flush=True)
        return None

    raw = _play_and_capture()
    if raw is None:
        print("  gallery harvest: retry play for network mp4", flush=True)
        page.wait_for_timeout(800)
        raw = _play_and_capture()
    if raw is not None:
        captured_videos.append(raw)
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(raw)
        print(f"  gallery harvest saved bytes={len(raw)}", flush=True)
        return f"gallery-network:{len(raw)}"

    return None





def absolute_media_url(name_or_url: str) -> str:
    if name_or_url.startswith("http"):
        return name_or_url
    if name_or_url.startswith("/"):
        return urljoin("https://labs.google", name_or_url)
    return (
        "https://labs.google/fx/api/trpc/media.getMediaUrlRedirect?name="
        + name_or_url
    )


def download_media(page, name_or_url: str, dest: Path) -> int:
    url = absolute_media_url(name_or_url)
    resp = page.request.get(url, timeout=180_000)
    if resp.status != 200:
        raise RuntimeError(f"media download HTTP {resp.status}: {url[:120]}")
    data = resp.body()
    ct = (resp.headers.get("content-type") or "").lower()
    if "video" not in ct and not data[:12].startswith(b"\x00\x00\x00"):
        # Still allow if large enough binary
        if len(data) < 200_000:
            raise RuntimeError(
                f"Unexpected media type {ct!r} size={len(data)} for {url[:120]}"
            )
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(data)
    return len(data)


def wait_and_download(
    page,
    dest: Path,
    *,
    before_ids: set[str],
    timeout_s: int = 900,
    min_elapsed_s: float = 0,
) -> str:
    """Wait for a new Flow media video and download it. Returns media id/url."""
    t0 = time.time()
    last_status = ""
    asked_status = False
    failed_since: float | None = None
    retry_clicks = 0
    seen_generating = False
    # Do NOT permanently blacklist early media ids — Flow often reuses the same
    # getMediaUrlRedirect name from a placeholder/upload into the finished mp4.
    early_gate_s = max(5.0, float(min_elapsed_s or 0) * 0.35)
    captured_videos: list[bytes] = []
    before_asb = set(collect_gallery_asb_srcs(page))
    gallery_tries = 0
    last_gallery_try = 0.0

    def _on_response(resp) -> None:
        try:
            ct = (resp.headers.get("content-type") or "").lower()
            url = (resp.url or "").lower()
            # NEVER body()-read googlevideo streams here — that crashes Chrome.
            # Gallery harvest uses expect_response around play instead.
            if "googlevideo.com" in url or "videoplayback" in url:
                return
            if not (
                "video" in ct
                or url.endswith(".mp4")
                or "getmediaurlredirect" in url
            ):
                return
            if resp.status != 200:
                return
            cl = resp.headers.get("content-length")
            if cl and cl.isdigit() and int(cl) < 150_000:
                return
            body = resp.body()
            if len(body) > 150_000 and (b"ftyp" in body[:64] or "video" in ct):
                captured_videos.append(body)
                print(
                    f"  network captured video bytes={len(body)} ct={ct[:40]}",
                    flush=True,
                )
        except Exception:
            pass

    try:
        page.on("response", _on_response)
    except Exception:
        pass
    while time.time() - t0 < timeout_s:
        # Stay on Flow — profile sometimes drifts to Facebook/Threads overlays.
        url = page.url or ""
        if "flow.google.com" not in url and "labs.google" not in url:
            print(f"  left Flow ({url[:80]}) — recovering…", flush=True)
            recover_to = getattr(page, "_orbit_flow_project_url", None) or FLOW_HOME_ULTRA
            # Never force a brand-new project during recover — that abandons in-flight gens.
            prev_force = os.environ.get("ORBIT_FLOW_FORCE_NEW_PROJECT")
            os.environ["ORBIT_FLOW_FORCE_NEW_PROJECT"] = "0"
            try:
                page.goto(recover_to, wait_until="domcontentloaded", timeout=60_000)
                dismiss_banners(page)
                if "/project/" not in (page.url or ""):
                    ensure_project(page)
            except Exception as e:
                print(f"  Flow recover failed: {e}", flush=True)
            finally:
                if prev_force is None:
                    os.environ.pop("ORBIT_FLOW_FORCE_NEW_PROJECT", None)
                else:
                    os.environ["ORBIT_FLOW_FORCE_NEW_PROJECT"] = prev_force
            page.wait_for_timeout(1000)
            continue
        # Remember last good project URL for recover.
        if "/project/" in url:
            try:
                page._orbit_flow_project_url = url  # type: ignore[attr-defined]
            except Exception:
                pass
        dismiss_soft_prompts(page)
        try:
            ids = collect_media_ids(page)
        except Exception as e:
            if is_transient_ui_error(e):
                settle_after_nav(page, wait_ms=800)
                continue
            raise
        new_ids = [i for i in ids if i not in before_ids]
        elapsed = time.time() - t0
        if captured_videos and elapsed >= max(20.0, float(min_elapsed_s or 0)):
            raw = captured_videos[-1]
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(raw)
            print(f"  saved network video bytes={len(raw)}", flush=True)
            try:
                page.remove_listener("response", _on_response)
            except Exception:
                pass
            return f"network-video:{len(raw)}"
        skip_download = elapsed < early_gate_s or elapsed < float(min_elapsed_s or 0)
        # Prefer ids that resolve as video/mp4 (Flow sometimes returns octet-stream)
        for mid in reversed(new_ids):
            if skip_download:
                continue
            url = absolute_media_url(mid)
            try:
                head = page.request.get(url, timeout=60_000)
                ct = (head.headers.get("content-type") or "").lower()
                body = head.body()
                # Skip still-image ingredient uploads that are not videos yet
                if body[:12].find(b"ftyp") < 0 and (
                    ct.startswith("image/")
                    or body[:3] in (b"\xff\xd8\xff", b"\x89PN")
                ):
                    if int(elapsed) % 30 < 5:
                        print(f"  skip image mid={mid[:48]}… ct={ct} n={len(body)}", flush=True)
                    continue
                looks_video = (
                    "video" in ct
                    or "mp4" in ct
                    or "octet-stream" in ct
                    or ct == ""
                    or body[:12].find(b"ftyp") >= 0
                )
                if looks_video and len(body) > 150_000:
                    dest.parent.mkdir(parents=True, exist_ok=True)
                    dest.write_bytes(body)
                    print(f"  downloaded mid={mid[:48]}… bytes={len(body)} ct={ct}", flush=True)
                    return mid
                if int(elapsed) % 30 < 5:
                    print(f"  mid not ready mid={mid[:48]}… ct={ct} n={len(body)} video={looks_video}", flush=True)
            except Exception as e:
                if int(elapsed) % 30 < 5:
                    print(f"  mid fetch err {type(e).__name__}: {e}", flush=True)
                continue

        body = ""
        try:
            body = page.locator("body").inner_text(timeout=3000)[:4000]
        except Exception:
            pass
        low = body.lower()
        status = ""
        pct = re.search(r"\b(\d{1,3})\s*%", body)
        for k in (
            "failed",
            "generating",
            "thinking",
            "queue",
            "high demand",
            "creating",
            "scheduled",
            "working",
        ):
            # Avoid false positives from unrelated copy; require a word boundary.
            if k == "failed":
                if re.search(r"\bfailed\b", low):
                    status = k
                    break
                continue
            if k in low:
                status = k
                break
        if pct and not status:
            status = f"{pct.group(1)}%"
        if status in ("generating", "thinking", "creating", "working", "queue", "scheduled") or (
            pct is not None
        ):
            seen_generating = True
        # Agent UI harvest: after gen finishes, play gallery card → googlevideo mp4.
        pct_n = int(pct.group(1)) if pct else None
        gen_done = seen_generating and (
            (pct_n is not None and pct_n >= 100)
            or (status == "" and elapsed >= max(35.0, float(min_elapsed_s or 0)))
            or elapsed >= 50.0
        )
        if (
            gen_done
            and gallery_tries < 6
            and (elapsed - last_gallery_try) >= 12.0
            and elapsed >= max(25.0, float(min_elapsed_s or 0))
        ):
            gallery_tries += 1
            last_gallery_try = elapsed
            print(f"  gallery harvest attempt #{gallery_tries}", flush=True)
            got = harvest_agent_gallery_mp4(
                page, dest, captured_videos, before_asb=before_asb
            )
            if got:
                try:
                    page.remove_listener("response", _on_response)
                except Exception:
                    pass
                return got
            if captured_videos:
                raw = captured_videos[-1]
                dest.parent.mkdir(parents=True, exist_ok=True)
                dest.write_bytes(raw)
                print(f"  saved network video bytes={len(raw)}", flush=True)
                try:
                    page.remove_listener("response", _on_response)
                except Exception:
                    pass
                return f"network-video:{len(raw)}"
        # Mount completed cards so <video> elements appear.
        if seen_generating and elapsed >= 30 and int(elapsed) % 20 < 5:
            try:
                page.evaluate(
                    """() => {
                      const plays = [...document.querySelectorAll('button,[role="button"],span')]
                        .filter(n => /play_circle|play_arrow/i.test(
                          (n.innerText||'') + (n.getAttribute('aria-label')||'')
                        ));
                      for (const n of plays.slice(0, 3)) { try { n.click(); } catch (e) {} }
                    }"""
                )
                page.wait_for_timeout(800)
            except Exception:
                pass
        # Also harvest <video src> / blob URLs that never appear as getMediaUrlRedirect
        if elapsed >= max(20.0, float(min_elapsed_s or 0)):
            vsrc = page.evaluate(
                """() => {
                  const vs = [...document.querySelectorAll('video')]
                    .map(v => v.currentSrc || v.src)
                    .filter(Boolean);
                  return vs.length ? vs[vs.length - 1] : null;
                }"""
            )
            if vsrc and (vsrc.startswith("http") or vsrc.startswith("blob:")):
                try:
                    if vsrc.startswith("blob:"):
                        data = page.evaluate(
                            """async (url) => {
                              const r = await fetch(url);
                              const buf = await r.arrayBuffer();
                              const bytes = new Uint8Array(buf);
                              let s = '';
                              const chunk = 0x8000;
                              for (let i = 0; i < bytes.length; i += chunk) {
                                s += String.fromCharCode(...bytes.subarray(i, i + chunk));
                              }
                              return btoa(s);
                            }""",
                            vsrc,
                        )
                        import base64

                        raw = base64.b64decode(data)
                        if len(raw) > 150_000 and raw.find(b"ftyp") >= 0:
                            dest.parent.mkdir(parents=True, exist_ok=True)
                            dest.write_bytes(raw)
                            print(
                                f"  downloaded blob video bytes={len(raw)}",
                                flush=True,
                            )
                            return vsrc
                    else:
                        head = page.request.get(vsrc, timeout=60_000)
                        body_b = head.body()
                        if len(body_b) > 150_000 and (
                            b"ftyp" in body_b[:64] or "video" in (head.headers.get("content-type") or "")
                        ):
                            dest.parent.mkdir(parents=True, exist_ok=True)
                            dest.write_bytes(body_b)
                            print(
                                f"  downloaded video src bytes={len(body_b)}",
                                flush=True,
                            )
                            return vsrc
                except Exception as e:
                    if int(elapsed) % 30 < 5:
                        print(f"  video-src fetch err {type(e).__name__}: {e}", flush=True)
        # After generation completes, new Flow UI often has no getMediaUrlRedirect
        # ids — pull via the card Download control / expect_download.
        if seen_generating and elapsed >= max(35.0, float(min_elapsed_s or 0)):
            try:
                # Prefer an explicit Download control near completed cards.
                dl_clicked = click_visible(page, "download") or click_visible(
                    page, "Download"
                )
                if not dl_clicked:
                    dl_clicked = bool(
                        page.evaluate(
                            """() => {
                              const nodes = [...document.querySelectorAll(
                                'button,[role="button"],a'
                              )];
                              for (const n of nodes) {
                                const t = (
                                  (n.innerText || '') +
                                  ' ' +
                                  (n.getAttribute('aria-label') || '')
                                ).toLowerCase();
                                if (t.includes('download') && !t.includes('undownload')) {
                                  n.click();
                                  return true;
                                }
                              }
                              // Overflow more_vert near latest media
                              for (const n of nodes) {
                                const t = (n.innerText || '').trim().toLowerCase();
                                if (t === 'more_vert' || t === 'more_horiz') {
                                  n.click();
                                  return 'menu';
                                }
                              }
                              return false;
                            }"""
                        )
                    )
                    if dl_clicked == "menu":
                        page.wait_for_timeout(500)
                        dl_clicked = click_visible(page, "download") or click_visible(
                            page, "Download"
                        )
                # Click must happen INSIDE expect_download or the event is missed.
                try:
                    with page.expect_download(timeout=25_000) as di:
                        clicked = (
                            click_visible(page, "download")
                            or click_visible(page, "Download")
                        )
                        if not clicked:
                            page.evaluate(
                                """() => {
                                  for (const n of document.querySelectorAll(
                                    'button,[role="button"],a'
                                  )) {
                                    const t = (
                                      (n.innerText || '') + ' ' +
                                      (n.getAttribute('aria-label') || '')
                                    ).toLowerCase();
                                    if (t.includes('download')) { n.click(); return; }
                                  }
                                  for (const n of document.querySelectorAll(
                                    'button,[role="button"]'
                                  )) {
                                    const t = (n.innerText || '').trim().toLowerCase();
                                    if (t === 'more_vert' || t === 'more_horiz') {
                                      n.click(); return;
                                    }
                                  }
                                }"""
                            )
                            page.wait_for_timeout(400)
                            click_visible(page, "download") or click_visible(
                                page, "Download"
                            )
                    dl = di.value
                    dest.parent.mkdir(parents=True, exist_ok=True)
                    dl.save_as(str(dest))
                    n = dest.stat().st_size if dest.exists() else 0
                    if n > 150_000:
                        print(f"  downloaded via UI Download bytes={n}", flush=True)
                        return f"ui-download:{n}"
                    print(f"  UI download too small bytes={n}", flush=True)
                except Exception as e:
                    if int(elapsed) % 30 < 5:
                        print(f"  UI download miss: {e}", flush=True)
            except Exception as e:
                if int(elapsed) % 30 < 5:
                    print(f"  UI download path err: {e}", flush=True)

        line = f"  wait {int(time.time() - t0)}s status={status or '…'} new_media={len(new_ids)} gen={seen_generating}"
        if line != last_status:
            print(line, flush=True)
            last_status = line

        # Hard stop only when BOTH Flow and AI credit pools are exhausted.
        # "Out of Google Flow credits" alone is OK — Ultra falls back to AI credits.
        # Do NOT treat "usage limit" / "try again later" as fatal (often the
        # wrong Google account, or a transient Fast-queue refuse).
        both_pools_empty = any(
            s in low
            for s in (
                "no ai credits",
                "out of ai credits",
                "not enough ai credits",
                "ai credits remaining: 0",
                "0 ai credits",
            )
        ) or (
            ("out of google flow credits" in low or "0 google flow credits" in low)
            and ("0 ai credits" in low or "no ai credits" in low)
        )
        hard_empty = any(
            s in low
            for s in (
                "not enough credits to generate",
                "purchase more credits",
                "buy more credits",
            )
        )
        if (both_pools_empty or hard_empty) and elapsed > 12 and not new_ids:
            raise RuntimeError(
                "Flow + AI credits exhausted — stop mint; top up Google One AI "
                "credits or wait for daily refresh"
            )

        # Flow often flashes "failed" while a usable mp4 is still arriving.
        # Soft-retry the UI (incl. material `refresh` on failed cards).
        # Fail fast once retries are exhausted with no new media.
        if status == "failed":
            if failed_since is None:
                failed_since = time.time()
            elif retry_clicks < 3 and time.time() - failed_since > 20:
                clicked = (
                    click_visible(page, "try again")
                    or click_visible(page, "retry")
                    or click_visible(page, "regenerate")
                    or click_visible(page, "refresh")
                )
                # Failed card icon is often a bare Material `refresh` glyph.
                if not clicked:
                    try:
                        clicked = bool(
                            page.evaluate(
                                """() => {
                                  const nodes = [...document.querySelectorAll(
                                    'button,[role="button"],span'
                                  )];
                                  for (const n of nodes) {
                                    const t = (n.innerText || n.textContent || '')
                                      .trim().toLowerCase();
                                    if (t === 'refresh') {
                                      n.click();
                                      return true;
                                    }
                                  }
                                  return false;
                                }"""
                            )
                        )
                    except Exception:
                        clicked = False
                retry_clicks += 1
                failed_since = time.time()
                print(
                    f"  Flow failed banner — soft retry click "
                    f"({'hit' if clicked else 'miss'}) #{retry_clicks}",
                    flush=True,
                )
            elif (
                retry_clicks >= 3
                and time.time() - failed_since > 45
                and not new_ids
            ):
                raise RuntimeError(
                    "Flow stuck in failed state after soft retries"
                )
            elif new_ids:
                # Media present — keep polling download; reset stuck timer
                failed_since = time.time()
        else:
            failed_since = None

        # If Create never entered generating, dump once then stop resubmitting
        # forever (resubmit spam burns credits / hangs when browser dies).
        if (
            not seen_generating
            and elapsed > 20
            and int(elapsed) % 30 < 5
            and retry_clicks < 3
        ):
            snippet = (body or "").replace("\n", " | ")
            print(f"  PAGE_SNIPPET gen=False head: {snippet[:700]}", flush=True)
            print(f"  PAGE_SNIPPET gen=False tail: {snippet[-900:]}", flush=True)
            try:
                btns = page.evaluate(
                    """() => [...document.querySelectorAll('button,[role="button"]')]
                      .map(b => (b.innerText || b.getAttribute('aria-label') || '')
                        .trim().replace(/\\n/g,' ')).filter(t => t).slice(0, 80)"""
                )
                print(f"  PAGE_BUTTONS: {btns}", flush=True)
            except Exception as e:
                print(f"  PAGE_BUTTONS err: {e}", flush=True)
            try:
                shot = dest.with_name(dest.stem + "_flow_stall.png")
                page.screenshot(path=str(shot), full_page=False, timeout=10_000)
                print(f"  stall screenshot {shot}", flush=True)
            except Exception as e:
                print(f"  screenshot skipped: {e}", flush=True)
                if "closed" in str(e).lower() or "crashed" in str(e).lower():
                    raise RuntimeError(f"Flow browser died during wait: {e}") from e
            # Prefer refresh-on-fail over blind Create resubmit.
            try:
                click_visible(page, "refresh") or click_visible(page, "try again")
            except Exception as e:
                print(f"  fail-refresh skipped: {e}", flush=True)

        # Click into All Media / videos if present to surface completed clips
        if time.time() - t0 > 60 and int(time.time() - t0) % 45 < 4:
            click_visible(page, "view videos") or click_visible(page, "all media")

        try:
            page.wait_for_timeout(4000)
        except Exception as e:
            if "closed" in str(e).lower() or "crashed" in str(e).lower():
                raise RuntimeError(f"Flow browser died during wait: {e}") from e
            raise

    raise TimeoutError(f"Flow video not ready after {timeout_s}s")


def _generate_clip_once(
    page,
    prompt: str,
    dest: Path,
    *,
    model: str = DEFAULT_MODEL,
    orbit_ref: Path | None = None,
    start_frame: Path | None = None,
    timeout_s: int = 900,
    reuse_project: bool = False,
    scenery_only: bool = False,
) -> dict:
    """One attempt: generate a silent Veo clip via Google Flow Ultra UI.

    Modes:
      - default: Orbit identity I2V (Orbit With Ben)
      - scenery_only: no attachment chip
      - start_frame: I2V from an arbitrary still (History of Science / custom)
    """
    t0 = time.time()
    ref = None
    if start_frame is not None:
        ref = Path(start_frame)
        if not ref.exists():
            raise FileNotFoundError(ref)
        print(f"  start-frame I2V: {ref}", flush=True)
        scenery_only = False
    elif not scenery_only:
        ref = _assert_orbit_identity_ref(orbit_ref or veo.ORBIT_REF)
        print(f"  orbit identity ref: {ref}", flush=True)
    else:
        print("  scenery-only (no Orbit identity ref)", flush=True)

    if reuse_project and "/project/" in (page.url or ""):
        url = page.url
    else:
        page.goto(FLOW_HOME, wait_until="domcontentloaded", timeout=120_000)
        settle_after_nav(page, wait_ms=1500)
        dismiss_banners(page)
        url = ensure_project(page)

    if not looks_logged_in(page):
        raise RuntimeError(
            "Not logged into Google Flow.\n"
            "Run once with --login on the Ultra Google account:\n"
            "  python3 04_Audio/tools/orbit_flow_veo_ui.py --login"
        )

    print(f"  flow: {url}", flush=True)
    model = assert_veo3_model(model)
    ensure_agent_session(page)
    before = collect_media_ids(page)
    # Start-frame / Orbit I2V: Ingredients mode (prompt chip), not Frames slots.
    configure_veo_settings(
        page,
        model=model,
        frames_mode=False,
        ingredients_mode=(start_frame is not None) or (not scenery_only),
    )
    # Agent UI defaults to x2 — burn 2× AI credits. Force x1 before Create.
    force_outputs_x1(page)
    print("  post-settings…", flush=True)
    settle_after_nav(page, wait_ms=600)
    ensure_agent_session(page)
    attached = False
    if start_frame is not None:
        ensure_agent_session(page)
        print("  attaching start frame…", flush=True)
        attached = attach_image_to_prompt(page, ref)
        # HOS-proven path (2026-08-26): right-click still → Animate, then prompt.
        # Without this, Create can accept the JPEG chip but never start Veo.
        if try_context_animate(page):
            configure_veo_settings(
                page,
                model=model,
                frames_mode=False,
                ingredients_mode=True,
            )
            force_outputs_x1(page)
        print("  setting start-frame I2V prompt…", flush=True)
        set_prompt(page, flow_prompt(prompt, start_frame_i2v=True))
        if _prompt_attachment_count(page) < 1:
            print("  chip missing after prompt paste — re-attaching", flush=True)
            attached = attach_image_to_prompt(page, ref)
        if _prompt_attachment_count(page) < 1:
            raise RuntimeError("Start-frame prompt chip missing after attach — aborting")
        print("  submitting Create…", flush=True)
        submit_create(page)
        print("  submitted Create (start-frame I2V)", flush=True)
        confirm_generation_spend(page)
    elif scenery_only:
        # Keep agent session healthy, but do NOT attach Orbit identity chip.
        ensure_agent_session(page)
        print("  setting scenery-only prompt (no Orbit chip)…", flush=True)
        set_prompt(
            page,
            (
                "GENERATE one silent 8-second Veo video NOW. Do not brainstorm. "
                "Do not ask questions. Do not edit images. Spend credits and output "
                "the video file only.\n\n"
                + flow_prompt(prompt, scenery_only=True)
            ),
        )
        # Clear any leftover attachment chips if present
        try:
            page.keyboard.press("Escape")
            page.wait_for_timeout(200)
        except Exception:
            pass
        print("  submitting Create…", flush=True)
        submit_create(page)
        print("  submitted Create (scenery-only, no Orbit ref)", flush=True)
        confirm_generation_spend(page)
    else:
        print("  ensuring Orbit agent instruction…", flush=True)
        ensure_orbit_agent_instruction(page)
        ensure_agent_session(page)
        print("  attaching Orbit ref…", flush=True)
        # Bind Orbit identity chip first, then paste prompt text (keeps chip stable).
        attached = attach_orbit_to_prompt(page, ref)
        print("  setting prompt…", flush=True)
        set_prompt(page, flow_prompt(prompt))
        if _prompt_attachment_count(page) < 1:
            print("  chip missing after prompt paste — re-attaching", flush=True)
            attached = attach_orbit_to_prompt(page, ref)
        if _prompt_attachment_count(page) < 1:
            raise RuntimeError("Orbit prompt chip missing after attach — aborting")
        print("  submitting Create…", flush=True)
        submit_create(page)
        print("  submitted Create (identity-locked, Orbit ref attached)", flush=True)
        confirm_generation_spend(page)
    media_id = wait_and_download(
        page, dest, before_ids=before, timeout_s=timeout_s, min_elapsed_s=25
    )
    size = dest.stat().st_size if dest.exists() else 0
    if size < 120_000:
        raise RuntimeError(f"download too small: {dest} ({size})")
    import subprocess as _sp
    try:
        dur = float(
            _sp.check_output(
                [
                    "ffprobe", "-v", "error", "-show_entries", "format=duration",
                    "-of", "default=nw=1:nk=1", str(dest),
                ],
                text=True,
            ).strip()
        )
    except Exception as e:
        raise RuntimeError(f"download unreadable: {dest} ({e})") from e
    if dur < 5.0 or dur > 40.0:
        raise RuntimeError(f"download bad duration: {dest} dur={dur:.2f} size={size}")
    veo.strip_audio(dest)
    return {
        "seconds": round(time.time() - t0, 1),
        "bytes": dest.stat().st_size,
        "model": model,
        "engine": "flow-ui-veo",
        "orbit_ref": str(ref) if ref and start_frame is None and not scenery_only else None,
        "start_frame": str(start_frame) if start_frame else None,
        "orbit_attached": attached,
        "identity_lock": (not scenery_only) and start_frame is None,
        "scenery_only": scenery_only,
        "media_id": media_id,
        "url": page.url,
    }


def generate_clip(
    page,
    prompt: str,
    dest: Path,
    *,
    model: str = DEFAULT_MODEL,
    orbit_ref: Path | None = None,
    start_frame: Path | None = None,
    timeout_s: int = 900,
    reuse_project: bool = False,
    scenery_only: bool = False,
    attempts: int = 3,
) -> dict:
    """Generate one silent Veo clip via Google Flow Ultra UI (with soft retries)."""
    last: BaseException | None = None
    use_reuse = reuse_project
    for attempt in range(1, attempts + 1):
        try:
            return _generate_clip_once(
                page,
                prompt,
                dest,
                model=model,
                orbit_ref=orbit_ref,
                start_frame=start_frame,
                timeout_s=timeout_s,
                reuse_project=use_reuse,
                scenery_only=scenery_only,
            )
        except Exception as e:
            last = e
            if "not logged into google flow" in str(e).lower():
                raise
            if attempt >= attempts or not is_transient_ui_error(e):
                raise
            print(
                f"  generate_clip soft-retry {attempt}/{attempts}: {e}",
                flush=True,
            )
            use_reuse = False
            recover_flow_home(page)
    assert last is not None
    raise last


def login_flow(profile: Path) -> None:
    from playwright.sync_api import sync_playwright

    print(f"Profile: {profile}", flush=True)
    print("Opening Google Flow — sign in with the Google One Ultra account…", flush=True)
    with sync_playwright() as p:
        ctx, page = launch_context(p, headed=True, profile=profile, slow_mo=50)
        try:
            page.goto(FLOW_HOME, wait_until="domcontentloaded", timeout=120_000)
            print(
                "\nWhen you see Flow with ULTRA badge (logged in), return here and press Enter.\n",
                flush=True,
            )
            try:
                input()
            except EOFError:
                print("No TTY — waiting up to 5 min for login…", flush=True)
                deadline = time.time() + 300
                while time.time() < deadline:
                    if looks_logged_in(page):
                        break
                    page.wait_for_timeout(3000)
            if not looks_logged_in(page):
                raise SystemExit("Still not logged in — re-run --login")
            print("OK — Flow session saved.", flush=True)
        finally:
            ctx.close()


def dump_probe(page, out_dir: Path) -> dict:
    out_dir.mkdir(parents=True, exist_ok=True)
    shot = out_dir / "flow_probe.png"
    html = out_dir / "flow_probe.html"
    ensure_project(page)
    page.screenshot(path=str(shot), full_page=True)
    html.write_text(page.content(), encoding="utf-8")
    summary = {
        "url": page.url,
        "logged_in": looks_logged_in(page),
        "editor": editor_box(page),
        "editor_usable": editor_usable(page),
        "ultra": page.locator('button:has-text("ULTRA")').count() > 0,
        "screenshot": str(shot),
        "html": str(html),
    }
    (out_dir / "flow_probe.json").write_text(json.dumps(summary, indent=2))
    return summary


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--login", action="store_true", help="Headed Google Ultra login")
    ap.add_argument("--probe", action="store_true", help="One short Orbit test clip")
    ap.add_argument("--prompt", default="", help="Scene action (Orbit-in-scene)")
    ap.add_argument("--out", type=Path, default=Path("/tmp/orbit_flow_veo_probe.mp4"))
    ap.add_argument("--pass-id", default="p0")
    ap.add_argument("--model", default=DEFAULT_MODEL)
    ap.add_argument("--profile", type=Path, default=None)
    ap.add_argument("--headed", action="store_true", help="Show browser (debug)")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--dump-ui", type=Path, default=None)
    ap.add_argument("--timeout", type=int, default=900)
    ap.add_argument(
        "--start-frame",
        type=Path,
        default=None,
        help="I2V from this still (HOS / custom — skips Orbit identity lock)",
    )
    ap.add_argument(
        "--scenery-only",
        action="store_true",
        help="No identity/start-frame attachment",
    )
    args = ap.parse_args()

    profile = profile_path(args.profile)

    if args.login:
        login_flow(profile)
        return

    if args.probe and not args.prompt:
        args.prompt = (
            "Orbit the orange robot floats beside the James Webb Space Telescope, "
            "cream eyes curious, soft underside glow, deep space stars behind."
        )

    prompt = ""
    if args.prompt:
        # HOS / start-frame prompts should stay short and literal — skip Orbit wrapper.
        if args.start_frame or args.scenery_only:
            prompt = args.prompt.strip()
        else:
            prompt = veo.build_prompt(args.prompt, pass_id=args.pass_id)

    print(f"Orbit ref: {veo.ORBIT_REF}", flush=True)
    if args.start_frame:
        print(f"start_frame: {args.start_frame}", flush=True)
    print(f"profile={profile}", flush=True)
    print(f"model={args.model} · engine=flow-ui", flush=True)

    if args.dry_run:
        if prompt:
            print(prompt[:500], "…")
        else:
            print("(no prompt — dry-run OK)")
        return

    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        ctx, page = launch_context(
            p, headed=args.headed or bool(args.dump_ui), profile=profile
        )
        try:
            if args.dump_ui:
                page.goto(FLOW_HOME, wait_until="domcontentloaded", timeout=120_000)
                summary = dump_probe(page, args.dump_ui)
                print(json.dumps(summary, indent=2))
                return
            if not args.prompt:
                ap.error("Provide --prompt, --probe, --login, or --dump-ui")
            print(f"out={args.out}", flush=True)
            meta = generate_clip(
                page,
                prompt,
                args.out,
                model=args.model,
                timeout_s=args.timeout,
                start_frame=args.start_frame,
                scenery_only=args.scenery_only,
            )
            print(json.dumps(meta, indent=2))
            print(f"SAVED {args.out}", flush=True)
        finally:
            ctx.close()


if __name__ == "__main__":
    main()
