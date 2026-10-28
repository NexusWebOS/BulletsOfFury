"""Real Chromium coverage through shoot.py. Explicit fixtures are recorded as such.
Actual canvas differences verify connected arms, liquid motion and hit flashes.
"""
from pathlib import Path
from playwright.sync_api import sync_playwright
from shoot import serve,TRAP_RAF,STEP
from PIL import Image,ImageDraw
import json,http.server,time
R=Path(__file__).resolve().parents[1];O=R/'_shots/warden_lunge_1028/diagnostic';O.mkdir(parents=True,exist_ok=True)
checks=[];errors=[];shots=[];trails=[]
def ck(name,value,data=None):
 checks.append({'name':name,'passed':bool(value),'data':data});print(('PASS 'if value else'FAIL ')+name,flush=True)
http.server.SimpleHTTPRequestHandler.protocol_version='HTTP/1.1';http.server.ThreadingHTTPServer.request_queue_size=128
port,stop=serve(str(R))
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(channel='msedge',args=['--autoplay-policy=no-user-gesture-required']);bc=br.new_context(viewport={'width':1280,'height':800})
  def page(stage):
   p=bc.new_page();p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text)if m.type=='error'or'draw error'in m.text else None)
   p.on('response',lambda r:errors.append('HTTP '+str(r.status)+' '+r.url.split('/')[-1])if r.status>=400 else None)
   p.goto(f'http://127.0.0.1:{port}/index.html',wait_until='load',timeout=180000);p.wait_for_function('window.__bofFrames>5&&typeof WT25!=="undefined"',timeout=180000);p.mouse.click(3,3);p.evaluate(TRAP_RAF)
   p.evaluate("n=>{debugUnlocked=true;diffKey='furious';debugStartFight(debugFightFor(n,'boss'),{pilot:'cole'});spawnBoss(debugFightFor(n,'boss').kind);debugFight.spawned=true;bossActive=true;warnT=0;BOFCinematicDirector.cancel();DBGT.god=true;run.lives=3;player.dead=false;player.invuln=1e9;setState(GS.PLAY);for(const k of Object.keys(Input.keys))Input.keys[k]=false;}",stage)
   p.wait_for_function('(n)=>{stageLoadTick();return stageLoadReady(n)}',arg=stage,timeout=180000)
   return p
  def shot(p,name):
   p.evaluate('drawWorld(0)');f=O/(name+'.png');p.screenshot(path=str(f));shots.append((f,name))
  p=page(7)
  p.evaluate("()=>{s7mWarm();r25Warm(7);bm9Warm(bm9StageNames(7));window.wt7Setup=(mode,x,y)=>{const b=boss,M=s7mInit(b);b.enter=false;b.x=x;b.y=y;b._drawY=y;M.height=M.drop=M.lean=0;M._mission29IntroDone=true;M.r25Gait=null;M.counterTell=null;M.frExit=null;s7mSet(b,mode);for(const q of M.parts)q.hp=q.max;player.x=worldWidth()/2;player.y=VH-55;};wt7Setup('recover',worldWidth()/2,175);}")
  p.wait_for_function('r25Warm(7)&&bm9StageNames(7).every(n=>BM9_ART[n].every(a=>XART.rdy(a.key)))',timeout=180000)
  print(p.evaluate("""()=>{const b=boss,M=b._s7mod;s7mSet(b,'swipeX');return {VH,VW,width:worldWidth(),player:{x:player.x,y:player.y},boss:{x:b.x,y:b.y},warn:M.warn,legs:s7mPose(b).filter(p=>p.r25).map(p=>({id:p.id,cell:p.cell,frame:p.frame,x:p.x,y:p.y,a:p.a,toe:p.toe,target:p.target,tip:p.bm9Tip,world:s7mWorld(b,p.toe||p.target)}))};}"""));shot(p,'current-swipe')
  br.close()
finally:stop()
