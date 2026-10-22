"""Short B v03: put the re-voiced 'The hand went cold.' where 'The hand went pale.' was in the finished Short VO
(hos_005_s02_the_tied_arm_vo_v01_fin.wav). Same start (7.053 s), RMS-matched, 10 ms fades, file length unchanged.
Writes hos_005_s02_the_tied_arm_vo_v03_fin_<take>.wav + _align.json (old alignment with pale->cold remapped)."""
import json, subprocess, sys
from pathlib import Path
import numpy as np
S = Path.home()/"YouTube/hos-005-blood/02_Video-Projects/005_How-Harvey-Proved-Blood-Circulates/10_Shorts/vo_v01"
SR = 48000; OLD0, OLD1 = 7.0533, 8.1818; Z0, Z1 = 6.70, 8.55; NEW0 = 6.96  # new speech starts 0.09 s earlier so the 1.3 s line fits the pause
# speech spans of each context take, from silencedetect n=-45dB d=0.05 (alignment is too coarse)
SPAN = {"a": (3.652, 4.963), "b": (3.738, 5.029), "c": (4.603, 5.932)}
def dec(p):
    return np.frombuffer(subprocess.run(["ffmpeg","-v","error","-i",str(p),"-f","f32le","-ar","48000","-ac","2","-"],capture_output=True,check=True).stdout,dtype=np.float32).reshape(-1,2).copy()
base = dec(S/"hos_005_s02_the_tied_arm_vo_v01_fin.wav")
rms = lambda x: float(np.sqrt(np.mean(x**2)))
old = base[int(OLD0*SR):int(OLD1*SR)]
for take in sys.argv[1:]:
    a = json.load(open(f"s02_line_v03_ctx_{take}_align.json")); x = dec(f"s02_line_v03_ctx_{take}.mp3")
    txt = "".join(a["characters"]); i0 = txt.index("The hand"); i1 = txt.index("cold.") + 4
    s = int((SPAN[take][0]-0.02)*SR); e = int((SPAN[take][1]+0.03)*SR)
    seg = x[s:e].copy(); seg *= rms(old)/max(rms(seg),1e-9)
    f = int(0.010*SR); ramp = np.linspace(0,1,f)[:,None]; seg[:f] *= ramp; seg[-f:] *= ramp[::-1]
    L = len(seg)/SR; print(take, "speech", round(L,3), "s; old", round(OLD1-OLD0,3))
    if NEW0 + L > Z1 - 0.15: print("  too long"); continue
    out = base.copy(); out[int(Z0*SR):int(Z1*SR)] = 0; p = int(NEW0*SR); out[p:p+len(seg)] = seg
    peak = float(np.abs(out).max()); print("  peak dB", round(20*np.log10(peak),2))
    w = f"hos_005_s02_the_tied_arm_vo_v03_fin_{take}.wav"
    subprocess.run(["ffmpeg","-y","-v","error","-f","f32le","-ar","48000","-ac","2","-i","-","-c:a","pcm_s16le",w],input=np.clip(out,-1,1).tobytes(),check=True)
    # alignment: same as old, but chars of 'pale.' -> 'cold.' and the sentence's times scaled to the new length
    al = json.load(open(S/"hos_005_s02_the_tied_arm_vo_v01_fin_align.json")); ch = al["characters"]
    full = "".join(ch); k = full.index("The hand went pale."); k1 = k + len("The hand went pale.")
    for j, c in enumerate("The hand went cold."): ch[k+j] = c
    # keep the sentence's first char time (so the builder's cut at word 16 - 0.15 s is unchanged), stretch to the new end
    A0 = al["character_start_times_seconds"][k]; A1 = al["character_end_times_seconds"][k1-1]; B1 = NEW0 + L
    sc = (B1 - A0) / (A1 - A0)
    for key in ("character_start_times_seconds","character_end_times_seconds"):
        al[key] = [round(A0 + (t-A0)*sc, 4) if k <= j < k1 else t for j, t in enumerate(al[key])]
    json.dump(al, open(w.replace(".wav","_align.json"),"w"), indent=1); print("  wrote", w)
