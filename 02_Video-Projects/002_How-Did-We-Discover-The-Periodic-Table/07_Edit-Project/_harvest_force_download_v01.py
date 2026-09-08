#!/usr/bin/env python3
"""Force-download newest Flow gallery clip (Download media / network play).

Usage:
  python3 _harvest_force_download_v01.py \\
    --project https://flow.google.com/u/1/project/<id> \\
    --dest .../plate_v01.mp4
"""
from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO / "04_Audio" / "tools"))

import orbit_flow_veo_ui as flow  # noqa: E402
import orbit_gemini_veo as veo  # noqa: E402

flow.FLOW_HOME = "https://flow.google.com/u/1/"
PROFILE = Path.home() / ".playwright-hos-flow-profile"


def probe_dur(path: Path) -> float:
    return float(
        subprocess.check_output(
            [
                "ffprobe", "-v", "error", "-show_entries", "format=duration",
                "-of", "default=nw=1:nk=1", str(path),
            ],
            text=True,
        ).strip()
    )


def accept_mp4(path: Path, dest: Path) -> bool:
    if not path.exists() or path.stat().st_size < 400_000:
        print(f"  reject small/missing {path}", flush=True)
        return False
    raw = path.read_bytes()
    if raw[:3] == b"\xff\xd8\xff":
        print(f"  REJECT jpeg bytes={len(raw)}", flush=True)
        return False
    if b"ftyp" not in raw[:64]:
        print(f"  REJECT non-mp4 head={raw[:16]!r}", flush=True)
        return False
    veo.strip_audio(path)
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.unlink(missing_ok=True)
    shutil.move(str(path), str(dest))
    dur = probe_dur(dest)
    print(f"SAVED {dest} bytes={dest.stat().st_size} dur={dur:.2f}", flush=True)
    return 5.0 <= dur <= 40.0


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--project", required=True)
    ap.add_argument("--dest", required=True, type=Path)
    ap.add_argument("--newest", action="store_true", default=True)
    args = ap.parse_args()
    project = args.project.rstrip("/")
    dest = args.dest

    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        ctx, page = flow.launch_context(
            p, headed=True, profile=flow.profile_path(PROFILE)
        )
        try:
            page.goto(project, wait_until="domcontentloaded", timeout=120_000)
            page.wait_for_timeout(5000)
            flow.dismiss_banners(page)

            thumbs = []
            for i in range(40):
                thumbs = flow.collect_gallery_asb_srcs(page)
                print(f"  poll {i} thumbs={len(thumbs)}", flush=True)
                if len(thumbs) >= 1:
                    break
                page.wait_for_timeout(4000)
                page.reload(wait_until="domcontentloaded")
                page.wait_for_timeout(2500)
                flow.dismiss_banners(page)

            if not thumbs:
                raise SystemExit("FAIL: no gallery thumbs")

            # Prefer Videos filter so we don't open the start-frame JPEG.
            try:
                page.get_by_text("Videos", exact=True).first.click(timeout=5000)
                page.wait_for_timeout(1500)
                thumbs = flow.collect_gallery_asb_srcs(page) or thumbs
                print(f"  after Videos tab thumbs={len(thumbs)}", flush=True)
            except Exception as e:
                print(f"  Videos tab warn: {e}", flush=True)

            src = thumbs[-1]
            page.evaluate(
                """(src)=>{
                  const els=[...document.querySelectorAll('img,video')];
                  const el=els.find(e=>(e.currentSrc||e.src||'')===src)
                    || els.find(e=>(e.currentSrc||e.src||'').includes('/asb/'));
                  if(el){el.scrollIntoView({block:'center'}); el.click();}
                }""",
                src,
            )
            page.wait_for_timeout(2500)
            flow.dismiss_banners(page)

            net_hits: list[bytes] = []

            def on_resp(resp) -> None:
                try:
                    u = (resp.url or "").lower()
                    ct = (resp.headers.get("content-type") or "").lower()
                    if resp.status != 200:
                        return
                    if not (
                        "flow-content.google/video" in u
                        or "googlevideo.com" in u
                        or "videoplayback" in u
                        or ("video" in ct and "mp4" in ct)
                    ):
                        return
                    body = resp.body()
                    if len(body) > 150_000 and b"ftyp" in body[:64]:
                        net_hits.append(body)
                        print(f"  net hit bytes={len(body)}", flush=True)
                except Exception:
                    pass

            page.on("response", on_resp)

            for label in ("Play Video", "Play", "Replay"):
                loc = page.get_by_role("button", name=re.compile(label, re.I))
                if loc.count() and loc.first.is_visible():
                    print(f"  click {label}", flush=True)
                    try:
                        loc.first.click(timeout=5000)
                    except Exception as e:
                        print(f"  play warn {e}", flush=True)
                    page.wait_for_timeout(8000)
                    break

            if net_hits:
                tmp = dest.with_suffix(".net.tmp.mp4")
                tmp.write_bytes(net_hits[-1])
                if accept_mp4(tmp, dest):
                    return

            # Prefer Videos tab so we open the clip, not the start-frame JPEG.
            try:
                page.get_by_text("Videos", exact=True).first.click(timeout=5000)
                page.wait_for_timeout(1500)
                thumbs2 = flow.collect_gallery_asb_srcs(page)
                if thumbs2:
                    src2 = thumbs2[-1]
                    page.evaluate(
                        """(src)=>{
                          const els=[...document.querySelectorAll('img,video')];
                          const el=els.find(e=>(e.currentSrc||e.src||'')===src)
                            || els.find(e=>(e.currentSrc||e.src||'').includes('/asb/'));
                          if(el){el.scrollIntoView({block:'center'}); el.click();}
                        }""",
                        src2,
                    )
                    page.wait_for_timeout(2000)
            except Exception as e:
                print(f"  Videos tab warn: {e}", flush=True)

            # CDP download path — Playwright expect_download often closes mid-save.
            dl_dir = dest.parent / "_dl"
            dl_dir.mkdir(parents=True, exist_ok=True)
            for old in dl_dir.glob("*"):
                if old.is_file():
                    old.unlink()
            try:
                cdp = ctx.new_cdp_session(page)
                cdp.send(
                    "Page.setDownloadBehavior",
                    {"behavior": "allow", "downloadPath": str(dl_dir)},
                )
                print(f"  CDP downloadPath={dl_dir}", flush=True)
            except Exception as e:
                print(f"  CDP download warn: {e}", flush=True)

            btn = page.get_by_role("button", name=re.compile(r"Download media", re.I))
            if not (btn.count() and btn.first.is_visible()):
                btn = page.locator('button[aria-label*="Download media" i]').first
            print("Download media…", flush=True)
            tmp = dest.with_suffix(".dl.tmp.mp4")
            tmp.unlink(missing_ok=True)
            try:
                if hasattr(btn, "count"):
                    btn.first.click(force=True)
                else:
                    btn.click(force=True)
                page.wait_for_timeout(900)
                item = page.evaluate(
                    """() => {
                      const items=[...document.querySelectorAll('*')];
                      const scored=[];
                      for (const el of items) {
                        const t=((el.innerText||'')+' '
                          +(el.getAttribute('aria-label')||'')).trim().replace(/\\n/g,' ');
                        if (!t || t.length>60) continue;
                        const r=el.getBoundingClientRect();
                        if (r.width<20 || r.height<12) continue;
                        let score=0;
                        if (/720p/i.test(t)) score+=12;
                        if (/1080p/i.test(t)) score+=10;
                        if (/\\bmp4\\b/i.test(t)) score+=10;
                        if (/upscaled/i.test(t)) score+=3;
                        if (/1k|original size|image|jpeg|png|still|fullscreen/i.test(t)
                            && !/mp4|1080|720|upscaled/i.test(t)) score-=12;
                        if (score>0) scored.push({score,t:t.slice(0,60),
                          x:r.x+r.width/2,y:r.y+r.height/2});
                      }
                      scored.sort((a,b)=>b.score-a.score);
                      return scored[0]||null;
                    }"""
                )
                if item:
                    print(f"  menu → {item}", flush=True)
                    page.mouse.click(item["x"], item["y"])
                else:
                    print("  no menu item — waiting for direct download", flush=True)
                # Wait for file on disk (CDP path)
                raw = None
                deadline = time.time() + 90
                while time.time() < deadline:
                    files = [
                        f for f in dl_dir.iterdir()
                        if f.is_file()
                        and not f.name.endswith(".crdownload")
                        and not f.name.endswith(".tmp")
                    ]
                    big = [f for f in files if f.stat().st_size > 400_000]
                    if big:
                        cand = max(big, key=lambda p: p.stat().st_size)
                        raw = cand.read_bytes()
                        print(f"  CDP file ok {cand.name} bytes={len(raw)}", flush=True)
                        break
                    time.sleep(1.5)
                if raw is None and net_hits:
                    raw = net_hits[-1]
                    print(f"  fallback net bytes={len(raw)}", flush=True)
                if raw:
                    tmp.write_bytes(raw)
                    if accept_mp4(tmp, dest):
                        return
            except Exception as e:
                print(f"  download flow err: {e}", flush=True)
                if net_hits:
                    tmp = dest.with_suffix(".net2.tmp.mp4")
                    tmp.write_bytes(net_hits[-1])
                    if accept_mp4(tmp, dest):
                        return

            print("FAIL: no usable mp4", flush=True)
            raise SystemExit(2)
        finally:
            try:
                ctx.close()
            except Exception:
                pass


if __name__ == "__main__":
    main()
