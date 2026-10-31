from pathlib import Path
import sys,json,http.server
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1];W=R/'_shots/sumpjaw_duo_1031';W.mkdir(parents=True,exist_ok=True);sys.path.insert(0,str(R/'_BUILD_SOURCE'))
from shoot import serve,STEP
from barrage_review_common_1025 import boot
checks=[];errors=[]
def ck(n,v,d=None):
 checks.append(dict(name=n,passed=bool(v),data=d));(W/'edge-checks.json').write_text(json.dumps(checks,indent=2));print('PASS'if v else'FAIL',n,d if not v else'',flush=True);assert v,(n,d)
port,stop=serve(str(R));http.server.ThreadingHTTPServer.request_queue_size=256
try:
 with sync_playwright()as pw:
  br=pw.chromium.launch(channel='msedge',headless=True,args=['--autoplay-policy=no-user-gesture-required']);p=boot(br.new_context(viewport={'width':1280,'height':800}),port,7,errors);p.wait_for_function('()=>{stageLoadTick();return sj98Ready()}',timeout=180000)
  def step(n):
   for i in range(0,n,10):
    e=p.evaluate(STEP,min(10,n-i));assert not e,e;p.wait_for_timeout(1)
  p.evaluate("()=>{run.ngplus=false;spawnSubBoss('dualscoopdredger');window.B=subBoss;window.base98=B.maxhp;run.ngplus=true;spawnSubBoss('dualscoopdredger');window.B=subBoss;window.G=B._sj98;G.rest=99;for(const a of G.actors){a.phase='idle';a.frame=0;a.t=0;}window.A=G.actors[0];}")
  ck('New Game Plus applies exactly25percent HP to pair, actors and part budgets once',p.evaluate('Math.abs(B.maxhp-base98*1.25)<.01&&G.actors.every(a=>Math.abs(a.hp-a.pools.reduce((s,p)=>s+p.hp,0))<.01)&&B.hp===B.maxhp'))
  p.evaluate("()=>{A.phase='warn';A.attack='bite';A.t=0;A.warn=1.25;A.target={x:player.x,y:player.y};G.owner=A;G.rest=10;window.c0=G.clock;}");step(30)
  ck('NGplus keeps warning duration in real time',p.evaluate('A.phase==="warn"&&Math.abs(A.t-(G.clock-c0))<.002&&A.t>.45&&A.t<.55'),p.evaluate('A.t'))
  ck('NGplus advances the director recovery gap by15percent',p.evaluate('Math.abs(G.rest-(10-(G.clock-c0)*1.15))<.002'),p.evaluate('G.rest'))
  p.evaluate("()=>{run.ngplus=false;spawnSubBoss('dualscoopdredger');window.B=subBoss;window.G=B._sj98;G.rest=999;for(const a of G.actors){a.phase='idle';a.frame=0;a.t=0;}DBGT.god=true;player.invuln=0;}")
  for direction in ['a','d']:
   p.evaluate('(key)=>{Input.keys.a=Input.keys.d=false;Input.keys[key]=true}',direction);step(180);p.evaluate('Input.keys.a=Input.keys.d=false')
   q=p.evaluate('G.actors.map(a=>{const p=sj98Pose(a),l=a.x+(a.flip?-p.bounds[2]:p.bounds[0]),r=a.x+(a.flip?-p.bounds[0]:p.bounds[2]);return{l,r,visible:l>=camLeftX()+5&&r<=camRightX()-5}})')
   ck(direction+' camera edge preserves both complete passive silhouettes',all(a['visible']for a in q),q)
  p.evaluate("()=>{window.A=G.actors[0];const q=sj98Socket(A,'gillR');window.hp98=A.hp;player.x=q.x;player.y=q.y+90;run.weapon=0;run.wlevel=1;Input.keys.j=true;Input.keys.c=false;}");step(90);p.evaluate('Input.keys.j=false')
  ck('Real native machine-gun projectiles reach and damage a gill',p.evaluate('A.hp<hp98'),p.evaluate('({before:hp98,after:A.hp,weapon:run.weapon,pools:A.pools})'))
  ck('Edge and NGplus runs produce no browser/render errors',not errors,errors);br.close()
finally:stop()
print('RESULT',len(checks),'extra checks passed')
