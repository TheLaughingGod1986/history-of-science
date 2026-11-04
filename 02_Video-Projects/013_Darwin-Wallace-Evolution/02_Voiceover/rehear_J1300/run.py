import json,time
from pathlib import Path
from faster_whisper import WhisperModel
p=Path("/private/tmp/j1300-rehear")
for name in ["base.en","small.en","medium.en"]:
 print("Starting",name,flush=True)
 m=WhisperModel(name,device="cpu",compute_type="int8",cpu_threads=4)
 segments,info=m.transcribe(str(p/"clip_165_177.wav"),word_timestamps=True,language="en",beam_size=5)
 rows=[]
 for s in segments:
  rows.append(dict(start=s.start+165,end=s.end+165,text=s.text,words=[dict(word=w.word,start=w.start+165,end=w.end+165,probability=w.probability) for w in s.words]))
 (p/(name+".json")).write_text(json.dumps(dict(model=name,device="cpu",compute_type="int8",word_timestamps=True,beam_size=5,clip_start=165,segments=rows),indent=2))
 print(json.dumps(rows),flush=True)
 del m
