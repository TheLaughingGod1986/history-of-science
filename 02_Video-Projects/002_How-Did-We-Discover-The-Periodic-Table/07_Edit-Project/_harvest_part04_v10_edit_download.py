#!/usr/bin/env python3
"""Download Part04 v10 plate 06 from a known Flow project (no Facebook pollution).

Prefer --edit URL (media edit page). Else open --project, filter Videos, open newest.
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
                "ffprobe",
                "-v",
                "error",
                "-show_entries",
                "format=duration",
                "-of",
                "default=nw=1:nk=1",
                str(path),
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


def abort_if_polluted(page) -> None:
    u = (page.url or "").lower()
    if "facebook.com" in u or "instagram.com" in u:
        raise SystemExit(f"FAIL: polluted navigation {page.url}")


def click_download_720(page, ctx, dl_dir: Path) -> Path | None:
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
        print(f"  CDP warn: {e}", flush=True)

    # Open download menu
    opened = False
    for sel in (
        page.get_by_role("button", name=re.compile(r"Download media", re.I)),
        page.locator('button[aria-label*="Download media" i]'),
        page.get_by_role("button", name=re.compile(r"^Download$", re.I)),
        page.get_by_text("Download media", exact=False),
    ):
        try:
            if sel.count() and sel.first.is_visible():
                sel.first.click(timeout=8000, force=True)
                opened = True
                page.wait_for_timeout(900)
                break
        except Exception as e:
            print(f"  open download warn: {e}", flush=True)
    if not opened:
        print("  Download control not found", flush=True)
        return None

    # Prefer 720p / mp4 menu item
    item = page.evaluate(
        """() => {
          const items=[...document.querySelectorAll('*')];
          const scored=[];
          for (const el of items) {
            const t=((el.innerText||'')+' '
              +(el.getAttribute('aria-label')||'')).trim().replace(/\\n/g,' ');
            if (!t || t.length>80) continue;
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
    clicked = False
    # Prefer leaf "720p" / "Original size" — avoid clicking the whole menu blob.
    for sel in (
        page.get_by_text("720p", exact=True),
        page.locator("text=720p"),
        page.get_by_role("menuitem", name=re.compile(r"720p", re.I)),
    ):
        try:
            n = min(sel.count(), 8)
            for i in range(n):
                el = sel.nth(i)
                box = el.bounding_box()
                if not box or box["width"] >= 400 or box["height"] >= 80:
                    continue
                el.click(timeout=3000, force=True)
                print(f"  leaf click 720p i={i} box={box}", flush=True)
                clicked = True
                break
            if clicked:
                break
        except Exception as e:
            print(f"  leaf warn: {e}", flush=True)
    if not clicked and item and item.get("t", "").strip() in ("720p", "Original size"):
        print(f"  menu → {item}", flush=True)
        page.mouse.click(item["x"], item["y"])
        clicked = True
    if not clicked:
        for label in ("720p", "Original size (720p)", "1080p", "mp4"):
            try:
                page.get_by_text(label, exact=False).first.click(timeout=2000)
                print(f"  clicked text {label}", flush=True)
                clicked = True
                break
            except Exception:
                continue
    if not clicked:
        print("  could not click a resolution item", flush=True)
        return None

    deadline = time.time() + 90
    while time.time() < deadline:
        abort_if_polluted(page)
        files = [
            f
            for f in dl_dir.iterdir()
            if f.is_file()
            and not f.name.endswith(".crdownload")
            and not f.name.endswith(".tmp")
        ]
        big = [f for f in files if f.stat().st_size > 400_000]
        if big:
            cand = max(big, key=lambda p: p.stat().st_size)
            print(f"  CDP file ok {cand.name} bytes={cand.stat().st_size}", flush=True)
            return cand
        time.sleep(1.5)
    return None


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--project",
        default="https://flow.google.com/u/1/project/8bbeb102-a2d7-4f17-bb3e-120c3f09d996",
    )
    ap.add_argument(
        "--edit",
        default=(
            "https://flow.google.com/u/1/project/"
            "8bbeb102-a2d7-4f17-bb3e-120c3f09d996/edit/"
            "5fd3ec92-6c41-4ef3-ad5a-382024fe810c"
        ),
        help="Direct Flow edit URL for the clip (preferred). Empty string skips.",
    )
    ap.add_argument(
        "--dest",
        type=Path,
        default=Path(
            "/Users/benjaminoats/YouTube/History Of Science/"
            "02_Video-Projects/002_How-Did-We-Discover-The-Periodic-Table/"
            "04_Generated-Clips/part04/raw/v10_fast/"
            "06_explorer_leaves_gap_v10.try2.tmp.mp4"
        ),
    )
    args = ap.parse_args()
    dest = args.dest
    dl_dir = dest.parent / "_dl"
    dl_dir.mkdir(parents=True, exist_ok=True)

    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        ctx, page = flow.launch_context(
            p, headed=True, profile=flow.profile_path(PROFILE)
        )
        # Block social pollution that previously stole the harvest.
        try:
            ctx.route(
                re.compile(r"https?://([^/]+\.)?(facebook|instagram)\.com/.*"),
                lambda route: route.abort(),
            )
        except Exception as e:
            print(f"  route warn: {e}", flush=True)

        try:
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

            urls = [u for u in (args.edit, args.project) if u]
            got = None
            for url in urls:
                print(f"goto {url}", flush=True)
                page.goto(url, wait_until="domcontentloaded", timeout=120_000)
                page.wait_for_timeout(5000)
                flow.dismiss_banners(page)
                abort_if_polluted(page)
                print(f"  url={page.url}", flush=True)

                # If on project gallery, open Videos + newest thumb first.
                if "/edit/" not in (page.url or ""):
                    try:
                        page.get_by_text("Videos", exact=True).first.click(timeout=8000)
                        page.wait_for_timeout(1500)
                    except Exception as e:
                        print(f"  Videos warn: {e}", flush=True)
                    thumbs = flow.collect_gallery_asb_srcs(page)
                    print(f"  thumbs={len(thumbs)}", flush=True)
                    if thumbs:
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
                        page.wait_for_timeout(3000)
                        abort_if_polluted(page)

                for label in ("Play Video", "Play", "Replay"):
                    loc = page.get_by_role("button", name=re.compile(label, re.I))
                    if loc.count() and loc.first.is_visible():
                        try:
                            loc.first.click(timeout=4000)
                            page.wait_for_timeout(6000)
                        except Exception:
                            pass
                        break

                if net_hits:
                    tmp = dest.with_suffix(".net.tmp.mp4")
                    tmp.write_bytes(net_hits[-1])
                    if accept_mp4(tmp, dest):
                        return

                cand = click_download_720(page, ctx, dl_dir)
                if cand is not None:
                    tmp = dest.with_suffix(".dl.tmp.mp4")
                    shutil.copy2(cand, tmp)
                    if accept_mp4(tmp, dest):
                        return
                print("  path failed; trying next URL…", flush=True)

            print("FAIL: no usable mp4", flush=True)
            raise SystemExit(2)
        finally:
            try:
                ctx.close()
            except Exception:
                pass


if __name__ == "__main__":
    main()
