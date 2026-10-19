"""Native Chromium: truck modules / hit pixels / live Furnace hazards."""
from pathlib import Path
import base64,io,json,sys,http.server
import numpy as np
from PIL import Image
from playwright.sync_api import sync_playwright
import shoot

ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'_shots/truck_furnace_1018/native';OUT.mkdir(parents=True,exist_ok=True)
checks=[];errors=[];measures=[]
def check(name,ok,data=None):
 checks.append({'name':name,'passed':bool(ok),'data':data});print(('PASS ' if ok else 'FAIL ')+name+((' '+json.dumps(data)) if not ok else ''),flush=True)
http.server.ThreadingHTTPServer.request_queue_size=128
port,stop=shoot.serve(str(ROOT))
try:
 with sync_playwright() as pw:
  browser=pw.chromium.launch(channel='msedge',args=['--mute-audio']);p=browser.new_page(viewport={'width':1600,'height':900});p.set_default_timeout(180000)
  # A physically connected controller also reaches headless Chromium. Isolate
  # hardware input in this test page; native keyboard/weapon code still runs.
  p.add_init_script("Object.defineProperty(navigator,'getGamepads',{value:()=>[]});")
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text[:500]) if m.type=='error' or 'draw error' in m.text else None)
  p.on('response',lambda r:errors.append(str(r.status)+' '+r.url) if r.status>=400 else None)
  p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('window.__bofFrames>4');p.evaluate(shoot.TRAP_RAF);p.wait_for_timeout(35)
  def ticks(n):
   for i in range(0,n,12):
    err=p.evaluate(shoot.STEP,min(12,n-i))
    if err:errors.append(err)
    p.wait_for_timeout(5)
  def snap(name):
   p.evaluate('()=>{shake=0;ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);SC12.refresh();window.__bofFit();}')
   p.screenshot(path=str(OUT/(name+'.png')))
  def truck_setup(diff='normal',black=False):
   p.evaluate('''([diff,black])=>{pilotIndex=PILOTS.findIndex(q=>q.key==='cole');diffKey=diff;DIFF=DIFFS[diff];run.mode='arcade';startRun(1);BOFCinematicDirector.cancel();story=fb2Talk=s6Opening=null;setState(GS.PLAY);stagePlan=[];enemies=[];pBullets=[];eBullets=[];player.invuln=99999;bossActive=subBossActive=false;boss=subBoss=null;subBossDone=true;mt18Warm();}''',[diff,black])
   p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(1)&&mt18Keys().map(k=>XART.rdy(k)).every(Boolean)&&bmfReady("game")}')
   p.evaluate('''black=>{const cfg=_levelCfg(),im=XART.get(cfg.master),range=im.naturalHeight-VH;let found=null;
    for(let y=1200;y<im.naturalHeight-VH-100&&!found;y+=100)for(let x=160;x<worldWidth()-160&&!found;x+=32)
     if([-50,0,50].every(dx=>[-70,0,70].every(dy=>tankDrivable(x+dx,y+180+dy,false))))found={x,y};
    if(!found)throw Error('No native land footprint for truck');mapScroll=range-found.y;drawBG(0);_lastScrollDy=0;window.truckLand=found;
    window.truck=spawnEnemy(black?'s1truckmissile_b':'s1truckmissile',found.x,180,{});truck.x=found.x;truck.y=180;truck._lvlY=found.y+180;
    player.x=found.x;player.y=VH*.86;camX=clamp(player.x-VW/2,0,worldWidth()-VW);MT18.events=[];MT18.shots=MT18.partsDestroyed=0;
    window.mtStats={hull:[],launcher:[],phases:[],shots:[],maxDraws:0};window.__qaTick=()=>{const A=truck._mt18;
     const h=Math.floor(A.wheel)%8;if(!mtStats.hull.includes(h))mtStats.hull.push(h);
     for(const p of A.parts){const f=mt18Frame(p);if(!mtStats.launcher.includes(f))mtStats.launcher.push(f);if(!mtStats.phases.includes(p.phase))mtStats.phases.push(p.phase);}
     for(const q of eBullets)if(q._mt18Missile&&!mtStats.shots.some(s=>s.q===q))mtStats.shots.push({q,vx:q.vx,vy:q.vy,shootable:q._shootable,proof:q._weaponProof,homing:q.homing});
    };}''',black)
  def pixels(name):
   raw=p.evaluate('''()=>{ctx.save();ctx.setTransform(SS,0,0,SS,0,0);ctx.clearRect(0,0,worldWidth(),viewH());mt18Draw(truck);ctx.restore();return ctx.canvas.toDataURL('image/png');}''')
   data=base64.b64decode(raw.split(',',1)[1]);(OUT/(name+'.png')).write_bytes(data);return np.asarray(Image.open(io.BytesIO(data)).convert('RGBA'))
  for diff in ['normal','hard','furious']:
   truck_setup(diff);ticks(85);snap(diff+'-truck-warning');ticks(80);snap(diff+'-truck-launch');ticks(65);snap(diff+'-truck-reload');ticks(360)
   row=p.evaluate('''()=>({diff:diffKey,phases:mtStats.phases,hullFrames:mtStats.hull,launcherFrames:mtStats.launcher,shots:MT18.shots,parts:truck._mt18.parts.map(q=>({id:q.id,hp:q.hp,phase:q.phase})),land:truckLand,missiles:mtStats.shots.map(s=>({shootable:s.shootable,proof:s.proof,homing:s.homing})),draws:MT18.draws})''');measures.append(row)
   check(diff+' truck warns, fires both racks and reloads',row['shots']>=6 and all(s in row['phases'] for s in ['tell','fire','reload','rest']),row)
   check(diff+' truck draws moving wheels and generated launcher poses',len(row['hullFrames'])>=4 and len(row['launcherFrames'])>=13 and row['draws']>0,row)
   check(diff+' missiles are counterable and do not home',row['shots']>=6 and len(row['missiles'])>=3 and all(q['shootable'] and not q['proof'] and not q['homing'] for q in row['missiles']),row['missiles'])
  truck_setup();ticks(145)
  interception=p.evaluate('''()=>{const q=eBullets.find(q=>q._mt18Missile&&!q.dead);if(!q)return false;window.truckIntercepts18=0;const original=ordnanceBreak1002;ordnanceBreak1002=function(b){if(b._mt18Missile)truckIntercepts18++;return original.apply(this,arguments);};run.weapon=0;run.wlevels[0]=1;run.wlevel=1;player.x=q.x;player.y=q.y+100;player.fireCd=0;Input.keys.j=true;return true;}''');ticks(30)
  check('Actual J gunfire shoots down a live truck missile',interception and p.evaluate('truckIntercepts18>0'))
  p.evaluate('Input.keys.j=false')
  truck_setup();ticks(30);before=pixels('truck-clean-pixels')
  hit=p.evaluate('''()=>{const p=truck._mt18.parts[0];_dmgBullet={kind:'bullet',x:truck.x+p.dx,y:truck.y+p.dy,dmg:1};_lastHitX=_dmgBullet.x;hitEnemy(truck,1);return {owner:truck.flash,part:p.flash,hp:p.hp,max:p.maxhp};}''')
  after=pixels('truck-hit-pixels');changed=int(np.count_nonzero((before[:,:,3]>128)&(np.max(np.abs(before[:,:,:3].astype(int)-after[:,:,:3].astype(int)),2)>8)))
  check('Native hull and launcher pixels visibly flash on a real hit',changed>100 and hit['owner']>0 and hit['part']>0,dict(changed=changed,**hit))
  ticks(25);check('Truck owner and module flash timers expire normally',p.evaluate('truck.flash<=0&&truck._mt18.parts.every(q=>q.flash<=0)&&truck._mt18.hullFlash<=0'))
  check('Retina exposes both launcher racks and the cab hull',p.evaluate('_lockTargets().filter(q=>q._retinaOwner===truck).length===3'))
  p.evaluate('''()=>{const A=truck._mt18;A.direct='rackL';_dmgBullet={kind:'missile',x:truck.x-17,y:truck.y-27};hitEnemy(truck,A.parts[0].hp+.1);MT18.shots=0;A.parts[1].cool=0;}''');ticks(230);snap('truck-left-rack-destroyed')
  row=p.evaluate('''()=>({dead:truck.dead,parts:truck._mt18.parts.map(q=>({hp:q.hp,phase:q.phase})),shots:MT18.shots,targets:_lockTargets().filter(q=>/missile truck/.test(q._pieceId||q.kind||q.type||'')).map(q=>({id:q._pieceId,kind:q.kind}))})''')
  check('Destroying one rack removes it while the surviving rack keeps firing',not row['dead'] and row['parts'][0]['hp']==0 and row['parts'][1]['hp']>0 and row['shots']>=3,row)
  check('Destroyed racks leave the live Retina targets',p.evaluate('_lockTargets().filter(q=>q._retinaOwner===truck).length===2'))
  p.evaluate('''()=>{const A=truck._mt18;A.direct='rackR';hitEnemy(truck,A.parts[1].hp+.1);MT18.shots=0;}''');ticks(120);check('Both destroyed racks stop firing without an invulnerable hull',p.evaluate('!truck.dead&&MT18.shots===0&&truck._mt18.hull>0'))
  death=p.evaluate('''()=>{const score=run.score;truck._mt18.direct='hull';hitEnemy(truck,truck._mt18.hull+1);return {reward:run.score-score,dying:truck._dyingT,hp:truck.hp};}''');ticks(90);check('The exposed hull dies through the native enemy reward owner',p.evaluate('truck.dead&&truck.hp<=0') and death['reward']>0,death)
  truck_setup(black=True);ticks(60);snap('black-truck');check('The black truck uses the same working modular bank',p.evaluate('truck._mt18.palette==="black"&&truck._mt18.parts.length===2'))
  for weapon,w,missile in [('machinegun',0,False),('missile',0,True),('laser',3,False),('iceorb',5,False)]:
   truck_setup();ticks(8)
   before=p.evaluate('''([w,missile])=>{run.weapon=w;run.wlevels??={};run.wlevels[w]=1;run.wlevel=1;player.x=truck.x-17;player.y=truck.y+160;player.fireCd=0;Input.keys.j=!missile;run.bombs=20;if(missile)useBomb(null);return truck.hp;}''',[w,missile]);ticks(100)
   row=p.evaluate('''()=>{Input.keys.j=false;return {hp:truck.hp,dead:truck.dead,parts:truck._mt18.parts.map(p=>p.hp),hull:truck._mt18.hull};}''')
   check('Real '+weapon+' projectiles can damage the modular truck',row['hp']<before or row['dead'],dict(before=before,after=row))
  # The boss fixture runs all hazards through updatePlay/drawWorld, not by
  # injecting a wall or setting a column alive for a screenshot.
  for diff in ['normal','hard','furious']:
   p.evaluate('''diff=>{diffKey=diff;DIFF=DIFFS[diff];startRun(2);BOFCinematicDirector.cancel();story=fb2Talk=s6Opening=null;setState(GS.PLAY);stagePlan=[];enemies=[];eBullets=[];pBullets=[];subBossActive=false;subBoss=null;subBossDone=true;boss=null;bossActive=false;spawnBoss('infernoreaver');furnaceSync(boss);furnaceEnter(boss,'core');boss._fz.trans=0;boss._mwStun=0;if(boss._mwBarrier)boss._mwBarrier.active=false;player.invuln=99999;player.x=worldWidth()/2;player.y=VH*.83;s2Vents=[];geysers=[];zoneCols=[];s2VentT=2.3;wfxReset();
    window.hazardStats={zones:0,wall:0,warn:0,geysers:0,wallAndVent:0,side:[],asterisk:0,arrows:0,head:f17Tune()};
    const baseVentDraw=s2VentDraw,baseGet=XART.get,baseDraw=ctx.drawImage;
    if(!window.hazardDrawInstalled){window.hazardDrawInstalled=true;s2VentDraw=function(){window.inSideWarn18=true;try{return baseVentDraw.apply(this,arguments);}finally{window.inSideWarn18=false;}};
     XART.get=function(k){window.hazardKey18=k;return baseGet.apply(this,arguments);};ctx.drawImage=function(){if(window.inSideWarn18){if(/^bmfx_alert_/.test(window.hazardKey18))hazardStats.asterisk++;if(window.hazardKey18==='warn_escape_arrow_0916')hazardStats.arrows++;}return baseDraw.apply(this,arguments);};}
    window.__qaTick=()=>{hazardStats.zones=Math.max(hazardStats.zones,zoneCols.filter(q=>q.hostile).length);hazardStats.wall+=wfx?.fseq?.wave?1:0;hazardStats.warn+=wfx?.fseq?.ph==='alerts'?1:0;const hostile=geysers.filter(q=>q.hostile);hazardStats.geysers+=hostile.length?1:0;if(wfx?.fseq&&s2Vents.some(v=>!v.done))hazardStats.wallAndVent++;for(const v of s2Vents)if(!hazardStats.side.includes(v.side))hazardStats.side.push(v.side);};}''',diff)
   p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(2)&&bmfReady("game")}')
   saved_wall=saved_vent=False
   for i in range(0,2400,12):
    ticks(12)
    state=p.evaluate('({wave:!!wfx?.fseq?.wave,vent:s2Vents.some(v=>!v.done)})')
    if state['wave'] and not saved_wall:snap(diff+'-boss-firewall');saved_wall=True
    if state['vent'] and not saved_vent:snap(diff+'-boss-side-warning');saved_vent=True
   row=p.evaluate('hazardStats');measures.append({'diff':diff,'hazards':row})
   check(diff+' Furnace uses travelling fire walls, never hostile red zone beams',row['zones']==0 and row['wall']>30 and row['warn']>30,row)
   check(diff+' side geysers warn with authored asterisks and arrows',row['geysers']>0 and row['asterisk']>10 and row['arrows']>10 and len(row['side'])==2,row)
   check(diff+' walls and side vents are sequenced rather than simultaneous tells',row['wallAndVent']==0,row)
  check('Hard and Furious sweeps are faster, with Normal unchanged',p.evaluate('''()=>{diffKey='normal';const n=f17Tune();diffKey='hard';const h=f17Tune();diffKey='furious';const f=f17Tune();return n.active===5.8&&h.active===4&&f.active===3&&f.warm===1.45;}'''))
  check('No native page, console or asset errors',not errors,errors)
  browser.close()
finally:stop()
result={'passed':sum(c['passed'] for c in checks),'failed':[c for c in checks if not c['passed']],'errors':errors,'checks':checks,'measures':measures}
(OUT/'results.json').write_text(json.dumps(result,indent=2),encoding='utf-8');print('SUMMARY',result['passed'],'passed',len(result['failed']),'failed',len(errors),'browser errors',flush=True)
sys.exit(bool(result['failed'] or errors))
