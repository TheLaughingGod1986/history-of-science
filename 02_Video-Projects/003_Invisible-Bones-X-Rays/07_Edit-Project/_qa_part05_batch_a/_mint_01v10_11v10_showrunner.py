"""Mint 01_v10 + 11_v10 from Showrunner CREATE md pastes only. NEW project d2ebe084. BLANK opener."""
import importlib.util, json, re, sys, time
from datetime import datetime, timezone
from pathlib import Path
from playwright.sync_api import sync_playwright

REPO = Path("/Users/benjaminoats/YouTube/History Of Science")
EDIT = REPO / "02_Video-Projects/003_Invisible-Bones-X-Rays/07_Edit-Project"
CLIP = REPO / "02_Video-Projects/003_Invisible-Bones-X-Rays/04_Generated-Clips/part05"
QA = EDIT / "_qa_part05_batch_a"
PROJECT = "https://flow.google.com/u/0/project/d2ebe084-78fb-4d48-9006-2d897c5a80fb"
CDP = "http://127.0.0.1:9222"

sys.path.insert(0, str(REPO / "04_Audio" / "tools"))
import orbit_flow_veo_ui as flow
import orbit_gemini_veo as veo

spec = importlib.util.spec_from_file_location("m", EDIT / "_mint_part04_batch_a.py")
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


def load_paste(md_name: str) -> str:
    text = (EDIT / md_name).read_text()
    mobj = re.search(r"```\n(.*?)```", text, re.S)
    if not mobj:
        raise SystemExit(f"no fence in {md_name}")
    body = mobj.group(1).strip()
    low = body.lower()
    for bad in ("dna", "helix"):
        if bad in low:
            raise SystemExit(f"STOP paste has {bad} in {md_name}")
    return body


JOBS = [
    (
        "01_chapter_new_seeing",
        "v10",
        "PART05_PLATE01_CREATE_v10.md",
        ["NO readable words", "chapter-open PICTURE ONLY", "EMPTY dark wood", "HARD REJECT: any on-screen"],
        "Showrunner Option A no on-screen text",
    ),
    (
        "11_soft_return",
        "v10",
        "PART05_PLATE11_CREATE_v06.md",
        ["soft fade", "fluorescent cardboard", "EMPTY dark space", "end of part"],
        "Showrunner PART05_PLATE11_CREATE_v06 paste (supersedes glow-only v09)",
    ),
]


def download(page, dest):
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
            return {x:ir.x+ir.width/2,y:ir.y+ir.height/2,t:raw.slice(0,140)};
          }
        }
        return null;
      }""",
            n,
        )
        if hit:
            return {**hit, "needle": n}
    return None


def pull(page, pid, ver, needles, reason, paste_name):
    page.goto(PROJECT, wait_until="domcontentloaded", timeout=120000)
    page.wait_for_timeout(2000)
    for _ in range(10):
        page.mouse.wheel(0, 800)
        page.wait_for_timeout(200)
    page.mouse.wheel(0, -8000)
    page.wait_for_timeout(400)
    hit = find_card(page, needles)
    print("  hit", hit, flush=True)
    if not hit:
        return False
    page.mouse.click(hit["x"], hit["y"])
    page.wait_for_timeout(2800)
    dest = CLIP / f"{pid}_{ver}.mp4"
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
    known = {m.sha256_file(f) for f in CLIP.glob("*.mp4") if f.name != dest.name}
    if sha in known or dur < 6 or dur > 12:
        print("  reject", flush=True)
        dest.unlink(missing_ok=True)
        return False
    m.extract_qa_frames(dest, f"{pid}_{ver}")
    report = {
        "plate": pid,
        "version": ver,
        "path": str(dest),
        "bytes": dest.stat().st_size,
        "sha256": sha,
        "duration_s": dur,
        "model": "Veo 3.1 - Quality",
        "account": "benoats@googlemail.com",
        "project": PROJECT,
        "source_paste": paste_name,
        "remint_reason": reason,
        "assemble": "CLOSED",
        "ts": datetime.now(timezone.utc).isoformat(),
    }
    (QA / f"{pid}_{ver}_mint.json").write_text(json.dumps(report, indent=2) + "\n")
    print("LANDED", pid, ver, flush=True)
    return True


def create_one(page, pid, ver, paste_name, needles, reason):
    prompt = load_paste(paste_name)
    print(f"\n=== {pid} {ver} paste={paste_name} len={len(prompt)} ===", flush=True)
    page.goto(PROJECT, wait_until="domcontentloaded", timeout=120000)
    page.wait_for_timeout(1500)
    aria = page.evaluate(
        """() => { const a=document.querySelector('a[aria-label*="Google Account"]');
           return a && a.getAttribute('aria-label'); }"""
    )
    if not aria or "googlemail" not in aria.lower():
        raise SystemExit(f"STOP wrong account {aria}")
    try:
        flow.configure_veo_settings(
            page, model="Veo 3.1 - Quality", frames_mode=False, ingredients_mode=False
        )
    except Exception as e:
        print("  settings", e, flush=True)
    page.keyboard.press("Escape")
    page.wait_for_timeout(300)
    # BLANK opener — do not paste DNA opener
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
        has = any(re.search(re.escape(n), body, re.I) for n in needles)
        line = f"  wait {int(time.time()-t0)}s pct={pcts[-2:] if pcts else None} active={active} has={has}"
        if line != last:
            print(line, flush=True)
            last = line
        if has and not active:
            page.wait_for_timeout(5000)
            break
        page.wait_for_timeout(8000)
    ok = pull(page, pid, ver, needles, reason, paste_name)
    if not ok:
        ok = pull(page, pid, ver, needles[:2], reason, paste_name)
    return ok


def main():
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(CDP)
        page = next(
            pg for pg in browser.contexts[0].pages if "flow.google.com" in (pg.url or "")
        )
        page.bring_to_front()
        for pid, ver, paste, needles, reason in JOBS:
            dest = CLIP / f"{pid}_{ver}.mp4"
            if dest.exists() and dest.stat().st_size > 150000:
                print("SKIP exists", pid, ver, flush=True)
                continue
            ok = create_one(page, pid, ver, paste, needles, reason)
            if not ok:
                print("FAIL retry", pid, flush=True)
                ok = create_one(page, pid, ver, paste, needles, reason)
                if not ok:
                    print("FAIL2", pid, flush=True)
    print("DONE", flush=True)


if __name__ == "__main__":
    main()
