"""Mint HOS 003 P05 plate 02 ONLY as v07 — NEW Flow project + Showrunner PART05_PLATE02_CREATE_v06.md paste."""
from __future__ import annotations
import importlib.util, json, re, sys, time
from datetime import datetime, timezone
from pathlib import Path
from playwright.sync_api import sync_playwright

REPO = Path("/Users/benjaminoats/YouTube/History Of Science")
EDIT = REPO / "02_Video-Projects/003_Invisible-Bones-X-Rays/07_Edit-Project"
CLIP = REPO / "02_Video-Projects/003_Invisible-Bones-X-Rays/04_Generated-Clips/part05"
QA = EDIT / "_qa_part05_batch_a"
PASTE_MD = EDIT / "PART05_PLATE02_CREATE_v06.md"
FLOW_HOME = "https://flow.google.com/u/0/"
CDP = "http://127.0.0.1:9222"
PID = "02_what_are_xrays"
VER = "v07"
# Unique needle from Showrunner paste (no DNA words)
NEEDLES = ["EMPTY dark wood desk", "X-RAYS sparse", "straight soft green-violet", "HARD REJECT: corkscrew"]

sys.path.insert(0, str(REPO / "04_Audio" / "tools"))
import orbit_flow_veo_ui as flow
import orbit_gemini_veo as veo

spec = importlib.util.spec_from_file_location("m", EDIT / "_mint_part04_batch_a.py")
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

SHELF = (
    " Bare empty shelves only — no corkscrew wood models, no ball-and-stick kits"
    " on shelves or desk. Prefer empty lab shelves."
)


def load_paste() -> str:
    text = PASTE_MD.read_text()
    # extract fenced Create prompt
    mobj = re.search(r"```\n(.*?)```", text, re.S)
    if not mobj:
        raise SystemExit("no paste fence in PART05_PLATE02_CREATE_v06.md")
    body = mobj.group(1).strip()
    # never inject DNA/helix words into Flow
    return body + SHELF


def assert_googlemail(page):
    aria = page.evaluate(
        """() => { const a=document.querySelector('a[aria-label*="Google Account"]');
           return a && a.getAttribute('aria-label'); }"""
    )
    if not aria or "googlemail" not in aria.lower():
        raise SystemExit(f"STOP wrong account {aria}")
    print("  account ok", aria[:80], flush=True)


def new_project(page) -> str:
    """Force a brand-new Flow project under u/0."""
    page.goto(FLOW_HOME, wait_until="domcontentloaded", timeout=120000)
    page.wait_for_timeout(2500)
    flow.dismiss_banners(page)
    assert_googlemail(page)
    clicked = page.evaluate(
        """() => {
          for (const b of document.querySelectorAll('button,a,[role=button]')) {
            const t = ((b.innerText||'')+' '+(b.getAttribute('aria-label')||'')).replace(/\\n/g,' ').trim();
            if (/^add\\s*new project$/i.test(t) || /^new project$/i.test(t) || /new project/i.test(t) && /add/i.test(t)) {
              b.click(); return t.slice(0,60);
            }
          }
          return null;
        }"""
    )
    if not clicked:
        # fallback helper
        ok = flow.click_visible(page, "new project")
        if not ok:
            raise SystemExit("could not click New project")
        clicked = "new project"
    print("  clicked", clicked, flush=True)
    page.wait_for_url("**/project/**", timeout=90000)
    page.wait_for_timeout(2500)
    flow.dismiss_banners(page)
    url = page.url
    if "/project/" not in url:
        raise SystemExit(f"not in project {url}")
    print("  NEW PROJECT", url, flush=True)
    return url


def download(page, dest: Path):
    dls = page.evaluate(
        """() => [...document.querySelectorAll('button,[role=button]')].map(el=>{
      const t=((el.innerText||'')+' '+(el.getAttribute('aria-label')||'')).trim().replace(/\\n/g,' ');
      const r=el.getBoundingClientRect();
      return {t:t.slice(0,50),x:r.x+r.width/2,y:r.y+r.height/2,ok:r.width>8&&r.height>8&&r.y>=0&&r.y<180};
    }).filter(o=>/download/i.test(o.t)&&o.ok&&!/batch/i.test(o.t))"""
    )
    for d in dls or []:
        try:
            with page.expect_download(timeout=120000) as di:
                page.mouse.click(d["x"], d["y"])
                page.wait_for_timeout(800)
                item = page.evaluate(
                    """() => {
                  for (const el of document.querySelectorAll('[role=menuitem],button,a,.mat-mdc-menu-item')) {
                    const t=((el.innerText||'')+' '+(el.getAttribute('aria-label')||'')).trim();
                    if (/720p|original|mp4/i.test(t)&&!/image|png|batch/i.test(t)) {
                      const r=el.getBoundingClientRect();
                      if(r.width>20) return {x:r.x+r.width/2,y:r.y+r.height/2};
                    }
                  }
                  return null;
                }"""
                )
                if item:
                    page.mouse.click(item["x"], item["y"])
            dl = di.value
            raw = None
            try:
                src = dl.path()
                if src:
                    raw = Path(src).read_bytes()
            except Exception:
                pass
            if raw is None:
                tmp = dest.with_suffix(".tmp")
                dl.save_as(str(tmp))
                raw = tmp.read_bytes()
                tmp.unlink(missing_ok=True)
            if raw and len(raw) > 150000 and b"ftyp" in raw[:64]:
                return raw
        except Exception as e:
            print("  dl err", e, flush=True)
            page.keyboard.press("Escape")
    return None


