from pathlib import Path
import sys,json,http.server
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1] if Path(__file__).parent.name=='_BUILD_SOURCE' else Path(r'C:\Users\Mike\Desktop\Github Coding\BulletsOfFury');W=R/'_shots/dracodia_helicopter_1030' if Path(__file__).parent.name=='_BUILD_SOURCE' else Path(__file__).parent;W.mkdir(parents=True,exist_ok=True);sys.path.insert(0,str(R/'_BUILD_SOURCE'))
from shoot import serve,STEP
from barrage_review_common_1025 import boot
http.server.ThreadingHTTPServer.request_queue_size=256;errors=[];checks=[];states=[];port,stop=serve(str(R))
def check(name,value):checks.append({'name':name,'passed':bool(value)});print(('PASS 'if value else'FAIL ')+name,flush=True)
SETUP="""([rank,kind])=>{diffKey=rank;spawnBoss('vileexistence');window.B=boss;v18Enter(B,2,1);B._r30.mode='fight';B.enter=B._noHit=false;B.x=340;B.y=174;player.dead=player.out=false;player.x=340;player.y=VH-65;player.invuln=0;player.roll=player.somer=null;run.armor=run.shield=0;DBGT.god=true;HC79.events=[];for(const k of Object.keys(Input.keys))Input.keys[k]=false;window.P=hc79Start(B,kind);window.Q=hc79State(B);}"""
try:
 with sync_playwright()as pw:
  br=pw.chromium.launch(channel='msedge',headless=True,args=['--autoplay-policy=no-user-gesture-required']);p=boot(br.new_context(viewport={'width':1280,'height':800}),port,8,errors,'boss')
  for rank in ['normal','hard','furious']:
   p.evaluate(SETUP,[rank,'guns']);before=p.evaluate('B.hp');p.evaluate('()=>{DBGT.god=false;}')
   for i in range(240):
    p.evaluate('()=>{Input.keys.a=player.x>P.safeX+2;Input.keys.d=player.x<P.safeX-2;}');p.evaluate(STEP,1)
   q=p.evaluate('({dead:player.dead,x:player.x,safeX:P.safeX,hp:B.hp,shots:HC79.events.filter(e=>e.event==="gun-shot"),part:Q.action?.kind})');states.append({'rank':rank,'guns':q})
   check(rank+' twin-gun lane reachable and survived without GOD',not q['dead']and abs(q['x']-q['safeX'])<7)
   check(rank+' dodge test preserves native copy HP',q['hp']==before)
   check(rank+' both real turrets fire sustained committed bursts',len(q['shots'])>=16 and{e['part']for e in q['shots']}=={'left','right'})
   safe=q['safeX'];errs=[]
   for s in q['shots']:
    import math
    at=s['x']+(447-s['y'])*math.cos(s['angle'])/math.sin(s['angle']);errs.append(abs(at-safe))
   check(rank+' bullet trajectories leave the stated 96px dodge corridor',min(errs)>48)
   p.evaluate(SETUP,[rank,'missiles']);p.evaluate('()=>{player.x=490;}');p.evaluate(STEP,125)
   q=p.evaluate('({n:HC79.events.filter(e=>e.event==="missile-launch").length,locks:playerLocks.filter(L=>L.src?._hc79Host===B).map(L=>({part:L.src._hc79Part,missiles:L.missiles.length,queued:L.launches.length})),angles:Object.values(Q.turn),shots:eBullets.filter(q=>q._hc79Type==="missile").map(q=>({lock:q._lockId,intercept:enemyOrdnanceCanIntercept(q)}))})')
   check(rank+' rapid missile count matches difficulty',q['n']=={'normal':4,'hard':6,'furious':8}[rank])
   check(rank+' each pod holds its own native player Retina lock',len(q['locks'])==2 and all(v['queued']=={'normal':2,'hard':3,'furious':4}[rank]for v in q['locks']))
   check(rank+' physical missiles remain shootable and owned by locks',len(q['shots'])>0 and all(s['intercept']and s['lock']for s in q['shots']))
   check(rank+' aiming changes the authored turret direction',max(abs(a)for a in q['angles'])>.25)
  p.evaluate(SETUP,['furious','guns']);p.evaluate(STEP,60);p.screenshot(path=str(W/'warning-native.png'))
  p.evaluate('()=>{DBGT.god=false;const m=hc79Socket(B,"right"),a=hc79Angle(hc79Dir(Q.turn.right+Math.PI/2));player.y=447;player.x=m.x+(447-m.y)*Math.cos(a)/Math.sin(a);}')
  p.evaluate(STEP,105);check('Gun tracers invoke actual native death when not dodged',p.evaluate('player.dead'))
  p.evaluate(SETUP,['furious','missiles']);p.evaluate(STEP,35);p.evaluate('()=>{B._lastPart=B.parts.find(p=>p.id==="left");modularHit(B._lastPart.hp);}')
  p.evaluate(STEP,150)
  check('Destroyed missile pod cancels every pending launch on its side',p.evaluate('B.parts.find(p=>p.id==="left").destroyed&&!HC79.events.some(e=>e.event==="missile-launch"&&e.part==="left")'))
  check('Other pod continues its four-shot Furious volley',p.evaluate('HC79.events.filter(e=>e.event==="missile-launch"&&e.part==="right").length===4'))
  check('Destroyed pod disappears from both exact hit rig and Retina list',p.evaluate('!v18Rig(B).some(v=>v.p.id==="left")&&!retinaBossTargets(B).some(t=>String(t._retinaId||t.id).endsWith("-left"))'))
  p.evaluate(SETUP,['furious','guns']);p.evaluate(STEP,85)
  check('Ordinary machine-gun bullets cannot be shot down from their first frame',p.evaluate('eBullets.filter(q=>q._hc79Type==="gun").length>0&&eBullets.filter(q=>q._hc79Type==="gun").every(q=>!enemyOrdnanceCanIntercept(q)&&q._weaponProof)'))
  q=p.evaluate('''()=>{const a=v18Rig(B),z=v18Rig(B);let tested=0,miss=0;for(const v of a)for(let y=0;y<v.a.h;y+=4)for(let x=0;x<v.a.w;x+=4){const row=v.a.spans[y];let expected=false;for(let i=0;i<row.length;i+=2)if(x>=row[i]&&x<row[i+1])expected=true;const actual=v19AtRect(v,v.ax+v.a.offset[0]+x+.1,v.ay+v.a.offset[1]+y+.1);tested++;if(expected!==actual)miss++;}const reused=a===z;B.x+=2;return{tested,miss,reused,moved:v18Rig(B)!==a};}''')
  check('Rendered pod rotations own exact source-alpha collision',q['tested']>2000 and q['miss']==0)
  check('Same-frame rig cache reuses geometry and invalidates on movement',q['reused']and q['moved'])
  p.evaluate(SETUP,['furious','sonic']);p.evaluate(STEP,110)
  check('Pressure waves are red authored non-interceptible ordnance',p.evaluate('eBullets.some(q=>q._hc79Type==="sonic")&&eBullets.filter(q=>q._hc79Type==="sonic").every(q=>!enemyOrdnanceCanIntercept(q)&&q._waveW===264)'))
  check('Helicopter fits the 85-percent authored footprint',p.evaluate('HC79_ART.size===348&&Math.abs(HC79_ART.size/410-.85)<.002'))
  check('Rotor advances at four times its previous authored rate',p.evaluate('HC79_ART.rotorFps===48&&HC79_ART.sourceRotorFps===12'))
  check('New jungle ground and faster near canopy both render',p.evaluate('HC79.draws.ground>0&&HC79.draws.canopy>0&&B._r30.v18.arenaPhase===2'))
  before=p.evaluate('({t:P.t,clock:B._r30.clock,rotor:Q.rotor})');p.evaluate("setState('paused')");p.evaluate(STEP,90);check('Pause freezes weapon, motion and rotor clocks',p.evaluate('({t:P.t,clock:B._r30.clock,rotor:Q.rotor})')==before);p.evaluate('setState(GS.PLAY)')
  p.evaluate(SETUP,['furious','dash']);p.evaluate(STEP,128);check('Charge commits its warned lane and exits the foreground',p.evaluate('B.y>VH&&B._noHit'))
  p.evaluate(STEP,145);check('Charge returns to a visible reachable hover height',p.evaluate('B.y>160&&B.y<190&&!B._noHit'))
  # Native death and download return, with previous main-body limb damage.
  p.evaluate(SETUP,['furious','missiles']);p.evaluate("()=>{const J=j3State(B);v18Enter(B,2,0);J.modules[0][1].destroyed=true;J.modules[0][1].hp=0;v18Enter(B,2,1);B._r30.mode='fight';B.enter=B._noHit=false;B._lastPart=B.parts[0];modularHit(B.hp);}");p.evaluate(STEP,435)
  check('Native copied-form death returns to the downloaded main arena',p.evaluate('B._r30.v18.form===0&&B._r30.mode==="fight"&&B.hp===j3State(B).max[0]'))
  check('Earlier copied-form death repairs the main body without restoring copy HP',p.evaluate('!B.parts.some(p=>p.destroyed)&&j3State(B).hp[1]===0'))
  p.evaluate(SETUP,['furious','guns']);p.evaluate('()=>{const J=j3State(B);for(const i of V18.forms)if(i!==1)J.hp[i]=0;B._lastPart=B.parts[0];modularHit(B.hp);}');p.evaluate(STEP,340)
  check('Last copied life reaches the native final destruction without an anatomy crash',p.evaluate('B._r30.mode==="dr5Death"&&B.hp===0'))
  p.evaluate(SETUP,['furious','missiles']);p.evaluate('()=>{spawnBoss("vileexistence");window.B=boss;}');check('Retry restores the original first host instead of the copied helicopter',p.evaluate('j3State(B).encounter===0&&!hc79Own(B)'))
  p.evaluate('()=>{v18Enter(B,2,0);B._r30.mode="fight";B.enter=B._noHit=false;for(const i of V18.forms)if(i!==0)j3State(B).hp[i]=0;rd78Start(B);}')
  check('New helicopter owner leaves the main-body Luminaire intact',p.evaluate('!!rd78Act(B)&&!hc79Own(B)'))
  check('No native draw, browser or loading errors',not errors);br.close()
finally:stop();(W/'checks.json').write_text(json.dumps({'checks':checks,'states':states,'errors':errors},indent=2))
assert all(c['passed']for c in checks),[c['name']for c in checks if not c['passed']]
