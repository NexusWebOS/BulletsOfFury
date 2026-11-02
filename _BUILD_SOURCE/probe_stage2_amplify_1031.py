"""Live native Stage2 smoke/attack/pixel evidence. No stand-in renderers."""
from pathlib import Path
import sys,json,http.server
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'_BUILD_SOURCE'))
from shoot import serve,STEP,TRAP_RAF
O=R/'_shots/stage2_amplify_1031';O.mkdir(exist_ok=True)
port,stop=serve(str(R));http.server.ThreadingHTTPServer.request_queue_size=256
errors=[];checks=[];runs=[]
SETUP="""([type,mode])=>{
 if(window.v31SavedSpawn)spawnEnemy=window.v31SavedSpawn;
 diffKey=mode;DIFF=difficultyForRun('arcade',mode);run.mode='campaign';run.stage=2;
 stagePlan=[];waveIdx=999;spawnClock=9999;_adaptiveSpawnT=99999;stageTimer=1;
 boss=null;subBoss=null;bossActive=subBossActive=false;bossWarned=true;subBossDone=true;stageEnding=false;
 BOFCinematicDirector.cancel();story=null;debugFight=null;setState(GS.PLAY);enemies=[];eBullets=[];pBullets=[];powerups=[];playerLocks=[];groundTargetingFx=[];V31.fx=[];V31.events=[];
 debugUnlocked=true;DBGT.god=true;DBGT.speed=1;DBGT.frozen=false;Input.pollGamepad=()=>{};for(const k of Object.keys(Input.keys))Input.keys[k]=false;Input.clearTaps();Input.mouse.down=false;
 player.x=worldWidth()/2;player.y=VH-65;player.invuln=1e9;
 if(typeof CP12!=='undefined')CP12.next=99999;if(typeof VP12!=='undefined')VP12.next=99999;
 s2VentTick=()=>{};s2Vents=[];geysers=[];
 mapScroll=levelScrollRange()*.35;drawWorld(0);
 for(let i=0;i<6;i++){window.__bofStepNow=(window.__bofStepNow||performance.now())+1000/60;loop(window.__bofStepNow);}
 let x=worldWidth()/2,y=PLAY.y-85;
 if(/lavamaw|pod|disc|modturret/.test(type))y=PLAY.y+110;
 window.E=spawnEnemy(type.startsWith('modturret')?'modturret':type,x,y,{_modWeapon:type==='modturret-laser'?'laser':'missile',_modStage:2});
 window.v31SavedSpawn=spawnEnemy;
 // Carrier is the sole fixture allowed to create its authored child squadron.
 if(type!=='carrier')spawnEnemy=()=>null;
 return E?{type:E.type,model:E._v31?.model,hp:E.hp,x:E.x,y:E.y}:null;
}"""
def ck(n,v,data=None):checks.append({'name':n,'passed':bool(v),'data':data});print('PASS'if v else'FAIL',n,str(data)[:300]if not v else'',flush=True)
def step(p,n):
 for i in range(0,n,4):
  err=p.evaluate(STEP,min(4,n-i))
  if err:raise RuntimeError(err)
  p.wait_for_timeout(1)
