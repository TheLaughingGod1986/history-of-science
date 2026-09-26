import json,time,base64,sys,urllib.request,websocket
class Tab:
    def __init__(self, match="studio.youtube.com"):
        ts=json.load(urllib.request.urlopen("http://127.0.0.1:9460/json/list"))
        t=[x for x in ts if x["type"]=="page" and match in x["url"]][0]
        self.ws=websocket.create_connection(t["webSocketDebuggerUrl"],timeout=60,suppress_origin=True,max_size=60_000_000); self.n=0
    def call(self,m,p=None,timeout=60):
        self.n+=1; i=self.n; self.ws.send(json.dumps({"id":i,"method":m,"params":p or {}}))
        end=time.time()+timeout
        while time.time()<end:
            d=json.loads(self.ws.recv())
            if d.get("id")==i:
                if "error" in d: raise RuntimeError(f"{m}: {d['error']}")
                return d.get("result",{})
        raise TimeoutError(m)
    def js(self,e):
        r=self.call("Runtime.evaluate",{"expression":e,"returnByValue":True,"awaitPromise":True})
        if r.get("exceptionDetails"): raise RuntimeError(json.dumps(r["exceptionDetails"])[:500])
        return r.get("result",{}).get("value")
    def go(self,url,wait=8):
        self.call("Page.navigate",{"url":url}); time.sleep(wait)
    def shot(self,path):
        open(path,"wb").write(base64.b64decode(self.call("Page.captureScreenshot",{"format":"png"})["data"]))
ROWS = r"""(() => [...document.querySelectorAll('ytcp-video-row')].map(r => ({
  text:(r.innerText||'').replace(/\s+/g,' ').slice(0,220),
  href:(r.querySelector('a[href*="/video/"]')||{}).getAttribute?.('href')||'',
  img:(r.querySelector('img')||{}).src||''})))()"""
