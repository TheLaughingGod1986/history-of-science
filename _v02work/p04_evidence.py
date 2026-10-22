import json, subprocess, re
from pathlib import Path
E = Path("07_Edit-Project"); X = Path("09_Final-Export"); W = Path.home()/"YouTube/hos-005-blood/_v02work/ev"; W.mkdir(exist_ok=True)
m1 = json.load(open(E/"part04_rough_v01_meta.json")); m2 = json.load(open(E/"part04_rough_v02_meta.json"))
p1 = {p["id"]: p for p in m1["plates"]}
print("v01", m1["sha256"], m1["duration_s"], "freeze", m1.get("freeze_events_0p8s"))
print("v02", m2["sha256"], m2["duration_s"], "freeze", m2.get("freeze_events_0p8s"), "vo", m2["vo"], m2["vo_sha256"][:12])
for b in m2["plates"]:
    a = p1.get(b["id"], {})
    ch = [f for f in ("sha256", "in_s", "use_s") if a.get(f) != b.get(f)]
    print(f"{b['id']:24s} part_t0 {a.get('part_t0')} -> {b['part_t0']}  {'CHANGED ' + ','.join(ch) if ch else 'same plate'}")
def lufs(f):
    e = subprocess.run(["ffmpeg","-hide_banner","-nostats","-i",str(f),"-af","ebur128=peak=true","-f","null","-"],capture_output=True,text=True).stderr
    s = e[e.rfind("Summary:"):]
    return re.search(r"I:\s+(-?[\d.]+) LUFS", s).group(1), re.search(r"LRA:\s+([\d.]+) LU", s).group(1), re.search(r"Peak:\s+(-?[\d.]+) dBFS", s).group(1)
for v in ("v01", "v02"):
    print(v, "LUFS I / LRA / TP", lufs(X/f"hos_005_part04_rough_{v}.mp4"))
for t in (15.0, 21.0, 27.0, 33.0):
    subprocess.run(["ffmpeg","-y","-v","error","-ss",str(t),"-i",str(X/"hos_005_part04_rough_v02.mp4"),"-frames:v","1","-vf","scale=640:-1",str(W/f"p04v02_{t:04.1f}.jpg")],check=True)
subprocess.run(["ffmpeg","-y","-v","error"] + sum([["-i",str(W/f"p04v02_{t:04.1f}.jpg")] for t in (15.0,21.0,27.0,33.0)],[]) +
               ["-filter_complex","[0][1][2][3]xstack=inputs=4:layout=0_0|w0_0|0_h0|w0_h0","-q:v","3",str(W/"p04v02_arm_sheet.jpg")],check=True)
print("sheet", W/"p04v02_arm_sheet.jpg")
