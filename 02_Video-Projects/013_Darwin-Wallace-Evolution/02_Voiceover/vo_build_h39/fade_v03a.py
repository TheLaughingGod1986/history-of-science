#!/usr/bin/env python3
"""Chief h39: build hos_013_vo_v03a from hos_013_vo_v03 (sha d56ba2a4...) by applying
qsin fade-outs that end on the last frame of each chapter's audio. Nothing else changes.
usage: python3 fade_v03a.py IN_v03.wav OUT_v03a.wav"""
import sys,wave,hashlib,numpy as np
SR=48000
# (chapter, end frame (exclusive), fade frames)
FADES=[('ch00',3590400,2880),   # 74.740-74.800 s, 60 ms  "changes."
       ('ch01',8175839,3840),   # 170.250-170.330 s, 80 ms "shaping?" (pickup tail; replaces J1300's 20 ms)
       ('ch02',13226880,960),   # 275.540-275.560 s, 20 ms "someone?" (+3 ms onset blip)
       ('ch03',17550720,2880),  # 365.580-365.640 s, 60 ms "heard?"
       ('ch04',21478080,960),   # 447.440-447.460 s, 20 ms "print."
       ('ch05',24599040,1920)]  # 512.440-512.480 s, 40 ms "today." (film end)
src,dst=sys.argv[1],sys.argv[2]
assert hashlib.sha256(open(src,'rb').read()).hexdigest().startswith('d56ba2a45a76125e'),'input is not v03'
w=wave.open(src); p=w.getparams(); a=np.frombuffer(w.readframes(w.getnframes()),np.int16).reshape(-1,2).copy(); w.close()
assert (p.nchannels,p.sampwidth,p.framerate,p.nframes)==(2,2,48000,24599040)
for name,E,n in FADES:
  g=np.sin(np.pi/2*(np.arange(n,0,-1)-1)/n)
  a[E-n:E]=np.round(a[E-n:E].astype(float)*g[:,None]).astype(np.int16)
o=wave.open(dst,'wb'); o.setparams(p); o.writeframes(a.tobytes()); o.close()
print('wrote',dst,len(a),'frames',hashlib.sha256(open(dst,'rb').read()).hexdigest())