try:
 with sync_playwright()as pw:
  b=pw.chromium.launch(channel='msedge',headless=True,args=['--autoplay-policy=no-user-gesture-required']);p=b.new_page(viewport={'width':1280,'height':800})
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text)if m.type=='error'or'draw error'in m.text else None)
  p.goto(f'http://127.0.0.1:{port}/index.html',wait_until='load',timeout=180000)
  p.wait_for_function('window.__bofFrames>5&&typeof V31!=="undefined"');p.mouse.click(3,3);p.evaluate(TRAP_RAF);p.wait_for_timeout(40)
  p.evaluate("()=>{debugStartFight(debugFightFor(2,'boss'),{pilot:'cole'});spawnBoss(debugFightFor(2,'boss').kind);warnT=0;BOFCinematicDirector.cancel();setState(GS.PLAY);stageLoadBegin(2)}")
  p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(2)&&Object.values(V31_ART.banks).every(a=>XART.rdy(a.key))}',timeout=180000)
  for typ in ['ash','skim','cinderwasp','lance','ac10firejet','basaltbomber','cruc','miner','lavamaw','pod','disc','lavasnake','carrier','modturret-laser','modturret-missile']:
   initial=p.evaluate(SETUP,[typ,'hard']);ck(typ+' native identity at birth',initial is not None,initial);seen=set();trace=[]
   for f in range(0,900,4):
    step(p,4);q=p.evaluate('()=>({x:E.x,y:E.y,hp:E.hp,dead:!!E.dead,phase:E._v31?.phase||E._v31Ground?.phase,frame:E._v31Rendered?.frame,key:E._v31Rendered?.key,projectiles:eBullets.filter(b=>b._v31Kind).length})');trace.append(q)
    if q['phase'] not in seen and 20<f<650:seen.add(q['phase']);p.screenshot(path=str(O/(typ+'-'+str(q['phase'])+'.png')))
    if q['dead']:break
   events=p.evaluate('V31.events');runs.append({'type':typ,'initial':initial,'trace':trace,'events':events})
   ck(typ+' attacks or deploys through native owner',any(e['event']in['shot','turret-shot','beam','volcano-orb','deploy-jet','bite']for e in events),{'events':list({e['event']for e in events})})
   ck(typ+' HP remains native without player firing',p.evaluate('E.hp')==initial['hp'])
  for typ in ['ash','skim','cinderwasp','lance','ac10firejet','basaltbomber','cruc','miner','lavamaw','pod','disc','lavasnake','carrier']:
   p.evaluate(SETUP,[typ,'hard']);step(p,45)
   result=p.evaluate("""()=>{E.x=worldWidth()/2;E.y=230;window.v31Pixels=()=>{
    ctx.save();ctx.setTransform(1,0,0,1,0,0);ctx.clearRect(0,0,cv.width,cv.height);drawEnemy(E);ctx.restore();
    const a=ctx.getImageData(0,0,cv.width,cv.height).data;let white=0,color=0;for(let i=0;i<a.length;i+=4){if(a[i]>235&&a[i+1]>235&&a[i+2]>235)white++;if(Math.max(a[i],a[i+1],a[i+2])>45&&Math.max(a[i],a[i+1],a[i+2])-Math.min(a[i],a[i+1],a[i+2])>25)color++;}return{white,color};};
    const clean=v31Pixels();hitEnemy(E,.1);return{clean,hit:v31Pixels()};}""")
   step(p,30);result['expired']=p.evaluate('v31Pixels()');ck(typ+' native damaged pixels and flash expiry',result['clean']['color']>40 and result['hit']['white']>result['clean']['white']+80 and result['expired']['white']<result['hit']['white']*.8,result)
   n=p.evaluate('()=>{const old=ctx.rotate;let n=0;ctx.rotate=function(){n++;return old.apply(this,arguments)};try{drawEnemy(E)}finally{ctx.rotate=old}return n}');ck(typ+' hull and engines use authored cells without canvas rotation',n==0,n)
  p.evaluate(SETUP,['cruc','hard']);step(p,90)
  shield=p.evaluate('()=>{const hp=E.hp,before=E._esh.energy;hitEnemy(E,1);const held=E.hp===hp&&E._esh.energy<before;for(let i=0;i<20&&E._esh.energy>0;i++)hitEnemy(E,1);const broken=E._esh.energy<=0;hitEnemy(E,.5);return{held,broken,hullDamaged:E.hp<hp,once:E._esh.once}}');ck('Crucible shield absorbs first, breaks, then hull takes real damage',all(shield.values()),shield)
  p.evaluate(SETUP,['ac10firejet','hard']);step(p,120)
  eligibility=p.evaluate("()=>{const p=v31Gun(E),s=v31Shot(E,p,'slug',4,true),o=v31Shot(E,p,'orb',2,true),m=v31Shot(E,p,'thunder_missile',3,true);return{bullet:enemyOrdnanceCanIntercept(s),orb:enemyOrdnanceCanIntercept(o),missile:enemyOrdnanceCanIntercept(m),orbElement:enemyOrdnanceElement(o),guns:V31_ART.models.interceptor.guns.length};}")
  ck('Fire bullets reject offensive interception from birth; magma/missiles retain it',eligibility['bullet']is False and eligibility['orb'] and eligibility['missile'] and eligibility['guns']==4,eligibility)
  p.evaluate(SETUP,['disc','hard']);step(p,240)
  d=p.evaluate('()=>({spikes:V31_ART.models.disc.spikes.every(q=>q.length===9),beams:V31.events.filter(q=>q.event==="beam").length,poses:V31_ART.models.disc.banks.spin.frames})');ck('Magma Disc has exactly nine actual spike sockets and simultaneous beams',d['spikes']and d['beams']>=9 and d['beams']%9==0,d)
  counts=[]
  for mode in ['normal','hard','furious']:
   p.evaluate(SETUP,['modturret-laser',mode]);step(p,600);counts.append(p.evaluate('V31.events.filter(e=>e.event==="turret-shot").length'))
  ck('Laser turret cadence increases Normal to Hard to Furious',0<counts[0]<counts[1]<counts[2],counts)
  for typ in ['lavamaw','pod','basaltbomber']:
   p.evaluate(SETUP,[typ,'hard']);orb=None
   for i in range(80):
    step(p,4);orb=p.evaluate('()=>groundTargetingFx.some(q=>q._v31Drop?.bullet&&!q.impact&&!q.dead&&!q._v31Drop.bullet.dead&&Math.hypot(q._v31Drop.bullet.x-E.x,q._v31Drop.bullet.y-E.y)>Math.max(E.w,E.h)*.95)')
    if orb:break
   ck(typ+' arcing magma has real native shootable projectile',orb)
   if orb:
    p.evaluate("()=>{const q=groundTargetingFx.find(q=>q._v31Drop?.bullet&&!q.impact&&!q.dead&&Math.hypot(q._v31Drop.bullet.x-E.x,q._v31Drop.bullet.y-E.y)>Math.max(E.w,E.h)*.95);window.arcTest=q;const b=q._v31Drop.bullet;pShard(b.x,b.y,0,1,{mul:20});pBullets.at(-1).vx=pBullets.at(-1).vy=0;}")
    step(p,4);value=p.evaluate('()=>({qdead:arcTest.dead,bulletDead:arcTest._v31Drop.bullet.dead,impact:arcTest.impact,hp:arcTest._v31Drop.bullet.hp,shots:pBullets.length})');ck(typ+' native player projectile cancels orb and landing Retina',value['qdead']and value['bulletDead']and not value['impact'],value)
  for typ in ['modturret-laser','modturret-missile']:
   p.evaluate(SETUP,[typ,'hard']);ck(typ+' full visible hull reserved on authored clear terrain',p.evaluate('v31GroundLegal(E,E.x,E.y)'))
  p.evaluate(SETUP,['carrier','hard']);step(p,600)
  roles=p.evaluate('V31.events.filter(e=>e.event==="deploy-jet").map(e=>e.role)');ck('Carrier deploys all four authored weapon roles',set(roles)=={'flame','balls','guns','wall'},roles)
  rejected=p.evaluate('()=>{spawnEnemy=window.v31SavedSpawn;return["eye","magmaeye","magmaorb"].every(t=>spawnEnemy(t,300,100)===null)}');ck('Retired Magma Eye/Orb cannot spawn through legacy routes',rejected)
  ck('No native page/console errors',not errors,errors[:20]);b.close()
finally:
 (O/'smoke-checks.json').write_text(json.dumps(checks,indent=2));(O/'smoke-runs.json').write_text(json.dumps(runs));(O/'smoke-errors.json').write_text(json.dumps(errors,indent=2));stop()
if errors or any(not c['passed']for c in checks):sys.exit(1)
