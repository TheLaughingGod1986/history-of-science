"""Short B v03 (PR #180 desk 5952762841): replace 'The hand went pale.' in the finished Short VO
(vo_v01/hos_005_s02_the_tied_arm_vo_v01_fin.wav) with the new eleven_v3 take of 'Below the band, the pulse stopped.'
New speech starts where the old did (NEW0); everything after the old sentence shifts by the extra length.
RMS-matched, 10 ms fades. Writes hos_005_s02_the_tied_arm_vo_v03_fin.wav + _align.json (old alignment, new
sentence's chars from the take's own alignment, later chars shifted).  usage: python splice_s02_v03b.py <take> [pre_trim_s]"""
import json, subprocess, sys
from pathlib import Path
import numpy as np
HERE = Path(__file__).resolve().parent
S = HERE.parent / "vo_v01"
SR = 48000; OLD0, OLD1 = 7.0533, 8.1818
SPAN = {"a": (4.230, 6.580), "b": (3.781, 5.609), "c": (4.194, 6.622)}   # silencedetect n=-45dB d=0.05
OLD = "The hand went pale."; NEW = "Below the band, the pulse stopped."
def dec(p):
    return np.frombuffer(subprocess.run(["ffmpeg","-v","error","-i",str(p),"-f","f32le","-ar","48000","-ac","2","-"],
        capture_output=True,check=True).stdout,dtype=np.float32).reshape(-1,2).copy()
take = sys.argv[1]; pre = float(sys.argv[2]) if len(sys.argv) > 2 else 0.0
NEW0 = OLD0 - pre                     # optionally tighten the pause before the line (old pause 6.454-7.053)
base = dec(S/"hos_005_s02_the_tied_arm_vo_v01_fin.wav")
rms = lambda x: float(np.sqrt(np.mean(x**2)))
old = base[int(OLD0*SR):int(OLD1*SR)]
x = dec(HERE/f"s02_pulse_ctx_{take}.mp3")
s0 = SPAN[take][0]-0.02; s = int(s0*SR); e = int((SPAN[take][1]+0.03)*SR)
seg = x[s:e].copy(); seg *= rms(old)/max(rms(seg),1e-9)
f = int(0.010*SR); ramp = np.linspace(0,1,f)[:,None]; seg[:f] *= ramp; seg[-f:] *= ramp[::-1]
L = len(seg)/SR; shift = NEW0 + L - OLD1
out = np.concatenate([base[:int(NEW0*SR)], seg, base[int(OLD1*SR):]])
peak = float(np.abs(out).max())
w = HERE/"hos_005_s02_the_tied_arm_vo_v03_fin.wav"
subprocess.run(["ffmpeg","-y","-v","error","-f","f32le","-ar","48000","-ac","2","-i","-","-c:a","pcm_s16le",str(w)],
               input=np.clip(out,-1,1).tobytes(),check=True)
al = json.load(open(S/"hos_005_s02_the_tied_arm_vo_v01_fin_align.json"))
ch, st, en = al["characters"], al["character_start_times_seconds"], al["character_end_times_seconds"]
full = "".join(ch); k = full.index(OLD); k1 = k + len(OLD)
ta = json.load(open(HERE/f"s02_pulse_ctx_{take}_align.json")); tt = "".join(ta["characters"]); i0 = tt.index(NEW)
off = NEW0 - s0
nst = [max(NEW0, round(t+off,4)) for t in ta["character_start_times_seconds"][i0:i0+len(NEW)]]
nen = [min(NEW0+L, round(t+off,4)) for t in ta["character_end_times_seconds"][i0:i0+len(NEW)]]
mv = lambda v: [round(t+shift,4) for t in v]
al["characters"] = ch[:k] + list(NEW) + ch[k1:]
al["character_start_times_seconds"] = st[:k] + nst + mv(st[k1:])
al["character_end_times_seconds"] = en[:k] + nen + mv(en[k1:])
json.dump(al, open(str(w).replace(".wav","_align.json"),"w"), indent=1)
dur = len(out)/SR
meta = {"take": take, "src": f"s02_pulse_ctx_{take}.mp3", "span_s": [round(s0,3), round(SPAN[take][1]+0.03,3)],
        "new0_s": round(NEW0,3), "new_line_s": round(L,3), "old_line_s": round(OLD1-OLD0,3), "shift_s": round(shift,3),
        "pre_trim_s": pre, "dur_s": round(dur,3), "short_total_s": round(dur+0.55,3), "peak_db": round(20*np.log10(peak),2)}
json.dump(meta, open(HERE/"SPLICE_v03b.json","w"), indent=1); print(meta)
