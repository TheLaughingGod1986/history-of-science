import sys
from faster_whisper import WhisperModel
m=WhisperModel("small.en",device="cpu",compute_type="int8")
for f in sys.argv[1:]:
    segs,_=m.transcribe(f,word_timestamps=True)
    ws=[(w.word.strip(),round(w.start,2),round(w.end,2)) for s in segs for w in s.words]
    print(f.split('/')[-1]," ".join(f"{w}[{a}-{b}]" for w,a,b in ws),flush=True)