def find_card(page, needles):
    for n in needles:
        hit = page.evaluate(
            """(needle) => {
        const re=new RegExp(needle.replace(/[.*+?^${}()|[\\]\\\\]/g,'\\\\$&'),'i');
        const walk=document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
        let node;
        while((node=walk.nextNode())){
          const raw=(node.textContent||'');
          if(!re.test(raw)) continue;
          let el=node.parentElement;
          for(let d=0; d<10 && el; d++, el=el.parentElement){
            const img=el.querySelector && el.querySelector('img[src*="/asb/"]');
            if(!img) continue;
            const ir=img.getBoundingClientRect();
            if(ir.width<80) continue;
            return {x:ir.x+ir.width/2,y:ir.y+ir.height/2,t:raw.slice(0,100)};
          }
        }
        return null;
      }""",
            n,
        )
        if hit:
            return {**hit, "needle": n}
    return None


def pull(page, project_url, needles):
    page.goto(project_url, wait_until="domcontentloaded", timeout=120000)
    page.wait_for_timeout(2000)
    for _ in range(10):
        page.mouse.wheel(0, 800)
        page.wait_for_timeout(250)
    page.mouse.wheel(0, -8000)
    page.wait_for_timeout(400)
    hit = find_card(page, needles)
    print("  hit", hit, flush=True)
    if not hit:
        return False
    page.mouse.click(hit["x"], hit["y"])
    page.wait_for_timeout(2800)
    dest = CLIP / f"{PID}_{VER}.mp4"
    raw = download(page, dest)
    if not raw:
        return False
    dest.write_bytes(raw)
    try:
        veo.strip_audio(dest)
    except Exception as e:
        print("  strip", e, flush=True)
    sha = m.sha256_file(dest)
    dur = m.probe_dur(dest)
    print(f"  sha={sha} dur={dur}", flush=True)
    if dur < 6 or dur > 12:
        dest.unlink(missing_ok=True)
        return False
    known = {m.sha256_file(f) for f in CLIP.glob("*.mp4") if f.name != dest.name}
    if sha in known:
        print("  DUP reject", flush=True)
        dest.unlink(missing_ok=True)
        return False
    m.extract_qa_frames(dest, f"{PID}_{VER}")
    report = {
        "plate": PID,
        "version": VER,
        "path": str(dest),
        "bytes": dest.stat().st_size,
        "sha256": sha,
        "duration_s": dur,
        "model": "Veo 3.1 - Quality",
        "account": "benoats@googlemail.com",
        "project": project_url,
        "source_paste": str(PASTE_MD),
        "remint_reason": "Ben rewrite path + UAT wooden DNA shelf FAIL; NEW Flow project",
        "assemble": "CLOSED",
        "ts": datetime.now(timezone.utc).isoformat(),
    }
    (QA / f"{PID}_{VER}_mint.json").write_text(json.dumps(report, indent=2) + "\n")
    (QA / "PART05_PLATE02_V07_PROJECT.txt").write_text(project_url + "\n")
    print("LANDED", PID, VER, flush=True)
    return True


def main():
    prompt = load_paste()
    print("prompt_len", len(prompt), flush=True)
    # sanity: no DNA/helix words in Flow paste
    low = prompt.lower()
    for bad in ("dna", "helix", "double-helix"):
        if bad in low:
            raise SystemExit(f"STOP paste contains forbidden word: {bad}")
    CLIP.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(CDP)
        page = next(
            pg for pg in browser.contexts[0].pages if "flow.google.com" in (pg.url or "")
        )
        page.bring_to_front()
        project_url = new_project(page)
        try:
            flow.configure_veo_settings(
                page, model="Veo 3.1 - Quality", frames_mode=False, ingredients_mode=False
            )
        except Exception as e:
            print("  settings", e, flush=True)
        page.keyboard.press("Escape")
        page.wait_for_timeout(300)
        # BLANK opener — do not paste DNA opener; leave default blank
        m.set_prompt_manual(page, prompt)
        btn = page.evaluate(
            """() => {
          for (const el of document.querySelectorAll('button,[role=button]')) {
            const a=el.getAttribute('aria-label')||'';
            if (/Start generation/i.test(a)&&!el.disabled){
              el.scrollIntoView({block:'center'});
              const r=el.getBoundingClientRect();
              return {x:r.x+r.width/2,y:r.y+r.height/2};
            }
          }
          return null;
        }"""
        )
        if not btn:
            raise SystemExit("no create")
        page.mouse.click(btn["x"], btn["y"])
        try:
            flow.confirm_generation_spend(page, timeout_s=8)
        except Exception:
            pass
        print("  submitted", flush=True)
        t0 = time.time()
        last = ""
        while time.time() - t0 < 780:
            body = page.locator("body").inner_text(timeout=5000)
            pcts = [int(x) for x in re.findall(r"(\d{1,3})%", body)]
            active = [x for x in pcts if x < 100]
            has = any(re.search(re.escape(n), body, re.I) for n in NEEDLES)
            line = f"  wait {int(time.time()-t0)}s pct={pcts[-2:] if pcts else None} active={active} has={has}"
            if line != last:
                print(line, flush=True)
                last = line
            if has and not active:
                page.wait_for_timeout(5000)
                break
            page.wait_for_timeout(8000)
        ok = pull(page, project_url, NEEDLES)
        if not ok:
            ok = pull(page, project_url, ["EMPTY dark wood", "X-RAYS", "corkscrew"])
        if not ok:
            raise SystemExit("FAIL pull")
    print("DONE", flush=True)


if __name__ == "__main__":
    main()
