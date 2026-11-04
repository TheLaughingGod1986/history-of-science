import wave,numpy as np,sys
r=lambda f:(lambda w:np.frombuffer(w.readframes(w.getnframes()),np.int16).reshape(-1,2))(wave.open(f))
db=lambda y:20*np.log10(np.sqrt(np.mean((y.astype(float)/32768)**2))+1e-12)
a=r('/Users/benjaminoats/repos/history-of-science/02_Video-Projects/013_Darwin-Wallace-Evolution/02_Voiceover/hos_013_vo_v03.wav'); b=r(sys.argv[1])
F=[(3590400,2880),(8175839,3840),(13226880,960),(17550720,2880),(21478080,960),(24599040,1920)]
mask=np.ones(len(a),bool)
for E,n in F:
  mask[E-n:E]=False; print('end %.3f window %.3f-%.3f last10 %.2f last20 %.2f last %s next10 %s'%(E/48000,(E-n)/48000,E/48000,db(b[E-480:E]),db(b[E-960:E]),tuple(int(x) for x in b[E-1]), None if E>=len(b) else int(np.abs(b[E:E+480]).max())))
d=np.abs(a.astype(int)-b.astype(int)).max(1)
print('frames',len(a),len(b),'null outside windows max',d[mask].max(),'inside max',d[~mask].max())
