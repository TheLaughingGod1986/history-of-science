"""Small helpers for the 005 end-screen editor (CDP :9460)."""
import importlib.util as iu
from pathlib import Path

_s = iu.spec_from_file_location("st", Path(__file__).with_name("_studio_step_v01.py"))
m = iu.module_from_spec(_s)
_s.loader.exec_module(m)

BOX_JS = """(want) => { let best=null; const walk=(r,d=0)=>{ if(!r||d>60) return;
  for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
    const t=(el.innerText||'').trim(); if (t!==want) continue;
    const b=el.getBoundingClientRect(); if (b.width<4||b.height<4) continue;
    if (!best || b.width*b.height < best.w*best.h) best={x:b.x+b.width/2,y:b.y+b.height/2,w:b.width,h:b.height,l:b.x,t:b.y}; }
  for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) if(el.shadowRoot) walk(el.shadowRoot,d+1);
 }; walk(document); return best; }"""


def box(pg, text):
    return pg.evaluate(BOX_JS, text)


def click(pg, text, wait=2000):
    b = box(pg, text)
    if b:
        pg.mouse.click(b["x"], b["y"])
        pg.wait_for_timeout(wait)
    return b
