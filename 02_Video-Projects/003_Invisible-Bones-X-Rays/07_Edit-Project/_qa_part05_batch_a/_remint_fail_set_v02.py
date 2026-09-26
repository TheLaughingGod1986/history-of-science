"""Remint P05 FAIL set as v02 — no DNA helix; Explorer only on 06 with finished crown hair."""
import importlib.util, json, re, time
from datetime import datetime, timezone
from pathlib import Path
from playwright.sync_api import sync_playwright

REPO = Path("/Users/benjaminoats/YouTube/History Of Science")
EDIT = REPO / "02_Video-Projects/003_Invisible-Bones-X-Rays/07_Edit-Project"
CLIP = REPO / "02_Video-Projects/003_Invisible-Bones-X-Rays/04_Generated-Clips/part05"
QA = EDIT / "_qa_part05_batch_a"
PROJECT = "https://flow.google.com/u/0/project/02ce23ba-3f6d-49ee-8177-67af2d9a1166"

# Stronger house bake for remint (UAT helix FAIL + 01 Explorer + 06 crown hair)
ANTI_HELIX = (
    " CRITICAL REMINT: X-ray / invisible beam / energy must be a straight soft cone or flat ray of light"
    " — NEVER a twisted double-helix, DNA spiral, corkscrew, braid, or glowing yellow helix."
    " HARD FAIL any DNA helix / double helix / spiral DNA prop / Periodic DNA desk."
    " Never open Create with Same DNA soft background; use Same Würzburg lab."
)
FACE = (
    " Readable Animistry cartoon faces with eyes and nose when any person appears"
    " — HARD FAIL blank mannequin ovals. No DNA helix."
)
NO_EXPLORER = (
    " HARD REJECT Explorer character on this plate — no boy with glasses/overcoat;"
    " diagram/lab/object only."
)
EXPLORER_CROWN = (
    " Explorer finished hair including full crown/top of head — HARD FAIL mid-crown unfinished,"
    " bald patch, flat unfinished scalp, or incomplete hair. Gold atom pin + satchel+compass on-model."
)

import sys

sys.path.insert(0, str(REPO / "04_Audio" / "tools"))
import orbit_flow_veo_ui as flow
import orbit_gemini_veo as veo

spec = importlib.util.spec_from_file_location("m", EDIT / "_mint_part04_batch_a.py")
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
board = {
    p["id"]: p
    for p in json.loads((EDIT / "parts/part-05_plates_v01.json").read_text())["plates"]
}

# KEEP 05+08 — do not remint
# Order: 02 first (helix blocker), then rest
JOBS = [
    ("02_what_are_xrays", ["X-RAYS", "invisible beam", "what X-rays"], False),
    ("01_chapter_new_seeing", ["A New Kind of Seeing", "Würzburg", "chapter open"], True),
    ("03_spectrum_past_uv", ["INVISIBLE LIGHT", "spectrum", "past visible"], False),
    ("04_soft_vs_bone", ["density", "soft tissue translucent", "bone denser"], False),
    ("06_explorer_diagram", ["Explorer", "own hand", "density diagram"], False),  # explorer plate
    ("07_why_groundbreaking", ["without a knife", "scalpel", "knife"], False),
    ("09_bigger_question", ["what else are we", "question-mark", "still blind"], False),
    ("10_cardboard_glow_hold", ["cardboard fluorescence", "fluorescence hold"], False),
    ("11_soft_return", ["soft fade energy", "end of part"], False),
]

KNOWN = {m.sha256_file(f) for f in CLIP.glob("*.mp4")}


def bake(pid: str) -> str:
    base = board[pid]["prompt"].strip()
    extra = ANTI_HELIX + FACE
    if pid == "01_chapter_new_seeing":
        extra += NO_EXPLORER
    if pid == "06_explorer_diagram":
        extra += EXPLORER_CROWN
    else:
        # non-06: reinforce no Explorer
        if pid != "06_explorer_diagram":
            extra += NO_EXPLORER
    return m.bake_prompt(base + extra)


def dump_cards(page):
    return page.evaluate(
        """() => {
      const out=[];
      const imgs=[...document.querySelectorAll('img')].filter(i=>/\\/asb\\//.test(i.src||''));
      for(const img of imgs){
        const ir=img.getBoundingClientRect();
        if(ir.width<80) continue;
        let el=img.parentElement, cardText='', depth=0;
        while(el && depth<8){
          const t=(el.innerText||'').replace(/\\s+/g,' ').trim();
          if(t.length>40 && t.length<900){ cardText=t; break; }
          el=el.parentElement; depth++;
        }
        out.push({x:ir.x+ir.width/2,y:ir.y+ir.height/2,w:ir.width,h:ir.height,t:cardText.slice(0,280)});
      }
      return out;
    }"""
    )


