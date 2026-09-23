#!/usr/bin/env python3
"""HOS 003 Premiere upload — remaps HOS 002 Studio bytecode to this film's assets.

Requires Mini Chrome CDP :9460 with ~/.hos-chrome-youtube-studio logged into
@HistoryOfScienceYT. Exit 2 = LOGIN_REQUIRED.
"""
from __future__ import annotations

import json
import marshal
import subprocess
import sys
import time
import types
import urllib.request
from pathlib import Path

PYC = Path(
    "/Users/benjaminoats/YouTube/History Of Science/02_Video-Projects/"
    "002_How-Did-We-Discover-The-Periodic-Table/11_Upload-Package/Schedule/"
    "__pycache__/_upload_hos_002_premiere_v01.cpython-314.pyc"
)
PROJ3 = Path(
    "/Users/benjaminoats/YouTube/History Of Science/02_Video-Projects/"
    "003_Invisible-Bones-X-Rays"
)
SCHED = PROJ3 / "11_Upload-Package/Schedule"
EV = SCHED / "evidence_2026-09-23_premiere"
EV.mkdir(parents=True, exist_ok=True)

REPLACEMENTS = {
    "09_Final-Export/hos_002_periodic_table_full_v02.mp4": str(
        PROJ3 / "09_Final-Export/hos_003_full_polish_v01.mp4"
    ),
    "8a5b8dde713cd4d6d2834b49635443ebf5fda1a83de92688bf79ca91746de31f": (
        "be6d156296dcfbf0ed632632109edc71e3dc7ed60bced442e1cfa9bc44dc4f98"
    ),
    "08_Thumbnail/Selected/hos_002_thumb_A_gallium_live_v02.jpg": str(
        PROJ3 / "08_Thumbnail/Selected/hos_003_thumb_long_xrays_v03.jpg"
    ),
    "How Did We Discover the Periodic Table?": "How Did We Discover X-rays?",
    "Descriptions/periodic_table_long_description_v01.txt": str(
        SCHED / "hos_003_long_description_v01.txt"
    ),
    "Tags/periodic_table_long_tags_v01.txt": str(SCHED / "hos_003_long_tags_v01.txt"),
    "Pinned-Comments/periodic_table_long_pinned-comment_v01.txt": str(
        PROJ3 / "11_Upload-Package/Pinned-Comments/hos_003_long_pinned-comment_v01.txt"
    ),
    "Schedule/evidence_2026-09-11_premiere": str(EV),
    "/tmp/hos_chrome_9460_002.log": "/tmp/hos_chrome_9460_003.log",
    "2026-09-17T18:00:00+00:00": "2026-09-24T17:00:00+00:00",
    "2026-09-17": "2026-09-24",
    r"17\s+(Sept|Sep|September)\s+2026": r"24\s+(Sept|Sep|September)\s+2026",
}


def remap_const(x):
    if isinstance(x, str):
        y = x
        for a, b in REPLACEMENTS.items():
            y = y.replace(a, b)
        y = y.replace("17 Sep 2026", "24 Sep 2026")
        y = y.replace("17 September 2026", "24 September 2026")
        y = y.replace("Thursday 17 Sep 2026 19:00", "Thursday 24 Sep 2026 18:00")
        # Premiere clock only (002 used 19:00)
        if "Premiere" in y or "premiere" in y or "18:00" in y or "19:00" in y:
            y = y.replace("19:00", "18:00")
        return y
    if isinstance(x, types.CodeType):
        return remap_code(x)
    if isinstance(x, tuple):
        return tuple(remap_const(i) for i in x)
    return x


def remap_code(code: types.CodeType) -> types.CodeType:
    return code.replace(co_consts=tuple(remap_const(c) for c in code.co_consts))


