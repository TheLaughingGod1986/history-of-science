"""Checks-only pass for Short B v03 (the build finished at 21:07 on 3 Oct, but the Mini reboot killed its checks).
Runs the builder's own caption_check / gate / vo_check / freezedetect / stills on the existing mp4 and writes SHORTS_INDEX_v03.json."""
import json, sys, shutil, re
from pathlib import Path
here = Path(__file__).resolve().parent
src = (here / "_build_shorts_v03.py").read_text()
src = re.sub(r"if VENV_PY\.exists\(\).*?\n    os\.execv\(.*?\n", "", src, flags=re.S).split('if __name__ == "__main__":')[0]
ns = {"__file__": str(here / "_build_shorts_v03.py"), "__name__": "b3"}; exec(compile(src, "b3", "exec"), ns)
item = [s for s in ns["SHORTS"] if s["id"] == "s02_the_tied_arm"][0]
PROJ, VER, WORK = ns["PROJ"], ns["VER"], ns["WORK"]
mp4 = here / "hos_005_s02_the_tied_arm_v03.mp4"
tl = json.loads((WORK / item["id"] / "timeline.json").read_text())
vo = item["vo_dir"] / "hos_005_s02_the_tied_arm_vo_v03_fin.wav"
rec = {"id": item["id"], "air_date": item["air_date"], "file": mp4.relative_to(PROJ).as_posix(), "sha256": ns["sha256"](mp4),
       "duration_s": round(ns["probe"](mp4), 3), "vo": str(vo.relative_to(PROJ)), "vo_sha256": ns["sha256"](vo),
       "vo_s": round(ns["probe"](vo), 3), "hook": item["hook"].replace("**", ""), "plan": tl["plan"]}
shutil.rmtree(WORK / item["id"] / "frames", ignore_errors=True)
rec["caption_check"] = ns["caption_check"](mp4, tl["overlays"])
code, out = ns["run"]([sys.executable, str(ns["GATE"]), "check", str(mp4), "--air-date", item["air_date"]]); rec["gate"] = {"exit": code, "output": out}
code, out = ns["run"]([str(ns["VO_PY"]), str(ns["VO_CHECK"]), str(mp4), "--script", str(item["vo_dir"] / "s02_the_tied_arm.txt")]); rec["vo_check"] = {"exit": code, "output": out}
rec["freezedetect_starts"] = ns["freeze"](mp4)
for name, ss in (("title_frame", "11.5"), ("frame0", None), ("pulse_beat", "8.2"), ("loosen_beat", "10.5")):
    p = WORK / item["id"] / f"{mp4.stem}_{name}.jpg"
    ns["ff"](*(["-ss", ss] if ss else []), "-i", str(mp4), "-frames:v", "1", "-q:v", "3", str(p)); rec[f"{name}_still"] = p.relative_to(PROJ).as_posix()
ns["ICLOUD"].mkdir(parents=True, exist_ok=True); shutil.copy2(mp4, ns["ICLOUD"] / mp4.name); rec["icloud"] = str(ns["ICLOUD"] / mp4.name)
idx = {"scripts": "SHORTS_SCRIPTS_v02.md", "task": "PR #180 comments 5952762841 / 5953047660",
       "change": "Short B only: 'The hand went pale.' -> 'Below the band, the pulse stopped.' (vo_v03b take a); arm plates 03/04 graded_v04; otherwise v02",
       "shorts": {item["id"]: rec}}
(here / f"SHORTS_INDEX_{VER}.json").write_text(json.dumps(idx, indent=2) + "\n")
print("SHA", rec["sha256"], rec["duration_s"], "captions", rec["caption_check"]); print(rec["gate"]["output"]); print(rec["vo_check"]["output"])
print("freeze", rec["freezedetect_starts"])
