from pathlib import Path
import sys,ast,json,time,base64
from playwright.sync_api import sync_playwright
R=Path(r'C:/Users/Mike/Desktop/Github Coding/BulletsOfFury');W=Path(__file__).parent
sys.path.insert(0,str(R/'_BUILD_SOURCE'));from shoot import TRAP_RAF
T=ast.parse((R/'_BUILD_SOURCE/probe_feedback_1002.py').read_text(encoding='utf8'));SETUP=next(ast.literal_eval(n.value)for n in T.body if isinstance(n,ast.Assign)and any(isinstance(x,ast.Name)and x.id=='SETUP'for x in n.targets))
checks=[];errors=[]
def check(ok,name,data=None):
 checks.append(dict(ok=bool(ok),name=name,data=data));print(('OK 'if ok else'FAIL ')+name,flush=True)
def warm(p,keys):
 p.evaluate('(ks)=>{window.qaKeys=ks;ks.forEach(k=>XART.rdy(k));}',keys)
 for i in range(1500):
  ready=p.evaluate('()=>{if(typeof __stepRAF==="function")__stepRAF(16.667);stageLoadTick();return qaKeys.every(k=>XART.rdy(k));}')
  if ready:return
  # The existing loader queue advances on native RAF, including hidden title state.
  p.evaluate('()=>{if(window.__rafCb){const f=window.__rafCb;window.__rafCb=null;f(performance.now());}}')
  p.wait_for_timeout(20)
 raise RuntimeError('Art load timeout '+str(p.evaluate('qaKeys.filter(k=>!XART.rdy(k))')))
def shot(p,name):
 p.evaluate('()=>{shake=0;ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);}')
 (W/(name+'.png')).write_bytes(base64.b64decode(p.evaluate('cv.toDataURL().split(",")[1]')))