def ensure_chrome() -> None:
    try:
        urllib.request.urlopen("http://127.0.0.1:9460/json/version", timeout=1).read()
        print("CDP_UP", flush=True)
        return
    except Exception:
        pass
    profile = str(Path.home() / ".hos-chrome-youtube-studio")
    for name in ("SingletonLock", "SingletonSocket", "SingletonCookie"):
        p = Path(profile) / name
        if p.exists():
            try:
                p.unlink()
            except Exception:
                pass
    log = "/tmp/hos_chrome_9460_003.log"
    subprocess.Popen(
        [
            "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
            "--remote-debugging-port=9460",
            "--remote-allow-origins=*",
            f"--user-data-dir={profile}",
            "--no-first-run",
            "--no-default-browser-check",
            "--disable-background-timer-throttling",
            "--disable-renderer-backgrounding",
            "https://studio.youtube.com/channel/UCXp7HkBIl1LgaznXuZHJyRg",
        ],
        stdout=open(log, "w"),
        stderr=subprocess.STDOUT,
    )
    for _ in range(30):
        time.sleep(0.5)
        try:
            urllib.request.urlopen("http://127.0.0.1:9460/json/version", timeout=1).read()
            print("CDP_STARTED", flush=True)
            return
        except Exception:
            pass
    raise SystemExit("chrome_failed_to_start")


def probe_login() -> str:
    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp("http://127.0.0.1:9460")
        ctx = browser.contexts[0]
        page = ctx.pages[0] if ctx.pages else ctx.new_page()
        for pg in ctx.pages:
            if any(x in pg.url for x in ("studio.youtube", "accounts.google", "youtube.com")):
                page = pg
                break
        page.wait_for_timeout(1500)
        page.screenshot(path=str(EV / "00_login_probe.png"))
        url = page.url
        print("URL", url[:220], flush=True)
        if any(x in url for x in ("accountchooser", "signin", "ServiceLogin", "identifier")):
            (EV / "LOGIN_REQUIRED.json").write_text(
                json.dumps({"ok": False, "reason": "LOGIN_REQUIRED", "url": url}, indent=2)
            )
            raise SystemExit(2)
        if "UCXp7HkBIl1LgaznXuZHJyRg" not in url and "studio.youtube.com" not in url:
            page.goto(
                "https://studio.youtube.com/channel/UCXp7HkBIl1LgaznXuZHJyRg",
                wait_until="domcontentloaded",
                timeout=60000,
            )
            page.wait_for_timeout(2000)
            url = page.url
            print("AFTER_GOTO", url[:220], flush=True)
            if any(x in url for x in ("accountchooser", "signin", "ServiceLogin", "identifier")):
                (EV / "LOGIN_REQUIRED.json").write_text(
                    json.dumps({"ok": False, "reason": "LOGIN_REQUIRED", "url": url}, indent=2)
                )
                raise SystemExit(2)
        return url


def main() -> None:
    ensure_chrome()
    time.sleep(1)
    probe_login()
    print("STUDIO_READY — running remapped HOS 002 premiere uploader", flush=True)
    code = remap_code(marshal.loads(PYC.read_bytes()[16:]))
    fake = str(SCHED / "_upload_hos_003_premiere_v01.py")
    # Load the 002 module without running its __main__ so we can patch
    # PREMIERE_DAY (bytecode LOAD_SMALL_INT 17 is not a remappable string).
    g = {"__name__": "hos003_premiere", "__file__": fake, "__builtins__": __builtins__}
    sys.argv = [fake] + sys.argv[1:]
    exec(code, g)
    g["PREMIERE_DAY"] = 24
    g["PREMIERE_TIME"] = "18:00"
    g["PREMIERE_LABEL"] = "Thursday 24 Sep 2026 18:00 Europe/London"
    g["PREMIERE_ISO"] = "2026-09-24T17:00:00+00:00"
    g["PREMIERE_MONTH"] = "September"
    g["PREMIERE_MONTH_SHORT"] = "Sept"
    print(
        f"PREMIERE_DAY={g['PREMIERE_DAY']} TIME={g['PREMIERE_TIME']} LABEL={g['PREMIERE_LABEL']}",
        flush=True,
    )
    extra = sys.argv[1:]
    if extra and extra[0] not in ("--id", "--premiere-tick", "--finish") and len(extra[0]) >= 8:
        raise SystemExit(g["finish_existing"](extra[0]))
    if "--premiere-tick" in extra:
        vid = extra[extra.index("--premiere-tick") + 1]
        raise SystemExit(g["premiere_tick_existing"](vid))
    if "--finish" in extra:
        vid = extra[extra.index("--finish") + 1]
        raise SystemExit(g["finish_existing"](vid))
    if "--id" in extra:
        vid = extra[extra.index("--id") + 1]
        raise SystemExit(g["finish_existing"](vid))
    raise SystemExit(g["main"]())


if __name__ == "__main__":
    main()
