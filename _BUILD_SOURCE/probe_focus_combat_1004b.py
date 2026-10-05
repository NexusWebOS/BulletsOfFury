"""Exercise extended Hammer states on the alien rig; verify music and portal completion."""
from pathlib import Path
import json,base64,sys,http.server
from playwright.sync_api import sync_playwright
import shoot as sh
R=Path(__file__).resolve().parents[1];O=R/'_shots/campaign_focus_1004b';O.mkdir(exist_ok=True)
SETUP=(R/'_BUILD_SOURCE/probe_feedback_1002.py').read_text(encoding='utf-8').split('SETUP="""')[1].split('"""')[0]
report={'checks':[]};errors=[]
def ck(value,name):
 report['checks'].append({'ok':bool(value),'name':name});print(('PASS ' if value else 'FAIL ')+name,flush=True)
def frames(p,n,expr):
 for i in range(0,n,30):
  p.evaluate('(n)=>{for(let i=0;i<n;i++){'+expr+'}}',min(n-i,30));p.wait_for_timeout(10)
def shot(p,name):
 p.evaluate('()=>{shake=0;const v=player.invuln;player.invuln=0;ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);player.invuln=v;}')
 (O/(name+'.png')).write_bytes(base64.b64decode(p.evaluate('()=>cv.toDataURL().split(",")[1]')))
port,stop=sh.serve(str(R));http.server.SimpleHTTPRequestHandler.log_message=lambda *a,**k:None
try:
 with sync_playwright() as pw:
  browser=pw.chromium.launch(args=['--no-sandbox','--autoplay-policy=no-user-gesture-required']);p=browser.new_page(viewport={'width':1440,'height':1000})
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text[:500]) if m.type=='error' or 'draw error' in m.text else None)
  p.goto(f'http://127.0.0.1:{port}/index.html',timeout=120000);p.wait_for_function('()=>window.__bofFrames>4',timeout=120000);p.evaluate(sh.TRAP_RAF)
  p.evaluate('()=>r30Warm()');p.wait_for_function('()=>Object.values(FMC_ART).every(a=>XART.rdy(a.key))',timeout=120000)
  p.evaluate(SETUP,{'stage':8,'kind':'vileexistence','diff':'furious'})
  p.evaluate('()=>{stagePlan=[];enemies=[];powerups=[];j3Encounter(B,2);j3Mimic(B,5);B._r30.mode="fight";B.enter=false;window.D=gd4Create(B,5);window.h=D.p._hammer;}')
  report['poses']=[]
  # Enter real source attacks, then let their source clocks/collisions progress.
  cases=[('coil','hammerTarget(D.p);hammerState(D.p,"warn");',18),('airborne','hammerTarget(D.p);hammerState(D.p,"leap");',7),
   ('slam','hammerState(D.p,"recover");',3),('reset','hammerState(D.p,"leap_reset");',12),
   ('sword-throw','hammerBoomerangStart(D.p);hammerBoomerangRelease(D.p);',40),
   ('chaingun','hammerPhaseTwoStart(D.p);hammerChainStart(D.p);',70),
   ('spell','hammerSpellStart(D.p);',159),('storm','h.mode="storm";hammerStormTarget(D.p);',98),
   ('whirlwind','h.mode="hammer";hammerWhirlStart(D.p);',45),('mega','hammerState(D.p,"mega_charge");',125),
   ('curled','hammerBallArm(D.p);h.vx=150;h.vy=165;hammerState(D.p,"ball");',40)]
  for name,init,n in cases:
   p.evaluate('()=>{eBullets=[];powerups=[];explosions=[];D.age=0;D.p.x=B.x=worldWidth()/2;D.p.y=B.y=180;h.throw=null;h.stormWaves=[];h.phasePending=false;h.mode="hammer";h.hitCd=1;'+init+'}')
   frames(p,n,'player.invuln=100;gd4Tick(B,1/60);B._r30.clock+=1/60;ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);')
   shot(p,'knight-'+name)
   row=p.evaluate('(name)=>({name,state:h.state,frame:cf4KnightFrame(h),throw:h.throw?{x:h.throw.x,y:h.throw.y}:null,rig:r30Parts(B).map(v=>({id:v.p.id,key:v.key,x:v.x,y:v.y,w:v.w,h:v.h,rot:v.rot})),finite:eBullets.every(q=>Number.isFinite(q.x+q.y+q.vx+q.vy))})',name);report['poses'].append(row)
   ck(row['finite'] and all(all(isinstance(v[k],(float,int)) for k in ['x','y','w','h','rot']) for v in row['rig']),name+' renders finite articulated geometry and projectiles')
   if name=='sword-throw':
    v=next(v for v in row['rig'] if v['id']=='sword');t=row['throw'];ck(t and abs(t['x']-v['x'])+abs(t['y']-v['y'])<.001,'thrown sword pixels and collision use the same position')
  p.evaluate('()=>{h.throw=null;hammerBoomerangStart(D.p);hammerBoomerangRelease(D.p);B.parts.find(v=>v.id==="sword").destroyed=true;gd4Tick(B,.02);}')
  ck(p.evaluate('()=>!h.throw&&h.mode==="chaingun"'),'broken sword cannot leave an invisible damaging boomerang')
  p.evaluate(SETUP,{'stage':8,'kind':'vileexistence','diff':'furious'})
  p.evaluate('()=>{window.cues=[];window.oldMusic=Audio.startMusic;Audio.startMusic=function(k){cues.push(k);return oldMusic.call(this,k)};B._r30.mode="takeover";B._r30.t=5.19;}')
  p.evaluate('()=>r30Tick(B,.05)')
  for phase in [1,2]:
   p.evaluate('()=>{B._r30.mode="encounterReform1003j";B._r30.t=2.99;r30Tick(B,.05);}')
  report['musicCues']=p.evaluate('()=>cues');ck(report['musicCues'][-3:]==['boss8','boss8p2','boss8p3'],'real encounter transitions start the three assigned tracks in order')
  p.evaluate('()=>{Audio.startMusic=oldMusic;stagePlan=[];enemies=[];powerups=[];B._r30.mode="fight";B.enter=false;B._r30.cd=0;}')
  frames(p,360,'player.invuln=100;updatePlay(1/60);');shot(p,'dracula-combat')
  # Skip results visually while still preserving the earned result data.
  p.evaluate(SETUP,{'stage':7,'kind':'sludgeemperor','diff':'furious'})
  p.evaluate('()=>{s7mInit(B);B._s7warden.final={};fr27Exit(B,.02);Object.assign(B._s7mod.frExit,{entry:{gone:true,goneAt:0,t0:0},flame:{t0:0,k:1,fx:1},t:100});fr27Exit(B,.02);}')
  frames(p,960,'ctx.setTransform(SS,0,0,SS,0,0);if(state===GS.WARPENTRY)drawL78Entry(1/60);else updatePlay(1/60);')
  ck(p.evaluate('()=>run.stage===8&&state===GS.PLAY&&!l78entry&&!run._l78Entry'),'direct portal countdown finishes into playable Stage 8')
  shot(p,'stage8-after-portal');browser.close()
finally:stop()
report['errors']=errors;(O/'combat-report.json').write_text(json.dumps(report,indent=2),encoding='utf-8');print(json.dumps({'checks':report['checks'],'errors':errors}))
sys.exit(bool(errors) or any(not c['ok'] for c in report['checks']))
