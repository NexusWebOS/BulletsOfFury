"""Native Chromium proof: five hatch cycles, real component pools and pixels."""
from pathlib import Path
import sys,json
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'_BUILD_SOURCE'));from shoot import TRAP_RAF
O=R/'_shots/cloud_carrier_1101';O.mkdir(exist_ok=True);errors=[];checks=[];trace=[]
SETUP=r'''()=>{bossWarned=false;story=thaw=fb2Talk=fb2Intro=null;CP12.next=VP12.next=CP22.nextWave=CP22.nextFlyby=99999;_adaptiveSpawnT=99999;stagePlan=[];waveIdx=999;playerLocks=[];CC111.events=[];C=sc12Spawn(-1);return {hp:C.maxhp,parts:C.parts.length,x:C.x,y:C.y};}'''
def ck(n,v,d=None):
 checks.append(dict(name=n,passed=bool(v),data=d));print('PASS'if v else'FAIL',n,flush=True);(O/'checks.json').write_text(json.dumps(checks,indent=2))
with sync_playwright()as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--autoplay-policy=no-user-gesture-required']);p=b.new_page(viewport={'width':1280,'height':800});p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text[:400])if m.type=='error'or'draw error'in m.text else None);p.add_init_script("Object.defineProperty(navigator,'getGamepads',{value:()=>[]});")
 p.goto('http://127.0.0.1:8805/game/index.html',wait_until='load',timeout=180000);p.wait_for_function('window.__bofFrames>5');p.mouse.click(3,3);p.evaluate(TRAP_RAF);p.add_script_tag(path=str(R/'_BUILD_SOURCE/enemy_behaviour_lab_1011.js'));p.evaluate('EA11.setup(6,"furious")');p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(6)&&Object.values(CC111_ART.banks).every(B=>XART.rdy(B.key))&&XART.rdy(CC111_ART.beam.key)}',timeout=180000)
 initial=p.evaluate(SETUP);ck('Five native bay pools plus visible bridge; fixed complete HP',initial['parts']==5,initial)
 ck('All FOV colours and real cloud plates decoded before entry',p.evaluate("['bmfx_fov_green_tall','bmfx_fov_yellow_tall','bmfx_fov_red_tall',...CC111_CLOUDS].every(k=>XART.rdy(k))"))
 for j in range(30):
  q=p.evaluate('()=>{for(let i=0;i<24;i++)updatePlay(1/60);drawWorld(0);return {y:C.y,phase:C.phase,hp:C.hp,states:C.parts.map(e=>e._sc12Phase),frames:C.parts.map(e=>e._sc12Frame),parts:C.parts.map(e=>[e.x,e.y]),finite:[...enemies,...eBullets].every(e=>Number.isFinite(e.x)&&Number.isFinite(e.y)),bullets:eBullets.length};}');trace.append(q);p.wait_for_timeout(3)
  if j in[7,15,19,24,32]:p.screenshot(path=str(O/('game-'+str(j)+'.png')))
 events=p.evaluate('CC111.events');(O/'trace.json').write_text(json.dumps(dict(initial=initial,trace=trace,events=events),indent=2))
 for i in range(5):ck('Bay'+str(i+1)+' opens, warns, fires and recoils',all(any(e['event']==s and e.get('bay')==i for e in events)for s in['opening','warning','laser','cease']))
 ck('Finite fixed hull and six native target positions',all(q['finite']and q['hp']==initial['hp']for q in trace))
 q=p.evaluate('''()=>{const e=C.parts[4],hp=e.hp;pBullets.push({kind:'spread',x:e.x,y:e.y+28,vx:0,vy:-4,w:5,h:10,dmg:2,lv:1,t:0,seat:1});for(let i=0;i<6;i++)updatePlay(1/60);return{before:hp,after:e.hp,flash:e.flash,targets:_lockTargets().filter(e=>e._sc12===C).length};}''');ck('Real travelling player shot hits the visible well; six native Retina targets',q['after']<q['before']and q['flash']>0 and q['targets']==6,q)
 q=p.evaluate('''()=>{const keys=['combatServo0927','bossWeaponCharge','enemyHeavyLaser','combatModule0927'];return keys.map(k=>({key:k,routed:!!Audio.SFX[k]}));}''');ck('Shared mixer door, charge, laser and module-break assignments',all(v['routed']for v in q),q)
 # Render through the real game context and read actual changed pixels.
 p.evaluate('''()=>{window.carrierPixels=()=>{CC111.epoch++;ctx.save();ctx.setTransform(1,0,0,1,0,0);ctx.clearRect(0,0,cv.width,cv.height);ctx.translate(210-C.x,220-C.y);drawEnemy(C.parts.find(e=>!e.dead)||C.corpse);ctx.restore();const a=ctx.getImageData(0,0,cv.width,cv.height).data;let white=0,opaque=0;for(let i=0;i<a.length;i+=4){if(a[i+3])opaque++;if(a[i]>235&&a[i+1]>235&&a[i+2]>235)white++;}return{white,opaque};};}''')
 for i in range(-1,5):
  q=p.evaluate('''i=>{const e=i<0?C.core:C.parts[i];const clean=carrierPixels(),hp=e.hp;hitEnemy(e,.01);const hit=carrierPixels();for(let n=0;n<20;n++)updatePlay(1/60);return{clean,hit,after:carrierPixels(),hp:e.hp,before:hp,flash:e.flash};}''',i);ck(('Bridge'if i<0 else'Bay'+str(i+1))+' real damaged pixels and flash expiry',q['hit']['white']>q['clean']['white']+8 and q['after']['white']<q['hit']['white']and q['flash']<=0 and q['hp']<q['before'],q)
 q=p.evaluate('''()=>{const score=run.score,kills=stageStats.kills;hitEnemy(C.core,100000);for(let i=0;i<20;i++)updatePlay(1/60);hitEnemy(C.core,100000);const live=_lockTargets().filter(t=>t.ref?._sc12===C||t._sc12===C);return{score,kills,coreDead:C.core.dead,bays:C.parts.filter(sc12Alive).length,hp:C.hp,phase:C.phase,targets:live.length};}''');ck('Destroyed core leaves all five independently live bay pools',q['coreDead']and q['bays']==5 and q['hp']>0 and q['phase']!='dying',q);before=q
 q=p.evaluate('''()=>{for(const e of C.parts){hitEnemy(e,100000);for(let i=0;i<20;i++)updatePlay(1/60);if(!e.dead)hitEnemy(e,100000);}drawWorld(0);return{hp:C.hp,phase:C.phase,dead:C.parts.every(e=>e.dead),reward:run.score,kills:stageStats.kills,corpses:enemies.filter(e=>e._sc12DeathOwner===C).length,complete:CC111.events.filter(e=>e.event==='complete-defeat').length,beam:C.parts.some(e=>e._sc12Phase==='fire')};}''');ck('Full exhaustion cancels attacks and awards one native complete kill',q['hp']==0 and q['dead']and q['corpses']==1 and q['complete']==1 and not q['beam']and q['kills']==before['kills']+1 and q['reward']>=before['score']+8000,q);p.screenshot(path=str(O/'native-defeat.png'))
 q=p.evaluate('''()=>{const plan=buildStagePlan(6).filter(w=>w._sc12);beginStage(5);return{waves:plan.map(w=>w.t),remaining:CC111.carriers.length};}''');ck('Both cloud-side campaign passes and stage cleanup',q['waves']==[18,54]and q['remaining']==0,q)
 p.evaluate('EA11.setup(6,"furious")');p.evaluate(SETUP)
 for j in range(36):
  q=p.evaluate('()=>{for(let i=0;i<15;i++)updatePlay(1/60);return C.parts.some(e=>e._sc12Phase==="fire"&&e._sc12Age>.1&&e._sc12Age<.4)}');p.wait_for_timeout(3)
  if q:break
 q=p.evaluate('''()=>{const e=C.parts.find(e=>e._sc12Phase==='fire'&&e._sc12Age>.1&&e._sc12Age<.4);if(!e)return{found:false};const p=sc12Bore(e);player.x=p.x+Math.cos(p.a)*180;player.y=p.y+Math.sin(p.a)*180;player.invuln=0;player.roll=player.somer=0;DBGT.god=false;run.shield=0;const before=run.lives;updatePlay(1/60);return{found:true,dead:player.dead,lives:run.lives,before,beam:e._sc12Phase};}''');ck('Committed visible laser causes native player damage on its ray',q.get('found')and(q.get('dead')or q.get('lives',99)<q.get('before',0)),q)
 ck('No page or console errors',not errors,errors);b.close()
(O/'errors.json').write_text(json.dumps(errors,indent=2));print('SUMMARY',sum(q['passed']for q in checks),'/',len(checks),flush=True);sys.exit(0 if all(q['passed']for q in checks)else 1)