def find_card(page, needles):
    cards = dump_cards(page)
    for n in needles:
        for c in cards:
            if re.search(re.escape(n), c["t"], re.I):
                return {**c, "needle": n}
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
            const img=el.querySelector && el.querySelector('img[src*=\"/asb/\"]');
            if(!img) continue;
            const ir=img.getBoundingClientRect();
            if(ir.width<80) continue;
            return {x:ir.x+ir.width/2,y:ir.y+ir.height/2,t:raw.slice(0,100),via:'ancestor'};
          }
        }
        return null;
      }""",
            n,
        )
        if hit:
            return {**hit, "needle": n}
    return None


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


def pull(page, pid, needles, ver="v02"):
    page.goto(PROJECT, wait_until="domcontentloaded", timeout=120000)
    page.wait_for_timeout(2000)
    for _ in range(12):
        page.mouse.wheel(0, 1000)
        page.wait_for_timeout(300)
    page.mouse.wheel(0, -10000)
    page.wait_for_timeout(500)
    hit = find_card(page, needles)
    print("  hit", hit, flush=True)
    if not hit:
        return False
    page.mouse.click(hit["x"], hit["y"])
    page.wait_for_timeout(2800)
    body = page.locator("body").inner_text(timeout=5000)
    if not any(re.search(re.escape(n), body, re.I) for n in needles):
        print("  wrong open", flush=True)
        return False
    dest = CLIP / f"{pid}_{ver}.mp4"
    raw = download(page, dest)
    if not raw:
        print("  no download", flush=True)
        return False
    dest.write_bytes(raw)
    try:
        veo.strip_audio(dest)
    except Exception as e:
        print("  strip", e, flush=True)
    sha = m.sha256_file(dest)
    dur = m.probe_dur(dest)
    print(f"  sha={sha} dur={dur}", flush=True)
    if sha in KNOWN:
        print("  DUP reject", flush=True)
        dest.unlink()
        return False
    if dur < 6 or dur > 12:
        print("  bad dur", flush=True)
        dest.unlink()
        return False
    KNOWN.add(sha)
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
        "remint_reason": "UAT plate-first HARD FAIL helix/Explorer/crown",
        "assemble": "CLOSED",
        "ts": datetime.now(timezone.utc).isoformat(),
    }
    (QA / f"{pid}_{ver}_mint.json").write_text(json.dumps(report, indent=2) + "\n")
    print("LANDED", pid, ver, flush=True)
    return True


def create_pull(page, pid, needles, ver="v02"):
    page.goto(PROJECT, wait_until="domcontentloaded", timeout=120000)
    page.wait_for_timeout(1500)
    prompt = bake(pid)
    print("  prompt_len", len(prompt), flush=True)
    try:
        flow.configure_veo_settings(
            page, model="Veo 3.1 - Quality", frames_mode=False, ingredients_mode=False
        )
    except Exception as e:
        print("  settings", e, flush=True)
    page.keyboard.press("Escape")
    page.wait_for_timeout(300)
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
    # After submit, wait for progress then use a remint-distinct needle if possible
    remint_needles = list(needles) + ["CRITICAL REMINT", "straight soft cone", "Never a twisted"]
    while time.time() - t0 < 780:
        body = page.locator("body").inner_text(timeout=5000)
        pcts = [int(x) for x in re.findall(r"(\d{1,3})%", body)]
        active = [x for x in pcts if x < 100]
        has = any(re.search(re.escape(n), body, re.I) for n in remint_needles)
        line = f"  wait {int(time.time()-t0)}s pct={pcts[-2:] if pcts else None} active={active} has={has}"
        if line != last:
            print(line, flush=True)
            last = line
        if has and not active:
            page.wait_for_timeout(5000)
            break
        page.wait_for_timeout(8000)
    # Prefer matching remint-specific card text
    ok = pull(page, pid, ["CRITICAL REMINT", "straight soft cone"] + needles, ver=ver)
    if not ok:
        ok = pull(page, pid, needles, ver=ver)
    return ok


def main():
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp("http://127.0.0.1:9222")
        page = next(
            pg
            for pg in browser.contexts[0].pages
            if "flow.google.com" in (pg.url or "")
        )
        page.bring_to_front()
        for pid, needles, _ in JOBS:
            dest = CLIP / f"{pid}_v02.mp4"
            if dest.exists() and dest.stat().st_size > 150000:
                print("SKIP", pid, flush=True)
                continue
            print(f"\n=== REMINT {pid} v02 ===", flush=True)
            ok = create_pull(page, pid, needles, ver="v02")
            if not ok:
                print("FAIL", pid, flush=True)

    print("\n=== DONE REMINT PASS ===", flush=True)
    for f in sorted(CLIP.glob("*_v02.mp4")):
        print(m.sha256_file(f), f.name, flush=True)


if __name__ == "__main__":
    main()
