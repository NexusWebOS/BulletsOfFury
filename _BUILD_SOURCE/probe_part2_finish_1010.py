"""Native camera, spike, direction and menu pixels for the part-two pass."""
from pathlib import Path
import sys,json
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'_BUILD_SOURCE'));import shoot
OUT=ROOT/'_shots/part2_1010/finishing';OUT.mkdir(parents=True,exist_ok=True)
checks=[];errors=[];shots=[]
def check(name,value,data=None):
 checks.append(dict(name=name,passed=bool(value),data=data));print(('PASS ' if value else 'FAIL ')+name,flush=True)
 if not value:print(json.dumps(data),flush=True)
port,stop=shoot.serve(str(ROOT))
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(args=['--autoplay-policy=no-user-gesture-required'])
  p=br.new_page(viewport=dict(width=1600,height=900));p.set_default_timeout(120000)
  p.on('pageerror',lambda e:errors.append(str(e)))
  p.on('console',lambda m:errors.append(m.text[:900]) if m.type=='error' or 'draw error' in m.text else None)
  p.on('response',lambda r:errors.append('HTTP '+str(r.status)+': '+r.url.split('?')[0]) if r.status>=400 else None)
  p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('window.__bofFrames>3');p.evaluate(shoot.TRAP_RAF)
  def frames(n):
   for i in range(0,n,15):
    e=p.evaluate(shoot.STEP,min(15,n-i))
    if e:errors.append(e)
    p.wait_for_timeout(3)
  def snap(name):p.screenshot(path=str(OUT/(name+'.png')));shots.append(name+'.png')
  p.evaluate(shoot.SETUP,dict(state='PLAY',stage=5,pilot='lizzie',invuln=True))
  p.wait_for_function('()=>{stageLoadTick();return stageLoadInfo(5).ready&&hm10Ready();}',polling=50)
  p.evaluate('()=>{BOFCinematicDirector.cancel();story=null;fb2Talk=null;s6Opening=null;H3.ending=null;stagePlan=[];enemies=[];powerups=[];pBullets=[];eBullets=[];player.invuln=1e9;player._spawnClearT=1e9;on5LaunchEncounter({stage:5,role:"boss",code:"BOSS5"});}')
  frames(180)
  p.evaluate('()=>{const h=boss._hammer;H3.ending=null;fb2Talk=null;story=null;h.intro1002=true;h.mode="storm";h.stormHome={x:worldWidth()/2,y:VH*.34};hammerStormTarget(boss);hammerStormImpact(boss);window.p2Spike=[...boss._hammer.stormWaves].sort((a,b)=>Math.abs(a.x-player.x)-Math.abs(b.x-player.x))[0];p2Spike.t=p2Spike.split+p2Spike.delay+p2Spike.warm+.36/p2Spike.riseRate;}')
  q=p.evaluate('()=>{const a=hammerStormSpikeShape(p2Spike);return {top:p2Spike.y-a.height,viewTop:viewTopY(),scaleEqual:a.kx===a.ky,live:hammerStormSpikeHits(p2Spike,p2Spike.x,p2Spike.y-a.height+5),lanes:boss._hammer.stormWaves.length};}')
  check('Hammer crest reaches the arena top with the same uniformly scaled visible and lethal shaft',abs(q['top']-q['viewTop'])<1.1 and q['scaleEqual'] and q['live'],q)
  p.evaluate('()=>{ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);ctx.save();ctx.translate(-camX,0);hammerStormSpikeDraw(p2Spike);ctx.restore();}')
  snap('hammer-full-height-spike')
  p.evaluate('()=>{boss._hammer.stormWaves=[];window.p2Earth=[];window.p2Flights=[];window.p2Capture=false;window.p2NextEarth=false;const get=XART.get,draw=ctx.drawImage,flight=furyShipDrawFlight;XART.get=function(k){if(p2Capture&&k==="h3_earth")window.p2NextEarth=true;return get.apply(this,arguments);};ctx.drawImage=function(){if(p2Capture&&p2NextEarth){p2NextEarth=false;p2Earth.push(Array.from(arguments).slice(1));}return draw.apply(this,arguments);};furyShipDrawFlight=function(x,y,size,pilot){if(p2Capture)p2Flights.push({x,y,size,pilot});return flight.apply(this,arguments);};XART.rdy("h3_earth");}')
  p.wait_for_function('()=>XART.rdy("h3_earth")')
  for t in [0,4,7.8]:
   p.evaluate('t=>{H3.ending={boss,phase:"descent",descent:t,t,homeAge:4,cheer:0};p2Capture=true;ctx.setTransform(SS,0,0,SS,0,0);h3EndingDraw();p2Capture=false;}',t)
   snap('earth-'+str(t).replace('.','-'))
  q=p.evaluate('()=>({earth:p2Earth,flights:p2Flights})')
  centers=[(a[0]+a[2]/2,a[1]+a[3]/2) for a in q['earth']]
  check('Earth keeps its camera center while the actual pilot ship shrinks and flies toward it',len(centers)==3 and max(x[0] for x in centers)-min(x[0] for x in centers)<.01 and max(x[1] for x in centers)-min(x[1] for x in centers)<.01 and q['flights'][0]['size']>q['flights'][1]['size']>q['flights'][2]['size'] and q['flights'][0]['y']>q['flights'][2]['y'] and all(x['pilot']=='lizzie' for x in q['flights']),q)
  p.evaluate('()=>{H3.ending=null;drawStageClear._init=false;drawStageClear._res=null;drawStageClear._fast=true;setState(GS.STAGECLEAR);window.__bofFit();}')
  frames(90);snap('stage-clear-full-screen')
  q=p.evaluate('()=>({row:getComputedStyle(document.getElementById("hud-row")).visibility,bottom:getComputedStyle(document.getElementById("hud-bottom")).display,screen:document.getElementById("screen").getBoundingClientRect().height,frame:document.getElementById("game-frame").getBoundingClientRect().height})')
  check('Stage Clear has no equipment row or reserved HUD gap',q['row']=='hidden' and q['bottom']=='none' and abs(q['screen']-q['frame'])<2,q)
  p.evaluate('()=>{run.mode="campaign";sselCursor=1;cmap2Reset({boot:true});setState(GS.STAGESEL);}')
  frames(180);snap('campaign-zoom')
  q=p.evaluate('()=>({state,loading:stageLoadInfo(1).ready,zoom:cmap2.cam.z,errors:window.__bofDrawError?.toString()})')
  check('The campaign map remains interactive after the slower entry zoom',q['state']=='stagesel' and not q.get('errors'),q)
  p.evaluate(shoot.SETUP,dict(state='PLAY',stage=6,pilot='lizzie',invuln=True))
  p.wait_for_function('()=>{stageLoadTick();fb2Warm();return stageLoadInfo(6).ready&&XART.rdy("fb2_stealth_red")&&XART.rdy("fb2_stealth_green");}',polling=50)
  p.evaluate('()=>{H3.ending=null;H3.release=false;BOFCinematicDirector.cancel();story=null;fb2Talk=null;s6Opening=null;stagePlan=[];enemies=[];boss=subBoss=null;bossActive=false;window.p2Bombers=[];for(const side of [-1,1]){const e=spawnEnemy("s1jetbomber_b",player.x+side*120,200);e._side=side;e._s6storm="s6bomber";e._s6Strike={direction:"south"};p2Bombers.push(e);}}')
  frames(3);snap('red-green-stealth-bombers')
  q=p.evaluate('()=>p2Bombers.map(e=>({palette:e._ap10Palette,key:e._p2StealthKey,facing:e._sm10Facing,hp:e.hp,size:e._drawH}))')
  check('Real bomber actors draw palette variants of the actual opening stealth fighter facing south',set(x['palette'] for x in q)=={'red','green'} and all(x['facing']=='south' and x.get('key')=='p2_stealth_'+x['palette']+'_idle' for x in q),q)
  check('No page, console, renderer or asset errors',not errors,errors);br.close()
except Exception as e:errors.append(type(e).__name__+': '+str(e));print(errors[-1],flush=True)
finally:
 stop();r=dict(passed=sum(q['passed'] for q in checks),failed=sum(not q['passed'] for q in checks),checks=checks,errors=errors,shots=shots)
 (OUT/'report.json').write_text(json.dumps(r,indent=2),encoding='utf-8');print(json.dumps(dict(passed=r['passed'],failed=r['failed'],errors=errors)),flush=True)
sys.exit(1 if errors or r['failed'] else 0)
