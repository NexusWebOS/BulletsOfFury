"""Live native Stage2 smoke/attack/pixel evidence. No stand-in renderers."""
from pathlib import Path
import sys,json,http.server
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'_BUILD_SOURCE'))
from shoot import serve,STEP,TRAP_RAF
O=R/'_shots/stage3_amplify_1031';O.mkdir(exist_ok=True)
port,stop=serve(str(R));http.server.ThreadingHTTPServer.request_queue_size=256
errors=[];checks=[];runs=[]
SETUP="""([type,mode])=>{
 if(window.i31SavedSpawn)spawnEnemy=window.i31SavedSpawn;
 diffKey=mode;DIFF=difficultyForRun('arcade',mode);run.mode='campaign';run.stage=3;
 stagePlan=[];waveIdx=999;spawnClock=9999;_adaptiveSpawnT=99999;stageTimer=1;
 boss=null;subBoss=null;bossActive=subBossActive=false;bossWarned=true;subBossDone=true;stageEnding=false;
 BOFCinematicDirector.cancel();story=null;thaw=null;debugFight=null;setState(GS.PLAY);enemies=[];eBullets=[];pBullets=[];powerups=[];playerLocks=[];groundTargetingFx=[];I31.fx=[];I31.events=[];
 debugUnlocked=true;DBGT.god=true;DBGT.speed=1;DBGT.frozen=false;Input.pollGamepad=()=>{};for(const k of Object.keys(Input.keys))Input.keys[k]=false;Input.clearTaps();Input.mouse.down=false;
 player.x=worldWidth()/2;player.y=VH-65;player.invuln=1e9;
 if(typeof CP12!=='undefined')CP12.next=99999;if(typeof VP12!=='undefined')VP12.next=99999;
 s2VentTick=()=>{};s2Vents=[];geysers=[];
 mapScroll=levelScrollRange()*.35;drawWorld(0);
 for(let i=0;i<6;i++){window.__bofStepNow=(window.__bofStepNow||performance.now())+1000/60;loop(window.__bofStepNow);}
 let x=worldWidth()/2,y=PLAY.y-85;
 if(/cryoeye|modturret/.test(type))y=PLAY.y+110;
 window.E=spawnEnemy(type.startsWith('modturret')?'modturret':type,x,y,{_modWeapon:type==='modturret-laser'?'laser':'sonic',_modStage:3});
 window.i31SavedSpawn=spawnEnemy;
 // Carrier is the sole fixture allowed to create its authored child squadron.
 if(type!=='carrier')spawnEnemy=()=>null;
 return E?{type:E.type,model:E._i31?.model,hp:E.hp,x:E.x,y:E.y}:null;
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
  p.wait_for_function('window.__bofFrames>5&&typeof I31!=="undefined"');p.mouse.click(3,3);p.evaluate(TRAP_RAF);p.wait_for_timeout(40)
  p.evaluate("()=>{debugStartFight(debugFightFor(3,'boss'),{pilot:'cole'});spawnBoss(debugFightFor(3,'boss').kind);warnT=0;BOFCinematicDirector.cancel();setState(GS.PLAY);stageLoadBegin(3)}")
  p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(3)&&Object.values(I31_ART.banks).every(a=>XART.rdy(a.key))}',timeout=180000)
  for typ in ['sharddart','s3interceptor','ac10icejet','glaciercarrier','cryoeye','s3mine','modturret-laser','modturret-sonic']:
   initial=p.evaluate(SETUP,[typ,'hard']);ck(typ+' current native identity',initial is not None,initial)
   if not initial:continue
   seen=set();trace=[]
   for f in range(0,900,4):
    step(p,4);q=p.evaluate('()=>({x:E.x,y:E.y,hp:E.hp,dead:!!E.dead,phase:E._i31?.phase||E._i31Ground?.phase,frame:E._i31Rendered?.frame,key:E._i31Rendered?.key,dir:E._i31Rendered?.dir,projectiles:eBullets.filter(b=>b._i31Kind).length})');trace.append(q)
    if q['phase']not in seen and 20<f<650:seen.add(q['phase']);p.screenshot(path=str(O/(typ+'-'+str(q['phase'])+'.png')))
    if q['dead']:break
   events=p.evaluate('I31.events');runs.append({'type':typ,'initial':initial,'trace':trace,'events':events})
   ck(typ+' releases native attack',any(e['event']in['shot','cross-lasers']for e in events),events[-5:])
   ck(typ+' retains native HP',p.evaluate('E.hp')==initial['hp'])
   if typ=='sharddart':ck('Shard Dart never flips',all(q.get('dir')==0 and 'drift'in(q.get('key')or'')for q in trace))
   if typ in ['ac10icejet','s3interceptor']:ck(typ+' uses actual turning poses',len({q.get('dir')for q in trace})>=4)
   if typ.startswith('modturret'):ck(typ+' remains on full island footprint',p.evaluate('i31Legal(E,E.x,E.y)'))
  for typ in ['sharddart','s3interceptor','ac10icejet','glaciercarrier','cryoeye','s3mine','modturret-laser','modturret-sonic']:
   p.evaluate(SETUP,[typ,'hard']);step(p,45)
   q=p.evaluate("""()=>{E.x=worldWidth()/2;E.y=230;window.icePixels=()=>{ctx.save();ctx.setTransform(1,0,0,1,0,0);ctx.clearRect(0,0,cv.width,cv.height);drawEnemy(E);ctx.restore();const a=ctx.getImageData(0,0,cv.width,cv.height).data;let white=0,color=0;for(let i=0;i<a.length;i+=4){if(a[i]>235&&a[i+1]>235&&a[i+2]>235)white++;if(Math.max(a[i],a[i+1],a[i+2])>45&&Math.max(a[i],a[i+1],a[i+2])-Math.min(a[i],a[i+1],a[i+2])>25)color++;}return{white,color};};const clean=icePixels();hitEnemy(E,.1);return{clean,hit:icePixels()};}""")
   step(p,30);q['expired']=p.evaluate('icePixels()');ck(typ+' actual damaged pixels and expiry',q['clean']['color']>30 and q['hit']['white']>q['clean']['white']+60 and q['expired']['white']<q['hit']['white']*.85,q)
  p.evaluate(SETUP,['cryoeye','hard']);step(p,245)
  q=p.evaluate('()=>({events:I31.events.filter(e=>e.event==="cross-lasers"),lanes:E._i31.lanes,beams:E._i31.beams})');ck('Cryoeye fires exactly four + beams',q['events']and all(e['count']==4 for e in q['events']) and len(q['lanes'])==4,q)
  p.evaluate(SETUP,['ac10icejet','hard']);step(p,90)
  q=p.evaluate('()=>{const e=E,p=i31Gun(e),s=i31Shot(e,p,"slug",true),m=i31Shot(e,p,"mine",true);return{guns:i31M(e).guns.length,bullet:enemyOrdnanceCanIntercept(s),mine:enemyOrdnanceCanIntercept(m),element:enemyOrdnanceElement(m)}}');ck('Two interceptor mounts, bullet immunity and shootable ice mines from birth',q['guns']==2 and not q['bullet']and q['mine']and q['element']=='ice',q)
  ck('No native page/console errors',not errors,errors[:20]);b.close()

finally:
 (O/'smoke-checks.json').write_text(json.dumps(checks,indent=2));(O/'smoke-runs.json').write_text(json.dumps(runs));(O/'smoke-errors.json').write_text(json.dumps(errors,indent=2));stop()
if errors or any(not c['passed']for c in checks):sys.exit(1)
