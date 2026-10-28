from pathlib import Path
from playwright.sync_api import sync_playwright
import sys,json,base64,http.server
R=Path(r'C:\Users\Mike\Desktop\Github Coding\BulletsOfFury');W=R/'_ART_SOURCES/pressure_1022' if Path(__file__).parent.name=='_BUILD_SOURCE' else Path(__file__).parent/'BOF-Pressure-1022'
O=R/'_shots/pressure_1022';O.mkdir(parents=True,exist_ok=True)
sys.path.insert(0,str(R/'_BUILD_SOURCE'));import shoot
checks=[];errors=[]
def ck(name,ok,data=None):
 checks.append(dict(name=name,ok=bool(ok),data=data));print(('PASS ' if ok else 'FAIL ')+name+(' '+str(data) if not ok else ''),flush=True)
http.server.ThreadingHTTPServer.request_queue_size=128;port,stop=shoot.serve(str(R))
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(channel='msedge',args=['--autoplay-policy=no-user-gesture-required']);p=br.new_page(viewport=dict(width=1280,height=1000));p.set_default_timeout(180000)
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text[:500]) if m.type=='error' or 'draw error' in m.text else None)
  p.goto(f'http://127.0.0.1:{port}');p.wait_for_function('window.__bofFrames>4');p.evaluate(shoot.TRAP_RAF);p.mouse.click(600,400)
  p.wait_for_function('()=>Object.values(CP22_ART.sheets).map(S=>XART.rdy(S.key)).every(Boolean)')
  p.evaluate('''()=>{window.cpFresh=n=>{run.stage=n;curStage=STAGES[n-1];state=GS.PLAY;story=null;fb2Talk=null;s6Wing=null;RADIO17.hold=false;enemies=[];eBullets=[];pBullets=[];stagePlan=[];boss=null;subBoss=null;bossActive=subBossActive=bossWarned=bossDefeated=false;warnT=0;stageTimer=0;CP22.age=0;CP22.pending=[];CP22.events=[];CP22.nextWave=999;CP22.nextFlyby=999;player.reset();player.invuln=9999;};window.cpPaint=()=>{ctx.setTransform(SS,0,0,SS,0,0);ctx.globalAlpha=1;ctx.globalCompositeOperation='source-over';ctx.fillStyle='#101722';ctx.fillRect(0,0,VW,VH);};window.cpPixels=()=>Array.from(ctx.getImageData(0,0,cv.width,cv.height).data);window.cpDiff=(a,b)=>{let n=0;for(let i=0;i<a.length;i+=4)if(a[i]!==b[i]||a[i+1]!==b[i+1]||a[i+2]!==b[i+2])n++;return n;};}''')
  for n in [6,7,8]:
   out=p.evaluate(shoot.SETUP,dict(state='PLAY',stage=n,pilot='cole',invuln=True));ck('Stage '+str(n)+' initializes',out.get('ok'),out)
   p.wait_for_function(f'()=>{{stageLoadTick();return stageLoadReady({n});}}')
  for source,model in [('s7skimmer','slimejet'),('s7serpent','slimejet'),('s7sampler','sewerdrone'),('s7lamprey','sewerheavy'),('s7mine','sewerdrone'),('s7canister','sewerheavy'),('mm1003_hexpyre','sewerheavy'),('mm1003_impharrow','sewerdrone')]:
   row=p.evaluate('''type=>{cpFresh(7);const e=spawnEnemy(type,worldWidth()/2,160);drawEnemy(e);return {type:e.type,model:bf22Model(e)?.id,render:e._bf22Rendered,hp:e.hp,role:e._cp22Sewer?.role};}''',source);ck(source+' routes to coherent toxic hull',row.get('model')==model and row.get('render',{}).get('id')==model,row)
  for source in ['s7barge','s7pipe','s7walker','s7tank']:
   row=p.evaluate('''type=>{cpFresh(7);const e=spawnEnemy(type,200,140);return {type:e?.type,custom:!!e?._cp22Sewer};}''',source);ck(source+' ground/fixture owner retained',not row['custom'],row)
  for source,model in [('s7skimmer','slimejet'),('s7sampler','sewerdrone'),('s7lamprey','sewerheavy')]:
   for kind in ['idle','attack','drift','roll','somer']:
    row=p.evaluate('''([type,kind])=>{cpFresh(7);const e=spawnEnemy(type,VW/2,160),S=e._cp22Sewer;S.phase=kind==='attack'?'tell':kind==='drift'?'move':'recover';S.warm=1;S.t=.5;if(['roll','somer'].includes(kind))e._air13Motion={kind,t:.35,dur:.7};cpPaint();drawEnemy(e);return e._bf22Rendered;}''',[source,kind]);ck(model+' '+kind+' native bank',row and row['kind']==kind,row)
   row=p.evaluate('''type=>{cpFresh(7);const e=spawnEnemy(type,VW/2,160);cpPaint();drawEnemy(e);const a=cpPixels();markHit(e,.18);cpPaint();drawEnemy(e);const b=cpPixels();for(let i=0;i<20;i++)updatePlay(1/60);return {pixels:cpDiff(a,b),expired:e.flash<=0};}''',source);ck(model+' visible flash expires',row['pixels']>10 and row['expired'],row)
   row=p.evaluate('''type=>{cpFresh(7);const e=spawnEnemy(type,worldWidth()/2,150),S=e._cp22Sewer;S.seq=0;sp22Tell(e);const target={...S.target};player.x+=110;let maxShots=0,owned=true,locked=true;const themes=new Set();for(let i=0;i<160;i++){updatePlay(1/60);if(S.seq===1&&target.x!==S.target.x)locked=false;const own=eBullets.filter(b=>b._bf22Owner===e);maxShots=Math.max(maxShots,own.length);for(const b of own)themes.add(b._bf22Theme);}drawEnemy(e);return {shots:maxShots,themes:[...themes],owner:owned,locked,history:SP22.events.slice(-5),render:e._bf22Rendered};}''',source);ck(model+' warned shots use owned toxic effects',row['shots']>0 and row['owner'] and row['themes']==['toxic'] and row['locked'],row)
  for side in [-1,1]:
   row=p.evaluate('''side=>{cpFresh(6);const e=cp22DashSpawn(side,VH*.55),D=e._cp22Dash,from=e.x;cp22DashTick(e,D.warm-.01);const held=e.x===from;player.y+=60;cp22DashTick(e,.02);const y=e.y;for(let i=0;i<200&&!e.dead;i++)cp22DashTick(e,1/60);return {held,dead:e.dead,locked:e.y===y,events:CP22.events,score:run.score};}''',side);ck('Dasher '+str(side)+' warns, commits and detonates at exit',row['held'] and row['dead'] and row['locked'] and any(x['event']=='dasher-edge-detonation' for x in row['events']),row)
  row=p.evaluate('''()=>{cpFresh(6);cp22Wave();for(let i=0;i<900;i++)updatePlay(1/60);return {launch:CP22.events.filter(e=>e.event==='dasher-launch').length,exit:CP22.events.filter(e=>e.event==='dasher-edge-detonation').length,waves:CP22.events.filter(e=>e.event==='dasher-wave').length};}''');ck('Native update runs full bounded crossing wave',row['launch']>=4 and row['exit']==row['launch'],row)
  row=p.evaluate('''()=>{cpFresh(6);CP22.nextWave=0;RADIO17.hold=true;cp22Tick(5);const radio=CP22.pending.length===0;RADIO17.hold=false;story={id:'held-scene'};cp22Tick(5);const scene=CP22.pending.length===0;story=null;subBossActive=true;cp22Tick(5);return {radio,scene,boss:CP22.pending.length===0};}''');ck('No new waves during radio/cinematic/miniboss',all(row.values()),row)
  for mode in ['bomb','rain','charge']:
   row=p.evaluate('''mode=>{cpFresh(6);const q=fb2FlightPlan('east');q._cp22Mode=mode;const e=fb2FlightSpawn(q);e.x=camLeftX()+80;e.y=viewTopY()+160;for(let i=0;i<200&&!e.dead;i++)fb2FlightTick(e,1/60);return {mode:e._cp22Flight.mode,events:CP22.events,bullets:eBullets.length,retinas:groundTargetingFx.filter(g=>g.owner===e).length};}''',mode);ck('Flyby '+mode+' actually releases',any(x['event']=='flyby-tell' for x in row['events']) and (row['retinas']>0 if mode=='bomb' else row['bullets']>0 if mode=='rain' else True),row)
  p.wait_for_function('XART.rdy("ship_cole_so0")')
  # Activate the real evasion functions rather than fabricating their flags.
  for evade in ['roll','somer']:
   row=p.evaluate('''evade=>{cpFresh(6);const e=cp22DashSpawn(1,VH*.55),D=e._cp22Dash;D.phase='dash';e.x=player.x-30;D.y=e.y=player.y;player.invuln=0;player.roll=player.somer=null;player._rollCool=player._somerCool=0;if(evade==='roll')startRoll(1);else startSomersault();const activated=!!player[evade],shield=run.shield;cp22DashTick(e,.05);return {activated,alive:!player.dead,shield:run.shield===shield,evade};}''',evade);ck('Crossing respects '+evade+' invulnerability',row['activated'] and row['alive'] and row['shield'],row)
  # Native renderer, original terrain and part targets. No surrogate scene drawing.
  for n in [6,7,8]:
   p.evaluate(shoot.SETUP,dict(state='PLAY',stage=n,pilot='cole',invuln=True));p.wait_for_function(f'()=>{{stageLoadTick();return stageLoadReady({n});}}')
   p.evaluate('''n=>{cpFresh(n);if(n===6){const e=cp22DashSpawn(1,VH*.60);e._cp22Dash.t=e._cp22Dash.warm*.6;const q=fb2FlightPlan('west');q._cp22Mode='rain';const f=fb2FlightSpawn(q);f.x=VW*.7;f.y=130;cp22FlightTell(f,f._cp22Flight);}if(n===7){mapScroll=0;for(const [i,t] of ['s7skimmer','s7sampler','s7lamprey'].entries()){const e=spawnEnemy(t,100+i*140,120+i%2*60);sp22Tell(e);e._cp22Sewer.t=.5;}}if(n===8){spawnSubBoss__inner('heralddeath');subBoss.enter=false;subBossActive=true;subBoss.x=VW/2;subBoss.y=160;hp22Start(subBoss,'talon-dive');hp22Lock(subBoss);subBoss._hd1003._hp22.t=.6;}ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);}''',n)
   (O/('stage-'+str(n)+'.png')).write_bytes(base64.b64decode(p.evaluate('cv.toDataURL().split(",")[1]')))
  for kind in ['talon-dive','swoop','feathers']:
   row=p.evaluate('''kind=>{cpFresh(8);spawnSubBoss__inner('heralddeath');const b=subBoss;b.enter=false;subBossActive=true;b.x=VW/2;b.y=150;const hp=b.hp;hp22Start(b,kind);hp22Lock(b);const P=b._hd1003._hp22,target={...P.target};player.x+=100;let recovery=false;for(let i=0;i<700&&b._hd1003._hp22;i++){hd1003Tick(b,1/60);if(b._hd1003._hp22?.phase==='recover')recovery=true;}return {hp:b.hp===hp,recovery,finished:!b._hd1003._hp22,locked:target.x===P.target.x,shots:eBullets.filter(b=>b._hp22Feather).length,events:HP22.events.slice(-8)};}''',kind);ck('Herald '+kind+' warns, commits and recovers',row['hp'] and row['recovery'] and row['finished'] and row['locked'] and (row['shots']>0 if kind=='feathers' else True),row)
  row=p.evaluate('''()=>{cpFresh(8);spawnSubBoss__inner('heralddeath');const b=subBoss;b.enter=false;b.x=VW/2;b.y=160;subBossActive=true;hp22Start(b,'feathers');hp22Lock(b);const part=hd1003Part(b,'wingL');hd1003Break(b,part);const P=b._hd1003._hp22;P.phase='strike';P.t=0;hd1003Tick(b,1/60);const cancelled=eBullets.every(q=>q._heraldPart1003!=='wingL'),targets=retinaBossTargets(b).length;const head=hd1003Part(b,'head');cpPaint();heraldDeathDraw(b);const a=cpPixels();markHit(head,.18);cpPaint();heraldDeathDraw(b);const pixels=cpDiff(a,cpPixels());for(let i=0;i<20;i++)updateSubBoss(1/60);return {cancelled,targets,pixels,expired:head.flash<=0,parts:b._hd1003.parts.length};}''');ck('Herald broken launcher cancels, live animated head flashes',row['cancelled'] and row['targets']==row['parts']-1 and row['pixels']>10 and row['expired'],row)
  row=p.evaluate('''()=>{cpFresh(8);spawnSubBoss__inner('heralddeath');const b=subBoss;b.enter=false;subBossActive=true;b.x=VW/2;b.y=150;b.hp=b.maxhp*.3;hp22Start(b,'swoop');return {passes:b._hd1003._hp22.total,warm:b._hd1003._hp22.warm};}''');ck('Herald last stand has separately warned double pass',row['passes']==2 and row['warm']>=.9,row)
  p.evaluate(shoot.SETUP,dict(state='PLAY',stage=7,pilot='cole',invuln=True));p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(7)&&XART.rdy("nst7_master_v3");}')
  row=p.evaluate('''()=>{cpFresh(7);mapScroll=0;state=GS.LAUNCH;drawLevelMaster(1);const held=mapScroll===0;state=GS.PLAY;_bossHold=0;drawLevelMaster(.5);const a={scroll:mapScroll,src:_masterSrcY};drawLevelMaster(.5);return {held,state,a,b:{scroll:mapScroll,src:_masterSrcY}};}''');ck('Sewer entrance holds for arrival then leaves with world scroll',row['held'] and row['b']['scroll']>row['a']['scroll'] and row['b']['src']<row['a']['src'],row)
  p.evaluate('()=>{window.BOF_ENEMY_ATLAS?.mute(false);Audio.resume();Snd.prepare(CP22_CUES.map(n=>{const a=CA15.aliases[n]||n;return window.BOF_CHIP_PASS?.aliases[a]||a;}));}')
  p.wait_for_timeout(1200)
  for cue in ['jetDash','enemyMachineGunLight','atomicLaunch','atomicDetonate','bossWeaponCharge','combatAlien0927','combatToxic0927','bossfireVileexistence']:
   row=p.evaluate('''async key=>{const a=CA15.aliases[key]||key,k=window.BOF_CHIP_PASS?.aliases[a]||a;await Snd._audioCtx().resume();Snd.stopCue(k);Snd._last[k]=0;AV3.last.clear();const owner={};combatAudioTick0927(1);const requested=combatAudio0927(owner,key,0);let el=null;for(let i=0;i<100;i++){el=Snd.pools[k]?.slots.find(s=>s?.attached&&!s.el.paused&&s.el.currentTime>0)?.el;if(el)break;await new Promise(r=>setTimeout(r,10));}return {cue:key,canonical:k,requested,playing:!!el,ready:el?.readyState,volume:el?.volume};}''',cue)
   ck(cue+' plays decoded audio through native mixer',row['requested'] and row['playing'] and row.get('ready',0)>=2 and row.get('volume',0)>0,row)
  # Capture short sequences from the actual game renderer, including moving
  # hazards and the unchanged explosion owner. These are review clips, not wins.
  from PIL import Image
  import io
  for n in [6,7,8]:
   p.evaluate(shoot.SETUP,dict(state='PLAY',stage=n,pilot='cole',invuln=True));p.wait_for_function(f'()=>{{stageLoadTick();return stageLoadReady({n});}}')
   p.evaluate('''n=>{cpFresh(n);stageTimer=3;waveIdx=999;spawnClock=9999;_adaptiveSpawnT=9999;player.x=worldWidth()/2;player.y=VH-100;player.invuln=99999;
    if(n===6){CP22.nextWave=.2;CP22.nextFlyby=1;CP22.waves=0;}
    if(n===7){for(const [i,type] of ['s7skimmer','s7sampler','s7lamprey'].entries())spawnEnemy(type,camLeftX()+viewW()*(.23+i*.27),100+i%2*65);}
    if(n===8){spawnSubBoss__inner('heralddeath');subBoss.enter=false;subBossActive=true;subBoss.x=worldWidth()/2;subBoss.y=145;hp22Start(subBoss,'swoop');}
   }''',n)
   frames=[]
   for i in range(36):
    p.evaluate('''()=>{for(let i=0;i<10;i++){efxClock+=1/60;updatePlay(1/60);ctx.setTransform(SS,0,0,SS,0,0);drawWorld(1/60);}}''')
    frames.append(Image.open(io.BytesIO(base64.b64decode(p.evaluate('cv.toDataURL().split(",")[1]')))).convert('RGB'))
   frames[0].save(O/('stage-'+str(n)+'.gif'),save_all=True,append_images=frames[1:],duration=167,loop=0)
  ck('No native renderer errors',not errors,errors);br.close()
finally:stop()
(O/'report.json').write_text(json.dumps(dict(checks=checks,errors=errors),indent=2),encoding='utf-8');print(json.dumps(dict(checks=len(checks),passed=sum(q['ok'] for q in checks),errors=errors)));sys.exit(bool(errors) or not all(q['ok'] for q in checks))
