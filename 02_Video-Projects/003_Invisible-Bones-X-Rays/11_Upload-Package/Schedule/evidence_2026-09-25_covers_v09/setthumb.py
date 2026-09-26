import sys,json,time; sys.path.insert(0,'/tmp/hos003thumbs'); from cdp import *
vid,thumb,tag=sys.argv[1],sys.argv[2],sys.argv[3]
E="/Users/benjaminoats/YouTube/History Of Science/02_Video-Projects/003_Invisible-Bones-X-Rays/11_Upload-Package/Schedule/evidence_2026-09-25_covers_v09"
t=Tab(); t.call("Emulation.setDeviceMetricsOverride",{"width":1440,"height":1000,"deviceScaleFactor":1,"mobile":False})
t.go(f"https://studio.youtube.com/video/{vid}/edit",10)
body=t.js("(document.body.innerText||'').slice(0,3000)")
assert "History of Science" in body or "Video details" in body, body[:400]
t.call("DOM.enable"); doc=t.call("DOM.getDocument",{"depth":-1,"pierce":True})
n=t.call("DOM.querySelector",{"nodeId":doc["root"]["nodeId"],"selector":'input[type="file"][accept*="image"]'}).get("nodeId")
if not n: print(json.dumps({"ok":False,"err":"no thumb input","body":body[:1500]})); t.shot(f"{E}/{tag}_noinput.png"); sys.exit(2)
t.call("DOM.setFileInputFiles",{"nodeId":n,"files":[thumb]}); time.sleep(6)
t.shot(f"{E}/{tag}_after_pick.png")
CLICK=r"""(()=>{let b=null;const v=(n)=>{for(const e of n.querySelectorAll('ytcp-button,button')){const s=(e.innerText||e.getAttribute('aria-label')||'').trim();if(s==='Save'&&e.getBoundingClientRect().width>20)b=e;if(e.shadowRoot)v(e.shadowRoot)}};v(document);if(!b)return 'missing';const dis=b.hasAttribute('disabled')||b.getAttribute('aria-disabled')==='true';if(dis)return 'disabled';b.click();return 'clicked'})()"""
s=t.js(CLICK); time.sleep(6)
after=t.js(CLICK.replace("b.click();return 'clicked'","return 'enabled'"))
t.shot(f"{E}/{tag}_after_save.png")
errs=t.js("(document.body.innerText||'').match(/(couldn.t|error|failed|try again)[^\\n]{0,120}/ig)")
print(json.dumps({"vid":vid,"save":s,"save_after":after,"errs":errs}))
