import sys,json,time; sys.path.insert(0,'/tmp/hos003thumbs'); from cdp import *
t=Tab(); C="https://studio.youtube.com/channel/UCXp7HkBIl1LgaznXuZHJyRg"
t.call("Emulation.setDeviceMetricsOverride",{"width":1440,"height":1000,"deviceScaleFactor":1,"mobile":False})
out={}
for k,u in (("shorts",C+"/videos/short"),("videos",C+"/videos/upload")):
    t.go(u,9); out[k]=t.js(ROWS); t.shot(f"/tmp/hos003thumbs/before_{k}.png")
out["url"]=t.js("location.href"); out["acct"]=t.js("(document.querySelector('#entity-name')||{}).innerText||''")
print(json.dumps(out,indent=1))
