#!/usr/bin/env python3
"""Force-download finished Flow mp4 from Part 03 v08 project (net-capture resilient).

Default: plate 08 from project minted 2026-09-07.
Usage:
  python3 _harvest_part03_v08_force_download.py \\
    [--project URL] [--dest path.mp4]
"""
from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO / "04_Audio" / "tools"))

import orbit_flow_veo_ui as flow  # noqa: E402
import orbit_gemini_veo as veo  # noqa: E402

flow.FLOW_HOME = "https://flow.google.com/u/1/"
DEFAULT_PROJ = "https://flow.google.com/u/1/project/2b3fce66-07a4-4232-8523-06e9dbcf4a9f"
DEFAULT_DEST = (
    Path(__file__).resolve().parents[1]
    / "04_Generated-Clips/part03/raw/v08_fast/08_property_waves_v08.mp4"
)
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
    ap.add_argument("--project", default=DEFAULT_PROJ)
    ap.add_argument("--dest", type=Path, default=DEFAULT_DEST)
    args = ap.parse_args()
    project = args.project.split("?")[0].rstrip("/")
    dest: Path = args.dest

    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        ctx, page = flow.launch_context(
            p, headed=True, profile=flow.profile_path(PROFILE)
        )
        try:
            page.goto(project, wait_until="domcontentloaded", timeout=120_000)
            page.wait_for_timeout(4000)
            flow.dismiss_banners(page)

            for label in (
                "Generating video from start frame",
                "Play Video",
                "Play",
            ):
                loc = page.get_by_role("button", name=re.compile(re.escape(label), re.I))
                if loc.count() and loc.first.is_visible():
                    print(f"click chip {label!r}", flush=True)
                    try:
                        loc.first.click(timeout=5000)
                    except Exception as e:
                        print(f"  chip click warn {e}", flush=True)
                    page.wait_for_timeout(1500)

            thumbs = flow.collect_gallery_asb_srcs(page)
            print(f"thumbs={len(thumbs)}", flush=True)
            tmp = dest.with_suffix(".tmp.mp4")
            tmp.unlink(missing_ok=True)
            captured: list[bytes] = []
            got = flow.harvest_agent_gallery_mp4(
                page, tmp, captured, before_asb=set()
            )
            print(f"harvest_agent got={got}", flush=True)
            if got and accept_mp4(tmp, dest):
                raise SystemExit(0)

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
            btn = page.get_by_role("button", name=re.compile(r"Download media", re.I))
            if not (btn.count() and btn.first.is_visible()):
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
                    page.wait_for_timeout(2000)
                btn = page.get_by_role(
                    "button", name=re.compile(r"Download media", re.I)
                )

            if btn.count() and btn.first.is_visible():
                print("Download media click", flush=True)
                out = dest.with_suffix(".dl.tmp")
                out.unlink(missing_ok=True)
                try:
                    with page.expect_download(timeout=45_000) as di:
                        btn.first.click(force=True)
                        page.wait_for_timeout(600)
                        item = page.evaluate(
                            """() => {
                              const items=[...document.querySelectorAll(
                                '[role=menuitem],button,a,mat-menu-item,.mat-mdc-menu-item'
                              )];
                              for (const el of items) {
                                const t=((el.innerText||'')+' '
                                  +(el.getAttribute('aria-label')||'')).trim();
                                if (/generat/i.test(t)) continue;
                                if (/image|jpeg|png|jpg|gif|still/i.test(t)) continue;
                                if (/mp4|original|full|1080|720|\\bvideo\\b/i.test(t)) {
                                  const r=el.getBoundingClientRect();
                                  if (r.width>20 && r.height>12)
                                    return {t:t.slice(0,60),
                                      x:r.x+r.width/2,y:r.y+r.height/2};
                                }
                              }
                              return null;
                            }"""
                        )
                        if item:
                            print(f"  menu {item}", flush=True)
                            page.mouse.click(item["x"], item["y"])
                    dl = di.value
                    try:
                        pth = dl.path()
                        if pth:
                            out.write_bytes(Path(pth).read_bytes())
                    except Exception as e:
                        print(f"  path warn {e}", flush=True)
                        try:
                            dl.save_as(str(out))
                        except Exception as e2:
                            print(f"  save_as warn {e2}", flush=True)
                    if accept_mp4(out, dest):
                        raise SystemExit(0)
                except SystemExit:
                    raise
                except Exception as e:
                    print(f"  expect_download warn {e}", flush=True)

            if net_hits:
                out = dest.with_suffix(".net.tmp")
                out.write_bytes(net_hits[-1])
                if accept_mp4(out, dest):
                    raise SystemExit(0)

            print("FAIL: no usable mp4 from project", flush=True)
            raise SystemExit(2)
        finally:
            try:
                ctx.close()
            except Exception:
                pass


if __name__ == "__main__":
    main()
