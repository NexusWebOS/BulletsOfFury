"""Real Chromium coverage through shoot.py. Explicit fixtures are recorded as such.
Actual canvas differences verify connected arms, liquid motion and hit flashes.
"""
from pathlib import Path
from playwright.sync_api import sync_playwright
from shoot import serve,TRAP_RAF,STEP
from PIL import Image,ImageDraw
import json,http.server,time
R=Path(__file__).resolve().parents[1];O=R/'_shots/warden_wreck_1028/probe';O.mkdir(parents=True,exist_ok=True)
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
  ck('Living Warden retains its central combat bounds',p.evaluate("()=>{wt7Setup('recover',worldWidth()/2+80,430);s7mTick(boss,.016);return boss.x===worldWidth()/2&&boss.y<=VH*.64;}"))
  p.evaluate("""()=>{wt7Setup('recover',worldWidth()/2,285);const b=boss,M=b._s7mod;for(const id of ['gunL','gunR','frontL','frontR','rearL','rearR']){const p=M.parts.find(p=>p.id===id);s7mHit(b,p.hp,0,0,id);}for(const c of M.er28Canisters)s7mHit(b,c.hp,0,0,c.id);}""")
  for i in range(45):p.evaluate(STEP,8)
  ck('Native core damage begins the existing death owner',p.evaluate("()=>{window.wreckBoss=boss;const b=boss,M=b._s7mod;s7mHit(b,M.core+1,0,0,'core');return M.core===0&&M.mode==='dead'&&bossDefeated&&!M.frExit;}"))
  p.evaluate("""()=>{window.wreckBlits=[];window.wreckBaseBlit=er28Blit;er28Blit=function(name,f,x,y,hit){if(name==='core'&&SW28.actor===wreckBoss)wreckBlits.push({t:wreckBoss._s7mod.frExit?.t||0,x,y});return wreckBaseBlit.apply(this,arguments);};}""")
  rows=[]
  for i in range(210):
   p.evaluate(STEP,1)
   if i%5==0:rows.append(p.evaluate("(()=>{const b=wreckBoss,E=b._s7mod.frExit;return{t:E.t,x:b.x,y:b.y,drawY:b._drawY,travel:E.travel,ground:E.groundY,hidden:b._s7warden.final.bossHidden,shipY:player.y}})()"))
   if i in [20,65,125,180]:shot(p,'escape-'+str(i))
  ck('Wreck remains fixed to its original terrain position',all(abs(q['y']-q['travel']-q['ground'])<.001 for q in rows),rows)
  ck('Wreck moves down and out of the camera as the ship escapes',rows[-1]['y']>rows[0]['y']+1000 and rows[-1]['hidden'],dict(start=rows[0],end=rows[-1]))
  ck('Draw anchor agrees with the native floor position',all(abs(q['drawY']-q['y'])<.001 for q in rows))
  q=p.evaluate("()=>{const draws=wreckBlits;return {early:draws.filter(q=>q.t<.8).length,late:draws.filter(q=>q.t>3).length,last:draws.at(-1)};}")
  ck('Native renderer stops drawing the wreck after it leaves the screen',q['early']>0 and q['late']==0,q)
  q=p.evaluate("()=>{const E=wreckBoss._s7mod.frExit;return {portal:E.portalOn,frameTime:E.portalT,blown:E.blown};}")
  ck('Portal opening and wreck explosion still occur under their native owner',q['portal'] and q['blown'] and q['frameTime']>0,q)
  for i in range(560):
   if p.evaluate('wreckBoss.dead'):break
   p.evaluate(STEP,1)
  q=p.evaluate("()=>{const b=wreckBoss,E=b._s7mod.frExit;return{dead:b.dead,finished:b._s7warden.final.finished,t:E.t,end:E.entry.goneAt+7.6,hidden:b._s7warden.final.bossHidden,reward:b._forgeRewardDropped};}")
  ck('Native finale, protection and reward complete once',q['dead']and q['finished']and q['reward']and abs(q['t']-q['end'])<.04,q)
  ck('No page, console or asset errors',not errors,errors)
  (O/'report.json').write_text(json.dumps(dict(checks=checks,errors=errors),indent=2),encoding='utf8');br.close()
finally:stop()
assert all(q['passed']for q in checks)
